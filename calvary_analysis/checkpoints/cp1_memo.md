# CP1 memo: analysis plan (confirmed 2026-10-10)

Plan approved in plan mode with all six defaults. Files written as approved:

| File | Path |
|---|---|
| Input map | `input_map.md` (project root) |
| Memory reconciliation | `memory_reconciliation.md` (project root) |
| Analysis plan | `calvary_analysis/analysis_plan.md` |
| Analysis log | `calvary_analysis/analysis_log.md` |
| Discoveries log | `calvary_analysis/discoveries_log.md` (empty; first flags will come from M1/M2) |
| Insight register | `calvary_analysis/insight_register.csv` (header only) |
| Shared helpers | `calvary_analysis/scripts/lib/common.py` (paths, loaders, chart-data manifest, register, log) |
| Environment check | `calvary_analysis/scripts/00_env_check.py` |
| Pinned requirements | `calvary_analysis/requirements.txt` (Prompt 1 pins + matplotlib 3.11.2, networkx 3.7, python-pptx 1.0.2, markitdown 0.1.8, pyyaml 6.0.3) |
| Deck toolchain | `calvary_analysis/decks/package.json` (pptxgenjs, sharp, react-icons) |

## Input map summary
All 15 inputs found; raw/ (7.0 GB) present; same machine as Prompt 1. Client template is 4:3 with a usable logo and palette (plum `41242F`, gold `D39F28`, teal `52C5DA`) and nothing else.

## Memory reconciliation summary
8 items, 0 High, 1 Medium (placeholder "see attached" grants: $3.2B/476 returns in memory and Prompt 1 docs vs $3.5B/667 rows/627 funder-years in the tables; analysis uses the table figure, Prompt 1 docs left untouched), 7 Low. Rulings recorded in `memory_reconciliation.md`.

## Environment check
All 25 clean tables load; pandas row counts match `data_quality.md`; the six reviewer-guide self-checks pass (FY25 revenue, DWC FY2024 revenue, FY23 SEFA, OVSJG FY2026, Ward 8 poverty, Cafritz TY2024). One lesson logged: two tables have quoted line breaks, so row counts must come from pandas, not `wc -l`.

**Still missing:** LibreOffice (visual QA in Phase 5). Install: `brew install --cask libreoffice`, then `/Applications/LibreOffice.app/Contents/MacOS/soffice`.

## What the data supports, modules, signals, gaps
See `analysis_plan.md` §3–§5. Ten modules (M1 trajectory, M2 exposure and stress test, M3 peers, M4 landscape, M5 gaps, M6 network, M7 pipeline, M8 expansion scan, M9 need/capacity, M10 comparator profiles).

## Open data gaps carried forward
1. No FY24/FY25 audits: government share for those years is line 1e plus a reconstructed stream estimate.
2. DHS/TCP contract values public for FY2024 only.
3. TY2024 grants partially filed; TY2025 mostly unfiled.
4. Only one high-confidence Calvary board interlock; relationship paths will be funder-sharing paths.
5. Grants.gov feed is mostly irrelevant for Calvary's model; the pipeline leans on DC and private funders.

## Decisions taken (defaults)
Keep 18 provisional peers; medium interlocks as "unconfirmed" in consulting materials only; approved small Tavily pull for Tier 1 targets in Phase 3; Prompt 1 docs untouched; outputs in `calvary_analysis/`; scenario levels OVSJG −10/−25%, CoC −15%/one project lost, DHS non-renewal, combined.

## Next
Phase 2 starts on acknowledgement: design system first, then M1–M10 with flags as they arise. No stop until CP2.
