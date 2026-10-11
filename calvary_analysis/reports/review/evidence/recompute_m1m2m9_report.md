# Independent recomputation: M1 / M2 / M9 figures (one-pager + leadership deck)

Source of truth: `calvary_funding_data/clean/` only (fact_org_financials, fact_gov_awards, fact_grants, dim_funder, dim_period, dim_geo, supp_hic_projects, supp_homeless_counts) plus the parameter file `calvary_analysis/config/scenarios.yaml`. No chart_data or analysis scripts were read. Script: `recompute_m1m2m9.py` (ROOT variable at top); results: `recompute_m1m2m9.csv` (223 items).

## Tally

| match | count |
|---|---|
| exact | 107 |
| rounding | 95 |
| MISMATCH | 6 |
| not shown (computed for the reviewer, no deck figure) | 15 |

Every arithmetic figure in the deliverables reproduces from the clean tables. All six mismatches are labeling or basis inconsistencies between what a slide says and what the number is, not wrong sums.

## The six mismatches

**A05 — "$2.49M → $4.97M, 2024 dollars" (leadership slide 3; one-pager without the "2024 dollars" tag).** The two figures are nominal FY19 and FY25 revenue. In 2024 dollars they are $3.05M → $4.84M (deflators 1.226992 and 0.974362 by fiscal-year-end year). The +59% is right (58.65% real). Fix: drop "2024 dollars" from the parenthetical or print the real values.

**B16 — "Donor-advised sponsors (Benevity, Fidelity, Schwab) add $1.1M over five years" (slide 6).** The three named sponsors sum to $954,088 ($0.95M). $1.09M is the total of all eight DAF sponsors (adds National Philanthropic Trust, PayPal, Vanguard, CAF America, Blackbaud). Read literally the sentence is 15% high. Fix: "DAF sponsors, led by Benevity, Fidelity and Schwab, add $1.1M".

**C05 — OVSJG 2019 = 660,935 (slide 5 stream map).** Sum of two Reach Up rows with different grant numbers: OVSJG-L35-690 ($292,000, purpose "Create 15 beds…") and OVSJG-L35-556 ($368,935, "Provide 15 beds…", identical to the FY2020 and FY2021 awards). In the OVSJG open-data layer grant numbers run in yearly blocks (FY2018: L35-468..544; FY2019: L35-545..783; FY2020: L35-784..912), so L35-556 is the first number of the 2019 block while every other Calvary award sits mid-block; the DC spending layer (dc_pass) shows Calvary OVSJG obligations of $208,372 in FY2019 and $368,395 in FY2020. Two cycles appear to be tagged FY2019 in the source layer; summing them is probably a double count of ~$290–370K, which makes the 2019 bar the second-highest OVSJG year and undercuts the "OVSJG is growing" line for 2019→2020. This is a judgment on the source, not arithmetic. Fix: show one row for 2019 (likely $292,000 or the dc_pass obligation) and footnote the other.

**C07 — "TCP carries 74% of a $4.1M award base" (slide 5, slide 2, one-pager).** The $4.1M is the 2024 column of the stream map (OVSJG FY2024 913,401 + CoC 2024 1,761,352 + DHS FY2024 1,423,664 = 4,098,417); on that base TCP (CoC + DHS) is 77.7%. The 74% is (CoC 2024 + DHS) ÷ the FY25-aligned ceiling base of 4,289,967 (OVSJG FY2025 998,278 + CoC 2024 + DHS + 106,673 other federal carried from the FY23 SEFA): 74.2%. The two numbers in one sentence come from two different bases. Fix: either "78% of the $4.1M 2024 base" or "74% of the $4.3M FY25 ceiling base".

**D09 — other federal pass-through: 0 on slide 5 for 2024–25, 106,673 in the slide 11 ceilings.** The FY24 and FY25 ceilings (3,595,278 and 4,289,967) reproduce only if the FY23 audit-SEFA EFSP ($67,684) + SNAP E&T ($38,989) = 106,673 is carried forward into both years; the stream-map chart on slide 5 shows 0 for those years and the "$4.1M" base excludes it. Same rows, two carry-forward rules. Effect is 2.5% of the ceiling (ratios move from 73%→75% and 67%→69% if dropped). Fix: apply one rule on both slides and say "carried forward" where it is.

**F10 — "124 beds … 6.8% of DC's transitional-housing beds" (slides 2, 3; one-pager).** 68 (2022) and 124 (2025) are all Calvary project types in the DC-500 HIC (TH + PSH + RRH). The 2.5% and 6.8% are TH-only beds (45 and 94) ÷ DC TH beds (1,783 and 1,385, which tie to the HIC summary rows). On an all-types numerator the shares would be 3.8% and 9.0%. The sentence implies 124 TH beds. Fix: "94 of its 124 beds are transitional housing, 6.8% of DC's TH inventory" or similar.

## Conventions stated by the authors: tested

| Convention | Applied as stated? | Notes |
|---|---|---|
| Gov share FY13–23 = audited gov ÷ audited revenue; FY24–25 = 990 1e ÷ 990 revenue | Yes | All 11 years FY15–25 reproduce (41,44,40,42,49,55,50,61,51,45,58), mean FY22–24 = 52.5 → 53. Range 39.7–61.4 (FY17 rounds to 40). With the 990 revenue denominator the series is 44.2, 46.9, 42.7, 45.5, 50.5, 55.6, 51.4, 64.1, 55.2, 45.1, 58.2 (range 42.7–64.1, FY22–24 mean 54.8). Deliverables used the audit denominator. FY21 on a pure 990 basis (line 1e ÷ 990 revenue) would be 13.1%, the known line-1e trap; the audit figure was correctly used. |
| One source per gov stream, never summed across source_type | Yes across sources | Within-source duplication not caught in OVSJG 2019 (C05). SLFRF 3,680,675 correctly excluded from OVSJG recurring (it sits in dc_ovsjg as L35-1059, in dc_pass as PO660852-V2 and in treasury_slfrf as subaward 12126). PPP and HUD CPF excluded. |
| CoC competition year t → Calvary FY t+1 for ceilings | Yes | FY24 ceiling uses CoC 2023 (1,151,540); FY25 uses CoC 2024 (1,761,352). The stream map (slide 5) plots CoC by competition year, un-lagged, as its method line says. |
| DHS via TCP = dc_oversight FY2024 only, carried forward | Yes | 593,280 + 830,384 = 1,423,664 in both ceilings. |
| Small federal pass-throughs = audit_sefa (EFSP, SNAP E&T) | Yes, but inconsistently carried | See D09. |
| Filed grants = pf_grants_paid + schedule_i, Calvary recipient, TY2020–24, cumulative_flag 0, by funder_id | Yes | 138 rows, 50 funders, $4,433,659; institutional $3,340,017 (42 funders), DAF $1,093,642 (8 sponsors, 24.7%). GWCF $1,206,500 (27.2%; two distinct non-cumulative rows in TY2021). Top five 63.4%. HHI 1,167.5. Slide 6 top-10 bars all exact. |
| "$0.64–1.17M a year from 26–29 funders" | Yes (all funders incl. DAF) | By year: TY2020 0.64M/27, 2021 0.81M/26, 2022 1.16M/29, 2023 0.66M/29, 2024 1.17M/26. Institutional only: 0.45–0.95M from 21–24. The slide sits under a heading about foundations; the range includes DAF sponsors. |
| Real dollars via dim_period deflator_to_2024_us by FY-end year | Yes for the growth rate | Mislabeled on slide 3 (A05). |
| Months of cash = cash_savings_eoy ÷ (total_expenses ÷ 12) | Yes | FY20–25: 6.33, 7.47, 6.33, 5.03, 5.23, 4.44. |
| Slide 4 chart: private contributions and other revenue | Reproduced, with a caveat | Private = 990 contributions_total − government (audit basis) − 990 line 1c; other revenue = total_revenue − contributions_total, floored at 0. In FY15–23 that difference is negative (net event losses on line 8c), so the chart's four categories sum to more than total revenue in 9 of 11 years (by up to $150K in FY23). |

## Scenario formula (E)

Apportionment: FY25 990 line 1e (2,892,598) × each stream's share of the FY25 ceiling base (4,289,967): OVSJG 673,109; CoC 1,187,628; DHS 959,935; other 71,926. New Foundations 2 = CoC × (542,456 ÷ 1,761,352) = 365,762. All six revenue losses, % of revenue and gross deficits reproduce (67/168/178/366/960/1,306K; −675/−776/−785/−973/−1,567/−1,914K).

Months of cash after a year, as the deck shows them, reproduce with:

`months = (cash_FY25 + baseline_deficit − loss × (1 − 0.5)) ÷ (FY25 total_expenses ÷ 12)`

i.e. cash is rolled forward by the net deficit but the denominator stays at the full FY25 expense run-rate (464,610/month). Results 3.13, 3.06, 2.95, 2.94, 2.74, 2.10, 1.73 → 3.1, 3.1, 3.0, 2.9, 2.7, 2.1, 1.7. The alternative the reviewer asked about (denominator = expenses net of avoided cost) gives 3.13, 3.08, 3.00, 2.99, 2.83, 2.30, 1.96 and does not reproduce S5/S6. Gross (no cost avoidance) would be 2.99, 2.77, 2.75, 2.35, 1.07, 0.32. Months to zero cash at baseline = 2,063,796 ÷ (607,326/12) = 40.8 → 41. "Even the baseline burns about $50K a month" = 50.6K.

## Ceilings vs recognized (D)

FY24: 913,401 + 1,151,540 + 1,423,664 + 106,673 = 3,595,278; 2,621,203 ÷ = 72.9%. FY25: 998,278 + 1,761,352 + 1,423,664 + 106,673 = 4,289,967; 2,892,598 ÷ = 67.4%. Alternatives: FY25 excluding DHS 100.9% (recognized exceeds the non-DHS ceilings, so line 1e must include DHS money); FY25 excluding Sisters Rise 78.2%; FY24 excluding Sisters Rise 87.3%; FY24 excluding DHS 120.7%.

## Need, capacity, reserve (F, G)

Ward 8 poverty 30.6%, Ward 7 22.9%, DC 15.4%; Ward 8 female poverty 31.7%; renters paying 50%+: Ward 7 33.3%, Ward 8 32.5%. PIT DC-500 2016 = 8,350, 2025 = 5,138. Six months of FY25 expenses 2,787,661; private revenue FY25 = 4,967,995 − 2,892,598 = 2,075,397; public share at $3.0M private and flat government = 49.1%.

## Reviewer-guide §4 self-checks (H)

All six pass: FY25 revenue 4,967,995; Cafritz TY2024 $170,000 (one row); audit_sefa FY2023 four rows sum 937,999 (largest 440,677); OVSJG FY2026 New Foundations 543,056 and Reach Up 507,595; Ward 8 poverty_rate 0.3061; DWC FY2024 total_revenue 34,403,997.
