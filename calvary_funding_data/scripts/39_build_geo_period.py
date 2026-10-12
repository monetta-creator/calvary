"""Phase 4 staging, area "context": dim_geo, dim_period and the DC tract->ward crosswalk.

Reads only files already pulled by scripts/16_probe_context.py (no network):
  raw/census/*_acs5_2024_{group}_{geo}.json   ACS 2020-2024 5-year group() pulls (11 groups x 9 geographies)
  raw/census/*_dec2020_pl_blocks_dc.json       2020 PL 94-171 block population / housing units (DC)
  raw/census/*_bef_sldu2022_11_DC.txt          2022 SLDU block equivalency file (block -> ward)
  config/dmv_counties.csv                       OMB 2023 CBSA 47900 county list
  config/cpi_u_annual.csv                       BLS CPI-U annual averages (US 2000-2025, DC metro 2015-2025)

Writes:
  interim/stage_dim_geo__context.csv     nation, states 11/24/51/54, CBSA 47900, DC/MD/VA MSA counties
                                         (+ WV 037 flagged out of scope), 8 DC wards, 206 DC tracts, plus the
                                         out-of-DMV geographies in config/extra_geographies.csv (named
                                         comparators' county and tract; x_outside_dmv = True)
  interim/tract_ward_crosswalk.csv       tract_geoid, ward, pop_weight (2020 block population weights)
  interim/stage_dim_period__context.csv  calendar years 2000-2027

Conventions used here:
  - Rates, shares and pct_* columns are proportions in [0, 1], not percents.
  - MOEs are 90% ACS MOEs. Derived MOEs follow the ACS handbook: sums use root-sum-of-squares
    (zero-estimate cells contribute only their single largest MOE); proportions use the proportion
    formula, falling back to the ratio formula when the radicand is negative.
  - MOE code -555555555 (controlled estimate) is read as 0. Other negative codes are read as missing.
  - Ward rows come straight from the ACS state-legislative-district (upper chamber) geography; the
    crosswalk is only for rolling tract-only measures up to wards.

Usage: .venv/bin/python scripts/39_build_geo_period.py [--no-notes]
"""
from __future__ import annotations

import csv
import json
import math
import re
import sys
from collections import defaultdict
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import CONFIG, INTERIM, append_md, latest_raw, log, rel, today

Y = 2024
VINTAGE = "2020-2024"
GROUPS = ["B01003", "B03002", "B09019", "B11001", "B17001", "B17012", "B18101", "B19013", "B21001",
          "B23025", "B25070"]
GEOS = ["us", "states", "cbsa47900", "dc_wards_sldu", "dc_tracts", "counties_dc", "counties_md",
        "counties_va", "counties_wv037"]
# out-of-DMV geographies (raw files written by scripts/16_probe_context.py --only extra_geos)
EXTRA = (pd.read_csv(CONFIG / "extra_geographies.csv", dtype=str, keep_default_na=False)
         if (CONFIG / "extra_geographies.csv").exists() else pd.DataFrame(columns=["geo_key"]))
EXTRA_BY_FILE = {f"xgeo_{r.geo_key}": r for r in EXTRA.itertuples(index=False)}
GEOS += list(EXTRA_BY_FILE)
STATE_ABBR = {"11": "DC", "24": "MD", "51": "VA", "54": "WV"}
SLDU = "state legislative district (upper chamber)"
CALVARY_TRACT = "11001007503"
OUT_GEO = INTERIM / "stage_dim_geo__context.csv"
OUT_XWALK = INTERIM / "tract_ward_crosswalk.csv"
OUT_PERIOD = INTERIM / "stage_dim_period__context.csv"
LOG = "39_build_geo_period"


# ---------------------------------------------------------------- ACS parsing
def stamp_date(p: Path) -> str:
    s = p.name[:8]
    return f"{s[:4]}-{s[4:6]}-{s[6:8]}"


def est_val(v):
    if v is None or v == "":
        return None
    x = float(v)
    return None if x < 0 else x   # all negative estimate values are Census annotation codes


def moe_val(v):
    if v is None or v == "":
        return None
    x = float(v)
    if x == -555555555:
        return 0.0                 # controlled estimate: no sampling error
    return None if x < 0 else x


def load_acs():
    """Return {GEO_ID: {"_geo": {...geography fields}, var: value}} and the list of raw files used."""
    data: dict[str, dict] = defaultdict(dict)
    files = []
    for g in GROUPS:
        for geo in GEOS:
            p = latest_raw("census", f"acs5_{Y}_{g}_{geo}.json")
            if p is None:
                raise SystemExit(f"missing raw ACS file for {g} {geo}; run scripts/16_probe_context.py")
            files.append(p)
            rows = json.loads(p.read_text(encoding="utf-8"))
            h = rows[0]
            for r in rows[1:]:
                rec = dict(zip(h, r))   # NAME appears twice; identical values
                gid = rec["GEO_ID"]
                d = data[gid]
                d.setdefault("_geo", {"geo_file": geo, "NAME": rec["NAME"],
                                      **{k: rec[k] for k in ("state", "county", "tract", SLDU,
                                         "metropolitan statistical area/micropolitan statistical area")
                                         if k in rec}})
                d.setdefault("_date", stamp_date(p))
                for k, v in rec.items():
                    if re.fullmatch(r"B\d{5}_\d{3}(E|M|EA|MA)", k):
                        d[k] = v
    return data, files


def E(d, v):
    return est_val(d.get(f"{v}E"))


def M(d, v):
    return moe_val(d.get(f"{v}M"))


def sum_est(d, vs):
    ests = [E(d, v) for v in vs]
    if any(x is None for x in ests):
        return None, None
    moes = [M(d, v) for v in vs]
    if any(m is None for m in moes):
        return sum(ests), None
    nz = [m for e, m in zip(ests, moes) if e != 0]
    z = [m for e, m in zip(ests, moes) if e == 0]
    sq = sum(m * m for m in nz) + (max(z) ** 2 if z else 0)
    return sum(ests), math.sqrt(sq)


def diff_est(a, am, b, bm):
    if a is None or b is None:
        return None, None
    return a - b, (math.sqrt(am * am + bm * bm) if am is not None and bm is not None else None)


def prop(num, num_m, den, den_m):
    if num is None or den is None or den <= 0:
        return None, None
    p = num / den
    if num_m is None or den_m is None:
        return p, None
    rad = num_m ** 2 - p ** 2 * den_m ** 2
    if rad < 0:
        rad = num_m ** 2 + p ** 2 * den_m ** 2
    return p, math.sqrt(rad) / den


def single(d, v):
    return E(d, v), M(d, v)


DISAB = [f"B18101_{i:03d}" for i in (4, 7, 10, 13, 16, 19, 23, 26, 29, 32, 35, 38)]
F_POV_ADULT = [f"B17001_{i:03d}" for i in range(24, 31)]
F_NONPOV_ADULT = [f"B17001_{i:03d}" for i in range(53, 60)]
BURDEN30 = [f"B25070_{i:03d}" for i in (7, 8, 9, 10)]


def indicators(d) -> dict:
    """Derived ACS indicators (estimate + MOE) for one geography."""
    out = {}

    def put(name, pair, nd=6):
        e, m = pair
        out[name] = None if e is None else round(e, nd)
        out[f"{name}_moe"] = None if m is None else round(m, nd)

    put("total_pop", single(d, "B01003_001"), 0)
    pov_u, pov_b = single(d, "B17001_001"), single(d, "B17001_002")
    put("poverty_rate", prop(*pov_b, *pov_u))
    f_b = single(d, "B17001_017")
    f_u = sum_est(d, ["B17001_017", "B17001_046"])
    put("female_poverty_rate", prop(*f_b, *f_u))
    put("median_hh_income", single(d, "B19013_001"), 0)
    rent_u = diff_est(*single(d, "B25070_001"), *single(d, "B25070_011"))
    b30 = sum_est(d, BURDEN30)
    b50 = single(d, "B25070_010")
    put("rent_burden_30plus_share", prop(*b30, *rent_u))
    put("rent_burden_50plus_share", prop(*b50, *rent_u))
    lf, un = single(d, "B23025_003"), single(d, "B23025_005")
    put("unemployment_rate", prop(*un, *lf))
    race_u = single(d, "B03002_001")
    put("pct_black_nh", prop(*single(d, "B03002_004"), *race_u))
    put("pct_hispanic", prop(*single(d, "B03002_012"), *race_u))
    put("pct_white_nh", prop(*single(d, "B03002_003"), *race_u))
    hh = single(d, "B11001_001")
    fhh = single(d, "B11001_006")
    put("female_hh_no_spouse_share", prop(*fhh, *hh))
    vet_u, vet = single(d, "B21001_001"), single(d, "B21001_002")
    put("veteran_share", prop(*vet, *vet_u))
    dis_u = single(d, "B18101_001")
    dis = sum_est(d, DISAB)
    put("disability_share", prop(*dis, *dis_u))

    # extras (x_): additional shares and the counts behind every rate, so rows can be re-aggregated
    asian = single(d, "B03002_006")
    other = sum_est(d, ["B03002_005", "B03002_007", "B03002_008", "B03002_009"])
    put("x_pct_asian_nh", prop(*asian, *race_u))
    put("x_pct_other_or_multi_nh", prop(*other, *race_u))
    fa_b = sum_est(d, F_POV_ADULT)
    fa_u = sum_est(d, F_POV_ADULT + F_NONPOV_ADULT)
    put("x_adult_female_poverty_rate", prop(*fa_b, *fa_u))
    fhf_b = single(d, "B17012_014")
    fhf_u = sum_est(d, ["B17012_014", "B17012_031"])
    put("x_female_hh_family_poverty_rate", prop(*fhf_b, *fhf_u))
    fv_u, fv = single(d, "B21001_022"), single(d, "B21001_023")
    put("x_female_veteran_share", prop(*fv, *fv_u))
    fla = single(d, "B09019_008")
    hhr = single(d, "B09019_003")
    put("x_female_living_alone_share_of_householders", prop(*fla, *hhr))
    counts = {
        "x_n_poverty_universe": pov_u, "x_n_below_poverty": pov_b,
        "x_n_female_poverty_universe": f_u, "x_n_female_below_poverty": f_b,
        "x_n_adult_female_poverty_universe": fa_u, "x_n_adult_female_below_poverty": fa_b,
        "x_n_renter_hh_computed": rent_u, "x_n_renter_hh_burden30plus": b30, "x_n_renter_hh_burden50plus": b50,
        "x_n_civilian_labor_force": lf, "x_n_unemployed": un,
        "x_n_race_universe": race_u, "x_n_black_nh": single(d, "B03002_004"),
        "x_n_hispanic": single(d, "B03002_012"), "x_n_white_nh": single(d, "B03002_003"),
        "x_n_households": hh, "x_n_female_hh_no_spouse_families": fhh,
        "x_n_female_hh_families_poverty_universe": fhf_u, "x_n_female_hh_families_below_poverty": fhf_b,
        "x_n_civilian_18plus": vet_u, "x_n_veterans": vet, "x_n_female_veterans": fv,
        "x_n_disability_universe": dis_u, "x_n_with_disability": dis,
    }
    for k, pair in counts.items():
        put(k, pair, 0)
    ea = d.get("B19013_001EA")
    out["x_median_hh_income_annotation"] = ea or None   # e.g. "250000+" top-code, "-" not computable
    return out


# ---------------------------------------------------------------- crosswalk
def build_crosswalk():
    pl = latest_raw("census", "dec2020_pl_blocks_dc.json")
    bef = latest_raw("census", "bef_sldu2022_11_DC.txt")
    if not pl or not bef:
        raise SystemExit("missing PL blocks or SLDU BEF raw file; run scripts/16_probe_context.py")
    rows = json.loads(pl.read_text(encoding="utf-8"))
    h = rows[0]
    ix = {c: h.index(c) for c in h}
    blocks = {r[ix["state"]] + r[ix["county"]] + r[ix["tract"]] + r[ix["block"]]:
              (int(r[ix["P1_001N"]]), int(r[ix["H1_001N"]])) for r in rows[1:]}
    with open(bef, encoding="utf-8") as f:
        b2w = {r["GEOID"]: int(r["SLDUST"]) for r in csv.DictReader(f)}
    agg = defaultdict(lambda: [0, 0, 0])   # (tract, ward) -> pop, hu, n_blocks
    no_ward = 0
    for b, (p, hu) in blocks.items():
        w = b2w.get(b)
        if w is None:
            no_ward += 1
            continue
        a = agg[(b[:11], w)]
        a[0] += p
        a[1] += hu
        a[2] += 1
    x = pd.DataFrame([(t, w, *v) for (t, w), v in agg.items()],
                     columns=["tract_geoid", "ward", "pop2020", "hu2020", "n_blocks"])
    tot = x.groupby("tract_geoid")[["pop2020", "hu2020", "n_blocks"]].transform("sum")
    x["pop_weight"] = x.pop2020 / tot.pop2020.where(tot.pop2020 > 0)
    x["hu_weight"] = x.hu2020 / tot.hu2020.where(tot.hu2020 > 0)
    x["weight_basis"] = "pop2020"
    # zero-population tracts (e.g. the Mall, parkland): fall back to housing units, then to block counts
    zp = tot.pop2020 == 0
    x.loc[zp, "pop_weight"] = x.loc[zp, "hu_weight"]
    x.loc[zp, "weight_basis"] = "hu2020"
    zz = zp & (tot.hu2020 == 0)
    x.loc[zz, "pop_weight"] = x.loc[zz, "n_blocks"] / tot.loc[zz, "n_blocks"]
    x.loc[zz, "weight_basis"] = "n_blocks"
    x = x[x.pop_weight > 0].copy()
    x["pop_weight"] = x.pop_weight.round(6)
    x["hu_weight"] = x.hu_weight.round(6)
    x["source_id"] = "api_census_dec_pl;bulk_census_bef_sldu2022"
    x["retrieved_date"] = stamp_date(pl)
    x["basis"] = "derived"
    x["confidence"] = "high"
    x = x.sort_values(["tract_geoid", "ward"])
    meta = {"n_blocks": len(blocks), "n_bef": len(b2w), "no_ward": no_ward, "pl": pl, "bef": bef}
    return x, meta


# ---------------------------------------------------------------- dim_geo
GEO_COLS = ["geo_id", "geo_level", "state_fips", "county_fips", "tract_geoid", "ward", "name", "acs_vintage"]
IND = ["total_pop", "poverty_rate", "female_poverty_rate", "median_hh_income", "rent_burden_30plus_share",
       "rent_burden_50plus_share", "unemployment_rate", "pct_black_nh", "pct_hispanic", "pct_white_nh",
       "female_hh_no_spouse_share", "veteran_share", "disability_share"]


def build_geo(data, xw):
    cty = pd.read_csv(CONFIG / "dmv_counties.csv", dtype=str)
    cty = cty[cty.cbsa_code == "47900"].set_index("county_geoid")
    maj = (xw.sort_values("pop_weight", ascending=False).drop_duplicates("tract_geoid")
           .set_index("tract_geoid"))
    nward = xw.groupby("tract_geoid").ward.nunique()
    rows = []
    for gid, d in data.items():
        g = d["_geo"]
        st = g.get("state")
        r = {"geo_id": gid, "name": g["NAME"], "acs_vintage": VINTAGE, "state_fips": st,
             "county_fips": None, "tract_geoid": None, "ward": None}
        src = "api_census_acs5"
        if gid == "0100000US":
            r.update(geo_level="nation", state_fips=None)
        elif g["geo_file"] == "states":
            r.update(geo_level="state", x_state_abbr=STATE_ABBR.get(st))
        elif g["geo_file"] == "cbsa47900":
            r.update(geo_level="msa", state_fips=None, x_cbsa_code="47900")
        elif g["geo_file"] == "dc_wards_sldu":
            r.update(geo_level="ward", county_fips="001", ward=int(g[SLDU]), x_county_geoid="11001",
                     x_in_service_area=int(g[SLDU]) in (7, 8))
        elif g["geo_file"] in EXTRA_BY_FILE:   # named comparator geographies outside the DMV
            x = EXTRA_BY_FILE[g["geo_file"]]
            cg = st + g["county"]
            r.update(geo_level=x.geo_level, county_fips=g["county"], x_county_geoid=cg, x_outside_dmv=True,
                     x_in_msa=False, x_named_comparator_ein=x.ein, x_scope_note=x.reason)
            if x.geo_level == "tract":
                r.update(tract_geoid=cg + g["tract"])
        elif g["geo_file"] == "dc_tracts":
            t = st + g["county"] + g["tract"]
            m = maj.loc[t] if t in maj.index else None
            r.update(geo_level="tract", county_fips=g["county"], tract_geoid=t, x_county_geoid=st + g["county"],
                     ward=None if m is None else int(m.ward),
                     x_ward_majority_pop_share=None if m is None else float(m.pop_weight),
                     x_split_ward=None if m is None else bool(nward.get(t, 1) > 1),
                     x_in_service_area=None if m is None else int(m.ward) in (7, 8))
            src = "api_census_acs5;api_census_dec_pl;bulk_census_bef_sldu2022"
        else:   # county files
            cg = st + g["county"]
            if cg not in cty.index:
                continue   # DC/MD/VA county outside CBSA 47900: not in scope for dim_geo
            c = cty.loc[cg]
            r.update(geo_level="county", county_fips=g["county"], x_county_geoid=cg, x_cbsa_code="47900",
                     x_in_msa=c.in_msa == "true", x_in_scope=c.in_scope == "true",
                     x_metro_division=c.metro_division, x_metro_division_code=c.metro_division_code,
                     x_central_outlying=c.central_outlying, x_scope_note=c.scope_note or None)
        if gid != "0100000US":
            r.setdefault("x_outside_dmv", False)
        r.update(indicators(d))
        r.update(source_id=src, retrieved_date=d["_date"], basis="derived",
                 confidence="medium" if r["geo_level"] == "tract" else "high")
        rows.append(r)
    df = pd.DataFrame(rows)
    order = {"nation": 0, "state": 1, "msa": 2, "county": 3, "ward": 4, "tract": 5}
    df["_o"] = df.geo_level.map(order)
    df = df.sort_values(["_o", "state_fips", "county_fips", "ward", "tract_geoid"]).drop(columns="_o")
    core = GEO_COLS + [c for i in IND for c in (i, f"{i}_moe")] + ["source_id", "retrieved_date", "confidence",
                                                                     "basis"]
    xcols = [c for c in df.columns if c.startswith("x_")]
    lead_x = [c for c in ["x_state_abbr", "x_county_geoid", "x_cbsa_code", "x_in_msa", "x_in_scope",
                          "x_metro_division", "x_metro_division_code", "x_central_outlying", "x_scope_note",
                          "x_ward_majority_pop_share", "x_split_ward", "x_in_service_area", "x_outside_dmv",
                          "x_named_comparator_ein"] if c in xcols]
    df = df[core + lead_x + [c for c in xcols if c not in lead_x]]
    for c in ["ward", "total_pop", "total_pop_moe", "median_hh_income", "median_hh_income_moe"] + \
            [c for c in xcols if c.startswith("x_n_")]:
        df[c] = df[c].astype("Int64")
    return df


# ---------------------------------------------------------------- dim_period
def build_period():
    cpi = pd.read_csv(CONFIG / "cpi_u_annual.csv", dtype={"year": int}).set_index("year")
    base_us = float(cpi.loc[2024, "cpi_u_us"])
    base_dc = float(cpi.loc[2024, "cpi_u_dc_metro"])
    bls_raw = latest_raw("bls", "cpi_*_2020_2025.json")
    retrieved = stamp_date(bls_raw) if bls_raw else today()
    rows = []
    for y in range(2000, 2028):
        has = y in cpi.index and pd.notna(cpi.loc[y, "cpi_u_us"])
        us = float(cpi.loc[y, "cpi_u_us"]) if has else None
        dc = float(cpi.loc[y, "cpi_u_dc_metro"]) if has and pd.notna(cpi.loc[y, "cpi_u_dc_metro"]) else None
        notes = []
        if not has:
            notes.append(f"CPI-U annual average not published as of {retrieved}; deflator blank")
        elif dc is None:
            notes.append("No published DC-metro (CUURS35ASA0) annual average before 2015; use the US series")
        if has and y in cpi.index and isinstance(cpi.loc[y, "notes"], str):
            notes.append(cpi.loc[y, "notes"])
        rows.append({
            "year": y,
            "cpi_u_us": us,
            "cpi_u_dc_metro": dc,
            "deflator_to_2024_us": round(base_us / us, 6) if us else None,
            # FY labels name the fiscal year ending Sep 30 of this calendar year (it covers Jan-Sep of Y);
            # Oct-Dec of calendar year Y falls in FY Y+1 (see the x_*_oct_dec columns).
            "federal_fy_label": f"FY{y}",
            "dc_fy_label": f"FY{y}",
            "calvary_fiscal_year_label": f"FY{y % 100:02d}",
            "notes": "; ".join(notes) or None,
            "source_id": "api_bls_cpi",
            "retrieved_date": retrieved,
            "confidence": "high",
            "basis": "derived",
            "x_deflator_to_2024_dc_metro": round(base_dc / dc, 6) if dc else None,
            "x_fy_jan_sep_fiscal_year": y,
            "x_fy_oct_dec_fiscal_year": y + 1,
            "x_federal_fy_oct_dec_label": f"FY{y + 1}",
            "x_dc_fy_oct_dec_label": f"FY{y + 1}",
            "x_calvary_fy_oct_dec_label": f"FY{(y + 1) % 100:02d}",
            "x_calvary_tax_year_jan_sep": y - 1,
            "x_calvary_tax_year_oct_dec": y,
            "x_cpi_us_series": "CUUR0000SA0" if us else None,
            "x_cpi_dc_series": "CUURS35ASA0" if dc else None,
        })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- QC + notes
def qc_and_notes(geo, xw, data, meta):
    lines, issues = [], []
    dup = geo.geo_id.duplicated().sum()
    lvl = geo.geo_level.value_counts().to_dict()
    lines.append(f"- dim_geo rows: {len(geo)} ({', '.join(f'{k}={v}' for k, v in lvl.items())}); "
                 f"duplicate geo_id: {dup}")
    if dup:
        issues.append(f"{dup} duplicate geo_id")
    dc = geo[(geo.geo_level == "state") & (geo.state_fips == "11")].iloc[0]
    wards = geo[geo.geo_level == "ward"].sort_values("ward")
    wsum = int(wards.total_pop.sum())
    pct = (wsum - dc.total_pop) / dc.total_pop * 100
    lines.append(f"- ward population sum {wsum:,} vs DC total {int(dc.total_pop):,} ({pct:+.2f}%)")
    if abs(pct) > 1:
        issues.append(f"ward pop sum off by {pct:.2f}%")
    tracts = geo[(geo.geo_level == "tract") & (geo.state_fips == "11")]   # DC tracts (extra geographies excluded)
    tsum = int(tracts.total_pop.sum())
    lines.append(f"- tracts: {len(tracts)}; tract population sum {tsum:,} "
                 f"({(tsum - dc.total_pop) / dc.total_pop * 100:+.2f}% vs DC)")
    # crosswalk check: tract B01003 allocated with pop weights vs ACS SLDU ward totals
    tp = tracts.set_index("tract_geoid").total_pop.astype(float)
    xa = xw.assign(v=xw.tract_geoid.map(tp) * xw.pop_weight).groupby("ward").v.sum()
    cmp_ = []
    worst = 0.0
    for _, w in wards.iterrows():
        a = xa.get(w.ward, 0)
        d = (a - w.total_pop) / w.total_pop * 100
        worst = max(worst, abs(d))
        cmp_.append(f"W{w.ward} {d:+.2f}%")
    lines.append(f"- crosswalk: {meta['n_blocks']:,} blocks, {meta['no_ward']} without a ward; "
                 f"{xw.tract_geoid.nunique()} tracts, {len(xw)} tract-ward rows, "
                 f"{int((xw.groupby('tract_geoid').ward.nunique() > 1).sum())} tracts split; "
                 f"weight bases {xw.drop_duplicates('tract_geoid').weight_basis.value_counts().to_dict()}")
    lines.append(f"- tract pop allocated to wards vs SLDU totals: {'; '.join(cmp_)} (max |diff| {worst:.2f}%)")
    wsum_chk = xw.groupby("tract_geoid").pop_weight.sum()
    if (wsum_chk - 1).abs().max() > 1e-4:
        issues.append("crosswalk weights do not sum to 1 for some tracts")
    cal = geo[geo.tract_geoid == CALVARY_TRACT]
    cal_w = None if cal.empty else cal.iloc[0].ward
    lines.append(f"- Calvary tract {CALVARY_TRACT}: majority ward {cal_w}, "
                 f"weights {xw[xw.tract_geoid == CALVARY_TRACT][['ward', 'pop_weight']].values.tolist()}")
    if cal_w != 8:
        issues.append(f"Calvary tract majority ward is {cal_w}, expected 8")
    for c in IND:
        n = geo[c].isna().sum()
        if n:
            lines.append(f"- {c}: {n} rows blank ({geo[geo[c].isna()].geo_level.value_counts().to_dict()})")
    if issues:
        lines.append("- **QC issues:** " + "; ".join(issues))
    else:
        lines.append("- QC: all checks passed")

    # analysis note: Wards 7/8 vs DC
    def fmt(r, c):
        return f"{r[c] * 100:.1f}% (±{r[c + '_moe'] * 100:.1f})"
    w = wards.set_index("ward")
    # Wards 7+8 combined from counts (MOE by root-sum-of-squares, proportion formula)
    def combo(num, den):
        n = w.loc[[7, 8], num].sum()
        dn = w.loc[[7, 8], den].sum()
        nm = math.sqrt((w.loc[[7, 8], num + "_moe"].astype(float) ** 2).sum())
        dm = math.sqrt((w.loc[[7, 8], den + "_moe"].astype(float) ** 2).sum())
        p, m = prop(float(n), nm, float(dn), dm)
        return f"{p * 100:.1f}% (±{m * 100:.1f})"
    note = [
        f"ACS {VINTAGE} 5-year, ward = Census SLDU (2022 wards). Rates are proportions in the CSV; "
        "shown here as % with 90% MOE.",
        f"- Poverty rate: Ward 7 {fmt(w.loc[7], 'poverty_rate')}, Ward 8 {fmt(w.loc[8], 'poverty_rate')}, "
        f"Wards 7+8 {combo('x_n_below_poverty', 'x_n_poverty_universe')}; DC {fmt(dc, 'poverty_rate')}.",
        f"- Female poverty rate: Ward 7 {fmt(w.loc[7], 'female_poverty_rate')}, "
        f"Ward 8 {fmt(w.loc[8], 'female_poverty_rate')}; DC {fmt(dc, 'female_poverty_rate')}.",
        f"- Rent burden 30%+ (renter households): Ward 7 {fmt(w.loc[7], 'rent_burden_30plus_share')}, "
        f"Ward 8 {fmt(w.loc[8], 'rent_burden_30plus_share')}, Wards 7+8 "
        f"{combo('x_n_renter_hh_burden30plus', 'x_n_renter_hh_computed')}; "
        f"DC {fmt(dc, 'rent_burden_30plus_share')}.",
        f"- Severe rent burden 50%+: Ward 7 {fmt(w.loc[7], 'rent_burden_50plus_share')}, "
        f"Ward 8 {fmt(w.loc[8], 'rent_burden_50plus_share')}; DC {fmt(dc, 'rent_burden_50plus_share')}.",
        f"- Unemployment: Ward 7 {fmt(w.loc[7], 'unemployment_rate')}, Ward 8 {fmt(w.loc[8], 'unemployment_rate')}"
        f"; DC {fmt(dc, 'unemployment_rate')}. Median HH income: Ward 7 ${int(w.loc[7].median_hh_income):,}, "
        f"Ward 8 ${int(w.loc[8].median_hh_income):,}, DC ${int(dc.median_hh_income):,}.",
        f"- Female householder, no spouse, share of households: Ward 8 {fmt(w.loc[8], 'female_hh_no_spouse_share')}"
        f" vs DC {fmt(dc, 'female_hh_no_spouse_share')}.",
        f"- Calvary's tract {CALVARY_TRACT}: poverty "
        f"{fmt(cal.iloc[0], 'poverty_rate')}, rent burden 30%+ {fmt(cal.iloc[0], 'rent_burden_30plus_share')}; "
        "tract MOEs are wide, so use ward rows for comparisons.",
        "- dim_geo `county_fips` is the 3-digit county code (per the context design); the 5-digit join key "
        "is `x_county_geoid`. Tract `ward` is the 2020-block-population majority ward "
        f"({int((xw.groupby('tract_geoid').ward.nunique() > 1).sum())} tracts span two or more wards; "
        "weights in interim/tract_ward_crosswalk.csv).",
    ]
    return lines, issues, note


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-notes", action="store_true", help="skip build-log and notes appends (test runs)")
    a = ap.parse_args()
    data, files = load_acs()
    xw, meta = build_crosswalk()
    geo = build_geo(data, xw)
    period = build_period()

    INTERIM.mkdir(parents=True, exist_ok=True)
    geo.to_csv(OUT_GEO, index=False)
    xw[["tract_geoid", "ward", "pop_weight", "pop2020", "hu2020", "hu_weight", "n_blocks", "weight_basis",
        "source_id", "retrieved_date", "confidence", "basis"]].to_csv(OUT_XWALK, index=False)
    period.to_csv(OUT_PERIOD, index=False)

    lines, issues, note = qc_and_notes(geo, xw, data, meta)
    lines.insert(0, f"- read {len(files)} ACS raw files (`raw/census/*_acs5_{Y}_*`), "
                    f"{rel(meta['pl'])}, {rel(meta['bef'])}")
    lines.append(f"- wrote {rel(OUT_GEO)} ({len(geo)} rows), {rel(OUT_XWALK)} ({len(xw)} rows), "
                 f"{rel(OUT_PERIOD)} ({len(period)} rows: {period.cpi_u_us.notna().sum()} with US CPI, "
                 f"{period.cpi_u_dc_metro.notna().sum()} with DC-metro CPI; 2026-2027 blank, not published)")
    if not a.no_notes:
        log(LOG, "\n".join(lines))
        append_md("notes_for_analysis.md", "Geo/context build", "\n".join(note))
    print("\n".join(lines))
    print("\n".join(note))
    if issues:
        sys.exit(1)


if __name__ == "__main__":
    main()
