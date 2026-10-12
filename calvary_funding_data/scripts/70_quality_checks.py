"""Phase 6: quality checks -> reports/data_quality.md and clean/supp_crm_cash_verification.csv.

Checks: row counts per table and source; null rates per column; primary-key duplicates; Calvary financial
reconciliation across sources; CRM-vs-990-PF cash verification (assumption A2); grant-parser check against
Calvary's donor-list foundations; unmatched names and their share of grant dollars; person-matching summary;
coverage gaps; portability (absolute paths, usernames, key-shaped strings, UTF-8).

Usage: python scripts/70_quality_checks.py
"""
import os
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import CLEAN, INTERIM, RAW, REPORTS, ROOT, log, norm_ein, norm_name, today
from lib.specs import SPECS

CAL = "521307706"
PK = {"dim_org": ["ein"], "dim_funder": ["funder_id"], "dim_period": ["year"], "dim_geo": ["geo_id"],
      "dim_program_area": ["program_area"], "dim_person": ["person_id"],
      "dim_universe_membership": ["universe", "ein", "rule_id"],
      "fact_org_financials": ["ein", "fiscal_year", "fye_month", "return_type", "source_id", "object_id"],
      "fact_grants": ["grant_id"], "fact_gov_awards": ["award_row_id"], "fact_opportunities": ["opportunity_id"],
      "fact_policy_events": ["event_id"], "fact_roles": ["role_id"], "fact_org_relationships": ["rel_id"]}
DONOR_LIST_PFS = {"eugene agnes e meyer foundation": "Meyer", "philip l graham fund": "Philip L. Graham",
                  "william s abell foundation": "Abell",   # MARPAT omitted: the DC MARPAT Foundation is no longer in the BMF
                                                            # and its name now resolves to an unrelated TX foundation
                  "venable foundation": "Venable (Venable Baetjer & Howard Foundation, Schedule I)", "rapoport family foundation": "Rapoport",
                  "baxt family foundation": "Baxt", "morris gwendolyn cafritz foundation": "Cafritz",
                  "clark winchcole foundation": "Clark-Winchcole", "leafglen foundation": "Leafglen",
                  "john edward fowler memorial foundation": "Fowler"}


def read(name):
    p = CLEAN / f"{name}.csv"
    try:
        return pd.read_csv(p, dtype=str, keep_default_na=False, low_memory=False) if p.exists() else pd.DataFrame()
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def md_table(df: pd.DataFrame, max_rows=60) -> str:
    if df is None or df.empty:
        return "_none_\n"
    df = df.head(max_rows)
    cols = [str(c) for c in df.columns]
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for r in df.itertuples(index=False):
        lines.append("| " + " | ".join(str(v).replace("|", "/") for v in r) + " |")
    return "\n".join(lines) + "\n"


def main():
    tables = {t: read(t) for t in list(SPECS) + ["dim_universe_membership"]}
    L = [f"# Data quality report", "", f"Generated {today()} by `scripts/70_quality_checks.py`.", ""]

    # 1. row counts
    L += ["## 1. Row counts", ""]
    rc = [{"table": t, "rows": len(d)} for t, d in tables.items()]
    for p in sorted(CLEAN.glob("supp_*.csv")) + [CLEAN / "candidate_interlocks.csv", CLEAN / "entity_aliases.csv"]:
        if p.exists():
            rc.append({"table": p.stem, "rows": sum(1 for _ in open(p, encoding="utf-8")) - 1})
    L += [md_table(pd.DataFrame(rc)), "", "### Rows per source (fact tables)", ""]
    per_src = []
    for t in ("fact_org_financials", "fact_grants", "fact_gov_awards", "fact_opportunities", "fact_policy_events",
              "fact_roles", "fact_org_relationships"):
        d = tables[t]
        if len(d) and "source_id" in d:
            for s, n in d.source_id.value_counts().head(25).items():
                per_src.append({"table": t, "source_id": s, "rows": n})
    L += [md_table(pd.DataFrame(per_src), 200), ""]

    # 2. null rates
    L += ["## 2. Missing-value rates (share of empty cells per column; columns > 0% only)", ""]
    nr = []
    for t, d in tables.items():
        if len(d):
            rates = (d == "").mean()
            for c, v in rates.items():
                if v > 0:
                    nr.append({"table": t, "column": c, "null_rate": f"{v:.1%}"})
    L += [md_table(pd.DataFrame(nr), 400), ""]

    # 3. duplicates
    L += ["## 3. Duplicate primary keys", ""]
    dup = []
    for t, k in PK.items():
        d = tables.get(t, pd.DataFrame())
        if len(d) and all(c in d for c in k):
            dup.append({"table": t, "key": "+".join(k), "duplicate_rows": int(d.duplicated(k).sum())})
    L += [md_table(pd.DataFrame(dup)), ""]

    # 4. Calvary reconciliation
    L += ["## 4. Calvary financial reconciliation across sources", "",
          "One row per fiscal year (FYE Sept 30) and source. `diff_vs_xml` = total revenue relative to the e-filed XML "
          "where available, else to the preferred row. Audits differ from 990s by design (in-kind treatment, "
          "release of restrictions); differences >1% are flagged, not corrected.", ""]
    f = tables["fact_org_financials"]
    rec = pd.DataFrame()
    if len(f):
        c = f[f.ein == CAL].copy()
        for col in ("total_revenue", "total_expenses", "net_assets_eoy", "government_grants"):
            c[col] = pd.to_numeric(c[col], errors="coerce")
        c["fy"] = pd.to_numeric(c.fiscal_year, errors="coerce")
        base = c[c.source_id.str.startswith(("bulk_irs_xml", "bulk_gt_datalake"))].groupby("fy").total_revenue.first()
        base = base.combine_first(c[c.preferred == "1"].groupby("fy").total_revenue.first())
        c["diff_vs_xml"] = (c.total_revenue / c.fy.map(base) - 1).round(4)
        c["flag"] = np.where(c.diff_vs_xml.abs() > 0.01, "DIFF>1%", "")
        rec = c.sort_values(["fy", "source_id"])[["fiscal_year", "return_type", "source_id", "total_revenue",
                                                  "total_expenses", "net_assets_eoy", "government_grants",
                                                  "diff_vs_xml", "flag"]]
        rec.to_csv(REPORTS / "calvary_financials_reconciliation.csv", index=False)
    L += [md_table(rec, 120), ""]

    # 5. CRM cash verification (A2)
    L += ["## 5. CRM funders vs 990-PF grants to Calvary (assumption A2: cash unless contradicted)", ""]
    g = tables["fact_grants"]
    ver = pd.DataFrame()
    if len(g):
        g["amt"] = pd.to_numeric(g.amount, errors="coerce")
        g["ty"] = pd.to_numeric(g.tax_year, errors="coerce")
        to_cal = g[(g.recipient_ein == CAL) & g.source_type.isin(["pf_grants_paid", "schedule_i"])]
        crm = g[g.source_type == "crm"].copy()
        org = read("dim_org").set_index("ein")
        recent = to_cal[to_cal.ty >= 2022].groupby("funder_ein").amt.sum()
        allyrs = to_cal.groupby("funder_ein").agg(total=("amt", "sum"), years=("ty", lambda s: ",".join(
            str(int(x)) for x in sorted(set(s.dropna())))))
        crm["crm_total"] = crm.amt
        crm["org_class"] = crm.funder_ein.map(org.org_class).fillna("")
        crm["filing_grants_ty2022plus"] = crm.funder_ein.map(recent)
        crm["filing_grant_years"] = crm.funder_ein.map(allyrs.years)
        ratio = crm.filing_grants_ty2022plus / crm.crm_total

        # funders whose recent returns list grants only as "see attached" placeholders
        ph = g[g.notes.str.contains("placeholder_row=1", regex=False) & (g.ty >= 2022)].funder_ein.unique()
        in_window = to_cal[to_cal.ty >= 2023].groupby("funder_ein").amt.sum()

        def verdict(r):
            if r.funder_ein == "" or r.org_class not in ("private_foundation", "public_charity"):
                return "not_exempt_filer"
            if r.funder_ein in in_window.index:
                return "confirmed_in_window"
            if not pd.isna(r.filing_grants_ty2022plus) or (isinstance(r.filing_grant_years, str) and r.filing_grant_years):
                return "confirmed_earlier_only"
            if r.funder_ein in set(ph):
                return "attachment_only_list"
            return "no_filing_rows"
        crm["cash_verified"] = [verdict(r) for r in crm.itertuples()]
        crm["ratio_filing_to_crm"] = ratio.round(2)
        ver = crm[["funder_name_raw", "funder_ein", "org_class", "crm_total", "filing_grants_ty2022plus",
                   "filing_grant_years", "ratio_filing_to_crm", "cash_verified"]].sort_values("crm_total", ascending=False)
        ew = INTERIM / "web_inkind_evidence.csv"
        if ew.exists():
            ev = pd.read_csv(ew, dtype=str)
            ev["k"] = ev.iloc[:, 0].map(norm_name)
            evm = ev.drop_duplicates("k").set_index("k")
            ver["web_inkind_classification"] = ver.funder_name_raw.map(norm_name).map(
                evm.get("classification", pd.Series(dtype=str)))
        ver.to_csv(CLEAN / "supp_crm_cash_verification.csv", index=False)
        L += [f"Counts: {ver.cash_verified.value_counts().to_dict()}. Full table: `clean/supp_crm_cash_verification.csv`. "
              "confirmed_in_window = the funder's own 990-PF/Schedule I lists grants to Calvary in TY2023+ (cash). Amounts "
              "differ from CRM totals because TY2025 returns are mostly unfiled and the CRM window is Oct 2023-Oct 2026.",
              "", md_table(ver, 40), ""]

    # 6. grant parser check
    L += ["## 6. Grant parser check: Calvary's donor-list foundations in parsed 990-PF / Schedule I data", ""]
    chk = []
    if len(g):
        pf = g[g.source_type.isin(["pf_grants_paid", "pf_grants_approved_future", "schedule_i"])]
        for key, label in DONOR_LIST_PFS.items():
            fe = g[g.funder_name_raw.map(norm_name) == key].funder_ein
            fe = fe[fe != ""].unique()
            filer_rows = pf[pf.funder_ein.isin(fe)] if len(fe) else pf.iloc[0:0]
            cal_rows = filer_rows[filer_rows.recipient_ein == CAL]
            chk.append({"foundation": label, "funder_ein": ";".join(fe), "parsed_grant_rows_all_recipients": len(filer_rows),
                        "rows_to_calvary": len(cal_rows),
                        "calvary_amount": int(cal_rows.amt.sum()) if len(cal_rows) else 0,
                        "tax_years_to_calvary": ",".join(sorted(set(cal_rows.tax_year)))})
    L += [md_table(pd.DataFrame(chk)),
          "", "A foundation with parsed rows but none to Calvary in TY2020+ is a funding-pattern observation, not "
          "a parser failure (e.g., listed on the 'over the years' support page only).", ""]

    # 7. unmatched names
    L += ["## 7. Unmatched entity names and their share of grant dollars", ""]
    if len(g):
        ann = g[pd.to_numeric(g.cumulative_flag, errors="coerce").fillna(0) == 0]
        ph = ann.notes.str.contains("placeholder_row=1", regex=False)
        indiv = ann.notes.str.contains("recipient_kind=individual", regex=False)
        named = ann[~ph & ~indiv]

        def share(df, label):
            tot, um = df.amt.sum(), df[df.recipient_ein == ""]
            return (f"- {label}: {len(df):,} rows, ${tot:,.0f}; without recipient EIN {len(um):,} rows, "
                    f"${um.amt.sum():,.0f} ({(um.amt.sum() / tot if tot else 0):.1%} of dollars).")
        dmv = named[named.recipient_state.isin(["DC", "MD", "VA"])]
        L += ["Grant dollars exclude cumulative rows. 'See attached' placeholder rows "
              f"({ph.sum():,} rows, ${ann[ph].amt.sum():,.0f}) and grants to individuals ({indiv.sum():,} rows; "
              "names redacted) are reported separately, since they cannot have a recipient EIN.", "",
              share(dmv, "Named organizational recipients in DC/MD/VA (the analysis focus)"),
              share(named, "All named organizational recipients (incl. national/global grants of non-DMV "
                    "known Calvary funders such as the Gates Foundation)"),
              share(ann, "All non-cumulative rows"),
              f"- Funders without an EIN (corporations, government, unnamed): "
              f"{(g.funder_ein == '').sum():,} rows across {g[g.funder_ein == ''].funder_id.nunique():,} funder ids.", ""]
        um_dmv = dmv[dmv.recipient_ein == ""]
        top_um = um_dmv.groupby(["recipient_name_raw", "recipient_state"]).amt.sum().sort_values(ascending=False).head(25)
        L += ["", "Top unmatched DC/MD/VA recipients by dollars (typically government units, public schools and "
              "universities' sub-units, churches, or name variants):", "", md_table(top_um.reset_index()), ""]
        mm = g.match_method.value_counts().reset_index()
        L += ["Recipient match methods:", "", md_table(mm), ""]

    # 8. people
    L += ["## 8. Person matching", ""]
    dp, ci = tables["dim_person"], read("candidate_interlocks")
    if len(dp):
        n_multi = (pd.to_numeric(dp.n_orgs, errors="coerce") > 1).sum()
        conf = dp.match_notes.str.extract(r"match_confidence=(\w+)")[0].value_counts().to_dict()
        L += [f"- People {len(dp):,}; linked across 2+ organizations {n_multi:,} (by confidence {conf}); "
              f"low-confidence candidate pairs for manual review: {len(ci):,} (`clean/candidate_interlocks.csv`).", ""]

    # 9. coverage gaps
    L += ["## 9. Known coverage gaps", ""]
    uni = tables["dim_universe_membership"]
    gaps = []
    if len(uni):
        gaps.append(f"- 990-N / non-filers: {uni[uni.rule_id.isin(['DCS2', 'DMV2'])].ein.nunique():,} sector orgs "
                    "have no return since TY2020 in the BMF or e-file index (990-N postcard filers or inactive): "
                    "no financials or governance data.")
    man = INTERIM / "xml_manifest.csv"
    if man.exists():
        m = pd.read_csv(man, dtype=str)
        gaps.append(f"- XML fetch: {(m.status != 'ok').sum():,} of {len(m):,} targeted returns not retrieved; "
                    f"by tax year: {m.groupby('tax_year').size().to_dict()}.")
    gaps += [
        "- Paper filers: returns filed on paper have no XML; financials rely on SOI/ProPublica where present.",
        "- Recent years: TY2024 returns are partially released (IRS 2025-2026 batches); TY2025 returns are mostly "
        "not yet filed (fiscal years ending mid-2026 have extensions into 2027).",
        "- Calvary audits for FY22, FY24, FY25 were not provided; FY22 comes from the FY23 audit's comparative column.",
        "- FAC audit-year 2023 record for Calvary repeats FY22 SEFA amounts; FY23 audit PDF shows $937,999 (both kept, flagged).",
        "- USAspending shows little of the DC pass-through money (SLFRF, CoC via TCP, EFSP); FAC and DC sources cover it.",
        "- DHS provider-level grant lists for 2025-2026 were not posted (Excel attachments missing); TCP Schedule I is the fallback.",
        "- Corporate giving (non-foundation) appears only where Calvary or a peer lists it (no public filing).",
        "- Individual donors are deliberately excluded except as counts per gift band (Calvary donor privacy policy).",
    ]
    L += gaps + [""]

    # 10. portability
    L += ["## 10. Portability", ""]
    bad, nonutf = [], []
    user = re.escape(Path.home().name)   # the local username, read at run time (never hard-coded)
    # local absolute paths only (not URL paths such as https://x.gov/home/), the username, key-shaped strings
    pat = re.compile(rf"((?<![\w.])/Users/|(?<![\w.])/home/|C:\\Users|\b{user}\b|tvly-[A-Za-z0-9]{{10,}})")
    for d in ("clean", "sources", "reports", "scripts", "config"):
        for p in (ROOT / d).rglob("*"):
            if p.resolve() == Path(__file__).resolve():
                continue   # this scanner necessarily contains the patterns it searches for
            if p.is_file() and p.suffix in (".csv", ".md", ".py", ".yaml", ".txt") and "__pycache__" not in str(p):
                try:
                    txt = p.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    nonutf.append(str(p.relative_to(ROOT)))
                    continue
                if pat.search(txt):
                    bad.append(str(p.relative_to(ROOT)))
    for p in ROOT.glob("*.md"):
        if pat.search(p.read_text(encoding="utf-8")):
            bad.append(p.name)
    L += [f"- Files with absolute paths, usernames or key-shaped strings: {bad or 'none'}",
          f"- Non-UTF-8 files: {nonutf or 'none'}", ""]

    (REPORTS / "data_quality.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    log("70_quality_checks", f"- wrote reports/data_quality.md; duplicates {[d for d in dup if d['duplicate_rows']]}; "
        f"portability issues {bad}")
    print("\n".join(L[:12]))
    print("dups:", [d for d in dup if d["duplicate_rows"]], "| portability:", bad, nonutf)


if __name__ == "__main__":
    main()
