"""Phase 3: build the comparison universes from the IRS EO BMF and the IRS e-file index.

Inputs (raw/, config/):
  raw/irs_bmf/*_eo{1..4}.csv           national BMF (latest copy of each)
  raw/irs_bmf/*_eo-info.pdf            IRS BMF documentation (NTEE labels)
  raw/irs_xml_index/*_index_{2021..2026}.csv
  raw/geo/*_census_zcta520_county20.txt  (downloaded here if absent)
  config/universes.yaml, funder_pins.csv, daf_sponsors.csv, dmv_counties.csv, named_comparators.csv,
  ntee_supplement.csv
  config/core_peers.csv                (optional; approved peer list from Checkpoint 2)
  interim/known_funder_matches.csv     (optional; from scripts/22_match_known_funders.py)

Outputs:
  clean/dim_universe_membership.csv    one row per (universe, ein, rule_id)
  clean/ref_ntee_codes.csv             NTEE 3-character codes and IRS labels
  interim/org_base.csv                 BMF + e-file attributes for every universe EIN (input to later phases)
  interim/efile_index_universe.csv     e-file index rows (TY2020+ periods) for universe EINs
  reports/universe_summary.md          counts by universe and rule

Usage: python scripts/20_build_universes.py [--refresh-geo]
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import (CLEAN, CONFIG, INTERIM, REPORTS, latest_raw, log, norm_ein, register_source,
                        save_raw, session, today)

ZCTA_URL = "https://www2.census.gov/geo/docs/maps-data/data/rel2020/zcta520/tab20_zcta520_county20_natl.txt"
BMF_COLS = ["EIN", "NAME", "ICO", "STREET", "CITY", "STATE", "ZIP", "SUBSECTION", "FOUNDATION", "RULING",
            "NTEE_CD", "REVENUE_AMT", "ASSET_AMT", "INCOME_AMT", "TAX_PERIOD", "FILING_REQ_CD", "PF_FILING_REQ_CD"]


# ---------------------------------------------------------------- loaders
def load_bmf() -> pd.DataFrame:
    frames = []
    for region in ("eo1.csv", "eo2.csv", "eo3.csv", "eo4.csv"):
        p = latest_raw("irs_bmf", region)
        if p is None:
            sys.exit(f"missing raw/irs_bmf/*_{region}; run scripts/10_probe_filings.py --only bmf")
        frames.append(pd.read_csv(p, dtype=str, usecols=BMF_COLS, keep_default_na=False))
    b = pd.concat(frames, ignore_index=True)
    b["ein"] = b.EIN.map(norm_ein)
    b = b.drop_duplicates("ein")
    b["ntee3"] = b.NTEE_CD.str[:3]
    b["zip5"] = b.ZIP.str[:5]
    for c in ("REVENUE_AMT", "ASSET_AMT", "INCOME_AMT", "TAX_PERIOD"):
        b[c] = pd.to_numeric(b[c].replace("", None), errors="coerce")
    return b


def load_index() -> pd.DataFrame:
    frames = []
    for yr in range(2021, 2027):
        p = latest_raw("irs_xml_index", f"index_{yr}.csv")
        if p is None:
            continue
        d = pd.read_csv(p, dtype=str, keep_default_na=False,
                        usecols=lambda c: c in {"EIN", "TAX_PERIOD", "SUB_DATE", "RETURN_TYPE", "OBJECT_ID", "XML_BATCH_ID",
                                                "TAXPAYER_NAME"})
        d["release_year"] = yr
        frames.append(d)
    ix = pd.concat(frames, ignore_index=True)
    ix = ix[ix.RETURN_TYPE.isin(["990", "990EZ", "990PF"])]
    ix["ein"] = ix.EIN.map(norm_ein)
    ix["tp"] = pd.to_numeric(ix.TAX_PERIOD, errors="coerce")
    return ix


def ntee_labels() -> pd.DataFrame:
    pdf = latest_raw("irs_bmf", "eo-info.pdf")
    txt = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True).stdout
    start = txt.find("National Taxonomy of Exempt Entities (NTEE) Code is a four-digit")
    rows = {}
    for line in txt[start:].splitlines():
        for code, label in re.findall(r"\b([A-Z]\d{2})\s{2,}(.+?)(?=\s+[A-Z]\d{2}\s{1,}|$)", line):
            rows.setdefault(code, label.strip())
    return pd.DataFrame(sorted(rows.items()), columns=["ntee3", "ntee_label"]).assign(
        major_group=lambda d: d.ntee3.str[0], source_id="bulk_irs_eo_bmf")


def zip_to_county(refresh: bool) -> pd.DataFrame:
    p = latest_raw("geo", "census_zcta520_county20.txt")
    if p is None or refresh:
        r = session().get(ZCTA_URL, timeout=120)
        r.raise_for_status()
        p = save_raw("geo", "census_zcta520_county20", r.content, "txt")
        register_source("bulk_census_zcta_county_2020", "Census 2020 ZCTA to County Relationship File", ZCTA_URL,
                        "U.S. Census Bureau", "Public domain (U.S. Census Bureau)",
                        "Used to assign BMF ZIP codes to a primary county (largest land-area overlap)")
    z = pd.read_csv(p, sep="|", dtype=str, keep_default_na=False)
    z = z[z.GEOID_ZCTA5_20 != ""]
    z["land"] = pd.to_numeric(z.AREALAND_PART, errors="coerce")
    z = z.sort_values("land", ascending=False).drop_duplicates("GEOID_ZCTA5_20")
    return z.rename(columns={"GEOID_ZCTA5_20": "zip5", "GEOID_COUNTY_20": "county_fips"})[["zip5", "county_fips"]]


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh-geo", action="store_true")
    a = ap.parse_args()
    cfg = yaml.safe_load((CONFIG / "universes.yaml").read_text())
    nt = cfg["ntee"]
    core, adj = set(nt["core"]), set(nt["adjacent"])
    min_tp = cfg["recent_filing"]["min_tax_period"]

    bmf = load_bmf()
    ix = load_index()
    labels = ntee_labels()
    sup = CONFIG / "ntee_supplement.csv"   # valid NTEE codes missing from the IRS table (e.g. P83)
    if sup.exists():
        extra = pd.read_csv(sup, dtype=str)[["ntee3", "ntee_label", "major_group", "source_id"]]
        labels = pd.concat([labels, extra[~extra.ntee3.isin(labels.ntee3)]], ignore_index=True).sort_values("ntee3")
    labels.to_csv(CLEAN / "ref_ntee_codes.csv", index=False)

    # latest e-filed return per EIN
    last = (ix.sort_values(["tp", "SUB_DATE"]).groupby("ein").tail(1)
            .set_index("ein")[["tp", "RETURN_TYPE"]]
            .rename(columns={"tp": "latest_efile_tax_period", "RETURN_TYPE": "latest_efile_return_type"}))
    bmf = bmf.join(last, on="ein")
    bmf["recent_filing"] = (bmf.TAX_PERIOD.fillna(0) >= min_tp) | (bmf.latest_efile_tax_period.fillna(0) >= min_tp)

    # geography: DC is one county; others by ZIP->ZCTA primary county
    z2c = zip_to_county(a.refresh_geo)
    bmf = bmf.merge(z2c, on="zip5", how="left")
    bmf.loc[bmf.STATE == "DC", "county_fips"] = "11001"
    bmf["geo_method"] = bmf.county_fips.notna().map({True: "zcta_primary_county", False: "unresolved"})
    bmf.loc[bmf.STATE == "DC", "geo_method"] = "state_dc"
    # PO-box ZIPs have no ZCTA: fall back to the modal county of resolved orgs in the same city+state
    resolved = bmf[bmf.geo_method == "zcta_primary_county"]
    modal = (resolved.groupby(["STATE", "CITY"]).county_fips
             .agg(lambda s: s.value_counts().index[0]).rename("city_county"))
    bmf = bmf.join(modal, on=["STATE", "CITY"])
    fb = (bmf.geo_method == "unresolved") & bmf.city_county.notna()
    bmf.loc[fb, "county_fips"] = bmf.loc[fb, "city_county"]
    bmf.loc[fb, "geo_method"] = "city_modal_county"
    bmf = bmf.drop(columns=["city_county"])
    msa = pd.read_csv(CONFIG / "dmv_counties.csv", dtype=str)
    msa_fips = set(msa[(msa.in_msa == "true") & (msa.in_scope == "true")].county_geoid)
    bmf["in_dc_msa"] = bmf.county_fips.isin(msa_fips)

    pc = (bmf.SUBSECTION == cfg["public_charity"]["subsection"]) & ~bmf.FOUNDATION.isin(
        cfg["public_charity"]["exclude_foundation_codes"])
    pf = bmf.FOUNDATION.isin(cfg["private_foundation"]["foundation_codes"]) | (
        bmf.PF_FILING_REQ_CD == cfg["private_foundation"]["or_pf_filing_req_cd"])
    sector = bmf.ntee3.isin(core | adj)
    rec = bmf.recent_filing
    dmv_states = cfg["geo"]["dmv_states"]
    women_re = re.compile(cfg["women_name_regex"])
    dvh_re = re.compile(cfg["dv_housing_name_regex"])

    cal = cfg["calvary"]
    med = float(pd.Series(list(cal["revenue_by_tax_year"].values())).median())
    lo, hi = (round(med * m) for m in cal["size_band_multipliers"])

    rules = {}
    rules["SUBJ"] = bmf.ein == cal["ein"]
    rules["DCS1"] = (bmf.STATE == "DC") & pc & sector & rec
    rules["DCS2"] = (bmf.STATE == "DC") & pc & sector & ~rec
    rules["DMV1"] = bmf.STATE.isin(dmv_states) & bmf.in_dc_msa & pc & sector & rec
    rules["DMV2"] = bmf.STATE.isin(dmv_states) & bmf.in_dc_msa & pc & sector & ~rec
    rules["NW1"] = pc & (bmf.ntee3 == "P43") & rec
    rules["NW2"] = pc & bmf.ntee3.isin(nt["women_name_codes"]) & bmf.NAME.str.contains(women_re) & rec
    rules["NW3"] = pc & (bmf.ntee3 == "I71") & bmf.NAME.str.contains(dvh_re) & rec
    rules["NW4"] = pc & (bmf.ntee3 == "P83") & rec
    rules["SZ1"] = pc & bmf.ntee3.isin(nt["shelter_dv"]) & bmf.REVENUE_AMT.between(lo, hi) & rec
    rules["F1"] = bmf.STATE.isin(dmv_states) & pf
    rules["F2"] = bmf.STATE.isin(dmv_states) & pc & bmf.ntee3.isin(nt["grantmaking_pc"]) & rec
    pins = pd.read_csv(CONFIG / "funder_pins.csv", dtype=str)
    dafs = pd.read_csv(CONFIG / "daf_sponsors.csv", dtype=str)
    # pinned EINs absent from the BMF (e.g. filers listed only in the e-file index) get a stub row
    stubs = []
    for df_, st_col in ((pins, None), (dafs, "hq_state")):
        for r in df_.itertuples():
            e = norm_ein(r.ein)
            if e not in set(bmf.ein):
                stubs.append({"ein": e, "NAME": r.name.upper(), "STATE": getattr(r, st_col) if st_col else "",
                              "geo_method": "not_in_bmf", "recent_filing": e in set(ix.ein),
                              "in_dc_msa": False})
    if stubs:
        bmf = pd.concat([bmf, pd.DataFrame(stubs)], ignore_index=True)
        for k in list(rules):
            rules[k] = rules[k].reindex(bmf.index, fill_value=False)
        pc, pf, sector, rec = (s.reindex(bmf.index, fill_value=False) for s in (pc, pf, sector, rec))
    rules["F3"] = bmf.ein.isin(pins.ein.map(norm_ein))
    rules["DAF1"] = bmf.ein.isin(dafs.ein.map(norm_ein))
    kf_path = INTERIM / "known_funder_matches.csv"
    if kf_path.exists():
        kf = pd.read_csv(kf_path, dtype=str)
        rules["KF1"] = bmf.ein.isin(kf[kf.accept == "yes"].ein.map(norm_ein))
        rules["KF2"] = bmf.ein.isin(kf[kf.accept == "inferred"].ein.map(norm_ein)) & ~rules["KF1"]
    nc = pd.read_csv(CONFIG / "named_comparators.csv", dtype=str)
    rules["NC1"] = bmf.ein.isin(nc.ein.map(norm_ein))
    cp_path = CONFIG / "core_peers.csv"
    if cp_path.exists():
        cp = pd.read_csv(cp_path, dtype=str)
        rules["CP1"] = bmf.ein.isin(cp.ein.map(norm_ein))

    rule_meta = {r["rule_id"]: (u, r["desc"]) for u, rs in cfg["universes"].items() for r in rs}
    out = []
    for rid, mask in rules.items():
        uni, desc = rule_meta[rid]
        sub = bmf[mask.fillna(False)].copy()
        sub["universe"], sub["rule_id"], sub["criteria"] = uni, rid, desc
        out.append(sub)
    m = pd.concat(out, ignore_index=True)

    # pinned EINs missing from the BMF are reported, not silently dropped
    missing = {rid: sorted(set(ids) - set(bmf.ein)) for rid, ids in
               {"F3": pins.ein.map(norm_ein), "DAF1": dafs.ein.map(norm_ein)}.items()}

    keep = ["universe", "ein", "rule_id", "criteria", "NAME", "CITY", "STATE", "zip5", "county_fips", "geo_method",
            "in_dc_msa", "NTEE_CD", "ntee3", "SUBSECTION", "FOUNDATION", "RULING", "REVENUE_AMT", "ASSET_AMT",
            "TAX_PERIOD", "latest_efile_tax_period", "latest_efile_return_type", "recent_filing"]
    m = m[keep].rename(columns={
        "NAME": "org_name_bmf", "CITY": "city", "STATE": "state", "NTEE_CD": "ntee_cd", "SUBSECTION": "subsection",
        "FOUNDATION": "foundation_code", "RULING": "ruling_yyyymm", "REVENUE_AMT": "bmf_revenue_amt",
        "ASSET_AMT": "bmf_asset_amt", "TAX_PERIOD": "bmf_tax_period"})
    for c in ("bmf_revenue_amt", "bmf_asset_amt", "bmf_tax_period", "latest_efile_tax_period"):
        m[c] = m[c].astype("Int64")
    m["source_id"] = "bulk_irs_eo_bmf;bulk_irs_xml_index"
    m["retrieved_date"] = today()
    m["basis"] = "derived"
    m["confidence"] = "high"
    m.loc[m.rule_id.isin(["NW2", "NW3"]), "confidence"] = "medium"  # name-keyword rules
    m.loc[m.rule_id.isin(["DCS2", "DMV2"]), "confidence"] = "medium"
    m.loc[m.rule_id == "KF2", "confidence"] = "low"
    m = m.sort_values(["universe", "rule_id", "ein"])
    m.to_csv(CLEAN / "dim_universe_membership.csv", index=False)

    # org base + e-file rows for every universe EIN (used by Phase 4 pulls)
    eins = set(m.ein)
    base = bmf[bmf.ein.isin(eins)].drop(columns=["EIN"])
    base.to_csv(INTERIM / "org_base.csv", index=False)
    ixu = ix[ix.ein.isin(eins) & (ix.tp >= 202012)]
    ixu.drop(columns=["EIN"]).to_csv(INTERIM / "efile_index_universe.csv", index=False)

    # summary
    cnt = m.groupby(["universe", "rule_id"]).ein.nunique().rename("eins").reset_index()
    uni_cnt = m.groupby("universe").ein.nunique()
    lines = ["# Universe summary", "",
             f"Built {today()} by `scripts/20_build_universes.py` from the IRS EO BMF and IRS e-file index "
             "(releases 2021–2026). Rules live in `config/universes.yaml`.", "",
             f"- Calvary revenue median TY2022–24: ${med:,.0f}; size band ${lo:,.0f}–${hi:,.0f}.",
             f"- Recent filing = BMF TAX_PERIOD or e-filed return period ≥ {min_tp}.",
             f"- ZIP→county: Census 2020 ZCTA–county relationship, primary county by land area. "
             f"Unresolved ZIPs among DMV-state rows: {int(((m.state != 'DC') & m.state.isin(dmv_states) & (m.geo_method == 'unresolved')).sum())}.",
             "", "| Universe | Rule | EINs |", "|---|---|---|"]
    lines += [f"| {r.universe} | {r.rule_id} | {r.eins:,} |" for r in cnt.itertuples()]
    lines += ["", "| Universe | Distinct EINs |", "|---|---|"]
    lines += [f"| {u} | {n:,} |" for u, n in uni_cnt.items()]
    lines += ["", f"Distinct EINs across all universes: {len(eins):,}. "
              f"E-file returns (periods ending 2020-12+) for these EINs: {len(ixu):,}."]
    if any(missing.values()):
        lines += ["", f"Pinned EINs not found in BMF: {missing}"]
    (REPORTS / "universe_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    log("20_build_universes", "\n".join(f"- {u}: {n:,} EINs" for u, n in uni_cnt.items()) +
        f"\n- membership rows {len(m):,}; distinct EINs {len(eins):,}; e-file rows {len(ixu):,}; "
        f"size band ${lo:,}–${hi:,}; missing pins {missing}")
    print(cnt.to_string(index=False))
    print(uni_cnt.to_string())


if __name__ == "__main__":
    main()
