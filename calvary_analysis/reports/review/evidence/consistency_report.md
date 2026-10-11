# Cross-document consistency check

Scope: 50 metrics compared across the seven deck text exports (`decks_md/`), the reports, recommendations, pipeline and action-plan CSVs, insight register, module readouts M1–M10, headline spines, README and the CP3 memo. Files: `consistency_matrix.csv` (505 rows, one per metric × document) and `disagreements.csv` (39 rows: 11 substantive, 13 rounding, 15 wording). Chart-data CSVs were read only to settle which side of a disagreement matches the build (`m1_summary_numbers`, `m3_00`, `m4_01`, `m4_04`, `m5_02`, `m5_04`, `m6_04`, `m6_05`, `m8_02`, the pipeline CSV).

## Overall

The headline numbers are stable across every audience document: 59% real growth, 68 → 124 beds, 6.8% of TH beds, $4.1M award base, 50 funders, 53% / 58% government share, 11th of 19, 57th / 46th percentiles, $1.05M OVSJG, $1.77M CoC, $1.42M DHS, $0.64–1.17M from 26–29 funders, GWCF 27% / top five 63%, DAF $1.1M / 25%, −$607K, $538K → $55K, 4.4 / 7.5 / 5.2 months, all six scenario losses and the 1.7-month combined case, 41 months to zero, $132M / $660M / 58% / 555, 23 / 75, Clark $7.8M / $250K / $32.8M, 12 lapsed, 15 headroom, 44% of $10.6M, 330 funders, 17 / 14 / 14, 182 rows, 36 notices, ward and PIT figures, the CBWC series, the $2.8M reserve and $2.1M → $3.0M target, and the eleven Tier 1 names.

The substantive problems concentrate in two places: `reports/full_findings.md`, which was not refreshed after the CP3 consistency pass, and slide-count or basis labels that mix years or measures.

## Substantive disagreements

1. **`reports/full_findings.md` is stale after CP3 (metrics 9, 10, 29, 38, 48).** Its M1 table still shows the mixed-denominator shares (FY19 51%, FY21 51%, FY22 64%, FY23 55%) that the memo says were replaced by the audited-denominator series (49 / 50 / 61 / 51), while its own text says 40–61%. Its M7 section lists twelve Tier 1 rows including Frontier Co-op at 0.60, its register summary says "12 Tier 1, 40 Tier 2" and its consistency note #11 says 12 / 39 / 131; every other document, the pipeline CSV and the action plan say 11 / 40 / 131. Its copy of M3-01 still gives DV providers 75–94% and classes Samaritan Inns as philanthropy-led (register now 70–89%, mixed). Its M4 finding puts institutional dollars at "42% ($260M)" of $660M; the module and `m4_01` give $276M. Consistency notes #1, #5, #7, #10 and #11 describe readout values that no longer exist (324 funders, 561 institutional funders, no rank).

2. **"74% of a $4.1M award base" mixes bases (metric 12).** 74% is CoC 41% + DHS 33% of the FY25-aligned ceilings ($4.29M, appendix A slide 22 and the M2 scenario method). On the 2024 award base that the $4.1M refers to (OVSJG $0.91M + CoC $1.76M + DHS $1.42M), TCP's share is 78%. The phrase appears in the one-pager (both forms), executive summary, recommendations, consulting briefing, strategic recommendations, leadership slides 2 and 5 and consulting slide 63.

3. **Leadership slide 3 labels nominal revenue as real (metrics 1–2).** "$2.49M → $4.97M, 2024 dollars" are the nominal figures; appendix A slide 4 gives the 2024-dollar series as $3.05M → $4.84M (+59%). The one-pager report and executive summary pair the real growth rate with the nominal endpoints without a label.

4. **Deck slide counts disagree (metric 47).** Leadership deck: "21 slides" (one-pager report), "22 content slides" (one-pager deck, briefing), "22 content slides plus five section dividers … 26 total" (README, CP3). The export has 26 slides = 22 spine slides (title and closing included) + 4 dividers; the "Where Calvary stands" divider named in the spine is not in the deck, and 22 + 5 ≠ 26. Consulting slide 66 states Appendix A 17, B 12, C 21, D 24 slides against 22 / 21 / 69 / 33 in the CP3 memo and the exports.

5. **Benchmark table organization count (metric 47, also M3).** Module M3, full findings and the appendix spine say the benchmark table and the small multiples cover 20 organizations; appendix B says 21 and `m3_00` has 21 rows (Calvary + 18 peers + 2 comparators).

## Worth a line, not a fix cycle

- Lapsed-funder total: $255K in M5, full findings and the consulting deck; $256K in appendix C, whose table sums to $256,150 (rounding slip toward the wrong side).
- DWC growth multiple: register magnitude "6x" vs ×5.5 everywhere else; leadership slide 13's "3× since 2018" is a different base and is correct on it. DWC months of cash "2–3" vs the appendix B range 1.8–4.4.
- Consulting slide 61 attributes DWC's 280 donor-list names to the 2023 list; M10 gives 202 (2023) and 148 (2025), 280 being the distinct total.
- Board interlocks: M6 says "across all 19 organizations, 27 interlocks touch a funder, 3 high"; `m6_04` has 56 rows, 33 touching a funder (27 once Calvary's own are removed), 4 high overall. Appendix C states 56 / 4 / 52. Both are reproducible, but the M6 sentence's filter is not what it says.
- Appendix B's benchmark "latest" government share is FY2024 for every row, so CBWC shows 85% there and 70% (FY2025) on its own slide and in the consulting deck.
- The verdict's evidence table quotes the 2024 OVSJG and CoC awards ($0.91M, $1.76M) while the executive summary and decks quote FY26 / FY2025 ($1.05M, $1.77M); full_findings note #13 already flags that these should not be mixed, and the executive summary does mix them in one sentence.
- "Top 10 = 55%" (register, CP3, consulting headline) vs "about half" (M4, full findings, consulting slide body); `m4_04` gives 55.2%.
- M7 and the recommendations report count "12 federal notices" in Tier 3 while M8 and the decks count 36 relevant notices; neither says one is a subset of the other.
