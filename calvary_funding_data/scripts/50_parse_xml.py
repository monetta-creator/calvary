"""Phase 4 parse: e-filed 990 / 990-EZ / 990-PF XML (interim/xml_manifest.csv) -> staging tables.

Parser: scripts/lib/xml990.py (namespace-stripped lxml iterparse, schema-version agnostic). Multiprocessing pool,
largest files first.

Outputs (columns follow config/table_specs.md; extras are x_-prefixed):
  interim/stage_fact_org_financials__xml.csv   one row per return; 990 Parts I/VIII/IX/X, 990-EZ, 990-PF
  interim/stage_fact_grants__xml.csv           990-PF grants paid + approved for future payment; Schedule I Part II
  interim/stage_fact_roles__xml.csv            990 Part VII-A, 990-EZ Part IV, 990-PF officers + highest-paid employees
  interim/stage_fact_org_relationships__xml.csv  Schedule R Parts I-V
  interim/org_profile__xml.csv                 mission, top-3 programs, website, formation year, domicile, counts,
                                               filer city/state/zip; street only on each EIN's latest return
  interim/xml_schedule_i_part3.csv             Schedule I Part III (grants to individuals), aggregate lines only
  interim/xml_daf_filter_totals.csv            DAF1 sponsors: Schedule I rows/dollars kept (DC/MD/VA) vs filtered out
  interim/xml_parse_errors.csv                 returns that failed to parse

Decisions
  - tax_year = XML TaxYr (fallback: period rule); fiscal_year / fye_month = period-end year / month.
  - source_id = bulk_irs_xml when the file came from an IRS ZIP, else bulk_gt_datalake. retrieved_date = raw file stamp.
  - Financial fields are single documented lines, except these sums of documented lines: cash_savings_eoy (990 Part X
    lines 1+2; 990-PF Part II lines 1+2; 990-EZ line 22, which includes investments), 990-PF investment_income
    (Part I lines 3+4a+6a, the scope of 990 Part I line 10) and 990-PF compensation_total (Part I lines 13-15, the
    scope of 990 Part I line 15). 990 investment_income / other_revenue are Part I lines 10 / 11.
  - 990-PF grants: amount_kind cash for grants paid (the form has one amount column), pledge for approved-future.
    Schedule I: amount = cash + noncash, amount_kind cash / noncash / mixed.
  - 990-PF rows whose recipient sits in RecipientPersonNm and doesn't look like an organization (name keywords or a
    charity foundation-status code) are grants to individuals: name, city and zip are blanked (x_recipient_kind =
    individual_redacted); state, amount and purpose are kept.
  - Lump-sum rows that point to an attachment ("SEE ATTACHED SCHEDULE", "See Statement 27A", "VARIOUS") are kept
    (they carry the documented amount) with x_placeholder_row = 1 and a blank recipient_name_norm.
  - DAF1 sponsors: only Schedule I rows with recipient state DC/MD/VA are kept; national totals go to
    xml_daf_filter_totals.csv and the build log.
  - Roles: 990 flags come from the Part VII-A checkboxes; 990-EZ / 990-PF flags and officer-vs-trustee come from a
    title regex (x_flags_basis). No addresses; no person_id.

Usage: .venv/bin/python scripts/50_parse_xml.py [--workers 5] [--limit N]
"""
from __future__ import annotations

import argparse
import csv
import multiprocessing as mp
import re
import sys
import time
from collections import Counter
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from lib import xml990  # noqa: E402
from lib.common import CLEAN, INTERIM, ROOT, log, norm_ein, norm_name, rel  # noqa: E402
from lib.tagging import tag_text  # noqa: E402

DAF_KEEP = {"DC", "MD", "VA"}
OUT = {
    "fin": INTERIM / "stage_fact_org_financials__xml.csv",
    "grants": INTERIM / "stage_fact_grants__xml.csv",
    "roles": INTERIM / "stage_fact_roles__xml.csv",
    "rels": INTERIM / "stage_fact_org_relationships__xml.csv",
    "profile": INTERIM / "org_profile__xml.csv",
    "p3": INTERIM / "xml_schedule_i_part3.csv",
    "daf": INTERIM / "xml_daf_filter_totals.csv",
    "errors": INTERIM / "xml_parse_errors.csv",
}

FIN_COLS = [
    "ein", "tax_year", "fiscal_year", "fye_month", "tax_period_end", "return_type", "object_id", "is_amended",
    "source_id", "retrieved_date", "preferred", "conflict_flag", "confidence", "basis",
    "total_revenue", "contributions_total", "federated_campaigns", "membership_dues", "fundraising_event_contributions",
    "related_org_contributions", "government_grants", "other_contributions", "noncash_contributions",
    "program_service_revenue", "investment_income", "special_events_net", "other_revenue",
    "total_expenses", "program_expenses", "management_expenses", "fundraising_expenses", "grants_paid",
    "compensation_total", "total_assets_eoy", "total_liabilities_eoy", "net_assets_eoy", "cash_savings_eoy",
    "pf_fmv_assets_eoy", "pf_total_grants_paid", "pf_qualifying_distributions", "pf_contributions_received",
]
GRANT_COLS = [
    "grant_id", "funder_id", "funder_ein", "funder_name_raw", "recipient_ein", "recipient_name_raw",
    "recipient_name_norm", "recipient_city", "recipient_state", "recipient_zip5", "tax_year", "fiscal_year",
    "grant_date", "year_basis", "amount", "amount_band_min", "amount_band_max", "amount_kind", "cumulative_flag",
    "purpose_text", "program_area_tags", "source_type", "object_id", "source_id", "match_method", "match_score",
    "retrieved_date", "confidence", "basis",
    "x_cash_amt", "x_noncash_amt", "x_noncash_desc", "x_valuation_method", "x_irc_section", "x_foundation_status",
    "x_relationship", "x_recipient_country", "x_recipient_kind", "x_return_type", "x_fye_month", "x_daf_dmv_only",
    "x_placeholder_row", "x_xpath", "x_seq",
]
ROLE_COLS = [
    "role_id", "person_id", "ein", "org_name", "tax_year", "fiscal_year", "name_display", "name_norm", "title",
    "role_type", "is_officer", "is_director_trustee", "is_key_employee", "is_highest_comp", "is_former",
    "avg_hours_per_week", "reportable_comp_org", "source_id", "object_id", "retrieved_date", "confidence", "basis",
    "x_return_type", "x_part", "x_flags_basis", "x_hours_related_org", "x_comp_related_org", "x_other_comp",
    "x_benefits", "x_expense_allowance", "x_institutional_trustee", "x_is_business_name", "x_name_looks_org",
    "x_fye_month", "x_xpath", "x_seq",
]
REL_COLS = [
    "rel_id", "org_a_ein", "org_a_name", "org_b_ein", "org_b_name", "rel_type", "direction", "tax_year", "amount",
    "evidence", "person_id", "source_id", "confidence", "basis", "retrieved_date",
    "x_object_id", "x_fiscal_year", "x_schedule_r_part", "x_relationship_kind", "x_direct_controlling_entity",
    "x_controlled_org_ind", "x_primary_activity", "x_legal_domicile", "x_org_b_state", "x_org_b_country",
    "x_exempt_code_section", "x_public_charity_status", "x_entity_type", "x_predominant_income",
    "x_share_total_income", "x_share_eoy_assets", "x_ownership_pct", "x_total_income", "x_eoy_assets",
    "x_transaction_type", "x_amount_method", "x_org_b_ein_basis", "x_xpath",
]
PROFILE_COLS = [
    "ein", "tax_year", "fiscal_year", "fye_month", "return_type", "object_id", "org_name", "mission", "mission_part3",
    *[f"program_{i}_{k}" for i in (1, 2, 3) for k in ("desc", "expense", "grants", "revenue")],
    "program_other_expense", "program_total_expense", "website", "formation_year", "legal_domicile_state",
    "employee_count", "volunteer_count", "voting_members", "city", "state", "zip5", "country", "street",
    "is_latest_return", "source_id", "retrieved_date",
]
P3_COLS = ["ein", "tax_year", "fiscal_year", "object_id", "grant_type", "recipient_cnt", "cash_amt", "noncash_amt",
           "valuation_method", "noncash_desc", "x_xpath", "source_id", "retrieved_date"]


def retrieved(path: str) -> str:
    m = re.search(r"/(\d{4})(\d{2})(\d{2})T\d{6}_", "/" + path)
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else ""


def ty_from_end(end: str) -> int:
    y, m = int(end[:4]), int(end[5:7])
    return y if m == 12 else y - 1


def work(task: dict) -> dict:
    path = ROOT / task["path"]
    try:
        d = xml990.extract(path, keep_states=DAF_KEEP if task["is_daf"] else None)
    except Exception as ex:  # noqa: BLE001
        try:
            ver = xml990.schema_version(path)
        except Exception:  # noqa: BLE001
            ver = None
        return {"error": {"object_id": task["object_id"], "ein": task["ein"], "path": task["path"],
                          "schema_version": ver, "error": repr(ex)[:300]}}
    h = d["header"]
    ein = norm_ein(h["ein"]) or task["ein"]
    end = h["period_end"] or ""
    tax_year = int(h["tax_yr"]) if (h["tax_yr"] or "").isdigit() else (ty_from_end(end) if end else int(task["tax_year"]))
    fiscal_year = int(end[:4]) if end else None
    fye_month = int(end[5:7]) if end else None
    src = "bulk_irs_xml" if task["fetch_source"].startswith("irs") else "bulk_gt_datalake"
    rd = retrieved(task["path"])
    oid = task["object_id"]
    form = d["form"]
    name = h["name"]
    base = {"source_id": src, "retrieved_date": rd, "confidence": "high", "basis": "documented"}

    # ---- financials
    gs = d["grant_stats"]
    fin = {"ein": ein, "tax_year": tax_year, "fiscal_year": fiscal_year, "fye_month": fye_month,
           "tax_period_end": xml990.last_day(end), "return_type": form, "object_id": oid,
           "is_amended": d["is_amended"], **base, "preferred": "", "conflict_flag": ""}
    fin.update(d["fin"])
    fin.update({
        "x_return_version": d["return_version"], "x_filer_name": name, "x_period_begin": h["period_begin"],
        "x_manifest_ein_mismatch": int(ein != task["ein"]), "x_n_submissions": task["n_submissions"],
        "x_superseded_object_ids": task["superseded_object_ids"], "x_scope_rules": task["scope_rules"],
        "x_fetch_source": task["fetch_source"],
        "x_has_schedule_i": int(d["has_sched"]["I"]), "x_has_schedule_r": int(d["has_sched"]["R"]),
        "x_pf_paid_rows_n": gs.get("pf_grants_paid_n", 0), "x_pf_paid_rows_sum": gs.get("pf_grants_paid_cash", 0),
        "x_pf_future_rows_n": gs.get("pf_grants_approved_future_n", 0),
        "x_pf_future_rows_sum": gs.get("pf_grants_approved_future_cash", 0),
        "x_si_rows_n": gs.get("schedule_i_n", 0), "x_si_rows_cash_sum": gs.get("schedule_i_cash", 0),
        "x_si_rows_noncash_sum": gs.get("schedule_i_noncash", 0),
        "x_si_rows_kept_n": sum(1 for g in d["grants"] if g["source_type"] == "schedule_i"),
        "x_pf_paid_placeholder_n": sum(1 for g in d["grants"] if g["source_type"] == "pf_grants_paid"
                                       and xml990.is_placeholder(g["name"], g.get("purpose"))),
        "x_pf_paid_placeholder_sum": sum(g["cash"] or 0 for g in d["grants"] if g["source_type"] == "pf_grants_paid"
                                         and xml990.is_placeholder(g["name"], g.get("purpose"))),
        "x_si_part3_cash_sum": sum(p["cash"] or 0 for p in d["sched_i_p3"]),
        "x_si_part3_recipient_cnt": sum(p["recipient_cnt"] or 0 for p in d["sched_i_p3"]),
        "x_si_total_501c3_cnt": d["sched_i_meta"].get("total_501c3_cnt"),
        "x_si_total_other_cnt": d["sched_i_meta"].get("total_other_cnt"),
    })

    # ---- grants
    grants = []
    for g in d["grants"]:
        st = g["source_type"]
        cash, non = g["cash"], g["noncash"]
        amount = None if cash is None and non is None else (cash or 0) + (non or 0)
        if st == "schedule_i":
            kind = "mixed" if (cash or 0) and (non or 0) else ("noncash" if (non or 0) and not (cash or 0) else "cash")
            rkind = "org"
        else:
            kind = "cash" if st == "pf_grants_paid" else "pledge"
            rkind = xml990.recipient_kind(g)
        redact = rkind == "individual_redacted"
        rname = None if redact else g["name"]
        purpose = g.get("purpose")
        placeholder = xml990.is_placeholder(g["name"], purpose)
        grants.append({
            "grant_id": "", "funder_id": ein, "funder_ein": ein, "funder_name_raw": name,
            "recipient_ein": norm_ein(g.get("ein")) if g.get("ein") else "",
            "recipient_name_raw": rname, "recipient_name_norm": norm_name(rname) if rname and not placeholder else "",
            "recipient_city": None if redact else g["city"], "recipient_state": g["state"],
            "recipient_zip5": None if redact else g["zip5"], "tax_year": tax_year, "fiscal_year": fiscal_year,
            "grant_date": "", "year_basis": "funder_tax_year", "amount": amount, "amount_band_min": "",
            "amount_band_max": "", "amount_kind": kind, "cumulative_flag": 0, "purpose_text": purpose,
            "program_area_tags": tag_text(purpose), "source_type": st, "object_id": oid, "source_id": src,
            "match_method": "", "match_score": "", "retrieved_date": rd, "confidence": "high", "basis": "documented",
            "x_cash_amt": cash, "x_noncash_amt": non, "x_noncash_desc": g.get("noncash_desc"),
            "x_valuation_method": g.get("valuation"), "x_irc_section": g.get("irc_section"),
            "x_foundation_status": g.get("foundation_status"), "x_relationship": g.get("relationship"),
            "x_recipient_country": g["country"], "x_recipient_kind": rkind, "x_return_type": form,
            "x_fye_month": fye_month, "x_daf_dmv_only": int(task["is_daf"] and st == "schedule_i"),
            "x_placeholder_row": int(placeholder),
            "x_xpath": g["xpath"], "x_seq": g["seq"],
        })

    # ---- roles
    roles = []
    for r in d["roles"]:
        if not r.get("name_display"):
            continue
        nm = r["name_display"]
        roles.append({
            "role_id": "", "person_id": "", "ein": ein, "org_name": name, "tax_year": tax_year,
            "fiscal_year": fiscal_year, "name_display": nm,
            "name_norm": norm_name(nm) if r["is_business"] else xml990.norm_person(nm), "title": r.get("title"),
            "role_type": r["role_type"], "is_officer": r.get("is_officer"),
            "is_director_trustee": r.get("is_director_trustee"), "is_key_employee": r.get("is_key_employee"),
            "is_highest_comp": r.get("is_highest_comp"), "is_former": r.get("is_former"),
            "avg_hours_per_week": r.get("avg_hours_per_week"), "reportable_comp_org": r.get("reportable_comp_org"),
            "source_id": src, "object_id": oid, "retrieved_date": rd, "confidence": "high", "basis": "documented",
            "x_return_type": form, "x_part": r["x_part"], "x_flags_basis": r["x_flags_basis"],
            "x_hours_related_org": r.get("x_hours_related_org"), "x_comp_related_org": r.get("x_comp_related_org"),
            "x_other_comp": r.get("x_other_comp"), "x_benefits": r.get("x_benefits"),
            "x_expense_allowance": r.get("x_expense_allowance"),
            "x_institutional_trustee": r.get("x_institutional_trustee"), "x_is_business_name": r["is_business"],
            "x_name_looks_org": int(bool(xml990.ORG_NAME_RE.search(nm))), "x_fye_month": fye_month,
            "x_xpath": r["xpath"], "x_seq": r["seq"],
        })

    # ---- Schedule R
    rels = []
    by_name = {norm_name(x["name"]): norm_ein(x["ein"]) for x in d["related"] if x["ein"] and x["name"]}
    for x in d["related"]:
        b_ein, b_basis = (norm_ein(x["ein"]) if x["ein"] else None), "documented" if x["ein"] else ""
        if not b_ein and x["part"] == "V":
            b_ein = by_name.get(norm_name(x["name"]))
            b_basis = "matched_by_name_within_return" if b_ein else ""
        ev = [f"Schedule R Part {x['part']} ({x['kind'].replace('_', ' ')})"]
        for lab, k in (("primary activity", "primary_activity"), ("domicile", "legal_domicile"),
                       ("exempt section", "exempt_code_section"), ("public charity status", "public_charity_status"),
                       ("entity type", "entity_type"), ("direct controlling entity", "direct_controlling_entity"),
                       ("transaction type", "transaction_type"), ("ownership pct", "ownership_pct")):
            if x.get(k):
                ev.append(f"{lab}: {x[k]}")
        if x.get("controlled_org") is not None:
            ev.append(f"controlled org: {'yes' if x['controlled_org'] else 'no'}")
        rels.append({
            "rel_id": "", "org_a_ein": ein, "org_a_name": name, "org_b_ein": b_ein, "org_b_name": x["name"],
            "rel_type": "schedule_r_related", "direction": "undirected", "tax_year": tax_year, "amount": x["amount"],
            "evidence": "; ".join(ev), "person_id": "", "source_id": src, "confidence": "high", "basis": "documented",
            "retrieved_date": rd, "x_object_id": oid, "x_fiscal_year": fiscal_year, "x_schedule_r_part": x["part"],
            "x_relationship_kind": x["kind"], "x_direct_controlling_entity": x["direct_controlling_entity"],
            "x_controlled_org_ind": x["controlled_org"], "x_primary_activity": x["primary_activity"],
            "x_legal_domicile": x["legal_domicile"], "x_org_b_state": x["state"], "x_org_b_country": x["country"],
            "x_exempt_code_section": x["exempt_code_section"], "x_public_charity_status": x["public_charity_status"],
            "x_entity_type": x["entity_type"], "x_predominant_income": x["predominant_income"],
            "x_share_total_income": x["share_total_income"], "x_share_eoy_assets": x["share_eoy_assets"],
            "x_ownership_pct": x["ownership_pct"], "x_total_income": x["total_income"], "x_eoy_assets": x["eoy_assets"],
            "x_transaction_type": x["transaction_type"], "x_amount_method": x["amount_method"],
            "x_org_b_ein_basis": b_basis, "x_xpath": x["xpath"],
        })

    # ---- profile
    p = d["profile"]
    prof = {"ein": ein, "tax_year": tax_year, "fiscal_year": fiscal_year, "fye_month": fye_month, "return_type": form,
            "object_id": oid, "org_name": name, "mission": p["mission"], "mission_part3": p["mission_part3"],
            "program_other_expense": p["program_other_expense"], "program_total_expense": p["program_total_expense"],
            "website": p["website"], "formation_year": p["formation_year"],
            "legal_domicile_state": p["legal_domicile_state"], "employee_count": p["employee_count"],
            "volunteer_count": p["volunteer_count"], "voting_members": p["voting_members"], "city": h["city"],
            "state": h["state"], "zip5": h["zip5"], "country": h["country"], "street": h["street"],
            "is_latest_return": 0, "source_id": src, "retrieved_date": rd}
    for i, pg in enumerate(p["programs"][:3], 1):
        for k in ("desc", "expense", "grants", "revenue"):
            prof[f"program_{i}_{k}"] = pg.get(k)

    p3 = [{"ein": ein, "tax_year": tax_year, "fiscal_year": fiscal_year, "object_id": oid,
           "grant_type": x["grant_type"], "recipient_cnt": x["recipient_cnt"], "cash_amt": x["cash"],
           "noncash_amt": x["noncash"], "valuation_method": x["valuation"], "noncash_desc": x["noncash_desc"],
           "x_xpath": x["xpath"], "source_id": src, "retrieved_date": rd} for x in d["sched_i_p3"]]

    daf = None
    if task["is_daf"]:
        fb, fa = d["filtered_by_state"], d["filtered_amt_by_state"]
        kept = [g for g in grants if g["source_type"] == "schedule_i"]
        daf = {"ein": ein, "name": name, "tax_year": tax_year, "object_id": oid,
               "si_rows_total": gs.get("schedule_i_n", 0),
               "si_amount_total": gs.get("schedule_i_cash", 0) + gs.get("schedule_i_noncash", 0),
               "rows_kept_dmv": len(kept), "amount_kept_dmv": sum(g["amount"] or 0 for g in kept),
               "rows_kept_dc": sum(1 for g in kept if g["recipient_state"] == "DC"),
               "amount_kept_dc": sum(g["amount"] or 0 for g in kept if g["recipient_state"] == "DC"),
               "rows_filtered": sum(fb.values()), "amount_filtered": sum(fa.values()),
               "top_filtered_states": ";".join(f"{k}:{v}" for k, v in fa.most_common(5))}
    return {"fin": fin, "grants": grants, "roles": roles, "rels": rels, "profile": prof, "p3": p3, "daf": daf,
            "version": d["return_version"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=5)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--test-outdir", default="", help="write outputs here instead of interim/ and skip the build log")
    a = ap.parse_args()
    t0 = time.time()
    out = {k: (Path(a.test_outdir) / v.name if a.test_outdir else v) for k, v in OUT.items()}
    _log = (lambda *x: None) if a.test_outdir else log

    m = pd.read_csv(INTERIM / "xml_manifest.csv", dtype=str, keep_default_na=False)
    m = m[m["status"] == "ok"].copy()
    u = pd.read_csv(CLEAN / "dim_universe_membership.csv", dtype=str)
    daf = set(u.loc[u["rule_id"] == "DAF1", "ein"].map(norm_ein))
    m["is_daf"] = m["ein"].isin(daf)
    m["b"] = m["bytes"].astype(int)
    m = m.sort_values("b", ascending=False)
    if a.limit:
        m = m.head(a.limit)
    tasks = m.drop(columns=["b"]).to_dict("records")
    print(f"parsing {len(tasks):,} returns with {a.workers} workers", flush=True)

    tmp = {k: v.with_suffix(".tmp") for k, v in out.items()}
    fh = {k: open(tmp[k], "w", newline="", encoding="utf-8") for k in ("grants", "roles", "rels")}
    w = {"grants": csv.DictWriter(fh["grants"], GRANT_COLS), "roles": csv.DictWriter(fh["roles"], ROLE_COLS),
         "rels": csv.DictWriter(fh["rels"], REL_COLS)}
    for x in w.values():
        x.writeheader()
    fins, profs, p3s, dafs, errs = [], [], [], [], []
    n = Counter()
    versions = Counter()
    with mp.get_context("spawn").Pool(a.workers, maxtasksperchild=300) as pool:
        for i, r in enumerate(pool.imap_unordered(work, tasks, chunksize=2), 1):
            if "error" in r:
                errs.append(r["error"])
            else:
                versions[r["version"]] += 1
                fins.append(r["fin"])
                profs.append(r["profile"])
                p3s.extend(r["p3"])
                if r["daf"]:
                    dafs.append(r["daf"])
                for k in ("grants", "roles", "rels"):
                    w[k].writerows(r[k])
                    n[k] += len(r[k])
            if i % 2000 == 0:
                msg = (f"- {i:,}/{len(tasks):,} parsed in {(time.time() - t0) / 60:.1f} min; grants {n['grants']:,}, "
                       f"roles {n['roles']:,}, relationships {n['rels']:,}; errors {len(errs)}")
                print(msg, flush=True)
                _log("50_parse_xml: progress", msg)
    for f in fh.values():
        f.close()

    fin = pd.DataFrame(fins)
    xcols = sorted(c for c in fin.columns if c.startswith("x_"))
    fin = fin.reindex(columns=FIN_COLS + xcols).sort_values(["ein", "tax_year", "return_type", "object_id"])
    fin.to_csv(tmp["fin"], index=False)

    prof = pd.DataFrame(profs).reindex(columns=PROFILE_COLS)
    prof = prof.sort_values(["ein", "tax_year", "fiscal_year", "object_id"])
    latest = prof.groupby("ein").tail(1).index
    prof.loc[latest, "is_latest_return"] = 1
    prof.loc[~prof.index.isin(latest), "street"] = None
    prof.to_csv(tmp["profile"], index=False)
    pd.DataFrame(p3s, columns=P3_COLS).to_csv(tmp["p3"], index=False)
    dafdf = pd.DataFrame(dafs).sort_values(["ein", "tax_year"]) if dafs else pd.DataFrame()
    dafdf.to_csv(tmp["daf"], index=False)
    pd.DataFrame(errs, columns=["object_id", "ein", "path", "schema_version", "error"]).to_csv(tmp["errors"], index=False)
    for k in out:
        tmp[k].replace(out[k])

    lines = [
        f"- parsed {len(fin):,} of {len(tasks):,} returns in {(time.time() - t0) / 60:.1f} min; errors {len(errs)} "
        f"-> {OUT['errors'].name}",
        f"- {rel(OUT['fin'])}: {len(fin):,} rows {fin['return_type'].value_counts().to_dict()}; amended "
        f"{int(fin['is_amended'].fillna(0).astype(int).sum())}; EIN differs from index {int(fin['x_manifest_ein_mismatch'].sum())}",
        f"- {rel(OUT['grants'])}: {n['grants']:,} rows",
        f"- {rel(OUT['roles'])}: {n['roles']:,} rows",
        f"- {rel(OUT['rels'])}: {n['rels']:,} rows",
        f"- {rel(OUT['profile'])}: {len(prof):,} rows ({prof['ein'].nunique():,} EINs; street kept on latest return only)",
        f"- {rel(OUT['p3'])}: {len(p3s):,} Schedule I Part III lines (aggregates, no names)",
        f"- schema versions: {dict(sorted(versions.items()))}",
    ]
    if len(dafdf):
        dafdf["name"] = dafdf["ein"].map(dafdf.sort_values("tax_year").groupby("ein")["name"].last())
        g = dafdf.groupby(["ein", "name"]).agg(rows_total=("si_rows_total", "sum"), amt_total=("si_amount_total", "sum"),
                                               rows_kept=("rows_kept_dmv", "sum"), amt_kept=("amount_kept_dmv", "sum"),
                                               amt_filtered=("amount_filtered", "sum")).reset_index()
        lines.append("- DAF1 sponsors, Schedule I kept only for DC/MD/VA recipients (all years in scope):")
        for _, r in g.sort_values("amt_total", ascending=False).iterrows():
            lines.append(f"  - {r['name']} ({r['ein']}): national {int(r['rows_total']):,} rows / ${r['amt_total'] / 1e6:,.1f}M; "
                         f"kept DMV {int(r['rows_kept']):,} / ${r['amt_kept'] / 1e6:,.1f}M; filtered out ${r['amt_filtered'] / 1e6:,.1f}M")
    _log("50_parse_xml: done", "\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
