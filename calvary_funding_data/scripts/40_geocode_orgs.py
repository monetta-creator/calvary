"""Phase 4 staging, area "context": geocode organization addresses -> county, tract, ward, lat/lon.

Scope: every EIN in universes calvary, core_peers, dc_sector, dmv_sector, dmv_funders, daf_sponsors
(clean/dim_universe_membership.csv). EINs only in the national universes keep the ZIP->county
assignment from interim/org_base.csv and are written with x_in_scope=False.

Address choice (organization addresses only, as filed):
  1. interim/core_peer_candidates.csv xml_street/xml_zip (990 filer address) when present, unless it is
     a PO box and the BMF street is not. BMF STREET is often a mailing address.
  2. otherwise BMF STREET/CITY/STATE/zip5 from interim/org_base.csv.
  Cleaning before geocoding: leading "C/O ..."/"CO ..."/"ATTN ..." text dropped, unit designators (STE,
  SUITE, UNIT, APT, RM, FL, #...), a bare unit number after the street type, and trailing "BOX nnn"
  dropped. Addresses that start with PO BOX / BOX / RR / DRAWER / GENERAL DELIVERY (or are a PO box
  with no house-number street) are not geocoded. MAR queries also drop "1/2" fractions (MAR returns
  HTTP 400 on an encoded "/").

Methods, in order:
  DC         MAR 2 (datagate.dc.gov/mar/open/api/v2.2/locations/{address}) -> ward, tract, lat/lon, MAR id.
             Accept the top candidate if _Score >= 90, or _Score >= 70 with the same house number and ZIP.
             MAR misses fall through to the Census batch below.
  non-DC     Census Geocoder batch (/geographies/addressbatch, benchmark Public_AR_Current, vintage
  (+ DC      Census2020_Current, <= CHUNK rows per request) -> county, tract, block, lat/lon. DC matches get
   misses)   the ward from the block via the 2022 SLDU BEF. No_Match/Tie rows are retried once with the
             ZIP dropped (city + state only; BMF ZIPs are often PO-box ZIPs) and street aliases applied
             (MARION BARRY AVE -> GOOD HOPE RD).
  fallback   PO boxes and failed matches keep org_base county_fips with geo_method zcta_primary_county or
             city_modal_county (DC rows, which org_base labels state_dc, are relabelled by their ZIP's
             2020 ZCTA primary county, else city_modal_county); no county -> unresolved.

Raw: raw/mar2/geocode40/{stamp}_{ein}_{addrhash}.json (one per MAR call),
     raw/census_geocoder/{stamp}_batch_{hash}_{request|response}.csv.
Responses are reused on rerun when the same address/batch was already saved (pass --refresh to call again).
Census rows are reused one by one: a job whose exact (id, street, city, state, zip5) appears in any saved
request/response pair is taken from that response, so new scope EINs are the only rows sent.
Keys: DC_MAR_API_KEY (environment only).

Writes interim/stage_org_geo__context.csv; build-log section "40_geocode_orgs"; notes and questions via append_md.
Usage: .venv/bin/python scripts/40_geocode_orgs.py [--refresh] [--chunk 2500] [--no-notes]
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import quote

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import (CLEAN, INTERIM, RAW, RateLimiter, append_md, env_key, latest_raw, log, norm_ein, rel,
                        save_raw, session, today)

SCOPE = ["calvary", "core_peers", "named_comparators", "dc_sector", "dmv_sector", "dmv_funders", "daf_sponsors"]
MAR = "https://datagate.dc.gov/mar/open/api/v2.2/locations/{addr}"
GEOCODER = "https://geocoding.geo.census.gov/geocoder/geographies/addressbatch"
OUT = INTERIM / "stage_org_geo__context.csv"
MAR_DIR = "mar2/geocode40"
LOG = "40_geocode_orgs"
CALVARY = "521307706"
CALVARY_TRACT = "11001007503"

POBOX = re.compile(r"^\s*(P\s*\.?\s*O\s*\.?\s*(BOX|B\b|DRAWER)|POST\s+OFFICE\s+BOX|POB\b|BOX\s*\d|DRAWER\b|"
                   r"RR\s*\d|R\s*R\s+\d|RURAL\s+ROUTE|HC\s*\d|GENERAL\s+DELIVERY)", re.I)
LEAD_CO = re.compile(r"^\s*(C/O|C\\O|CO/|C O\b|CO\b|%|ATTN:?|ATTENTION:?)\s*[^0-9]*", re.I)
TRAIL_NO = re.compile(r"(\b(?:ST|STREET|AVE|AVENUE|RD|ROAD|DR|DRIVE|BLVD|BOULEVARD|PKWY|PARKWAY|PIKE|WAY|LN|LANE|CT|"
                      r"COURT|PL|PLACE|CIR|CIRCLE|TER|TERRACE|TPKE|TURNPIKE|SQ|SQUARE|PLZ|PLAZA|CTR|CENTER)"
                      r"(?:\s+(?:NW|NE|SW|SE|N|S|E|W))?)\s+[A-Z]?\d+[A-Z]?$", re.I)
FRACTION = re.compile(r"\s+\d+/\d+\b")
UNIT = [re.compile(p, re.I) for p in (
    r"\s+(P\s*\.?\s*O\s*\.?\s*)?BOX\s+\d+\b.*$",
    r"\s+\d+(ST|ND|RD|TH)\s+(FL|FLR|FLOOR)\b.*$",
    r"\s+(STE|SUITE|UNIT|APT|RM|ROOM|FL|FLR|FLOOR|BLDG|PMB|LBBY|LOBBY|OFC|OFFICE)\b\.?.*$",
    r"\s*#.*$",
    r"\s*,.*$",
)]
ALIASES = [(re.compile(r"\bMARION BARRY (AVE|AVENUE)\b", re.I), "GOOD HOPE RD")]
DC_ZIP3 = ("200", "202", "203", "204", "205")


# ---------------------------------------------------------------- addresses
def is_pobox(s: str) -> bool:
    return bool(POBOX.match(s or ""))


def clean_street(s: str) -> str:
    s = re.sub(r"\s+", " ", str(s or "")).strip()
    s2 = LEAD_CO.sub("", s).strip()
    if re.match(r"^\d", s2):
        s = s2
    for p in UNIT:
        t = p.sub("", s).strip()
        if re.match(r"^\d+\S*\s+\S+", t):   # keep the cut only if a house number + street remains
            s = t
    t = TRAIL_NO.sub(r"\1", s).strip()   # bare unit number after the street type, e.g. "671 N GLEBE RD 610"
    if re.match(r"^\d+\S*\s+\S+", t) and not re.search(r"\b(COUNTY|STATE)\s+(ROAD|RD)\s+\d+$", s, re.I):
        s = t
    return s


def state_from_zip(z: str, default: str) -> str:
    if not z:
        return default
    if z[:3] in DC_ZIP3:
        return "DC"
    if "206" <= z[:3] <= "219":
        return "MD"
    if "220" <= z[:3] <= "246":
        return "VA"
    return default


def load_inputs():
    org = pd.read_csv(INTERIM / "org_base.csv", dtype=str, keep_default_na=False)
    org["ein"] = org.ein.map(norm_ein)
    um = pd.read_csv(CLEAN / "dim_universe_membership.csv", dtype=str, keep_default_na=False)
    um["ein"] = um.ein.map(norm_ein)
    univ = um.groupby("ein").universe.agg(lambda s: ";".join(sorted(set(s))))
    scope = set(um[um.universe.isin(SCOPE)].ein)
    cp = pd.read_csv(INTERIM / "core_peer_candidates.csv", dtype=str, keep_default_na=False)
    cp["ein"] = cp.ein.map(norm_ein)
    cp = cp[cp.xml_street.str.strip() != ""].drop_duplicates("ein").set_index("ein")
    org["x_universes"] = org.ein.map(univ).fillna("")
    org["x_in_scope"] = org.ein.isin(scope)
    missing = scope - set(org.ein)
    return org, cp, missing


def choose_address(r, cp) -> dict:
    bmf_street = r.STREET.strip()
    a = {"street_raw": bmf_street, "city": r.CITY.strip(), "state": r.STATE.strip(), "zip5": r.zip5.strip(),
         "address_source": "irs_eo_bmf" if bmf_street else "none"}
    if r.ein in cp.index:
        x = cp.loc[r.ein]
        xs = x.xml_street.strip()
        if xs and not (is_pobox(xs) and bmf_street and not is_pobox(bmf_street)):
            xz = (x.xml_zip or "").strip()[:5]
            same_zip = not xz or xz == a["zip5"]
            a = {"street_raw": xs, "city": a["city"] if same_zip else "",
                 "state": a["state"] if same_zip else state_from_zip(xz, a["state"]),
                 "zip5": xz or a["zip5"], "address_source": "irs_990_xml_filer"}
    cleaned = clean_street(a["street_raw"]) if a["street_raw"] else ""
    # PO box first, or a PO box with no house-number street in front of it (e.g. "BOTANY DEPT MRC 166 PO BOX 370")
    a["pobox"] = is_pobox(a["street_raw"]) or bool(
        re.search(r"\bP\s*\.?\s*O\s*\.?\s*BOX\b", a["street_raw"], re.I) and not re.match(r"^\d", cleaned))
    a["street_used"] = cleaned if not a["pobox"] else ""
    return a


def addr_hash(*parts) -> str:
    return hashlib.sha1("|".join(p or "" for p in parts).upper().encode()).hexdigest()[:10]


# ---------------------------------------------------------------- MAR 2
def mar_cache() -> dict[str, Path]:
    d = RAW / MAR_DIR
    out = {}
    if d.exists():
        for p in sorted(d.glob("*.json")):
            out[p.stem.split("_", 1)[1]] = p   # "{ein}_{hash}" -> newest file
    return out


def house_no(s: str) -> str:
    m = re.match(r"^\s*(\d+)", s or "")
    return m.group(1) if m else ""


def parse_mar(j: dict, street: str, zip5: str) -> dict | None:
    res = (j or {}).get("Result") or {}
    cands = []
    for x in (res.get("addresses") or []):
        p = (x.get("address") or {}).get("properties") or {}
        if p:
            cands.append(p)
    if not cands:
        return {"ok": False, "why": "no_result"}
    p = max(cands, key=lambda q: q.get("_Score") or 0)
    score = float(p.get("_Score") or 0)
    same_no = house_no(street) and house_no(street) == str(p.get("AddrNum") or "")
    same_zip = zip5 and zip5 == str(p.get("Zipcode") or "")
    ok = score >= 90 or (score >= 70 and same_no and same_zip)
    w = re.search(r"(\d)", str(p.get("Ward") or ""))
    tr = str(p.get("CensusTract") or "").strip()
    return {"ok": ok, "why": "" if ok else f"low_score_{score:g}", "score": score,
            "mar_id": str(p.get("MarId") or ""), "lat": p.get("Latitude"), "lon": p.get("Longitude"),
            "ward": int(w.group(1)) if w else None, "tract": ("11001" + tr.zfill(6)) if tr else None,
            "matched": p.get("FullAddress"), "zip_match": bool(same_zip), "n_cands": len(cands)}


def run_mar(jobs: list[dict], refresh: bool) -> tuple[dict, dict]:
    key = env_key("DC_MAR_API_KEY")
    if not key:
        raise SystemExit("DC_MAR_API_KEY not set; source ~/.config/calvary/keys.env")
    cache = {} if refresh else mar_cache()
    s = session(retries=3)
    rl = RateLimiter(4.0)   # <= 5 req/s requested by the task; stay under it
    out, stats = {}, {"calls": 0, "reused": 0, "http_errors": 0}
    lock = threading.Lock()

    def one(job):
        q = FRACTION.sub("", job["street_used"])   # MAR rejects an encoded "/" (HTTP 400), e.g. "2728 1/2 ..."
        tag = f"{job['ein']}_{addr_hash(q, 'DC')}"
        p = cache.get(tag)
        if p is not None:
            raw, date = p.read_bytes(), f"{p.name[:4]}-{p.name[4:6]}-{p.name[6:8]}"
            with lock:
                stats["reused"] += 1
        else:
            rl.wait()
            try:
                r = s.get(MAR.format(addr=quote(q, safe="")), params={"apikey": key}, timeout=60)
                raw = r.content
                if r.status_code != 200:
                    with lock:
                        stats["http_errors"] += 1
            except Exception as e:   # noqa: BLE001
                raw = json.dumps({"_error": type(e).__name__}).encode()
                with lock:
                    stats["http_errors"] += 1
            save_raw(MAR_DIR, tag, raw, "json")
            date = today()
            with lock:
                stats["calls"] += 1
        try:
            j = json.loads(raw)
        except ValueError:
            j = {}
        m = parse_mar(j, job["street_used"], job["zip5"])
        m["date"] = date
        with lock:
            out[job["ein"]] = m

    with ThreadPoolExecutor(4) as ex:
        list(ex.map(one, jobs))
    return out, stats


# ---------------------------------------------------------------- Census batch
def census_row_cache() -> dict[tuple, tuple[list, str]]:
    """(id, street, city, state, zip5) -> (response row, retrieved date), from every saved request/response pair in
    raw/census_geocoder/. Lets a rerun reuse rows whose chunk changed (e.g. new scope EINs shift the chunking)."""
    cache = {}
    d = RAW / "census_geocoder"
    for req in sorted(d.glob("*_batch_*_request.csv")) if d.exists() else []:
        h = req.name.split("_batch_", 1)[1].split("_", 1)[0]
        resp = latest_raw("census_geocoder", f"batch_{h}_response.csv")
        if resp is None:
            continue
        date = f"{resp.name[:4]}-{resp.name[4:6]}-{resp.name[6:8]}"
        sent = {r[0]: tuple(r) for r in csv.reader(io.StringIO(req.read_text(encoding="utf-8"))) if r}
        for row in csv.reader(io.StringIO(resp.read_text(encoding="utf-8", errors="replace"))):
            if row and row[0] in sent:
                cache[sent[row[0]]] = (row, date)
    return cache


def census_batches(jobs: list[dict], chunk: int, refresh: bool, label: str) -> tuple[dict, dict]:
    """jobs: dicts with id, street, city, state, zip5. Returns {id: parsed} and stats.
    Unless refresh, a job whose exact (id, street, city, state, zip5) was sent before reuses that saved response
    row; only the remaining jobs are batched."""
    s = session(retries=3, backoff=5)
    out, stats = {}, {"batches": 0, "reused": 0, "rows": 0, "rows_reused": 0}
    rc = {} if refresh else census_row_cache()
    todo, cached_rows = [], []
    for j in jobs:
        k = (j["id"], j["street"], j["city"], j["state"], j["zip5"])
        if k in rc:
            cached_rows.append(rc[k])
        else:
            todo.append(j)
    stats["rows_reused"] = len(cached_rows)
    for row, date in cached_rows:
        out[row[0]] = parse_census_row(row, date)
        stats["rows"] += 1
    jobs = todo
    for i in range(0, len(jobs), chunk):
        part = jobs[i:i + chunk]
        buf = io.StringIO()
        w = csv.writer(buf, lineterminator="\n")
        for j in part:
            w.writerow([j["id"], j["street"], j["city"], j["state"], j["zip5"]])
        body = buf.getvalue().encode()
        h = hashlib.sha1(body).hexdigest()[:12]
        cached = None if refresh else latest_raw("census_geocoder", f"batch_{h}_response.csv")
        if cached is not None:
            text = cached.read_text(encoding="utf-8", errors="replace")
            date = f"{cached.name[:4]}-{cached.name[4:6]}-{cached.name[6:8]}"
            stats["reused"] += 1
        else:
            save_raw("census_geocoder", f"batch_{h}_request", body, "csv")
            r = s.post(GEOCODER, files={"addressFile": ("addresses.csv", body, "text/csv")},
                       data={"benchmark": "Public_AR_Current", "vintage": "Census2020_Current"}, timeout=1800)
            r.raise_for_status()
            save_raw("census_geocoder", f"batch_{h}_response", r.content, "csv")
            text, date = r.text, today()
            stats["batches"] += 1
            print(f"  census {label} batch {i // chunk + 1}: {len(part)} rows", flush=True)
        for row in csv.reader(io.StringIO(text)):
            if not row:
                continue
            out[row[0]] = parse_census_row(row, date)
            stats["rows"] += 1
    return out, stats


def parse_census_row(row: list, date: str) -> dict:
    rec = {"status": row[2] if len(row) > 2 else "", "date": date}
    if rec["status"] == "Match" and len(row) >= 12:
        lon, lat = (row[5].split(",") + [None, None])[:2]
        rec.update(type=row[3], matched=row[4], lon=float(lon), lat=float(lat), state=row[8],
                   county=row[8] + row[9], tract=row[8] + row[9] + row[10],
                   block=row[8] + row[9] + row[10] + row[11])
    return rec


def apply_alias(s: str) -> str:
    for p, rep in ALIASES:
        s = p.sub(rep, s)
    return s


# ---------------------------------------------------------------- reference data
def load_bef() -> dict[str, int]:
    p = latest_raw("census", "bef_sldu2022_11_DC.txt")
    with open(p, encoding="utf-8") as f:
        return {r["GEOID"]: int(r["SLDUST"]) for r in csv.DictReader(f)}


def load_polys():
    from shapely.geometry import shape
    from shapely.strtree import STRtree
    wj = json.loads(latest_raw("geo", "dcgis_wards_2022.geojson").read_text(encoding="utf-8"))
    tj = json.loads(latest_raw("geo", "tigerweb_acs2024_tracts_dc.geojson").read_text(encoding="utf-8"))
    wards = [(int(f["properties"]["WARD"]), shape(f["geometry"])) for f in wj["features"]]
    tracts = [(f["properties"]["GEOID"], shape(f["geometry"])) for f in tj["features"]]
    tree = STRtree([g for _, g in tracts])
    return wards, tracts, tree


def pip(lat, lon, wards, tracts, tree):
    from shapely.geometry import Point
    if lat is None or lon is None:
        return None, None
    pt = Point(float(lon), float(lat))
    w = next((k for k, g in wards if g.covers(pt)), None)
    t = None
    for i in tree.query(pt):
        if tracts[int(i)][1].covers(pt):
            t = tracts[int(i)][0]
            break
    return w, t


def dc_zip_primary() -> dict[str, str]:
    p = latest_raw("geo", "census_zcta520_county20.txt")
    z = pd.read_csv(p, sep="|", dtype=str, keep_default_na=False, encoding="utf-8-sig")
    z = z[z.GEOID_ZCTA5_20 != ""]
    z["land"] = pd.to_numeric(z.AREALAND_PART, errors="coerce")
    z = z.sort_values("land", ascending=False).drop_duplicates("GEOID_ZCTA5_20")
    return dict(zip(z.GEOID_ZCTA5_20, z.GEOID_COUNTY_20))


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true", help="call the APIs again instead of reusing raw responses")
    ap.add_argument("--chunk", type=int, default=2500, help="rows per Census batch request (max 10000)")
    ap.add_argument("--no-notes", action="store_true", help="skip build-log, notes and questions appends")
    a = ap.parse_args()
    chunk = min(a.chunk, 10000)

    org, cp, missing = load_inputs()
    addrs = {r.ein: choose_address(r, cp) for r in org.itertuples(index=False)}
    sc = org[org.x_in_scope]

    # ---- MAR 2 for DC street addresses
    dc_jobs = [{"ein": e, **addrs[e]} for e in sc.ein
               if addrs[e]["state"] == "DC" and addrs[e]["street_used"]]
    print(f"MAR 2: {len(dc_jobs)} DC addresses", flush=True)
    mar, mar_stats = run_mar(dc_jobs, a.refresh)

    # ---- Census batch: non-DC street addresses + DC MAR misses
    cen_jobs = []
    for e in sc.ein:
        ad = addrs[e]
        if not ad["street_used"]:
            continue
        if ad["state"] == "DC" and mar.get(e, {}).get("ok"):
            continue
        cen_jobs.append({"id": e, "street": ad["street_used"], "city": ad["city"], "state": ad["state"],
                         "zip5": ad["zip5"]})
    print(f"Census batch: {len(cen_jobs)} addresses", flush=True)
    cen, cen_stats = census_batches(cen_jobs, chunk, a.refresh, "pass1")
    retry = []
    for j in cen_jobs:
        if cen.get(j["id"], {}).get("status") != "Match":
            st = apply_alias(j["street"])
            # BMF ZIPs are often PO-box or mailing ZIPs: retry on city + state without the ZIP
            if j["city"] and (j["zip5"] or st != j["street"]):
                retry.append({**j, "street": st, "zip5": ""})
    print(f"Census retry: {len(retry)} addresses", flush=True)
    cen2, cen2_stats = census_batches(retry, chunk, a.refresh, "retry")
    retried_ok, retry_rejected = set(), 0
    orig_zip = {j["id"]: j["zip5"] for j in cen_jobs}
    bmf_cty = dict(zip(org.ein, org.county_fips))
    for k, v in cen2.items():
        if v.get("status") == "Match":
            # without the ZIP the geocoder can jump to a look-alike street elsewhere: keep the retry match only
            # if it lands in the original ZIP or in the org_base ZIP->county
            if v["matched"][-5:] != orig_zip.get(k) and v["county"] != bmf_cty.get(k):
                retry_rejected += 1
                continue
            cen[k] = {**v, "type": v.get("type", "") + "_retry"}
            retried_ok.add(k)
    retry_street = {j["id"]: j["street"] for j in retry}

    # ---- assemble
    bef = load_bef()
    wards, tracts, tree = load_polys()
    zprim = dc_zip_primary()
    dc_tracts = {t for t, _ in tracts}
    rows = []
    pip_ward_diff = pip_tract_diff = mar_tract_fix = 0
    for r in org.itertuples(index=False):
        e = r.ein
        ad = addrs[e]
        row = {"ein": e, "street_used": ad["street_used"] if r.x_in_scope else "",
               "address_source": ad["address_source"] if r.x_in_scope else "not_geocoded_out_of_scope",
               "county_fips": None, "ward": None, "tract_geoid": None, "lat": None, "lon": None,
               "geo_method": None, "match_quality": None, "source_id": None, "retrieved_date": None,
               "confidence": None, "basis": "derived", "x_in_scope": bool(r.x_in_scope),
               "x_universes": r.x_universes, "x_state": ad["state"], "x_zip5": ad["zip5"],
               "x_pobox": ad["pobox"], "x_mar_id": None, "x_match_score": None, "x_matched_address": None,
               "x_census_block_geoid": None, "x_bmf_county_fips": r.county_fips or None,
               "x_bmf_geo_method": r.geo_method or None, "x_fail_reason": None}
        m = mar.get(e) if r.x_in_scope else None
        c = cen.get(e) if r.x_in_scope else None
        if m and m.get("ok"):
            tract = m["tract"]
            pw, pt = pip(m["lat"], m["lon"], wards, tracts, tree)
            if tract not in dc_tracts and pt:
                tract, mar_tract_fix = pt, mar_tract_fix + 1
            pip_ward_diff += pw is not None and m["ward"] is not None and pw != m["ward"]
            pip_tract_diff += pt is not None and pt != tract
            row.update(county_fips="11001", ward=m["ward"] if m["ward"] is not None else pw, tract_geoid=tract,
                       lat=round(float(m["lat"]), 7), lon=round(float(m["lon"]), 7), geo_method="mar2",
                       match_quality="exact" if m["score"] >= 100 else "non_exact", source_id="api_dc_mar2",
                       retrieved_date=m["date"], confidence="high" if m["score"] >= 90 else "medium",
                       x_mar_id=m["mar_id"], x_match_score=m["score"], x_matched_address=m["matched"])
        elif c and c.get("status") == "Match":
            ward = bef.get(c["block"]) if c["state"] == "11" else None
            if e in retried_ok:
                row["street_used"] = retry_street[e]
            exact = c["type"].startswith("Exact")
            row.update(county_fips=c["county"], ward=ward, tract_geoid=c["tract"], lat=round(c["lat"], 7),
                       lon=round(c["lon"], 7), geo_method="census_geocoder",
                       match_quality=("exact" if exact else "non_exact") + ("_retry" if e in retried_ok else ""),
                       source_id="api_census_geocoder" + (";bulk_census_bef_sldu2022" if ward else ""),
                       retrieved_date=c["date"], confidence="high" if exact else "medium",
                       x_matched_address=c["matched"], x_census_block_geoid=c["block"])
        else:
            gm = r.geo_method
            cf = r.county_fips or None
            if gm == "state_dc":   # DC is one county; label by the ZIP's ZCTA primary county when it is DC
                gm = "zcta_primary_county" if zprim.get(ad["zip5"] or r.zip5) == "11001" else "city_modal_county"
            if gm not in ("zcta_primary_county", "city_modal_county") or not cf:
                gm, cf = "unresolved", None
            src = {"zcta_primary_county": "bulk_irs_eo_bmf;bulk_census_zcta_county_2020",
                   "city_modal_county": "bulk_irs_eo_bmf;bulk_census_zcta_county_2020",
                   "unresolved": "bulk_irs_eo_bmf"}[gm]
            why = ("out_of_scope" if not r.x_in_scope else "po_box" if ad["pobox"] else
                   "no_street" if not ad["street_used"] else
                   (m or {}).get("why") or (c or {}).get("status") or "not_attempted")
            if r.x_in_scope and m and not m.get("ok") and c:
                why = f"mar2_{m.get('why')};census_{c.get('status') or 'none'}"
            row.update(county_fips=cf, geo_method=gm,
                       match_quality={"zcta_primary_county": "zip_only", "city_modal_county": "city_only",
                                      "unresolved": "none"}[gm],
                       source_id=src, retrieved_date=today(), confidence="low", x_fail_reason=why)
        rows.append(row)
    df = pd.DataFrame(rows)
    df["ward"] = df.ward.astype("Int64")
    df.to_csv(OUT, index=False)

    # ---------------------------------------------------------------- QC + reporting
    s = df[df.x_in_scope]
    issues, lines = [], []
    dup = df.ein.duplicated().sum()
    if dup:
        issues.append(f"{dup} duplicate EIN rows")
    lines.append(f"- inputs: org_base {len(org):,} EINs; in scope {len(s):,} "
                 f"(universes {', '.join(SCOPE)}); scope EINs missing from org_base: {len(missing)}")
    lines.append(f"- address source (in scope): {s.address_source.value_counts().to_dict()}; "
                 f"PO box / mailing-only: {int(s.x_pobox.sum()):,}; no street: "
                 f"{int(((s.street_used == '') & ~s.x_pobox).sum())}")
    lines.append(f"- MAR 2: {len(dc_jobs):,} DC addresses, {mar_stats['calls']} calls, {mar_stats['reused']} reused, "
                 f"{mar_stats['http_errors']} HTTP errors; accepted {sum(v.get('ok', False) for v in mar.values()):,}")
    lines.append(f"- Census batch: pass 1 {len(cen_jobs):,} rows ({cen_stats['batches']} new batches, "
                 f"{cen_stats['reused']} reused, {cen_stats['rows_reused']:,} rows reused from earlier responses); "
                 f"retry {len(retry):,} rows (ZIP dropped; {cen2_stats['batches']} new batches, "
                 f"{cen2_stats['rows_reused']:,} rows reused), {len(retried_ok)} matched on "
                 f"retry, {retry_rejected} retry matches rejected (outside the original ZIP and county)")
    vc = s.geo_method.value_counts()
    lines.append("- match rates by method (in scope, n=%s): " % f"{len(s):,}" + "; ".join(
        f"{k} {v:,} ({v / len(s) * 100:.1f}%)" for k, v in vc.items()))
    for st, g in [("DC", s[s.x_state == "DC"]), ("MD", s[s.x_state == "MD"]), ("VA", s[s.x_state == "VA"]),
                  ("other", s[~s.x_state.isin(["DC", "MD", "VA"])])]:
        geo = g.geo_method.isin(["mar2", "census_geocoder"]).sum()
        att = (g.street_used != "").sum()
        lines.append(f"  - {st}: {len(g):,} orgs, {att:,} with a street address, {geo:,} point-geocoded "
                     f"({geo / max(len(g), 1) * 100:.1f}% of all, {geo / max(att, 1) * 100:.1f}% of street "
                     f"addresses); {g.geo_method.value_counts().to_dict()}")
    lines.append(f"- match_quality (in scope): {s.match_quality.value_counts().to_dict()}")
    cg = s[s.geo_method == "census_geocoder"]
    agree = (cg.county_fips == cg.x_bmf_county_fips).sum()
    lines.append(f"- Census-geocoded county vs org_base ZIP county: {agree:,}/{len(cg):,} agree "
                 f"({agree / max(len(cg), 1) * 100:.1f}%)")
    lines.append(f"- MAR 2 QC vs polygons: ward differs from 2022 ward polygon for {pip_ward_diff}, tract "
                 f"differs from TIGER tract polygon for {pip_tract_diff}; MAR tract replaced by polygon tract "
                 f"for {mar_tract_fix}")
    dcp = s[(s.county_fips == "11001")]
    lines.append(f"- DC orgs with a ward: {dcp.ward.notna().sum():,} of {len(dcp):,}; "
                 f"tract outside the 206 ACS tracts: {int((dcp.tract_geoid.notna() & ~dcp.tract_geoid.isin(dc_tracts)).sum())}")
    cal = df[df.ein == CALVARY]
    if cal.empty:
        issues.append("Calvary missing")
    else:
        cr = cal.iloc[0]
        lines.append(f"- Calvary {CALVARY}: {cr.geo_method}, ward {cr.ward}, tract {cr.tract_geoid}, "
                     f"MAR id {cr.x_mar_id}, lat {cr.lat}, lon {cr.lon}")
        if not (cr.ward == 8 and cr.tract_geoid == CALVARY_TRACT):
            issues.append(f"Calvary geocoded to ward {cr.ward} tract {cr.tract_geoid}")
    lines.append(f"- out of scope (national universes only): {len(df) - len(s):,} rows carried with the org_base "
                 f"ZIP->county ({df[~df.x_in_scope].geo_method.value_counts().to_dict()})")
    lines.append(f"- wrote {rel(OUT)} ({len(df):,} rows; duplicate EINs {dup})")
    lines.append("- **QC issues:** " + "; ".join(issues) if issues else "- QC: all checks passed")
    print("\n".join(lines))

    # analysis notes: dc_sector orgs by ward
    dcs = s[s.x_universes.str.contains(r"(?:^|;)dc_sector(?:;|$)")]
    wk = dcs[dcs.ward.notna()]
    wc = wk.ward.value_counts().sort_index()
    n78 = int(wc.get(7, 0) + wc.get(8, 0))
    res78 = "n/a"
    gp = INTERIM / "stage_dim_geo__context.csv"
    if gp.exists():
        g = pd.read_csv(gp, dtype={"ward": "Int64"})
        gw = g[g.geo_level == "ward"]
        res78 = f"{gw[gw.ward.isin([7, 8])].total_pop.sum() / gw.total_pop.sum() * 100:.1f}%"
    note = [
        f"- dc_sector orgs with a ward: {len(wk):,} of {len(dcs):,}. Wards 7+8 hold {n78} "
        f"({n78 / max(len(wk), 1) * 100:.1f}%; Ward 7 {int(wc.get(7, 0))}, Ward 8 {int(wc.get(8, 0))}) vs "
        f"{res78} of DC residents (ACS 2020-2024). By ward: " + ", ".join(f"W{int(k)} {v}" for k, v in wc.items()) + ".",
        "- Org ward/tract reflects the filing address (BMF street or 990 filer address), which may be a "
        "headquarters or mailing address, not where services are delivered.",
        f"- Org geocode match rates (in scope n={len(s):,}): " + "; ".join(
            f"{k} {v / len(s) * 100:.1f}%" for k, v in vc.items()) + ". `county_fips` here is the 5-digit "
        "county GEOID (joins to dim_geo `x_county_geoid`).",
    ]
    if not a.no_notes:
        log(LOG, "\n".join(lines))
        append_md("notes_for_analysis.md", "Geo/context build", "\n".join(note))
        q = []
        if (s.geo_method == "unresolved").any():
            q.append(f"- {int((s.geo_method == 'unresolved').sum())} in-scope orgs have no county "
                     "(ZIP outside DMV ZCTAs and no street match). Leave them unresolved, or assign by hand?")
        q.append(f"- {int(s.x_pobox.sum()):,} in-scope orgs file only a PO box, so they have a county but no "
                 "tract or ward. Is ZIP-level county enough for these (mostly small foundations), or should "
                 "990 filer addresses be pulled for them too?")
        other_u = sorted({u for us in org.x_universes for u in us.split(";") if u} - set(SCOPE))
        q.append(f"- Universes outside the geocode scope keep ZIP->county only: {', '.join(other_u)} "
                 f"({len(df) - len(s):,} EINs not in any scoped universe). Should `calvary_known_funders` "
                 "(added to org_base after this task was scoped) be point-geocoded too?")
        append_md("open_questions.md", "Geo/context build", "\n".join(q))
    print("\n".join(note))
    if issues:
        sys.exit(1)


if __name__ == "__main__":
    main()
