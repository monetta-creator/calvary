# Consulting team deck: storyline

Headline numbers match `consulting_headline_spine.md`. Each row: layout, evidence on the slide, chart or table, footnote source and method note. Charts marked *native* are editable PowerPoint charts; *PNG* are rendered images.

| # | Layout | Evidence on the slide | Chart / table | Footnote (source; method note) |
|---|---|---|---|---|
| 1 | TITLE | Two anchor questions; audience; as-of date 2026-10-10 | — | — |
| 2 | TABLE | Table of the 25 clean tables with grain and main sources; counts (928,658 grant rows, 40,300 award rows, 150,461 financial rows, 297 policy events) | input map | calvary_funding_data/README.md; data_inventory.md |
| 3 | TABLE | Universe table: calvary, core_peers 18 (provisional, with tiers), named_comparators 2, dc_sector 1,027, size_matched 566, national_women 2,878, dmv_funders 7,705, daf_sponsors 15 | universe_summary | dim_universe_membership; method note D2 |
| 4 | CHART native line | Audit vs line 1e government share FY13–FY25 | m1_03 | fact_org_financials; A1 |
| 5 | TABLE | Limitations table: item, effect, mitigation (no FY24–25 audits; DHS one year; TY2024 partial; "see attached" filers; provisional peers; interlock confidence) | — | data_quality.md; D3 |
| 6 | CHART native line | Revenue nominal and 2024$, expenses; FY22 annotation | m1_01 | fact_org_financials, dim_period; A1 |
| 7 | CHART native stacked column | Revenue mix FY15–FY25 with government share labels | m1_02 | A1 |
| 8 | CHART native line | Two measures (repeat of 4 with the FY21 reconciliation table: audit $1.98M vs 1e $503K; FY22–23 identical) | m1_03 | A1 |
| 9 | CHART native column + bar | Surplus/deficit FY11–FY25; months of cash with the 3–6 month band | m1_04, m1_05 | A1 |
| 10 | CHART native column/line | Event contributions (1c) vs net event income (8c) | m1_06 | A1; flag D3 |
| 11 | CHART native bar | Top 12 filed funders with shares; by-year institutional vs DAF | m1_07, m1_08 | fact_grants, dim_funder; A3 |
| 12 | CHART native stacked column | Recurring streams by award year; one-time awards listed below | m2_01, m2_01b | fact_gov_awards; A2 |
| 13 | TABLE | Stream durability table: stream, detail, first/latest amount, funding source, renewal mechanism, risk | m2_03 | fact_gov_awards, fact_policy_events, supp_hic_projects; A2 (ratings = analyst judgment) |
| 14 | CHART native column | Ceilings (stacked by stream) vs recognized FY24, FY25 | m2_02 | A5; flag D1 |
| 15 | CHART PNG | DC budget small multiples (approved, actual, Mayor's proposal) | m2_04 | supp_dc_budget_lines; A6 |
| 16 | CHART native bar | Policy events ≥$2M touching Calvary's lines, cuts vs restorations | m2_06 | fact_policy_events; A6 |
| 17 | CHART native line | Calvary's share of OVSJG and CoC pools by year | m2_05 | fact_gov_awards; A2 |
| 18 | TABLE + native bar | Scenario table (gross and net) and parameters; bar of revenue loss | m2_07, m2_07 parameters | config/scenarios.yaml; A4 |
| 19 | CHART native bar | Government share ranked, FY22–24 mean, bands | m3_01 | B1 |
| 20 | CHART native range | Sector distributions with Calvary's percentile | m3_07 | B1 |
| 21 | CHART PNG scatter | Size vs government share, typology bands | m3_02 | B1 |
| 22 | CHART native bar | Real CAGR FY19–24 | m3_03 | B1 |
| 23 | CHART native bar | Months of cash FY2024 | m3_04 | B1 |
| 24 | CHART PNG | 20 small multiples of government share FY17–25 | m3_05 | B1 |
| 25 | CHART native bar | Institutional grants as share of revenue, with funder counts; DAF share column | m3_06, m3_00 | B2 |
| 26 | CHART PNG | Four case-study mix charts | m3_08 | B1 |
| 27 | CHART native bar | OVSJG FY2026 and CoC FY2025 awards to peers | m3_09 | fact_gov_awards; A2 |
| 28 | CHART native stacked column | DC-sector grants by year, institutional vs DAF | m4_01 | C1 |
| 29 | CHART native bar | Top 25 institutional funders, colored by Calvary status; concentration curve inset | m4_03, m4_04 | C1 |
| 30 | CHART PNG range | Grant size by funder type | m4_05 | C1 |
| 31 | CHART native bar | DAF sponsors to DC sector | m4_06 | C1 |
| 32 | CHART native bar | Purpose tags; mission-tagged funders | m4_07, m4_08 | C1 |
| 33 | CHART native bar | Peer-funder gaps (23 with 3+ peers) | m5_01 | C1 |
| 34 | CHART native bar | Lapsed funders with first/last year | m5_02 | C1 |
| 35 | CHART native bar pairs | Current-funder headroom: largest grant to Calvary vs to a peer | m5_03 | C1 |
| 36 | CHART native bar | CRM reconciliation by status | m5_06 | supp_crm_cash_verification; C1; assumptions A1–A2 (Prompt 1) |
| 37 | CHART PNG | Network diagram | m6_03 | C2 |
| 38 | CHART native bar pairs | Co-funding overlap by peer | m6_02 | C2 |
| 39 | TABLE | Interlocks: high-confidence rows (funder-related) and medium rows labeled unconfirmed; candidate_interlocks count | m6_04 | fact_org_relationships, dim_person; C2 (person_id only) |
| 40 | TABLE | Scoring dimensions, evidence, weights; tier rules | config/scoring_weights.yaml | C3 |
| 41 | TABLE | Tier 1 rows with scores and tracks | m7_00 | C3 |
| 42 | CHART native stacked bar | Tier 1 score decomposition | m7_03 | C3 |
| 43 | TABLE | 90-day plan with application notes | m7_01, m7_04 | C3; sources/web_tier1_guidelines.csv |
| 44 | TABLE | Sensitivity: ranks under ±0.05 weight changes and alternative tier cutoffs | m7_05 (sensitivity run) | C3 |
| 45 | CHART native bar | Expansion scan by area with distance | m8_01 | D1 |
| 46 | TABLE | Options and trade-offs | m8_01 | D1 |
| 47 | TABLE | Relevant federal notices (36) grouped by agency | m8_02 | fact_opportunities (Grants.gov) |
| 48 | CHART native grouped column + PNG map | Ward indicators; ward poverty map with Calvary's site | m9_01, m9_05 | dim_geo (ACS), DC Open Data wards |
| 49 | CHART native line + stacked column | DC PIT; Calvary HIC inventory | m9_02, m9_03 | supp_homeless_counts, supp_hic_projects |
| 50 | CHART PNG | DWC and CBWC trajectories; DWC federal programs | m10_01, m10_02 | fact_org_financials, fact_gov_awards (FAC); B3 |
| 51 | TABLE | Comparator profiles: programs, funders, what transfers | m10_03–05 | fact_grants web rows; B3 |
| 52 | STAT | Verdict tiles and one paragraph | verdict | recommendations/funding_pressure_verdict.md |
| 53 | HEADLINE | Five recommendation areas with the target arithmetic ($3M private in three years; 50% share; six-month reserve) | — | recommendations/strategic_recommendations.md |
| 54 | TABLE | Open flags D1–D3 and documents requested | discoveries_log | discoveries_log.md |
| 55 | HEADLINE | Appendix map and register status | — | insight_register.csv |
