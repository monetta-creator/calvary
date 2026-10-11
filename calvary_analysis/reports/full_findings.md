# Calvary Women's Services: Full Findings Report (All Modules)

**Audience:** consulting team
**As of:** 2026-10-10 (draft for CP2)
**Covers:** modules M1–M10, the funding-pressure verdict, open flags D1–D3, and the insight register

**Purpose.** This report gathers the ten analysis modules for the consulting team around two anchor questions: **how exposed is Calvary to government funding** (how much revenue relies on government, through which channels, how durable each is, and what cuts would do to revenue and cash), and **where is the opportunity** (which funders, programs and channels could grow private and earned revenue). It starts from what Calvary's team has built: 15 years of growth, a funder base at the core of its peer network, and a housing inventory that grew from 68 to 124 beds since 2022. Risks are stated plainly as clouds on the horizon, each with a path. Every number is taken as written from the module readouts (`modules/`), the verdict, the insight register and the discoveries log; nothing is newly computed. Provisional items (core peers, reconstructed FY24–25 government share, medium-confidence interlocks) are labeled. Recommendations are in `recommendations/strategic_recommendations.md`.

---

## Summary of findings

**M1 – Calvary's trajectory.** Calvary's team has grown real revenue 59% from FY19 to FY25 (government +130%, private contributions ex-events +85%); government has supplied 40–61% of revenue every year since FY15. FY25 brings the first clouds: a $607K deficit, contributions down from $5.55M to $4.75M, and 4.4 months of cash (7.5 in FY21). Event contributions fell from $538K to $55K, likely a reporting or calendar change (D3). Filed institutional grants are flat (~$1M/yr from 26–29 funders) and concentrated: GWCF 27% of five-year filed grants, top five 63%. FY22's spike was a one-time $3.68M SLFRF building award. *Insights: M1-01, M1-02, M1-03, M1-04, M1-05.*

**M2 – Government channels and stress test.** Calvary built a recurring award base of $4.1M (2024), up from $0.9M (2019), across OVSJG, HUD CoC via TCP and DHS via TCP; about 74% passes through TCP, the main concentration. Recognized revenue was 73% (FY24) and 67% (FY25) of ceilings (D1), possibly recoverable headroom. DC pools are flat to rising, with cuts proposed each spring and restored. OVSJG cuts are survivable; losing the DHS/TCP contract (−$960K, 19% of revenue) is not without new money or cost cuts, and Sisters Rise left the 2025 HIC (D2). *Insights: M2-01, M2-02, M2-03, M2-04, M2-05, M2-06.*

**M3 – Peer benchmarking.** Calvary's government share (53%, FY2022–24) is mid-pack: below every DC DV provider (70–89%), above the philanthropy-led models, and typical of the sector (57th percentile DC, 46th national women's/DV). Its +13.8%/yr real growth trails only My Sister's Place, DWC and DC SAFE; liquidity is mid-pack (5.2 months, FY24); it already works institutional funders harder than most peers (42 funders, 12% of revenue). The N Street Village path is the closest fit. *Insights: M3-01, M3-02, M3-03, M3-04, M3-05, M3-06.*

**M4 – Funder landscape.** About $132M a year flows from DMV funders into DC-sector organizations, 58% via DAF sponsors and 42% from 555 institutional funders. The top 10 give about half of institutional dollars; 6 of the 25 largest already fund Calvary. The median grant is ~$15K, so growth means a handful of six-figure, multi-year relationships. Mission-tagged dollars are a minority. *Insights: M4-01, M4-02, M4-03, M4-04, M4-05.*

**M5 – Funder gaps.** 23 institutional funders give to three or more peers with no filed grant to Calvary (75 to two or more), led by Clark Charitable Foundation (5 peers, $7.8M, median grant $250K); add 12 lapsed funders ($255K historically) and 15 current funders with upgrade headroom. 44% of the CRM's $10.56M (2023–26) is confirmed in funders' filings. *Insights: M5-01, M5-02, M5-03, M5-04.*

**M6 – Network.** Calvary sits in the core of the funder web, not at its edge: nearly every highly connected funder already funds it. It shares the most funders with Miriam's Kitchen (17), DASH (14) and House of Ruth DC (14), the natural routes to new funders. Board interlocks are thin (8 links, 1 high-confidence). The strongest paths to non-funders run through peers (Venable, T. Rowe Price Program, JPMorgan Chase, Clark). *Insights: M6-01, M6-02, M6-03.*

**M7 – Pipeline.** Tier 1 combines upgrades with current majors (Abell, GWCF, Cafritz, Fowler), new foundations (Clark Charitable, Schattner, America's Charities), CRM corporate relationships (MGAC, Frontier Co-op) and the government rows; a 90-day plan sequences them. Readout and register differ on counts and some tiers (Consistency notes). *Insight: M7-01.*

**M8 – Mission expansion.** Programs Calvary already runs in some form carry about $149M a year of tagged DMV grants; workforce and behavioral health are the real near pools. Physical health is the largest medium-distance pool ($84M/yr, 206 funders at $100K+), reachable through partnership. Direct federal competition is thin (36 notices). *Insights: M8-01, M8-02.*

**M9 – Need and capacity.** Ward 8 poverty is 30.6% (DC 15.4%), with the highest female poverty in DC. While DC's homeless count fell from 8,350 (2016) to 5,138 (2025), Calvary grew from 68 to 124 beds (2022–2025), the fastest-growing women-focused provider, with 6.8% of DC's transitional-housing beds. *Insights: M9-01, M9-02.*

**M10 – Named comparators.** DWC grew from $6.3M to $34.4M (FY2014–FY2024) as government rose from 24% to 57%, through the same pass-through channels Calvary uses, on 2–3 months of cash; its programs transfer, its mix does not. SheWorks offers a program design for Step Up DC; its parent is 70% government. *Insights: M10-01, M10-02.*

---

## M1 Calvary's financial trajectory, FY2011–FY2025

### Question
How has Calvary's revenue, mix, margin and liquidity moved over 15 years, and how concentrated is its private funding?

### Method
- Preferred 990 rows from `fact_org_financials` (five sources agree within 1%); real values in 2024 dollars (CPI-U).
- Government on the **audit basis** FY13–FY23, 990 line 1e FY24–FY25 (line 1e equalled audits in FY22–23; FY21 line 1e, $503K vs $1.98M audited, is the known exception).
- Private contributions ex-events = contributions total − government − line 1c events. Institutional giving is measured from funders' own filings naming Calvary (TY2020–24, non-cumulative); concentration via funder shares and a Herfindahl index.

### Findings

| | FY19 | FY21 | FY22 | FY23 | FY24 | FY25 |
|---|---|---|---|---|---|---|
| Total revenue | $2.49M | $3.85M | $8.87M | $4.46M | $5.82M | $4.97M |
| Government (audit basis / line 1e) | $1.26M | $1.98M | $5.69M | $2.46M | $2.62M | $2.89M |
| Government share | 51% | 51% | 64% | 55% | 45% | 58% |
| Surplus / deficit | +$83K | +$517K | +$4.32M | −$674K | +$507K | −$607K |
| Months of cash | 5.8 | 7.5 | 6.3 | 5.0 | 5.2 | 4.4 |

1. **Government supplied 40–61% of revenue every year since FY15 and most of the growth** (M1-01). Real revenue grew 59% FY19→FY25; government revenue grew 130% over the same period and private contributions ex-events 85%, while event income fell.
2. **FY25 is a stress year** (M1-02): a $607K deficit, contributions down from $5.55M to $4.75M, and a cash cushion of 4.4 months (7.5 in FY21). Net assets ($8.1M) are mostly the building, so they are not a liquidity buffer.
3. **Event contributions fell from $538K to $55K** (M1-03) while net event income turned positive. This looks like a reporting or calendar change rather than lost donors. Flagged as D3.
4. **Filed institutional grants are flat (~$1M/yr from 26–29 funders) and concentrated** (M1-04): GWCF, including the Health Equity Fund, is 27% of five-year filed grants ($1.21M of $4.43M); the top five are 63%; HHI 1,168 (moderately concentrated). DAF sponsors add $1.09M over five years (Benevity, Fidelity, Schwab lead).
5. **FY22 was a capital event, not operating growth** (M1-05): the $3.68M SLFRF award bought the New Foundations building.

### Charts
- `m1_01_revenue_expenses` – Calvary revenue and expenses FY11-FY25, nominal and 2024 dollars
- `m1_02_revenue_mix` – Calvary revenue mix FY15-FY25 (government on the audit basis to FY23)
- `m1_03_gov_share_two_measures` – Government share of revenue: audit basis vs 990 line 1e
- `m1_04_surplus_deficit` – Calvary surplus/deficit, net assets, cash and months of cash FY11-FY25 (an earlier write of the same data is `m1_04_surplus_net_assets`)
- `m1_05_months_of_cash` – Calvary months of cash FY11-FY25
- `m1_06_event_income` (PNG; data `m1_06_events`) – Calvary event contributions (line 1c) and net special-event income FY15-FY25
- `m1_07_funder_concentration` (PNG; data `m1_07_calvary_funder_concentration`) – Grants to Calvary in funders' own filings TY2020-24, by funder, with cumulative share
- `m1_08_filed_grants_by_year` – Filed grants to Calvary by funder tax year: institutional vs DAF
- Supporting: `m1_summary_numbers` – M1 headline numbers used in readouts and decks

### Caveats
- No FY24/FY25 audits are public; those years rest on the 990 (reconstructed government share).
- Funder tax years do not align with Calvary's fiscal year; TY2024 is partial and TY2025 mostly unfiled, so "flat" after TY2023 is partly filing lag.
- The 990 cannot separate individuals from foundations; the CRM export covers institutional gifts only, cumulative over an unconfirmed window.

### Confidence
High on the revenue, margin and liquidity series and on government share through FY23; high on concentration of filed grants; medium on the FY24–25 government share (990 only).

---

## M2 Government funding: channels, durability and stress test

### Question
Which government streams does Calvary rely on, how durable is each, what is happening to the pools behind them, and what would cuts do to revenue and cash?

### Method
- One source per stream, never summed: OVSJG award lists (DC FY2019–2026); HUD CoC awards via TCP (competition years 2019–FY2025); DHS contracts via TCP (Council oversight, DC FY2024 only); audited SEFA lines for EFSP and SNAP E&T. One-time money (SLFRF $3.68M, PPP $327K, HUD CPF $200K) listed separately.
- Award ceilings aligned to Calvary's fiscal year (DC FY = Calvary FY; CoC competition year t → operating year t+1; DHS FY2024 value carried forward) and compared with recognized government revenue.
- DC budget context from `supp_dc_budget_lines` and `fact_policy_events`.
- Scenarios apportion FY25 recognized government revenue ($2.89M) to streams by ceiling share (OVSJG 23%, CoC 41%, DHS 33%, other 2%) and apply cuts from `config/scenarios.yaml`; "net" assumes 50% of a lost stream's revenue is avoidable cost.

### Findings
1. **Three channels, two of them through one intermediary** (M2-01). Recurring awards grew from $0.9M (2019) to $4.1M (2024): OVSJG $0.37M (FY20) → $1.05M (FY26); CoC $0.24M (2019) → $1.77M (FY2025) across three projects; DHS/TCP $1.42M (FY2024: transitional housing $830K, Sisters Rise EHV $593K). TCP carries both CoC and DHS money, so about 74% of the award base passes through TCP. Winning this base is the team's achievement; the cloud is reliance on one intermediary.
2. **Ceilings exceed recognized revenue by a third** (M2-02, flag D1): FY24 ceilings $3.6M vs $2.62M recognized (73%); FY25 $4.3M vs $2.89M (67%). The gap is undrawn awards, timing, or an overstated DHS carry-forward. Calvary's FY24/FY25 audits and TCP subgrant agreements are the most useful documents Calvary could provide; if awards are under-drawn, this is the cheapest headroom available.
3. **Stream durability** (judgment; register M2-06 covers Sisters Rise): OVSJG grants are annual and subject to the spring budget cycle but have been restored every year; CoC renewals are usually protected, but TCP cut Reach Up 65% in 2022 and the 2025 HUD NOFO changed priorities; the DHS/TCP contract is the largest, least documented and most at risk, and Sisters Rise left the 2025 HIC (flag D2).
4. **DC pools are flat to rising, with cuts proposed every spring** (M2-03): OVSJG Victim Services grants approved $45.5M (FY24) → $55.9M (FY25) → $55.4M (FY26) → $55.3M (FY27); the Mayor's FY26 proposal ($50.1M, −10.4%) was restored by the Council. DHS continuum $170M (FY24) → $206M (FY26) → $194M (FY27); PSH $145–166M. Actual spending runs 9–14% below approved on OVSJG.
5. **Calvary is a price-taker in each pool** (M2-04): 5.3% of DC CoC awards, 1.1% of OVSJG awards.
6. **Scenarios** (M2-05; FY25 baseline: revenue $4.97M, expenses $5.58M, cash $2.06M, deficit −$607K):

| Scenario | Revenue loss | % of revenue | Deficit (gross) | Months of cash after a year (net) |
|---|---|---|---|---|
| OVSJG −10% | −$67K | 1% | −$675K | 3.1 |
| OVSJG −25% | −$168K | 3% | −$776K | 3.0 |
| CoC renewals −15% | −$178K | 4% | −$785K | 2.9 |
| One CoC project lost (New Foundations 2) | −$366K | 7% | −$973K | 2.7 |
| DHS/TCP contract not renewed | −$960K | 19% | −$1.57M | 2.1 |
| Combined (OVSJG −25%, CoC −15%, DHS lost) | −$1.31M | 26% | −$1.91M | 1.7 |

OVSJG cuts are survivable; a TCP contract loss is not without new money or cost cuts. Even the baseline uses cash: at the FY25 run-rate, cash lasts about 41 months.

### Charts
- `m2_01_stream_map` – Calvary recurring government streams by award year and channel (one source per stream)
- `m2_01b_one_time_awards` (table) – Calvary one-time government awards
- `m2_02_ceilings_vs_recognized` – Government award ceilings aligned to Calvary FY vs recognized government revenue
- `m2_03_stream_durability` (table) – Calvary government streams: size, trend, funding source, renewal mechanism and durability risk
- `m2_04_dc_budget_context` – DC budget lines behind Calvary's local streams: approved vs actual, FY2021-FY2027
- `m2_05_pool_shares` – Calvary's share of all OVSJG awards and of DC CoC awards by year
- `m2_06_policy_timeline` – DC budget events of $1M+ touching homeless, PSH, DV and victim-services lines, FY2024-FY2027
- `m2_07_scenarios` – Stress-test scenarios on Calvary's FY25 government revenue (config/scenarios.yaml)
- `m2_07_scenario_parameters` (table) – Scenario baseline parameters

### Caveats
- DHS/TCP amounts are public for FY2024 only; every other year of that stream is unknown, not zero.
- HUD CoC award years are competition years; the one-year lag to Calvary's operating year is an assumption.
- Scenario stream shares are apportioned from ceilings, not from Calvary's ledger.
- Federal policy risk (2025 CoC NOFO, EHV sunset) is only partly captured in the data and is noted as external context.

### Confidence
High on the stream map, pool shares and DC budget lines; medium on ceilings-vs-recognized and the scenarios (apportionment and carry-forward assumptions); durability ratings are judgment.

---

## M3 Peer benchmarking

### Question
Where does Calvary sit against comparable organizations on reliance on government, size, growth, liquidity and private funder base, and which peers show a workable path to lower concentration?

### Method
- Core peers are the 18 **provisional** organizations in `calvary_funding_data/config/core_peers.csv`; DWC and the CBWC Empowerment Institute (SheWorks) appear as Los Angeles reference rows on every chart.
- Preferred 990 rows FY2015–FY2025. Government share = line 1e ÷ total revenue, except Calvary FY≤2023 (audit basis). Three-year means (FY2022–24) smooth single-year reporting breaks.
- Real growth = CAGR of 2024-dollar revenue FY2019→FY2024 (endpoints avoid Calvary's one-time FY22 award). Months of cash = cash and savings ÷ monthly expenses.
- Funder base = filed grants naming each organization TY2020–24, institutional vs DAF; depth = institutional dollars ÷ FY2020–24 revenue.
- Typology: government-anchored ≥65%, mixed 35–65%, philanthropy-led <35%. Sector distributions: `dc_sector` FY2023 (n=163), `size_matched` FY2022 (n=334), `national_women` FY2022 (n=542).

### Findings

| Organization | Rev FY24 | Gov share FY22–24 | Real CAGR FY19–24 | Months of cash FY24 | Institutional funders | Inst. $ ÷ revenue | Type |
|---|---|---|---|---|---|---|---|
| **Calvary** | $5.8M | 53% | +13.8% | 5.2 | 42 | 12% | mixed |
| DC SAFE | $7.0M | 89% | +17.7% | 0.9 | 7 | 3% | gov-anchored |
| My Sister's Place | $7.2M | 83% | +19.4% | 2.9 | 25 | 8% | gov-anchored |
| DASH | $7.0M | 70% | −2.7% | 4.0 | 23 | 5% | gov-anchored |
| House of Ruth DC | $14.6M | 53% | +5.0% | 3.8 | 83 | 8% | mixed |
| N Street Village | $10.0M | 42% | −1.7% | 8.0 | 54 | 6% | mixed |
| Samaritan Inns | $7.1M | 44% | +10.1% | 4.5 | 14 | 27% | mixed |
| Miriam's Kitchen | $11.3M | 0% | +12.0% | 4.1 | 66 | 11% | philanthropy-led |
| DWC (LA, ref.) | $34.4M | 57% | +19.0% | 2.4 | n/a | n/a | mixed |
| CBWC Inst./SheWorks (LA, ref.) | $1.5M | 86% | n/a | 4.8 | n/a | n/a | gov-anchored |

Full table: `chart_data/m3_00_benchmark_table.csv` (20 organizations, all metrics).

1. **Calvary is mid-pack on government share** (M3-01): 53%, below every DC DV provider (70–89%) and above the philanthropy-led models (Miriam's Kitchen, Thrive DC, Christ House). Against the broader sector it is typical: 57th percentile in the DC sector, 46th among national women's/DV organizations (M3-02).
2. **Growth has come on both models** (M3-03): Calvary's +13.8%/yr real growth trails only My Sister's Place, DWC and DC SAFE, a strong record for the team; Miriam's Kitchen grew +12%/yr with almost no government money.
3. **Liquidity is mid-pack** (M3-04): 5.2 months in FY24 (4.4 in FY25). Government-anchored DV providers run on ~1 month; Doorways, Everyone Home DC and N Street Village hold 8–12 months.
4. **Calvary already works institutional funders harder than most peers** (M3-05): 42 institutional funders and filed institutional grants equal to 12% of revenue, versus 6–8% at N Street Village and House of Ruth DC; only Samaritan Inns (27%) is far ahead. The headroom is in grant size and multi-year commitments, in DAF/major-donor giving (N Street Village 51% of filed grants via DAFs, Calvary 25%), and in earned revenue.
5. **Three paths** (M3-06): Samaritan Inns replaced government (72% → 11%) with program-service and other revenue while revenue held near $6–7M; N Street Village grew private giving alongside a stable ~40% government share; DWC and House of Ruth MD scaled with government rising above 55%. The N Street Village path is the closest fit for Calvary; Samaritan Inns shows the earned-revenue option; DWC shows that scaling with government needs a much larger balance sheet (DWC's months of cash: 2.4).
6. **Shared DC pools** (`m3_09`): the DV peers draw $3–5M a year each from OVSJG; Calvary's $1.05M makes it a mid-sized OVSJG grantee and one of the larger CoC sub-recipients ($1.77M; only Christ House and My Sister's Place draw more).

### Charts
- `m3_01_gov_share_ranked`, `m3_02_size_vs_gov_share`, `m3_03_real_growth`, `m3_04_months_of_cash`, `m3_06_institutional_base` (PNGs; data `m3_00_benchmark_table`) – Peer benchmark table: Calvary, 18 provisional core peers, 2 named comparators
- `m3_05_gov_share_trajectories` – Government share of revenue FY2017-FY2025, 20 organizations
- `m3_07_sector_distributions` – Government share distributions in the comparison universes, with Calvary's percentile
- `m3_08_case_studies_mix` – Revenue mix FY2018-FY2025 for four model organizations
- `m3_09_peer_pools` – OVSJG FY2026 and HUD CoC FY2025 awards to Calvary and core peers

### Caveats
- Core peers are provisional; swapping them is a config edit plus rerun.
- Line 1e understates government for organizations that book contracts as program revenue (Samaritan Inns' FY24–25 drop may be partly reclassification).
- Funder-base metrics cover DMV funders' filings only; TY2024 partial.
- DWC's fiscal year is the calendar year; CBWC Institute has three years of filings and SheWorks itself begins after TY2024.

### Confidence
High for shares, growth, liquidity and sector percentiles; medium for funder-base depth and the typology of diversifiers (judgment on three cases).

---

## M4 Funder landscape (DC and DMV)

### Question
Who funds Calvary's space in DC and the DMV, at what scale, how concentrated is it, and how has it moved TY2020–24?

### Method
- `fact_grants` rows from funders' own filings (990-PF grants paid, Schedule I), TY2020–24, non-cumulative, excluding the two funders in `config/landscape_exclusions.csv` (the Gates Foundation, global-development recipients; TCP, a government pass-through).
- Lens A: grants to the 1,027 `dc_sector` organizations. Lens B: grants to DC/MD/VA recipients whose purpose text is tagged housing, DV or women.
- DAF sponsors (Fidelity, Schwab, Benevity/AOGF, NPT, Vanguard and others) are donor intermediaries and are reported separately from institutional decision-makers.
- Landscape table: one row per institutional funder (dollars, recipients, grant sizes, mission tags, Calvary and peer funding, "see attached" years).

### Findings
1. **Scale** (M4-01): about $132M a year flows from DMV funders into DC-sector organizations ($660M TY2020–24), 58% of it through DAF sponsors and 42% ($260M) from 555 institutional funders. Institutional dollars to the sector rose from ~$50M (TY2020–23) to $72M in TY2024 even with partial TY2024 filings.
2. **Concentration** (M4-02): the top 10 institutional funders give about half of institutional dollars to the DC sector. Of the 25 largest, 6 already fund Calvary (GWCF, Cafritz, Bank of America, United Way NCA, Jane Bancroft Robinson, Abell), a mark of the relationships Calvary's team holds. The largest non-funders are Clark Charitable ($32.8M to 20 DC organizations, 5 core peers), JPMorgan Chase Foundation ($18.0M, mostly matching gifts), Wal-Mart, Annie E. Casey, Weinberg, Morningstar, Diana Davis Spencer and Meyer (full list in `m4_00_funder_landscape_table.csv`).
3. **Grant size** (M4-03): the median institutional grant to a DC-sector organization is ~$15K (private foundations $10K, community foundations $40K); six-figure grants are the top decile. A $0.5M/yr increase in institutional revenue is a handful of six-figure, multi-year relationships, not dozens of $10K grants.
4. **DAF channel** (M4-04): Fidelity Charitable moved $179M into DC-sector organizations in five years, NPT $80M, Benevity $49M, Schwab $36M. This is individual-donor money routed through sponsors; Calvary's $1.1M over five years (25% of its filed grants) tracks its major donors.
5. **Purpose** (M4-05): most institutional money is general operating or untagged; dollars whose purpose names housing, DV or women are a minority. The biggest mission-tagged funders in the DMV (Weinberg, The Community Foundation, Clark, Wells Fargo, Abell) are mostly Maryland and Virginia foundations, several of which give little in DC.

### Charts
- `m4_00_funder_landscape_table` (table) – Institutional funders of DC-sector organizations TY2020-24 (landscape table; base for M5 and M7)
- `m4_01_dc_sector_by_year` – Grants to DC-sector organizations by funder tax year: institutional vs DAF
- `m4_02_dc_sector_by_funder_type` (table) – Grants to DC-sector organizations TY2020-24 by funder type
- `m4_03_top_institutional_funders` (PNG; data `m4_00_funder_landscape_table`) – see `m4_00` title above
- `m4_04_concentration` – Cumulative share of institutional DC-sector grant dollars by funder rank
- `m4_05_grant_size_by_type` – Grant size distribution to DC-sector organizations by funder type
- `m4_06_daf_sponsors` – DAF sponsor grants to DC-sector organizations by sponsor and tax year
- `m4_07_purpose_tags` – Institutional DC-sector grant dollars by program-area tag (purpose text)
- `m4_08_mission_tagged_funders` – Institutional funders of DMV grants tagged housing / DV / women, TY2020-24

### Caveats
- Funder tax years; TY2024 partial, TY2025 excluded.
- "See attached" filers (476 returns / 667 rows, ~$3.5B DMV-wide) have no recipient names, so Philip L. Graham, Clark-Winchcole and (some years) Bank of America are under-counted.
- Corporate giving without a foundation vehicle is invisible; a few research-oriented national recipients remain in the sector universe.

### Confidence
High on totals, concentration and grant sizes; medium on purpose tags (keyword-based) and the mission-tagged lens.

---

## M5 Funder gap analysis

### Question
Which funders support Calvary's peers or the DC sector but not Calvary, which former funders have lapsed, where do current funders have headroom, and how much of Calvary's CRM-recorded institutional giving can be verified?

### Method
- Filed grants TY2020–24, non-cumulative, landscape exclusions applied. "Funds Calvary" = any filed grant naming Calvary TY2020–24. "Itemized TY2023+" = the funder filed itemized grant lists in TY2023 or TY2024, so a missing Calvary grant is current, not filing lag.
- Gap categories: (G1) institutional funders of ≥2 core peers with no Calvary grant; (G2) lapsed Calvary funders (last grant ≤TY2022, funder itemized since); (G3) current funders whose largest grant to a core peer exceeds their largest to Calvary; (G4) funders giving ≥$500K to the DC sector with no Calvary grant; (G5) funders on ≥2 peer donor lists but on no Calvary list or filing; plus the CRM reconciliation from `supp_crm_cash_verification`. The candidate base (166 funders) feeds M7.

### Findings
1. **Peer funders not funding Calvary** (M5-01): 23 institutional funders give to three or more of the 18 peers with no filed grant to Calvary; 75 give to two or more. Leaders: Venable Foundation (10 peers; in Calvary's CRM for $75K, so filing lag), T. Rowe Price Program for Charitable Giving (8; a DAF-like program), Gifts for the Homeless (8; in-kind), Capital Area Food Bank (7; in-kind food), America's Charities (7; workplace giving, also in the CRM), JPMorgan Chase Foundation (7; matching gifts), **Clark Charitable Foundation (5 peers, $7.8M, median grant $250K)**, Give Lively, Schattner (4, $800K), Bunting, Bechtel, Cohen (3, $940K), Bernstein (3, $908K), The Washington Home (3, $873K), Dweck, Jack R. Anderson, Collins. All 23 filed itemized lists in TY2023+.
2. **Lapsed funders** (M5-02): 12 former institutional funders itemized grants since TY2023 with nothing for Calvary ($255K historically): World Bank Community Connections Fund ($100K, TY2022), Many Hands ($55.5K, TY2020), Jane Bancroft Robinson ($25K, TY2020), Robert M. Fisher ($25K, TY2022), Junior League of Washington, Levatus, Phase Foundation, Poole, Spur Local, Jacquemin, Grossman, Whispering Bells. Max & Victoria Dreyfus is unclear (no itemized TY2023+ return in the data).
3. **Headroom with current funders** (M5-03): 15 current institutional funders have written larger single grants to a core peer than to Calvary. The material ones: Cafritz ($170K to Calvary vs $250K to a peer), GWCF ($458K vs $526K), Bank of America ($15K vs $50K), United Way NCA ($23K vs $56K), Ludwig ($25K vs $50K), Shaver, Fowler ($40K vs $50K), Dreyfus.
4. **DC-sector majors without Calvary** (G4): 41 institutional funders gave ≥$500K to DC-sector organizations TY2020–24 with no Calvary grant, led by Clark, JPMorgan Chase, Wal-Mart, Casey, Weinberg, Morningstar, Diana Davis Spencer, Rast, Meyer, Capital Area Food Bank, Wells Fargo ("see attached" since TY2023); full list in `m5_04_dc_majors_not_calvary.csv`.
5. **Web-list-only gaps** (G5): 16 names appear on two or more peer donor lists but on no Calvary list or filing, mostly corporations with no public filing (Accenture, Boeing, Carlyle, Deloitte, GMMB, Mars Foundation, World Bank Group) plus a few small foundations (`m5_05_web_list_gaps.csv`).
6. **CRM reconciliation** (M5-04): of the CRM's $10.56M (160 funders, 2023–26), $4.63M (44%, 25 funders) is confirmed in the funder's own TY2023+ filing; $2.55M (92 funders) is corporate or otherwise has no public filing (MGAC, IMF, Latham & Watkins, Frontier Co-op, Reservoir); $1.61M (29 exempt filers) shows no Calvary row; $1.28M comes from "see attached" filers (Philip L. Graham, Clark-Winchcole, Kay, Herb Block, Loughran, Kirkland & Ellis); $0.48M was confirmed only in earlier years. Corporate relationships are a larger share of private money than filings show.

### Charts
- `m5_00_candidate_funders` (table) – Candidate funder base for scoring (M7): current, lapsed, peer-funder and DC-major gaps with evidence fields
- `m5_01_peer_funders_not_calvary` – Institutional funders of 2+ core peers with no filed grant to Calvary, TY2020-24
- `m5_02_lapsed_funders` – Calvary funders in filings whose last grant was TY2022 or earlier
- `m5_03_current_funder_headroom` – Calvary's current institutional funders: Calvary grant size vs the same funder's grants to core peers
- `m5_04_dc_majors_not_calvary` (table) – Institutional funders giving $500K+ to DC-sector organizations TY2020-24 with no filed grant to Calvary
- `m5_05_web_list_gaps` (table) – Funders named on 2+ peer donor lists but on no Calvary list or filing
- `m5_06_crm_reconciliation` – Calvary CRM funders (2023-26) reconciled against funders' own filings

### Caveats
- A filing "gap" can be a gift routed through a DAF, matching program or fiscal sponsor; check the CRM before outreach.
- Peer donor lists are undated and amount-less; only six peers publish them.
- Several high-count gap funders are in-kind or workplace channels; M7 scores them down.
- Core peers are provisional; the gap list moves with the peer set.

### Confidence
High on the filing-based gap and lapsed lists; medium on headroom (single largest grants may be capital or restricted) and on web-list gaps.

---

## M6 Network analysis

### Question
Which funders sit at the center of the web around Calvary and its peers, which peers share Calvary's funders, how much do board interlocks add, and how strong is the relationship path to each candidate funder?

### Method
- Bipartite graph: funders × 19 recipients (Calvary + 18 provisional peers), edges = filed grants TY2020–24, landscape exclusions applied. Degree = organizations funded; betweenness on the unweighted graph.
- Co-funding overlap per peer: shared institutional funders with Calvary (DAF sponsors excluded), Jaccard, and the peer's institutional funders that do not fund Calvary.
- Board interlocks from `fact_org_relationships` (`shared_board_member`) touching Calvary, a peer or a named comparator; matched on exact normalized name plus a corroborating signal. **Leadership materials use high-confidence links only; medium links are labeled "unconfirmed" and go to the consulting team.** No names are stored.
- Relationship-path score (0–1): 0.40 × peers funded (cap 12) + 0.25 × close peers funded (cap 8) + 0.25 × overlapping co-funders (cap 20) + 0.10 × any high-confidence board link; consulting variant adds 0.05 for a medium link.

### Findings
1. **Central funders** (M6-01): 330 funders connect the 19 organizations. By organizations funded: GWCF 18, Benevity/AOGF 18, Schwab DAF 16, Cafritz 14, Vanguard 13, NPT 13, United Way NCA 13, Blackbaud Giving Fund 11, Venable Foundation 10, Bank of America 10, Abell 9, T. Rowe Price Program 8, Fowler 8, Gifts for the Homeless 8. Every one of these funds Calvary except Venable, T. Rowe Price, Gifts for the Homeless and (further down) Capital Area Food Bank, America's Charities, JPMorgan Chase, Clark. Calvary is in the core of the web, not at its edge, which reflects years of relationship-building by its team.
2. **Overlap** (M6-02): Calvary shares the most institutional funders with Miriam's Kitchen (17), DASH (14), House of Ruth DC (14), New Endeavors by Women (12) and My Sister's Place (12). The longest lists of institutional funders Calvary lacks belong to House of Ruth MD (81), House of Ruth DC (69), Miriam's Kitchen (48), N Street Village (45), Community of Hope (33), Doorways (29).
3. **Board interlocks are thin** (M6-03): Calvary has 8 shared-board links in filings, 1 at high confidence (Clean Power Institute, not a funder) and 7 at medium confidence, **unconfirmed** (Washington Area Women's Foundation, United Way NCA, United Way of Central Maryland, DAVIS Construction Foundation, Charter School Incubator Initiative, Miriam's Kitchen, Dress for Success). Across all 19 organizations, 27 interlocks touch a funder, 3 at high confidence. `candidate_interlocks` (low confidence) has one row touching the peer set and none touching Calvary. The 17 board-employer overlaps from Prompt 1 (Capital One, DAVIS, Venable, KPMG, Baker Tilly and others) are a stronger lead than filings, but they are corporate relationships, not foundation boards.
4. **Paths** (`m6_05`): the strongest paths to non-funders run through peers: Venable (10 peers, 9 close, 22 overlapping co-funders), T. Rowe Price Program (8/7/16), JPMorgan Chase (7/7/15), Capital Area Food Bank, America's Charities, Clark (5/5/14), Give Lively, Schattner, Bunting, Bechtel. Among current funders the most deeply embedded are GWCF, Cafritz, Abell, Fowler, Bank of America and United Way NCA.

### Charts
- `m6_01_central_funders` (table) – Funders ranked by how many of the 19 organizations (Calvary + 18 peers) they fund, with betweenness centrality
- `m6_02_cofunding_overlap` – Funder overlap between Calvary and each core peer (filed grants TY2020-24)
- `m6_03_network` (PNG, 58 funders of 3+ organizations; data `m6_03_network_nodes` and `m6_01_central_funders`) – Nodes and layout of the network diagram (funders of 3+ organizations)
- `m6_04_board_interlocks` (table) – Shared-board links between Calvary / peers / named comparators and other organizations, with confidence
- `m6_05_relationship_paths` (table) – Relationship-path scores for candidate funders: peers funded, close peers, overlapping co-funders, board links

### Caveats
- DMV funders' filings only; corporate and DAF-routed gifts are partly visible.
- Interlocks rest on name matching; a medium match may be two different people. Treat as leads.
- Path weights are analyst choices, reweightable in M7.

### Confidence
High on the graph and overlap counts; high that board paths are thin; medium on the path-strength construct.

---

## M7 Opportunity pipeline and scoring

### Question
Which funders and programs should Calvary pursue first, and on what evidence?

### Method
Candidate base = M5 gaps joined to M6 relationship paths and the M4 landscape; DAF sponsors excluded (the T. Rowe Price Program is scored like a DAF). Seven dimensions scored 0–1 and weighted per `config/scoring_weights.yaml`: mission fit 0.20 (issue tags plus share of DC-sector dollars naming housing/DV/women), peer giving 0.20 (core peers funded, cap 8), regional giving 0.10 (DC-sector dollars, log $50K → $10M), award size 0.15 (median grant, log $5K → $250K), accessibility 0.10 (funder type and breadth; −0.15 for "see attached" filers, −0.30 for in-kind or workplace channels), durability 0.10 (years active), relationship 0.15 (M6 path strength + 0.35 current funder + 0.20 lapsed + 0.15 on Calvary's CRM/lists).

Tiers: **Tier 1** score ≥ 0.62 and typical grant ≥ $25K (max 20); **Tier 2** score ≥ 0.48; **Tier 3** the rest. Government rows (OVSJG, DHS/TCP, HUD CoC, DHS PSH, HUD CPF) and corporate CRM relationships (≥$50K, no public filing) carry analyst scores (basis = inferred). Federal Grants.gov notices are Tier 3 by default.

### Findings
Result as stated in the readout (182 rows; see Consistency notes for the register's 182-row version):

| Track | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|
| Institutional: steward / upgrade | 4 (Abell, GWCF, Cafritz, Fowler) | 12 | 22 |
| Institutional: new | 3 (Clark Charitable, Schattner, America's Charities) | 15 (Venable, JPMorgan Chase, Gifts for the Homeless, Capital Area Food Bank, Weinberg, Give Lively, The Washington Home, Cohen, Viragh, Arlington CF, Coca-Cola, Morrison & Foerster, Meyer, Eugene B. Casey, ImpactAssets) | 97 |
| DAF channel | – | 1 (T. Rowe Price Program) | – |
| Corporate (CRM) | 1 (MGAC) | 10 (IMF, Reservoir, Latham & Watkins, UnitedHealth, …) | – |
| Government DC | 2 (OVSJG grants; DHS/TCP contracts) | 1 (DHS PSH expansion) | – |
| Government federal | 1 (HUD CoC via TCP) | 1 (HUD CPF renewal) | 12 opportunities |

1. **Tier 1** (M7-01): Abell (0.86), GWCF (0.85), Clark Charitable (0.82, typical grant $250K, 5 peers, no Calvary grant), OVSJG (0.80), Cafritz (0.78), HUD CoC via TCP (0.78), DHS/TCP (0.72), Fowler (0.72), MGAC (0.70), Schattner (0.67), America's Charities (0.64), Frontier Co-op (0.60). The list leads with relationships Calvary already holds, which is the cheapest place to start.
2. **90-day plan** (`recommendations/action_plan_90day.csv`): government rows by day 30 (confirm FY26 award letters and draw-down against ceilings; FY27 renewal calendar); upgrade asks to current majors by day 45 (multi-year general operating at the funder's peer-level amount); warm introductions and LOIs for Clark, Schattner, America's Charities by day 60–90; corporate cash-vs-in-kind quantification. Owner roles: CEO + board chair for ≥$100K and government rows; development director otherwise.

### Charts
- `m7_00_funder_pipeline` – Scored and tiered funder pipeline with application-process notes (config/scoring_weights.yaml; config/guideline_notes.csv)
- `m7_02_pipeline_scores`, `m7_03_tier1_score_breakdown` (PNGs; data `m7_00_funder_pipeline`) – see `m7_00` title above
- `m7_01_action_plan_90day` – 90-day action plan for Tier 1 targets, with application notes
- `m7_04_guideline_notes` – Application process and deadlines for Tier 1-2 institutional funders (web pull, analyst-reviewed)

### Caveats
- Scores rank evidence, not fit with funder guidelines (the approved Tier 1 guideline pull refines this).
- In-kind and workplace channels are penalized, not removed; government and corporate scores are analyst judgment.
- Weights are editable in `config/scoring_weights.yaml`.

### Confidence
Medium: the ordering holds under moderate weight changes (the same ten institutional names stay in Tiers 1–2); exact ranks do not.

---

## M8 Mission-expansion scan

### Question
Which funding pools open up if Calvary formalizes or adds adjacent programs, and how far is each from current operations?

### Method
For each program area: tagged DMV institutional grant dollars TY2020–24 (DAF sponsors and exclusions removed), funders active and at $100K+, relevant Grants.gov notices (research, tribal, rural and overseas removed), DC policy events, and an analyst distance rating (`config/expansion_areas.yaml`): core, near (already delivered in some form), medium (new capability or credential), far (new population or licensing).

### Findings

| Area | Distance | DMV $/yr (tagged) | Funders ($100K+) | Federal notices | Calvary today | Models |
|---|---|---|---|---|---|---|
| Housing and homelessness | core | $32.4M | 391 (104) | 9 | TH 94, PSH 16, RRH 14 | N Street Village, DWC |
| Education and life skills | near | $93.7M | 744 (271) | 5 | LEAP | N Street Village, Thrive DC |
| Workforce and employment | near | $30.4M | 181 (66) | 6 | Step Up DC; SNAP E&T | SheWorks (stipends, childcare, employer partners); DWC MADE |
| Behavioral health and recovery | near | $20.7M | 251 (84) | 17 | On-site therapy, recovery | Samaritan Inns; N Street Village |
| DV and victim services | near | $4.5M | 161 (34) | 3 | DV-designated site; OVSJG | DASH, My Sister's Place, DC SAFE |
| Physical health | medium | $84.2M | 697 (206) | 0 | Meals, partnerships | Community of Hope (FQHC), Christ House, DWC clinic |
| Aging and older adults | medium | $9.7M | 153 (34) | 2 | Older PSH residents | DWC; The Washington Home |
| Women veterans | medium | $7.7M | 152 (34) | 5 | None documented | Access Housing DC; VA GPD |
| Reentry | medium | $1.0M | 39 (8) | 5 | Served, not named | SheWorks; OVSJG reentry |
| Maternal and family health | far | $4.2M | 60 (12) | 3 | Single women only | Community of Hope, House of Ruth |

1. **Near pools are substantial** (M8-01): education, workforce, behavioral health and DV together carry about $149M a year of tagged DMV institutional grants. Calvary already runs programs in each; formalizing them (named program, outcomes, credentials) opens funders without changing the mission. The education figure is dominated by schools and scholarships, so its practical share for Calvary is small; workforce and behavioral health are the real near pools.
2. **Health is the largest medium-distance pool** ($84M/yr, 206 funders at $100K+). The peer models are partnerships (DWC's clinic with JWCH; Community of Hope's FQHC), not building a clinic. A behavioral-health certification that allows Medicaid billing would turn therapy from a cost into program-service revenue (Samaritan Inns' path).
3. **Aging, veterans and reentry pools are small** in DMV philanthropy; their money is federal (VA GPD, DOL HVRP, DOJ reentry) and program-specific. Reentry fits Calvary's population (OVSJG runs reentry grants) but the private pool is $1M/yr.
4. **Federal direct competition is thin** (M8-02): 36 relevant notices, mostly HUD programs that flow through DC, DOJ behavioral-health and reentry, SAMHSA forecasts, DOL VETS HVRP and VA grants. Realistic direct targets: HUD CPF earmark renewal, DOL HVRP (if a veterans track is added), SAMHSA treatment/recovery (with a licensed partner).

**Trade-offs carried into the recommendations:** workforce (near, recommended: SheWorks-style cohort inside Step Up DC, unlocks DOES/WIOA, modest cost); behavioral health (near, recommended with a credential decision: DBH certification or a partner converts therapy to billable revenue, the biggest earned-revenue lever); DV formalization (near: deepens OVSJG, adds reporting burden); health partnership (medium: FQHC clinic hours, low capital); aging (medium: small pool, strong narrative); families/maternal (far, not recommended).

### Charts
- `m8_01_expansion_scan` – Mission-expansion scan: dollars, funders, federal opportunities and DC budget signals by adjacent program area, with distance from Calvary's operations
- `m8_02_federal_opportunities` (table) – Federal opportunities (Grants.gov) tagged to Calvary's core or adjacent areas, after removing research, tribal and overseas notices

### Caveats
Tagged dollars understate what funders would give (general operating excluded); distance ratings are judgment; federal notices are a snapshot.

### Confidence
Medium.

---

## M9 Need and capacity context

### Question
How deep is the need in Calvary's service area, how is DC's homeless population moving, and how much of the system's capacity for single women does Calvary now provide?

### Method
ACS 2020–24 five-year estimates by ward (90% margins of error in the chart data); HUD point-in-time counts for CoC DC-500 (2007–2025); HUD Housing Inventory Count 2022–2025 (Calvary's beds and share of DC transitional-housing beds; women-focused providers flagged); ward map from DC Open Data boundaries colored by poverty rate.

### Findings

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
3. **Calvary's capacity** (M9-02): inventory grew from 68 beds (2022) to 124 (2025): 94 TH beds (6.8% of all DC transitional-housing beds, up from 2.5%), 16 PSH (Sister Circle), 14 RRH. Sisters Rise PSH (24 units) appears in 2024 only. Among women-focused providers in the HIC (N Street Village 457, House of Ruth 388, Open Arms 412, New Endeavors 135, Calvary 124 beds in 2025), Calvary is the fastest-growing, which is a strong case to put in front of funders.

### Charts
- `m9_01_ward_indicators` – ACS 2020-24 indicators: Wards 7 and 8 vs DC
- `m9_02_dc_pit` – DC point-in-time count of people experiencing homelessness, 2007-2025
- `m9_03_calvary_hic_share` – Calvary's transitional-housing beds and share of DC TH beds, HIC 2022-2025
- `m9_04_women_focused_beds` (table) – Beds of women-focused providers in the DC HIC by year
- `m9_05_ward_map` – Ward poverty rates behind the map

### Caveats
- Ward-level ACS has wide margins of error for small subgroups; tract-level figures were not used.
- HIC counts beds, not people served, and project naming changes year to year (Calvary's projects were re-labelled in 2024).
- PIT gender breakdowns are not in HUD's PIT workbook; the CoC's own 2024 subpopulation table counts 2,167 women among 5,616 people.

### Confidence
High.

---

## M10 Named-comparator profiles (CEO request)

### Question
What do the two comparators named by Calvary's CEO, the Downtown Women's Center (DWC, Los Angeles) and the CBWC Empowerment Institute (which runs SheWorks), show about growth paths, funding mix and transferable programs?

### Method
990 financials (line 1e as the government measure); DWC federal programs from FAC single audits FY2020–25; funders from DMV filings plus web sources. Both appear as reference rows on every peer chart.

### Findings

**Downtown Women's Center (DWC), Los Angeles – EIN 31-1597223, NTEE P83, FY = calendar year**

| | FY2014 | FY2018 | FY2021 | FY2024 |
|---|---|---|---|---|
| Revenue | $6.3M | $11.6M | $21.0M | $34.4M |
| Government share (line 1e) | 24% | 31% | 44% | 57% |
| Private contributions | $4.0M | $6.9M | $9.9M | $12.8M |
| Program service revenue | $0.5M | $1.1M | $1.2M | $1.8M |
| Months of cash | 2.1 | 3.1 | 3.1 | 2.4 |

1. **Trajectory** (M10-01): revenue ×5.5 in a decade; government went from a quarter to well over half. Private contributions tripled in absolute terms but fell from 64% to 37% of revenue. Program service revenue (social enterprise, rental) is 5%.
2. **Federal money** (M10-01; $21.6M FY2020–25 in single audits): 99% pass-through, led by HUD CoC 14.267 ($14.3M), ESG 14.231 ($3.5M), VOCA 16.575 ($2.7M), Coronavirus Relief Fund, SNAP E&T, CDBG, EFSP, plus a $194K HUD Community Project Funding award. These are the same federal channels Calvary uses, at about five times the scale, routed through LA County and LAHSA rather than TCP.
3. **Programs:** 159 PSH units plus community-based housing (451 people housed in 2024); Skid Row's only women's health clinic (with JWCH); MADE by DWC paid transitional work; Rosa's Place (97 PSH units) under construction; 358 employees, 1,750 volunteers.
4. **Funders:** 2023 donor list 202 organizations, 2025 list 148; $1M+ band includes GO-Biz, LA County DHS and LAHSA; announced grants: Hilton $1.53M over two years (2026), Blue Shield of California Foundation $450K (2024), Ahmanson $325K (FY2023), Anthem Blue Cross Foundation $200K (2023) and $300K (2026), LA County First District $3M (2025). DMV funders in the data: Bank of America Charitable Foundation ($154K over four years), Wells Fargo ($100K), Give Lively, ImpactAssets, Bainum, JPMorgan Chase. DAF grants to DWC are not captured.
5. **What transfers to Calvary:** the housing-development pipeline, the health-clinic partnership, a paid transitional-work enterprise with earned revenue, and donor-base scale. Not the mix: DWC scaled *with* government and runs on 2–3 months of cash, the concentration Calvary is working to reduce.

**California Black Women's Collective Empowerment Institute (runs SheWorks) – EIN 88-2046704, Carson CA, FYE June, founded 2022**

| | FY2023 | FY2024 | FY2025 |
|---|---|---|---|
| Revenue | $1.38M | $1.49M | $1.84M |
| Government share | 88% | 85% | 70% |
| Private contributions | $169K | $223K | $558K |
| Months of cash | 28.5 | 4.8 | 8.2 |

6. **Profile** (M10-02): a young research-and-advocacy institute that started almost entirely on government funding and is diversifying quickly; it also makes small grants ($42.5K to 8 organizations in TY2024).
7. **SheWorks** was announced in October 2025 and runs its first cohort (about 30 women, January–May 2026) at the L.A. Care / Blue Shield Promise Community Resource Center in Long Beach, with stipends, childcare and ride credits; the LA County Federation of Labor is a partial funder and the health plans host in kind. No FAC or USAspending awards; its funding will appear only in TY2025+ filings.
8. **What transfers to Calvary:** the program design (cohort model, stipends, childcare and transport, employer and health-plan partners, system-impacted women as a named population) as an upgrade to Step Up DC, and the labor-federation + health-plan partner structure. Not a funding model: the parent relies on government more than Calvary does.

### Charts
- `m10_01_comparator_trajectories` – DWC and CBWC Institute revenue mix and government share by fiscal year
- `m10_02_dwc_federal_programs` – DWC federal expenditures by program (FAC single-audit SEFA, FY2020-25)
- `m10_03_comparator_funder_sources` (table) – Funder evidence for DWC and CBWC Institute by source type
- `m10_04_dwc_dmv_funders` (table) – DMV funders' filed grants to DWC TY2020-25
- `m10_05_dwc_named_grants` (table) – DWC grants named with amounts in web sources (funder announcements, annual reports)

### Caveats
DWC's fiscal year is the calendar year; line 1e is the government measure for both (no audits in the data except DWC's single audits for federal money); LA-area funders of DWC are only partly captured (web lists without amounts, DMV funders' filings only).

### Confidence
High on DWC's trajectory and federal programs; medium on funder lists; medium on the SheWorks parent (three filings, program launched after the last one).

---

## The verdict

Copied from `recommendations/funding_pressure_verdict.md` (draft for CP2). The verdict uses the plain verdict words the design system reserves for verdicts ("exposed", "concentrated"); the surrounding report keeps to "concentration", "reliance" and "headroom".

> Calvary is **exposed, but not because its government share is unusual**. Government supplies 53% of revenue (FY2022–24 average on the audit basis; 58% in FY25 on the 990), which is mid-pack among DC peers and near the median of the sector. The exposure is structural: (1) the government money arrives through **three channels, two of them via a single intermediary** (TCP carries the HUD CoC renewals and the DHS contract, about 74% of Calvary's recurring award base); (2) **private revenue is flat and concentrated**: filed institutional grants have stayed near $1M a year from the same 26–29 funders, one funder (GWCF, including the time-limited Health Equity Fund) is 27% of five years of filed grants, and event income fell from $538K to $55K in FY25; (3) **the cash cushion is thinning**: FY25 ran a $607K deficit, cash fell to 4.4 months (7.5 in FY21), and at the FY25 run-rate cash lasts about 41 months with no shock at all. The DC budget lines behind Calvary's local money are flat to rising through FY2027, but the Mayor proposed cuts to victim-services and DV lines in each of the last two springs and the Council restored them: the local risk is annual and political, not structural. The federal side (CoC renewals, EHV sunset) is the larger uncertainty.
>
> **Rating: moderate-to-high exposure, driven by channel concentration and liquidity rather than by the government share.**

**Evidence**

| Claim | Figure | Source |
|---|---|---|
| Government share, FY2022–24 mean (audit basis to FY23) | 53%; FY25 58% (990 line 1e) | m1_02, m1_03, m3_00 |
| Rank among 19 DC-area organizations | 11th of 19; DC DV providers 70–89%; philanthropy-led peers 0–27% | m3_01 |
| Sector percentile | 57th (DC sector FY23), 46th (national women's/DV FY22) | m3_07 |
| Recurring award base 2024 | $4.1M: OVSJG $0.91M, HUD CoC via TCP $1.76M, DHS via TCP $1.42M | m2_01 |
| Share of award base via TCP | 74% | m2_01 |
| Recognized vs awarded | FY24 73%, FY25 67% of known ceilings recognized as revenue | m2_02 (flag D1) |
| Filed institutional grants | $0.64–1.17M/yr TY2020–24; 26–29 funders/yr; GWCF 27%, top five 63% | m1_07, m1_08 |
| Event income | $538K (FY24) → $55K (FY25) | m1_06 (flag D3) |
| FY25 margin and cash | −$607K; cash $2.06M = 4.4 months | m1_04, m1_05 |
| OVSJG pool | approved $55.9M FY25, $55.4M FY26, $55.3M FY27; Mayor proposed −$5.8M (FY26) and −$5.6M (FY27), Council restored | m2_04, m2_06 |
| Calvary's share of pools | 1.1% of OVSJG, 5.3% of DC CoC | m2_05 |

Charts cited: `m1_02_revenue_mix`, `m1_03_gov_share_two_measures`, `m1_04_surplus_deficit`, `m1_05_months_of_cash`, `m1_06_events`, `m1_07_calvary_funder_concentration`, `m1_08_filed_grants_by_year`, `m2_01_stream_map`, `m2_02_ceilings_vs_recognized`, `m2_04_dc_budget_context`, `m2_05_pool_shares`, `m2_06_policy_timeline`, `m2_07_scenarios`, `m3_00_benchmark_table`, `m3_01_gov_share_ranked`, `m3_07_sector_distributions`.

**What would change the verdict:** Calvary's FY24/FY25 audits and TCP subgrant agreements (D1, D2; if awards are under-drawn, the first recommendation becomes "draw what is awarded"); confirmation the FY25 gala moved across the fiscal-year line (D3); a change in the provisional peer set (moves the rank, not the sector percentile).

The path through these clouds is in `recommendations/strategic_recommendations.md`.

---

## Open flags

All three flags were raised 2026-10-10 and **approved as proposed at CP2 (2026-10-10)**. They stay open until Calvary supplies the documents named.

| Flag | Finding | Why it matters | Approved handling |
|---|---|---|---|
| **D1** Ceilings vs recognized | Calvary recognized only ~67–73% of its known government award ceilings as revenue in FY24–FY25 (ceilings $3.6M / $4.3M vs 990 line 1e $2.62M / $2.89M). Line 1e matched the audited figure exactly in FY22–23. | $0.9–1.4M/yr of awarded money may be undrawn (utilization, timing, cost-reimbursement limits), or the DHS carry-forward overstates FY25. Undrawn awards are the cheapest revenue to recover. | Keep at medium confidence, label "ceilings vs recognized", and put "FY24/FY25 audits and TCP subgrant agreements" at the top of the questions for Calvary. No scope change. |
| **D2** Sisters Rise | Sisters Rise (24-unit PSH paired with Emergency Housing Vouchers; $593K DHS/TCP contract in FY2024) is absent from the 2025 HIC. | If the EHV program ended in FY25, part of the FY25 revenue drop is already a lost government stream and the scenario baseline should exclude it. | Treat the DHS stream as "at risk" in M2 durability; ask Calvary; keep the FY2024 value in the baseline until confirmed. |
| **D3** Event income | Event contributions fell from $538K (FY24) to $55K (FY25) while net special-event income turned positive (+$219K). | Explains most of the $0.8M FY25 contribution drop; a reporting or scheduling change rather than donor flight changes the private-revenue story. | Report it as the largest single swing; ask Calvary whether the FY25 gala moved across the fiscal-year line. |

---

## Insight register summary

All 36 rows of `insight_register.csv`, in module order; finding = the register's first sentence as written. † = differs from the module readout (see Consistency notes; the body uses the readout).

| insight_id | module | finding (first sentence) | confidence | status |
|---|---|---|---|---|
| M1-01 † | M1 | Government supplied 40-61% of Calvary's revenue in every year FY15-FY25 on the audit basis (line 1e for FY24-25), and most of the growth since FY19. | high | draft |
| M1-02 | M1 | FY25 ran a $607K deficit with contributions down $0.8M and the cash cushion at 4.4 months, versus 7.5 months in FY21. | high | draft |
| M1-03 | M1 | Event contributions fell from $538K (FY24) to $55K (FY25), the largest single private-revenue swing. | high | draft |
| M1-04 | M1 | Filed institutional grants to Calvary have stayed near $1M a year from 26-29 funders, and one funder (GWCF incl. the Health Equity Fund) is 27% of five-year filed grants; the top five are 63%. | high | draft |
| M1-05 | M1 | The FY22 revenue spike ($8.87M) was a one-time $3.68M SLFRF award for the New Foundations building, not operating growth. | high | draft |
| M2-01 | M2 | Calvary's recurring government awards rose from $0.9M (2019) to about $4.1M (2024) across three channels: OVSJG, HUD CoC via TCP, and DHS via TCP. | high | draft |
| M2-02 † | M2 | In FY24-FY25 Calvary recognized only about 73%-67% of its known award ceilings as revenue. | medium | draft |
| M2-03 | M2 | DC's budgets behind Calvary's local streams stayed flat to rising through FY2027, but the Mayor proposed cuts to victim services and DV lines in both FY2026 and FY2027 and the Council restored them. | high | draft |
| M2-04 | M2 | Calvary receives about 5% of DC's CoC awards and about 1% of OVSJG's awards. | high | draft |
| M2-05 | M2 | A non-renewed DHS/TCP contract would remove about $0.96M (19% of revenue); the combined worst case removes $1.31M and leaves roughly 1.7 months of cash after one year even with 50% cost avoidance. | medium | draft |
| M2-06 † | M2 | Sisters Rise (25 EHV-paired PSH units, $593K DHS contract in FY2024) disappeared from the 2025 Housing Inventory Count. | medium | draft |
| M3-01 † | M3 | Calvary's government share (53%, FY2022-24 mean) ranks 11 of 19 DC-area organizations: below every DC DV provider (75-94%) and above the philanthropy-led models (Miriam's Kitchen, Thrive DC, Christ House, Samaritan Inns). | high | draft |
| M3-02 | M3 | Against the broader sector Calvary is typical: its government share is near the median of DC human-services organizations and of national women's/DV organizations. | high | draft |
| M3-03 † | M3 | Calvary's real revenue growth FY19-FY24 (+13.8%/yr) beat most DC peers; the fastest growers were government-anchored (My Sister's Place, DWC) or philanthropy-led (Miriam's Kitchen). | high | draft |
| M3-04 | M3 | Calvary's liquidity (5.2 months FY2024, 4.4 in FY2025) is mid-pack; government-anchored DV providers run on about one month of cash or less, while Doorways, N Street Village and Everyone Home DC hold 8-12 months. | high | draft |
| M3-05 | M3 | Calvary already works institutional funders harder than most peers: 42 institutional funders TY2020-24 and filed institutional grants equal to 12% of revenue, versus 8% at House of Ruth DC, 6% at N Street Village and 11% at Miriam's Kitchen; only Samaritan Inns (27%) is far ahead. | medium | draft |
| M3-06 | M3 | Three replicable paths among peers: Samaritan Inns replaced government (72% -> 11%) with program and private revenue while holding revenue; N Street Village grew on private money at a stable ~40% share; DWC and House of Ruth MD scaled with government rising above 55%. | medium | draft |
| M4-01 † | M4 | DMV funders put about $132.10M a year into DC-sector organizations TY2020-24 ($660.49M total): 58% through DAF sponsors and 42% from 555 institutional funders. | high | draft |
| M4-02 † | M4 | The institutional pool is concentrated: the top 10 funders give 55% of institutional dollars to the DC sector, and 6 of the top 25 already fund Calvary. | high | draft |
| M4-03 † | M4 | The typical institutional grant to a DC-sector organization is small (median $10K); six-figure grants are the top decile and come from community and private foundations. | high | draft |
| M4-04 | M4 | Fidelity Charitable moved $179.22M into DC-sector organizations in five years, more than any foundation; DAF money is a donor-cultivation channel, not a grant pipeline. | high | draft |
| M4-05 | M4 | Most institutional money to the DC sector is general operating or untagged; grants whose purpose names housing, DV or women are a minority, and the biggest mission-tagged funders are Maryland and Virginia foundations that give little in DC. | medium | draft |
| M5-01 | M5 | 23 institutional funders give to three or more of Calvary's 18 peers and have no filed grant to Calvary; 75 give to two or more. | high | draft |
| M5-02 | M5 | 12 former institutional funders filed itemized grant lists since TY2023 with nothing for Calvary; they once gave $0.26M in total. | medium | draft |
| M5-03 | M5 | 15 of Calvary's current institutional funders have written larger single grants to a core peer than to Calvary. | medium | draft |
| M5-04 | M5 | Only 44% of the CRM's $10.6M in 2023-26 institutional giving is verifiable in funders' own filings; corporate givers with no public filing (MGAC, IMF, Latham, Frontier Co-op) are $2.6M and 'see attached' filers (Philip L. Graham, Clark-Winchcole, Kay, Herb Block) $1.3M. | medium | draft |
| M6-01 † | M6 | The funder web around Calvary and its peers has 330 funders; the most connected institutional funders (GWCF 18 of 19 organizations, Cafritz 14, Venable 10, Abell 9) already fund Calvary except Venable, and the DAF sponsors (Fidelity, Benevity, Schwab) connect almost everyone. | high | draft |
| M6-02 | M6 | Calvary shares the most institutional funders with Miriam's Kitchen (17), DASH (14) and House of Ruth DC (14); House of Ruth DC and House of Ruth MD have the longest lists of institutional funders Calvary lacks. | high | draft |
| M6-03 | M6 | Board interlocks are a thin channel: Calvary has 8 shared-board links in filings, 1 at high confidence (none with a funder); 7 medium-confidence links include Washington Area Women's Foundation, United Way NCA, United Way of Central Maryland and Miriam's Kitchen. | high | draft |
| M7-01 † | M7 | The scored pipeline has 182 rows: 12 Tier 1 (pursue now), 40 Tier 2, 131 Tier 3. | medium | draft |
| M8-01 | M8 | The adjacent areas Calvary already touches (DV, behavioral health, workforce, education) carry about $149.22M a year of DMV institutional grants whose purpose names them; physical health is the largest pool one step further ($84.15M/yr, 206 funders at $100K+). | medium | draft |
| M8-02 | M8 | The Grants.gov feed yields only 36 relevant federal notices across all areas after filtering; the federal path for Calvary runs through DC intermediaries (TCP, OVSJG, DHS), not direct competition. | high | draft |
| M9-01 | M9 | Calvary's service area carries the city's deepest need: Ward 8 poverty 31% and Ward 7 23% against 15% for DC; female poverty 32% in Ward 8; a third of renters in both wards pay over half their income in rent. | high | draft |
| M9-02 | M9 | DC's homeless count fell from 8,350 (2016) to 5,138 (2025) while Calvary's inventory grew to 124 beds and 7% of DC's transitional-housing beds. | high | draft |
| M10-01 † | M10 | DWC grew from $6.31M (FY2014) to $34.40M (FY2024) while its government share rose from 24% to 57%; its federal money is 99% pass-through (HUD CoC, ESG, VOCA), the same channels Calvary uses. | high | draft |
| M10-02 | M10 | The SheWorks parent (CBWC Empowerment Institute, founded 2022) is 70% government at $1.84M revenue, down from 88% in its first year, with private contributions rising from $169K to $558K; SheWorks itself launched in late 2025 with labor-federation and health-plan partners, so its funding will only appear in TY2025+ filings. | medium | draft |

---

## Source note

Every chart ID in this report maps to `chart_data/<id>.csv` (listed in `chart_data/_manifest.csv` with its title, source tables, source IDs, script and row count). Each CSV's `source_ids` map to `calvary_funding_data/sources/source_registry.csv` (the Prompt 1 data build), plus `sources/source_registry_extension.csv` in this analysis folder for the web guideline pull behind `m7_04_guideline_notes` and the pipeline's application notes. Charts that exist only as PNG names (for example `m3_01_gov_share_ranked`, `m1_06_event_income`, `m6_03_network`, `m7_02_pipeline_scores`) are listed in `config/png_data_map.csv`, which maps each to the named chart-data CSV(s) that hold its data. Underlying clean tables are named in each module's Method and in the manifest's `source_tables` column. Data as of 2026-10-10.

---

## Consistency notes

Where inputs disagree, the body uses the module readout.

1. **M1-01 yearly shares:** register evidence gives audit-basis shares of 50% (FY21), 61% (FY22), 51% (FY23); the M1 readout table gives 51%, 64%, 55%. The register's M3-02 row cites 51% for FY2023 on a line 1e basis, so the register may mix measures (not verified).
2. **M2 labels:** the M2 readout tags both the durability and the DC-pools findings as M2-03; the register ties durability to M2-06 (Sisters Rise).
3. **M2-02 gap size:** register "$1-1.4M/yr"; flag D1 "$0.9-1.4M/yr".
4. **M2-06 Sisters Rise:** register finding says 25 units; its own evidence, the M9 readout and D2 say 24.
5. **M3-01 rank and ranges:** register says 11 of 19, DC DV providers 75–94%, and counts Samaritan Inns as philanthropy-led; the verdict says 11th of 19; the readout gives no rank, says 70–89%, and classes Samaritan Inns (44%) as mixed.
6. **M3-03 growth:** register magnitude "+9.6%/yr real" conflicts with its finding and the readout (+13.8%/yr); the register implies Miriam's Kitchen grew faster than Calvary, but the readout shows +12.0%.
7. **M4-01 totals:** register says about $132.10M a year, $660.49M, 555 institutional funders (the `m4_04` manifest note also says 555); the readout says about $132M, $660M, 561. Re-check `m4_01_dc_sector_by_year.csv` before decks quote either.
8. **M4-02:** register and the `m4_04` manifest note say top 10 = 55%; the readout says "about half".
9. **M4-03:** register finding says median $10K, its magnitude ~$15K; the readout gives ~$15K overall, $10K for private foundations.
10. **M6-01:** register says 330 funders and GWCF 18 of 19; the readout says 324 and GWCF 18.
11. **M7 counts and tiers:** the readout says 182 rows and "Tier 1 (11 rows)" but lists 12, and places Frontier Co-op (0.60) in Tier 1 below the 0.62 cutoff. The register gives 182 rows (12 / 39 / 131) and names United Way NCA, Bank of America, Venable, Cohen, Bernstein and The Washington Home among Tier 1 institutional targets; the readout puts Venable, Cohen and The Washington Home in Tier 2. The manifest shows `m7_00_funder_pipeline` (182 rows) was rewritten by the guideline-merge script after the readout, a likely but unverified cause. The readout also calls the guideline pull pending, yet `m7_04_guideline_notes` exists. Re-read `recommendations/funder_pipeline.csv` before citing tiers.
12. **M10-01:** register magnitude "5.5x scale"; readout "×5.5".
13. **Verdict award base:** the verdict lists 2024 OVSJG $0.91M and CoC $1.76M; the M2 readout quotes OVSJG $1.05M (FY26) and CoC $1.77M (FY2025). Different award years, not a contradiction, but decks should not mix them.
