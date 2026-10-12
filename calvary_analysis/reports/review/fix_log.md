# Fix log: review findings → changes (2026-10-11)

Every finding in `review_findings.csv` with what changed and where. Canonical wording is in `fix_spec.md`. Numbers come from the rerun of modules 01–10, 12 and 13 on 2026-10-11. "Decks" means the build scripts in `decks/` and the rebuilt PPTX, PDFs (`decks/pdf/`) and QA images. "Reports" means the Markdown deliverables in `reports/` and `recommendations/`.

| Finding | Change | Where |
|---|---|---|
| R01 stress test apportionment | Losses are ranges across three splits of FY25 government revenue (ceiling share; CoC at its FY22–23 SEFA draw rate with DHS the residual; without Sisters Rise) plus a floor case. DHS/TCP lost: $0.65–1.13M (13–23%); combined: $1.05–1.47M, 1.5–2.0 months of cash. Range bar chart | `scripts/02_m2_exposure.py`, `chart_data/m2_07_*`, `charts/m2_07_scenarios.png`, register M2-05, leadership slide 10, consulting slide 20, Appendix A slide 22, reports, M2 readout |
| R02 TCP share basis | "78% of the $4.1M 2024 award base" everywhere | decks, reports, M2 readout, register M2-01 |
| R03 nominal labelled as 2024 dollars | "$2.49M → $4.97M nominal, +59% after inflation ($3.05M → $4.84M in 2024 dollars)" | leadership slides 2–3, consulting slide 7, reports, M1 readout |
| R04 contact details in a cached snippet | Row 58 of `sources/web_tier1_guidelines.csv` redacted | `sources/web_tier1_guidelines.csv` |
| R05 board-link confidence | "High" now needs overlapping board terms; a funder needs a filed grant. Calvary has no high-confidence links (eight medium, unconfirmed) | `scripts/06_m6_network.py` (`confidence_source` column), `chart_data/m6_04`, register M6-03, leadership slide 17, consulting slides 44–45, Appendices C and D, M6 readout |
| R06 America's Charities in Tier 1 | Workplace-giving channel, capped at Tier 2 with a CFC enrollment step | `config/scoring_weights.yaml` (`channels`, `next_step_overrides`), `scripts/07_m7_pipeline.py`, pipeline and plan CSVs |
| R07 sector percentile method | 57th percentile among organizations reporting government revenue; 84th (DC) and 74th (national) against all filers; "typical" rests on 11th of 19 | `scripts/03_m3_peers.py`, `chart_data/m3_07`, register M3-02, leadership slide 4, consulting slide 23, Appendix B slide 11, reports, M3 readout |
| R08 upgrade steps | Peer-level multi-year ask for Cafritz and Fowler only; GWCF two conversations; Abell steward and renew | `config/scoring_weights.yaml` `next_step_overrides`, plan CSV, leadership slides 19–20, reports |
| R09 capacity | 90-day plan sequenced for six fundraising positions; the unfunded FY2026 workforce position is the first cost of the workforce option (Calvary-facing only) | `scripts/07_m7_pipeline.py` deadlines, leadership slides 19 and 21, consulting slide 54, reports, M7 and M8 readouts |
| R10 peer-set sensitivity | Only Schattner is named as a new prospect in leadership materials; funders of exactly three peers are marked as depending on the provisional peer set; 11th → 12th of 19 under the swap is stated | `peer_set_note` in the pipeline, leadership slide 16 (asterisks), consulting slide 37, reports, M5 readout |
| R11 stale full findings | `reports/full_findings.md` is now generated from the readouts, register, verdict and discoveries log | `scripts/lib/full_findings.py` |
| R12 beds basis | "124 beds across transitional, permanent supportive and rapid-rehousing programs; its 94 transitional beds are 6.8% of DC's" (68 beds in 2022) | register M9-02, leadership slides 2–3, consulting slide 58, reports, M9 readout |
| R13 channels on the peer-funder slide | Leadership chart shows the 15 grantmakers; the six channels, Clark and Venable are counted in the card. Consulting chart does the same and lists the eight by name | leadership slide 16, consulting slide 37, Appendix C status column, reports, M5 readout |
| R14 draw-down already visible | FY22–23 single audits show CoC spending at 28% and 58% of prior-year CoC awards; recommendation is "reconcile CoC draw-down first, then DHS" | leadership slides 2, 11 and 19, consulting slide 16, Appendix A, D1 in `discoveries_log.md`, reports |
| R15 FY25 event "collapse" | Event receipts = 990 lines 1c + 8a: $596K (FY24), $533K (FY25). The FY25 return moved the gala to line 8a. "Restore the event line" dropped; the $3.0M target rebuilt without an events component; flag D3 closed | `scripts/01_m1_trajectory.py`, `chart_data/m1_06_events.csv`, `charts/m1_06_event_income.png`, register M1-02 and M1-03, leadership slides 2 and 7, consulting slide 11, Appendix A slide 5, Appendix D, reports |
| R16 Clark sunset | Clark marked `sunset` (closed 31 Dec 2025): excluded from tiers and prospect lists; its giving described as a spend-down | `config/guideline_notes.csv`, `scripts/07_m7_pipeline.py`, `scripts/05_m5_gaps.py`, decks, reports, readouts, web page status tag |
| R17 open status | `open_status` column with note, source and date: Schattner, Abell, Cohen invitation-only; Venable and Meyer closed to new applicants; invitation-only funders get an introduction step, never an LOI. Status column on the Tier 1 table | `config/guideline_notes.csv`, `scripts/07`, `scripts/12_merge_guidelines.py`, leadership slide 20, consulting slide 50, Appendix C, web page |
| R18 federal and DC dates | FY2026 CoC competition (awards about December 2026), EHV ends 31 December 2026, FY27 OVSJG restoration $5.1M one-time plus $0.5M recurring | leadership slides 9, 19 and 22, consulting slides 18 and 63, reports, M2 readout, `reference/source_quirks.md` |
| M01 itemized count | "22 of 23" | consulting slide 37, M5 readout |
| M02 Baltimore namesake grants | Seven rows ($131,906 TY2020–24) excluded on every load; network 328 funders, $69.9M | `config/grant_exclusions.csv`, `scripts/lib/common.py` `load()`, all modules rerun, web page |
| M03 undocumented pipeline rules | Rules documented in `config/scoring_weights.yaml`; consulting slide 47 lists them | `config/scoring_weights.yaml`, consulting deck, methodology |
| M04 orphan chart data | `chart_data/m1_04_surplus_net_assets.csv` deleted and its manifest row removed; trace passes | `chart_data/`, `reports/methodology.md` |
| M05 slide counts | Leadership 22 headline slides plus 4 dividers; consulting 66; appendices 22, 21, 70 and 33 | spines, README, decks, reports |
| M06 2019 OVSJG value | Series quoted from 2020 ($0.6M) with a note on the two 2019 Reach Up records | `scripts/01`, `scripts/02`, register M2-01, consulting slide 14, M2 readout |
| M07 small figures | 21 organizations; lapsed per N01; DWC 5.5x since FY2014 and 3x since FY2018; "280 names across the two 2023 lists"; Benevity, Fidelity and Schwab $0.95M | register M10-01, decks, reports, readouts |
| M08 matching-gift channels | JPMorgan Chase and Bank of America labelled matching-gift channels | `config/scoring_weights.yaml`, pipeline, Appendix C |
| M09 TCP exclusion reason | "Pass-through intermediary with no itemized Schedule I" | consulting slide 32, methodology, M2 and M4 readouts |
| M10 appendix headline check | `headline_check.py --appendix=A..D`; drift is a warning in appendix mode | `scripts/lib/headline_check.py`, `decks/build_all.sh` |
| M11 pointer to a missing report | Pointers now go to `reports/review/` | README, consulting briefing |
| M12 median grant | "Under $1K" ($570 over 601 rows) | M10 readout and reports |
| M13 headroom filter | "Among current funders that also fund two or more peers" stated | consulting slide 39, M5 readout |
| N01 World Bank CCF | One-time capital-campaign grant, not lapsed: lapsed funders are 11 ($156,150); World Bank CCF is an employee-giving channel | `scripts/05_m5_gaps.py`, `chart_data/m5_02`, register M5-02, consulting slide 38, Appendix C, web page Lapsed view (14) |
| N02 Many Hands | Not eligible while Calvary's budget is above $5M; removed from re-engage steps, Tier 3 | `config/guideline_notes.csv`, pipeline, decks, reports |
| N03 Abell grant year | $270K was TY2021; latest filed $25K (TY2023) | `config/scoring_weights.yaml` override, reports, M7 readout |

## Further changes made in the same cycle

- **Status checks beyond the review:** Bunting Family Foundation and Brendan & Helen Bechtel Foundation (no public application process; Tier 3, not plan targets) and Jane Bancroft Robinson Foundation (grants by periodic RFP) were checked and recorded in `config/guideline_notes.csv` with registry rows.
- **Register text** for M2-03, M4-02, M4-03, M5-01, M9-01 and M10-01 was brought in line with the spec (closed funders, tone words, magnitudes).
- **Tone:** "exposed", "exposure" and "dependency" removed from the verdict, the strategic recommendations, the 90-day step text and the consulting deck's section 3 title; `design_system.md` §6 now agrees with the CP2 voice ruling.
- **Charts:** every horizontal native bar chart labels every bar (`decks/lib/deck.js`).
- **Tooling:** `decks/build_all.sh` and `decks/lib/theme_colors.js` make the deck build self-contained; `scripts/lib/full_findings.py` regenerates the full findings report.

## Re-verification

An independent read-only pass checked every finding against the rebuilt PDFs, reports, readouts, register and chart data. Its report and the follow-up fixes are summarized below.

The pass (2026-10-11, read-only, against the PDFs, reports, readouts, register, chart data and the web page) rated 20 findings fixed, 13 partly fixed and 1 not fixed, and confirmed that every number on the leadership surfaces matches chart data. The follow-up fixes, all made the same day:

| Finding | What remained | Follow-up |
|---|---|---|
| R01, R14 | Appendix D method notes A4 and A5 still described one split and no SEFA comparison | A4 and A5 rewritten (three splits, floor case, ranges; CoC draw rates 28% and 58%) |
| R10 | Leadership slide 16 presented the three-peer and Tier 3 funders under "Warm cold prospects" | Card retitled "Who already funds Calvary's model": only Schattner is a checked target, the rest need a status check and the confirmed peer set; three-peer names no longer offered as prospects in the strategic recommendations and the recommendations report |
| R12, M06 | Appendix D showed old register text | Rebuilt after the final rerun |
| R18 | Durability table (m2_03), register M2-06, Appendix A and D still said "2025 CoC NOFO shifted priorities" and "EHV sunset" | Re-dated in `scripts/02_m2_exposure.py` and Appendix D, rerun |
| M04 | Leadership slide 22 footer cited a PNG id and nothing for the $2.8M reserve | Footer now cites m3_00, m2_07 parameters and m2_06. Chart-data `source_ids` remain module-wide supersets (listed as a limitation in methodology) |
| M05 | Slide and page counts disagreed (Appendix C 69 vs 70; consulting 55 vs 66; README dividers) | Counts aligned |
| M07 | Appendix spine said 20 organizations | 21 |
| M09 | Appendix D quoted the Prompt 1 line "TCP Schedule I is the fallback" | Slide quotes the correction; the Prompt 1 report is left untouched |
| M11 | README review section named the missing report | Reworded |
| M12 | Consulting slide 34 said "median $1K" | "Median under $1K ($570)" |
| M13 | Executive summary and register M5-03 lacked the filter | Filter added to both |
| N01 | Web page Lapsed view counted 14 (DAF sponsors and an unclear funder included) | Web page uses the M5 definition: 11 funders, $156,150 |
| New | "live exposure" in the verdict and briefing; "largest single exposure" in the pipeline note; consulting section title "Government exposure"; semicolons in seven consulting dividers and one leadership divider; the board readout said three plan fronts; the Appendix D discoveries table overflowed; the briefing listed Jane Bancroft Robinson as unverified; slide 39 counted lapsed funders as current without saying so | All fixed; dividers rewritten as single sentences; readout now four fronts; table shows the latest response per flag; "current" defined on slide 39 |

After these fixes the modules were rerun in order, `full_findings.md` regenerated, all seven decks rebuilt (headline checks pass), the web page rebuilt, and `trace.py` printed TRACE OK. All 36 register rows are marked `verified`.
