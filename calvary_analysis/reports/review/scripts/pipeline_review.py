"""Independent recomputation of funder_pipeline.csv scores, tiers, components and evidence.
Review-only: reads from ROOT, writes only to this directory."""
# Review script. Paths resolve from this file: calvary_analysis/reports/review/scripts/ -> project root three levels up.
import os as _os, pathlib as _pl
_HERE = _pl.Path(__file__).resolve().parent
PROJECT_ROOT = str(_pl.Path(_os.environ.get("CALVARY_ROOT", _HERE.parents[3])))
REVIEW_OUT = _os.environ.get("REVIEW_OUT", str(_HERE.parent / "evidence"))
import os, math, yaml, numpy as np, pandas as pd

ROOT = PROJECT_ROOT
OUT = os.path.dirname(os.path.abspath(__file__))
pd.set_option("display.width", 250)

W = yaml.safe_load(open(f"{ROOT}/calvary_analysis/config/scoring_weights.yaml"))
weights = W["weights"]
AS, RS = W["award_size_scale"], W["regional_scale"]
CAP = W["peer_giving_cap"]
ACC = W["accessibility_scores"]
TIERS = W["tiers"]
IN_KIND = set(W["in_kind_channels"]); DAF_LIKE = set(W["daf_like_channels"])

pipe = pd.read_csv(f"{ROOT}/calvary_analysis/recommendations/funder_pipeline.csv", dtype={"funder_id": str})
for c in ["gives_to_calvary_ty2020_24", "on_calvary_list_or_crm", "itemized_ty2023plus", "placeholder_ty2023plus"]:
    pipe[c] = pipe[c].map(lambda v: True if str(v) == "True" else (False if str(v) == "False" else np.nan))
comp_cols = [f"s_{k}" for k in weights]
inst = pipe[comp_cols].notna().all(axis=1)          # rows with numeric component scores
pipe["is_institutional"] = inst
print("rows with numeric components:", inst.sum(), "| by tier:", pipe[inst].tier.value_counts().to_dict())
print("funder_type among institutional:", pipe[inst].funder_type.value_counts().to_dict())

# ---------------- Step 1: arithmetic + tier rule ----------------
def wscore(r):
    return sum(weights[k] * r[f"s_{k}"] for k in weights)

a = pipe[inst].copy()
a["score_recomputed"] = a.apply(wscore, axis=1)
a["score_diff"] = a.score_recomputed - a.score
a["score_match"] = a.score_diff.abs() <= 0.0005

def rule_tier(df, score_col="score", min_award=TIERS["tier1_min_award"], t1=TIERS["tier1_min_score"], t2=TIERS["tier2_min_score"], cap=TIERS["max_tier1"], daf_cap=False):
    """Tier rule as documented in the yaml. daf_cap=True adds the undocumented rule found in 07_m7_pipeline.py
    (daf_like_channels are held at Tier 2 or lower), used only for the alternative-weighting scenarios."""
    s = df[score_col]
    t1_elig = (s >= t1) & (df.typical_grant >= min_award)
    if daf_cap:
        t1_elig &= ~df.funder_id.isin(DAF_LIKE)
    # cap: keep the top `cap` eligible by score
    elig_idx = df[t1_elig].sort_values(score_col, ascending=False).index[:cap]
    tier = pd.Series(3, index=df.index)
    tier[s >= t2] = 2
    tier[elig_idx] = 1
    return tier

a["tier_by_rule"] = rule_tier(a)
a["tier_by_rule_with_daf_cap"] = rule_tier(a, daf_cap=True)
a["tier_match"] = a.tier_by_rule == a.tier
a["tier_rule_note"] = ""
a.loc[~a.tier_match & (a.tier == 3), "tier_rule_note"] = "Tier 3 in file but would qualify for tier " + a.tier_by_rule.astype(str)
a.loc[~a.tier_match & (a.tier != 3), "tier_rule_note"] = "file tier " + a.tier.astype(str) + " vs rule tier " + a.tier_by_rule.astype(str)
arith = a[["rank", "funder_id", "funder_name", "funder_type", "tier", "score", "typical_grant"] + comp_cols +
          ["score_recomputed", "score_diff", "score_match", "tier_by_rule", "tier_match", "tier_rule_note", "tier_by_rule_with_daf_cap"]].sort_values("rank")
arith.to_csv(f"{OUT}/pipeline_arithmetic.csv", index=False)
print("\nSTEP 1: score matches", arith.score_match.sum(), "/", len(arith), "; max |diff|", arith.score_diff.abs().max().round(5))
print("tier matches", arith.tier_match.sum(), "/", len(arith))
print(arith[~arith.score_match | ~arith.tier_match][["rank", "funder_id", "funder_name", "tier", "score", "score_recomputed", "typical_grant", "tier_by_rule", "tier_rule_note"]].to_string())
# non-institutional rows: tier vs score only (no award rule applies to gov/corporate analyst rows)
ni = pipe[~inst]
print("\nnon-institutional rows whose tier does not follow the score cutoffs (informational):")
print(ni[((ni.tier == 2) & (ni.score < TIERS["tier2_min_score"])) | ((ni.tier == 1) & (ni.score < TIERS["tier1_min_score"])) | ((ni.tier == 3) & (ni.score >= TIERS["tier2_min_score"]))][["rank", "funder_id", "funder_name", "funder_type", "tier", "score", "typical_grant"]].to_string())

# ---------------- Step 2: components from evidence columns ----------------
def loglin(x, lo, hi):
    if pd.isna(x) or x <= 0:
        return 0.0
    return float(np.clip((math.log(x) - math.log(lo)) / (math.log(hi) - math.log(lo)), 0, 1))

def access(r):
    fid, ft, n = r.funder_id, r.funder_type, r.dc_sector_recipients
    if fid in DAF_LIKE:
        base = ACC["daf_sponsor"]; label = "daf_sponsor"
    elif ft == "private_foundation":
        n = 0 if pd.isna(n) else n
        label = "private_foundation_broad" if n >= 20 else ("private_foundation_mid" if n >= 8 else "private_foundation_narrow")
        base = ACC[label]
    elif ft in ACC:
        base, label = ACC[ft], ft
    else:
        base, label = ACC["other"], "other"
    pen = 0.0
    if r.placeholder_ty2023plus is True:
        pen += W["placeholder_penalty"]
    if fid in IN_KIND:
        pen += W["in_kind_penalty"]
    return pd.Series({"acc_label": label, "acc_base": base, "acc_penalty": pen, "s_accessibility_recomputed": max(base - pen, 0.0)})

c = pipe[inst].copy()
c["s_peer_giving_recomputed"] = (c.peers_funded.fillna(0) / CAP).clip(upper=1)
c["s_award_size_recomputed_typical"] = c.typical_grant.map(lambda x: loglin(x, AS["min_amount"], AS["max_amount"]))
c["s_award_size_recomputed_median"] = c.median_peer_grant.map(lambda x: loglin(x, AS["min_amount"], AS["max_amount"]))
c["s_regional_giving_recomputed"] = c.dc_sector_amount.map(lambda x: loglin(x, RS["min_amount"], RS["max_amount"]))
c = pd.concat([c, c.apply(access, axis=1)], axis=1)
TOL = 0.0005
c["d_peer_giving"] = c.s_peer_giving_recomputed - c.s_peer_giving
c["d_award_size_typical"] = c.s_award_size_recomputed_typical - c.s_award_size
c["d_award_size_median"] = c.s_award_size_recomputed_median - c.s_award_size
c["d_regional_giving"] = c.s_regional_giving_recomputed - c.s_regional_giving
c["d_accessibility"] = c.s_accessibility_recomputed - c.s_accessibility
c["peer_giving_match"] = c.d_peer_giving.abs() <= TOL
c["award_size_match_typical"] = c.d_award_size_typical.abs() <= TOL
c["award_size_match_median"] = c.d_award_size_median.abs() <= TOL
c["regional_giving_match"] = c.d_regional_giving.abs() <= TOL
c["accessibility_match"] = c.d_accessibility.abs() <= TOL
c["typical_eq_median"] = np.isclose(c.typical_grant.fillna(-1), c.median_peer_grant.fillna(-1))
comp = c[["rank", "funder_id", "funder_name", "funder_type", "tier", "score", "typical_grant", "median_peer_grant", "peers_funded", "dc_sector_amount", "dc_sector_recipients", "placeholder_ty2023plus",
          "s_peer_giving", "s_peer_giving_recomputed", "d_peer_giving", "peer_giving_match",
          "s_award_size", "s_award_size_recomputed_typical", "d_award_size_typical", "award_size_match_typical", "s_award_size_recomputed_median", "d_award_size_median", "award_size_match_median", "typical_eq_median",
          "s_regional_giving", "s_regional_giving_recomputed", "d_regional_giving", "regional_giving_match",
          "s_accessibility", "acc_label", "acc_base", "acc_penalty", "s_accessibility_recomputed", "d_accessibility", "accessibility_match"]].sort_values("rank")
comp.to_csv(f"{OUT}/pipeline_components.csv", index=False)
print("\nSTEP 2 matches of", len(comp), ":")
for k in ["peer_giving_match", "award_size_match_typical", "award_size_match_median", "regional_giving_match", "accessibility_match"]:
    print(f"  {k}: {comp[k].sum()}")
print("typical_grant == median_peer_grant:", comp.typical_eq_median.sum())
mism = comp[~(comp.peer_giving_match & comp.award_size_match_typical & comp.regional_giving_match & comp.accessibility_match)]
print(mism[["rank", "funder_id", "funder_name", "tier", "typical_grant", "median_peer_grant", "s_peer_giving", "s_peer_giving_recomputed", "s_award_size", "s_award_size_recomputed_typical", "s_award_size_recomputed_median", "s_regional_giving", "s_regional_giving_recomputed", "s_accessibility", "s_accessibility_recomputed", "acc_label", "acc_penalty"]].to_string())

# ---------------- Step 3: evidence from clean tables ----------------
g = pd.read_csv(f"{OUT}/grants_pipeline_funders.csv", dtype={"funder_id": str, "recipient_ein": str, "notes": str, "source_type": str})
g["placeholder"] = g.notes.fillna("").str.contains("placeholder_row=1")
peers = pd.read_csv(f"{ROOT}/calvary_funding_data/config/core_peers.csv", dtype={"ein": str})
PEERS = set(peers.ein)
um = pd.read_csv(f"{ROOT}/calvary_funding_data/clean/dim_universe_membership.csv", dtype=str, usecols=["universe", "ein"])
DCS = set(um[um.universe == "dc_sector"].ein)
print("\ncore peers:", len(PEERS), "| dc_sector EINs:", len(DCS), "| peers in dc_sector:", len(PEERS & DCS))
FILED = {"pf_grants_paid", "schedule_i"}
CALVARY = "521307706"

t1 = pipe[inst & (pipe.tier == 1)].sort_values("score", ascending=False)
t2 = pipe[inst & (pipe.tier == 2)].sort_values("score", ascending=False).head(10)
targets = pd.concat([t1, t2])
rows = []
for _, r in targets.iterrows():
    gf = g[g.funder_id == r.funder_id]
    filed = gf[gf.source_type.isin(FILED) & (gf.cumulative_flag == 0) & gf.tax_year.between(2020, 2024)]
    pg = filed[filed.recipient_ein.isin(PEERS) & filed.amount.notna()]
    per_peer = pg.groupby("recipient_ein").amount.sum()
    per_peer_year = pg.groupby(["recipient_ein", "tax_year"]).amount.sum()
    dc = filed[filed.recipient_ein.isin(DCS)]
    any_calv = gf[(gf.recipient_ein == CALVARY) & gf.tax_year.between(2020, 2024)]
    rows.append({
        "rank": r["rank"], "funder_id": r.funder_id, "funder_name": r.funder_name, "tier": r.tier, "score": r.score,
        "peers_funded_file": r.peers_funded, "peers_funded_recomputed": pg.recipient_ein.nunique(),
        "peer_amount_file": r.peer_amount, "peer_amount_recomputed": pg.amount.sum(),
        "median_peer_grant_file": r.median_peer_grant,
        "median_over_grant_rows": pg.amount.median() if len(pg) else np.nan,
        "median_over_per_peer_totals": per_peer.median() if len(per_peer) else np.nan,
        "median_over_peer_year_totals": per_peer_year.median() if len(per_peer_year) else np.nan,
        "n_peer_grant_rows": len(pg),
        "max_peer_grant_file": r.max_peer_grant, "max_peer_grant_recomputed": pg.amount.max() if len(pg) else np.nan,
        "dc_sector_amount_file": r.dc_sector_amount, "dc_sector_amount_recomputed": dc.amount.sum(),
        "dc_sector_recipients_file": r.dc_sector_recipients, "dc_sector_recipients_recomputed": dc.recipient_ein.nunique(),
        "gives_to_calvary_file": r.gives_to_calvary_ty2020_24,
        "gives_to_calvary_filed_recomputed": bool(len(filed[filed.recipient_ein == CALVARY])),
        "gives_to_calvary_any_source_recomputed": bool(len(any_calv)),
        "calvary_total_file": r.calvary_total_ty2020_24, "calvary_total_filed_recomputed": filed[filed.recipient_ein == CALVARY].amount.sum(),
        "itemized_ty2023plus_file": r.itemized_ty2023plus,
        "itemized_ty2023plus_recomputed": bool(len(gf[gf.source_type.isin(FILED) & (gf.tax_year >= 2023) & ~gf.placeholder])),
        "placeholder_ty2023plus_file": r.placeholder_ty2023plus,
        "placeholder_ty2023plus_recomputed": bool(len(gf[(gf.tax_year >= 2023) & gf.placeholder])),
        "n_filed_rows_ty2020_24": len(filed), "n_rows_any_source": len(gf),
        "tax_years_filed": ",".join(str(int(y)) for y in sorted(filed.tax_year.dropna().unique())),
    })
ev = pd.DataFrame(rows)
def close(a_, b_):
    return np.isclose(a_.fillna(-1).astype(float), b_.fillna(-1).astype(float), rtol=0, atol=0.5)
ev["peers_funded_match"] = close(ev.peers_funded_file, ev.peers_funded_recomputed)
ev["peer_amount_match"] = close(ev.peer_amount_file, ev.peer_amount_recomputed)
ev["median_match_rows"] = close(ev.median_peer_grant_file, ev.median_over_grant_rows)
ev["median_match_per_peer"] = close(ev.median_peer_grant_file, ev.median_over_per_peer_totals)
ev["median_match_peer_year"] = close(ev.median_peer_grant_file, ev.median_over_peer_year_totals)
ev["max_peer_match"] = close(ev.max_peer_grant_file, ev.max_peer_grant_recomputed)
ev["dc_amount_match"] = close(ev.dc_sector_amount_file, ev.dc_sector_amount_recomputed)
ev["dc_recipients_match"] = close(ev.dc_sector_recipients_file, ev.dc_sector_recipients_recomputed)
ev["gives_match"] = ev.gives_to_calvary_file == ev.gives_to_calvary_filed_recomputed
ev["itemized_match"] = ev.itemized_ty2023plus_file == ev.itemized_ty2023plus_recomputed
ev["placeholder_match"] = ev.placeholder_ty2023plus_file == ev.placeholder_ty2023plus_recomputed
ev = ev.sort_values("rank")
ev.to_csv(f"{OUT}/pipeline_evidence.csv", index=False)
print("\nSTEP 3 evidence matches of", len(ev))
for k in [k for k in ev.columns if k.endswith("_match") or k.startswith("median_match")]:
    print(f"  {k}: {ev[k].sum()}")
print(ev[["rank", "funder_id", "funder_name", "peers_funded_file", "peers_funded_recomputed", "median_peer_grant_file", "median_over_grant_rows", "median_over_per_peer_totals", "median_over_peer_year_totals", "dc_sector_amount_file", "dc_sector_amount_recomputed", "dc_sector_recipients_file", "dc_sector_recipients_recomputed", "gives_to_calvary_file", "gives_to_calvary_filed_recomputed", "gives_to_calvary_any_source_recomputed", "itemized_ty2023plus_file", "itemized_ty2023plus_recomputed", "placeholder_ty2023plus_file", "placeholder_ty2023plus_recomputed"]].to_string())

# ---------------- Step 4: alternative weightings ----------------
base_t1 = set(pipe[pipe.tier == 1].funder_id); base_t2 = set(pipe[pipe.tier == 2].funder_id)
def apply_alt(wts=None, min_award=TIERS["tier1_min_award"], adj=None):
    p = pipe.copy()
    s = p.score.copy()
    if wts is not None:
        s[inst] = p[inst].apply(lambda r: sum(wts[k] * r[f"s_{k}"] for k in wts), axis=1)
    if adj is not None:
        s = s + adj(p)
    p["new_score"] = s.round(4)
    p["new_tier"] = p.tier
    p.loc[inst, "new_tier"] = rule_tier(p[inst], "new_score", min_award=min_award, daf_cap=True)
    return p

def membership(p):
    n1 = set(p[p.new_tier == 1].funder_id); n2 = set(p[p.new_tier == 2].funder_id)
    nm = lambda ids: "; ".join(f"{i} {p.set_index('funder_id').funder_name[i][:40]} ({p.set_index('funder_id').new_score[i]:.3f})" for i in sorted(ids, key=lambda i: -p.set_index('funder_id').new_score[i])) or "none"
    return {"t1_added": nm(n1 - base_t1), "t1_dropped": nm(base_t1 - n1), "t2_added": nm(n2 - base_t2 - base_t1), "t2_dropped": nm((base_t2 - n2) - n1),
            "n_t1": len(n1), "n_t2": len(n2)}

W_eq = {k: 1 / 7 for k in weights}
W_size = {"award_size": 0.30, "mission_fit": 0.20, "peer_giving": 0.15, "relationship": 0.15, "regional_giving": 0.10, "accessibility": 0.05, "durability": 0.05}
W_rel = dict(weights); W_rel["relationship"] = 0.05; W_rel["award_size"] = weights["award_size"] + 0.10
scen = {
    "(a) equal weights 1/7": apply_alt(W_eq),
    "(b) size matters": apply_alt(W_size),
    "(c) relationship-light": apply_alt(W_rel),
    "(d) no current-funder bonus (-0.0525 where gives_to_calvary)": apply_alt(adj=lambda p: np.where(inst & (p.gives_to_calvary_ty2020_24 == True), -W["relationship_bonus"]["current_funder"] * weights["relationship"], 0.0)),
    "(e) tier1_min_award = $50,000": apply_alt(min_award=50000),
    "(f) tier1_min_award = $10,000": apply_alt(min_award=10000),
}
md = ["# Alternative weightings: Tier 1 / Tier 2 membership changes vs funder_pipeline.csv", "",
      f"Baseline (file): Tier 1 = {len(base_t1)} rows ({sum(inst & (pipe.tier==1))} institutional), Tier 2 = {len(base_t2)} rows ({sum(inst & (pipe.tier==2))} institutional).",
      "Only rows with numeric component scores are re-scored; government / CRM-corporate / opportunity rows keep their file score and tier. Tier rule applied: Tier 1 iff score >= 0.62 and typical_grant >= min award (cap 20); Tier 2 iff score >= 0.48.",
      "The undocumented script rule that holds daf_like_channels (311709466) at Tier 2 is kept in these scenarios so it does not show up as a spurious change.",
      "Scenario (d) caveat: s_relationship is clipped at 1.0 in the file, so for rows at 1.0 the true effect of removing the 0.35 bonus is at most 0.0525 and may be smaller (the un-clipped path strength is not in the pipeline file).",
      "Scores shown to 3 dp. Names truncated to 40 characters.", ""]
md.append("| scenario | weights / change | Tier 1 n | Tier 2 n | Tier 1 added | Tier 1 dropped | Tier 2 added (from Tier 3) | Tier 2 dropped (to Tier 3) |")
md.append("|---|---|---|---|---|---|---|---|")
desc = {"(a) equal weights 1/7": "all seven 0.1429", "(b) size matters": "award 0.30 mission 0.20 peer 0.15 rel 0.15 regional 0.10 access 0.05 durab 0.05",
        "(c) relationship-light": "rel 0.05, award 0.25, others as file", "(d) no current-funder bonus (-0.0525 where gives_to_calvary)": "file weights; score - 0.35*0.15 for current funders",
        "(e) tier1_min_award = $50,000": "file weights; min award 50,000", "(f) tier1_min_award = $10,000": "file weights; min award 10,000"}
tops = []
for name, p in scen.items():
    m = membership(p)
    md.append(f"| {name} | {desc[name]} | {m['n_t1']} | {m['n_t2']} | {m['t1_added']} | {m['t1_dropped']} | {m['t2_added']} | {m['t2_dropped']} |")
    top = p.sort_values(["new_score", "rank"], ascending=[False, True]).head(15)
    tops.append((name, top))
md.append("")
for name, top in tops:
    md += [f"## Top 15 by score: {name}", "", "| # | funder_id | funder | type | file tier | new tier | file score | new score | typical grant |", "|---|---|---|---|---|---|---|---|---|"]
    for i, (_, r) in enumerate(top.iterrows(), 1):
        tg = "" if pd.isna(r.typical_grant) else f"{r.typical_grant:,.0f}"
        md.append(f"| {i} | {r.funder_id} | {r.funder_name[:40]} | {r.funder_type} | {r.tier} | {r.new_tier} | {r.score:.3f} | {r.new_score:.3f} | {tg} |")
    md.append("")

# relationship = 0.5 sensitivity for Tier 1 institutional
md += ["## Tier 1 institutional rows if s_relationship were 0.5 (original weights)", "", "| funder_id | funder | s_relationship | score | score at rel=0.5 | still Tier 1? |", "|---|---|---|---|---|---|"]
for _, r in t1.iterrows():
    s05 = r.score - weights["relationship"] * (r.s_relationship - 0.5)
    md.append(f"| {r.funder_id} | {r.funder_name[:40]} | {r.s_relationship:.3f} | {r.score:.3f} | {s05:.3f} | {'yes' if s05 >= TIERS['tier1_min_score'] else 'NO (falls to Tier ' + ('2' if s05 >= TIERS['tier2_min_score'] else '3') + ')'} |")
md.append("")
# also: which Tier 2 institutional rows would enter Tier 1 at rel = 0.5
md += ["## Tier 2 institutional rows that would enter Tier 1 if s_relationship were 0.5 (original weights, min award $25K)", ""]
ent = []
for _, r in pipe[inst & (pipe.tier == 2)].iterrows():
    s05 = r.score - weights["relationship"] * (r.s_relationship - 0.5)
    if s05 >= TIERS["tier1_min_score"] and r.typical_grant >= TIERS["tier1_min_award"]:
        ent.append(f"- {r.funder_id} {r.funder_name[:40]}: {r.score:.3f} -> {s05:.3f}")
md += ent or ["- none"]
open(f"{OUT}/pipeline_alt_weights.md", "w").write("\n".join(md) + "\n")
print("\nSTEP 4 written")
for name, p in scen.items():
    m = membership(p); print(name, "| T1 n", m["n_t1"], "| T1 +", m["t1_added"], "| T1 -", m["t1_dropped"], "| T2 +", m["t2_added"], "| T2 -", m["t2_dropped"])

# ---------------- Step 5: flags ----------------
fl = []
WORKPLACE = {"521593963", "521167581", "541517707", "810693451"}
for _, r in pipe.iterrows():
    flags = []
    if r.tier in (1, 2) and pd.notna(r.typical_grant) and r.typical_grant < 5000:
        flags.append("typical_grant_below_5000 (matching-gift / small-check channel)")
    if r.funder_id in WORKPLACE:
        flags.append("workplace_giving_or_in_kind_channel")
    if r.funder_id in DAF_LIKE:
        flags.append("daf_like_program (T. Rowe Price)")
    if r.on_calvary_list_or_crm is True and r.gives_to_calvary_ty2020_24 is False:
        flags.append("on_list_or_crm_but_no_filed_grant (filing-lag candidate)")
    if isinstance(r.state, str) and r.state not in ("DC", "MD", "VA"):
        flags.append(f"state_outside_DMV ({r.state})")
    if flags:
        fl.append({"rank": r["rank"], "funder_id": r.funder_id, "funder_name": r.funder_name, "funder_type": r.funder_type, "tier": r.tier, "score": r.score, "typical_grant": r.typical_grant,
                   "state": r.state, "gives_to_calvary_ty2020_24": r.gives_to_calvary_ty2020_24, "on_calvary_list_or_crm": r.on_calvary_list_or_crm, "calvary_last_ty": r.calvary_last_ty, "flags": " | ".join(flags)})
flags_df = pd.DataFrame(fl).sort_values("rank")
flags_df.to_csv(f"{OUT}/pipeline_flags.csv", index=False)
print("\nSTEP 5 flags:", len(flags_df), "rows;", (flags_df.tier <= 2).sum(), "in Tier 1/2")
print(flags_df[flags_df.tier <= 2].to_string())
