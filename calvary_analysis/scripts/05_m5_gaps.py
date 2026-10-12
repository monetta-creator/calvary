"""M5: Funder gap analysis. Funders who support Calvary's peers or the DC sector and do not yet support
Calvary; Calvary's lapsed funders; current funders with headroom; CRM-vs-filings reconciliation.
Output: chart_data/m5_00_candidate_funders.csv (the candidate base for M7 scoring)."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import style  # noqa: E402
from lib.common import ANALYSIS, CALVARY, CLEAN, core_peers, load, log, money, register_insight, save_chart_data, universe  # noqa: E402

S = "05_m5_gaps"
GR = ["grant_id", "purpose_text", "funder_id", "funder_ein", "funder_name_raw", "recipient_ein", "recipient_name_raw", "recipient_state", "tax_year",
      "amount", "cumulative_flag", "program_area_tags", "source_type", "source_id", "notes"]
g_all = load("fact_grants", usecols=GR)
excl = pd.read_csv(ANALYSIS / "config" / "landscape_exclusions.csv", dtype=str)
g_all = g_all[~g_all.funder_id.isin(set(excl.funder_id))]
filed = g_all[(g_all.cumulative_flag != 1) & g_all.source_type.isin(["pf_grants_paid", "schedule_i"]) & g_all.amount.notna()]
df = load("dim_funder", usecols=["funder_id", "ein", "funder_name", "funder_type", "state", "issue_focus_tags", "universes"]).set_index("funder_id")
peers = core_peers(); peer_eins = set(peers.ein); peer_short = peers.set_index("ein").name
dcs = set(universe("dc_sector"))
land = pd.read_csv(ANALYSIS / "chart_data" / "m4_00_funder_landscape_table.csv", dtype={"funder_id": str})
src = sorted(filed.source_id.unique())

win = filed[filed.tax_year.between(2020, 2024)]
cal_now = win[win.recipient_ein == CALVARY]
cal_funders_now = set(cal_now.funder_id)
cal_ever = filed[filed.recipient_ein == CALVARY]
cal_funders_ever = set(cal_ever.funder_id)
# funders that filed itemized returns in TY2023-24 (so absence of a Calvary grant is a real absence, not lag)
recent_itemized = set(filed[filed.tax_year >= 2023].funder_id)
placeholder_recent = set(g_all[(g_all.tax_year >= 2023) & g_all.notes.fillna("").str.contains("placeholder_row=1")].funder_id)
ftype = df.funder_type

# ------------------------------------------------------------------ G1: peer funders not funding Calvary (filings)
pw = win[win.recipient_ein.isin(peer_eins)]
pf = pw.groupby("funder_id").agg(peers_funded=("recipient_ein", "nunique"), peer_amount=("amount", "sum"), peer_grants=("amount", "size"),
                                 peer_years=("tax_year", "nunique"), median_peer_grant=("amount", "median"), max_peer_grant=("amount", "max"),
                                 last_peer_ty=("tax_year", "max"), peers_list=("recipient_ein", lambda s: "; ".join(sorted({peer_short[e] for e in s}))))
pf["funder_name"] = pf.index.map(df.funder_name); pf["funder_type"] = pf.index.map(ftype); pf["state"] = pf.index.map(df.state)
pf["gives_to_calvary_ty2020_24"] = pf.index.isin(cal_funders_now); pf["gave_to_calvary_ever"] = pf.index.isin(cal_funders_ever)
pf["itemized_ty2023plus"] = pf.index.isin(recent_itemized); pf["placeholder_ty2023plus"] = pf.index.isin(placeholder_recent)
g1 = pf[(~pf.gives_to_calvary_ty2020_24) & (pf.funder_type != "daf_sponsor") & (pf.peers_funded >= 2)].sort_values(["peers_funded", "peer_amount"], ascending=False)
g1 = g1.reset_index()
save_chart_data(g1, "m5_01_peer_funders_not_calvary", "Institutional funders of 2+ core peers with no filed grant to Calvary, TY2020-24", ["fact_grants", "dim_funder"], src, S,
                "DAF sponsors excluded; 'itemized_ty2023plus' = funder filed itemized grants recently, so the absence is current")
top = g1[g1.peers_funded >= 3].head(22).iloc[::-1]
f, ax = style.fig(10.5, 7.6)
names = [n.title().replace("'S", "'s").replace(" Inc", "")[:46] for n in top.funder_name]
cols = [style.SERIES["institutional"] if t in ("private_foundation", "community_foundation") else style.SERIES["other"] for t in top.funder_type]
bars = ax.barh(names, top.peers_funded, color=cols, height=0.62)
for b_, n, a, m in zip(bars, top.peers_funded, top.peer_amount, top.median_peer_grant):
    ax.annotate(f"{int(n)} peers · ${a/1e3:,.0f}K total · median grant ${m/1e3:,.0f}K", (n, b_.get_y() + b_.get_height() / 2), xytext=(4, 0), textcoords="offset points", va="center", fontsize=8, color=style.TEXT_2)
from matplotlib.patches import Patch  # noqa: E402
ax.legend(handles=[Patch(color=style.SERIES["institutional"], label="Private / community foundation"), Patch(color=style.SERIES["other"], label="Public charity grantmaker, corporate or federated")], loc="lower right")
ax.set_xlim(0, top.peers_funded.max() * 2.1); ax.set_xticks(range(0, int(top.peers_funded.max()) + 1, 2)); ax.set_xlabel("Core peers funded TY2020-24 (of 18)"); ax.grid(axis="y", visible=False); ax.grid(axis="x", visible=True); ax.tick_params(axis="y", labelsize=8.5)
style.finish(f, ax, "m5_01_peer_funders_not_calvary",
             f"{len(g1[g1.peers_funded >= 3])} institutional funders give to three or more of Calvary's peers and have no filed grant to Calvary; the largest, Clark Charitable ($7.8M to peers), was a spend-down and closed at the end of 2025",
             "fact_grants (990-PF and Schedule I rows naming the 18 provisional core peers, TY2020-24) cross-checked against rows naming Calvary; dim_funder",
             note="Venable Foundation appears in Calvary's CRM ($75K, 2023-26) but not yet in filings; treated as filing lag. Core peers are provisional.")

# ------------------------------------------------------------------ G2: lapsed Calvary funders
ce = cal_ever.groupby("funder_id").agg(first_ty=("tax_year", "min"), last_ty=("tax_year", "max"), total=("amount", "sum"), years=("tax_year", "nunique"), last_amount=("amount", lambda s: s[cal_ever.loc[s.index, "tax_year"] == cal_ever.loc[s.index, "tax_year"].max()].sum()))
ce["funder_name"] = ce.index.map(df.funder_name); ce["funder_type"] = ce.index.map(ftype)
ce["itemized_ty2023plus"] = ce.index.isin(recent_itemized); ce["placeholder_ty2023plus"] = ce.index.isin(placeholder_recent)
ce["peers_funded_ty2020_24"] = ce.index.map(pf.peers_funded).fillna(0).astype(int)
# A funder whose every grant to Calvary was a capital-campaign gift made a one-time grant by design; it has not lapsed
# (review fix-cycle finding N01: World Bank Community Connections Fund).
one_time = cal_ever.groupby("funder_id").purpose_text.agg(lambda t: t.fillna("").str.upper().str.contains("CAPITAL CAMPAIGN").all())
ce["one_time_capital"] = ce.index.map(one_time).fillna(False).astype(bool)
lapsed = ce[(ce.last_ty <= 2022) & ce.itemized_ty2023plus & (ce.funder_type != "daf_sponsor") & ~ce.one_time_capital].sort_values("total", ascending=False).reset_index()
lapsed["status"] = "lapsed (funder itemized TY2023+ with no Calvary grant)"
one_off = ce[(ce.last_ty <= 2022) & ce.one_time_capital & (ce.funder_type != "daf_sponsor")].sort_values("total", ascending=False).reset_index()
one_off["status"] = "one-time capital-campaign grant (not lapsed)"
unclear = ce[(ce.last_ty <= 2022) & ~ce.itemized_ty2023plus & (ce.funder_type != "daf_sponsor")].sort_values("total", ascending=False).reset_index()
unclear["status"] = "unclear (funder has no itemized TY2023+ filing in the data)"
unclear = unclear[~unclear.funder_id.isin(one_off.funder_id)]
lap = pd.concat([lapsed, one_off, unclear], ignore_index=True)
save_chart_data(lap, "m5_02_lapsed_funders", "Calvary funders in filings whose last grant was TY2022 or earlier", ["fact_grants", "dim_funder"], src, S)
f, ax = style.fig(10, 5.6)
d = lapsed.head(15).iloc[::-1]
names = [n.title().replace("'S", "'s").replace(" Inc", "")[:44] for n in d.funder_name]
bars = ax.barh(names, d.total, color=style.SERIES["individuals"], height=0.62)
for b_, v, ft_, lt in zip(bars, d.total, d.first_ty, d.last_ty):
    ax.annotate(f"${v/1e3:,.0f}K over TY{int(ft_)}-TY{int(lt)}", (v, b_.get_y() + b_.get_height() / 2), xytext=(4, 0), textcoords="offset points", va="center", fontsize=8.5, color=style.TEXT_2)
style.money_axis(ax, "K", "x"); ax.set_xlim(0, d.total.max() * 1.45); ax.grid(axis="y", visible=False); ax.grid(axis="x", visible=True)
style.finish(f, ax, "m5_02_lapsed_funders",
             f"{len(lapsed)} former institutional funders have filed itemized grant lists since TY2023 with nothing for Calvary; together they once gave {money(lapsed.total.sum())}",
             "fact_grants (990-PF and Schedule I rows naming Calvary, all years) and each funder's TY2023+ returns; dim_funder",
             note="A lapse in filings can still be a gift booked as a DAF or corporate gift; confirm against Calvary's CRM before outreach.")

# ------------------------------------------------------------------ G3: current funders with headroom (Calvary grant vs funder's typical peer grant)
cur = cal_now.groupby("funder_id").agg(calvary_total=("amount", "sum"), calvary_years=("tax_year", "nunique"), calvary_median=("amount", "median"), calvary_max=("amount", "max"), last_ty=("tax_year", "max"))
cur["calvary_per_year"] = cur.calvary_total / cur.calvary_years
cur = cur.join(pf[["peers_funded", "median_peer_grant", "max_peer_grant", "peer_amount"]], how="left")
cur["funder_name"] = cur.index.map(df.funder_name); cur["funder_type"] = cur.index.map(ftype)
cur["headroom_ratio"] = cur.median_peer_grant / cur.calvary_median
cur["headroom_to_max_peer_grant"] = cur.max_peer_grant - cur.calvary_max
head = cur[(cur.funder_type != "daf_sponsor") & (cur.peers_funded >= 2)].sort_values("headroom_to_max_peer_grant", ascending=False).reset_index()
save_chart_data(head, "m5_03_current_funder_headroom", "Calvary's current institutional funders: Calvary grant size vs the same funder's grants to core peers", ["fact_grants", "dim_funder"], src, S)
d = head[(head.headroom_to_max_peer_grant >= 5000) & (head.calvary_max >= 1000)].head(12).iloc[::-1]
f, ax = style.fig(10.5, 6.4)
names = [n.title().replace("'S", "'s").replace(" Inc", "")[:44] for n in d.funder_name]
y = np.arange(len(d)); h = 0.38
ax.barh(y + h / 2, d.calvary_max, h, color=style.SERIES["government"], label="Largest grant to Calvary (TY2020-24)")
ax.barh(y - h / 2, d.max_peer_grant, h, color=style.PEER_COLOR, label="Largest grant to a core peer (TY2020-24)")
for yi, (a, b_, p) in enumerate(zip(d.calvary_max, d.max_peer_grant, d.peers_funded)):
    ax.annotate(f"${a/1e3:,.0f}K", (a, yi + h / 2), xytext=(3, 0), textcoords="offset points", va="center", fontsize=7.5, color=style.TEXT_2)
    ax.annotate(f"${b_/1e3:,.0f}K ({int(p)} peers)", (b_, yi - h / 2), xytext=(3, 0), textcoords="offset points", va="center", fontsize=7.5, color=style.TEXT_2)
ax.set_yticks(y, names); style.money_axis(ax, "K", "x"); ax.set_xlim(0, d.max_peer_grant.max() * 1.25); ax.grid(axis="y", visible=False); ax.grid(axis="x", visible=True); ax.legend(loc="lower right"); ax.tick_params(axis="y", labelsize=8.5)
style.finish(f, ax, "m5_03_current_funder_headroom",
             "Several of Calvary's current funders write much larger checks to peers: the upgrade conversation is with funders Calvary already knows",
             "fact_grants (990-PF and Schedule I, TY2020-24) rows naming Calvary vs rows naming the 18 provisional core peers; dim_funder",
             note="Largest single grants, not totals; a peer's larger grant may be capital or program-specific.")

# ------------------------------------------------------------------ G4: DC-sector majors (landscape) with no Calvary grant
maj = land[(~land.gives_to_calvary) & (land.dc_sector_amount >= 500_000)].copy()
maj["itemized_ty2023plus"] = maj.funder_id.isin(recent_itemized); maj["placeholder_ty2023plus"] = maj.funder_id.isin(placeholder_recent)
maj["gave_to_calvary_ever"] = maj.funder_id.isin(cal_funders_ever)
maj["mission_share"] = maj.mission_tagged_amount / maj.dc_sector_amount
maj = maj.sort_values("dc_sector_amount", ascending=False).reset_index(drop=True)
save_chart_data(maj, "m5_04_dc_majors_not_calvary", "Institutional funders giving $500K+ to DC-sector organizations TY2020-24 with no filed grant to Calvary", ["fact_grants", "dim_funder"], src, S)

# ------------------------------------------------------------------ G5: web / list-only evidence (peer donor lists, Calvary lists, CRM)
web_types = ["annual_report", "support_page", "web", "crm", "audit_note"]
lists = g_all[g_all.source_type.isin(web_types)]
cal_list = set(lists[lists.recipient_ein == CALVARY].funder_id)
peer_list = lists[lists.recipient_ein.isin(peer_eins)].groupby("funder_id").agg(peers_listed=("recipient_ein", "nunique"), funder_name=("funder_name_raw", "first"))
peer_list["funder_type"] = peer_list.index.map(ftype).fillna("unknown (no EIN match)")
web_gap = peer_list[(peer_list.peers_listed >= 2) & ~peer_list.index.isin(cal_list) & ~peer_list.index.isin(cal_funders_now) & (peer_list.funder_name.str.len() > 3)].sort_values("peers_listed", ascending=False).reset_index()
save_chart_data(web_gap, "m5_05_web_list_gaps", "Funders named on 2+ peer donor lists but on no Calvary list or filing", ["fact_grants"], sorted(lists.source_id.unique()), S,
                "web lists are undated 'supporters' lists without amounts; only 6 peers post donor lists")
# CRM reconciliation
crm = pd.read_csv(CLEAN / "supp_crm_cash_verification.csv", dtype={"funder_ein": str})
crm_sum = crm.cash_verified.value_counts().rename_axis("status").reset_index(name="funders")
crm_sum["crm_total"] = crm_sum.status.map(crm.groupby("cash_verified").crm_total.sum())
save_chart_data(crm_sum, "m5_06_crm_reconciliation", "Calvary CRM funders (2023-26) reconciled against funders' own filings", ["supp_crm_cash_verification"], ["input_crm_funders_2023_2026"], S)
f, ax = style.fig(10, 4.2)
order = ["confirmed_in_window", "confirmed_earlier_only", "attachment_only_list", "no_filing_rows", "not_exempt_filer"]
lab = {"confirmed_in_window": "Confirmed in funder's TY2023+ filing", "confirmed_earlier_only": "Confirmed only in earlier filings", "attachment_only_list": "Funder files 'see attached' lists (unverifiable)", "no_filing_rows": "Exempt filer, no Calvary row found", "not_exempt_filer": "Corporate / no public filing"}
cs = crm_sum.set_index("status").reindex(order)
bars = ax.barh([lab[o] for o in order][::-1], cs.crm_total.values[::-1], color=[style.SERIES["institutional"], style.SERIES["individuals"], style.PEER_COLOR, style.PEER_COLOR, style.SERIES["other"]][::-1], height=0.62)
for b_, v, n in zip(bars, cs.crm_total.values[::-1], cs.funders.values[::-1]):
    ax.annotate(f"${v/1e6:,.2f}M · {int(n)} funders", (v, b_.get_y() + b_.get_height() / 2), xytext=(4, 0), textcoords="offset points", va="center", fontsize=8.5, color=style.TEXT_2)
style.money_axis(ax, "M", "x"); ax.set_xlim(0, cs.crm_total.max() * 1.3); ax.grid(axis="y", visible=False); ax.grid(axis="x", visible=True)
style.finish(f, ax, "m5_06_crm_reconciliation",
             f"Only {cs.loc['confirmed_in_window','crm_total']/cs.crm_total.sum():.0%} of the CRM's ${cs.crm_total.sum()/1e6:,.1f}M in 2023-26 institutional giving is verifiable in funders' own filings; the rest is corporate, unfiled or 'see attached'",
             "supp_crm_cash_verification (Calvary CRM export 2023-26 vs 990-PF / Schedule I rows); funders' filings TY2022+",
             note="CRM totals are cumulative over an unconfirmed window and may include in-kind or pro bono value (assumptions A1-A2).")

# ------------------------------------------------------------------ candidate base for M7
cand = pd.DataFrame({"funder_id": sorted(set(g1.funder_id) | set(lapsed.funder_id) | set(head.funder_id) | set(maj.funder_id) | set(cur.index))})
cand["funder_name"] = cand.funder_id.map(df.funder_name); cand["funder_type"] = cand.funder_id.map(ftype); cand["state"] = cand.funder_id.map(df.state)
cand["issue_focus_tags"] = cand.funder_id.map(df.issue_focus_tags)
cand["gives_to_calvary_ty2020_24"] = cand.funder_id.isin(cal_funders_now); cand["gave_to_calvary_ever"] = cand.funder_id.isin(cal_funders_ever)
cand["on_calvary_list_or_crm"] = cand.funder_id.isin(cal_list)
cand["peers_funded"] = cand.funder_id.map(pf.peers_funded).fillna(0).astype(int); cand["peer_amount"] = cand.funder_id.map(pf.peer_amount).fillna(0)
cand["median_peer_grant"] = cand.funder_id.map(pf.median_peer_grant); cand["max_peer_grant"] = cand.funder_id.map(pf.max_peer_grant); cand["peer_years"] = cand.funder_id.map(pf.peer_years).fillna(0).astype(int)
cand["peers_list"] = cand.funder_id.map(pf.peers_list)
L = land.set_index("funder_id")
for c in ["dc_sector_amount", "dc_sector_recipients", "years_active", "median_grant", "p75_grant", "max_grant", "mission_tagged_amount", "placeholder_years", "dmv_share_of_all", "dc_sector_share_of_all", "total_grants_all_recipients"]:
    cand[c] = cand.funder_id.map(L[c])
cand["calvary_total_ty2020_24"] = cand.funder_id.map(cur.calvary_total).fillna(0); cand["calvary_max_grant"] = cand.funder_id.map(cur.calvary_max)
cand["calvary_last_ty"] = cand.funder_id.map(ce.last_ty)
cand["itemized_ty2023plus"] = cand.funder_id.isin(recent_itemized); cand["placeholder_ty2023plus"] = cand.funder_id.isin(placeholder_recent)
cand["gap_category"] = np.select(
    [cand.gives_to_calvary_ty2020_24 & cand.funder_id.isin(head.funder_id), cand.gives_to_calvary_ty2020_24, cand.funder_id.isin(lapsed.funder_id),
     cand.funder_id.isin(g1.funder_id) & (cand.peers_funded >= 3), cand.funder_id.isin(g1.funder_id), cand.funder_id.isin(maj.funder_id)],
    ["current: headroom vs peers", "current", "lapsed", "peer funder (3+ peers), not Calvary", "peer funder (2 peers), not Calvary", "DC-sector major, not Calvary"], default="other")
cand = cand.sort_values(["gap_category", "peers_funded", "dc_sector_amount"], ascending=[True, False, False]).reset_index(drop=True)
save_chart_data(cand, "m5_00_candidate_funders", "Candidate funder base for scoring (M7): current, lapsed, peer-funder and DC-major gaps with evidence fields", ["fact_grants", "dim_funder", "supp_crm_cash_verification"], src, S)

print(g1.head(30)[["funder_name", "funder_type", "peers_funded", "peer_amount", "median_peer_grant", "itemized_ty2023plus", "placeholder_ty2023plus", "peers_list"]].to_string())
print(lapsed[["funder_name", "funder_type", "first_ty", "last_ty", "total", "peers_funded_ty2020_24"]].to_string())
print(unclear[["funder_name", "funder_type", "first_ty", "last_ty", "total"]].head(15).to_string())
print(head.head(15)[["funder_name", "funder_type", "calvary_max", "calvary_total", "peers_funded", "median_peer_grant", "max_peer_grant"]].to_string())
print(maj.head(25)[["funder_name", "funder_type", "state", "dc_sector_amount", "dc_sector_recipients", "peers_funded", "mission_share", "itemized_ty2023plus", "placeholder_ty2023plus"]].to_string())
print(web_gap.head(25).to_string()); print(crm_sum.to_string()); print(cand.gap_category.value_counts())

register_insight("M5-01", "M5", f"{len(g1[g1.peers_funded >= 3])} institutional funders give to three or more of Calvary's 18 peers and have no filed grant to Calvary; {len(g1)} give to two or more.",
                 "m5_01 with open status from config/guideline_notes.csv: of the 23, six are channels (Gifts for the Homeless, T. Rowe Price Program, Capital Area Food Bank, America's Charities, JPMorgan Chase matching gifts, Give Lively), Clark has closed (spend-down ended 2025) and Venable is closed to new applicants, leaving 15 grantmakers; Schattner, Bunting and Bechtel fund four peers each, and the three-peer names depend on the provisional peer set.",
                 ["m5_01_peer_funders_not_calvary"], ["fact_grants", "dim_funder"], f"{len(g1)} funders", "high",
                 "The 15 grantmakers are the warmest cold prospects because they fund Calvary's model already; the route is an introduction through the peers they fund, and Schattner is invitation-only.", "both")
register_insight("M5-02", "M5", f"{len(lapsed)} former institutional funders filed itemized grant lists since TY2023 with nothing for Calvary; they once gave {money(lapsed.total.sum())} in total.",
                 "m5_02; " + ", ".join(lapsed.head(6).funder_name.str.title()), ["m5_02_lapsed_funders"], ["fact_grants", "dim_funder"], money(lapsed.total.sum()), "medium",
                 "Re-engagement is cheaper than acquisition; check the CRM for gifts routed through DAFs or corporate channels first.", "both")
register_insight("M5-03", "M5", f"{int((head.headroom_to_max_peer_grant > 0).sum())} of Calvary's current institutional funders that also fund two or more peers have written larger single grants to a core peer than to Calvary.",
                 "m5_03: largest grant to Calvary vs largest grant to a peer, TY2020-24", ["m5_03_current_funder_headroom"], ["fact_grants", "dim_funder"], "upgrade headroom", "medium",
                 "An upgrade ask to known funders is the fastest institutional money; pair it with the multi-year framing.", "both")
register_insight("M5-04", "M5", f"Only {cs.loc['confirmed_in_window','crm_total']/cs.crm_total.sum():.0%} of the CRM's ${cs.crm_total.sum()/1e6:,.1f}M in 2023-26 institutional giving is verifiable in funders' own filings; corporate givers with no public filing (MGAC, IMF, Latham, Frontier Co-op) are ${cs.loc['not_exempt_filer','crm_total']/1e6:,.1f}M and 'see attached' filers (Philip L. Graham, Clark-Winchcole, Kay, Herb Block) ${cs.loc['attachment_only_list','crm_total']/1e6:,.1f}M.",
                 "m5_06 (supp_crm_cash_verification)", ["m5_06_crm_reconciliation"], ["supp_crm_cash_verification"], f"{cs.loc['confirmed_in_window','crm_total']/cs.crm_total.sum():.0%} verifiable", "medium",
                 "Corporate relationships are a larger share of Calvary's private money than the filings show; the pipeline must treat them as a separate, relationship-led track.", "both")
log(S, [f"G1 peer-funder gaps {len(g1)} (>=3 peers: {len(g1[g1.peers_funded>=3])}); lapsed {len(lapsed)} + unclear {len(unclear)}; headroom {int((head.headroom_to_max_peer_grant>0).sum())}; DC majors {len(maj)}; web-only {len(web_gap)}",
        f"candidate base {len(cand)} funders written to m5_00_candidate_funders.csv"])
