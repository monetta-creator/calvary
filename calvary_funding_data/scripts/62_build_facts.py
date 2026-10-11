"""Phase 5: union staging files into clean fact tables.

For each fact table, every interim/stage_{table}__*.csv is unioned and coerced to the spec column order
(scripts/lib/specs.py). Source-specific x_* columns are folded into a `notes` column as key=value pairs.
Then:
  - recipient/funder EINs are filled from interim/name_resolution.csv (scripts/61), with match_method/score
  - stable row ids are assigned (hash of identifying fields + occurrence index)
  - *_real_2024 columns use dim_period deflators (CPI-U US, base 2024)
  - fact_org_financials: preferred row per ein+fiscal_year, conflict_flag, derived ratios
Supplementary staging files (stage_supp_*, stage_homeless_counts__*, stage_hic_projects__*,
stage_dc_budget_lines__*) are copied to clean/supp_*.csv.

Usage: python scripts/62_build_facts.py
"""
import hashlib
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import CLEAN, CONFIG, INTERIM, log, norm_ein, norm_name
from lib.refdata import city_norm
def fold_notes(df, xcols):
    """Fold x_* columns into one 'k=v; k=v' string per row (vectorized)."""
    out = pd.Series("", index=df.index)
    for c in xcols:
        v = df[c].fillna("").astype(str).fillna("")   # pandas 3 keeps NaN through astype(str)
        keep = ~v.isin(["", "nan", "<NA>", "None"])
        piece = (c[2:] + "=" + v).where(keep, "")
        sep = pd.Series(np.where((out != "") & keep, "; ", ""), index=df.index)
        out = out + sep + piece
    return out


from lib.specs import SPECS, columns

# preferred-row ranking: e-filed XML, then NCCS e-file tables (carry Part VIII detail incl. government grants),
# then ProPublica / SOI (same SOI fields), then Calvary's 990 PDFs, then audits (GAAP basis)
SOURCE_RANK = [("bulk_irs_xml", 1), ("bulk_gt_datalake", 1), ("bulk_nccs_efile", 2), ("api_propublica", 3),
               ("bulk_irs_soi_extract", 4), ("input_990", 5), ("input_propublica_990", 5), ("input_", 6)]
INT_HINT = {c for t in SPECS.values() for c, typ, *_ in t if typ == "int"}


def h(*parts) -> str:
    return hashlib.sha1("|".join("" if p is None or (isinstance(p, float) and np.isnan(p)) else str(p)
                                 for p in parts).encode()).hexdigest()[:12]


def union_stage(table: str) -> pd.DataFrame:
    frames = []
    for p in sorted(INTERIM.glob(f"stage_{table}__*.csv")):
        d = pd.read_csv(p, dtype=str, keep_default_na=False, low_memory=False)
        d["x_stage_file"] = p.name
        frames.append(d)
    if not frames:
        return pd.DataFrame(columns=columns(table))
    return pd.concat(frames, ignore_index=True)


def finalize(df: pd.DataFrame, table: str) -> pd.DataFrame:
    cols = columns(table)
    xcols = [c for c in df.columns if c.startswith("x_") and c != "x_stage_file"]
    notes = fold_notes(df, xcols) if xcols else ""
    out = df.reindex(columns=cols)
    out["notes"] = notes
    for c in cols:
        if c in INT_HINT:
            out[c] = pd.to_numeric(out[c].replace("", np.nan), errors="coerce").round().astype("Int64")
    return out


def deflators() -> dict:
    p = INTERIM / "stage_dim_period__context.csv"
    if p.exists():
        d = pd.read_csv(p)
    else:
        d = pd.read_csv(CONFIG / "cpi_u_annual.csv")
        d["deflator_to_2024_us"] = d.loc[d.year == 2024, "cpi_u_us"].iloc[0] / d.cpi_u_us
    return dict(zip(d.year.astype(int), pd.to_numeric(d.deflator_to_2024_us, errors="coerce")))


def real(amount: pd.Series, year: pd.Series, defl: dict) -> pd.Series:
    f = pd.to_numeric(year, errors="coerce").map(defl)
    return (pd.to_numeric(amount, errors="coerce") * f).round().astype("Int64")


def resolver():
    p = INTERIM / "name_resolution.csv"
    if not p.exists():
        return {}
    r = pd.read_csv(p, dtype=str, keep_default_na=False)
    r = r[r.ein != ""]
    return {(x.role, x.name_norm, x.city_norm, x.state): (x.ein, x.match_method, x.match_score)
            for x in r.itertuples()}


def resolve_col(df, role, name_col, city_col, state_col, ein_col, res):
    names = df[name_col].fillna("").map(norm_name)
    cities = city_norm(df[city_col]) if city_col in df else pd.Series("", index=df.index)
    states = df[state_col].fillna("").str.upper().str.strip() if state_col in df else pd.Series("", index=df.index)
    given = df[ein_col].fillna("").map(lambda e: norm_ein(e) or "") if ein_col in df else pd.Series("", index=df.index)
    keys = list(zip([role] * len(df), names, cities, states))
    hit = [res.get(k) for k in keys]
    ein = [g or (x[0] if x else "") for g, x in zip(given, hit)]
    meth = ["given" if g else (x[1] if x else "unmatched") for g, x in zip(given, hit)]
    score = ["" if g else (x[2] if x else "") for g, x in zip(given, hit)]
    return ein, meth, score


# ------------------------------------------------------------------ tables
def build_financials(defl):
    df = union_stage("fact_org_financials")
    if df.empty:
        return df
    df["ein"] = df.ein.map(norm_ein)
    rank = df.source_id.map(lambda s: next((r for k, r in SOURCE_RANK if str(s).startswith(k)), 9))
    df["_rank"] = rank
    for c in ("total_revenue", "fiscal_year"):
        df[c] = pd.to_numeric(df[c].replace("", np.nan), errors="coerce")
    df = df.drop_duplicates(["ein", "fiscal_year", "fye_month", "return_type", "source_id", "object_id"], keep="last")
    df = df.sort_values(["ein", "fiscal_year", "_rank", "tax_period_end"])
    # one preferred row per ein + fiscal_year (+fye_month, for orgs that changed fiscal year)
    df["preferred"] = (~df.duplicated(["ein", "fiscal_year", "fye_month"])).astype(int)
    rng = df.groupby(["ein", "fiscal_year"]).total_revenue.agg(["min", "max"])
    conflict = (rng["max"] - rng["min"]).abs() > 0.01 * rng["max"].abs().clip(lower=1)
    df["conflict_flag"] = df.set_index(["ein", "fiscal_year"]).index.map(conflict).fillna(False).astype(int)
    out = finalize(df, "fact_org_financials")
    out["preferred"] = df.preferred.values
    pref = out.preferred == 1
    num = lambda c: pd.to_numeric(out[c], errors="coerce").astype(float)
    with np.errstate(divide="ignore", invalid="ignore"):
        out.loc[pref, "gov_share_of_revenue"] = (num("government_grants") / num("total_revenue")).where(pref).round(4)
        out.loc[pref, "months_of_cash"] = (num("cash_savings_eoy") / (num("total_expenses") / 12)).where(pref).round(2)
        out.loc[pref, "program_expense_ratio"] = (num("program_expenses") / num("total_expenses")).where(pref).round(4)
        p = out[pref].sort_values(["ein", "fiscal_year"])
        prev = p.groupby("ein").total_revenue.shift(1).astype(float)
        gap = p.fiscal_year.astype(float) - p.groupby("ein").fiscal_year.shift(1).astype(float)
        growth = (p.total_revenue.astype(float) / prev - 1).where(gap == 1)
        out.loc[growth.index, "revenue_growth_yoy"] = growth.round(4)
    for c in ("gov_share_of_revenue", "months_of_cash", "program_expense_ratio", "revenue_growth_yoy"):
        out[c] = out[c].replace([np.inf, -np.inf], np.nan)
    for c in ("total_revenue", "government_grants", "total_expenses"):
        out[f"{c}_real_2024"] = real(out[c], out.fiscal_year, defl)
    return out


def build_grants(defl, res):
    df = union_stage("fact_grants")
    if df.empty:
        return df
    e, m, s = resolve_col(df, "recipient", "recipient_name_raw", "recipient_city", "recipient_state",
                          "recipient_ein", res)
    df["recipient_ein"], df["match_method"], df["match_score"] = e, m, s
    fe, fm, fs = resolve_col(df, "funder", "funder_name_raw", "x_funder_city", "x_funder_state", "funder_ein", res)
    df["funder_ein"] = fe
    df["x_funder_match_method"] = fm
    df["funder_id"] = [f if f else "F" + hashlib.sha1(norm_name(n).encode()).hexdigest()[:10]
                       for f, n in zip(df.funder_ein, df.funder_name_raw.fillna(""))]
    # second-pass redaction of individuals among recipients that did not resolve to an EIN (lib/privacy.py)
    from lib.privacy import REDACTED, person_like
    pl = (df.recipient_ein == "") & df.source_type.isin(["pf_grants_paid", "pf_grants_approved_future", "schedule_i"]) \
        & df.recipient_name_raw.map(person_like)
    df.loc[pl, "recipient_name_raw"] = REDACTED
    for c in ("recipient_city", "recipient_zip5"):
        if c in df:
            df.loc[pl, c] = ""
    df.loc[pl, "x_redacted_individual"] = "1"
    df.loc[pl, "match_method"] = "redacted_individual"
    df["recipient_name_norm"] = df.recipient_name_raw.fillna("").map(norm_name)
    df.loc[pl, "recipient_name_norm"] = ""
    key = df[["source_id", "object_id", "funder_id", "recipient_name_norm", "amount", "fiscal_year", "source_type"]] \
        .astype(str).agg("|".join, axis=1)
    occ = key.groupby(key).cumcount()
    df["grant_id"] = ["G" + h(k, o) for k, o in zip(key, occ)]
    out = finalize(df, "fact_grants")
    yr = out.fiscal_year.astype("Float64").fillna(
        pd.to_numeric(df.grant_date.str[:4], errors="coerce").astype("Float64"))
    out["amount_real_2024"] = real(out.amount, yr, defl)
    return out


def build_gov_awards(defl, res):
    df = union_stage("fact_gov_awards")
    if df.empty:
        return df
    if "x_recipient_state" not in df:
        df["x_recipient_state"] = ""
    dc = df.x_stage_file.str.contains("__dc") & (df.x_recipient_state.fillna("") == "")
    df.loc[dc, "x_recipient_state"] = "DC"   # same default as scripts/61
    e, m, s = resolve_col(df, "recipient", "recipient_name_raw", "x_recipient_city", "x_recipient_state",
                          "recipient_ein", res)
    df["recipient_ein"] = e
    df["x_recipient_match_method"] = m
    key = df[["source_type", "source_id", "award_id", "recipient_name_raw", "assistance_listing", "fiscal_year",
              "amount", "flow_type"]].astype(str).agg("|".join, axis=1)
    df["award_row_id"] = ["A" + h(k, o) for k, o in zip(key, key.groupby(key).cumcount())]
    out = finalize(df, "fact_gov_awards")
    out["amount_real_2024"] = real(out.amount, out.fiscal_year, defl)
    return out


def build_simple(table, id_col, prefix, id_fields):
    df = union_stage(table)
    if df.empty:
        return df
    if id_col not in df or (df[id_col] == "").any():
        key = df.reindex(columns=id_fields).astype(str).agg("|".join, axis=1)
        gen = [prefix + h(k, o) for k, o in zip(key, key.groupby(key).cumcount())]
        df[id_col] = df[id_col].where(df[id_col] != "", pd.Series(gen, index=df.index)) if id_col in df else gen
    out = finalize(df, table)
    return out.drop_duplicates(id_col)


def main():
    defl = deflators()
    res = resolver()
    tables = {
        "fact_org_financials": build_financials(defl),
        "fact_grants": build_grants(defl, res),
        "fact_gov_awards": build_gov_awards(defl, res),
        "fact_opportunities": build_simple("fact_opportunities", "opportunity_id", "O",
                                           ["opportunity_number", "title", "status"]),
        "fact_policy_events": build_simple("fact_policy_events", "event_id", "E",
                                           ["event_date", "agency", "program_code", "fiscal_year", "event_type",
                                            "description"]),
    }
    lines = []
    for name, df in tables.items():
        df.to_csv(CLEAN / f"{name}.csv", index=False)
        lines.append(f"- {name}: {len(df):,} rows")
    for pat, prefix in (("stage_supp_*.csv", "stage_supp_"), ("stage_homeless_counts__*.csv", "stage_"),
                        ("stage_hic_projects__*.csv", "stage_"), ("stage_dc_budget_lines__*.csv", "stage_")):
        for p in sorted(INTERIM.glob(pat)):
            stem = p.stem.replace(prefix, "").split("__")[0]
            dst = CLEAN / f"supp_{stem}.csv"
            pd.read_csv(p, dtype=str, keep_default_na=False).to_csv(dst, index=False)
            lines.append(f"- {dst.name}: copied from {p.name}")
    log("62_build_facts", "\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
