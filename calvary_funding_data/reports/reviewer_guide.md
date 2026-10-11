# Reviewer guide: how much to trust this data

This is for someone reviewing the dataset without reading code. It covers:
1. what was built
2. how it was checked
3. where to be skeptical
4. how to verify it yourself in about 10 minutes

The detailed QC output is in `reports/data_quality.md`; this page summarizes it.

## 1. What was built

The dataset is a funding map around **Calvary Women's Services** (DC; EIN 521307706). It covers:
- **Calvary's money:** its finances FY11–FY25 and every funding stream: government, foundations, corporations, donor-advised funds.
- **Comparison groups:** 18 core DC-area peers, the DC and DMV nonprofit sectors, women's/DV organizations nationwide, size-matched organizations, and two organizations Calvary's CEO asked to include in every analysis: Downtown Women's Center (LA) and SheWorks (LA).
- **Funders:** every DMV private foundation and grantmaking public charity, the national DAF sponsors, and the funders named in Calvary's own records.
- **Grants:** 928,658 grant rows (who gives to whom, how much, when), mostly from funders' IRS filings, TY2020–TY2025.
- **Government funding:** 40,300 award rows from federal, DC and HUD sources, including federal money passed through DC government.
- **People and relationships:** board and officer roles (163K rows), cross-organization links, DC budget lines and policy changes, and census need data by ward.

Every row says where it came from (`source_id`, listed in `sources/source_registry.csv` with a URL or file) and when it was retrieved.

## 2. How it was checked

| Check | Result |
|---|---|
| Calvary's audits balance internally (revenue lines sum to totals, expenses by function, balance sheet) | 260 of 260 checks pass, across 8 audits and 6 readable 990 PDFs |
| Calvary's revenue agrees across independent sources (IRS e-file XML, IRS SOI extract, ProPublica, NCCS, 990 PDFs) | 0 of 42 year-source rows differ by >1%. Audits differ 0–9% on revenue for a known reason (GAAP in-kind and special-event presentation), and net assets match every year. |
| Foundation grant lists add up to the totals the foundations reported | Exact on 99.96% of 18,116 returns with grants |
| Parsed rows match the original IRS file | 20 of 20 random rows traced to the exact XML element |
| XML fetch and parse | 31,469 of 31,469 returns fetched; 0 parse errors |
| DC budget tables tie to the documents' printed totals | 257 of 257 |
| HUD CoC awards and housing-inventory beds tie to HUD's printed totals | All years tie |
| Independent confirmations of specific facts | The Cafritz Foundation's own filing shows $170,000 to Calvary (TY2024). The FY22 audit (found on Candid) matches the federal audit clearinghouse's FY22 total within $3,000. Calvary's OVSJG awards match across DC's open-data layer and its PDF award lists. The Philip L. Graham Fund's published $200K two-year grant matches the CRM's $100K first installment. |
| Duplicate keys in any clean table | None |
| Portability (no local paths, usernames or keys in shared files) | Clean |
| Rebuild from raw data | See section 5 |

**How conflicts are handled.** When two sources disagree, both rows are kept and flagged instead of picking one silently. In the financials, one row per organization-year is marked `preferred`, and 2.0% of org-years carry a `conflict_flag` (revenue differs by more than 1% between sources). The best-known conflict: the federal clearinghouse's FY23 record for Calvary repeats FY22's numbers. It is flagged, and the audit PDF ($937,999) is the better figure.

## 3. Where to be skeptical

**Matching names to organizations.** Grant filings name recipients in free text, and about 72% of grant rows carry a recipient EIN, either given in the filing or matched.
- **DC/MD/VA:** for named organizational recipients, 10.1% of grant dollars have no EIN. These are mostly government units, school sub-units and churches, which have no IRS listing.
- **Match quality:** each matched row records how it was matched (`match_method`). Most are exact; 25,091 rows were matched fuzzily (≥92% similar name in the same city, first word required to agree).

**Missing or thin data.**
- **Recent years are incomplete.** Many TY2024 returns are still being released, and most TY2025 returns aren't filed yet.
- **"See attached" grant lists.** 476 foundation returns ($3.2B) list grants only as "see attached", so the grants are real but the recipients are unknown. Some of Calvary's own funders file this way in some years: Philip L. Graham, Clark-Winchcole, Bank of America Charitable Foundation.
- **No FY24/FY25 audits** for Calvary are public.
- **DHS funding via TCP** is visible for one year only. TCP doesn't itemize provider payments in its filings.
- **Foundation bulk data for FY2016–18 is thin.** The IRS published no extract for those years.
- **Corporate giving** (not via a foundation) appears only where Calvary or a peer lists it.

**Assumptions** (listed in `open_questions.md`, part A):
- **CRM spreadsheet:** its total is treated as cumulative over an unconfirmed 2023–2026 window, and gifts are assumed to be cash unless the funder's own filings or web evidence say otherwise. `clean/supp_crm_cash_verification.csv` shows which CRM funders are confirmed by their filings: 25 in-window, 7 earlier-only.
- **Core peers:** the 18 were chosen by the build lead and are **provisional**. Review `reports/core_peers_proposal.md`.

**People matching.** Filings carry no person IDs. Two people are linked across organizations only on an exact normalized name plus a corroborating signal (same metro, overlapping years, matching middle initial or suffix).
- Of the 2,036 people linked across organizations, 597 are high confidence and 1,439 medium.
- 1,270 weaker pairs are held back for manual review in `clean/candidate_interlocks.csv`.
- Treat "shared board member" links as leads to confirm, not facts.

**Measurement traps.**
- **Government share depends on the line used.** The 990's "government grants" line misses government contracts booked as program revenue. Calvary FY21: $1.98M per the audit vs $503K on the 990 line.
- **Government award sources overlap.** Award lists, payments and audit expenditures can describe the same dollars, so never add `fact_gov_awards` rows across sources.
- **Cumulative rows.** CRM totals and "supporters over the years" lists are flagged `cumulative_flag=1`. Don't add them to annual grants.

**Privacy choices.**
- Individual donors appear only as counts per gift band.
- Names of individuals who received foundation grants (scholarships, aid) are redacted.
- Governance data is limited to what filings disclose about organizational roles.

## 4. Check it yourself (about 10 minutes, public sources)

Each check names a row you can find in `clean/` and the public document it came from. The `source_id` on each row leads to a URL in `sources/source_registry.csv`.

1. **Calvary's FY25 revenue.** In `clean/fact_org_financials.csv`, filter ein `521307706`, fiscal_year `2025`, preferred `1`; total_revenue should be **4,967,995**. Open ProPublica Nonprofit Explorer for EIN 52-1307706 (TY2024 990, Part I line 12). The same filing is in `inputs/` as the ProPublica PDF.
2. **A foundation grant.** In `clean/fact_grants.csv`, filter funder_ein `526036989` (Cafritz) and recipient_ein `521307706`; the tax_year 2024 row should be **$170,000**. Open the Cafritz Foundation (EIN 52-6036989) on ProPublica and check its TY2024 990-PF grants list.
3. **Federal pass-through.** In `clean/fact_gov_awards.csv`, filter source_type `audit_sefa`, fiscal_year `2023`; the four rows should sum to **$937,999** (SLFRF via OVSJG $440,677 is the largest). Open `inputs/Calvary-Womens-Services-Inc.-9.30.23-FS.pdf`, Schedule of Expenditures of Federal Awards (p. 28).
4. **A DC grant.** In `clean/fact_gov_awards.csv`, filter source_type `dc_ovsjg`, recipient_ein `521307706`, fiscal_year `2026`: New Foundations should be **$543,056** and Reach Up **$507,595**. The row's `source_id` points to OVSJG's FY2026 recipient list.
5. **Neighborhood need.** In `clean/dim_geo.csv`, geo_level `ward`, ward `8`: poverty_rate should be **0.306**. On data.census.gov, see ACS 5-year 2020–2024, table B17001, for "State Senate District 8 (2022), District of Columbia". DC wards are published as state senate districts.
6. **A named comparator.** In `clean/fact_org_financials.csv`, ein `311597223` (Downtown Women's Center), fiscal_year `2024`: total_revenue should be **34,403,997**. Check ProPublica for EIN 31-1597223.

If any of these fail, that is a real defect; please flag it.

## 5. Reproducibility

- **Scripts:** every clean table is produced by numbered scripts in `scripts/` from untouched source files in `raw/`. `./run_all.sh` rebuilds `clean/` from `raw/`; `./run_all.sh pull` re-downloads everything.
- **Records:** decisions, failures and row counts are logged in `logs/build_log.md`. Assumptions are listed in `open_questions.md`.
- **Rebuild test** (deleting `clean/` and regenerating it): **Passed. On 2026-10-10, `clean/` was deleted and regenerated with `./run_all.sh` four times (offline, about 20 min each). Two consecutive runs of the same code reproduced 24 of 25 tables with identical content (22 byte-for-byte). The 25th, `entity_aliases`, differed only in which spelling of a recipient name it displays; that choice now follows a fixed sort. The earlier runs found and fixed three order-dependence or normalization issues, each re-verified by shuffling the input and getting byte-identical output:
  - role titles chosen when a person is listed twice in one return
  - the representative spelling of a name in `entity_aliases`
  - an over-broad name-collapse rule**
