# Methodology: Calvary Women's Services funding strategy

Data as of 2026-10-10. Paths are relative to the project root (the folder holding `calvary_funding_data/` and `calvary_analysis/`).

---

## 1. Purpose and scope

This pro bono engagement for **Calvary Women's Services** (Washington, DC; EIN 521307706) answers two anchor questions:

1. **Exposure:** how exposed is Calvary to government funding?
2. **Opportunity:** what other funding should it pursue first?

All figures are as of **2026-10-10**. Calvary's fiscal year ends September 30, so FY25 = October 2024 to September 2025 = tax year (TY) 2024.

This report covers the Prompt 1 data foundation, comparison groups, measures, one method note per question (A1–D3, the numbers slide footnotes cite), traceability, reruns, the memory reconciliation and limitations. Findings are not repeated; they are in `calvary_analysis/modules/`, `recommendations/` and the decks.

---

## 2. Data foundation

### 2.1 The 25 clean tables

`calvary_funding_data/clean/` holds 25 UTF-8 CSVs: 24 data tables plus `data_dictionary.csv` (542 rows: table, column, type, definition, allowed values, sources). Row counts come from `reports/data_quality.md` §1.

**Dimensions**

| Table | Grain | Rows | Notes |
|---|---|---|---|
| `dim_org` | one row per EIN | 105,189 | BMF attributes, NTEE, geography (DC ward/tract via MAR 2), mission, `universes` |
| `dim_funder` | one row per `funder_id` | 8,928 | `funder_id` = EIN, else `F` + name hash; `funder_type`, `issue_focus_tags` |
| `dim_universe_membership` | universe × EIN × rule | 17,210 | Rules in `config/universes.yaml` |
| `dim_period` | calendar year | 28 | CPI-U, 2024-dollar deflator, fiscal-year labels |
| `dim_geo` | geography | 246 | Nation to 206 DC tracts, with ACS 2020–2024 |
| `dim_program_area` | tag | 13 | Vocabulary for `program_area_tags` |
| `dim_person` | person | 48,563 | Names only, as disclosed in filings |
| `entity_aliases` | name variant | 231,647 | Variant → canonical EIN, method, score |
| `ref_ntee_codes` | NTEE code | — | IRS labels |

**Facts**

| Table | Grain | Rows | Main sources |
|---|---|---|---|
| `fact_org_financials` | org × fiscal year × source | 150,461 | E-filed 990/990-EZ/990-PF XML (TY2020+), NCCS e-file tables, IRS SOI extracts (2011+), ProPublica, Calvary's audits and 990 PDFs |
| `fact_grants` | grant or gift record | 928,658 | 990-PF grants paid and approved for future payment; Schedule I (DMV funders, DAF sponsors filtered to DC/MD/VA recipients, known Calvary funders); Calvary's CRM export; annual reports; support page; funder and peer web pages |
| `fact_gov_awards` | award / subaward / expenditure line | 40,300 | USAspending, Federal Audit Clearinghouse (FAC) SEFA, Calvary audit SEFA, Treasury SLFRF, DC OVSJG, DC Council oversight responses, DC PASS, HUD CoC |
| `fact_opportunities` | open or forecast opportunity | 286 | Grants.gov |
| `fact_policy_events` | dated budget or policy change | 297 | DC budget books FY2024–FY2027, Council budget reports, Budget Support Acts |
| `fact_roles` | person × org × filing year | 163,473 | 990 Part VII-A, 990-EZ, 990-PF officers, Calvary annual-report board lists |
| `fact_org_relationships` | org pair × type × year | 544,041 | grant, daf_sponsor_grant, pass_through_funding, schedule_r_related, shared_board_member |
| `candidate_interlocks` | person-record pair | 1,270 | Low-confidence cross-org name matches held back for manual review |

**Supplementary tables**

| Table | Rows |
|---|---|
| `supp_calvary_program_metrics` | 178 |
| `supp_calvary_strategic_targets` | 18 |
| `supp_calvary_individual_donor_bands` (counts only, no names) | 4 |
| `supp_crm_cash_verification` | 160 |
| `supp_homeless_counts` (HUD PIT/HIC by CoC) | 49,393 |
| `supp_hic_projects` (HIC beds by project and provider) | 1,257 |
| `supp_dc_budget_lines` | 5,172 |

**Counting rule.** Count rows with pandas, never `wc -l`: quoted line breaks give `entity_aliases` 231,678 lines for 231,647 rows, and `fact_gov_awards` 42,958 lines for 40,300 rows.

**Large tables.** `fact_grants` (567 MB) and `fact_org_relationships` (101 MB) are read with `usecols`.

### 2.2 Sources

`calvary_funding_data/sources/source_registry.csv` lists **238** `source_id`s. Each has a URL or file, publisher, retrieved date (all 2026-10-10) and license or citation.

**By acquisition type** (the `source_id` prefix):

| Prefix | Sources |
|---|---|
| `web_` (web pages: Calvary, peers, comparators, funders) | 156 |
| `input_` (client-provided files) | 30 |
| `api_` | 24 |
| `bulk_` | 16 |
| `doc_` (government documents) | 11 |
| `ref_` | 1 |

**By publisher type** (grouped from the `publisher` column):

| Publisher type | Sources | Publishers | Examples |
|---|---|---|---|
| Calvary (own documents, website, CRM export) | 72 | 3 | audits, 990 PDFs, annual reports, CRM |
| Funders and companies | 44 | 23 | Greater Washington Community Foundation (8), Meyer (5), Cafritz |
| Core peers (annual reports, donor lists) | 36 | 17 | Community of Hope, N Street Village |
| Federal government | 23 | 12 | Census (7), IRS, Treasury, HUD, GSA |
| DC and regional government, DC CoC | 23 | 13 | DC GIS / OCTO, OCFO, Council, OVSJG, TCP |
| Named comparators | 16 | 2 | Downtown Women's Center (11), CBWC Empowerment Institute (5) |
| Data intermediaries and tools | 13 | 7 | GivingTuesday Data Commons (5), NCCS (3), ProPublica, NODC, Charity Navigator, Tavily |
| Calvary's auditors | 8 | 3 | audit firms |
| News and press | 3 | 2 | press releases, local news |

`sources/api_catalog.md` records **65 sources probed across 4 areas**. Status counts: ok 55, ok_no_results 4, blocked_needs_key 3, not_applicable 2, failed 1. The blocked sources were Charity Navigator, the SAM.gov Entity API and the DC Council LIMS API. All three were skipped as not needed (`open_questions.md` A).

Prompt 2 added `calvary_analysis/sources/source_registry_extension.csv` (33 rows). These are the web pages found by the approved Tier 1–2 guideline pull (§5, C3).

### 2.3 Conventions

- **Years.** `tax_year` is the IRS tax year (the year the fiscal year begins). `fiscal_year` is the year it ends; `fye_month` is the month it ends.
  - Calvary: TY2024 = FY25 = Oct 2024–Sep 2025. DWC's year ends in December; the SheWorks parent's ends in June.
  - One tax year therefore mixes fiscal years ending in different months. Show `fiscal_year` + `fye_month` when timing matters.
  - ProPublica's `tax_prd_yr` is the year the fiscal year ends.
  - Government amounts state their own calendar in `fiscal_year_basis`.
- **Money.** Integer nominal USD. `*_real_2024` columns use CPI-U US annual average, base 2024.
- **One fact per row.** The same figure from different sources is kept as separate rows.
- **Preferred rows.** `fact_org_financials.preferred = 1` marks one row per org-year, ranked XML > NCCS > ProPublica > SOI > 990 PDF > audit. Derived ratios use preferred rows only.
- **Conflict flags.** `conflict_flag = 1` marks org-years whose sources disagree on revenue by more than 1%: 2.0% of org-years. Conflicts are kept and flagged, never resolved silently.
- **Cumulative rows.** `fact_grants.cumulative_flag = 1` marks amounts spanning several years: CRM totals and "supporters over the years" lists. They are never added to annual rows.
- **Provenance columns.**
  - Every row carries `source_id` (→ the registry) and `retrieved_date`.
  - `confidence` is high / medium / low.
  - `basis` is documented, derived or inferred.
  - `notes` holds `key=value` extras, such as `placeholder_row=1` for "see attached" 990-PF rows.
- **Join keys.** `ein`, `funder_id`, `person_id`, `tax_year`/`fiscal_year`, `county_fips`/`ward`/`tract_geoid`. Wards are digits `1`–`8`.
- **Funder types.** Institutional decision-makers vs `daf_sponsor` intermediaries (see §4); `corporate` = companies giving directly, named only in Calvary's or peers' lists.

### 2.4 Prompt 1 quality checks

From `reports/reviewer_guide.md` §2:

| Check | Result |
|---|---|
| Calvary's audits balance internally | 260 of 260 checks pass, across 8 audits and 6 readable 990 PDFs |
| Calvary's revenue agrees across independent sources (XML, SOI, ProPublica, NCCS, 990 PDFs) | 0 of 42 year-source rows differ by >1%. Audits differ 0–9% on revenue for a known reason (GAAP in-kind and special-event presentation); net assets match every year |
| Foundation grant lists add up to reported totals | Exact on 99.96% of 18,116 returns with grants |
| Parsed rows match the original IRS file | 20 of 20 random rows traced to the exact XML element |
| XML fetch and parse | 31,469 of 31,469 returns fetched; 0 parse errors |
| DC budget tables tie to printed totals | 257 of 257 |
| HUD CoC awards and HIC beds tie to HUD's printed totals | All years tie |
| Independent confirmations | Cafritz filing: $170,000 to Calvary (TY2024); FY22 audit vs FAC within $3,000; OVSJG awards match across DC open data and PDF lists; Graham's $200K two-year grant matches the CRM's $100K first installment |
| Duplicate keys | None |
| Portability (no local paths, usernames or keys) | Clean |
| Rebuild test | Passed 2026-10-10: two consecutive offline rebuilds reproduced 24 of 25 tables (22 byte-for-byte); `entity_aliases` differed only in displayed spelling, now fixed by a sort |

**Other checks** (`reports/data_quality.md`):
- **§4 reconciliation.** One row per Calvary fiscal year and source, FY2011–FY2025. The FY21 audit shows government revenue $1,981,161 against 990 line 1e $503,222.
- **§5 CRM verification.** Of 160 CRM funders: 25 `confirmed_in_window`, 7 `confirmed_earlier_only`, 7 `attachment_only_list`, 29 `no_filing_rows`, 92 `not_exempt_filer`.
- **§7 unmatched recipients.** For named organizational recipients in DC/MD/VA, 76,801 rows and $3,972,062,391 lack a recipient EIN (10.0% of dollars; the reviewer guide rounds this to 10.1%). "See attached" placeholder rows (667 rows, $3,497,262,549) and grants to individuals (37,472 rows, names redacted) are reported separately. Fuzzy matches: 25,134 rows (`fuzzy_name_city`).
- **§8 person matching.** 48,563 people; 2,036 linked across 2+ organizations (597 high, 1,439 medium); 1,270 low-confidence candidate pairs held back.

### 2.5 Known gaps

From `reports/data_quality.md` §9:

- 660 sector orgs have no return since TY2020 (990-N or inactive); paper filers have no XML.
- 0 of 31,483 targeted XML returns not retrieved.
- TY2024 returns are partially released; TY2025 mostly not yet filed.
- Calvary's FY22, FY24 and FY25 audits were not provided; FY22 was later found on Candid (`open_questions.md` A3).
- FAC's audit-year 2023 record repeats FY22 SEFA; the FY23 audit PDF shows $937,999 (both kept, flagged).
- USAspending shows little DC pass-through money (SLFRF, CoC via TCP, EFSP); FAC and DC sources cover it.
- DHS provider lists for 2025–2026 were not posted; TCP Schedule I is the fallback.
- Non-foundation corporate giving appears only where Calvary or a peer lists it.
- Individual donors are excluded except as counts per gift band.

---

## 3. Universes and comparison groups

### 3.1 Universes

Built by `scripts/20_build_universes.py` from the IRS EO BMF and the e-file index (releases 2021–2026); rules are in `config/universes.yaml`. Sizes are distinct EINs from `reports/universe_summary.md`. Across all universes there are 15,812 distinct EINs.

| Universe | EINs | Rules (EINs) | Definition |
|---|---|---|---|
| `calvary` | 1 | SUBJ | The subject organization |
| `named_comparators` | 2 | NC1 (2) | DWC (311597223) and the CBWC Empowerment Institute (882046704), at the CEO's request |
| `core_peers` | 18 | CP1 (18) | Provisional set in `config/core_peers.csv` |
| `dc_sector` | 1,027 | DCS1 (896), DCS2 (131) | DC public charities in core and adjacent NTEE codes (homelessness, housing, DV/victim services, human services, behavioral health, reentry, workforce, food, veterans, women's rights). DCS2 flags orgs with no return since TY2020 |
| `dmv_sector` | 4,910 | DMV1 (4,250), DMV2 (660) | Same filters across DC/MD/VA counties in the DC MSA |
| `national_women` | 2,878 | NW1 (1,118), NW2 (1,326), NW3 (8), NW4 (426) | Nationwide DV shelters (P43), women's centers (P83, added as NW4), women-named homeless/housing orgs, I71 DV orgs with housing terms |
| `size_matched` | 566 | SZ1 (566) | Nationwide L40/L41/P85/P43/P83, revenue 0.5×–2× Calvary's TY2022–24 median ($4,967,995; band $2,483,998–$9,935,990), so the TY2021 $8.87M outlier is excluded |
| `dmv_funders` | 7,705 | F1 (5,855), F2 (1,847), F3 (3) | DC/MD/VA private foundations and grantmaking public charities (NTEE T-codes), plus three pins: TCP, Washington Area Women's Foundation, America's Charities. Includes private operating foundations |
| `daf_sponsors` | 15 | DAF1 (15) | National DAF sponsors (Fidelity, Schwab, Vanguard, NPT, …), Schedule I filtered to DC/MD/VA recipients |
| `calvary_known_funders` | 88 | KF1 (68), KF2 (20) | Funders named in Calvary's CRM, reports or support page, matched to EINs. KF2 = inferred corporate foundation (low confidence) |

**Other parameters:**
- "Recent filing" = BMF TAX_PERIOD or e-filed return period ≥ 202101.
- Peer geography is CBSA 47900. Baltimore-area orgs appear only when named.

### 3.2 Provisional core peers

The 18 core peers were chosen by the Prompt 1 build lead while the engagement lead was away. They have **not been formally reviewed** and are labeled "provisional" in every output.

**Candidate search** (`reports/core_peers_proposal.md`):
- 36 named DC-area seeds, matched against the full DC/MD/VA BMF.
- A data-driven sweep: DC/DMV sector charities with revenue ≥ $750K and either a shelter/DV NTEE code or a women-focused name.
- **Score:** women focus 3, DV 2, homeless/housing 2, recovery or mental health 1, Ward 7/8 2, DC 1, size similarity up to 2 (log distance from $4.97M).
- **Relevance gate:** homeless or DV language must appear in the filing text.
- Final picks combine the score with judgment about model similarity.

| Tier | Organizations (latest revenue TY2024; line-1e government share) |
|---|---|
| 1a — DC, women-focused homelessness | N Street Village ($10.5M; 39%), House of Ruth DC ($20.0M; 45%), Open Arms Housing ($2.5M; 77%), New Endeavors by Women ($3.1M; 82%) |
| 1b — DC, DV survivors | DASH ($7.3M; 90%), My Sister's Place ($8.3M; 83%), DC SAFE ($6.9M; 94%) |
| 2 — DC homelessness and recovery at similar size, or Ward 7/8 presence | Samaritan Inns ($6.2M; 11%), Christ House ($4.9M; 35%), Everyone Home DC ($4.9M; 85%), Coalition for the Homeless ($7.5M; 92%), Thrive DC ($2.6M; 1%), Miriam's Kitchen ($13.0M; 10%), Community of Hope ($57.6M; 38%), Covenant House Washington DC ($7.3M; 56%) |
| 3 — DMV women/DV housing outside DC | Doorways for Women and Families ($6.1M; 47%), House of Ruth Maryland ($11.6M; 63%), Heartly House ($5.1M; 79%) |

**Alternates.** Thirteen, with revenue and mission, are listed in the proposal.

**Swap procedure:**
1. Edit `calvary_funding_data/config/core_peers.csv`.
2. Rerun `calvary_funding_data/scripts/20_build_universes.py`. Every candidate's 990 XML was already fetched, so no new downloads are needed.
3. Rerun the analysis scripts from `03_m3_peers.py` onward (§7).

### 3.3 Named comparators

Calvary's CEO asked on 2026-10-10 that every analysis include two organizations:

- **Downtown Women's Center (DWC), Los Angeles** (EIN 311597223; NTEE P83; fiscal year = calendar year; FY2024 revenue $34,403,997). Also in `national_women` via rule NW4.
- **SheWorks**, a workforce program of the **California Black Women's Collective Empowerment Institute** (EIN 882046704; Carson, CA; FYE June; founded 2022; ~$1.8M; no federal awards or single audit found). SheWorks is a program, not a separate entity. Filing data describe the parent institute, and program-level funders come from the web.

**Why reference rows, not peers:** both are in Los Angeles (LA County and LAHSA rather than DC and TCP); DWC (FY2024 revenue $34,403,997) operates at a much larger scale than Calvary (FY25 $4,967,995); the SheWorks parent has three years of filings and SheWorks starts after TY2024; and DAF grants to them are not captured. They appear on every peer table and chart, including DC-only views, as "(LA, reference)" in teal with a dotted outline (`storylines/design_system.md` §5).

---

## 4. Measures and definitions

**Government share.** Calvary FY13–FY23 uses the audit basis (audited government contracts and grants ÷ total revenue); Calvary FY24–FY25 and all peers use 990 Part VIII line 1e ÷ total revenue. Line 1e misses contracts booked as program service revenue: Calvary's FY21 audit shows $1,981,161 of government revenue against $503,222 on line 1e. Line 1e is trusted for FY24–25 because it equalled the audited figure in FY22 and FY23. Chart `m1_03_gov_share_two_measures` shows both measures.

**One source per government stream.** `fact_gov_awards` mixes award lists, obligations, payments and audited expenditures from overlapping sources (e.g., OVSJG awards vs PASS payments vs SEFA). Rows are **never summed across `source_type`**. Each stream uses one source (A2).

**Calendar conventions:**
- **DC fiscal year** runs October–September, the same as Calvary's, so DC FY t = Calvary FY t.
- **HUD CoC** amounts are stated by competition year. Competition year t is aligned to Calvary operating year t+1 (`coc_award_lag_years: 1` in `config/scenarios.yaml`).
- **Expenditure year.** Audited SEFA lines and FAC records are expenditures in the audited fiscal year, not awards.

**Award ceilings vs recognized revenue.** An award list gives the maximum Calvary may draw (the ceiling). Recognized revenue is what the 990 or audit books in the year. The two are compared, not substituted (A5).

**Filed grants.**
- **Included:** grants from funders' own filings, meaning 990-PF grants paid and Schedule I rows.
- **Window:** TY2020–24. TY2025 is excluded as mostly unfiled.
- **Excluded:** rows with `cumulative_flag = 1`, and the two funders in `config/landscape_exclusions.csv` for landscape work.
- **Aggregation:** by `funder_id` / EIN, never by raw name.
- **Trend window:** TY2020–23. TY2024 is "arriving."

**Institutional vs DAF.** `dim_funder.funder_type = daf_sponsor` (Fidelity, Schwab, Benevity/AOGF, NPT, Vanguard, …) marks a channel for individual donors, not a grantmaker. DAF dollars are reported separately and excluded from the pipeline. The T. Rowe Price Program is scored like a DAF.

**Real dollars.**
- CPI-U US annual average, base 2024, applied by the calendar year in which the fiscal year ends (`dim_period`).
- The DC-metro CPI (2015+) is in `dim_period` for sensitivity checks.

**Months of cash.** Cash and savings ÷ monthly expenses (a clean-table field). Comparable from FY2020.

**Resilience typology.** Three-year mean government share FY2022–24:
- government-anchored ≥65%
- mixed 35–65%
- philanthropy-led <35%

**Landscape lenses.**
- **Lens A:** grants to the 1,027 `dc_sector` organizations.
- **Lens B:** grants to DC/MD/VA recipients whose purpose text is tagged housing, DV or women.

**Landscape exclusions** (`config/landscape_exclusions.csv`):
- **Gates Foundation (562618866):** a national funder whose DC recipients are global-development and research organizations. It is in the data only because it appears in Calvary's CRM (matching gifts), and it distorts landscape totals.
- **TCP (521681401):** DC's CoC/DHS pass-through intermediary. Its Schedule I grants are public funds already counted in `fact_gov_awards`.

**Need and capacity context (M9):**
- ACS 2020–24 five-year estimates by ward from `dim_geo`. DC wards are Census state-legislative-district geographies; 90% margins of error are kept.
- HUD PIT counts for CoC DC-500, 2007–2025.
- HUD HIC 2022–2025 from `supp_hic_projects`: Calvary's TH, PSH and RRH beds and its share of DC transitional-housing beds.
- A ward map from DC Open Data boundaries, colored by poverty rate.

---

## 5. Method notes

### A1 Government share and line-1e reconciliation

**Question:** how large is government money in Calvary's revenue, and how reliable is each measure?

**Data and method:**
- Revenue, expenses, net assets and cash come from `fact_org_financials` preferred 990 rows, one per fiscal year. Five sources agree within 1%.
- Government revenue: audit basis FY13–FY23, line 1e FY24–FY25 (reasoning in §4).
- **Private contributions ex-events** = contributions total − government − line 1c events. The 990 does not split foundations from individuals, so institutional giving is measured separately from funders' filings (A3).
- Real values use the 2024-dollar deflator.

**Peers:** line 1e ÷ total revenue on preferred rows, FY2015–FY2025.

### A2 One source per stream and calendars

**Question:** which government streams fund Calvary, and how big is each?

**Data and method.** One source per stream from `fact_gov_awards`, never summed across sources:
- **OVSJG:** award lists, DC FY2019–2026.
- **HUD CoC via TCP:** award lists, competition years 2019–FY2025. Projects with TCP as applicant are stored once, as a subaward to the sponsor with TCP as pass-through.
- **DHS provider contracts via TCP:** Council oversight responses, DC FY2024 only.
- **Small federal pass-throughs (EFSP, SNAP E&T):** audited SEFA lines.
- **One-time money,** listed separately: SLFRF $3.68M, PPP $327K, HUD CPF $200K.

**Calendars:**
- DC FY = Calvary FY.
- CoC competition year t → Calvary operating year t+1.
- SEFA = expenditure in the audited year.
- The FAC "audit year 2023" record duplicates FY22. The FY23 audit PDF ($937,999) is used.

**Stream durability** (annual, renewal, at-risk) is an analyst rating (`m2_03_stream_durability`).

### A3 Filed grants to Calvary

**Question:** which institutions fund Calvary, and how concentrated is that base?

**Data and method:**
- `fact_grants` 990-PF and Schedule I rows naming Calvary, TY2020–24, non-cumulative, aggregated by funder EIN.
- The base is 138 rows from 50 funders, $4.43M (analysis plan §3).
- Concentration = each funder's share of five-year filed grants, plus a Herfindahl index (`m1_07_calvary_funder_concentration`).
- GWCF is the largest filed funder at $1,206,500 TY2020–24, under two raw spellings on EIN 237343119. Health Equity Fund is attributed to GWCF as funder of record (`config/funder_match_overrides.csv`).

**How the CRM export is used:**
- 160 funders, $10.56M cumulative.
- Treated as cumulative over an unconfirmed 2023–2026 window (assumption A1).
- Gifts assumed to be cash unless contradicted (A2).
- Each CRM funder is checked against its own filings in `supp_crm_cash_verification`.
- CRM amounts are never added to filed annual grants.

### A4 Scenario construction and parameters

**Question:** what happens to revenue, deficit and cash if government streams are cut?

**Data and method:**
- **Baseline:** FY25 recognized government revenue ($2.89M) is apportioned to streams by ceiling share: OVSJG 23%, CoC 41%, DHS 33%, other 2%.
- Each scenario applies its cuts to those stream amounts.
- The **gross** view is the revenue loss.
- The **net** view assumes a share of a lost stream's revenue disappears as avoidable program cost.
- Outputs: revenue loss, deficit and months of cash after a year (`m2_07_scenarios`; parameters echoed in `m2_07_scenario_parameters`).

**Parameters** (`config/scenarios.yaml`):

| Parameter | Value | Meaning |
|---|---|---|
| `baseline_fiscal_year` | 2025 | Calvary FY (Oct 2024–Sep 2025), latest 990 |
| `cost_avoidance_share` | 0.5 | Share of a lost stream's revenue that disappears as avoidable program cost (net view) |
| `dhs_assumed_flat_from_fy2024` | true | DHS/TCP contract values are public for DC FY2024 only and are carried forward unchanged |
| `coc_award_lag_years` | 1 | HUD CoC competition year t funds Calvary's operating year t+1 |

| ID | Scenario | Cuts | Rationale |
|---|---|---|---|
| S1 | OVSJG grants cut 10% | ovsjg 0.10 | Mayor's FY2026 proposal cut Victim Services grants 10.4% ($5.8M of $55.9M) before the Council restored it |
| S2 | OVSJG grants cut 25% | ovsjg 0.25 | A deeper local cut in a revenue downturn, comparable to the FY2024 under-spend against approved (9%) plus a proposed cut |
| S3 | HUD CoC renewals cut 15% | coc 0.15 | Federal CoC renewal pressure; TCP reallocation reduced Calvary's Reach Up award 65% in 2022 |
| S4 | One CoC project lost (New Foundations 2) | coc_project_new_foundations_2 1.0 | A single project not renewed in the annual competition |
| S5 | DHS/TCP contract not renewed | dhs 1.0 | DHS contracts via TCP are annual; provider amounts are public for one year only |
| S6 | Combined (OVSJG −25%, CoC −15%, DHS lost) | ovsjg 0.25, coc 0.15, dhs 1.0 | Worst plausible case across all three channels in one year |

The scenario levels were set by the CP1 ruling: OVSJG −10%/−25%; CoC −15% or loss of one project; DHS non-renewal; combined worst case.

### A5 Award ceilings aligned to Calvary FY

**Question:** does Calvary recognize the government money it is awarded?

**Data and method:**
- Award ceilings come from the A2 sources, aligned to Calvary's fiscal year: DC FY = Calvary FY, CoC lagged one year, DHS FY2024 carried forward.
- They are compared with recognized government revenue (990 line 1e) in `m2_02_ceilings_vs_recognized`.
- The result is discovery flag D1: FY24 ceilings $3.6M vs $2.62M recognized; FY25 $4.3M vs $2.89M. The flag was approved at CP2 as a medium-confidence finding labeled "ceilings vs recognized."
- Possible explanations: undrawn awards, timing, cost-reimbursement limits, or an overstated DHS carry-forward. The data cannot distinguish them.

### A6 DC budget lines and policy events

**Question:** are the DC pools Calvary draws on growing or shrinking, and when are they cut?

**Data and method:**
- **`supp_dc_budget_lines`** (5,172 rows): activity-level totals from the DC Approved Budget and Financial Plan books FY2024–FY2027, approved vs actual vs Mayor's proposal. Each book carries two years of actuals and two approved years.
- **`fact_policy_events`** (297 rows): dated changes from the budget books, Council committee budget reports and Council Budget Office change charts, and the Budget Support Acts FY2024–FY2027.
- Committee recommendations the Council did not enact stay as `budget_proposed`.
- Budget tables tie to printed totals (257 of 257).
- **Lines tracked:** OVSJG Victim Services grants, the DHS homeless-services continuum and local PSH, alongside DCHA, DBH, DHCD and DOES.
- **Pool shares:** Calvary's share of the OVSJG and CoC award pools (`m2_05_pool_shares`).
- **Timeline:** policy events plotted against Calvary's streams (`m2_06_policy_timeline`).

### B1 Peer metrics, three-year means, real growth

**Question:** how does Calvary compare with its peers on mix, size, growth and liquidity?

**Data and method:**
- Preferred 990 rows FY2015–FY2025 for Calvary, the 18 provisional peers and the two named comparators.
- **Government share:** line 1e ÷ total revenue (Calvary FY≤2023 on the audit basis). Three-year means (FY2022–24) smooth single-year reporting breaks, for example Coalition for the Homeless FY23 and Samaritan Inns FY24.
- **Real growth:** CAGR of 2024-dollar revenue FY2019→FY2024. The endpoints avoid Calvary's one-time FY22 award.
- **Months of cash:** as defined in §4.
- **Resilience typology:** thresholds in §4.
- **Sector distributions:** `dc_sector` FY2023 (n=163), `size_matched` FY2022 (n=334), `national_women` FY2022 (n=542), with Calvary's percentile. These years were chosen for filing coverage; the national universes collapse to under 15 filers after FY2022.

**Output:** `m3_00_benchmark_table`.

### B2 Institutional funder base and DAF share

**Question:** how deep is each organization's institutional funder base?

**Data and method:**
- **Funder base:** 990-PF and Schedule I rows naming each organization, TY2020–24, non-cumulative.
- **Split:** institutional vs DAF via `dim_funder.funder_type`.
- **Measures:** institutional-funder count, DAF share, and depth = institutional dollars ÷ FY2020–24 revenue.
- **Coverage limit:** only DMV funders' filings are present, so the LA comparators' local funders are not captured. Diversifier case studies use line-1e mix trajectories (`m3_08_case_studies_mix`).

### B3 Comparator profiles and source limits

**Question:** what can Calvary learn from DWC and SheWorks?

**Data and method** (`scripts/10_m10_profiles.py`):
- **Financials:** trajectory, mix and months of cash from preferred 990 rows (line 1e for government).
- **DWC federal programs:** FAC single-audit SEFA FY2020–25 (`m10_02_dwc_federal_programs`).
- **Funder evidence:** DWC donor lists and gala pages (2023, 2025), funders' press releases and announced grants, and DMV funders' filings.
- **SheWorks:** program evidence from the parent's and partners' web pages.
- Each profile closes with "what transfers to Calvary."

**Source limits:**
- DWC's fiscal year is the calendar year.
- Line 1e is the only government measure for both; there are no audits beyond DWC's single audits.
- LA-area funders are only partly captured: web lists carry no amounts, and only DMV funders' filings are present.
- The CBWC Institute has three filings, and SheWorks launched after the last one.

### C1 Landscape lenses, exclusions and gap categories

**Question:** who funds Calvary's space, and which of those funders do not yet fund Calvary?

**Landscape (M4):**
- **Base:** filed grants TY2020–24, non-cumulative, with landscape exclusions applied.
- **Lenses:** A and B as defined in §4.
- **DAF sponsors** are reported separately.
- **Institutional landscape table** (`m4_00_funder_landscape_table`): one row per funder with dollars, recipients, years active, grant-size quantiles, mission-tagged dollars, Calvary and peer funding, "see attached" years, DMV/DC share.

**Gap categories (M5):**
- "Funds Calvary" = any filed grant naming Calvary TY2020–24.
- "Itemized TY2023+" = the funder filed itemized lists in TY2023 or TY2024, so a missing Calvary grant is current, not filing lag.
- "See attached" filers are flagged.

| Code | Definition |
|---|---|
| G1 | Institutional funders of ≥2 core peers with no Calvary grant |
| G2 | Lapsed Calvary funders (last grant ≤TY2022, funder itemized since) |
| G3 | Current funders whose largest grant to a core peer exceeds their largest to Calvary |
| G4 | Institutional funders giving ≥$500K to the DC sector with no Calvary grant |
| G5 | Funders on ≥2 peer donor lists (web) but on no Calvary list or filing |
| CRM | Reconciliation from `supp_crm_cash_verification` |

**Output:** the candidate base for scoring is `m5_00_candidate_funders`.

### C2 Network construction, interlock confidence and path strength

**Question:** which funders sit closest to Calvary's network, and are there board links to them?

**Network:**
- **Graph:** bipartite, funders × 19 recipients (Calvary + 18 provisional peers).
- **Edges:** filed grants TY2020–24 with exclusions applied.
- **Measures:** degree = organizations funded; betweenness on the unweighted graph.
- **Co-funding overlap per peer:** shared institutional funders with Calvary (DAF sponsors excluded), Jaccard similarity, and the peer's institutional funders that do not fund Calvary.

**Interlock confidence:**
- Board interlocks come from `fact_org_relationships` (`shared_board_member`), restricted to links touching Calvary, a peer or a named comparator.
- Prompt 1 linked person records only on an exact normalized name plus a corroborating signal (same metro, overlapping years, matching middle initial or suffix).
- **CP1 ruling:** leadership materials use high-confidence links only. Medium links are labeled "unconfirmed" and go to consulting materials, alongside the low-confidence `candidate_interlocks`.
- Analysis outputs store `person_id` only, never names.

**Path strength (0–1) per candidate funder:**

| Component | Weight | Cap |
|---|---|---|
| Peers funded | 0.40 | 12 |
| Close peers funded (peers sharing ≥5 institutional funders with Calvary) | 0.25 | 8 |
| Calvary's current institutional funders whose grantee sets overlap the candidate's by ≥2 | 0.25 | 20 |
| Any high-confidence board link | 0.10 | — |

The consulting variant adds 0.05 for a medium link. **Output:** `m6_05_relationship_paths`.

### C3 Pipeline scoring, tiers and the web pull

**Question:** which funders should Calvary pursue first?

**Candidate base:**
- The M5 candidates (current funders with headroom, lapsed funders, peer-funder gaps, DC-sector majors), joined to M6 paths and the M4 landscape.
- DAF sponsors are excluded. The T. Rowe Price Program (311709466) is scored like a DAF.

**Weights** (`config/scoring_weights.yaml`):

| Dimension | Weight | Scoring (0–1) |
|---|---|---|
| Mission fit | 0.20 | Issue tags (housing/DV/women 1.0; behavioral health/workforce/health 0.7; general operating 0.6) plus the share of DC-sector dollars whose purpose names housing/DV/women |
| Peer giving | 0.20 | Core peers funded TY2020–24; reaches 1 at 8 peers (`peer_giving_cap`) |
| Regional giving | 0.10 | Dollars to DC-sector orgs, log-linear $50,000 → $10,000,000 |
| Award size | 0.15 | Median grant to peers (else median DC-sector grant), log-linear $5,000 → $250,000 |
| Accessibility | 0.10 | By funder type (table below); −0.15 `placeholder_penalty` for "see attached" filers; −0.30 `in_kind_penalty` for in-kind or workplace channels |
| Durability | 0.10 | Years funding peers and years active in the DC sector |
| Relationship | 0.15 | M6 path strength + `relationship_bonus`: current funder 0.35, lapsed 0.20, on Calvary's list or CRM 0.15 |

**Accessibility scores:** community foundation 0.85; public charity grantmaker 0.75; federated giving 0.70; private foundation broad (≥20 DC-sector recipients) 0.70, mid (8–19) 0.50, narrow (<8) 0.30; corporate foundation 0.55; other 0.40; DAF sponsor 0.15.

**Channels penalized:**
- In-kind: Gifts for the Homeless, Capital Area Food Bank, America's Charities, Give Lively (`in_kind_channels`).
- DAF-like: T. Rowe Price Program (`daf_like_channels`).

**Tier rules:**
- **Tier 1:** score ≥ 0.62 **and** median grant to peers ≥ $25,000, at most 20 funders.
- **Tier 2:** score ≥ 0.48.
- **Tier 3:** the rest.

**Analyst-scored rows** (basis = inferred). These are government rows from `government_rows`:

| ID | Row | Score | Tier |
|---|---|---|---|
| GOV-DC-1 | OVSJG Victim Services grants | 0.80 | 1 |
| GOV-FED-1 | HUD CoC via TCP | 0.78 | 1 |
| GOV-DC-2 | DHS via TCP | 0.72 | 1 |
| GOV-DC-3 | DHS local PSH | 0.55 | 2 |
| GOV-FED-2 | HUD Community Project Funding renewal | 0.45 | 2 |

Corporate CRM relationships (≥$50K, no public filing) are also analyst-scored. Federal Grants.gov notices default to Tier 3. **Output:** `m7_00_funder_pipeline` (182 rows).

**Web pull (approved at CP1, run in Phase 3):**
1. `scripts/11_web_tier1_guidelines.py` searched Tavily for application process and deadlines for 32 Tier 1–2 institutional funders.
   - It returned 128 hits, saved in `sources/web_tier1_guidelines.csv`.
   - Sources were added to `sources/source_registry_extension.csv` (33 rows on disk; the run log records 32).
   - The API key is read from the environment and never written to disk.
2. Hits were hand-reviewed into `config/guideline_notes.csv`.
   - Columns: `funder_id, funder_name, application_process, next_deadline_or_cycle, guidelines_url, basis, note`.
   - 27 rows by basis: **web (first-party)** 13, **web (third-party)** 7, **no usable hit; analyst note** 7.
   - Third-party pages and misdirected top hits were not trusted as first-party guidelines.
3. `scripts/12_merge_guidelines.py` merges the notes into the pipeline and the 90-day plan (`m7_04_guideline_notes`, `m7_01_action_plan_90day`).

**Sensitivity:** `scripts/13_m7_sensitivity.py` tests how Tier 1–2 membership and ranks move when each weight shifts ±0.05 (renormalized) and each tier cutoff ±0.05 (`m7_05_sensitivity`: rank shift in the top 30, top-10 overlap, Tier 1–2 additions and drops). It covers institutional rows only; government, corporate and federal rows carry fixed analyst scores.

### D1 Expansion scan tags and distance ratings

**Question:** which adjacent program areas would open new funding pools, and how far are they from what Calvary runs today?

**Data and method.** For each tag in `dim_program_area`, M8 measures:
- DMV institutional grant dollars TY2020–24 whose purpose text carries the tag (DAF sponsors and exclusions removed)
- funders active, funders at $100K+, and median grant
- federal Grants.gov notices, after dropping research, tribal, rural and overseas notices and keeping HUD, VA, DOL, DOJ, ACF, SAMHSA, USDA, Treasury and ACL
- DC policy events
- peer and comparator examples

**Distance ratings** (`config/expansion_areas.yaml`): core; near = already delivered in some form; medium = same clients, new capability or credential; far = new population or licensing.

Ratings: housing core; DV, behavioral health, workforce and education near; physical health, aging, women veterans and reentry medium; maternal and family health far. The YAML records Calvary's current footprint and peer examples for each area.

**Output:** `m8_01_expansion_scan`.

### D2 Universes and the provisional peer set

Universe rules and sizes are in §3.1, and peer selection and swapping in §3.2.

**Effects on the analysis:**
- Every peer-dependent output moves if the peer set changes: B1–B2 benchmarks, C1 gap categories G1 and G3, C2 network and path strength, and C3 peer-giving and relationship scores.
- For that reason, every chart and table carries the label "core peers provisional."
- `size_matched` and `national_women` benchmarks use FY2022 and `dc_sector` uses FY2023, because filing coverage collapses afterwards.

### D3 Limitations and what would close them

The consolidated list is in §9.

**Discovery flags** (`discoveries_log.md`), all approved as proposed at CP2:

| Flag | Finding | Handling |
|---|---|---|
| D1 | Calvary recognized ~67–73% of known government award ceilings in FY24–FY25 (ceilings $3.6M / $4.3M vs line 1e $2.62M / $2.89M). Line 1e matched audits exactly in FY22–23 | Medium confidence, labeled "ceilings vs recognized"; FY24/FY25 audits and TCP subgrant agreements go to the top of the questions for Calvary |
| D2 | Sisters Rise (24-unit PSH with Emergency Housing Vouchers; $593K DHS/TCP contract in FY2024) is absent from the 2025 HIC | DHS stream rated "at risk"; FY2024 value kept in the baseline until Calvary confirms |
| D3 | Event contributions fell from $538K (FY24) to $55K (FY25) while net special-event income turned positive (+$219K) | Reported as the largest single swing; ask whether the FY25 gala moved across the fiscal-year line |

**Documents requested from Calvary:**
1. **FY24 and FY25 audits,** including any single audits. Closes the audit-basis government share for FY24–25 and flag D1.
2. **TCP subgrant agreements FY2023–FY2026.** Closes the DHS/TCP stream, which is public for one year only, and flags D1 and D2. The alternative is the unposted DHS attachments ("Attachment 27 Contracts FY24-FY25"; "Question_13_JA0_2026.xls").
3. **CRM export definitions.** Is GIFT_TOTAL limited to 2023–2026 or lifetime? Is it by gift date or fiscal year? What is the in-kind, pro bono or matching share of MGAC's $712,730 and Capital One's $367,340? Closes assumptions A1 and A2.
4. **Sisters Rise / EHV status in FY25.** Closes flag D2.
5. **FY25 gala timing.** Closes flag D3.
6. **SheWorks program-level budget and funders.**

---

## 6. Traceability

**The chain:** each figure traces chart → chart data CSV → clean table → source registry.

1. **Chart.** Every PNG in `calvary_analysis/charts/` (45 files) and every deck chart carries a chart ID.
2. **Chart data.** Each chart ID has a CSV in `calvary_analysis/chart_data/` with the plotted values and provenance columns (`source_tables`, `source_ids`). Scripts write these through `save_chart_data()` in `scripts/lib/common.py`.
3. **Clean table.** `source_tables` names the tables in `calvary_funding_data/clean/`. Each clean row carries its own `source_id` and `retrieved_date`.
4. **Registry.** `source_ids` resolve to `calvary_funding_data/sources/source_registry.csv` (238 rows) or, for the web pull, to `calvary_analysis/sources/source_registry_extension.csv`.

**The manifest.** `chart_data/_manifest.csv` has one row per chart-data CSV (60 rows). Columns: `chart_id, title, source_tables, source_ids, script, rows, notes, written`.

**`config/png_data_map.csv`.** Some PNGs draw on a differently named CSV, usually a shared table. The map lists those 12 PNGs and the CSV(s) behind each. For example, `m3_01_gov_share_ranked` through `m3_06_institutional_base` read `m3_00_benchmark_table`, and `m6_03_network` reads `m6_03_network_nodes` and `m6_01_central_funders`.

**`scripts/lib/trace.py` checks four things.** Run it with `python scripts/lib/trace.py`; it exits 1 on any failure.
1. Every manifest row has a CSV in `chart_data/`, and every chart-data CSV has a manifest row.
2. Every `source_id` in the manifest exists in the source registry or its extension.
3. Every PNG has a CSV with the same ID or a mapping in `config/png_data_map.csv` whose CSVs exist.
4. Every chart ID referenced in markdown under `modules/`, `storylines/`, `reports/`, `recommendations/` and `checkpoints/`, and in `insight_register.csv` (`chart_ids`), exists as a CSV or PNG. IDs are found by the pattern `m<module>_<two digits>_<name>`.

It prints counts and "TRACE OK" or the problems. This report is inside its scope; the run after writing it returned TRACE OK.

**Sourcing rule for slides** (`storylines/design_system.md` §4, engagement lead, 2026-10-10). Every slide that shows a number, chart or table carries a footnote block (9 pt, muted, bottom-left, up to three lines):
1. **Source:** the original publisher(s) and document(s), then the clean table(s).
2. **Method:** the measure and any transformation in one clause, with assumptions named (e.g., "CoC competition year t aligned to Calvary FY t+1").
3. **Trace:** chart ID, "data as of 2026-10-10" and the method note number (e.g., `Chart m2_02 · data as of 2026-10-10 · method note A3`).

Longer methods go in a numbered method note in the deck's "Data and methods" appendix (full notes in the consulting and appendix decks; short footnotes in the leadership deck). Reports use end-of-section source notes. The numbers in §5 are the ones footnotes cite.

---

## 7. Reproducibility

**Environment:**
- Python 3.12 in `calvary_funding_data/.venv` (pandas 3.0.6).
- Analysis packages are pinned in `calvary_analysis/requirements.txt`, including pandas 3.0.6, matplotlib 3.11.2, networkx 3.7, python-pptx 1.0.2, pyyaml 6.0.3, shapely 2.2.0, markitdown 0.1.8 and tavily-python 0.8.5.
- Install the same way as the data build:

```sh
uv pip install --python calvary_funding_data/.venv/bin/python -r calvary_analysis/requirements.txt
```

Scripts read only from `calvary_funding_data/clean/` (and `raw/geo` for the ward map). They resolve paths from their own location, so they run from any working directory.

**Script order** (`calvary_analysis/scripts/`):

| Script | Does | Reads config |
|---|---|---|
| `00_env_check.py` | Loads clean tables, checks row counts and reviewer-guide self-checks, confirms packages | — |
| `01_m1_trajectory.py` | M1 Calvary trajectory | — |
| `02_m2_exposure.py` | M2 streams, ceilings, DC budget, scenarios | `scenarios.yaml` |
| `03_m3_peers.py` | M3 peer benchmarking | core peers (via `dim_universe_membership`) |
| `04_m4_landscape.py` | M4 funder landscape | `landscape_exclusions.csv` |
| `05_m5_gaps.py` | M5 gap categories, candidate base | `landscape_exclusions.csv` |
| `06_m6_network.py` | M6 network, interlocks, path scores | `landscape_exclusions.csv` |
| `07_m7_pipeline.py` | M7 scoring, tiers, 90-day plan | `scoring_weights.yaml` |
| `08_m8_expansion.py` | M8 expansion scan | `expansion_areas.yaml` |
| `09_m9_need_capacity.py` | M9 need and capacity | — |
| `10_m10_profiles.py` | M10 comparator profiles | — |
| `11_web_tier1_guidelines.py` | Tavily guideline pull (network; needs `TAVILY_API_KEY`) | — |
| `12_merge_guidelines.py` | Merges hand-reviewed guideline notes into the pipeline and plan | `guideline_notes.csv` |
| `13_m7_sensitivity.py` | Weight and cutoff sensitivity for M7 | `scoring_weights.yaml` |
| `lib/trace.py` | Trace test (§6) | `png_data_map.csv` |

**How to rerun:**
1. Run `00` to confirm the environment.
2. Run `01`–`10`, then `12` and `13`, then `lib/trace.py`. All use `calvary_funding_data/.venv/bin/python`.
3. Skip `11` on a rerun. Its output (`sources/web_tier1_guidelines.csv`) and the registry extension are kept, and rerunning it needs the network and a key.
4. Each script appends a section to `analysis_log.md` and rewrites its chart data, manifest rows and insight-register rows.

**What to edit for each change:**

| To change | Edit | Then rerun |
|---|---|---|
| Core peers | `calvary_funding_data/config/core_peers.csv` | `calvary_funding_data/scripts/20_build_universes.py`, then analysis `03`–`07`, `12`, `13` |
| Scenarios | `calvary_analysis/config/scenarios.yaml` | `02` |
| Scoring weights or tiers | `calvary_analysis/config/scoring_weights.yaml` | `07`, `12`, `13` |
| Landscape exclusions | `calvary_analysis/config/landscape_exclusions.csv` | `04`–`07`, `12`, `13` |
| Expansion areas or distances | `calvary_analysis/config/expansion_areas.yaml` | `08` |
| Guideline notes | `calvary_analysis/config/guideline_notes.csv` | `12` |

Rebuilding `clean/` itself is covered in `calvary_funding_data/README.md` ("Rebuild").

---

## 8. Memory reconciliation summary

On 2026-10-10 (CP1), project memory was compared with the project files (`memory_reconciliation.md`). The project files are the working source of truth. No item was rated High, so nothing blocked the analysis.

Agreements checked with no difference include FY25 revenue $4,967,995, the FY21 audit-vs-1e figures, GWCF $1,206,500, the 18 peers, the two comparators, 88 known funders, the large-table row counts and the DAF DC/MD/VA filter.

| # | Item | Memory said | Files show | Severity | Ruling (2026-10-10) |
|---|---|---|---|---|---|
| 1 | "See attached" placeholder grants | 476 returns, $3.2B (same in README, reviewer guide, notes) | `data_quality.md` §7 and `fact_grants`: 667 rows, $3,497,262,549; 627 funder-tax-years, 180 funders | Medium (landscape totals, not Calvary figures) | Approved: use $3.5B / 627 funder-years; Prompt 1 docs untouched |
| 2 | `fact_grants` size | ~930K rows | 928,658 | Low | Approved (rounding) |
| 3 | `entity_aliases` row count | Not in memory; QC lists 231,647 and 231,678 | 231,647 parsed rows; 31 quoted names contain line breaks | Low | Approved: use 231,647; count with pandas, never `wc -l` |
| 4 | Grant depth | TY2020–TY2025 | Funder tax years 2012–2025; pre-2020 from NCCS/SOI, thinner | Low | Approved: TY2020–24 is the complete window; pre-2020 only for long trends with a caveat |
| 5 | Funder naming | One GWCF at $1.21M | Two raw spellings under EIN 237343119 ($748,500 + $458,000); same for Schwab, Vanguard, Gates, Schattner | Low | Approved: aggregate on `funder_id` / EIN, never raw name |
| 6 | Machine | Different machine in original brief | `raw/` present (7.0 GB): same machine | Low | Approved: no action |
| 7 | Core peers | Provisional, never formally reviewed | Same statement in README, open questions, proposal | — (pending decision) | Approved: keep the 18 as provisional; swap via `config/core_peers.csv` + rerun |
| 8 | Named comparators in universes | DWC also in `national_women` via NW4 | 311597223 = `named_comparators;national_women`; 882046704 = `named_comparators` only | — (consistent) | Approved: no action |

Related CP1 rulings: medium interlocks in consulting materials only, labeled "unconfirmed"; Tier 1 web pull approved; stress-test levels as in A4.

---

## 9. Limitations

Consolidated from the module readouts' Caveats sections and the Prompt 1 reports. Duplicates are merged.

| # | Limitation | Mitigation used |
|---|---|---|
| 1 | No FY24/FY25 audits are public; those years rest on the 990 | Line 1e used for FY24–25 because it matched audits exactly in FY22–23; audits requested from Calvary (D3) |
| 2 | 990 line 1e understates government money where contracts are booked as program revenue (Calvary FY21; possibly Samaritan Inns FY24–25, whose program-service revenue rose at the same time) | Calvary on the audit basis through FY23; both measures shown; three-year means for peers; reporting breaks flagged |
| 3 | DHS/TCP amounts are public for FY2024 only; other years are unknown, not zero | FY2024 carried forward as a config assumption; stream rated "at risk"; TCP agreements requested |
| 4 | HUD CoC amounts are competition years; the one-year lag to Calvary's operating year is an assumption | Lag set in `scenarios.yaml` and named in footnotes |
| 5 | Scenario stream shares are apportioned from award ceilings, not from Calvary's ledger | Shares published in `m2_07_scenario_parameters`; ceilings vs recognized gap reported as flag D1 at medium confidence |
| 6 | Federal policy risk (2025 CoC NOFO, EHV sunset) is only partly in the data | Treated as external context in durability ratings, not modeled |
| 7 | Government award sources overlap (awards, payments, SEFA) | One source per stream, never summed across `source_type` |
| 8 | Funder tax years don't align with Calvary's fiscal year; TY2024 is partial and TY2025 mostly unfiled, so "flat" after TY2023 is partly filing lag | TY2020–23 as the trend window, TY2024 labeled "arriving", TY2025 excluded; "itemized TY2023+" test in M5 |
| 9 | The 990 cannot split individuals from foundations in private contributions | Institutional giving measured from funders' own filings instead |
| 10 | CRM export is cumulative over an unconfirmed window, institutional only, cash vs in-kind unknown | `cumulative_flag=1`, never added to annual rows; each funder checked against its filings (`supp_crm_cash_verification`); questions sent to Calvary |
| 11 | "See attached" filers (667 rows, $3,497,262,549; 627 funder-years) have no recipient names, under-counting some DC funders (Philip L. Graham, Clark-Winchcole, Bank of America in some years) | Reported separately; flagged in the landscape table; −0.15 accessibility penalty; CRM used to confirm relationships |
| 12 | Corporate giving without a foundation vehicle is invisible in filings | Corporate CRM relationships scored as a separate, analyst-scored track |
| 13 | Funder-base, landscape and network metrics cover DMV funders' filings only; DAF Schedule I kept for DC/MD/VA recipients | LA comparators' funders taken from web lists and press; DWC/SheWorks shown as reference rows, not benchmarks |
| 14 | 10.0% of DC/MD/VA named-recipient grant dollars have no recipient EIN (government units, schools, churches) | Match method and score kept on every row; unmatched mass reported in `data_quality.md` §7 |
| 15 | Sector universe includes DC-based national and research organizations | Gates and TCP excluded via `landscape_exclusions.csv`; a few research recipients remain and are noted |
| 16 | Core peers are provisional; benchmarks, gap list, network and pipeline move with them | Labeled provisional everywhere; swap is a config edit plus rerun (§3.2) |
| 17 | A filing "gap" may be a gift routed through a DAF, corporate match or fiscal sponsor | Check the CRM before outreach; CRM status feeds the relationship score |
| 18 | Peer donor lists are undated and amount-less, and only six peers publish them | Used only for gap category G5 and as supporting evidence |
| 19 | Several high-count gap funders are in-kind or workplace-giving channels (Gifts for the Homeless, Capital Area Food Bank, America's Charities, Give Lively) | −0.30 in-kind penalty; penalized, not removed |
| 20 | Interlocks depend on name matching; a medium match may be two different people | High-confidence only in leadership materials; medium labeled "unconfirmed"; treated as leads |
| 21 | Path weights, pipeline weights, government and corporate scores, durability and distance ratings are analyst judgment | All weights in YAML; government rows marked basis = inferred; sensitivity script `13`; readouts state "judgment" |
| 22 | Pipeline scores rank evidence, not fit with funder guidelines | Phase 3 web pull on Tier 1–2 guidelines; notes merged into the pipeline and 90-day plan |
| 23 | Web-pull top hits were sometimes third-party or unrelated pages, and one registry-extension row (`web_guidelines_526037034`) has a truncated `url_or_file` value | Every hit hand-reviewed; `basis` column separates first-party (13), third-party (7) and no usable hit (7) |
| 24 | Expansion-scan tagged dollars understate what funders would give (general operating excluded); federal notices are a snapshot | Read as relative pool sizes; distance ratings stated as judgment |
| 25 | Need data: ward-level ACS has wide margins of error; HIC counts beds, not people, and Calvary's projects were re-labelled in 2024; HUD's PIT workbook has no gender breakdown | 90% MOEs kept, no tract figures; bed shares only, re-labelling noted in M9; CoC's 2024 subpopulation table used (2,167 women among 5,616 people) |
| 26 | Named comparators: DWC's fiscal year is the calendar year; the CBWC Institute has three filings and SheWorks starts after TY2024 | `fiscal_year` + `fye_month` shown; medium confidence on the SheWorks parent; SheWorks budget requested |
| 27 | FAC's "audit year 2023" record for Calvary repeats FY22 amounts | Both kept and flagged; FY23 audit PDF ($937,999) used |
| 28 | 660 sector orgs have no return since TY2020; paper filers have no XML; national universes fall below 15 filers after FY2022 | Flagged by rule DCS2; SOI/ProPublica where present; FY2022 benchmark year nationally, FY2023 for DC |
| 29 | Grants.gov feed is mostly irrelevant to Calvary (NIH, NSF, embassies) | Filtered by agency and topic; federal notices Tier 3 by default |
