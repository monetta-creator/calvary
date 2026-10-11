"""Phase 5: build dimension tables (run after 62_build_facts.py).

dim_org          every EIN in a universe or referenced by a fact table; BMF attributes, latest e-filed profile
                 (interim/org_profile__xml.csv), geocodes (interim/stage_org_geo__context.csv), universes
dim_funder       every funder_id in fact_grants plus universe funders; type, geography, focus tags, totals
dim_period       from interim/stage_dim_period__context.csv
dim_geo          from interim/stage_dim_geo__context.csv
dim_program_area from config/program_areas.yaml

Usage: python scripts/63_build_dims.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import CLEAN, CONFIG, INTERIM, log, norm_ein, today
from lib.refdata import bmf_national
from lib.specs import columns

CORP_HINT = r"(?i)\b(corporate|company|bank|corp|inc foundation|llp|llc|group|financial|insurance|energy|resorts|" \
            r"capital one|wells fargo|pepsico|coca-cola|northrop|jpmorgan|morgan stanley|tiffany|intuit|workday)\b"


def read(p, **kw):
    return pd.read_csv(p, dtype=str, keep_default_na=False, low_memory=False, **kw) if Path(p).exists() else pd.DataFrame()


def build_dim_org(bmf, uni):
    facts = {t: read(CLEAN / f"{t}.csv") for t in ("fact_grants", "fact_gov_awards", "fact_org_financials")}
    eins = set(uni.ein)
    for t, cols in (("fact_grants", ["recipient_ein", "funder_ein"]), ("fact_gov_awards", ["recipient_ein"]),
                    ("fact_org_financials", ["ein"])):
        for c in cols:
            if c in facts[t]:
                eins |= set(facts[t][c].map(lambda e: norm_ein(e) or ""))
    eins.discard("")
    d = bmf[bmf.ein.isin(eins)].copy()
    missing = eins - set(d.ein)
    if missing:   # EINs referenced by facts but absent from the current BMF (revoked, merged, terminated)
        d = pd.concat([d, pd.DataFrame({"ein": sorted(missing)})], ignore_index=True)
    d = d.fillna("")
    out = pd.DataFrame({
        "ein": d.ein, "org_name_bmf": d.NAME, "dba_name": d.ICO, "street": d.STREET, "city": d.CITY, "state": d.STATE,
        "zip5": d.zip5, "ntee_cd": d.NTEE_CD, "ntee3": d.ntee3, "subsection": d.SUBSECTION,
        "foundation_code": d.FOUNDATION, "ruling_year": d.RULING.str[:4], "bmf_revenue_amt": d.REVENUE_AMT})
    out["org_class"] = np.select(
        [out.foundation_code.isin(["02", "03", "04"]), out.subsection == "03"],
        ["private_foundation", "public_charity"], default=np.where(out.subsection == "", "", "other_exempt"))
    # county from universe build (zip->county) when present
    geo_u = uni.drop_duplicates("ein").set_index("ein")[["county_fips", "geo_method"]]
    out = out.join(geo_u, on="ein")
    # geocodes
    g = read(INTERIM / "stage_org_geo__context.csv")
    if len(g):
        g = g.drop_duplicates("ein").set_index("ein")
        for c in ("county_fips", "ward", "tract_geoid", "lat", "lon", "geo_method"):
            if c in g:
                v = out.ein.map(g[c])
                out[c] = v.where(v.fillna("") != "", out.get(c))
        if "street_used" in g:
            v = out.ein.map(g["street_used"])
            out["street"] = v.where(v.fillna("") != "", out.street)
    # address overrides (office address where the BMF street is residential/mailing): scripts/47
    ovr = read(INTERIM / "org_geo_overrides.csv")
    if len(ovr):
        ovr = ovr.drop_duplicates("ein").set_index("ein")
        hit = out.ein.isin(ovr.index)
        for src, dst in (("street_used", "street"), ("county_fips", "county_fips"), ("tract_geoid", "tract_geoid"),
                         ("lat", "lat"), ("lon", "lon"), ("geo_method", "geo_method")):
            if src in ovr:
                out.loc[hit, dst] = out.loc[hit, "ein"].map(ovr[src])
        out.loc[hit, "ward"] = ""
    # latest e-filed profile
    prof = read(INTERIM / "org_profile__xml.csv")
    if len(prof):
        prof["ty"] = pd.to_numeric(prof.get("tax_year"), errors="coerce")
        prof = prof.sort_values("ty").drop_duplicates("ein", keep="last").set_index("ein")
        for src, dst in (("org_name", "org_name"), ("website", "website"), ("mission", "mission")):
            if src in prof:
                out[dst] = out.ein.map(prof[src])
    ix = read(INTERIM / "efile_index_universe.csv")
    if len(ix):
        ix["tpn"] = pd.to_numeric(ix.TAX_PERIOD, errors="coerce")
        last = ix.sort_values("tpn").drop_duplicates("ein", keep="last").set_index("ein")
        tp = out.ein.map(last.tpn)
        out["fye_month"] = (tp % 100).astype("Int64")
        out["latest_tax_year"] = np.where(tp % 100 == 12, tp // 100, tp // 100 - 1)
        out["latest_tax_year"] = pd.to_numeric(out.latest_tax_year, errors="coerce").astype("Int64")
        out["latest_return_type"] = out.ein.map(last.RETURN_TYPE)
    labels = read(CLEAN / "ref_ntee_codes.csv")
    if len(labels):
        out["ntee_label"] = out.ntee3.map(labels.set_index("ntee3").ntee_label)
    out["org_name"] = out.get("org_name", pd.Series("", index=out.index)).fillna("")
    out["org_name"] = out.org_name.where(out.org_name != "", out.org_name_bmf.str.title())
    out["universes"] = out.ein.map(uni.groupby("ein").universe.agg(lambda s: ";".join(sorted(set(s)))))
    out["is_calvary"] = (out.ein == "521307706").astype(int)
    out["source_id"] = "bulk_irs_eo_bmf;bulk_irs_xml_index;bulk_irs_xml"
    out["retrieved_date"] = today()
    return out.reindex(columns=columns("dim_org"))


def build_dim_funder(dim_org, uni):
    g = read(CLEAN / "fact_grants.csv")
    o = dim_org.set_index("ein")
    rows = []
    if len(g):
        g["amt"] = pd.to_numeric(g.amount, errors="coerce")
        g["cum"] = pd.to_numeric(g.cumulative_flag, errors="coerce").fillna(0)
        agg = g.groupby("funder_id").agg(ein=("funder_ein", "first"), name=("funder_name_raw", "first"),
                                         n_grants=("grant_id", "size"),
                                         total=("amt", lambda s: s[g.loc[s.index, "cum"] == 0].sum()),
                                         tags=("program_area_tags", lambda s: ";".join(
                                             pd.Series(";".join(s).split(";")).replace("", np.nan).dropna()
                                             .value_counts().head(5).index)),
                                         type_guess=("notes", lambda s: next(
                                             (x.split("funder_type_guess=")[1].split(";")[0] for x in s
                                              if "funder_type_guess=" in x), "")),
                                         srcs=("source_id", lambda s: ";".join(sorted(set(s))[:5])))
        rows.append(agg.reset_index())
    f = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame(columns=["funder_id", "ein"])
    # universe funders with no grant rows yet
    fu = uni[uni.universe.isin(["dmv_funders", "daf_sponsors", "calvary_known_funders"])].ein.unique()
    extra = sorted(set(fu) - set(f.ein))
    f = pd.concat([f, pd.DataFrame({"funder_id": extra, "ein": extra, "n_grants": 0, "total": 0})], ignore_index=True)
    f["ein"] = f.ein.fillna("")
    f["funder_name"] = f.ein.map(o.org_name_bmf).fillna("")
    f["funder_name"] = f.funder_name.where(f.funder_name != "", f.get("name", "")).fillna("")
    u_by = uni.groupby("ein").universe.agg(lambda s: ";".join(sorted(set(s))))
    rule_by = uni.groupby("ein").rule_id.agg(lambda s: set(s))
    ntee = f.ein.map(o.ntee3).fillna("")
    cls = f.ein.map(o.org_class).fillna("")
    rules = f.ein.map(rule_by)
    tg = f.get("type_guess", pd.Series("", index=f.index)).fillna("")
    conds = [
        rules.map(lambda r: isinstance(r, set) and "DAF1" in r),
        # BMF NTEE T21 ("Corporate Foundations") is unreliable (e.g. Cafritz, Wyss are coded T21), so use the name
        # or an inferred company-foundation link (universe rule KF2) instead
        (cls == "private_foundation") & (f.funder_name.str.contains(CORP_HINT, na=False) |
                                         rules.map(lambda r: isinstance(r, set) and "KF2" in r)),
        cls == "private_foundation",
        ntee == "T31",
        ntee == "T70",
        cls == "public_charity",
        tg.isin(["corporate", "corporation", "corporate_matching"]),
        tg.isin(["corporate_foundation"]),
        tg.isin(["government", "intergovernmental"]),
        tg.isin(["faith", "congregation"]),
        tg.isin(["civic", "association"]),
        tg.isin(["daf_sponsor"]),
        tg.isin(["foundation"]),
    ]
    vals = ["daf_sponsor", "corporate_foundation", "private_foundation", "community_foundation", "federated_giving",
            "public_charity_grantmaker", "corporate", "corporate_foundation", "government_agency", "faith",
            "civic_association", "daf_sponsor", "private_foundation"]
    f["funder_type"] = np.select(conds, vals, default="other")
    out = pd.DataFrame({
        "funder_id": f.funder_id, "ein": f.ein, "funder_name": f.funder_name, "funder_type": f.funder_type,
        "state": f.ein.map(o.state).fillna(""), "county_fips": f.ein.map(o.county_fips).fillna(""),
        "ward": f.ein.map(o.ward).fillna(""), "issue_focus_tags": f.get("tags", ""),
        "universes": f.ein.map(u_by).fillna(""), "n_grants": f.n_grants.fillna(0).astype(int),
        "total_grant_amount": pd.to_numeric(f.total, errors="coerce").fillna(0).round().astype("Int64"),
        "source_id": f.get("srcs", "").fillna("") if "srcs" in f else "", "retrieved_date": today()})
    return out.drop_duplicates("funder_id").reindex(columns=columns("dim_funder"))


def build_program_area():
    v = yaml.safe_load((CONFIG / "program_areas.yaml").read_text())
    return pd.DataFrame([{"program_area": k, "label": d.get("label", ""), "description": d.get("label", ""),
                          "keywords": ";".join(d.get("keywords", [])), "ntee3_codes": ";".join(d.get("ntee3", [])),
                          "assistance_listings": ";".join(d.get("assistance_listings", []))} for k, d in v.items()])


def main():
    bmf = bmf_national()
    uni = read(CLEAN / "dim_universe_membership.csv")
    dim_org = build_dim_org(bmf, uni)
    dims = {"dim_org": dim_org, "dim_funder": build_dim_funder(dim_org, uni),
            "dim_program_area": build_program_area()}
    for name, stage in (("dim_period", "stage_dim_period__context.csv"), ("dim_geo", "stage_dim_geo__context.csv")):
        s = read(INTERIM / stage)
        if name == "dim_geo" and "x_county_geoid" in s:
            # spec: county_fips is the 5-digit state+county code; the staging file carries 3-digit + x_county_geoid
            s["x_county_fips_3"] = s.county_fips
            s["county_fips"] = s.x_county_geoid.where(s.x_county_geoid != "", s.county_fips)
        dims[name] = s.reindex(columns=columns(name) + [c for c in s.columns if c not in columns(name)]) if len(s) else s
    lines = []
    for name, df in dims.items():
        df.to_csv(CLEAN / f"{name}.csv", index=False)
        lines.append(f"- {name}: {len(df):,} rows")
    log("63_build_dims", "\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
