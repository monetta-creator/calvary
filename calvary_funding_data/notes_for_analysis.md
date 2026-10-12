# Notes for analysis

These are patterns, anomalies and questions noticed while building the data. They are observations only; verdicts and recommendations are left to the analysis. Figures were verified in the build; the tables in `clean/` are authoritative if anything here disagrees.

Year labels: `tax_year` (TY) = the year Calvary's fiscal year begins; FY = the year it ends (FYE Sept 30). TY2024 = FY25. ProPublica's `tax_prd_yr` is the FY-end year.

Sections:
1. Calvary: finances and revenue mix
2. Calvary: government funding
3. Calvary: private funders
4. Core peers and the DC sector
5. Regional funder landscape
6. DC budget and policy context
7. Need and capacity context
8. Named comparators (Calvary CEO request)
9. Measurement cautions

## 1. Calvary: finances and revenue mix

- **Revenue (990 basis):**

  | Year | Revenue | Year | Revenue |
  |---|---|---|---|
  | FY11 | $1.45M | FY19 | $2.49M |
  | FY12 | $2.02M | FY20 | $3.90M |
  | FY13 | $1.89M | FY21 | $3.85M |
  | FY14 | $2.07M | FY22 | $8.87M |
  | FY15 | $2.01M | FY23 | $4.46M |
  | FY16 | $1.99M | FY24 | $5.82M |
  | FY17 | $2.26M | FY25 | $4.97M |
  | FY18 | $2.15M | | |

  - FY25 ran a $607K deficit, with contributions down from $5.55M to $4.75M.
  - All 990-based sources (XML, SOI, ProPublica, NCCS, 990 PDFs) agree within 1% in every year.
- **The FY22 spike** (TY2021, $8.87M) is mostly government money:
  - the FY22 audit shows $5.69M in government revenue;
  - the Treasury SLFRF file shows a $3.68M DC subaward on 2022-03-08 for the New Foundations building purchase;
  - net assets rose $4.32M;
  - property and equipment went from $2.74M to $6.33M.
- **Government share of revenue** (audits, total column):

  | FY14 | FY15 | FY16 | FY17 | FY18 | FY19 | FY20 | FY21 | FY22 | FY23 |
  |---|---|---|---|---|---|---|---|---|---|
  | 37% | 41% | 44% | 40% | 43% | 49% | 47% | 50% | 61% | 51% |

  - FY20 adds PPP of 8% on top of the 47%.
  - TY2024 990 line 1e: 58%.
  - See section 9: line 1e alone understates this.
- **Program service revenue** is 0 every year.
- **Special events:** net special-event income is negative every year (−$19.5K to −$149K). Line 1c event contributions were $538K in TY2023 and $55K in TY2024.
- **Audit vs 990:** audits run 0–9% above the 990 on revenue and expenses (GAAP: in-kind and special-event presentation). Net assets match every year.
- **Restatements:** the FY19 audit restated FY18 with events shown net (revenue $2.35M → $2.27M). The FY23 annual report's "$5.42M revenue" is the audit's without-restriction column including releases; total audit revenue is $4.81M.
- **Strategic plans** (`clean/supp_calvary_strategic_targets.csv`):
  - **2016–19:** target 20 new PSH units; reported 45 new housing slots (all types).
  - **2021–24:** target 25 units; the internal final report says 66 units, though its printed components sum to 64.
  - **Fundraising staff:** held at 6 positions with "limited growth" (2021–24 report).

## 2. Calvary: government funding

- **Channels**, all visible in `fact_gov_awards`:
  - DC OVSJG (direct)
  - DC DHS via The Community Partnership (TCP)
  - HUD CoC via TCP
  - federal pass-through via OVSJG, DHS and FEMA (SEFA)
  - small direct federal awards
- **OVSJG awards:**
  - **Reach Up TH:** $368,935 per year FY2019–FY2022, plus $292,000 in FY2019 and $99,500 in FY2022. Then $402,540 (FY23), $430,873 (FY24), $478,622 (FY25), $507,595 (FY26).
  - **New Foundations TH:** $3,680,675 in FY2022 (one-time). Then $438,500 (FY23), $482,528 (FY24), $519,656 (FY25), $543,056 (FY26).
  - **Total:** Calvary's OVSJG total rose from $368,935 (FY2020) to $1,050,651 (FY2026).
  - **Funding source labels:** FY2024–26 lists label all Calvary grants Local, while the FY23 SEFA shows OVSJG federal pass-through (SLFRF 21.027).
- **HUD CoC** (Calvary projects; TCP is the applicant):
  - **Sister Circle PSH:** $239,659 (2019) → $296,930 (FY2025).
  - **Reach Up:** $1,222,263 (2021), $421,930 (2022), $427,330 (2023), $921,970 (2024, including expansion), $923,637 (FY2025).
  - **New Foundations 2:** $469,719 (2023, new), $542,456 (2024), $546,247 (FY2025).
  - **Share of DC-500 awards:** Calvary's three projects are 1.1% (2019) and 5.3% (FY2025, $1,766,814).
- **DHS via TCP:** provider amounts are public for one year only (2024-cycle oversight responses, pp 111–112): Transitional Housing $830,384 (capacity 45) and Sisters Rise EHV $593,280 (capacity 25).
  - TCP's 990s do not itemize provider payments on Schedule I (Schedule I appears only in TY2021–22, with a few rows), so TCP's filings are not a source for this stream.
- **Federal:**
  - **FY22 SEFA $4,067,718:** SLFRF via OVSJG $3,583,885; 14.235 via TCP $415,830; EFSP $48,889; SNAP E&T $19,114.
  - **FY23 SEFA $937,999:** SLFRF $440,677; 14.235 $390,649; EFSP $67,684; SNAP E&T $38,989.
  - **FAC conflict:** FAC's "audit_year 2023" record repeats the FY22 lines ($4,064,718). Both are kept and flagged; the FY22 audit found on Candid matches FAC FY22.
  - **No single audit before FY22:** FY17–FY20 audits state Calvary was not subject to a single audit. The FY21 audit is silent despite $1.98M in "federal and local government contracts".
  - **Direct federal:** HUD 14.251 Community Project Funding $200,000 (2023; $76,866 outlaid), SBA PPP $327,200 (2020), and a LISC subaward of $25,000 (2017).
  - **USAspending blind spot:** DC reports no FSRS subawards for SLFRF, EFSP or CoC-via-TCP.
- **PASS** (DC procurement) shows Calvary POs only FY2019–FY2023 and payments only FY2019–FY2024. The cutoff coincides with DC's FY2025 financial-system change, and TCP's DHS POs drop from $110.4M (FY2024) to $7.1M (FY2025).

## 3. Calvary: private funders

- **CRM export** (internal):
  - **Size:** 160 organizations, $10.56M, 877 gifts. Top 10 = 54%: Cafritz $1.09M, Health Equity Fund $801K, MGAC $713K, Philip L. Graham $634K, Abell $533K, Clark-Winchcole $480K, Leafglen $467K, Capital One $367K, Bank of America Charitable Foundation $328K, Fowler $310K.
  - **By type** (rule-based): foundation $5.91M, corporate $3.78M, corporate matching $358K, civic $302K, DAF sponsor $13K.
  - **Inconsistent rows:** 21 rows have one gift but a total above it (see assumption A1).
- **Funders' own filings** (`clean/supp_crm_cash_verification.csv`):
  - 25 CRM funders confirmed by their own 990-PF/Schedule I in TY2023+.
  - 7 confirmed only in earlier years.
  - 7 CRM rows show only "see attached" grant lists in recent years and no itemized Calvary grant: Philip L. Graham Fund, Clark-Winchcole, Kay Family Foundation, Herb Block, Mary and Daniel Loughran, Kirkland & Ellis Foundation (two CRM rows). Other known funders with attachment-only years: Bank of America Charitable Foundation (TY2024), TJX (TY2024), Wells Fargo Foundation (TY2023), Nancy Peery Marriott (TY2023).
  - 29 exempt funders show no Calvary rows in TY2020+ filings.
- **Grants to Calvary in funders' own filings.**
  - **Filter:** `fact_grants` where recipient_ein = 521307706, source_type in (pf_grants_paid, schedule_i), cumulative_flag ≠ 1, by funder tax_year.
  - **TY2020–24 total:** 138 rows, 50 funders, $4.43M.

  | TY | Funders | Amount |
  |---|---|---|
  | TY2020 | 27 | $637K |
  | TY2021 | 26 | $811K |
  | TY2022 | 29 | $1.16M |
  | TY2023 | 29 | $659K |
  | TY2024 | 26 | $1.17M |

  TY2024 is still arriving.
- **Top 10 funders in those filings** (TY2020–24):
  1. Greater Washington Community Foundation: $1,206,500. This includes Health Equity Fund grants and is Calvary's largest filed funder.
  2. American Online Giving Foundation (Benevity DAF): $511,616
  3. Cafritz: $450,000
  4. Leafglen: $330,000
  5. Fidelity Charitable (DAF): $314,317
  6. Abell: $295,000
  7. Schwab DAF: $128,155
  8. World Bank Community Connections Fund: $100,000
  9. AAMC: $91,500
  10. United Way NCA: $89,549

  DAF sponsors are donor intermediaries; see the README's note on funder types.
- **DAF sponsors to Calvary** (TY2020–24): $1.1M in 26 rows. American Online Giving Foundation (Benevity) $512K, Fidelity $314K, Schwab $128K, NPT $46K, PayPal $42K, Vanguard $31K.
- **Cash vs in-kind** (web evidence):
  - **Health Equity Fund:** cash. It is a Greater Washington Community Foundation fund created under the DC–CareFirst agreement; Calvary was in the 2022 and October 2024 rounds, and My Sister's Place is the only other core peer in both.
  - **World Bank Community Connections Fund:** cash (staff giving plus a match).
  - **MGAC:** mixed. It provides substantial pro bono project management alongside cash and gala sponsorship.
  - **Capital One:** unclear. Cash grants plus pro bono and matching.
- **Recent grants published by funders:**
  - **Cafritz:** $100,000 (2025, general support).
  - **Philip L. Graham:** $200,000 over two years (2025-11-13). This matches the CRM's $100,000 gift on 2025-11-26.
- **Meyer:** appears on the Sept 2023 support page ("over the years"), but its TY2021–24 990-PFs list no Calvary grant, out of 1,254 parsed Meyer grants.
- **Board-to-funder overlap:** 17 board-listed employers also appear on Calvary funder lists. Examples: Baker Tilly, Battelle, Bipartisan Policy Center, Bracewell, Capital One, DAVIS Construction, KPMG, Salt River Project, TV One, Venable, White & Case, Williams & Connolly. CRM totals for those firms include Capital One $367K, DAVIS $117K, Venable Foundation $75K and SRP $48K.
- **Donor lists over time:** only the FY15 annual report prints a donor list. It names 72 organizations, 33 of which are also on the Sept 2023 support page (98 names). Individual listings in FY15: 17 at $5K+, 63 at $1K–5K, 57 at $500–999, 93 at $250–499.

## 4. Core peers and the DC sector

- **Core peers are provisional:** 18 orgs (`config/core_peers.csv`, rationale in `reports/core_peers_proposal.md`).
- **Government share** (990 line 1e / revenue, NCCS):
  - **Core-peer median:** TY2011–21 ranges 39–54% (TY2019 54%, TY2020 53%, TY2021 52%).
  - **Calvary:** 56% in TY2019, above 53% of peers. 13% in TY2020, above 22%; that year is line-1e-distorted (see section 9).
  - **DC sector:** the median is 0% because most small orgs report no government grants.
- **Peer grants.**
  - **Filter:** `fact_grants` where recipient_ein is in the 18 core peers, source_type in (pf_grants_paid, schedule_i), cumulative_flag ≠ 1, funder tax_year 2020–2024.
  - **Totals:** 1,933 rows, $65.7M, from 324 funders, covering all 18 peers.
- **Largest funders of core peers.** DAF sponsors (intermediaries) lead: Fidelity Charitable $8.5M to 17 peers, Benevity $4.8M to 17, Schwab $3.0M to 15, Vanguard $2.0M to 12, NPT $1.5M to 12. All also give to Calvary. The institutional funders:
  - Clark Charitable Foundation: $7.8M to 5 peers, none to Calvary
  - Greater Washington Community Foundation: $5.7M to 17 peers, also Calvary
  - Cafritz: $2.4M to 13 peers, also Calvary
- **Funders of 4+ core peers with no grant naming Calvary in TY2020–24** (same filter; 12 in total):

  | Funder | Peers | Amount |
  |---|---|---|
  | Venable Baetjer & Howard Foundation | 10 | $735K |
  | T. Rowe Price Program for Charitable Giving | 8 | $924K |
  | Gifts for the Homeless | 8 | $157K |
  | Capital Area Food Bank | 7 | $787K |
  | America's Charities | 7 | $420K |
  | JPMorgan Chase Foundation | 7 | $3K, matching gifts |
  | American Endowment Foundation | 6 | $698K |
  | Clark Charitable Foundation | 5 | $7.83M |
  | Give Lively | 5 | $110K |
  | Schattner Foundation | 4 | $800K |
  | Bunting Family Foundation | 4 | $120K |
  | Brendan & Helen Bechtel Foundation | 4 | $100K |

  - Venable Baetjer & Howard (Venable LLP's foundation, a public charity filing Schedule I) appears in Calvary's CRM as "Venable Foundation", $75K in the 2023–26 window. That suggests filing lag rather than absence.
  - America's Charities is also a CRM funder ($1.6K).
- **Funders shared by Calvary and 3+ peers** (web lists): Cafritz (11), Philip L. Graham (10), Share Fund (4), Venable Foundation (4), UWNCA (3), Charles Delmar Foundation (3), IMF (3), America's Charities (3).
- **Funders on 2+ peer lists but no Calvary list:** 23 in total, including Accenture, Helen Bechtel Foundation, Alexander and Margaret Stewart Trust, Capitol Hill Community Foundation, Christ Church Georgetown, Exelon, Lenzner Family Foundation, Shell, Target, Boeing and Carlyle. Only 6 peers post donor lists.
- **Recent funder grant lists** (2024–26):
  - **Cafritz:** 12 grants to 11 peers plus Calvary. Calvary and Covenant House are the largest at $100K; Community of Hope $85K; DC SAFE $60K.
  - **Philip L. Graham Fund:** 12 grants. Community of Hope $300K, Calvary $200K, House of Ruth $150K, Doorways $150K.
- **OVSJG FY2026 to core peers:** DASH $5.28M, DC SAFE $4.61M, My Sister's Place $3.81M, House of Ruth $3.17M. Universe orgs receive 28–42% of OVSJG dollars per year. Calvary's share is 0.7–1.5%, or 4.6% in FY2022.
- **Ward distribution:** 213 of 951 DC-sector orgs with a known ward (22.4%) sit in Wards 7/8, while those wards hold 26.2% of DC residents. Org ward reflects the filing address, not service sites.

## 5. Regional funder landscape

- **DMV private foundations** (itemized 990-PF grants TY2020–24):
  - **Volume:** $15.7B from 3,852 foundations in 355K rows.
  - **Concentration:** the top 1% of foundations account for 48% of dollars.
  - **Grant size:** the median grant is $5,000, and 58% of rows are ≤$5K.
  - **Where it goes:** 58% of dollars go to DC/MD/VA recipients (DC 18%). Purpose text tagged "housing" covers 2%.
  - **Largest:** Wyss, Weinberg, Clark, Annie E. Casey, Charles Koch.
- **"See attached" returns:** 476 990-PF returns ($3.2B) itemize grants only as "see attached". These are real grants without grantee names.
- **Meyer:** its contributions paid (Part I line 25) exceed its itemized grants every year (TY2021 $13.6M vs $9.9M). Keep both measures.
- **DAF sponsors** (Schedule I, DC/MD/VA recipients only):
  - **Volume:** $19.6B to DMV recipients TY2020–24.
  - **To 44 DC homeless/housing/DV/women's orgs:** $42.9M. Fidelity $22.3M, NPT $6.0M, Benevity $5.5M, Schwab $4.8M, Vanguard $2.5M.
  - **Top recipients:** YWCA USA $15.8M, Miriam's Kitchen $3.8M, House of Ruth $3.2M, Friendship Place $2.0M, Calvary $1.1M.
- **BMF NTEE codes** are blank for some large DMV foundations (e.g., Meyer, Philip L. Graham). Funder universes key on foundation status, not NTEE.

## 6. DC budget and policy context (`fact_policy_events`, `supp_dc_budget_lines`)

- **DHS PSH** (H03010–13), approved:

  | FY24 | FY25 | FY26 | FY27 |
  |---|---|---|---|
  | $152.9M | $144.8M | $147.6M | $166.2M |

  - FY27 changes: PSH Families +$25.4M; PSH General $5.41M → $1.0M; PSH Individuals $76.4M → $74.0M.
  - PSH is 98.7% local funds.
- **DHS homeless services continuum** (H03002–04, H03009):

  | FY24 | FY25 | FY26 | FY27 |
  |---|---|---|---|
  | $170.0M | $178.7M | $205.9M | $193.7M |

  The FY27 change includes H03003 General −$13.1M.
- **Family rapid re-housing (FRSP):** approved fell from $73.2M (FY24) to $36.3M (FY26–27), while FY25 actual spending was $111.6M.
- **ERAP:** approved fell from $42.5M to $7.0M.
- **Victim services:**
  - OVSJG grants (P02303): $45.5M, $55.9M, $55.4M, $55.3M (FY24–27). The Mayor proposed −$5.8M (FY26) and −$5.6M (FY27); the Council restored both.
  - DHS DV services (H03007): proposed −$500K in FY26 and FY27; restored each year.
- **LRSP tenant-based:** $128.1M (FY24), $163.8M (FY25–26), $199.2M (FY27).
- **Gaps:** FY2026 has activity totals only; its appendix fund splits are images and were not OCR'd.

## 7. Need and capacity context

- **ACS 2020–24 by ward** (wards are Census SLDU geographies; 90% MOE in `dim_geo`):

  | Measure | Ward 7 | Ward 8 | DC |
  |---|---|---|---|
  | Poverty | 22.9% | 30.6% | 15.4% |
  | Female poverty | 24.8% | 31.7% | 16.3% |
  | Rent burden ≥30% | 55.3% | 54.6% | 46.6% |
  | Rent burden ≥50% | 33.3% | 32.5% | 23.6% |
  | Unemployment | 12.7% | 13.4% | 6.3% |
  | Median household income | $71,088 | $52,769 | $109,870 |

  - **Combined Wards 7+8:** poverty 26.7%, rent burden ≥30% 54.9%.
  - **Ward 8 female householders, no spouse:** 29.8% of households vs 13.1% citywide.
- **Calvary's site:** 1217 Marion Barry Ave SE, formerly Good Hope Rd SE (same MAR ID 338288). It sits in tract 11001007503 (100% Ward 8; ANC 8A, SMD 8A06). Tract MOEs are wide, so compare at ward level.
- **Point-in-Time counts:**
  - **DC:** peaked at 8,350 (2016); 5,138 in 2025.
  - **Other seven DMV CoCs:** 5,562 (2007) → 2,947 (2022) → 4,502 (2025).
  - **Gender:** HUD's PIT workbook has no gender columns. CoC PopSub 2024 shows 2,167 women of 5,616 counted in DC.
- **HIC beds:**
  - **Calvary's share of DC transitional-housing beds:** rose from 2.5% (2022, 45 beds) to 6.8% (2025, 94 beds); 11.4% of adult-only TH beds.
  - **Among women-focused providers** (N Street Village, House of Ruth, New Endeavors, Open Arms, Calvary): Calvary holds 14–23% of adult-only ES/SH/TH beds.
  - **Calvary 2025:** TH 94 beds across five projects, PSH 16 (Sister Circle), RRH 14. Sisters Rise PSH (24) was listed in 2024 but not in 2025.
- **Program metrics:** Calvary's at-a-glance metrics, e.g. women served, nights of housing, therapy sessions, are in `clean/supp_calvary_program_metrics.csv`.

## 8. Named comparators (Calvary CEO request): include in every analysis

**Downtown Women's Center (DWC), Los Angeles (Skid Row), EIN 311597223, NTEE P83, FY = calendar year**

- **Size** (TY2024): revenue $34.4M (6.9× Calvary); expenses $28.9M; assets $49.0M. 358 employees (Calvary 85); 1,750 volunteers (Calvary 130).
- **Revenue and government share** (990 line 1e):

  | TY | Revenue | Gov share |
  |---|---|---|
  | TY2014 | $6.31M | 23.9% |
  | TY2016 | $9.18M | 32.5% |
  | TY2018 | $11.59M | 30.5% |
  | TY2020 | $14.72M | 39.7% |
  | TY2021 | $20.99M | 44.3% |
  | TY2022 | $24.11M | 56.6% |
  | TY2023 | $27.16M | 57.9% |
  | TY2024 | $34.40M | 57.0% |

  Non-government contributions fell from 64% to 37% of revenue. Program service revenue is 5–13% (rental, social enterprise).
- **Federal** (FAC FY2020–25): 99% pass-through. Top programs are CoC 14.267 ($14.3M), ESG 14.231 ($3.5M) and VOCA 16.575 ($2.7M).
- **Programs:**
  - 159 PSH units plus community-based housing; 451 people housed in 2024.
  - Skid Row's only women's health clinic (with JWCH).
  - MADE by DWC paid transitional work.
  - Rosa's Place (97 PSH units) broke ground March 2025.
- **Funders** (web; `stage_fact_grants__web_named` → `fact_grants`):
  - **Donor lists:** 2023 lists 202 organizations; 2025 lists 148.
  - **Largest 2025 band ($1M+):** GO-Biz, LA County DHS, LAHSA.
  - **Funder-announced grants:** Hilton $1.53M over two years (2026); Blue Shield of California Foundation $450K (2024); Ahmanson $325K (FY2023); Anthem Blue Cross Foundation $200K (2023) and $300K (2026).
  - **Overlap with Calvary's funders:** the DMV funder data shows 56 grants to DWC from 8 funders ($308K TY2020–25), e.g. Wells Fargo Foundation $100K and Bank of America Charitable Foundation ~$30–35K/yr.
  - **Gap:** DAF grants to DWC are not captured, because the DAF Schedule I is kept for DC/MD/VA recipients only.
- **Context:** DWC's tract 06037206202 has 41.9% poverty and $24K median household income. LA County: 13.7% poverty, 57.7% rent-burdened.

**SheWorks: a program of the California Black Women's Collective Empowerment Institute, Carson CA, EIN 882046704, founded 2022, FYE June**

- **Revenue and government share** (990):

  | TY | Revenue | Gov share |
  |---|---|---|
  | TY2022 | $1.38M | 87.7% |
  | TY2023 | $1.49M | 84.6% |
  | TY2024 | $1.84M | 69.6% |

  - Other contributions rose from $169K to $558K.
  - Size vs Calvary (TY2024): revenue 0.37×, assets 0.11×.
- **Programs** (TY2024): Black Women's Think Tank / Research and Innovation Institute ($836K), Conversations for Black Women, Protecting Black Women and Girls. It made $42.5K in grants to 8 orgs.
- **SheWorks itself:** announced 2025-10-28, so it starts after TY2024 and its money will appear in TY2025+ filings.
  - **First cohort:** about 30 women, Jan–May 2026, at the L.A. Care / Blue Shield Promise Community Resource Center in Long Beach.
  - **Support:** stipends, childcare and ride credits.
  - **Named supporters:** LA County Federation of Labor (partial funding, no amount); L.A. Care and Blue Shield of California Promise (host sites, in-kind).
  - **Federal:** no FAC reports and no USAspending awards.
- **Geography:** geocoded to its office (500 E Carson Plaza Dr; tract 06037543400). SheWorks is delivered at Community Resource Centers.

## 9. Measurement cautions

- **Government share depends on the measure.** Contracts often land in program service revenue (990 line 2) or "other contributions" (line 1f), not line 1e.
  - Calvary FY21: audit government revenue $1.98M vs line 1e $503K (line 1f $3.06M).
  - FY20: audit $1.84M vs line 1e $2.17M; the line 1e figure includes PPP.
  - State which measure is used. For Calvary, audits and SEFA are the better basis.
- **Sources overlap in `fact_gov_awards`.** It mixes awards, obligations, payments and expenditures from overlapping sources: OVSJG award lists vs PASS payments vs SEFA expenditure, and USAspending subawards vs FAC pass-through. Never sum across `source_type`; pick one source per question.
  - **USAspending vs FAC:** USAspending subawards from DC-government primes to DC-sector orgs are about 24% of the FAC DC-government pass-through figure over FY2019–24.
- **USAspending prime rows** are award totals with the base-action fiscal year; multi-year awards are not split by year.
- **990-PF filing lag:** TY2024 is partially released and TY2025 is mostly unfiled, so recent-year grant totals are incomplete. Also, a CRM gift dated 2025 may appear on a funder's TY2025 return, filed in 2026–27.
- **Thin 990-PF bulk data** for FY2016–18: no IRS 990-PF extract exists for those processing years. TY2020+ comes from XML.
- **The "dc_sector" federal program list** is dominated by DC-based international and research nonprofits (e.g., 19.800, 98.001). Filter by NTEE before ranking programs.
- **Org geography** comes from the filing address (headquarters or mailing), not service sites.
- **Unmatched recipients:** for named DC/MD/VA organizational recipients, 10.1% of grant dollars lack an EIN, mostly government units, school sub-units and churches.
