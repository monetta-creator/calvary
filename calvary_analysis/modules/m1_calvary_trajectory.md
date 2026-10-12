# M1 readout: Calvary financial trajectory FY2011–FY2025

Script `scripts/01_m1_trajectory.py`. Chart data `chart_data/m1_*.csv`, charts `charts/m1_*.png`. Insights M1-01 to M1-05 in `insight_register.csv`.

## Question
How has Calvary's revenue, mix, margin and liquidity moved over 15 years, and how concentrated is its private funding?

## Method
- Revenue, expenses, net assets and cash from `fact_org_financials` preferred 990 rows (one per fiscal year; five sources agree within 1%). Real values use the CPI-U deflator to 2024 dollars in `dim_period`.
- Government revenue on the **audit basis** (contracts and grants ÷ audited total revenue) for FY13–FY23, and 990 line 1e ÷ 990 revenue for FY24–FY25. Line 1e equalled the audited figure in FY22 and FY23, so the FY24–25 numbers are treated as reliable; the FY21 line 1e ($503K vs $1.98M audited) is the known exception.
- Private contributions ex-events = contributions total − government − line 1c events. The 990 does not split foundations from individuals, so institutional giving is measured separately from funders' own filings (`fact_grants`, 990-PF and Schedule I rows naming Calvary, TY2020–24, excluding cumulative rows, aggregated by funder EIN).
- Concentration: funder shares of five-year filed grants and a Herfindahl index.

## Findings

| | FY19 | FY21 | FY22 | FY23 | FY24 | FY25 |
|---|---|---|---|---|---|---|
| Total revenue (nominal) | $2.49M | $3.85M | $8.87M | $4.46M | $5.82M | $4.97M |
| Government (audit basis / line 1e) | $1.26M | $1.98M | $5.69M | $2.46M | $2.62M | $2.89M |
| Government share (audit ÷ audit revenue; 990 for FY24–25) | 49% | 50% | 61% | 51% | 45% | 58% |
| Surplus / deficit | +$83K | +$517K | +$4.32M | −$674K | +$507K | −$607K |
| Months of cash | 5.8 | 7.5 | 6.3 | 5.0 | 5.2 | 4.4 |

1. **Government supplied 40–61% of revenue every year since FY15 and most of the growth** (M1-01). Revenue went from $2.49M (FY19) to $4.97M (FY25) in nominal dollars, +59% after inflation ($3.05M to $4.84M in 2024 dollars). In nominal terms government revenue grew 130% over the same period and private contributions ex-events 85%; event receipts are covered in item 3.
2. **FY25 ran a $607K deficit and ended with 4.4 months of cash** (M1-02; 7.5 months in FY21). The 990's contributions total fell from $5.55M to $4.75M, but much of that fall is the change in how the gala was presented (item 3), not lost donors. Net assets ($8.1M) are mostly the building.
3. **Event receipts held near $0.53–0.60M (FY24 $596K, FY25 $533K)** (M1-03). The FY25 990 presented gala receipts as fundraising-event income (line 8a, with $259K of direct costs netted) instead of contributions (line 1c), so line 1c alone drops from $538K to $55K and net event income turns positive. The 2025 gala took place on 23 April 2025 (inside FY25) and the 2026 gala raised over $620K. Flag D3 is closed (resolved from the 990 itself).
4. **Filed institutional grants are flat (~$1M/yr from 26–29 funders) and concentrated** (M1-04): GWCF, including the Health Equity Fund, is 27% of five-year filed grants ($1.21M of $4.43M); the top five are 63%; HHI 1,168 (moderately concentrated). DAF sponsors add $1.09M over five years (Benevity, Fidelity, Schwab lead).
5. **FY22 was a capital event, not growth** (M1-05): the $3.68M SLFRF award bought the New Foundations building.

## Charts
- `m1_01_revenue_expenses` — revenue and expenses, nominal and 2024$, FY11–FY25
- `m1_02_revenue_mix` — stacked mix with government share labels, FY15–FY25
- `m1_03_gov_share_two_measures` — audit basis vs line 1e
- `m1_04_surplus_deficit` — annual surplus/deficit
- `m1_05_months_of_cash` — months of cash with a 3–6 month band
- `m1_06_event_income` — line 1c vs net event income (FY25 line 1c excludes the gala, reported on line 8a)
- `m1_07_funder_concentration` — top 12 filed funders with shares
- `m1_08_filed_grants_by_year` — institutional vs DAF by funder tax year

## Caveats
- No FY24/FY25 audits are public; those years rest on the 990. Line 1e matched audits in FY22–23.
- Funder tax years do not align with Calvary's fiscal year; TY2024 filings are partial and TY2025 mostly unfiled, so "flat" after TY2023 is partly filing lag.
- The 990 cannot separate individuals from foundations inside "private contributions ex-events"; the CRM export covers institutional gifts only and is cumulative over an unconfirmed window.

## Confidence
High on the revenue, margin and liquidity series and on government share through FY23; high on concentration of filed grants; medium on the FY24–25 government share (990 only).
