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
