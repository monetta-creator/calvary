"""Phase 4: ProPublica Nonprofit Explorer org records -> fact_org_financials cross-check rows (+ Calvary reconciliation).

STAGES (run all, or pick with --only):
  fetch      GET /organizations/{ein}.json for the target EINs (<=2 req/s) -> raw/propublica/{stamp}_org_{ein}.json
  stage      filings_with_data -> interim/stage_fact_org_financials__propublica.csv
  reconcile  Calvary across SOI, NCCS e-file, ProPublica, the 990 PDFs and the audits
             -> interim/calvary_financials_reconciliation.csv (one row per fiscal_year x source; each metric's
             % difference vs a reference: SOI, else ProPublica, else the 990 PDF; government grants vs the 990 PDF
             line 1e, else NCCS; flag_over_1pct lists metrics off by more than 1%)
  notes      observations -> notes_for_analysis.md ("Financial series")
Run after scripts/41_pull_soi_extracts.py (reconcile and notes read its staging file).

Target EINs (assumption, documented): universes calvary, core_peers, dc_sector (all members, fetched first), plus
dmv_funders members where rule F1 (private foundations) is restricted to BMF ASSET_AMT >= $1M and rules F2/F3
(grantmaking public charities) are kept; the funder set is capped at the top 1,500 by BMF ASSET_AMT.

Usage: .venv/bin/python scripts/42_pull_propublica.py [--only fetch,stage,reconcile,notes] [--refresh]
An org whose raw JSON already exists is not re-fetched unless --refresh (so an interrupted fetch resumes).
"""
from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import (CLEAN, RAW, RateLimiter, latest_raw, log, norm_ein, rel, save_raw,
                        session, today)

PP = "https://projects.propublica.org/nonprofits/api/v2"
FUNDER_CAP = 1500
PF_MIN_ASSETS = 1_000_000
PRIORITY_UNIVERSES = ("calvary", "core_peers", "named_comparators", "dc_sector")


# ---------------------------------------------------------------- targets
def targets() -> tuple[list[str], dict]:
    u = pd.read_csv(CLEAN / "dim_universe_membership.csv", dtype=str, keep_default_na=False)
    u["ein"] = u.ein.map(norm_ein)
    u["assets"] = pd.to_numeric(u.bmf_asset_amt.replace("", None), errors="coerce")
    pri = u[u.universe.isin(PRIORITY_UNIVERSES)]
    pri_eins = list(dict.fromkeys(  # calvary, then core peers, then dc_sector
        pri.assign(o=pri.universe.map({k: i for i, k in enumerate(PRIORITY_UNIVERSES)})).sort_values("o").ein))
    f = u[u.universe == "dmv_funders"]
    keep = f[((f.rule_id == "F1") & (f.assets >= PF_MIN_ASSETS)) | f.rule_id.isin(["F2", "F3"])]
    keep = (keep.sort_values("assets", ascending=False).drop_duplicates("ein"))
    keep = keep[~keep.ein.isin(pri_eins)]
    capped = keep.head(FUNDER_CAP)
    info = {
        "priority_eins": len(pri_eins),
        "funder_candidates": len(keep),
        "funder_candidates_by_rule": keep.rule_id.value_counts().to_dict(),
        "funders_kept": len(capped),
        "funders_kept_by_rule": capped.rule_id.value_counts().to_dict(),
        "cap_min_assets": int(capped.assets.min()) if len(capped) else None,
        "dropped_by_cap": len(keep) - len(capped),
    }
    return pri_eins + list(capped.ein), info


# ---------------------------------------------------------------- fetch
def valid_raw(ein: str) -> Path | None:
    """Newest raw org JSON for this EIN, if it parses (a killed run can leave a truncated file)."""
    p = latest_raw("propublica", f"org_{ein}.json")
    if p is None:
        return None
    try:
        json.loads(p.read_text(encoding="utf-8"))
        return p
    except ValueError:
        return None


def stage_fetch(refresh: bool):
    eins, info = targets()
    S = session()
    rl = RateLimiter(2.0)  # shared by the workers: <= 2 requests/s in total

    def one(ein: str) -> dict:
        old = None if refresh else valid_raw(ein)
        if old:
            return {"ein": ein, "status": "reused", "file": rel(old)}
        rl.wait()
        try:
            r = S.get(f"{PP}/organizations/{int(ein)}.json", timeout=60)
        except Exception as e:  # network failure after retries: record and move on
            return {"ein": ein, "status": f"error {type(e).__name__}", "file": ""}
        if r.status_code == 200:
            return {"ein": ein, "status": 200, "file": rel(save_raw("propublica", f"org_{ein}", r.content, "json"))}
        return {"ein": ein, "status": r.status_code, "file": ""}

    # responses take ~1.5 s uncached, so 3 workers are needed to reach the 2 req/s budget
    with ThreadPoolExecutor(max_workers=3) as ex:
        manifest = []
        for i, m in enumerate(ex.map(one, eins)):
            manifest.append(m)
            if (i + 1) % 250 == 0:
                print(f"{i + 1}/{len(eins)}", flush=True)
    n_new = sum(m["status"] == 200 for m in manifest)
    n_reused = sum(m["status"] == "reused" for m in manifest)
    save_raw("propublica", "org_fetch_manifest", {"retrieved": today(), "targets": info, "rows": manifest})
    st = pd.Series([str(m["status"]) for m in manifest]).value_counts().to_dict()
    log("42_pull_propublica: fetch", "\n".join([
        f"- targets: {len(eins):,} EINs = {info['priority_eins']:,} calvary/core_peers/dc_sector + "
        f"{info['funders_kept']:,} dmv_funders",
        f"- funder candidates (F1 with BMF assets >= $1M, plus F2/F3): {info['funder_candidates']:,} "
        f"{info['funder_candidates_by_rule']}",
        f"- CAP: kept top {FUNDER_CAP:,} funders by BMF ASSET_AMT (min kept ${info['cap_min_assets']:,}); "
        f"dropped {info['dropped_by_cap']:,}; kept by rule {info['funders_kept_by_rule']}",
        f"- status counts: {st}; new downloads {n_new:,}, reused raw {n_reused:,}",
        "- rate limit 2 req/s (lib.common.RateLimiter)",
    ]))
    print(st)


# ---------------------------------------------------------------- stage
# ProPublica filings_with_data carry SOI extract field names (lowercase). formtype 0 = 990, 1 = 990-EZ, 2 = 990-PF.
# Same field mapping as scripts/41_pull_soi_extracts.py; "+" = sum. ProPublica's 990 rows carry the reduced
# 2012-style field set, so grants_paid, compensation_total and cash_savings_eoy are not available here.
PP_MAP = {
    "990": {"total_revenue": ["totrevenue"], "contributions_total": ["totcntrbgfts"],
            "program_service_revenue": ["totprgmrevnue"], "investment_income": ["invstmntinc"],
            "special_events_net": ["netincfndrsng"], "other_revenue": ["miscrevtot11e"],
            "total_expenses": ["totfuncexpns"], "total_assets_eoy": ["totassetsend"],
            "total_liabilities_eoy": ["totliabend"], "net_assets_eoy": ["totnetassetend"]},
    "990EZ": {"total_revenue": ["totrevnue"], "contributions_total": ["totcntrbs"],
              "program_service_revenue": ["prgmservrev"], "membership_dues": ["duesassesmnts"],
              "investment_income": ["othrinvstinc"], "special_events_net": ["netincfndrsng"],
              "other_revenue": ["othrevnue"], "total_expenses": ["totexpns"], "total_assets_eoy": ["totassetsend"],
              "total_liabilities_eoy": ["totliabend"], "net_assets_eoy": ["totnetassetsend"]},
    "990PF": {"total_revenue": ["totrcptperbks"], "contributions_total": ["grscontrgifts"],
              "investment_income": ["intrstrvnue", "dividndsamt"], "total_expenses": ["totexpnspbks"],
              "grants_paid": ["contrpdpbks"], "total_assets_eoy": ["totassetsend"],
              "total_liabilities_eoy": ["totliabend"], "net_assets_eoy": ["tfundnworth"],
              "pf_total_grants_paid": ["contrpdpbks"], "pf_contributions_received": ["grscontrgifts"],
              "pf_fmv_assets_eoy": ["fairmrktvaleoy|fairmrktvalamt"],
              "x_pf_disbursements_exempt_purpose": ["totexpnsexempt"], "x_pf_qlfydistrib_opfdn": ["qlfydistribtot"],
              "x_pf_distributable_amount": ["distribamt"], "x_pf_net_investment_income": ["netinvstinc"],
              "x_pf_cash_nonint_eoy": ["othrcashamt"]},
}
FORMTYPE = {0: "990", 1: "990EZ", 2: "990PF"}
OUT = Path(__file__).resolve().parents[1] / "interim" / "stage_fact_org_financials__propublica.csv"
SOURCE_ID = "api_propublica"
CALVARY = "521307706"


def money_cols():
    import importlib.util
    spec = importlib.util.spec_from_file_location("s41", Path(__file__).parent / "41_pull_soi_extracts.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.KEYS, m.MONEY, m.period_fields


def _val(f: dict, expr: str):
    for k in expr.split("|"):  # first non-null alternative
        v = f.get(k)
        if v is not None and v != "":
            return v
    return None


def stage_stage():
    KEYS, MONEY, period_fields = money_cols()
    eins, _ = targets()
    rows, skipped, n_files, n_404 = [], {}, 0, 0
    for ein in eins:
        p = valid_raw(ein)
        if p is None:
            n_404 += 1
            continue
        n_files += 1
        d = json.loads(p.read_text(encoding="utf-8"))
        org = d.get("organization") or {}
        for f in d.get("filings_with_data") or []:
            form = FORMTYPE.get(f.get("formtype"))
            if form is None:
                skipped[f.get("formtype")] = skipped.get(f.get("formtype"), 0) + 1
                continue
            r = {"ein": ein, "return_type": form, "x_tax_pd_raw": str(f.get("tax_prd") or "")[:6],
                 "x_pp_tax_prd_yr": f.get("tax_prd_yr"), "x_pp_updated": f.get("updated") or "",
                 "x_pp_data_source": org.get("data_source") or "",
                 "retrieved_date": pd.Timestamp(p.name[:8]).date().isoformat()}
            for field, parts in PP_MAP[form].items():
                vals = [_val(f, e) for e in parts]
                vals = [float(v) for v in vals if v is not None]
                r[field] = sum(vals) if vals else None
            rows.append(r)
    df = pd.DataFrame(rows)
    df = pd.concat([df, period_fields(df.x_tax_pd_raw)], axis=1)
    bad = df.fiscal_year.isna()
    df = df[~bad]
    # ProPublica tax_prd_yr is the period-END year (= fiscal_year), not the IRS tax year
    yr_ok = (pd.to_numeric(df.x_pp_tax_prd_yr, errors="coerce") == df.fiscal_year).mean()
    df = df.sort_values(["ein", "tax_period_end", "return_type", "x_pp_updated"])
    df["x_pp_n_versions"] = df.groupby(["ein", "tax_period_end", "return_type"]).ein.transform("size")
    st = df.drop_duplicates(["ein", "tax_period_end", "return_type"], keep="last").copy()
    st["object_id"] = ""
    st["is_amended"] = ""
    st["source_id"] = SOURCE_ID
    st["confidence"] = "high"
    st["basis"] = "documented"
    for c in MONEY + [c for c in st.columns if c.startswith("x_pf_")]:
        if c not in st:
            st[c] = pd.NA
        st[c] = pd.to_numeric(st[c], errors="coerce").round().astype("Int64")
    xcols = sorted(c for c in st.columns if c.startswith("x_") and c not in MONEY)
    st = st[KEYS + MONEY + xcols].sort_values(["ein", "tax_period_end", "return_type"])
    st.to_csv(OUT, index=False)

    dup = st.duplicated(["ein", "tax_period_end", "return_type", "source_id"]).sum()
    cal = st[st.ein == CALVARY].set_index("tax_year")
    qc = [f"TY{ty} " + ("not present" if pd.isna(cal.total_revenue.get(ty)) else
                        f"{int(cal.total_revenue.get(ty)):,} {'OK' if cal.total_revenue.get(ty) == want else 'MISMATCH'}")
          for ty, want in {2020: 3_851_984, 2021: 8_867_250}.items()]
    # cross-check against SOI on matching (ein, period, form)
    soi_p = OUT.parent / "stage_fact_org_financials__soi.csv"
    xc = ""
    if soi_p.exists():
        soi = pd.read_csv(soi_p, dtype={"ein": str}, usecols=["ein", "tax_period_end", "return_type", "source_id",
                                                               "total_revenue", "total_expenses", "total_assets_eoy"])
        soi = soi[soi.source_id == "bulk_irs_soi_extract"]
        m = st.merge(soi, on=["ein", "tax_period_end", "return_type"], suffixes=("", "_soi"))
        eq = {c: (m[c].astype("Float64") == m[f"{c}_soi"]).mean() for c in
              ("total_revenue", "total_expenses", "total_assets_eoy")}
        keys = set(zip(soi.ein, soi.tax_period_end, soi.return_type))
        only_pp = st[[k not in keys for k in zip(st.ein, st.tax_period_end, st.return_type)]]
        xc = (f"- cross-check vs SOI: {len(m):,} matching (ein, period, form) rows; equal total_revenue "
              f"{eq['total_revenue']:.1%}, total_expenses {eq['total_expenses']:.1%}, total_assets_eoy "
              f"{eq['total_assets_eoy']:.1%}\n- ProPublica rows with no SOI row: {len(only_pp):,} "
              f"(by fiscal_year {only_pp.fiscal_year.value_counts().sort_index().to_dict()})")
    lines = [
        f"- {n_files:,} org JSONs read ({n_404:,} target EINs with no ProPublica record); "
        f"{len(df):,} filings_with_data rows; skipped formtypes {skipped}; {int(bad.sum())} bad periods",
        f"- tax_prd_yr equals derived fiscal_year (period-end year) on {yr_ok:.1%} of rows",
        f"- staged {len(st):,} rows, {st.ein.nunique():,} EINs -> {rel(OUT)}; duplicates on "
        f"(ein, tax_period_end, return_type, source_id): {dup}",
        f"- Calvary total_revenue QC: {'; '.join(qc)}",
        xc,
        "- rows by fiscal_year x return_type:", "```",
        pd.crosstab(st.fiscal_year, st.return_type, margins=True).to_string(), "```",
    ]
    log("42_pull_propublica: stage", "\n".join(lines))
    print("\n".join(lines))


# ---------------------------------------------------------------- Calvary reconciliation
RECON = Path(__file__).resolve().parents[1] / "interim" / "calvary_financials_reconciliation.csv"
METRICS = ["total_revenue", "total_expenses", "net_assets_eoy", "gov_grants"]


def recon_rows() -> pd.DataFrame:
    I = Path(__file__).resolve().parents[1] / "interim"
    out = []
    for f, label in ((I / "stage_fact_org_financials__soi.csv", None), (OUT, None)):
        if not f.exists():
            continue
        d = pd.read_csv(f, dtype={"ein": str})
        d = d[d.ein == CALVARY]
        for _, r in d.iterrows():
            out.append({"fiscal_year": r.fiscal_year, "tax_year": r.tax_year,
                        "source": {"bulk_irs_soi_extract": "soi_extract", "bulk_nccs_efile": "nccs_efile",
                                   "api_propublica": "propublica"}[r.source_id],
                        "source_id": r.source_id, "total_revenue": r.total_revenue,
                        "total_expenses": r.total_expenses, "net_assets_eoy": r.net_assets_eoy,
                        "gov_grants": r.government_grants})
    raw_in = RAW / "inputs_extracted"
    p = pd.read_csv(raw_in / "form990_pdf_financials.csv", dtype=str)
    p["amount"] = pd.to_numeric(p.amount, errors="coerce")
    for sid, g in p.groupby("source_id"):
        ty = int(g.tax_year.iloc[0])

        def pick(part, line, col, label=None):
            h = g[(g.part == part) & (g.line == line) & (g.column == col)]
            if label:
                h = h[h.line_label == label]
            return h.amount.iloc[0] if len(h) else None
        na = pick("X", "33", "end_of_year", "net_assets_total")
        na = na if na is not None else pick("X", "32", "end_of_year", "net_assets_total")
        out.append({"fiscal_year": ty + 1, "tax_year": ty, "source": "form990_pdf", "source_id": sid,
                    "total_revenue": pick("VIII", "12", "A_total"), "total_expenses": pick("IX", "25", "A_total"),
                    "net_assets_eoy": na, "gov_grants": pick("VIII", "1e", "inner_box")})
        out.append({"fiscal_year": ty, "tax_year": ty - 1, "source": "form990_pdf_prior_year_column",
                    "source_id": sid, "total_revenue": pick("I", "12", "prior_year"),
                    "total_expenses": pick("I", "18", "prior_year"),
                    "net_assets_eoy": pick("I", "22", "beginning_of_year"), "gov_grants": None})
    a = pd.read_csv(raw_in / "audit_financials.csv", dtype=str)
    a["amount"] = pd.to_numeric(a.amount, errors="coerce")
    a = a[a.net_asset_class.isin(["total", "n/a"])]
    for (fy, comp), g in a.groupby(["fiscal_year", "is_prior_year_comparative"]):
        if comp == "True" and not a[(a.fiscal_year == fy) & (a.is_prior_year_comparative == "False")].empty:
            continue  # use the comparative column only when no current-year statement exists
        sid = g.source_id.iloc[0]

        def tot(std):
            h = g[g.line_item_std == std].drop_duplicates("line_item_std")
            return h.amount.iloc[0] if len(h) else None
        gov = g[g.line_item_std.str.startswith("rev_gov_")].amount
        out.append({"fiscal_year": int(fy), "tax_year": int(fy) - 1,
                    "source": "audit_comparative" if comp == "True" else "audit", "source_id": sid,
                    "total_revenue": tot("rev_total"), "total_expenses": tot("exp_total"),
                    "net_assets_eoy": tot("net_assets_end"), "gov_grants": gov.sum() if len(gov) else None})
    r = pd.DataFrame(out)
    r = r[r[METRICS].notna().any(axis=1)]
    for c in ("fiscal_year", "tax_year"):
        r[c] = r[c].astype(int)
    return r


def stage_reconcile():
    r = recon_rows()
    # reference per fiscal year and metric: the e-file basis first (SOI, then ProPublica, then the filed PDF);
    # government grants: the filed 990 Part VIII-1e (PDF), else NCCS e-file
    pdf = ["form990_pdf", "form990_pdf_prior_year_column"]
    order = {"total_revenue": ["soi_extract", "propublica"] + pdf + ["nccs_efile"],
             "total_expenses": ["soi_extract", "propublica"] + pdf,
             "net_assets_eoy": ["soi_extract", "propublica"] + pdf,
             "gov_grants": ["form990_pdf", "nccs_efile"]}
    flags = {i: [] for i in r.index}
    for m, pref in order.items():
        r[f"{m}_ref_source"] = ""
        r[f"{m}_pct_vs_ref"] = pd.NA
        for fy, g in r.groupby("fiscal_year"):
            ref = next((g[(g.source == s) & g[m].notna()][m].iloc[0] for s in pref
                        if not g[(g.source == s) & g[m].notna()].empty), None)
            src = next((s for s in pref if not g[(g.source == s) & g[m].notna()].empty), "")
            if ref is None or ref == 0:
                continue
            for i in g.index:
                if pd.notna(r.at[i, m]):
                    pct = (r.at[i, m] - ref) / abs(ref) * 100
                    r.at[i, f"{m}_pct_vs_ref"] = round(pct, 2)
                    r.at[i, f"{m}_ref_source"] = src
                    if abs(pct) > 1:
                        flags[i].append(m)
    r["flag_over_1pct"] = [";".join(flags[i]) for i in r.index]
    r["source_order"] = r.source.map({s: k for k, s in enumerate(
        ["soi_extract", "propublica", "nccs_efile", "form990_pdf", "form990_pdf_prior_year_column", "audit",
         "audit_comparative"])})
    r = r.sort_values(["fiscal_year", "source_order"]).drop(columns="source_order")
    cols = ["fiscal_year", "tax_year", "source", "source_id"] + METRICS + [
        c for m in METRICS for c in (f"{m}_pct_vs_ref", f"{m}_ref_source")] + ["flag_over_1pct"]
    r[METRICS] = r[METRICS].round().astype("Int64")
    r[cols].to_csv(RECON, index=False)
    efile = r[r.source.isin(["soi_extract", "propublica", "form990_pdf", "form990_pdf_prior_year_column",
                             "nccs_efile"])]
    ef_flag = efile[efile.flag_over_1pct != ""]
    au = r[r.source.str.startswith("audit")]
    lines = [
        f"- {len(r):,} rows -> {rel(RECON)}; fiscal years {r.fiscal_year.min()}-{r.fiscal_year.max()}; sources "
        f"{r.source.value_counts().to_dict()}",
        f"- 990-basis sources (SOI, ProPublica, NCCS, 990 PDFs): {len(ef_flag)} of {len(efile)} rows differ >1% "
        f"from the reference: " + ("; ".join(f"FY{x.fiscal_year} {x.source} {x.flag_over_1pct}"
                                            for x in ef_flag.itertuples()) or "none"),
        f"- audits (GAAP basis): {int((au.flag_over_1pct != '').sum())} of {len(au)} rows differ >1% on at least one "
        "metric: " + "; ".join(f"FY{x.fiscal_year} {x.flag_over_1pct}" for x in au.itertuples()
                               if x.flag_over_1pct),
    ]
    for ty, want in {2020: 3_851_984, 2021: 8_867_250}.items():
        h = r[(r.tax_year == ty) & r.total_revenue.notna() & ~r.source.str.startswith("audit")]
        lines.append(f"- TY{ty} total_revenue by 990-basis source: "
                     + ", ".join(f"{x.source} {int(x.total_revenue):,}{'' if x.total_revenue == want else ' MISMATCH'}"
                                 for x in h.itertuples()))
    log("42_pull_propublica: reconcile", "\n".join(lines))
    print("\n".join(lines))



# ---------------------------------------------------------------- notes
def pct(x: float) -> str:
    return "n/a" if pd.isna(x) else f"{x:.0%}"


def stage_notes():
    from lib.common import append_md
    I = Path(__file__).resolve().parents[1] / "interim"
    s = pd.read_csv(I / "stage_fact_org_financials__soi.csv", dtype={"ein": str}, low_memory=False)
    pp = pd.read_csv(OUT, dtype={"ein": str})
    u = pd.read_csv(CLEAN / "dim_universe_membership.csv", dtype=str, usecols=["universe", "ein"])
    soi = s[s.source_id == "bulk_irs_soi_extract"]
    nc = s[s.source_id == "bulk_nccs_efile"].copy()
    lines = []

    # coverage by year
    ct = pd.crosstab(soi.fiscal_year, soi.return_type)
    core = ct.loc[2011:2023]
    lines.append(
        f"- Coverage. SOI extract: {len(soi):,} rows, {soi.ein.nunique():,} EINs, fiscal years (period-end) "
        f"2011-2023 complete; 2024 partial ({int(ct.loc[2024].sum()) if 2024 in ct.index else 0} rows, early filers "
        f"in the 24 extract). 990 rows/yr {int(core['990'].min()):,}-{int(core['990'].max()):,}, 990-EZ "
        f"{int(core['990EZ'].min()):,}-{int(core['990EZ'].max()):,}. 990-PF rows/yr {int(core['990PF'].max()):,} at "
        f"most but FY2016-FY2018 only {', '.join(str(int(ct.loc[y, '990PF'])) for y in (2016, 2017, 2018))}: "
        "IRS published no 990-PF extract for processing years 2017-2019, and NCCS Core and ProPublica share the gap "
        "(the XML parse is the only fill).")
    lines.append(
        f"- NCCS e-file Part VIII (source of government_grants): {len(nc):,} Form 990 rows, {nc.ein.nunique():,} EINs, "
        f"TY{int(nc.tax_year.min())}-TY{int(nc.tax_year.max())} (TY2021 partial, TY2022 thin; e-filers only, so "
        "early years under-cover paper filers).")
    cov = []
    for name in ("core_peers", "dc_sector", "dmv_funders", "national_women", "size_matched"):
        e = set(u[u.universe == name].ein)
        cov.append(f"{name} {soi[soi.ein.isin(e)].ein.nunique():,}/{len(e):,}")
    uf = pd.read_csv(CLEAN / "dim_universe_membership.csv", dtype=str,
                     usecols=["universe", "ein", "bmf_revenue_amt", "latest_efile_return_type"])
    gap = uf[(uf.universe == "dc_sector") & ~uf.ein.isin(set(soi.ein))]
    small = (pd.to_numeric(gap.bmf_revenue_amt, errors="coerce").fillna(0) < 50_000).mean()
    lines.append("- Universe EINs with >=1 SOI row: " + "; ".join(cov)
                 + f". Of the {len(gap):,} dc_sector EINs with no SOI row, {small:.0%} have BMF revenue under $50K "
                 f"(990-N range) and {int(gap.latest_efile_return_type.isna().sum()):,} have no e-filed 990/990-EZ.")
    keys = set(zip(soi.ein, soi.tax_period_end, soi.return_type))
    m = pp.merge(soi, on=["ein", "tax_period_end", "return_type"], suffixes=("", "_s"))
    only = pp[[k not in keys for k in zip(pp.ein, pp.tax_period_end, pp.return_type)]]
    lines.append(
        f"- ProPublica ({len(pp):,} rows, {pp.ein.nunique():,} EINs) equals SOI on total_revenue for "
        f"{(m.total_revenue == m.total_revenue_s).mean():.1%} of {len(m):,} overlapping rows and adds {len(only):,} "
        "rows SOI lacks: its financial fields are the SOI extract fields, so it is a transcription check, not an "
        "independent source.")

    # Calvary revenue mix
    c = soi[soi.ein == CALVARY].set_index("fiscal_year").sort_index()
    g = nc[nc.ein == CALVARY].set_index("fiscal_year").government_grants
    mix = []
    for fy, r in c.iterrows():
        gv = g.get(fy)
        mix.append(f"FY{str(fy)[2:]} {r.total_revenue / 1e6:.2f}M"
                   + (f" gov {gv / r.total_revenue:.0%}" if pd.notna(gv) else ""))
    se = c.special_events_net
    lines.append(
        "- Calvary (SOI total revenue; government share = Part VIII-1e / total revenue from NCCS e-file): "
        + ", ".join(mix) + f". Contributions are {c.contributions_total.min() / 1e6:.2f}M-"
        f"{c.contributions_total.max() / 1e6:.2f}M and exceed total revenue every year because special events net "
        f"is negative every year ({int(se.max()):,} to {int(se.min()):,}); program service revenue is 0 every year.")
    r = pd.read_csv(RECON)
    au = r[r.source.str.startswith("audit")]
    ef = r[~r.source.str.startswith("audit")]
    gov = au[au.gov_grants_pct_vs_ref.notna()]
    same = sorted(gov[gov.gov_grants_pct_vs_ref.abs() <= 1].fiscal_year)
    o = nc[nc.ein == CALVARY].set_index("fiscal_year")
    diffs = []
    for x in gov[gov.gov_grants_pct_vs_ref.abs() > 1].itertuples():
        ref = ef[(ef.fiscal_year == x.fiscal_year) & (ef.source == x.gov_grants_ref_source)].gov_grants.iloc[0]
        oth = o.other_contributions.get(x.fiscal_year)
        diffs.append(f"FY{str(x.fiscal_year)[2:]} audit {int(x.gov_grants):,} vs 990 line 1e {int(ref):,}"
                     + (f" (line 1f other contributions {int(oth):,})" if pd.notna(oth) else ""))
    lines.append(
        f"- Calvary 990 vs audits ({rel(RECON)}): {int((ef.flag_over_1pct.fillna('') != '').sum())} of {len(ef)} "
        "990-basis rows (SOI, ProPublica, NCCS, 990 PDFs) differ >1%. Audit total revenue runs "
        f"{au.total_revenue_pct_vs_ref.min():.0f}% to {au.total_revenue_pct_vs_ref.max():.0f}% and expenses "
        f"{au.total_expenses_pct_vs_ref.min():.0f}% to {au.total_expenses_pct_vs_ref.max():.0f}% vs the 990 "
        "(GAAP presentation: in-kind, special-event costs); net assets match every year. Audit government revenue "
        f"equals 990 line 1e in FY{str(min(same))[2:]}-FY{str(max(same))[2:]}, then: " + "; ".join(diffs) + ".")

    # government share among core peers and dc_sector (NCCS e-file), fixed tax years
    nc["gov_share"] = nc.government_grants / nc.total_revenue
    pos = nc[nc.total_revenue > 0]
    for name in ("core_peers", "dc_sector"):
        e = set(u[u.universe == name].ein)
        parts = []
        for ty in (2019, 2020):
            x = pos[pos.ein.isin(e) & (pos.tax_year == ty)].set_index("ein").gov_share
            cs = pos[(pos.ein == CALVARY) & (pos.tax_year == ty)].gov_share
            cs = cs.iloc[0] if len(cs) else float("nan")
            x = x.drop(CALVARY, errors="ignore")
            parts.append(f"TY{ty} n={len(x)}: p25 {pct(x.quantile(.25))}, median {pct(x.median())}, p75 "
                         f"{pct(x.quantile(.75))}, {(x == 0).mean():.0%} with none; Calvary {pct(cs)} "
                         f"(above {(x < cs).mean():.0%} of them)")
        lines.append(f"- Government share of revenue (990 line 1e / total revenue, NCCS e-file), {name}: "
                     + "; ".join(parts) + ".")
    e = set(u[u.universe == "core_peers"].ein)
    trend = nc[nc.ein.isin(e) & (nc.total_revenue > 0)].groupby("tax_year").gov_share.median()
    lines.append("- Core-peer median government share by tax year (NCCS): "
                 + ", ".join(f"TY{int(t)} {v:.0%}" for t, v in trend.loc[2011:2021].items()) + ".")
    append_md("notes_for_analysis.md", "Financial series", "\n".join(lines))
    log("42_pull_propublica: notes", "- appended 'Financial series' to notes_for_analysis.md\n" + "\n".join(lines))
    print("\n".join(lines))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="fetch,stage,reconcile,notes")
    ap.add_argument("--refresh", action="store_true")
    a = ap.parse_args()
    todo = a.only.split(",")
    if "fetch" in todo:
        stage_fetch(a.refresh)
    if "stage" in todo:
        stage_stage()
    if "reconcile" in todo:
        stage_reconcile()
    if "notes" in todo:
        stage_notes()
