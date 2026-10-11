# Build conventions (all scripts and subagents follow these)

Project root is `calvary_funding_data/`. Run scripts from the root with `.venv/bin/python scripts/NN_name.py`.

## Subject
Calvary Women's Services Inc. EIN `521307706`, Washington DC, NTEE L41Z, 501(c)(3) public charity, fiscal year ends Sept 30.
- IRS `tax_year` = the year the fiscal year **begins**. TY2024 = Oct 2024–Sep 2025 = Calvary "FY25".
- `fiscal_year` = the year the fiscal year **ends**. Always store `tax_year`, `fiscal_year` and `fye_month`.

## Hard rules
1. **Raw stays raw.** Every API response and download is saved untouched via `lib.common.save_raw(source, desc, content, ext)`, which writes `raw/{source}/{YYYYMMDDTHHMMSS}_{desc}.{ext}`. Never edit raw files. All transformation reads raw and writes elsewhere.
2. **Reproducible.** Any pull or extraction you do must live in a numbered script in `scripts/` that can be rerun. Ad-hoc exploration is fine, but the final pull must be scripted.
3. **Provenance.** Register every source with `lib.common.register_source(source_id, name, url_or_file, publisher, license_or_citation, notes)`. Source ids are lowercase snake case with a prefix:
   - `api_` for live APIs (`api_propublica`, `api_gt_990basic`, `api_usaspending`)
   - `bulk_` for downloadable files (`bulk_irs_eo_bmf`, `bulk_irs_xml_index`)
   - `input_` for user PDFs (`input_fy23_audit`)
   - `web_` for web pages (`web_calvary_corp_found_support`)
   - `doc_` for government PDFs and budget books (`doc_dc_budget_fy26`)

   Every clean row carries `source_id` and `retrieved_date`.
4. **EIN** is a 9-digit zero-padded string with no hyphen. Use `lib.common.norm_ein`.
5. **Names**: keep the original, and add a normalized form via `lib.common.norm_name` when matching.
6. **Confidence and basis** on facts. `confidence` is high, medium or low. `basis` is `documented` (stated by the source), `derived` (computed from documented values) or `inferred` (judgment).
7. **Keys** come from the environment only, via `lib.common.env_key("NAME")`. Before running a script that needs keys, source the key file if it exists: `[ -f ~/.config/calvary/keys.env ] && set -a && . ~/.config/calvary/keys.env && set +a`. Never print, log or write key values. Never put a key in a sample request (write `api_key=$FAC_API_KEY`).
8. **Logging.** Call `lib.common.log(section, markdown_text)` after each meaningful step: what ran, row counts, failures and decisions.
9. **Portability.** UTF-8 CSV and Markdown. In anything under `clean/`, `sources/`, `reports/`, `scripts/` or the docs, use only project-relative paths (`lib.common.rel(path)`). No usernames, absolute paths or machine details.
10. **No interpretation.** Patterns, anomalies and questions go to `notes_for_analysis.md`, and items needing the user's input go to `open_questions.md`. Append ONLY via `lib.common.append_md(filename, heading, text)`, which is locked for parallel writers, never with Edit or Write. Keep both short.
11. **People data.** Only names, titles and roles as disclosed in filings or the org's own publications. No addresses, contact details or outside enrichment. **Individual donors**, from annual-report donor lists: do NOT store names. Store aggregate counts per gift band per year only, which is consistent with Calvary's donor privacy policy.
12. **HTTP**: use `lib.common.session()` (retry + UA) and `lib.common.RateLimiter`. Be polite: GivingTuesday allows 300 requests per 5 minutes; ProPublica has no stated limit, so stay at ≤2 req/s or less.

## Script number ranges (avoid collisions)
- `0x`: setup and input inventory/extraction
- `1x`: API recon probes
- `2x`: universes
- `3x`–`4x`: bulk pulls
- `5x`–`6x`: parse, clean, resolve
- `7x`: QC
- `8x`: docs

## API catalog parts
Each recon area writes `sources/catalog_parts/{area}.csv` and `sources/catalog_parts/{area}.md`. These are merged later into `sources/api_catalog.csv` and `.md`.

CSV columns, in this order:
`name,area,base_url,auth_required,auth_env_var,rate_limit,key_endpoints,fields_of_interest,years_covered,coverage_gaps,sample_request,sample_status,probe_date,feeds_tables,source_id,notes`
- `sample_status`: `ok`, `ok_no_results`, `blocked_needs_key`, `failed` or `not_applicable`.
- `feeds_tables` lists the target clean tables separated by `;`:
  - dimensions: dim_org, dim_funder, dim_geo, dim_period, dim_program_area, dim_universe_membership, dim_person
  - facts: fact_org_financials, fact_grants, fact_gov_awards, fact_opportunities, fact_policy_events, fact_roles, fact_org_relationships

The `.md` part gives a short section per source covering what it returns for Calvary, any gotchas, and a recommendation for the bulk phase. Keep it factual.

## Identity in requests
Never put the user's email, name or any personal identifier in request headers, URLs, payloads or files. Use `lib.common.USER_AGENT` only. If a server rejects a request without a contact email, mark it `failed` with that reason and use an alternative source; don't work around it.
