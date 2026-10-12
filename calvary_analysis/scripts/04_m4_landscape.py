"""M4: Funder landscape. Who funds Calvary's space in DC and the DMV, at what scale, how concentrated,
and how giving shifted TY2020-24. Two lenses: (a) grants to DC-sector organizations (homelessness, housing,
DV, human services and adjacent codes in DC); (b) DMV grants tagged housing / DV / women.
Produces the funder landscape table that M5 and M7 build on."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import style  # noqa: E402
from lib.common import CALVARY, core_peers, load, log, money, register_insight, save_chart_data, universe  # noqa: E402

S = "04_m4_landscape"
GR = ["grant_id", "funder_id", "funder_ein", "funder_name_raw", "recipient_ein", "recipient_name_raw", "recipient_state", "tax_year",
      "amount", "cumulative_flag", "program_area_tags", "source_type", "source_id", "notes"]
gr = load("fact_grants", usecols=GR)
gr = gr[(gr.cumulative_flag != 1) & gr.source_type.isin(["pf_grants_paid", "schedule_i"]) & gr.tax_year.between(2020, 2024) & gr.amount.notna()]
gr["placeholder"] = gr.notes.fillna("").str.contains("placeholder_row=1")
excl = pd.read_csv(Path(__file__).resolve().parents[1] / "config" / "landscape_exclusions.csv", dtype=str)
gr = gr[~gr.funder_id.isin(set(excl.funder_id))]   # see config/landscape_exclusions.csv (Gates, TCP)
df = load("dim_funder", usecols=["funder_id", "funder_name", "funder_type", "state", "issue_focus_tags", "universes"]).set_index("funder_id")
gr["funder_type"] = gr.funder_id.map(df.funder_type).fillna("other")
gr["funder_name"] = gr.funder_id.map(df.funder_name).fillna(gr.funder_name_raw)
gr["is_daf"] = gr.funder_type == "daf_sponsor"
dcs = set(universe("dc_sector")); peers = set(core_peers().ein)
gr["to_dc_sector"] = gr.recipient_ein.isin(dcs)
gr["to_calvary"] = gr.recipient_ein == CALVARY
gr["to_peer"] = gr.recipient_ein.isin(peers)
tags = gr.program_area_tags.fillna("")
gr["mission_tag"] = tags.str.contains("housing|dv|women")
gr["to_dmv"] = gr.recipient_state.isin(["DC", "MD", "VA"])
src = sorted(gr.source_id.unique())
INST_TYPES = ["private_foundation", "community_foundation", "corporate_foundation", "public_charity_grantmaker", "federated_giving"]

# ------------------------------------------------------------------ lens A: grants to DC-sector organizations
a = gr[gr.to_dc_sector]
tot_a = a.amount.sum()
by_ty = a.groupby(["tax_year", "is_daf"]).amount.sum().unstack(fill_value=0).rename(columns={False: "institutional_and_other", True: "daf_sponsors"}).reset_index()
by_ty["funders"] = a.groupby("tax_year").funder_id.nunique().values
by_ty["recipients"] = a.groupby("tax_year").recipient_ein.nunique().values
by_type = a.groupby("funder_type").agg(amount=("amount", "sum"), funders=("funder_id", "nunique"), grants=("amount", "size"), median_grant=("amount", "median")).sort_values("amount", ascending=False).reset_index()
by_type["share"] = by_type.amount / tot_a
save_chart_data(by_ty, "m4_01_dc_sector_by_year", "Grants to DC-sector organizations by funder tax year: institutional vs DAF", ["fact_grants", "dim_funder", "dim_universe_membership"], src, S, "TY2024 partial, TY2025 excluded")
save_chart_data(by_type, "m4_02_dc_sector_by_funder_type", "Grants to DC-sector organizations TY2020-24 by funder type", ["fact_grants", "dim_funder", "dim_universe_membership"], src, S)

f, ax = style.fig(10, 5.4)
lab = by_ty.tax_year.astype(int).astype(str).radd("TY")
ax.bar(lab, by_ty.institutional_and_other, color=style.SERIES["institutional"], width=0.62, label="Institutional funders (foundations, corporate, federated)")
ax.bar(lab, by_ty.daf_sponsors, bottom=by_ty.institutional_and_other, color=style.SERIES["daf"], width=0.62, label="DAF sponsors (donor intermediaries)", edgecolor="white", linewidth=1.5)
for i, (x1, x2, n) in enumerate(zip(by_ty.institutional_and_other, by_ty.daf_sponsors, by_ty.funders)):
    ax.text(i, x1 + x2 + 2e6, f"${(x1+x2)/1e6:,.0f}M · {n} funders", ha="center", fontsize=8.5, color=style.TEXT_2)
style.money_axis(ax); ax.set_ylim(0, (by_ty.institutional_and_other + by_ty.daf_sponsors).max() * 1.18); ax.legend(loc="upper left")
style.finish(f, ax, "m4_01_dc_sector_by_year",
             f"DMV funders put about ${tot_a/1e6/5:,.0f}M a year into DC homelessness, housing, DV and human-services organizations, {by_type.set_index('funder_type').loc['daf_sponsor','share']:.0%} of it through donor-advised funds",
             "fact_grants (990-PF and Schedule I, TY2020-24, non-cumulative) to dc_sector recipients; dim_funder",
             note="Funder tax years; TY2024 returns are partly filed so the last bar understates. DAF sponsor Schedule I rows are kept for DC/MD/VA recipients only.")

# ------------------------------------------------------------------ funder landscape table (institutional funders to DC sector)
inst = a[~a.is_daf]
cal_funders = set(gr[gr.to_calvary].funder_id)
peer_counts = gr[gr.to_peer].groupby("funder_id").recipient_ein.nunique()
peer_amt = gr[gr.to_peer].groupby("funder_id").amount.sum()
cal_amt = gr[gr.to_calvary].groupby("funder_id").amount.sum()
ph_funders = gr[gr.placeholder].groupby("funder_id").tax_year.nunique()
all_dmv = gr[gr.to_dmv].groupby("funder_id").amount.sum()
all_any = gr.groupby("funder_id").amount.sum()
ft = inst.groupby("funder_id").agg(funder_name=("funder_name", "first"), funder_type=("funder_type", "first"), dc_sector_amount=("amount", "sum"),
                                   dc_sector_recipients=("recipient_ein", "nunique"), dc_sector_grants=("amount", "size"), years_active=("tax_year", "nunique"),
                                   median_grant=("amount", "median"), p75_grant=("amount", lambda s: s.quantile(.75)), max_grant=("amount", "max"),
                                   mission_tagged_amount=("amount", lambda s: s[inst.loc[s.index, "mission_tag"]].sum())).reset_index()
ft["state"] = ft.funder_id.map(df.state); ft["issue_focus_tags"] = ft.funder_id.map(df.issue_focus_tags)
ft["gives_to_calvary"] = ft.funder_id.isin(cal_funders); ft["calvary_amount"] = ft.funder_id.map(cal_amt).fillna(0)
ft["peers_funded"] = ft.funder_id.map(peer_counts).fillna(0).astype(int); ft["peer_amount"] = ft.funder_id.map(peer_amt).fillna(0)
ft["placeholder_years"] = ft.funder_id.map(ph_funders).fillna(0).astype(int)
ft["total_grants_all_recipients"] = ft.funder_id.map(all_any); ft["dmv_share_of_all"] = ft.funder_id.map(all_dmv) / ft.total_grants_all_recipients
ft["dc_sector_share_of_all"] = ft.dc_sector_amount / ft.total_grants_all_recipients
ft = ft.sort_values("dc_sector_amount", ascending=False).reset_index(drop=True)
ft["rank"] = ft.index + 1
ft["cum_share"] = ft.dc_sector_amount.cumsum() / ft.dc_sector_amount.sum()
save_chart_data(ft, "m4_00_funder_landscape_table", "Institutional funders of DC-sector organizations TY2020-24 (landscape table; base for M5 and M7)",
                ["fact_grants", "dim_funder", "dim_universe_membership"], src, S, "institutional = not a DAF sponsor; placeholder_years = returns with 'see attached' grant lists (recipients unknown)")

# ------------------------------------------------------------------ m4_03 top institutional funders of the DC sector
top = ft.head(25).iloc[::-1]
f, ax = style.fig(10.5, 8.2)
colors = [style.SERIES["institutional"] if g else style.PEER_COLOR for g in top.gives_to_calvary]
names = [n.title().replace("'S", "'s").replace(" Inc", "").replace(" Dba ", " dba ")[:52] for n in top.funder_name]
bars = ax.barh(names, top.dc_sector_amount, color=colors, height=0.62)
for b_, v, n, p in zip(bars, top.dc_sector_amount, top.dc_sector_recipients, top.peers_funded):
    ax.annotate(f"${v/1e6:,.1f}M · {n} DC orgs · {p} core peers", (v, b_.get_y() + b_.get_height() / 2), xytext=(4, 0), textcoords="offset points", va="center", fontsize=8, color=style.TEXT_2)
from matplotlib.patches import Patch  # noqa: E402
ax.legend(handles=[Patch(color=style.SERIES["institutional"], label="Gives to Calvary (TY2020-24 filings)"), Patch(color=style.PEER_COLOR, label="No filed grant to Calvary")], loc="lower right")
style.money_axis(ax, "M", "x"); ax.set_xlim(0, top.dc_sector_amount.max() * 1.45); ax.grid(axis="y", visible=False); ax.grid(axis="x", visible=True); ax.tick_params(axis="y", labelsize=8.5)
style.finish(f, ax, "m4_03_top_institutional_funders",
             f"Of the 25 largest institutional funders of DC's homelessness and human-services organizations, {int(top.gives_to_calvary.sum())} already give to Calvary",
             "fact_grants (990-PF and Schedule I, TY2020-24) to dc_sector recipients; dim_funder",
             note="Excludes the Gates Foundation (its DC recipients are global-development and research organizations) and TCP (government pass-through); see config/landscape_exclusions.csv.")

# ------------------------------------------------------------------ m4_04 concentration
conc = pd.DataFrame({"rank": ft["rank"], "cum_share": ft.cum_share, "funder_name": ft.funder_name, "dc_sector_amount": ft.dc_sector_amount})
n_f = len(ft); top1pct = int(np.ceil(n_f * 0.01)); top10 = ft.head(10).dc_sector_amount.sum() / ft.dc_sector_amount.sum()
save_chart_data(conc, "m4_04_concentration", "Cumulative share of institutional DC-sector grant dollars by funder rank", ["fact_grants", "dim_funder"], src, S,
                f"{n_f} institutional funders; top 10 = {top10:.0%}; top 1% ({top1pct} funders) = {ft.head(top1pct).dc_sector_amount.sum()/ft.dc_sector_amount.sum():.0%}")
f, ax = style.fig(10, 5)
ax.plot(conc["rank"], conc.cum_share, color=style.SERIES["institutional"], lw=2.2)
ax.set_xscale("log"); ax.xaxis.set_minor_formatter(plt.NullFormatter()); ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:,.0f}"))
style.pct_axis(ax); ax.set_ylim(0, 1.02); ax.set_xlabel("Funder rank by dollars to DC-sector organizations (log scale)"); ax.set_ylabel("Cumulative share of dollars")
for r_ in [10, 50, 100]:
    v = float(conc[conc["rank"] == r_].cum_share.iloc[0]) if r_ <= n_f else None
    if v:
        ax.plot([r_], [v], marker="o", color=style.INK, ms=7, markeredgecolor="white"); ax.annotate(f"top {r_}: {v:.0%}", (r_, v), xytext=(6, -14), textcoords="offset points", fontsize=8.5, color=style.TEXT_2)
style.finish(f, ax, "m4_04_concentration",
             f"Ten institutional funders supply {top10:.0%} of foundation dollars to DC's sector; the other {n_f-10:,} funders share the rest in small grants",
             "fact_grants (990-PF and Schedule I, TY2020-24) to dc_sector recipients; dim_funder")

# ------------------------------------------------------------------ m4_05 grant size by funder type
gs = a.groupby("funder_type").amount.describe(percentiles=[.25, .5, .75, .9])[["count", "25%", "50%", "75%", "90%", "mean"]].reset_index()
gs = gs[gs["count"] >= 100].sort_values("50%", ascending=True)
save_chart_data(gs, "m4_05_grant_size_by_type", "Grant size distribution to DC-sector organizations by funder type", ["fact_grants", "dim_funder"], src, S)
f, ax = style.fig(10, 4.8)
for i, r in gs.iterrows():
    y = list(gs.funder_type).index(r.funder_type)
    ax.plot([r["25%"], r["75%"]], [y, y], color=style.PEER_COLOR, lw=10, solid_capstyle="butt")
    ax.plot([r["50%"]], [y], marker="|", ms=18, color=style.INK, mew=2)
    ax.plot([r["90%"]], [y], marker="o", ms=7, color=style.SERIES["institutional"], markeredgecolor="white")
    ax.text(r["90%"] * 1.15, y, f"median ${r['50%']/1e3:,.0f}K · p90 ${r['90%']/1e3:,.0f}K · n={int(r['count']):,}", va="center", fontsize=8.5, color=style.TEXT_2)
ax.set_yticks(range(len(gs)), [t.replace("_", " ") for t in gs.funder_type]); ax.set_xscale("log"); ax.xaxis.set_minor_formatter(plt.NullFormatter())
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v/1e3:,.0f}K" if v < 1e6 else f"${v/1e6:,.0f}M")); ax.set_xlim(1e3, 3e7); ax.grid(axis="y", visible=False); ax.grid(axis="x", visible=True)
ax.text(0.005, len(gs) - 0.45, "bar: 25th-75th percentile; tick: median; dot: 90th percentile", fontsize=8, color=style.TEXT_MUTED, transform=ax.get_yaxis_transform())
style.finish(f, ax, "m4_05_grant_size_by_type",
             "The typical foundation grant to a DC-sector organization is $10-25K; six-figure grants are the top decile from community and private foundations",
             "fact_grants (990-PF and Schedule I, TY2020-24) to dc_sector recipients; dim_funder")

# ------------------------------------------------------------------ m4_06 DAF sponsors to DC sector
daf = a[a.is_daf].groupby(["funder_name", "tax_year"]).amount.sum().unstack(fill_value=0)
daf["total"] = daf.sum(axis=1); daf = daf.sort_values("total", ascending=False).head(8)
dafr = daf.reset_index()
save_chart_data(dafr, "m4_06_daf_sponsors", "DAF sponsor grants to DC-sector organizations by sponsor and tax year", ["fact_grants", "dim_funder"], src, S, "Schedule I rows kept for DC/MD/VA recipients only")
f, ax = style.fig(10, 5.2)
names = [n.title().replace(" Inc", "")[:40] for n in daf.index[::-1]]
bars = ax.barh(names, daf.total.values[::-1], color=style.SERIES["daf"], height=0.62)
for b_, v in zip(bars, daf.total.values[::-1]):
    ax.annotate(f"${v/1e6:,.0f}M", (v, b_.get_y() + b_.get_height() / 2), xytext=(4, 0), textcoords="offset points", va="center", fontsize=8.5, color=style.TEXT_2)
style.money_axis(ax, "M", "x"); ax.set_xlim(0, daf.total.max() * 1.15); ax.grid(axis="y", visible=False); ax.grid(axis="x", visible=True)
style.finish(f, ax, "m4_06_daf_sponsors",
             f"Fidelity Charitable alone moved ${daf.total.iloc[0]/1e6:,.0f}M of donor-advised money into DC-sector organizations in five years, more than any foundation",
             "fact_grants (Schedule I of national DAF sponsors, DC/MD/VA recipients, TY2020-24); dim_funder",
             note="DAF sponsors are intermediaries: the decisions sit with individual donors, so these are a cultivation channel, not a grant pipeline.")

# ------------------------------------------------------------------ m4_07 what the money is for (program-area tags, institutional, DC sector)
tg = inst.assign(tag=inst.program_area_tags.fillna("other").str.split(";")).explode("tag")
tg = tg.groupby("tag").agg(amount=("amount", "sum"), grants=("amount", "size"), funders=("funder_id", "nunique")).sort_values("amount", ascending=False).reset_index()
tg["share_of_tagged_dollars"] = tg.amount / tg.amount.sum()
save_chart_data(tg, "m4_07_purpose_tags", "Institutional DC-sector grant dollars by program-area tag (purpose text)", ["fact_grants", "dim_program_area"], src, S, "a grant can carry several tags")
f, ax = style.fig(10, 5.2)
t2 = tg[tg.tag != "other"].head(10).iloc[::-1]
cols = [style.SERIES["government"] if t in ("housing", "dv", "women") else style.PEER_COLOR for t in t2.tag]
bars = ax.barh(t2.tag.str.replace("_", " "), t2.amount, color=cols, height=0.62)
for b_, v, n in zip(bars, t2.amount, t2.funders):
    ax.annotate(f"${v/1e6:,.0f}M · {n} funders", (v, b_.get_y() + b_.get_height() / 2), xytext=(4, 0), textcoords="offset points", va="center", fontsize=8.5, color=style.TEXT_2)
style.money_axis(ax, "M", "x"); ax.set_xlim(0, t2.amount.max() * 1.3); ax.grid(axis="y", visible=False); ax.grid(axis="x", visible=True)
style.finish(f, ax, "m4_07_purpose_tags",
             "Most institutional money to the DC sector is unrestricted or untagged; grants whose purpose names housing, DV or women are a minority",
             "fact_grants purpose_text tagged with dim_program_area keywords (institutional funders, dc_sector recipients, TY2020-24)",
             note="Tags come from the funder's purpose text; 'general operating' is the largest named purpose. Dollars tagged housing/DV/women are highlighted.")

# ------------------------------------------------------------------ lens B: DMV grants tagged housing / DV / women
b = gr[gr.to_dmv & gr.mission_tag]
tb = b[~b.is_daf].groupby(["funder_id", "funder_name", "funder_type"]).agg(amount=("amount", "sum"), recipients=("recipient_ein", "nunique"), dc_amount=("amount", lambda s: s[b.loc[s.index, "recipient_state"] == "DC"].sum())).reset_index().sort_values("amount", ascending=False)
tb["gives_to_calvary"] = tb.funder_id.isin(cal_funders); tb["peers_funded"] = tb.funder_id.map(peer_counts).fillna(0).astype(int)
tb["dc_share"] = tb.dc_amount / tb.amount
save_chart_data(tb, "m4_08_mission_tagged_funders", "Institutional funders of DMV grants tagged housing / DV / women, TY2020-24", ["fact_grants", "dim_funder", "dim_program_area"], src, S)
top = tb.head(20).iloc[::-1]
f, ax = style.fig(10.5, 7.2)
colors = [style.SERIES["institutional"] if g else style.PEER_COLOR for g in top.gives_to_calvary]
names = [n.title().replace("'S", "'s").replace(" Inc", "")[:48] for n in top.funder_name]
bars = ax.barh(names, top.amount, color=colors, height=0.62)
for b_, v, d, p in zip(bars, top.amount, top.dc_share, top.peers_funded):
    ax.annotate(f"${v/1e6:,.1f}M · {d:.0%} to DC · {p} core peers", (v, b_.get_y() + b_.get_height() / 2), xytext=(4, 0), textcoords="offset points", va="center", fontsize=8, color=style.TEXT_2)
ax.legend(handles=[Patch(color=style.SERIES["institutional"], label="Gives to Calvary"), Patch(color=style.PEER_COLOR, label="No filed grant to Calvary")], loc="lower right")
style.money_axis(ax, "M", "x"); ax.set_xlim(0, top.amount.max() * 1.5); ax.grid(axis="y", visible=False); ax.grid(axis="x", visible=True); ax.tick_params(axis="y", labelsize=8.5)
style.finish(f, ax, "m4_08_mission_tagged_funders",
             "The largest funders whose grant language names housing, DV or women are mostly Maryland and Virginia foundations that give little in DC",
             "fact_grants (990-PF and Schedule I, TY2020-24, DC/MD/VA recipients) with purpose text tagged housing, dv or women; dim_funder",
             note="Share to DC = share of each funder's mission-tagged dollars going to DC recipients.")

# ------------------------------------------------------------------ summary and insights
print(by_ty.to_string()); print(by_type.to_string())
print(ft.head(30)[["rank", "funder_name", "funder_type", "state", "dc_sector_amount", "dc_sector_recipients", "median_grant", "gives_to_calvary", "calvary_amount", "peers_funded", "placeholder_years"]].to_string())
print(gs.to_string()); print(tg.head(12).to_string()); print(tb.head(20)[["funder_name", "funder_type", "amount", "dc_share", "gives_to_calvary", "peers_funded"]].to_string())
inst_total = ft.dc_sector_amount.sum(); daf_total = a[a.is_daf].amount.sum()
register_insight("M4-01", "M4", f"DMV funders put about {money(tot_a/5)} a year into DC-sector organizations TY2020-24 ({money(tot_a)} total): {daf_total/tot_a:.0%} through DAF sponsors and {inst_total/tot_a:.0%} from {n_f:,} institutional funders.",
                 "m4_01, m4_02: by year and funder type", ["m4_01_dc_sector_by_year"], ["fact_grants", "dim_funder", "dim_universe_membership"], f"{money(tot_a/5)}/yr", "high",
                 "The pool is large relative to Calvary's $1M/yr of filed grants; the constraint is access, not supply.", "both")
register_insight("M4-02", "M4", f"The institutional pool is concentrated: the top 10 funders give {top10:.0%} of institutional dollars to the DC sector, and {int(ft.head(25).gives_to_calvary.sum())} of the top 25 already fund Calvary.",
                 "m4_03, m4_04", ["m4_03_top_institutional_funders", "m4_04_concentration"], ["fact_grants", "dim_funder"], f"top 10 = {top10:.0%}", "high",
                 "Calvary's institutional coverage of the majors is already broad; the next wins are deeper grants from current majors and the open large non-funders (Casey, Wal-Mart, Morningstar). Clark has closed, Meyer is closed to new applicants and Weinberg's grants center outside DC.", "both")
register_insight("M4-03", "M4", f"The typical institutional grant to a DC-sector organization is small (median {money(a[~a.is_daf].amount.median(), 'K')}); six-figure grants are the top decile and come from community and private foundations.",
                 "m4_05", ["m4_05_grant_size_by_type"], ["fact_grants", "dim_funder"], f"median {money(a[~a.is_daf].amount.median(), 'K')}", "high",
                 "Moving the needle by $0.5M needs a handful of six-figure, multi-year relationships, not dozens of new $10K grants.", "both")
register_insight("M4-04", "M4", f"Fidelity Charitable moved {money(daf.total.iloc[0])} into DC-sector organizations in five years, more than any foundation; DAF money is a donor-cultivation channel, not a grant pipeline.",
                 "m4_06", ["m4_06_daf_sponsors"], ["fact_grants", "dim_funder"], f"{money(daf_total)} DAF total", "high",
                 "Calvary's DAF receipts ($1.1M over five years, 25% of filed grants) track individual major donors; growth there is a major-gifts strategy.", "both")
register_insight("M4-05", "M4", "Most institutional money to the DC sector is general operating or untagged; grants whose purpose names housing, DV or women are a minority, and the biggest mission-tagged funders are Maryland and Virginia foundations that give little in DC.",
                 "m4_07, m4_08", ["m4_07_purpose_tags", "m4_08_mission_tagged_funders"], ["fact_grants", "dim_program_area", "dim_funder"], "minority of dollars", "medium",
                 "Mission language alone will not find the money; the funders to target are the DC general-support givers who already fund peers.", "consulting")
log(S, [f"lens A dc_sector TY2020-24 {tot_a:,.0f} ({len(a):,} rows, {a.funder_id.nunique()} funders); institutional {inst_total:,.0f} from {n_f} funders; DAF {daf_total:,.0f}",
        f"lens B mission-tagged DMV {b.amount.sum():,.0f} from {b.funder_id.nunique()} funders", "charts m4_01..m4_08 and landscape table written"])
