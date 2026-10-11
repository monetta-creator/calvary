"""Phase 4 bulk pull: Federal Audit Clearinghouse (FAC) single-audit data for DC, MD and VA auditees.

Steps
  1. GET /general for auditee_state in (DC, MD, VA) x audit_year 2016-2025 (selected columns; no
     contact or address fields). One call per state-year, paged with limit/offset.
  2. Reports with is_multiple_eins / is_additional_ueis -> /additional_eins and /additional_ueis
     (batches of 100 report_ids) so multi-entity audits can be matched on a secondary EIN.
  3. Keep reports whose auditee_ein (or an additional EIN) is in the FAC EIN scope:
     universes calvary, core_peers, dc_sector, dmv_sector, named_comparators, dmv_funders
     (clean/dim_universe_membership.csv), plus Calvary (521307706) and the named comparators in NAMED_EINS
     (Downtown Women's Center, Los Angeles, 311597223). Calvary and named EINs are also queried by
     auditee_ein for ALL audit years, since they can fall outside the DC/MD/VA state filter.
  4. For kept reports: /federal_awards and /passthrough in batches of 100 report_ids.
  5. Write interim/uei_ein_map.csv: one row per (ein, uei, audit_year) from every DC/MD/VA general
     row with a UEI, plus additional_ueis rows. Extra columns: auditee_state, in_scope.
  6. Save a run manifest (raw/fac/{stamp}_pull34_manifest.json) listing every raw file by role.
     scripts/33_pull_usaspending.py reads it to stage FAC SEFA lines into fact_gov_awards.

Rate limit: the api.data.gov key allows 1,000 requests/hour. This script paces at 1 request per 3.7 s
(<= 973/hour) and pauses when x-ratelimit-remaining drops below 25.

Usage:
  [ -f ~/.config/calvary/keys.env ] && set -a && . ~/.config/calvary/keys.env && set +a
  .venv/bin/python scripts/34_pull_fac.py
Key (FAC_API_KEY) comes from the environment only and is never written.
"""
from __future__ import annotations

import csv
import json
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import (CLEAN, INTERIM, RateLimiter, env_key, log, norm_ein, register_source, rel,
                        save_raw, session, stamp, today)

FAC = "https://api.fac.gov"
STATES = ["DC", "MD", "VA"]
YEARS = list(range(2016, 2026))
CALVARY_EIN = "521307706"
SCOPE_UNIVERSES = ["calvary", "core_peers", "dc_sector", "dmv_sector", "named_comparators"]
# Named comparators requested by the lead (rule NC1 in dim_universe_membership); hard-coded so the pull
# works before the universe file carries them.
import csv as _csv
NAMED_EINS = {r["ein"]: r["name"] for r in _csv.DictReader(open(Path(__file__).resolve().parents[1] / "config" / "named_comparators.csv", encoding="utf-8"))}
FAC_EXTRA_UNIVERSES = ["dmv_funders"]
PAGE = 20000
BATCH = 100

GENERAL_COLS = ("report_id,audit_year,auditee_ein,auditee_uei,auditee_name,auditee_city,auditee_state,"
                "auditee_zip,entity_type,fy_start_date,fy_end_date,number_months,audit_period_covered,"
                "audit_type,total_amount_expended,dollar_threshold,fac_accepted_date,auditor_firm_name,"
                "is_low_risk_auditee,is_going_concern_included,is_material_noncompliance_disclosed,"
                "cognizant_agency,oversight_agency,data_source,resubmission_status,resubmission_version,"
                "is_multiple_eins,is_additional_ueis")

S = session()
RL_FAC = RateLimiter(1 / 3.7)
MANIFEST: list[dict] = []
H: dict = {}


def fget(desc: str, ep: str, params: dict, role: str) -> list | None:
    """GET one FAC page, save the body untouched, return the parsed list (or None)."""
    for attempt in range(4):
        RL_FAC.wait()
        try:
            r = S.get(f"{FAC}/{ep}", params=params, headers=H, timeout=180)
        except Exception as e:  # noqa: BLE001
            MANIFEST.append({"desc": desc, "role": role, "endpoint": ep, "params": params,
                             "status": f"error: {e.__class__.__name__}", "raw": None, "at": stamp()})
            time.sleep(10)
            continue
        p = save_raw("fac", desc, r.content, "json")
        rem = r.headers.get("x-ratelimit-remaining")
        MANIFEST.append({"desc": desc, "role": role, "endpoint": ep, "params": params,
                         "status": r.status_code, "raw": rel(p), "ratelimit_remaining": rem, "at": stamp()})
        if rem is not None and rem.isdigit() and int(rem) < 25:
            log("34_pull_fac: rate limit", f"- x-ratelimit-remaining={rem}; sleeping 15 min")
            time.sleep(900)
        if r.status_code == 429:
            time.sleep(600)
            continue
        if r.status_code != 200:
            return None
        try:
            j = r.json()
        except ValueError:
            return None
        return j if isinstance(j, list) else None
    return None


def fget_all(desc: str, ep: str, params: dict, role: str) -> list:
    rows, off = [], 0
    while True:
        j = fget(f"{desc}_o{off}" if off else desc, ep, dict(params, limit=PAGE, offset=off), role)
        if j is None:
            break
        rows += j
        if len(j) < PAGE:
            break
        off += PAGE
    return rows


def load_scope() -> tuple[dict, set]:
    """EIN -> ';'-joined universes for the FAC scope; and the 4-universe core scope set."""
    uni: dict[str, set] = {}
    with open(CLEAN / "dim_universe_membership.csv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["universe"] in SCOPE_UNIVERSES + FAC_EXTRA_UNIVERSES:
                e = norm_ein(r["ein"])
                if e:
                    uni.setdefault(e, set()).add(r["universe"])
    uni.setdefault(CALVARY_EIN, set()).add("calvary")
    for e in NAMED_EINS:
        uni.setdefault(e, set()).add("named_comparators")
    core = {e for e, u in uni.items() if u & set(SCOPE_UNIVERSES)}
    return {e: ";".join(sorted(u)) for e, u in uni.items()}, core


def batched(ids: list[str]):
    for i in range(0, len(ids), BATCH):
        yield i // BATCH, f"in.({','.join(ids[i:i + BATCH])})"


def main():
    key = env_key("FAC_API_KEY")
    if not key:
        log("34_pull_fac", "- FAC_API_KEY not set; nothing pulled")
        sys.exit("FAC_API_KEY not set")
    H["X-Api-Key"] = key
    scope, core = load_scope()

    # 1. general, per state-year
    gen: dict[str, dict] = {}
    per_sy = {}
    for st in STATES:
        for yr in YEARS:
            rows = fget_all(f"general_{st}_{yr}", "general",
                            {"auditee_state": f"eq.{st}", "audit_year": f"eq.{yr}", "select": GENERAL_COLS},
                            "general")
            per_sy[f"{st}_{yr}"] = len(rows)
            for g in rows:
                gen[g["report_id"]] = g
    # Calvary + named comparators by EIN, all audit years, regardless of state
    by_ein = {}
    for e, tag in [(CALVARY_EIN, "calvary")] + [(e, f"named_{e}") for e in NAMED_EINS]:
        rows = fget_all(f"general_{tag}_ein", "general", {"auditee_ein": f"eq.{e}", "select": GENERAL_COLS}, "general")
        by_ein[e] = sorted(g["audit_year"] for g in rows)
        for g in rows:
            gen[g["report_id"]] = g

    # 2. additional EINs / UEIs for multi-entity reports
    multi = sorted(r for r, g in gen.items() if str(g.get("is_multiple_eins")).lower() in ("true", "y", "yes"))
    addl_ueis_ids = sorted(r for r, g in gen.items() if str(g.get("is_additional_ueis")).lower() in ("true", "y", "yes"))
    add_eins: dict[str, set] = {}
    for b, chunk in batched(multi):
        for r in fget_all(f"additional_eins_b{b:03d}", "additional_eins", {"report_id": chunk}, "additional_eins"):
            e = norm_ein(r.get("additional_ein"))
            if e:
                add_eins.setdefault(r["report_id"], set()).add(e)
    add_ueis: list[dict] = []
    for b, chunk in batched(addl_ueis_ids):
        add_ueis += fget_all(f"additional_ueis_b{b:03d}", "additional_ueis", {"report_id": chunk}, "additional_ueis")

    # 3. keep in-scope reports
    kept = {}
    for rid, g in gen.items():
        e = norm_ein(g.get("auditee_ein"))
        if e in scope:
            kept[rid] = "auditee_ein"
        elif add_eins.get(rid, set()) & set(scope):
            kept[rid] = "additional_ein"
    kept_ids = sorted(kept)

    # 4. children for kept reports
    n_fa = n_pt = 0
    for b, chunk in batched(kept_ids):
        n_fa += len(fget_all(f"federal_awards_b{b:03d}", "federal_awards", {"report_id": chunk}, "federal_awards"))
        n_pt += len(fget_all(f"passthrough_b{b:03d}", "passthrough", {"report_id": chunk}, "passthrough"))

    # 5. uei_ein_map
    INTERIM.mkdir(parents=True, exist_ok=True)
    mp = {}
    for g in gen.values():
        e, u = norm_ein(g.get("auditee_ein")), (g.get("auditee_uei") or "").strip().upper()
        if e and u and u not in ("GSA_MIGRATION",) and len(u) == 12:
            mp[(e, u, g["audit_year"])] = {"ein": e, "uei": u, "auditee_name": g.get("auditee_name"),
                                           "audit_year": g["audit_year"], "source_id": "api_fac",
                                           "auditee_state": g.get("auditee_state"), "uei_role": "auditee_uei",
                                           "report_id": g["report_id"], "in_scope": int(e in core)}
    for a in add_ueis:
        g = gen.get(a["report_id"], {})
        e, u = norm_ein(g.get("auditee_ein")), (a.get("additional_uei") or "").strip().upper()
        if e and u and len(u) == 12 and (e, u, g.get("audit_year")) not in mp:
            mp[(e, u, g["audit_year"])] = {"ein": e, "uei": u, "auditee_name": g.get("auditee_name"),
                                           "audit_year": g["audit_year"], "source_id": "api_fac",
                                           "auditee_state": g.get("auditee_state"), "uei_role": "additional_uei",
                                           "report_id": a["report_id"], "in_scope": int(e in core)}
    fields = ["ein", "uei", "auditee_name", "audit_year", "source_id", "auditee_state", "uei_role",
              "report_id", "in_scope"]
    with open(INTERIM / "uei_ein_map.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(sorted(mp.values(), key=lambda r: (r["ein"], r["audit_year"], r["uei"])))

    # 6. manifest
    man = save_raw("fac", "pull34_manifest", {
        "script": "scripts/34_pull_fac.py", "run_date": today(), "states": STATES, "years": YEARS,
        "kept_reports": kept, "requests": MANIFEST}, "json")

    # audit_year semantics check: compare to FY start/end years
    sem = Counter()
    for g in gen.values():
        s, e, a = (g.get("fy_start_date") or "")[:4], (g.get("fy_end_date") or "")[:4], g.get("audit_year")
        if s and e and s != e:
            sem["noncal_audit_year=end" if a == e else ("noncal_audit_year=start" if a == s else "noncal_other")] += 1
        elif s and e:
            sem["calendar_or_same_year"] += 1
    ueis_core = {r["uei"] for r in mp.values() if r["in_scope"]}
    eins_core_kept = {norm_ein(gen[r]["auditee_ein"]) for r in kept_ids} & core
    register_source("api_fac", "Federal Audit Clearinghouse API", FAC,
                    "U.S. General Services Administration (GSA)",
                    "Public domain (U.S. government data); see https://www.fac.gov/api/terms/",
                    "PostgREST over the FAC dissemination tables; api.data.gov key (FAC_API_KEY), 1,000 req/hour. "
                    "Phase 4 pull (scripts/34_pull_fac.py): general for DC/MD/VA audit years 2016-2025; "
                    "federal_awards + passthrough for in-scope auditees.")
    log("34_pull_fac: FAC bulk pull",
        f"- general rows (DC/MD/VA, 2016-2025, + Calvary/named EINs all years; deduped by report_id): {len(gen)}; "
        f"per state-year: {json.dumps(per_sy)}\n- by-EIN audit years: {json.dumps(by_ein)}\n"
        f"- multi-EIN reports {len(multi)} (additional EINs on {len(add_eins)}); additional-UEI reports {len(addl_ueis_ids)} "
        f"({len(add_ueis)} rows)\n"
        f"- kept reports (FAC scope: calvary, core_peers, dc_sector, dmv_sector, named_comparators, dmv_funders): {len(kept_ids)} "
        f"({dict(Counter(kept.values()))}); core-scope EINs with a report: {len(eins_core_kept)}\n"
        f"- federal_awards rows {n_fa}; passthrough rows {n_pt}\n"
        f"- uei_ein_map rows {len(mp)} (in-scope UEIs {len(ueis_core)}) -> {rel(INTERIM / 'uei_ein_map.csv')}\n"
        f"- audit_year vs FY dates: {dict(sem)}\n- requests {len(MANIFEST)}; manifest {rel(man)}")
    print(json.dumps({"general": len(gen), "kept": len(kept_ids), "federal_awards": n_fa, "passthrough": n_pt,
                      "map": len(mp), "in_scope_ueis": len(ueis_core), "audit_year_semantics": dict(sem),
                      "by_ein_years": by_ein,
                      "requests": len(MANIFEST)}, indent=1))


if __name__ == "__main__":
    main()
