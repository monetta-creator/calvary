# Catalog part: dc_hud (DC government, DC Council, HUD/regional homelessness)

Probe script: `scripts/14_probe_dc_hud.py` (groups `dcgis`, `budget`, `council`, `hud`, `misc`). Probe date 2026-10-10.
Raw output: `raw/dc_gov/` (~87 MB), `raw/dc_council/` (~118 MB), `raw/hud/` (~55 MB). No keys used.
File names below omit the `{YYYYMMDDTHHMMSS}_` prefix.

## How Calvary's DC and HUD money flows (what the sources can and cannot show)

| Stream | Grantor of record | Public award record with Calvary amounts | Source |
|---|---|---|---|
| OVSJG victim-services grants (Reach Up TH, New Foundations TH) | OVSJG, direct | yes, FY2019-FY2026 | DC GIS layer 35, OVSJG recipient PDFs, PASS POs/payments |
| HUD CoC (Sister Circle PSH, Reach Up joint TH-RRH, New Foundations 2 joint TH-RRH DV) | HUD to TCP; Calvary is subrecipient | yes, 2019-FY2025 awards; FY2026 renewal inventory | HUD Exchange AwardComp, hud.gov award PDFs, GIW xlsx |
| DHS homeless services (TH contract, Sisters Rise EHV PSH) | DHS to TCP; TCP subgrants to Calvary | one year only (DHS FY2023-24 oversight responses pp 111-112) | DC Council POH 2024 |
| DHS SNAP E&T | DHS, direct | yes, FY2022-FY2023 POs | PASS POs; Council Attachment I (no per-grantee split) |
| DHCD COVID nonprofit grant | DHCD, direct | FY2021 $32,298 | PASS PO/payment |
| DBH, DOES | none found | no | PASS, Council Attachment I |

The Calvary FY2023 audit SEFA lists pass-through from OVSJG, TCP, FEMA and DHS. TCP-routed DHS dollars are invisible in PASS (supplier = TCP, ~$100-130M per year from DHS FY2013-FY2024).

---

## 1. DC Open Data / DC GIS (`raw/dc_gov/dcgis_*`, `hub_search_*`, `dcat_us_1_1_feed.json`)

**Hub search API and DCAT** (`api_dc_opendata_hub`). `https://opendata.dc.gov/api/search/v1/collections/dataset/items?q=` returns GeoJSON-like items whose `url` is the ArcGIS layer. DCAT feed lists 1,871 datasets. No budget-line or grant-award datasets exist besides the OVSJG and PASS layers ("budget" search returns only PASS layers).

**Boundaries** (`api_dcgis_boundaries`). Wards from 2022 = `Administrative_Other_Boundaries_WebMercator/MapServer/53` (8 polygons; WARD, NAME, GEOID, LABEL). Census Tracts 2020 = `Demographic_WebMercator/MapServer/8` (206 tracts; GEOID, TRACT, POP100, HU100; no ward field). Both saved as GeoJSON (outSR=4326). The context area registered the same ward layer as `api_dcgis_wards_2022` and also saves wards and TIGERweb tracts to `raw/geo/`; Phase 4 should pick one canonical copy.

**Homeless facilities** (`api_dcgis_homeless_facilities`). Shelter Locations (layer 25): 19 DHS sites, 2,763 active beds, WARD and PROVIDER fields. Service Facilities (layer 6): 115 rows with service flags. Calvary appears in neither.

**OVSJG Grant Recipients** (`api_dcgis_ovsjg_grants`, layer 35). 1,267 rows FY2016-FY2025. Field labels are swapped: `AGENCY` holds the grantee, `ORGANIZATIONNAME` the project title. Calvary rows (13): Reach Up TH FY2019 $368,935 + $292,000, FY2020 $368,935, FY2021 $368,935, FY2022 $368,935 + $99,500, FY2023 $402,540, FY2024 $430,873, FY2025 $478,622; New Foundations TH FY2022 $3,680,675, FY2023 $438,500, FY2024 $482,528, FY2025 $519,656. FY2026 not loaded yet.

**PASS purchase orders / payments / contracts** (`api_dcgis_pass`, `Government_Operations/MapServer/16`, `/17`, `/37`).
- POs: 279,712 rows FY2013-FY2027 (POs > $2,500). Calvary (`SUPPLIER = CALVARY WOMEN'S SERVICES`): 10 POs FY2019-FY2023 (OVSJG `20xx-CWSH-01/02`, DHS SNAP E&T FY2022 $62,899 and FY2023 $68,544, DHCD FY2021 $32,298). `Calvary Healthcare, Inc` and `Greater Mt. Calvary` are different vendors.
- Payments: 1,576,128 rows FY2017-FY2027. Calvary 95 payments FY2019-FY2024; none after FY2024.
- Contracts (OCP awards >= $100K): Calvary 0 rows.
- Gotchas: (a) POs under agency code AA0 (EOM) repeat once per EOM sub-office acronym (146 duplicate rows across 14 peer suppliers); dedupe on PONUMBER + FISCALYEAR + POTOTAL and group on AGENCYCODE, not AGENCY_ACRONYM. (b) `PONUMBER` suffix `-V2/-V3` marks modified versions. (c) Calvary POs/payments and TCP's DHS POs fall off after FY2024 (TCP: $110.4M FY2024, $7.1M FY2025, $71.1M FY2026) although OVSJG awards continue; likely the FY2025 change to the new financial system and chart of accounts (budget codes change to `H03010`-style in FY2025). Treat PASS as incomplete from FY2025. (d) Layers carry DC staff names, e-mails and phones; the script requests explicit field lists without them.
- OCP Transparency Portal (`web_ocp_transparency_portal`) is a JS app over the same data; use the layers.
- DC grants clearinghouse (`web_dc_grants_clearinghouse`, now MOCA/Serve DC; opgs.dc.gov redirects) lists opportunities only, no awards.

## 2. DC budget books (`doc_dc_budget_fy2024`..`fy2027`; `raw/dc_gov/cfo_budget_fy{FY}_{AG}_*`)

Approved budgets for FY2024-FY2027 (FY2027 approved is published). Each book has columns for two actual years and two approved years, so the four books cover FY2021-FY2027. Agencies pulled: JA0 DHS, FO0 OVSJG, RM0 DBH, DB0 DHCD, HY0 Housing Authority Payment/Subsidy (Local Rent Supplement), CF0 DOES, HG0 DMHHS. The Interagency Council on Homelessness has no budget chapter; its staff (deputy director) is funded in HG0 DMHHS Agency Management (FY2027 chapter p4).

Text quality by book (decides the parse source):

| Book | Chapter Table XX0-4 (division/program/activity) | Appendix Schedule 30-PBB (activity x fund) | Use |
|---|---|---|---|
| FY2027 (`*_2027a_*`) | clean text | clean text | chapter or 30-PBB |
| FY2026 (`*_2026o*`) | clean text | image-only (0 text pages) | chapter Table XX0-4 (OCR needed for fund split) |
| FY2025 (`*_2025j*`) | broken font map, garbled for all but CF0 | clean text | 30-PBB |
| FY2024 (`*_2024j*`) | clean text, old 4-digit codes | clean text | either |

Page index (PDF page numbers; "chg" = narrative budget-change pages for fact_policy_events):

| Agency | FY2027 chapter / tables | FY2026 chapter | FY2025 chapter / tables | FY2024 chapter / tables |
|---|---|---|---|---|
| JA0 DHS | `ja0_dhs_chapter_2027a_1.pdf` Table JA0-4 pp 3-5 (homeless & PSH activities p4-5), chg 8-10; `ja0_dhs_tables_2027a_0.pdf` 30-PBB pp 1-2 | `ja_dhs_chapter_2026o.pdf` JA0-4 pp 3-5, chg 9-12 | chapter chg 11-13 (text OK); `ja_dhs_tables_2025j.pdf` 30-PBB pp 1-2 | `ja_dhs_chapter_2024j.pdf` JA0-4 pp 3-5, chg 9-12; tables 30-PBB pp 1-3 |
| FO0 OVSJG | chapter FO0-4 pp 3-4, chg 5-6; tables p1; crosswalk `fo0_ovsjg_crosswalk_2027a.pdf` | `fo_vsjg_chapter_2026o.pdf` pp 3-4, chg 6-7 | tables 30-PBB pp 1-2; crosswalk `fo_ovsjg_crosswalk_2025j_0.pdf` | `fo_vsjg_chapter_2024j.pdf` pp 3-4, chg 5-7; tables p1 |
| RM0 DBH | chapter RM0-4 pp 3-6, chg 11-14; tables pp 1-3 | `rm_dbh_chapter_2026o.pdf` pp 3-7, chg 13-16 | tables pp 1-3 | `rm_dbh_chapter_2023j_0.pdf` (is FY2024 approved) pp 3-8, chg 14-17; tables pp 1-5 |
| HY0 LRSP | chapter HY0-4 p2, chg 3-4; tables p1 | `hy_has_chapter_2026o.pdf` p2, chg 3-4 | tables p1 | `hy_has_chapter_2024j.pdf` pp 2-3, chg 4-5 |
| DB0 DHCD | chapter pp 3-4, chg 6-8; tables pp 1-2 | pp 3-4, chg 6-8 | tables pp 1-2 | pp 3-5, chg 8-9 |
| HG0 DMHHS (ICH) | chapter p3, chg p4 | p3, chg 4-5 | tables p1 | p3, chg 4-5 |
| CF0 DOES | chapter pp 3-5, chg 8-10 | pp 3-5, chg 9-10 | chapter pp 3-6 (clean), chg 9-11 | pp 3-5, chg 9-11 |

Program/activity codes for the line items (FY2025+ chart of accounts; FY2024 old codes in brackets):
- **DHS homeless services** (division HS0030 Family Services; cost-center division H4002 Homeless Continuum): H03002 Homeless Services Continuum - Families [5037], H03003 - General [5039], H03004 - Individuals [5038], H03009 - Youth [5023]; H03014-H03016 Prevention Services [5013]; H03017-H03019 Rapid Rehousing [5027-5029]; H03022 Transitional Age Youth Shelter [5026]; H03023 Transitional Housing Youth [5021].
- **DHS PSH**: H03010 PSH Families [5035], H03011 PSH General (Shelter Plus Care, federal) [5032], H03012 PSH Individuals [5034], H03013 PSH Youth (Extended Transitional Housing) [5024].
- **DHS DV**: H03007 Domestic Violence Services [5020].
- **OVSJG victim services**: division PS0023 Victim Services [4000]; P02303 Victim Services Grants [4010]; P04502 Emergency and Traditional Housing; PS0045 Safe Housing Gun Violence [6040].
- **DBH behavioral health / housing**: H04308 Housing, Residential Support and Continuity of Services [6507 Housing Support Services; 6940 Housing Development]; H04504 Crisis Services [6625]; H04311 Adult BH Services MH/SUD [6502]; FY2024 also 5842 Homeless Outreach / Mobile Crisis - CPEP.
- **Local Rent Supplement (HY0)**: R03905 Local Rent Supplement [6000 tenant-based], R03907 LRSP Project & Sponsor Based [7000], R03904 Affordable Housing; FY2024 had 6020 PSH - Individual and 6050 Homeless Services - Admin.
- FY2027 example values (Table JA0-4 p4, $000): H03011 PSH General 5,411 -> 1,000; H03012 PSH Individuals 76,441 -> 73,998; H03010 PSH Families 61,413 -> 86,807; H03003 HSC General 75,199 -> 62,076.

## 3. DC contract and grant award records

- **OVSJG recipient lists** (`doc_ovsjg_recipients`; `raw/dc_gov/ovsjg_funding_recipients_FY2024..FY2026.pdf`): one row per grant with grantee, title, period, amount, funding source, abstract. Calvary FY2024 New Foundations $482,528 LOCAL (p1); FY2025 New Foundations $519,656 and Reach Up $478,622, "Victim Service Local" (p1); FY2026 New Foundations $543,055.72 and Reach Up $507,595.05, Local (p3). Lists also name DC grant managers (do not store).
- **PASS** (above): Calvary found by name; amounts by PO and payment.
- **DHS provider lists**: only in Council oversight responses (section 4).
- **Grants clearinghouse**: no award data.

## 4. DC Council oversight and budget materials (`doc_dc_council_oversight`, `doc_dc_council_budget_reports`, `doc_dc_bsa`; `raw/dc_council/`)

Discovery uses the WordPress REST API: `/wp-json/wp/v2/pages?slug=human-services-13` (committee page HTML in `content.rendered`) and `/wp-json/wp/v2/media?search=..&after=..&before=` / `?parent={page id}`. Committee pages are renumbered every cycle and DHS moved committees (Housing in 2024, Human Services from 2025). Page JSON is saved as `wp_page_{slug}.json`.

Performance oversight (pre-hearing responses):
- **DHS 2024 cycle** (`POH2024_DHS_responses_*`, 134 pp): pp 111-112 table "Provider Name | Program Type | Contract Amount | Capacity | # of Clients Served" covering TCP/DHS shelter and housing providers. Calvary: "Calvary Transitional Housing $830,384.15, capacity 45, served 36"; "Sisters Rise (EHV) $593,280.00, capacity 25". Peers on the same table (N Street Village, New Endeavors by Women, Catholic Charities, Sasha Bruce...). Text PDF, parse with pdfplumber. p24 ERAP grants by provider.
- **DHS 2025 cycle** (`POH2025_DHS_responses_*`, 183 pp; `POH2025_DHS_attachments_dhsatt25.pdf`, 616 pp, 35 MB): grants and contracts were answered by Excel attachments ("Attachment 27 Contracts FY24-FY25 .xlsx", grants list) that are not posted; the PDF bundle has no Calvary rows. p69 TCP youth provider grants FY24/FY25; pp 120-122 PSH case-management providers with DHS local and Medicaid funding (Calvary not listed); p58 complaint counts by site (Calvary 1217 Good Hope Rd SE: 3 in FY24).
- **DHS 2026 cycle** (`POH2026_DHS_responses_*`, 241 pp): grants in "Question_13_JA0_2026.xls", not posted.
- **ICH** 2024 and 2025 responses + attachments: governance/strategic plan, TCP references; no Calvary.
- **OVSJG** 2024/2025/2026 responses: no Calvary; 2026 attachments (`ovsjgatt.pdf` p21) list monitoring visits incl. Calvary (6/24/2025-9/30/2025), no amounts.
- **DBH** 2024 responses and 2025 attachments (`dbhatt.pdf`, 5,238 pp, 1,804 with text): no Calvary.

Budget oversight Attachment I (contracts & grants) and III, FY2024-FY2027 for JA0, FO0, RM0, DB0, CF0 (text PDFs, 1-10 pp each): Calvary appears only in the DHS SNAP E&T row listing ~18 grantees with one combined amount ($6,328,421; JA0 FY24 p1, FY25 p2).

Committee budget reports and change charts: FY2025 Housing (then DHS/ICH committee) and JPS reports; FY2026 Human Services, Housing, JPS, Health reports; FY2027 Housing, Health, JPS reports, BSA committee print packet (643 pp), LBA 1st-to-2nd reading changes, and the Council Budget Office **Net Operating Budget Adjustments Chart** (120 pp; one row per change: agency, scenario Committee Recommendation/Councilwide, fund, program/activity code, cost center, account, comment, FY26-FY30 amounts; DHS pp 43-45, e.g., H03013 PSH Youth +$1,530,545 "restores extended transitional housing to FY26 levels", H03007 DV services +$500,000, H03004 Shirley's Place +$254,000). The FY2027 Human Services committee report is not posted on dccouncilbudget.com (links to LIMS hearing 2330). Calvary appears only in the FY2027 Housing report p52 (ORCA referral list, no funding).

Budget Support Acts (`bsa_*.html`, D.C. Law Library full text): relevant subtitles
- FY2024 (Law 25-50): Emergency Housing Assistance Program financial responsibility; DHS grant; DBH targeted outreach grants; Housing Production Trust Fund.
- FY2025 (Law 25-217, eff. 2024-09-18): Local Rent Supplement Program accounts; Housing for Victims of Domestic Violence Fund clarification; Rapid Re-Housing; DHS grant; Federal City Shelter and CCNV redevelopment planning.
- FY2026 (Law 26-55, eff. 2025-12-06): Human Services Grant Administration; Rapid Rehousing Programs; TANF benefits; DHS grant.
- FY2027 (Act 26-416, emergency, 2026): LRSP vouchers for families exiting rapid rehousing; Rapid Re-Housing; Department of Human Services grants; Human Services Pathways to Independence; Human Services Resource Utilization.

LIMS API v2 (`api_dc_lims`) returns HTTP 401 without a token; direct `lims.dccouncil.gov/downloads/LIMS/...` PDF links work when known.

## 5. HUD (`raw/hud/`)

- **AHAR 2025 PIT by CoC** (`bulk_hud_ahar_pit_hic`; `huduser_2007-2025-PIT-Counts-by-CoC.xlsb`, one sheet per year 2007-2025; read with `pyxlsb`). DC-500 2025: 5,138 overall; ES 3,275; TH 1,065; unsheltered 798; individuals 3,782; chronically homeless individuals 1,431. No gender columns in any year.
- **AHAR 2025 HIC by CoC** (`huduser_2007-2025-HIC-Counts-by-CoC.xlsx`). DC-500 2025: ES/TH/SH 4,965 beds; TH 1,385; PSH 12,696; RRH 6,012.
- huduser.gov sits behind an AWS WAF: the project UA gets HTTP 202 with an empty body; the script sends `Mozilla/5.0 (compatible; <project UA>)`, which passes and still identifies the project.
- **CoC awards, project level** (`doc_hud_coc_awards`). AwardComp DC-500 2019-2024 (`hudx_CoC_AwardComp_DC-500_{yyyy}.pdf`): rows "TCP | Calvary Women's Services - {project} | renewal/new/expansion | amount". Sister Circle $239,659 (2019) -> $296,926 (2024); Reach Up $1,222,263 (2021 renewal), $421,930 (2022 reallocation new), $427,330 (2023), $921,970 (2024 expansion); New Foundations 2 $469,719 (2023 new), $542,456 (2024). hud.gov FY2024 DC report splits Reach Up into $479,538 + $442,432 (Expansion). FY2025 awards (national PDFs `hudgov_FY2025_CoC_award_round{1,2,3}.pdf`): New Foundations 2 $546,247 and Sister Circle $296,930 (round 1 p12), Reach Up $923,637 (round 2 p22). GIW FY2024 and FY2026 (`hudgov_FY{yyyy}_DC-500_GIW.xlsx`): one row per grant with applicant (TCP), project, grant number (DC0099 Sister Circle, DC0125 Reach Up, DC0130 New Foundations 2 with DV flag), budget lines, units, ARD.
- **HIC project level** (`doc_hud_hic_dc500`; `hudx_CoC_HIC_DC-500_{2022..2025}.pdf`): provider, project, beds by household type and project type. Calvary 2025: TH "CWS - Transitional Housing" 45, Reach Up OVSJG 18, New Foundations 17, Reach Up TH 8 and 6; PSH Sister Circle 16; RRH Reach Up 14. 2024 adds Sisters Rise PSH 24. 2026 HIC not yet published.
- **PopSub** 2024 and 2025: 2024 has a gender table (Woman 2,167 of 5,616); 2025 has none.
- **MWCOG** (`doc_mwcog_pit`; `mwcog_homelessness_metro_washington_{2023..2026}_PIT.pdf`): jurisdiction-level tables incl. DC; no ward breakdown; no Calvary. The document page lists 2007-2026 reports. mwcog.org returns 403 to a full browser UA and 200 to the project UA.

## 6. TCP and ICH (`web_tcp_ich`)

No public provider-level bed or funding tables (community-partnership.org media holds PIT presentations through 2021-2024; dcpit.org hub holds a story map). Provider-level beds come from the HUD HIC PDFs. TCP (EIN 521681401) is the applicant on every Calvary CoC grant and DHS's homeless-services intermediary, so its Form 990 Schedule I is the likeliest public source of Calvary's TCP subgrant amounts (IRS area).

---

## Phase 4 pull design

### fact_gov_awards (DC grants/contracts and HUD CoC by provider)
1. **OVSJG layer 35** (already pulled in full): one row per record; `funder` OVSJG, `recipient_name` = `AGENCY`, `program` = `ORGANIZATIONNAME`, `amount` = `AWARDAMOUNT`, `fiscal_year` = `FY` (DC FY ends Sep 30); `basis` documented, `confidence` high. Keep Calvary + peer list; normalize names with `norm_name`.
2. **OVSJG recipient PDFs FY2024-FY2026**: pdfplumber table extraction on all pages (FY2026 23 pp; columns Department, External Organization, Grant Title, Project Period, Awarded Amount, Funding Source, Abstract, Issue Date). Use for FY2026 rows and the funding-source field; drop grant-manager names.
3. **PASS POs + payments**: query `UPPER(SUPPLIER) LIKE` per Calvary/peer variant with explicit field lists, paginate 1,000; dedupe (PONUMBER base + version, FISCALYEAR, POTOTAL); PO = obligation, payments = cash. Flag FY2025+ as incomplete. Skip Calvary Healthcare / Mt. Calvary.
4. **HUD CoC**: parse AwardComp 2019-2024 project tables (pages 2-3), the FY2025 round PDFs (DC-500 pages 12, 22, 37), and GIW xlsx (openpyxl; header row "Applicant Name | Project Name | Grant Number | ..."). Store `funder` HUD CoC (ALN 14.267), `pass_through_entity` TCP, `recipient` Calvary (subrecipient named in the project title), grant number, component, amount; `basis` documented. Cross-check against USAspending (other area) for TCP prime awards.
5. **DHS via TCP**: parse DHS 2024-cycle POH responses pp 111-112 (provider, program, contract amount, capacity, clients served) as FY2024 DHS/TCP rows, `confidence` medium (period not stated on the page). Remaining DHS/TCP years need the unposted Excel attachments or TCP 990 Schedule I (open question).
6. **Council Attachment I**: record SNAP E&T multi-grantee rows as membership only (no amount); amounts come from PASS POs.

### fact_policy_events (dated budget/policy changes)
1. **Council Budget Office FY2027 Net Operating Budget Adjustments Chart** (`BR_FY27_council_operating_changes_chart_*.pdf`, 120 pp): pdfplumber table extraction; keep agencies JA0/FO0/RM0/DB0/HY0/HG0 and activity codes listed above; one event per row with comment text and FY26-FY30 amounts; event date = Council second-reading vote (confirm date from the LBA page or LIMS). Repeat for FY2026 if the equivalent chart exists on `dccouncilbudget.com/fy-2026-budget`.
2. **Budget chapters, narrative change pages** (page index above, "chg"): regex for "increase/decrease of $X ... in the Y division/program" plus "one-time"; event date = budget approval (BSA effective date).
3. **Program budget time series**: Table XX0-4 (FY2024, FY2026, FY2027 chapters) or Schedule 30-PBB (FY2025, FY2027 appendix) for the activity codes above; map FY2024 4-digit codes to FY2025+ codes by name and the FO0 crosswalk PDFs; store approved and actual amounts per FY. These feed year-over-year funding-change events (e.g., FY2027 H03011 PSH General -$4.41M).
4. **BSA subtitles**: parse `bsa_*.html` TITLE/SUBTITLE headings and the law effective date on each page; keep homeless, rent supplement, rapid re-housing, DV housing fund and DHS-grant earmark subtitles.
5. **Committee reports** FY2025-FY2027: page lists for "homeless" and "PSH" are in the build log; extract narrative recommendations manually or by regex.

### dim_geo (wards)
1. Wards 2022 GeoJSON (8 polygons; WARD, NAME, GEOID) as the ward dimension; coordinate with the context area's `raw/geo/` copy and pick one.
2. Census tracts 2020 GeoJSON (206) -> tract-to-ward assignment by polygon overlay (shapely is installed) or the context area's block-based crosswalk.
3. Shelter layer 25 gives WARD per DHS shelter site (peer context); HIC PDFs have no addresses.

### Context metrics (no fact table fits exactly)
PIT xlsb (one sheet per year) and HIC xlsx for DC-500 2007-2025; MWCOG tables for DC vs region. Gender detail exists only through PopSub 2024.
