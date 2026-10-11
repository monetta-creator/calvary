"""Phase 4 QC for the XML pull (scripts 30 + 50) -> interim/xml_qc.md.

Checks
  1. Fetch coverage by release year and source (interim/xml_manifest.csv).
  2. Parse errors by schema version.
  3. 990-PF grants paid: sum of itemized rows vs the reported total (Part XIV/XV line 3a), match rate.
  4. Calvary financials vs ProPublica/GT totals (TY2020 3,851,984; TY2021 8,867,250; TY2024 4,967,995).
  5. Cafritz Foundation: EIN check and the TY2024 990-PF grant to Calvary ($170,000 expected).
  6. Grant rows naming Calvary ("calvary women" in the normalized name, or recipient EIN 521307706): rows and dollars by
     funder, compared with the CRM funder list (raw/inputs_extracted/crm_funders_2023_2026.csv via
     interim/known_funder_matches.csv).
  7. Trace checks: 10 random grant rows and 10 random role rows re-read from the raw XML with a plain (non-streaming)
     namespace-stripped parse at the recorded xpath.

Usage: .venv/bin/python scripts/51_qc_xml.py [--seed 7]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd
from lxml import etree

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import INTERIM, RAW, ROOT, log, norm_ein, norm_name, rel  # noqa: E402

CALVARY = "521307706"
CALVARY_EXPECTED = {2020: 3851984, 2021: 8867250, 2024: 4967995}
CAFRITZ_GUESS = "530241716"
QC = INTERIM / "xml_qc.md"


def md_table(df: pd.DataFrame, floatfmt: str = ",.0f") -> str:
    cols = list(df.columns)
    out = ["| " + " | ".join(str(c) for c in cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for _, r in df.iterrows():
        cells = []
        for c in cols:
            v = r[c]
            if ("rate" in c or "share" in c) and isinstance(v, float) and pd.notna(v):
                cells.append(f"{v:.2%}")
            elif ("year" in c or c.endswith("_ty_filed")) and pd.notna(v) and not isinstance(v, str):
                cells.append(str(int(v)))
            elif isinstance(v, float) and pd.notna(v):
                cells.append(format(v, floatfmt) if abs(v) >= 1 or v == 0 else f"{v:.3f}")
            elif isinstance(v, (int,)) and not isinstance(v, bool):
                cells.append(f"{v:,}")
            else:
                cells.append("" if pd.isna(v) else str(v))
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


def strip_parse(path: Path):
    root = etree.parse(str(path), etree.XMLParser(huge_tree=True)).getroot()
    for el in root.iter():
        if isinstance(el.tag, str):
            el.tag = etree.QName(el).localname
    return root


def first_text(el, paths):
    for p in paths:
        v = el.findtext(p)
        if v:
            return " ".join(v.split())
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=7)
    a = ap.parse_args()
    S = []  # markdown sections
    summary = []

    # ------------------------------------------------ 1. fetch coverage
    m = pd.read_csv(INTERIM / "xml_manifest.csv", dtype=str, keep_default_na=False)
    m["src"] = m["fetch_source"].str.split(":").str[0].replace("", "none")
    m["rel_yr"] = m["release_year"].replace("", "pre-2021 (Calvary)")
    cov = m.groupby("rel_yr").agg(returns=("object_id", "size"), ok=("status", lambda s: int((s == "ok").sum())),
                                  gt_s3=("src", lambda s: int((s == "gt_s3").sum())),
                                  irs_zip=("src", lambda s: int((s == "irs").sum()))).reset_index()
    cov["success_rate"] = cov["ok"] / cov["returns"]
    tot = m["status"].eq("ok").mean()
    irs_by_zip = m[m["src"] == "irs"]["fetch_source"].value_counts().head(12)
    mb = m.loc[m["status"] == "ok", "bytes"].astype(float).sum() / 1e6
    irs_files = m.loc[(m["src"] == "irs") & (m["status"] == "ok"), "path"]
    n_bom = sum(1 for p in irs_files if (ROOT / p).open("rb").read(3) == b"\xef\xbb\xbf")
    gt_gap = m["fetch_source"].isin(["irs:2026_TEOS_XML_05B", "irs:2026_TEOS_XML_08A"]).sum()
    S.append("## 1. Fetch coverage\n"
             f"{len(m):,} returns in scope; fetched {int(m['status'].eq('ok').sum()):,} ({tot:.2%}); XML on disk {mb:,.0f} MB. "
             f"By type: {m['return_type'].value_counts().to_dict()}.\n\n" + md_table(cov) +
             "\n\nIRS ZIP fallback by batch (GT S3 lacked the object): " +
             "; ".join(f"{k.split(':')[1]} {v:,}" for k, v in irs_by_zip.items()) +
             f".\n\nOf the {len(irs_files):,} IRS-ZIP files, {gt_gap:,} are in the two batches GT has not unpacked "
             f"(2026 05B/08A). The other {len(irs_files) - gt_gap:,} exist on GT S3 but start with a UTF-8 byte-order mark "
             f"({n_bom:,} of all IRS-ZIP files do): `XmlStore.get()` tests `content.lstrip().startswith(b\"<\")`, which "
             "fails on a BOM, so the first fetch run fell through to the IRS ZIP (same bytes, 4 req/s). Script 30 now "
             "overrides `get()` to accept the BOM; the shared fix belongs in scripts/lib/xmlstore.py" +
             (f"\n\nNot fetched: {m[m['status'] != 'ok'][['object_id', 'ein', 'release_year', 'error']].head(20).to_dict('records')}"
              if (m["status"] != "ok").any() else "\n\nNot fetched: none."))
    summary.append(f"fetch {tot:.2%} of {len(m):,}")

    # ------------------------------------------------ 2. parse errors
    fin = pd.read_csv(INTERIM / "stage_fact_org_financials__xml.csv", dtype={"ein": str, "object_id": str})
    err = pd.read_csv(INTERIM / "xml_parse_errors.csv", dtype=str)
    pv = fin.groupby("x_return_version").size().rename("parsed")
    ev = err.groupby("schema_version").size().rename("errors") if len(err) else pd.Series(dtype=int, name="errors")
    vt = pd.concat([pv, ev], axis=1).fillna(0).astype(int).reset_index().rename(columns={"index": "schema_version"})
    vt["error_rate"] = vt["errors"] / (vt["parsed"] + vt["errors"])
    S.append("## 2. Parse errors by schema version\n"
             f"Parsed {len(fin):,}; errors {len(err)}" + (f" (sample: {err['error'].head(3).tolist()})" if len(err) else "")
             + f". Amended returns (XML AmendedReturnInd): {int(fin['is_amended'].sum())}. Filer EIN differs from the "
             f"index EIN: {int(fin['x_manifest_ein_mismatch'].sum())}.\n\n" + md_table(vt))
    summary.append(f"parse errors {len(err)}")

    # ------------------------------------------------ 3. PF grants sum vs reported
    pf = fin[fin["return_type"] == "990PF"].copy()
    pf["reported"] = pf["x_pf_grants_paid_total_line3a"]
    pf["rows_sum"] = pf["x_pf_paid_rows_sum"].fillna(0)
    pf["rows_n"] = pf["x_pf_paid_rows_n"].fillna(0)
    pf["diff"] = pf["rows_sum"] - pf["reported"].fillna(0)

    def cat(r):
        rep = r["reported"]
        if pd.isna(rep) or rep == 0:
            return "no grants reported, no rows" if r["rows_n"] == 0 else "rows but total blank/0"
        if abs(r["diff"]) <= 1:
            return "exact match"
        if r["rows_n"] == 0:
            return "total reported, no itemized rows"
        if abs(r["diff"]) <= 0.01 * rep:
            return "within 1%"
        return "mismatch >1%"
    pf["cat"] = pf.apply(cat, axis=1)
    ct = pf["cat"].value_counts().rename_axis("category").reset_index(name="returns")
    ct["share"] = ct["returns"] / len(pf)
    with_tot = pf[pf["reported"].fillna(0) > 0]
    exact = (with_tot["cat"] == "exact match").mean()
    w1 = with_tot["cat"].isin(["exact match", "within 1%"]).mean()
    allm = pf["cat"].isin(["exact match", "no grants reported, no rows"]).mean()
    dollars_cov = with_tot["rows_sum"].clip(upper=with_tot["reported"]).sum() / with_tot["reported"].sum()
    by_ty = with_tot.groupby("tax_year")["cat"].apply(lambda s: (s == "exact match").mean()).rename("exact_rate")
    big = with_tot[with_tot["cat"].isin(["mismatch >1%", "total reported, no itemized rows"])].copy()
    big["absdiff"] = big["diff"].abs()
    big = big.sort_values("absdiff", ascending=False).head(10)[
        ["ein", "x_filer_name", "tax_year", "object_id", "reported", "rows_sum", "rows_n", "cat"]]
    pf["ph_n"] = pf["x_pf_paid_placeholder_n"].fillna(0)
    pf["ph_sum"] = pf["x_pf_paid_placeholder_sum"].fillna(0)
    wt = pf[pf["reported"].fillna(0) > 0]
    all_ph = wt[(wt["rows_n"] > 0) & (wt["ph_n"] == wt["rows_n"])]
    some_ph = wt[(wt["ph_n"] > 0) & (wt["ph_n"] < wt["rows_n"])]
    named_cov = (wt["rows_sum"] - wt["ph_sum"]).clip(lower=0).clip(upper=wt["reported"]).sum() / wt["reported"].sum()
    S.append("## 3. 990-PF grants paid: itemized rows vs reported total (line 3a)\n"
             f"{len(pf):,} 990-PF returns. Exact match (±$1) on every return, counting no-grant returns as matches: "
             f"**{allm:.2%}**. Among the {len(with_tot):,} returns reporting grants > 0: exact **{exact:.2%}**, "
             f"within 1% {w1:.2%}; rows cover {dollars_cov:.1%} of reported dollars.\n\n"
             f"The sum check confirms the parser, not itemization: {len(all_ph):,} returns ({len(all_ph) / len(wt):.1%}) "
             f"carry only lump-sum placeholder rows (\"SEE ATTACHED SCHEDULE\", \"See Statement 27A\", \"VARIOUS\"; "
             f"the grantee list is a PDF/text attachment not in the XML) worth "
             f"${all_ph['reported'].sum() / 1e6:,.0f}M, and {len(some_ph):,} more mix named rows with placeholders. Rows "
             f"naming a grantee cover **{named_cov:.1%}** of reported grant dollars. Placeholder rows are flagged "
             "`x_placeholder_row = 1` in the grants staging file.\n\n" + md_table(ct) +
             "\n\nExact-match rate by tax year (returns with grants): " +
             ", ".join(f"TY{int(k)} {v:.2%}" for k, v in by_ty.items()) +
             "\n\nLargest attachment-only filers (placeholder rows only, latest return): " +
             "; ".join(f"{r.x_filer_name} TY{int(r.tax_year)} ${r.reported / 1e6:,.1f}M"
                       for r in all_ph.sort_values("reported", ascending=False).drop_duplicates("ein").head(10).itertuples()) +
             "\n\nLargest gaps (usually a grant list filed as a PDF/text attachment, so the XML has the total but no rows):\n\n"
             + md_table(big))
    summary.append(f"PF grants sum exact {exact:.2%} of returns with grants ({allm:.2%} of all PF); named-grantee "
                   f"rows cover {named_cov:.1%} of PF grant dollars")

    # ------------------------------------------------ 4. Calvary financials
    cal = fin[fin["ein"] == CALVARY].sort_values("tax_year")[
        ["tax_year", "fiscal_year", "object_id", "x_return_version", "total_revenue", "government_grants",
         "contributions_total", "total_expenses", "net_assets_eoy", "is_amended"]].copy()
    cal["expected_total_revenue"] = cal["tax_year"].map(CALVARY_EXPECTED)
    cal["match"] = cal.apply(lambda r: "" if pd.isna(r["expected_total_revenue"])
                             else ("yes" if r["total_revenue"] == r["expected_total_revenue"] else "NO"), axis=1)
    ok3 = all(cal.loc[cal["tax_year"] == ty, "total_revenue"].eq(v).any() for ty, v in CALVARY_EXPECTED.items())
    S.append("## 4. Calvary (521307706) financials\n"
             f"Expected totals (ProPublica/GT/XML recon) match for TY2020, TY2021, TY2024: **{'yes' if ok3 else 'NO'}**.\n\n"
             + md_table(cal))
    summary.append(f"Calvary revenue checks {'pass' if ok3 else 'FAIL'}")

    # ------------------------------------------------ 5. Cafritz
    g = pd.read_csv(INTERIM / "stage_fact_grants__xml.csv", dtype={"funder_ein": str, "recipient_ein": str,
                                                                    "object_id": str, "recipient_zip5": str},
                    low_memory=False)
    names = fin.groupby("ein")["x_filer_name"].last()
    caf = names[names.str.contains("CAFRITZ", case=False, na=False)]
    guess_name = names.get(CAFRITZ_GUESS, "(not in scope)")
    mg = caf[caf.str.contains("MORRIS", case=False)]
    caf_ein = mg.index[0] if len(mg) else None
    calv_mask = g["recipient_name_norm"].fillna("").str.contains("calvary women") | (g["recipient_ein"] == CALVARY)
    gc = g[calv_mask].copy()
    caf_rows = gc[(gc["funder_ein"] == caf_ein)] if caf_ein else gc.iloc[0:0]
    caf_24 = caf_rows[caf_rows["tax_year"] == 2024]
    S.append("## 5. Cafritz Foundation spot check\n"
             f"- EIN {CAFRITZ_GUESS} is **{guess_name}**, not Cafritz. The Morris and Gwendolyn Cafritz Foundation is "
             f"**{caf_ein}** ({names.get(caf_ein, '')}). Other Cafritz-named filers in scope: "
             f"{', '.join(f'{e} {n}' for e, n in caf.items() if e != caf_ein) or 'none'}.\n"
             f"- Cafritz grant rows naming Calvary, all years: " +
             ("; ".join(f"TY{int(r.tax_year)} ${r.amount:,.0f} ({r.recipient_name_raw}; {r.purpose_text}; object {r.object_id})"
                        for r in caf_rows.sort_values("tax_year").itertuples()) or "none") +
             f"\n- TY2024 amount to Calvary: **{caf_24['amount'].sum():,.0f}** (expected 170,000: "
             f"{'match' if caf_24['amount'].sum() == 170000 else 'NO MATCH'}).")
    summary.append(f"Cafritz EIN {caf_ein}; TY2024 to Calvary ${caf_24['amount'].sum():,.0f}")

    # ------------------------------------------------ 6. grants to Calvary vs CRM
    gc["funder_name_raw"] = gc["funder_ein"].map(gc.sort_values("tax_year").groupby("funder_ein")["funder_name_raw"].last())
    by_f = gc.groupby(["funder_ein", "funder_name_raw"]).agg(
        rows=("amount", "size"), dollars=("amount", "sum"),
        years=("tax_year", lambda s: ",".join(str(int(x)) for x in sorted(set(s)))),
        source_types=("source_type", lambda s: ",".join(sorted(set(s))))).reset_index()
    by_f = by_f.sort_values("dollars", ascending=False)
    crm = pd.read_csv(RAW / "inputs_extracted" / "crm_funders_2023_2026.csv", dtype=str)
    km = pd.read_csv(INTERIM / "known_funder_matches.csv", dtype=str)
    km = km[km["accept"].isin(["yes", "inferred"]) & km["ein"].notna()]
    km["ein"] = km["ein"].map(norm_ein)
    crm["name_norm"] = crm["funder_name_norm"].fillna(crm["last_name"].map(norm_name))
    crm = crm.merge(km[["name_norm", "ein"]].drop_duplicates("name_norm"), on="name_norm", how="left")
    crm_eins = crm.dropna(subset=["ein"]).groupby("ein").agg(
        crm_name=("last_name", "first"), crm_gift_total=("GIFT_TOTAL", lambda s: pd.to_numeric(s, errors="coerce").sum()),
        crm_last_date=("LAST_CONTRIB_DATE", "max")).reset_index()
    by_f = by_f.merge(crm_eins, left_on="funder_ein", right_on="ein", how="left").drop(columns=["ein"])
    by_f["in_crm"] = by_f["crm_name"].notna().map({True: "yes", False: "no"})
    # CRM funders with an EIN that filed XML in scope but show no Calvary grant row
    filed = set(fin["ein"])
    xml_funders = set(gc["funder_ein"])
    crm_missing = crm_eins[crm_eins["ein"].isin(filed) & ~crm_eins["ein"].isin(xml_funders)].copy()
    crm_missing["latest_ty_filed"] = crm_missing["ein"].map(fin.groupby("ein")["tax_year"].max())
    crm_missing["form"] = crm_missing["ein"].map(fin.groupby("ein")["return_type"].last())
    lastpf = fin[fin["return_type"] == "990PF"].sort_values("tax_year").groupby("ein").last()
    att = (lastpf["x_pf_paid_rows_n"] > 0) & (lastpf["x_pf_paid_placeholder_n"] == lastpf["x_pf_paid_rows_n"])
    crm_missing["pf_grants_attachment_only"] = crm_missing["ein"].map(att).map({True: "yes", False: "no"})
    crm_missing = crm_missing.sort_values("crm_gift_total", ascending=False)
    recent = gc[gc["tax_year"] >= 2022]
    S.append("## 6. Grant rows naming Calvary\n"
             f"{len(gc):,} rows (name contains \"calvary women\" or recipient EIN {CALVARY}) from {gc['funder_ein'].nunique()} "
             f"funders, ${gc['amount'].sum():,.0f} across TY{int(gc['tax_year'].min()) if len(gc) else ''}-"
             f"TY{int(gc['tax_year'].max()) if len(gc) else ''}; TY2022+ {len(recent):,} rows / ${recent['amount'].sum():,.0f}. "
             f"By source type: {gc['source_type'].value_counts().to_dict()}.\n\n"
             f"CRM: {crm['ein'].notna().sum()} of {len(crm)} CRM funder names carry an accepted EIN ({crm_eins.shape[0]} EINs). "
             f"Of the XML funders naming Calvary, {int((by_f['in_crm'] == 'yes').sum())} are in the CRM by EIN and "
             f"{int((by_f['in_crm'] == 'no').sum())} are not (mostly gifts before the CRM window, 2023-2026, or donors "
             f"recorded under another name).\n\n"
             + md_table(by_f[["funder_ein", "funder_name_raw", "rows", "dollars", "years", "source_types", "in_crm",
                              "crm_gift_total"]].head(60)) +
             f"\n\nCRM funders (by EIN) that filed an in-scope XML but list no Calvary grant ({len(crm_missing)}; "
             f"{int((crm_missing['pf_grants_attachment_only'] == 'yes').sum())} are 990-PF filers whose grant list is "
             "attachment-only, so the XML can't name Calvary; most others are corporate or matching-gift sources):\n\n"
             + md_table(crm_missing.head(40)))
    summary.append(f"Calvary grant rows {len(gc):,} from {gc['funder_ein'].nunique()} funders (${gc['amount'].sum():,.0f})")

    # ------------------------------------------------ 7. trace checks
    roles = pd.read_csv(INTERIM / "stage_fact_roles__xml.csv", dtype={"ein": str, "object_id": str}, low_memory=False)
    path_of = dict(zip(m["object_id"], m["path"]))
    lines = []
    n_ok = 0
    gs = g.sample(10, random_state=a.seed)
    for r in gs.itertuples():
        root = strip_parse(ROOT / path_of[r.object_id])
        hits = root.xpath(r.x_xpath)
        if not hits:
            lines.append(f"| grant | {r.object_id} | `{r.x_xpath}` | element not found | FAIL |")
            continue
        el = hits[0]
        amt = sum(float(el.findtext(t) or 0) for t in ("Amt", "CashGrantAmt", "NonCashAssistanceAmt"))
        nm = " ".join(x for x in (first_text(el, ["RecipientBusinessName/BusinessNameLine1Txt"]),
                                  first_text(el, ["RecipientBusinessName/BusinessNameLine2Txt"])) if x) \
            or first_text(el, ["RecipientPersonNm"])
        exp_nm = r.recipient_name_raw if isinstance(r.recipient_name_raw, str) else None
        good = (abs(amt - (r.amount if pd.notna(r.amount) else 0)) < 1) and (exp_nm is None or exp_nm == nm)
        n_ok += good
        shown = nm if exp_nm else "[individual, redacted]"
        lines.append(f"| grant | {r.object_id} | `{r.x_xpath}` | {shown} / {amt:,.0f} vs staged {r.amount:,.0f} | "
                     f"{'ok' if good else 'FAIL'} |")
    rs = roles.sample(10, random_state=a.seed)
    for r in rs.itertuples():
        root = strip_parse(ROOT / path_of[r.object_id])
        hits = root.xpath(r.x_xpath)
        if not hits:
            lines.append(f"| role | {r.object_id} | `{r.x_xpath}` | element not found | FAIL |")
            continue
        el = hits[0]
        nm = first_text(el, ["PersonNm"]) or " ".join(
            x for x in (first_text(el, ["BusinessName/BusinessNameLine1Txt"]),
                        first_text(el, ["BusinessName/BusinessNameLine2Txt"])) if x)
        ti = first_text(el, ["TitleTxt"])
        good = nm == r.name_display and (ti or "") == (r.title if isinstance(r.title, str) else "")
        n_ok += good
        lines.append(f"| role | {r.object_id} | `{r.x_xpath}` | {nm} / {ti} | {'ok' if good else 'FAIL'} |")
    S.append("## 7. Trace checks (staged row -> raw XML element)\n"
             f"{n_ok}/20 rows re-read from the raw file at the recorded xpath with a plain namespace-stripped parse "
             f"(independent of the streaming parser) and matched on name and amount (grants) or name and title (roles).\n\n"
             "| table | object_id | xpath | raw value | result |\n|---|---|---|---|---|\n" + "\n".join(lines))
    summary.append(f"trace {n_ok}/20")

    head = ("# XML pull QC (scripts 30_fetch_xml, 50_parse_xml, 51_qc_xml)\n\n"
            f"Inputs: {rel(INTERIM / 'xml_manifest.csv')}, interim/stage_*__xml.csv. Summary: " + "; ".join(summary) + ".\n")
    QC.write_text(head + "\n\n".join(S) + "\n", encoding="utf-8")
    log("51_qc_xml", "- " + "\n- ".join(summary) + f"\n- report -> {rel(QC)}")
    print("\n".join(summary))


if __name__ == "__main__":
    main()
