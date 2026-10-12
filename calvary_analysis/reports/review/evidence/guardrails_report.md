# Guardrails scan: people data, portability, secrets, interlock placement

Scope: 138 text files under `calvary_analysis/` (.md .csv .yaml .yml .py .js .json .txt; excluding `decks/node_modules/`, `__pycache__`, `*.lock`, `reports/review/`) plus `input_map.md` and `README.md`, plus 7 decks in `calvary_analysis/decks/*.pptx` scanned two ways (markitdown text; raw XML under `ppt/` for `a:t` runs, `descr/name/title/alt` attributes, and raw 2000-char chunks). Scanner: `scan.py` in this folder (deterministic; all CSVs sorted by file, location, pattern).

Locations: text files use line numbers; decks use `slideN:md:<line>` for markitdown output and `ppt/slides/slideN.xml:pK|attrK|rawK` for XML.

## Check 1: personal names (names_hits.csv, names_summary.md)

Index: 65,268 name variants from 48,563 `dim_person` rows (name_display, name_norm, first+last), matched as 2+ token sequences. Classification (a) `org-name` when the matched text sits inside a `dim_funder.funder_name` / `dim_org` name on the same line (including `&`/`and` and truncated `...` cells); (b) `person` otherwise. A `note` column carries sub-signals for the `person` class.

| classification | hits |
|---|---|
| org-name | 568 |
| person | 154 |
| total | 722 |

`person` breakdown:

| note | hits | person_ids | assessment |
|---|---|---|---|
| placeholder token row in dim_person (not a person) | 120 | P2e2f5b0a16 | `dim_person` contains a row whose "name" is the two-word placeholder string that some foundations print in place of a grantee list; every hit is the analysis describing that placeholder. Not a person leak. Data-quality note for `dim_person`. |
| match spans punctuation | 24 | P2e2f5b0a16, Pb6f09c167b, P8affd2121a | tokens straddle `,` `'s` `&` etc. (e.g. end of one org name + start of the next). Not a person reference. Pb6f09c167b is itself a non-person row in `dim_person` (bank-name fragment). |
| parse-artifact row in dim_person | 1 | Pc733246cc9 | `dim_person` row whose last-name token is a stopword; the hit is ordinary prose in `reports/full_findings.md:201`. Not a person reference. |
| plain match | 8 | Pb2635a81aa | A 3-token foundation name printed as shorthand (without the word "Foundation") in a list of Calvary funders: `decks/build_consulting.js:214`, `decks/consulting_deck.pptx` slide 33, `modules/m4_funder_landscape.md:16`, `modules/m5_funder_gaps.md:16`, `reports/full_findings.md:201,240`. The foundation exists in `dim_funder` under `<NAME> FOUNDATION`; the mechanical rule did not see "Foundation" on the line. Effectively org-name. Not in leadership materials. |
| plain match | 1 | P653c8eaeaa | **Real person reference.** `sources/web_tier1_guidelines.csv:58`: a Tavily search snippet containing a foundation contact's honorific + full name and a street mailing address. Source-cache file, not a deliverable, but it is under `calvary_analysis/`. Recommend redacting the snippet or dropping the `snippet` column from the stored CSV. |

Leadership materials (`leadership_deck.pptx`, `executive_one_pager.pptx`, `reports/executive_one_pager.md`, `reports/executive_summary.md`, `reports/board_readout.md`): 13 hits, all `org-name` (founder-named foundations). No `person` hits.

`org-name` hits by volume: `chart_data/m4_00_funder_landscape_table.csv` (64), `m4_04_concentration.csv` (64), `m4_08_mission_tagged_funders.csv` (51), `m6_01_central_funders.csv` (35), `decks/appendix_C_funders_pipeline.pptx` (52 text + 95 XML), `sources/web_tier1_guidelines.csv` (26). All are foundation names (114 distinct person_ids map to founder-named funders).

## Check 2: paths and usernames (path_hits.csv)

Patterns: `/Users/`, `/home/`, `C:\`, `\Users\`, `$HOME`, `~/`, `file://`.

| classification | hits |
|---|---|
| hit | 0 |
| allowed-doc-reference | 2 |

The two allowed references are `~/.config/calvary/keys.env` in `calvary_analysis/analysis_plan.md:31` and `input_map.md:24`. No absolute paths, home directories or the username appear in any output, deck text or deck XML.

## Check 3: secrets (secrets_hits.csv)

Patterns: `tvly-`, `TAVILY_API_KEY`, `api_key`, `apikey`, `Bearer `, `secret`, `token=`, 32+ char key-like strings adjacent to "key", plus the literal values of the 4 variables in `~/.config/calvary/keys.env` (values compared in memory only; never written).

| pattern | hits | assessment |
|---|---|---|
| TAVILY_API_KEY / api_key | 13 | env-var name references only: `README.md:61`, `reports/methodology.md:630`, `scripts/11_web_tier1_guidelines.py:16,18,20` (`os.environ.get`), `decks/appendix_D_data_methods.pptx` slide 32. No values. |
| secret | 5 | the word "Secretary" in a federal opportunity title (`chart_data/m7_00_funder_pipeline.csv:54`, `recommendations/funder_pipeline.csv:54`, `appendix_C` slide 51). |
| token= | 1 | `requirements.txt:48` (`tiktoken==...`). |
| 32+char string near "key" | 1 | a URL slug in `sources/web_tier1_guidelines.csv:46`. |
| tvly- / apikey / Bearer | 0 | |
| keys.env value present | 0 | none of the 4 key values appear in any scanned file. |
| file named keys.env under calvary_analysis/ | 0 | |

No secret material found.

## Check 4: medium-confidence interlock placement (interlock_placement.csv)

`chart_data/m6_04_board_interlocks.csv`: 56 rows, 52 `medium` (label `unconfirmed (medium confidence)`, `use_in_leadership=False`), 4 `high`. The 48 distinct linked organizations (`other_name`) from medium rows were searched in the five leadership files, together with the words "medium confidence" and "unconfirmed".

15 rows found, none presenting a board link:

| file | location | organization | how it appears |
|---|---|---|---|
| decks/leadership_deck.pptx | slide 6 | United Way of the National Capital Area; Fidelity Investments Charitable Gift Fund | rows in a funder table with grant amounts |
| decks/leadership_deck.pptx | slides 13, 14, 17 (+XML) | Miriam's Kitchen | named as a peer (chart label, grant-share comparison, shared-funder count) |
| decks/leadership_deck.pptx | slide 16 (+XML) | America's Charities | "already in Calvary's records; the filing gap is lag" (funder context) |
| reports/executive_summary.md | 29, 32 | Miriam's Kitchen | peer comparison; "shares 17 institutional funders with ..." |
| reports/board_readout.md | 26 | Miriam's Kitchen | peer in funder-count sentence |
| reports/board_readout.md | 48 | keyword "unconfirmed" | "Public filings show one high-confidence overlap, not with a funder; the consulting team has a list of unconfirmed leads." No organizations named. |

`executive_one_pager.pptx` and `reports/executive_one_pager.md`: no occurrences. "medium confidence" does not appear in any leadership file. Placement rule holds.

## Summary of real findings

1. P653c8eaeaa: a named foundation contact with a street address in `calvary_analysis/sources/web_tier1_guidelines.csv:58` (scraped snippet). Redact or drop the snippet.
2. `dim_person` quality: rows P2e2f5b0a16, Pb6f09c167b, Pc733246cc9 are not people (placeholder string, bank-name fragment, parse artifact). Harmless for outputs; worth filtering upstream.
3. No path, username, secret or interlock-placement breaches.
