"""Phase 4 pull: Grants.gov posted + forecasted opportunities -> interim/stage_fact_opportunities__grantsgov.csv.

Steps (all responses saved untouched to raw/grantsgov/):
  1. POST /v1/api/search2 {"oppStatuses":"forecasted|posted"} - the whole open+forecast universe
     (paged with startRecordNum if hitCount exceeds the page size).
  2. POST search2 per target assistance listing with the `cfda` key (the documented `aln` key is ignored
     in production) - cross-check of the local cfdaList filter.
  3. POST search2 per keyword (multi-word keywords quoted as exact phrases) - the server-side full-text match.
  4. Candidates = local cfdaList hit on a target ALN OR cfda-key hit OR keyword search hit OR local
     keyword regex hit on the title.
  5. POST /v1/api/fetchOpportunity for every candidate (reuses a saved raw response for the same id
     unless --refresh).
  6. Local filter (the kept set): target-ALN match on the detail record OR a local keyword regex hit in
     title + description + ALN titles + eligibility text. The server keyword search is fuzzy (stemming,
     non-text fields), so a server hit alone does not keep an opportunity; it is recorded in
     x_keyword_hits_search.
  7. Stage one row per kept opportunity: amounts, dates, eligibility codes, ALNs, program_area_tags
     (lib.tagging on title + description, plus tag_assistance_listing per ALN) and keyword_hits
     (local regex hits).

Usage: .venv/bin/python scripts/35_pull_grantsgov.py [--refresh]   (no key needed)
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import (INTERIM, RateLimiter, latest_raw, log, register_source, rel, save_raw, session, stamp,
                        today)
from lib.tagging import tag_assistance_listing, tag_text

GG = "https://api.grants.gov/v1/api"
ROWS = 5000
# 24 target ALNs (scripts/12_probe_federal.py list minus 59.073 PPP)
CFDAS = ["14.267", "14.231", "14.241", "14.218", "14.239", "16.575", "16.588", "16.736", "93.671",
         "93.959", "93.958", "93.243", "21.027", "21.019", "97.024", "64.033", "17.258", "17.259",
         "16.812", "14.235", "10.561", "14.251", "14.252", "21.023"]
KEYWORDS = ["homelessness", "housing", "domestic violence", "victim services", "women", "substance use",
            "workforce", "reentry", "veterans", "aging"]
# local text match; small documented variants of each keyword
KW_RE = {
    "homelessness": r"\bhomeless(ness)?\b", "housing": r"\bhousing\b", "domestic violence": r"\bdomestic violence\b",
    "victim services": r"\bvictim services?\b", "women": r"\bwom[ae]n\b",
    "substance use": r"\bsubstance (use|misuse|abuse)\b", "workforce": r"\bworkforce\b", "reentry": r"\bre-?entry\b",
    "veterans": r"\bveterans?\b", "aging": r"\baging\b",
}
KW_RE = {k: re.compile(v, re.I) for k, v in KW_RE.items()}
ELIG_NONPROFIT = {"12", "13", "25", "99"}

S = session()
RL = RateLimiter(2.0)
MANIFEST: list[dict] = []


def post(desc: str, url: str, body: dict):
    RL.wait()
    try:
        r = S.post(url, json=body, timeout=300)
    except Exception as e:  # noqa: BLE001
        MANIFEST.append({"desc": desc, "url": url, "payload": body, "status": f"error: {e.__class__.__name__}",
                         "raw": None, "at": stamp()})
        return None, None
    p = save_raw("grantsgov", desc, r.content, "json")
    MANIFEST.append({"desc": desc, "url": url, "payload": body, "status": r.status_code, "raw": rel(p), "at": stamp()})
    try:
        return r.json(), p
    except ValueError:
        return None, p


def search_all(desc: str, extra: dict) -> list[dict]:
    hits, start = [], 0
    while True:
        j, _ = post(f"{desc}_s{start}" if start else desc, f"{GG}/search2",
                    dict(extra, rows=ROWS, startRecordNum=start, oppStatuses="forecasted|posted"))
        d = (j or {}).get("data") or {}
        page = d.get("oppHits") or []
        hits += page
        if not page or len(hits) >= (d.get("hitCount") or 0):
            break
        start += ROWS
    return hits


def dstr(s: str | None) -> str:
    """'2026-11-02-00-00-00' -> '2026-11-02'."""
    return s[:10] if s and re.match(r"\d{4}-\d{2}-\d{2}", s) else ""


def num(x) -> int | None:
    try:
        return int(float(str(x).replace(",", "")))
    except (TypeError, ValueError):
        return None


def clean_text(s: str | None) -> str:
    s = html.unescape(re.sub(r"<[^>]+>", " ", s or ""))
    return re.sub(r"\s+", " ", s).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true")
    refresh = ap.parse_args().refresh
    retrieved = today()
    universe = search_all("search2_35_posted_forecasted_all", {})
    by_id = {str(h["id"]): h for h in universe}
    target = set(CFDAS)
    local_cfda = {i for i, h in by_id.items() if target & set(h.get("cfdaList") or [])}
    cfda_key = {}
    for c in CFDAS:
        for h in search_all(f"search2_35_cfda_{c}", {"cfda": c}):
            cfda_key.setdefault(str(h["id"]), set()).add(c)
            by_id.setdefault(str(h["id"]), h)
    kw_search = {}
    for k in KEYWORDS:
        q = f'"{k}"' if " " in k else k
        for h in search_all(f"search2_35_kw_{k.replace(' ', '_')}", {"keyword": q}):
            kw_search.setdefault(str(h["id"]), set()).add(k)
            by_id.setdefault(str(h["id"]), h)
    title_hit = {i for i, h in by_id.items() if any(KW_RE[k].search(html.unescape(h.get("title") or "")) for k in KEYWORDS)}
    cands = sorted(local_cfda | set(cfda_key) | set(kw_search) | title_hit, key=int)

    rows, failed, dropped, reused = [], [], [], 0
    for oid in cands:
        old = None if refresh else latest_raw("grantsgov", f"fetchOpportunity_35_{oid}.json")
        if old:
            j, p = json.loads(old.read_text()), old
            reused += 1
        else:
            j, p = post(f"fetchOpportunity_35_{oid}", f"{GG}/fetchOpportunity", {"opportunityId": int(oid)})
        d = (j or {}).get("data") or {}
        if not d:
            failed.append(oid)
            continue
        blk = d.get("synopsis") or d.get("forecast") or {}
        is_fc = not d.get("synopsis") and bool(d.get("forecast"))
        h = by_id.get(oid, {})
        status = (h.get("oppStatus") or ("forecasted" if is_fc else "posted")).lower()
        cfdas = [c.get("cfdaNumber") for c in d.get("cfdas") or [] if c.get("cfdaNumber")]
        cf_titles = " ".join(c.get("programTitle") or "" for c in d.get("cfdas") or [])
        title = html.unescape(d.get("opportunityTitle") or h.get("title") or "")
        desc = clean_text(blk.get("synopsisDesc") or blk.get("forecastDesc"))
        elig = [a.get("id") for a in blk.get("applicantTypes") or [] if a.get("id")]
        elig_txt = clean_text(blk.get("applicantEligibilityDesc"))
        text = f"{title} {desc} {cf_titles} {elig_txt}"
        kw_text = [k for k in KEYWORDS if KW_RE[k].search(text)]
        kw_srch = [k for k in KEYWORDS if k in kw_search.get(oid, set())]
        cf_match = sorted(set(cfdas) & target | cfda_key.get(oid, set()))
        if not kw_text and not cf_match:
            dropped.append(oid)
            continue
        tags = [t for t in tag_text(f"{title} {desc}", default_other=False).split(";") if t]
        for c in cfdas:
            tags += [t for t in tag_assistance_listing(c).split(";") if t and t not in tags]
        agency = (d.get("agencyDetails") or {}).get("agencyName") or blk.get("agencyName") or h.get("agency")
        rows.append({
            "opportunity_id": oid, "opportunity_number": d.get("opportunityNumber"), "title": title,
            "funder_name": (agency or "").strip(), "agency_code": d.get("owningAgencyCode") or h.get("agencyCode"),
            "status": status, "assistance_listings": ";".join(cfdas), "eligibility_codes": ";".join(elig),
            "eligibility_text": elig_txt[:1000],
            "award_floor": num(blk.get("awardFloor")), "award_ceiling": num(blk.get("awardCeiling")),
            "estimated_total_funding": num(blk.get("estimatedFunding")), "expected_awards": num(blk.get("numberOfAwards")),
            "post_date": dstr(blk.get("postingDateStr")),
            "close_date": dstr(blk.get("responseDateStr") or blk.get("estApplicationResponseDateStr")),
            "forecast_award_date": dstr(blk.get("estAwardDateStr")),
            "funding_category": ";".join(c.get("description", "") for c in blk.get("fundingActivityCategories") or []),
            "program_area_tags": ";".join(tags) or "other",
            "keyword_hits": ";".join(kw_text),
            "url": f"https://www.grants.gov/search-results-detail/{oid}", "source_id": "api_grantsgov",
            "retrieved_date": retrieved, "confidence": "high", "basis": "documented",
            "x_top_agency": (d.get("topAgencyDetails") or {}).get("agencyName"),
            "x_funding_instruments": ";".join(f.get("description", "") for f in blk.get("fundingInstruments") or []),
            "x_opportunity_category": (d.get("opportunityCategory") or {}).get("description"),
            "x_cfda_match": ";".join(cf_match),
            "x_keyword_hits_text": ";".join(kw_text), "x_keyword_hits_search": ";".join(kw_srch),
            "x_elig_nonprofit": int(bool(set(elig) & ELIG_NONPROFIT)), "x_elig_501c3": int("12" in elig or "99" in elig),
            "x_cost_sharing": blk.get("costSharing"), "x_forecast_fiscal_year": blk.get("fiscalYear") if is_fc else "",
            "x_est_synopsis_post_date": dstr(blk.get("estSynopsisPostingDateStr")) if is_fc else "",
            "x_last_updated": blk.get("lastUpdatedDate"), "x_description_excerpt": desc[:500],
            "x_raw_file": rel(p) if p else "",
        })
    fields = list(rows[0].keys()) if rows else []
    out = INTERIM / "stage_fact_opportunities__grantsgov.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    man = save_raw("grantsgov", "pull35_manifest", {"script": "scripts/35_pull_grantsgov.py", "run_date": retrieved,
                                                    "candidates": cands, "kept": [r["opportunity_id"] for r in rows],
                                                    "dropped_by_local_filter": dropped, "failed_fetch": failed,
                                                    "fetch_reused_from_raw": reused, "requests": MANIFEST}, "json")
    register_source("api_grantsgov", "Grants.gov REST API (search2, fetchOpportunity)", GG,
                    "U.S. Department of Health and Human Services (Grants.gov PMO)", "Public domain (U.S. government data)",
                    "Keyless. Phase 4 (scripts/35_pull_grantsgov.py): posted+forecasted universe, cfda-key and keyword "
                    "searches, fetchOpportunity details for kept opportunities.")
    dup = len(rows) - len({r["opportunity_id"] for r in rows})
    kwc = {k: sum(1 for r in rows if k in r["keyword_hits"].split(";")) for k in KEYWORDS}
    log("35_pull_grantsgov: opportunities",
        f"- universe posted+forecasted {len(universe)}; candidates {len(cands)} (local cfdaList {len(local_cfda)}, cfda key "
        f"{len(cfda_key)}, keyword search {len(kw_search)}, title regex {len(title_hit)}); fetched {len(cands) - reused} "
        f"(reused {reused} saved responses); fetch failures {len(failed)}; dropped by local filter {len(dropped)}\n"
        f"- {rel(out)}: {len(rows)} rows ({sum(1 for r in rows if r['status'] == 'posted')} posted, "
        f"{sum(1 for r in rows if r['status'] == 'forecasted')} forecasted); duplicate ids {dup}\n"
        f"- keyword_hits counts: {json.dumps(kwc)}\n- target-ALN rows: {sum(1 for r in rows if r['x_cfda_match'])}; "
        f"nonprofit-eligible (12/13/25/99): {sum(r['x_elig_nonprofit'] for r in rows)}\n- manifest {rel(man)}")
    print(json.dumps({"universe": len(universe), "candidates": len(cands), "dropped": len(dropped), "rows": len(rows),
                      "failed": len(failed),
                      "dup": dup, "kw": kwc, "cfda_rows": sum(1 for r in rows if r['x_cfda_match'])}, indent=1))


if __name__ == "__main__":
    main()
