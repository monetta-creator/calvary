# Consulting team briefing

*How to pick this work up, what it concluded, what is fragile, and what to do next. Data as of 2026-10-10. Paths are relative to `calvary_analysis/`; the data build is in `../calvary_funding_data/`.*

## 1. Orientation in ten minutes
1. `../input_map.md` and `../memory_reconciliation.md`: where every input lives and the eight documented differences between the build's memory and its files (none affecting a finding).
2. `analysis_plan.md`: the approved plan (CP1), modules M1–M10, data profile.
3. `insight_register.csv`: 36 findings with evidence summaries, chart IDs, confidence and status.
4. `recommendations/funding_pressure_verdict.md` and `strategic_recommendations.md`.
5. `storylines/leadership_headline_spine.md` (22 slides) and `consulting_headline_spine.md` (55): the arguments in headline form.
6. `discoveries_log.md`: the three flags (D1 ceilings vs recognized; D2 Sisters Rise/EHV; D3 event income) and how they were handled.
7. `reports/methodology.md`: method notes A1–D3, universes, measures, limitations.

## 2. What the analysis concluded
- **Verdict:** moderate-to-high pressure from channel concentration (three streams; TCP carries 74% of a $4.1M award base) and liquidity (FY25 −$607K; 4.4 months of cash), not from the government share (53%, 11th of 19 peers, sector median).
- **Private base:** flat at ~$1M/yr of filed grants from 26–29 funders; GWCF 27%; DAF share 25% vs 40–50% at peers; event line −$483K in FY25.
- **Pools and politics:** OVSJG flat at $55M through FY2027 with cuts proposed and restored twice; DHS continuum rising; Calvary 1.1% of OVSJG, 5.3% of DC CoC.
- **Scenarios:** OVSJG −10% $67K; DHS/TCP lost $960K; combined $1.31M → 1.7 months of cash after a year (net).
- **Opportunity:** $132M/yr from DMV funders to DC's sector (58% DAF); 23 funders of 3+ peers not funding Calvary; 12 lapsed; 15 with headroom; closest neighbors Miriam's Kitchen, DASH, House of Ruth DC.
- **Pipeline:** 182 rows; 11 Tier 1; weights in `config/scoring_weights.yaml`; sensitivity in `m7_05`.
- **Expansion:** near = workforce, behavioral health (credential), DV formalization; medium = FQHC partnership, older women; far = families.

## 3. What is fragile (handle with care)
- FY24–25 government share rests on 990 line 1e (matched audits exactly in FY22–23, but FY21 shows the line can understate).
- DHS/TCP contract values are public for FY2024 only; the FY25 baseline carries them forward.
- TY2024 foundation filings are partial; "flat" private trends after TY2023 are partly filing lag.
- Core peers are provisional (`../calvary_funding_data/config/core_peers.csv`); the gap list and rank move with them; the sector percentiles do not.
- Board interlocks are name matches; only high-confidence links appear in leadership materials; medium links are labeled unconfirmed in `m6_04`.
- The web pull on funder guidelines (`sources/web_tier1_guidelines.csv`) returned usable first-party pages for about half of the Tier 1–2 funders; `config/guideline_notes.csv` labels each as first-party, third-party or analyst note.
- The CRM export is cumulative over an unconfirmed window and only 44% is verifiable in filings.

## 4. How to rerun or change things
- Environment: `../calvary_funding_data/.venv` plus `requirements.txt` here (matplotlib, networkx, python-pptx, markitdown, pyyaml). Decks: `decks/package.json` (pptxgenjs); LibreOffice for rendering.
- Modules: `scripts/01_m1_trajectory.py` … `10_m10_profiles.py`, then `12_merge_guidelines.py` and `13_m7_sensitivity.py`; `scripts/lib/trace.py` checks chart → CSV → registry; `scripts/lib/headline_check.py deck.pptx spine.md` checks titles.
- Change the peers: edit `core_peers.csv`, rerun `../calvary_funding_data/scripts/20_build_universes.py`, then M3, M5, M6, M7.
- Change scenario levels: `config/scenarios.yaml` → rerun M2.
- Change scoring weights or tiers: `config/scoring_weights.yaml` → rerun 07, 12, 13.
- Change landscape exclusions or expansion distances: `config/landscape_exclusions.csv`, `config/expansion_areas.yaml`.
- Decks: `cd decks && NODE_PATH=$PWD/node_modules PPTX_SKILL_APPLY_THEME=<pptx skill>/scripts/apply_theme.js node build_leadership.js` (and `build_consulting.js`, `build_appendix_*.js`, `build_onepager.js`); validate with the pptx skill's `validate.py`; render with `soffice --headless --convert-to pdf` and `pdftoppm`.

## 5. Open items for the team
1. Ask Calvary for the FY24/FY25 audits, the TCP subgrant agreements (FY2023–FY2026) and the FY25 gala calendar; update M1, M2 and the verdict when they arrive.
2. Confirm the provisional peer set with Calvary's leadership.
3. Verify the "no usable hit" guideline rows (Abell, Clark, Schattner, Jane Bancroft Robinson, AAMC) directly before outreach.
4. Walk the CRM for gifts routed through DAFs before contacting lapsed funders.
5. Keep the discoveries log current; new flags go there with evidence and a proposed action.
6. After the independent review (Phase 6), mark register rows `verified` and record fixes in `reports/review_report.md`.

## 6. Tone and sourcing rules
- Lead with what Calvary has built; state risks plainly as clouds on the horizon with a path; offer options, not prescriptions; avoid "exposed", "dependent" and "failure" as labels (design_system.md §6).
- Every data slide: source (publisher + clean table), method clause, trace line with chart ID and method note (design_system.md §4, sourcing rule).
- No personal names in any output; organization names only; relative paths only.
