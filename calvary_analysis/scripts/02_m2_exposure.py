"""M2: Government exposure and stress test.

Stream-by-stream map of Calvary's government money (one source per stream, never summed across
sources), award ceilings vs recognized government revenue, DC budget context, Calvary's share of the
OVSJG and CoC pools, the policy timeline, and revenue/cash scenarios from config/scenarios.yaml.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import style  # noqa: E402
from lib.common import ANALYSIS, CALVARY, load, log, money, register_insight, save_chart_data  # noqa: E402

S = "02_m2_exposure"
CFG = yaml.safe_load(open(ANALYSIS / "config" / "scenarios.yaml"))
G_COLS = ["recipient_ein", "recipient_name_raw", "awarding_agency", "program_name", "assistance_listing", "flow_type",
          "pass_through_entity", "fiscal_year", "fiscal_year_basis", "amount", "amount_type", "source_type", "source_id", "notes"]
g = load("fact_gov_awards", usecols=G_COLS)
cg = g[g.recipient_ein == CALVARY].copy()
src_gov = sorted(cg.source_id.unique())

# ------------------------------------------------------------------ stream map (one source per stream)
ov = cg[cg.source_type == "dc_ovsjg"].copy()
ov["program"] = np.where(ov.program_name.str.contains("New Foundations"), "OVSJG: New Foundations TH", "OVSJG: Reach Up TH")
ov["one_time"] = ov.amount == 3680675
coc = cg[cg.source_type == "hud_coc"].copy()
coc["project"] = coc.program_name.str.split(" - ").str[-1].str.replace(" Reallocation", "", regex=False).str.strip()
coc["project"] = coc.project.replace({"Sister Circle": "CoC: Sister Circle PSH", "Reach Up": "CoC: Reach Up", "New Foundations 2": "CoC: New Foundations 2"})
dhs = cg[cg.source_type == "dc_oversight"].copy()
dhs["program"] = np.where(dhs.program_name.str.contains("Sisters Rise"), "DHS/TCP: Sisters Rise EHV", "DHS/TCP: Transitional Housing")
sefa = cg[cg.source_type == "audit_sefa"].copy()
sefa["program"] = np.where(sefa.assistance_listing == "21.027", "SLFRF via OVSJG (one-time)",
                  np.where(sefa.assistance_listing == "14.235", "CoC 14.235 via TCP (expenditure)",
                  np.where(sefa.assistance_listing == "97.024", "EFSP via FEMA", "SNAP E&T via DHS")))
usa = cg[cg.source_type == "usaspending"].copy()

recurring = pd.concat([
    ov[~ov.one_time].assign(stream="OVSJG (DC local)", detail=ov.program, year_basis="DC FY")[["stream", "detail", "fiscal_year", "amount", "year_basis", "source_type", "source_id"]],
    coc.assign(stream="HUD CoC via TCP (federal)", detail=coc.project, year_basis="HUD CoC competition FY")[["stream", "detail", "fiscal_year", "amount", "year_basis", "source_type", "source_id"]],
    dhs.assign(stream="DHS via TCP (DC local)", detail=dhs.program, year_basis="DC FY")[["stream", "detail", "fiscal_year", "amount", "year_basis", "source_type", "source_id"]],
    sefa[sefa.assistance_listing.isin(["97.024", "10.561"])].assign(stream="Other federal pass-through", detail=sefa.program, year_basis="Calvary FY (expenditure)")[["stream", "detail", "fiscal_year", "amount", "year_basis", "source_type", "source_id"]],
], ignore_index=True)
one_time = pd.concat([
    ov[ov.one_time].assign(stream="SLFRF via OVSJG: New Foundations building", year_basis="DC FY")[["stream", "fiscal_year", "amount", "year_basis", "source_type", "source_id"]],
    usa.assign(stream=usa.program_name.str.title().str.slice(0, 60), year_basis="federal FY")[["stream", "fiscal_year", "amount", "year_basis", "source_type", "source_id"]],
], ignore_index=True)
recurring["fiscal_year"] = recurring.fiscal_year.astype(int)
save_chart_data(recurring.sort_values(["stream", "detail", "fiscal_year"]), "m2_01_stream_map",
                "Calvary recurring government streams by award year and channel (one source per stream)",
                ["fact_gov_awards"], src_gov, S,
                "OVSJG and DHS by DC FY (Oct-Sep, same as Calvary FY); CoC by HUD competition year; the $3.68M FY2022 SLFRF building award is excluded as one-time")
save_chart_data(one_time, "m2_01b_one_time_awards", "Calvary one-time government awards", ["fact_gov_awards"], src_gov, S)

piv = recurring.pivot_table(index="fiscal_year", columns="stream", values="amount", aggfunc="sum").fillna(0)
piv = piv.reindex(range(2019, 2027)).fillna(0)
order = ["OVSJG (DC local)", "HUD CoC via TCP (federal)", "DHS via TCP (DC local)", "Other federal pass-through"]
piv = piv[[c for c in order if c in piv.columns]]
colors = {"OVSJG (DC local)": style.SERIES["government"], "HUD CoC via TCP (federal)": style.SERIES["daf"],
          "DHS via TCP (DC local)": style.SERIES["institutional"], "Other federal pass-through": style.SERIES["other"]}
f, ax = style.fig(10.5, 5.8)
bottom = np.zeros(len(piv))
labels = [str(y) for y in piv.index]
for c in piv.columns:
    ax.bar(labels, piv[c].values, bottom=bottom, color=colors[c], width=0.62, label=c, edgecolor="white", linewidth=1.5)
    bottom += piv[c].values
for i, t in enumerate(bottom):
    if t > 0:
        ax.text(i, t + 4e4, f"${t/1e6:,.2f}M", ha="center", fontsize=8.5, color=style.TEXT_2)
style.money_axis(ax)
ax.set_ylim(0, bottom.max() * 1.15)
ax.legend(loc="upper left")
ax.set_xlabel("Award year (DC FY for OVSJG and DHS; HUD CoC competition year; expenditure year for other federal)")
style.finish(f, ax, "m2_01_stream_map",
             "Calvary's recurring government awards grew from $0.6M (2020) to about $4.1M (2024) across three channels",
             "fact_gov_awards: dc_ovsjg, hud_coc, dc_oversight, audit_sefa rows for Calvary (one source per stream)",
             note="DHS/TCP contract values are public for DC FY2024 only; other years show no DHS bar because the figure is unknown, not zero. Excludes the one-time $3.68M SLFRF award (FY2022). The 2019 OVSJG value adds two Reach Up records ($292,000 and $368,935) that may be a start-up grant plus a continuation or one award recorded twice (review finding M06).")

# ------------------------------------------------------------------ award ceilings aligned to Calvary FY vs recognized government revenue
lag = int(CFG["coc_award_lag_years"])
fin = load("fact_org_financials", usecols=["ein", "fiscal_year", "return_type", "preferred", "total_revenue", "government_grants"])
cal = fin[fin.ein == CALVARY]
aud = cal[cal.return_type == "audit"].set_index("fiscal_year").government_grants
pref = cal[cal.preferred == 1].set_index("fiscal_year")
recog = aud.reindex(range(2019, 2026)).fillna(pref.government_grants)
basis = pd.Series(np.where(aud.reindex(range(2019, 2026)).notna(), "audit", "990 line 1e"), index=range(2019, 2026))
ovs = ov[~ov.one_time].groupby("fiscal_year").amount.sum()
cocs = coc.groupby("fiscal_year").amount.sum()
cocs.index = cocs.index + lag
dhss = dhs.groupby("fiscal_year").amount.sum()
if CFG["dhs_assumed_flat_from_fy2024"]:
    dhss = dhss.reindex(range(2024, 2027)).ffill()
oth = sefa[sefa.assistance_listing.isin(["97.024", "10.561"])].groupby("fiscal_year").amount.sum()
oth = oth.reindex(range(2019, 2027)).ffill().bfill()  # EFSP + SNAP E&T are small; carry the audited FY23 level forward
slfrf_exp = sefa[sefa.assistance_listing == "21.027"].groupby("fiscal_year").amount.sum()
al = pd.DataFrame({"fiscal_year": range(2019, 2026)})
al["ovsjg_award"] = al.fiscal_year.map(ovs).fillna(0)
al["coc_award_lagged"] = al.fiscal_year.map(cocs).fillna(0)
al["dhs_award"] = al.fiscal_year.map(dhss)
al["other_federal"] = al.fiscal_year.map(oth)
al["slfrf_expenditure"] = al.fiscal_year.map(slfrf_exp).fillna(0)
al["award_ceiling_known"] = al[["ovsjg_award", "coc_award_lagged", "dhs_award", "other_federal"]].sum(axis=1)
al["recognized_gov_revenue"] = al.fiscal_year.map(recog)
al["recognized_basis"] = al.fiscal_year.map(basis)
al["recognized_ex_slfrf"] = al.recognized_gov_revenue - al.slfrf_expenditure
al["total_revenue"] = al.fiscal_year.map(pref.total_revenue)
al["gov_share"] = al.recognized_gov_revenue / al.total_revenue
al["ratio_recognized_ex_slfrf_to_ceiling"] = al.recognized_ex_slfrf / al.award_ceiling_known
al["fy_label"] = "FY" + al.fiscal_year.astype(str).str[2:]
save_chart_data(al, "m2_02_ceilings_vs_recognized", "Government award ceilings aligned to Calvary FY vs recognized government revenue",
                ["fact_gov_awards", "fact_org_financials"], src_gov + sorted(cal.source_id.unique()) if "source_id" in cal else src_gov, S,
                f"CoC competition year t -> Calvary FY t+{lag}; DHS FY2024 value carried forward; EFSP/SNAP at audited FY23 level; DHS unknown before FY2024 (ceiling understated FY19-23)")
a2 = al[al.fiscal_year >= 2024].reset_index(drop=True)
f, ax = style.fig(10, 5.8)
x = np.arange(len(a2)); w = 0.34
bottom = np.zeros(len(a2))
for col, lab, role in [("ovsjg_award", "OVSJG awards (DC FY)", "government"), ("coc_award_lagged", "HUD CoC awards (prior competition year)", "daf"),
                       ("dhs_award", "DHS/TCP contracts (FY2024 value, carried forward)", "institutional"), ("other_federal", "EFSP + SNAP E&T (FY23 level)", "other")]:
    ax.bar(x - w / 2 - 0.02, a2[col], w, bottom=bottom, color=style.SERIES[role], label=lab, edgecolor="white", linewidth=1.5)
    bottom += a2[col].values
ax.bar(x + w / 2 + 0.02, a2.recognized_gov_revenue, w, color=style.PEER_COLOR, label="Recognized government revenue (990 line 1e)")
for xi in range(len(a2)):
    ax.text(xi - w / 2 - 0.02, bottom[xi] + 5e4, f"ceilings ${bottom[xi]/1e6:,.2f}M", ha="center", fontsize=9, color=style.TEXT_2)
    ax.text(xi + w / 2 + 0.02, a2.recognized_gov_revenue[xi] + 5e4,
            f"recognized ${a2.recognized_gov_revenue[xi]/1e6:,.2f}M\n({a2.ratio_recognized_ex_slfrf_to_ceiling[xi]:.0%} of ceilings)",
            ha="center", fontsize=9, color=style.TEXT_2)
ax.set_xticks(x, a2.fy_label)
style.money_axis(ax)
ax.set_ylim(0, bottom.max() * 1.25)
ax.legend(loc="upper left", fontsize=8.5)
style.finish(f, ax, "m2_02_ceilings_vs_recognized",
             "Calvary recognized about two-thirds of its known award ceilings as revenue in FY24 and FY25",
             "fact_gov_awards (Calvary award rows) and fact_org_financials (Calvary 990 FY24-25)",
             note="Ceilings are award amounts aligned to Calvary's fiscal year, not revenue; DHS/TCP values are public for FY2024 only and are carried into FY25. 990 line 1e matched the audited government revenue exactly in FY22 and FY23.")

# ------------------------------------------------------------------ stream durability table
latest = {}
for stream, df_, col in [("OVSJG (DC local)", ov[~ov.one_time], "program"), ("HUD CoC via TCP (federal)", coc, "project"),
                         ("DHS via TCP (DC local)", dhs, "program")]:
    for d, sub in df_.groupby(col):
        sub = sub.sort_values("fiscal_year")
        latest[d] = {"stream": stream, "detail": d, "first_year": int(sub.fiscal_year.min()), "latest_year": int(sub.fiscal_year.max()),
                     "latest_amount": float(sub[sub.fiscal_year == sub.fiscal_year.max()].amount.sum()),
                     "first_amount": float(sub[sub.fiscal_year == sub.fiscal_year.min()].amount.sum()), "years_observed": int(sub.fiscal_year.nunique())}
dur = pd.DataFrame(latest.values())
dur["change_first_to_latest"] = dur.latest_amount / dur.first_amount - 1
meta = {
    "OVSJG: Reach Up TH": ("DC local funds (FY24-26 lists); SLFRF-funded in FY22-23", "Annual OVSJG grant; continuation funding", "Medium: annual, Mayor proposed cuts to Victim Services grants in FY26 and FY27, Council restored both"),
    "OVSJG: New Foundations TH": ("DC local funds", "Annual OVSJG grant; started FY23 after the FY22 building award", "Medium: as above; tied to a DV-designated site"),
    "CoC: Sister Circle PSH": ("Federal HUD CoC 14.267 via TCP", "Annual renewal in the DC CoC competition", "Medium-low: PSH renewals are usually protected; FY2025 renewals were paid in full after the NOFO was enjoined, and the FY2026 competition (awards about December 2026) is the live question"),
    "CoC: Reach Up": ("Federal HUD CoC 14.267 via TCP", "Annual renewal; expanded in 2024", "Medium: TCP reallocation cut it from $1.22M to $0.42M in 2022, then it grew to $0.92M"),
    "CoC: New Foundations 2": ("Federal HUD CoC 14.267 via TCP", "Annual renewal; new in 2023", "Medium: a young project is the first to go in a tight competition"),
    "DHS/TCP: Transitional Housing": ("DC local funds via TCP (DHS Homeless Services Continuum)", "Annual provider contract via TCP (45 beds)", "Medium-high: single public data point; TCP's DHS POs fell sharply in FY2025 after DC's financial-system change"),
    "DHS/TCP: Sisters Rise EHV": ("DC local funds via TCP, paired with Emergency Housing Vouchers", "Annual provider contract (25 units); the project left the HIC in 2025", "High: HUD's 29 September 2026 notice ends the EHV program (vouchers convert by 31 December 2026 and cannot be reissued); the 2025 HIC no longer lists Sisters Rise PSH"),
}
dur["funding_source"] = dur.detail.map(lambda d: meta[d][0])
dur["renewal_mechanism"] = dur.detail.map(lambda d: meta[d][1])
dur["durability_risk"] = dur.detail.map(lambda d: meta[d][2])
dur = dur.sort_values(["stream", "detail"])
save_chart_data(dur, "m2_03_stream_durability", "Calvary government streams: size, trend, funding source, renewal mechanism and durability risk",
                ["fact_gov_awards", "fact_policy_events", "supp_hic_projects"], src_gov, S, "risk ratings are analyst judgment (basis=inferred)")

# ------------------------------------------------------------------ DC budget context
b = pd.read_csv(ANALYSIS.parent / "calvary_funding_data" / "clean" / "supp_dc_budget_lines.csv", low_memory=False)
b = b[(b.x_preferred == 1) & (b.fund_type == "total") & (b.x_level == "activity")]
groups = {"OVSJG Victim Services grants (P02303)": ["P02303"],
          "DHS homeless services continuum (H03002-04, H03009)": ["H03002", "H03003", "H03004", "H03009"],
          "DHS permanent supportive housing (H03010-13)": ["H03010", "H03011", "H03012", "H03013"],
          "DHS domestic violence services (H03007)": ["H03007"]}
rows = []
for gname, codes in groups.items():
    sub = b[b.program_code.isin(codes)]
    for (fy, stage), s2 in sub.groupby(["fiscal_year", "budget_stage"]):
        if s2.program_code.nunique() == len(codes):
            rows.append({"group": gname, "fiscal_year": int(fy), "budget_stage": stage, "amount": float(s2.amount.sum())})
bud = pd.DataFrame(rows).sort_values(["group", "budget_stage", "fiscal_year"])
save_chart_data(bud, "m2_04_dc_budget_context", "DC budget lines behind Calvary's local streams: approved vs actual, FY2021-FY2027",
                ["supp_dc_budget_lines"], sorted(b.source_id.unique()), S, "sums of activity-level 'total' rows per program code; proposed = Mayor's FY2026 proposal as reported by Council committees")
import matplotlib.pyplot as plt  # noqa: E402
style.apply()
f, axes = plt.subplots(2, 2, figsize=(11, 7))
for ax, (gname, _) in zip(axes.flat, groups.items()):
    sub = bud[bud.group == gname]
    for stage, col, mk in [("approved", style.SERIES["government"], "o"), ("actual", style.SERIES["institutional"], "s"), ("proposed", style.NEGATIVE, "D")]:
        s2 = sub[sub.budget_stage == stage]
        if len(s2):
            ax.plot(s2.fiscal_year, s2.amount, color=col, marker=mk, ms=6, markeredgecolor="white", markeredgewidth=1.5,
                    lw=2 if stage != "proposed" else 0, label=stage.capitalize() + (" (Mayor, FY26)" if stage == "proposed" else ""))
    ax.set_title(gname, fontsize=10.5, loc="left", color=style.INK)
    ax.set_ylim(0, sub.amount.max() * 1.2)
    style.money_axis(ax)
    ax.set_xticks(sorted(sub.fiscal_year.unique()))
    ax.set_xticklabels([f"FY{y}" for y in sorted(sub.fiscal_year.unique())], fontsize=8.5)
    ax.legend(loc="lower right", fontsize=8)
f.suptitle("Since pandemic money ended in FY2023, DC's homeless and victim-services budgets have held flat to rising\nthrough FY2027, with cuts proposed each spring",
           x=0.01, ha="left", fontsize=12, fontweight="bold", color=style.INK)
f.text(0.01, 0.005, "Source: supp_dc_budget_lines (DC budget books FY2024-FY2027, Council committee reports). Data as of 2026-10-10. Chart m2_04_dc_budget_context.",
       fontsize=7.5, color=style.TEXT_MUTED)
style.polish(f, "m2_04_dc_budget_context"); f.tight_layout(rect=(0, 0.03, 1, 0.93))
f.savefig(style.CHARTS / "m2_04_dc_budget_context.png", dpi=200); plt.close(f)

# ------------------------------------------------------------------ Calvary's share of the OVSJG and CoC pools
ov_all = g[g.source_type == "dc_ovsjg"].groupby("fiscal_year").amount.sum()
coc_all = g[g.source_type == "hud_coc"].groupby("fiscal_year").amount.sum()
sh = pd.DataFrame({"fiscal_year": range(2019, 2027)})
sh["ovsjg_total"] = sh.fiscal_year.map(ov_all); sh["ovsjg_calvary"] = sh.fiscal_year.map(ov.groupby("fiscal_year").amount.sum())
sh["ovsjg_calvary_recurring"] = sh.fiscal_year.map(ovs)
sh["ovsjg_share"] = sh.ovsjg_calvary / sh.ovsjg_total
sh["coc_total"] = sh.fiscal_year.map(coc_all); sh["coc_calvary"] = sh.fiscal_year.map(coc.groupby("fiscal_year").amount.sum())
sh["coc_share"] = sh.coc_calvary / sh.coc_total
save_chart_data(sh, "m2_05_pool_shares", "Calvary's share of all OVSJG awards and of DC CoC awards by year", ["fact_gov_awards"], src_gov, S,
                "OVSJG totals = all recipients in the OVSJG award lists; CoC totals = all DC-500 projects in HUD award lists")
f, ax = style.fig(10, 5)
ax.plot(sh.fiscal_year, sh.coc_share, color=style.SERIES["daf"], marker="o", ms=6, markeredgecolor="white", markeredgewidth=1.5, label="Share of DC CoC awards (HUD)")
ax.plot(sh.fiscal_year, sh.ovsjg_share, color=style.SERIES["government"], marker="o", ms=6, markeredgecolor="white", markeredgewidth=1.5, label="Share of all OVSJG awards (DC)")
for yv, v in zip(sh.fiscal_year, sh.coc_share):
    if pd.notna(v):
        ax.text(yv, v + 0.003, f"{v:.1%}", ha="center", fontsize=8, color=style.TEXT_2)
for yv, v in zip(sh.fiscal_year, sh.ovsjg_share):
    if pd.notna(v):
        ax.text(yv, v - 0.006, f"{v:.1%}", ha="center", fontsize=8, color=style.TEXT_2)
style.pct_axis(ax); ax.set_ylim(0, 0.07)
ax.set_xticks(sh.fiscal_year); ax.legend(loc="upper left")
style.finish(f, ax, "m2_05_pool_shares",
             "Calvary draws 5% of DC's CoC money and about 1% of OVSJG's, so it depends on pools it cannot move",
             "fact_gov_awards: HUD CoC award lists (DC-500) and OVSJG award lists, all recipients",
             note="FY2022 OVSJG share (4.6%) includes the one-time $3.68M building award.")

# ------------------------------------------------------------------ policy timeline (events touching Calvary's channels)
pe = load("fact_policy_events")
sel = pe[pe.agency.str.contains("Victim Services|Human Services", na=False) & pe.amount_change.notna()
         & (pe.amount_change.abs() >= 1e6) & pe.event_type.isin(["budget_proposed", "budget_revised", "budget_enacted"])
         & pe.description.str.contains("Victim Services|homeless|Homeless|Permanent Supportive|Domestic Violence|Continuum|shelter|Rapid Re|FRSP|ERAP", case=False, na=False)].copy()
sel = sel[~sel.description.str.contains("Department of Human Services total|total \\(as printed", na=False)]
sel["event_date"] = pd.to_datetime(sel.event_date)
sel = sel.sort_values("event_date")
save_chart_data(sel[["event_id", "event_date", "event_type", "agency", "funding_stream", "description", "amount", "prior_amount", "amount_change", "fiscal_year", "source_id"]],
                "m2_06_policy_timeline", "DC budget events of $1M+ touching homeless, PSH, DV and victim-services lines, FY2024-FY2027",
                ["fact_policy_events"], sorted(sel.source_id.unique()), S)
key = sel[sel.description.str.contains("Victim Services|Domestic Violence|Permanent Supportive|Homeless Services Continuum|FRSP|Re-housing|ERAP|homeless services", case=False, na=False)].copy()
key = key[(key.amount_change.abs() >= 2e6) & key.event_date.notna()].sort_values("event_date").tail(14)


def short_desc(r):
    d = r.description.split("[")[0]
    for a, b_ in [("Mayor's proposed FY2026 budget ", ""), ("Committee on Human Services recommended change to the Mayor's proposed FY2026 budget for ", "Council: "),
                  ("FY2026 approved budget vs FY2025 approved (all funds): ", "Enacted FY26 vs FY25: "), ("FY2025 approved budget vs FY2024 approved (all funds): ", "Enacted FY25 vs FY24: "),
                  ("FY2024 approved budget vs FY2023 approved (all funds): ", "Enacted FY24 vs FY23: "), ("FY2027 approved budget vs FY2026 approved (all funds): ", "Enacted FY27 vs FY26: ")]:
        d = d.replace(a, b_)
    for yr_ in ["2024", "2025", "2026", "2027"]:
        d = d.replace(f" (as printed in the FY{yr_} book)", "")
    stage = {"budget_proposed": "Mayor", "budget_revised": "Council", "budget_enacted": "Enacted"}[r.event_type]
    return f"{r.event_date:%Y-%m} {stage}: {d.strip()[:70]}"


key["label"] = key.apply(short_desc, axis=1)
f, ax = style.fig(11, 6.5)
cols = [style.NEGATIVE if v < 0 else style.POSITIVE for v in key.amount_change]
bars = ax.barh(key.label, key.amount_change, color=cols, height=0.6)
for b_, v in zip(bars, key.amount_change):
    ax.annotate(f"{'+' if v>0 else '−'}${abs(v)/1e6:,.1f}M", (v, b_.get_y() + b_.get_height() / 2), xytext=(4 if v > 0 else -4, 0),
                textcoords="offset points", va="center", ha="left" if v > 0 else "right", fontsize=8, color=style.TEXT_2)
ax.axvline(0, color=style.TEXT_2, lw=0.8)
ax.grid(axis="y", visible=False); ax.grid(axis="x", visible=True)
ax.tick_params(axis="y", labelsize=8)
style.money_axis(ax, "M", axis="x")
ax.set_xlim(min(key.amount_change.min() * 1.3, -5e6), key.amount_change.max() * 1.3)
ax.invert_yaxis()
style.finish(f, ax, "m2_06_policy_timeline",
             "Since 2023 the Mayor has proposed cuts to victim-services and DV lines each spring and the Council has restored them",
             "fact_policy_events: DC budget books FY2024-FY2027, Council committee reports, Budget Support Act",
             note="Budget events of $2M or more touching the homeless continuum, PSH, DV and victim-services lines; newest at the bottom.")

# ------------------------------------------------------------------ scenarios
fy = int(CFG["baseline_fiscal_year"])
base_row = al[al.fiscal_year == fy].iloc[0]
gov_recog = float(base_row.recognized_gov_revenue)
ceil = {"ovsjg": float(base_row.ovsjg_award), "coc": float(base_row.coc_award_lagged), "dhs": float(base_row.dhs_award), "other": float(base_row.other_federal)}
coc_proj = coc[coc.fiscal_year == fy - lag].groupby("project").amount.sum()
nf2_share_of_coc = float(coc_proj.get("CoC: New Foundations 2", 0) / coc_proj.sum())
tot_ceil = sum(ceil.values())
alloc = {k: v / tot_ceil * gov_recog for k, v in ceil.items()}   # recognized revenue apportioned by ceiling shares
total_rev = float(pref.loc[fy].total_revenue); expenses = float(fin[(fin.ein == CALVARY) & (fin.preferred == 1) & (fin.fiscal_year == fy)].total_revenue.iloc[0] - (pref.loc[fy].total_revenue - load("fact_org_financials", usecols=["ein", "fiscal_year", "preferred", "total_expenses"]).query("ein == @CALVARY and preferred == 1 and fiscal_year == @fy").total_expenses.iloc[0]))
fin2 = load("fact_org_financials", usecols=["ein", "fiscal_year", "preferred", "total_expenses", "cash_savings_eoy"]).query("ein == @CALVARY and preferred == 1 and fiscal_year == @fy").iloc[0]
expenses = float(fin2.total_expenses); cash = float(fin2.cash_savings_eoy)
base_deficit = total_rev - expenses
ca = float(CFG["cost_avoidance_share"])
rows = [{"scenario_id": "S0", "scenario": f"Baseline FY{str(fy)[2:]} (actual)", "revenue_loss": 0.0}]
for sc in CFG["scenarios"]:
    loss = 0.0
    for k, pct in sc["cuts"].items():
        if k == "coc_project_new_foundations_2":
            loss += alloc["coc"] * nf2_share_of_coc * pct
        else:
            loss += alloc[k] * pct
    rows.append({"scenario_id": sc["id"], "scenario": sc["name"], "revenue_loss": loss, "rationale": sc["rationale"]})
scn = pd.DataFrame(rows)
# Ranges across defensible apportionments (review finding R01). Streams are not drawn at a common rate (CoC drew 28-62%
# of its ceiling in the audited FY22-23 SEFA), so stream-level losses are reported as ranges, not point estimates.
#   A  recognized revenue split by award-ceiling share (the point estimate in revenue_loss)
#   B  OVSJG and other federal fully drawn, CoC at the audited FY22-23 SEFA draw rate, DHS the residual
#   C  ceiling share without Sisters Rise, which left the HIC in 2025
#   D  OVSJG and CoC fully drawn, DHS the residual: a floor case that nearly removes the DHS loss; reported, not a bound
coc_by_comp = coc.groupby("fiscal_year").amount.sum()
sefa_coc = sum(sefa[(sefa.fiscal_year == y) & sefa.program_name.str.contains("Supportive Housing", na=False)].amount.sum() for y in (2022, 2023))
coc_draw_rate = sefa_coc / (coc_by_comp.get(2021, 0) + coc_by_comp.get(2022, 0))
sisters_rise = dhs[dhs.program_name.str.contains("Sisters Rise")].amount.sum()
split_b = {"ovsjg": ceil["ovsjg"], "other": ceil["other"], "coc": ceil["coc"] * coc_draw_rate}; split_b["dhs"] = gov_recog - sum(split_b.values())
ceil_c = dict(ceil, dhs=ceil["dhs"] - sisters_rise)
split_c = {k: v / sum(ceil_c.values()) * gov_recog for k, v in ceil_c.items()}
split_d = {"ovsjg": ceil["ovsjg"], "other": ceil["other"], "coc": ceil["coc"]}; split_d["dhs"] = gov_recog - sum(split_d.values())
def scenario_loss(sc, split):
    return sum(split["coc"] * nf2_share_of_coc * pct if k == "coc_project_new_foundations_2" else split[k] * pct for k, pct in sc["cuts"].items())
alt = {sc["id"]: [scenario_loss(sc, sp) for sp in (alloc, split_b, split_c)] for sc in CFG["scenarios"]}
scn["revenue_loss_low"] = scn.scenario_id.map(lambda i: min(alt[i]) if i in alt else 0.0)
scn["revenue_loss_high"] = scn.scenario_id.map(lambda i: max(alt[i]) if i in alt else 0.0)
scn["revenue_loss_floor_case_d"] = scn.scenario_id.map(lambda i: scenario_loss(next(c for c in CFG["scenarios"] if c["id"] == i), split_d) if i in alt else 0.0)
scn["loss_pct_of_total_revenue"] = scn.revenue_loss / total_rev
scn["loss_pct_of_gov_revenue"] = scn.revenue_loss / gov_recog
scn["deficit_gross"] = base_deficit - scn.revenue_loss
scn["deficit_net_of_cost_avoidance"] = base_deficit - scn.revenue_loss * (1 - ca)
scn["months_of_cash_after_12m_gross"] = (cash + scn.deficit_gross).clip(lower=0) / (expenses / 12)
scn["months_of_cash_after_12m_net"] = (cash + scn.deficit_net_of_cost_avoidance).clip(lower=0) / (expenses / 12)
scn["months_until_cash_zero_gross"] = np.where(scn.deficit_gross < 0, cash / (-scn.deficit_gross / 12), np.inf)
scn["months_until_cash_zero_net"] = np.where(scn.deficit_net_of_cost_avoidance < 0, cash / (-scn.deficit_net_of_cost_avoidance / 12), np.inf)
for end in ("low", "high"):  # months of cash after a year at each end of the range (net of cost avoidance)
    scn[f"months_of_cash_after_12m_net_{end}"] = (cash + base_deficit - scn[f"revenue_loss_{'high' if end == 'low' else 'low'}"] * (1 - ca)).clip(lower=0) / (expenses / 12)
params = pd.DataFrame([{"parameter": k, "value": v} for k, v in {
    "baseline_fy": fy, "total_revenue": total_rev, "total_expenses": expenses, "baseline_surplus_deficit": base_deficit,
    "cash_eoy": cash, "recognized_gov_revenue": gov_recog, "gov_share": gov_recog / total_rev,
    "alloc_ovsjg": alloc["ovsjg"], "alloc_coc": alloc["coc"], "alloc_dhs": alloc["dhs"], "alloc_other": alloc["other"],
    "nf2_share_of_coc": nf2_share_of_coc, "cost_avoidance_share": ca, "coc_draw_rate_fy22_23_sefa": coc_draw_rate, "sisters_rise_dhs": sisters_rise}.items()])
save_chart_data(scn, "m2_07_scenarios", "Stress-test scenarios on Calvary's FY25 government revenue (config/scenarios.yaml)",
                ["fact_gov_awards", "fact_org_financials"], src_gov, S, "losses as ranges across three apportionments of recognized government revenue (A ceiling share, B CoC at the FY22-23 SEFA draw rate with DHS residual, C ceiling share without Sisters Rise); D floor case reported separately")
save_chart_data(params, "m2_07_scenario_parameters", "Scenario baseline parameters", ["fact_gov_awards", "fact_org_financials"], src_gov, S)
f, ax = style.fig(10.5, 5.6)
s2 = scn[scn.scenario_id != "S0"].iloc[::-1]
bars = ax.barh(s2.scenario, s2.revenue_loss_high - s2.revenue_loss_low, left=s2.revenue_loss_low, color=style.NEGATIVE, height=0.6)
for b_, lo, hi, mlo, mhi in zip(bars, s2.revenue_loss_low, s2.revenue_loss_high, s2.months_of_cash_after_12m_net_low, s2.months_of_cash_after_12m_net_high):
    ax.annotate(f"−${lo/1e3:,.0f}K to −${hi/1e3:,.0f}K ({lo/total_rev:.0%}–{hi/total_rev:.0%} of revenue) → {mlo:.1f}–{mhi:.1f} months of cash after a year (net)",
                (hi, b_.get_y() + b_.get_height() / 2), xytext=(5, 0), textcoords="offset points", va="center", fontsize=8.5, color=style.TEXT_2)
ax.grid(axis="y", visible=False); ax.grid(axis="x", visible=True)
style.money_axis(ax, "K", axis="x"); ax.set_xlim(0, s2.revenue_loss.max() * 1.9)
style.finish(f, ax, "m2_07_scenarios",
             f"Losing the DHS/TCP contract would cost about {money(scn.set_index('scenario_id').loc['S5', 'revenue_loss_low'])}-{money(scn.set_index('scenario_id').loc['S5', 'revenue_loss_high'])} a year, and the combined case leaves {scn.set_index('scenario_id').loc['S6', 'months_of_cash_after_12m_net_low']:.1f}-{scn.set_index('scenario_id').loc['S6', 'months_of_cash_after_12m_net_high']:.1f} months of cash after a year",
             "fact_gov_awards and fact_org_financials; parameters in config/scenarios.yaml",
             note=f"Baseline: FY{str(fy)[2:]} revenue {money(total_rev)}, expenses {money(expenses)}, cash {money(cash)}, government revenue {money(gov_recog)} ({gov_recog/total_rev:.0%}). Net view assumes {ca:.0%} of a lost stream's revenue is avoidable cost. Bars span three ways of splitting recognized revenue across streams (ceiling share; CoC at its audited FY22-23 draw rate of {coc_draw_rate:.0%}; without Sisters Rise); a floor case with OVSJG and CoC fully drawn nearly removes the DHS loss.")

print(al[["fy_label", "ovsjg_award", "coc_award_lagged", "dhs_award", "other_federal", "award_ceiling_known", "recognized_gov_revenue", "recognized_basis", "slfrf_expenditure", "gov_share", "ratio_recognized_ex_slfrf_to_ceiling"]].round(3).to_string())
print(dur[["detail", "first_year", "first_amount", "latest_year", "latest_amount", "change_first_to_latest"]].to_string())
print(bud.pivot_table(index="group", columns=["budget_stage", "fiscal_year"], values="amount").to_string())
print(sh.round(3).to_string())
print(params.to_string())
print(scn[["scenario_id", "scenario", "revenue_loss", "loss_pct_of_total_revenue", "deficit_gross", "deficit_net_of_cost_avoidance", "months_of_cash_after_12m_gross", "months_of_cash_after_12m_net", "months_until_cash_zero_net"]].round(2).to_string())
print(sel[["event_date", "event_type", "agency", "amount_change", "description"]].to_string())

# ------------------------------------------------------------------ insights
r24 = al.set_index("fiscal_year")
register_insight("M2-01", "M2", "Calvary's recurring government awards rose from about $0.6M (2020) to about $4.1M (2024) across three channels: OVSJG, HUD CoC via TCP, and DHS via TCP; about three-quarters (78% of the 2024 base) passes through TCP.",
                 f"OVSJG recurring {money(ovs.get(2020))} FY20 -> {money(ovs.get(2026))} FY26; CoC {money(cocs.get(2020))} (2019 awards) -> {money(cocs.get(2026))} (FY2025 awards); DHS/TCP {money(dhss.get(2024))} in FY2024.",
                 ["m2_01_stream_map", "m2_03_stream_durability"], ["fact_gov_awards"], "$4.1M/yr award base", "high",
                 "Three channels, two pass-through intermediaries (TCP for both CoC and DHS) and one direct grantor: concentration sits in TCP more than in any single program.", "both")
register_insight("M2-02", "M2", f"In FY24-FY25 Calvary recognized only about {r24.loc[2024,'ratio_recognized_ex_slfrf_to_ceiling']:.0%}-{r24.loc[2025,'ratio_recognized_ex_slfrf_to_ceiling']:.0%} of its known award ceilings as revenue.",
                 f"FY24 ceilings {money(r24.loc[2024,'award_ceiling_known'])} vs recognized {money(r24.loc[2024,'recognized_gov_revenue'])}; FY25 {money(r24.loc[2025,'award_ceiling_known'])} vs {money(r24.loc[2025,'recognized_gov_revenue'])}. Line 1e matched audits in FY22-23, so the 990 figure is credible.",
                 ["m2_02_ceilings_vs_recognized"], ["fact_gov_awards", "fact_org_financials"], "$1-1.4M/yr gap", "medium",
                 "Either awards are drawn below ceiling (utilization, timing, cost-reimbursement limits) or the DHS carry-forward assumption overstates FY25; both are worth asking Calvary, because undrawn awards are the cheapest revenue to recover.", "both")
register_insight("M2-03", "M2", "DC's budgets behind Calvary's local streams stayed flat to rising through FY2027, but the Mayor proposed cuts to victim services and DV lines in both FY2026 and FY2027 and the Council restored them.",
                 "OVSJG Victim Services grants approved $45.5M FY24, $55.9M FY25, $55.4M FY26, $55.3M FY27; Mayor's FY26 proposal $50.1M; DHS continuum $170M FY24 -> $206M FY26; PSH ~$145-166M.",
                 ["m2_04_dc_budget_context", "m2_06_policy_timeline"], ["supp_dc_budget_lines", "fact_policy_events"], "flat pools, annual threat", "high",
                 "The local risk is annual and political rather than structural: the line has held through Council restorations, the FY27 restoration is mostly one-time ($5.1M of $5.6M), and actual spending runs 9-14% under approved.", "both")
register_insight("M2-04", "M2", "Calvary receives about 5% of DC's CoC awards and about 1% of OVSJG's awards.",
                 f"CoC share {sh.set_index('fiscal_year').coc_share.get(2025):.1%} (FY2025, $1.77M of $33.5M); OVSJG share {sh.set_index('fiscal_year').ovsjg_share.get(2026):.1%} (FY2026, $1.05M of $96.7M).",
                 ["m2_05_pool_shares"], ["fact_gov_awards"], "5% and 1% of pools", "high",
                 "Calvary is a price-taker in both pools; growth comes from winning projects in competitions it does not control, not from pool growth.", "both")
s5 = scn.set_index("scenario_id")
register_insight("M2-05", "M2", f"A non-renewed DHS/TCP contract would remove about {money(s5.loc['S5','revenue_loss_low'])}-{money(s5.loc['S5','revenue_loss_high'])} a year, depending on how recognized revenue splits across streams; the combined worst case removes {money(s5.loc['S6','revenue_loss_low'])}-{money(s5.loc['S6','revenue_loss_high'])} and leaves about {s5.loc['S6','months_of_cash_after_12m_net_low']:.1f}-{s5.loc['S6','months_of_cash_after_12m_net_high']:.1f} months of cash after one year even with 50% cost avoidance.",
                 f"Baseline FY25: revenue {money(total_rev)}, expenses {money(expenses)}, cash {money(cash)}, deficit {money(base_deficit)}. OVSJG -10% costs {money(s5.loc['S1','revenue_loss_low'])}-{money(s5.loc['S1','revenue_loss_high'])}; CoC -15% {money(s5.loc['S3','revenue_loss_low'])}-{money(s5.loc['S3','revenue_loss_high'])}. Ranges span three apportionments (review finding R01).",
                 ["m2_07_scenarios"], ["fact_gov_awards", "fact_org_financials"], f"up to {money(s5.loc['S6','revenue_loss_high'])}/yr", "medium",
                 "The DHS/TCP contract is the single largest exposure and the least documented; the OVSJG cuts that make headlines are survivable, a TCP contract loss is not without new money or cuts.", "both")
register_insight("M2-06", "M2", "Sisters Rise (24 EHV-paired PSH beds in the HIC; DHS contract capacity 25; $593K in FY2024) disappeared from the 2025 Housing Inventory Count.",
                 "supp_hic_projects: 'CWS - Sisters Rise - PSH' 24 beds in 2024, absent in 2025; HUD's 29 September 2026 notice ends the EHV program, with vouchers converting by 31 December 2026.",
                 ["m2_03_stream_durability"], ["supp_hic_projects", "fact_gov_awards"], "$593K stream at risk or gone", "medium",
                 "Confirm with Calvary whether the EHV program ended in FY25; if so, part of the FY25 revenue drop is already this.", "both")
log(S, [f"streams: OVSJG recurring FY26 {ovs.get(2026):,.0f}; CoC FY2025 awards {coc[coc.fiscal_year==2025].amount.sum():,.0f}; DHS FY2024 {dhss.get(2024):,.0f}",
        f"ceilings vs recognized FY24 {r24.loc[2024,'award_ceiling_known']:,.0f} vs {r24.loc[2024,'recognized_gov_revenue']:,.0f}; FY25 {r24.loc[2025,'award_ceiling_known']:,.0f} vs {r24.loc[2025,'recognized_gov_revenue']:,.0f}",
        "scenarios S1-S6 written to chart_data/m2_07_scenarios.csv", "charts m2_01..m2_07 written"])
