# Build log

Append-only record of what ran, row counts, failures and decisions.

### 2026-10-10 12:05 — 00_setup
- inputs/: copied 25, already present 0
- API keys present: TAVILY_API_KEY=no, FAC_API_KEY=no, CENSUS_API_KEY=no

### 2026-10-10 12:16 — 10_probe_filings: bmf
- eo_dc.csv: 14,155 rows, 2.6 MB, subsection 03 10,917, FOUNDATION 02/03/04 629, PF_FILING_REQ_CD=1 626 (downloaded raw/irs_bmf/20261010T121504_eo_dc.csv)
- eo_md.csv: 43,659 rows, 7.7 MB, subsection 03 37,165, FOUNDATION 02/03/04 2,397, PF_FILING_REQ_CD=1 2,397 (downloaded raw/irs_bmf/20261010T121505_eo_md.csv)
- eo_va.csv: 54,196 rows, 9.5 MB, subsection 03 45,151, FOUNDATION 02/03/04 2,784, PF_FILING_REQ_CD=1 2,795 (downloaded raw/irs_bmf/20261010T121505_eo_va.csv)
- eo1.csv: 279,041 rows, 48.8 MB, subsection 03 234,977, FOUNDATION 02/03/04 24,652, PF_FILING_REQ_CD=1 25,073 (downloaded raw/irs_bmf/20261010T121506_eo1.csv)
- eo2.csv: 721,547 rows, 126.1 MB, subsection 03 578,354, FOUNDATION 02/03/04 43,174, PF_FILING_REQ_CD=1 45,852 (downloaded raw/irs_bmf/20261010T121508_eo2.csv)
- eo3.csv: 959,426 rows, 165.3 MB, subsection 03 824,268, FOUNDATION 02/03/04 62,403, PF_FILING_REQ_CD=1 64,346 (downloaded raw/irs_bmf/20261010T121605_eo3.csv)
- eo4.csv: 4,944 rows, 0.9 MB, subsection 03 4,506, FOUNDATION 02/03/04 285, PF_FILING_REQ_CD=1 287 (downloaded raw/irs_bmf/20261010T121612_eo4.csv)
- columns (28): EIN, NAME, ICO, STREET, CITY, STATE, ZIP, GROUP, SUBSECTION, AFFILIATION, CLASSIFICATION, RULING, DEDUCTIBILITY, FOUNDATION, ACTIVITY, ORGANIZATION, STATUS, TAX_PERIOD, ASSET_CD, INCOME_CD, FILING_REQ_CD, PF_FILING_REQ_CD, ACCT_PD, ASSET_AMT, INCOME_AMT, REVENUE_AMT, NTEE_CD, SORT_NAME
- Calvary row: {"NAME": "CALVARY WOMENS SERVICES INC", "SUBSECTION": "03", "FOUNDATION": "15", "NTEE_CD": "L41Z", "RULING": "198406", "TAX_PERIOD": "202509", "ASSET_AMT": "10059516", "INCOME_AMT": "5227366", "REVENUE_AMT": "4967995", "FILING_REQ_CD": "01", "PF_FILING_REQ_CD": "0", "ACCT_PD": "09"}
- DC+MD+VA: 112,010 rows; FOUNDATION 02/03/04 = 5,810 EINs; PF_FILING_REQ_CD=1 = 5,818; both = 5,773; either = 5,855

### 2026-10-10 12:16 — 10_probe_filings: irs_index
- index_2021.csv: 589,904 rows, 74.8 MB, sha256 c810e27f276d, downloaded raw/irs_xml_index/20261010T121613_index_2021.csv
  - columns: RETURN_ID, FILING_TYPE, EIN, TAX_PERIOD, SUB_DATE, TAXPAYER_NAME, RETURN_TYPE, DLN, OBJECT_ID
  - RETURN_TYPE: {'990': 305173, '990EZ': 164035, '990PF': 108644, '990T': 12052}
  - XML_BATCH_ID values: 1 ((blank))
  - TAX_PERIOD year: {'2018': 2000, '2019': 14090, '2020': 490856, '2021': 82958}
- index_2022.csv: 656,503 rows, 72.2 MB, sha256 5493bf8850e2, downloaded raw/irs_xml_index/20261010T121616_index_2022.csv
  - columns: RETURN_ID, FILING_TYPE, EIN, TAX_PERIOD, SUB_DATE, TAXPAYER_NAME, RETURN_TYPE, DLN, OBJECT_ID
  - RETURN_TYPE: {'990': 325555, '990EZ': 189690, '990PF': 117073, '990T': 24185}
  - XML_BATCH_ID values: 1 ((blank))
  - TAX_PERIOD year: {'2019': 2690, '2020': 25139, '2021': 544954, '2022': 83720}
- index_2023.csv: 705,156 rows, 77.5 MB, sha256 3906ff84e872, downloaded raw/irs_xml_index/20261010T121618_index_2023.csv
  - columns: RETURN_ID, FILING_TYPE, EIN, TAX_PERIOD, SUB_DATE, TAXPAYER_NAME, RETURN_TYPE, DLN, OBJECT_ID
  - RETURN_TYPE: {'990': 347337, '990EZ': 209957, '990PF': 124666, '990T': 23196}
  - XML_BATCH_ID values: 1 ((blank))
  - TAX_PERIOD year: {'2020': 4831, '2021': 29921, '2022': 581879, '2023': 88525}
- index_2024.csv: 728,719 rows, 91.1 MB, sha256 c00051a33f65, downloaded raw/irs_xml_index/20261010T121621_index_2024.csv
  - columns: RETURN_ID, FILING_TYPE, EIN, TAX_PERIOD, SUB_DATE, TAXPAYER_NAME, RETURN_TYPE, DLN, OBJECT_ID, XML_BATCH_ID
  - RETURN_TYPE: {'990': 363100, '990EZ': 215355, '990PF': 126982, '990T': 23282}
  - XML_BATCH_ID values: 12 (2024_TEOS_XML_01A, 2024_TEOS_XML_02A, 2024_TEOS_XML_03A, 2024_TEOS_XML_04a, 2024_TEOS_XML_05a, 2024_TEOS_XML_06a, 2024_TEOS_XML_07A, 2024_TEOS_XML_08A, 2024_TEOS_XML_09A, 2024_TEOS_XML_10A, 2024_TEOS_XML_11A, 2024_TEOS_XML_12A)
  - TAX_PERIOD year: {'2019': 42, '2020': 356, '2021': 13815, '2022': 29084, '2023': 594434, '2024': 90988}
- index_2025.csv: 748,906 rows, 93.1 MB, sha256 e54ba6938d98, downloaded raw/irs_xml_index/20261010T121624_index_2025.csv
  - columns: RETURN_ID, FILING_TYPE, EIN, TAX_PERIOD, SUB_DATE, TAXPAYER_NAME, RETURN_TYPE, DLN, OBJECT_ID, XML_BATCH_ID
  - RETURN_TYPE: {'990': 376920, '990EZ': 217102, '990PF': 130347, '990T': 24537}
  - XML_BATCH_ID values: 15 (2025_TEOS_XML_01A, 2025_TEOS_XML_02A, 2025_TEOS_XML_03A, 2025_TEOS_XML_04A, 2025_TEOS_XML_05A, 2025_TEOS_XML_06A, 2025_TEOS_XML_07A, 2025_TEOS_XML_08A, 2025_TEOS_XML_09A, 2025_TEOS_XML_10A, 2025_TEOS_XML_11A, 2025_TEOS_XML_11B, 2025_TEOS_XML_11C, 2025_TEOS_XML_11D, 2025_TEOS_XML_12A)
  - TAX_PERIOD year: {'2021': 38, '2022': 4524, '2023': 29453, '2024': 617444, '2025': 97447}
- index_2026.csv: 436,239 rows, 54.1 MB, sha256 49fddcbea054, downloaded raw/irs_xml_index/20261010T121627_index_2026.csv
  - columns: RETURN_ID, FILING_TYPE, EIN, TAX_PERIOD, SUB_DATE, TAXPAYER_NAME, RETURN_TYPE, DLN, OBJECT_ID, XML_BATCH_ID
  - RETURN_TYPE: {'990': 208833, '990EZ': 135053, '990PF': 79686, '990T': 12667}
  - XML_BATCH_ID values: 8 (2026_TEOS_XML_01A, 2026_TEOS_XML_02A, 2026_TEOS_XML_03A, 2026_TEOS_XML_04A, 2026_TEOS_XML_05A, 2026_TEOS_XML_06A, 2026_TEOS_XML_07A, 2026_TEOS_XML_08A)
  - TAX_PERIOD year: {'2022': 4, '2023': 3168, '2024': 16301, '2025': 396940, '2026': 19826}
- Calvary rows (all release years):
  - {"RETURN_ID": "17925397", "FILING_TYPE": "EFILE", "TAX_PERIOD": "202009", "SUB_DATE": "4/12/2021 4:46:12 PM", "RETURN_TYPE": "990", "DLN": "93493044002081", "OBJECT_ID": "202130449349300208", "_release_year": 2021}
  - {"RETURN_ID": "20302809", "FILING_TYPE": "EFILE", "TAX_PERIOD": "202109", "SUB_DATE": "2022", "RETURN_TYPE": "990", "DLN": "93493227015112", "OBJECT_ID": "202212279349301511", "_release_year": 2022}
  - {"RETURN_ID": "21868614", "FILING_TYPE": "EFILE", "TAX_PERIOD": "202209", "SUB_DATE": "2023", "RETURN_TYPE": "990", "DLN": "93493223021023", "OBJECT_ID": "202322239349302102", "_release_year": 2023}
  - {"RETURN_ID": "22613638", "FILING_TYPE": "EFILE", "TAX_PERIOD": "202309", "SUB_DATE": "2024", "RETURN_TYPE": "990", "DLN": "93493164002154", "OBJECT_ID": "202401649349300215", "XML_BATCH_ID": "2024_TEOS_XML_06a", "_release_year": 2024}
  - {"RETURN_ID": "23842749", "FILING_TYPE": "EFILE", "TAX_PERIOD": "202409", "SUB_DATE": "2025", "RETURN_TYPE": "990", "DLN": "93493216004195", "OBJECT_ID": "202542169349300419", "XML_BATCH_ID": "2025_TEOS_XML_08A", "_release_year": 2025}
  - {"RETURN_ID": "", "FILING_TYPE": "EFILE", "TAX_PERIOD": "202509", "SUB_DATE": "2026", "RETURN_TYPE": "990", "DLN": "93493153008486", "OBJECT_ID": "202631539349300848", "XML_BATCH_ID": "2026_TEOS_XML_06A", "_release_year": 2026}

### 2026-10-10 12:23 — 01_inventory_inputs
- sources/input_inventory.csv: 25 rows (duplicate=1, ok=19, partial=4, unreadable=1)
- registered 25 input_* sources
- period checks: all match

### 2026-10-10 12:24 — 16_probe_context: census
- ACS 5-year vintage probe (dataset metadata HTTP): 2026:404, 2025:404, 2024:200 -> latest 2024
- Census data API: ok; keyless HTTP 302 -> https://api.census.gov/data/missing_key.html; keyed HTTP 200
- variables.json: raw/census/20261010T122307_acs5_2024_variables.json (new)
- wrote config/acs_variables.csv: 65 variables
- ACS 2024 group pulls: 99 new, 0 reused, 0 failed (11 groups x 9 geographies)
- B01003 row counts by geography: us=1, states=4, cbsa47900=1, dc_wards_sldu=8, dc_tracts=206, counties_dc=1, counties_md=24, counties_va=133, counties_wv037=1
- Summary File 2024 5YR keyless listing ok; table files (national, all summary levels incl. tract 140, ward/SLDU 610, CBSA 310): B01003=17M, B03002=79M, B09019=57M, B11001=44M, B17001=113M, B17012=66M, B18101=82M, B19013=17M, B21001=145M, B23025=38M, B25070=44M
- 2020 PL blocks DC: 6012 rows (new)
- 2022 SLDU BEF 11_DC_SLDU22.txt: 6012 rows (new)

### 2026-10-10 12:24 — 16_probe_context: geo
- DC wards 2022: 8 features -> raw/geo/20261010T122409_dcgis_wards_2022.geojson
- TIGERweb DC tracts: 206 -> raw/geo/20261010T122411_tigerweb_acs2024_tracts_dc.geojson
- DC OP ACS ward layers: demographic_dp05 2020-2024 (8 rows); economic_dp03 2020-2024 (8 rows); housing_dp04 2020-2024 (8 rows); social_dp02 2020-2024 (8 rows)
- DC Open Data search for tract-ward crosswalk: none found
- crosswalk check: 6012 blocks, 6012 BEF rows, 0 blocks without ward
- 206 tracts; 12 span >1 ward (pop>0); 9 have <95% of pop in one ward
- 2020 pop by ward (blocks via BEF): W1=85,285, W2=89,485, W3=85,301, W4=84,660, W5=89,617, W6=84,266, W7=85,685, W8=85,246
- tract internal-point method vs block-majority ward: 202 agree, 4 differ
- Calvary tract 11001007503 ward pop split: {8: 2528}
- ACS 2024 B01003 ward (SLDU) vs tract-allocated: W1 sldu=81,010 alloc=81,524; W2 sldu=80,347 alloc=79,905; W3 sldu=81,004 alloc=81,090; W4 sldu=85,682 alloc=85,688; W5 sldu=90,611 alloc=90,461; W6 sldu=84,376 alloc=84,853; W7 sldu=90,540 alloc=90,249; W8 sldu=87,724 alloc=87,524

### 2026-10-10 12:24 — 16_probe_context: geocode
- MAR 2 API: blocked_needs_key (HTTP 500: API Key is required.)
- DC GIS Address Points: 1217 MARION BARRY AVENUE SE: Ward 8, SMD 8A06, ANC 8A, lat 38.86708202, lon -76.98804548, MAR_ID 338288; no tract field
- Census Geocoder single: 3/4 matched; batch: 3/4 matched; calvary_new_name: no match | calvary_old_name: county 11001, tract 11001007503, SLDU Ward 8 | md_shepherds_table: county 24031, tract 24031702501, SLDU State Senate District 20 | va_carpenters_shelter: county 51510, tract 51510201602, SLDU State Senate District 39

### 2026-10-10 12:24 — 16_probe_context: omb
- OMB list1_2023 (new): CBSA 47900 23 rows {'DC': 1, 'MD': 4, 'VA': 17, 'WV': 1} -> config/dmv_counties.csv

### 2026-10-10 12:24 — 10_probe_filings: propublica
- org 521307706: HTTP 200; filings_with_data 13 (tax_prd 201109-202309); filings_without_data 11 (tax_prd [200109, 200209, 200309, 200409, 200509, 200609, 200709, 200809, 200909, 201009, 202409]); latest_object_id 202631539349300848; org.tax_period 2025-09-01; data_source current_2026_09_16
- per-filing fields (68): compnsatncurrofcr, cstbasisecur, cstbasisothr, ein, formtype, gftgrntsrcvd170, gnlsecur, gnlsothr, grsalesecur, grsalesinvent, grsalesothr, grsinc170, grsincfndrsng, grsincgaming, grsincmembers, grsincother, grsrcptsadmissn509, grsrcptspublicuse, grsrcptsrelated170, grsrntsprsnl, grsrntsreal, initiationfees, invstmntinc, lesscstofgoods, lessdirfndrsng, lessdirgaming, miscrevtot11e, netgnls, netincfndrsng, netincgaming, netincsales, netrntlinc, nonpfrea, othrsalwages, payrolltx, pct_compnsatncurrofcr, pdf_url, profndraising, retainedearnend, rntlexpnsprsnl, rntlexpnsreal, rntlincprsnl, rntlincreal, royaltsinc, secrdmrtgsend, srvcsval170, srvcsval509, subseccd, subtotsuppinc509, tax_pd, tax_prd, tax_prd_yr, totassetsend, totcntrbgfts, totfuncexpns, totgftgrntrcvd509, totliabend, totnetassetend, totprgmrevnue, totrevenue, totsupp509, txexmptbndsend, txexmptbndsproceeds, txrevnuelevied170, txrevnuelevied509, unrelbusinccd, unsecurednotesend, updated
- Calvary series (tax_prd -> totrevenue / totfuncexpns / totassetsend): 201109: 1445107 / 1065764 / 2202464; 201209: 2021027 / 1144102 / 3829682; 201309: 1886681 / 1464641 / 4161470; 201409: 2072635 / 1705571 / 4277367; 201509: 2008601 / 1879006 / 4350228; 201609: 1990443 / 1989199 / 4280011; 201709: 2259177 / 2076427 / 4371584; 201809: 2153899 / 2152260 / 4345403; 201909: 2486678 / 2403977 / 4371143; 202009: 3896046 / 3215728 / 5071477; 202109: 3851984 / 3334967 / 5588973; 202209: 8867250 / 4550205 / 10214831; 202309: 4456814 / 5130964 / 10374467
- object_id keys in filings: none; pdf_url present on 12/13
- search_dc_ntee5_p0: HTTP 200, total_results 3069, num_pages 123, returned 25
- search_dc_ntee5_c3_p0: HTTP 200, total_results 2824, num_pages 113, returned 25
- search_md_ntee5_c3_p0: HTTP 200, total_results 10000, num_pages 400, returned 25
- search_va_ntee5_c3_p0: HTTP 200, total_results 10000, num_pages 400, returned 25
- search_dc_all_p0: HTTP 200, total_results 10000, num_pages 400, returned 25
- search_dc_all_p399: HTTP 200, total_results 10000, num_pages 400, returned 25
- search_dc_all_p400: HTTP 400, total_results None, num_pages None, returned 0, error 'Pagination out of range'
- search_q_calvary_dc: HTTP 200, total_results 14, num_pages 1, returned 14
- search_q_women_dc_ntee5_c3: HTTP 200, total_results 49, num_pages 2, returned 25
- search record fields: ein, strein, name, sub_name, city, state, ntee_code, raw_ntee_code, subseccd, has_subseccd, have_filings, have_extracts, have_pdfs, score (no financials; per-org call needed)
- paged DC ntee[id]=5 pages 0..123: 3,069 distinct EINs vs total_results 3,069
- org 530241716 (Eugene & Agnes E Meyer Foundation): 10 with data, latest tax_prd 202312, formtype 2, 126 fields
- org 526036989 (Morris And Gwendolyn Cafritz Foundation): 12 with data, latest tax_prd 202404, formtype 2, 126 fields
- org 520781600: HTTP 404
- download-xml?object_id=...: HTTP 403, cf-mitigated=challenge (Cloudflare browser challenge; not scriptable)
- rate: 137 requests, status {200: 134, 400: 1, 404: 1, 403: 1}, cf-cache-status {'HIT': 131, 'MISS': 5, '-': 1}, latency median 0.04s p90 0.11s max 1.55s

### 2026-10-10 12:24 — 16_probe_context: cpi
- BLS v2 keyless: 3 requests; US annual avg 2000-2025; DC metro 2015-2025; 2025 annual average published: True (321.943); keyless (10-year windows); messages: ['No Data Available for Series CUUSS35ASA0 Year: 2000', 'No Data Available for Series CUUSS35ASA0 Year: 2001', 'No Data Available for Series CUUSS35ASA0 Year: 2002']
- wrote config/cpi_u_annual.csv (26 US years, base 2024: US 313.689, DC 315.186)
- FRED fredgraph.csv: failed ReadTimeout (connection reset/timeout from this host)

### 2026-10-10 12:24 — 16_probe_context: catalog
- wrote sources/catalog_parts/context.csv
- statuses: acs=ok, sf=ok, pl=ok, bef=ok, wards=ok, tiger=ok, opward=ok, xwalk=ok, mar2=blocked_needs_key, addrpts=ok, geocoder=ok, omb=ok, bls=ok, fred=failed

### 2026-10-10 12:24 — 10_probe_filings: gt
- irs-data/efilexml?ein=521307706: HTTP 200, no_results 7
- irs-data/990basic120fields?ein=521307706: HTTP 200, no_results 8
- irs-data/bmf?ein=521307706: HTTP 200, no_results 1
- irs-data/postcard?ein=521307706: HTTP 200, no_results 0
- irs-data/pub78-deductible?ein=521307706: HTTP 200, no_results 1
- irs-data/revoked?ein=521307706: HTTP 200, no_results 0
- probe docs_path_irs_data_underscore (irs_data/efilexml {'ein': '521307706'}): HTTP 403, Missing Authentication Token
- probe no_ein (irs-data/990basic120fields {}): HTTP 400, Missing required request parameters: [ein]
- probe state_filter_only (irs-data/990basic120fields {'state': 'DC'}): HTTP 400, Missing required request parameters: [ein]
- probe two_eins_comma (irs-data/990basic120fields {'ein': '521307706,530241716'}): HTTP 200, Your EIN should be 9 digits long with no hyphens. i.e 123456789 not 12-3456789 We recommend adding zeros if the ein is t
- probe taxyear_param_ignored (irs-data/990basic120fields {'ein': '521307706', 'taxyear': '2021'}): HTTP 200, no_results 8
- probe undocumented_990pf (irs-data/990pf {'ein': '521307706'}): HTTP 403, Missing Authentication Token
- efilexml TaxYear set: ['2014', '2015', '2016', '2017', '2018', '2019', '2020']; IndexedOn max 2023-11-19; columns: id, BuildTs, DAF, DateSigned, DocStatus, EIN, FileSha256, FileSizeBytes, FormType, GrossReceipts, GroupAffiliatesIncluded, GroupExemptionNumber, GroupReturnForAffiliates, IndexedOn, LegalDomicileCountry, LegalDomicileState, ObjectId, OrgType, OrganizationName, ReturnTs, ReturnVersion, SubmittedOn, TaxPeriod, TaxPeriodBeginDate, TaxPeriodEndDate, TaxStatus, TaxYear, TotalAssetsBkEOY, TotalExpensesCY, TotalLiabilitiesBkEOY, TotalNetAssetsBkEOY, TotalRevenueCY, URL, Website, YearFormed, ZipFile
- 990basic120fields TAXYEAR set: ['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021']; 117 columns; rows with URL: 6; TY2021 TOTREVCURYEA ['8867250']
- bmf: Date_Released 2024_02_13, tax_period 202209 (stale vs IRS BMF)
- XML TY2014 201600959349300900 (2014v6.0): 46,911 B, sha256 matches -> raw/xml/gt/20261010T122336_521307706_TY2014_201600959349300900_public.xml
- XML TY2015 201731189349300503 (2015v3.0): 46,924 B, sha256 matches -> raw/xml/gt/20261010T122336_521307706_TY2015_201731189349300503_public.xml
- XML TY2016 201801039349300220 (2016v3.0): 46,480 B, sha256 matches -> raw/xml/gt/20261010T122336_521307706_TY2016_201801039349300220_public.xml
- XML TY2017 201910249349300501 (2017v2.3): 48,631 B, sha256 matches -> raw/xml/gt/20261010T122336_521307706_TY2017_201910249349300501_public.xml
- XML TY2018 202010389349301241 (2018v3.1): 46,326 B, sha256 matches -> raw/xml/gt/20261010T122337_521307706_TY2018_202010389349301241_public.xml
- XML TY2019 202130449349300208 (2019v5.2): 45,792 B, sha256 matches -> raw/xml/gt/20261010T122337_521307706_TY2019_202130449349300208_public.xml
- XML TY2020 202212279349301511 (2020v4.2): 51,469 B, sha256 matches -> raw/xml/gt/20261010T122337_521307706_TY2020_202212279349301511_public.xml
- data lake Indices/990xmls/: 250 objects; latest yearly build 2026-08-25: 2007 0.0 MB, 2008 0.1 MB, 2009 22.4 MB, 2010 92.2 MB, 2011 120.3 MB, 2012 136.5 MB, 2013 142.8 MB, 2014 171.9 MB, 2015 184.6 MB, 2016 193.4 MB, 2017 207.7 MB, 2018 221.1 MB, 2019 231.6 MB, 2020 286.3 MB, 2021 298.7 MB, 2022 304.0 MB, 2023 310.1 MB, 2024 267.6 MB, 2025 78.2 MB
- data lake EfileData/XmlZips/: 103 ZIPs, latest modified 2026-08-25
- GT S3 XmlFiles 202130449349300208 (TAX_PERIOD 202009): HTTP 200, 45,792 B, Last-Modified Sat, 28 Oct 2023 01:06:56 GMT
- GT S3 XmlFiles 202212279349301511 (TAX_PERIOD 202109): HTTP 200, 51,469 B, Last-Modified Sat, 28 Oct 2023 00:26:53 GMT
- GT S3 XmlFiles 202322239349302102 (TAX_PERIOD 202209): HTTP 200, 55,842 B, Last-Modified Sat, 27 Sep 2025 00:37:35 GMT
- GT S3 XmlFiles 202401649349300215 (TAX_PERIOD 202309): HTTP 200, 57,566 B, Last-Modified Tue, 23 Jul 2024 17:01:10 GMT
- GT S3 XmlFiles 202542169349300419 (TAX_PERIOD 202409): HTTP 200, 55,565 B, Last-Modified Sat, 27 Sep 2025 13:54:05 GMT
- GT S3 XmlFiles 202631539349300848 (TAX_PERIOD 202509): HTTP 200, 54,115 B, Last-Modified Tue, 25 Aug 2026 09:26:19 GMT
- GT S3 per-object coverage, random 40 990/EZ/PF rows per IRS index release year: 2021: 40/40, 2022: 40/40, 2023: 40/40, 2024: 40/40, 2025: 40/40, 2026: 26/40
- API rate: 12 requests, status {200: 8, 403: 2, 400: 2}, cf-cache-status {'-': 12}, latency median 0.05s p90 0.08s max 0.13s

### 2026-10-10 12:25 — 10_probe_filings: soi
- 49 files on page, year labels 12-24
  - 12eofinextract990.zip: 17.9 MB (HTTP 200, Thu, 01 Jan 1970 00:00:00 GMT)
  - 12eofinextract990ez.zip: 9.3 MB (HTTP 200, Fri, 07 Nov 2025 08:57:53 GMT)
  - 12eofinextract990pf.zip: 8.8 MB (HTTP 200, Thu, 01 Jan 1970 00:00:00 GMT)
  - 12eofinextractdoc.xls: 0.1 MB (HTTP 200, Mon, 01 Apr 2013 14:30:00 GMT)
  - 13eofinextract990.zip: 47.3 MB (HTTP 200, Mon, 31 Mar 2014 17:10:29 GMT)
  - 13eofinextract990ez.zip: 11.1 MB (HTTP 200, Fri, 07 Nov 2025 08:57:56 GMT)
  - 13eofinextract990pf.zip: 10.8 MB (HTTP 200, Thu, 01 Jan 1970 00:00:00 GMT)
  - 13eofinextractdoc.xls: 0.1 MB (HTTP 200, Tue, 25 Mar 2014 15:42:27 GMT)
  - 14eofinextract990.zip: 48.5 MB (HTTP 200, Fri, 17 Apr 2015 14:48:59 GMT)
  - 14eofinextract990ez.zip: 11.7 MB (HTTP 200, Fri, 07 Nov 2025 08:57:58 GMT)
  - 14eofinextract990pf.zip: 11.0 MB (HTTP 200, Fri, 07 Nov 2025 08:57:58 GMT)
  - 14eofinextractdoc.xls: 0.1 MB (HTTP 200, Thu, 01 Jan 1970 00:00:00 GMT)
  - 15eofinextract990.zip: 48.4 MB (HTTP 200, Fri, 11 Jul 2025 18:10:05 GMT)
  - 15eofinextract990pf.zip: 11.3 MB (HTTP 200, Fri, 11 Jul 2025 18:10:07 GMT)
  - 15eofinextractEZ.zip: 11.0 MB (HTTP 200, Fri, 11 Jul 2025 18:10:08 GMT)
  - 15eofinextractdoc.xls: 0.1 MB (HTTP 200, Tue, 26 Apr 2016 18:27:41 GMT)
  - 16eofinextract990.zip: 50.7 MB (HTTP 200, Fri, 11 Jul 2025 18:10:10 GMT)
  - 16eofinextract990pf.zip: 11.6 MB (HTTP 200, Fri, 11 Jul 2025 18:10:12 GMT)
  - 16eofinextractdoc.xls: 0.1 MB (HTTP 200, Thu, 01 Jan 1970 00:00:00 GMT)
  - 16eofinextractez.zip: 11.6 MB (HTTP 200, Fri, 11 Jul 2025 18:10:13 GMT)
  - 17eofinextract990.zip: 49.8 MB (HTTP 200, Fri, 11 Jul 2025 18:10:15 GMT)
  - 17eofinextractEZ.zip: 11.1 MB (HTTP 200, Fri, 11 Jul 2025 18:10:17 GMT)
  - 17eofinextractdoc.xls: 0.1 MB (HTTP 200, Fri, 07 Nov 2025 08:57:10 GMT)
  - 18eoextract990.zip: 50.7 MB (HTTP 200, Fri, 11 Jul 2025 18:10:19 GMT)
  - 18eoextractez.zip: 11.6 MB (HTTP 200, Fri, 11 Jul 2025 18:10:20 GMT)
  - 18eofinextractdoc.xlsx: 0.0 MB (HTTP 200, Fri, 07 Nov 2025 08:57:09 GMT)
  - 19eoextract990.zip: 51.2 MB (HTTP 200, Fri, 11 Jul 2025 18:10:22 GMT)
  - 19eoextractez.zip: 11.2 MB (HTTP 200, Fri, 11 Jul 2025 18:10:24 GMT)
  - 19eofinextractdoc.xlsx: 0.0 MB (HTTP 200, Wed, 27 May 2020 02:14:51 GMT)
  - 20eoextract990.zip: 46.5 MB (HTTP 200, Fri, 11 Jul 2025 18:10:25 GMT)
  - 20eoextract990pf.zip: 10.3 MB (HTTP 200, Fri, 11 Jul 2025 18:10:27 GMT)
  - 20eoextractez.zip: 8.1 MB (HTTP 200, Fri, 11 Jul 2025 18:10:27 GMT)
  - 20eofinextractdoc.xlsx: 0.0 MB (HTTP 200, Tue, 22 Jun 2021 02:11:33 GMT)
  - 21eoextract990.zip: 54.8 MB (HTTP 200, Fri, 11 Jul 2025 18:10:29 GMT)
  - 21eoextract990pf.zip: 13.6 MB (HTTP 200, Fri, 11 Jul 2025 18:10:31 GMT)
  - 21eoextractez.zip: 10.6 MB (HTTP 200, Fri, 11 Jul 2025 18:10:32 GMT)
  - 21eofinextractdoc.xlsx: 0.0 MB (HTTP 200, Thu, 30 Jun 2022 02:11:46 GMT)
  - 22eoextract990.zip: 53.3 MB (HTTP 200, Fri, 11 Jul 2025 18:10:33 GMT)
  - 22eoextract990pf.zip: 12.5 MB (HTTP 200, Fri, 11 Jul 2025 18:10:35 GMT)
  - 22eoextractez.zip: 11.1 MB (HTTP 200, Fri, 11 Jul 2025 18:10:36 GMT)
  - 22eofinextractdoc.xlsx: 0.0 MB (HTTP 200, Tue, 21 Nov 2023 03:10:48 GMT)
  - 23eoextract990.zip: 55.3 MB (HTTP 200, Fri, 11 Jul 2025 18:10:38 GMT)
  - 23eoextract990pf.zip: 13.0 MB (HTTP 200, Fri, 11 Jul 2025 18:10:39 GMT)
  - 23eoextractez.zip: 10.0 MB (HTTP 200, Fri, 11 Jul 2025 18:10:40 GMT)
  - 23eofinextractdoc.xlsx: 0.0 MB (HTTP 200, Tue, 30 Jul 2024 02:10:43 GMT)
  - 24eoextract990.zip: 56.7 MB (HTTP 200, Fri, 01 Aug 2025 02:10:14 GMT)
  - 24eoextract990EZ.zip: 9.9 MB (HTTP 200, Fri, 01 Aug 2025 02:10:16 GMT)
  - 24eoextract990pf.zip: 12.8 MB (HTTP 200, Fri, 01 Aug 2025 02:10:17 GMT)
  - 24eofinextractdoc.xlsx: 0.0 MB (HTTP 200, Fri, 01 Aug 2025 02:10:18 GMT)
- downloaded 24eoextract990.zip -> raw/irs_soi/20261010T122508_24eoextract990.zip sha256 dc3898cad200
  - member 24eoextract990.csv: 247.4 MB unzipped, 345,365 rows, 246 columns; tax period year mix {'2008': 3, '2009': 7, '2010': 6, '2011': 9, '2012': 13, '2013': 14, '2014': 29, '2015': 41, '2016': 46, '2017': 82, '2018': 180, '2019': 465, '2020': 854, '2021': 2264, '2022': 10153, '2023': 290029, '2024': 41170}
  - columns: efile, EIN, tax_pd, subseccd, s501c3or4947a1cd, schdbind, politicalactvtscd, lbbyingactvtscd, subjto6033cd, dnradvisedfundscd, prptyintrcvdcd, maintwrkofartcd, crcounselingqstncd, hldassetsintermpermcd, rptlndbldgeqptcd, rptinvstothsecd, rptinvstprgrelcd, rptothasstcd, rptothliabcd, sepcnsldtfinstmtcd, sepindaudfinstmtcd, inclinfinstmtcd, operateschools170cd, frgnofficecd, frgnrevexpnscd, frgngrntscd, frgnaggragrntscd, rptprofndrsngfeescd, rptincfnndrsngcd, rptincgamingcd, operatehosptlcd, hospaudfinstmtcd, rptgrntstogovtcd, rptgrntstoindvcd, rptyestocompnstncd, txexmptbndcd, invstproceedscd, maintescrwaccntcd, actonbehalfcd, engageexcessbnftcd, awarexcessbnftcd, loantofficercd, grantoofficercd, dirbusnreltdcd, fmlybusnreltdcd, servasofficercd, recvnoncashcd, recvartcd, ceaseoperationscd, sellorexchcd, ownsepentcd, reltdorgcd, intincntrlcd, orgtrnsfrcd, conduct5percentcd, compltschocd, f1096cnt, fw2gcnt, wthldngrulescd, noemplyeesw3cnt, filerqrdrtnscd, unrelbusinccd, filedf990tcd, frgnacctcd, prohibtdtxshltrcd, prtynotifyorgcd, filedf8886tcd, solicitcntrbcd, exprstmntcd, providegoodscd, notfydnrvalcd, filedf8282cd, f8282cnt, fndsrcvdcd, premiumspaidcd, filedf8899cd, filedf1098ccd, excbushldngscd, s4966distribcd, distribtodonorcd, initiationfees, grsrcptspublicuse, grsincmembers, grsincother, filedlieuf1041cd, txexmptint, qualhlthplncd, qualhlthreqmntn, qualhlthonhnd, rcvdpdtngcd, filedf720cd, totreprtabled, totcomprelatede, totestcompf, noindiv100kcnt, nocontractor100kcnt, totcntrbgfts, prgmservcode2acd, totrev2acola, prgmservcode2bcd, totrev2bcola, prgmservcode2ccd, totrev2ccola, prgmservcode2dcd, totrev2dcola, prgmservcode2ecd, totrev2ecola, totrev2fcola, totprgmrevnue, invstmntinc, txexmptbndsproceeds, royaltsinc, grsrntsreal, grsrntsprsnl, rntlexpnsreal, rntlexpnsprsnl, rntlincreal, rntlincprsnl, netrntlinc, grsalesecur, grsalesothr, cstbasisecur, cstbasisothr, gnlsecur, gnlsothr, netgnls, grsincfndrsng, lessdirfndrsng, netincfndrsng, grsincgaming, lessdirgaming, netincgaming, grsalesinvent, lesscstofgoods, netincsales, miscrev11acd, miscrevtota, miscrev11bcd, miscrevtot11b, miscrev11ccd, miscrevtot11c, miscrevtot11d, miscrevtot11e, totrevenue, grntstogovt, grnsttoindiv, grntstofrgngovt, benifitsmembrs, compnsatncurrofcr, compnsatnandothr, othrsalwages, pensionplancontrb, othremplyeebenef, payrolltx, feesforsrvcmgmt, legalfees, accntingfees, feesforsrvclobby, profndraising, feesforsrvcinvstmgmt, feesforsrvcothr, advrtpromo, officexpns, infotech, royaltsexpns, occupancy, travel, travelofpublicoffcl, converconventmtng, interestamt, pymtoaffiliates, deprcatndepletn, insurance, othrexpnsa, othrexpnsb, othrexpnsc, othrexpnsd, othrexpnse, othrexpnsf, totfuncexpns, nonintcashend, svngstempinvend, pldgegrntrcvblend, accntsrcvblend, currfrmrcvblend, rcvbldisqualend, notesloansrcvblend, invntriesalesend, prepaidexpnsend, lndbldgsequipend, invstmntsend, invstmntsothrend, invstmntsprgmend, intangibleassetsend, othrassetsend, totassetsend, accntspayableend, grntspayableend, deferedrevnuend, txexmptbndsend, escrwaccntliabend, paybletoffcrsend, secrdmrtgsend, unsecurednotesend, othrliabend, totliabend, unrstrctnetasstsend, temprstrctnetasstsend, permrstrctnetasstsend, capitalstktrstend, paidinsurplusend, retainedearnend, totnetassetend, totnetliabastend, nonpfrea, totnooforgscnt, totsupport, gftgrntsrcvd170, txrevnuelevied170, srvcsval170, pubsuppsubtot170, exceeds2pct170, pubsupplesspct170, samepubsuppsubtot170, grsinc170, netincunreltd170, othrinc170, totsupp170, grsrcptsrelated170, totgftgrntrcvd509, grsrcptsadmissn509, grsrcptsactivities509, txrevnuelevied509, srvcsval509, pubsuppsubtot509, rcvdfrmdisqualsub509, exceeds1pct509, subtotpub509, pubsupplesub509, samepubsuppsubtot509, grsinc509, unreltxincls511tx509, subtotsuppinc509, netincunrelatd509, othrinc509, totsupp509
  - Calvary row: {"efile": "E", "EIN": "521307706", "tax_pd": "202309", "subseccd": "03", "s501c3or4947a1cd": "Y", "schdbind": "Y", "totcntrbgfts": "4603409", "totprgmrevnue": "0", "totrevenue": "4456814", "totfuncexpns": "5130964", "totassetsend": "10374467", "totnetassetend": "8198649"}
- downloaded 24eoextract990pf.zip -> raw/irs_soi/20261010T122514_24eoextract990pf.zip sha256 f293695ca384
  - member 24eoextract990pf.csv: 58.7 MB unzipped, 119,059 rows, 180 columns; tax period year mix {'2007': 3, '2008': 1, '2009': 3, '2010': 1, '2011': 2, '2012': 6, '2013': 5, '2014': 4, '2015': 4, '2016': 13, '2017': 26, '2018': 90, '2019': 248, '2020': 587, '2021': 960, '2022': 3164, '2023': 103551, '2024': 10391}
  - columns: ELF, EIN, TAX_PRD, EOSTATUS, TAX_YR, OPERATINGCD, SUBCD, FAIRMRKTVALAMT, GRSCONTRGIFTS, SCHEDBIND, INTRSTRVNUE, DIVIDNDSAMT, GRSRENTS, GRSSLSPRAMT, COSTSOLD, GRSPROFITBUS, OTHERINCAMT, TOTRCPTPERBKS, COMPOFFICERS, PENSPLEMPLBENF, LEGALFEESAMT, ACCOUNTINGFEES, INTERESTAMT, DEPRECIATIONAMT, OCCUPANCYAMT, TRAVLCONFMTNGS, PRINTINGPUBL, TOPRADMNEXPNSA, CONTRPDPBKS, TOTEXPNSPBKS, EXCESSRCPTS, TOTRCPTNETINC, TOPRADMNEXPNSB, TOTEXPNSNETINC, NETINVSTINC, TRCPTADJNETINC, TOTEXPNSADJNET, ADJNETINC, TOPRADMNEXPNSD, TOTEXPNSEXEMPT, OTHRCASHAMT, INVSTGOVTOBLIG, INVSTCORPSTK, INVSTCORPBND, TOTINVSTSEC, MRTGLOANS, OTHRINVSTEND, OTHRASSETSEOY, TOTASSETSEND, MRTGNOTESPAY, OTHRLIABLTSEOY, TOTLIABEND, TFUNDNWORTH, FAIRMRKTVALEOY, TOTEXCAPGNLS, TOTEXCAPGN, TOTEXCAPLS, INVSTEXCISETX, SEC4940NOTXCD, SEC4940REDTXCD, SECT511TX, SUBTITLEATX, TOTAXPYR, ESTTAXCR, TXWITHLDSRC, TXPAIDF2758, ERRONBKUPWTHLD, ESTPNLTY, TAXDUE, OVERPAY, CRELAMT, INFLEG, ACTNOTPR, CHGNPRVRPTCD, FILEDF990TCD, CONTRACTNCD, FURNISHCPYCD, CLAIMSTATCD, CNTRBTRSTXYRCD, ACQDRINDRINTCD, ORGCMPLYPUBCD, FILEDLF1041IND, PROPEXCHCD, BRWLNDMNYCD, FURNGOODSCD, PAIDCMPNCD, TRANSFERCD, AGREMKPAYCD, EXCEPTACTSIND, PRIORACTVCD, UNDISTRINCCD, APPLYPROVIND, DIRINDIRINTCD, EXCESSHLDCD, INVSTJEXMPTCD, PREVJEXMPTCD, PROPGNDACD, IPUBELECTCD, GRNTINDIVCD, NCHRTYGRNTCD, NRELIGIOUSCD, EXCPTRANSIND, RFPRSNLBNFTIND, PYPRSNLBNFTIND, S4960_TX_PYMT_CD, TFAIRMRKTUNUSE, VALNCHARITASSETS, CMPMININVSTRET, DISTRIBAMT, UNDISTRIBINCYR, ADJNETINCCOLA, ADJNETINCCOLB, ADJNETINCCOLC, ADJNETINCCOLD, ADJNETINCTOT, QLFYDISTRIBA, QLFYDISTRIBB, QLFYDISTRIBC, QLFYDISTRIBD, QLFYDISTRIBTOT, VALASSETSCOLA, VALASSETSCOLB, VALASSETSCOLC, VALASSETSCOLD, VALASSETSTOT, QLFYASSETA, QLFYASSETB, QLFYASSETC, QLFYASSETD, QLFYASSETTOT, ENDWMNTSCOLA, ENDWMNTSCOLB, ENDWMNTSCOLC, ENDWMNTSCOLD, ENDWMNTSTOT, TOTSUPRTCOLA, TOTSUPRTCOLB, TOTSUPRTCOLC, TOTSUPRTCOLD, TOTSUPRTTOT, PUBSUPRTCOLA, PUBSUPRTCOLB, PUBSUPRTCOLC, PUBSUPRTCOLD, PUBSUPRTTOT, GRSINVSTINCA, GRSINVSTINCB, GRSINVSTINCC, GRSINVSTINCD, GRSINVSTINCTOT, GRNTAPPRVFUT, PROGSRVCACOLD, PROGSRVCACOLE, PROGSRVCBCOLD, PROGSRVCBCOLE, PROGSRVCCCOLD, PROGSRVCCCOLE, PROGSRVCDCOLD, PROGSRVCDCOLE, PROGSRVCECOLD, PROGSRVCECOLE, PROGSRVCFCOLD, PROGSRVCFCOLE, PROGSRVCGCOLD, PROGSRVCGCOLE, MEMBERSHPDUESD, MEMBERSHPDUESE, INTONSVNGSD, INTONSVNGSE, DVDNDSINTD, DVDNDSINTE, TRNSFRCASHCD, TRNSOTHASSTSCD, SALESASSTSCD, PRCHSASSTSCD, RENTLSFACLTSCD, REIMBRSMNTSCD, LOANSGUARCD, PERFSERVICESCD, SHARNGASSTSCD
- downloaded 24eofinextractdoc.xlsx -> raw/irs_soi/20261010T122515_24eofinextractdoc.xlsx sha256 80319c89b3a8

### 2026-10-10 12:25 — 10_probe_filings: pages
- nccs_catalogs_index: HTTP 200, 77,545 B
- nccs_catalog_core: HTTP 200, 386,478 B
- nccs_catalog_efile: HTTP 200, 372,672 B
- nccs_catalog_bmf: HTTP 200, 216,509 B
- nccs_datasets: HTTP 200, 47,029 B
- charitynavigator_graphql_api: HTTP 200, 172,664 B
- charitynavigator_developer: HTTP 200, 34,294 B
- gt_api_access_page: HTTP 200, 145,714 B
- gt_datalake_page: HTTP 200, 148,935 B
- HEAD processed_merged/core/2024/990combined/core_2024_990combined.csv: HTTP 200, 18.8 MB, Wed, 20 May 2026 20:18:17 GMT
- HEAD processed/core/2024/990/core_2024_990.csv: HTTP 200, 40.6 MB, Wed, 20 May 2026 15:31:29 GMT
- HEAD processed_merged/core/2023/990pf/core_2023_990pf.csv: HTTP 200, 82.4 MB, Wed, 20 May 2026 20:18:16 GMT
- HEAD geocoding/unified-bmf/latest/bmf_unified_geocoded.csv: HTTP 200, 3,593.1 MB, Mon, 21 Sep 2026 12:40:54 GMT
- HEAD parsed/F9-P08-T00-REVENUE-2022.csv: HTTP 200, 69.5 MB, Sat, 02 Mar 2024 18:22:59 GMT
- HEAD parsed/F9-P08-T00-REVENUE-2023.csv: HTTP 404, 0.0 MB, 
- HEAD parsed/SI-P02-T00-GRANTS-US-ORGS-GOVTS-2022.csv: HTTP 200, 35.9 MB, Sat, 02 Mar 2024 18:58:37 GMT
- NCCS core_2024_990combined header (66 cols): ein,efile_indicator,excess_benefit_transaction_cd,excess_over_1pct_sec509,excess_over_2pct_sec170,filed_form_990t_cd,gifts_grants_received_sec170,gross_sales_inventory,gross_income_interest_sec170,gross_income_interest_sec509,gross_income_fundraising_events,gross_income_gaming_activities,gross_receipts_related_activities_sec509,gross_receipts_admissions_sec509,gross_receipts_public_use,gross_receipts_related_activities_sec170,initiation_fees,investment_income,cost_of_goods_sold,loan_to_interested_person_cd,other_revenue_total_11e,net_income_fundraising_events,net_income_inventory_sales,net_ubi
- Charity Navigator GraphQL keyless POST: HTTP 401 '{\n  "type": "https://httpproblems.com/http-status/401",\n  "title": "Unauthorized",\n  "status": 401,\n  "detail": "No Auth'

### 2026-10-10 12:25 — 10_probe_filings: remotezip
- 51 ZIP names for 2021-2026 (downloads page + index batch ids); 51 reachable (HTTP 200, Accept-Ranges); not reachable: none
  - 2021: 1 ZIPs, 3.72 GB, 589,904 members, central directories 55.5 MB
  - 2022: 1 ZIPs, 2.60 GB, 433,529 members, central directories 41.2 MB
  - 2023: 12 ZIPs, 4.29 GB, 705,154 members, central directories 65.6 MB
  - 2024: 12 ZIPs, 4.39 GB, 728,719 members, central directories 67.8 MB
  - 2025: 16 ZIPs, 4.46 GB, 748,906 members, central directories 56.2 MB
  - 2026: 9 ZIPs, 2.56 GB, 436,239 members, central directories 32.7 MB
  - 2021_TEOS_XML_01A: 3,715.5 MB, 589,904 members, CD 55.5 MB, Thu, 06 Mar 2025 20:08:25 GMT, page
  - 2022_TEOS_XML_01A: 2,603.7 MB, 433,529 members, CD 41.2 MB, Thu, 06 Mar 2025 20:08:56 GMT, page
  - 2023_TEOS_XML_01A: 123.1 MB, 21,513 members, CD 2.0 MB, Thu, 06 Mar 2025 17:04:40 GMT, page
  - 2023_TEOS_XML_02A: 234.6 MB, 40,304 members, CD 3.7 MB, Thu, 06 Mar 2025 17:07:26 GMT, page
  - 2023_TEOS_XML_03A: 197.2 MB, 36,224 members, CD 3.4 MB, Thu, 06 Mar 2025 17:06:19 GMT, page
  - 2023_TEOS_XML_04A: 244.5 MB, 42,995 members, CD 4.0 MB, Thu, 06 Mar 2025 17:07:59 GMT, page
  - 2023_TEOS_XML_05A: 990.5 MB, 156,228 members, CD 14.5 MB, Thu, 06 Mar 2025 17:27:59 GMT, page
  - 2023_TEOS_XML_06A: 163.7 MB, 29,240 members, CD 2.7 MB, Thu, 06 Mar 2025 17:05:35 GMT, page
  - 2023_TEOS_XML_07A: 219.9 MB, 38,027 members, CD 3.5 MB, Thu, 06 Mar 2025 17:07:06 GMT, page
  - 2023_TEOS_XML_08A: 266.2 MB, 42,301 members, CD 3.9 MB, Thu, 06 Mar 2025 17:08:23 GMT, page
  - 2023_TEOS_XML_09A: 200.4 MB, 35,070 members, CD 3.3 MB, Thu, 06 Mar 2025 17:06:29 GMT, page
  - 2023_TEOS_XML_10A: 332.5 MB, 56,858 members, CD 5.3 MB, Thu, 06 Mar 2025 17:10:21 GMT, page
  - 2023_TEOS_XML_11A: 1,200.3 MB, 186,387 members, CD 17.3 MB, Thu, 06 Mar 2025 17:32:53 GMT, page
  - 2023_TEOS_XML_12A: 120.7 MB, 20,007 members, CD 1.9 MB, Thu, 06 Mar 2025 17:04:34 GMT, page
  - 2024_TEOS_XML_01A: 104.8 MB, 17,246 members, CD 1.6 MB, Thu, 06 Mar 2025 14:04:31 GMT, page
  - 2024_TEOS_XML_02A: 243.7 MB, 40,284 members, CD 3.7 MB, Thu, 06 Mar 2025 14:04:23 GMT, page
  - 2024_TEOS_XML_03A: 209.3 MB, 38,418 members, CD 3.6 MB, Thu, 06 Mar 2025 14:04:55 GMT, page
  - 2024_TEOS_XML_04A: 350.3 MB, 59,487 members, CD 5.5 MB, Thu, 06 Mar 2025 14:05:02 GMT, page
  - 2024_TEOS_XML_05A: 977.5 MB, 156,237 members, CD 14.5 MB, Thu, 06 Mar 2025 14:05:40 GMT, page
  - 2024_TEOS_XML_06A: 163.9 MB, 29,408 members, CD 2.7 MB, Thu, 06 Mar 2025 14:04:01 GMT, page
  - 2024_TEOS_XML_07A: 288.3 MB, 50,144 members, CD 4.7 MB, Thu, 06 Mar 2025 14:04:23 GMT, page
  - 2024_TEOS_XML_08A: 260.6 MB, 41,687 members, CD 3.9 MB, Thu, 06 Mar 2025 14:04:56 GMT, page
  - 2024_TEOS_XML_09A: 247.0 MB, 44,108 members, CD 4.1 MB, Thu, 06 Mar 2025 14:04:54 GMT, page
  - 2024_TEOS_XML_10A: 251.6 MB, 43,392 members, CD 4.0 MB, Thu, 06 Mar 2025 14:04:55 GMT, page
  - 2024_TEOS_XML_11A: 1,165.6 MB, 186,632 members, CD 17.4 MB, Thu, 06 Mar 2025 14:05:48 GMT, page
  - 2024_TEOS_XML_12A: 128.3 MB, 21,676 members, CD 2.0 MB, Thu, 06 Mar 2025 14:04:05 GMT, page
  - 2025_TEOS_XML_01A: 103.7 MB, 17,044 members, CD 1.3 MB, Wed, 05 Mar 2025 15:12:42 GMT, page
  - 2025_TEOS_XML_02A: 239.9 MB, 41,855 members, CD 3.1 MB, Wed, 19 Mar 2025 13:01:47 GMT, page
  - 2025_TEOS_XML_03A: 222.6 MB, 41,570 members, CD 3.1 MB, Wed, 16 Apr 2025 13:01:48 GMT, page
  - 2025_TEOS_XML_04A: 338.2 MB, 57,595 members, CD 4.3 MB, Wed, 21 May 2025 13:09:56 GMT, page
  - 2025_TEOS_XML_05A: 495.9 MB, 81,770 members, CD 6.1 MB, Wed, 25 Jun 2025 13:13:15 GMT, page
  - 2025_TEOS_XML_05B: 501.0 MB, 81,770 members, CD 6.1 MB, Wed, 25 Jun 2025 13:13:33 GMT, page
  - 2025_TEOS_XML_06A: 246.8 MB, 44,824 members, CD 3.4 MB, Wed, 20 Aug 2025 13:11:59 GMT, page
  - 2025_TEOS_XML_07A: 143.5 MB, 24,854 members, CD 1.9 MB, Wed, 20 Aug 2025 13:08:44 GMT, page
  - 2025_TEOS_XML_08A: 262.7 MB, 42,291 members, CD 3.2 MB, Wed, 17 Sep 2025 13:18:06 GMT, page
  - 2025_TEOS_XML_09A: 256.3 MB, 45,643 members, CD 3.4 MB, Wed, 19 Nov 2025 20:41:59 GMT, page
  - 2025_TEOS_XML_10A: 56.5 MB, 9,836 members, CD 0.7 MB, Wed, 19 Nov 2025 14:08:07 GMT, page
  - 2025_TEOS_XML_11A: 340.1 MB, 55,488 members, CD 4.2 MB, Wed, 17 Dec 2025 14:31:07 GMT, page
  - 2025_TEOS_XML_11B: 494.5 MB, 80,283 members, CD 6.0 MB, Wed, 17 Dec 2025 14:43:04 GMT, page
  - 2025_TEOS_XML_11C: 277.9 MB, 44,896 members, CD 3.4 MB, Wed, 17 Dec 2025 14:25:37 GMT, page
  - 2025_TEOS_XML_11D: 332.8 MB, 53,800 members, CD 4.0 MB, Wed, 17 Dec 2025 17:10:02 GMT, page
  - 2025_TEOS_XML_12A: 151.8 MB, 25,387 members, CD 1.9 MB, Wed, 21 Jan 2026 14:14:30 GMT, page
  - 2026_TEOS_XML_01A: 71.5 MB, 12,245 members, CD 0.9 MB, Thu, 19 Feb 2026 18:32:24 GMT, page
  - 2026_TEOS_XML_02A: 222.1 MB, 38,719 members, CD 2.9 MB, Wed, 18 Mar 2026 13:02:56 GMT, page
  - 2026_TEOS_XML_03A: 259.3 MB, 48,471 members, CD 3.6 MB, Wed, 15 Apr 2026 13:03:42 GMT, page
  - 2026_TEOS_XML_04A: 261.9 MB, 47,627 members, CD 3.6 MB, Wed, 20 May 2026 13:02:32 GMT, page
  - 2026_TEOS_XML_05A: 521.2 MB, 84,172 members, CD 6.3 MB, Wed, 17 Jun 2026 13:13:47 GMT, page
  - 2026_TEOS_XML_05B: 513.4 MB, 84,172 members, CD 6.3 MB, Wed, 17 Jun 2026 13:13:52 GMT, page
  - 2026_TEOS_XML_06A: 210.8 MB, 38,244 members, CD 2.9 MB, Wed, 15 Jul 2026 16:01:18 GMT, page
  - 2026_TEOS_XML_07A: 189.2 MB, 32,240 members, CD 2.4 MB, Wed, 19 Aug 2026 13:00:50 GMT, page
  - 2026_TEOS_XML_08A: 314.7 MB, 50,349 members, CD 3.8 MB, Wed, 16 Sep 2026 13:02:45 GMT, index_only
- remotezip 2026_TEOS_XML_06A (210.8 MB, 38,244 members, names like 202601429339300000_public.xml): central directory 2 requests / 2.9 MB; member 202631539349300848_public.xml 54,115 B (10,872 B compressed); total 3 requests / 2.9 MB = 1.40% of the ZIP; 0.5s -> raw/xml/irs/20261010T122536_521307706_TY2024_2026_TEOS_XML_06A_202631539349300848_public.xml
- 2026_TEOS_XML_06A: mean member 28.7 KB uncompressed, compression ratio 5.3x
- GT S3 copy of 202631539349300848 byte-identical to the IRS ZIP member: True

### 2026-10-10 12:25 — 10_probe_filings: volume
- BMF sets: (a) DMV PF filers (FOUNDATION 02/03/04 or PF_FILING_REQ_CD=1) 5,855 EINs; (b) DC 501(c)(3) public charities in NTEE L/P/F/I/J/W 1,750 EINs
- (a: DMV 990-PF filers) 25,367 returns from 5,249 EINs; by type {'990PF': 25367}; by tax year {2018: 22, 2019: 397, 2020: 3884, 2021: 4256, 2022: 4527, 2023: 4835, 2024: 4912, 2025: 2534}; by release year {2021: 3679, 2022: 4169, 2023: 4553, 2024: 4872, 2025: 5068, 2026: 3026}; same EIN+period+type repeats (amended/superseded) 213
  - ZIP batches: 49 distinct ZIPs touched (2021_TEOS_XML_01A 3679, 2022_TEOS_XML_01A 4169, 2023_ANY 4553, 2024_TEOS_XML_01A 72, 2024_TEOS_XML_02A 185, 2024_TEOS_XML_03A 195, 2024_TEOS_XML_04A 386, 2024_TEOS_XML_05A 1326, 2024_TEOS_XML_06A 182, 2024_TEOS_XML_07A 256, 2024_TEOS_XML_08A 258, 2024_TEOS_XML_09A 260, 2024_TEOS_XML_10A 240, 2024_TEOS_XML_11A 1407, 2024_TEOS_XML_12A 105, 2025_TEOS_XML_01A 69, 2025_TEOS_XML_02A 185, 2025_TEOS_XML_03A 274, 2025_TEOS_XML_04A 417, 2025_TEOS_XML_05A 1363, 2025_TEOS_XML_06A 283, 2025_TEOS_XML_07A 131, 2025_TEOS_XML_08A 186, 2025_TEOS_XML_09A 307, 2025_TEOS_XML_10A 43, 2025_TEOS_XML_11A 383, 2025_TEOS_XML_11B 568, 2025_TEOS_XML_11C 330, 2025_TEOS_XML_11D 416, 2025_TEOS_XML_12A 113, 2026_TEOS_XML_01A 42, 2026_TEOS_XML_02A 198, 2026_TEOS_XML_03A 327, 2026_TEOS_XML_04A 384, 2026_TEOS_XML_05A 1392, 2026_TEOS_XML_06A 219, 2026_TEOS_XML_07A 194, 2026_TEOS_XML_08A 270)
  - bytes: full ZIP downloads 21.0 GB; remotezip ~457 MB (central directories 306.4 MB + members ~150.5 MB compressed); GT S3 per-object ~802.0 MB uncompressed
- (b: DC public charities L/P/F/I/J/W) 4,580 returns from 968 EINs; by type {'990EZ': 670, '990': 3907, '990PF': 3}; by tax year {2018: 5, 2019: 215, 2020: 731, 2021: 812, 2022: 826, 2023: 883, 2024: 885, 2025: 223}; by release year {2021: 712, 2022: 783, 2023: 832, 2024: 874, 2025: 899, 2026: 480}; same EIN+period+type repeats (amended/superseded) 114
  - ZIP batches: 49 distinct ZIPs touched (2021_TEOS_XML_01A 712, 2022_TEOS_XML_01A 783, 2023_ANY 832, 2024_TEOS_XML_01A 16, 2024_TEOS_XML_02A 26, 2024_TEOS_XML_03A 39, 2024_TEOS_XML_04A 60, 2024_TEOS_XML_05A 133, 2024_TEOS_XML_06A 47, 2024_TEOS_XML_07A 45, 2024_TEOS_XML_08A 78, 2024_TEOS_XML_09A 50, 2024_TEOS_XML_10A 63, 2024_TEOS_XML_11A 299, 2024_TEOS_XML_12A 18, 2025_TEOS_XML_01A 12, 2025_TEOS_XML_02A 38, 2025_TEOS_XML_03A 30, 2025_TEOS_XML_04A 56, 2025_TEOS_XML_05A 142, 2025_TEOS_XML_06A 46, 2025_TEOS_XML_07A 28, 2025_TEOS_XML_08A 90, 2025_TEOS_XML_09A 53, 2025_TEOS_XML_10A 15, 2025_TEOS_XML_11A 91, 2025_TEOS_XML_11B 114, 2025_TEOS_XML_11C 85, 2025_TEOS_XML_11D 78, 2025_TEOS_XML_12A 21, 2026_TEOS_XML_01A 14, 2026_TEOS_XML_02A 34, 2026_TEOS_XML_03A 46, 2026_TEOS_XML_04A 54, 2026_TEOS_XML_05A 130, 2026_TEOS_XML_06A 51, 2026_TEOS_XML_07A 59, 2026_TEOS_XML_08A 92)
  - bytes: full ZIP downloads 21.0 GB; remotezip ~334 MB (central directories 306.4 MB + members ~27.2 MB compressed); GT S3 per-object ~144.9 MB uncompressed

### 2026-10-10 12:26 — 16_probe_context: docs
- wrote sources/catalog_parts/context.md (incl. Phase 4/5 design)
- appended 'Context recon' to notes_for_analysis.md and open_questions.md
- new package installed (not in requirements.txt): openpyxl 3.1.5 (+ et-xmlfile 2.0.0) for the OMB xlsx

### 2026-10-10 12:27 — 16_probe_context: geo
- DC wards 2022: 8 features -> raw/geo/20261010T122409_dcgis_wards_2022.geojson
- TIGERweb DC tracts: 206 -> raw/geo/20261010T122411_tigerweb_acs2024_tracts_dc.geojson
- DC OP ACS ward layers: demographic_dp05 2020-2024 (8 rows); economic_dp03 2020-2024 (8 rows); housing_dp04 2020-2024 (8 rows); social_dp02 2020-2024 (8 rows)
- DC Open Data search for tract-ward crosswalk: none found
- crosswalk check: 6012 blocks, 6012 BEF rows, 0 blocks without ward
- 206 tracts; 12 span >1 ward (pop>0); 9 have <95% of pop in one ward
- 2020 pop by ward (blocks via BEF): W1=85,285, W2=89,485, W3=85,301, W4=84,660, W5=89,617, W6=84,266, W7=85,685, W8=85,246
- tract internal-point method vs block-majority ward: 202 agree, 4 differ
- Calvary tract 11001007503 ward pop split: {8: 2528}
- ACS 2024 B01003 ward (SLDU) vs tract-allocated: W1 sldu=81,010 alloc=81,524; W2 sldu=80,347 alloc=79,905; W3 sldu=81,004 alloc=81,090; W4 sldu=85,682 alloc=85,688; W5 sldu=90,611 alloc=90,461; W6 sldu=84,376 alloc=84,853; W7 sldu=90,540 alloc=90,249; W8 sldu=87,724 alloc=87,524

### 2026-10-10 12:27 — 16_probe_context: catalog
- wrote sources/catalog_parts/context.csv
- statuses: wards=ok, tiger=ok, opward=ok, xwalk=ok

### 2026-10-10 12:27 — 16_probe_context: census
- ACS 5-year vintage probe (dataset metadata HTTP): 2026:404, 2025:404, 2024:200 -> latest 2024
- Census data API: ok; keyless HTTP 302 -> https://api.census.gov/data/missing_key.html; keyed HTTP 200
- variables.json: raw/census/20261010T122307_acs5_2024_variables.json (reused)
- wrote config/acs_variables.csv: 65 variables
- ACS 2024 group pulls: 0 new, 99 reused, 0 failed (11 groups x 9 geographies)
- B01003 row counts by geography: us=1, states=4, cbsa47900=1, dc_wards_sldu=8, dc_tracts=206, counties_dc=1, counties_md=24, counties_va=133, counties_wv037=1
- Summary File 2024 5YR keyless listing ok; table files (national, all summary levels incl. tract 140, ward/SLDU 610, CBSA 310): B01003=17M, B03002=79M, B09019=57M, B11001=44M, B17001=113M, B17012=66M, B18101=82M, B19013=17M, B21001=145M, B23025=38M, B25070=44M
- 2020 PL blocks DC: 6012 rows (reused)
- 2022 SLDU BEF 11_DC_SLDU22.txt: 6012 rows (reused)

### 2026-10-10 12:27 — 16_probe_context: geo
- DC wards 2022: 8 features -> raw/geo/20261010T122409_dcgis_wards_2022.geojson
- TIGERweb DC tracts: 206 -> raw/geo/20261010T122411_tigerweb_acs2024_tracts_dc.geojson
- DC OP ACS ward layers: demographic_dp05 2020-2024 (8 rows); economic_dp03 2020-2024 (8 rows); housing_dp04 2020-2024 (8 rows); social_dp02 2020-2024 (8 rows)
- DC Open Data search for tract-ward crosswalk: none found
- crosswalk check: 6012 blocks, 6012 BEF rows, 0 blocks without ward
- 206 tracts; 12 span >1 ward (pop>0); 9 have <95% of pop in one ward
- 2020 pop by ward (blocks via BEF): W1=85,285, W2=89,485, W3=85,301, W4=84,660, W5=89,617, W6=84,266, W7=85,685, W8=85,246
- tract internal-point method vs block-majority ward: 202 agree, 4 differ
- Calvary tract 11001007503 ward pop split: {8: 2528}
- ACS 2024 B01003 ward (SLDU) vs tract-allocated: W1 sldu=81,010 alloc=81,524; W2 sldu=80,347 alloc=79,905; W3 sldu=81,004 alloc=81,090; W4 sldu=85,682 alloc=85,688; W5 sldu=90,611 alloc=90,461; W6 sldu=84,376 alloc=84,853; W7 sldu=90,540 alloc=90,249; W8 sldu=87,724 alloc=87,524

### 2026-10-10 12:27 — 16_probe_context: geocode
- MAR 2 API: blocked_needs_key (HTTP 500: API Key is required.)
- DC GIS Address Points: 1217 MARION BARRY AVENUE SE: Ward 8, SMD 8A06, ANC 8A, lat 38.86708202, lon -76.98804548, MAR_ID 338288; no tract field
- Census Geocoder single: 3/4 matched; batch: 3/4 matched; calvary_new_name: no match | calvary_old_name: county 11001, tract 11001007503, SLDU Ward 8 | md_shepherds_table: county 24031, tract 24031702501, SLDU State Senate District 20 | va_carpenters_shelter: county 51510, tract 51510201602, SLDU State Senate District 39

### 2026-10-10 12:27 — 16_probe_context: omb
- OMB list1_2023 (reused): CBSA 47900 23 rows {'DC': 1, 'MD': 4, 'VA': 17, 'WV': 1} -> config/dmv_counties.csv

### 2026-10-10 12:27 — 16_probe_context: cpi
- BLS v2 keyless: 3 requests; US annual avg 2000-2025; DC metro 2015-2025; 2025 annual average published: True (321.943); keyless (10-year windows); messages: ['No Data Available for Series CUUSS35ASA0 Year: 2000', 'No Data Available for Series CUUSS35ASA0 Year: 2001', 'No Data Available for Series CUUSS35ASA0 Year: 2002']
- wrote config/cpi_u_annual.csv (26 US years, base 2024: US 313.689, DC 315.186)
- FRED fredgraph.csv: failed ReadTimeout (connection reset/timeout from this host)

### 2026-10-10 12:27 — 16_probe_context: catalog
- wrote sources/catalog_parts/context.csv
- statuses: acs=ok, sf=ok, pl=ok, bef=ok, wards=ok, tiger=ok, opward=ok, xwalk=ok, mar2=blocked_needs_key, addrpts=ok, geocoder=ok, omb=ok, bls=ok, fred=failed

### 2026-10-10 12:27 — 10_probe_filings: remotezip
- 52 ZIP names for 2021-2026 (downloads page + index batch ids); 52 reachable (HTTP 200, Accept-Ranges); not reachable: none
  - 2021: 1 ZIPs, 3.72 GB, 589,904 members, central directories 55.5 MB
  - 2022: 2 ZIPs, 4.01 GB, 656,503 members, central directories 62.6 MB
  - 2023: 12 ZIPs, 4.29 GB, 705,154 members, central directories 65.6 MB
  - 2024: 12 ZIPs, 4.39 GB, 728,719 members, central directories 67.8 MB
  - 2025: 16 ZIPs, 4.46 GB, 748,906 members, central directories 56.2 MB
  - 2026: 9 ZIPs, 2.56 GB, 436,239 members, central directories 32.7 MB
  - 2021_TEOS_XML_01A: 3,715.5 MB, 589,904 members, CD 55.5 MB, Thu, 06 Mar 2025 20:08:25 GMT, page
  - 2022_TEOS_XML_01A: 2,603.7 MB, 433,529 members, CD 41.2 MB, Thu, 06 Mar 2025 20:08:56 GMT, page
  - 2022_TEOS_XML_02A: 1,408.2 MB, 222,974 members, CD 21.4 MB, Thu, 06 Mar 2025 20:06:10 GMT, probe_only
  - 2023_TEOS_XML_01A: 123.1 MB, 21,513 members, CD 2.0 MB, Thu, 06 Mar 2025 17:04:40 GMT, page
  - 2023_TEOS_XML_02A: 234.6 MB, 40,304 members, CD 3.7 MB, Thu, 06 Mar 2025 17:07:26 GMT, page
  - 2023_TEOS_XML_03A: 197.2 MB, 36,224 members, CD 3.4 MB, Thu, 06 Mar 2025 17:06:19 GMT, page
  - 2023_TEOS_XML_04A: 244.5 MB, 42,995 members, CD 4.0 MB, Thu, 06 Mar 2025 17:07:59 GMT, page
  - 2023_TEOS_XML_05A: 990.5 MB, 156,228 members, CD 14.5 MB, Thu, 06 Mar 2025 17:27:59 GMT, page
  - 2023_TEOS_XML_06A: 163.7 MB, 29,240 members, CD 2.7 MB, Thu, 06 Mar 2025 17:05:35 GMT, page
  - 2023_TEOS_XML_07A: 219.9 MB, 38,027 members, CD 3.5 MB, Thu, 06 Mar 2025 17:07:06 GMT, page
  - 2023_TEOS_XML_08A: 266.2 MB, 42,301 members, CD 3.9 MB, Thu, 06 Mar 2025 17:08:23 GMT, page
  - 2023_TEOS_XML_09A: 200.4 MB, 35,070 members, CD 3.3 MB, Thu, 06 Mar 2025 17:06:29 GMT, page
  - 2023_TEOS_XML_10A: 332.5 MB, 56,858 members, CD 5.3 MB, Thu, 06 Mar 2025 17:10:21 GMT, page
  - 2023_TEOS_XML_11A: 1,200.3 MB, 186,387 members, CD 17.3 MB, Thu, 06 Mar 2025 17:32:53 GMT, page
  - 2023_TEOS_XML_12A: 120.7 MB, 20,007 members, CD 1.9 MB, Thu, 06 Mar 2025 17:04:34 GMT, page
  - 2024_TEOS_XML_01A: 104.8 MB, 17,246 members, CD 1.6 MB, Thu, 06 Mar 2025 14:04:31 GMT, page
  - 2024_TEOS_XML_02A: 243.7 MB, 40,284 members, CD 3.7 MB, Thu, 06 Mar 2025 14:04:23 GMT, page
  - 2024_TEOS_XML_03A: 209.3 MB, 38,418 members, CD 3.6 MB, Thu, 06 Mar 2025 14:04:55 GMT, page
  - 2024_TEOS_XML_04A: 350.3 MB, 59,487 members, CD 5.5 MB, Thu, 06 Mar 2025 14:05:02 GMT, page
  - 2024_TEOS_XML_05A: 977.5 MB, 156,237 members, CD 14.5 MB, Thu, 06 Mar 2025 14:05:40 GMT, page
  - 2024_TEOS_XML_06A: 163.9 MB, 29,408 members, CD 2.7 MB, Thu, 06 Mar 2025 14:04:01 GMT, page
  - 2024_TEOS_XML_07A: 288.3 MB, 50,144 members, CD 4.7 MB, Thu, 06 Mar 2025 14:04:23 GMT, page
  - 2024_TEOS_XML_08A: 260.6 MB, 41,687 members, CD 3.9 MB, Thu, 06 Mar 2025 14:04:56 GMT, page
  - 2024_TEOS_XML_09A: 247.0 MB, 44,108 members, CD 4.1 MB, Thu, 06 Mar 2025 14:04:54 GMT, page
  - 2024_TEOS_XML_10A: 251.6 MB, 43,392 members, CD 4.0 MB, Thu, 06 Mar 2025 14:04:55 GMT, page
  - 2024_TEOS_XML_11A: 1,165.6 MB, 186,632 members, CD 17.4 MB, Thu, 06 Mar 2025 14:05:48 GMT, page
  - 2024_TEOS_XML_12A: 128.3 MB, 21,676 members, CD 2.0 MB, Thu, 06 Mar 2025 14:04:05 GMT, page
  - 2025_TEOS_XML_01A: 103.7 MB, 17,044 members, CD 1.3 MB, Wed, 05 Mar 2025 15:12:42 GMT, page
  - 2025_TEOS_XML_02A: 239.9 MB, 41,855 members, CD 3.1 MB, Wed, 19 Mar 2025 13:01:47 GMT, page
  - 2025_TEOS_XML_03A: 222.6 MB, 41,570 members, CD 3.1 MB, Wed, 16 Apr 2025 13:01:48 GMT, page
  - 2025_TEOS_XML_04A: 338.2 MB, 57,595 members, CD 4.3 MB, Wed, 21 May 2025 13:09:56 GMT, page
  - 2025_TEOS_XML_05A: 495.9 MB, 81,770 members, CD 6.1 MB, Wed, 25 Jun 2025 13:13:15 GMT, page
  - 2025_TEOS_XML_05B: 501.0 MB, 81,770 members, CD 6.1 MB, Wed, 25 Jun 2025 13:13:33 GMT, page
  - 2025_TEOS_XML_06A: 246.8 MB, 44,824 members, CD 3.4 MB, Wed, 20 Aug 2025 13:11:59 GMT, page
  - 2025_TEOS_XML_07A: 143.5 MB, 24,854 members, CD 1.9 MB, Wed, 20 Aug 2025 13:08:44 GMT, page
  - 2025_TEOS_XML_08A: 262.7 MB, 42,291 members, CD 3.2 MB, Wed, 17 Sep 2025 13:18:06 GMT, page
  - 2025_TEOS_XML_09A: 256.3 MB, 45,643 members, CD 3.4 MB, Wed, 19 Nov 2025 20:41:59 GMT, page
  - 2025_TEOS_XML_10A: 56.5 MB, 9,836 members, CD 0.7 MB, Wed, 19 Nov 2025 14:08:07 GMT, page
  - 2025_TEOS_XML_11A: 340.1 MB, 55,488 members, CD 4.2 MB, Wed, 17 Dec 2025 14:31:07 GMT, page
  - 2025_TEOS_XML_11B: 494.5 MB, 80,283 members, CD 6.0 MB, Wed, 17 Dec 2025 14:43:04 GMT, page
  - 2025_TEOS_XML_11C: 277.9 MB, 44,896 members, CD 3.4 MB, Wed, 17 Dec 2025 14:25:37 GMT, page
  - 2025_TEOS_XML_11D: 332.8 MB, 53,800 members, CD 4.0 MB, Wed, 17 Dec 2025 17:10:02 GMT, page
  - 2025_TEOS_XML_12A: 151.8 MB, 25,387 members, CD 1.9 MB, Wed, 21 Jan 2026 14:14:30 GMT, page
  - 2026_TEOS_XML_01A: 71.5 MB, 12,245 members, CD 0.9 MB, Thu, 19 Feb 2026 18:32:24 GMT, page
  - 2026_TEOS_XML_02A: 222.1 MB, 38,719 members, CD 2.9 MB, Wed, 18 Mar 2026 13:02:56 GMT, page
  - 2026_TEOS_XML_03A: 259.3 MB, 48,471 members, CD 3.6 MB, Wed, 15 Apr 2026 13:03:42 GMT, page
  - 2026_TEOS_XML_04A: 261.9 MB, 47,627 members, CD 3.6 MB, Wed, 20 May 2026 13:02:32 GMT, page
  - 2026_TEOS_XML_05A: 521.2 MB, 84,172 members, CD 6.3 MB, Wed, 17 Jun 2026 13:13:47 GMT, page
  - 2026_TEOS_XML_05B: 513.4 MB, 84,172 members, CD 6.3 MB, Wed, 17 Jun 2026 13:13:52 GMT, page
  - 2026_TEOS_XML_06A: 210.8 MB, 38,244 members, CD 2.9 MB, Wed, 15 Jul 2026 16:01:18 GMT, page
  - 2026_TEOS_XML_07A: 189.2 MB, 32,240 members, CD 2.4 MB, Wed, 19 Aug 2026 13:00:50 GMT, page
  - 2026_TEOS_XML_08A: 314.7 MB, 50,349 members, CD 3.8 MB, Wed, 16 Sep 2026 13:02:45 GMT, index_only
  - release 2021: index rows 589,904 vs ZIP members 589,904 (diff +0)
  - release 2022: index rows 656,503 vs ZIP members 656,503 (diff +0)
  - release 2023: index rows 705,156 vs ZIP members 705,154 (diff -2)
  - release 2024: index rows 728,719 vs ZIP members 728,719 (diff +0)
  - release 2025: index rows 748,906 vs ZIP members 748,906 (diff +0)
  - release 2026: index rows 436,239 vs ZIP members 436,239 (diff +0)
  - 2025_TEOS_XML_05A vs 2025_TEOS_XML_05B: 81,770 / 81,770 object ids, overlap 0; index rows labelled 2025_TEOS_XML_05A: 163,540, found in 2025_TEOS_XML_05A 81,770, in 2025_TEOS_XML_05B 81,770 (read 12.4 MB of central directory)
  - 2026_TEOS_XML_05A vs 2026_TEOS_XML_05B: 84,172 / 84,172 object ids, overlap 0; index rows labelled 2026_TEOS_XML_05A: 168,344, found in 2026_TEOS_XML_05A 84,172, in 2026_TEOS_XML_05B 84,172 (read 12.8 MB of central directory)
- remotezip 2026_TEOS_XML_06A (210.8 MB, 38,244 members, names like 202601429339300000_public.xml): central directory 2 requests / 2.9 MB; member 202631539349300848_public.xml 54,115 B (10,872 B compressed); total 3 requests / 2.9 MB = 1.40% of the ZIP; 0.3s -> raw/xml/irs/20261010T122754_521307706_TY2024_2026_TEOS_XML_06A_202631539349300848_public.xml
- 2026_TEOS_XML_06A: mean member 28.7 KB uncompressed, compression ratio 5.3x
- GT S3 copy of 202631539349300848 byte-identical to the IRS ZIP member: True

### 2026-10-10 12:27 — 16_probe_context: omb
- OMB list1_2023 (reused): CBSA 47900 23 rows {'DC': 1, 'MD': 4, 'VA': 17, 'WV': 1} -> config/dmv_counties.csv

### 2026-10-10 12:27 — 16_probe_context: catalog
- wrote sources/catalog_parts/context.csv
- statuses: omb=ok

### 2026-10-10 12:28 — 10_probe_filings: volume
- BMF sets: (a) DMV PF filers (FOUNDATION 02/03/04 or PF_FILING_REQ_CD=1) 5,855 EINs; (b) DC 501(c)(3) public charities in NTEE L/P/F/I/J/W 1,750 EINs
- (a: DMV 990-PF filers) 25,367 returns from 5,249 EINs; by type {'990PF': 25367}; by tax year {2018: 22, 2019: 397, 2020: 3884, 2021: 4256, 2022: 4527, 2023: 4835, 2024: 4912, 2025: 2534}; by release year {2021: 3679, 2022: 4169, 2023: 4553, 2024: 4872, 2025: 5068, 2026: 3026}; same EIN+period+type repeats (amended/superseded) 213
  - ZIP batches: 50 distinct ZIPs touched (2021_TEOS_XML_01A 3679, 2022_ANY 4169, 2023_ANY 4553, 2024_TEOS_XML_01A 72, 2024_TEOS_XML_02A 185, 2024_TEOS_XML_03A 195, 2024_TEOS_XML_04A 386, 2024_TEOS_XML_05A 1326, 2024_TEOS_XML_06A 182, 2024_TEOS_XML_07A 256, 2024_TEOS_XML_08A 258, 2024_TEOS_XML_09A 260, 2024_TEOS_XML_10A 240, 2024_TEOS_XML_11A 1407, 2024_TEOS_XML_12A 105, 2025_TEOS_XML_01A 69, 2025_TEOS_XML_02A 185, 2025_TEOS_XML_03A 274, 2025_TEOS_XML_04A 417, 2025_TEOS_XML_05A 1363, 2025_TEOS_XML_06A 283, 2025_TEOS_XML_07A 131, 2025_TEOS_XML_08A 186, 2025_TEOS_XML_09A 307, 2025_TEOS_XML_10A 43, 2025_TEOS_XML_11A 383, 2025_TEOS_XML_11B 568, 2025_TEOS_XML_11C 330, 2025_TEOS_XML_11D 416, 2025_TEOS_XML_12A 113, 2026_TEOS_XML_01A 42, 2026_TEOS_XML_02A 198, 2026_TEOS_XML_03A 327, 2026_TEOS_XML_04A 384, 2026_TEOS_XML_05A 1392, 2026_TEOS_XML_06A 219, 2026_TEOS_XML_07A 194, 2026_TEOS_XML_08A 270)
  - bytes: full ZIP downloads 22.4 GB; remotezip ~479 MB (central directories 327.8 MB + members ~151.1 MB compressed); GT S3 per-object ~805.4 MB uncompressed
- (b: DC public charities L/P/F/I/J/W) 4,580 returns from 968 EINs; by type {'990EZ': 670, '990': 3907, '990PF': 3}; by tax year {2018: 5, 2019: 215, 2020: 731, 2021: 812, 2022: 826, 2023: 883, 2024: 885, 2025: 223}; by release year {2021: 712, 2022: 783, 2023: 832, 2024: 874, 2025: 899, 2026: 480}; same EIN+period+type repeats (amended/superseded) 114
  - ZIP batches: 50 distinct ZIPs touched (2021_TEOS_XML_01A 712, 2022_ANY 783, 2023_ANY 832, 2024_TEOS_XML_01A 16, 2024_TEOS_XML_02A 26, 2024_TEOS_XML_03A 39, 2024_TEOS_XML_04A 60, 2024_TEOS_XML_05A 133, 2024_TEOS_XML_06A 47, 2024_TEOS_XML_07A 45, 2024_TEOS_XML_08A 78, 2024_TEOS_XML_09A 50, 2024_TEOS_XML_10A 63, 2024_TEOS_XML_11A 299, 2024_TEOS_XML_12A 18, 2025_TEOS_XML_01A 12, 2025_TEOS_XML_02A 38, 2025_TEOS_XML_03A 30, 2025_TEOS_XML_04A 56, 2025_TEOS_XML_05A 142, 2025_TEOS_XML_06A 46, 2025_TEOS_XML_07A 28, 2025_TEOS_XML_08A 90, 2025_TEOS_XML_09A 53, 2025_TEOS_XML_10A 15, 2025_TEOS_XML_11A 91, 2025_TEOS_XML_11B 114, 2025_TEOS_XML_11C 85, 2025_TEOS_XML_11D 78, 2025_TEOS_XML_12A 21, 2026_TEOS_XML_01A 14, 2026_TEOS_XML_02A 34, 2026_TEOS_XML_03A 46, 2026_TEOS_XML_04A 54, 2026_TEOS_XML_05A 130, 2026_TEOS_XML_06A 51, 2026_TEOS_XML_07A 59, 2026_TEOS_XML_08A 92)
  - bytes: full ZIP downloads 22.4 GB; remotezip ~355 MB (central directories 327.8 MB + members ~27.3 MB compressed); GT S3 per-object ~145.5 MB uncompressed

### 2026-10-10 12:28 — 14_probe_dc_hud: DC Open Data / DC GIS
- hub search 'ward 2022': numberMatched 14; top: Crime Incidents in 2022; 311 City Service Requests in 2022; Wards from 2022; DC COVID 19 Cases by Ward; ACS 5-Year Economic Characteristics DC Ward; High Injury Network
- hub search 'census tracts 2020': numberMatched 43; top: Census Tracts in 2020; ACS 5-Year Housing Characteristics DC Census Tract; ACS 5-Year Social Characteristics DC Census Tract; ACS 5-Year Economic Characteristics DC Census Tract; ACS 5-Year Demographic Characteristics DC Census Tract; Census Block Groups in 2020
- hub search 'homeless': numberMatched 7; top: Homeless Service Facilities; Homeless Shelter Locations; Homeless Facility Shuttle Stops; Human Services Catchment Area; DC COVID 19 Shelter Vaccine Summary; Primary Care Facility
- hub search 'shelter': numberMatched 11; top: Homeless Shelter Locations; DC COVID 19 Shelter Vaccine Summary; Homeless Service Facilities; Homeless Facility Shuttle Stops; Human Services Catchment Area; Commuter Bus Stops
- hub search 'contracts': numberMatched 49; top: Contracts from PASS; Contract CBE Vendors; Forecast from PASS; Purchase Orders from PASS; Contractor Awarded Engagements; Contractor Open Engagements
- hub search 'purchase orders': numberMatched 4; top: Purchase Orders from PASS; Pipeline Contractor Awarded Engagments Archive; Contractor Awarded Engagements; Payments from PASS
- hub search 'grants': numberMatched 18; top: DC Main Streets Business Sub Grants; Families First DC Communities; Neighborhood Investment Fund Areas; My Out of School Time; OVSJG Grant Recipients; Community-Based Dementia Care
- hub search 'budget': numberMatched 17; top: Payments from PASS; Solicitations from PASS; Forecast from PASS; Purchase Orders from PASS; High Injury Network; Contracts from PASS
- hub search 'victim': numberMatched 1; top: OVSJG Grant Recipients
- DCAT feed: 1871 datasets; 42 titles match homeless/contract/ward/budget terms
- layer wards_2022 (Administrative_Other_Boundaries_WebMercator/MapServer/53): name 'Ward - 2022', 21 fields, maxRecordCount 1000
- layer census_tracts_2020 (Demographic_WebMercator/MapServer/8): name 'Census Tracts - 2020', 316 fields, maxRecordCount 1000
- layer homeless_shelters (Public_Service_WebMercator/MapServer/25): name 'Homeless Shelter Locations', 33 fields, maxRecordCount 1000
- layer homeless_service_facilities (Public_Service_WebMercator/MapServer/6): name 'Homeless Service Facilities', 67 fields, maxRecordCount 1000
- layer ovsjg_grant_recipients (Public_Safety_WebMercator/MapServer/35): name 'OVSJG Grant Recipients', 9 fields, maxRecordCount 1000
- layer pass_contracts (Government_Operations/MapServer/37): name 'PASS Contracts', 45 fields, maxRecordCount 1000
- layer pass_purchase_orders (Government_Operations/MapServer/16): name 'PASS Purchase Orders', 19 fields, maxRecordCount 1000
- layer pass_payments (Government_Operations/MapServer/17): name 'PASS Payments', 22 fields, maxRecordCount 1000
- wards_2022 GeoJSON: 8 features; WARD values [1, 2, 3, 4, 5, 6, 7, 8]
- census_tracts_2020 GeoJSON: 206 features (fields TRACT, GEOID, NAME, POP100, HU100, ALAND, AWATER)
- homeless_shelters: 19 rows, active beds 2,763; Calvary rows: none (layer covers DHS low-barrier/TH shelters only)
- homeless_service_facilities: 115 rows; Calvary rows: none
- ovsjg_grant_recipients: 1267 rows; FY counts 2016: 69 ($26.9M), 2017: 78 ($29.1M), 2018: 77 ($38.4M), 2019: 239 ($96.7M), 2020: 129 ($47.5M), 2021: 134 ($54.6M), 2022: 168 ($90.9M), 2023: 132 ($71.6M), 2024: 121 ($62.9M), 2025: 120 ($92.7M)
- ovsjg_grant_recipients Calvary rows (AGENCY field = grantee): FY2019 Reach Up Transitional Housing Program $368,935; FY2019 Reach Up Transitional Housing Program $292,000; FY2020 Reach Up Transitional Housing Program $368,935; FY2021 Reach Up Transitional Housing Program $368,935; FY2022 New Foundations Transitional Housing Program $3,680,675; FY2022 Reach Up Transitional Housing Program $368,935; FY2022 Reach Up Transitional Housing Program $99,500; FY2023 New Foundations Transitional Housing Program $438,500; FY2023 Reach Up Transitional Housing Program $402,540; FY2024 New Foundations Transitional Housing $482,528; FY2024 Reach Up Transitional Housing $430,873; FY2025 New Foundations Transitional Housing $519,656; FY2025 Reach Up Transitional Housing $478,622
- PASS purchase orders, supplier like CALVARY WOM: 10 rows: FY2019 OVSJG FY19 - OVSJG - VS - 2019-CWSH-01  -  CALVARY  $208,372; FY2020 OVSJG FY20 - OVSJG - VS - 2020-CWSH-01  -  CALVARY  $368,395; FY2021 OVSJG FY21 - OVSJG - VS - 2021-CWSH-01  - Calvary W $482,423; FY2021 DHCD FY21 IDIS#2764 Calvary Women Services Covid-1 $32,298; FY2022 OVSJG FY22 - OVSJG - VS - 2022-CWSH-01  -  CALVARY  $468,435; FY2022 DHS Calvary Women's Services - SNAP E&T FY22 $62,899; FY2022 OVSJG FY22 - OVSJG - VS - 2022-CWSH-02  -  CALVARY  $3,680,675; FY2023 OVSJG FY23 - OVSJG - VS - 2023-CWSH-01  -  CALVARY  $402,540; FY2023 OVSJG FY23 - OVSJG - VS - 2023-CWSH-02  -  CALVARY  $343,887; FY2023 DHS Calvary Women's Services - SNAP E&T FY23 $68,544
- PASS payments to CALVARY WOM*: 95 rows; by FY/agency: FY2019 OVSJG $73,603; FY2020 OVSJG $476,040; FY2021 DHCD $32,298; FY2021 OVSJG $327,634; FY2022 DHS $15,183; FY2022 OVSJG $3,910,132; FY2023 DHS $109,084; FY2023 OVSJG $1,461,366; FY2024 DHS $3,024; FY2024 OVSJG $1,116,183
- PASS contracts (OCP awards >= $100K), supplier like CALVARY: 0 rows
- PASS POs to THE COMMUNITY PARTNERSHIP: 148 rows; DHS by FY: FYNone $1.9M, FY2013 $82.2M, FY2014 $95.3M, FY2015 $108.8M, FY2016 $119.0M, FY2017 $91.0M, FY2018 $98.2M, FY2019 $104.9M, FY2020 $101.5M, FY2021 $112.4M, FY2022 $131.6M, FY2023 $108.3M, FY2024 $110.4M, FY2025 $7.1M, FY2026 $71.1M
- PASS PO totals by peer supplier (all years): N Street Village: $7.5M, FY2013-2026, DBH/DHCD/DHS/DOH; Miriam's Kitchen: $22.1M, FY2013-2026, CAH/DBH/DHCD/DHS/EOM/MOAA/MOAAA/MOCC/MOCRS/MOFMB/MOLGBTQ/MONC/MORA/MORCA/MOTA/MOWPI/OGVP/OPLA; Friendship Place: $64.4M, FY2013-2026, DHS/DOES/EOM/MOAA/MOAAA/MOCC/MOCRS/MOFMB/MOLGBTQ/MONC/MORA/MORCA/MOTA/MOWPI/OGVP/OPLA; Pathways to Housing: $53.3M, FY2013-2026, DBH/DDS/DHCD/DHS/EOM/MOAA/MOAAA/MOCC/MOCRS/MOFMB/MOLGBTQ/MONC/MORA/MORCA/MOTA/MOWPI/OGVP/OPLA; House of Ruth: $23.2M, FY2013-2023, CFSA/DHCD/DHS/EOM/MOAA/MOAAA/MOCC/MOCRS/MOFMB/MOLGBTQ/MONC/MORA/MORCA/MOTA/MOWPI/OGVP/OPLA/OVSJG; My Sister's Place: $27.9M, FY2013-2025, CFSA/DHS/EOM/MOAA/MOAAA/MOCC/MOCRS/MOFMB/MOLA/MOLGBTQ/MONC/MORA/MORCA/MOTA/MOWPI/OGVP/OPLA/OVSJG; DASH: $0.0M, FY---, ; Community of Hope: $93.5M, FY2013-2026, CFSA/DBH/DHS/DOH/EOM/HBX/MOAA/MOAAA/MOCC/MOCRS/MOFMB/MOLGBTQ/MONC/MORA/MORCA/MOTA/MOWPI/OGVP/OPLA; New Endeavors by Women: $0.0M, FY2021-2021, DHCD; Coalition for the Homeless: $1.3M, FY2017-2023, DHS; SOME: $0.0M, FY---, ; Catholic Charities: $92.7M, FY2013-2026, CFSA/DACL/DBH/DCPS/DHS/DOH/DYRS/EOM/MOAA/MOAAA/MOCC/MOCRS/MOFMB/MOLA/MOLGBTQ/MONC/MORA/MORCA/MOTA/MOWPI/OAG/OGVP/OPLA/OVSJG; Christ House: $0.2M, FY2013-2022, DBH/DOH; TCP: $1,352.3M, FY2013-2026, CFSA/DBH/DHS/DOH/OSSE/OVSJG
- pass_purchase_orders: 279,712 rows, FISCALYEAR 2013-2027
- pass_contracts: 51,263 rows, FISCALYEAR 2005-2027
- pass_payments: 1,576,128 rows, FISCALYEAR 2017-2027

### 2026-10-10 12:28 — 14_probe_dc_hud: run summary
- bytes saved this run: raw/dc_gov 10.4 MB; total 10.4 MB
- failures (0): none

### 2026-10-10 12:29 — 12_probe_federal: usaspending recipient
- autocomplete: [("CALVARY WOMEN'S SERVICES, INC", None), ("CALVARY WOMEN'S SERVICES", None)]
- /recipient/ rows: 3; UEI KMGRTKET2KJ1 (DUNS 126543453) on P/C levels; R-level name-only record has no UEI
- profiles: {"2813d90d-8166-9870-4c74-3eca995e2739-C": {"total_transaction_amount": 200000.0, "total_transactions": 1, "loan_face_value": 0.0, "address": "1217 GOOD HOPE RD SE", "congressional_code": "98", "business_types": ["category_business", "corporate_entity_tax_exempt", "nonprofit"]}, "2813d90d-8166-9870-4c74-3eca995e2739-P": {"total_transaction_amount": 200000.0, "total_transactions": 1, "loan_face_value": 0.0, "address": "1217 GOOD HOPE RD SE", "congressional_code": "98", "business_types": ["category_business", "corporate_entity_tax_exempt", "nonprofit"]}, "a141975f-7383-7c48-fffa-47d17089658a-R": {"total_transaction_amount": 332827.84, "total_transactions": 1, "loan_face_value": 327200.0, "address": "1217 GOOD HOPE RD, S.E.", "congressional_code": "98", "business_types": ["nonprofit"]}}

### 2026-10-10 12:29 — 12_probe_federal: usaspending Calvary awards
- prime awards (all types, FY2008+): 2 -> grants B-22-CP-DC-0213 ['14.251'] $200,000 Department of Housing and Urban Development; loans 5894917008 ['59.073'] $327,200 Small Business Administration
- Calvary subawards (FSRS): 1 -> LOCAL INITIATIVES SUPPORT CORPORATION 14.252 $25,000 2017-08-18
- transactions: 2

### 2026-10-10 12:30 — 14_probe_dc_hud: DC budget books (CFO approved chapters)
- FY2027 approved: agency pages found ['CF0', 'DB0', 'FO0', 'HG0', 'HY0', 'JA0', 'RM0']
- FY2026 approved: agency pages found ['CF0', 'DB0', 'FO0', 'HG0', 'HY0', 'JA0', 'RM0']
- FY2025 approved: agency pages found ['CF0', 'DB0', 'FO0', 'HG0', 'HY0', 'JA0', 'RM0']
  - FY2025 CF0: agency page links no FY2025 chapter/tables (['cf_does_capital_2026o.pdf', 'cf_does_chapter_2026o.pdf', 'cf_does_tables_2026o-1.pdf', 'cf_does_tables_2026o-2.pdf']); using fallback ['cf0_does_chapter_2025j.pdf', 'cf_does_tables_2025j.pdf']
- FY2024 CF0 cf_des_tables_2024j.pdf [Approved FY2024, 18 pp]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; program_table -
- FY2024 CF0 cf_does_chapter_2024j.pdf [Approved FY2023, 12 pp]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; program_table 3-5
- FY2024 DB0 db_dhcd_chapter_2024j.pdf [Approved FY2023, 10 pp]: homeless -; PSH -; victim_svcs -; rent_supp 4,6,10; ICH -; program_table 3-5
  - codes: (2010) Affordable Housing Project; (2045) Local Rent Supplement 0 0 9,655 1,100 -8,555 0.0 0.0 0.0 0.0; (8100) HOUSING REGULATION; (8120) Housing Resource Center 0 0 5 205 200 0.0 0.0 0.0 0.0 0.0
- FY2024 DB0 db_dhcd_tables_2024j.pdf [Approved FY2024, 14 pp]: homeless -; PSH -; victim_svcs -; rent_supp 1; ICH -; program_table -
- FY2024 FO0 fo_vsjg_chapter_2024j.pdf [Approved FY2023, 8 pp]: homeless -; PSH -; victim_svcs 1,3-7; rent_supp -; ICH -; program_table 3-4
  - codes: (4000) VICTIM SERVICES; (4010) Victim Services 30,590 42,328 41,805 45,515 3,710 7.2 7.9 14; (6040) Safe Housing-Gun Violence 0 2,206 4,420 3,720 -700 0.0 0.0 0
- FY2024 FO0 fo_vsjg_tables_2024j.pdf [Approved FY2024, 11 pp]: homeless -; PSH -; victim_svcs 1-11; rent_supp -; ICH -; program_table -
- FY2024 HG0 hg_dmhhs_chapter_2024j.pdf [Approved FY2023, 5 pp]: homeless 1; PSH -; victim_svcs -; rent_supp -; ICH 1; program_table 3
- FY2024 HG0 hg_dmhhs_tables_2024j.pdf [Approved FY2024, 7 pp]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; program_table -
- FY2024 HY0 hy_has_chapter_2024j.pdf [Approved FY2023, 5 pp]: homeless 3; PSH 4; victim_svcs -; rent_supp 1-5; ICH -; program_table 2-3
  - codes: (6000) LOCAL RENT SUPPLEMENT -; (6020) Permanent Supp. Housing -; (6035) Targeted Affordable Housing; (6040) Targeted Affordable Housing; (6050) Homeless Services -Admin 3,410 0 4,721 0 -4,721 0.0 0.0 0.0 ; (7000) LOCAL RENT SUPPLEMENT -
- FY2024 HY0 hy_has_tables_2024j.pdf [Approved FY2024, 6 pp]: homeless 1; PSH -; victim_svcs -; rent_supp 1-3; ICH -; program_table -
- FY2024 JA0 ja_dhs_chapter_2024j.pdf [Approved FY2023, 13 pp]: homeless 1,4-9,11-12; PSH 4-5,8-9,12; victim_svcs -; rent_supp 12; ICH -; program_table 3-5
  - codes: (5000) FAMILY SERVICES; (5013) Homeless Prevention 3,783 5,111 8,541 11,541 3,000 0.0 0.0 0; (5020) Domestic Violence Services 2,224 3,089 3,117 2,940 -177 0.0 ; (5021) Transitional Housing Youth 9,793 9,357 10,764 12,032 1,269 0; (5022) Youth Services 10,703 9,876 13,635 10,989 -2,646 80.2 91.1 1; (5023) Homeless Service Continuum -; (5024) Permanent Supportive Housing -; (5026) Transitional Age Youth Shelter 1,980 1,980 1,980 1,980 0 0.0; (5027) Rapid Rehousing - Youth 1,200 1,008 1,150 1,150 0 0.0 0.0 0.; (5028) Rapid Rehousing - Individuals; (5029) Rapid Rehousing - Families; (5030) Homeless Services 0 21 0 0 0 0.0 0.0 0.0 0.0 0.0; (5032) Permanent Supportive Housing 4,912 5,122 4,935 4,935 0 0.0 0; (5034) Permanent Supportive Housing -; (5035) Permanent Supportive Housing -; (5037) Homeless Services Continuum -; (5038) Homeless Services; (5039) Homeless Services Continuum -
- FY2024 JA0 ja_dhs_tables_2024j.pdf [Approved FY2024, 13 pp]: homeless 2; PSH 2; victim_svcs -; rent_supp -; ICH -; program_table -
- FY2024 RM0 rm_dbh_crosswalk_2024j.pdf [stage?, 1 pp]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; program_table -
- FY2024 RM0 rm_dbh_tables_2024j.pdf [Approved FY2024, 20 pp]: homeless 2; PSH -; victim_svcs -; rent_supp -; ICH -; program_table -
- FY2024 RM0 rm_dbh_chapter_2023j_0.pdf [Approved FY2024, 18 pp]: homeless 5,11; PSH -; victim_svcs -; rent_supp -; ICH -; program_table 3-8
  - codes: (1800) BEHAVIORAL HEALTH; (5830) Behavioral Health Services 596 448 7 116 109 5.6 5.6 0.0 2.0; (5831) Behavioral Health Services - Adult 3,416 175 0 0 0 20.1 0.0 ; (5832) Behavioral Health Services - Child 1,847 356 0 0 0 15.8 0.9 ; (5836) Behavioral Health Services -; (5842) Homeless Outreach / Mobile Crisis; (5883) Disaster Behavioral Health &; (6501) Adult/Transitional Youth Services; (6502) Behavioral Health Services; (6507) Housing Support Services 0 30,848 28,397 29,637 1,240 0.0 2.; (6515) Behavioral Health Rehabilitation -; (6601) Child/Adolescent/Family Services; (6610) Behavioral Health Services; (6615) SUD Prevention & Treatment 0 303 2,499 1,267 -1,232 0.0 2.6 ; (6620) School Based Behavioral Health; (6625) Crisis Services 0 351 1,867 1,467 -400 0.0 0.0 0.0 0.0 0.0; (6704) Behavioral Health Block Grant; (6800) ADDICTION PREVENTION; (6910) Prevention and Early Intervention 861 55 0 0 0 2.8 0.0 0.0 0; (6911) Prevention/Early; (6912) Prevention/Early Intervention-Sch; (6913) Prevention Substance Use Disorder 1,771 -75 0 0 0 12.8 0.0 0; (6940) Housing Development 28,075 -19 0 0 0 7.7 0.0 0.0 0.0 0.0; (6970) Behavioral Health Rehab 10,082 -3 0 0 0 0.0 0.0 0.0 0.0 0.0; (6980) Behavioral Health Rehab- Local
- FY2025 CF0 cf0_does_chapter_2025j.pdf [Approved FY2025, 12 pp]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; program_table 3-6
- FY2025 CF0 cf_does_tables_2025j.pdf [Approved FY2025, 20 pp]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; program_table -
- FY2025 DB0 db0_dhcd_chapter_2025j.pdf [Approved FY2025, 10 pp]: homeless -; PSH -; victim_svcs -; rent_supp 9; ICH -; program_table -
- FY2025 DB0 db_dhcd_tables_2025j.pdf [Approved FY2025, 14 pp]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; program_table -
- FY2025 FO0 fo0_ovsjg_chapter_2025j.pdf [Approved FY2025, 8 pp]: homeless -; PSH -; victim_svcs 1-8; rent_supp -; ICH -; program_table -
- FY2025 FO0 fo_ovsjg_crosswalk_2025j_0.pdf [stage?, 1 pp]: homeless -; PSH -; victim_svcs 1; rent_supp -; ICH -; program_table -
- FY2025 FO0 fo_ovsjg_tables_2025j.pdf [Approved FY2025, 13 pp]: homeless -; PSH -; victim_svcs 1-13; rent_supp -; ICH -; program_table -
- FY2025 HG0 hg0_dmhhs_chapter_2025j.pdf [Approved FY2025, 6 pp]: homeless 1; PSH -; victim_svcs -; rent_supp -; ICH 1; program_table -
- FY2025 HG0 hg_dmhhs_tables_2025j.pdf [Approved FY2025, 7 pp]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; program_table -
- FY2025 HY0 hy0_hap_chapter_2025j.pdf [Approved FY2025, 4 pp]: homeless -; PSH 4; victim_svcs -; rent_supp 1,3-4; ICH -; program_table -
- FY2025 HY0 hy_hap_tables_2025j.pdf [Approved FY2025, 7 pp]: homeless -; PSH -; victim_svcs -; rent_supp 1; ICH -; program_table -
- FY2025 JA0 ja0_dhs_chapter_2025j.pdf [Approved FY2025, 14 pp]: homeless 1,7-9,12-13; PSH 7-8,11-12; victim_svcs -; rent_supp -; ICH -; program_table -
- FY2025 JA0 ja_dhs_tables_2025j.pdf [Approved FY2025, 14 pp]: homeless 1-2,4-5; PSH 2,5; victim_svcs -; rent_supp -; ICH -; program_table -
- FY2025 RM0 rm0_dbh_chapter_2025j.pdf [Approved FY2025, 18 pp]: homeless -; PSH -; victim_svcs 12; rent_supp -; ICH -; program_table -
- FY2025 RM0 rm_dbh_tables_2025j.pdf [Approved FY2025, 20 pp]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; program_table -
- FY2026 CF0 cf_does_chapter_2026o.pdf [Approved FY2025, 11 pp]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; program_table 3-5
- FY2026 CF0 cf_does_tables_2026o-1.pdf [stage?, 9 pp]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; program_table -
- FY2026 CF0 cf_does_tables_2026o-2.pdf [stage?, 12 pp]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; program_table -
- FY2026 DB0 db_dhcd_chapter_2026o.pdf [Approved FY2025, 9 pp]: homeless -; PSH -; victim_svcs -; rent_supp 5; ICH -; program_table 3-4
- FY2026 DB0 db_dhcd_tables_2026o.pdf [stage?, 13 pp]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; program_table -
- FY2026 FO0 fo_vsjg_chapter_2026o.pdf [Approved FY2025, 8 pp]: homeless -; PSH -; victim_svcs 1,4-7; rent_supp -; ICH -; program_table 3-4
- FY2026 FO0 fo_vsjg_tables_2026o.pdf [stage?, 13 pp]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; program_table -
- FY2026 HG0 hg_dmhhs_chapter_2026o.pdf [Approved FY2025, 5 pp]: homeless 1; PSH -; victim_svcs -; rent_supp -; ICH 1; program_table 3
- FY2026 HG0 hg_dmhhs_tables_2026o.pdf [stage?, 7 pp]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; program_table -
- FY2026 HY0 hy_has_chapter_2026o.pdf [Approved FY2025, 4 pp]: homeless -; PSH -; victim_svcs -; rent_supp 1-3; ICH -; program_table 2
- FY2026 HY0 hy_has_tables_2026o.pdf [stage?, 7 pp]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; program_table -
- FY2026 JA0 ja_dhs_chapter_2026o.pdf [Approved FY2025, 13 pp]: homeless 1,4-9,11-12; PSH 5,7,9,11-12; victim_svcs 13; rent_supp -; ICH -; program_table 3-5
  - codes: (FRSP) Family Services 9,893 0.0; (STFH) Family Services 13,191 0.0
- FY2026 JA0 ja_dhs_tables_2026o.pdf [stage?, 15 pp]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; program_table -
- FY2026 RM0 rm_dbh_chapter_2026o.pdf [Approved FY2025, 17 pp]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; program_table 3-7
- FY2026 RM0 rm_dbh_tables_2026o-1.pdf [stage?, 9 pp]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; program_table -
- FY2026 RM0 rm_dbh_tables_2026o-2.pdf [stage?, 11 pp]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; program_table -
- FY2027 CF0 cf0_does_chapter_2027a_1.pdf [Approved FY2027, 10 pp]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; program_table 3-5
- FY2027 CF0 cf0_does_tables_2027a_0.pdf [Approved FY2027, 18 pp]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; program_table -
- FY2027 DB0 db0_dhcd_chapter_2027a_1.pdf [Approved FY2027, 9 pp]: homeless -; PSH -; victim_svcs -; rent_supp 5-6,8; ICH -; program_table 3-4
- FY2027 DB0 db0_dhcd_tables_2027a_0.pdf [Approved FY2027, 11 pp]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; program_table -
- FY2027 FO0 fo0_ovsjg_chapter_2027a_1.pdf [Approved FY2027, 7 pp]: homeless -; PSH -; victim_svcs 1-7; rent_supp -; ICH -; program_table 3-4
- FY2027 FO0 fo0_ovsjg_crosswalk_2027a.pdf [stage?, 1 pp]: homeless -; PSH -; victim_svcs 1; rent_supp -; ICH -; program_table -
- FY2027 FO0 fo0_ovsjg_tables_2027a_0.pdf [Approved FY2027, 9 pp]: homeless -; PSH -; victim_svcs 1-9; rent_supp -; ICH -; program_table -
- FY2027 HG0 hg0_dmhhs_chapter_2027a_1.pdf [Approved FY2027, 5 pp]: homeless 1,4; PSH -; victim_svcs -; rent_supp -; ICH 1,4; program_table 3
- FY2027 HG0 hg0_dmhhs_tables_2027a_0.pdf [Approved FY2027, 7 pp]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; program_table -
- FY2027 HY0 hy0_hap_chapter_2027a_1.pdf [Approved FY2027, 4 pp]: homeless -; PSH -; victim_svcs -; rent_supp 1-4; ICH -; program_table 2
  - codes: (LRSP) HOUSING 27,708 0.0
- FY2027 HY0 hy0_hap_tables_2027a_0.pdf [Approved FY2027, 7 pp]: homeless -; PSH -; victim_svcs -; rent_supp 1; ICH -; program_table -
- FY2027 JA0 ja0_dhs_chapter_2027a_1.pdf [Approved FY2027, 10 pp]: homeless 1,4,6-7,10; PSH 4,6-7; victim_svcs -; rent_supp -; ICH -; program_table 3-5
- FY2027 JA0 ja0_dhs_tables_2027a_0.pdf [Approved FY2027, 14 pp]: homeless 1-2,5-6; PSH 2,6; victim_svcs -; rent_supp -; ICH -; program_table -
- FY2027 RM0 rm0_dbh_chapter_2027a_1.pdf [Approved FY2027, 14 pp]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; program_table 3-6
- FY2027 RM0 rm0_dbh_tables_2027a_0.pdf [Approved FY2027, 17 pp]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; program_table -

### 2026-10-10 12:30 — 14_probe_dc_hud: run summary
- bytes saved this run: raw/dc_gov 75.1 MB; total 75.1 MB
- failures (0): none

### 2026-10-10 12:31 — 11_eval_xml_tooling: fetch
- calvary_990 TY2021 202322239349302102: GT S3 55,842 B -> raw/xml/gt/20261010T123138_521307706_TY2021_202322239349302102_public.xml
- calvary_990 TY2022 202401649349300215: GT S3 57,566 B -> raw/xml/gt/20261010T123138_521307706_TY2022_202401649349300215_public.xml
- calvary_990 TY2023 202542169349300419: GT S3 55,565 B -> raw/xml/gt/20261010T123138_521307706_TY2023_202542169349300419_public.xml
- meyer_990pf TY2021 202233149349102223: GT S3 266,942 B -> raw/xml/gt/20261010T123138_530241716_TY2021_202233149349102223_public.xml
- meyer_990pf TY2022 202303119349102405: GT S3 258,324 B -> raw/xml/gt/20261010T123138_530241716_TY2022_202303119349102405_public.xml
- meyer_990pf TY2023 202443119349102189: remotezip 2024_TEOS_XML_11A member 271,303 B; transferred 3 requests / 17.4 MB (central directory 17.4 MB) -> raw/xml/irs/20261010T123139_530241716_TY2023_2024_TEOS_XML_11A_202443119349102189_public.xml
- meyer_990pf TY2024 202512959349101021: GT S3 407,374 B -> raw/xml/gt/20261010T123139_530241716_TY2024_202512959349101021_public.xml
- cafritz_990pf TY2024 202513399349100006: GT S3 359,089 B -> raw/xml/gt/20261010T123139_526036989_TY2024_202513399349100006_public.xml
- gwcf_990 TY2023 202520389349300807: GT S3 843,305 B -> raw/xml/gt/20261010T123140_237343119_TY2023_202520389349300807_public.xml
- gwcf_990 TY2024 202640449349302259: GT S3 1,029,409 B -> raw/xml/gt/20261010T123140_237343119_TY2024_202640449349302259_public.xml

### 2026-10-10 12:31 — 11_eval_xml_tooling: concordance
- commit d8266da934cd (2026-08-23T04:30:32Z)
- concordance.csv: 3,352,506 B -> raw/concordance/20261010T123141_d8266da9_concordance.csv
- README.md: 6,046 B -> raw/concordance/20261010T123141_d8266da9_README.md
- LICENSE.md: 19,977 B -> raw/concordance/20261010T123141_d8266da9_LICENSE.md
- CITATION.cff: 794 B -> raw/concordance/20261010T123141_d8266da9_CITATION.cff
- 00-documentation/VARNAMES.md: 12,268 B -> raw/concordance/20261010T123141_d8266da9_00-documentation__VARNAMES.md
- 02-concordance-foundations/F990-PF-FULL.CSV: 976,451 B -> raw/concordance/20261010T123141_d8266da9_02-concordance-foundations__F990-PF-FULL.csv
- draft-updates/DUCKDB-XPATH-REPORT.CSV: 9,421,578 B -> raw/concordance/20261010T123142_d8266da9_draft-updates__DUCKDB-XPATH-REPORT.csv
- draft-updates/XPATH-VERSION-COUNT.CSV: 1,830,847 B -> raw/concordance/20261010T123142_d8266da9_draft-updates__XPATH-VERSION-COUNT.csv
- draft-updates/MISSING-XPATHS-UNIQUE-FILE-ALL.CSV: 172,326 B -> raw/concordance/20261010T123142_d8266da9_draft-updates__MISSING-XPATHS-UNIQUE-FILE-ALL.csv

### 2026-10-10 12:32 — 11_eval_xml_tooling: lxml
- concordance.csv (990, 990-EZ, schedules): 6,864 rows; form_type {'PC': 1940, 'EZ': 463, 'F9': 1, 'PZ': 2, 'SZ': 4458}; newest versions tagged: 2022v5.0, 2023v4.0, 2023v5.0, 2023v5.1; rows tagged with a 2021+ version 61; latest_version mix {'2016': 2324, '2012': 2206, 'NA': 1794, '2013': 344}
- F990-PF-FULL.CSV: 2,231 rows; form_type {'PF': 2231}; newest versions tagged: 2015v2.0, 2015v2.1, 2015v3.0, 2016v3.0; rows tagged with a 2021+ version 0; latest_version mix {'': 782, '2012': 681, '2016': 681, '2013': 87}
- xpaths in concordance + F990-PF-FULL by area: Part VIII revenue 16; Part IX expenses 14; Part VII-A people 17; Schedule I 102; Schedule R 417; 990-PF grants paid 31; 990-PF officers 93
- DUCKDB-XPATH-REPORT (observed DATA xpaths, Oct 2025 rebuild): 6,972; seen in 2023/2024 schemas 5,163, of which mapped to a concordance variable 5,050
  - Part VIII revenue: 16 xpaths seen in 2023/2024 schemas, unmapped 0
  - Part IX expenses: 14 xpaths seen in 2023/2024 schemas, unmapped 0
  - Part VII-A people: 17 xpaths seen in 2023/2024 schemas, unmapped 0
  - Schedule I: 77 xpaths seen in 2023/2024 schemas, unmapped 0
  - Schedule R: 367 xpaths seen in 2023/2024 schemas, unmapped 0
  - 990-PF grants paid: 0 xpaths seen in 2023/2024 schemas, unmapped 0
  - 990-PF officers: 0 xpaths seen in 2023/2024 schemas, unmapped 0
  - all IRS990PF xpaths seen in 2023/2024: 0, unmapped 0
- cafritz_990pf TY2024 202513399349100006 [2024v5.2] TaxYr 2024 2024-05-01..2025-04-30: {"returnVersion": "2024v5.2", "TaxYr": "2024", "TaxPeriodEndDt": "2025-04-30", "ReturnTypeCd": "990PF", "PF_TotalRevAndExpnssAmt": "65646300", "PF_ContriPaidRevAndExpnssAmt": "23052750", "PF_FMVAssetsEOYAmt": "781380241", "PF_grants": 452, "PF_grants_sum": 23052750.0, "PF_TotalGrantOrContriPdDurYrAmt": "23052750", "PF_grants_with_name": 452, "PF_grants_with_purpose": 452, "PF_grant_first": "21ST CENTURY CONSORT", "PF_people": 12, "PF_calvary_hits": [["CALVARY WOMEN'S SERVICES", "170000"]]}
  - schedules: IRS990PF, AccountingFeesSchedule, DepreciationSchedule, ExplnOfNonFilingWithAGStmt, InvestmentsCorpBondsSchedule, InvestmentsCorpStockSchedule, InvestmentsLandSchedule2, InvestmentsOtherSchedule2, LandEtcSchedule2, LegalFeesSchedule, OtherAssetsSchedule, OtherExpensesSchedule, OtherIncomeSchedule2, OtherLiabilitiesSchedule, OtherProfessionalFeesSchedule, ReductionExplanationStatement, TaxesSchedule
  - concordance covers 97% of 420 leaf paths; e.g. missing: IRS990PF/AnalysisIncomeProducingActyGrp/DividendsAndInterestFromSecDtl/ExclusionAmt, IRS990PF/AnalysisIncomeProducingActyGrp/DividendsAndInterestFromSecDtl/ExclusionCd, IRS990PF/AnalysisIncomeProducingActyGrp/DividendsAndInterestFromSecDtl/UnrelatedBusinessTaxblIncmAmt, IRS990PF/ExciseTaxBasedOnInvstIncmGrp/ExemptFrgnOrgTaxWthldAtSrceAmt
- calvary_990 TY2014 201600959349300900 [2014v6.0] TaxYr 2014 2014-10-01..2015-09-30: {"returnVersion": "2014v6.0", "TaxYr": "2014", "TaxPeriodEndDt": "2015-09-30", "ReturnTypeCd": "990", "CYTotalRevenueAmt": "2008601", "CYTotalExpensesAmt": "1879006", "mission": "TO PROVIDE HOUSING AND SUPPORT SERVICES TO THE HOMELESS WOME", "P8_TotalContributionsAmt": "2083419", "P8_GovernmentGrantsAmt": "888295", "P8_FundraisingAmt": "287580", "P8_AllOtherContributionsAmt": "887551", "P8_NoncashContributionsAmt": "85953", "P8_TotalRevenueColumnAmt": "2008601", "P9_TotalAmt": "1879006", "P9_ProgramServicesAmt": "1535029", "P9_ManagementAndGeneralAmt": "36762", "P9_FundraisingAmt": "307215", "P7A_people": 19, "P7A_first": "PRESIDENT"}
  - schedules: IRS990, IRS990ScheduleA, IRS990ScheduleB, IRS990ScheduleD, IRS990ScheduleG, IRS990ScheduleM, IRS990ScheduleO
  - concordance covers 100% of 424 leaf paths; e.g. missing: 
- calvary_990 TY2015 201731189349300503 [2015v3.0] TaxYr 2015 2015-10-01..2016-09-30: {"returnVersion": "2015v3.0", "TaxYr": "2015", "TaxPeriodEndDt": "2016-09-30", "ReturnTypeCd": "990", "CYTotalRevenueAmt": "1990443", "CYTotalExpensesAmt": "1989199", "mission": "TO PROVIDE HOUSING AND SUPPORT SERVICES TO THE HOMELESS WOME", "P8_TotalContributionsAmt": "2071314", "P8_GovernmentGrantsAmt": "932814", "P8_FundraisingAmt": "301790", "P8_AllOtherContributionsAmt": "820144", "P8_NoncashContributionsAmt": "98098", "P8_TotalRevenueColumnAmt": "1990443", "P9_TotalAmt": "1989199", "P9_ProgramServicesAmt": "1653902", "P9_ManagementAndGeneralAmt": "25854", "P9_FundraisingAmt": "309443", "P7A_people": 19, "P7A_first": "PRESIDENT"}
  - schedules: IRS990, IRS990ScheduleA, IRS990ScheduleB, IRS990ScheduleD, IRS990ScheduleG, IRS990ScheduleM, IRS990ScheduleO
  - concordance covers 100% of 427 leaf paths; e.g. missing: 
- calvary_990 TY2016 201801039349300220 [2016v3.0] TaxYr 2016 2016-10-01..2017-09-30: {"returnVersion": "2016v3.0", "TaxYr": "2016", "TaxPeriodEndDt": "2017-09-30", "ReturnTypeCd": "990", "CYTotalRevenueAmt": "2259177", "CYTotalExpensesAmt": "2076427", "mission": "TO PROVIDE HOUSING AND SUPPORT SERVICES TO THE HOMELESS WOME", "P8_TotalContributionsAmt": "2338922", "P8_GovernmentGrantsAmt": "965548", "P8_FundraisingAmt": "301899", "P8_AllOtherContributionsAmt": "1064786", "P8_NoncashContributionsAmt": "109020", "P8_TotalRevenueColumnAmt": "2259177", "P9_TotalAmt": "2076427", "P9_ProgramServicesAmt": "1730779", "P9_ManagementAndGeneralAmt": "46803", "P9_FundraisingAmt": "298845", "P7A_people": 17, "P7A_first": "PRESIDENT"}
  - schedules: IRS990, IRS990ScheduleA, IRS990ScheduleB, IRS990ScheduleD, IRS990ScheduleG, IRS990ScheduleM, IRS990ScheduleO
  - concordance covers 100% of 436 leaf paths; e.g. missing: 
- calvary_990 TY2017 201910249349300501 [2017v2.3] TaxYr 2017 2017-10-01..2018-09-30: {"returnVersion": "2017v2.3", "TaxYr": "2017", "TaxPeriodEndDt": "2018-09-30", "ReturnTypeCd": "990", "CYTotalRevenueAmt": "2153899", "CYTotalExpensesAmt": "2152260", "mission": "TO PROVIDE HOUSING AND SUPPORT SERVICES TO THE HOMELESS WOME", "P8_TotalContributionsAmt": "2250913", "P8_GovernmentGrantsAmt": "979272", "P8_FundraisingAmt": "279265", "P8_AllOtherContributionsAmt": "970017", "P8_NoncashContributionsAmt": "121904", "P8_TotalRevenueColumnAmt": "2153899", "P9_TotalAmt": "2152260", "P9_ProgramServicesAmt": "1821356", "P9_ManagementAndGeneralAmt": "18290", "P9_FundraisingAmt": "312614", "P7A_people": 20, "P7A_first": "PRESIDENT"}
  - schedules: IRS990, IRS990ScheduleA, IRS990ScheduleB, IRS990ScheduleD, IRS990ScheduleG, IRS990ScheduleM, IRS990ScheduleO
  - concordance covers 100% of 432 leaf paths; e.g. missing: IRS990ScheduleB
- calvary_990 TY2018 202010389349301241 [2018v3.1] TaxYr 2018 2018-10-01..2019-09-30: {"returnVersion": "2018v3.1", "TaxYr": "2018", "TaxPeriodEndDt": "2019-09-30", "ReturnTypeCd": "990", "CYTotalRevenueAmt": "2486678", "CYTotalExpensesAmt": "2403977", "mission": "TO PROVIDE HOUSING AND SUPPORT SERVICES TO THE HOMELESS WOME", "P8_TotalContributionsAmt": "2561745", "P8_GovernmentGrantsAmt": "1256102", "P8_FundraisingAmt": "331837", "P8_AllOtherContributionsAmt": "960414", "P8_NoncashContributionsAmt": "109213", "P8_TotalRevenueColumnAmt": "2486678", "P9_TotalAmt": "2403977", "P9_ProgramServicesAmt": "1857983", "P9_ManagementAndGeneralAmt": "189243", "P9_FundraisingAmt": "356751", "P7A_people": 16, "P7A_first": "PRESIDENT"}
  - schedules: IRS990, IRS990ScheduleA, IRS990ScheduleB, IRS990ScheduleD, IRS990ScheduleG, IRS990ScheduleM, IRS990ScheduleO
  - concordance covers 100% of 437 leaf paths; e.g. missing: 
- calvary_990 TY2019 202130449349300208 [2019v5.2] TaxYr 2019 2019-10-01..2020-09-30: {"returnVersion": "2019v5.2", "TaxYr": "2019", "TaxPeriodEndDt": "2020-09-30", "ReturnTypeCd": "990", "CYTotalRevenueAmt": "3896046", "CYTotalExpensesAmt": "3215728", "mission": "TO PROVIDE HOUSING AND SUPPORT SERVICES TO THE HOMELESS WOME", "P8_TotalContributionsAmt": "3914077", "P8_GovernmentGrantsAmt": "2166119", "P8_FundraisingAmt": "165497", "P8_AllOtherContributionsAmt": "1570112", "P8_NoncashContributionsAmt": "122440", "P8_TotalRevenueColumnAmt": "3896046", "P9_TotalAmt": "3215728", "P9_ProgramServicesAmt": "2652566", "P9_ManagementAndGeneralAmt": "164985", "P9_FundraisingAmt": "398177", "P7A_people": 17, "P7A_first": "PRESIDENT"}
  - schedules: IRS990, IRS990ScheduleA, IRS990ScheduleB, IRS990ScheduleD, IRS990ScheduleG, IRS990ScheduleM, IRS990ScheduleO
  - concordance covers 100% of 436 leaf paths; e.g. missing: 
- calvary_990 TY2020 202212279349301511 [2020v4.2] TaxYr 2020 2020-10-01..2021-09-30: {"returnVersion": "2020v4.2", "TaxYr": "2020", "TaxPeriodEndDt": "2021-09-30", "ReturnTypeCd": "990", "CYTotalRevenueAmt": "3851984", "CYTotalExpensesAmt": "3334967", "mission": "TO PROVIDE HOUSING AND SUPPORT SERVICES TO THE HOMELESS WOME", "P8_TotalContributionsAmt": "3869866", "P8_GovernmentGrantsAmt": "503222", "P8_FundraisingAmt": "287145", "P8_AllOtherContributionsAmt": "3063099", "P8_NoncashContributionsAmt": "159487", "P8_TotalRevenueColumnAmt": "3851984", "P9_TotalAmt": "3334967", "P9_ProgramServicesAmt": "2685622", "P9_ManagementAndGeneralAmt": "180215", "P9_FundraisingAmt": "469130", "P7A_people": 21, "P7A_first": "CHIEF EXECUTIVE OFFICER", "SI_grants": 0, "SI_cash_total": 0}
  - schedules: IRS990, IRS990ScheduleA, IRS990ScheduleB, IRS990ScheduleD, IRS990ScheduleG, IRS990ScheduleI, IRS990ScheduleJ, IRS990ScheduleM, IRS990ScheduleO
  - concordance covers 100% of 465 leaf paths; e.g. missing: 
- calvary_990 TY2021 202322239349302102 [2021v4.2] TaxYr 2021 2021-10-01..2022-09-30: {"returnVersion": "2021v4.2", "TaxYr": "2021", "TaxPeriodEndDt": "2022-09-30", "ReturnTypeCd": "990", "CYTotalRevenueAmt": "8867250", "CYTotalExpensesAmt": "4550205", "mission": "TO PROVIDE HOUSING AND SUPPORT SERVICES TO THE HOMELESS WOME", "P8_TotalContributionsAmt": "8954424", "P8_GovernmentGrantsAmt": "5685504", "P8_FundraisingAmt": "383731", "P8_AllOtherContributionsAmt": "2863364", "P8_NoncashContributionsAmt": "112647", "P8_TotalRevenueColumnAmt": "8867250", "P9_TotalAmt": "4550205", "P9_ProgramServicesAmt": "3655867", "P9_ManagementAndGeneralAmt": "310650", "P9_FundraisingAmt": "583688", "P7A_people": 22, "P7A_first": "CHIEF EXECUTIVE OFFICER", "SI_grants": 0, "SI_cash_total": 0}
  - schedules: IRS990, IRS990ScheduleA, IRS990ScheduleB, IRS990ScheduleD, IRS990ScheduleG, IRS990ScheduleI, IRS990ScheduleJ, IRS990ScheduleM, IRS990ScheduleO
  - concordance covers 100% of 498 leaf paths; e.g. missing: 
- calvary_990 TY2022 202401649349300215 [2022v5.0] TaxYr 2022 2022-10-01..2023-09-30: {"returnVersion": "2022v5.0", "TaxYr": "2022", "TaxPeriodEndDt": "2023-09-30", "ReturnTypeCd": "990", "CYTotalRevenueAmt": "4456814", "CYTotalExpensesAmt": "5130964", "mission": "TO PROVIDE HOUSING AND SUPPORT SERVICES TO THE HOMELESS WOME", "P8_TotalContributionsAmt": "4603409", "P8_GovernmentGrantsAmt": "2460897", "P8_FundraisingAmt": "457758", "P8_AllOtherContributionsAmt": "1664378", "P8_NoncashContributionsAmt": "139811", "P8_TotalRevenueColumnAmt": "4456814", "P9_TotalAmt": "5130964", "P9_ProgramServicesAmt": "4043376", "P9_ManagementAndGeneralAmt": "337548", "P9_FundraisingAmt": "750040", "P7A_people": 21, "P7A_first": "PRESIDENT", "SI_grants": 0, "SI_cash_total": 0}
  - schedules: IRS990, IRS990ScheduleA, IRS990ScheduleB, IRS990ScheduleD, IRS990ScheduleG, IRS990ScheduleI, IRS990ScheduleJ, IRS990ScheduleM, IRS990ScheduleO
  - concordance covers 100% of 536 leaf paths; e.g. missing: 
- calvary_990 TY2023 202542169349300419 [2023v6.0] TaxYr 2023 2023-10-01..2024-09-30: {"returnVersion": "2023v6.0", "TaxYr": "2023", "TaxPeriodEndDt": "2024-09-30", "ReturnTypeCd": "990", "CYTotalRevenueAmt": "5817167", "CYTotalExpensesAmt": "5310627", "mission": "TO PROVIDE HOUSING AND SUPPORT SERVICES TO THE HOMELESS WOME", "P8_TotalContributionsAmt": "5552129", "P8_GovernmentGrantsAmt": "2621203", "P8_FundraisingAmt": "538070", "P8_AllOtherContributionsAmt": "2374677", "P8_NoncashContributionsAmt": "156174", "P8_TotalRevenueColumnAmt": "5817167", "P9_TotalAmt": "5310627", "P9_ProgramServicesAmt": "4192940", "P9_ManagementAndGeneralAmt": "479604", "P9_FundraisingAmt": "638083", "P7A_people": 23, "P7A_first": "CHIEF EXECUTIVE OFFICER", "SI_grants": 0, "SI_cash_total": 0}
  - schedules: IRS990, IRS990ScheduleA, IRS990ScheduleB, IRS990ScheduleD, IRS990ScheduleG, IRS990ScheduleI, IRS990ScheduleJ, IRS990ScheduleM, IRS990ScheduleO
  - concordance covers 100% of 499 leaf paths; e.g. missing: 
- calvary_990 TY2024 202631539349300848 [2024v5.5] TaxYr 2024 2024-10-01..2025-09-30: {"returnVersion": "2024v5.5", "TaxYr": "2024", "TaxPeriodEndDt": "2025-09-30", "ReturnTypeCd": "990", "CYTotalRevenueAmt": "4967995", "CYTotalExpensesAmt": "5575321", "mission": "TO PROVIDE HOUSING AND SUPPORT SERVICES TO THE HOMELESS WOME", "P8_TotalContributionsAmt": "4747134", "P8_GovernmentGrantsAmt": "2892598", "P8_FundraisingAmt": "54730", "P8_AllOtherContributionsAmt": "1643841", "P8_NoncashContributionsAmt": "138856", "P8_TotalRevenueColumnAmt": "4967995", "P9_TotalAmt": "5575321", "P9_ProgramServicesAmt": "4484739", "P9_ManagementAndGeneralAmt": "552301", "P9_FundraisingAmt": "538281", "P7A_people": 22, "P7A_first": "PRESIDENT", "SI_grants": 0, "SI_cash_total": 0}
  - schedules: IRS990, IRS990ScheduleA, IRS990ScheduleB, IRS990ScheduleD, IRS990ScheduleG, IRS990ScheduleI, IRS990ScheduleJ, IRS990ScheduleM, IRS990ScheduleO
  - concordance covers 100% of 485 leaf paths; e.g. missing: 
- gwcf_990 TY2023 202520389349300807 [2023v6.0] TaxYr 2023 2023-04-01..2024-03-31: {"returnVersion": "2023v6.0", "TaxYr": "2023", "TaxPeriodEndDt": "2024-03-31", "ReturnTypeCd": "990", "CYTotalRevenueAmt": "99984918", "CYTotalExpensesAmt": "100751172", "mission": "The Community Foundation aims to mobilize and ignite the pow", "P8_TotalContributionsAmt": "75421557", "P8_GovernmentGrantsAmt": "525288", "P8_FundraisingAmt": "1180524", "P8_AllOtherContributionsAmt": "73715745", "P8_NoncashContributionsAmt": "31649043", "P8_TotalProgramServiceRevenueAmt": "0", "P8_TotalRevenueColumnAmt": "99984918", "P9_TotalAmt": "100751172", "P9_ProgramServicesAmt": "92678133", "P9_ManagementAndGeneralAmt": "6725569", "P9_FundraisingAmt": "1347470", "P9_GrantsToDomesticOrgs": "90418317", "P7A_people": 35, "P7A_first": "President & CEO", "SI_grants": 1163, "SI_cash_total": 83729369.0, "SI_first": "1st Stage Inc"}
  - schedules: IRS990, IRS990ScheduleA, IRS990ScheduleB, IRS990ScheduleC, IRS990ScheduleD, IRS990ScheduleF, IRS990ScheduleG, IRS990ScheduleI, IRS990ScheduleJ, IRS990ScheduleM, IRS990ScheduleO
  - concordance covers 95% of 734 leaf paths; e.g. missing: IRS990ScheduleC/GrassrootsNontaxableGrp, IRS990ScheduleC/LobbyingNontaxableAmountGrp, IRS990ScheduleC/OtherExemptPurposeExpendGrp, IRS990ScheduleC/TotLbbyExpendMnsLbbyngNonTxGrp
- gwcf_990 TY2024 202640449349302259 [2024v5.1] TaxYr 2024 2024-04-01..2025-03-31: {"returnVersion": "2024v5.1", "TaxYr": "2024", "TaxPeriodEndDt": "2025-03-31", "ReturnTypeCd": "990", "CYTotalRevenueAmt": "123242853", "CYTotalExpensesAmt": "130100629", "mission": "THE GREATER WASHINGTON COMMUNITY FOUNDATION'S MISSION IS TO ", "P8_TotalContributionsAmt": "84525355", "P8_GovernmentGrantsAmt": "1015000", "P8_FundraisingAmt": "628172", "P8_AllOtherContributionsAmt": "82882183", "P8_NoncashContributionsAmt": "25398430", "P8_TotalProgramServiceRevenueAmt": "0", "P8_TotalRevenueColumnAmt": "123242853", "P9_TotalAmt": "130100629", "P9_ProgramServicesAmt": "122014557", "P9_ManagementAndGeneralAmt": "6287619", "P9_FundraisingAmt": "1798453", "P9_GrantsToDomesticOrgs": "119378786", "P7A_people": 31, "P7A_first": "BOARD VICE CHAIR", "SI_grants": 1417, "SI_cash_total": 116850076.0, "SI_first": "100 REPORTERS", "SR_related_exempt": 1, "SR_related_txbl_corp": 0, "SR_related_partnership": 0, "SR_disregarded": 0}
  - schedules: IRS990, IRS990ScheduleA, IRS990ScheduleB, IRS990ScheduleC, IRS990ScheduleD, IRS990ScheduleF, IRS990ScheduleG, IRS990ScheduleI, IRS990ScheduleJ, IRS990ScheduleM, IRS990ScheduleO, IRS990ScheduleR
  - concordance covers 100% of 753 leaf paths; e.g. missing: 
- meyer_990pf TY2021 202233149349102223 [2021v4.2] TaxYr 2021 2021-01-01..2021-12-31: {"returnVersion": "2021v4.2", "TaxYr": "2021", "TaxPeriodEndDt": "2021-12-31", "ReturnTypeCd": "990PF", "PF_TotalRevAndExpnssAmt": "6565769", "PF_ContriPaidRevAndExpnssAmt": "13604183", "PF_FMVAssetsEOYAmt": "265374116", "PF_grants": 170, "PF_grants_sum": 9889546.0, "PF_TotalGrantOrContriPdDurYrAmt": "9889546", "PF_grants_with_name": 170, "PF_grants_with_purpose": 170, "PF_grant_first": "ACADEMY OF HOPE", "PF_people": 13}
  - schedules: IRS990PF, AccountingFeesSchedule, ExpenditureResponsibilityStmt, GeneralExplanationAttachment, InvestmentsCorpBondsSchedule, InvestmentsCorpStockSchedule, InvestmentsOtherSchedule2, LandEtcSchedule2, LegalFeesSchedule, OtherAssetsSchedule, OtherDecreasesSchedule, OtherExpensesSchedule, OtherIncomeSchedule2, OtherIncreasesSchedule, OtherLiabilitiesSchedule, OtherProfessionalFeesSchedule, TaxesSchedule
  - concordance covers 97% of 434 leaf paths; e.g. missing: IRS990PF/AnalysisIncomeProducingActyGrp/DividendsAndInterestFromSecDtl/BusinessCd, IRS990PF/AnalysisIncomeProducingActyGrp/DividendsAndInterestFromSecDtl/ExclusionAmt, IRS990PF/AnalysisIncomeProducingActyGrp/DividendsAndInterestFromSecDtl/ExclusionCd, IRS990PF/AnalysisIncomeProducingActyGrp/DividendsAndInterestFromSecDtl/UnrelatedBusinessTaxblIncmAmt
- meyer_990pf TY2022 202303119349102405 [2022v5.0] TaxYr 2022 2022-01-01..2022-12-31: {"returnVersion": "2022v5.0", "TaxYr": "2022", "TaxPeriodEndDt": "2022-12-31", "ReturnTypeCd": "990PF", "PF_TotalRevAndExpnssAmt": "463421", "PF_ContriPaidRevAndExpnssAmt": "14369398", "PF_FMVAssetsEOYAmt": "210722273", "PF_grants": 166, "PF_grants_sum": 11027775.0, "PF_TotalGrantOrContriPdDurYrAmt": "11027775", "PF_grants_with_name": 166, "PF_grants_with_purpose": 166, "PF_grant_first": "ACADEMY OF HOPE", "PF_people": 12}
  - schedules: IRS990PF, AccountingFeesSchedule, ExpenditureResponsibilityStmt, GeneralExplanationAttachment, InvestmentsCorpStockSchedule, InvestmentsOtherSchedule2, LandEtcSchedule2, LegalFeesSchedule, OtherAssetsSchedule, OtherDecreasesSchedule, OtherExpensesSchedule, OtherIncomeSchedule2, OtherIncreasesSchedule, OtherLiabilitiesSchedule, OtherProfessionalFeesSchedule, TaxesSchedule
  - concordance covers 97% of 430 leaf paths; e.g. missing: IRS990PF/AnalysisIncomeProducingActyGrp/DividendsAndInterestFromSecDtl/BusinessCd, IRS990PF/AnalysisIncomeProducingActyGrp/DividendsAndInterestFromSecDtl/ExclusionAmt, IRS990PF/AnalysisIncomeProducingActyGrp/DividendsAndInterestFromSecDtl/ExclusionCd, IRS990PF/AnalysisIncomeProducingActyGrp/DividendsAndInterestFromSecDtl/UnrelatedBusinessTaxblIncmAmt
- meyer_990pf TY2023 202443119349102189 [2023v5.1] TaxYr 2023 2023-01-01..2023-12-31: {"returnVersion": "2023v5.1", "TaxYr": "2023", "TaxPeriodEndDt": "2023-12-31", "ReturnTypeCd": "990PF", "PF_TotalRevAndExpnssAmt": "6548862", "PF_ContriPaidRevAndExpnssAmt": "10830490", "PF_FMVAssetsEOYAmt": "224816964", "PF_grants": 177, "PF_grants_sum": 11003160.0, "PF_TotalGrantOrContriPdDurYrAmt": "11003160", "PF_grants_with_name": 177, "PF_grants_with_purpose": 177, "PF_grant_first": "ACT FOR ALEXANDRIA", "PF_people": 16}
  - schedules: IRS990PF, AccountingFeesSchedule, ExpenditureResponsibilityStmt, GeneralExplanationAttachment, InvestmentsCorpBondsSchedule, InvestmentsCorpStockSchedule, InvestmentsGovtObligationsSch, InvestmentsOtherSchedule2, LandEtcSchedule2, LegalFeesSchedule, OtherAssetsSchedule, OtherDecreasesSchedule, OtherExpensesSchedule, OtherIncomeSchedule2, OtherIncreasesSchedule, OtherLiabilitiesSchedule, OtherProfessionalFeesSchedule
  - concordance covers 97% of 426 leaf paths; e.g. missing: IRS990PF/AnalysisIncomeProducingActyGrp/DividendsAndInterestFromSecDtl/BusinessCd, IRS990PF/AnalysisIncomeProducingActyGrp/DividendsAndInterestFromSecDtl/ExclusionAmt, IRS990PF/AnalysisIncomeProducingActyGrp/DividendsAndInterestFromSecDtl/ExclusionCd, IRS990PF/AnalysisIncomeProducingActyGrp/DividendsAndInterestFromSecDtl/UnrelatedBusinessTaxblIncmAmt
- meyer_990pf TY2024 202512959349101021 [2024v5.2] TaxYr 2024 2024-01-01..2024-12-31: {"returnVersion": "2024v5.2", "TaxYr": "2024", "TaxPeriodEndDt": "2024-12-31", "ReturnTypeCd": "990PF", "PF_TotalRevAndExpnssAmt": "21806456", "PF_ContriPaidRevAndExpnssAmt": "12779344", "PF_FMVAssetsEOYAmt": "230700683", "PF_grants": 274, "PF_grants_sum": 13550350.0, "PF_TotalGrantOrContriPdDurYrAmt": "13550350", "PF_grants_with_name": 274, "PF_grants_with_purpose": 274, "PF_grant_first": "4DASOIL COLLECTIVE", "PF_people": 15}
  - schedules: IRS990PF, AccountingFeesSchedule, ExpenditureResponsibilityStmt, GeneralExplanationAttachment, InvestmentsCorpBondsSchedule, InvestmentsCorpStockSchedule, InvestmentsGovtObligationsSch, InvestmentsOtherSchedule2, LandEtcSchedule2, LegalFeesSchedule, OtherAssetsSchedule, OtherDecreasesSchedule, OtherExpensesSchedule, OtherIncomeSchedule2, OtherIncreasesSchedule, OtherLiabilitiesSchedule, OtherProfessionalFeesSchedule, TaxesSchedule
  - concordance covers 97% of 430 leaf paths; e.g. missing: IRS990PF/AnalysisIncomeProducingActyGrp/DividendsAndInterestFromSecDtl/BusinessCd, IRS990PF/AnalysisIncomeProducingActyGrp/DividendsAndInterestFromSecDtl/ExclusionAmt, IRS990PF/AnalysisIncomeProducingActyGrp/DividendsAndInterestFromSecDtl/ExclusionCd, IRS990PF/AnalysisIncomeProducingActyGrp/DividendsAndInterestFromSecDtl/UnrelatedBusinessTaxblIncmAmt
- schema versions seen: {'2014v6.0': 1, '2015v3.0': 1, '2016v3.0': 1, '2017v2.3': 1, '2018v3.1': 1, '2019v5.2': 1, '2020v4.2': 1, '2021v4.2': 2, '2022v5.0': 2, '2023v5.1': 1, '2023v6.0': 2, '2024v5.1': 1, '2024v5.2': 2, '2024v5.5': 1}

### 2026-10-10 12:32 — 11_eval_xml_tooling: irsx
- pip install irsx: rc 0; irsx/python: 0.5.1 3.12.13
- Python 3.13 venv: install rc 0, import ok
- cafritz_990pf TY2024 202513399349100006: {"version": "2024v5.2", "supported": true, "parsed_schedules": ["ReturnHeader990x", "IRS990PF"], "keyerrors": 0, "keyerror_sample": [], "PF_grants": 452, "PF_grants_sum": 0.0, "PF_parts": ["pf_part_0", "pf_part_i", "pf_part_ii", "pf_part_iii", "pf_part_iv", "pf_part_vi", "pf_part_viia", "pf_part_viib", "pf_part_viii", "pf_part_x", "pf_part_xi", "pf_part_xv", "pf_part_xvii"], "PF_groups": {"PFCpGnsLssTxInvstIncm": 1, "PFOrgRprtOrRgstrSttCd": 1, "PFOffcrDrTrstKyEmpl": 12, "PFCmpnstnHghstPdEmpl": 5, "PFCmpnstnOfHghstPdCntrct": 5, "pf_part_ixb": 1, "pf_part_xiii": 1, "PFApplctnSbmssnInf": 1, "PFGrntOrCntrbtnPdDrYr": 452, "PFOthrRvnDscrbd": 2, "pf_part_xvia": 1, "PFRlnOfActyTAccmOfExmptPrps": 1}}
- calvary_990 TY2019 202130449349300208: {"version": "2019v5.2", "supported": true, "parsed_schedules": ["ReturnHeader990x", "IRS990", "IRS990ScheduleA", "IRS990ScheduleB", "IRS990ScheduleD", "IRS990ScheduleG", "IRS990ScheduleM", "IRS990ScheduleO"], "keyerrors": 0, "keyerror_sample": [], "IRS990_CYTotalRevenueAmt": "3896046", "IRS990_part_viii_keys": 23, "IRS990_groups": {"part_iii": 3, "SttsWhrCpyOfRtrnIsFldCd": 1, "Frm990PrtVIISctnA": 17, "part_viii": 1, "OthrExpnss": 4, "part_ix": 1, "part_x": 4, "part_xii": 1}}
- calvary_990 TY2020 202212279349301511: {"version": "2020v4.2", "supported": true, "parsed_schedules": ["ReturnHeader990x", "IRS990", "IRS990ScheduleA", "IRS990ScheduleB", "IRS990ScheduleD", "IRS990ScheduleG", "IRS990ScheduleI", "IRS990ScheduleJ", "IRS990ScheduleM", "IRS990ScheduleO"], "keyerrors": 0, "keyerror_sample": [], "IRS990_CYTotalRevenueAmt": "3851984", "IRS990_part_viii_keys": 19, "IRS990_groups": {"part_iii": 3, "Frm990PrtVIISctnA": 21, "OthrExpnss": 4, "part_ix": 1, "part_x": 5, "part_xii": 1}, "SI_grants": 0}
- calvary_990 TY2021 202322239349302102: {"version": "2021v4.2", "supported": true, "parsed_schedules": ["ReturnHeader990x", "IRS990", "IRS990ScheduleA", "IRS990ScheduleB", "IRS990ScheduleD", "IRS990ScheduleG", "IRS990ScheduleI", "IRS990ScheduleJ", "IRS990ScheduleM", "IRS990ScheduleO"], "keyerrors": 0, "keyerror_sample": [], "IRS990_CYTotalRevenueAmt": "8867250", "IRS990_part_viii_keys": 24, "IRS990_groups": {"part_iii": 3, "PrgSrvcAccmActyOthr": 2, "Frm990PrtVIISctnA": 22, "CntrctrCmpnstn": 1, "part_viii": 1, "OthrRvnMsc": 1, "OthrExpnss": 4, "part_ix": 1, "part_x": 5, "part_xii": 1}, "SI_grants": 0}
- calvary_990 TY2022 202401649349300215: {"version": "2022v5.0", "supported": true, "parsed_schedules": ["ReturnHeader990x", "IRS990", "IRS990ScheduleA", "IRS990ScheduleB", "IRS990ScheduleD", "IRS990ScheduleG", "IRS990ScheduleI", "IRS990ScheduleJ", "IRS990ScheduleM", "IRS990ScheduleO"], "keyerrors": 0, "keyerror_sample": [], "IRS990_CYTotalRevenueAmt": "4456814", "IRS990_part_viii_keys": 23, "IRS990_groups": {"part_iii": 3, "PrgSrvcAccmActyOthr": 2, "Frm990PrtVIISctnA": 21, "CntrctrCmpnstn": 1, "part_viii": 1, "OthrExpnss": 4, "part_ix": 1, "part_x": 4, "part_xii": 1}, "SI_grants": 0}
- calvary_990 TY2023 202542169349300419: {"version": "2023v6.0", "supported": true, "parsed_schedules": ["ReturnHeader990x", "IRS990", "IRS990ScheduleA", "IRS990ScheduleB", "IRS990ScheduleD", "IRS990ScheduleG", "IRS990ScheduleI", "IRS990ScheduleJ", "IRS990ScheduleM", "IRS990ScheduleO"], "keyerrors": 0, "keyerror_sample": [], "IRS990_CYTotalRevenueAmt": "5817167", "IRS990_part_viii_keys": 25, "IRS990_groups": {"part_iii": 3, "PrgSrvcAccmActyOthr": 2, "Frm990PrtVIISctnA": 23, "part_viii": 1, "OthrRvnMsc": 2, "OthrExpnss": 4, "part_ix": 1, "part_x": 4, "part_xii": 1}, "SI_grants": 0}
- calvary_990 TY2024 202631539349300848: {"version": "2024v5.5", "supported": true, "parsed_schedules": ["ReturnHeader990x", "IRS990", "IRS990ScheduleA", "IRS990ScheduleB", "IRS990ScheduleD", "IRS990ScheduleG", "IRS990ScheduleI", "IRS990ScheduleJ", "IRS990ScheduleM", "IRS990ScheduleO"], "keyerrors": 0, "keyerror_sample": [], "IRS990_CYTotalRevenueAmt": "4967995", "IRS990_part_viii_keys": 19, "IRS990_groups": {"part_iii": 3, "PrgSrvcAccmActyOthr": 2, "Frm990PrtVIISctnA": 22, "OthrExpnss": 4, "part_x": 5, "part_xii": 1}, "SI_grants": 0}
- gwcf_990 TY2023 202520389349300807: {"version": "2023v6.0", "supported": true, "parsed_schedules": ["ReturnHeader990x", "IRS990", "IRS990ScheduleA", "IRS990ScheduleB", "IRS990ScheduleC", "IRS990ScheduleD", "IRS990ScheduleF", "IRS990ScheduleG", "IRS990ScheduleI", "IRS990ScheduleJ", "IRS990ScheduleM", "IRS990ScheduleO"], "keyerrors": 0, "keyerror_sample": [], "IRS990_CYTotalRevenueAmt": "99984918", "IRS990_part_viii_keys": 36, "IRS990_groups": {"part_iii": 3, "SttsWhrCpyOfRtrnIsFldCd": 2, "Frm990PrtVIISctnA": 35, "CntrctrCmpnstn": 5, "part_viii": 2, "OthrRvnMsc": 2, "OthrExpnss": 3, "part_x": 10, "part_xii": 1}, "SI_grants": 1163}
- gwcf_990 TY2024 202640449349302259: {"version": "2024v5.1", "supported": true, "parsed_schedules": ["ReturnHeader990x", "IRS990", "IRS990ScheduleA", "IRS990ScheduleB", "IRS990ScheduleC", "IRS990ScheduleD", "IRS990ScheduleF", "IRS990ScheduleG", "IRS990ScheduleI", "IRS990ScheduleJ", "IRS990ScheduleM", "IRS990ScheduleO", "IRS990ScheduleR"], "keyerrors": 0, "keyerror_sample": [], "IRS990_CYTotalRevenueAmt": "123242853", "IRS990_part_viii_keys": 39, "IRS990_groups": {"part_iii": 3, "SttsWhrCpyOfRtrnIsFldCd": 2, "Frm990PrtVIISctnA": 31, "CntrctrCmpnstn": 5, "part_viii": 1, "OthrRvnMsc": 3, "OthrExpnss": 4, "part_ix": 1, "part_x": 13}, "SI_grants": 1417, "SR_groups": {"SkdRIdRltdTxExmptOrg": 1}}
- meyer_990pf TY2021 202233149349102223: {"version": "2021v4.2", "supported": true, "parsed_schedules": ["ReturnHeader990x", "IRS990PF"], "keyerrors": 0, "keyerror_sample": [], "PF_grants": 170, "PF_grants_sum": 0.0, "PF_parts": ["pf_part_0", "pf_part_i", "pf_part_ii", "pf_part_iii", "pf_part_iv", "pf_part_vi", "pf_part_viia", "pf_part_viib", "pf_part_viii", "pf_part_x", "pf_part_xi", "pf_part_xv", "pf_part_xvii"], "PF_groups": {"PFCpGnsLssTxInvstIncm": 17, "PFOrgRprtOrRgstrSttCd": 2, "PFOffcrDrTrstKyEmpl": 13, "PFCmpnstnHghstPdEmpl": 5, "PFCmpnstnOfHghstPdCntrct": 5, "pf_part_ixa": 1, "pf_part_ixb": 1, "pf_part_xiii": 1, "PFApplctnSbmssnInf": 1, "PFGrntOrCntrbtnPdDrYr": 170, "PFGrntOrCntrApprvFrFt": 42, "PFOthrRvnDscrbd": 3, "pf_part_xvia": 1}}
- meyer_990pf TY2022 202303119349102405: {"version": "2022v5.0", "supported": true, "parsed_schedules": ["ReturnHeader990x", "IRS990PF"], "keyerrors": 0, "keyerror_sample": [], "PF_grants": 166, "PF_grants_sum": 0.0, "PF_parts": ["pf_part_0", "pf_part_i", "pf_part_ii", "pf_part_iii", "pf_part_iv", "pf_part_vi", "pf_part_viia", "pf_part_viib", "pf_part_viii", "pf_part_x", "pf_part_xi", "pf_part_xv", "pf_part_xvii"], "PF_groups": {"PFCpGnsLssTxInvstIncm": 8, "PFOrgRprtOrRgstrSttCd": 2, "PFOffcrDrTrstKyEmpl": 12, "PFCmpnstnHghstPdEmpl": 5, "PFCmpnstnOfHghstPdCntrct": 5, "pf_part_ixa": 1, "pf_part_ixb": 1, "pf_part_xiii": 1, "PFApplctnSbmssnInf": 1, "PFGrntOrCntrbtnPdDrYr": 166, "PFGrntOrCntrApprvFrFt": 43, "PFOthrRvnDscrbd": 5, "pf_part_xvia": 1}}
- meyer_990pf TY2023 202443119349102189: {"version": "2023v5.1", "supported": true, "parsed_schedules": ["ReturnHeader990x", "IRS990PF"], "keyerrors": 0, "keyerror_sample": [], "PF_grants": 177, "PF_grants_sum": 0.0, "PF_parts": ["pf_part_0", "pf_part_i", "pf_part_ii", "pf_part_iii", "pf_part_iv", "pf_part_vi", "pf_part_viia", "pf_part_viib", "pf_part_viii", "pf_part_x", "pf_part_xi", "pf_part_xv", "pf_part_xvii"], "PF_groups": {"PFCpGnsLssTxInvstIncm": 19, "PFOrgRprtOrRgstrSttCd": 2, "PFOffcrDrTrstKyEmpl": 16, "PFCmpnstnHghstPdEmpl": 5, "PFCmpnstnOfHghstPdCntrct": 5, "pf_part_ixb": 1, "pf_part_xiii": 1, "PFApplctnSbmssnInf": 1, "PFGrntOrCntrbtnPdDrYr": 177, "PFGrntOrCntrApprvFrFt": 45, "PFOthrRvnDscrbd": 4, "pf_part_xvia": 1}}
- meyer_990pf TY2024 202512959349101021: {"version": "2024v5.2", "supported": true, "parsed_schedules": ["ReturnHeader990x", "IRS990PF"], "keyerrors": 0, "keyerror_sample": [], "PF_grants": 274, "PF_grants_sum": 0.0, "PF_parts": ["pf_part_0", "pf_part_i", "pf_part_ii", "pf_part_iii", "pf_part_iv", "pf_part_vi", "pf_part_viia", "pf_part_viib", "pf_part_viii", "pf_part_x", "pf_part_xi", "pf_part_xv", "pf_part_xvii"], "PF_groups": {"PFCpGnsLssTxInvstIncm": 22, "PFOrgRprtOrRgstrSttCd": 2, "PFOffcrDrTrstKyEmpl": 15, "PFCmpnstnHghstPdEmpl": 5, "PFCmpnstnOfHghstPdCntrct": 5, "pf_part_ixb": 1, "pf_part_xiii": 1, "PFApplctnSbmssnInf": 1, "PFGrntOrCntrbtnPdDrYr": 274, "PFGrntOrCntrApprvFrFt": 57, "PFOthrRvnDscrbd": 2, "pf_part_xvia": 1}}

### 2026-10-10 12:32 — 14_probe_dc_hud: DC Council oversight, OVSJG lists, budget reports, BSA
- OVSJG funding-recipients page lists 10 annual PDFs: ['FY26 OVSJG Grant Recipients', 'FY25 OVSJG Grant Recipients', 'FY24 OVSJG Grant Recipients', 'FY23 OVSJG Grant Recipients', 'FY22 OVSJG Grant Recipients', 'FY21 OVSJG Grant Recipients', 'FY20&nbsp;OVSJG Grant Recipients', 'FY19 OVSJG Grant Recipients', 'FY18 OVSJG Grant Recipients', 'FY17 OVSJG Grant Recipients']
- OVSJG recipients FY2026: 23 pp (23 with text); Calvary pages: 3; peer page counts: House of Ruth 1, My Sister's Place 2, DASH 1, New Endeavors by Women 1, SOME 1, Catholic Charities 2
- OVSJG recipients FY2025: 5 pp (5 with text); Calvary pages: 1; peer page counts: House of Ruth 2, My Sister's Place 1, DASH 1, New Endeavors by Women 1, SOME 1, Catholic Charities 1
  - p1: CALVARY WOMEN'S SERVICES, INC New Foundations Transitional Housing 10/1/2024 - 9/30/2025 $ 519,656.00 Victim Service Local Melanie Kujawa Victim Services
  - p1: CALVARY WOMEN'S SERVICES, INC Reach Up Transitional Housing 10/1/2024 - 9/30/2025 $ 478,622.00 Victim Service Local Melanie Kujawa Victim Services
- OVSJG recipients FY2024: 2 pp (2 with text); Calvary pages: 1; peer page counts: House of Ruth 1, My Sister's Place 1, DASH 1, SOME 1, Catholic Charities 1
  - p1: Calvary Women's Services, Inc. New Foundations Transitional Housing Provide 15 beds of transitional housing and wraparound services, serving at least 35 unaccom
  - p1: Calvary Women's Services, Inc. Reach Up Transitional Housing Provide 15 beds of transitional housing and wraparound services, serving at least 35 unaccompanied 
- POH2024 DHS responses (Pre-Hearing-Responses-DHS-02.28.2024.pdf, 5.6 MB): 134 pp (107 with text); Calvary pages: 97,111; peer page counts: N Street Village 4, Miriam's Kitchen 1, Friendship Place 5, Pathways to Housing DC 2, House of Ruth 3, My Sister's Place 1, DASH 2, Community of Hope 6, New Endeavors by Women 1, Coalition for the Homeless 2, Catholic Charities 11, Christ House 1, The Community Partnership (TCP) 2
  - p97: Calvary Women's Services,Calvary Women's
  - p97: Calvary Women's Services,Calvary Women's
  - p97: Calvary Women's Services,Calvary Women's
  - p97: Calvary Women's Services,Calvary Women's
  - p97: Calvary Women's Services,Calvary Women's
  - p97: Calvary Women's Services,Calvary Women's
  - p111: Calvary Women's Services Calvary Transitional Housing $830,384.15 45 36
  - p111: Calvary Women's Services Sisters Rise (EHV) $593,280.00 25 does not
- POH2024 ICH responses (Pre-Hearing-Responses-ICH-02.27.2024.pdf, 0.5 MB): 33 pp (33 with text); Calvary pages: -; peer page counts: Friendship Place 1, The Community Partnership (TCP) 10
- POH2024 ICH attachments (Pre-Hearing-Attachments-ICH-02.27.2024.pdf, 2.7 MB): 108 pp (104 with text); Calvary pages: -; peer page counts: N Street Village 1, Miriam's Kitchen 1, Friendship Place 5, Pathways to Housing DC 2, My Sister's Place 1, Community of Hope 8, Coalition for the Homeless 2, Catholic Charities 6, The Community Partnership (TCP) 18
- POH2024 OVSJG responses (OVSJG-FY23-24-Oversight-Pre-Hearing-Questions_final.pdf, 1.3 MB): 41 pp (41 with text); Calvary pages: -; peer page counts: House of Ruth 1, DASH 1, SOME 1, Catholic Charities 2, Thrive DC 1
- POH2024 DBH responses (FY-23-Oversight-Pre-Hearing-Responses.-DBH_UPDATED.pdf, 1.3 MB): 118 pp (118 with text); Calvary pages: -; peer page counts: Catholic Charities 5
- POH2025 DHS responses (DHS-Combined-POH-Responses-3.3.2025.pdf, 2.3 MB): 183 pp (182 with text); Calvary pages: 58; peer page counts: N Street Village 6, Miriam's Kitchen 3, Friendship Place 7, Pathways to Housing DC 3, House of Ruth 4, My Sister's Place 3, DASH 5, Community of Hope 7, New Endeavors by Women 1, Coalition for the Homeless 4, SOME 1, Catholic Charities 20, Christ House 1, The Community Partnership (TCP) 11
  - p58: Calvary Women's Services: 1217 Good Hope Road SE 3 0 3
- POH2025 DHS attachments (dhsatt25.pdf, 35.0 MB): 616 pp (518 with text); Calvary pages: -; peer page counts: N Street Village 1, Miriam's Kitchen 1, Friendship Place 3, Pathways to Housing DC 1, My Sister's Place 1, Community of Hope 4, Catholic Charities 3
- POH2025 ICH responses (ICH-Response-_2025-03-04-SUBMISSION.pdf, 1.3 MB): 53 pp (53 with text); Calvary pages: -; peer page counts: Friendship Place 2, Pathways to Housing DC 1, Community of Hope 2, Coalition for the Homeless 1, Catholic Charities 2, Thrive DC 1, The Community Partnership (TCP) 9
- POH2025 ICH attachments (ichatt.pdf, 0.7 MB): 77 pp (76 with text); Calvary pages: -; peer page counts: The Community Partnership (TCP) 10
- POH2025 OVSJG responses (FINAL-OVSJG-FY24-25-Prehearing-questions.pdf, 2.1 MB): 46 pp (46 with text); Calvary pages: -; peer page counts: House of Ruth 2, DASH 1, Catholic Charities 5
- POH2025 DBH attachments (dbhatt.pdf, 13.0 MB): 5238 pp (1804 with text); Calvary pages: -; peer page counts: Miriam's Kitchen 25, Friendship Place 25, Pathways to Housing DC 27, House of Ruth 25, Community of Hope 36, New Endeavors by Women 18, SOME 35, Catholic Charities 25
- POH2026 DHS responses (DHS-Responses-to-Pre-FY25-POH-Questions-FINAL.pdf, 2.2 MB): 241 pp (240 with text); Calvary pages: -; peer page counts: N Street Village 1, House of Ruth 3, My Sister's Place 1, DASH 7, Catholic Charities 1, The Community Partnership (TCP) 6
- POH2026 OVSJG responses (OVSJG-POH-FY25-26-Responses.pdf, 0.9 MB): 39 pp (39 with text); Calvary pages: -
- POH2026 OVSJG attachments (ovsjgatt.pdf, 0.8 MB): 28 pp (23 with text); Calvary pages: 21; peer page counts: House of Ruth 3, New Endeavors by Women 1, Catholic Charities 3
  - p21: CALVARY WOMEN'S SERVICES,
- POH2026 DHCD responses (DHCD-Reponses-to-POH-Pre-Questions-.pdf, 1.4 MB): 132 pp (131 with text); Calvary pages: -
- BO_FY24 JA0 att_I_contracts_grants (JA0_FY24_Attachment-I.pdf, 0.1 MB): 1 pp (1 with text); Calvary pages: 1; peer page counts: Friendship Place 1, House of Ruth 1, DASH 1, Community of Hope 1, Catholic Charities 1, The Community Partnership (TCP) 1
  - p1: Covenant House; Calvary Women's Service
- BO_FY24 FO0 att_I_contracts_grants (FO0_FY24_Attachment-I.pdf, 0.1 MB): 1 pp (1 with text); Calvary pages: -
- BO_FY24 RM0 att_I_contracts_grants (RM0_FY24_Attachment-I.pdf, 0.6 MB): 3 pp (3 with text); Calvary pages: -; peer page counts: N Street Village 1, Pathways to Housing DC 2
- BO_FY25 JA0 att_I_contracts_grants (JA0_FY25_-Attachment-I-Contracts-Grants.pdf, 0.2 MB): 3 pp (3 with text); Calvary pages: 2; peer page counts: Friendship Place 1, House of Ruth 1, DASH 1, Community of Hope 1, Catholic Charities 2, The Community Partnership (TCP) 1
  - p2: Covenant House; Calvary Women's Service;
- BO_FY25 DB0 att_I_contracts_grants (DB0-Attachment-I-Contracts-Grants.pdf, 0.1 MB): 3 pp (3 with text); Calvary pages: -
- BO_FY26 JA0 att_I_contracts_grants (JA0_FY26-Attachment-I.pdf, 0.2 MB): 3 pp (3 with text); Calvary pages: -; peer page counts: Friendship Place 1, House of Ruth 1, DASH 1, Community of Hope 1, Catholic Charities 1, The Community Partnership (TCP) 1
- BO_FY26 JA0 att_III_grants (JA0_FY26-Attachment-III-Grants-Federal-Payments-Lapses.pdf, 0.2 MB): 3 pp (3 with text); Calvary pages: -
- BO_FY26 FO0 att_I_contracts_grants (FO0_FY26_Attachment-I.pdf, 0.1 MB): 3 pp (3 with text); Calvary pages: -
- BO_FY26 RM0 att_I_contracts_grants (RM0_FY26_Attachment-I.pdf, 0.5 MB): 4 pp (4 with text); Calvary pages: -; peer page counts: N Street Village 1, Pathways to Housing DC 2
- BO_FY26 DB0 att_I_contracts_grants (DB0-Attachment-I-Contracts-Grants.pdf, 0.2 MB): 3 pp (3 with text); Calvary pages: -
- BO_FY26 CF0 att_I_contracts_grants (CF0_FY26_-Attachment-I.pdf, 0.2 MB): 10 pp (10 with text); Calvary pages: -
- BO_FY27 JA0 att_I_contracts_grants (JA0_FY27_Attachment-I.pdf, 0.1 MB): 1 pp (1 with text); Calvary pages: -
- BO_FY27 JA0 att_III_grants (JA0_FY27_Attachment-III.pdf, 0.2 MB): 1 pp (1 with text); Calvary pages: -
- BO_FY27 FO0 att_I_contracts_grants (FO0_FY27_Attachment-I.pdf, 0.1 MB): 3 pp (3 with text); Calvary pages: -
- BO_FY27 DB0 att_I_contracts_grants (DB0_FY27_Attachment-I-Contracts-Grants.pdf, 0.1 MB): 1 pp (1 with text); Calvary pages: -
- BO_FY27 CF0 att_I_contracts_grants (CF0_FY27_Attachment-I.pdf, 0.3 MB): 5 pp (5 with text); Calvary pages: -
- BO_FY27 OVSJG budget_prehearing_responses (FY27-OVSJG-Budget-Pre-Hearing-Questions_FINAL.pdf, 0.2 MB): 6 pp (6 with text); Calvary pages: -
- BR_FY25 Housing (DHS, DHCD, DCHA, ICH) committee_budget_report (Circulation-Draft-Budget-Report-Committee-on-Housing-FY25-05.08.2024.pdf, 2.2 MB): 165 pp (165 with text); Calvary pages: -
- BR_FY25 JPS (OVSJG) committee_budget_report (JPS-FY-25-Budget-Report-DRAFT.pdf, 0.9 MB): 96 pp (96 with text); Calvary pages: -
- BR_FY26 Human Services (DHS, ICH) committee_budget_report (Human-Services_FY26-Budget-Recommendations-and-Report-Circulation-Draft_updaetd-622pm.pdf, 1.8 MB): 92 pp (92 with text); Calvary pages: -; peer page counts: The Community Partnership (TCP) 2; homeless pp: 4,7,10,15,32,34-38,43-48,60-62,64,67,69,72,77,79,84,...; PSH pp: 10,36,44,79
- BR_FY26 Housing (DHCD, DCHA) committee_budget_report (Housing_FY26-Budget-Recommendations-and-Report-Updated-circulation-draft.pdf, 1.7 MB): 96 pp (95 with text); Calvary pages: -; homeless pp: 4-5,33; PSH pp: -
- BR_FY26 JPS (OVSJG) committee_budget_report (JPS_FY26-Budget-Recommendations-and-Report-Revised-Draft-624am.pdf, 4.1 MB): 179 pp (179 with text); Calvary pages: -; peer page counts: DASH 1; homeless pp: 106,108; PSH pp: -
- BR_FY26 Health (DBH) committee_budget_report (Health_FY26-Budget-Recommendations-and-Report-Revised-Draft-1.pdf, 6.1 MB): 179 pp (168 with text); Calvary pages: -; peer page counts: Pathways to Housing DC 1; homeless pp: 69,83,86,149; PSH pp: 59
- BR_FY27 All agencies council_operating_changes_chart (Net-Operating-Budget-Adjustments-Chart-2nd-Reading-Circulation_final_6212026.pdf, 0.9 MB): 120 pp (120 with text); Calvary pages: -; peer page counts: Community of Hope 1; homeless pp: 43-45,102; PSH pp: 44
- BR_FY27 All agencies lba_changes_1st_to_2nd_reading (LBA-Budget-Adjustments-Showing-Changes-Between-1st-and-2nd-Reading_final_6212026.pdf, 0.2 MB): 18 pp (18 with text); Calvary pages: -; homeless pp: -; PSH pp: -
- BR_FY27 BSA bsa_committee_print_packet (B26-661-FY27-BSA-COMMITTEE-PACKET.pdf, 4.8 MB): 643 pp (643 with text); Calvary pages: -; peer page counts: Friendship Place 3, DASH 1, SOME 1; homeless pp: 8,22,25,44,125,140,149,278,286,394,429,459,495; PSH pp: 25,497,499
- BR_FY27 Housing (DHCD, DCHA) committee_budget_report (FY27-Committee-on-Housing-Budget-Report-Markup-Draft_revised.pdf, 3.2 MB): 126 pp (126 with text); Calvary pages: 52; peer page counts: House of Ruth 1; homeless pp: 19,36-37,68-69; PSH pp: -
  - p52: o Calvary Women’s
- BR_FY27 Health (DBH) committee_budget_report (DRAFT-FY2027-Committee-on-Health-Budget-Recommendations-Report.pdf, 2.7 MB): 143 pp (143 with text); Calvary pages: -; peer page counts: Community of Hope 1, Catholic Charities 2; homeless pp: 5,11,64,68,92,96,109; PSH pp: -
- BR_FY27 JPS (OVSJG) committee_budget_report (52226-FY2027-JPS-Budget-Report_DRAFT_Recirculated-with-Tables.pdf, 11.7 MB): 124 pp (124 with text); Calvary pages: -; homeless pp: 94; PSH pp: -
- BSA FY2024 (D.C. Law 25-50. Fiscal Year 2024 Budget Support Act of 2023.): 86 subtitles; relevant: DISTRICT OF COLUMBIA HOUSING AUTHORITY PROCUREMENT CLARIFICATION; TAX ABATEMENTS FOR AFFORDABLE HOUSING IN HIGH-NEED AREAS; DOWNTOWN HOUSING; EMERGENCY HOUSING ASSISTANCE PROGRAM FINANCIAL RESPONSIBILITY; EMERGENCY RENTAL ASSISTANCE FUNDS REPORTING AND NOTICE REQUIREMENTS; HOUSING AUTHORITY ACCOUNTABILITY; HOUSING AUTHORITY FINANCIAL REPORTING; PUBLIC HOUSING STABILITY; HOUSING PRODUCTION TRUST FUND; GRANDPARENT AND CAREGIVER SUBSIDY ELIGIBILITY EXPANSION; SCHOOL-BASED BEHAVIORAL HEALTH STUDENT PEER EDUCATOR PILOT; DEPARTMENT OF BEHAVIORAL HEALTH TARGETED OUTREACH GRANTS; DEPARTMENT OF HUMAN SERVICES GRANT
- BSA FY2025 (D.C. Law 25-217. Fiscal Year 2025 Budget Support Act of 2024.): 134 subtitles; relevant: LOCAL RENT SUPPLEMENT PROGRAM ACCOUNTS; EMERGENCY RENTAL ASSISTANCE PROGRAM REPORTS; HOUSING SUBSIDY CONTRACT EXTENSIONS; HOUSING PRESERVATION FUND; FEDERAL CITY SHELTER AND CCNV REDEVELOPMENT PLANNING; DC LOW-INCOME HOUSING TAX CREDIT; HOUSING FOR VICTIMS OF DOMESTIC VIOLENCE FUND CLARIFICATION; GRANDPARENT AND CLOSE RELATIVE CAREGIVER PROGRAM ELIGIBILITY EXPANSION; RAPID RE-HOUSING; CHILDCARE FOR PREGNANT AND BIRTHING PARENTS GRANTS; SCHOOL-BASED BEHAVIORAL HEALTH STUDENT PEER EDUCATOR PILOT; SUBSTANCE ABUSE AND BEHAVIORAL HEALTH SERVICES TARGETED OUTREACH GRANTS; DEPARTMENT OF HUMAN SERVICES GRANT; CORPORATE SHORT-TERM STAY HOUSING IN DOWNTOWN
- BSA FY2026 (D.C. Law 26-55. Fiscal Year 2026 Budget Support Act of 2025.): 111 subtitles; relevant: HUMAN SERVICES GRANT ADMINISTRATION; HOUSING IN DOWNTOWN PROGRAM; HOUSING PRODUCTION TRUST FUND; TANF BENEFITS; RAPID REHOUSING PROGRAMS; SCHOOL-BASED BEHAVIORAL HEALTH STRENGTHENING; SUBSTANCE USE AND BEHAVIORAL HEALTH SERVICES TARGETED OUTREACH PILOT; DEPARTMENT OF HUMAN SERVICES GRANT; NONPROFIT WORKFORCE HOUSING PROPERTIES
- BSA FY2027_emergency (D.C. Act 26-416. Fiscal Year 2027 Budget Support Emergency Act of 2026.): 153 subtitles; relevant: DISTRICT EMPLOYEE PAID PARENTAL, FAMILY, AND MEDICAL LEAVE; RENT PAYMENT REPORTING PROGRAM; WORKFORCE HOUSING OPPORTUNITY TAX ABATEMENT; LRSP VOUCHERS FOR FAMILIES EXITING RAPID REHOUSING; NONPROFIT AFFORDABLE HOUSING DEVELOPMENT TAX RELIEF CLARIFICATION; HOUSING PRODUCTION TRUST FUND; RAPID RE-HOUSING; SCHOOL-BASED BEHAVIORAL HEALTH PROGRAM STABILIZATION AND OVERSIGHT; TANF BENEFITS; DEPARTMENT OF HUMAN SERVICES GRANTS; HUMAN SERVICES PATHWAYS TO INDEPENDENCE; HUMAN SERVICES RESOURCE UTILIZATION; TANF ELIGIBILITY DURING PREGNANCY; HOTEL AND RENTAL CAR TAX

### 2026-10-10 12:32 — 14_probe_dc_hud: run summary
- bytes saved this run: raw/dc_council 117.9 MB, raw/dc_gov 1.3 MB; total 119.3 MB
- failures (0): none

### 2026-10-10 12:32 — lead: MAR 2 key check
- DC_MAR_API_KEY now set; /locations/{address} returns HTTP 200 for Calvary: MAR_ID 338288, Ward 8, ANC 8A, tract 007503, lat/lon. MAR also returns tract, so Phase 5 uses MAR for DC addresses and the Census geocoder for MD/VA. Catalog row for MAR 2 to be updated from blocked_needs_key to ok at the merge.

### 2026-10-10 12:33 — 11_eval_xml_tooling: irsx
- pip install irsx: rc 0; irsx/python: 0.5.1 3.12.13
- Python 3.13 venv: install rc 0, import ok
- cafritz_990pf TY2024 202513399349100006: {"version": "2024v5.2", "supported": true, "parsed_schedules": ["ReturnHeader990x", "IRS990PF"], "keyerrors": 0, "keyerror_sample": [], "PF_grants": 452, "PF_grants_sum": 23052750.0, "PF_parts": ["pf_part_0", "pf_part_i", "pf_part_ii", "pf_part_iii", "pf_part_iv", "pf_part_vi", "pf_part_viia", "pf_part_viib", "pf_part_viii", "pf_part_x", "pf_part_xi", "pf_part_xv", "pf_part_xvii"], "PF_groups": {"PFCpGnsLssTxInvstIncm": 1, "PFOrgRprtOrRgstrSttCd": 1, "PFOffcrDrTrstKyEmpl": 12, "PFCmpnstnHghstPdEmpl": 5, "PFCmpnstnOfHghstPdCntrct": 5, "pf_part_ixb": 1, "pf_part_xiii": 1, "PFApplctnSbmssnInf": 1, "PFGrntOrCntrbtnPdDrYr": 452, "PFOthrRvnDscrbd": 2, "pf_part_xvia": 1, "PFRlnOfActyTAccmOfExmptPrps": 1}}
- calvary_990 TY2019 202130449349300208: {"version": "2019v5.2", "supported": true, "parsed_schedules": ["ReturnHeader990x", "IRS990", "IRS990ScheduleA", "IRS990ScheduleB", "IRS990ScheduleD", "IRS990ScheduleG", "IRS990ScheduleM", "IRS990ScheduleO"], "keyerrors": 0, "keyerror_sample": [], "IRS990_CYTotalRevenueAmt": "3896046", "IRS990_part_viii_keys": 23, "IRS990_groups": {"part_iii": 3, "SttsWhrCpyOfRtrnIsFldCd": 1, "Frm990PrtVIISctnA": 17, "part_viii": 1, "OthrExpnss": 4, "part_ix": 1, "part_x": 4, "part_xii": 1}}
- calvary_990 TY2020 202212279349301511: {"version": "2020v4.2", "supported": true, "parsed_schedules": ["ReturnHeader990x", "IRS990", "IRS990ScheduleA", "IRS990ScheduleB", "IRS990ScheduleD", "IRS990ScheduleG", "IRS990ScheduleI", "IRS990ScheduleJ", "IRS990ScheduleM", "IRS990ScheduleO"], "keyerrors": 0, "keyerror_sample": [], "IRS990_CYTotalRevenueAmt": "3851984", "IRS990_part_viii_keys": 19, "IRS990_groups": {"part_iii": 3, "Frm990PrtVIISctnA": 21, "OthrExpnss": 4, "part_ix": 1, "part_x": 5, "part_xii": 1}, "SI_grants": 0}
- calvary_990 TY2021 202322239349302102: {"version": "2021v4.2", "supported": true, "parsed_schedules": ["ReturnHeader990x", "IRS990", "IRS990ScheduleA", "IRS990ScheduleB", "IRS990ScheduleD", "IRS990ScheduleG", "IRS990ScheduleI", "IRS990ScheduleJ", "IRS990ScheduleM", "IRS990ScheduleO"], "keyerrors": 0, "keyerror_sample": [], "IRS990_CYTotalRevenueAmt": "8867250", "IRS990_part_viii_keys": 24, "IRS990_groups": {"part_iii": 3, "PrgSrvcAccmActyOthr": 2, "Frm990PrtVIISctnA": 22, "CntrctrCmpnstn": 1, "part_viii": 1, "OthrRvnMsc": 1, "OthrExpnss": 4, "part_ix": 1, "part_x": 5, "part_xii": 1}, "SI_grants": 0}
- calvary_990 TY2022 202401649349300215: {"version": "2022v5.0", "supported": true, "parsed_schedules": ["ReturnHeader990x", "IRS990", "IRS990ScheduleA", "IRS990ScheduleB", "IRS990ScheduleD", "IRS990ScheduleG", "IRS990ScheduleI", "IRS990ScheduleJ", "IRS990ScheduleM", "IRS990ScheduleO"], "keyerrors": 0, "keyerror_sample": [], "IRS990_CYTotalRevenueAmt": "4456814", "IRS990_part_viii_keys": 23, "IRS990_groups": {"part_iii": 3, "PrgSrvcAccmActyOthr": 2, "Frm990PrtVIISctnA": 21, "CntrctrCmpnstn": 1, "part_viii": 1, "OthrExpnss": 4, "part_ix": 1, "part_x": 4, "part_xii": 1}, "SI_grants": 0}
- calvary_990 TY2023 202542169349300419: {"version": "2023v6.0", "supported": true, "parsed_schedules": ["ReturnHeader990x", "IRS990", "IRS990ScheduleA", "IRS990ScheduleB", "IRS990ScheduleD", "IRS990ScheduleG", "IRS990ScheduleI", "IRS990ScheduleJ", "IRS990ScheduleM", "IRS990ScheduleO"], "keyerrors": 0, "keyerror_sample": [], "IRS990_CYTotalRevenueAmt": "5817167", "IRS990_part_viii_keys": 25, "IRS990_groups": {"part_iii": 3, "PrgSrvcAccmActyOthr": 2, "Frm990PrtVIISctnA": 23, "part_viii": 1, "OthrRvnMsc": 2, "OthrExpnss": 4, "part_ix": 1, "part_x": 4, "part_xii": 1}, "SI_grants": 0}
- calvary_990 TY2024 202631539349300848: {"version": "2024v5.5", "supported": true, "parsed_schedules": ["ReturnHeader990x", "IRS990", "IRS990ScheduleA", "IRS990ScheduleB", "IRS990ScheduleD", "IRS990ScheduleG", "IRS990ScheduleI", "IRS990ScheduleJ", "IRS990ScheduleM", "IRS990ScheduleO"], "keyerrors": 0, "keyerror_sample": [], "IRS990_CYTotalRevenueAmt": "4967995", "IRS990_part_viii_keys": 19, "IRS990_groups": {"part_iii": 3, "PrgSrvcAccmActyOthr": 2, "Frm990PrtVIISctnA": 22, "OthrExpnss": 4, "part_x": 5, "part_xii": 1}, "SI_grants": 0}
- gwcf_990 TY2023 202520389349300807: {"version": "2023v6.0", "supported": true, "parsed_schedules": ["ReturnHeader990x", "IRS990", "IRS990ScheduleA", "IRS990ScheduleB", "IRS990ScheduleC", "IRS990ScheduleD", "IRS990ScheduleF", "IRS990ScheduleG", "IRS990ScheduleI", "IRS990ScheduleJ", "IRS990ScheduleM", "IRS990ScheduleO"], "keyerrors": 0, "keyerror_sample": [], "IRS990_CYTotalRevenueAmt": "99984918", "IRS990_part_viii_keys": 36, "IRS990_groups": {"part_iii": 3, "SttsWhrCpyOfRtrnIsFldCd": 2, "Frm990PrtVIISctnA": 35, "CntrctrCmpnstn": 5, "part_viii": 2, "OthrRvnMsc": 2, "OthrExpnss": 3, "part_x": 10, "part_xii": 1}, "SI_grants": 1163}
- gwcf_990 TY2024 202640449349302259: {"version": "2024v5.1", "supported": true, "parsed_schedules": ["ReturnHeader990x", "IRS990", "IRS990ScheduleA", "IRS990ScheduleB", "IRS990ScheduleC", "IRS990ScheduleD", "IRS990ScheduleF", "IRS990ScheduleG", "IRS990ScheduleI", "IRS990ScheduleJ", "IRS990ScheduleM", "IRS990ScheduleO", "IRS990ScheduleR"], "keyerrors": 0, "keyerror_sample": [], "IRS990_CYTotalRevenueAmt": "123242853", "IRS990_part_viii_keys": 39, "IRS990_groups": {"part_iii": 3, "SttsWhrCpyOfRtrnIsFldCd": 2, "Frm990PrtVIISctnA": 31, "CntrctrCmpnstn": 5, "part_viii": 1, "OthrRvnMsc": 3, "OthrExpnss": 4, "part_ix": 1, "part_x": 13}, "SI_grants": 1417, "SR_groups": {"SkdRIdRltdTxExmptOrg": 1}}
- meyer_990pf TY2021 202233149349102223: {"version": "2021v4.2", "supported": true, "parsed_schedules": ["ReturnHeader990x", "IRS990PF"], "keyerrors": 0, "keyerror_sample": [], "PF_grants": 170, "PF_grants_sum": 9889546.0, "PF_parts": ["pf_part_0", "pf_part_i", "pf_part_ii", "pf_part_iii", "pf_part_iv", "pf_part_vi", "pf_part_viia", "pf_part_viib", "pf_part_viii", "pf_part_x", "pf_part_xi", "pf_part_xv", "pf_part_xvii"], "PF_groups": {"PFCpGnsLssTxInvstIncm": 17, "PFOrgRprtOrRgstrSttCd": 2, "PFOffcrDrTrstKyEmpl": 13, "PFCmpnstnHghstPdEmpl": 5, "PFCmpnstnOfHghstPdCntrct": 5, "pf_part_ixa": 1, "pf_part_ixb": 1, "pf_part_xiii": 1, "PFApplctnSbmssnInf": 1, "PFGrntOrCntrbtnPdDrYr": 170, "PFGrntOrCntrApprvFrFt": 42, "PFOthrRvnDscrbd": 3, "pf_part_xvia": 1}}
- meyer_990pf TY2022 202303119349102405: {"version": "2022v5.0", "supported": true, "parsed_schedules": ["ReturnHeader990x", "IRS990PF"], "keyerrors": 0, "keyerror_sample": [], "PF_grants": 166, "PF_grants_sum": 11027775.0, "PF_parts": ["pf_part_0", "pf_part_i", "pf_part_ii", "pf_part_iii", "pf_part_iv", "pf_part_vi", "pf_part_viia", "pf_part_viib", "pf_part_viii", "pf_part_x", "pf_part_xi", "pf_part_xv", "pf_part_xvii"], "PF_groups": {"PFCpGnsLssTxInvstIncm": 8, "PFOrgRprtOrRgstrSttCd": 2, "PFOffcrDrTrstKyEmpl": 12, "PFCmpnstnHghstPdEmpl": 5, "PFCmpnstnOfHghstPdCntrct": 5, "pf_part_ixa": 1, "pf_part_ixb": 1, "pf_part_xiii": 1, "PFApplctnSbmssnInf": 1, "PFGrntOrCntrbtnPdDrYr": 166, "PFGrntOrCntrApprvFrFt": 43, "PFOthrRvnDscrbd": 5, "pf_part_xvia": 1}}
- meyer_990pf TY2023 202443119349102189: {"version": "2023v5.1", "supported": true, "parsed_schedules": ["ReturnHeader990x", "IRS990PF"], "keyerrors": 0, "keyerror_sample": [], "PF_grants": 177, "PF_grants_sum": 11003160.0, "PF_parts": ["pf_part_0", "pf_part_i", "pf_part_ii", "pf_part_iii", "pf_part_iv", "pf_part_vi", "pf_part_viia", "pf_part_viib", "pf_part_viii", "pf_part_x", "pf_part_xi", "pf_part_xv", "pf_part_xvii"], "PF_groups": {"PFCpGnsLssTxInvstIncm": 19, "PFOrgRprtOrRgstrSttCd": 2, "PFOffcrDrTrstKyEmpl": 16, "PFCmpnstnHghstPdEmpl": 5, "PFCmpnstnOfHghstPdCntrct": 5, "pf_part_ixb": 1, "pf_part_xiii": 1, "PFApplctnSbmssnInf": 1, "PFGrntOrCntrbtnPdDrYr": 177, "PFGrntOrCntrApprvFrFt": 45, "PFOthrRvnDscrbd": 4, "pf_part_xvia": 1}}
- meyer_990pf TY2024 202512959349101021: {"version": "2024v5.2", "supported": true, "parsed_schedules": ["ReturnHeader990x", "IRS990PF"], "keyerrors": 0, "keyerror_sample": [], "PF_grants": 274, "PF_grants_sum": 13550350.0, "PF_parts": ["pf_part_0", "pf_part_i", "pf_part_ii", "pf_part_iii", "pf_part_iv", "pf_part_vi", "pf_part_viia", "pf_part_viib", "pf_part_viii", "pf_part_x", "pf_part_xi", "pf_part_xv", "pf_part_xvii"], "PF_groups": {"PFCpGnsLssTxInvstIncm": 22, "PFOrgRprtOrRgstrSttCd": 2, "PFOffcrDrTrstKyEmpl": 15, "PFCmpnstnHghstPdEmpl": 5, "PFCmpnstnOfHghstPdCntrct": 5, "pf_part_ixb": 1, "pf_part_xiii": 1, "PFApplctnSbmssnInf": 1, "PFGrntOrCntrbtnPdDrYr": 274, "PFGrntOrCntrApprvFrFt": 57, "PFOthrRvnDscrbd": 2, "pf_part_xvia": 1}}

### 2026-10-10 12:34 — 14_probe_dc_hud: HUD CoC / PIT / HIC and MWCOG
- AHAR 2025 Part 1 page data files: ['2007-2025-PIT-Counts-by-CoC.xlsb', '2007-2025-PIT-Counts-by-State.xlsb', '2007-2025-HIC-Counts-by-CoC.xlsx', '2007-2025-HIC-Counts-by-State.xlsx', '2011-2025-PIT-Veteran-Counts-by-CoC.xlsx', '2011-2025-PIT-Veteran-Counts-by-State.xlsx', '2025-HIC-Counts-by-State.csv']
- 2007-2025-PIT-Counts-by-CoC.xlsb: 30 sheets (2025..PIT_Counts_Chart_Template); DC-500 rows in '2025': 1; {}
- 2007-2025-HIC-Counts-by-CoC.xlsx: 20 sheets (2025..Revisions); DC-500 rows in '2025': 1; {'Total Year-Round Beds (ES, TH, SH)': 4965, 'Total Year-Round Beds (PSH)': 12696}
- AwardComp DC-500 2019: total $22,075,117; Calvary lines: p2: Calvary Women's Service - Sister Circle Renewal project $239,659.00
- AwardComp DC-500 2020: total $23,608,105; Calvary lines: p2: Calvary Women's Service - Sister Circle Renewal project $248,131.00
- AwardComp DC-500 2021: total $25,062,775; Calvary lines: p2: Calvary Women's Service - Sister Circle Renewal project $250,135.00 | p3: Calvary Women's Services - Reach Up Renewal project $1,222,263.00
- AwardComp DC-500 2022: total $27,933,554; Calvary lines: p2: Calvary Women's Services - Sister Circle Renewal project $250,135.00 | p3: Calvary Women's Services - Reach Up Reallocation New project $421,930.00
- AwardComp DC-500 2023: total $29,711,325; Calvary lines: p2: Calvary Women's Services - Sister Circle Renewal project $254,491.00 | p3: Calvary Women's Services - New Foundations 2 New project $469,719.00 | p3: Calvary Women's Services - Reach Up Renewal project $427,330.00
- AwardComp DC-500 2024: total $33,659,924; Calvary lines: p2: Calvary Women's Services - Sister Circle Renewal project $296,926.00 | p3: Calvary Women's Services - Reach Up Expansion project $921,970.00 | p3: Calvary Women's Services - New Foundations 2 Renewal project $542,456.00
- hud.gov FY2024 DC award report: p1: Calvary Women's Services - New Foundations 2 CoC $542,456 | p1: Calvary Women's Services - Reach Up CoC $479,538 | p1: Calvary Women's Services - Reach Up (Expansion) CoC $442,432 | p1: Calvary Women's Services - Sister Circle CoC $296,926
- FY2025 CoC award announcement round 1: 71 pp; DC-500 pages 12; Calvary: p12: Calvary Women's Services - New Foundations 2 CoC $546,247 | p12: Calvary Women's Services - Sister Circle CoC $296,930
- FY2025 CoC award announcement round 2: 127 pp; DC-500 pages 22; Calvary: p22: Calvary Women's Services - Reach Up CoC $923,637
- FY2025 CoC award announcement round 3: 224 pp; DC-500 pages 37; Calvary: none
- FY2024 DC-500 GIW read failed: sequence item 2: expected str instance, float found
- FY2026 DC-500 GIW read failed: sequence item 2: expected str instance, float found
- HIC DC-500 2022: 16 pp; Calvary rows: p4: Calvary Women's Services Reach Up TH (Joint RRH TH 0 0 6 0 n/a n/a 6 n/a 0 0 | p4: Calvary Women's Services Reach UP TH TCP Funded 0 0 10 0 n/a n/a 10 n/a 0 0 | p4: Calvary Women's Services Calvary Women's Transitional 0 0 29 0 n/a n/a 29 n/a 0 0 | p7: Calvary Women's Services Sister Circle 0 0 16 0 n/a n/a 16 16 0 0 | p13: Calvary Women's Services Reach Up RRH (joint RRH T 0 0 7 0 n/a n/a 7 n/a 0 0
- HIC DC-500 2023: 14 pp; Calvary rows: p4: Calvary Women's Services Reach up OVSJG 0 0 12 0 n/a n/a 12 n/a 0 0 | p4: Calvary Women's Services Reach UP TH TCP Funded 0 0 10 0 n/a n/a 10 n/a 0 0 | p4: Calvary Women's Services Reach Up TH (Joint RRH TH 0 0 6 0 n/a n/a 6 n/a 0 0 | p4: Calvary Women's Services Calvary Women's Transitional 0 0 45 0 n/a n/a 45 n/a 0 0 | p7: Calvary Women's Services Sister Circle 0 0 16 0 n/a n/a 16 16 0 0 | p12: Calvary Women's Services Reach Up RRH (joint RRH T 0 0 9 0 n/a n/a 9 n/a 0 0
- HIC DC-500 2024: 15 pp; Calvary rows: p4: Calvary Women's Services (CWS) (Agenc CWS - Reach Up - TH IND - 0 0 6 0 n/a n/a 6 n/a 0 0 | p4: Calvary Women's Services (CWS) (Agenc CWS - Reach Up - TH IND - 0 0 10 0 n/a n/a 10 n/a 0 0 | p4: Calvary Women's Services (CWS) (Agenc CWS - Reach Up OVSJG - T 0 0 15 0 n/a n/a 15 n/a 0 0 | p4: Calvary Women's Services (CWS) (Agenc CWS - Transitional Housing - 0 0 29 0 n/a n/a 29 n/a 0 0 | p7: Calvary Women's Services (CWS) (Agenc CWS - Sisters Rise - PSH IN 0 0 24 0 n/a n/a 24 0 0 0 | p7: Calvary Women's Services (CWS) (Agenc CWS - Sister Circle - PSH IN 0 0 16 0 n/a n/a 16 16 0 0 | p13: Calvary Women's Services (CWS) (Agenc CWS - Reach Up - RRH IND 0 0 7 0 n/a n/a 7 n/a 0 0
- HIC DC-500 2025: 14 pp; Calvary rows: p4: Calvary Women's Services (CWS) (Agenc CWS - Reach Up - TH IND - 0 0 6 0 n/a n/a 6 n/a 0 0 | p4: Calvary Women's Services (CWS) (Agenc CWS - Reach Up - TH IND - 0 0 8 0 n/a n/a 8 n/a 0 0 | p4: Calvary Women's Services (CWS) (Agenc CWS - Transitional Housing - 0 0 45 0 n/a n/a 45 n/a 0 0 | p4: Calvary Women's Services (CWS) (Agenc CWS - Reach Up OVSJG - T 0 0 18 0 n/a n/a 18 n/a 0 0 | p4: Calvary Women's Services (CWS) (Agenc CWS - New Foundations - TH 0 0 17 0 n/a n/a 17 n/a 0 0 | p7: Calvary Women's Services (CWS) (Agenc CWS - Sister Circle - PSH IN 0 0 16 0 n/a n/a 16 16 0 0 | p13: Calvary Women's Services (CWS) (Agenc CWS - Reach Up - RRH IND 0 0 14 0 n/a n/a 14 n/a 0 0
- PopSub DC-500 2024: 3 pp
- PopSub DC-500 2025: 3 pp
- MWCOG report page lists 20 annual reports
- MWCOG 2026 PIT report (5.1 MB): 131 pp (131 with text); Calvary pages: -; peer page counts: Pathways to Housing DC 1, Coalition for the Homeless 1, SOME 1, The Community Partnership (TCP) 7; DC pages: 9-10,13,17-18,22-26,28,32-39,42,44,46,48-51,53-57,59-63,67,69,75,...; ward pp: -
- MWCOG 2025 PIT report (11.2 MB): 194 pp (192 with text); Calvary pages: -; peer page counts: Friendship Place 1, Pathways to Housing DC 6, Coalition for the Homeless 1, SOME 2, The Community Partnership (TCP) 9; DC pages: 2-3,7-9,11-12,17-18,20-23,26,28-29,31-33,45,47-48,50-53,59-60,65,76,100,...; ward pp: -
- MWCOG 2024 PIT report (8.3 MB): 195 pp (194 with text); Calvary pages: -; peer page counts: Friendship Place 1, Pathways to Housing DC 5, Coalition for the Homeless 2, SOME 2, The Community Partnership (TCP) 9; DC pages: 2-3,8,12,16-17,19-20,22-23,29-33,46,48-49,51-54,56,60,66,78,93,...; ward pp: -
- MWCOG 2023 PIT report (7.6 MB): 182 pp (180 with text); Calvary pages: -; peer page counts: Friendship Place 1, Pathways to Housing DC 5, Coalition for the Homeless 4, SOME 1, The Community Partnership (TCP) 12; DC pages: 2-3,8-9,12,15-17,19-20,22-23,25-28,40-42,44-46,48,51-53,58,71,93,98,...; ward pp: -

### 2026-10-10 12:34 — 14_probe_dc_hud: run summary
- bytes saved this run: raw/hud 54.6 MB; total 54.6 MB
- failures (0): none

### 2026-10-10 12:35 — 10_probe_filings: remotezip
- 52 ZIP names for 2021-2026 (downloads page + index batch ids); 52 reachable (HTTP 200, Accept-Ranges); not reachable: none
  - 2021: 1 ZIPs, 3.72 GB, 589,904 members, central directories 55.5 MB
  - 2022: 2 ZIPs, 4.01 GB, 656,503 members, central directories 62.6 MB
  - 2023: 12 ZIPs, 4.29 GB, 705,154 members, central directories 65.6 MB
  - 2024: 12 ZIPs, 4.39 GB, 728,719 members, central directories 67.8 MB
  - 2025: 16 ZIPs, 4.46 GB, 748,906 members, central directories 56.2 MB
  - 2026: 9 ZIPs, 2.56 GB, 436,239 members, central directories 32.7 MB
  - 2021_TEOS_XML_01A: 3,715.5 MB, 589,904 members, CD 55.5 MB, Thu, 06 Mar 2025 20:08:25 GMT, page
  - 2022_TEOS_XML_01A: 2,603.7 MB, 433,529 members, CD 41.2 MB, Thu, 06 Mar 2025 20:08:56 GMT, page
  - 2022_TEOS_XML_02A: 1,408.2 MB, 222,974 members, CD 21.4 MB, Thu, 06 Mar 2025 20:06:10 GMT, probe_only
  - 2023_TEOS_XML_01A: 123.1 MB, 21,513 members, CD 2.0 MB, Thu, 06 Mar 2025 17:04:40 GMT, page
  - 2023_TEOS_XML_02A: 234.6 MB, 40,304 members, CD 3.7 MB, Thu, 06 Mar 2025 17:07:26 GMT, page
  - 2023_TEOS_XML_03A: 197.2 MB, 36,224 members, CD 3.4 MB, Thu, 06 Mar 2025 17:06:19 GMT, page
  - 2023_TEOS_XML_04A: 244.5 MB, 42,995 members, CD 4.0 MB, Thu, 06 Mar 2025 17:07:59 GMT, page
  - 2023_TEOS_XML_05A: 990.5 MB, 156,228 members, CD 14.5 MB, Thu, 06 Mar 2025 17:27:59 GMT, page
  - 2023_TEOS_XML_06A: 163.7 MB, 29,240 members, CD 2.7 MB, Thu, 06 Mar 2025 17:05:35 GMT, page
  - 2023_TEOS_XML_07A: 219.9 MB, 38,027 members, CD 3.5 MB, Thu, 06 Mar 2025 17:07:06 GMT, page
  - 2023_TEOS_XML_08A: 266.2 MB, 42,301 members, CD 3.9 MB, Thu, 06 Mar 2025 17:08:23 GMT, page
  - 2023_TEOS_XML_09A: 200.4 MB, 35,070 members, CD 3.3 MB, Thu, 06 Mar 2025 17:06:29 GMT, page
  - 2023_TEOS_XML_10A: 332.5 MB, 56,858 members, CD 5.3 MB, Thu, 06 Mar 2025 17:10:21 GMT, page
  - 2023_TEOS_XML_11A: 1,200.3 MB, 186,387 members, CD 17.3 MB, Thu, 06 Mar 2025 17:32:53 GMT, page
  - 2023_TEOS_XML_12A: 120.7 MB, 20,007 members, CD 1.9 MB, Thu, 06 Mar 2025 17:04:34 GMT, page
  - 2024_TEOS_XML_01A: 104.8 MB, 17,246 members, CD 1.6 MB, Thu, 06 Mar 2025 14:04:31 GMT, page
  - 2024_TEOS_XML_02A: 243.7 MB, 40,284 members, CD 3.7 MB, Thu, 06 Mar 2025 14:04:23 GMT, page
  - 2024_TEOS_XML_03A: 209.3 MB, 38,418 members, CD 3.6 MB, Thu, 06 Mar 2025 14:04:55 GMT, page
  - 2024_TEOS_XML_04A: 350.3 MB, 59,487 members, CD 5.5 MB, Thu, 06 Mar 2025 14:05:02 GMT, page
  - 2024_TEOS_XML_05A: 977.5 MB, 156,237 members, CD 14.5 MB, Thu, 06 Mar 2025 14:05:40 GMT, page
  - 2024_TEOS_XML_06A: 163.9 MB, 29,408 members, CD 2.7 MB, Thu, 06 Mar 2025 14:04:01 GMT, page
  - 2024_TEOS_XML_07A: 288.3 MB, 50,144 members, CD 4.7 MB, Thu, 06 Mar 2025 14:04:23 GMT, page
  - 2024_TEOS_XML_08A: 260.6 MB, 41,687 members, CD 3.9 MB, Thu, 06 Mar 2025 14:04:56 GMT, page
  - 2024_TEOS_XML_09A: 247.0 MB, 44,108 members, CD 4.1 MB, Thu, 06 Mar 2025 14:04:54 GMT, page
  - 2024_TEOS_XML_10A: 251.6 MB, 43,392 members, CD 4.0 MB, Thu, 06 Mar 2025 14:04:55 GMT, page
  - 2024_TEOS_XML_11A: 1,165.6 MB, 186,632 members, CD 17.4 MB, Thu, 06 Mar 2025 14:05:48 GMT, page
  - 2024_TEOS_XML_12A: 128.3 MB, 21,676 members, CD 2.0 MB, Thu, 06 Mar 2025 14:04:05 GMT, page
  - 2025_TEOS_XML_01A: 103.7 MB, 17,044 members, CD 1.3 MB, Wed, 05 Mar 2025 15:12:42 GMT, page
  - 2025_TEOS_XML_02A: 239.9 MB, 41,855 members, CD 3.1 MB, Wed, 19 Mar 2025 13:01:47 GMT, page
  - 2025_TEOS_XML_03A: 222.6 MB, 41,570 members, CD 3.1 MB, Wed, 16 Apr 2025 13:01:48 GMT, page
  - 2025_TEOS_XML_04A: 338.2 MB, 57,595 members, CD 4.3 MB, Wed, 21 May 2025 13:09:56 GMT, page
  - 2025_TEOS_XML_05A: 495.9 MB, 81,770 members, CD 6.1 MB, Wed, 25 Jun 2025 13:13:15 GMT, page
  - 2025_TEOS_XML_05B: 501.0 MB, 81,770 members, CD 6.1 MB, Wed, 25 Jun 2025 13:13:33 GMT, page
  - 2025_TEOS_XML_06A: 246.8 MB, 44,824 members, CD 3.4 MB, Wed, 20 Aug 2025 13:11:59 GMT, page
  - 2025_TEOS_XML_07A: 143.5 MB, 24,854 members, CD 1.9 MB, Wed, 20 Aug 2025 13:08:44 GMT, page
  - 2025_TEOS_XML_08A: 262.7 MB, 42,291 members, CD 3.2 MB, Wed, 17 Sep 2025 13:18:06 GMT, page
  - 2025_TEOS_XML_09A: 256.3 MB, 45,643 members, CD 3.4 MB, Wed, 19 Nov 2025 20:41:59 GMT, page
  - 2025_TEOS_XML_10A: 56.5 MB, 9,836 members, CD 0.7 MB, Wed, 19 Nov 2025 14:08:07 GMT, page
  - 2025_TEOS_XML_11A: 340.1 MB, 55,488 members, CD 4.2 MB, Wed, 17 Dec 2025 14:31:07 GMT, page
  - 2025_TEOS_XML_11B: 494.5 MB, 80,283 members, CD 6.0 MB, Wed, 17 Dec 2025 14:43:04 GMT, page
  - 2025_TEOS_XML_11C: 277.9 MB, 44,896 members, CD 3.4 MB, Wed, 17 Dec 2025 14:25:37 GMT, page
  - 2025_TEOS_XML_11D: 332.8 MB, 53,800 members, CD 4.0 MB, Wed, 17 Dec 2025 17:10:02 GMT, page
  - 2025_TEOS_XML_12A: 151.8 MB, 25,387 members, CD 1.9 MB, Wed, 21 Jan 2026 14:14:30 GMT, page
  - 2026_TEOS_XML_01A: 71.5 MB, 12,245 members, CD 0.9 MB, Thu, 19 Feb 2026 18:32:24 GMT, page
  - 2026_TEOS_XML_02A: 222.1 MB, 38,719 members, CD 2.9 MB, Wed, 18 Mar 2026 13:02:56 GMT, page
  - 2026_TEOS_XML_03A: 259.3 MB, 48,471 members, CD 3.6 MB, Wed, 15 Apr 2026 13:03:42 GMT, page
  - 2026_TEOS_XML_04A: 261.9 MB, 47,627 members, CD 3.6 MB, Wed, 20 May 2026 13:02:32 GMT, page
  - 2026_TEOS_XML_05A: 521.2 MB, 84,172 members, CD 6.3 MB, Wed, 17 Jun 2026 13:13:47 GMT, page
  - 2026_TEOS_XML_05B: 513.4 MB, 84,172 members, CD 6.3 MB, Wed, 17 Jun 2026 13:13:52 GMT, page
  - 2026_TEOS_XML_06A: 210.8 MB, 38,244 members, CD 2.9 MB, Wed, 15 Jul 2026 16:01:18 GMT, page
  - 2026_TEOS_XML_07A: 189.2 MB, 32,240 members, CD 2.4 MB, Wed, 19 Aug 2026 13:00:50 GMT, page
  - 2026_TEOS_XML_08A: 314.7 MB, 50,349 members, CD 3.8 MB, Wed, 16 Sep 2026 13:02:45 GMT, index_only
  - release 2021: index rows 589,904 vs ZIP members 589,904 (diff +0)
  - release 2022: index rows 656,503 vs ZIP members 656,503 (diff +0)
  - release 2023: index rows 705,156 vs ZIP members 705,154 (diff -2)
  - release 2024: index rows 728,719 vs ZIP members 728,719 (diff +0)
  - release 2025: index rows 748,906 vs ZIP members 748,906 (diff +0)
  - release 2026: index rows 436,239 vs ZIP members 436,239 (diff +0)
  - 2025_TEOS_XML_05A vs 2025_TEOS_XML_05B: 81,770 / 81,770 object ids, overlap 0; index rows labelled 2025_TEOS_XML_05A: 163,540, found in 2025_TEOS_XML_05A 81,770, in 2025_TEOS_XML_05B 81,770 (read 12.4 MB of central directory)
  - 2026_TEOS_XML_05A vs 2026_TEOS_XML_05B: 84,172 / 84,172 object ids, overlap 0; index rows labelled 2026_TEOS_XML_05A: 168,344, found in 2026_TEOS_XML_05A 84,172, in 2026_TEOS_XML_05B 84,172 (read 12.8 MB of central directory)
- remotezip 2026_TEOS_XML_06A (210.8 MB, 38,244 members, names like 202601429339300000_public.xml): central directory 2 requests / 2.9 MB; member 202631539349300848_public.xml 54,115 B (10,872 B compressed); total 3 requests / 2.9 MB = 1.40% of the ZIP; 0.4s -> raw/xml/irs/20261010T122754_521307706_TY2024_2026_TEOS_XML_06A_202631539349300848_public.xml
- 2026_TEOS_XML_06A: mean member 28.7 KB uncompressed, compression ratio 5.3x
- GT S3 copy of 202631539349300848 byte-identical to the IRS ZIP member: True

### 2026-10-10 12:35 — 10_probe_filings: volume
- BMF sets: (a) DMV PF filers (FOUNDATION 02/03/04 or PF_FILING_REQ_CD=1) 5,855 EINs; (b) DC 501(c)(3) public charities in NTEE L/P/F/I/J/W 1,750 EINs
- (a: DMV 990-PF filers) 25,367 returns from 5,249 EINs; by type {'990PF': 25367}; by tax year {2018: 22, 2019: 397, 2020: 3884, 2021: 4256, 2022: 4527, 2023: 4835, 2024: 4912, 2025: 2534}; by release year {2021: 3679, 2022: 4169, 2023: 4553, 2024: 4872, 2025: 5068, 2026: 3026}; same EIN+period+type repeats (amended/superseded) 213
  - after keeping the latest OBJECT_ID per EIN+TAX_PERIOD+type: 25,154 returns; TY2020-TY2024 22,210
  - ZIP batches: 52 distinct ZIPs touched (2021_TEOS_XML_01A 3679, 2022_ANY 4169, 2023_ANY 4553, 2024_TEOS_XML_01A 72, 2024_TEOS_XML_02A 185, 2024_TEOS_XML_03A 195, 2024_TEOS_XML_04A 386, 2024_TEOS_XML_05A 1326, 2024_TEOS_XML_06A 182, 2024_TEOS_XML_07A 256, 2024_TEOS_XML_08A 258, 2024_TEOS_XML_09A 260, 2024_TEOS_XML_10A 240, 2024_TEOS_XML_11A 1407, 2024_TEOS_XML_12A 105, 2025_TEOS_XML_01A 69, 2025_TEOS_XML_02A 185, 2025_TEOS_XML_03A 274, 2025_TEOS_XML_04A 417, 2025_TEOS_XML_05* 1363, 2025_TEOS_XML_06A 283, 2025_TEOS_XML_07A 131, 2025_TEOS_XML_08A 186, 2025_TEOS_XML_09A 307, 2025_TEOS_XML_10A 43, 2025_TEOS_XML_11A 383, 2025_TEOS_XML_11B 568, 2025_TEOS_XML_11C 330, 2025_TEOS_XML_11D 416, 2025_TEOS_XML_12A 113, 2026_TEOS_XML_01A 42, 2026_TEOS_XML_02A 198, 2026_TEOS_XML_03A 327, 2026_TEOS_XML_04A 384, 2026_TEOS_XML_05* 1392, 2026_TEOS_XML_06A 219, 2026_TEOS_XML_07A 194, 2026_TEOS_XML_08A 270)
  - bytes: full ZIP downloads 23.4 GB; remotezip ~491 MB (central directories 340.3 MB + members ~151.1 MB compressed); GT S3 per-object ~805.3 MB uncompressed
- (b: DC public charities L/P/F/I/J/W) 4,580 returns from 968 EINs; by type {'990EZ': 670, '990': 3907, '990PF': 3}; by tax year {2018: 5, 2019: 215, 2020: 731, 2021: 812, 2022: 826, 2023: 883, 2024: 885, 2025: 223}; by release year {2021: 712, 2022: 783, 2023: 832, 2024: 874, 2025: 899, 2026: 480}; same EIN+period+type repeats (amended/superseded) 114
  - after keeping the latest OBJECT_ID per EIN+TAX_PERIOD+type: 4,466 returns; TY2020-TY2024 4,032
  - ZIP batches: 52 distinct ZIPs touched (2021_TEOS_XML_01A 712, 2022_ANY 783, 2023_ANY 832, 2024_TEOS_XML_01A 16, 2024_TEOS_XML_02A 26, 2024_TEOS_XML_03A 39, 2024_TEOS_XML_04A 60, 2024_TEOS_XML_05A 133, 2024_TEOS_XML_06A 47, 2024_TEOS_XML_07A 45, 2024_TEOS_XML_08A 78, 2024_TEOS_XML_09A 50, 2024_TEOS_XML_10A 63, 2024_TEOS_XML_11A 299, 2024_TEOS_XML_12A 18, 2025_TEOS_XML_01A 12, 2025_TEOS_XML_02A 38, 2025_TEOS_XML_03A 30, 2025_TEOS_XML_04A 56, 2025_TEOS_XML_05* 142, 2025_TEOS_XML_06A 46, 2025_TEOS_XML_07A 28, 2025_TEOS_XML_08A 90, 2025_TEOS_XML_09A 53, 2025_TEOS_XML_10A 15, 2025_TEOS_XML_11A 91, 2025_TEOS_XML_11B 114, 2025_TEOS_XML_11C 85, 2025_TEOS_XML_11D 78, 2025_TEOS_XML_12A 21, 2026_TEOS_XML_01A 14, 2026_TEOS_XML_02A 34, 2026_TEOS_XML_03A 46, 2026_TEOS_XML_04A 54, 2026_TEOS_XML_05* 130, 2026_TEOS_XML_06A 51, 2026_TEOS_XML_07A 59, 2026_TEOS_XML_08A 92)
  - bytes: full ZIP downloads 23.4 GB; remotezip ~368 MB (central directories 340.3 MB + members ~27.3 MB compressed); GT S3 per-object ~145.5 MB uncompressed

### 2026-10-10 12:36 — 12_probe_federal: usaspending DC probes
- CFDA titles (USAspending autocomplete): {"14.267": "Continuum of Care Program", "14.231": "Emergency Solutions Grant Program", "14.241": "Housing Opportunities for Persons with AIDS", "14.218": "Community Development Block Grants/Entitlement Grants", "14.239": "Home Investment Partnerships Program", "16.575": "Crime Victim Assistance", "16.588": "Violence Against Women Formula Grants", "16.736": "Transitional Housing Assistance for Victims of Domestic Violence, Dating Violence, Stalking, or Sexual Assault", "93.671": "Family Violence Prevention and Services/Domestic Violence Shelter and Supportive Services", "93.959": "Block Grants for Prevention and Treatment of Substance Abuse", "93.958": "Block Grants for Community Mental Health Services", "93.243": "Substance Abuse and Mental Health Services Projects of Regional and National Significance", "21.027": "CORONAVIRUS STATE AND LOCAL FISCAL RECOVERY FUNDS", "21.019": "Coronavirus Relief Fund", "97.024": "Emergency Food and Shelter National Board Program", "64.033": "VA Supportive Services for Veteran Families Program", "17.258": "WIOA Adult Program", "17.259": "WIOA Youth Activities", "16.812": "Second Chance Act Reentry Initiative", "14.235": "Supportive Housing Program", "10.561": "State Administrative Matching Grants for the Supplemental Nutrition Assistance Program", "14.251": "Economic Development Initiative, Community Project Funding, and Miscellaneous grants", "14.252": "Section 4 Capacity Building for Community Development and Affordable Housing", "59.073": "Paycheck Protection Loan Program (PPP)", "21.023": "Emergency Rental Assistance Program"}
- DC counts per CFDA FY2019-FY2026 (recipient in DC): {"14.267": {"grants": 494, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 2}, "14.231": {"grants": 12, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 1}, "14.241": {"grants": 11, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 103}, "14.218": {"grants": 11, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 137}, "14.239": {"grants": 11, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 4}, "16.575": {"grants": 10, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 116}, "16.588": {"grants": 11, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 42}, "16.736": {"grants": 7, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 0}, "93.671": {"grants": 19, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 5}, "93.959": {"grants": 12, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 69}, "93.958": {"grants": 16, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 55}, "93.243": {"grants": 77, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 256}, "21.027": {"grants": 0, "direct_payments": 5, "other": 0, "loans": 0, "subgrants": 0}, "21.019": {"grants": 0, "direct_payments": 2, "other": 0, "loans": 0, "subgrants": 0}, "97.024": {"grants": 0, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 0}, "64.033": {"grants": 36, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 0}, "17.258": {"grants": 10, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 1}, "17.259": {"grants": 9, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 1}, "16.812": {"grants": 9, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 26}, "14.235": {"grants": 0, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 0}, "10.561": {"grants": 64, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 15}, "14.251": {"grants": 21, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 0}, "14.252": {"grants": 0, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 71}, "59.073": {"grants": 0, "direct_payments": 0, "other": 0, "loans": 32800, "subgrants": 0}, "21.023": {"grants": 0, "direct_payments": 3, "other": 0, "loans": 0, "subgrants": 0}}
- DC prime probe: {"rows": 5836, "by_group": {"grants": 826, "direct_payments": 10, "loans": 5000}, "dc_gov_rows_name_match": 224, "dc_gov_amount": 4439095425, "dc_gov_by_cfda": {"10.561": 60, "14.267": 23, "93.671": 16, "93.958": 15, "93.959": 11, "14.241": 11, "16.588": 11, "14.231": 10, "16.575": 10, "93.243": 10, "14.239": 9, "14.218": 7, "93.243,93.788": 4, "17.258,17.259,17.278": 4, "21.027": 4, "17.259": 3, "17.258": 3, "21.023": 3, "14.218,14.228": 2, "16.812": 2, "21.019": 2, "14.218,14.248": 1, "93.00R,93.243": 1, "93.104,93.243": 1, "10.551,10.561": 1}, "dc_gov_recipient_names": {"DISTRICT COLUMBIA GOVERNMENT": 112, "GOVERNMENT OF THE DISTRICT OF COLUMBIA": 45, "DISTRICT OF COLUMBIA, GOVERNMENT OF": 27, "DC OFFICE OF VICTIM SERVICES": 21, "DISTRICT OF COLUMBIA GOVERNMENT OF": 10, "DISTRICT OF COLUMBIA GOVERNMENT": 9}, "recipient_type_government_counts": {"contracts": 0, "direct_payments": 10, "grants": 195, "idvs": 0, "loans": 0, "other": 0}, "calvary_rows": ["B-22-CP-DC-0213", "5639698601", "6371477100", "5894917008"]}
- DC subaward probe: {"rows": 891, "dc_gov_prime_rows": 546, "dc_gov_prime_amount": 177195890, "by_cfda": {"93.243, 93.788": 175, "14.218": 136, "16.575": 116, "14.241": 103, "14.252": 71, "93.243": 64, "93.959": 59, "93.958": 50, "16.588": 42, "10.561": 15, "16.812": 15, "16.735, 16.812": 11, "93.243, 93.959": 6, "93.243, 93.958": 5, "93.671": 5, "14.239": 4, "93.104, 93.243": 4, "93.590, 93.959": 4, "14.267": 2, "93.150, 93.243": 2, "17.258, 17.259, 17.278": 1, "14.231": 1}, "dc_gov_by_cfda": {"93.243, 93.788": 145, "14.218": 116, "14.241": 103, "16.575": 77, "93.959": 39, "16.588": 30, "93.958": 24, "93.243": 4, "93.104, 93.243": 4, "14.239": 3, "16.812": 1}, "prime_names": [["GOVERNMENT OF THE DISTRICT OF COLUMBIA", 216], ["DISTRICT OF COLUMBIA GOVERNMENT OF", 119], ["DISTRICT OF COLUMBIA, GOVERNMENT OF", 103], ["DC OFFICE OF VICTIM SERVICES", 82], ["LOCAL INITIATIVES SUPPORT CORPORATION", 45], ["ENTERPRISE COMMUNITY PARTNERS, INC.", 26], ["OFFICE OF VICTIM SERVICES AND JUSTICE GRANTS", 24], ["EXECUTIVE OFFICE OF THE STATE OF MARYLAND", 23], ["PUBLIC HEALTH AND HUMAN SERVICES, MONTANA DEPARTMENT OF", 22], ["PRINCE GEORGE'S COUNTY, MARYLAND", 17], ["ILLINOIS DEPARTMENT OF HUMAN SERVICE", 14], ["IMPACT JUSTICE", 13]], "by_year": {"2018": 49, "2019": 62, "2020": 120, "2021": 72, "2022": 64, "2023": 116, "2024": 150, "2025": 206, "2026": 52}, "calvary_rows": []}
- download/count sizing: {"dc_target_cfdas_grants_direct": {"awards": 836, "transactions": 2100, "subawards": 891}, "dc_all_grants": {"awards": 21168, "transactions": 79160, "subawards": 23709}, "dc_nonprofit_grants": {"awards": 9028, "transactions": 34073, "subawards": 2569}, "dc_pop_target_cfdas": {"awards": 818, "transactions": 2067, "subawards": 513}, "slfrf_21027_dc": {"awards": 5, "transactions": 9, "subawards": 0}}

### 2026-10-10 12:36 — 10_probe_filings: gt_marts
- 157 objects under EfileDataMarts/; 65 distinct marts; latest build of key marts:
  - 2026_06_16 All_Years_990EZStandardFields.csv: 1,548.5 MB
  - 2026_06_16 All_Years_990PFPart14Grants3A.csv: 5,875.9 MB
  - 2026_06_16 All_Years_990PFPart14Grants3B.csv: 172.4 MB
  - 2026_06_16 All_Years_990PFPart7p1Officers.csv: 1,228.1 MB
  - 2026_06_16 All_Years_990PFStandardFields.csv: 841.8 MB
  - 2026_06_16 All_Years_990Part1Missions.csv: 1,560.1 MB
  - 2026_06_16 All_Years_990Part3Programs.csv: 3,057.0 MB
  - 2026_06_16 All_Years_990StandardFields.csv: 3,179.9 MB
  - 2026_06_16 All_Years_990_990ez_990pf_990n_Combined_DataMart.csv: 3,490.3 MB
  - 2026_06_25 All_Years_ScheduleIPart2Grants.csv: 3,257.8 MB

### 2026-10-10 12:37 — 12_probe_federal: usaspending downloads
- download_awards_calvary: {"status": "finished", "total_rows": 3, "seconds": 12, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H16M36S53_1.csv": 2, "Assistance_Subawards_2026-10-10_H16M36S55_1.csv": 1}, "raw": "raw/usaspending/20261010T123659_download_awards_calvary.zip"}
- bulk_download_hud_dc_fy2024: {"status": "finished", "total_rows": 658, "seconds": 0, "members": {"All_Assistance_PrimeTransactions_2026-10-10_H16M24S40_1.csv": 893, "All_Assistance_Subawards_2026-10-10_H16M25S01_1.csv": 686}, "raw": "raw/usaspending/20261010T123701_bulk_download_hud_dc_fy2024.zip"}

### 2026-10-10 12:37 — 12_probe_federal: catalog
- wrote sources/catalog_parts/federal.csv; sections run: ['usaspending', 'usa_download']

### 2026-10-10 12:37 — 14_probe_dc_hud: DC Open Data / DC GIS
- hub search 'ward 2022': numberMatched 14; top: Crime Incidents in 2022; 311 City Service Requests in 2022; Wards from 2022; DC COVID 19 Cases by Ward; ACS 5-Year Economic Characteristics DC Ward; High Injury Network
- hub search 'census tracts 2020': numberMatched 43; top: Census Tracts in 2020; ACS 5-Year Social Characteristics DC Census Tract; ACS 5-Year Economic Characteristics DC Census Tract; ACS 5-Year Demographic Characteristics DC Census Tract; ACS 5-Year Housing Characteristics DC Census Tract; Census Block Groups in 2020
- hub search 'homeless': numberMatched 7; top: Homeless Service Facilities; Homeless Shelter Locations; Homeless Facility Shuttle Stops; Human Services Catchment Area; DC COVID 19 Shelter Vaccine Summary; Primary Care Facility
- hub search 'shelter': numberMatched 11; top: Homeless Shelter Locations; Homeless Service Facilities; DC COVID 19 Shelter Vaccine Summary; Homeless Facility Shuttle Stops; Human Services Catchment Area; Commuter Bus Stops
- hub search 'contracts': numberMatched 49; top: Contracts from PASS; Contract CBE Vendors; Forecast from PASS; Contractor Awarded Engagements; Purchase Orders from PASS; Payments from PASS
- hub search 'purchase orders': numberMatched 4; top: Purchase Orders from PASS; Contractor Awarded Engagements; Pipeline Contractor Awarded Engagments Archive; Payments from PASS
- hub search 'grants': numberMatched 18; top: DC Main Streets Business Sub Grants; Neighborhood Investment Fund Areas; Families First DC Communities; My Out of School Time; OVSJG Grant Recipients; Community-Based Dementia Care
- hub search 'budget': numberMatched 17; top: Payments from PASS; Solicitations from PASS; Forecast from PASS; Purchase Orders from PASS; High Injury Network; Contracts from PASS
- hub search 'victim': numberMatched 1; top: OVSJG Grant Recipients
- DCAT feed: 1871 datasets; 42 titles match homeless/contract/ward/budget terms
- layer wards_2022 (Administrative_Other_Boundaries_WebMercator/MapServer/53): name 'Ward - 2022', 21 fields, maxRecordCount 1000
- layer census_tracts_2020 (Demographic_WebMercator/MapServer/8): name 'Census Tracts - 2020', 316 fields, maxRecordCount 1000
- layer homeless_shelters (Public_Service_WebMercator/MapServer/25): name 'Homeless Shelter Locations', 33 fields, maxRecordCount 1000
- layer homeless_service_facilities (Public_Service_WebMercator/MapServer/6): name 'Homeless Service Facilities', 67 fields, maxRecordCount 1000
- layer ovsjg_grant_recipients (Public_Safety_WebMercator/MapServer/35): name 'OVSJG Grant Recipients', 9 fields, maxRecordCount 1000
- layer pass_contracts (Government_Operations/MapServer/37): name 'PASS Contracts', 45 fields, maxRecordCount 1000
- layer pass_purchase_orders (Government_Operations/MapServer/16): name 'PASS Purchase Orders', 19 fields, maxRecordCount 1000
- layer pass_payments (Government_Operations/MapServer/17): name 'PASS Payments', 22 fields, maxRecordCount 1000
- wards_2022 GeoJSON: 8 features; WARD values [1, 2, 3, 4, 5, 6, 7, 8]
- census_tracts_2020 GeoJSON: 206 features (fields TRACT, GEOID, NAME, POP100, HU100, ALAND, AWATER)
- homeless_shelters: 19 rows, active beds 2,763; Calvary rows: none (layer covers DHS low-barrier/TH shelters only)
- homeless_service_facilities: 115 rows; Calvary rows: none
- ovsjg_grant_recipients: 1267 rows; FY counts 2016: 69 ($26.9M), 2017: 78 ($29.1M), 2018: 77 ($38.4M), 2019: 239 ($96.7M), 2020: 129 ($47.5M), 2021: 134 ($54.6M), 2022: 168 ($90.9M), 2023: 132 ($71.6M), 2024: 121 ($62.9M), 2025: 120 ($92.7M)
- ovsjg_grant_recipients Calvary rows (AGENCY field = grantee): FY2019 Reach Up Transitional Housing Program $368,935; FY2019 Reach Up Transitional Housing Program $292,000; FY2020 Reach Up Transitional Housing Program $368,935; FY2021 Reach Up Transitional Housing Program $368,935; FY2022 New Foundations Transitional Housing Program $3,680,675; FY2022 Reach Up Transitional Housing Program $368,935; FY2022 Reach Up Transitional Housing Program $99,500; FY2023 New Foundations Transitional Housing Program $438,500; FY2023 Reach Up Transitional Housing Program $402,540; FY2024 New Foundations Transitional Housing $482,528; FY2024 Reach Up Transitional Housing $430,873; FY2025 New Foundations Transitional Housing $519,656; FY2025 Reach Up Transitional Housing $478,622
- PASS purchase orders, supplier like CALVARY WOM: 10 rows: FY2019 OVSJG FY19 - OVSJG - VS - 2019-CWSH-01  -  CALVARY  $208,372; FY2020 OVSJG FY20 - OVSJG - VS - 2020-CWSH-01  -  CALVARY  $368,395; FY2021 OVSJG FY21 - OVSJG - VS - 2021-CWSH-01  - Calvary W $482,423; FY2021 DHCD FY21 IDIS#2764 Calvary Women Services Covid-1 $32,298; FY2022 OVSJG FY22 - OVSJG - VS - 2022-CWSH-01  -  CALVARY  $468,435; FY2022 DHS Calvary Women's Services - SNAP E&T FY22 $62,899; FY2022 OVSJG FY22 - OVSJG - VS - 2022-CWSH-02  -  CALVARY  $3,680,675; FY2023 OVSJG FY23 - OVSJG - VS - 2023-CWSH-01  -  CALVARY  $402,540; FY2023 OVSJG FY23 - OVSJG - VS - 2023-CWSH-02  -  CALVARY  $343,887; FY2023 DHS Calvary Women's Services - SNAP E&T FY23 $68,544
- PASS payments to CALVARY WOM*: 95 rows; by FY/agency: FY2019 OVSJG $73,603; FY2020 OVSJG $476,040; FY2021 DHCD $32,298; FY2021 OVSJG $327,634; FY2022 DHS $15,183; FY2022 OVSJG $3,910,132; FY2023 DHS $109,084; FY2023 OVSJG $1,461,366; FY2024 DHS $3,024; FY2024 OVSJG $1,116,183
- PASS contracts (OCP awards >= $100K), supplier like CALVARY: 0 rows
- PASS POs to THE COMMUNITY PARTNERSHIP: 148 rows; DHS by FY: FYNone $1.9M, FY2013 $82.2M, FY2014 $95.3M, FY2015 $108.8M, FY2016 $119.0M, FY2017 $91.0M, FY2018 $98.2M, FY2019 $104.9M, FY2020 $101.5M, FY2021 $112.4M, FY2022 $131.6M, FY2023 $108.3M, FY2024 $110.4M, FY2025 $7.1M, FY2026 $71.1M
- PASS PO duplicate rows removed for peers (AA0 sub-office fan-out): 146
- PASS PO totals by peer supplier (all years): N Street Village: 43 POs $7.5M, FY2013-2026, agency codes DB0/HC0/JA0/RM0; Miriam's Kitchen: 57 POs $21.5M, FY2013-2026, agency codes AA0/BX0/DB0/JA0/RM0; Friendship Place: 69 POs $64.3M, FY2013-2026, agency codes AA0/CF0/JA0; Pathways to Housing: 135 POs $52.6M, FY2013-2026, agency codes AA0/DB0/JA0/JM0/RM0; House of Ruth: 56 POs $23.1M, FY2013-2023, agency codes AA0/DB0/FO0/JA0/RL0; My Sister's Place: 70 POs $27.8M, FY2013-2025, agency codes AA0/BZ0/FO0/JA0/RL0; DASH: 0 POs $0.0M, FY---, agency codes -; Community of Hope: 132 POs $92.8M, FY2013-2026, agency codes AA0/HC0/HI0/JA0/RL0/RM0; New Endeavors by Women: 1 POs $0.0M, FY2021-2021, agency codes DB0; Coalition for the Homeless: 7 POs $1.3M, FY2017-2023, agency codes JA0; SOME: 0 POs $0.0M, FY---, agency codes -; Catholic Charities: 164 POs $92.0M, FY2013-2026, agency codes AA0/BY0/BZ0/CB0/FO0/GA0/HC0/JA0/JZ0/RL0/RM0; Christ House: 4 POs $0.2M, FY2013-2022, agency codes HC0/RM0; TCP: 148 POs $1,352.3M, FY2013-2026, agency codes FO0/GD0/HC0/JA0/RL0/RM0
- pass_purchase_orders: 279,712 rows, FISCALYEAR 2013-2027
- pass_contracts: 51,263 rows, FISCALYEAR 2005-2027
- pass_payments: 1,576,128 rows, FISCALYEAR 2017-2027

### 2026-10-10 12:37 — 14_probe_dc_hud: DC budget books (CFO approved chapters)
- FY2027 approved: agency pages found ['CF0', 'DB0', 'FO0', 'HG0', 'HY0', 'JA0', 'RM0']
- FY2026 approved: agency pages found ['CF0', 'DB0', 'FO0', 'HG0', 'HY0', 'JA0', 'RM0']
- FY2025 approved: agency pages found ['CF0', 'DB0', 'FO0', 'HG0', 'HY0', 'JA0', 'RM0']
  - FY2025 CF0: agency page links no FY2025 chapter/tables (['cf_does_capital_2026o.pdf', 'cf_does_chapter_2026o.pdf', 'cf_does_tables_2026o-1.pdf', 'cf_does_tables_2026o-2.pdf']); using fallback ['cf0_does_chapter_2025j.pdf', 'cf_does_tables_2025j.pdf']
- FY2024 CF0 cf_des_tables_2024j.pdf [Approved FY2024; 18 pp, 18 with text]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; tbl_prog_activity -; sched_30PBB 1-3; budget_changes -
- FY2024 CF0 cf_does_chapter_2024j.pdf [Approved FY2024; 12 pp, 12 with text]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; tbl_prog_activity 3-5; sched_30PBB 5; budget_changes 9-11
- FY2024 DB0 db_dhcd_chapter_2024j.pdf [Approved FY2024; 10 pp, 10 with text]: homeless -; PSH -; victim_svcs -; rent_supp 4,6,10; ICH -; tbl_prog_activity 3-5; sched_30PBB 5; budget_changes 8-9
  - activity codes: 2010 Affordable Housing Project Financing; 2045 Local Rent Supplement; 8100 HOUSING REGULATION ADMINISTRATION; 8120 Housing Resource Center
- FY2024 DB0 db_dhcd_tables_2024j.pdf [Approved FY2024; 14 pp, 14 with text]: homeless -; PSH -; victim_svcs -; rent_supp 1; ICH -; tbl_prog_activity -; sched_30PBB 1-2; budget_changes -
  - activity codes: 2010 AFFORDABLE HOUSING PROJECT FINANCING; 2045 LOCAL RENT SUPPLEMENT; 8120 HOUSING RESOURCE CENTER
- FY2024 FO0 fo_vsjg_chapter_2024j.pdf [Approved FY2024; 8 pp, 8 with text]: homeless -; PSH -; victim_svcs 1,3-7; rent_supp -; ICH -; tbl_prog_activity 3-4; sched_30PBB 4; budget_changes 5-7
  - activity codes: 4000 VICTIM SERVICES; 4010 Victim Services; 6040 Safe Housing-Gun Violence
- FY2024 FO0 fo_vsjg_tables_2024j.pdf [Approved FY2024; 11 pp, 11 with text]: homeless -; PSH -; victim_svcs 1-11; rent_supp -; ICH -; tbl_prog_activity -; sched_30PBB 1; budget_changes -
  - activity codes: 4010 VICTIM SERVICES; 6040 SAFE HOUSING-GUN VIOLENCE
- FY2024 HG0 hg_dmhhs_chapter_2024j.pdf [Approved FY2024; 5 pp, 5 with text]: homeless 1; PSH -; victim_svcs -; rent_supp -; ICH 1; tbl_prog_activity 3; sched_30PBB 3; budget_changes 4-5
- FY2024 HG0 hg_dmhhs_tables_2024j.pdf [Approved FY2024; 7 pp, 7 with text]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; tbl_prog_activity -; sched_30PBB 1; budget_changes -
- FY2024 HY0 hy_has_chapter_2024j.pdf [Approved FY2024; 5 pp, 5 with text]: homeless 3; PSH 4; victim_svcs -; rent_supp 1-5; ICH -; tbl_prog_activity 2-3; sched_30PBB 3; budget_changes 4-5
  - activity codes: 6000 LOCAL RENT SUPPLEMENT - TENANT BASED; 6020 Permanent Supp. Housing - Individual; 6035 Targeted Affordable Housing -Families; 6040 Targeted Affordable Housing -Individuals; 6050 Homeless Services -Admin; 7000 LOCAL RENT SUPPLEMENT - PROJECT AND SPONSOR
- FY2024 HY0 hy_has_tables_2024j.pdf [Approved FY2024; 6 pp, 6 with text]: homeless 1; PSH -; victim_svcs -; rent_supp 1-3; ICH -; tbl_prog_activity -; sched_30PBB 1; budget_changes -
  - activity codes: 6020 PERMANENT SUPP. HOUSING - INDIVIDUAL; 6035 TARGETED AFFORDABLE HOUSING -FAMILIES; 6040 TARGETED AFFORDABLE HOUSING -INDIVIDUALS; 6050 HOMELESS SERVICES -ADMIN
- FY2024 JA0 ja_dhs_chapter_2024j.pdf [Approved FY2024; 13 pp, 13 with text]: homeless 1,4-9,11-12; PSH 4-5,8-9,12; victim_svcs -; rent_supp 12; ICH -; tbl_prog_activity 3-5; sched_30PBB 5; budget_changes 9-12
  - activity codes: 5000 FAMILY SERVICES; 5013 Homeless Prevention; 5020 Domestic Violence Services; 5021 Transitional Housing Youth; 5022 Youth Services; 5023 Homeless Service Continuum - Youth; 5024 Permanent Supportive Housing - Youth; 5026 Transitional Age Youth Shelter; 5027 Rapid Rehousing - Youth; 5030 Homeless Services; 5032 Permanent Supportive Housing; 5034 Permanent Supportive Housing - Individuals; 5035 Permanent Supportive Housing - Families; 5037 Homeless Services Continuum - Families; 5038 Homeless Services Continuum-Individuals; 5039 Homeless Services Continuum - General
- FY2024 JA0 ja_dhs_tables_2024j.pdf [Approved FY2024; 13 pp, 13 with text]: homeless 2; PSH 2; victim_svcs -; rent_supp -; ICH -; tbl_prog_activity -; sched_30PBB 1-3; budget_changes -
  - activity codes: 5013 HOMELESS PREVENTION; 5020 DOMESTIC VIOLENCE SERVICES; 5021 TRANSITIONAL HOUSING YOUTH; 5022 YOUTH SERVICES; 5023 HOMELESS SERVICE CONTINUUM - YOUTH; 5024 PERMANENT SUPPORTIVE HOUSING - YOUTH; 5026 TRANSITIONAL AGE YOUTH SHELTER; 5027 RAPID REHOUSING - YOUTH; 5028 RAPID REHOUSING - INDIVIDUALS (RRH-I); 5029 RAPID REHOUSING - FAMILIES (RRH-F); 5030 HOMELESS SERVICES; 5032 PERMANENT SUPPORTIVE HOUSING; 5034 PERMANENT SUPPORTIVE HOUSING - INDIV; 5035 PERMANENT SUPPORTIVE HOUSING - FAMILIES; 5037 HOMELESS SERVICES CONTINUUM - FAMILIES; 5038 HOMELESS SERVICES CONTINUUM-INDIVIDUALS; 5039 HOMELESS SERVICES CONTINUUM - GENERAL
- FY2024 RM0 rm_dbh_crosswalk_2024j.pdf [stage?; 1 pp, 1 with text]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; tbl_prog_activity -; sched_30PBB -; budget_changes -
- FY2024 RM0 rm_dbh_tables_2024j.pdf [Approved FY2024; 20 pp, 20 with text]: homeless 2; PSH -; victim_svcs -; rent_supp -; ICH -; tbl_prog_activity -; sched_30PBB 1-5; budget_changes -
  - activity codes: 4830 ADULT SERVICES - FORENSIC - BHSS; 5830 BEHAVIORAL HEALTH SERVICES; 5831 BEHAVIORAL HEALTH SERVICES - ADULT; 5832 BEHAVIORAL HEALTH SERVICES - CHILD; 5836 BEHAVIORAL HEALTH SERVICES - PHARMACY; 5842 HOMELESS OUTREACH / MOBILE CRISIS - CPEP; 5883 DISASTER BEHAVIORAL HEALTH & SUPPORT SVC; 6501 ADULT/TRANSITIONAL YOUTH SERVICES ADMIN; 6502 BEHAVIORAL HEALTH SERVICES MH/SUD; 6507 HOUSING SUPPORT SERVICES; 6515 BEHAVIORAL HEALTH REHAB. - LOCAL MATCH; 6601 CHILD/ADOLESCENT/FAMILY SERVICES ADMIN; 6610 BEHAVIORAL HEALTH SERVICES MH/SUD; 6615 SUD PREVENTION & TREATMENT; 6620 SCHOOL BASED BEHAVIORAL HEALTH SERVICES; 6625 CRISIS SERVICES; 6704 BEHAVIORAL HEALTH BLOCK GRANT PROGRAM; 6910 PREVENTION AND EARLY INTERVENTION; 6911 PREVENTION/EARLY INTERVEN-EARLY CHLDHOOD; 6912 PREVENTION/EARLY INTERVEN-SCH MENT HLTH; 6913 PREVENTION SUBSTANCE USE DISORDER; 6940 HOUSING DEVELOPMENT; 6970 BEHAVIORAL HEALTH REHAB; 6980 BEHAVIORAL HEALTH REHAB- LOCAL MATCH
- FY2024 RM0 rm_dbh_chapter_2023j_0.pdf [Approved FY2024; 18 pp, 18 with text]: homeless 5,11; PSH -; victim_svcs -; rent_supp -; ICH -; tbl_prog_activity 3-8; sched_30PBB 8; budget_changes 14-17
  - activity codes: 1800 BEHAVIORAL HEALTH AUTHORITY; 5830 Behavioral Health Services; 5831 Behavioral Health Services - Adult; 5832 Behavioral Health Services - Child; 5836 Behavioral Health Services - Pharmacy; 5842 Homeless Outreach / Mobile Crisis - CPEP; 5883 Disaster Behavioral Health & Support Svc; 6500 ADULT/TRANSITIONAL YOUTH SERVICES; 6501 Adult/Transitional Youth Services Admin; 6502 Behavioral Health Services MH/SUD; 6507 Housing Support Services; 6515 Behavioral Health Rehabilitation - Local Match; 6600 CHILD/ADOLESCENT/FAMILY SERVICES; 6601 Child/Adolescent/Family Services Admin; 6610 Behavioral Health Services MH/SUD; 6615 SUD Prevention & Treatment; 6620 School Based Behavioral Health Services; 6625 Crisis Services; 6704 Behavioral Health Block Grant Program; 6800 ADDICTION PREVENTION AND RECOVERY ADMINISTRATION; 6910 Prevention and Early Intervention; 6911 Prevention/Early Intervention-Early Childhood; 6912 Prevention/Early Intervention-Sch Mental Health; 6913 Prevention Substance Use Disorder; 6940 Housing Development; 6970 Behavioral Health Rehab; 6980 Behavioral Health Rehab- Local Match
- FY2025 CF0 cf0_does_chapter_2025j.pdf [Approved FY2025; 12 pp, 12 with text]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; tbl_prog_activity 3-6; sched_30PBB 6; budget_changes 9-11
- FY2025 CF0 cf_does_tables_2025j.pdf [Approved FY2025; 20 pp, 20 with text]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; tbl_prog_activity -; sched_30PBB 1-3; budget_changes -
- FY2025 DB0 db0_dhcd_chapter_2025j.pdf [Approved FY2025; 10 pp, 10 with text]: homeless -; PSH -; victim_svcs -; rent_supp 9; ICH -; tbl_prog_activity 3-5; sched_30PBB -; budget_changes 9
- FY2025 DB0 db_dhcd_tables_2025j.pdf [Approved FY2025; 14 pp, 14 with text]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; tbl_prog_activity -; sched_30PBB 1-2; budget_changes -
  - activity codes: R02004 HOUSING COUNSELING
- FY2025 FO0 fo0_ovsjg_chapter_2025j.pdf [Approved FY2025; 8 pp, 8 with text]: homeless -; PSH -; victim_svcs 1-8; rent_supp -; ICH -; tbl_prog_activity 3-5; sched_30PBB -; budget_changes 7
- FY2025 FO0 fo_ovsjg_crosswalk_2025j_0.pdf [stage?; 1 pp, 1 with text]: homeless -; PSH -; victim_svcs 1; rent_supp -; ICH -; tbl_prog_activity -; sched_30PBB -; budget_changes -
- FY2025 FO0 fo_ovsjg_tables_2025j.pdf [Approved FY2025; 13 pp, 13 with text]: homeless -; PSH -; victim_svcs 1-13; rent_supp -; ICH -; tbl_prog_activity -; sched_30PBB 1-2; budget_changes -
  - activity codes: P02303 VICTIM SERVICES GRANTS; P04502 EMERGENCY AND TRADITIONAL HOUSING
- FY2025 HG0 hg0_dmhhs_chapter_2025j.pdf [Approved FY2025; 6 pp, 5 with text]: homeless 1; PSH -; victim_svcs -; rent_supp -; ICH 1; tbl_prog_activity 3; sched_30PBB -; budget_changes 4
- FY2025 HG0 hg_dmhhs_tables_2025j.pdf [Approved FY2025; 7 pp, 7 with text]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; tbl_prog_activity -; sched_30PBB 1; budget_changes -
- FY2025 HY0 hy0_hap_chapter_2025j.pdf [Approved FY2025; 4 pp, 4 with text]: homeless -; PSH 4; victim_svcs -; rent_supp 1,3-4; ICH -; tbl_prog_activity 2; sched_30PBB -; budget_changes 4
- FY2025 HY0 hy_hap_tables_2025j.pdf [Approved FY2025; 7 pp, 7 with text]: homeless -; PSH -; victim_svcs -; rent_supp 1; ICH -; tbl_prog_activity -; sched_30PBB 1; budget_changes -
  - activity codes: R03904 AFFORDABLE HOUSING; R03905 LOCAL RENT SUPPLEMENT; R03907 LOCAL RENT SUPPLMENT - PROJECT & SPONSOR BASED
- FY2025 JA0 ja0_dhs_chapter_2025j.pdf [Approved FY2025; 14 pp, 13 with text]: homeless 1,7-9,12-13; PSH 7-8,11-12; victim_svcs -; rent_supp -; ICH -; tbl_prog_activity 3-6; sched_30PBB -; budget_changes 11-13
- FY2025 JA0 ja_dhs_tables_2025j.pdf [Approved FY2025; 14 pp, 14 with text]: homeless 1-2,4-5; PSH 2,5; victim_svcs -; rent_supp -; ICH -; tbl_prog_activity -; sched_30PBB 1-2; budget_changes -
  - activity codes: H03002 HOMELESS SERVICES CONTINUUM - FAMILIES; H03003 HOMELESS SERVICES CONTINUUM - GENERAL; H03004 HOMELESS SERVICES CONTINUUM-INDIVIDUALS; H03007 DOMESTIC VIOLENCE SERVICES; H03009 HOMELESS SERVICE CONTINUUM - YOUTH; H03010 PERMANENT SUPPORTIVE HOUSING FAMILIES; H03011 PERMANENT SUPPORTIVE HOUSING GENERAL; H03012 PERMANENT SUPPORTIVE HOUSING INDIVIDUALS; H03013 PERMANENT SUPPORTIVE HOUSING YOUTH; H03014 PREVENTION SERVICES FAMILIES; H03015 PREVENTION SERVICES INDIVIDUALS; H03016 PREVENTION SERVICES YOUTH; H03017 RAPID REHOUSING - FAMILIES; H03018 RAPID REHOUSING - INDIVIDUALS; H03019 RAPID REHOUSING - YOUTH; H03022 TRANSITIONAL AGE YOUTH SHELTER; H03023 TRANSITIONAL HOUSING YOUTH; H03024 YOUTH SERVICES: ACE PROGRAM; H03025 YOUTH SERVICES: DIVERSION PROGRAM (STEP); H03026 YOUTH SERVICES: PASS PROGRAM; H03027 YOUTH SERVICES: TEEN PREGNANCY PROGRAM
- FY2025 RM0 rm0_dbh_chapter_2025j.pdf [Approved FY2025; 18 pp, 18 with text]: homeless -; PSH -; victim_svcs 12; rent_supp -; ICH -; tbl_prog_activity 3-7; sched_30PBB -; budget_changes 16-17
- FY2025 RM0 rm_dbh_tables_2025j.pdf [Approved FY2025; 20 pp, 20 with text]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; tbl_prog_activity -; sched_30PBB 1-3; budget_changes -
  - activity codes: H04303 ADULT/TRANSITIONAL YOUTH SERVICES ADMINISTRATIVE SERVICES; H04308 HOUSING, RESIDENTIAL SUPPORT AND CONTINUITY OF SERVICES; H04311 ADULT BEHAVIORAL HEALTH SERVICES MH/SUD; H04317 BEHAVIORAL HEALTH REHABILITATION - LOCAL MATCH; H04501 BEHAVIORAL SERVICES - HOWARD ROAD; H04502 CHILD/ADOLESCENT/FAMILY SERVICES ADMINISTRATIVE SERVICES; H04504 CRISIS SERVICES; H04508 SCHOOL BASED BEHAVIORAL HEALTH SERVICES; H04510 SUD PREVENTION AND TREATMENT SERVICES; H04601 BEHAVIORAL HEALTH SERVICES; H04602 BEHAVIORAL HEALTH SERVICES-PHARMACY; H04604 DISASTER BEHAVIORAL HEALTH SERVICES AND SUPPORT SERVICES; H04701 BEHAVIORAL HEALTH GRANT OVERSIGHT SERVICES; H05301 CHILD/YOUTH CRISIS & COMMUNITY TRAUMA RESPONS
- FY2026 CF0 cf_does_chapter_2026o.pdf [Approved FY2026; 11 pp, 11 with text]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; tbl_prog_activity 3-5; sched_30PBB 5; budget_changes 9-10
- FY2026 CF0 cf_does_tables_2026o-1.pdf [image-only, needs OCR; 9 pp, 0 with text]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; tbl_prog_activity -; sched_30PBB -; budget_changes -
- FY2026 CF0 cf_does_tables_2026o-2.pdf [image-only, needs OCR; 12 pp, 0 with text]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; tbl_prog_activity -; sched_30PBB -; budget_changes -
- FY2026 DB0 db_dhcd_chapter_2026o.pdf [Approved FY2026; 9 pp, 9 with text]: homeless -; PSH -; victim_svcs -; rent_supp 5; ICH -; tbl_prog_activity 3-4; sched_30PBB 4; budget_changes 6-8
  - activity codes: EC0019 AFFORDABLE HOUSING; EC0021 HOUSING PRESERVATION; EC0022 HOUSING REGULATION; R02004 Housing Counseling
- FY2026 DB0 db_dhcd_tables_2026o.pdf [image-only, needs OCR; 13 pp, 0 with text]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; tbl_prog_activity -; sched_30PBB -; budget_changes -
- FY2026 FO0 fo_vsjg_chapter_2026o.pdf [Approved FY2026; 8 pp, 8 with text]: homeless -; PSH -; victim_svcs 1,4-7; rent_supp -; ICH -; tbl_prog_activity 3-4; sched_30PBB 4; budget_changes 6-7
  - activity codes: P02303 Victim Services Grants; P04502 Emergency and Traditional Housing; PS0023 VICTIM SERVICES; PS0045 SAFE HOUSING GUN VIOLENCE
- FY2026 FO0 fo_vsjg_tables_2026o.pdf [image-only, needs OCR; 13 pp, 0 with text]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; tbl_prog_activity -; sched_30PBB -; budget_changes -
- FY2026 HG0 hg_dmhhs_chapter_2026o.pdf [Approved FY2026; 5 pp, 5 with text]: homeless 1; PSH -; victim_svcs -; rent_supp -; ICH 1; tbl_prog_activity 3; sched_30PBB 3; budget_changes 4-5
- FY2026 HG0 hg_dmhhs_tables_2026o.pdf [image-only, needs OCR; 7 pp, 0 with text]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; tbl_prog_activity -; sched_30PBB -; budget_changes -
- FY2026 HY0 hy_has_chapter_2026o.pdf [Approved FY2026; 4 pp, 4 with text]: homeless -; PSH -; victim_svcs -; rent_supp 1-3; ICH -; tbl_prog_activity 2; sched_30PBB 2; budget_changes 3-4
  - activity codes: EC0039 HOUSING; R03904 Affordable Housing; R03905 Local Rent Supplement; R03907 Local Rent Supplement - Project & Sponsor Based
- FY2026 HY0 hy_has_tables_2026o.pdf [image-only, needs OCR; 7 pp, 0 with text]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; tbl_prog_activity -; sched_30PBB -; budget_changes -
- FY2026 JA0 ja_dhs_chapter_2026o.pdf [Approved FY2026; 13 pp, 13 with text]: homeless 1,4-9,11-12; PSH 5,7,9,11-12; victim_svcs 13; rent_supp -; ICH -; tbl_prog_activity 3-5; sched_30PBB 5; budget_changes 9-12
  - activity codes: FRSP Family Services; H03002 Homeless Services Continuum - Families; H03003 Homeless Services Continuum - General; H03004 Homeless Services Continuum-Individuals; H03007 Domestic Violence Services; H03009 Homeless Service Continuum - Youth; H03010 Permanent Supportive Housing Families; H03011 Permanent Supportive Housing General; H03012 Permanent Supportive Housing Individuals; H03013 Permanent Supportive Housing Youth; H03014 Prevention Services Families; H03015 Prevention Services Individuals; H03016 Prevention Services Youth; H03017 Rapid Rehousing - Families; H03018 Rapid Rehousing - Individuals; H03019 Rapid Rehousing - Youth; H03022 Transitional Age Youth Shelter; H03023 Transitional Housing Youth; H03024 Youth Services: Ace Program; H03026 Youth Services: Pass Program; H03027 Youth Services: Teen Pregnancy Program; HS0030 FAMILY SERVICES; STFH Family Services
- FY2026 JA0 ja_dhs_tables_2026o.pdf [image-only, needs OCR; 15 pp, 0 with text]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; tbl_prog_activity -; sched_30PBB -; budget_changes -
- FY2026 RM0 rm_dbh_chapter_2026o.pdf [Approved FY2026; 17 pp, 17 with text]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; tbl_prog_activity 3-7; sched_30PBB 7; budget_changes 13-16
  - activity codes: H04303 Adult/Transitional Youth Services Administrative Services; H04308 Housing, Residential Support and Continuity of Services; H04311 Adult Behavioral Health Services MH/SUD; H04317 Behavioral Health Rehabilitation - Local Match; H04501 Behavioral Services - Howard Road; H04502 Child/Adolescent/Family Services Administrative Services; H04504 Crisis Services; H04508 School Based Behavioral Health Services; H04601 Behavioral Health Services; H04602 Behavioral Health Services-Pharmacy; H04604 Disaster Behavioral Health Services and Support Services; H04701 Behavioral Health Grant Oversight Services; HS0043 ADULT/TRANSITIONAL YOUTH SERVICES PROGRAM; HS0044 BEHAVIORAL HEALTH AUTHORITY PROGRAM; HS0045 CHILD/ADOLESCENT/FAMILY SERVICES PROGRAM; HS0053 CRISIS SERVICES; HS0054 ADULT SERVICES ADMINISTRATION PROGRAM
- FY2026 RM0 rm_dbh_tables_2026o-1.pdf [image-only, needs OCR; 9 pp, 0 with text]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; tbl_prog_activity -; sched_30PBB -; budget_changes -
- FY2026 RM0 rm_dbh_tables_2026o-2.pdf [image-only, needs OCR; 11 pp, 0 with text]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; tbl_prog_activity -; sched_30PBB -; budget_changes -
- FY2027 CF0 cf0_does_chapter_2027a_1.pdf [Approved FY2027; 10 pp, 10 with text]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; tbl_prog_activity 3-5; sched_30PBB 5; budget_changes 8-10
- FY2027 CF0 cf0_does_tables_2027a_0.pdf [Approved FY2027; 18 pp, 18 with text]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; tbl_prog_activity -; sched_30PBB 1-3; budget_changes -
- FY2027 DB0 db0_dhcd_chapter_2027a_1.pdf [Approved FY2027; 9 pp, 9 with text]: homeless -; PSH -; victim_svcs -; rent_supp 5-6,8; ICH -; tbl_prog_activity 3-4; sched_30PBB 4; budget_changes 6-8
  - activity codes: EC0019 AFFORDABLE HOUSING; EC0021 HOUSING PRESERVATION; EC0022 HOUSING REGULATION; R02004 HOUSING COUNSELING
- FY2027 DB0 db0_dhcd_tables_2027a_0.pdf [Approved FY2027; 11 pp, 11 with text]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; tbl_prog_activity -; sched_30PBB 1-2; budget_changes -
  - activity codes: EC0019 AFFORDABLE HOUSING; EC0021 HOUSING PRESERVATION; EC0022 HOUSING REGULATION; R02004 HOUSING COUNSELING; R2201 HOUSING PRESERVATION OFFICE (DB0); R2402 HOUSING REGULATION ADMINISTRATION (DB0); R2403 OFFICE OF HOUSING PROGRAMS (DB0)
- FY2027 FO0 fo0_ovsjg_chapter_2027a_1.pdf [Approved FY2027; 7 pp, 7 with text]: homeless -; PSH -; victim_svcs 1-7; rent_supp -; ICH -; tbl_prog_activity 3-4; sched_30PBB 4; budget_changes 5-6
  - activity codes: P02303 VICTIM SERVICES GRANTS; P04502 EMERGENCY AND TRADITIONAL HOUSING; PS0023 VICTIM SERVICES
- FY2027 FO0 fo0_ovsjg_crosswalk_2027a.pdf [stage?; 1 pp, 1 with text]: homeless -; PSH -; victim_svcs 1; rent_supp -; ICH -; tbl_prog_activity -; sched_30PBB -; budget_changes -
- FY2027 FO0 fo0_ovsjg_tables_2027a_0.pdf [Approved FY2027; 9 pp, 9 with text]: homeless -; PSH -; victim_svcs 1-9; rent_supp -; ICH -; tbl_prog_activity -; sched_30PBB 1; budget_changes -
  - activity codes: P02303 VICTIM SERVICES GRANTS; P04502 EMERGENCY AND TRADITIONAL HOUSING; PS0023 VICTIM SERVICES
- FY2027 HG0 hg0_dmhhs_chapter_2027a_1.pdf [Approved FY2027; 5 pp, 5 with text]: homeless 1,4; PSH -; victim_svcs -; rent_supp -; ICH 1,4; tbl_prog_activity 3; sched_30PBB 3; budget_changes 4
- FY2027 HG0 hg0_dmhhs_tables_2027a_0.pdf [Approved FY2027; 7 pp, 7 with text]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; tbl_prog_activity -; sched_30PBB 1; budget_changes -
- FY2027 HY0 hy0_hap_chapter_2027a_1.pdf [Approved FY2027; 4 pp, 4 with text]: homeless -; PSH -; victim_svcs -; rent_supp 1-4; ICH -; tbl_prog_activity 2; sched_30PBB 2; budget_changes 3-4
  - activity codes: EC0039 HOUSING; LRSP HOUSING; R03904 AFFORDABLE HOUSING; R03905 LOCAL RENT SUPPLEMENT; R03907 LOCAL RENT SUPPLMENT - PROJECT & SPONSOR BASED
- FY2027 HY0 hy0_hap_tables_2027a_0.pdf [Approved FY2027; 7 pp, 7 with text]: homeless -; PSH -; victim_svcs -; rent_supp 1; ICH -; tbl_prog_activity -; sched_30PBB 1; budget_changes -
  - activity codes: EC0039 HOUSING; R03904 AFFORDABLE HOUSING; R03905 LOCAL RENT SUPPLEMENT; R03907 LOCAL RENT SUPPLMENT - PROJECT & SPONSOR BASED; R3901 HOUSING DIVISION (HY0)
- FY2027 JA0 ja0_dhs_chapter_2027a_1.pdf [Approved FY2027; 10 pp, 10 with text]: homeless 1,4,6-7,10; PSH 4,6-7; victim_svcs -; rent_supp -; ICH -; tbl_prog_activity 3-5; sched_30PBB 5; budget_changes 8-10
  - activity codes: H03002 HOMELESS SERVICES CONTINUUM - FAMILIES; H03003 HOMELESS SERVICES CONTINUUM - GENERAL; H03004 HOMELESS SERVICES CONTINUUM-INDIVIDUALS; H03007 DOMESTIC VIOLENCE SERVICES; H03009 HOMELESS SERVICE CONTINUUM - YOUTH; H03010 PERMANENT SUPPORTIVE HOUSING FAMILIES; H03011 PERMANENT SUPPORTIVE HOUSING GENERAL; H03012 PERMANENT SUPPORTIVE HOUSING INDIVIDUALS; H03013 PERMANENT SUPPORTIVE HOUSING YOUTH; H03014 PREVENTION SERVICES FAMILIES; H03015 PREVENTION SERVICES INDIVIDUALS; H03016 PREVENTION SERVICES YOUTH; H03017 RAPID REHOUSING - FAMILIES; H03018 RAPID REHOUSING - INDIVIDUALS; H03019 RAPID REHOUSING - YOUTH; H03022 TRANSITIONAL AGE YOUTH SHELTER; H03023 TRANSITIONAL HOUSING YOUTH; H03024 YOUTH SERVICES: ACE PROGRAM; H03025 YOUTH SERVICES: DIVERSION PROGRAM (STEP); H03026 YOUTH SERVICES: PASS PROGRAM; H03027 YOUTH SERVICES: TEEN PREGNANCY PROGRAM; HS0030 FAMILY SERVICES
- FY2027 JA0 ja0_dhs_tables_2027a_0.pdf [Approved FY2027; 14 pp, 14 with text]: homeless 1-2,5-6; PSH 2,6; victim_svcs -; rent_supp -; ICH -; tbl_prog_activity -; sched_30PBB 1-2; budget_changes -
  - activity codes: H03002 HOMELESS SERVICES CONTINUUM - FAMILIES; H03003 HOMELESS SERVICES CONTINUUM - GENERAL; H03004 HOMELESS SERVICES CONTINUUM-INDIVIDUALS; H03007 DOMESTIC VIOLENCE SERVICES; H03009 HOMELESS SERVICE CONTINUUM - YOUTH; H03010 PERMANENT SUPPORTIVE HOUSING FAMILIES; H03011 PERMANENT SUPPORTIVE HOUSING GENERAL; H03012 PERMANENT SUPPORTIVE HOUSING INDIVIDUALS; H03013 PERMANENT SUPPORTIVE HOUSING YOUTH; H03014 PREVENTION SERVICES FAMILIES; H03015 PREVENTION SERVICES INDIVIDUALS; H03016 PREVENTION SERVICES YOUTH; H03017 RAPID REHOUSING - FAMILIES; H03018 RAPID REHOUSING - INDIVIDUALS; H03019 RAPID REHOUSING - YOUTH; H03022 TRANSITIONAL AGE YOUTH SHELTER; H03023 TRANSITIONAL HOUSING YOUTH; H03024 YOUTH SERVICES: ACE PROGRAM; H03025 YOUTH SERVICES: DIVERSION PROGRAM (STEP); H03026 YOUTH SERVICES: PASS PROGRAM; H03027 YOUTH SERVICES: TEEN PREGNANCY PROGRAM; H4002 HOMELESS CONTINUUM DIVISION (JA0); HS0030 FAMILY SERVICES
- FY2027 RM0 rm0_dbh_chapter_2027a_1.pdf [Approved FY2027; 14 pp, 14 with text]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; tbl_prog_activity 3-6; sched_30PBB 6; budget_changes 11-14
  - activity codes: H04308 HOUSING, RESIDENTIAL SUPPORT AND CONTINUITY OF SER; H04311 ADULT BEHAVIORAL HEALTH SERVICES MH/SUD; H04317 BEHAVIORAL HEALTH REHABILITATION - LOCAL MATCH; H04501 BEHAVIORAL SERVICES - HOWARD ROAD; H04502 CHILD/ADOLESCENT/FAMILY SERVICES ADMINISTRATIVE SE; H04504 CRISIS SERVICES; H04508 SCHOOL BASED BEHAVIORAL HEALTH SERVICES; H04601 BEHAVIORAL HEALTH SERVICES; H04602 BEHAVIORAL HEALTH SERVICES-PHARMACY; H04604 DISASTER BEHAVIORAL HEALTH SERVICES AND SUPPORT SE; H04701 BEHAVIORAL HEALTH GRANT OVERSIGHT SERVICES; HS0044 BEHAVIORAL HEALTH AUTHORITY PROGRAM; HS0045 CHILD/ADOLESCENT/FAMILY SERVICES PROGRAM; HS0053 CRISIS SERVICES; HS0054 ADULT SERVICES ADMINISTRATION PROGRAM
- FY2027 RM0 rm0_dbh_tables_2027a_0.pdf [Approved FY2027; 17 pp, 17 with text]: homeless -; PSH -; victim_svcs -; rent_supp -; ICH -; tbl_prog_activity -; sched_30PBB 1-3; budget_changes -
  - activity codes: H04308 HOUSING, RESIDENTIAL SUPPORT AND CONTINUITY OF SER; H04311 ADULT BEHAVIORAL HEALTH SERVICES MH/SUD; H04317 BEHAVIORAL HEALTH REHABILITATION - LOCAL MATCH; H04501 BEHAVIORAL SERVICES - HOWARD ROAD; H04502 CHILD/ADOLESCENT/FAMILY SERVICES ADMINISTRATIVE SE; H04504 CRISIS SERVICES; H04508 SCHOOL BASED BEHAVIORAL HEALTH SERVICES; H04601 BEHAVIORAL HEALTH SERVICES; H04602 BEHAVIORAL HEALTH SERVICES-PHARMACY; H04604 DISASTER BEHAVIORAL HEALTH SERVICES AND SUPPORT SE; H04701 BEHAVIORAL HEALTH GRANT OVERSIGHT SERVICES; H5701 DIVISION OF ADULT SERVICES (RM0); H5801 DIVISION OF CHILD/ADOLESCENT/FAMILY SERVICES (RM0); H8300 DIVISION OF CRISIS SERVICES (RM0); HS0044 BEHAVIORAL HEALTH AUTHORITY PROGRAM; HS0045 CHILD/ADOLESCENT/FAMILY SERVICES PROGRAM; HS0053 CRISIS SERVICES; HS0054 ADULT SERVICES ADMINISTRATION PROGRAM

### 2026-10-10 12:37 — 14_probe_dc_hud: DC Council oversight, OVSJG lists, budget reports, BSA
- OVSJG funding-recipients page lists 10 annual PDFs: ['FY26 OVSJG Grant Recipients', 'FY25 OVSJG Grant Recipients', 'FY24 OVSJG Grant Recipients', 'FY23 OVSJG Grant Recipients', 'FY22 OVSJG Grant Recipients', 'FY21 OVSJG Grant Recipients', 'FY20&nbsp;OVSJG Grant Recipients', 'FY19 OVSJG Grant Recipients', 'FY18 OVSJG Grant Recipients', 'FY17 OVSJG Grant Recipients']
- OVSJG recipients FY2026: 23 pp (23 with text); Calvary pages: 3; peer page counts: House of Ruth 1, My Sister's Place 2, DASH 1, New Endeavors by Women 1, SOME 1, Catholic Charities 2
- OVSJG recipients FY2025: 5 pp (5 with text); Calvary pages: 1; peer page counts: House of Ruth 2, My Sister's Place 1, DASH 1, New Endeavors by Women 1, SOME 1, Catholic Charities 1
  - p1: CALVARY WOMEN'S SERVICES, INC New Foundations Transitional Housing 10/1/2024 - 9/30/2025 $ 519,656.00 Victim Service Local Melanie Kujawa Victim Services
  - p1: CALVARY WOMEN'S SERVICES, INC Reach Up Transitional Housing 10/1/2024 - 9/30/2025 $ 478,622.00 Victim Service Local Melanie Kujawa Victim Services
- OVSJG recipients FY2024: 2 pp (2 with text); Calvary pages: 1; peer page counts: House of Ruth 1, My Sister's Place 1, DASH 1, SOME 1, Catholic Charities 1
  - p1: Calvary Women's Services, Inc. New Foundations Transitional Housing Provide 15 beds of transitional housing and wraparound services, serving at least 35 unaccom
  - p1: Calvary Women's Services, Inc. Reach Up Transitional Housing Provide 15 beds of transitional housing and wraparound services, serving at least 35 unaccompanied 
- POH2024 DHS responses (Pre-Hearing-Responses-DHS-02.28.2024.pdf, 5.6 MB): 134 pp (107 with text); Calvary pages: 97,111; peer page counts: N Street Village 4, Miriam's Kitchen 1, Friendship Place 5, Pathways to Housing DC 2, House of Ruth 3, My Sister's Place 1, DASH 2, Community of Hope 6, New Endeavors by Women 1, Coalition for the Homeless 2, Catholic Charities 11, Christ House 1, The Community Partnership (TCP) 2
  - p97: Calvary Women's Services,Calvary Women's
  - p97: Calvary Women's Services,Calvary Women's
  - p97: Calvary Women's Services,Calvary Women's
  - p97: Calvary Women's Services,Calvary Women's
  - p97: Calvary Women's Services,Calvary Women's
  - p97: Calvary Women's Services,Calvary Women's
  - p111: Calvary Women's Services Calvary Transitional Housing $830,384.15 45 36
  - p111: Calvary Women's Services Sisters Rise (EHV) $593,280.00 25 does not
- POH2024 ICH responses (Pre-Hearing-Responses-ICH-02.27.2024.pdf, 0.5 MB): 33 pp (33 with text); Calvary pages: -; peer page counts: Friendship Place 1, The Community Partnership (TCP) 10
- POH2024 ICH attachments (Pre-Hearing-Attachments-ICH-02.27.2024.pdf, 2.7 MB): 108 pp (104 with text); Calvary pages: -; peer page counts: N Street Village 1, Miriam's Kitchen 1, Friendship Place 5, Pathways to Housing DC 2, My Sister's Place 1, Community of Hope 8, Coalition for the Homeless 2, Catholic Charities 6, The Community Partnership (TCP) 18
- POH2024 OVSJG responses (OVSJG-FY23-24-Oversight-Pre-Hearing-Questions_final.pdf, 1.3 MB): 41 pp (41 with text); Calvary pages: -; peer page counts: House of Ruth 1, DASH 1, SOME 1, Catholic Charities 2, Thrive DC 1
- POH2024 DBH responses (FY-23-Oversight-Pre-Hearing-Responses.-DBH_UPDATED.pdf, 1.3 MB): 118 pp (118 with text); Calvary pages: -; peer page counts: Catholic Charities 5
- POH2025 DHS responses (DHS-Combined-POH-Responses-3.3.2025.pdf, 2.3 MB): 183 pp (182 with text); Calvary pages: 58; peer page counts: N Street Village 6, Miriam's Kitchen 3, Friendship Place 7, Pathways to Housing DC 3, House of Ruth 4, My Sister's Place 3, DASH 5, Community of Hope 7, New Endeavors by Women 1, Coalition for the Homeless 4, SOME 1, Catholic Charities 20, Christ House 1, The Community Partnership (TCP) 11
  - p58: Calvary Women's Services: 1217 Good Hope Road SE 3 0 3
- POH2025 DHS attachments (dhsatt25.pdf, 35.0 MB): 616 pp (518 with text); Calvary pages: -; peer page counts: N Street Village 1, Miriam's Kitchen 1, Friendship Place 3, Pathways to Housing DC 1, My Sister's Place 1, Community of Hope 4, Catholic Charities 3
- POH2025 ICH responses (ICH-Response-_2025-03-04-SUBMISSION.pdf, 1.3 MB): 53 pp (53 with text); Calvary pages: -; peer page counts: Friendship Place 2, Pathways to Housing DC 1, Community of Hope 2, Coalition for the Homeless 1, Catholic Charities 2, Thrive DC 1, The Community Partnership (TCP) 9
- POH2025 ICH attachments (ichatt.pdf, 0.7 MB): 77 pp (76 with text); Calvary pages: -; peer page counts: The Community Partnership (TCP) 10
- POH2025 OVSJG responses (FINAL-OVSJG-FY24-25-Prehearing-questions.pdf, 2.1 MB): 46 pp (46 with text); Calvary pages: -; peer page counts: House of Ruth 2, DASH 1, Catholic Charities 5
- POH2025 DBH attachments (dbhatt.pdf, 13.0 MB): 5238 pp (1804 with text); Calvary pages: -; peer page counts: Miriam's Kitchen 25, Friendship Place 25, Pathways to Housing DC 27, House of Ruth 25, Community of Hope 36, New Endeavors by Women 18, SOME 35, Catholic Charities 25
- POH2026 DHS responses (DHS-Responses-to-Pre-FY25-POH-Questions-FINAL.pdf, 2.2 MB): 241 pp (240 with text); Calvary pages: -; peer page counts: N Street Village 1, House of Ruth 3, My Sister's Place 1, DASH 7, Catholic Charities 1, The Community Partnership (TCP) 6
- POH2026 OVSJG responses (OVSJG-POH-FY25-26-Responses.pdf, 0.9 MB): 39 pp (39 with text); Calvary pages: -
- POH2026 OVSJG attachments (ovsjgatt.pdf, 0.8 MB): 28 pp (23 with text); Calvary pages: 21; peer page counts: House of Ruth 3, New Endeavors by Women 1, Catholic Charities 3
  - p21: CALVARY WOMEN'S SERVICES,
- POH2026 DHCD responses (DHCD-Reponses-to-POH-Pre-Questions-.pdf, 1.4 MB): 132 pp (131 with text); Calvary pages: -
- BO_FY24 JA0 att_I_contracts_grants (JA0_FY24_Attachment-I.pdf, 0.1 MB): 1 pp (1 with text); Calvary pages: 1; peer page counts: Friendship Place 1, House of Ruth 1, DASH 1, Community of Hope 1, Catholic Charities 1, The Community Partnership (TCP) 1
  - p1: Covenant House; Calvary Women's Service
- BO_FY24 FO0 att_I_contracts_grants (FO0_FY24_Attachment-I.pdf, 0.1 MB): 1 pp (1 with text); Calvary pages: -
- BO_FY24 RM0 att_I_contracts_grants (RM0_FY24_Attachment-I.pdf, 0.6 MB): 3 pp (3 with text); Calvary pages: -; peer page counts: N Street Village 1, Pathways to Housing DC 2
- BO_FY25 JA0 att_I_contracts_grants (JA0_FY25_-Attachment-I-Contracts-Grants.pdf, 0.2 MB): 3 pp (3 with text); Calvary pages: 2; peer page counts: Friendship Place 1, House of Ruth 1, DASH 1, Community of Hope 1, Catholic Charities 2, The Community Partnership (TCP) 1
  - p2: Covenant House; Calvary Women's Service;
- BO_FY25 DB0 att_I_contracts_grants (DB0-Attachment-I-Contracts-Grants.pdf, 0.1 MB): 3 pp (3 with text); Calvary pages: -
- BO_FY26 JA0 att_I_contracts_grants (JA0_FY26-Attachment-I.pdf, 0.2 MB): 3 pp (3 with text); Calvary pages: -; peer page counts: Friendship Place 1, House of Ruth 1, DASH 1, Community of Hope 1, Catholic Charities 1, The Community Partnership (TCP) 1
- BO_FY26 JA0 att_III_grants (JA0_FY26-Attachment-III-Grants-Federal-Payments-Lapses.pdf, 0.2 MB): 3 pp (3 with text); Calvary pages: -
- BO_FY26 FO0 att_I_contracts_grants (FO0_FY26_Attachment-I.pdf, 0.1 MB): 3 pp (3 with text); Calvary pages: -
- BO_FY26 RM0 att_I_contracts_grants (RM0_FY26_Attachment-I.pdf, 0.5 MB): 4 pp (4 with text); Calvary pages: -; peer page counts: N Street Village 1, Pathways to Housing DC 2
- BO_FY26 DB0 att_I_contracts_grants (DB0-Attachment-I-Contracts-Grants.pdf, 0.2 MB): 3 pp (3 with text); Calvary pages: -
- BO_FY26 CF0 att_I_contracts_grants (CF0_FY26_-Attachment-I.pdf, 0.2 MB): 10 pp (10 with text); Calvary pages: -
- BO_FY27 JA0 att_I_contracts_grants (JA0_FY27_Attachment-I.pdf, 0.1 MB): 1 pp (1 with text); Calvary pages: -
- BO_FY27 JA0 att_III_grants (JA0_FY27_Attachment-III.pdf, 0.2 MB): 1 pp (1 with text); Calvary pages: -
- BO_FY27 FO0 att_I_contracts_grants (FO0_FY27_Attachment-I.pdf, 0.1 MB): 3 pp (3 with text); Calvary pages: -
- BO_FY27 DB0 att_I_contracts_grants (DB0_FY27_Attachment-I-Contracts-Grants.pdf, 0.1 MB): 1 pp (1 with text); Calvary pages: -
- BO_FY27 CF0 att_I_contracts_grants (CF0_FY27_Attachment-I.pdf, 0.3 MB): 5 pp (5 with text); Calvary pages: -
- BO_FY27 OVSJG budget_prehearing_responses (FY27-OVSJG-Budget-Pre-Hearing-Questions_FINAL.pdf, 0.2 MB): 6 pp (6 with text); Calvary pages: -
- BR_FY25 Housing (DHS, DHCD, DCHA, ICH) committee_budget_report (Circulation-Draft-Budget-Report-Committee-on-Housing-FY25-05.08.2024.pdf, 2.2 MB): 165 pp (165 with text); Calvary pages: -
- BR_FY25 JPS (OVSJG) committee_budget_report (JPS-FY-25-Budget-Report-DRAFT.pdf, 0.9 MB): 96 pp (96 with text); Calvary pages: -
- BR_FY26 Human Services (DHS, ICH) committee_budget_report (Human-Services_FY26-Budget-Recommendations-and-Report-Circulation-Draft_updaetd-622pm.pdf, 1.8 MB): 92 pp (92 with text); Calvary pages: -; peer page counts: The Community Partnership (TCP) 2; homeless pp: 4,7,10,15,32,34-38,43-48,60-62,64,67,69,72,77,79,84,...; PSH pp: 10,36,44,79
- BR_FY26 Housing (DHCD, DCHA) committee_budget_report (Housing_FY26-Budget-Recommendations-and-Report-Updated-circulation-draft.pdf, 1.7 MB): 96 pp (95 with text); Calvary pages: -; homeless pp: 4-5,33; PSH pp: -
- BR_FY26 JPS (OVSJG) committee_budget_report (JPS_FY26-Budget-Recommendations-and-Report-Revised-Draft-624am.pdf, 4.1 MB): 179 pp (179 with text); Calvary pages: -; peer page counts: DASH 1; homeless pp: 106,108; PSH pp: -
- BR_FY26 Health (DBH) committee_budget_report (Health_FY26-Budget-Recommendations-and-Report-Revised-Draft-1.pdf, 6.1 MB): 179 pp (168 with text); Calvary pages: -; peer page counts: Pathways to Housing DC 1; homeless pp: 69,83,86,149; PSH pp: 59
- BR_FY27 All agencies council_operating_changes_chart (Net-Operating-Budget-Adjustments-Chart-2nd-Reading-Circulation_final_6212026.pdf, 0.9 MB): 120 pp (120 with text); Calvary pages: -; peer page counts: Community of Hope 1; homeless pp: 43-45,102; PSH pp: 44
- BR_FY27 All agencies lba_changes_1st_to_2nd_reading (LBA-Budget-Adjustments-Showing-Changes-Between-1st-and-2nd-Reading_final_6212026.pdf, 0.2 MB): 18 pp (18 with text); Calvary pages: -; homeless pp: -; PSH pp: -
- BR_FY27 BSA bsa_committee_print_packet (B26-661-FY27-BSA-COMMITTEE-PACKET.pdf, 4.8 MB): 643 pp (643 with text); Calvary pages: -; peer page counts: Friendship Place 3, DASH 1, SOME 1; homeless pp: 8,22,25,44,125,140,149,278,286,394,429,459,495; PSH pp: 25,497,499
- BR_FY27 Housing (DHCD, DCHA) committee_budget_report (FY27-Committee-on-Housing-Budget-Report-Markup-Draft_revised.pdf, 3.2 MB): 126 pp (126 with text); Calvary pages: 52; peer page counts: House of Ruth 1; homeless pp: 19,36-37,68-69; PSH pp: -
  - p52: o Calvary Women’s
- BR_FY27 Health (DBH) committee_budget_report (DRAFT-FY2027-Committee-on-Health-Budget-Recommendations-Report.pdf, 2.7 MB): 143 pp (143 with text); Calvary pages: -; peer page counts: Community of Hope 1, Catholic Charities 2; homeless pp: 5,11,64,68,92,96,109; PSH pp: -
- BR_FY27 JPS (OVSJG) committee_budget_report (52226-FY2027-JPS-Budget-Report_DRAFT_Recirculated-with-Tables.pdf, 11.7 MB): 124 pp (124 with text); Calvary pages: -; homeless pp: 94; PSH pp: -
- BSA FY2024 (D.C. Law 25-50. Fiscal Year 2024 Budget Support Act of 2023.): 86 subtitles; relevant: DISTRICT OF COLUMBIA HOUSING AUTHORITY PROCUREMENT CLARIFICATION; TAX ABATEMENTS FOR AFFORDABLE HOUSING IN HIGH-NEED AREAS; DOWNTOWN HOUSING; EMERGENCY HOUSING ASSISTANCE PROGRAM FINANCIAL RESPONSIBILITY; EMERGENCY RENTAL ASSISTANCE FUNDS REPORTING AND NOTICE REQUIREMENTS; HOUSING AUTHORITY ACCOUNTABILITY; HOUSING AUTHORITY FINANCIAL REPORTING; PUBLIC HOUSING STABILITY; HOUSING PRODUCTION TRUST FUND; GRANDPARENT AND CAREGIVER SUBSIDY ELIGIBILITY EXPANSION; SCHOOL-BASED BEHAVIORAL HEALTH STUDENT PEER EDUCATOR PILOT; DEPARTMENT OF BEHAVIORAL HEALTH TARGETED OUTREACH GRANTS; DEPARTMENT OF HUMAN SERVICES GRANT
- BSA FY2025 (D.C. Law 25-217. Fiscal Year 2025 Budget Support Act of 2024.): 134 subtitles; relevant: LOCAL RENT SUPPLEMENT PROGRAM ACCOUNTS; EMERGENCY RENTAL ASSISTANCE PROGRAM REPORTS; HOUSING SUBSIDY CONTRACT EXTENSIONS; HOUSING PRESERVATION FUND; FEDERAL CITY SHELTER AND CCNV REDEVELOPMENT PLANNING; DC LOW-INCOME HOUSING TAX CREDIT; HOUSING FOR VICTIMS OF DOMESTIC VIOLENCE FUND CLARIFICATION; GRANDPARENT AND CLOSE RELATIVE CAREGIVER PROGRAM ELIGIBILITY EXPANSION; RAPID RE-HOUSING; CHILDCARE FOR PREGNANT AND BIRTHING PARENTS GRANTS; SCHOOL-BASED BEHAVIORAL HEALTH STUDENT PEER EDUCATOR PILOT; SUBSTANCE ABUSE AND BEHAVIORAL HEALTH SERVICES TARGETED OUTREACH GRANTS; DEPARTMENT OF HUMAN SERVICES GRANT; CORPORATE SHORT-TERM STAY HOUSING IN DOWNTOWN
- BSA FY2026 (D.C. Law 26-55. Fiscal Year 2026 Budget Support Act of 2025.): 111 subtitles; relevant: HUMAN SERVICES GRANT ADMINISTRATION; HOUSING IN DOWNTOWN PROGRAM; HOUSING PRODUCTION TRUST FUND; TANF BENEFITS; RAPID REHOUSING PROGRAMS; SCHOOL-BASED BEHAVIORAL HEALTH STRENGTHENING; SUBSTANCE USE AND BEHAVIORAL HEALTH SERVICES TARGETED OUTREACH PILOT; DEPARTMENT OF HUMAN SERVICES GRANT; NONPROFIT WORKFORCE HOUSING PROPERTIES
- BSA FY2027_emergency (D.C. Act 26-416. Fiscal Year 2027 Budget Support Emergency Act of 2026.): 153 subtitles; relevant: DISTRICT EMPLOYEE PAID PARENTAL, FAMILY, AND MEDICAL LEAVE; RENT PAYMENT REPORTING PROGRAM; WORKFORCE HOUSING OPPORTUNITY TAX ABATEMENT; LRSP VOUCHERS FOR FAMILIES EXITING RAPID REHOUSING; NONPROFIT AFFORDABLE HOUSING DEVELOPMENT TAX RELIEF CLARIFICATION; HOUSING PRODUCTION TRUST FUND; RAPID RE-HOUSING; SCHOOL-BASED BEHAVIORAL HEALTH PROGRAM STABILIZATION AND OVERSIGHT; TANF BENEFITS; DEPARTMENT OF HUMAN SERVICES GRANTS; HUMAN SERVICES PATHWAYS TO INDEPENDENCE; HUMAN SERVICES RESOURCE UTILIZATION; TANF ELIGIBILITY DURING PREGNANCY; HOTEL AND RENTAL CAR TAX

### 2026-10-10 12:37 — 14_probe_dc_hud: HUD CoC / PIT / HIC and MWCOG
- AHAR 2025 Part 1 page data files: ['2007-2025-PIT-Counts-by-CoC.xlsb', '2007-2025-PIT-Counts-by-State.xlsb', '2007-2025-HIC-Counts-by-CoC.xlsx', '2007-2025-HIC-Counts-by-State.xlsx', '2011-2025-PIT-Veteran-Counts-by-CoC.xlsx', '2011-2025-PIT-Veteran-Counts-by-State.xlsx', '2025-HIC-Counts-by-State.csv']
- 2007-2025-PIT-Counts-by-CoC.xlsb: 30 sheets (2025..PIT_Counts_Chart_Template); DC-500 rows in '2025': 1; {'Overall Homeless': np.float64(5138.0), 'Sheltered ES Homeless': np.float64(3275.0), 'Sheltered TH Homeless': np.float64(1065.0), 'Unsheltered Homeless': np.float64(798.0), 'Overall Homeless Individuals': np.float64(3782.0), 'Overall Chronically Homeless Individuals': np.float64(1431.0), 'gender_columns_by_sheet': {'2025': 0, '2024': 0}}
- 2007-2025-HIC-Counts-by-CoC.xlsx: 20 sheets (2025..Revisions); DC-500 rows in '2025': 1; {'Total Year-Round Beds (ES, TH, SH)': np.int64(4965), 'Total Year-Round Beds (TH)': np.int64(1385), 'Total Year-Round Beds (PSH)': np.int64(12696), 'Total Year-Round Beds (RRH)': np.int64(6012), 'gender_columns_by_sheet': {'2025': 0, '2024': 0}}
- AwardComp DC-500 2019: total $22,075,117; Calvary lines: p2: Calvary Women's Service - Sister Circle Renewal project $239,659.00
- AwardComp DC-500 2020: total $23,608,105; Calvary lines: p2: Calvary Women's Service - Sister Circle Renewal project $248,131.00
- AwardComp DC-500 2021: total $25,062,775; Calvary lines: p2: Calvary Women's Service - Sister Circle Renewal project $250,135.00 | p3: Calvary Women's Services - Reach Up Renewal project $1,222,263.00
- AwardComp DC-500 2022: total $27,933,554; Calvary lines: p2: Calvary Women's Services - Sister Circle Renewal project $250,135.00 | p3: Calvary Women's Services - Reach Up Reallocation New project $421,930.00
- AwardComp DC-500 2023: total $29,711,325; Calvary lines: p2: Calvary Women's Services - Sister Circle Renewal project $254,491.00 | p3: Calvary Women's Services - New Foundations 2 New project $469,719.00 | p3: Calvary Women's Services - Reach Up Renewal project $427,330.00
- AwardComp DC-500 2024: total $33,659,924; Calvary lines: p2: Calvary Women's Services - Sister Circle Renewal project $296,926.00 | p3: Calvary Women's Services - Reach Up Expansion project $921,970.00 | p3: Calvary Women's Services - New Foundations 2 Renewal project $542,456.00
- hud.gov FY2024 DC award report: p1: Calvary Women's Services - New Foundations 2 CoC $542,456 | p1: Calvary Women's Services - Reach Up CoC $479,538 | p1: Calvary Women's Services - Reach Up (Expansion) CoC $442,432 | p1: Calvary Women's Services - Sister Circle CoC $296,926
- FY2025 CoC award announcement round 1: 71 pp; DC-500 pages 12; Calvary: p12: Calvary Women's Services - New Foundations 2 CoC $546,247 | p12: Calvary Women's Services - Sister Circle CoC $296,930
- FY2025 CoC award announcement round 2: 127 pp; DC-500 pages 22; Calvary: p22: Calvary Women's Services - Reach Up CoC $923,637
- FY2025 CoC award announcement round 3: 224 pp; DC-500 pages 37; Calvary: none
- FY2024 DC-500 GIW: sheets ['FY 2024 GIW']; Calvary rows 3: The Community Partnership for the Prevention of Homelessness | Calvary Women's Services - Sister Circle | DC0099L3G002306 | 2025 | PH | 0 | 141864 | 91500 | 0 | || The Community Partnership for the Prevention of Homelessness | Calvary Women's Services - Reach Up | DC0125L3G002301 | 2025 | Joint TH & PH-RRH | 86904 | 166212 || The Community Partnership for the Prevention of Homelessness | Calvary Women's Services - New Foundations 2 | DC0130D3G002300 | 2025 | Joint TH & PH-RRH | 0 | 2
- FY2026 DC-500 GIW: sheets ['FY 2026 GIW']; Calvary rows 3: The Community Partnership for the Prevention of Homelessness | Calvary Women's Services - Sister Circle | DC0099L3G002508 | 2027 | PH | 0 | 174924 | 100879 | 0  || The Community Partnership for the Prevention of Homelessness | Calvary Women's Services - Reach Up | DC0125L3G002503 | 2027 | Joint TH & PH-RRH | 86904 | 445284 || The Community Partnership for the Prevention of Homelessness | Calvary Women's Services - New Foundations 2 | DC0130D3G002502 | 2027 | Joint TH & PH-RRH | DV | 
- HIC DC-500 2022: 16 pp; Calvary rows: p4: Calvary Women's Services Reach Up TH (Joint RRH TH 0 0 6 0 n/a n/a 6 n/a 0 0 | p4: Calvary Women's Services Reach UP TH TCP Funded 0 0 10 0 n/a n/a 10 n/a 0 0 | p4: Calvary Women's Services Calvary Women's Transitional 0 0 29 0 n/a n/a 29 n/a 0 0 | p7: Calvary Women's Services Sister Circle 0 0 16 0 n/a n/a 16 16 0 0 | p13: Calvary Women's Services Reach Up RRH (joint RRH T 0 0 7 0 n/a n/a 7 n/a 0 0
- HIC DC-500 2023: 14 pp; Calvary rows: p4: Calvary Women's Services Reach up OVSJG 0 0 12 0 n/a n/a 12 n/a 0 0 | p4: Calvary Women's Services Reach UP TH TCP Funded 0 0 10 0 n/a n/a 10 n/a 0 0 | p4: Calvary Women's Services Reach Up TH (Joint RRH TH 0 0 6 0 n/a n/a 6 n/a 0 0 | p4: Calvary Women's Services Calvary Women's Transitional 0 0 45 0 n/a n/a 45 n/a 0 0 | p7: Calvary Women's Services Sister Circle 0 0 16 0 n/a n/a 16 16 0 0 | p12: Calvary Women's Services Reach Up RRH (joint RRH T 0 0 9 0 n/a n/a 9 n/a 0 0
- HIC DC-500 2024: 15 pp; Calvary rows: p4: Calvary Women's Services (CWS) (Agenc CWS - Reach Up - TH IND - 0 0 6 0 n/a n/a 6 n/a 0 0 | p4: Calvary Women's Services (CWS) (Agenc CWS - Reach Up - TH IND - 0 0 10 0 n/a n/a 10 n/a 0 0 | p4: Calvary Women's Services (CWS) (Agenc CWS - Reach Up OVSJG - T 0 0 15 0 n/a n/a 15 n/a 0 0 | p4: Calvary Women's Services (CWS) (Agenc CWS - Transitional Housing - 0 0 29 0 n/a n/a 29 n/a 0 0 | p7: Calvary Women's Services (CWS) (Agenc CWS - Sisters Rise - PSH IN 0 0 24 0 n/a n/a 24 0 0 0 | p7: Calvary Women's Services (CWS) (Agenc CWS - Sister Circle - PSH IN 0 0 16 0 n/a n/a 16 16 0 0 | p13: Calvary Women's Services (CWS) (Agenc CWS - Reach Up - RRH IND 0 0 7 0 n/a n/a 7 n/a 0 0
- HIC DC-500 2025: 14 pp; Calvary rows: p4: Calvary Women's Services (CWS) (Agenc CWS - Reach Up - TH IND - 0 0 6 0 n/a n/a 6 n/a 0 0 | p4: Calvary Women's Services (CWS) (Agenc CWS - Reach Up - TH IND - 0 0 8 0 n/a n/a 8 n/a 0 0 | p4: Calvary Women's Services (CWS) (Agenc CWS - Transitional Housing - 0 0 45 0 n/a n/a 45 n/a 0 0 | p4: Calvary Women's Services (CWS) (Agenc CWS - Reach Up OVSJG - T 0 0 18 0 n/a n/a 18 n/a 0 0 | p4: Calvary Women's Services (CWS) (Agenc CWS - New Foundations - TH 0 0 17 0 n/a n/a 17 n/a 0 0 | p7: Calvary Women's Services (CWS) (Agenc CWS - Sister Circle - PSH IN 0 0 16 0 n/a n/a 16 16 0 0 | p13: Calvary Women's Services (CWS) (Agenc CWS - Reach Up - RRH IND 0 0 14 0 n/a n/a 14 n/a 0 0
- PopSub DC-500 2024: 3 pp
- PopSub DC-500 2025: 3 pp
- MWCOG report page lists 20 annual reports
- MWCOG 2026 PIT report (5.1 MB): 131 pp (131 with text); Calvary pages: -; peer page counts: Pathways to Housing DC 1, Coalition for the Homeless 1, SOME 1, The Community Partnership (TCP) 7; DC pages: 9-10,13,17-18,22-26,28,32-39,42,44,46,48-51,53-57,59-63,67,69,75,...; ward pp: -
- MWCOG 2025 PIT report (11.2 MB): 194 pp (192 with text); Calvary pages: -; peer page counts: Friendship Place 1, Pathways to Housing DC 6, Coalition for the Homeless 1, SOME 2, The Community Partnership (TCP) 9; DC pages: 2-3,7-9,11-12,17-18,20-23,26,28-29,31-33,45,47-48,50-53,59-60,65,76,100,...; ward pp: -
- MWCOG 2024 PIT report (8.3 MB): 195 pp (194 with text); Calvary pages: -; peer page counts: Friendship Place 1, Pathways to Housing DC 5, Coalition for the Homeless 2, SOME 2, The Community Partnership (TCP) 9; DC pages: 2-3,8,12,16-17,19-20,22-23,29-33,46,48-49,51-54,56,60,66,78,93,...; ward pp: -
- MWCOG 2023 PIT report (7.6 MB): 182 pp (180 with text); Calvary pages: -; peer page counts: Friendship Place 1, Pathways to Housing DC 5, Coalition for the Homeless 4, SOME 1, The Community Partnership (TCP) 12; DC pages: 2-3,8-9,12,15-17,19-20,22-23,25-28,40-42,44-46,48,51-53,58,71,93,98,...; ward pp: -

### 2026-10-10 12:37 — 14_probe_dc_hud: run summary
- bytes saved this run: raw/dc_council 117.9 MB, raw/dc_gov 87.3 MB, raw/hud 54.6 MB; total 259.8 MB
- failures (0): none

### 2026-10-10 12:37 — 10_probe_filings: bmf
- documentation: raw/irs_bmf/20261010T123741_eo-info.pdf
- eo_dc.csv: 14,155 rows, 2.6 MB, subsection 03 10,917, FOUNDATION 02/03/04 629, PF_FILING_REQ_CD=1 626 (reused raw/irs_bmf/20261010T121504_eo_dc.csv)
- eo_md.csv: 43,659 rows, 7.7 MB, subsection 03 37,165, FOUNDATION 02/03/04 2,397, PF_FILING_REQ_CD=1 2,397 (reused raw/irs_bmf/20261010T121505_eo_md.csv)
- eo_va.csv: 54,196 rows, 9.5 MB, subsection 03 45,151, FOUNDATION 02/03/04 2,784, PF_FILING_REQ_CD=1 2,795 (reused raw/irs_bmf/20261010T121505_eo_va.csv)
- eo1.csv: 279,041 rows, 48.8 MB, subsection 03 234,977, FOUNDATION 02/03/04 24,652, PF_FILING_REQ_CD=1 25,073 (reused raw/irs_bmf/20261010T121506_eo1.csv)
- eo2.csv: 721,547 rows, 126.1 MB, subsection 03 578,354, FOUNDATION 02/03/04 43,174, PF_FILING_REQ_CD=1 45,852 (reused raw/irs_bmf/20261010T121508_eo2.csv)
- eo3.csv: 959,426 rows, 165.3 MB, subsection 03 824,268, FOUNDATION 02/03/04 62,403, PF_FILING_REQ_CD=1 64,346 (reused raw/irs_bmf/20261010T121605_eo3.csv)
- eo4.csv: 4,944 rows, 0.9 MB, subsection 03 4,506, FOUNDATION 02/03/04 285, PF_FILING_REQ_CD=1 287 (reused raw/irs_bmf/20261010T121612_eo4.csv)
- columns (28): EIN, NAME, ICO, STREET, CITY, STATE, ZIP, GROUP, SUBSECTION, AFFILIATION, CLASSIFICATION, RULING, DEDUCTIBILITY, FOUNDATION, ACTIVITY, ORGANIZATION, STATUS, TAX_PERIOD, ASSET_CD, INCOME_CD, FILING_REQ_CD, PF_FILING_REQ_CD, ACCT_PD, ASSET_AMT, INCOME_AMT, REVENUE_AMT, NTEE_CD, SORT_NAME
- Calvary row: {"NAME": "CALVARY WOMENS SERVICES INC", "SUBSECTION": "03", "FOUNDATION": "15", "NTEE_CD": "L41Z", "RULING": "198406", "TAX_PERIOD": "202509", "ASSET_AMT": "10059516", "INCOME_AMT": "5227366", "REVENUE_AMT": "4967995", "FILING_REQ_CD": "01", "PF_FILING_REQ_CD": "0", "ACCT_PD": "09"}
- DC+MD+VA: 112,010 rows; FOUNDATION 02/03/04 = 5,810 EINs; PF_FILING_REQ_CD=1 = 5,818; both = 5,773; either = 5,855

### 2026-10-10 12:38 — 12_probe_federal: fac
- Calvary reports: 2 (audit years [2022, 2023]); additional_eins hits 0
  - 2022-09-CENSUS-0000258136 FYE 2022-09-30 total $4,067,718; awards [('21.027', 3583885, 'N'), ('14.235', 415830, 'N'), ('97.024', 48889, 'N'), ('10.561', 19114, 'N')]; passthrough {'AWARD-00001': 'DISTRICT OF COLUMBIA OFFICE OF VICTIM SERVICES AND JUSTICE GRANTS', 'AWARD-00002': 'THE COMMUNITY PARTNERSHIP', 'AWARD-00003': 'FEDERAL EMERGENCY MANAGEMENT AGENCY', 'AWARD-00004': 'DISTRICT OF COLUMBIA DEPARTMENT OF HUMAN SERVICES'}; children {'federal_awards': 4, 'passthrough': 4, 'findings': 0, 'findings_text': 0, 'notes_to_sefa': 1, 'secondary_auditors': 0, 'additional_eins': 0, 'additional_ueis': 0, 'corrective_action_plans': 0}
  - 2023-09-GSAFAC-0000037691 FYE 2023-09-30 total $4,064,718; awards [('21.027', 3583885, 'N'), ('14.235', 415830, 'N'), ('97.024', 45889, 'N'), ('10.561', 19114, 'N')]; passthrough {'AWARD-00001': 'District of Columbia Office of Victim Services and Justice Grants', 'AWARD-00002': 'The Community Partnership', 'AWARD-00003': 'Federal Emergency Management Agency', 'AWARD-00004': 'District of Columbia Department of Human Services'}; children {'federal_awards': 4, 'passthrough': 4, 'findings': 0, 'findings_text': 0, 'notes_to_sefa': 3, 'secondary_auditors': 0, 'additional_eins': 0, 'additional_ueis': 0, 'corrective_action_plans': 0}
- DC auditees by audit_year: {"2016": {"audits": 391, "nonprofit": 371, "expended": 13206882145}, "2017": {"audits": 384, "nonprofit": 367, "expended": 13979710795}, "2018": {"audits": 402, "nonprofit": 383, "expended": 13021048914}, "2019": {"audits": 398, "nonprofit": 381, "expended": 14451399643}, "2020": {"audits": 387, "nonprofit": 368, "expended": 17308664616}, "2021": {"audits": 409, "nonprofit": 394, "expended": 20391585672}, "2022": {"audits": 466, "nonprofit": 437, "expended": 20085076799}, "2023": {"audits": 477, "nonprofit": 457, "expended": 20989240408}, "2024": {"audits": 467, "nonprofit": 451, "expended": 20678342419}, "2025": {"audits": 359, "nonprofit": 342, "expended": 25753007771}, "2026": {"audits": 1, "nonprofit": 1, "expended": 42466823}}
- DC 2023 SEFA: {"federal_awards_rows": 9602, "indirect_rows": 3614, "target_cfda_rows": 486, "target_cfda_indirect_rows": 256, "target_cfda_auditees": 111, "passthrough_rows": 3614, "top_passthrough_names": [["DISTRICT OF COLUMBIA OFFICE OF THE STATE SUPERINTENDENT OF EDUCATION", 341], ["MARYLAND STATE DEPARTMENT OF EDUCATION", 90], ["CONSORTIUM FOR ELECTIONS AND POLITICAL PROCESS STRENGTHENING", 62], ["DC OFFICE OF THE STATE SUPERINTENDENT OF EDUCATION", 60], ["SPACE TELESCOPE SCIENCE INSTITUTE", 57], ["D.C OFFICE OF STATE SUPERINTENDENT OF EDUCATION", 53], ["GEORGE WASHINGTON UNIVERSITY", 52], ["CONSORTIUM FOR ELECTIONS AND POLICAL STRENGTHENING", 50], ["NATIONAL ENDOWMENT FOR DEMOCRACY", 46], ["DISTRICT OF COLUMBIA DEPARTMENT OF HEALTH", 42], ["DC DEPARTMENT OF HEALTH", 42], ["FREEDOM HOUSE", 39]]}
- OVSJG pass-through rows: {"rows": 75, "by_year": {"2016": 4, "2017": 3, "2018": 2, "2019": 2, "2020": 4, "2021": 7, "2022": 13, "2023": 18, "2024": 13, "2025": 9}, "reports": 43}

### 2026-10-10 12:38 — 02_extract_inputs
- text dumps: 25 files in raw/inputs_extracted/text
- raw/inputs_extracted/audit_financials.csv: 1089 rows
- raw/inputs_extracted/audit_tieout_checks.csv: 260 rows
- raw/inputs_extracted/sefa_federal_awards.csv: 4 rows
- raw/inputs_extracted/form990_pdf_financials.csv: 362 rows
- raw/inputs_extracted/form990_pdf_people.csv: 113 rows
- raw/inputs_extracted/form990_pdf_schedule_i.csv: 2 rows
- raw/inputs_extracted/funder_mentions.csv: 197 rows
- raw/inputs_extracted/individual_donor_band_counts.csv: 4 rows
- raw/inputs_extracted/board_lists.csv: 82 rows
- raw/inputs_extracted/annual_report_metrics.csv: 178 rows
- tie-out checks: 260/260 tie
- SEFA: FY15-Audited-Financial-Statements.pdf: SEFA none
- SEFA: 2016-Audited-Financial-Statements.pdf: SEFA none
- SEFA: 2017-Audited-Financial-Statements-Calvary-Women_s-Services.pdf: SEFA none
- SEFA: CWS-FY18-Audit-.pdf: SEFA none
- SEFA: 2019-Audited-Financial-Statements-CWS.pdf: SEFA none
- SEFA: 2020-Audited-Financial-Statements-CWS.pdf: SEFA none
- SEFA: 2021-Audited-Financial-Statements-CWS.pdf: SEFA none
- SEFA: Calvary-Womens-Services-Inc.-9.30.23-FS.pdf: SEFA 4 programs sum 937,999 vs printed total 937,999
- funder names verified in layout text: 168/168
- note: 2015-Form-990-Calvary-Women_s-Services.pdf: Part I not in text layer (page 1 scanned)
- note: 2016-Form-990-Calvary-Women_s-Services.pdf: Part I not in text layer (page 1 scanned)
- note: 2019-990-Form-990-CWS.pdf: Part I not in text layer (page 1 scanned)

### 2026-10-10 12:38 — 12_probe_federal: grantsgov
- posted+forecasted total 1467 (returned 1467 in one call); target-CFDA hits 3; status facets {'posted': 867, 'closed': 8714, 'archived': 73376, 'forecasted': 600}
- row cap: {10000: {'http': 200, 'returned': 10000}, 30000: {'http': None, 'returned': 0}}; pagination: {'startRecord': 1462, 'returned': 5}; filter key test (16.575 all statuses): {'aln': 83557, 'cfda': 9}
- keywords (posted+forecasted): {"homelessness": {"hits": 13, "posted": 11, "forecasted": 2, "elig_501c3": 10}, "housing": {"hits": 176, "posted": 163, "forecasted": 13, "elig_501c3": 134}, "domestic violence": {"hits": 387, "posted": 358, "forecasted": 29, "elig_501c3": 189, "phrase_hits": 9}, "victim services": {"hits": 670, "posted": 457, "forecasted": 213, "elig_501c3": 361, "phrase_hits": 4}, "women": {"hits": 162, "posted": 130, "forecasted": 32, "elig_501c3": 54}, "substance use": {"hits": 677, "posted": 489, "forecasted": 188, "elig_501c3": 368, "phrase_hits": 60}, "workforce": {"hits": 217, "posted": 187, "forecasted": 30, "elig_501c3": 96}, "reentry": {"hits": 9, "posted": 9, "forecasted": 0, "elig_501c3": 3}, "veterans": {"hits": 82, "posted": 73, "forecasted": 9, "elig_501c3": 13}, "aging": {"hits": 94, "posted": 63, "forecasted": 31, "elig_501c3": 75}}
- fetchOpportunity: {"posted": {"id": "363961", "number": "O-OJJDP-2026-172751", "docType": "synopsis", "top_keys": ["agencyDetails", "assistCompatible", "assistURL", "cfdas", "closedOpportunityPkgs", "docType", "draftMode", "errorMessages", "flag2006", "forecastHistCount", "forecastModifiedFields", "id", "listed", "opportunityCategory", "opportunityHistoryDetails", "opportunityNumber", "opportunityPkgs", "opportunityTitle", "originalDueDate", "ost", "owningAgencyCode", "publisherUid", "relatedOpps", "revision", "synAttChangeComments", "synPostDateInPast", "synopsis", "synopsisAttachmentFolders", "synopsisDocumentURLs", "synopsisHistCount", "synopsisModifiedFields", "topAgencyDetails"], "detail_block": "synopsis", "awardCeiling": "750000", "awardFloor": "0", "estimatedFunding": "12440720", "responseDate": "Nov 02, 2026 12:00:00 AM EST", "estimatedSynopsisCloseDate": null, "applicantTypes": ["12", "13", "02", "25", "01", "07", "00"], "cfdas": ["16.812"]}, "forecasted": {"id": "355824", "number": "MP-CPI-25-001", "docType": "forecast", "top_keys": ["agencyDetails", "assistCompatible", "assistURL", "cfdas", "closedOpportunityPkgs", "docType", "draftMode", "errorMessages", "flag2006", "forecast", "forecastHistCount", "forecastModifiedFields", "id", "listed", "modifiedComments", "opportunityCategory", "opportunityHistoryDetails", "opportunityNumber", "opportunityPkgs", "opportunityTitle", "ost", "owningAgencyCode", "publisherUid", "relatedOpps", "revision", "synAttChangeComments", "synPostDateInPast", "synopsisAttachmentFolders", "synopsisDocumentURLs", "synopsisHistCount", "synopsisModifiedFields", "topAgencyDetails"], "detail_block": "forecast", "awardCeiling": "600000", "awardFloor": "450000", "estimatedFunding": "5000000", "responseDate": null, "estimatedSynopsisCloseDate": null, "applicantTypes": ["11", "01", "04", "06", "02", "08", "13", "07", "05", "00", "12"], "cfdas": ["93.137"]}}

### 2026-10-10 12:39 — 14_probe_dc_hud: probe-only sources
- ocp_transparency_portal: HTTP 200, 5,395 B (https://contracts.ocp.dc.gov/contracts/search)
- moca_community_grant_program: HTTP 200, 114,003 B (https://communityaffairs.dc.gov/content/community-grant-program)
- tcp_homelessness_in_dc: HTTP 200, 200,828 B (https://community-partnership.org/homelessness-in-dc/)
- ich_pit_release: HTTP 200, 57,584 B (https://ich.dc.gov/release/mayor-bowser-releases-annual-point-time-count-results)
- dcpit_hub_search: HTTP 200, 10,483 B (https://www.dcpit.org/api/search/v1/collections/all/items?limit=50)
- DC Council LIMS API v2 (https://lims.dccouncil.gov/api/v2/PublicData/LegislationDetails/B26-0661): HTTP 401 'Valid Access Token required.' (token required; not used)

### 2026-10-10 12:39 — 14_probe_dc_hud: run summary
- bytes saved this run: raw/dc_gov 0.1 MB, raw/hud 0.3 MB; total 0.4 MB
- failures (0): none

### 2026-10-10 12:40 — 02_extract_inputs
- text dumps: 25 files in raw/inputs_extracted/text
- raw/inputs_extracted/audit_financials.csv: 1089 rows
- raw/inputs_extracted/audit_tieout_checks.csv: 260 rows
- raw/inputs_extracted/sefa_federal_awards.csv: 4 rows
- raw/inputs_extracted/form990_pdf_financials.csv: 362 rows
- raw/inputs_extracted/form990_pdf_people.csv: 113 rows
- raw/inputs_extracted/form990_pdf_schedule_i.csv: 2 rows
- raw/inputs_extracted/funder_mentions.csv: 202 rows
- raw/inputs_extracted/individual_donor_band_counts.csv: 4 rows
- raw/inputs_extracted/board_lists.csv: 82 rows
- raw/inputs_extracted/annual_report_metrics.csv: 178 rows
- tie-out checks: 260/260 tie
- SEFA: FY15-Audited-Financial-Statements.pdf: SEFA none
- SEFA: 2016-Audited-Financial-Statements.pdf: SEFA none
- SEFA: 2017-Audited-Financial-Statements-Calvary-Women_s-Services.pdf: SEFA none
- SEFA: CWS-FY18-Audit-.pdf: SEFA none
- SEFA: 2019-Audited-Financial-Statements-CWS.pdf: SEFA none
- SEFA: 2020-Audited-Financial-Statements-CWS.pdf: SEFA none
- SEFA: 2021-Audited-Financial-Statements-CWS.pdf: SEFA none
- SEFA: Calvary-Womens-Services-Inc.-9.30.23-FS.pdf: SEFA 4 programs sum 937,999 vs printed total 937,999
- funder names verified in layout text: 173/173
- note: 2015-Form-990-Calvary-Women_s-Services.pdf: Part I not in text layer (page 1 scanned)
- note: 2016-Form-990-Calvary-Women_s-Services.pdf: Part I not in text layer (page 1 scanned)
- note: 2019-990-Form-990-CWS.pdf: Part I not in text layer (page 1 scanned)

### 2026-10-10 12:40 — 10_probe_filings: remotezip
- 52 ZIP names for 2021-2026 (downloads page + index batch ids); 52 reachable (HTTP 200, Accept-Ranges); not reachable: none
  - 2021: 1 ZIPs, 3.72 GB, 589,904 members, central directories 55.5 MB
  - 2022: 2 ZIPs, 4.01 GB, 656,503 members, central directories 62.6 MB
  - 2023: 12 ZIPs, 4.29 GB, 705,154 members, central directories 65.6 MB
  - 2024: 12 ZIPs, 4.39 GB, 728,719 members, central directories 67.8 MB
  - 2025: 16 ZIPs, 4.46 GB, 748,906 members, central directories 56.2 MB
  - 2026: 9 ZIPs, 2.56 GB, 436,239 members, central directories 32.7 MB
  - 2021_TEOS_XML_01A: 3,715.5 MB, 589,904 members, CD 55.5 MB, Thu, 06 Mar 2025 20:08:25 GMT, page
  - 2022_TEOS_XML_01A: 2,603.7 MB, 433,529 members, CD 41.2 MB, Thu, 06 Mar 2025 20:08:56 GMT, page
  - 2022_TEOS_XML_02A: 1,408.2 MB, 222,974 members, CD 21.4 MB, Thu, 06 Mar 2025 20:06:10 GMT, probe_only
  - 2023_TEOS_XML_01A: 123.1 MB, 21,513 members, CD 2.0 MB, Thu, 06 Mar 2025 17:04:40 GMT, page
  - 2023_TEOS_XML_02A: 234.6 MB, 40,304 members, CD 3.7 MB, Thu, 06 Mar 2025 17:07:26 GMT, page
  - 2023_TEOS_XML_03A: 197.2 MB, 36,224 members, CD 3.4 MB, Thu, 06 Mar 2025 17:06:19 GMT, page
  - 2023_TEOS_XML_04A: 244.5 MB, 42,995 members, CD 4.0 MB, Thu, 06 Mar 2025 17:07:59 GMT, page
  - 2023_TEOS_XML_05A: 990.5 MB, 156,228 members, CD 14.5 MB, Thu, 06 Mar 2025 17:27:59 GMT, page
  - 2023_TEOS_XML_06A: 163.7 MB, 29,240 members, CD 2.7 MB, Thu, 06 Mar 2025 17:05:35 GMT, page
  - 2023_TEOS_XML_07A: 219.9 MB, 38,027 members, CD 3.5 MB, Thu, 06 Mar 2025 17:07:06 GMT, page
  - 2023_TEOS_XML_08A: 266.2 MB, 42,301 members, CD 3.9 MB, Thu, 06 Mar 2025 17:08:23 GMT, page
  - 2023_TEOS_XML_09A: 200.4 MB, 35,070 members, CD 3.3 MB, Thu, 06 Mar 2025 17:06:29 GMT, page
  - 2023_TEOS_XML_10A: 332.5 MB, 56,858 members, CD 5.3 MB, Thu, 06 Mar 2025 17:10:21 GMT, page
  - 2023_TEOS_XML_11A: 1,200.3 MB, 186,387 members, CD 17.3 MB, Thu, 06 Mar 2025 17:32:53 GMT, page
  - 2023_TEOS_XML_12A: 120.7 MB, 20,007 members, CD 1.9 MB, Thu, 06 Mar 2025 17:04:34 GMT, page
  - 2024_TEOS_XML_01A: 104.8 MB, 17,246 members, CD 1.6 MB, Thu, 06 Mar 2025 14:04:31 GMT, page
  - 2024_TEOS_XML_02A: 243.7 MB, 40,284 members, CD 3.7 MB, Thu, 06 Mar 2025 14:04:23 GMT, page
  - 2024_TEOS_XML_03A: 209.3 MB, 38,418 members, CD 3.6 MB, Thu, 06 Mar 2025 14:04:55 GMT, page
  - 2024_TEOS_XML_04A: 350.3 MB, 59,487 members, CD 5.5 MB, Thu, 06 Mar 2025 14:05:02 GMT, page
  - 2024_TEOS_XML_05A: 977.5 MB, 156,237 members, CD 14.5 MB, Thu, 06 Mar 2025 14:05:40 GMT, page
  - 2024_TEOS_XML_06A: 163.9 MB, 29,408 members, CD 2.7 MB, Thu, 06 Mar 2025 14:04:01 GMT, page
  - 2024_TEOS_XML_07A: 288.3 MB, 50,144 members, CD 4.7 MB, Thu, 06 Mar 2025 14:04:23 GMT, page
  - 2024_TEOS_XML_08A: 260.6 MB, 41,687 members, CD 3.9 MB, Thu, 06 Mar 2025 14:04:56 GMT, page
  - 2024_TEOS_XML_09A: 247.0 MB, 44,108 members, CD 4.1 MB, Thu, 06 Mar 2025 14:04:54 GMT, page
  - 2024_TEOS_XML_10A: 251.6 MB, 43,392 members, CD 4.0 MB, Thu, 06 Mar 2025 14:04:55 GMT, page
  - 2024_TEOS_XML_11A: 1,165.6 MB, 186,632 members, CD 17.4 MB, Thu, 06 Mar 2025 14:05:48 GMT, page
  - 2024_TEOS_XML_12A: 128.3 MB, 21,676 members, CD 2.0 MB, Thu, 06 Mar 2025 14:04:05 GMT, page
  - 2025_TEOS_XML_01A: 103.7 MB, 17,044 members, CD 1.3 MB, Wed, 05 Mar 2025 15:12:42 GMT, page
  - 2025_TEOS_XML_02A: 239.9 MB, 41,855 members, CD 3.1 MB, Wed, 19 Mar 2025 13:01:47 GMT, page
  - 2025_TEOS_XML_03A: 222.6 MB, 41,570 members, CD 3.1 MB, Wed, 16 Apr 2025 13:01:48 GMT, page
  - 2025_TEOS_XML_04A: 338.2 MB, 57,595 members, CD 4.3 MB, Wed, 21 May 2025 13:09:56 GMT, page
  - 2025_TEOS_XML_05A: 495.9 MB, 81,770 members, CD 6.1 MB, Wed, 25 Jun 2025 13:13:15 GMT, page
  - 2025_TEOS_XML_05B: 501.0 MB, 81,770 members, CD 6.1 MB, Wed, 25 Jun 2025 13:13:33 GMT, page
  - 2025_TEOS_XML_06A: 246.8 MB, 44,824 members, CD 3.4 MB, Wed, 20 Aug 2025 13:11:59 GMT, page
  - 2025_TEOS_XML_07A: 143.5 MB, 24,854 members, CD 1.9 MB, Wed, 20 Aug 2025 13:08:44 GMT, page
  - 2025_TEOS_XML_08A: 262.7 MB, 42,291 members, CD 3.2 MB, Wed, 17 Sep 2025 13:18:06 GMT, page
  - 2025_TEOS_XML_09A: 256.3 MB, 45,643 members, CD 3.4 MB, Wed, 19 Nov 2025 20:41:59 GMT, page
  - 2025_TEOS_XML_10A: 56.5 MB, 9,836 members, CD 0.7 MB, Wed, 19 Nov 2025 14:08:07 GMT, page
  - 2025_TEOS_XML_11A: 340.1 MB, 55,488 members, CD 4.2 MB, Wed, 17 Dec 2025 14:31:07 GMT, page
  - 2025_TEOS_XML_11B: 494.5 MB, 80,283 members, CD 6.0 MB, Wed, 17 Dec 2025 14:43:04 GMT, page
  - 2025_TEOS_XML_11C: 277.9 MB, 44,896 members, CD 3.4 MB, Wed, 17 Dec 2025 14:25:37 GMT, page
  - 2025_TEOS_XML_11D: 332.8 MB, 53,800 members, CD 4.0 MB, Wed, 17 Dec 2025 17:10:02 GMT, page
  - 2025_TEOS_XML_12A: 151.8 MB, 25,387 members, CD 1.9 MB, Wed, 21 Jan 2026 14:14:30 GMT, page
  - 2026_TEOS_XML_01A: 71.5 MB, 12,245 members, CD 0.9 MB, Thu, 19 Feb 2026 18:32:24 GMT, page
  - 2026_TEOS_XML_02A: 222.1 MB, 38,719 members, CD 2.9 MB, Wed, 18 Mar 2026 13:02:56 GMT, page
  - 2026_TEOS_XML_03A: 259.3 MB, 48,471 members, CD 3.6 MB, Wed, 15 Apr 2026 13:03:42 GMT, page
  - 2026_TEOS_XML_04A: 261.9 MB, 47,627 members, CD 3.6 MB, Wed, 20 May 2026 13:02:32 GMT, page
  - 2026_TEOS_XML_05A: 521.2 MB, 84,172 members, CD 6.3 MB, Wed, 17 Jun 2026 13:13:47 GMT, page
  - 2026_TEOS_XML_05B: 513.4 MB, 84,172 members, CD 6.3 MB, Wed, 17 Jun 2026 13:13:52 GMT, page
  - 2026_TEOS_XML_06A: 210.8 MB, 38,244 members, CD 2.9 MB, Wed, 15 Jul 2026 16:01:18 GMT, page
  - 2026_TEOS_XML_07A: 189.2 MB, 32,240 members, CD 2.4 MB, Wed, 19 Aug 2026 13:00:50 GMT, page
  - 2026_TEOS_XML_08A: 314.7 MB, 50,349 members, CD 3.8 MB, Wed, 16 Sep 2026 13:02:45 GMT, index_only
  - release 2021: index rows 589,904 vs ZIP members 589,904 (diff +0)
  - release 2022: index rows 656,503 vs ZIP members 656,503 (diff +0)
  - release 2023: index rows 705,156 vs ZIP members 705,154 (diff -2)
  - release 2024: index rows 728,719 vs ZIP members 728,719 (diff +0)
  - release 2025: index rows 748,906 vs ZIP members 748,906 (diff +0)
  - release 2026: index rows 436,239 vs ZIP members 436,239 (diff +0)
  - 2025_TEOS_XML_05A vs 2025_TEOS_XML_05B: 81,770 / 81,770 object ids, overlap 0; index rows labelled 2025_TEOS_XML_05A: 163,540, found in 2025_TEOS_XML_05A 81,770, in 2025_TEOS_XML_05B 81,770 (read 12.4 MB of central directory)
  - 2026_TEOS_XML_05A vs 2026_TEOS_XML_05B: 84,172 / 84,172 object ids, overlap 0; index rows labelled 2026_TEOS_XML_05A: 168,344, found in 2026_TEOS_XML_05A 84,172, in 2026_TEOS_XML_05B 84,172 (read 12.8 MB of central directory)
- remotezip 2026_TEOS_XML_06A (210.8 MB, 38,244 members, names like 202601429339300000_public.xml): central directory 2 requests / 2.9 MB; member 202631539349300848_public.xml 54,115 B (10,872 B compressed); total 3 requests / 2.9 MB = 1.40% of the ZIP; 0.4s -> raw/xml/irs/20261010T122754_521307706_TY2024_2026_TEOS_XML_06A_202631539349300848_public.xml
- 2026_TEOS_XML_06A: mean member 28.7 KB uncompressed, compression ratio 5.3x
- GT S3 copy of 202631539349300848 byte-identical to the IRS ZIP member: True
- Calvary TY2021 202322239349302102 (release 2023, no batch id; DLN day -> month 08): found in None after reading 12 central directories (66.4 MB)

### 2026-10-10 12:41 — 02_extract_inputs
- text dumps: 25 files in raw/inputs_extracted/text
- raw/inputs_extracted/audit_financials.csv: 1089 rows
- raw/inputs_extracted/audit_tieout_checks.csv: 260 rows
- raw/inputs_extracted/sefa_federal_awards.csv: 4 rows
- raw/inputs_extracted/form990_pdf_financials.csv: 362 rows
- raw/inputs_extracted/form990_pdf_people.csv: 113 rows
- raw/inputs_extracted/form990_pdf_schedule_i.csv: 2 rows
- raw/inputs_extracted/funder_mentions.csv: 200 rows
- raw/inputs_extracted/individual_donor_band_counts.csv: 4 rows
- raw/inputs_extracted/board_lists.csv: 82 rows
- raw/inputs_extracted/annual_report_metrics.csv: 178 rows
- tie-out checks: 260/260 tie
- SEFA: FY15-Audited-Financial-Statements.pdf: SEFA none
- SEFA: 2016-Audited-Financial-Statements.pdf: SEFA none
- SEFA: 2017-Audited-Financial-Statements-Calvary-Women_s-Services.pdf: SEFA none
- SEFA: CWS-FY18-Audit-.pdf: SEFA none
- SEFA: 2019-Audited-Financial-Statements-CWS.pdf: SEFA none
- SEFA: 2020-Audited-Financial-Statements-CWS.pdf: SEFA none
- SEFA: 2021-Audited-Financial-Statements-CWS.pdf: SEFA none
- SEFA: Calvary-Womens-Services-Inc.-9.30.23-FS.pdf: SEFA 4 programs sum 937,999 vs printed total 937,999
- funder names verified in layout text: 171/171
- note: 2015-Form-990-Calvary-Women_s-Services.pdf: Part I not in text layer (page 1 scanned)
- note: 2016-Form-990-Calvary-Women_s-Services.pdf: Part I not in text layer (page 1 scanned)
- note: 2019-990-Form-990-CWS.pdf: Part I not in text layer (page 1 scanned)

### 2026-10-10 12:41 — 10_probe_filings: volume
- BMF sets: (a) DMV PF filers (FOUNDATION 02/03/04 or PF_FILING_REQ_CD=1) 5,855 EINs; (b) DC 501(c)(3) public charities in NTEE L/P/F/I/J/W 1,750 EINs
- (a: DMV 990-PF filers) 25,367 returns from 5,249 EINs; by type {'990PF': 25367}; by tax year {2018: 22, 2019: 397, 2020: 3884, 2021: 4256, 2022: 4527, 2023: 4835, 2024: 4912, 2025: 2534}; by release year {2021: 3679, 2022: 4169, 2023: 4553, 2024: 4872, 2025: 5068, 2026: 3026}; same EIN+period+type repeats (amended/superseded) 213
  - after keeping the latest OBJECT_ID per EIN+TAX_PERIOD+type: 25,154 returns; TY2020-TY2024 22,210
  - ZIP batches: 52 distinct ZIPs touched (2021_TEOS_XML_01A 3679, 2022_ANY 4169, 2023_ANY 4553, 2024_TEOS_XML_01A 72, 2024_TEOS_XML_02A 185, 2024_TEOS_XML_03A 195, 2024_TEOS_XML_04A 386, 2024_TEOS_XML_05A 1326, 2024_TEOS_XML_06A 182, 2024_TEOS_XML_07A 256, 2024_TEOS_XML_08A 258, 2024_TEOS_XML_09A 260, 2024_TEOS_XML_10A 240, 2024_TEOS_XML_11A 1407, 2024_TEOS_XML_12A 105, 2025_TEOS_XML_01A 69, 2025_TEOS_XML_02A 185, 2025_TEOS_XML_03A 274, 2025_TEOS_XML_04A 417, 2025_TEOS_XML_05* 1363, 2025_TEOS_XML_06A 283, 2025_TEOS_XML_07A 131, 2025_TEOS_XML_08A 186, 2025_TEOS_XML_09A 307, 2025_TEOS_XML_10A 43, 2025_TEOS_XML_11A 383, 2025_TEOS_XML_11B 568, 2025_TEOS_XML_11C 330, 2025_TEOS_XML_11D 416, 2025_TEOS_XML_12A 113, 2026_TEOS_XML_01A 42, 2026_TEOS_XML_02A 198, 2026_TEOS_XML_03A 327, 2026_TEOS_XML_04A 384, 2026_TEOS_XML_05* 1392, 2026_TEOS_XML_06A 219, 2026_TEOS_XML_07A 194, 2026_TEOS_XML_08A 270)
  - bytes: full ZIP downloads 23.4 GB; remotezip ~491 MB (central directories 340.3 MB + members ~151.1 MB compressed); GT S3 per-object ~805.3 MB uncompressed
- (b: DC public charities L/P/F/I/J/W) 4,580 returns from 968 EINs; by type {'990EZ': 670, '990': 3907, '990PF': 3}; by tax year {2018: 5, 2019: 215, 2020: 731, 2021: 812, 2022: 826, 2023: 883, 2024: 885, 2025: 223}; by release year {2021: 712, 2022: 783, 2023: 832, 2024: 874, 2025: 899, 2026: 480}; same EIN+period+type repeats (amended/superseded) 114
  - after keeping the latest OBJECT_ID per EIN+TAX_PERIOD+type: 4,466 returns; TY2020-TY2024 4,032
  - ZIP batches: 52 distinct ZIPs touched (2021_TEOS_XML_01A 712, 2022_ANY 783, 2023_ANY 832, 2024_TEOS_XML_01A 16, 2024_TEOS_XML_02A 26, 2024_TEOS_XML_03A 39, 2024_TEOS_XML_04A 60, 2024_TEOS_XML_05A 133, 2024_TEOS_XML_06A 47, 2024_TEOS_XML_07A 45, 2024_TEOS_XML_08A 78, 2024_TEOS_XML_09A 50, 2024_TEOS_XML_10A 63, 2024_TEOS_XML_11A 299, 2024_TEOS_XML_12A 18, 2025_TEOS_XML_01A 12, 2025_TEOS_XML_02A 38, 2025_TEOS_XML_03A 30, 2025_TEOS_XML_04A 56, 2025_TEOS_XML_05* 142, 2025_TEOS_XML_06A 46, 2025_TEOS_XML_07A 28, 2025_TEOS_XML_08A 90, 2025_TEOS_XML_09A 53, 2025_TEOS_XML_10A 15, 2025_TEOS_XML_11A 91, 2025_TEOS_XML_11B 114, 2025_TEOS_XML_11C 85, 2025_TEOS_XML_11D 78, 2025_TEOS_XML_12A 21, 2026_TEOS_XML_01A 14, 2026_TEOS_XML_02A 34, 2026_TEOS_XML_03A 46, 2026_TEOS_XML_04A 54, 2026_TEOS_XML_05* 130, 2026_TEOS_XML_06A 51, 2026_TEOS_XML_07A 59, 2026_TEOS_XML_08A 92)
  - bytes: full ZIP downloads 23.4 GB; remotezip ~368 MB (central directories 340.3 MB + members ~27.3 MB compressed); GT S3 per-object ~145.5 MB uncompressed

### 2026-10-10 12:41 — 12_probe_federal: sam
- Assistance Listings extract: 2871 active listings, 38 columns (raw/sam/20261010T123845_AssistanceListings_DataGov_PUBLIC_CURRENT.csv)
- target CFDAs missing from active extract: ['21.019', '14.235']
- sgs cfda search http 200 hits 4; sgs ei result types {'exclusion': 10} (Calvary UEI found: False)
- api.sam.gov without key: {'entity_v3': 404, 'assistance_listings_v1': 404}

### 2026-10-10 12:42 — 02_extract_inputs
- appended one-time correction to notes_for_analysis.md (heading "Inputs (Phase 1): correction"): support-page all-caps names were skipped on the first run; fixed in script

### 2026-10-10 12:42 — 12_probe_federal: slfrf
- subaward file: {"sheet": "SLFRF Subawards as of 06-30-23", "rows": 37616, "dc_prime_rows": 462, "dc_prime_amount": 815227025, "raw": "raw/treasury_slfrf/20261010T124148_SLFRF-Subaward-USASpending-File.xlsx"}
- Calvary rows: [{"subawardee": "Calvary Women's Services Inc.", "amount": 113488, "date": "2021-08-05", "prime": "DISTRICT OF COLUMBIA GOVERNMENT", "sub_number": "1500", "description": "\"Provide 15 beds of transitional housing and wraparound services, serving at least 25 unaccompanied homeless women who are fleeing domestic violence.\""}, {"subawardee": "Calvary Women's Services Inc.", "amount": 3680675, "date": "2022-03-08", "prime": "DISTRICT OF COLUMBIA GOVERNMENT", "sub_number": "12126", "description": "\"Purchase a building to create New Foundations, a transitional housing program serving up to 35 homeless women who are survivors of domestic violence. \""}]
- projects file: {"sheets": ["Definitions", "Recipients (Q1 2026)", "Projects (Q1 2026)", "2025 Recovery Plans"], "dc_projects": 305, "dc_projects_sector_keyword": 33, "has_subrecipient_columns": false, "raw": "raw/treasury_slfrf/20261010T124217_April-2026-Reporting-Data-through-March-31-2026.xlsx"}

### 2026-10-10 12:42 — 12_probe_federal: catalog
- wrote sources/catalog_parts/federal.csv; sections run: ['fac', 'grantsgov', 'sam', 'slfrf']

### 2026-10-10 12:42 — 12_probe_federal: usaspending recipient
- autocomplete: [("CALVARY WOMEN'S SERVICES, INC", None), ("CALVARY WOMEN'S SERVICES", None)]
- /recipient/ rows: 3; UEI KMGRTKET2KJ1 (DUNS 126543453) on P/C levels; R-level name-only record has no UEI
- profiles: {"2813d90d-8166-9870-4c74-3eca995e2739-C": {"total_transaction_amount": 200000.0, "total_transactions": 1, "loan_face_value": 0.0, "address": "1217 GOOD HOPE RD SE", "congressional_code": "98", "business_types": ["category_business", "corporate_entity_tax_exempt", "nonprofit"]}, "2813d90d-8166-9870-4c74-3eca995e2739-P": {"total_transaction_amount": 200000.0, "total_transactions": 1, "loan_face_value": 0.0, "address": "1217 GOOD HOPE RD SE", "congressional_code": "98", "business_types": ["category_business", "corporate_entity_tax_exempt", "nonprofit"]}, "a141975f-7383-7c48-fffa-47d17089658a-R": {"total_transaction_amount": 332827.84, "total_transactions": 1, "loan_face_value": 327200.0, "address": "1217 GOOD HOPE RD, S.E.", "congressional_code": "98", "business_types": ["nonprofit"]}}

### 2026-10-10 12:42 — 10_probe_filings: remotezip
- 52 ZIP names for 2021-2026 (downloads page + index batch ids); 52 reachable (HTTP 200, Accept-Ranges); not reachable: none
  - 2021: 1 ZIPs, 3.72 GB, 589,904 members, central directories 55.5 MB
  - 2022: 2 ZIPs, 4.01 GB, 656,503 members, central directories 62.6 MB
  - 2023: 12 ZIPs, 4.29 GB, 705,154 members, central directories 65.6 MB
  - 2024: 12 ZIPs, 4.39 GB, 728,719 members, central directories 67.8 MB
  - 2025: 16 ZIPs, 4.46 GB, 748,906 members, central directories 56.2 MB
  - 2026: 9 ZIPs, 2.56 GB, 436,239 members, central directories 32.7 MB
  - 2021_TEOS_XML_01A: 3,715.5 MB, 589,904 members, CD 55.5 MB, Thu, 06 Mar 2025 20:08:25 GMT, page
  - 2022_TEOS_XML_01A: 2,603.7 MB, 433,529 members, CD 41.2 MB, Thu, 06 Mar 2025 20:08:56 GMT, page
  - 2022_TEOS_XML_02A: 1,408.2 MB, 222,974 members, CD 21.4 MB, Thu, 06 Mar 2025 20:06:10 GMT, probe_only
  - 2023_TEOS_XML_01A: 123.1 MB, 21,513 members, CD 2.0 MB, Thu, 06 Mar 2025 17:04:40 GMT, page
  - 2023_TEOS_XML_02A: 234.6 MB, 40,304 members, CD 3.7 MB, Thu, 06 Mar 2025 17:07:26 GMT, page
  - 2023_TEOS_XML_03A: 197.2 MB, 36,224 members, CD 3.4 MB, Thu, 06 Mar 2025 17:06:19 GMT, page
  - 2023_TEOS_XML_04A: 244.5 MB, 42,995 members, CD 4.0 MB, Thu, 06 Mar 2025 17:07:59 GMT, page
  - 2023_TEOS_XML_05A: 990.5 MB, 156,228 members, CD 14.5 MB, Thu, 06 Mar 2025 17:27:59 GMT, page
  - 2023_TEOS_XML_06A: 163.7 MB, 29,240 members, CD 2.7 MB, Thu, 06 Mar 2025 17:05:35 GMT, page
  - 2023_TEOS_XML_07A: 219.9 MB, 38,027 members, CD 3.5 MB, Thu, 06 Mar 2025 17:07:06 GMT, page
  - 2023_TEOS_XML_08A: 266.2 MB, 42,301 members, CD 3.9 MB, Thu, 06 Mar 2025 17:08:23 GMT, page
  - 2023_TEOS_XML_09A: 200.4 MB, 35,070 members, CD 3.3 MB, Thu, 06 Mar 2025 17:06:29 GMT, page
  - 2023_TEOS_XML_10A: 332.5 MB, 56,858 members, CD 5.3 MB, Thu, 06 Mar 2025 17:10:21 GMT, page
  - 2023_TEOS_XML_11A: 1,200.3 MB, 186,387 members, CD 17.3 MB, Thu, 06 Mar 2025 17:32:53 GMT, page
  - 2023_TEOS_XML_12A: 120.7 MB, 20,007 members, CD 1.9 MB, Thu, 06 Mar 2025 17:04:34 GMT, page
  - 2024_TEOS_XML_01A: 104.8 MB, 17,246 members, CD 1.6 MB, Thu, 06 Mar 2025 14:04:31 GMT, page
  - 2024_TEOS_XML_02A: 243.7 MB, 40,284 members, CD 3.7 MB, Thu, 06 Mar 2025 14:04:23 GMT, page
  - 2024_TEOS_XML_03A: 209.3 MB, 38,418 members, CD 3.6 MB, Thu, 06 Mar 2025 14:04:55 GMT, page
  - 2024_TEOS_XML_04A: 350.3 MB, 59,487 members, CD 5.5 MB, Thu, 06 Mar 2025 14:05:02 GMT, page
  - 2024_TEOS_XML_05A: 977.5 MB, 156,237 members, CD 14.5 MB, Thu, 06 Mar 2025 14:05:40 GMT, page
  - 2024_TEOS_XML_06A: 163.9 MB, 29,408 members, CD 2.7 MB, Thu, 06 Mar 2025 14:04:01 GMT, page
  - 2024_TEOS_XML_07A: 288.3 MB, 50,144 members, CD 4.7 MB, Thu, 06 Mar 2025 14:04:23 GMT, page
  - 2024_TEOS_XML_08A: 260.6 MB, 41,687 members, CD 3.9 MB, Thu, 06 Mar 2025 14:04:56 GMT, page
  - 2024_TEOS_XML_09A: 247.0 MB, 44,108 members, CD 4.1 MB, Thu, 06 Mar 2025 14:04:54 GMT, page
  - 2024_TEOS_XML_10A: 251.6 MB, 43,392 members, CD 4.0 MB, Thu, 06 Mar 2025 14:04:55 GMT, page
  - 2024_TEOS_XML_11A: 1,165.6 MB, 186,632 members, CD 17.4 MB, Thu, 06 Mar 2025 14:05:48 GMT, page
  - 2024_TEOS_XML_12A: 128.3 MB, 21,676 members, CD 2.0 MB, Thu, 06 Mar 2025 14:04:05 GMT, page
  - 2025_TEOS_XML_01A: 103.7 MB, 17,044 members, CD 1.3 MB, Wed, 05 Mar 2025 15:12:42 GMT, page
  - 2025_TEOS_XML_02A: 239.9 MB, 41,855 members, CD 3.1 MB, Wed, 19 Mar 2025 13:01:47 GMT, page
  - 2025_TEOS_XML_03A: 222.6 MB, 41,570 members, CD 3.1 MB, Wed, 16 Apr 2025 13:01:48 GMT, page
  - 2025_TEOS_XML_04A: 338.2 MB, 57,595 members, CD 4.3 MB, Wed, 21 May 2025 13:09:56 GMT, page
  - 2025_TEOS_XML_05A: 495.9 MB, 81,770 members, CD 6.1 MB, Wed, 25 Jun 2025 13:13:15 GMT, page
  - 2025_TEOS_XML_05B: 501.0 MB, 81,770 members, CD 6.1 MB, Wed, 25 Jun 2025 13:13:33 GMT, page
  - 2025_TEOS_XML_06A: 246.8 MB, 44,824 members, CD 3.4 MB, Wed, 20 Aug 2025 13:11:59 GMT, page
  - 2025_TEOS_XML_07A: 143.5 MB, 24,854 members, CD 1.9 MB, Wed, 20 Aug 2025 13:08:44 GMT, page
  - 2025_TEOS_XML_08A: 262.7 MB, 42,291 members, CD 3.2 MB, Wed, 17 Sep 2025 13:18:06 GMT, page
  - 2025_TEOS_XML_09A: 256.3 MB, 45,643 members, CD 3.4 MB, Wed, 19 Nov 2025 20:41:59 GMT, page
  - 2025_TEOS_XML_10A: 56.5 MB, 9,836 members, CD 0.7 MB, Wed, 19 Nov 2025 14:08:07 GMT, page
  - 2025_TEOS_XML_11A: 340.1 MB, 55,488 members, CD 4.2 MB, Wed, 17 Dec 2025 14:31:07 GMT, page
  - 2025_TEOS_XML_11B: 494.5 MB, 80,283 members, CD 6.0 MB, Wed, 17 Dec 2025 14:43:04 GMT, page
  - 2025_TEOS_XML_11C: 277.9 MB, 44,896 members, CD 3.4 MB, Wed, 17 Dec 2025 14:25:37 GMT, page
  - 2025_TEOS_XML_11D: 332.8 MB, 53,800 members, CD 4.0 MB, Wed, 17 Dec 2025 17:10:02 GMT, page
  - 2025_TEOS_XML_12A: 151.8 MB, 25,387 members, CD 1.9 MB, Wed, 21 Jan 2026 14:14:30 GMT, page
  - 2026_TEOS_XML_01A: 71.5 MB, 12,245 members, CD 0.9 MB, Thu, 19 Feb 2026 18:32:24 GMT, page
  - 2026_TEOS_XML_02A: 222.1 MB, 38,719 members, CD 2.9 MB, Wed, 18 Mar 2026 13:02:56 GMT, page
  - 2026_TEOS_XML_03A: 259.3 MB, 48,471 members, CD 3.6 MB, Wed, 15 Apr 2026 13:03:42 GMT, page
  - 2026_TEOS_XML_04A: 261.9 MB, 47,627 members, CD 3.6 MB, Wed, 20 May 2026 13:02:32 GMT, page
  - 2026_TEOS_XML_05A: 521.2 MB, 84,172 members, CD 6.3 MB, Wed, 17 Jun 2026 13:13:47 GMT, page
  - 2026_TEOS_XML_05B: 513.4 MB, 84,172 members, CD 6.3 MB, Wed, 17 Jun 2026 13:13:52 GMT, page
  - 2026_TEOS_XML_06A: 210.8 MB, 38,244 members, CD 2.9 MB, Wed, 15 Jul 2026 16:01:18 GMT, page
  - 2026_TEOS_XML_07A: 189.2 MB, 32,240 members, CD 2.4 MB, Wed, 19 Aug 2026 13:00:50 GMT, page
  - 2026_TEOS_XML_08A: 314.7 MB, 50,349 members, CD 3.8 MB, Wed, 16 Sep 2026 13:02:45 GMT, index_only
  - release 2021: index rows 589,904 vs ZIP members 589,904 (diff +0)
  - release 2022: index rows 656,503 vs ZIP members 656,503 (diff +0)
  - release 2023: index rows 705,156 vs ZIP members 705,154 (diff -2)
  - release 2024: index rows 728,719 vs ZIP members 728,719 (diff +0)
  - release 2025: index rows 748,906 vs ZIP members 748,906 (diff +0)
  - release 2026: index rows 436,239 vs ZIP members 436,239 (diff +0)
  - 2025_TEOS_XML_05A vs 2025_TEOS_XML_05B: 81,770 / 81,770 object ids, overlap 0; index rows labelled 2025_TEOS_XML_05A: 163,540, found in 2025_TEOS_XML_05A 81,770, in 2025_TEOS_XML_05B 81,770 (read 12.4 MB of central directory)
  - 2026_TEOS_XML_05A vs 2026_TEOS_XML_05B: 84,172 / 84,172 object ids, overlap 0; index rows labelled 2026_TEOS_XML_05A: 168,344, found in 2026_TEOS_XML_05A 84,172, in 2026_TEOS_XML_05B 84,172 (read 12.8 MB of central directory)
- remotezip 2026_TEOS_XML_06A (210.8 MB, 38,244 members, names like 202601429339300000_public.xml): central directory 2 requests / 2.9 MB; member 202631539349300848_public.xml 54,115 B (10,872 B compressed); total 3 requests / 2.9 MB = 1.40% of the ZIP; 0.4s -> raw/xml/irs/20261010T122754_521307706_TY2024_2026_TEOS_XML_06A_202631539349300848_public.xml
- 2026_TEOS_XML_06A: mean member 28.7 KB uncompressed, compression ratio 5.3x
- GT S3 copy of 202631539349300848 byte-identical to the IRS ZIP member: True
- Calvary TY2021 202322239349302102 (release 2023, no batch id; DLN day -> month 08): found in 2023_TEOS_XML_08A after reading 1 central directories (4.0 MB)

### 2026-10-10 12:42 — 12_probe_federal: usaspending Calvary awards
- prime awards (all types, FY2008+): 2 -> grants B-22-CP-DC-0213 ['14.251'] $200,000 Department of Housing and Urban Development; loans 5894917008 ['59.073'] $327,200 Small Business Administration
- Calvary subawards (FSRS): 1 -> LOCAL INITIATIVES SUPPORT CORPORATION 14.252 $25,000 2017-08-18
- transactions: 2

### 2026-10-10 12:43 — 10_probe_filings: volume
- BMF sets: (a) DMV PF filers (FOUNDATION 02/03/04 or PF_FILING_REQ_CD=1) 5,855 EINs; (b) DC 501(c)(3) public charities in NTEE L/P/F/I/J/W 1,750 EINs
- (a: DMV 990-PF filers) 25,367 returns from 5,249 EINs; by type {'990PF': 25367}; by tax year {2018: 22, 2019: 397, 2020: 3884, 2021: 4256, 2022: 4527, 2023: 4835, 2024: 4912, 2025: 2534}; by release year {2021: 3679, 2022: 4169, 2023: 4553, 2024: 4872, 2025: 5068, 2026: 3026}; same EIN+period+type repeats (amended/superseded) 213
  - after keeping the latest OBJECT_ID per EIN+TAX_PERIOD+type: 25,154 returns; TY2020-TY2024 22,210
  - ZIP batches: 52 distinct ZIPs touched (2021_TEOS_XML_01A 3679, 2022_ANY 4169, 2023_ANY 4553, 2024_TEOS_XML_01A 72, 2024_TEOS_XML_02A 185, 2024_TEOS_XML_03A 195, 2024_TEOS_XML_04A 386, 2024_TEOS_XML_05A 1326, 2024_TEOS_XML_06A 182, 2024_TEOS_XML_07A 256, 2024_TEOS_XML_08A 258, 2024_TEOS_XML_09A 260, 2024_TEOS_XML_10A 240, 2024_TEOS_XML_11A 1407, 2024_TEOS_XML_12A 105, 2025_TEOS_XML_01A 69, 2025_TEOS_XML_02A 185, 2025_TEOS_XML_03A 274, 2025_TEOS_XML_04A 417, 2025_TEOS_XML_05* 1363, 2025_TEOS_XML_06A 283, 2025_TEOS_XML_07A 131, 2025_TEOS_XML_08A 186, 2025_TEOS_XML_09A 307, 2025_TEOS_XML_10A 43, 2025_TEOS_XML_11A 383, 2025_TEOS_XML_11B 568, 2025_TEOS_XML_11C 330, 2025_TEOS_XML_11D 416, 2025_TEOS_XML_12A 113, 2026_TEOS_XML_01A 42, 2026_TEOS_XML_02A 198, 2026_TEOS_XML_03A 327, 2026_TEOS_XML_04A 384, 2026_TEOS_XML_05* 1392, 2026_TEOS_XML_06A 219, 2026_TEOS_XML_07A 194, 2026_TEOS_XML_08A 270)
  - bytes: full ZIP downloads 23.4 GB; remotezip ~491 MB (central directories 340.3 MB + members ~151.1 MB compressed); GT S3 per-object ~805.3 MB uncompressed
- (b: DC public charities L/P/F/I/J/W) 4,580 returns from 968 EINs; by type {'990EZ': 670, '990': 3907, '990PF': 3}; by tax year {2018: 5, 2019: 215, 2020: 731, 2021: 812, 2022: 826, 2023: 883, 2024: 885, 2025: 223}; by release year {2021: 712, 2022: 783, 2023: 832, 2024: 874, 2025: 899, 2026: 480}; same EIN+period+type repeats (amended/superseded) 114
  - after keeping the latest OBJECT_ID per EIN+TAX_PERIOD+type: 4,466 returns; TY2020-TY2024 4,032
  - ZIP batches: 52 distinct ZIPs touched (2021_TEOS_XML_01A 712, 2022_ANY 783, 2023_ANY 832, 2024_TEOS_XML_01A 16, 2024_TEOS_XML_02A 26, 2024_TEOS_XML_03A 39, 2024_TEOS_XML_04A 60, 2024_TEOS_XML_05A 133, 2024_TEOS_XML_06A 47, 2024_TEOS_XML_07A 45, 2024_TEOS_XML_08A 78, 2024_TEOS_XML_09A 50, 2024_TEOS_XML_10A 63, 2024_TEOS_XML_11A 299, 2024_TEOS_XML_12A 18, 2025_TEOS_XML_01A 12, 2025_TEOS_XML_02A 38, 2025_TEOS_XML_03A 30, 2025_TEOS_XML_04A 56, 2025_TEOS_XML_05* 142, 2025_TEOS_XML_06A 46, 2025_TEOS_XML_07A 28, 2025_TEOS_XML_08A 90, 2025_TEOS_XML_09A 53, 2025_TEOS_XML_10A 15, 2025_TEOS_XML_11A 91, 2025_TEOS_XML_11B 114, 2025_TEOS_XML_11C 85, 2025_TEOS_XML_11D 78, 2025_TEOS_XML_12A 21, 2026_TEOS_XML_01A 14, 2026_TEOS_XML_02A 34, 2026_TEOS_XML_03A 46, 2026_TEOS_XML_04A 54, 2026_TEOS_XML_05* 130, 2026_TEOS_XML_06A 51, 2026_TEOS_XML_07A 59, 2026_TEOS_XML_08A 92)
  - bytes: full ZIP downloads 23.4 GB; remotezip ~368 MB (central directories 340.3 MB + members ~27.3 MB compressed); GT S3 per-object ~145.5 MB uncompressed

### 2026-10-10 12:44 — lead: CRM export decisions
- User (2026-10-10): GIFT_TOTAL in `Foundation & Corporate Funders_2023-2026.xlsx` is believed to cover the 2023–2026 window only. Record as window-limited, confidence=medium, basis=documented (user statement).
- In-kind vs cash vs pledge is unknown. Planned cross-checks, no user input needed:
  (a) Phase 4: match CRM foundation totals to grants paid to Calvary on the funders' 990-PF filings (Part XV/XIV).
  (b) Calvary 990 TY2023/TY2024 Part VIII line 1g noncash + Schedule M, as an upper bound on in-kind.
  (c) Tavily search on the top non-foundation donors (MGAC, Health Equity Fund, Capital One) for pro bono or in-kind evidence.
- Output: a CRM-vs-filings reconciliation section in reports/data_quality.md. Each CRM funder row gets a `cash_verified` flag (yes/partial/no/unknown) plus evidence.

### 2026-10-10 12:44 — 01_inventory_inputs
- sources/input_inventory.csv: 30 rows (duplicate=1, ok=24, partial=4, unreadable=1)
- registered 30 input_* sources
- period checks: all match

### 2026-10-10 12:44 — 14_probe_dc_hud: notes
- Earlier 14_probe_dc_hud log entries from today before the full run (sections 'DC Open Data', 'DC budget books', 'DC Council', 'HUD') were test runs; their raw files were removed and replaced by the single full run that follows them. The full run is the last set of entries with these section names.
- Catalog part written: sources/catalog_parts/dc_hud.csv (30 rows) and dc_hud.md.
- New package installed (not in requirements.txt): pyxlsb 1.0.10 (reads HUD PIT .xlsb).

### 2026-10-10 12:45 — 12_probe_federal: usaspending DC probes
- CFDA titles (USAspending autocomplete): {"14.267": "Continuum of Care Program", "14.231": "Emergency Solutions Grant Program", "14.241": "Housing Opportunities for Persons with AIDS", "14.218": "Community Development Block Grants/Entitlement Grants", "14.239": "Home Investment Partnerships Program", "16.575": "Crime Victim Assistance", "16.588": "Violence Against Women Formula Grants", "16.736": "Transitional Housing Assistance for Victims of Domestic Violence, Dating Violence, Stalking, or Sexual Assault", "93.671": "Family Violence Prevention and Services/Domestic Violence Shelter and Supportive Services", "93.959": "Block Grants for Prevention and Treatment of Substance Abuse", "93.958": "Block Grants for Community Mental Health Services", "93.243": "Substance Abuse and Mental Health Services Projects of Regional and National Significance", "21.027": "CORONAVIRUS STATE AND LOCAL FISCAL RECOVERY FUNDS", "21.019": "Coronavirus Relief Fund", "97.024": "Emergency Food and Shelter National Board Program", "64.033": "VA Supportive Services for Veteran Families Program", "17.258": "WIOA Adult Program", "17.259": "WIOA Youth Activities", "16.812": "Second Chance Act Reentry Initiative", "14.235": "Supportive Housing Program", "10.561": "State Administrative Matching Grants for the Supplemental Nutrition Assistance Program", "14.251": "Economic Development Initiative, Community Project Funding, and Miscellaneous grants", "14.252": "Section 4 Capacity Building for Community Development and Affordable Housing", "59.073": "Paycheck Protection Loan Program (PPP)", "21.023": "Emergency Rental Assistance Program"}
- DC counts per CFDA FY2019-FY2026 (recipient in DC): {"14.267": {"grants": 494, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 2}, "14.231": {"grants": 12, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 1}, "14.241": {"grants": 11, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 103}, "14.218": {"grants": 11, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 137}, "14.239": {"grants": 11, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 4}, "16.575": {"grants": 10, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 116}, "16.588": {"grants": 11, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 42}, "16.736": {"grants": 7, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 0}, "93.671": {"grants": 19, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 5}, "93.959": {"grants": 12, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 69}, "93.958": {"grants": 16, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 55}, "93.243": {"grants": 77, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 256}, "21.027": {"grants": 0, "direct_payments": 5, "other": 0, "loans": 0, "subgrants": 0}, "21.019": {"grants": 0, "direct_payments": 2, "other": 0, "loans": 0, "subgrants": 0}, "97.024": {"grants": 0, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 0}, "64.033": {"grants": 36, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 0}, "17.258": {"grants": 10, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 1}, "17.259": {"grants": 9, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 1}, "16.812": {"grants": 9, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 26}, "14.235": {"grants": 0, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 0}, "10.561": {"grants": 64, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 15}, "14.251": {"grants": 21, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 0}, "14.252": {"grants": 0, "direct_payments": 0, "other": 0, "loans": 0, "subgrants": 71}, "59.073": {"grants": 0, "direct_payments": 0, "other": 0, "loans": 32800, "subgrants": 0}, "21.023": {"grants": 0, "direct_payments": 3, "other": 0, "loans": 0, "subgrants": 0}}
- DC prime probe: {"rows": 836, "by_group": {"grants": 826, "direct_payments": 10}, "dc_gov_rows_name_match": 224, "dc_gov_amount": 4439095425, "dc_gov_by_cfda": {"10.561": 60, "14.267": 23, "93.671": 16, "93.958": 15, "93.959": 11, "14.241": 11, "16.588": 11, "14.231": 10, "16.575": 10, "93.243": 10, "14.239": 9, "14.218": 7, "93.243,93.788": 4, "17.258,17.259,17.278": 4, "21.027": 4, "17.259": 3, "17.258": 3, "21.023": 3, "14.218,14.228": 2, "16.812": 2, "21.019": 2, "14.218,14.248": 1, "93.00R,93.243": 1, "93.104,93.243": 1, "10.551,10.561": 1}, "dc_gov_recipient_names": {"DISTRICT COLUMBIA GOVERNMENT": 112, "GOVERNMENT OF THE DISTRICT OF COLUMBIA": 45, "DISTRICT OF COLUMBIA, GOVERNMENT OF": 27, "DC OFFICE OF VICTIM SERVICES": 21, "DISTRICT OF COLUMBIA GOVERNMENT OF": 10, "DISTRICT OF COLUMBIA GOVERNMENT": 9}, "recipient_type_government_counts": {"contracts": 0, "direct_payments": 10, "grants": 195, "idvs": 0, "loans": 0, "other": 0}, "calvary_rows": ["B-22-CP-DC-0213"]}
- DC subaward probe: {"rows": 891, "dc_gov_prime_rows": 546, "dc_gov_prime_amount": 177195890, "by_cfda": {"93.243, 93.788": 175, "14.218": 136, "16.575": 116, "14.241": 103, "14.252": 71, "93.243": 64, "93.959": 59, "93.958": 50, "16.588": 42, "10.561": 15, "16.812": 15, "16.735, 16.812": 11, "93.243, 93.959": 6, "93.243, 93.958": 5, "93.671": 5, "14.239": 4, "93.104, 93.243": 4, "93.590, 93.959": 4, "14.267": 2, "93.150, 93.243": 2, "17.258, 17.259, 17.278": 1, "14.231": 1}, "dc_gov_by_cfda": {"93.243, 93.788": 145, "14.218": 116, "14.241": 103, "16.575": 77, "93.959": 39, "16.588": 30, "93.958": 24, "93.243": 4, "93.104, 93.243": 4, "14.239": 3, "16.812": 1}, "prime_names": [["GOVERNMENT OF THE DISTRICT OF COLUMBIA", 216], ["DISTRICT OF COLUMBIA GOVERNMENT OF", 119], ["DISTRICT OF COLUMBIA, GOVERNMENT OF", 103], ["DC OFFICE OF VICTIM SERVICES", 82], ["LOCAL INITIATIVES SUPPORT CORPORATION", 45], ["ENTERPRISE COMMUNITY PARTNERS, INC.", 26], ["OFFICE OF VICTIM SERVICES AND JUSTICE GRANTS", 24], ["EXECUTIVE OFFICE OF THE STATE OF MARYLAND", 23], ["PUBLIC HEALTH AND HUMAN SERVICES, MONTANA DEPARTMENT OF", 22], ["PRINCE GEORGE'S COUNTY, MARYLAND", 17], ["ILLINOIS DEPARTMENT OF HUMAN SERVICE", 14], ["IMPACT JUSTICE", 13]], "by_year": {"2018": 49, "2019": 62, "2020": 120, "2021": 72, "2022": 64, "2023": 116, "2024": 150, "2025": 206, "2026": 52}, "calvary_rows": []}
- download/count sizing: {"dc_target_cfdas_grants_direct": {"awards": 836, "transactions": 2100, "subawards": 891}, "dc_all_grants": {"awards": 21168, "transactions": 79160, "subawards": 23709}, "dc_nonprofit_grants": {"awards": 9028, "transactions": 34073, "subawards": 2569}, "dc_pop_target_cfdas": {"awards": 818, "transactions": 2067, "subawards": 513}, "slfrf_21027_dc": {"awards": 5, "transactions": 9, "subawards": 0}}

### 2026-10-10 12:45 — 12_probe_federal: usaspending downloads
- download_awards_calvary: {"status": "finished", "total_rows": 3, "seconds": 0, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H16M36S53_1.csv": 2, "Assistance_Subawards_2026-10-10_H16M36S55_1.csv": 1}, "raw": "raw/usaspending/20261010T123659_download_awards_calvary.zip"}
- bulk_download_hud_dc_fy2024: {"status": "finished", "total_rows": 658, "seconds": 0, "members": {"All_Assistance_PrimeTransactions_2026-10-10_H16M24S40_1.csv": 599, "All_Assistance_Subawards_2026-10-10_H16M25S01_1.csv": 59}, "raw": "raw/usaspending/20261010T123701_bulk_download_hud_dc_fy2024.zip"}

### 2026-10-10 12:45 — 12_probe_federal: catalog
- wrote sources/catalog_parts/federal.csv; sections run: ['usaspending', 'usa_download']

### 2026-10-10 12:45 — lead: housekeeping
- Moved stray root-level ob26.html (exploration leftover, likely an OBP FY26 budget page; no script references it, URL unrecorded) to raw/_unattributed/. Not used by any clean table.
- Re-pinned requirements.txt after subagents added openpyxl and pyxlsb.

### 2026-10-10 12:46 — 10_probe_filings: gt
- irs-data/efilexml?ein=521307706: HTTP 200, no_results 7
- irs-data/990basic120fields?ein=521307706: HTTP 200, no_results 8
- irs-data/bmf?ein=521307706: HTTP 200, no_results 1
- irs-data/postcard?ein=521307706: HTTP 200, no_results 0
- irs-data/pub78-deductible?ein=521307706: HTTP 200, no_results 1
- irs-data/revoked?ein=521307706: HTTP 200, no_results 0
- probe docs_path_irs_data_underscore (irs_data/efilexml {'ein': '521307706'}): HTTP 403, Missing Authentication Token
- probe no_ein (irs-data/990basic120fields {}): HTTP 400, Missing required request parameters: [ein]
- probe state_filter_only (irs-data/990basic120fields {'state': 'DC'}): HTTP 400, Missing required request parameters: [ein]
- probe two_eins_comma (irs-data/990basic120fields {'ein': '521307706,530241716'}): HTTP 200, Your EIN should be 9 digits long with no hyphens. i.e 123456789 not 12-3456789 We recommend adding zeros if the ein is t
- probe taxyear_param_ignored (irs-data/990basic120fields {'ein': '521307706', 'taxyear': '2021'}): HTTP 200, no_results 8
- probe undocumented_990pf (irs-data/990pf {'ein': '521307706'}): HTTP 403, Missing Authentication Token
- efilexml TaxYear set: ['2014', '2015', '2016', '2017', '2018', '2019', '2020']; IndexedOn max 2023-11-19; columns: id, BuildTs, DAF, DateSigned, DocStatus, EIN, FileSha256, FileSizeBytes, FormType, GrossReceipts, GroupAffiliatesIncluded, GroupExemptionNumber, GroupReturnForAffiliates, IndexedOn, LegalDomicileCountry, LegalDomicileState, ObjectId, OrgType, OrganizationName, ReturnTs, ReturnVersion, SubmittedOn, TaxPeriod, TaxPeriodBeginDate, TaxPeriodEndDate, TaxStatus, TaxYear, TotalAssetsBkEOY, TotalExpensesCY, TotalLiabilitiesBkEOY, TotalNetAssetsBkEOY, TotalRevenueCY, URL, Website, YearFormed, ZipFile
- 990basic120fields TAXYEAR set: ['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021']; 117 columns; rows with URL: 6; TY2021 TOTREVCURYEA ['8867250']
- bmf: Date_Released 2024_02_13, tax_period 202209 (stale vs IRS BMF)
- XML TY2014 201600959349300900 (2014v6.0): 46,911 B, sha256 matches -> raw/xml/gt/20261010T122336_521307706_TY2014_201600959349300900_public.xml
- XML TY2015 201731189349300503 (2015v3.0): 46,924 B, sha256 matches -> raw/xml/gt/20261010T122336_521307706_TY2015_201731189349300503_public.xml
- XML TY2016 201801039349300220 (2016v3.0): 46,480 B, sha256 matches -> raw/xml/gt/20261010T122336_521307706_TY2016_201801039349300220_public.xml
- XML TY2017 201910249349300501 (2017v2.3): 48,631 B, sha256 matches -> raw/xml/gt/20261010T122336_521307706_TY2017_201910249349300501_public.xml
- XML TY2018 202010389349301241 (2018v3.1): 46,326 B, sha256 matches -> raw/xml/gt/20261010T122337_521307706_TY2018_202010389349301241_public.xml
- XML TY2019 202130449349300208 (2019v5.2): 45,792 B, sha256 matches -> raw/xml/gt/20261010T122337_521307706_TY2019_202130449349300208_public.xml
- XML TY2020 202212279349301511 (2020v4.2): 51,469 B, sha256 matches -> raw/xml/gt/20261010T122337_521307706_TY2020_202212279349301511_public.xml
- data lake Indices/990xmls/: 250 objects; latest yearly build 2026-08-25: 2007 0.0 MB, 2008 0.1 MB, 2009 22.4 MB, 2010 92.2 MB, 2011 120.3 MB, 2012 136.5 MB, 2013 142.8 MB, 2014 171.9 MB, 2015 184.6 MB, 2016 193.4 MB, 2017 207.7 MB, 2018 221.1 MB, 2019 231.6 MB, 2020 286.3 MB, 2021 298.7 MB, 2022 304.0 MB, 2023 310.1 MB, 2024 267.6 MB, 2025 78.2 MB
- data lake EfileData/XmlZips/: 103 ZIPs, latest modified 2026-08-25
- GT S3 XmlFiles 202130449349300208 (TAX_PERIOD 202009): HTTP 200, 45,792 B, Last-Modified Sat, 28 Oct 2023 01:06:56 GMT
- GT S3 XmlFiles 202212279349301511 (TAX_PERIOD 202109): HTTP 200, 51,469 B, Last-Modified Sat, 28 Oct 2023 00:26:53 GMT
- GT S3 XmlFiles 202322239349302102 (TAX_PERIOD 202209): HTTP 200, 55,842 B, Last-Modified Sat, 27 Sep 2025 00:37:35 GMT
- GT S3 XmlFiles 202401649349300215 (TAX_PERIOD 202309): HTTP 200, 57,566 B, Last-Modified Tue, 23 Jul 2024 17:01:10 GMT
- GT S3 XmlFiles 202542169349300419 (TAX_PERIOD 202409): HTTP 200, 55,565 B, Last-Modified Sat, 27 Sep 2025 13:54:05 GMT
- GT S3 XmlFiles 202631539349300848 (TAX_PERIOD 202509): HTTP 200, 54,115 B, Last-Modified Tue, 25 Aug 2026 09:26:19 GMT
- GT S3 per-object coverage, random 40 990/EZ/PF rows per IRS index release year: 2021: 40/40, 2022: 40/40, 2023: 40/40, 2024: 40/40, 2025: 40/40, 2026: 26/40
- GT S3 coverage of release 2026 by batch (8 rows each): 01A 8/8, 02A 8/8, 03A 8/8, 04A 8/8, 05A 4/8, 06A 8/8, 07A 8/8, 08A 0/8
- API rate: 12 requests, status {200: 8, 403: 2, 400: 2}, cf-cache-status {'-': 12}, latency median 0.12s p90 0.85s max 0.91s

### 2026-10-10 12:47 — 02_extract_inputs
- text dumps: 29 files in raw/inputs_extracted/text
- raw/inputs_extracted/audit_financials.csv: 1089 rows
- raw/inputs_extracted/audit_tieout_checks.csv: 260 rows
- raw/inputs_extracted/sefa_federal_awards.csv: 4 rows
- raw/inputs_extracted/form990_pdf_financials.csv: 362 rows
- raw/inputs_extracted/form990_pdf_people.csv: 113 rows
- raw/inputs_extracted/form990_pdf_schedule_i.csv: 2 rows
- raw/inputs_extracted/funder_mentions.csv: 200 rows
- raw/inputs_extracted/individual_donor_band_counts.csv: 4 rows
- raw/inputs_extracted/board_lists.csv: 82 rows
- raw/inputs_extracted/annual_report_metrics.csv: 178 rows
- raw/inputs_extracted/crm_funders_2023_2026.csv: 160 rows
- raw/inputs_extracted/strategic_plan_targets.csv: 18 rows
- tie-out checks: 260/260 tie
- SEFA: FY15-Audited-Financial-Statements.pdf: SEFA none
- SEFA: 2016-Audited-Financial-Statements.pdf: SEFA none
- SEFA: 2017-Audited-Financial-Statements-Calvary-Women_s-Services.pdf: SEFA none
- SEFA: CWS-FY18-Audit-.pdf: SEFA none
- SEFA: 2019-Audited-Financial-Statements-CWS.pdf: SEFA none
- SEFA: 2020-Audited-Financial-Statements-CWS.pdf: SEFA none
- SEFA: 2021-Audited-Financial-Statements-CWS.pdf: SEFA none
- SEFA: Calvary-Womens-Services-Inc.-9.30.23-FS.pdf: SEFA 4 programs sum 937,999 vs printed total 937,999
- CRM export: 160 orgs, GIFT_TOTAL $10,556,075.88, 877 gifts, last-gift dates 2023-10-16 to 2026-10-03; 21 rows have NUM_GIFTS=1 but GIFT_TOTAL != LAST_CONTRIB_AMT; GIFT_TOTAL window recorded as unconfirmed
- funder names verified in layout text: 171/171
- note: 2015-Form-990-Calvary-Women_s-Services.pdf: Part I not in text layer (page 1 scanned)
- note: 2016-Form-990-Calvary-Women_s-Services.pdf: Part I not in text layer (page 1 scanned)
- note: 2019-990-Form-990-CWS.pdf: Part I not in text layer (page 1 scanned)

### 2026-10-10 12:48 — 10_probe_filings: remotezip
- 52 ZIP names for 2021-2026 (downloads page + index batch ids); 52 reachable (HTTP 200, Accept-Ranges); not reachable: none
  - 2021: 1 ZIPs, 3.72 GB, 589,904 members, central directories 55.5 MB
  - 2022: 2 ZIPs, 4.01 GB, 656,503 members, central directories 62.6 MB
  - 2023: 12 ZIPs, 4.29 GB, 705,154 members, central directories 65.6 MB
  - 2024: 12 ZIPs, 4.39 GB, 728,719 members, central directories 67.8 MB
  - 2025: 16 ZIPs, 4.46 GB, 748,906 members, central directories 56.2 MB
  - 2026: 9 ZIPs, 2.56 GB, 436,239 members, central directories 32.7 MB
  - 2021_TEOS_XML_01A: 3,715.5 MB, 589,904 members, CD 55.5 MB, Thu, 06 Mar 2025 20:08:25 GMT, page
  - 2022_TEOS_XML_01A: 2,603.7 MB, 433,529 members, CD 41.2 MB, Thu, 06 Mar 2025 20:08:56 GMT, page
  - 2022_TEOS_XML_02A: 1,408.2 MB, 222,974 members, CD 21.4 MB, Thu, 06 Mar 2025 20:06:10 GMT, probe_only
  - 2023_TEOS_XML_01A: 123.1 MB, 21,513 members, CD 2.0 MB, Thu, 06 Mar 2025 17:04:40 GMT, page
  - 2023_TEOS_XML_02A: 234.6 MB, 40,304 members, CD 3.7 MB, Thu, 06 Mar 2025 17:07:26 GMT, page
  - 2023_TEOS_XML_03A: 197.2 MB, 36,224 members, CD 3.4 MB, Thu, 06 Mar 2025 17:06:19 GMT, page
  - 2023_TEOS_XML_04A: 244.5 MB, 42,995 members, CD 4.0 MB, Thu, 06 Mar 2025 17:07:59 GMT, page
  - 2023_TEOS_XML_05A: 990.5 MB, 156,228 members, CD 14.5 MB, Thu, 06 Mar 2025 17:27:59 GMT, page
  - 2023_TEOS_XML_06A: 163.7 MB, 29,240 members, CD 2.7 MB, Thu, 06 Mar 2025 17:05:35 GMT, page
  - 2023_TEOS_XML_07A: 219.9 MB, 38,027 members, CD 3.5 MB, Thu, 06 Mar 2025 17:07:06 GMT, page
  - 2023_TEOS_XML_08A: 266.2 MB, 42,301 members, CD 3.9 MB, Thu, 06 Mar 2025 17:08:23 GMT, page
  - 2023_TEOS_XML_09A: 200.4 MB, 35,070 members, CD 3.3 MB, Thu, 06 Mar 2025 17:06:29 GMT, page
  - 2023_TEOS_XML_10A: 332.5 MB, 56,858 members, CD 5.3 MB, Thu, 06 Mar 2025 17:10:21 GMT, page
  - 2023_TEOS_XML_11A: 1,200.3 MB, 186,387 members, CD 17.3 MB, Thu, 06 Mar 2025 17:32:53 GMT, page
  - 2023_TEOS_XML_12A: 120.7 MB, 20,007 members, CD 1.9 MB, Thu, 06 Mar 2025 17:04:34 GMT, page
  - 2024_TEOS_XML_01A: 104.8 MB, 17,246 members, CD 1.6 MB, Thu, 06 Mar 2025 14:04:31 GMT, page
  - 2024_TEOS_XML_02A: 243.7 MB, 40,284 members, CD 3.7 MB, Thu, 06 Mar 2025 14:04:23 GMT, page
  - 2024_TEOS_XML_03A: 209.3 MB, 38,418 members, CD 3.6 MB, Thu, 06 Mar 2025 14:04:55 GMT, page
  - 2024_TEOS_XML_04A: 350.3 MB, 59,487 members, CD 5.5 MB, Thu, 06 Mar 2025 14:05:02 GMT, page
  - 2024_TEOS_XML_05A: 977.5 MB, 156,237 members, CD 14.5 MB, Thu, 06 Mar 2025 14:05:40 GMT, page
  - 2024_TEOS_XML_06A: 163.9 MB, 29,408 members, CD 2.7 MB, Thu, 06 Mar 2025 14:04:01 GMT, page
  - 2024_TEOS_XML_07A: 288.3 MB, 50,144 members, CD 4.7 MB, Thu, 06 Mar 2025 14:04:23 GMT, page
  - 2024_TEOS_XML_08A: 260.6 MB, 41,687 members, CD 3.9 MB, Thu, 06 Mar 2025 14:04:56 GMT, page
  - 2024_TEOS_XML_09A: 247.0 MB, 44,108 members, CD 4.1 MB, Thu, 06 Mar 2025 14:04:54 GMT, page
  - 2024_TEOS_XML_10A: 251.6 MB, 43,392 members, CD 4.0 MB, Thu, 06 Mar 2025 14:04:55 GMT, page
  - 2024_TEOS_XML_11A: 1,165.6 MB, 186,632 members, CD 17.4 MB, Thu, 06 Mar 2025 14:05:48 GMT, page
  - 2024_TEOS_XML_12A: 128.3 MB, 21,676 members, CD 2.0 MB, Thu, 06 Mar 2025 14:04:05 GMT, page
  - 2025_TEOS_XML_01A: 103.7 MB, 17,044 members, CD 1.3 MB, Wed, 05 Mar 2025 15:12:42 GMT, page
  - 2025_TEOS_XML_02A: 239.9 MB, 41,855 members, CD 3.1 MB, Wed, 19 Mar 2025 13:01:47 GMT, page
  - 2025_TEOS_XML_03A: 222.6 MB, 41,570 members, CD 3.1 MB, Wed, 16 Apr 2025 13:01:48 GMT, page
  - 2025_TEOS_XML_04A: 338.2 MB, 57,595 members, CD 4.3 MB, Wed, 21 May 2025 13:09:56 GMT, page
  - 2025_TEOS_XML_05A: 495.9 MB, 81,770 members, CD 6.1 MB, Wed, 25 Jun 2025 13:13:15 GMT, page
  - 2025_TEOS_XML_05B: 501.0 MB, 81,770 members, CD 6.1 MB, Wed, 25 Jun 2025 13:13:33 GMT, page
  - 2025_TEOS_XML_06A: 246.8 MB, 44,824 members, CD 3.4 MB, Wed, 20 Aug 2025 13:11:59 GMT, page
  - 2025_TEOS_XML_07A: 143.5 MB, 24,854 members, CD 1.9 MB, Wed, 20 Aug 2025 13:08:44 GMT, page
  - 2025_TEOS_XML_08A: 262.7 MB, 42,291 members, CD 3.2 MB, Wed, 17 Sep 2025 13:18:06 GMT, page
  - 2025_TEOS_XML_09A: 256.3 MB, 45,643 members, CD 3.4 MB, Wed, 19 Nov 2025 20:41:59 GMT, page
  - 2025_TEOS_XML_10A: 56.5 MB, 9,836 members, CD 0.7 MB, Wed, 19 Nov 2025 14:08:07 GMT, page
  - 2025_TEOS_XML_11A: 340.1 MB, 55,488 members, CD 4.2 MB, Wed, 17 Dec 2025 14:31:07 GMT, page
  - 2025_TEOS_XML_11B: 494.5 MB, 80,283 members, CD 6.0 MB, Wed, 17 Dec 2025 14:43:04 GMT, page
  - 2025_TEOS_XML_11C: 277.9 MB, 44,896 members, CD 3.4 MB, Wed, 17 Dec 2025 14:25:37 GMT, page
  - 2025_TEOS_XML_11D: 332.8 MB, 53,800 members, CD 4.0 MB, Wed, 17 Dec 2025 17:10:02 GMT, page
  - 2025_TEOS_XML_12A: 151.8 MB, 25,387 members, CD 1.9 MB, Wed, 21 Jan 2026 14:14:30 GMT, page
  - 2026_TEOS_XML_01A: 71.5 MB, 12,245 members, CD 0.9 MB, Thu, 19 Feb 2026 18:32:24 GMT, page
  - 2026_TEOS_XML_02A: 222.1 MB, 38,719 members, CD 2.9 MB, Wed, 18 Mar 2026 13:02:56 GMT, page
  - 2026_TEOS_XML_03A: 259.3 MB, 48,471 members, CD 3.6 MB, Wed, 15 Apr 2026 13:03:42 GMT, page
  - 2026_TEOS_XML_04A: 261.9 MB, 47,627 members, CD 3.6 MB, Wed, 20 May 2026 13:02:32 GMT, page
  - 2026_TEOS_XML_05A: 521.2 MB, 84,172 members, CD 6.3 MB, Wed, 17 Jun 2026 13:13:47 GMT, page
  - 2026_TEOS_XML_05B: 513.4 MB, 84,172 members, CD 6.3 MB, Wed, 17 Jun 2026 13:13:52 GMT, page
  - 2026_TEOS_XML_06A: 210.8 MB, 38,244 members, CD 2.9 MB, Wed, 15 Jul 2026 16:01:18 GMT, page
  - 2026_TEOS_XML_07A: 189.2 MB, 32,240 members, CD 2.4 MB, Wed, 19 Aug 2026 13:00:50 GMT, page
  - 2026_TEOS_XML_08A: 314.7 MB, 50,349 members, CD 3.8 MB, Wed, 16 Sep 2026 13:02:45 GMT, index_only
  - release 2021: index rows 589,904 vs ZIP members 589,904 (diff +0)
  - release 2022: index rows 656,503 vs ZIP members 656,503 (diff +0)
  - release 2023: index rows 705,156 vs ZIP members 705,154 (diff -2)
  - release 2024: index rows 728,719 vs ZIP members 728,719 (diff +0)
  - release 2025: index rows 748,906 vs ZIP members 748,906 (diff +0)
  - release 2026: index rows 436,239 vs ZIP members 436,239 (diff +0)
  - 2025_TEOS_XML_05A vs 2025_TEOS_XML_05B: 81,770 / 81,770 object ids, overlap 0; index rows labelled 2025_TEOS_XML_05A: 163,540, found in 2025_TEOS_XML_05A 81,770, in 2025_TEOS_XML_05B 81,770 (read 12.4 MB of central directory)
    - GT S3 per-object presence, 10 members each: 05A 10/10, 05B 10/10
  - 2026_TEOS_XML_05A vs 2026_TEOS_XML_05B: 84,172 / 84,172 object ids, overlap 0; index rows labelled 2026_TEOS_XML_05A: 168,344, found in 2026_TEOS_XML_05A 84,172, in 2026_TEOS_XML_05B 84,172 (read 12.8 MB of central directory)
    - GT S3 per-object presence, 10 members each: 05A 10/10, 05B 0/10
- remotezip 2026_TEOS_XML_06A (210.8 MB, 38,244 members, names like 202601429339300000_public.xml): central directory 2 requests / 2.9 MB; member 202631539349300848_public.xml 54,115 B (10,872 B compressed); total 3 requests / 2.9 MB = 1.40% of the ZIP; 0.3s -> raw/xml/irs/20261010T122754_521307706_TY2024_2026_TEOS_XML_06A_202631539349300848_public.xml
- 2026_TEOS_XML_06A: mean member 28.7 KB uncompressed, compression ratio 5.3x
- GT S3 copy of 202631539349300848 byte-identical to the IRS ZIP member: True
- Calvary TY2021 202322239349302102 (release 2023, no batch id; DLN day -> month 08): found in 2023_TEOS_XML_08A after reading 1 central directories (4.0 MB)

### 2026-10-10 12:48 — 12_probe_federal: sam
- Assistance Listings extract: 2871 active listings, 38 columns (raw/sam/20261010T123845_AssistanceListings_DataGov_PUBLIC_CURRENT.csv)
- target CFDAs missing from active extract: ['21.019', '14.235']
- sgs cfda search http 200 hits 4; sgs ei result types {'exclusion': 10} (Calvary UEI found: False)
- api.sam.gov without key: {'entity_v3': 404, 'assistance_listings_v1': 404}

### 2026-10-10 12:48 — 12_probe_federal: catalog
- wrote sources/catalog_parts/federal.csv; sections run: ['sam']

### 2026-10-10 12:48 — 02_extract_inputs
- text dumps: 29 files in raw/inputs_extracted/text
- raw/inputs_extracted/audit_financials.csv: 1089 rows
- raw/inputs_extracted/audit_tieout_checks.csv: 260 rows
- raw/inputs_extracted/sefa_federal_awards.csv: 4 rows
- raw/inputs_extracted/form990_pdf_financials.csv: 362 rows
- raw/inputs_extracted/form990_pdf_people.csv: 113 rows
- raw/inputs_extracted/form990_pdf_schedule_i.csv: 2 rows
- raw/inputs_extracted/funder_mentions.csv: 200 rows
- raw/inputs_extracted/individual_donor_band_counts.csv: 4 rows
- raw/inputs_extracted/board_lists.csv: 82 rows
- raw/inputs_extracted/annual_report_metrics.csv: 178 rows
- raw/inputs_extracted/crm_funders_2023_2026.csv: 160 rows
- raw/inputs_extracted/strategic_plan_targets.csv: 18 rows
- tie-out checks: 260/260 tie
- SEFA: FY15-Audited-Financial-Statements.pdf: SEFA none
- SEFA: 2016-Audited-Financial-Statements.pdf: SEFA none
- SEFA: 2017-Audited-Financial-Statements-Calvary-Women_s-Services.pdf: SEFA none
- SEFA: CWS-FY18-Audit-.pdf: SEFA none
- SEFA: 2019-Audited-Financial-Statements-CWS.pdf: SEFA none
- SEFA: 2020-Audited-Financial-Statements-CWS.pdf: SEFA none
- SEFA: 2021-Audited-Financial-Statements-CWS.pdf: SEFA none
- SEFA: Calvary-Womens-Services-Inc.-9.30.23-FS.pdf: SEFA 4 programs sum 937,999 vs printed total 937,999
- CRM export: 160 orgs, GIFT_TOTAL $10,556,075.88, 877 gifts, last-gift dates 2023-10-16 to 2026-10-03; 21 rows have NUM_GIFTS=1 but GIFT_TOTAL != LAST_CONTRIB_AMT; GIFT_TOTAL window recorded as unconfirmed
- funder names verified in layout text: 171/171
- note: 2015-Form-990-Calvary-Women_s-Services.pdf: Part I not in text layer (page 1 scanned)
- note: 2016-Form-990-Calvary-Women_s-Services.pdf: Part I not in text layer (page 1 scanned)
- note: 2019-990-Form-990-CWS.pdf: Part I not in text layer (page 1 scanned)

### 2026-10-10 12:49 — 10_probe_filings: volume
- BMF sets: (a) DMV PF filers (FOUNDATION 02/03/04 or PF_FILING_REQ_CD=1) 5,855 EINs; (b) DC 501(c)(3) public charities in NTEE L/P/F/I/J/W 1,750 EINs
- (a: DMV 990-PF filers) 25,367 returns from 5,249 EINs; by type {'990PF': 25367}; by tax year {2018: 22, 2019: 397, 2020: 3884, 2021: 4256, 2022: 4527, 2023: 4835, 2024: 4912, 2025: 2534}; by release year {2021: 3679, 2022: 4169, 2023: 4553, 2024: 4872, 2025: 5068, 2026: 3026}; same EIN+period+type repeats (amended/superseded) 213
  - after keeping the latest OBJECT_ID per EIN+TAX_PERIOD+type: 25,154 returns; TY2020-TY2024 22,210
  - ZIP batches: 52 distinct ZIPs touched (2021_TEOS_XML_01A 3679, 2022_ANY 4169, 2023_ANY 4553, 2024_TEOS_XML_01A 72, 2024_TEOS_XML_02A 185, 2024_TEOS_XML_03A 195, 2024_TEOS_XML_04A 386, 2024_TEOS_XML_05A 1326, 2024_TEOS_XML_06A 182, 2024_TEOS_XML_07A 256, 2024_TEOS_XML_08A 258, 2024_TEOS_XML_09A 260, 2024_TEOS_XML_10A 240, 2024_TEOS_XML_11A 1407, 2024_TEOS_XML_12A 105, 2025_TEOS_XML_01A 69, 2025_TEOS_XML_02A 185, 2025_TEOS_XML_03A 274, 2025_TEOS_XML_04A 417, 2025_TEOS_XML_05* 1363, 2025_TEOS_XML_06A 283, 2025_TEOS_XML_07A 131, 2025_TEOS_XML_08A 186, 2025_TEOS_XML_09A 307, 2025_TEOS_XML_10A 43, 2025_TEOS_XML_11A 383, 2025_TEOS_XML_11B 568, 2025_TEOS_XML_11C 330, 2025_TEOS_XML_11D 416, 2025_TEOS_XML_12A 113, 2026_TEOS_XML_01A 42, 2026_TEOS_XML_02A 198, 2026_TEOS_XML_03A 327, 2026_TEOS_XML_04A 384, 2026_TEOS_XML_05* 1392, 2026_TEOS_XML_06A 219, 2026_TEOS_XML_07A 194, 2026_TEOS_XML_08A 270)
  - bytes: full ZIP downloads 23.4 GB; remotezip ~491 MB (central directories 340.3 MB + members ~151.1 MB compressed); GT S3 per-object ~805.3 MB uncompressed
- (b: DC public charities L/P/F/I/J/W) 4,580 returns from 968 EINs; by type {'990EZ': 670, '990': 3907, '990PF': 3}; by tax year {2018: 5, 2019: 215, 2020: 731, 2021: 812, 2022: 826, 2023: 883, 2024: 885, 2025: 223}; by release year {2021: 712, 2022: 783, 2023: 832, 2024: 874, 2025: 899, 2026: 480}; same EIN+period+type repeats (amended/superseded) 114
  - after keeping the latest OBJECT_ID per EIN+TAX_PERIOD+type: 4,466 returns; TY2020-TY2024 4,032
  - ZIP batches: 52 distinct ZIPs touched (2021_TEOS_XML_01A 712, 2022_ANY 783, 2023_ANY 832, 2024_TEOS_XML_01A 16, 2024_TEOS_XML_02A 26, 2024_TEOS_XML_03A 39, 2024_TEOS_XML_04A 60, 2024_TEOS_XML_05A 133, 2024_TEOS_XML_06A 47, 2024_TEOS_XML_07A 45, 2024_TEOS_XML_08A 78, 2024_TEOS_XML_09A 50, 2024_TEOS_XML_10A 63, 2024_TEOS_XML_11A 299, 2024_TEOS_XML_12A 18, 2025_TEOS_XML_01A 12, 2025_TEOS_XML_02A 38, 2025_TEOS_XML_03A 30, 2025_TEOS_XML_04A 56, 2025_TEOS_XML_05* 142, 2025_TEOS_XML_06A 46, 2025_TEOS_XML_07A 28, 2025_TEOS_XML_08A 90, 2025_TEOS_XML_09A 53, 2025_TEOS_XML_10A 15, 2025_TEOS_XML_11A 91, 2025_TEOS_XML_11B 114, 2025_TEOS_XML_11C 85, 2025_TEOS_XML_11D 78, 2025_TEOS_XML_12A 21, 2026_TEOS_XML_01A 14, 2026_TEOS_XML_02A 34, 2026_TEOS_XML_03A 46, 2026_TEOS_XML_04A 54, 2026_TEOS_XML_05* 130, 2026_TEOS_XML_06A 51, 2026_TEOS_XML_07A 59, 2026_TEOS_XML_08A 92)
  - bytes: full ZIP downloads 23.4 GB; remotezip ~368 MB (central directories 340.3 MB + members ~27.3 MB compressed); GT S3 per-object ~145.5 MB uncompressed

### 2026-10-10 12:49 — 01_inventory_inputs
- sources/input_inventory.csv: 30 rows (duplicate=1, ok=24, partial=4, unreadable=1)
- registered 30 input_* sources
- period checks: all match

### 2026-10-10 12:49 — 10/11 filings recon: summary
- Catalog part: sources/catalog_parts/filings.csv (15 rows) + filings.md
- XML parsing decision: hand-written namespace-stripped lxml (one code path 2014v6.0-2024v5.5); concordance as dictionary; IRSx 0.5.1 as optional QC cross-check
- XML acquisition: GT S3 per-object primary; IRS remotezip fallback for 2026_TEOS_XML_05B and 08A members
- Volume: (a) DMV 990-PF 25,367 returns (22,210 TY2020-TY2024 after dedupe), (b) DC PC L/P/F/I/J/W 4,580 returns; remotezip ~0.5 GB vs full ZIPs 23.4 GB vs GT S3 ~1 GB
- raw/ added ~896 MB; no new packages in the project venv

### 2026-10-10 12:49 — 02_extract_inputs
- text dumps: 29 files in raw/inputs_extracted/text
- raw/inputs_extracted/audit_financials.csv: 1089 rows
- raw/inputs_extracted/audit_tieout_checks.csv: 260 rows
- raw/inputs_extracted/sefa_federal_awards.csv: 4 rows
- raw/inputs_extracted/form990_pdf_financials.csv: 362 rows
- raw/inputs_extracted/form990_pdf_people.csv: 113 rows
- raw/inputs_extracted/form990_pdf_schedule_i.csv: 2 rows
- raw/inputs_extracted/funder_mentions.csv: 200 rows
- raw/inputs_extracted/individual_donor_band_counts.csv: 4 rows
- raw/inputs_extracted/board_lists.csv: 82 rows
- raw/inputs_extracted/annual_report_metrics.csv: 178 rows
- raw/inputs_extracted/crm_funders_2023_2026.csv: 160 rows
- raw/inputs_extracted/strategic_plan_targets.csv: 18 rows
- tie-out checks: 260/260 tie
- SEFA: FY15-Audited-Financial-Statements.pdf: SEFA none
- SEFA: 2016-Audited-Financial-Statements.pdf: SEFA none
- SEFA: 2017-Audited-Financial-Statements-Calvary-Women_s-Services.pdf: SEFA none
- SEFA: CWS-FY18-Audit-.pdf: SEFA none
- SEFA: 2019-Audited-Financial-Statements-CWS.pdf: SEFA none
- SEFA: 2020-Audited-Financial-Statements-CWS.pdf: SEFA none
- SEFA: 2021-Audited-Financial-Statements-CWS.pdf: SEFA none
- SEFA: Calvary-Womens-Services-Inc.-9.30.23-FS.pdf: SEFA 4 programs sum 937,999 vs printed total 937,999
- CRM export: 160 orgs, GIFT_TOTAL $10,556,075.88, 877 gifts, last-gift dates 2023-10-16 to 2026-10-03; 21 rows have NUM_GIFTS=1 but GIFT_TOTAL != LAST_CONTRIB_AMT; GIFT_TOTAL window recorded as unconfirmed
- funder names verified in layout text: 171/171
- note: 2015-Form-990-Calvary-Women_s-Services.pdf: Part I not in text layer (page 1 scanned)
- note: 2016-Form-990-Calvary-Women_s-Services.pdf: Part I not in text layer (page 1 scanned)
- note: 2019-990-Form-990-CWS.pdf: Part I not in text layer (page 1 scanned)

### 2026-10-10 12:50 — 01_inventory_inputs
- sources/input_inventory.csv: 30 rows (duplicate=1, ok=24, partial=4, unreadable=1)
- registered 30 input_* sources
- period checks: all match

### 2026-10-10 12:50 — 02_extract_inputs
- text dumps: 29 files in raw/inputs_extracted/text
- raw/inputs_extracted/audit_financials.csv: 1089 rows
- raw/inputs_extracted/audit_tieout_checks.csv: 260 rows
- raw/inputs_extracted/sefa_federal_awards.csv: 4 rows
- raw/inputs_extracted/form990_pdf_financials.csv: 362 rows
- raw/inputs_extracted/form990_pdf_people.csv: 113 rows
- raw/inputs_extracted/form990_pdf_schedule_i.csv: 2 rows
- raw/inputs_extracted/funder_mentions.csv: 200 rows
- raw/inputs_extracted/individual_donor_band_counts.csv: 4 rows
- raw/inputs_extracted/board_lists.csv: 82 rows
- raw/inputs_extracted/annual_report_metrics.csv: 178 rows
- raw/inputs_extracted/crm_funders_2023_2026.csv: 160 rows
- raw/inputs_extracted/strategic_plan_targets.csv: 18 rows
- tie-out checks: 260/260 tie
- SEFA: FY15-Audited-Financial-Statements.pdf: SEFA none
- SEFA: 2016-Audited-Financial-Statements.pdf: SEFA none
- SEFA: 2017-Audited-Financial-Statements-Calvary-Women_s-Services.pdf: SEFA none
- SEFA: CWS-FY18-Audit-.pdf: SEFA none
- SEFA: 2019-Audited-Financial-Statements-CWS.pdf: SEFA none
- SEFA: 2020-Audited-Financial-Statements-CWS.pdf: SEFA none
- SEFA: 2021-Audited-Financial-Statements-CWS.pdf: SEFA none
- SEFA: Calvary-Womens-Services-Inc.-9.30.23-FS.pdf: SEFA 4 programs sum 937,999 vs printed total 937,999
- CRM export: 160 orgs, GIFT_TOTAL $10,556,075.88, 877 gifts, last-gift dates 2023-10-16 to 2026-10-03; 21 rows have NUM_GIFTS=1 but GIFT_TOTAL != LAST_CONTRIB_AMT; GIFT_TOTAL window recorded as unconfirmed
- funder names verified in layout text: 171/171
- note: 2015-Form-990-Calvary-Women_s-Services.pdf: Part I not in text layer (page 1 scanned)
- note: 2016-Form-990-Calvary-Women_s-Services.pdf: Part I not in text layer (page 1 scanned)
- note: 2019-990-Form-990-CWS.pdf: Part I not in text layer (page 1 scanned)

### 2026-10-10 12:51 — 16_probe_context: geocode
- MAR 2 API: ok (HTTP 200)
- DC GIS Address Points: 1217 MARION BARRY AVENUE SE: Ward 8, SMD 8A06, ANC 8A, lat 38.86708202, lon -76.98804548, MAR_ID 338288; no tract field
- Census Geocoder single: 3/4 matched; batch: 3/4 matched; calvary_new_name: no match | calvary_old_name: county 11001, tract 11001007503, SLDU Ward 8 | md_shepherds_table: county 24031, tract 24031702501, SLDU State Senate District 20 | va_carpenters_shelter: county 51510, tract 51510201602, SLDU State Senate District 39

### 2026-10-10 12:51 — 16_probe_context: catalog
- wrote sources/catalog_parts/context.csv
- statuses: mar2=ok, addrpts=ok, geocoder=ok

### 2026-10-10 12:51 — 19_merge_catalog
- api_catalog.csv: 65 rows; status {'ok': 55, 'ok_no_results': 4, 'blocked_needs_key': 3, 'not_applicable': 2, 'failed': 1}

### 2026-10-10 12:51 — 12_probe_federal: sam
- Assistance Listings extract: 2871 active listings, 38 columns (raw/sam/20261010T123845_AssistanceListings_DataGov_PUBLIC_CURRENT.csv)
- target CFDAs missing from active extract: ['21.019', '14.235']
- sgs cfda search http 200 hits 4; sgs ei result types {'exclusion': 10} (Calvary UEI found: False)
- api.sam.gov without key: {'entity_v3': 404, 'assistance_listings_v1': 404}

### 2026-10-10 12:51 — 12_probe_federal: catalog
- wrote sources/catalog_parts/federal.csv; sections run: ['sam']

### 2026-10-10 12:54 — 12_probe_federal: fac
- Calvary reports: 2 (audit years [2022, 2023]); additional_eins hits 0
  - 2022-09-CENSUS-0000258136 FYE 2022-09-30 total $4,067,718; awards [('21.027', 3583885, 'N'), ('14.235', 415830, 'N'), ('97.024', 48889, 'N'), ('10.561', 19114, 'N')]; passthrough {'AWARD-00001': 'DISTRICT OF COLUMBIA OFFICE OF VICTIM SERVICES AND JUSTICE GRANTS', 'AWARD-00002': 'THE COMMUNITY PARTNERSHIP', 'AWARD-00003': 'FEDERAL EMERGENCY MANAGEMENT AGENCY', 'AWARD-00004': 'DISTRICT OF COLUMBIA DEPARTMENT OF HUMAN SERVICES'}; children {'federal_awards': 4, 'passthrough': 4, 'findings': 0, 'findings_text': 0, 'notes_to_sefa': 1, 'secondary_auditors': 0, 'additional_eins': 0, 'additional_ueis': 0, 'corrective_action_plans': 0}
  - 2023-09-GSAFAC-0000037691 FYE 2023-09-30 total $4,064,718; awards [('21.027', 3583885, 'N'), ('14.235', 415830, 'N'), ('97.024', 45889, 'N'), ('10.561', 19114, 'N')]; passthrough {'AWARD-00001': 'District of Columbia Office of Victim Services and Justice Grants', 'AWARD-00002': 'The Community Partnership', 'AWARD-00003': 'Federal Emergency Management Agency', 'AWARD-00004': 'District of Columbia Department of Human Services'}; children {'federal_awards': 4, 'passthrough': 4, 'findings': 0, 'findings_text': 0, 'notes_to_sefa': 3, 'secondary_auditors': 0, 'additional_eins': 0, 'additional_ueis': 0, 'corrective_action_plans': 0}
- DC auditees by audit_year: {"2016": {"audits": 391, "nonprofit": 371, "expended": 13206882145}, "2017": {"audits": 384, "nonprofit": 367, "expended": 13979710795}, "2018": {"audits": 402, "nonprofit": 383, "expended": 13021048914}, "2019": {"audits": 398, "nonprofit": 381, "expended": 14451399643}, "2020": {"audits": 387, "nonprofit": 368, "expended": 17308664616}, "2021": {"audits": 409, "nonprofit": 394, "expended": 20391585672}, "2022": {"audits": 466, "nonprofit": 437, "expended": 20085076799}, "2023": {"audits": 477, "nonprofit": 457, "expended": 20989240408}, "2024": {"audits": 467, "nonprofit": 451, "expended": 20678342419}, "2025": {"audits": 359, "nonprofit": 342, "expended": 25753007771}, "2026": {"audits": 1, "nonprofit": 1, "expended": 42466823}}
- DC 2023 SEFA: {"federal_awards_rows": 9602, "indirect_rows": 3614, "target_cfda_rows": 486, "target_cfda_indirect_rows": 256, "target_cfda_auditees": 111, "passthrough_rows": 3614, "top_passthrough_names": [["DISTRICT OF COLUMBIA OFFICE OF THE STATE SUPERINTENDENT OF EDUCATION", 341], ["MARYLAND STATE DEPARTMENT OF EDUCATION", 90], ["CONSORTIUM FOR ELECTIONS AND POLITICAL PROCESS STRENGTHENING", 62], ["DC OFFICE OF THE STATE SUPERINTENDENT OF EDUCATION", 60], ["SPACE TELESCOPE SCIENCE INSTITUTE", 57], ["D.C OFFICE OF STATE SUPERINTENDENT OF EDUCATION", 53], ["GEORGE WASHINGTON UNIVERSITY", 52], ["CONSORTIUM FOR ELECTIONS AND POLICAL STRENGTHENING", 50], ["NATIONAL ENDOWMENT FOR DEMOCRACY", 46], ["DISTRICT OF COLUMBIA DEPARTMENT OF HEALTH", 42], ["DC DEPARTMENT OF HEALTH", 42], ["FREEDOM HOUSE", 39]]}
- OVSJG pass-through rows: {"rows": 75, "by_year": {"2016": 4, "2017": 3, "2018": 2, "2019": 2, "2020": 4, "2021": 7, "2022": 13, "2023": 18, "2024": 13, "2025": 9}, "reports": 43}
- passthrough_name counts, all auditee states: {"*district of columbia*": 5224, "*DC Department*": 716, "*community partnership*": 919}

### 2026-10-10 12:54 — 12_probe_federal: catalog
- wrote sources/catalog_parts/federal.csv; sections run: ['fac']

### 2026-10-10 12:55 — lead: assumptions register
User direction (2026-10-10): work with the data we have and make reasonable, documented assumptions instead of waiting on confirmations.

- **A1. CRM GIFT_TOTAL window.** Treated as the CRM's cumulative total for the export, with the window unconfirmed.
  - LAST_CONTRIB_AMT and LAST_CONTRIB_DATE are single-gift facts: confidence=high.
  - GIFT_TOTAL: confidence=medium. For the 21 rows where NUM_GIFTS=1 but GIFT_TOTAL > LAST_CONTRIB_AMT, confidence=low (possible pre-window gifts or pledge installments).
  - The funder 990-PF cross-check in Phase 4 will refine this.
- **A2. Cash vs in-kind in the CRM.** Assumed cash unless contradicted (foundation 990-PF match, Calvary Schedule M noncash totals, web evidence). Each row is flagged `cash_verified`.
- **A3. Missing audits (FY22, FY24, FY25).** Not available from the user. Fallbacks:
  - FAC single-audit records (SEFA by year).
  - Audits posted on calvaryservices.org/financials, fetched in Phase 4.
  - 990 XML Part VIII for the government-grant totals.
- **A4. "At a Glance 2024" PDF.** Treated as FY24 (Oct 2023–Sep 2024), confidence=medium. This matches the FY23 flyer's "AT A GLANCE | 2023" naming.
- **A5. Calvary's single audit status for FY21/FY22.** Taken from FAC records if present; otherwise recorded as unknown.

### 2026-10-10 12:55 — 12_probe_federal: wrap-up
- Catalog part written: sources/catalog_parts/federal.csv (7 rows) + federal.md (with Phase 4 pull design)
- Sources registered: api_usaspending, bulk_usaspending, api_fac, api_grantsgov, bulk_sam_assistance_listings, api_sam_sgs, bulk_treasury_slfrf
- Decision: the DC prime probe excludes 59.073 (PPP; 32,800 DC loans). Treasury SLFRF files were added because SLFRF subawards are missing from USAspending.
- Notes and open questions appended under "Federal recon".

### 2026-10-10 12:56 — 19_merge_catalog
- api_catalog.csv: 65 rows; status {'ok': 55, 'ok_no_results': 4, 'blocked_needs_key': 3, 'not_applicable': 2, 'failed': 1}

### 2026-10-10 13:05 — 20_build_universes
- calvary: 1 EINs
- daf_sponsors: 14 EINs
- dc_sector: 1,024 EINs
- dmv_funders: 7,705 EINs
- dmv_sector: 4,686 EINs
- national_women: 2,452 EINs
- size_matched: 557 EINs
- membership rows 16,439; distinct EINs 15,123; e-file rows 44,108; size band $2,483,998–$9,935,990; missing pins {'F3': [], 'DAF1': ['141782466']}

### 2026-10-10 13:06 — 20_build_universes
- calvary: 1 EINs
- daf_sponsors: 15 EINs
- dc_sector: 1,024 EINs
- dmv_funders: 7,705 EINs
- dmv_sector: 4,890 EINs
- national_women: 2,452 EINs
- size_matched: 557 EINs
- membership rows 16,644; distinct EINs 15,320; e-file rows 44,511; size band $2,483,998–$9,935,990; missing pins {'F3': [], 'DAF1': []}

### 2026-10-10 13:10 — 21_core_peer_candidates
- candidates 68 (seeds matched 15, data-driven 53); seeds not found: N Street Village, House of Ruth (DC), My Sister's Place, DC SAFE, Thrive DC, So Others Might Eat (SOME), Community of Hope, Jubilee Housing, Coalition for the Homeless / Housing Up, Bright Beginnings, Covenant House DC, Sasha Bruce Youthwork, New Hope Ministries, Mary's Center, Life Deeds, Doorways for Women and Families, House of Ruth Maryland, Mission of Love / Shepherd's Table, Interfaith Works, Community Crisis Services / Family Crisis Center PG, Women Who Care Ministries; XML ok 53; wards 35

### 2026-10-10 13:10 — 21_core_peer_candidates
- candidates 82 (seeds matched 29, data-driven 53); seeds not found: House of Ruth (DC), DC SAFE, So Others Might Eat (SOME), Community of Hope, New Hope Ministries, Life Deeds, House of Ruth Maryland; XML ok 65; wards 44

### 2026-10-10 13:12 — 21_core_peer_candidates
- candidates 82 (seeds matched 29, data-driven 53); seeds not found: House of Ruth (DC), DC SAFE, So Others Might Eat (SOME), Community of Hope, New Hope Ministries, Life Deeds, House of Ruth Maryland; XML ok 82; wards 44

### 2026-10-10 13:13 — 21_core_peer_candidates
- candidates 86 (seeds matched 35, data-driven 51); seeds not found: New Hope Ministries (DC); XML ok 86; wards 46

### 2026-10-10 13:14 — 20_build_universes
- calvary: 1 EINs
- core_peers: 18 EINs
- daf_sponsors: 15 EINs
- dc_sector: 1,024 EINs
- dmv_funders: 7,705 EINs
- dmv_sector: 4,890 EINs
- national_women: 2,452 EINs
- size_matched: 557 EINs
- membership rows 16,662; distinct EINs 15,327; e-file rows 44,547; size band $2,483,998–$9,935,990; missing pins {'F3': [], 'DAF1': []}

### 2026-10-10 13:17 — 22_match_known_funders
- names 243; outcomes {('corp_foundation', 'inferred'): 21, ('exact_name_state', 'yes'): 33, ('exact_name_unique', 'yes'): 22, ('fuzzy_name_state', 'yes'): 11, ('unmatched', 'no'): 156}; accepted EINs 85

### 2026-10-10 13:18 — 41_pull_soi_extracts: download
- downloaded 12eofinextract990.zip -> raw/irs_soi/20261010T131751_12eofinextract990.zip (17.9 MB, sha256 dad53ede773f)
- downloaded 12eofinextract990ez.zip -> raw/irs_soi/20261010T131752_12eofinextract990ez.zip (9.3 MB, sha256 8d38d3d03b00)
- downloaded 12eofinextract990pf.zip -> raw/irs_soi/20261010T131752_12eofinextract990pf.zip (8.8 MB, sha256 1927c4ab45d8)
- downloaded 12eofinextractdoc.xls -> raw/irs_soi/20261010T131753_12eofinextractdoc.xls (0.1 MB, sha256 6aee7670b5a3)
- downloaded 13eofinextract990.zip -> raw/irs_soi/20261010T131753_13eofinextract990.zip (47.3 MB, sha256 9c41a1367161)
- downloaded 13eofinextract990ez.zip -> raw/irs_soi/20261010T131756_13eofinextract990ez.zip (11.1 MB, sha256 64e0ff8a301a)
- downloaded 13eofinextract990pf.zip -> raw/irs_soi/20261010T131756_13eofinextract990pf.zip (10.8 MB, sha256 e4c5ca353588)
- downloaded 13eofinextractdoc.xls -> raw/irs_soi/20261010T131757_13eofinextractdoc.xls (0.1 MB, sha256 131860d6b548)
- downloaded 14eofinextract990.zip -> raw/irs_soi/20261010T131757_14eofinextract990.zip (48.5 MB, sha256 68e01c5ce64e)
- downloaded 14eofinextract990ez.zip -> raw/irs_soi/20261010T131759_14eofinextract990ez.zip (11.7 MB, sha256 a105ad883534)
- downloaded 14eofinextract990pf.zip -> raw/irs_soi/20261010T131759_14eofinextract990pf.zip (11.0 MB, sha256 4ad82393e771)
- downloaded 14eofinextractdoc.xls -> raw/irs_soi/20261010T131759_14eofinextractdoc.xls (0.1 MB, sha256 09ce46e30537)
- downloaded 15eofinextract990.zip -> raw/irs_soi/20261010T131800_15eofinextract990.zip (48.4 MB, sha256 fde32b89d638)
- downloaded 15eofinextract990pf.zip -> raw/irs_soi/20261010T131802_15eofinextract990pf.zip (11.3 MB, sha256 64201b4797e1)
- downloaded 15eofinextractEZ.zip -> raw/irs_soi/20261010T131802_15eofinextractEZ.zip (11.0 MB, sha256 3eecdc5a45ac)
- downloaded 15eofinextractdoc.xls -> raw/irs_soi/20261010T131803_15eofinextractdoc.xls (0.1 MB, sha256 56443eb91184)
- downloaded 16eofinextract990.zip -> raw/irs_soi/20261010T131803_16eofinextract990.zip (50.7 MB, sha256 bf6744aa0f76)
- downloaded 16eofinextract990pf.zip -> raw/irs_soi/20261010T131805_16eofinextract990pf.zip (11.6 MB, sha256 796ebfe65859)
- downloaded 16eofinextractdoc.xls -> raw/irs_soi/20261010T131806_16eofinextractdoc.xls (0.1 MB, sha256 1b2f79c2be40)
- downloaded 16eofinextractez.zip -> raw/irs_soi/20261010T131806_16eofinextractez.zip (11.6 MB, sha256 21e625e0abc9)
- downloaded 17eofinextract990.zip -> raw/irs_soi/20261010T131807_17eofinextract990.zip (49.8 MB, sha256 fef92bfd9227)
- downloaded 17eofinextractEZ.zip -> raw/irs_soi/20261010T131810_17eofinextractEZ.zip (11.1 MB, sha256 61de50a2bd7e)
- downloaded 17eofinextractdoc.xls -> raw/irs_soi/20261010T131811_17eofinextractdoc.xls (0.1 MB, sha256 3adc0f9a325c)
- downloaded 18eoextract990.zip -> raw/irs_soi/20261010T131811_18eoextract990.zip (50.7 MB, sha256 cbf88b8401b5)
- downloaded 18eoextractez.zip -> raw/irs_soi/20261010T131812_18eoextractez.zip (11.6 MB, sha256 135f69041f94)
- downloaded 18eofinextractdoc.xlsx -> raw/irs_soi/20261010T131813_18eofinextractdoc.xlsx (0.0 MB, sha256 380a7d88fd97)
- downloaded 19eoextract990.zip -> raw/irs_soi/20261010T131813_19eoextract990.zip (51.2 MB, sha256 3c7719d86091)
- downloaded 19eoextractez.zip -> raw/irs_soi/20261010T131815_19eoextractez.zip (11.2 MB, sha256 9fb76416edf9)
- downloaded 19eofinextractdoc.xlsx -> raw/irs_soi/20261010T131815_19eofinextractdoc.xlsx (0.0 MB, sha256 cdfd43639f02)
- downloaded 20eoextract990.zip -> raw/irs_soi/20261010T131816_20eoextract990.zip (46.5 MB, sha256 9d2d051901d5)
- downloaded 20eoextract990pf.zip -> raw/irs_soi/20261010T131818_20eoextract990pf.zip (10.3 MB, sha256 eb7040005421)
- downloaded 20eoextractez.zip -> raw/irs_soi/20261010T131818_20eoextractez.zip (8.1 MB, sha256 0dccac3867a5)
- downloaded 20eofinextractdoc.xlsx -> raw/irs_soi/20261010T131819_20eofinextractdoc.xlsx (0.0 MB, sha256 6a64356a30ad)
- downloaded 21eoextract990.zip -> raw/irs_soi/20261010T131819_21eoextract990.zip (54.8 MB, sha256 7f18251a8545)
- downloaded 21eoextract990pf.zip -> raw/irs_soi/20261010T131820_21eoextract990pf.zip (13.6 MB, sha256 927e0bc97da3)
- downloaded 21eoextractez.zip -> raw/irs_soi/20261010T131821_21eoextractez.zip (10.6 MB, sha256 2e9ea6cdae17)
- downloaded 21eofinextractdoc.xlsx -> raw/irs_soi/20261010T131821_21eofinextractdoc.xlsx (0.0 MB, sha256 4b5c0eea9a35)
- downloaded 22eoextract990.zip -> raw/irs_soi/20261010T131822_22eoextract990.zip (53.3 MB, sha256 d9b8eb2a88b2)
- downloaded 22eoextract990pf.zip -> raw/irs_soi/20261010T131823_22eoextract990pf.zip (12.5 MB, sha256 49a7fd6b8581)
- downloaded 22eoextractez.zip -> raw/irs_soi/20261010T131824_22eoextractez.zip (11.1 MB, sha256 eb27ffab423a)
- downloaded 22eofinextractdoc.xlsx -> raw/irs_soi/20261010T131824_22eofinextractdoc.xlsx (0.0 MB, sha256 0f64ef332456)
- downloaded 23eoextract990.zip -> raw/irs_soi/20261010T131824_23eoextract990.zip (55.3 MB, sha256 a32f2744b6d7)
- downloaded 23eoextract990pf.zip -> raw/irs_soi/20261010T131826_23eoextract990pf.zip (13.0 MB, sha256 e29d278cf429)
- downloaded 23eoextractez.zip -> raw/irs_soi/20261010T131827_23eoextractez.zip (10.0 MB, sha256 173c976e05fc)
- downloaded 23eofinextractdoc.xlsx -> raw/irs_soi/20261010T131827_23eofinextractdoc.xlsx (0.0 MB, sha256 5cd4d5bc7b63)
- reused 24eoextract990.zip -> raw/irs_soi/20261010T122508_24eoextract990.zip
- downloaded 24eoextract990EZ.zip -> raw/irs_soi/20261010T131827_24eoextract990EZ.zip (9.9 MB, sha256 da6a12f42c30)
- reused 24eoextract990pf.zip -> raw/irs_soi/20261010T122514_24eoextract990pf.zip
- reused 24eofinextractdoc.xlsx -> raw/irs_soi/20261010T122515_24eofinextractdoc.xlsx

### 2026-10-10 13:20 — 22_match_known_funders
- names 243; outcomes {('corp_foundation', 'inferred'): 16, ('exact_name_state', 'yes'): 33, ('exact_name_unique', 'yes'): 20, ('fuzzy_name_state', 'yes'): 6, ('manual', 'inferred'): 3, ('manual', 'yes'): 10, ('manual_reject', 'no'): 9, ('unmatched', 'no'): 146}; accepted EINs 85

### 2026-10-10 13:21 — 22_match_known_funders
- names 243; outcomes {('corp_foundation', 'inferred'): 16, ('exact_name_state', 'yes'): 33, ('exact_name_unique', 'yes'): 20, ('fuzzy_name_state', 'yes'): 6, ('manual', 'inferred'): 3, ('manual', 'yes'): 10, ('manual_reject', 'no'): 9, ('unmatched', 'no'): 146}; accepted EINs 85

### 2026-10-10 13:22 — 20_build_universes
- calvary: 1 EINs
- calvary_known_funders: 85 EINs
- core_peers: 18 EINs
- daf_sponsors: 15 EINs
- dc_sector: 1,024 EINs
- dmv_funders: 7,705 EINs
- dmv_sector: 4,890 EINs
- national_women: 2,452 EINs
- size_matched: 557 EINs
- membership rows 16,747; distinct EINs 15,375; e-file rows 44,778; size band $2,483,998–$9,935,990; missing pins {'F3': [], 'DAF1': []}

### 2026-10-10 13:24 — 60_stage_inputs
- stage_fact_org_financials__inputs.csv: 16 rows
- stage_fact_gov_awards__inputs.csv: 4 rows
- stage_fact_grants__inputs.csv: 360 rows
- stage_fact_roles__inputs.csv: 195 rows

### 2026-10-10 13:25 — 39_build_geo_period
- read 99 ACS raw files (`raw/census/*_acs5_2024_*`), raw/census/20261010T122408_dec2020_pl_blocks_dc.json, raw/census/20261010T122409_bef_sldu2022_11_DC.txt
- dim_geo rows: 243 (tract=206, county=23, ward=8, state=4, nation=1, msa=1); duplicate geo_id: 0
- ward population sum 681,294 vs DC total 681,294 (+0.00%)
- tracts: 206; tract population sum 681,294 (+0.00% vs DC)
- crosswalk: 6,012 blocks, 0 without a ward; 206 tracts, 218 tract-ward rows, 12 tracts split; weight bases {'pop2020': 206}
- tract pop allocated to wards vs SLDU totals: W1 +0.63%; W2 -0.55%; W3 +0.11%; W4 +0.01%; W5 -0.17%; W6 +0.57%; W7 -0.32%; W8 -0.23% (max |diff| 0.63%)
- Calvary tract 11001007503: majority ward 8, weights [[8.0, 1.0]]
- female_poverty_rate: 2 rows blank ({'tract': 2})
- median_hh_income: 9 rows blank ({'tract': 9})
- rent_burden_30plus_share: 2 rows blank ({'tract': 2})
- rent_burden_50plus_share: 2 rows blank ({'tract': 2})
- female_hh_no_spouse_share: 2 rows blank ({'tract': 2})
- QC: all checks passed
- wrote interim/stage_dim_geo__context.csv (243 rows), interim/tract_ward_crosswalk.csv (218 rows), interim/stage_dim_period__context.csv (28 rows: 26 with US CPI, 11 with DC-metro CPI; 2026-2027 blank, not published)

### 2026-10-10 13:25 — 60_stage_inputs
- stage_fact_org_financials__inputs.csv: 16 rows
- stage_fact_gov_awards__inputs.csv: 4 rows
- stage_fact_grants__inputs.csv: 360 rows
- stage_fact_roles__inputs.csv: 195 rows

### 2026-10-10 13:26 — 33_pull_usaspending: slfrf
- public-data page subaward links: []
- workbook raw/treasury/20261010T132621_SLFRF-Subaward-USASpending-File.xlsx (fresh=True; same size as recon copy: True)

### 2026-10-10 13:26 — 33_pull_usaspending: slfrf
- public-data page subaward links: ['https://home.treasury.gov/system/files/136/SLFRF-Subaward-USASpending-File.xlsx']
- workbook raw/treasury/20261010T132621_SLFRF-Subaward-USASpending-File.xlsx (fresh=False; same size as recon copy: True)

### 2026-10-10 13:26 — 61_resolve_entities
- unique name keys 311; alias rows 311
- occurrences by method:
match_method  exact_ein  exact_name_city  exact_name_state  fuzzy_name_city  manual  manual_reject  unmatched
role                                                                                                         
funder                0               30                 3                3      23             12        289
pass_through          0                0                 0                0       0              0          4
recipient           364                0                 0                0       0              0          0

### 2026-10-10 13:27 — 41_pull_soi_extracts: stage
- universe EINs: 15,375
- 990 2012 (12eofinextract990.zip): 294,019 rows read, 2,200 universe rows; fields absent this year: grants_paid, compensation_total, cash_savings_eoy
- 990 2013 (13eofinextract990.zip): 289,603 rows read, 2,202 universe rows
- 990 2014 (14eofinextract990.zip): 299,405 rows read, 2,284 universe rows
- 990 2015 (15eofinextract990.zip): 294,782 rows read, 2,199 universe rows
- 990 2016 (16eofinextract990.zip): 307,483 rows read, 2,368 universe rows
- 990 2017 (17eofinextract990.zip): 300,910 rows read, 2,369 universe rows
- 990 2018 (18eoextract990.zip): 313,339 rows read, 2,457 universe rows
- 990 2019 (19eoextract990.zip): 304,441 rows read, 2,468 universe rows
- 990 2020 (20eoextract990.zip): 273,971 rows read, 2,246 universe rows
- 990 2021 (21eoextract990.zip): 342,920 rows read, 2,817 universe rows
- 990 2022 (22eoextract990.zip): 326,123 rows read, 2,742 universe rows
- 990 2023 (23eoextract990.zip): 338,048 rows read, 2,761 universe rows
- 990 2024 (24eoextract990.zip): 345,365 rows read, 2,905 universe rows
- 990EZ 2012 (12eofinextract990ez.zip): 223,348 rows read, 584 universe rows
- 990EZ 2013 (13eofinextract990ez.zip): 218,981 rows read, 597 universe rows
- 990EZ 2014 (14eofinextract990ez.zip): 234,820 rows read, 643 universe rows
- 990EZ 2015 (15eofinextractEZ.zip): 223,028 rows read, 653 universe rows
- 990EZ 2016 (16eofinextractez.zip): 230,745 rows read, 723 universe rows
- 990EZ 2017 (17eofinextractEZ.zip): 218,097 rows read, 723 universe rows
- 990EZ 2018 (18eoextractez.zip): 226,533 rows read, 753 universe rows
- 990EZ 2019 (19eoextractez.zip): 218,671 rows read, 766 universe rows
- 990EZ 2020 (20eoextractez.zip): 154,314 rows read, 530 universe rows
- 990EZ 2021 (21eoextractez.zip): 218,733 rows read, 852 universe rows
- 990EZ 2022 (22eoextractez.zip): 231,289 rows read, 972 universe rows
- 990EZ 2023 (23eoextractez.zip): 207,536 rows read, 909 universe rows
- 990EZ 2024 (24eoextract990EZ.zip): 203,699 rows read, 959 universe rows
- 990PF 2012 (12eofinextract990pf.zip): 98,948 rows read, 2,669 universe rows; fields absent this year: x_pf_grants_approved_future
- 990PF 2013 (13eofinextract990pf.zip): 100,484 rows read, 2,753 universe rows
- 990PF 2014 (14eofinextract990pf.zip): 101,381 rows read, 2,902 universe rows
- 990PF 2015 (15eofinextract990pf.zip): 103,000 rows read, 2,934 universe rows
- 990PF 2016 (16eofinextract990pf.zip): 105,239 rows read, 3,128 universe rows
- 990PF 2020 (20eoextract990pf.zip): 91,473 rows read, 3,021 universe rows
- 990PF 2021 (21eoextract990pf.zip): 125,312 rows read, 4,414 universe rows
- 990PF 2022 (22eoextract990pf.zip): 115,024 rows read, 4,266 universe rows
- 990PF 2023 (23eoextract990pf.zip): 120,350 rows read, 4,588 universe rows
- 990PF 2024 (24eoextract990pf.zip): 119,059 rows read, 4,795 universe rows
- staged 77,152 rows (interim/stage_fact_org_financials__soi.csv), 9,329 EINs; dropped 0 older-processing-year copies; 0 staged rows whose copies disagree on total_revenue
- duplicate (ein, tax_period_end, return_type, source_id): 0
- Calvary QC: TY2020 total_revenue 3,851,984 OK; TY2021 total_revenue 8,867,250 OK
- 990-PF SOI TAX_YR equals derived tax_year on 100.0% of rows
- rows by return_type x fiscal_year (period-end year):
```
return_type    990  990EZ  990PF    All
fiscal_year                            
2002             0      0      1      1
2003             1      0      1      2
2004             0      0      1      1
2005             1      0      1      2
2006             0      0      1      1
2007             0      2      3      5
2008             2     12      7     21
2009             4     30     14     48
2010           175     92     84    351
2011          1833    512   2406   4751
2012          2176    611   2754   5541
2013          2229    609   2829   5667
2014          2245    655   2972   5872
2015          2312    694   3038   6044
2016          2389    729    310   3428
2017          2439    737     23   3199
2018          2512    751    110   3373
2019          2570    788   3460   6818
2020          2591    830   3903   7324
2021          2698    818   4204   7720
2022          2785    855   4434   8074
2023          2790    857   4559   8206
2024           266     82    355    703
All          32018   9664  35470  77152
```
- coverage by universe:
  - calvary: 1/1 EINs with >=1 SOI row; 13 org-years; median years per covered org 13
  - calvary_known_funders: 81/85 EINs with >=1 SOI row; 837 org-years; median years per covered org 10
  - core_peers: 18/18 EINs with >=1 SOI row; 235 org-years; median years per covered org 13
  - daf_sponsors: 15/15 EINs with >=1 SOI row; 184 org-years; median years per covered org 13
  - dc_sector: 524/1,024 EINs with >=1 SOI row; 4,620 org-years; median years per covered org 11
  - dmv_funders: 5,744/7,705 EINs with >=1 SOI row; 44,487 org-years; median years per covered org 10
  - dmv_sector: 1,939/4,890 EINs with >=1 SOI row; 15,524 org-years; median years per covered org 9
  - national_women: 1,280/2,452 EINs with >=1 SOI row; 12,487 org-years; median years per covered org 13
  - size_matched: 555/557 EINs with >=1 SOI row; 6,773 org-years; median years per covered org 13

### 2026-10-10 13:27 — 34_pull_fac: FAC bulk pull
- general rows (DC/MD/VA, 2016-2025, deduped by report_id): 18233; per state-year: {"DC_2016": 391, "DC_2017": 384, "DC_2018": 402, "DC_2019": 398, "DC_2020": 387, "DC_2021": 409, "DC_2022": 466, "DC_2023": 477, "DC_2024": 467, "DC_2025": 359, "MD_2016": 522, "MD_2017": 529, "MD_2018": 516, "MD_2019": 527, "MD_2020": 515, "MD_2021": 585, "MD_2022": 637, "MD_2023": 616, "MD_2024": 599, "MD_2025": 552, "VA_2016": 763, "VA_2017": 801, "VA_2018": 805, "VA_2019": 802, "VA_2020": 816, "VA_2021": 914, "VA_2022": 900, "VA_2023": 884, "VA_2024": 965, "VA_2025": 845}
- multi-EIN reports 1417 (additional EINs on 1417); additional-UEI reports 475 (2126 rows)
- kept reports (FAC scope: calvary, core_peers, dc_sector, dmv_sector, dmv_funders): 1835 ({'auditee_ein': 1787, 'additional_ein': 48}); core-scope EINs with a report: 233
- federal_awards rows 9864; passthrough rows 5538
- uei_ein_map rows 9785 (in-scope UEIs 209) -> interim/uei_ein_map.csv
- audit_year vs FY dates: {'calendar_or_same_year': 2346, 'noncal_audit_year=end': 15887}
- requests 89; manifest raw/fac/20261010T132731_pull34_manifest.json

### 2026-10-10 13:27 — 61_resolve_entities
- unique name keys 311; alias rows 311
- occurrences by method:
match_method  exact_ein  known_funder  manual  manual_reject  unmatched
role                                                                   
funder                0           112      23             12        213
pass_through          0             0       0              0          4
recipient           364             0       0              0          0

### 2026-10-10 13:29 — 62_build_facts
- fact_org_financials: 77,168 rows
- fact_grants: 360 rows
- fact_gov_awards: 4 rows
- fact_opportunities: 0 rows
- fact_policy_events: 0 rows
- supp_calvary_individual_donor_bands.csv: copied from stage_supp_calvary_individual_donor_bands.csv
- supp_calvary_program_metrics.csv: copied from stage_supp_calvary_program_metrics.csv
- supp_calvary_strategic_targets.csv: copied from stage_supp_calvary_strategic_targets.csv

### 2026-10-10 13:30 — 43_web_calvary
- support page: 98 organizations (3 flagged in-kind); Phase 1 PDF had 98 (11 truncated). Names absent from the PDF parse: 11
- truncated names recovered: Morris, Mann -> Morris, Manning & Martin, LLP; Nelson Mulli -> Nelson Mullins; NFP Golden & -> NFP Golden & Cohen; Robert Charle -> Robert Charles Lesser Co.; Sapodilla's C -> Sapodilla's Caribbean Restaurant and Catering; Saul Ewing A -> Saul Ewing Arnstein & Lehr LLP; Southern Com -> Southern Company; The Brand Gu -> The Brand Guild; The Menkiti G -> The Menkiti Group; United Bank -> United Bank; Women's Ene -> Women's Energy Resource Council
- PDFs seen: 96 (financials page links + WP media library + off-site search); kept as new: 21: 2015-07-Corporate-Partner-Program-packet.pdf [funder_list, ok]; CWS-Audited-Financial-Statements-2014.pdf [audit, ok]; CWS-Form-990-2014.pdf [form_990, ok]; Corporate-Partners-Program-packet.pdf [funder_list, ok]; Corporate-Partners-Program-packet_11-11-2014.pdf [funder_list, ok]; Corporate-Partners-Program-packet_11-13-2014.pdf [funder_list, ok]; FY2013-Annual-Report-simple-version-FINAL.pdf [annual_report, ok]; What-Do-Corporate-Partners-Do_combined.pdf [funder_list, ok]; Calvary-Womens-Services-2014-Annual-Report.pdf [annual_report, ok]; 2017-Hope-Awards-Sponsorship-Opportunities.pdf [funder_list, ok]; Step-Up-DC-2016-Year-End-Report.pdf [funder_list, ok]; 2019-02-04-Calvary-Annual-Design.pdf [annual_report, ok]; Calvary-Womens-Services-FY18-Annual-Report.pdf [annual_report, ok]; CWS-Corporate-Partners-Program-Overview.pdf [funder_list, ok]; Hope-Awards-Sponsors.pdf [funder_list, ok]; 2024-Corporate-Partners-Program-Opportunities_CWS.pdf [funder_list, ok]; 2025-Hope-Gala-Sponsorship_CWS-2.pdf [funder_list, ok]; 2025-Hope-Gala-Sponsorship_CWS-2.pdf [funder_list, ok]; Calvary-Newsletter-02_25.pdf [funder_list, ok]; 521307706_2022_25813620221_A133.pdf [other, ok; found by cal_audit_fy24]; Calvary-Independent-Auditors-Report.pdf [audit, ok; found by cal_audit_fy25]
- off-site search hits: 54 results, PDFs downloaded: 2
- annual-report donors: 0 org rows; individual band counts rows 0; 
- new audits: 0 financial/note rows, 0 SEFA rows; 
- this run: Tavily search 6, extract 0, HTTP GET 26, cache hits 0; cumulative (manifest): search 6/300, extract 0/200, HTTP 26

### 2026-10-10 13:30 — 30_fetch_xml: targets
- scope EINs 8,705; EINs with a TY2020+ e-filed 990/EZ/PF in the index 6,772
- returns 31,469 (latest per EIN+period+type) {'990PF': 24877, '990': 4858, '990EZ': 1734}; with >1 submission 351
- GT S3 at 20 req/s, IRS ZIP fallback 4 req/s; 16 threads

### 2026-10-10 13:30 — 41_pull_soi_extracts: nccs_download
- downloaded F9-P08-T00-REVENUE-2009.csv -> raw/nccs/20261010T132915_F9-P08-T00-REVENUE-2009.csv (22.5 MB)
- downloaded F9-P08-T00-REVENUE-2010.csv -> raw/nccs/20261010T132916_F9-P08-T00-REVENUE-2010.csv (83.0 MB)
- downloaded F9-P08-T00-REVENUE-2011.csv -> raw/nccs/20261010T132919_F9-P08-T00-REVENUE-2011.csv (108.4 MB)
- downloaded F9-P08-T00-REVENUE-2012.csv -> raw/nccs/20261010T132923_F9-P08-T00-REVENUE-2012.csv (122.6 MB)
- downloaded F9-P08-T00-REVENUE-2013.csv -> raw/nccs/20261010T132928_F9-P08-T00-REVENUE-2013.csv (135.7 MB)
- downloaded F9-P08-T00-REVENUE-2014.csv -> raw/nccs/20261010T132933_F9-P08-T00-REVENUE-2014.csv (149.8 MB)
- downloaded F9-P08-T00-REVENUE-2015.csv -> raw/nccs/20261010T132940_F9-P08-T00-REVENUE-2015.csv (160.0 MB)
- downloaded F9-P08-T00-REVENUE-2016.csv -> raw/nccs/20261010T132946_F9-P08-T00-REVENUE-2016.csv (166.9 MB)
- downloaded F9-P08-T00-REVENUE-2017.csv -> raw/nccs/20261010T132953_F9-P08-T00-REVENUE-2017.csv (174.4 MB)
- downloaded F9-P08-T00-REVENUE-2018.csv -> raw/nccs/20261010T132959_F9-P08-T00-REVENUE-2018.csv (181.1 MB)
- downloaded F9-P08-T00-REVENUE-2019.csv -> raw/nccs/20261010T133005_F9-P08-T00-REVENUE-2019.csv (237.7 MB)
- downloaded F9-P08-T00-REVENUE-2020.csv -> raw/nccs/20261010T133015_F9-P08-T00-REVENUE-2020.csv (263.8 MB)
- downloaded F9-P08-T00-REVENUE-2021.csv -> raw/nccs/20261010T133024_F9-P08-T00-REVENUE-2021.csv (266.4 MB)
- downloaded F9-P08-T00-REVENUE-2022.csv -> raw/nccs/20261010T133034_F9-P08-T00-REVENUE-2022.csv (69.5 MB)
- NCCS Core 990-PF merged file sizes (raw/nccs/20261010T133039_core_990pf_head_check.json): 2012 68.7 MB; 2013 71.6 MB; 2014 73.5 MB; 2015 72.7 MB; 2016 8.6 MB; 2017 0.5 MB; 2018 2.3 MB; 2019 72.3 MB; 2020 80.6 MB; 2021 82.1 MB; 2022 83.7 MB; 2023 82.4 MB; 2024 7.5 MB
- NCCS Core 990-PF 2016-2018 files are 0.5-8.6 MB vs 69-84 MB in other years: the same gap as the SOI 990-PF extracts, so no NCCS 990-PF download

### 2026-10-10 13:30 — 63_build_dims
- dim_org: 15,375 rows
- dim_funder: 7,938 rows
- dim_program_area: 13 rows
- dim_period: 28 rows
- dim_geo: 243 rows

### 2026-10-10 13:31 — 43_web_calvary
- support page: 98 organizations (3 flagged in-kind); Phase 1 PDF had 98 (11 truncated). Names absent from the PDF parse: 11
- truncated names recovered: Morris, Mann -> Morris, Manning & Martin, LLP; Nelson Mulli -> Nelson Mullins; NFP Golden & -> NFP Golden & Cohen; Robert Charle -> Robert Charles Lesser Co.; Sapodilla's C -> Sapodilla's Caribbean Restaurant and Catering; Saul Ewing A -> Saul Ewing Arnstein & Lehr LLP; Southern Com -> Southern Company; The Brand Gu -> The Brand Guild; The Menkiti G -> The Menkiti Group; United Bank -> United Bank; Women's Ene -> Women's Energy Resource Council
- PDFs seen: 95 (financials page links + WP media library + off-site search); kept as new: 20: 2015-07-Corporate-Partner-Program-packet.pdf [funder_list, ok]; CWS-Audited-Financial-Statements-2014.pdf [audit, ok]; CWS-Form-990-2014.pdf [form_990, ok]; Corporate-Partners-Program-packet.pdf [funder_list, ok]; Corporate-Partners-Program-packet_11-11-2014.pdf [funder_list, ok]; Corporate-Partners-Program-packet_11-13-2014.pdf [funder_list, ok]; FY2013-Annual-Report-simple-version-FINAL.pdf [annual_report, ok]; What-Do-Corporate-Partners-Do_combined.pdf [funder_list, ok]; Calvary-Womens-Services-2014-Annual-Report.pdf [annual_report, ok]; 2017-Hope-Awards-Sponsorship-Opportunities.pdf [funder_list, ok]; Step-Up-DC-2016-Year-End-Report.pdf [funder_list, ok]; 2019-02-04-Calvary-Annual-Design.pdf [annual_report, ok]; Calvary-Womens-Services-FY18-Annual-Report.pdf [annual_report, ok]; CWS-Corporate-Partners-Program-Overview.pdf [funder_list, ok]; Hope-Awards-Sponsors.pdf [funder_list, ok]; 2024-Corporate-Partners-Program-Opportunities_CWS.pdf [funder_list, ok]; 2025-Hope-Gala-Sponsorship_CWS-2.pdf [funder_list, ok]; 2025-Hope-Gala-Sponsorship_CWS-2.pdf [funder_list, ok]; Calvary-Newsletter-02_25.pdf [funder_list, ok]; 521307706_2022_25813620221_A133.pdf [other, ok; found by cal_audit_fy24]
- off-site search hits: 104 results; Calvary PDFs kept: 1; rejected: Calvary-Independent-Auditors-Report.pdf (cal_audit_fy25: not a Calvary Women's Services document)
- annual-report donors: 0 org rows; individual band counts rows 0; 
- new audits: 0 financial/note rows, 0 SEFA rows; 
- this run: Tavily search 5, extract 0, HTTP GET 0, cache hits 32; cumulative (manifest): search 11/300, extract 0/200, HTTP 26

### 2026-10-10 13:31 — 64_people_relationships
- fact_roles 195; dim_person 84 (multi-org 0); candidate_interlocks 0; fact_org_relationships 29 {'grant': 29}

### 2026-10-10 13:32 — 35_pull_grantsgov: opportunities
- universe posted+forecasted 1467; kept 530 (local cfdaList 3, cfda key 3, keyword search 530); fetch failures 0
- interim/stage_fact_opportunities__grantsgov.csv: 530 rows (407 posted, 123 forecasted); duplicate ids 0
- keyword_hits counts: {"homelessness": 15, "housing": 176, "domestic violence": 9, "victim services": 4, "women": 167, "substance use": 62, "workforce": 217, "reentry": 9, "veterans": 83, "aging": 99}
- target-ALN rows: 3; nonprofit-eligible (12/13/25/99): 498
- manifest raw/grantsgov/20261010T133220_pull35_manifest.json

### 2026-10-10 13:32 — 41_pull_soi_extracts: stage
- universe EINs: 15,375
- 990 2012 (12eofinextract990.zip): 294,019 rows read, 2,200 universe rows; fields absent this year: grants_paid, compensation_total, cash_savings_eoy
- 990 2013 (13eofinextract990.zip): 289,603 rows read, 2,202 universe rows
- 990 2014 (14eofinextract990.zip): 299,405 rows read, 2,284 universe rows
- 990 2015 (15eofinextract990.zip): 294,782 rows read, 2,199 universe rows
- 990 2016 (16eofinextract990.zip): 307,483 rows read, 2,368 universe rows
- 990 2017 (17eofinextract990.zip): 300,910 rows read, 2,369 universe rows
- 990 2018 (18eoextract990.zip): 313,339 rows read, 2,457 universe rows
- 990 2019 (19eoextract990.zip): 304,441 rows read, 2,468 universe rows
- 990 2020 (20eoextract990.zip): 273,971 rows read, 2,246 universe rows
- 990 2021 (21eoextract990.zip): 342,920 rows read, 2,817 universe rows
- 990 2022 (22eoextract990.zip): 326,123 rows read, 2,742 universe rows
- 990 2023 (23eoextract990.zip): 338,048 rows read, 2,761 universe rows
- 990 2024 (24eoextract990.zip): 345,365 rows read, 2,905 universe rows
- 990EZ 2012 (12eofinextract990ez.zip): 223,348 rows read, 584 universe rows
- 990EZ 2013 (13eofinextract990ez.zip): 218,981 rows read, 597 universe rows
- 990EZ 2014 (14eofinextract990ez.zip): 234,820 rows read, 643 universe rows
- 990EZ 2015 (15eofinextractEZ.zip): 223,028 rows read, 653 universe rows
- 990EZ 2016 (16eofinextractez.zip): 230,745 rows read, 723 universe rows
- 990EZ 2017 (17eofinextractEZ.zip): 218,097 rows read, 723 universe rows
- 990EZ 2018 (18eoextractez.zip): 226,533 rows read, 753 universe rows
- 990EZ 2019 (19eoextractez.zip): 218,671 rows read, 766 universe rows
- 990EZ 2020 (20eoextractez.zip): 154,314 rows read, 530 universe rows
- 990EZ 2021 (21eoextractez.zip): 218,733 rows read, 852 universe rows
- 990EZ 2022 (22eoextractez.zip): 231,289 rows read, 972 universe rows
- 990EZ 2023 (23eoextractez.zip): 207,536 rows read, 909 universe rows
- 990EZ 2024 (24eoextract990EZ.zip): 203,699 rows read, 959 universe rows
- 990PF 2012 (12eofinextract990pf.zip): 98,948 rows read, 2,669 universe rows; fields absent this year: x_pf_grants_approved_future
- 990PF 2013 (13eofinextract990pf.zip): 100,484 rows read, 2,753 universe rows
- 990PF 2014 (14eofinextract990pf.zip): 101,381 rows read, 2,902 universe rows
- 990PF 2015 (15eofinextract990pf.zip): 103,000 rows read, 2,934 universe rows
- 990PF 2016 (16eofinextract990pf.zip): 105,239 rows read, 3,128 universe rows
- 990PF 2020 (20eoextract990pf.zip): 91,473 rows read, 3,021 universe rows
- 990PF 2021 (21eoextract990pf.zip): 125,312 rows read, 4,414 universe rows
- 990PF 2022 (22eoextract990pf.zip): 115,024 rows read, 4,266 universe rows
- 990PF 2023 (23eoextract990pf.zip): 120,350 rows read, 4,588 universe rows
- 990PF 2024 (24eoextract990pf.zip): 119,059 rows read, 4,795 universe rows
- SOI: 77,152 rows, 9,329 EINs; 0 older-processing-year copies dropped; 0 rows whose copies disagree on total_revenue
- NCCS 2009: 48,857 rows read, 272 universe 990 rows
- NCCS 2010: 184,553 rows read, 913 universe 990 rows
- NCCS 2011: 241,595 rows read, 1,249 universe 990 rows
- NCCS 2012: 273,429 rows read, 1,453 universe 990 rows
- NCCS 2013: 303,225 rows read, 1,609 universe 990 rows
- NCCS 2014: 335,066 rows read, 1,745 universe 990 rows
- NCCS 2015: 358,459 rows read, 1,921 universe 990 rows
- NCCS 2016: 374,252 rows read, 2,000 universe 990 rows
- NCCS 2017: 391,170 rows read, 2,115 universe 990 rows
- NCCS 2018: 406,376 rows read, 2,207 universe 990 rows
- NCCS 2019: 436,217 rows read, 2,343 universe 990 rows
- NCCS 2020: 485,459 rows read, 2,616 universe 990 rows
- NCCS 2021: 491,127 rows read, 2,502 universe 990 rows
- NCCS 2022: 131,588 rows read, 340 universe 990 rows
- NCCS: 22,080 rows staged, 3,038 EINs, tax years 2010-2022; period from SOI match 22,063, from IRS index 17; dropped 883 with no period; 307 EIN-years had >1 return (kept the latest OBJECT_ID)
- NCCS total_revenue equals SOI total_revenue on 99.1% of 22,063 matched rows
- wrote 99,232 rows to interim/stage_fact_org_financials__soi.csv (SOI 77,152; NCCS 22,080)
- duplicate (ein, tax_period_end, return_type, source_id): 0
- Calvary total_revenue QC: bulk_irs_soi_extract TY2020 3,851,984 OK; bulk_irs_soi_extract TY2021 8,867,250 OK; bulk_nccs_efile TY2020 3,851,984 OK; bulk_nccs_efile TY2021 not present
- 990-PF SOI TAX_YR equals derived tax_year on 100.0% of rows
- rows by fiscal_year (period-end year) x return_type / source:
```
source_id   irs_soi_extract              nccs_efile    All
return_type             990 990EZ  990PF        990       
fiscal_year                                               
2002                      0     0      1          0      1
2003                      1     0      1          0      2
2004                      0     0      1          0      1
2005                      1     0      1          0      2
2006                      0     0      1          0      1
2007                      0     2      3          0      5
2008                      2    12      7          0     21
2009                      4    30     14          0     48
2010                    175    92     84          5    356
2011                   1833   512   2406        808   5559
2012                   2176   611   2754       1355   6896
2013                   2229   609   2829       1524   7191
2014                   2245   655   2972       1625   7497
2015                   2312   694   3038       1818   7862
2016                   2389   729    310       1932   5360
2017                   2439   737     23       2033   5232
2018                   2512   751    110       2134   5507
2019                   2570   788   3460       2254   9072
2020                   2591   830   3903       2484   9808
2021                   2698   818   4204       2626  10346
2022                   2785   855   4434       1476   9550
2023                   2790   857   4559          6   8212
2024                    266    82    355          0    703
All                   32018  9664  35470      22080  99232
```
- coverage, bulk_irs_soi_extract (EINs with >=1 row / universe EINs; org-years; median years per covered org):
  - calvary: 1/1; 13; 13
  - calvary_known_funders: 81/85; 837; 10
  - core_peers: 18/18; 235; 13
  - daf_sponsors: 15/15; 184; 13
  - dc_sector: 524/1,024; 4,620; 11
  - dmv_funders: 5,744/7,705; 44,487; 10
  - dmv_sector: 1,939/4,890; 15,524; 9
  - national_women: 1,280/2,452; 12,487; 13
  - size_matched: 555/557; 6,773; 13
- coverage, bulk_nccs_efile (EINs with >=1 row / universe EINs; org-years; median years per covered org):
  - calvary: 1/1; 7; 7
  - calvary_known_funders: 31/85; 247; 9
  - core_peers: 18/18; 172; 10
  - daf_sponsors: 15/15; 84; 6
  - dc_sector: 370/1,024; 2,550; 7
  - dmv_funders: 650/7,705; 4,046; 6
  - dmv_sector: 1,139/4,890; 7,856; 7
  - national_women: 892/2,452; 7,277; 10
  - size_matched: 549/557; 4,772; 10

### 2026-10-10 13:32 — 43_web_calvary
- support page: 98 organizations (3 flagged in-kind); Phase 1 PDF had 98 (11 truncated). Names absent from the PDF parse: 11
- truncated names recovered: Morris, Mann -> Morris, Manning & Martin, LLP; Nelson Mulli -> Nelson Mullins; NFP Golden & -> NFP Golden & Cohen; Robert Charle -> Robert Charles Lesser Co.; Sapodilla's C -> Sapodilla's Caribbean Restaurant and Catering; Saul Ewing A -> Saul Ewing Arnstein & Lehr LLP; Southern Com -> Southern Company; The Brand Gu -> The Brand Guild; The Menkiti G -> The Menkiti Group; United Bank -> United Bank; Women's Ene -> Women's Energy Resource Council
- PDFs seen: 98 (financials page links + WP media library + off-site search); kept as new: 22: 2015-07-Corporate-Partner-Program-packet.pdf [funder_list, ok]; CWS-Audited-Financial-Statements-2014.pdf [audit, ok]; CWS-Form-990-2014.pdf [form_990, ok]; CWS-form-990-2013.pdf [form_990, ok]; Corporate-Partners-Program-packet.pdf [funder_list, ok]; Corporate-Partners-Program-packet_11-11-2014.pdf [funder_list, ok]; Corporate-Partners-Program-packet_11-13-2014.pdf [funder_list, ok]; FY2013-Annual-Report-simple-version-FINAL.pdf [annual_report, ok]; What-Do-Corporate-Partners-Do_combined.pdf [funder_list, ok]; audited-statements-2013.pdf [audit, ok]; Calvary-Womens-Services-2014-Annual-Report.pdf [annual_report, ok]; 2017-Hope-Awards-Sponsorship-Opportunities.pdf [funder_list, ok]; Step-Up-DC-2016-Year-End-Report.pdf [funder_list, ok]; 2019-02-04-Calvary-Annual-Design.pdf [annual_report, ok]; Calvary-Womens-Services-FY18-Annual-Report.pdf [annual_report, ok]; CWS-Corporate-Partners-Program-Overview.pdf [funder_list, ok]; Hope-Awards-Sponsors.pdf [funder_list, ok]; 2024-Corporate-Partners-Program-Opportunities_CWS.pdf [funder_list, ok]; 2025-Hope-Gala-Sponsorship_CWS-2.pdf [funder_list, ok]; 2025-Hope-Gala-Sponsorship_CWS-2.pdf [funder_list, ok]; Calvary-Newsletter-02_25.pdf [funder_list, ok]; 521307706_2022_25813620221_A133.pdf [other, ok; found by cal_audit_fy24]
- off-site search hits: 104 results; Calvary PDFs kept: 1; rejected: Calvary-Independent-Auditors-Report.pdf (cal_audit_fy25: not a Calvary Women's Services document)
- annual-report donors: 0 org rows; individual band counts rows 0; 
- new audits: 0 financial/note rows, 0 SEFA rows; 
- this run: Tavily search 0, extract 0, HTTP GET 4, cache hits 37; cumulative (manifest): search 11/300, extract 0/200, HTTP 30

### 2026-10-10 13:32 — 30_fetch_xml: progress
- pass 1: 2,000/31,469 done in 2.1 min (16.0/s); 93 MB on disk for done files; ok 2,000, not_found 0, error 0

### 2026-10-10 13:33 — 64_people_relationships
- fact_roles 195; dim_person 84 (multi-org 0); candidate_interlocks 0; fact_org_relationships 29 {'grant': 29}

### 2026-10-10 13:33 — 70_quality_checks
- wrote reports/data_quality.md; duplicates []; portability issues ['scripts/70_quality_checks.py']

### 2026-10-10 13:33 — 70_quality_checks
- wrote reports/data_quality.md; duplicates []; portability issues ['scripts/70_quality_checks.py']

### 2026-10-10 13:33 — 70_quality_checks
- wrote reports/data_quality.md; duplicates []; portability issues []

### 2026-10-10 13:34 — 30_fetch_xml: progress
- pass 1: 4,000/31,469 done in 3.7 min (17.8/s); 253 MB on disk for done files; ok 4,000, not_found 0, error 0

### 2026-10-10 13:34 — 80_docs
- data_dictionary rows 460; undocumented columns 101; source_ids missing from registry: none

### 2026-10-10 13:34 — 80_docs
- data_dictionary rows 460; undocumented columns 0; source_ids missing from registry: none

### 2026-10-10 13:36 — 30_fetch_xml: progress
- pass 1: 6,000/31,469 done in 5.6 min (18.0/s); 363 MB on disk for done files; ok 6,000, not_found 0, error 0

### 2026-10-10 13:37 — 43_web_calvary
- support page: 98 organizations (3 flagged in-kind); Phase 1 PDF had 98 (11 truncated). Names absent from the PDF parse: 11
- truncated names recovered: Morris, Mann -> Morris, Manning & Martin, LLP; Nelson Mulli -> Nelson Mullins; NFP Golden & -> NFP Golden & Cohen; Robert Charle -> Robert Charles Lesser Co.; Sapodilla's C -> Sapodilla's Caribbean Restaurant and Catering; Saul Ewing A -> Saul Ewing Arnstein & Lehr LLP; Southern Com -> Southern Company; The Brand Gu -> The Brand Guild; The Menkiti G -> The Menkiti Group; United Bank -> United Bank; Women's Ene -> Women's Energy Resource Council
- PDFs seen: 98 (financials page links + WP media library + off-site search); kept as new: 22: 2015-07-Corporate-Partner-Program-packet.pdf [funder_list, ok]; CWS-Audited-Financial-Statements-2014.pdf [audit, ok]; CWS-Form-990-2014.pdf [form_990, ok]; CWS-form-990-2013.pdf [form_990, ok]; Corporate-Partners-Program-packet.pdf [funder_list, ok]; Corporate-Partners-Program-packet_11-11-2014.pdf [funder_list, ok]; Corporate-Partners-Program-packet_11-13-2014.pdf [funder_list, ok]; FY2013-Annual-Report-simple-version-FINAL.pdf [annual_report, ok]; What-Do-Corporate-Partners-Do_combined.pdf [funder_list, ok]; audited-statements-2013.pdf [audit, ok]; Calvary-Womens-Services-2014-Annual-Report.pdf [annual_report, ok]; 2017-Hope-Awards-Sponsorship-Opportunities.pdf [funder_list, ok]; Step-Up-DC-2016-Year-End-Report.pdf [funder_list, ok]; 2019-02-04-Calvary-Annual-Design.pdf [annual_report, ok]; Calvary-Womens-Services-FY18-Annual-Report.pdf [annual_report, ok]; CWS-Corporate-Partners-Program-Overview.pdf [funder_list, ok]; Hope-Awards-Sponsors.pdf [funder_list, ok]; 2024-Corporate-Partners-Program-Opportunities_CWS.pdf [funder_list, ok]; 2025-Hope-Gala-Sponsorship_CWS-2.pdf [funder_list, ok]; 2025-Hope-Gala-Sponsorship_CWS-2.pdf [funder_list, duplicate_of_web:https://www.calvaryservices.org/wp-content/uploads/2025/02/2025-Hope-Gala-Sponsorship_CWS-2.pdf]; Calvary-Newsletter-02_25.pdf [funder_list, ok]; 521307706_2022_25813620221_A133.pdf [other, ok; found by cal_audit_fy24]
- off-site search hits: 104 results; Calvary PDFs kept: 1; rejected: Calvary-Independent-Auditors-Report.pdf (cal_audit_fy25: not a Calvary Women's Services document)
- annual-report donors: 74 org rows; named lists/mentions 127 rows; individual band-count rows 3; Calvary-Womens-Services-2014-Annual-Report.pdf: 74 org donor entries, 182 individual entries (counted only); 2017-Hope-Awards-Sponsorship-Opportunities.pdf [Hope Awards Dinner: companies that have sponsored (cumulative)]: 41; Step-Up-DC-2016-Year-End-Report.pdf [Step Up DC supporters ('supported the program this year')]: 5; 2025-Hope-Gala-Sponsorship_CWS-2.pdf [Hope Gala: Past Event Sponsors (cumulative)]: 39; 2025-Hope-Gala-Sponsorship_CWS-2.pdf [Hope Gala: Past Event Sponsors (cumulative)]: 39
- new audits: 293 financial/note rows, 4 SEFA rows; CWS-Audited-Financial-Statements-2014.pdf p5 SFP: 'Grants receivable (Note' has 3 amounts, expected 2; CWS-Audited-Financial-Statements-2014.pdf p5 SFP: 'Furniture and equipment (Note' has 3 amounts, expected 2; CWS-Audited-Financial-Statements-2014.pdf p5 SFP: 'Current portion of long-term debt (Note' has 3 amounts, expected 2; CWS-Audited-Financial-Statements-2014.pdf p5 SFP: 'Long-term debt, net of current portion (Note' has 3 amounts, expected 2; CWS-Audited-Financial-Statements-2014.pdf p5 SFP: 'Temporarily restricted (Note' has 3 amounts, expected 2; CWS-Audited-Financial-Statements-2014.pdf p6 SOA: 'Government grants (Note' has 5 amounts, expected 4; CWS-Audited-Financial-Statements-2014.pdf p6 SOA: 'Contributed services and materials (Note' has 5 amounts, expected 4; CWS-Audited-Financial-Statements-2014.pdf p6 SOA: 'Net assets released from donor restrictions (Note' has 5 amounts, expected 4; CWS-Audited-Financial-Statements-2014.pdf: no SEFA in the PDF; 521307706_2022_25813620221_A133.pdf: SEFA p29 4 programs sum 4,067,718 vs printed total 4,067,718
- this run: Tavily search 0, extract 0, HTTP GET 0, cache hits 41; cumulative (manifest): search 11/300, extract 0/200, HTTP 30

### 2026-10-10 13:37 — 41_pull_soi_extracts: stage
- universe EINs: 15,375
- 990 2012 (12eofinextract990.zip): 294,019 rows read, 2,200 universe rows; fields absent this year: grants_paid, compensation_total, cash_savings_eoy
- 990 2013 (13eofinextract990.zip): 289,603 rows read, 2,202 universe rows
- 990 2014 (14eofinextract990.zip): 299,405 rows read, 2,284 universe rows
- 990 2015 (15eofinextract990.zip): 294,782 rows read, 2,199 universe rows
- 990 2016 (16eofinextract990.zip): 307,483 rows read, 2,368 universe rows
- 990 2017 (17eofinextract990.zip): 300,910 rows read, 2,369 universe rows
- 990 2018 (18eoextract990.zip): 313,339 rows read, 2,457 universe rows
- 990 2019 (19eoextract990.zip): 304,441 rows read, 2,468 universe rows
- 990 2020 (20eoextract990.zip): 273,971 rows read, 2,246 universe rows
- 990 2021 (21eoextract990.zip): 342,920 rows read, 2,817 universe rows
- 990 2022 (22eoextract990.zip): 326,123 rows read, 2,742 universe rows
- 990 2023 (23eoextract990.zip): 338,048 rows read, 2,761 universe rows
- 990 2024 (24eoextract990.zip): 345,365 rows read, 2,905 universe rows
- 990EZ 2012 (12eofinextract990ez.zip): 223,348 rows read, 584 universe rows
- 990EZ 2013 (13eofinextract990ez.zip): 218,981 rows read, 597 universe rows
- 990EZ 2014 (14eofinextract990ez.zip): 234,820 rows read, 643 universe rows
- 990EZ 2015 (15eofinextractEZ.zip): 223,028 rows read, 653 universe rows
- 990EZ 2016 (16eofinextractez.zip): 230,745 rows read, 723 universe rows
- 990EZ 2017 (17eofinextractEZ.zip): 218,097 rows read, 723 universe rows
- 990EZ 2018 (18eoextractez.zip): 226,533 rows read, 753 universe rows
- 990EZ 2019 (19eoextractez.zip): 218,671 rows read, 766 universe rows
- 990EZ 2020 (20eoextractez.zip): 154,314 rows read, 530 universe rows
- 990EZ 2021 (21eoextractez.zip): 218,733 rows read, 852 universe rows
- 990EZ 2022 (22eoextractez.zip): 231,289 rows read, 972 universe rows
- 990EZ 2023 (23eoextractez.zip): 207,536 rows read, 909 universe rows
- 990EZ 2024 (24eoextract990EZ.zip): 203,699 rows read, 959 universe rows
- 990PF 2012 (12eofinextract990pf.zip): 98,948 rows read, 2,669 universe rows; fields absent this year: x_pf_grants_approved_future
- 990PF 2013 (13eofinextract990pf.zip): 100,484 rows read, 2,753 universe rows
- 990PF 2014 (14eofinextract990pf.zip): 101,381 rows read, 2,902 universe rows
- 990PF 2015 (15eofinextract990pf.zip): 103,000 rows read, 2,934 universe rows
- 990PF 2016 (16eofinextract990pf.zip): 105,239 rows read, 3,128 universe rows
- 990PF 2020 (20eoextract990pf.zip): 91,473 rows read, 3,021 universe rows
- 990PF 2021 (21eoextract990pf.zip): 125,312 rows read, 4,414 universe rows
- 990PF 2022 (22eoextract990pf.zip): 115,024 rows read, 4,266 universe rows
- 990PF 2023 (23eoextract990pf.zip): 120,350 rows read, 4,588 universe rows
- 990PF 2024 (24eoextract990pf.zip): 119,059 rows read, 4,795 universe rows
- SOI: 77,152 rows, 9,329 EINs; 0 older-processing-year copies dropped; 0 rows whose copies disagree on total_revenue
- NCCS 2009: 48,857 rows read, 272 universe 990 rows
- NCCS 2010: 184,553 rows read, 913 universe 990 rows
- NCCS 2011: 241,595 rows read, 1,249 universe 990 rows
- NCCS 2012: 273,429 rows read, 1,453 universe 990 rows
- NCCS 2013: 303,225 rows read, 1,609 universe 990 rows
- NCCS 2014: 335,066 rows read, 1,745 universe 990 rows
- NCCS 2015: 358,459 rows read, 1,921 universe 990 rows
- NCCS 2016: 374,252 rows read, 2,000 universe 990 rows
- NCCS 2017: 391,170 rows read, 2,115 universe 990 rows
- NCCS 2018: 406,376 rows read, 2,207 universe 990 rows
- NCCS 2019: 436,217 rows read, 2,343 universe 990 rows
- NCCS 2020: 485,459 rows read, 2,616 universe 990 rows
- NCCS 2021: 491,127 rows read, 2,502 universe 990 rows
- NCCS 2022: 131,588 rows read, 340 universe 990 rows
- NCCS: 22,080 rows staged, 3,038 EINs, tax years 2010-2022; period from SOI match 22,063, from IRS index 17; dropped 883 with no period; 307 EIN-years had >1 return (kept the latest OBJECT_ID)
- NCCS total_revenue equals SOI total_revenue on 99.1% of 22,063 matched rows
- wrote 99,232 rows to interim/stage_fact_org_financials__soi.csv (SOI 77,152; NCCS 22,080)
- duplicate (ein, tax_period_end, return_type, source_id): 0
- Calvary total_revenue QC: bulk_irs_soi_extract TY2020 3,851,984 OK; bulk_irs_soi_extract TY2021 8,867,250 OK; bulk_nccs_efile TY2020 3,851,984 OK; bulk_nccs_efile TY2021 not present
- 990-PF SOI TAX_YR equals derived tax_year on 100.0% of rows
- rows by fiscal_year (period-end year) x return_type / source:
```
source_id   irs_soi_extract              nccs_efile    All
return_type             990 990EZ  990PF        990       
fiscal_year                                               
2002                      0     0      1          0      1
2003                      1     0      1          0      2
2004                      0     0      1          0      1
2005                      1     0      1          0      2
2006                      0     0      1          0      1
2007                      0     2      3          0      5
2008                      2    12      7          0     21
2009                      4    30     14          0     48
2010                    175    92     84          5    356
2011                   1833   512   2406        808   5559
2012                   2176   611   2754       1355   6896
2013                   2229   609   2829       1524   7191
2014                   2245   655   2972       1625   7497
2015                   2312   694   3038       1818   7862
2016                   2389   729    310       1932   5360
2017                   2439   737     23       2033   5232
2018                   2512   751    110       2134   5507
2019                   2570   788   3460       2254   9072
2020                   2591   830   3903       2484   9808
2021                   2698   818   4204       2626  10346
2022                   2785   855   4434       1476   9550
2023                   2790   857   4559          6   8212
2024                    266    82    355          0    703
All                   32018  9664  35470      22080  99232
```
- coverage, bulk_irs_soi_extract (EINs with >=1 row / universe EINs; org-years; median years per covered org):
  - calvary: 1/1; 13; 13
  - calvary_known_funders: 81/85; 837; 10
  - core_peers: 18/18; 235; 13
  - daf_sponsors: 15/15; 184; 13
  - dc_sector: 524/1,024; 4,620; 11
  - dmv_funders: 5,744/7,705; 44,487; 10
  - dmv_sector: 1,939/4,890; 15,524; 9
  - national_women: 1,280/2,452; 12,487; 13
  - size_matched: 555/557; 6,773; 13
- coverage, bulk_nccs_efile (EINs with >=1 row / universe EINs; org-years; median years per covered org):
  - calvary: 1/1; 7; 7
  - calvary_known_funders: 31/85; 247; 9
  - core_peers: 18/18; 172; 10
  - daf_sponsors: 15/15; 84; 6
  - dc_sector: 370/1,024; 2,550; 7
  - dmv_funders: 650/7,705; 4,046; 6
  - dmv_sector: 1,139/4,890; 7,856; 7
  - national_women: 892/2,452; 7,277; 10
  - size_matched: 549/557; 4,772; 10

### 2026-10-10 13:37 — 30_fetch_xml: progress
- pass 1: 8,000/31,469 done in 7.3 min (18.4/s); 611 MB on disk for done files; ok 8,000, not_found 0, error 0

### 2026-10-10 13:37 — 43_web_calvary
- support page: 98 organizations (3 flagged in-kind); Phase 1 PDF had 98 (11 truncated). Names absent from the PDF parse: 11
- truncated names recovered: Morris, Mann -> Morris, Manning & Martin, LLP; Nelson Mulli -> Nelson Mullins; NFP Golden & -> NFP Golden & Cohen; Robert Charle -> Robert Charles Lesser Co.; Sapodilla's C -> Sapodilla's Caribbean Restaurant and Catering; Saul Ewing A -> Saul Ewing Arnstein & Lehr LLP; Southern Com -> Southern Company; The Brand Gu -> The Brand Guild; The Menkiti G -> The Menkiti Group; United Bank -> United Bank; Women's Ene -> Women's Energy Resource Council
- PDFs seen: 98 (financials page links + WP media library + off-site search); kept as new: 22: 2015-07-Corporate-Partner-Program-packet.pdf [funder_list, ok]; CWS-Audited-Financial-Statements-2014.pdf [audit, ok]; CWS-Form-990-2014.pdf [form_990, ok]; CWS-form-990-2013.pdf [form_990, ok]; Corporate-Partners-Program-packet.pdf [funder_list, ok]; Corporate-Partners-Program-packet_11-11-2014.pdf [funder_list, ok]; Corporate-Partners-Program-packet_11-13-2014.pdf [funder_list, ok]; FY2013-Annual-Report-simple-version-FINAL.pdf [annual_report, ok]; What-Do-Corporate-Partners-Do_combined.pdf [funder_list, ok]; audited-statements-2013.pdf [audit, ok]; Calvary-Womens-Services-2014-Annual-Report.pdf [annual_report, ok]; 2017-Hope-Awards-Sponsorship-Opportunities.pdf [funder_list, ok]; Step-Up-DC-2016-Year-End-Report.pdf [funder_list, ok]; 2019-02-04-Calvary-Annual-Design.pdf [annual_report, ok]; Calvary-Womens-Services-FY18-Annual-Report.pdf [annual_report, ok]; CWS-Corporate-Partners-Program-Overview.pdf [funder_list, ok]; Hope-Awards-Sponsors.pdf [funder_list, ok]; 2024-Corporate-Partners-Program-Opportunities_CWS.pdf [funder_list, ok]; 2025-Hope-Gala-Sponsorship_CWS-2.pdf [funder_list, ok]; 2025-Hope-Gala-Sponsorship_CWS-2.pdf [funder_list, duplicate_of_web:https://www.calvaryservices.org/wp-content/uploads/2025/02/2025-Hope-Gala-Sponsorship_CWS-2.pdf]; Calvary-Newsletter-02_25.pdf [funder_list, ok]; 521307706_2022_25813620221_A133.pdf [other, ok; found by cal_audit_fy24]
- off-site search hits: 104 results; Calvary PDFs kept: 1; rejected: Calvary-Independent-Auditors-Report.pdf (cal_audit_fy25: not a Calvary Women's Services document)
- annual-report donors: 74 org rows; named lists/mentions 88 rows; individual band-count rows 3; Calvary-Womens-Services-2014-Annual-Report.pdf: 74 org donor entries, 182 individual entries (counted only); 2017-Hope-Awards-Sponsorship-Opportunities.pdf [Hope Awards Dinner: companies that have sponsored (cumulative)]: 41; Step-Up-DC-2016-Year-End-Report.pdf [Step Up DC supporters ('supported the program this year')]: 5; 2025-Hope-Gala-Sponsorship_CWS-2.pdf [Hope Gala: Past Event Sponsors (cumulative)]: 39
- new audits: 315 financial/note rows, 4 SEFA rows; CWS-Audited-Financial-Statements-2014.pdf: no SEFA in the PDF; 521307706_2022_25813620221_A133.pdf: SEFA p29 4 programs sum 4,067,718 vs printed total 4,067,718
- this run: Tavily search 0, extract 0, HTTP GET 0, cache hits 41; cumulative (manifest): search 11/300, extract 0/200, HTTP 30

### 2026-10-10 13:38 — 43_web_calvary
- support page: 98 organizations (3 flagged in-kind); Phase 1 PDF had 98 (11 truncated). Names absent from the PDF parse: 11
- truncated names recovered: Morris, Mann -> Morris, Manning & Martin, LLP; Nelson Mulli -> Nelson Mullins; NFP Golden & -> NFP Golden & Cohen; Robert Charle -> Robert Charles Lesser Co.; Sapodilla's C -> Sapodilla's Caribbean Restaurant and Catering; Saul Ewing A -> Saul Ewing Arnstein & Lehr LLP; Southern Com -> Southern Company; The Brand Gu -> The Brand Guild; The Menkiti G -> The Menkiti Group; United Bank -> United Bank; Women's Ene -> Women's Energy Resource Council
- PDFs seen: 98 (financials page links + WP media library + off-site search); kept as new: 22: 2015-07-Corporate-Partner-Program-packet.pdf [funder_list, ok]; CWS-Audited-Financial-Statements-2014.pdf [audit, ok]; CWS-Form-990-2014.pdf [form_990, ok]; CWS-form-990-2013.pdf [form_990, ok]; Corporate-Partners-Program-packet.pdf [funder_list, ok]; Corporate-Partners-Program-packet_11-11-2014.pdf [funder_list, ok]; Corporate-Partners-Program-packet_11-13-2014.pdf [funder_list, ok]; FY2013-Annual-Report-simple-version-FINAL.pdf [annual_report, ok]; What-Do-Corporate-Partners-Do_combined.pdf [funder_list, ok]; audited-statements-2013.pdf [audit, ok]; Calvary-Womens-Services-2014-Annual-Report.pdf [annual_report, ok]; 2017-Hope-Awards-Sponsorship-Opportunities.pdf [funder_list, ok]; Step-Up-DC-2016-Year-End-Report.pdf [funder_list, ok]; 2019-02-04-Calvary-Annual-Design.pdf [annual_report, ok]; Calvary-Womens-Services-FY18-Annual-Report.pdf [annual_report, ok]; CWS-Corporate-Partners-Program-Overview.pdf [funder_list, ok]; Hope-Awards-Sponsors.pdf [funder_list, ok]; 2024-Corporate-Partners-Program-Opportunities_CWS.pdf [funder_list, ok]; 2025-Hope-Gala-Sponsorship_CWS-2.pdf [funder_list, ok]; 2025-Hope-Gala-Sponsorship_CWS-2.pdf [funder_list, duplicate_of_web:https://www.calvaryservices.org/wp-content/uploads/2025/02/2025-Hope-Gala-Sponsorship_CWS-2.pdf]; Calvary-Newsletter-02_25.pdf [funder_list, ok]; 521307706_2022_25813620221_A133.pdf [other, ok; found by cal_audit_fy24]
- off-site search hits: 104 results; Calvary PDFs kept: 1; rejected: Calvary-Independent-Auditors-Report.pdf (cal_audit_fy25: not a Calvary Women's Services document)
- annual-report donors: 72 org rows; named lists/mentions 87 rows; individual band-count rows 3; Calvary-Womens-Services-2014-Annual-Report.pdf: 72 org donor entries, 182 individual entries (counted only); 2017-Hope-Awards-Sponsorship-Opportunities.pdf [Hope Awards Dinner: companies that have sponsored (cumulative)]: 41; Step-Up-DC-2016-Year-End-Report.pdf [Step Up DC supporters ('supported the program this year')]: 4; 2025-Hope-Gala-Sponsorship_CWS-2.pdf [Hope Gala: Past Event Sponsors (cumulative)]: 39
- new audits: 315 financial/note rows, 4 SEFA rows; CWS-Audited-Financial-Statements-2014.pdf: no SEFA in the PDF; 521307706_2022_25813620221_A133.pdf: SEFA p29 4 programs sum 4,067,718 vs printed total 4,067,718
- this run: Tavily search 0, extract 0, HTTP GET 0, cache hits 41; cumulative (manifest): search 11/300, extract 0/200, HTTP 30

### 2026-10-10 13:38 — 38_parse_hud_counts
- wrote interim/stage_homeless_counts__hud.csv: 49,393 rows ({'bulk_hud_ahar_pit_hic': 48224, 'doc_hud_hic_dc500': 428, 'doc_mwcog_pit': 741}); PIT 39,029, HIC by CoC 9,195, PopSub 428, MWCOG 741
- wrote interim/stage_hic_projects__hud.csv: 1,257 rows (2022: 332, 2023: 292, 2024: 323, 2025: 310)
- HIC project PDFs: provider and facility names are truncated in the PDF itself (fixed-width report cells; same text in pdfplumber chars, pypdf and pdftotext); kept as printed. 'units' = family units (HIC reports units only for households with children). target_population is derived from the bed columns (household type, plus youth/veterans/chronic when all beds are dedicated) and set to single_women / women_with_children only when the provider or project name says women (basis in x_target_population_basis). x_women_focused_org = core peer tier 1a or Calvary; x_dv_focused_org = tier 1b (config/core_peers.csv).
- PIT by CoC (raw/hud/20261010T123731_huduser_2007-2025-PIT-Counts-by-CoC.xlsb): sheets 2007-2025; 39,029 rows for 8 CoCs; unparsed column names 216 (e.g. ['Overall Homeless - Under 18', 'Overall Homeless - Age 18 to 24', 'Overall Homeless - Over 24']); CoC-years absent: none
- partial unsheltered counts (Count Types): MD-601 2021; VA-602 2021
- workbook has no gender columns in any year (only age, race/ethnicity, household and subpopulation splits); DC gender comes from PopSub 2024 and the MWCOG 2025 DC narrative
- HIC by CoC (raw/hud/20261010T123733_huduser_2007-2025-HIC-Counts-by-CoC.xlsx): sheets 2007-2025; 9,195 rows; unparsed columns 9 (['HMIS Participation Rate (ES,TH) (non-numeric)', 'ES HMIS Participation Rate (non-numeric)', 'Total TH Beds for Households with only Children (non-numeric)', 'HMIS Participation Rate for Year-Round Beds (SH) (non-numeric)']); same-measure columns with different values kept as '__alt': 0
- PopSub DC-500 2024 (raw/hud/20261010T123749_hudx_CoC_PopSub_DC-500_2024.pdf): 232 rows; total persons 5616; women 2167
- PopSub DC-500 2025 (raw/hud/20261010T123750_hudx_CoC_PopSub_DC-500_2025.pdf): 196 rows; total persons 5138; women n/a
- MWCOG 2023 report (raw/hud/20261010T123754_mwcog_homelessness_metro_washington_2023_PIT.pdf): 548 table cells kept
- MWCOG 2024 report (raw/hud/20261010T123753_mwcog_homelessness_metro_washington_2024_PIT.pdf): 504 table cells kept
- MWCOG 2025 report (raw/hud/20261010T123752_mwcog_homelessness_metro_washington_2025_PIT.pdf): 520 table cells kept
- MWCOG 2026 report (raw/hud/20261010T123751_mwcog_homelessness_metro_washington_2026_PIT.pdf): 531 table cells kept
- MWCOG: 2103 cells parsed across reports -> 741 after keeping the latest report per jurisdiction/year/measure/population; values revised between reports: 38 (e.g. Prince William County, VA 2022 all: 241 (rpt 2023) -> 282 (rpt 2024); Prince William County, VA 2021 all: 282 (rpt 2023) -> 326 (rpt 2024); Prince William County, VA 2020 all: 326 (rpt 2023) -> 277 (rpt 2024); COG region 2023 households_without_children: 5901 (rpt 2023) -> 5755 (rpt 2024)); same report, two tables disagree (earlier page kept): 17 (District of Columbia 2020 households_with_only_children rpt 2023: p68 12 vs p25 11; Frederick City & County, MD 2021 households_with_only_children rpt 2023: p68 5 vs p25 0; COG region 2020 households_with_only_children rpt 2023: p69 13 vs p25 12; City of Alexandria, VA 2020 all rpt 2023: p68 198 vs p17 207)
- skipped tables (did not parse reliably): none; source-inconsistent columns are kept with confidence medium and an x_note
- not parsed: figures/charts (demographic profiles, income, gender charts), Table 3 population shares, Table 13/14 shelter status, TAY tables, Table 16 bed inventory, Table 17 formerly homeless in PH, Appendix B narrative percentages except the 2025 DC gender-of-adults table
- HIC provider names (cleaned, distinct): 105; matched 42 (40%); methods {'unmatched': 63, 'fuzzy_token_set': 11, 'exact_norm_name': 29, 'manual_known_ein': 2}; government providers (no EIN expected) 7; beds at matched providers 60,873 of 133,181 (46%)
- fuzzy matches: Access Housing -> 521918702 (100.0); Access Housing INC (AHI) (Agency) -> 521918702 (100.0); Catholic Charities -> 530196524 (100.0); Catholic Charities (Agency) -> 530196524 (100.0); Covenant House Washington -> 133537709 (100.0); Covenant House Washington (CHW)(Age -> 133537709 (100.0); East River Family Strengthening Collabor -> 522277915 (100.0); Edgewood-Brookland Family Support Col -> 522246995 (100.0); Edgewood/Brookland Family Support Col -> 522246995 (100.0); Far Southeast Family Strengthening Colla -> 522117070 (100.0); Georgia Avenue Family Support Collabor -> 522349433 (100.0); Operation Renewed Hope -> 453848293 (100.0); Survivors & Advocates for Empowerment -> 412226446 (100.0)
- unmatched nonprofit providers (not in dc_sector/dmv_sector/core_peers by name): 801 East Collaborative; Bradley & Associates; CCDC; CORE DC; Casa Ruby; Church of Epiphany; Church of the Epiphany; Collaborative Solutions for Communities; Communities Helping & Empowering Pat; Communities Helping and Empowering P; Community Solutions; Cornerstone Community; Dawn Deaf; Deaf Dawn; East of the River Family Support Collabor; Echelon Community Services; Far Southeast Family Support Collaborati; Healthy Babies; Healthy Babies Project; Hillcrest Children & Family Center; Hope and a Home; Housing Up; Institute for Emotional Regulation; Jaydot; Joseph's House; Jubilee Housing; KBEC Group, Inc; KBEC Group, Inc.; KC Community Services; Latin American Youth Center; MBI Health Services; Maximus; Metropolitan Education Solutions; Metropolitan Educational Solutions; North Capitol Collaborative Inc.; North Capitol Family Support Collaborati; Positive Kinship Bonding; SLS; SMYAL; Salvation Army; Sasha Bruce Youthwork; Sasha Bruce Youthworks; So Others Might Eat; Spring Leaf; St. Aloysius Roman Catholic Church; St. John's Community Community Servic; St. John's Community Services; Supporting & Mentoring Youth Advocate; Temple Micah; Temple Sinai; The Community Builders and Emory Bea; The Institute for Emotional Regulation, L; The Salvation Army; U.S. Vets; US Veterans Initiative; Wheeler Creek
- matcher: norm_name exact, then rapidfuzz token_set_ratio >= 92 after expanding a truncated last token (raw names >= 30 chars) to the candidate token it prefixes, with guards (candidate >= 2 tokens; shorter token set contained in the longer; token-count ratio >= 0.5) and a reviewed reject list; TCP by known EIN
- PopSub 2024 gender rows sum 5616 vs total 5616: pass
- MWCOG 2023 p16 'People Experiencing Literal Homelessness by Jurisdiction, 2022 - 2023': pass (2 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p17 'People Experiencing Literal Homelessness by Jurisdiction, 2019-2023': pass (5 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p22 '2023 Persons In Families Experiencing Homelessness by Jurisdiction': pass (4 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p23 'Change In Persons In Families Experiencing Homelessness by Jurisdictio': pass (5 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p25 'Households With Only Children Under Age 18 By Jurisdiction, 2020 - 202': pass (4 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p41 'Comparison of Unsheltered Single Adults By Jurisdiction, 2019 – 2023': pass (5 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p45 'Single Adults Experiencing Chronic Homelessness by Jurisdiction, 2019 ': pass (5 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p51 'Veterans Experiencing Homelessness By Jurisdiction, 2019 - 2023': pass (5 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 pp[68, 69] 'People Experiencing Literal Homelessness by Jurisdiction, 20': kept with flags: 14/20 columns do not add up in the source (2022 households_without_children 5,307 vs 5,273; 2022 households_with_adults_and_children 2,329 vs 2,322; 2022 all 7,646 vs 7,605); 2 jurisdiction-years whose household columns do not add up
- MWCOG 2024 p16 'People Experiencing Literal Homelessness by Jurisdiction, 2023 - 2024': pass (2 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p17 'People Experiencing Literal Homelessness by Jurisdiction, 2020-2024*': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p22 '2024 Persons in Families Experiencing Homelessness by Jurisdiction': pass (4 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p23 'Change in Persons in Families Experiencing Homelessness by Jurisdictio': kept with flags: 1/5 columns do not add up in the source (2020 persons_in_families 3,690 vs 3,760)
- MWCOG 2024 p29 'Households With Only Children Under Age 18 By Jurisdiction, 2020 - 202': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p49 'Unsheltered Single Adults Experiencing Homelessness by Jurisdiction, 2': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p52 'Single Adults Experiencing Chronic Homelessness by Jurisdiction, 2020 ': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p60 'Veterans Experiencing Homelessness by Jurisdiction, 2020 - 2024': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 pp[75, 76] 'People Experiencing Literal Homelessness by Jurisdiction, 20': kept with flags: 9/20 columns do not add up in the source (2022 households_without_children 5,154 vs 5,120; 2022 households_with_adults_and_children 2,272 vs 2,265; 2022 all 7,422 vs 7,395); 2 jurisdiction-years whose household columns do not add up
- MWCOG 2025 p17 'People Experiencing Literal Homelessness by Jurisdiction, 2024 - 2025': pass (2 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p18 'People Experiencing Literal Homelessness by Jurisdiction, 2021-2025*': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p22 '2025 Persons in Families Experiencing Homelessness by Jurisdiction': pass (4 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p23 'Change in Persons in Families Experiencing Homelessness by Jurisdictio': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p29 'Households With Only Children Under Age 18 By Jurisdiction, 2021 - 202': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p48 'Comparison of Unsheltered Single Adults by Jurisdiction, 2021 - 2025': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p51 'Single Adults Experiencing Chronic Homelessness by Jurisdiction, 2021 ': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p59 'Veterans Experiencing Homelessness by Jurisdiction, 2021 - 2025': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 pp[73, 74] 'People Experiencing Literal Homelessness by Jurisdiction, 20': pass (20 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p18 'People Experiencing Literal Homelessness by Jurisdiction, 2025-2026': pass (2 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p19 'People Experiencing Literal Homelessness by Jurisdiction, 2019-2026': pass (8 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p24 '2026 Persons in Families Experiencing Homelessness by Jurisdiction': pass (4 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p25 'Change in Persons in Families Experiencing Homelessness by Jurisdictio': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p32 'Households With Only Children Under Age 18 By Jurisdiction, 2022 – 202': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p50 'Comparison of Unsheltered Single Adults by Jurisdiction, 2022 – 2026': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p54 'Single Adults Experiencing Chronic Homelessness by Jurisdiction, 2022 ': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p59 'Veterans Experiencing Homelessness by Jurisdiction, 2022 – 2026': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 pp[79, 80] 'People Experiencing Literal Homelessness by Jurisdiction, 20': pass (20 year/measure columns, 8 jurisdictions + total)
- MWCOG total persons vs HUD PIT overall, CoC-years that differ: 9: MD-600 2020: MWCOG 453 vs HUD 466; MD-600 2021: MWCOG 537 vs HUD 535; MD-600 2022: MWCOG 571 vs HUD 533; MD-600 2023: MWCOG 659 vs HUD 595; MD-600 2024: MWCOG 658 vs HUD 650; MD-600 2025: MWCOG 608 vs HUD 588; VA-602 2019: MWCOG 169 vs HUD 167; VA-604 2019: MWCOG 277 vs HUD 280; VA-604 2025: MWCOG 392 vs HUD 393
- DC-500 MWCOG vs HUD by year: 2019 6,521/6521, 2020 6,380/6380, 2021 5,111/5111, 2022 4,410/4410, 2023 4,922/4922, 2024 5,616/5616, 2025 5,138/5138, 2026 5,363/n/a
- stage_homeless_counts duplicate keys (coc, jurisdiction, year, measure, population, source): 0
- DC-500 2025 recon values: pit_overall 5138 (exp 5138) pass; pit_sheltered_es 3275 (exp 3275) pass; pit_sheltered_th 1065 (exp 1065) pass; pit_unsheltered 798 (exp 798) pass; hic_beds_year_round__es_th_sh 4965 (exp 4965) pass; hic_beds_year_round__th 1385 (exp 1385) pass; hic_beds_year_round__psh 12696 (exp 12696) pass; hic_beds_year_round__rrh 6012 (exp 6012) pass
- HIC projects 2022 ES: 43 projects; total beds 5,159 vs Total row 5159; year-round 4,795 vs summary p1 4795 vs CoC workbook 4795: pass
- HIC projects 2022 SH: 1 projects; total beds 20 vs Total row 20; year-round 20 vs summary p1 20 vs CoC workbook 20: pass
- HIC projects 2022 TH: 71 projects; total beds 1,783 vs Total row 1783; year-round 1,783 vs summary p1 1783 vs CoC workbook 1783: pass
- HIC projects 2022 PSH: 148 projects; total beds 14,467 vs Total row 14467; year-round 14,467 vs summary p1 14467 vs CoC workbook 14467: pass
- HIC projects 2022 RRH: 34 projects; total beds 7,193 vs Total row 7193; year-round 7,193 vs summary p1 7193 vs CoC workbook 7193: pass
- HIC projects 2022 OPH: 35 projects; total beds 6,498 vs Total row 6498; year-round 6,498 vs summary p1 6498 vs CoC workbook 6498: pass
- HIC projects 2023 ES: 38 projects; total beds 4,026 vs Total row 4026; year-round 3,720 vs summary p1 3720 vs CoC workbook 3720: pass
- HIC projects 2023 SH: 1 projects; total beds 20 vs Total row 20; year-round 20 vs summary p1 20 vs CoC workbook 20: pass
- HIC projects 2023 TH: 65 projects; total beds 1,476 vs Total row 1476; year-round 1,476 vs summary p1 1476 vs CoC workbook 1476: pass
- HIC projects 2023 PSH: 138 projects; total beds 15,349 vs Total row 15349; year-round 15,349 vs summary p1 15349 vs CoC workbook 15349: pass
- HIC projects 2023 RRH: 35 projects; total beds 9,206 vs Total row 9206; year-round 9,206 vs summary p1 9206 vs CoC workbook 9206: pass
- HIC projects 2023 OPH: 15 projects; total beds 5,381 vs Total row 5381; year-round 5,381 vs summary p1 5381 vs CoC workbook 5381: pass
- HIC projects 2024 ES: 46 projects; total beds 4,000 vs Total row 4000; year-round 3,505 vs summary p1 3505 vs CoC workbook 3505: pass
- HIC projects 2024 SH: 1 projects; total beds 20 vs Total row 20; year-round 20 vs summary p1 20 vs CoC workbook 20: pass
- HIC projects 2024 TH: 70 projects; total beds 1,693 vs Total row 1693; year-round 1,693 vs summary p1 1693 vs CoC workbook 1693: pass
- HIC projects 2024 PSH: 154 projects; total beds 11,856 vs Total row 11856; year-round 11,856 vs summary p1 11856 vs CoC workbook 11856: pass
- HIC projects 2024 RRH: 33 projects; total beds 10,156 vs Total row 10156; year-round 10,156 vs summary p1 10156 vs CoC workbook 10156: pass
- HIC projects 2024 OPH: 19 projects; total beds 5,842 vs Total row 5842; year-round 5,842 vs summary p1 5842 vs CoC workbook 5842: pass
- HIC projects 2025 ES: 45 projects; total beds 3,954 vs Total row 3954; year-round 3,580 vs summary p1 3580 vs CoC workbook 3580: pass
- HIC projects 2025 TH: 64 projects; total beds 1,385 vs Total row 1385; year-round 1,385 vs summary p1 1385 vs CoC workbook 1385: pass
- HIC projects 2025 PSH: 159 projects; total beds 12,696 vs Total row 12696; year-round 12,696 vs summary p1 12696 vs CoC workbook 12696: pass
- HIC projects 2025 RRH: 26 projects; total beds 6,012 vs Total row 6012; year-round 6,012 vs summary p1 6012 vs CoC workbook 6012: pass
- HIC projects 2025 OPH: 16 projects; total beds 4,989 vs Total row 4989; year-round 4,989 vs summary p1 4989 vs CoC workbook 4989: pass
- stage_hic_projects duplicate keys (year, type, page, seq): 0
- Calvary HIC 2025 rows pass (7 projects, 124 beds); 2024 Sisters Rise PSH [24] (exp [24])

### 2026-10-10 13:39 — 30_fetch_xml: progress
- pass 1: 10,000/31,469 done in 9.0 min (18.5/s); 768 MB on disk for done files; ok 10,000, not_found 0, error 0

### 2026-10-10 13:41 — 30_fetch_xml: progress
- pass 1: 12,000/31,469 done in 10.8 min (18.6/s); 901 MB on disk for done files; ok 12,000, not_found 0, error 0

### 2026-10-10 13:41 — 44_web_peers_funders (searches only)
- hits 603
- this run: Tavily search 72, extract 0, HTTP GET 0, cache hits 0; cumulative (manifest): search 83/300, extract 0/200, HTTP 30

### 2026-10-10 13:42 — 35_pull_grantsgov: opportunities
- universe posted+forecasted 1467; candidates 531 (local cfdaList 3, cfda key 3, keyword search 530, title regex 51); fetched 1 (reused 530 saved responses); fetch failures 0; dropped by local filter 245
- interim/stage_fact_opportunities__grantsgov.csv: 286 rows (173 posted, 113 forecasted); duplicate ids 0
- keyword_hits counts: {"homelessness": 6, "housing": 17, "domestic violence": 5, "victim services": 2, "women": 59, "substance use": 47, "workforce": 98, "reentry": 5, "veterans": 19, "aging": 77}
- target-ALN rows: 3; nonprofit-eligible (12/13/25/99): 263
- manifest raw/grantsgov/20261010T134203_pull35_manifest.json

### 2026-10-10 13:42 — 30_fetch_xml: progress
- pass 1: 14,000/31,469 done in 12.4 min (18.8/s); 1,119 MB on disk for done files; ok 14,000, not_found 0, error 0

### 2026-10-10 13:44 — 44_web_peers_funders (searches only)
- hits 757
- this run: Tavily search 21, extract 0, HTTP GET 0, cache hits 69; cumulative (manifest): search 104/300, extract 0/200, HTTP 30

### 2026-10-10 13:44 — 30_fetch_xml: progress
- pass 1: 16,000/31,469 done in 14.4 min (18.5/s); 1,241 MB on disk for done files; ok 16,000, not_found 0, error 0

### 2026-10-10 13:45 — 37_parse_dc_budget: DC budget lines and policy events
- interim/stage_dc_budget_lines__dc.csv: 6,185 rows (Counter({'approved': 3682, 'actual': 2471, 'proposed': 32})); in-scope program/agency rows 933; duplicate keys 0
- interim/stage_fact_policy_events__dc.csv: 306 rows; by kind {'change_table_FO0-5': 8, 'change_table_HY0-5': 9, 'change_table_JA0-5': 25, 'yoy_approved_change': 161, 'bsa_subtitle': 25, 'fy2025_change_narrative': 21, 'committee_report_item': 22, 'committee_report_variance': 6, 'change_table_RM0-5': 1, 'change_table_DB0-5': 1, 'council_adjustments_chart_fy2027': 27}; by type {'budget_proposed': 41, 'budget_enacted': 161, 'budget_revised': 75, 'policy_change': 26, 'other': 1, 'program_launch': 2}
- parsed tables: FY2024 JA0 30-PBB (2024_JA0_ja_dhs_tables_2024j.pdf): 62 lines; FY2024 FO0 30-PBB (024_FO0_fo_vsjg_tables_2024j.pdf): 21 lines; FY2024 RM0 30-PBB (2024_RM0_rm_dbh_tables_2024j.pdf): 128 lines; FY2024 DB0 30-PBB (024_DB0_db_dhcd_tables_2024j.pdf): 44 lines; FY2024 HY0 30-PBB (2024_HY0_hy_has_tables_2024j.pdf): 16 lines; FY2024 CF0 30-PBB (2024_CF0_cf_des_tables_2024j.pdf): 69 lines; FY2024 HG0 30-PBB (24_HG0_hg_dmhhs_tables_2024j.pdf): 9 lines; FY2025 JA0 30-PBB (2025_JA0_ja_dhs_tables_2025j.pdf): 61 lines; FY2025 FO0 30-PBB (25_FO0_fo_ovsjg_tables_2025j.pdf): 28 lines; FY2025 RM0 30-PBB (2025_RM0_rm_dbh_tables_2025j.pdf): 87 lines; FY2025 DB0 30-PBB (025_DB0_db_dhcd_tables_2025j.pdf): 36 lines; FY2025 HY0 30-PBB (2025_HY0_hy_hap_tables_2025j.pdf): 7 lines; FY2025 CF0 30-PBB (025_CF0_cf_does_tables_2025j.pdf): 62 lines; FY2025 HG0 30-PBB (25_HG0_hg_dmhhs_tables_2025j.pdf): 8 lines; FY2026 JA0 Table JA0-4 (026_JA0_ja_dhs_chapter_2026o.pdf): 57 lines; FY2026 FO0 Table FO0-4 (26_FO0_fo_vsjg_chapter_2026o.pdf): 26 lines; FY2026 RM0 Table RM0-4 (026_RM0_rm_dbh_chapter_2026o.pdf): 83 lines; FY2026 DB0 Table DB0-4 (26_DB0_db_dhcd_chapter_2026o.pdf): 36 lines; FY2026 HY0 Table HY0-4 (026_HY0_hy_has_chapter_2026o.pdf): 7 lines; FY2026 CF0 Table CF0-4 (26_CF0_cf_does_chapter_2026o.pdf): 61 lines; FY2026 HG0 Table HG0-4 (6_HG0_hg_dmhhs_chapter_2026o.pdf): 6 lines; FY2027 JA0 30-PBB (7_JA0_ja0_dhs_tables_2027a_0.pdf): 57 lines; FY2027 FO0 30-PBB (FO0_fo0_ovsjg_tables_2027a_0.pdf): 26 lines; FY2027 RM0 30-PBB (7_RM0_rm0_dbh_tables_2027a_0.pdf): 80 lines; FY2027 DB0 30-PBB (_DB0_db0_dhcd_tables_2027a_0.pdf): 36 lines; FY2027 HY0 30-PBB (7_HY0_hy0_hap_tables_2027a_0.pdf): 7 lines; FY2027 CF0 30-PBB (_CF0_cf0_does_tables_2027a_0.pdf): 61 lines; FY2027 HG0 30-PBB (HG0_hg0_dmhhs_tables_2027a_0.pdf): 7 lines
- change items: FY2024 JA0 Table JA0-5: 29 change lines, 7 in scope; FY2024 FO0 Table FO0-5: 14 change lines, 3 in scope; FY2024 RM0 Table RM0-5: 25 change lines, 0 in scope; FY2024 DB0 Table DB0-5: 14 change lines, 0 in scope; FY2024 HY0 Table HY0-5: 6 change lines, 6 in scope; FY2024 CF0 Table CF0-5: 16 change lines, 0 in scope; FY2024 HG0 Table HG0-5: 7 change lines, 0 in scope; FY2025 JA0 narrative change sentences (pypdfium2): 15 in scope; FY2025 FO0: chapter change text is font-garbled (amounts missing); OVSJG FY2025 changes taken from the JPS committee report; FY2025 RM0 narrative change sentences (pypdfium2): 0 in scope; FY2025 DB0 narrative change sentences (pypdfium2): 2 in scope; FY2025 HY0 narrative change sentences (pypdfium2): 4 in scope; FY2025 CF0 Table CF0-5: 20 change lines, 0 in scope; FY2025 HG0 narrative change sentences (pypdfium2): 0 in scope; FY2026 JA0 Table JA0-5: 29 change lines, 14 in scope; FY2026 FO0 Table FO0-5: 16 change lines, 4 in scope; FY2026 RM0 Table RM0-5: 27 change lines, 1 in scope; FY2026 DB0 Table DB0-5: 16 change lines, 0 in scope; FY2026 HY0 Table HY0-5: 2 change lines, 2 in scope; FY2026 CF0 Table CF0-5: 17 change lines, 0 in scope; FY2026 HG0 Table HG0-5: 4 change lines, 0 in scope; FY2027 JA0 Table JA0-5: 15 change lines, 4 in scope; FY2027 FO0 Table FO0-5: 11 change lines, 1 in scope; FY2027 RM0 Table RM0-5: 17 change lines, 0 in scope; FY2027 DB0 Table DB0-5: 15 change lines, 1 in scope; FY2027 HY0 Table HY0-5: 3 change lines, 1 in scope; FY2027 CF0 Table CF0-5: 8 change lines, 0 in scope; FY2027 HG0 Table HG0-5: 3 change lines, 0 in scope
- committee report tables: BR_FY25_Housing -> 1 in-scope proposed activity rows (markup 2024-05-09); BR_FY25_JPS -> 0 in-scope proposed activity rows (markup not printed); BR_FY26_committee_budget_report_Human-Services -> 18 in-scope proposed activity rows (markup 2025-06-24); BR_FY26_committee_budget_report_Housing -> 5 in-scope proposed activity rows (markup 2025-06-24); BR_FY26_committee_budget_report_JPS -> 2 in-scope proposed activity rows (markup not printed); BR_FY26_committee_budget_report_Health -> 0 in-scope proposed activity rows (markup 2025-06-23); BR_FY27_committee_budget_report_DRAFT-FY2027-Committee-on-Health -> 2 in-scope proposed activity rows (markup 2026-05-20); BR_FY27_committee_budget_report_FY27-Committee-on-Housing -> 4 in-scope proposed activity rows (markup not printed); BR_FY27_committee_budget_report_52226-FY2027-JPS -> 0 in-scope proposed activity rows (markup not printed)
- FY2027 Council adjustments chart: 1627 rows read, 27 in-scope events
- BSA subtitles kept: 25; curated committee-report items: 22; YoY approved-change events: 161
- tie-outs: 257 pass, 0 fail
- tie-out detail (in-scope divisions): FY2024 JA0 30-PBB p2 division 5000: sum of 23 activities vs subtotal, deltas by column [0, 0, 0, -1] ($000) -> pass | FY2024 JA0 30-PBB p3 agency total: sum of 8 division subtotals, deltas [0, -2, 0, 1] ($000) -> pass | FY2024 JA0 Table JA0-2 p2: sum of 7 fund rows vs GROSS FUNDS, deltas [-1, 0, -1, 0] ($000) -> pass | FY2024 FO0 30-PBB p1 division 4000: sum of 2 activities vs subtotal, deltas by column [0, 0, 0, -1] ($000) -> pass | FY2024 FO0 30-PBB p1 division 5000: sum of 1 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 FO0 30-PBB p1 division 6000: sum of 5 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 FO0 30-PBB p1 agency total: sum of 7 division subtotals, deltas [-2, -1, -2, 1] ($000) -> pass | FY2024 FO0 Table FO0-2 p2: sum of 5 fund rows vs GROSS FUNDS, deltas [0, 0, -1, 0] ($000) -> pass | FY2024 RM0 30-PBB p5 agency total: sum of 16 division subtotals, deltas [0, 1, 1, 0] ($000) -> pass | FY2024 RM0 Table RM0-2 p2: sum of 9 fund rows vs GROSS FUNDS, deltas [0, 1, 0, 1] ($000) -> pass | FY2024 DB0 30-PBB p2 agency total: sum of 9 division subtotals, deltas [0, 0, 0, -1] ($000) -> pass | FY2024 DB0 Table DB0-2 p2: sum of 5 fund rows vs GROSS FUNDS, deltas [1, -1, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 division 4000: sum of 1 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 division 5000: sum of 1 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 division 6000: sum of 5 activities vs subtotal, deltas by column [2, -1, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 agency total: sum of 5 division subtotals, deltas [0, 0, -1, 0] ($000) -> pass | FY2024 HY0 Table HY0-2 p1: sum of 1 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2024 CF0 30-PBB p2 division 4000: sum of 16 activities vs subtotal, deltas by column [0, 0, 0, -1] ($000) -> pass | FY2024 CF0 30-PBB p2 division 5000: sum of 3 activities vs subtotal, deltas by column [1, 0, 1, 0] ($000) -> pass | FY2024 CF0 30-PBB p2 division 6000: sum of 6 activities vs subtotal, deltas by column [1, 0, 0, 0] ($000) -> pass | FY2024 CF0 30-PBB p3 agency total: sum of 11 division subtotals, deltas [-1, 0, 0, -1] ($000) -> pass | FY2024 CF0 Table CF0-2 p2: sum of 6 fund rows vs GROSS FUNDS, deltas [1, 0, 0, 0] ($000) -> pass | FY2024 HG0 30-PBB p1 agency total: sum of 4 division subtotals, deltas [0, 0, 0, 0] ($000) -> pass | FY2024 HG0 Table HG0-2 p2: sum of 2 fund rows vs GROSS FUNDS, deltas [0, 1, 0, 0] ($000) -> pass | FY2025 JA0 30-PBB p2 division HS0030: sum of 28 activities vs subtotal, deltas by column [-2, 1, -1, 1] ($000) -> pass | FY2025 JA0 30-PBB p2 agency total: sum of 6 division subtotals, deltas [0, -1, 1, 0] ($000) -> pass | FY2025 FO0 30-PBB p1 division PS0023: sum of 2 activities vs subtotal, deltas by column [0, 0, -1, 0] ($000) -> pass | FY2025 FO0 30-PBB p2 agency total: sum of 12 division subtotals, deltas [-1, -2, 1, 0] ($000) -> pass | FY2025 RM0 30-PBB p3 agency total: sum of 13 division subtotals, deltas [1, 1, 0, 1] ($000) -> pass | FY2025 DB0 30-PBB p2 agency total: sum of 6 division subtotals, deltas [0, 1, 1, 0] ($000) -> pass | FY2025 HY0 30-PBB p1 division EC0039: sum of 5 activities vs subtotal, deltas by column [0, -1, 0, 0] ($000) -> pass | FY2025 HY0 30-PBB p1 agency total: sum of 1 division subtotals, deltas [0, 0, 0, 0] ($000) -> pass | FY2025 CF0 30-PBB p3 agency total: sum of 10 division subtotals, deltas [0, -1, 0, -1] ($000) -> pass | FY2025 CF0 Table CF0-2 p2: sum of 6 fund rows vs GROSS FUNDS, deltas [0, -1, 0, 0] ($000) -> pass | FY2025 HG0 30-PBB p1 agency total: sum of 3 division subtotals, deltas [0, 0, 0, 1] ($000) -> pass | FY2026 JA0 Table JA0-4 p5 division HS0030: sum of 28 activities vs subtotal, deltas [1, -2, 1, -1] ($000) -> pass | FY2026 JA0 Table JA0-4 p5 agency total: sum of 5 divisions, deltas [-1, -1, 0, 0] ($000) -> pass | FY2026 JA0 Table JA0-2 p2: sum of 7 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 FO0 Table FO0-4 p4 division PS0023: sum of 2 activities vs subtotal, deltas [0, 1, 0, 0] ($000) -> pass | FY2026 FO0 Table FO0-4 p4 agency total: sum of 11 divisions, deltas [-2, 0, 0, 0] ($000) -> pass | FY2026 FO0 Table FO0-2 p2: sum of 4 fund rows vs GROSS FUNDS, deltas [-1, 0, 0, 0] ($000) -> pass | FY2026 RM0 Table RM0-4 p7 agency total: sum of 13 divisions, deltas [1, 1, 2, 0] ($000) -> pass | FY2026 RM0 Table RM0-2 p2: sum of 8 fund rows vs GROSS FUNDS, deltas [1, 0, -1, 0] ($000) -> pass | FY2026 DB0 Table DB0-4 p4 agency total: sum of 6 divisions, deltas [1, -1, 0, -1] ($000) -> pass | FY2026 DB0 Table DB0-2 p2: sum of 4 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 HY0 Table HY0-4 p2 division EC0039: sum of 5 activities vs subtotal, deltas [-1, 1, 0, 0] ($000) -> pass | FY2026 HY0 Table HY0-4 p2 agency total: sum of 1 divisions, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 HY0 Table HY0-2 p1: sum of 1 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 CF0 Table CF0-4 p5 agency total: sum of 10 divisions, deltas [-1, 1, 0, 0] ($000) -> pass | FY2026 CF0 Table CF0-2 p2: sum of 5 fund rows vs GROSS FUNDS, deltas [-1, 1, 0, 1] ($000) -> pass | FY2026 HG0 Table HG0-4 p3 agency total: sum of 2 divisions, deltas [0, 1, 1, 0] ($000) -> pass | FY2026 HG0 Table HG0-2 p2: sum of 1 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2027 JA0 30-PBB p2 division HS0030: sum of 28 activities vs subtotal, deltas by column [-2, -2, -1, -3] ($000) -> pass | FY2027 JA0 30-PBB p2 agency total: sum of 5 division subtotals, deltas [-1, 1, 0, -1] ($000) -> pass | FY2027 JA0 Table JA0-2 p2: sum of 7 fund rows vs GROSS FUNDS, deltas [0, 1, 0, 0] ($000) -> pass | FY2027 FO0 30-PBB p1 division PS0023: sum of 2 activities vs subtotal, deltas by column [1, 0, 0, 0] ($000) -> pass | FY2027 FO0 30-PBB p1 agency total: sum of 11 division subtotals, deltas [-1,
- cross-book disagreements (same FY/stage/code, >$2K apart; later book preferred via x_preferred): 2022 actual JA0 AMP000 total: FY2025 book 33,466,000, FY2024 book 33,534,000 | 2022 actual JA0 AFO000 total: FY2025 book 3,079,000, FY2024 book 3,025,000 | 2022 actual JA0 HS0029 total: FY2025 book 279,438,000, FY2024 book 280,259,000 | 2022 actual JA0 HS0030 total: FY2025 book 625,848,000, FY2024 book 625,869,000 | 2025 approved JA0 H02902 total: FY2026 book 42,867,000, FY2025 book 42,943,000 | 2025 approved JA0 H02905 total: FY2026 book 91,735,000, FY2025 book 91,660,000 | 2025 approved FO0 P01903 total: FY2026 book 18,405,000, FY2025 book 18,312,000 | 2025 approved FO0 PS0019 total: FY2026 book 18,405,000, FY2025 book 18,312,000 | 2025 approved RM0 AFO003 total: FY2026 book 1,120,000, FY2025 book 1,010,000 | 2025 approved RM0 AFO005 total: FY2026 book 567,000, FY2025 book 577,000 | 2025 approved RM0 AFO000 total: FY2026 book 2,378,000, FY2025 book 2,278,000 | 2025 approved RM0 H04201 total: FY2026 book 175,000, FY2025 book 179,000 | 2025 approved RM0 H04202 total: FY2026 book 1,128,000, FY2025 book 1,151,000 | 2025 approved RM0 H04205 total: FY2026 book 381,000, FY2025 book 355,000 | 2025 approved RM0 H04504 total: FY2026 book 1,367,000, FY2025 book 100,000 | 2025 approved RM0 HS0045 total: FY2026 book 37,390,000, FY2025 book 36,123,000 | 2025 approved RM0 H04802 total: FY2026 book 27,140,000, FY2025 book 22,840,000 | 2025 approved RM0 H04805 total: FY2026 book 1,391,000, FY2025 book 5,691,000 | 2025 approved RM0 HS0053 total: FY2026 book 20,351,000, FY2025 book 21,717,000 | 2025 approved CF0 AFO003 total: FY2026 book 2,141,000, FY2025 book 2,222,000 | 2025 approved CF0 AFO000 total: FY2026 book 4,023,000, FY2025 book 4,104,000 | 2025 approved CF0 AMP026 total: FY2026 book 0, FY2025 book -3,000 | 2025 approved CF0 AMP000 total: FY2026 book 24,947,000, FY2025 book 24,944,000 | 2025 approved CF0 O00111 total: FY2026 book 556,000, FY2025 book 559,000 | 2025 approved CF0 GO0047 total: FY2026 book 6,545,000, FY2025 book 6,548,000 | 2025 approved CF0 O05201 total: FY2026 book 15,504,000, FY2025 book 15,422,000 | 2025 approved CF0 GO0052 total: FY2026 book 75,929,000, FY2025 book 75,847,000
- FY2024 old-code -> FY2025 code crosswalk (FY2024 approved): FO0 AMP000: FY2024 book 1,217,000 vs FY2025 book restated 1,217,000 (delta +0) | FO0 P02301: FY2024 book 171,000 vs FY2025 book restated 171,000 (delta +0) | FO0 P02303: FY2024 book 45,515,000 vs FY2025 book restated 45,515,000 (delta +0) | FO0 P04502: FY2024 book 3,720,000 vs FY2025 book restated 3,720,000 (delta +0) | FO0 PS0023: FY2024 book 45,687,000 vs FY2025 book restated 45,687,000 (delta +0) | HY0 R03903: FY2024 book 4,400,000 vs FY2025 book restated 4,400,000 (delta +0) | HY0 R03904: FY2024 book 0 vs FY2025 book restated 0 (delta +0) | HY0 R03905: FY2024 book 128,094,000 vs FY2025 book restated 128,094,000 (delta +0) | HY0 R03906: FY2024 book 10,581,000 vs FY2025 book restated 10,581,000 (delta +0) | HY0 R03907: FY2024 book 43,296,000 vs FY2025 book restated 43,296,000 (delta +0) | JA0 AFO000: FY2024 book 3,665,000 vs FY2025 book restated 3,665,000 (delta +0) | JA0 AMP000: FY2024 book 45,240,000 vs FY2025 book restated 45,240,000 (delta +0) | JA0 H03002: FY2024 book 79,033,000 vs FY2025 book restated 93,339,000 (delta +14,306,000) | JA0 H03003: FY2024 book 59,994,000 vs FY2025 book restated 59,994,000 (delta +0) | JA0 H03004: FY2024 book 31,818,000 vs FY2025 book restated 12,421,000 (delta -19,397,000) | JA0 H03007: FY2024 book 2,940,000 vs FY2025 book restated 2,940,000 (delta +0) | JA0 H03008: FY2024 book 42,536,000 vs FY2025 book restated 42,536,000 (delta +0) | JA0 H03009: FY2024 book 2,799,000 vs FY2025 book restated 4,259,000 (delta +1,460,000) | JA0 H03010: FY2024 book 51,764,000 vs FY2025 book restated 60,770,000 (delta +9,006,000) | JA0 H03011: FY2024 book 4,935,000 vs FY2025 book restated 4,935,000 (delta +0) | JA0 H03012: FY2024 book 86,929,000 vs FY2025 book restated 83,014,000 (delta -3,915,000) | JA0 H03013: FY2024 book 4,222,000 vs FY2025 book restated 4,222,000 (delta +0) | JA0 H03014-H03016: FY2024 book 11,541,000 vs FY2025 book restated 11,542,000 (delta +1,000) | JA0 H03017: FY2024 book 73,209,000 vs FY2025 book restated 73,209,000 (delta +0) | JA0 H03018: FY2024 book 10,875,000 vs FY2025 book restated 10,875,000 (delta +0) | JA0 H03019: FY2024 book 1,150,000 vs FY2025 book restated 1,150,000 (delta +0) | JA0 H03022: FY2024 book 1,980,000 vs FY2025 book restated 1,980,000 (delta +0) | JA0 H03023: FY2024 book 12,032,000 vs FY2025 book restated 12,032,000 (delta +0) | JA0 HS0029: FY2024 book 300,564,000 vs FY2025 book restated 300,564,000 (delta +0) | JA0 HS0030: FY2024 book 505,476,000 vs FY2025 book restated 505,476,000 (delta +0) | RM0 H04308: FY2024 book 29,637,000 vs FY2025 book restated 29,637,000 (delta +0) | RM0 H04504: FY2024 book 1,467,000 vs FY2025 book restated 1,467,000 (delta +0)
- event dates: budget_enacted/budget_revised = Local Budget Act 2nd reading {2024: '2023-05-30', 2025: '2024-06-12', 2026: '2025-07-28', 2027: '2026-06-23'}; budget_proposed = BSA introduced on behalf of the Mayor {2025: '2024-04-03', 2026: '2025-06-02', 2027: '2026-04-14'} (FY2024 proposal date not in downloaded docs -> blank); BSA policy rows = law/act effective date {2024: '2023-09-06', 2025: '2024-09-18', 2026: '2025-12-06', 2027: '2026-08-13'}; committee items = markup date when printed, else Local Budget Act date
- mapping: Table XX0-5 lines before 'Mayor's Proposed Budget' -> budget_proposed; lines between it and 'District's Approved Budget' -> budget_revised (Council changes); FY2027 Council-level changes taken from the activity-level Council chart instead of JA0-5 to avoid double counting
- coverage (stage[+funds] by FY x agency JA0/FO0/RM0/DB0/HY0/CF0/HG0):
| FY2021 | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds |
| FY2022 | actu | actu | actu | actu | actu | actu+funds | actu |
| FY2023 | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds |
| FY2024 | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds |
| FY2025 | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds,prop | actu+funds,appr+funds | actu+funds,appr+funds |
| FY2026 | appr+funds,prop | appr+funds,prop | appr+funds | appr+funds | appr+funds,prop | appr+funds | appr+funds |
| FY2027 | appr+funds | appr+funds | appr+funds,prop | appr+funds | appr+funds,prop | appr+funds | appr+funds |
- warnings (0):

### 2026-10-10 13:46 — 44_web_peers_funders
- search hits 757; pages listed 60, with content 57
- by group (listed, fetched): peer 25/25, funder 26/26, inkind 9/9
- failed/empty: nuvaya_fin_reports (http:http_403; chars 0 -> tavily no_content); hormd_ar_2024 (http:http_404; chars 0 -> tavily no_content); ik_hef_home (http:ok; chars 18 -> tavily no_content)
- this run: Tavily search 0, extract 7, HTTP GET 60, cache hits 90; cumulative (manifest): search 104/300, extract 7/200, HTTP 90

### 2026-10-10 13:47 — 37_parse_dc_budget: DC budget lines and policy events
- interim/stage_dc_budget_lines__dc.csv: 5,172 rows (Counter({'approved': 3172, 'actual': 1968, 'proposed': 32})); in-scope program/agency rows 854; duplicate keys 0
- interim/stage_fact_policy_events__dc.csv: 306 rows; by kind {'change_table_FO0-5': 8, 'change_table_HY0-5': 9, 'change_table_JA0-5': 25, 'yoy_approved_change': 161, 'bsa_subtitle': 25, 'fy2025_change_narrative': 21, 'committee_report_item': 22, 'committee_report_variance': 6, 'change_table_RM0-5': 1, 'change_table_DB0-5': 1, 'council_adjustments_chart_fy2027': 27}; by type {'budget_proposed': 41, 'budget_enacted': 161, 'budget_revised': 75, 'policy_change': 26, 'other': 1, 'program_launch': 2}
- parsed tables: FY2024 JA0 30-PBB (2024_JA0_ja_dhs_tables_2024j.pdf): 62 lines; FY2024 FO0 30-PBB (024_FO0_fo_vsjg_tables_2024j.pdf): 21 lines; FY2024 RM0 30-PBB (2024_RM0_rm_dbh_tables_2024j.pdf): 128 lines; FY2024 DB0 30-PBB (024_DB0_db_dhcd_tables_2024j.pdf): 44 lines; FY2024 HY0 30-PBB (2024_HY0_hy_has_tables_2024j.pdf): 16 lines; FY2024 CF0 30-PBB (2024_CF0_cf_des_tables_2024j.pdf): 69 lines; FY2024 HG0 30-PBB (24_HG0_hg_dmhhs_tables_2024j.pdf): 9 lines; FY2025 JA0 30-PBB (2025_JA0_ja_dhs_tables_2025j.pdf): 61 lines; FY2025 FO0 30-PBB (25_FO0_fo_ovsjg_tables_2025j.pdf): 28 lines; FY2025 RM0 30-PBB (2025_RM0_rm_dbh_tables_2025j.pdf): 87 lines; FY2025 DB0 30-PBB (025_DB0_db_dhcd_tables_2025j.pdf): 36 lines; FY2025 HY0 30-PBB (2025_HY0_hy_hap_tables_2025j.pdf): 7 lines; FY2025 CF0 30-PBB (025_CF0_cf_does_tables_2025j.pdf): 62 lines; FY2025 HG0 30-PBB (25_HG0_hg_dmhhs_tables_2025j.pdf): 8 lines; FY2026 JA0 Table JA0-4 (026_JA0_ja_dhs_chapter_2026o.pdf): 57 lines; FY2026 FO0 Table FO0-4 (26_FO0_fo_vsjg_chapter_2026o.pdf): 26 lines; FY2026 RM0 Table RM0-4 (026_RM0_rm_dbh_chapter_2026o.pdf): 83 lines; FY2026 DB0 Table DB0-4 (26_DB0_db_dhcd_chapter_2026o.pdf): 36 lines; FY2026 HY0 Table HY0-4 (026_HY0_hy_has_chapter_2026o.pdf): 7 lines; FY2026 CF0 Table CF0-4 (26_CF0_cf_does_chapter_2026o.pdf): 61 lines; FY2026 HG0 Table HG0-4 (6_HG0_hg_dmhhs_chapter_2026o.pdf): 6 lines; FY2027 JA0 30-PBB (7_JA0_ja0_dhs_tables_2027a_0.pdf): 57 lines; FY2027 FO0 30-PBB (FO0_fo0_ovsjg_tables_2027a_0.pdf): 26 lines; FY2027 RM0 30-PBB (7_RM0_rm0_dbh_tables_2027a_0.pdf): 80 lines; FY2027 DB0 30-PBB (_DB0_db0_dhcd_tables_2027a_0.pdf): 36 lines; FY2027 HY0 30-PBB (7_HY0_hy0_hap_tables_2027a_0.pdf): 7 lines; FY2027 CF0 30-PBB (_CF0_cf0_does_tables_2027a_0.pdf): 61 lines; FY2027 HG0 30-PBB (HG0_hg0_dmhhs_tables_2027a_0.pdf): 7 lines
- change items: FY2024 JA0 Table JA0-5: 29 change lines, 7 in scope; FY2024 FO0 Table FO0-5: 14 change lines, 3 in scope; FY2024 RM0 Table RM0-5: 25 change lines, 0 in scope; FY2024 DB0 Table DB0-5: 14 change lines, 0 in scope; FY2024 HY0 Table HY0-5: 6 change lines, 6 in scope; FY2024 CF0 Table CF0-5: 16 change lines, 0 in scope; FY2024 HG0 Table HG0-5: 7 change lines, 0 in scope; FY2025 JA0 narrative change sentences (pypdfium2): 15 in scope; FY2025 FO0: chapter change text is font-garbled (amounts missing); OVSJG FY2025 changes taken from the JPS committee report; FY2025 RM0 narrative change sentences (pypdfium2): 0 in scope; FY2025 DB0 narrative change sentences (pypdfium2): 2 in scope; FY2025 HY0 narrative change sentences (pypdfium2): 4 in scope; FY2025 CF0 Table CF0-5: 20 change lines, 0 in scope; FY2025 HG0 narrative change sentences (pypdfium2): 0 in scope; FY2026 JA0 Table JA0-5: 29 change lines, 14 in scope; FY2026 FO0 Table FO0-5: 16 change lines, 4 in scope; FY2026 RM0 Table RM0-5: 27 change lines, 1 in scope; FY2026 DB0 Table DB0-5: 16 change lines, 0 in scope; FY2026 HY0 Table HY0-5: 2 change lines, 2 in scope; FY2026 CF0 Table CF0-5: 17 change lines, 0 in scope; FY2026 HG0 Table HG0-5: 4 change lines, 0 in scope; FY2027 JA0 Table JA0-5: 15 change lines, 4 in scope; FY2027 FO0 Table FO0-5: 11 change lines, 1 in scope; FY2027 RM0 Table RM0-5: 17 change lines, 0 in scope; FY2027 DB0 Table DB0-5: 15 change lines, 1 in scope; FY2027 HY0 Table HY0-5: 3 change lines, 1 in scope; FY2027 CF0 Table CF0-5: 8 change lines, 0 in scope; FY2027 HG0 Table HG0-5: 3 change lines, 0 in scope
- committee report tables: BR_FY25_Housing -> 1 in-scope proposed activity rows (markup 2024-05-09); BR_FY25_JPS -> 0 in-scope proposed activity rows (markup not printed); BR_FY26_committee_budget_report_Human-Services -> 18 in-scope proposed activity rows (markup 2025-06-24); BR_FY26_committee_budget_report_Housing -> 5 in-scope proposed activity rows (markup 2025-06-24); BR_FY26_committee_budget_report_JPS -> 2 in-scope proposed activity rows (markup not printed); BR_FY26_committee_budget_report_Health -> 0 in-scope proposed activity rows (markup 2025-06-23); BR_FY27_committee_budget_report_DRAFT-FY2027-Committee-on-Health -> 2 in-scope proposed activity rows (markup 2026-05-20); BR_FY27_committee_budget_report_FY27-Committee-on-Housing -> 4 in-scope proposed activity rows (markup not printed); BR_FY27_committee_budget_report_52226-FY2027-JPS -> 0 in-scope proposed activity rows (markup not printed)
- FY2027 Council adjustments chart: 1627 rows read, 27 in-scope events
- BSA subtitles kept: 25; curated committee-report items: 22; YoY approved-change events: 161
- tie-outs: 257 pass, 0 fail
- tie-out detail (in-scope divisions): FY2024 JA0 30-PBB p2 division 5000: sum of 23 activities vs subtotal, deltas by column [0, 0, 0, -1] ($000) -> pass | FY2024 JA0 30-PBB p3 agency total: sum of 8 division subtotals, deltas [0, -2, 0, 1] ($000) -> pass | FY2024 JA0 Table JA0-2 p2: sum of 7 fund rows vs GROSS FUNDS, deltas [-1, 0, -1, 0] ($000) -> pass | FY2024 FO0 30-PBB p1 division 4000: sum of 2 activities vs subtotal, deltas by column [0, 0, 0, -1] ($000) -> pass | FY2024 FO0 30-PBB p1 division 5000: sum of 1 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 FO0 30-PBB p1 division 6000: sum of 5 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 FO0 30-PBB p1 agency total: sum of 7 division subtotals, deltas [-2, -1, -2, 1] ($000) -> pass | FY2024 FO0 Table FO0-2 p2: sum of 5 fund rows vs GROSS FUNDS, deltas [0, 0, -1, 0] ($000) -> pass | FY2024 RM0 30-PBB p5 agency total: sum of 16 division subtotals, deltas [0, 1, 1, 0] ($000) -> pass | FY2024 RM0 Table RM0-2 p2: sum of 9 fund rows vs GROSS FUNDS, deltas [0, 1, 0, 1] ($000) -> pass | FY2024 DB0 30-PBB p2 agency total: sum of 9 division subtotals, deltas [0, 0, 0, -1] ($000) -> pass | FY2024 DB0 Table DB0-2 p2: sum of 5 fund rows vs GROSS FUNDS, deltas [1, -1, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 division 4000: sum of 1 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 division 5000: sum of 1 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 division 6000: sum of 5 activities vs subtotal, deltas by column [2, -1, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 agency total: sum of 5 division subtotals, deltas [0, 0, -1, 0] ($000) -> pass | FY2024 HY0 Table HY0-2 p1: sum of 1 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2024 CF0 30-PBB p2 division 4000: sum of 16 activities vs subtotal, deltas by column [0, 0, 0, -1] ($000) -> pass | FY2024 CF0 30-PBB p2 division 5000: sum of 3 activities vs subtotal, deltas by column [1, 0, 1, 0] ($000) -> pass | FY2024 CF0 30-PBB p2 division 6000: sum of 6 activities vs subtotal, deltas by column [1, 0, 0, 0] ($000) -> pass | FY2024 CF0 30-PBB p3 agency total: sum of 11 division subtotals, deltas [-1, 0, 0, -1] ($000) -> pass | FY2024 CF0 Table CF0-2 p2: sum of 6 fund rows vs GROSS FUNDS, deltas [1, 0, 0, 0] ($000) -> pass | FY2024 HG0 30-PBB p1 agency total: sum of 4 division subtotals, deltas [0, 0, 0, 0] ($000) -> pass | FY2024 HG0 Table HG0-2 p2: sum of 2 fund rows vs GROSS FUNDS, deltas [0, 1, 0, 0] ($000) -> pass | FY2025 JA0 30-PBB p2 division HS0030: sum of 28 activities vs subtotal, deltas by column [-2, 1, -1, 1] ($000) -> pass | FY2025 JA0 30-PBB p2 agency total: sum of 6 division subtotals, deltas [0, -1, 1, 0] ($000) -> pass | FY2025 FO0 30-PBB p1 division PS0023: sum of 2 activities vs subtotal, deltas by column [0, 0, -1, 0] ($000) -> pass | FY2025 FO0 30-PBB p2 agency total: sum of 12 division subtotals, deltas [-1, -2, 1, 0] ($000) -> pass | FY2025 RM0 30-PBB p3 agency total: sum of 13 division subtotals, deltas [1, 1, 0, 1] ($000) -> pass | FY2025 DB0 30-PBB p2 agency total: sum of 6 division subtotals, deltas [0, 1, 1, 0] ($000) -> pass | FY2025 HY0 30-PBB p1 division EC0039: sum of 5 activities vs subtotal, deltas by column [0, -1, 0, 0] ($000) -> pass | FY2025 HY0 30-PBB p1 agency total: sum of 1 division subtotals, deltas [0, 0, 0, 0] ($000) -> pass | FY2025 CF0 30-PBB p3 agency total: sum of 10 division subtotals, deltas [0, -1, 0, -1] ($000) -> pass | FY2025 CF0 Table CF0-2 p2: sum of 6 fund rows vs GROSS FUNDS, deltas [0, -1, 0, 0] ($000) -> pass | FY2025 HG0 30-PBB p1 agency total: sum of 3 division subtotals, deltas [0, 0, 0, 1] ($000) -> pass | FY2026 JA0 Table JA0-4 p5 division HS0030: sum of 28 activities vs subtotal, deltas [1, -2, 1, -1] ($000) -> pass | FY2026 JA0 Table JA0-4 p5 agency total: sum of 5 divisions, deltas [-1, -1, 0, 0] ($000) -> pass | FY2026 JA0 Table JA0-2 p2: sum of 7 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 FO0 Table FO0-4 p4 division PS0023: sum of 2 activities vs subtotal, deltas [0, 1, 0, 0] ($000) -> pass | FY2026 FO0 Table FO0-4 p4 agency total: sum of 11 divisions, deltas [-2, 0, 0, 0] ($000) -> pass | FY2026 FO0 Table FO0-2 p2: sum of 4 fund rows vs GROSS FUNDS, deltas [-1, 0, 0, 0] ($000) -> pass | FY2026 RM0 Table RM0-4 p7 agency total: sum of 13 divisions, deltas [1, 1, 2, 0] ($000) -> pass | FY2026 RM0 Table RM0-2 p2: sum of 8 fund rows vs GROSS FUNDS, deltas [1, 0, -1, 0] ($000) -> pass | FY2026 DB0 Table DB0-4 p4 agency total: sum of 6 divisions, deltas [1, -1, 0, -1] ($000) -> pass | FY2026 DB0 Table DB0-2 p2: sum of 4 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 HY0 Table HY0-4 p2 division EC0039: sum of 5 activities vs subtotal, deltas [-1, 1, 0, 0] ($000) -> pass | FY2026 HY0 Table HY0-4 p2 agency total: sum of 1 divisions, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 HY0 Table HY0-2 p1: sum of 1 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 CF0 Table CF0-4 p5 agency total: sum of 10 divisions, deltas [-1, 1, 0, 0] ($000) -> pass | FY2026 CF0 Table CF0-2 p2: sum of 5 fund rows vs GROSS FUNDS, deltas [-1, 1, 0, 1] ($000) -> pass | FY2026 HG0 Table HG0-4 p3 agency total: sum of 2 divisions, deltas [0, 1, 1, 0] ($000) -> pass | FY2026 HG0 Table HG0-2 p2: sum of 1 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2027 JA0 30-PBB p2 division HS0030: sum of 28 activities vs subtotal, deltas by column [-2, -2, -1, -3] ($000) -> pass | FY2027 JA0 30-PBB p2 agency total: sum of 5 division subtotals, deltas [-1, 1, 0, -1] ($000) -> pass | FY2027 JA0 Table JA0-2 p2: sum of 7 fund rows vs GROSS FUNDS, deltas [0, 1, 0, 0] ($000) -> pass | FY2027 FO0 30-PBB p1 division PS0023: sum of 2 activities vs subtotal, deltas by column [1, 0, 0, 0] ($000) -> pass | FY2027 FO0 30-PBB p1 agency total: sum of 11 division subtotals, deltas [-1,
- cross-book disagreements (same FY/stage/code, >$2K apart; later book preferred via x_preferred): 2022 actual JA0 AMP000 total: FY2025 book 33,466,000, FY2024 book 33,534,000 | 2022 actual JA0 AFO000 total: FY2025 book 3,079,000, FY2024 book 3,025,000 | 2022 actual JA0 HS0029 total: FY2025 book 279,438,000, FY2024 book 280,259,000 | 2022 actual JA0 HS0030 total: FY2025 book 625,848,000, FY2024 book 625,869,000 | 2025 approved JA0 H02902 total: FY2026 book 42,867,000, FY2025 book 42,943,000 | 2025 approved JA0 H02905 total: FY2026 book 91,735,000, FY2025 book 91,660,000 | 2025 approved FO0 P01903 total: FY2026 book 18,405,000, FY2025 book 18,312,000 | 2025 approved FO0 PS0019 total: FY2026 book 18,405,000, FY2025 book 18,312,000 | 2025 approved RM0 AFO003 total: FY2026 book 1,120,000, FY2025 book 1,010,000 | 2025 approved RM0 AFO005 total: FY2026 book 567,000, FY2025 book 577,000 | 2025 approved RM0 AFO000 total: FY2026 book 2,378,000, FY2025 book 2,278,000 | 2025 approved RM0 H04201 total: FY2026 book 175,000, FY2025 book 179,000 | 2025 approved RM0 H04202 total: FY2026 book 1,128,000, FY2025 book 1,151,000 | 2025 approved RM0 H04205 total: FY2026 book 381,000, FY2025 book 355,000 | 2025 approved RM0 H04504 total: FY2026 book 1,367,000, FY2025 book 100,000 | 2025 approved RM0 HS0045 total: FY2026 book 37,390,000, FY2025 book 36,123,000 | 2025 approved RM0 H04802 total: FY2026 book 27,140,000, FY2025 book 22,840,000 | 2025 approved RM0 H04805 total: FY2026 book 1,391,000, FY2025 book 5,691,000 | 2025 approved RM0 HS0053 total: FY2026 book 20,351,000, FY2025 book 21,717,000 | 2025 approved CF0 AFO003 total: FY2026 book 2,141,000, FY2025 book 2,222,000 | 2025 approved CF0 AFO000 total: FY2026 book 4,023,000, FY2025 book 4,104,000 | 2025 approved CF0 AMP026 total: FY2026 book 0, FY2025 book -3,000 | 2025 approved CF0 AMP000 total: FY2026 book 24,947,000, FY2025 book 24,944,000 | 2025 approved CF0 O00111 total: FY2026 book 556,000, FY2025 book 559,000 | 2025 approved CF0 GO0047 total: FY2026 book 6,545,000, FY2025 book 6,548,000 | 2025 approved CF0 O05201 total: FY2026 book 15,504,000, FY2025 book 15,422,000 | 2025 approved CF0 GO0052 total: FY2026 book 75,929,000, FY2025 book 75,847,000
- FY2024 old-code -> FY2025 code crosswalk (FY2024 approved): FO0 P02301: FY2024 book 171,000 vs FY2025 book restated 171,000 (delta +0) | FO0 P02303: FY2024 book 45,515,000 vs FY2025 book restated 45,515,000 (delta +0) | FO0 P04502: FY2024 book 3,720,000 vs FY2025 book restated 3,720,000 (delta +0) | HY0 R03903: FY2024 book 4,400,000 vs FY2025 book restated 4,400,000 (delta +0) | HY0 R03904: FY2024 book 0 vs FY2025 book restated 0 (delta +0) | HY0 R03905: FY2024 book 128,094,000 vs FY2025 book restated 128,094,000 (delta +0) | HY0 R03906: FY2024 book 10,581,000 vs FY2025 book restated 10,581,000 (delta +0) | HY0 R03907: FY2024 book 43,296,000 vs FY2025 book restated 43,296,000 (delta +0) | JA0 H03002: FY2024 book 79,033,000 vs FY2025 book restated 93,339,000 (delta +14,306,000) | JA0 H03003: FY2024 book 59,994,000 vs FY2025 book restated 59,994,000 (delta +0) | JA0 H03004: FY2024 book 31,818,000 vs FY2025 book restated 12,421,000 (delta -19,397,000) | JA0 H03007: FY2024 book 2,940,000 vs FY2025 book restated 2,940,000 (delta +0) | JA0 H03008: FY2024 book 42,536,000 vs FY2025 book restated 42,536,000 (delta +0) | JA0 H03009: FY2024 book 2,799,000 vs FY2025 book restated 4,259,000 (delta +1,460,000) | JA0 H03010: FY2024 book 51,764,000 vs FY2025 book restated 60,770,000 (delta +9,006,000) | JA0 H03011: FY2024 book 4,935,000 vs FY2025 book restated 4,935,000 (delta +0) | JA0 H03012: FY2024 book 86,929,000 vs FY2025 book restated 83,014,000 (delta -3,915,000) | JA0 H03013: FY2024 book 4,222,000 vs FY2025 book restated 4,222,000 (delta +0) | JA0 H03014-H03016: FY2024 book 11,541,000 vs FY2025 book restated 11,542,000 (delta +1,000) | JA0 H03017: FY2024 book 73,209,000 vs FY2025 book restated 73,209,000 (delta +0) | JA0 H03018: FY2024 book 10,875,000 vs FY2025 book restated 10,875,000 (delta +0) | JA0 H03019: FY2024 book 1,150,000 vs FY2025 book restated 1,150,000 (delta +0) | JA0 H03022: FY2024 book 1,980,000 vs FY2025 book restated 1,980,000 (delta +0) | JA0 H03023: FY2024 book 12,032,000 vs FY2025 book restated 12,032,000 (delta +0) | RM0 H04308: FY2024 book 29,637,000 vs FY2025 book restated 29,637,000 (delta +0) | RM0 H04504: FY2024 book 1,467,000 vs FY2025 book restated 1,467,000 (delta +0)
- event dates: budget_enacted/budget_revised = Local Budget Act 2nd reading {2024: '2023-05-30', 2025: '2024-06-12', 2026: '2025-07-28', 2027: '2026-06-23'}; budget_proposed = BSA introduced on behalf of the Mayor {2025: '2024-04-03', 2026: '2025-06-02', 2027: '2026-04-14'} (FY2024 proposal date not in downloaded docs -> blank); BSA policy rows = law/act effective date {2024: '2023-09-06', 2025: '2024-09-18', 2026: '2025-12-06', 2027: '2026-08-13'}; committee items = markup date when printed, else Local Budget Act date
- mapping: Table XX0-5 lines before 'Mayor's Proposed Budget' -> budget_proposed; lines between it and 'District's Approved Budget' -> budget_revised (Council changes); FY2027 Council-level changes taken from the activity-level Council chart instead of JA0-5 to avoid double counting
- coverage (stage[+funds] by FY x agency JA0/FO0/RM0/DB0/HY0/CF0/HG0):
| FY2021 | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds |
| FY2022 | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds |
| FY2023 | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds |
| FY2024 | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds |
| FY2025 | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds,prop | actu+funds,appr+funds | actu+funds,appr+funds |
| FY2026 | appr+funds,prop | appr+funds,prop | appr+funds | appr+funds | appr+funds,prop | appr+funds | appr+funds |
| FY2027 | appr+funds | appr+funds | appr+funds,prop | appr+funds | appr+funds,prop | appr+funds | appr+funds |
- warnings (0):

### 2026-10-10 13:48 — 42_pull_propublica: fetch
- targets: 2,533 EINs = 1,033 calvary/core_peers/dc_sector + 1,500 dmv_funders
- funder candidates (F1 with BMF assets >= $1M, plus F2/F3): 3,777 {'F1': 1928, 'F2': 1847, 'F3': 2}
- CAP: kept top 1,500 funders by BMF ASSET_AMT (min kept $2,409,780); dropped 2,277; kept by rule {'F1': 1310, 'F2': 188, 'F3': 2}
- status counts: {'200': 2051, 'reused': 482}; new downloads 2,051, reused raw 482
- rate limit 2 req/s (lib.common.RateLimiter)

### 2026-10-10 13:49 — 37_parse_dc_budget: DC budget lines and policy events
- interim/stage_dc_budget_lines__dc.csv: 5,172 rows (Counter({'approved': 3172, 'actual': 1968, 'proposed': 32})); in-scope program/agency rows 854; duplicate keys 0
- interim/stage_fact_policy_events__dc.csv: 306 rows; by kind {'change_table_FO0-5': 8, 'change_table_HY0-5': 9, 'change_table_JA0-5': 25, 'yoy_approved_change': 161, 'bsa_subtitle': 25, 'fy2025_change_narrative': 21, 'committee_report_item': 22, 'committee_report_variance': 6, 'change_table_RM0-5': 1, 'change_table_DB0-5': 1, 'council_adjustments_chart_fy2027': 27}; by type {'budget_proposed': 41, 'budget_enacted': 161, 'budget_revised': 75, 'policy_change': 26, 'other': 1, 'program_launch': 2}
- parsed tables: FY2024 JA0 30-PBB (2024_JA0_ja_dhs_tables_2024j.pdf): 62 lines; FY2024 FO0 30-PBB (024_FO0_fo_vsjg_tables_2024j.pdf): 21 lines; FY2024 RM0 30-PBB (2024_RM0_rm_dbh_tables_2024j.pdf): 128 lines; FY2024 DB0 30-PBB (024_DB0_db_dhcd_tables_2024j.pdf): 44 lines; FY2024 HY0 30-PBB (2024_HY0_hy_has_tables_2024j.pdf): 16 lines; FY2024 CF0 30-PBB (2024_CF0_cf_des_tables_2024j.pdf): 69 lines; FY2024 HG0 30-PBB (24_HG0_hg_dmhhs_tables_2024j.pdf): 9 lines; FY2025 JA0 30-PBB (2025_JA0_ja_dhs_tables_2025j.pdf): 61 lines; FY2025 FO0 30-PBB (25_FO0_fo_ovsjg_tables_2025j.pdf): 28 lines; FY2025 RM0 30-PBB (2025_RM0_rm_dbh_tables_2025j.pdf): 87 lines; FY2025 DB0 30-PBB (025_DB0_db_dhcd_tables_2025j.pdf): 36 lines; FY2025 HY0 30-PBB (2025_HY0_hy_hap_tables_2025j.pdf): 7 lines; FY2025 CF0 30-PBB (025_CF0_cf_does_tables_2025j.pdf): 62 lines; FY2025 HG0 30-PBB (25_HG0_hg_dmhhs_tables_2025j.pdf): 8 lines; FY2026 JA0 Table JA0-4 (026_JA0_ja_dhs_chapter_2026o.pdf): 57 lines; FY2026 FO0 Table FO0-4 (26_FO0_fo_vsjg_chapter_2026o.pdf): 26 lines; FY2026 RM0 Table RM0-4 (026_RM0_rm_dbh_chapter_2026o.pdf): 83 lines; FY2026 DB0 Table DB0-4 (26_DB0_db_dhcd_chapter_2026o.pdf): 36 lines; FY2026 HY0 Table HY0-4 (026_HY0_hy_has_chapter_2026o.pdf): 7 lines; FY2026 CF0 Table CF0-4 (26_CF0_cf_does_chapter_2026o.pdf): 61 lines; FY2026 HG0 Table HG0-4 (6_HG0_hg_dmhhs_chapter_2026o.pdf): 6 lines; FY2027 JA0 30-PBB (7_JA0_ja0_dhs_tables_2027a_0.pdf): 57 lines; FY2027 FO0 30-PBB (FO0_fo0_ovsjg_tables_2027a_0.pdf): 26 lines; FY2027 RM0 30-PBB (7_RM0_rm0_dbh_tables_2027a_0.pdf): 80 lines; FY2027 DB0 30-PBB (_DB0_db0_dhcd_tables_2027a_0.pdf): 36 lines; FY2027 HY0 30-PBB (7_HY0_hy0_hap_tables_2027a_0.pdf): 7 lines; FY2027 CF0 30-PBB (_CF0_cf0_does_tables_2027a_0.pdf): 61 lines; FY2027 HG0 30-PBB (HG0_hg0_dmhhs_tables_2027a_0.pdf): 7 lines
- change items: FY2024 JA0 Table JA0-5: 29 change lines, 7 in scope; FY2024 FO0 Table FO0-5: 14 change lines, 3 in scope; FY2024 RM0 Table RM0-5: 25 change lines, 0 in scope; FY2024 DB0 Table DB0-5: 14 change lines, 0 in scope; FY2024 HY0 Table HY0-5: 6 change lines, 6 in scope; FY2024 CF0 Table CF0-5: 16 change lines, 0 in scope; FY2024 HG0 Table HG0-5: 7 change lines, 0 in scope; FY2025 JA0 narrative change sentences (pypdfium2): 15 in scope; FY2025 FO0: chapter change text is font-garbled (amounts missing); OVSJG FY2025 changes taken from the JPS committee report; FY2025 RM0 narrative change sentences (pypdfium2): 0 in scope; FY2025 DB0 narrative change sentences (pypdfium2): 2 in scope; FY2025 HY0 narrative change sentences (pypdfium2): 4 in scope; FY2025 CF0 Table CF0-5: 20 change lines, 0 in scope; FY2025 HG0 narrative change sentences (pypdfium2): 0 in scope; FY2026 JA0 Table JA0-5: 29 change lines, 14 in scope; FY2026 FO0 Table FO0-5: 16 change lines, 4 in scope; FY2026 RM0 Table RM0-5: 27 change lines, 1 in scope; FY2026 DB0 Table DB0-5: 16 change lines, 0 in scope; FY2026 HY0 Table HY0-5: 2 change lines, 2 in scope; FY2026 CF0 Table CF0-5: 17 change lines, 0 in scope; FY2026 HG0 Table HG0-5: 4 change lines, 0 in scope; FY2027 JA0 Table JA0-5: 15 change lines, 4 in scope; FY2027 FO0 Table FO0-5: 11 change lines, 1 in scope; FY2027 RM0 Table RM0-5: 17 change lines, 0 in scope; FY2027 DB0 Table DB0-5: 15 change lines, 1 in scope; FY2027 HY0 Table HY0-5: 3 change lines, 1 in scope; FY2027 CF0 Table CF0-5: 8 change lines, 0 in scope; FY2027 HG0 Table HG0-5: 3 change lines, 0 in scope
- committee report tables: BR_FY25_Housing -> 1 in-scope proposed activity rows (markup 2024-05-09); BR_FY25_JPS -> 0 in-scope proposed activity rows (markup not printed); BR_FY26_committee_budget_report_Human-Services -> 18 in-scope proposed activity rows (markup 2025-06-24); BR_FY26_committee_budget_report_Housing -> 5 in-scope proposed activity rows (markup 2025-06-24); BR_FY26_committee_budget_report_JPS -> 2 in-scope proposed activity rows (markup not printed); BR_FY26_committee_budget_report_Health -> 0 in-scope proposed activity rows (markup 2025-06-23); BR_FY27_committee_budget_report_DRAFT-FY2027-Committee-on-Health -> 2 in-scope proposed activity rows (markup 2026-05-20); BR_FY27_committee_budget_report_FY27-Committee-on-Housing -> 4 in-scope proposed activity rows (markup not printed); BR_FY27_committee_budget_report_52226-FY2027-JPS -> 0 in-scope proposed activity rows (markup not printed)
- FY2027 Council adjustments chart: 1627 rows read, 27 in-scope events
- BSA subtitles kept: 25; curated committee-report items: 22; YoY approved-change events: 161
- tie-outs: 257 pass, 0 fail
- tie-out detail (in-scope divisions): FY2024 JA0 30-PBB p2 division 5000: sum of 23 activities vs subtotal, deltas by column [0, 0, 0, -1] ($000) -> pass | FY2024 JA0 30-PBB p3 agency total: sum of 8 division subtotals, deltas [0, -2, 0, 1] ($000) -> pass | FY2024 JA0 Table JA0-2 p2: sum of 7 fund rows vs GROSS FUNDS, deltas [-1, 0, -1, 0] ($000) -> pass | FY2024 FO0 30-PBB p1 division 4000: sum of 2 activities vs subtotal, deltas by column [0, 0, 0, -1] ($000) -> pass | FY2024 FO0 30-PBB p1 division 5000: sum of 1 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 FO0 30-PBB p1 division 6000: sum of 5 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 FO0 30-PBB p1 agency total: sum of 7 division subtotals, deltas [-2, -1, -2, 1] ($000) -> pass | FY2024 FO0 Table FO0-2 p2: sum of 5 fund rows vs GROSS FUNDS, deltas [0, 0, -1, 0] ($000) -> pass | FY2024 RM0 30-PBB p5 agency total: sum of 16 division subtotals, deltas [0, 1, 1, 0] ($000) -> pass | FY2024 RM0 Table RM0-2 p2: sum of 9 fund rows vs GROSS FUNDS, deltas [0, 1, 0, 1] ($000) -> pass | FY2024 DB0 30-PBB p2 agency total: sum of 9 division subtotals, deltas [0, 0, 0, -1] ($000) -> pass | FY2024 DB0 Table DB0-2 p2: sum of 5 fund rows vs GROSS FUNDS, deltas [1, -1, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 division 4000: sum of 1 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 division 5000: sum of 1 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 division 6000: sum of 5 activities vs subtotal, deltas by column [2, -1, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 agency total: sum of 5 division subtotals, deltas [0, 0, -1, 0] ($000) -> pass | FY2024 HY0 Table HY0-2 p1: sum of 1 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2024 CF0 30-PBB p2 division 4000: sum of 16 activities vs subtotal, deltas by column [0, 0, 0, -1] ($000) -> pass | FY2024 CF0 30-PBB p2 division 5000: sum of 3 activities vs subtotal, deltas by column [1, 0, 1, 0] ($000) -> pass | FY2024 CF0 30-PBB p2 division 6000: sum of 6 activities vs subtotal, deltas by column [1, 0, 0, 0] ($000) -> pass | FY2024 CF0 30-PBB p3 agency total: sum of 11 division subtotals, deltas [-1, 0, 0, -1] ($000) -> pass | FY2024 CF0 Table CF0-2 p2: sum of 6 fund rows vs GROSS FUNDS, deltas [1, 0, 0, 0] ($000) -> pass | FY2024 HG0 30-PBB p1 agency total: sum of 4 division subtotals, deltas [0, 0, 0, 0] ($000) -> pass | FY2024 HG0 Table HG0-2 p2: sum of 2 fund rows vs GROSS FUNDS, deltas [0, 1, 0, 0] ($000) -> pass | FY2025 JA0 30-PBB p2 division HS0030: sum of 28 activities vs subtotal, deltas by column [-2, 1, -1, 1] ($000) -> pass | FY2025 JA0 30-PBB p2 agency total: sum of 6 division subtotals, deltas [0, -1, 1, 0] ($000) -> pass | FY2025 FO0 30-PBB p1 division PS0023: sum of 2 activities vs subtotal, deltas by column [0, 0, -1, 0] ($000) -> pass | FY2025 FO0 30-PBB p2 agency total: sum of 12 division subtotals, deltas [-1, -2, 1, 0] ($000) -> pass | FY2025 RM0 30-PBB p3 agency total: sum of 13 division subtotals, deltas [1, 1, 0, 1] ($000) -> pass | FY2025 DB0 30-PBB p2 agency total: sum of 6 division subtotals, deltas [0, 1, 1, 0] ($000) -> pass | FY2025 HY0 30-PBB p1 division EC0039: sum of 5 activities vs subtotal, deltas by column [0, -1, 0, 0] ($000) -> pass | FY2025 HY0 30-PBB p1 agency total: sum of 1 division subtotals, deltas [0, 0, 0, 0] ($000) -> pass | FY2025 CF0 30-PBB p3 agency total: sum of 10 division subtotals, deltas [0, -1, 0, -1] ($000) -> pass | FY2025 CF0 Table CF0-2 p2: sum of 6 fund rows vs GROSS FUNDS, deltas [0, -1, 0, 0] ($000) -> pass | FY2025 HG0 30-PBB p1 agency total: sum of 3 division subtotals, deltas [0, 0, 0, 1] ($000) -> pass | FY2026 JA0 Table JA0-4 p5 division HS0030: sum of 28 activities vs subtotal, deltas [1, -2, 1, -1] ($000) -> pass | FY2026 JA0 Table JA0-4 p5 agency total: sum of 5 divisions, deltas [-1, -1, 0, 0] ($000) -> pass | FY2026 JA0 Table JA0-2 p2: sum of 7 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 FO0 Table FO0-4 p4 division PS0023: sum of 2 activities vs subtotal, deltas [0, 1, 0, 0] ($000) -> pass | FY2026 FO0 Table FO0-4 p4 agency total: sum of 11 divisions, deltas [-2, 0, 0, 0] ($000) -> pass | FY2026 FO0 Table FO0-2 p2: sum of 4 fund rows vs GROSS FUNDS, deltas [-1, 0, 0, 0] ($000) -> pass | FY2026 RM0 Table RM0-4 p7 agency total: sum of 13 divisions, deltas [1, 1, 2, 0] ($000) -> pass | FY2026 RM0 Table RM0-2 p2: sum of 8 fund rows vs GROSS FUNDS, deltas [1, 0, -1, 0] ($000) -> pass | FY2026 DB0 Table DB0-4 p4 agency total: sum of 6 divisions, deltas [1, -1, 0, -1] ($000) -> pass | FY2026 DB0 Table DB0-2 p2: sum of 4 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 HY0 Table HY0-4 p2 division EC0039: sum of 5 activities vs subtotal, deltas [-1, 1, 0, 0] ($000) -> pass | FY2026 HY0 Table HY0-4 p2 agency total: sum of 1 divisions, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 HY0 Table HY0-2 p1: sum of 1 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 CF0 Table CF0-4 p5 agency total: sum of 10 divisions, deltas [-1, 1, 0, 0] ($000) -> pass | FY2026 CF0 Table CF0-2 p2: sum of 5 fund rows vs GROSS FUNDS, deltas [-1, 1, 0, 1] ($000) -> pass | FY2026 HG0 Table HG0-4 p3 agency total: sum of 2 divisions, deltas [0, 1, 1, 0] ($000) -> pass | FY2026 HG0 Table HG0-2 p2: sum of 1 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2027 JA0 30-PBB p2 division HS0030: sum of 28 activities vs subtotal, deltas by column [-2, -2, -1, -3] ($000) -> pass | FY2027 JA0 30-PBB p2 agency total: sum of 5 division subtotals, deltas [-1, 1, 0, -1] ($000) -> pass | FY2027 JA0 Table JA0-2 p2: sum of 7 fund rows vs GROSS FUNDS, deltas [0, 1, 0, 0] ($000) -> pass | FY2027 FO0 30-PBB p1 division PS0023: sum of 2 activities vs subtotal, deltas by column [1, 0, 0, 0] ($000) -> pass | FY2027 FO0 30-PBB p1 agency total: sum of 11 division subtotals, deltas [-1,
- cross-book disagreements (same FY/stage/code, >$2K apart; later book preferred via x_preferred): 2022 actual JA0 AMP000 total: FY2025 book 33,466,000, FY2024 book 33,534,000 | 2022 actual JA0 AFO000 total: FY2025 book 3,079,000, FY2024 book 3,025,000 | 2022 actual JA0 HS0029 total: FY2025 book 279,438,000, FY2024 book 280,259,000 | 2022 actual JA0 HS0030 total: FY2025 book 625,848,000, FY2024 book 625,869,000 | 2025 approved JA0 H02902 total: FY2026 book 42,867,000, FY2025 book 42,943,000 | 2025 approved JA0 H02905 total: FY2026 book 91,735,000, FY2025 book 91,660,000 | 2025 approved FO0 P01903 total: FY2026 book 18,405,000, FY2025 book 18,312,000 | 2025 approved FO0 PS0019 total: FY2026 book 18,405,000, FY2025 book 18,312,000 | 2025 approved RM0 AFO003 total: FY2026 book 1,120,000, FY2025 book 1,010,000 | 2025 approved RM0 AFO005 total: FY2026 book 567,000, FY2025 book 577,000 | 2025 approved RM0 AFO000 total: FY2026 book 2,378,000, FY2025 book 2,278,000 | 2025 approved RM0 H04201 total: FY2026 book 175,000, FY2025 book 179,000 | 2025 approved RM0 H04202 total: FY2026 book 1,128,000, FY2025 book 1,151,000 | 2025 approved RM0 H04205 total: FY2026 book 381,000, FY2025 book 355,000 | 2025 approved RM0 H04504 total: FY2026 book 1,367,000, FY2025 book 100,000 | 2025 approved RM0 HS0045 total: FY2026 book 37,390,000, FY2025 book 36,123,000 | 2025 approved RM0 H04802 total: FY2026 book 27,140,000, FY2025 book 22,840,000 | 2025 approved RM0 H04805 total: FY2026 book 1,391,000, FY2025 book 5,691,000 | 2025 approved RM0 HS0053 total: FY2026 book 20,351,000, FY2025 book 21,717,000 | 2025 approved CF0 AFO003 total: FY2026 book 2,141,000, FY2025 book 2,222,000 | 2025 approved CF0 AFO000 total: FY2026 book 4,023,000, FY2025 book 4,104,000 | 2025 approved CF0 AMP026 total: FY2026 book 0, FY2025 book -3,000 | 2025 approved CF0 AMP000 total: FY2026 book 24,947,000, FY2025 book 24,944,000 | 2025 approved CF0 O00111 total: FY2026 book 556,000, FY2025 book 559,000 | 2025 approved CF0 GO0047 total: FY2026 book 6,545,000, FY2025 book 6,548,000 | 2025 approved CF0 O05201 total: FY2026 book 15,504,000, FY2025 book 15,422,000 | 2025 approved CF0 GO0052 total: FY2026 book 75,929,000, FY2025 book 75,847,000
- FY2024 old-code -> FY2025 code crosswalk (FY2024 approved): FO0 P02301: FY2024 book 171,000 vs FY2025 book restated 171,000 (delta +0) | FO0 P02303: FY2024 book 45,515,000 vs FY2025 book restated 45,515,000 (delta +0) | FO0 P04502: FY2024 book 3,720,000 vs FY2025 book restated 3,720,000 (delta +0) | HY0 R03903: FY2024 book 4,400,000 vs FY2025 book restated 4,400,000 (delta +0) | HY0 R03904: FY2024 book 0 vs FY2025 book restated 0 (delta +0) | HY0 R03905: FY2024 book 128,094,000 vs FY2025 book restated 128,094,000 (delta +0) | HY0 R03906: FY2024 book 10,581,000 vs FY2025 book restated 10,581,000 (delta +0) | HY0 R03907: FY2024 book 43,296,000 vs FY2025 book restated 43,296,000 (delta +0) | JA0 H03002: FY2024 book 79,033,000 vs FY2025 book restated 93,339,000 (delta +14,306,000) | JA0 H03003: FY2024 book 59,994,000 vs FY2025 book restated 59,994,000 (delta +0) | JA0 H03004: FY2024 book 31,818,000 vs FY2025 book restated 12,421,000 (delta -19,397,000) | JA0 H03007: FY2024 book 2,940,000 vs FY2025 book restated 2,940,000 (delta +0) | JA0 H03008: FY2024 book 42,536,000 vs FY2025 book restated 42,536,000 (delta +0) | JA0 H03009: FY2024 book 2,799,000 vs FY2025 book restated 4,259,000 (delta +1,460,000) | JA0 H03010: FY2024 book 51,764,000 vs FY2025 book restated 60,770,000 (delta +9,006,000) | JA0 H03011: FY2024 book 4,935,000 vs FY2025 book restated 4,935,000 (delta +0) | JA0 H03012: FY2024 book 86,929,000 vs FY2025 book restated 83,014,000 (delta -3,915,000) | JA0 H03013: FY2024 book 4,222,000 vs FY2025 book restated 4,222,000 (delta +0) | JA0 H03014-H03016: FY2024 book 11,541,000 vs FY2025 book restated 11,542,000 (delta +1,000) | JA0 H03017: FY2024 book 73,209,000 vs FY2025 book restated 73,209,000 (delta +0) | JA0 H03018: FY2024 book 10,875,000 vs FY2025 book restated 10,875,000 (delta +0) | JA0 H03019: FY2024 book 1,150,000 vs FY2025 book restated 1,150,000 (delta +0) | JA0 H03022: FY2024 book 1,980,000 vs FY2025 book restated 1,980,000 (delta +0) | JA0 H03023: FY2024 book 12,032,000 vs FY2025 book restated 12,032,000 (delta +0) | RM0 H04308: FY2024 book 29,637,000 vs FY2025 book restated 29,637,000 (delta +0) | RM0 H04504: FY2024 book 1,467,000 vs FY2025 book restated 1,467,000 (delta +0)
- event dates: budget_enacted/budget_revised = Local Budget Act 2nd reading {2024: '2023-05-30', 2025: '2024-06-12', 2026: '2025-07-28', 2027: '2026-06-23'}; budget_proposed = BSA introduced on behalf of the Mayor {2025: '2024-04-03', 2026: '2025-06-02', 2027: '2026-04-14'} (FY2024 proposal date not in downloaded docs -> blank); BSA policy rows = law/act effective date {2024: '2023-09-06', 2025: '2024-09-18', 2026: '2025-12-06', 2027: '2026-08-13'}; committee items = markup date when printed, else Local Budget Act date
- mapping: Table XX0-5 lines before 'Mayor's Proposed Budget' -> budget_proposed; lines between it and 'District's Approved Budget' -> budget_revised (Council changes); FY2027 Council-level changes taken from the activity-level Council chart instead of JA0-5 to avoid double counting
- coverage (stage[+funds] by FY x agency JA0/FO0/RM0/DB0/HY0/CF0/HG0):
| FY2021 | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds |
| FY2022 | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds |
| FY2023 | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds |
| FY2024 | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds |
| FY2025 | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds,prop | actu+funds,appr+funds | actu+funds,appr+funds |
| FY2026 | appr+funds,prop | appr+funds,prop | appr+funds | appr+funds | appr+funds,prop | appr+funds | appr+funds |
| FY2027 | appr+funds | appr+funds | appr+funds,prop | appr+funds | appr+funds,prop | appr+funds | appr+funds |
- warnings (0):

### 2026-10-10 13:50 — 30_fetch_xml: progress
- pass 1: 18,000/31,469 done in 20.0 min (15.0/s); 1,439 MB on disk for done files; ok 18,000, not_found 0, error 0

### 2026-10-10 13:50 — 43_web_calvary
- support page: 98 organizations (3 flagged in-kind); Phase 1 PDF had 98 (11 truncated). Names absent from the PDF parse: 11
- truncated names recovered: Morris, Mann -> Morris, Manning & Martin, LLP; Nelson Mulli -> Nelson Mullins; NFP Golden & -> NFP Golden & Cohen; Robert Charle -> Robert Charles Lesser Co.; Sapodilla's C -> Sapodilla's Caribbean Restaurant and Catering; Saul Ewing A -> Saul Ewing Arnstein & Lehr LLP; Southern Com -> Southern Company; The Brand Gu -> The Brand Guild; The Menkiti G -> The Menkiti Group; United Bank -> United Bank; Women's Ene -> Women's Energy Resource Council
- PDFs seen: 98 (financials page links + WP media library + off-site search); kept as new: 22: 2015-07-Corporate-Partner-Program-packet.pdf [funder_list, ok]; CWS-Audited-Financial-Statements-2014.pdf [audit, ok]; CWS-Form-990-2014.pdf [form_990, ok]; CWS-form-990-2013.pdf [form_990, ok]; Corporate-Partners-Program-packet.pdf [funder_list, ok]; Corporate-Partners-Program-packet_11-11-2014.pdf [funder_list, ok]; Corporate-Partners-Program-packet_11-13-2014.pdf [funder_list, ok]; FY2013-Annual-Report-simple-version-FINAL.pdf [annual_report, ok]; What-Do-Corporate-Partners-Do_combined.pdf [funder_list, ok]; audited-statements-2013.pdf [audit, ok]; Calvary-Womens-Services-2014-Annual-Report.pdf [annual_report, ok]; 2017-Hope-Awards-Sponsorship-Opportunities.pdf [funder_list, ok]; Step-Up-DC-2016-Year-End-Report.pdf [funder_list, ok]; 2019-02-04-Calvary-Annual-Design.pdf [annual_report, ok]; Calvary-Womens-Services-FY18-Annual-Report.pdf [annual_report, ok]; CWS-Corporate-Partners-Program-Overview.pdf [funder_list, ok]; Hope-Awards-Sponsors.pdf [funder_list, ok]; 2024-Corporate-Partners-Program-Opportunities_CWS.pdf [funder_list, ok]; 2025-Hope-Gala-Sponsorship_CWS-2.pdf [funder_list, ok]; 2025-Hope-Gala-Sponsorship_CWS-2.pdf [funder_list, duplicate_of_web:https://www.calvaryservices.org/wp-content/uploads/2025/02/2025-Hope-Gala-Sponsorship_CWS-2.pdf]; Calvary-Newsletter-02_25.pdf [funder_list, ok]; 521307706_2022_25813620221_A133.pdf [other, ok; found by cal_audit_fy24]
- off-site search hits: 104 results; Calvary PDFs kept: 1; rejected: Calvary-Independent-Auditors-Report.pdf (cal_audit_fy25: not a Calvary Women's Services document)
- annual-report donors: 72 org rows; named lists/mentions 87 rows; individual band-count rows 3; Calvary-Womens-Services-2014-Annual-Report.pdf: 72 org donor entries, 182 individual entries (counted only); 2017-Hope-Awards-Sponsorship-Opportunities.pdf [Hope Awards Dinner: companies that have sponsored (cumulative)]: 41; Step-Up-DC-2016-Year-End-Report.pdf [Step Up DC supporters ('supported the program this year')]: 4; 2025-Hope-Gala-Sponsorship_CWS-2.pdf [Hope Gala: Past Event Sponsors (cumulative)]: 39
- new audits: 314 financial/note rows, 4 SEFA rows; CWS-Audited-Financial-Statements-2014.pdf: no SEFA in the PDF; 521307706_2022_25813620221_A133.pdf: SEFA p29 4 programs sum 4,067,718 vs printed total 4,067,718
- this run: Tavily search 0, extract 0, HTTP GET 14, cache hits 41; cumulative (manifest): search 104/300, extract 7/200, HTTP 104

### 2026-10-10 13:51 — 37_parse_dc_budget: DC budget lines and policy events
- interim/stage_dc_budget_lines__dc.csv: 5,172 rows (Counter({'approved': 3172, 'actual': 1968, 'proposed': 32})); in-scope program/agency rows 854; duplicate keys 0
- interim/stage_fact_policy_events__dc.csv: 297 rows; by kind {'change_table_FO0-5': 8, 'change_table_HY0-5': 9, 'change_table_JA0-5': 25, 'yoy_approved_change': 161, 'bsa_subtitle': 25, 'fy2025_change_narrative': 13, 'committee_report_item': 22, 'committee_report_variance': 6, 'change_table_DB0-5': 1, 'council_adjustments_chart_fy2027': 27}; by type {'budget_proposed': 41, 'budget_enacted': 161, 'budget_revised': 66, 'policy_change': 26, 'other': 1, 'program_launch': 2}
- parsed tables: FY2024 JA0 30-PBB (2024_JA0_ja_dhs_tables_2024j.pdf): 62 lines; FY2024 FO0 30-PBB (024_FO0_fo_vsjg_tables_2024j.pdf): 21 lines; FY2024 RM0 30-PBB (2024_RM0_rm_dbh_tables_2024j.pdf): 128 lines; FY2024 DB0 30-PBB (024_DB0_db_dhcd_tables_2024j.pdf): 44 lines; FY2024 HY0 30-PBB (2024_HY0_hy_has_tables_2024j.pdf): 16 lines; FY2024 CF0 30-PBB (2024_CF0_cf_des_tables_2024j.pdf): 69 lines; FY2024 HG0 30-PBB (24_HG0_hg_dmhhs_tables_2024j.pdf): 9 lines; FY2025 JA0 30-PBB (2025_JA0_ja_dhs_tables_2025j.pdf): 61 lines; FY2025 FO0 30-PBB (25_FO0_fo_ovsjg_tables_2025j.pdf): 28 lines; FY2025 RM0 30-PBB (2025_RM0_rm_dbh_tables_2025j.pdf): 87 lines; FY2025 DB0 30-PBB (025_DB0_db_dhcd_tables_2025j.pdf): 36 lines; FY2025 HY0 30-PBB (2025_HY0_hy_hap_tables_2025j.pdf): 7 lines; FY2025 CF0 30-PBB (025_CF0_cf_does_tables_2025j.pdf): 62 lines; FY2025 HG0 30-PBB (25_HG0_hg_dmhhs_tables_2025j.pdf): 8 lines; FY2026 JA0 Table JA0-4 (026_JA0_ja_dhs_chapter_2026o.pdf): 57 lines; FY2026 FO0 Table FO0-4 (26_FO0_fo_vsjg_chapter_2026o.pdf): 26 lines; FY2026 RM0 Table RM0-4 (026_RM0_rm_dbh_chapter_2026o.pdf): 83 lines; FY2026 DB0 Table DB0-4 (26_DB0_db_dhcd_chapter_2026o.pdf): 36 lines; FY2026 HY0 Table HY0-4 (026_HY0_hy_has_chapter_2026o.pdf): 7 lines; FY2026 CF0 Table CF0-4 (26_CF0_cf_does_chapter_2026o.pdf): 61 lines; FY2026 HG0 Table HG0-4 (6_HG0_hg_dmhhs_chapter_2026o.pdf): 6 lines; FY2027 JA0 30-PBB (7_JA0_ja0_dhs_tables_2027a_0.pdf): 57 lines; FY2027 FO0 30-PBB (FO0_fo0_ovsjg_tables_2027a_0.pdf): 26 lines; FY2027 RM0 30-PBB (7_RM0_rm0_dbh_tables_2027a_0.pdf): 80 lines; FY2027 DB0 30-PBB (_DB0_db0_dhcd_tables_2027a_0.pdf): 36 lines; FY2027 HY0 30-PBB (7_HY0_hy0_hap_tables_2027a_0.pdf): 7 lines; FY2027 CF0 30-PBB (_CF0_cf0_does_tables_2027a_0.pdf): 61 lines; FY2027 HG0 30-PBB (HG0_hg0_dmhhs_tables_2027a_0.pdf): 7 lines
- change items: FY2024 JA0 Table JA0-5: 29 change lines, 7 in scope; FY2024 FO0 Table FO0-5: 14 change lines, 3 in scope; FY2024 RM0 Table RM0-5: 25 change lines, 0 in scope; FY2024 DB0 Table DB0-5: 14 change lines, 0 in scope; FY2024 HY0 Table HY0-5: 6 change lines, 6 in scope; FY2024 CF0 Table CF0-5: 16 change lines, 0 in scope; FY2024 HG0 Table HG0-5: 7 change lines, 0 in scope; FY2025 JA0 narrative change sentences (pypdfium2): 8 in scope; FY2025 FO0: chapter change text is font-garbled (amounts missing); OVSJG FY2025 changes taken from the JPS committee report; FY2025 RM0 narrative change sentences (pypdfium2): 0 in scope; FY2025 DB0 narrative change sentences (pypdfium2): 2 in scope; FY2025 HY0 narrative change sentences (pypdfium2): 3 in scope; FY2025 CF0 Table CF0-5: 20 change lines, 0 in scope; FY2025 HG0 narrative change sentences (pypdfium2): 0 in scope; FY2026 JA0 Table JA0-5: 29 change lines, 14 in scope; FY2026 FO0 Table FO0-5: 16 change lines, 4 in scope; FY2026 RM0 Table RM0-5: 27 change lines, 0 in scope; FY2026 DB0 Table DB0-5: 16 change lines, 0 in scope; FY2026 HY0 Table HY0-5: 2 change lines, 2 in scope; FY2026 CF0 Table CF0-5: 17 change lines, 0 in scope; FY2026 HG0 Table HG0-5: 4 change lines, 0 in scope; FY2027 JA0 Table JA0-5: 15 change lines, 4 in scope; FY2027 FO0 Table FO0-5: 11 change lines, 1 in scope; FY2027 RM0 Table RM0-5: 17 change lines, 0 in scope; FY2027 DB0 Table DB0-5: 15 change lines, 1 in scope; FY2027 HY0 Table HY0-5: 3 change lines, 1 in scope; FY2027 CF0 Table CF0-5: 8 change lines, 0 in scope; FY2027 HG0 Table HG0-5: 3 change lines, 0 in scope
- committee report tables: BR_FY25_Housing -> 1 in-scope proposed activity rows (markup 2024-05-09); BR_FY25_JPS -> 0 in-scope proposed activity rows (markup not printed); BR_FY26_committee_budget_report_Human-Services -> 18 in-scope proposed activity rows (markup 2025-06-24); BR_FY26_committee_budget_report_Housing -> 5 in-scope proposed activity rows (markup 2025-06-24); BR_FY26_committee_budget_report_JPS -> 2 in-scope proposed activity rows (markup not printed); BR_FY26_committee_budget_report_Health -> 0 in-scope proposed activity rows (markup 2025-06-23); BR_FY27_committee_budget_report_DRAFT-FY2027-Committee-on-Health -> 2 in-scope proposed activity rows (markup 2026-05-20); BR_FY27_committee_budget_report_FY27-Committee-on-Housing -> 4 in-scope proposed activity rows (markup not printed); BR_FY27_committee_budget_report_52226-FY2027-JPS -> 0 in-scope proposed activity rows (markup not printed)
- FY2027 Council adjustments chart: 1627 rows read, 27 in-scope events
- BSA subtitles kept: 25; curated committee-report items: 22; YoY approved-change events: 161
- tie-outs: 257 pass, 0 fail
- tie-out detail (in-scope divisions): FY2024 JA0 30-PBB p2 division 5000: sum of 23 activities vs subtotal, deltas by column [0, 0, 0, -1] ($000) -> pass | FY2024 JA0 30-PBB p3 agency total: sum of 8 division subtotals, deltas [0, -2, 0, 1] ($000) -> pass | FY2024 JA0 Table JA0-2 p2: sum of 7 fund rows vs GROSS FUNDS, deltas [-1, 0, -1, 0] ($000) -> pass | FY2024 FO0 30-PBB p1 division 4000: sum of 2 activities vs subtotal, deltas by column [0, 0, 0, -1] ($000) -> pass | FY2024 FO0 30-PBB p1 division 5000: sum of 1 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 FO0 30-PBB p1 division 6000: sum of 5 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 FO0 30-PBB p1 agency total: sum of 7 division subtotals, deltas [-2, -1, -2, 1] ($000) -> pass | FY2024 FO0 Table FO0-2 p2: sum of 5 fund rows vs GROSS FUNDS, deltas [0, 0, -1, 0] ($000) -> pass | FY2024 RM0 30-PBB p5 agency total: sum of 16 division subtotals, deltas [0, 1, 1, 0] ($000) -> pass | FY2024 RM0 Table RM0-2 p2: sum of 9 fund rows vs GROSS FUNDS, deltas [0, 1, 0, 1] ($000) -> pass | FY2024 DB0 30-PBB p2 agency total: sum of 9 division subtotals, deltas [0, 0, 0, -1] ($000) -> pass | FY2024 DB0 Table DB0-2 p2: sum of 5 fund rows vs GROSS FUNDS, deltas [1, -1, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 division 4000: sum of 1 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 division 5000: sum of 1 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 division 6000: sum of 5 activities vs subtotal, deltas by column [2, -1, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 agency total: sum of 5 division subtotals, deltas [0, 0, -1, 0] ($000) -> pass | FY2024 HY0 Table HY0-2 p1: sum of 1 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2024 CF0 30-PBB p2 division 4000: sum of 16 activities vs subtotal, deltas by column [0, 0, 0, -1] ($000) -> pass | FY2024 CF0 30-PBB p2 division 5000: sum of 3 activities vs subtotal, deltas by column [1, 0, 1, 0] ($000) -> pass | FY2024 CF0 30-PBB p2 division 6000: sum of 6 activities vs subtotal, deltas by column [1, 0, 0, 0] ($000) -> pass | FY2024 CF0 30-PBB p3 agency total: sum of 11 division subtotals, deltas [-1, 0, 0, -1] ($000) -> pass | FY2024 CF0 Table CF0-2 p2: sum of 6 fund rows vs GROSS FUNDS, deltas [1, 0, 0, 0] ($000) -> pass | FY2024 HG0 30-PBB p1 agency total: sum of 4 division subtotals, deltas [0, 0, 0, 0] ($000) -> pass | FY2024 HG0 Table HG0-2 p2: sum of 2 fund rows vs GROSS FUNDS, deltas [0, 1, 0, 0] ($000) -> pass | FY2025 JA0 30-PBB p2 division HS0030: sum of 28 activities vs subtotal, deltas by column [-2, 1, -1, 1] ($000) -> pass | FY2025 JA0 30-PBB p2 agency total: sum of 6 division subtotals, deltas [0, -1, 1, 0] ($000) -> pass | FY2025 FO0 30-PBB p1 division PS0023: sum of 2 activities vs subtotal, deltas by column [0, 0, -1, 0] ($000) -> pass | FY2025 FO0 30-PBB p2 agency total: sum of 12 division subtotals, deltas [-1, -2, 1, 0] ($000) -> pass | FY2025 RM0 30-PBB p3 agency total: sum of 13 division subtotals, deltas [1, 1, 0, 1] ($000) -> pass | FY2025 DB0 30-PBB p2 agency total: sum of 6 division subtotals, deltas [0, 1, 1, 0] ($000) -> pass | FY2025 HY0 30-PBB p1 division EC0039: sum of 5 activities vs subtotal, deltas by column [0, -1, 0, 0] ($000) -> pass | FY2025 HY0 30-PBB p1 agency total: sum of 1 division subtotals, deltas [0, 0, 0, 0] ($000) -> pass | FY2025 CF0 30-PBB p3 agency total: sum of 10 division subtotals, deltas [0, -1, 0, -1] ($000) -> pass | FY2025 CF0 Table CF0-2 p2: sum of 6 fund rows vs GROSS FUNDS, deltas [0, -1, 0, 0] ($000) -> pass | FY2025 HG0 30-PBB p1 agency total: sum of 3 division subtotals, deltas [0, 0, 0, 1] ($000) -> pass | FY2026 JA0 Table JA0-4 p5 division HS0030: sum of 28 activities vs subtotal, deltas [1, -2, 1, -1] ($000) -> pass | FY2026 JA0 Table JA0-4 p5 agency total: sum of 5 divisions, deltas [-1, -1, 0, 0] ($000) -> pass | FY2026 JA0 Table JA0-2 p2: sum of 7 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 FO0 Table FO0-4 p4 division PS0023: sum of 2 activities vs subtotal, deltas [0, 1, 0, 0] ($000) -> pass | FY2026 FO0 Table FO0-4 p4 agency total: sum of 11 divisions, deltas [-2, 0, 0, 0] ($000) -> pass | FY2026 FO0 Table FO0-2 p2: sum of 4 fund rows vs GROSS FUNDS, deltas [-1, 0, 0, 0] ($000) -> pass | FY2026 RM0 Table RM0-4 p7 agency total: sum of 13 divisions, deltas [1, 1, 2, 0] ($000) -> pass | FY2026 RM0 Table RM0-2 p2: sum of 8 fund rows vs GROSS FUNDS, deltas [1, 0, -1, 0] ($000) -> pass | FY2026 DB0 Table DB0-4 p4 agency total: sum of 6 divisions, deltas [1, -1, 0, -1] ($000) -> pass | FY2026 DB0 Table DB0-2 p2: sum of 4 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 HY0 Table HY0-4 p2 division EC0039: sum of 5 activities vs subtotal, deltas [-1, 1, 0, 0] ($000) -> pass | FY2026 HY0 Table HY0-4 p2 agency total: sum of 1 divisions, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 HY0 Table HY0-2 p1: sum of 1 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 CF0 Table CF0-4 p5 agency total: sum of 10 divisions, deltas [-1, 1, 0, 0] ($000) -> pass | FY2026 CF0 Table CF0-2 p2: sum of 5 fund rows vs GROSS FUNDS, deltas [-1, 1, 0, 1] ($000) -> pass | FY2026 HG0 Table HG0-4 p3 agency total: sum of 2 divisions, deltas [0, 1, 1, 0] ($000) -> pass | FY2026 HG0 Table HG0-2 p2: sum of 1 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2027 JA0 30-PBB p2 division HS0030: sum of 28 activities vs subtotal, deltas by column [-2, -2, -1, -3] ($000) -> pass | FY2027 JA0 30-PBB p2 agency total: sum of 5 division subtotals, deltas [-1, 1, 0, -1] ($000) -> pass | FY2027 JA0 Table JA0-2 p2: sum of 7 fund rows vs GROSS FUNDS, deltas [0, 1, 0, 0] ($000) -> pass | FY2027 FO0 30-PBB p1 division PS0023: sum of 2 activities vs subtotal, deltas by column [1, 0, 0, 0] ($000) -> pass | FY2027 FO0 30-PBB p1 agency total: sum of 11 division subtotals, deltas [-1,
- cross-book disagreements (same FY/stage/code, >$2K apart; later book preferred via x_preferred): 2022 actual JA0 AMP000 total: FY2025 book 33,466,000, FY2024 book 33,534,000 | 2022 actual JA0 AFO000 total: FY2025 book 3,079,000, FY2024 book 3,025,000 | 2022 actual JA0 HS0029 total: FY2025 book 279,438,000, FY2024 book 280,259,000 | 2022 actual JA0 HS0030 total: FY2025 book 625,848,000, FY2024 book 625,869,000 | 2025 approved JA0 H02902 total: FY2026 book 42,867,000, FY2025 book 42,943,000 | 2025 approved JA0 H02905 total: FY2026 book 91,735,000, FY2025 book 91,660,000 | 2025 approved FO0 P01903 total: FY2026 book 18,405,000, FY2025 book 18,312,000 | 2025 approved FO0 PS0019 total: FY2026 book 18,405,000, FY2025 book 18,312,000 | 2025 approved RM0 AFO003 total: FY2026 book 1,120,000, FY2025 book 1,010,000 | 2025 approved RM0 AFO005 total: FY2026 book 567,000, FY2025 book 577,000 | 2025 approved RM0 AFO000 total: FY2026 book 2,378,000, FY2025 book 2,278,000 | 2025 approved RM0 H04201 total: FY2026 book 175,000, FY2025 book 179,000 | 2025 approved RM0 H04202 total: FY2026 book 1,128,000, FY2025 book 1,151,000 | 2025 approved RM0 H04205 total: FY2026 book 381,000, FY2025 book 355,000 | 2025 approved RM0 H04504 total: FY2026 book 1,367,000, FY2025 book 100,000 | 2025 approved RM0 HS0045 total: FY2026 book 37,390,000, FY2025 book 36,123,000 | 2025 approved RM0 H04802 total: FY2026 book 27,140,000, FY2025 book 22,840,000 | 2025 approved RM0 H04805 total: FY2026 book 1,391,000, FY2025 book 5,691,000 | 2025 approved RM0 HS0053 total: FY2026 book 20,351,000, FY2025 book 21,717,000 | 2025 approved CF0 AFO003 total: FY2026 book 2,141,000, FY2025 book 2,222,000 | 2025 approved CF0 AFO000 total: FY2026 book 4,023,000, FY2025 book 4,104,000 | 2025 approved CF0 AMP026 total: FY2026 book 0, FY2025 book -3,000 | 2025 approved CF0 AMP000 total: FY2026 book 24,947,000, FY2025 book 24,944,000 | 2025 approved CF0 O00111 total: FY2026 book 556,000, FY2025 book 559,000 | 2025 approved CF0 GO0047 total: FY2026 book 6,545,000, FY2025 book 6,548,000 | 2025 approved CF0 O05201 total: FY2026 book 15,504,000, FY2025 book 15,422,000 | 2025 approved CF0 GO0052 total: FY2026 book 75,929,000, FY2025 book 75,847,000
- FY2024 old-code -> FY2025 code crosswalk (FY2024 approved): FO0 P02301: FY2024 book 171,000 vs FY2025 book restated 171,000 (delta +0) | FO0 P02303: FY2024 book 45,515,000 vs FY2025 book restated 45,515,000 (delta +0) | FO0 P04502: FY2024 book 3,720,000 vs FY2025 book restated 3,720,000 (delta +0) | HY0 R03903: FY2024 book 4,400,000 vs FY2025 book restated 4,400,000 (delta +0) | HY0 R03904: FY2024 book 0 vs FY2025 book restated 0 (delta +0) | HY0 R03905: FY2024 book 128,094,000 vs FY2025 book restated 128,094,000 (delta +0) | HY0 R03906: FY2024 book 10,581,000 vs FY2025 book restated 10,581,000 (delta +0) | HY0 R03907: FY2024 book 43,296,000 vs FY2025 book restated 43,296,000 (delta +0) | JA0 H03002: FY2024 book 79,033,000 vs FY2025 book restated 93,339,000 (delta +14,306,000) | JA0 H03003: FY2024 book 59,994,000 vs FY2025 book restated 59,994,000 (delta +0) | JA0 H03004: FY2024 book 31,818,000 vs FY2025 book restated 12,421,000 (delta -19,397,000) | JA0 H03007: FY2024 book 2,940,000 vs FY2025 book restated 2,940,000 (delta +0) | JA0 H03008: FY2024 book 42,536,000 vs FY2025 book restated 42,536,000 (delta +0) | JA0 H03009: FY2024 book 2,799,000 vs FY2025 book restated 4,259,000 (delta +1,460,000) | JA0 H03010: FY2024 book 51,764,000 vs FY2025 book restated 60,770,000 (delta +9,006,000) | JA0 H03011: FY2024 book 4,935,000 vs FY2025 book restated 4,935,000 (delta +0) | JA0 H03012: FY2024 book 86,929,000 vs FY2025 book restated 83,014,000 (delta -3,915,000) | JA0 H03013: FY2024 book 4,222,000 vs FY2025 book restated 4,222,000 (delta +0) | JA0 H03014-H03016: FY2024 book 11,541,000 vs FY2025 book restated 11,542,000 (delta +1,000) | JA0 H03017: FY2024 book 73,209,000 vs FY2025 book restated 73,209,000 (delta +0) | JA0 H03018: FY2024 book 10,875,000 vs FY2025 book restated 10,875,000 (delta +0) | JA0 H03019: FY2024 book 1,150,000 vs FY2025 book restated 1,150,000 (delta +0) | JA0 H03022: FY2024 book 1,980,000 vs FY2025 book restated 1,980,000 (delta +0) | JA0 H03023: FY2024 book 12,032,000 vs FY2025 book restated 12,032,000 (delta +0) | RM0 H04308: FY2024 book 29,637,000 vs FY2025 book restated 29,637,000 (delta +0) | RM0 H04504: FY2024 book 1,467,000 vs FY2025 book restated 1,467,000 (delta +0)
- event dates: budget_enacted/budget_revised = Local Budget Act 2nd reading {2024: '2023-05-30', 2025: '2024-06-12', 2026: '2025-07-28', 2027: '2026-06-23'}; budget_proposed = BSA introduced on behalf of the Mayor {2025: '2024-04-03', 2026: '2025-06-02', 2027: '2026-04-14'} (FY2024 proposal date not in downloaded docs -> blank); BSA policy rows = law/act effective date {2024: '2023-09-06', 2025: '2024-09-18', 2026: '2025-12-06', 2027: '2026-08-13'}; committee items = markup date when printed, else Local Budget Act date
- mapping: Table XX0-5 lines before 'Mayor's Proposed Budget' -> budget_proposed; lines between it and 'District's Approved Budget' -> budget_revised (Council changes); FY2027 Council-level changes taken from the activity-level Council chart instead of JA0-5 to avoid double counting
- coverage (stage[+funds] by FY x agency JA0/FO0/RM0/DB0/HY0/CF0/HG0):
| FY2021 | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds |
| FY2022 | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds |
| FY2023 | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds |
| FY2024 | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds |
| FY2025 | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds,prop | actu+funds,appr+funds | actu+funds,appr+funds |
| FY2026 | appr+funds,prop | appr+funds,prop | appr+funds | appr+funds | appr+funds,prop | appr+funds | appr+funds |
| FY2027 | appr+funds | appr+funds | appr+funds,prop | appr+funds | appr+funds,prop | appr+funds | appr+funds |
- warnings (0):

### 2026-10-10 13:52 — 38_parse_hud_counts
- wrote interim/stage_homeless_counts__hud.csv: 49,393 rows ({'bulk_hud_ahar_pit_hic': 48224, 'doc_hud_hic_dc500': 428, 'doc_mwcog_pit': 741}); PIT 39,029, HIC by CoC 9,195, PopSub 428, MWCOG 741
- wrote interim/stage_hic_projects__hud.csv: 1,257 rows (2022: 332, 2023: 292, 2024: 323, 2025: 310)
- HIC project PDFs: provider and facility names are truncated in the PDF itself (fixed-width report cells; same text in pdfplumber chars, pypdf and pdftotext); kept as printed. 'units' = family units (HIC reports units only for households with children). target_population is derived from the bed columns (household type, plus youth/veterans/chronic when all beds are dedicated) and set to single_women / women_with_children only when the provider or project name says women (basis in x_target_population_basis). x_women_focused_org = core peer tier 1a or Calvary; x_dv_focused_org = tier 1b (config/core_peers.csv).
- PIT by CoC (raw/hud/20261010T123731_huduser_2007-2025-PIT-Counts-by-CoC.xlsb): sheets 2007-2025; 39,029 rows for 8 CoCs; unparsed column names 216 (e.g. ['Overall Homeless - Under 18', 'Overall Homeless - Age 18 to 24', 'Overall Homeless - Over 24']); CoC-years absent: none
- partial unsheltered counts (Count Types): MD-601 2021; VA-602 2021
- workbook has no gender columns in any year (only age, race/ethnicity, household and subpopulation splits); DC gender comes from PopSub 2024 and the MWCOG 2025 DC narrative
- HIC by CoC (raw/hud/20261010T123733_huduser_2007-2025-HIC-Counts-by-CoC.xlsx): sheets 2007-2025; 9,195 rows; unparsed columns 9 (['HMIS Participation Rate (ES,TH) (non-numeric)', 'ES HMIS Participation Rate (non-numeric)', 'Total TH Beds for Households with only Children (non-numeric)', 'HMIS Participation Rate for Year-Round Beds (SH) (non-numeric)']); same-measure columns with different values kept as '__alt': 0
- PopSub DC-500 2024 (raw/hud/20261010T123749_hudx_CoC_PopSub_DC-500_2024.pdf): 232 rows; total persons 5616; women 2167
- PopSub DC-500 2025 (raw/hud/20261010T123750_hudx_CoC_PopSub_DC-500_2025.pdf): 196 rows; total persons 5138; women n/a
- MWCOG 2023 report (raw/hud/20261010T123754_mwcog_homelessness_metro_washington_2023_PIT.pdf): 548 table cells kept
- MWCOG 2024 report (raw/hud/20261010T123753_mwcog_homelessness_metro_washington_2024_PIT.pdf): 504 table cells kept
- MWCOG 2025 report (raw/hud/20261010T123752_mwcog_homelessness_metro_washington_2025_PIT.pdf): 520 table cells kept
- MWCOG 2026 report (raw/hud/20261010T123751_mwcog_homelessness_metro_washington_2026_PIT.pdf): 531 table cells kept
- MWCOG: 2103 cells parsed across reports -> 741 after keeping the latest report per jurisdiction/year/measure/population; values revised between reports: 38 (e.g. Prince William County, VA 2022 all: 241 (rpt 2023) -> 282 (rpt 2024); Prince William County, VA 2021 all: 282 (rpt 2023) -> 326 (rpt 2024); Prince William County, VA 2020 all: 326 (rpt 2023) -> 277 (rpt 2024); COG region 2023 households_without_children: 5901 (rpt 2023) -> 5755 (rpt 2024)); same report, two tables disagree (earlier page kept): 17 (District of Columbia 2020 households_with_only_children rpt 2023: p68 12 vs p25 11; Frederick City & County, MD 2021 households_with_only_children rpt 2023: p68 5 vs p25 0; COG region 2020 households_with_only_children rpt 2023: p69 13 vs p25 12; City of Alexandria, VA 2020 all rpt 2023: p68 198 vs p17 207)
- skipped tables (did not parse reliably): none; source-inconsistent columns are kept with confidence medium and an x_note
- not parsed: figures/charts (demographic profiles, income, gender charts), Table 3 population shares, Table 13/14 shelter status, TAY tables, Table 16 bed inventory, Table 17 formerly homeless in PH, Appendix B narrative percentages except the 2025 DC gender-of-adults table
- HIC provider names (cleaned, distinct): 105; matched 43 (41%); methods {'unmatched': 62, 'fuzzy_token_set': 11, 'exact_norm_name': 29, 'manual_known_ein': 2, 'manual_alias': 1}; government providers (no EIN expected) 7; beds at matched providers 67,575 of 133,181 (51%)
- fuzzy matches: Access Housing -> 521918702 (100.0); Access Housing INC (AHI) (Agency) -> 521918702 (100.0); Catholic Charities -> 530196524 (100.0); Catholic Charities (Agency) -> 530196524 (100.0); Covenant House Washington -> 133537709 (100.0); Covenant House Washington (CHW)(Age -> 133537709 (100.0); East River Family Strengthening Collabor -> 522277915 (100.0); Edgewood-Brookland Family Support Col -> 522246995 (100.0); Edgewood/Brookland Family Support Col -> 522246995 (100.0); Far Southeast Family Strengthening Colla -> 522117070 (100.0); Georgia Avenue Family Support Collabor -> 522349433 (100.0); Operation Renewed Hope -> 453848293 (100.0); Survivors & Advocates for Empowerment -> 412226446 (100.0)
- unmatched nonprofit providers (not in dc_sector/dmv_sector/core_peers by name): 801 East Collaborative; Bradley & Associates; CCDC; CORE DC; Casa Ruby; Church of Epiphany; Church of the Epiphany; Collaborative Solutions for Communities; Communities Helping & Empowering Pat; Communities Helping and Empowering P; Community Solutions; Cornerstone Community; Dawn Deaf; Deaf Dawn; East of the River Family Support Collabor; Echelon Community Services; Far Southeast Family Support Collaborati; Healthy Babies; Healthy Babies Project; Hillcrest Children & Family Center; Hope and a Home; Institute for Emotional Regulation; Jaydot; Joseph's House; Jubilee Housing; KBEC Group, Inc; KBEC Group, Inc.; KC Community Services; Latin American Youth Center; MBI Health Services; Maximus; Metropolitan Education Solutions; Metropolitan Educational Solutions; North Capitol Collaborative Inc.; North Capitol Family Support Collaborati; Positive Kinship Bonding; SLS; SMYAL; Salvation Army; Sasha Bruce Youthwork; Sasha Bruce Youthworks; So Others Might Eat; Spring Leaf; St. Aloysius Roman Catholic Church; St. John's Community Community Servic; St. John's Community Services; Supporting & Mentoring Youth Advocate; Temple Micah; Temple Sinai; The Community Builders and Emory Bea; The Institute for Emotional Regulation, L; The Salvation Army; U.S. Vets; US Veterans Initiative; Wheeler Creek
- matcher (shared with script 36): manual aliases (TCP 521681401; DASH, DC SAFE, Housing Up), norm_name exact, then rapidfuzz token_set_ratio >= 92 (after expanding a truncated last token for raw names >= 30 chars) accepted only when fuzzy_ok() holds: both names >= 2 tokens, a shared non-generic token, no one-sided entity-marker token (foundation, fund, maryland, county, ...), and token containment (ratio >= 0.5) or prefix or only soft one-sided words or fuzz.ratio >= 90; reviewed reject list
- PopSub 2024 gender rows sum 5616 vs total 5616: pass
- MWCOG 2023 p16 'People Experiencing Literal Homelessness by Jurisdiction, 2022 - 2023': pass (2 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p17 'People Experiencing Literal Homelessness by Jurisdiction, 2019-2023': pass (5 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p22 '2023 Persons In Families Experiencing Homelessness by Jurisdiction': pass (4 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p23 'Change In Persons In Families Experiencing Homelessness by Jurisdictio': pass (5 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p25 'Households With Only Children Under Age 18 By Jurisdiction, 2020 - 202': pass (4 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p41 'Comparison of Unsheltered Single Adults By Jurisdiction, 2019 – 2023': pass (5 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p45 'Single Adults Experiencing Chronic Homelessness by Jurisdiction, 2019 ': pass (5 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p51 'Veterans Experiencing Homelessness By Jurisdiction, 2019 - 2023': pass (5 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 pp[68, 69] 'People Experiencing Literal Homelessness by Jurisdiction, 20': kept with flags: 14/20 columns do not add up in the source (2022 households_without_children 5,307 vs 5,273; 2022 households_with_adults_and_children 2,329 vs 2,322; 2022 all 7,646 vs 7,605); 2 jurisdiction-years whose household columns do not add up
- MWCOG 2024 p16 'People Experiencing Literal Homelessness by Jurisdiction, 2023 - 2024': pass (2 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p17 'People Experiencing Literal Homelessness by Jurisdiction, 2020-2024*': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p22 '2024 Persons in Families Experiencing Homelessness by Jurisdiction': pass (4 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p23 'Change in Persons in Families Experiencing Homelessness by Jurisdictio': kept with flags: 1/5 columns do not add up in the source (2020 persons_in_families 3,690 vs 3,760)
- MWCOG 2024 p29 'Households With Only Children Under Age 18 By Jurisdiction, 2020 - 202': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p49 'Unsheltered Single Adults Experiencing Homelessness by Jurisdiction, 2': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p52 'Single Adults Experiencing Chronic Homelessness by Jurisdiction, 2020 ': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p60 'Veterans Experiencing Homelessness by Jurisdiction, 2020 - 2024': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 pp[75, 76] 'People Experiencing Literal Homelessness by Jurisdiction, 20': kept with flags: 9/20 columns do not add up in the source (2022 households_without_children 5,154 vs 5,120; 2022 households_with_adults_and_children 2,272 vs 2,265; 2022 all 7,422 vs 7,395); 2 jurisdiction-years whose household columns do not add up
- MWCOG 2025 p17 'People Experiencing Literal Homelessness by Jurisdiction, 2024 - 2025': pass (2 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p18 'People Experiencing Literal Homelessness by Jurisdiction, 2021-2025*': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p22 '2025 Persons in Families Experiencing Homelessness by Jurisdiction': pass (4 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p23 'Change in Persons in Families Experiencing Homelessness by Jurisdictio': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p29 'Households With Only Children Under Age 18 By Jurisdiction, 2021 - 202': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p48 'Comparison of Unsheltered Single Adults by Jurisdiction, 2021 - 2025': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p51 'Single Adults Experiencing Chronic Homelessness by Jurisdiction, 2021 ': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p59 'Veterans Experiencing Homelessness by Jurisdiction, 2021 - 2025': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 pp[73, 74] 'People Experiencing Literal Homelessness by Jurisdiction, 20': pass (20 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p18 'People Experiencing Literal Homelessness by Jurisdiction, 2025-2026': pass (2 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p19 'People Experiencing Literal Homelessness by Jurisdiction, 2019-2026': pass (8 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p24 '2026 Persons in Families Experiencing Homelessness by Jurisdiction': pass (4 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p25 'Change in Persons in Families Experiencing Homelessness by Jurisdictio': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p32 'Households With Only Children Under Age 18 By Jurisdiction, 2022 – 202': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p50 'Comparison of Unsheltered Single Adults by Jurisdiction, 2022 – 2026': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p54 'Single Adults Experiencing Chronic Homelessness by Jurisdiction, 2022 ': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p59 'Veterans Experiencing Homelessness by Jurisdiction, 2022 – 2026': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 pp[79, 80] 'People Experiencing Literal Homelessness by Jurisdiction, 20': pass (20 year/measure columns, 8 jurisdictions + total)
- MWCOG total persons vs HUD PIT overall, CoC-years that differ: 9: MD-600 2020: MWCOG 453 vs HUD 466; MD-600 2021: MWCOG 537 vs HUD 535; MD-600 2022: MWCOG 571 vs HUD 533; MD-600 2023: MWCOG 659 vs HUD 595; MD-600 2024: MWCOG 658 vs HUD 650; MD-600 2025: MWCOG 608 vs HUD 588; VA-602 2019: MWCOG 169 vs HUD 167; VA-604 2019: MWCOG 277 vs HUD 280; VA-604 2025: MWCOG 392 vs HUD 393
- DC-500 MWCOG vs HUD by year: 2019 6,521/6521, 2020 6,380/6380, 2021 5,111/5111, 2022 4,410/4410, 2023 4,922/4922, 2024 5,616/5616, 2025 5,138/5138, 2026 5,363/n/a
- stage_homeless_counts duplicate keys (coc, jurisdiction, year, measure, population, source): 0
- DC-500 2025 recon values: pit_overall 5138 (exp 5138) pass; pit_sheltered_es 3275 (exp 3275) pass; pit_sheltered_th 1065 (exp 1065) pass; pit_unsheltered 798 (exp 798) pass; hic_beds_year_round__es_th_sh 4965 (exp 4965) pass; hic_beds_year_round__th 1385 (exp 1385) pass; hic_beds_year_round__psh 12696 (exp 12696) pass; hic_beds_year_round__rrh 6012 (exp 6012) pass
- HIC projects 2022 ES: 43 projects; total beds 5,159 vs Total row 5159; year-round 4,795 vs summary p1 4795 vs CoC workbook 4795: pass
- HIC projects 2022 SH: 1 projects; total beds 20 vs Total row 20; year-round 20 vs summary p1 20 vs CoC workbook 20: pass
- HIC projects 2022 TH: 71 projects; total beds 1,783 vs Total row 1783; year-round 1,783 vs summary p1 1783 vs CoC workbook 1783: pass
- HIC projects 2022 PSH: 148 projects; total beds 14,467 vs Total row 14467; year-round 14,467 vs summary p1 14467 vs CoC workbook 14467: pass
- HIC projects 2022 RRH: 34 projects; total beds 7,193 vs Total row 7193; year-round 7,193 vs summary p1 7193 vs CoC workbook 7193: pass
- HIC projects 2022 OPH: 35 projects; total beds 6,498 vs Total row 6498; year-round 6,498 vs summary p1 6498 vs CoC workbook 6498: pass
- HIC projects 2023 ES: 38 projects; total beds 4,026 vs Total row 4026; year-round 3,720 vs summary p1 3720 vs CoC workbook 3720: pass
- HIC projects 2023 SH: 1 projects; total beds 20 vs Total row 20; year-round 20 vs summary p1 20 vs CoC workbook 20: pass
- HIC projects 2023 TH: 65 projects; total beds 1,476 vs Total row 1476; year-round 1,476 vs summary p1 1476 vs CoC workbook 1476: pass
- HIC projects 2023 PSH: 138 projects; total beds 15,349 vs Total row 15349; year-round 15,349 vs summary p1 15349 vs CoC workbook 15349: pass
- HIC projects 2023 RRH: 35 projects; total beds 9,206 vs Total row 9206; year-round 9,206 vs summary p1 9206 vs CoC workbook 9206: pass
- HIC projects 2023 OPH: 15 projects; total beds 5,381 vs Total row 5381; year-round 5,381 vs summary p1 5381 vs CoC workbook 5381: pass
- HIC projects 2024 ES: 46 projects; total beds 4,000 vs Total row 4000; year-round 3,505 vs summary p1 3505 vs CoC workbook 3505: pass
- HIC projects 2024 SH: 1 projects; total beds 20 vs Total row 20; year-round 20 vs summary p1 20 vs CoC workbook 20: pass
- HIC projects 2024 TH: 70 projects; total beds 1,693 vs Total row 1693; year-round 1,693 vs summary p1 1693 vs CoC workbook 1693: pass
- HIC projects 2024 PSH: 154 projects; total beds 11,856 vs Total row 11856; year-round 11,856 vs summary p1 11856 vs CoC workbook 11856: pass
- HIC projects 2024 RRH: 33 projects; total beds 10,156 vs Total row 10156; year-round 10,156 vs summary p1 10156 vs CoC workbook 10156: pass
- HIC projects 2024 OPH: 19 projects; total beds 5,842 vs Total row 5842; year-round 5,842 vs summary p1 5842 vs CoC workbook 5842: pass
- HIC projects 2025 ES: 45 projects; total beds 3,954 vs Total row 3954; year-round 3,580 vs summary p1 3580 vs CoC workbook 3580: pass
- HIC projects 2025 TH: 64 projects; total beds 1,385 vs Total row 1385; year-round 1,385 vs summary p1 1385 vs CoC workbook 1385: pass
- HIC projects 2025 PSH: 159 projects; total beds 12,696 vs Total row 12696; year-round 12,696 vs summary p1 12696 vs CoC workbook 12696: pass
- HIC projects 2025 RRH: 26 projects; total beds 6,012 vs Total row 6012; year-round 6,012 vs summary p1 6012 vs CoC workbook 6012: pass
- HIC projects 2025 OPH: 16 projects; total beds 4,989 vs Total row 4989; year-round 4,989 vs summary p1 4989 vs CoC workbook 4989: pass
- stage_hic_projects duplicate keys (year, type, page, seq): 0
- Calvary HIC 2025 rows pass (7 projects, 124 beds); 2024 Sisters Rise PSH [24] (exp [24])

### 2026-10-10 13:52 — 40_geocode_orgs
- inputs: org_base 15,375 EINs; in scope 12,615 (universes calvary, core_peers, dc_sector, dmv_sector, dmv_funders, daf_sponsors); scope EINs missing from org_base: 0
- address source (in scope): {'irs_eo_bmf': 12545, 'irs_990_xml_filer': 69, 'none': 1}; PO box / mailing-only: 1,386; no street: 1
- MAR 2: 1,769 DC addresses, 0 calls, 1769 reused, 0 HTTP errors; accepted 1,745
- Census batch: pass 1 9,483 rows (0 new batches, 4 reused); retry 619 rows (ZIP dropped), 38 matched on retry, 2 retry matches rejected (outside the original ZIP and county)
- match rates by method (in scope, n=12,615): census_geocoder 8,902 (70.6%); mar2 1,745 (13.8%); zcta_primary_county 1,351 (10.7%); city_modal_county 586 (4.6%); unresolved 31 (0.2%)
  - DC: 1,877 orgs, 1,769 with a street address, 1,758 point-geocoded (93.7% of all, 99.4% of street addresses); {'mar2': 1745, 'city_modal_county': 66, 'zcta_primary_county': 53, 'census_geocoder': 13}
  - MD: 5,211 orgs, 4,750 with a street address, 4,462 point-geocoded (85.6% of all, 93.9% of street addresses); {'census_geocoder': 4462, 'zcta_primary_county': 559, 'city_modal_county': 177, 'unresolved': 13}
  - VA: 5,514 orgs, 4,697 with a street address, 4,416 point-geocoded (80.1% of all, 94.0% of street addresses); {'census_geocoder': 4416, 'zcta_primary_county': 738, 'city_modal_county': 343, 'unresolved': 17}
  - other: 13 orgs, 12 with a street address, 11 point-geocoded (84.6% of all, 91.7% of street addresses); {'census_geocoder': 11, 'zcta_primary_county': 1, 'unresolved': 1}
- match_quality (in scope): {'exact': 10129, 'zip_only': 1351, 'city_only': 586, 'non_exact': 480, 'non_exact_retry': 38, 'none': 31}
- Census-geocoded county vs org_base ZIP county: 8,492/8,902 agree (95.4%)
- MAR 2 QC vs polygons: ward differs from 2022 ward polygon for 0, tract differs from TIGER tract polygon for 0; MAR tract replaced by polygon tract for 0
- DC orgs with a ward: 1,758 of 1,877; tract outside the 206 ACS tracts: 0
- Calvary 521307706: mar2, ward 8, tract 11001007503, MAR id 338288, lat 38.867082, lon -76.9880455
- out of scope (national universes only): 2,760 rows carried with the org_base ZIP->county ({'zcta_primary_county': 2420, 'city_modal_county': 331, 'unresolved': 9})
- wrote interim/stage_org_geo__context.csv (15,375 rows; duplicate EINs 0)
- QC: all checks passed

### 2026-10-10 13:53 — 63_build_dims
- dim_org: 15,375 rows
- dim_funder: 7,938 rows
- dim_program_area: 13 rows
- dim_period: 28 rows
- dim_geo: 243 rows

### 2026-10-10 13:53 — 37_parse_dc_budget: DC budget lines and policy events
- interim/stage_dc_budget_lines__dc.csv: 5,172 rows (Counter({'approved': 3172, 'actual': 1968, 'proposed': 32})); in-scope program/agency rows 854; duplicate keys 0
- interim/stage_fact_policy_events__dc.csv: 297 rows; by kind {'change_table_FO0-5': 8, 'change_table_HY0-5': 9, 'change_table_JA0-5': 25, 'yoy_approved_change': 161, 'bsa_subtitle': 25, 'fy2025_change_narrative': 13, 'committee_report_item': 22, 'committee_report_variance': 6, 'change_table_DB0-5': 1, 'council_adjustments_chart_fy2027': 27}; by type {'budget_proposed': 41, 'budget_enacted': 161, 'budget_revised': 66, 'policy_change': 26, 'other': 1, 'program_launch': 2}
- parsed tables: FY2024 JA0 30-PBB (2024_JA0_ja_dhs_tables_2024j.pdf): 62 lines; FY2024 FO0 30-PBB (024_FO0_fo_vsjg_tables_2024j.pdf): 21 lines; FY2024 RM0 30-PBB (2024_RM0_rm_dbh_tables_2024j.pdf): 128 lines; FY2024 DB0 30-PBB (024_DB0_db_dhcd_tables_2024j.pdf): 44 lines; FY2024 HY0 30-PBB (2024_HY0_hy_has_tables_2024j.pdf): 16 lines; FY2024 CF0 30-PBB (2024_CF0_cf_des_tables_2024j.pdf): 69 lines; FY2024 HG0 30-PBB (24_HG0_hg_dmhhs_tables_2024j.pdf): 9 lines; FY2025 JA0 30-PBB (2025_JA0_ja_dhs_tables_2025j.pdf): 61 lines; FY2025 FO0 30-PBB (25_FO0_fo_ovsjg_tables_2025j.pdf): 28 lines; FY2025 RM0 30-PBB (2025_RM0_rm_dbh_tables_2025j.pdf): 87 lines; FY2025 DB0 30-PBB (025_DB0_db_dhcd_tables_2025j.pdf): 36 lines; FY2025 HY0 30-PBB (2025_HY0_hy_hap_tables_2025j.pdf): 7 lines; FY2025 CF0 30-PBB (025_CF0_cf_does_tables_2025j.pdf): 62 lines; FY2025 HG0 30-PBB (25_HG0_hg_dmhhs_tables_2025j.pdf): 8 lines; FY2026 JA0 Table JA0-4 (026_JA0_ja_dhs_chapter_2026o.pdf): 57 lines; FY2026 FO0 Table FO0-4 (26_FO0_fo_vsjg_chapter_2026o.pdf): 26 lines; FY2026 RM0 Table RM0-4 (026_RM0_rm_dbh_chapter_2026o.pdf): 83 lines; FY2026 DB0 Table DB0-4 (26_DB0_db_dhcd_chapter_2026o.pdf): 36 lines; FY2026 HY0 Table HY0-4 (026_HY0_hy_has_chapter_2026o.pdf): 7 lines; FY2026 CF0 Table CF0-4 (26_CF0_cf_does_chapter_2026o.pdf): 61 lines; FY2026 HG0 Table HG0-4 (6_HG0_hg_dmhhs_chapter_2026o.pdf): 6 lines; FY2027 JA0 30-PBB (7_JA0_ja0_dhs_tables_2027a_0.pdf): 57 lines; FY2027 FO0 30-PBB (FO0_fo0_ovsjg_tables_2027a_0.pdf): 26 lines; FY2027 RM0 30-PBB (7_RM0_rm0_dbh_tables_2027a_0.pdf): 80 lines; FY2027 DB0 30-PBB (_DB0_db0_dhcd_tables_2027a_0.pdf): 36 lines; FY2027 HY0 30-PBB (7_HY0_hy0_hap_tables_2027a_0.pdf): 7 lines; FY2027 CF0 30-PBB (_CF0_cf0_does_tables_2027a_0.pdf): 61 lines; FY2027 HG0 30-PBB (HG0_hg0_dmhhs_tables_2027a_0.pdf): 7 lines
- change items: FY2024 JA0 Table JA0-5: 29 change lines, 7 in scope; FY2024 FO0 Table FO0-5: 14 change lines, 3 in scope; FY2024 RM0 Table RM0-5: 25 change lines, 0 in scope; FY2024 DB0 Table DB0-5: 14 change lines, 0 in scope; FY2024 HY0 Table HY0-5: 6 change lines, 6 in scope; FY2024 CF0 Table CF0-5: 16 change lines, 0 in scope; FY2024 HG0 Table HG0-5: 7 change lines, 0 in scope; FY2025 JA0 narrative change sentences (pypdfium2): 8 in scope; FY2025 FO0: chapter change text is font-garbled (amounts missing); OVSJG FY2025 changes taken from the JPS committee report; FY2025 RM0 narrative change sentences (pypdfium2): 0 in scope; FY2025 DB0 narrative change sentences (pypdfium2): 2 in scope; FY2025 HY0 narrative change sentences (pypdfium2): 3 in scope; FY2025 CF0 Table CF0-5: 20 change lines, 0 in scope; FY2025 HG0 narrative change sentences (pypdfium2): 0 in scope; FY2026 JA0 Table JA0-5: 29 change lines, 14 in scope; FY2026 FO0 Table FO0-5: 16 change lines, 4 in scope; FY2026 RM0 Table RM0-5: 27 change lines, 0 in scope; FY2026 DB0 Table DB0-5: 16 change lines, 0 in scope; FY2026 HY0 Table HY0-5: 2 change lines, 2 in scope; FY2026 CF0 Table CF0-5: 17 change lines, 0 in scope; FY2026 HG0 Table HG0-5: 4 change lines, 0 in scope; FY2027 JA0 Table JA0-5: 15 change lines, 4 in scope; FY2027 FO0 Table FO0-5: 11 change lines, 1 in scope; FY2027 RM0 Table RM0-5: 17 change lines, 0 in scope; FY2027 DB0 Table DB0-5: 15 change lines, 1 in scope; FY2027 HY0 Table HY0-5: 3 change lines, 1 in scope; FY2027 CF0 Table CF0-5: 8 change lines, 0 in scope; FY2027 HG0 Table HG0-5: 3 change lines, 0 in scope
- committee report tables: BR_FY25_Housing -> 1 in-scope proposed activity rows (markup 2024-05-09); BR_FY25_JPS -> 0 in-scope proposed activity rows (markup not printed); BR_FY26_committee_budget_report_Human-Services -> 18 in-scope proposed activity rows (markup 2025-06-24); BR_FY26_committee_budget_report_Housing -> 5 in-scope proposed activity rows (markup 2025-06-24); BR_FY26_committee_budget_report_JPS -> 2 in-scope proposed activity rows (markup not printed); BR_FY26_committee_budget_report_Health -> 0 in-scope proposed activity rows (markup 2025-06-23); BR_FY27_committee_budget_report_DRAFT-FY2027-Committee-on-Health -> 2 in-scope proposed activity rows (markup 2026-05-20); BR_FY27_committee_budget_report_FY27-Committee-on-Housing -> 4 in-scope proposed activity rows (markup not printed); BR_FY27_committee_budget_report_52226-FY2027-JPS -> 0 in-scope proposed activity rows (markup not printed)
- FY2027 Council adjustments chart: 1627 rows read, 27 in-scope events
- BSA subtitles kept: 25; curated committee-report items: 22; YoY approved-change events: 161
- tie-outs: 257 pass, 0 fail
- tie-out detail (in-scope divisions): FY2024 JA0 30-PBB p2 division 5000: sum of 23 activities vs subtotal, deltas by column [0, 0, 0, -1] ($000) -> pass | FY2024 JA0 30-PBB p3 agency total: sum of 8 division subtotals, deltas [0, -2, 0, 1] ($000) -> pass | FY2024 JA0 Table JA0-2 p2: sum of 7 fund rows vs GROSS FUNDS, deltas [-1, 0, -1, 0] ($000) -> pass | FY2024 FO0 30-PBB p1 division 4000: sum of 2 activities vs subtotal, deltas by column [0, 0, 0, -1] ($000) -> pass | FY2024 FO0 30-PBB p1 division 5000: sum of 1 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 FO0 30-PBB p1 division 6000: sum of 5 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 FO0 30-PBB p1 agency total: sum of 7 division subtotals, deltas [-2, -1, -2, 1] ($000) -> pass | FY2024 FO0 Table FO0-2 p2: sum of 5 fund rows vs GROSS FUNDS, deltas [0, 0, -1, 0] ($000) -> pass | FY2024 RM0 30-PBB p5 agency total: sum of 16 division subtotals, deltas [0, 1, 1, 0] ($000) -> pass | FY2024 RM0 Table RM0-2 p2: sum of 9 fund rows vs GROSS FUNDS, deltas [0, 1, 0, 1] ($000) -> pass | FY2024 DB0 30-PBB p2 agency total: sum of 9 division subtotals, deltas [0, 0, 0, -1] ($000) -> pass | FY2024 DB0 Table DB0-2 p2: sum of 5 fund rows vs GROSS FUNDS, deltas [1, -1, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 division 4000: sum of 1 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 division 5000: sum of 1 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 division 6000: sum of 5 activities vs subtotal, deltas by column [2, -1, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 agency total: sum of 5 division subtotals, deltas [0, 0, -1, 0] ($000) -> pass | FY2024 HY0 Table HY0-2 p1: sum of 1 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2024 CF0 30-PBB p2 division 4000: sum of 16 activities vs subtotal, deltas by column [0, 0, 0, -1] ($000) -> pass | FY2024 CF0 30-PBB p2 division 5000: sum of 3 activities vs subtotal, deltas by column [1, 0, 1, 0] ($000) -> pass | FY2024 CF0 30-PBB p2 division 6000: sum of 6 activities vs subtotal, deltas by column [1, 0, 0, 0] ($000) -> pass | FY2024 CF0 30-PBB p3 agency total: sum of 11 division subtotals, deltas [-1, 0, 0, -1] ($000) -> pass | FY2024 CF0 Table CF0-2 p2: sum of 6 fund rows vs GROSS FUNDS, deltas [1, 0, 0, 0] ($000) -> pass | FY2024 HG0 30-PBB p1 agency total: sum of 4 division subtotals, deltas [0, 0, 0, 0] ($000) -> pass | FY2024 HG0 Table HG0-2 p2: sum of 2 fund rows vs GROSS FUNDS, deltas [0, 1, 0, 0] ($000) -> pass | FY2025 JA0 30-PBB p2 division HS0030: sum of 28 activities vs subtotal, deltas by column [-2, 1, -1, 1] ($000) -> pass | FY2025 JA0 30-PBB p2 agency total: sum of 6 division subtotals, deltas [0, -1, 1, 0] ($000) -> pass | FY2025 FO0 30-PBB p1 division PS0023: sum of 2 activities vs subtotal, deltas by column [0, 0, -1, 0] ($000) -> pass | FY2025 FO0 30-PBB p2 agency total: sum of 12 division subtotals, deltas [-1, -2, 1, 0] ($000) -> pass | FY2025 RM0 30-PBB p3 agency total: sum of 13 division subtotals, deltas [1, 1, 0, 1] ($000) -> pass | FY2025 DB0 30-PBB p2 agency total: sum of 6 division subtotals, deltas [0, 1, 1, 0] ($000) -> pass | FY2025 HY0 30-PBB p1 division EC0039: sum of 5 activities vs subtotal, deltas by column [0, -1, 0, 0] ($000) -> pass | FY2025 HY0 30-PBB p1 agency total: sum of 1 division subtotals, deltas [0, 0, 0, 0] ($000) -> pass | FY2025 CF0 30-PBB p3 agency total: sum of 10 division subtotals, deltas [0, -1, 0, -1] ($000) -> pass | FY2025 CF0 Table CF0-2 p2: sum of 6 fund rows vs GROSS FUNDS, deltas [0, -1, 0, 0] ($000) -> pass | FY2025 HG0 30-PBB p1 agency total: sum of 3 division subtotals, deltas [0, 0, 0, 1] ($000) -> pass | FY2026 JA0 Table JA0-4 p5 division HS0030: sum of 28 activities vs subtotal, deltas [1, -2, 1, -1] ($000) -> pass | FY2026 JA0 Table JA0-4 p5 agency total: sum of 5 divisions, deltas [-1, -1, 0, 0] ($000) -> pass | FY2026 JA0 Table JA0-2 p2: sum of 7 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 FO0 Table FO0-4 p4 division PS0023: sum of 2 activities vs subtotal, deltas [0, 1, 0, 0] ($000) -> pass | FY2026 FO0 Table FO0-4 p4 agency total: sum of 11 divisions, deltas [-2, 0, 0, 0] ($000) -> pass | FY2026 FO0 Table FO0-2 p2: sum of 4 fund rows vs GROSS FUNDS, deltas [-1, 0, 0, 0] ($000) -> pass | FY2026 RM0 Table RM0-4 p7 agency total: sum of 13 divisions, deltas [1, 1, 2, 0] ($000) -> pass | FY2026 RM0 Table RM0-2 p2: sum of 8 fund rows vs GROSS FUNDS, deltas [1, 0, -1, 0] ($000) -> pass | FY2026 DB0 Table DB0-4 p4 agency total: sum of 6 divisions, deltas [1, -1, 0, -1] ($000) -> pass | FY2026 DB0 Table DB0-2 p2: sum of 4 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 HY0 Table HY0-4 p2 division EC0039: sum of 5 activities vs subtotal, deltas [-1, 1, 0, 0] ($000) -> pass | FY2026 HY0 Table HY0-4 p2 agency total: sum of 1 divisions, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 HY0 Table HY0-2 p1: sum of 1 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 CF0 Table CF0-4 p5 agency total: sum of 10 divisions, deltas [-1, 1, 0, 0] ($000) -> pass | FY2026 CF0 Table CF0-2 p2: sum of 5 fund rows vs GROSS FUNDS, deltas [-1, 1, 0, 1] ($000) -> pass | FY2026 HG0 Table HG0-4 p3 agency total: sum of 2 divisions, deltas [0, 1, 1, 0] ($000) -> pass | FY2026 HG0 Table HG0-2 p2: sum of 1 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2027 JA0 30-PBB p2 division HS0030: sum of 28 activities vs subtotal, deltas by column [-2, -2, -1, -3] ($000) -> pass | FY2027 JA0 30-PBB p2 agency total: sum of 5 division subtotals, deltas [-1, 1, 0, -1] ($000) -> pass | FY2027 JA0 Table JA0-2 p2: sum of 7 fund rows vs GROSS FUNDS, deltas [0, 1, 0, 0] ($000) -> pass | FY2027 FO0 30-PBB p1 division PS0023: sum of 2 activities vs subtotal, deltas by column [1, 0, 0, 0] ($000) -> pass | FY2027 FO0 30-PBB p1 agency total: sum of 11 division subtotals, deltas [-1,
- cross-book disagreements (same FY/stage/code, >$2K apart; later book preferred via x_preferred): 2022 actual JA0 AMP000 total: FY2025 book 33,466,000, FY2024 book 33,534,000 | 2022 actual JA0 AFO000 total: FY2025 book 3,079,000, FY2024 book 3,025,000 | 2022 actual JA0 HS0029 total: FY2025 book 279,438,000, FY2024 book 280,259,000 | 2022 actual JA0 HS0030 total: FY2025 book 625,848,000, FY2024 book 625,869,000 | 2025 approved JA0 H02902 total: FY2026 book 42,867,000, FY2025 book 42,943,000 | 2025 approved JA0 H02905 total: FY2026 book 91,735,000, FY2025 book 91,660,000 | 2025 approved FO0 P01903 total: FY2026 book 18,405,000, FY2025 book 18,312,000 | 2025 approved FO0 PS0019 total: FY2026 book 18,405,000, FY2025 book 18,312,000 | 2025 approved RM0 AFO003 total: FY2026 book 1,120,000, FY2025 book 1,010,000 | 2025 approved RM0 AFO005 total: FY2026 book 567,000, FY2025 book 577,000 | 2025 approved RM0 AFO000 total: FY2026 book 2,378,000, FY2025 book 2,278,000 | 2025 approved RM0 H04201 total: FY2026 book 175,000, FY2025 book 179,000 | 2025 approved RM0 H04202 total: FY2026 book 1,128,000, FY2025 book 1,151,000 | 2025 approved RM0 H04205 total: FY2026 book 381,000, FY2025 book 355,000 | 2025 approved RM0 H04504 total: FY2026 book 1,367,000, FY2025 book 100,000 | 2025 approved RM0 HS0045 total: FY2026 book 37,390,000, FY2025 book 36,123,000 | 2025 approved RM0 H04802 total: FY2026 book 27,140,000, FY2025 book 22,840,000 | 2025 approved RM0 H04805 total: FY2026 book 1,391,000, FY2025 book 5,691,000 | 2025 approved RM0 HS0053 total: FY2026 book 20,351,000, FY2025 book 21,717,000 | 2025 approved CF0 AFO003 total: FY2026 book 2,141,000, FY2025 book 2,222,000 | 2025 approved CF0 AFO000 total: FY2026 book 4,023,000, FY2025 book 4,104,000 | 2025 approved CF0 AMP026 total: FY2026 book 0, FY2025 book -3,000 | 2025 approved CF0 AMP000 total: FY2026 book 24,947,000, FY2025 book 24,944,000 | 2025 approved CF0 O00111 total: FY2026 book 556,000, FY2025 book 559,000 | 2025 approved CF0 GO0047 total: FY2026 book 6,545,000, FY2025 book 6,548,000 | 2025 approved CF0 O05201 total: FY2026 book 15,504,000, FY2025 book 15,422,000 | 2025 approved CF0 GO0052 total: FY2026 book 75,929,000, FY2025 book 75,847,000
- FY2024 old-code -> FY2025 code crosswalk (FY2024 approved): FO0 P02301: FY2024 book 171,000 vs FY2025 book restated 171,000 (delta +0) | FO0 P02303: FY2024 book 45,515,000 vs FY2025 book restated 45,515,000 (delta +0) | FO0 P04502: FY2024 book 3,720,000 vs FY2025 book restated 3,720,000 (delta +0) | HY0 R03903: FY2024 book 4,400,000 vs FY2025 book restated 4,400,000 (delta +0) | HY0 R03904: FY2024 book 0 vs FY2025 book restated 0 (delta +0) | HY0 R03905: FY2024 book 128,094,000 vs FY2025 book restated 128,094,000 (delta +0) | HY0 R03906: FY2024 book 10,581,000 vs FY2025 book restated 10,581,000 (delta +0) | HY0 R03907: FY2024 book 43,296,000 vs FY2025 book restated 43,296,000 (delta +0) | JA0 H03002: FY2024 book 79,033,000 vs FY2025 book restated 93,339,000 (delta +14,306,000) | JA0 H03003: FY2024 book 59,994,000 vs FY2025 book restated 59,994,000 (delta +0) | JA0 H03004: FY2024 book 31,818,000 vs FY2025 book restated 12,421,000 (delta -19,397,000) | JA0 H03007: FY2024 book 2,940,000 vs FY2025 book restated 2,940,000 (delta +0) | JA0 H03008: FY2024 book 42,536,000 vs FY2025 book restated 42,536,000 (delta +0) | JA0 H03009: FY2024 book 2,799,000 vs FY2025 book restated 4,259,000 (delta +1,460,000) | JA0 H03010: FY2024 book 51,764,000 vs FY2025 book restated 60,770,000 (delta +9,006,000) | JA0 H03011: FY2024 book 4,935,000 vs FY2025 book restated 4,935,000 (delta +0) | JA0 H03012: FY2024 book 86,929,000 vs FY2025 book restated 83,014,000 (delta -3,915,000) | JA0 H03013: FY2024 book 4,222,000 vs FY2025 book restated 4,222,000 (delta +0) | JA0 H03014-H03016: FY2024 book 11,541,000 vs FY2025 book restated 11,542,000 (delta +1,000) | JA0 H03017: FY2024 book 73,209,000 vs FY2025 book restated 73,209,000 (delta +0) | JA0 H03018: FY2024 book 10,875,000 vs FY2025 book restated 10,875,000 (delta +0) | JA0 H03019: FY2024 book 1,150,000 vs FY2025 book restated 1,150,000 (delta +0) | JA0 H03022: FY2024 book 1,980,000 vs FY2025 book restated 1,980,000 (delta +0) | JA0 H03023: FY2024 book 12,032,000 vs FY2025 book restated 12,032,000 (delta +0) | RM0 H04308: FY2024 book 29,637,000 vs FY2025 book restated 29,637,000 (delta +0) | RM0 H04504: FY2024 book 1,467,000 vs FY2025 book restated 1,467,000 (delta +0)
- event dates: budget_enacted/budget_revised = Local Budget Act 2nd reading {2024: '2023-05-30', 2025: '2024-06-12', 2026: '2025-07-28', 2027: '2026-06-23'}; budget_proposed = BSA introduced on behalf of the Mayor {2025: '2024-04-03', 2026: '2025-06-02', 2027: '2026-04-14'} (FY2024 proposal date not in downloaded docs -> blank); BSA policy rows = law/act effective date {2024: '2023-09-06', 2025: '2024-09-18', 2026: '2025-12-06', 2027: '2026-08-13'}; committee items = markup date when printed, else Local Budget Act date
- mapping: Table XX0-5 lines before 'Mayor's Proposed Budget' -> budget_proposed; lines between it and 'District's Approved Budget' -> budget_revised (Council changes); FY2027 Council-level changes taken from the activity-level Council chart instead of JA0-5 to avoid double counting
- coverage (stage[+funds] by FY x agency JA0/FO0/RM0/DB0/HY0/CF0/HG0):
| FY2021 | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds |
| FY2022 | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds |
| FY2023 | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds |
| FY2024 | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds |
| FY2025 | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds,prop | actu+funds,appr+funds | actu+funds,appr+funds |
| FY2026 | appr+funds,prop | appr+funds,prop | appr+funds | appr+funds | appr+funds,prop | appr+funds | appr+funds |
| FY2027 | appr+funds | appr+funds | appr+funds,prop | appr+funds | appr+funds,prop | appr+funds | appr+funds |
- warnings (0):

### 2026-10-10 13:55 — 30_fetch_xml: progress
- pass 1: 20,000/31,469 done in 24.7 min (13.5/s); 1,558 MB on disk for done files; ok 20,000, not_found 0, error 0

### 2026-10-10 13:56 — 37_parse_dc_budget: DC budget lines and policy events
- interim/stage_dc_budget_lines__dc.csv: 5,172 rows (Counter({'approved': 3172, 'actual': 1968, 'proposed': 32})); in-scope program/agency rows 854; duplicate keys 0
- interim/stage_fact_policy_events__dc.csv: 297 rows; by kind {'change_table_FO0-5': 8, 'change_table_HY0-5': 9, 'change_table_JA0-5': 25, 'yoy_approved_change': 161, 'bsa_subtitle': 25, 'fy2025_change_narrative': 13, 'committee_report_item': 22, 'committee_report_variance': 6, 'change_table_DB0-5': 1, 'council_adjustments_chart_fy2027': 27}; by type {'budget_proposed': 41, 'budget_enacted': 161, 'budget_revised': 66, 'policy_change': 26, 'other': 1, 'program_launch': 2}
- parsed tables: FY2024 JA0 30-PBB (2024_JA0_ja_dhs_tables_2024j.pdf): 62 lines; FY2024 FO0 30-PBB (024_FO0_fo_vsjg_tables_2024j.pdf): 21 lines; FY2024 RM0 30-PBB (2024_RM0_rm_dbh_tables_2024j.pdf): 128 lines; FY2024 DB0 30-PBB (024_DB0_db_dhcd_tables_2024j.pdf): 44 lines; FY2024 HY0 30-PBB (2024_HY0_hy_has_tables_2024j.pdf): 16 lines; FY2024 CF0 30-PBB (2024_CF0_cf_des_tables_2024j.pdf): 69 lines; FY2024 HG0 30-PBB (24_HG0_hg_dmhhs_tables_2024j.pdf): 9 lines; FY2025 JA0 30-PBB (2025_JA0_ja_dhs_tables_2025j.pdf): 61 lines; FY2025 FO0 30-PBB (25_FO0_fo_ovsjg_tables_2025j.pdf): 28 lines; FY2025 RM0 30-PBB (2025_RM0_rm_dbh_tables_2025j.pdf): 87 lines; FY2025 DB0 30-PBB (025_DB0_db_dhcd_tables_2025j.pdf): 36 lines; FY2025 HY0 30-PBB (2025_HY0_hy_hap_tables_2025j.pdf): 7 lines; FY2025 CF0 30-PBB (025_CF0_cf_does_tables_2025j.pdf): 62 lines; FY2025 HG0 30-PBB (25_HG0_hg_dmhhs_tables_2025j.pdf): 8 lines; FY2026 JA0 Table JA0-4 (026_JA0_ja_dhs_chapter_2026o.pdf): 57 lines; FY2026 FO0 Table FO0-4 (26_FO0_fo_vsjg_chapter_2026o.pdf): 26 lines; FY2026 RM0 Table RM0-4 (026_RM0_rm_dbh_chapter_2026o.pdf): 83 lines; FY2026 DB0 Table DB0-4 (26_DB0_db_dhcd_chapter_2026o.pdf): 36 lines; FY2026 HY0 Table HY0-4 (026_HY0_hy_has_chapter_2026o.pdf): 7 lines; FY2026 CF0 Table CF0-4 (26_CF0_cf_does_chapter_2026o.pdf): 61 lines; FY2026 HG0 Table HG0-4 (6_HG0_hg_dmhhs_chapter_2026o.pdf): 6 lines; FY2027 JA0 30-PBB (7_JA0_ja0_dhs_tables_2027a_0.pdf): 57 lines; FY2027 FO0 30-PBB (FO0_fo0_ovsjg_tables_2027a_0.pdf): 26 lines; FY2027 RM0 30-PBB (7_RM0_rm0_dbh_tables_2027a_0.pdf): 80 lines; FY2027 DB0 30-PBB (_DB0_db0_dhcd_tables_2027a_0.pdf): 36 lines; FY2027 HY0 30-PBB (7_HY0_hy0_hap_tables_2027a_0.pdf): 7 lines; FY2027 CF0 30-PBB (_CF0_cf0_does_tables_2027a_0.pdf): 61 lines; FY2027 HG0 30-PBB (HG0_hg0_dmhhs_tables_2027a_0.pdf): 7 lines
- change items: FY2024 JA0 Table JA0-5: 29 change lines, 7 in scope; FY2024 FO0 Table FO0-5: 14 change lines, 3 in scope; FY2024 RM0 Table RM0-5: 25 change lines, 0 in scope; FY2024 DB0 Table DB0-5: 14 change lines, 0 in scope; FY2024 HY0 Table HY0-5: 6 change lines, 6 in scope; FY2024 CF0 Table CF0-5: 16 change lines, 0 in scope; FY2024 HG0 Table HG0-5: 7 change lines, 0 in scope; FY2025 JA0 narrative change sentences (pypdfium2): 8 in scope; FY2025 FO0: chapter change text is font-garbled (amounts missing); OVSJG FY2025 changes taken from the JPS committee report; FY2025 RM0 narrative change sentences (pypdfium2): 0 in scope; FY2025 DB0 narrative change sentences (pypdfium2): 2 in scope; FY2025 HY0 narrative change sentences (pypdfium2): 3 in scope; FY2025 CF0 Table CF0-5: 20 change lines, 0 in scope; FY2025 HG0 narrative change sentences (pypdfium2): 0 in scope; FY2026 JA0 Table JA0-5: 29 change lines, 14 in scope; FY2026 FO0 Table FO0-5: 16 change lines, 4 in scope; FY2026 RM0 Table RM0-5: 27 change lines, 0 in scope; FY2026 DB0 Table DB0-5: 16 change lines, 0 in scope; FY2026 HY0 Table HY0-5: 2 change lines, 2 in scope; FY2026 CF0 Table CF0-5: 17 change lines, 0 in scope; FY2026 HG0 Table HG0-5: 4 change lines, 0 in scope; FY2027 JA0 Table JA0-5: 15 change lines, 4 in scope; FY2027 FO0 Table FO0-5: 11 change lines, 1 in scope; FY2027 RM0 Table RM0-5: 17 change lines, 0 in scope; FY2027 DB0 Table DB0-5: 15 change lines, 1 in scope; FY2027 HY0 Table HY0-5: 3 change lines, 1 in scope; FY2027 CF0 Table CF0-5: 8 change lines, 0 in scope; FY2027 HG0 Table HG0-5: 3 change lines, 0 in scope
- committee report tables: BR_FY25_Housing -> 1 in-scope proposed activity rows (markup 2024-05-09); BR_FY25_JPS -> 0 in-scope proposed activity rows (markup not printed); BR_FY26_committee_budget_report_Human-Services -> 18 in-scope proposed activity rows (markup 2025-06-24); BR_FY26_committee_budget_report_Housing -> 5 in-scope proposed activity rows (markup 2025-06-24); BR_FY26_committee_budget_report_JPS -> 2 in-scope proposed activity rows (markup not printed); BR_FY26_committee_budget_report_Health -> 0 in-scope proposed activity rows (markup 2025-06-23); BR_FY27_committee_budget_report_DRAFT-FY2027-Committee-on-Health -> 2 in-scope proposed activity rows (markup 2026-05-20); BR_FY27_committee_budget_report_FY27-Committee-on-Housing -> 4 in-scope proposed activity rows (markup not printed); BR_FY27_committee_budget_report_52226-FY2027-JPS -> 0 in-scope proposed activity rows (markup not printed)
- FY2027 Council adjustments chart: 1627 rows read, 27 in-scope events
- BSA subtitles kept: 25; curated committee-report items: 22; YoY approved-change events: 161
- tie-outs: 257 pass, 0 fail
- tie-out detail (in-scope divisions): FY2024 JA0 30-PBB p2 division 5000: sum of 23 activities vs subtotal, deltas by column [0, 0, 0, -1] ($000) -> pass | FY2024 JA0 30-PBB p3 agency total: sum of 8 division subtotals, deltas [0, -2, 0, 1] ($000) -> pass | FY2024 JA0 Table JA0-2 p2: sum of 7 fund rows vs GROSS FUNDS, deltas [-1, 0, -1, 0] ($000) -> pass | FY2024 FO0 30-PBB p1 division 4000: sum of 2 activities vs subtotal, deltas by column [0, 0, 0, -1] ($000) -> pass | FY2024 FO0 30-PBB p1 division 5000: sum of 1 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 FO0 30-PBB p1 division 6000: sum of 5 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 FO0 30-PBB p1 agency total: sum of 7 division subtotals, deltas [-2, -1, -2, 1] ($000) -> pass | FY2024 FO0 Table FO0-2 p2: sum of 5 fund rows vs GROSS FUNDS, deltas [0, 0, -1, 0] ($000) -> pass | FY2024 RM0 30-PBB p5 agency total: sum of 16 division subtotals, deltas [0, 1, 1, 0] ($000) -> pass | FY2024 RM0 Table RM0-2 p2: sum of 9 fund rows vs GROSS FUNDS, deltas [0, 1, 0, 1] ($000) -> pass | FY2024 DB0 30-PBB p2 agency total: sum of 9 division subtotals, deltas [0, 0, 0, -1] ($000) -> pass | FY2024 DB0 Table DB0-2 p2: sum of 5 fund rows vs GROSS FUNDS, deltas [1, -1, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 division 4000: sum of 1 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 division 5000: sum of 1 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 division 6000: sum of 5 activities vs subtotal, deltas by column [2, -1, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 agency total: sum of 5 division subtotals, deltas [0, 0, -1, 0] ($000) -> pass | FY2024 HY0 Table HY0-2 p1: sum of 1 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2024 CF0 30-PBB p2 division 4000: sum of 16 activities vs subtotal, deltas by column [0, 0, 0, -1] ($000) -> pass | FY2024 CF0 30-PBB p2 division 5000: sum of 3 activities vs subtotal, deltas by column [1, 0, 1, 0] ($000) -> pass | FY2024 CF0 30-PBB p2 division 6000: sum of 6 activities vs subtotal, deltas by column [1, 0, 0, 0] ($000) -> pass | FY2024 CF0 30-PBB p3 agency total: sum of 11 division subtotals, deltas [-1, 0, 0, -1] ($000) -> pass | FY2024 CF0 Table CF0-2 p2: sum of 6 fund rows vs GROSS FUNDS, deltas [1, 0, 0, 0] ($000) -> pass | FY2024 HG0 30-PBB p1 agency total: sum of 4 division subtotals, deltas [0, 0, 0, 0] ($000) -> pass | FY2024 HG0 Table HG0-2 p2: sum of 2 fund rows vs GROSS FUNDS, deltas [0, 1, 0, 0] ($000) -> pass | FY2025 JA0 30-PBB p2 division HS0030: sum of 28 activities vs subtotal, deltas by column [-2, 1, -1, 1] ($000) -> pass | FY2025 JA0 30-PBB p2 agency total: sum of 6 division subtotals, deltas [0, -1, 1, 0] ($000) -> pass | FY2025 FO0 30-PBB p1 division PS0023: sum of 2 activities vs subtotal, deltas by column [0, 0, -1, 0] ($000) -> pass | FY2025 FO0 30-PBB p2 agency total: sum of 12 division subtotals, deltas [-1, -2, 1, 0] ($000) -> pass | FY2025 RM0 30-PBB p3 agency total: sum of 13 division subtotals, deltas [1, 1, 0, 1] ($000) -> pass | FY2025 DB0 30-PBB p2 agency total: sum of 6 division subtotals, deltas [0, 1, 1, 0] ($000) -> pass | FY2025 HY0 30-PBB p1 division EC0039: sum of 5 activities vs subtotal, deltas by column [0, -1, 0, 0] ($000) -> pass | FY2025 HY0 30-PBB p1 agency total: sum of 1 division subtotals, deltas [0, 0, 0, 0] ($000) -> pass | FY2025 CF0 30-PBB p3 agency total: sum of 10 division subtotals, deltas [0, -1, 0, -1] ($000) -> pass | FY2025 CF0 Table CF0-2 p2: sum of 6 fund rows vs GROSS FUNDS, deltas [0, -1, 0, 0] ($000) -> pass | FY2025 HG0 30-PBB p1 agency total: sum of 3 division subtotals, deltas [0, 0, 0, 1] ($000) -> pass | FY2026 JA0 Table JA0-4 p5 division HS0030: sum of 28 activities vs subtotal, deltas [1, -2, 1, -1] ($000) -> pass | FY2026 JA0 Table JA0-4 p5 agency total: sum of 5 divisions, deltas [-1, -1, 0, 0] ($000) -> pass | FY2026 JA0 Table JA0-2 p2: sum of 7 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 FO0 Table FO0-4 p4 division PS0023: sum of 2 activities vs subtotal, deltas [0, 1, 0, 0] ($000) -> pass | FY2026 FO0 Table FO0-4 p4 agency total: sum of 11 divisions, deltas [-2, 0, 0, 0] ($000) -> pass | FY2026 FO0 Table FO0-2 p2: sum of 4 fund rows vs GROSS FUNDS, deltas [-1, 0, 0, 0] ($000) -> pass | FY2026 RM0 Table RM0-4 p7 agency total: sum of 13 divisions, deltas [1, 1, 2, 0] ($000) -> pass | FY2026 RM0 Table RM0-2 p2: sum of 8 fund rows vs GROSS FUNDS, deltas [1, 0, -1, 0] ($000) -> pass | FY2026 DB0 Table DB0-4 p4 agency total: sum of 6 divisions, deltas [1, -1, 0, -1] ($000) -> pass | FY2026 DB0 Table DB0-2 p2: sum of 4 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 HY0 Table HY0-4 p2 division EC0039: sum of 5 activities vs subtotal, deltas [-1, 1, 0, 0] ($000) -> pass | FY2026 HY0 Table HY0-4 p2 agency total: sum of 1 divisions, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 HY0 Table HY0-2 p1: sum of 1 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 CF0 Table CF0-4 p5 agency total: sum of 10 divisions, deltas [-1, 1, 0, 0] ($000) -> pass | FY2026 CF0 Table CF0-2 p2: sum of 5 fund rows vs GROSS FUNDS, deltas [-1, 1, 0, 1] ($000) -> pass | FY2026 HG0 Table HG0-4 p3 agency total: sum of 2 divisions, deltas [0, 1, 1, 0] ($000) -> pass | FY2026 HG0 Table HG0-2 p2: sum of 1 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2027 JA0 30-PBB p2 division HS0030: sum of 28 activities vs subtotal, deltas by column [-2, -2, -1, -3] ($000) -> pass | FY2027 JA0 30-PBB p2 agency total: sum of 5 division subtotals, deltas [-1, 1, 0, -1] ($000) -> pass | FY2027 JA0 Table JA0-2 p2: sum of 7 fund rows vs GROSS FUNDS, deltas [0, 1, 0, 0] ($000) -> pass | FY2027 FO0 30-PBB p1 division PS0023: sum of 2 activities vs subtotal, deltas by column [1, 0, 0, 0] ($000) -> pass | FY2027 FO0 30-PBB p1 agency total: sum of 11 division subtotals, deltas [-1,
- cross-book disagreements (same FY/stage/code, >$2K apart; later book preferred via x_preferred): 2022 actual JA0 AMP000 total: FY2025 book 33,466,000, FY2024 book 33,534,000 | 2022 actual JA0 AFO000 total: FY2025 book 3,079,000, FY2024 book 3,025,000 | 2022 actual JA0 HS0029 total: FY2025 book 279,438,000, FY2024 book 280,259,000 | 2022 actual JA0 HS0030 total: FY2025 book 625,848,000, FY2024 book 625,869,000 | 2025 approved JA0 H02902 total: FY2026 book 42,867,000, FY2025 book 42,943,000 | 2025 approved JA0 H02905 total: FY2026 book 91,735,000, FY2025 book 91,660,000 | 2025 approved FO0 P01903 total: FY2026 book 18,405,000, FY2025 book 18,312,000 | 2025 approved FO0 PS0019 total: FY2026 book 18,405,000, FY2025 book 18,312,000 | 2025 approved RM0 AFO003 total: FY2026 book 1,120,000, FY2025 book 1,010,000 | 2025 approved RM0 AFO005 total: FY2026 book 567,000, FY2025 book 577,000 | 2025 approved RM0 AFO000 total: FY2026 book 2,378,000, FY2025 book 2,278,000 | 2025 approved RM0 H04201 total: FY2026 book 175,000, FY2025 book 179,000 | 2025 approved RM0 H04202 total: FY2026 book 1,128,000, FY2025 book 1,151,000 | 2025 approved RM0 H04205 total: FY2026 book 381,000, FY2025 book 355,000 | 2025 approved RM0 H04504 total: FY2026 book 1,367,000, FY2025 book 100,000 | 2025 approved RM0 HS0045 total: FY2026 book 37,390,000, FY2025 book 36,123,000 | 2025 approved RM0 H04802 total: FY2026 book 27,140,000, FY2025 book 22,840,000 | 2025 approved RM0 H04805 total: FY2026 book 1,391,000, FY2025 book 5,691,000 | 2025 approved RM0 HS0053 total: FY2026 book 20,351,000, FY2025 book 21,717,000 | 2025 approved CF0 AFO003 total: FY2026 book 2,141,000, FY2025 book 2,222,000 | 2025 approved CF0 AFO000 total: FY2026 book 4,023,000, FY2025 book 4,104,000 | 2025 approved CF0 AMP026 total: FY2026 book 0, FY2025 book -3,000 | 2025 approved CF0 AMP000 total: FY2026 book 24,947,000, FY2025 book 24,944,000 | 2025 approved CF0 O00111 total: FY2026 book 556,000, FY2025 book 559,000 | 2025 approved CF0 GO0047 total: FY2026 book 6,545,000, FY2025 book 6,548,000 | 2025 approved CF0 O05201 total: FY2026 book 15,504,000, FY2025 book 15,422,000 | 2025 approved CF0 GO0052 total: FY2026 book 75,929,000, FY2025 book 75,847,000
- FY2024 old-code -> FY2025 code crosswalk (FY2024 approved): FO0 P02301: FY2024 book 171,000 vs FY2025 book restated 171,000 (delta +0) | FO0 P02303: FY2024 book 45,515,000 vs FY2025 book restated 45,515,000 (delta +0) | FO0 P04502: FY2024 book 3,720,000 vs FY2025 book restated 3,720,000 (delta +0) | HY0 R03903: FY2024 book 4,400,000 vs FY2025 book restated 4,400,000 (delta +0) | HY0 R03904: FY2024 book 0 vs FY2025 book restated 0 (delta +0) | HY0 R03905: FY2024 book 128,094,000 vs FY2025 book restated 128,094,000 (delta +0) | HY0 R03906: FY2024 book 10,581,000 vs FY2025 book restated 10,581,000 (delta +0) | HY0 R03907: FY2024 book 43,296,000 vs FY2025 book restated 43,296,000 (delta +0) | JA0 H03002: FY2024 book 79,033,000 vs FY2025 book restated 93,339,000 (delta +14,306,000) | JA0 H03003: FY2024 book 59,994,000 vs FY2025 book restated 59,994,000 (delta +0) | JA0 H03004: FY2024 book 31,818,000 vs FY2025 book restated 12,421,000 (delta -19,397,000) | JA0 H03007: FY2024 book 2,940,000 vs FY2025 book restated 2,940,000 (delta +0) | JA0 H03008: FY2024 book 42,536,000 vs FY2025 book restated 42,536,000 (delta +0) | JA0 H03009: FY2024 book 2,799,000 vs FY2025 book restated 4,259,000 (delta +1,460,000) | JA0 H03010: FY2024 book 51,764,000 vs FY2025 book restated 60,770,000 (delta +9,006,000) | JA0 H03011: FY2024 book 4,935,000 vs FY2025 book restated 4,935,000 (delta +0) | JA0 H03012: FY2024 book 86,929,000 vs FY2025 book restated 83,014,000 (delta -3,915,000) | JA0 H03013: FY2024 book 4,222,000 vs FY2025 book restated 4,222,000 (delta +0) | JA0 H03014-H03016: FY2024 book 11,541,000 vs FY2025 book restated 11,542,000 (delta +1,000) | JA0 H03017: FY2024 book 73,209,000 vs FY2025 book restated 73,209,000 (delta +0) | JA0 H03018: FY2024 book 10,875,000 vs FY2025 book restated 10,875,000 (delta +0) | JA0 H03019: FY2024 book 1,150,000 vs FY2025 book restated 1,150,000 (delta +0) | JA0 H03022: FY2024 book 1,980,000 vs FY2025 book restated 1,980,000 (delta +0) | JA0 H03023: FY2024 book 12,032,000 vs FY2025 book restated 12,032,000 (delta +0) | RM0 H04308: FY2024 book 29,637,000 vs FY2025 book restated 29,637,000 (delta +0) | RM0 H04504: FY2024 book 1,467,000 vs FY2025 book restated 1,467,000 (delta +0)
- event dates: budget_enacted/budget_revised = Local Budget Act 2nd reading {2024: '2023-05-30', 2025: '2024-06-12', 2026: '2025-07-28', 2027: '2026-06-23'}; budget_proposed = BSA introduced on behalf of the Mayor {2025: '2024-04-03', 2026: '2025-06-02', 2027: '2026-04-14'} (FY2024 proposal date not in downloaded docs -> blank); BSA policy rows = law/act effective date {2024: '2023-09-06', 2025: '2024-09-18', 2026: '2025-12-06', 2027: '2026-08-13'}; committee items = markup date when printed, else Local Budget Act date
- mapping: Table XX0-5 lines before 'Mayor's Proposed Budget' -> budget_proposed; lines between it and 'District's Approved Budget' -> budget_revised (Council changes); FY2027 Council-level changes taken from the activity-level Council chart instead of JA0-5 to avoid double counting
- coverage (stage[+funds] by FY x agency JA0/FO0/RM0/DB0/HY0/CF0/HG0):
| FY2021 | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds |
| FY2022 | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds |
| FY2023 | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds |
| FY2024 | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds |
| FY2025 | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds,prop | actu+funds,appr+funds | actu+funds,appr+funds |
| FY2026 | appr+funds,prop | appr+funds,prop | appr+funds | appr+funds | appr+funds,prop | appr+funds | appr+funds |
| FY2027 | appr+funds | appr+funds | appr+funds,prop | appr+funds | appr+funds,prop | appr+funds | appr+funds |
- warnings (0):

### 2026-10-10 13:56 — 44_web_peers_funders
- search hits 757; pages listed 70, with content 66
- by group (listed, fetched): peer 35/35, funder 26/26, inkind 9/9
- failed/empty: nuvaya_fin_reports (http:http_403; chars 0 -> tavily no_content); christhouse_ar_2025_pdf (ok); miriams_ar_fy25 (http:ok; chars 21 -> tavily no_content); hormd_ar_2024 (http:http_404; chars 0 -> tavily no_content); ik_hef_home (http:ok; chars 18 -> tavily no_content)
- this run: Tavily search 0, extract 2, HTTP GET 11, cache hits 156; cumulative (manifest): search 104/300, extract 9/200, HTTP 115

### 2026-10-10 13:57 — 37_parse_dc_budget: DC budget lines and policy events
- interim/stage_dc_budget_lines__dc.csv: 5,172 rows (Counter({'approved': 3172, 'actual': 1968, 'proposed': 32})); in-scope program/agency rows 854; duplicate keys 0
- interim/stage_fact_policy_events__dc.csv: 297 rows; by kind {'change_table_FO0-5': 8, 'change_table_HY0-5': 9, 'change_table_JA0-5': 25, 'yoy_approved_change': 161, 'bsa_subtitle': 25, 'fy2025_change_narrative': 13, 'committee_report_item': 22, 'committee_report_variance': 6, 'change_table_DB0-5': 1, 'council_adjustments_chart_fy2027': 27}; by type {'budget_proposed': 41, 'budget_enacted': 161, 'budget_revised': 66, 'policy_change': 26, 'other': 1, 'program_launch': 2}
- parsed tables: FY2024 JA0 30-PBB (2024_JA0_ja_dhs_tables_2024j.pdf): 62 lines; FY2024 FO0 30-PBB (024_FO0_fo_vsjg_tables_2024j.pdf): 21 lines; FY2024 RM0 30-PBB (2024_RM0_rm_dbh_tables_2024j.pdf): 128 lines; FY2024 DB0 30-PBB (024_DB0_db_dhcd_tables_2024j.pdf): 44 lines; FY2024 HY0 30-PBB (2024_HY0_hy_has_tables_2024j.pdf): 16 lines; FY2024 CF0 30-PBB (2024_CF0_cf_des_tables_2024j.pdf): 69 lines; FY2024 HG0 30-PBB (24_HG0_hg_dmhhs_tables_2024j.pdf): 9 lines; FY2025 JA0 30-PBB (2025_JA0_ja_dhs_tables_2025j.pdf): 61 lines; FY2025 FO0 30-PBB (25_FO0_fo_ovsjg_tables_2025j.pdf): 28 lines; FY2025 RM0 30-PBB (2025_RM0_rm_dbh_tables_2025j.pdf): 87 lines; FY2025 DB0 30-PBB (025_DB0_db_dhcd_tables_2025j.pdf): 36 lines; FY2025 HY0 30-PBB (2025_HY0_hy_hap_tables_2025j.pdf): 7 lines; FY2025 CF0 30-PBB (025_CF0_cf_does_tables_2025j.pdf): 62 lines; FY2025 HG0 30-PBB (25_HG0_hg_dmhhs_tables_2025j.pdf): 8 lines; FY2026 JA0 Table JA0-4 (026_JA0_ja_dhs_chapter_2026o.pdf): 57 lines; FY2026 FO0 Table FO0-4 (26_FO0_fo_vsjg_chapter_2026o.pdf): 26 lines; FY2026 RM0 Table RM0-4 (026_RM0_rm_dbh_chapter_2026o.pdf): 83 lines; FY2026 DB0 Table DB0-4 (26_DB0_db_dhcd_chapter_2026o.pdf): 36 lines; FY2026 HY0 Table HY0-4 (026_HY0_hy_has_chapter_2026o.pdf): 7 lines; FY2026 CF0 Table CF0-4 (26_CF0_cf_does_chapter_2026o.pdf): 61 lines; FY2026 HG0 Table HG0-4 (6_HG0_hg_dmhhs_chapter_2026o.pdf): 6 lines; FY2027 JA0 30-PBB (7_JA0_ja0_dhs_tables_2027a_0.pdf): 57 lines; FY2027 FO0 30-PBB (FO0_fo0_ovsjg_tables_2027a_0.pdf): 26 lines; FY2027 RM0 30-PBB (7_RM0_rm0_dbh_tables_2027a_0.pdf): 80 lines; FY2027 DB0 30-PBB (_DB0_db0_dhcd_tables_2027a_0.pdf): 36 lines; FY2027 HY0 30-PBB (7_HY0_hy0_hap_tables_2027a_0.pdf): 7 lines; FY2027 CF0 30-PBB (_CF0_cf0_does_tables_2027a_0.pdf): 61 lines; FY2027 HG0 30-PBB (HG0_hg0_dmhhs_tables_2027a_0.pdf): 7 lines
- change items: FY2024 JA0 Table JA0-5: 29 change lines, 7 in scope; FY2024 FO0 Table FO0-5: 14 change lines, 3 in scope; FY2024 RM0 Table RM0-5: 25 change lines, 0 in scope; FY2024 DB0 Table DB0-5: 14 change lines, 0 in scope; FY2024 HY0 Table HY0-5: 6 change lines, 6 in scope; FY2024 CF0 Table CF0-5: 16 change lines, 0 in scope; FY2024 HG0 Table HG0-5: 7 change lines, 0 in scope; FY2025 JA0 narrative change sentences (pypdfium2): 8 in scope; FY2025 FO0: chapter change text is font-garbled (amounts missing); OVSJG FY2025 changes taken from the JPS committee report; FY2025 RM0 narrative change sentences (pypdfium2): 0 in scope; FY2025 DB0 narrative change sentences (pypdfium2): 2 in scope; FY2025 HY0 narrative change sentences (pypdfium2): 3 in scope; FY2025 CF0 Table CF0-5: 20 change lines, 0 in scope; FY2025 HG0 narrative change sentences (pypdfium2): 0 in scope; FY2026 JA0 Table JA0-5: 29 change lines, 14 in scope; FY2026 FO0 Table FO0-5: 16 change lines, 4 in scope; FY2026 RM0 Table RM0-5: 27 change lines, 0 in scope; FY2026 DB0 Table DB0-5: 16 change lines, 0 in scope; FY2026 HY0 Table HY0-5: 2 change lines, 2 in scope; FY2026 CF0 Table CF0-5: 17 change lines, 0 in scope; FY2026 HG0 Table HG0-5: 4 change lines, 0 in scope; FY2027 JA0 Table JA0-5: 15 change lines, 4 in scope; FY2027 FO0 Table FO0-5: 11 change lines, 1 in scope; FY2027 RM0 Table RM0-5: 17 change lines, 0 in scope; FY2027 DB0 Table DB0-5: 15 change lines, 1 in scope; FY2027 HY0 Table HY0-5: 3 change lines, 1 in scope; FY2027 CF0 Table CF0-5: 8 change lines, 0 in scope; FY2027 HG0 Table HG0-5: 3 change lines, 0 in scope
- committee report tables: BR_FY25_Housing -> 1 in-scope proposed activity rows (markup 2024-05-09); BR_FY25_JPS -> 0 in-scope proposed activity rows (markup not printed); BR_FY26_committee_budget_report_Human-Services -> 18 in-scope proposed activity rows (markup 2025-06-24); BR_FY26_committee_budget_report_Housing -> 5 in-scope proposed activity rows (markup 2025-06-24); BR_FY26_committee_budget_report_JPS -> 2 in-scope proposed activity rows (markup not printed); BR_FY26_committee_budget_report_Health -> 0 in-scope proposed activity rows (markup 2025-06-23); BR_FY27_committee_budget_report_DRAFT-FY2027-Committee-on-Health -> 2 in-scope proposed activity rows (markup 2026-05-20); BR_FY27_committee_budget_report_FY27-Committee-on-Housing -> 4 in-scope proposed activity rows (markup not printed); BR_FY27_committee_budget_report_52226-FY2027-JPS -> 0 in-scope proposed activity rows (markup not printed)
- FY2027 Council adjustments chart: 1627 rows read, 27 in-scope events
- BSA subtitles kept: 25; curated committee-report items: 22; YoY approved-change events: 161
- tie-outs: 257 pass, 0 fail
- tie-out detail (in-scope divisions): FY2024 JA0 30-PBB p2 division 5000: sum of 23 activities vs subtotal, deltas by column [0, 0, 0, -1] ($000) -> pass | FY2024 JA0 30-PBB p3 agency total: sum of 8 division subtotals, deltas [0, -2, 0, 1] ($000) -> pass | FY2024 JA0 Table JA0-2 p2: sum of 7 fund rows vs GROSS FUNDS, deltas [-1, 0, -1, 0] ($000) -> pass | FY2024 FO0 30-PBB p1 division 4000: sum of 2 activities vs subtotal, deltas by column [0, 0, 0, -1] ($000) -> pass | FY2024 FO0 30-PBB p1 division 5000: sum of 1 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 FO0 30-PBB p1 division 6000: sum of 5 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 FO0 30-PBB p1 agency total: sum of 7 division subtotals, deltas [-2, -1, -2, 1] ($000) -> pass | FY2024 FO0 Table FO0-2 p2: sum of 5 fund rows vs GROSS FUNDS, deltas [0, 0, -1, 0] ($000) -> pass | FY2024 RM0 30-PBB p5 agency total: sum of 16 division subtotals, deltas [0, 1, 1, 0] ($000) -> pass | FY2024 RM0 Table RM0-2 p2: sum of 9 fund rows vs GROSS FUNDS, deltas [0, 1, 0, 1] ($000) -> pass | FY2024 DB0 30-PBB p2 agency total: sum of 9 division subtotals, deltas [0, 0, 0, -1] ($000) -> pass | FY2024 DB0 Table DB0-2 p2: sum of 5 fund rows vs GROSS FUNDS, deltas [1, -1, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 division 4000: sum of 1 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 division 5000: sum of 1 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 division 6000: sum of 5 activities vs subtotal, deltas by column [2, -1, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 agency total: sum of 5 division subtotals, deltas [0, 0, -1, 0] ($000) -> pass | FY2024 HY0 Table HY0-2 p1: sum of 1 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2024 CF0 30-PBB p2 division 4000: sum of 16 activities vs subtotal, deltas by column [0, 0, 0, -1] ($000) -> pass | FY2024 CF0 30-PBB p2 division 5000: sum of 3 activities vs subtotal, deltas by column [1, 0, 1, 0] ($000) -> pass | FY2024 CF0 30-PBB p2 division 6000: sum of 6 activities vs subtotal, deltas by column [1, 0, 0, 0] ($000) -> pass | FY2024 CF0 30-PBB p3 agency total: sum of 11 division subtotals, deltas [-1, 0, 0, -1] ($000) -> pass | FY2024 CF0 Table CF0-2 p2: sum of 6 fund rows vs GROSS FUNDS, deltas [1, 0, 0, 0] ($000) -> pass | FY2024 HG0 30-PBB p1 agency total: sum of 4 division subtotals, deltas [0, 0, 0, 0] ($000) -> pass | FY2024 HG0 Table HG0-2 p2: sum of 2 fund rows vs GROSS FUNDS, deltas [0, 1, 0, 0] ($000) -> pass | FY2025 JA0 30-PBB p2 division HS0030: sum of 28 activities vs subtotal, deltas by column [-2, 1, -1, 1] ($000) -> pass | FY2025 JA0 30-PBB p2 agency total: sum of 6 division subtotals, deltas [0, -1, 1, 0] ($000) -> pass | FY2025 FO0 30-PBB p1 division PS0023: sum of 2 activities vs subtotal, deltas by column [0, 0, -1, 0] ($000) -> pass | FY2025 FO0 30-PBB p2 agency total: sum of 12 division subtotals, deltas [-1, -2, 1, 0] ($000) -> pass | FY2025 RM0 30-PBB p3 agency total: sum of 13 division subtotals, deltas [1, 1, 0, 1] ($000) -> pass | FY2025 DB0 30-PBB p2 agency total: sum of 6 division subtotals, deltas [0, 1, 1, 0] ($000) -> pass | FY2025 HY0 30-PBB p1 division EC0039: sum of 5 activities vs subtotal, deltas by column [0, -1, 0, 0] ($000) -> pass | FY2025 HY0 30-PBB p1 agency total: sum of 1 division subtotals, deltas [0, 0, 0, 0] ($000) -> pass | FY2025 CF0 30-PBB p3 agency total: sum of 10 division subtotals, deltas [0, -1, 0, -1] ($000) -> pass | FY2025 CF0 Table CF0-2 p2: sum of 6 fund rows vs GROSS FUNDS, deltas [0, -1, 0, 0] ($000) -> pass | FY2025 HG0 30-PBB p1 agency total: sum of 3 division subtotals, deltas [0, 0, 0, 1] ($000) -> pass | FY2026 JA0 Table JA0-4 p5 division HS0030: sum of 28 activities vs subtotal, deltas [1, -2, 1, -1] ($000) -> pass | FY2026 JA0 Table JA0-4 p5 agency total: sum of 5 divisions, deltas [-1, -1, 0, 0] ($000) -> pass | FY2026 JA0 Table JA0-2 p2: sum of 7 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 FO0 Table FO0-4 p4 division PS0023: sum of 2 activities vs subtotal, deltas [0, 1, 0, 0] ($000) -> pass | FY2026 FO0 Table FO0-4 p4 agency total: sum of 11 divisions, deltas [-2, 0, 0, 0] ($000) -> pass | FY2026 FO0 Table FO0-2 p2: sum of 4 fund rows vs GROSS FUNDS, deltas [-1, 0, 0, 0] ($000) -> pass | FY2026 RM0 Table RM0-4 p7 agency total: sum of 13 divisions, deltas [1, 1, 2, 0] ($000) -> pass | FY2026 RM0 Table RM0-2 p2: sum of 8 fund rows vs GROSS FUNDS, deltas [1, 0, -1, 0] ($000) -> pass | FY2026 DB0 Table DB0-4 p4 agency total: sum of 6 divisions, deltas [1, -1, 0, -1] ($000) -> pass | FY2026 DB0 Table DB0-2 p2: sum of 4 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 HY0 Table HY0-4 p2 division EC0039: sum of 5 activities vs subtotal, deltas [-1, 1, 0, 0] ($000) -> pass | FY2026 HY0 Table HY0-4 p2 agency total: sum of 1 divisions, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 HY0 Table HY0-2 p1: sum of 1 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 CF0 Table CF0-4 p5 agency total: sum of 10 divisions, deltas [-1, 1, 0, 0] ($000) -> pass | FY2026 CF0 Table CF0-2 p2: sum of 5 fund rows vs GROSS FUNDS, deltas [-1, 1, 0, 1] ($000) -> pass | FY2026 HG0 Table HG0-4 p3 agency total: sum of 2 divisions, deltas [0, 1, 1, 0] ($000) -> pass | FY2026 HG0 Table HG0-2 p2: sum of 1 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2027 JA0 30-PBB p2 division HS0030: sum of 28 activities vs subtotal, deltas by column [-2, -2, -1, -3] ($000) -> pass | FY2027 JA0 30-PBB p2 agency total: sum of 5 division subtotals, deltas [-1, 1, 0, -1] ($000) -> pass | FY2027 JA0 Table JA0-2 p2: sum of 7 fund rows vs GROSS FUNDS, deltas [0, 1, 0, 0] ($000) -> pass | FY2027 FO0 30-PBB p1 division PS0023: sum of 2 activities vs subtotal, deltas by column [1, 0, 0, 0] ($000) -> pass | FY2027 FO0 30-PBB p1 agency total: sum of 11 division subtotals, deltas [-1,
- cross-book disagreements (same FY/stage/code, >$2K apart; later book preferred via x_preferred): 2022 actual JA0 AMP000 total: FY2025 book 33,466,000, FY2024 book 33,534,000 | 2022 actual JA0 AFO000 total: FY2025 book 3,079,000, FY2024 book 3,025,000 | 2022 actual JA0 HS0029 total: FY2025 book 279,438,000, FY2024 book 280,259,000 | 2022 actual JA0 HS0030 total: FY2025 book 625,848,000, FY2024 book 625,869,000 | 2025 approved JA0 H02902 total: FY2026 book 42,867,000, FY2025 book 42,943,000 | 2025 approved JA0 H02905 total: FY2026 book 91,735,000, FY2025 book 91,660,000 | 2025 approved FO0 P01903 total: FY2026 book 18,405,000, FY2025 book 18,312,000 | 2025 approved FO0 PS0019 total: FY2026 book 18,405,000, FY2025 book 18,312,000 | 2025 approved RM0 AFO003 total: FY2026 book 1,120,000, FY2025 book 1,010,000 | 2025 approved RM0 AFO005 total: FY2026 book 567,000, FY2025 book 577,000 | 2025 approved RM0 AFO000 total: FY2026 book 2,378,000, FY2025 book 2,278,000 | 2025 approved RM0 H04201 total: FY2026 book 175,000, FY2025 book 179,000 | 2025 approved RM0 H04202 total: FY2026 book 1,128,000, FY2025 book 1,151,000 | 2025 approved RM0 H04205 total: FY2026 book 381,000, FY2025 book 355,000 | 2025 approved RM0 H04504 total: FY2026 book 1,367,000, FY2025 book 100,000 | 2025 approved RM0 HS0045 total: FY2026 book 37,390,000, FY2025 book 36,123,000 | 2025 approved RM0 H04802 total: FY2026 book 27,140,000, FY2025 book 22,840,000 | 2025 approved RM0 H04805 total: FY2026 book 1,391,000, FY2025 book 5,691,000 | 2025 approved RM0 HS0053 total: FY2026 book 20,351,000, FY2025 book 21,717,000 | 2025 approved CF0 AFO003 total: FY2026 book 2,141,000, FY2025 book 2,222,000 | 2025 approved CF0 AFO000 total: FY2026 book 4,023,000, FY2025 book 4,104,000 | 2025 approved CF0 AMP026 total: FY2026 book 0, FY2025 book -3,000 | 2025 approved CF0 AMP000 total: FY2026 book 24,947,000, FY2025 book 24,944,000 | 2025 approved CF0 O00111 total: FY2026 book 556,000, FY2025 book 559,000 | 2025 approved CF0 GO0047 total: FY2026 book 6,545,000, FY2025 book 6,548,000 | 2025 approved CF0 O05201 total: FY2026 book 15,504,000, FY2025 book 15,422,000 | 2025 approved CF0 GO0052 total: FY2026 book 75,929,000, FY2025 book 75,847,000
- FY2024 old-code -> FY2025 code crosswalk (FY2024 approved): FO0 P02301: FY2024 book 171,000 vs FY2025 book restated 171,000 (delta +0) | FO0 P02303: FY2024 book 45,515,000 vs FY2025 book restated 45,515,000 (delta +0) | FO0 P04502: FY2024 book 3,720,000 vs FY2025 book restated 3,720,000 (delta +0) | HY0 R03903: FY2024 book 4,400,000 vs FY2025 book restated 4,400,000 (delta +0) | HY0 R03904: FY2024 book 0 vs FY2025 book restated 0 (delta +0) | HY0 R03905: FY2024 book 128,094,000 vs FY2025 book restated 128,094,000 (delta +0) | HY0 R03906: FY2024 book 10,581,000 vs FY2025 book restated 10,581,000 (delta +0) | HY0 R03907: FY2024 book 43,296,000 vs FY2025 book restated 43,296,000 (delta +0) | JA0 H03002: FY2024 book 79,033,000 vs FY2025 book restated 93,339,000 (delta +14,306,000) | JA0 H03003: FY2024 book 59,994,000 vs FY2025 book restated 59,994,000 (delta +0) | JA0 H03004: FY2024 book 31,818,000 vs FY2025 book restated 12,421,000 (delta -19,397,000) | JA0 H03007: FY2024 book 2,940,000 vs FY2025 book restated 2,940,000 (delta +0) | JA0 H03008: FY2024 book 42,536,000 vs FY2025 book restated 42,536,000 (delta +0) | JA0 H03009: FY2024 book 2,799,000 vs FY2025 book restated 4,259,000 (delta +1,460,000) | JA0 H03010: FY2024 book 51,764,000 vs FY2025 book restated 60,770,000 (delta +9,006,000) | JA0 H03011: FY2024 book 4,935,000 vs FY2025 book restated 4,935,000 (delta +0) | JA0 H03012: FY2024 book 86,929,000 vs FY2025 book restated 83,014,000 (delta -3,915,000) | JA0 H03013: FY2024 book 4,222,000 vs FY2025 book restated 4,222,000 (delta +0) | JA0 H03014-H03016: FY2024 book 11,541,000 vs FY2025 book restated 11,542,000 (delta +1,000) | JA0 H03017: FY2024 book 73,209,000 vs FY2025 book restated 73,209,000 (delta +0) | JA0 H03018: FY2024 book 10,875,000 vs FY2025 book restated 10,875,000 (delta +0) | JA0 H03019: FY2024 book 1,150,000 vs FY2025 book restated 1,150,000 (delta +0) | JA0 H03022: FY2024 book 1,980,000 vs FY2025 book restated 1,980,000 (delta +0) | JA0 H03023: FY2024 book 12,032,000 vs FY2025 book restated 12,032,000 (delta +0) | RM0 H04308: FY2024 book 29,637,000 vs FY2025 book restated 29,637,000 (delta +0) | RM0 H04504: FY2024 book 1,467,000 vs FY2025 book restated 1,467,000 (delta +0)
- event dates: budget_enacted/budget_revised = Local Budget Act 2nd reading {2024: '2023-05-30', 2025: '2024-06-12', 2026: '2025-07-28', 2027: '2026-06-23'}; budget_proposed = BSA introduced on behalf of the Mayor {2025: '2024-04-03', 2026: '2025-06-02', 2027: '2026-04-14'} (FY2024 proposal date not in downloaded docs -> blank); BSA policy rows = law/act effective date {2024: '2023-09-06', 2025: '2024-09-18', 2026: '2025-12-06', 2027: '2026-08-13'}; committee items = markup date when printed, else Local Budget Act date
- mapping: Table XX0-5 lines before 'Mayor's Proposed Budget' -> budget_proposed; lines between it and 'District's Approved Budget' -> budget_revised (Council changes); FY2027 Council-level changes taken from the activity-level Council chart instead of JA0-5 to avoid double counting
- coverage (stage[+funds] by FY x agency JA0/FO0/RM0/DB0/HY0/CF0/HG0):
| FY2021 | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds |
| FY2022 | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds |
| FY2023 | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds |
| FY2024 | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds |
| FY2025 | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds,prop | actu+funds,appr+funds | actu+funds,appr+funds |
| FY2026 | appr+funds,prop | appr+funds,prop | appr+funds | appr+funds | appr+funds,prop | appr+funds | appr+funds |
| FY2027 | appr+funds | appr+funds | appr+funds,prop | appr+funds | appr+funds,prop | appr+funds | appr+funds |
- warnings (0):

### 2026-10-10 13:57 — 37_parse_dc_budget: notes
- Earlier 37_parse_dc_budget entries from today were development runs; the last 'DC budget lines and policy events' entry is the authoritative run.

### 2026-10-10 13:58 — 42_pull_propublica: stage
- 2,533 org JSONs read (0 target EINs with no ProPublica record); 18,265 filings_with_data rows; skipped formtypes {}; 0 bad periods
- tax_prd_yr equals derived fiscal_year (period-end year) on 100.0% of rows
- staged 18,265 rows, 2,002 EINs -> interim/stage_fact_org_financials__propublica.csv; duplicates on (ein, tax_period_end, return_type, source_id): 0
- Calvary total_revenue QC: TY2020 3,851,984 OK; TY2021 8,867,250 OK
- cross-check vs SOI: 18,265 matching (ein, period, form) rows; equal total_revenue 100.0%, total_expenses 100.0%, total_assets_eoy 100.0%
- ProPublica rows with no SOI row: 0 (by fiscal_year {})
- rows by fiscal_year x return_type:
```
return_type   990  990EZ  990PF    All
fiscal_year                           
2007            0      1      1      2
2008            0      1      1      2
2009            0      3      4      7
2010           53     20     20     93
2011          391     61    812   1264
2012          439     70    936   1445
2013          447     65    960   1472
2014          447     66    999   1512
2015          464     72   1017   1553
2016          475     66    107    648
2017          483     69      4    556
2018          492     71     15    578
2019          512     73   1082   1667
2020          510     75   1182   1767
2021          535     74   1229   1838
2022          549     69   1245   1863
2023          548     76   1243   1867
2024           28      4     99    131
All          6373    936  10956  18265
```

### 2026-10-10 13:58 — 42_pull_propublica: reconcile
- 52 rows -> interim/calvary_financials_reconciliation.csv; fiscal years 2011-2025; sources {'soi_extract': 13, 'propublica': 13, 'audit': 8, 'nccs_efile': 7, 'form990_pdf': 6, 'form990_pdf_prior_year_column': 3, 'audit_comparative': 2}
- 990-basis sources (SOI, ProPublica, NCCS, 990 PDFs): 0 of 42 rows differ >1% from the reference: none
- audits (GAAP basis): 10 of 10 rows differ >1% on at least one metric: FY2014 total_revenue;total_expenses; FY2015 total_revenue;total_expenses; FY2016 total_revenue;total_expenses; FY2017 total_revenue;total_expenses; FY2018 total_revenue;total_expenses; FY2019 total_revenue;total_expenses; FY2020 gov_grants; FY2021 total_revenue;total_expenses;gov_grants; FY2022 total_revenue;total_expenses; FY2023 total_revenue;total_expenses
- TY2020 total_revenue by 990-basis source: soi_extract 3,851,984, propublica 3,851,984, nccs_efile 3,851,984
- TY2021 total_revenue by 990-basis source: soi_extract 8,867,250, propublica 8,867,250

### 2026-10-10 13:58 — 42_pull_propublica: notes
- appended 'Financial series' to notes_for_analysis.md
- Coverage. SOI extract: 77,152 rows, 9,329 EINs, fiscal years (period-end) 2011-2023 complete; 2024 partial (703 rows, early filers in the 24 extract). 990 rows/yr 1,833-2,790, 990-EZ 512-857. 990-PF rows/yr 4,559 at most but FY2016-FY2018 only 310, 23, 110: IRS published no 990-PF extract for processing years 2017-2019, and NCCS Core and ProPublica share the gap (the XML parse is the only fill).
- NCCS e-file Part VIII (source of government_grants): 22,080 Form 990 rows, 3,038 EINs, TY2010-TY2022 (TY2021 partial, TY2022 thin; e-filers only, so early years under-cover paper filers).
- Universe EINs with >=1 SOI row: core_peers 18/18; dc_sector 524/1,024; dmv_funders 5,744/7,705; national_women 1,280/2,452; size_matched 555/557. Of the 500 dc_sector EINs with no SOI row, 95% have BMF revenue under $50K (990-N range) and 451 have no e-filed 990/990-EZ.
- ProPublica (18,265 rows, 2,002 EINs) equals SOI on total_revenue for 100.0% of 18,265 overlapping rows and adds 0 rows SOI lacks: its financial fields are the SOI extract fields, so it is a transcription check, not an independent source.
- Calvary (SOI total revenue; government share = Part VIII-1e / total revenue from NCCS e-file): FY11 1.45M, FY12 2.02M, FY13 1.89M, FY14 2.07M, FY15 2.01M gov 44%, FY16 1.99M gov 47%, FY17 2.26M gov 43%, FY18 2.15M gov 45%, FY19 2.49M gov 51%, FY20 3.90M gov 56%, FY21 3.85M gov 13%, FY22 8.87M, FY23 4.46M. Contributions are 1.46M-8.95M and exceed total revenue every year because special events net is negative every year (-19,511 to -149,059); program service revenue is 0 every year.
- Calvary 990 vs audits (interim/calvary_financials_reconciliation.csv): 0 of 42 990-basis rows (SOI, ProPublica, NCCS, 990 PDFs) differ >1%. Audit total revenue runs 0% to 9% and expenses 0% to 9% vs the 990 (GAAP presentation: in-kind, special-event costs); net assets match every year. Audit government revenue equals 990 line 1e in FY15-FY19, then: FY20 audit 1,838,919 vs 990 line 1e 2,166,119 (line 1f other contributions 1,570,112); FY21 audit 1,981,161 vs 990 line 1e 503,222 (line 1f other contributions 3,063,099).
- Government share of revenue (990 line 1e / total revenue, NCCS e-file), core_peers: TY2019 n=17: p25 34%, median 54%, p75 78%, 0% with none; Calvary 56% (above 53% of them); TY2020 n=18: p25 32%, median 53%, p75 76%, 6% with none; Calvary 13% (above 22% of them).
- Government share of revenue (990 line 1e / total revenue, NCCS e-file), dc_sector: TY2019 n=264: p25 0%, median 0%, p75 16%, 64% with none; Calvary 56% (above 85% of them); TY2020 n=305: p25 0%, median 0%, p75 25%, 50% with none; Calvary 13% (above 66% of them).
- Core-peer median government share by tax year (NCCS): TY2011 46%, TY2012 46%, TY2013 47%, TY2014 39%, TY2015 50%, TY2016 48%, TY2017 51%, TY2018 52%, TY2019 54%, TY2020 53%, TY2021 52%.

### 2026-10-10 14:00 — 44_web_peers_funders
- search hits 757; pages listed 71, with content 67
- by group (listed, fetched): peer 35/35, funder 27/27, inkind 9/9
- failed/empty: nuvaya_fin_reports (http:http_403; chars 0 -> tavily no_content); christhouse_ar_2025_pdf (ok); miriams_ar_fy25 (http:ok; chars 21 -> tavily no_content); hormd_ar_2024 (http:http_404; chars 0 -> tavily no_content); ik_hef_home (http:ok; chars 18 -> tavily no_content)
- this run: Tavily search 0, extract 0, HTTP GET 0, cache hits 170; cumulative (manifest): search 104/300, extract 9/200, HTTP 115

### 2026-10-10 14:01 — 30_fetch_xml: progress
- pass 1: 22,000/31,469 done in 31.0 min (11.8/s); 1,751 MB on disk for done files; ok 22,000, not_found 0, error 0

### 2026-10-10 14:02 — 30_fetch_xml: restart
- stopped run 1 at ~22,000/31,469 (all ok, 0 errors): GT objects starting with a UTF-8 BOM were being rejected by XmlStore.get() and re-read from IRS ZIPs at 4 req/s (6,192 IRS files so far, nearly all BOM, GT has them). Added a BOM-tolerant get() in PooledXmlStore (script 30 only) and restarted; cached files are reused. Last 721 files written before the stop all parse (no truncation).

### 2026-10-10 14:02 — 30_fetch_xml: targets
- scope EINs 8,705; EINs with a TY2020+ e-filed 990/EZ/PF in the index 6,772
- returns 31,469 (latest per EIN+period+type) {'990PF': 24877, '990': 4858, '990EZ': 1734}; with >1 submission 351
- GT S3 at 20 req/s, IRS ZIP fallback 4 req/s; 16 threads

### 2026-10-10 14:02 — 30_fetch_xml: progress
- pass 1: 2,000/31,469 done in 0.0 min (3743.3/s); 93 MB on disk for done files; ok 2,000, not_found 0, error 0

### 2026-10-10 14:02 — 30_fetch_xml: progress
- pass 1: 4,000/31,469 done in 0.0 min (4797.6/s); 253 MB on disk for done files; ok 4,000, not_found 0, error 0

### 2026-10-10 14:02 — 30_fetch_xml: progress
- pass 1: 6,000/31,469 done in 0.0 min (5233.1/s); 363 MB on disk for done files; ok 6,000, not_found 0, error 0

### 2026-10-10 14:02 — 30_fetch_xml: progress
- pass 1: 8,000/31,469 done in 0.0 min (5438.2/s); 608 MB on disk for done files; ok 8,000, not_found 0, error 0

### 2026-10-10 14:02 — 30_fetch_xml: progress
- pass 1: 10,000/31,469 done in 0.0 min (5590.5/s); 768 MB on disk for done files; ok 10,000, not_found 0, error 0

### 2026-10-10 14:02 — 30_fetch_xml: progress
- pass 1: 12,000/31,469 done in 0.0 min (5690.3/s); 901 MB on disk for done files; ok 12,000, not_found 0, error 0

### 2026-10-10 14:02 — 30_fetch_xml: progress
- pass 1: 14,000/31,469 done in 0.0 min (5757.2/s); 1,119 MB on disk for done files; ok 14,000, not_found 0, error 0

### 2026-10-10 14:02 — 30_fetch_xml: progress
- pass 1: 16,000/31,469 done in 0.0 min (5805.3/s); 1,241 MB on disk for done files; ok 16,000, not_found 0, error 0

### 2026-10-10 14:02 — 30_fetch_xml: progress
- pass 1: 18,000/31,469 done in 0.1 min (5830.3/s); 1,439 MB on disk for done files; ok 18,000, not_found 0, error 0

### 2026-10-10 14:02 — 30_fetch_xml: progress
- pass 1: 20,000/31,469 done in 0.1 min (5882.9/s); 1,558 MB on disk for done files; ok 20,000, not_found 0, error 0

### 2026-10-10 14:02 — 30_fetch_xml: progress
- pass 1: 22,000/31,469 done in 0.1 min (5884.7/s); 1,751 MB on disk for done files; ok 22,000, not_found 0, error 0

### 2026-10-10 14:04 — 30_fetch_xml: progress
- pass 1: 24,000/31,469 done in 1.6 min (246.9/s); 1,887 MB on disk for done files; ok 24,000, not_found 0, error 0

### 2026-10-10 14:04 — 43_web_calvary
- support page: 98 organizations (3 flagged in-kind); Phase 1 PDF had 98 (11 truncated). Names absent from the PDF parse: 11
- truncated names recovered: Morris, Mann -> Morris, Manning & Martin, LLP; Nelson Mulli -> Nelson Mullins; NFP Golden & -> NFP Golden & Cohen; Robert Charle -> Robert Charles Lesser Co.; Sapodilla's C -> Sapodilla's Caribbean Restaurant and Catering; Saul Ewing A -> Saul Ewing Arnstein & Lehr LLP; Southern Com -> Southern Company; The Brand Gu -> The Brand Guild; The Menkiti G -> The Menkiti Group; United Bank -> United Bank; Women's Ene -> Women's Energy Resource Council
- PDFs seen: 98 (financials page links + WP media library + off-site search); kept as new: 22: 2015-07-Corporate-Partner-Program-packet.pdf [funder_list, ok]; CWS-Audited-Financial-Statements-2014.pdf [audit, ok]; CWS-Form-990-2014.pdf [form_990, ok]; CWS-form-990-2013.pdf [form_990, ok]; Corporate-Partners-Program-packet.pdf [funder_list, ok]; Corporate-Partners-Program-packet_11-11-2014.pdf [funder_list, ok]; Corporate-Partners-Program-packet_11-13-2014.pdf [funder_list, ok]; FY2013-Annual-Report-simple-version-FINAL.pdf [annual_report, ok]; What-Do-Corporate-Partners-Do_combined.pdf [funder_list, ok]; audited-statements-2013.pdf [audit, ok]; Calvary-Womens-Services-2014-Annual-Report.pdf [annual_report, ok]; 2017-Hope-Awards-Sponsorship-Opportunities.pdf [funder_list, ok]; Step-Up-DC-2016-Year-End-Report.pdf [funder_list, ok]; 2019-02-04-Calvary-Annual-Design.pdf [annual_report, ok]; Calvary-Womens-Services-FY18-Annual-Report.pdf [annual_report, ok]; CWS-Corporate-Partners-Program-Overview.pdf [funder_list, ok]; Hope-Awards-Sponsors.pdf [funder_list, ok]; 2024-Corporate-Partners-Program-Opportunities_CWS.pdf [funder_list, ok]; 2025-Hope-Gala-Sponsorship_CWS-2.pdf [funder_list, ok]; 2025-Hope-Gala-Sponsorship_CWS-2.pdf [funder_list, duplicate_of_web:https://www.calvaryservices.org/wp-content/uploads/2025/02/2025-Hope-Gala-Sponsorship_CWS-2.pdf]; Calvary-Newsletter-02_25.pdf [funder_list, ok]; 521307706_2022_25813620221_A133.pdf [other, ok; found by cal_audit_fy24]
- off-site search hits: 104 results; Calvary PDFs kept: 1; rejected: Calvary-Independent-Auditors-Report.pdf (cal_audit_fy25: not a Calvary Women's Services document)
- annual-report donors: 72 org rows; named lists/mentions 86 rows; individual band-count rows 3; Calvary-Womens-Services-2014-Annual-Report.pdf: 72 org donor entries, 182 individual entries (counted only); 2017-Hope-Awards-Sponsorship-Opportunities.pdf [Hope Awards Dinner: companies that have sponsored (cumulative)]: 40; Step-Up-DC-2016-Year-End-Report.pdf [Step Up DC supporters ('supported the program this year')]: 4; 2025-Hope-Gala-Sponsorship_CWS-2.pdf [Hope Gala: Past Event Sponsors (cumulative)]: 39
- new audits: 314 financial/note rows, 4 SEFA rows; CWS-Audited-Financial-Statements-2014.pdf: no SEFA in the PDF; 521307706_2022_25813620221_A133.pdf: SEFA p29 4 programs sum 4,067,718 vs printed total 4,067,718
- this run: Tavily search 0, extract 0, HTTP GET 0, cache hits 55; cumulative (manifest): search 104/300, extract 9/200, HTTP 115

### 2026-10-10 14:04 — 45_stage_web_grants
- staged rows 1012: by source_type {'support_page': 252, 'annual_report': 635, 'web': 125}; confidence {'medium': 989, 'high': 23}
- amount stated 30; band only 393; unknown 589
- recipient Calvary 259; core peers 745 (13 peers); whole-list keyword keeps 8
- Calvary-site rows by type {'support_page': 98, 'annual_report': 74, 'anonymous_skipped': 1, 'web': 83}
- pages parsed 19/62; not parsed or failed: nsv_funding_reports (index page (links to annual reports)); openarms_about (no funder list on the site); nebw_reports (index page (links to annual reports)); nebw_ar_2025 (2025 annual report text has no funder list); msp_ar_fy22 (no funder list); dcsafe_ar_fy25 (no funder list (revenue split only)); nuvaya_fin_reports (HTTP 403 and Tavily extract empty); christhouse_ar_2025 (landing page; PDF has no text layer); christhouse_ar_2025_pdf (image-only PDF (12 chars of text)); ehdc_ar_2024 (landing page); ehdc_ar_2024_pdf (2024 annual report text has no funder list); cfh_ar_list (index page); thrive_impact_2024 (lists corporate volunteer groups, not funders); miriams_financials (index page); miriams_ar_fy25 (mkannualreport.org is JavaScript-rendered; no text retrieved); coh_ar_2025 (2025 annual report summary has no funder list); coh_impact_2024 (same list as coh_funders (parsed there)); chgw_home (home page); chgw_impact_fy24 (FY24 impact report text has no funder list); doorways_ar_2023 (landing page); doorways_ar_2023_issuu (issuu viewer; no document text); hormd_honor_roll (URL now serves the About Us page; no honor roll content); hormd_ar_2024 (PDF returns HTTP 404); hormd_ar_page (annual report page has no donor list); meyer_118m_28 (2020 list (outside 2024-2026); no Calvary or peers); meyer_635k_8 (2022 list (outside 2024-2026); no Calvary or peers); meyer_rapid (program description only; no grantee list); meyer_news (news index); abell_grantmaking (guidelines only; no gran
- in-kind evidence rows 17: MGAC=unclear; MGAC=in_kind; MGAC=in_kind; MGAC=cash; Health Equity Fund=cash; Health Equity Fund=cash; Health Equity Fund=cash; Health Equity Fund=cash; Capital One=unclear; Capital One=unclear; Capital One=cash; World Bank Community Connections Fund=cash; World Bank Community Connections Fund=cash; World Bank Community Connections Fund=cash; Frontier Co-op / Aura Cacia (Frontier Co-op Giving Fund)=in_kind; Frontier Co-op / Aura Cacia (Frontier Co-op Giving Fund)=unclear; MGAC; Capital One; World Bank Community Connections Fund=unclear

### 2026-10-10 14:05 — 45_stage_web_grants
- staged rows 1002: by source_type {'support_page': 248, 'annual_report': 629, 'web': 125}; confidence {'medium': 979, 'high': 23}
- amount stated 30; band only 390; unknown 582
- recipient Calvary 259; core peers 735 (13 peers); whole-list keyword keeps 8
- Calvary-site rows by type {'support_page': 98, 'annual_report': 74, 'anonymous_skipped': 1, 'web': 83}
- pages parsed 19/62; not parsed or failed: nsv_funding_reports (index page (links to annual reports)); openarms_about (no funder list on the site); nebw_reports (index page (links to annual reports)); nebw_ar_2025 (2025 annual report text has no funder list); msp_ar_fy22 (no funder list); dcsafe_ar_fy25 (no funder list (revenue split only)); nuvaya_fin_reports (HTTP 403 and Tavily extract empty); christhouse_ar_2025 (landing page; PDF has no text layer); christhouse_ar_2025_pdf (image-only PDF (12 chars of text)); ehdc_ar_2024 (landing page); ehdc_ar_2024_pdf (2024 annual report text has no funder list); cfh_ar_list (index page); thrive_impact_2024 (lists corporate volunteer groups, not funders); miriams_financials (index page); miriams_ar_fy25 (mkannualreport.org is JavaScript-rendered; no text retrieved); coh_ar_2025 (2025 annual report summary has no funder list); coh_impact_2024 (same list as coh_funders (parsed there)); chgw_home (home page); chgw_impact_fy24 (FY24 impact report text has no funder list); doorways_ar_2023 (landing page); doorways_ar_2023_issuu (issuu viewer; no document text); hormd_honor_roll (URL now serves the About Us page; no honor roll content); hormd_ar_2024 (PDF returns HTTP 404); hormd_ar_page (annual report page has no donor list); meyer_118m_28 (2020 list (outside 2024-2026); no Calvary or peers); meyer_635k_8 (2022 list (outside 2024-2026); no Calvary or peers); meyer_rapid (program description only; no grantee list); meyer_news (news index); abell_grantmaking (guidelines only; no gran
- in-kind evidence rows 17: MGAC=unclear; MGAC=in_kind; MGAC=in_kind; MGAC=cash; Health Equity Fund=cash; Health Equity Fund=cash; Health Equity Fund=cash; Health Equity Fund=cash; Capital One=unclear; Capital One=unclear; Capital One=cash; World Bank Community Connections Fund=cash; World Bank Community Connections Fund=cash; World Bank Community Connections Fund=cash; Frontier Co-op / Aura Cacia (Frontier Co-op Giving Fund)=in_kind; Frontier Co-op / Aura Cacia (Frontier Co-op Giving Fund)=unclear; MGAC; Capital One; World Bank Community Connections Fund=unclear

### 2026-10-10 14:05 — 30_fetch_xml: progress
- pass 1: 26,000/31,469 done in 3.3 min (132.0/s); 2,090 MB on disk for done files; ok 26,000, not_found 0, error 0

### 2026-10-10 14:05 — 45_stage_web_grants
- staged rows 1004: by source_type {'support_page': 249, 'annual_report': 630, 'web': 125}; confidence {'medium': 981, 'high': 23}
- amount stated 30; band only 391; unknown 583
- recipient Calvary 259; core peers 737 (13 peers); whole-list keyword keeps 8
- Calvary-site rows by type {'support_page': 98, 'annual_report': 74, 'anonymous_skipped': 1, 'web': 83}
- pages parsed 19/62; not parsed or failed: nsv_funding_reports (index page (links to annual reports)); openarms_about (no funder list on the site); nebw_reports (index page (links to annual reports)); nebw_ar_2025 (2025 annual report text has no funder list); msp_ar_fy22 (no funder list); dcsafe_ar_fy25 (no funder list (revenue split only)); nuvaya_fin_reports (HTTP 403 and Tavily extract empty); christhouse_ar_2025 (landing page; PDF has no text layer); christhouse_ar_2025_pdf (image-only PDF (12 chars of text)); ehdc_ar_2024 (landing page); ehdc_ar_2024_pdf (2024 annual report text has no funder list); cfh_ar_list (index page); thrive_impact_2024 (lists corporate volunteer groups, not funders); miriams_financials (index page); miriams_ar_fy25 (mkannualreport.org is JavaScript-rendered; no text retrieved); coh_ar_2025 (2025 annual report summary has no funder list); coh_impact_2024 (same list as coh_funders (parsed there)); chgw_home (home page); chgw_impact_fy24 (FY24 impact report text has no funder list); doorways_ar_2023 (landing page); doorways_ar_2023_issuu (issuu viewer; no document text); hormd_honor_roll (URL now serves the About Us page; no honor roll content); hormd_ar_2024 (PDF returns HTTP 404); hormd_ar_page (annual report page has no donor list); meyer_118m_28 (2020 list (outside 2024-2026); no Calvary or peers); meyer_635k_8 (2022 list (outside 2024-2026); no Calvary or peers); meyer_rapid (program description only; no grantee list); meyer_news (news index); abell_grantmaking (guidelines only; no gran
- in-kind evidence rows 17: MGAC=unclear; MGAC=in_kind; MGAC=in_kind; MGAC=cash; Health Equity Fund=cash; Health Equity Fund=cash; Health Equity Fund=cash; Health Equity Fund=cash; Capital One=unclear; Capital One=unclear; Capital One=cash; World Bank Community Connections Fund=cash; World Bank Community Connections Fund=cash; World Bank Community Connections Fund=cash; Frontier Co-op / Aura Cacia (Frontier Co-op Giving Fund)=in_kind; Frontier Co-op / Aura Cacia (Frontier Co-op Giving Fund)=unclear; MGAC; Capital One; World Bank Community Connections Fund=unclear

### 2026-10-10 14:06 — 43_web_calvary
- support page: 98 organizations (3 flagged in-kind); Phase 1 PDF had 98 (11 truncated). Names absent from the PDF parse: 11
- truncated names recovered: Morris, Mann -> Morris, Manning & Martin, LLP; Nelson Mulli -> Nelson Mullins; NFP Golden & -> NFP Golden & Cohen; Robert Charle -> Robert Charles Lesser Co.; Sapodilla's C -> Sapodilla's Caribbean Restaurant and Catering; Saul Ewing A -> Saul Ewing Arnstein & Lehr LLP; Southern Com -> Southern Company; The Brand Gu -> The Brand Guild; The Menkiti G -> The Menkiti Group; United Bank -> United Bank; Women's Ene -> Women's Energy Resource Council
- PDFs seen: 98 (financials page links + WP media library + off-site search); kept as new: 22: 2015-07-Corporate-Partner-Program-packet.pdf [funder_list, ok]; CWS-Audited-Financial-Statements-2014.pdf [audit, ok]; CWS-Form-990-2014.pdf [form_990, ok]; CWS-form-990-2013.pdf [form_990, ok]; Corporate-Partners-Program-packet.pdf [funder_list, ok]; Corporate-Partners-Program-packet_11-11-2014.pdf [funder_list, ok]; Corporate-Partners-Program-packet_11-13-2014.pdf [funder_list, ok]; FY2013-Annual-Report-simple-version-FINAL.pdf [annual_report, ok]; What-Do-Corporate-Partners-Do_combined.pdf [funder_list, ok]; audited-statements-2013.pdf [audit, ok]; Calvary-Womens-Services-2014-Annual-Report.pdf [annual_report, ok]; 2017-Hope-Awards-Sponsorship-Opportunities.pdf [funder_list, ok]; Step-Up-DC-2016-Year-End-Report.pdf [funder_list, ok]; 2019-02-04-Calvary-Annual-Design.pdf [annual_report, ok]; Calvary-Womens-Services-FY18-Annual-Report.pdf [annual_report, ok]; CWS-Corporate-Partners-Program-Overview.pdf [funder_list, ok]; Hope-Awards-Sponsors.pdf [funder_list, ok]; 2024-Corporate-Partners-Program-Opportunities_CWS.pdf [funder_list, ok]; 2025-Hope-Gala-Sponsorship_CWS-2.pdf [funder_list, ok]; 2025-Hope-Gala-Sponsorship_CWS-2.pdf [funder_list, duplicate_of_web:https://www.calvaryservices.org/wp-content/uploads/2025/02/2025-Hope-Gala-Sponsorship_CWS-2.pdf]; Calvary-Newsletter-02_25.pdf [funder_list, ok]; 521307706_2022_25813620221_A133.pdf [other, ok; found by cal_audit_fy24]
- off-site search hits: 104 results; Calvary PDFs kept: 1; rejected: Calvary-Independent-Auditors-Report.pdf (cal_audit_fy25: not a Calvary Women's Services document)
- annual-report donors: 72 org rows; named lists/mentions 93 rows; individual band-count rows 3; Calvary-Womens-Services-2014-Annual-Report.pdf: 72 org donor entries, 182 individual entries (counted only); 2017-Hope-Awards-Sponsorship-Opportunities.pdf [Hope Awards Dinner: companies that have sponsored (cumulative)]: 40; Step-Up-DC-2016-Year-End-Report.pdf [Step Up DC supporters ('supported the program this year')]: 4; 2025-Hope-Gala-Sponsorship_CWS-2.pdf [Hope Gala: Past Event Sponsors (cumulative)]: 39
- new audits: 314 financial/note rows, 4 SEFA rows; CWS-Audited-Financial-Statements-2014.pdf: no SEFA in the PDF; 521307706_2022_25813620221_A133.pdf: SEFA p29 4 programs sum 4,067,718 vs printed total 4,067,718
- this run: Tavily search 0, extract 0, HTTP GET 0, cache hits 55; cumulative (manifest): search 104/300, extract 9/200, HTTP 115

### 2026-10-10 14:06 — 45_stage_web_grants
- staged rows 1011: by source_type {'support_page': 249, 'annual_report': 630, 'web': 132}; confidence {'medium': 988, 'high': 23}
- amount stated 30; band only 392; unknown 589
- recipient Calvary 266; core peers 737 (13 peers); whole-list keyword keeps 8
- Calvary-site rows by type {'support_page': 98, 'annual_report': 74, 'anonymous_skipped': 1, 'web': 90}
- pages parsed 19/62; not parsed or failed: nsv_funding_reports (index page (links to annual reports)); openarms_about (no funder list on the site); nebw_reports (index page (links to annual reports)); nebw_ar_2025 (2025 annual report text has no funder list); msp_ar_fy22 (no funder list); dcsafe_ar_fy25 (no funder list (revenue split only)); nuvaya_fin_reports (HTTP 403 and Tavily extract empty); christhouse_ar_2025 (landing page; PDF has no text layer); christhouse_ar_2025_pdf (image-only PDF (12 chars of text)); ehdc_ar_2024 (landing page); ehdc_ar_2024_pdf (2024 annual report text has no funder list); cfh_ar_list (index page); thrive_impact_2024 (lists corporate volunteer groups, not funders); miriams_financials (index page); miriams_ar_fy25 (mkannualreport.org is JavaScript-rendered; no text retrieved); coh_ar_2025 (2025 annual report summary has no funder list); coh_impact_2024 (same list as coh_funders (parsed there)); chgw_home (home page); chgw_impact_fy24 (FY24 impact report text has no funder list); doorways_ar_2023 (landing page); doorways_ar_2023_issuu (issuu viewer; no document text); hormd_honor_roll (URL now serves the About Us page; no honor roll content); hormd_ar_2024 (PDF returns HTTP 404); hormd_ar_page (annual report page has no donor list); meyer_118m_28 (2020 list (outside 2024-2026); no Calvary or peers); meyer_635k_8 (2022 list (outside 2024-2026); no Calvary or peers); meyer_rapid (program description only; no grantee list); meyer_news (news index); abell_grantmaking (guidelines only; no gran
- in-kind evidence rows 17: MGAC=unclear; MGAC=in_kind; MGAC=in_kind; MGAC=cash; Health Equity Fund=cash; Health Equity Fund=cash; Health Equity Fund=cash; Health Equity Fund=cash; Capital One=unclear; Capital One=unclear; Capital One=cash; World Bank Community Connections Fund=cash; World Bank Community Connections Fund=cash; World Bank Community Connections Fund=cash; Frontier Co-op / Aura Cacia (Frontier Co-op Giving Fund)=in_kind; Frontier Co-op / Aura Cacia (Frontier Co-op Giving Fund)=unclear; MGAC; Capital One; World Bank Community Connections Fund=unclear

### 2026-10-10 14:07 — 45_stage_web_grants
- staged rows 1013: by source_type {'support_page': 249, 'annual_report': 630, 'web': 134}; confidence {'medium': 988, 'high': 25}
- amount stated 32; band only 392; unknown 589
- recipient Calvary 266; core peers 739 (14 peers); whole-list keyword keeps 8
- Calvary-site rows by type {'support_page': 98, 'annual_report': 74, 'anonymous_skipped': 1, 'web': 90}
- pages parsed 19/62; not parsed or failed: nsv_funding_reports (index page (links to annual reports)); openarms_about (no funder list on the site); nebw_reports (index page (links to annual reports)); nebw_ar_2025 (2025 annual report text has no funder list); msp_ar_fy22 (no funder list); dcsafe_ar_fy25 (no funder list (revenue split only)); nuvaya_fin_reports (HTTP 403 and Tavily extract empty); christhouse_ar_2025 (landing page; PDF has no text layer); christhouse_ar_2025_pdf (image-only PDF (12 chars of text)); ehdc_ar_2024 (landing page); ehdc_ar_2024_pdf (2024 annual report text has no funder list); cfh_ar_list (index page); thrive_impact_2024 (lists corporate volunteer groups, not funders); miriams_financials (index page); miriams_ar_fy25 (mkannualreport.org is JavaScript-rendered; no text retrieved); coh_ar_2025 (2025 annual report summary has no funder list); coh_impact_2024 (same list as coh_funders (parsed there)); chgw_home (home page); chgw_impact_fy24 (FY24 impact report text has no funder list); doorways_ar_2023 (landing page); doorways_ar_2023_issuu (issuu viewer; no document text); hormd_honor_roll (URL now serves the About Us page; no honor roll content); hormd_ar_2024 (PDF returns HTTP 404); hormd_ar_page (annual report page has no donor list); meyer_118m_28 (2020 list (outside 2024-2026); no Calvary or peers); meyer_635k_8 (2022 list (outside 2024-2026); no Calvary or peers); meyer_rapid (program description only; no grantee list); meyer_news (news index); abell_grantmaking (guidelines only; no gran
- in-kind evidence rows 17: MGAC=unclear; MGAC=in_kind; MGAC=in_kind; MGAC=cash; Health Equity Fund=cash; Health Equity Fund=cash; Health Equity Fund=cash; Health Equity Fund=cash; Capital One=unclear; Capital One=unclear; Capital One=cash; World Bank Community Connections Fund=cash; World Bank Community Connections Fund=cash; World Bank Community Connections Fund=cash; Frontier Co-op / Aura Cacia (Frontier Co-op Giving Fund)=in_kind; Frontier Co-op / Aura Cacia (Frontier Co-op Giving Fund)=unclear; MGAC; Capital One; World Bank Community Connections Fund=unclear

### 2026-10-10 14:07 — 30_fetch_xml: progress
- pass 1: 28,000/31,469 done in 4.9 min (94.6/s); 2,279 MB on disk for done files; ok 28,000, not_found 0, error 0

### 2026-10-10 14:07 — 44_web_peers_funders
- search hits 757; pages listed 72, with content 68
- by group (listed, fetched): peer 36/36, funder 27/27, inkind 9/9
- failed/empty: nuvaya_fin_reports (http:http_403; chars 0 -> tavily no_content); christhouse_ar_2025_pdf (ok); miriams_ar_fy25 (http:ok; chars 21 -> tavily no_content); hormd_ar_2024 (http:http_404; chars 0 -> tavily no_content); ik_hef_home (http:ok; chars 18 -> tavily no_content)
- this run: Tavily search 0, extract 1, HTTP GET 0, cache hits 170; cumulative (manifest): search 104/300, extract 10/200, HTTP 115

### 2026-10-10 14:07 — 44_web_peers_funders (searches only)
- hits 801
- this run: Tavily search 5, extract 0, HTTP GET 0, cache hits 90; cumulative (manifest): search 109/300, extract 10/200, HTTP 115

### 2026-10-10 14:08 — 44_web_peers_funders
- search hits 801; pages listed 74, with content 70
- by group (listed, fetched): peer 36/36, funder 29/29, inkind 9/9
- failed/empty: nuvaya_fin_reports (http:http_403; chars 0 -> tavily no_content); christhouse_ar_2025_pdf (ok); miriams_ar_fy25 (http:ok; chars 21 -> tavily no_content); hormd_ar_2024 (http:http_404; chars 0 -> tavily no_content); ik_hef_home (http:ok; chars 18 -> tavily no_content)
- this run: Tavily search 0, extract 0, HTTP GET 2, cache hits 176; cumulative (manifest): search 109/300, extract 10/200, HTTP 117

### 2026-10-10 14:10 — 43_web_calvary
- support page: 98 organizations (3 flagged in-kind); Phase 1 PDF had 98 (11 truncated). Names absent from the PDF parse: 11
- truncated names recovered: Morris, Mann -> Morris, Manning & Martin, LLP; Nelson Mulli -> Nelson Mullins; NFP Golden & -> NFP Golden & Cohen; Robert Charle -> Robert Charles Lesser Co.; Sapodilla's C -> Sapodilla's Caribbean Restaurant and Catering; Saul Ewing A -> Saul Ewing Arnstein & Lehr LLP; Southern Com -> Southern Company; The Brand Gu -> The Brand Guild; The Menkiti G -> The Menkiti Group; United Bank -> United Bank; Women's Ene -> Women's Energy Resource Council
- PDFs seen: 98 (financials page links + WP media library + off-site search); kept as new: 22: 2015-07-Corporate-Partner-Program-packet.pdf [funder_list, ok]; CWS-Audited-Financial-Statements-2014.pdf [audit, ok]; CWS-Form-990-2014.pdf [form_990, ok]; CWS-form-990-2013.pdf [form_990, ok]; Corporate-Partners-Program-packet.pdf [funder_list, ok]; Corporate-Partners-Program-packet_11-11-2014.pdf [funder_list, ok]; Corporate-Partners-Program-packet_11-13-2014.pdf [funder_list, ok]; FY2013-Annual-Report-simple-version-FINAL.pdf [annual_report, ok]; What-Do-Corporate-Partners-Do_combined.pdf [funder_list, ok]; audited-statements-2013.pdf [audit, ok]; Calvary-Womens-Services-2014-Annual-Report.pdf [annual_report, ok]; 2017-Hope-Awards-Sponsorship-Opportunities.pdf [funder_list, ok]; Step-Up-DC-2016-Year-End-Report.pdf [funder_list, ok]; 2019-02-04-Calvary-Annual-Design.pdf [annual_report, ok]; Calvary-Womens-Services-FY18-Annual-Report.pdf [annual_report, ok]; CWS-Corporate-Partners-Program-Overview.pdf [funder_list, ok]; Hope-Awards-Sponsors.pdf [funder_list, ok]; 2024-Corporate-Partners-Program-Opportunities_CWS.pdf [funder_list, ok]; 2025-Hope-Gala-Sponsorship_CWS-2.pdf [funder_list, ok]; 2025-Hope-Gala-Sponsorship_CWS-2.pdf [funder_list, duplicate_of_web:https://www.calvaryservices.org/wp-content/uploads/2025/02/2025-Hope-Gala-Sponsorship_CWS-2.pdf]; Calvary-Newsletter-02_25.pdf [funder_list, ok]; 521307706_2022_25813620221_A133.pdf [other, ok; found by cal_audit_fy24]
- off-site search hits: 104 results; Calvary PDFs kept: 1; rejected: Calvary-Independent-Auditors-Report.pdf (cal_audit_fy25: not a Calvary Women's Services document)
- annual-report donors: 72 org rows; named lists/mentions 93 rows; individual band-count rows 3; Calvary-Womens-Services-2014-Annual-Report.pdf: 72 org donor entries, 182 individual entries (counted only); 2017-Hope-Awards-Sponsorship-Opportunities.pdf [Hope Awards Dinner: companies that have sponsored (cumulative)]: 40; Step-Up-DC-2016-Year-End-Report.pdf [Step Up DC supporters ('supported the program this year')]: 4; 2025-Hope-Gala-Sponsorship_CWS-2.pdf [Hope Gala: Past Event Sponsors (cumulative)]: 39
- new audits: 314 financial/note rows, 4 SEFA rows; CWS-Audited-Financial-Statements-2014.pdf: no SEFA in the PDF; 521307706_2022_25813620221_A133.pdf: SEFA p29 4 programs sum 4,067,718 vs printed total 4,067,718
- this run: Tavily search 0, extract 0, HTTP GET 0, cache hits 55; cumulative (manifest): search 109/300, extract 10/200, HTTP 117

### 2026-10-10 14:10 — 30_fetch_xml: progress
- pass 1: 30,000/31,469 done in 7.6 min (65.9/s); 2,528 MB on disk for done files; ok 30,000, not_found 0, error 0

### 2026-10-10 14:10 — 44_web_peers_funders
- search hits 801; pages listed 74, with content 70
- by group (listed, fetched): peer 36/36, funder 29/29, inkind 9/9
- failed/empty: nuvaya_fin_reports (http:http_403; chars 0 -> tavily no_content); christhouse_ar_2025_pdf (ok); miriams_ar_fy25 (http:ok; chars 21 -> tavily no_content); hormd_ar_2024 (http:http_404; chars 0 -> tavily no_content); ik_hef_home (http:ok; chars 18 -> tavily no_content)
- this run: Tavily search 0, extract 0, HTTP GET 0, cache hits 178; cumulative (manifest): search 109/300, extract 10/200, HTTP 117

### 2026-10-10 14:10 — 45_stage_web_grants
- staged rows 1015: by source_type {'support_page': 249, 'annual_report': 630, 'web': 136}; confidence {'medium': 988, 'high': 27}
- amount stated 34; band only 392; unknown 589
- recipient Calvary 268; core peers 739 (14 peers); whole-list keyword keeps 8
- Calvary-site rows by type {'support_page': 98, 'annual_report': 74, 'anonymous_skipped': 1, 'web': 90}
- pages parsed 20/65; not parsed or failed: nsv_funding_reports (index page (links to annual reports)); openarms_about (no funder list on the site); nebw_reports (index page (links to annual reports)); nebw_ar_2025 (2025 annual report text has no funder list); msp_ar_fy22 (no funder list); dcsafe_ar_fy25 (no funder list (revenue split only)); nuvaya_fin_reports (HTTP 403 and Tavily extract empty); christhouse_ar_2025 (landing page; PDF has no text layer); christhouse_ar_2025_pdf (image-only PDF (12 chars of text)); ehdc_ar_2024 (landing page); ehdc_ar_2024_pdf (2024 annual report text has no funder list); cfh_ar_list (index page); thrive_impact_2024 (lists corporate volunteer groups, not funders); miriams_financials (index page); miriams_ar_fy25 (mkannualreport.org is JavaScript-rendered; no text retrieved); coh_ar_2025 (2025 annual report summary has no funder list); coh_impact_2024 (same list as coh_funders (parsed there)); chgw_home (home page); chgw_impact_fy24 (FY24 impact report text has no funder list); doorways_ar_2023 (landing page); doorways_ar_2023_issuu (issuu viewer; no document text); hormd_honor_roll (URL now serves the About Us page; no honor roll content); hormd_honor_roll_tav (Tavily advanced extract also returns no honor roll content); hormd_ar_2024 (PDF returns HTTP 404); hormd_ar_page (annual report page has no donor list); meyer_118m_28 (2020 list (outside 2024-2026); no Calvary or peers); meyer_635k_8 (2022 list (outside 2024-2026); no Calvary or peers); meyer_rapid (program description only; no 
- in-kind evidence rows 17: MGAC=unclear; MGAC=in_kind; MGAC=in_kind; MGAC=cash; Health Equity Fund=cash; Health Equity Fund=cash; Health Equity Fund=cash; Health Equity Fund=cash; Capital One=unclear; Capital One=unclear; Capital One=cash; World Bank Community Connections Fund=cash; World Bank Community Connections Fund=cash; World Bank Community Connections Fund=cash; Frontier Co-op / Aura Cacia (Frontier Co-op Giving Fund)=in_kind; Frontier Co-op / Aura Cacia (Frontier Co-op Giving Fund)=unclear; MGAC; Capital One; World Bank Community Connections Fund=unclear
- Tavily usage to date (manifest, scripts 43-44): search 109/300, extract 10/200; plus 1 exploratory search during development (same query as cal_audit_fy24; response not saved). HTTP GETs 117.
- appended notes_for_analysis.md 'Web funder data' and open_questions.md

### 2026-10-10 14:11 — 60_stage_inputs
- stage_fact_org_financials__inputs.csv: 17 rows
- stage_fact_gov_awards__inputs.csv: 8 rows
- stage_fact_grants__inputs.csv: 360 rows
- stage_fact_roles__inputs.csv: 195 rows

### 2026-10-10 14:13 — 30_fetch_xml: done
- returns 31,469; ok 31,469; not_found 0; error 0
- by source (ok): {'gt_s3': 24013, 'irs': 7456}; downloaded this run 9,261 (869 MB), reused cache 22,208
- total XML bytes in manifest 2,632 MB; elapsed 11.3 min
- manifest -> interim/xml_manifest.csv

### 2026-10-10 14:14 — 50_parse_xml: progress
- 2,000/31,469 parsed in 0.7 min; grants 698,214, roles 22,703, relationships 5,719; errors 0

### 2026-10-10 14:14 — 50_parse_xml: progress
- 4,000/31,469 parsed in 0.7 min; grants 764,445, roles 41,090, relationships 9,843; errors 0

### 2026-10-10 14:14 — 50_parse_xml: progress
- 6,000/31,469 parsed in 0.8 min; grants 805,222, roles 56,702, relationships 10,893; errors 0

### 2026-10-10 14:14 — 50_parse_xml: progress
- 8,000/31,469 parsed in 0.8 min; grants 833,603, roles 71,376, relationships 11,565; errors 0

### 2026-10-10 14:14 — 50_parse_xml: progress
- 10,000/31,469 parsed in 0.8 min; grants 855,988, roles 83,493, relationships 11,952; errors 0

### 2026-10-10 14:14 — 50_parse_xml: progress
- 12,000/31,469 parsed in 0.9 min; grants 872,794, roles 94,219, relationships 12,296; errors 0

### 2026-10-10 14:14 — 50_parse_xml: progress
- 14,000/31,469 parsed in 0.9 min; grants 885,862, roles 103,874, relationships 12,521; errors 0

### 2026-10-10 14:14 — 50_parse_xml: progress
- 16,000/31,469 parsed in 0.9 min; grants 896,954, roles 112,601, relationships 12,652; errors 0

### 2026-10-10 14:14 — 50_parse_xml: progress
- 18,000/31,469 parsed in 1.0 min; grants 906,218, roles 120,561, relationships 12,779; errors 0

### 2026-10-10 14:15 — 50_parse_xml: progress
- 20,000/31,469 parsed in 1.0 min; grants 913,765, roles 128,040, relationships 12,842; errors 0

### 2026-10-10 14:15 — 50_parse_xml: progress
- 22,000/31,469 parsed in 1.0 min; grants 919,344, roles 134,952, relationships 12,846; errors 0

### 2026-10-10 14:15 — 50_parse_xml: progress
- 24,000/31,469 parsed in 1.0 min; grants 923,233, roles 141,341, relationships 12,848; errors 0

### 2026-10-10 14:15 — 50_parse_xml: progress
- 26,000/31,469 parsed in 1.1 min; grants 925,322, roles 147,812, relationships 12,848; errors 0

### 2026-10-10 14:15 — 50_parse_xml: progress
- 28,000/31,469 parsed in 1.1 min; grants 926,458, roles 154,256, relationships 12,848; errors 0

### 2026-10-10 14:15 — 50_parse_xml: progress
- 30,000/31,469 parsed in 1.1 min; grants 926,803, roles 160,435, relationships 12,848; errors 0

### 2026-10-10 14:15 — 50_parse_xml: done
- parsed 31,469 of 31,469 returns in 1.1 min; errors 0 -> xml_parse_errors.csv
- interim/stage_fact_org_financials__xml.csv: 31,469 rows {'990PF': 24877, '990': 4858, '990EZ': 1734}; amended 335; EIN differs from index 0
- interim/stage_fact_grants__xml.csv: 926,850 rows
- interim/stage_fact_roles__xml.csv: 163,595 rows
- interim/stage_fact_org_relationships__xml.csv: 12,848 rows
- interim/org_profile__xml.csv: 31,469 rows (6,772 EINs; street kept on latest return only)
- interim/xml_schedule_i_part3.csv: 1,717 Schedule I Part III lines (aggregates, no names)
- schema versions: {'2014v6.0': 1, '2015v3.0': 1, '2016v3.0': 1, '2017v2.3': 1, '2018v3.1': 1, '2019v5.2': 1, '2020v4.0': 1671, '2020v4.1': 2869, '2020v4.2': 423, '2021v4.0': 1467, '2021v4.1': 767, '2021v4.2': 3217, '2022v4.0': 4, '2022v4.1': 248, '2022v5.0': 5524, '2023v4.0': 271, '2023v5.0': 2462, '2023v5.1': 2420, '2023v6.0': 959, '2024v5.0': 1374, '2024v5.1': 1978, '2024v5.2': 2494, '2024v5.5': 372, '2025v4.0': 1220, '2025v4.1': 1441, '2025v4.2': 282}
- DAF1 sponsors, Schedule I kept only for DC/MD/VA recipients (all years in scope):
  - FIDELITY INVESTMENTS CHARITABLE GIFT FUND (110303001): national 372,180 rows / $58,823.5M; kept DMV 24,496 / $8,007.2M; filtered out $50,816.2M
  - NATIONAL PHILANTHROPIC TRUST (237825575): national 83,803 rows / $26,775.7M; kept DMV 6,855 / $3,393.6M; filtered out $23,382.1M
  - DONOR ADVISED CHARITABLE GIVING INC (311640316): national 119,989 rows / $14,989.8M; kept DMV 8,114 / $1,995.9M; filtered out $12,993.8M
  - SCHWAB CHARITABLE FUND (311640316): national 137,543 rows / $13,053.5M; kept DMV 9,339 / $2,005.8M; filtered out $11,047.7M
  - AMERICAN ONLINE GIVING FOUNDATION INC (810739440): national 228,879 rows / $10,079.9M; kept DMV 15,079 / $1,159.3M; filtered out $8,920.6M
  - VANGUARD CHARITABLE ENDOWMENT PROGRAM (232888152): national 72,758 rows / $8,460.4M; kept DMV 6,036 / $1,528.2M; filtered out $6,932.1M
  - AMERICAN ENDOWMENT FOUNDATION (341747398): national 65,226 rows / $4,638.5M; kept DMV 5,501 / $441.8M; filtered out $4,196.7M
  - Vanguard Charitable Endowment Program (232888152): national 41,050 rows / $3,616.6M; kept DMV 3,435 / $494.2M; filtered out $3,122.4M
  - BANK OF AMERICA CHARITABLE GIFT FD (046010342): national 3 rows / $2,538.9M; kept DMV 0 / $0.0M; filtered out $2,538.9M
  - THE AYCO CHARITABLE FOUNDATION (141782466): national 21,612 rows / $2,375.6M; kept DMV 1,874 / $113.0M; filtered out $2,262.5M
  - Renaissance Charitable Foundation Inc (352129262): national 4 rows / $2,054.0M; kept DMV 0 / $0.0M; filtered out $2,054.0M
  - CHARITIES AID FOUNDATION AMERICA (431634280): national 44,986 rows / $1,870.2M; kept DMV 3,095 / $204.6M; filtered out $1,665.5M
  - THE BLACKBAUD GIVING FUND (460942102): national 35,201 rows / $1,351.7M; kept DMV 2,007 / $135.2M; filtered out $1,216.5M
  - PAYPAL Charitable Giving Fund (450931286): national 32,699 rows / $1,188.6M; kept DMV 2,783 / $95.5M; filtered out $1,093.1M
  - THE GOLDMAN SACHS CHARITABLE GIFT FUND (113813663): national 12,471 rows / $1,056.1M; kept DMV 1,077 / $131.3M; filtered out $924.9M
  - BNY MELLON CHARITABLE GIFT FUND C/O BNY MELLON NA (300748315): national 5,467 rows / $1,022.5M; kept DMV 466 / $17.6M; filtered out $1,004.9M
  - BANK OF AMERICA CHARITABLE GIFT FUND (046010342): national 1 rows / $710.3M; kept DMV 0 / $0.0M; filtered out $710.3M
  - PAYPAL CHARITABLE GIVING FUND (450931286): national 14,871 rows / $708.8M; kept DMV 1,081 / $50.3M; filtered out $658.5M
  - The US Charitable Gift Trust co Eaton Vance Trust Company (311663020): national 3 rows / $477.2M; kept DMV 0 / $0.0M; filtered out $477.2M
  - THE US CHARITABLE GIFT TRUST (311663020): national 12,030 rows / $406.8M; kept DMV 984 / $29.0M; filtered out $377.8M
  - RENAISSANCE CHARITABLE FOUNDATION INC (352129262): national 1 rows / $234.1M; kept DMV 0 / $0.0M; filtered out $234.1M
  - Schwab Charitable Fund (311640316): national 0 rows / $0.0M; kept DMV 0 / $0.0M; filtered out $0.0M

### 2026-10-10 14:15 — 51_qc_xml
- fetch 100.00% of 31,469
- parse errors 0
- PF grants exact 100.0% (with grants), 99.8% all PF
- Calvary revenue checks pass
- Cafritz EIN 137049873; TY2024 to Calvary $0
- Calvary grant rows 150 from 50 funders ($4,701,886)
- trace 20/20
- report -> interim/xml_qc.md

### 2026-10-10 14:18 — 50_parse_xml: progress
- 2,000/31,469 parsed in 0.7 min; grants 698,214, roles 22,703, relationships 5,719; errors 0

### 2026-10-10 14:18 — 50_parse_xml: progress
- 4,000/31,469 parsed in 0.8 min; grants 764,445, roles 41,090, relationships 9,843; errors 0

### 2026-10-10 14:18 — 50_parse_xml: progress
- 6,000/31,469 parsed in 0.8 min; grants 805,222, roles 56,702, relationships 10,893; errors 0

### 2026-10-10 14:18 — 50_parse_xml: progress
- 8,000/31,469 parsed in 0.9 min; grants 833,603, roles 71,376, relationships 11,565; errors 0

### 2026-10-10 14:18 — 50_parse_xml: progress
- 10,000/31,469 parsed in 0.9 min; grants 855,988, roles 83,493, relationships 11,952; errors 0

### 2026-10-10 14:18 — 50_parse_xml: progress
- 12,000/31,469 parsed in 0.9 min; grants 872,794, roles 94,219, relationships 12,296; errors 0

### 2026-10-10 14:18 — 50_parse_xml: progress
- 14,000/31,469 parsed in 1.0 min; grants 885,837, roles 103,877, relationships 12,521; errors 0

### 2026-10-10 14:18 — 50_parse_xml: progress
- 16,000/31,469 parsed in 1.0 min; grants 896,942, roles 112,605, relationships 12,652; errors 0

### 2026-10-10 14:18 — 50_parse_xml: progress
- 18,000/31,469 parsed in 1.0 min; grants 906,218, roles 120,561, relationships 12,779; errors 0

### 2026-10-10 14:18 — 50_parse_xml: progress
- 20,000/31,469 parsed in 1.1 min; grants 913,765, roles 128,040, relationships 12,842; errors 0

### 2026-10-10 14:18 — 50_parse_xml: progress
- 22,000/31,469 parsed in 1.1 min; grants 919,344, roles 134,952, relationships 12,846; errors 0

### 2026-10-10 14:18 — 50_parse_xml: progress
- 24,000/31,469 parsed in 1.1 min; grants 923,233, roles 141,341, relationships 12,848; errors 0

### 2026-10-10 14:18 — 50_parse_xml: progress
- 26,000/31,469 parsed in 1.1 min; grants 925,327, roles 147,810, relationships 12,848; errors 0

### 2026-10-10 14:18 — 50_parse_xml: progress
- 28,000/31,469 parsed in 1.2 min; grants 926,458, roles 154,245, relationships 12,848; errors 0

### 2026-10-10 14:18 — 50_parse_xml: progress
- 30,000/31,469 parsed in 1.2 min; grants 926,803, roles 160,435, relationships 12,848; errors 0

### 2026-10-10 14:18 — 50_parse_xml: done
- parsed 31,469 of 31,469 returns in 1.2 min; errors 0 -> xml_parse_errors.csv
- interim/stage_fact_org_financials__xml.csv: 31,469 rows {'990PF': 24877, '990': 4858, '990EZ': 1734}; amended 335; EIN differs from index 0
- interim/stage_fact_grants__xml.csv: 926,850 rows
- interim/stage_fact_roles__xml.csv: 163,595 rows
- interim/stage_fact_org_relationships__xml.csv: 12,848 rows
- interim/org_profile__xml.csv: 31,469 rows (6,772 EINs; street kept on latest return only)
- interim/xml_schedule_i_part3.csv: 1,717 Schedule I Part III lines (aggregates, no names)
- schema versions: {'2014v6.0': 1, '2015v3.0': 1, '2016v3.0': 1, '2017v2.3': 1, '2018v3.1': 1, '2019v5.2': 1, '2020v4.0': 1671, '2020v4.1': 2869, '2020v4.2': 423, '2021v4.0': 1467, '2021v4.1': 767, '2021v4.2': 3217, '2022v4.0': 4, '2022v4.1': 248, '2022v5.0': 5524, '2023v4.0': 271, '2023v5.0': 2462, '2023v5.1': 2420, '2023v6.0': 959, '2024v5.0': 1374, '2024v5.1': 1978, '2024v5.2': 2494, '2024v5.5': 372, '2025v4.0': 1220, '2025v4.1': 1441, '2025v4.2': 282}
- DAF1 sponsors, Schedule I kept only for DC/MD/VA recipients (all years in scope):
  - FIDELITY INVESTMENTS CHARITABLE GIFT FUND (110303001): national 372,180 rows / $58,823.5M; kept DMV 24,496 / $8,007.2M; filtered out $50,816.2M
  - DONOR ADVISED CHARITABLE GIVING INC (311640316): national 257,532 rows / $28,043.2M; kept DMV 17,453 / $4,001.7M; filtered out $24,041.5M
  - NATIONAL PHILANTHROPIC TRUST (237825575): national 83,803 rows / $26,775.7M; kept DMV 6,855 / $3,393.6M; filtered out $23,382.1M
  - VANGUARD CHARITABLE ENDOWMENT PROGRAM (232888152): national 113,808 rows / $12,077.0M; kept DMV 9,471 / $2,022.5M; filtered out $10,054.5M
  - AMERICAN ONLINE GIVING FOUNDATION INC (810739440): national 228,879 rows / $10,079.9M; kept DMV 15,079 / $1,159.3M; filtered out $8,920.6M
  - AMERICAN ENDOWMENT FOUNDATION (341747398): national 65,226 rows / $4,638.5M; kept DMV 5,501 / $441.8M; filtered out $4,196.7M
  - BANK OF AMERICA CHARITABLE GIFT FD (046010342): national 4 rows / $3,249.2M; kept DMV 0 / $0.0M; filtered out $3,249.2M
  - THE AYCO CHARITABLE FOUNDATION (141782466): national 21,612 rows / $2,375.6M; kept DMV 1,874 / $113.0M; filtered out $2,262.5M
  - Renaissance Charitable Foundation Inc (352129262): national 5 rows / $2,288.2M; kept DMV 0 / $0.0M; filtered out $2,288.2M
  - PAYPAL CHARITABLE GIVING FUND (450931286): national 47,570 rows / $1,897.4M; kept DMV 3,864 / $145.8M; filtered out $1,751.5M
  - CHARITIES AID FOUNDATION AMERICA (431634280): national 44,986 rows / $1,870.2M; kept DMV 3,095 / $204.6M; filtered out $1,665.5M
  - THE BLACKBAUD GIVING FUND (460942102): national 35,201 rows / $1,351.7M; kept DMV 2,007 / $135.2M; filtered out $1,216.5M
  - THE GOLDMAN SACHS CHARITABLE GIFT FUND (113813663): national 12,471 rows / $1,056.1M; kept DMV 1,077 / $131.3M; filtered out $924.9M
  - BNY MELLON CHARITABLE GIFT FUND C/O BNY MELLON NA (300748315): national 5,467 rows / $1,022.5M; kept DMV 466 / $17.6M; filtered out $1,004.9M
  - THE US CHARITABLE GIFT TRUST (311663020): national 12,033 rows / $883.9M; kept DMV 984 / $29.0M; filtered out $854.9M

### 2026-10-10 14:18 — 51_qc_xml
- fetch 100.00% of 31,469
- parse errors 0
- PF grants sum exact 99.96% of returns with grants (99.81% of all PF); named-grantee rows cover 93.8% of PF grant dollars
- Calvary revenue checks pass
- Cafritz EIN 526036989; TY2024 to Calvary $170,000
- Calvary grant rows 150 from 50 funders ($4,701,886)
- trace 20/20
- report -> interim/xml_qc.md

### 2026-10-10 14:19 — 51_qc_xml
- fetch 100.00% of 31,469
- parse errors 0
- PF grants sum exact 99.96% of returns with grants (99.81% of all PF); named-grantee rows cover 93.8% of PF grant dollars
- Calvary revenue checks pass
- Cafritz EIN 526036989; TY2024 to Calvary $170,000
- Calvary grant rows 150 from 50 funders ($4,701,886)
- trace 20/20
- report -> interim/xml_qc.md

### 2026-10-10 14:20 — 38_parse_hud_counts
- wrote interim/stage_homeless_counts__hud.csv: 49,393 rows ({'bulk_hud_ahar_pit_hic': 48224, 'doc_hud_hic_dc500': 428, 'doc_mwcog_pit': 741}); PIT 39,029, HIC by CoC 9,195, PopSub 428, MWCOG 741
- wrote interim/stage_hic_projects__hud.csv: 1,257 rows (2022: 332, 2023: 292, 2024: 323, 2025: 310)
- HIC project PDFs: provider and facility names are truncated in the PDF itself (fixed-width report cells; same text in pdfplumber chars, pypdf and pdftotext); kept as printed. 'units' = family units (HIC reports units only for households with children). target_population is derived from the bed columns (household type, plus youth/veterans/chronic when all beds are dedicated) and set to single_women / women_with_children only when the provider or project name says women (basis in x_target_population_basis). x_women_focused_org = core peer tier 1a or Calvary; x_dv_focused_org = tier 1b (config/core_peers.csv).
- PIT by CoC (raw/hud/20261010T123731_huduser_2007-2025-PIT-Counts-by-CoC.xlsb): sheets 2007-2025; 39,029 rows for 8 CoCs; unparsed column names 216 (e.g. ['Overall Homeless - Under 18', 'Overall Homeless - Age 18 to 24', 'Overall Homeless - Over 24']); CoC-years absent: none
- partial unsheltered counts (Count Types): MD-601 2021; VA-602 2021
- workbook has no gender columns in any year (only age, race/ethnicity, household and subpopulation splits); DC gender comes from PopSub 2024 and the MWCOG 2025 DC narrative
- HIC by CoC (raw/hud/20261010T123733_huduser_2007-2025-HIC-Counts-by-CoC.xlsx): sheets 2007-2025; 9,195 rows; unparsed columns 9 (['HMIS Participation Rate (ES,TH) (non-numeric)', 'ES HMIS Participation Rate (non-numeric)', 'Total TH Beds for Households with only Children (non-numeric)', 'HMIS Participation Rate for Year-Round Beds (SH) (non-numeric)']); same-measure columns with different values kept as '__alt': 0
- PopSub DC-500 2024 (raw/hud/20261010T123749_hudx_CoC_PopSub_DC-500_2024.pdf): 232 rows; total persons 5616; women 2167
- PopSub DC-500 2025 (raw/hud/20261010T123750_hudx_CoC_PopSub_DC-500_2025.pdf): 196 rows; total persons 5138; women n/a
- MWCOG 2023 report (raw/hud/20261010T123754_mwcog_homelessness_metro_washington_2023_PIT.pdf): 548 table cells kept
- MWCOG 2024 report (raw/hud/20261010T123753_mwcog_homelessness_metro_washington_2024_PIT.pdf): 504 table cells kept
- MWCOG 2025 report (raw/hud/20261010T123752_mwcog_homelessness_metro_washington_2025_PIT.pdf): 520 table cells kept
- MWCOG 2026 report (raw/hud/20261010T123751_mwcog_homelessness_metro_washington_2026_PIT.pdf): 531 table cells kept
- MWCOG: 2103 cells parsed across reports -> 741 after keeping the latest report per jurisdiction/year/measure/population; values revised between reports: 38 (e.g. Prince William County, VA 2022 all: 241 (rpt 2023) -> 282 (rpt 2024); Prince William County, VA 2021 all: 282 (rpt 2023) -> 326 (rpt 2024); Prince William County, VA 2020 all: 326 (rpt 2023) -> 277 (rpt 2024); COG region 2023 households_without_children: 5901 (rpt 2023) -> 5755 (rpt 2024)); same report, two tables disagree (earlier page kept): 17 (District of Columbia 2020 households_with_only_children rpt 2023: p68 12 vs p25 11; Frederick City & County, MD 2021 households_with_only_children rpt 2023: p68 5 vs p25 0; COG region 2020 households_with_only_children rpt 2023: p69 13 vs p25 12; City of Alexandria, VA 2020 all rpt 2023: p68 198 vs p17 207)
- skipped tables (did not parse reliably): none; source-inconsistent columns are kept with confidence medium and an x_note
- not parsed: figures/charts (demographic profiles, income, gender charts), Table 3 population shares, Table 13/14 shelter status, TAY tables, Table 16 bed inventory, Table 17 formerly homeless in PH, Appendix B narrative percentages except the 2025 DC gender-of-adults table
- HIC provider names (cleaned, distinct): 105; matched 42 (40%); methods {'unmatched': 63, 'fuzzy_token_set': 10, 'exact_norm_name': 29, 'manual_known_ein': 2, 'manual_alias': 1}; government providers (no EIN expected) 7; beds at matched providers 67,567 of 133,181 (51%)
- fuzzy matches: Access Housing -> 521918702 (100.0); Access Housing INC (AHI) (Agency) -> 521918702 (100.0); Catholic Charities -> 530196524 (100.0); Catholic Charities (Agency) -> 530196524 (100.0); Covenant House Washington -> 133537709 (100.0); Covenant House Washington (CHW)(Age -> 133537709 (100.0); East River Family Strengthening Collabor -> 522277915 (100.0); Edgewood-Brookland Family Support Col -> 522246995 (100.0); Edgewood/Brookland Family Support Col -> 522246995 (100.0); Far Southeast Family Strengthening Colla -> 522117070 (100.0); Georgia Avenue Family Support Collabor -> 522349433 (100.0); Survivors & Advocates for Empowerment -> 412226446 (100.0)
- unmatched nonprofit providers (not in dc_sector/dmv_sector/core_peers by name): 801 East Collaborative; Bradley & Associates; CCDC; CORE DC; Casa Ruby; Church of Epiphany; Church of the Epiphany; Collaborative Solutions for Communities; Communities Helping & Empowering Pat; Communities Helping and Empowering P; Community Solutions; Cornerstone Community; Dawn Deaf; Deaf Dawn; East of the River Family Support Collabor; Echelon Community Services; Far Southeast Family Support Collaborati; Healthy Babies; Healthy Babies Project; Hillcrest Children & Family Center; Hope and a Home; Institute for Emotional Regulation; Jaydot; Joseph's House; Jubilee Housing; KBEC Group, Inc; KBEC Group, Inc.; KC Community Services; Latin American Youth Center; MBI Health Services; Maximus; Metropolitan Education Solutions; Metropolitan Educational Solutions; North Capitol Collaborative Inc.; North Capitol Family Support Collaborati; Operation Renewed Hope; Positive Kinship Bonding; SLS; SMYAL; Salvation Army; Sasha Bruce Youthwork; Sasha Bruce Youthworks; So Others Might Eat; Spring Leaf; St. Aloysius Roman Catholic Church; St. John's Community Community Servic; St. John's Community Services; Supporting & Mentoring Youth Advocate; Temple Micah; Temple Sinai; The Community Builders and Emory Bea; The Institute for Emotional Regulation, L; The Salvation Army; U.S. Vets; US Veterans Initiative; Wheeler Creek
- matcher (shared with script 36): manual aliases (TCP 521681401; DASH, DC SAFE, Housing Up), norm_name exact, then rapidfuzz token_set_ratio >= 92 (after expanding a truncated last token for raw names >= 30 chars) accepted only when fuzzy_ok() holds: both names >= 2 tokens, a shared non-generic token, no one-sided entity-marker token (foundation, fund, maryland, county, ...), and token containment (ratio >= 0.5) or prefix or only soft one-sided words or fuzz.ratio >= 90; reviewed reject list
- PopSub 2024 gender rows sum 5616 vs total 5616: pass
- MWCOG 2023 p16 'People Experiencing Literal Homelessness by Jurisdiction, 2022 - 2023': pass (2 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p17 'People Experiencing Literal Homelessness by Jurisdiction, 2019-2023': pass (5 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p22 '2023 Persons In Families Experiencing Homelessness by Jurisdiction': pass (4 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p23 'Change In Persons In Families Experiencing Homelessness by Jurisdictio': pass (5 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p25 'Households With Only Children Under Age 18 By Jurisdiction, 2020 - 202': pass (4 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p41 'Comparison of Unsheltered Single Adults By Jurisdiction, 2019 – 2023': pass (5 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p45 'Single Adults Experiencing Chronic Homelessness by Jurisdiction, 2019 ': pass (5 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p51 'Veterans Experiencing Homelessness By Jurisdiction, 2019 - 2023': pass (5 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 pp[68, 69] 'People Experiencing Literal Homelessness by Jurisdiction, 20': kept with flags: 14/20 columns do not add up in the source (2022 households_without_children 5,307 vs 5,273; 2022 households_with_adults_and_children 2,329 vs 2,322; 2022 all 7,646 vs 7,605); 2 jurisdiction-years whose household columns do not add up
- MWCOG 2024 p16 'People Experiencing Literal Homelessness by Jurisdiction, 2023 - 2024': pass (2 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p17 'People Experiencing Literal Homelessness by Jurisdiction, 2020-2024*': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p22 '2024 Persons in Families Experiencing Homelessness by Jurisdiction': pass (4 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p23 'Change in Persons in Families Experiencing Homelessness by Jurisdictio': kept with flags: 1/5 columns do not add up in the source (2020 persons_in_families 3,690 vs 3,760)
- MWCOG 2024 p29 'Households With Only Children Under Age 18 By Jurisdiction, 2020 - 202': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p49 'Unsheltered Single Adults Experiencing Homelessness by Jurisdiction, 2': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p52 'Single Adults Experiencing Chronic Homelessness by Jurisdiction, 2020 ': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p60 'Veterans Experiencing Homelessness by Jurisdiction, 2020 - 2024': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 pp[75, 76] 'People Experiencing Literal Homelessness by Jurisdiction, 20': kept with flags: 9/20 columns do not add up in the source (2022 households_without_children 5,154 vs 5,120; 2022 households_with_adults_and_children 2,272 vs 2,265; 2022 all 7,422 vs 7,395); 2 jurisdiction-years whose household columns do not add up
- MWCOG 2025 p17 'People Experiencing Literal Homelessness by Jurisdiction, 2024 - 2025': pass (2 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p18 'People Experiencing Literal Homelessness by Jurisdiction, 2021-2025*': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p22 '2025 Persons in Families Experiencing Homelessness by Jurisdiction': pass (4 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p23 'Change in Persons in Families Experiencing Homelessness by Jurisdictio': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p29 'Households With Only Children Under Age 18 By Jurisdiction, 2021 - 202': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p48 'Comparison of Unsheltered Single Adults by Jurisdiction, 2021 - 2025': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p51 'Single Adults Experiencing Chronic Homelessness by Jurisdiction, 2021 ': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p59 'Veterans Experiencing Homelessness by Jurisdiction, 2021 - 2025': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 pp[73, 74] 'People Experiencing Literal Homelessness by Jurisdiction, 20': pass (20 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p18 'People Experiencing Literal Homelessness by Jurisdiction, 2025-2026': pass (2 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p19 'People Experiencing Literal Homelessness by Jurisdiction, 2019-2026': pass (8 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p24 '2026 Persons in Families Experiencing Homelessness by Jurisdiction': pass (4 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p25 'Change in Persons in Families Experiencing Homelessness by Jurisdictio': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p32 'Households With Only Children Under Age 18 By Jurisdiction, 2022 – 202': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p50 'Comparison of Unsheltered Single Adults by Jurisdiction, 2022 – 2026': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p54 'Single Adults Experiencing Chronic Homelessness by Jurisdiction, 2022 ': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p59 'Veterans Experiencing Homelessness by Jurisdiction, 2022 – 2026': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 pp[79, 80] 'People Experiencing Literal Homelessness by Jurisdiction, 20': pass (20 year/measure columns, 8 jurisdictions + total)
- MWCOG total persons vs HUD PIT overall, CoC-years that differ: 9: MD-600 2020: MWCOG 453 vs HUD 466; MD-600 2021: MWCOG 537 vs HUD 535; MD-600 2022: MWCOG 571 vs HUD 533; MD-600 2023: MWCOG 659 vs HUD 595; MD-600 2024: MWCOG 658 vs HUD 650; MD-600 2025: MWCOG 608 vs HUD 588; VA-602 2019: MWCOG 169 vs HUD 167; VA-604 2019: MWCOG 277 vs HUD 280; VA-604 2025: MWCOG 392 vs HUD 393
- DC-500 MWCOG vs HUD by year: 2019 6,521/6521, 2020 6,380/6380, 2021 5,111/5111, 2022 4,410/4410, 2023 4,922/4922, 2024 5,616/5616, 2025 5,138/5138, 2026 5,363/n/a
- stage_homeless_counts duplicate keys (coc, jurisdiction, year, measure, population, source): 0
- DC-500 2025 recon values: pit_overall 5138 (exp 5138) pass; pit_sheltered_es 3275 (exp 3275) pass; pit_sheltered_th 1065 (exp 1065) pass; pit_unsheltered 798 (exp 798) pass; hic_beds_year_round__es_th_sh 4965 (exp 4965) pass; hic_beds_year_round__th 1385 (exp 1385) pass; hic_beds_year_round__psh 12696 (exp 12696) pass; hic_beds_year_round__rrh 6012 (exp 6012) pass
- HIC projects 2022 ES: 43 projects; total beds 5,159 vs Total row 5159; year-round 4,795 vs summary p1 4795 vs CoC workbook 4795: pass
- HIC projects 2022 SH: 1 projects; total beds 20 vs Total row 20; year-round 20 vs summary p1 20 vs CoC workbook 20: pass
- HIC projects 2022 TH: 71 projects; total beds 1,783 vs Total row 1783; year-round 1,783 vs summary p1 1783 vs CoC workbook 1783: pass
- HIC projects 2022 PSH: 148 projects; total beds 14,467 vs Total row 14467; year-round 14,467 vs summary p1 14467 vs CoC workbook 14467: pass
- HIC projects 2022 RRH: 34 projects; total beds 7,193 vs Total row 7193; year-round 7,193 vs summary p1 7193 vs CoC workbook 7193: pass
- HIC projects 2022 OPH: 35 projects; total beds 6,498 vs Total row 6498; year-round 6,498 vs summary p1 6498 vs CoC workbook 6498: pass
- HIC projects 2023 ES: 38 projects; total beds 4,026 vs Total row 4026; year-round 3,720 vs summary p1 3720 vs CoC workbook 3720: pass
- HIC projects 2023 SH: 1 projects; total beds 20 vs Total row 20; year-round 20 vs summary p1 20 vs CoC workbook 20: pass
- HIC projects 2023 TH: 65 projects; total beds 1,476 vs Total row 1476; year-round 1,476 vs summary p1 1476 vs CoC workbook 1476: pass
- HIC projects 2023 PSH: 138 projects; total beds 15,349 vs Total row 15349; year-round 15,349 vs summary p1 15349 vs CoC workbook 15349: pass
- HIC projects 2023 RRH: 35 projects; total beds 9,206 vs Total row 9206; year-round 9,206 vs summary p1 9206 vs CoC workbook 9206: pass
- HIC projects 2023 OPH: 15 projects; total beds 5,381 vs Total row 5381; year-round 5,381 vs summary p1 5381 vs CoC workbook 5381: pass
- HIC projects 2024 ES: 46 projects; total beds 4,000 vs Total row 4000; year-round 3,505 vs summary p1 3505 vs CoC workbook 3505: pass
- HIC projects 2024 SH: 1 projects; total beds 20 vs Total row 20; year-round 20 vs summary p1 20 vs CoC workbook 20: pass
- HIC projects 2024 TH: 70 projects; total beds 1,693 vs Total row 1693; year-round 1,693 vs summary p1 1693 vs CoC workbook 1693: pass
- HIC projects 2024 PSH: 154 projects; total beds 11,856 vs Total row 11856; year-round 11,856 vs summary p1 11856 vs CoC workbook 11856: pass
- HIC projects 2024 RRH: 33 projects; total beds 10,156 vs Total row 10156; year-round 10,156 vs summary p1 10156 vs CoC workbook 10156: pass
- HIC projects 2024 OPH: 19 projects; total beds 5,842 vs Total row 5842; year-round 5,842 vs summary p1 5842 vs CoC workbook 5842: pass
- HIC projects 2025 ES: 45 projects; total beds 3,954 vs Total row 3954; year-round 3,580 vs summary p1 3580 vs CoC workbook 3580: pass
- HIC projects 2025 TH: 64 projects; total beds 1,385 vs Total row 1385; year-round 1,385 vs summary p1 1385 vs CoC workbook 1385: pass
- HIC projects 2025 PSH: 159 projects; total beds 12,696 vs Total row 12696; year-round 12,696 vs summary p1 12696 vs CoC workbook 12696: pass
- HIC projects 2025 RRH: 26 projects; total beds 6,012 vs Total row 6012; year-round 6,012 vs summary p1 6012 vs CoC workbook 6012: pass
- HIC projects 2025 OPH: 16 projects; total beds 4,989 vs Total row 4989; year-round 4,989 vs summary p1 4989 vs CoC workbook 4989: pass
- stage_hic_projects duplicate keys (year, type, page, seq): 0
- Calvary HIC 2025 rows pass (7 projects, 124 beds); 2024 Sisters Rise PSH [24] (exp [24])

### 2026-10-10 14:20 — 52_xml_notes
- appended 7 observations to notes_for_analysis.md (XML pulls) and 2 questions to open_questions.md

### 2026-10-10 14:22 — 33_pull_usaspending: downloads
- jobs 15 (206 in-scope UEIs in 11 chunks)
  - cfda_DC: count {'awards': 836, 'subawards': 892}; {"status": "finished", "total_rows": 1728, "seconds": 40, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H17M28S11_1.csv": 836, "Assistance_Subawards_2026-10-10_H17M28S20_1.csv": 892}}
  - cfda_MD: count {'awards': 2316, 'subawards': 3961}; {"status": "finished", "total_rows": 6277, "seconds": 53, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H17M28S13_1.csv": 2316, "Assistance_Subawards_2026-10-10_H17M28S30_1.csv": 3961}}
  - cfda_VA: count {'awards': 2370, 'subawards': 5869}; {"status": "finished", "total_rows": 8239, "seconds": 55, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H17M28S12_1.csv": 2370, "Assistance_Subawards_2026-10-10_H17M28S34_1.csv": 5869}}
  - calvary: count {'awards': 2, 'subawards': 1}; {"status": "finished", "total_rows": 3, "seconds": 67, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H17M28S09_1.csv": 2, "Assistance_Subawards_2026-10-10_H17M28S12_1.csv": 1}}
  - uei_b00: count {'awards': 275, 'subawards': 235}; {"status": "finished", "total_rows": 510, "seconds": 68, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H17M31S01_1.csv": 275, "Assistance_Subawards_2026-10-10_H17M31S06_1.csv": 235}}
  - uei_b01: count {'awards': 172, 'subawards': 30}; {"status": "finished", "total_rows": 202, "seconds": 69, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H17M31S04_1.csv": 172, "Assistance_Subawards_2026-10-10_H17M31S07_1.csv": 30}}
  - uei_b02: count {'awards': 184, 'subawards': 171}; {"status": "finished", "total_rows": 355, "seconds": 97, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H17M31S06_1.csv": 184, "Assistance_Subawards_2026-10-10_H17M31S09_1.csv": 171}}
  - uei_b03: count {'awards': 213, 'subawards': 140}; {"status": "finished", "total_rows": 353, "seconds": 105, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H17M31S08_1.csv": 213, "Assistance_Subawards_2026-10-10_H17M31S12_1.csv": 140}}
  - uei_b04: count {'awards': 245, 'subawards': 363}; {"status": "finished", "total_rows": 608, "seconds": 107, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H17M31S09_1.csv": 245, "Assistance_Subawards_2026-10-10_H17M31S15_1.csv": 363}}
  - uei_b05: count {'awards': 173, 'subawards': 232}; {"status": "request failed http None", "detail": null}
  - uei_b06: count {'awards': None, 'subawards': None}; {"status": "request failed http None", "detail": null}
  - uei_b07: count {'awards': None, 'subawards': None}; {"status": "request failed http None", "detail": null}
  - uei_b08: count {'awards': None, 'subawards': None}; {"status": "request failed http None", "detail": null}
  - uei_b09: count {'awards': None, 'subawards': None}; {"status": "request failed http None", "detail": null}
  - uei_b10: count {'awards': None, 'subawards': None}; {"status": "request failed http None", "detail": null}
- manifest raw/usaspending/20261010T142255_pull33_manifest.json

### 2026-10-10 14:24 — 61_resolve_entities
- unique name keys 234,983; alias rows 234,082
- occurrences by method:
match_method  exact_ein  exact_name_city  exact_name_national  exact_name_state  fuzzy_name_city  known_funder  manual  manual_reject  unmatched
role                                                                                                                                            
funder           924976                0                  135                 0                0           229      37             19       2829
pass_through        248                0                    0                 0                0             0       0              0         80
recipient        184877           341734                 1378             50989            27429             0      48              2     286316

### 2026-10-10 14:26 — 62_build_facts
- fact_org_financials: 148,983 rows
- fact_grants: 928,225 rows
- fact_gov_awards: 30,222 rows
- fact_opportunities: 286 rows
- fact_policy_events: 297 rows
- supp_calvary_individual_donor_bands.csv: copied from stage_supp_calvary_individual_donor_bands.csv
- supp_calvary_program_metrics.csv: copied from stage_supp_calvary_program_metrics.csv
- supp_calvary_strategic_targets.csv: copied from stage_supp_calvary_strategic_targets.csv
- supp_homeless_counts.csv: copied from stage_homeless_counts__hud.csv
- supp_hic_projects.csv: copied from stage_hic_projects__hud.csv
- supp_dc_budget_lines.csv: copied from stage_dc_budget_lines__dc.csv

### 2026-10-10 14:26 — 63_build_dims
- dim_org: 104,582 rows
- dim_funder: 8,652 rows
- dim_program_area: 13 rows
- dim_period: 28 rows
- dim_geo: 243 rows

### 2026-10-10 14:26 — 36_parse_dc_awards
- wrote interim/stage_fact_gov_awards__dc.csv: 12,085 rows; by source/section: dc_oversight/dv_grantees 53; dc_oversight/erap_arpa_grants 25; dc_oversight/homelessness_prevention 19; dc_oversight/psh_case_management 90; dc_oversight/singles_shelter_contract_periods 53; dc_oversight/singles_shelter_contracts 50; dc_oversight/singles_shelter_subgrants 6; dc_oversight/youth_dhs_direct_housing 65; dc_oversight/youth_dhs_direct_nonhousing 37; dc_oversight/youth_tcp_housing 44; dc_ovsjg/ovsjg_layer 1267; dc_ovsjg/ovsjg_pdf 118; dc_pass/pass_payments 5494; dc_pass/pass_po 4494; hud_coc/hud_coc 270
- decisions: OVSJG flow_type dc_local_grant unless the stated funding source is federal only (then subaward with OVSJG as pass-through); assistance_listing filled only from the stated funding source (VOCA 16.575, STOP VAWA 16.588, SASP 16.017, Byrne JAG 16.738, JJDP Title II 16.540, Title V 16.548, RSAT 16.593, Coverdell 16.742, ARPA -> SLFRF 21.027); DHS ERAP ARPA/ERA2 shares are subawards (21.027/21.023); HUD CoC rows: TCP-applicant projects -> recipient = sponsor in the project title, flow subaward, pass-through TCP; other applicants -> prime; fiscal_year = CoC competition year (federal_fy).
- OVSJG layer 35: 1267 rows FY2016-FY2025; AGENCY used as grantee, ORGANIZATIONNAME as project title (labels swapped); 6 rows flagged as identical repeats
- OVSJG FY2024 PDF p2: 'Metro DC Community Center Inc., The' amount from text layer: 327000
- OVSJG FY2024 PDF (raw/dc_gov/20261010T123646_ovsjg_funding_recipients_FY2024.pdf): 121 grant rows, total $62,935,024
- OVSJG FY2025 PDF (raw/dc_gov/20261010T123645_ovsjg_funding_recipients_FY2025.pdf): 120 grant rows, total $92,682,681
- OVSJG FY2026 PDF (raw/dc_gov/20261010T123645_ovsjg_funding_recipients_FY2026.pdf): 118 grant rows, total $96,653,604
- OVSJG merge: 241 FY2024/FY2025 layer rows enriched from the PDFs (funding source, period, issue date); 118 PDF rows added (118 FY2026); PDF rows without a layer match: 0 []; layer FY2024/25 rows without a PDF match: 0 []
- DHS oversight provider tables: 442 rows; by section {'erap_arpa_grants': 25, 'homelessness_prevention': 19, 'youth_dhs_direct_nonhousing': 37, 'youth_tcp_housing': 44, 'youth_dhs_direct_housing': 65, 'psh_case_management': 90, 'singles_shelter_contracts': 50, 'dv_grantees': 53, 'singles_shelter_contract_periods': 53, 'singles_shelter_subgrants': 6}; $0 cells skipped: 20
- HUD CoC DC-500: 270 project rows ({2019: 38, 2020: 39, 2021: 40, 2022: 43, 2023: 39, 2024: 36, 2025: 35}); flow {'prime': 66, 'subaward': 204}
- PASS: 18,655 distinct PO suppliers, 73,834 distinct payment suppliers; matched to universe/TCP EINs: 188 PO supplier strings (182 EINs), 258 payment supplier strings (196 EINs); PO methods {'exact_norm_name': 145, 'fuzzy_token_set': 42, 'manual_known_ein': 1}
- PASS fuzzy supplier matches (75): ACCESS HOUSING INC. -> ACCESS HOUSING INC DC (100); ACCESS HOUSING INC. (DC) -> ACCESS HOUSING INC DC (100); AFFORDABLE HOUSING OPPORTUNITI -> AFFORDABLE HOUSING OPPORTUNITIES INC (97); AMERICAN ASSOC OF RESIDENTIAL -> AMERICAN ASSOCIATION OF RESIDENTIAL MORTGAGE REGULATORS (100); AMERICAN SOCIETY OF ADDICTION -> AMERICAN SOCIETY OF ADDICTION MEDICINE INC (100); American Society of Addiction -> AMERICAN SOCIETY OF ADDICTION MEDICINE INC (100); BENNING PARK NEIGHBORHOOD CORP -> BENNING PARK NEIGHBORHOOD ASSOCIATI ON (100); BLACK FEM  INC -> BLACKFEM INC (94); BLACK FEM, INC -> BLACKFEM INC (94); BREASTFEEDING OUTREACH FOR GRE -> BREASTFEEDING OUTREACH FOR GREATER WASHINGTON (93); Breastfeeding Outreach for Gre -> BREASTFEEDING OUTREACH FOR GREATER WASHINGTON (93); CAPITOL HILL COUNSELING A -> CAPITOL HILL COUNSELING AND RESOURCE CENTER INC (100); CARE AND PROGRESS COMMUNITY DE -> CARE AND PROGRESS COMMUNITY DEVELOPMENT (94); CATHOLIC CHARITIES -> CATHOLIC CHARITIES OF THE ARCHDIOCESE OF WASHINGTON INC (100); CENTER FOR ADOPTION SUPPORT -> CENTER FOR ADOPTION SUPPORT AND EDUCATION INC (100); CHILDREN & CHARITY INTERNATION -> CHILDREN & CHARITY INTERNATIONAL (97); COALITION FOR THE HOMELESS, IN -> COALITION FOR THE HOMELESS INC (100); COMMUNITY BRIDGE INC -> COMMUNITY BRIDGES INCORPORATED (97); COMMUNITY CONNECTION -> COMMUNITY CONNECTIONS (98); COMMUNITY FAMILY LIFE SERVICE, -> COMMUNITY FAMILY LIFE SERVICES INC (98); COURTNEY S HOUSE INC -> COURTNEYS HOUSE INC (97); COVENANT HOUSE WASHINGTON -> COVENANT HOUSE WASHINGTON DC (100); Care and Progress Community De -> CARE AND PROGRESS COMMUNITY DEVELOPMENT (94); Catholic Charities of the Archdiocese of -> CATHOLIC CHARITIES OF THE ARCHDIOCESE OF WASHINGTON INC (100); DC ACTION FOR CHILDREN TODAY -> DC ACTION FOR CHILDREN TODAY DC ACT (100); DEAF ABUSED WOMEN'S NETWORK -> DEAF ABUSED WOMEN NETWORK (98); DEEDS OF KINDNESS OUTREACH -> DEEDS OF KINDNESS OUTREACH SERVICES (100); DISABLED VETERANS NATL FOUNDAT -> DISABLED VETERANS NATIONAL FOUNDATION (96); DISTRICT ALLIANCE SAFE HOUSING -> DISTRICT ALLIANCE FOR SAFE HOUSING INC (100); DOORS OF HOPE INC -> DOOR OF HOPE (95); Doors of Hope Inc -> DOOR OF HOPE (95); EXCELLENT COMMUNITY SERVI -> EXCELLENT COMMUNITY SERVICES INC (94); FAMILY MEDICAL COUNSELING -> FAMILY AND MEDICAL COUNSELING SERVICE INC (100); FAR SOUTHEAST FAMILY -> FAR SOUTHEAST FAMILY STRENGTHENING COLLABORATIVE (100); FOUR WALLS DEVELOPEMENT INC. -> FOUR WALLS DEVELOPMENT INC (98); FRY PLUMBING & HEATING -> FRY PLUMBING AND HEATING NON PROFIT (100); FRY PLUMBING AND HEATING -> FRY PLUMBING AND HEATING NON PROFIT (100); Fry Plumbing and Heating -> FRY PLUMBING AND HEATING NON PROFIT (100); HOUSING COUNSELING SERVICE -> HOUSING COUNSELING SERVICES INC (98); HOUSING COUNSELING SERVICES, I -> HOUSING COUNSELING SERVICES INC (100); KEY BRIDGE FOUNDATION -> KEY BRIDGE FOUNDATION FOR EDUCATION AND RESEARCH (100); LITTLE SISTERS OF THE POOR -> LITTLE SISTERS OF THE POOR OF WASHINGTON DC INC (100); LUTHERAN SOCIAL SERVICES -> LUTHERAN SOCIAL SERVICES OF THE NATIONAL CAPITAL AREA INC (100); LUTHERAN SOCIAL SERVICES NATL' -> LUTHERAN SOCIAL SERVICES OF THE NATIONAL CAPITAL AREA INC (100); MARTHA S TABLE INC -> MARTHAS TABLE (96); MARY ELIZABETH HOUSE, INC A MI -> THE MARY ELIZABETH HOUSE INC A MINISTRY (93); MISSION FIRST HOUSING DEVELOPM -> MISSION FIRST HOUSING DEVELOPMENT CORPORATION (95); MOUNT LEBANON COMMUNITY DEVELO -> MOUNT LEBANON COMMUNITY DEVELOPMENT CORPORATION (92); Mission First Housing Developm -> MISSION FIRST HOUSING DEVELOPMENT CORPORATION (95); NAT'L FEDERATION OF THE BLIND -> NATIONAL FEDERATION OF THE BLIND OF THE DISTRICT OF COLUMBIA (100); NATIONAL CENTER FOR CHILDREN A -> NATIONAL CENTER FOR CHILDREN AND FAMILIES (100); NATIONAL CENTER FOR VICTIMS OF -> NATIONAL CENTER FOR VICTIMS OF CRIME INC (100); NATIONAL ENERGY AND UTILITY AF -> THE NATIONAL ENERGY AND UTILITY AFFORDABILITY COALITION (94); NATIONAL FEDERATION OF THE BLIND -> NATIONAL FEDERATION OF THE BLIND OF THE DISTRICT OF COLUMBIA (100); NATIONAL FOUNDATION TO END SEN -> NATIONAL FOUNDATION TO END SENIOR HUNGER INC (93); NEIGHBOR S CONSEJO -> NEIGHBORS CONSEJO (97); NORTHERN VIRGINIA FAMILY -> NORTHERN VIRGINIA FAMILY SERVICES INC (100); National Association of State Mental Health Program Directors -> NATIONAL ASSOCIATION OF STATE MENTAL HEALTH PROGRAM DIRECTORS IN (100); National Center For Victims Of -> NATIONAL CENTER FOR VICTIMS OF CRIME INC (100); OMEGA GOLD DEVELOPMENT GR -> OMEGA GOLD DEVELOPMENT GROUP INC (94); PAVING THE WAY MULTI-SERVICE -> PAVING THE WAY MULTI SERVICE INSTITUTE (100); PSI SERVICE III INC -> PSI SERVICES III INC (97); RAPE, ABUSE, INCEST, NATIONAL -> RAPE ABUSE AND INCEST NATIONAL NETWORK INC (100); RESTORATION COMMUNITY ALLIANCE -> RESTORATION COMMUNITY ALLIANCE COMMUNITY DEVLEOPMENT CORPORATION (100); Rape, Abuse, Incest, National -> RAPE ABUSE AND INCEST NATIONAL NETWORK INC (100); SAMARITAN MINISTRY OF GREATER -> SAMARITAN MINISTRY OF GREATER WASHINGTON (100); SERVICE SOURCE, INC -> SERVICESOURCE INC (96); STEPPINGSTONE FOUNDATION, INC. -> STEPPING STONE FOUNDATION INC (98); SYMBRAL FOUNDATION FOR CMTY. -> SYMBRAL FOUNDATION FOR COMMUNITY SERVICES INC (100); Safe Routes to School National Partnersh -> SAFE ROUTES TO SCHOOL NATIONAL PARTNERSHIP (98); THE HOPE FOUNDATION RE-ENTRY -> HOPE FOUNDATION RE-ENTRY NETWORK INC (100); THE MARY ELIZABETH HOUSE -> THE MARY ELIZABETH HOUSE INC A MINISTRY (100); THE NATIONAL REENTRY NETWORK -> THE NATIONAL REENTRY NETWORK FOR RETURNING CITIZENS (100); Torture abolition and Survivors Support -> TORTURE ABOLITION AND SURVIVORS SUPPORT COALITION INTERNATIONAL (100); WASHINGTON REGIONAL ALCOHOL PR -> WASHINGTON REGIONAL ALCOHOL PROGRAM (95)
- PASS POs for universe vendors: 5,602 raw rows -> 4,494 after dedupe on PONUMBER + FISCALYEAR + POTOTAL (repeats removed: 1,108, almost all AA0 sub-office fan-out)
- PASS payments for universe vendors: 5,494 supplier x FY x agency x PO aggregates; FY2025+ rows flagged x_pass_incomplete_fy=1 (PASS incomplete from FY2025, financial-system change)
- fuzzy name matches in DC/HUD documents (21): CENTER FOR NON- PROFIT ADVANCEMENT -> CENTER FOR NONPROFIT ADVANCEMENT (98); CENTER FOR NON-PROFIT ADVANCEMENT -> CENTER FOR NONPROFIT ADVANCEMENT (98); Calvary Women's Service -> CALVARY WOMENS SERVICES INC (98); Catholic Charities -> CATHOLIC CHARITIES OF THE ARCHDIOCESE OF WASHINGTON INC (100); Catholic Charities of the Archdiocese of -> CATHOLIC CHARITIES OF THE ARCHDIOCESE OF WASHINGTON INC (100); Community Family Live Services -> COMMUNITY FAMILY LIFE SERVICES INC (97); Covenant House -> COVENANT HOUSE WASHINGTON DC (100); Covenant House Greater Washington -> COVENANT HOUSE WASHINGTON DC (94); Covenant House Washington -> COVENANT HOUSE WASHINGTON DC (100); DISTRICT ALLIANCE SAFE HOUSING -> DISTRICT ALLIANCE FOR SAFE HOUSING INC (100); Deaf Abused Women's Network -> DEAF ABUSED WOMEN NETWORK (98); Deaf Abused Women's Network (DAWN) -> DEAF ABUSED WOMEN NETWORK (98); Everyone Home -> EVERYONE HOME DC (100); Housing Counseling Service -> HOUSING COUNSELING SERVICES INC (98); Institute for African Man Development Inc. -> INSTITUTE FOR AFRICAN MAN DEVELOPME NT INC (99); Pathways to Housing -> PATHWAYS TO HOUSING DC (100); SURVIVORS AND ADVOCATES FOR EMPOWERM ENT (DC SAFE) -> SURVIVORS AND ADVOCATES FOR EMPOWERMENT SAFE INC (92); SURVIVORS AND ADVOCATES FOR EMPOWERMENT (SAFE) -> SURVIVORS AND ADVOCATES FOR EMPOWERMENT SAFE INC (100); Survivors and Advocates for Empowerment, Inc. -> SURVIVORS AND ADVOCATES FOR EMPOWERMENT SAFE INC (100); The Hope Foundation Reentry Network Inc. -> HOPE FOUNDATION RE-ENTRY NETWORK INC (92); The National Centers for Children and Families -> NATIONAL CENTER FOR CHILDREN AND FAMILIES (99)
- DHS oversight tie-out: 2024 erap_arpa_grants [ARPA] printed $42,070,444 vs parsed $42,070,444 -> tie
- DHS oversight tie-out: 2024 erap_arpa_grants [ERA2] printed $6,326,098 vs parsed $6,326,098 -> tie
- DHS oversight tie-out: 2024 erap_arpa_grants [Local] printed $576,903 vs parsed $576,903 -> tie
- DHS oversight tie-out: 2025 dv_grantees [FY2024 total grant award] printed $4,462,363 vs parsed $4,462,363 -> tie
- DHS oversight tie-out: 2025 dv_grantees [FY2025 total grant award] printed $4,847,166 vs parsed $4,847,167 -> tie
- DHS oversight tie-out: 2025 erap_arpa_grants [ARPA] printed $7,763,167 vs parsed $7,763,167 -> tie
- DHS oversight tie-out: 2025 erap_arpa_grants [ERA2] printed $30,181,471 vs parsed $30,181,472 -> tie
- DHS oversight tie-out: 2025 erap_arpa_grants [Local] printed $22,587,325 vs parsed $22,587,325 -> tie
- DHS oversight tie-out: 2025 homelessness_prevention [FY24] printed $7,450,000 vs parsed $7,450,000 -> tie
- DHS oversight tie-out: 2025 homelessness_prevention [FY25 YTD] printed $6,119,700 vs parsed $6,119,700 -> tie
- DHS oversight tie-out: 2025 psh_case_management [DHS local] printed $25,803,404 vs parsed $25,803,404 -> tie
- DHS oversight tie-out: 2025 psh_case_management [Medicaid] printed $38,687,549 vs parsed $38,687,549 -> tie
- HUD AwardComp DC-500 2019: 38 projects, parsed $22,075,117 vs printed total $22,075,117 -> tie
- HUD AwardComp DC-500 2020: 39 projects, parsed $23,608,105 vs printed total $23,608,105 -> tie
- HUD AwardComp DC-500 2021: 40 projects, parsed $25,062,775 vs printed total $25,062,775 -> tie
- HUD AwardComp DC-500 2022: 43 projects, parsed $27,933,554 vs printed total $27,933,554 -> tie
- HUD AwardComp DC-500 2023: 39 projects, parsed $29,711,325 vs printed total $29,711,325 -> tie
- HUD AwardComp DC-500 2024: 36 projects, parsed $33,659,924 vs printed total $33,659,924 -> tie
- HUD FY2025 round 1 DC-500 (p12): 15 projects, parsed $15,042,362 vs printed $15,042,362 -> tie
- HUD FY2025 round 2 DC-500 (p22): 4 projects, parsed $6,616,773 vs printed $6,616,773 -> tie
- HUD FY2025 round 3 DC-500 (p37): 16 projects, parsed $11,878,879 vs printed $11,878,879 -> tie
- HUD FY2024 AwardComp vs hud.gov DC report: 36 vs 36 projects, total $33,659,924 vs $33,659,924; project-level differences 0: []
- duplicates: award_row_id collisions 0; fully identical rows 0
- Calvary OVSJG rows: 15 (FY2019-FY2025 layer 13, FY2026 PDF 2); match recon: yes
- provider-name match rate (non-PASS): 114/437 distinct names (26%), 903/2097 rows, 49% of dollars; by source {'dc_oversight': '46/93 names, 263/442 rows', 'dc_ovsjg': '73/351 names, 404/1385 rows', 'hud_coc': '19/26 names, 236/270 rows'}; methods {'unmatched': 1194, 'fuzzy_token_set': 136, 'exact_norm_name': 664, 'manual_alias': 68, 'manual_known_ein': 35}

### 2026-10-10 14:27 — 64_people_relationships
- fact_roles 163,150; dim_person 48,474 (multi-org 2,036); candidate_interlocks 1,270; fact_org_relationships 542,435 {'grant': 431144, 'daf_sponsor_grant': 90827, 'schedule_r_related': 12848, 'shared_board_member': 4162, 'pass_through_funding': 3454}

### 2026-10-10 14:27 — 36-38 dc_hud pulls: notes
- Removed 1,174 identical raw pages (raw/dc_gov/20261010T13*_dcgis_pass_po_supplier_stats_p*.json) written by a failed first run of script 36: the DC GIS statistics endpoint ignores resultOffset, so the pager re-saved page 0. Script 36 now pulls supplier lists with returnDistinctValues and splits grouped statistics so no request exceeds 1,000 rows. The authoritative PASS pull is the run listed in the newest raw/dc_gov/*_dcgis_pass_universe_manifest.json.
- An intermediate PASS pull from the same day used an earlier, looser fuzzy guard. Its raw files stay in raw/, but the final run (--refresh-pass) re-pulled with the final vendor list.
- Scripts 36 and 38 share one name matcher. Order: manual aliases (TCP 521681401; DASH 711019574; DC SAFE 412226446; Housing Up = Transitional Housing Corporation 521675958; Edgewood/Brookland 522246995; Wanda Alston 463159251), then norm_name exact, then rapidfuzz token_set_ratio >= 92 filtered by fuzzy_ok(). fuzzy_ok() rejects LLC/LLP firms and one-sided entity markers (foundation, county, state names), and requires one of: a shared non-generic token with only soft one-sided words, a leading-part match (>= 3 content tokens, >= 60% coverage, or a source-truncated name), or ratio >= 92 with the same first 4 characters.
- Script 38 was rerun after the matcher change; its latest log entry is authoritative.
- Row counts:
  - stage_fact_gov_awards__dc 12,085
  - stage_dc_budget_lines__dc 5,172
  - stage_fact_policy_events__dc 297
  - stage_homeless_counts__hud 49,393
  - stage_hic_projects__hud 1,257

### 2026-10-10 14:28 — 70_quality_checks
- wrote reports/data_quality.md; duplicates []; portability issues ['clean/fact_opportunities.csv']

### 2026-10-10 14:28 — 80_docs
- data_dictionary rows 540; undocumented columns 26; source_ids missing from registry: none

### 2026-10-10 14:47 — 20_build_universes
- calvary: 1 EINs
- calvary_known_funders: 85 EINs
- core_peers: 18 EINs
- daf_sponsors: 15 EINs
- dc_sector: 1,027 EINs
- dmv_funders: 7,705 EINs
- dmv_sector: 4,910 EINs
- named_comparators: 1 EINs
- national_women: 2,878 EINs
- size_matched: 566 EINs
- membership rows 17,206; distinct EINs 15,810; e-file rows 45,294; size band $2,483,998–$9,935,990; missing pins {'F3': [], 'DAF1': []}

### 2026-10-10 14:49 — 33_pull_usaspending: downloads
- jobs 15 (206 in-scope UEIs in 11 chunks)
  - cfda_DC: count {'awards': 836, 'subawards': 892}; {"status": "finished", "total_rows": 1728, "seconds": 40, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H17M28S11_1.csv": 836, "Assistance_Subawards_2026-10-10_H17M28S20_1.csv": 892}, "reused_from": "raw/usaspending/20261010T142255_pull33_manifest.json"}
  - cfda_MD: count {'awards': 2316, 'subawards': 3961}; {"status": "finished", "total_rows": 6277, "seconds": 53, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H17M28S13_1.csv": 2316, "Assistance_Subawards_2026-10-10_H17M28S30_1.csv": 3961}, "reused_from": "raw/usaspending/20261010T142255_pull33_manifest.json"}
  - cfda_VA: count {'awards': 2370, 'subawards': 5869}; {"status": "finished", "total_rows": 8239, "seconds": 55, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H17M28S12_1.csv": 2370, "Assistance_Subawards_2026-10-10_H17M28S34_1.csv": 5869}, "reused_from": "raw/usaspending/20261010T142255_pull33_manifest.json"}
  - calvary: count {'awards': 2, 'subawards': 1}; {"status": "finished", "total_rows": 3, "seconds": 67, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H17M28S09_1.csv": 2, "Assistance_Subawards_2026-10-10_H17M28S12_1.csv": 1}, "reused_from": "raw/usaspending/20261010T142255_pull33_manifest.json"}
  - uei_b00: count {'awards': 275, 'subawards': 235}; {"status": "finished", "total_rows": 510, "seconds": 68, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H17M31S01_1.csv": 275, "Assistance_Subawards_2026-10-10_H17M31S06_1.csv": 235}, "reused_from": "raw/usaspending/20261010T142255_pull33_manifest.json"}
  - uei_b01: count {'awards': 172, 'subawards': 30}; {"status": "finished", "total_rows": 202, "seconds": 69, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H17M31S04_1.csv": 172, "Assistance_Subawards_2026-10-10_H17M31S07_1.csv": 30}, "reused_from": "raw/usaspending/20261010T142255_pull33_manifest.json"}
  - uei_b02: count {'awards': 184, 'subawards': 171}; {"status": "finished", "total_rows": 355, "seconds": 97, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H17M31S06_1.csv": 184, "Assistance_Subawards_2026-10-10_H17M31S09_1.csv": 171}, "reused_from": "raw/usaspending/20261010T142255_pull33_manifest.json"}
  - uei_b03: count {'awards': 213, 'subawards': 140}; {"status": "finished", "total_rows": 353, "seconds": 105, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H17M31S08_1.csv": 213, "Assistance_Subawards_2026-10-10_H17M31S12_1.csv": 140}, "reused_from": "raw/usaspending/20261010T142255_pull33_manifest.json"}
  - uei_b04: count {'awards': 245, 'subawards': 363}; {"status": "finished", "total_rows": 608, "seconds": 107, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H17M31S09_1.csv": 245, "Assistance_Subawards_2026-10-10_H17M31S15_1.csv": 363}, "reused_from": "raw/usaspending/20261010T142255_pull33_manifest.json"}
  - uei_b05: count {}; {"status": "finished", "total_rows": 405, "seconds": 49, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H18M45S37_1.csv": 173, "Assistance_Subawards_2026-10-10_H18M45S40_1.csv": 232}}
  - uei_b06: count {}; {"status": "finished", "total_rows": 292, "seconds": 50, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H18M45S59_1.csv": 140, "Assistance_Subawards_2026-10-10_H18M46S03_1.csv": 152}}
  - uei_b07: count {}; {"status": "finished", "total_rows": 263, "seconds": 123, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H18M47S00_1.csv": 165, "Assistance_Subawards_2026-10-10_H18M47S04_1.csv": 98}}
  - uei_b08: count {}; {"status": "finished", "total_rows": 303, "seconds": 125, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H18M47S16_1.csv": 194, "Assistance_Subawards_2026-10-10_H18M47S19_1.csv": 109}}
  - uei_b09: count {}; {"status": "finished", "total_rows": 360, "seconds": 204, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H18M48S14_1.csv": 223, "Assistance_Subawards_2026-10-10_H18M48S17_1.csv": 137}}
  - uei_b10: count {}; {"status": "finished", "total_rows": 121, "seconds": 206, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H18M48S39_1.csv": 51, "Assistance_Subawards_2026-10-10_H18M48S42_1.csv": 70}}
- manifest raw/usaspending/20261010T144926_pull33_manifest.json

### 2026-10-10 14:52 — 30_fetch_xml: named comparators TY2014-TY2019
- GT efilexml index 311597223: HTTP 200
- 311597223 TY2014-TY2019: 6 returns in GT index: TY2014 990 201523209349311837 gt_s3; TY2015 990 201633209349311293 gt_s3; TY2016 990 201733199349307838 gt_s3; TY2017 990 201843199349319379 gt_s3; TY2018 990 201903199349307010 gt_s3; TY2019 990 202023219349323207 gt_s3

### 2026-10-10 14:52 — 30_fetch_xml: targets
- scope EINs 8,709; EINs with a TY2020+ e-filed 990/EZ/PF in the index 6,773
- returns 31,480 (latest per EIN+period+type) {'990PF': 24877, '990': 4869, '990EZ': 1734}; with >1 submission 351
- GT S3 at 20 req/s, IRS ZIP fallback 4 req/s; 16 threads

### 2026-10-10 14:52 — 30_fetch_xml: progress
- pass 1: 2,000/31,480 done in 0.0 min (3772.1/s); 93 MB on disk for done files; ok 2,000, not_found 0, error 0

### 2026-10-10 14:52 — 30_fetch_xml: progress
- pass 1: 4,000/31,480 done in 0.0 min (4994.9/s); 253 MB on disk for done files; ok 4,000, not_found 0, error 0

### 2026-10-10 14:52 — 30_fetch_xml: progress
- pass 1: 6,000/31,480 done in 0.0 min (5522.9/s); 363 MB on disk for done files; ok 6,000, not_found 0, error 0

### 2026-10-10 14:52 — 30_fetch_xml: progress
- pass 1: 8,000/31,480 done in 0.0 min (5709.3/s); 611 MB on disk for done files; ok 8,000, not_found 0, error 0

### 2026-10-10 14:52 — 30_fetch_xml: progress
- pass 1: 10,000/31,480 done in 0.0 min (5805.6/s); 768 MB on disk for done files; ok 10,000, not_found 0, error 0

### 2026-10-10 14:52 — 30_fetch_xml: progress
- pass 1: 12,000/31,480 done in 0.0 min (5955.6/s); 900 MB on disk for done files; ok 12,000, not_found 0, error 0

### 2026-10-10 14:52 — 30_fetch_xml: progress
- pass 1: 14,000/31,480 done in 0.0 min (6012.1/s); 1,119 MB on disk for done files; ok 14,000, not_found 0, error 0

### 2026-10-10 14:52 — 30_fetch_xml: progress
- pass 1: 16,000/31,480 done in 0.0 min (6332.3/s); 1,241 MB on disk for done files; ok 16,000, not_found 0, error 0

### 2026-10-10 14:52 — 30_fetch_xml: progress
- pass 1: 18,000/31,480 done in 0.0 min (6332.5/s); 1,439 MB on disk for done files; ok 18,000, not_found 0, error 0

### 2026-10-10 14:52 — 30_fetch_xml: progress
- pass 1: 20,000/31,480 done in 0.1 min (6493.6/s); 1,558 MB on disk for done files; ok 20,000, not_found 0, error 0

### 2026-10-10 14:52 — 30_fetch_xml: progress
- pass 1: 22,000/31,480 done in 0.1 min (6469.3/s); 1,751 MB on disk for done files; ok 22,000, not_found 0, error 0

### 2026-10-10 14:52 — 30_fetch_xml: progress
- pass 1: 24,000/31,480 done in 0.1 min (6372.3/s); 1,888 MB on disk for done files; ok 24,000, not_found 0, error 0

### 2026-10-10 14:52 — 30_fetch_xml: progress
- pass 1: 26,000/31,480 done in 0.1 min (6271.5/s); 2,090 MB on disk for done files; ok 26,000, not_found 0, error 0

### 2026-10-10 14:52 — 30_fetch_xml: progress
- pass 1: 28,000/31,480 done in 0.1 min (6287.6/s); 2,279 MB on disk for done files; ok 28,000, not_found 0, error 0

### 2026-10-10 14:52 — 30_fetch_xml: progress
- pass 1: 30,000/31,480 done in 0.1 min (6312.6/s); 2,528 MB on disk for done files; ok 30,000, not_found 0, error 0

### 2026-10-10 14:52 — 30_fetch_xml: done
- returns 31,480; ok 31,480; not_found 0; error 0
- by source (ok): {'gt_s3': 24024, 'irs': 7456}; downloaded this run 5 (0 MB), reused cache 31,475
- total XML bytes in manifest 2,633 MB; elapsed 0.1 min
- manifest -> interim/xml_manifest.csv

### 2026-10-10 14:53 — 50_parse_xml: progress
- 2,000/31,480 parsed in 0.5 min; grants 698,214, roles 22,703, relationships 5,719; errors 0

### 2026-10-10 14:53 — 50_parse_xml: progress
- 4,000/31,480 parsed in 0.5 min; grants 764,178, roles 41,319, relationships 9,850; errors 0

### 2026-10-10 14:53 — 50_parse_xml: progress
- 6,000/31,480 parsed in 0.6 min; grants 804,949, roles 56,969, relationships 10,909; errors 0

### 2026-10-10 14:53 — 50_parse_xml: progress
- 8,000/31,480 parsed in 0.6 min; grants 833,504, roles 71,610, relationships 11,579; errors 0

### 2026-10-10 14:53 — 50_parse_xml: progress
- 10,000/31,480 parsed in 0.6 min; grants 855,931, roles 83,719, relationships 11,966; errors 0

### 2026-10-10 14:53 — 50_parse_xml: progress
- 12,000/31,480 parsed in 0.6 min; grants 872,756, roles 94,450, relationships 12,310; errors 0

### 2026-10-10 14:53 — 50_parse_xml: progress
- 14,000/31,480 parsed in 0.7 min; grants 885,829, roles 104,137, relationships 12,537; errors 0

### 2026-10-10 14:53 — 50_parse_xml: progress
- 16,000/31,480 parsed in 0.7 min; grants 896,903, roles 112,864, relationships 12,668; errors 0

### 2026-10-10 14:53 — 50_parse_xml: progress
- 18,000/31,480 parsed in 0.7 min; grants 906,215, roles 120,812, relationships 12,795; errors 0

### 2026-10-10 14:53 — 50_parse_xml: progress
- 20,000/31,480 parsed in 0.7 min; grants 913,734, roles 128,317, relationships 12,858; errors 0

### 2026-10-10 14:53 — 50_parse_xml: progress
- 22,000/31,480 parsed in 0.8 min; grants 919,347, roles 135,220, relationships 12,862; errors 0

### 2026-10-10 14:53 — 50_parse_xml: progress
- 24,000/31,480 parsed in 0.8 min; grants 923,235, roles 141,610, relationships 12,864; errors 0

### 2026-10-10 14:53 — 50_parse_xml: progress
- 26,000/31,480 parsed in 0.8 min; grants 925,341, roles 148,082, relationships 12,864; errors 0

### 2026-10-10 14:53 — 50_parse_xml: progress
- 28,000/31,480 parsed in 0.8 min; grants 926,481, roles 154,517, relationships 12,864; errors 0

### 2026-10-10 14:53 — 50_parse_xml: progress
- 30,000/31,480 parsed in 0.8 min; grants 926,825, roles 160,709, relationships 12,864; errors 0

### 2026-10-10 14:53 — 50_parse_xml: done
- parsed 31,480 of 31,480 returns in 0.9 min; errors 0 -> xml_parse_errors.csv
- interim/stage_fact_org_financials__xml.csv: 31,480 rows {'990PF': 24877, '990': 4869, '990EZ': 1734}; amended 335; EIN differs from index 0
- interim/stage_fact_grants__xml.csv: 926,874 rows
- interim/stage_fact_roles__xml.csv: 163,902 rows
- interim/stage_fact_org_relationships__xml.csv: 12,864 rows
- interim/org_profile__xml.csv: 31,480 rows (6,773 EINs; street kept on latest return only)
- interim/xml_schedule_i_part3.csv: 1,730 Schedule I Part III lines (aggregates, no names)
- schema versions: {'2014v5.0': 1, '2014v6.0': 1, '2015v2.1': 1, '2015v3.0': 1, '2016v3.0': 2, '2017v2.3': 2, '2018v3.1': 2, '2019v5.1': 1, '2019v5.2': 1, '2020v4.0': 1671, '2020v4.1': 2870, '2020v4.2': 423, '2021v4.0': 1467, '2021v4.1': 767, '2021v4.2': 3218, '2022v4.0': 4, '2022v4.1': 248, '2022v5.0': 5525, '2023v4.0': 271, '2023v5.0': 2462, '2023v5.1': 2421, '2023v6.0': 959, '2024v5.0': 1374, '2024v5.1': 1978, '2024v5.2': 2495, '2024v5.5': 372, '2025v4.0': 1220, '2025v4.1': 1441, '2025v4.2': 282}
- DAF1 sponsors, Schedule I kept only for DC/MD/VA recipients (all years in scope):
  - FIDELITY INVESTMENTS CHARITABLE GIFT FUND (110303001): national 372,180 rows / $58,823.5M; kept DMV 24,496 / $8,007.2M; filtered out $50,816.2M
  - DONOR ADVISED CHARITABLE GIVING INC (311640316): national 257,532 rows / $28,043.2M; kept DMV 17,453 / $4,001.7M; filtered out $24,041.5M
  - NATIONAL PHILANTHROPIC TRUST (237825575): national 83,803 rows / $26,775.7M; kept DMV 6,855 / $3,393.6M; filtered out $23,382.1M
  - VANGUARD CHARITABLE ENDOWMENT PROGRAM (232888152): national 113,808 rows / $12,077.0M; kept DMV 9,471 / $2,022.5M; filtered out $10,054.5M
  - AMERICAN ONLINE GIVING FOUNDATION INC (810739440): national 228,879 rows / $10,079.9M; kept DMV 15,079 / $1,159.3M; filtered out $8,920.6M
  - AMERICAN ENDOWMENT FOUNDATION (341747398): national 65,226 rows / $4,638.5M; kept DMV 5,501 / $441.8M; filtered out $4,196.7M
  - BANK OF AMERICA CHARITABLE GIFT FD (046010342): national 4 rows / $3,249.2M; kept DMV 0 / $0.0M; filtered out $3,249.2M
  - THE AYCO CHARITABLE FOUNDATION (141782466): national 21,612 rows / $2,375.6M; kept DMV 1,874 / $113.0M; filtered out $2,262.5M
  - Renaissance Charitable Foundation Inc (352129262): national 5 rows / $2,288.2M; kept DMV 0 / $0.0M; filtered out $2,288.2M
  - PAYPAL CHARITABLE GIVING FUND (450931286): national 47,570 rows / $1,897.4M; kept DMV 3,864 / $145.8M; filtered out $1,751.5M
  - CHARITIES AID FOUNDATION AMERICA (431634280): national 44,986 rows / $1,870.2M; kept DMV 3,095 / $204.6M; filtered out $1,665.5M
  - THE BLACKBAUD GIVING FUND (460942102): national 35,201 rows / $1,351.7M; kept DMV 2,007 / $135.2M; filtered out $1,216.5M
  - THE GOLDMAN SACHS CHARITABLE GIFT FUND (113813663): national 12,471 rows / $1,056.1M; kept DMV 1,077 / $131.3M; filtered out $924.9M
  - BNY MELLON CHARITABLE GIFT FUND C/O BNY MELLON NA (300748315): national 5,467 rows / $1,022.5M; kept DMV 466 / $17.6M; filtered out $1,004.9M
  - THE US CHARITABLE GIFT TRUST (311663020): national 12,033 rows / $883.9M; kept DMV 984 / $29.0M; filtered out $854.9M

### 2026-10-10 14:55 — 41_pull_soi_extracts: stage
- universe EINs: 15,810
- 990 2012 (12eofinextract990.zip): 294,019 rows read, 2,255 universe rows; fields absent this year: grants_paid, compensation_total, cash_savings_eoy
- 990 2013 (13eofinextract990.zip): 289,603 rows read, 2,255 universe rows
- 990 2014 (14eofinextract990.zip): 299,405 rows read, 2,334 universe rows
- 990 2015 (15eofinextract990.zip): 294,782 rows read, 2,252 universe rows
- 990 2016 (16eofinextract990.zip): 307,483 rows read, 2,421 universe rows
- 990 2017 (17eofinextract990.zip): 300,910 rows read, 2,426 universe rows
- 990 2018 (18eoextract990.zip): 313,339 rows read, 2,514 universe rows
- 990 2019 (19eoextract990.zip): 304,441 rows read, 2,520 universe rows
- 990 2020 (20eoextract990.zip): 273,971 rows read, 2,294 universe rows
- 990 2021 (21eoextract990.zip): 342,920 rows read, 2,874 universe rows
- 990 2022 (22eoextract990.zip): 326,123 rows read, 2,802 universe rows
- 990 2023 (23eoextract990.zip): 338,048 rows read, 2,830 universe rows
- 990 2024 (24eoextract990.zip): 345,365 rows read, 2,985 universe rows
- 990EZ 2012 (12eofinextract990ez.zip): 223,348 rows read, 593 universe rows
- 990EZ 2013 (13eofinextract990ez.zip): 218,981 rows read, 613 universe rows
- 990EZ 2014 (14eofinextract990ez.zip): 234,820 rows read, 659 universe rows
- 990EZ 2015 (15eofinextractEZ.zip): 223,028 rows read, 669 universe rows
- 990EZ 2016 (16eofinextractez.zip): 230,745 rows read, 738 universe rows
- 990EZ 2017 (17eofinextractEZ.zip): 218,097 rows read, 731 universe rows
- 990EZ 2018 (18eoextractez.zip): 226,533 rows read, 766 universe rows
- 990EZ 2019 (19eoextractez.zip): 218,671 rows read, 777 universe rows
- 990EZ 2020 (20eoextractez.zip): 154,314 rows read, 536 universe rows
- 990EZ 2021 (21eoextractez.zip): 218,733 rows read, 867 universe rows
- 990EZ 2022 (22eoextractez.zip): 231,289 rows read, 990 universe rows
- 990EZ 2023 (23eoextractez.zip): 207,536 rows read, 933 universe rows
- 990EZ 2024 (24eoextract990EZ.zip): 203,699 rows read, 986 universe rows
- 990PF 2012 (12eofinextract990pf.zip): 98,948 rows read, 2,669 universe rows; fields absent this year: x_pf_grants_approved_future
- 990PF 2013 (13eofinextract990pf.zip): 100,484 rows read, 2,753 universe rows
- 990PF 2014 (14eofinextract990pf.zip): 101,381 rows read, 2,902 universe rows
- 990PF 2015 (15eofinextract990pf.zip): 103,000 rows read, 2,934 universe rows
- 990PF 2016 (16eofinextract990pf.zip): 105,239 rows read, 3,128 universe rows
- 990PF 2020 (20eoextract990pf.zip): 91,473 rows read, 3,021 universe rows
- 990PF 2021 (21eoextract990pf.zip): 125,312 rows read, 4,414 universe rows
- 990PF 2022 (22eoextract990pf.zip): 115,024 rows read, 4,267 universe rows
- 990PF 2023 (23eoextract990pf.zip): 120,350 rows read, 4,588 universe rows
- 990PF 2024 (24eoextract990pf.zip): 119,059 rows read, 4,795 universe rows
- SOI: 78,091 rows, 9,444 EINs; 0 older-processing-year copies dropped; 0 rows whose copies disagree on total_revenue
- NCCS 2009: 48,857 rows read, 280 universe 990 rows
- NCCS 2010: 184,553 rows read, 932 universe 990 rows
- NCCS 2011: 241,595 rows read, 1,272 universe 990 rows
- NCCS 2012: 273,429 rows read, 1,485 universe 990 rows
- NCCS 2013: 303,225 rows read, 1,645 universe 990 rows
- NCCS 2014: 335,066 rows read, 1,783 universe 990 rows
- NCCS 2015: 358,459 rows read, 1,962 universe 990 rows
- NCCS 2016: 374,252 rows read, 2,045 universe 990 rows
- NCCS 2017: 391,170 rows read, 2,163 universe 990 rows
- NCCS 2018: 406,376 rows read, 2,255 universe 990 rows
- NCCS 2019: 436,217 rows read, 2,393 universe 990 rows
- NCCS 2020: 485,459 rows read, 2,675 universe 990 rows
- NCCS 2021: 491,127 rows read, 2,558 universe 990 rows
- NCCS 2022: 131,588 rows read, 350 universe 990 rows
- NCCS: 22,573 rows staged, 3,105 EINs, tax years 2010-2022; period from SOI match 22,555, from IRS index 18; dropped 901 with no period; 309 EIN-years had >1 return (kept the latest OBJECT_ID)
- NCCS total_revenue equals SOI total_revenue on 99.1% of 22,555 matched rows
- wrote 100,664 rows to interim/stage_fact_org_financials__soi.csv (SOI 78,091; NCCS 22,573)
- duplicate (ein, tax_period_end, return_type, source_id): 0
- Calvary total_revenue QC: bulk_irs_soi_extract TY2020 3,851,984 OK; bulk_irs_soi_extract TY2021 8,867,250 OK; bulk_nccs_efile TY2020 3,851,984 OK; bulk_nccs_efile TY2021 not present
- 990-PF SOI TAX_YR equals derived tax_year on 100.0% of rows
- rows by fiscal_year (period-end year) x return_type / source:
```
source_id   irs_soi_extract              nccs_efile     All
return_type             990 990EZ  990PF        990        
fiscal_year                                                
2002                      0     0      1          0       1
2003                      1     0      1          0       2
2004                      0     0      1          0       1
2005                      1     0      1          0       2
2006                      0     0      1          0       1
2007                      0     2      3          0       5
2008                      2    12      7          0      21
2009                      4    30     14          0      48
2010                    179    93     84          5     361
2011                   1876   519   2406        826    5627
2012                   2227   624   2754       1381    6986
2013                   2279   626   2829       1558    7292
2014                   2299   670   2972       1662    7603
2015                   2365   708   3038       1856    7967
2016                   2445   739    310       1979    5473
2017                   2494   750     23       2078    5345
2018                   2566   763    110       2181    5620
2019                   2625   802   3460       2303    9190
2020                   2649   848   3903       2539    9939
2021                   2761   833   4205       2685   10484
2022                   2852   872   4434       1513    9671
2023                   2861   882   4559          7    8309
2024                    276    85    355          0     716
All                   32762  9858  35471      22573  100664
```
- coverage, bulk_irs_soi_extract (EINs with >=1 row / universe EINs; org-years; median years per covered org):
  - calvary: 1/1; 13; 13
  - calvary_known_funders: 81/85; 837; 10
  - core_peers: 18/18; 235; 13
  - daf_sponsors: 15/15; 184; 13
  - dc_sector: 524/1,027; 4,620; 11
  - dmv_funders: 5,744/7,705; 44,487; 10
  - dmv_sector: 1,942/4,910; 15,530; 9
  - named_comparators: 1/1; 13; 13
  - national_women: 1,395/2,878; 13,420; 12
  - size_matched: 564/566; 6,892; 13
- coverage, bulk_nccs_efile (EINs with >=1 row / universe EINs; org-years; median years per covered org):
  - calvary: 1/1; 7; 7
  - calvary_known_funders: 31/85; 247; 9
  - core_peers: 18/18; 172; 10
  - daf_sponsors: 15/15; 84; 6
  - dc_sector: 370/1,027; 2,550; 7
  - dmv_funders: 650/7,705; 4,046; 6
  - dmv_sector: 1,140/4,910; 7,857; 7
  - named_comparators: 1/1; 11; 11
  - national_women: 959/2,878; 7,769; 9
  - size_matched: 558/566; 4,840; 10

### 2026-10-10 14:55 — 34_pull_fac: FAC bulk pull
- general rows (DC/MD/VA, 2016-2025, + Calvary/named EINs all years; deduped by report_id): 18239; per state-year: {"DC_2016": 391, "DC_2017": 384, "DC_2018": 402, "DC_2019": 398, "DC_2020": 387, "DC_2021": 409, "DC_2022": 466, "DC_2023": 477, "DC_2024": 467, "DC_2025": 359, "MD_2016": 522, "MD_2017": 529, "MD_2018": 516, "MD_2019": 527, "MD_2020": 515, "MD_2021": 585, "MD_2022": 637, "MD_2023": 616, "MD_2024": 599, "MD_2025": 552, "VA_2016": 763, "VA_2017": 801, "VA_2018": 805, "VA_2019": 802, "VA_2020": 816, "VA_2021": 914, "VA_2022": 900, "VA_2023": 884, "VA_2024": 965, "VA_2025": 845}
- by-EIN audit years: {"521307706": ["2022", "2023"], "311597223": ["2020", "2021", "2022", "2023", "2024", "2025"]}
- multi-EIN reports 1417 (additional EINs on 1417); additional-UEI reports 475 (2126 rows)
- kept reports (FAC scope: calvary, core_peers, dc_sector, dmv_sector, named_comparators, dmv_funders): 1841 ({'auditee_ein': 1793, 'additional_ein': 48}); core-scope EINs with a report: 234
- federal_awards rows 9896; passthrough rows 5568
- uei_ein_map rows 9789 (in-scope UEIs 210) -> interim/uei_ein_map.csv
- audit_year vs FY dates: {'calendar_or_same_year': 2350, 'noncal_audit_year=end': 15889}
- requests 90; manifest raw/fac/20261010T145546_pull34_manifest.json

### 2026-10-10 14:56 — 42_pull_propublica: fetch
- targets: 2,537 EINs = 1,037 calvary/core_peers/dc_sector + 1,500 dmv_funders
- funder candidates (F1 with BMF assets >= $1M, plus F2/F3): 3,777 {'F1': 1928, 'F2': 1847, 'F3': 2}
- CAP: kept top 1,500 funders by BMF ASSET_AMT (min kept $2,409,780); dropped 2,277; kept by rule {'F1': 1310, 'F2': 188, 'F3': 2}
- status counts: {'reused': 2533, '200': 4}; new downloads 4, reused raw 2,533
- rate limit 2 req/s (lib.common.RateLimiter)

### 2026-10-10 14:56 — 42_pull_propublica: stage
- 2,537 org JSONs read (0 target EINs with no ProPublica record); 18,278 filings_with_data rows; skipped formtypes {}; 0 bad periods
- tax_prd_yr equals derived fiscal_year (period-end year) on 100.0% of rows
- staged 18,278 rows, 2,003 EINs -> interim/stage_fact_org_financials__propublica.csv; duplicates on (ein, tax_period_end, return_type, source_id): 0
- Calvary total_revenue QC: TY2020 3,851,984 OK; TY2021 8,867,250 OK
- cross-check vs SOI: 18,278 matching (ein, period, form) rows; equal total_revenue 100.0%, total_expenses 100.0%, total_assets_eoy 100.0%
- ProPublica rows with no SOI row: 0 (by fiscal_year {})
- rows by fiscal_year x return_type:
```
return_type   990  990EZ  990PF    All
fiscal_year                           
2007            0      1      1      2
2008            0      1      1      2
2009            0      3      4      7
2010           53     20     20     93
2011          392     61    812   1265
2012          440     70    936   1446
2013          448     65    960   1473
2014          448     66    999   1513
2015          465     72   1017   1554
2016          476     66    107    649
2017          484     69      4    557
2018          493     71     15    579
2019          513     73   1082   1668
2020          511     75   1182   1768
2021          536     74   1229   1839
2022          550     69   1245   1864
2023          549     76   1243   1868
2024           28      4     99    131
All          6386    936  10956  18278
```

### 2026-10-10 14:56 — Named comparator DWC (311597223): XML + financial series
- backups of every staging file touched: interim/_backup/20261010T145214_nc1_dwc/
- scripts/30_fetch_xml.py extended: named comparators (rule NC1) get TY2014-TY2019 returns from the GivingTuesday efilexml index (raw/gt/*_efilexml_311597223.json) via XmlStore; `--refresh-older` re-calls the index. Run: 11 new manifest rows, all DWC (TY2014-TY2024, Form 990, 1 submission each, all GT S3); the other 31,469 manifest rows are unchanged apart from fetch_action (downloaded -> cached).
- scripts/50_parse_xml.py has no subset mode, so it was rerun in full (0.9 min; parser files unchanged since the 14:18 run). Added DWC only: fin +11, profile +11, roles +307, Schedule R +16, grants (as funder, Schedule I) +24, Schedule I Part III +13. Non-DWC rows byte-identical to the backup in every XML staging file; exact duplicate rows 0.
- QC: DWC TY2024 XML total_revenue 34,403,997 = BMF REVENUE_AMT 34,403,997; total_assets_eoy 48,950,770 = BMF ASSET_AMT.
- 41 --only stage: DWC +24 rows (SOI TY2011-TY2023 13, NCCS TY2011-TY2021 11). Pre-existing EINs' rows identical. 114 other EINs also gained rows (1,408): national_women NW4 members (with a few also in dmv_sector/size_matched) added by the 14:47 universe rebuild after the 13:37 stage run.
- 42 --only fetch,stage: 4 new org JSONs (DWC + 3 targets with no raw yet; the 3 have no filings_with_data). DWC +13 rows (TY2011-TY2023); other EINs unchanged. reconcile/notes stages not rerun (Calvary-only, and notes would duplicate).

### 2026-10-10 14:57 — 33_pull_usaspending: downloads
- jobs 16 (206 in-scope UEIs in 11 chunks)
  - cfda_DC: count {'awards': 836, 'subawards': 892}; {"status": "finished", "total_rows": 1728, "seconds": 40, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H17M28S11_1.csv": 836, "Assistance_Subawards_2026-10-10_H17M28S20_1.csv": 892}, "reused_from": "raw/usaspending/20261010T144926_pull33_manifest.json"}
  - cfda_MD: count {'awards': 2316, 'subawards': 3961}; {"status": "finished", "total_rows": 6277, "seconds": 53, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H17M28S13_1.csv": 2316, "Assistance_Subawards_2026-10-10_H17M28S30_1.csv": 3961}, "reused_from": "raw/usaspending/20261010T144926_pull33_manifest.json"}
  - cfda_VA: count {'awards': 2370, 'subawards': 5869}; {"status": "finished", "total_rows": 8239, "seconds": 55, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H17M28S12_1.csv": 2370, "Assistance_Subawards_2026-10-10_H17M28S34_1.csv": 5869}, "reused_from": "raw/usaspending/20261010T144926_pull33_manifest.json"}
  - calvary: count {'awards': 2, 'subawards': 1}; {"status": "finished", "total_rows": 3, "seconds": 67, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H17M28S09_1.csv": 2, "Assistance_Subawards_2026-10-10_H17M28S12_1.csv": 1}, "reused_from": "raw/usaspending/20261010T144926_pull33_manifest.json"}
  - uei_b00: count {'awards': 275, 'subawards': 235}; {"status": "finished", "total_rows": 510, "seconds": 68, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H17M31S01_1.csv": 275, "Assistance_Subawards_2026-10-10_H17M31S06_1.csv": 235}, "reused_from": "raw/usaspending/20261010T144926_pull33_manifest.json"}
  - uei_b01: count {'awards': 172, 'subawards': 30}; {"status": "finished", "total_rows": 202, "seconds": 69, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H17M31S04_1.csv": 172, "Assistance_Subawards_2026-10-10_H17M31S07_1.csv": 30}, "reused_from": "raw/usaspending/20261010T144926_pull33_manifest.json"}
  - uei_b02: count {'awards': 184, 'subawards': 171}; {"status": "finished", "total_rows": 355, "seconds": 97, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H17M31S06_1.csv": 184, "Assistance_Subawards_2026-10-10_H17M31S09_1.csv": 171}, "reused_from": "raw/usaspending/20261010T144926_pull33_manifest.json"}
  - uei_b03: count {'awards': 213, 'subawards': 140}; {"status": "finished", "total_rows": 353, "seconds": 105, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H17M31S08_1.csv": 213, "Assistance_Subawards_2026-10-10_H17M31S12_1.csv": 140}, "reused_from": "raw/usaspending/20261010T144926_pull33_manifest.json"}
  - uei_b04: count {'awards': 245, 'subawards': 363}; {"status": "finished", "total_rows": 608, "seconds": 107, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H17M31S09_1.csv": 245, "Assistance_Subawards_2026-10-10_H17M31S15_1.csv": 363}, "reused_from": "raw/usaspending/20261010T144926_pull33_manifest.json"}
  - uei_b05: count {}; {"status": "finished", "total_rows": 405, "seconds": 49, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H18M45S37_1.csv": 173, "Assistance_Subawards_2026-10-10_H18M45S40_1.csv": 232}, "reused_from": "raw/usaspending/20261010T144926_pull33_manifest.json"}
  - uei_b06: count {}; {"status": "finished", "total_rows": 292, "seconds": 50, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H18M45S59_1.csv": 140, "Assistance_Subawards_2026-10-10_H18M46S03_1.csv": 152}, "reused_from": "raw/usaspending/20261010T144926_pull33_manifest.json"}
  - uei_b07: count {}; {"status": "finished", "total_rows": 263, "seconds": 123, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H18M47S00_1.csv": 165, "Assistance_Subawards_2026-10-10_H18M47S04_1.csv": 98}, "reused_from": "raw/usaspending/20261010T144926_pull33_manifest.json"}
  - uei_b08: count {}; {"status": "finished", "total_rows": 303, "seconds": 125, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H18M47S16_1.csv": 194, "Assistance_Subawards_2026-10-10_H18M47S19_1.csv": 109}, "reused_from": "raw/usaspending/20261010T144926_pull33_manifest.json"}
  - uei_b09: count {}; {"status": "finished", "total_rows": 360, "seconds": 204, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H18M48S14_1.csv": 223, "Assistance_Subawards_2026-10-10_H18M48S17_1.csv": 137}, "reused_from": "raw/usaspending/20261010T144926_pull33_manifest.json"}
  - uei_b10: count {}; {"status": "finished", "total_rows": 121, "seconds": 206, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H18M48S39_1.csv": 51, "Assistance_Subawards_2026-10-10_H18M48S42_1.csv": 70}, "reused_from": "raw/usaspending/20261010T144926_pull33_manifest.json"}
  - named_311597223: count {'awards': 3, 'subawards': 18}; {"status": "finished", "total_rows": 21, "seconds": 23, "members": {"Assistance_PrimeAwardSummaries_2026-10-10_H18M56S25_1.csv": 3, "Assistance_Subawards_2026-10-10_H18M56S27_1.csv": 18}}
- manifest raw/usaspending/20261010T145705_pull33_manifest.json

### 2026-10-10 14:57 — 33_pull_usaspending: stage fact_gov_awards
- interim/stage_fact_gov_awards__federal.csv: 29350 rows; {"named_job_rows_dropped": 1, "usaspending_prime": 7163, "usaspending_sub": 11875, "fac_reports_kept": 1841, "fac_reports_used": 1831, "fac_lines": 9851, "slfrf_dc_rows": 462, "named_comparators": {"311597223": {"rows": 52, "by_source_flow": {"usaspending/prime": 2, "usaspending/subaward": 18, "fac_sefa/pass_through_expenditure": 30, "fac_sefa/prime": 2}, "fac_audit_years": ["2020", "2021", "2022", "2023", "2024", "2025"], "fac_expenditure_by_fy": {"2020": 1043889, "2021": 2781894, "2022": 6904511, "2023": 3279830, "2024": 4249604, "2025": 3358800}, "usaspending_amount": 8521915}}, "rows": 29350, "duplicate_ids": 0, "rows_missing_provenance": 0, "by_source_flow": {"usaspending/prime": 7162, "usaspending/subaward": 11875, "fac_sefa/prime": 4492, "fac_sefa/pass_through_expenditure": 5359, "treasury_slfrf/subaward": 462}, "ein_filled": 23766}
- Calvary reconciliation: {"fac_fy22_total": 4067718, "fac_fy22_ok": true, "fac_ay2023_total": 4064718, "fac_ay2023_conflict_rows": 4, "hud_14251": [200000], "hud_ok": true, "ppp": [327200], "usaspending_subawards": [["14.252", 25000]], "slfrf": [113488, 3680675], "slfrf_ok": true, "calvary_rows": 13}
- EIN coverage (scope = calvary, core_peers, dc_sector, dmv_sector): {"scope_orgs": 4919, "orgs_with_any_row_by_ein": 234, "by_source": {"usaspending": 185, "fac_sefa": 234, "treasury_slfrf": 2}, "extra_orgs_by_exact_name_state_candidate_only": 60}

### 2026-10-10 14:58 — Named comparator DWC (311597223): geocode
- scripts/40_geocode_orgs.py: census_batches() now reuses saved Census response rows one by one (exact id + address match across all raw/census_geocoder request/response pairs), so a scope change that shifts chunk boundaries no longer re-sends whole chunks. Run with --no-notes (no build-log/notes/questions appends from the script; this entry replaces its log).
- Run: MAR 2 1,772 DC addresses, 3 new calls (1,769 reused); Census pass 1 9,500 rows, 17 sent in 1 new batch (9,483 reused); retry 621 rows, 2 sent (619 reused). QC passed; Calvary still ward 8, tract 11001007503.
- interim/stage_org_geo__context.csv: 15,375 -> 15,810 rows (+435 org_base EINs added since the 13:52 run; 21 of them newly in geocode scope, incl. DWC). The 15,375 pre-existing rows are unchanged in every column; duplicate EINs 0.
- DWC: 442 S SAN PEDRO ST, Los Angeles CA 90013 (BMF street) -> census_geocoder exact match, county 06037, tract 06037206202, block 060372062021012, lat 34.0447987, lon -118.2434578.

### 2026-10-10 14:58 — 33_pull_usaspending: stage fact_gov_awards
- interim/stage_fact_gov_awards__federal.csv: 29350 rows; {"named_job_rows_dropped": 1, "usaspending_prime": 7163, "usaspending_sub": 11875, "fac_reports_kept": 1841, "fac_reports_used": 1831, "fac_lines": 9851, "slfrf_dc_rows": 462, "named_comparators": {"311597223": {"rows": 52, "by_source_flow": {"usaspending/prime": 2, "usaspending/subaward": 18, "fac_sefa/pass_through_expenditure": 30, "fac_sefa/prime": 2}, "fac_audit_years": ["2020", "2021", "2022", "2023", "2024", "2025"], "fac_expenditure_by_fy": {"2020": 1043889, "2021": 2781894, "2022": 6904511, "2023": 3279830, "2024": 4249604, "2025": 3358800}, "usaspending_amount": 8521915}}, "rows": 29350, "duplicate_ids": 0, "rows_missing_provenance": 0, "by_source_flow": {"usaspending/prime": 7162, "usaspending/subaward": 11875, "fac_sefa/prime": 4492, "fac_sefa/pass_through_expenditure": 5359, "treasury_slfrf/subaward": 462}, "ein_filled": 23766}
- Calvary reconciliation: {"fac_fy22_total": 4067718, "fac_fy22_ok": true, "fac_ay2023_total": 4064718, "fac_ay2023_conflict_rows": 4, "hud_14251": [200000], "hud_ok": true, "ppp": [327200], "usaspending_subawards": [["14.252", 25000]], "slfrf": [113488, 3680675], "slfrf_ok": true, "calvary_rows": 13}
- EIN coverage (scope = calvary, core_peers, dc_sector, dmv_sector): {"scope_orgs": 4919, "orgs_with_any_row_by_ein": 234, "by_source": {"usaspending": 185, "fac_sefa": 234, "treasury_slfrf": 2}, "extra_orgs_by_exact_name_state_candidate_only": 60}

### 2026-10-10 14:58 — 33_pull_usaspending: notes
- 'Federal pulls' section already in notes_for_analysis.md; not re-appended

### 2026-10-10 14:58 — 16_probe_context: extra_geos
- ACS 2024 group pulls: 22 new, 0 reused, 0 failed (11 groups x 2 geographies)
- B01003 row counts by geography: xgeo_county_06037=1, xgeo_tract_06037206202=1

### 2026-10-10 14:58 — 16_probe_context: catalog
- wrote sources/catalog_parts/context.csv
- statuses:

### 2026-10-10 14:59 — Named comparator DWC (311597223): ACS context geographies
- New config/extra_geographies.csv lists out-of-DMV geographies: Los Angeles County (06037) and DWC's tract 06037206202 (from scripts/40_geocode_orgs.py).
- scripts/16_probe_context.py: acs_geos() appends those rows (raw desc acs5_2024_{group}_xgeo_{geo_key}); new step `--only extra_geos` pulls only them. Run: 22 new ACS group pulls (11 groups x 2 geographies), 0 failed; catalog part unchanged.
- scripts/39_build_geo_period.py: reads the same config; extra rows use the same indicators() derivation as DMV rows and carry x_outside_dmv = True, x_named_comparator_ein, x_scope_note, x_in_msa = False. All other rows get x_outside_dmv = False (nation blank). The DC-tract population QC now filters to state 11. Run with --no-notes (its notes were already appended by the earlier run).
- interim/stage_dim_geo__context.csv 243 -> 245 rows (+1 county, +1 tract); the 243 existing rows unchanged in every existing column; duplicate geo_id 0. tract_ward_crosswalk.csv and stage_dim_period__context.csv byte-identical to the backup.
- LA County: pop 9,808,667; poverty 13.7%; female poverty 14.9%; median HH income $90,112; rent burden 30%+ 57.7%. Tract 2062.02: pop 1,702; poverty 41.9%; female poverty 50.7%; median HH income $24,182 (tract MOEs are wide).

### 2026-10-10 15:00 — 33_pull_usaspending: stage fact_gov_awards
- interim/stage_fact_gov_awards__federal.csv: 28209 rows; {"named_job_rows_dropped": 1, "usaspending_sub_reports": 11875, "usaspending_prime": 7163, "usaspending_sub": 10735, "fac_reports_kept": 1841, "fac_reports_used": 1831, "fac_lines": 9851, "fac_reports_identical_sefa": 18, "slfrf_dc_report_rows": 462, "slfrf_dc_rows": 461, "named_comparators": {"311597223": {"rows": 51, "by_source_flow": {"usaspending/prime": 2, "usaspending/subaward": 17, "fac_sefa/pass_through_expenditure": 30, "fac_sefa/prime": 2}, "fac_audit_years": ["2020", "2021", "2022", "2023", "2024", "2025"], "fac_expenditure_by_fy": {"2020": 1043889, "2021": 2781894, "2022": 6904511, "2023": 3279830, "2024": 4249604, "2025": 3358800}, "usaspending_amount": 8294415}}, "rows": 28209, "duplicate_ids": 0, "rows_missing_provenance": 0, "by_source_flow": {"usaspending/prime": 7162, "usaspending/subaward": 10735, "fac_sefa/prime": 4492, "fac_sefa/pass_through_expenditure": 5359, "treasury_slfrf/subaward": 461}, "ein_filled": 23151}
- Calvary reconciliation: {"fac_fy22_total": 4067718, "fac_fy22_ok": true, "fac_ay2023_total": 4064718, "fac_ay2023_conflict_rows": 4, "hud_14251": [200000], "hud_ok": true, "ppp": [327200], "usaspending_subawards": [["14.252", 25000]], "slfrf": [113488, 3680675], "slfrf_ok": true, "calvary_rows": 13}
- EIN coverage (scope = calvary, core_peers, dc_sector, dmv_sector): {"scope_orgs": 4919, "orgs_with_any_row_by_ein": 234, "by_source": {"usaspending": 185, "fac_sefa": 234, "treasury_slfrf": 2}, "extra_orgs_by_exact_name_state_candidate_only": 60}

### 2026-10-10 15:00 — 33_pull_usaspending: notes
- 'Federal pulls' section already in notes_for_analysis.md; not re-appended

### 2026-10-10 15:02 — 46_web_named_comparators (search)
- searches configured 10; hits 102 (75 distinct URLs) -> interim/web_named_search_hits.csv
- this run: Tavily search 10, extract 0, HTTP GET 0, cache hits 0; cumulative (manifest): search 119/300, extract 10/200, HTTP 117; script-46 totals: search 10/30, extract 0/15

### 2026-10-10 15:02 — 46_web_named_comparators (pages)
- pages listed 9, fetched 9 -> interim/web_named_pages.csv
- failed/empty: none
- this run: Tavily search 0, extract 0, HTTP GET 9, cache hits 0; cumulative (manifest): search 119/300, extract 10/200, HTTP 126; script-46 totals: search 10/30, extract 0/15

### 2026-10-10 15:02 — 33_pull_usaspending: stage fact_gov_awards
- interim/stage_fact_gov_awards__federal.csv: 28207 rows; {"named_job_rows_dropped": 1, "usaspending_sub_reports": 11875, "usaspending_prime": 7163, "usaspending_sub": 10733, "fac_reports_kept": 1841, "fac_reports_used": 1831, "fac_lines": 9851, "fac_reports_identical_sefa": 18, "slfrf_dc_report_rows": 462, "slfrf_dc_rows": 461, "named_comparators": {"311597223": {"rows": 51, "by_source_flow": {"usaspending/prime": 2, "usaspending/subaward": 17, "fac_sefa/pass_through_expenditure": 30, "fac_sefa/prime": 2}, "fac_audit_years": ["2020", "2021", "2022", "2023", "2024", "2025"], "fac_expenditure_by_fy": {"2020": 1043889, "2021": 2781894, "2022": 6904511, "2023": 3279830, "2024": 4249604, "2025": 3358800}, "usaspending_amount": 8294415}}, "rows": 28207, "duplicate_ids": 0, "rows_missing_provenance": 0, "by_source_flow": {"usaspending/prime": 7162, "usaspending/subaward": 10733, "fac_sefa/prime": 4492, "fac_sefa/pass_through_expenditure": 5359, "treasury_slfrf/subaward": 461}, "ein_filled": 23149}
- Calvary reconciliation: {"fac_fy22_total": 4067718, "fac_fy22_ok": true, "fac_ay2023_total": 4064718, "fac_ay2023_conflict_rows": 4, "hud_14251": [200000], "hud_ok": true, "ppp": [327200], "usaspending_subawards": [["14.252", 25000]], "slfrf": [113488, 3680675], "slfrf_ok": true, "calvary_rows": 13}
- EIN coverage (scope = calvary, core_peers, dc_sector, dmv_sector): {"scope_orgs": 4919, "orgs_with_any_row_by_ein": 234, "by_source": {"usaspending": 185, "fac_sefa": 234, "treasury_slfrf": 2}, "extra_orgs_by_exact_name_state_candidate_only": 60}

### 2026-10-10 15:02 — 33_pull_usaspending: notes
- 'Federal pulls' section already in notes_for_analysis.md; not re-appended

### 2026-10-10 15:03 — 33-35 federal pulls: decisions
- Scope for USAspending UEI pull and coverage: calvary, core_peers, dc_sector, dmv_sector, named_comparators; FAC also dmv_funders.
- Downtown Women's Center (311597223, UEI K46WB6NRE7Q7) added at the lead's request: FAC by EIN all years (audit years 2020-2025), USAspending named job FY2019-FY2026 (1 namesake prime dropped).
- USAspending recipient_search_text accepts at most 20 terms (21+ -> HTTP 503); UEI pull runs in 11 chunks of 20.
- api/files.usaspending.gov refused one IP family for ~1 h after request bursts; script now paces 2 jobs in flight, 20 s between submits, 30 s polls, with --ipv and resume of finished jobs.
- Subaward repeat reports collapsed (USAspending 11,875 -> 10,733; SLFRF DC 462 -> 461). FAC: 18 reports with SEFA line sets identical to another report of the same EIN flagged conflict_flag=1; Calvary audit_year 2023 flagged per audit PDF.
- Grants.gov: server keyword search is fuzzy (matches applicant-type labels such as 'Public housing authorities'); kept set uses local regex on title/description/ALN titles/eligibility text or target-ALN match: 286 of 531 candidates.
- USAspending prime amounts = total obligations (loans: face value, amount_type=award_amount); fiscal_year = award base-action federal FY. FAC fiscal_year = year(fy_end_date), org_fy.

### 2026-10-10 15:05 — 46_web_named_comparators (search)
- searches configured 26; hits 262 (204 distinct URLs) -> interim/web_named_search_hits.csv
- this run: Tavily search 16, extract 0, HTTP GET 0, cache hits 10; cumulative (manifest): search 135/300, extract 10/200, HTTP 126; script-46 totals: search 26/30, extract 0/15

### 2026-10-10 15:14 — 46_web_named_comparators (pages)
- pages listed 18, fetched 18 -> interim/web_named_pages.csv
- failed/empty: nc_dwc_anthem_2026 (http:failed; chars 0 -> tavily no_content)
- this run: Tavily search 0, extract 3, HTTP GET 9, cache hits 9; cumulative (manifest): search 135/300, extract 13/200, HTTP 135; script-46 totals: search 26/30, extract 3/15

### 2026-10-10 15:23 — 46_web_named_comparators (pages)
- pages listed 18, fetched 18 -> interim/web_named_pages.csv
- failed/empty: nc_dwc_anthem_2026 (http:failed; chars 0 -> tavily no_content)
- this run: Tavily search 0, extract 1, HTTP GET 2, cache hits 18; cumulative (manifest): search 135/300, extract 14/200, HTTP 137; script-46 totals: search 26/30, extract 4/15

### 2026-10-10 15:25 — lead: named comparator 882046704 federal check
- FAC general by EIN: {'error': {'code': 'API_KEY_MISSING', 'message': 'No api_key was supplied. Get one at https://api.fac.gov:443'}}
- USAspending autocomplete + prime assistance search (name 'CALIFORNIA BLACK WOMEN'): 0 awards. Raw saved under raw/fac/ and raw/usaspending/.

### 2026-10-10 15:25 — lead: named comparator 882046704 FAC (keyed retry)
- FAC general by EIN 882046704: HTTP 200, 0 reports (earlier unkeyed attempt returned 403 API_KEY_MISSING; raw kept)

### 2026-10-10 15:26 — 46_web_named_comparators (stage)
- staged 376 rows -> interim/stage_fact_grants__web_named.csv (exact duplicates dropped 1); recipients {'311597223': 376}
- by source_type {'annual_report': 335, 'support_page': 33, 'web': 8}; amount_kind {'unknown': 335, 'mixed': 33, 'cash': 8}; with amount 8, with band 339
- by fiscal_year {2023: 189, 2024: 2, 2025: 154, 2026: 31}
- non-organization entries counted per band only: 565 -> interim/web_named_donor_band_counts.csv; joint credits with a personal name: 9 trimmed to the organization, 0 dropped
- per page (entries, kept, dropped as non-org, status): nc_dwc_ar_2024 669/188/417/ok; nc_dwc_ar_web 277/148/112/ok; nc_dwc_gala_2025 26/4/18/ok; nc_dwc_gala_2026 54/29/18/ok; nc_dwc_rosas_place_pr 1/1/0/ok; nc_dwc_hilton_2026 1/1/0/ok; nc_dwc_ahmanson_grants 2/2/0/ok; nc_dwc_bscf_grantee 1/1/0/ok; nc_dwc_foxwynd 1/1/0/ok; nc_dwc_anthem_2023 1/1/0/ok; nc_dwc_anthem_2026_dwc_pr 1/1/0/ok
- this run: Tavily search 0, extract 0, HTTP GET 0, cache hits 0; cumulative (manifest): search 135/300, extract 14/200, HTTP 137; script-46 totals: search 26/30, extract 4/15

### 2026-10-10 15:29 — 46_web_named_comparators (stage)
- staged 392 rows -> interim/stage_fact_grants__web_named.csv (exact duplicates dropped 1); recipients {'311597223': 392}
- by source_type {'annual_report': 351, 'support_page': 33, 'web': 8}; amount_kind {'unknown': 351, 'mixed': 33, 'cash': 8}; with amount 8, with band 355
- by fiscal_year {2023: 205, 2024: 2, 2025: 154, 2026: 31}
- non-organization entries counted per band only: 570 -> interim/web_named_donor_band_counts.csv; joint credits with a personal name: 9 trimmed to the organization, 0 dropped
- per page (entries, kept, dropped as non-org, status): nc_dwc_ar_2024 669/204/422/ok; nc_dwc_ar_web 277/148/112/ok; nc_dwc_gala_2025 26/4/18/ok; nc_dwc_gala_2026 54/29/18/ok; nc_dwc_rosas_place_pr 1/1/0/ok; nc_dwc_hilton_2026 1/1/0/ok; nc_dwc_ahmanson_grants 2/2/0/ok; nc_dwc_bscf_grantee 1/1/0/ok; nc_dwc_foxwynd 1/1/0/ok; nc_dwc_anthem_2023 1/1/0/ok; nc_dwc_anthem_2026_dwc_pr 1/1/0/ok
- this run: Tavily search 0, extract 0, HTTP GET 0, cache hits 0; cumulative (manifest): search 135/300, extract 14/200, HTTP 137; script-46 totals: search 26/30, extract 4/15

### 2026-10-10 15:30 — 46_web_named_comparators (stage)
- staged 391 rows -> interim/stage_fact_grants__web_named.csv (exact duplicates dropped 1); recipients {'311597223': 391}
- by source_type {'annual_report': 350, 'support_page': 33, 'web': 8}; amount_kind {'unknown': 350, 'mixed': 33, 'cash': 8}; with amount 8, with band 354
- by fiscal_year {2023: 204, 2024: 2, 2025: 154, 2026: 31}
- non-organization entries counted per band only: 570 -> interim/web_named_donor_band_counts.csv; joint credits with a personal name: 6 trimmed to the organization, 1 dropped
- per page (entries, kept, dropped as non-org, status): nc_dwc_ar_2024 669/203/422/ok; nc_dwc_ar_web 277/148/112/ok; nc_dwc_gala_2025 26/4/18/ok; nc_dwc_gala_2026 54/29/18/ok; nc_dwc_rosas_place_pr 1/1/0/ok; nc_dwc_hilton_2026 1/1/0/ok; nc_dwc_ahmanson_grants 2/2/0/ok; nc_dwc_bscf_grantee 1/1/0/ok; nc_dwc_foxwynd 1/1/0/ok; nc_dwc_anthem_2023 1/1/0/ok; nc_dwc_anthem_2026_dwc_pr 1/1/0/ok
- this run: Tavily search 0, extract 0, HTTP GET 0, cache hits 0; cumulative (manifest): search 135/300, extract 14/200, HTTP 137; script-46 totals: search 26/30, extract 4/15

### 2026-10-10 15:31 — 20_build_universes
- calvary: 1 EINs
- calvary_known_funders: 85 EINs
- core_peers: 18 EINs
- daf_sponsors: 15 EINs
- dc_sector: 1,027 EINs
- dmv_funders: 7,705 EINs
- dmv_sector: 4,910 EINs
- named_comparators: 2 EINs
- national_women: 2,878 EINs
- size_matched: 566 EINs
- membership rows 17,207; distinct EINs 15,811; e-file rows 45,297; size band $2,483,998–$9,935,990; missing pins {'F3': [], 'DAF1': []}

### 2026-10-10 15:31 — Named comparator CBWCEI (882046704): universe rebuild
- Second named comparator added by the lead to config/named_comparators.csv: California Black Women's Collective Empowerment Institute (runs SheWorks), EIN 882046704, Carson CA, NTEE S05, ruling 2022-10, FYE June.
- Reran scripts/20_build_universes.py (backups: interim/_backup/20261010T145214_nc1_dwc/pre_20_rerun/). Diff vs backup: dim_universe_membership 17,206 -> 17,207 (+1 row, named_comparators/NC1 882046704); org_base 15,810 -> 15,811 (+882046704); efile_index_universe 45,294 -> 45,297 (+3 rows, 882046704 TY2022-TY2024: 202343199349315809, 202530959349301108, 202641359349301209); no rows removed or changed; ref_ntee_codes unchanged.

### 2026-10-10 15:31 — 30_fetch_xml: named comparators TY2014-TY2019
- 311597223 TY2014-TY2019: 6 returns in GT index: TY2014 990 201523209349311837 cached; TY2015 990 201633209349311293 cached; TY2016 990 201733199349307838 cached; TY2017 990 201843199349319379 cached; TY2018 990 201903199349307010 cached; TY2019 990 202023219349323207 cached
- GT efilexml index 882046704: HTTP 200
- 882046704 TY2014-TY2019: 0 returns in GT index

### 2026-10-10 15:31 — 30_fetch_xml: targets
- scope EINs 8,710; EINs with a TY2020+ e-filed 990/EZ/PF in the index 6,774
- returns 31,483 (latest per EIN+period+type) {'990PF': 24877, '990': 4872, '990EZ': 1734}; with >1 submission 351
- GT S3 at 20 req/s, IRS ZIP fallback 4 req/s; 16 threads

### 2026-10-10 15:31 — 30_fetch_xml: progress
- pass 1: 2,000/31,483 done in 0.0 min (3993.6/s); 93 MB on disk for done files; ok 2,000, not_found 0, error 0

### 2026-10-10 15:31 — 30_fetch_xml: progress
- pass 1: 4,000/31,483 done in 0.0 min (5312.3/s); 253 MB on disk for done files; ok 4,000, not_found 0, error 0

### 2026-10-10 15:31 — 30_fetch_xml: progress
- pass 1: 6,000/31,483 done in 0.0 min (5980.8/s); 363 MB on disk for done files; ok 6,000, not_found 0, error 0

### 2026-10-10 15:31 — 30_fetch_xml: progress
- pass 1: 8,000/31,483 done in 0.0 min (6247.5/s); 608 MB on disk for done files; ok 8,000, not_found 0, error 0

### 2026-10-10 15:31 — 30_fetch_xml: progress
- pass 1: 10,000/31,483 done in 0.0 min (6571.1/s); 768 MB on disk for done files; ok 10,000, not_found 0, error 0

### 2026-10-10 15:31 — 30_fetch_xml: progress
- pass 1: 12,000/31,483 done in 0.0 min (6680.0/s); 901 MB on disk for done files; ok 12,000, not_found 0, error 0

### 2026-10-10 15:31 — 30_fetch_xml: progress
- pass 1: 14,000/31,483 done in 0.0 min (6763.5/s); 1,119 MB on disk for done files; ok 14,000, not_found 0, error 0

### 2026-10-10 15:31 — 30_fetch_xml: progress
- pass 1: 16,000/31,483 done in 0.0 min (6793.1/s); 1,241 MB on disk for done files; ok 16,000, not_found 0, error 0

### 2026-10-10 15:31 — 30_fetch_xml: progress
- pass 1: 18,000/31,483 done in 0.0 min (6838.1/s); 1,439 MB on disk for done files; ok 18,000, not_found 0, error 0

### 2026-10-10 15:31 — 30_fetch_xml: progress
- pass 1: 20,000/31,483 done in 0.0 min (6859.3/s); 1,558 MB on disk for done files; ok 20,000, not_found 0, error 0

### 2026-10-10 15:31 — 30_fetch_xml: progress
- pass 1: 22,000/31,483 done in 0.1 min (6864.5/s); 1,751 MB on disk for done files; ok 22,000, not_found 0, error 0

### 2026-10-10 15:31 — 30_fetch_xml: progress
- pass 1: 24,000/31,483 done in 0.1 min (6873.1/s); 1,888 MB on disk for done files; ok 24,000, not_found 0, error 0

### 2026-10-10 15:31 — 30_fetch_xml: progress
- pass 1: 26,000/31,483 done in 0.1 min (6862.2/s); 2,090 MB on disk for done files; ok 26,000, not_found 0, error 0

### 2026-10-10 15:31 — 30_fetch_xml: progress
- pass 1: 28,000/31,483 done in 0.1 min (6748.9/s); 2,279 MB on disk for done files; ok 28,000, not_found 0, error 0

### 2026-10-10 15:31 — 30_fetch_xml: progress
- pass 1: 30,000/31,483 done in 0.1 min (6792.5/s); 2,528 MB on disk for done files; ok 30,000, not_found 0, error 0

### 2026-10-10 15:31 — 30_fetch_xml: done
- returns 31,483; ok 31,483; not_found 0; error 0
- by source (ok): {'gt_s3': 24026, 'irs': 7457}; downloaded this run 3 (0 MB), reused cache 31,480
- total XML bytes in manifest 2,633 MB; elapsed 0.1 min
- manifest -> interim/xml_manifest.csv

### 2026-10-10 15:32 — 50_parse_xml: progress
- 2,000/31,483 parsed in 0.4 min; grants 698,214, roles 22,703, relationships 5,719; errors 0

### 2026-10-10 15:32 — 50_parse_xml: progress
- 4,000/31,483 parsed in 0.5 min; grants 764,178, roles 41,319, relationships 9,850; errors 0

### 2026-10-10 15:32 — 50_parse_xml: progress
- 6,000/31,483 parsed in 0.5 min; grants 804,949, roles 56,969, relationships 10,909; errors 0

### 2026-10-10 15:32 — 50_parse_xml: progress
- 8,000/31,483 parsed in 0.6 min; grants 833,489, roles 71,605, relationships 11,579; errors 0

### 2026-10-10 15:32 — 50_parse_xml: progress
- 10,000/31,483 parsed in 0.6 min; grants 855,931, roles 83,719, relationships 11,966; errors 0

### 2026-10-10 15:32 — 50_parse_xml: progress
- 12,000/31,483 parsed in 0.6 min; grants 872,756, roles 94,450, relationships 12,310; errors 0

### 2026-10-10 15:32 — 50_parse_xml: progress
- 14,000/31,483 parsed in 0.6 min; grants 885,831, roles 104,143, relationships 12,537; errors 0

### 2026-10-10 15:32 — 50_parse_xml: progress
- 16,000/31,483 parsed in 0.7 min; grants 896,882, roles 112,871, relationships 12,668; errors 0

### 2026-10-10 15:32 — 50_parse_xml: progress
- 18,000/31,483 parsed in 0.7 min; grants 906,213, roles 120,818, relationships 12,795; errors 0

### 2026-10-10 15:32 — 50_parse_xml: progress
- 20,000/31,483 parsed in 0.7 min; grants 913,736, roles 128,324, relationships 12,858; errors 0

### 2026-10-10 15:32 — 50_parse_xml: progress
- 22,000/31,483 parsed in 0.7 min; grants 919,348, roles 135,226, relationships 12,862; errors 0

### 2026-10-10 15:32 — 50_parse_xml: progress
- 24,000/31,483 parsed in 0.7 min; grants 923,248, roles 141,620, relationships 12,864; errors 0

### 2026-10-10 15:32 — 50_parse_xml: progress
- 26,000/31,483 parsed in 0.7 min; grants 925,353, roles 148,088, relationships 12,864; errors 0

### 2026-10-10 15:32 — 50_parse_xml: progress
- 28,000/31,483 parsed in 0.8 min; grants 926,494, roles 154,519, relationships 12,864; errors 0

### 2026-10-10 15:32 — 50_parse_xml: progress
- 30,000/31,483 parsed in 0.8 min; grants 926,838, roles 160,722, relationships 12,864; errors 0

### 2026-10-10 15:32 — 50_parse_xml: done
- parsed 31,483 of 31,483 returns in 0.8 min; errors 0 -> xml_parse_errors.csv
- interim/stage_fact_org_financials__xml.csv: 31,483 rows {'990PF': 24877, '990': 4872, '990EZ': 1734}; amended 335; EIN differs from index 0
- interim/stage_fact_grants__xml.csv: 926,887 rows
- interim/stage_fact_roles__xml.csv: 163,918 rows
- interim/stage_fact_org_relationships__xml.csv: 12,864 rows
- interim/org_profile__xml.csv: 31,483 rows (6,774 EINs; street kept on latest return only)
- interim/xml_schedule_i_part3.csv: 1,730 Schedule I Part III lines (aggregates, no names)
- schema versions: {'2014v5.0': 1, '2014v6.0': 1, '2015v2.1': 1, '2015v3.0': 1, '2016v3.0': 2, '2017v2.3': 2, '2018v3.1': 2, '2019v5.1': 1, '2019v5.2': 1, '2020v4.0': 1671, '2020v4.1': 2870, '2020v4.2': 423, '2021v4.0': 1467, '2021v4.1': 767, '2021v4.2': 3218, '2022v4.0': 4, '2022v4.1': 248, '2022v5.0': 5526, '2023v4.0': 271, '2023v5.0': 2462, '2023v5.1': 2421, '2023v6.0': 960, '2024v5.0': 1374, '2024v5.1': 1978, '2024v5.2': 2496, '2024v5.5': 372, '2025v4.0': 1220, '2025v4.1': 1441, '2025v4.2': 282}
- DAF1 sponsors, Schedule I kept only for DC/MD/VA recipients (all years in scope):
  - FIDELITY INVESTMENTS CHARITABLE GIFT FUND (110303001): national 372,180 rows / $58,823.5M; kept DMV 24,496 / $8,007.2M; filtered out $50,816.2M
  - DONOR ADVISED CHARITABLE GIVING INC (311640316): national 257,532 rows / $28,043.2M; kept DMV 17,453 / $4,001.7M; filtered out $24,041.5M
  - NATIONAL PHILANTHROPIC TRUST (237825575): national 83,803 rows / $26,775.7M; kept DMV 6,855 / $3,393.6M; filtered out $23,382.1M
  - VANGUARD CHARITABLE ENDOWMENT PROGRAM (232888152): national 113,808 rows / $12,077.0M; kept DMV 9,471 / $2,022.5M; filtered out $10,054.5M
  - AMERICAN ONLINE GIVING FOUNDATION INC (810739440): national 228,879 rows / $10,079.9M; kept DMV 15,079 / $1,159.3M; filtered out $8,920.6M
  - AMERICAN ENDOWMENT FOUNDATION (341747398): national 65,226 rows / $4,638.5M; kept DMV 5,501 / $441.8M; filtered out $4,196.7M
  - BANK OF AMERICA CHARITABLE GIFT FD (046010342): national 4 rows / $3,249.2M; kept DMV 0 / $0.0M; filtered out $3,249.2M
  - THE AYCO CHARITABLE FOUNDATION (141782466): national 21,612 rows / $2,375.6M; kept DMV 1,874 / $113.0M; filtered out $2,262.5M
  - Renaissance Charitable Foundation Inc (352129262): national 5 rows / $2,288.2M; kept DMV 0 / $0.0M; filtered out $2,288.2M
  - PAYPAL CHARITABLE GIVING FUND (450931286): national 47,570 rows / $1,897.4M; kept DMV 3,864 / $145.8M; filtered out $1,751.5M
  - CHARITIES AID FOUNDATION AMERICA (431634280): national 44,986 rows / $1,870.2M; kept DMV 3,095 / $204.6M; filtered out $1,665.5M
  - THE BLACKBAUD GIVING FUND (460942102): national 35,201 rows / $1,351.7M; kept DMV 2,007 / $135.2M; filtered out $1,216.5M
  - THE GOLDMAN SACHS CHARITABLE GIFT FUND (113813663): national 12,471 rows / $1,056.1M; kept DMV 1,077 / $131.3M; filtered out $924.9M
  - BNY MELLON CHARITABLE GIFT FUND C/O BNY MELLON NA (300748315): national 5,467 rows / $1,022.5M; kept DMV 466 / $17.6M; filtered out $1,004.9M
  - THE US CHARITABLE GIFT TRUST (311663020): national 12,033 rows / $883.9M; kept DMV 984 / $29.0M; filtered out $854.9M

### 2026-10-10 15:34 — 41_pull_soi_extracts: stage
- universe EINs: 15,811
- 990 2012 (12eofinextract990.zip): 294,019 rows read, 2,255 universe rows; fields absent this year: grants_paid, compensation_total, cash_savings_eoy
- 990 2013 (13eofinextract990.zip): 289,603 rows read, 2,255 universe rows
- 990 2014 (14eofinextract990.zip): 299,405 rows read, 2,334 universe rows
- 990 2015 (15eofinextract990.zip): 294,782 rows read, 2,252 universe rows
- 990 2016 (16eofinextract990.zip): 307,483 rows read, 2,421 universe rows
- 990 2017 (17eofinextract990.zip): 300,910 rows read, 2,426 universe rows
- 990 2018 (18eoextract990.zip): 313,339 rows read, 2,514 universe rows
- 990 2019 (19eoextract990.zip): 304,441 rows read, 2,520 universe rows
- 990 2020 (20eoextract990.zip): 273,971 rows read, 2,294 universe rows
- 990 2021 (21eoextract990.zip): 342,920 rows read, 2,874 universe rows
- 990 2022 (22eoextract990.zip): 326,123 rows read, 2,802 universe rows
- 990 2023 (23eoextract990.zip): 338,048 rows read, 2,831 universe rows
- 990 2024 (24eoextract990.zip): 345,365 rows read, 2,985 universe rows
- 990EZ 2012 (12eofinextract990ez.zip): 223,348 rows read, 593 universe rows
- 990EZ 2013 (13eofinextract990ez.zip): 218,981 rows read, 613 universe rows
- 990EZ 2014 (14eofinextract990ez.zip): 234,820 rows read, 659 universe rows
- 990EZ 2015 (15eofinextractEZ.zip): 223,028 rows read, 669 universe rows
- 990EZ 2016 (16eofinextractez.zip): 230,745 rows read, 738 universe rows
- 990EZ 2017 (17eofinextractEZ.zip): 218,097 rows read, 731 universe rows
- 990EZ 2018 (18eoextractez.zip): 226,533 rows read, 766 universe rows
- 990EZ 2019 (19eoextractez.zip): 218,671 rows read, 777 universe rows
- 990EZ 2020 (20eoextractez.zip): 154,314 rows read, 536 universe rows
- 990EZ 2021 (21eoextractez.zip): 218,733 rows read, 867 universe rows
- 990EZ 2022 (22eoextractez.zip): 231,289 rows read, 990 universe rows
- 990EZ 2023 (23eoextractez.zip): 207,536 rows read, 933 universe rows
- 990EZ 2024 (24eoextract990EZ.zip): 203,699 rows read, 986 universe rows
- 990PF 2012 (12eofinextract990pf.zip): 98,948 rows read, 2,669 universe rows; fields absent this year: x_pf_grants_approved_future
- 990PF 2013 (13eofinextract990pf.zip): 100,484 rows read, 2,753 universe rows
- 990PF 2014 (14eofinextract990pf.zip): 101,381 rows read, 2,902 universe rows
- 990PF 2015 (15eofinextract990pf.zip): 103,000 rows read, 2,934 universe rows
- 990PF 2016 (16eofinextract990pf.zip): 105,239 rows read, 3,128 universe rows
- 990PF 2020 (20eoextract990pf.zip): 91,473 rows read, 3,021 universe rows
- 990PF 2021 (21eoextract990pf.zip): 125,312 rows read, 4,414 universe rows
- 990PF 2022 (22eoextract990pf.zip): 115,024 rows read, 4,267 universe rows
- 990PF 2023 (23eoextract990pf.zip): 120,350 rows read, 4,588 universe rows
- 990PF 2024 (24eoextract990pf.zip): 119,059 rows read, 4,795 universe rows
- SOI: 78,092 rows, 9,445 EINs; 0 older-processing-year copies dropped; 0 rows whose copies disagree on total_revenue
- NCCS 2009: 48,857 rows read, 280 universe 990 rows
- NCCS 2010: 184,553 rows read, 932 universe 990 rows
- NCCS 2011: 241,595 rows read, 1,272 universe 990 rows
- NCCS 2012: 273,429 rows read, 1,485 universe 990 rows
- NCCS 2013: 303,225 rows read, 1,645 universe 990 rows
- NCCS 2014: 335,066 rows read, 1,783 universe 990 rows
- NCCS 2015: 358,459 rows read, 1,962 universe 990 rows
- NCCS 2016: 374,252 rows read, 2,045 universe 990 rows
- NCCS 2017: 391,170 rows read, 2,163 universe 990 rows
- NCCS 2018: 406,376 rows read, 2,255 universe 990 rows
- NCCS 2019: 436,217 rows read, 2,393 universe 990 rows
- NCCS 2020: 485,459 rows read, 2,675 universe 990 rows
- NCCS 2021: 491,127 rows read, 2,558 universe 990 rows
- NCCS 2022: 131,588 rows read, 350 universe 990 rows
- NCCS: 22,573 rows staged, 3,105 EINs, tax years 2010-2022; period from SOI match 22,555, from IRS index 18; dropped 901 with no period; 309 EIN-years had >1 return (kept the latest OBJECT_ID)
- NCCS total_revenue equals SOI total_revenue on 99.1% of 22,555 matched rows
- wrote 100,665 rows to interim/stage_fact_org_financials__soi.csv (SOI 78,092; NCCS 22,573)
- duplicate (ein, tax_period_end, return_type, source_id): 0
- Calvary total_revenue QC: bulk_irs_soi_extract TY2020 3,851,984 OK; bulk_irs_soi_extract TY2021 8,867,250 OK; bulk_nccs_efile TY2020 3,851,984 OK; bulk_nccs_efile TY2021 not present
- 990-PF SOI TAX_YR equals derived tax_year on 100.0% of rows
- rows by fiscal_year (period-end year) x return_type / source:
```
source_id   irs_soi_extract              nccs_efile     All
return_type             990 990EZ  990PF        990        
fiscal_year                                                
2002                      0     0      1          0       1
2003                      1     0      1          0       2
2004                      0     0      1          0       1
2005                      1     0      1          0       2
2006                      0     0      1          0       1
2007                      0     2      3          0       5
2008                      2    12      7          0      21
2009                      4    30     14          0      48
2010                    179    93     84          5     361
2011                   1876   519   2406        826    5627
2012                   2227   624   2754       1381    6986
2013                   2279   626   2829       1558    7292
2014                   2299   670   2972       1662    7603
2015                   2365   708   3038       1856    7967
2016                   2445   739    310       1979    5473
2017                   2494   750     23       2078    5345
2018                   2566   763    110       2181    5620
2019                   2625   802   3460       2303    9190
2020                   2649   848   3903       2539    9939
2021                   2761   833   4205       2685   10484
2022                   2852   872   4434       1513    9671
2023                   2862   882   4559          7    8310
2024                    276    85    355          0     716
All                   32763  9858  35471      22573  100665
```
- coverage, bulk_irs_soi_extract (EINs with >=1 row / universe EINs; org-years; median years per covered org):
  - calvary: 1/1; 13; 13
  - calvary_known_funders: 81/85; 837; 10
  - core_peers: 18/18; 235; 13
  - daf_sponsors: 15/15; 184; 13
  - dc_sector: 524/1,027; 4,620; 11
  - dmv_funders: 5,744/7,705; 44,487; 10
  - dmv_sector: 1,942/4,910; 15,530; 9
  - named_comparators: 2/2; 14; 7
  - national_women: 1,395/2,878; 13,420; 12
  - size_matched: 564/566; 6,892; 13
- coverage, bulk_nccs_efile (EINs with >=1 row / universe EINs; org-years; median years per covered org):
  - calvary: 1/1; 7; 7
  - calvary_known_funders: 31/85; 247; 9
  - core_peers: 18/18; 172; 10
  - daf_sponsors: 15/15; 84; 6
  - dc_sector: 370/1,027; 2,550; 7
  - dmv_funders: 650/7,705; 4,046; 6
  - dmv_sector: 1,140/4,910; 7,857; 7
  - named_comparators: 1/2; 11; 11
  - national_women: 959/2,878; 7,769; 9
  - size_matched: 558/566; 4,840; 10

### 2026-10-10 15:34 — 42_pull_propublica: fetch
- targets: 2,538 EINs = 1,038 calvary/core_peers/dc_sector + 1,500 dmv_funders
- funder candidates (F1 with BMF assets >= $1M, plus F2/F3): 3,777 {'F1': 1928, 'F2': 1847, 'F3': 2}
- CAP: kept top 1,500 funders by BMF ASSET_AMT (min kept $2,409,780); dropped 2,277; kept by rule {'F1': 1310, 'F2': 188, 'F3': 2}
- status counts: {'reused': 2537, '200': 1}; new downloads 1, reused raw 2,537
- rate limit 2 req/s (lib.common.RateLimiter)

### 2026-10-10 15:35 — 42_pull_propublica: stage
- 2,538 org JSONs read (0 target EINs with no ProPublica record); 18,279 filings_with_data rows; skipped formtypes {}; 0 bad periods
- tax_prd_yr equals derived fiscal_year (period-end year) on 100.0% of rows
- staged 18,279 rows, 2,004 EINs -> interim/stage_fact_org_financials__propublica.csv; duplicates on (ein, tax_period_end, return_type, source_id): 0
- Calvary total_revenue QC: TY2020 3,851,984 OK; TY2021 8,867,250 OK
- cross-check vs SOI: 18,279 matching (ein, period, form) rows; equal total_revenue 100.0%, total_expenses 100.0%, total_assets_eoy 100.0%
- ProPublica rows with no SOI row: 0 (by fiscal_year {})
- rows by fiscal_year x return_type:
```
return_type   990  990EZ  990PF    All
fiscal_year                           
2007            0      1      1      2
2008            0      1      1      2
2009            0      3      4      7
2010           53     20     20     93
2011          392     61    812   1265
2012          440     70    936   1446
2013          448     65    960   1473
2014          448     66    999   1513
2015          465     72   1017   1554
2016          476     66    107    649
2017          484     69      4    557
2018          493     71     15    579
2019          513     73   1082   1668
2020          511     75   1182   1768
2021          536     74   1229   1839
2022          550     69   1245   1864
2023          550     76   1243   1869
2024           28      4     99    131
All          6387    936  10956  18279
```

### 2026-10-10 15:35 — 16_probe_context: extra_geos
- ACS 2024 group pulls: 11 new, 22 reused, 0 failed (11 groups x 3 geographies)
- B01003 row counts by geography: xgeo_county_06037=1, xgeo_tract_06037206202=1, xgeo_tract_06037543322=1

### 2026-10-10 15:35 — 16_probe_context: catalog
- wrote sources/catalog_parts/context.csv
- statuses:

### 2026-10-10 15:35 — Named comparator CBWCEI (882046704): XML, financial series, geography
- 30_fetch_xml: 3 new returns (TY2022 GT S3, TY2023 GT S3, TY2024 IRS 2026_TEOS_XML_05B); GT efilexml index call for 882046704 found no TY2014-TY2019 returns (ruling 2022).
- 50_parse_xml full rerun: added for 882046704 fin 3, profile 3, roles 16, Schedule I grants (as funder) 13; DWC rows unchanged; all other EINs byte-identical to the original backup; duplicates 0.
- QC: TY2024 XML total_revenue 1,840,152 = BMF REVENUE_AMT 1,840,152.
- 41 --only stage: +1 SOI row (TY2022); NCCS e-file tables end at TY2021. 42 --only fetch,stage: 1 new org JSON, +1 row (TY2022). Pre-existing EINs unchanged in both.
- 40 --no-notes: 1 Census row sent (row-level reuse for the rest); 882046704 -> 20218 EDDINGTON DR, Carson CA 90746 (BMF street), exact match, county 06037, tract 06037543322. Pre-existing rows unchanged.
- config/extra_geographies.csv: + tract_06037543322 (LA County row now lists both EINs). 16 --only extra_geos: 11 new ACS pulls. 39 --no-notes: stage_dim_geo__context 246 rows (+3 vs the original 243: LA County, tracts 06037206202 and 06037543322); existing rows unchanged; crosswalk and period files identical.

### 2026-10-10 15:44 — 46_web_named_comparators (pages)
- pages listed 19, fetched 19 -> interim/web_named_pages.csv
- failed/empty: nc_dwc_anthem_2026 (http:failed; chars 0 -> tavily no_content)
- this run: Tavily search 0, extract 0, HTTP GET 3, cache hits 19; cumulative (manifest): search 135/300, extract 14/200, HTTP 140; script-46 totals: search 26/30, extract 4/15

### 2026-10-10 15:53 — 46_web_named_comparators (search,pages)
- searches configured 30; hits 302 (237 distinct URLs) -> interim/web_named_search_hits.csv
- pages listed 20, fetched 20 -> interim/web_named_pages.csv
- failed/empty: nc_dwc_anthem_2026 (http:failed; chars 0 -> tavily no_content); nc_cbw_partners (http:http_404; chars 0 -> tavily no_content)
- this run: Tavily search 4, extract 1, HTTP GET 3, cache hits 46; cumulative (manifest): search 139/300, extract 15/200, HTTP 143; script-46 totals: search 30/30, extract 5/15

### 2026-10-10 16:01 — 46_web_named_comparators (pages)
- pages listed 25, fetched 25 -> interim/web_named_pages.csv
- failed/empty: nc_dwc_anthem_2026 (http:failed; chars 0 -> tavily no_content); nc_cbw_partners (http:http_404; chars 0 -> tavily no_content)
- this run: Tavily search 0, extract 0, HTTP GET 7, cache hits 22; cumulative (manifest): search 139/300, extract 15/200, HTTP 150; script-46 totals: search 30/30, extract 5/15

### 2026-10-10 16:02 — 46_web_named_comparators (stage)
- staged 396 rows -> interim/stage_fact_grants__web_named.csv (exact duplicates dropped 1); recipients {'311597223': 391, '882046704': 5}
- by source_type {'annual_report': 350, 'support_page': 33, 'web': 13}; amount_kind {'unknown': 353, 'mixed': 33, 'cash': 8, 'noncash': 2}; with amount 8, with band 354
- by fiscal_year {2023: 204, 2024: 2, 2025: 155, 2026: 35}
- non-organization entries counted per band only: 570 -> interim/web_named_donor_band_counts.csv; joint credits with a personal name: 6 trimmed to the organization, 1 dropped
- per page (entries, kept, dropped as non-org, status): nc_dwc_ar_2024 669/203/422/ok; nc_dwc_ar_web 277/148/112/ok; nc_dwc_gala_2025 26/4/18/ok; nc_dwc_gala_2026 54/29/18/ok; nc_dwc_rosas_place_pr 1/1/0/ok; nc_dwc_hilton_2026 1/1/0/ok; nc_dwc_ahmanson_grants 2/2/0/ok; nc_dwc_bscf_grantee 1/1/0/ok; nc_dwc_foxwynd 1/1/0/ok; nc_dwc_anthem_2023 1/1/0/ok; nc_dwc_anthem_2026_dwc_pr 1/1/0/ok; nc_cbw_sheworks 1/1/0/ok; nc_cbw_launch_pr 1/1/0/ok; nc_cbw_lacare_pr 2/2/0/ok; nc_cbw_econ_mobility 1/1/0/ok
- this run: Tavily search 0, extract 0, HTTP GET 0, cache hits 0; cumulative (manifest): search 139/300, extract 15/200, HTTP 150; script-46 totals: search 30/30, extract 5/15

### 2026-10-10 16:04 — Named comparators: web funders (46) and XML grant lookup
- New scripts/46_web_named_comparators.py (steps search, pages, stage; reuses the 43 WebFetcher, the 44 fetch_page and the 45 parsers/page_rows). Additions in 46 only:
  - pdf_words: a pdfplumber word-coordinate parser for multi-column donor PDFs.
  - Fixes for 45 rules, patched for this process only: middle initials are not sentence breaks; couples' and firm names are not split as "<person> and <org>".
  - strip_people(): removes personal names from joint credits.
  - Gift-tier price mapping and "$1M +" bands.
- Queries and pages are in config/web_queries.yaml under `named_comparators` (dwc: 26 searches, 18 pages; cbwcei: 4 searches, 7 pages). Script-46 Tavily use: 30/30 searches, 5/15 extracts; other pages by direct GET. Raw in raw/tavily/ and raw/web/; one web_nc_* source per page in the registry; hits in interim/web_named_search_hits.csv; page index in interim/web_named_pages.csv.
- interim/stage_fact_grants__web_named.csv: 396 rows. DWC (311597223): 391 rows = 2023 annual-report list 202, 2025 web annual-report list 148, gala sponsors 33, announcements with amounts 8 (2023-2026). CABWCEI (882046704): 5 rows (LA County Federation of Labor x2, Blue Shield Promise and L.A. Care in-kind, First 5 LA).
- Individuals are not stored: 570 non-organization entries are counted per band in interim/web_named_donor_band_counts.csv; 6 joint credits were trimmed to the organization and 1 dropped. Exact duplicates: 1 dropped.
- Not staged: DWC posts from 2016 ($500K S.L. Gimbel fund) and 2017 ($45K Bank of America), which fall outside 2023-2026; the UniHealth $500K grant (year not stated); Rosa's Place capital-stack partners (project financing).
- XML grants staging lookup: 56 rows to DWC (5 by recipient EIN, 51 by name "downtown women" + CA), 8 funders, $307,596, TY2020-TY2025; 0 to CABWCEI. No file written.

### 2026-10-10 16:06 — 22_match_known_funders
- names 243; outcomes {('corp_foundation', 'inferred'): 16, ('exact_name_state', 'yes'): 33, ('exact_name_unique', 'yes'): 20, ('fuzzy_name_state', 'yes'): 6, ('manual', 'inferred'): 5, ('manual', 'yes'): 11, ('manual_reject', 'no'): 9, ('unmatched', 'no'): 143}; accepted EINs 88

### 2026-10-10 16:07 — 20_build_universes
- calvary: 1 EINs
- calvary_known_funders: 88 EINs
- core_peers: 18 EINs
- daf_sponsors: 15 EINs
- dc_sector: 1,027 EINs
- dmv_funders: 7,705 EINs
- dmv_sector: 4,910 EINs
- named_comparators: 2 EINs
- national_women: 2,878 EINs
- size_matched: 566 EINs
- membership rows 17,210; distinct EINs 15,813; e-file rows 45,309; size band $2,483,998–$9,935,990; missing pins {'F3': [], 'DAF1': []}

### 2026-10-10 16:07 — 60_stage_inputs
- stage_fact_org_financials__inputs.csv: 17 rows
- stage_fact_gov_awards__inputs.csv: 8 rows
- stage_fact_grants__inputs.csv: 360 rows
- stage_fact_roles__inputs.csv: 195 rows

### 2026-10-10 16:09 — 61_resolve_entities
- unique name keys 238,560; alias rows 237,574
- occurrences by method:
match_method  exact_ein  exact_name_city  exact_name_national  exact_name_state  fuzzy_name_city  known_funder  manual  manual_reject  unmatched
role                                                                                                                                            
funder           925013                0                  274                 0                0           231      41             19       3080
pass_through        686                0                 1936                 0                0             0      16              0      14243
recipient        212746           343542                  912             51757            27487             0      48              2     294907

### 2026-10-10 16:11 — 62_build_facts
- fact_org_financials: 150,444 rows
- fact_grants: 928,658 rows
- fact_gov_awards: 40,300 rows
- fact_opportunities: 286 rows
- fact_policy_events: 297 rows
- supp_calvary_individual_donor_bands.csv: copied from stage_supp_calvary_individual_donor_bands.csv
- supp_calvary_program_metrics.csv: copied from stage_supp_calvary_program_metrics.csv
- supp_calvary_strategic_targets.csv: copied from stage_supp_calvary_strategic_targets.csv
- supp_homeless_counts.csv: copied from stage_homeless_counts__hud.csv
- supp_hic_projects.csv: copied from stage_hic_projects__hud.csv
- supp_dc_budget_lines.csv: copied from stage_dc_budget_lines__dc.csv

### 2026-10-10 16:11 — 63_build_dims
- dim_org: 105,156 rows
- dim_funder: 8,930 rows
- dim_program_area: 13 rows
- dim_period: 28 rows
- dim_geo: 246 rows

### 2026-10-10 16:12 — 64_people_relationships
- fact_roles 163,473; dim_person 48,563 (multi-org 2,036); candidate_interlocks 1,270; fact_org_relationships 542,972 {'grant': 431361, 'daf_sponsor_grant': 90830, 'schedule_r_related': 12864, 'shared_board_member': 4162, 'pass_through_funding': 3755}

### 2026-10-10 16:12 — 63_build_dims
- dim_org: 105,156 rows
- dim_funder: 8,930 rows
- dim_program_area: 13 rows
- dim_period: 28 rows
- dim_geo: 246 rows

### 2026-10-10 16:13 — 70_quality_checks
- wrote reports/data_quality.md; duplicates []; portability issues ['clean/fact_grants.csv', 'clean/fact_opportunities.csv', 'sources/source_registry.csv', 'config/web_queries.yaml']

### 2026-10-10 16:13 — 80_docs
- data_dictionary rows 542; undocumented columns 0; source_ids missing from registry: none

### 2026-10-10 16:17 — 70_quality_checks
- wrote reports/data_quality.md; duplicates []; portability issues []

### 2026-10-10 16:18 — 22_match_known_funders
- names 243; outcomes {('corp_foundation', 'inferred'): 16, ('exact_name_state', 'yes'): 33, ('exact_name_unique', 'yes'): 19, ('fuzzy_name_state', 'yes'): 6, ('manual', 'inferred'): 5, ('manual', 'yes'): 11, ('manual_reject', 'no'): 10, ('unmatched', 'no'): 143}; accepted EINs 87

### 2026-10-10 16:19 — 20_build_universes
- calvary: 1 EINs
- calvary_known_funders: 87 EINs
- core_peers: 18 EINs
- daf_sponsors: 15 EINs
- dc_sector: 1,027 EINs
- dmv_funders: 7,705 EINs
- dmv_sector: 4,910 EINs
- named_comparators: 2 EINs
- national_women: 2,878 EINs
- size_matched: 566 EINs
- membership rows 17,209; distinct EINs 15,812; e-file rows 45,305; size band $2,483,998–$9,935,990; missing pins {'F3': [], 'DAF1': []}

### 2026-10-10 16:21 — 61_resolve_entities
- unique name keys 238,560; alias rows 237,574
- occurrences by method:
match_method  exact_ein  exact_name_city  exact_name_national  exact_name_state  fuzzy_name_city  known_funder  manual  manual_reject  unmatched
role                                                                                                                                            
funder           925013                0                  274                 0                0           227      50             23       3071
pass_through        686                0                 1936                 0                0             0      16              0      14243
recipient        212746           343542                  912             51757            27487             0      48              2     294907

### 2026-10-10 16:23 — 62_build_facts
- fact_org_financials: 150,444 rows
- fact_grants: 928,658 rows
- fact_gov_awards: 40,300 rows
- fact_opportunities: 286 rows
- fact_policy_events: 297 rows
- supp_calvary_individual_donor_bands.csv: copied from stage_supp_calvary_individual_donor_bands.csv
- supp_calvary_program_metrics.csv: copied from stage_supp_calvary_program_metrics.csv
- supp_calvary_strategic_targets.csv: copied from stage_supp_calvary_strategic_targets.csv
- supp_homeless_counts.csv: copied from stage_homeless_counts__hud.csv
- supp_hic_projects.csv: copied from stage_hic_projects__hud.csv
- supp_dc_budget_lines.csv: copied from stage_dc_budget_lines__dc.csv

### 2026-10-10 16:23 — 63_build_dims
- dim_org: 105,156 rows
- dim_funder: 8,929 rows
- dim_program_area: 13 rows
- dim_period: 28 rows
- dim_geo: 246 rows

### 2026-10-10 16:24 — 64_people_relationships
- fact_roles 163,473; dim_person 48,563 (multi-org 2,036); candidate_interlocks 1,270; fact_org_relationships 542,975 {'grant': 431364, 'daf_sponsor_grant': 90830, 'schedule_r_related': 12864, 'shared_board_member': 4162, 'pass_through_funding': 3755}

### 2026-10-10 16:24 — 63_build_dims
- dim_org: 105,156 rows
- dim_funder: 8,929 rows
- dim_program_area: 13 rows
- dim_period: 28 rows
- dim_geo: 246 rows

### 2026-10-10 16:26 — 70_quality_checks
- wrote reports/data_quality.md; duplicates []; portability issues []

### 2026-10-10 16:26 — 80_docs
- data_dictionary rows 542; undocumented columns 0; source_ids missing from registry: none

### 2026-10-10 16:27 — 47_geocode_address_overrides
- 882046704: match 06037543400

### 2026-10-10 16:27 — 16_probe_context: extra_geos
- ACS 2024 group pulls: 11 new, 22 reused, 0 failed (11 groups x 3 geographies)
- B01003 row counts by geography: xgeo_county_06037=1, xgeo_tract_06037206202=1, xgeo_tract_06037543400=1

### 2026-10-10 16:27 — 16_probe_context: catalog
- wrote sources/catalog_parts/context.csv
- statuses:

### 2026-10-10 16:28 — 63_build_dims
- dim_org: 105,156 rows
- dim_funder: 8,929 rows
- dim_program_area: 13 rows
- dim_period: 28 rows
- dim_geo: 246 rows

### 2026-10-10 16:31 — 61_resolve_entities
- unique name keys 233,183; alias rows 232,207
- occurrences by method:
match_method  exact_ein  exact_name_city  exact_name_national  exact_name_state  fuzzy_name_city  known_funder  manual  manual_reject  unmatched
role                                                                                                                                            
funder           925013                0                  274                 0                0           227      50             23       3071
pass_through        686                0                 1936                 0                0             0      16              0      14243
recipient        212746           343542                  912             51757            27487             0      48              2     286832

### 2026-10-10 16:33 — 62_build_facts
- fact_org_financials: 150,444 rows
- fact_grants: 928,658 rows
- fact_gov_awards: 40,300 rows
- fact_opportunities: 286 rows
- fact_policy_events: 297 rows
- supp_calvary_individual_donor_bands.csv: copied from stage_supp_calvary_individual_donor_bands.csv
- supp_calvary_program_metrics.csv: copied from stage_supp_calvary_program_metrics.csv
- supp_calvary_strategic_targets.csv: copied from stage_supp_calvary_strategic_targets.csv
- supp_homeless_counts.csv: copied from stage_homeless_counts__hud.csv
- supp_hic_projects.csv: copied from stage_hic_projects__hud.csv
- supp_dc_budget_lines.csv: copied from stage_dc_budget_lines__dc.csv

### 2026-10-10 16:33 — 63_build_dims
- dim_org: 105,156 rows
- dim_funder: 8,929 rows
- dim_program_area: 13 rows
- dim_period: 28 rows
- dim_geo: 246 rows

### 2026-10-10 16:34 — 64_people_relationships
- fact_roles 163,473; dim_person 48,563 (multi-org 2,036); candidate_interlocks 1,270; fact_org_relationships 542,975 {'grant': 431364, 'daf_sponsor_grant': 90830, 'schedule_r_related': 12864, 'shared_board_member': 4162, 'pass_through_funding': 3755}

### 2026-10-10 16:34 — 63_build_dims
- dim_org: 105,156 rows
- dim_funder: 8,929 rows
- dim_program_area: 13 rows
- dim_period: 28 rows
- dim_geo: 246 rows

### 2026-10-10 16:36 — 70_quality_checks
- wrote reports/data_quality.md; duplicates []; portability issues []

### 2026-10-10 16:36 — 80_docs
- data_dictionary rows 542; undocumented columns 0; source_ids missing from registry: none

### 2026-10-10 16:44 — 01_inventory_inputs
- sources/input_inventory.csv: 30 rows (duplicate=1, ok=24, partial=4, unreadable=1)
- registered 30 input_* sources
- period checks: all match

### 2026-10-10 16:45 — 02_extract_inputs
- text dumps: 29 files in raw/inputs_extracted/text
- raw/inputs_extracted/audit_financials.csv: 1089 rows
- raw/inputs_extracted/audit_tieout_checks.csv: 260 rows
- raw/inputs_extracted/sefa_federal_awards.csv: 4 rows
- raw/inputs_extracted/form990_pdf_financials.csv: 362 rows
- raw/inputs_extracted/form990_pdf_people.csv: 113 rows
- raw/inputs_extracted/form990_pdf_schedule_i.csv: 2 rows
- raw/inputs_extracted/funder_mentions.csv: 200 rows
- raw/inputs_extracted/individual_donor_band_counts.csv: 4 rows
- raw/inputs_extracted/board_lists.csv: 82 rows
- raw/inputs_extracted/annual_report_metrics.csv: 178 rows
- raw/inputs_extracted/crm_funders_2023_2026.csv: 160 rows
- raw/inputs_extracted/strategic_plan_targets.csv: 18 rows
- tie-out checks: 260/260 tie
- SEFA: FY15-Audited-Financial-Statements.pdf: SEFA none
- SEFA: 2016-Audited-Financial-Statements.pdf: SEFA none
- SEFA: 2017-Audited-Financial-Statements-Calvary-Women_s-Services.pdf: SEFA none
- SEFA: CWS-FY18-Audit-.pdf: SEFA none
- SEFA: 2019-Audited-Financial-Statements-CWS.pdf: SEFA none
- SEFA: 2020-Audited-Financial-Statements-CWS.pdf: SEFA none
- SEFA: 2021-Audited-Financial-Statements-CWS.pdf: SEFA none
- SEFA: Calvary-Womens-Services-Inc.-9.30.23-FS.pdf: SEFA 4 programs sum 937,999 vs printed total 937,999
- CRM export: 160 orgs, GIFT_TOTAL $10,556,075.88, 877 gifts, last-gift dates 2023-10-16 to 2026-10-03; 21 rows have NUM_GIFTS=1 but GIFT_TOTAL != LAST_CONTRIB_AMT; GIFT_TOTAL window recorded as unconfirmed
- funder names verified in layout text: 171/171
- note: 2015-Form-990-Calvary-Women_s-Services.pdf: Part I not in text layer (page 1 scanned)
- note: 2016-Form-990-Calvary-Women_s-Services.pdf: Part I not in text layer (page 1 scanned)
- note: 2019-990-Form-990-CWS.pdf: Part I not in text layer (page 1 scanned)

### 2026-10-10 16:46 — 20_build_universes
- calvary: 1 EINs
- calvary_known_funders: 87 EINs
- core_peers: 18 EINs
- daf_sponsors: 15 EINs
- dc_sector: 1,027 EINs
- dmv_funders: 7,705 EINs
- dmv_sector: 4,910 EINs
- named_comparators: 2 EINs
- national_women: 2,878 EINs
- size_matched: 566 EINs
- membership rows 17,209; distinct EINs 15,812; e-file rows 45,305; size band $2,483,998–$9,935,990; missing pins {'F3': [], 'DAF1': []}

### 2026-10-10 16:47 — 22_match_known_funders
- names 243; outcomes {('corp_foundation', 'inferred'): 16, ('exact_name_state', 'yes'): 33, ('exact_name_unique', 'yes'): 19, ('fuzzy_name_state', 'yes'): 6, ('manual', 'inferred'): 5, ('manual', 'yes'): 11, ('manual_reject', 'no'): 10, ('unmatched', 'no'): 143}; accepted EINs 87

### 2026-10-10 16:47 — 20_build_universes
- calvary: 1 EINs
- calvary_known_funders: 87 EINs
- core_peers: 18 EINs
- daf_sponsors: 15 EINs
- dc_sector: 1,027 EINs
- dmv_funders: 7,705 EINs
- dmv_sector: 4,910 EINs
- named_comparators: 2 EINs
- national_women: 2,878 EINs
- size_matched: 566 EINs
- membership rows 17,209; distinct EINs 15,812; e-file rows 45,305; size band $2,483,998–$9,935,990; missing pins {'F3': [], 'DAF1': []}

### 2026-10-10 16:52 — 36_parse_dc_awards
- wrote interim/stage_fact_gov_awards__dc.csv: 12,085 rows; by source/section: dc_oversight/dv_grantees 53; dc_oversight/erap_arpa_grants 25; dc_oversight/homelessness_prevention 19; dc_oversight/psh_case_management 90; dc_oversight/singles_shelter_contract_periods 53; dc_oversight/singles_shelter_contracts 50; dc_oversight/singles_shelter_subgrants 6; dc_oversight/youth_dhs_direct_housing 65; dc_oversight/youth_dhs_direct_nonhousing 37; dc_oversight/youth_tcp_housing 44; dc_ovsjg/ovsjg_layer 1267; dc_ovsjg/ovsjg_pdf 118; dc_pass/pass_payments 5494; dc_pass/pass_po 4494; hud_coc/hud_coc 270
- decisions: OVSJG flow_type dc_local_grant unless the stated funding source is federal only (then subaward with OVSJG as pass-through); assistance_listing filled only from the stated funding source (VOCA 16.575, STOP VAWA 16.588, SASP 16.017, Byrne JAG 16.738, JJDP Title II 16.540, Title V 16.548, RSAT 16.593, Coverdell 16.742, ARPA -> SLFRF 21.027); DHS ERAP ARPA/ERA2 shares are subawards (21.027/21.023); HUD CoC rows: TCP-applicant projects -> recipient = sponsor in the project title, flow subaward, pass-through TCP; other applicants -> prime; fiscal_year = CoC competition year (federal_fy).
- OVSJG layer 35: 1267 rows FY2016-FY2025; AGENCY used as grantee, ORGANIZATIONNAME as project title (labels swapped); 6 rows flagged as identical repeats
- OVSJG FY2024 PDF p2: 'Metro DC Community Center Inc., The' amount from text layer: 327000
- OVSJG FY2024 PDF (raw/dc_gov/20261010T123646_ovsjg_funding_recipients_FY2024.pdf): 121 grant rows, total $62,935,024
- OVSJG FY2025 PDF (raw/dc_gov/20261010T123645_ovsjg_funding_recipients_FY2025.pdf): 120 grant rows, total $92,682,681
- OVSJG FY2026 PDF (raw/dc_gov/20261010T123645_ovsjg_funding_recipients_FY2026.pdf): 118 grant rows, total $96,653,604
- OVSJG merge: 241 FY2024/FY2025 layer rows enriched from the PDFs (funding source, period, issue date); 118 PDF rows added (118 FY2026); PDF rows without a layer match: 0 []; layer FY2024/25 rows without a PDF match: 0 []
- DHS oversight provider tables: 442 rows; by section {'erap_arpa_grants': 25, 'homelessness_prevention': 19, 'youth_dhs_direct_nonhousing': 37, 'youth_tcp_housing': 44, 'youth_dhs_direct_housing': 65, 'psh_case_management': 90, 'singles_shelter_contracts': 50, 'dv_grantees': 53, 'singles_shelter_contract_periods': 53, 'singles_shelter_subgrants': 6}; $0 cells skipped: 20
- HUD CoC DC-500: 270 project rows ({2019: 38, 2020: 39, 2021: 40, 2022: 43, 2023: 39, 2024: 36, 2025: 35}); flow {'prime': 66, 'subaward': 204}
- PASS: 18,655 distinct PO suppliers, 73,834 distinct payment suppliers; matched to universe/TCP EINs: 188 PO supplier strings (182 EINs), 258 payment supplier strings (196 EINs); PO methods {'exact_norm_name': 145, 'fuzzy_token_set': 42, 'manual_known_ein': 1}
- PASS fuzzy supplier matches (75): ACCESS HOUSING INC. -> ACCESS HOUSING INC DC (100); ACCESS HOUSING INC. (DC) -> ACCESS HOUSING INC DC (100); AFFORDABLE HOUSING OPPORTUNITI -> AFFORDABLE HOUSING OPPORTUNITIES INC (97); AMERICAN ASSOC OF RESIDENTIAL -> AMERICAN ASSOCIATION OF RESIDENTIAL MORTGAGE REGULATORS (100); AMERICAN SOCIETY OF ADDICTION -> AMERICAN SOCIETY OF ADDICTION MEDICINE INC (100); American Society of Addiction -> AMERICAN SOCIETY OF ADDICTION MEDICINE INC (100); BENNING PARK NEIGHBORHOOD CORP -> BENNING PARK NEIGHBORHOOD ASSOCIATI ON (100); BLACK FEM  INC -> BLACKFEM INC (94); BLACK FEM, INC -> BLACKFEM INC (94); BREASTFEEDING OUTREACH FOR GRE -> BREASTFEEDING OUTREACH FOR GREATER WASHINGTON (93); Breastfeeding Outreach for Gre -> BREASTFEEDING OUTREACH FOR GREATER WASHINGTON (93); CAPITOL HILL COUNSELING A -> CAPITOL HILL COUNSELING AND RESOURCE CENTER INC (100); CARE AND PROGRESS COMMUNITY DE -> CARE AND PROGRESS COMMUNITY DEVELOPMENT (94); CATHOLIC CHARITIES -> CATHOLIC CHARITIES OF THE ARCHDIOCESE OF WASHINGTON INC (100); CENTER FOR ADOPTION SUPPORT -> CENTER FOR ADOPTION SUPPORT AND EDUCATION INC (100); CHILDREN & CHARITY INTERNATION -> CHILDREN & CHARITY INTERNATIONAL (97); COALITION FOR THE HOMELESS, IN -> COALITION FOR THE HOMELESS INC (100); COMMUNITY BRIDGE INC -> COMMUNITY BRIDGES INCORPORATED (97); COMMUNITY CONNECTION -> COMMUNITY CONNECTIONS (98); COMMUNITY FAMILY LIFE SERVICE, -> COMMUNITY FAMILY LIFE SERVICES INC (98); COURTNEY S HOUSE INC -> COURTNEYS HOUSE INC (97); COVENANT HOUSE WASHINGTON -> COVENANT HOUSE WASHINGTON DC (100); Care and Progress Community De -> CARE AND PROGRESS COMMUNITY DEVELOPMENT (94); Catholic Charities of the Archdiocese of -> CATHOLIC CHARITIES OF THE ARCHDIOCESE OF WASHINGTON INC (100); DC ACTION FOR CHILDREN TODAY -> DC ACTION FOR CHILDREN TODAY DC ACT (100); DEAF ABUSED WOMEN'S NETWORK -> DEAF ABUSED WOMEN NETWORK (98); DEEDS OF KINDNESS OUTREACH -> DEEDS OF KINDNESS OUTREACH SERVICES (100); DISABLED VETERANS NATL FOUNDAT -> DISABLED VETERANS NATIONAL FOUNDATION (96); DISTRICT ALLIANCE SAFE HOUSING -> DISTRICT ALLIANCE FOR SAFE HOUSING INC (100); DOORS OF HOPE INC -> DOOR OF HOPE (95); Doors of Hope Inc -> DOOR OF HOPE (95); EXCELLENT COMMUNITY SERVI -> EXCELLENT COMMUNITY SERVICES INC (94); FAMILY MEDICAL COUNSELING -> FAMILY AND MEDICAL COUNSELING SERVICE INC (100); FAR SOUTHEAST FAMILY -> FAR SOUTHEAST FAMILY STRENGTHENING COLLABORATIVE (100); FOUR WALLS DEVELOPEMENT INC. -> FOUR WALLS DEVELOPMENT INC (98); FRY PLUMBING & HEATING -> FRY PLUMBING AND HEATING NON PROFIT (100); FRY PLUMBING AND HEATING -> FRY PLUMBING AND HEATING NON PROFIT (100); Fry Plumbing and Heating -> FRY PLUMBING AND HEATING NON PROFIT (100); HOUSING COUNSELING SERVICE -> HOUSING COUNSELING SERVICES INC (98); HOUSING COUNSELING SERVICES, I -> HOUSING COUNSELING SERVICES INC (100); KEY BRIDGE FOUNDATION -> KEY BRIDGE FOUNDATION FOR EDUCATION AND RESEARCH (100); LITTLE SISTERS OF THE POOR -> LITTLE SISTERS OF THE POOR OF WASHINGTON DC INC (100); LUTHERAN SOCIAL SERVICES -> LUTHERAN SOCIAL SERVICES OF THE NATIONAL CAPITAL AREA INC (100); LUTHERAN SOCIAL SERVICES NATL' -> LUTHERAN SOCIAL SERVICES OF THE NATIONAL CAPITAL AREA INC (100); MARTHA S TABLE INC -> MARTHAS TABLE (96); MARY ELIZABETH HOUSE, INC A MI -> THE MARY ELIZABETH HOUSE INC A MINISTRY (93); MISSION FIRST HOUSING DEVELOPM -> MISSION FIRST HOUSING DEVELOPMENT CORPORATION (95); MOUNT LEBANON COMMUNITY DEVELO -> MOUNT LEBANON COMMUNITY DEVELOPMENT CORPORATION (92); Mission First Housing Developm -> MISSION FIRST HOUSING DEVELOPMENT CORPORATION (95); NAT'L FEDERATION OF THE BLIND -> NATIONAL FEDERATION OF THE BLIND OF THE DISTRICT OF COLUMBIA (100); NATIONAL CENTER FOR CHILDREN A -> NATIONAL CENTER FOR CHILDREN AND FAMILIES (100); NATIONAL CENTER FOR VICTIMS OF -> NATIONAL CENTER FOR VICTIMS OF CRIME INC (100); NATIONAL ENERGY AND UTILITY AF -> THE NATIONAL ENERGY AND UTILITY AFFORDABILITY COALITION (94); NATIONAL FEDERATION OF THE BLIND -> NATIONAL FEDERATION OF THE BLIND OF THE DISTRICT OF COLUMBIA (100); NATIONAL FOUNDATION TO END SEN -> NATIONAL FOUNDATION TO END SENIOR HUNGER INC (93); NEIGHBOR S CONSEJO -> NEIGHBORS CONSEJO (97); NORTHERN VIRGINIA FAMILY -> NORTHERN VIRGINIA FAMILY SERVICES INC (100); National Association of State Mental Health Program Directors -> NATIONAL ASSOCIATION OF STATE MENTAL HEALTH PROGRAM DIRECTORS IN (100); National Center For Victims Of -> NATIONAL CENTER FOR VICTIMS OF CRIME INC (100); OMEGA GOLD DEVELOPMENT GR -> OMEGA GOLD DEVELOPMENT GROUP INC (94); PAVING THE WAY MULTI-SERVICE -> PAVING THE WAY MULTI SERVICE INSTITUTE (100); PSI SERVICE III INC -> PSI SERVICES III INC (97); RAPE, ABUSE, INCEST, NATIONAL -> RAPE ABUSE AND INCEST NATIONAL NETWORK INC (100); RESTORATION COMMUNITY ALLIANCE -> RESTORATION COMMUNITY ALLIANCE COMMUNITY DEVLEOPMENT CORPORATION (100); Rape, Abuse, Incest, National -> RAPE ABUSE AND INCEST NATIONAL NETWORK INC (100); SAMARITAN MINISTRY OF GREATER -> SAMARITAN MINISTRY OF GREATER WASHINGTON (100); SERVICE SOURCE, INC -> SERVICESOURCE INC (96); STEPPINGSTONE FOUNDATION, INC. -> STEPPING STONE FOUNDATION INC (98); SYMBRAL FOUNDATION FOR CMTY. -> SYMBRAL FOUNDATION FOR COMMUNITY SERVICES INC (100); Safe Routes to School National Partnersh -> SAFE ROUTES TO SCHOOL NATIONAL PARTNERSHIP (98); THE HOPE FOUNDATION RE-ENTRY -> HOPE FOUNDATION RE-ENTRY NETWORK INC (100); THE MARY ELIZABETH HOUSE -> THE MARY ELIZABETH HOUSE INC A MINISTRY (100); THE NATIONAL REENTRY NETWORK -> THE NATIONAL REENTRY NETWORK FOR RETURNING CITIZENS (100); Torture abolition and Survivors Support -> TORTURE ABOLITION AND SURVIVORS SUPPORT COALITION INTERNATIONAL (100); WASHINGTON REGIONAL ALCOHOL PR -> WASHINGTON REGIONAL ALCOHOL PROGRAM (95)
- PASS POs for universe vendors: 5,602 raw rows -> 4,494 after dedupe on PONUMBER + FISCALYEAR + POTOTAL (repeats removed: 1,108, almost all AA0 sub-office fan-out)
- PASS payments for universe vendors: 5,494 supplier x FY x agency x PO aggregates; FY2025+ rows flagged x_pass_incomplete_fy=1 (PASS incomplete from FY2025, financial-system change)
- fuzzy name matches in DC/HUD documents (21): CENTER FOR NON- PROFIT ADVANCEMENT -> CENTER FOR NONPROFIT ADVANCEMENT (98); CENTER FOR NON-PROFIT ADVANCEMENT -> CENTER FOR NONPROFIT ADVANCEMENT (98); Calvary Women's Service -> CALVARY WOMENS SERVICES INC (98); Catholic Charities -> CATHOLIC CHARITIES OF THE ARCHDIOCESE OF WASHINGTON INC (100); Catholic Charities of the Archdiocese of -> CATHOLIC CHARITIES OF THE ARCHDIOCESE OF WASHINGTON INC (100); Community Family Live Services -> COMMUNITY FAMILY LIFE SERVICES INC (97); Covenant House -> COVENANT HOUSE WASHINGTON DC (100); Covenant House Greater Washington -> COVENANT HOUSE WASHINGTON DC (94); Covenant House Washington -> COVENANT HOUSE WASHINGTON DC (100); DISTRICT ALLIANCE SAFE HOUSING -> DISTRICT ALLIANCE FOR SAFE HOUSING INC (100); Deaf Abused Women's Network -> DEAF ABUSED WOMEN NETWORK (98); Deaf Abused Women's Network (DAWN) -> DEAF ABUSED WOMEN NETWORK (98); Everyone Home -> EVERYONE HOME DC (100); Housing Counseling Service -> HOUSING COUNSELING SERVICES INC (98); Institute for African Man Development Inc. -> INSTITUTE FOR AFRICAN MAN DEVELOPME NT INC (99); Pathways to Housing -> PATHWAYS TO HOUSING DC (100); SURVIVORS AND ADVOCATES FOR EMPOWERM ENT (DC SAFE) -> SURVIVORS AND ADVOCATES FOR EMPOWERMENT SAFE INC (92); SURVIVORS AND ADVOCATES FOR EMPOWERMENT (SAFE) -> SURVIVORS AND ADVOCATES FOR EMPOWERMENT SAFE INC (100); Survivors and Advocates for Empowerment, Inc. -> SURVIVORS AND ADVOCATES FOR EMPOWERMENT SAFE INC (100); The Hope Foundation Reentry Network Inc. -> HOPE FOUNDATION RE-ENTRY NETWORK INC (92); The National Centers for Children and Families -> NATIONAL CENTER FOR CHILDREN AND FAMILIES (99)
- DHS oversight tie-out: 2024 erap_arpa_grants [ARPA] printed $42,070,444 vs parsed $42,070,444 -> tie
- DHS oversight tie-out: 2024 erap_arpa_grants [ERA2] printed $6,326,098 vs parsed $6,326,098 -> tie
- DHS oversight tie-out: 2024 erap_arpa_grants [Local] printed $576,903 vs parsed $576,903 -> tie
- DHS oversight tie-out: 2025 dv_grantees [FY2024 total grant award] printed $4,462,363 vs parsed $4,462,363 -> tie
- DHS oversight tie-out: 2025 dv_grantees [FY2025 total grant award] printed $4,847,166 vs parsed $4,847,167 -> tie
- DHS oversight tie-out: 2025 erap_arpa_grants [ARPA] printed $7,763,167 vs parsed $7,763,167 -> tie
- DHS oversight tie-out: 2025 erap_arpa_grants [ERA2] printed $30,181,471 vs parsed $30,181,472 -> tie
- DHS oversight tie-out: 2025 erap_arpa_grants [Local] printed $22,587,325 vs parsed $22,587,325 -> tie
- DHS oversight tie-out: 2025 homelessness_prevention [FY24] printed $7,450,000 vs parsed $7,450,000 -> tie
- DHS oversight tie-out: 2025 homelessness_prevention [FY25 YTD] printed $6,119,700 vs parsed $6,119,700 -> tie
- DHS oversight tie-out: 2025 psh_case_management [DHS local] printed $25,803,404 vs parsed $25,803,404 -> tie
- DHS oversight tie-out: 2025 psh_case_management [Medicaid] printed $38,687,549 vs parsed $38,687,549 -> tie
- HUD AwardComp DC-500 2019: 38 projects, parsed $22,075,117 vs printed total $22,075,117 -> tie
- HUD AwardComp DC-500 2020: 39 projects, parsed $23,608,105 vs printed total $23,608,105 -> tie
- HUD AwardComp DC-500 2021: 40 projects, parsed $25,062,775 vs printed total $25,062,775 -> tie
- HUD AwardComp DC-500 2022: 43 projects, parsed $27,933,554 vs printed total $27,933,554 -> tie
- HUD AwardComp DC-500 2023: 39 projects, parsed $29,711,325 vs printed total $29,711,325 -> tie
- HUD AwardComp DC-500 2024: 36 projects, parsed $33,659,924 vs printed total $33,659,924 -> tie
- HUD FY2025 round 1 DC-500 (p12): 15 projects, parsed $15,042,362 vs printed $15,042,362 -> tie
- HUD FY2025 round 2 DC-500 (p22): 4 projects, parsed $6,616,773 vs printed $6,616,773 -> tie
- HUD FY2025 round 3 DC-500 (p37): 16 projects, parsed $11,878,879 vs printed $11,878,879 -> tie
- HUD FY2024 AwardComp vs hud.gov DC report: 36 vs 36 projects, total $33,659,924 vs $33,659,924; project-level differences 0: []
- duplicates: award_row_id collisions 0; fully identical rows 0
- Calvary OVSJG rows: 15 (FY2019-FY2025 layer 13, FY2026 PDF 2); match recon: yes
- provider-name match rate (non-PASS): 114/437 distinct names (26%), 903/2097 rows, 49% of dollars; by source {'dc_oversight': '46/93 names, 263/442 rows', 'dc_ovsjg': '73/351 names, 404/1385 rows', 'hud_coc': '19/26 names, 236/270 rows'}; methods {'unmatched': 1194, 'fuzzy_token_set': 136, 'exact_norm_name': 664, 'manual_alias': 68, 'manual_known_ein': 35}

### 2026-10-10 16:53 — 37_parse_dc_budget: DC budget lines and policy events
- interim/stage_dc_budget_lines__dc.csv: 5,172 rows (Counter({'approved': 3172, 'actual': 1968, 'proposed': 32})); in-scope program/agency rows 854; duplicate keys 0
- interim/stage_fact_policy_events__dc.csv: 297 rows; by kind {'change_table_FO0-5': 8, 'change_table_HY0-5': 9, 'change_table_JA0-5': 25, 'yoy_approved_change': 161, 'bsa_subtitle': 25, 'fy2025_change_narrative': 13, 'committee_report_item': 22, 'committee_report_variance': 6, 'change_table_DB0-5': 1, 'council_adjustments_chart_fy2027': 27}; by type {'budget_proposed': 41, 'budget_enacted': 161, 'budget_revised': 66, 'policy_change': 26, 'other': 1, 'program_launch': 2}
- parsed tables: FY2024 JA0 30-PBB (2024_JA0_ja_dhs_tables_2024j.pdf): 62 lines; FY2024 FO0 30-PBB (024_FO0_fo_vsjg_tables_2024j.pdf): 21 lines; FY2024 RM0 30-PBB (2024_RM0_rm_dbh_tables_2024j.pdf): 128 lines; FY2024 DB0 30-PBB (024_DB0_db_dhcd_tables_2024j.pdf): 44 lines; FY2024 HY0 30-PBB (2024_HY0_hy_has_tables_2024j.pdf): 16 lines; FY2024 CF0 30-PBB (2024_CF0_cf_des_tables_2024j.pdf): 69 lines; FY2024 HG0 30-PBB (24_HG0_hg_dmhhs_tables_2024j.pdf): 9 lines; FY2025 JA0 30-PBB (2025_JA0_ja_dhs_tables_2025j.pdf): 61 lines; FY2025 FO0 30-PBB (25_FO0_fo_ovsjg_tables_2025j.pdf): 28 lines; FY2025 RM0 30-PBB (2025_RM0_rm_dbh_tables_2025j.pdf): 87 lines; FY2025 DB0 30-PBB (025_DB0_db_dhcd_tables_2025j.pdf): 36 lines; FY2025 HY0 30-PBB (2025_HY0_hy_hap_tables_2025j.pdf): 7 lines; FY2025 CF0 30-PBB (025_CF0_cf_does_tables_2025j.pdf): 62 lines; FY2025 HG0 30-PBB (25_HG0_hg_dmhhs_tables_2025j.pdf): 8 lines; FY2026 JA0 Table JA0-4 (026_JA0_ja_dhs_chapter_2026o.pdf): 57 lines; FY2026 FO0 Table FO0-4 (26_FO0_fo_vsjg_chapter_2026o.pdf): 26 lines; FY2026 RM0 Table RM0-4 (026_RM0_rm_dbh_chapter_2026o.pdf): 83 lines; FY2026 DB0 Table DB0-4 (26_DB0_db_dhcd_chapter_2026o.pdf): 36 lines; FY2026 HY0 Table HY0-4 (026_HY0_hy_has_chapter_2026o.pdf): 7 lines; FY2026 CF0 Table CF0-4 (26_CF0_cf_does_chapter_2026o.pdf): 61 lines; FY2026 HG0 Table HG0-4 (6_HG0_hg_dmhhs_chapter_2026o.pdf): 6 lines; FY2027 JA0 30-PBB (7_JA0_ja0_dhs_tables_2027a_0.pdf): 57 lines; FY2027 FO0 30-PBB (FO0_fo0_ovsjg_tables_2027a_0.pdf): 26 lines; FY2027 RM0 30-PBB (7_RM0_rm0_dbh_tables_2027a_0.pdf): 80 lines; FY2027 DB0 30-PBB (_DB0_db0_dhcd_tables_2027a_0.pdf): 36 lines; FY2027 HY0 30-PBB (7_HY0_hy0_hap_tables_2027a_0.pdf): 7 lines; FY2027 CF0 30-PBB (_CF0_cf0_does_tables_2027a_0.pdf): 61 lines; FY2027 HG0 30-PBB (HG0_hg0_dmhhs_tables_2027a_0.pdf): 7 lines
- change items: FY2024 JA0 Table JA0-5: 29 change lines, 7 in scope; FY2024 FO0 Table FO0-5: 14 change lines, 3 in scope; FY2024 RM0 Table RM0-5: 25 change lines, 0 in scope; FY2024 DB0 Table DB0-5: 14 change lines, 0 in scope; FY2024 HY0 Table HY0-5: 6 change lines, 6 in scope; FY2024 CF0 Table CF0-5: 16 change lines, 0 in scope; FY2024 HG0 Table HG0-5: 7 change lines, 0 in scope; FY2025 JA0 narrative change sentences (pypdfium2): 8 in scope; FY2025 FO0: chapter change text is font-garbled (amounts missing); OVSJG FY2025 changes taken from the JPS committee report; FY2025 RM0 narrative change sentences (pypdfium2): 0 in scope; FY2025 DB0 narrative change sentences (pypdfium2): 2 in scope; FY2025 HY0 narrative change sentences (pypdfium2): 3 in scope; FY2025 CF0 Table CF0-5: 20 change lines, 0 in scope; FY2025 HG0 narrative change sentences (pypdfium2): 0 in scope; FY2026 JA0 Table JA0-5: 29 change lines, 14 in scope; FY2026 FO0 Table FO0-5: 16 change lines, 4 in scope; FY2026 RM0 Table RM0-5: 27 change lines, 0 in scope; FY2026 DB0 Table DB0-5: 16 change lines, 0 in scope; FY2026 HY0 Table HY0-5: 2 change lines, 2 in scope; FY2026 CF0 Table CF0-5: 17 change lines, 0 in scope; FY2026 HG0 Table HG0-5: 4 change lines, 0 in scope; FY2027 JA0 Table JA0-5: 15 change lines, 4 in scope; FY2027 FO0 Table FO0-5: 11 change lines, 1 in scope; FY2027 RM0 Table RM0-5: 17 change lines, 0 in scope; FY2027 DB0 Table DB0-5: 15 change lines, 1 in scope; FY2027 HY0 Table HY0-5: 3 change lines, 1 in scope; FY2027 CF0 Table CF0-5: 8 change lines, 0 in scope; FY2027 HG0 Table HG0-5: 3 change lines, 0 in scope
- committee report tables: BR_FY25_Housing -> 1 in-scope proposed activity rows (markup 2024-05-09); BR_FY25_JPS -> 0 in-scope proposed activity rows (markup not printed); BR_FY26_committee_budget_report_Human-Services -> 18 in-scope proposed activity rows (markup 2025-06-24); BR_FY26_committee_budget_report_Housing -> 5 in-scope proposed activity rows (markup 2025-06-24); BR_FY26_committee_budget_report_JPS -> 2 in-scope proposed activity rows (markup not printed); BR_FY26_committee_budget_report_Health -> 0 in-scope proposed activity rows (markup 2025-06-23); BR_FY27_committee_budget_report_DRAFT-FY2027-Committee-on-Health -> 2 in-scope proposed activity rows (markup 2026-05-20); BR_FY27_committee_budget_report_FY27-Committee-on-Housing -> 4 in-scope proposed activity rows (markup not printed); BR_FY27_committee_budget_report_52226-FY2027-JPS -> 0 in-scope proposed activity rows (markup not printed)
- FY2027 Council adjustments chart: 1627 rows read, 27 in-scope events
- BSA subtitles kept: 25; curated committee-report items: 22; YoY approved-change events: 161
- tie-outs: 257 pass, 0 fail
- tie-out detail (in-scope divisions): FY2024 JA0 30-PBB p2 division 5000: sum of 23 activities vs subtotal, deltas by column [0, 0, 0, -1] ($000) -> pass | FY2024 JA0 30-PBB p3 agency total: sum of 8 division subtotals, deltas [0, -2, 0, 1] ($000) -> pass | FY2024 JA0 Table JA0-2 p2: sum of 7 fund rows vs GROSS FUNDS, deltas [-1, 0, -1, 0] ($000) -> pass | FY2024 FO0 30-PBB p1 division 4000: sum of 2 activities vs subtotal, deltas by column [0, 0, 0, -1] ($000) -> pass | FY2024 FO0 30-PBB p1 division 5000: sum of 1 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 FO0 30-PBB p1 division 6000: sum of 5 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 FO0 30-PBB p1 agency total: sum of 7 division subtotals, deltas [-2, -1, -2, 1] ($000) -> pass | FY2024 FO0 Table FO0-2 p2: sum of 5 fund rows vs GROSS FUNDS, deltas [0, 0, -1, 0] ($000) -> pass | FY2024 RM0 30-PBB p5 agency total: sum of 16 division subtotals, deltas [0, 1, 1, 0] ($000) -> pass | FY2024 RM0 Table RM0-2 p2: sum of 9 fund rows vs GROSS FUNDS, deltas [0, 1, 0, 1] ($000) -> pass | FY2024 DB0 30-PBB p2 agency total: sum of 9 division subtotals, deltas [0, 0, 0, -1] ($000) -> pass | FY2024 DB0 Table DB0-2 p2: sum of 5 fund rows vs GROSS FUNDS, deltas [1, -1, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 division 4000: sum of 1 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 division 5000: sum of 1 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 division 6000: sum of 5 activities vs subtotal, deltas by column [2, -1, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 agency total: sum of 5 division subtotals, deltas [0, 0, -1, 0] ($000) -> pass | FY2024 HY0 Table HY0-2 p1: sum of 1 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2024 CF0 30-PBB p2 division 4000: sum of 16 activities vs subtotal, deltas by column [0, 0, 0, -1] ($000) -> pass | FY2024 CF0 30-PBB p2 division 5000: sum of 3 activities vs subtotal, deltas by column [1, 0, 1, 0] ($000) -> pass | FY2024 CF0 30-PBB p2 division 6000: sum of 6 activities vs subtotal, deltas by column [1, 0, 0, 0] ($000) -> pass | FY2024 CF0 30-PBB p3 agency total: sum of 11 division subtotals, deltas [-1, 0, 0, -1] ($000) -> pass | FY2024 CF0 Table CF0-2 p2: sum of 6 fund rows vs GROSS FUNDS, deltas [1, 0, 0, 0] ($000) -> pass | FY2024 HG0 30-PBB p1 agency total: sum of 4 division subtotals, deltas [0, 0, 0, 0] ($000) -> pass | FY2024 HG0 Table HG0-2 p2: sum of 2 fund rows vs GROSS FUNDS, deltas [0, 1, 0, 0] ($000) -> pass | FY2025 JA0 30-PBB p2 division HS0030: sum of 28 activities vs subtotal, deltas by column [-2, 1, -1, 1] ($000) -> pass | FY2025 JA0 30-PBB p2 agency total: sum of 6 division subtotals, deltas [0, -1, 1, 0] ($000) -> pass | FY2025 FO0 30-PBB p1 division PS0023: sum of 2 activities vs subtotal, deltas by column [0, 0, -1, 0] ($000) -> pass | FY2025 FO0 30-PBB p2 agency total: sum of 12 division subtotals, deltas [-1, -2, 1, 0] ($000) -> pass | FY2025 RM0 30-PBB p3 agency total: sum of 13 division subtotals, deltas [1, 1, 0, 1] ($000) -> pass | FY2025 DB0 30-PBB p2 agency total: sum of 6 division subtotals, deltas [0, 1, 1, 0] ($000) -> pass | FY2025 HY0 30-PBB p1 division EC0039: sum of 5 activities vs subtotal, deltas by column [0, -1, 0, 0] ($000) -> pass | FY2025 HY0 30-PBB p1 agency total: sum of 1 division subtotals, deltas [0, 0, 0, 0] ($000) -> pass | FY2025 CF0 30-PBB p3 agency total: sum of 10 division subtotals, deltas [0, -1, 0, -1] ($000) -> pass | FY2025 CF0 Table CF0-2 p2: sum of 6 fund rows vs GROSS FUNDS, deltas [0, -1, 0, 0] ($000) -> pass | FY2025 HG0 30-PBB p1 agency total: sum of 3 division subtotals, deltas [0, 0, 0, 1] ($000) -> pass | FY2026 JA0 Table JA0-4 p5 division HS0030: sum of 28 activities vs subtotal, deltas [1, -2, 1, -1] ($000) -> pass | FY2026 JA0 Table JA0-4 p5 agency total: sum of 5 divisions, deltas [-1, -1, 0, 0] ($000) -> pass | FY2026 JA0 Table JA0-2 p2: sum of 7 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 FO0 Table FO0-4 p4 division PS0023: sum of 2 activities vs subtotal, deltas [0, 1, 0, 0] ($000) -> pass | FY2026 FO0 Table FO0-4 p4 agency total: sum of 11 divisions, deltas [-2, 0, 0, 0] ($000) -> pass | FY2026 FO0 Table FO0-2 p2: sum of 4 fund rows vs GROSS FUNDS, deltas [-1, 0, 0, 0] ($000) -> pass | FY2026 RM0 Table RM0-4 p7 agency total: sum of 13 divisions, deltas [1, 1, 2, 0] ($000) -> pass | FY2026 RM0 Table RM0-2 p2: sum of 8 fund rows vs GROSS FUNDS, deltas [1, 0, -1, 0] ($000) -> pass | FY2026 DB0 Table DB0-4 p4 agency total: sum of 6 divisions, deltas [1, -1, 0, -1] ($000) -> pass | FY2026 DB0 Table DB0-2 p2: sum of 4 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 HY0 Table HY0-4 p2 division EC0039: sum of 5 activities vs subtotal, deltas [-1, 1, 0, 0] ($000) -> pass | FY2026 HY0 Table HY0-4 p2 agency total: sum of 1 divisions, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 HY0 Table HY0-2 p1: sum of 1 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 CF0 Table CF0-4 p5 agency total: sum of 10 divisions, deltas [-1, 1, 0, 0] ($000) -> pass | FY2026 CF0 Table CF0-2 p2: sum of 5 fund rows vs GROSS FUNDS, deltas [-1, 1, 0, 1] ($000) -> pass | FY2026 HG0 Table HG0-4 p3 agency total: sum of 2 divisions, deltas [0, 1, 1, 0] ($000) -> pass | FY2026 HG0 Table HG0-2 p2: sum of 1 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2027 JA0 30-PBB p2 division HS0030: sum of 28 activities vs subtotal, deltas by column [-2, -2, -1, -3] ($000) -> pass | FY2027 JA0 30-PBB p2 agency total: sum of 5 division subtotals, deltas [-1, 1, 0, -1] ($000) -> pass | FY2027 JA0 Table JA0-2 p2: sum of 7 fund rows vs GROSS FUNDS, deltas [0, 1, 0, 0] ($000) -> pass | FY2027 FO0 30-PBB p1 division PS0023: sum of 2 activities vs subtotal, deltas by column [1, 0, 0, 0] ($000) -> pass | FY2027 FO0 30-PBB p1 agency total: sum of 11 division subtotals, deltas [-1,
- cross-book disagreements (same FY/stage/code, >$2K apart; later book preferred via x_preferred): 2022 actual JA0 AMP000 total: FY2025 book 33,466,000, FY2024 book 33,534,000 | 2022 actual JA0 AFO000 total: FY2025 book 3,079,000, FY2024 book 3,025,000 | 2022 actual JA0 HS0029 total: FY2025 book 279,438,000, FY2024 book 280,259,000 | 2022 actual JA0 HS0030 total: FY2025 book 625,848,000, FY2024 book 625,869,000 | 2025 approved JA0 H02902 total: FY2026 book 42,867,000, FY2025 book 42,943,000 | 2025 approved JA0 H02905 total: FY2026 book 91,735,000, FY2025 book 91,660,000 | 2025 approved FO0 P01903 total: FY2026 book 18,405,000, FY2025 book 18,312,000 | 2025 approved FO0 PS0019 total: FY2026 book 18,405,000, FY2025 book 18,312,000 | 2025 approved RM0 AFO003 total: FY2026 book 1,120,000, FY2025 book 1,010,000 | 2025 approved RM0 AFO005 total: FY2026 book 567,000, FY2025 book 577,000 | 2025 approved RM0 AFO000 total: FY2026 book 2,378,000, FY2025 book 2,278,000 | 2025 approved RM0 H04201 total: FY2026 book 175,000, FY2025 book 179,000 | 2025 approved RM0 H04202 total: FY2026 book 1,128,000, FY2025 book 1,151,000 | 2025 approved RM0 H04205 total: FY2026 book 381,000, FY2025 book 355,000 | 2025 approved RM0 H04504 total: FY2026 book 1,367,000, FY2025 book 100,000 | 2025 approved RM0 HS0045 total: FY2026 book 37,390,000, FY2025 book 36,123,000 | 2025 approved RM0 H04802 total: FY2026 book 27,140,000, FY2025 book 22,840,000 | 2025 approved RM0 H04805 total: FY2026 book 1,391,000, FY2025 book 5,691,000 | 2025 approved RM0 HS0053 total: FY2026 book 20,351,000, FY2025 book 21,717,000 | 2025 approved CF0 AFO003 total: FY2026 book 2,141,000, FY2025 book 2,222,000 | 2025 approved CF0 AFO000 total: FY2026 book 4,023,000, FY2025 book 4,104,000 | 2025 approved CF0 AMP026 total: FY2026 book 0, FY2025 book -3,000 | 2025 approved CF0 AMP000 total: FY2026 book 24,947,000, FY2025 book 24,944,000 | 2025 approved CF0 O00111 total: FY2026 book 556,000, FY2025 book 559,000 | 2025 approved CF0 GO0047 total: FY2026 book 6,545,000, FY2025 book 6,548,000 | 2025 approved CF0 O05201 total: FY2026 book 15,504,000, FY2025 book 15,422,000 | 2025 approved CF0 GO0052 total: FY2026 book 75,929,000, FY2025 book 75,847,000
- FY2024 old-code -> FY2025 code crosswalk (FY2024 approved): FO0 P02301: FY2024 book 171,000 vs FY2025 book restated 171,000 (delta +0) | FO0 P02303: FY2024 book 45,515,000 vs FY2025 book restated 45,515,000 (delta +0) | FO0 P04502: FY2024 book 3,720,000 vs FY2025 book restated 3,720,000 (delta +0) | HY0 R03903: FY2024 book 4,400,000 vs FY2025 book restated 4,400,000 (delta +0) | HY0 R03904: FY2024 book 0 vs FY2025 book restated 0 (delta +0) | HY0 R03905: FY2024 book 128,094,000 vs FY2025 book restated 128,094,000 (delta +0) | HY0 R03906: FY2024 book 10,581,000 vs FY2025 book restated 10,581,000 (delta +0) | HY0 R03907: FY2024 book 43,296,000 vs FY2025 book restated 43,296,000 (delta +0) | JA0 H03002: FY2024 book 79,033,000 vs FY2025 book restated 93,339,000 (delta +14,306,000) | JA0 H03003: FY2024 book 59,994,000 vs FY2025 book restated 59,994,000 (delta +0) | JA0 H03004: FY2024 book 31,818,000 vs FY2025 book restated 12,421,000 (delta -19,397,000) | JA0 H03007: FY2024 book 2,940,000 vs FY2025 book restated 2,940,000 (delta +0) | JA0 H03008: FY2024 book 42,536,000 vs FY2025 book restated 42,536,000 (delta +0) | JA0 H03009: FY2024 book 2,799,000 vs FY2025 book restated 4,259,000 (delta +1,460,000) | JA0 H03010: FY2024 book 51,764,000 vs FY2025 book restated 60,770,000 (delta +9,006,000) | JA0 H03011: FY2024 book 4,935,000 vs FY2025 book restated 4,935,000 (delta +0) | JA0 H03012: FY2024 book 86,929,000 vs FY2025 book restated 83,014,000 (delta -3,915,000) | JA0 H03013: FY2024 book 4,222,000 vs FY2025 book restated 4,222,000 (delta +0) | JA0 H03014-H03016: FY2024 book 11,541,000 vs FY2025 book restated 11,542,000 (delta +1,000) | JA0 H03017: FY2024 book 73,209,000 vs FY2025 book restated 73,209,000 (delta +0) | JA0 H03018: FY2024 book 10,875,000 vs FY2025 book restated 10,875,000 (delta +0) | JA0 H03019: FY2024 book 1,150,000 vs FY2025 book restated 1,150,000 (delta +0) | JA0 H03022: FY2024 book 1,980,000 vs FY2025 book restated 1,980,000 (delta +0) | JA0 H03023: FY2024 book 12,032,000 vs FY2025 book restated 12,032,000 (delta +0) | RM0 H04308: FY2024 book 29,637,000 vs FY2025 book restated 29,637,000 (delta +0) | RM0 H04504: FY2024 book 1,467,000 vs FY2025 book restated 1,467,000 (delta +0)
- event dates: budget_enacted/budget_revised = Local Budget Act 2nd reading {2024: '2023-05-30', 2025: '2024-06-12', 2026: '2025-07-28', 2027: '2026-06-23'}; budget_proposed = BSA introduced on behalf of the Mayor {2025: '2024-04-03', 2026: '2025-06-02', 2027: '2026-04-14'} (FY2024 proposal date not in downloaded docs -> blank); BSA policy rows = law/act effective date {2024: '2023-09-06', 2025: '2024-09-18', 2026: '2025-12-06', 2027: '2026-08-13'}; committee items = markup date when printed, else Local Budget Act date
- mapping: Table XX0-5 lines before 'Mayor's Proposed Budget' -> budget_proposed; lines between it and 'District's Approved Budget' -> budget_revised (Council changes); FY2027 Council-level changes taken from the activity-level Council chart instead of JA0-5 to avoid double counting
- coverage (stage[+funds] by FY x agency JA0/FO0/RM0/DB0/HY0/CF0/HG0):
| FY2021 | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds |
| FY2022 | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds |
| FY2023 | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds |
| FY2024 | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds |
| FY2025 | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds,prop | actu+funds,appr+funds | actu+funds,appr+funds |
| FY2026 | appr+funds,prop | appr+funds,prop | appr+funds | appr+funds | appr+funds,prop | appr+funds | appr+funds |
| FY2027 | appr+funds | appr+funds | appr+funds,prop | appr+funds | appr+funds,prop | appr+funds | appr+funds |
- warnings (0):

### 2026-10-10 16:54 — 38_parse_hud_counts
- wrote interim/stage_homeless_counts__hud.csv: 49,393 rows ({'bulk_hud_ahar_pit_hic': 48224, 'doc_hud_hic_dc500': 428, 'doc_mwcog_pit': 741}); PIT 39,029, HIC by CoC 9,195, PopSub 428, MWCOG 741
- wrote interim/stage_hic_projects__hud.csv: 1,257 rows (2022: 332, 2023: 292, 2024: 323, 2025: 310)
- HIC project PDFs: provider and facility names are truncated in the PDF itself (fixed-width report cells; same text in pdfplumber chars, pypdf and pdftotext); kept as printed. 'units' = family units (HIC reports units only for households with children). target_population is derived from the bed columns (household type, plus youth/veterans/chronic when all beds are dedicated) and set to single_women / women_with_children only when the provider or project name says women (basis in x_target_population_basis). x_women_focused_org = core peer tier 1a or Calvary; x_dv_focused_org = tier 1b (config/core_peers.csv).
- PIT by CoC (raw/hud/20261010T123731_huduser_2007-2025-PIT-Counts-by-CoC.xlsb): sheets 2007-2025; 39,029 rows for 8 CoCs; unparsed column names 216 (e.g. ['Overall Homeless - Under 18', 'Overall Homeless - Age 18 to 24', 'Overall Homeless - Over 24']); CoC-years absent: none
- partial unsheltered counts (Count Types): MD-601 2021; VA-602 2021
- workbook has no gender columns in any year (only age, race/ethnicity, household and subpopulation splits); DC gender comes from PopSub 2024 and the MWCOG 2025 DC narrative
- HIC by CoC (raw/hud/20261010T123733_huduser_2007-2025-HIC-Counts-by-CoC.xlsx): sheets 2007-2025; 9,195 rows; unparsed columns 9 (['HMIS Participation Rate (ES,TH) (non-numeric)', 'ES HMIS Participation Rate (non-numeric)', 'Total TH Beds for Households with only Children (non-numeric)', 'HMIS Participation Rate for Year-Round Beds (SH) (non-numeric)']); same-measure columns with different values kept as '__alt': 0
- PopSub DC-500 2024 (raw/hud/20261010T123749_hudx_CoC_PopSub_DC-500_2024.pdf): 232 rows; total persons 5616; women 2167
- PopSub DC-500 2025 (raw/hud/20261010T123750_hudx_CoC_PopSub_DC-500_2025.pdf): 196 rows; total persons 5138; women n/a
- MWCOG 2023 report (raw/hud/20261010T123754_mwcog_homelessness_metro_washington_2023_PIT.pdf): 548 table cells kept
- MWCOG 2024 report (raw/hud/20261010T123753_mwcog_homelessness_metro_washington_2024_PIT.pdf): 504 table cells kept
- MWCOG 2025 report (raw/hud/20261010T123752_mwcog_homelessness_metro_washington_2025_PIT.pdf): 520 table cells kept
- MWCOG 2026 report (raw/hud/20261010T123751_mwcog_homelessness_metro_washington_2026_PIT.pdf): 531 table cells kept
- MWCOG: 2103 cells parsed across reports -> 741 after keeping the latest report per jurisdiction/year/measure/population; values revised between reports: 38 (e.g. Prince William County, VA 2022 all: 241 (rpt 2023) -> 282 (rpt 2024); Prince William County, VA 2021 all: 282 (rpt 2023) -> 326 (rpt 2024); Prince William County, VA 2020 all: 326 (rpt 2023) -> 277 (rpt 2024); COG region 2023 households_without_children: 5901 (rpt 2023) -> 5755 (rpt 2024)); same report, two tables disagree (earlier page kept): 17 (District of Columbia 2020 households_with_only_children rpt 2023: p68 12 vs p25 11; Frederick City & County, MD 2021 households_with_only_children rpt 2023: p68 5 vs p25 0; COG region 2020 households_with_only_children rpt 2023: p69 13 vs p25 12; City of Alexandria, VA 2020 all rpt 2023: p68 198 vs p17 207)
- skipped tables (did not parse reliably): none; source-inconsistent columns are kept with confidence medium and an x_note
- not parsed: figures/charts (demographic profiles, income, gender charts), Table 3 population shares, Table 13/14 shelter status, TAY tables, Table 16 bed inventory, Table 17 formerly homeless in PH, Appendix B narrative percentages except the 2025 DC gender-of-adults table
- HIC provider names (cleaned, distinct): 105; matched 42 (40%); methods {'unmatched': 63, 'fuzzy_token_set': 10, 'exact_norm_name': 29, 'manual_known_ein': 2, 'manual_alias': 1}; government providers (no EIN expected) 7; beds at matched providers 67,567 of 133,181 (51%)
- fuzzy matches: Access Housing -> 521918702 (100.0); Access Housing INC (AHI) (Agency) -> 521918702 (100.0); Catholic Charities -> 530196524 (100.0); Catholic Charities (Agency) -> 530196524 (100.0); Covenant House Washington -> 133537709 (100.0); Covenant House Washington (CHW)(Age -> 133537709 (100.0); East River Family Strengthening Collabor -> 522277915 (100.0); Edgewood-Brookland Family Support Col -> 522246995 (100.0); Edgewood/Brookland Family Support Col -> 522246995 (100.0); Far Southeast Family Strengthening Colla -> 522117070 (100.0); Georgia Avenue Family Support Collabor -> 522349433 (100.0); Survivors & Advocates for Empowerment -> 412226446 (100.0)
- unmatched nonprofit providers (not in dc_sector/dmv_sector/core_peers by name): 801 East Collaborative; Bradley & Associates; CCDC; CORE DC; Casa Ruby; Church of Epiphany; Church of the Epiphany; Collaborative Solutions for Communities; Communities Helping & Empowering Pat; Communities Helping and Empowering P; Community Solutions; Cornerstone Community; Dawn Deaf; Deaf Dawn; East of the River Family Support Collabor; Echelon Community Services; Far Southeast Family Support Collaborati; Healthy Babies; Healthy Babies Project; Hillcrest Children & Family Center; Hope and a Home; Institute for Emotional Regulation; Jaydot; Joseph's House; Jubilee Housing; KBEC Group, Inc; KBEC Group, Inc.; KC Community Services; Latin American Youth Center; MBI Health Services; Maximus; Metropolitan Education Solutions; Metropolitan Educational Solutions; North Capitol Collaborative Inc.; North Capitol Family Support Collaborati; Operation Renewed Hope; Positive Kinship Bonding; SLS; SMYAL; Salvation Army; Sasha Bruce Youthwork; Sasha Bruce Youthworks; So Others Might Eat; Spring Leaf; St. Aloysius Roman Catholic Church; St. John's Community Community Servic; St. John's Community Services; Supporting & Mentoring Youth Advocate; Temple Micah; Temple Sinai; The Community Builders and Emory Bea; The Institute for Emotional Regulation, L; The Salvation Army; U.S. Vets; US Veterans Initiative; Wheeler Creek
- matcher (shared with script 36): manual aliases (TCP 521681401; DASH, DC SAFE, Housing Up), norm_name exact, then rapidfuzz token_set_ratio >= 92 (after expanding a truncated last token for raw names >= 30 chars) accepted only when fuzzy_ok() holds: both names >= 2 tokens, a shared non-generic token, no one-sided entity-marker token (foundation, fund, maryland, county, ...), and token containment (ratio >= 0.5) or prefix or only soft one-sided words or fuzz.ratio >= 90; reviewed reject list
- PopSub 2024 gender rows sum 5616 vs total 5616: pass
- MWCOG 2023 p16 'People Experiencing Literal Homelessness by Jurisdiction, 2022 - 2023': pass (2 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p17 'People Experiencing Literal Homelessness by Jurisdiction, 2019-2023': pass (5 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p22 '2023 Persons In Families Experiencing Homelessness by Jurisdiction': pass (4 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p23 'Change In Persons In Families Experiencing Homelessness by Jurisdictio': pass (5 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p25 'Households With Only Children Under Age 18 By Jurisdiction, 2020 - 202': pass (4 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p41 'Comparison of Unsheltered Single Adults By Jurisdiction, 2019 – 2023': pass (5 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p45 'Single Adults Experiencing Chronic Homelessness by Jurisdiction, 2019 ': pass (5 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p51 'Veterans Experiencing Homelessness By Jurisdiction, 2019 - 2023': pass (5 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 pp[68, 69] 'People Experiencing Literal Homelessness by Jurisdiction, 20': kept with flags: 14/20 columns do not add up in the source (2022 households_without_children 5,307 vs 5,273; 2022 households_with_adults_and_children 2,329 vs 2,322; 2022 all 7,646 vs 7,605); 2 jurisdiction-years whose household columns do not add up
- MWCOG 2024 p16 'People Experiencing Literal Homelessness by Jurisdiction, 2023 - 2024': pass (2 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p17 'People Experiencing Literal Homelessness by Jurisdiction, 2020-2024*': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p22 '2024 Persons in Families Experiencing Homelessness by Jurisdiction': pass (4 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p23 'Change in Persons in Families Experiencing Homelessness by Jurisdictio': kept with flags: 1/5 columns do not add up in the source (2020 persons_in_families 3,690 vs 3,760)
- MWCOG 2024 p29 'Households With Only Children Under Age 18 By Jurisdiction, 2020 - 202': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p49 'Unsheltered Single Adults Experiencing Homelessness by Jurisdiction, 2': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p52 'Single Adults Experiencing Chronic Homelessness by Jurisdiction, 2020 ': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p60 'Veterans Experiencing Homelessness by Jurisdiction, 2020 - 2024': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 pp[75, 76] 'People Experiencing Literal Homelessness by Jurisdiction, 20': kept with flags: 9/20 columns do not add up in the source (2022 households_without_children 5,154 vs 5,120; 2022 households_with_adults_and_children 2,272 vs 2,265; 2022 all 7,422 vs 7,395); 2 jurisdiction-years whose household columns do not add up
- MWCOG 2025 p17 'People Experiencing Literal Homelessness by Jurisdiction, 2024 - 2025': pass (2 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p18 'People Experiencing Literal Homelessness by Jurisdiction, 2021-2025*': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p22 '2025 Persons in Families Experiencing Homelessness by Jurisdiction': pass (4 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p23 'Change in Persons in Families Experiencing Homelessness by Jurisdictio': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p29 'Households With Only Children Under Age 18 By Jurisdiction, 2021 - 202': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p48 'Comparison of Unsheltered Single Adults by Jurisdiction, 2021 - 2025': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p51 'Single Adults Experiencing Chronic Homelessness by Jurisdiction, 2021 ': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p59 'Veterans Experiencing Homelessness by Jurisdiction, 2021 - 2025': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 pp[73, 74] 'People Experiencing Literal Homelessness by Jurisdiction, 20': pass (20 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p18 'People Experiencing Literal Homelessness by Jurisdiction, 2025-2026': pass (2 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p19 'People Experiencing Literal Homelessness by Jurisdiction, 2019-2026': pass (8 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p24 '2026 Persons in Families Experiencing Homelessness by Jurisdiction': pass (4 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p25 'Change in Persons in Families Experiencing Homelessness by Jurisdictio': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p32 'Households With Only Children Under Age 18 By Jurisdiction, 2022 – 202': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p50 'Comparison of Unsheltered Single Adults by Jurisdiction, 2022 – 2026': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p54 'Single Adults Experiencing Chronic Homelessness by Jurisdiction, 2022 ': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p59 'Veterans Experiencing Homelessness by Jurisdiction, 2022 – 2026': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 pp[79, 80] 'People Experiencing Literal Homelessness by Jurisdiction, 20': pass (20 year/measure columns, 8 jurisdictions + total)
- MWCOG total persons vs HUD PIT overall, CoC-years that differ: 9: MD-600 2020: MWCOG 453 vs HUD 466; MD-600 2021: MWCOG 537 vs HUD 535; MD-600 2022: MWCOG 571 vs HUD 533; MD-600 2023: MWCOG 659 vs HUD 595; MD-600 2024: MWCOG 658 vs HUD 650; MD-600 2025: MWCOG 608 vs HUD 588; VA-602 2019: MWCOG 169 vs HUD 167; VA-604 2019: MWCOG 277 vs HUD 280; VA-604 2025: MWCOG 392 vs HUD 393
- DC-500 MWCOG vs HUD by year: 2019 6,521/6521, 2020 6,380/6380, 2021 5,111/5111, 2022 4,410/4410, 2023 4,922/4922, 2024 5,616/5616, 2025 5,138/5138, 2026 5,363/n/a
- stage_homeless_counts duplicate keys (coc, jurisdiction, year, measure, population, source): 0
- DC-500 2025 recon values: pit_overall 5138 (exp 5138) pass; pit_sheltered_es 3275 (exp 3275) pass; pit_sheltered_th 1065 (exp 1065) pass; pit_unsheltered 798 (exp 798) pass; hic_beds_year_round__es_th_sh 4965 (exp 4965) pass; hic_beds_year_round__th 1385 (exp 1385) pass; hic_beds_year_round__psh 12696 (exp 12696) pass; hic_beds_year_round__rrh 6012 (exp 6012) pass
- HIC projects 2022 ES: 43 projects; total beds 5,159 vs Total row 5159; year-round 4,795 vs summary p1 4795 vs CoC workbook 4795: pass
- HIC projects 2022 SH: 1 projects; total beds 20 vs Total row 20; year-round 20 vs summary p1 20 vs CoC workbook 20: pass
- HIC projects 2022 TH: 71 projects; total beds 1,783 vs Total row 1783; year-round 1,783 vs summary p1 1783 vs CoC workbook 1783: pass
- HIC projects 2022 PSH: 148 projects; total beds 14,467 vs Total row 14467; year-round 14,467 vs summary p1 14467 vs CoC workbook 14467: pass
- HIC projects 2022 RRH: 34 projects; total beds 7,193 vs Total row 7193; year-round 7,193 vs summary p1 7193 vs CoC workbook 7193: pass
- HIC projects 2022 OPH: 35 projects; total beds 6,498 vs Total row 6498; year-round 6,498 vs summary p1 6498 vs CoC workbook 6498: pass
- HIC projects 2023 ES: 38 projects; total beds 4,026 vs Total row 4026; year-round 3,720 vs summary p1 3720 vs CoC workbook 3720: pass
- HIC projects 2023 SH: 1 projects; total beds 20 vs Total row 20; year-round 20 vs summary p1 20 vs CoC workbook 20: pass
- HIC projects 2023 TH: 65 projects; total beds 1,476 vs Total row 1476; year-round 1,476 vs summary p1 1476 vs CoC workbook 1476: pass
- HIC projects 2023 PSH: 138 projects; total beds 15,349 vs Total row 15349; year-round 15,349 vs summary p1 15349 vs CoC workbook 15349: pass
- HIC projects 2023 RRH: 35 projects; total beds 9,206 vs Total row 9206; year-round 9,206 vs summary p1 9206 vs CoC workbook 9206: pass
- HIC projects 2023 OPH: 15 projects; total beds 5,381 vs Total row 5381; year-round 5,381 vs summary p1 5381 vs CoC workbook 5381: pass
- HIC projects 2024 ES: 46 projects; total beds 4,000 vs Total row 4000; year-round 3,505 vs summary p1 3505 vs CoC workbook 3505: pass
- HIC projects 2024 SH: 1 projects; total beds 20 vs Total row 20; year-round 20 vs summary p1 20 vs CoC workbook 20: pass
- HIC projects 2024 TH: 70 projects; total beds 1,693 vs Total row 1693; year-round 1,693 vs summary p1 1693 vs CoC workbook 1693: pass
- HIC projects 2024 PSH: 154 projects; total beds 11,856 vs Total row 11856; year-round 11,856 vs summary p1 11856 vs CoC workbook 11856: pass
- HIC projects 2024 RRH: 33 projects; total beds 10,156 vs Total row 10156; year-round 10,156 vs summary p1 10156 vs CoC workbook 10156: pass
- HIC projects 2024 OPH: 19 projects; total beds 5,842 vs Total row 5842; year-round 5,842 vs summary p1 5842 vs CoC workbook 5842: pass
- HIC projects 2025 ES: 45 projects; total beds 3,954 vs Total row 3954; year-round 3,580 vs summary p1 3580 vs CoC workbook 3580: pass
- HIC projects 2025 TH: 64 projects; total beds 1,385 vs Total row 1385; year-round 1,385 vs summary p1 1385 vs CoC workbook 1385: pass
- HIC projects 2025 PSH: 159 projects; total beds 12,696 vs Total row 12696; year-round 12,696 vs summary p1 12696 vs CoC workbook 12696: pass
- HIC projects 2025 RRH: 26 projects; total beds 6,012 vs Total row 6012; year-round 6,012 vs summary p1 6012 vs CoC workbook 6012: pass
- HIC projects 2025 OPH: 16 projects; total beds 4,989 vs Total row 4989; year-round 4,989 vs summary p1 4989 vs CoC workbook 4989: pass
- stage_hic_projects duplicate keys (year, type, page, seq): 0
- Calvary HIC 2025 rows pass (7 projects, 124 beds); 2024 Sisters Rise PSH [24] (exp [24])

### 2026-10-10 16:54 — 33_pull_usaspending: stage fact_gov_awards
- interim/stage_fact_gov_awards__federal.csv: 28207 rows; {"named_job_rows_dropped": 1, "usaspending_sub_reports": 11875, "usaspending_prime": 7163, "usaspending_sub": 10733, "fac_reports_kept": 1841, "fac_reports_used": 1831, "fac_lines": 9851, "fac_reports_identical_sefa": 18, "slfrf_dc_report_rows": 462, "slfrf_dc_rows": 461, "named_comparators": {"311597223": {"rows": 51, "by_source_flow": {"usaspending/prime": 2, "usaspending/subaward": 17, "fac_sefa/pass_through_expenditure": 30, "fac_sefa/prime": 2}, "fac_audit_years": ["2020", "2021", "2022", "2023", "2024", "2025"], "fac_expenditure_by_fy": {"2020": 1043889, "2021": 2781894, "2022": 6904511, "2023": 3279830, "2024": 4249604, "2025": 3358800}, "usaspending_amount": 8294415}, "882046704": {"rows": 0, "by_source_flow": {}, "fac_audit_years": [], "fac_expenditure_by_fy": {}, "usaspending_amount": 0}}, "rows": 28207, "duplicate_ids": 0, "rows_missing_provenance": 0, "by_source_flow": {"usaspending/prime": 7162, "usaspending/subaward": 10733, "fac_sefa/prime": 4492, "fac_sefa/pass_through_expenditure": 5359, "treasury_slfrf/subaward": 461}, "ein_filled": 23149}
- Calvary reconciliation: {"fac_fy22_total": 4067718, "fac_fy22_ok": true, "fac_ay2023_total": 4064718, "fac_ay2023_conflict_rows": 4, "hud_14251": [200000], "hud_ok": true, "ppp": [327200], "usaspending_subawards": [["14.252", 25000]], "slfrf": [113488, 3680675], "slfrf_ok": true, "calvary_rows": 13}
- EIN coverage (scope = calvary, core_peers, dc_sector, dmv_sector): {"scope_orgs": 4920, "orgs_with_any_row_by_ein": 234, "by_source": {"usaspending": 185, "fac_sefa": 234, "treasury_slfrf": 2}, "extra_orgs_by_exact_name_state_candidate_only": 60}

### 2026-10-10 16:55 — 35_pull_grantsgov: opportunities
- universe posted+forecasted 1467; candidates 531 (local cfdaList 3, cfda key 3, keyword search 530, title regex 51); fetched 0 (reused 531 saved responses); fetch failures 0; dropped by local filter 245
- interim/stage_fact_opportunities__grantsgov.csv: 286 rows (173 posted, 113 forecasted); duplicate ids 0
- keyword_hits counts: {"homelessness": 6, "housing": 17, "domestic violence": 5, "victim services": 2, "women": 59, "substance use": 47, "workforce": 98, "reentry": 5, "veterans": 19, "aging": 77}
- target-ALN rows: 3; nonprofit-eligible (12/13/25/99): 263
- manifest raw/grantsgov/20261010T165513_pull35_manifest.json

### 2026-10-10 16:56 — 41_pull_soi_extracts: stage
- universe EINs: 15,812
- 990 2012 (12eofinextract990.zip): 294,019 rows read, 2,255 universe rows; fields absent this year: grants_paid, compensation_total, cash_savings_eoy
- 990 2013 (13eofinextract990.zip): 289,603 rows read, 2,255 universe rows
- 990 2014 (14eofinextract990.zip): 299,405 rows read, 2,334 universe rows
- 990 2015 (15eofinextract990.zip): 294,782 rows read, 2,252 universe rows
- 990 2016 (16eofinextract990.zip): 307,483 rows read, 2,421 universe rows
- 990 2017 (17eofinextract990.zip): 300,910 rows read, 2,426 universe rows
- 990 2018 (18eoextract990.zip): 313,339 rows read, 2,514 universe rows
- 990 2019 (19eoextract990.zip): 304,441 rows read, 2,520 universe rows
- 990 2020 (20eoextract990.zip): 273,971 rows read, 2,294 universe rows
- 990 2021 (21eoextract990.zip): 342,920 rows read, 2,874 universe rows
- 990 2022 (22eoextract990.zip): 326,123 rows read, 2,802 universe rows
- 990 2023 (23eoextract990.zip): 338,048 rows read, 2,831 universe rows
- 990 2024 (24eoextract990.zip): 345,365 rows read, 2,985 universe rows
- 990EZ 2012 (12eofinextract990ez.zip): 223,348 rows read, 593 universe rows
- 990EZ 2013 (13eofinextract990ez.zip): 218,981 rows read, 613 universe rows
- 990EZ 2014 (14eofinextract990ez.zip): 234,820 rows read, 659 universe rows
- 990EZ 2015 (15eofinextractEZ.zip): 223,028 rows read, 669 universe rows
- 990EZ 2016 (16eofinextractez.zip): 230,745 rows read, 738 universe rows
- 990EZ 2017 (17eofinextractEZ.zip): 218,097 rows read, 731 universe rows
- 990EZ 2018 (18eoextractez.zip): 226,533 rows read, 766 universe rows
- 990EZ 2019 (19eoextractez.zip): 218,671 rows read, 777 universe rows
- 990EZ 2020 (20eoextractez.zip): 154,314 rows read, 536 universe rows
- 990EZ 2021 (21eoextractez.zip): 218,733 rows read, 867 universe rows
- 990EZ 2022 (22eoextractez.zip): 231,289 rows read, 990 universe rows
- 990EZ 2023 (23eoextractez.zip): 207,536 rows read, 933 universe rows
- 990EZ 2024 (24eoextract990EZ.zip): 203,699 rows read, 986 universe rows
- 990PF 2012 (12eofinextract990pf.zip): 98,948 rows read, 2,671 universe rows; fields absent this year: x_pf_grants_approved_future
- 990PF 2013 (13eofinextract990pf.zip): 100,484 rows read, 2,755 universe rows
- 990PF 2014 (14eofinextract990pf.zip): 101,381 rows read, 2,904 universe rows
- 990PF 2015 (15eofinextract990pf.zip): 103,000 rows read, 2,935 universe rows
- 990PF 2016 (16eofinextract990pf.zip): 105,239 rows read, 3,131 universe rows
- 990PF 2020 (20eoextract990pf.zip): 91,473 rows read, 3,022 universe rows
- 990PF 2021 (21eoextract990pf.zip): 125,312 rows read, 4,417 universe rows
- 990PF 2022 (22eoextract990pf.zip): 115,024 rows read, 4,268 universe rows
- 990PF 2023 (23eoextract990pf.zip): 120,350 rows read, 4,589 universe rows
- 990PF 2024 (24eoextract990pf.zip): 119,059 rows read, 4,796 universe rows
- SOI: 78,109 rows, 9,446 EINs; 0 older-processing-year copies dropped; 0 rows whose copies disagree on total_revenue
- NCCS 2009: 48,857 rows read, 280 universe 990 rows
- NCCS 2010: 184,553 rows read, 932 universe 990 rows
- NCCS 2011: 241,595 rows read, 1,272 universe 990 rows
- NCCS 2012: 273,429 rows read, 1,485 universe 990 rows
- NCCS 2013: 303,225 rows read, 1,645 universe 990 rows
- NCCS 2014: 335,066 rows read, 1,783 universe 990 rows
- NCCS 2015: 358,459 rows read, 1,962 universe 990 rows
- NCCS 2016: 374,252 rows read, 2,045 universe 990 rows
- NCCS 2017: 391,170 rows read, 2,163 universe 990 rows
- NCCS 2018: 406,376 rows read, 2,255 universe 990 rows
- NCCS 2019: 436,217 rows read, 2,393 universe 990 rows
- NCCS 2020: 485,459 rows read, 2,675 universe 990 rows
- NCCS 2021: 491,127 rows read, 2,558 universe 990 rows
- NCCS 2022: 131,588 rows read, 350 universe 990 rows
- NCCS: 22,573 rows staged, 3,105 EINs, tax years 2010-2022; period from SOI match 22,555, from IRS index 18; dropped 901 with no period; 309 EIN-years had >1 return (kept the latest OBJECT_ID)
- NCCS total_revenue equals SOI total_revenue on 99.1% of 22,555 matched rows
- wrote 100,682 rows to interim/stage_fact_org_financials__soi.csv (SOI 78,109; NCCS 22,573)
- duplicate (ein, tax_period_end, return_type, source_id): 0
- Calvary total_revenue QC: bulk_irs_soi_extract TY2020 3,851,984 OK; bulk_irs_soi_extract TY2021 8,867,250 OK; bulk_nccs_efile TY2020 3,851,984 OK; bulk_nccs_efile TY2021 not present
- 990-PF SOI TAX_YR equals derived tax_year on 100.0% of rows
- rows by fiscal_year (period-end year) x return_type / source:
```
source_id   irs_soi_extract              nccs_efile     All
return_type             990 990EZ  990PF        990        
fiscal_year                                                
2002                      0     0      1          0       1
2003                      1     0      1          0       2
2004                      0     0      1          0       1
2005                      1     0      1          0       2
2006                      0     0      1          0       1
2007                      0     2      3          0       5
2008                      2    12      7          0      21
2009                      4    30     14          0      48
2010                    179    93     84          5     361
2011                   1876   519   2408        826    5629
2012                   2227   624   2756       1381    6988
2013                   2279   626   2831       1558    7294
2014                   2299   670   2974       1662    7605
2015                   2365   708   3040       1856    7969
2016                   2445   739    310       1979    5473
2017                   2494   750     23       2078    5345
2018                   2566   763    110       2181    5620
2019                   2625   802   3462       2303    9192
2020                   2649   848   3905       2539    9941
2021                   2761   833   4206       2685   10485
2022                   2852   872   4435       1513    9672
2023                   2862   882   4560          7    8311
2024                    276    85    355          0     716
All                   32763  9858  35488      22573  100682
```
- coverage, bulk_irs_soi_extract (EINs with >=1 row / universe EINs; org-years; median years per covered org):
  - calvary: 1/1; 13; 13
  - calvary_known_funders: 83/87; 867; 10
  - core_peers: 18/18; 235; 13
  - daf_sponsors: 15/15; 184; 13
  - dc_sector: 524/1,027; 4,620; 11
  - dmv_funders: 5,744/7,705; 44,487; 10
  - dmv_sector: 1,942/4,910; 15,530; 9
  - named_comparators: 2/2; 14; 7
  - national_women: 1,395/2,878; 13,420; 12
  - size_matched: 564/566; 6,892; 13
- coverage, bulk_nccs_efile (EINs with >=1 row / universe EINs; org-years; median years per covered org):
  - calvary: 1/1; 7; 7
  - calvary_known_funders: 32/87; 259; 10
  - core_peers: 18/18; 172; 10
  - daf_sponsors: 15/15; 84; 6
  - dc_sector: 370/1,027; 2,550; 7
  - dmv_funders: 650/7,705; 4,046; 6
  - dmv_sector: 1,140/4,910; 7,857; 7
  - named_comparators: 1/2; 11; 11
  - national_women: 959/2,878; 7,769; 9
  - size_matched: 558/566; 4,840; 10

### 2026-10-10 16:56 — 42_pull_propublica: stage
- 2,538 org JSONs read (0 target EINs with no ProPublica record); 18,279 filings_with_data rows; skipped formtypes {}; 0 bad periods
- tax_prd_yr equals derived fiscal_year (period-end year) on 100.0% of rows
- staged 18,279 rows, 2,004 EINs -> interim/stage_fact_org_financials__propublica.csv; duplicates on (ein, tax_period_end, return_type, source_id): 0
- Calvary total_revenue QC: TY2020 3,851,984 OK; TY2021 8,867,250 OK
- cross-check vs SOI: 18,279 matching (ein, period, form) rows; equal total_revenue 100.0%, total_expenses 100.0%, total_assets_eoy 100.0%
- ProPublica rows with no SOI row: 0 (by fiscal_year {})
- rows by fiscal_year x return_type:
```
return_type   990  990EZ  990PF    All
fiscal_year                           
2007            0      1      1      2
2008            0      1      1      2
2009            0      3      4      7
2010           53     20     20     93
2011          392     61    812   1265
2012          440     70    936   1446
2013          448     65    960   1473
2014          448     66    999   1513
2015          465     72   1017   1554
2016          476     66    107    649
2017          484     69      4    557
2018          493     71     15    579
2019          513     73   1082   1668
2020          511     75   1182   1768
2021          536     74   1229   1839
2022          550     69   1245   1864
2023          550     76   1243   1869
2024           28      4     99    131
All          6387    936  10956  18279
```

### 2026-10-10 16:56 — 46_web_named_comparators (stage)
- staged 396 rows -> interim/stage_fact_grants__web_named.csv (exact duplicates dropped 1); recipients {'311597223': 391, '882046704': 5}
- by source_type {'annual_report': 350, 'support_page': 33, 'web': 13}; amount_kind {'unknown': 353, 'mixed': 33, 'cash': 8, 'noncash': 2}; with amount 8, with band 354
- by fiscal_year {2023: 204, 2024: 2, 2025: 155, 2026: 35}
- non-organization entries counted per band only: 570 -> interim/web_named_donor_band_counts.csv; joint credits with a personal name: 6 trimmed to the organization, 1 dropped
- per page (entries, kept, dropped as non-org, status): nc_dwc_ar_2024 669/203/422/ok; nc_dwc_ar_web 277/148/112/ok; nc_dwc_gala_2025 26/4/18/ok; nc_dwc_gala_2026 54/29/18/ok; nc_dwc_rosas_place_pr 1/1/0/ok; nc_dwc_hilton_2026 1/1/0/ok; nc_dwc_ahmanson_grants 2/2/0/ok; nc_dwc_bscf_grantee 1/1/0/ok; nc_dwc_foxwynd 1/1/0/ok; nc_dwc_anthem_2023 1/1/0/ok; nc_dwc_anthem_2026_dwc_pr 1/1/0/ok; nc_cbw_sheworks 1/1/0/ok; nc_cbw_launch_pr 1/1/0/ok; nc_cbw_lacare_pr 2/2/0/ok; nc_cbw_econ_mobility 1/1/0/ok
- this run: Tavily search 0, extract 0, HTTP GET 0, cache hits 0; cumulative (manifest): search 139/300, extract 15/200, HTTP 150; script-46 totals: search 30/30, extract 5/15

### 2026-10-10 16:56 — 45_stage_web_grants
- staged rows 1015: by source_type {'support_page': 249, 'annual_report': 630, 'web': 136}; confidence {'medium': 988, 'high': 27}
- amount stated 34; band only 392; unknown 589
- recipient Calvary 268; core peers 739 (14 peers); whole-list keyword keeps 8
- Calvary-site rows by type {'support_page': 98, 'annual_report': 74, 'anonymous_skipped': 1, 'web': 90}
- pages parsed 20/65; not parsed or failed: nsv_funding_reports (index page (links to annual reports)); openarms_about (no funder list on the site); nebw_reports (index page (links to annual reports)); nebw_ar_2025 (2025 annual report text has no funder list); msp_ar_fy22 (no funder list); dcsafe_ar_fy25 (no funder list (revenue split only)); nuvaya_fin_reports (HTTP 403 and Tavily extract empty); christhouse_ar_2025 (landing page; PDF has no text layer); christhouse_ar_2025_pdf (image-only PDF (12 chars of text)); ehdc_ar_2024 (landing page); ehdc_ar_2024_pdf (2024 annual report text has no funder list); cfh_ar_list (index page); thrive_impact_2024 (lists corporate volunteer groups, not funders); miriams_financials (index page); miriams_ar_fy25 (mkannualreport.org is JavaScript-rendered; no text retrieved); coh_ar_2025 (2025 annual report summary has no funder list); coh_impact_2024 (same list as coh_funders (parsed there)); chgw_home (home page); chgw_impact_fy24 (FY24 impact report text has no funder list); doorways_ar_2023 (landing page); doorways_ar_2023_issuu (issuu viewer; no document text); hormd_honor_roll (URL now serves the About Us page; no honor roll content); hormd_honor_roll_tav (Tavily advanced extract also returns no honor roll content); hormd_ar_2024 (PDF returns HTTP 404); hormd_ar_page (annual report page has no donor list); meyer_118m_28 (2020 list (outside 2024-2026); no Calvary or peers); meyer_635k_8 (2022 list (outside 2024-2026); no Calvary or peers); meyer_rapid (program description only; no 
- in-kind evidence rows 17: MGAC=unclear; MGAC=in_kind; MGAC=in_kind; MGAC=cash; Health Equity Fund=cash; Health Equity Fund=cash; Health Equity Fund=cash; Health Equity Fund=cash; Capital One=unclear; Capital One=unclear; Capital One=cash; World Bank Community Connections Fund=cash; World Bank Community Connections Fund=cash; World Bank Community Connections Fund=cash; Frontier Co-op / Aura Cacia (Frontier Co-op Giving Fund)=in_kind; Frontier Co-op / Aura Cacia (Frontier Co-op Giving Fund)=unclear; MGAC; Capital One; World Bank Community Connections Fund=unclear
- Tavily usage to date (manifest, scripts 43-44): search 139/300, extract 15/200; plus 1 exploratory search during development (same query as cal_audit_fy24; response not saved). HTTP GETs 150.
- appended notes_for_analysis.md 'Web funder data' and open_questions.md

### 2026-10-10 16:56 — 50_parse_xml: progress
- 2,000/31,483 parsed in 0.5 min; grants 698,214, roles 22,703, relationships 5,719; errors 0

### 2026-10-10 16:57 — 50_parse_xml: progress
- 4,000/31,483 parsed in 0.6 min; grants 764,178, roles 41,319, relationships 9,850; errors 0

### 2026-10-10 16:57 — 50_parse_xml: progress
- 6,000/31,483 parsed in 0.6 min; grants 804,949, roles 56,969, relationships 10,909; errors 0

### 2026-10-10 16:57 — 50_parse_xml: progress
- 8,000/31,483 parsed in 0.6 min; grants 833,478, roles 71,614, relationships 11,579; errors 0

### 2026-10-10 16:57 — 50_parse_xml: progress
- 10,000/31,483 parsed in 0.7 min; grants 855,931, roles 83,719, relationships 11,966; errors 0

### 2026-10-10 16:57 — 50_parse_xml: progress
- 12,000/31,483 parsed in 0.7 min; grants 872,756, roles 94,450, relationships 12,310; errors 0

### 2026-10-10 16:57 — 50_parse_xml: progress
- 14,000/31,483 parsed in 0.7 min; grants 885,831, roles 104,143, relationships 12,537; errors 0

### 2026-10-10 16:57 — 50_parse_xml: progress
- 16,000/31,483 parsed in 0.7 min; grants 896,903, roles 112,869, relationships 12,668; errors 0

### 2026-10-10 16:57 — 50_parse_xml: progress
- 18,000/31,483 parsed in 0.8 min; grants 906,213, roles 120,818, relationships 12,795; errors 0

### 2026-10-10 16:57 — 50_parse_xml: progress
- 20,000/31,483 parsed in 0.8 min; grants 913,736, roles 128,324, relationships 12,858; errors 0

### 2026-10-10 16:57 — 50_parse_xml: progress
- 22,000/31,483 parsed in 0.8 min; grants 919,348, roles 135,226, relationships 12,862; errors 0

### 2026-10-10 16:57 — 50_parse_xml: progress
- 24,000/31,483 parsed in 0.8 min; grants 923,248, roles 141,620, relationships 12,864; errors 0

### 2026-10-10 16:57 — 50_parse_xml: progress
- 26,000/31,483 parsed in 0.8 min; grants 925,353, roles 148,088, relationships 12,864; errors 0

### 2026-10-10 16:57 — 50_parse_xml: progress
- 28,000/31,483 parsed in 0.8 min; grants 926,494, roles 154,519, relationships 12,864; errors 0

### 2026-10-10 16:57 — 50_parse_xml: progress
- 30,000/31,483 parsed in 0.9 min; grants 926,838, roles 160,722, relationships 12,864; errors 0

### 2026-10-10 16:57 — 50_parse_xml: done
- parsed 31,483 of 31,483 returns in 0.9 min; errors 0 -> xml_parse_errors.csv
- interim/stage_fact_org_financials__xml.csv: 31,483 rows {'990PF': 24877, '990': 4872, '990EZ': 1734}; amended 335; EIN differs from index 0
- interim/stage_fact_grants__xml.csv: 926,887 rows
- interim/stage_fact_roles__xml.csv: 163,918 rows
- interim/stage_fact_org_relationships__xml.csv: 12,864 rows
- interim/org_profile__xml.csv: 31,483 rows (6,774 EINs; street kept on latest return only)
- interim/xml_schedule_i_part3.csv: 1,730 Schedule I Part III lines (aggregates, no names)
- schema versions: {'2014v5.0': 1, '2014v6.0': 1, '2015v2.1': 1, '2015v3.0': 1, '2016v3.0': 2, '2017v2.3': 2, '2018v3.1': 2, '2019v5.1': 1, '2019v5.2': 1, '2020v4.0': 1671, '2020v4.1': 2870, '2020v4.2': 423, '2021v4.0': 1467, '2021v4.1': 767, '2021v4.2': 3218, '2022v4.0': 4, '2022v4.1': 248, '2022v5.0': 5526, '2023v4.0': 271, '2023v5.0': 2462, '2023v5.1': 2421, '2023v6.0': 960, '2024v5.0': 1374, '2024v5.1': 1978, '2024v5.2': 2496, '2024v5.5': 372, '2025v4.0': 1220, '2025v4.1': 1441, '2025v4.2': 282}
- DAF1 sponsors, Schedule I kept only for DC/MD/VA recipients (all years in scope):
  - FIDELITY INVESTMENTS CHARITABLE GIFT FUND (110303001): national 372,180 rows / $58,823.5M; kept DMV 24,496 / $8,007.2M; filtered out $50,816.2M
  - DONOR ADVISED CHARITABLE GIVING INC (311640316): national 257,532 rows / $28,043.2M; kept DMV 17,453 / $4,001.7M; filtered out $24,041.5M
  - NATIONAL PHILANTHROPIC TRUST (237825575): national 83,803 rows / $26,775.7M; kept DMV 6,855 / $3,393.6M; filtered out $23,382.1M
  - VANGUARD CHARITABLE ENDOWMENT PROGRAM (232888152): national 113,808 rows / $12,077.0M; kept DMV 9,471 / $2,022.5M; filtered out $10,054.5M
  - AMERICAN ONLINE GIVING FOUNDATION INC (810739440): national 228,879 rows / $10,079.9M; kept DMV 15,079 / $1,159.3M; filtered out $8,920.6M
  - AMERICAN ENDOWMENT FOUNDATION (341747398): national 65,226 rows / $4,638.5M; kept DMV 5,501 / $441.8M; filtered out $4,196.7M
  - BANK OF AMERICA CHARITABLE GIFT FD (046010342): national 4 rows / $3,249.2M; kept DMV 0 / $0.0M; filtered out $3,249.2M
  - THE AYCO CHARITABLE FOUNDATION (141782466): national 21,612 rows / $2,375.6M; kept DMV 1,874 / $113.0M; filtered out $2,262.5M
  - Renaissance Charitable Foundation Inc (352129262): national 5 rows / $2,288.2M; kept DMV 0 / $0.0M; filtered out $2,288.2M
  - PAYPAL CHARITABLE GIVING FUND (450931286): national 47,570 rows / $1,897.4M; kept DMV 3,864 / $145.8M; filtered out $1,751.5M
  - CHARITIES AID FOUNDATION AMERICA (431634280): national 44,986 rows / $1,870.2M; kept DMV 3,095 / $204.6M; filtered out $1,665.5M
  - THE BLACKBAUD GIVING FUND (460942102): national 35,201 rows / $1,351.7M; kept DMV 2,007 / $135.2M; filtered out $1,216.5M
  - THE GOLDMAN SACHS CHARITABLE GIFT FUND (113813663): national 12,471 rows / $1,056.1M; kept DMV 1,077 / $131.3M; filtered out $924.9M
  - BNY MELLON CHARITABLE GIFT FUND C/O BNY MELLON NA (300748315): national 5,467 rows / $1,022.5M; kept DMV 466 / $17.6M; filtered out $1,004.9M
  - THE US CHARITABLE GIFT TRUST (311663020): national 12,033 rows / $883.9M; kept DMV 984 / $29.0M; filtered out $854.9M

### 2026-10-10 16:57 — 51_qc_xml
- fetch 100.00% of 31,483
- parse errors 0
- PF grants sum exact 99.96% of returns with grants (99.81% of all PF); named-grantee rows cover 93.8% of PF grant dollars
- Calvary revenue checks pass
- Cafritz EIN 526036989; TY2024 to Calvary $170,000
- Calvary grant rows 150 from 50 funders ($4,701,886)
- trace 20/20
- report -> interim/xml_qc.md

### 2026-10-10 16:57 — 60_stage_inputs
- stage_fact_org_financials__inputs.csv: 17 rows
- stage_fact_gov_awards__inputs.csv: 8 rows
- stage_fact_grants__inputs.csv: 360 rows
- stage_fact_roles__inputs.csv: 195 rows

### 2026-10-10 16:59 — 61_resolve_entities
- unique name keys 233,183; alias rows 232,203
- occurrences by method:
match_method  exact_ein  exact_name_city  exact_name_national  exact_name_state  fuzzy_name_city  known_funder  manual  manual_reject  unmatched
role                                                                                                                                            
funder           925013                0                  274                 0                0           227      50             23       3071
pass_through        686                0                 1936                 0                0             0      16              0      14243
recipient        212746           343542                  912             51757            27487             0      48              2     286832

### 2026-10-10 17:01 — 62_build_facts
- fact_org_financials: 150,461 rows
- fact_grants: 928,658 rows
- fact_gov_awards: 40,300 rows
- fact_opportunities: 286 rows
- fact_policy_events: 297 rows
- supp_calvary_individual_donor_bands.csv: copied from stage_supp_calvary_individual_donor_bands.csv
- supp_calvary_program_metrics.csv: copied from stage_supp_calvary_program_metrics.csv
- supp_calvary_strategic_targets.csv: copied from stage_supp_calvary_strategic_targets.csv
- supp_homeless_counts.csv: copied from stage_homeless_counts__hud.csv
- supp_hic_projects.csv: copied from stage_hic_projects__hud.csv
- supp_dc_budget_lines.csv: copied from stage_dc_budget_lines__dc.csv

### 2026-10-10 17:01 — 63_build_dims
- dim_org: 105,156 rows
- dim_funder: 8,929 rows
- dim_program_area: 13 rows
- dim_period: 28 rows
- dim_geo: 246 rows

### 2026-10-10 17:02 — 64_people_relationships
- fact_roles 163,473; dim_person 48,563 (multi-org 2,036); candidate_interlocks 1,270; fact_org_relationships 542,975 {'grant': 431364, 'daf_sponsor_grant': 90830, 'schedule_r_related': 12864, 'shared_board_member': 4162, 'pass_through_funding': 3755}

### 2026-10-10 17:02 — 63_build_dims
- dim_org: 105,156 rows
- dim_funder: 8,929 rows
- dim_program_area: 13 rows
- dim_period: 28 rows
- dim_geo: 246 rows

### 2026-10-10 17:04 — 70_quality_checks
- wrote reports/data_quality.md; duplicates []; portability issues []

### 2026-10-10 17:04 — 80_docs
- data_dictionary rows 542; undocumented columns 0; source_ids missing from registry: none

### 2026-10-10 17:10 — 22_match_known_funders
- names 243; outcomes {('corp_foundation', 'inferred'): 16, ('exact_name_state', 'yes'): 33, ('exact_name_unique', 'yes'): 19, ('fuzzy_name_state', 'yes'): 6, ('manual', 'inferred'): 5, ('manual', 'yes'): 12, ('manual_reject', 'no'): 10, ('unmatched', 'no'): 142}; accepted EINs 88

### 2026-10-10 17:11 — 20_build_universes
- calvary: 1 EINs
- calvary_known_funders: 88 EINs
- core_peers: 18 EINs
- daf_sponsors: 15 EINs
- dc_sector: 1,027 EINs
- dmv_funders: 7,705 EINs
- dmv_sector: 4,910 EINs
- named_comparators: 2 EINs
- national_women: 2,878 EINs
- size_matched: 566 EINs
- membership rows 17,210; distinct EINs 15,812; e-file rows 45,305; size band $2,483,998–$9,935,990; missing pins {'F3': [], 'DAF1': []}

### 2026-10-10 17:13 — 61_resolve_entities
- unique name keys 232,661; alias rows 231,681
- occurrences by method:
match_method  exact_ein  exact_name_city  exact_name_national  exact_name_state  fuzzy_name_city  known_funder  manual  manual_reject  unmatched
role                                                                                                                                            
funder           925013                0                  274                 0                0           227      59             23       3062
pass_through        686                0                 1936                 0                0             0      16              0      14243
recipient        212746           344289                  912             51873            27536             0      48              2     285903

### 2026-10-10 17:14 — 62_build_facts
- fact_org_financials: 150,461 rows
- fact_grants: 928,658 rows
- fact_gov_awards: 40,300 rows
- fact_opportunities: 286 rows
- fact_policy_events: 297 rows
- supp_calvary_individual_donor_bands.csv: copied from stage_supp_calvary_individual_donor_bands.csv
- supp_calvary_program_metrics.csv: copied from stage_supp_calvary_program_metrics.csv
- supp_calvary_strategic_targets.csv: copied from stage_supp_calvary_strategic_targets.csv
- supp_homeless_counts.csv: copied from stage_homeless_counts__hud.csv
- supp_hic_projects.csv: copied from stage_hic_projects__hud.csv
- supp_dc_budget_lines.csv: copied from stage_dc_budget_lines__dc.csv

### 2026-10-10 17:15 — 63_build_dims
- dim_org: 105,190 rows
- dim_funder: 8,928 rows
- dim_program_area: 13 rows
- dim_period: 28 rows
- dim_geo: 246 rows

### 2026-10-10 17:15 — 64_people_relationships
- fact_roles 163,473; dim_person 48,563 (multi-org 2,036); candidate_interlocks 1,270; fact_org_relationships 544,100 {'grant': 432489, 'daf_sponsor_grant': 90830, 'schedule_r_related': 12864, 'shared_board_member': 4162, 'pass_through_funding': 3755}

### 2026-10-10 17:16 — 63_build_dims
- dim_org: 105,190 rows
- dim_funder: 8,928 rows
- dim_program_area: 13 rows
- dim_period: 28 rows
- dim_geo: 246 rows

### 2026-10-10 17:16 — 64_people_relationships
- fact_roles 163,473; dim_person 48,563 (multi-org 2,036); candidate_interlocks 1,270; fact_org_relationships 544,100 {'grant': 432489, 'daf_sponsor_grant': 90830, 'schedule_r_related': 12864, 'shared_board_member': 4162, 'pass_through_funding': 3755}

### 2026-10-10 17:17 — 64_people_relationships
- fact_roles 163,473; dim_person 48,563 (multi-org 2,036); candidate_interlocks 1,270; fact_org_relationships 544,100 {'grant': 432489, 'daf_sponsor_grant': 90830, 'schedule_r_related': 12864, 'shared_board_member': 4162, 'pass_through_funding': 3755}

### 2026-10-10 17:18 — 64_people_relationships
- fact_roles 163,473; dim_person 48,563 (multi-org 2,036); candidate_interlocks 1,270; fact_org_relationships 544,100 {'grant': 432489, 'daf_sponsor_grant': 90830, 'schedule_r_related': 12864, 'shared_board_member': 4162, 'pass_through_funding': 3755}

### 2026-10-10 17:19 — 64_people_relationships
- fact_roles 163,473; dim_person 48,563 (multi-org 2,036); candidate_interlocks 1,270; fact_org_relationships 544,100 {'grant': 432489, 'daf_sponsor_grant': 90830, 'schedule_r_related': 12864, 'shared_board_member': 4162, 'pass_through_funding': 3755}

### 2026-10-10 17:19 — 64_people_relationships
- fact_roles 163,473; dim_person 48,563 (multi-org 2,036); candidate_interlocks 1,270; fact_org_relationships 544,100 {'grant': 432489, 'daf_sponsor_grant': 90830, 'schedule_r_related': 12864, 'shared_board_member': 4162, 'pass_through_funding': 3755}

### 2026-10-10 17:20 — 64_people_relationships
- fact_roles 163,473; dim_person 48,563 (multi-org 2,036); candidate_interlocks 1,270; fact_org_relationships 544,100 {'grant': 432489, 'daf_sponsor_grant': 90830, 'schedule_r_related': 12864, 'shared_board_member': 4162, 'pass_through_funding': 3755}

### 2026-10-10 17:21 — 64_people_relationships
- fact_roles 163,473; dim_person 48,563 (multi-org 2,036); candidate_interlocks 1,270; fact_org_relationships 544,100 {'grant': 432489, 'daf_sponsor_grant': 90830, 'schedule_r_related': 12864, 'shared_board_member': 4162, 'pass_through_funding': 3755}

### 2026-10-10 17:22 — 64_people_relationships
- fact_roles 163,473; dim_person 48,563 (multi-org 2,036); candidate_interlocks 1,270; fact_org_relationships 544,100 {'grant': 432489, 'daf_sponsor_grant': 90830, 'schedule_r_related': 12864, 'shared_board_member': 4162, 'pass_through_funding': 3755}

### 2026-10-10 17:22 — 63_build_dims
- dim_org: 105,190 rows
- dim_funder: 8,928 rows
- dim_program_area: 13 rows
- dim_period: 28 rows
- dim_geo: 246 rows

### 2026-10-10 17:24 — 70_quality_checks
- wrote reports/data_quality.md; duplicates []; portability issues []

### 2026-10-10 17:24 — 80_docs
- data_dictionary rows 542; undocumented columns 0; source_ids missing from registry: none

### 2026-10-10 17:25 — 63_build_dims
- dim_org: 105,190 rows
- dim_funder: 8,928 rows
- dim_program_area: 13 rows
- dim_period: 28 rows
- dim_geo: 246 rows

### 2026-10-10 17:27 — 70_quality_checks
- wrote reports/data_quality.md; duplicates []; portability issues []

### 2026-10-10 17:27 — 80_docs
- data_dictionary rows 542; undocumented columns 0; source_ids missing from registry: none

### 2026-10-10 17:28 — 01_inventory_inputs
- sources/input_inventory.csv: 30 rows (duplicate=1, ok=24, partial=4, unreadable=1)
- registered 30 input_* sources
- period checks: all match

### 2026-10-10 17:29 — 02_extract_inputs
- text dumps: 29 files in raw/inputs_extracted/text
- raw/inputs_extracted/audit_financials.csv: 1089 rows
- raw/inputs_extracted/audit_tieout_checks.csv: 260 rows
- raw/inputs_extracted/sefa_federal_awards.csv: 4 rows
- raw/inputs_extracted/form990_pdf_financials.csv: 362 rows
- raw/inputs_extracted/form990_pdf_people.csv: 113 rows
- raw/inputs_extracted/form990_pdf_schedule_i.csv: 2 rows
- raw/inputs_extracted/funder_mentions.csv: 200 rows
- raw/inputs_extracted/individual_donor_band_counts.csv: 4 rows
- raw/inputs_extracted/board_lists.csv: 82 rows
- raw/inputs_extracted/annual_report_metrics.csv: 178 rows
- raw/inputs_extracted/crm_funders_2023_2026.csv: 160 rows
- raw/inputs_extracted/strategic_plan_targets.csv: 18 rows
- tie-out checks: 260/260 tie
- SEFA: FY15-Audited-Financial-Statements.pdf: SEFA none
- SEFA: 2016-Audited-Financial-Statements.pdf: SEFA none
- SEFA: 2017-Audited-Financial-Statements-Calvary-Women_s-Services.pdf: SEFA none
- SEFA: CWS-FY18-Audit-.pdf: SEFA none
- SEFA: 2019-Audited-Financial-Statements-CWS.pdf: SEFA none
- SEFA: 2020-Audited-Financial-Statements-CWS.pdf: SEFA none
- SEFA: 2021-Audited-Financial-Statements-CWS.pdf: SEFA none
- SEFA: Calvary-Womens-Services-Inc.-9.30.23-FS.pdf: SEFA 4 programs sum 937,999 vs printed total 937,999
- CRM export: 160 orgs, GIFT_TOTAL $10,556,075.88, 877 gifts, last-gift dates 2023-10-16 to 2026-10-03; 21 rows have NUM_GIFTS=1 but GIFT_TOTAL != LAST_CONTRIB_AMT; GIFT_TOTAL window recorded as unconfirmed
- funder names verified in layout text: 171/171
- note: 2015-Form-990-Calvary-Women_s-Services.pdf: Part I not in text layer (page 1 scanned)
- note: 2016-Form-990-Calvary-Women_s-Services.pdf: Part I not in text layer (page 1 scanned)
- note: 2019-990-Form-990-CWS.pdf: Part I not in text layer (page 1 scanned)

### 2026-10-10 17:29 — 20_build_universes
- calvary: 1 EINs
- calvary_known_funders: 88 EINs
- core_peers: 18 EINs
- daf_sponsors: 15 EINs
- dc_sector: 1,027 EINs
- dmv_funders: 7,705 EINs
- dmv_sector: 4,910 EINs
- named_comparators: 2 EINs
- national_women: 2,878 EINs
- size_matched: 566 EINs
- membership rows 17,210; distinct EINs 15,812; e-file rows 45,305; size band $2,483,998–$9,935,990; missing pins {'F3': [], 'DAF1': []}

### 2026-10-10 17:30 — 22_match_known_funders
- names 243; outcomes {('corp_foundation', 'inferred'): 16, ('exact_name_state', 'yes'): 33, ('exact_name_unique', 'yes'): 19, ('fuzzy_name_state', 'yes'): 6, ('manual', 'inferred'): 5, ('manual', 'yes'): 12, ('manual_reject', 'no'): 10, ('unmatched', 'no'): 142}; accepted EINs 88

### 2026-10-10 17:31 — 20_build_universes
- calvary: 1 EINs
- calvary_known_funders: 88 EINs
- core_peers: 18 EINs
- daf_sponsors: 15 EINs
- dc_sector: 1,027 EINs
- dmv_funders: 7,705 EINs
- dmv_sector: 4,910 EINs
- named_comparators: 2 EINs
- national_women: 2,878 EINs
- size_matched: 566 EINs
- membership rows 17,210; distinct EINs 15,812; e-file rows 45,305; size band $2,483,998–$9,935,990; missing pins {'F3': [], 'DAF1': []}

### 2026-10-10 17:35 — 36_parse_dc_awards
- wrote interim/stage_fact_gov_awards__dc.csv: 12,085 rows; by source/section: dc_oversight/dv_grantees 53; dc_oversight/erap_arpa_grants 25; dc_oversight/homelessness_prevention 19; dc_oversight/psh_case_management 90; dc_oversight/singles_shelter_contract_periods 53; dc_oversight/singles_shelter_contracts 50; dc_oversight/singles_shelter_subgrants 6; dc_oversight/youth_dhs_direct_housing 65; dc_oversight/youth_dhs_direct_nonhousing 37; dc_oversight/youth_tcp_housing 44; dc_ovsjg/ovsjg_layer 1267; dc_ovsjg/ovsjg_pdf 118; dc_pass/pass_payments 5494; dc_pass/pass_po 4494; hud_coc/hud_coc 270
- decisions: OVSJG flow_type dc_local_grant unless the stated funding source is federal only (then subaward with OVSJG as pass-through); assistance_listing filled only from the stated funding source (VOCA 16.575, STOP VAWA 16.588, SASP 16.017, Byrne JAG 16.738, JJDP Title II 16.540, Title V 16.548, RSAT 16.593, Coverdell 16.742, ARPA -> SLFRF 21.027); DHS ERAP ARPA/ERA2 shares are subawards (21.027/21.023); HUD CoC rows: TCP-applicant projects -> recipient = sponsor in the project title, flow subaward, pass-through TCP; other applicants -> prime; fiscal_year = CoC competition year (federal_fy).
- OVSJG layer 35: 1267 rows FY2016-FY2025; AGENCY used as grantee, ORGANIZATIONNAME as project title (labels swapped); 6 rows flagged as identical repeats
- OVSJG FY2024 PDF p2: 'Metro DC Community Center Inc., The' amount from text layer: 327000
- OVSJG FY2024 PDF (raw/dc_gov/20261010T123646_ovsjg_funding_recipients_FY2024.pdf): 121 grant rows, total $62,935,024
- OVSJG FY2025 PDF (raw/dc_gov/20261010T123645_ovsjg_funding_recipients_FY2025.pdf): 120 grant rows, total $92,682,681
- OVSJG FY2026 PDF (raw/dc_gov/20261010T123645_ovsjg_funding_recipients_FY2026.pdf): 118 grant rows, total $96,653,604
- OVSJG merge: 241 FY2024/FY2025 layer rows enriched from the PDFs (funding source, period, issue date); 118 PDF rows added (118 FY2026); PDF rows without a layer match: 0 []; layer FY2024/25 rows without a PDF match: 0 []
- DHS oversight provider tables: 442 rows; by section {'erap_arpa_grants': 25, 'homelessness_prevention': 19, 'youth_dhs_direct_nonhousing': 37, 'youth_tcp_housing': 44, 'youth_dhs_direct_housing': 65, 'psh_case_management': 90, 'singles_shelter_contracts': 50, 'dv_grantees': 53, 'singles_shelter_contract_periods': 53, 'singles_shelter_subgrants': 6}; $0 cells skipped: 20
- HUD CoC DC-500: 270 project rows ({2019: 38, 2020: 39, 2021: 40, 2022: 43, 2023: 39, 2024: 36, 2025: 35}); flow {'prime': 66, 'subaward': 204}
- PASS: 18,655 distinct PO suppliers, 73,834 distinct payment suppliers; matched to universe/TCP EINs: 188 PO supplier strings (182 EINs), 258 payment supplier strings (196 EINs); PO methods {'exact_norm_name': 145, 'fuzzy_token_set': 42, 'manual_known_ein': 1}
- PASS fuzzy supplier matches (75): ACCESS HOUSING INC. -> ACCESS HOUSING INC DC (100); ACCESS HOUSING INC. (DC) -> ACCESS HOUSING INC DC (100); AFFORDABLE HOUSING OPPORTUNITI -> AFFORDABLE HOUSING OPPORTUNITIES INC (97); AMERICAN ASSOC OF RESIDENTIAL -> AMERICAN ASSOCIATION OF RESIDENTIAL MORTGAGE REGULATORS (100); AMERICAN SOCIETY OF ADDICTION -> AMERICAN SOCIETY OF ADDICTION MEDICINE INC (100); American Society of Addiction -> AMERICAN SOCIETY OF ADDICTION MEDICINE INC (100); BENNING PARK NEIGHBORHOOD CORP -> BENNING PARK NEIGHBORHOOD ASSOCIATI ON (100); BLACK FEM  INC -> BLACKFEM INC (94); BLACK FEM, INC -> BLACKFEM INC (94); BREASTFEEDING OUTREACH FOR GRE -> BREASTFEEDING OUTREACH FOR GREATER WASHINGTON (93); Breastfeeding Outreach for Gre -> BREASTFEEDING OUTREACH FOR GREATER WASHINGTON (93); CAPITOL HILL COUNSELING A -> CAPITOL HILL COUNSELING AND RESOURCE CENTER INC (100); CARE AND PROGRESS COMMUNITY DE -> CARE AND PROGRESS COMMUNITY DEVELOPMENT (94); CATHOLIC CHARITIES -> CATHOLIC CHARITIES OF THE ARCHDIOCESE OF WASHINGTON INC (100); CENTER FOR ADOPTION SUPPORT -> CENTER FOR ADOPTION SUPPORT AND EDUCATION INC (100); CHILDREN & CHARITY INTERNATION -> CHILDREN & CHARITY INTERNATIONAL (97); COALITION FOR THE HOMELESS, IN -> COALITION FOR THE HOMELESS INC (100); COMMUNITY BRIDGE INC -> COMMUNITY BRIDGES INCORPORATED (97); COMMUNITY CONNECTION -> COMMUNITY CONNECTIONS (98); COMMUNITY FAMILY LIFE SERVICE, -> COMMUNITY FAMILY LIFE SERVICES INC (98); COURTNEY S HOUSE INC -> COURTNEYS HOUSE INC (97); COVENANT HOUSE WASHINGTON -> COVENANT HOUSE WASHINGTON DC (100); Care and Progress Community De -> CARE AND PROGRESS COMMUNITY DEVELOPMENT (94); Catholic Charities of the Archdiocese of -> CATHOLIC CHARITIES OF THE ARCHDIOCESE OF WASHINGTON INC (100); DC ACTION FOR CHILDREN TODAY -> DC ACTION FOR CHILDREN TODAY DC ACT (100); DEAF ABUSED WOMEN'S NETWORK -> DEAF ABUSED WOMEN NETWORK (98); DEEDS OF KINDNESS OUTREACH -> DEEDS OF KINDNESS OUTREACH SERVICES (100); DISABLED VETERANS NATL FOUNDAT -> DISABLED VETERANS NATIONAL FOUNDATION (96); DISTRICT ALLIANCE SAFE HOUSING -> DISTRICT ALLIANCE FOR SAFE HOUSING INC (100); DOORS OF HOPE INC -> DOOR OF HOPE (95); Doors of Hope Inc -> DOOR OF HOPE (95); EXCELLENT COMMUNITY SERVI -> EXCELLENT COMMUNITY SERVICES INC (94); FAMILY MEDICAL COUNSELING -> FAMILY AND MEDICAL COUNSELING SERVICE INC (100); FAR SOUTHEAST FAMILY -> FAR SOUTHEAST FAMILY STRENGTHENING COLLABORATIVE (100); FOUR WALLS DEVELOPEMENT INC. -> FOUR WALLS DEVELOPMENT INC (98); FRY PLUMBING & HEATING -> FRY PLUMBING AND HEATING NON PROFIT (100); FRY PLUMBING AND HEATING -> FRY PLUMBING AND HEATING NON PROFIT (100); Fry Plumbing and Heating -> FRY PLUMBING AND HEATING NON PROFIT (100); HOUSING COUNSELING SERVICE -> HOUSING COUNSELING SERVICES INC (98); HOUSING COUNSELING SERVICES, I -> HOUSING COUNSELING SERVICES INC (100); KEY BRIDGE FOUNDATION -> KEY BRIDGE FOUNDATION FOR EDUCATION AND RESEARCH (100); LITTLE SISTERS OF THE POOR -> LITTLE SISTERS OF THE POOR OF WASHINGTON DC INC (100); LUTHERAN SOCIAL SERVICES -> LUTHERAN SOCIAL SERVICES OF THE NATIONAL CAPITAL AREA INC (100); LUTHERAN SOCIAL SERVICES NATL' -> LUTHERAN SOCIAL SERVICES OF THE NATIONAL CAPITAL AREA INC (100); MARTHA S TABLE INC -> MARTHAS TABLE (96); MARY ELIZABETH HOUSE, INC A MI -> THE MARY ELIZABETH HOUSE INC A MINISTRY (93); MISSION FIRST HOUSING DEVELOPM -> MISSION FIRST HOUSING DEVELOPMENT CORPORATION (95); MOUNT LEBANON COMMUNITY DEVELO -> MOUNT LEBANON COMMUNITY DEVELOPMENT CORPORATION (92); Mission First Housing Developm -> MISSION FIRST HOUSING DEVELOPMENT CORPORATION (95); NAT'L FEDERATION OF THE BLIND -> NATIONAL FEDERATION OF THE BLIND OF THE DISTRICT OF COLUMBIA (100); NATIONAL CENTER FOR CHILDREN A -> NATIONAL CENTER FOR CHILDREN AND FAMILIES (100); NATIONAL CENTER FOR VICTIMS OF -> NATIONAL CENTER FOR VICTIMS OF CRIME INC (100); NATIONAL ENERGY AND UTILITY AF -> THE NATIONAL ENERGY AND UTILITY AFFORDABILITY COALITION (94); NATIONAL FEDERATION OF THE BLIND -> NATIONAL FEDERATION OF THE BLIND OF THE DISTRICT OF COLUMBIA (100); NATIONAL FOUNDATION TO END SEN -> NATIONAL FOUNDATION TO END SENIOR HUNGER INC (93); NEIGHBOR S CONSEJO -> NEIGHBORS CONSEJO (97); NORTHERN VIRGINIA FAMILY -> NORTHERN VIRGINIA FAMILY SERVICES INC (100); National Association of State Mental Health Program Directors -> NATIONAL ASSOCIATION OF STATE MENTAL HEALTH PROGRAM DIRECTORS IN (100); National Center For Victims Of -> NATIONAL CENTER FOR VICTIMS OF CRIME INC (100); OMEGA GOLD DEVELOPMENT GR -> OMEGA GOLD DEVELOPMENT GROUP INC (94); PAVING THE WAY MULTI-SERVICE -> PAVING THE WAY MULTI SERVICE INSTITUTE (100); PSI SERVICE III INC -> PSI SERVICES III INC (97); RAPE, ABUSE, INCEST, NATIONAL -> RAPE ABUSE AND INCEST NATIONAL NETWORK INC (100); RESTORATION COMMUNITY ALLIANCE -> RESTORATION COMMUNITY ALLIANCE COMMUNITY DEVLEOPMENT CORPORATION (100); Rape, Abuse, Incest, National -> RAPE ABUSE AND INCEST NATIONAL NETWORK INC (100); SAMARITAN MINISTRY OF GREATER -> SAMARITAN MINISTRY OF GREATER WASHINGTON (100); SERVICE SOURCE, INC -> SERVICESOURCE INC (96); STEPPINGSTONE FOUNDATION, INC. -> STEPPING STONE FOUNDATION INC (98); SYMBRAL FOUNDATION FOR CMTY. -> SYMBRAL FOUNDATION FOR COMMUNITY SERVICES INC (100); Safe Routes to School National Partnersh -> SAFE ROUTES TO SCHOOL NATIONAL PARTNERSHIP (98); THE HOPE FOUNDATION RE-ENTRY -> HOPE FOUNDATION RE-ENTRY NETWORK INC (100); THE MARY ELIZABETH HOUSE -> THE MARY ELIZABETH HOUSE INC A MINISTRY (100); THE NATIONAL REENTRY NETWORK -> THE NATIONAL REENTRY NETWORK FOR RETURNING CITIZENS (100); Torture abolition and Survivors Support -> TORTURE ABOLITION AND SURVIVORS SUPPORT COALITION INTERNATIONAL (100); WASHINGTON REGIONAL ALCOHOL PR -> WASHINGTON REGIONAL ALCOHOL PROGRAM (95)
- PASS POs for universe vendors: 5,602 raw rows -> 4,494 after dedupe on PONUMBER + FISCALYEAR + POTOTAL (repeats removed: 1,108, almost all AA0 sub-office fan-out)
- PASS payments for universe vendors: 5,494 supplier x FY x agency x PO aggregates; FY2025+ rows flagged x_pass_incomplete_fy=1 (PASS incomplete from FY2025, financial-system change)
- fuzzy name matches in DC/HUD documents (21): CENTER FOR NON- PROFIT ADVANCEMENT -> CENTER FOR NONPROFIT ADVANCEMENT (98); CENTER FOR NON-PROFIT ADVANCEMENT -> CENTER FOR NONPROFIT ADVANCEMENT (98); Calvary Women's Service -> CALVARY WOMENS SERVICES INC (98); Catholic Charities -> CATHOLIC CHARITIES OF THE ARCHDIOCESE OF WASHINGTON INC (100); Catholic Charities of the Archdiocese of -> CATHOLIC CHARITIES OF THE ARCHDIOCESE OF WASHINGTON INC (100); Community Family Live Services -> COMMUNITY FAMILY LIFE SERVICES INC (97); Covenant House -> COVENANT HOUSE WASHINGTON DC (100); Covenant House Greater Washington -> COVENANT HOUSE WASHINGTON DC (94); Covenant House Washington -> COVENANT HOUSE WASHINGTON DC (100); DISTRICT ALLIANCE SAFE HOUSING -> DISTRICT ALLIANCE FOR SAFE HOUSING INC (100); Deaf Abused Women's Network -> DEAF ABUSED WOMEN NETWORK (98); Deaf Abused Women's Network (DAWN) -> DEAF ABUSED WOMEN NETWORK (98); Everyone Home -> EVERYONE HOME DC (100); Housing Counseling Service -> HOUSING COUNSELING SERVICES INC (98); Institute for African Man Development Inc. -> INSTITUTE FOR AFRICAN MAN DEVELOPME NT INC (99); Pathways to Housing -> PATHWAYS TO HOUSING DC (100); SURVIVORS AND ADVOCATES FOR EMPOWERM ENT (DC SAFE) -> SURVIVORS AND ADVOCATES FOR EMPOWERMENT SAFE INC (92); SURVIVORS AND ADVOCATES FOR EMPOWERMENT (SAFE) -> SURVIVORS AND ADVOCATES FOR EMPOWERMENT SAFE INC (100); Survivors and Advocates for Empowerment, Inc. -> SURVIVORS AND ADVOCATES FOR EMPOWERMENT SAFE INC (100); The Hope Foundation Reentry Network Inc. -> HOPE FOUNDATION RE-ENTRY NETWORK INC (92); The National Centers for Children and Families -> NATIONAL CENTER FOR CHILDREN AND FAMILIES (99)
- DHS oversight tie-out: 2024 erap_arpa_grants [ARPA] printed $42,070,444 vs parsed $42,070,444 -> tie
- DHS oversight tie-out: 2024 erap_arpa_grants [ERA2] printed $6,326,098 vs parsed $6,326,098 -> tie
- DHS oversight tie-out: 2024 erap_arpa_grants [Local] printed $576,903 vs parsed $576,903 -> tie
- DHS oversight tie-out: 2025 dv_grantees [FY2024 total grant award] printed $4,462,363 vs parsed $4,462,363 -> tie
- DHS oversight tie-out: 2025 dv_grantees [FY2025 total grant award] printed $4,847,166 vs parsed $4,847,167 -> tie
- DHS oversight tie-out: 2025 erap_arpa_grants [ARPA] printed $7,763,167 vs parsed $7,763,167 -> tie
- DHS oversight tie-out: 2025 erap_arpa_grants [ERA2] printed $30,181,471 vs parsed $30,181,472 -> tie
- DHS oversight tie-out: 2025 erap_arpa_grants [Local] printed $22,587,325 vs parsed $22,587,325 -> tie
- DHS oversight tie-out: 2025 homelessness_prevention [FY24] printed $7,450,000 vs parsed $7,450,000 -> tie
- DHS oversight tie-out: 2025 homelessness_prevention [FY25 YTD] printed $6,119,700 vs parsed $6,119,700 -> tie
- DHS oversight tie-out: 2025 psh_case_management [DHS local] printed $25,803,404 vs parsed $25,803,404 -> tie
- DHS oversight tie-out: 2025 psh_case_management [Medicaid] printed $38,687,549 vs parsed $38,687,549 -> tie
- HUD AwardComp DC-500 2019: 38 projects, parsed $22,075,117 vs printed total $22,075,117 -> tie
- HUD AwardComp DC-500 2020: 39 projects, parsed $23,608,105 vs printed total $23,608,105 -> tie
- HUD AwardComp DC-500 2021: 40 projects, parsed $25,062,775 vs printed total $25,062,775 -> tie
- HUD AwardComp DC-500 2022: 43 projects, parsed $27,933,554 vs printed total $27,933,554 -> tie
- HUD AwardComp DC-500 2023: 39 projects, parsed $29,711,325 vs printed total $29,711,325 -> tie
- HUD AwardComp DC-500 2024: 36 projects, parsed $33,659,924 vs printed total $33,659,924 -> tie
- HUD FY2025 round 1 DC-500 (p12): 15 projects, parsed $15,042,362 vs printed $15,042,362 -> tie
- HUD FY2025 round 2 DC-500 (p22): 4 projects, parsed $6,616,773 vs printed $6,616,773 -> tie
- HUD FY2025 round 3 DC-500 (p37): 16 projects, parsed $11,878,879 vs printed $11,878,879 -> tie
- HUD FY2024 AwardComp vs hud.gov DC report: 36 vs 36 projects, total $33,659,924 vs $33,659,924; project-level differences 0: []
- duplicates: award_row_id collisions 0; fully identical rows 0
- Calvary OVSJG rows: 15 (FY2019-FY2025 layer 13, FY2026 PDF 2); match recon: yes
- provider-name match rate (non-PASS): 114/437 distinct names (26%), 903/2097 rows, 49% of dollars; by source {'dc_oversight': '46/93 names, 263/442 rows', 'dc_ovsjg': '73/351 names, 404/1385 rows', 'hud_coc': '19/26 names, 236/270 rows'}; methods {'unmatched': 1194, 'fuzzy_token_set': 136, 'exact_norm_name': 664, 'manual_alias': 68, 'manual_known_ein': 35}

### 2026-10-10 17:37 — 37_parse_dc_budget: DC budget lines and policy events
- interim/stage_dc_budget_lines__dc.csv: 5,172 rows (Counter({'approved': 3172, 'actual': 1968, 'proposed': 32})); in-scope program/agency rows 854; duplicate keys 0
- interim/stage_fact_policy_events__dc.csv: 297 rows; by kind {'change_table_FO0-5': 8, 'change_table_HY0-5': 9, 'change_table_JA0-5': 25, 'yoy_approved_change': 161, 'bsa_subtitle': 25, 'fy2025_change_narrative': 13, 'committee_report_item': 22, 'committee_report_variance': 6, 'change_table_DB0-5': 1, 'council_adjustments_chart_fy2027': 27}; by type {'budget_proposed': 41, 'budget_enacted': 161, 'budget_revised': 66, 'policy_change': 26, 'other': 1, 'program_launch': 2}
- parsed tables: FY2024 JA0 30-PBB (2024_JA0_ja_dhs_tables_2024j.pdf): 62 lines; FY2024 FO0 30-PBB (024_FO0_fo_vsjg_tables_2024j.pdf): 21 lines; FY2024 RM0 30-PBB (2024_RM0_rm_dbh_tables_2024j.pdf): 128 lines; FY2024 DB0 30-PBB (024_DB0_db_dhcd_tables_2024j.pdf): 44 lines; FY2024 HY0 30-PBB (2024_HY0_hy_has_tables_2024j.pdf): 16 lines; FY2024 CF0 30-PBB (2024_CF0_cf_des_tables_2024j.pdf): 69 lines; FY2024 HG0 30-PBB (24_HG0_hg_dmhhs_tables_2024j.pdf): 9 lines; FY2025 JA0 30-PBB (2025_JA0_ja_dhs_tables_2025j.pdf): 61 lines; FY2025 FO0 30-PBB (25_FO0_fo_ovsjg_tables_2025j.pdf): 28 lines; FY2025 RM0 30-PBB (2025_RM0_rm_dbh_tables_2025j.pdf): 87 lines; FY2025 DB0 30-PBB (025_DB0_db_dhcd_tables_2025j.pdf): 36 lines; FY2025 HY0 30-PBB (2025_HY0_hy_hap_tables_2025j.pdf): 7 lines; FY2025 CF0 30-PBB (025_CF0_cf_does_tables_2025j.pdf): 62 lines; FY2025 HG0 30-PBB (25_HG0_hg_dmhhs_tables_2025j.pdf): 8 lines; FY2026 JA0 Table JA0-4 (026_JA0_ja_dhs_chapter_2026o.pdf): 57 lines; FY2026 FO0 Table FO0-4 (26_FO0_fo_vsjg_chapter_2026o.pdf): 26 lines; FY2026 RM0 Table RM0-4 (026_RM0_rm_dbh_chapter_2026o.pdf): 83 lines; FY2026 DB0 Table DB0-4 (26_DB0_db_dhcd_chapter_2026o.pdf): 36 lines; FY2026 HY0 Table HY0-4 (026_HY0_hy_has_chapter_2026o.pdf): 7 lines; FY2026 CF0 Table CF0-4 (26_CF0_cf_does_chapter_2026o.pdf): 61 lines; FY2026 HG0 Table HG0-4 (6_HG0_hg_dmhhs_chapter_2026o.pdf): 6 lines; FY2027 JA0 30-PBB (7_JA0_ja0_dhs_tables_2027a_0.pdf): 57 lines; FY2027 FO0 30-PBB (FO0_fo0_ovsjg_tables_2027a_0.pdf): 26 lines; FY2027 RM0 30-PBB (7_RM0_rm0_dbh_tables_2027a_0.pdf): 80 lines; FY2027 DB0 30-PBB (_DB0_db0_dhcd_tables_2027a_0.pdf): 36 lines; FY2027 HY0 30-PBB (7_HY0_hy0_hap_tables_2027a_0.pdf): 7 lines; FY2027 CF0 30-PBB (_CF0_cf0_does_tables_2027a_0.pdf): 61 lines; FY2027 HG0 30-PBB (HG0_hg0_dmhhs_tables_2027a_0.pdf): 7 lines
- change items: FY2024 JA0 Table JA0-5: 29 change lines, 7 in scope; FY2024 FO0 Table FO0-5: 14 change lines, 3 in scope; FY2024 RM0 Table RM0-5: 25 change lines, 0 in scope; FY2024 DB0 Table DB0-5: 14 change lines, 0 in scope; FY2024 HY0 Table HY0-5: 6 change lines, 6 in scope; FY2024 CF0 Table CF0-5: 16 change lines, 0 in scope; FY2024 HG0 Table HG0-5: 7 change lines, 0 in scope; FY2025 JA0 narrative change sentences (pypdfium2): 8 in scope; FY2025 FO0: chapter change text is font-garbled (amounts missing); OVSJG FY2025 changes taken from the JPS committee report; FY2025 RM0 narrative change sentences (pypdfium2): 0 in scope; FY2025 DB0 narrative change sentences (pypdfium2): 2 in scope; FY2025 HY0 narrative change sentences (pypdfium2): 3 in scope; FY2025 CF0 Table CF0-5: 20 change lines, 0 in scope; FY2025 HG0 narrative change sentences (pypdfium2): 0 in scope; FY2026 JA0 Table JA0-5: 29 change lines, 14 in scope; FY2026 FO0 Table FO0-5: 16 change lines, 4 in scope; FY2026 RM0 Table RM0-5: 27 change lines, 0 in scope; FY2026 DB0 Table DB0-5: 16 change lines, 0 in scope; FY2026 HY0 Table HY0-5: 2 change lines, 2 in scope; FY2026 CF0 Table CF0-5: 17 change lines, 0 in scope; FY2026 HG0 Table HG0-5: 4 change lines, 0 in scope; FY2027 JA0 Table JA0-5: 15 change lines, 4 in scope; FY2027 FO0 Table FO0-5: 11 change lines, 1 in scope; FY2027 RM0 Table RM0-5: 17 change lines, 0 in scope; FY2027 DB0 Table DB0-5: 15 change lines, 1 in scope; FY2027 HY0 Table HY0-5: 3 change lines, 1 in scope; FY2027 CF0 Table CF0-5: 8 change lines, 0 in scope; FY2027 HG0 Table HG0-5: 3 change lines, 0 in scope
- committee report tables: BR_FY25_Housing -> 1 in-scope proposed activity rows (markup 2024-05-09); BR_FY25_JPS -> 0 in-scope proposed activity rows (markup not printed); BR_FY26_committee_budget_report_Human-Services -> 18 in-scope proposed activity rows (markup 2025-06-24); BR_FY26_committee_budget_report_Housing -> 5 in-scope proposed activity rows (markup 2025-06-24); BR_FY26_committee_budget_report_JPS -> 2 in-scope proposed activity rows (markup not printed); BR_FY26_committee_budget_report_Health -> 0 in-scope proposed activity rows (markup 2025-06-23); BR_FY27_committee_budget_report_DRAFT-FY2027-Committee-on-Health -> 2 in-scope proposed activity rows (markup 2026-05-20); BR_FY27_committee_budget_report_FY27-Committee-on-Housing -> 4 in-scope proposed activity rows (markup not printed); BR_FY27_committee_budget_report_52226-FY2027-JPS -> 0 in-scope proposed activity rows (markup not printed)
- FY2027 Council adjustments chart: 1627 rows read, 27 in-scope events
- BSA subtitles kept: 25; curated committee-report items: 22; YoY approved-change events: 161
- tie-outs: 257 pass, 0 fail
- tie-out detail (in-scope divisions): FY2024 JA0 30-PBB p2 division 5000: sum of 23 activities vs subtotal, deltas by column [0, 0, 0, -1] ($000) -> pass | FY2024 JA0 30-PBB p3 agency total: sum of 8 division subtotals, deltas [0, -2, 0, 1] ($000) -> pass | FY2024 JA0 Table JA0-2 p2: sum of 7 fund rows vs GROSS FUNDS, deltas [-1, 0, -1, 0] ($000) -> pass | FY2024 FO0 30-PBB p1 division 4000: sum of 2 activities vs subtotal, deltas by column [0, 0, 0, -1] ($000) -> pass | FY2024 FO0 30-PBB p1 division 5000: sum of 1 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 FO0 30-PBB p1 division 6000: sum of 5 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 FO0 30-PBB p1 agency total: sum of 7 division subtotals, deltas [-2, -1, -2, 1] ($000) -> pass | FY2024 FO0 Table FO0-2 p2: sum of 5 fund rows vs GROSS FUNDS, deltas [0, 0, -1, 0] ($000) -> pass | FY2024 RM0 30-PBB p5 agency total: sum of 16 division subtotals, deltas [0, 1, 1, 0] ($000) -> pass | FY2024 RM0 Table RM0-2 p2: sum of 9 fund rows vs GROSS FUNDS, deltas [0, 1, 0, 1] ($000) -> pass | FY2024 DB0 30-PBB p2 agency total: sum of 9 division subtotals, deltas [0, 0, 0, -1] ($000) -> pass | FY2024 DB0 Table DB0-2 p2: sum of 5 fund rows vs GROSS FUNDS, deltas [1, -1, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 division 4000: sum of 1 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 division 5000: sum of 1 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 division 6000: sum of 5 activities vs subtotal, deltas by column [2, -1, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 agency total: sum of 5 division subtotals, deltas [0, 0, -1, 0] ($000) -> pass | FY2024 HY0 Table HY0-2 p1: sum of 1 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2024 CF0 30-PBB p2 division 4000: sum of 16 activities vs subtotal, deltas by column [0, 0, 0, -1] ($000) -> pass | FY2024 CF0 30-PBB p2 division 5000: sum of 3 activities vs subtotal, deltas by column [1, 0, 1, 0] ($000) -> pass | FY2024 CF0 30-PBB p2 division 6000: sum of 6 activities vs subtotal, deltas by column [1, 0, 0, 0] ($000) -> pass | FY2024 CF0 30-PBB p3 agency total: sum of 11 division subtotals, deltas [-1, 0, 0, -1] ($000) -> pass | FY2024 CF0 Table CF0-2 p2: sum of 6 fund rows vs GROSS FUNDS, deltas [1, 0, 0, 0] ($000) -> pass | FY2024 HG0 30-PBB p1 agency total: sum of 4 division subtotals, deltas [0, 0, 0, 0] ($000) -> pass | FY2024 HG0 Table HG0-2 p2: sum of 2 fund rows vs GROSS FUNDS, deltas [0, 1, 0, 0] ($000) -> pass | FY2025 JA0 30-PBB p2 division HS0030: sum of 28 activities vs subtotal, deltas by column [-2, 1, -1, 1] ($000) -> pass | FY2025 JA0 30-PBB p2 agency total: sum of 6 division subtotals, deltas [0, -1, 1, 0] ($000) -> pass | FY2025 FO0 30-PBB p1 division PS0023: sum of 2 activities vs subtotal, deltas by column [0, 0, -1, 0] ($000) -> pass | FY2025 FO0 30-PBB p2 agency total: sum of 12 division subtotals, deltas [-1, -2, 1, 0] ($000) -> pass | FY2025 RM0 30-PBB p3 agency total: sum of 13 division subtotals, deltas [1, 1, 0, 1] ($000) -> pass | FY2025 DB0 30-PBB p2 agency total: sum of 6 division subtotals, deltas [0, 1, 1, 0] ($000) -> pass | FY2025 HY0 30-PBB p1 division EC0039: sum of 5 activities vs subtotal, deltas by column [0, -1, 0, 0] ($000) -> pass | FY2025 HY0 30-PBB p1 agency total: sum of 1 division subtotals, deltas [0, 0, 0, 0] ($000) -> pass | FY2025 CF0 30-PBB p3 agency total: sum of 10 division subtotals, deltas [0, -1, 0, -1] ($000) -> pass | FY2025 CF0 Table CF0-2 p2: sum of 6 fund rows vs GROSS FUNDS, deltas [0, -1, 0, 0] ($000) -> pass | FY2025 HG0 30-PBB p1 agency total: sum of 3 division subtotals, deltas [0, 0, 0, 1] ($000) -> pass | FY2026 JA0 Table JA0-4 p5 division HS0030: sum of 28 activities vs subtotal, deltas [1, -2, 1, -1] ($000) -> pass | FY2026 JA0 Table JA0-4 p5 agency total: sum of 5 divisions, deltas [-1, -1, 0, 0] ($000) -> pass | FY2026 JA0 Table JA0-2 p2: sum of 7 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 FO0 Table FO0-4 p4 division PS0023: sum of 2 activities vs subtotal, deltas [0, 1, 0, 0] ($000) -> pass | FY2026 FO0 Table FO0-4 p4 agency total: sum of 11 divisions, deltas [-2, 0, 0, 0] ($000) -> pass | FY2026 FO0 Table FO0-2 p2: sum of 4 fund rows vs GROSS FUNDS, deltas [-1, 0, 0, 0] ($000) -> pass | FY2026 RM0 Table RM0-4 p7 agency total: sum of 13 divisions, deltas [1, 1, 2, 0] ($000) -> pass | FY2026 RM0 Table RM0-2 p2: sum of 8 fund rows vs GROSS FUNDS, deltas [1, 0, -1, 0] ($000) -> pass | FY2026 DB0 Table DB0-4 p4 agency total: sum of 6 divisions, deltas [1, -1, 0, -1] ($000) -> pass | FY2026 DB0 Table DB0-2 p2: sum of 4 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 HY0 Table HY0-4 p2 division EC0039: sum of 5 activities vs subtotal, deltas [-1, 1, 0, 0] ($000) -> pass | FY2026 HY0 Table HY0-4 p2 agency total: sum of 1 divisions, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 HY0 Table HY0-2 p1: sum of 1 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 CF0 Table CF0-4 p5 agency total: sum of 10 divisions, deltas [-1, 1, 0, 0] ($000) -> pass | FY2026 CF0 Table CF0-2 p2: sum of 5 fund rows vs GROSS FUNDS, deltas [-1, 1, 0, 1] ($000) -> pass | FY2026 HG0 Table HG0-4 p3 agency total: sum of 2 divisions, deltas [0, 1, 1, 0] ($000) -> pass | FY2026 HG0 Table HG0-2 p2: sum of 1 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2027 JA0 30-PBB p2 division HS0030: sum of 28 activities vs subtotal, deltas by column [-2, -2, -1, -3] ($000) -> pass | FY2027 JA0 30-PBB p2 agency total: sum of 5 division subtotals, deltas [-1, 1, 0, -1] ($000) -> pass | FY2027 JA0 Table JA0-2 p2: sum of 7 fund rows vs GROSS FUNDS, deltas [0, 1, 0, 0] ($000) -> pass | FY2027 FO0 30-PBB p1 division PS0023: sum of 2 activities vs subtotal, deltas by column [1, 0, 0, 0] ($000) -> pass | FY2027 FO0 30-PBB p1 agency total: sum of 11 division subtotals, deltas [-1,
- cross-book disagreements (same FY/stage/code, >$2K apart; later book preferred via x_preferred): 2022 actual JA0 AMP000 total: FY2025 book 33,466,000, FY2024 book 33,534,000 | 2022 actual JA0 AFO000 total: FY2025 book 3,079,000, FY2024 book 3,025,000 | 2022 actual JA0 HS0029 total: FY2025 book 279,438,000, FY2024 book 280,259,000 | 2022 actual JA0 HS0030 total: FY2025 book 625,848,000, FY2024 book 625,869,000 | 2025 approved JA0 H02902 total: FY2026 book 42,867,000, FY2025 book 42,943,000 | 2025 approved JA0 H02905 total: FY2026 book 91,735,000, FY2025 book 91,660,000 | 2025 approved FO0 P01903 total: FY2026 book 18,405,000, FY2025 book 18,312,000 | 2025 approved FO0 PS0019 total: FY2026 book 18,405,000, FY2025 book 18,312,000 | 2025 approved RM0 AFO003 total: FY2026 book 1,120,000, FY2025 book 1,010,000 | 2025 approved RM0 AFO005 total: FY2026 book 567,000, FY2025 book 577,000 | 2025 approved RM0 AFO000 total: FY2026 book 2,378,000, FY2025 book 2,278,000 | 2025 approved RM0 H04201 total: FY2026 book 175,000, FY2025 book 179,000 | 2025 approved RM0 H04202 total: FY2026 book 1,128,000, FY2025 book 1,151,000 | 2025 approved RM0 H04205 total: FY2026 book 381,000, FY2025 book 355,000 | 2025 approved RM0 H04504 total: FY2026 book 1,367,000, FY2025 book 100,000 | 2025 approved RM0 HS0045 total: FY2026 book 37,390,000, FY2025 book 36,123,000 | 2025 approved RM0 H04802 total: FY2026 book 27,140,000, FY2025 book 22,840,000 | 2025 approved RM0 H04805 total: FY2026 book 1,391,000, FY2025 book 5,691,000 | 2025 approved RM0 HS0053 total: FY2026 book 20,351,000, FY2025 book 21,717,000 | 2025 approved CF0 AFO003 total: FY2026 book 2,141,000, FY2025 book 2,222,000 | 2025 approved CF0 AFO000 total: FY2026 book 4,023,000, FY2025 book 4,104,000 | 2025 approved CF0 AMP026 total: FY2026 book 0, FY2025 book -3,000 | 2025 approved CF0 AMP000 total: FY2026 book 24,947,000, FY2025 book 24,944,000 | 2025 approved CF0 O00111 total: FY2026 book 556,000, FY2025 book 559,000 | 2025 approved CF0 GO0047 total: FY2026 book 6,545,000, FY2025 book 6,548,000 | 2025 approved CF0 O05201 total: FY2026 book 15,504,000, FY2025 book 15,422,000 | 2025 approved CF0 GO0052 total: FY2026 book 75,929,000, FY2025 book 75,847,000
- FY2024 old-code -> FY2025 code crosswalk (FY2024 approved): FO0 P02301: FY2024 book 171,000 vs FY2025 book restated 171,000 (delta +0) | FO0 P02303: FY2024 book 45,515,000 vs FY2025 book restated 45,515,000 (delta +0) | FO0 P04502: FY2024 book 3,720,000 vs FY2025 book restated 3,720,000 (delta +0) | HY0 R03903: FY2024 book 4,400,000 vs FY2025 book restated 4,400,000 (delta +0) | HY0 R03904: FY2024 book 0 vs FY2025 book restated 0 (delta +0) | HY0 R03905: FY2024 book 128,094,000 vs FY2025 book restated 128,094,000 (delta +0) | HY0 R03906: FY2024 book 10,581,000 vs FY2025 book restated 10,581,000 (delta +0) | HY0 R03907: FY2024 book 43,296,000 vs FY2025 book restated 43,296,000 (delta +0) | JA0 H03002: FY2024 book 79,033,000 vs FY2025 book restated 93,339,000 (delta +14,306,000) | JA0 H03003: FY2024 book 59,994,000 vs FY2025 book restated 59,994,000 (delta +0) | JA0 H03004: FY2024 book 31,818,000 vs FY2025 book restated 12,421,000 (delta -19,397,000) | JA0 H03007: FY2024 book 2,940,000 vs FY2025 book restated 2,940,000 (delta +0) | JA0 H03008: FY2024 book 42,536,000 vs FY2025 book restated 42,536,000 (delta +0) | JA0 H03009: FY2024 book 2,799,000 vs FY2025 book restated 4,259,000 (delta +1,460,000) | JA0 H03010: FY2024 book 51,764,000 vs FY2025 book restated 60,770,000 (delta +9,006,000) | JA0 H03011: FY2024 book 4,935,000 vs FY2025 book restated 4,935,000 (delta +0) | JA0 H03012: FY2024 book 86,929,000 vs FY2025 book restated 83,014,000 (delta -3,915,000) | JA0 H03013: FY2024 book 4,222,000 vs FY2025 book restated 4,222,000 (delta +0) | JA0 H03014-H03016: FY2024 book 11,541,000 vs FY2025 book restated 11,542,000 (delta +1,000) | JA0 H03017: FY2024 book 73,209,000 vs FY2025 book restated 73,209,000 (delta +0) | JA0 H03018: FY2024 book 10,875,000 vs FY2025 book restated 10,875,000 (delta +0) | JA0 H03019: FY2024 book 1,150,000 vs FY2025 book restated 1,150,000 (delta +0) | JA0 H03022: FY2024 book 1,980,000 vs FY2025 book restated 1,980,000 (delta +0) | JA0 H03023: FY2024 book 12,032,000 vs FY2025 book restated 12,032,000 (delta +0) | RM0 H04308: FY2024 book 29,637,000 vs FY2025 book restated 29,637,000 (delta +0) | RM0 H04504: FY2024 book 1,467,000 vs FY2025 book restated 1,467,000 (delta +0)
- event dates: budget_enacted/budget_revised = Local Budget Act 2nd reading {2024: '2023-05-30', 2025: '2024-06-12', 2026: '2025-07-28', 2027: '2026-06-23'}; budget_proposed = BSA introduced on behalf of the Mayor {2025: '2024-04-03', 2026: '2025-06-02', 2027: '2026-04-14'} (FY2024 proposal date not in downloaded docs -> blank); BSA policy rows = law/act effective date {2024: '2023-09-06', 2025: '2024-09-18', 2026: '2025-12-06', 2027: '2026-08-13'}; committee items = markup date when printed, else Local Budget Act date
- mapping: Table XX0-5 lines before 'Mayor's Proposed Budget' -> budget_proposed; lines between it and 'District's Approved Budget' -> budget_revised (Council changes); FY2027 Council-level changes taken from the activity-level Council chart instead of JA0-5 to avoid double counting
- coverage (stage[+funds] by FY x agency JA0/FO0/RM0/DB0/HY0/CF0/HG0):
| FY2021 | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds |
| FY2022 | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds |
| FY2023 | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds |
| FY2024 | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds |
| FY2025 | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds,prop | actu+funds,appr+funds | actu+funds,appr+funds |
| FY2026 | appr+funds,prop | appr+funds,prop | appr+funds | appr+funds | appr+funds,prop | appr+funds | appr+funds |
| FY2027 | appr+funds | appr+funds | appr+funds,prop | appr+funds | appr+funds,prop | appr+funds | appr+funds |
- warnings (0):

### 2026-10-10 17:37 — 38_parse_hud_counts
- wrote interim/stage_homeless_counts__hud.csv: 49,393 rows ({'bulk_hud_ahar_pit_hic': 48224, 'doc_hud_hic_dc500': 428, 'doc_mwcog_pit': 741}); PIT 39,029, HIC by CoC 9,195, PopSub 428, MWCOG 741
- wrote interim/stage_hic_projects__hud.csv: 1,257 rows (2022: 332, 2023: 292, 2024: 323, 2025: 310)
- HIC project PDFs: provider and facility names are truncated in the PDF itself (fixed-width report cells; same text in pdfplumber chars, pypdf and pdftotext); kept as printed. 'units' = family units (HIC reports units only for households with children). target_population is derived from the bed columns (household type, plus youth/veterans/chronic when all beds are dedicated) and set to single_women / women_with_children only when the provider or project name says women (basis in x_target_population_basis). x_women_focused_org = core peer tier 1a or Calvary; x_dv_focused_org = tier 1b (config/core_peers.csv).
- PIT by CoC (raw/hud/20261010T123731_huduser_2007-2025-PIT-Counts-by-CoC.xlsb): sheets 2007-2025; 39,029 rows for 8 CoCs; unparsed column names 216 (e.g. ['Overall Homeless - Under 18', 'Overall Homeless - Age 18 to 24', 'Overall Homeless - Over 24']); CoC-years absent: none
- partial unsheltered counts (Count Types): MD-601 2021; VA-602 2021
- workbook has no gender columns in any year (only age, race/ethnicity, household and subpopulation splits); DC gender comes from PopSub 2024 and the MWCOG 2025 DC narrative
- HIC by CoC (raw/hud/20261010T123733_huduser_2007-2025-HIC-Counts-by-CoC.xlsx): sheets 2007-2025; 9,195 rows; unparsed columns 9 (['HMIS Participation Rate (ES,TH) (non-numeric)', 'ES HMIS Participation Rate (non-numeric)', 'Total TH Beds for Households with only Children (non-numeric)', 'HMIS Participation Rate for Year-Round Beds (SH) (non-numeric)']); same-measure columns with different values kept as '__alt': 0
- PopSub DC-500 2024 (raw/hud/20261010T123749_hudx_CoC_PopSub_DC-500_2024.pdf): 232 rows; total persons 5616; women 2167
- PopSub DC-500 2025 (raw/hud/20261010T123750_hudx_CoC_PopSub_DC-500_2025.pdf): 196 rows; total persons 5138; women n/a
- MWCOG 2023 report (raw/hud/20261010T123754_mwcog_homelessness_metro_washington_2023_PIT.pdf): 548 table cells kept
- MWCOG 2024 report (raw/hud/20261010T123753_mwcog_homelessness_metro_washington_2024_PIT.pdf): 504 table cells kept
- MWCOG 2025 report (raw/hud/20261010T123752_mwcog_homelessness_metro_washington_2025_PIT.pdf): 520 table cells kept
- MWCOG 2026 report (raw/hud/20261010T123751_mwcog_homelessness_metro_washington_2026_PIT.pdf): 531 table cells kept
- MWCOG: 2103 cells parsed across reports -> 741 after keeping the latest report per jurisdiction/year/measure/population; values revised between reports: 38 (e.g. Prince William County, VA 2022 all: 241 (rpt 2023) -> 282 (rpt 2024); Prince William County, VA 2021 all: 282 (rpt 2023) -> 326 (rpt 2024); Prince William County, VA 2020 all: 326 (rpt 2023) -> 277 (rpt 2024); COG region 2023 households_without_children: 5901 (rpt 2023) -> 5755 (rpt 2024)); same report, two tables disagree (earlier page kept): 17 (District of Columbia 2020 households_with_only_children rpt 2023: p68 12 vs p25 11; Frederick City & County, MD 2021 households_with_only_children rpt 2023: p68 5 vs p25 0; COG region 2020 households_with_only_children rpt 2023: p69 13 vs p25 12; City of Alexandria, VA 2020 all rpt 2023: p68 198 vs p17 207)
- skipped tables (did not parse reliably): none; source-inconsistent columns are kept with confidence medium and an x_note
- not parsed: figures/charts (demographic profiles, income, gender charts), Table 3 population shares, Table 13/14 shelter status, TAY tables, Table 16 bed inventory, Table 17 formerly homeless in PH, Appendix B narrative percentages except the 2025 DC gender-of-adults table
- HIC provider names (cleaned, distinct): 105; matched 42 (40%); methods {'unmatched': 63, 'fuzzy_token_set': 10, 'exact_norm_name': 29, 'manual_known_ein': 2, 'manual_alias': 1}; government providers (no EIN expected) 7; beds at matched providers 67,567 of 133,181 (51%)
- fuzzy matches: Access Housing -> 521918702 (100.0); Access Housing INC (AHI) (Agency) -> 521918702 (100.0); Catholic Charities -> 530196524 (100.0); Catholic Charities (Agency) -> 530196524 (100.0); Covenant House Washington -> 133537709 (100.0); Covenant House Washington (CHW)(Age -> 133537709 (100.0); East River Family Strengthening Collabor -> 522277915 (100.0); Edgewood-Brookland Family Support Col -> 522246995 (100.0); Edgewood/Brookland Family Support Col -> 522246995 (100.0); Far Southeast Family Strengthening Colla -> 522117070 (100.0); Georgia Avenue Family Support Collabor -> 522349433 (100.0); Survivors & Advocates for Empowerment -> 412226446 (100.0)
- unmatched nonprofit providers (not in dc_sector/dmv_sector/core_peers by name): 801 East Collaborative; Bradley & Associates; CCDC; CORE DC; Casa Ruby; Church of Epiphany; Church of the Epiphany; Collaborative Solutions for Communities; Communities Helping & Empowering Pat; Communities Helping and Empowering P; Community Solutions; Cornerstone Community; Dawn Deaf; Deaf Dawn; East of the River Family Support Collabor; Echelon Community Services; Far Southeast Family Support Collaborati; Healthy Babies; Healthy Babies Project; Hillcrest Children & Family Center; Hope and a Home; Institute for Emotional Regulation; Jaydot; Joseph's House; Jubilee Housing; KBEC Group, Inc; KBEC Group, Inc.; KC Community Services; Latin American Youth Center; MBI Health Services; Maximus; Metropolitan Education Solutions; Metropolitan Educational Solutions; North Capitol Collaborative Inc.; North Capitol Family Support Collaborati; Operation Renewed Hope; Positive Kinship Bonding; SLS; SMYAL; Salvation Army; Sasha Bruce Youthwork; Sasha Bruce Youthworks; So Others Might Eat; Spring Leaf; St. Aloysius Roman Catholic Church; St. John's Community Community Servic; St. John's Community Services; Supporting & Mentoring Youth Advocate; Temple Micah; Temple Sinai; The Community Builders and Emory Bea; The Institute for Emotional Regulation, L; The Salvation Army; U.S. Vets; US Veterans Initiative; Wheeler Creek
- matcher (shared with script 36): manual aliases (TCP 521681401; DASH, DC SAFE, Housing Up), norm_name exact, then rapidfuzz token_set_ratio >= 92 (after expanding a truncated last token for raw names >= 30 chars) accepted only when fuzzy_ok() holds: both names >= 2 tokens, a shared non-generic token, no one-sided entity-marker token (foundation, fund, maryland, county, ...), and token containment (ratio >= 0.5) or prefix or only soft one-sided words or fuzz.ratio >= 90; reviewed reject list
- PopSub 2024 gender rows sum 5616 vs total 5616: pass
- MWCOG 2023 p16 'People Experiencing Literal Homelessness by Jurisdiction, 2022 - 2023': pass (2 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p17 'People Experiencing Literal Homelessness by Jurisdiction, 2019-2023': pass (5 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p22 '2023 Persons In Families Experiencing Homelessness by Jurisdiction': pass (4 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p23 'Change In Persons In Families Experiencing Homelessness by Jurisdictio': pass (5 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p25 'Households With Only Children Under Age 18 By Jurisdiction, 2020 - 202': pass (4 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p41 'Comparison of Unsheltered Single Adults By Jurisdiction, 2019 – 2023': pass (5 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p45 'Single Adults Experiencing Chronic Homelessness by Jurisdiction, 2019 ': pass (5 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p51 'Veterans Experiencing Homelessness By Jurisdiction, 2019 - 2023': pass (5 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 pp[68, 69] 'People Experiencing Literal Homelessness by Jurisdiction, 20': kept with flags: 14/20 columns do not add up in the source (2022 households_without_children 5,307 vs 5,273; 2022 households_with_adults_and_children 2,329 vs 2,322; 2022 all 7,646 vs 7,605); 2 jurisdiction-years whose household columns do not add up
- MWCOG 2024 p16 'People Experiencing Literal Homelessness by Jurisdiction, 2023 - 2024': pass (2 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p17 'People Experiencing Literal Homelessness by Jurisdiction, 2020-2024*': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p22 '2024 Persons in Families Experiencing Homelessness by Jurisdiction': pass (4 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p23 'Change in Persons in Families Experiencing Homelessness by Jurisdictio': kept with flags: 1/5 columns do not add up in the source (2020 persons_in_families 3,690 vs 3,760)
- MWCOG 2024 p29 'Households With Only Children Under Age 18 By Jurisdiction, 2020 - 202': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p49 'Unsheltered Single Adults Experiencing Homelessness by Jurisdiction, 2': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p52 'Single Adults Experiencing Chronic Homelessness by Jurisdiction, 2020 ': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p60 'Veterans Experiencing Homelessness by Jurisdiction, 2020 - 2024': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 pp[75, 76] 'People Experiencing Literal Homelessness by Jurisdiction, 20': kept with flags: 9/20 columns do not add up in the source (2022 households_without_children 5,154 vs 5,120; 2022 households_with_adults_and_children 2,272 vs 2,265; 2022 all 7,422 vs 7,395); 2 jurisdiction-years whose household columns do not add up
- MWCOG 2025 p17 'People Experiencing Literal Homelessness by Jurisdiction, 2024 - 2025': pass (2 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p18 'People Experiencing Literal Homelessness by Jurisdiction, 2021-2025*': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p22 '2025 Persons in Families Experiencing Homelessness by Jurisdiction': pass (4 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p23 'Change in Persons in Families Experiencing Homelessness by Jurisdictio': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p29 'Households With Only Children Under Age 18 By Jurisdiction, 2021 - 202': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p48 'Comparison of Unsheltered Single Adults by Jurisdiction, 2021 - 2025': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p51 'Single Adults Experiencing Chronic Homelessness by Jurisdiction, 2021 ': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p59 'Veterans Experiencing Homelessness by Jurisdiction, 2021 - 2025': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 pp[73, 74] 'People Experiencing Literal Homelessness by Jurisdiction, 20': pass (20 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p18 'People Experiencing Literal Homelessness by Jurisdiction, 2025-2026': pass (2 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p19 'People Experiencing Literal Homelessness by Jurisdiction, 2019-2026': pass (8 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p24 '2026 Persons in Families Experiencing Homelessness by Jurisdiction': pass (4 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p25 'Change in Persons in Families Experiencing Homelessness by Jurisdictio': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p32 'Households With Only Children Under Age 18 By Jurisdiction, 2022 – 202': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p50 'Comparison of Unsheltered Single Adults by Jurisdiction, 2022 – 2026': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p54 'Single Adults Experiencing Chronic Homelessness by Jurisdiction, 2022 ': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p59 'Veterans Experiencing Homelessness by Jurisdiction, 2022 – 2026': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 pp[79, 80] 'People Experiencing Literal Homelessness by Jurisdiction, 20': pass (20 year/measure columns, 8 jurisdictions + total)
- MWCOG total persons vs HUD PIT overall, CoC-years that differ: 9: MD-600 2020: MWCOG 453 vs HUD 466; MD-600 2021: MWCOG 537 vs HUD 535; MD-600 2022: MWCOG 571 vs HUD 533; MD-600 2023: MWCOG 659 vs HUD 595; MD-600 2024: MWCOG 658 vs HUD 650; MD-600 2025: MWCOG 608 vs HUD 588; VA-602 2019: MWCOG 169 vs HUD 167; VA-604 2019: MWCOG 277 vs HUD 280; VA-604 2025: MWCOG 392 vs HUD 393
- DC-500 MWCOG vs HUD by year: 2019 6,521/6521, 2020 6,380/6380, 2021 5,111/5111, 2022 4,410/4410, 2023 4,922/4922, 2024 5,616/5616, 2025 5,138/5138, 2026 5,363/n/a
- stage_homeless_counts duplicate keys (coc, jurisdiction, year, measure, population, source): 0
- DC-500 2025 recon values: pit_overall 5138 (exp 5138) pass; pit_sheltered_es 3275 (exp 3275) pass; pit_sheltered_th 1065 (exp 1065) pass; pit_unsheltered 798 (exp 798) pass; hic_beds_year_round__es_th_sh 4965 (exp 4965) pass; hic_beds_year_round__th 1385 (exp 1385) pass; hic_beds_year_round__psh 12696 (exp 12696) pass; hic_beds_year_round__rrh 6012 (exp 6012) pass
- HIC projects 2022 ES: 43 projects; total beds 5,159 vs Total row 5159; year-round 4,795 vs summary p1 4795 vs CoC workbook 4795: pass
- HIC projects 2022 SH: 1 projects; total beds 20 vs Total row 20; year-round 20 vs summary p1 20 vs CoC workbook 20: pass
- HIC projects 2022 TH: 71 projects; total beds 1,783 vs Total row 1783; year-round 1,783 vs summary p1 1783 vs CoC workbook 1783: pass
- HIC projects 2022 PSH: 148 projects; total beds 14,467 vs Total row 14467; year-round 14,467 vs summary p1 14467 vs CoC workbook 14467: pass
- HIC projects 2022 RRH: 34 projects; total beds 7,193 vs Total row 7193; year-round 7,193 vs summary p1 7193 vs CoC workbook 7193: pass
- HIC projects 2022 OPH: 35 projects; total beds 6,498 vs Total row 6498; year-round 6,498 vs summary p1 6498 vs CoC workbook 6498: pass
- HIC projects 2023 ES: 38 projects; total beds 4,026 vs Total row 4026; year-round 3,720 vs summary p1 3720 vs CoC workbook 3720: pass
- HIC projects 2023 SH: 1 projects; total beds 20 vs Total row 20; year-round 20 vs summary p1 20 vs CoC workbook 20: pass
- HIC projects 2023 TH: 65 projects; total beds 1,476 vs Total row 1476; year-round 1,476 vs summary p1 1476 vs CoC workbook 1476: pass
- HIC projects 2023 PSH: 138 projects; total beds 15,349 vs Total row 15349; year-round 15,349 vs summary p1 15349 vs CoC workbook 15349: pass
- HIC projects 2023 RRH: 35 projects; total beds 9,206 vs Total row 9206; year-round 9,206 vs summary p1 9206 vs CoC workbook 9206: pass
- HIC projects 2023 OPH: 15 projects; total beds 5,381 vs Total row 5381; year-round 5,381 vs summary p1 5381 vs CoC workbook 5381: pass
- HIC projects 2024 ES: 46 projects; total beds 4,000 vs Total row 4000; year-round 3,505 vs summary p1 3505 vs CoC workbook 3505: pass
- HIC projects 2024 SH: 1 projects; total beds 20 vs Total row 20; year-round 20 vs summary p1 20 vs CoC workbook 20: pass
- HIC projects 2024 TH: 70 projects; total beds 1,693 vs Total row 1693; year-round 1,693 vs summary p1 1693 vs CoC workbook 1693: pass
- HIC projects 2024 PSH: 154 projects; total beds 11,856 vs Total row 11856; year-round 11,856 vs summary p1 11856 vs CoC workbook 11856: pass
- HIC projects 2024 RRH: 33 projects; total beds 10,156 vs Total row 10156; year-round 10,156 vs summary p1 10156 vs CoC workbook 10156: pass
- HIC projects 2024 OPH: 19 projects; total beds 5,842 vs Total row 5842; year-round 5,842 vs summary p1 5842 vs CoC workbook 5842: pass
- HIC projects 2025 ES: 45 projects; total beds 3,954 vs Total row 3954; year-round 3,580 vs summary p1 3580 vs CoC workbook 3580: pass
- HIC projects 2025 TH: 64 projects; total beds 1,385 vs Total row 1385; year-round 1,385 vs summary p1 1385 vs CoC workbook 1385: pass
- HIC projects 2025 PSH: 159 projects; total beds 12,696 vs Total row 12696; year-round 12,696 vs summary p1 12696 vs CoC workbook 12696: pass
- HIC projects 2025 RRH: 26 projects; total beds 6,012 vs Total row 6012; year-round 6,012 vs summary p1 6012 vs CoC workbook 6012: pass
- HIC projects 2025 OPH: 16 projects; total beds 4,989 vs Total row 4989; year-round 4,989 vs summary p1 4989 vs CoC workbook 4989: pass
- stage_hic_projects duplicate keys (year, type, page, seq): 0
- Calvary HIC 2025 rows pass (7 projects, 124 beds); 2024 Sisters Rise PSH [24] (exp [24])

### 2026-10-10 17:38 — 33_pull_usaspending: stage fact_gov_awards
- interim/stage_fact_gov_awards__federal.csv: 28207 rows; {"named_job_rows_dropped": 1, "usaspending_sub_reports": 11875, "usaspending_prime": 7163, "usaspending_sub": 10733, "fac_reports_kept": 1841, "fac_reports_used": 1831, "fac_lines": 9851, "fac_reports_identical_sefa": 18, "slfrf_dc_report_rows": 462, "slfrf_dc_rows": 461, "named_comparators": {"311597223": {"rows": 51, "by_source_flow": {"usaspending/prime": 2, "usaspending/subaward": 17, "fac_sefa/pass_through_expenditure": 30, "fac_sefa/prime": 2}, "fac_audit_years": ["2020", "2021", "2022", "2023", "2024", "2025"], "fac_expenditure_by_fy": {"2020": 1043889, "2021": 2781894, "2022": 6904511, "2023": 3279830, "2024": 4249604, "2025": 3358800}, "usaspending_amount": 8294415}, "882046704": {"rows": 0, "by_source_flow": {}, "fac_audit_years": [], "fac_expenditure_by_fy": {}, "usaspending_amount": 0}}, "rows": 28207, "duplicate_ids": 0, "rows_missing_provenance": 0, "by_source_flow": {"usaspending/prime": 7162, "usaspending/subaward": 10733, "fac_sefa/prime": 4492, "fac_sefa/pass_through_expenditure": 5359, "treasury_slfrf/subaward": 461}, "ein_filled": 23149}
- Calvary reconciliation: {"fac_fy22_total": 4067718, "fac_fy22_ok": true, "fac_ay2023_total": 4064718, "fac_ay2023_conflict_rows": 4, "hud_14251": [200000], "hud_ok": true, "ppp": [327200], "usaspending_subawards": [["14.252", 25000]], "slfrf": [113488, 3680675], "slfrf_ok": true, "calvary_rows": 13}
- EIN coverage (scope = calvary, core_peers, dc_sector, dmv_sector): {"scope_orgs": 4920, "orgs_with_any_row_by_ein": 234, "by_source": {"usaspending": 185, "fac_sefa": 234, "treasury_slfrf": 2}, "extra_orgs_by_exact_name_state_candidate_only": 60}

### 2026-10-10 17:38 — 35_pull_grantsgov: opportunities
- universe posted+forecasted 1467; candidates 531 (local cfdaList 3, cfda key 3, keyword search 530, title regex 51); fetched 0 (reused 531 saved responses); fetch failures 0; dropped by local filter 245
- interim/stage_fact_opportunities__grantsgov.csv: 286 rows (173 posted, 113 forecasted); duplicate ids 0
- keyword_hits counts: {"homelessness": 6, "housing": 17, "domestic violence": 5, "victim services": 2, "women": 59, "substance use": 47, "workforce": 98, "reentry": 5, "veterans": 19, "aging": 77}
- target-ALN rows: 3; nonprofit-eligible (12/13/25/99): 263
- manifest raw/grantsgov/20261010T173845_pull35_manifest.json

### 2026-10-10 17:39 — 41_pull_soi_extracts: stage
- universe EINs: 15,812
- 990 2012 (12eofinextract990.zip): 294,019 rows read, 2,255 universe rows; fields absent this year: grants_paid, compensation_total, cash_savings_eoy
- 990 2013 (13eofinextract990.zip): 289,603 rows read, 2,255 universe rows
- 990 2014 (14eofinextract990.zip): 299,405 rows read, 2,334 universe rows
- 990 2015 (15eofinextract990.zip): 294,782 rows read, 2,252 universe rows
- 990 2016 (16eofinextract990.zip): 307,483 rows read, 2,421 universe rows
- 990 2017 (17eofinextract990.zip): 300,910 rows read, 2,426 universe rows
- 990 2018 (18eoextract990.zip): 313,339 rows read, 2,514 universe rows
- 990 2019 (19eoextract990.zip): 304,441 rows read, 2,520 universe rows
- 990 2020 (20eoextract990.zip): 273,971 rows read, 2,294 universe rows
- 990 2021 (21eoextract990.zip): 342,920 rows read, 2,874 universe rows
- 990 2022 (22eoextract990.zip): 326,123 rows read, 2,802 universe rows
- 990 2023 (23eoextract990.zip): 338,048 rows read, 2,831 universe rows
- 990 2024 (24eoextract990.zip): 345,365 rows read, 2,985 universe rows
- 990EZ 2012 (12eofinextract990ez.zip): 223,348 rows read, 593 universe rows
- 990EZ 2013 (13eofinextract990ez.zip): 218,981 rows read, 613 universe rows
- 990EZ 2014 (14eofinextract990ez.zip): 234,820 rows read, 659 universe rows
- 990EZ 2015 (15eofinextractEZ.zip): 223,028 rows read, 669 universe rows
- 990EZ 2016 (16eofinextractez.zip): 230,745 rows read, 738 universe rows
- 990EZ 2017 (17eofinextractEZ.zip): 218,097 rows read, 731 universe rows
- 990EZ 2018 (18eoextractez.zip): 226,533 rows read, 766 universe rows
- 990EZ 2019 (19eoextractez.zip): 218,671 rows read, 777 universe rows
- 990EZ 2020 (20eoextractez.zip): 154,314 rows read, 536 universe rows
- 990EZ 2021 (21eoextractez.zip): 218,733 rows read, 867 universe rows
- 990EZ 2022 (22eoextractez.zip): 231,289 rows read, 990 universe rows
- 990EZ 2023 (23eoextractez.zip): 207,536 rows read, 933 universe rows
- 990EZ 2024 (24eoextract990EZ.zip): 203,699 rows read, 986 universe rows
- 990PF 2012 (12eofinextract990pf.zip): 98,948 rows read, 2,671 universe rows; fields absent this year: x_pf_grants_approved_future
- 990PF 2013 (13eofinextract990pf.zip): 100,484 rows read, 2,755 universe rows
- 990PF 2014 (14eofinextract990pf.zip): 101,381 rows read, 2,904 universe rows
- 990PF 2015 (15eofinextract990pf.zip): 103,000 rows read, 2,935 universe rows
- 990PF 2016 (16eofinextract990pf.zip): 105,239 rows read, 3,131 universe rows
- 990PF 2020 (20eoextract990pf.zip): 91,473 rows read, 3,022 universe rows
- 990PF 2021 (21eoextract990pf.zip): 125,312 rows read, 4,417 universe rows
- 990PF 2022 (22eoextract990pf.zip): 115,024 rows read, 4,268 universe rows
- 990PF 2023 (23eoextract990pf.zip): 120,350 rows read, 4,589 universe rows
- 990PF 2024 (24eoextract990pf.zip): 119,059 rows read, 4,796 universe rows
- SOI: 78,109 rows, 9,446 EINs; 0 older-processing-year copies dropped; 0 rows whose copies disagree on total_revenue
- NCCS 2009: 48,857 rows read, 280 universe 990 rows
- NCCS 2010: 184,553 rows read, 932 universe 990 rows
- NCCS 2011: 241,595 rows read, 1,272 universe 990 rows
- NCCS 2012: 273,429 rows read, 1,485 universe 990 rows
- NCCS 2013: 303,225 rows read, 1,645 universe 990 rows
- NCCS 2014: 335,066 rows read, 1,783 universe 990 rows
- NCCS 2015: 358,459 rows read, 1,962 universe 990 rows
- NCCS 2016: 374,252 rows read, 2,045 universe 990 rows
- NCCS 2017: 391,170 rows read, 2,163 universe 990 rows
- NCCS 2018: 406,376 rows read, 2,255 universe 990 rows
- NCCS 2019: 436,217 rows read, 2,393 universe 990 rows
- NCCS 2020: 485,459 rows read, 2,675 universe 990 rows
- NCCS 2021: 491,127 rows read, 2,558 universe 990 rows
- NCCS 2022: 131,588 rows read, 350 universe 990 rows
- NCCS: 22,573 rows staged, 3,105 EINs, tax years 2010-2022; period from SOI match 22,555, from IRS index 18; dropped 901 with no period; 309 EIN-years had >1 return (kept the latest OBJECT_ID)
- NCCS total_revenue equals SOI total_revenue on 99.1% of 22,555 matched rows
- wrote 100,682 rows to interim/stage_fact_org_financials__soi.csv (SOI 78,109; NCCS 22,573)
- duplicate (ein, tax_period_end, return_type, source_id): 0
- Calvary total_revenue QC: bulk_irs_soi_extract TY2020 3,851,984 OK; bulk_irs_soi_extract TY2021 8,867,250 OK; bulk_nccs_efile TY2020 3,851,984 OK; bulk_nccs_efile TY2021 not present
- 990-PF SOI TAX_YR equals derived tax_year on 100.0% of rows
- rows by fiscal_year (period-end year) x return_type / source:
```
source_id   irs_soi_extract              nccs_efile     All
return_type             990 990EZ  990PF        990        
fiscal_year                                                
2002                      0     0      1          0       1
2003                      1     0      1          0       2
2004                      0     0      1          0       1
2005                      1     0      1          0       2
2006                      0     0      1          0       1
2007                      0     2      3          0       5
2008                      2    12      7          0      21
2009                      4    30     14          0      48
2010                    179    93     84          5     361
2011                   1876   519   2408        826    5629
2012                   2227   624   2756       1381    6988
2013                   2279   626   2831       1558    7294
2014                   2299   670   2974       1662    7605
2015                   2365   708   3040       1856    7969
2016                   2445   739    310       1979    5473
2017                   2494   750     23       2078    5345
2018                   2566   763    110       2181    5620
2019                   2625   802   3462       2303    9192
2020                   2649   848   3905       2539    9941
2021                   2761   833   4206       2685   10485
2022                   2852   872   4435       1513    9672
2023                   2862   882   4560          7    8311
2024                    276    85    355          0     716
All                   32763  9858  35488      22573  100682
```
- coverage, bulk_irs_soi_extract (EINs with >=1 row / universe EINs; org-years; median years per covered org):
  - calvary: 1/1; 13; 13
  - calvary_known_funders: 84/88; 881; 10
  - core_peers: 18/18; 235; 13
  - daf_sponsors: 15/15; 184; 13
  - dc_sector: 524/1,027; 4,620; 11
  - dmv_funders: 5,744/7,705; 44,487; 10
  - dmv_sector: 1,942/4,910; 15,530; 9
  - named_comparators: 2/2; 14; 7
  - national_women: 1,395/2,878; 13,420; 12
  - size_matched: 564/566; 6,892; 13
- coverage, bulk_nccs_efile (EINs with >=1 row / universe EINs; org-years; median years per covered org):
  - calvary: 1/1; 7; 7
  - calvary_known_funders: 33/88; 267; 9
  - core_peers: 18/18; 172; 10
  - daf_sponsors: 15/15; 84; 6
  - dc_sector: 370/1,027; 2,550; 7
  - dmv_funders: 650/7,705; 4,046; 6
  - dmv_sector: 1,140/4,910; 7,857; 7
  - named_comparators: 1/2; 11; 11
  - national_women: 959/2,878; 7,769; 9
  - size_matched: 558/566; 4,840; 10

### 2026-10-10 17:39 — 42_pull_propublica: stage
- 2,538 org JSONs read (0 target EINs with no ProPublica record); 18,279 filings_with_data rows; skipped formtypes {}; 0 bad periods
- tax_prd_yr equals derived fiscal_year (period-end year) on 100.0% of rows
- staged 18,279 rows, 2,004 EINs -> interim/stage_fact_org_financials__propublica.csv; duplicates on (ein, tax_period_end, return_type, source_id): 0
- Calvary total_revenue QC: TY2020 3,851,984 OK; TY2021 8,867,250 OK
- cross-check vs SOI: 18,279 matching (ein, period, form) rows; equal total_revenue 100.0%, total_expenses 100.0%, total_assets_eoy 100.0%
- ProPublica rows with no SOI row: 0 (by fiscal_year {})
- rows by fiscal_year x return_type:
```
return_type   990  990EZ  990PF    All
fiscal_year                           
2007            0      1      1      2
2008            0      1      1      2
2009            0      3      4      7
2010           53     20     20     93
2011          392     61    812   1265
2012          440     70    936   1446
2013          448     65    960   1473
2014          448     66    999   1513
2015          465     72   1017   1554
2016          476     66    107    649
2017          484     69      4    557
2018          493     71     15    579
2019          513     73   1082   1668
2020          511     75   1182   1768
2021          536     74   1229   1839
2022          550     69   1245   1864
2023          550     76   1243   1869
2024           28      4     99    131
All          6387    936  10956  18279
```

### 2026-10-10 17:39 — 46_web_named_comparators (stage)
- staged 396 rows -> interim/stage_fact_grants__web_named.csv (exact duplicates dropped 1); recipients {'311597223': 391, '882046704': 5}
- by source_type {'annual_report': 350, 'support_page': 33, 'web': 13}; amount_kind {'unknown': 353, 'mixed': 33, 'cash': 8, 'noncash': 2}; with amount 8, with band 354
- by fiscal_year {2023: 204, 2024: 2, 2025: 155, 2026: 35}
- non-organization entries counted per band only: 570 -> interim/web_named_donor_band_counts.csv; joint credits with a personal name: 6 trimmed to the organization, 1 dropped
- per page (entries, kept, dropped as non-org, status): nc_dwc_ar_2024 669/203/422/ok; nc_dwc_ar_web 277/148/112/ok; nc_dwc_gala_2025 26/4/18/ok; nc_dwc_gala_2026 54/29/18/ok; nc_dwc_rosas_place_pr 1/1/0/ok; nc_dwc_hilton_2026 1/1/0/ok; nc_dwc_ahmanson_grants 2/2/0/ok; nc_dwc_bscf_grantee 1/1/0/ok; nc_dwc_foxwynd 1/1/0/ok; nc_dwc_anthem_2023 1/1/0/ok; nc_dwc_anthem_2026_dwc_pr 1/1/0/ok; nc_cbw_sheworks 1/1/0/ok; nc_cbw_launch_pr 1/1/0/ok; nc_cbw_lacare_pr 2/2/0/ok; nc_cbw_econ_mobility 1/1/0/ok
- this run: Tavily search 0, extract 0, HTTP GET 0, cache hits 0; cumulative (manifest): search 139/300, extract 15/200, HTTP 150; script-46 totals: search 30/30, extract 5/15

### 2026-10-10 17:40 — 45_stage_web_grants
- staged rows 1012: by source_type {'support_page': 249, 'annual_report': 627, 'web': 136}; confidence {'medium': 985, 'high': 27}
- amount stated 34; band only 389; unknown 589
- recipient Calvary 268; core peers 736 (14 peers); whole-list keyword keeps 8
- Calvary-site rows by type {'support_page': 98, 'annual_report': 74, 'anonymous_skipped': 1, 'web': 90}
- pages parsed 20/65; not parsed or failed: nsv_funding_reports (index page (links to annual reports)); openarms_about (no funder list on the site); nebw_reports (index page (links to annual reports)); nebw_ar_2025 (2025 annual report text has no funder list); msp_ar_fy22 (no funder list); dcsafe_ar_fy25 (no funder list (revenue split only)); nuvaya_fin_reports (HTTP 403 and Tavily extract empty); christhouse_ar_2025 (landing page; PDF has no text layer); christhouse_ar_2025_pdf (image-only PDF (12 chars of text)); ehdc_ar_2024 (landing page); ehdc_ar_2024_pdf (2024 annual report text has no funder list); cfh_ar_list (index page); thrive_impact_2024 (lists corporate volunteer groups, not funders); miriams_financials (index page); miriams_ar_fy25 (mkannualreport.org is JavaScript-rendered; no text retrieved); coh_ar_2025 (2025 annual report summary has no funder list); coh_impact_2024 (same list as coh_funders (parsed there)); chgw_home (home page); chgw_impact_fy24 (FY24 impact report text has no funder list); doorways_ar_2023 (landing page); doorways_ar_2023_issuu (issuu viewer; no document text); hormd_honor_roll (URL now serves the About Us page; no honor roll content); hormd_honor_roll_tav (Tavily advanced extract also returns no honor roll content); hormd_ar_2024 (PDF returns HTTP 404); hormd_ar_page (annual report page has no donor list); meyer_118m_28 (2020 list (outside 2024-2026); no Calvary or peers); meyer_635k_8 (2022 list (outside 2024-2026); no Calvary or peers); meyer_rapid (program description only; no 
- in-kind evidence rows 17: MGAC=unclear; MGAC=in_kind; MGAC=in_kind; MGAC=cash; Health Equity Fund=cash; Health Equity Fund=cash; Health Equity Fund=cash; Health Equity Fund=cash; Capital One=unclear; Capital One=unclear; Capital One=cash; World Bank Community Connections Fund=cash; World Bank Community Connections Fund=cash; World Bank Community Connections Fund=cash; Frontier Co-op / Aura Cacia (Frontier Co-op Giving Fund)=in_kind; Frontier Co-op / Aura Cacia (Frontier Co-op Giving Fund)=unclear; MGAC; Capital One; World Bank Community Connections Fund=unclear
- Tavily usage to date (manifest, scripts 43-44): search 139/300, extract 15/200; plus 1 exploratory search during development (same query as cal_audit_fy24; response not saved). HTTP GETs 150.
- appended notes_for_analysis.md 'Web funder data' and open_questions.md

### 2026-10-10 17:40 — 50_parse_xml: progress
- 2,000/31,483 parsed in 0.6 min; grants 698,214, roles 22,703, relationships 5,719; errors 0

### 2026-10-10 17:40 — 50_parse_xml: progress
- 4,000/31,483 parsed in 0.6 min; grants 764,178, roles 41,319, relationships 9,850; errors 0

### 2026-10-10 17:40 — 50_parse_xml: progress
- 6,000/31,483 parsed in 0.7 min; grants 804,949, roles 56,969, relationships 10,909; errors 0

### 2026-10-10 17:40 — 50_parse_xml: progress
- 8,000/31,483 parsed in 0.7 min; grants 833,478, roles 71,614, relationships 11,579; errors 0

### 2026-10-10 17:40 — 50_parse_xml: progress
- 10,000/31,483 parsed in 0.8 min; grants 855,931, roles 83,719, relationships 11,966; errors 0

### 2026-10-10 17:40 — 50_parse_xml: progress
- 12,000/31,483 parsed in 0.8 min; grants 872,756, roles 94,450, relationships 12,310; errors 0

### 2026-10-10 17:40 — 50_parse_xml: progress
- 14,000/31,483 parsed in 0.8 min; grants 885,831, roles 104,143, relationships 12,537; errors 0

### 2026-10-10 17:40 — 50_parse_xml: progress
- 16,000/31,483 parsed in 0.8 min; grants 896,903, roles 112,869, relationships 12,668; errors 0

### 2026-10-10 17:40 — 50_parse_xml: progress
- 18,000/31,483 parsed in 0.9 min; grants 906,213, roles 120,818, relationships 12,795; errors 0

### 2026-10-10 17:40 — 50_parse_xml: progress
- 20,000/31,483 parsed in 0.9 min; grants 913,736, roles 128,324, relationships 12,858; errors 0

### 2026-10-10 17:40 — 50_parse_xml: progress
- 22,000/31,483 parsed in 0.9 min; grants 919,338, roles 135,218, relationships 12,862; errors 0

### 2026-10-10 17:40 — 50_parse_xml: progress
- 24,000/31,483 parsed in 0.9 min; grants 923,248, roles 141,620, relationships 12,864; errors 0

### 2026-10-10 17:40 — 50_parse_xml: progress
- 26,000/31,483 parsed in 0.9 min; grants 925,353, roles 148,088, relationships 12,864; errors 0

### 2026-10-10 17:40 — 50_parse_xml: progress
- 28,000/31,483 parsed in 1.0 min; grants 926,494, roles 154,519, relationships 12,864; errors 0

### 2026-10-10 17:40 — 50_parse_xml: progress
- 30,000/31,483 parsed in 1.0 min; grants 926,838, roles 160,722, relationships 12,864; errors 0

### 2026-10-10 17:41 — 50_parse_xml: done
- parsed 31,483 of 31,483 returns in 1.0 min; errors 0 -> xml_parse_errors.csv
- interim/stage_fact_org_financials__xml.csv: 31,483 rows {'990PF': 24877, '990': 4872, '990EZ': 1734}; amended 335; EIN differs from index 0
- interim/stage_fact_grants__xml.csv: 926,887 rows
- interim/stage_fact_roles__xml.csv: 163,918 rows
- interim/stage_fact_org_relationships__xml.csv: 12,864 rows
- interim/org_profile__xml.csv: 31,483 rows (6,774 EINs; street kept on latest return only)
- interim/xml_schedule_i_part3.csv: 1,730 Schedule I Part III lines (aggregates, no names)
- schema versions: {'2014v5.0': 1, '2014v6.0': 1, '2015v2.1': 1, '2015v3.0': 1, '2016v3.0': 2, '2017v2.3': 2, '2018v3.1': 2, '2019v5.1': 1, '2019v5.2': 1, '2020v4.0': 1671, '2020v4.1': 2870, '2020v4.2': 423, '2021v4.0': 1467, '2021v4.1': 767, '2021v4.2': 3218, '2022v4.0': 4, '2022v4.1': 248, '2022v5.0': 5526, '2023v4.0': 271, '2023v5.0': 2462, '2023v5.1': 2421, '2023v6.0': 960, '2024v5.0': 1374, '2024v5.1': 1978, '2024v5.2': 2496, '2024v5.5': 372, '2025v4.0': 1220, '2025v4.1': 1441, '2025v4.2': 282}
- DAF1 sponsors, Schedule I kept only for DC/MD/VA recipients (all years in scope):
  - FIDELITY INVESTMENTS CHARITABLE GIFT FUND (110303001): national 372,180 rows / $58,823.5M; kept DMV 24,496 / $8,007.2M; filtered out $50,816.2M
  - DONOR ADVISED CHARITABLE GIVING INC (311640316): national 257,532 rows / $28,043.2M; kept DMV 17,453 / $4,001.7M; filtered out $24,041.5M
  - NATIONAL PHILANTHROPIC TRUST (237825575): national 83,803 rows / $26,775.7M; kept DMV 6,855 / $3,393.6M; filtered out $23,382.1M
  - VANGUARD CHARITABLE ENDOWMENT PROGRAM (232888152): national 113,808 rows / $12,077.0M; kept DMV 9,471 / $2,022.5M; filtered out $10,054.5M
  - AMERICAN ONLINE GIVING FOUNDATION INC (810739440): national 228,879 rows / $10,079.9M; kept DMV 15,079 / $1,159.3M; filtered out $8,920.6M
  - AMERICAN ENDOWMENT FOUNDATION (341747398): national 65,226 rows / $4,638.5M; kept DMV 5,501 / $441.8M; filtered out $4,196.7M
  - BANK OF AMERICA CHARITABLE GIFT FD (046010342): national 4 rows / $3,249.2M; kept DMV 0 / $0.0M; filtered out $3,249.2M
  - THE AYCO CHARITABLE FOUNDATION (141782466): national 21,612 rows / $2,375.6M; kept DMV 1,874 / $113.0M; filtered out $2,262.5M
  - Renaissance Charitable Foundation Inc (352129262): national 5 rows / $2,288.2M; kept DMV 0 / $0.0M; filtered out $2,288.2M
  - PAYPAL CHARITABLE GIVING FUND (450931286): national 47,570 rows / $1,897.4M; kept DMV 3,864 / $145.8M; filtered out $1,751.5M
  - CHARITIES AID FOUNDATION AMERICA (431634280): national 44,986 rows / $1,870.2M; kept DMV 3,095 / $204.6M; filtered out $1,665.5M
  - THE BLACKBAUD GIVING FUND (460942102): national 35,201 rows / $1,351.7M; kept DMV 2,007 / $135.2M; filtered out $1,216.5M
  - THE GOLDMAN SACHS CHARITABLE GIFT FUND (113813663): national 12,471 rows / $1,056.1M; kept DMV 1,077 / $131.3M; filtered out $924.9M
  - BNY MELLON CHARITABLE GIFT FUND C/O BNY MELLON NA (300748315): national 5,467 rows / $1,022.5M; kept DMV 466 / $17.6M; filtered out $1,004.9M
  - THE US CHARITABLE GIFT TRUST (311663020): national 12,033 rows / $883.9M; kept DMV 984 / $29.0M; filtered out $854.9M

### 2026-10-10 17:41 — 51_qc_xml
- fetch 100.00% of 31,483
- parse errors 0
- PF grants sum exact 99.96% of returns with grants (99.81% of all PF); named-grantee rows cover 93.8% of PF grant dollars
- Calvary revenue checks pass
- Cafritz EIN 526036989; TY2024 to Calvary $170,000
- Calvary grant rows 150 from 50 funders ($4,701,886)
- trace 20/20
- report -> interim/xml_qc.md

### 2026-10-10 17:41 — 60_stage_inputs
- stage_fact_org_financials__inputs.csv: 17 rows
- stage_fact_gov_awards__inputs.csv: 8 rows
- stage_fact_grants__inputs.csv: 360 rows
- stage_fact_roles__inputs.csv: 195 rows

### 2026-10-10 17:43 — 61_resolve_entities
- unique name keys 232,661; alias rows 231,688
- occurrences by method:
match_method  exact_ein  exact_name_city  exact_name_national  exact_name_state  fuzzy_name_city  known_funder  manual  manual_reject  unmatched
role                                                                                                                                            
funder           925013                0                  274                 0                0           227      59             23       3059
pass_through        686                0                 1936                 0                0             0      16              0      14243
recipient        212743           344289                  912             51873            27536             0      48              2     285903

### 2026-10-10 17:44 — 62_build_facts
- fact_org_financials: 150,461 rows
- fact_grants: 928,655 rows
- fact_gov_awards: 40,300 rows
- fact_opportunities: 286 rows
- fact_policy_events: 297 rows
- supp_calvary_individual_donor_bands.csv: copied from stage_supp_calvary_individual_donor_bands.csv
- supp_calvary_program_metrics.csv: copied from stage_supp_calvary_program_metrics.csv
- supp_calvary_strategic_targets.csv: copied from stage_supp_calvary_strategic_targets.csv
- supp_homeless_counts.csv: copied from stage_homeless_counts__hud.csv
- supp_hic_projects.csv: copied from stage_hic_projects__hud.csv
- supp_dc_budget_lines.csv: copied from stage_dc_budget_lines__dc.csv

### 2026-10-10 17:45 — 63_build_dims
- dim_org: 105,190 rows
- dim_funder: 8,928 rows
- dim_program_area: 13 rows
- dim_period: 28 rows
- dim_geo: 246 rows

### 2026-10-10 17:45 — 64_people_relationships
- fact_roles 163,473; dim_person 48,563 (multi-org 2,036); candidate_interlocks 1,270; fact_org_relationships 544,100 {'grant': 432489, 'daf_sponsor_grant': 90830, 'schedule_r_related': 12864, 'shared_board_member': 4162, 'pass_through_funding': 3755}

### 2026-10-10 17:46 — 63_build_dims
- dim_org: 105,190 rows
- dim_funder: 8,928 rows
- dim_program_area: 13 rows
- dim_period: 28 rows
- dim_geo: 246 rows

### 2026-10-10 17:47 — 70_quality_checks
- wrote reports/data_quality.md; duplicates []; portability issues []

### 2026-10-10 17:48 — 80_docs
- data_dictionary rows 542; undocumented columns 0; source_ids missing from registry: none

### 2026-10-10 17:52 — 01_inventory_inputs
- sources/input_inventory.csv: 30 rows (duplicate=1, ok=24, partial=4, unreadable=1)
- registered 30 input_* sources
- period checks: all match

### 2026-10-10 17:52 — 02_extract_inputs
- text dumps: 29 files in raw/inputs_extracted/text
- raw/inputs_extracted/audit_financials.csv: 1089 rows
- raw/inputs_extracted/audit_tieout_checks.csv: 260 rows
- raw/inputs_extracted/sefa_federal_awards.csv: 4 rows
- raw/inputs_extracted/form990_pdf_financials.csv: 362 rows
- raw/inputs_extracted/form990_pdf_people.csv: 113 rows
- raw/inputs_extracted/form990_pdf_schedule_i.csv: 2 rows
- raw/inputs_extracted/funder_mentions.csv: 200 rows
- raw/inputs_extracted/individual_donor_band_counts.csv: 4 rows
- raw/inputs_extracted/board_lists.csv: 82 rows
- raw/inputs_extracted/annual_report_metrics.csv: 178 rows
- raw/inputs_extracted/crm_funders_2023_2026.csv: 160 rows
- raw/inputs_extracted/strategic_plan_targets.csv: 18 rows
- tie-out checks: 260/260 tie
- SEFA: FY15-Audited-Financial-Statements.pdf: SEFA none
- SEFA: 2016-Audited-Financial-Statements.pdf: SEFA none
- SEFA: 2017-Audited-Financial-Statements-Calvary-Women_s-Services.pdf: SEFA none
- SEFA: CWS-FY18-Audit-.pdf: SEFA none
- SEFA: 2019-Audited-Financial-Statements-CWS.pdf: SEFA none
- SEFA: 2020-Audited-Financial-Statements-CWS.pdf: SEFA none
- SEFA: 2021-Audited-Financial-Statements-CWS.pdf: SEFA none
- SEFA: Calvary-Womens-Services-Inc.-9.30.23-FS.pdf: SEFA 4 programs sum 937,999 vs printed total 937,999
- CRM export: 160 orgs, GIFT_TOTAL $10,556,075.88, 877 gifts, last-gift dates 2023-10-16 to 2026-10-03; 21 rows have NUM_GIFTS=1 but GIFT_TOTAL != LAST_CONTRIB_AMT; GIFT_TOTAL window recorded as unconfirmed
- funder names verified in layout text: 171/171
- note: 2015-Form-990-Calvary-Women_s-Services.pdf: Part I not in text layer (page 1 scanned)
- note: 2016-Form-990-Calvary-Women_s-Services.pdf: Part I not in text layer (page 1 scanned)
- note: 2019-990-Form-990-CWS.pdf: Part I not in text layer (page 1 scanned)

### 2026-10-10 17:53 — 20_build_universes
- calvary: 1 EINs
- calvary_known_funders: 88 EINs
- core_peers: 18 EINs
- daf_sponsors: 15 EINs
- dc_sector: 1,027 EINs
- dmv_funders: 7,705 EINs
- dmv_sector: 4,910 EINs
- named_comparators: 2 EINs
- national_women: 2,878 EINs
- size_matched: 566 EINs
- membership rows 17,210; distinct EINs 15,812; e-file rows 45,305; size band $2,483,998–$9,935,990; missing pins {'F3': [], 'DAF1': []}

### 2026-10-10 17:54 — 22_match_known_funders
- names 243; outcomes {('corp_foundation', 'inferred'): 16, ('exact_name_state', 'yes'): 33, ('exact_name_unique', 'yes'): 19, ('fuzzy_name_state', 'yes'): 6, ('manual', 'inferred'): 5, ('manual', 'yes'): 12, ('manual_reject', 'no'): 10, ('unmatched', 'no'): 142}; accepted EINs 88

### 2026-10-10 17:55 — 20_build_universes
- calvary: 1 EINs
- calvary_known_funders: 88 EINs
- core_peers: 18 EINs
- daf_sponsors: 15 EINs
- dc_sector: 1,027 EINs
- dmv_funders: 7,705 EINs
- dmv_sector: 4,910 EINs
- named_comparators: 2 EINs
- national_women: 2,878 EINs
- size_matched: 566 EINs
- membership rows 17,210; distinct EINs 15,812; e-file rows 45,305; size band $2,483,998–$9,935,990; missing pins {'F3': [], 'DAF1': []}

### 2026-10-10 17:59 — 36_parse_dc_awards
- wrote interim/stage_fact_gov_awards__dc.csv: 12,085 rows; by source/section: dc_oversight/dv_grantees 53; dc_oversight/erap_arpa_grants 25; dc_oversight/homelessness_prevention 19; dc_oversight/psh_case_management 90; dc_oversight/singles_shelter_contract_periods 53; dc_oversight/singles_shelter_contracts 50; dc_oversight/singles_shelter_subgrants 6; dc_oversight/youth_dhs_direct_housing 65; dc_oversight/youth_dhs_direct_nonhousing 37; dc_oversight/youth_tcp_housing 44; dc_ovsjg/ovsjg_layer 1267; dc_ovsjg/ovsjg_pdf 118; dc_pass/pass_payments 5494; dc_pass/pass_po 4494; hud_coc/hud_coc 270
- decisions: OVSJG flow_type dc_local_grant unless the stated funding source is federal only (then subaward with OVSJG as pass-through); assistance_listing filled only from the stated funding source (VOCA 16.575, STOP VAWA 16.588, SASP 16.017, Byrne JAG 16.738, JJDP Title II 16.540, Title V 16.548, RSAT 16.593, Coverdell 16.742, ARPA -> SLFRF 21.027); DHS ERAP ARPA/ERA2 shares are subawards (21.027/21.023); HUD CoC rows: TCP-applicant projects -> recipient = sponsor in the project title, flow subaward, pass-through TCP; other applicants -> prime; fiscal_year = CoC competition year (federal_fy).
- OVSJG layer 35: 1267 rows FY2016-FY2025; AGENCY used as grantee, ORGANIZATIONNAME as project title (labels swapped); 6 rows flagged as identical repeats
- OVSJG FY2024 PDF p2: 'Metro DC Community Center Inc., The' amount from text layer: 327000
- OVSJG FY2024 PDF (raw/dc_gov/20261010T123646_ovsjg_funding_recipients_FY2024.pdf): 121 grant rows, total $62,935,024
- OVSJG FY2025 PDF (raw/dc_gov/20261010T123645_ovsjg_funding_recipients_FY2025.pdf): 120 grant rows, total $92,682,681
- OVSJG FY2026 PDF (raw/dc_gov/20261010T123645_ovsjg_funding_recipients_FY2026.pdf): 118 grant rows, total $96,653,604
- OVSJG merge: 241 FY2024/FY2025 layer rows enriched from the PDFs (funding source, period, issue date); 118 PDF rows added (118 FY2026); PDF rows without a layer match: 0 []; layer FY2024/25 rows without a PDF match: 0 []
- DHS oversight provider tables: 442 rows; by section {'erap_arpa_grants': 25, 'homelessness_prevention': 19, 'youth_dhs_direct_nonhousing': 37, 'youth_tcp_housing': 44, 'youth_dhs_direct_housing': 65, 'psh_case_management': 90, 'singles_shelter_contracts': 50, 'dv_grantees': 53, 'singles_shelter_contract_periods': 53, 'singles_shelter_subgrants': 6}; $0 cells skipped: 20
- HUD CoC DC-500: 270 project rows ({2019: 38, 2020: 39, 2021: 40, 2022: 43, 2023: 39, 2024: 36, 2025: 35}); flow {'prime': 66, 'subaward': 204}
- PASS: 18,655 distinct PO suppliers, 73,834 distinct payment suppliers; matched to universe/TCP EINs: 188 PO supplier strings (182 EINs), 258 payment supplier strings (196 EINs); PO methods {'exact_norm_name': 145, 'fuzzy_token_set': 42, 'manual_known_ein': 1}
- PASS fuzzy supplier matches (75): ACCESS HOUSING INC. -> ACCESS HOUSING INC DC (100); ACCESS HOUSING INC. (DC) -> ACCESS HOUSING INC DC (100); AFFORDABLE HOUSING OPPORTUNITI -> AFFORDABLE HOUSING OPPORTUNITIES INC (97); AMERICAN ASSOC OF RESIDENTIAL -> AMERICAN ASSOCIATION OF RESIDENTIAL MORTGAGE REGULATORS (100); AMERICAN SOCIETY OF ADDICTION -> AMERICAN SOCIETY OF ADDICTION MEDICINE INC (100); American Society of Addiction -> AMERICAN SOCIETY OF ADDICTION MEDICINE INC (100); BENNING PARK NEIGHBORHOOD CORP -> BENNING PARK NEIGHBORHOOD ASSOCIATI ON (100); BLACK FEM  INC -> BLACKFEM INC (94); BLACK FEM, INC -> BLACKFEM INC (94); BREASTFEEDING OUTREACH FOR GRE -> BREASTFEEDING OUTREACH FOR GREATER WASHINGTON (93); Breastfeeding Outreach for Gre -> BREASTFEEDING OUTREACH FOR GREATER WASHINGTON (93); CAPITOL HILL COUNSELING A -> CAPITOL HILL COUNSELING AND RESOURCE CENTER INC (100); CARE AND PROGRESS COMMUNITY DE -> CARE AND PROGRESS COMMUNITY DEVELOPMENT (94); CATHOLIC CHARITIES -> CATHOLIC CHARITIES OF THE ARCHDIOCESE OF WASHINGTON INC (100); CENTER FOR ADOPTION SUPPORT -> CENTER FOR ADOPTION SUPPORT AND EDUCATION INC (100); CHILDREN & CHARITY INTERNATION -> CHILDREN & CHARITY INTERNATIONAL (97); COALITION FOR THE HOMELESS, IN -> COALITION FOR THE HOMELESS INC (100); COMMUNITY BRIDGE INC -> COMMUNITY BRIDGES INCORPORATED (97); COMMUNITY CONNECTION -> COMMUNITY CONNECTIONS (98); COMMUNITY FAMILY LIFE SERVICE, -> COMMUNITY FAMILY LIFE SERVICES INC (98); COURTNEY S HOUSE INC -> COURTNEYS HOUSE INC (97); COVENANT HOUSE WASHINGTON -> COVENANT HOUSE WASHINGTON DC (100); Care and Progress Community De -> CARE AND PROGRESS COMMUNITY DEVELOPMENT (94); Catholic Charities of the Archdiocese of -> CATHOLIC CHARITIES OF THE ARCHDIOCESE OF WASHINGTON INC (100); DC ACTION FOR CHILDREN TODAY -> DC ACTION FOR CHILDREN TODAY DC ACT (100); DEAF ABUSED WOMEN'S NETWORK -> DEAF ABUSED WOMEN NETWORK (98); DEEDS OF KINDNESS OUTREACH -> DEEDS OF KINDNESS OUTREACH SERVICES (100); DISABLED VETERANS NATL FOUNDAT -> DISABLED VETERANS NATIONAL FOUNDATION (96); DISTRICT ALLIANCE SAFE HOUSING -> DISTRICT ALLIANCE FOR SAFE HOUSING INC (100); DOORS OF HOPE INC -> DOOR OF HOPE (95); Doors of Hope Inc -> DOOR OF HOPE (95); EXCELLENT COMMUNITY SERVI -> EXCELLENT COMMUNITY SERVICES INC (94); FAMILY MEDICAL COUNSELING -> FAMILY AND MEDICAL COUNSELING SERVICE INC (100); FAR SOUTHEAST FAMILY -> FAR SOUTHEAST FAMILY STRENGTHENING COLLABORATIVE (100); FOUR WALLS DEVELOPEMENT INC. -> FOUR WALLS DEVELOPMENT INC (98); FRY PLUMBING & HEATING -> FRY PLUMBING AND HEATING NON PROFIT (100); FRY PLUMBING AND HEATING -> FRY PLUMBING AND HEATING NON PROFIT (100); Fry Plumbing and Heating -> FRY PLUMBING AND HEATING NON PROFIT (100); HOUSING COUNSELING SERVICE -> HOUSING COUNSELING SERVICES INC (98); HOUSING COUNSELING SERVICES, I -> HOUSING COUNSELING SERVICES INC (100); KEY BRIDGE FOUNDATION -> KEY BRIDGE FOUNDATION FOR EDUCATION AND RESEARCH (100); LITTLE SISTERS OF THE POOR -> LITTLE SISTERS OF THE POOR OF WASHINGTON DC INC (100); LUTHERAN SOCIAL SERVICES -> LUTHERAN SOCIAL SERVICES OF THE NATIONAL CAPITAL AREA INC (100); LUTHERAN SOCIAL SERVICES NATL' -> LUTHERAN SOCIAL SERVICES OF THE NATIONAL CAPITAL AREA INC (100); MARTHA S TABLE INC -> MARTHAS TABLE (96); MARY ELIZABETH HOUSE, INC A MI -> THE MARY ELIZABETH HOUSE INC A MINISTRY (93); MISSION FIRST HOUSING DEVELOPM -> MISSION FIRST HOUSING DEVELOPMENT CORPORATION (95); MOUNT LEBANON COMMUNITY DEVELO -> MOUNT LEBANON COMMUNITY DEVELOPMENT CORPORATION (92); Mission First Housing Developm -> MISSION FIRST HOUSING DEVELOPMENT CORPORATION (95); NAT'L FEDERATION OF THE BLIND -> NATIONAL FEDERATION OF THE BLIND OF THE DISTRICT OF COLUMBIA (100); NATIONAL CENTER FOR CHILDREN A -> NATIONAL CENTER FOR CHILDREN AND FAMILIES (100); NATIONAL CENTER FOR VICTIMS OF -> NATIONAL CENTER FOR VICTIMS OF CRIME INC (100); NATIONAL ENERGY AND UTILITY AF -> THE NATIONAL ENERGY AND UTILITY AFFORDABILITY COALITION (94); NATIONAL FEDERATION OF THE BLIND -> NATIONAL FEDERATION OF THE BLIND OF THE DISTRICT OF COLUMBIA (100); NATIONAL FOUNDATION TO END SEN -> NATIONAL FOUNDATION TO END SENIOR HUNGER INC (93); NEIGHBOR S CONSEJO -> NEIGHBORS CONSEJO (97); NORTHERN VIRGINIA FAMILY -> NORTHERN VIRGINIA FAMILY SERVICES INC (100); National Association of State Mental Health Program Directors -> NATIONAL ASSOCIATION OF STATE MENTAL HEALTH PROGRAM DIRECTORS IN (100); National Center For Victims Of -> NATIONAL CENTER FOR VICTIMS OF CRIME INC (100); OMEGA GOLD DEVELOPMENT GR -> OMEGA GOLD DEVELOPMENT GROUP INC (94); PAVING THE WAY MULTI-SERVICE -> PAVING THE WAY MULTI SERVICE INSTITUTE (100); PSI SERVICE III INC -> PSI SERVICES III INC (97); RAPE, ABUSE, INCEST, NATIONAL -> RAPE ABUSE AND INCEST NATIONAL NETWORK INC (100); RESTORATION COMMUNITY ALLIANCE -> RESTORATION COMMUNITY ALLIANCE COMMUNITY DEVLEOPMENT CORPORATION (100); Rape, Abuse, Incest, National -> RAPE ABUSE AND INCEST NATIONAL NETWORK INC (100); SAMARITAN MINISTRY OF GREATER -> SAMARITAN MINISTRY OF GREATER WASHINGTON (100); SERVICE SOURCE, INC -> SERVICESOURCE INC (96); STEPPINGSTONE FOUNDATION, INC. -> STEPPING STONE FOUNDATION INC (98); SYMBRAL FOUNDATION FOR CMTY. -> SYMBRAL FOUNDATION FOR COMMUNITY SERVICES INC (100); Safe Routes to School National Partnersh -> SAFE ROUTES TO SCHOOL NATIONAL PARTNERSHIP (98); THE HOPE FOUNDATION RE-ENTRY -> HOPE FOUNDATION RE-ENTRY NETWORK INC (100); THE MARY ELIZABETH HOUSE -> THE MARY ELIZABETH HOUSE INC A MINISTRY (100); THE NATIONAL REENTRY NETWORK -> THE NATIONAL REENTRY NETWORK FOR RETURNING CITIZENS (100); Torture abolition and Survivors Support -> TORTURE ABOLITION AND SURVIVORS SUPPORT COALITION INTERNATIONAL (100); WASHINGTON REGIONAL ALCOHOL PR -> WASHINGTON REGIONAL ALCOHOL PROGRAM (95)
- PASS POs for universe vendors: 5,602 raw rows -> 4,494 after dedupe on PONUMBER + FISCALYEAR + POTOTAL (repeats removed: 1,108, almost all AA0 sub-office fan-out)
- PASS payments for universe vendors: 5,494 supplier x FY x agency x PO aggregates; FY2025+ rows flagged x_pass_incomplete_fy=1 (PASS incomplete from FY2025, financial-system change)
- fuzzy name matches in DC/HUD documents (21): CENTER FOR NON- PROFIT ADVANCEMENT -> CENTER FOR NONPROFIT ADVANCEMENT (98); CENTER FOR NON-PROFIT ADVANCEMENT -> CENTER FOR NONPROFIT ADVANCEMENT (98); Calvary Women's Service -> CALVARY WOMENS SERVICES INC (98); Catholic Charities -> CATHOLIC CHARITIES OF THE ARCHDIOCESE OF WASHINGTON INC (100); Catholic Charities of the Archdiocese of -> CATHOLIC CHARITIES OF THE ARCHDIOCESE OF WASHINGTON INC (100); Community Family Live Services -> COMMUNITY FAMILY LIFE SERVICES INC (97); Covenant House -> COVENANT HOUSE WASHINGTON DC (100); Covenant House Greater Washington -> COVENANT HOUSE WASHINGTON DC (94); Covenant House Washington -> COVENANT HOUSE WASHINGTON DC (100); DISTRICT ALLIANCE SAFE HOUSING -> DISTRICT ALLIANCE FOR SAFE HOUSING INC (100); Deaf Abused Women's Network -> DEAF ABUSED WOMEN NETWORK (98); Deaf Abused Women's Network (DAWN) -> DEAF ABUSED WOMEN NETWORK (98); Everyone Home -> EVERYONE HOME DC (100); Housing Counseling Service -> HOUSING COUNSELING SERVICES INC (98); Institute for African Man Development Inc. -> INSTITUTE FOR AFRICAN MAN DEVELOPME NT INC (99); Pathways to Housing -> PATHWAYS TO HOUSING DC (100); SURVIVORS AND ADVOCATES FOR EMPOWERM ENT (DC SAFE) -> SURVIVORS AND ADVOCATES FOR EMPOWERMENT SAFE INC (92); SURVIVORS AND ADVOCATES FOR EMPOWERMENT (SAFE) -> SURVIVORS AND ADVOCATES FOR EMPOWERMENT SAFE INC (100); Survivors and Advocates for Empowerment, Inc. -> SURVIVORS AND ADVOCATES FOR EMPOWERMENT SAFE INC (100); The Hope Foundation Reentry Network Inc. -> HOPE FOUNDATION RE-ENTRY NETWORK INC (92); The National Centers for Children and Families -> NATIONAL CENTER FOR CHILDREN AND FAMILIES (99)
- DHS oversight tie-out: 2024 erap_arpa_grants [ARPA] printed $42,070,444 vs parsed $42,070,444 -> tie
- DHS oversight tie-out: 2024 erap_arpa_grants [ERA2] printed $6,326,098 vs parsed $6,326,098 -> tie
- DHS oversight tie-out: 2024 erap_arpa_grants [Local] printed $576,903 vs parsed $576,903 -> tie
- DHS oversight tie-out: 2025 dv_grantees [FY2024 total grant award] printed $4,462,363 vs parsed $4,462,363 -> tie
- DHS oversight tie-out: 2025 dv_grantees [FY2025 total grant award] printed $4,847,166 vs parsed $4,847,167 -> tie
- DHS oversight tie-out: 2025 erap_arpa_grants [ARPA] printed $7,763,167 vs parsed $7,763,167 -> tie
- DHS oversight tie-out: 2025 erap_arpa_grants [ERA2] printed $30,181,471 vs parsed $30,181,472 -> tie
- DHS oversight tie-out: 2025 erap_arpa_grants [Local] printed $22,587,325 vs parsed $22,587,325 -> tie
- DHS oversight tie-out: 2025 homelessness_prevention [FY24] printed $7,450,000 vs parsed $7,450,000 -> tie
- DHS oversight tie-out: 2025 homelessness_prevention [FY25 YTD] printed $6,119,700 vs parsed $6,119,700 -> tie
- DHS oversight tie-out: 2025 psh_case_management [DHS local] printed $25,803,404 vs parsed $25,803,404 -> tie
- DHS oversight tie-out: 2025 psh_case_management [Medicaid] printed $38,687,549 vs parsed $38,687,549 -> tie
- HUD AwardComp DC-500 2019: 38 projects, parsed $22,075,117 vs printed total $22,075,117 -> tie
- HUD AwardComp DC-500 2020: 39 projects, parsed $23,608,105 vs printed total $23,608,105 -> tie
- HUD AwardComp DC-500 2021: 40 projects, parsed $25,062,775 vs printed total $25,062,775 -> tie
- HUD AwardComp DC-500 2022: 43 projects, parsed $27,933,554 vs printed total $27,933,554 -> tie
- HUD AwardComp DC-500 2023: 39 projects, parsed $29,711,325 vs printed total $29,711,325 -> tie
- HUD AwardComp DC-500 2024: 36 projects, parsed $33,659,924 vs printed total $33,659,924 -> tie
- HUD FY2025 round 1 DC-500 (p12): 15 projects, parsed $15,042,362 vs printed $15,042,362 -> tie
- HUD FY2025 round 2 DC-500 (p22): 4 projects, parsed $6,616,773 vs printed $6,616,773 -> tie
- HUD FY2025 round 3 DC-500 (p37): 16 projects, parsed $11,878,879 vs printed $11,878,879 -> tie
- HUD FY2024 AwardComp vs hud.gov DC report: 36 vs 36 projects, total $33,659,924 vs $33,659,924; project-level differences 0: []
- duplicates: award_row_id collisions 0; fully identical rows 0
- Calvary OVSJG rows: 15 (FY2019-FY2025 layer 13, FY2026 PDF 2); match recon: yes
- provider-name match rate (non-PASS): 114/437 distinct names (26%), 903/2097 rows, 49% of dollars; by source {'dc_oversight': '46/93 names, 263/442 rows', 'dc_ovsjg': '73/351 names, 404/1385 rows', 'hud_coc': '19/26 names, 236/270 rows'}; methods {'unmatched': 1194, 'fuzzy_token_set': 136, 'exact_norm_name': 664, 'manual_alias': 68, 'manual_known_ein': 35}

### 2026-10-10 18:00 — 37_parse_dc_budget: DC budget lines and policy events
- interim/stage_dc_budget_lines__dc.csv: 5,172 rows (Counter({'approved': 3172, 'actual': 1968, 'proposed': 32})); in-scope program/agency rows 854; duplicate keys 0
- interim/stage_fact_policy_events__dc.csv: 297 rows; by kind {'change_table_FO0-5': 8, 'change_table_HY0-5': 9, 'change_table_JA0-5': 25, 'yoy_approved_change': 161, 'bsa_subtitle': 25, 'fy2025_change_narrative': 13, 'committee_report_item': 22, 'committee_report_variance': 6, 'change_table_DB0-5': 1, 'council_adjustments_chart_fy2027': 27}; by type {'budget_proposed': 41, 'budget_enacted': 161, 'budget_revised': 66, 'policy_change': 26, 'other': 1, 'program_launch': 2}
- parsed tables: FY2024 JA0 30-PBB (2024_JA0_ja_dhs_tables_2024j.pdf): 62 lines; FY2024 FO0 30-PBB (024_FO0_fo_vsjg_tables_2024j.pdf): 21 lines; FY2024 RM0 30-PBB (2024_RM0_rm_dbh_tables_2024j.pdf): 128 lines; FY2024 DB0 30-PBB (024_DB0_db_dhcd_tables_2024j.pdf): 44 lines; FY2024 HY0 30-PBB (2024_HY0_hy_has_tables_2024j.pdf): 16 lines; FY2024 CF0 30-PBB (2024_CF0_cf_des_tables_2024j.pdf): 69 lines; FY2024 HG0 30-PBB (24_HG0_hg_dmhhs_tables_2024j.pdf): 9 lines; FY2025 JA0 30-PBB (2025_JA0_ja_dhs_tables_2025j.pdf): 61 lines; FY2025 FO0 30-PBB (25_FO0_fo_ovsjg_tables_2025j.pdf): 28 lines; FY2025 RM0 30-PBB (2025_RM0_rm_dbh_tables_2025j.pdf): 87 lines; FY2025 DB0 30-PBB (025_DB0_db_dhcd_tables_2025j.pdf): 36 lines; FY2025 HY0 30-PBB (2025_HY0_hy_hap_tables_2025j.pdf): 7 lines; FY2025 CF0 30-PBB (025_CF0_cf_does_tables_2025j.pdf): 62 lines; FY2025 HG0 30-PBB (25_HG0_hg_dmhhs_tables_2025j.pdf): 8 lines; FY2026 JA0 Table JA0-4 (026_JA0_ja_dhs_chapter_2026o.pdf): 57 lines; FY2026 FO0 Table FO0-4 (26_FO0_fo_vsjg_chapter_2026o.pdf): 26 lines; FY2026 RM0 Table RM0-4 (026_RM0_rm_dbh_chapter_2026o.pdf): 83 lines; FY2026 DB0 Table DB0-4 (26_DB0_db_dhcd_chapter_2026o.pdf): 36 lines; FY2026 HY0 Table HY0-4 (026_HY0_hy_has_chapter_2026o.pdf): 7 lines; FY2026 CF0 Table CF0-4 (26_CF0_cf_does_chapter_2026o.pdf): 61 lines; FY2026 HG0 Table HG0-4 (6_HG0_hg_dmhhs_chapter_2026o.pdf): 6 lines; FY2027 JA0 30-PBB (7_JA0_ja0_dhs_tables_2027a_0.pdf): 57 lines; FY2027 FO0 30-PBB (FO0_fo0_ovsjg_tables_2027a_0.pdf): 26 lines; FY2027 RM0 30-PBB (7_RM0_rm0_dbh_tables_2027a_0.pdf): 80 lines; FY2027 DB0 30-PBB (_DB0_db0_dhcd_tables_2027a_0.pdf): 36 lines; FY2027 HY0 30-PBB (7_HY0_hy0_hap_tables_2027a_0.pdf): 7 lines; FY2027 CF0 30-PBB (_CF0_cf0_does_tables_2027a_0.pdf): 61 lines; FY2027 HG0 30-PBB (HG0_hg0_dmhhs_tables_2027a_0.pdf): 7 lines
- change items: FY2024 JA0 Table JA0-5: 29 change lines, 7 in scope; FY2024 FO0 Table FO0-5: 14 change lines, 3 in scope; FY2024 RM0 Table RM0-5: 25 change lines, 0 in scope; FY2024 DB0 Table DB0-5: 14 change lines, 0 in scope; FY2024 HY0 Table HY0-5: 6 change lines, 6 in scope; FY2024 CF0 Table CF0-5: 16 change lines, 0 in scope; FY2024 HG0 Table HG0-5: 7 change lines, 0 in scope; FY2025 JA0 narrative change sentences (pypdfium2): 8 in scope; FY2025 FO0: chapter change text is font-garbled (amounts missing); OVSJG FY2025 changes taken from the JPS committee report; FY2025 RM0 narrative change sentences (pypdfium2): 0 in scope; FY2025 DB0 narrative change sentences (pypdfium2): 2 in scope; FY2025 HY0 narrative change sentences (pypdfium2): 3 in scope; FY2025 CF0 Table CF0-5: 20 change lines, 0 in scope; FY2025 HG0 narrative change sentences (pypdfium2): 0 in scope; FY2026 JA0 Table JA0-5: 29 change lines, 14 in scope; FY2026 FO0 Table FO0-5: 16 change lines, 4 in scope; FY2026 RM0 Table RM0-5: 27 change lines, 0 in scope; FY2026 DB0 Table DB0-5: 16 change lines, 0 in scope; FY2026 HY0 Table HY0-5: 2 change lines, 2 in scope; FY2026 CF0 Table CF0-5: 17 change lines, 0 in scope; FY2026 HG0 Table HG0-5: 4 change lines, 0 in scope; FY2027 JA0 Table JA0-5: 15 change lines, 4 in scope; FY2027 FO0 Table FO0-5: 11 change lines, 1 in scope; FY2027 RM0 Table RM0-5: 17 change lines, 0 in scope; FY2027 DB0 Table DB0-5: 15 change lines, 1 in scope; FY2027 HY0 Table HY0-5: 3 change lines, 1 in scope; FY2027 CF0 Table CF0-5: 8 change lines, 0 in scope; FY2027 HG0 Table HG0-5: 3 change lines, 0 in scope
- committee report tables: BR_FY25_Housing -> 1 in-scope proposed activity rows (markup 2024-05-09); BR_FY25_JPS -> 0 in-scope proposed activity rows (markup not printed); BR_FY26_committee_budget_report_Human-Services -> 18 in-scope proposed activity rows (markup 2025-06-24); BR_FY26_committee_budget_report_Housing -> 5 in-scope proposed activity rows (markup 2025-06-24); BR_FY26_committee_budget_report_JPS -> 2 in-scope proposed activity rows (markup not printed); BR_FY26_committee_budget_report_Health -> 0 in-scope proposed activity rows (markup 2025-06-23); BR_FY27_committee_budget_report_DRAFT-FY2027-Committee-on-Health -> 2 in-scope proposed activity rows (markup 2026-05-20); BR_FY27_committee_budget_report_FY27-Committee-on-Housing -> 4 in-scope proposed activity rows (markup not printed); BR_FY27_committee_budget_report_52226-FY2027-JPS -> 0 in-scope proposed activity rows (markup not printed)
- FY2027 Council adjustments chart: 1627 rows read, 27 in-scope events
- BSA subtitles kept: 25; curated committee-report items: 22; YoY approved-change events: 161
- tie-outs: 257 pass, 0 fail
- tie-out detail (in-scope divisions): FY2024 JA0 30-PBB p2 division 5000: sum of 23 activities vs subtotal, deltas by column [0, 0, 0, -1] ($000) -> pass | FY2024 JA0 30-PBB p3 agency total: sum of 8 division subtotals, deltas [0, -2, 0, 1] ($000) -> pass | FY2024 JA0 Table JA0-2 p2: sum of 7 fund rows vs GROSS FUNDS, deltas [-1, 0, -1, 0] ($000) -> pass | FY2024 FO0 30-PBB p1 division 4000: sum of 2 activities vs subtotal, deltas by column [0, 0, 0, -1] ($000) -> pass | FY2024 FO0 30-PBB p1 division 5000: sum of 1 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 FO0 30-PBB p1 division 6000: sum of 5 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 FO0 30-PBB p1 agency total: sum of 7 division subtotals, deltas [-2, -1, -2, 1] ($000) -> pass | FY2024 FO0 Table FO0-2 p2: sum of 5 fund rows vs GROSS FUNDS, deltas [0, 0, -1, 0] ($000) -> pass | FY2024 RM0 30-PBB p5 agency total: sum of 16 division subtotals, deltas [0, 1, 1, 0] ($000) -> pass | FY2024 RM0 Table RM0-2 p2: sum of 9 fund rows vs GROSS FUNDS, deltas [0, 1, 0, 1] ($000) -> pass | FY2024 DB0 30-PBB p2 agency total: sum of 9 division subtotals, deltas [0, 0, 0, -1] ($000) -> pass | FY2024 DB0 Table DB0-2 p2: sum of 5 fund rows vs GROSS FUNDS, deltas [1, -1, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 division 4000: sum of 1 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 division 5000: sum of 1 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 division 6000: sum of 5 activities vs subtotal, deltas by column [2, -1, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 agency total: sum of 5 division subtotals, deltas [0, 0, -1, 0] ($000) -> pass | FY2024 HY0 Table HY0-2 p1: sum of 1 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2024 CF0 30-PBB p2 division 4000: sum of 16 activities vs subtotal, deltas by column [0, 0, 0, -1] ($000) -> pass | FY2024 CF0 30-PBB p2 division 5000: sum of 3 activities vs subtotal, deltas by column [1, 0, 1, 0] ($000) -> pass | FY2024 CF0 30-PBB p2 division 6000: sum of 6 activities vs subtotal, deltas by column [1, 0, 0, 0] ($000) -> pass | FY2024 CF0 30-PBB p3 agency total: sum of 11 division subtotals, deltas [-1, 0, 0, -1] ($000) -> pass | FY2024 CF0 Table CF0-2 p2: sum of 6 fund rows vs GROSS FUNDS, deltas [1, 0, 0, 0] ($000) -> pass | FY2024 HG0 30-PBB p1 agency total: sum of 4 division subtotals, deltas [0, 0, 0, 0] ($000) -> pass | FY2024 HG0 Table HG0-2 p2: sum of 2 fund rows vs GROSS FUNDS, deltas [0, 1, 0, 0] ($000) -> pass | FY2025 JA0 30-PBB p2 division HS0030: sum of 28 activities vs subtotal, deltas by column [-2, 1, -1, 1] ($000) -> pass | FY2025 JA0 30-PBB p2 agency total: sum of 6 division subtotals, deltas [0, -1, 1, 0] ($000) -> pass | FY2025 FO0 30-PBB p1 division PS0023: sum of 2 activities vs subtotal, deltas by column [0, 0, -1, 0] ($000) -> pass | FY2025 FO0 30-PBB p2 agency total: sum of 12 division subtotals, deltas [-1, -2, 1, 0] ($000) -> pass | FY2025 RM0 30-PBB p3 agency total: sum of 13 division subtotals, deltas [1, 1, 0, 1] ($000) -> pass | FY2025 DB0 30-PBB p2 agency total: sum of 6 division subtotals, deltas [0, 1, 1, 0] ($000) -> pass | FY2025 HY0 30-PBB p1 division EC0039: sum of 5 activities vs subtotal, deltas by column [0, -1, 0, 0] ($000) -> pass | FY2025 HY0 30-PBB p1 agency total: sum of 1 division subtotals, deltas [0, 0, 0, 0] ($000) -> pass | FY2025 CF0 30-PBB p3 agency total: sum of 10 division subtotals, deltas [0, -1, 0, -1] ($000) -> pass | FY2025 CF0 Table CF0-2 p2: sum of 6 fund rows vs GROSS FUNDS, deltas [0, -1, 0, 0] ($000) -> pass | FY2025 HG0 30-PBB p1 agency total: sum of 3 division subtotals, deltas [0, 0, 0, 1] ($000) -> pass | FY2026 JA0 Table JA0-4 p5 division HS0030: sum of 28 activities vs subtotal, deltas [1, -2, 1, -1] ($000) -> pass | FY2026 JA0 Table JA0-4 p5 agency total: sum of 5 divisions, deltas [-1, -1, 0, 0] ($000) -> pass | FY2026 JA0 Table JA0-2 p2: sum of 7 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 FO0 Table FO0-4 p4 division PS0023: sum of 2 activities vs subtotal, deltas [0, 1, 0, 0] ($000) -> pass | FY2026 FO0 Table FO0-4 p4 agency total: sum of 11 divisions, deltas [-2, 0, 0, 0] ($000) -> pass | FY2026 FO0 Table FO0-2 p2: sum of 4 fund rows vs GROSS FUNDS, deltas [-1, 0, 0, 0] ($000) -> pass | FY2026 RM0 Table RM0-4 p7 agency total: sum of 13 divisions, deltas [1, 1, 2, 0] ($000) -> pass | FY2026 RM0 Table RM0-2 p2: sum of 8 fund rows vs GROSS FUNDS, deltas [1, 0, -1, 0] ($000) -> pass | FY2026 DB0 Table DB0-4 p4 agency total: sum of 6 divisions, deltas [1, -1, 0, -1] ($000) -> pass | FY2026 DB0 Table DB0-2 p2: sum of 4 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 HY0 Table HY0-4 p2 division EC0039: sum of 5 activities vs subtotal, deltas [-1, 1, 0, 0] ($000) -> pass | FY2026 HY0 Table HY0-4 p2 agency total: sum of 1 divisions, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 HY0 Table HY0-2 p1: sum of 1 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 CF0 Table CF0-4 p5 agency total: sum of 10 divisions, deltas [-1, 1, 0, 0] ($000) -> pass | FY2026 CF0 Table CF0-2 p2: sum of 5 fund rows vs GROSS FUNDS, deltas [-1, 1, 0, 1] ($000) -> pass | FY2026 HG0 Table HG0-4 p3 agency total: sum of 2 divisions, deltas [0, 1, 1, 0] ($000) -> pass | FY2026 HG0 Table HG0-2 p2: sum of 1 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2027 JA0 30-PBB p2 division HS0030: sum of 28 activities vs subtotal, deltas by column [-2, -2, -1, -3] ($000) -> pass | FY2027 JA0 30-PBB p2 agency total: sum of 5 division subtotals, deltas [-1, 1, 0, -1] ($000) -> pass | FY2027 JA0 Table JA0-2 p2: sum of 7 fund rows vs GROSS FUNDS, deltas [0, 1, 0, 0] ($000) -> pass | FY2027 FO0 30-PBB p1 division PS0023: sum of 2 activities vs subtotal, deltas by column [1, 0, 0, 0] ($000) -> pass | FY2027 FO0 30-PBB p1 agency total: sum of 11 division subtotals, deltas [-1,
- cross-book disagreements (same FY/stage/code, >$2K apart; later book preferred via x_preferred): 2022 actual JA0 AMP000 total: FY2025 book 33,466,000, FY2024 book 33,534,000 | 2022 actual JA0 AFO000 total: FY2025 book 3,079,000, FY2024 book 3,025,000 | 2022 actual JA0 HS0029 total: FY2025 book 279,438,000, FY2024 book 280,259,000 | 2022 actual JA0 HS0030 total: FY2025 book 625,848,000, FY2024 book 625,869,000 | 2025 approved JA0 H02902 total: FY2026 book 42,867,000, FY2025 book 42,943,000 | 2025 approved JA0 H02905 total: FY2026 book 91,735,000, FY2025 book 91,660,000 | 2025 approved FO0 P01903 total: FY2026 book 18,405,000, FY2025 book 18,312,000 | 2025 approved FO0 PS0019 total: FY2026 book 18,405,000, FY2025 book 18,312,000 | 2025 approved RM0 AFO003 total: FY2026 book 1,120,000, FY2025 book 1,010,000 | 2025 approved RM0 AFO005 total: FY2026 book 567,000, FY2025 book 577,000 | 2025 approved RM0 AFO000 total: FY2026 book 2,378,000, FY2025 book 2,278,000 | 2025 approved RM0 H04201 total: FY2026 book 175,000, FY2025 book 179,000 | 2025 approved RM0 H04202 total: FY2026 book 1,128,000, FY2025 book 1,151,000 | 2025 approved RM0 H04205 total: FY2026 book 381,000, FY2025 book 355,000 | 2025 approved RM0 H04504 total: FY2026 book 1,367,000, FY2025 book 100,000 | 2025 approved RM0 HS0045 total: FY2026 book 37,390,000, FY2025 book 36,123,000 | 2025 approved RM0 H04802 total: FY2026 book 27,140,000, FY2025 book 22,840,000 | 2025 approved RM0 H04805 total: FY2026 book 1,391,000, FY2025 book 5,691,000 | 2025 approved RM0 HS0053 total: FY2026 book 20,351,000, FY2025 book 21,717,000 | 2025 approved CF0 AFO003 total: FY2026 book 2,141,000, FY2025 book 2,222,000 | 2025 approved CF0 AFO000 total: FY2026 book 4,023,000, FY2025 book 4,104,000 | 2025 approved CF0 AMP026 total: FY2026 book 0, FY2025 book -3,000 | 2025 approved CF0 AMP000 total: FY2026 book 24,947,000, FY2025 book 24,944,000 | 2025 approved CF0 O00111 total: FY2026 book 556,000, FY2025 book 559,000 | 2025 approved CF0 GO0047 total: FY2026 book 6,545,000, FY2025 book 6,548,000 | 2025 approved CF0 O05201 total: FY2026 book 15,504,000, FY2025 book 15,422,000 | 2025 approved CF0 GO0052 total: FY2026 book 75,929,000, FY2025 book 75,847,000
- FY2024 old-code -> FY2025 code crosswalk (FY2024 approved): FO0 P02301: FY2024 book 171,000 vs FY2025 book restated 171,000 (delta +0) | FO0 P02303: FY2024 book 45,515,000 vs FY2025 book restated 45,515,000 (delta +0) | FO0 P04502: FY2024 book 3,720,000 vs FY2025 book restated 3,720,000 (delta +0) | HY0 R03903: FY2024 book 4,400,000 vs FY2025 book restated 4,400,000 (delta +0) | HY0 R03904: FY2024 book 0 vs FY2025 book restated 0 (delta +0) | HY0 R03905: FY2024 book 128,094,000 vs FY2025 book restated 128,094,000 (delta +0) | HY0 R03906: FY2024 book 10,581,000 vs FY2025 book restated 10,581,000 (delta +0) | HY0 R03907: FY2024 book 43,296,000 vs FY2025 book restated 43,296,000 (delta +0) | JA0 H03002: FY2024 book 79,033,000 vs FY2025 book restated 93,339,000 (delta +14,306,000) | JA0 H03003: FY2024 book 59,994,000 vs FY2025 book restated 59,994,000 (delta +0) | JA0 H03004: FY2024 book 31,818,000 vs FY2025 book restated 12,421,000 (delta -19,397,000) | JA0 H03007: FY2024 book 2,940,000 vs FY2025 book restated 2,940,000 (delta +0) | JA0 H03008: FY2024 book 42,536,000 vs FY2025 book restated 42,536,000 (delta +0) | JA0 H03009: FY2024 book 2,799,000 vs FY2025 book restated 4,259,000 (delta +1,460,000) | JA0 H03010: FY2024 book 51,764,000 vs FY2025 book restated 60,770,000 (delta +9,006,000) | JA0 H03011: FY2024 book 4,935,000 vs FY2025 book restated 4,935,000 (delta +0) | JA0 H03012: FY2024 book 86,929,000 vs FY2025 book restated 83,014,000 (delta -3,915,000) | JA0 H03013: FY2024 book 4,222,000 vs FY2025 book restated 4,222,000 (delta +0) | JA0 H03014-H03016: FY2024 book 11,541,000 vs FY2025 book restated 11,542,000 (delta +1,000) | JA0 H03017: FY2024 book 73,209,000 vs FY2025 book restated 73,209,000 (delta +0) | JA0 H03018: FY2024 book 10,875,000 vs FY2025 book restated 10,875,000 (delta +0) | JA0 H03019: FY2024 book 1,150,000 vs FY2025 book restated 1,150,000 (delta +0) | JA0 H03022: FY2024 book 1,980,000 vs FY2025 book restated 1,980,000 (delta +0) | JA0 H03023: FY2024 book 12,032,000 vs FY2025 book restated 12,032,000 (delta +0) | RM0 H04308: FY2024 book 29,637,000 vs FY2025 book restated 29,637,000 (delta +0) | RM0 H04504: FY2024 book 1,467,000 vs FY2025 book restated 1,467,000 (delta +0)
- event dates: budget_enacted/budget_revised = Local Budget Act 2nd reading {2024: '2023-05-30', 2025: '2024-06-12', 2026: '2025-07-28', 2027: '2026-06-23'}; budget_proposed = BSA introduced on behalf of the Mayor {2025: '2024-04-03', 2026: '2025-06-02', 2027: '2026-04-14'} (FY2024 proposal date not in downloaded docs -> blank); BSA policy rows = law/act effective date {2024: '2023-09-06', 2025: '2024-09-18', 2026: '2025-12-06', 2027: '2026-08-13'}; committee items = markup date when printed, else Local Budget Act date
- mapping: Table XX0-5 lines before 'Mayor's Proposed Budget' -> budget_proposed; lines between it and 'District's Approved Budget' -> budget_revised (Council changes); FY2027 Council-level changes taken from the activity-level Council chart instead of JA0-5 to avoid double counting
- coverage (stage[+funds] by FY x agency JA0/FO0/RM0/DB0/HY0/CF0/HG0):
| FY2021 | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds |
| FY2022 | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds |
| FY2023 | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds |
| FY2024 | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds |
| FY2025 | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds,prop | actu+funds,appr+funds | actu+funds,appr+funds |
| FY2026 | appr+funds,prop | appr+funds,prop | appr+funds | appr+funds | appr+funds,prop | appr+funds | appr+funds |
| FY2027 | appr+funds | appr+funds | appr+funds,prop | appr+funds | appr+funds,prop | appr+funds | appr+funds |
- warnings (0):

### 2026-10-10 18:01 — 38_parse_hud_counts
- wrote interim/stage_homeless_counts__hud.csv: 49,393 rows ({'bulk_hud_ahar_pit_hic': 48224, 'doc_hud_hic_dc500': 428, 'doc_mwcog_pit': 741}); PIT 39,029, HIC by CoC 9,195, PopSub 428, MWCOG 741
- wrote interim/stage_hic_projects__hud.csv: 1,257 rows (2022: 332, 2023: 292, 2024: 323, 2025: 310)
- HIC project PDFs: provider and facility names are truncated in the PDF itself (fixed-width report cells; same text in pdfplumber chars, pypdf and pdftotext); kept as printed. 'units' = family units (HIC reports units only for households with children). target_population is derived from the bed columns (household type, plus youth/veterans/chronic when all beds are dedicated) and set to single_women / women_with_children only when the provider or project name says women (basis in x_target_population_basis). x_women_focused_org = core peer tier 1a or Calvary; x_dv_focused_org = tier 1b (config/core_peers.csv).
- PIT by CoC (raw/hud/20261010T123731_huduser_2007-2025-PIT-Counts-by-CoC.xlsb): sheets 2007-2025; 39,029 rows for 8 CoCs; unparsed column names 216 (e.g. ['Overall Homeless - Under 18', 'Overall Homeless - Age 18 to 24', 'Overall Homeless - Over 24']); CoC-years absent: none
- partial unsheltered counts (Count Types): MD-601 2021; VA-602 2021
- workbook has no gender columns in any year (only age, race/ethnicity, household and subpopulation splits); DC gender comes from PopSub 2024 and the MWCOG 2025 DC narrative
- HIC by CoC (raw/hud/20261010T123733_huduser_2007-2025-HIC-Counts-by-CoC.xlsx): sheets 2007-2025; 9,195 rows; unparsed columns 9 (['HMIS Participation Rate (ES,TH) (non-numeric)', 'ES HMIS Participation Rate (non-numeric)', 'Total TH Beds for Households with only Children (non-numeric)', 'HMIS Participation Rate for Year-Round Beds (SH) (non-numeric)']); same-measure columns with different values kept as '__alt': 0
- PopSub DC-500 2024 (raw/hud/20261010T123749_hudx_CoC_PopSub_DC-500_2024.pdf): 232 rows; total persons 5616; women 2167
- PopSub DC-500 2025 (raw/hud/20261010T123750_hudx_CoC_PopSub_DC-500_2025.pdf): 196 rows; total persons 5138; women n/a
- MWCOG 2023 report (raw/hud/20261010T123754_mwcog_homelessness_metro_washington_2023_PIT.pdf): 548 table cells kept
- MWCOG 2024 report (raw/hud/20261010T123753_mwcog_homelessness_metro_washington_2024_PIT.pdf): 504 table cells kept
- MWCOG 2025 report (raw/hud/20261010T123752_mwcog_homelessness_metro_washington_2025_PIT.pdf): 520 table cells kept
- MWCOG 2026 report (raw/hud/20261010T123751_mwcog_homelessness_metro_washington_2026_PIT.pdf): 531 table cells kept
- MWCOG: 2103 cells parsed across reports -> 741 after keeping the latest report per jurisdiction/year/measure/population; values revised between reports: 38 (e.g. Prince William County, VA 2022 all: 241 (rpt 2023) -> 282 (rpt 2024); Prince William County, VA 2021 all: 282 (rpt 2023) -> 326 (rpt 2024); Prince William County, VA 2020 all: 326 (rpt 2023) -> 277 (rpt 2024); COG region 2023 households_without_children: 5901 (rpt 2023) -> 5755 (rpt 2024)); same report, two tables disagree (earlier page kept): 17 (District of Columbia 2020 households_with_only_children rpt 2023: p68 12 vs p25 11; Frederick City & County, MD 2021 households_with_only_children rpt 2023: p68 5 vs p25 0; COG region 2020 households_with_only_children rpt 2023: p69 13 vs p25 12; City of Alexandria, VA 2020 all rpt 2023: p68 198 vs p17 207)
- skipped tables (did not parse reliably): none; source-inconsistent columns are kept with confidence medium and an x_note
- not parsed: figures/charts (demographic profiles, income, gender charts), Table 3 population shares, Table 13/14 shelter status, TAY tables, Table 16 bed inventory, Table 17 formerly homeless in PH, Appendix B narrative percentages except the 2025 DC gender-of-adults table
- HIC provider names (cleaned, distinct): 105; matched 42 (40%); methods {'unmatched': 63, 'fuzzy_token_set': 10, 'exact_norm_name': 29, 'manual_known_ein': 2, 'manual_alias': 1}; government providers (no EIN expected) 7; beds at matched providers 67,567 of 133,181 (51%)
- fuzzy matches: Access Housing -> 521918702 (100.0); Access Housing INC (AHI) (Agency) -> 521918702 (100.0); Catholic Charities -> 530196524 (100.0); Catholic Charities (Agency) -> 530196524 (100.0); Covenant House Washington -> 133537709 (100.0); Covenant House Washington (CHW)(Age -> 133537709 (100.0); East River Family Strengthening Collabor -> 522277915 (100.0); Edgewood-Brookland Family Support Col -> 522246995 (100.0); Edgewood/Brookland Family Support Col -> 522246995 (100.0); Far Southeast Family Strengthening Colla -> 522117070 (100.0); Georgia Avenue Family Support Collabor -> 522349433 (100.0); Survivors & Advocates for Empowerment -> 412226446 (100.0)
- unmatched nonprofit providers (not in dc_sector/dmv_sector/core_peers by name): 801 East Collaborative; Bradley & Associates; CCDC; CORE DC; Casa Ruby; Church of Epiphany; Church of the Epiphany; Collaborative Solutions for Communities; Communities Helping & Empowering Pat; Communities Helping and Empowering P; Community Solutions; Cornerstone Community; Dawn Deaf; Deaf Dawn; East of the River Family Support Collabor; Echelon Community Services; Far Southeast Family Support Collaborati; Healthy Babies; Healthy Babies Project; Hillcrest Children & Family Center; Hope and a Home; Institute for Emotional Regulation; Jaydot; Joseph's House; Jubilee Housing; KBEC Group, Inc; KBEC Group, Inc.; KC Community Services; Latin American Youth Center; MBI Health Services; Maximus; Metropolitan Education Solutions; Metropolitan Educational Solutions; North Capitol Collaborative Inc.; North Capitol Family Support Collaborati; Operation Renewed Hope; Positive Kinship Bonding; SLS; SMYAL; Salvation Army; Sasha Bruce Youthwork; Sasha Bruce Youthworks; So Others Might Eat; Spring Leaf; St. Aloysius Roman Catholic Church; St. John's Community Community Servic; St. John's Community Services; Supporting & Mentoring Youth Advocate; Temple Micah; Temple Sinai; The Community Builders and Emory Bea; The Institute for Emotional Regulation, L; The Salvation Army; U.S. Vets; US Veterans Initiative; Wheeler Creek
- matcher (shared with script 36): manual aliases (TCP 521681401; DASH, DC SAFE, Housing Up), norm_name exact, then rapidfuzz token_set_ratio >= 92 (after expanding a truncated last token for raw names >= 30 chars) accepted only when fuzzy_ok() holds: both names >= 2 tokens, a shared non-generic token, no one-sided entity-marker token (foundation, fund, maryland, county, ...), and token containment (ratio >= 0.5) or prefix or only soft one-sided words or fuzz.ratio >= 90; reviewed reject list
- PopSub 2024 gender rows sum 5616 vs total 5616: pass
- MWCOG 2023 p16 'People Experiencing Literal Homelessness by Jurisdiction, 2022 - 2023': pass (2 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p17 'People Experiencing Literal Homelessness by Jurisdiction, 2019-2023': pass (5 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p22 '2023 Persons In Families Experiencing Homelessness by Jurisdiction': pass (4 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p23 'Change In Persons In Families Experiencing Homelessness by Jurisdictio': pass (5 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p25 'Households With Only Children Under Age 18 By Jurisdiction, 2020 - 202': pass (4 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p41 'Comparison of Unsheltered Single Adults By Jurisdiction, 2019 – 2023': pass (5 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p45 'Single Adults Experiencing Chronic Homelessness by Jurisdiction, 2019 ': pass (5 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p51 'Veterans Experiencing Homelessness By Jurisdiction, 2019 - 2023': pass (5 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 pp[68, 69] 'People Experiencing Literal Homelessness by Jurisdiction, 20': kept with flags: 14/20 columns do not add up in the source (2022 households_without_children 5,307 vs 5,273; 2022 households_with_adults_and_children 2,329 vs 2,322; 2022 all 7,646 vs 7,605); 2 jurisdiction-years whose household columns do not add up
- MWCOG 2024 p16 'People Experiencing Literal Homelessness by Jurisdiction, 2023 - 2024': pass (2 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p17 'People Experiencing Literal Homelessness by Jurisdiction, 2020-2024*': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p22 '2024 Persons in Families Experiencing Homelessness by Jurisdiction': pass (4 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p23 'Change in Persons in Families Experiencing Homelessness by Jurisdictio': kept with flags: 1/5 columns do not add up in the source (2020 persons_in_families 3,690 vs 3,760)
- MWCOG 2024 p29 'Households With Only Children Under Age 18 By Jurisdiction, 2020 - 202': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p49 'Unsheltered Single Adults Experiencing Homelessness by Jurisdiction, 2': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p52 'Single Adults Experiencing Chronic Homelessness by Jurisdiction, 2020 ': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p60 'Veterans Experiencing Homelessness by Jurisdiction, 2020 - 2024': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 pp[75, 76] 'People Experiencing Literal Homelessness by Jurisdiction, 20': kept with flags: 9/20 columns do not add up in the source (2022 households_without_children 5,154 vs 5,120; 2022 households_with_adults_and_children 2,272 vs 2,265; 2022 all 7,422 vs 7,395); 2 jurisdiction-years whose household columns do not add up
- MWCOG 2025 p17 'People Experiencing Literal Homelessness by Jurisdiction, 2024 - 2025': pass (2 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p18 'People Experiencing Literal Homelessness by Jurisdiction, 2021-2025*': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p22 '2025 Persons in Families Experiencing Homelessness by Jurisdiction': pass (4 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p23 'Change in Persons in Families Experiencing Homelessness by Jurisdictio': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p29 'Households With Only Children Under Age 18 By Jurisdiction, 2021 - 202': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p48 'Comparison of Unsheltered Single Adults by Jurisdiction, 2021 - 2025': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p51 'Single Adults Experiencing Chronic Homelessness by Jurisdiction, 2021 ': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p59 'Veterans Experiencing Homelessness by Jurisdiction, 2021 - 2025': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 pp[73, 74] 'People Experiencing Literal Homelessness by Jurisdiction, 20': pass (20 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p18 'People Experiencing Literal Homelessness by Jurisdiction, 2025-2026': pass (2 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p19 'People Experiencing Literal Homelessness by Jurisdiction, 2019-2026': pass (8 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p24 '2026 Persons in Families Experiencing Homelessness by Jurisdiction': pass (4 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p25 'Change in Persons in Families Experiencing Homelessness by Jurisdictio': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p32 'Households With Only Children Under Age 18 By Jurisdiction, 2022 – 202': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p50 'Comparison of Unsheltered Single Adults by Jurisdiction, 2022 – 2026': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p54 'Single Adults Experiencing Chronic Homelessness by Jurisdiction, 2022 ': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p59 'Veterans Experiencing Homelessness by Jurisdiction, 2022 – 2026': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 pp[79, 80] 'People Experiencing Literal Homelessness by Jurisdiction, 20': pass (20 year/measure columns, 8 jurisdictions + total)
- MWCOG total persons vs HUD PIT overall, CoC-years that differ: 9: MD-600 2020: MWCOG 453 vs HUD 466; MD-600 2021: MWCOG 537 vs HUD 535; MD-600 2022: MWCOG 571 vs HUD 533; MD-600 2023: MWCOG 659 vs HUD 595; MD-600 2024: MWCOG 658 vs HUD 650; MD-600 2025: MWCOG 608 vs HUD 588; VA-602 2019: MWCOG 169 vs HUD 167; VA-604 2019: MWCOG 277 vs HUD 280; VA-604 2025: MWCOG 392 vs HUD 393
- DC-500 MWCOG vs HUD by year: 2019 6,521/6521, 2020 6,380/6380, 2021 5,111/5111, 2022 4,410/4410, 2023 4,922/4922, 2024 5,616/5616, 2025 5,138/5138, 2026 5,363/n/a
- stage_homeless_counts duplicate keys (coc, jurisdiction, year, measure, population, source): 0
- DC-500 2025 recon values: pit_overall 5138 (exp 5138) pass; pit_sheltered_es 3275 (exp 3275) pass; pit_sheltered_th 1065 (exp 1065) pass; pit_unsheltered 798 (exp 798) pass; hic_beds_year_round__es_th_sh 4965 (exp 4965) pass; hic_beds_year_round__th 1385 (exp 1385) pass; hic_beds_year_round__psh 12696 (exp 12696) pass; hic_beds_year_round__rrh 6012 (exp 6012) pass
- HIC projects 2022 ES: 43 projects; total beds 5,159 vs Total row 5159; year-round 4,795 vs summary p1 4795 vs CoC workbook 4795: pass
- HIC projects 2022 SH: 1 projects; total beds 20 vs Total row 20; year-round 20 vs summary p1 20 vs CoC workbook 20: pass
- HIC projects 2022 TH: 71 projects; total beds 1,783 vs Total row 1783; year-round 1,783 vs summary p1 1783 vs CoC workbook 1783: pass
- HIC projects 2022 PSH: 148 projects; total beds 14,467 vs Total row 14467; year-round 14,467 vs summary p1 14467 vs CoC workbook 14467: pass
- HIC projects 2022 RRH: 34 projects; total beds 7,193 vs Total row 7193; year-round 7,193 vs summary p1 7193 vs CoC workbook 7193: pass
- HIC projects 2022 OPH: 35 projects; total beds 6,498 vs Total row 6498; year-round 6,498 vs summary p1 6498 vs CoC workbook 6498: pass
- HIC projects 2023 ES: 38 projects; total beds 4,026 vs Total row 4026; year-round 3,720 vs summary p1 3720 vs CoC workbook 3720: pass
- HIC projects 2023 SH: 1 projects; total beds 20 vs Total row 20; year-round 20 vs summary p1 20 vs CoC workbook 20: pass
- HIC projects 2023 TH: 65 projects; total beds 1,476 vs Total row 1476; year-round 1,476 vs summary p1 1476 vs CoC workbook 1476: pass
- HIC projects 2023 PSH: 138 projects; total beds 15,349 vs Total row 15349; year-round 15,349 vs summary p1 15349 vs CoC workbook 15349: pass
- HIC projects 2023 RRH: 35 projects; total beds 9,206 vs Total row 9206; year-round 9,206 vs summary p1 9206 vs CoC workbook 9206: pass
- HIC projects 2023 OPH: 15 projects; total beds 5,381 vs Total row 5381; year-round 5,381 vs summary p1 5381 vs CoC workbook 5381: pass
- HIC projects 2024 ES: 46 projects; total beds 4,000 vs Total row 4000; year-round 3,505 vs summary p1 3505 vs CoC workbook 3505: pass
- HIC projects 2024 SH: 1 projects; total beds 20 vs Total row 20; year-round 20 vs summary p1 20 vs CoC workbook 20: pass
- HIC projects 2024 TH: 70 projects; total beds 1,693 vs Total row 1693; year-round 1,693 vs summary p1 1693 vs CoC workbook 1693: pass
- HIC projects 2024 PSH: 154 projects; total beds 11,856 vs Total row 11856; year-round 11,856 vs summary p1 11856 vs CoC workbook 11856: pass
- HIC projects 2024 RRH: 33 projects; total beds 10,156 vs Total row 10156; year-round 10,156 vs summary p1 10156 vs CoC workbook 10156: pass
- HIC projects 2024 OPH: 19 projects; total beds 5,842 vs Total row 5842; year-round 5,842 vs summary p1 5842 vs CoC workbook 5842: pass
- HIC projects 2025 ES: 45 projects; total beds 3,954 vs Total row 3954; year-round 3,580 vs summary p1 3580 vs CoC workbook 3580: pass
- HIC projects 2025 TH: 64 projects; total beds 1,385 vs Total row 1385; year-round 1,385 vs summary p1 1385 vs CoC workbook 1385: pass
- HIC projects 2025 PSH: 159 projects; total beds 12,696 vs Total row 12696; year-round 12,696 vs summary p1 12696 vs CoC workbook 12696: pass
- HIC projects 2025 RRH: 26 projects; total beds 6,012 vs Total row 6012; year-round 6,012 vs summary p1 6012 vs CoC workbook 6012: pass
- HIC projects 2025 OPH: 16 projects; total beds 4,989 vs Total row 4989; year-round 4,989 vs summary p1 4989 vs CoC workbook 4989: pass
- stage_hic_projects duplicate keys (year, type, page, seq): 0
- Calvary HIC 2025 rows pass (7 projects, 124 beds); 2024 Sisters Rise PSH [24] (exp [24])

### 2026-10-10 18:02 — 33_pull_usaspending: stage fact_gov_awards
- interim/stage_fact_gov_awards__federal.csv: 28207 rows; {"named_job_rows_dropped": 1, "usaspending_sub_reports": 11875, "usaspending_prime": 7163, "usaspending_sub": 10733, "fac_reports_kept": 1841, "fac_reports_used": 1831, "fac_lines": 9851, "fac_reports_identical_sefa": 18, "slfrf_dc_report_rows": 462, "slfrf_dc_rows": 461, "named_comparators": {"311597223": {"rows": 51, "by_source_flow": {"usaspending/prime": 2, "usaspending/subaward": 17, "fac_sefa/pass_through_expenditure": 30, "fac_sefa/prime": 2}, "fac_audit_years": ["2020", "2021", "2022", "2023", "2024", "2025"], "fac_expenditure_by_fy": {"2020": 1043889, "2021": 2781894, "2022": 6904511, "2023": 3279830, "2024": 4249604, "2025": 3358800}, "usaspending_amount": 8294415}, "882046704": {"rows": 0, "by_source_flow": {}, "fac_audit_years": [], "fac_expenditure_by_fy": {}, "usaspending_amount": 0}}, "rows": 28207, "duplicate_ids": 0, "rows_missing_provenance": 0, "by_source_flow": {"usaspending/prime": 7162, "usaspending/subaward": 10733, "fac_sefa/prime": 4492, "fac_sefa/pass_through_expenditure": 5359, "treasury_slfrf/subaward": 461}, "ein_filled": 23149}
- Calvary reconciliation: {"fac_fy22_total": 4067718, "fac_fy22_ok": true, "fac_ay2023_total": 4064718, "fac_ay2023_conflict_rows": 4, "hud_14251": [200000], "hud_ok": true, "ppp": [327200], "usaspending_subawards": [["14.252", 25000]], "slfrf": [113488, 3680675], "slfrf_ok": true, "calvary_rows": 13}
- EIN coverage (scope = calvary, core_peers, dc_sector, dmv_sector): {"scope_orgs": 4920, "orgs_with_any_row_by_ein": 234, "by_source": {"usaspending": 185, "fac_sefa": 234, "treasury_slfrf": 2}, "extra_orgs_by_exact_name_state_candidate_only": 60}

### 2026-10-10 18:02 — 35_pull_grantsgov: opportunities
- universe posted+forecasted 1467; candidates 531 (local cfdaList 3, cfda key 3, keyword search 530, title regex 51); fetched 0 (reused 531 saved responses); fetch failures 0; dropped by local filter 245
- interim/stage_fact_opportunities__grantsgov.csv: 286 rows (173 posted, 113 forecasted); duplicate ids 0
- keyword_hits counts: {"homelessness": 6, "housing": 17, "domestic violence": 5, "victim services": 2, "women": 59, "substance use": 47, "workforce": 98, "reentry": 5, "veterans": 19, "aging": 77}
- target-ALN rows: 3; nonprofit-eligible (12/13/25/99): 263
- manifest raw/grantsgov/20261010T180228_pull35_manifest.json

### 2026-10-10 18:03 — 41_pull_soi_extracts: stage
- universe EINs: 15,812
- 990 2012 (12eofinextract990.zip): 294,019 rows read, 2,255 universe rows; fields absent this year: grants_paid, compensation_total, cash_savings_eoy
- 990 2013 (13eofinextract990.zip): 289,603 rows read, 2,255 universe rows
- 990 2014 (14eofinextract990.zip): 299,405 rows read, 2,334 universe rows
- 990 2015 (15eofinextract990.zip): 294,782 rows read, 2,252 universe rows
- 990 2016 (16eofinextract990.zip): 307,483 rows read, 2,421 universe rows
- 990 2017 (17eofinextract990.zip): 300,910 rows read, 2,426 universe rows
- 990 2018 (18eoextract990.zip): 313,339 rows read, 2,514 universe rows
- 990 2019 (19eoextract990.zip): 304,441 rows read, 2,520 universe rows
- 990 2020 (20eoextract990.zip): 273,971 rows read, 2,294 universe rows
- 990 2021 (21eoextract990.zip): 342,920 rows read, 2,874 universe rows
- 990 2022 (22eoextract990.zip): 326,123 rows read, 2,802 universe rows
- 990 2023 (23eoextract990.zip): 338,048 rows read, 2,831 universe rows
- 990 2024 (24eoextract990.zip): 345,365 rows read, 2,985 universe rows
- 990EZ 2012 (12eofinextract990ez.zip): 223,348 rows read, 593 universe rows
- 990EZ 2013 (13eofinextract990ez.zip): 218,981 rows read, 613 universe rows
- 990EZ 2014 (14eofinextract990ez.zip): 234,820 rows read, 659 universe rows
- 990EZ 2015 (15eofinextractEZ.zip): 223,028 rows read, 669 universe rows
- 990EZ 2016 (16eofinextractez.zip): 230,745 rows read, 738 universe rows
- 990EZ 2017 (17eofinextractEZ.zip): 218,097 rows read, 731 universe rows
- 990EZ 2018 (18eoextractez.zip): 226,533 rows read, 766 universe rows
- 990EZ 2019 (19eoextractez.zip): 218,671 rows read, 777 universe rows
- 990EZ 2020 (20eoextractez.zip): 154,314 rows read, 536 universe rows
- 990EZ 2021 (21eoextractez.zip): 218,733 rows read, 867 universe rows
- 990EZ 2022 (22eoextractez.zip): 231,289 rows read, 990 universe rows
- 990EZ 2023 (23eoextractez.zip): 207,536 rows read, 933 universe rows
- 990EZ 2024 (24eoextract990EZ.zip): 203,699 rows read, 986 universe rows
- 990PF 2012 (12eofinextract990pf.zip): 98,948 rows read, 2,671 universe rows; fields absent this year: x_pf_grants_approved_future
- 990PF 2013 (13eofinextract990pf.zip): 100,484 rows read, 2,755 universe rows
- 990PF 2014 (14eofinextract990pf.zip): 101,381 rows read, 2,904 universe rows
- 990PF 2015 (15eofinextract990pf.zip): 103,000 rows read, 2,935 universe rows
- 990PF 2016 (16eofinextract990pf.zip): 105,239 rows read, 3,131 universe rows
- 990PF 2020 (20eoextract990pf.zip): 91,473 rows read, 3,022 universe rows
- 990PF 2021 (21eoextract990pf.zip): 125,312 rows read, 4,417 universe rows
- 990PF 2022 (22eoextract990pf.zip): 115,024 rows read, 4,268 universe rows
- 990PF 2023 (23eoextract990pf.zip): 120,350 rows read, 4,589 universe rows
- 990PF 2024 (24eoextract990pf.zip): 119,059 rows read, 4,796 universe rows
- SOI: 78,109 rows, 9,446 EINs; 0 older-processing-year copies dropped; 0 rows whose copies disagree on total_revenue
- NCCS 2009: 48,857 rows read, 280 universe 990 rows
- NCCS 2010: 184,553 rows read, 932 universe 990 rows
- NCCS 2011: 241,595 rows read, 1,272 universe 990 rows
- NCCS 2012: 273,429 rows read, 1,485 universe 990 rows
- NCCS 2013: 303,225 rows read, 1,645 universe 990 rows
- NCCS 2014: 335,066 rows read, 1,783 universe 990 rows
- NCCS 2015: 358,459 rows read, 1,962 universe 990 rows
- NCCS 2016: 374,252 rows read, 2,045 universe 990 rows
- NCCS 2017: 391,170 rows read, 2,163 universe 990 rows
- NCCS 2018: 406,376 rows read, 2,255 universe 990 rows
- NCCS 2019: 436,217 rows read, 2,393 universe 990 rows
- NCCS 2020: 485,459 rows read, 2,675 universe 990 rows
- NCCS 2021: 491,127 rows read, 2,558 universe 990 rows
- NCCS 2022: 131,588 rows read, 350 universe 990 rows
- NCCS: 22,573 rows staged, 3,105 EINs, tax years 2010-2022; period from SOI match 22,555, from IRS index 18; dropped 901 with no period; 309 EIN-years had >1 return (kept the latest OBJECT_ID)
- NCCS total_revenue equals SOI total_revenue on 99.1% of 22,555 matched rows
- wrote 100,682 rows to interim/stage_fact_org_financials__soi.csv (SOI 78,109; NCCS 22,573)
- duplicate (ein, tax_period_end, return_type, source_id): 0
- Calvary total_revenue QC: bulk_irs_soi_extract TY2020 3,851,984 OK; bulk_irs_soi_extract TY2021 8,867,250 OK; bulk_nccs_efile TY2020 3,851,984 OK; bulk_nccs_efile TY2021 not present
- 990-PF SOI TAX_YR equals derived tax_year on 100.0% of rows
- rows by fiscal_year (period-end year) x return_type / source:
```
source_id   irs_soi_extract              nccs_efile     All
return_type             990 990EZ  990PF        990        
fiscal_year                                                
2002                      0     0      1          0       1
2003                      1     0      1          0       2
2004                      0     0      1          0       1
2005                      1     0      1          0       2
2006                      0     0      1          0       1
2007                      0     2      3          0       5
2008                      2    12      7          0      21
2009                      4    30     14          0      48
2010                    179    93     84          5     361
2011                   1876   519   2408        826    5629
2012                   2227   624   2756       1381    6988
2013                   2279   626   2831       1558    7294
2014                   2299   670   2974       1662    7605
2015                   2365   708   3040       1856    7969
2016                   2445   739    310       1979    5473
2017                   2494   750     23       2078    5345
2018                   2566   763    110       2181    5620
2019                   2625   802   3462       2303    9192
2020                   2649   848   3905       2539    9941
2021                   2761   833   4206       2685   10485
2022                   2852   872   4435       1513    9672
2023                   2862   882   4560          7    8311
2024                    276    85    355          0     716
All                   32763  9858  35488      22573  100682
```
- coverage, bulk_irs_soi_extract (EINs with >=1 row / universe EINs; org-years; median years per covered org):
  - calvary: 1/1; 13; 13
  - calvary_known_funders: 84/88; 881; 10
  - core_peers: 18/18; 235; 13
  - daf_sponsors: 15/15; 184; 13
  - dc_sector: 524/1,027; 4,620; 11
  - dmv_funders: 5,744/7,705; 44,487; 10
  - dmv_sector: 1,942/4,910; 15,530; 9
  - named_comparators: 2/2; 14; 7
  - national_women: 1,395/2,878; 13,420; 12
  - size_matched: 564/566; 6,892; 13
- coverage, bulk_nccs_efile (EINs with >=1 row / universe EINs; org-years; median years per covered org):
  - calvary: 1/1; 7; 7
  - calvary_known_funders: 33/88; 267; 9
  - core_peers: 18/18; 172; 10
  - daf_sponsors: 15/15; 84; 6
  - dc_sector: 370/1,027; 2,550; 7
  - dmv_funders: 650/7,705; 4,046; 6
  - dmv_sector: 1,140/4,910; 7,857; 7
  - named_comparators: 1/2; 11; 11
  - national_women: 959/2,878; 7,769; 9
  - size_matched: 558/566; 4,840; 10

### 2026-10-10 18:03 — 42_pull_propublica: stage
- 2,538 org JSONs read (0 target EINs with no ProPublica record); 18,279 filings_with_data rows; skipped formtypes {}; 0 bad periods
- tax_prd_yr equals derived fiscal_year (period-end year) on 100.0% of rows
- staged 18,279 rows, 2,004 EINs -> interim/stage_fact_org_financials__propublica.csv; duplicates on (ein, tax_period_end, return_type, source_id): 0
- Calvary total_revenue QC: TY2020 3,851,984 OK; TY2021 8,867,250 OK
- cross-check vs SOI: 18,279 matching (ein, period, form) rows; equal total_revenue 100.0%, total_expenses 100.0%, total_assets_eoy 100.0%
- ProPublica rows with no SOI row: 0 (by fiscal_year {})
- rows by fiscal_year x return_type:
```
return_type   990  990EZ  990PF    All
fiscal_year                           
2007            0      1      1      2
2008            0      1      1      2
2009            0      3      4      7
2010           53     20     20     93
2011          392     61    812   1265
2012          440     70    936   1446
2013          448     65    960   1473
2014          448     66    999   1513
2015          465     72   1017   1554
2016          476     66    107    649
2017          484     69      4    557
2018          493     71     15    579
2019          513     73   1082   1668
2020          511     75   1182   1768
2021          536     74   1229   1839
2022          550     69   1245   1864
2023          550     76   1243   1869
2024           28      4     99    131
All          6387    936  10956  18279
```

### 2026-10-10 18:03 — 46_web_named_comparators (stage)
- staged 396 rows -> interim/stage_fact_grants__web_named.csv (exact duplicates dropped 1); recipients {'311597223': 391, '882046704': 5}
- by source_type {'annual_report': 350, 'support_page': 33, 'web': 13}; amount_kind {'unknown': 353, 'mixed': 33, 'cash': 8, 'noncash': 2}; with amount 8, with band 354
- by fiscal_year {2023: 204, 2024: 2, 2025: 155, 2026: 35}
- non-organization entries counted per band only: 570 -> interim/web_named_donor_band_counts.csv; joint credits with a personal name: 6 trimmed to the organization, 1 dropped
- per page (entries, kept, dropped as non-org, status): nc_dwc_ar_2024 669/203/422/ok; nc_dwc_ar_web 277/148/112/ok; nc_dwc_gala_2025 26/4/18/ok; nc_dwc_gala_2026 54/29/18/ok; nc_dwc_rosas_place_pr 1/1/0/ok; nc_dwc_hilton_2026 1/1/0/ok; nc_dwc_ahmanson_grants 2/2/0/ok; nc_dwc_bscf_grantee 1/1/0/ok; nc_dwc_foxwynd 1/1/0/ok; nc_dwc_anthem_2023 1/1/0/ok; nc_dwc_anthem_2026_dwc_pr 1/1/0/ok; nc_cbw_sheworks 1/1/0/ok; nc_cbw_launch_pr 1/1/0/ok; nc_cbw_lacare_pr 2/2/0/ok; nc_cbw_econ_mobility 1/1/0/ok
- this run: Tavily search 0, extract 0, HTTP GET 0, cache hits 0; cumulative (manifest): search 139/300, extract 15/200, HTTP 150; script-46 totals: search 30/30, extract 5/15

### 2026-10-10 18:03 — 45_stage_web_grants
- staged rows 1015: by source_type {'support_page': 249, 'annual_report': 630, 'web': 136}; confidence {'medium': 988, 'high': 27}
- amount stated 34; band only 392; unknown 589
- recipient Calvary 268; core peers 739 (14 peers); whole-list keyword keeps 8
- Calvary-site rows by type {'support_page': 98, 'annual_report': 74, 'anonymous_skipped': 1, 'web': 90}
- pages parsed 20/65; not parsed or failed: nsv_funding_reports (index page (links to annual reports)); openarms_about (no funder list on the site); nebw_reports (index page (links to annual reports)); nebw_ar_2025 (2025 annual report text has no funder list); msp_ar_fy22 (no funder list); dcsafe_ar_fy25 (no funder list (revenue split only)); nuvaya_fin_reports (HTTP 403 and Tavily extract empty); christhouse_ar_2025 (landing page; PDF has no text layer); christhouse_ar_2025_pdf (image-only PDF (12 chars of text)); ehdc_ar_2024 (landing page); ehdc_ar_2024_pdf (2024 annual report text has no funder list); cfh_ar_list (index page); thrive_impact_2024 (lists corporate volunteer groups, not funders); miriams_financials (index page); miriams_ar_fy25 (mkannualreport.org is JavaScript-rendered; no text retrieved); coh_ar_2025 (2025 annual report summary has no funder list); coh_impact_2024 (same list as coh_funders (parsed there)); chgw_home (home page); chgw_impact_fy24 (FY24 impact report text has no funder list); doorways_ar_2023 (landing page); doorways_ar_2023_issuu (issuu viewer; no document text); hormd_honor_roll (URL now serves the About Us page; no honor roll content); hormd_honor_roll_tav (Tavily advanced extract also returns no honor roll content); hormd_ar_2024 (PDF returns HTTP 404); hormd_ar_page (annual report page has no donor list); meyer_118m_28 (2020 list (outside 2024-2026); no Calvary or peers); meyer_635k_8 (2022 list (outside 2024-2026); no Calvary or peers); meyer_rapid (program description only; no 
- in-kind evidence rows 17: MGAC=unclear; MGAC=in_kind; MGAC=in_kind; MGAC=cash; Health Equity Fund=cash; Health Equity Fund=cash; Health Equity Fund=cash; Health Equity Fund=cash; Capital One=unclear; Capital One=unclear; Capital One=cash; World Bank Community Connections Fund=cash; World Bank Community Connections Fund=cash; World Bank Community Connections Fund=cash; Frontier Co-op / Aura Cacia (Frontier Co-op Giving Fund)=in_kind; Frontier Co-op / Aura Cacia (Frontier Co-op Giving Fund)=unclear; MGAC; Capital One; World Bank Community Connections Fund=unclear
- Tavily usage to date (manifest, scripts 43-44): search 139/300, extract 15/200; plus 1 exploratory search during development (same query as cal_audit_fy24; response not saved). HTTP GETs 150.
- appended notes_for_analysis.md 'Web funder data' and open_questions.md

### 2026-10-10 18:04 — 50_parse_xml: progress
- 2,000/31,483 parsed in 0.5 min; grants 698,214, roles 22,703, relationships 5,719; errors 0

### 2026-10-10 18:04 — 50_parse_xml: progress
- 4,000/31,483 parsed in 0.6 min; grants 764,178, roles 41,319, relationships 9,850; errors 0

### 2026-10-10 18:04 — 50_parse_xml: progress
- 6,000/31,483 parsed in 0.6 min; grants 804,949, roles 56,969, relationships 10,909; errors 0

### 2026-10-10 18:04 — 50_parse_xml: progress
- 8,000/31,483 parsed in 0.6 min; grants 833,478, roles 71,614, relationships 11,579; errors 0

### 2026-10-10 18:04 — 50_parse_xml: progress
- 10,000/31,483 parsed in 0.7 min; grants 855,931, roles 83,719, relationships 11,966; errors 0

### 2026-10-10 18:04 — 50_parse_xml: progress
- 12,000/31,483 parsed in 0.7 min; grants 872,756, roles 94,450, relationships 12,310; errors 0

### 2026-10-10 18:04 — 50_parse_xml: progress
- 14,000/31,483 parsed in 0.7 min; grants 885,821, roles 104,143, relationships 12,537; errors 0

### 2026-10-10 18:04 — 50_parse_xml: progress
- 16,000/31,483 parsed in 0.7 min; grants 896,903, roles 112,869, relationships 12,668; errors 0

### 2026-10-10 18:04 — 50_parse_xml: progress
- 18,000/31,483 parsed in 0.8 min; grants 906,213, roles 120,818, relationships 12,795; errors 0

### 2026-10-10 18:04 — 50_parse_xml: progress
- 20,000/31,483 parsed in 0.8 min; grants 913,747, roles 128,321, relationships 12,858; errors 0

### 2026-10-10 18:04 — 50_parse_xml: progress
- 22,000/31,483 parsed in 0.8 min; grants 919,346, roles 135,225, relationships 12,862; errors 0

### 2026-10-10 18:04 — 50_parse_xml: progress
- 24,000/31,483 parsed in 0.8 min; grants 923,248, roles 141,620, relationships 12,864; errors 0

### 2026-10-10 18:04 — 50_parse_xml: progress
- 26,000/31,483 parsed in 0.8 min; grants 925,353, roles 148,088, relationships 12,864; errors 0

### 2026-10-10 18:04 — 50_parse_xml: progress
- 28,000/31,483 parsed in 0.9 min; grants 926,494, roles 154,519, relationships 12,864; errors 0

### 2026-10-10 18:04 — 50_parse_xml: progress
- 30,000/31,483 parsed in 0.9 min; grants 926,838, roles 160,722, relationships 12,864; errors 0

### 2026-10-10 18:04 — 50_parse_xml: done
- parsed 31,483 of 31,483 returns in 0.9 min; errors 0 -> xml_parse_errors.csv
- interim/stage_fact_org_financials__xml.csv: 31,483 rows {'990PF': 24877, '990': 4872, '990EZ': 1734}; amended 335; EIN differs from index 0
- interim/stage_fact_grants__xml.csv: 926,887 rows
- interim/stage_fact_roles__xml.csv: 163,918 rows
- interim/stage_fact_org_relationships__xml.csv: 12,864 rows
- interim/org_profile__xml.csv: 31,483 rows (6,774 EINs; street kept on latest return only)
- interim/xml_schedule_i_part3.csv: 1,730 Schedule I Part III lines (aggregates, no names)
- schema versions: {'2014v5.0': 1, '2014v6.0': 1, '2015v2.1': 1, '2015v3.0': 1, '2016v3.0': 2, '2017v2.3': 2, '2018v3.1': 2, '2019v5.1': 1, '2019v5.2': 1, '2020v4.0': 1671, '2020v4.1': 2870, '2020v4.2': 423, '2021v4.0': 1467, '2021v4.1': 767, '2021v4.2': 3218, '2022v4.0': 4, '2022v4.1': 248, '2022v5.0': 5526, '2023v4.0': 271, '2023v5.0': 2462, '2023v5.1': 2421, '2023v6.0': 960, '2024v5.0': 1374, '2024v5.1': 1978, '2024v5.2': 2496, '2024v5.5': 372, '2025v4.0': 1220, '2025v4.1': 1441, '2025v4.2': 282}
- DAF1 sponsors, Schedule I kept only for DC/MD/VA recipients (all years in scope):
  - FIDELITY INVESTMENTS CHARITABLE GIFT FUND (110303001): national 372,180 rows / $58,823.5M; kept DMV 24,496 / $8,007.2M; filtered out $50,816.2M
  - DONOR ADVISED CHARITABLE GIVING INC (311640316): national 257,532 rows / $28,043.2M; kept DMV 17,453 / $4,001.7M; filtered out $24,041.5M
  - NATIONAL PHILANTHROPIC TRUST (237825575): national 83,803 rows / $26,775.7M; kept DMV 6,855 / $3,393.6M; filtered out $23,382.1M
  - VANGUARD CHARITABLE ENDOWMENT PROGRAM (232888152): national 113,808 rows / $12,077.0M; kept DMV 9,471 / $2,022.5M; filtered out $10,054.5M
  - AMERICAN ONLINE GIVING FOUNDATION INC (810739440): national 228,879 rows / $10,079.9M; kept DMV 15,079 / $1,159.3M; filtered out $8,920.6M
  - AMERICAN ENDOWMENT FOUNDATION (341747398): national 65,226 rows / $4,638.5M; kept DMV 5,501 / $441.8M; filtered out $4,196.7M
  - BANK OF AMERICA CHARITABLE GIFT FD (046010342): national 4 rows / $3,249.2M; kept DMV 0 / $0.0M; filtered out $3,249.2M
  - THE AYCO CHARITABLE FOUNDATION (141782466): national 21,612 rows / $2,375.6M; kept DMV 1,874 / $113.0M; filtered out $2,262.5M
  - Renaissance Charitable Foundation Inc (352129262): national 5 rows / $2,288.2M; kept DMV 0 / $0.0M; filtered out $2,288.2M
  - PAYPAL CHARITABLE GIVING FUND (450931286): national 47,570 rows / $1,897.4M; kept DMV 3,864 / $145.8M; filtered out $1,751.5M
  - CHARITIES AID FOUNDATION AMERICA (431634280): national 44,986 rows / $1,870.2M; kept DMV 3,095 / $204.6M; filtered out $1,665.5M
  - THE BLACKBAUD GIVING FUND (460942102): national 35,201 rows / $1,351.7M; kept DMV 2,007 / $135.2M; filtered out $1,216.5M
  - THE GOLDMAN SACHS CHARITABLE GIFT FUND (113813663): national 12,471 rows / $1,056.1M; kept DMV 1,077 / $131.3M; filtered out $924.9M
  - BNY MELLON CHARITABLE GIFT FUND C/O BNY MELLON NA (300748315): national 5,467 rows / $1,022.5M; kept DMV 466 / $17.6M; filtered out $1,004.9M
  - THE US CHARITABLE GIFT TRUST (311663020): national 12,033 rows / $883.9M; kept DMV 984 / $29.0M; filtered out $854.9M

### 2026-10-10 18:04 — 51_qc_xml
- fetch 100.00% of 31,483
- parse errors 0
- PF grants sum exact 99.96% of returns with grants (99.81% of all PF); named-grantee rows cover 93.8% of PF grant dollars
- Calvary revenue checks pass
- Cafritz EIN 526036989; TY2024 to Calvary $170,000
- Calvary grant rows 150 from 50 funders ($4,701,886)
- trace 20/20
- report -> interim/xml_qc.md

### 2026-10-10 18:04 — 60_stage_inputs
- stage_fact_org_financials__inputs.csv: 17 rows
- stage_fact_gov_awards__inputs.csv: 8 rows
- stage_fact_grants__inputs.csv: 360 rows
- stage_fact_roles__inputs.csv: 195 rows

### 2026-10-10 18:07 — 61_resolve_entities
- unique name keys 232,696; alias rows 231,717
- occurrences by method:
match_method  exact_ein  exact_name_city  exact_name_national  exact_name_state  fuzzy_name_city  known_funder  manual  manual_reject  unmatched
role                                                                                                                                            
funder           925013                0                  274                 0                0           227      59             23       3062
pass_through        686                0                 1936                 0                0             0      16              0      14243
recipient        212746           344250                  912             51870            27536             0      48              2     285961

### 2026-10-10 18:08 — 62_build_facts
- fact_org_financials: 150,461 rows
- fact_grants: 928,658 rows
- fact_gov_awards: 40,300 rows
- fact_opportunities: 286 rows
- fact_policy_events: 297 rows
- supp_calvary_individual_donor_bands.csv: copied from stage_supp_calvary_individual_donor_bands.csv
- supp_calvary_program_metrics.csv: copied from stage_supp_calvary_program_metrics.csv
- supp_calvary_strategic_targets.csv: copied from stage_supp_calvary_strategic_targets.csv
- supp_homeless_counts.csv: copied from stage_homeless_counts__hud.csv
- supp_hic_projects.csv: copied from stage_hic_projects__hud.csv
- supp_dc_budget_lines.csv: copied from stage_dc_budget_lines__dc.csv

### 2026-10-10 18:08 — 63_build_dims
- dim_org: 105,189 rows
- dim_funder: 8,928 rows
- dim_program_area: 13 rows
- dim_period: 28 rows
- dim_geo: 246 rows

### 2026-10-10 18:09 — 64_people_relationships
- fact_roles 163,473; dim_person 48,563 (multi-org 2,036); candidate_interlocks 1,270; fact_org_relationships 544,041 {'grant': 432430, 'daf_sponsor_grant': 90830, 'schedule_r_related': 12864, 'shared_board_member': 4162, 'pass_through_funding': 3755}

### 2026-10-10 18:09 — 63_build_dims
- dim_org: 105,189 rows
- dim_funder: 8,928 rows
- dim_program_area: 13 rows
- dim_period: 28 rows
- dim_geo: 246 rows

### 2026-10-10 18:11 — 70_quality_checks
- wrote reports/data_quality.md; duplicates []; portability issues []

### 2026-10-10 18:11 — 80_docs
- data_dictionary rows 542; undocumented columns 0; source_ids missing from registry: none

### 2026-10-10 18:15 — 01_inventory_inputs
- sources/input_inventory.csv: 30 rows (duplicate=1, ok=24, partial=4, unreadable=1)
- registered 30 input_* sources
- period checks: all match

### 2026-10-10 18:16 — 02_extract_inputs
- text dumps: 29 files in raw/inputs_extracted/text
- raw/inputs_extracted/audit_financials.csv: 1089 rows
- raw/inputs_extracted/audit_tieout_checks.csv: 260 rows
- raw/inputs_extracted/sefa_federal_awards.csv: 4 rows
- raw/inputs_extracted/form990_pdf_financials.csv: 362 rows
- raw/inputs_extracted/form990_pdf_people.csv: 113 rows
- raw/inputs_extracted/form990_pdf_schedule_i.csv: 2 rows
- raw/inputs_extracted/funder_mentions.csv: 200 rows
- raw/inputs_extracted/individual_donor_band_counts.csv: 4 rows
- raw/inputs_extracted/board_lists.csv: 82 rows
- raw/inputs_extracted/annual_report_metrics.csv: 178 rows
- raw/inputs_extracted/crm_funders_2023_2026.csv: 160 rows
- raw/inputs_extracted/strategic_plan_targets.csv: 18 rows
- tie-out checks: 260/260 tie
- SEFA: FY15-Audited-Financial-Statements.pdf: SEFA none
- SEFA: 2016-Audited-Financial-Statements.pdf: SEFA none
- SEFA: 2017-Audited-Financial-Statements-Calvary-Women_s-Services.pdf: SEFA none
- SEFA: CWS-FY18-Audit-.pdf: SEFA none
- SEFA: 2019-Audited-Financial-Statements-CWS.pdf: SEFA none
- SEFA: 2020-Audited-Financial-Statements-CWS.pdf: SEFA none
- SEFA: 2021-Audited-Financial-Statements-CWS.pdf: SEFA none
- SEFA: Calvary-Womens-Services-Inc.-9.30.23-FS.pdf: SEFA 4 programs sum 937,999 vs printed total 937,999
- CRM export: 160 orgs, GIFT_TOTAL $10,556,075.88, 877 gifts, last-gift dates 2023-10-16 to 2026-10-03; 21 rows have NUM_GIFTS=1 but GIFT_TOTAL != LAST_CONTRIB_AMT; GIFT_TOTAL window recorded as unconfirmed
- funder names verified in layout text: 171/171
- note: 2015-Form-990-Calvary-Women_s-Services.pdf: Part I not in text layer (page 1 scanned)
- note: 2016-Form-990-Calvary-Women_s-Services.pdf: Part I not in text layer (page 1 scanned)
- note: 2019-990-Form-990-CWS.pdf: Part I not in text layer (page 1 scanned)

### 2026-10-10 18:16 — 20_build_universes
- calvary: 1 EINs
- calvary_known_funders: 88 EINs
- core_peers: 18 EINs
- daf_sponsors: 15 EINs
- dc_sector: 1,027 EINs
- dmv_funders: 7,705 EINs
- dmv_sector: 4,910 EINs
- named_comparators: 2 EINs
- national_women: 2,878 EINs
- size_matched: 566 EINs
- membership rows 17,210; distinct EINs 15,812; e-file rows 45,305; size band $2,483,998–$9,935,990; missing pins {'F3': [], 'DAF1': []}

### 2026-10-10 18:17 — 22_match_known_funders
- names 243; outcomes {('corp_foundation', 'inferred'): 16, ('exact_name_state', 'yes'): 33, ('exact_name_unique', 'yes'): 19, ('fuzzy_name_state', 'yes'): 6, ('manual', 'inferred'): 5, ('manual', 'yes'): 12, ('manual_reject', 'no'): 10, ('unmatched', 'no'): 142}; accepted EINs 88

### 2026-10-10 18:18 — 20_build_universes
- calvary: 1 EINs
- calvary_known_funders: 88 EINs
- core_peers: 18 EINs
- daf_sponsors: 15 EINs
- dc_sector: 1,027 EINs
- dmv_funders: 7,705 EINs
- dmv_sector: 4,910 EINs
- named_comparators: 2 EINs
- national_women: 2,878 EINs
- size_matched: 566 EINs
- membership rows 17,210; distinct EINs 15,812; e-file rows 45,305; size band $2,483,998–$9,935,990; missing pins {'F3': [], 'DAF1': []}

### 2026-10-10 18:22 — 36_parse_dc_awards
- wrote interim/stage_fact_gov_awards__dc.csv: 12,085 rows; by source/section: dc_oversight/dv_grantees 53; dc_oversight/erap_arpa_grants 25; dc_oversight/homelessness_prevention 19; dc_oversight/psh_case_management 90; dc_oversight/singles_shelter_contract_periods 53; dc_oversight/singles_shelter_contracts 50; dc_oversight/singles_shelter_subgrants 6; dc_oversight/youth_dhs_direct_housing 65; dc_oversight/youth_dhs_direct_nonhousing 37; dc_oversight/youth_tcp_housing 44; dc_ovsjg/ovsjg_layer 1267; dc_ovsjg/ovsjg_pdf 118; dc_pass/pass_payments 5494; dc_pass/pass_po 4494; hud_coc/hud_coc 270
- decisions: OVSJG flow_type dc_local_grant unless the stated funding source is federal only (then subaward with OVSJG as pass-through); assistance_listing filled only from the stated funding source (VOCA 16.575, STOP VAWA 16.588, SASP 16.017, Byrne JAG 16.738, JJDP Title II 16.540, Title V 16.548, RSAT 16.593, Coverdell 16.742, ARPA -> SLFRF 21.027); DHS ERAP ARPA/ERA2 shares are subawards (21.027/21.023); HUD CoC rows: TCP-applicant projects -> recipient = sponsor in the project title, flow subaward, pass-through TCP; other applicants -> prime; fiscal_year = CoC competition year (federal_fy).
- OVSJG layer 35: 1267 rows FY2016-FY2025; AGENCY used as grantee, ORGANIZATIONNAME as project title (labels swapped); 6 rows flagged as identical repeats
- OVSJG FY2024 PDF p2: 'Metro DC Community Center Inc., The' amount from text layer: 327000
- OVSJG FY2024 PDF (raw/dc_gov/20261010T123646_ovsjg_funding_recipients_FY2024.pdf): 121 grant rows, total $62,935,024
- OVSJG FY2025 PDF (raw/dc_gov/20261010T123645_ovsjg_funding_recipients_FY2025.pdf): 120 grant rows, total $92,682,681
- OVSJG FY2026 PDF (raw/dc_gov/20261010T123645_ovsjg_funding_recipients_FY2026.pdf): 118 grant rows, total $96,653,604
- OVSJG merge: 241 FY2024/FY2025 layer rows enriched from the PDFs (funding source, period, issue date); 118 PDF rows added (118 FY2026); PDF rows without a layer match: 0 []; layer FY2024/25 rows without a PDF match: 0 []
- DHS oversight provider tables: 442 rows; by section {'erap_arpa_grants': 25, 'homelessness_prevention': 19, 'youth_dhs_direct_nonhousing': 37, 'youth_tcp_housing': 44, 'youth_dhs_direct_housing': 65, 'psh_case_management': 90, 'singles_shelter_contracts': 50, 'dv_grantees': 53, 'singles_shelter_contract_periods': 53, 'singles_shelter_subgrants': 6}; $0 cells skipped: 20
- HUD CoC DC-500: 270 project rows ({2019: 38, 2020: 39, 2021: 40, 2022: 43, 2023: 39, 2024: 36, 2025: 35}); flow {'prime': 66, 'subaward': 204}
- PASS: 18,655 distinct PO suppliers, 73,834 distinct payment suppliers; matched to universe/TCP EINs: 188 PO supplier strings (182 EINs), 258 payment supplier strings (196 EINs); PO methods {'exact_norm_name': 145, 'fuzzy_token_set': 42, 'manual_known_ein': 1}
- PASS fuzzy supplier matches (75): ACCESS HOUSING INC. -> ACCESS HOUSING INC DC (100); ACCESS HOUSING INC. (DC) -> ACCESS HOUSING INC DC (100); AFFORDABLE HOUSING OPPORTUNITI -> AFFORDABLE HOUSING OPPORTUNITIES INC (97); AMERICAN ASSOC OF RESIDENTIAL -> AMERICAN ASSOCIATION OF RESIDENTIAL MORTGAGE REGULATORS (100); AMERICAN SOCIETY OF ADDICTION -> AMERICAN SOCIETY OF ADDICTION MEDICINE INC (100); American Society of Addiction -> AMERICAN SOCIETY OF ADDICTION MEDICINE INC (100); BENNING PARK NEIGHBORHOOD CORP -> BENNING PARK NEIGHBORHOOD ASSOCIATI ON (100); BLACK FEM  INC -> BLACKFEM INC (94); BLACK FEM, INC -> BLACKFEM INC (94); BREASTFEEDING OUTREACH FOR GRE -> BREASTFEEDING OUTREACH FOR GREATER WASHINGTON (93); Breastfeeding Outreach for Gre -> BREASTFEEDING OUTREACH FOR GREATER WASHINGTON (93); CAPITOL HILL COUNSELING A -> CAPITOL HILL COUNSELING AND RESOURCE CENTER INC (100); CARE AND PROGRESS COMMUNITY DE -> CARE AND PROGRESS COMMUNITY DEVELOPMENT (94); CATHOLIC CHARITIES -> CATHOLIC CHARITIES OF THE ARCHDIOCESE OF WASHINGTON INC (100); CENTER FOR ADOPTION SUPPORT -> CENTER FOR ADOPTION SUPPORT AND EDUCATION INC (100); CHILDREN & CHARITY INTERNATION -> CHILDREN & CHARITY INTERNATIONAL (97); COALITION FOR THE HOMELESS, IN -> COALITION FOR THE HOMELESS INC (100); COMMUNITY BRIDGE INC -> COMMUNITY BRIDGES INCORPORATED (97); COMMUNITY CONNECTION -> COMMUNITY CONNECTIONS (98); COMMUNITY FAMILY LIFE SERVICE, -> COMMUNITY FAMILY LIFE SERVICES INC (98); COURTNEY S HOUSE INC -> COURTNEYS HOUSE INC (97); COVENANT HOUSE WASHINGTON -> COVENANT HOUSE WASHINGTON DC (100); Care and Progress Community De -> CARE AND PROGRESS COMMUNITY DEVELOPMENT (94); Catholic Charities of the Archdiocese of -> CATHOLIC CHARITIES OF THE ARCHDIOCESE OF WASHINGTON INC (100); DC ACTION FOR CHILDREN TODAY -> DC ACTION FOR CHILDREN TODAY DC ACT (100); DEAF ABUSED WOMEN'S NETWORK -> DEAF ABUSED WOMEN NETWORK (98); DEEDS OF KINDNESS OUTREACH -> DEEDS OF KINDNESS OUTREACH SERVICES (100); DISABLED VETERANS NATL FOUNDAT -> DISABLED VETERANS NATIONAL FOUNDATION (96); DISTRICT ALLIANCE SAFE HOUSING -> DISTRICT ALLIANCE FOR SAFE HOUSING INC (100); DOORS OF HOPE INC -> DOOR OF HOPE (95); Doors of Hope Inc -> DOOR OF HOPE (95); EXCELLENT COMMUNITY SERVI -> EXCELLENT COMMUNITY SERVICES INC (94); FAMILY MEDICAL COUNSELING -> FAMILY AND MEDICAL COUNSELING SERVICE INC (100); FAR SOUTHEAST FAMILY -> FAR SOUTHEAST FAMILY STRENGTHENING COLLABORATIVE (100); FOUR WALLS DEVELOPEMENT INC. -> FOUR WALLS DEVELOPMENT INC (98); FRY PLUMBING & HEATING -> FRY PLUMBING AND HEATING NON PROFIT (100); FRY PLUMBING AND HEATING -> FRY PLUMBING AND HEATING NON PROFIT (100); Fry Plumbing and Heating -> FRY PLUMBING AND HEATING NON PROFIT (100); HOUSING COUNSELING SERVICE -> HOUSING COUNSELING SERVICES INC (98); HOUSING COUNSELING SERVICES, I -> HOUSING COUNSELING SERVICES INC (100); KEY BRIDGE FOUNDATION -> KEY BRIDGE FOUNDATION FOR EDUCATION AND RESEARCH (100); LITTLE SISTERS OF THE POOR -> LITTLE SISTERS OF THE POOR OF WASHINGTON DC INC (100); LUTHERAN SOCIAL SERVICES -> LUTHERAN SOCIAL SERVICES OF THE NATIONAL CAPITAL AREA INC (100); LUTHERAN SOCIAL SERVICES NATL' -> LUTHERAN SOCIAL SERVICES OF THE NATIONAL CAPITAL AREA INC (100); MARTHA S TABLE INC -> MARTHAS TABLE (96); MARY ELIZABETH HOUSE, INC A MI -> THE MARY ELIZABETH HOUSE INC A MINISTRY (93); MISSION FIRST HOUSING DEVELOPM -> MISSION FIRST HOUSING DEVELOPMENT CORPORATION (95); MOUNT LEBANON COMMUNITY DEVELO -> MOUNT LEBANON COMMUNITY DEVELOPMENT CORPORATION (92); Mission First Housing Developm -> MISSION FIRST HOUSING DEVELOPMENT CORPORATION (95); NAT'L FEDERATION OF THE BLIND -> NATIONAL FEDERATION OF THE BLIND OF THE DISTRICT OF COLUMBIA (100); NATIONAL CENTER FOR CHILDREN A -> NATIONAL CENTER FOR CHILDREN AND FAMILIES (100); NATIONAL CENTER FOR VICTIMS OF -> NATIONAL CENTER FOR VICTIMS OF CRIME INC (100); NATIONAL ENERGY AND UTILITY AF -> THE NATIONAL ENERGY AND UTILITY AFFORDABILITY COALITION (94); NATIONAL FEDERATION OF THE BLIND -> NATIONAL FEDERATION OF THE BLIND OF THE DISTRICT OF COLUMBIA (100); NATIONAL FOUNDATION TO END SEN -> NATIONAL FOUNDATION TO END SENIOR HUNGER INC (93); NEIGHBOR S CONSEJO -> NEIGHBORS CONSEJO (97); NORTHERN VIRGINIA FAMILY -> NORTHERN VIRGINIA FAMILY SERVICES INC (100); National Association of State Mental Health Program Directors -> NATIONAL ASSOCIATION OF STATE MENTAL HEALTH PROGRAM DIRECTORS IN (100); National Center For Victims Of -> NATIONAL CENTER FOR VICTIMS OF CRIME INC (100); OMEGA GOLD DEVELOPMENT GR -> OMEGA GOLD DEVELOPMENT GROUP INC (94); PAVING THE WAY MULTI-SERVICE -> PAVING THE WAY MULTI SERVICE INSTITUTE (100); PSI SERVICE III INC -> PSI SERVICES III INC (97); RAPE, ABUSE, INCEST, NATIONAL -> RAPE ABUSE AND INCEST NATIONAL NETWORK INC (100); RESTORATION COMMUNITY ALLIANCE -> RESTORATION COMMUNITY ALLIANCE COMMUNITY DEVLEOPMENT CORPORATION (100); Rape, Abuse, Incest, National -> RAPE ABUSE AND INCEST NATIONAL NETWORK INC (100); SAMARITAN MINISTRY OF GREATER -> SAMARITAN MINISTRY OF GREATER WASHINGTON (100); SERVICE SOURCE, INC -> SERVICESOURCE INC (96); STEPPINGSTONE FOUNDATION, INC. -> STEPPING STONE FOUNDATION INC (98); SYMBRAL FOUNDATION FOR CMTY. -> SYMBRAL FOUNDATION FOR COMMUNITY SERVICES INC (100); Safe Routes to School National Partnersh -> SAFE ROUTES TO SCHOOL NATIONAL PARTNERSHIP (98); THE HOPE FOUNDATION RE-ENTRY -> HOPE FOUNDATION RE-ENTRY NETWORK INC (100); THE MARY ELIZABETH HOUSE -> THE MARY ELIZABETH HOUSE INC A MINISTRY (100); THE NATIONAL REENTRY NETWORK -> THE NATIONAL REENTRY NETWORK FOR RETURNING CITIZENS (100); Torture abolition and Survivors Support -> TORTURE ABOLITION AND SURVIVORS SUPPORT COALITION INTERNATIONAL (100); WASHINGTON REGIONAL ALCOHOL PR -> WASHINGTON REGIONAL ALCOHOL PROGRAM (95)
- PASS POs for universe vendors: 5,602 raw rows -> 4,494 after dedupe on PONUMBER + FISCALYEAR + POTOTAL (repeats removed: 1,108, almost all AA0 sub-office fan-out)
- PASS payments for universe vendors: 5,494 supplier x FY x agency x PO aggregates; FY2025+ rows flagged x_pass_incomplete_fy=1 (PASS incomplete from FY2025, financial-system change)
- fuzzy name matches in DC/HUD documents (21): CENTER FOR NON- PROFIT ADVANCEMENT -> CENTER FOR NONPROFIT ADVANCEMENT (98); CENTER FOR NON-PROFIT ADVANCEMENT -> CENTER FOR NONPROFIT ADVANCEMENT (98); Calvary Women's Service -> CALVARY WOMENS SERVICES INC (98); Catholic Charities -> CATHOLIC CHARITIES OF THE ARCHDIOCESE OF WASHINGTON INC (100); Catholic Charities of the Archdiocese of -> CATHOLIC CHARITIES OF THE ARCHDIOCESE OF WASHINGTON INC (100); Community Family Live Services -> COMMUNITY FAMILY LIFE SERVICES INC (97); Covenant House -> COVENANT HOUSE WASHINGTON DC (100); Covenant House Greater Washington -> COVENANT HOUSE WASHINGTON DC (94); Covenant House Washington -> COVENANT HOUSE WASHINGTON DC (100); DISTRICT ALLIANCE SAFE HOUSING -> DISTRICT ALLIANCE FOR SAFE HOUSING INC (100); Deaf Abused Women's Network -> DEAF ABUSED WOMEN NETWORK (98); Deaf Abused Women's Network (DAWN) -> DEAF ABUSED WOMEN NETWORK (98); Everyone Home -> EVERYONE HOME DC (100); Housing Counseling Service -> HOUSING COUNSELING SERVICES INC (98); Institute for African Man Development Inc. -> INSTITUTE FOR AFRICAN MAN DEVELOPME NT INC (99); Pathways to Housing -> PATHWAYS TO HOUSING DC (100); SURVIVORS AND ADVOCATES FOR EMPOWERM ENT (DC SAFE) -> SURVIVORS AND ADVOCATES FOR EMPOWERMENT SAFE INC (92); SURVIVORS AND ADVOCATES FOR EMPOWERMENT (SAFE) -> SURVIVORS AND ADVOCATES FOR EMPOWERMENT SAFE INC (100); Survivors and Advocates for Empowerment, Inc. -> SURVIVORS AND ADVOCATES FOR EMPOWERMENT SAFE INC (100); The Hope Foundation Reentry Network Inc. -> HOPE FOUNDATION RE-ENTRY NETWORK INC (92); The National Centers for Children and Families -> NATIONAL CENTER FOR CHILDREN AND FAMILIES (99)
- DHS oversight tie-out: 2024 erap_arpa_grants [ARPA] printed $42,070,444 vs parsed $42,070,444 -> tie
- DHS oversight tie-out: 2024 erap_arpa_grants [ERA2] printed $6,326,098 vs parsed $6,326,098 -> tie
- DHS oversight tie-out: 2024 erap_arpa_grants [Local] printed $576,903 vs parsed $576,903 -> tie
- DHS oversight tie-out: 2025 dv_grantees [FY2024 total grant award] printed $4,462,363 vs parsed $4,462,363 -> tie
- DHS oversight tie-out: 2025 dv_grantees [FY2025 total grant award] printed $4,847,166 vs parsed $4,847,167 -> tie
- DHS oversight tie-out: 2025 erap_arpa_grants [ARPA] printed $7,763,167 vs parsed $7,763,167 -> tie
- DHS oversight tie-out: 2025 erap_arpa_grants [ERA2] printed $30,181,471 vs parsed $30,181,472 -> tie
- DHS oversight tie-out: 2025 erap_arpa_grants [Local] printed $22,587,325 vs parsed $22,587,325 -> tie
- DHS oversight tie-out: 2025 homelessness_prevention [FY24] printed $7,450,000 vs parsed $7,450,000 -> tie
- DHS oversight tie-out: 2025 homelessness_prevention [FY25 YTD] printed $6,119,700 vs parsed $6,119,700 -> tie
- DHS oversight tie-out: 2025 psh_case_management [DHS local] printed $25,803,404 vs parsed $25,803,404 -> tie
- DHS oversight tie-out: 2025 psh_case_management [Medicaid] printed $38,687,549 vs parsed $38,687,549 -> tie
- HUD AwardComp DC-500 2019: 38 projects, parsed $22,075,117 vs printed total $22,075,117 -> tie
- HUD AwardComp DC-500 2020: 39 projects, parsed $23,608,105 vs printed total $23,608,105 -> tie
- HUD AwardComp DC-500 2021: 40 projects, parsed $25,062,775 vs printed total $25,062,775 -> tie
- HUD AwardComp DC-500 2022: 43 projects, parsed $27,933,554 vs printed total $27,933,554 -> tie
- HUD AwardComp DC-500 2023: 39 projects, parsed $29,711,325 vs printed total $29,711,325 -> tie
- HUD AwardComp DC-500 2024: 36 projects, parsed $33,659,924 vs printed total $33,659,924 -> tie
- HUD FY2025 round 1 DC-500 (p12): 15 projects, parsed $15,042,362 vs printed $15,042,362 -> tie
- HUD FY2025 round 2 DC-500 (p22): 4 projects, parsed $6,616,773 vs printed $6,616,773 -> tie
- HUD FY2025 round 3 DC-500 (p37): 16 projects, parsed $11,878,879 vs printed $11,878,879 -> tie
- HUD FY2024 AwardComp vs hud.gov DC report: 36 vs 36 projects, total $33,659,924 vs $33,659,924; project-level differences 0: []
- duplicates: award_row_id collisions 0; fully identical rows 0
- Calvary OVSJG rows: 15 (FY2019-FY2025 layer 13, FY2026 PDF 2); match recon: yes
- provider-name match rate (non-PASS): 114/437 distinct names (26%), 903/2097 rows, 49% of dollars; by source {'dc_oversight': '46/93 names, 263/442 rows', 'dc_ovsjg': '73/351 names, 404/1385 rows', 'hud_coc': '19/26 names, 236/270 rows'}; methods {'unmatched': 1194, 'fuzzy_token_set': 136, 'exact_norm_name': 664, 'manual_alias': 68, 'manual_known_ein': 35}

### 2026-10-10 18:23 — 37_parse_dc_budget: DC budget lines and policy events
- interim/stage_dc_budget_lines__dc.csv: 5,172 rows (Counter({'approved': 3172, 'actual': 1968, 'proposed': 32})); in-scope program/agency rows 854; duplicate keys 0
- interim/stage_fact_policy_events__dc.csv: 297 rows; by kind {'change_table_FO0-5': 8, 'change_table_HY0-5': 9, 'change_table_JA0-5': 25, 'yoy_approved_change': 161, 'bsa_subtitle': 25, 'fy2025_change_narrative': 13, 'committee_report_item': 22, 'committee_report_variance': 6, 'change_table_DB0-5': 1, 'council_adjustments_chart_fy2027': 27}; by type {'budget_proposed': 41, 'budget_enacted': 161, 'budget_revised': 66, 'policy_change': 26, 'other': 1, 'program_launch': 2}
- parsed tables: FY2024 JA0 30-PBB (2024_JA0_ja_dhs_tables_2024j.pdf): 62 lines; FY2024 FO0 30-PBB (024_FO0_fo_vsjg_tables_2024j.pdf): 21 lines; FY2024 RM0 30-PBB (2024_RM0_rm_dbh_tables_2024j.pdf): 128 lines; FY2024 DB0 30-PBB (024_DB0_db_dhcd_tables_2024j.pdf): 44 lines; FY2024 HY0 30-PBB (2024_HY0_hy_has_tables_2024j.pdf): 16 lines; FY2024 CF0 30-PBB (2024_CF0_cf_des_tables_2024j.pdf): 69 lines; FY2024 HG0 30-PBB (24_HG0_hg_dmhhs_tables_2024j.pdf): 9 lines; FY2025 JA0 30-PBB (2025_JA0_ja_dhs_tables_2025j.pdf): 61 lines; FY2025 FO0 30-PBB (25_FO0_fo_ovsjg_tables_2025j.pdf): 28 lines; FY2025 RM0 30-PBB (2025_RM0_rm_dbh_tables_2025j.pdf): 87 lines; FY2025 DB0 30-PBB (025_DB0_db_dhcd_tables_2025j.pdf): 36 lines; FY2025 HY0 30-PBB (2025_HY0_hy_hap_tables_2025j.pdf): 7 lines; FY2025 CF0 30-PBB (025_CF0_cf_does_tables_2025j.pdf): 62 lines; FY2025 HG0 30-PBB (25_HG0_hg_dmhhs_tables_2025j.pdf): 8 lines; FY2026 JA0 Table JA0-4 (026_JA0_ja_dhs_chapter_2026o.pdf): 57 lines; FY2026 FO0 Table FO0-4 (26_FO0_fo_vsjg_chapter_2026o.pdf): 26 lines; FY2026 RM0 Table RM0-4 (026_RM0_rm_dbh_chapter_2026o.pdf): 83 lines; FY2026 DB0 Table DB0-4 (26_DB0_db_dhcd_chapter_2026o.pdf): 36 lines; FY2026 HY0 Table HY0-4 (026_HY0_hy_has_chapter_2026o.pdf): 7 lines; FY2026 CF0 Table CF0-4 (26_CF0_cf_does_chapter_2026o.pdf): 61 lines; FY2026 HG0 Table HG0-4 (6_HG0_hg_dmhhs_chapter_2026o.pdf): 6 lines; FY2027 JA0 30-PBB (7_JA0_ja0_dhs_tables_2027a_0.pdf): 57 lines; FY2027 FO0 30-PBB (FO0_fo0_ovsjg_tables_2027a_0.pdf): 26 lines; FY2027 RM0 30-PBB (7_RM0_rm0_dbh_tables_2027a_0.pdf): 80 lines; FY2027 DB0 30-PBB (_DB0_db0_dhcd_tables_2027a_0.pdf): 36 lines; FY2027 HY0 30-PBB (7_HY0_hy0_hap_tables_2027a_0.pdf): 7 lines; FY2027 CF0 30-PBB (_CF0_cf0_does_tables_2027a_0.pdf): 61 lines; FY2027 HG0 30-PBB (HG0_hg0_dmhhs_tables_2027a_0.pdf): 7 lines
- change items: FY2024 JA0 Table JA0-5: 29 change lines, 7 in scope; FY2024 FO0 Table FO0-5: 14 change lines, 3 in scope; FY2024 RM0 Table RM0-5: 25 change lines, 0 in scope; FY2024 DB0 Table DB0-5: 14 change lines, 0 in scope; FY2024 HY0 Table HY0-5: 6 change lines, 6 in scope; FY2024 CF0 Table CF0-5: 16 change lines, 0 in scope; FY2024 HG0 Table HG0-5: 7 change lines, 0 in scope; FY2025 JA0 narrative change sentences (pypdfium2): 8 in scope; FY2025 FO0: chapter change text is font-garbled (amounts missing); OVSJG FY2025 changes taken from the JPS committee report; FY2025 RM0 narrative change sentences (pypdfium2): 0 in scope; FY2025 DB0 narrative change sentences (pypdfium2): 2 in scope; FY2025 HY0 narrative change sentences (pypdfium2): 3 in scope; FY2025 CF0 Table CF0-5: 20 change lines, 0 in scope; FY2025 HG0 narrative change sentences (pypdfium2): 0 in scope; FY2026 JA0 Table JA0-5: 29 change lines, 14 in scope; FY2026 FO0 Table FO0-5: 16 change lines, 4 in scope; FY2026 RM0 Table RM0-5: 27 change lines, 0 in scope; FY2026 DB0 Table DB0-5: 16 change lines, 0 in scope; FY2026 HY0 Table HY0-5: 2 change lines, 2 in scope; FY2026 CF0 Table CF0-5: 17 change lines, 0 in scope; FY2026 HG0 Table HG0-5: 4 change lines, 0 in scope; FY2027 JA0 Table JA0-5: 15 change lines, 4 in scope; FY2027 FO0 Table FO0-5: 11 change lines, 1 in scope; FY2027 RM0 Table RM0-5: 17 change lines, 0 in scope; FY2027 DB0 Table DB0-5: 15 change lines, 1 in scope; FY2027 HY0 Table HY0-5: 3 change lines, 1 in scope; FY2027 CF0 Table CF0-5: 8 change lines, 0 in scope; FY2027 HG0 Table HG0-5: 3 change lines, 0 in scope
- committee report tables: BR_FY25_Housing -> 1 in-scope proposed activity rows (markup 2024-05-09); BR_FY25_JPS -> 0 in-scope proposed activity rows (markup not printed); BR_FY26_committee_budget_report_Human-Services -> 18 in-scope proposed activity rows (markup 2025-06-24); BR_FY26_committee_budget_report_Housing -> 5 in-scope proposed activity rows (markup 2025-06-24); BR_FY26_committee_budget_report_JPS -> 2 in-scope proposed activity rows (markup not printed); BR_FY26_committee_budget_report_Health -> 0 in-scope proposed activity rows (markup 2025-06-23); BR_FY27_committee_budget_report_DRAFT-FY2027-Committee-on-Health -> 2 in-scope proposed activity rows (markup 2026-05-20); BR_FY27_committee_budget_report_FY27-Committee-on-Housing -> 4 in-scope proposed activity rows (markup not printed); BR_FY27_committee_budget_report_52226-FY2027-JPS -> 0 in-scope proposed activity rows (markup not printed)
- FY2027 Council adjustments chart: 1627 rows read, 27 in-scope events
- BSA subtitles kept: 25; curated committee-report items: 22; YoY approved-change events: 161
- tie-outs: 257 pass, 0 fail
- tie-out detail (in-scope divisions): FY2024 JA0 30-PBB p2 division 5000: sum of 23 activities vs subtotal, deltas by column [0, 0, 0, -1] ($000) -> pass | FY2024 JA0 30-PBB p3 agency total: sum of 8 division subtotals, deltas [0, -2, 0, 1] ($000) -> pass | FY2024 JA0 Table JA0-2 p2: sum of 7 fund rows vs GROSS FUNDS, deltas [-1, 0, -1, 0] ($000) -> pass | FY2024 FO0 30-PBB p1 division 4000: sum of 2 activities vs subtotal, deltas by column [0, 0, 0, -1] ($000) -> pass | FY2024 FO0 30-PBB p1 division 5000: sum of 1 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 FO0 30-PBB p1 division 6000: sum of 5 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 FO0 30-PBB p1 agency total: sum of 7 division subtotals, deltas [-2, -1, -2, 1] ($000) -> pass | FY2024 FO0 Table FO0-2 p2: sum of 5 fund rows vs GROSS FUNDS, deltas [0, 0, -1, 0] ($000) -> pass | FY2024 RM0 30-PBB p5 agency total: sum of 16 division subtotals, deltas [0, 1, 1, 0] ($000) -> pass | FY2024 RM0 Table RM0-2 p2: sum of 9 fund rows vs GROSS FUNDS, deltas [0, 1, 0, 1] ($000) -> pass | FY2024 DB0 30-PBB p2 agency total: sum of 9 division subtotals, deltas [0, 0, 0, -1] ($000) -> pass | FY2024 DB0 Table DB0-2 p2: sum of 5 fund rows vs GROSS FUNDS, deltas [1, -1, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 division 4000: sum of 1 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 division 5000: sum of 1 activities vs subtotal, deltas by column [0, 0, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 division 6000: sum of 5 activities vs subtotal, deltas by column [2, -1, 0, 0] ($000) -> pass | FY2024 HY0 30-PBB p1 agency total: sum of 5 division subtotals, deltas [0, 0, -1, 0] ($000) -> pass | FY2024 HY0 Table HY0-2 p1: sum of 1 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2024 CF0 30-PBB p2 division 4000: sum of 16 activities vs subtotal, deltas by column [0, 0, 0, -1] ($000) -> pass | FY2024 CF0 30-PBB p2 division 5000: sum of 3 activities vs subtotal, deltas by column [1, 0, 1, 0] ($000) -> pass | FY2024 CF0 30-PBB p2 division 6000: sum of 6 activities vs subtotal, deltas by column [1, 0, 0, 0] ($000) -> pass | FY2024 CF0 30-PBB p3 agency total: sum of 11 division subtotals, deltas [-1, 0, 0, -1] ($000) -> pass | FY2024 CF0 Table CF0-2 p2: sum of 6 fund rows vs GROSS FUNDS, deltas [1, 0, 0, 0] ($000) -> pass | FY2024 HG0 30-PBB p1 agency total: sum of 4 division subtotals, deltas [0, 0, 0, 0] ($000) -> pass | FY2024 HG0 Table HG0-2 p2: sum of 2 fund rows vs GROSS FUNDS, deltas [0, 1, 0, 0] ($000) -> pass | FY2025 JA0 30-PBB p2 division HS0030: sum of 28 activities vs subtotal, deltas by column [-2, 1, -1, 1] ($000) -> pass | FY2025 JA0 30-PBB p2 agency total: sum of 6 division subtotals, deltas [0, -1, 1, 0] ($000) -> pass | FY2025 FO0 30-PBB p1 division PS0023: sum of 2 activities vs subtotal, deltas by column [0, 0, -1, 0] ($000) -> pass | FY2025 FO0 30-PBB p2 agency total: sum of 12 division subtotals, deltas [-1, -2, 1, 0] ($000) -> pass | FY2025 RM0 30-PBB p3 agency total: sum of 13 division subtotals, deltas [1, 1, 0, 1] ($000) -> pass | FY2025 DB0 30-PBB p2 agency total: sum of 6 division subtotals, deltas [0, 1, 1, 0] ($000) -> pass | FY2025 HY0 30-PBB p1 division EC0039: sum of 5 activities vs subtotal, deltas by column [0, -1, 0, 0] ($000) -> pass | FY2025 HY0 30-PBB p1 agency total: sum of 1 division subtotals, deltas [0, 0, 0, 0] ($000) -> pass | FY2025 CF0 30-PBB p3 agency total: sum of 10 division subtotals, deltas [0, -1, 0, -1] ($000) -> pass | FY2025 CF0 Table CF0-2 p2: sum of 6 fund rows vs GROSS FUNDS, deltas [0, -1, 0, 0] ($000) -> pass | FY2025 HG0 30-PBB p1 agency total: sum of 3 division subtotals, deltas [0, 0, 0, 1] ($000) -> pass | FY2026 JA0 Table JA0-4 p5 division HS0030: sum of 28 activities vs subtotal, deltas [1, -2, 1, -1] ($000) -> pass | FY2026 JA0 Table JA0-4 p5 agency total: sum of 5 divisions, deltas [-1, -1, 0, 0] ($000) -> pass | FY2026 JA0 Table JA0-2 p2: sum of 7 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 FO0 Table FO0-4 p4 division PS0023: sum of 2 activities vs subtotal, deltas [0, 1, 0, 0] ($000) -> pass | FY2026 FO0 Table FO0-4 p4 agency total: sum of 11 divisions, deltas [-2, 0, 0, 0] ($000) -> pass | FY2026 FO0 Table FO0-2 p2: sum of 4 fund rows vs GROSS FUNDS, deltas [-1, 0, 0, 0] ($000) -> pass | FY2026 RM0 Table RM0-4 p7 agency total: sum of 13 divisions, deltas [1, 1, 2, 0] ($000) -> pass | FY2026 RM0 Table RM0-2 p2: sum of 8 fund rows vs GROSS FUNDS, deltas [1, 0, -1, 0] ($000) -> pass | FY2026 DB0 Table DB0-4 p4 agency total: sum of 6 divisions, deltas [1, -1, 0, -1] ($000) -> pass | FY2026 DB0 Table DB0-2 p2: sum of 4 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 HY0 Table HY0-4 p2 division EC0039: sum of 5 activities vs subtotal, deltas [-1, 1, 0, 0] ($000) -> pass | FY2026 HY0 Table HY0-4 p2 agency total: sum of 1 divisions, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 HY0 Table HY0-2 p1: sum of 1 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2026 CF0 Table CF0-4 p5 agency total: sum of 10 divisions, deltas [-1, 1, 0, 0] ($000) -> pass | FY2026 CF0 Table CF0-2 p2: sum of 5 fund rows vs GROSS FUNDS, deltas [-1, 1, 0, 1] ($000) -> pass | FY2026 HG0 Table HG0-4 p3 agency total: sum of 2 divisions, deltas [0, 1, 1, 0] ($000) -> pass | FY2026 HG0 Table HG0-2 p2: sum of 1 fund rows vs GROSS FUNDS, deltas [0, 0, 0, 0] ($000) -> pass | FY2027 JA0 30-PBB p2 division HS0030: sum of 28 activities vs subtotal, deltas by column [-2, -2, -1, -3] ($000) -> pass | FY2027 JA0 30-PBB p2 agency total: sum of 5 division subtotals, deltas [-1, 1, 0, -1] ($000) -> pass | FY2027 JA0 Table JA0-2 p2: sum of 7 fund rows vs GROSS FUNDS, deltas [0, 1, 0, 0] ($000) -> pass | FY2027 FO0 30-PBB p1 division PS0023: sum of 2 activities vs subtotal, deltas by column [1, 0, 0, 0] ($000) -> pass | FY2027 FO0 30-PBB p1 agency total: sum of 11 division subtotals, deltas [-1,
- cross-book disagreements (same FY/stage/code, >$2K apart; later book preferred via x_preferred): 2022 actual JA0 AMP000 total: FY2025 book 33,466,000, FY2024 book 33,534,000 | 2022 actual JA0 AFO000 total: FY2025 book 3,079,000, FY2024 book 3,025,000 | 2022 actual JA0 HS0029 total: FY2025 book 279,438,000, FY2024 book 280,259,000 | 2022 actual JA0 HS0030 total: FY2025 book 625,848,000, FY2024 book 625,869,000 | 2025 approved JA0 H02902 total: FY2026 book 42,867,000, FY2025 book 42,943,000 | 2025 approved JA0 H02905 total: FY2026 book 91,735,000, FY2025 book 91,660,000 | 2025 approved FO0 P01903 total: FY2026 book 18,405,000, FY2025 book 18,312,000 | 2025 approved FO0 PS0019 total: FY2026 book 18,405,000, FY2025 book 18,312,000 | 2025 approved RM0 AFO003 total: FY2026 book 1,120,000, FY2025 book 1,010,000 | 2025 approved RM0 AFO005 total: FY2026 book 567,000, FY2025 book 577,000 | 2025 approved RM0 AFO000 total: FY2026 book 2,378,000, FY2025 book 2,278,000 | 2025 approved RM0 H04201 total: FY2026 book 175,000, FY2025 book 179,000 | 2025 approved RM0 H04202 total: FY2026 book 1,128,000, FY2025 book 1,151,000 | 2025 approved RM0 H04205 total: FY2026 book 381,000, FY2025 book 355,000 | 2025 approved RM0 H04504 total: FY2026 book 1,367,000, FY2025 book 100,000 | 2025 approved RM0 HS0045 total: FY2026 book 37,390,000, FY2025 book 36,123,000 | 2025 approved RM0 H04802 total: FY2026 book 27,140,000, FY2025 book 22,840,000 | 2025 approved RM0 H04805 total: FY2026 book 1,391,000, FY2025 book 5,691,000 | 2025 approved RM0 HS0053 total: FY2026 book 20,351,000, FY2025 book 21,717,000 | 2025 approved CF0 AFO003 total: FY2026 book 2,141,000, FY2025 book 2,222,000 | 2025 approved CF0 AFO000 total: FY2026 book 4,023,000, FY2025 book 4,104,000 | 2025 approved CF0 AMP026 total: FY2026 book 0, FY2025 book -3,000 | 2025 approved CF0 AMP000 total: FY2026 book 24,947,000, FY2025 book 24,944,000 | 2025 approved CF0 O00111 total: FY2026 book 556,000, FY2025 book 559,000 | 2025 approved CF0 GO0047 total: FY2026 book 6,545,000, FY2025 book 6,548,000 | 2025 approved CF0 O05201 total: FY2026 book 15,504,000, FY2025 book 15,422,000 | 2025 approved CF0 GO0052 total: FY2026 book 75,929,000, FY2025 book 75,847,000
- FY2024 old-code -> FY2025 code crosswalk (FY2024 approved): FO0 P02301: FY2024 book 171,000 vs FY2025 book restated 171,000 (delta +0) | FO0 P02303: FY2024 book 45,515,000 vs FY2025 book restated 45,515,000 (delta +0) | FO0 P04502: FY2024 book 3,720,000 vs FY2025 book restated 3,720,000 (delta +0) | HY0 R03903: FY2024 book 4,400,000 vs FY2025 book restated 4,400,000 (delta +0) | HY0 R03904: FY2024 book 0 vs FY2025 book restated 0 (delta +0) | HY0 R03905: FY2024 book 128,094,000 vs FY2025 book restated 128,094,000 (delta +0) | HY0 R03906: FY2024 book 10,581,000 vs FY2025 book restated 10,581,000 (delta +0) | HY0 R03907: FY2024 book 43,296,000 vs FY2025 book restated 43,296,000 (delta +0) | JA0 H03002: FY2024 book 79,033,000 vs FY2025 book restated 93,339,000 (delta +14,306,000) | JA0 H03003: FY2024 book 59,994,000 vs FY2025 book restated 59,994,000 (delta +0) | JA0 H03004: FY2024 book 31,818,000 vs FY2025 book restated 12,421,000 (delta -19,397,000) | JA0 H03007: FY2024 book 2,940,000 vs FY2025 book restated 2,940,000 (delta +0) | JA0 H03008: FY2024 book 42,536,000 vs FY2025 book restated 42,536,000 (delta +0) | JA0 H03009: FY2024 book 2,799,000 vs FY2025 book restated 4,259,000 (delta +1,460,000) | JA0 H03010: FY2024 book 51,764,000 vs FY2025 book restated 60,770,000 (delta +9,006,000) | JA0 H03011: FY2024 book 4,935,000 vs FY2025 book restated 4,935,000 (delta +0) | JA0 H03012: FY2024 book 86,929,000 vs FY2025 book restated 83,014,000 (delta -3,915,000) | JA0 H03013: FY2024 book 4,222,000 vs FY2025 book restated 4,222,000 (delta +0) | JA0 H03014-H03016: FY2024 book 11,541,000 vs FY2025 book restated 11,542,000 (delta +1,000) | JA0 H03017: FY2024 book 73,209,000 vs FY2025 book restated 73,209,000 (delta +0) | JA0 H03018: FY2024 book 10,875,000 vs FY2025 book restated 10,875,000 (delta +0) | JA0 H03019: FY2024 book 1,150,000 vs FY2025 book restated 1,150,000 (delta +0) | JA0 H03022: FY2024 book 1,980,000 vs FY2025 book restated 1,980,000 (delta +0) | JA0 H03023: FY2024 book 12,032,000 vs FY2025 book restated 12,032,000 (delta +0) | RM0 H04308: FY2024 book 29,637,000 vs FY2025 book restated 29,637,000 (delta +0) | RM0 H04504: FY2024 book 1,467,000 vs FY2025 book restated 1,467,000 (delta +0)
- event dates: budget_enacted/budget_revised = Local Budget Act 2nd reading {2024: '2023-05-30', 2025: '2024-06-12', 2026: '2025-07-28', 2027: '2026-06-23'}; budget_proposed = BSA introduced on behalf of the Mayor {2025: '2024-04-03', 2026: '2025-06-02', 2027: '2026-04-14'} (FY2024 proposal date not in downloaded docs -> blank); BSA policy rows = law/act effective date {2024: '2023-09-06', 2025: '2024-09-18', 2026: '2025-12-06', 2027: '2026-08-13'}; committee items = markup date when printed, else Local Budget Act date
- mapping: Table XX0-5 lines before 'Mayor's Proposed Budget' -> budget_proposed; lines between it and 'District's Approved Budget' -> budget_revised (Council changes); FY2027 Council-level changes taken from the activity-level Council chart instead of JA0-5 to avoid double counting
- coverage (stage[+funds] by FY x agency JA0/FO0/RM0/DB0/HY0/CF0/HG0):
| FY2021 | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds |
| FY2022 | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds | actu+funds |
| FY2023 | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds |
| FY2024 | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds |
| FY2025 | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds | actu+funds,appr+funds,prop | actu+funds,appr+funds | actu+funds,appr+funds |
| FY2026 | appr+funds,prop | appr+funds,prop | appr+funds | appr+funds | appr+funds,prop | appr+funds | appr+funds |
| FY2027 | appr+funds | appr+funds | appr+funds,prop | appr+funds | appr+funds,prop | appr+funds | appr+funds |
- warnings (0):

### 2026-10-10 18:24 — 38_parse_hud_counts
- wrote interim/stage_homeless_counts__hud.csv: 49,393 rows ({'bulk_hud_ahar_pit_hic': 48224, 'doc_hud_hic_dc500': 428, 'doc_mwcog_pit': 741}); PIT 39,029, HIC by CoC 9,195, PopSub 428, MWCOG 741
- wrote interim/stage_hic_projects__hud.csv: 1,257 rows (2022: 332, 2023: 292, 2024: 323, 2025: 310)
- HIC project PDFs: provider and facility names are truncated in the PDF itself (fixed-width report cells; same text in pdfplumber chars, pypdf and pdftotext); kept as printed. 'units' = family units (HIC reports units only for households with children). target_population is derived from the bed columns (household type, plus youth/veterans/chronic when all beds are dedicated) and set to single_women / women_with_children only when the provider or project name says women (basis in x_target_population_basis). x_women_focused_org = core peer tier 1a or Calvary; x_dv_focused_org = tier 1b (config/core_peers.csv).
- PIT by CoC (raw/hud/20261010T123731_huduser_2007-2025-PIT-Counts-by-CoC.xlsb): sheets 2007-2025; 39,029 rows for 8 CoCs; unparsed column names 216 (e.g. ['Overall Homeless - Under 18', 'Overall Homeless - Age 18 to 24', 'Overall Homeless - Over 24']); CoC-years absent: none
- partial unsheltered counts (Count Types): MD-601 2021; VA-602 2021
- workbook has no gender columns in any year (only age, race/ethnicity, household and subpopulation splits); DC gender comes from PopSub 2024 and the MWCOG 2025 DC narrative
- HIC by CoC (raw/hud/20261010T123733_huduser_2007-2025-HIC-Counts-by-CoC.xlsx): sheets 2007-2025; 9,195 rows; unparsed columns 9 (['HMIS Participation Rate (ES,TH) (non-numeric)', 'ES HMIS Participation Rate (non-numeric)', 'Total TH Beds for Households with only Children (non-numeric)', 'HMIS Participation Rate for Year-Round Beds (SH) (non-numeric)']); same-measure columns with different values kept as '__alt': 0
- PopSub DC-500 2024 (raw/hud/20261010T123749_hudx_CoC_PopSub_DC-500_2024.pdf): 232 rows; total persons 5616; women 2167
- PopSub DC-500 2025 (raw/hud/20261010T123750_hudx_CoC_PopSub_DC-500_2025.pdf): 196 rows; total persons 5138; women n/a
- MWCOG 2023 report (raw/hud/20261010T123754_mwcog_homelessness_metro_washington_2023_PIT.pdf): 548 table cells kept
- MWCOG 2024 report (raw/hud/20261010T123753_mwcog_homelessness_metro_washington_2024_PIT.pdf): 504 table cells kept
- MWCOG 2025 report (raw/hud/20261010T123752_mwcog_homelessness_metro_washington_2025_PIT.pdf): 520 table cells kept
- MWCOG 2026 report (raw/hud/20261010T123751_mwcog_homelessness_metro_washington_2026_PIT.pdf): 531 table cells kept
- MWCOG: 2103 cells parsed across reports -> 741 after keeping the latest report per jurisdiction/year/measure/population; values revised between reports: 38 (e.g. Prince William County, VA 2022 all: 241 (rpt 2023) -> 282 (rpt 2024); Prince William County, VA 2021 all: 282 (rpt 2023) -> 326 (rpt 2024); Prince William County, VA 2020 all: 326 (rpt 2023) -> 277 (rpt 2024); COG region 2023 households_without_children: 5901 (rpt 2023) -> 5755 (rpt 2024)); same report, two tables disagree (earlier page kept): 17 (District of Columbia 2020 households_with_only_children rpt 2023: p68 12 vs p25 11; Frederick City & County, MD 2021 households_with_only_children rpt 2023: p68 5 vs p25 0; COG region 2020 households_with_only_children rpt 2023: p69 13 vs p25 12; City of Alexandria, VA 2020 all rpt 2023: p68 198 vs p17 207)
- skipped tables (did not parse reliably): none; source-inconsistent columns are kept with confidence medium and an x_note
- not parsed: figures/charts (demographic profiles, income, gender charts), Table 3 population shares, Table 13/14 shelter status, TAY tables, Table 16 bed inventory, Table 17 formerly homeless in PH, Appendix B narrative percentages except the 2025 DC gender-of-adults table
- HIC provider names (cleaned, distinct): 105; matched 42 (40%); methods {'unmatched': 63, 'fuzzy_token_set': 10, 'exact_norm_name': 29, 'manual_known_ein': 2, 'manual_alias': 1}; government providers (no EIN expected) 7; beds at matched providers 67,567 of 133,181 (51%)
- fuzzy matches: Access Housing -> 521918702 (100.0); Access Housing INC (AHI) (Agency) -> 521918702 (100.0); Catholic Charities -> 530196524 (100.0); Catholic Charities (Agency) -> 530196524 (100.0); Covenant House Washington -> 133537709 (100.0); Covenant House Washington (CHW)(Age -> 133537709 (100.0); East River Family Strengthening Collabor -> 522277915 (100.0); Edgewood-Brookland Family Support Col -> 522246995 (100.0); Edgewood/Brookland Family Support Col -> 522246995 (100.0); Far Southeast Family Strengthening Colla -> 522117070 (100.0); Georgia Avenue Family Support Collabor -> 522349433 (100.0); Survivors & Advocates for Empowerment -> 412226446 (100.0)
- unmatched nonprofit providers (not in dc_sector/dmv_sector/core_peers by name): 801 East Collaborative; Bradley & Associates; CCDC; CORE DC; Casa Ruby; Church of Epiphany; Church of the Epiphany; Collaborative Solutions for Communities; Communities Helping & Empowering Pat; Communities Helping and Empowering P; Community Solutions; Cornerstone Community; Dawn Deaf; Deaf Dawn; East of the River Family Support Collabor; Echelon Community Services; Far Southeast Family Support Collaborati; Healthy Babies; Healthy Babies Project; Hillcrest Children & Family Center; Hope and a Home; Institute for Emotional Regulation; Jaydot; Joseph's House; Jubilee Housing; KBEC Group, Inc; KBEC Group, Inc.; KC Community Services; Latin American Youth Center; MBI Health Services; Maximus; Metropolitan Education Solutions; Metropolitan Educational Solutions; North Capitol Collaborative Inc.; North Capitol Family Support Collaborati; Operation Renewed Hope; Positive Kinship Bonding; SLS; SMYAL; Salvation Army; Sasha Bruce Youthwork; Sasha Bruce Youthworks; So Others Might Eat; Spring Leaf; St. Aloysius Roman Catholic Church; St. John's Community Community Servic; St. John's Community Services; Supporting & Mentoring Youth Advocate; Temple Micah; Temple Sinai; The Community Builders and Emory Bea; The Institute for Emotional Regulation, L; The Salvation Army; U.S. Vets; US Veterans Initiative; Wheeler Creek
- matcher (shared with script 36): manual aliases (TCP 521681401; DASH, DC SAFE, Housing Up), norm_name exact, then rapidfuzz token_set_ratio >= 92 (after expanding a truncated last token for raw names >= 30 chars) accepted only when fuzzy_ok() holds: both names >= 2 tokens, a shared non-generic token, no one-sided entity-marker token (foundation, fund, maryland, county, ...), and token containment (ratio >= 0.5) or prefix or only soft one-sided words or fuzz.ratio >= 90; reviewed reject list
- PopSub 2024 gender rows sum 5616 vs total 5616: pass
- MWCOG 2023 p16 'People Experiencing Literal Homelessness by Jurisdiction, 2022 - 2023': pass (2 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p17 'People Experiencing Literal Homelessness by Jurisdiction, 2019-2023': pass (5 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p22 '2023 Persons In Families Experiencing Homelessness by Jurisdiction': pass (4 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p23 'Change In Persons In Families Experiencing Homelessness by Jurisdictio': pass (5 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p25 'Households With Only Children Under Age 18 By Jurisdiction, 2020 - 202': pass (4 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p41 'Comparison of Unsheltered Single Adults By Jurisdiction, 2019 – 2023': pass (5 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p45 'Single Adults Experiencing Chronic Homelessness by Jurisdiction, 2019 ': pass (5 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 p51 'Veterans Experiencing Homelessness By Jurisdiction, 2019 - 2023': pass (5 year/measure columns, 9 jurisdictions + total)
- MWCOG 2023 pp[68, 69] 'People Experiencing Literal Homelessness by Jurisdiction, 20': kept with flags: 14/20 columns do not add up in the source (2022 households_without_children 5,307 vs 5,273; 2022 households_with_adults_and_children 2,329 vs 2,322; 2022 all 7,646 vs 7,605); 2 jurisdiction-years whose household columns do not add up
- MWCOG 2024 p16 'People Experiencing Literal Homelessness by Jurisdiction, 2023 - 2024': pass (2 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p17 'People Experiencing Literal Homelessness by Jurisdiction, 2020-2024*': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p22 '2024 Persons in Families Experiencing Homelessness by Jurisdiction': pass (4 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p23 'Change in Persons in Families Experiencing Homelessness by Jurisdictio': kept with flags: 1/5 columns do not add up in the source (2020 persons_in_families 3,690 vs 3,760)
- MWCOG 2024 p29 'Households With Only Children Under Age 18 By Jurisdiction, 2020 - 202': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p49 'Unsheltered Single Adults Experiencing Homelessness by Jurisdiction, 2': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p52 'Single Adults Experiencing Chronic Homelessness by Jurisdiction, 2020 ': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 p60 'Veterans Experiencing Homelessness by Jurisdiction, 2020 - 2024': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2024 pp[75, 76] 'People Experiencing Literal Homelessness by Jurisdiction, 20': kept with flags: 9/20 columns do not add up in the source (2022 households_without_children 5,154 vs 5,120; 2022 households_with_adults_and_children 2,272 vs 2,265; 2022 all 7,422 vs 7,395); 2 jurisdiction-years whose household columns do not add up
- MWCOG 2025 p17 'People Experiencing Literal Homelessness by Jurisdiction, 2024 - 2025': pass (2 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p18 'People Experiencing Literal Homelessness by Jurisdiction, 2021-2025*': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p22 '2025 Persons in Families Experiencing Homelessness by Jurisdiction': pass (4 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p23 'Change in Persons in Families Experiencing Homelessness by Jurisdictio': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p29 'Households With Only Children Under Age 18 By Jurisdiction, 2021 - 202': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p48 'Comparison of Unsheltered Single Adults by Jurisdiction, 2021 - 2025': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p51 'Single Adults Experiencing Chronic Homelessness by Jurisdiction, 2021 ': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 p59 'Veterans Experiencing Homelessness by Jurisdiction, 2021 - 2025': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2025 pp[73, 74] 'People Experiencing Literal Homelessness by Jurisdiction, 20': pass (20 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p18 'People Experiencing Literal Homelessness by Jurisdiction, 2025-2026': pass (2 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p19 'People Experiencing Literal Homelessness by Jurisdiction, 2019-2026': pass (8 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p24 '2026 Persons in Families Experiencing Homelessness by Jurisdiction': pass (4 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p25 'Change in Persons in Families Experiencing Homelessness by Jurisdictio': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p32 'Households With Only Children Under Age 18 By Jurisdiction, 2022 – 202': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p50 'Comparison of Unsheltered Single Adults by Jurisdiction, 2022 – 2026': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p54 'Single Adults Experiencing Chronic Homelessness by Jurisdiction, 2022 ': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 p59 'Veterans Experiencing Homelessness by Jurisdiction, 2022 – 2026': pass (5 year/measure columns, 8 jurisdictions + total)
- MWCOG 2026 pp[79, 80] 'People Experiencing Literal Homelessness by Jurisdiction, 20': pass (20 year/measure columns, 8 jurisdictions + total)
- MWCOG total persons vs HUD PIT overall, CoC-years that differ: 9: MD-600 2020: MWCOG 453 vs HUD 466; MD-600 2021: MWCOG 537 vs HUD 535; MD-600 2022: MWCOG 571 vs HUD 533; MD-600 2023: MWCOG 659 vs HUD 595; MD-600 2024: MWCOG 658 vs HUD 650; MD-600 2025: MWCOG 608 vs HUD 588; VA-602 2019: MWCOG 169 vs HUD 167; VA-604 2019: MWCOG 277 vs HUD 280; VA-604 2025: MWCOG 392 vs HUD 393
- DC-500 MWCOG vs HUD by year: 2019 6,521/6521, 2020 6,380/6380, 2021 5,111/5111, 2022 4,410/4410, 2023 4,922/4922, 2024 5,616/5616, 2025 5,138/5138, 2026 5,363/n/a
- stage_homeless_counts duplicate keys (coc, jurisdiction, year, measure, population, source): 0
- DC-500 2025 recon values: pit_overall 5138 (exp 5138) pass; pit_sheltered_es 3275 (exp 3275) pass; pit_sheltered_th 1065 (exp 1065) pass; pit_unsheltered 798 (exp 798) pass; hic_beds_year_round__es_th_sh 4965 (exp 4965) pass; hic_beds_year_round__th 1385 (exp 1385) pass; hic_beds_year_round__psh 12696 (exp 12696) pass; hic_beds_year_round__rrh 6012 (exp 6012) pass
- HIC projects 2022 ES: 43 projects; total beds 5,159 vs Total row 5159; year-round 4,795 vs summary p1 4795 vs CoC workbook 4795: pass
- HIC projects 2022 SH: 1 projects; total beds 20 vs Total row 20; year-round 20 vs summary p1 20 vs CoC workbook 20: pass
- HIC projects 2022 TH: 71 projects; total beds 1,783 vs Total row 1783; year-round 1,783 vs summary p1 1783 vs CoC workbook 1783: pass
- HIC projects 2022 PSH: 148 projects; total beds 14,467 vs Total row 14467; year-round 14,467 vs summary p1 14467 vs CoC workbook 14467: pass
- HIC projects 2022 RRH: 34 projects; total beds 7,193 vs Total row 7193; year-round 7,193 vs summary p1 7193 vs CoC workbook 7193: pass
- HIC projects 2022 OPH: 35 projects; total beds 6,498 vs Total row 6498; year-round 6,498 vs summary p1 6498 vs CoC workbook 6498: pass
- HIC projects 2023 ES: 38 projects; total beds 4,026 vs Total row 4026; year-round 3,720 vs summary p1 3720 vs CoC workbook 3720: pass
- HIC projects 2023 SH: 1 projects; total beds 20 vs Total row 20; year-round 20 vs summary p1 20 vs CoC workbook 20: pass
- HIC projects 2023 TH: 65 projects; total beds 1,476 vs Total row 1476; year-round 1,476 vs summary p1 1476 vs CoC workbook 1476: pass
- HIC projects 2023 PSH: 138 projects; total beds 15,349 vs Total row 15349; year-round 15,349 vs summary p1 15349 vs CoC workbook 15349: pass
- HIC projects 2023 RRH: 35 projects; total beds 9,206 vs Total row 9206; year-round 9,206 vs summary p1 9206 vs CoC workbook 9206: pass
- HIC projects 2023 OPH: 15 projects; total beds 5,381 vs Total row 5381; year-round 5,381 vs summary p1 5381 vs CoC workbook 5381: pass
- HIC projects 2024 ES: 46 projects; total beds 4,000 vs Total row 4000; year-round 3,505 vs summary p1 3505 vs CoC workbook 3505: pass
- HIC projects 2024 SH: 1 projects; total beds 20 vs Total row 20; year-round 20 vs summary p1 20 vs CoC workbook 20: pass
- HIC projects 2024 TH: 70 projects; total beds 1,693 vs Total row 1693; year-round 1,693 vs summary p1 1693 vs CoC workbook 1693: pass
- HIC projects 2024 PSH: 154 projects; total beds 11,856 vs Total row 11856; year-round 11,856 vs summary p1 11856 vs CoC workbook 11856: pass
- HIC projects 2024 RRH: 33 projects; total beds 10,156 vs Total row 10156; year-round 10,156 vs summary p1 10156 vs CoC workbook 10156: pass
- HIC projects 2024 OPH: 19 projects; total beds 5,842 vs Total row 5842; year-round 5,842 vs summary p1 5842 vs CoC workbook 5842: pass
- HIC projects 2025 ES: 45 projects; total beds 3,954 vs Total row 3954; year-round 3,580 vs summary p1 3580 vs CoC workbook 3580: pass
- HIC projects 2025 TH: 64 projects; total beds 1,385 vs Total row 1385; year-round 1,385 vs summary p1 1385 vs CoC workbook 1385: pass
- HIC projects 2025 PSH: 159 projects; total beds 12,696 vs Total row 12696; year-round 12,696 vs summary p1 12696 vs CoC workbook 12696: pass
- HIC projects 2025 RRH: 26 projects; total beds 6,012 vs Total row 6012; year-round 6,012 vs summary p1 6012 vs CoC workbook 6012: pass
- HIC projects 2025 OPH: 16 projects; total beds 4,989 vs Total row 4989; year-round 4,989 vs summary p1 4989 vs CoC workbook 4989: pass
- stage_hic_projects duplicate keys (year, type, page, seq): 0
- Calvary HIC 2025 rows pass (7 projects, 124 beds); 2024 Sisters Rise PSH [24] (exp [24])

### 2026-10-10 18:25 — 33_pull_usaspending: stage fact_gov_awards
- interim/stage_fact_gov_awards__federal.csv: 28207 rows; {"named_job_rows_dropped": 1, "usaspending_sub_reports": 11875, "usaspending_prime": 7163, "usaspending_sub": 10733, "fac_reports_kept": 1841, "fac_reports_used": 1831, "fac_lines": 9851, "fac_reports_identical_sefa": 18, "slfrf_dc_report_rows": 462, "slfrf_dc_rows": 461, "named_comparators": {"311597223": {"rows": 51, "by_source_flow": {"usaspending/prime": 2, "usaspending/subaward": 17, "fac_sefa/pass_through_expenditure": 30, "fac_sefa/prime": 2}, "fac_audit_years": ["2020", "2021", "2022", "2023", "2024", "2025"], "fac_expenditure_by_fy": {"2020": 1043889, "2021": 2781894, "2022": 6904511, "2023": 3279830, "2024": 4249604, "2025": 3358800}, "usaspending_amount": 8294415}, "882046704": {"rows": 0, "by_source_flow": {}, "fac_audit_years": [], "fac_expenditure_by_fy": {}, "usaspending_amount": 0}}, "rows": 28207, "duplicate_ids": 0, "rows_missing_provenance": 0, "by_source_flow": {"usaspending/prime": 7162, "usaspending/subaward": 10733, "fac_sefa/prime": 4492, "fac_sefa/pass_through_expenditure": 5359, "treasury_slfrf/subaward": 461}, "ein_filled": 23149}
- Calvary reconciliation: {"fac_fy22_total": 4067718, "fac_fy22_ok": true, "fac_ay2023_total": 4064718, "fac_ay2023_conflict_rows": 4, "hud_14251": [200000], "hud_ok": true, "ppp": [327200], "usaspending_subawards": [["14.252", 25000]], "slfrf": [113488, 3680675], "slfrf_ok": true, "calvary_rows": 13}
- EIN coverage (scope = calvary, core_peers, dc_sector, dmv_sector): {"scope_orgs": 4920, "orgs_with_any_row_by_ein": 234, "by_source": {"usaspending": 185, "fac_sefa": 234, "treasury_slfrf": 2}, "extra_orgs_by_exact_name_state_candidate_only": 60}

### 2026-10-10 18:25 — 35_pull_grantsgov: opportunities
- universe posted+forecasted 1467; candidates 531 (local cfdaList 3, cfda key 3, keyword search 530, title regex 51); fetched 0 (reused 531 saved responses); fetch failures 0; dropped by local filter 245
- interim/stage_fact_opportunities__grantsgov.csv: 286 rows (173 posted, 113 forecasted); duplicate ids 0
- keyword_hits counts: {"homelessness": 6, "housing": 17, "domestic violence": 5, "victim services": 2, "women": 59, "substance use": 47, "workforce": 98, "reentry": 5, "veterans": 19, "aging": 77}
- target-ALN rows: 3; nonprofit-eligible (12/13/25/99): 263
- manifest raw/grantsgov/20261010T182531_pull35_manifest.json

### 2026-10-10 18:26 — 41_pull_soi_extracts: stage
- universe EINs: 15,812
- 990 2012 (12eofinextract990.zip): 294,019 rows read, 2,255 universe rows; fields absent this year: grants_paid, compensation_total, cash_savings_eoy
- 990 2013 (13eofinextract990.zip): 289,603 rows read, 2,255 universe rows
- 990 2014 (14eofinextract990.zip): 299,405 rows read, 2,334 universe rows
- 990 2015 (15eofinextract990.zip): 294,782 rows read, 2,252 universe rows
- 990 2016 (16eofinextract990.zip): 307,483 rows read, 2,421 universe rows
- 990 2017 (17eofinextract990.zip): 300,910 rows read, 2,426 universe rows
- 990 2018 (18eoextract990.zip): 313,339 rows read, 2,514 universe rows
- 990 2019 (19eoextract990.zip): 304,441 rows read, 2,520 universe rows
- 990 2020 (20eoextract990.zip): 273,971 rows read, 2,294 universe rows
- 990 2021 (21eoextract990.zip): 342,920 rows read, 2,874 universe rows
- 990 2022 (22eoextract990.zip): 326,123 rows read, 2,802 universe rows
- 990 2023 (23eoextract990.zip): 338,048 rows read, 2,831 universe rows
- 990 2024 (24eoextract990.zip): 345,365 rows read, 2,985 universe rows
- 990EZ 2012 (12eofinextract990ez.zip): 223,348 rows read, 593 universe rows
- 990EZ 2013 (13eofinextract990ez.zip): 218,981 rows read, 613 universe rows
- 990EZ 2014 (14eofinextract990ez.zip): 234,820 rows read, 659 universe rows
- 990EZ 2015 (15eofinextractEZ.zip): 223,028 rows read, 669 universe rows
- 990EZ 2016 (16eofinextractez.zip): 230,745 rows read, 738 universe rows
- 990EZ 2017 (17eofinextractEZ.zip): 218,097 rows read, 731 universe rows
- 990EZ 2018 (18eoextractez.zip): 226,533 rows read, 766 universe rows
- 990EZ 2019 (19eoextractez.zip): 218,671 rows read, 777 universe rows
- 990EZ 2020 (20eoextractez.zip): 154,314 rows read, 536 universe rows
- 990EZ 2021 (21eoextractez.zip): 218,733 rows read, 867 universe rows
- 990EZ 2022 (22eoextractez.zip): 231,289 rows read, 990 universe rows
- 990EZ 2023 (23eoextractez.zip): 207,536 rows read, 933 universe rows
- 990EZ 2024 (24eoextract990EZ.zip): 203,699 rows read, 986 universe rows
- 990PF 2012 (12eofinextract990pf.zip): 98,948 rows read, 2,671 universe rows; fields absent this year: x_pf_grants_approved_future
- 990PF 2013 (13eofinextract990pf.zip): 100,484 rows read, 2,755 universe rows
- 990PF 2014 (14eofinextract990pf.zip): 101,381 rows read, 2,904 universe rows
- 990PF 2015 (15eofinextract990pf.zip): 103,000 rows read, 2,935 universe rows
- 990PF 2016 (16eofinextract990pf.zip): 105,239 rows read, 3,131 universe rows
- 990PF 2020 (20eoextract990pf.zip): 91,473 rows read, 3,022 universe rows
- 990PF 2021 (21eoextract990pf.zip): 125,312 rows read, 4,417 universe rows
- 990PF 2022 (22eoextract990pf.zip): 115,024 rows read, 4,268 universe rows
- 990PF 2023 (23eoextract990pf.zip): 120,350 rows read, 4,589 universe rows
- 990PF 2024 (24eoextract990pf.zip): 119,059 rows read, 4,796 universe rows
- SOI: 78,109 rows, 9,446 EINs; 0 older-processing-year copies dropped; 0 rows whose copies disagree on total_revenue
- NCCS 2009: 48,857 rows read, 280 universe 990 rows
- NCCS 2010: 184,553 rows read, 932 universe 990 rows
- NCCS 2011: 241,595 rows read, 1,272 universe 990 rows
- NCCS 2012: 273,429 rows read, 1,485 universe 990 rows
- NCCS 2013: 303,225 rows read, 1,645 universe 990 rows
- NCCS 2014: 335,066 rows read, 1,783 universe 990 rows
- NCCS 2015: 358,459 rows read, 1,962 universe 990 rows
- NCCS 2016: 374,252 rows read, 2,045 universe 990 rows
- NCCS 2017: 391,170 rows read, 2,163 universe 990 rows
- NCCS 2018: 406,376 rows read, 2,255 universe 990 rows
- NCCS 2019: 436,217 rows read, 2,393 universe 990 rows
- NCCS 2020: 485,459 rows read, 2,675 universe 990 rows
- NCCS 2021: 491,127 rows read, 2,558 universe 990 rows
- NCCS 2022: 131,588 rows read, 350 universe 990 rows
- NCCS: 22,573 rows staged, 3,105 EINs, tax years 2010-2022; period from SOI match 22,555, from IRS index 18; dropped 901 with no period; 309 EIN-years had >1 return (kept the latest OBJECT_ID)
- NCCS total_revenue equals SOI total_revenue on 99.1% of 22,555 matched rows
- wrote 100,682 rows to interim/stage_fact_org_financials__soi.csv (SOI 78,109; NCCS 22,573)
- duplicate (ein, tax_period_end, return_type, source_id): 0
- Calvary total_revenue QC: bulk_irs_soi_extract TY2020 3,851,984 OK; bulk_irs_soi_extract TY2021 8,867,250 OK; bulk_nccs_efile TY2020 3,851,984 OK; bulk_nccs_efile TY2021 not present
- 990-PF SOI TAX_YR equals derived tax_year on 100.0% of rows
- rows by fiscal_year (period-end year) x return_type / source:
```
source_id   irs_soi_extract              nccs_efile     All
return_type             990 990EZ  990PF        990        
fiscal_year                                                
2002                      0     0      1          0       1
2003                      1     0      1          0       2
2004                      0     0      1          0       1
2005                      1     0      1          0       2
2006                      0     0      1          0       1
2007                      0     2      3          0       5
2008                      2    12      7          0      21
2009                      4    30     14          0      48
2010                    179    93     84          5     361
2011                   1876   519   2408        826    5629
2012                   2227   624   2756       1381    6988
2013                   2279   626   2831       1558    7294
2014                   2299   670   2974       1662    7605
2015                   2365   708   3040       1856    7969
2016                   2445   739    310       1979    5473
2017                   2494   750     23       2078    5345
2018                   2566   763    110       2181    5620
2019                   2625   802   3462       2303    9192
2020                   2649   848   3905       2539    9941
2021                   2761   833   4206       2685   10485
2022                   2852   872   4435       1513    9672
2023                   2862   882   4560          7    8311
2024                    276    85    355          0     716
All                   32763  9858  35488      22573  100682
```
- coverage, bulk_irs_soi_extract (EINs with >=1 row / universe EINs; org-years; median years per covered org):
  - calvary: 1/1; 13; 13
  - calvary_known_funders: 84/88; 881; 10
  - core_peers: 18/18; 235; 13
  - daf_sponsors: 15/15; 184; 13
  - dc_sector: 524/1,027; 4,620; 11
  - dmv_funders: 5,744/7,705; 44,487; 10
  - dmv_sector: 1,942/4,910; 15,530; 9
  - named_comparators: 2/2; 14; 7
  - national_women: 1,395/2,878; 13,420; 12
  - size_matched: 564/566; 6,892; 13
- coverage, bulk_nccs_efile (EINs with >=1 row / universe EINs; org-years; median years per covered org):
  - calvary: 1/1; 7; 7
  - calvary_known_funders: 33/88; 267; 9
  - core_peers: 18/18; 172; 10
  - daf_sponsors: 15/15; 84; 6
  - dc_sector: 370/1,027; 2,550; 7
  - dmv_funders: 650/7,705; 4,046; 6
  - dmv_sector: 1,140/4,910; 7,857; 7
  - named_comparators: 1/2; 11; 11
  - national_women: 959/2,878; 7,769; 9
  - size_matched: 558/566; 4,840; 10

### 2026-10-10 18:26 — 42_pull_propublica: stage
- 2,538 org JSONs read (0 target EINs with no ProPublica record); 18,279 filings_with_data rows; skipped formtypes {}; 0 bad periods
- tax_prd_yr equals derived fiscal_year (period-end year) on 100.0% of rows
- staged 18,279 rows, 2,004 EINs -> interim/stage_fact_org_financials__propublica.csv; duplicates on (ein, tax_period_end, return_type, source_id): 0
- Calvary total_revenue QC: TY2020 3,851,984 OK; TY2021 8,867,250 OK
- cross-check vs SOI: 18,279 matching (ein, period, form) rows; equal total_revenue 100.0%, total_expenses 100.0%, total_assets_eoy 100.0%
- ProPublica rows with no SOI row: 0 (by fiscal_year {})
- rows by fiscal_year x return_type:
```
return_type   990  990EZ  990PF    All
fiscal_year                           
2007            0      1      1      2
2008            0      1      1      2
2009            0      3      4      7
2010           53     20     20     93
2011          392     61    812   1265
2012          440     70    936   1446
2013          448     65    960   1473
2014          448     66    999   1513
2015          465     72   1017   1554
2016          476     66    107    649
2017          484     69      4    557
2018          493     71     15    579
2019          513     73   1082   1668
2020          511     75   1182   1768
2021          536     74   1229   1839
2022          550     69   1245   1864
2023          550     76   1243   1869
2024           28      4     99    131
All          6387    936  10956  18279
```

### 2026-10-10 18:26 — 46_web_named_comparators (stage)
- staged 396 rows -> interim/stage_fact_grants__web_named.csv (exact duplicates dropped 1); recipients {'311597223': 391, '882046704': 5}
- by source_type {'annual_report': 350, 'support_page': 33, 'web': 13}; amount_kind {'unknown': 353, 'mixed': 33, 'cash': 8, 'noncash': 2}; with amount 8, with band 354
- by fiscal_year {2023: 204, 2024: 2, 2025: 155, 2026: 35}
- non-organization entries counted per band only: 570 -> interim/web_named_donor_band_counts.csv; joint credits with a personal name: 6 trimmed to the organization, 1 dropped
- per page (entries, kept, dropped as non-org, status): nc_dwc_ar_2024 669/203/422/ok; nc_dwc_ar_web 277/148/112/ok; nc_dwc_gala_2025 26/4/18/ok; nc_dwc_gala_2026 54/29/18/ok; nc_dwc_rosas_place_pr 1/1/0/ok; nc_dwc_hilton_2026 1/1/0/ok; nc_dwc_ahmanson_grants 2/2/0/ok; nc_dwc_bscf_grantee 1/1/0/ok; nc_dwc_foxwynd 1/1/0/ok; nc_dwc_anthem_2023 1/1/0/ok; nc_dwc_anthem_2026_dwc_pr 1/1/0/ok; nc_cbw_sheworks 1/1/0/ok; nc_cbw_launch_pr 1/1/0/ok; nc_cbw_lacare_pr 2/2/0/ok; nc_cbw_econ_mobility 1/1/0/ok
- this run: Tavily search 0, extract 0, HTTP GET 0, cache hits 0; cumulative (manifest): search 139/300, extract 15/200, HTTP 150; script-46 totals: search 30/30, extract 5/15

### 2026-10-10 18:26 — 45_stage_web_grants
- staged rows 1015: by source_type {'support_page': 249, 'annual_report': 630, 'web': 136}; confidence {'medium': 988, 'high': 27}
- amount stated 34; band only 392; unknown 589
- recipient Calvary 268; core peers 739 (14 peers); whole-list keyword keeps 8
- Calvary-site rows by type {'support_page': 98, 'annual_report': 74, 'anonymous_skipped': 1, 'web': 90}
- pages parsed 20/65; not parsed or failed: nsv_funding_reports (index page (links to annual reports)); openarms_about (no funder list on the site); nebw_reports (index page (links to annual reports)); nebw_ar_2025 (2025 annual report text has no funder list); msp_ar_fy22 (no funder list); dcsafe_ar_fy25 (no funder list (revenue split only)); nuvaya_fin_reports (HTTP 403 and Tavily extract empty); christhouse_ar_2025 (landing page; PDF has no text layer); christhouse_ar_2025_pdf (image-only PDF (12 chars of text)); ehdc_ar_2024 (landing page); ehdc_ar_2024_pdf (2024 annual report text has no funder list); cfh_ar_list (index page); thrive_impact_2024 (lists corporate volunteer groups, not funders); miriams_financials (index page); miriams_ar_fy25 (mkannualreport.org is JavaScript-rendered; no text retrieved); coh_ar_2025 (2025 annual report summary has no funder list); coh_impact_2024 (same list as coh_funders (parsed there)); chgw_home (home page); chgw_impact_fy24 (FY24 impact report text has no funder list); doorways_ar_2023 (landing page); doorways_ar_2023_issuu (issuu viewer; no document text); hormd_honor_roll (URL now serves the About Us page; no honor roll content); hormd_honor_roll_tav (Tavily advanced extract also returns no honor roll content); hormd_ar_2024 (PDF returns HTTP 404); hormd_ar_page (annual report page has no donor list); meyer_118m_28 (2020 list (outside 2024-2026); no Calvary or peers); meyer_635k_8 (2022 list (outside 2024-2026); no Calvary or peers); meyer_rapid (program description only; no 
- in-kind evidence rows 17: MGAC=unclear; MGAC=in_kind; MGAC=in_kind; MGAC=cash; Health Equity Fund=cash; Health Equity Fund=cash; Health Equity Fund=cash; Health Equity Fund=cash; Capital One=unclear; Capital One=unclear; Capital One=cash; World Bank Community Connections Fund=cash; World Bank Community Connections Fund=cash; World Bank Community Connections Fund=cash; Frontier Co-op / Aura Cacia (Frontier Co-op Giving Fund)=in_kind; Frontier Co-op / Aura Cacia (Frontier Co-op Giving Fund)=unclear; MGAC; Capital One; World Bank Community Connections Fund=unclear
- Tavily usage to date (manifest, scripts 43-44): search 139/300, extract 15/200; plus 1 exploratory search during development (same query as cal_audit_fy24; response not saved). HTTP GETs 150.
- appended notes_for_analysis.md 'Web funder data' and open_questions.md

### 2026-10-10 18:27 — 50_parse_xml: progress
- 2,000/31,483 parsed in 0.5 min; grants 698,214, roles 22,703, relationships 5,719; errors 0

### 2026-10-10 18:27 — 50_parse_xml: progress
- 4,000/31,483 parsed in 0.6 min; grants 764,178, roles 41,319, relationships 9,850; errors 0

### 2026-10-10 18:27 — 50_parse_xml: progress
- 6,000/31,483 parsed in 0.6 min; grants 804,949, roles 56,969, relationships 10,909; errors 0

### 2026-10-10 18:27 — 50_parse_xml: progress
- 8,000/31,483 parsed in 0.7 min; grants 833,504, roles 71,609, relationships 11,579; errors 0

### 2026-10-10 18:27 — 50_parse_xml: progress
- 10,000/31,483 parsed in 0.7 min; grants 855,931, roles 83,719, relationships 11,966; errors 0

### 2026-10-10 18:27 — 50_parse_xml: progress
- 12,000/31,483 parsed in 0.7 min; grants 872,756, roles 94,450, relationships 12,310; errors 0

### 2026-10-10 18:27 — 50_parse_xml: progress
- 14,000/31,483 parsed in 0.7 min; grants 885,831, roles 104,143, relationships 12,537; errors 0

### 2026-10-10 18:27 — 50_parse_xml: progress
- 16,000/31,483 parsed in 0.8 min; grants 896,903, roles 112,869, relationships 12,668; errors 0

### 2026-10-10 18:27 — 50_parse_xml: progress
- 18,000/31,483 parsed in 0.8 min; grants 906,213, roles 120,818, relationships 12,795; errors 0

### 2026-10-10 18:27 — 50_parse_xml: progress
- 20,000/31,483 parsed in 0.8 min; grants 913,747, roles 128,321, relationships 12,858; errors 0

### 2026-10-10 18:27 — 50_parse_xml: progress
- 22,000/31,483 parsed in 0.8 min; grants 919,346, roles 135,225, relationships 12,862; errors 0

### 2026-10-10 18:27 — 50_parse_xml: progress
- 24,000/31,483 parsed in 0.8 min; grants 923,248, roles 141,620, relationships 12,864; errors 0

### 2026-10-10 18:27 — 50_parse_xml: progress
- 26,000/31,483 parsed in 0.9 min; grants 925,353, roles 148,088, relationships 12,864; errors 0

### 2026-10-10 18:27 — 50_parse_xml: progress
- 28,000/31,483 parsed in 0.9 min; grants 926,494, roles 154,519, relationships 12,864; errors 0

### 2026-10-10 18:27 — 50_parse_xml: progress
- 30,000/31,483 parsed in 0.9 min; grants 926,838, roles 160,722, relationships 12,864; errors 0

### 2026-10-10 18:27 — 50_parse_xml: done
- parsed 31,483 of 31,483 returns in 0.9 min; errors 0 -> xml_parse_errors.csv
- interim/stage_fact_org_financials__xml.csv: 31,483 rows {'990PF': 24877, '990': 4872, '990EZ': 1734}; amended 335; EIN differs from index 0
- interim/stage_fact_grants__xml.csv: 926,887 rows
- interim/stage_fact_roles__xml.csv: 163,918 rows
- interim/stage_fact_org_relationships__xml.csv: 12,864 rows
- interim/org_profile__xml.csv: 31,483 rows (6,774 EINs; street kept on latest return only)
- interim/xml_schedule_i_part3.csv: 1,730 Schedule I Part III lines (aggregates, no names)
- schema versions: {'2014v5.0': 1, '2014v6.0': 1, '2015v2.1': 1, '2015v3.0': 1, '2016v3.0': 2, '2017v2.3': 2, '2018v3.1': 2, '2019v5.1': 1, '2019v5.2': 1, '2020v4.0': 1671, '2020v4.1': 2870, '2020v4.2': 423, '2021v4.0': 1467, '2021v4.1': 767, '2021v4.2': 3218, '2022v4.0': 4, '2022v4.1': 248, '2022v5.0': 5526, '2023v4.0': 271, '2023v5.0': 2462, '2023v5.1': 2421, '2023v6.0': 960, '2024v5.0': 1374, '2024v5.1': 1978, '2024v5.2': 2496, '2024v5.5': 372, '2025v4.0': 1220, '2025v4.1': 1441, '2025v4.2': 282}
- DAF1 sponsors, Schedule I kept only for DC/MD/VA recipients (all years in scope):
  - FIDELITY INVESTMENTS CHARITABLE GIFT FUND (110303001): national 372,180 rows / $58,823.5M; kept DMV 24,496 / $8,007.2M; filtered out $50,816.2M
  - DONOR ADVISED CHARITABLE GIVING INC (311640316): national 257,532 rows / $28,043.2M; kept DMV 17,453 / $4,001.7M; filtered out $24,041.5M
  - NATIONAL PHILANTHROPIC TRUST (237825575): national 83,803 rows / $26,775.7M; kept DMV 6,855 / $3,393.6M; filtered out $23,382.1M
  - VANGUARD CHARITABLE ENDOWMENT PROGRAM (232888152): national 113,808 rows / $12,077.0M; kept DMV 9,471 / $2,022.5M; filtered out $10,054.5M
  - AMERICAN ONLINE GIVING FOUNDATION INC (810739440): national 228,879 rows / $10,079.9M; kept DMV 15,079 / $1,159.3M; filtered out $8,920.6M
  - AMERICAN ENDOWMENT FOUNDATION (341747398): national 65,226 rows / $4,638.5M; kept DMV 5,501 / $441.8M; filtered out $4,196.7M
  - BANK OF AMERICA CHARITABLE GIFT FD (046010342): national 4 rows / $3,249.2M; kept DMV 0 / $0.0M; filtered out $3,249.2M
  - THE AYCO CHARITABLE FOUNDATION (141782466): national 21,612 rows / $2,375.6M; kept DMV 1,874 / $113.0M; filtered out $2,262.5M
  - Renaissance Charitable Foundation Inc (352129262): national 5 rows / $2,288.2M; kept DMV 0 / $0.0M; filtered out $2,288.2M
  - PAYPAL CHARITABLE GIVING FUND (450931286): national 47,570 rows / $1,897.4M; kept DMV 3,864 / $145.8M; filtered out $1,751.5M
  - CHARITIES AID FOUNDATION AMERICA (431634280): national 44,986 rows / $1,870.2M; kept DMV 3,095 / $204.6M; filtered out $1,665.5M
  - THE BLACKBAUD GIVING FUND (460942102): national 35,201 rows / $1,351.7M; kept DMV 2,007 / $135.2M; filtered out $1,216.5M
  - THE GOLDMAN SACHS CHARITABLE GIFT FUND (113813663): national 12,471 rows / $1,056.1M; kept DMV 1,077 / $131.3M; filtered out $924.9M
  - BNY MELLON CHARITABLE GIFT FUND C/O BNY MELLON NA (300748315): national 5,467 rows / $1,022.5M; kept DMV 466 / $17.6M; filtered out $1,004.9M
  - THE US CHARITABLE GIFT TRUST (311663020): national 12,033 rows / $883.9M; kept DMV 984 / $29.0M; filtered out $854.9M

### 2026-10-10 18:27 — 51_qc_xml
- fetch 100.00% of 31,483
- parse errors 0
- PF grants sum exact 99.96% of returns with grants (99.81% of all PF); named-grantee rows cover 93.8% of PF grant dollars
- Calvary revenue checks pass
- Cafritz EIN 526036989; TY2024 to Calvary $170,000
- Calvary grant rows 150 from 50 funders ($4,701,886)
- trace 20/20
- report -> interim/xml_qc.md

### 2026-10-10 18:27 — 60_stage_inputs
- stage_fact_org_financials__inputs.csv: 17 rows
- stage_fact_gov_awards__inputs.csv: 8 rows
- stage_fact_grants__inputs.csv: 360 rows
- stage_fact_roles__inputs.csv: 195 rows

### 2026-10-10 18:30 — 61_resolve_entities
- unique name keys 232,696; alias rows 231,716
- occurrences by method:
match_method  exact_ein  exact_name_city  exact_name_national  exact_name_state  fuzzy_name_city  known_funder  manual  manual_reject  unmatched
role                                                                                                                                            
funder           925013                0                  274                 0                0           227      59             23       3062
pass_through        686                0                 1936                 0                0             0      16              0      14243
recipient        212746           344250                  912             51870            27536             0      48              2     285961

### 2026-10-10 18:31 — 62_build_facts
- fact_org_financials: 150,461 rows
- fact_grants: 928,658 rows
- fact_gov_awards: 40,300 rows
- fact_opportunities: 286 rows
- fact_policy_events: 297 rows
- supp_calvary_individual_donor_bands.csv: copied from stage_supp_calvary_individual_donor_bands.csv
- supp_calvary_program_metrics.csv: copied from stage_supp_calvary_program_metrics.csv
- supp_calvary_strategic_targets.csv: copied from stage_supp_calvary_strategic_targets.csv
- supp_homeless_counts.csv: copied from stage_homeless_counts__hud.csv
- supp_hic_projects.csv: copied from stage_hic_projects__hud.csv
- supp_dc_budget_lines.csv: copied from stage_dc_budget_lines__dc.csv

### 2026-10-10 18:32 — 63_build_dims
- dim_org: 105,189 rows
- dim_funder: 8,928 rows
- dim_program_area: 13 rows
- dim_period: 28 rows
- dim_geo: 246 rows

### 2026-10-10 18:32 — 64_people_relationships
- fact_roles 163,473; dim_person 48,563 (multi-org 2,036); candidate_interlocks 1,270; fact_org_relationships 544,041 {'grant': 432430, 'daf_sponsor_grant': 90830, 'schedule_r_related': 12864, 'shared_board_member': 4162, 'pass_through_funding': 3755}

### 2026-10-10 18:33 — 63_build_dims
- dim_org: 105,189 rows
- dim_funder: 8,928 rows
- dim_program_area: 13 rows
- dim_period: 28 rows
- dim_geo: 246 rows

### 2026-10-10 18:34 — 70_quality_checks
- wrote reports/data_quality.md; duplicates []; portability issues []

### 2026-10-10 18:35 — 80_docs
- data_dictionary rows 542; undocumented columns 0; source_ids missing from registry: none

### 2026-10-10 18:40 — 61_resolve_entities
- unique name keys 232,677; alias rows 231,647
- occurrences by method:
match_method  exact_ein  exact_name_city  exact_name_national  exact_name_state  fuzzy_name_city  known_funder  manual  manual_reject  unmatched
role                                                                                                                                            
funder           925013                0                  274                 0                0           227      59             23       3062
pass_through        686                0                 1936                 0                0             0      16              0      14243
recipient        212746           344250                  912             51870            27536             0      48              2     285868

### 2026-10-10 18:42 — 61_resolve_entities
- unique name keys 232,677; alias rows 231,647
- occurrences by method:
match_method  exact_ein  exact_name_city  exact_name_national  exact_name_state  fuzzy_name_city  known_funder  manual  manual_reject  unmatched
role                                                                                                                                            
funder           925013                0                  274                 0                0           227      59             23       3062
pass_through        686                0                 1936                 0                0             0      16              0      14243
recipient        212746           344250                  912             51870            27536             0      48              2     285868

### 2026-10-10 18:45 — 61_resolve_entities
- unique name keys 232,677; alias rows 231,647
- occurrences by method:
match_method  exact_ein  exact_name_city  exact_name_national  exact_name_state  fuzzy_name_city  known_funder  manual  manual_reject  unmatched
role                                                                                                                                            
funder           925013                0                  274                 0                0           227      59             23       3062
pass_through        686                0                 1936                 0                0             0      16              0      14243
recipient        212746           344250                  912             51870            27536             0      48              2     285868

### 2026-10-10 18:46 — 62_build_facts
- fact_org_financials: 150,461 rows
- fact_grants: 928,658 rows
- fact_gov_awards: 40,300 rows
- fact_opportunities: 286 rows
- fact_policy_events: 297 rows
- supp_calvary_individual_donor_bands.csv: copied from stage_supp_calvary_individual_donor_bands.csv
- supp_calvary_program_metrics.csv: copied from stage_supp_calvary_program_metrics.csv
- supp_calvary_strategic_targets.csv: copied from stage_supp_calvary_strategic_targets.csv
- supp_homeless_counts.csv: copied from stage_homeless_counts__hud.csv
- supp_hic_projects.csv: copied from stage_hic_projects__hud.csv
- supp_dc_budget_lines.csv: copied from stage_dc_budget_lines__dc.csv

### 2026-10-10 18:47 — 63_build_dims
- dim_org: 105,189 rows
- dim_funder: 8,928 rows
- dim_program_area: 13 rows
- dim_period: 28 rows
- dim_geo: 246 rows

### 2026-10-10 18:47 — 64_people_relationships
- fact_roles 163,473; dim_person 48,563 (multi-org 2,036); candidate_interlocks 1,270; fact_org_relationships 544,041 {'grant': 432430, 'daf_sponsor_grant': 90830, 'schedule_r_related': 12864, 'shared_board_member': 4162, 'pass_through_funding': 3755}

### 2026-10-10 18:48 — 63_build_dims
- dim_org: 105,189 rows
- dim_funder: 8,928 rows
- dim_program_area: 13 rows
- dim_period: 28 rows
- dim_geo: 246 rows

### 2026-10-10 18:49 — 70_quality_checks
- wrote reports/data_quality.md; duplicates []; portability issues []

### 2026-10-10 18:50 — 80_docs
- data_dictionary rows 542; undocumented columns 0; source_ids missing from registry: none
