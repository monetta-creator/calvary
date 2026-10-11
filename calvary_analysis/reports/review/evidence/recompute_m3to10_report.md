# Independent recompute, M3–M10 and appendix sample

Scope: leadership deck slides 13, 14, 16, 17, 21, 22, 23; consulting deck slides 22–30, 32–35, 37–39, 42–43, 53, 60–61; every 10th numeric table cell of appendix B and appendix C. All values recomputed from `calvary_funding_data/clean/` with the scripts in this directory (`00_load_cache.py` → `01_m3.py`, `02_m4_m5_m6.py`, `03_m8_m10.py`, `04_appendix_sample.py`, `05_assemble.py`; `ROOT` in `common.py`). Chart-data files and analysis scripts were not read. Output table: `recompute_m3to10.csv` (item, as_shown, recomputed, match, notes).

## Tally

| match | count |
|---|---|
| exact | 628 |
| rounding | 10 |
| MISMATCH | 5 |
| skipped (labels, scores, duplicates, out-of-scope tables) | 283 |

Appendix sample: 5,445 numeric cells in document order, 544 sampled (every 10th), 263 recomputed (261 exact, 2 rounding), 281 skipped with a reason in `notes` (pipeline scores/tiers keyed only by rank, path-strength and board-link columns, rank labels, config values, duplicates of main-deck items, board-interlock filing years).

## Mismatches

1. **Sector distributions, stated rule (consulting 23, appendix B11; items `M3.sector_dist.*.stated_zero_fill_rule`).** The method line says "organizations with no government line counted at 0%". That rule gives dc_sector FY2023 median 0%, n=425, Calvary at the 84th percentile; size_matched FY2022 median 3%, n=556, 74th; national_women FY2022 median 0%, n=1,124, 74th. The numbers on the slide (37% / n=163 / 57th; 56% / 334 / 57th; 65% / 542 / 46th) reproduce exactly only when organizations with a blank line 1e are **dropped**. The values are right; the stated convention is the opposite of the one applied. Appendix B11 also says "p10 is 0% in every universe" because of zero-filling; under the drop rule p10 is still 0% (filers reporting $0), so that sentence happens to hold. Fix the method text, or re-run with zero-fill and change the numbers.

2. **Miriam's Kitchen "tripled since FY18" (leadership 13; `M3.miriams_tripled_since_fy18`).** Preferred 990 revenue FY2018 $4.66M → FY2024 $11.33M = 2.43× nominal, 1.95× in 2024 dollars; FY2025 $12.96M = 2.78× nominal. "Nearly tripled" or "2.4×" would be accurate; "tripled" is not.

3. **"All 23 filed itemized lists in TY2023+" (consulting 37; `M5.all_23_itemized_TY2023plus`).** 22 of 23. Melamed Foundation (3 peers) has filed grant rows only for TY2020 and TY2021 — no row of any kind in TY2023+, so its absence from Calvary's funders cannot be called current. Appendix C10–15 shows "yes" in the Itemized column for every row, so the same issue is there.

## Items that reproduce only under a convention not stated on the slide (classified exact, flagged in notes)

- **15 current funders with a larger peer grant (consulting 39, `M5.current_funders_bigger_peer_grant`).** Under the stated rule (filed Calvary grant TY2020–24, largest single peer grant > largest Calvary grant) the count is 27 (20 excluding DAF sponsors). It is 15 only for non-DAF funders that fund at least two core peers, which is the 25-row universe of appendix C17–18. The pairs on the slide (Cafritz, GWCF, Bank of America, United Way NCA, Fowler, Ludwig, Jacquemin, Dreyfus, Shaver) all match exactly.
- **12 lapsed funders / $256,150 (consulting 38, `M5.lapsed_*`).** Reproduces with DAF sponsors excluded (slide 37's method says so; slide 38's does not). With all funder types: 14 funders, $305,018 (adds PayPal Giving Fund TY2020 $41,636 and Blackbaud Giving Fund TY2022 $7,232). The 12 listed names and amounts match exactly.
- **M8 area pools (leadership 21, consulting 53, appendix C66).** Every dollar figure, funder count and median matches exactly, but only when "DMV" means **recipient state in DC/MD/VA**, not "DMV institutional funders" (funder in the dmv_funders universe), which the slide text says. Funder-side DMV gives e.g. workforce $38.4M/yr, health $104.9M/yr. "General operating excluded" means grants tagged only general_operating carry no area tag; grants carrying an area tag plus general_operating are still counted (dropping them would give workforce $29.6M, behavioral health $17.9M).
- **Appendix B6/B7 funder-base table** does not apply the landscape exclusions (Miriam's Kitchen institutional $5.61M includes a $25K TCP grant); the M4/M5/M6 tables do. Consistent with slide 28, but worth a footnote.
- **Appendix B13/B14 "Other" revenue** is floored at $0 where the residual (total − contributions − program service) is negative (N Street Village FY2025 −$42,672; Miriam's Kitchen FY2022 −$82,470).

## Rounding notes

- Corporate-foundation median grant: $570 (appendix C7 shows $570); consulting 34 rounds to "$1K (matching gifts)".
- DWC "3× since 2018": 2.97× nominal, 2.38× real; the deck does not say nominal. "5.5× in a decade" (appendix B18) is 5.45× nominal, 4.12× real.
- Federal notices (36): a mechanical filter (agency prefix HUD/VA/DOL/DOJ/ACF/SAMHSA/USDA/Treasury/ACL, then drop titles matching research/tribal/rural/overseas/evaluation/statistics/agriculture/forestry/academic) keeps 41 of 286; 34 of the deck's 36 are in that set. The deck keeps two I drop (an NIJ evaluation and a BJS statistics notice) and drops seven I keep (an ETA guidance letter, three HUD PIH notices, two BJA notices, SAMHSA TI-27-001). Agency filter alone gives 52. The count moves by about ±6 with keyword choice; treat 36 as a curated list, not a reproducible count.
- Government-share FY22–24 means differ from the shown long-precision values by ≤1e-4 for Christ House, Covenant House DC and Everyone Home DC (display-level).
- Miriam's Kitchen FY22–24 government share (0.49%) is a one-year mean: FY2023 and FY2024 line 1e are blank in the XML rows and were dropped, consistent with the drop rule above. Zero-filling would give 0.16%; typology unchanged.

## Everything else

Exact: all 21 government shares and the 11th-of-19 rank; typology 7/11/3; all real CAGRs incl. Calvary 13.8%; all months of cash incl. Calvary 5.23 (FY24) and 4.4 (FY25); institutional grants ÷ revenue and funder counts for all 20; DAF shares; OVSJG FY2026 and HUD CoC FY2025 awards; Samaritan Inns 72% (FY2022) → 11% (FY2025); N Street Village 42% mean; M4 by-year dollars, $660M/$132M/58%/555 funders/1,027 orgs, top-20 funders and values, top-10 = 55.2%, six of 25, DAF sponsor totals, grant-size percentiles and n=3,288; M5 23 gap funders with peer counts, 75 of 2+, Clark $7.83M/5 peers/$250K/$32.8M/20 recipients, CRM status totals ($10,556,076; 43.9%); M6 330 funders/58 of 3+, all orgs-funded counts, all shared and not-shared counts; M8 $149.22M near total and 206 health funders at $100K+; M10 DWC and CBWC figures and SEFA totals.
