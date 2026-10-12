---
name: calvary-data
description: Navigate the Calvary engagement's data and analysis pipeline without producing wrong numbers. Where each fact lives, how to compute a funding total, share or peer comparison safely, the traps that already caused errors, the rerun order, the QA gates, and the shell, rendering and subagent gotchas learned on this repo. Use before computing any number, writing a module script, pulling new data, or changing config in calvary_funding_data/ or calvary_analysis/.
---

# Calvary data: map, traps and tricks

Two folders. `calvary_funding_data/` (Prompt 1) is the data foundation: 25 clean tables, the source registry and the rebuild scripts. Do not edit it; it was rebuild-tested and reviewed. `calvary_analysis/` (Prompt 2) is everything built on top: module scripts, chart data, register, config, decks, reports, the web page. Python is `calvary_funding_data/.venv/bin/python` (3.12, pandas 3). Data as of 2026-10-10. Funder open status checked 2026-10-11.

## 1. Where things live

| You need | Look in | Notes |
|---|---|---|
| A finding already made | `calvary_analysis/insight_register.csv` | 36 rows, one per finding, with chart IDs, magnitude, confidence, status (`verified` after the fix cycle) |
| The number behind a chart | `calvary_analysis/chart_data/<chart_id>.csv` | Every row carries `source_tables` and `source_ids`. `_manifest.csv` lists every chart with title and script |
| How a module works | `calvary_analysis/modules/m<N>_*.md` | Question, method, findings, charts, caveats, confidence |
| Canonical wording after the review | `calvary_analysis/reports/review/fix_spec.md`, `fix_log.md` | Use these sentences for scenarios, events, percentiles, Tier 1, beds |
| What was wrong once | `calvary_analysis/reports/review/review_findings.csv` | R01–R18, M01–M13, N01–N03 |
| Column meanings | `calvary_funding_data/clean/data_dictionary.csv` and `calvary_funding_data/README.md` | The README has the long version of section 3 below |
| A source document | `calvary_funding_data/sources/source_registry.csv` (+ `calvary_analysis/sources/source_registry_extension.csv`) | Every `source_id` in chart data must exist here (`trace.py` checks) |
| Whether a funder takes requests | `calvary_analysis/config/guideline_notes.csv` `open_status` | open, invitation_only, rfp_only, closed_to_new, sunset, not_eligible, channel, unverified; with note, source and date checked |
| Who the peers are | `calvary_funding_data/config/core_peers.csv` (18, provisional), `named_comparators.csv` (DWC, CBWC/SheWorks) | `lib.common.peer_set()` returns Calvary + 18 + 2 with short names |

Key IDs: Calvary EIN `521307706` (FYE 30 Sept, Ward 8). DWC `311597223`. CBWC Empowerment Institute (runs SheWorks) `882046704`. TCP (The Community Partnership, DC's homeless intermediary) `521681401`. GWCF `237343119`.

## 2. How to get a number safely

1. Check the register and chart data first. Quote, don't recompute.
2. If you must compute: `from lib.common import load, CALVARY, peer_set` (with `sys.path` pointing at `calvary_analysis/scripts`). `load(table, usecols=[...])` keeps EINs as strings and drops the rows in `config/grant_exclusions.csv`. Always pass `usecols` for `fact_grants` (~930K rows) and `fact_org_relationships` (~544K).
3. Write chart data with `save_chart_data(df, chart_id, title, source_tables, source_ids, script)`. Record findings with `register_insight(...)`. Draw PNGs with `lib.style` and save through `style.finish()`, which applies the house chart style.
4. State the measure in the footnote: which line, which basis, which years.

## 3. Traps that produced wrong numbers before

**Measures**
- **Government share:** 990 line 1e understates it because contracts land in program revenue or line 1f (Calvary FY21: audit $1.98M vs line 1e $503K). Use the audit basis through FY23 and line 1e for FY24–25 (they matched in FY22–23). Peers are compared on line 1e only.
- **Sector percentile:** say which comparison set. Calvary is the 57th percentile among DC organizations that *report* government revenue, the 84th against all filers (a missing line counted as 0%). The review caught a method line that said the opposite.
- **Events:** event receipts are line 1c **plus** line 8a. The FY25 return moved the gala from 1c to 8a, so 1c alone shows a fake $483K collapse (review R15). Receipts were $596K (FY24) and $533K (FY25).
- **Beds:** the 6.8% share counts transitional beds only (94 of DC's TH beds). The 124 total spans TH, PSH and RRH. Never put "124 beds" and "6.8%" in one clause as if they share a base.
- **Nominal vs real:** $2.49M → $4.97M is nominal. +59% is after inflation ($3.05M → $4.84M in 2024 dollars).
- **Bases:** "78% of the $4.1M 2024 award base passes through TCP". Don't mix award years (OVSJG FY26 vs CoC FY2025 vs DHS FY2024) in one total.

**Sums and rows**
- **`fact_gov_awards`:** never sum across `source_type`. OVSJG awards, DC PASS payments and SEFA expenditures describe the same dollars. One source per stream.
- **`fact_grants`:** drop `cumulative_flag == 1` rows (CRM totals, "over the years" lists). Annual sums use `source_type` in `pf_grants_paid`, `schedule_i` only; `pf_grants_approved_future` would double-count.
- **"See attached" rows** (`placeholder_row=1` in `notes`): real grants with no grantee. Flag the funder; don't count them as grants to anyone.
- **Financials:** use `preferred == 1` rows (one per org and year). `conflict_flag` marks source disagreement.
- **Gala income on line 8a** is in `notes` as `fundraising_gross_income=`, not in its own column.

**Who counts as what**
- **DAF sponsors** (Fidelity, Benevity / American Online Giving Foundation, Schwab = "Donor Advised Charitable Giving", Vanguard, NPT, Blackbaud) are individual donors' money. Report them apart from institutional funders and never put them in a pipeline.
- **Channels are not grantmakers:** America's Charities (workplace giving, Calvary enrolled), JPMorgan Chase and Bank of America (matching gifts), Gifts for the Homeless and Capital Area Food Bank (in-kind), Give Lively (online platform), World Bank Community Connections Fund (employee giving), T. Rowe Price Program (DAF-like). Listed in `config/scoring_weights.yaml` `channels:`.
- **Closed or closing funders:** Clark Charitable Foundation spent down and closed on 31 Dec 2025. Its $32.8M to DC's sector inflates the 2020–24 landscape and gap totals. Venable and Meyer are closed to new applicants. Many Hands requires a budget under $5M (Calvary spent $5.58M). Check `open_status` before naming any funder.
- **One-time capital grants are not lapsed relationships** (World Bank CCF's $100K, TY2022).
- **Namesakes:** "My Sister's Place" exists in DC and Baltimore. Baltimore funders' grants to the Baltimore one were matched to the DC peer until `config/grant_exclusions.csv` removed them. Check city and state on surprising grants.
- **TCP** passes money through and files no itemized provider list, so DHS contract values exist only in DC's FY2024 oversight responses. Excluded from the landscape as an intermediary.
- **Funders of exactly three peers** depend on the provisional peer set: swapping three peers drops several of them. Label them, and confirm the peer set before outreach.

**Years**
- `tax_year` = the year the fiscal year begins; `fiscal_year` = the year it ends. Calvary's FY ends in September, DWC's in December, CBWC's in June. Label "FY25" for Calvary, "TY2024" for funders, "DC FY2026" for budgets.
- HUD CoC competition year t funds Calvary FY t+1. TY2024 filings are partial and TY2025 mostly unfiled, so recent private trends read low.

## 4. Rerun order and side effects

```sh
V=calvary_funding_data/.venv/bin/python; cd calvary_analysis
for s in 01_m1_trajectory 02_m2_exposure 03_m3_peers 04_m4_landscape 05_m5_gaps 06_m6_network 07_m7_pipeline \
         08_m8_expansion 09_m9_need_capacity 10_m10_profiles 12_merge_guidelines 13_m7_sensitivity; do $V scripts/$s.py; done
$V scripts/lib/full_findings.py      # regenerates reports/full_findings.md from readouts + register
$V scripts/lib/trace.py              # must print TRACE OK
$V web/build_network_page.py         # Grantmaker Web page; asserts it matches m6_01
cd decks && ./build_all.sh           # PPTX + PDF + QA images + headline check
```
- **Order matters.** 07 writes the pipeline, 12 merges guideline columns into it, 13 runs sensitivity. Running 07 without 12 silently drops the open-status columns from `funder_pipeline.csv`. 05 feeds 07, 06 feeds 07, 02 and 03 feed the decks.
- **Skip 11** (`11_web_tier1_guidelines.py`): it calls a paid search API and its reviewed output is already in `config/guideline_notes.csv`.
- **Noise in git:** every rerun rewrites the `written` timestamp in `chart_data/_manifest.csv` and appends to `analysis_log.md`. Judge a rerun by `git diff chart_data/*.csv insight_register.csv`, not by the manifest.
- **Register status:** a rerun keeps `verified` only if the finding, evidence and magnitude are unchanged. Change the text and it drops to `draft`, which is correct: it needs re-checking.
- **Determinism:** sort before taking "first" or de-duplicating. A set-ordered networkx subgraph once made the network layout change between runs.
- **The data foundation** (`calvary_funding_data/run_all.sh`) rebuilds `clean/` offline in about 20 minutes. Set `CALVARY_NO_NOTES=1` when rerunning one of its scripts, or it re-appends to the notes files. The two biggest tables are committed in parts; rejoin per `clean/_parts/REJOIN.md` after a fresh clone.

## 5. Config you will touch

| File | Controls | Rerun |
|---|---|---|
| `config/scoring_weights.yaml` | Pipeline weights, tiers, channels, next-step overrides, status rules | 07, 12, 13, web page |
| `config/guideline_notes.csv` | Application process and open status per funder | 07, 12, 13, web page |
| `config/grant_exclusions.csv` | Mis-attributed grant rows dropped on every load | all modules |
| `config/landscape_exclusions.csv` | Funders left out of the landscape (Gates, TCP) | 04–07 |
| `config/scenarios.yaml` | Stress-test cuts | 02 |
| `calvary_funding_data/config/core_peers.csv` | The 18 provisional peers | data build script 20, then 03, 05, 06, 07 |

## 6. QA gates

- `scripts/lib/trace.py`: chart ID → CSV → source registry, every PNG mapped, every chart ID mentioned in Markdown exists. Top-level `reports/*.md` are scanned, `reports/review/` is not.
- `scripts/lib/headline_check.py <deck.pptx> <spine.md> [--appendix=A..D]`: 20 words, no semicolons, titles match the spine in order. `decks/build_all.sh` runs it.
- `reports/review/scripts/guardrail_scan.py`: secrets, personal names and paths in every deliverable. **Always set `REVIEW_OUT` to a scratch folder**, or it writes its hit lists (including any names it finds) into `reports/review/evidence/`. Delete the scratch output afterwards. Its "person" hits are usually foundation names (for example a family foundation); its secret hits are usually env-var names.

## 7. Rendering and tooling gotchas

- **PDFs are the deliverable.** Native pptxgenjs charts render correctly in PowerPoint and LibreOffice, but Keynote, Quick Look, Google Slides and VS Code's Office viewer drop stacking, number formats and the house style. Review decks from `decks/pdf/` or `decks/qa/<deck>/slide-NN.jpg`.
- **LibreOffice hides colliding category labels** even with `tickLblSkip=1`, so a 23-bar horizontal chart loses every other name. Chart fewer bars or shorten labels to one line.
- **Deck build:** `decks/build_all.sh` is self-contained (`lib/theme_colors.js` writes the palette into the theme). Needs `npm install` in `decks/`, `soffice`, `pdftoppm`, `pdfinfo`.
- **zsh** (the default shell here) does not word-split `$VAR` (use arrays or `${=VAR}`), has no `PIPESTATUS` (use `if ! cmd; then`), and `echo ===` fails (`=cmd` expansion; quote it). macOS `/bin/sh` is bash 3.2: no associative arrays, so use `case` tables in portable scripts. `sed -i ''` on macOS.
- **Headless Chrome screenshots** capture the page before `setTimeout` callbacks run. Make interactions synchronous for screenshot tests, or use `--virtual-time-budget`.
- **python-pptx** crashes on empty chart-cache cells when reading `series.values`. Read the raw `c:val//c:pt/c:v` XML instead.
- **CSV hygiene:** a field with an unquoted comma broke `review_findings.csv` once. Write CSVs with the `csv` module or pandas, never by string concatenation.

## 8. Personal and internal data

- Never put a private individual's name, home address or email in a deliverable, a commit message, a subagent prompt or a request to an outside service. Board links are organization pairs with a confidence label; `dim_person` is used by ID only.
- Calvary-internal sources (the CRM export, the internal 2021–24 plan report, Calvary's audits) may appear only in materials for Calvary and the consulting team (`storylines/audiences.md`).
- Before the repository or any page goes public, remove: the CRM export, the internal plan report, `dim_person`, `fact_roles`, `candidate_interlocks`. Row 58 of `sources/web_tier1_guidelines.csv` is already redacted.
- API keys live in `~/.config/calvary/keys.env`. Source them per command (`set -a; . ~/.config/calvary/keys.env; set +a`) and never print them.

## 9. Pulling new data

Read `reference/source_quirks.md` before any new pull. Every new source gets a registry row (`source_id`, URL or file, publisher, retrieved date, licence or citation). Funder facts from the web come from the funder's own page; a third-party profile is labelled as such. Subagents doing pulls must: write deterministic, sorted output; use locked helpers when several write at once; send no personal identifiers in headers, URLs or payloads.
