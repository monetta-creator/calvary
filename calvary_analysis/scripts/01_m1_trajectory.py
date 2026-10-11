"""M1: Calvary financial trajectory FY2011-FY2025.

Revenue (nominal and 2024$), revenue mix on the audit basis for government, surplus/deficit,
net assets and liquidity, event income, and concentration of institutional funders.
Reads: fact_org_financials, fact_grants, dim_funder, dim_period. Writes chart_data/m1_*.csv, charts/m1_*.png.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import style  # noqa: E402
from lib.common import CALVARY, deflators, load, log, register_insight, save_chart_data, money  # noqa: E402

S = "01_m1_trajectory"
FIN_COLS = ["ein", "tax_year", "fiscal_year", "return_type", "source_id", "preferred", "total_revenue",
            "contributions_total", "fundraising_event_contributions", "government_grants", "other_contributions",
            "program_service_revenue", "investment_income", "special_events_net", "other_revenue", "total_expenses",
            "fundraising_expenses", "program_expenses", "management_expenses", "total_assets_eoy",
            "total_liabilities_eoy", "net_assets_eoy", "cash_savings_eoy", "months_of_cash"]
fin = load("fact_org_financials", usecols=FIN_COLS)
cal = fin[fin.ein == CALVARY].copy()
pref = cal[cal.preferred == 1].set_index("fiscal_year").sort_index()
audit = cal[cal.return_type == "audit"].set_index("fiscal_year").sort_index()
defl = deflators()
src_fin = sorted(cal.source_id.unique())

# ------------------------------------------------------------------ m1_01 revenue & expenses, nominal and real
d1 = pd.DataFrame({
    "fiscal_year": pref.index,
    "total_revenue": pref.total_revenue.values,
    "total_expenses": pref.total_expenses.values,
    "surplus_deficit": (pref.total_revenue - pref.total_expenses).values,
    "deflator_to_2024": pref.index.map(defl).values,
})
d1["total_revenue_real_2024"] = d1.total_revenue * d1.deflator_to_2024
d1["total_expenses_real_2024"] = d1.total_expenses * d1.deflator_to_2024
d1["revenue_ex_fy22_spike"] = d1.total_revenue
d1["fy_label"] = "FY" + d1.fiscal_year.astype(int).astype(str).str[2:]
save_chart_data(d1, "m1_01_revenue_expenses", "Calvary revenue and expenses FY11-FY25, nominal and 2024 dollars",
                ["fact_org_financials", "dim_period"], src_fin + ["api_bls_cpi"], S,
                "preferred 990 rows; FY22 includes the one-time $3.68M SLFRF building award")

f, ax = style.fig()
ax.plot(d1.fy_label, d1.total_revenue_real_2024, color=style.SERIES["government"], marker="o", ms=5,
        markeredgecolor="white", markeredgewidth=1.5, label="Revenue (2024 $)")
ax.plot(d1.fy_label, d1.total_revenue, color=style.PEER_COLOR, marker="o", ms=4, markeredgecolor="white",
        markeredgewidth=1.5, label="Revenue (nominal)")
ax.plot(d1.fy_label, d1.total_expenses_real_2024, color=style.SERIES["individuals"], linestyle="--", lw=1.6,
        label="Expenses (2024 $)")
style.money_axis(ax)
ax.set_ylim(0, None)
ax.legend(loc="upper left")
ax.annotate("FY22: $3.68M one-time SLFRF\naward for the New Foundations building", xy=(11, d1.total_revenue_real_2024.iloc[11]),
            xytext=(5.2, 8.6e6), fontsize=8.5, color=style.TEXT_2,
            arrowprops=dict(arrowstyle="-", color=style.TEXT_MUTED, lw=0.8))
style.finish(f, ax, "m1_01_revenue_expenses",
             "Calvary's revenue grew 59% in real terms from FY19 to FY25, but FY25 expenses outran revenue",
             "fact_org_financials (preferred 990 rows), dim_period CPI-U")

# ------------------------------------------------------------------ m1_02 revenue mix (audit basis for government)
# government: audit government revenue where an audit exists (FY13-FY23), else 990 line 1e (FY24-FY25)
gov = audit.government_grants.reindex(pref.index)
gov_basis = pd.Series(np.where(gov.notna(), "audit", "990_line_1e"), index=pref.index)
gov = gov.fillna(pref.government_grants)
events = pref.fundraising_event_contributions.fillna(0)
contrib = pref.contributions_total
other_private = contrib - gov - events            # individuals + foundations + corporate + DAF (990 doesn't split these)
other_rev = pref.total_revenue - contrib          # program service (0), investment, special events net, other
mix = pd.DataFrame({"fiscal_year": pref.index, "government": gov.values, "government_basis": gov_basis.values,
                    "private_contributions_ex_events": other_private.values, "event_contributions": events.values,
                    "other_revenue": other_rev.values, "total_revenue": pref.total_revenue.values})
mix["denominator_revenue"] = np.where(mix.government_basis == "audit", audit.total_revenue.reindex(pref.index).values, pref.total_revenue.values)
mix = mix[mix.fiscal_year >= 2015]
mix["gov_share"] = mix.government / mix.denominator_revenue   # audit gov ÷ audit revenue where an audit exists
mix["fy_label"] = "FY" + mix.fiscal_year.astype(int).astype(str).str[2:]
save_chart_data(mix, "m1_02_revenue_mix", "Calvary revenue mix FY15-FY25 (government on the audit basis to FY23)",
                ["fact_org_financials"], src_fin, S,
                "private_contributions_ex_events = contributions_total - government - line 1c events; 990 does not split foundations from individuals")

f, ax = style.fig()
bottom = np.zeros(len(mix))
for col, role, lab in [("government", "government", "Government (audit basis; 990 line 1e for FY24-25)"),
                       ("private_contributions_ex_events", "institutional", "Private contributions (foundations, corporate, individuals)"),
                       ("event_contributions", "individuals", "Event contributions"),
                       ("other_revenue", "other", "Other revenue")]:
    vals = mix[col].clip(lower=0).values
    ax.bar(mix.fy_label, vals, bottom=bottom, color=style.SERIES[role], width=0.62, label=lab,
           edgecolor="white", linewidth=1.5)
    bottom += vals
for i, (x, g, t) in enumerate(zip(mix.fy_label, mix.gov_share, mix.total_revenue)):
    ax.text(i, t + 1.2e5, f"{g:.0%}", ha="center", fontsize=8.5, color=style.TEXT_2)
style.money_axis(ax)
ax.set_ylim(0, mix.total_revenue.max() * 1.12)
ax.legend(loc="upper left", ncol=1)
ax.text(0.99, 0.97, "Labels: government share of revenue", transform=ax.transAxes, ha="right", fontsize=8.5, color=style.TEXT_2)
style.finish(f, ax, "m1_02_revenue_mix",
             f"Government has supplied {mix.gov_share.min():.0%}-{mix.gov_share.max():.0%} of Calvary's revenue every year since FY15 and most of the growth",
             "fact_org_financials: Calvary audits FY15-FY23 (government revenue), 990 preferred rows",
             note="FY24 and FY25 government figures are 990 line 1e, which understated government revenue in FY21 (see M2 reconstruction).")

# ------------------------------------------------------------------ m1_03 government share: audit vs line 1e
gs = pd.DataFrame({"fiscal_year": pref.index,
                   "gov_share_audit": (audit.government_grants / audit.total_revenue).reindex(pref.index).values,
                   "gov_share_line_1e": (pref.government_grants / pref.total_revenue).values,
                   "gov_audit": audit.government_grants.reindex(pref.index).values,
                   "gov_line_1e": pref.government_grants.values,
                   "audit_total_revenue": audit.total_revenue.reindex(pref.index).values,
                   "total_revenue_990": pref.total_revenue.values})
gs = gs[gs.fiscal_year >= 2013]
gs["fy_label"] = "FY" + gs.fiscal_year.astype(int).astype(str).str[2:]
save_chart_data(gs, "m1_03_gov_share_two_measures", "Government share of revenue: audit basis vs 990 line 1e",
                ["fact_org_financials"], src_fin, S, "audit share uses audit total revenue; line 1e share uses 990 total revenue")
f, ax = style.fig()
ax.plot(gs.fy_label, gs.gov_share_audit, color=style.SERIES["government"], marker="o", ms=6, markeredgecolor="white",
        markeredgewidth=1.5, label="Audit basis (government contracts and grants)")
ax.plot(gs.fy_label, gs.gov_share_line_1e, color=style.PEER_COLOR, marker="o", ms=5, markeredgecolor="white",
        markeredgewidth=1.5, label="990 line 1e (government grants)")
style.pct_axis(ax)
ax.set_ylim(0, 0.75)
ax.legend(loc="upper left")
ax.annotate("FY21: contracts booked\noutside line 1e", xy=(8, gs.gov_share_line_1e.iloc[8]), xytext=(5.5, 0.1),
            fontsize=8.5, color=style.TEXT_2, arrowprops=dict(arrowstyle="-", color=style.TEXT_MUTED, lw=0.8))
style.finish(f, ax, "m1_03_gov_share_two_measures",
             "On the audit basis, government rose from 37% of revenue in FY14 to about half since FY19",
             "fact_org_financials: Calvary audits FY13-FY23 and 990 returns FY15-FY25")

# ------------------------------------------------------------------ m1_04 surplus / deficit and net assets
d4 = pd.DataFrame({"fiscal_year": pref.index, "surplus_deficit": (pref.total_revenue - pref.total_expenses).values,
                   "net_assets_eoy": pref.net_assets_eoy.values, "total_assets_eoy": pref.total_assets_eoy.values,
                   "cash_savings_eoy": pref.cash_savings_eoy.values, "months_of_cash": pref.months_of_cash.values,
                   "total_expenses": pref.total_expenses.values})
d4["fy_label"] = "FY" + d4.fiscal_year.astype(int).astype(str).str[2:]
save_chart_data(d4, "m1_04_surplus_deficit", "Calvary surplus/deficit, net assets, cash and months of cash FY11-FY25",
                ["fact_org_financials"], src_fin, S, "months_of_cash = cash_savings_eoy / (total_expenses/12), from the clean table")
save_chart_data(d4[["fiscal_year", "fy_label", "cash_savings_eoy", "total_expenses", "months_of_cash"]], "m1_05_months_of_cash",
                "Calvary months of cash FY11-FY25", ["fact_org_financials"], src_fin, S, "same rows as m1_04")
f, ax = style.fig()
cols = [style.POSITIVE if v >= 0 else style.NEGATIVE for v in d4.surplus_deficit]
bars = ax.bar(d4.fy_label, d4.surplus_deficit, color=cols, width=0.62)
for b, v in zip(bars, d4.surplus_deficit):
    ax.annotate(f"{'+' if v>=0 else '−'}${abs(v)/1e6:,.1f}M", (b.get_x() + b.get_width() / 2, v),
                xytext=(0, 3 if v >= 0 else -11), textcoords="offset points", ha="center", fontsize=8, color=style.TEXT_2)
ax.axhline(0, color=style.TEXT_2, lw=0.8)
style.money_axis(ax)
style.finish(f, ax, "m1_04_surplus_deficit",
             "Calvary ran operating deficits in two of the last three years (FY23 −$674K, FY25 −$607K) after the FY22 capital windfall",
             "fact_org_financials: Calvary 990 preferred rows (revenue minus expenses)",
             note="FY22 surplus reflects the $3.68M SLFRF award used to buy the New Foundations building, not operating margin.")

f, ax = style.fig(10, 5)
ax.bar(d4.fy_label, d4.months_of_cash, color=style.SERIES["government"], width=0.62)
for i, v in enumerate(d4.months_of_cash):
    if pd.notna(v):
        ax.text(i, v + 0.12, f"{v:.1f}", ha="center", fontsize=8.5, color=style.TEXT_2)
ax.axhspan(3, 6, color=style.GOLD_LIGHT, alpha=0.35, lw=0)
ax.text(0.01, 0.95, "Shaded: 3-6 months, a common reserve target band", transform=ax.transAxes, fontsize=8.5, color=style.TEXT_2)
ax.set_ylabel("Months of cash (cash ÷ monthly expenses)")
style.finish(f, ax, "m1_05_months_of_cash",
             "Calvary's cash cushion fell from 7.5 months in FY21 to 4.4 months in FY25",
             "fact_org_financials: cash_savings_eoy and total_expenses, Calvary 990 preferred rows")

# ------------------------------------------------------------------ m1_06 event income
ev = pd.DataFrame({"fiscal_year": pref.index, "event_contributions_line_1c": pref.fundraising_event_contributions.values,
                   "special_events_net": pref.special_events_net.values})
ev = ev[ev.fiscal_year >= 2015]
ev["fy_label"] = "FY" + ev.fiscal_year.astype(int).astype(str).str[2:]
save_chart_data(ev, "m1_06_events", "Calvary event contributions (line 1c) and net special-event income FY15-FY25",
                ["fact_org_financials"], src_fin, S)
f, ax = style.fig(10, 5)
ax.bar(ev.fy_label, ev.event_contributions_line_1c, color=style.SERIES["individuals"], width=0.62, label="Event contributions (line 1c)")
ax.plot(ev.fy_label, ev.special_events_net, color=style.TEXT_2, marker="o", ms=5, markeredgecolor="white",
        markeredgewidth=1.5, label="Net special-event income (line 8c)")
ax.axhline(0, color=style.TEXT_2, lw=0.8)
style.money_axis(ax, "K")
ax.legend(loc="upper left")
style.finish(f, ax, "m1_06_event_income",
             "Event contributions collapsed from $538K in FY24 to $55K in FY25, the single largest private-revenue swing",
             "fact_org_financials: Calvary 990 preferred rows, Part VIII lines 1c and 8c")

# ------------------------------------------------------------------ m1_07 institutional funder concentration (filed grants TY2020-24)
GR_COLS = ["funder_id", "funder_ein", "funder_name_raw", "recipient_ein", "tax_year", "amount", "cumulative_flag",
           "source_type", "source_id"]
gr = load("fact_grants", usecols=GR_COLS)
cg = gr[(gr.recipient_ein == CALVARY) & (gr.cumulative_flag != 1) & gr.source_type.isin(["pf_grants_paid", "schedule_i"])
        & gr.tax_year.between(2020, 2024)].copy()
df = load("dim_funder", usecols=["funder_id", "funder_name", "funder_type"]).set_index("funder_id")
cg["funder_name"] = cg.funder_id.map(df.funder_name).fillna(cg.funder_name_raw)
cg["funder_type"] = cg.funder_id.map(df.funder_type).fillna("other")
by_funder = (cg.groupby(["funder_id", "funder_name", "funder_type"]).agg(amount=("amount", "sum"), years=("tax_year", "nunique"),
                                                                        n_grants=("amount", "size")).reset_index()
             .sort_values("amount", ascending=False))
total = by_funder.amount.sum()
by_funder["share"] = by_funder.amount / total
by_funder["cum_share"] = by_funder.share.cumsum()
by_funder["rank"] = range(1, len(by_funder) + 1)
inst = by_funder[by_funder.funder_type != "daf_sponsor"]
inst_total = inst.amount.sum()
hhi_all = float((by_funder.share ** 2).sum() * 10000)
save_chart_data(by_funder, "m1_07_calvary_funder_concentration",
                "Grants to Calvary in funders' own filings TY2020-24, by funder, with cumulative share",
                ["fact_grants", "dim_funder"], sorted(cg.source_id.unique()), S,
                f"total ${total:,.0f}; institutional (ex-DAF) ${inst_total:,.0f}; HHI across funders {hhi_all:.0f}")
top = by_funder.head(12).iloc[::-1]
f, ax = style.fig(10, 6)
colors = [style.SERIES["daf"] if t == "daf_sponsor" else style.SERIES["institutional"] for t in top.funder_type]
names = [n.title().replace("'S", "'s").replace(" Inc", "")[:46] for n in top.funder_name]
bars = ax.barh(names, top.amount, color=colors, height=0.62)
for b, v, s in zip(bars, top.amount, top.share):
    ax.annotate(f"${v/1e3:,.0f}K  ({s:.0%})", (v, b.get_y() + b.get_height() / 2), xytext=(4, 0),
                textcoords="offset points", va="center", fontsize=8.5, color=style.TEXT_2)
ax.grid(axis="y", visible=False); ax.grid(axis="x", visible=True)
style.money_axis(ax, "K", axis="x")
ax.set_xlim(0, top.amount.max() * 1.25)
from matplotlib.patches import Patch  # noqa: E402
ax.legend(handles=[Patch(color=style.SERIES["institutional"], label="Institutional funder"),
                   Patch(color=style.SERIES["daf"], label="DAF sponsor (donor intermediary)")], loc="lower right")
style.finish(f, ax, "m1_07_funder_concentration",
             "One funder, the Greater Washington Community Foundation, supplied 27% of Calvary's filed grants over five years",
             "fact_grants (990-PF and Schedule I rows naming Calvary, TY2020-24, excluding cumulative rows), dim_funder",
             note="Share = share of all $4.43M in filed grants to Calvary TY2020-24; TY2024 filings are still arriving.")

# yearly filed grants: institutional vs DAF
yr = cg.assign(kind=np.where(cg.funder_type == "daf_sponsor", "daf", "institutional")).groupby(["tax_year", "kind"]).amount.sum().unstack(fill_value=0).reset_index()
yr["funders"] = cg.groupby("tax_year").funder_id.nunique().values
save_chart_data(yr, "m1_08_filed_grants_by_year", "Filed grants to Calvary by funder tax year: institutional vs DAF",
                ["fact_grants", "dim_funder"], sorted(cg.source_id.unique()), S, "funder tax year, not Calvary fiscal year; TY2024 partial")
f, ax = style.fig(10, 5)
ax.bar(yr.tax_year.astype(int).astype(str).radd("TY"), yr.institutional, color=style.SERIES["institutional"], width=0.62, label="Institutional funders")
ax.bar(yr.tax_year.astype(int).astype(str).radd("TY"), yr.daf, bottom=yr.institutional, color=style.SERIES["daf"], width=0.62, label="DAF sponsors",
       edgecolor="white", linewidth=1.5)
for i, (a, b, n) in enumerate(zip(yr.institutional, yr.daf, yr.funders)):
    ax.text(i, a + b + 2e4, f"${(a+b)/1e3:,.0f}K · {n} funders", ha="center", fontsize=8.5, color=style.TEXT_2)
style.money_axis(ax, "K")
ax.set_ylim(0, (yr.institutional + yr.daf).max() * 1.18)
ax.legend(loc="upper left")
style.finish(f, ax, "m1_08_filed_grants_by_year",
             "Filed grants to Calvary have stayed near $1M a year from the same 26-29 funders, with no growth trend",
             "fact_grants: 990-PF and Schedule I rows naming Calvary, by funder tax year; dim_funder",
             note="Funder tax years do not align with Calvary's fiscal year; TY2024 returns are partly filed, TY2025 mostly unfiled.")

# ------------------------------------------------------------------ summary numbers for the readout
fy25 = pref.loc[2025]; fy24 = pref.loc[2024]; fy21 = pref.loc[2021]; fy19 = pref.loc[2019]
real19 = d1.set_index("fiscal_year").total_revenue_real_2024
summary = {
    "rev_fy25": fy25.total_revenue, "rev_fy19": fy19.total_revenue, "real_growth_fy19_25": real19[2025] / real19[2019] - 1,
    "deficit_fy25": fy25.total_revenue - fy25.total_expenses, "contrib_fy24": fy24.contributions_total, "contrib_fy25": fy25.contributions_total,
    "months_cash_fy21": fy21.months_of_cash, "months_cash_fy25": fy25.months_of_cash, "net_assets_fy25": fy25.net_assets_eoy,
    "gov_share_audit_fy14": gs.set_index("fiscal_year").gov_share_audit[2014], "gov_share_audit_fy23": gs.set_index("fiscal_year").gov_share_audit[2023],
    "gov_share_1e_fy25": gs.set_index("fiscal_year").gov_share_line_1e[2025],
    "events_fy24": ev.set_index("fiscal_year").event_contributions_line_1c[2024], "events_fy25": ev.set_index("fiscal_year").event_contributions_line_1c[2025],
    "filed_total_ty20_24": total, "gwcf_share": float(by_funder.iloc[0].share), "top5_share": float(by_funder.head(5).share.sum()),
    "n_funders": len(by_funder), "hhi": hhi_all, "inst_total": inst_total, "daf_total": total - inst_total,
}
save_chart_data(pd.Series(summary, name="value").rename_axis("metric").reset_index(), "m1_summary_numbers", "M1 headline numbers used in readouts and decks",
                ["fact_org_financials", "fact_grants", "dim_funder", "dim_period"], src_fin + sorted(cg.source_id.unique()), S)
for k, v in summary.items():
    print(f"{k}: {v:,.3f}" if isinstance(v, float) else f"{k}: {v}")
print(mix[["fy_label", "government", "government_basis", "private_contributions_ex_events", "event_contributions", "other_revenue", "gov_share"]].to_string())
print(by_funder.head(12)[["funder_name", "funder_type", "amount", "years", "share"]].to_string())

register_insight("M1-01", "M1", f"Government supplied {mix.gov_share.min():.0%}-{mix.gov_share.max():.0%} of Calvary's revenue in every year FY15-FY25 on the audit basis (line 1e for FY24-25), and most of the growth since FY19.",
                 f"Audit-basis share 37% FY14 -> 50% FY21 -> 61% FY22 -> 51% FY23; line 1e 45% FY24, 58% FY25. Revenue {money(summary['rev_fy19'])} FY19 -> {money(summary['rev_fy25'])} FY25.",
                 ["m1_02_revenue_mix", "m1_03_gov_share_two_measures"], ["fact_org_financials"], "about half of revenue", "high",
                 "Calvary is a government-anchored organization; private growth has not kept pace.", "both")
register_insight("M1-02", "M1", "FY25 ran a $607K deficit with contributions down $0.8M and the cash cushion at 4.4 months, versus 7.5 months in FY21.",
                 f"Revenue {money(summary['rev_fy25'])} vs expenses {money(fy25.total_expenses)}; contributions {money(summary['contrib_fy24'])} -> {money(summary['contrib_fy25'])}; months of cash {summary['months_cash_fy21']:.1f} -> {summary['months_cash_fy25']:.1f}.",
                 ["m1_04_surplus_deficit", "m1_05_months_of_cash"], ["fact_org_financials"], "$607K deficit; 4.4 months of cash", "high",
                 "Little room to absorb a government cut; a reserve floor and a private-revenue recovery plan are both needed.", "both")
register_insight("M1-03", "M1", "Event contributions fell from $538K (FY24) to $55K (FY25), the largest single private-revenue swing.",
                 "990 Part VIII line 1c: $457,758 FY23, $538,070 FY24, $54,730 FY25; net special-event income negative every year through FY24.",
                 ["m1_06_event_income"], ["fact_org_financials"], "$483K drop", "high",
                 "Either the gala was cancelled/moved or re-booked; confirm with Calvary. It explains most of the FY25 contribution drop.", "both")
register_insight("M1-04", "M1", f"Filed institutional grants to Calvary have stayed near $1M a year from 26-29 funders, and one funder (GWCF incl. the Health Equity Fund) is {summary['gwcf_share']:.0%} of five-year filed grants; the top five are {summary['top5_share']:.0%}.",
                 f"TY2020-24 filed grants {money(total)} from {len(by_funder)} funders; institutional {money(inst_total)}, DAF {money(total-inst_total)}; HHI {hhi_all:.0f}.",
                 ["m1_07_funder_concentration", "m1_08_filed_grants_by_year"], ["fact_grants", "dim_funder"], "27% from one funder", "high",
                 "Private revenue is both flat and concentrated: broadening the institutional base is as important as growing it.", "both")
register_insight("M1-05", "M1", "The FY22 revenue spike ($8.87M) was a one-time $3.68M SLFRF award for the New Foundations building, not operating growth.",
                 "FY22 audit government revenue $5.69M; Treasury SLFRF subaward $3,680,675 (2022-03-08); property and equipment $2.74M -> $6.33M; net assets +$4.32M.",
                 ["m1_01_revenue_expenses", "m1_04_surplus_deficit"], ["fact_org_financials", "fact_gov_awards"], "$3.68M one-time", "high",
                 "Exclude FY22 from growth baselines; the building is an asset, not recurring revenue.", "both")
log(S, [f"charts m1_01..m1_08 written; filed grants TY2020-24 {total:,.0f} from {len(by_funder)} funders; HHI {hhi_all:.0f}",
        f"gov share audit FY14 {summary['gov_share_audit_fy14']:.3f}, FY23 {summary['gov_share_audit_fy23']:.3f}; line 1e FY25 {summary['gov_share_1e_fy25']:.3f}",
        f"FY25 deficit {summary['deficit_fy25']:,.0f}; months of cash FY25 {summary['months_cash_fy25']:.2f}"])
