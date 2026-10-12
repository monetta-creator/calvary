"""M3: Peer benchmarking. Calvary vs 18 provisional core peers plus the two named comparators
(DWC, CBWC Institute / SheWorks) on revenue mix, size, growth, liquidity, funder base and resilience type,
plus sector distributions and diversifier case studies."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import style  # noqa: E402
from lib.common import CALVARY, NAMED, deflators, load, log, money, peer_set, register_insight, save_chart_data, universe  # noqa: E402

S = "03_m3_peers"
ps = peer_set()
eins = ps.ein.tolist()
short = ps.set_index("ein")["short"]
group = ps.set_index("ein")["group"]
tier = ps.set_index("ein")["tier"]
FIN_COLS = ["ein", "fiscal_year", "fye_month", "preferred", "total_revenue", "contributions_total", "government_grants",
            "program_service_revenue", "investment_income", "other_revenue", "special_events_net", "total_expenses",
            "fundraising_expenses", "net_assets_eoy", "cash_savings_eoy", "gov_share_of_revenue", "months_of_cash", "source_id"]
fin = load("fact_org_financials", usecols=FIN_COLS)
fin = fin[fin.preferred == 1]
pf = fin[fin.ein.isin(eins)].copy()
pf["short"] = pf.ein.map(short)
defl = deflators()
pf["rev_real"] = pf.total_revenue * pf.fiscal_year.map(defl)
src = sorted(pf.source_id.unique())

# Calvary's government share on the audit basis for FY<=2023 (line 1e distorts FY21), per M1
cal_audit = load("fact_org_financials", usecols=["ein", "fiscal_year", "return_type", "government_grants", "total_revenue"])
cal_audit = cal_audit[(cal_audit.ein == CALVARY) & (cal_audit.return_type == "audit")].set_index("fiscal_year")
cal_gs_audit = (cal_audit.government_grants / cal_audit.total_revenue)


def gov_share(row):
    if row.ein == CALVARY and row.fiscal_year in cal_gs_audit.index:
        return cal_gs_audit[row.fiscal_year]
    return row.gov_share_of_revenue


pf["gov_share"] = pf.apply(gov_share, axis=1)

# ------------------------------------------------------------------ benchmark table (latest 3 years FY2022-24)
win = pf[pf.fiscal_year.between(2022, 2024)]
latest = pf[pf.fiscal_year <= 2024].sort_values("fiscal_year").groupby("ein").tail(1).set_index("ein")
b19 = pf[pf.fiscal_year == 2019].set_index("ein").rev_real
b24 = pf[pf.fiscal_year == 2024].set_index("ein").rev_real
bench = pd.DataFrame({"ein": eins})
bench["org"] = bench.ein.map(short); bench["group"] = bench.ein.map(group); bench["tier"] = bench.ein.map(tier)
bench["revenue_fy2024"] = bench.ein.map(pf[pf.fiscal_year == 2024].set_index("ein").total_revenue)
bench["latest_fy"] = bench.ein.map(latest.fiscal_year)
bench["gov_share_fy2022_24_mean"] = bench.ein.map(win.groupby("ein").gov_share.mean())
bench["gov_share_latest"] = bench.ein.map(latest.gov_share)
bench["real_cagr_fy2019_24"] = bench.ein.map((b24 / b19) ** (1 / 5) - 1)
bench["months_of_cash_fy2024"] = bench.ein.map(pf[pf.fiscal_year == 2024].set_index("ein").months_of_cash)
bench["months_of_cash_fy2022_24_mean"] = bench.ein.map(win.groupby("ein").months_of_cash.mean())
bench["program_service_share_fy2022_24"] = bench.ein.map((win.groupby("ein").program_service_revenue.sum() / win.groupby("ein").total_revenue.sum()))
fe = win.groupby("ein").agg(fr=("fundraising_expenses", "sum"), ct=("contributions_total", "sum"), gg=("government_grants", "sum"))
bench["fundraising_cost_per_private_dollar_fy2022_24"] = bench.ein.map(fe.fr / (fe.ct - fe.gg.fillna(0)).clip(lower=1))


def typology(g):
    if pd.isna(g):
        return "unknown"
    return "government-anchored (≥65%)" if g >= 0.65 else ("mixed (35-65%)" if g >= 0.35 else "philanthropy-led (<35%)")


bench["resilience_type"] = bench.gov_share_fy2022_24_mean.map(typology)

# funder base from filings TY2020-24
GR = ["funder_id", "recipient_ein", "tax_year", "amount", "cumulative_flag", "source_type", "source_id"]
gr = load("fact_grants", usecols=GR)
gr = gr[gr.recipient_ein.isin(eins) & (gr.cumulative_flag != 1) & gr.source_type.isin(["pf_grants_paid", "schedule_i"]) & gr.tax_year.between(2020, 2024)]
ft = load("dim_funder", usecols=["funder_id", "funder_type"]).set_index("funder_id").funder_type
gr["is_daf"] = gr.funder_id.map(ft).eq("daf_sponsor")
fb = gr.groupby("recipient_ein").agg(filed_grants_ty2020_24=("amount", "sum"), funders=("funder_id", "nunique"))
fb["institutional_funders"] = gr[~gr.is_daf].groupby("recipient_ein").funder_id.nunique()
fb["institutional_amount"] = gr[~gr.is_daf].groupby("recipient_ein").amount.sum()
fb["daf_amount"] = gr[gr.is_daf].groupby("recipient_ein").amount.sum()
fb = fb.fillna(0)
fb["daf_share_of_filed"] = fb.daf_amount / fb.filed_grants_ty2020_24
bench = bench.merge(fb, left_on="ein", right_index=True, how="left")
rev5 = pf[pf.fiscal_year.between(2020, 2024)].groupby("ein").total_revenue.sum()
bench["institutional_per_revenue_dollar"] = bench.institutional_amount / bench.ein.map(rev5)
bench["note"] = np.where(bench.group == "named_comparator", "LA reference; DAF grants not captured (Schedule I kept for DC/MD/VA recipients only)", "")
bench.loc[bench.ein == "882046704", "note"] = "Founded 2022; SheWorks program starts after TY2024; LA reference"
bench = bench.sort_values(["group", "gov_share_fy2022_24_mean"], ascending=[True, False])
save_chart_data(bench, "m3_00_benchmark_table", "Peer benchmark table: Calvary, 18 provisional core peers, 2 named comparators",
                ["fact_org_financials", "fact_grants", "dim_funder", "dim_period"], src + sorted(gr.source_id.unique()), S,
                "gov share on 990 line 1e except Calvary FY<=2023 (audit basis); core peers are provisional")


def color_for(e):
    return style.CALVARY_COLOR if e == CALVARY else (style.NAMED_COLOR if e in NAMED else style.PEER_COLOR)


# ------------------------------------------------------------------ m3_01 government share ranked
d = bench.dropna(subset=["gov_share_fy2022_24_mean"]).sort_values("gov_share_fy2022_24_mean")
cb_gs = float(bench.set_index("ein").loc[CALVARY, "gov_share_fy2022_24_mean"])
f, ax = style.fig(10, 7.2)
bars = ax.barh(d.org, d.gov_share_fy2022_24_mean, color=[color_for(e) for e in d.ein], height=0.62)
for b_, v, r in zip(bars, d.gov_share_fy2022_24_mean, d.revenue_fy2024):
    ax.annotate(f"{v:.0%}   (rev {money(r, 'M', 1)})", (v, b_.get_y() + b_.get_height() / 2), xytext=(4, 0), textcoords="offset points", va="center", fontsize=8.5, color=style.TEXT_2)
ax.axvspan(0.35, 0.65, color=style.SURFACE_2, zorder=0)
ax.text(0.50, len(d) - 0.4, "mixed", ha="center", fontsize=8.5, color=style.TEXT_MUTED)
ax.text(0.17, len(d) - 0.4, "philanthropy-led", ha="center", fontsize=8.5, color=style.TEXT_MUTED)
ax.text(0.82, len(d) - 0.4, "government-anchored", ha="center", fontsize=8.5, color=style.TEXT_MUTED)
style.pct_axis(ax, "x"); ax.set_xlim(0, 1.25); ax.grid(axis="y", visible=False); ax.grid(axis="x", visible=True)
from matplotlib.patches import Patch  # noqa: E402
ax.legend(handles=[Patch(color=style.CALVARY_COLOR, label="Calvary"), Patch(color=style.PEER_COLOR, label="Core peers (provisional)"), Patch(color=style.NAMED_COLOR, label="Named comparators (LA, reference)")], loc="lower right")
style.finish(f, ax, "m3_01_gov_share_ranked",
             f"Calvary's {cb_gs:.0%} government share sits in the middle of its peers: below every DC DV provider and above the philanthropy-led models",
             "fact_org_financials (990 line 1e / total revenue, FY2022-24 mean; Calvary on the audit basis for FY22-23)",
             note="FY2022-24 mean smooths single-year reporting breaks. Core peers are provisional. CBWC Institute/SheWorks: FY2023-24 only.")

# ------------------------------------------------------------------ m3_02 size vs government share
d = bench.dropna(subset=["gov_share_fy2022_24_mean", "revenue_fy2024"])
f, ax = style.fig(10, 6.2)
ax.axhspan(0.65, 1.0, color=style.SURFACE_2, zorder=0); ax.axhspan(0, 0.35, color=style.SURFACE_2, zorder=0)
ax.scatter(d.revenue_fy2024, d.gov_share_fy2022_24_mean, s=90, c=[color_for(e) for e in d.ein], edgecolors="white", linewidths=1.5, zorder=3)
for _, r in d.iterrows():
    ax.annotate(r.org, (r.revenue_fy2024, r.gov_share_fy2022_24_mean), xytext=(6, 4), textcoords="offset points", fontsize=8,
                color=style.INK if r.ein == CALVARY else style.TEXT_2, fontweight="bold" if r.ein == CALVARY else "normal")
ax.set_xscale("log"); ax.set_xlim(1.2e6, 9e7); ax.xaxis.set_minor_formatter(plt.NullFormatter())
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v/1e6:,.0f}M"))
ax.set_xticks([2e6, 5e6, 1e7, 2e7, 5e7]); ax.set_xlabel("Total revenue FY2024 (log scale)")
style.pct_axis(ax); ax.set_ylim(0, 1.02); ax.set_ylabel("Government share of revenue, FY2022-24 mean")
ax.text(1.6e6, 0.98, "government-anchored", fontsize=8.5, color=style.TEXT_MUTED, va="top"); ax.text(1.6e6, 0.02, "philanthropy-led", fontsize=8.5, color=style.TEXT_MUTED)
style.finish(f, ax, "m3_02_size_vs_gov_share",
             "Peers that grew past $10M did it either with government (DWC, House of Ruth) or almost without it (Miriam's Kitchen); size does not require either path",
             "fact_org_financials (preferred rows): FY2024 revenue and FY2022-24 government share",
             note="Core peers are provisional; DWC and CBWC Institute are Los Angeles reference organizations.")

# ------------------------------------------------------------------ m3_03 real growth FY2019-24
d = bench.dropna(subset=["real_cagr_fy2019_24"]).sort_values("real_cagr_fy2019_24")
cb_growth = float(bench.set_index("ein").loc[CALVARY, "real_cagr_fy2019_24"])
f, ax = style.fig(10, 6.8)
bars = ax.barh(d.org, d.real_cagr_fy2019_24, color=[color_for(e) for e in d.ein], height=0.62)
for b_, v in zip(bars, d.real_cagr_fy2019_24):
    ax.annotate(f"{v:+.1%}", (v, b_.get_y() + b_.get_height() / 2), xytext=(4 if v >= 0 else -4, 0), textcoords="offset points", va="center", ha="left" if v >= 0 else "right", fontsize=8.5, color=style.TEXT_2)
ax.axvline(0, color=style.TEXT_2, lw=0.8); style.pct_axis(ax, "x"); ax.grid(axis="y", visible=False); ax.grid(axis="x", visible=True)
ax.set_xlim(d.real_cagr_fy2019_24.min() * 1.4, d.real_cagr_fy2019_24.max() * 1.25)
style.finish(f, ax, "m3_03_real_growth",
             f"Calvary grew {cb_growth:.1%} a year in real terms from FY19 to FY24, faster than all but three peers (My Sister's Place, DWC, DC SAFE)",
             "fact_org_financials (preferred rows), dim_period CPI-U; compound annual growth of 2024-dollar revenue FY2019-FY2024",
             note="FY2019 and FY2024 endpoints avoid Calvary's one-time FY22 award. CBWC Institute omitted (founded 2022).")

# ------------------------------------------------------------------ m3_04 months of cash
d = bench.dropna(subset=["months_of_cash_fy2024"]).sort_values("months_of_cash_fy2024")
f, ax = style.fig(10, 6.8)
bars = ax.barh(d.org, d.months_of_cash_fy2024, color=[color_for(e) for e in d.ein], height=0.62)
for b_, v in zip(bars, d.months_of_cash_fy2024):
    ax.annotate(f"{v:.1f}", (v, b_.get_y() + b_.get_height() / 2), xytext=(4, 0), textcoords="offset points", va="center", fontsize=8.5, color=style.TEXT_2)
ax.axvspan(3, 6, color=style.GOLD_LIGHT, alpha=0.35, lw=0, zorder=0)
ax.grid(axis="y", visible=False); ax.grid(axis="x", visible=True); ax.set_xlabel("Months of cash, FY2024 (cash and savings ÷ monthly expenses); shaded 3-6 months")
style.finish(f, ax, "m3_04_months_of_cash",
             "Calvary's 5.2 months of cash in FY2024 was mid-pack; the government-anchored DV providers run on 1 month or less",
             "fact_org_financials (preferred rows): cash_savings_eoy and total_expenses, FY2024",
             note="FY2024 is the latest year with all 20 organizations. Calvary fell to 4.4 months in FY2025.")

# ------------------------------------------------------------------ m3_05 small multiples: gov share trajectories
tr = pf[pf.fiscal_year.between(2017, 2025)].pivot_table(index="fiscal_year", columns="ein", values="gov_share")
order = [CALVARY] + [e for e in bench.sort_values("gov_share_fy2022_24_mean", ascending=False).ein if e != CALVARY]
save_chart_data(tr.reset_index().melt(id_vars="fiscal_year", var_name="ein", value_name="gov_share").assign(org=lambda x: x.ein.map(short)).dropna(),
                "m3_05_gov_share_trajectories", "Government share of revenue FY2017-FY2025, 20 organizations", ["fact_org_financials"], src, S)
style.apply()
f, axes = plt.subplots(4, 5, figsize=(13, 9), sharex=True, sharey=True)
for ax, e in zip(axes.flat, order):
    s_ = tr[e].dropna()
    ax.plot(s_.index, s_.values, color=color_for(e) if e != CALVARY else style.CALVARY_COLOR, marker="o", ms=4, markeredgecolor="white", markeredgewidth=1, lw=2)
    ax.set_title(short[e], fontsize=9, loc="left", color=style.INK, fontweight="bold" if e == CALVARY else "normal")
    ax.set_ylim(0, 1.05); ax.set_xticks([2017, 2019, 2021, 2023, 2025]); ax.tick_params(labelsize=7.5)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    if len(s_):
        ax.text(s_.index[-1], s_.values[-1] + 0.06, f"{s_.values[-1]:.0%}", fontsize=7.5, ha="center", color=style.TEXT_2)
f.text(0.01, 0.985, "Government share has been stable for most peers since 2017; the movers are Samaritan Inns (down), DWC and House of Ruth MD (up)",
       fontsize=12.5, fontweight="bold", color=style.INK, va="top")
f.text(0.01, 0.005, "Source: fact_org_financials, 990 line 1e / total revenue (Calvary on the audit basis FY17-23). Data as of 2026-10-10. Chart m3_05_gov_share_trajectories. Core peers provisional; DWC and CBWC Institute are LA reference organizations.",
       fontsize=7.5, color=style.TEXT_MUTED)
style.polish(f, "m3_05_gov_share_trajectories"); f.tight_layout(rect=(0, 0.03, 1, 0.95)); f.savefig(style.CHARTS / "m3_05_gov_share_trajectories.png", dpi=200); plt.close(f)

# ------------------------------------------------------------------ m3_06 institutional funder base
d = bench.dropna(subset=["institutional_funders"]).sort_values("institutional_per_revenue_dollar")
cb_inst = float(bench.set_index("ein").loc[CALVARY, "institutional_per_revenue_dollar"])
f, ax = style.fig(10, 6.8)
bars = ax.barh(d.org, d.institutional_per_revenue_dollar, color=[color_for(e) for e in d.ein], height=0.62)
for b_, v, n in zip(bars, d.institutional_per_revenue_dollar, d.institutional_funders):
    ax.annotate(f"{v:.1%}   ({int(n)} institutional funders)", (v, b_.get_y() + b_.get_height() / 2), xytext=(4, 0), textcoords="offset points", va="center", fontsize=8.5, color=style.TEXT_2)
style.pct_axis(ax, "x"); ax.set_xlim(0, d.institutional_per_revenue_dollar.max() * 1.45); ax.grid(axis="y", visible=False); ax.grid(axis="x", visible=True)
ax.set_xlabel("Filed institutional grants TY2020-24 as a share of FY2020-24 revenue (DAF sponsors excluded)")
style.finish(f, ax, "m3_06_institutional_base",
             f"Calvary's institutional funders already cover {cb_inst:.0%} of revenue, more than all peers except Samaritan Inns (27%), so the gap is depth per funder, not effort",
             "fact_grants (990-PF and Schedule I rows naming each organization, TY2020-24, non-cumulative), dim_funder, fact_org_financials",
             note="DMV funders' filings only, so the LA comparators' local funders are not captured. TY2024 filings partial. Core peers provisional.")

# ------------------------------------------------------------------ m3_07 sector distributions
dist_rows = []
for u, fy, label in [("dc_sector", 2023, "DC sector, FY2023"), ("size_matched", 2022, "Size-matched national, FY2022"), ("national_women", 2022, "National women's/DV orgs, FY2022")]:
    e_ = set(universe(u))
    # Comparison set: organizations whose return reports a government line (review finding R07). Against all filers
    # in the universe, with no line counted as 0%, the percentile is much higher; both are kept.
    all_ = fin[fin.ein.isin(e_) & (fin.fiscal_year == fy) & (fin.total_revenue > 0)]
    s_ = all_[all_.gov_share_of_revenue.notna()]
    cal_v = float(pf[(pf.ein == CALVARY) & (pf.fiscal_year == fy)].gov_share.iloc[0])
    pct = float((s_.gov_share_of_revenue < cal_v).mean())
    pct_all = float((all_.gov_share_of_revenue.fillna(0) < cal_v).mean())
    dist_rows.append({"universe": u, "label": label, "fiscal_year": fy, "n": len(s_), "p10": s_.gov_share_of_revenue.quantile(.1), "p25": s_.gov_share_of_revenue.quantile(.25),
                      "median": s_.gov_share_of_revenue.median(), "p75": s_.gov_share_of_revenue.quantile(.75), "p90": s_.gov_share_of_revenue.quantile(.9),
                      "calvary_gov_share": cal_v, "calvary_percentile": pct, "n_all_filers": len(all_), "calvary_percentile_all_filers": pct_all,
                      "median_all_filers": all_.gov_share_of_revenue.fillna(0).median(), "median_revenue": s_.total_revenue.median()})
dist = pd.DataFrame(dist_rows)
save_chart_data(dist, "m3_07_sector_distributions", "Government share distributions in the comparison universes, with Calvary's percentile",
                ["fact_org_financials", "dim_universe_membership"], src, S, "990 line 1e basis; percentile among organizations that report a government line, and among all filers with no line counted as 0%; benchmark years chosen for coverage (TY2024+ returns incomplete)")
f, ax = style.fig(10, 4.6)
for i, r in dist.iterrows():
    ax.plot([r.p10, r.p90], [i, i], color=style.GRID, lw=6, solid_capstyle="round")
    ax.plot([r.p25, r.p75], [i, i], color=style.PEER_COLOR, lw=10, solid_capstyle="butt")
    ax.plot([r["median"]], [i], marker="|", ms=18, color=style.INK, mew=2)
    ax.plot([r.calvary_gov_share], [i], marker="o", ms=11, color=style.CALVARY_COLOR, markeredgecolor="white", mew=1.5, zorder=5)
    ax.text(r.calvary_gov_share, i + 0.3, f"Calvary {r.calvary_gov_share:.0%} ({r.calvary_percentile:.0%}ile)", ha="center", fontsize=8.5, color=style.INK)
    ax.text(1.01, i, f"n={r.n:,}", fontsize=8, color=style.TEXT_MUTED, va="center")
ax.set_yticks(range(len(dist)), dist.label); ax.invert_yaxis(); ax.set_ylim(len(dist) - 0.4, -0.7)
style.pct_axis(ax, "x"); ax.set_xlim(0, 1.08); ax.grid(axis="y", visible=False); ax.grid(axis="x", visible=True)
ax.text(0.005, -0.62, "bars: 10th-90th (light) and 25th-75th (dark) percentiles; tick = median", fontsize=8, color=style.TEXT_MUTED)
style.finish(f, ax, "m3_07_sector_distributions",
             "Among organizations that report government revenue Calvary's share is near the median; against all filers it is in the top quarter",
             "fact_org_financials (990 line 1e / revenue, preferred rows) by universe from dim_universe_membership",
             note="Distributions cover organizations whose return reports a government line (990 line 1e). Against all filers in each universe, counting no line as 0%, Calvary sits at the " + ", ".join(f"{r.calvary_percentile_all_filers:.0%}" for _, r in dist.iterrows()) + " percentile. Universe years chosen for filing coverage.")

# ------------------------------------------------------------------ m3_08 diversifier / model case studies (mix over time)
cases = {"521474935": "Samaritan Inns: government fell from 72% to 11% while revenue held", "521007373": "N Street Village: 40% government, grew on private money",
         "521331552": "Miriam's Kitchen: philanthropy-led, tripled revenue since FY18", "311597223": "DWC (LA): scaled 3x with government rising to 57%"}
cm = pf[pf.ein.isin(cases) & pf.fiscal_year.between(2018, 2025)].copy()
cm["government"] = cm.government_grants.fillna(0)
cm["private_contributions"] = (cm.contributions_total - cm.government_grants.fillna(0)).clip(lower=0)
cm["program_service"] = cm.program_service_revenue.fillna(0).clip(lower=0)
cm["other"] = (cm.total_revenue - cm.government - cm.private_contributions - cm.program_service).clip(lower=0)
cm["gov_share"] = cm.government / cm.total_revenue
save_chart_data(cm[["ein", "short", "fiscal_year", "total_revenue", "government", "private_contributions", "program_service", "other", "gov_share"]],
                "m3_08_case_studies_mix", "Revenue mix FY2018-FY2025 for four model organizations", ["fact_org_financials"], src, S)
style.apply()
f, axes = plt.subplots(2, 2, figsize=(12, 7.6))
for ax, (e, ttl) in zip(axes.flat, cases.items()):
    s_ = cm[cm.ein == e].sort_values("fiscal_year")
    bottom = np.zeros(len(s_))
    for col, role, lab in [("government", "government", "Government"), ("private_contributions", "institutional", "Private contributions"), ("program_service", "other", "Program service revenue"), ("other", "individuals", "Other")]:
        ax.bar(s_.fiscal_year.astype(int).astype(str).radd("FY").str.slice(0, 2) + s_.fiscal_year.astype(int).astype(str).str[2:], s_[col], bottom=bottom, color=style.SERIES[role], width=0.62, label=lab, edgecolor="white", linewidth=1)
        bottom += s_[col].values
    for i, (t, g) in enumerate(zip(s_.total_revenue, s_.gov_share)):
        ax.text(i, t * 1.02, f"{g:.0%}", ha="center", fontsize=7.5, color=style.TEXT_2)
    ax.set_title(ttl, fontsize=9.5, loc="left", color=style.INK); style.money_axis(ax); ax.tick_params(labelsize=8); ax.set_ylim(0, s_.total_revenue.max() * 1.15)
axes.flat[0].legend(loc="upper left", fontsize=8)
f.text(0.01, 0.985, "Three ways peers reduced exposure or grew through it: replace government with program and private revenue, grow private alongside, or scale with it",
       fontsize=12, fontweight="bold", color=style.INK, va="top")
f.text(0.01, 0.005, "Source: fact_org_financials (990 preferred rows; government = line 1e). Labels: government share. Data as of 2026-10-10. Chart m3_08_case_studies_mix. Core peers provisional; DWC is an LA reference.",
       fontsize=7.5, color=style.TEXT_MUTED)
style.polish(f, "m3_08_case_studies_mix"); f.tight_layout(rect=(0, 0.03, 1, 0.95)); f.savefig(style.CHARTS / "m3_08_case_studies_mix.png", dpi=200); plt.close(f)

# ------------------------------------------------------------------ m3_09 OVSJG and CoC among peers (government concentration in the same pools)
g = load("fact_gov_awards", usecols=["recipient_ein", "fiscal_year", "amount", "source_type", "program_name", "source_id"])
gp = g[g.recipient_ein.isin(eins)]
ov26 = gp[(gp.source_type == "dc_ovsjg") & (gp.fiscal_year == 2026)].groupby("recipient_ein").amount.sum()
coc25 = gp[(gp.source_type == "hud_coc") & (gp.fiscal_year == 2025)].groupby("recipient_ein").amount.sum()
pools = pd.DataFrame({"ein": eins}); pools["org"] = pools.ein.map(short)
pools["ovsjg_fy2026"] = pools.ein.map(ov26).fillna(0); pools["hud_coc_fy2025"] = pools.ein.map(coc25).fillna(0)
pools["revenue_fy2024"] = pools.ein.map(bench.set_index("ein").revenue_fy2024)
pools["ovsjg_share_of_revenue"] = pools.ovsjg_fy2026 / pools.revenue_fy2024; pools["coc_share_of_revenue"] = pools.hud_coc_fy2025 / pools.revenue_fy2024
pools = pools[pools.ein.isin([CALVARY]) | (pools.ovsjg_fy2026 + pools.hud_coc_fy2025 > 0)].sort_values("ovsjg_fy2026", ascending=True)
save_chart_data(pools, "m3_09_peer_pools", "OVSJG FY2026 and HUD CoC FY2025 awards to Calvary and core peers", ["fact_gov_awards", "fact_org_financials"], sorted(gp.source_id.unique()) + src, S,
                "DC pools only; LA comparators have no rows by construction")
f, ax = style.fig(10, 6.4)
y = np.arange(len(pools)); h = 0.38
ax.barh(y + h / 2, pools.ovsjg_fy2026, h, color=style.SERIES["government"], label="OVSJG awards, DC FY2026")
ax.barh(y - h / 2, pools.hud_coc_fy2025, h, color=style.SERIES["daf"], label="HUD CoC awards via TCP, FY2025")
for yi, (a, b_) in enumerate(zip(pools.ovsjg_fy2026, pools.hud_coc_fy2025)):
    if a: ax.annotate(f"${a/1e6:,.2f}M", (a, yi + h / 2), xytext=(3, 0), textcoords="offset points", va="center", fontsize=8, color=style.TEXT_2)
    if b_: ax.annotate(f"${b_/1e6:,.2f}M", (b_, yi - h / 2), xytext=(3, 0), textcoords="offset points", va="center", fontsize=8, color=style.TEXT_2)
ax.set_yticks(y, [f"{o}{' (subject)' if e == CALVARY else ''}" for o, e in zip(pools.org, pools.ein)])
style.money_axis(ax, "M", "x"); ax.grid(axis="y", visible=False); ax.grid(axis="x", visible=True); ax.legend(loc="lower right")
style.finish(f, ax, "m3_09_peer_pools",
             "The DV peers draw $3-5M a year each from OVSJG; Calvary's $1.05M makes it a mid-sized OVSJG grantee and one of the larger CoC sub-recipients",
             "fact_gov_awards: OVSJG FY2026 award list; HUD CoC FY2025 awards (TCP as applicant)",
             note="Core peers provisional. DHS/TCP contracts not shown (public for one year only).")

# ------------------------------------------------------------------ summary + insights
cb = bench.set_index("ein")
print(bench[["org", "group", "revenue_fy2024", "gov_share_fy2022_24_mean", "real_cagr_fy2019_24", "months_of_cash_fy2024", "institutional_funders", "institutional_per_revenue_dollar", "daf_share_of_filed", "resilience_type"]].round(3).to_string())
print(dist.round(3).to_string())
print(pools.round(3).to_string())
rank = bench[bench.group != "named_comparator"].sort_values("gov_share_fy2022_24_mean", ascending=False).reset_index(drop=True)
cal_rank = int(rank.index[rank.ein == CALVARY][0]) + 1
register_insight("M3-01", "M3", f"Calvary's government share ({cb.loc[CALVARY,'gov_share_fy2022_24_mean']:.0%}, FY2022-24 mean) ranks {cal_rank} of 19 DC-area organizations: below every DC DV provider (DASH 70%, My Sister's Place 83%, DC SAFE 89%) and above the philanthropy-led models (Christ House, Thrive DC, Miriam's Kitchen).",
                 "m3_00_benchmark_table: DC SAFE 89%, My Sister's Place 83%, Everyone Home DC 76%, N Street Village 42%, Samaritan Inns 44%, Miriam's Kitchen ~1%.", ["m3_01_gov_share_ranked", "m3_02_size_vs_gov_share"],
                 ["fact_org_financials"], "mid-pack, 53%", "high", "Calvary is 'mixed', not an outlier; the exposure problem is concentration in three streams plus a thin private base, not an unusual share.", "both")
register_insight("M3-02", "M3", "Among organizations that report government revenue, Calvary's government share is near the median in DC human services and among national women's/DV organizations; against all filers (no line counted as 0%) it is in the top quarter. The peer rank (M3-01) is the stronger evidence.",
                 "; ".join(f"{r.label}: median {r['median']:.0%}, Calvary {r.calvary_gov_share:.0%} at the {r.calvary_percentile:.0%} percentile of {r.n} reporting a government line, {r.calvary_percentile_all_filers:.0%} of all {r.n_all_filers} filers" for _, r in dist.iterrows()),
                 ["m3_07_sector_distributions"], ["fact_org_financials", "dim_universe_membership"], "near median", "high", "The board should not read the government share itself as a crisis; the fragility is in the streams and the cash.", "both")
register_insight("M3-03", "M3", f"Calvary's real revenue growth FY19-FY24 ({cb.loc[CALVARY,'real_cagr_fy2019_24']:+.1%}/yr) trails only My Sister's Place, DWC and DC SAFE; Miriam's Kitchen grew 12% a year with almost no government money.",
                 "m3_03_real_growth", ["m3_03_real_growth"], ["fact_org_financials", "dim_period"], f"{cb.loc[CALVARY,'real_cagr_fy2019_24']:+.1%}/yr real", "high", "Growth has been possible on both models; the choice is about durability and cash, not growth.", "both")
register_insight("M3-04", "M3", f"Calvary's liquidity (5.2 months FY2024, 4.4 in FY2025) is mid-pack; government-anchored DV providers run on about one month of cash or less, while Doorways, N Street Village and Everyone Home DC hold 8-12 months.",
                 "m3_04_months_of_cash", ["m3_04_months_of_cash"], ["fact_org_financials"], "5.2 months vs 0.5-12 range", "high", "Peers with Calvary's mix hold more cash; a 6-month reserve target is in line with the better-capitalized mixed peers.", "both")
register_insight("M3-05", "M3", f"Calvary already works institutional funders harder than most peers: {int(cb.loc[CALVARY,'institutional_funders'])} institutional funders TY2020-24 and filed institutional grants equal to {cb.loc[CALVARY,'institutional_per_revenue_dollar']:.0%} of revenue, versus 8% at House of Ruth DC, 6% at N Street Village and 11% at Miriam's Kitchen; only Samaritan Inns (27%) is far ahead.",
                 "m3_06_institutional_base", ["m3_06_institutional_base"], ["fact_grants", "dim_funder", "fact_org_financials"], "12% of revenue vs peer median ~6%", "medium", "More of the same (more foundation applications) has limited headroom; the upside is larger multi-year grants from the funders in the gap list (M5), DAF/individual giving where N Street Village and Miriam's Kitchen lead, and earned revenue as at Samaritan Inns.", "both")
register_insight("M3-06", "M3", "Three replicable paths among peers: Samaritan Inns replaced government (72% -> 11%) with program and private revenue while holding revenue; N Street Village grew on private money at a stable ~40% share; DWC and House of Ruth MD scaled with government rising above 55%.",
                 "m3_08_case_studies_mix; m3_05_gov_share_trajectories", ["m3_08_case_studies_mix", "m3_05_gov_share_trajectories"], ["fact_org_financials"], "three models", "medium",
                 "Calvary's realistic path is N Street Village's (grow private alongside government) with elements of Samaritan Inns' earned revenue; DWC shows that scaling with government needs a much larger balance sheet.", "both")
log(S, [f"benchmark table {len(bench)} orgs; Calvary gov share FY22-24 mean {cb.loc[CALVARY,'gov_share_fy2022_24_mean']:.3f}; rank {cal_rank}/19",
        "charts m3_01..m3_09 written"])
