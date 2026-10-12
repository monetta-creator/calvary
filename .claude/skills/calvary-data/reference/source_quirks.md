# Source quirks (verified during the 2026-10-10 data build and the 2026-10-11 fix cycle)

Check here before writing a new pull or interpreting a figure from these sources.

## IRS and nonprofit filings
- **IRS e-file XML:** fetch by OBJECT_ID from the GivingTuesday data lake (`gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{id}_public.xml`). GivingTuesday lacks the 2026 batches 05B and 08A; fall back to range reads of the IRS ZIPs (`calvary_funding_data/scripts/lib/xmlstore.py`). Some 2026 IRS ZIPs use Deflate64 (`inflate64` handles it). Some files start with a UTF-8 BOM. The IRS index `SUB_DATE` is year-only from 2022.
- **Name lines:** some filings repeat the organization name in both name lines. Collapse only multi-word repeats ("Johnson & Johnson" is a real name).
- **990 Part VIII:** line 1c is event contributions, line 8a gross fundraising-event income, 8c net. Organizations move the gala between them from year to year (Calvary did in FY25).
- **ProPublica:** `tax_prd_yr` is the fiscal-year-end year. Search caps at 10K results / 400 pages. XML downloads sit behind Cloudflare, so use GivingTuesday.
- **IRS BMF:** NTEE is blank for some large foundations (Meyer, Graham). NTEE T21 "corporate foundation" is unreliable (Cafritz and Wyss are coded T21). P83 Women's Centers is valid in NCCS but missing from the IRS eo-info table. The Schwab DAF's legal name is "Donor Advised Charitable Giving" (311640316).
- **TCP** (521681401) does not itemize provider payments on Schedule I, so DHS money to providers is not in its 990.

## Federal
- **Federal Audit Clearinghouse** (api.fac.gov): `audit_year` is the fiscal-year-end year; needs an api.data.gov key. Calvary's "2023" record duplicates FY22. SEFA expenditure against prior-year CoC awards gives the draw rate (28% FY22, 58% FY23).
- **USAspending:** misses most DC pass-through (SLFRF, EFSP, CoC via TCP); the Treasury SLFRF subaward file fills SLFRF. `recipient_search_text` above 20 terms returns 503. Throttles after bursts.
- **Grants.gov `search2`:** the `aln` filter is silently ignored; use `cfda`.
- **HUD CoC:** the FY2025 NOFO was enjoined and FY2025 renewals paid in full; the FY2026 NOFO (awards about December 2026) is live and in litigation. HUD's 29 September 2026 notice ends the Emergency Housing Voucher program by 31 December 2026.

## DC
- **DC budget books:** FY2025 chapter tables extract as garbled text, so use appendix Schedule 30-PBB. FY2026 appendix tables are images. The FY2027 book carries FY2026 approved amounts. The FY2027 OVSJG restoration is $5.1M one-time plus $0.5M recurring.
- **DC MAR 2 API** (`datagate.dc.gov/mar/open/api/v2.2/locations/{addr}?apikey=`) returns ward, ANC, tract and lat/lon. The Census Geocoder knows Marion Barry Ave SE only by its old name, Good Hope Rd SE.

## Census
- A new Census API key needs email activation (`invalid_key.html` until then). DC wards are the ACS state-legislative-district (upper) geography.

## Funders' own pages (October 2026)
- Status changes fast. Record the date checked and the URL in `config/guideline_notes.csv`. Third-party profiles (Candid, GrantedAI, Grantable, Instrumentl) are secondary: label them, and prefer the funder's own FAQ or guidelines page.
- Clark Charitable Foundation (the A. James & Alice B. Clark Foundation) closed on 31 Dec 2025. Schattner and Abell are invitation-only. Venable takes DC applications only from recent grantees or by invitation. Meyer closed to new applicants in 2026. Many Hands requires a budget of $0.5–5M. Jane Bancroft Robinson grants through periodic RFPs (East of the Anacostia focus).
