# Analysis plan (approved at CP1, 2026-10-10)

## Context

Prompt 1 built `calvary_funding_data/clean/` (25 tables, QC'd, rebuild-tested). Prompt 2 turns it into analysis, recommendations and deliverables answering two questions: how exposed is Calvary to government funding, and what other funding should it pursue first. This plan is the CP1 artifact: input map, memory reconciliation, data profile, modules, early signals, open decisions. On approval I write `input_map.md`, `memory_reconciliation.md` and `analysis_plan.md` to disk as approved, confirm, and start Phase 2.

Working directory for everything new: **`calvary_analysis/`** (sibling of `calvary_funding_data/`, under `the project root`). Paths below are relative to `the project root`.

---

## 1. Input map (all found; nothing missing)

| Input | Path | Notes |
|---|---|---|
| Project README | `calvary_funding_data/README.md` | Data model, conventions, caveats, "Start here" |
| Clean tables | `calvary_funding_data/clean/*.csv` (25 files, 1.9 GB) | `dim_*`, `fact_*`, `supp_*`, `entity_aliases`, `candidate_interlocks`, `ref_ntee_codes` |
| Data dictionary | `calvary_funding_data/clean/data_dictionary.csv` | 542 rows, every column |
| Source registry | `calvary_funding_data/sources/source_registry.csv` | 238 source_ids |
| API catalog | `calvary_funding_data/sources/api_catalog.md` + `.csv` | 65 sources probed |
| Data quality report | `calvary_funding_data/reports/data_quality.md` | Row counts, nulls, reconciliation, gaps |
| Data inventory | `calvary_funding_data/reports/data_inventory.md` | Counts per universe/table |
| Analysis notes | `calvary_funding_data/notes_for_analysis.md` | 9 sections of observations |
| Open questions | `calvary_funding_data/open_questions.md` | Assumptions A1–A5, questions for Calvary, extensions |
| Build scripts | `calvary_funding_data/scripts/00–80_*.py`, `scripts/lib/` | Numbered pipeline |
| Requirements | `calvary_funding_data/requirements.txt` + `.venv/` (Python 3.12, pandas 3.0.6) | No matplotlib / networkx / python-pptx yet |
| Raw data | `calvary_funding_data/raw/` (7.0 GB) | **Present** on this machine |
| Build log | `calvary_funding_data/logs/build_log.md` (6,760 lines) | Append-only |
| Client template | `2019 CalvaryPPT_White.pptx` (project root) | 4:3 (13.54"×10.16"), 6 placeholder slides, 2 logo PNGs (white and gold-chevron variants), theme colors plum `41242F`, gold `D39F28`, light gold `FFDD7F`, teal `52C5DA`/`B1E1E9` |
| Client data | `calvary_funding_data/inputs/` (30 files: CRM xlsx, 8 audits, 7 990 PDFs, annual reports, strategic plans, donor policy) | Already extracted into clean tables; originals also duplicated at project root and `pdf-data/` |
| Supporting reports | `reports/reviewer_guide.md`, `core_peers_proposal.md`, `universe_summary.md`, `calvary_financials_reconciliation.csv` | |
| Keys | `~/.config/calvary/keys.env` (Tavily, FAC, Census, MAR) | Only needed if a new web pull is approved |

**Environment check (done, read-only):** all 25 clean tables load; row counts match `data_inventory.md` / `data_quality.md` (fact_grants 928,658; fact_gov_awards 40,300; fact_org_financials 150,461; fact_org_relationships 544,041; fact_roles 163,473). Missing tooling: `matplotlib`, `networkx`, `python-pptx`, `markitdown` (pip into `.venv`), `pptxgenjs` (npm, local to `calvary_analysis/decks/`), **LibreOffice (you are installing; needed for visual QA)**. Node 25.9, pdftoppm, pdftotext present.

---

## 2. Memory reconciliation (memory vs files)

Memory and files agree on every number I checked (Calvary FY25 revenue $4,967,995; FY21 audit gov $1.98M vs line 1e $503K; GWCF $1,206,500 TY2020–24; core peers 18 provisional; named comparators; 88 known funders; fact_org_relationships 544,041; keys file; `run_all.sh` sets `CALVARY_NO_NOTES=1`). Differences found:

| # | Item | Memory says | Files show | Likely explanation | Severity | Proposed resolution |
|---|---|---|---|---|---|---|
| 1 | "See attached" placeholder grants | 476 returns, $3.2B (also README, reviewer_guide, notes) | `data_quality.md` §7: 667 rows, $3,497,262,549; my count: 667 rows, 627 funder-years, 180 funders | README figure predates the final build (Schedule I placeholders added later, or earlier run) | **Medium** (affects landscape totals, not Calvary figures) | Use the table-derived figure ($3.5B, 627 funder-years) in analysis; note README/notes are stale; do not edit Prompt 1 docs unless you say so |
| 2 | fact_grants size | "~930K rows" | 928,658 | Rounding | Low | None |
| 3 | entity_aliases row count | (not in memory) `data_quality.md` lists it twice: 231,647 and 231,678 | File has 231,678 data rows | QC script ran twice in one build; stale first line | Low | Use 231,678; note in reconciliation |
| 4 | Grant depth | "TY2020–TY2025" | funder tax years 2012–2025 (pre-2020 from NCCS/SOI bulk, thinner) | Memory describes the XML pull scope, not the table | Low | State TY2020–24 as the complete window; use pre-2020 only for long trends with a thin-coverage caveat |
| 5 | GWCF name | one funder, $1.21M | Two `funder_name_raw` spellings under EIN 237343119 ($748,500 + $458,000) | Raw filer spelling | Low | Always aggregate on `funder_id`/EIN, never on raw name (same for Schwab 311640316, Vanguard, Gates, Schattner) |
| 6 | Machine | "original brief said a different machine; user continued here" | Prompt 2 says "may be a different machine"; raw/ present, so same machine | Wording | Low | None |
| 7 | Core peers | "provisional, user never reviewed" | Same (README, open_questions) | — | — (decision, not a difference) | **Your ruling needed** (see §6) |
| 8 | Named comparators in universes | DWC also in `national_women` via NW4 | `dim_org.universes` = `named_comparators;national_women` ✓; SheWorks parent only `named_comparators` | Consistent | — | None |

Nothing is rated High, so no analysis is blocked.

---

## 3. Data profile: what the data supports

**Strong (high confidence):**
- Calvary financial series FY2011–FY2025 (990 basis, 5 sources agree within 1%), audits FY13–FY23 with government revenue on the audit basis (37%→61%→51% share FY14–FY23). FY24/FY25 government share only on 990 line 1e (45%, 58%).
- Calvary government streams by channel and year: OVSJG (FY19–FY26 award lists), HUD CoC via TCP (2019–FY2025, three projects), SEFA FY22–23, DHS via TCP (FY2024 only: $830K TH + $593K Sisters Rise EHV), SLFRF ($3.68M one-time, FY22), PPP, small direct federal.
- Core peers (18) + DWC + SheWorks parent: full preferred financials FY2015–FY2024 (13 of 20 for FY2025), line-1e gov share, months of cash FY2020+, revenue, expenses.
- Grants to Calvary from funders' filings (138 rows, 50 funders, $4.43M TY2020–24), grants to the 18 peers (1,933 rows, 324 funders, $65.7M), CRM export (160 funders, $10.56M cumulative), support-page and annual-report lists.
- DMV funder landscape TY2020–24: $857M to `dc_sector` recipients from 570 funders; $1.98B tagged housing/dv/women from 716 funders; funder types separate DAF intermediaries from institutional decision-makers.
- DC budget lines and 297 policy events FY2024–FY2027 (OVSJG, DHS, DCHA, DBH, DHCD, DOES).
- Need/capacity context: ACS by ward, PIT 2007–2025, HIC beds 2022–2025 (Calvary's TH share 2.5%→6.8%).

**Usable with caveats (medium):**
- Gov-share benchmarks for `dc_sector` (n≈163–260/yr), `size_matched` (n≈334–543 through FY2022, then collapses to <15), `national_women` (same). Use FY2022 as the benchmark year for the national universes; FY2023 for DC.
- TY2024 grants partially filed, TY2025 mostly unfiled: "flat/declining" private trends after TY2023 are partly filing lag. Treat TY2020–23 as the trend window; TY2024 as "arriving".
- Board interlocks: 4,162 shared-board rows (2,067 high, 2,095 medium). Calvary itself: 8 links, **1 high-confidence (Clean Power Institute, irrelevant)**, 7 medium (Washington Area Women's Foundation, United Way NCA, United Way Central MD, Miriam's Kitchen, Dress for Success, DAVIS Construction Foundation, Charter School Incubator). Funder↔(peer or Calvary) links: 29, only 3 high. Zero `candidate_interlocks` involve Calvary. **Board-based relationship paths will be thin in leadership materials** and will rely on funder-sharing paths instead.
- `fact_opportunities` (286 Grants.gov rows) is mostly noise for Calvary (120 NIH, 31 NSF, embassies). Relevant rows after filtering: roughly 10–20 (HUD ROSS/CoC/Housing Counseling, VA GPD forecast, SAMHSA, OVW absent). The federal pipeline will be short; the private pipeline must come from funder behavior (M4/M5), not from an RFP feed.

**Cannot answer (and what it would take):**
- Government share on the audit basis for FY24/FY25 (no public audits). I will reconstruct a stream-level estimate from award data with explicit calendar caveats (DC FY vs HUD grant year vs Calvary FY) and label it "reconstructed". Closing it needs Calvary's FY24/FY25 audits.
- DHS/TCP contract values for FY2023, FY2025–26 (one public year). Needs Calvary's TCP subgrant agreements.
- Corporate giving not routed through a foundation (CRM-only: MGAC, IMF, Latham, Frontier Co-op, Reservoir). Treated as CRM-documented, cash-unverified.
- Foundation open RFPs/guidelines: not in the data. Optional small Tavily pull for Tier 1 targets (decision §6).

---

## 4. Proposed analysis modules

Every module: numbered script in `calvary_analysis/scripts/`, chart-data CSVs in `chart_data/`, PNG charts in `charts/`, readout in `modules/`, rows in `insight_register.csv`. Each chart CSV carries `source_tables` and `source_ids` columns so every figure traces chart → clean table → registry.

| # | Module | Purpose | Inputs | Methods / outputs | Serves |
|---|---|---|---|---|---|
| M1 | Calvary financial trajectory | Revenue, mix, growth, liquidity, concentration FY11–FY25 | `fact_org_financials` (preferred + audit rows), `fact_grants` (Calvary recipient), `fact_gov_awards` (Calvary), `dim_period` | Nominal and 2024$ series; mix = government (audit basis to FY23, line 1e + reconstructed FY24–25), institutional grants, DAF, events, residual individuals; deficit/net assets/months of cash; stream HHI; top-funder shares; FY22 spike decomposition (SLFRF building purchase) | Exposure |
| M2 | Government exposure and stress test | Stream-by-stream map vs policy timeline; scenarios | `fact_gov_awards` (one source per stream: dc_ovsjg, hud_coc, dc_oversight, audit_sefa), `fact_policy_events`, `supp_dc_budget_lines`, M1 outputs | Stream table (OVSJG Reach Up / New Foundations, CoC ×3 via TCP, DHS TH + EHV, SNAP E&T, EFSP, one-time SLFRF/PPP); durability rating per stream; scenarios (OVSJG −10/−25% = Mayor's proposed cut scale; CoC flat / −15% / loss of one project; DHS contract non-renewal; combined) → revenue gap, months of cash, deficit; DC budget trend lines (OVSJG Victim Services grants, DHS continuum, PSH) | Exposure |
| M3 | Peer benchmarking | Calvary vs 18 peers + DWC + SheWorks on mix, size, growth, resilience; who diversified and how | `fact_org_financials`, `dim_universe_membership`, `fact_grants`, `fact_gov_awards` (peer rows), `supp_hic_projects` | Gov share (line 1e; flag reporting breaks), revenue CAGR real, months of cash, institutional-funder count, DAF share, fundraising expense ratio; typology (gov-anchored / mixed / philanthropy-led); diversifier case studies (Samaritan Inns 56%→11%, N Street Village, Miriam's Kitchen, DWC scaling *with* government); sector distributions (dc_sector FY23, size_matched/national_women FY22) with Calvary's percentile; DWC + SheWorks as reference rows in every table | Both |
| M4 | Funder landscape | Who funds this space in DC/DMV, scale, concentration, shift | `fact_grants` (TY2020–24, non-cumulative, pf_grants_paid + schedule_i), `dim_funder`, `dim_universe_membership` | Institutional vs DAF; by funder type; top 25 institutional funders of dc_sector and of housing/dv/women-tagged recipients; concentration (top-1%/top-10 share); median grant size; DC vs MD/VA share; trend TY2020–23 with TY2024 "arriving" caveat; placeholder ("see attached") mass noted | Opportunity |
| M5 | Funder gap analysis | Funders supporting peers but not Calvary; lapsed and under-tapped funders | M4 base, Calvary funder set (filings + CRM + web lists), `supp_crm_cash_verification` | Gap list (27 funders fund ≥3 peers, 0 Calvary rows: Venable Foundation, T. Rowe Price Program, Clark Charitable $7.8M, Cohen, Bernstein, Washington Home, Schattner, Bunting, Bechtel…); web-list-only gaps (23); lapsed Calvary funders (gave pre-2023, not since: e.g., Meyer, Dreyfus, World Bank CCF); CRM-vs-filing reconciliation to separate "not a funder" from "filing lag/attachment-only" | Opportunity |
| M6 | Network analysis | Central funders, co-funding clusters, relationship paths | `fact_org_relationships` (grant, daf_sponsor_grant, shared_board_member, pass_through_funding), `fact_roles`, `dim_person`, `candidate_interlocks` | Bipartite funder–grantee graph (Calvary + peers + their funders; networkx); degree/betweenness; co-funding clusters; paths Calvary→target funder via shared funders, shared peers, board interlocks (**high-confidence only in leadership materials; medium labeled "unconfirmed" in consulting materials**); PNG network diagrams | Opportunity |
| M7 | Opportunity pipeline and scoring | Scored, tiered pipeline + 90-day plan | M4–M6 outputs, `fact_opportunities` (filtered), `fact_gov_awards` (DC cycles), `config/scoring_weights.yaml` | Candidate set = gap funders + lapsed funders + under-tapped current funders + DC/federal programs; dimensions: mission fit (issue tags + peer giving), regional giving, peer-giving breadth, typical award size, accessibility (public charity vs invitation-only; attachment-only filers), durability (multi-year to peers), relationship path strength, current-relationship status; weights in YAML; Tier 1/2/3; `funder_pipeline.csv`, `action_plan_90day.csv` | Opportunity |
| M8 | Mission-expansion scan | Funding pools opened by adjacent programs, with distance from current ops | `fact_grants` + `dim_funder.issue_focus_tags` by program area, `fact_opportunities` by tag, `supp_dc_budget_lines`, `fact_policy_events`, peer/DWC/SheWorks program evidence, `supp_calvary_program_metrics` | For each area (workforce, behavioral health, health, aging, veterans, reentry, maternal health, DV formalization): DMV institutional dollars, federal opps, DC budget lines, peers already there, distance (Calvary already runs job program, therapy, LEAP education) → near/medium/far; SheWorks and DWC's MADE as workforce models | Opportunity |
| M9 | Need and capacity context | Case-statement evidence | `dim_geo` (wards), `supp_homeless_counts`, `supp_hic_projects`, `supp_calvary_program_metrics` | Ward 7/8 vs DC indicators; PIT trend; Calvary's bed share and growth; women-focused provider capacity; one map of Wards 7/8 (dim_geo tract/ward attributes; shapes from `raw/geo` if present, else a schematic) | Both (short) |
| M10 | Named-comparator profiles | DWC and SheWorks as models | M3 outputs, `fact_grants` web rows, `fact_gov_awards` (DWC FAC) | One-page profile each: trajectory, mix, funders, programs, what transfers to Calvary; appendix slides | Both |

Dropped/merged from the menu: none dropped; "funder gap" and "pipeline" kept separate because the gap list is evidence and the pipeline is judgment with tunable weights.

---

## 5. Early signals (from profiling; to be verified in Phase 2)

1. **Government is the growth engine and now the majority of revenue.** Audit-basis share rose 37% (FY14) → 50% (FY21) → 61% (FY22, SLFRF spike) → 51% (FY23); line 1e 58% in FY25. OVSJG awards $369K (FY20) → $1.05M (FY26); HUD CoC $240K (2019) → $1.77M (FY2025); DHS/TCP ≈ $1.42M (FY24). Those three channels alone ≈ $4.2M/yr against $5.0M revenue, which suggests line 1e still understates government in FY24–25.
2. **FY25 stress:** $607K deficit, contributions down $5.55M → $4.75M, months of cash 4.4 (7.5 in FY21), event income collapsed ($538K → $55K line 1c).
3. **Private institutional money is flat and concentrated.** Filed grants $0.64–1.17M/yr TY2020–24; GWCF (incl. Health Equity Fund) = 27% of the five-year total; top 5 = 55%. The HEF rounds ($456K TY2022, $458K TY2024) are a CareFirst-settlement fund with a finite life: a concentration and durability flag.
4. **Peers:** DV peers run 80–94% government; Calvary (45–58%) sits mid-pack with N Street Village (39–48%) and House of Ruth (45–56%). Philanthropy-led contrast cases: Miriam's Kitchen (≤10%), Thrive DC, Samaritan Inns (56% → 11% in FY24–25: a diversification or lost-contract case to examine). DWC grew 3× in six years while its gov share rose 31% → 57%: scaling with government, not away from it.
5. **Gap funders are concrete:** 27 institutional funders give to ≥3 peers and nothing to Calvary in filings, led by Clark Charitable ($7.8M to 5 peers). Venable Foundation (10 peers) is in the CRM ($75K) but not yet in filings: filing lag, not a gap.
6. **DC budget:** OVSJG Victim Services grants flat ≈ $55M FY24–27 with Mayor-proposed cuts (−$5.8M, −$5.6M) restored by Council both years; DHS homeless continuum $170M → $206M (FY26) → $194M (FY27); PSH stable. Exposure is to flat-with-annual-threat rather than collapse; the federal side (CoC NOFO direction, SLFRF ended) is the larger uncertainty and is only partly in the data.
7. **Board paths are thin:** only one high-confidence Calvary interlock and it is irrelevant; relationship paths will be funder-sharing paths. Employer overlaps (17 board employers on funder lists) are a stronger lead but come from annual-report board lists, not filings.
8. **Federal opportunity feed is weak for Calvary's model;** DC (OVSJG/DHS/TCP) and private funders are where the pipeline will be.

---

## 6. Decisions I need from you (defaults in bold; I proceed on defaults if you only say "approved")

1. **Core peers:** **keep the 18 provisional peers as-is** and label them provisional in outputs; alternates available via `config/core_peers.csv` + rerun of `20_build_universes.py`. Or: swap now (name which).
2. **Medium-confidence interlocks:** **leadership materials use high-confidence only (per brief); consulting materials show medium ones labeled "unconfirmed" alongside the low-confidence candidates.**
3. **Small web pull for Tier 1 targets** (guidelines, deadlines, invitation-only status, ~25–40 funders via Tavily, Phase 3): **yes**, logged as a new source batch in a `calvary_analysis/sources/` registry extension. Or: no new pulls.
4. **Stale "$3.2B / 476 returns" figure in Prompt 1 docs:** **leave Prompt 1 docs untouched; note in `memory_reconciliation.md` and use $3.5B.** Or: patch the README/notes.
5. **Output location:** **`calvary_analysis/`** sibling folder, plus an "Analysis outputs" section appended to `calvary_funding_data/README.md` and a short top-level `README.md` at the project root mapping both folders. `input_map.md` and `memory_reconciliation.md` at the project root (as the brief says).
6. **Scenario severities for M2:** **OVSJG −10% / −25%, CoC −15% / loss of one project, DHS contract non-renewal, combined worst case.** Tell me if you want different levels.

---

## 7. Deliverable structure and tooling

```
calvary_analysis/
  README.md                     where everything lives, how to rerun, where to change weights
  analysis_plan.md              this plan as approved
  analysis_log.md               environment state, runs, decisions
  discoveries_log.md            flags: date, finding, evidence, proposed action, your response
  insight_register.csv          columns per brief
  config/scoring_weights.yaml   pipeline weights + tier cutoffs
  requirements.txt              pinned (pandas, matplotlib, networkx, python-pptx, markitdown, pyyaml, shapely)
  scripts/                      00_env_check.py, 01_m1_*.py … 10_m10_*.py, 20_score_pipeline.py, lib/style.py, lib/trace.py
  chart_data/                   one CSV per chart (chart_id, source_tables, source_ids)
  charts/                       PNG, 200 dpi, consistent style
  modules/                      m1_…m10 readouts
  recommendations/              funding_pressure_verdict.md, funder_pipeline.csv, action_plan_90day.csv, strategic_recommendations.md
  storylines/                   design_system.md, leadership_storyline.md, leadership_headline_spine.md, consulting_storyline.md, consulting_headline_spine.md, appendix_headline_spine.md
  decks/                        build_*.js (pptxgenjs), package.json, *.pptx, qa/ (renders, headline checks)
  reports/                      executive_one_pager.md, executive_summary.md, full_findings.md, methodology.md, recommendations.md, board_readout.md, consulting_briefing.md, review_report.md
  checkpoints/                  cp1_memo.md, cp2_memo.md, cp3_memo.md
```

**Tooling decisions:**
- Charts: matplotlib in `.venv`, palette from `storylines/design_system.md` (plum `41242F`, gold `D39F28`, teal `52C5DA` + neutrals; validated with the dataviz skill's `validate_palette.js` before use). Government = plum, institutional = gold, DAF = teal, consistently across all charts.
- Decks: pptxgenjs structured decks (theme + layouts + sections, `apply_theme.js`), 16:9, logo from the template (`image1.png` white variant) on layouts; native editable charts for bar/line/stacked; PNG for network, map, Sankey. Validate with the skill's `validate.py`; render via LibreOffice → `pdftoppm` for visual QA; headline check via `markitdown` extraction.
- Execution scripts read only from `calvary_funding_data/clean/` with relative paths; `usecols` on the two big tables.

**Skill conflicts (noted per brief):** the pptx skill prefers a slide artifact type over `.pptx` unless `.pptx` is requested — the brief requests PPTX, so `.pptx` it is. The dataviz skill's interaction rules (hover, filters) don't apply to static PNG/PPTX charts; its form, color, mark and anti-pattern rules do. The Claude Docs connector guidance (create a doc first) doesn't apply: the brief asks for local Markdown files.

**Subagents (Opus 5.5, strict rules per memory: no personal identifiers in requests, deterministic sorts, locked writes):** chart-batch rendering per module after I define each chart's spec; appendix slide assembly; visual QA passes; peer/funder/comparator profile assembly. Judgment stays here: module design, insight register, flags, scoring, verdict, storylines. Phase 6 reviewer: a fresh general-purpose agent with the input map, deliverables, register and clean tables only.

---

## 8. Phase sequence and checkpoints

| Phase | Work | Stop? |
|---|---|---|
| 1 (now) | This plan → your approval → write `input_map.md`, `memory_reconciliation.md`, `analysis_plan.md`, `analysis_log.md`, `discoveries_log.md`; install packages; CP1 confirmation | Wait for your acknowledgement |
| 2 | M1–M10 scripts, chart data, charts, readouts, insight register; design system written before the first chart; flags as they arise | No (flags only) |
| 3 | Verdict, scoring config, pipeline, 90-day plan, strategic recommendations → CP2 memo | **CP2** |
| 4 | Headline spines first, then both storylines | No |
| 5 | Exec one-pager (PPTX + MD), leadership deck (15–25), consulting deck, appendix deck(s), reports, readouts; validate, render, visual QA, headline check → CP3 memo | **CP3** |
| 6 | Independent review agent → review_report.md → fixes → register marked verified; README/input_map updated | Done |

## 9. Verification

- `scripts/00_env_check.py`: loads all 25 tables, asserts row counts vs `data_quality.md`, records package versions → `analysis_log.md`.
- Each module script asserts the sanity checks from the reviewer guide (FY25 revenue 4,967,995; Cafritz TY2024 $170,000; FY23 SEFA $937,999; OVSJG FY2026 $543,056 / $507,595; Ward 8 poverty 0.306; DWC FY2024 $34,403,997).
- Trace test: `lib/trace.py` verifies every `chart_id` referenced in a readout/storyline has a CSV, and every CSV's `source_ids` exist in the registry.
- Decks: `validate.py` clean; LibreOffice render; every slide inspected; headline spine extracted from the built deck and diffed against the approved spine.
- Phase 6 reviewer re-computes every number in decks/reports against chart data and clean tables.
