# Memory reconciliation (Prompt 2, CP1)

Compared on 2026-10-10: Claude Code memory for this project (5 memory files plus the index) against the project files. Until a ruling says otherwise, the project files are the working source of truth. No item is rated High, so no analysis is blocked.

**Agreements checked (no difference):** Calvary FY25 revenue $4,967,995; FY21 audit government revenue $1,981,161 vs 990 line 1e $503,222; GWCF the largest filed funder at $1,206,500 TY2020–24; 18 provisional core peers; two named comparators (DWC 311597223, CBWC Empowerment Institute 882046704, SheWorks a program of the latter); 88 known funders; `fact_org_relationships` 544,041 rows; `fact_gov_awards` 40,300; `fact_org_financials` 150,461; keys file present; `run_all.sh` sets `CALVARY_NO_NOTES=1` in rebuild mode; DAF Schedule I limited to DC/MD/VA recipients; `.venv` Python 3.12 / pandas 3.

| item | what_memory_says | what_the_files_show | likely_explanation | proposed_severity | proposed_resolution | ruling (2026-10-10) |
|---|---|---|---|---|---|---|
| "See attached" placeholder grants | 476 returns, $3.2B (`calvary-dataset-guide`); same figure in README, `reviewer_guide.md`, `notes_for_analysis.md` | `reports/data_quality.md` §7: 667 rows, $3,497,262,549. Recount from `fact_grants` (notes contain `placeholder_row=1`): 667 rows, 627 funder-tax-years, 180 funders | README/notes figure comes from an earlier build pass (990-PF only); the final tables include Schedule I placeholders | Medium (affects landscape totals, not Calvary figures) | Use the table-derived figure in analysis and say so; leave Prompt 1 docs unchanged | Approved: use $3.5B / 627 funder-years; Prompt 1 docs untouched |
| `fact_grants` size | "~930K rows" | 928,658 | Rounding | Low | None | Approved |
| `entity_aliases` row count | Not in memory; `data_quality.md` §1 lists the table twice: 231,647 and 231,678 | pandas parses 231,647 rows; the file has 231,678 physical lines because 31 quoted alias names contain line breaks | Two counting methods in the QC script | Low | Use 231,647 (parsed rows); count tables with pandas, never `wc -l` (`fact_gov_awards` shows the same effect: 42,958 lines, 40,300 rows) | Approved |
| Grant depth | "TY2020–TY2025" | `fact_grants` funder tax years 2012–2025 (pre-2020 from NCCS/SOI bulk extracts, thinner coverage; FY2016–18 990-PF extracts absent) | Memory describes the XML pull scope, not the table's full span | Low | TY2020–24 is the complete window; pre-2020 only for long trends with a coverage caveat | Approved |
| Funder naming | One GWCF at $1.21M | Two `funder_name_raw` spellings under EIN 237343119 ($748,500 + $458,000); same for Schwab (311640316 "Schwab Charitable Fund" / "Donor Advised Charitable Giving"), Vanguard, Gates, Schattner | Filer spelling varies by return | Low | Aggregate on `funder_id` / EIN, never on raw name | Approved |
| Machine | "The original brief said a different machine, but the user continued here" | Prompt 2 brief says the session *may* run on a different machine; `raw/` (7.0 GB) is present, so it is the same machine | Wording | Low | None | Approved |
| Core peers | "Provisional; picked while the user was away; never formally reviewed" | Same statement in README, `open_questions.md`, `core_peers_proposal.md` | Not a difference; a pending decision | — | Keep the 18 and label them provisional in every output; swap via `config/core_peers.csv` + rerun if wanted | Approved: keep the 18 as provisional |
| Named comparators in universes | DWC also in `national_women` via rule NW4 | `dim_org.universes` for 311597223 = `named_comparators;national_women`; 882046704 = `named_comparators` only | Consistent | — | None | Approved |

## Related rulings recorded at CP1

- Medium-confidence board interlocks: leadership materials use high-confidence matches only; consulting materials may show medium matches labeled "unconfirmed", alongside the low-confidence `candidate_interlocks`.
- A small web pull (Tavily) for Tier 1 target funders' guidelines and deadlines is approved for Phase 3, logged in `calvary_analysis/sources/`.
- Stress-test scenario levels: OVSJG −10% / −25%; HUD CoC −15% / loss of one project; DHS contract non-renewal; combined worst case.
- Analysis outputs live in `calvary_analysis/`; `input_map.md` and this file at the project root.
