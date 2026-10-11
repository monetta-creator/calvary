"""Merge the hand-reviewed guideline notes (config/guideline_notes.csv, built from the Tavily hits in
sources/web_tier1_guidelines.csv) into the pipeline and the 90-day plan."""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import ANALYSIS, log, save_chart_data  # noqa: E402

S = "12_merge_guidelines"
notes = pd.read_csv(ANALYSIS / "config" / "guideline_notes.csv", dtype=str).fillna("")
pipe = pd.read_csv(ANALYSIS / "recommendations" / "funder_pipeline.csv", dtype={"funder_id": str})
plan = pd.read_csv(ANALYSIS / "recommendations" / "action_plan_90day.csv")
for c in ["application_process", "next_deadline_or_cycle", "guidelines_url", "guidelines_basis"]:
    if c in pipe.columns:
        pipe = pipe.drop(columns=c)
m = notes.rename(columns={"basis": "guidelines_basis"})[["funder_id", "application_process", "next_deadline_or_cycle", "guidelines_url", "guidelines_basis"]]
pipe = pipe.merge(m, on="funder_id", how="left")
pipe.to_csv(ANALYSIS / "recommendations" / "funder_pipeline.csv", index=False)
save_chart_data(pipe, "m7_00_funder_pipeline", "Scored and tiered funder pipeline with application-process notes (config/scoring_weights.yaml; config/guideline_notes.csv)",
                ["fact_grants", "dim_funder", "fact_org_relationships", "supp_crm_cash_verification", "fact_opportunities", "fact_gov_awards"],
                ["bulk_gt_datalake", "bulk_irs_xml", "input_crm_funders_2023_2026", "api_grantsgov"], S, "guideline notes from the approved web pull (sources/web_tier1_guidelines.csv), reviewed by the analyst")
plan = plan.merge(pipe[["funder_name", "application_process", "next_deadline_or_cycle", "guidelines_url"]], on="funder_name", how="left")
plan.to_csv(ANALYSIS / "recommendations" / "action_plan_90day.csv", index=False)
save_chart_data(plan, "m7_01_action_plan_90day", "90-day action plan for Tier 1 targets, with application notes", ["fact_grants", "dim_funder", "fact_org_relationships"], ["bulk_gt_datalake", "bulk_irs_xml"], S)
save_chart_data(notes, "m7_04_guideline_notes", "Application process and deadlines for Tier 1-2 institutional funders (web pull, analyst-reviewed)", [], [f"web_guidelines_{f}" for f in notes.funder_id if f], S,
                "basis column: web (first-party) / web (third-party) / no usable hit; analyst note")
print(pipe[pipe.tier <= 2][["funder_name", "tier", "next_deadline_or_cycle", "guidelines_basis"]].head(40).to_string())
log(S, [f"guideline notes merged for {notes.funder_id.ne('').sum()} funders; pipeline and action plan updated"])
