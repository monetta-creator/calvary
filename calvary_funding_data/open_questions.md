# Open questions and decisions

The engagement lead was often away during the build and asked for reasonable, documented assumptions instead of waiting on confirmations (2026-10-10). This file has three parts:
- **Part A:** what was decided, and on what basis. Revisit these if you disagree; most are a config edit plus a rerun.
- **Part B:** questions only Calvary can answer.
- **Part C:** optional extensions.

## A. Decisions and assumptions (in effect)

**Calvary's own data**
- **A1. CRM GIFT_TOTAL window.** It is treated as cumulative over an unconfirmed window; the user believes it covers 2023–2026.
  - Rows carry `cumulative_flag=1`. Confidence is medium, or low for the 21 rows where NUM_GIFTS=1 but GIFT_TOTAL exceeds the last gift.
  - LAST_CONTRIB_AMT and LAST_CONTRIB_DATE are high confidence.
- **A2. CRM cash vs in-kind.** Gifts are assumed cash unless contradicted. Each funder is checked against its own filings in `clean/supp_crm_cash_verification.csv`.
  - Web evidence: Health Equity Fund = cash; MGAC = mixed (pro bono project management); Capital One = unclear.
- **A3. Missing audits.**
  - FY22 audit: found on Candid and used.
  - FY24/FY25 audits: not public. Those years rely on the 990 XML and the TY2024 990.
  - FY13 and FY14 audits: found on Calvary's site and used.
- **A4. "At a Glance 2024"** is treated as FY24, matching the FY23 flyer's naming.
- **A5. Single audits.** Calvary has single audits for FY22 (FAC and the Candid PDF) and FY23 (the PDF; FAC's "2023" record duplicates FY22 and is flagged). Prior years were stated as not subject to a single audit.
- **Health Equity Fund.** Attributed to the Greater Washington Community Foundation (EIN 237343119) as funder of record (`config/funder_match_overrides.csv`), on the web evidence.

**Scope and geography**
- **Core peers.** The 18 are provisional and were picked by the build lead (`config/core_peers.csv`). Rationale and alternates are in `reports/core_peers_proposal.md`.
- **Named comparators.** Downtown Women's Center (311597223) and the California Black Women's Collective Empowerment Institute / SheWorks (882046704), at the Calvary CEO's request. Both go in every analysis.
- **Peer geography.** CBSA 47900, covering DC/MD/VA counties in the DC MSA. Baltimore-area orgs appear only when named (e.g., House of Ruth Maryland).
- **NTEE P83 Women's Centers** added to `national_women` (NW4), `size_matched` and the sector adjacent codes. It was missing from the IRS NTEE table.
- **`size_matched` band.** Revenue 0.5–2× Calvary's TY2022–24 median ($4.97M), so the TY2021 $8.87M outlier is excluded.
- **`dmv_funders`.** Includes private operating foundations (FOUNDATION 02/03, 502 of 5,810). Filter on `dim_org.foundation_code` if unwanted.
- **Geocoding.**
  - Point geocodes cover the DMV and named-comparator universes. National universes stop at ZIP→county; PO-box filers stop at county.
  - 31 orgs are unresolved.
  - One residential-looking BMF street was replaced with the office address from its 990 (`config/org_address_overrides.csv`).
- **Inflation.** CPI-U US annual average, base 2024, applied by fiscal-year-end calendar year. The DC-metro CPI is in `dim_period` (2015+) for sensitivity checks.

**Sources**
- **USAspending.** Covers the 24 target assistance listings for DC/MD/VA recipients, plus all awards for UEI-matched universe orgs. The Treasury SLFRF subaward file is included because USAspending misses that money.
- **DAF sponsors.** Schedule I is kept only for DC/MD/VA recipients; national totals are in `interim/xml_daf_filter_totals.csv`. Consequence: DAF grants to the LA named comparators are not captured.
- **HUD CoC.** Projects with TCP as applicant are stored once, as a subaward to the sponsor with TCP as the pass-through, to avoid double counting.
- **Skipped as not needed:**
  - Charity Navigator (paid; ratings only)
  - SAM.gov Entity API (UEIs came from FAC/USAspending)
  - DC Council LIMS token (one report)
  - OCR of the FY2026 budget appendix (FY2027 books carry FY2026 approved amounts)
  - FRED (BLS covers it)
- **TY2016 990 PDF** (one scanned page): the e-file XML is used instead.
- **Committee budget recommendations the Council did not enact** stay in `fact_policy_events` as `budget_proposed`.

**Privacy**
- **Individual donors** in Calvary's reports are stored only as counts per gift band.
- **Grant recipients who are individuals** (scholarships, emergency aid) have their name, city and ZIP redacted. A second-pass rule is in `scripts/lib/privacy.py`.
- **Governance people data** is limited to what the filings disclose about organizational roles.

## B. Questions for Calvary (would improve accuracy)

1. **CRM export:** Is GIFT_TOTAL limited to gifts dated 2023–2026, or lifetime? Is it by gift date or by fiscal year? How much of MGAC's $712,730 and Capital One's $367,340 is in-kind or pro bono value, or matching?
2. **FY24 and FY25 audits:** these are not public. Did Calvary have single audits for FY24/FY25? None are in FAC, though FY24's would have been due 2025-06-30.
3. **DHS funding via TCP:** amounts are public for one year only (2024-cycle oversight Attachment 77). TCP's 990s don't itemize provider payments. Calvary's TCP subgrant agreements for FY2023–FY2026 would fill this stream. The other route is the unposted DHS Excel attachments: the 2025-cycle "Attachment 27 Contracts FY24-FY25" and the 2026-cycle "Question_13_JA0_2026.xls".
4. **SheWorks:** program-level budget and funders. It started after the institute's TY2024 990, and public sources name supporters without amounts.

## C. Optional extensions (scope choices for the analysis)

- **Large DC providers outside the sector universes.** Their DC/HUD award rows have no EIN: SOME, Sasha Bruce, LAYC, Ayuda, NVRDC, Wendt Center, Collaborative Solutions, Greater Washington Urban League, DC Bar Foundation. Their NTEE codes fall outside the sector sets. Adding them means pinning them in `config/universes.yaml` and rerunning.
- **PASS payments FY2025+:** missing after DC's financial-system change. A FOIA to OCFO would be needed.
- **National funders of the LA named comparators** (Hilton, Ahmanson, Weingart, California Endowment): their 990-PFs are not in the DMV funder universe. Add them as a pinned funder list if the analysis compares funding bases.
- **HIC provider names in `entity_aliases`:** not added. `clean/supp_hic_projects.csv` carries `recipient_ein` where matched.
- **Recipient names of grants to individuals:** redacted. Reverse this only if scholarship giving becomes a topic (one line in `scripts/62_build_facts.py`).
