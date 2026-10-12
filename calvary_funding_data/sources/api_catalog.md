# API and data source catalog

Merged 2026-10-10 from `sources/catalog_parts/` by `scripts/19_merge_catalog.py`. 65 sources probed across 4 areas. Status counts: blocked_needs_key 3, failed 1, not_applicable 2, ok 55, ok_no_results 4.

Keys are read from environment variables only (names in `auth_env_var`); sample requests show `$VAR` placeholders, never values.

## Status summary

| Area | Source | Auth | Status | Years covered |
|---|---|---|---|---|
| filings | ProPublica Nonprofit Explorer API v2 | no | ok | Calvary: financial data tax_prd 201109-202309 (TY2010-TY2022 |
| filings | GivingTuesday 990 API: efilexml | no | ok | Calvary TY2014-TY2020 (7 XMLs); IndexedOn max 2023-11-19 |
| filings | GivingTuesday 990 API: 990basic120fields | no | ok | Calvary TY2014-TY2021 (8 rows) |
| filings | GivingTuesday 990 API: bmf, postcard, pub78-deductible, revoked | no | ok | bmf Date_Released 2024_02_13 (tax_period 202209 for Calvary) |
| filings | GivingTuesday 990 Data Lake (S3) | no | ok | XMLs 2009-2026 releases; yearly indices TY2007-TY2025 (build |
| filings | GivingTuesday 990 Data Marts (S3) | no | ok | All e-file years; latest builds 2026-06-16 / 2026-06-25 |
| filings | IRS Form 990 e-file XML index CSVs | no | ok | Release years 2021-2026 downloaded (4.27M rows); release yea |
| filings | IRS Form 990 e-file XML batch ZIPs (range reads) | no | ok | Releases 2021-2026: 24.0 GB, 3.86M members |
| filings | IRS EO Business Master File extract | no | ok | Snapshot dated 2026-09-07 (Last-Modified); one row per EIN;  |
| filings | IRS SOI annual extract of exempt-org financial data | no | ok | Extract years 2012-2024; '24' extract = filings processed in |
| filings | Urban Institute NCCS Core Series (harmonized panel) | no | ok | 1987-2024 |
| filings | Urban Institute NCCS E-file 990 tables | no | ok | 2009-2022 |
| filings | Urban Institute NCCS Unified BMF | no | ok | 1989-2026-09 |
| filings | Charity Navigator GraphQL API | yes | blocked_needs_key | Current ratings only |
| filings | NODC IRS e-file master concordance | no | ok | Version tags to 2023v5.1 (990) / 2016v3.0 (990-PF); observed |
| federal | USAspending.gov API v2 (search, recipient, references) | no | ok | search endpoints FY2008+ (2007-10-01 floor); downloads FY200 |
| federal | USAspending.gov award downloads (download/awards, bulk_download/awards) | no | ok | FY2001+ |
| federal | Federal Audit Clearinghouse API | yes (api.data.gov key) | ok | audit years 2016+ (Census-migrated through 2022, GSA intake  |
| federal | Grants.gov REST API (search2, fetchOpportunity) | no | ok | current posted/forecasted plus closed and archived history |
| federal | SAM.gov Assistance Listings data extract (CSV) | no | ok | current active listings only |
| federal | SAM.gov Entity Management API | yes (SAM.gov account API key) | blocked_needs_key | current registrations |
| federal | Treasury SLFRF public data (subaward file; quarterly reporting data) | no | ok | subawards reported through 2023-06-30; projects through 2026 |
| dc_hud | DC Open Data Hub search API and DCAT-US feed | no | ok | current catalog (1,871 datasets) |
| dc_hud | DC GIS Wards from 2022 (layer 53) | no | ok | 2022 redistricting (current) |
| dc_hud | DC GIS Census Tracts 2020 (layer 8) | no | ok | 2020 tracts |
| dc_hud | DC GIS Homeless Shelter Locations (layer 25) | no | ok_no_results | current snapshot |
| dc_hud | DC GIS Homeless Service Facilities (layer 6) | no | ok_no_results | current snapshot |
| dc_hud | DC GIS OVSJG Grant Recipients (layer 35) | no | ok | FY2016-FY2025 (1,267 rows) |
| dc_hud | OVSJG annual funding recipient lists (PDF) | no | ok | FY2016-FY2026 (FY2024-FY2026 downloaded) |
| dc_hud | DC OCP PASS Purchase Orders (layer 16) | no | ok | FY2013-FY2027 (279,712 rows) |
| dc_hud | DC OCP PASS Payments (layer 17) | no | ok | FY2017-FY2027 (1,576,128 rows) |
| dc_hud | DC OCP PASS Contracts (layer 37) | no | ok_no_results | FY2005-FY2027 (51,263 rows) |
| dc_hud | OCP Contracts and Procurement Transparency Portal | no | not_applicable | same as PASS layers |
| dc_hud | DC grants clearinghouse (MOCA / Serve DC, formerly OPGS) | no | not_applicable | current |
| dc_hud | DC FY2027 Approved Budget and Financial Plan: agency chapters + appendix tables | no | ok | FY2024 actual, FY2025 actual, FY2026 approved, FY2027 approv |
| dc_hud | DC FY2026 Approved Budget and Financial Plan: agency chapters + appendix tables | no | ok | FY2023 actual, FY2024 actual, FY2025 approved, FY2026 approv |
| dc_hud | DC FY2025 Approved Budget and Financial Plan: agency chapters + appendix tables | no | ok | FY2022 actual, FY2023 actual, FY2024 approved, FY2025 approv |
| dc_hud | DC FY2024 Approved Budget and Financial Plan: agency chapters + appendix tables | no | ok | FY2021 actual, FY2022 actual, FY2023 approved, FY2024 approv |
| dc_hud | DC Council performance-oversight pre-hearing responses (DHS, ICH, OVSJG, DBH, DHCD) | no | ok | 2024 cycle (FY23-24), 2025 cycle (FY24-25), 2026 cycle (FY25 |
| dc_hud | DC Council budget-oversight attachments (Attachment I contracts & grants, III grants) | no | ok | FY2024-FY2027 budget cycles |
| dc_hud | DC Council committee budget reports and Council Budget Office change charts | no | ok | FY2025-FY2027 budget cycles |
| dc_hud | DC Budget Support Acts FY2024-FY2027 (D.C. Law Library) | no | ok | FY2024-FY2027 |
| dc_hud | DC Council LIMS API | yes | blocked_needs_key | Council Periods 8-26 |
| dc_hud | HUD AHAR 2025 PIT counts by CoC, 2007-2025 | no | ok | 2007-2025 (one sheet per year) |
| dc_hud | HUD AHAR 2025 HIC counts by CoC, 2007-2025 | no | ok | 2007-2025 |
| dc_hud | HUD Exchange CoC Program award reports, DC-500 (AwardComp) | no | ok | 2019-2024 (FY2025 not published in this series) |
| dc_hud | hud.gov CoC award announcements (FY2024 DC report; FY2025 rounds 1-3) | no | ok | FY2024; FY2025 (announced 2026-03-31, 2026-04-27, 2026-05-21 |
| dc_hud | hud.gov CoC Grant Inventory Worksheet, DC-500 (FY2024, FY2026) | no | ok | FY2024 GIW, FY2026 GIW (FY2025 not posted) |
| dc_hud | HUD Exchange CoC Housing Inventory Count reports, DC-500 (project level) | no | ok | 2022-2025 downloaded (series back to 2007) |
| dc_hud | HUD Exchange CoC Population and Subpopulations reports, DC-500 | no | ok | 2024-2025 downloaded |
| dc_hud | MWCOG Homelessness in Metropolitan Washington (annual PIT report) | no | ok | 2023-2026 downloaded (2007-2026 linked) |
| dc_hud | The Community Partnership, DC ICH and DC PIT hub | no | ok_no_results | PIT summaries 2017-2025 |
| context | Census ACS 5-year API | yes | ok | latest 5-year 2020-2024; 2009-2024 vintages |
| context | ACS table-based Summary File (5-year) | no | ok | 2020-2024 (table-based format since 2021 vintage) |
| context | Census 2020 PL 94-171 (block counts) | yes | ok | 2020 |
| context | Census 2022 State Legislative District BEF (DC wards) | no | ok | 2022 wards (still current: DC absent from 2024 SLD BEF updat |
| context | TIGERweb ACS2024 Census Tracts | no | ok | 2020 tracts (used by ACS 2020-2024) |
| context | DC GIS Wards from 2022 | no | ok | 2022 wards (effective 2022 elections) |
| context | DC Office of Planning ACS 5-year ward profiles | no | ok | current vintage only (overwritten annually) |
| context | DC MAR 2 API (geocoder) | yes | ok | current |
| context | DC GIS Address Points (MAR extract) | no | ok | current MAR |
| context | Census Geocoder | no | ok | benchmarks Public_AR_Current, Public_AR_ACS2026, Census2020 |
| context | OMB CBSA delineation file (July 2023) | no | ok | July 2023 delineation (latest) |
| context | BLS CPI-U (Public Data API v2) | no (key optional) | ok | 2000-2025 annual averages |
| context | FRED fredgraph CSV (CPI) | no | failed |  |

---

# Filings recon (Phase 2)

Probe date 2026-10-10. Scripts: `scripts/10_probe_filings.py` (sources, reference downloads, volume estimate) and `scripts/11_eval_xml_tooling.py` (test XMLs, concordance, parser evaluation). Full probe output is in `logs/build_log.md` under the `10_probe_filings:` and `11_eval_xml_tooling:` headings.

## Phase 4 recommendations (short)
- **XML acquisition**: fetch every return by OBJECT_ID from the GivingTuesday data lake (`EfileData/XmlFiles/{OBJECT_ID}_public.xml`, anonymous S3). Use the IRS index CSVs (already in `raw/irs_xml_index/`) to pick OBJECT_IDs. Fall back to an IRS ZIP range read (remotezip) only for objects GT lacks, which today means members of `2026_TEOS_XML_05B` and `2026_TEOS_XML_08A`.
- **Parsing**: hand-written lxml parser with namespace-stripped, relative xpaths (see "XML parsing decision"). Use the NODC concordance as the data dictionary for labels and line numbers.
- **Financial series**: ProPublica for Calvary/core/DC/DMV only where a per-EIN call is acceptable; parse XML for TY2023+ (ProPublica has no data for Calvary TY2023 or TY2024). National series: IRS SOI extract or NCCS Core merged panel; GT data marts if XML-level fields are needed nationally.
- **Universe base**: IRS EO BMF state + region files (downloaded).

## Year labels (applies to every source)
IRS `TaxYr` in the XML header = year the period begins. Checked on all 11 Calvary XMLs: TY2021 = 2021-10-01..2022-09-30.
- ProPublica `tax_prd` = YYYYMM the period **ends**, and `tax_prd_yr` = that year (the fiscal year), not the IRS tax year. ProPublica `tax_prd_yr` 2022 = IRS TY2021.
- IRS index `TAX_PERIOD`, SOI `tax_pd`, BMF `TAX_PERIOD` = YYYYMM end of period. GT `TaxYear`/`TAXYEAR` = IRS tax year.
- Convert: `tax_year = YYYY if MM == 12 else YYYY - 1`.

## Calvary's e-filed returns
| tax_year | period end (fiscal_year) | OBJECT_ID | returnVersion | IRS index release / ZIP | GT S3 object | ProPublica data | total revenue (XML) |
|---|---|---|---|---|---|---|---|
| 2014-2018 | 2015-09 .. 2019-09 | 5 ids (see log) | 2014v6.0 .. 2018v3.1 | pre-2021 releases | yes | yes | 2.01M .. 2.49M |
| 2019 | 2020-09 (FY20) | 202130449349300208 | 2019v5.2 | index_2021 / 2021_TEOS_XML_01A | yes | yes | 3,896,046 |
| 2020 | 2021-09 (FY21) | 202212279349301511 | 2020v4.2 | index_2022 / 2022 ZIPs (no batch id) | yes | yes | 3,851,984 |
| 2021 | 2022-09 (FY22) | 202322239349302102 | 2021v4.2 | index_2023 / 2023_TEOS_XML_08A (found by central-directory scan) | yes | yes | 8,867,250 |
| 2022 | 2023-09 (FY23) | 202401649349300215 | 2022v5.0 | index_2024 / 2024_TEOS_XML_06A (index says `06a`) | yes | yes | 4,456,814 |
| 2023 | 2024-09 (FY24) | 202542169349300419 | 2023v6.0 | index_2025 / 2025_TEOS_XML_08A | yes | listed, no data | 5,817,167 |
| 2024 | 2025-09 (FY25) | 202631539349300848 | 2024v5.5 | index_2026 / 2026_TEOS_XML_06A | yes | latest_object_id only | 4,967,995 |

Raw copies: TY2014-TY2023 in `raw/xml/gt/`; TY2024 in `raw/xml/irs/` (range-read from the IRS ZIP; byte-identical to the GT S3 copy). No amended returns for Calvary in releases 2021-2026.

## ProPublica Nonprofit Explorer API v2 (`api_propublica`)
- Keyless. `/organizations/521307706.json` returns 13 `filings_with_data` (tax_prd 201109-202309) and 11 `filings_without_data` (PDF links only, incl. 202409). 68 financial fields per 990 filing, 126 per 990-PF filing (Meyer, Cafritz checked). No OBJECT_ID per filing; the org record carries `latest_object_id`.
- Search: `state[id]`, `ntee[id]` (1-10 major groups; 5 = Human Services = NTEE I-P), `c_code[id]` (subsection) all work. `total_results` caps at 10,000 and `num_pages` at 400; page 400 returns HTTP 400 "Pagination out of range". DC + ntee 5 = 3,069 orgs (123 pages); paged all of them, 3,069 distinct EINs. DC + ntee 5 + c3 = 2,824. MD and VA ntee 5 c3 hit the 10,000 cap, so split by city or use the BMF.
- Search rows carry no financials; one org call per EIN.
- Rate: 137 requests at 2 req/s, no 429s, median 0.04 s; responses are Cloudflare-cached (131 HITs).
- `download-xml?object_id=` returns 403 with a Cloudflare browser challenge, so ProPublica is not an XML source.
- Citation: cite ProPublica Nonprofit Explorer.

## GivingTuesday 990 Data Infrastructure API (`api_gt_efilexml`, `api_gt_990basic`, `api_gt_bmf`)
- Real endpoints (all GET, `ein=` required, one EIN per call): `/irs-data/efilexml`, `/irs-data/990basic120fields`, `/irs-data/bmf`, `/irs-data/postcard`, `/irs-data/pub78-deductible`, `/irs-data/revoked`. The docs page spells the path `/irs_data/`; that returns 403 "Missing Authentication Token". There is no swagger/openapi document (every docs path returns 403).
- No bulk or filter: a missing `ein` returns 400; `state=` alone returns 400; comma-separated EINs return an error body; unknown params (`taxyear=`) are ignored.
- `efilexml`: Calvary TY2014-TY2020 only, `IndexedOn` 2023-11-19. All 7 XMLs downloaded and sha256-matched.
- `990basic120fields`: 117 columns, Calvary TY2014-TY2021 (TY2021 has no XML URL). This is the only API endpoint with TY2021+ for Calvary.
- `bmf` is the 2024-02-13 BMF release (Calvary tax_period 202209), so it is stale.
- Rate limit 300 requests / 5 min (documented); probed at 0.9 req/s.

## GivingTuesday data lake (`bulk_gt_datalake`) and data marts (`bulk_gt_datamarts`)
- Bucket `gt990datalake-rawdata`, anonymous listing and GET. Per-object XML at `EfileData/XmlFiles/{OBJECT_ID}_public.xml`. Calvary TY2019-TY2024 all present.
- Coverage sample (40 random 990/EZ/PF rows per IRS index release): 2021-2025 releases 40/40; 2026 release 26/40.
  - By 2026 batch (8 rows each): every batch 8/8 except `05A` 4/8 and `08A` 0/8.
  - Sampling members straight from the ZIPs gives 2026 `05A` 10/10 and `05B` 0/10 (2025: 10/10 and 10/10).
  - So GT's 2026-08-25 build is missing two IRS batches: `2026_TEOS_XML_05B` (84,172 returns; GT mirrors the ZIP but has not unpacked it) and `08A` (50,349; posted 2026-09-16).
- Per-year indices `Indices/990xmls/yearly/{YYYY}_efiledata_xmls_created_on_2026-08-25.csv` cover 2007-2025 (2021: 299 MB ... 2025: 78 MB). These were not downloaded because the IRS index CSVs already cover the lookup.
- Data marts bucket `gt990datalake-analytics-and-datamarts/EfileDataMarts/`: national all-years CSVs, latest builds 2026-06-16/25. Examples: `990StandardFields` 3.2 GB, `990PFStandardFields` 0.84 GB, `990PFPart14Grants3A` (PF grants paid) 5.9 GB, `ScheduleIPart2Grants` 3.3 GB, `990PFPart7p1Officers` 1.2 GB. Listing only.

## IRS Form 990 XML index + batch ZIPs (`bulk_irs_xml_index`, `bulk_irs_xml`)
- `index_{2021..2026}.csv` downloaded (442 MB, 4.27M rows). Columns: RETURN_ID, FILING_TYPE, EIN, TAX_PERIOD, SUB_DATE, TAXPAYER_NAME, RETURN_TYPE (990/990EZ/990PF/990T), DLN, OBJECT_ID, plus XML_BATCH_ID from 2024 on. One release year mixes ~5 tax periods (e.g. index_2025: 617k rows TAX_PERIOD 2024, 97k 2025, 29k 2023).
- ZIPs: 52 live ZIPs for releases 2021-2026, 24.0 GB, 3.86M members, all serve `Accept-Ranges: bytes`. Member counts equal index row counts per release, except 2023 (2 index rows have no member).
- Gotchas:
  - 2021 is a single 3.7 GB ZIP (`2021_TEOS_XML_01A`). 2022 is `01A` (2.6 GB) plus `02A` (1.4 GB). `02A` is not linked on the downloads page and was found by probing names.
  - `2026_TEOS_XML_08A` is also not on the page, though the index references it.
  - 2024 batch ids are mixed case (`2024_TEOS_XML_04a`/`05a`/`06a`); the ZIP URLs need upper case, since the lower-case URL 302-redirects.
  - In 2025 and 2026 the index labels 163,540 / 168,344 rows `05A`, but they are split evenly across the `05A` and `05B` ZIPs (no overlap).
  - 2023 members sit under a folder (`2023_TEOS_XML_08A/{id}_public.xml`); other years have bare names.
- OBJECT_ID to ZIP without XML_BATCH_ID (releases 2021-2023):
  - 2021 has one ZIP.
  - 2022 has two; read both central directories (62.6 MB).
  - 2023 has 12 monthly ZIPs. Use the month of the DLN julian day (`DLN[5:8]`, year = `OBJECT_ID[:4]`) as the first guess, then read central directories. This found Calvary TY2021 in `2023_TEOS_XML_08A` after 1 central directory (4.0 MB). The month rule matches the batch for 85% of 2024-2026 rows (misses are mostly one month late), so it needs the central-directory check.
- remotezip test (Calvary TY2024, `2026_TEOS_XML_06A`, 210.8 MB): 3 range requests, 2.9 MB transferred (1.4% of the ZIP), nearly all of it central directory; member 54,115 B (10,872 B deflated). The cost is dominated by central directories: 0.7-55 MB per ZIP, 340 MB for all 52.

## IRS EO BMF (`bulk_irs_eo_bmf`)
- Downloaded `eo_dc/eo_md/eo_va.csv`, `eo1-eo4.csv` and `eo-info.pdf` (field and code definitions) to `raw/irs_bmf/` (364 MB). The files are dated 2026-09-07.
- Rows: DC 14,155; MD 43,659; VA 54,196; eo1 279,041; eo2 721,547; eo3 959,426; eo4 4,944 (national 1,964,958).
- 28 columns: EIN, NAME, ICO, STREET, CITY, STATE, ZIP, GROUP, SUBSECTION, AFFILIATION, CLASSIFICATION, RULING (YYYYMM), DEDUCTIBILITY, FOUNDATION, ACTIVITY, ORGANIZATION, STATUS, TAX_PERIOD (latest return, YYYYMM), ASSET_CD, INCOME_CD, FILING_REQ_CD, PF_FILING_REQ_CD, ACCT_PD (FYE month), ASSET_AMT, INCOME_AMT, REVENUE_AMT, NTEE_CD, SORT_NAME.
- Codes (from eo-info.pdf):
  - FOUNDATION: 00 not 501(c)(3); 02 private operating foundation exempt from excise tax; 03 private operating foundation (other); 04 private non-operating foundation; 09 suspense; 10 church; 11 school; 12 hospital/medical research; 13 college/university support org owned by a government unit; 14 governmental unit; 15 170(b)(1)(A)(vi) publicly supported; 16 509(a)(2); 17 509(a)(3); 18 509(a)(4); 21-24 509(a)(3) Types I/II/III-FI/III-NFI.
  - FILING_REQ_CD: 01 990/990-EZ; 02 990-N; 03 group return; 06 church; 07 government; 13 religious; 14 instrumentality; 00 not required.
  - PF_FILING_REQ_CD: 1 files 990-PF; 0 does not.
  - ASSET_CD/INCOME_CD: bands 0 to 9 ($0 ... $50M+).
  - ASSET_AMT = EOY book total assets. INCOME_AMT = total revenue with cost items added back. REVENUE_AMT = 990 Part I line 12 / 990-EZ line 9.
- DMV 990-PF filers: FOUNDATION 02/03/04 = 5,810 EINs (DC 629, MD 2,397, VA 2,784); PF_FILING_REQ_CD=1 = 5,818; both 5,773; either 5,855.
- NTEE_CD is blank for some large foundations (e.g. Meyer 530241716, Philip L. Graham Fund 526051781), so filter funders by FOUNDATION/PF code, not by NTEE.
- Calvary: SUBSECTION 03, FOUNDATION 15, NTEE L41Z, RULING 198406, TAX_PERIOD 202509, REVENUE_AMT 4,967,995, ACCT_PD 09.

## IRS SOI annual extract (`bulk_irs_soi_extract`)
- Files `{YY}eoextract990.zip`, `{YY}eoextract990pf.zip`, `{YY}eoextract990EZ.zip` (name casing varies by year) and `{YY}eofinextractdoc.xlsx`, for YY = 12 to 24. Each ZIP is 8-57 MB. No `25` files yet.
- The year label is the processing year: the `24` 990 extract is 84% tax periods ending 2023, plus 41k ending 2024 and a tail back to 2008.
- Downloaded `24eoextract990.zip` (56.7 MB; one CSV, 247 MB, 345,365 rows, 246 columns), `24eoextract990pf.zip` (12.8 MB; 119,059 rows, 180 columns incl. TAX_YR, GRSCONTRGIFTS, CONTRPDPBKS, FAIRMRKTVALEOY) and the doc xlsx.
- Calvary row in the 24 extract: tax_pd 202309 (TY2022), totrevenue 4,456,814, totfuncexpns 5,130,964, totassetsend 10,374,467. This matches ProPublica and the XML.
- GT mirrors the 12-23 extracts under `EfileData/Extracts/`.

## Urban Institute NCCS (`web_nccs_catalogs`)
- License ODC-BY (per Urban data catalog); cite NCCS.
- **Core Series** (catalog-core): harmonized panel 1987-2024.
  - Merged files at `nccsdata/processed_merged/core/{YEAR}/990combined/core_{YEAR}_990combined.csv` (2024: 18.8 MB, 66 columns, one row per EIN x tax period, SOI precedence, `is_amendment`).
  - SOI-current files at `processed/core/{YEAR}/990/` (2024: 40.6 MB) and PF at `processed_merged/core/{YEAR}/990pf/` (2023: 82.4 MB). CSV and parquet.
  - This is the cleaned long series that fits TY2011-TY2024 national financials, but it lags like SOI. Bucket listing is denied, so files must be fetched by direct URL.
- **E-file tables** (catalog-efile): 125 part-level tables at `nccs-efile/parsed/{TABLE}-{YEAR}.csv`, 2009-2022 only (2023 returns 404), no 990-PF.
- **Unified BMF** (catalog-bmf): 1989-present, build 2026-09-15, geocoded CSV 3.6 GB (`geocoding/unified-bmf/latest/`), plus monthly processed and raw BMF archives.
- Nothing bulk-downloaded; only catalog pages, HEADs, and a 16 KB header read of the Core 2024 file.

## Charity Navigator GraphQL API (`web_charitynavigator_api`)
- `POST https://api.charitynavigator.org/graphql`, header `Authorization: <key>`. A keyless call returns 401 "No Authorization Header".
- The developer portal advertises a 30-day free trial on its plans. A permanent free tier is not stated on the public pages, and the pricing page is script-rendered.
- Data: ratings (encompass score/stars), alerts, causes, not funding flows. Not signed up; logged in `open_questions.md`.

## NODC master concordance (`bulk_nodc_concordance`)
- Downloaded at commit d8266da934cd (2026-08-23) to `raw/concordance/` (15 MB): `concordance.csv` (6,864 rows, 990/990-EZ/schedules), `F990-PF-FULL.CSV` (2,231 PF rows), `DUCKDB-XPATH-REPORT.CSV` (every xpath observed in the Oct 2025 e-file rebuild, with schema versions and the mapped variable), `XPATH-VERSION-COUNT.CSV`, `MISSING-XPATHS-UNIQUE-FILE-ALL.CSV`, README, LICENSE, CITATION.
- The `versions` tags are stale. concordance.csv's newest tag is 2023v5.1, on 61 rows; F990-PF-FULL's newest is 2016v3.0. The xpaths themselves still match, though:
  - DUCKDB report: 5,163 990/EZ xpaths seen in 2023/2024 schemas, 5,050 mapped. Zero unmapped for Part VIII (16), Part IX (14), Part VII-A (17), Schedule I (77), Schedule R (367). The report has no 990-PF rows.
  - Leaf-path coverage on test XMLs: Calvary 2014v6.0-2024v5.5 100%; GWCF 2023v6.0 95% (Schedule C groups), 2024v5.1 100%; Meyer/Cafritz 990-PF 2021v4.2-2024v5.2 97%. The PF misses are `AnalysisIncomeProducingActyGrp` detail lines; grants-paid and officer xpaths are covered.

## XML parsing decision
**Recommendation: hand-written lxml parser with namespace-stripped, relative xpaths, one code path for all schema versions.** Use the concordance as the dictionary (variable names, part/line labels), not as the extraction driver. IRSx is a usable cross-check in QC.

Evidence (18 test XMLs: Calvary TY2014-TY2024, Meyer 990-PF TY2021-TY2024, Cafritz 990-PF TY2024, Greater Washington Community Foundation 990 TY2023-TY2024 with Schedules I and R; schema versions 2014v6.0 to 2024v5.5):
- **Hand-written lxml** (prototype `parse_return()` in script 11): the same xpaths extract every target field in every version, with no version branching:
  - Part I and VIII totals; Part IX `TotalFunctionalExpensesGrp`; Part VII-A `Form990PartVIISectionAGrp`; Schedule I `RecipientTable`; Schedule R `IdRelated*Grp`.
  - 990-PF `SupplementaryInformationGrp/GrantOrContributionPdDurYrGrp` and `OfficerDirTrstKeyEmplInfoGrp`.
  - For every 990-PF, the sum of listed grants equals `TotalGrantOrContriPdDurYrAmt`.
  - The TY2022+ 990-PF part renumbering (Supplementary Information moved from Part XV to Part XIV) did not change element names, so the xpaths are unaffected. Only line labels differ.
- **IRSx 0.5.1** (released 2026-09-22; throwaway venv): installs on Python 3.12 and 3.13.
  - It parsed all 13 files tested (Calvary TY2019-TY2024 plus the 7 foundation and GWCF returns), 2019v5.2-2024v5.5, as supported versions with 0 key errors.
  - Its counts and sums match lxml exactly: PF grants 170/166/177/274/452; Schedule I 1,163/1,417; Calvary revenue for each tested year.
  - Drawbacks: its output uses IRSx's abbreviated names (`GrntOrCntrbtnPdDrYr_Amt`); its PF part labels keep the pre-2022 numbering (`pf_part_xv`); and it is a single-maintainer project with a 2023-2026 release gap.
- **Concordance-driven lxml**: works, since 95-100% of leaf paths are mapped. But the version tags are stale, 990-PF sits in a separate file, and the target tables only need ~60 xpaths, so driving extraction from 9k rows adds indirection without adding coverage.

## Volume estimate for Phase 4 (IRS index releases 2021-2026 joined to DC/MD/VA BMF)
| set | EINs in BMF | returns (EINs filing) | by type | TY2020 / 21 / 22 / 23 / 24 / 25 | after latest-per-EIN+period | TY2020-TY2024 |
|---|---|---|---|---|---|---|
| (a) DMV 990-PF filers (FOUNDATION 02-04 or PF_FILING_REQ_CD=1), 990PF returns | 5,855 | 25,367 (5,249) | 990PF 25,367 | 3,884 / 4,256 / 4,527 / 4,835 / 4,912 / 2,534 | 25,154 | 22,210 |
| (b) DC 501(c)(3) public charities, NTEE L/P/F/I/J/W | 1,750 | 4,580 (968) | 990 3,907; 990EZ 670; 990PF 3 | 731 / 812 / 826 / 883 / 885 / 223 | 4,466 | 4,032 |

- Both sets touch 52 of the 52 ZIPs (every batch has some).
- Full ZIP download: 23.4 GB.
- remotezip: about 0.5 GB for (a)+(b) together. Central directories are 340 MB (read once and shared), members about 151 MB + 27 MB deflated.
- GT S3 per-object: about 0.95 GB uncompressed, from about 30k GETs with no ZIP mapping. This is a lower bound, since large foundations run 250-400 KB per XML. About 1,000 of the (a) returns sit in `2026_TEOS_XML_05B`/`08A` and need the remotezip fallback (central directories 10 MB).
- Amended or superseded repeats of EIN+period: 213 in (a), 114 in (b).

## Raw added by this area
`raw/irs_xml_index` 442 MB, `raw/irs_bmf` 365 MB, `raw/irs_soi` 67 MB, `raw/concordance` 15 MB, `raw/xml` 3.8 MB (18 XMLs), `raw/web_filings` 1.6 MB, `raw/propublica` 1.3 MB, `raw/gt` 0.4 MB. Total ≈ 896 MB.

---

# Federal sources (recon, probe date 2026-10-10)

Script: `scripts/12_probe_federal.py` (sections `usaspending`, `usa_download`, `fac`, `grantsgov`, `sam`, `slfrf`). Raw responses are in `raw/usaspending/`, `raw/fac/`, `raw/grantsgov/`, `raw/sam/` and `raw/treasury_slfrf/`. Each folder has a `*_requests_manifest.json` listing every request (URL, params/body, HTTP status, raw file). Key values are never saved.

| source_id | status | Calvary result |
|---|---|---|
| api_usaspending | ok | UEI `KMGRTKET2KJ1`, DUNS 126543453. 2 prime awards, 1 FSRS subaward. None from DC government. |
| bulk_usaspending | ok | Async download of Calvary's awards returned 3 rows (2 prime, 1 sub). |
| api_fac | ok | 2 single audits: audit years 2022 and 2023. |
| api_grantsgov | ok | Not applicable to Calvary. 1,467 posted+forecasted opportunities. |
| bulk_sam_assistance_listings | ok | Not applicable. 2,871 active listings. |
| api_sam_entity | blocked_needs_key | api.sam.gov returns 404 without a key. |
| bulk_treasury_slfrf | ok | 2 SLFRF subawards from DC government: $113,488 (2021-08-05) and $3,680,675 (2022-03-08). |

## Calvary identifiers
- USAspending recipient ids: `2813d90d-8166-9870-4c74-3eca995e2739-P` (parent), `...-C` (child). Both carry UEI `KMGRTKET2KJ1` and DUNS 126543453, with address 1217 Good Hope Rd SE (the street's former name), DC-98.
- A third, name-only record `a141975f-7383-7c48-fffa-47d17089658a-R` ("CALVARY WOMEN'S SERVICES", no UEI) holds the PPP loan.
- FAC `auditee_uei` = `KMGRTKET2KJ1` and `auditee_ein` = 521307706, so FAC links EIN to UEI.

## USAspending API v2 (`api_usaspending`)
**Calvary**
- Prime grant: `B-22-CP-DC-0213`. HUD 14.251 (Economic Development Initiative / Community Project Funding), $200,000 obligated, $76,866 outlaid. Period 2023-02-17 to 2030-08-31; action date 2023-08-04.
- Loan: SBA 59.073 PPP `5894917008`, $327,200, issued 2020-04-07. It is only on the name-only R-level record, so a UEI search misses it.
- Subaward (FSRS): LISC → Calvary, 14.252 Section 4 Capacity Building, $25,000, 2017-08-18 (prime `B-15-CB-NY-0001`).
- No contracts, IDVs, direct payments or other assistance.
- **No subawards from any DC government prime** under any CFDA. The FY23 SEFA's pass-through lines do not appear: OVSJG 21.027, TCP 14.235, DHS 10.561 and EFSP 97.024.

**DC probe** (recipient location DC, target CFDAs, FY2019–FY2026, `spending_by_award`)
- **Primes:** 836 rows (826 grants, 10 direct payments).
  - 224 rows go to DC government recipients by name match, totaling $4.44B. Names include "DISTRICT COLUMBIA GOVERNMENT", "GOVERNMENT OF THE DISTRICT OF COLUMBIA" and "DC OFFICE OF VICTIM SERVICES". The `recipient_type_names:["government"]` filter returns 205 instead.
  - TCP (The Community Partnership for the Prevention of Homelessness) has 366 CoC prime rows.
- **Subawards** (sub-recipient in DC): 891 rows. 546 come from DC government primes ($177.2M). By CFDA: 93.243/93.788 (145), 14.218 (116), 14.241 (103), 16.575 (77), 93.959 (39), 16.588 (30), 93.958 (24).
  - The CoC (14.267) has only 2 DC subaward rows. SLFRF (21.027) has 0. EFSP (97.024) has 0.
- **Prime counts per CFDA** (recipient in DC):
  - 14.267: 494
  - 10.561: 64
  - 93.243: 77
  - 64.033: 36
  - 14.251: 21
  - 93.671: 19
  - Most formula programs (14.218, 14.231, 14.239, 14.241, 16.575, 16.588, 93.958, 93.959, 17.258/17.259): 9–16 each
  - 21.027: 5 direct payments
  - 21.019: 2 direct payments
  - 21.023: 3 direct payments
  - 14.235 and 97.024: 0 (see gotchas)

**Gotchas**
- `award_type_codes` must come from a single group (grants 02–05; direct payments 06/10; loans 07/08; other 09/11/-1; contracts; IDVs).
- Loans reject `sort:"Award Amount"`. Use `"Loan Value"`.
- SLFRF, CRF and ERA primes to DC are **direct payments (06/10)**, not grants.
- Award-level location filters use the award's *current* recipient location. EFSP awards to the National Board (now in Alexandria, VA) are invisible under a DC filter in `spending_by_award` but appear in `spending_by_transaction` and `spending_by_category`. In the category rollup, 97.024 shows $1.475B under DC.
- With `subawards:true`, `recipient_locations` and `recipient_search_text` apply to the **sub-recipient**.
- The search endpoints only go back to 2007-10-01. Downloads go back to FY2001.
- The DC prime pull excludes 59.073 (PPP), which has 32,800 DC loans.

## USAspending downloads (`bulk_usaspending`)
- `POST /api/v2/download/awards/` takes the full advanced-search filter set (`program_numbers`, `recipient_locations`, `recipient_type_names`, `recipient_search_text`). It returns prime award summaries and subawards as separate CSVs in one zip, up to 500,000 rows.
  - Calvary job: finished in about 12 s, 2 prime rows + 1 subaward row.
- `POST /api/v2/bulk_download/awards/` requires `agencies` and does **not** accept `program_numbers`. It returns prime *transactions* plus subawards.
  - Probe (HUD-awarded, DC recipients, FY2024): finished in about 32 s, 599 prime transaction rows and 59 subaward rows.
- Poll `GET /api/v2/download/status/?file_name=`. An identical request returns the cached file.
- CSV descriptions contain embedded newlines, so count rows with a CSV parser, not a line count.

## Federal Audit Clearinghouse API (`api_fac`)
**Access:** `X-Api-Key` header with an api.data.gov key (`FAC_API_KEY`). The service is PostgREST, so filters look like `?auditee_ein=eq.521307706` and `in.(...)`.
- Rate limit header: 1,000 requests/hour. Each request returns at most 20,000 rows (use `limit`/`offset`).
- Data refreshes weekly (Wednesdays). Audit years run from 2016 on.
- Endpoints probed: general, federal_awards, passthrough, findings, findings_text, notes_to_sefa, secondary_auditors, additional_eins, additional_ueis, corrective_action_plans.

**Calvary**
- Only 2 reports.
- **`2022-09-CENSUS-0000258136`** (FYE 2022-09-30; JONES, MARESCA & MCELWANEY): total $4,067,718. All awards pass-through.

  | ALN | Program | Expended | Major | Pass-through |
  |---|---|---|---|---|
  | 21.027 | SLFRF | $3,583,885 | yes | DC OVSJG |
  | 14.235 | Supportive Housing Program | $415,830 | | The Community Partnership |
  | 97.024 | EFSP | $48,889 | | "Federal Emergency Management Agency" |
  | 10.561 | SNAP administrative matching grants | $19,114 | | DC DHS |

- **`2023-09-GSAFAC-0000037691`** (FYE 2023-09-30; JM&M; accepted 2024-04-22): total $4,064,718. Same four lines, same pass-through entities and amounts, except 97.024 = $45,889.
  - The FY23 audit PDF in `inputs/` shows a SEFA total of $937,999: 21.027 $440,677; 14.235 $390,649; 97.024 $67,684; 10.561 $38,989. See notes_for_analysis.
- No findings, secondary auditors, additional EINs or UEIs. `passthrough_id` is blank (2023) or `GSA_MIGRATION` (2022).
- No FAC records for audit years 2016–2021 or 2024–2025 under the EIN, the UEI or the name.

**DC universe** (`auditee_state=eq.DC`)

| Audit year | Audits |
|---|---|
| 2016 | 391 |
| 2017 | 384 |
| 2018 | 402 |
| 2019 | 398 |
| 2020 | 387 |
| 2021 | 409 |
| 2022 | 466 |
| 2023 | 477 |
| 2024 | 467 |
| 2025 | 359 (still arriving) |

- About 95% are non-profits.
- Audit year 2023 has 9,602 `federal_awards` rows, 3,614 of them pass-through (`is_direct=N`), with 3,614 matching `passthrough` rows. 486 rows from 111 auditees fall in the target CFDAs.
  - 97.024 appears only as pass-through (29 rows).
  - The legacy 14.235 is still reported (14 rows) alongside 14.267 (20 rows).
- OVSJG as pass-through (`passthrough_name ilike *victim services and justice*`): 75 rows across 43 reports, 2016–2025.

**Gotchas**
- No ALN field: build it from `federal_agency_prefix` + `.` + `federal_award_extension`.
- `federal_awards` has no state column, so filter `general` first, then query children by `report_id=in.(...)` in batches of 100.
- Pass-through names are free text with several spellings of the same agency (e.g. "DC OFFICE OF THE STATE SUPERINTENDENT OF EDUCATION" vs "D.C OFFICE OF STATE SUPERINTENDENT OF EDUCATION").
- The single-audit threshold rises from $750k to $1M for fiscal years beginning on or after 2024-10-01, which changes which orgs appear.

## Grants.gov REST API (`api_grantsgov`)
- `POST /v1/api/search2` and `POST /v1/api/fetchOpportunity` need no key.
- **The production filter key is `cfda`.** The docs say `aln`, but production ignores it and returns everything: `aln:"16.575"` matched 83,557, `cfda:"16.575"` matched 9. Responses use `cfdaList` (search) and `cfdas[].cfdaNumber` (detail).
- `oppStatuses` is pipe-joined (`forecasted|posted|closed|archived`). Other filters: `eligibilities` (e.g. `12` = 501(c)(3) nonprofits), `agencies`, `fundingCategories`, `fundingInstruments`.
- Pagination: `rows` + `startRecordNum` work. `rows=10000` returned 10,000; `rows=30000` failed (HTTP 502 or a dropped connection).
- Current universe: 867 posted + 600 forecasted = 1,467, all returned in one call. Only 3 of them list a target CFDA.
- `fetchOpportunity` returns a `synopsis` block (posted) or a `forecast` block. Fields include `awardCeiling`, `awardFloor`, `estimatedFunding`, `responseDate` (close date), `applicantTypes[].id` (eligibility codes), `applicantEligibilityDesc` and `cfdas`.
- An unquoted multi-word keyword is OR-matched; a quoted phrase is matched exactly.

**Keyword hits** (posted+forecasted)

| Keyword | Total | Posted | Forecasted | 501(c)(3)-eligible | Phrase |
|---|---|---|---|---|---|
| homelessness | 13 | 11 | 2 | 10 | |
| housing | 176 | 163 | 13 | 134 | |
| domestic violence | 387 | 358 | 29 | 189 | 9 |
| victim services | 670 | 457 | 213 | 361 | 4 |
| women | 162 | 130 | 32 | 54 | |
| substance use | 677 | 489 | 188 | 368 | 60 |
| workforce | 217 | 187 | 30 | 96 | |
| reentry | 9 | 9 | 0 | 3 | |
| veterans | 82 | 73 | 9 | 13 | |
| aging | 94 | 63 | 31 | 75 | |

## SAM.gov (`bulk_sam_assistance_listings`, `api_sam_sgs`, `api_sam_entity`)
- **Assistance Listings (CFDA catalog) metadata is available without a key.**
  - The public CSV extract (redirects to a signed S3 URL; 22 MB; 2,871 active listings; 38 columns including title, agency, eligibility and obligations) is in `raw/sam/`.
  - sam.gov's own search backend (`/api/prod/sgs/v1/search/?index=cfda&q=`) also works without a key but is undocumented.
- **UEI lookup by name: no keyless SAM route.** `index=ei` without login returns exclusions only, and `api.sam.gov` entity and assistance-listing paths return 404 without a key.
  - USAspending and FAC already give Calvary's UEI. For other DC orgs, FAC gives EIN→UEI for single-audit filers, and USAspending gives name→UEI for federal recipients.

## Treasury SLFRF public data (`bulk_treasury_slfrf`)
- `SLFRF-Subaward-USASpending-File.xlsx` (60 MB; sheet "SLFRF Subawards as of 06-30-23") has 37,616 subaward rows. They are in USAspending's subaward column layout but are **not loaded into USAspending's subaward search**.
  - DC government prime: 462 rows, $815.2M.
  - Calvary rows:
    - `1500`: $113,488, 2021-08-05, "15 beds of transitional housing ... women fleeing domestic violence"
    - `12126`: $3,680,675, 2022-03-08, "Purchase a building to create New Foundations ... 35 homeless women who are survivors of domestic violence"
- The latest reporting workbook, `April-2026-Reporting-Data-through-March-31-2026.xlsx`, is project-level only. It has no subrecipient columns. DC has 305 projects, 33 of which match homeless/victim/women/domestic/shelter/unhoused keywords.

## Assistance listings: current titles
USAspending titles and the SAM active extract match. 21.019 and 14.235 are not in the active extract, so their titles come from USAspending.

| ALN | Current title |
|---|---|
| 14.267 | Continuum of Care Program |
| 14.231 | Emergency Solutions Grant Program |
| 14.241 | Housing Opportunities for Persons with AIDS |
| 14.218 | Community Development Block Grants/Entitlement Grants |
| 14.239 | Home Investment Partnerships Program |
| 16.575 | Crime Victim Assistance |
| 16.588 | Violence Against Women Formula Grants |
| 16.736 | Transitional Housing Assistance for Victims of Domestic Violence, Dating Violence, Stalking, or Sexual Assault |
| 93.671 | Family Violence Prevention and Services/Domestic Violence Shelter and Supportive Services |
| 93.959 | Block Grants for Prevention and Treatment of Substance Abuse |
| 93.958 | Block Grants for Community Mental Health Services |
| 93.243 | Substance Abuse and Mental Health Services Projects of Regional and National Significance |
| 21.027 | Coronavirus State and Local Fiscal Recovery Funds |
| 21.019 | Coronavirus Relief Fund (inactive) |
| 97.024 | Emergency Food and Shelter National Board Program |
| 64.033 | VA Supportive Services for Veteran Families Program |
| 17.258 | WIOA Adult Program |
| 17.259 | WIOA Youth Activities |
| 16.812 | Second Chance Act Reentry Initiative |
| 14.235 | Supportive Housing Program (inactive; still on Calvary's SEFA) |
| 10.561 | State Administrative Matching Grants for the Supplemental Nutrition Assistance Program |
| 14.251 | Economic Development Initiative, Community Project Funding, and Miscellaneous grants |
| 14.252 | Section 4 Capacity Building for Community Development and Affordable Housing |
| 59.073 | Paycheck Protection Loan Program (PPP) |
| 21.023 | Emergency Rental Assistance Program |

## Phase 4 pull design
Use script numbers in the `3x`–`4x` range. Every pull saves raw, then `5x` scripts parse.

### (a) Calvary and DC-sector orgs: federal awards, including subawards
1. **USAspending prime + subaward download (target CFDAs):** `POST /api/v2/download/awards/`. Filters:
   ```json
   {"program_numbers": [<24 target ALNs, excluding 59.073>],
    "recipient_locations": [{"country": "USA", "state": "DC"}],
    "award_type_codes": ["02","03","04","05","06","10"],
    "time_period": [{"start_date": "2018-10-01", "end_date": "2026-09-30"}]}
   ```
   Then poll `/api/v2/download/status/`.
   - Expected rows: **836 prime award summaries, 891 subawards**. At transaction level (`download/count`, `spending_level:"transactions"`) this is 2,100 rows.
   - Run a second job with `place_of_performance_locations` DC: 818 awards, 513 subawards.
2. **USAspending DC nonprofit grants (all CFDAs, for peer context):** the same endpoint with `recipient_type_names:["nonprofit"]` and `award_type_codes` 02–05.
   - Expected: **9,028 awards, 2,569 subawards**.
   - The all-recipient DC grant universe is 21,168 awards and 23,709 subawards. All of these are under the 500k limit.
3. **Calvary:** `recipient_search_text:["CALVARY WOMEN'S SERVICES"]` (the name, not the UEI, because the PPP loan has no UEI), all assistance types, FY2008 onward. Expected: 2 prime + 1 subaward.
4. **Join keys:** match orgs to USAspending by UEI. EIN→UEI comes from FAC `general` (`auditee_ein`, `auditee_uei`). For other orgs, use `norm_name` matching against `recipient_name`.
5. **SLFRF subawards (Treasury):** parse the saved `SLFRF-Subaward-USASpending-File.xlsx` for `prime_awardee_state_code = DC`. Expected: 462 rows. Join the DC "Projects" sheet (305 rows) from the latest quarterly workbook for project and expenditure-category context.
   - Before Phase 4, check the public-data page for a newer subaward file (the current one is as of 2023-06-30).
6. **Coverage note:** DC government's CoC (TCP), EFSP and SLFRF pass-through to nonprofits is missing or nearly missing in USAspending subawards. FAC (b) and the Treasury file are the sources for those streams.

### (b) FAC SEFA lines for DC auditees
1. `GET /general?auditee_state=eq.DC&audit_year=eq.{Y}&limit=20000` for Y = 2016…2026, with selected columns. Expected: about **4,140 audits** for 2016–2025, growing as 2025–2026 audits arrive.
2. For report_ids in batches of 100:
   - `GET /federal_awards?report_id=in.(...)&limit=20000`: expected about 85–95k rows (2023 alone has 9,602).
   - `GET /passthrough?report_id=in.(...)`: expected about 30–35k rows (2023 has 3,614).
   - Optionally `findings` and `notes_to_sefa`.
3. Calls: about 42 batches × 2–4 endpoints + 11 general calls ≈ 100–180 requests. That fits under the 1,000/hour key limit at 1 req/s.
4. Optional national pass-through sweep, to catch DC agencies passing funds to orgs outside DC. Counts are all auditee states, all years:
   - `GET /passthrough?passthrough_name=ilike.*district of columbia*`: 5,224 rows
   - `*DC Department*`: 716 rows
   - `*community partnership*`: 919 rows (includes non-DC namesakes)
5. Build the ALN as prefix + "." + extension. Normalize `passthrough_name` to DC agency ids (OVSJG, DHS, DBH, DC Health, DHCD, OSSE, TCP).

### (c) Grants.gov open and forecast opportunities
1. `POST /v1/api/search2 {"rows":5000,"oppStatuses":"forecasted|posted"}`: one call, about **1,467 rows** today. Page with `startRecordNum` if `hitCount` exceeds 5,000.
2. Filter locally:
   - `cfdaList` ∩ the target ALNs (3 today)
   - keyword sets (quoted phrases for multi-word terms)
   - eligibility, via a second search with `eligibilities:"12|25|99"`
   - Estimated relevant set: 300–700.
3. `POST /v1/api/fetchOpportunity {"opportunityId":N}` for each relevant id, for ceiling/floor, estimated funding, close date, eligibility codes and CFDAs.
4. Optional history: `oppStatuses:"closed|archived"` (82,090 rows) in pages of 10,000, filtered by `cfda` for the target ALNs. This gives each program's past NOFO cadence.

---

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

---

# Context sources: geography, demographics, inflation

Probed 2026-10-10 by `scripts/16_probe_context.py` (rerunnable; static downloads reused unless `--refresh`). Status per source is in `context.csv`. Run log: `logs/build_log.md`, sections "16_probe_context: *".

## Census ACS 5-year API (`api_census_acs5`)
- The latest vintage is **2024 (2020-2024)**. `/data/2025/acs/acs5.json` and `/data/2025/acs/acs1.json` return 404.
- **A key is required for every data call.** Keyless requests get a 302 to `missing_key.html` over both http and https. Metadata (`variables.json`, `groups/*.json`, dataset `.json`) is keyless. `CENSUS_API_KEY` is active (keyed HTTP 200).
- The pull is done: 11 groups (`B01003 B03002 B09019 B11001 B17001 B17012 B18101 B19013 B21001 B23025 B25070`) x 9 geographies = 99 raw JSON files in `raw/census/*_acs5_2024_{group}_{geo}.json`. Geographies: US, states 11/24/51/54, CBSA 47900, DC wards, DC tracts (206), all DC/MD/VA counties, and WV 037. Each pull is `group()`, which returns E, M, EA and MA columns plus `GEO_ID`.
- **DC wards are Census state legislative districts (upper chamber).** `for=state legislative district (upper chamber):*&in=state:11` returns official ward estimates with MOEs ("Ward 8 (2024)"), so ward totals need no crosswalk.
- `config/acs_variables.csv` lists 65 variables. Labels and concepts are copied exactly from `variables.json`. Each row also has the MOE variable and the Summary File column names.
- Gotcha: the ward GEOID differs by SLD vintage code. ACS 2024 uses `610U900US11008`, the DC GIS ward layer uses `610U600US11008`. Join on the ward number, not the GEOID.
- Recommendation: no further bulk work is needed for the latest vintage. For a time series, rerun the same pulls for earlier vintages. 2020+ vintages use 2020 tracts, and 2022+ use 2022 wards.

## ACS table-based Summary File (`bulk_census_acs_sf`)
- This is the keyless fallback. National pipe-delimited files `acsdt5y2024-{table}.dat` (16-145 MB each) contain every summary level: tract `1400000US11001…`, ward `610U900US110…`, county `0500000US…` and MSA `310M700US47900`. The probe confirmed B01003 values match the API.
- Not downloaded by default. `--sf-fallback` fetches all 11 tables (~750 MB).

## 2020 PL 94-171 blocks (`api_census_dec_pl`) and 2022 SLDU BEF (`bulk_census_bef_sldu2022`)
- PL: 6,012 DC blocks with `P1_001N` (population) and `H1_001N` (housing units). The keyless fallback is the DC GIS "Census Blocks 2020" layer.
- BEF: `11_DC_SLDU22.txt` (block GEOID → SLDUST 001-008), read by HTTP range from the 25 MB national zip. This is the **official block-to-ward assignment**. DC is not in the 2024 SLD BEF update, so the 2022 wards are still current.

## TIGERweb ACS2024 tracts (`api_tigerweb`)
- 206 DC tract polygons with internal points, as GeoJSON (EPSG:4326) in `raw/geo/`.

## DC GIS Wards from 2022 (`api_dcgis_wards_2022`)
- 8 polygons in `raw/geo/*_dcgis_wards_2022.geojson`. The layer also has councilmember phone, email and office fields. These are excluded from the pull (people-data rule).
- DC Open Data searches for "crosswalk", "tract ward" and "census tract ward equivalency" found **no official tract-to-ward crosswalk** (raw search responses are saved).

## DC Office of Planning ACS ward profiles (`api_dcgis_acs_ward`)
- `Demographic_WebMercator/MapServer` layers 39 (DP05), 42 (DP03), 45 (DP04) and 48 (DP02) by 2022 ward. Tract versions are layers 38/41/44/47. The current vintage is 2020-2024 (DC OP pulled it from the Census API on 2026-03-11).
- These are profile tables only: no female-by-age poverty detail, and only the current vintage (the service is overwritten each year). Use them as a cross-check against the SLDU pulls, not as the primary source.

## DC MAR 2 API (`api_dc_mar2`)
- `blocked_needs_key`: without a key it returns HTTP 500 "API Key is required." Keys are free through the Data Developers Portal (developers.data.dc.gov), and the env var would be `DC_MAR_API_KEY`. The script uses the key automatically when it is set.
- Per OCTO bulletins, it returns MAR ID, lat/lon, wards (2002/2012/2022), ANC, SMD, precinct and neighborhood cluster. It does fuzzy matching.

## DC GIS Address Points (`api_dcgis_address_points`)
- Keyless MAR extract. It matches on exact attributes (`ADDRESS_NUMBER`, `STREET_NAME`, `QUADRANT`).
- Calvary result: **1217 MARION BARRY AVENUE SE → Ward 8, SMD 8A06, ANC 8A**, lat 38.86708, lon -76.98805, MAR_ID 338288.
- It has no census tract field. Get the tract from the Census Geocoder or by point-in-polygon.

## Census Geocoder (`api_census_geocoder`)
- Keyless. Single-line requests with `vintage=ACS2024_Current&layers=all` return state, county, tract, and SLDU (= DC ward).
- The batch endpoint (`/geographies/addressbatch`, multipart POST, up to 10,000 rows) returns state, county, tract and, with `vintage=Census2020_Current`, the 2020 block. The block joins straight to the ward BEF.
- **Gotcha:** "1217 Marion Barry Ave SE" does not match, because TIGER still has the former name **Good Hope Rd SE**. The old name matches: tract 11001007503, Ward 8.
- MD test (8106 Georgia Ave, Silver Spring) → 24031 / tract 24031702501. VA test (930 N Henry St, Alexandria) → 51510 / tract 51510201602.

## OMB CBSA delineation, July 2023 (`bulk_omb_cbsa_2023`)
- `list1_2023.xlsx` is the latest delineation. CBSA 47900 has 23 county equivalents: DC 1, MD 4, VA 17 (including 6 independent cities), and WV 1 (Jefferson, flagged `in_scope=false`).
- The MSA has 3 metro divisions: Washington DC-MD (47764), Frederick-Gaithersburg-Bethesda (23224), and Arlington-Alexandria-Reston (11694).
- Calvert Co. MD moved to the Lexington Park CBSA in 2023, so older ACS MSA totals are not comparable.
- Output: `config/dmv_counties.csv`. Reading the xlsx needs `openpyxl`.

## BLS CPI-U (`api_bls_cpi`)
- BLS API v2 works **without a key** at the v1 limits: 10-year windows and 25 queries per day. `annualaverage:true` returns M13.
- Series:
  - `CUUR0000SA0`: 2000-2025.
  - `CUURS35ASA0` (Washington-Arlington-Alexandria, bimonthly): annual averages only from 2015. 2000-2014 has bimonthly values but no published annual average.
  - `CUUSS35ASA0`: semiannual, with S03 as the annual average. Kept as a fallback.
- **2025 annual average is published**: US 321.943, DC metro 321.993. October 2025 was not collected because of the 2025 lapse in appropriations (BLS footnote).
- `config/cpi_u_annual.csv` is based on **2024** (US 313.689, DC 315.186). `*_factor_to_base` converts nominal dollars to 2024 dollars.
- `download.bls.gov` flat files return 403 unless the User-Agent includes a contact email. They are not needed.

## FRED (not registered)
- `fredgraph.csv` timed out or reset from this host, so it is marked `failed`. BLS covers the same series.

## Phase 4/5 design

### dim_geo
- **Grain:** one row per geography unit. `geo_level` ∈ {us, state, cbsa, metro_division, county, ward, tract}.
- **Keys:**
  - `state_fips` (2-char)
  - `county_fips` (3-char; `county_geoid` = state + county)
  - `tract_geoid` (11-char)
  - `ward` (int 1-8; DC only)
  - `geo_id` = the Census `GEO_ID` from the ACS pull, as a natural key for joins back to raw.
- **Ward rows:** `state_fips=11`, `county_fips=001`, `ward=n`, no tract. Estimates come straight from the ACS SLDU pull, which is official and has MOEs.
- **Service-area row:** `geo_level=service_area`, Wards 7+8. Counts are summed; MOE = sqrt(m7² + m8²).
- **Tract rows:**
  - `ward_majority`, `ward_majority_pop_share` and `split_ward` come from the block crosswalk.
  - `in_service_area` = majority ward in {7, 8}.
- **County rows:** all DC/MD/VA counties that were pulled. Columns `in_msa`, `in_scope`, `metro_division` and `central_outlying` come from `config/dmv_counties.csv`.
- **Indicator columns:** one set per vintage, with `acs_vintage`, each estimate plus its `_moe`, then `source_id` and `retrieved_date`. Derived rates follow Census ACS MOE formulas: sums use root-sum-of-squares, proportions use the proportion formula, and both are flagged `basis=derived`.
  - poverty rate
  - adult-female poverty rate and female poverty counts by age band
  - rent burden 30%+ and 50%+ (universe excludes "not computed")
  - median household income
  - race/ethnicity shares
  - female-householder family share and female householders living alone
  - female-householder family poverty
  - unemployment rate
  - disability rate (sum of all "With a disability" cells)
  - veterans and female veterans
  - total population
- **Tract-to-ward crosswalk (chosen method): population-weighted through 2020 blocks.**
  - Each 2020 block gets its ward from the official SLDU BEF and its population and housing units from PL 94-171.
  - Sum by (tract, ward), then divide by tract population. Write the result to `clean/` as a support table: `tract_geoid, ward, pop2020, hu2020, pop_share, hu_share`.
  - Checks:
    - 6,012/6,012 blocks have a ward.
    - 12 of 206 tracts span more than one ward; 9 have less than 95% of their population in one ward.
    - Tract B01003 allocated to wards lands within 1% of the ACS SLDU totals.
    - The tract internal-point method disagrees with the block majority for 4 tracts. Area-weighting is not needed.
  - Use the crosswalk only to roll up tract-only measures. Ward totals come from SLDU.

### Org addresses → ward / county / tract
1. **Input:** org mailing or street addresses as stated in BMF or 990 filings, keeping the original. These are organization addresses only.
2. **Census batch geocoder** for all addresses, `benchmark=Public_AR_Current`, `vintage=Census2020_Current`, in chunks of 10,000 or fewer. It returns state FIPS, county FIPS, tract and block. For DC orgs, the block joins to the BEF to give the ward.
3. **No_Match retries:**
   1. Apply a street-alias table, e.g. `MARION BARRY AVE SE → GOOD HOPE RD SE`, then retry.
   2. For DC, run an exact lookup in DC GIS Address Points (or MAR 2 if a key appears), which gives ward, SMD, ANC and lat/lon. Then assign the tract by point-in-polygon against the TIGERweb tracts (shapely).
   3. For PO boxes or remaining misses, assign the county from the ZIP (ZCTA-county relationship) with `confidence=low`. Leave tract and ward null.
4. **Provenance:** keep `geo_method` (census_batch_exact, census_batch_nonexact, alias, dc_address_points, mar2, zip_fallback), `confidence` (high, medium, low) and `basis=derived`.
5. **Join to dim_geo:** `county_geoid`, then `tract_geoid`, then `ward`.

### dim_period (CPI)
- Columns: `year`, `cpi_u_us`, `cpi_u_dc_metro`, and factors to 2024.
- The DC metro series has no annual average before 2015. Use the US series for any series that starts before 2015, or flag it.
