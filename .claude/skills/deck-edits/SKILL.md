---
name: deck-edits
description: Apply a visual edit to the Calvary decks or charts, usually given as a screenshot plus a description ("make the legend smaller", "remove the gridlines", "shorten the appendix titles"). Fixes it at the shared layer so every slide gets it, rebuilds PPTX, PDF and QA images, and proves no content changed. Use for formatting and layout changes, not for new content (use new-deck) or number changes (fix the source script).
---

# Deck edits: visual changes, applied everywhere, with no content drift

The engagement lead sends a screenshot and a description. The edit is visual only: no wording or number changes unless the lead says so. A formatting rule shown on one slide applies to every slide in every deck, and to the PNG charts if it concerns charts.

## 1. Find the layer that owns it

| What changes | Fix it in | Covers |
|---|---|---|
| Colors, fonts | `calvary_analysis/decks/theme.js` | all decks |
| Slide masters, footnotes, bumpers, cards, native charts, tables | `calvary_analysis/decks/lib/deck.js` | all decks |
| Appendix-only helpers (covers, tables, PNG placement) | `calvary_analysis/decks/build_appendix_common.js` | Appendices A–D |
| PNG charts (matplotlib) | `calvary_analysis/scripts/lib/style.py` (`polish()` runs at save) | every chart in `charts/` |
| One slide only | the specific `decks/build_*.js` | that slide |

Prefer the shared layer. Then grep every `build_*.js` for hard-coded options that bypass it (for example a `fontSize`, `catFontSize` or `valFmt` passed on one chart) and bring them in line.

## 2. Record the rule

A new formatting rule goes into `calvary_analysis/storylines/design_system.md` (chart rules in §5, deck craft in §5b) with the date, so future decks follow it. A rule about how the lead works goes in `docs/decisions.md`.

## 3. Rebuild and prove nothing else changed

1. Before editing, snapshot the slide text: extract every deck's text, tables and native chart data with python-pptx into a scratch folder.
2. Make the change. If PNG charts are affected, rerun the module scripts that draw them, in README order, and check with `git diff --stat calvary_analysis/chart_data/` that the chart data did not change.
3. `cd calvary_analysis/decks && ./build_all.sh` (or name the decks). It rebuilds PPTX, renders `pdf/` and `qa/<deck>/slide-NN.jpg`, and runs the headline check.
4. Extract the text again and diff it against the snapshot. A visual edit should show no text difference.
5. Look at the before and after images of the slides the lead pointed at, and at a sample of others, especially charts with many labels. LibreOffice hides colliding category labels, so a longer label can silently drop every other bar name.

## 4. Report

One line: what changed, where (file and helper), how many slides it touched, and that the text diff is clean. Point to `decks/pdf/` for review. The PDFs are the deliverable.

## Known traps
- Native charts look wrong in Keynote, Quick Look and VS Code's Office viewer. Judge from the PDF or the QA images.
- `fitTitles()` in the build scripts steps the title size down for long headlines. A shorter title can change the layout below it.
- Data labels on stacked bars sit in the center; on single bars, outside the end. Changing one can collide with the axis.
- When you rerun module scripts, the manifest's `written` column and `analysis_log.md` change on every run. That is noise, not content.
