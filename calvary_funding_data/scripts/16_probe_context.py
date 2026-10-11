"""Phase 2 recon, area "context": geography, demographics, inflation.

Probes the context sources and pulls the small reference files later phases need:
  census  : ACS 5-year API (vintage check, keyless vs keyed, group pulls for DC tracts, DC wards,
            DMV counties, states, MSA, US), variables.json, ACS table-based Summary File (keyless
            fallback), 2020 PL 94-171 block counts for DC, 2022 SLDU block equivalency file (DC wards)
  geo     : DC 2022 ward polygons, TIGERweb ACS2024 tracts for DC, DC Office of Planning ACS ward
            profiles, DC Open Data search for an official tract-ward crosswalk, crosswalk validation
  geocode : DC MAR 2 API, DC GIS Address Points (MAR), Census Geocoder (single + batch)
  omb     : OMB July 2023 CBSA delineation file -> config/dmv_counties.csv
  cpi     : BLS CPI-U (US and Washington metro) annual averages -> config/cpi_u_annual.csv; FRED probe
  extra_geos : ACS group pulls for the out-of-DMV geographies in config/extra_geographies.csv only (named
            comparators' county and tract). "census" pulls them too; this step skips the other census probes.

Writes raw/census/, raw/geo/, raw/bls/, config/acs_variables.csv, config/dmv_counties.csv,
config/cpi_u_annual.csv, sources/catalog_parts/context.csv, source registry rows and build-log entries.

Static reference downloads are reused from raw/ when present; pass --refresh to download again.
Keys (environment only): CENSUS_API_KEY (ACS + PL), DC_MAR_API_KEY (MAR 2, optional),
BLS_API_KEY (optional; raises BLS limits).

Usage: .venv/bin/python scripts/16_probe_context.py [--refresh] [--sf-fallback] [--only census,geo,...]
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import (CONFIG, RAW, SOURCES, RateLimiter, env_key, log, register_source, rel,
                        save_raw, session, today)

PROBE_DATE = today()
S = session()
RL = RateLimiter(2.0)
RESULTS: dict[str, dict] = {}   # catalog key -> {"status", "note"}
SUMMARY: dict[str, list[str]] = defaultdict(list)   # log section -> lines

CENSUS = "https://api.census.gov/data"
SF_BASE = "https://www2.census.gov/programs-surveys/acs/summary_file/{y}/table-based-SF"
PL_URL = "https://api.census.gov/data/2020/dec/pl"
BEF_ZIP = ("https://www2.census.gov/programs-surveys/decennial/rdo/mapping-files/2023/"
           "2022-state-legislative-bef/sldu_2022.zip")
BEF_MEMBER = "11_DC_SLDU22.txt"
DCGIS = "https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA"
WARDS_LAYER = f"{DCGIS}/Administrative_Other_Boundaries_WebMercator/MapServer/53"
BLOCKS_LAYER = f"{DCGIS}/Demographic_WebMercator/MapServer/0"
ADDR_LAYER = f"{DCGIS}/Location_WebMercator/FeatureServer/0"
ACS_WARD_LAYERS = {"demographic_dp05": 39, "economic_dp03": 42, "housing_dp04": 45, "social_dp02": 48}
HUB_SEARCH = "https://opendata.dc.gov/api/search/v1/collections/dataset/items"
TIGER_TRACTS = "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_ACS2024/MapServer/8"
MAR2 = "https://datagate.dc.gov/mar/open/api/v2.2"
GEOCODER = "https://geocoding.geo.census.gov/geocoder"
OMB_XLSX = ("https://www2.census.gov/programs-surveys/metro-micro/geographies/reference-files/2023/"
            "delineation-files/list1_2023.xlsx")
BLS_V2 = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
FRED_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv"

ACS_GROUPS = ["B01003", "B03002", "B09019", "B11001", "B17001", "B17012", "B18101", "B19013",
              "B21001", "B23025", "B25070"]
STATE_ABBR = {"11": "DC", "24": "MD", "51": "VA", "54": "WV"}
CBSA = "47900"
BASE_YEAR = 2024
CPI_SERIES = {"CUUR0000SA0": "cpi_u_us", "CUURS35ASA0": "cpi_u_dc_metro",
              "CUUSS35ASA0": "cpi_u_dc_metro_semiannual"}

# Organization addresses used for geocoder tests (public org addresses only).
TEST_ADDRESSES = [
    ("calvary_new_name", "1217 Marion Barry Ave SE", "Washington", "DC", "20020"),
    ("calvary_old_name", "1217 Good Hope Rd SE", "Washington", "DC", "20020"),
    ("md_shepherds_table", "8106 Georgia Ave", "Silver Spring", "MD", "20910"),
    ("va_carpenters_shelter", "930 N Henry St", "Alexandria", "VA", "22314"),
]

# Short ACS variable list: variable -> use. Labels and concepts come from variables.json.
ACS_VARS = {
    "B01003_001E": "Total population; denominator and crosswalk check",
    "B17001_001E": "Poverty universe (pop. for whom poverty status is determined)",
    "B17001_002E": "Persons below poverty; poverty rate numerator",
    "B17001_017E": "Females below poverty (all ages)",
    "B17001_024E": "Women 18-24 below poverty",
    "B17001_025E": "Women 25-34 below poverty",
    "B17001_026E": "Women 35-44 below poverty",
    "B17001_027E": "Women 45-54 below poverty",
    "B17001_028E": "Women 55-64 below poverty",
    "B17001_029E": "Women 65-74 below poverty",
    "B17001_030E": "Women 75+ below poverty",
    "B17001_046E": "Females at or above poverty (all ages); female poverty-rate denominator with _017E",
    "B17001_053E": "Women 18-24 at/above poverty; adult female poverty-rate denominator",
    "B17001_054E": "Women 25-34 at/above poverty; adult female poverty-rate denominator",
    "B17001_055E": "Women 35-44 at/above poverty; adult female poverty-rate denominator",
    "B17001_056E": "Women 45-54 at/above poverty; adult female poverty-rate denominator",
    "B17001_057E": "Women 55-64 at/above poverty; adult female poverty-rate denominator",
    "B17001_058E": "Women 65-74 at/above poverty; adult female poverty-rate denominator",
    "B17001_059E": "Women 75+ at/above poverty; adult female poverty-rate denominator",
    "B25070_001E": "Renter households (rent-burden universe)",
    "B25070_007E": "Rent 30.0-34.9% of income (rent burdened)",
    "B25070_008E": "Rent 35.0-39.9% of income (rent burdened)",
    "B25070_009E": "Rent 40.0-49.9% of income (rent burdened)",
    "B25070_010E": "Rent 50%+ of income (severely rent burdened)",
    "B25070_011E": "Not computed; subtract from universe for burden-rate denominator",
    "B19013_001E": "Median household income (inflation-adjusted to ACS end year)",
    "B03002_001E": "Race/ethnicity universe",
    "B03002_003E": "Non-Hispanic White alone",
    "B03002_004E": "Non-Hispanic Black or African American alone",
    "B03002_005E": "Non-Hispanic American Indian and Alaska Native alone",
    "B03002_006E": "Non-Hispanic Asian alone",
    "B03002_007E": "Non-Hispanic Native Hawaiian and Other Pacific Islander alone",
    "B03002_008E": "Non-Hispanic some other race alone",
    "B03002_009E": "Non-Hispanic two or more races",
    "B03002_012E": "Hispanic or Latino (any race)",
    "B11001_001E": "Households (household-type universe)",
    "B11001_002E": "Family households",
    "B11001_006E": "Female-householder family, no spouse present (female-headed family households)",
    "B09019_003E": "Householders (persons)",
    "B09019_007E": "Female householders (family and nonfamily)",
    "B09019_008E": "Female householders living alone",
    "B17012_001E": "Families (family poverty universe)",
    "B17012_014E": "Female-householder families (no spouse) below poverty",
    "B17012_031E": "Female-householder families (no spouse) at/above poverty",
    "B23025_001E": "Population 16+",
    "B23025_003E": "Civilian labor force; unemployment-rate denominator",
    "B23025_005E": "Unemployed; unemployment-rate numerator",
    "B18101_001E": "Civilian noninstitutionalized population (disability universe)",
    "B18101_021E": "Females, civilian noninstitutionalized",
    "B18101_004E": "Males under 5 with a disability (sum all 'With a disability' rows for total)",
    "B18101_007E": "Males 5-17 with a disability",
    "B18101_010E": "Males 18-34 with a disability",
    "B18101_013E": "Males 35-64 with a disability",
    "B18101_016E": "Males 65-74 with a disability",
    "B18101_019E": "Males 75+ with a disability",
    "B18101_023E": "Females under 5 with a disability",
    "B18101_026E": "Females 5-17 with a disability",
    "B18101_029E": "Women 18-34 with a disability",
    "B18101_032E": "Women 35-64 with a disability",
    "B18101_035E": "Women 65-74 with a disability",
    "B18101_038E": "Women 75+ with a disability",
    "B21001_001E": "Civilian population 18+ (veteran universe)",
    "B21001_002E": "Veterans",
    "B21001_022E": "Civilian females 18+",
    "B21001_023E": "Female veterans",
}


# ---------------------------------------------------------------- helpers
def redact(url: str) -> str:
    return re.sub(r"(key|apikey|registrationkey)=[^&]+", r"\1=$KEY", url, flags=re.I)


def get(url, **kw):
    RL.wait()
    kw.setdefault("timeout", 90)
    return S.get(url, **kw)


def latest_raw(source: str, desc: str) -> Path | None:
    hits = sorted((RAW / source).glob(f"*_{desc}.*")) if (RAW / source).exists() else []
    return hits[-1] if hits else None


def fetch_or_reuse(source, desc, ext, fetch, refresh) -> tuple[Path, bool]:
    """Return (raw path, reused). fetch() must return bytes/str/dict for save_raw."""
    p = latest_raw(source, desc)
    if p and not refresh:
        return p, True
    return save_raw(source, desc, fetch(), ext), False


def result(key, status, note=""):
    RESULTS[key] = {"status": status, "note": note}


def arcgis_query(layer, params, method="get"):
    p = {"f": "json", **params}
    r = get(f"{layer}/query", params=p)
    r.raise_for_status()
    return r


# ---------------------------------------------------------------- census
def acs_latest_vintage() -> tuple[int, list[str]]:
    notes, latest = [], None
    for y in range(int(PROBE_DATE[:4]), 2019, -1):
        r = get(f"{CENSUS}/{y}/acs/acs5.json", allow_redirects=False)
        notes.append(f"{y}:{r.status_code}")
        if r.status_code == 200 and latest is None:
            latest = y
            save_raw("census", f"acs5_{y}_dataset_metadata", r.content, "json")
            break
    return latest, notes


def census_key_status(y: int) -> tuple[str, str]:
    """Return (status, note) for keyless and keyed data access."""
    q = {"get": "NAME,B01003_001E", "for": "state:11"}
    r = get(f"{CENSUS}/{y}/acs/acs5", params=q, allow_redirects=False)
    keyless = f"keyless HTTP {r.status_code} -> {r.headers.get('Location', '')}".strip()
    k = env_key("CENSUS_API_KEY")
    if not k:
        return "blocked_needs_key", keyless + "; CENSUS_API_KEY not set"
    r = get(f"{CENSUS}/{y}/acs/acs5", params={**q, "key": k}, allow_redirects=False)
    if r.status_code == 200:
        return "ok", keyless + "; keyed HTTP 200"
    loc = r.headers.get("Location", "")
    if "invalid_key" in loc:
        return "blocked_needs_key", keyless + "; key issued, pending activation (invalid_key redirect)"
    return "failed", keyless + f"; keyed HTTP {r.status_code} {loc}"


def acs_geos():
    geos = [("us", {"for": "us:1"}),
            ("states", {"for": "state:11,24,51,54"}),
            ("cbsa47900", {"for": f"metropolitan statistical area/micropolitan statistical area:{CBSA}"}),
            ("dc_wards_sldu", {"for": "state legislative district (upper chamber):*", "in": "state:11"}),
            ("dc_tracts", {"for": "tract:*", "in": "state:11 county:001"})]
    for st in ("11", "24", "51"):
        geos.append((f"counties_{STATE_ABBR[st].lower()}", {"for": "county:*", "in": f"state:{st}"}))
    geos.append(("counties_wv037", {"for": "county:037", "in": "state:54"}))
    return geos + extra_geos()


def extra_geos():
    """Geographies outside the DMV listed in config/extra_geographies.csv (e.g. a named comparator's county and
    tract). Raw files: raw/census/*_acs5_{y}_{group}_xgeo_{geo_key}.json."""
    p = CONFIG / "extra_geographies.csv"
    if not p.exists():
        return []
    out = []
    with open(p, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["geo_level"] == "county":
                params = {"for": f"county:{r['county_fips']}", "in": f"state:{r['state_fips']}"}
            elif r["geo_level"] == "tract":
                params = {"for": f"tract:{r['tract']}", "in": f"state:{r['state_fips']} county:{r['county_fips']}"}
            else:
                continue
            out.append((f"xgeo_{r['geo_key']}", params))
    return out


def acs_pulls(y, refresh, geos=None, section="census"):
    k = env_key("CENSUS_API_KEY")
    n_new = n_reuse = 0
    fails = []
    counts = {}
    geos = acs_geos() if geos is None else geos
    for g in ACS_GROUPS:
        for geo, params in geos:
            desc = f"acs5_{y}_{g}_{geo}"

            def fetch():
                r = get(f"{CENSUS}/{y}/acs/acs5", params={"get": f"NAME,group({g})", **params, "key": k},
                        allow_redirects=False)
                if r.status_code != 200:
                    raise RuntimeError(f"{g} {geo} HTTP {r.status_code}")
                return r.content
            try:
                p, reused = fetch_or_reuse("census", desc, "json", fetch, refresh)
            except Exception as e:  # noqa: BLE001
                fails.append(str(e))
                continue
            n_reuse += reused
            n_new += not reused
            if g == "B01003":
                counts[geo] = len(json.loads(p.read_text(encoding="utf-8"))) - 1
    SUMMARY[section].append(f"- ACS {y} group pulls: {n_new} new, {n_reuse} reused, {len(fails)} failed "
                            f"({len(ACS_GROUPS)} groups x {len(geos)} geographies)")
    SUMMARY[section].append("- B01003 row counts by geography: " + ", ".join(f"{k}={v}" for k, v in counts.items()))
    if fails:
        SUMMARY[section].append("- failures: " + "; ".join(fails[:10]))
    return counts, fails


def write_acs_variables(vars_path: Path, y: int):
    v = json.loads(vars_path.read_text(encoding="utf-8"))["variables"]
    out = CONFIG / "acs_variables.csv"
    missing = []
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["variable", "label", "concept", "use", "group", "moe_variable", "sf_est_col",
                    "sf_moe_col", "vintage", "source_id"])
        for var, use in ACS_VARS.items():
            meta = v.get(var)
            if not meta:
                missing.append(var)
                continue
            grp, num = var[:-1].split("_")
            w.writerow([var, meta["label"], meta.get("concept", ""), use, meta.get("group", grp),
                        var[:-1] + "M", f"{grp}_E{num}", f"{grp}_M{num}", f"{y - 4}-{y}", "api_census_acs5"])
    SUMMARY["census"].append(f"- wrote {rel(out)}: {len(ACS_VARS) - len(missing)} variables"
                             + (f"; missing from variables.json: {missing}" if missing else ""))


def sf_probe(y, fallback):
    base = SF_BASE.format(y=y)
    r = get(f"{base}/data/5YRData/")
    if r.status_code != 200:
        result("sf", "failed", f"listing HTTP {r.status_code}")
        return
    save_raw("census", f"acs_sf_{y}_5yr_listing", r.content, "html")
    sizes = {}
    for g in ACS_GROUPS:
        m = re.search(rf"acsdt5y{y}-{g.lower()}\.dat</a></td><td[^>]*>([^<]*)</td><td[^>]*>\s*([^<]*)</td>", r.text)
        sizes[g] = m.group(2).strip() if m else "missing"
    note = "table files (national, all summary levels incl. tract 140, ward/SLDU 610, CBSA 310): " + \
           ", ".join(f"{g}={s}" for g, s in sizes.items())
    result("sf", "ok", note)
    SUMMARY["census"].append(f"- Summary File {y} 5YR keyless listing ok; {note}")
    if fallback:
        for g in ACS_GROUPS:
            u = f"{base}/data/5YRData/acsdt5y{y}-{g.lower()}.dat"
            rr = get(u, timeout=600)
            rr.raise_for_status()
            p = save_raw("census", f"acs_sf_{y}_5yr_{g.lower()}", rr.content, "dat")
            SUMMARY["census"].append(f"- SF fallback downloaded {rel(p)} ({len(rr.content):,} bytes)")


def pl_blocks(refresh) -> Path | None:
    k = env_key("CENSUS_API_KEY")
    if k:
        def fetch():
            r = get(PL_URL, params={"get": "P1_001N,H1_001N", "for": "block:*",
                                    "in": "state:11 county:001 tract:*", "key": k}, allow_redirects=False)
            r.raise_for_status()
            if r.status_code != 200:
                raise RuntimeError(f"PL HTTP {r.status_code}")
            return r.content
        try:
            p, reused = fetch_or_reuse("census", "dec2020_pl_blocks_dc", "json", fetch, refresh)
            n = len(json.loads(p.read_text(encoding="utf-8"))) - 1
            result("pl", "ok", f"{n} DC blocks with P1_001N/H1_001N")
            SUMMARY["census"].append(f"- 2020 PL blocks DC: {n} rows ({'reused' if reused else 'new'})")
            return p
        except Exception as e:  # noqa: BLE001
            result("pl", "failed", str(e))
    # keyless fallback: DC GIS Census Blocks 2020 attributes
    feats, offset = [], 0
    while True:
        r = arcgis_query(BLOCKS_LAYER, {"where": "1=1", "outFields": "GEOID,P0010001,H0010001",
                                        "returnGeometry": "false", "resultOffset": offset,
                                        "resultRecordCount": 1000, "orderByFields": "GEOID"})
        page = r.json().get("features", [])
        feats += page
        if len(page) < 1000:
            break
        offset += 1000
    p = save_raw("census", "dcgis_blocks2020_pop_dc", {"features": feats}, "json")
    result("pl", "ok" if feats else "failed", f"keyless fallback via DC GIS blocks layer: {len(feats)} blocks")
    return p


def bef_dc(refresh) -> Path | None:
    def fetch():
        from remotezip import RemoteZip
        with RemoteZip(BEF_ZIP, headers={"User-Agent": S.headers["User-Agent"]}) as z:
            return z.read(BEF_MEMBER)
    try:
        p, reused = fetch_or_reuse("census", "bef_sldu2022_11_DC", "txt", fetch, refresh)
        n = sum(1 for _ in open(p, encoding="utf-8")) - 1
        result("bef", "ok", f"{BEF_MEMBER}: {n} blocks -> SLDU (ward)")
        SUMMARY["census"].append(f"- 2022 SLDU BEF {BEF_MEMBER}: {n} rows ({'reused' if reused else 'new'})")
        return p
    except Exception as e:  # noqa: BLE001
        result("bef", "failed", str(e))
        return None


def run_census(refresh, sf_fallback):
    y, vnotes = acs_latest_vintage()
    SUMMARY["census"].append(f"- ACS 5-year vintage probe (dataset metadata HTTP): {', '.join(vnotes)} -> latest {y}")
    status, note = census_key_status(y)
    result("acs", status, f"latest vintage {y} ({y - 4}-{y}); {note}")
    SUMMARY["census"].append(f"- Census data API: {status}; {note}")
    vp, reused = fetch_or_reuse("census", f"acs5_{y}_variables", "json",
                                lambda: get(f"{CENSUS}/{y}/acs/acs5/variables.json").content, refresh)
    SUMMARY["census"].append(f"- variables.json: {rel(vp)} ({'reused' if reused else 'new'})")
    write_acs_variables(vp, y)
    if status == "ok":
        acs_pulls(y, refresh)
    else:
        SUMMARY["census"].append("- ACS group pulls skipped (no working key); keyless fallback = Summary File "
                                 "(rerun with --sf-fallback)")
    sf_probe(y, sf_fallback)
    pl = pl_blocks(refresh)
    bef = bef_dc(refresh)
    return y, pl, bef


# ---------------------------------------------------------------- geo
def run_geo(refresh, y, pl_path, bef_path):
    out = {}
    # ward polygons (no representative contact fields)
    meta = get(WARDS_LAYER, params={"f": "json"})
    save_raw("geo", "dcgis_wards_2022_layer_metadata", meta.content, "json")
    fields = "WARD,NAME,WARD_ID,LABEL,STUSAB,SUMLEV,GEOID,GEOCODE,STATE,OBJECTID"
    wp, reused = fetch_or_reuse(
        "geo", "dcgis_wards_2022", "geojson",
        lambda: arcgis_query(WARDS_LAYER, {"where": "1=1", "outFields": fields, "outSR": 4326,
                                           "f": "geojson"}).content, refresh)
    wards = json.loads(wp.read_text(encoding="utf-8"))
    result("wards", "ok" if len(wards["features"]) == 8 else "failed",
           f"{len(wards['features'])} ward polygons")
    SUMMARY["geo"].append(f"- DC wards 2022: {len(wards['features'])} features -> {rel(wp)}")
    out["wards"] = wards

    tp, reused = fetch_or_reuse(
        "geo", "tigerweb_acs2024_tracts_dc", "geojson",
        lambda: arcgis_query(TIGER_TRACTS, {"where": "STATE='11'", "outSR": 4326, "f": "geojson",
                                            "outFields": "GEOID,STATE,COUNTY,TRACT,NAME,AREALAND,"
                                                         "AREAWATER,CENTLAT,CENTLON,INTPTLAT,INTPTLON"}).content,
        refresh)
    tracts = json.loads(tp.read_text(encoding="utf-8"))
    result("tiger", "ok", f"{len(tracts['features'])} DC tracts (2020 tract vintage, ACS2024 service)")
    SUMMARY["geo"].append(f"- TIGERweb DC tracts: {len(tracts['features'])} -> {rel(tp)}")
    out["tracts"] = tracts

    # DC Office of Planning ACS ward profiles
    vint = {}
    for name, lid in ACS_WARD_LAYERS.items():
        layer = f"{DCGIS}/Demographic_WebMercator/MapServer/{lid}"
        m = get(layer, params={"f": "json"})
        save_raw("geo", f"dcgis_acs5_ward_{name}_metadata", m.content, "json")
        desc = m.json().get("description", "") or ""
        mv = re.search(r"Current Vintage:\s*([0-9]{4}-[0-9]{4})", desc)
        vint[name] = mv.group(1) if mv else "unknown"
        a = arcgis_query(layer, {"where": "1=1", "outFields": "*", "returnGeometry": "false"})
        save_raw("geo", f"dcgis_acs5_ward_{name}", a.content, "json")
        vint[name] += f" ({len(a.json().get('features', []))} rows)"
    result("opward", "ok", "DC OP ward profiles: " + "; ".join(f"{k} {v}" for k, v in vint.items()))
    SUMMARY["geo"].append("- DC OP ACS ward layers: " + "; ".join(f"{k} {v}" for k, v in vint.items()))

    # official crosswalk search
    found = []
    for q in ("crosswalk", "tract ward", "census tract ward equivalency"):
        r = get(HUB_SEARCH, params={"q": q, "limit": 25})
        save_raw("geo", f"dcopendata_search_{q.replace(' ', '_')}", r.content, "json")
        for f in r.json().get("features", []):
            t = f["properties"].get("title", "")
            if re.search(r"crosswalk|equivalen|relationship", t, re.I) and re.search(r"tract|ward", t, re.I):
                found.append(t)
    SUMMARY["geo"].append(f"- DC Open Data search for tract-ward crosswalk: {found or 'none found'}")
    out["crosswalk_found"] = found

    pl_path = pl_path or latest_raw("census", "dec2020_pl_blocks_dc") or latest_raw("census", "dcgis_blocks2020_pop_dc")
    bef_path = bef_path or latest_raw("census", "bef_sldu2022_11_DC")
    if y is None:
        hits = sorted((RAW / "census").glob("*_acs5_*_variables.json"))
        y = int(re.search(r"acs5_(\d{4})_variables", hits[-1].name).group(1)) if hits else None
    if pl_path and bef_path:
        crosswalk_check(pl_path, bef_path, wards, tracts, y)
    return out


def load_block_pop(pl_path: Path) -> dict[str, tuple[int, int]]:
    d = json.loads(pl_path.read_text(encoding="utf-8"))
    if isinstance(d, list):   # Census API array
        h = d[0]
        i = {c: h.index(c) for c in h}
        return {r[i["state"]] + r[i["county"]] + r[i["tract"]] + r[i["block"]]:
                (int(r[i["P1_001N"]]), int(r[i["H1_001N"]])) for r in d[1:]}
    return {f["attributes"]["GEOID"]: (int(f["attributes"]["P0010001"] or 0), int(f["attributes"]["H0010001"] or 0))
            for f in d["features"]}


def crosswalk_check(pl_path, bef_path, wards, tracts, y):
    """Validate block-based tract->ward weights and compare with the tract-centroid method."""
    from shapely.geometry import Point, shape
    pop = load_block_pop(pl_path)
    bef = {}
    with open(bef_path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            bef[r["GEOID"]] = int(r["SLDUST"])
    tw = defaultdict(lambda: defaultdict(int))
    unmatched = 0
    for b, (p, _) in pop.items():
        w = bef.get(b)
        if w is None:
            unmatched += 1
            continue
        tw[b[:11]][w] += p
    split = {t: d for t, d in tw.items() if sum(1 for v in d.values() if v > 0) > 1}
    minor = {t: d for t, d in split.items() if max(d.values()) / max(sum(d.values()), 1) < 0.95}
    ward_pop = defaultdict(int)
    for d in tw.values():
        for w, v in d.items():
            ward_pop[w] += v
    polys = {int(f["properties"]["WARD"]): shape(f["geometry"]) for f in wards["features"]}
    agree = disagree = 0
    for f in tracts["features"]:
        pr = f["properties"]
        t = pr["GEOID"]
        pt = Point(float(pr["INTPTLON"]), float(pr["INTPTLAT"]))
        cw = next((w for w, g in polys.items() if g.contains(pt)), None)
        if t in tw and sum(tw[t].values()) > 0:
            maj = max(tw[t], key=tw[t].get)
            agree += cw == maj
            disagree += cw != maj
    cal = dict(tw.get("11001007503", {}))
    lines = [
        f"- crosswalk check: {len(pop)} blocks, {len(bef)} BEF rows, {unmatched} blocks without ward",
        f"- {len(tw)} tracts; {len(split)} span >1 ward (pop>0); {len(minor)} have <95% of pop in one ward",
        "- 2020 pop by ward (blocks via BEF): " + ", ".join(f"W{w}={v:,}" for w, v in sorted(ward_pop.items())),
        f"- tract internal-point method vs block-majority ward: {agree} agree, {disagree} differ",
        f"- Calvary tract 11001007503 ward pop split: {cal}",
    ]
    SUMMARY["geo"] += lines
    # compare ACS SLDU ward totals vs tract totals allocated by block-pop weights
    tp = latest_raw("census", f"acs5_{y}_B01003_dc_tracts")
    wp = latest_raw("census", f"acs5_{y}_B01003_dc_wards_sldu")
    if tp and wp:
        tj = json.loads(tp.read_text(encoding="utf-8"))
        wj = json.loads(wp.read_text(encoding="utf-8"))
        th, wh = tj[0], wj[0]
        alloc = defaultdict(float)
        for r in tj[1:]:
            t = r[th.index("GEO_ID")][-11:]
            v = float(r[th.index("B01003_001E")])
            tot = sum(tw.get(t, {}).values())
            for w, p in tw.get(t, {}).items():
                alloc[w] += v * p / tot if tot else 0
        cmp_ = []
        for r in wj[1:]:
            w = int(r[wh.index("state legislative district (upper chamber)")])
            cmp_.append(f"W{w} sldu={int(r[wh.index('B01003_001E')]):,} alloc={alloc[w]:,.0f}")
        SUMMARY["geo"].append(f"- ACS {y} B01003 ward (SLDU) vs tract-allocated: " + "; ".join(cmp_))
    result("xwalk", "ok", f"{len(split)} of {len(tw)} tracts split; {len(minor)} <95% in one ward; "
                          f"centroid agrees with block-majority for {agree}/{agree + disagree}")


# ---------------------------------------------------------------- geocode
def run_geocode():
    calvary = TEST_ADDRESSES[0][1]
    # MAR 2 API
    k = env_key("DC_MAR_API_KEY")
    params = {"apikey": k} if k else {}
    RL.wait()   # plain requests: MAR 2 answers a missing key with HTTP 500, which the retry session would retry
    r = requests.get(f"{MAR2}/locations/{calvary}", params=params, timeout=60,
                     headers={"User-Agent": S.headers["User-Agent"]})
    save_raw("geo", "mar2_locations_calvary", r.content, "json")
    try:
        j = r.json()
    except ValueError:
        j = {}
    if not k:
        result("mar2", "blocked_needs_key", f"HTTP {r.status_code}: {j.get('Message', '')}")
    else:
        result("mar2", "ok" if r.status_code == 200 and j.get("Success") else "failed", f"HTTP {r.status_code}")
    SUMMARY["geocode"].append(f"- MAR 2 API: {RESULTS['mar2']['status']} ({RESULTS['mar2']['note']})")

    # DC GIS Address Points (MAR) keyless
    a = arcgis_query(ADDR_LAYER, {"where": "ADDRESS_NUMBER=1217 AND STREET_NAME='MARION BARRY' AND QUADRANT='SE'",
                                  "outFields": "ADDRESS,MAR_ID,WARD,SMD,ANC,ZIPCODE,LATITUDE,LONGITUDE,STATUS,"
                                               "RESIDENTIAL_TYPE,SSL",
                                  "returnGeometry": "false"})
    save_raw("geo", "dcgis_address_points_calvary", a.content, "json")
    feats = a.json().get("features", [])
    if feats:
        at = feats[0]["attributes"]
        note = (f"{at['ADDRESS']}: {at['WARD']}, {at['SMD']}, {at['ANC']}, lat {at['LATITUDE']}, "
                f"lon {at['LONGITUDE']}, MAR_ID {int(at['MAR_ID'])}; no tract field")
        result("addrpts", "ok", note)
    else:
        result("addrpts", "ok_no_results", "no match")
    SUMMARY["geocode"].append(f"- DC GIS Address Points: {RESULTS['addrpts']['note']}")

    # Census Geocoder single-line
    lines = []
    for label, street, city, st, z in TEST_ADDRESSES:
        rr = get(f"{GEOCODER}/geographies/onelineaddress",
                 params={"address": f"{street}, {city}, {st} {z}", "benchmark": "Public_AR_Current",
                         "vintage": "ACS2024_Current", "layers": "all", "format": "json"})
        save_raw("geo", f"census_geocoder_oneline_{label}", rr.content, "json")
        m = rr.json().get("result", {}).get("addressMatches", [])
        if not m:
            lines.append(f"{label}: no match")
            continue
        g = m[0]["geographies"]
        tract = g.get("Census Tracts", [{}])[0].get("GEOID")
        county = g.get("Counties", [{}])[0].get("GEOID")
        sldu = next((v[0].get("NAME") for kk, v in g.items() if "Legislative Districts - Upper" in kk and v), "")
        lines.append(f"{label}: county {county}, tract {tract}, SLDU {sldu}")
    ok_single = sum("no match" not in x for x in lines)
    # Census Geocoder batch (2020 vintage returns block, which joins to the ward BEF)
    buf = io.StringIO()
    w = csv.writer(buf)
    for i, (label, street, city, st, z) in enumerate(TEST_ADDRESSES, 1):
        w.writerow([i, street, city, st, z])
    RL.wait()
    br = S.post(f"{GEOCODER}/geographies/addressbatch",
                files={"addressFile": ("batch.csv", buf.getvalue().encode(), "text/csv")},
                data={"benchmark": "Public_AR_Current", "vintage": "Census2020_Current"}, timeout=300)
    save_raw("geo", "census_geocoder_batch_test", br.content, "csv")
    brows = list(csv.reader(io.StringIO(br.text)))
    bmatch = sum(1 for r in brows if len(r) > 2 and r[2] == "Match")
    note = (f"single: {ok_single}/{len(lines)} matched; batch: {bmatch}/{len(brows)} matched; "
            + " | ".join(lines))
    result("geocoder", "ok", note)
    SUMMARY["geocode"].append("- Census Geocoder " + note)


# ---------------------------------------------------------------- omb
def run_omb(refresh):
    import pandas as pd
    p, reused = fetch_or_reuse("census", "omb_cbsa_delineation_list1_2023", "xlsx",
                               lambda: get(OMB_XLSX).content, refresh)
    raw = pd.read_excel(p, header=None, dtype=str)
    hdr = raw.index[raw.iloc[:, 0].astype(str).str.strip().eq("CBSA Code")][0]
    d = pd.read_excel(p, header=hdr, dtype=str)
    m = d[d["CBSA Code"] == CBSA].copy()
    rows = []
    for _, r in m.iterrows():
        st = r["FIPS State Code"].zfill(2)
        rows.append({
            "state_fips": st, "county_fips": r["FIPS County Code"].zfill(3),
            "county_name": r["County/County Equivalent"], "state_abbr": STATE_ABBR.get(st, ""),
            "in_msa": "true", "metro_division": r["Metropolitan Division Title"],
            "metro_division_code": r["Metropolitan Division Code"],
            "county_geoid": st + r["FIPS County Code"].zfill(3),
            "central_outlying": r["Central/Outlying County"],
            "in_scope": "true" if st in ("11", "24", "51") else "false",
            "scope_note": "" if st in ("11", "24", "51") else "in MSA but outside DC/MD/VA scope",
            "cbsa_code": CBSA, "cbsa_title": r["CBSA Title"], "delineation": "OMB Bulletin 23-01 (July 2023)",
            "source_id": "bulk_omb_cbsa_2023",
        })
    rows.sort(key=lambda x: (x["state_fips"] != "11", x["state_fips"], x["county_fips"]))
    out = CONFIG / "dmv_counties.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    by = defaultdict(int)
    for r in rows:
        by[r["state_abbr"]] += 1
    result("omb", "ok", f"CBSA {CBSA}: {len(rows)} counties/cities ({dict(by)})")
    SUMMARY["omb"].append(f"- OMB list1_2023 ({'reused' if reused else 'new'}): CBSA {CBSA} {len(rows)} rows "
                          f"{dict(by)} -> {rel(out)}")


# ---------------------------------------------------------------- cpi
def run_cpi():
    k = env_key("BLS_API_KEY")
    span = 20 if k else 10
    windows, start = [], 2000
    while start <= 2025:
        windows.append((start, min(start + span - 1, 2025)))
        start += span
    data = defaultdict(dict)   # series -> year -> (value, footnotes)
    monthly_2025 = {}
    msgs = []
    for a, b in windows:
        body = {"seriesid": list(CPI_SERIES), "startyear": str(a), "endyear": str(b), "annualaverage": True}
        if k:
            body["registrationkey"] = k
        RL.wait()
        r = S.post(BLS_V2, json=body, timeout=90)
        save_raw("bls", f"cpi_{'_'.join(CPI_SERIES)}_{a}_{b}", r.content, "json")
        j = r.json()
        msgs += [m for m in j.get("message", []) if m]
        if j.get("status") != "REQUEST_SUCCEEDED":
            result("bls", "failed", f"{j.get('status')} {j.get('message')}")
            return
        for s in j["Results"]["series"]:
            for row in s["data"]:
                per = row["period"]
                if per in ("M13", "S03"):
                    fn = "; ".join(f.get("text", "") for f in row.get("footnotes", []) if f and f.get("text"))
                    data[s["seriesID"]][int(row["year"])] = (row["value"], fn)
                if s["seriesID"] == "CUUR0000SA0" and row["year"] == "2025" and per.startswith("M") and per != "M13":
                    monthly_2025[per] = row["value"]
    us, dcm, dcs = data["CUUR0000SA0"], data["CUURS35ASA0"], data["CUUSS35ASA0"]
    out = CONFIG / "cpi_u_annual.csv"
    b_us = float(us[BASE_YEAR][0])
    b_dc = float((dcm.get(BASE_YEAR) or dcs.get(BASE_YEAR))[0])
    n = 0
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["year", "cpi_u_us", "cpi_u_dc_metro", "source_id", "base_year", "us_factor_to_base",
                    "dc_factor_to_base", "us_series", "dc_series", "dc_period", "notes"])
        for yr in range(2000, 2026):
            u = us.get(yr, ("", ""))[0]
            dv, dsrc, dper = "", "", ""
            if yr in dcm:
                dv, dsrc, dper = dcm[yr][0], "CUURS35ASA0", "M13"
            elif yr in dcs:
                dv, dsrc, dper = dcs[yr][0], "CUUSS35ASA0", "S03"
            note = []
            if yr == 2025 and monthly_2025.get("M10") in ("-", None):
                note.append("Oct 2025 not collected (2025 lapse in appropriations); BLS annual average still published")
            uf = f"{b_us / float(u):.6f}" if u not in ("", "-") else ""
            df = f"{b_dc / float(dv):.6f}" if dv not in ("", "-") else ""
            w.writerow([yr, u, dv, "api_bls_cpi", BASE_YEAR, uf, df, "CUUR0000SA0" if u else "", dsrc, dper,
                        "; ".join(note)])
            n += bool(u)
    have25 = 2025 in us
    dc_years = sorted(set(dcm) | set(dcs))
    result("bls", "ok", f"US annual avg {min(us)}-{max(us)}; DC metro {dc_years[0] if dc_years else '-'}-"
                        f"{dc_years[-1] if dc_years else '-'}; 2025 annual average published: {have25}"
                        + (f" ({us[2025][0]})" if have25 else "") + ("; keyless (10-year windows)" if not k else ""))
    SUMMARY["cpi"].append(f"- BLS v2 {'keyed' if k else 'keyless'}: {len(windows)} requests; {RESULTS['bls']['note']}; "
                          f"messages: {sorted(set(msgs))[:3]}")
    SUMMARY["cpi"].append(f"- wrote {rel(out)} ({n} US years, base {BASE_YEAR}: US {b_us}, DC {b_dc})")
    # FRED probe (keyless CSV)
    try:
        r = requests.get(FRED_CSV, params={"id": "CPIAUCNS"}, timeout=20, headers={"User-Agent": S.headers["User-Agent"]})
        if r.status_code == 200 and r.text.startswith("observation_date"):
            save_raw("bls", "fred_cpiaucns", r.content, "csv")
            result("fred", "ok", "fredgraph.csv reachable")
        else:
            result("fred", "failed", f"HTTP {r.status_code}")
    except requests.RequestException as e:
        result("fred", "failed", f"{type(e).__name__} (connection reset/timeout from this host)")
    SUMMARY["cpi"].append(f"- FRED fredgraph.csv: {RESULTS['fred']['status']} {RESULTS['fred']['note']}")


# ---------------------------------------------------------------- catalog + registry
CATALOG_COLS = ["name", "area", "base_url", "auth_required", "auth_env_var", "rate_limit", "key_endpoints",
                "fields_of_interest", "years_covered", "coverage_gaps", "sample_request", "sample_status",
                "probe_date", "feeds_tables", "source_id", "notes"]


def catalog_rows(y):
    yy = y or 2024
    acs_q = (f"{CENSUS}/{yy}/acs/acs5?get=NAME,group(B17001)&for=tract:*&in=state:11%20county:001"
             "&key=$CENSUS_API_KEY")
    R = lambda k, d="not_applicable": RESULTS.get(k, {"status": d, "note": "not probed this run"})  # noqa: E731
    return [
        ["Census ACS 5-year API", "context", f"{CENSUS}/{yy}/acs/acs5", "yes", "CENSUS_API_KEY",
         "key required for every data call (keyless redirects to missing_key.html); max 50 variables or one "
         "group() per call; metadata (variables.json, groups) keyless",
         "/data/{y}/acs/acs5?get=NAME,group(Bxxxxx)&for=...; /variables.json; /groups/{g}.json",
         "B01003 B03002 B09019 B11001 B17001 B17012 B18101 B19013 B21001 B23025 B25070 (E,M,EA,MA)",
         f"latest 5-year {yy - 4}-{yy}; 2009-{yy} vintages", "2025 5-year (2021-2025) not released at probe date; "
         "tract MOEs large in Wards 7/8", acs_q, R("acs")["status"], PROBE_DATE, "dim_geo", "api_census_acs5",
         R("acs")["note"] + "; geographies: tract, SLDU (=DC ward), county, state, CBSA 47900, us"],
        ["ACS table-based Summary File (5-year)", "context", SF_BASE.format(y=yy) + "/data/5YRData/", "no", "",
         "static files; no limit", "acsdt5y{y}-{table}.dat (pipe-delimited, GEO_ID|{T}_E001|{T}_M001...)",
         "same tables as API; GEO_ID prefixes 1400000US11001 (DC tracts), 610U900US110 (wards), "
         "0500000US (counties), 310M700US47900 (MSA)",
         f"{yy - 4}-{yy} (table-based format since 2021 vintage)", "national files 16-145 MB per table",
         SF_BASE.format(y=yy) + f"/data/5YRData/acsdt5y{yy}-b19013.dat", R("sf")["status"], PROBE_DATE,
         "dim_geo", "bulk_census_acs_sf", "keyless fallback to the API. " + R("sf")["note"]],
        ["Census 2020 PL 94-171 (block counts)", "context", PL_URL, "yes", "CENSUS_API_KEY", "as ACS API",
         "?get=P1_001N,H1_001N&for=block:*&in=state:11 county:001 tract:*", "P1_001N total pop; H1_001N housing units",
         "2020", "decennial only; weights fixed at 2020",
         PL_URL + "?get=P1_001N,H1_001N&for=block:*&in=state:11%20county:001%20tract:*&key=$CENSUS_API_KEY",
         R("pl")["status"], PROBE_DATE, "dim_geo", "api_census_dec_pl",
         R("pl")["note"] + "; weights for tract->ward crosswalk; keyless fallback = DC GIS Census Blocks 2020 layer"],
        ["Census 2022 State Legislative District BEF (DC wards)", "context", BEF_ZIP, "no", "", "static file",
         BEF_MEMBER + " inside sldu_2022.zip (25 MB; member read by HTTP range)", "GEOID (2020 block), SLDUST (ward 001-008)",
         "2022 wards (still current: DC absent from 2024 SLD BEF update)", "none for DC", BEF_ZIP, R("bef")["status"],
         PROBE_DATE, "dim_geo", "bulk_census_bef_sldu2022",
         R("bef")["note"] + "; official block->ward assignment (DC wards are Census SLDU)"],
        ["TIGERweb ACS2024 Census Tracts", "context", TIGER_TRACTS, "no", "", "maxRecordCount 100000",
         "/query?where=STATE='11'&outSR=4326&f=geojson", "GEOID, AREALAND, INTPTLAT/INTPTLON polygons",
         "2020 tracts (used by ACS 2020-2024)", "", TIGER_TRACTS + "/query?where=STATE%3D%2711%27&outFields=GEOID"
         "&outSR=4326&f=geojson", R("tiger")["status"], PROBE_DATE, "dim_geo", "api_tigerweb", R("tiger")["note"]],
        ["DC GIS Wards from 2022", "context", WARDS_LAYER, "no", "", "maxRecordCount 1000",
         "/query?where=1=1&outSR=4326&f=geojson", "WARD, NAME, GEOID polygons", "2022 wards (effective 2022 elections)",
         "layer also carries councilmember contact fields; excluded from pull", WARDS_LAYER +
         "/query?where=1%3D1&outFields=WARD,NAME,GEOID&outSR=4326&f=geojson", R("wards")["status"], PROBE_DATE,
         "dim_geo", "api_dcgis_wards_2022", R("wards")["note"] + "; no official tract-ward crosswalk found on DC Open Data"],
        ["DC Office of Planning ACS 5-year ward profiles", "context", f"{DCGIS}/Demographic_WebMercator/MapServer",
         "no", "", "maxRecordCount 1000", "layers 39 (DP05), 42 (DP03), 45 (DP04), 48 (DP02) by 2022 ward; "
         "38/41/44/47 by tract", "DP02-DP05 profile estimates by ward", "current vintage only (overwritten annually)",
         "profile tables only (no B17001 female-by-age detail); no history in service",
         f"{DCGIS}/Demographic_WebMercator/MapServer/42/query?where=1%3D1&outFields=*&returnGeometry=false&f=json",
         R("opward")["status"], PROBE_DATE, "dim_geo", "api_dcgis_acs_ward", R("opward")["note"]],
        ["DC MAR 2 API (geocoder)", "context", MAR2, "yes", "DC_MAR_API_KEY", "unknown (free key via "
         "developers.data.dc.gov)", "/locations/{address}?apikey=; /locations/{x,y}/{radius}",
         "MAR ID, lat/lon, ward (2002/2012/2022), ANC, SMD, voter precinct, cluster", "current", "DC addresses only",
         MAR2 + "/locations/1217%20Marion%20Barry%20Ave%20SE?apikey=$DC_MAR_API_KEY", R("mar2")["status"], PROBE_DATE,
         "dim_geo;dim_org", "api_dc_mar2", R("mar2")["note"] + "; register at developers.data.dc.gov"],
        ["DC GIS Address Points (MAR extract)", "context", ADDR_LAYER, "no", "", "maxRecordCount 2000",
         "/query?where=ADDRESS_NUMBER=..&STREET_NAME=..&f=json", "ADDRESS, MAR_ID, WARD, SMD, ANC, LATITUDE, LONGITUDE",
         "current MAR", "exact-attribute match only (no fuzzy geocoding); no census tract field",
         ADDR_LAYER + "/query?where=ADDRESS_NUMBER%3D1217%20AND%20STREET_NAME%3D%27MARION%20BARRY%27"
         "&outFields=ADDRESS,WARD,SMD,ANC,LATITUDE,LONGITUDE&returnGeometry=false&f=json",
         R("addrpts")["status"], PROBE_DATE, "dim_geo;dim_org", "api_dcgis_address_points", R("addrpts")["note"]],
        ["Census Geocoder", "context", GEOCODER, "no", "", "batch: 10,000 addresses per file; single: no stated limit",
         "/geographies/onelineaddress; /geographies/address; /geographies/addressbatch (POST multipart)",
         "lat/lon, state, county, tract, block (Census2020 vintage), SLDU (=DC ward) in single-line layers=all",
         "benchmarks Public_AR_Current, Public_AR_ACS2026, Census2020", "TIGER street names lag local renames "
         "(Marion Barry Ave SE = former Good Hope Rd SE: new name does not match)",
         GEOCODER + "/geographies/onelineaddress?address=1217%20Good%20Hope%20Rd%20SE%2C%20Washington%2C%20DC%2020020"
         "&benchmark=Public_AR_Current&vintage=ACS2024_Current&format=json", R("geocoder")["status"], PROBE_DATE,
         "dim_geo;dim_org", "api_census_geocoder", R("geocoder")["note"]],
        ["OMB CBSA delineation file (July 2023)", "context", OMB_XLSX, "no", "", "static file", "list1_2023.xlsx",
         "CBSA, metro division, CSA, county FIPS, central/outlying", "July 2023 delineation (latest)",
         "Calvert Co. MD left CBSA 47900 in 2023 (now Lexington Park CBSA)", OMB_XLSX, R("omb")["status"], PROBE_DATE,
         "dim_geo", "bulk_omb_cbsa_2023", R("omb")["note"]],
        ["BLS CPI-U (Public Data API v2)", "context", BLS_V2, "no (key optional)", "BLS_API_KEY",
         "keyless: 25 queries/day, 10 years and 25 series per query; keyed: 500/day, 20 years, 50 series",
         "POST {seriesid:[...], startyear, endyear, annualaverage:true}",
         "CUUR0000SA0 (US city avg), CUURS35ASA0 (Washington-Arlington-Alexandria, bimonthly), "
         "CUUSS35ASA0 (same, semiannual; S03 = annual)", "2000-2025 annual averages", "Oct 2025 not collected",
         '{"seriesid":["CUUR0000SA0","CUURS35ASA0"],"startyear":"2016","endyear":"2025","annualaverage":true}',
         R("bls")["status"], PROBE_DATE, "dim_period", "api_bls_cpi", R("bls")["note"]],
        ["FRED fredgraph CSV (CPI)", "context", FRED_CSV, "no", "", "unknown", "?id=CPIAUCNS&fq=Annual&fam=avg",
         "CPIAUCNS, CUURS35ASA0", "", "not reachable from build host", FRED_CSV + "?id=CPIAUCNS",
         R("fred")["status"], PROBE_DATE, "dim_period", "", R("fred")["note"] + "; not needed (BLS covers it)"],
    ]


def register_all():
    reg = [
        ("api_census_acs5", "Census ACS 5-year detailed tables API", f"{CENSUS}/{{y}}/acs/acs5",
         "U.S. Census Bureau", "Public domain; cite U.S. Census Bureau, American Community Survey 5-year estimates",
         "Key required for data; variables.json keyless. Raw: raw/census/*_acs5_*"),
        ("bulk_census_acs_sf", "ACS table-based Summary File (5-year)", SF_BASE.format(y="{y}"),
         "U.S. Census Bureau", "Public domain", "Keyless fallback for ACS tables; listing probed"),
        ("api_census_dec_pl", "2020 Census Redistricting Data (PL 94-171) API, block counts", PL_URL,
         "U.S. Census Bureau", "Public domain", "DC block population and housing units for crosswalk weights"),
        ("bulk_census_bef_sldu2022", "2022 State Legislative District Block Equivalency File (SLDU)", BEF_ZIP,
         "U.S. Census Bureau", "Public domain", f"Member {BEF_MEMBER} read via HTTP range; DC SLDU = 2022 wards"),
        ("api_tigerweb", "TIGERweb ACS2024 Census Tracts (ArcGIS REST)", TIGER_TRACTS, "U.S. Census Bureau",
         "Public domain", "DC tract polygons and internal points"),
        ("api_dcgis_wards_2022", "DC Wards from 2022 (DC GIS)", WARDS_LAYER, "DC Office of the Chief Technology Officer",
         "DC Open Data (CC BY 4.0)", "Ward polygons; contact fields excluded"),
        ("api_dcgis_acs_ward", "DC Office of Planning ACS 5-year profiles by ward (DC GIS)",
         f"{DCGIS}/Demographic_WebMercator/MapServer", "DC Office of Planning", "DC Open Data (CC BY 4.0); cite ACS",
         "Layers 39/42/45/48; current vintage only"),
        ("api_dc_mar2", "DC Master Address Repository 2 API", MAR2, "DC Office of the Chief Technology Officer",
         "DC Open Data terms", "Key required (DC_MAR_API_KEY)"),
        ("api_dcgis_address_points", "DC Address Points (MAR extract, DC GIS)", ADDR_LAYER,
         "DC Office of the Chief Technology Officer", "DC Open Data (CC BY 4.0)", "Keyless ward/SMD/ANC/lat-lon lookup"),
        ("api_census_geocoder", "Census Geocoder (single and batch)", GEOCODER, "U.S. Census Bureau", "Public domain",
         "Keyless; batch up to 10,000"),
        ("bulk_omb_cbsa_2023", "OMB CBSA delineation file, July 2023 (list 1)", OMB_XLSX, "U.S. Census Bureau / OMB",
         "Public domain; OMB Bulletin 23-01", "Source of config/dmv_counties.csv"),
        ("api_bls_cpi", "BLS Public Data API v2, CPI-U", BLS_V2, "U.S. Bureau of Labor Statistics", "Public domain",
         "CUUR0000SA0, CUURS35ASA0, CUUSS35ASA0 annual averages; source of config/cpi_u_annual.csv"),
    ]
    for r in reg:
        register_source(*r)


def write_catalog(y):
    """Write the catalog part; rows not probed in a partial run (--only) keep their previous values."""
    out = SOURCES / "catalog_parts" / "context.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    old = {}
    if out.exists():
        with open(out, newline="", encoding="utf-8") as f:
            old = {r["name"]: [r[c] for c in CATALOG_COLS] for r in csv.DictReader(f)}
    rows = [old.get(r[0], r) if "not probed this run" in r[-1] else r for r in catalog_rows(y)]
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(CATALOG_COLS)
        w.writerows(rows)
    return out


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true", help="re-download static reference files")
    ap.add_argument("--sf-fallback", action="store_true", help="download ACS Summary File tables (~750 MB)")
    ap.add_argument("--only", default="census,geo,geocode,omb,cpi")
    a = ap.parse_args()
    only = set(a.only.split(","))
    y = pl = bef = None
    steps = [("census", lambda: run_census(a.refresh, a.sf_fallback)),
             ("geo", lambda: run_geo(a.refresh, y, pl, bef)),
             ("geocode", run_geocode), ("omb", lambda: run_omb(a.refresh)), ("cpi", run_cpi),
             # ACS group pulls for config/extra_geographies.csv only (also included in "census")
             ("extra_geos", lambda: acs_pulls(BASE_YEAR, a.refresh, extra_geos(), "extra_geos"))]
    for name, fn in steps:
        if name not in only:
            continue
        try:
            res = fn()
            if name == "census":
                y, pl, bef = res
        except Exception as e:  # noqa: BLE001
            SUMMARY[name].append(f"- FAILED: {type(e).__name__}: {redact(str(e))[:300]}")
        log(f"16_probe_context: {name}", "\n".join(SUMMARY[name]) or "- nothing to report")
        print(f"[{name}]\n" + "\n".join(SUMMARY[name]))
    register_all()
    out = write_catalog(y)
    statuses = ", ".join(f"{k}={v['status']}" for k, v in RESULTS.items())
    log("16_probe_context: catalog", f"- wrote {rel(out)}\n- statuses: {statuses}")
    print(f"catalog -> {rel(out)}\n{statuses}")


if __name__ == "__main__":
    main()
