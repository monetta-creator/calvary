"""Phase 2 recon, area "federal": probe federal award, audit and opportunity sources.

Sections (run all, or pick with --only):
  usaspending   USAspending API v2: Calvary recipient profile, prime awards, subawards, transactions;
                assistance-listing titles; DC recipient counts per CFDA; DC prime + subaward probe
                pulls (target CFDAs, FY2019-FY2026); download/count sizing        -> raw/usaspending/
  usa_download  USAspending async downloads: /download/awards (Calvary) and /bulk_download/awards
                (HUD-awarded, DC recipients, FY2024) end to end                   -> raw/usaspending/
  fac           Federal Audit Clearinghouse API (needs FAC_API_KEY): Calvary general + all child
                endpoints; DC auditee universe per audit year; DC 2023 SEFA + pass-through sizing
                                                                                  -> raw/fac/
  grantsgov     Grants.gov search2 + fetchOpportunity: row cap, pagination, keyword hit counts,
                cfda/aln filter key, detail fields                                -> raw/grantsgov/
  sam           SAM.gov keyless checks: Assistance Listings CSV extract, internal search index,
                api.sam.gov without key                                           -> raw/sam/
  slfrf         Treasury SLFRF public data: subaward file (as of 2023-06-30) and latest
                project-level reporting workbook; Calvary + DC rows               -> raw/treasury_slfrf/

Usage:
  [ -f ~/.config/calvary/keys.env ] && set -a && . ~/.config/calvary/keys.env && set +a
  .venv/bin/python scripts/12_probe_federal.py [--only usaspending,fac,...] [--refresh]
Large files (SAM extract, SLFRF workbooks) are reused from raw/ unless --refresh.
Writes sources/catalog_parts/federal.csv. Keys are read from the environment only and never saved.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
import time
import zipfile
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import (RAW, SOURCES, RateLimiter, env_key, log, raw_path, register_source, rel,
                        save_raw, session, stamp, today)

CALVARY_EIN = "521307706"
CALVARY_UEI = "KMGRTKET2KJ1"          # found via /api/v2/recipient/ (see usaspending section)
CALVARY_NAME = "CALVARY WOMEN'S SERVICES"
FY_START, FY_END = "2018-10-01", "2026-09-30"   # federal FY2019-FY2026

USA = "https://api.usaspending.gov"
FAC = "https://api.fac.gov"
GG = "https://api.grants.gov/v1/api"
SAM_EXTRACT = ("https://sam.gov/api/prod/fileextractservices/v1/api/download/Assistance%20Listings/"
               "datagov/AssistanceListings_DataGov_PUBLIC_CURRENT.csv?privacy=Public")
SAM_SGS = "https://sam.gov/api/prod/sgs/v1/search/"
SLFRF_SUB = "https://home.treasury.gov/system/files/136/SLFRF-Subaward-USASpending-File.xlsx"
SLFRF_RPT = "https://home.treasury.gov/system/files/136/April-2026-Reporting-Data-through-March-31-2026.xlsx"
SLFRF_PAGE = ("https://home.treasury.gov/policy-issues/coronavirus/assistance-for-state-local-and-"
              "tribal-governments/state-and-local-fiscal-recovery-funds/public-data")

# Target assistance listings. origin: "brief" = listed in the recon brief; "sefa" = on Calvary's
# FY22/FY23 SEFA; "usa" = seen on Calvary records in USAspending; "added" = DC-relevant extra.
CFDAS = {
    "14.267": "brief", "14.231": "brief", "14.241": "brief", "14.218": "brief", "14.239": "brief",
    "16.575": "brief", "16.588": "brief", "16.736": "brief", "93.671": "brief", "93.959": "brief",
    "93.958": "brief", "93.243": "brief", "21.027": "brief;sefa", "21.019": "brief",
    "97.024": "brief;sefa", "64.033": "brief", "17.258": "brief", "17.259": "brief",
    "16.812": "brief", "14.235": "sefa", "10.561": "sefa", "14.251": "usa", "14.252": "usa",
    "59.073": "usa", "21.023": "added",
}
GRANTS = ["02", "03", "04", "05"]
DIRECT = ["06", "10"]
LOANS = ["07", "08"]
OTHER = ["09", "11", "-1"]
CONTRACTS = ["A", "B", "C", "D"]
IDVS = ["IDV_A", "IDV_B", "IDV_B_A", "IDV_B_B", "IDV_B_C", "IDV_C", "IDV_D", "IDV_E"]
DC_LOC = [{"country": "USA", "state": "DC"}]
TP = [{"start_date": FY_START, "end_date": FY_END}]
TP_ALL = [{"start_date": "2007-10-01", "end_date": FY_END}]
DCGOV_RE = re.compile(r"(DISTRICT OF COLUMBIA,? GOVERNMENT|GOVERNMENT OF (THE )?DISTRICT OF COLUMBIA|"
                      r"DISTRICT COLUMBIA GOVERNMENT|DISTRICT OF COLUMBIA GOVERNMENT|^DC OFFICE|"
                      r"^DC DEPARTMENT|^OFFICE OF VICTIM SERVICES AND JUSTICE GRANTS)", re.I)

KEYWORDS = ["homelessness", "housing", "domestic violence", "victim services", "women",
            "substance use", "workforce", "reentry", "veterans", "aging"]

S = session()
S1 = session(retries=0)        # single-shot, for limit tests that are expected to fail
RL = RateLimiter(2.0)          # USAspending, Grants.gov, SAM, Treasury: <= 2 req/s
RL_FAC = RateLimiter(1.0)      # FAC: 1,000 req/hour per api.data.gov key
REFRESH = False
R: dict = {}                   # probe results, logged and used for the catalog CSV
MANIFEST: dict[str, list] = {}


# ---------------------------------------------------------------- helpers
def note_req(source: str, desc: str, method: str, url: str, payload, status, path: Path | None):
    MANIFEST.setdefault(source, []).append({
        "desc": desc, "method": method, "url": url, "payload": payload, "status": status,
        "raw": rel(path) if path else None, "at": stamp()})


def post(source: str, desc: str, url: str, body: dict, timeout: int = 120, retry: bool = True):
    """POST JSON, save the response body untouched, return (status, parsed_json_or_None)."""
    RL.wait()
    try:
        r = (S if retry else S1).post(url, json=body, timeout=timeout)
    except Exception as e:  # noqa: BLE001
        note_req(source, desc, "POST", url, body, f"error: {e.__class__.__name__}", None)
        return None, None
    p = save_raw(source, desc, r.content, "json")
    note_req(source, desc, "POST", url, body, r.status_code, p)
    try:
        return r.status_code, r.json()
    except ValueError:
        return r.status_code, None


def get(source: str, desc: str, url: str, params: dict | None = None, headers: dict | None = None,
        limiter: RateLimiter = RL, ext: str = "json", timeout: int = 120):
    """GET, save the body untouched. Header values are never written (they may hold keys)."""
    limiter.wait()
    try:
        r = S.get(url, params=params, headers=headers or {}, timeout=timeout)
    except Exception as e:  # noqa: BLE001
        note_req(source, desc, "GET", url, params, f"error: {e.__class__.__name__}", None)
        return None, None, {}
    p = save_raw(source, desc, r.content, ext)
    note_req(source, desc, "GET", url, params, r.status_code, p)
    meta = {k.lower(): v for k, v in r.headers.items()
            if k.lower() in ("content-range", "x-ratelimit-limit", "x-ratelimit-remaining")}
    try:
        return r.status_code, (r.json() if ext == "json" else r.text), meta
    except ValueError:
        return r.status_code, None, meta


def existing_raw(source: str, desc: str, ext: str) -> Path | None:
    d = RAW / source
    hits = sorted(d.glob(f"*_{desc}.{ext}")) if d.exists() else []
    return hits[-1] if hits else None


def download(source: str, desc: str, url: str, ext: str) -> tuple[Path, bool]:
    old = existing_raw(source, desc, ext)
    if old and not REFRESH:
        note_req(source, desc, "GET", url, None, "reused", old)
        return old, False
    p = raw_path(source, desc, ext)
    RL.wait()
    with S.get(url, stream=True, timeout=600) as r:
        r.raise_for_status()
        with open(p, "wb") as f:
            for chunk in r.iter_content(1 << 20):
                f.write(chunk)
    note_req(source, desc, "GET", url, None, 200, p)
    return p, True


def flush_manifest():
    for source, rows in MANIFEST.items():
        if rows:
            save_raw(source, "requests_manifest", rows, "json")
    MANIFEST.clear()


def amt(x) -> str:
    return f"${x:,.0f}" if isinstance(x, (int, float)) else str(x)


def paged_awards(desc: str, filters: dict, fields: list[str], sort: str, subawards: bool = False,
                 max_pages: int = 50) -> list[dict]:
    rows, page = [], 1
    while page <= max_pages:
        sc, j = post("usaspending", f"{desc}_p{page}", f"{USA}/api/v2/search/spending_by_award/",
                     {"filters": filters, "fields": fields, "limit": 100, "page": page,
                      "sort": sort, "order": "desc", "subawards": subawards})
        if sc != 200 or not j:
            break
        rows += j.get("results", [])
        if not j.get("page_metadata", {}).get("hasNext"):
            break
        page += 1
    return rows


# ---------------------------------------------------------------- USAspending
AWARD_FIELDS = ["Award ID", "Recipient Name", "Recipient UEI", "recipient_id", "Award Amount",
                "Total Outlays", "Description", "Start Date", "End Date", "Awarding Agency",
                "Awarding Sub Agency", "Funding Agency", "Assistance Listings", "def_codes",
                "Last Modified Date", "Base Obligation Date", "generated_internal_id"]
LOAN_FIELDS = ["Award ID", "Recipient Name", "Recipient UEI", "recipient_id", "Loan Value",
               "Subsidy Cost", "Description", "Issued Date", "Awarding Agency",
               "Assistance Listings", "generated_internal_id"]
CONTRACT_FIELDS = ["Award ID", "Recipient Name", "Recipient UEI", "Award Amount", "Start Date",
                   "End Date", "Awarding Agency", "Description", "generated_internal_id"]
SUB_FIELDS = ["Sub-Award ID", "Sub-Awardee Name", "Sub-Recipient UEI", "Sub-Award Date",
              "Sub-Award Amount", "Awarding Agency", "Awarding Sub Agency", "Prime Award ID",
              "Prime Recipient Name", "prime_award_recipient_id", "Sub-Award Description",
              "Assistance Listing", "prime_award_generated_internal_id", "sub_award_recipient_id"]


def usaspending():
    out = R.setdefault("usaspending", {})
    # 1. recipient autocomplete + recipient list + profiles
    _, j = post("usaspending", "autocomplete_recipient_calvary", f"{USA}/api/v2/autocomplete/recipient/",
                {"search_text": "calvary women", "limit": 20})
    out["autocomplete"] = [(x.get("recipient_name"), x.get("uei")) for x in (j or {}).get("results", [])]
    _, j = post("usaspending", "recipient_list_calvary", f"{USA}/api/v2/recipient/",
                {"keyword": "calvary women", "award_type": "all", "limit": 50, "page": 1})
    recips = (j or {}).get("results", [])
    out["recipients"] = [{"id": x["id"], "uei": x["uei"], "duns": x["duns"], "name": x["name"],
                          "level": x["recipient_level"]} for x in recips]
    profiles = {}
    for x in recips:
        sc, pj, _ = get("usaspending", f"recipient_profile_{x['id']}", f"{USA}/api/v2/recipient/{x['id']}/",
                        {"year": "all"})
        if pj:
            profiles[x["id"]] = {"total_transaction_amount": pj.get("total_transaction_amount"),
                                 "total_transactions": pj.get("total_transactions"),
                                 "loan_face_value": pj.get("total_face_value_loan_amount"),
                                 "address": (pj.get("location") or {}).get("address_line1"),
                                 "congressional_code": (pj.get("location") or {}).get("congressional_code"),
                                 "business_types": pj.get("business_types")}
    out["profiles"] = profiles
    log("12_probe_federal: usaspending recipient",
        f"- autocomplete: {out['autocomplete']}\n- /recipient/ rows: {len(recips)}; "
        f"UEI {CALVARY_UEI} (DUNS 126543453) on P/C levels; R-level name-only record has no UEI\n"
        f"- profiles: {json.dumps(profiles, default=str)}")

    # 2. Calvary prime awards by group, by UEI and by name
    groups = {"grants": (GRANTS, AWARD_FIELDS, "Award Amount"),
              "direct_payments": (DIRECT, AWARD_FIELDS, "Award Amount"),
              "loans": (LOANS, LOAN_FIELDS, "Loan Value"),
              "other": (OTHER, AWARD_FIELDS, "Award Amount"),
              "contracts": (CONTRACTS, CONTRACT_FIELDS, "Award Amount"),
              "idvs": (IDVS, CONTRACT_FIELDS, "Award Amount")}
    prime = {}
    for term, tag in ((CALVARY_UEI, "uei"), (CALVARY_NAME, "name")):
        for g, (codes, fields, sort) in groups.items():
            rows = paged_awards(f"calvary_prime_{tag}_{g}",
                                {"recipient_search_text": [term], "award_type_codes": codes,
                                 "time_period": TP_ALL}, fields, sort)
            for r in rows:
                prime[r.get("generated_internal_id")] = {
                    "group": g, "award_id": r.get("Award ID"), "recipient": r.get("Recipient Name"),
                    "uei": r.get("Recipient UEI"),
                    "amount": r.get("Award Amount", r.get("Loan Value")),
                    "outlays": r.get("Total Outlays"),
                    "cfda": [a.get("cfda_number") for a in (r.get("Assistance Listings") or [])],
                    "agency": r.get("Awarding Agency"),
                    "start": r.get("Start Date", r.get("Issued Date")), "end": r.get("End Date")}
    out["calvary_prime_awards"] = list(prime.values())

    # 3. Calvary as subrecipient (FSRS subaward data)
    subs = {}
    for term, tag in (("CALVARY WOMEN", "name"), (CALVARY_UEI, "uei")):
        for codes, g in ((GRANTS + DIRECT, "grant"), (CONTRACTS, "procurement")):
            rows = paged_awards(f"calvary_sub_{tag}_{g}",
                                {"recipient_search_text": [term], "award_type_codes": codes,
                                 "time_period": TP_ALL}, SUB_FIELDS, "Sub-Award Amount", subawards=True)
            for r in rows:
                if "CALVARY WOMEN" in (r.get("Sub-Awardee Name") or "").upper():
                    subs[r.get("Sub-Award ID")] = {
                        "sub_id": r.get("Sub-Award ID"), "subawardee": r.get("Sub-Awardee Name"),
                        "amount": r.get("Sub-Award Amount"), "date": r.get("Sub-Award Date"),
                        "prime": r.get("Prime Recipient Name"), "prime_award": r.get("Prime Award ID"),
                        "cfda": (r.get("Assistance Listing") or {}).get("cfda_number")}
    out["calvary_subawards"] = list(subs.values())

    # 4. transactions (grants, loans)
    tx = []
    for codes, g in ((GRANTS, "grants"), (LOANS, "loans")):
        sc, j = post("usaspending", f"calvary_transactions_{g}", f"{USA}/api/v2/search/spending_by_transaction/",
                     {"filters": {"recipient_search_text": [CALVARY_NAME], "award_type_codes": codes,
                                  "time_period": TP_ALL},
                      "fields": ["Award ID", "Recipient Name", "Transaction Amount", "Action Date",
                                 "Award Type", "Assistance Listing", "Mod", "Transaction Description"],
                      "limit": 100, "page": 1, "sort": "Action Date", "order": "desc"})
        tx += [{"award_id": t.get("Award ID"), "amount": t.get("Transaction Amount"),
                "date": t.get("Action Date"), "type": t.get("Award Type")} for t in (j or {}).get("results", [])]
    out["calvary_transactions"] = tx
    log("12_probe_federal: usaspending Calvary awards",
        f"- prime awards (all types, FY2008+): {len(prime)} -> "
        + "; ".join(f"{a['group']} {a['award_id']} {a['cfda']} {amt(a['amount'])} {a['agency']}" for a in prime.values())
        + f"\n- Calvary subawards (FSRS): {len(subs)} -> "
        + "; ".join(f"{s['prime']} {s['cfda']} {amt(s['amount'])} {s['date']}" for s in subs.values())
        + f"\n- transactions: {len(tx)}")

    # 5. assistance listing titles + DC counts per CFDA (FY2019-FY2026)
    titles, per_cfda = {}, {}
    for c in CFDAS:
        _, j = post("usaspending", f"cfda_title_{c}", f"{USA}/api/v2/autocomplete/cfda/", {"search_text": c, "limit": 5})
        hit = [x for x in (j or {}).get("results", []) if x.get("program_number") == c]
        titles[c] = hit[0]["program_title"].strip() if hit else None
        f = {"program_numbers": [c], "recipient_locations": DC_LOC, "time_period": TP}
        _, pc = post("usaspending", f"dc_count_prime_{c}", f"{USA}/api/v2/search/spending_by_award_count/", {"filters": f})
        _, sc_ = post("usaspending", f"dc_count_sub_{c}", f"{USA}/api/v2/search/spending_by_award_count/",
                      {"filters": f, "subawards": True})
        pr, sr = (pc or {}).get("results", {}), (sc_ or {}).get("results", {})
        per_cfda[c] = {"grants": pr.get("grants"), "direct_payments": pr.get("direct_payments"),
                       "other": pr.get("other"), "loans": pr.get("loans"), "subgrants": sr.get("subgrants")}
    out["cfda_titles"], out["dc_counts_per_cfda"] = titles, per_cfda

    # 6. DC prime probe pull, target CFDAs (PPP 59.073 excluded: 32.8k DC loans), FY2019-FY2026
    cf = [c for c in CFDAS if c != "59.073"]
    dc_rows = []
    for codes, g in ((GRANTS, "grants"), (DIRECT, "direct_payments"), (OTHER, "other")):
        rows = paged_awards(f"dc_prime_{g}", {"program_numbers": cf, "recipient_locations": DC_LOC,
                                              "award_type_codes": codes, "time_period": TP}, AWARD_FIELDS, "Award Amount")
        for r in rows:
            r["_group"] = g
        dc_rows += rows
    dcgov = [r for r in dc_rows if DCGOV_RE.search(r.get("Recipient Name") or "")]
    _, gj = post("usaspending", "dc_count_prime_govtype", f"{USA}/api/v2/search/spending_by_award_count/",
                 {"filters": {"program_numbers": cf, "recipient_locations": DC_LOC,
                              "recipient_type_names": ["government"], "time_period": TP}})

    def cf_of(r):
        return ",".join(sorted({a.get("cfda_number") for a in (r.get("Assistance Listings") or []) if a.get("cfda_number")}))

    out["dc_prime_probe"] = {
        "rows": len(dc_rows), "by_group": dict(Counter(r["_group"] for r in dc_rows)),
        "dc_gov_rows_name_match": len(dcgov),
        "dc_gov_amount": round(sum((r.get("Award Amount") or 0) for r in dcgov)),
        "dc_gov_by_cfda": dict(Counter(cf_of(r) for r in dcgov).most_common()),
        "dc_gov_recipient_names": dict(Counter(r.get("Recipient Name") for r in dcgov).most_common()),
        "recipient_type_government_counts": (gj or {}).get("results"),
        "top_recipients": Counter(r.get("Recipient Name") for r in dc_rows).most_common(15),
        "calvary_rows": [r.get("Award ID") for r in dc_rows if "CALVARY WOMEN" in (r.get("Recipient Name") or "").upper()],
    }

    # 7. DC subaward probe pull (sub-recipient located in DC), target CFDAs
    sub_rows = paged_awards("dc_subawards", {"program_numbers": cf, "recipient_locations": DC_LOC,
                                             "award_type_codes": GRANTS + DIRECT, "time_period": TP},
                            SUB_FIELDS, "Sub-Award Amount", subawards=True)
    dcgov_sub = [r for r in sub_rows if DCGOV_RE.search(r.get("Prime Recipient Name") or "")]
    out["dc_sub_probe"] = {
        "rows": len(sub_rows), "dc_gov_prime_rows": len(dcgov_sub),
        "dc_gov_prime_amount": round(sum((r.get("Sub-Award Amount") or 0) for r in dcgov_sub)),
        "by_cfda": dict(Counter((r.get("Assistance Listing") or {}).get("cfda_number") for r in sub_rows).most_common()),
        "dc_gov_by_cfda": dict(Counter((r.get("Assistance Listing") or {}).get("cfda_number") for r in dcgov_sub).most_common()),
        "prime_names": Counter(r.get("Prime Recipient Name") for r in sub_rows).most_common(12),
        "by_year": dict(sorted(Counter((r.get("Sub-Award Date") or "")[:4] for r in sub_rows).items())),
        "calvary_rows": [r.get("Sub-Award ID") for r in sub_rows if "CALVARY WOMEN" in (r.get("Sub-Awardee Name") or "").upper()],
    }

    # 8. category rollups for the DC filter
    f = {"program_numbers": cf, "recipient_locations": DC_LOC, "award_type_codes": GRANTS + DIRECT, "time_period": TP}
    _, cj = post("usaspending", "dc_category_cfda", f"{USA}/api/v2/search/spending_by_category/cfda/",
                 {"filters": f, "limit": 50, "page": 1})
    out["dc_category_cfda"] = {x["code"]: round(x["amount"]) for x in (cj or {}).get("results", [])}

    # 9. download/count sizing for Phase 4
    sizing = {}
    sets = {
        "dc_target_cfdas_grants_direct": {"program_numbers": cf, "recipient_locations": DC_LOC,
                                          "award_type_codes": GRANTS + DIRECT, "time_period": TP},
        "dc_all_grants": {"recipient_locations": DC_LOC, "award_type_codes": GRANTS, "time_period": TP},
        "dc_nonprofit_grants": {"recipient_locations": DC_LOC, "recipient_type_names": ["nonprofit"],
                                "award_type_codes": GRANTS, "time_period": TP},
        "dc_pop_target_cfdas": {"program_numbers": cf, "place_of_performance_locations": DC_LOC,
                                "award_type_codes": GRANTS + DIRECT, "time_period": TP},
        "slfrf_21027_dc": {"program_numbers": ["21.027"], "recipient_locations": DC_LOC,
                           "award_type_codes": GRANTS + DIRECT, "time_period": TP},
    }
    for name, flt in sets.items():
        sizing[name] = {}
        for lvl in ("awards", "transactions", "subawards"):
            _, j = post("usaspending", f"download_count_{name}_{lvl}", f"{USA}/api/v2/download/count/",
                        {"filters": flt, "spending_level": lvl})
            sizing[name][lvl] = (j or {}).get("calculated_count")
    out["download_count"] = sizing
    log("12_probe_federal: usaspending DC probes",
        f"- CFDA titles (USAspending autocomplete): {json.dumps(titles)}\n"
        f"- DC counts per CFDA FY2019-FY2026 (recipient in DC): {json.dumps(per_cfda)}\n"
        f"- DC prime probe: {json.dumps({k: v for k, v in out['dc_prime_probe'].items() if k != 'top_recipients'}, default=str)}\n"
        f"- DC subaward probe: {json.dumps(out['dc_sub_probe'], default=str)}\n"
        f"- download/count sizing: {json.dumps(sizing)}")
    flush_manifest()


# ---------------------------------------------------------------- USAspending async downloads
def poll(file_name: str, desc: str, max_wait: int = 600) -> dict:
    t0 = time.time()
    last = {}
    while time.time() - t0 < max_wait:
        RL.wait()
        r = S.get(f"{USA}/api/v2/download/status/", params={"file_name": file_name}, timeout=60)
        last = r.json() if r.ok else {"status": f"http {r.status_code}"}
        if last.get("status") in ("finished", "failed"):
            break
        time.sleep(5)
    p = save_raw("usaspending", f"{desc}_status", last, "json")
    note_req("usaspending", f"{desc}_status", "GET", f"{USA}/api/v2/download/status/", {"file_name": file_name},
             last.get("status"), p)
    last["_seconds"] = round(time.time() - t0)
    return last


def zip_summary(p: Path) -> dict:
    """Data rows per CSV member (csv-parsed: descriptions contain embedded newlines)."""
    csv.field_size_limit(1 << 30)
    out = {}
    with zipfile.ZipFile(p) as z:
        for m in z.namelist():
            with z.open(m) as fh:
                out[m] = sum(1 for _ in csv.reader(io.TextIOWrapper(fh, encoding="utf-8", errors="replace"))) - 1
    return out


def usa_download():
    out = R.setdefault("usa_download", {})
    jobs = {
        "download_awards_calvary": (f"{USA}/api/v2/download/awards/", {
            "filters": {"recipient_search_text": [CALVARY_NAME],
                        "award_type_codes": GRANTS + DIRECT + LOANS + OTHER, "time_period": TP_ALL},
            "file_format": "csv"}),
        "bulk_download_hud_dc_fy2024": (f"{USA}/api/v2/bulk_download/awards/", {
            "filters": {"prime_award_types": GRANTS, "sub_award_types": ["grant"], "date_type": "action_date",
                        "date_range": {"start_date": "2023-10-01", "end_date": "2024-09-30"},
                        "agencies": [{"type": "awarding", "tier": "toptier",
                                      "name": "Department of Housing and Urban Development"}],
                        "recipient_locations": DC_LOC},
            "file_format": "csv"}),
    }
    for desc, (url, body) in jobs.items():
        sc, j = post("usaspending", f"{desc}_request", url, body)
        if sc != 200 or not j:
            out[desc] = {"status": f"request failed http {sc}"}
            continue
        st = poll(j["file_name"], desc)
        res = {"status": st.get("status"), "total_rows": st.get("total_rows"), "seconds": st["_seconds"]}
        if st.get("status") == "finished":
            p, _ = download("usaspending", desc, st.get("file_url") or j["file_url"], "zip")
            res["members"] = zip_summary(p)
            res["raw"] = rel(p)
        out[desc] = res
    log("12_probe_federal: usaspending downloads", "\n".join(f"- {k}: {json.dumps(v)}" for k, v in out.items()))
    flush_manifest()


# ---------------------------------------------------------------- FAC
FAC_CHILDREN = ["federal_awards", "passthrough", "findings", "findings_text", "notes_to_sefa",
                "secondary_auditors", "additional_eins", "additional_ueis", "corrective_action_plans"]


def fac():
    out = R.setdefault("fac", {})
    # docs pages (keyless), saved for provenance
    for slug in ("dictionary", "results-management", "getting-started"):
        get("fac", f"docs_{slug}", f"https://www.fac.gov/api/{slug}/", ext="html")
    key = env_key("FAC_API_KEY")
    if not key:
        out["status"] = "blocked_needs_key"
        log("12_probe_federal: fac", "- FAC_API_KEY not set; saved docs only. sample_status=blocked_needs_key")
        flush_manifest()
        return
    H = {"X-Api-Key": key}

    def fget(desc, ep, params):
        return get("fac", desc, f"{FAC}/{ep}", params, headers=H, limiter=RL_FAC)

    gens = {}
    for desc, params in (("general_calvary_ein", {"auditee_ein": f"eq.{CALVARY_EIN}"}),
                         ("general_calvary_uei", {"auditee_uei": f"eq.{CALVARY_UEI}"}),
                         ("general_calvary_name_dc", {"auditee_name": "ilike.*calvary*", "auditee_state": "eq.DC"})):
        sc, j, meta = fget(desc, "general", dict(params, order="audit_year.desc"))
        out.setdefault("http", {})[desc] = sc
        out["rate_limit"] = meta.get("x-ratelimit-limit")
        for g in (j or []) if isinstance(j, list) else []:
            if "calvary women" in (g.get("auditee_name") or "").lower():
                gens[g["report_id"]] = g
    _, j, _ = fget("additional_eins_calvary", "additional_eins", {"additional_ein": f"eq.{CALVARY_EIN}"})
    out["calvary_as_additional_ein"] = len(j or [])
    reports = []
    for rid, g in sorted(gens.items(), key=lambda kv: kv[1]["audit_year"]):
        rep = {"report_id": rid, "audit_year": g["audit_year"], "fy_end_date": g["fy_end_date"],
               "auditee_name": g["auditee_name"], "auditee_uei": g["auditee_uei"],
               "total_amount_expended": g["total_amount_expended"], "fac_accepted_date": g["fac_accepted_date"],
               "auditor_firm_name": g["auditor_firm_name"], "is_low_risk_auditee": g["is_low_risk_auditee"],
               "data_source": g.get("data_source"), "resubmission_status": g.get("resubmission_status"),
               "children": {}}
        for ep in FAC_CHILDREN:
            _, cj, _ = fget(f"{ep}_{rid}", ep, {"report_id": f"eq.{rid}"})
            rep["children"][ep] = len(cj or []) if isinstance(cj, list) else None
            if ep == "federal_awards" and isinstance(cj, list):
                rep["awards"] = [{"ref": a["award_reference"],
                                  "aln": f"{a['federal_agency_prefix']}.{a['federal_award_extension']}",
                                  "program": a["federal_program_name"], "amount": a["amount_expended"],
                                  "is_direct": a["is_direct"], "is_major": a["is_major"]} for a in cj]
            if ep == "passthrough" and isinstance(cj, list):
                rep["passthrough"] = {a["award_reference"]: a["passthrough_name"] for a in cj}
        reports.append(rep)
    out["calvary_reports"] = reports
    years = sorted(int(r["audit_year"]) for r in reports)
    out["calvary_years_present"] = years

    # DC universe per audit year (rows pulled, counted locally)
    dc = {}
    dc_ids = {}
    for yr in range(2016, int(today()[:4]) + 1):
        _, j, _ = fget(f"general_dc_{yr}", "general",
                       {"auditee_state": "eq.DC", "audit_year": f"eq.{yr}", "limit": 20000,
                        "select": "report_id,audit_year,auditee_ein,auditee_uei,auditee_name,entity_type,"
                                  "total_amount_expended,fy_end_date,fac_accepted_date"})
        rows = j if isinstance(j, list) else []
        dc[yr] = {"audits": len(rows), "nonprofit": sum(1 for r in rows if r.get("entity_type") == "non-profit"),
                  "expended": sum(int(r.get("total_amount_expended") or 0) for r in rows)}
        dc_ids[yr] = [r["report_id"] for r in rows]
    out["dc_by_year"] = dc

    # DC 2023 SEFA + pass-through rows, batched by report_id
    ids = dc_ids.get(2023, [])
    fa_rows, pt_rows = [], []
    for i in range(0, len(ids), 100):
        chunk = f"in.({','.join(ids[i:i + 100])})"
        _, j, _ = fget(f"federal_awards_dc2023_b{i // 100:02d}", "federal_awards",
                       {"report_id": chunk, "limit": 20000,
                        "select": "report_id,award_reference,federal_agency_prefix,federal_award_extension,"
                                  "federal_program_name,amount_expended,is_direct,is_passthrough_award,passthrough_amount"})
        fa_rows += j if isinstance(j, list) else []
        _, j, _ = fget(f"passthrough_dc2023_b{i // 100:02d}", "passthrough", {"report_id": chunk, "limit": 20000})
        pt_rows += j if isinstance(j, list) else []
    target = set(CFDAS)
    fa_t = [r for r in fa_rows if f"{r['federal_agency_prefix']}.{r['federal_award_extension']}" in target]
    out["dc_2023_sefa"] = {
        "federal_awards_rows": len(fa_rows), "indirect_rows": sum(1 for r in fa_rows if r["is_direct"] == "N"),
        "target_cfda_rows": len(fa_t), "target_cfda_indirect_rows": sum(1 for r in fa_t if r["is_direct"] == "N"),
        "target_cfda_auditees": len({r["report_id"] for r in fa_t}),
        "passthrough_rows": len(pt_rows),
        "top_passthrough_names": Counter((r.get("passthrough_name") or "").strip().upper() for r in pt_rows).most_common(12),
    }
    # OVSJG as pass-through, any auditee state, all years
    _, j, _ = fget("passthrough_ovsjg_all", "passthrough",
                   {"passthrough_name": "ilike.*victim services and justice*", "limit": 20000})
    pj = j if isinstance(j, list) else []
    out["ovsjg_passthrough"] = {"rows": len(pj), "by_year": dict(sorted(Counter(r["audit_year"] for r in pj).items())),
                                "reports": len({r["report_id"] for r in pj})}
    # national pass-through sweep sizing: exact counts come back in Content-Range
    counts = {}
    for tag, pat in (("district_of_columbia", "*district of columbia*"), ("dc_department", "*DC Department*"),
                     ("community_partnership", "*community partnership*")):
        _, _, meta = get("fac", f"passthrough_count_{tag}", f"{FAC}/passthrough",
                         {"passthrough_name": f"ilike.{pat}", "select": "report_id", "limit": 1},
                         headers=dict(H, Prefer="count=exact"), limiter=RL_FAC)
        cr = meta.get("content-range", "")
        counts[pat] = int(cr.split("/")[1]) if "/" in cr and cr.split("/")[1].isdigit() else None
    out["passthrough_name_counts_all_states"] = counts
    out["status"] = "ok"
    log("12_probe_federal: fac",
        f"- Calvary reports: {len(reports)} (audit years {years}); additional_eins hits {out['calvary_as_additional_ein']}\n"
        + "\n".join(f"  - {r['report_id']} FYE {r['fy_end_date']} total {amt(r['total_amount_expended'])}; "
                    f"awards {[(a['aln'], a['amount'], a['is_direct']) for a in r.get('awards', [])]}; "
                    f"passthrough {r.get('passthrough')}; children {r['children']}" for r in reports)
        + f"\n- DC auditees by audit_year: {json.dumps(dc)}\n- DC 2023 SEFA: {json.dumps(out['dc_2023_sefa'], default=str)}"
        + f"\n- OVSJG pass-through rows: {json.dumps(out['ovsjg_passthrough'])}"
        + f"\n- passthrough_name counts, all auditee states: {json.dumps(counts)}")
    flush_manifest()


# ---------------------------------------------------------------- Grants.gov
def grantsgov():
    out = R.setdefault("grantsgov", {})
    get("grantsgov", "docs_search2", "https://www.grants.gov/api/common/search2", ext="html")
    get("grantsgov", "docs_fetchopportunity", "https://www.grants.gov/api/common/fetchopportunity", ext="html")
    s2 = f"{GG}/search2"
    # full open + forecast universe in one call
    _, j = post("grantsgov", "search2_posted_forecasted_all", s2, {"rows": 5000, "oppStatuses": "forecasted|posted"})
    d = (j or {}).get("data", {})
    hits = d.get("oppHits", [])
    out["open_forecast_total"] = d.get("hitCount")
    out["open_forecast_returned"] = len(hits)
    out["status_counts"] = {o["label"]: o["count"] for o in d.get("oppStatusOptions", [])}
    target = set(CFDAS)
    out["open_forecast_target_cfda"] = sum(1 for h in hits if target & set(h.get("cfdaList") or []))
    # row-cap test
    cap = {}
    for rows in (10000, 30000):
        sc, j = post("grantsgov", f"search2_rowcap_{rows}", s2, {"rows": rows, "oppStatuses": "closed|archived"},
                     timeout=300, retry=False)
        cap[rows] = {"http": sc, "returned": len(((j or {}).get("data") or {}).get("oppHits", []))}
    out["row_cap"] = cap
    # pagination
    tot = out["open_forecast_total"] or 0
    _, j = post("grantsgov", "search2_pagination", s2,
                {"rows": 10, "startRecordNum": max(tot - 5, 0), "oppStatuses": "forecasted|posted"})
    pd = (j or {}).get("data", {})
    out["pagination"] = {"startRecord": pd.get("startRecord"), "returned": len(pd.get("oppHits", []))}
    # filter key test: documented "aln" vs live "cfda"
    keytest = {}
    for k in ("aln", "cfda"):
        _, j = post("grantsgov", f"search2_key_{k}_16.575", s2, {"rows": 1, k: "16.575",
                                                                 "oppStatuses": "forecasted|posted|closed|archived"})
        keytest[k] = ((j or {}).get("data") or {}).get("hitCount")
    out["filter_key_test"] = keytest
    # keyword hit counts
    kw = {}
    for k in KEYWORDS:
        safe = k.replace(" ", "_")
        row = {}
        _, j = post("grantsgov", f"search2_kw_{safe}", s2, {"rows": 1, "keyword": k, "oppStatuses": "forecasted|posted"})
        dd = (j or {}).get("data", {})
        sc_ = {o["label"]: o["count"] for o in dd.get("oppStatusOptions", [])}
        row.update(hits=dd.get("hitCount"), posted=sc_.get("posted"), forecasted=sc_.get("forecasted"))
        _, j = post("grantsgov", f"search2_kw_{safe}_elig12", s2,
                    {"rows": 1, "keyword": k, "oppStatuses": "forecasted|posted", "eligibilities": "12"})
        row["elig_501c3"] = ((j or {}).get("data") or {}).get("hitCount")
        if " " in k:
            _, j = post("grantsgov", f"search2_kw_{safe}_phrase", s2,
                        {"rows": 1, "keyword": f'"{k}"', "oppStatuses": "forecasted|posted"})
            row["phrase_hits"] = ((j or {}).get("data") or {}).get("hitCount")
        kw[k] = row
    out["keywords"] = kw
    # fetchOpportunity: one posted synopsis and one forecast, preferring target CFDAs
    picks = {}
    for st in ("posted", "forecasted"):
        cand = [h for h in hits if h.get("oppStatus") == st and target & set(h.get("cfdaList") or [])] or \
               [h for h in hits if h.get("oppStatus") == st]
        if cand:
            picks[st] = cand[0]["id"]
    det = {}
    for st, oid in picks.items():
        _, j = post("grantsgov", f"fetchOpportunity_{oid}", f"{GG}/fetchOpportunity", {"opportunityId": int(oid)})
        dd = (j or {}).get("data", {})
        blk = dd.get("synopsis") or dd.get("forecast") or {}
        det[st] = {"id": oid, "number": dd.get("opportunityNumber"), "docType": dd.get("docType"),
                   "top_keys": sorted(dd.keys()), "detail_block": "synopsis" if dd.get("synopsis") else "forecast",
                   "awardCeiling": blk.get("awardCeiling"), "awardFloor": blk.get("awardFloor"),
                   "estimatedFunding": blk.get("estimatedFunding"), "responseDate": blk.get("responseDate"),
                   "estimatedSynopsisCloseDate": blk.get("estimatedSynopsisCloseDate"),
                   "applicantTypes": [a.get("id") for a in blk.get("applicantTypes") or []],
                   "cfdas": [c.get("cfdaNumber") for c in dd.get("cfdas") or []]}
    out["fetch"] = det
    log("12_probe_federal: grantsgov",
        f"- posted+forecasted total {out['open_forecast_total']} (returned {out['open_forecast_returned']} in one call); "
        f"target-CFDA hits {out['open_forecast_target_cfda']}; status facets {out['status_counts']}\n"
        f"- row cap: {cap}; pagination: {out['pagination']}; filter key test (16.575 all statuses): {keytest}\n"
        f"- keywords (posted+forecasted): {json.dumps(kw)}\n- fetchOpportunity: {json.dumps(det, default=str)}")
    flush_manifest()


# ---------------------------------------------------------------- SAM.gov (keyless only)
def sam():
    out = R.setdefault("sam", {})
    p, _ = download("sam", "AssistanceListings_DataGov_PUBLIC_CURRENT", SAM_EXTRACT, "csv")
    csv.field_size_limit(1 << 30)
    with open(p, encoding="utf-8", errors="replace", newline="") as fh:
        rows = list(csv.DictReader(fh))
    by = {r["Program Number"]: r for r in rows}
    out["extract_rows"] = len(rows)
    out["extract_columns"] = len(rows[0]) if rows else 0
    out["titles"] = {c: (by[c]["Program Title"].strip() if c in by else None) for c in CFDAS}
    out["not_in_active_extract"] = [c for c in CFDAS if c not in by]
    sc, j, _ = get("sam", "sgs_cfda_14.267", SAM_SGS, {"index": "cfda", "q": "14.267", "page": 0, "size": 1})
    out["sgs_cfda_http"] = sc
    out["sgs_cfda_hits"] = ((j or {}).get("page") or {}).get("totalElements")
    sc, j, _ = get("sam", "sgs_ei_calvary", SAM_SGS, {"index": "ei", "q": "calvary women's services", "page": 0, "size": 10})
    res = ((j or {}).get("_embedded") or {}).get("results", [])
    out["sgs_ei_types"] = dict(Counter(x.get("_type") for x in res))
    out["sgs_ei_calvary_uei_found"] = any(x.get("ueiSam") == CALVARY_UEI for x in res)
    keyless = {}
    for name, url in (("entity_v3", "https://api.sam.gov/entity-information/v3/entities?ueiSAM=" + CALVARY_UEI),
                      ("assistance_listings_v1", "https://api.sam.gov/assistance-listings/v1/search?keyword=continuum")):
        RL.wait()
        r = S.get(url, timeout=60)
        keyless[name] = r.status_code
        note_req("sam", f"nokey_{name}", "GET", url, None, r.status_code, None)
    out["api_sam_without_key"] = keyless
    log("12_probe_federal: sam",
        f"- Assistance Listings extract: {out['extract_rows']} active listings, {out['extract_columns']} columns ({rel(p)})\n"
        f"- target CFDAs missing from active extract: {out['not_in_active_extract']}\n"
        f"- sgs cfda search http {out['sgs_cfda_http']} hits {out['sgs_cfda_hits']}; sgs ei result types {out['sgs_ei_types']} "
        f"(Calvary UEI found: {out['sgs_ei_calvary_uei_found']})\n- api.sam.gov without key: {keyless}")
    flush_manifest()


# ---------------------------------------------------------------- Treasury SLFRF
def slfrf():
    import openpyxl  # noqa: PLC0415  (present in venv; not in requirements.txt)
    out = R.setdefault("slfrf", {})
    get("treasury_slfrf", "public_data_page", SLFRF_PAGE, ext="html")
    p, _ = download("treasury_slfrf", "SLFRF-Subaward-USASpending-File", SLFRF_SUB, "xlsx")
    wb = openpyxl.load_workbook(p, read_only=True)
    sheet = next(n for n in wb.sheetnames if n.startswith("SLFRF Subawards"))
    it = wb[sheet].iter_rows(values_only=True)
    hdr = next(it)
    ix = {h: i for i, h in enumerate(hdr)}
    n, dc, cal = 0, [], []
    for r in it:
        n += 1
        if r[ix["prime_awardee_state_code"]] == "DC":
            dc.append(r)
            if "CALVARY" in str(r[ix["subawardee_name"]]).upper():
                cal.append({"subawardee": r[ix["subawardee_name"]], "amount": r[ix["subaward_amount"]],
                            "date": str(r[ix["subaward_action_date"]]), "prime": r[ix["prime_awardee_name"]],
                            "sub_number": r[ix["subaward_number"]], "description": str(r[ix["subaward_description"]])[:200]})
    out["subaward_file"] = {"sheet": sheet, "rows": n, "dc_prime_rows": len(dc),
                            "dc_prime_amount": round(sum(float(r[ix["subaward_amount"]] or 0) for r in dc)),
                            "calvary": cal, "raw": rel(p)}
    wb.close()
    p2, _ = download("treasury_slfrf", "April-2026-Reporting-Data-through-March-31-2026", SLFRF_RPT, "xlsx")
    wb = openpyxl.load_workbook(p2, read_only=True)
    proj = next(n for n in wb.sheetnames if n.startswith("Projects"))
    it = wb[proj].iter_rows(values_only=True)
    next(it)
    hdr = next(it)
    ix = {h: i for i, h in enumerate(hdr)}
    dcp = [r for r in it if r[ix["State/Territory"]] == "District of Columbia"]
    kw = ("homeless", "victim", "women", "domestic", "shelter", "unhoused")
    out["projects_file"] = {"sheets": wb.sheetnames, "dc_projects": len(dcp),
                            "dc_projects_sector_keyword": sum(1 for r in dcp if any(
                                k in f"{r[ix['Project Name']]} {r[ix['Project Description']]}".lower() for k in kw)),
                            "has_subrecipient_columns": any("ubrecipient" in str(h) for h in hdr), "raw": rel(p2)}
    wb.close()
    log("12_probe_federal: slfrf",
        f"- subaward file: {json.dumps({k: v for k, v in out['subaward_file'].items() if k != 'calvary'})}\n"
        f"- Calvary rows: {json.dumps(cal, default=str)}\n- projects file: {json.dumps(out['projects_file'])}")
    flush_manifest()


# ---------------------------------------------------------------- catalog part + registry
CAT_FIELDS = ["name", "area", "base_url", "auth_required", "auth_env_var", "rate_limit", "key_endpoints",
              "fields_of_interest", "years_covered", "coverage_gaps", "sample_request", "sample_status",
              "probe_date", "feeds_tables", "source_id", "notes"]


def status_of(section: str, ok_test) -> str:
    if section not in R:
        return "not_run"
    try:
        return ok_test(R[section])
    except Exception:  # noqa: BLE001
        return "failed"


def write_catalog():
    path = SOURCES / "catalog_parts" / "federal.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    prev = {}
    if path.exists():
        with open(path, newline="", encoding="utf-8") as f:
            prev = {r["source_id"]: r for r in csv.DictReader(f)}
    usa = R.get("usaspending", {})
    fac_ = R.get("fac", {})
    rows = [
        dict(name="USAspending.gov API v2 (search, recipient, references)", base_url=USA,
             auth_required="no", auth_env_var="", rate_limit="none published; probed at 2 req/s",
             key_endpoints="POST /api/v2/recipient/; GET /api/v2/recipient/{id}/; POST /api/v2/search/spending_by_award/ "
                           "(subawards=true for FSRS subawards); POST /api/v2/search/spending_by_award_count/; "
                           "POST /api/v2/search/spending_by_transaction/; POST /api/v2/search/spending_by_category/{cfda|recipient}/; "
                           "POST /api/v2/autocomplete/cfda/; POST /api/v2/download/count/",
             fields_of_interest="Award ID; generated_internal_id; Recipient Name; Recipient UEI; recipient_id; Award Amount; "
                                "Total Outlays; Assistance Listings; Awarding Agency/Sub Agency; Start/End Date; def_codes; "
                                "Sub-Award ID/Amount/Date; Sub-Awardee Name; Sub-Recipient UEI; Prime Recipient Name; Prime Award ID",
             years_covered="search endpoints FY2008+ (2007-10-01 floor); downloads FY2001+",
             coverage_gaps="Subawards only where primes report to FSRS: SLFRF 21.027 subawards absent for DC; "
                           "CoC 14.267 has 2 DC subaward rows. Award-level location filters use the current award "
                           "recipient location (EFSP National Board now VA). Name-only (R-level) recipients lack UEI.",
             sample_request='curl -s -X POST https://api.usaspending.gov/api/v2/search/spending_by_award/ -H "Content-Type: application/json" '
                            '-d \'{"filters":{"recipient_search_text":["KMGRTKET2KJ1"],"award_type_codes":["02","03","04","05"],'
                            '"time_period":[{"start_date":"2007-10-01","end_date":"2026-09-30"}]},"fields":["Award ID","Recipient Name",'
                            '"Award Amount","Assistance Listings"],"limit":100,"page":1,"sort":"Award Amount","order":"desc"}\'',
             sample_status=status_of("usaspending", lambda u: "ok" if u.get("calvary_prime_awards") else "ok_no_results"),
             feeds_tables="dim_org;dim_funder;dim_program_area;fact_gov_awards;fact_org_relationships",
             source_id="api_usaspending",
             notes=f"Calvary UEI {CALVARY_UEI}, DUNS 126543453; prime awards {len(usa.get('calvary_prime_awards', []))}, "
                   f"FSRS subawards {len(usa.get('calvary_subawards', []))}; DC target-CFDA probe "
                   f"{usa.get('dc_prime_probe', {}).get('rows')} prime / {usa.get('dc_sub_probe', {}).get('rows')} sub rows."),
        dict(name="USAspending.gov award downloads (download/awards, bulk_download/awards)",
             base_url=f"{USA}/api/v2/download/awards/", auth_required="no", auth_env_var="",
             rate_limit="async jobs; download/awards max 500,000 rows per file",
             key_endpoints="POST /api/v2/download/awards/ (advanced-search filters incl. program_numbers, recipient_locations); "
                           "POST /api/v2/bulk_download/awards/ (agencies required; no program_numbers filter; prime transactions); "
                           "GET /api/v2/download/status/?file_name=",
             fields_of_interest="assistance_award_unique_key; award_id_fain; cfda_number; recipient_uei; recipient_name; "
                                "total_obligated_amount; total_outlayed_amount; period_of_performance_*; subaward_* columns",
             years_covered="FY2001+", coverage_gaps="Same FSRS gaps as the search API.",
             sample_request='curl -s -X POST https://api.usaspending.gov/api/v2/download/awards/ -H "Content-Type: application/json" '
                            '-d \'{"filters":{"program_numbers":["14.267","16.575"],"recipient_locations":[{"country":"USA","state":"DC"}],'
                            '"award_type_codes":["02","03","04","05","06","10"],"time_period":[{"start_date":"2018-10-01","end_date":"2026-09-30"}]},'
                            '"file_format":"csv"}\'',
             sample_status=status_of("usa_download", lambda d: "ok" if all(v.get("status") == "finished" for v in d.values()) else "failed"),
             feeds_tables="fact_gov_awards;fact_org_relationships", source_id="bulk_usaspending",
             notes="; ".join(f"{k}: {v.get('status')} {v.get('total_rows')} rows in {v.get('seconds')}s"
                             for k, v in R.get("usa_download", {}).items())),
        dict(name="Federal Audit Clearinghouse API", base_url=FAC, auth_required="yes (api.data.gov key)",
             auth_env_var="FAC_API_KEY", rate_limit=f"{fac_.get('rate_limit') or '1000'} requests/hour per key; 20,000 rows per request",
             key_endpoints="GET /general; /federal_awards; /passthrough; /findings; /findings_text; /notes_to_sefa; "
                           "/secondary_auditors; /additional_eins; /additional_ueis; /corrective_action_plans (PostgREST filters)",
             fields_of_interest="report_id; auditee_ein; auditee_uei; audit_year; fy_end_date; total_amount_expended; "
                                "federal_agency_prefix; federal_award_extension; federal_program_name; amount_expended; is_direct; "
                                "is_major; passthrough_name; passthrough_id; award_reference",
             years_covered="audit years 2016+ (Census-migrated through 2022, GSA intake 2023+)",
             coverage_gaps="Only auditees over the single-audit threshold ($750k; $1M for FY beginning on/after 2024-10-01). "
                           "Calvary present for audit years 2022 and 2023 only. passthrough_id often blank or 'GSA_MIGRATION'.",
             sample_request='curl -s -H "X-Api-Key: $FAC_API_KEY" "https://api.fac.gov/federal_awards?report_id=eq.2023-09-GSAFAC-0000037691"',
             sample_status=status_of("fac", lambda f: f.get("status") if f.get("status") != "ok" else
                                     ("ok" if f.get("calvary_reports") else "ok_no_results")),
             feeds_tables="dim_org;dim_funder;dim_program_area;fact_gov_awards;fact_org_relationships",
             source_id="api_fac",
             notes=f"Calvary audit years {fac_.get('calvary_years_present')}; DC auditees/year "
                   f"{ {k: v['audits'] for k, v in (fac_.get('dc_by_year') or {}).items()} }."),
        dict(name="Grants.gov REST API (search2, fetchOpportunity)", base_url=GG, auth_required="no", auth_env_var="",
             rate_limit="none published; probed at 2 req/s; rows=10000 OK, rows=30000 fails (HTTP 502 / dropped connection)",
             key_endpoints="POST /v1/api/search2 (keyword, cfda, oppStatuses, agencies, eligibilities, fundingCategories, "
                           "fundingInstruments, rows, startRecordNum); POST /v1/api/fetchOpportunity (opportunityId)",
             fields_of_interest="id; number; title; agencyCode; openDate; closeDate; oppStatus; docType; cfdaList; "
                                "synopsis.awardCeiling/awardFloor/estimatedFunding/responseDate/applicantTypes; forecast.*; cfdas",
             years_covered="current posted/forecasted plus closed and archived history",
             coverage_gaps="Federal discretionary opportunities only; formula/pass-through funds Calvary receives via DC are not listed. "
                           "Filter key is 'cfda' in production (docs say 'aln', which is ignored).",
             sample_request='curl -s -X POST https://api.grants.gov/v1/api/search2 -H "Content-Type: application/json" '
                            '-d \'{"rows":5000,"oppStatuses":"forecasted|posted","eligibilities":"12"}\'',
             sample_status=status_of("grantsgov", lambda g: "ok" if g.get("open_forecast_total") else "failed"),
             feeds_tables="fact_opportunities;dim_funder;dim_program_area", source_id="api_grantsgov",
             notes=f"posted+forecasted total {R.get('grantsgov', {}).get('open_forecast_total')}; "
                   f"target-CFDA {R.get('grantsgov', {}).get('open_forecast_target_cfda')}"),
        dict(name="SAM.gov Assistance Listings data extract (CSV)", base_url=SAM_EXTRACT, auth_required="no", auth_env_var="",
             rate_limit="single file", key_endpoints="GET extract URL (303 redirect to signed S3 URL); "
                                                     "GET https://sam.gov/api/prod/sgs/v1/search/?index=cfda&q= (undocumented)",
             fields_of_interest="Program Number; Program Title; Popular Name; Federal Agency; Types of Assistance; "
                                "Applicant Eligibility; Obligations; Website Address",
             years_covered="current active listings only", coverage_gaps="Archived listings (21.019, 14.235) are absent; "
                                                                      "use USAspending autocomplete for their titles.",
             sample_request=f"curl -sL -o AssistanceListings.csv '{SAM_EXTRACT}'",
             sample_status=status_of("sam", lambda s: "ok" if s.get("extract_rows") else "failed"),
             feeds_tables="dim_program_area;dim_funder", source_id="bulk_sam_assistance_listings",
             notes=f"{R.get('sam', {}).get('extract_rows')} active listings."),
        dict(name="SAM.gov Entity Management API", base_url="https://api.sam.gov/entity-information/v3/entities",
             auth_required="yes (SAM.gov account API key)", auth_env_var="SAM_API_KEY (not set)",
             rate_limit="per SAM.gov public docs (not verified here): 10/day without a SAM role, 1,000/day with one",
             key_endpoints="GET /entity-information/v3/entities?ueiSAM=&api_key=",
             fields_of_interest="ueiSAM; legalBusinessName; registrationStatus; registrationExpirationDate; physicalAddress; entityStructure",
             years_covered="current registrations", coverage_gaps="Keyless sam.gov search index (index=ei) returns exclusions only.",
             sample_request="curl -s 'https://api.sam.gov/entity-information/v3/entities?ueiSAM=KMGRTKET2KJ1&api_key=$SAM_API_KEY'",
             sample_status="blocked_needs_key", feeds_tables="dim_org", source_id="api_sam_entity",
             notes=f"Without key: {R.get('sam', {}).get('api_sam_without_key')}. UEI already available from USAspending and FAC."),
        dict(name="Treasury SLFRF public data (subaward file; quarterly reporting data)", base_url=SLFRF_PAGE,
             auth_required="no", auth_env_var="", rate_limit="static files (~60 MB each)",
             key_endpoints="GET /system/files/136/SLFRF-Subaward-USASpending-File.xlsx; "
                           "GET /system/files/136/April-2026-Reporting-Data-through-March-31-2026.xlsx",
             fields_of_interest="prime_awardee_name; subawardee_name; subawardee_uei; subaward_amount; subaward_action_date; "
                                "subaward_description; Project ID; Project Name; Expenditure Category; Total Cumulative Obligations/Expenditures",
             years_covered="subawards reported through 2023-06-30; projects through 2026-03-31",
             coverage_gaps="Subaward detail stops at 2023-06-30; project workbook has no subrecipient names.",
             sample_request=f"curl -sL -o slfrf_subawards.xlsx {SLFRF_SUB}",
             sample_status=status_of("slfrf", lambda s: "ok" if s.get("subaward_file", {}).get("calvary") else "ok_no_results"),
             feeds_tables="fact_gov_awards;fact_org_relationships", source_id="bulk_treasury_slfrf",
             notes=f"Calvary SLFRF subawards from DC: "
                   f"{[(c['amount'], c['date'][:10]) for c in R.get('slfrf', {}).get('subaward_file', {}).get('calvary', [])]}"),
    ]
    section_of = {"api_usaspending": "usaspending", "bulk_usaspending": "usa_download", "api_fac": "fac",
                  "api_grantsgov": "grantsgov", "bulk_sam_assistance_listings": "sam", "api_sam_entity": "sam",
                  "bulk_treasury_slfrf": "slfrf"}
    for r in rows:
        r["area"] = "federal"
        r["probe_date"] = today()
        if section_of[r["source_id"]] not in R and r["source_id"] in prev:   # not run now: keep last result
            r.update({k: prev[r["source_id"]][k] for k in ("sample_status", "probe_date", "notes")})
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAT_FIELDS)
        w.writeheader()
        w.writerows(rows)
    return path


def register():
    register_source("api_usaspending", "USAspending.gov API v2", USA, "U.S. Department of the Treasury, Bureau of the Fiscal Service",
                    "Public domain (U.S. government data); cite USAspending.gov",
                    "Keyless JSON. Search, recipient, autocomplete and download/count endpoints.")
    register_source("bulk_usaspending", "USAspending.gov award downloads (download/awards, bulk_download/awards)",
                    f"{USA}/api/v2/download/awards/", "U.S. Department of the Treasury, Bureau of the Fiscal Service",
                    "Public domain (U.S. government data); cite USAspending.gov",
                    "Async zip of CSVs; poll /api/v2/download/status/. 500k-row limit for download/awards.")
    register_source("api_fac", "Federal Audit Clearinghouse API", FAC, "U.S. General Services Administration (GSA)",
                    "Public domain (U.S. government data); see https://www.fac.gov/api/terms/",
                    "PostgREST over FAC dissemination tables; X-Api-Key header with an api.data.gov key (FAC_API_KEY).")
    register_source("api_grantsgov", "Grants.gov REST API (search2, fetchOpportunity)", GG,
                    "U.S. Department of Health and Human Services (Grants.gov PMO)",
                    "Public domain (U.S. government data)", "Keyless POST JSON.")
    register_source("bulk_sam_assistance_listings", "SAM.gov Assistance Listings data extract (CSV)", SAM_EXTRACT,
                    "U.S. General Services Administration (SAM.gov)", "Public domain (U.S. government data)",
                    "Keyless; active listings only.")
    register_source("api_sam_sgs", "SAM.gov site search index (undocumented)", SAM_SGS,
                    "U.S. General Services Administration (SAM.gov)", "Public domain (U.S. government data)",
                    "Keyless backend of sam.gov search; index=cfda returns listing metadata, index=ei returns exclusions only.")
    register_source("bulk_treasury_slfrf", "Treasury SLFRF public data files", SLFRF_PAGE, "U.S. Department of the Treasury",
                    "Public domain (U.S. government data)",
                    "SLFRF-Subaward-USASpending-File.xlsx (subawards as of 2023-06-30); quarterly Reporting Data workbooks (project level).")


# ---------------------------------------------------------------- main
SECTIONS = {"usaspending": usaspending, "usa_download": usa_download, "fac": fac,
            "grantsgov": grantsgov, "sam": sam, "slfrf": slfrf}


def main():
    global REFRESH
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="", help="comma list of sections: " + ",".join(SECTIONS))
    ap.add_argument("--refresh", action="store_true")
    a = ap.parse_args()
    REFRESH = a.refresh
    todo = [s for s in a.only.split(",") if s] or list(SECTIONS)
    register()
    for s in todo:
        t0 = time.time()
        try:
            SECTIONS[s]()
        except Exception as e:  # noqa: BLE001
            R.setdefault(s, {})["error"] = f"{e.__class__.__name__}: {e}"
            log(f"12_probe_federal: {s} FAILED", f"- {e.__class__.__name__}: {e}")
            flush_manifest()
        print(f"[{s}] done in {time.time() - t0:.0f}s", file=sys.stderr)
    p = write_catalog()
    log("12_probe_federal: catalog", f"- wrote {rel(p)}; sections run: {todo}")
    print(json.dumps(R, indent=1, default=str))


if __name__ == "__main__":
    main()
