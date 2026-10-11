"""Phase 4 bulk pull: USAspending prime awards + subawards, Treasury SLFRF subawards, and staging of
interim/stage_fact_gov_awards__federal.csv (USAspending + FAC SEFA lines + Treasury SLFRF DC rows).

Sections (run all in order, or pick with --only):
  usaspending  POST /api/v2/download/awards/ jobs, polled via /api/v2/download/status/, zips saved to
               raw/usaspending/:
                 cfda_{DC,MD,VA}  24 target assistance listings (recon list minus 59.073 PPP), recipient
                                  location = state, all assistance award types, FY2019-FY2026.
                                  Subaward file: sub-recipient located in the state.
                 calvary          recipient_search_text = Calvary's name + UEI, all assistance types,
                                  FY2008+ (catches the name-only PPP loan and HUD 14.251).
                 uei_bNN          recipient_search_text = UEIs of in-scope orgs (calvary, core_peers,
                                  dc_sector, dmv_sector, named_comparators) from interim/uei_ein_map.csv
                                  (scripts/34_pull_fac.py) + Calvary's UEI; any CFDA, all assistance types,
                                  FY2019-FY2026; 20 UEIs per job. Named comparators' UEIs are excluded here.
                 named_{ein}      named comparators (NAMED): recipient_search_text = their UEIs (FAC map, else
                                  USAspending recipient search) + legal name; all assistance types, FY2019-FY2026.
                                  Rows found only by this job are kept only if they resolve to that EIN.
  slfrf        Treasury SLFRF public-data page + subaward workbook (SLFRF-Subaward-USASpending-File.xlsx)
               -> raw/treasury/. Reuses an existing raw/treasury/ copy unless --refresh.
  stage        Builds interim/stage_fact_gov_awards__federal.csv from the latest raw of the three sources:
                 - USAspending prime award summaries (flow_type=prime) and subawards (flow_type=subaward)
                 - FAC federal_awards lines for in-scope reports (34's manifest): is_direct=Y -> prime,
                   is_direct=N -> pass_through_expenditure
                 - Treasury SLFRF subawards whose prime awardee is in DC (flow_type=subaward)
               Runs the Calvary reconciliation and duplicate checks, logs, appends notes.

Run order: scripts/34_pull_fac.py first (UEIs + FAC raw), then this script.
Usage:
  .venv/bin/python scripts/33_pull_usaspending.py [--only usaspending,slfrf,stage] [--refresh] [--ipv 4|6] [--no-count]
Download jobs already finished in an earlier run (same filters, zip on disk) are reused unless --refresh.
Pacing: <= 2 downloads in flight, 20 s between submits, 30 s between status polls. The API dropped
connections for about an hour after faster bursts on 2026-10-10.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import sys
import time
import socket
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

import urllib3.util.connection as _u3conn

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import (CLEAN, INTERIM, RAW, ROOT, RateLimiter, append_md, latest_raw, log, norm_ein,
                        norm_name, raw_path, register_source, rel, save_raw, session, stamp, today)

CALVARY_EIN = "521307706"
CALVARY_UEI = "KMGRTKET2KJ1"
CALVARY_NAME = "CALVARY WOMEN'S SERVICES"
USA = "https://api.usaspending.gov"
TP = [{"start_date": "2018-10-01", "end_date": "2026-09-30"}]       # federal FY2019-FY2026
TP_ALL = [{"start_date": "2007-10-01", "end_date": "2026-09-30"}]   # search floor
STATES = ["DC", "MD", "VA"]
# 24 target assistance listings: scripts/12_probe_federal.py CFDAS minus 59.073 (PPP)
CFDAS = ["14.267", "14.231", "14.241", "14.218", "14.239", "16.575", "16.588", "16.736", "93.671",
         "93.959", "93.958", "93.243", "21.027", "21.019", "97.024", "64.033", "17.258", "17.259",
         "16.812", "14.235", "10.561", "14.251", "14.252", "21.023"]
ASST = ["02", "03", "04", "05", "06", "10", "07", "08", "09", "11", "-1"]   # all assistance groups
SCOPE_UNIVERSES = ["calvary", "core_peers", "dc_sector", "dmv_sector", "named_comparators"]
# Named comparators added at the lead's request (universe named_comparators, rule NC1). Hard-coded so the
# pull and staging work before dim_universe_membership carries them.
import csv as _csv
_NAME_OVERRIDE = {"311597223": "DOWNTOWN WOMEN'S CENTER"}   # USAspending recipient name differs from BMF
NAMED = {r["ein"]: {"name": _NAME_OVERRIDE.get(r["ein"], r["name"].split(" (")[0].upper()), "state": r["state"], "label": r["name"]}
         for r in _csv.DictReader(open(Path(__file__).resolve().parents[1] / "config" / "named_comparators.csv", encoding="utf-8"))}
UEI_CHUNK = 20      # recipient_search_text with >20 terms returns HTTP 503 (tested 2026-10-10)

SLFRF_PAGE = ("https://home.treasury.gov/policy-issues/coronavirus/assistance-for-state-local-and-"
              "tribal-governments/state-and-local-fiscal-recovery-funds/public-data")
SLFRF_SUB = "https://home.treasury.gov/system/files/136/SLFRF-Subaward-USASpending-File.xlsx"

DCGOV_RE = re.compile(r"(DISTRICT OF COLUMBIA,? GOVERNMENT|GOVERNMENT OF (THE )?DISTRICT OF COLUMBIA|"
                      r"DISTRICT COLUMBIA GOVERNMENT|^DC OFFICE|^DC DEPARTMENT|^OFFICE OF VICTIM SERVICES)", re.I)
# FAC passthrough_name -> DC government (free text, many spellings)
DC_PT_RE = re.compile(r"(district of columbia|^\s*(the\s+)?d\.?\s?c\.?\s|\bd\.?c\.?\s+(department|dept|office|government|"
                      r"health|human|housing|executive|mayor)|victim services and justice|\bovsjg\b|"
                      r"office of the state superintendent of education|^\s*dc\s*$|^\s*dc-|[,-]\s*d\.?c\.?\s*$|columubia)", re.I)
DC_PT_NOT = re.compile(r"(foundation|\bbar\b|universit|college|\binc\b|\bllc\b|catholic|charities|united way|"
                       r"community partnership|children'?s national|hospital|efsp|emergency food and shelter|fema board)", re.I)


def is_dc_gov_pt(name: str) -> bool:
    """FAC passthrough_name reads as a DC government agency (not a DC-named nonprofit)."""
    return any(bool(DC_PT_RE.search(n)) and not DC_PT_NOT.search(n) for n in (name or "").split(" | "))
TCP_RE = re.compile(r"community partnership", re.I)

FED_PREFIX = {"10": "Department of Agriculture", "11": "Department of Commerce", "12": "Department of Defense",
              "14": "Department of Housing and Urban Development", "15": "Department of the Interior",
              "16": "Department of Justice", "17": "Department of Labor", "19": "Department of State",
              "20": "Department of Transportation", "21": "Department of the Treasury",
              "39": "General Services Administration", "43": "National Aeronautics and Space Administration",
              "45": "National Foundation on the Arts and the Humanities", "47": "National Science Foundation",
              "59": "Small Business Administration", "64": "Department of Veterans Affairs",
              "66": "Environmental Protection Agency", "81": "Department of Energy", "84": "Department of Education",
              "93": "Department of Health and Human Services", "94": "Corporation for National and Community Service",
              "96": "Social Security Administration", "97": "Department of Homeland Security",
              "98": "Agency for International Development"}

# On 2026-10-10 api/files.usaspending.gov answered one address family with empty replies for ~1 h after
# request bursts (IPv6 first, later IPv4). --ipv 4|6 pins the family; default leaves the system order.
def set_ip_family(v: str):
    if v == "4":
        _u3conn.allowed_gai_family = lambda: socket.AF_INET
    elif v == "6":
        _u3conn.allowed_gai_family = lambda: socket.AF_INET6

S = session()
S1 = session(retries=0)     # no adapter retries: download submits/polls retry in our own loop
RL = RateLimiter(2.0)
MAX_INFLIGHT = 2
SUBMIT_GAP = 20   # seconds between download submits (server refused connections after a burst)
POLL_GAP = 30     # seconds between status-poll rounds
NO_COUNT = False  # --no-count skips the optional download/count sizing calls
MANIFEST: list[dict] = []
REFRESH = False


# ---------------------------------------------------------------- helpers
def note(desc, method, url, payload, status, path):
    MANIFEST.append({"desc": desc, "method": method, "url": url, "payload": payload, "status": status,
                     "raw": rel(path) if path else None, "at": stamp()})


def post(desc: str, url: str, body: dict, source: str = "usaspending", sess=None):
    RL.wait()
    try:
        r = (sess or S).post(url, json=body, timeout=(15, 90))
    except Exception as e:  # noqa: BLE001
        note(desc, "POST", url, body, f"error: {e.__class__.__name__}", None)
        return None, None
    p = save_raw(source, desc, r.content, "json")
    note(desc, "POST", url, body, r.status_code, p)
    try:
        return r.status_code, r.json()
    except ValueError:
        return r.status_code, None


def stream_get(source: str, desc: str, url: str, ext: str) -> Path:
    p = raw_path(source, desc, ext)
    RL.wait()
    with S.get(url, stream=True, timeout=(15, 300)) as r:
        r.raise_for_status()
        with open(p, "wb") as f:
            for chunk in r.iter_content(1 << 20):
                f.write(chunk)
    note(desc, "GET", url, None, 200, p)
    return p


def to_int(x) -> int | None:
    if x is None or str(x).strip() in ("", "None", "nan"):
        return None
    try:
        return int(round(float(str(x).replace(",", ""))))
    except ValueError:
        return None


def fy_of(date: str | None) -> int | None:
    """Federal FY (Oct-Sep) of an ISO date."""
    if not date or len(str(date)) < 7:
        return None
    y, m = int(str(date)[:4]), int(str(date)[5:7])
    return y + 1 if m >= 10 else y


def load_universes() -> dict[str, str]:
    uni = defaultdict(set)
    with open(CLEAN / "dim_universe_membership.csv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            e = norm_ein(r["ein"])
            if e:
                uni[e].add(r["universe"])
    for e in NAMED:
        uni[e].add("named_comparators")
    return {e: ";".join(sorted(u)) for e, u in uni.items()}


def load_name_index() -> dict[tuple, set]:
    """(norm_name, state) -> EINs, over the in-scope universes, from BMF names."""
    idx = defaultdict(set)
    with open(CLEAN / "dim_universe_membership.csv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["universe"] in SCOPE_UNIVERSES and r.get("org_name_bmf"):
                idx[(norm_name(r["org_name_bmf"]), (r.get("state") or "").upper())].add(norm_ein(r["ein"]))
    return idx


def load_uei_map() -> dict[str, dict]:
    """UEI -> {ein, ambiguous, audit_year} using the latest audit year per UEI."""
    p = INTERIM / "uei_ein_map.csv"
    by = defaultdict(list)
    if p.exists():
        with open(p, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                by[r["uei"]].append(r)
    out = {}
    for u, rows in by.items():
        rows.sort(key=lambda r: r["audit_year"])
        out[u] = {"ein": rows[-1]["ein"], "ambiguous": len({r["ein"] for r in rows}) > 1,
                  "in_scope": rows[-1].get("in_scope") == "1"}
    out.setdefault(CALVARY_UEI, {"ein": CALVARY_EIN, "ambiguous": False, "in_scope": True})
    return out


# ---------------------------------------------------------------- USAspending downloads
def named_ueis(umap: dict) -> dict[str, list]:
    """Named EIN -> UEIs from the FAC map; falls back to USAspending recipient search by name + state."""
    out = {}
    for ein, d in NAMED.items():
        us = sorted(u for u, m in umap.items() if m["ein"] == ein)
        if not us:
            _, j = post(f"recipient_search_named_{ein}", f"{USA}/api/v2/recipient/",
                        {"keyword": d["name"], "award_type": "all", "limit": 50, "page": 1})
            us = sorted({x["uei"] for x in (j or {}).get("results", [])
                         if x.get("uei") and norm_name(x.get("name")) == norm_name(d["name"])})
        out[ein] = us
    return out


def usaspending():
    umap = load_uei_map()
    nmap = named_ueis(umap)
    skip = {u for us in nmap.values() for u in us}
    ueis = sorted(({u for u, d in umap.items() if d["in_scope"]} | {CALVARY_UEI}) - skip)
    jobs = {f"cfda_{st}": {"program_numbers": CFDAS, "recipient_locations": [{"country": "USA", "state": st}],
                           "award_type_codes": ASST, "time_period": TP} for st in STATES}
    jobs["calvary"] = {"recipient_search_text": [CALVARY_NAME, CALVARY_UEI], "award_type_codes": ASST,
                       "time_period": TP_ALL}
    for i in range(0, len(ueis), UEI_CHUNK):
        jobs[f"uei_b{i // UEI_CHUNK:02d}"] = {"recipient_search_text": ueis[i:i + UEI_CHUNK],
                                              "award_type_codes": ASST, "time_period": TP}
    for ein, us in nmap.items():
        jobs[f"named_{ein}"] = {"recipient_search_text": us + [NAMED[ein]["name"]], "award_type_codes": ASST,
                                "time_period": TP}
    # Submit in waves of MAX_INFLIGHT: with ~10 downloads queued from one client the 10th
    # download/awards POST hung for >10 min (2026-10-10). Each job: size (download/count), submit, poll.
    sizes, pending, done = {}, {}, {}
    # resume: reuse a finished zip from earlier pull33 manifests when the job's filters are identical
    for mp in sorted(RAW.joinpath("usaspending").glob("*_pull33_manifest.json")):
        prev = json.loads(mp.read_text())
        for job, res in prev.get("results", {}).items():
            if (job in jobs and prev["jobs"].get(job) == jobs[job] and res.get("status") == "finished"
                    and res.get("zip") and (ROOT / res["zip"]).exists() and not REFRESH):
                done[job] = dict(res, reused_from=rel(mp))
                sizes[job] = prev.get("sizes", {}).get(job)
    queue = [j for j in jobs if j not in done]
    t0 = time.time()
    while (queue or pending) and time.time() - t0 < 5400:
        while queue and len(pending) < MAX_INFLIGHT:
            job = queue.pop(0)
            flt = jobs[job]
            sizes[job] = {}
            for lvl in ("awards", "subawards") if not NO_COUNT else ():
                _, j = post(f"dl33_count_{job}_{lvl}", f"{USA}/api/v2/download/count/",
                            {"filters": flt, "spending_level": lvl})
                sizes[job][lvl] = (j or {}).get("calculated_count")
            sc, j = None, None
            for _try in range(3):
                sc, j = post(f"dl33_request_{job}", f"{USA}/api/v2/download/awards/",
                             {"filters": flt, "file_format": "csv"}, sess=S1)
                if sc == 200 and j and j.get("file_name"):
                    break
                time.sleep(30)
            time.sleep(SUBMIT_GAP)
            if sc == 200 and j and j.get("file_name"):
                pending[job] = j
            else:
                done[job] = {"status": f"request failed http {sc}", "detail": (j or {}).get("detail")}
        for job in list(pending):
            RL.wait()
            try:
                r = S1.get(f"{USA}/api/v2/download/status/", params={"file_name": pending[job]["file_name"]},
                           timeout=(15, 60))
                st = r.json() if r.ok else {"status": f"http {r.status_code}"}
            except Exception:  # noqa: BLE001
                continue
            if st.get("status") in ("finished", "failed"):
                ps = save_raw("usaspending", f"dl33_status_{job}", st, "json")
                note(f"dl33_status_{job}", "GET", f"{USA}/api/v2/download/status/",
                     {"file_name": pending[job]["file_name"]}, st.get("status"), ps)
                res = {"status": st.get("status"), "total_rows": st.get("total_rows"), "seconds": round(time.time() - t0)}
                if st.get("status") == "finished":
                    pz = stream_get("usaspending", f"dl33_{job}", st.get("file_url") or pending[job]["file_url"], "zip")
                    res["zip"] = rel(pz)
                    res["members"] = zip_rows(pz)
                done[job] = res
                del pending[job]
        time.sleep(POLL_GAP)
    for job in pending:
        done[job] = {"status": "timeout"}
    for job in queue:
        done[job] = {"status": "not_submitted (time budget)"}
    man = save_raw("usaspending", "pull33_manifest", {"script": "scripts/33_pull_usaspending.py", "run_date": today(),
                                                      "jobs": jobs, "sizes": sizes, "results": done,
                                                      "n_ueis": len(ueis), "named_ueis": nmap,
                                                      "requests": MANIFEST}, "json")
    MANIFEST.clear()
    register_source("bulk_usaspending", "USAspending.gov award downloads (download/awards, bulk_download/awards)",
                    f"{USA}/api/v2/download/awards/", "U.S. Department of the Treasury, Bureau of the Fiscal Service",
                    "Public domain (U.S. government data); cite USAspending.gov",
                    "Phase 4 (scripts/33_pull_usaspending.py): prime award summaries + subawards; 24 target ALNs "
                    "for DC/MD/VA recipients FY2019-FY2026; in-scope UEIs (any ALN); Calvary by name+UEI FY2008+.")
    log("33_pull_usaspending: downloads",
        f"- jobs {len(jobs)} ({len(ueis)} in-scope UEIs in {sum(1 for j in jobs if j.startswith('uei_'))} chunks)\n"
        + "\n".join(f"  - {k}: count {sizes.get(k)}; {json.dumps({kk: vv for kk, vv in v.items() if kk != 'zip'})}"
                    for k, v in done.items())
        + f"\n- manifest {rel(man)}")
    bad = {k: v for k, v in done.items() if v.get("status") != "finished"}
    if bad:
        print("FAILED JOBS:", json.dumps(bad))


def zip_rows(p: Path) -> dict:
    csv.field_size_limit(1 << 30)
    out = {}
    with zipfile.ZipFile(p) as z:
        for m in z.namelist():
            with z.open(m) as fh:
                out[m] = sum(1 for _ in csv.reader(io.TextIOWrapper(fh, encoding="utf-8", errors="replace"))) - 1
    return out


def read_zip(p: Path):
    """Yield (kind, row) where kind is 'prime' or 'sub'."""
    csv.field_size_limit(1 << 30)
    with zipfile.ZipFile(p) as z:
        for m in z.namelist():
            kind = "sub" if "Subaward" in m else "prime"
            with z.open(m) as fh:
                for r in csv.DictReader(io.TextIOWrapper(fh, encoding="utf-8", errors="replace")):
                    yield kind, r


# ---------------------------------------------------------------- Treasury SLFRF
def slfrf():
    RL.wait()
    r = S.get(SLFRF_PAGE, timeout=120)
    pg = save_raw("treasury", "slfrf_public_data_page", r.content, "html")
    note("slfrf_public_data_page", "GET", SLFRF_PAGE, None, r.status_code, pg)
    links = sorted(set(re.findall(r'href="?([^"\s>]*[Ss]ubaward[^"\s>]*\.xlsx)', r.text)))
    links = [lk if lk.startswith("http") else "https://home.treasury.gov" + lk for lk in links]
    url = next((lk for lk in links if "USASpending" in lk), links[0] if links else SLFRF_SUB)
    old = latest_raw("treasury", "SLFRF-Subaward-USASpending-File.xlsx")
    if old and not REFRESH:
        p, fresh = old, False
        note("SLFRF-Subaward-USASpending-File", "GET", url, None, "reused", p)
    else:
        p, fresh = stream_get("treasury", "SLFRF-Subaward-USASpending-File", url, "xlsx"), True
    recon = latest_raw("treasury_slfrf", "SLFRF-Subaward-USASpending-File.xlsx")
    same = recon is not None and recon.stat().st_size == p.stat().st_size
    save_raw("treasury", "pull33_slfrf_manifest", {"subaward_links_on_page": links, "url": url, "file": rel(p),
                                                    "fresh_download": fresh, "same_size_as_recon_copy": same,
                                                    "requests": MANIFEST}, "json")
    MANIFEST.clear()
    register_source("bulk_treasury_slfrf", "Treasury SLFRF public data files", SLFRF_PAGE,
                    "U.S. Department of the Treasury", "Public domain (U.S. government data)",
                    "SLFRF-Subaward-USASpending-File.xlsx (subawards as of 2023-06-30; USAspending subaward layout, "
                    "not loaded into USAspending search). Phase 4: raw/treasury/ via scripts/33_pull_usaspending.py.")
    log("33_pull_usaspending: slfrf",
        f"- public-data page subaward links: {links}\n- workbook {rel(p)} (fresh={fresh}; same size as recon copy: {same})")


# ---------------------------------------------------------------- staging
FIELDS = ["award_row_id", "recipient_ein", "recipient_uei", "recipient_name_raw", "awarding_agency", "funding_agency",
          "program_name", "assistance_listing", "award_id", "award_type", "flow_type", "pass_through_entity",
          "pass_through_ein", "period_start", "period_end", "fiscal_year", "fiscal_year_basis", "amount",
          "amount_type", "source_type", "source_id", "source_page", "conflict_flag", "retrieved_date", "confidence",
          "basis",
          "x_recipient_state", "x_recipient_city", "x_recipient_business_types", "x_recipient_name_norm",
          "x_ein_method", "x_ein_name_match", "x_universes", "x_in_scope", "x_action_date", "x_latest_action_date",
          "x_total_outlayed_amount", "x_loan_subsidy_cost", "x_def_codes", "x_prime_award_unique_key",
          "x_prime_award_id", "x_prime_awardee_uei", "x_pass_through_is_dc_gov", "x_description",
          "x_pulls", "x_audit_year", "x_report_id", "x_award_reference", "x_is_major", "x_is_loan",
          "x_federal_program_total", "x_cluster_name", "x_passthrough_id", "x_org_passes_through",
          "x_org_passthrough_amount", "x_findings_count", "x_fac_data_source", "x_n_reports_collapsed", "x_conflict_note", "x_raw_file"]

ATYPE = {"02": "grant", "03": "grant", "04": "grant", "05": "cooperative_agreement", "06": "direct_payment",
         "10": "direct_payment", "07": "loan", "08": "loan", "09": "other", "11": "other", "-1": "other"}


def cfda_split(s: str) -> tuple[str, str]:
    """'14.251: TITLE; 14.252: TITLE2' -> ('14.251;14.252', 'TITLE; TITLE2')."""
    nums, titles = [], []
    for part in re.split(r";\s*(?=\d{2}\.\d{3})", s or ""):
        m = re.match(r"\s*(\d{2}\.[\w]+):\s*(.*)", part)
        if m and m.group(1) not in nums:
            nums.append(m.group(1))
            titles.append(m.group(2).strip())
    return ";".join(nums), "; ".join(titles)


class Ctx:
    def __init__(self):
        self.uni = load_universes()
        self.umap = load_uei_map()
        self.names = load_name_index()
        self.core = {e for e, u in self.uni.items() if set(u.split(";")) & set(SCOPE_UNIVERSES)}
        self.core.add(CALVARY_EIN)

    def resolve(self, uei: str | None, name: str | None, state: str | None):
        """(recipient_ein, method, name_match_candidate)."""
        uei = (uei or "").strip().upper()
        nm = norm_name(name)
        cand = self.names.get((nm, (state or "").upper()), set())
        cand_s = next(iter(cand)) if len(cand) == 1 else ""
        if uei and uei in self.umap:
            d = self.umap[uei]
            return d["ein"], "uei_fac_map" + ("_ambiguous" if d["ambiguous"] else ""), cand_s
        if nm == norm_name(CALVARY_NAME) and (state or "").upper() == "DC":
            return CALVARY_EIN, "calvary_identity", cand_s
        for ein, d in NAMED.items():
            if nm == norm_name(d["name"]) and (state or "").upper() == d["state"]:
                return ein, "named_identity", cand_s
        return "", "", cand_s

    def scope_cols(self, ein: str, cand: str) -> dict:
        """x_in_scope: 1 = recipient_ein in scope; name_candidate = only the exact-name candidate is; else 0."""
        if ein:
            return {"x_universes": self.uni.get(ein, ""), "x_in_scope": int(ein in self.core)}
        if cand:
            return {"x_universes": "candidate:" + self.uni.get(cand, ""),
                    "x_in_scope": "name_candidate" if cand in self.core else 0}
        return {"x_universes": "", "x_in_scope": 0}


def keep_named(pulls: set, ein: str) -> bool:
    """Rows found only by named_{ein} jobs (name text search can hit namesakes) must resolve to that EIN."""
    if pulls and all(p.startswith("named_") for p in pulls):
        return ein in {p[len("named_"):] for p in pulls}
    return True


def stage_usaspending(ctx: Ctx, rows: list, stats: dict):
    man_p = latest_raw("usaspending", "pull33_manifest.json")
    if not man_p:
        stats["usaspending"] = "no manifest"
        return
    man = json.loads(man_p.read_text())
    prime, sub = {}, {}
    pulls = defaultdict(set)
    retrieved = man.get("run_date") or today()
    for job, res in man["results"].items():
        if res.get("status") != "finished":
            continue
        zp = ROOT / res["zip"]
        for kind, r in read_zip(zp):
            if kind == "prime":
                k = r["assistance_award_unique_key"]
                prime.setdefault(k, (r, res["zip"]))
            else:
                k = "|".join([r["prime_award_unique_key"], r.get("subaward_sam_report_id") or "", r["subaward_number"],
                              r["subaward_action_date"], r["subaward_amount"], r.get("subawardee_uei") or "",
                              norm_name(r.get("subawardee_name"))])
                sub.setdefault(k, (r, res["zip"]))
            pulls[k].add(job.split("_b")[0] if job.startswith("uei_") else job)
    for k, (r, zf) in prime.items():
        code = r.get("assistance_type_code") or ""
        is_loan = ATYPE.get(code) == "loan"
        aln, title = cfda_split(r.get("cfda_numbers_and_titles"))
        ein, meth, cand = ctx.resolve(r.get("recipient_uei"), r.get("recipient_name"), r.get("recipient_state_code"))
        if not keep_named(pulls[k], ein):
            stats["named_job_rows_dropped"] = stats.get("named_job_rows_dropped", 0) + 1
            continue
        rows.append({
            "award_row_id": f"usa_p_{k}", "recipient_ein": ein, "recipient_uei": r.get("recipient_uei"),
            "recipient_name_raw": r.get("recipient_name") or r.get("recipient_name_raw"),
            "awarding_agency": r.get("awarding_agency_name"), "funding_agency": r.get("funding_agency_name"),
            "program_name": title, "assistance_listing": aln, "award_id": r.get("award_id_fain") or r.get("award_id_uri"),
            "award_type": ATYPE.get(code, "other"), "flow_type": "prime",
            "period_start": r.get("period_of_performance_start_date"),
            "period_end": r.get("period_of_performance_current_end_date"),
            "fiscal_year": to_int(r.get("award_base_action_date_fiscal_year")), "fiscal_year_basis": "federal_fy",
            "amount": to_int(r.get("total_face_value_of_loan") if is_loan else r.get("total_obligated_amount")),
            "amount_type": "award_amount" if is_loan else "obligation",
            "source_type": "usaspending", "source_id": "bulk_usaspending", "source_page": r.get("usaspending_permalink"),
            "conflict_flag": 0, "retrieved_date": retrieved, "confidence": "high", "basis": "documented",
            "x_recipient_state": r.get("recipient_state_code"), "x_recipient_city": r.get("recipient_city_name"),
            "x_recipient_business_types": r.get("business_types_description"),
            "x_recipient_name_norm": norm_name(r.get("recipient_name")), "x_ein_method": meth, "x_ein_name_match": cand,
            **ctx.scope_cols(ein, cand),
            "x_action_date": r.get("award_base_action_date"), "x_latest_action_date": r.get("award_latest_action_date"),
            "x_total_outlayed_amount": to_int(r.get("total_outlayed_amount")),
            "x_loan_subsidy_cost": to_int(r.get("total_loan_subsidy_cost")) if is_loan else None,
            "x_def_codes": r.get("disaster_emergency_fund_codes"),
            "x_description": (r.get("prime_award_base_transaction_description") or "")[:300],
            "x_pulls": ";".join(sorted(pulls[k])), "x_raw_file": zf,
        })
    # The same subaward (prime, subaward number, action date, amount, sub-recipient) is often reported in
    # several SAM/FSRS reports; collapse to the most recently modified report so dollars count once.
    groups = defaultdict(list)
    for k, (r, zf) in sub.items():
        ck = (r["prime_award_unique_key"], r["subaward_number"], r["subaward_action_date"][:10], to_int(r["subaward_amount"]),
              (r.get("subawardee_uei") or "").upper() or norm_name(r.get("subawardee_name")))
        groups[ck].append(k)
    keep = {}
    for ck, ks in groups.items():
        ks.sort(key=lambda k: (sub[k][0].get("subaward_sam_report_last_modified_date") or "",
                               sub[k][0].get("subaward_sam_report_id") or ""))
        best = ks[-1]
        keep[best] = len(ks)
        for k in ks[:-1]:
            pulls[best] |= pulls[k]
    stats["usaspending_sub_reports"] = len(sub)
    sub = {k: v for k, v in sub.items() if k in keep}
    for k, (r, zf) in sub.items():
        aln, title = cfda_split(r.get("prime_award_cfda_numbers_and_titles"))
        ein, meth, cand = ctx.resolve(r.get("subawardee_uei"), r.get("subawardee_name"), r.get("subawardee_state_code"))
        if not keep_named(pulls[k], ein):
            stats["named_job_rows_dropped"] = stats.get("named_job_rows_dropped", 0) + 1
            continue
        pt_ein, _, _ = ctx.resolve(r.get("prime_awardee_uei"), r.get("prime_awardee_name"), r.get("prime_awardee_state_code"))
        st = (r.get("subaward_type") or "").lower()
        rows.append({
            "award_row_id": "usa_s_" + hashlib.sha1(k.encode()).hexdigest()[:16],
            "recipient_ein": ein, "recipient_uei": r.get("subawardee_uei"), "recipient_name_raw": r.get("subawardee_name"),
            "awarding_agency": r.get("prime_award_awarding_agency_name"),
            "funding_agency": r.get("prime_award_funding_agency_name"),
            "program_name": title, "assistance_listing": aln, "award_id": r.get("subaward_number"),
            "award_type": "grant" if st.startswith(("grant", "sub-grant")) else ("contract" if st.startswith(("contract", "sub-contract")) else "other"),
            "flow_type": "subaward", "pass_through_entity": r.get("prime_awardee_name"), "pass_through_ein": pt_ein,
            "fiscal_year": to_int(r.get("subaward_action_date_fiscal_year")) or fy_of(r.get("subaward_action_date")),
            "fiscal_year_basis": "federal_fy", "amount": to_int(r.get("subaward_amount")), "amount_type": "award_amount",
            "source_type": "usaspending", "source_id": "bulk_usaspending", "source_page": r.get("usaspending_permalink"),
            "conflict_flag": 0, "retrieved_date": retrieved, "confidence": "high", "basis": "documented",
            "x_recipient_state": r.get("subawardee_state_code"), "x_recipient_city": r.get("subawardee_city_name"),
            "x_recipient_business_types": r.get("subawardee_business_types"),
            "x_recipient_name_norm": norm_name(r.get("subawardee_name")), "x_ein_method": meth, "x_ein_name_match": cand,
            **ctx.scope_cols(ein, cand),
            "x_action_date": r.get("subaward_action_date"), "x_def_codes": r.get("prime_award_disaster_emergency_fund_codes"),
            "x_prime_award_unique_key": r.get("prime_award_unique_key"), "x_prime_award_id": r.get("prime_award_fain"),
            "x_prime_awardee_uei": r.get("prime_awardee_uei"),
            "x_pass_through_is_dc_gov": int(bool(DCGOV_RE.search(r.get("prime_awardee_name") or ""))),
            "x_description": (r.get("subaward_description") or "")[:300],
            "x_pulls": ";".join(sorted(pulls[k])), "x_n_reports_collapsed": keep[k], "x_raw_file": zf,
        })
    stats["usaspending_prime"] = len(prime)
    stats["usaspending_sub"] = len(sub)


def stage_fac(ctx: Ctx, rows: list, stats: dict):
    man_p = latest_raw("fac", "pull34_manifest.json")
    if not man_p:
        stats["fac"] = "no manifest"
        return
    man = json.loads(man_p.read_text())
    kept = man["kept_reports"]
    files = defaultdict(list)
    for q in man["requests"]:
        if q.get("raw") and q.get("status") == 200:
            files[q["role"]].append(ROOT / q["raw"])
    gen = {}
    for p in files["general"]:
        for g in json.loads(p.read_text()):
            gen[g["report_id"]] = g
    gen = {k: v for k, v in gen.items() if k in kept}
    # one report per (ein, fy_end_date): drop superseded resubmissions, then keep latest accepted
    best = {}
    for rid, g in gen.items():
        if (g.get("resubmission_status") or "") == "deprecated_via_resubmission":
            continue
        key = (norm_ein(g.get("auditee_ein")), g.get("fy_end_date"))
        if key not in best or (g.get("fac_accepted_date") or "") > (gen[best[key]].get("fac_accepted_date") or ""):
            best[key] = rid
    use = set(best.values())
    stats["fac_reports_kept"] = len(kept)
    stats["fac_reports_used"] = len(use)
    pts = defaultdict(list)
    for p in files["passthrough"]:
        for r in json.loads(p.read_text()):
            pts[(r["report_id"], r["award_reference"])].append(r)
    retrieved = man.get("run_date") or today()
    n = 0
    seen = set()
    for p in files["federal_awards"]:
        for a in json.loads(p.read_text()):
            rid = a["report_id"]
            if rid not in use:
                continue
            key = (rid, a["award_reference"])
            if key in seen:
                continue
            seen.add(key)
            g = gen[rid]
            ein = norm_ein(g.get("auditee_ein"))
            aln = f"{a.get('federal_agency_prefix')}.{a.get('federal_award_extension')}"
            pt = pts.get(key, [])
            pt_names = " | ".join(sorted({(x.get("passthrough_name") or "").strip() for x in pt if x.get("passthrough_name")}))
            direct = (a.get("is_direct") or "").upper()
            conflict = int(ein == CALVARY_EIN and g.get("audit_year") == "2023")
            fye = g.get("fy_end_date") or ""
            rows.append({
                "award_row_id": f"fac_{rid}_{a['award_reference']}", "recipient_ein": ein,
                "recipient_uei": g.get("auditee_uei"), "recipient_name_raw": g.get("auditee_name"),
                "awarding_agency": FED_PREFIX.get(str(a.get("federal_agency_prefix")), ""),
                "program_name": a.get("federal_program_name"), "assistance_listing": aln,
                "award_id": a.get("additional_award_identification") or "",
                "award_type": "loan" if (a.get("is_loan") or "").upper() == "Y" else "",
                "flow_type": "prime" if direct == "Y" else "pass_through_expenditure",
                "pass_through_entity": pt_names if direct != "Y" else "",
                "period_start": g.get("fy_start_date"), "period_end": fye,
                "fiscal_year": int(fye[:4]) if fye[:4].isdigit() else None, "fiscal_year_basis": "org_fy",
                "amount": to_int(a.get("amount_expended")), "amount_type": "expenditure",
                "source_type": "fac_sefa", "source_id": "api_fac",
                "source_page": f"https://app.fac.gov/dissemination/summary/{rid}",
                "conflict_flag": conflict, "retrieved_date": retrieved,
                "confidence": "low" if conflict else "high", "basis": "documented",
                "x_recipient_state": g.get("auditee_state"), "x_recipient_city": g.get("auditee_city"),
                "x_recipient_business_types": g.get("entity_type"), "x_recipient_name_norm": norm_name(g.get("auditee_name")),
                "x_ein_method": "fac_auditee_ein" if kept[rid] == "auditee_ein" else "fac_auditee_ein(additional_ein_in_scope)",
                **ctx.scope_cols(ein, ""),
                "x_pass_through_is_dc_gov": int(direct != "Y" and is_dc_gov_pt(pt_names)) if pt_names else "",
                "x_audit_year": g.get("audit_year"), "x_report_id": rid, "x_award_reference": a["award_reference"],
                "x_is_major": a.get("is_major"), "x_is_loan": a.get("is_loan"),
                "x_federal_program_total": to_int(a.get("federal_program_total")), "x_cluster_name": a.get("cluster_name"),
                "x_passthrough_id": " | ".join(sorted({(x.get("passthrough_id") or "").strip() for x in pt if x.get("passthrough_id")})),
                "x_org_passes_through": a.get("is_passthrough_award"),
                "x_org_passthrough_amount": to_int(a.get("passthrough_amount")),
                "x_findings_count": a.get("findings_count"), "x_fac_data_source": g.get("data_source"),
                "x_conflict_note": ("FAC audit_year 2023 SEFA repeats FY22 lines (FAC total $4,064,718); the FY23 audit "
                                    "PDF SEFA totals $937,999 (raw/inputs_extracted/sefa_federal_awards.csv). Prefer "
                                    "the audit PDF for FY23." if conflict else ""),
                "x_raw_file": rel(p),
            })
            n += 1
    stats["fac_lines"] = n
    # Reports of the same EIN with an identical SEFA line set (ALN, amount) -> conflict_flag on both.
    sig = defaultdict(list)
    for r in rows:
        if r["source_type"] == "fac_sefa":
            sig[r["x_report_id"]].append((r["assistance_listing"], r["amount"]))
    by_ein = defaultdict(lambda: defaultdict(list))
    for rid, lines in sig.items():
        by_ein[norm_ein(gen[rid].get("auditee_ein"))][tuple(sorted(lines, key=str))].append(rid)
    dup_rep = {}
    for e, sigs in by_ein.items():
        for rids in sigs.values():
            if len(rids) > 1:
                for rid in rids:
                    dup_rep[rid] = [x for x in rids if x != rid]
    for r in rows:
        if r["source_type"] == "fac_sefa" and r["x_report_id"] in dup_rep and not r["conflict_flag"]:
            r["conflict_flag"] = 1
            r["confidence"] = "low"
            r["x_conflict_note"] = ("Identical SEFA lines (ALN + amount) on another FAC report for this EIN: "
                                    + ", ".join(dup_rep[r["x_report_id"]]) + "; one filing likely repeats the other.")
    stats["fac_reports_identical_sefa"] = len(dup_rep)


def stage_slfrf(ctx: Ctx, rows: list, stats: dict):
    import openpyxl  # noqa: PLC0415
    p = latest_raw("treasury", "SLFRF-Subaward-USASpending-File.xlsx")
    if not p:
        stats["slfrf"] = "no raw file"
        return
    wb = openpyxl.load_workbook(p, read_only=True)
    sheet = next(n for n in wb.sheetnames if n.startswith("SLFRF Subawards"))
    it = wb[sheet].iter_rows(values_only=True)
    hdr = next(it)
    ix = {h: i for i, h in enumerate(hdr)}
    retrieved = today()
    n = 0
    seen: dict = {}
    for v in it:
        r = {h: v[i] for h, i in ix.items()}
        if r["prime_awardee_state_code"] != "DC":
            continue
        n += 1
        d = str(r.get("subaward_action_date") or "")[:10]
        aln, title = cfda_split(r.get("prime_award_cfda_numbers_and_titles"))
        ein, meth, cand = ctx.resolve(r.get("subawardee_uei"), r.get("subawardee_name"), r.get("subawardee_state_code"))
        st = str(r.get("subaward_type") or "").lower()
        ck = (r.get("subaward_number"), d, to_int(r.get("subaward_amount")), norm_name(r.get("subawardee_name")))
        mod = str(r.get("subaward_fsrs_report_last_modified_date") or "")
        if ck in seen:
            prev = seen[ck]
            prev["x_n_reports_collapsed"] += 1
            if mod <= prev["_mod"]:
                continue
            rows.remove(prev)
        rid = f"slfrf_{r.get('subaward_fsrs_report_id')}_{r.get('subaward_number')}"
        rows.append({
            "award_row_id": rid, "recipient_ein": ein, "recipient_uei": r.get("subawardee_uei") or "",
            "recipient_name_raw": r.get("subawardee_name"),
            "awarding_agency": r.get("prime_award_awarding_agency_name"), "funding_agency": r.get("prime_award_funding_agency_name"),
            "program_name": title, "assistance_listing": aln, "award_id": r.get("subaward_number"),
            "award_type": "grant" if st.startswith(("grant", "sub-grant")) else ("contract" if st.startswith(("contract", "sub-contract")) else "other"),
            "flow_type": "subaward", "pass_through_entity": r.get("prime_awardee_name"), "pass_through_ein": "",
            "fiscal_year": to_int(r.get("subaward_action_date_fiscal_year")) or fy_of(d), "fiscal_year_basis": "federal_fy",
            "amount": to_int(r.get("subaward_amount")), "amount_type": "award_amount",
            "source_type": "treasury_slfrf", "source_id": "bulk_treasury_slfrf",
            "source_page": f"{rel(p)}#{sheet}", "conflict_flag": 0, "retrieved_date": retrieved,
            "confidence": "high", "basis": "documented",
            "x_recipient_state": r.get("subawardee_state_code"), "x_recipient_city": r.get("subawardee_city_name"),
            "x_recipient_business_types": r.get("subawardee_business_types"),
            "x_recipient_name_norm": norm_name(r.get("subawardee_name")), "x_ein_method": meth, "x_ein_name_match": cand,
            **ctx.scope_cols(ein, cand),
            "x_action_date": d, "x_def_codes": r.get("prime_award_disaster_emergency_fund_codes"),
            "x_prime_award_unique_key": r.get("prime_award_unique_key"), "x_prime_award_id": r.get("prime_award_fain"),
            "x_prime_awardee_uei": r.get("prime_awardee_uei"), "x_pass_through_is_dc_gov": 1,
            "x_description": str(r.get("subaward_description") or "")[:300].strip('"'),
            "x_raw_file": rel(p), "x_n_reports_collapsed": (seen[ck]["x_n_reports_collapsed"] if ck in seen else 1),
            "_mod": mod,
        })
        seen[ck] = rows[-1]
    wb.close()
    stats["slfrf_dc_report_rows"] = n
    stats["slfrf_dc_rows"] = len(seen)


def money(x) -> str:
    return f"${x:,.0f}"


def stage():
    ctx = Ctx()
    rows: list[dict] = []
    stats: dict = {}
    stage_usaspending(ctx, rows, stats)
    stage_fac(ctx, rows, stats)
    stage_slfrf(ctx, rows, stats)
    for r in rows:
        r["recipient_ein"] = norm_ein(r.get("recipient_ein")) or ""
        if r.get("x_ein_method") in ("calvary_identity", "named_identity"):
            r["confidence"] = "medium"    # amount documented; EIN link by exact name + state (name-only record)
    # duplicate check
    ids = Counter(r["award_row_id"] for r in rows)
    dups = {k: v for k, v in ids.items() if v > 1}
    out = INTERIM / "stage_fact_gov_awards__federal.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in FIELDS})
    missing = sum(1 for r in rows if not all(r.get(k) for k in ("source_id", "retrieved_date", "confidence", "basis")))

    # Calvary reconciliation
    cal = [r for r in rows if r["recipient_ein"] == CALVARY_EIN]
    fac22 = sum(r["amount"] or 0 for r in cal if r["source_type"] == "fac_sefa" and r["x_audit_year"] == "2022")
    fac23 = sum(r["amount"] or 0 for r in cal if r["source_type"] == "fac_sefa" and r["x_audit_year"] == "2023")
    hud = [r["amount"] for r in cal if r["source_type"] == "usaspending" and r["assistance_listing"] == "14.251"]
    ppp = [r["amount"] for r in cal if r["source_type"] == "usaspending" and r["assistance_listing"] == "59.073"]
    usa_sub = [(r["assistance_listing"], r["amount"]) for r in cal if r["source_type"] == "usaspending" and r["flow_type"] == "subaward"]
    sl = sorted(r["amount"] for r in cal if r["source_type"] == "treasury_slfrf")
    named_summary = {}
    for ein in NAMED:
        nr = [r for r in rows if r["recipient_ein"] == ein]
        named_summary[ein] = {
            "rows": len(nr), "by_source_flow": dict(Counter(f"{r['source_type']}/{r['flow_type']}" for r in nr)),
            "fac_audit_years": sorted({r["x_audit_year"] for r in nr if r["source_type"] == "fac_sefa"}),
            "fac_expenditure_by_fy": {str(fy): sum(r["amount"] or 0 for r in nr
                                                   if r["source_type"] == "fac_sefa" and r["fiscal_year"] == fy)
                                      for fy in sorted({r["fiscal_year"] for r in nr if r["source_type"] == "fac_sefa"})},
            "usaspending_amount": sum(r["amount"] or 0 for r in nr if r["source_type"] == "usaspending")}
    stats["named_comparators"] = named_summary
    recon = {"fac_fy22_total": fac22, "fac_fy22_ok": fac22 == 4067718, "fac_ay2023_total": fac23,
             "fac_ay2023_conflict_rows": sum(1 for r in cal if r["conflict_flag"] == 1),
             "hud_14251": hud, "hud_ok": hud == [200000], "ppp": ppp, "usaspending_subawards": usa_sub,
             "slfrf": sl, "slfrf_ok": sl == [113488, 3680675], "calvary_rows": len(cal)}

    # coverage
    core = ctx.core
    by_src = defaultdict(set)
    by_src_name = defaultdict(set)
    for r in rows:
        if r["recipient_ein"] in core:
            by_src[r["source_type"]].add(r["recipient_ein"])
        if r.get("x_ein_name_match") in core and not r["recipient_ein"]:
            by_src_name[r["source_type"]].add(r["x_ein_name_match"])
    any_ein = set().union(*by_src.values()) if by_src else set()
    any_name = set().union(*by_src_name.values()) - any_ein if by_src_name else set()
    cov = {"scope_orgs": len(core), "orgs_with_any_row_by_ein": len(any_ein),
           "by_source": {k: len(v) for k, v in by_src.items()},
           "extra_orgs_by_exact_name_state_candidate_only": len(any_name)}
    stats.update(rows=len(rows), duplicate_ids=len(dups), rows_missing_provenance=missing,
                 by_source_flow=dict(Counter(f"{r['source_type']}/{r['flow_type']}" for r in rows)),
                 ein_filled=sum(1 for r in rows if r["recipient_ein"]))
    log("33_pull_usaspending: stage fact_gov_awards",
        f"- {rel(out)}: {len(rows)} rows; {json.dumps(stats)}\n- Calvary reconciliation: {json.dumps(recon)}\n"
        f"- EIN coverage (scope = calvary, core_peers, dc_sector, dmv_sector): {json.dumps(cov)}")
    notes(rows, ctx)
    print(json.dumps({"stats": stats, "calvary": recon, "coverage": cov, "dups": list(dups)[:5]}, indent=1, default=str))


def notes(rows: list[dict], ctx: Ctx):
    """Short observations for notes_for_analysis.md."""
    dcs = {e for e, u in ctx.uni.items() if "dc_sector" in u.split(";")}
    yrs = range(2019, 2025)
    fac_pt = defaultdict(int)
    fac_pt_dc = defaultdict(int)
    fac_pt_tcp = defaultdict(int)
    usa_sub_dc = defaultdict(int)
    slfrf_dc = defaultdict(int)
    slfrf_dc_name = defaultdict(int)
    fac_by_aln = Counter()
    fac_by_aln_t = Counter()
    fac_titles = {}
    usa_by_aln = Counter()
    fac_orgs = set()
    for r in rows:
        e, fy, a = r["recipient_ein"], r.get("fiscal_year"), r.get("amount") or 0
        if r["source_type"] == "fac_sefa" and e in dcs and r["conflict_flag"] == 0:
            fac_orgs.add(e)
            if fy in yrs and (r.get("x_is_loan") or "").upper() != "Y":
                fac_by_aln[r["assistance_listing"]] += a
                if r["assistance_listing"] in CFDAS:
                    fac_by_aln_t[r["assistance_listing"]] += a
                fac_titles.setdefault(r["assistance_listing"], Counter())[r["program_name"]] += 1
            if r["flow_type"] == "pass_through_expenditure" and fy in yrs:
                fac_pt[fy] += a
                if r.get("x_pass_through_is_dc_gov") == 1:
                    fac_pt_dc[fy] += a
                elif TCP_RE.search(r.get("pass_through_entity") or ""):
                    fac_pt_tcp[fy] += a
        if r["source_type"] == "usaspending" and r["flow_type"] == "subaward" and e in dcs and r.get("x_pass_through_is_dc_gov") == 1 and fy in yrs:
            usa_sub_dc[fy] += a
        if r["source_type"] == "usaspending" and r["flow_type"] == "prime" and e in dcs and fy in yrs:
            usa_by_aln[r["assistance_listing"]] += a
        if r["source_type"] == "treasury_slfrf":
            if e in dcs:
                slfrf_dc[fy] += a
            elif r.get("x_ein_name_match") in dcs:
                slfrf_dc_name[fy] += a
    yl = lambda d: ", ".join(f"FY{y} {money(d.get(y, 0))}" for y in yrs)  # noqa: E731
    fac_titles = {k: c.most_common(1)[0][0] or "" for k, c in fac_titles.items()}   # FAC names are free text
    top_fac = "; ".join(f"{k} {fac_titles.get(k, '')[:45]} {money(v)}" for k, v in fac_by_aln.most_common(8))
    top_fac_t = "; ".join(f"{k} {fac_titles.get(k, '')[:45]} {money(v)}" for k, v in fac_by_aln_t.most_common(8))
    ratio = sum(usa_sub_dc.values()) / max(sum(fac_pt_dc.values()), 1)
    top_usa = "; ".join(f"{k} {money(v)}" for k, v in usa_by_aln.most_common(6))
    txt = (
        f"- **DC pass-through to dc_sector orgs, FAC vs USAspending (org FY / federal FY 2019-2024).** "
        f"FAC SEFA pass-through expenditure by {len(fac_orgs)} dc_sector auditees: {yl(fac_pt)}. Of this, lines whose "
        f"pass-through name reads as DC government: {yl(fac_pt_dc)}; via The Community Partnership: {yl(fac_pt_tcp)}. "
        f"USAspending subawards from DC-government primes to EIN-matched dc_sector orgs: {yl(usa_sub_dc)}. "
        f"Over FY2019-2024 the USAspending figure is {ratio:.0%} of the FAC DC-government pass-through figure "
        f"(different measures: subaward obligations vs SEFA expenditures; same org set only where UEIs map).\n"
        f"- Treasury SLFRF DC subawards (as of 2023-06-30) to dc_sector orgs, UEI/identity-matched: {yl(slfrf_dc)}; "
        f"additional exact-name candidates: {yl(slfrf_dc_name)}. The SLFRF file has almost no subawardee UEIs, so EIN "
        f"matching there depends on name resolution in Phase 5.\n"
        f"- **Largest federal programs for dc_sector orgs, FAC expenditure FY2019-2024 (direct + pass-through, "
        f"loan balances excluded):** {top_fac}. dc_sector includes DC-based international and research nonprofits, "
        f"which dominate this list.\n"
        f"- Same, limited to the 24 target ALNs: {top_fac_t}.\n"
        f"- Largest ALNs by USAspending prime obligations to EIN-matched dc_sector orgs (award base FY2019-2024): {top_usa}.\n"
        f"- FAC audit_year = the calendar year in which the auditee's fiscal year ENDS (checked on every DC/MD/VA "
        f"report with a non-calendar FY; see build log). Staged fiscal_year = year(fy_end_date), fiscal_year_basis=org_fy.\n"
        f"- Calvary FAC audit_year 2023 (FYE 2023-09-30) repeats the FY22 SEFA lines ($4,064,718 vs FY22 $4,067,718); "
        f"the FY23 audit PDF SEFA is $937,999. FAC rows kept with conflict_flag=1, confidence=low.\n"
        f"- USAspending prime rows carry total obligations to date for awards active in FY2019-FY2026; fiscal_year is the "
        f"award's base-action FY, so multi-year awards are not split by year (outlays in x_total_outlayed_amount).")
    for ein, d in NAMED.items():
        nr = [r for r in rows if r["recipient_ein"] == ein]
        fac = defaultdict(int)
        alns = Counter()
        for r in nr:
            if r["source_type"] == "fac_sefa":
                fac[r["fiscal_year"]] += r["amount"] or 0
                alns[r["assistance_listing"]] += r["amount"] or 0
        usa_p = sum(r["amount"] or 0 for r in nr if r["source_type"] == "usaspending" and r["flow_type"] == "prime")
        usa_s = sum(r["amount"] or 0 for r in nr if r["source_type"] == "usaspending" and r["flow_type"] == "subaward")
        pt = sum(r["amount"] or 0 for r in nr if r["flow_type"] == "pass_through_expenditure")
        tot = sum(fac.values())
        txt += (f"\n- **Named comparator {d['label']} (EIN {ein}):** {len(nr)} federal rows. FAC SEFA expenditure by "
                f"org FY: " + (", ".join(f"FY{y} {money(v)}" for y, v in sorted(fac.items())) or "none")
                + (f" ({pt / tot:.0%} pass-through)" if tot else "")
                + f"; top ALNs {', '.join(f'{k} {money(v)}' for k, v in alns.most_common(4)) or 'none'}. "
                f"USAspending FY2019-FY2026: prime obligations {money(usa_p)}, subawards {money(usa_s)}.")
    notes_p = ROOT / "notes_for_analysis.md"
    if notes_p.exists() and "\n## Federal pulls\n" in notes_p.read_text(encoding="utf-8"):
        log("33_pull_usaspending: notes", "- 'Federal pulls' section already in notes_for_analysis.md; not re-appended")
        return
    append_md("notes_for_analysis.md", "Federal pulls", txt)


def main():
    global REFRESH, NO_COUNT
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="usaspending,slfrf,stage")
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--ipv", choices=["4", "6", "any"], default="any")
    ap.add_argument("--no-count", action="store_true")
    a = ap.parse_args()
    REFRESH = a.refresh
    NO_COUNT = a.no_count
    set_ip_family(a.ipv)
    secs = a.only.split(",")
    if "usaspending" in secs:
        usaspending()
    if "slfrf" in secs:
        slfrf()
    if "stage" in secs:
        stage()


if __name__ == "__main__":
    main()
