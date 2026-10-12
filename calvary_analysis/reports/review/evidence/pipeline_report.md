# Funder pipeline review: independent recomputation

Scope: `calvary_analysis/recommendations/funder_pipeline.csv` (182 rows) against `calvary_analysis/config/scoring_weights.yaml` and the clean tables. Scripts: `00_extract_grants.py` (one pass over fact_grants, 424,888 rows kept for the 182 pipeline funder_ids), `01_pipeline_review.py` (steps 1-5). Outputs in this directory. Steps 1-3 were done before reading `07_m7_pipeline.py`; the script was read afterwards only to explain the two items marked "resolved by reading the script".

Row classes: 154 rows carry numeric component scores (7 Tier 1, 28 Tier 2, 119 Tier 3); the other 28 are government (5), CRM corporate (11) and Grants.gov opportunity (12) rows with analyst scores and no components.

## Step 1: arithmetic and tier rule (pipeline_arithmetic.csv)

- Score: 154 / 154 rows reproduce `score = sum(weight_i * s_i)` within 0.0005 (file scores are rounded to 3 dp; max |diff| = 0.0005, i.e. rounding only).
- Tier rule (Tier 1 iff score >= 0.62 and typical_grant >= 25,000, cap 20; Tier 2 iff score >= 0.48): 153 / 154 rows follow it.
- One exception: rank 19, 311709466 (T. Rowe Price Program for Charitable Giving), score 0.624, typical_grant 25,029, is Tier 2 in the file but qualifies for Tier 1 under the documented rule. Resolved by reading the script: line 59 of `07_m7_pipeline.py` holds `daf_like_channels` at Tier 2 or lower (`tier = max(tier, 2)`). This rule is not stated in the yaml or in the yaml comment on `daf_like_channels`; it is a judgment call that should be documented in the config.
- No Tier 3 institutional row has a score >= 0.48.
- Non-institutional rows: 4 CRM corporate rows (Altria 0.469, Courembis 0.463, CareFirst 0.463, Hyde 0.450) and GOV-FED-2 (0.450) sit in Tier 2 below the 0.48 cutoff; 8 opportunity rows with scores 0.50-0.60 sit in Tier 3. These rows are placed by their own rules (corporate: Tier 1 only if CRM total >= 250K and score >= 0.62, else Tier 2; opportunities: Tier 3), so this is informational, but the pipeline CSV does not say so.
- Tier 1 cap (20) is not binding: 11 Tier 1 rows total (7 institutional, 3 government, 1 CRM corporate).

## Step 2: component scores from the evidence columns (pipeline_components.csv)

All 154 rows reproduce for every component checked:

| component | formula used | matches |
|---|---|---|
| s_peer_giving | min(peers_funded / 8, 1) | 154 / 154 |
| s_award_size | log-linear of typical_grant, 5,000 -> 250,000, clipped 0-1 | 154 / 154 |
| s_regional_giving | log-linear of dc_sector_amount, 50,000 -> 10,000,000, clipped 0-1 | 154 / 154 |
| s_accessibility | type score (private foundations split at 20 / 8 DC-sector recipients) - 0.15 placeholder - 0.30 in-kind; 0.15 for 311709466 | 154 / 154 |

Notes:
- typical_grant equals median_peer_grant for 123 rows. For the 31 rows with peers_funded = 0, median_peer_grant is null and typical_grant comes from another figure (resolved by reading the script: fallback to the funder's median DC-sector grant, then Calvary's max grant, then 0). s_award_size therefore matched on typical_grant for all rows but on median_peer_grant for only 124. The fallback is reasonable but is not visible in the pipeline CSV; a `typical_grant_basis` column would make it auditable. One Tier 2 row depends on the fallback: 581574705 (Coca-Cola Foundation), typical 150,000 from 5 DC-sector grants and 0 peers.
- The script adds +1 inside the log for award size and regional giving and uses log10; differences are below 1e-5 and inside tolerance.
- mission_fit and durability could not be checked from the pipeline CSV (their inputs, mission_tagged_amount, peer_years and years_active, are not in the file). Not checked.

## Step 3: evidence recomputed from clean tables (pipeline_evidence.csv)

Covered: 7 Tier 1 institutional funders and the 10 highest-scoring Tier 2 institutional funders (ranks 12-21). Definitions used: filed rows = source_type in {pf_grants_paid, schedule_i}, cumulative_flag = 0, tax_year 2020-2024; core peers = 18 EINs in `calvary_funding_data/config/core_peers.csv`; DC sector = 1,027 EINs in dim_universe_membership with universe = dc_sector (9 of the 18 peers are in it).

| evidence column | matches of 17 | note |
|---|---|---|
| peers_funded | 17 | distinct peer EINs |
| peer_amount | 17 | |
| median_peer_grant | 17 | the file's median is over grant rows (one row per filed grant line). Median over per-peer totals matches 1 of 17 and is 2-7x higher for most funders (e.g. Abell 25,000 by rows vs 82,500 per peer; GWCF 32,525 vs 182,900; Cafritz 36,250 vs 150,000). Median over peer-year totals matches 12 of 17. |
| max_peer_grant | 17 | |
| dc_sector_amount | 17 | |
| dc_sector_recipients | 17 | |
| gives_to_calvary_ty2020_24 | 17 | same answer whether restricted to filed rows or any source type |
| itemized_ty2023plus | 17 | |
| placeholder_ty2023plus | 17 | only 200721133 (Bank of America) has placeholder rows TY >= 2023; it also has itemized rows, so both flags are true |

Judgment point from the median choice: "typical grant" per grant row understates what a multi-year or multi-program funder gives a peer per year. With per-peer-year medians, Tier 1 membership would not change (GWCF 35,050; Cafritz 40,000; Abell, Fowler, Schattner unchanged), but Gifts for the Homeless would move from 6,488 to 7,021 and Bank of America from 100 to 550; neither crosses a tier threshold.

Reproduction summary across steps 1-3: 154 / 154 score rows, 153 / 154 tier placements, 154 / 154 for each of four component scores, 17 / 17 for each of nine evidence columns. The only non-reproducing item is the T. Rowe Price tier, explained by an undocumented script rule.

## Step 4: alternative weightings (pipeline_alt_weights.md)

Baseline Tier 1 institutional: Abell, GWCF, Clark, Cafritz, Fowler, Schattner, America's Charities. Changes below are versus the file; government and CRM corporate rows are unchanged in every scenario; the script's DAF-channel cap on 311709466 is kept.

| scenario | Tier 1 added | Tier 1 dropped | Tier 2 added (from 3) | Tier 2 dropped (to 3) |
|---|---|---|---|---|
| (a) equal 1/7 | World Bank CCF (0.622) | none | 8 (Morningstar, Bernstein, Annie E Casey, PepsiCo, Workday, Donors Trust, England Family, Higginson) | none |
| (b) size matters | World Bank CCF (0.627), Weinberg (0.620) | America's Charities (0.600) | 16, mostly large corporate / national foundations with 0 peers (Wells Fargo, PepsiCo, Workday, Donors Trust, Marriott, Martha's Table, Matan, Jack Kent Cooke, Public Welfare, Luminate, ...) | 8 small-check current funders (Give Lively, Dimick, Ludwig, Congressional Sports, ImpactAssets, MoFo, Omidyar, Bloedorn) |
| (c) relationship-light | Weinberg (0.632) | America's Charities (0.620) | 17 (PepsiCo, Workday, Wells Fargo, Donors Trust, Martha's Table, Morningstar, Marriott, Cornerstone, Public Welfare, O'Neil, Washington Area Women's Fdn, Revada, Matan, YWCA USA, Dweck, Wallace Global, Jack Kent Cooke) | 4 (Ludwig, Congressional Sports, Omidyar, Bloedorn) |
| (d) no current-funder bonus (-0.0525) | none | none | none | 5 (Omidyar, Congressional Sports, Jane Bancroft Robinson, Ludwig, Bloedorn) |
| (e) min award 50,000 | none | Abell, GWCF, Cafritz, Fowler, America's Charities (Tier 1 institutional shrinks to Clark and Schattner) | none | none |
| (f) min award 10,000 | Venable (0.780), United Way NCA (0.710), AAMC (0.683) | none | none | none |

Reading: Tier 1 is not just the current-funder list. Removing the current-funder bonus (d) drops no one from Tier 1: the four current funders in Tier 1 clear 0.62 by 0.04-0.18 after the deduction (Fowler closest at 0.665). Tier 1 is more sensitive to the award floor than to the weights: the floor at 25,000 is what keeps Venable, United Way and AAMC out, and raising it to 50,000 removes four of the five current-funder rows. America's Charities is the marginal Tier 1 row under every weighting that de-emphasises relationship (b, c) and under the rel=0.5 test below. Weinberg (Tier 2, typical 75,000, s_relationship 0.248) is the marginal entrant under those same weightings.

Relationship at 0.5 instead of its value (original weights): only America's Charities (0.638 -> 0.608) would fall out of Tier 1; Clark (0.498) and Schattner (0.408 -> 0.687) would rise slightly; the four current funders at 1.0 would lose 0.075 but stay above 0.62 (Fowler closest at 0.642). Weinberg would enter Tier 1 (0.588 -> 0.626).

Caveat on (d): s_relationship is clipped at 1.0 in the file, so for the rows at 1.0 the un-clipped value is unknown and the true effect of removing the 0.35 bonus is at most 0.0525.

## Step 5: flags for judgment (pipeline_flags.csv)

26 flagged rows, 15 in Tier 1/2:

- typical_grant below 5,000 in Tier 1/2 (matching-gift / small-check pattern): 237049738 JPMorgan Chase Fdn (100, Tier 2, 0.712), 200721133 Bank of America Charitable Fdn (100, Tier 2, 0.654), 526035549 Miller & Chevalier (3,700), 526038149 Dimick (3,000), 201173866 Omidyar Network Fund (2,000). JPMorgan and BofA rank 13 and 17 on the strength of regional giving and relationship while their per-grant median to peers is 100; the score does not distinguish an employee-matching channel from a grant program.
- Workplace-giving / in-kind channels in Tier 1/2: 541517707 America's Charities (Tier 1, rank 11), 521593963 Gifts for the Homeless (Tier 2, rank 15), 521167581 Capital Area Food Bank (Tier 2, rank 20), 810693451 Give Lively (Tier 2, rank 26). The 0.30 in-kind penalty leaves them in tier; America's Charities is the only non-foundation, non-current-funder row in Tier 1.
- 311709466 T. Rowe Price Program (Tier 2, rank 19): scored as a DAF sponsor and held at Tier 2 by an undocumented script rule; it would be Tier 1 under the documented rule.
- On Calvary list / CRM but no filed grant TY2020-24 (filing-lag candidates), Tier 1/2: America's Charities, Venable, JPMorgan Chase Fdn, Weinberg, Give Lively, Coca-Cola Fdn, Morrison & Foerster Fdn, Meyer Fdn. Plus 6 Tier 3 rows (PepsiCo, Workday, Wells Fargo, Center for Nonprofit Advancement, Wal-Mart, Morgan Stanley). These rows carry the 0.15 list bonus but not the 0.35 current-funder bonus; if the CRM gifts are real and recent, several are mis-scored downward.
- State outside DC/MD/VA in Tier 1/2: JPMorgan (NY), Bank of America (NC), Give Lively (NY), Coca-Cola (GA), Omidyar (CA), Morrison & Foerster (CA). Tier 3 out-of-region current funders: Alice Shaver (MA), Rapoport (NY), MGM Resorts (NV), RCLCO (CA), Leslie Joanne (CA).

## Items resolved only by reading 07_m7_pipeline.py

1. The T. Rowe Price Tier 2 placement (line 59: daf_like_channels capped at Tier 2).
2. The typical_grant fallback when median_peer_grant is null (line 36: median DC-sector grant, then Calvary max grant, then 0).
3. Two filters applied before scoring that are not in the yaml: DAF sponsors (funder_type = daf_sponsor) removed; current funders with calvary_total_ty2020_24 < 10,000 removed. These explain why some small current funders are absent from the 182 rows; not verified further here.

Everything else (score arithmetic, tier rule, four component formulas, nine evidence columns) reproduced from the yaml, the pipeline CSV and the clean tables without the script.

## Files

- `00_extract_grants.py`, `01_pipeline_review.py`: review scripts (ROOT variable; write only to this directory).
- `grants_pipeline_funders.csv`: cached fact_grants subset (7 columns, 182 funder_ids), used by step 3.
- `pipeline_arithmetic.csv`, `pipeline_components.csv`, `pipeline_evidence.csv`, `pipeline_flags.csv`: sorted by rank.
- `pipeline_alt_weights.md`: membership changes, top-15 tables per scenario, relationship sensitivity.
