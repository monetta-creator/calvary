"""Phase 4 observations from the XML staging tables -> notes_for_analysis.md ("XML pulls") and open_questions.md.

Facts only, no interpretation. Recipient matching here is a light, notes-only pass (recipient EIN, else exact
normalized name or rapidfuzz token_sort_ratio >= 92 within the peer's state); Phase 5 does the real resolution.

  1. Top DMV funders of the 18 core peers (CP1), TY2020-TY2024.
  2. Funders giving to many core peers but not to Calvary.
  3. DAF-sponsor Schedule I flows to DC women's / homeless / DV organizations.
  4. 990-PF grant concentration among DMV private foundations.

Usage: .venv/bin/python scripts/52_xml_notes.py [--dry-run]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import pandas as pd
from rapidfuzz import fuzz, process

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import CLEAN, CONFIG, INTERIM, append_md, log, norm_ein, norm_name  # noqa: E402

CALVARY = "521307706"
DMV = {"DC", "MD", "VA"}
CORE_NTEE = {"L40", "L41", "P85", "P43", "I70", "I71", "I73", "P62", "F42"}
WOMEN_RE = re.compile(r"(?i)\b(women|womens|woman|sister|sisters|mothers|ladies|girls|ywca|house of ruth|"
                      r"domestic violence|survivors)\b")


def money(x: float) -> str:
    return f"${x / 1e6:,.1f}M" if abs(x) >= 1e6 else f"${x / 1e3:,.0f}k"


def peer_aliases(fin: pd.DataFrame, u: pd.DataFrame) -> dict[tuple[str, str], str]:
    cp = pd.read_csv(CONFIG / "core_peers.csv", dtype=str)
    cp["ein"] = cp["ein"].map(norm_ein)
    bmf = u[u["rule_id"] == "CP1"].set_index("ein")
    out = {}
    for _, r in cp.iterrows():
        e = r["ein"]
        st = bmf.loc[e, "state"] if e in bmf.index else "DC"
        names = {r["name"], re.sub(r"\s*\(.*?\)", "", r["name"])}
        names |= set(re.findall(r"\((.*?)\)", r["name"]))
        if e in bmf.index:
            names.add(bmf.loc[e, "org_name_bmf"])
        names |= set(fin.loc[fin["ein"] == e, "x_filer_name"].dropna())
        for n in names:
            k = norm_name(n)
            if len(k) >= 4 and k not in ("dc", "md", "va"):
                out[(k, st)] = e
    return out


def match_peers(g: pd.DataFrame, aliases: dict, peer_eins: set) -> pd.Series:
    """peer EIN per grant row ('' if none)."""
    res = pd.Series("", index=g.index)
    by_ein = g["recipient_ein"].isin(peer_eins)
    res[by_ein] = g.loc[by_ein, "recipient_ein"]
    keys = list({k for k, _ in aliases})
    cand = g[~by_ein & g["recipient_state"].isin(DMV) & g["recipient_name_norm"].notna()]
    pairs = cand[["recipient_name_norm", "recipient_state"]].drop_duplicates()
    hit = {}
    for nm, st in pairs.itertuples(index=False):
        if (nm, st) in aliases:
            hit[(nm, st)] = aliases[(nm, st)]
            continue
        best = process.extractOne(nm, keys, scorer=fuzz.token_sort_ratio, score_cutoff=92)
        if best and (best[0], st) in aliases:
            hit[(nm, st)] = aliases[(best[0], st)]
    k = list(zip(cand["recipient_name_norm"], cand["recipient_state"]))
    res[cand.index] = [hit.get(x, "") for x in k]
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    fin = pd.read_csv(INTERIM / "stage_fact_org_financials__xml.csv", dtype={"ein": str, "object_id": str},
                      low_memory=False)
    g = pd.read_csv(INTERIM / "stage_fact_grants__xml.csv", dtype={"funder_ein": str, "recipient_ein": str,
                                                                    "object_id": str, "recipient_zip5": str},
                    low_memory=False)
    prof = pd.read_csv(INTERIM / "org_profile__xml.csv", dtype={"ein": str}, low_memory=False)
    u = pd.read_csv(CLEAN / "dim_universe_membership.csv", dtype=str)
    u["ein"] = u["ein"].map(norm_ein)
    g = g[(g["tax_year"] >= 2020) & (g["tax_year"] <= 2024) & (g["source_type"] != "pf_grants_approved_future")].copy()
    funder_state = prof.sort_values("tax_year").groupby("ein")["state"].last()
    g["funder_state"] = g["funder_ein"].map(funder_state)
    fname = fin.sort_values("tax_year").groupby("ein")["x_filer_name"].last()

    peer_eins = set(u.loc[u["rule_id"] == "CP1", "ein"])
    aliases = peer_aliases(fin, u)
    g["peer"] = match_peers(g, aliases, peer_eins)
    g["is_calvary"] = g["recipient_name_norm"].fillna("").str.contains("calvary women") | (g["recipient_ein"] == CALVARY)
    pg = g[g["peer"] != ""]
    lines = []

    # 1. top DMV funders of core peers
    dmv_pg = pg[pg["funder_state"].isin(DMV)]
    top = (dmv_pg.groupby("funder_ein").agg(dollars=("amount", "sum"), peers=("peer", "nunique"))
           .sort_values("dollars", ascending=False).head(10))
    cal_f = set(g.loc[g["is_calvary"], "funder_ein"])
    lines.append(f"- Core-peer grant rows matched (TY2020-TY2024, paid): {len(pg):,} rows, {money(pg['amount'].sum())}, "
                 f"{pg['peer'].nunique()} of {len(peer_eins)} peers, {pg['funder_ein'].nunique():,} funders "
                 f"(recipient EIN or name+state match; notes-only matching).")
    lines.append("- Top DMV funders of core peers by dollars: " + "; ".join(
        f"{fname.get(e, e)} {money(r.dollars)} to {int(r.peers)} peers{' (also Calvary)' if e in cal_f else ''}"
        for e, r in top.iterrows()) + ".")

    # 2. funders giving to many core peers but not Calvary
    many = pg.groupby("funder_ein").agg(peers=("peer", "nunique"), dollars=("amount", "sum"))
    many = many[(many["peers"] >= 4) & ~many.index.isin(cal_f)].sort_values(["peers", "dollars"], ascending=False)
    lines.append(f"- Funders giving to 4+ core peers with no grant row naming Calvary in TY2020-TY2024: {len(many)}. "
                 "Top: " + "; ".join(f"{fname.get(e, e)} ({funder_state.get(e, '?')}) {int(r.peers)} peers / {money(r.dollars)}"
                                     for e, r in many.head(12).iterrows()) + ".")

    # 3. DAF flows to DC women's / homeless / DV orgs
    dcs = u[u["rule_id"].isin(["DCS1", "DCS2", "CP1", "SUBJ"]) & (u["state"] == "DC")].drop_duplicates("ein")
    target = set(dcs.loc[dcs["ntee3"].isin(CORE_NTEE) | dcs["org_name_bmf"].fillna("").map(lambda x: bool(WOMEN_RE.search(x))), "ein"])
    d = g[g["x_daf_dmv_only"] == 1]
    d_dc = d[d["recipient_state"] == "DC"]
    d_t = d_dc[d_dc["recipient_ein"].isin(target)]
    by_sp = d_t.groupby("funder_ein")["amount"].sum().sort_values(ascending=False)
    by_rec = d_t.groupby("recipient_ein").agg(n=("amount", "size"), dollars=("amount", "sum")).sort_values(
        "dollars", ascending=False).head(8)
    rec_name = dcs.set_index("ein")["org_name_bmf"]
    cal_d = d[d["is_calvary"]]
    lines.append(f"- DAF sponsors (15, Schedule I, TY2020-TY2024): DMV rows {len(d):,} / {money(d['amount'].sum())}; "
                 f"DC {money(d_dc['amount'].sum())}; to {d_t['recipient_ein'].nunique()} DC homeless/housing/DV/women's orgs "
                 f"(DC-sector universe orgs with core homeless/housing/DV NTEE or a women-focused name) {money(d_t['amount'].sum())}. By sponsor: " +
                 "; ".join(f"{fname.get(e, e)} {money(v)}" for e, v in by_sp.head(6).items()) +
                 ". Top recipients: " + "; ".join(f"{rec_name.get(e, e)} {money(r.dollars)}" for e, r in by_rec.iterrows())
                 + f". Calvary: {len(cal_d)} DAF rows / {money(cal_d['amount'].sum())}" +
                 (" (" + "; ".join(f"{fname.get(e, e)} {money(v)}" for e, v in
                                  cal_d.groupby('funder_ein')['amount'].sum().sort_values(ascending=False).items()) + ")"
                  if len(cal_d) else "") + ".")

    # 4. PF concentration (DMV private foundations, F1)
    f1 = set(u.loc[u["rule_id"] == "F1", "ein"])
    p = g[(g["source_type"] == "pf_grants_paid") & g["funder_ein"].isin(f1)]
    tot = p["amount"].sum()
    byf = p.groupby("funder_ein")["amount"].sum().sort_values(ascending=False)
    n_f = (byf > 0).sum()
    top10 = byf.head(10).sum() / tot if tot else 0
    top1p = byf.head(max(1, int(n_f * 0.01))).sum() / tot if tot else 0
    dmv_share = p.loc[p["recipient_state"].isin(DMV), "amount"].sum() / tot if tot else 0
    dc_share = p.loc[p["recipient_state"] == "DC", "amount"].sum() / tot if tot else 0
    housing = p.loc[p["program_area_tags"].fillna("").str.contains("housing"), "amount"].sum() / tot if tot else 0
    lines.append(f"- DMV private foundations (F1) itemized 990-PF grants TY2020-TY2024: {len(p):,} rows, {money(tot)} from "
                 f"{n_f:,} foundations. Top 10 foundations = {top10:.0%} of dollars; top 1% ({max(1, int(n_f * 0.01))}) = "
                 f"{top1p:.0%}. Median grant ${p['amount'].median():,.0f}; {(p['amount'] <= 5000).mean():.0%} of rows are "
                 f"<= $5k. Recipients in DC/MD/VA get {dmv_share:.0%} of dollars (DC {dc_share:.0%}); purpose text tagged "
                 f"housing {housing:.0%}. Top: " + "; ".join(f"{fname.get(e, e)} {money(v)}" for e, v in byf.head(5).items()) + ".")

    # Calvary funders seen in XML vs earlier years
    cg = g[g["is_calvary"]]
    yr = cg.groupby("tax_year").agg(n=("amount", "size"), funders=("funder_ein", "nunique"), dollars=("amount", "sum"))
    lines.append("- Grant rows naming Calvary by funder tax year: " + "; ".join(
        f"TY{int(k)} {int(r.n)} rows / {int(r.funders)} funders / {money(r.dollars)}" for k, r in yr.iterrows()) +
        " (filing lag: TY2024 PF returns are still arriving in the 2025-2026 index releases).")

    # attachment-only 990-PF grant lists (placeholder rows only)
    pfr = fin[(fin["return_type"] == "990PF") & (fin["x_pf_grants_paid_total_line3a"].fillna(0) > 0)]
    att = pfr[(pfr["x_pf_paid_rows_n"] > 0) & (pfr["x_pf_paid_placeholder_n"] == pfr["x_pf_paid_rows_n"])]
    kf = set(u.loc[u["rule_id"].isin(["KF1", "KF2"]), "ein"])
    att_kf = att[att["ein"].isin(kf)].sort_values("tax_year").drop_duplicates("ein", keep="last")
    lines.append(f"- 990-PF grant lists filed only as attachments (every itemized row is a placeholder such as \"SEE "
                 f"ATTACHED SCHEDULE\"): {len(att):,} returns, {money(att['x_pf_grants_paid_total_line3a'].sum())} of grants "
                 f"with no grantee names in the XML. Known Calvary funders (KF1/KF2) affected, so XML can't confirm their "
                 f"Calvary gifts: " + "; ".join(f"{r.x_filer_name} (TY{int(r.tax_year)})" for r in att_kf.itertuples()) + ".")

    text = "\n".join(lines)
    qs = ("- XML pulls: 990-PF grants to individuals (RecipientPersonNm with no organization keyword or charity status) "
          "are stored with name, city and zip blanked (state, amount, purpose kept), per the people-data rule. Confirm, "
          "or say if scholarship/assistance grants to individuals should be dropped entirely.\n"
          "- XML pulls: DAF1 sponsor Schedule I rows are kept only for DC/MD/VA recipients (national totals in "
          "interim/xml_daf_filter_totals.csv). Confirm the three-state cut is enough, or whether specific out-of-region "
          "women's/homeless orgs are wanted as comparators.")
    print(text)
    print(qs)
    if not a.dry_run:
        append_md("notes_for_analysis.md", "XML pulls", text)
        append_md("open_questions.md", "XML pulls", qs)
        log("52_xml_notes", f"- appended {len(lines)} observations to notes_for_analysis.md (XML pulls) and 2 questions "
                            "to open_questions.md")


if __name__ == "__main__":
    main()
