# Traceability check: 40 sampled numbers

Scope: deck text exports, `calvary_analysis/reports/full_findings.md`, `calvary_analysis/reports/executive_summary.md`. Chain tested per number: text -> chart id in footnote (or insight register) -> `calvary_analysis/chart_data/<id>_*.csv` (PNG ids via `calvary_analysis/config/png_data_map.csv`) -> CSV `source_tables` / `source_ids` -> `calvary_funding_data/sources/source_registry.csv` + `calvary_analysis/sources/source_registry_extension.csv` -> a row in the named clean table for the relevant entity carrying one of those ids. Detail per sample in `trace_sample.csv`.

Sampling rule applied: first numeric figure in body text, excluding headline and chart table; years and labels skipped. Four slides had no qualifying number and the next eligible slide was used (noted in `location`). For report numbers the chart id comes from the section's chart list or the insight register row.

## Result

| Status | Count | Samples |
|---|---|---|
| Complete | 36 | all others |
| Breaks at number_found_in_csv | 3 | T03, T12, T34 |
| Breaks at chart_id (no chart cited) | 1 | T32 |

Of the 36 complete chains, 24 numbers appear verbatim in the CSV and 12 are simple derivations (sum, ratio or min/max of CSV values); each derivation is written out in `number_found_in_csv`.

Registry step: all 118 source_ids used anywhere in `_manifest.csv` resolve to a registry row, and every row has a non-empty `url_or_file` and `publisher`. No duplicate ids across the two registries.

Clean-table step: confirmed for 39 of 40 (T32 is a direct row count). Calvary rows in `fact_org_financials` (61), `fact_gov_awards` (82), `fact_grants` (778), `supp_hic_projects` (25) and `fact_org_relationships` (235) carry the ids the charts list. One exact reconciliation: Calvary's filed, non-cumulative TY2020-24 grant rows in `fact_grants` sum to 4,433,659, the figure in `m1_07` and `m3_00`.

## Broken chains

- T03 (leadership slide 5, "TCP carries 74% of the base", chart m2_01): the cited CSV's 2024 rows give 77.7%. 74.2% reproduces from `m2_02` FY2025 aligned ceilings, which the slide does not cite. The number is defensible but the footnote points at the wrong chart.
- T12 (leadership slide 22, "six months of expenses, about $2.8M", charts m3_04, m2_06): neither cited CSV holds FY2025 expenses. The figure is `m1_04`/`m1_05` FY2025 total_expenses / 2. "Calvary holds 4.4 today" on the same slide is also from `m1_05`.
- T34 (full_findings M4 method, "1,027 dc_sector organizations", chart m4_01): the CSV has recipients per tax year (209-251). 1,027 is the dc_sector universe size in `dim_universe_membership`, a table the chart names but whose source_ids (bulk_irs_eo_bmf, bulk_irs_xml_index) are not in the chart's list. Consulting slide 32 shows the same figure (second number on that slide).
- T32 (appendix D slide 6, "entity_aliases has 231,647 parsed rows"): no chart id; the footnote points to a method note and `data_quality.md`. Verified directly: pandas row count of `clean/entity_aliases.csv` is 231,647. A documentary chain, not a chart chain.

## One content discrepancy inside a complete chain

- T23 (consulting slide 37, repeated in full_findings M5-01): "All 23 filed itemized lists in TY2023+". `m5_01` has `itemized_ty2023plus = False` for one of the 23 (a $5K, three-peer foundation). 22 of 23 is the supportable claim.

## Patterns

1. Source_ids are module-wide, not chart-specific. Every CSV repeats the same id string on every row, and the string equals the manifest entry. m1 charts list 20-21 ids including every audit PDF and input 990 (m1_06 events uses 990 line items only); every m2 chart lists all 10 government-award ids, including `m2_01b` whose own per-row `source_id` column shows just two in use. `m2_01` and `m2_01b` are the only CSVs with a row-level source_id column; that is the model the others lack. Per module, charts share 1-4 distinct id lists.
2. Source_ids omit the ids of some tables the chart names. `m2_02` and `m2_07` name `fact_org_financials` but list no 990 ids; `m3_00` names `dim_period` but not `api_bls_cpi`; `m4_01` and `m3_07` name `dim_universe_membership` but not its two ids; `m8_01` names `fact_policy_events` but none of the five `doc_dc_budget_*` ids; `m5_00` and `m7_00` name `supp_crm_cash_verification`, which has no source_id column at all (`m5_00` also omits the CRM input id). `dim_program_area` has no source_id column. A reader following table -> id from these charts cannot reach the registry for those tables.
3. Derived numbers are common (12 of 40) and all but T03 recompute cleanly. Headline-style text (ranges, shares, sums) relies on the reader recomputing from the CSV; none of the CSVs carries the rounded figure as shown.
4. Basis mixing is flagged in method notes but not always in the text: T26's "68 beds, 2.5% of DC TH beds" uses all project types for the count and TH only for the share; T37's $4.1M sums DC FY2024 and CoC competition year 2024.

## Recommended fixes (smallest first)

- Add `m2_02` to the leadership slide 5 footnote, or recompute the TCP share from `m2_01` (78%) and say which basis is used.
- Add `m1_05` to the leadership slide 22 footnote.
- Change "All 23" to "22 of 23" on consulting slide 37 and in full_findings M5-01, or document why the one exception counts as itemized.
- Give `m4_01` a universe-count column or cite `dim_universe_membership` with its ids where 1,027 is used.
- Trim each chart's source_ids to the ids actually used (or add a per-row source_id column as in `m2_01`), and add the ids for every named table; add a source_id column to `supp_crm_cash_verification` and `dim_program_area`.
