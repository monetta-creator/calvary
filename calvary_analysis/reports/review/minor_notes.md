# Minor notes

Below the materiality bar: style, wording, documentation and small caveats. Ids M01–M13 are rows in `review_findings.csv`; the rest are listed here only.

## From the findings file (M01–M13)

- M01 "All 23 filed itemized lists in TY2023+" is 22 of 23 (consulting slide 37, full findings).
- M02 $131,906 from two Baltimore-area funders is attributed to My Sister's Place (DC) but belongs to a Baltimore namesake; its institutional depth is slightly overstated.
- M03 Three pipeline rules live only in `scripts/07_m7_pipeline.py`: the Tier 2 cap for DAF-like channels (T. Rowe Price), the DC-sector-median fallback for typical grant (31 rows; Coca-Cola's Tier 2 place depends on it), and the drop of current funders under $10K.
- M04 Traceability: source_ids are module-wide, several named tables' ids are missing, two leadership footnotes cite the wrong charts (74% on slide 5; $2.8M on slide 22), the committed folder holds an orphan CSV (`m1_04_surplus_net_assets`) that `full_findings.md` references and no script writes (trace.py fails on a clean regeneration), and `m6_03_network_nodes` is not byte-for-byte reproducible.
- M05 Slide counts disagree (leadership "21 slides" vs "22 content slides" vs 22 + 4 dividers in the file; consulting slide 66's appendix counts 17/12/21/24 vs 22/21/69/33).
- M06 OVSJG 2019 sums two Reach Up records ($292,000 and $368,935) from the same open-data layer; DC PASS shows a $208K FY19 obligation. "$0.9M (2019)" on consulting slide 14 and in M2-01 may be about $0.6M.
- M07 Small slips: "20 organizations" vs 21; lapsed $255K vs $256,150; DWC "6x" (register) vs 5.5x (CP3) vs "3x since 2018" (slide 13; 2.97x nominal, 2.4x real); "280 names on the 2023 list" is both lists; "Benevity, Fidelity, Schwab add $1.1M" (the three sum to $0.95M); slide 5 shows "other federal" as 0 for 2024–25 while the ceiling base carries $106,673 forward; slide 4's "other revenue" is floored at zero so stacked categories exceed total revenue in 9 of 11 years; the verdict quotes 2024 awards where the decks quote FY26/FY2025.
- M08 JPMorgan Chase and Bank of America sit in Tier 2 with $100 typical grants (matching gifts); label them channels.
- M09 The TCP exclusion rationale says its Schedule I grants are already counted; TCP's returns carry one Schedule I row ($3M, TY2023) and none in TY2024–25, so there is no itemized TCP list to exclude or fall back on for DHS values.
- M10 Appendix decks fail `headline_check.py` (10/10/38/13 flags) by design; record the exemption or add an appendix mode.
- M11 README and the consulting briefing point at `reports/review_report.md`, which does not exist; this review's folder replaces it (README append done here; the briefing edit belongs to the fix cycle).
- M12 Corporate-foundation median grant is $570, shown as $1K.
- M13 "15 current funders with headroom" depends on an unstated filter (non-DAF funders of 2+ peers); 20 over all current institutional funders.

## Other notes

- Miriam's Kitchen "tripled since FY18" (leadership slide 13): 2.4x nominal, 2.0x real to FY24; 2.8x nominal to FY25.
- Samaritan Inns "72% → 11%" uses the FY22 peak; its typical share was 50–57% before FY24, and the methodology itself notes its FY24–25 program-service revenue rose at the same time, so part of the "replaced government with program revenue" story may be a reporting change. Worth a sentence on slide 13 before it carries the behavioral-health-credential recommendation.
- Leadership slide 6: "held steady near $1M a year" describes TY2020 $0.64M, TY2021 $0.81M, TY2022 $1.16M, TY2023 $0.66M, TY2024 $1.17M (partial); "oscillating with the Health Equity Fund rounds" is closer.
- DHS continuum "$170M (FY24)": FY2025 actual in the CFO book is $178.8M; state the basis of the $170M.
- The "TCP's DHS purchase orders fell sharply in FY2025" line (consulting slide 15) is an observed pattern in the PASS pull with no public corroboration; the documented FY2025 DHS payment delays (October 2024 to January 2025, new grants and contracts software) are the citable event.
- Health Equity Fund: about $84M of $95M committed by January 2026; the December 2025 round was coalition-only; no wind-down or successor announced. "Ask about a successor" should read "no successor announced; ask".
- The 2025 Hope Award went to GWCF's chief executive (public record); a relationship signal the materials could mention by role.
- Many Hands: 2027 cycle 4–15 January; Calvary's cumulative $79.5K keeps it eligible under the $100K cap; Impact Grant $100K+. Worth promoting in the day-60 list.
- `analysis_log.md` shows the first two env-check runs failing on row counts (fact_gov_awards 42,958; entity_aliases 231,647 vs 231,678) before the counting rule was fixed; the log is honest about it, and the final state passes.
- `analysis_plan.md` and `input_map.md` mention `~/.config/calvary/keys.env` by path; allowed documentation references, no key material anywhere.
- The three non-person rows in `dim_person` (a "see attached" placeholder and two parse artefacts) generate most of the false name hits in the guardrail scan; a Prompt 1 clean-up item.
- Appendix D's "231,647 entity_aliases rows" has no chart id; it is a documentary number and verifies directly.
- Register status is `draft` for all 36 rows, as expected before the fix cycle.
- M8 pools reproduce only when "DMV" means recipients in DC/MD/VA (not DMV funders, as the slide says) and when "general operating excluded" means grants tagged only general operating carry no area tag; appendix B6–7 do not apply the landscape exclusions that other slides apply. State the conventions.
