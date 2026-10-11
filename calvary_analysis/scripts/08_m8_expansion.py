"""M8: Mission-expansion scan. For each adjacent program area: DMV institutional dollars whose purpose names it,
funders active in it, federal opportunities, DC budget lines, peer examples, and the distance from Calvary's
current operations (config/expansion_areas.yaml)."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import style  # noqa: E402
from lib.common import ANALYSIS, CLEAN, load, log, money, register_insight, save_chart_data  # noqa: E402

S = "08_m8_expansion"
CFG = yaml.safe_load(open(ANALYSIS / "config" / "expansion_areas.yaml"))
areas = pd.DataFrame(CFG["areas"])
GR = ["funder_id", "recipient_ein", "recipient_state", "tax_year", "amount", "cumulative_flag", "program_area_tags", "source_type", "source_id"]
gr = load("fact_grants", usecols=GR)
excl = pd.read_csv(ANALYSIS / "config" / "landscape_exclusions.csv", dtype=str)
gr = gr[(gr.cumulative_flag != 1) & gr.source_type.isin(["pf_grants_paid", "schedule_i"]) & gr.tax_year.between(2020, 2024) & gr.recipient_state.isin(["DC", "MD", "VA"]) & ~gr.funder_id.isin(set(excl.funder_id))]
df = load("dim_funder", usecols=["funder_id", "funder_type"]).set_index("funder_id").funder_type
gr = gr[gr.funder_id.map(df).ne("daf_sponsor")]
src = sorted(gr.source_id.unique())
tg = gr.assign(tag=gr.program_area_tags.fillna("other").str.split(";")).explode("tag").reset_index(drop=True)
tg["is_dc"] = tg.recipient_state == "DC"
by_tag = tg.groupby("tag").agg(dmv_amount=("amount", "sum"), dc_amount=("amount", lambda s: s[tg.loc[s.index, "is_dc"]].sum()), funders=("funder_id", "nunique"), grants=("amount", "size"), median_grant=("amount", "median"))
by_tag["funders_100k_plus"] = tg.groupby(["tag", "funder_id"]).amount.sum().reset_index().query("amount >= 100000").groupby("tag").funder_id.nunique()
o = load("fact_opportunities")
RELEVANT_AGENCIES = "Housing and Urban Development|Veterans|Employment and Training|VETS|Justice|Violence Against Women|Children and Families|Substance Abuse|SAMHSA|Agriculture|Treasury|Community Services|Administration for Community Living|Economic Development"
o = o[o.funder_name.str.contains(RELEVANT_AGENCIES, na=False) & ~o.title.str.contains("Tribal|Indian|Native|Research|Clinical|Rural|Surveillance|polio", case=False, na=False)]
ot = o.assign(tag=o.program_area_tags.fillna("other").str.split(";")).explode("tag").reset_index(drop=True)
by_opp = ot.groupby("tag").agg(federal_opps=("opportunity_id", "nunique"), posted=("status", lambda s: (s == "posted").sum()), est_total_funding=("estimated_total_funding", "sum"), median_ceiling=("award_ceiling", "median"))
pe = load("fact_policy_events")
pt = pe.assign(tag=pe.program_area_tags.fillna("other").str.split(";")).explode("tag").reset_index(drop=True)
by_pol = pt.groupby("tag").agg(dc_policy_events=("event_id", "nunique"), dc_enacted_amount_fy2026=("amount", lambda s: s[(pt.loc[s.index, "event_type"] == "budget_enacted") & (pt.loc[s.index, "fiscal_year"] == 2026)].max()))
scan = areas.merge(by_tag, left_on="tag", right_index=True, how="left").merge(by_opp, left_on="tag", right_index=True, how="left").merge(by_pol, left_on="tag", right_index=True, how="left")
scan = scan.fillna({"dmv_amount": 0, "dc_amount": 0, "funders": 0, "grants": 0, "funders_100k_plus": 0, "federal_opps": 0, "posted": 0, "est_total_funding": 0, "dc_policy_events": 0})
scan["dmv_amount_per_year"] = scan.dmv_amount / 5
dist_rank = {"core": 0, "near": 1, "medium": 2, "far": 3}
scan["distance_rank"] = scan.distance.map(dist_rank)
scan = scan.sort_values(["distance_rank", "dmv_amount"], ascending=[True, False]).reset_index(drop=True)
save_chart_data(scan, "m8_01_expansion_scan", "Mission-expansion scan: dollars, funders, federal opportunities and DC budget signals by adjacent program area, with distance from Calvary's operations",
                ["fact_grants", "dim_program_area", "fact_opportunities", "fact_policy_events", "dim_funder"], src + ["api_grantsgov"], S, "distance and examples are analyst judgment in config/expansion_areas.yaml (basis=inferred)")

f, ax = style.fig(10.5, 6.4)
d = scan.iloc[::-1]
cols = {"core": style.SERIES["government"], "near": style.SERIES["institutional"], "medium": style.SERIES["daf"], "far": style.PEER_COLOR}
bars = ax.barh(d.label, d.dmv_amount_per_year, color=[cols[x] for x in d.distance], height=0.62)
for b_, v, fnd, f100, fo in zip(bars, d.dmv_amount_per_year, d.funders, d.funders_100k_plus, d.federal_opps):
    ax.annotate(f"{money(v,'M',1)}/yr · {int(fnd)} funders ({int(f100)} at $100K+) · {int(fo)} federal opps", (v, b_.get_y() + b_.get_height() / 2), xytext=(4, 0), textcoords="offset points", va="center", fontsize=8, color=style.TEXT_2)
from matplotlib.patches import Patch  # noqa: E402
ax.legend(handles=[Patch(color=cols[k], label=f"{k}: {lab}") for k, lab in [("core", "current mission"), ("near", "already delivered in some form"), ("medium", "same clients, new capability"), ("far", "new population or licensing")]], loc="lower right", fontsize=8)
style.money_axis(ax, "M", "x"); ax.set_xlim(0, d.dmv_amount_per_year.max() * 1.6); ax.grid(axis="y", visible=False); ax.grid(axis="x", visible=True); ax.tick_params(axis="y", labelsize=8.5)
style.finish(f, ax, "m8_01_expansion_scan",
             "Health and workforce funding pools are large and only one step from Calvary's current programs; aging, veterans and reentry pools are small",
             "fact_grants purpose text tagged by dim_program_area (DMV institutional funders, DC/MD/VA recipients, TY2020-24); fact_opportunities (Grants.gov, filtered); fact_policy_events",
             note="Dollars whose purpose text names the area; general-operating money is excluded, so these understate what a funder would give. Distance ratings are analyst judgment (config/expansion_areas.yaml).")

# federal opportunities table for the areas
fed = ot[ot.tag.isin(areas.tag)].drop_duplicates("opportunity_id")[["opportunity_number", "title", "funder_name", "status", "award_ceiling", "estimated_total_funding", "close_date", "program_area_tags", "url"]].sort_values(["status", "close_date"])
save_chart_data(fed, "m8_02_federal_opportunities", "Federal opportunities (Grants.gov) tagged to Calvary's core or adjacent areas, after removing research, tribal and overseas notices", ["fact_opportunities"], ["api_grantsgov"], S)
print(scan[["label", "distance", "dmv_amount_per_year", "dc_amount", "funders", "funders_100k_plus", "median_grant", "federal_opps", "posted", "dc_policy_events"]].round(0).to_string())
print(fed.head(30)[["opportunity_number", "title", "funder_name", "status", "award_ceiling", "close_date", "program_area_tags"]].to_string())
near = scan[scan.distance == "near"]
register_insight("M8-01", "M8", f"The adjacent areas Calvary already touches (DV, behavioral health, workforce, education) carry about {money(near.dmv_amount_per_year.sum())} a year of DMV institutional grants whose purpose names them; physical health is the largest pool one step further ({money(scan.set_index('tag').loc['health','dmv_amount_per_year'])}/yr, {int(scan.set_index('tag').loc['health','funders_100k_plus'])} funders at $100K+).",
                 "m8_01_expansion_scan", ["m8_01_expansion_scan"], ["fact_grants", "dim_program_area", "fact_opportunities"], f"{money(near.dmv_amount_per_year.sum())}/yr near pools", "medium",
                 "Formalizing what Calvary already does (workforce, behavioral health, DV designation) opens funders without changing the mission; health and aging need a partner or credential.", "both")
register_insight("M8-02", "M8", f"The Grants.gov feed yields only {len(fed)} relevant federal notices across all areas after filtering; the federal path for Calvary runs through DC intermediaries (TCP, OVSJG, DHS), not direct competition.",
                 "m8_02_federal_opportunities", ["m8_01_expansion_scan"], ["fact_opportunities"], f"{len(fed)} notices", "high",
                 "Direct federal grants are a Tier 3 option; HUD CoC via TCP and HUD CPF earmarks are the realistic federal channels.", "both")
log(S, [f"scan {len(scan)} areas; federal relevant {len(fed)}", "chart m8_01 written"])
