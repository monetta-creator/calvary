# M9 readout: need and capacity context

Script `scripts/09_m9_need_capacity.py`. Charts `charts/m9_*.png`; tables `chart_data/m9_*.csv`. Insights M9-01, M9-02.

## Question
How deep is the need in Calvary's service area, how is DC's homeless population moving, and how much of the system's capacity for single women does Calvary now provide?

## Method
- ACS 2020–24 five-year estimates by ward from `dim_geo` (DC wards are Census state-legislative-district geographies; 90% margins of error in the table).
- HUD point-in-time counts for CoC DC-500 from `supp_homeless_counts` (2007–2025).
- HUD Housing Inventory Count 2022–2025 from `supp_hic_projects`: Calvary's TH, PSH and RRH beds and share of all DC transitional-housing beds; women-focused providers flagged in the table.
- Ward map from DC Open Data ward boundaries (`raw/geo`), colored by ACS poverty rate, with Calvary's site.

## Findings
| Indicator (ACS 2020–24) | Ward 7 | Ward 8 | DC |
|---|---|---|---|
| Poverty rate | 22.9% | 30.6% | 15.4% |
| Female poverty rate | 24.8% | 31.7% | 16.3% |
| Renters paying 30%+ of income | 55.3% | 54.6% | 46.6% |
| Renters paying 50%+ | 33.3% | 32.5% | 23.6% |
| Unemployment | 12.7% | 13.4% | 6.3% |
| Female householder, no spouse | 29.0% | 29.8% | 13.1% |

1. **Need** (M9-01): Ward 8 has twice the city's poverty rate and the highest female poverty in DC; a third of renters in both wards pay more than half their income in rent; unemployment is double the city rate.
2. **System trend** (M9-02): DC's homeless count fell from 8,350 (2016) to 5,138 (2025), with a post-pandemic rebound in 2023–24. The system is shrinking while per-person investment (PSH, vouchers) rises.
3. **Calvary's capacity**: inventory grew from 68 beds (2022) to 124 (2025): 94 TH beds (6.8% of all DC transitional-housing beds, up from 2.5%), 16 PSH (Sister Circle), 14 RRH. Sisters Rise PSH (24 units) appears in 2024 only. Among women-focused providers in the HIC (N Street Village 457, House of Ruth 388, Open Arms 412, New Endeavors 135, Calvary 124 beds in 2025), Calvary is the fastest-growing.

## Charts
`m9_01_ward_indicators`, `m9_02_dc_pit`, `m9_03_calvary_hic_share`, `m9_05_ward_map` (if boundaries loaded; see analysis log); tables `m9_04_women_focused_beds.csv`.

## Caveats
- Ward-level ACS has wide margins of error for small subgroups; tract-level figures were not used.
- HIC counts beds, not people served, and HIC project naming changes year to year (Calvary's projects were re-labelled in 2024).
- PIT gender breakdowns are not in HUD's PIT workbook; the CoC's own 2024 subpopulation table counts 2,167 women among 5,616 people.

## Confidence
High.
