# M2 readout: government exposure and stress test

Script `scripts/02_m2_exposure.py`; parameters `config/scenarios.yaml`. Chart data `chart_data/m2_*.csv`, charts `charts/m2_*.png`. Insights M2-01 to M2-06.

## Question
Which government streams does Calvary depend on, how durable is each, what is happening to the pools behind them, and what would cuts do to revenue and cash?

## Method
- One source per stream from `fact_gov_awards`, never summed across sources: OVSJG award lists (DC FY2019–2026), HUD CoC award lists via TCP (competition years 2019–FY2025), DHS provider contracts via TCP (Council oversight responses, DC FY2024 only), audited SEFA lines for the small federal pass-throughs (EFSP, SNAP E&T). One-time money (SLFRF $3.68M, PPP $327K, HUD CPF $200K) is listed separately.
- Award ceilings aligned to Calvary's fiscal year (DC FY = Calvary FY; HUD CoC competition year t → operating year t+1; DHS FY2024 value carried forward) and compared with recognized government revenue.
- DC budget context from `supp_dc_budget_lines` (activity-level totals, approved vs actual vs Mayor's proposal) and `fact_policy_events`.
- Scenarios split FY25 recognized government revenue ($2.89M) across streams three ways and apply cuts from the config: (A) ceiling share (OVSJG 23%, CoC 41%, DHS 33%, other 2%); (B) CoC at its audited FY22–23 draw rate (38%), with DHS the residual; (C) ceiling share without Sisters Rise. Losses are reported as the range across the three splits. A floor case (OVSJG and CoC fully drawn, DHS the residual) is reported separately, not as a bound. "Net" assumes 50% of a lost stream's revenue is avoidable cost.

## Findings
1. **Three channels, two of them through one intermediary** (M2-01). Recurring awards grew from $0.6M (2020) to $4.1M (2024): OVSJG $0.37M (FY20) → $1.05M (FY26); CoC $0.24M (2019) → $1.77M (FY2025) across three projects; DHS/TCP $1.42M (FY2024: transitional housing $830K, Sisters Rise EHV $593K). TCP carries both CoC and DHS money, so about three-quarters (78% of the $4.1M 2024 award base, `m2_01`) passes through TCP. The series is quoted from 2020 because the 2019 value ($0.9M) adds two OVSJG Reach Up records ($292,000 and $368,935) that may be one award recorded twice.
2. **Ceilings exceed recognized revenue by a third** (M2-02, flag D1): FY24 ceilings $3.6M vs $2.62M recognized (73%); FY25 $4.3M vs $2.89M (67%). The gap is undrawn awards, timing, or an overstated DHS carry-forward. Calvary's FY22 and FY23 single audits already show CoC expenditure at 28% (FY22) and 58% (FY23) of the prior year's CoC award ceilings, so the gap is specific to the CoC stream and predates FY24 (the 2021 Reach Up expansion award, $1.22M reallocated to $0.42M in 2022, explains part). The next step is to reconcile CoC draw-down first, then DHS: Calvary's FY24/FY25 audits and TCP subgrant agreements are the single most useful documents Calvary could provide.
3. **Stream durability** (M2-03, judgment): OVSJG grants are annual and set in each spring's budget but have been restored every year; CoC renewals are usually protected but TCP cut Reach Up 65% in 2022. The FY2025 CoC NOFO was enjoined and FY2025 renewals were paid in full; the live cloud is the FY2026 CoC NOFO (protected renewals 60% of demand, a $1.3B transitional-housing and services set-aside, applications closed 30 September 2026, awards expected about December 2026, litigation pending). The DHS/TCP contract is the largest, least documented and most at risk, and Sisters Rise left the 2025 HIC (flag D2); HUD's 29 September 2026 notice ends the EHV program (families leased on 30 September 2026 convert to non-reissuable tenant-protection vouchers by 31 December 2026), so Sisters Rise's voucher base cannot be rebuilt.
4. **DC pools are flat to rising, with cuts proposed every spring** (M2-03): OVSJG Victim Services grants approved $45.5M (FY24) → $55.9M (FY25) → $55.4M (FY26) → $55.3M (FY27); the Mayor's FY26 proposal ($50.1M, −10.4%) was restored by the Council. The FY2027 OVSJG restoration is $5.1M one-time plus $0.5M recurring, so the FY2028 base is at risk again. DHS continuum $170M (FY24) → $206M (FY26) → $194M (FY27); PSH $145–166M. Actual spending runs 9–14% below approved on OVSJG.
5. **Calvary is a price-taker** (M2-04): 5.3% of DC CoC awards, 1.1% of OVSJG awards.
6. **Scenarios** (M2-05, FY25 baseline: revenue $4.97M, expenses $5.58M, cash $2.06M, deficit −$607K):

| Scenario | Revenue loss (range across three splits) | % of revenue | Deficit (gross) | Months of cash after a year (net) |
|---|---|---|---|---|
| OVSJG −10% | −$67K to −$100K | 1–2% | −$675K to −$707K | 3.0–3.1 |
| OVSJG −25% | −$168K to −$250K | 3–5% | −$776K to −$857K | 2.9–3.0 |
| CoC renewals −15% | −$99K to −$207K | 2–4% | −$707K to −$814K | 2.9–3.0 |
| One CoC project lost (New Foundations 2) | −$204K to −$424K | 4–9% | −$811K to −$1.03M | 2.7–2.9 |
| DHS/TCP contract not renewed | −$0.65M to −$1.13M | 13–23% | −$1.26M to −$1.73M | 1.9–2.4 |
| Combined (OVSJG −25%, CoC −15%, DHS lost) | −$1.05M to −$1.47M | 21–30% | −$1.66M to −$2.08M | 1.5–2.0 |

The DHS figure depends on how revenue splits across streams; the floor case with OVSJG and CoC fully drawn nearly removes it ($26K). The headline stands: the TCP channel is the cloud, since CoC and DHS together are $1.8–2.2M under every split. The headline OVSJG cuts are survivable; a TCP contract loss is not without new money or cost cuts. Even the baseline burns cash: at the FY25 run-rate, cash lasts about 41 months.

## Charts
`m2_01_stream_map`, `m2_02_ceilings_vs_recognized`, `m2_04_dc_budget_context`, `m2_05_pool_shares`, `m2_06_policy_timeline`, `m2_07_scenarios`; tables `m2_03_stream_durability.csv`, `m2_07_scenario_parameters.csv`.

## Caveats
- DHS/TCP amounts are public for FY2024 only; every other year of that stream is unknown, not zero. TCP is a pass-through intermediary with no itemized Schedule I list in the data, so TCP agreements are the only route to FY25–26 DHS values.
- HUD CoC award years are competition years; the one-year lag to Calvary's operating year is an assumption (config).
- Scenario stream shares are apportioned three ways from ceilings and the audited CoC draw rate, not from Calvary's ledger; the ledger would turn each range into one figure.
- Federal policy risk (FY2026 CoC NOFO, the EHV program's end) is only partly captured in the data and is noted as external context, dated October 2026.

## Confidence
High on the stream map, pool shares and DC budget lines; medium on ceilings-vs-recognized and the scenarios (apportionment and carry-forward assumptions); durability ratings are judgment.
