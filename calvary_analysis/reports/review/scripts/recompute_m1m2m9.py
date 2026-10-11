"""Independent recomputation of M1/M2/M9 figures shown in the executive one-pager and
leadership deck, from calvary_funding_data/clean/ only.

Run:  <venv>/bin/python recompute_m1m2m9.py
ROOT is the project root; all data paths are relative to it. OUT is where results go.
"""
# Review script. Paths resolve from this file: calvary_analysis/reports/review/scripts/ -> project root three levels up.
import os as _os, pathlib as _pl
_HERE = _pl.Path(__file__).resolve().parent
PROJECT_ROOT = str(_pl.Path(_os.environ.get("CALVARY_ROOT", _HERE.parents[3])))
REVIEW_OUT = _os.environ.get("REVIEW_OUT", str(_HERE.parent / "evidence"))
import os, sys, math
import pandas as pd
import numpy as np

ROOT = PROJECT_ROOT
CLEAN = os.path.join(ROOT, "calvary_funding_data", "clean")
OUT = os.environ.get("RECOMPUTE_OUT", os.path.dirname(os.path.abspath(__file__)))
EIN = "521307706"

def rd(name, **kw):
    return pd.read_csv(os.path.join(CLEAN, name), low_memory=False, **kw)

rows = []
def add(item, label, shown, rec, nd=None, notes="", unit=""):
    """shown: value as displayed (number or str). rec: recomputed numeric (or str).
    nd: decimals at which 'shown' is displayed; match = exact if |rec-shown| tiny,
    rounding if round(rec, nd) == shown, else MISMATCH. Pass match explicitly via nd='manual:<match>'."""
    if isinstance(nd, str) and nd.startswith("manual:"):
        match = nd.split(":", 1)[1]
    elif isinstance(shown, str) or rec is None or (isinstance(rec, float) and math.isnan(rec)):
        match = "n/a"
    else:
        if abs(float(rec) - float(shown)) < 1e-6:
            match = "exact"
        elif nd is not None and round(float(rec), nd) == round(float(shown), nd):
            match = "rounding"
        elif nd is not None and abs(float(rec) - float(shown)) <= 0.5 * 10 ** (-nd) + 1e-9:
            # within half a unit of the last displayed digit (e.g. 2.954 shown as 3.0)
            match = "rounding"
        else:
            match = "MISMATCH"
    rows.append(dict(item=item, label=label, as_shown=shown, recomputed=rec, unit=unit, match=match, notes=notes))

# ---------------------------------------------------------------- load
fin = rd("fact_org_financials.csv", dtype={"ein": str})
cal = fin[fin.ein == EIN].copy()
pref = cal[cal.preferred == 1].set_index("fiscal_year")
aud = cal[cal.return_type == "audit"].set_index("fiscal_year")
assert aud.index.is_unique
per = rd("dim_period.csv").set_index("year")
defl = per["deflator_to_2024_us"]

gov = rd("fact_gov_awards.csv", dtype={"recipient_ein": str, "pass_through_ein": str})
cg = gov[gov.recipient_ein == EIN].copy()

# ================================================================ A. trajectory
rev = pref["total_revenue"]
add("A01", "Nominal revenue FY11", 1445107, rev[2011], 0, "preferred 990 row")
add("A02", "Nominal revenue FY19 ($M)", 2.49, rev[2019] / 1e6, 2, f"preferred 990 row = {rev[2019]:,.0f}")
add("A03", "Nominal revenue FY25 ($M)", 4.97, rev[2025] / 1e6, 2, f"preferred 990 row = {rev[2025]:,.0f}")
real19 = rev[2019] * defl[2019]; real25 = rev[2025] * defl[2025]
add("A04", "Real revenue growth FY19->FY25 (%)", 59, 100 * (real25 / real19 - 1), 0,
    f"FY19 {rev[2019]:,.0f} x {defl[2019]:.6f} = {real19:,.0f}; FY25 {rev[2025]:,.0f} x {defl[2025]:.6f} = {real25:,.0f}; deflator by fiscal-year-end year")
add("A05", "Slide 3 / one-pager label '$2.49M -> $4.97M, 2024 dollars'", "2.49 -> 4.97 (2024 $)",
    f"{real19/1e6:.2f} -> {real25/1e6:.2f} (2024 $); 2.49 -> 4.97 are nominal", "manual:MISMATCH",
    "The two dollar figures printed next to '+59%' are nominal, but the slide and one-pager label them 2024 dollars. The growth rate itself is right.")
add("A06", "FY22 revenue ($M)", 8.87, rev[2022] / 1e6, 2, f"{rev[2022]:,.0f}; deck says 'FY22 spike' without a revenue figure")
slfrf = cg[(cg.amount == 3680675)]
add("A07", "SLFRF award 3,680,675 present in fact_gov_awards", 3680675, 3680675 if len(slfrf) else None, 0,
    "rows: " + "; ".join(f"{r.source_type}/{r.award_id or r.program_name[:30]}/{int(r.fiscal_year)}" for r in slfrf.itertuples()) +
    ". Appears as dc_ovsjg OVSJG-L35-1059 (New Foundations building purchase, DC FY2022), as dc_pass obligation PO660852-V2 and as treasury_slfrf subaward 12126; same dollars in three sources")
for fy, shown in [(2023, -674), (2024, 507), (2025, -607)]:
    s = rev[fy] - pref.loc[fy, "total_expenses"]
    add(f"A08.{fy}", f"FY{fy-2000} surplus/deficit ($K)", shown, s / 1e3, 0, f"{rev[fy]:,.0f} - {pref.loc[fy,'total_expenses']:,.0f} = {s:,.0f}")
for fy, shown in zip(range(2020, 2026), [6.3, 7.5, 6.3, 5.0, 5.2, 4.4]):
    m = pref.loc[fy, "cash_savings_eoy"] / (pref.loc[fy, "total_expenses"] / 12)
    add(f"A09.{fy}", f"Months of cash FY{fy-2000}", shown, m, 1, f"{pref.loc[fy,'cash_savings_eoy']:,.0f} / ({pref.loc[fy,'total_expenses']:,.0f}/12)")
for fy, shown in [(2023, 458), (2024, 538), (2025, 55)]:
    add(f"A10.{fy}", f"Event contributions line 1c FY{fy-2000} ($K)", shown, pref.loc[fy, "fundraising_event_contributions"] / 1e3, 0)
add("A11", "Net special events line 8c FY25 ($K)", 219, pref.loc[2025, "special_events_net"] / 1e3, 0)
add("A12", "Event-income drop FY24->FY25 ($K)", 483, (pref.loc[2024, "fundraising_event_contributions"] - pref.loc[2025, "fundraising_event_contributions"]) / 1e3, 0, "line 1c difference")
add("A13a", "Contributions total FY24 ($M)", 5.55, pref.loc[2024, "contributions_total"] / 1e6, 2)
add("A13b", "Contributions total FY25 ($M)", 4.75, pref.loc[2025, "contributions_total"] / 1e6, 2)
add("A14", "Net assets FY25 ($M)", 8.1, pref.loc[2025, "net_assets_eoy"] / 1e6, 1)

# government share by year
shown_share = dict(zip(range(2015, 2026), [41, 44, 40, 42, 49, 55, 50, 61, 51, 45, 58]))
share_audit, share_990den, share_990both = {}, {}, {}
for fy in range(2015, 2026):
    if fy <= 2023:
        g = aud.loc[fy, "government_grants"]; den_a = aud.loc[fy, "total_revenue"]
        basis = "audit"
    else:
        g = pref.loc[fy, "government_grants"]; den_a = pref.loc[fy, "total_revenue"]
        basis = "990 line 1e"
    share_audit[fy] = 100 * g / den_a
    share_990den[fy] = 100 * g / pref.loc[fy, "total_revenue"]
    g990 = pref.loc[fy, "government_grants"]
    share_990both[fy] = 100 * g990 / pref.loc[fy, "total_revenue"] if pd.notna(g990) else np.nan
    add(f"A15.{fy}", f"Government share FY{fy-2000} (%)", shown_share[fy], share_audit[fy], 0,
        f"{basis}: gov {g:,.0f} / {basis} revenue {den_a:,.0f}; same gov / 990 revenue {pref.loc[fy,'total_revenue']:,.0f} = {share_990den[fy]:.1f}%; 990 1e / 990 revenue = {share_990both[fy]:.1f}%")
mean_a = np.mean([share_audit[y] for y in (2022, 2023, 2024)])
mean_b = np.mean([share_990den[y] for y in (2022, 2023, 2024)])
add("A16", "Mean government share FY22-24 (%)", 53, mean_a, 0, f"audit basis mean {mean_a:.2f}; with 990 revenue denominators {mean_b:.2f}")
lo, hi = min(share_audit.values()), max(share_audit.values())
lo2, hi2 = min(share_990den.values()), max(share_990den.values())
add("A17", "'Every year since FY15 between 40% and 61%'", "40-61", f"{lo:.1f}-{hi:.1f} (audit basis); {lo2:.1f}-{hi2:.1f} with 990 revenue denominator",
    "manual:rounding" if round(lo) >= 40 and round(hi) <= 61 else "manual:MISMATCH",
    f"FY17 is {lo:.1f}% on the audit basis (rounds to 40); FY22 is {hi:.1f}%. On the 990-revenue denominator FY22 would be {hi2:.1f}%")

# slide 4 chart table (private contributions ex events; other revenue)
slide4 = {2015: (907544, 0), 2016: (836710, 0), 2017: (1071475, 0), 2018: (992376, 0), 2019: (973806, 0),
          2020: (1582461, 0), 2021: (1601560, 0), 2022: (2885189, 0), 2023: (1684754, 0), 2024: (2392856, 265038), 2025: (1799806, 220861)}
slide4_gov = {2015: 888295, 2016: 932814, 2017: 965548, 2018: 979272, 2019: 1256102, 2020: 2166119, 2021: 1981161, 2022: 5685504, 2023: 2460897, 2024: 2621203, 2025: 2892598}
slide4_evt = {2015: 287580, 2016: 301790, 2017: 301899, 2018: 279265, 2019: 331837, 2020: 165497, 2021: 287145, 2022: 383731, 2023: 457758, 2024: 538070, 2025: 54730}
for fy in range(2015, 2026):
    g = aud.loc[fy, "government_grants"] if fy <= 2023 else pref.loc[fy, "government_grants"]
    evt = pref.loc[fy, "fundraising_event_contributions"]
    priv = pref.loc[fy, "contributions_total"] - g - evt
    other = pref.loc[fy, "total_revenue"] - pref.loc[fy, "contributions_total"]
    add(f"A18.{fy}", f"Slide 4 chart FY{fy-2000}: government", slide4_gov[fy], g, 0, "audit gov FY15-23, 990 1e FY24-25")
    add(f"A19.{fy}", f"Slide 4 chart FY{fy-2000}: event contributions", slide4_evt[fy], evt, 0, "990 line 1c")
    add(f"A20.{fy}", f"Slide 4 chart FY{fy-2000}: private contributions ex events", slide4[fy][0], priv, 0,
        f"990 contributions_total {pref.loc[fy,'contributions_total']:,.0f} - gov - line 1c")
    add(f"A21.{fy}", f"Slide 4 chart FY{fy-2000}: other revenue", slide4[fy][1], max(other, 0), 0,
        f"total_revenue - contributions_total = {other:,.0f}" + ("; negative (net event loss) shown as 0, so the chart's four categories sum to more than total revenue" if other < 0 else ""))

# ================================================================ C. streams
ovsjg = cg[cg.source_type == "dc_ovsjg"]
coc = cg[cg.source_type == "hud_coc"]
dhs = cg[cg.source_type == "dc_oversight"]
sefa = cg[cg.source_type == "audit_sefa"]
one_time_ids = {"OVSJG-L35-1059"}  # SLFRF building purchase
ovsjg_rec = ovsjg[~ovsjg.award_id.isin(one_time_ids)]
small_fed = sefa[sefa.assistance_listing.isin(["97.024", "10.561"])]  # EFSP, SNAP E&T

ov_y = ovsjg_rec.groupby("fiscal_year").amount.sum()
coc_y = coc.groupby("fiscal_year").amount.sum()
dhs_y = dhs.groupby("fiscal_year").amount.sum()
oth_y = small_fed.groupby("fiscal_year").amount.sum()
slide5 = {2019: (660935, 239659, 0, 0), 2020: (368935, 248131, 0, 0), 2021: (368935, 1472398, 0, 0), 2022: (468435, 672065, 0, 68003),
          2023: (841040, 1151540, 0, 106673), 2024: (913401, 1761352, 1423664, 0), 2025: (998278, 1766814, 0, 0), 2026: (1050651, 0, 0, 0)}
for y, (a, b, c, d) in slide5.items():
    add(f"C01.{y}", f"Stream map {y}: OVSJG", a, ov_y.get(y, 0), 0, "dc_ovsjg, DC FY, excl. OVSJG-L35-1059 (SLFRF building purchase)")
    add(f"C02.{y}", f"Stream map {y}: HUD CoC via TCP", b, coc_y.get(y, 0), 0, "hud_coc by competition year")
    add(f"C03.{y}", f"Stream map {y}: DHS via TCP", c, dhs_y.get(y, 0), 0, "dc_oversight, DC FY2024 only")
    add(f"C04.{y}", f"Stream map {y}: other federal pass-through", d, oth_y.get(y, 0), 0, "audit_sefa EFSP 97.024 + SNAP E&T 10.561")
# 2019 OVSJG duplicate question
o19 = ovsjg[ovsjg.fiscal_year == 2019]
dcpass = cg[cg.source_type == "dc_pass"]
ob19 = dcpass[(dcpass.fiscal_year == 2019) & (dcpass.amount_type == "obligation")].amount.sum()
ob20 = dcpass[(dcpass.fiscal_year == 2020) & (dcpass.amount_type == "obligation") & (dcpass.program_name.astype(str).str.contains("OVSJG"))].amount.sum()
all_ov = gov[gov.source_type == "dc_ovsjg"].copy()
all_ov["num"] = all_ov.award_id.astype(str).str.extract(r"L35-(\d+)").astype(float)
rng = all_ov.dropna(subset=["num"]).groupby("fiscal_year").num.agg(["min", "max", "count"])
add("C05", "OVSJG 2019 = sum of two Reach Up rows (660,935)?", 660935, o19.amount.sum(), 0,
    "Two rows with different grant numbers: " + "; ".join(f"{r.award_id} {r.amount:,.0f} ('{str(r.notes).split('purpose_text=')[1][:40]}...')" for r in o19.itertuples()) +
    f". Grant-number ranges per DC FY in the OVSJG layer: " + "; ".join(f"{int(y)}: L35-{int(r['min'])}..{int(r['max'])} (n={int(r['count'])})" for y, r in rng.iterrows()) +
    f". L35-556 sits below every other FY2019 number and the FY2020 Reach Up grant is 368,935 with the same text, so L35-556 looks like the FY2018 cycle filed under 2019. DC spending data (dc_pass) shows OVSJG obligations of {ob19:,.0f} in FY2019 and {ob20:,.0f} in FY2020. Summing to 660,935 is very likely a double count; the 2019 OVSJG bar is overstated by roughly 290-370K. Judgment call, flagged as MISMATCH-in-method rather than arithmetic.")
rows[-1]["match"] = "MISMATCH"

base24 = ov_y[2024] + coc_y[2024] + dhs_y[2024] + oth_y.get(2024, 0)
add("C06", "'$4.1M award base' (2024 column of the stream map, $M)", 4.1, base24 / 1e6, 1,
    f"OVSJG FY2024 {ov_y[2024]:,.0f} + CoC 2024 {coc_y[2024]:,.0f} + DHS FY2024 {dhs_y[2024]:,.0f} + other 0 = {base24:,.0f}")
tcp24 = 100 * (coc_y[2024] + dhs_y[2024]) / base24
# FY25-aligned ceiling base
oth_carry = oth_y[2023]
ceil25 = ov_y[2025] + coc_y[2024] + dhs_y[2024] + oth_carry
ceil24 = ov_y[2024] + coc_y[2023] + dhs_y[2024] + oth_carry
tcp25 = 100 * (coc_y[2024] + dhs_y[2024]) / ceil25
add("C07", "TCP share of the base (%)", 74, tcp25, 0,
    f"(CoC + DHS) / 2024 stream-map base {base24:,.0f} = {tcp24:.1f}%; (CoC + DHS) / FY25-aligned ceiling base {ceil25:,.0f} = {tcp25:.1f}%. 74% comes from the FY25 ceiling base, which includes 106,673 of carried-forward other federal and FY25 OVSJG; the $4.1M quoted beside it is the 2024 base, where TCP is {tcp24:.0f}%. Slide 5 and the one-pager pair the 74% with the $4.1M.")
rows[-1]["match"] = "MISMATCH"
rows[-1]["as_shown"] = "74 (of $4.1M)"
n_proj = coc[coc.fiscal_year.isin([2023, 2024, 2025])].program_name.str.replace("Continuum of Care Program: ", "").str.replace("Calvary Women's Services - ", "").nunique()
add("C08", "CoC 'three projects' (distinct project names, 2023-25)", 3, n_proj, 0, "Sister Circle (PSH), Reach Up (Joint TH-RRH), New Foundations 2 (Joint TH-RRH)")
add("C09a", "CoC 2019 ($M)", 0.24, coc_y[2019] / 1e6, 2)
add("C09b", "CoC 2025 ($M)", 1.77, coc_y[2025] / 1e6, 2)
add("C10a", "OVSJG FY20 ($M)", 0.37, ov_y[2020] / 1e6, 2)
add("C10b", "OVSJG FY26 ($M)", 1.05, ov_y[2026] / 1e6, 2)
add("C11a", "DHS FY2024 transitional housing ($K)", 830, dhs[dhs.program_name.str.contains("Transitional")].amount.sum() / 1e3, 0)
add("C11b", "DHS FY2024 Sisters Rise ($K)", 593, dhs[dhs.program_name.str.contains("Sisters Rise")].amount.sum() / 1e3, 0)
add("C11c", "DHS FY2024 total ($M)", 1.42, dhs_y[2024] / 1e6, 2)

# ================================================================ D. ceilings vs recognized
g24 = pref.loc[2024, "government_grants"]; g25 = pref.loc[2025, "government_grants"]
add("D01", "FY24 ceiling", 3595278, ceil24, 0,
    f"OVSJG FY2024 {ov_y[2024]:,.0f} + CoC competition 2023 {coc_y[2023]:,.0f} + DHS FY2024 {dhs_y[2024]:,.0f} + other federal {oth_carry:,.0f} (= FY23 audit SEFA EFSP 67,684 + SNAP E&T 38,989, carried forward)")
add("D02", "FY25 ceiling", 4289967, ceil25, 0,
    f"OVSJG FY2025 {ov_y[2025]:,.0f} + CoC competition 2024 {coc_y[2024]:,.0f} + DHS FY2024 carried {dhs_y[2024]:,.0f} + other federal {oth_carry:,.0f} carried from FY23 SEFA")
add("D03", "FY24 recognized / ceiling (%)", 73, 100 * g24 / ceil24, 0, f"{g24:,.0f} / {ceil24:,.0f}")
add("D04", "FY25 recognized / ceiling (%)", 67, 100 * g25 / ceil25, 0, f"{g25:,.0f} / {ceil25:,.0f}")
add("D05", "FY25 ratio with DHS excluded (%)", "not shown", 100 * g25 / (ceil25 - dhs_y[2024]), "manual:not_shown", f"{g25:,.0f} / {ceil25 - dhs_y[2024]:,.0f}: recognized revenue exceeds the non-DHS ceilings, so the FY25 990 figure implies DHS money is in line 1e")
add("D06", "FY25 ratio with Sisters Rise (593,280) excluded (%)", "not shown", 100 * g25 / (ceil25 - 593280), "manual:not_shown", f"{g25:,.0f} / {ceil25 - 593280:,.0f}")
add("D07", "FY24 ratio with Sisters Rise excluded (%)", "not shown", 100 * g24 / (ceil24 - 593280), "manual:not_shown", f"{g24:,.0f} / {ceil24 - 593280:,.0f}")
add("D08", "FY24 ratio with DHS excluded (%)", "not shown", 100 * g24 / (ceil24 - dhs_y[2024]), "manual:not_shown")
add("D09", "Other federal in FY24/FY25 ceilings vs stream map", "ceiling uses 106,673; slide 5 shows 0 for 2024-25", "same rows", "manual:MISMATCH",
    "The ceiling (slide 11) carries the FY23 SEFA small pass-throughs into FY24 and FY25; the stream map (slide 5) shows 0 for 2024 and 2025 and its 2024 base excludes them. Internally inconsistent carry-forward rule between the two slides (effect: 106,673, about 2.5% of the ceiling).")

# ================================================================ E. scenarios
import yaml
scn = yaml.safe_load(open(os.path.join(ROOT, "calvary_analysis", "config", "scenarios.yaml")))
cas = scn["cost_avoidance_share"]
R = rev[2025]; X = pref.loc[2025, "total_expenses"]; CASH = pref.loc[2025, "cash_savings_eoy"]; GOV = g25
add("E01", "Baseline FY25 revenue", 4967995, R, 0)
add("E02", "Baseline FY25 expenses ($M)", 5.58, X / 1e6, 2, f"{X:,.0f}")
add("E03", "Baseline FY25 cash", 2063796, CASH, 0)
D0 = R - X
add("E04", "Baseline deficit ($K)", -607, D0 / 1e3, 0)
add("E05", "Baseline monthly burn ('about $50K a month', $K)", 50, -D0 / 12 / 1e3, "manual:rounding", "deficit / 12 = 50.6K; deck says 'about $50K'")
shares = {"ovsjg": ov_y[2025] / ceil25, "coc": coc_y[2024] / ceil25, "dhs": dhs_y[2024] / ceil25, "other": oth_carry / ceil25}
app = {k: v * GOV for k, v in shares.items()}
nf2_share = coc[(coc.fiscal_year == 2024) & coc.program_name.str.contains("New Foundations 2")].amount.sum() / coc_y[2024]
app["coc_project_new_foundations_2"] = app["coc"] * nf2_share
for k in ["ovsjg", "coc", "dhs", "other"]:
    add(f"E06.{k}", f"FY25 government revenue apportioned to {k}", "not shown", round(app[k]), "manual:not_shown", f"share of FY25 ceiling {shares[k]:.4f} x {GOV:,.0f}")
mexp = X / 12
cash_after_12_base = CASH + 12 * (D0 / 12)
add("E07", "Baseline months of cash after 12 months", 3.1, cash_after_12_base / mexp, 1,
    f"(cash {CASH:,.0f} + deficit {D0:,.0f}) / (expenses/12 = {mexp:,.0f})")
add("E08", "Baseline months to zero cash", 41, CASH / (-D0 / 12), 0, "cash / monthly deficit")
shown_s = {"S1": (67, 1, -675, 3.1), "S2": (168, 3, -776, 3.0), "S3": (178, 4, -785, 2.9), "S4": (366, 7, -973, 2.7), "S5": (960, 19, -1567, 2.1), "S6": (1306, 26, -1914, 1.7)}
for s in scn["scenarios"]:
    sid = s["id"]; loss = sum(app[k] * v for k, v in s["cuts"].items())
    gross = D0 - loss
    net = D0 - loss * (1 - cas)
    m_gross = (CASH + gross) / mexp
    m_net = (CASH + net) / mexp
    m_net_alt = (CASH + net) / ((X - loss * cas) / 12)
    sl, sp, sg, sm = shown_s[sid]
    add(f"E09.{sid}a", f"{sid} revenue loss ($K)", sl, loss / 1e3, 0, s["name"])
    add(f"E09.{sid}b", f"{sid} % of revenue", sp, 100 * loss / R, 0)
    add(f"E09.{sid}c", f"{sid} gross deficit ($K)", sg, gross / 1e3, 0, "baseline deficit - loss")
    add(f"E09.{sid}d", f"{sid} net deficit at 50% cost avoidance ($K)", "not shown", round(net / 1e3), "manual:not_shown", "baseline deficit - loss x (1 - 0.5)")
    add(f"E09.{sid}e", f"{sid} months of cash after 12 months (net)", sm, m_net, 1,
        f"(cash + net deficit) / (FY25 expenses / 12) = {m_net:.2f}; gross version = {m_gross:.2f}; alternative dividing by expenses net of avoided cost = {m_net_alt:.2f}")

# ================================================================ B. filed grants
parts = []
for ch in pd.read_csv(os.path.join(CLEAN, "fact_grants.csv"), dtype=str, chunksize=250000, low_memory=False):
    parts.append(ch[ch.recipient_ein == EIN])
gr = pd.concat(parts)
gr["amount"] = pd.to_numeric(gr.amount, errors="coerce"); gr["tax_year"] = pd.to_numeric(gr.tax_year, errors="coerce")
filed = gr[gr.source_type.isin(["pf_grants_paid", "schedule_i"]) & (gr.cumulative_flag == "0") & gr.tax_year.between(2020, 2024)].copy()
dfun = rd("dim_funder.csv", dtype=str)
filed = filed.merge(dfun[["funder_id", "funder_name", "funder_type"]], on="funder_id", how="left")
byf = filed.groupby(["funder_id", "funder_type"]).amount.sum().reset_index().sort_values("amount", ascending=False)
tot = byf.amount.sum()
daf = byf[byf.funder_type == "daf_sponsor"].amount.sum(); inst = tot - daf
add("B01", "Filed grants TY2020-24 total ($M)", 4.43, tot / 1e6, 2, f"{tot:,.0f}; {len(filed)} rows; pf_grants_paid + schedule_i, cumulative_flag 0")
add("B02", "Funder count", 50, byf.funder_id.nunique(), 0)
add("B03", "Institutional ($M)", 3.34, inst / 1e6, 2, f"{inst:,.0f}; {byf[byf.funder_type!='daf_sponsor'].funder_id.nunique()} funders")
add("B04", "DAF sponsors ($M)", 1.09, daf / 1e6, 2, f"{daf:,.0f}; {byf[byf.funder_type=='daf_sponsor'].funder_id.nunique()} sponsors")
add("B05", "Calvary DAF share of filed grants (%)", 25, 100 * daf / tot, 0)
yr_all = filed.groupby("tax_year").agg(total=("amount", "sum"), n=("funder_id", "nunique"))
yr_inst = filed[filed.funder_type != "daf_sponsor"].groupby("tax_year").agg(total=("amount", "sum"), n=("funder_id", "nunique"))
add("B06", "By-year range, all funders ('$0.64-1.17M a year from 26-29 funders')", "0.64-1.17M / 26-29",
    f"{yr_all.total.min()/1e6:.2f}-{yr_all.total.max()/1e6:.2f}M / {yr_all.n.min()}-{yr_all.n.max()}", "manual:exact",
    "by year: " + "; ".join(f"TY{int(y)} {r.total/1e6:.2f}M n={int(r.n)}" for y, r in yr_all.iterrows()))
add("B07", "By-year range, institutional only", "not shown", f"{yr_inst.total.min()/1e6:.2f}-{yr_inst.total.max()/1e6:.2f}M / {yr_inst.n.min()}-{yr_inst.n.max()}", "manual:not_shown",
    "by year: " + "; ".join(f"TY{int(y)} {r.total/1e6:.2f}M n={int(r.n)}" for y, r in yr_inst.iterrows()) + ". The slide's 'steady near $1M' claim uses the all-funders version (which includes DAF sponsors).")
gw = byf[byf.funder_id == "237343119"].amount.sum()
add("B08", "GWCF five-year total", 1206500, gw, 0, "funder_id 237343119; two non-cumulative rows in TY2021 (distinct grants in one filing)")
add("B09", "GWCF share (%)", 27, 100 * gw / tot, 0)
top5 = byf.amount.head(5).sum()
add("B10", "Top-five share (%)", 63, 100 * top5 / tot, 0, f"top five = {top5:,.0f}")
hhi = ((byf.amount / tot) ** 2).sum() * 10000
add("B11", "HHI", 1168, hhi, 0, "sum of squared funder shares x 10,000 over 50 funders")
slide6 = {"530234290": 89549, "362169124": 91500, "421559999": 100000, "311640316": 128155, "521435573": 295000, "110303001": 314317, "352599437": 330000, "526036989": 450000, "810739440": 511616, "237343119": 1206500}
top10 = byf.head(10).set_index("funder_id").amount
for fid, shown in slide6.items():
    add(f"B12.{fid}", f"Slide 6 bar, funder_id {fid}", shown, top10.get(fid, np.nan), 0, "in recomputed top 10" if fid in top10.index else "NOT in recomputed top 10")
add("B13", "Benevity / AOGF ($K)", 512, byf[byf.funder_id == "810739440"].amount.sum() / 1e3, 0)
add("B14", "Fidelity ($K)", 314, byf[byf.funder_id == "110303001"].amount.sum() / 1e3, 0)
add("B15", "Schwab ($K)", 128, byf[byf.funder_id == "311640316"].amount.sum() / 1e3, 0)
three = byf[byf.funder_id.isin(["810739440", "110303001", "311640316"])].amount.sum()
add("B16", "'Donor-advised sponsors (Benevity, Fidelity, Schwab) add $1.1M' ($M)", 1.1, three / 1e6, 1,
    f"the three named sum to {three:,.0f} = $0.95M; all eight DAF sponsors sum to {daf:,.0f} = $1.09M. The $1.1M is the all-DAF total; read literally (three named sponsors) it is 15% high. Labeling, not arithmetic.")
rev5 = sum(rev[y] for y in range(2020, 2025))
add("B17", "Slide 14: institutional grants / 990 revenue FY2020-24 (%)", 12, 100 * inst / rev5, 0, f"{inst:,.0f} / {rev5:,.0f}; slide 14 chart value 0.1242")
add("B18", "Slide 14: Calvary institutional funder count", 42, byf[byf.funder_type != "daf_sponsor"].funder_id.nunique(), 0)

# ================================================================ F. need and capacity
geo = rd("dim_geo.csv", dtype=str)
w = geo[geo.geo_level == "ward"].set_index("ward"); dc = geo[(geo.geo_level == "state") & (geo.name == "District of Columbia")].iloc[0]
add("F01", "Ward 8 poverty (%)", 31, 100 * float(w.loc["8", "poverty_rate"]), 0, "ACS 2020-24")
add("F02", "Ward 7 poverty (%)", 23, 100 * float(w.loc["7", "poverty_rate"]), 0)
add("F03", "DC poverty (%)", 15, 100 * float(dc["poverty_rate"]), 0)
add("F04", "Ward 8 female poverty (%)", 32, 100 * float(w.loc["8", "female_poverty_rate"]), 0, f"adult female poverty {100*float(w.loc['8','x_adult_female_poverty_rate']):.1f}%")
add("F05", "Renters paying 50%+ of income, Wards 7 and 8 ('about a third')", "~33", f"W7 {100*float(w.loc['7','rent_burden_50plus_share']):.1f}, W8 {100*float(w.loc['8','rent_burden_50plus_share']):.1f}", "manual:rounding", f"DC {100*float(dc['rent_burden_50plus_share']):.1f}%")
hic = rd("supp_hic_projects.csv", dtype=str); hic["total_beds"] = pd.to_numeric(hic.total_beds, errors="coerce")
dch = hic[hic.coc_code == "DC-500"]; calh = dch[dch.recipient_ein == EIN]
b22_all = calh[calh.year == "2022"].total_beds.sum(); b25_all = calh[calh.year == "2025"].total_beds.sum()
b22_th = calh[(calh.year == "2022") & (calh.project_type == "TH")].total_beds.sum(); b25_th = calh[(calh.year == "2025") & (calh.project_type == "TH")].total_beds.sum()
dc22_th = dch[(dch.year == "2022") & (dch.project_type == "TH")].total_beds.sum(); dc25_th = dch[(dch.year == "2025") & (dch.project_type == "TH")].total_beds.sum()
hc = rd("supp_homeless_counts.csv", dtype=str); hc["value"] = pd.to_numeric(hc.value, errors="coerce")
th_sum22 = hc[(hc.coc_code == "DC-500") & (hc.year == "2022") & (hc.measure == "hic_beds_year_round__th") & (hc.population == "all")].value.iloc[0]
th_sum25 = hc[(hc.coc_code == "DC-500") & (hc.year == "2025") & (hc.measure == "hic_beds_year_round__th") & (hc.population == "all")].value.iloc[0]
add("F06", "Calvary beds 2022", 68, b22_all, 0, f"all project types (TH {b22_th:.0f} + PSH + RRH); TH only = {b22_th:.0f}")
add("F07", "Calvary beds 2025", 124, b25_all, 0, f"all project types (TH {b25_th:.0f} + PSH 16 + RRH 14); TH only = {b25_th:.0f}")
add("F08", "Share of DC TH beds 2022 (%)", 2.5, 100 * b22_th / dc22_th, 1, f"TH-only {b22_th:.0f} / DC TH {dc22_th:.0f} (HIC summary {th_sum22:.0f}); all-types 68 / DC TH = {100*b22_all/dc22_th:.1f}%")
add("F09", "Share of DC TH beds 2025 (%)", 6.8, 100 * b25_th / dc25_th, 1, f"TH-only {b25_th:.0f} / DC TH {dc25_th:.0f} (HIC summary {th_sum25:.0f}); all-types 124 / DC TH = {100*b25_all/dc25_th:.1f}%")
add("F10", "Beds vs share basis consistency", "124 beds ... 6.8% of DC TH beds", f"124 = all types; 6.8% = TH-only ({b25_th:.0f}) / DC TH", "manual:MISMATCH",
    "The headline bed count is all project types (TH+PSH+RRH) but the share is computed on TH beds only. Read together ('124 beds, 6.8% of DC's transitional-housing beds') the sentence implies 124 TH beds. Either state 94 TH beds (6.8%) or 124 beds of all types (no single-type share).")
pit = hc[(hc.coc_code == "DC-500") & (hc.measure == "pit_overall") & (hc.population == "all")].set_index("year").value
add("F11", "DC PIT 2016", 8350, pit["2016"], 0)
add("F12", "DC PIT 2025", 5138, pit["2025"], 0)

# ================================================================ G. reserve
add("G01", "Six months of FY25 expenses ($M)", 2.8, X / 2 / 1e6, 1, f"{X/2:,.0f}")
privrev = R - GOV
add("G02", "Private (non-government) revenue FY25 ($M)", 2.1, privrev / 1e6, 1, f"total revenue - 990 line 1e = {privrev:,.0f}")
add("G03", "Public share if private rises to $3.0M at flat government (%)", "about half", 100 * GOV / (GOV + 3.0e6), "manual:rounding", f"{GOV:,.0f} / ({GOV:,.0f} + 3,000,000)")

# ================================================================ H. reviewer-guide self-checks
add("H01", "Reviewer check 1: FY25 preferred total_revenue", 4967995, R, 0)
caf = gr[(gr.funder_ein == "526036989") & (gr.tax_year == 2024) & (gr.source_type == "pf_grants_paid")]
add("H02", "Reviewer check 2: Cafritz TY2024 grant", 170000, caf.amount.sum(), 0, f"{len(caf)} row(s)")
s23 = gov[(gov.source_type == "audit_sefa") & (gov.fiscal_year == 2023)]
add("H03", "Reviewer check 3: audit_sefa FY2023 sum", 937999, s23.amount.sum(), 0, f"{len(s23)} rows; largest {s23.amount.max():,.0f}")
o26 = ovsjg[ovsjg.fiscal_year == 2026].set_index("program_name").amount
add("H04a", "Reviewer check 4: OVSJG FY2026 New Foundations", 543056, o26.filter(like="New Foundations").iloc[0], 0)
add("H04b", "Reviewer check 4: OVSJG FY2026 Reach Up", 507595, o26.filter(like="Reach Up").iloc[0], 0)
add("H05", "Reviewer check 5: Ward 8 poverty_rate", 0.306, float(w.loc["8", "poverty_rate"]), 3)
dwc = fin[(fin.ein == "311597223") & (fin.fiscal_year == 2024) & (fin.preferred == 1)]
add("H06", "Reviewer check 6: DWC FY2024 total_revenue", 34403997, dwc.total_revenue.iloc[0] if len(dwc) else None, 0, f"{len(dwc)} preferred row(s)")

# ---------------------------------------------------------------- write
df = pd.DataFrame(rows)
df["recomputed"] = df.recomputed.apply(lambda v: round(v, 4) if isinstance(v, (float, np.floating)) else v)
df = df.sort_values("item", key=lambda s: s.map(lambda x: (x[0], x[1:]))).reset_index(drop=True)
df.to_csv(os.path.join(OUT, "recompute_m1m2m9.csv"), index=False)
df.to_csv(os.path.join(OUT, "recompute_m1m2m9.csv"), index=False)
print(df.match.value_counts())
print(df[df.match == "MISMATCH"][["item", "label", "as_shown", "recomputed"]].to_string())
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 60)
print(df[["item", "label", "as_shown", "recomputed", "match"]].to_string())
