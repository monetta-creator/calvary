# Entity matching and board-interlock review

Scope: fact_grants rows whose recipient is Calvary (521307706) or one of the 18 core peers (config/core_peers.csv), TY2020-2024, cumulative_flag != 1. That is 2,078 rows from 331 funder_ids (3,578 rows before the year/cumulative filter; 445 of those are cumulative). Interlocks: all shared_board_member rows in fact_org_relationships touching Calvary (8 rows, 7 person_ids). No personal names appear in this report or the CSVs; people are person_ids, and "c/o <trustee>" suffixes inside raw funder strings were redacted in the output files.

Files (this directory):
- entity_spellings.csv - A1 forward test: 25 funder_ids with the most distinct raw spellings, canonical name, spellings, verdict.
- entity_spellings_reverse.csv - A1 reverse test (empty: no normalized raw name maps to more than one funder_id).
- entity_sample40.csv - A2 deterministic sample (sorted by funder_id, recipient_ein, tax_year, amount, grant_id; every 51st row, k = 2078 // 40), with verdict.
- entity_state_mismatch.csv - extra test: rows where the recipient state printed in the source differs from dim_org (7 rows).
- entity_weak_matches.csv - extra test: all 18 restricted rows resolved by exact_name_state or fuzzy_name_city rather than EIN.
- entity_named_funders.csv - A3: every funder_id whose canonical or raw name carries the key token, with dollars to Calvary and peers.
- aliases_tier1.csv - A4: entity_aliases rows for the seven Tier 1 EINs, with a flag column.
- interlocks_calvary.csv - B1/B2: the 8 Calvary interlock rows joined to fact_roles spans, dim_person match notes, m6_04 flags, and a verdict.

## Part A - funder-to-grant matches

### A1 spelling variation (entity_spellings.csv, entity_spellings_reverse.csv)
Spelling variation is small: the maximum is 4 raw spellings for one funder_id (521691418, England Family Foundation, whose raw string itself says "FKA ..."); 24 of the top 25 have 2-3. Every set of spellings in the top 25 belongs to one filer. Three are renames rather than typos, all under one EIN and all consistent with the filing years: 471086460 (Wilczynski Foundation Inc in TY2021-22, Keehn Family Foundation in TY2023-25; BMF name is Wilczynski), 844185836 (LiveGiveRun -> Charm City Run Foundation), 562305290 (Ludwig Family Foundation -> Carol and Gene Ludwig Family Foundation). 311640316 is Schwab Charitable under its BMF legal name "Donor Advised Charitable Giving" (config override). No case of two different Clark, Abell, Casey or regional community foundations folded into one id.

Reverse test: after normalizing raw names (case, punctuation, Inc/Foundation/Fund/Trust tokens), no normalized name maps to more than one funder_id inside the restricted rows. No evident funder is split across ids in this slice.

### A2 sample of 40 (entity_sample40.csv)
38 plausible, 2 doubtful, 0 wrong. Match methods in the restricted rows: exact_ein 1,290 (990-PF rows; the EIN is supplied by the GT datalake's own recipient resolution, since a 990-PF grant table has no EIN field), given 770 (Schedule I rows, EIN written by the filer), exact_name_state 11, fuzzy_name_city 7. All sampled funder names agree with dim_funder (differences are Inc, ampersand, "The", or BMF legal-name forms).

The two doubtful rows are both for peer 521263256 (My Sister's Place Inc, Washington DC): Reval Foundation Inc (203560525, Riderwood MD) -> "MY SISTER'S PLACE", Baltimore MD; and Whiteford Taylor & Preston Charitable Trust (526908570, Baltimore) -> "MY SISTER'S PLACE", Baltimore MD. Baltimore has a "My Sister's Place Women's Center" run by Catholic Charities of Baltimore; a Baltimore-county foundation giving $25,000 a year to a Baltimore address is far more likely funding that program than the DC shelter. entity_state_mismatch.csv shows this is the whole pattern: 6 of the 7 state-mismatch rows are these two funders (5 x $25,000 TY2020-24 from Reval, $6,906 TY2021 from Whiteford; $131,906 total, 2 of My Sister's Place's funder count). The seventh is Pew Charitable Trusts -> Miriam's Kitchen with an Arlington VA address ($6,151, Schedule I, EIN given by the filer): plausible, likely an address error in the filing. None of the mismatches touch Calvary.

The 18 weaker-method rows (entity_weak_matches.csv) are all misspellings of the recipient's own name or city (e.g. "Washingtion", "Calvary Womens's Services", "Doorways for Women and Familes"; a House of Ruth row printed with a Silver Spring city) and are all plausible. The two Calvary rows among them (Harry and Zoe Poole Foundation, $2,500 in TY2020 and TY2021, fuzzy_name_city 97.9) are correct.

### A3 named funders (entity_named_funders.csv)
Dollars are TY2020-24, non-cumulative, Calvary vs the 18 peers.
- Clark: Clark Charitable Foundation Inc (521512330, DBA A James & Alice B Clark Foundation) is one id with one raw spelling; $0 to Calvary, $8,330,500 to 5 peers. Thirteen other "Clark" ids exist (Clark-Winchcole, Clark Construction Group Charitable Foundation, Clark Foundation DC 872699920, several VA family foundations) and none is merged into it. One matters for the pipeline wording: Clark-Winchcole Foundation (526058340, Bethesda) is in Calvary's CRM as a current funder ($480,000 cumulative over 3 gifts, 2023-26 window) and on N Street Village's FY25 donor list. The decks' "Clark Charitable ... no Calvary grant yet" is correct for 521512330, but a reader could conflate the two Clark foundations; the consulting deck already names Clark-Winchcole separately (a "see attached" filer). Nothing merged or split wrongly.
- Abell: William S Abell Foundation Inc (521435573, 2 spellings) is $295,000 to Calvary and $860,000 to 8 peers; The Abell Foundation Inc (526036106, Baltimore) is a separate id with $5,000 to one peer. Correctly kept apart. (Three regex hits - Zanvyl and Isabelle Krieger Fund, Cabell Foundation, Parabellum Foundation - are substring artifacts of my search and are marked as such.)
- Greater Washington Community Foundation (237343119): one id; $1,206,500 to Calvary, $5,659,049 to 17 peers. The Health Equity Fund attributions come from config/funder_match_overrides.csv (two rows, "inferred" and "yes") and produce for Calvary: a CRM row "Health Equity Fund" $801,000 cumulative (3 gifts) and two web mentions (2022 inaugural round, 2024 round, no amounts). The attribution is a documented inference, not a filing; the GWCF Schedule I rows under the same id are filed. Capitol Hill, Arlington, Baltimore, Frederick County, Anne Arundel and Northern Virginia community foundations all keep their own ids.
- Robert I Schattner Foundation (521800778): one id, two spellings ("Robert I Schattner Foundation" and "... Inc aka Schattner Foundation"); $0 to Calvary, $800,000 to 4 peers.
- Casey: Eugene B Casey Foundation (526220316) $775,000 to 2 peers; Annie E Casey Foundation (521951681) $12,000 to 2 peers; separate ids, neither funds Calvary in filings.
- The Washington Home (530196647): one id, case variants only; $0 to Calvary, $1,147,050 to 3 peers.

### A4 entity_aliases (aliases_tier1.csv)
Columns: alias_name_raw, alias_name_norm, alias_city, alias_state, entity_kind (org | funder), canonical_id, canonical_name, match_method (exact_ein, manual, manual_reject, known_funder, exact_name_city, exact_name_state, exact_name_national, fuzzy_name_city, unmatched), match_score, n_occurrences, source_ids. Table-wide method counts: unmatched 93,590; exact_ein 59,296; exact_name_city 55,654; exact_name_state 13,415; fuzzy_name_city 9,017; exact_name_national 520; known_funder 106; manual 36; manual_reject 13.

For the seven Tier 1 EINs there are 31 alias rows. Funder-side aliases are all the same organization (exact_ein 100 or known_funder 95 for the CRM spellings; the two Health Equity Fund aliases are the manual override). Six org-side aliases deserve a look but are not wrong matches: under GWCF's EIN, "Food Justice DMV" (4 occurrences; a fiscally sponsored program whose grants were filed with GWCF's EIN) and one "Greater Washington Community Foundation, Baltimore MD" address oddity; under America's Charities' EIN, "Giving Block Fee", "Helios Technologies Employee Assistance Fund (EAF)" and "SiteOne Cares" (funds and a fee line that filers recorded with America's Charities' EIN). These are the filers' EINs, so they attach correctly, but they mean "grants to America's Charities / GWCF" in the data includes pass-through and sponsored-program money. No alias points to a different organization.

## Part B - board interlocks

### How the pipeline derives the labels (06_m6_network.py)
- Rows come straight from fact_org_relationships where rel_type == shared_board_member; the script does not recompute anything. `confidence` is the person-match confidence copied from dim_person (match_notes), and `evidence` is the two role-year spans. Every one of the 56 Calvary+peer rows has basis = inferred; the signals in `notes` are: overlap_years+same_metro 39, overlap_years 7, same_metro 6, middle_initial+overlap_years+same_metro 3, middle_initial+same_metro 1.
- From those rows, "high" appears only when the middle_initial signal is present (4 rows), so the label measures how distinctive the printed name is, not whether the two tenures overlap. A row can be "high" with no year overlap (the Calvary case) and "medium" with four overlapping years.
- `other_is_funder` = the other EIN is in the dmv_funders, daf_sponsors or calvary_known_funders universe, or in m5_00_candidate_funders. It does not check for a grant. Clean Power Institute is in dmv_funders because its NTEE is T30 (public foundation); dim_funder shows n_grants = 0 and fact_grants has zero rows with it as funder to anyone, including Calvary.
- `use_in_leadership` = confidence == "high"; label text is "high confidence" vs "unconfirmed (medium confidence)". The leadership deck honours this: its network slide says "Board overlaps are thin in public filings. One high-confidence link, not a funder" and names none of the medium-row organizations in an interlock context (United Way NCA and Miriam's Kitchen appear in the deck only as a funder and as a peer). The consulting deck (line 877) and appendix C (line 604) print the Clean Power Institute row with funder = "yes" while the leadership deck says "not a funder" and insight M6-03 says "none with a funder": the materials contradict each other because the flag means "in the funder universe" and the prose means "has given to Calvary".

### B1 the high-confidence link (L212084949644, Clean Power Institute, 872722157)
- One person_id (Pc980c65d8b) carries roles at both organizations: Calvary Vice President (officer+director, 1 hr/wk) TY2019-2020, Director TY2021, and listed in the FY20 annual report; Clean Power Institute "President as of 09/2023" TY2023 and President TY2024 (0.25 hr/wk, no pay). dim_person: n_orgs 2, n_filings 6, match_notes "exact normalized name + signals middle_initial+same_metro; match_confidence=high".
- Spans do not overlap (2019-2021 vs 2023-2024), as the deck states. The linking evidence is the full name including middle initial printed identically in both filings plus both organizations being in DC. Two other dim_person rows share the same first+last name (different or missing middle initial), so the name is not unique in the DMV filings; the middle initial is doing all the work.
- Clean Power Institute: DC, ruled 2022, NTEE T30, BMF revenue $3.3M, universes = dmv_funders only; no fact_grants rows as funder; no money relationship with Calvary of any kind in the data.
- Verdict: the person link is plausible but the "high" label is overstated relative to the other three high rows in m6_04 (all of which have overlapping years as well as a middle initial). As a relationship path it is worth nothing for fundraising: a former Calvary board officer now runs a two-year-old research entity that has made no grants. Recommend relabelling it medium/unconfirmed (or stating "high name match, no tenure overlap, not a grantmaker") and fixing the funder flag so the three documents agree.

### B2 the seven medium rows (six person_ids)
- Le4ba36d544d0 Washington Area Women's Foundation and Lacad655a6d68 United Way NCA share person_id P202672d156 (n_orgs 3): Calvary director TY2020-24 (two annual reports too), WAWF board TY2022-24, UWNCA board TY2020-21. Years overlap at both; signals overlap_years+same_metro; no middle initial printed. Medium is fair, and this is the best-evidenced Calvary link: UWNCA is a filed Calvary funder ($89,549 TY2020-24, 6 rows). If any link belongs in leadership material it is this one, labelled unconfirmed.
- L080061a017dc United Way of Central Maryland (Pfb8439767f): Calvary director from Sept 2023 (TY2022-24) and UWCM AVP/VP operations (staff, Baltimore) TY2022-24. Overlap yes; signal overlap_years only (different metro); one other dim_person row shares the first+last name. Medium is fair.
- Lfd85a4e4b3e1 Miriam's Kitchen (Pb89bf8db81): Calvary COO (staff) TY2020-24 and a Miriam's Kitchen board seat that ended Nov 2020. Overlap 2020; medium fair. It is a staff-to-peer-board link, not board-to-board.
- L19dd50afadb3 Charter School Incubator Initiative (P0525ea6da5): Calvary director TY2019-21, CSII board TY2020. Overlap 2020; medium fair; CSII has no grants to Calvary.
- L51aa0cf7bb34 Dress for Success Washington DC (P05badec278): Calvary director TY2015-18, DFS secretary TY2021-22. No overlap; only signal same_metro. Medium is generous; treat as low.
- Lda3a0bfd74c7 Davis Construction Foundation (P1d57f4c0e4): Calvary director TY2017-19, foundation secretary/director TY2021-25. No overlap; only signal same_metro. Medium is generous; treat as low. Davis Construction Foundation is in calvary_known_funders (3 cumulative CRM rows to Calvary, no filed grant TY2020-24), so it is worth a confirmation call, but the data alone do not support it.
- Note the counts: M6-03 says "7 medium-confidence links"; that is 7 rows but 6 people and 7 organizations.

### B3 candidate_interlocks
1,270 rows (name-only candidates, all match_confidence low, person_id_a != person_id_b). Zero rows involve Calvary. One row involves a core peer (no corroborating signals). The M6 insight "candidate_interlocks has no Calvary rows" is correct.

### B4 summary of label fidelity
- Clean Power Institute "high": label overstated (name-distinctiveness only, no tenure overlap, no grants, entity ruled 2022); the leadership deck's "not a funder" is right and m6_04's funder flag is misleading.
- WAWF, UWNCA, UWCM, Miriam's Kitchen, CSII "medium": fair.
- Dress for Success, Davis Construction Foundation "medium": generous; evidence is an exact common-format name in the same metro with non-overlapping tenures.
- The leadership deck's high-only restriction is implemented and no medium organization is named there as an interlock.

## Suggested fixes (for the pipeline owner, not applied)
1. In the shared_board_member confidence, require overlap_years for "high", or add a separate tenure_overlap flag to m6_04 and the appendix tables.
2. Rename or redefine other_is_funder as "in funder universe" and add "has_filed_grant_to_subject" so the leadership deck, consulting deck and appendix C agree.
3. Add a recipient-state check to the recipient match: the Reval and Whiteford rows to My Sister's Place (Baltimore address) should be rejected or flagged; $131,906 and 2 funders move off that peer's totals.
4. Where decks name "Clark", say "Clark Charitable Foundation (A. James & Alice B. Clark Foundation), distinct from Clark-Winchcole, which already gives to Calvary".
