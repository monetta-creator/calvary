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
