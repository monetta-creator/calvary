# Consulting team briefing

*How to pick this work up, what it concluded, what is fragile, and what to do next. Data as of 2026-10-10; revised 2026-10-11 after the review fix cycle (`reports/review/`). Paths are relative to `calvary_analysis/`; the data build is in `../calvary_funding_data/`.*

## 1. Orientation in ten minutes
1. `../input_map.md` and `../memory_reconciliation.md`: where every input lives and the eight documented differences between the build's memory and its files (none affecting a finding).
2. `analysis_plan.md`: the approved plan (CP1), modules M1–M10, data profile.
3. `insight_register.csv`: 36 findings with evidence summaries, chart IDs, confidence and status.
4. `recommendations/funding_pressure_verdict.md` and `strategic_recommendations.md`.
5. `storylines/leadership_headline_spine.md` (22 headline slides; the deck adds 4 dividers, 26 slides) and `consulting_headline_spine.md` (55): the arguments in headline form.
6. `discoveries_log.md`: the three flags (D1 ceilings vs recognized; D2 Sisters Rise/EHV; D3 event income, closed from the 990 itself) and how they were handled.
7. `reports/methodology.md`: method notes A1–D3, universes, measures, limitations.

## 2. What the analysis concluded
- **Verdict:** moderate-to-high pressure from channel concentration (three streams; TCP carries about three-quarters, 78% of the $4.1M 2024 award base, chart m2_01) and liquidity (FY25 −$607K; 4.4 months of cash), not from the government share (53%, 11th of 19 peers; 57th percentile among DC human-services organizations that report government revenue, top quarter against all filers with no line counted as 0%).
- **Private base:** flat at ~$1M/yr of filed grants from 26–29 funders; GWCF 27%; DAF share 25% vs 40–50% at peers; event receipts held near $0.53–0.60M (FY24 $596K, FY25 $533K); the FY25 990 presented gala receipts as fundraising-event income (line 8a, with $259K of direct costs netted) instead of contributions (line 1c).
- **Pools and politics:** OVSJG flat at $55M through FY2027 with cuts proposed and restored twice (the FY2027 restoration is $5.1M one-time plus $0.5M recurring, so the FY2028 base is in play again); DHS continuum rising; Calvary 1.1% of OVSJG, 5.3% of DC CoC. Federal: the FY2025 CoC NOFO was enjoined and FY2025 renewals were paid in full; the live question is the FY2026 CoC NOFO (awards expected about December 2026, litigation pending); HUD's 29 September 2026 notice ends EHV, so Sisters Rise's voucher base cannot be rebuilt.
- **Scenarios** (ranges across three splits of FY25 government revenue): OVSJG −10% $67K–$100K; DHS/TCP lost about $0.65M–$1.13M (13–23% of revenue); combined about $1.05M–$1.47M (21–30%) → 1.5–2.0 months of cash after a year (net). The DHS point estimate depends on the split (a floor case with OVSJG and CoC fully drawn nearly removes it); CoC and DHS together are $1.8–2.2M under every split, so the TCP channel is the cloud.
- **Opportunity:** $132M/yr from DMV funders to DC's sector (58% DAF); 23 funders of 3+ peers not funding Calvary (six are channels, Clark has closed and Venable is closed to new applicants, so 15 choose their own grantees; Clark's $32.8M spend-down inflates the 2020–24 landscape and gap totals); 11 lapsed ($0.16M); 15 with headroom among current funders that also fund two or more peers; closest neighbors Miriam's Kitchen, DASH, House of Ruth DC.
- **Pipeline:** 182 rows; 9 Tier 1 (five foundations, three government streams, MGAC); Clark closed and out; America's Charities a Tier 2 workplace-giving channel; weights, channel and status rules in `config/scoring_weights.yaml`, open status in `config/guideline_notes.csv`; sensitivity in `m7_05`.
- **Expansion:** near = workforce, behavioral health (credential), DV formalization; medium = FQHC partnership, older women; far = families.

## 3. What is fragile (handle with care)
- FY24–25 government share rests on 990 line 1e (matched audits exactly in FY22–23, but FY21 shows the line can understate).
- DHS/TCP contract values are public for FY2024 only; the FY25 baseline carries them forward. TCP is a pass-through intermediary with no itemized Schedule I list to fall back on, so TCP agreements are the only route to FY25–26 DHS values. Scenario losses are ranges because the split of recognized revenue across streams is not known (method note A4).
- TY2024 foundation filings are partial; "flat" private trends after TY2023 are partly filing lag.
- Core peers are provisional (`../calvary_funding_data/config/core_peers.csv`); the gap list and rank move with them; the sector percentiles do not. Swapping three provisional peers drops the three-peer funders (Cohen, Bernstein, The Washington Home and nine others, flagged "depends on the provisional peer set") and moves Calvary from 11th to 12th of 19.
- Board interlocks are name matches. There are no high-confidence board links in public filings: "high" now requires overlapping board tenures, and the one link once labelled high (Calvary and Clean Power Institute) spans terms that never overlap; Clean Power Institute has no filed grants, so it is not a funder. Medium links stay in consulting materials, labeled unconfirmed in `m6_04`.
- The web pull on funder guidelines (`sources/web_tier1_guidelines.csv`) returned usable first-party pages for about half of the Tier 1–2 funders; `config/guideline_notes.csv` labels each as first-party, third-party or analyst note, and its `open_status` column records whether each funder is open, invitation-only, closed or a channel, checked on the funder's own page with a date. Leadership materials name a funder only after that check.
- The CRM export is cumulative over an unconfirmed window and only 44% is verifiable in filings.

## 4. How to rerun or change things
- Environment: `../calvary_funding_data/.venv` plus `requirements.txt` here (matplotlib, networkx, python-pptx, markitdown, pyyaml). Decks: `decks/package.json` (pptxgenjs); LibreOffice for rendering.
- Modules: `scripts/01_m1_trajectory.py` … `10_m10_profiles.py`, then `12_merge_guidelines.py` and `13_m7_sensitivity.py`; `scripts/lib/trace.py` checks chart → CSV → registry; `scripts/lib/headline_check.py deck.pptx spine.md` checks titles (`--appendix=A..D` for appendix decks).
- Change the peers: edit `core_peers.csv`, rerun `../calvary_funding_data/scripts/20_build_universes.py`, then M3, M5, M6, M7.
- Change scenario levels: `config/scenarios.yaml` → rerun M2.
- Change scoring weights or tiers: `config/scoring_weights.yaml` → rerun 07, 12, 13.
- Change landscape exclusions or expansion distances: `config/landscape_exclusions.csv`, `config/expansion_areas.yaml`. Mis-attributed grant rows go in `config/grant_exclusions.csv` (dropped on every load of `fact_grants`; today two Baltimore funders' grants to a Baltimore namesake of My Sister's Place, $131,906).
- Change a funder's open status: `config/guideline_notes.csv` `open_status` → rerun 07, 12, 13.
- Decks: `cd decks && NODE_PATH=$PWD/node_modules PPTX_SKILL_APPLY_THEME=<pptx skill>/scripts/apply_theme.js node build_leadership.js` (and `build_consulting.js`, `build_appendix_*.js`, `build_onepager.js`); validate with the pptx skill's `validate.py`; render with `soffice --headless --convert-to pdf` and `pdftoppm`.

## 5. Open items for the team
1. Ask Calvary for the FY24/FY25 audits and the TCP subgrant agreements (FY2023–FY2026); reconcile CoC draw-down first (the audited FY22–23 years already show the gap there), then DHS; confirm the FY26 gala date as a small check. Update M1, M2 and the verdict when the documents arrive.
2. Confirm the provisional peer set with Calvary's leadership.
3. Abell, Schattner and Cohen (invitation-only), Clark (closed), Venable and Meyer (closed to new applicants), Many Hands and Weinberg (not eligible) and Jane Bancroft Robinson (grants by RFP) are checked; Bunting and Bechtel have no public process (Tier 3). Verify the rows still marked `unverified` in `config/guideline_notes.csv` (AAMC and others) on the funder's own page before outreach.
4. Walk the CRM for gifts routed through DAFs before contacting lapsed funders.
5. Keep the discoveries log current; new flags go there with evidence and a proposed action.
6. The independent review and its fix spec are in `reports/review/`; after re-verification, mark register rows `verified` and record fixes there.

## 6. Tone and sourcing rules
- Lead with what Calvary has built; state risks plainly as clouds on the horizon with a path; offer options, not prescriptions; avoid "exposed", "dependent" and "failure" as labels (design_system.md §6).
- Every data slide: source (publisher + clean table), method clause, trace line with chart ID and method note (design_system.md §4, sourcing rule).
- No personal names in any output; organization names only; relative paths only.
