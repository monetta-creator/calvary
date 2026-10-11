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
