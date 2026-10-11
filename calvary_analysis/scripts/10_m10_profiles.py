"""M10: Named-comparator profiles (Calvary CEO request): Downtown Women's Center (Los Angeles) and the
California Black Women's Collective Empowerment Institute (runs SheWorks). Trajectory, mix, federal programs,
funder lists, and what transfers to Calvary."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import style  # noqa: E402
from lib.common import CALVARY, DWC, SHEWORKS, CLEAN, load, log, money, register_insight, save_chart_data  # noqa: E402

S = "10_m10_profiles"
FIN = ["ein", "fiscal_year", "fye_month", "preferred", "total_revenue", "contributions_total", "government_grants", "program_service_revenue", "investment_income", "other_revenue",
       "total_expenses", "net_assets_eoy", "total_assets_eoy", "cash_savings_eoy", "months_of_cash", "gov_share_of_revenue", "source_id"]
fin = load("fact_org_financials", usecols=FIN)
fin = fin[(fin.preferred == 1) & fin.ein.isin([CALVARY, DWC, SHEWORKS])].copy()
fin["government"] = fin.government_grants.fillna(0); fin["private_contributions"] = (fin.contributions_total - fin.government).clip(lower=0)
fin["program_service"] = fin.program_service_revenue.fillna(0).clip(lower=0); fin["other"] = (fin.total_revenue - fin.government - fin.private_contributions - fin.program_service).clip(lower=0)
fin["gov_share"] = fin.government / fin.total_revenue
src = sorted(fin.source_id.unique())
prof = fin[fin.ein.isin([DWC, SHEWORKS]) & (fin.fiscal_year >= 2014)].sort_values(["ein", "fiscal_year"])
save_chart_data(prof[["ein", "fiscal_year", "fye_month", "total_revenue", "government", "private_contributions", "program_service", "other", "gov_share", "total_expenses", "net_assets_eoy", "months_of_cash"]],
                "m10_01_comparator_trajectories", "DWC and CBWC Institute revenue mix and government share by fiscal year", ["fact_org_financials"], src, S)

style.apply()
f, axes = plt.subplots(1, 2, figsize=(13, 5.6), gridspec_kw={"width_ratios": [2.2, 1]})
for ax, (e, ttl) in zip(axes, [(DWC, "Downtown Women's Center, Los Angeles (FY = calendar year)"), (SHEWORKS, "CBWC Empowerment Institute / SheWorks (FYE June)")]):
    s_ = prof[prof.ein == e]
    labels = s_.fiscal_year.astype(int).astype(str)
    bottom = np.zeros(len(s_))
    for col, role, lab in [("government", "government", "Government"), ("private_contributions", "institutional", "Private contributions"), ("program_service", "other", "Program service"), ("other", "individuals", "Other")]:
        ax.bar(labels, s_[col], bottom=bottom, color=style.SERIES[role], width=0.62, label=lab, edgecolor="white", linewidth=1); bottom += s_[col].values
    for i, (t, g) in enumerate(zip(s_.total_revenue, s_.gov_share)):
        ax.text(i, t * 1.02, f"{g:.0%}", ha="center", fontsize=8, color=style.TEXT_2)
    ax.set_title(ttl, fontsize=10, loc="left", color=style.INK); style.money_axis(ax); ax.set_ylim(0, s_.total_revenue.max() * 1.15); ax.tick_params(labelsize=8.5)
axes[0].legend(loc="upper left", fontsize=8.5)
f.text(0.01, 0.985, "DWC grew from $6M to $34M in a decade with government rising to 57% of revenue, while the SheWorks parent\nstarted at 88% government and is diversifying fast",
       fontsize=12.5, fontweight="bold", color=style.INK, va="top")
f.text(0.01, 0.005, "Source: fact_org_financials (IRS 990 e-file returns via GivingTuesday / ProPublica / IRS SOI; government = Part VIII line 1e). Labels: government share. Data as of 2026-10-10. Chart m10_01_comparator_trajectories.",
       fontsize=7.5, color=style.TEXT_MUTED)
style.polish(f, "m10_01_comparator_trajectories"); f.tight_layout(rect=(0, 0.03, 1, 0.90)); f.savefig(style.CHARTS / "m10_01_comparator_trajectories.png", dpi=200); plt.close(f)

# federal programs (FAC) for DWC
g = load("fact_gov_awards", usecols=["recipient_ein", "source_type", "fiscal_year", "assistance_listing", "program_name", "awarding_agency", "pass_through_entity", "flow_type", "amount", "source_id"])
gd = g[(g.recipient_ein == DWC) & (g.source_type == "fac_sefa")]
fed = gd.groupby(["assistance_listing", "program_name"]).agg(amount=("amount", "sum"), years=("fiscal_year", "nunique"), pass_through=("flow_type", lambda s: (s == "pass_through_expenditure").mean())).reset_index().sort_values("amount", ascending=False)
save_chart_data(fed, "m10_02_dwc_federal_programs", "DWC federal expenditures by program (FAC single-audit SEFA, FY2020-25)", ["fact_gov_awards"], sorted(gd.source_id.unique()), S)
top = fed.head(8).iloc[::-1]
f, ax = style.fig(10, 4.8)
bars = ax.barh([f"{a} {n.title()[:48]}" for a, n in zip(top.assistance_listing, top.program_name)], top.amount, color=style.SERIES["daf"], height=0.62)
for b_, v, y_ in zip(bars, top.amount, top.years):
    ax.annotate(f"{money(v)} over {int(y_)} yrs", (v, b_.get_y() + b_.get_height() / 2), xytext=(4, 0), textcoords="offset points", va="center", fontsize=8.5, color=style.TEXT_2)
style.money_axis(ax, "M", "x"); ax.set_xlim(0, top.amount.max() * 1.3); ax.grid(axis="y", visible=False); ax.grid(axis="x", visible=True); ax.tick_params(axis="y", labelsize=8)
style.finish(f, ax, "m10_02_dwc_federal_programs",
             f"DWC's federal money ({money(gd.amount.sum())} FY2020-25) is {gd[gd.flow_type=='pass_through_expenditure'].amount.sum()/gd.amount.sum():.0%} pass-through, led by HUD CoC, ESG and VOCA: the same channels Calvary uses, at five times the scale",
             "fact_gov_awards: Federal Audit Clearinghouse single-audit SEFA rows for DWC (EIN 31-1597223)")

# funder lists for the comparators (web + filings)
gr = load("fact_grants", usecols=["funder_id", "funder_name_raw", "recipient_ein", "tax_year", "fiscal_year", "amount", "amount_band_min", "cumulative_flag", "source_type", "source_id"])
gc = gr[gr.recipient_ein.isin([DWC, SHEWORKS])]
summ = gc.groupby(["recipient_ein", "source_type"]).agg(rows=("funder_id", "size"), funders=("funder_id", "nunique"), amount_known=("amount", "sum")).reset_index()
save_chart_data(summ, "m10_03_comparator_funder_sources", "Funder evidence for DWC and CBWC Institute by source type", ["fact_grants"], sorted(gc.source_id.unique()), S, "annual-report and gala lists carry bands, not amounts; DMV funders' filings only")
dwc_filed = gc[(gc.recipient_ein == DWC) & gc.source_type.isin(["pf_grants_paid", "schedule_i"]) & (gc.cumulative_flag != 1)].groupby("funder_name_raw").agg(amount=("amount", "sum"), years=("tax_year", "nunique")).sort_values("amount", ascending=False)
dwc_named = gc[(gc.recipient_ein == DWC) & gc.source_type.isin(["web", "annual_report"]) & gc.amount.notna()].sort_values("amount", ascending=False)[["funder_name_raw", "fiscal_year", "amount", "source_type"]]
save_chart_data(dwc_filed.reset_index(), "m10_04_dwc_dmv_funders", "DMV funders' filed grants to DWC TY2020-25", ["fact_grants"], sorted(gc.source_id.unique()), S)
save_chart_data(dwc_named, "m10_05_dwc_named_grants", "DWC grants named with amounts in web sources (funder announcements, annual reports)", ["fact_grants"], sorted(gc.source_id.unique()), S)

print(prof[["ein", "fiscal_year", "total_revenue", "gov_share", "private_contributions", "program_service", "months_of_cash"]].round(2).to_string())
print(fed.head(10).to_string()); print(summ.to_string()); print(dwc_filed.head(10).to_string()); print(dwc_named.head(12).to_string())
d24 = prof[(prof.ein == DWC) & (prof.fiscal_year == 2024)].iloc[0]; d14 = prof[(prof.ein == DWC) & (prof.fiscal_year == prof[prof.ein == DWC].fiscal_year.min())].iloc[0]
s24 = prof[(prof.ein == SHEWORKS)].sort_values("fiscal_year").iloc[-1]
register_insight("M10-01", "M10", f"DWC grew from {money(d14.total_revenue)} (FY{int(d14.fiscal_year)}) to {money(d24.total_revenue)} (FY2024) while its government share rose from {d14.gov_share:.0%} to {d24.gov_share:.0%}; its federal money is {gd[gd.flow_type=='pass_through_expenditure'].amount.sum()/gd.amount.sum():.0%} pass-through (HUD CoC, ESG, VOCA), the same channels Calvary uses.",
                 "m10_01, m10_02", ["m10_01_comparator_trajectories", "m10_02_dwc_federal_programs"], ["fact_org_financials", "fact_gov_awards"], "6x scale, 57% government", "high",
                 "The CEO's model comparator scaled with government rather than away from it, carrying 2-3 months of cash; the transferable parts are the housing pipeline (PSH development), the women's health clinic partnership and the MADE social enterprise, not the mix.", "both")
register_insight("M10-02", "M10", f"The SheWorks parent (CBWC Empowerment Institute, founded 2022) is {s24.gov_share:.0%} government at {money(s24.total_revenue)} revenue, down from 88% in its first year, with private contributions rising from $169K to $558K; SheWorks itself launched in late 2025 with labor-federation and health-plan partners, so its funding will only appear in TY2025+ filings.",
                 "m10_01; notes_for_analysis §8", ["m10_01_comparator_trajectories"], ["fact_org_financials", "fact_grants"], "$1.8M, 70% government", "medium",
                 "SheWorks is a program design to borrow (stipends, childcare, ride credits, employer and health-plan partners), not a funding model to copy; Calvary's Step Up DC is the natural host.", "both")
log(S, [f"profiles written; DWC FAC total {gd.amount.sum():,.0f}; DWC DMV-filed funders {len(dwc_filed)}", "charts m10_01, m10_02 written"])
