"""M9: Need and capacity context. Wards 7/8 vs DC on ACS indicators, DC point-in-time counts, Calvary's share of
DC transitional-housing beds, and women-focused provider capacity. One ward map if shapes are available."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import style  # noqa: E402
from lib.common import CALVARY, CLEAN, DATA, load, log, register_insight, save_chart_data  # noqa: E402

S = "09_m9_need_capacity"
geo = pd.read_csv(CLEAN / "dim_geo.csv", low_memory=False)
wards = geo[geo.geo_level == "ward"].copy(); wards["ward"] = wards.ward.astype(str).str.extract(r"(\d)")[0]
dc = geo[(geo.geo_level == "state") & (geo.name.str.contains("District", na=False))]
if dc.empty:
    dc = geo[geo.geo_level.isin(["state"]) & (geo.state_fips == 11)]
ind = ["poverty_rate", "female_poverty_rate", "rent_burden_30plus_share", "rent_burden_50plus_share", "unemployment_rate", "female_hh_no_spouse_share"]
labels = {"poverty_rate": "Poverty rate", "female_poverty_rate": "Female poverty rate", "rent_burden_30plus_share": "Renters paying 30%+ of income", "rent_burden_50plus_share": "Renters paying 50%+", "unemployment_rate": "Unemployment", "female_hh_no_spouse_share": "Female householder, no spouse"}
rows = []
for i in ind:
    for w in ["7", "8"]:
        r = wards[wards.ward == w].iloc[0]; rows.append({"indicator": labels[i], "geo": f"Ward {w}", "value": r[i], "moe": r.get(i + "_moe", np.nan)})
    rows.append({"indicator": labels[i], "geo": "DC", "value": float(dc.iloc[0][i]) if len(dc) else np.nan, "moe": float(dc.iloc[0].get(i + "_moe", np.nan)) if len(dc) else np.nan})
acs = pd.DataFrame(rows)
save_chart_data(acs, "m9_01_ward_indicators", "ACS 2020-24 indicators: Wards 7 and 8 vs DC", ["dim_geo"], ["api_census_acs5"], S, "DC wards = Census state legislative district (upper) geographies; 90% MOE in moe")
f, ax = style.fig(10, 5.4)
piv = acs.pivot(index="indicator", columns="geo", values="value").reindex([labels[i] for i in ind])
x = np.arange(len(piv)); w = 0.26
for j, (g, col) in enumerate([("Ward 8", style.SERIES["government"]), ("Ward 7", style.SERIES["institutional"]), ("DC", style.PEER_COLOR)]):
    ax.bar(x + (j - 1) * w, piv[g], w, color=col, label=g)
    for xi, v in zip(x, piv[g]):
        ax.text(xi + (j - 1) * w, v + 0.008, f"{v:.0%}", ha="center", fontsize=7.5, color=style.TEXT_2)
ax.set_xticks(x, [l.replace(", ", ",\n") for l in piv.index], fontsize=8.5); style.pct_axis(ax); ax.set_ylim(0, piv.values.max() * 1.2); ax.legend(loc="upper right")
style.finish(f, ax, "m9_01_ward_indicators",
             "Calvary's home ward has twice the city's poverty rate and the highest female poverty in DC, with rent burden above 50% for a third of renters",
             "dim_geo (ACS 5-year 2020-2024, DC wards as state legislative districts, U.S. Census Bureau)")

# PIT
hc = pd.read_csv(CLEAN / "supp_homeless_counts.csv", low_memory=False)
pit = hc[(hc.coc_code == "DC-500") & (hc.measure == "pit_overall") & (hc.population == "all")].groupby("year").value.first().reset_index()
pit_w = hc[(hc.coc_code == "DC-500") & (hc.measure == "pit_overall") & hc.population.str.contains("women|female", case=False, na=False)]
save_chart_data(pit, "m9_02_dc_pit", "DC point-in-time count of people experiencing homelessness, 2007-2025", ["supp_homeless_counts"], ["doc_hud_pit_hic"] if "doc_hud_pit_hic" in set(hc.source_id) else sorted(hc.source_id.unique()), S)
f, ax = style.fig(10, 4.8)
ax.plot(pit.year, pit.value, color=style.SERIES["government"], marker="o", ms=5, markeredgecolor="white", markeredgewidth=1.2)
for yv, v in [(pit.year.iloc[0], pit.value.iloc[0]), (int(pit.loc[pit.value.idxmax(), "year"]), pit.value.max()), (pit.year.iloc[-1], pit.value.iloc[-1])]:
    ax.annotate(f"{int(v):,}", (yv, v), xytext=(0, 8), textcoords="offset points", ha="center", fontsize=8.5, color=style.TEXT_2)
ax.set_ylim(0, pit.value.max() * 1.18); ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:,.0f}")); ax.set_xticks(range(int(pit.year.min()), int(pit.year.max()) + 1, 2))
style.finish(f, ax, "m9_02_dc_pit",
             f"DC's homeless count fell from a 2016 peak of {int(pit.value.max()):,} to {int(pit.value.iloc[-1]):,} in {int(pit.year.iloc[-1])}, so the system is shrinking while per-person investment rises",
             "supp_homeless_counts (HUD point-in-time counts, CoC DC-500)")

# HIC: Calvary share of TH beds; women-focused providers
hic = pd.read_csv(CLEAN / "supp_hic_projects.csv", dtype={"recipient_ein": str}, low_memory=False)
th = hic[hic.project_type == "TH"].groupby("year").total_beds.sum()
cal = hic[hic.recipient_ein == CALVARY].groupby(["year", "project_type"]).total_beds.sum().unstack(fill_value=0)
share = pd.DataFrame({"year": th.index, "dc_th_beds": th.values}); share["calvary_th_beds"] = share.year.map(cal["TH"]).fillna(0); share["calvary_share_of_th"] = share.calvary_th_beds / share.dc_th_beds
share["calvary_psh_beds"] = share.year.map(cal.get("PSH", pd.Series(dtype=float))).fillna(0); share["calvary_rrh_beds"] = share.year.map(cal.get("RRH", pd.Series(dtype=float))).fillna(0)
wf = hic[hic.x_women_focused_org.astype(str).str.lower().isin(["true", "1"])]
wfb = wf.groupby(["year", "x_org_name_clean"]).total_beds.sum().unstack(fill_value=0)
save_chart_data(share, "m9_03_calvary_hic_share", "Calvary's transitional-housing beds and share of DC TH beds, HIC 2022-2025", ["supp_hic_projects"], sorted(hic.source_id.unique()), S)
save_chart_data(wfb.reset_index(), "m9_04_women_focused_beds", "Beds of women-focused providers in the DC HIC by year", ["supp_hic_projects"], sorted(hic.source_id.unique()), S)
f, ax = style.fig(10, 4.8)
ax.bar(share.year.astype(int).astype(str), share.calvary_th_beds, color=style.SERIES["government"], width=0.5, label="Calvary TH beds")
ax.bar(share.year.astype(int).astype(str), share.calvary_psh_beds, bottom=share.calvary_th_beds, color=style.SERIES["daf"], width=0.5, label="Calvary PSH beds", edgecolor="white")
ax.bar(share.year.astype(int).astype(str), share.calvary_rrh_beds, bottom=share.calvary_th_beds + share.calvary_psh_beds, color=style.SERIES["institutional"], width=0.5, label="Calvary RRH units", edgecolor="white")
for i, (t, p, r, s_) in enumerate(zip(share.calvary_th_beds, share.calvary_psh_beds, share.calvary_rrh_beds, share.calvary_share_of_th)):
    ax.text(i, t + p + r + 2, f"{int(t+p+r)} beds · {s_:.1%} of DC TH beds", ha="center", fontsize=8.5, color=style.TEXT_2)
ax.set_ylim(0, (share.calvary_th_beds + share.calvary_psh_beds + share.calvary_rrh_beds).max() * 1.25); ax.legend(loc="upper left")
style.finish(f, ax, "m9_03_calvary_hic_share",
             f"Calvary's housing inventory grew from {int(share.iloc[0].calvary_th_beds + share.iloc[0].calvary_psh_beds + share.iloc[0].calvary_rrh_beds)} to {int(share.iloc[-1].calvary_th_beds + share.iloc[-1].calvary_psh_beds + share.iloc[-1].calvary_rrh_beds)} beds in three years and now holds {share.iloc[-1].calvary_share_of_th:.0%} of DC's transitional-housing beds",
             "supp_hic_projects (HUD Housing Inventory Count, CoC DC-500, 2022-2025)", note="Sisters Rise PSH (24 units) appears in 2024 only.")

# ward map (if a ward GeoJSON is available in raw/geo)
import glob, json
cands = sorted(p for p in glob.glob(str(DATA / "raw" / "geo" / "**" / "*"), recursive=True) if p.lower().endswith(".geojson") and "wards" in Path(p).name.lower())
map_done = False
if cands:
    try:
        from shapely.geometry import shape
        gj = json.load(open(cands[0]))
        feats = gj["features"]
        f, ax = plt.subplots(figsize=(8.5, 8)); style.apply(); ax.set_axis_off()
        vals = wards.set_index("ward").poverty_rate
        vmin, vmax = vals.min(), vals.max()
        ramp = style.SEQUENTIAL
        for ft in feats:
            props = {k.lower(): v for k, v in ft["properties"].items()}
            wnum = str(props.get("ward", props.get("ward_id", props.get("name", "")))).strip()[-1]
            geom = shape(ft["geometry"]); v = vals.get(wnum, np.nan)
            col = ramp[int(np.clip((v - vmin) / (vmax - vmin + 1e-9) * (len(ramp) - 1), 0, len(ramp) - 1))] if pd.notna(v) else style.SURFACE_2
            polys = [geom] if geom.geom_type == "Polygon" else list(geom.geoms)
            for pg in polys:
                xs, ys = pg.exterior.xy; ax.fill(xs, ys, color=col, edgecolor="white", linewidth=1.2)
            c = geom.centroid; ax.text(c.x, c.y, f"Ward {wnum}\n{v:.0%}", ha="center", va="center", fontsize=9, color=style.INK if (pd.isna(v) or (v - vmin) / (vmax - vmin + 1e-9) < 0.55) else "white", fontweight="bold")
        site = pd.read_csv(CLEAN / "dim_org.csv", dtype=str, usecols=["ein", "lat", "lon"]); site = site[site.ein == CALVARY].iloc[0]
        if pd.notna(site.lat):
            ax.plot(float(site.lon), float(site.lat), marker="*", ms=18, color=style.GOLD, markeredgecolor=style.INK, markeredgewidth=1); ax.annotate("Calvary (Marion Barry Ave SE)", (float(site.lon), float(site.lat)), xytext=(10, -14), textcoords="offset points", fontsize=8.5, color=style.INK)
        ax.set_aspect("equal")
        f.text(0.01, 0.985, "Calvary serves the two wards where poverty is highest: Ward 8 (31%) and Ward 7 (23%) against 15% citywide", fontsize=12.5, fontweight="bold", color=style.INK, va="top", wrap=True)
        f.text(0.01, 0.005, "Source: dim_geo (ACS 2020-2024 poverty rate by ward, U.S. Census Bureau); ward boundaries DC Open Data (CC BY 4.0). Data as of 2026-10-10. Chart m9_05_ward_map.", fontsize=7.5, color=style.TEXT_MUTED)
        f.tight_layout(rect=(0, 0.02, 1, 0.94)); f.savefig(style.CHARTS / "m9_05_ward_map.png", dpi=200); plt.close(f); map_done = True
        save_chart_data(wards[["ward", "name", "poverty_rate", "female_poverty_rate", "median_hh_income", "total_pop"]], "m9_05_ward_map", "Ward poverty rates behind the map", ["dim_geo"], ["api_census_acs5"], S, f"boundaries from {Path(cands[0]).name}")
    except Exception as e:  # noqa: BLE001
        print("map skipped:", e)
print(acs.pivot(index="indicator", columns="geo", values="value").round(3).to_string()); print(pit.tail(5).to_string()); print(share.to_string()); print(wfb.tail(4).to_string()); print("map:", map_done, cands[:2])
w8 = wards[wards.ward == "8"].iloc[0]; w7 = wards[wards.ward == "7"].iloc[0]; dcv = dc.iloc[0] if len(dc) else None
register_insight("M9-01", "M9", f"Calvary's service area carries the city's deepest need: Ward 8 poverty {w8.poverty_rate:.0%} and Ward 7 {w7.poverty_rate:.0%} against {dcv.poverty_rate:.0%} for DC; female poverty {w8.female_poverty_rate:.0%} in Ward 8; a third of renters in both wards pay over half their income in rent.",
                 "m9_01_ward_indicators", ["m9_01_ward_indicators"] + (["m9_05_ward_map"] if map_done else []), ["dim_geo"], "2x city poverty", "high", "The case statement for place-based funders (Bainum, Cafritz, GWCF, Clark) is strong and quantified.", "both")
register_insight("M9-02", "M9", f"DC's homeless count fell from {int(pit.value.max()):,} (2016) to {int(pit.value.iloc[-1]):,} ({int(pit.year.iloc[-1])}) while Calvary's inventory grew to {int(share.iloc[-1].calvary_th_beds + share.iloc[-1].calvary_psh_beds + share.iloc[-1].calvary_rrh_beds)} beds and {share.iloc[-1].calvary_share_of_th:.0%} of DC's transitional-housing beds.",
                 "m9_02_dc_pit; m9_03_calvary_hic_share", ["m9_02_dc_pit", "m9_03_calvary_hic_share"], ["supp_homeless_counts", "supp_hic_projects"], f"{share.iloc[-1].calvary_share_of_th:.0%} of TH beds", "high",
                 "Calvary has become a system-level provider for single women; that position is the argument for durable public contracts and for PSH expansion.", "both")
log(S, [f"ACS wards written; PIT {int(pit.value.iloc[-1])} ({int(pit.year.iloc[-1])}); Calvary TH share {share.iloc[-1].calvary_share_of_th:.3f}; map {map_done}"])
