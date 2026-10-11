# Calvary Women's Services: funding data foundation

This is the data build for a pro bono funding strategy engagement with **Calvary Women's Services** (EIN 521307706; calvaryservices.org). Calvary is a Washington, DC nonprofit serving women experiencing homelessness, with programs in Wards 7 and 8.

This folder holds the collected, cleaned and documented data only. Analysis, interpretation and recommendations belong to the next step ("Prompt 2"). Observations made during the build are in `notes_for_analysis.md`, not in the tables.

## Start here (Prompt 2)

0. **`reports/reviewer_guide.md`:** how the data was checked, where to be skeptical, and a 10-minute self-check (for human reviewers).
1. **This README:** data model, conventions and caveats.
2. **`clean/data_dictionary.csv`:** every table and column, with type, definition and allowed values.
3. **`reports/data_inventory.md`:** what was collected, with counts.
4. **`reports/data_quality.md`:** reconciliation, coverage gaps, match rates and null rates.
5. **`notes_for_analysis.md`:** patterns and questions noticed during the build, grouped by area.
6. **`open_questions.md`:** the assumptions made (A1–A5 and others), plus items still open.

**Client requirement:** Calvary's CEO asked on 2026-10-10 that every analysis include two organizations, both in the `named_comparators` universe:
- **Downtown Women's Center (DWC)**, Los Angeles (EIN 311597223).
- **SheWorks**, a workforce program of the **California Black Women's Collective Empowerment Institute** (EIN 882046704; Carson, CA; founded 2022). SheWorks is a program, not a separate entity, so filing data describe the parent institute and program-level funders come from the web. Show it as a reference row in every peer table, benchmark and chart, including DC-only views.

All tables are UTF-8 CSV in `clean/`. Join keys: `ein` for organizations, `funder_id` for funders, `person_id` for people, `tax_year`/`fiscal_year` for time, and `county_fips`/`ward`/`tract_geoid` for geography.

## Folder map

```
README.md                  this file
notes_for_analysis.md      observations for the analysis (no verdicts)
open_questions.md          assumptions register + open items
requirements.txt           pinned Python packages
run_all.sh                 rebuild (see "Rebuild")
inputs/                    user-provided PDFs and the CRM export (read-only)
raw/                       untouched downloads and API responses (large; may stay behind)
interim/                   regenerable intermediates: staging tables, caches (not needed for analysis)
clean/                     final tables + data_dictionary.csv
config/                    universe rules, NTEE sets, peers, overrides, program-area vocabulary, table specs
sources/                   input_inventory.csv, api_catalog.md/.csv, source_registry.csv
scripts/                   numbered pipeline; scripts/lib/ shared helpers
reports/                   data_quality.md, data_inventory.md, universe_summary.md, core_peers_proposal.md
logs/build_log.md          what ran, row counts, failures, decisions
```

## Data model (`clean/`)

**Dimensions**

| Table | Grain | Notes |
|---|---|---|
| `dim_org` | one row per EIN | Every organization in a universe or referenced by a fact. Holds BMF attributes, NTEE label, org class, geography (county; DC ward/tract via MAR 2; MD/VA tract via the Census geocoder), website and mission from the latest e-filed return, and `universes`. |
| `dim_funder` | one row per `funder_id` | `funder_id` is the EIN when known, else `F` + a hash of the normalized name. Also holds `funder_type`, geography, `issue_focus_tags` and totals. |
| `dim_universe_membership` | universe × EIN × rule | Rules are in `config/universes.yaml` and `reports/universe_summary.md`. |
| `dim_period` | calendar year | CPI-U (US and DC metro), the deflator to 2024 dollars, and federal/DC/Calvary fiscal-year labels. |
| `dim_geo` | geography | Nation, state, DC MSA (CBSA 47900), counties, the 8 DC wards and 206 DC tracts, with ACS 2020–2024 context. |
| `dim_program_area` | tag | The vocabulary used in `program_area_tags`. |
| `dim_person` | person | Names only, as disclosed in filings. See "People". |
| `entity_aliases` | name variant | Every observed name variant → canonical EIN, with match method and score. |
| `ref_ntee_codes` | NTEE code | IRS labels. |

**Facts**

| Table | Grain | Main sources |
|---|---|---|
| `fact_org_financials` | org × fiscal year × source | E-filed 990/990-EZ/990-PF XML (TY2020+), NCCS e-file tables, IRS SOI extracts (2011+), ProPublica, Calvary's audits and 990 PDFs |
| `fact_grants` | grant or gift record | 990-PF grants paid and approved-future, Schedule I (DMV funders, DAF sponsors filtered to DC/MD/VA recipients, known Calvary funders), Calvary's CRM export, annual reports, support page, funder and peer web pages |
| `fact_gov_awards` | award / subaward / expenditure line | USAspending, Federal Audit Clearinghouse SEFA, Calvary audit SEFA, Treasury SLFRF, DC OVSJG, DC Council oversight responses, DC PASS, HUD CoC |
| `fact_opportunities` | open/forecast opportunity | Grants.gov |
| `fact_policy_events` | dated budget/policy change | DC budget books FY2024–FY2027, Council budget reports, Budget Support Act |
| `fact_roles` | person × org × filing year | 990 Part VII-A, 990-EZ, 990-PF officers, Calvary annual-report board lists |
| `fact_org_relationships` | org pair × type × year | grant, daf_sponsor_grant, pass_through_funding, schedule_r_related, shared_board_member |
| `candidate_interlocks` | person-record pair | Low-confidence cross-org name matches held back for manual review |

**Supplementary tables** (`clean/supp_*.csv`):
- `supp_calvary_program_metrics`
- `supp_calvary_strategic_targets`
- `supp_calvary_individual_donor_bands`: counts only, no names
- `supp_crm_cash_verification`
- `supp_homeless_counts`: HUD PIT/HIC by CoC
- `supp_hic_projects`: HIC beds by project and provider
- `supp_dc_budget_lines`

## Conventions

- **EIN**: 9-digit zero-padded string.
- **Years**:
  - `tax_year` = IRS tax year, the year the fiscal year begins.
  - `fiscal_year` = the year it ends.
  - `fye_month` = the month it ends.
  - Example: Calvary's FY ends Sept 30, so TY2024 = FY25 = Oct 2024–Sep 2025.
  - ProPublica's `tax_prd_yr` is the year the fiscal year ends.
  - Government amounts state their own calendar in `fiscal_year_basis`.
- **Money**: integer nominal USD. `*_real_2024` columns use the CPI-U US annual average with base 2024 (deflator by `fiscal_year`; see `dim_period`).
- **Provenance**: every row carries `source_id` (→ `sources/source_registry.csv`) and `retrieved_date`.
- **Quality**:
  - `confidence` is high / medium / low.
  - `basis` is `documented` (stated by the source), `derived` (computed) or `inferred` (judgment).
- **One fact per row**: the same figure from different sources is kept as separate rows.
  - `fact_org_financials.preferred = 1` marks one row per org-year. Ranking: XML > NCCS > ProPublica > SOI > 990 PDF > audit.
  - `conflict_flag = 1` marks org-years whose sources disagree on revenue by more than 1%.
  - Derived ratios are computed on preferred rows only.
- **`fact_grants.cumulative_flag = 1`**: the amount or mention spans several years. Examples: CRM totals, and support-page lists of supporters "over the years". Never add these to annual rows.
- **`notes` column**: source-specific extras as `key=value` pairs, e.g. `placeholder_row=1` for "see attached" 990-PF rows, and match details.
- **Ward**: digits `1`–`8`, joining `dim_org.ward` to `dim_geo.ward`.
- **Universe membership**: look it up in `clean/dim_universe_membership.csv` (or `dim_org.universes`). `config/` only holds the rules.
- **Comparing orgs by `tax_year`**: one tax year mixes fiscal years ending in different months. Calvary's ends in September, DWC's in December, SheWorks' parent's in June. Show `fiscal_year` + `fye_month` when timing matters.
- **Funder types** (`dim_funder.funder_type`):
  - private, corporate and community foundations, federated giving, and other grantmaking public charities are institutional decision-makers.
  - `daf_sponsor` rows (Fidelity, Schwab, Benevity, ...) are intermediaries for individual donors' advised funds. Analyze them separately from institutional funders.
  - `corporate` = companies giving directly, named only in Calvary's or peers' lists, with no public filing.

## Universes

| Universe | Size | Definition |
|---|---|---|
| `calvary` | 1 | The subject organization |
| `named_comparators` | 2 | Organizations Calvary leadership asked to see in every analysis (`config/named_comparators.csv`): Downtown Women's Center, LA (311597223, NTEE P83, ~$34M); California Black Women's Collective Empowerment Institute, runs SheWorks (882046704, ~$1.8M, no federal awards or single audit found) |
| `core_peers` | 18 | Provisional set in `config/core_peers.csv`, with tier and rationale. Alternates and evidence are in `reports/core_peers_proposal.md`. Edit the CSV and rerun to change it. |
| `dc_sector` | ~1,027 | DC public charities in core + adjacent NTEE codes (homelessness, housing, DV/victim services, human services, behavioral health, reentry, workforce, food, veterans, women's rights). Rule DCS2 flags orgs with no return since TY2020. |
| `dmv_sector` | ~4,910 | Same filters across DC/MD/VA counties in the DC MSA |
| `national_women` | ~2,880 | Nationwide DV shelters (P43), women's centers (P83), women-named homeless/housing orgs, and I71 DV orgs with housing terms |
| `size_matched` | ~566 | Nationwide shelter/DV/women's-center NTEE codes (L40/L41/P85/P43/P83), revenue 0.5×–2× Calvary's TY2022–24 median ($2.48M–$9.94M) |
| `dmv_funders` | ~7,705 | DC/MD/VA private foundations, grantmaking public charities (NTEE T-codes), and pins: TCP, Washington Area Women's Foundation, America's Charities |
| `daf_sponsors` | 15 | National DAF sponsors (Fidelity, Schwab, Vanguard, NPT, …), Schedule I filtered to DC/MD/VA recipients |
| `calvary_known_funders` | 88 | Funders named in Calvary's CRM, reports or support page, matched to EINs. KF2 = inferred corporate foundation (low confidence). |

## People (governance)

- **What's stored:** names, titles, role flags, hours and reported compensation, exactly as disclosed on filings, plus board lists printed in Calvary's own annual reports. Nothing else: no home addresses, contact details or outside enrichment.
- **Matching across organizations:** two records are treated as the same person only when the normalized names match exactly AND at least one corroborating signal holds: same metro, overlapping years, matching middle initial, or matching suffix. Common names need a name-based signal plus another signal. `dim_person.match_notes` gives the confidence.
- **Held-back matches:** low-confidence pairs are in `clean/candidate_interlocks.csv`.

## Caveats the analysis should know

1. **Government share.** 990 Part VIII line 1e understates government money when contracts are booked as program service revenue. Calvary FY21: audit government revenue $1.98M vs line 1e $503K. Use audits/SEFA/DC award data, or state the measure.
2. **CRM export** (`Foundation & Corporate Funders_2023-2026.xlsx`): GIFT_TOTAL is treated as cumulative, window unconfirmed (assumption A1), amounts unknown cash vs in-kind (A2). `supp_crm_cash_verification.csv` checks each funder against its own filings.
3. **Recent years are incomplete.** TY2024 returns are partly released; TY2025 is mostly unfiled. Audits: FY13–FY23 (FY24/FY25 not public).
4. **FAC record for "audit year 2023"** repeats FY22 amounts; Calvary's FY23 audit shows $937,999. Both are kept and flagged.
5. **Federal pass-through money** (SLFRF via OVSJG, CoC via TCP) is mostly invisible in USAspending. Use FAC, audits, Treasury SLFRF and the DC sources.
   - **Overlapping sources:** `fact_gov_awards` mixes award lists, obligations, payments and audited expenditures from overlapping sources (e.g., OVSJG awards vs PASS payments vs SEFA). Never sum across `source_type`; pick one source per question.
   - **DHS money via TCP** is public for one year only, and TCP's 990s don't itemize provider payments.
6. **990-PF "see attached" grant lists** (`placeholder_row=1`): 476 returns, $3.2B. These are real grants without grantee names, e.g. some years of Philip L. Graham Fund and Clark-Winchcole.
7. **Unmatched recipients.** Foreign recipients, public schools, churches and government units have no EIN. For named DC/MD/VA organizational recipients, 10.1% of grant dollars are unmatched. Individuals' names are redacted (`match_method = redacted_individual`). `confidence` on grant rows rates the documented grant record; recipient-match quality is in `match_method` and `match_score`.
8. **Core peers are provisional.** They were adopted while the engagement lead was away. Review `reports/core_peers_proposal.md`.

## Sensitivity and citation

- **Internal documents:** `inputs/Foundation & Corporate Funders_2023-2026.xlsx` (Calvary CRM export) and `inputs/2021-2024 Strategic Plan Final Report_internal (1).pdf`. Rows derived from them carry those `source_id`s.
- **Individual donors:** never stored by name; only counts per gift band, per Calvary's donor privacy policy.
- **Required citations:**
  - Cite ProPublica Nonprofit Explorer for `api_propublica` data.
  - Cite NCCS (ODC-BY) for `bulk_nccs_efile`.
  - GivingTuesday data-use terms apply to `bulk_gt_datalake`.
  - DC Open Data is CC BY 4.0.
  - IRS, Census, BLS, HUD, USAspending, FAC and Grants.gov data are public domain.
  - Web pages are cited by URL in the registry.
  - See `license_or_citation` in `sources/source_registry.csv`.

## Rebuild

```sh
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r requirements.txt
./run_all.sh            # rebuild clean/ from raw/ (parsing + modeling; ~15-20 min)
./run_all.sh pull       # full re-pull from the network (hours; needs keys)
```

- **Keys** (environment variables, never written to files): `TAVILY_API_KEY`, `FAC_API_KEY` (api.data.gov), `CENSUS_API_KEY`, `DC_MAR_API_KEY`. `run_all.sh` sources `~/.config/calvary/keys.env` if present.
- **Network in rebuild mode:** none. Pull-only scripts (34 FAC, 43/44 web pages, 47 address geocode) are skipped, and their staging files in `interim/` are reused.
- **Python:** 3.12. **External tools:** `pdftotext`/`pdfinfo` (poppler) for the PDF steps.
- **Script order:** numbered by phase.
  - `0x` inputs
  - `1x` recon
  - `2x` universes
  - `3x–4x` pulls
  - `5x` XML parsing
  - `6x` modeling
  - `7x` QC
  - `8x` docs
- **`raw/` size:** about 7.0 GB: XML 2.5 GB, NCCS 2.0 GB, SOI 0.85 GB, IRS index 0.44 GB, BMF 0.35 GB, web 0.3 GB, other ~0.6 GB. `interim/` is about 1.2 GB. Both may stay behind. `clean/`, `sources/`, `reports/`, `scripts/`, `config/` and the docs are self-sufficient for analysis.
- **Regenerating `raw/`:** run `./run_all.sh pull`. Without `raw/`, rebuild mode cannot run, but the analysis does not need it.

## Analysis outputs (Prompt 2)

The analysis built on this data lives in `../calvary_analysis/` (see its README): module scripts and readouts (M1–M10), chart data and charts, the insight register, the funding-pressure verdict, the scored funder pipeline (`recommendations/funder_pipeline.csv`, weights in `config/scoring_weights.yaml`), the 90-day plan, decks (leadership, consulting, appendices A–D, executive one-pager) and reports. Rerun instructions and the places to change peers, scenarios and weights are in `../calvary_analysis/README.md`. `../input_map.md` records where every input used by the analysis lives.
