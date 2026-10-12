# Analysis log

Append-only record of environment state, runs, row counts, decisions and failures for Prompt 2.

## 2026-10-10 — Phase 1: orientation (plan mode, read-only)

- Machine: same as Prompt 1 (raw/ present, 7.0 GB). Python: `calvary_funding_data/.venv` (3.12, pandas 3.0.6). Node 25.9.0 present. pdftoppm/pdftotext present.
- Missing at start: matplotlib, networkx, python-pptx, markitdown (pip); pptxgenjs (npm); LibreOffice (user installing).
- All 25 clean tables load; row counts match reports/data_quality.md.
- Plan approved at CP1 with defaults (see analysis_plan.md §6 and ../memory_reconciliation.md).

### 2026-10-10 20:46 — 00_env_check
- candidate_interlocks: 1,270 rows
- data_dictionary: 542 rows
- dim_funder: 8,928 rows
- dim_geo: 246 rows
- dim_org: 105,189 rows
- dim_period: 28 rows
- dim_person: 48,563 rows
- dim_program_area: 13 rows
- dim_universe_membership: 17,210 rows
- entity_aliases: 231,678 rows
- fact_gov_awards: 42,958 rows  MISMATCH expected 40300
- fact_grants: 928,658 rows
- fact_opportunities: 286 rows
- fact_org_financials: 150,461 rows
- fact_org_relationships: 544,041 rows
- fact_policy_events: 297 rows
- fact_roles: 163,473 rows
- ref_ntee_codes: 623 rows
- supp_calvary_individual_donor_bands: 4 rows
- supp_calvary_program_metrics: 178 rows
- supp_calvary_strategic_targets: 18 rows
- supp_crm_cash_verification: 160 rows
- supp_dc_budget_lines: 5,172 rows
- supp_hic_projects: 1,257 rows
- supp_homeless_counts: 49,393 rows
- self-check PASS: Calvary FY25 revenue 4,967,995
- self-check PASS: DWC FY2024 revenue 34,403,997
- self-check PASS: FY23 audit SEFA sums to 937,999
- self-check PASS: OVSJG FY2026 New Foundations 543,056 / Reach Up 507,595
- self-check PASS: Ward 8 poverty 0.306
- self-check PASS: Cafritz TY2024 grant 170,000
- pandas 3.0.6
- numpy 2.5.3
- matplotlib 3.11.2
- networkx 3.7
- pptx 1.0.2
- yaml 6.0.3
- shapely 2.2.0
- raw/ present: True
- RESULT: PROBLEMS

### 2026-10-10 20:47 — 00_env_check
- candidate_interlocks: 1,270 rows
- data_dictionary: 542 rows
- dim_funder: 8,928 rows
- dim_geo: 246 rows
- dim_org: 105,189 rows
- dim_period: 28 rows
- dim_person: 48,563 rows
- dim_program_area: 13 rows
- dim_universe_membership: 17,210 rows
- entity_aliases: 231,647 rows  MISMATCH expected 231678
- fact_gov_awards: 40,300 rows
- fact_grants: 928,658 rows
- fact_opportunities: 286 rows
- fact_org_financials: 150,461 rows
- fact_org_relationships: 544,041 rows
- fact_policy_events: 297 rows
- fact_roles: 163,473 rows
- ref_ntee_codes: 623 rows
- supp_calvary_individual_donor_bands: 4 rows
- supp_calvary_program_metrics: 178 rows
- supp_calvary_strategic_targets: 18 rows
- supp_crm_cash_verification: 160 rows
- supp_dc_budget_lines: 5,172 rows
- supp_hic_projects: 1,257 rows
- supp_homeless_counts: 49,393 rows
- self-check PASS: Calvary FY25 revenue 4,967,995
- self-check PASS: DWC FY2024 revenue 34,403,997
- self-check PASS: FY23 audit SEFA sums to 937,999
- self-check PASS: OVSJG FY2026 New Foundations 543,056 / Reach Up 507,595
- self-check PASS: Ward 8 poverty 0.306
- self-check PASS: Cafritz TY2024 grant 170,000
- pandas 3.0.6
- numpy 2.5.3
- matplotlib 3.11.2
- networkx 3.7
- pptx 1.0.2
- yaml 6.0.3
- shapely 2.2.0
- raw/ present: True
- RESULT: PROBLEMS

### 2026-10-10 20:47 — 00_env_check
- candidate_interlocks: 1,270 rows
- data_dictionary: 542 rows
- dim_funder: 8,928 rows
- dim_geo: 246 rows
- dim_org: 105,189 rows
- dim_period: 28 rows
- dim_person: 48,563 rows
- dim_program_area: 13 rows
- dim_universe_membership: 17,210 rows
- entity_aliases: 231,647 rows
- fact_gov_awards: 40,300 rows
- fact_grants: 928,658 rows
- fact_opportunities: 286 rows
- fact_org_financials: 150,461 rows
- fact_org_relationships: 544,041 rows
- fact_policy_events: 297 rows
- fact_roles: 163,473 rows
- ref_ntee_codes: 623 rows
- supp_calvary_individual_donor_bands: 4 rows
- supp_calvary_program_metrics: 178 rows
- supp_calvary_strategic_targets: 18 rows
- supp_crm_cash_verification: 160 rows
- supp_dc_budget_lines: 5,172 rows
- supp_hic_projects: 1,257 rows
- supp_homeless_counts: 49,393 rows
- self-check PASS: Calvary FY25 revenue 4,967,995
- self-check PASS: DWC FY2024 revenue 34,403,997
- self-check PASS: FY23 audit SEFA sums to 937,999
- self-check PASS: OVSJG FY2026 New Foundations 543,056 / Reach Up 507,595
- self-check PASS: Ward 8 poverty 0.306
- self-check PASS: Cafritz TY2024 grant 170,000
- pandas 3.0.6
- numpy 2.5.3
- matplotlib 3.11.2
- networkx 3.7
- pptx 1.0.2
- yaml 6.0.3
- shapely 2.2.0
- raw/ present: True
- RESULT: OK

### 2026-10-10 20:51 — environment
- LibreOffice 26.8.1 installed (brew cask); `soffice --headless --convert-to pdf` verified on the client template; pdftoppm render verified.
- CP1 acknowledged (user installed LibreOffice in reply); Phase 2 started.

### 2026-10-10 20:55 — 01_m1_trajectory
- charts m1_01..m1_08 written; filed grants TY2020-24 4,433,659 from 50 funders; HHI 1168
- gov share audit FY14 0.374, FY23 0.512; line 1e FY25 0.582
- FY25 deficit -607,326; months of cash FY25 4.44

### 2026-10-10 20:57 — 01_m1_trajectory
- charts m1_01..m1_08 written; filed grants TY2020-24 4,433,659 from 50 funders; HHI 1168
- gov share audit FY14 0.374, FY23 0.512; line 1e FY25 0.582
- FY25 deficit -607,326; months of cash FY25 4.44

### 2026-10-10 21:00 — 02_m2_exposure
- streams: OVSJG recurring FY26 1,050,651; CoC FY2025 awards 1,766,814; DHS FY2024 1,423,664
- ceilings vs recognized FY24 3,595,278 vs 2,621,203; FY25 4,289,967 vs 2,892,598
- scenarios S1-S6 written to chart_data/m2_07_scenarios.csv
- charts m2_01..m2_07 written

### 2026-10-10 21:02 — 01_m1_trajectory
- charts m1_01..m1_08 written; filed grants TY2020-24 4,433,659 from 50 funders; HHI 1168
- gov share audit FY14 0.374, FY23 0.512; line 1e FY25 0.582
- FY25 deficit -607,326; months of cash FY25 4.44

### 2026-10-10 21:02 — 02_m2_exposure
- streams: OVSJG recurring FY26 1,050,651; CoC FY2025 awards 1,766,814; DHS FY2024 1,423,664
- ceilings vs recognized FY24 3,595,278 vs 2,621,203; FY25 4,289,967 vs 2,892,598
- scenarios S1-S6 written to chart_data/m2_07_scenarios.csv
- charts m2_01..m2_07 written

### 2026-10-10 21:03 — 02_m2_exposure
- streams: OVSJG recurring FY26 1,050,651; CoC FY2025 awards 1,766,814; DHS FY2024 1,423,664
- ceilings vs recognized FY24 3,595,278 vs 2,621,203; FY25 4,289,967 vs 2,892,598
- scenarios S1-S6 written to chart_data/m2_07_scenarios.csv
- charts m2_01..m2_07 written

### 2026-10-10 21:07 — 01_m1_trajectory
- charts m1_01..m1_08 written; filed grants TY2020-24 4,433,659 from 50 funders; HHI 1168
- gov share audit FY14 0.374, FY23 0.512; line 1e FY25 0.582
- FY25 deficit -607,326; months of cash FY25 4.44

### 2026-10-10 21:07 — 02_m2_exposure
- streams: OVSJG recurring FY26 1,050,651; CoC FY2025 awards 1,766,814; DHS FY2024 1,423,664
- ceilings vs recognized FY24 3,595,278 vs 2,621,203; FY25 4,289,967 vs 2,892,598
- scenarios S1-S6 written to chart_data/m2_07_scenarios.csv
- charts m2_01..m2_07 written

### 2026-10-10 21:07 — 03_m3_peers
- benchmark table 21 orgs; Calvary gov share FY22-24 mean 0.525; rank 11/19
- charts m3_01..m3_09 written

### 2026-10-10 21:08 — 03_m3_peers
- benchmark table 21 orgs; Calvary gov share FY22-24 mean 0.525; rank 11/19
- charts m3_01..m3_09 written

### 2026-10-10 21:10 — 03_m3_peers
- benchmark table 21 orgs; Calvary gov share FY22-24 mean 0.525; rank 11/19
- charts m3_01..m3_09 written

### 2026-10-10 21:11 — 04_m4_landscape
- lens A dc_sector TY2020-24 856,633,491 (7,302 rows, 570 funders); institutional 472,480,641 from 557 funders; DAF 384,152,850
- lens B mission-tagged DMV 633,815,768 from 558 funders
- charts m4_01..m4_08 and landscape table written

### 2026-10-10 21:14 — 04_m4_landscape
- lens A dc_sector TY2020-24 660,487,525 (7,148 rows, 568 funders); institutional 276,334,675 from 555 funders; DAF 384,152,850
- lens B mission-tagged DMV 230,895,076 from 556 funders
- charts m4_01..m4_08 and landscape table written

### 2026-10-10 21:14 — 04_m4_landscape
- lens A dc_sector TY2020-24 660,487,525 (7,148 rows, 568 funders); institutional 276,334,675 from 555 funders; DAF 384,152,850
- lens B mission-tagged DMV 230,895,076 from 556 funders
- charts m4_01..m4_08 and landscape table written

### 2026-10-10 21:14 — 05_m5_gaps
- G1 peer-funder gaps 75 (>=3 peers: 23); lapsed 12 + unclear 1; headroom 15; DC majors 65; web-only 17
- candidate base 166 funders written to m5_00_candidate_funders.csv

### 2026-10-10 21:17 — 06_m6_network
- graph: 349 nodes, 701 edges; funders 330; Calvary interlocks 8; paths scored for 166 candidates
- charts m6_02, m6_03 written; tables m6_01, m6_04, m6_05

### 2026-10-10 21:21 — 04_m4_landscape
- lens A dc_sector TY2020-24 660,487,525 (7,148 rows, 568 funders); institutional 276,334,675 from 555 funders; DAF 384,152,850
- lens B mission-tagged DMV 230,895,076 from 556 funders
- charts m4_01..m4_08 and landscape table written

### 2026-10-10 21:22 — 05_m5_gaps
- G1 peer-funder gaps 75 (>=3 peers: 23); lapsed 12 + unclear 1; headroom 15; DC majors 65; web-only 16
- candidate base 166 funders written to m5_00_candidate_funders.csv

### 2026-10-10 21:22 — 06_m6_network
- graph: 349 nodes, 701 edges; funders 330; Calvary interlocks 8; paths scored for 166 candidates
- charts m6_02, m6_03 written; tables m6_01, m6_04, m6_05

### 2026-10-10 21:22 — 07_m7_pipeline
- pipeline 182 rows; tiers {3: 131, 2: 38, 1: 13}; action plan 13 rows
- charts m7_02, m7_03 written

### 2026-10-10 21:23 — 08_m8_expansion
- scan 10 areas; federal relevant 82
- chart m8_01 written

### 2026-10-10 21:23 — 09_m9_need_capacity
- ACS wards written; PIT 5138 (2025); Calvary TH share 0.068; map False

### 2026-10-10 21:25 — 07_m7_pipeline
- pipeline 182 rows; tiers {3: 131, 2: 39, 1: 12}; action plan 12 rows
- charts m7_02, m7_03 written

### 2026-10-10 21:25 — 08_m8_expansion
- scan 10 areas; federal relevant 36
- chart m8_01 written

### 2026-10-10 21:25 — 08_m8_expansion
- scan 10 areas; federal relevant 36
- chart m8_01 written

### 2026-10-10 21:25 — 09_m9_need_capacity
- ACS wards written; PIT 5138 (2025); Calvary TH share 0.068; map True

### 2026-10-10 21:25 — 10_m10_profiles
- profiles written; DWC FAC total 21,618,528; DWC DMV-filed funders 8
- charts m10_01, m10_02 written

### 2026-10-10 21:29 — 01_m1_trajectory
- charts m1_01..m1_08 written; filed grants TY2020-24 4,433,659 from 50 funders; HHI 1168
- gov share audit FY14 0.374, FY23 0.512; line 1e FY25 0.582
- FY25 deficit -607,326; months of cash FY25 4.44

### 2026-10-10 — CP2
- CP2 approved with defaults; flags D1-D3 handled as proposed; tone guidance recorded in design_system.md §6 and memory.

### 2026-10-10 21:40 — 11_web_tier1_guidelines
- Tavily guideline search for 32 Tier 1-2 institutional funders; 128 hits; registry extension 32 rows

### 2026-10-10 21:46 — 12_merge_guidelines
- guideline notes merged for 27 funders; pipeline and action plan updated

### 2026-10-10 21:48 — 12_merge_guidelines
- guideline notes merged for 27 funders; pipeline and action plan updated

### 2026-10-10 21:52 — 13_m7_sensitivity
- sensitivity: max mean rank shift in top 30 = 1.70; min top-10 overlap = 9

### 2026-10-10 22:01 — 01_m1_trajectory
- charts m1_01..m1_08 written; filed grants TY2020-24 4,433,659 from 50 funders; HHI 1168
- gov share audit FY14 0.374, FY23 0.512; line 1e FY25 0.582
- FY25 deficit -607,326; months of cash FY25 4.44

### 2026-10-10 22:01 — 02_m2_exposure
- streams: OVSJG recurring FY26 1,050,651; CoC FY2025 awards 1,766,814; DHS FY2024 1,423,664
- ceilings vs recognized FY24 3,595,278 vs 2,621,203; FY25 4,289,967 vs 2,892,598
- scenarios S1-S6 written to chart_data/m2_07_scenarios.csv
- charts m2_01..m2_07 written

### 2026-10-10 22:01 — 03_m3_peers
- benchmark table 21 orgs; Calvary gov share FY22-24 mean 0.525; rank 11/19
- charts m3_01..m3_09 written

### 2026-10-10 22:01 — 06_m6_network
- graph: 349 nodes, 701 edges; funders 330; Calvary interlocks 8; paths scored for 166 candidates
- charts m6_02, m6_03 written; tables m6_01, m6_04, m6_05

### 2026-10-10 22:01 — 07_m7_pipeline
- pipeline 182 rows; tiers {3: 131, 2: 40, 1: 11}; action plan 11 rows
- charts m7_02, m7_03 written

### 2026-10-10 22:01 — 12_merge_guidelines
- guideline notes merged for 27 funders; pipeline and action plan updated

### 2026-10-10 22:01 — 13_m7_sensitivity
- sensitivity: max mean rank shift in top 30 = 1.70; min top-10 overlap = 9

### 2026-10-10 — consistency pass after the report assembly
- Register vs readout differences resolved at the source: M1 audit-basis share now uses audited total revenue (FY15–25 range 40–61%); M3 rank 11 of 19 and DV range 70–89%; M4 landscape $660M / $132M a year, 555 institutional funders, top 10 = 55%; M6 330 funders, GWCF 18; M7 corporate rows need the Tier 1 score cutoff (Frontier Co-op → Tier 2), Tier 1 = 11 of 182 rows; M2-06 Sisters Rise 24 HIC beds (DHS capacity 25); DWC ×5.5. Text files updated by a scripted replacement; cp2_memo.md left as the record of that checkpoint.

### 2026-10-10 22:23 — 02_m2_exposure
- streams: OVSJG recurring FY26 1,050,651; CoC FY2025 awards 1,766,814; DHS FY2024 1,423,664
- ceilings vs recognized FY24 3,595,278 vs 2,621,203; FY25 4,289,967 vs 2,892,598
- scenarios S1-S6 written to chart_data/m2_07_scenarios.csv
- charts m2_01..m2_07 written

### 2026-10-10 22:23 — 10_m10_profiles
- profiles written; DWC FAC total 21,618,528; DWC DMV-filed funders 8
- charts m10_01, m10_02 written

### 2026-10-10 22:32 — Phase 5 QA gates
- All seven decks pass validate.py; zero absolute paths or usernames in slide XML; headline checks: leadership 22/22 and consulting 55/55 match their spines with no title over 20 words and no semicolons; appendices A–D under 24 words with reference headers allowed; trace test OK.
- Visual QA: subagent pass on leadership, consulting and one-pager (about 40 fixes), appendix decks checked slide by slide by the appendix builder; final spot checks by the lead.

### 2026-10-11 16:53 — 06_m6_network (cosmetic redraw of m6_03)
- graph: 349 nodes, 701 edges; funders 330; Calvary interlocks 8; paths scored for 166 candidates (unchanged)
- m6_03_network redrawn for a full-width slide band (12.13 x 3.3 in): concentric layout (Calvary centre, 12 hub funders inner ring, 18 peers outer ring), all peers and hub funders labelled with no overlaps; node build order sorted so the layout reproduces run to run (a set-ordered subgraph had moved it between runs). m6_03_network_nodes: only x/y changed. Other chart data byte-identical; trace test OK.
- Slides: leadership 17, consulting 42, Appendix C 26 now use lib/deck.js wideImage (chart full width, card as a band below); footnote method text updated from "spring layout" to "concentric layout" on consulting 42 and Appendix C 26.

### 2026-10-11 17:10 — web/build_network_page.py (Calvary Funder Web explorer)
- New: interactive network page from the m6 graph (same fact_grants filters and landscape exclusions as 06). Reconciles to m6_01 before writing (funder set, organizations funded, dollars, grant counts): 330 funders (58 fund 3+), 19 organizations, 701 links, $70,079,227 TY2020-24; 50 Calvary funders.
- Public filings only: no CRM data, no people or board links (R05 open), no pipeline tiers (R16/R17 open). One status note: Clark Charitable Foundation winding down (R16).
- Outputs: web/Calvary_Grantmaker_Web.html (self-contained: d3 7.9.0 and the two OFL fonts embedded from web/vendor/, verified rendering with network blocked) and web/publish/funder_network.html, published as a private claude.ai artifact: https://claude.ai/artifact/WCuc16rXqs4UhqRpztfs47 (republish to this URL). FUNDER_SHORT moved to scripts/lib/common.py and shared with 06; m6_03 PNG byte-identical after the move.
- 2026-10-11: page renamed "Calvary Grantmaker Web" (file web/Calvary_Grantmaker_Web.html) and "funder" replaced by "grantmaker" in all visible text, because the page covers only organizations that report grants on their own IRS returns. Header simplified to the title plus Data dictionary and Methodology.
- 2026-10-11: "Download data" added to the Grantmaker Web: three CSVs built in the page from its embedded data (grantmakers 330 rows, grants by organization and year 701, the 19 organizations). Checked: $4,433,659 to Calvary, $70,079,227 total, year columns sum to each row's total, all lines parse. Plain browser download plus Copy (tab-separated for pasting); the claude.ai copy is no longer republished.
- 2026-10-11: Grantmaker Web filter bar rebuilt: quick views (Overview 58, Prospects 25, Calvary's grantmakers 50, Lapsed from Calvary 15, Major hubs 12), dropdown filters with live counts (Calvary, Reach, Type, Funds peer, Size, Recent), List mode in the side panel with sort and a CSV export of the current view, Reset. "Lapsed" = Calvary grant in TY2020-22 and none in TY2023-24 filings (some 2024 returns still arriving).
- 2026-10-11: Grantmaker Web side panel now explains each quick view (Prospects, Calvary's grantmakers, Lapsed, Major hubs) with live figures above its list, and summarizes custom filter mixes; "Fdn" short names spelled out as "Foundation" on the page.
- 2026-10-11: Grantmaker Web keeps all 18 peers on the ring under every filter but fades a peer no grantmaker in view funds (e.g. 4 in Lapsed from Calvary); peer hover shows its count in view.
- 2026-10-11: Grantmaker Web focused views: map caption per view, spotlit grantmakers (larger, outlined), names on the map for views of 40 or fewer (four placement tries, caption and legend treated as taken), hover traces a node's lines; fit shrinks only when the caption or legend would cover a circle or peer name.
- 2026-10-11: fix: standalone file lacked a global [hidden] rule, so the map caption stayed after returning to Overview and an empty search-results box showed under the search field.
- 2026-10-11: chart pass: 1 px black outline on every bar (PNG polish() and native dataBorder), replacing white gaps; label declutter in polish() (labels nudged off other labels and scatter dots, leader lines when moved 9 pt+): m3_02 17 labels moved, m6_02 2, none left overlapping; m1_02 share labels now sit above the stack top. Modules rerun in README order: data byte-identical; all decks rebuilt, slide text and chart data identical.

### 2026-10-11 18:58 — 05_m5_gaps
- G1 peer-funder gaps 75 (>=3 peers: 23); lapsed 11 + unclear 1; headroom 15; DC majors 65; web-only 16
- candidate base 166 funders written to m5_00_candidate_funders.csv

### 2026-10-11 18:58 — 06_m6_network
- graph: 349 nodes, 701 edges; funders 330; Calvary interlocks 8; paths scored for 166 candidates
- charts m6_02, m6_03 written; tables m6_01, m6_04, m6_05

### 2026-10-11 18:58 — 07_m7_pipeline
- pipeline 182 rows; tiers {3: 134, 2: 39, 1: 9}; action plan 9 rows
- charts m7_02, m7_03 written

### 2026-10-11 18:58 — 12_merge_guidelines
- guideline notes merged for 27 funders; pipeline and action plan updated

### 2026-10-11 18:58 — 13_m7_sensitivity
- sensitivity: max mean rank shift in top 30 = 1.70; min top-10 overlap = 9

### 2026-10-11 18:59 — 02_m2_exposure
- streams: OVSJG recurring FY26 1,050,651; CoC FY2025 awards 1,766,814; DHS FY2024 1,423,664
- ceilings vs recognized FY24 3,595,278 vs 2,621,203; FY25 4,289,967 vs 2,892,598
- scenarios S1-S6 written to chart_data/m2_07_scenarios.csv
- charts m2_01..m2_07 written

### 2026-10-11 19:00 — 03_m3_peers
- benchmark table 21 orgs; Calvary gov share FY22-24 mean 0.525; rank 11/19
- charts m3_01..m3_09 written

### 2026-10-11 19:04 — 01_m1_trajectory
- charts m1_01..m1_08 written; filed grants TY2020-24 4,433,659 from 50 funders; HHI 1168
- gov share audit FY14 0.374, FY23 0.512; line 1e FY25 0.582
- FY25 deficit -607,326; months of cash FY25 4.44

### 2026-10-11 19:04 — 02_m2_exposure
- streams: OVSJG recurring FY26 1,050,651; CoC FY2025 awards 1,766,814; DHS FY2024 1,423,664
- ceilings vs recognized FY24 3,595,278 vs 2,621,203; FY25 4,289,967 vs 2,892,598
- scenarios S1-S6 written to chart_data/m2_07_scenarios.csv
- charts m2_01..m2_07 written

### 2026-10-11 19:04 — 03_m3_peers
- benchmark table 21 orgs; Calvary gov share FY22-24 mean 0.525; rank 11/19
- charts m3_01..m3_09 written

### 2026-10-11 19:04 — 04_m4_landscape
- lens A dc_sector TY2020-24 660,487,525 (7,148 rows, 568 funders); institutional 276,334,675 from 555 funders; DAF 384,152,850
- lens B mission-tagged DMV 230,895,076 from 556 funders
- charts m4_01..m4_08 and landscape table written

### 2026-10-11 19:05 — 05_m5_gaps
- G1 peer-funder gaps 75 (>=3 peers: 23); lapsed 11 + unclear 1; headroom 15; DC majors 65; web-only 16
- candidate base 166 funders written to m5_00_candidate_funders.csv

### 2026-10-11 19:05 — 06_m6_network
- graph: 347 nodes, 699 edges; funders 328; Calvary interlocks 8; paths scored for 166 candidates
- charts m6_02, m6_03 written; tables m6_01, m6_04, m6_05

### 2026-10-11 19:05 — 07_m7_pipeline
- pipeline 182 rows; tiers {3: 134, 2: 39, 1: 9}; action plan 9 rows
- charts m7_02, m7_03 written

### 2026-10-11 19:05 — 08_m8_expansion
- scan 10 areas; federal relevant 36
- chart m8_01 written

### 2026-10-11 19:05 — 09_m9_need_capacity
- ACS wards written; PIT 5138 (2025); Calvary TH share 0.068; map True

### 2026-10-11 19:05 — 10_m10_profiles
- profiles written; DWC FAC total 21,618,528; DWC DMV-filed funders 8
- charts m10_01, m10_02 written

### 2026-10-11 19:05 — 12_merge_guidelines
- guideline notes merged for 27 funders; pipeline and action plan updated

### 2026-10-11 19:05 — 13_m7_sensitivity
- sensitivity: max mean rank shift in top 30 = 1.70; min top-10 overlap = 9

### 2026-10-11 19:10 — 01_m1_trajectory
- charts m1_01..m1_08 written; filed grants TY2020-24 4,433,659 from 50 funders; HHI 1168
- gov share audit FY14 0.374, FY23 0.512; line 1e FY25 0.582
- FY25 deficit -607,326; months of cash FY25 4.44

### 2026-10-11 19:17 — 01_m1_trajectory
- charts m1_01..m1_08 written; filed grants TY2020-24 4,433,659 from 50 funders; HHI 1168
- gov share audit FY14 0.374, FY23 0.512; line 1e FY25 0.582
- FY25 deficit -607,326; months of cash FY25 4.44

### 2026-10-11 19:17 — 02_m2_exposure
- streams: OVSJG recurring FY26 1,050,651; CoC FY2025 awards 1,766,814; DHS FY2024 1,423,664
- ceilings vs recognized FY24 3,595,278 vs 2,621,203; FY25 4,289,967 vs 2,892,598
- scenarios S1-S6 written to chart_data/m2_07_scenarios.csv
- charts m2_01..m2_07 written

### 2026-10-11 19:17 — 03_m3_peers
- benchmark table 21 orgs; Calvary gov share FY22-24 mean 0.525; rank 11/19
- charts m3_01..m3_09 written

### 2026-10-11 19:17 — 04_m4_landscape
- lens A dc_sector TY2020-24 660,487,525 (7,148 rows, 568 funders); institutional 276,334,675 from 555 funders; DAF 384,152,850
- lens B mission-tagged DMV 230,895,076 from 556 funders
- charts m4_01..m4_08 and landscape table written

### 2026-10-11 19:17 — 05_m5_gaps
- G1 peer-funder gaps 75 (>=3 peers: 23); lapsed 11 + unclear 1; headroom 15; DC majors 65; web-only 16
- candidate base 166 funders written to m5_00_candidate_funders.csv

### 2026-10-11 19:17 — 06_m6_network
- graph: 347 nodes, 699 edges; funders 328; Calvary interlocks 8; paths scored for 166 candidates
- charts m6_02, m6_03 written; tables m6_01, m6_04, m6_05

### 2026-10-11 19:17 — 07_m7_pipeline
- pipeline 182 rows; tiers {3: 134, 2: 39, 1: 9}; action plan 9 rows
- charts m7_02, m7_03 written

### 2026-10-11 19:18 — 08_m8_expansion
- scan 10 areas; federal relevant 36
- chart m8_01 written

### 2026-10-11 19:18 — 09_m9_need_capacity
- ACS wards written; PIT 5138 (2025); Calvary TH share 0.068; map True

### 2026-10-11 19:18 — 10_m10_profiles
- profiles written; DWC FAC total 21,618,528; DWC DMV-filed funders 8
- charts m10_01, m10_02 written

### 2026-10-11 19:18 — 12_merge_guidelines
- guideline notes merged for 27 funders; pipeline and action plan updated

### 2026-10-11 19:18 — 13_m7_sensitivity
- sensitivity: max mean rank shift in top 30 = 1.70; min top-10 overlap = 9

### 2026-10-11 19:18 — 07_m7_pipeline
- pipeline 182 rows; tiers {3: 134, 2: 39, 1: 9}; action plan 9 rows
- charts m7_02, m7_03 written

### 2026-10-11 19:18 — 12_merge_guidelines
- guideline notes merged for 29 funders; pipeline and action plan updated

### 2026-10-11 19:18 — 13_m7_sensitivity
- sensitivity: max mean rank shift in top 30 = 1.70; min top-10 overlap = 9

### 2026-10-11 19:28 — 01_m1_trajectory
- charts m1_01..m1_08 written; filed grants TY2020-24 4,433,659 from 50 funders; HHI 1168
- gov share audit FY14 0.374, FY23 0.512; line 1e FY25 0.582
- FY25 deficit -607,326; months of cash FY25 4.44

### 2026-10-11 19:28 — 02_m2_exposure
- streams: OVSJG recurring FY26 1,050,651; CoC FY2025 awards 1,766,814; DHS FY2024 1,423,664
- ceilings vs recognized FY24 3,595,278 vs 2,621,203; FY25 4,289,967 vs 2,892,598
- scenarios S1-S6 written to chart_data/m2_07_scenarios.csv
- charts m2_01..m2_07 written

### 2026-10-11 19:28 — 03_m3_peers
- benchmark table 21 orgs; Calvary gov share FY22-24 mean 0.525; rank 11/19
- charts m3_01..m3_09 written

### 2026-10-11 19:29 — 04_m4_landscape
- lens A dc_sector TY2020-24 660,487,525 (7,148 rows, 568 funders); institutional 276,334,675 from 555 funders; DAF 384,152,850
- lens B mission-tagged DMV 230,895,076 from 556 funders
- charts m4_01..m4_08 and landscape table written

### 2026-10-11 19:29 — 05_m5_gaps
- G1 peer-funder gaps 75 (>=3 peers: 23); lapsed 11 + unclear 1; headroom 15; DC majors 65; web-only 16
- candidate base 166 funders written to m5_00_candidate_funders.csv

### 2026-10-11 19:29 — 06_m6_network
- graph: 347 nodes, 699 edges; funders 328; Calvary interlocks 8; paths scored for 166 candidates
- charts m6_02, m6_03 written; tables m6_01, m6_04, m6_05

### 2026-10-11 19:29 — 07_m7_pipeline
- pipeline 182 rows; tiers {3: 134, 2: 39, 1: 9}; action plan 9 rows
- charts m7_02, m7_03 written

### 2026-10-11 19:29 — 08_m8_expansion
- scan 10 areas; federal relevant 36
- chart m8_01 written

### 2026-10-11 19:29 — 09_m9_need_capacity
- ACS wards written; PIT 5138 (2025); Calvary TH share 0.068; map True

### 2026-10-11 19:29 — 10_m10_profiles
- profiles written; DWC FAC total 21,618,528; DWC DMV-filed funders 8
- charts m10_01, m10_02 written

### 2026-10-11 19:29 — 12_merge_guidelines
- guideline notes merged for 29 funders; pipeline and action plan updated

### 2026-10-11 19:29 — 13_m7_sensitivity
- sensitivity: max mean rank shift in top 30 = 1.70; min top-10 overlap = 9

## 2026-10-11 — review fix cycle (Prompt 3 findings R01–R18, M01–M13, N01–N03)
- Worked every row of `reports/review/review_findings.csv` from the canonical wording in `reports/review/fix_spec.md`; the per-finding record is `reports/review/fix_log.md`.
- Code and config: scenario ranges (02), sector percentile among reporters and all filers (03), lapsed rule excludes one-time capital grants (05), board-link confidence needs overlapping terms (06), open status, channels, next-step overrides and capacity sequencing in the pipeline (07, 12, `config/scoring_weights.yaml`, `config/guideline_notes.csv`), event receipts = lines 1c + 8a (01), grant exclusions on every load (`config/grant_exclusions.csv`, `lib/common.py`), register keeps `verified` on unchanged reruns.
- Assumptions: Bunting and Bechtel have no public application process (third-party profiles; treated as invitation-only, Tier 3, not plan targets), confidence medium; Jane Bancroft Robinson grants by periodic RFP (its own grants page), confidence medium.
- Deliverables: all seven decks, the reports, the module readouts, the storylines and the Grantmaker Web page updated and rebuilt; `reports/full_findings.md` is now generated (`scripts/lib/full_findings.py`). Trace OK; headline checks OK on all decks; guardrail scan clean (run with `REVIEW_OUT` in scratch).
- Tooling: `decks/build_all.sh` and `decks/lib/theme_colors.js` remove the dependency on an external skill; every horizontal native bar chart labels every bar.
- Process: `CLAUDE.md` (house rules, analyst approach), `.claude/skills/new-deck` and `.claude/skills/calvary-data`, `storylines/audiences.md`.

### 2026-10-12 11:27 — 01_m1_trajectory
- charts m1_01..m1_08 written; filed grants TY2020-24 4,433,659 from 50 funders; HHI 1168
- gov share audit FY14 0.374, FY23 0.512; line 1e FY25 0.582
- FY25 deficit -607,326; months of cash FY25 4.44

### 2026-10-12 11:27 — 02_m2_exposure
- streams: OVSJG recurring FY26 1,050,651; CoC FY2025 awards 1,766,814; DHS FY2024 1,423,664
- ceilings vs recognized FY24 3,595,278 vs 2,621,203; FY25 4,289,967 vs 2,892,598
- scenarios S1-S6 written to chart_data/m2_07_scenarios.csv
- charts m2_01..m2_07 written

### 2026-10-12 11:28 — 03_m3_peers
- benchmark table 21 orgs; Calvary gov share FY22-24 mean 0.525; rank 11/19
- charts m3_01..m3_09 written

### 2026-10-12 11:28 — 04_m4_landscape
- lens A dc_sector TY2020-24 660,487,525 (7,148 rows, 568 funders); institutional 276,334,675 from 555 funders; DAF 384,152,850
- lens B mission-tagged DMV 230,895,076 from 556 funders
- charts m4_01..m4_08 and landscape table written

### 2026-10-12 11:28 — 05_m5_gaps
- G1 peer-funder gaps 75 (>=3 peers: 23); lapsed 11 + unclear 1; headroom 15; DC majors 65; web-only 16
- candidate base 166 funders written to m5_00_candidate_funders.csv

### 2026-10-12 11:28 — 06_m6_network
- graph: 347 nodes, 699 edges; funders 328; Calvary interlocks 8; paths scored for 166 candidates
- charts m6_02, m6_03 written; tables m6_01, m6_04, m6_05

### 2026-10-12 11:28 — 07_m7_pipeline
- pipeline 182 rows; tiers {3: 134, 2: 39, 1: 9}; action plan 9 rows
- charts m7_02, m7_03 written

### 2026-10-12 11:28 — 08_m8_expansion
- scan 10 areas; federal relevant 36
- chart m8_01 written

### 2026-10-12 11:28 — 09_m9_need_capacity
- ACS wards written; PIT 5138 (2025); Calvary TH share 0.068; map True

### 2026-10-12 11:28 — 10_m10_profiles
- profiles written; DWC FAC total 21,618,528; DWC DMV-filed funders 8
- charts m10_01, m10_02 written

### 2026-10-12 11:28 — 12_merge_guidelines
- guideline notes merged for 29 funders; pipeline and action plan updated

### 2026-10-12 11:28 — 13_m7_sensitivity
- sensitivity: max mean rank shift in top 30 = 1.70; min top-10 overlap = 9

### 2026-10-12 11:40 — 00_env_check
- candidate_interlocks: 1,270 rows
- data_dictionary: 542 rows
- dim_funder: 8,928 rows
- dim_geo: 246 rows
- dim_org: 105,189 rows
- dim_period: 28 rows
- dim_person: 48,563 rows
- dim_program_area: 13 rows
- dim_universe_membership: 17,210 rows
- entity_aliases: 231,647 rows
- fact_gov_awards: 40,300 rows
- fact_grants: 928,658 rows
- fact_opportunities: 286 rows
- fact_org_financials: 150,461 rows
- fact_org_relationships: 544,041 rows
- fact_policy_events: 297 rows
- fact_roles: 163,473 rows
- ref_ntee_codes: 623 rows
- supp_calvary_individual_donor_bands: 4 rows
- supp_calvary_program_metrics: 178 rows
- supp_calvary_strategic_targets: 18 rows
- supp_crm_cash_verification: 160 rows
- supp_dc_budget_lines: 5,172 rows
- supp_hic_projects: 1,257 rows
- supp_homeless_counts: 49,393 rows
- self-check PASS: Calvary FY25 revenue 4,967,995
- self-check PASS: DWC FY2024 revenue 34,403,997
- self-check PASS: FY23 audit SEFA sums to 937,999
- self-check PASS: OVSJG FY2026 New Foundations 543,056 / Reach Up 507,595
- self-check PASS: Ward 8 poverty 0.306
- self-check PASS: Cafritz TY2024 grant 170,000
- pandas 3.0.6
- numpy 2.5.3
- matplotlib 3.11.2
- networkx 3.7
- pptx 1.0.2
- yaml 6.0.3
- shapely 2.2.0
- raw/ present: True
- RESULT: OK
