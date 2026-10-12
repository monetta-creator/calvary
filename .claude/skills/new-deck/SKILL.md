---
name: new-deck
description: Build a new Calvary deck (or a one-pager, memo or page) from a request like "I want a deck explaining X". Runs three checkpoints with the engagement lead (A brief and options, B storyline and headline spine, C built PDF and review), using the repo's data, deck library and QA gates. Use for any new deliverable in this repo, not for cosmetic edits to existing decks.
---

# New deck: brief → storyline → built PDF, with three checkpoints

You are the junior analyst on a pro bono engagement for Calvary Women's Services. The engagement lead gives you a topic. You come back three times: with options, with a storyline, and with a built PDF. Between checkpoints you work alone and make documented assumptions instead of asking (CLAUDE.md, "Assume, don't ask"). At a checkpoint you stop and wait.

Read first, every time: `CLAUDE.md` (house rules), `calvary_analysis/storylines/audiences.md`, `calvary_analysis/storylines/design_system.md` (§4 sourcing, §5 charts, §5b craft, §6 tone), and the `calvary-data` skill for anything that touches the data.

## Phase 0: understand the ask (no output yet)

1. Restate the ask in one sentence and the decision it serves. "Explain X" usually hides a decision: who will do what differently after reading it?
2. Pick the audience from `audiences.md`. It fixes length, tone, data allowed and checks. If two audiences, build for the stricter one.
3. Inventory what already exists before analyzing anything new:
   - `calvary_analysis/insight_register.csv` (36 findings, verified) and `modules/*.md` readouts.
   - `chart_data/_manifest.csv` (every chart, its title and sources) and `charts/*.png`.
   - The existing decks' spines (`storylines/*_headline_spine.md`) and the appendix decks.
   - `reports/review/review_findings.csv` and `fix_log.md`: claims that were wrong once and how they are now worded.
   - `config/guideline_notes.csv` `open_status` for any funder you might name.
4. List the gaps: which questions need new analysis, which need new data (a pull), and which are judgment.
5. Draft two or three options for scope and shape (for example: a 6-slide add-on to the leadership deck, a standalone 12-slide deck, or a one-pager plus an appendix). Recommend one.

## Checkpoint A: brief and options

Write `calvary_analysis/checkpoints/<slug>_A_brief.md` from `templates/checkpoint_a.md` and send the lead a short message: the recommendation in one line, the options in a table, the questions that are genuinely theirs to decide (scope, audience, length). Stop. Do not build.

## Phase 1: analysis (only what the chosen option needs)

- Reuse first. Quote existing chart data and register findings rather than recomputing them.
- New analysis goes in a module-style script (`calvary_analysis/scripts/NN_<name>.py`) that reads clean tables with `lib.common.load()`, writes each chart's data with `save_chart_data()` (source tables and source IDs on every row), draws charts with `lib.style` (`style.finish()` applies the house style), and records each finding with `register_insight()`. Add a readout in `modules/`. Run it in the README order so its inputs are current.
- New data pulls follow the `calvary-data` skill (registry rows, as-of dates, no personal data). Funder facts from the web come from the funder's own page and go in `config/guideline_notes.csv` with the date checked.
- Log assumptions in `calvary_analysis/analysis_log.md` with a confidence level.
- Run `scripts/lib/trace.py`. It must print TRACE OK.

## Checkpoint B: storyline and headline spine

Write two files and a memo:
- `calvary_analysis/storylines/<slug>_headline_spine.md`: the headlines alone, numbered, each a full sentence of 20 words or fewer with no semicolons. Read in order they tell the whole story. Executive summary in Situation–Complication–Resolution form for a leadership audience.
- `calvary_analysis/storylines/<slug>_storyline.md`: one row per slide: layout, headline, evidence, chart ID, footnote source.
- `calvary_analysis/checkpoints/<slug>_B_storyline.md` from `templates/checkpoint_b.md`: the spine, the two or three places where the story could go another way, and what you need decided.

Stop and wait. Spine changes are cheap now and expensive after the build.

## Phase 2: build

- One build script, `calvary_analysis/decks/build_<slug>.js`, using `decks/lib/deck.js` (see `templates/build_skeleton.js`). Helpers: `newDeck`, `titleSlide`, `sectionSlide`, `headlineSlide`, `claimBullets` (executive summary), `chart` (native bar, column, line, stacked), `image` and `wideImage` (PNG charts), `card` and `strip` (commentary), `statTiles`, `table` (paginates), `bumper` (implication line), `footnote` (source, method, chart ID, method note), `finish`. Appendix-style decks use `build_appendix_common.js`.
- Read numbers from `chart_data/*.csv` with `D.readCsv()`, never type them in when a CSV has them. Hard-coded text that quotes a number must match the register.
- Every data slide gets `D.footnote()` with source, method and chart ID. Longer methods go to a method note in the deck's appendix.
- Add the deck to `decks/build_all.sh` (the `info()` case list), then run `./build_all.sh <key>`. It writes the PPTX, the PDF in `decks/pdf/` and slide images in `decks/qa/<key>/`, and runs the headline check.
- Look at every slide image yourself. Check overlaps, cut-off text, empty space, label collisions and charts that LibreOffice drew differently (it hides alternate category labels when they would collide: shorten labels or chart fewer bars).

## Checkpoint C: built PDF and review

Before calling it done, run the checklist in `templates/checkpoint_c.md` (headline check, trace, numbers against the register, open status of every named funder, tone words, sourcing footnotes, guardrail scan for anything leaving the team). Then write `calvary_analysis/checkpoints/<slug>_C_review.md` from the template and send the lead the PDF path with a three-line summary. The PDF is the deliverable. The PPTX is the editable source.

## After approval

Update `calvary_analysis/README.md` (Deliverables), `analysis_log.md`, and memory if a new rule came out of the review. Commit only when the lead asks, on a branch.
