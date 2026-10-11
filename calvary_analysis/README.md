# Calvary Women's Services: funding analysis (Prompt 2)

This folder holds the analysis, recommendations and deliverables built on the Prompt 1 data foundation in `../calvary_funding_data/`. Two questions anchor it: how much pressure Calvary's reliance on government funding creates, and which other funding fits its mission now or with a plausible expansion. Data as of 2026-10-10. All paths are relative; everything is Markdown, CSV, PNG or PPTX.

## Start here
1. `../input_map.md` and `../memory_reconciliation.md` (project root): inputs and the eight reconciled memory-vs-file differences.
2. `analysis_plan.md` (approved at CP1), `checkpoints/cp1_memo.md`, `cp2_memo.md`, `cp3_memo.md`.
3. `reports/executive_summary.md` → `recommendations/funding_pressure_verdict.md` → `recommendations/strategic_recommendations.md`.
4. `insight_register.csv` (36 findings, confidence and verification status) and `discoveries_log.md` (flags D1–D3 and their resolutions).
5. `reports/consulting_briefing.md` for how to pick the work up.

## Folder map
```
analysis_plan.md, analysis_log.md, discoveries_log.md, insight_register.csv
config/            scenarios.yaml (stress test), scoring_weights.yaml (pipeline), expansion_areas.yaml, landscape_exclusions.csv,
                   guideline_notes.csv (web pull, reviewed), png_data_map.csv (PNG -> chart data)
scripts/           00_env_check.py; 01..10 module scripts (M1-M10); 11 web pull; 12 merge guidelines; 13 sensitivity; lib/ (common, style, trace, headline_check)
chart_data/        one CSV per chart with source_tables and source_ids columns; _manifest.csv (chart id -> title, sources, script)
charts/            PNG charts, 200 dpi, one visual system (storylines/design_system.md)
modules/           one readout per module (question, method, findings, charts, caveats, confidence)
recommendations/   funding_pressure_verdict.md, strategic_recommendations.md, funder_pipeline.csv, action_plan_90day.csv
storylines/        design_system.md, leadership_* and consulting_* storylines and headline spines, appendix_headline_spine.md
decks/             build_*.js (pptxgenjs), theme.js, lib/deck.js, assets/ (logo), *.pptx, qa/ (rendered slide images)
reports/           executive_one_pager.md, executive_summary.md, full_findings.md, methodology.md, recommendations.md,
                   board_readout.md, consulting_briefing.md, review_report.md (Phase 6)
sources/           web_tier1_guidelines.csv (Tavily hits), source_registry_extension.csv (web guideline pages)
checkpoints/       CP1-CP3 memos
```

## Modules
| Module | Script | Readout | Charts |
|---|---|---|---|
| M1 Calvary trajectory | `01_m1_trajectory.py` | `modules/m1_calvary_trajectory.md` | m1_01–m1_08 |
| M2 Government exposure and stress test | `02_m2_exposure.py` (+ `config/scenarios.yaml`) | `m2_government_exposure.md` | m2_01–m2_07 |
| M3 Peer benchmarking | `03_m3_peers.py` | `m3_peer_benchmarking.md` | m3_00–m3_09 |
| M4 Funder landscape | `04_m4_landscape.py` (+ `landscape_exclusions.csv`) | `m4_funder_landscape.md` | m4_00–m4_08 |
| M5 Funder gaps | `05_m5_gaps.py` | `m5_funder_gaps.md` | m5_00–m5_06 |
| M6 Network | `06_m6_network.py` | `m6_network.md` | m6_01–m6_05 |
| M7 Pipeline and scoring | `07_m7_pipeline.py`, `12_merge_guidelines.py`, `13_m7_sensitivity.py` (+ `scoring_weights.yaml`, `guideline_notes.csv`) | `m7_pipeline.md` | m7_00–m7_05 |
| M8 Mission expansion | `08_m8_expansion.py` (+ `expansion_areas.yaml`) | `m8_expansion_scan.md` | m8_01–m8_02 |
| M9 Need and capacity | `09_m9_need_capacity.py` | `m9_need_capacity.md` | m9_01–m9_05 |
| M10 Named comparators | `10_m10_profiles.py` | `m10_comparator_profiles.md` | m10_01–m10_05 |

## Deliverables
- **Executive one-pager:** `decks/executive_one_pager.pptx` and `reports/executive_one_pager.md`.
- **Leadership and board deck:** `decks/leadership_deck.pptx` (22 content slides plus five section dividers; spine `storylines/leadership_headline_spine.md`).
- **Consulting deck:** `decks/consulting_deck.pptx` (55 content slides plus dividers and table continuations; spine `storylines/consulting_headline_spine.md`).
- **Appendix decks:** `decks/appendix_A_calvary_government.pptx`, `appendix_B_peers_comparators.pptx`, `appendix_C_funders_pipeline.pptx`, `appendix_D_data_methods.pptx` (spines in `storylines/appendix_headline_spine.md`; method notes A1–D3 in D and in `reports/methodology.md`).
- **Reports:** executive summary, full findings, methodology, recommendations; board readout talking points; consulting team briefing.

## How to rerun
```sh
V=../calvary_funding_data/.venv/bin/python        # Python 3.12 env from the data build
uv pip install --python $V -r requirements.txt     # pinned (adds matplotlib, networkx, python-pptx, markitdown, pyyaml)
$V scripts/00_env_check.py                         # tables load, row counts match, six self-checks
for s in 01_m1_trajectory 02_m2_exposure 03_m3_peers 04_m4_landscape 05_m5_gaps 06_m6_network 07_m7_pipeline 08_m8_expansion 09_m9_need_capacity 10_m10_profiles 12_merge_guidelines 13_m7_sensitivity; do $V scripts/$s.py; done
$V scripts/lib/trace.py                            # chart -> CSV -> registry chain
cd decks && npm install && NODE_PATH=$PWD/node_modules PPTX_SKILL_APPLY_THEME=<pptx-skill>/scripts/apply_theme.js node build_leadership.js   # and the other build_*.js
$V ../scripts/lib/headline_check.py leadership_deck.pptx ../storylines/leadership_headline_spine.md
```
`11_web_tier1_guidelines.py` needs `TAVILY_API_KEY` in the environment and is only rerun to refresh the guideline hits; its reviewed output is `config/guideline_notes.csv`. Rendering for visual QA: `soffice --headless --convert-to pdf deck.pptx` then `pdftoppm -jpeg`.

## Where to change things
- **Scoring weights and tiers:** `config/scoring_weights.yaml`, then rerun 07, 12, 13.
- **Stress-test scenarios:** `config/scenarios.yaml`, then rerun 02.
- **Core peers (provisional):** `../calvary_funding_data/config/core_peers.csv`, rerun `../calvary_funding_data/scripts/20_build_universes.py`, then 03, 05, 06, 07.
- **Landscape exclusions, expansion distances, guideline notes:** the files in `config/`.
- **Design system:** `storylines/design_system.md` (charts: `scripts/lib/style.py`; decks: `decks/theme.js`, `decks/lib/deck.js`).

## Traceability and sourcing
Every chart ID maps to `chart_data/<id>.csv`, whose `source_ids` map to `../calvary_funding_data/sources/source_registry.csv` (plus `sources/source_registry_extension.csv` for the web guideline pages); PNG-only charts map through `config/png_data_map.csv`. Every data slide carries a footnote with the source, the method and the chart ID (design system, sourcing rule). Core peers are provisional; FY24–25 government figures rest on the 990 until Calvary's audits are shared; see `reports/methodology.md` §9 for all limitations.

## Independent review (Prompt 3, 2026-10-10)
`reports/review/` holds the independent audit and adversarial review that replaces Phase 6: `executive_verdict.md` (one page: ready for the board after specific fixes), `audit_report.md` (ratings per deliverable, reproducibility and diff results, traceability sample, guardrail scan), `adversarial_review.md` (material challenges ranked by their effect on Calvary's decisions, judgment calls tested, execution realism, external check, three alternative stories and the ruling), `what_holds_up.md` (findings and recommendations that survived, by insight id), `review_findings.csv` (one row per finding, R01–R18 material and M01–M13 minor; the fix cycle works from this file), `review_coverage.csv` (what was checked and how deeply), `minor_notes.md`, `evidence/` (recomputation CSVs, traceability sample, consistency matrix, guardrail and entity reports, external sources in registry-extension format) and `scripts/` (recomputation code; paths resolve from the project root). Nothing else in this folder was changed by the review; `reports/review_report.md` named above does not exist and is superseded by this folder.
- 2026-10-10, after the review: at the engagement lead's request the seven decks were rebuilt with an 18 pt hanging indent on every bullet style (`decks/lib/deck.js`; text unchanged, validator and headline checks pass) and exported to `decks/pdf/*.pdf` with LibreOffice. The PDFs render the native charts; Quick Look and Keynote import do not.
