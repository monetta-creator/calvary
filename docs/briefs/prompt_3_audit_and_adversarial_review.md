# Prompt 3: Audit and Adversarial Review of the Calvary Women's Services Funding Survey

## Your role

You are an independent reviewer of a completed strategy engagement for **Calvary Women's Services**, a Washington, DC nonprofit serving women experiencing homelessness. Earlier sessions built a dataset (Prompt 1, in `calvary_funding_data/`) and produced analysis, recommendations, decks, and reports (Prompt 2, in `calvary_analysis/`). You had no part in that work, and that independence is your value.

Start from the project root `README.md`, then `input_map.md`, then `calvary_analysis/README.md`, and locate everything else from there. Read what was produced as an outside expert would: on the strength of what is on the page and in the data.

**Read the deliverables before the process files.** Form your first view from the one-pager, the leadership deck, the consulting deck, the reports and `insight_register.csv`. Only then read `checkpoints/`, `discoveries_log.md`, `analysis_log.md` and `analysis_plan.md`, so that the team's own account of its choices does not shape your cold read.

This prompt replaces Phase 6 of Prompt 2. The fix step that Prompt 2 describes (fix every issue, mark register rows `verified`) happens **after** this review, in a separate approved step, not here.

## Philosophy

**The work earns trust by surviving scrutiny.** Your job is to determine, accurately, whether and where it breaks. A clean result is a valid and valuable result: confirming that the work holds up gives the team confidence to present it. Report the problems that exist, at their true severity, and report nothing you would have to stretch to find.

**Materiality is the bar.** A finding belongs in the main review only if it could change a number Calvary relies on, a conclusion, a recommendation, or a decision. Everything below that bar (style, wording, minor caveats) goes in a short "minor notes" list at the end. Before you start, write down what would count as material for this engagement, and hold yourself to it. At minimum, these are material:

- any number on the executive one-pager or in the leadership deck that is wrong or unsupported
- any change to Tier 1 or Tier 2 membership in `recommendations/funder_pipeline.csv`
- any change to the funding-pressure verdict or its rating
- any stress-test scenario whose loss moves by more than 10%
- a recommendation in the 90-day plan that Calvary cannot act on as written
- any breach of the people-data guardrails (automatically material, whatever its size)

**Show your coverage.** For every area, state what you checked and how deeply. "Recomputed from clean tables", "checked against chart data", "read for consistency" and "not checked" carry different weight, so label them distinctly, and record them in `review_coverage.csv` (below).

**Evidence decides.** Every conclusion should follow from data that can be traced, reproduced, and defended. Where it does, say so with confidence. Where it does not, say exactly what is missing.

**Be fair as well as hard.** Distinguish a fatal flaw from a caveat, and a wrong conclusion from a debatable one. Credit what holds up so the team knows what it can stand behind.

**Judge honesty, not softness.** The leadership materials are deliberately humble and recommendation-led: this is pro bono work for an organization that did not commission a critique. Do not flag that framing as understating risk. The test is whether every cloud on the horizon is stated plainly somewhere in the leadership deck and the one-pager, and whether the consulting materials carry the full picture.

**Calvary's decisions are the stakes.** Leadership will make funding choices from this work: which funders to approach first, what reserve to hold, whether to expand into adjacent program areas, how to prepare for a lost or cut government stream. Weight every issue by how much it could change those choices.

## Known caveats (not new findings)

The team has already disclosed these. Verify that each is stated where it should be, and test whether the disclosure is adequate, but do not report them as discoveries:

1. Three open flags rest on documents only Calvary can provide (`discoveries_log.md` D1–D3): FY24–25 audits and TCP subgrant agreements, the Sisters Rise/EHV status, and the FY25 event calendar.
2. The 18 core peers are provisional (`calvary_funding_data/reports/core_peers_proposal.md`); nobody at Calvary has reviewed the set.
3. FY24–25 government share rests on 990 line 1e, treated as audit-equivalent because line 1e matched the audits in FY22–23.
4. The DHS/TCP contract has one public year (FY2024), carried forward.
5. TY2024 grant filings are partial and TY2025 mostly unfiled, so private trends after TY2023 are partly filing lag.
6. Corporate giving without a public filing is CRM-documented and cash-unverified.

## Two passes

Run the audit first. The adversarial review should build on numbers you have confirmed.

### Pass 1: Audit. Is the work correct?

Determine whether the numbers are right, reproducible, and traceable to real sources; whether entity and board-interlock matches can be trusted; and whether the people data stays within its guardrails.

**1a. Reproducibility.** Follow `calvary_analysis/README.md` "How to rerun": `scripts/00_env_check.py`, every module script, `scripts/lib/trace.py`, `scripts/lib/headline_check.py` against each deck and spine. Regenerate `chart_data/` into a scratch directory and diff it against the committed CSVs. Report every script that fails and every CSV that differs. Do not overwrite the committed outputs.

**1b. Independent recomputation.** Recompute from `calvary_funding_data/clean/` with your own code, not by re-reading `chart_data/`. Coverage targets:

- 100% of the numbers on the executive one-pager and in the leadership deck
- 100% of the stress-test table, from `config/scenarios.yaml` and the award base
- every Tier 1 and Tier 2 score in `funder_pipeline.csv`, from `config/scoring_weights.yaml` and the evidence columns
- a 25% sample of the consulting deck's data slides, chosen to cover every module M1–M10
- a 10% sample of appendix table cells
- the sanity checks in `calvary_funding_data/reports/reviewer_guide.md` §4

Check these conventions in particular, because an error in any of them would move headline numbers: government share on the audit basis (audited government ÷ audited revenue, FY13–23) with the 990 line 1e only for FY24–25; one source per government stream in `fact_gov_awards` (never summed across `source_type`); CoC competition year t mapped to Calvary FY t+1; non-cumulative grant rows only; landscape exclusions in `config/landscape_exclusions.csv` applied; DAF sponsors reported separately from institutional funders; aggregation on `funder_id`/EIN, never on raw funder name.

**1c. Traceability.** For a sample of 40 numbers across decks and reports, follow the chain: slide or paragraph → chart ID in the footnote → `chart_data/<id>.csv` → `source_tables` and `source_ids` → `calvary_funding_data/sources/source_registry.csv` or `calvary_analysis/sources/source_registry_extension.csv` → the public document. Record where the chain breaks.

**1d. Consistency.** Compare every number that appears in more than one place (one-pager, both decks, appendices, four reports, two readouts, `insight_register.csv`, module readouts). Report every disagreement.

**1e. Entity and interlock matches.** Test a sample of funder-to-grant matches in `fact_grants` and `entity_aliases` for false positives, with attention to funders with multiple raw spellings. Check `candidate_interlocks` and the shared-board rows used in M6: does the confidence label match the evidence, and do medium-confidence links appear only in consulting and appendix materials, labeled as unconfirmed?

**1f. People-data guardrails (mechanical, 100% coverage).** Compare every deck, report, readout, CSV and Markdown file in `calvary_analysis/` against `dim_person.name_display` and confirm no personal name of a private individual appears (organizational roles and `person_id` only). Grep all outputs for absolute paths, home-directory strings and usernames. Confirm no API key or key-file content appears anywhere.

**1g. Headlines and claims.** For each deck, test whether each headline follows from the evidence on its slide and whether the headlines alone, read in order, tell the deck's story. Flag claims that overstate what the data supports and caveats that are missing where a reader would need them.

### Pass 2: Adversarial review. Is the work right?

Challenge the funding-pressure verdict, the key findings, and the recommendations. Consider alternative explanations, what a skeptical board member, foundation program officer, or senior consulting partner would push back on, opportunities the pipeline missed or underrated, and whether Calvary can realistically execute the Tier 1 recommendations.

**2a. Judgment calls to attack.** The team made these choices; test each for whether a defensible alternative changes a material number:

- the verdict's weighting of channel concentration and liquidity over the headline government share
- treating line 1e as audit-equivalent for FY24–25
- the award-ceiling alignment (CoC lagged one year, DHS FY2024 carried forward) and the "recognized vs ceiling" gap
- scenario construction: apportionment by ceiling share, the 50% cost-avoidance assumption, the chosen severities
- the one-source-per-stream rule
- the Gates and TCP landscape exclusions
- T. Rowe Price scored as a DAF channel rather than a funder, and the exclusion of DAF channels from the pipeline
- the scoring weights and tier cutoffs (rerun with your own alternative weights and report what moves)
- the provisional peer set (swap three peers for alternates from `core_peers_proposal.md`, rerun M3/M5/M7, and report what moves)
- guideline rows with no usable web hit, and the first-party / third-party / analyst-note basis labels in `config/guideline_notes.csv`
- filing lag in TY2024 and its effect on "lapsed" and "gap" funders

**2b. Execution realism.** For each Tier 1 target and 90-day action: is the ask size in line with the funder's median grant to peers, does the application cycle in `guideline_notes.csv` fit the 90-day deadline, is the named owner role plausible for a fundraising team held at its current size (`supp_calvary_strategic_targets`), and does the relationship path exist in the data or only in hope?

**2c. Missed or underrated opportunities.** Look for funders, public streams or program areas the pipeline excluded or scored low that a program officer would name first. Say why the scoring missed them and whether the fix is a weight, a data gap or a judgment.

**2d. External reality check (bounded).** The analysis is public-records-only as of 2026-10-10. You may use the web to test time-sensitive claims that a skeptical reader would raise: the remaining life of GWCF's Health Equity Fund, the 2025 HUD CoC NOFO direction, the Emergency Housing Voucher sunset, the FY2027 OVSJG line, and the actual process at the Tier 1 foundations. Log every page you rely on in the format of `calvary_analysis/sources/source_registry_extension.csv` (in your own review file, not by editing theirs). Never put personal identifiers, Calvary's contacts, or the user's identity in any search or request. Do not pull new bulk data.

**2e. Alternative stories.** Write the strongest one-paragraph case for each of: (i) the pressure is lower than stated, (ii) the pressure is higher than stated, (iii) the pipeline is pointed at the wrong funders. Then say which, if any, the evidence supports.

## Outcomes

Write everything to `calvary_analysis/reports/review/`:

1. **`audit_report.md`** — each deliverable rated *verified*, *verified with caveats*, or *failed*, with the evidence behind each rating and an overall judgment of how far the numbers can be trusted. Include the reproducibility and diff results, the traceability sample, and the guardrail scan.
2. **`adversarial_review.md`** — material challenges ranked by their potential impact on Calvary's decisions. For each: the claim being challenged, the challenge, the evidence, your confidence that the challenge is correct, and a proposed fix. If no challenges meet the materiality bar, state that directly and explain what you tested. End with the three alternative stories and your ruling.
3. **`what_holds_up.md`** — a short list of the findings and recommendations that survived review and can be presented with confidence, each tied to its `insight_id`.
4. **`executive_verdict.md`** — one page stating whether the work is ready for the board, ready with specific fixes, or needs rework, and why.
5. **`review_coverage.csv`** — columns `area, deliverable, check, depth (recomputed | checked against chart data | read | not checked), result, notes`.
6. **`review_findings.csv`** — columns `finding_id, pass, severity (material | minor), deliverable, location, claim, issue, evidence, confidence, proposed_fix, insight_ids`. This is the file the fix cycle works from, row by row.
7. **`minor_notes.md`** — everything below the materiality bar.

Add the folder to `calvary_analysis/README.md` (append-only) and to `input_map.md`. Touch nothing else.

## Ground rules

- Review only. **Change no existing deliverable, script, config or data file.** Propose fixes and stop for my approval. The only permitted edits are the two append-only README/input-map additions above.
- When you find something material mid-review, flag it to me right away in one line, then continue.
- Use subagents where independent checks can run in parallel (recomputation by module, the guardrail scan, the traceability sample). Give each one file paths and a precise check, never personal identifiers or the user's identity. Require deterministic output (sorted, reproducible) and one owner per output file. Keep the judgment and final synthesis in this session.
- Scratch work (regenerated chart data, recomputation scripts) goes in a scratch directory, not in the project. If you keep your recomputation scripts, put them in `calvary_analysis/reports/review/scripts/` with relative paths.
- Do not rebuild or re-pull the Prompt 1 data. API keys live in `~/.config/calvary/keys.env`, sourced per command and never printed or written.
- The work moves between machines: Markdown and CSV only, relative paths, no usernames or absolute paths.
- Prompt 1 and Prompt 2 documents, including the checkpoint memos, stay as written.

## Recommended setup

Start a fresh session with no history from the authoring work. Run Pass 1 on Opus 5.5 and Pass 2 on Fable 5.1 at high effort, ideally in separate sessions so the adversary starts from the audited record: Pass 2 begins by reading `audit_report.md` and `review_findings.csv`. Check available skills first and use any that fit this review (the pptx skill's `validate.py` and `markitdown` for reading decks are the expected tools).

After both passes, the fix step runs in a session that has the Prompt 2 context: apply the approved fixes from `review_findings.csv`, record each fix against its `finding_id`, mark `insight_register.csv` rows `verified`, and return the fixed items to the review session for a short re-verification pass on those items only.
