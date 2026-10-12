# M3 readout: peer benchmarking

Script `scripts/03_m3_peers.py`. Benchmark table `chart_data/m3_00_benchmark_table.csv`; charts `charts/m3_*.png`. Insights M3-01 to M3-06. Core peers are the 18 **provisional** organizations in `calvary_funding_data/config/core_peers.csv`; DWC and the CBWC Empowerment Institute (SheWorks) appear as Los Angeles reference rows on every chart.

## Question
Where does Calvary sit against comparable organizations on government dependence, size, growth, liquidity and private funder base, and which peers show a workable path to lower exposure?

## Method
- Preferred 990 rows from `fact_org_financials` FY2015–FY2025. Government share = line 1e ÷ total revenue, except Calvary FY≤2023 where the audit basis is used (line 1e understated FY21). Three-year means (FY2022–24) smooth single-year reporting breaks (e.g., Coalition for the Homeless FY23, Samaritan Inns FY24).
- Real growth = CAGR of 2024-dollar revenue FY2019→FY2024 (endpoints avoid Calvary's one-time FY22 award).
- Months of cash = cash and savings ÷ monthly expenses (clean-table field).
- Funder base = 990-PF/Schedule I rows naming each organization TY2020–24 (non-cumulative), split institutional vs DAF via `dim_funder.funder_type`; depth = institutional dollars ÷ FY2020–24 revenue. DMV funders' filings only, so the LA comparators' local funders are not captured. Two Baltimore funders' grants to a Baltimore namesake of My Sister's Place ($131,906) are excluded (`config/grant_exclusions.csv`).
- Resilience typology: government-anchored ≥65%, mixed 35–65%, philanthropy-led <35%.
- Sector distributions: `dc_sector` FY2023, `size_matched` FY2022, `national_women` FY2022, chosen for filing coverage. Percentiles are computed among organizations whose 990 reports a government line (n=163/334/542), and again against all filers with no government line counted as 0% (n=426/556/1,124).

## Findings

| Organization | Rev FY24 | Gov share FY22–24 | Real CAGR FY19–24 | Months of cash FY24 | Institutional funders | Inst. $ ÷ revenue | Type |
|---|---|---|---|---|---|---|---|
| **Calvary** | $5.8M | 53% | +13.8% | 5.2 | 42 | 12% | mixed |
| DC SAFE | $7.0M | 89% | +17.7% | 0.9 | 7 | 3% | gov-anchored |
| My Sister's Place | $7.2M | 83% | +19.4% | 2.9 | 23 | 7% | gov-anchored |
| DASH | $7.0M | 70% | −2.7% | 4.0 | 23 | 5% | gov-anchored |
| House of Ruth DC | $14.6M | 53% | +5.0% | 3.8 | 83 | 8% | mixed |
| N Street Village | $10.0M | 42% | −1.7% | 8.0 | 54 | 6% | mixed |
| Samaritan Inns | $7.1M | 44% | +10.1% | 4.5 | 14 | 27% | mixed |
| Miriam's Kitchen | $11.3M | 0% | +12.0% | 4.1 | 66 | 11% | philanthropy-led |
| DWC (LA, ref.) | $34.4M | 57% | +19.0% | 2.4 | n/a | n/a | mixed |
| CBWC Inst./SheWorks (LA, ref.) | $1.5M | 86% | n/a | 4.8 | n/a | n/a | gov-anchored |

Full table: `m3_00_benchmark_table.csv` (21 organizations, all metrics).

1. **Calvary is mid-pack on government share** (M3-01): 53%, 11th of 19 DC-area organizations, below every DC DV provider (70–89%) and above the philanthropy-led models (Miriam's Kitchen, Thrive DC, Christ House). The peer rank is the stronger evidence that Calvary's share is typical. Against the broader sector (M3-02), Calvary is at the 57th percentile among DC human-services organizations that report government revenue (46th among national women's/DV organizations); against all filers, with no government line counted as 0%, it is in the top quarter (84th in DC, 74th nationally).
2. **Growth has come on both models** (M3-03): Calvary's +13.8%/yr real growth trails only My Sister's Place, DWC and DC SAFE; Miriam's Kitchen grew +12%/yr with almost no government money.
3. **Liquidity is mid-pack** (M3-04): 5.2 months in FY24 (4.4 in FY25). Government-anchored DV providers run on ~1 month; Doorways, Everyone Home DC and N Street Village hold 8–12 months.
4. **Calvary already works institutional funders harder than most peers** (M3-05): 42 institutional funders and filed institutional grants equal to 12% of revenue, versus 6–8% at N Street Village and House of Ruth DC; only Samaritan Inns (27%) is far ahead. The headroom is in grant size and multi-year commitments, in DAF/major-donor giving (N Street Village 51% of filed grants via DAFs, Calvary 25%), and in earned revenue.
5. **Three paths** (M3-06): Samaritan Inns replaced government (72% → 11%) with program-service and other revenue while revenue held near $6–7M; N Street Village grew private giving alongside a stable ~40% government share; DWC and House of Ruth MD scaled with government rising above 55%. The N Street Village path is the closest fit for Calvary; Samaritan Inns shows the earned-revenue option; DWC shows that scaling with government needs a much larger balance sheet (DWC's months of cash: 2.4).
6. **In the shared DC pools** (m3_09): the DV peers draw $3–5M a year each from OVSJG; Calvary's $1.05M makes it a mid-sized OVSJG grantee and one of the larger CoC sub-recipients ($1.77M; only Christ House and My Sister's Place draw more).

## Charts
`m3_01_gov_share_ranked`, `m3_02_size_vs_gov_share`, `m3_03_real_growth`, `m3_04_months_of_cash`, `m3_05_gov_share_trajectories` (20 small multiples), `m3_06_institutional_base`, `m3_07_sector_distributions`, `m3_08_case_studies_mix`, `m3_09_peer_pools`.

## Caveats
- Core peers are provisional; swapping them is a config edit plus rerun. Swapping three provisional peers for alternates moves Calvary from 11th to 12th of 19; confirm the peer set with Calvary before outreach.
- Line 1e understates government for organizations that book contracts as program revenue (Samaritan Inns' FY24–25 drop may be partly reclassification; its program-service revenue rose at the same time).
- Funder-base metrics cover DMV funders' filings only; TY2024 partial.
- Named comparators: DWC's fiscal year is the calendar year; CBWC Institute has three years of filings and SheWorks itself begins after TY2024.

## Confidence
High for shares, growth, liquidity and sector percentiles (on the stated comparison set); medium for funder-base depth and the typology of diversifiers (judgment on three cases).
