"""Phase 5: convert Phase 1 extracts (raw/inputs_extracted/) into staging rows for the clean model.

Outputs (interim/):
  stage_fact_org_financials__inputs.csv   audited statements (FY13-FY23, incl. FY14/FY22 audits found online
                                          in interim/web_new_audit_financials.csv) + 990 PDFs (Part I/VIII/IX/X)
  stage_fact_gov_awards__inputs.csv       audit SEFA lines (FY22 from web, FY23 from inputs/)
  stage_fact_grants__inputs.csv           CRM export (one row per funder, cumulative), annual-report and
                                          support-page funder lists, government grantors named in audit notes
  stage_fact_roles__inputs.csv            990 PDF Part VII-A people; board/leadership lists in annual reports
  stage_supp_*.csv                        Calvary program metrics, strategic-plan targets, donor band counts

Conventions: Calvary FYE is September, so tax_year = fiscal_year - 1 and tax_period_end = {fiscal_year}-09-30.
Usage: python scripts/60_stage_inputs.py
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import INTERIM, RAW, log, norm_name, today
from lib.tagging import tag_text

X = RAW / "inputs_extracted"
CAL = "521307706"
CAL_NAME = "Calvary Women's Services Inc"

# audit line_item_std -> fact_org_financials field (summed within a document-year, total net-asset class)
AUDIT_MAP = {
    "rev_total": "total_revenue",
    "rev_contributions_private": "other_contributions",
    "rev_gov_federal": "government_grants", "rev_gov_state_local": "government_grants",
    "rev_gov_unspecified": "government_grants", "rev_gov_federal_and_local": "government_grants",
    "rev_ppp_forgiveness": "government_grants",   # PPP loan forgiveness: most 990s report it on Part VIII 1e
    "net_assets_end": "net_assets_eoy",
    "rev_inkind": "noncash_contributions",
    "rev_special_events_net": "special_events_net",
    "rev_investment": "investment_income",
    "rev_other": "other_revenue",
    "exp_total": "total_expenses", "exp_program_total": "program_expenses",
    "exp_mgmt_general": "management_expenses", "exp_fundraising": "fundraising_expenses",
    "total_assets": "total_assets_eoy", "total_liabilities": "total_liabilities_eoy",
    "net_assets_total": "net_assets_eoy", "cash": "cash_savings_eoy",
}
# 990 PDF (part, line, column) -> field
F990_MAP = {
    ("I", "12", "current_year"): "total_revenue", ("I", "8", "current_year"): "contributions_total",
    ("I", "9", "current_year"): "program_service_revenue", ("I", "10", "current_year"): "investment_income",
    ("I", "11", "current_year"): "other_revenue", ("I", "13", "current_year"): "grants_paid",
    ("I", "15", "current_year"): "compensation_total", ("I", "18", "current_year"): "total_expenses",
    ("I", "16b", "current_year"): "fundraising_expenses",
    ("I", "20", "end_of_year"): "total_assets_eoy", ("I", "21", "end_of_year"): "total_liabilities_eoy",
    ("I", "22", "end_of_year"): "net_assets_eoy",
    ("VIII", "1a", "inner_box"): "federated_campaigns", ("VIII", "1b", "inner_box"): "membership_dues",
    ("VIII", "1c", "inner_box"): "fundraising_event_contributions", ("VIII", "1d", "inner_box"): "related_org_contributions",
    ("VIII", "1e", "inner_box"): "government_grants", ("VIII", "1f", "inner_box"): "other_contributions",
    ("VIII", "1g", "inner_box"): "noncash_contributions", ("VIII", "8c", "A_total"): "special_events_net",
    ("IX", "25", "B_program"): "program_expenses", ("IX", "25", "C_mgmt_general"): "management_expenses",
    ("IX", "25", "D_fundraising"): "fundraising_expenses",
}


def fin_base(fy: int, rt: str, sid: str) -> dict:
    return {"ein": CAL, "tax_year": fy - 1, "fiscal_year": fy, "fye_month": 9, "tax_period_end": f"{fy}-09-30",
            "return_type": rt, "object_id": "", "is_amended": 0, "source_id": sid, "retrieved_date": today(),
            "confidence": "high", "basis": "documented"}


def stage_financials() -> pd.DataFrame:
    rows = []
    frames = [pd.read_csv(X / "audit_financials.csv")]
    if (INTERIM / "web_new_audit_financials.csv").exists():   # audits found online by scripts/43_web_calvary.py
        frames.append(pd.read_csv(INTERIM / "web_new_audit_financials.csv"))
    a = pd.concat(frames, ignore_index=True)
    a["is_prior_year_comparative"] = a.is_prior_year_comparative.astype(str).str.lower() == "true"
    # SOA lines: use the total net-asset column; SFP lines carry no net-asset class (blank or 'n/a')
    a = a[(a.net_asset_class.isin(["total", "n/a"]) | a.net_asset_class.isna()) & a.line_item_std.isin(AUDIT_MAP)]
    current = set(a[~a.is_prior_year_comparative].fiscal_year)
    # comparatives are used only for fiscal years that have no audit of their own (e.g. FY22 from the FY23 audit)
    a = a[~a.is_prior_year_comparative | ~a.fiscal_year.isin(current)]
    for (sid, fy, comp), g in a.groupby(["source_id", "fiscal_year", "is_prior_year_comparative"]):
        r = fin_base(int(fy), "audit", sid)
        for std, grp in g.groupby("line_item_std"):
            fld = AUDIT_MAP[std]
            if std == "net_assets_total" and "net_assets_eoy" in r:
                continue   # SOA end-of-year net assets and SFP total net assets are the same figure
            r[fld] = int(r.get(fld, 0) + grp.amount.sum())
        if comp:
            r["confidence"], r["x_note"] = "medium", "prior-year comparative column of the following year's audit"
        rows.append(r)
    f = pd.read_csv(X / "form990_pdf_financials.csv", dtype={"line": str})
    for (sid, ty), g in f.groupby(["source_id", "tax_year"]):
        r = fin_base(int(ty) + 1, "990_pdf", sid)
        for x in g.itertuples():
            fld = F990_MAP.get((x.part, str(x.line), x.column))
            if fld and fld not in r:
                r[fld] = int(x.amount)
        if len(r) > 12:
            rows.append(r)
    return pd.DataFrame(rows)


def stage_sefa() -> pd.DataFrame:
    s = pd.read_csv(X / "sefa_federal_awards.csv", dtype=str)
    if (INTERIM / "web_new_audit_sefa.csv").exists():
        s = pd.concat([s, pd.read_csv(INTERIM / "web_new_audit_sefa.csv", dtype=str)], ignore_index=True)
    out = pd.DataFrame({
        "recipient_ein": CAL, "recipient_uei": "KMGRTKET2KJ1", "recipient_name_raw": CAL_NAME,
        "awarding_agency": s.federal_agency, "funding_agency": s.federal_agency, "program_name": s.program_name,
        "assistance_listing": s.assistance_listing, "award_id": s.pass_through_award_id.fillna(""),
        "award_type": "grant",
        "flow_type": s.pass_through_entity.fillna("").map(lambda p: "pass_through_expenditure" if p else "prime"),
        "pass_through_entity": s.pass_through_entity, "pass_through_ein": "",
        "period_start": s.fiscal_year.map(lambda y: f"{int(y) - 1}-10-01"),
        "period_end": s.fiscal_year.map(lambda y: f"{y}-09-30"),
        "fiscal_year": s.fiscal_year, "fiscal_year_basis": "org_fy",
        "amount": pd.to_numeric(s.amount).astype("Int64"), "amount_type": "expenditure",
        "source_type": "audit_sefa", "source_id": s.source_id, "source_page": s.page, "conflict_flag": 0,
        "retrieved_date": today(), "confidence": "high", "basis": "documented", "x_note": s.notes})
    return out


def band(v):
    return pd.to_numeric(v, errors="coerce").astype("Int64")


def stage_grants() -> pd.DataFrame:
    crm = pd.read_csv(X / "crm_funders_2023_2026.csv", dtype=str)
    num_g = pd.to_numeric(crm.NUM_GIFTS, errors="coerce")
    tot = pd.to_numeric(crm.GIFT_TOTAL, errors="coerce")
    last = pd.to_numeric(crm.LAST_CONTRIB_AMT, errors="coerce")
    inconsistent = (num_g == 1) & (tot > last + 0.5)
    c = pd.DataFrame({
        "funder_name_raw": crm.last_name, "x_funder_city": crm.city, "x_funder_state": crm.state,
        "x_funder_type_guess": crm.org_type_guess,
        "recipient_ein": CAL, "recipient_name_raw": CAL_NAME, "recipient_name_norm": norm_name(CAL_NAME),
        "recipient_city": "Washington", "recipient_state": "DC", "recipient_zip5": "20020",
        "tax_year": "", "fiscal_year": "", "grant_date": crm.LAST_CONTRIB_DATE, "year_basis": "gift_date",
        "amount": tot.round().astype("Int64"), "amount_kind": "unknown", "cumulative_flag": 1,
        "purpose_text": "", "program_area_tags": "", "source_type": "crm", "object_id": "",
        "source_id": crm.source_id, "match_method": "", "match_score": "", "retrieved_date": today(),
        "confidence": inconsistent.map({True: "low", False: "medium"}), "basis": "documented",
        "x_last_gift_amount": last.round().astype("Int64"), "x_num_gifts": num_g.astype("Int64"),
        "x_window": "assumed 2023-10..2026-10 (A1); grant_date = last gift date",
        "x_note": inconsistent.map({True: "NUM_GIFTS=1 but GIFT_TOTAL > last gift: total may span pre-window gifts",
                                    False: ""})})
    fm = pd.read_csv(X / "funder_mentions.csv", dtype=str)
    st = fm.document.str.contains("Support", case=False).map({True: "support_page", False: "annual_report"})
    st = st.where(~fm.document.str.contains("Audit|FS", case=True), "audit_note")
    m = pd.DataFrame({
        "funder_name_raw": fm.funder_name_raw, "x_funder_type_guess": fm.org_type_guess,
        "recipient_ein": CAL, "recipient_name_raw": CAL_NAME, "recipient_name_norm": norm_name(CAL_NAME),
        "recipient_city": "Washington", "recipient_state": "DC", "recipient_zip5": "20020",
        "tax_year": "", "fiscal_year": fm.fiscal_year, "grant_date": "", "year_basis": "report_year",
        "amount": pd.Series([pd.NA] * len(fm), dtype="Int64"), "amount_band_min": band(fm.band_min),
        "amount_band_max": band(fm.band_max),
        "amount_kind": fm.in_kind_flag.fillna("").map(lambda v: "noncash" if str(v).lower() == "true" else "unknown"),
        "cumulative_flag": st.map({"support_page": 1}).fillna(0).astype(int),
        "purpose_text": "", "program_area_tags": "", "source_type": st, "object_id": "",
        "source_id": fm.source_id, "retrieved_date": today(),
        "confidence": fm.truncated.astype(str).str.lower().map({"true": "low"}).fillna("medium"),
        "basis": "documented", "x_gift_band_raw": fm.gift_band_raw, "x_section": fm.section_heading,
        "x_truncated": fm.truncated, "x_report_year": fm.report_year,
        "x_note": st.map({"support_page": "support page lists supporters 'over the years' (current as of Sept 2023)"}).fillna("")})
    return pd.concat([c, m], ignore_index=True)


def stage_roles() -> pd.DataFrame:
    p = pd.read_csv(X / "form990_pdf_people.csv", dtype=str)
    flags = p.role_flags.fillna("")
    a = pd.DataFrame({
        "name_display": p.name, "name_norm": p.name.map(lambda n: " ".join(str(n).lower().replace(".", " ").split())),
        "ein": CAL, "org_name": CAL_NAME, "tax_year": p.tax_year,
        "fiscal_year": (pd.to_numeric(p.tax_year) + 1).astype("Int64"), "title": p.title,
        "role_type": flags.map(lambda f: "officer" if "officer" in f else ("key_employee" if "key_employee" in f else
                               ("highest_compensated" if "highest" in f else "board"))),
        "is_officer": flags.str.contains("officer").astype(int),
        "is_director_trustee": flags.str.contains("trustee_or_director").astype(int),
        "is_key_employee": flags.str.contains("key_employee").astype(int),
        "is_highest_comp": flags.str.contains("highest").astype(int),
        "is_former": flags.str.contains("former").astype(int),
        "avg_hours_per_week": p.avg_hours, "reportable_comp_org": p.reportable_comp,
        "source_id": p.source_id, "object_id": "", "retrieved_date": today()})
    b = pd.read_csv(X / "board_lists.csv", dtype=str)
    bb = pd.DataFrame({
        "name_display": b.name, "name_norm": b.name.map(lambda n: " ".join(str(n).lower().replace(".", " ").split())),
        "ein": CAL, "org_name": CAL_NAME, "tax_year": "", "fiscal_year": b.report_year, "title": b.board_title,
        "role_type": "listed_in_report", "is_officer": b.role_type.fillna("").str.contains("officer").astype(int),
        "is_director_trustee": b.role_type.fillna("").str.contains("board").astype(int),
        "source_id": b.source_id, "retrieved_date": today(),
        "x_listed_affiliation": b.listed_affiliation, "x_list_role_type": b.role_type})
    return pd.concat([a, bb], ignore_index=True)


def main():
    out = {
        "stage_fact_org_financials__inputs.csv": stage_financials(),
        "stage_fact_gov_awards__inputs.csv": stage_sefa(),
        "stage_fact_grants__inputs.csv": stage_grants(),
        "stage_fact_roles__inputs.csv": stage_roles(),
    }
    for name, df in out.items():
        df.to_csv(INTERIM / name, index=False)
    for src, dst in (("annual_report_metrics.csv", "stage_supp_calvary_program_metrics.csv"),
                     ("strategic_plan_targets.csv", "stage_supp_calvary_strategic_targets.csv"),
                     ("individual_donor_band_counts.csv", "stage_supp_calvary_individual_donor_bands.csv")):
        pd.read_csv(X / src, dtype=str).assign(retrieved_date=today()).to_csv(INTERIM / dst, index=False)
    msg = "\n".join(f"- {k}: {len(v):,} rows" for k, v in out.items())
    log("60_stage_inputs", msg)
    print(msg)


if __name__ == "__main__":
    main()
