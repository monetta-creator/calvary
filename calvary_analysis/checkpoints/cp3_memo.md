# CP3 memo: draft deliverables (2026-10-10)

Five-minute read. Everything below is in `calvary_analysis/`; paths are relative to it.

## 1. Where the drafts are

| Deliverable | Location | Size | QA |
|---|---|---|---|
| Executive one-pager | `decks/executive_one_pager.pptx`, `reports/executive_one_pager.md` | 1 slide | validated, rendered, headline ≤20 words |
| Leadership and board deck | `decks/leadership_deck.pptx` (spine `storylines/leadership_headline_spine.md`, storyline `leadership_storyline.md`) | 22 content slides + 5 dividers (26 total) | validated; 22/22 headlines match the spine, all ≤20 words, no semicolons; visual QA pass |
| Consulting deck | `decks/consulting_deck.pptx` (spine `consulting_headline_spine.md`, storyline `consulting_storyline.md`) | 55 content slides + dividers and table continuations (66 total) | validated; 55/55 match, ≤20 words, no semicolons; visual QA pass |
| Appendix decks | `decks/appendix_A_calvary_government.pptx` (22), `appendix_B_peers_comparators.pptx` (21), `appendix_C_funders_pipeline.pptx` (69), `appendix_D_data_methods.pptx` (33); spines in `storylines/appendix_headline_spine.md` | 145 slides | validated; slide-by-slide check by the builder; reference headers allowed per your note |
| Reports | `reports/executive_summary.md`, `full_findings.md`, `methodology.md`, `recommendations.md` | — | numbers reconciled to the register after a consistency pass |
| Readouts | `reports/board_readout.md` (talking points), `reports/consulting_briefing.md` | — | — |
| Supporting | `storylines/design_system.md` (incl. the sourcing rule and the consulting-craft section), `scripts/`, `chart_data/` (60 CSVs + manifest), `charts/` (45 PNGs), `modules/` (10 readouts), `insight_register.csv` (36, status draft), `recommendations/funder_pipeline.csv` (182 rows), `action_plan_90day.csv` (11 rows), `config/scoring_weights.yaml` | — | `scripts/lib/trace.py` OK; `scripts/lib/headline_check.py` OK |
| READMEs | `README.md` (analysis), `../README.md` (project), section added to `../calvary_funding_data/README.md`; `../input_map.md` current | — | — |
| Rendered slides for review | `decks/qa/<deck>/slide-NN.jpg` | — | — |

## 2. What changed since CP2

- **Craft rules applied from your reference material:** SCR executive summary up front, action titles ≤20 words on two lines, no semicolons, one message per slide, bold-claim/evidence cards, a bumper (implication) line on content slides, "decisions needed" on the next-steps slide, source/method/trace footnote on every data slide. Appendix slides may use plain reference headers (your note today).
- **Consistency pass:** the report-assembly subagents found register-vs-readout differences, which were fixed at the source and propagated: Calvary ranks **11th of 19** peers (not 12th); landscape total **$660M / $132M a year** (not $620M / $124M), 555 institutional funders, top 10 = 55%; audit-basis government share range **40–61%** (audited government ÷ audited revenue; was 44–64% with a mixed denominator); M6 330 funders; **Tier 1 = 11** after T. Rowe Price was reclassified as a donor-advised channel and corporate rows were held to the score cutoff (Frontier Co-op → Tier 2); Sisters Rise 24 HIC beds (DHS capacity 25); DWC ×5.5. `cp2_memo.md` is left as the record of that checkpoint.
- **Guideline pull done:** Tavily hits for 32 Tier 1–2 funders, reviewed into `config/guideline_notes.csv` (27 funders; first-party pages for about half, e.g., Cafritz Mar 1 / Jul 1 / Nov 1, Venable Feb 1 / Jun 1 / Sep 1, Many Hands January window, Bank of America two RFP cycles, Meyer Interest Form, Cohen invitation-only) and merged into the pipeline and 90-day plan.
- **Sensitivity run** (`chart_data/m7_05_sensitivity.csv`): ±0.05 on any weight moves top-30 ranks by about one place and keeps 9–10 of the top 10.
- **Portability fix:** image alt text in the decks carried absolute paths; now relative. Zero path or username strings in any deck.

## 3. Open issues

1. Three flags still rest on documents only Calvary can provide (D1 audits/TCP agreements, D2 Sisters Rise, D3 gala calendar); the decks say so.
2. Core peers remain provisional; a swap moves the gap list and rank but not the verdict.
3. Text inside PNG charts (network map, 20-panel small multiples) is small at slide size; the native-chart slides carry the same numbers legibly, and the PNGs are there for the appendix and reports.
4. `reports/full_findings.md` is about 9,400 words and `methodology.md` about 7,100 (over the targets I set the subagents because the full tables are kept); trim if you want shorter.
5. Register rows are `draft` until the Phase 6 review.

## 4. Feedback I would value before the final review

- The leadership deck's tone, especially slides 2 (executive summary), 7 (FY25), 9–10 (the clouds), and 21 (decisions needed).
- Whether the five dividers and the 22-slide length suit the board meeting you have in mind.
- Any Tier 1 name you would not want raised with Calvary, and the owner roles.
- Whether to keep DV formalization in the expansion options (it raises the public share).

## 5. Next

On your go: Phase 6, an independent review agent with no access to this session's history (inputs: input map, deliverables, insight register, clean tables) checks every number, headline and caveat, confirms interlock handling, and writes `reports/review_report.md`; I fix every issue, mark register rows `verified`, and update the README and input map.

Stopping here until you respond.
