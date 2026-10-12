"""M7: Opportunity pipeline. Scores the candidate funders from M5 (with M6 relationship paths and the M4
landscape) on the dimensions in config/scoring_weights.yaml, assigns tiers, adds the government and
corporate (CRM) tracks and relevant federal opportunities, and drafts the 90-day action plan for Tier 1."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import style  # noqa: E402
from lib.common import ANALYSIS, CLEAN, load, log, money, register_insight, save_chart_data  # noqa: E402

S = "07_m7_pipeline"
CFG = yaml.safe_load(open(ANALYSIS / "config" / "scoring_weights.yaml"))
W = CFG["weights"]; assert abs(sum(W.values()) - 1) < 1e-6, "weights must sum to 1"
cand = pd.read_csv(ANALYSIS / "chart_data" / "m5_00_candidate_funders.csv", dtype={"funder_id": str})
paths = pd.read_csv(ANALYSIS / "chart_data" / "m6_05_relationship_paths.csv", dtype={"funder_id": str})
cand = cand.merge(paths[["funder_id", "close_peers_funded", "calvary_cofunders_overlapping", "board_links_high", "board_links_medium", "board_link_subjects", "path_strength", "path_strength_consulting"]], on="funder_id", how="left")
cand = cand[cand.funder_type != "daf_sponsor"].copy()        # DAF sponsors are a channel, handled separately
cand = cand[~cand.gap_category.eq("current") | (cand.calvary_total_ty2020_24 >= CFG["min_current_funder_total"])]   # drop trivial current funders with no headroom signal
# Funder status from the guideline notes (first-party page and date per funder; review findings R16, R17)
NOTES = pd.read_csv(ANALYSIS / "config" / "guideline_notes.csv", dtype=str).fillna("").set_index("funder_id")
cand["open_status"] = cand.funder_id.map(NOTES.open_status).replace("", np.nan).fillna("unverified")
CH = CFG.get("channels", {})


def loglin(x, lo, hi):
    x = np.clip(np.asarray(x, dtype=float), lo, hi)
    return (np.log10(x) - np.log10(lo)) / (np.log10(hi) - np.log10(lo))


tags = cand.issue_focus_tags.fillna("")
mission = np.select([tags.str.contains("housing|dv|women"), tags.str.contains("behavioral_health|workforce|health"), tags.str.contains("general_operating")], [1.0, 0.7, 0.6], default=0.35)
mshare = (cand.mission_tagged_amount.fillna(0) / cand.dc_sector_amount.replace(0, np.nan)).fillna(0)
cand["s_mission_fit"] = np.clip(0.7 * mission + 0.3 * np.minimum(mshare * 4, 1), 0, 1)
cand["s_peer_giving"] = np.minimum(cand.peers_funded, CFG["peer_giving_cap"]) / CFG["peer_giving_cap"]
cand["s_regional_giving"] = loglin(cand.dc_sector_amount.fillna(0) + 1, CFG["regional_scale"]["min_amount"], CFG["regional_scale"]["max_amount"])
typical = cand.median_peer_grant.fillna(cand.median_grant).fillna(cand.calvary_max_grant).fillna(0)
cand["typical_grant"] = typical
cand["s_award_size"] = loglin(typical + 1, CFG["award_size_scale"]["min_amount"], CFG["award_size_scale"]["max_amount"])
A = CFG["accessibility_scores"]
rec = cand.dc_sector_recipients.fillna(0)
acc = np.select([cand.funder_type == "private_foundation"], [np.where(rec >= 20, A["private_foundation_broad"], np.where(rec >= 8, A["private_foundation_mid"], A["private_foundation_narrow"]))],
                default=cand.funder_type.map(A).fillna(A["other"]).astype(float))
acc = acc - CFG["placeholder_penalty"] * cand.placeholder_ty2023plus.astype(int) - CFG["in_kind_penalty"] * cand.funder_id.isin(CFG["in_kind_channels"]).astype(int)
acc = np.where(cand.funder_id.isin(CFG.get("daf_like_channels", [])), A["daf_sponsor"], acc)
cand["track_override"] = np.where(cand.funder_id.isin(CFG.get("daf_like_channels", [])), "daf channel (donor-advised program)", cand.funder_id.map(CH).fillna(""))
cand["s_accessibility"] = np.clip(acc, 0, 1)
cand["s_durability"] = np.clip(0.6 * cand.peer_years.fillna(0) / 5 + 0.4 * cand.years_active.fillna(0) / 5, 0, 1)
R = CFG["relationship_bonus"]
rel = cand.path_strength.fillna(0) + R["current_funder"] * cand.gives_to_calvary_ty2020_24.astype(int) + R["lapsed_funder"] * cand.gap_category.eq("lapsed").astype(int) + R["on_calvary_list_or_crm"] * cand.on_calvary_list_or_crm.astype(int)
cand["s_relationship"] = np.clip(rel, 0, 1)
cand["score"] = sum(W[k] * cand[f"s_{k}"] for k in W).round(3)
T = CFG["tiers"]
cand["tier"] = np.select([(cand.score >= T["tier1_min_score"]) & (typical >= T["tier1_min_award"]), cand.score >= T["tier2_min_score"]], [1, 2], default=3)
cand = cand.sort_values(["tier", "score"], ascending=[True, False]).reset_index(drop=True)
t1_idx = cand.index[cand.tier == 1][T["max_tier1"]:]
cand.loc[t1_idx, "tier"] = 2
cand["track"] = np.where(cand.gap_category.str.startswith("current"), "institutional: steward / upgrade", np.where(cand.gap_category == "lapsed", "institutional: re-engage", "institutional: new"))
cand["track"] = np.where(cand.track_override != "", cand.track_override, cand.track)
cand.loc[cand.track_override != "", "tier"] = np.maximum(cand.loc[cand.track_override != "", "tier"], 2)
# status rules (see config/scoring_weights.yaml): closed and ineligible funders are never pursued
closed_new = cand.open_status.eq("closed_to_new")
cand.loc[closed_new, "tier"] = np.maximum(cand.loc[closed_new, "tier"], 2)
cand.loc[closed_new, "track"] = cand.loc[closed_new, "track"] + " (closed to new applicants)"
cand.loc[cand.open_status.eq("not_eligible"), "tier"] = 3
cand.loc[cand.open_status.eq("not_eligible"), "track"] = "not eligible: " + cand.loc[cand.open_status.eq("not_eligible"), "funder_id"].map(NOTES.open_status_note)
sunset = cand.open_status.eq("sunset")
cand.loc[sunset, "tier"] = 3
cand.loc[sunset, "track"] = "excluded: closed funder (" + cand.loc[sunset, "funder_id"].map(NOTES.open_status_note).str.split(";").str[0] + ")"
# peer-set sensitivity (review finding R10): a funder of exactly three peers can drop out when a provisional peer is swapped
cand["peer_set_note"] = np.where((cand.peers_funded == 3) & ~cand.gap_category.str.startswith("current"), "depends on the provisional peer set", "")
cand["why"] = cand.apply(lambda r: f"{int(r.peers_funded)} peers; typical grant {money(r.typical_grant,'K')}; DC-sector {money(r.dc_sector_amount or 0,'M',1)}; " + ("current funder" if r.gives_to_calvary_ty2020_24 else ("lapsed" if r.gap_category == "lapsed" else "no Calvary grant")) + ("; 'see attached' filer" if r.placeholder_ty2023plus else ""), axis=1)
cand["relationship_path"] = cand.apply(lambda r: "; ".join([x for x in [
    f"current funder (largest grant {money(r.calvary_max_grant,'K')})" if r.gives_to_calvary_ty2020_24 else "",
    f"funds {int(r.close_peers_funded)} peers that share 5+ funders with Calvary" if r.close_peers_funded else "",
    f"{int(r.calvary_cofunders_overlapping)} of Calvary's funders co-fund its grantees" if r.calvary_cofunders_overlapping else "",
    f"board link (high confidence) via {r.board_link_subjects}" if r.board_links_high else "",
    "in Calvary CRM / lists" if r.on_calvary_list_or_crm else ""] if x]), axis=1)
cand["relationship_path_consulting"] = cand.relationship_path + np.where(cand.board_links_medium > 0, cand.board_link_subjects.fillna("").radd("; unconfirmed board link (medium confidence) via "), "")

# ------------------------------------------------------------------ corporate (CRM) track
crm = pd.read_csv(CLEAN / "supp_crm_cash_verification.csv", dtype={"funder_ein": str})
corp = crm[(crm.cash_verified == "not_exempt_filer") & (crm.crm_total >= 50000)].copy()
corp["score"] = np.clip(0.45 + 0.25 * loglin(corp.crm_total, 50000, 750000), 0, 1).round(3)
corp["tier"] = np.where((corp.crm_total >= 250000) & (corp.score >= T["tier1_min_score"]), 1, 2)
corp_rows = pd.DataFrame({"funder_id": corp.funder_ein.fillna("CRM:" + corp.funder_name_raw.str.replace(" ", "_")), "funder_name": corp.funder_name_raw, "funder_type": "corporate (no public filing)",
                          "track": "corporate: steward / upgrade (CRM)", "gap_category": "current corporate (CRM)", "score": corp.score, "tier": corp.tier, "typical_grant": corp.crm_total / 3,
                          "why": "CRM total " + corp.crm_total.map(lambda v: money(v, 'K')) + " 2023-26; cash vs in-kind " + corp.web_inkind_classification.fillna("unverified"),
                          "relationship_path": "existing corporate relationship (CRM); " + np.where(corp.web_inkind_classification.fillna("") == "mixed", "includes pro bono / in-kind", "verify cash share")})

# ------------------------------------------------------------------ government rows and federal opportunities
gov_rows = pd.DataFrame(CFG["government_rows"]).rename(columns={"id": "funder_id", "name": "funder_name", "note": "why"})
gov_rows["funder_type"] = "government"; gov_rows["gap_category"] = "government: retain / expand"; gov_rows["relationship_path"] = "existing grantee / sub-recipient"
o = load("fact_opportunities")
rel_o = o[o.program_area_tags.fillna("").str.contains("housing|dv|women|behavioral_health|workforce|reentry|veterans|maternal") & ~o.funder_name.str.contains("Mission|Embassy|National Institutes|National Science|Indian Health|Defense|Tribal|Bureau of Land", na=False)
          & ~o.title.str.contains("Tribal|Indian|Native|Research|Clinical", na=False) & o.eligibility_text.fillna("").str.contains("nonprofit|Nonprofit|501", regex=True)]
rel_o = rel_o[rel_o.status.isin(["posted", "forecasted"])].copy()
rel_o["score"] = (0.35 + 0.15 * rel_o.program_area_tags.str.contains("housing|dv|women").astype(int) + 0.10 * (rel_o.status == "posted").astype(int)).round(3)
rel_o["tier"] = 3
fed_rows = pd.DataFrame({"funder_id": "OPP:" + rel_o.opportunity_number.astype(str), "funder_name": rel_o.funder_name + ": " + rel_o.title.str.slice(0, 90), "funder_type": "federal opportunity (Grants.gov)",
                         "track": "government_federal: opportunity", "gap_category": "federal opportunity", "score": rel_o.score, "tier": rel_o.tier, "typical_grant": rel_o.award_ceiling,
                         "why": "status " + rel_o.status + "; closes " + rel_o.close_date.fillna("n/a").astype(str) + "; tags " + rel_o.program_area_tags, "relationship_path": "open competition"})

pipe_cols = ["funder_id", "funder_name", "funder_type", "track", "gap_category", "tier", "score", "typical_grant", "why", "relationship_path", "relationship_path_consulting", "open_status", "peer_set_note",
             "s_mission_fit", "s_peer_giving", "s_regional_giving", "s_award_size", "s_accessibility", "s_durability", "s_relationship",
             "peers_funded", "peer_amount", "median_peer_grant", "max_peer_grant", "dc_sector_amount", "dc_sector_recipients", "calvary_total_ty2020_24", "calvary_max_grant", "calvary_last_ty",
             "gives_to_calvary_ty2020_24", "on_calvary_list_or_crm", "itemized_ty2023plus", "placeholder_ty2023plus", "issue_focus_tags", "peers_list", "board_links_high", "board_links_medium", "state"]
pipe = pd.concat([cand.reindex(columns=pipe_cols), gov_rows.reindex(columns=pipe_cols), corp_rows.reindex(columns=pipe_cols), fed_rows.reindex(columns=pipe_cols)], ignore_index=True)
pipe = pipe.sort_values(["tier", "score"], ascending=[True, False]).reset_index(drop=True)
pipe.insert(0, "rank", pipe.index + 1)
out = ANALYSIS / "recommendations"; out.mkdir(exist_ok=True)
pipe.to_csv(out / "funder_pipeline.csv", index=False)
save_chart_data(pipe, "m7_00_funder_pipeline", "Scored and tiered funder pipeline (config/scoring_weights.yaml)", ["fact_grants", "dim_funder", "fact_org_relationships", "supp_crm_cash_verification", "fact_opportunities", "fact_gov_awards"], ["bulk_gt_datalake", "bulk_irs_xml", "input_crm_funders_2023_2026", "api_grantsgov"], S,
                "tiers: 1 pursue now, 2 cultivate 6-12 months, 3 long-term / expansion-dependent; government and corporate rows carry analyst scores (basis=inferred)")

# ------------------------------------------------------------------ 90-day action plan (Tier 1)
t1 = pipe[pipe.tier == 1].copy()
OVR = CFG.get("next_step_overrides", {})
def step(r):
    if r.funder_id in OVR:
        return OVR[r.funder_id]
    if r.track.startswith("government"):
        return "Confirm FY26 award letters and draw-down status; schedule program-officer check-in; map FY27 renewal calendar"
    if r.track.startswith("corporate"):
        return "Quantify cash vs in-kind in the CRM; propose a multi-year sponsorship or program partnership"
    if r.gap_category.startswith("current"):
        return "Upgrade ask: request a multi-year general-operating grant at the funder's peer-level amount, citing the FY25 deficit and the concentration in three public streams"
    if r.gap_category == "lapsed":
        return "Re-engagement call; share FY25 impact data; ask what changed and whether an invitation is possible"
    if r.open_status == "rfp_only":
        return "Watch for its next RFP and meet program staff before it posts"
    if r.open_status == "invitation_only":
        return "Introduction through a named peer or co-funder that leads to an invitation; no LOI"
    return "Warm introduction through a shared peer or co-funder; request guidelines / invitation; submit an LOI in the next cycle"
def owner(r):
    return "CEO + board chair" if (r.typical_grant or 0) >= 100000 or r.track.startswith("government") else ("Development director" if not r.track.startswith("corporate") else "CEO + corporate relations lead")
t1["next_step"] = t1.apply(step, axis=1); t1["owner_role"] = t1.apply(owner, axis=1)
# Sequenced for a six-person fundraising team (supp_calvary_strategic_targets; review finding R09): government
# confirmations first, then two current-funder conversations a fortnight, then introductions.
cur = t1.gap_category.str.startswith("current") & t1.track.str.startswith("institutional")
t1["deadline"] = "Day 60"
t1.loc[t1.track.str.startswith("government"), "deadline"] = "Day 30"
t1.loc[cur, "deadline"] = ["Day 45" if i < 2 else "Day 60" for i in range(int(cur.sum()))]
t1.loc[t1.gap_category == "lapsed", "deadline"] = "Day 75"
t1.loc[t1.track.str.startswith("institutional: new"), "deadline"] = "Day 90 (introduction, then invitation)"
plan = t1[["rank", "funder_name", "track", "tier", "score", "typical_grant", "next_step", "owner_role", "deadline", "open_status", "relationship_path", "why"]]
plan.to_csv(out / "action_plan_90day.csv", index=False)
save_chart_data(plan, "m7_01_action_plan_90day", "90-day action plan for Tier 1 targets", ["fact_grants", "dim_funder", "fact_org_relationships"], ["bulk_gt_datalake", "bulk_irs_xml"], S)

# ------------------------------------------------------------------ charts
inst = pipe[pipe.funder_type.isin(["private_foundation", "community_foundation", "public_charity_grantmaker", "corporate_foundation", "federated_giving"])]
d = inst[inst.tier <= 2].sort_values("score").tail(30)
f, ax = style.fig(10.5, 9)
names = [n.title().replace("'S", "'s").replace(" Inc", "")[:46] for n in d.funder_name]
cols = [style.SERIES["government"] if t == 1 else style.SERIES["institutional"] for t in d.tier]
bars = ax.barh(names, d.score, color=cols, height=0.62)
for b_, s_, tr, tg in zip(bars, d.score, d.track, d.typical_grant):
    ax.annotate(f"{s_:.2f} · {tr.split(':')[-1].strip()} · typical {money(tg,'K')}", (s_, b_.get_y() + b_.get_height() / 2), xytext=(4, 0), textcoords="offset points", va="center", fontsize=7.5, color=style.TEXT_2)
from matplotlib.patches import Patch  # noqa: E402
ax.legend(handles=[Patch(color=style.SERIES["government"], label="Tier 1: pursue now"), Patch(color=style.SERIES["institutional"], label="Tier 2: cultivate 6-12 months")], loc="lower right")
ax.set_xlim(0, 1.0); ax.grid(axis="y", visible=False); ax.grid(axis="x", visible=True); ax.tick_params(axis="y", labelsize=8); ax.set_xlabel("Pipeline score (weights in config/scoring_weights.yaml)")
style.finish(f, ax, "m7_02_pipeline_scores",
             f"The scored pipeline puts {int((inst.tier==1).sum())} institutional funders in Tier 1: current partners to deepen, and peer funders reached by introduction",
             "chart_data/m5_00_candidate_funders.csv, m6_05_relationship_paths.csv, m4_00_funder_landscape_table.csv (from fact_grants, dim_funder, fact_org_relationships); scoring in config/scoring_weights.yaml",
             note="Score = weighted sum of mission fit, peer giving, regional giving, award size, accessibility, durability and relationship path. Closed funders (Clark) and channels are excluded from Tier 1. Core peers provisional.")
# score decomposition for Tier 1
d1 = inst[inst.tier == 1].sort_values("score")
f, ax = style.fig(10.5, 7)
left = np.zeros(len(d1)); names = [n.title().replace("'S", "'s").replace(" Inc", "")[:44] for n in d1.funder_name]
pal = {"mission_fit": style.SERIES["government"], "peer_giving": style.SERIES["institutional"], "regional_giving": style.SERIES["daf"], "award_size": style.SERIES["individuals"], "accessibility": style.SERIES["other"], "durability": "#8C8488", "relationship": style.GOLD}
for k in W:
    v = W[k] * d1[f"s_{k}"].values
    ax.barh(names, v, left=left, color=pal[k], height=0.62, label=k.replace("_", " "), edgecolor="white", linewidth=0.8); left += v
ax.set_xlim(0, 1); ax.grid(axis="y", visible=False); ax.grid(axis="x", visible=True); ax.legend(loc="lower right", ncol=2, fontsize=8); ax.tick_params(axis="y", labelsize=8)
style.finish(f, ax, "m7_03_tier1_score_breakdown",
             "Tier 1 scores are driven by peer giving and existing relationships; award size separates the foundations that can move Calvary's numbers",
             "chart_data/m7_00_funder_pipeline.csv; weights in config/scoring_weights.yaml")

print(pipe[pipe.tier <= 2][["rank", "funder_name", "track", "tier", "score", "typical_grant", "peers_funded", "relationship_path"]].head(45).to_string())
print(pipe.groupby(["track", "tier"]).size())
n1 = int((pipe.tier == 1).sum()); n1i = int((inst.tier == 1).sum())
register_insight("M7-01", "M7", f"The scored pipeline has {len(pipe)} rows: {n1} Tier 1 (pursue now), {int((pipe.tier==2).sum())} Tier 2, {int((pipe.tier==3).sum())} Tier 3. Tier 1 institutional targets ({n1i}): " + ", ".join(inst[inst.tier==1].funder_name.str.title().str.replace(" Inc", "", regex=False)) + ".",
                 "recommendations/funder_pipeline.csv", ["m7_02_pipeline_scores", "m7_03_tier1_score_breakdown"], ["fact_grants", "dim_funder", "fact_org_relationships", "supp_crm_cash_verification", "fact_opportunities"], f"{n1} Tier 1", "medium",
                 "Weights are editable in config/scoring_weights.yaml; the ranking is a starting point for the development team's judgment, not a verdict on any funder.", "both")
log(S, [f"pipeline {len(pipe)} rows; tiers {pipe.tier.value_counts().to_dict()}; action plan {len(plan)} rows", "charts m7_02, m7_03 written"])
