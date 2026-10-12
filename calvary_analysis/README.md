# Calvary Women's Services: funding analysis (Prompt 2)

This folder holds the analysis, recommendations and deliverables built on the Prompt 1 data foundation in `../calvary_funding_data/`. Two questions anchor it: how much pressure Calvary's reliance on government funding creates, and which other funding fits its mission now or with a plausible expansion. Data as of 2026-10-10. All paths are relative; everything is Markdown, CSV, PNG or PPTX.

## Start here
1. `../input_map.md` and `../memory_reconciliation.md` (project root): inputs and the eight reconciled memory-vs-file differences.
2. `analysis_plan.md` (approved at CP1), `checkpoints/cp1_memo.md`, `cp2_memo.md`, `cp3_memo.md`.
3. `reports/executive_summary.md` → `recommendations/funding_pressure_verdict.md` → `recommendations/strategic_recommendations.md`.
4. `insight_register.csv` (36 findings, confidence and verification status, all `verified` after the 2026-10-11 fix cycle) and `discoveries_log.md` (flags D1–D3; D3 closed).
5. `reports/consulting_briefing.md` for how to pick the work up, and `../CLAUDE.md` for the house rules and how an analyst approaches a new request (project skills in `../.claude/skills/`: `new-deck`, `calvary-data`).

## Folder map
```
analysis_plan.md, analysis_log.md, discoveries_log.md, insight_register.csv
config/            scenarios.yaml (stress test), scoring_weights.yaml (pipeline weights, tiers, channels, status rules), expansion_areas.yaml,
                   landscape_exclusions.csv, grant_exclusions.csv (mis-attributed grant rows), guideline_notes.csv (web pull, reviewed,
                   with open_status per funder), png_data_map.csv (PNG -> chart data)
scripts/           00_env_check.py; 01..10 module scripts (M1-M10); 11 web pull; 12 merge guidelines; 13 sensitivity; lib/ (common, style, trace, headline_check, full_findings)
chart_data/        one CSV per chart with source_tables and source_ids columns; _manifest.csv (chart id -> title, sources, script)
charts/            PNG charts, 200 dpi, one visual system (storylines/design_system.md)
modules/           one readout per module (question, method, findings, charts, caveats, confidence)
recommendations/   funding_pressure_verdict.md, strategic_recommendations.md, funder_pipeline.csv, action_plan_90day.csv
storylines/        design_system.md, audiences.md (who reads what), leadership_* and consulting_* storylines and headline spines, appendix_headline_spine.md
decks/             build_*.js (pptxgenjs), build_all.sh (one-command rebuild + checks), theme.js, lib/ (deck.js, theme_colors.js), assets/ (logo),
                   *.pptx (editable source), pdf/ (the deliverables), qa/ (rendered slide images)
web/               Calvary Grantmaker Web: build_network_page.py + network_page.template.html -> Calvary_Grantmaker_Web.html (self-contained,
                   d3 and fonts embedded from vendor/; download and double-click, works offline)
                   and publish/funder_network.html (an earlier claude.ai artifact copy; no longer republished)
reports/           executive_one_pager.md, executive_summary.md, full_findings.md (generated), methodology.md, recommendations.md,
                   board_readout.md, consulting_briefing.md; review/ (independent review, fix_spec.md, fix_log.md)
sources/           web_tier1_guidelines.csv (Tavily hits), source_registry_extension.csv (web guideline pages)
checkpoints/       CP1-CP3 memos
```

## Modules
| Module | Script | Readout | Charts |
|---|---|---|---|
| M1 Calvary trajectory | `01_m1_trajectory.py` | `modules/m1_calvary_trajectory.md` | m1_01–m1_08 |
| M2 Government funding and stress test | `02_m2_exposure.py` (+ `config/scenarios.yaml`) | `m2_government_exposure.md` | m2_01–m2_07 |
| M3 Peer benchmarking | `03_m3_peers.py` | `m3_peer_benchmarking.md` | m3_00–m3_09 |
| M4 Funder landscape | `04_m4_landscape.py` (+ `landscape_exclusions.csv`) | `m4_funder_landscape.md` | m4_00–m4_08 |
| M5 Funder gaps | `05_m5_gaps.py` | `m5_funder_gaps.md` | m5_00–m5_06 |
| M6 Network | `06_m6_network.py` | `m6_network.md` | m6_01–m6_05 |
| M7 Pipeline and scoring | `07_m7_pipeline.py`, `12_merge_guidelines.py`, `13_m7_sensitivity.py` (+ `scoring_weights.yaml`, `guideline_notes.csv`) | `m7_pipeline.md` | m7_00–m7_05 |
| M8 Mission expansion | `08_m8_expansion.py` (+ `expansion_areas.yaml`) | `m8_expansion_scan.md` | m8_01–m8_02 |
| M9 Need and capacity | `09_m9_need_capacity.py` | `m9_need_capacity.md` | m9_01–m9_05 |
| M10 Named comparators | `10_m10_profiles.py` | `m10_comparator_profiles.md` | m10_01–m10_05 |

## Deliverables
**Share the PDFs in `decks/pdf/`.** They are rendered from the PPTX files by LibreOffice and look the same in every viewer. The PPTX files are the editable source: their charts are native PowerPoint charts, which PowerPoint draws correctly but Keynote, Google Slides and Mac Quick Look do not (stacking, number formats and styling get lost). Edit the decks through `decks/build_*.js`, then rebuild the PPTX and PDF together.

- **Executive one-pager:** `decks/pdf/executive_one_pager.pdf` (source `decks/executive_one_pager.pptx`) and `reports/executive_one_pager.md`.
- **Leadership and board deck:** `decks/pdf/leadership_deck.pdf` (source `decks/leadership_deck.pptx`; 22 headline slides plus four section dividers; spine `storylines/leadership_headline_spine.md`).
- **Consulting deck:** `decks/pdf/consulting_deck.pdf` (source `decks/consulting_deck.pptx`; 66 slides: 55 headlines plus dividers and table continuations; spine `storylines/consulting_headline_spine.md`).
- **Appendix decks:** `decks/pdf/appendix_A_calvary_government.pdf`, `appendix_B_peers_comparators.pdf`, `appendix_C_funders_pipeline.pdf`, `appendix_D_data_methods.pdf` (sources are the matching `decks/*.pptx`; spines in `storylines/appendix_headline_spine.md`; method notes A1–D3 in D and in `reports/methodology.md`).
- **Reports:** executive summary, full findings, methodology, recommendations; board readout talking points; consulting team briefing.

## How to rerun
```sh
V=../calvary_funding_data/.venv/bin/python        # Python 3.12 env from the data build
uv pip install --python $V -r requirements.txt     # pinned (adds matplotlib, networkx, python-pptx, markitdown, pyyaml)
$V scripts/00_env_check.py                         # tables load, row counts match, six self-checks
for s in 01_m1_trajectory 02_m2_exposure 03_m3_peers 04_m4_landscape 05_m5_gaps 06_m6_network 07_m7_pipeline 08_m8_expansion 09_m9_need_capacity 10_m10_profiles 12_merge_guidelines 13_m7_sensitivity; do $V scripts/$s.py; done
$V scripts/lib/full_findings.py                    # regenerate reports/full_findings.md from the readouts and register
$V scripts/lib/trace.py                            # chart -> CSV -> registry chain; must print TRACE OK
$V web/build_network_page.py                       # Grantmaker Web page (reconciles to m6_01 before writing)
cd decks && npm install && ./build_all.sh          # all seven decks: PPTX, pdf/, qa/ images, headline check (or ./build_all.sh leadership)
cd .. && REVIEW_OUT=/tmp/guard $V reports/review/scripts/guardrail_scan.py   # before anything leaves the team; delete /tmp/guard after
```
Run the modules in this order: 07 without 12 drops the open-status columns from the pipeline. `11_web_tier1_guidelines.py` needs `TAVILY_API_KEY` and is only rerun to refresh the guideline hits; its reviewed output is `config/guideline_notes.csv`. `build_all.sh` needs Node, LibreOffice (`soffice`) and poppler (`pdftoppm`, `pdfinfo`); it no longer depends on any external skill. Reruns rewrite the `written` column of `chart_data/_manifest.csv` and append to `analysis_log.md`, so judge a rerun by `git diff chart_data/*.csv insight_register.csv`.

## Where to change things
- **Scoring weights, tiers, channels and next-step overrides:** `config/scoring_weights.yaml`, then rerun 07, 12, 13 and the web page.
- **A funder's open status** (open, invitation only, closed to new applicants, sunset, not eligible, channel): `config/guideline_notes.csv` with the source and date checked, then rerun 07, 12, 13 and the web page.
- **A mis-attributed grant** (for example a namesake organization in another city): add its `grant_id` to `config/grant_exclusions.csv`, then rerun all modules.
- **Stress-test scenarios:** `config/scenarios.yaml`, then rerun 02.
- **Core peers (provisional):** `../calvary_funding_data/config/core_peers.csv`, rerun `../calvary_funding_data/scripts/20_build_universes.py`, then 03, 05, 06, 07.
- **Landscape exclusions, expansion distances, guideline notes:** the files in `config/`.
- **Design system:** `storylines/design_system.md` (charts: `scripts/lib/style.py`; decks: `decks/theme.js`, `decks/lib/deck.js`). Audiences: `storylines/audiences.md`.

## Traceability and sourcing
Every chart ID maps to `chart_data/<id>.csv`, whose `source_ids` map to `../calvary_funding_data/sources/source_registry.csv` (plus `sources/source_registry_extension.csv` for the web guideline pages); PNG-only charts map through `config/png_data_map.csv`. Every data slide carries a footnote with the source, the method and the chart ID (design system, sourcing rule). Core peers are provisional; FY24–25 government figures rest on the 990 until Calvary's audits are shared; see `reports/methodology.md` §9 for all limitations.

## Independent review (Prompt 3, 2026-10-10)
`reports/review/` holds the independent audit and adversarial review that replaces Phase 6: `executive_verdict.md` (one page: ready for the board after specific fixes), `audit_report.md` (ratings per deliverable, reproducibility and diff results, traceability sample, guardrail scan), `adversarial_review.md` (material challenges ranked by their effect on Calvary's decisions, judgment calls tested, execution realism, external check, three alternative stories and the ruling), `what_holds_up.md` (findings and recommendations that survived, by insight id), `review_findings.csv` (one row per finding, R01–R18 material and M01–M13 minor; the fix cycle works from this file), `review_coverage.csv` (what was checked and how deeply), `minor_notes.md`, `evidence/` (recomputation CSVs, traceability sample, consistency matrix, guardrail and entity reports, external sources in registry-extension format) and `scripts/` (recomputation code; paths resolve from the project root). Nothing else in this folder was changed by the review; this folder replaces the Phase 6 `review_report.md` that was planned but never written.
- 2026-10-11, fix cycle: every finding was fixed and independently re-verified; `fix_spec.md` holds the canonical wording and numbers, `fix_log.md` records each change by finding ID, and `insight_register.csv` rows are marked `verified`.
- 2026-10-10, after the review: at the engagement lead's request the seven decks were rebuilt with an 18 pt hanging indent on every bullet style (`decks/lib/deck.js`; text unchanged, validator and headline checks pass) and exported to `decks/pdf/*.pdf` with LibreOffice. The PDFs render the native charts; Quick Look and Keynote import do not.
