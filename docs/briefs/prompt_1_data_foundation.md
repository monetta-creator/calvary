# Prompt 1 of 2: Data Foundation for the Calvary Women's Services Funding Survey

## Your role and scope

You are the data engineer on a pro bono strategy engagement for **Calvary Women's Services** (EIN 52-1307706, calvaryservices.org), a Washington, DC nonprofit serving women experiencing homelessness in Wards 7 and 8.

This prompt covers **data gathering, cleaning, and structuring only.** A second prompt will run the analysis later, in a different session on a different machine. Your deliverable is a clean, documented, portable dataset that a fresh Claude Code session can pick up and analyze without any other context.

Stay in your lane: collect, clean, join, dimension, and document. Save interpretations, verdicts, and recommendations for Prompt 2. When you notice something analytically interesting, write it in `notes_for_analysis.md` and keep building.

## Inputs

1. **User-provided sources** in `inputs/`. Inventory these first (Phase 1). They may include PDFs, web exports, spreadsheets, annual reports, and links.
2. **Tavily** for web search and page extraction.
3. **Public APIs and bulk data** listed in Phase 2.

## Guiding principles

- **Raw stays raw.** Save every API response and download untouched in `raw/`, with a timestamped filename. All transformation happens in scripts that read from `raw/` and write to `clean/`.
- **Everything is reproducible.** Every clean table is produced by a script in `scripts/`. Running the scripts in order rebuilds `clean/` from `raw/`.
- **Every row has provenance.** Each clean record carries `source_id` (pointing to `sources/source_registry.csv`) and `retrieved_date`.
- **EIN is the master key** for organizations and foundations. Normalize to 9 digits, zero-padded, no hyphen.
- **One fact per row.** Bind each figure to exactly one entity, one period, and one source. Keep conflicting values from different sources as separate rows and flag the conflict.
- **Unverified figures get flagged.** Use a `confidence` column (high / medium / low) and a `basis` column (`documented`, `derived`, `inferred`).
- **Parallelize.** Use subagents for independent pulls (e.g., one per API, one per peer cluster). Merge and dedupe centrally.
- **Log continuously** to `logs/build_log.md`: what ran, row counts, failures, and decisions.

## Phase 1: Inventory the provided sources

- List every file and link in `inputs/` in `sources/input_inventory.csv`: filename, type, apparent publisher, date, entities mentioned, data it contains, and which clean table(s) it should feed.
- Extract structured data from each (tables from PDFs, figures from annual reports, funder names from donor lists) into `raw/inputs_extracted/`.
- Flag inputs that are duplicates, outdated, or unreadable.

## Phase 2: API and data source reconnaissance

Before bulk pulling, probe each source with Calvary's EIN (or a relevant query) and document what it actually returns. Record findings in `sources/api_catalog.md` and `sources/api_catalog.csv` with: name, base URL, auth required, rate limit, key endpoints, fields of interest, years covered, coverage gaps, and a sample request that worked.

Probe at least these:

**Nonprofit financials and filings**
- **ProPublica Nonprofit Explorer API** — `https://projects.propublica.org/nonprofits/api/v2`. GET only, JSON, no key. Search endpoint (filter by state, NTEE, subsection) and organization endpoint by EIN. Search returns 25 per page. Cite ProPublica in any output that uses this data.
- **GivingTuesday 990 Data Infrastructure API** — `https://990-infrastructure.gtdata.org`. No key; rate limit of 300 requests per 5 minutes. Endpoints include `990basic120fields`, `bmf`, and `efilexml` (an index of e-filed XML files per EIN). Use the `efilexml` index to locate full XML filings per organization.
- **IRS Form 990 XML bulk downloads** — monthly ZIPs under `https://apps.irs.gov/pub/epostcard/990/xml/{YEAR}/`. Use only if the per-EIN route is insufficient; these files are large.
- **IRS Exempt Organizations Business Master File (EO BMF)** — CSV extracts by state. Use it to build the universe of organizations and private foundations in DC, MD, and VA with NTEE codes, subsection, foundation status, and ruling date.
- **IRS SOI Annual Extract of Tax-Exempt Organization Financial Data** — bulk financial fields for cross-checking.
- **Urban Institute NCCS data** — check for cleaned historical 990 files useful for longer time series.
- **Charity Navigator API** — check access terms; use if available without cost.

**Government funding**
- **USAspending.gov API** (`api.usaspending.gov`) — federal prime awards and subawards by recipient, location, and assistance listing (CFDA) number.
- **Federal Audit Clearinghouse API** (via api.data.gov; requires a free key) — single audit data showing federal expenditures by program for organizations above the audit threshold. This captures federal dollars that flow through DC government as pass-through, which USAspending often misses. Treat this source as high priority.
- **Grants.gov `search2` API** (`https://api.grants.gov/v1/api/search2`) — open and forecasted federal opportunities; no key required. Also probe `fetchOpportunity` for details.
- **HUD data** — Continuum of Care award data for the DC CoC, Point-in-Time and Housing Inventory Counts (HUD Exchange / HUD User).
- **DC government** — DC Open Data portal, DC budget books (current and prior three fiscal years), DC contract and grant award records, and DC Council budget oversight materials. Locate the line items for homeless services, permanent supportive housing, victim services (OVSJG), and behavioral health.

**Context data**
- **Census ACS API** — Ward and tract-level poverty, housing burden, and demographics for Calvary's service area and peer service areas.

If a source requires a key, note it in `open_questions.md`, read keys from environment variables, and continue with keyless sources. Never write keys into any file.

## Phase 3: Define the comparison universes

Build multiple organization sets, each stored as a list of EINs with inclusion criteria in `clean/dim_universe_membership.csv`:

| Universe | Definition (refine with the data) |
|---|---|
| `core_peers` | 10–20 DC-area organizations closest to Calvary: homeless women, DV survivors, recovery, Wards 7/8 |
| `dc_sector` | All DC public charities in homelessness, housing, DV, and related human services NTEE codes |
| `dmv_sector` | Same filters across the DC metro (DC, MD, VA counties) |
| `national_women` | Organizations nationwide focused on homeless women or DV housing |
| `size_matched` | Organizations nationwide in the same NTEE codes within a revenue band around Calvary's |
| `dmv_funders` | Private foundations (990-PF filers) and grantmaking public charities in DC, MD, and VA |

Use the BMF and ProPublica search to build these from NTEE codes and geography. Confirm the relevant NTEE codes from the IRS classification itself (homeless shelters, homeless centers, family violence shelters, and adjacent codes). Document every filter so the universes can be rebuilt.

## Phase 4: Bulk pulls

1. **Financial time series** for every organization in every universe: as many years of 990 data as available.
2. **Full XML filings** for `core_peers`, `dc_sector`, and Calvary, parsed for revenue lines, functional expenses, program descriptions, and Schedule I grants.
3. **Funder-to-grantee grants** from `dmv_funders`: parse 990-PF grants paid (Part XV) and Schedule I from grantmaking public charities. This is the single most valuable dataset for the project. It shows who funds whom, at what size, over time.
4. **Federal award history** for Calvary and all `core_peers` and `dc_sector` organizations from USAspending and the Federal Audit Clearinghouse.
5. **Open federal opportunities** from Grants.gov matching relevant assistance listings and keywords (homelessness, housing, domestic violence, victim services, women, substance use, workforce, reentry, veterans, aging).
6. **Web-sourced funder data** via Tavily: annual report donor lists, foundation grantee pages, press releases, and corporate giving pages for `core_peers`. Structure into grant-level rows wherever an amount or year is stated.

7. **Governance and people (board interlocks).** From the same XML filings, parse Form 990 Part VII Section A (officers, directors, trustees, key employees) for Calvary, `core_peers`, and `dc_sector`, and 990-PF Part VIII (foundation officers, directors, trustees) for `dmv_funders`. Capture name, title, role flags, hours, and filing year. The ProPublica API returns financial fields and PDF links; the structured people data lives in the XML.
8. **Organizational relationships.** Parse Schedule R (related organizations) for Calvary and `core_peers`. Parse Schedule I from grantmaking public charities, including community foundations, United Ways, and donor-advised fund sponsors, which report grants to named organizations above $5,000. DAF sponsor grants give an aggregate view of individual donors who give through those vehicles.

For XML parsing, evaluate existing tools (e.g., the IRSx library and the Nonprofit Open Data Collective concordance that maps XML paths across schema versions) before writing a parser from scratch. Schema versions change across years; handle them explicitly.

## Phase 5: Clean, resolve, and model

**Entity resolution**
- Match funder names from web sources and Schedule I/990-PF recipient fields to EINs. Recipient names in grant data are messy free text; use normalized names plus city/state, and record match method and score.
- Keep an `entity_aliases.csv` table mapping every observed name variant to a canonical entity.

**Standardization**
- Fiscal year vs. tax year: record both and the fiscal year end month.
- Dollar amounts as integers in nominal USD; add a CPI-adjusted column using a documented base year.
- Dates in ISO 8601.
- Geography: state, county FIPS, DC ward where derivable.

**Data model** (all CSV in `clean/`)

Dimensions:
- `dim_org` — every nonprofit: EIN, name, address, ward/county, NTEE, subsection, foundation status, ruling year, website.
- `dim_funder` — every funder: EIN (if any), name, type (private foundation, community foundation, corporate, government agency, individual/DAF, other), geography, issue focus tags.
- `dim_period` — fiscal years and calendar years.
- `dim_geo` — state, county, ward, tract with ACS context fields.
- `dim_program_area` — standardized tags (housing, DV, behavioral health, workforce, health, education, aging, veterans, reentry, maternal health, other).
- `dim_universe_membership` — EIN-to-universe mapping with criteria.

Facts:
- `fact_org_financials` — one row per org per fiscal year: total revenue, government grants, other contributions, program service revenue, special events net, investment income, total expenses, program/management/fundraising expenses, net assets, cash. Include derived ratios (government share of revenue, months of cash, revenue growth) labeled `derived`.
- `fact_grants` — one row per grant: funder, recipient, year, amount, purpose text, program area tag, source.
- `fact_gov_awards` — one row per federal or DC award or expenditure line: agency, program, assistance listing, recipient, prime vs. subaward vs. pass-through, period, amount.
- `fact_opportunities` — open or forecast opportunities: funder, title, eligibility, award range, deadline, program area tags, retrieved date.
- `fact_policy_events` — dated budget and policy changes affecting relevant funding streams, with source.
- `dim_person` — canonical people appearing in governance filings: person_id, normalized name, and match notes. Store only what the filings disclose about organizational roles: name, title, and the organizations served. Exclude home addresses, contact details, and any personal enrichment from outside sources.
- `fact_roles` — one row per person per organization per filing year: person_id, EIN, title, role type (board, officer, key employee, foundation trustee), hours, source.
- `fact_org_relationships` — one row per relationship between two organizations: type (grant, related org per Schedule R, shared board member, fiscal sponsorship, DAF sponsor grant), direction, year, amount where applicable, evidence, source.

**Person matching rules.** Names in filings carry no unique identifier, so matching across organizations creates false positives. Treat a person as the same individual across organizations only when the name matches exactly after normalization and at least one corroborating signal exists (same metro area, overlapping years, a middle initial or suffix match, or a public source confirming both roles). Record `match_confidence` and the signals used. Keep low-confidence matches in a separate `candidate_interlocks.csv` for manual review.

**Quality checks** — write results to `reports/data_quality.md`:
- Row counts per table and per source.
- Missing-value rates per column.
- Duplicate checks on keys.
- Reconciliation of Calvary's financials across ProPublica, GivingTuesday, and XML.
- Unmatched entity names and their share of grant dollars.
- Known coverage gaps (e.g., paper filers, 990-N filers, recent years not yet released).

## Phase 6: Documentation and handoff

- `README.md` — project purpose, folder map, how to rebuild, and where Prompt 2 should start.
- `clean/data_dictionary.csv` — every table and column: name, type, definition, allowed values, source(s).
- `sources/source_registry.csv` — every source: id, URL or file, publisher, retrieved date, license or citation requirement.
- `reports/data_inventory.md` — a plain-language summary of what was collected: entities per universe, years covered, grant rows, funders identified, and the dimensions available for slicing.
- `notes_for_analysis.md` — patterns you noticed, anomalies, and questions the analysis should explore.
- `open_questions.md` — anything needing my input (keys, ambiguous entities, sources behind paywalls).

## Folder structure

```
calvary_funding_data/
├── README.md
├── notes_for_analysis.md
├── open_questions.md
├── requirements.txt
├── inputs/                  # user-provided sources (read-only)
├── raw/                     # untouched API responses and downloads
├── clean/                   # final CSVs + data_dictionary.csv
├── sources/
│   ├── input_inventory.csv
│   ├── api_catalog.md
│   ├── api_catalog.csv
│   └── source_registry.csv
├── scripts/                 # numbered in run order: 01_..., 02_...
├── reports/
│   ├── data_quality.md
│   └── data_inventory.md
└── logs/
    └── build_log.md
```

## Portability

The `clean/`, `sources/`, `reports/`, `scripts/`, and documentation files will move to another machine. `raw/` may stay behind if it is large.
- UTF-8 CSV and Markdown only in everything that moves.
- Relative paths everywhere. No usernames, absolute paths, or environment details in outputs.
- Python scripts with a pinned `requirements.txt`; API keys from environment variables only.
- If `raw/` exceeds a few hundred MB, note its size and contents in the README so the next session knows what it is missing and how to regenerate it.

## Definition of done

- Every API in Phase 2 has been probed and cataloged.
- All six universes are built with documented criteria.
- All dimension and fact tables exist, are populated, and pass the quality checks (with failures documented).
- `fact_grants` contains the funder-to-grantee network for DMV foundations and core peers.
- `fact_roles` and `fact_org_relationships` capture governance links between Calvary, its peers, and regional funders, with every cross-organization person match carrying a confidence level.
- A fresh Claude Code session can read the README and data dictionary and begin analysis immediately.
