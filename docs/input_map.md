# Input map (Prompt 2)

Written 2026-10-10 at CP1; moved to `docs/` on 2026-10-12, when the client template moved to `calvary_funding_data/inputs/` and the root copies of Calvary's documents (identical to those in `inputs/`) were removed. Paths are relative to the project root (the folder holding `calvary_funding_data/` and `calvary_analysis/`). Every input the Prompt 2 brief describes was found; nothing is missing.

| Input | Actual path | What was found | Missing / ambiguous |
|---|---|---|---|
| Project README | `calvary_funding_data/README.md` | Data model, conventions, universes, caveats, rebuild steps, "Start here" list | Analysis-outputs section added by Prompt 2 (see `calvary_analysis/README.md`) |
| Clean tables | `calvary_funding_data/clean/*.csv` | 25 UTF-8 CSVs, 1.9 GB: `dim_org`, `dim_funder`, `dim_universe_membership`, `dim_period`, `dim_geo`, `dim_program_area`, `dim_person`, `entity_aliases`, `ref_ntee_codes`, `fact_org_financials`, `fact_grants`, `fact_gov_awards`, `fact_opportunities`, `fact_policy_events`, `fact_roles`, `fact_org_relationships`, `candidate_interlocks`, 7 `supp_*` tables | `fact_grants` (567 MB) and `fact_org_relationships` (101 MB) need `usecols` |
| Data dictionary | `calvary_funding_data/clean/data_dictionary.csv` | 542 rows: table, column, type, definition, allowed values, sources | — |
| Source registry | `calvary_funding_data/sources/source_registry.csv` | 238 `source_id`s with URL/file, publisher, retrieved date, license | — |
| API catalog | `calvary_funding_data/sources/api_catalog.md`, `api_catalog.csv`, `catalog_parts/` | 65 sources probed, status, coverage, limits | — |
| Data quality report | `calvary_funding_data/reports/data_quality.md` | Row counts, null rates, duplicate keys, Calvary reconciliation, CRM verification, unmatched names, person matching, gaps, portability | `entity_aliases` listed twice with different counts (see reconciliation) |
| Data inventory report | `calvary_funding_data/reports/data_inventory.md` | Counts per universe, table and source | — |
| Analysis notes | `calvary_funding_data/notes_for_analysis.md` | 9 sections of observations and leads | Placeholder-grant figure stale (see reconciliation) |
| Open questions | `calvary_funding_data/open_questions.md` | Part A assumptions A1–A5 and others; Part B questions for Calvary; Part C extensions | — |
| Build scripts | `calvary_funding_data/scripts/` (`00_setup.py` … `80_docs.py`, `lib/`) | Numbered pipeline; `run_all.sh` at the data-folder root | — |
| Requirements file | `calvary_funding_data/requirements.txt`; environment `calvary_funding_data/.venv/` (Python 3.12, pandas 3.0.6) | 36 pinned packages | Analysis packages added in `calvary_analysis/requirements.txt` |
| Raw data | `calvary_funding_data/raw/` | Present, 7.0 GB | Not needed for analysis |
| Build log | `calvary_funding_data/logs/build_log.md` | 6,760 lines, append-only, per-script sections with timestamps | — |
| Client template | `calvary_funding_data/inputs/2019 CalvaryPPT_White.pptx` | 4:3 deck (13.54 × 10.16 in), 6 placeholder slides, two logo PNGs (`ppt/media/image1.png` white background, `image2.png` gold chevron), theme colors plum `41242F`, gold `D39F28`, light gold `FFDD7F`, teal `52C5DA` / `B1E1E9` | No layouts worth reusing; Prompt 2 builds its own 16:9 design system around the logo and palette |
| Client data | `calvary_funding_data/inputs/` (30 files) | CRM export `Foundation & Corporate Funders_2023-2026.xlsx`; audits FY15–FY21, FY23; 990 PDFs TY2014–TY2019 and the ProPublica TY2024 render; annual reports FY15, FY17, FY18, FY20, FY21, FY23, FY24 at-a-glance; strategic plans 2016–19 and 2021–24 with reports; donor privacy policy; support-page printout | Copies of the same files also sit at the project root and in `pdf-data/`; `inputs/` is the canonical set |
| Supporting reports | `calvary_funding_data/reports/reviewer_guide.md`, `core_peers_proposal.md`, `universe_summary.md`, `calvary_financials_reconciliation.csv` | Trust guide with 6 self-checks; provisional peer rationale and alternates; universe rule counts | — |
| Config | `calvary_funding_data/config/` | `core_peers.csv` (18, provisional), `named_comparators.csv` (2), `universes.yaml`, `program_areas.yaml`, overrides, CPI, counties | — |
| API keys | `~/.config/calvary/keys.env` (outside the project) | Tavily, FAC, Census, DC MAR | Used only for the approved Tier 1 web pull in Phase 3 |

## Prompt 2 outputs

| Output | Path |
|---|---|
| Analysis workspace | `calvary_analysis/` (plan, log, discoveries, insight register, scripts, chart data, charts, modules, recommendations, storylines, decks, reports, checkpoints) |
| This map | `docs/input_map.md` |
| Memory reconciliation | `docs/memory_reconciliation.md` |
| The three engagement briefs | `docs/briefs/prompt_1_data_foundation.md`, `prompt_2_analysis_and_deliverables.md`, `prompt_3_audit_and_adversarial_review.md` |

## Prompt 3 outputs (independent review, 2026-10-10)

| Output | Path |
|---|---|
| Executive verdict, audit report, adversarial review, what holds up, minor notes | `calvary_analysis/reports/review/*.md` |
| Findings for the fix cycle (row by row) and coverage | `calvary_analysis/reports/review/review_findings.csv`, `review_coverage.csv` |
| Evidence (recomputation, traceability, consistency, guardrails, entities, external sources) and scripts | `calvary_analysis/reports/review/evidence/`, `calvary_analysis/reports/review/scripts/` |
