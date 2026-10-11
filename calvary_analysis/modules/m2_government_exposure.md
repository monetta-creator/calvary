# M2 readout: government exposure and stress test

Script `scripts/02_m2_exposure.py`; parameters `config/scenarios.yaml`. Chart data `chart_data/m2_*.csv`, charts `charts/m2_*.png`. Insights M2-01 to M2-06.

## Question
Which government streams does Calvary depend on, how durable is each, what is happening to the pools behind them, and what would cuts do to revenue and cash?

## Method
- One source per stream from `fact_gov_awards`, never summed across sources: OVSJG award lists (DC FY2019–2026), HUD CoC award lists via TCP (competition years 2019–FY2025), DHS provider contracts via TCP (Council oversight responses, DC FY2024 only), audited SEFA lines for the small federal pass-throughs (EFSP, SNAP E&T). One-time money (SLFRF $3.68M, PPP $327K, HUD CPF $200K) is listed separately.
- Award ceilings aligned to Calvary's fiscal year (DC FY = Calvary FY; HUD CoC competition year t → operating year t+1; DHS FY2024 value carried forward) and compared with recognized government revenue.
- DC budget context from `supp_dc_budget_lines` (activity-level totals, approved vs actual vs Mayor's proposal) and `fact_policy_events`.
- Scenarios apportion FY25 recognized government revenue ($2.89M) to streams by ceiling share (OVSJG 23%, CoC 41%, DHS 33%, other 2%) and apply cuts from the config; "net" assumes 50% of a lost stream's revenue is avoidable cost.

## Findings
1. **Three channels, two of them through one intermediary** (M2-01). Recurring awards grew from $0.9M (2019) to $4.1M (2024): OVSJG $0.37M (FY20) → $1.05M (FY26); CoC $0.24M (2019) → $1.77M (FY2025) across three projects; DHS/TCP $1.42M (FY2024: transitional housing $830K, Sisters Rise EHV $593K). TCP carries both CoC and DHS money, so about 74% of the award base passes through TCP.
2. **Ceilings exceed recognized revenue by a third** (M2-02, flag D1): FY24 ceilings $3.6M vs $2.62M recognized (73%); FY25 $4.3M vs $2.89M (67%). The gap is undrawn awards, timing, or an overstated DHS carry-forward. Either way, Calvary's FY24/FY25 audits and TCP subgrant agreements are the single most useful documents Calvary could provide.
3. **Stream durability** (M2-03, judgment): OVSJG grants are annual and politically exposed but have been restored every year; CoC renewals are usually protected but TCP cut Reach Up 65% in 2022 and the 2025 HUD NOFO changed priorities; the DHS/TCP contract is the largest, least documented and most at risk, and Sisters Rise left the 2025 HIC (flag D2).
4. **DC pools are flat to rising, with cuts proposed every spring** (M2-03): OVSJG Victim Services grants approved $45.5M (FY24) → $55.9M (FY25) → $55.4M (FY26) → $55.3M (FY27); the Mayor's FY26 proposal ($50.1M, −10.4%) was restored by the Council. DHS continuum $170M (FY24) → $206M (FY26) → $194M (FY27); PSH $145–166M. Actual spending runs 9–14% below approved on OVSJG.
5. **Calvary is a price-taker** (M2-04): 5.3% of DC CoC awards, 1.1% of OVSJG awards.
6. **Scenarios** (M2-05, FY25 baseline: revenue $4.97M, expenses $5.58M, cash $2.06M, deficit −$607K):

| Scenario | Revenue loss | % of revenue | Deficit (gross) | Months of cash after a year (net) |
|---|---|---|---|---|
| OVSJG −10% | −$67K | 1% | −$675K | 3.1 |
| OVSJG −25% | −$168K | 3% | −$776K | 3.0 |
| CoC renewals −15% | −$178K | 4% | −$785K | 2.9 |
| One CoC project lost (New Foundations 2) | −$366K | 7% | −$973K | 2.7 |
| DHS/TCP contract not renewed | −$960K | 19% | −$1.57M | 2.1 |
| Combined (OVSJG −25%, CoC −15%, DHS lost) | −$1.31M | 26% | −$1.91M | 1.7 |

The headline OVSJG cuts are survivable; a TCP contract loss is not without new money or cost cuts. Even the baseline burns cash: at the FY25 run-rate, cash lasts about 41 months.

## Charts
`m2_01_stream_map`, `m2_02_ceilings_vs_recognized`, `m2_04_dc_budget_context`, `m2_05_pool_shares`, `m2_06_policy_timeline`, `m2_07_scenarios`; tables `m2_03_stream_durability.csv`, `m2_07_scenario_parameters.csv`.

## Caveats
- DHS/TCP amounts are public for FY2024 only; every other year of that stream is unknown, not zero.
- HUD CoC award years are competition years; the one-year lag to Calvary's operating year is an assumption (config).
- Scenario stream shares are apportioned from ceilings, not from Calvary's ledger.
- Federal policy risk (2025 CoC NOFO, EHV sunset) is only partly captured in the data and is noted as external context.

## Confidence
High on the stream map, pool shares and DC budget lines; medium on ceilings-vs-recognized and the scenarios (apportionment and carry-forward assumptions); durability ratings are judgment.
