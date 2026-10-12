# Design system: Calvary funding engagement

Written 2026-10-10, before the first chart. Applies to every chart (PNG), every deck (PPTX) and the Markdown reports. The executable version for charts is `scripts/lib/style.py`; for decks it is `decks/theme.js`.

## 1. Brand inputs

From `2019 CalvaryPPT_White.pptx`: the logo (hand-drawn house over a gold heart, wordmark "Calvary Women's Services", tagline "Ending homelessness. Inspiring hope. Transforming lives.") and a theme with plum `41242F`, gold `D39F28`, light gold `FFDD7F`, teal `52C5DA` / `B1E1E9`. The template's layouts are placeholders only, so everything else here is original.

Logo files: `decks/assets/calvary_logo_white_bg.png` (use on white), `decks/assets/calvary_logo_gold_chevron.png` (title slides only, bottom-right).

## 2. Palette

Two families: **brand** colors for chrome (titles, text, surfaces, accents) and a **data** palette for series. Data colors are assigned by role and never change between charts.

### Brand / chrome

| Token | Hex | Use |
|---|---|---|
| `ink` | `41242F` | Slide titles, chart titles, primary dark surface (title and section slides) |
| `gold` | `D39F28` | Accent: highlighted number, callout, the one emphasized element on a slide |
| `gold_light` | `FFDD7F` | Tint behind a callout card on white |
| `text` | `1F1B1D` | Body text |
| `text_2` | `5C5458` | Secondary text, axis labels, legends |
| `text_muted` | `8C8488` | Source lines, footnotes, as-of dates |
| `grid` | `E6E2E4` | Gridlines, hairline rules, table borders |
| `surface` | `FFFFFF` | Default slide and chart background |
| `surface_2` | `F6F3F4` | Card tint, table header band |

### Data series (validated)

Validated with the dataviz skill's `validate_palette.js` (light mode, white surface, adjacent pairs). All five pass every check: lightness band, chroma floor, CVD separation (worst adjacent ΔE ≥ 8), normal-vision floor (≥ 15) and 3:1 contrast.

| Slot | Role | Hex | Meaning (fixed across all charts) |
|---|---|---|---|
| 1 | `government` | `A03F7E` | Government money (DC and federal, all channels). Also Calvary as an entity on peer charts |
| 2 | `institutional` | `B8810C` | Institutional philanthropy: private, corporate, community foundations, federated giving |
| 3 | `daf` | `0F9ACB` | Donor-advised fund sponsors (donor intermediaries). Also DWC/SheWorks reference rows |
| 4 | `individuals` | `CF5A2C` | Individuals, events, residual private contributions |
| 5 | `other` | `3B6FD8` | Program service, investment, other revenue |

Supporting:
- `peer` `B9B2B6`: peers as a muted set when Calvary is the story.
- Status (only where the color *means* good/bad): `negative` `B23A48` (deficit, cut), `positive` `2E7D5B` (surplus, restored). Always paired with a label.
- Sequential ramp (one hue, light → dark, for magnitude on maps and heat tables): `F7E6F0 E9BFD9 D693BD BF669E A03F7E 7A2A5E 521A40`.
- Diverging (cut ↔ increase): `CF5A2C E9A98E F3E6E0 | D9D5D7 | CFE9F3 7CC3E0 0F9ACB` with the neutral gray at the midpoint.
- Never more than five categorical series on one chart; fold the tail into "Other" (gray) or facet.

## 3. Typography

Fonts that render true-to-width in LibreOffice QA and ship with Office: **Arial** for everything in decks and charts (headings bold, body regular). Reports are Markdown and inherit the reader's font.

| Element | Deck size | Chart (PNG) size |
|---|---|---|
| Slide headline (full sentence) | 26–30 pt bold, ink, left, max 2 lines | — |
| Section divider title | 36 pt bold, white on ink | — |
| Body / bullets | 14–16 pt, text | — |
| Big number (stat callout) | 54–64 pt bold, ink or gold, with a 12 pt label below | — |
| Table text | 11–12 pt | — |
| Source line + as-of date | 9 pt, text_muted, bottom-left of every chart/table slide | 7.5 pt |
| Chart title | — | 12.5 pt bold, ink, left |
| Axis labels / ticks | — | 9–9.5 pt, text_2 |
| Direct labels | — | 8.5 pt, text_2 (white inside dark fills) |

## 4. Slide layouts (pptxgenjs `defineSlideMaster`, 16:9, 13.33 × 7.5 in)

| Layout | Use | Frame |
|---|---|---|
| `TITLE` | Deck cover | Ink background; title 40 pt white, subtitle 18 pt gold_light, date/audience 12 pt; gold-chevron logo bottom-right |
| `SECTION` | Divider between sections | Ink background; section title 36 pt white; one-line takeaway 16 pt gold_light |
| `HEADLINE` | Any content slide | White; headline placeholder (0.6, 0.45, 12.1 × 1.05 in); body region below (0.6, 1.65, 12.1 × 5.1 in); footer: source/as-of (0.6, 6.95) left, logo small (12.0, 6.8) right, slide number |
| `CHART` | One chart + commentary | HEADLINE frame; chart region (0.6, 1.65, 8.0 × 5.1 in) left; commentary card (8.9, 1.65, 3.8 × 5.1 in) right with 3–4 short bullets |
| `WIDE` (2026-10-11) | A chart that needs the whole width (the m6_03 network) | HEADLINE frame; chart full width at (0.6, 1.75, 12.13 × 3.3 in), drawn at that size so its fonts are true points; the card becomes a band below (surface_2, title left, one column per claim or bullet). `lib/deck.js` `wideImage()` |
| `TWO_UP` | Two charts or chart + table | HEADLINE frame; two regions 5.9 in wide |
| `STAT` | Verdict / big numbers | HEADLINE frame; 3–4 stat tiles (number 60 pt, label 12 pt) in a row, one paragraph below |
| `TABLE` | Pipeline, peers, scenarios | HEADLINE frame; table region 12.1 × 5.0 in, header band surface_2, 11 pt |

Appendix covers (engagement lead, 2026-10-11): the white title is a short label, `Appendix X: Short Name` in title case (e.g. "Appendix C: Funder Pipelines"), not a sentence; the gold subtitle carries the description.

Rules: headline position identical on every content slide; 0.6 in side margins; 0.3 in between blocks; no accent bars, stripes or lines under titles; emphasis by color (gold) and size, not decoration; nothing but the logo and the footer below y = 6.8 in.

### Sourcing rule (engagement lead, 2026-10-10): every slide with data is rigorously footnoted

Every slide that shows a number, chart or table carries a footnote block (9 pt, `text_muted`, bottom-left, up to three lines):
1. **Source:** the original publisher(s) and document(s) (e.g., "IRS Form 990 e-file returns TY2020–24 via GivingTuesday; Calvary audited financial statements FY15–FY23; DC OVSJG award lists FY2019–2026"), then the clean table(s) in `calvary_funding_data/clean/`.
2. **Method:** the measure and any transformation in one clause (e.g., "government share = audited government revenue ÷ total revenue; 990 line 1e for FY24–25"), with assumptions named ("CoC competition year t aligned to Calvary FY t+1").
3. **Trace:** `Chart m2_02 · data as of 2026-10-10 · method note A3` — the chart ID links to `chart_data/<id>.csv`, whose `source_ids` link to `sources/source_registry.csv`; the method note number links to the "Data and methods" appendix of that deck.

Where the method needs more than one clause, the slide footnote cites a numbered **method note** and the full explanation lives in that deck's appendix section "Data and methods" (one slide per note: question, tables, filters, formula, caveats, confidence). The consulting and appendix decks carry the complete method notes; the leadership deck carries the short footnotes and points to the appendix deck. Reports use the same convention as end-of-section source notes.

## 5. Chart style

- Form follows the job: trend → line; composition over time → stacked area/column; magnitude comparison → horizontal bars sorted by value; change between two points → slope; one number → stat tile; flows → Sankey (PNG); relationships → network (PNG); geography → ward map (PNG).
- Native PowerPoint charts (editable) for bar, column, line, stacked and scatter; PNG at 200 dpi for network, Sankey, map, small multiples and anything annotated.
- One y-axis, always. Two measures → two charts or an index.
- Marks: bars ≤ 60% of slot width with a flat baseline and a 1 px black outline (0.5 pt at 200 dpi; no white gaps between stacked segments, no outline on empty segments, legend swatches match) — engagement lead, 2026-10-11; lines 2 px; markers ≥ 8 px with a white ring; area fills at 10–15% opacity.
- Axes (engagement lead, 2026-10-11): no gridlines; x and y axis lines in black (`text`); no top/right spines; axis tick labels, axis titles and data labels bold and black. Enforced at save time by `scripts/lib/style.py` `polish()` for PNGs and by `decks/lib/deck.js` `chart()` for native charts; notes placed in axes coordinates keep regular weight. `polish()` also nudges data labels off each other and off scatter dots, with a thin leader line back to the point when a label moves 9 pt or more, and prints any label it could not clear. Ticks rounded with thousands commas; money in $M (one decimal) or $K.
- Labels: a legend whenever ≥ 2 series; direct labels only at endpoints, extremes or the series the story is about; text never wears the series color.
- Emphasis: the story series in its role color, everything else `peer` gray; one gold annotation per chart at most.
- Every PNG carries: title (full sentence takeaway when standalone), source line naming the clean table(s), as-of date, chart id. Every chart slide carries the same in the footer.
- Fiscal-year labels: "FY25" for Calvary (FYE Sept), "TY2024" for funder tax years, "DC FY2026" for District budget years. Mixed calendars are labeled on the chart.
- Named comparators (DWC, CBWC/SheWorks) appear as reference rows in `daf` teal with a dotted outline on every peer chart, labeled "(LA, reference)".

## 5b. Deck craft (consulting patterns adopted 2026-10-10, from the engagement lead's reference material)

**Argument structure (Pyramid Principle / SCQA).** The deck leads with the answer, then 3–5 mutually exclusive, collectively exhaustive supporting arguments, then evidence. The leadership deck opens with an executive-summary slide in Situation → Complication → Resolution form (most of the space on the resolution), and the section order is the argument: what Calvary built → the shape of its funding → the clouds → what peers show → where the opportunities are → the plan.

**Executive-summary slide, bold-claim / evidence-bullet format.** Each claim is one bold sentence; under it, two or three bullets carry the specific numbers. A reader who skims only the bold lines gets the whole argument. The same format is used inside commentary cards on content slides (bold lead sentence, then evidence).

**Action titles.** A complete sentence with a verb, 20 words or fewer, never more than two lines at 21 pt, passing the "so what" test. No semicolons in a title or bumper: a title with a semicolon is two thoughts, so rephrase it as one sentence (engagement lead, 2026-10-10). Topic titles ("Revenue mix", "Peer comparison") are not allowed. Reading the titles in order tells the whole story (checked by extracting them from the built deck against the headline spine).

**One message per slide.** Every element proves the title; anything else moves to the appendix. Body text 11–13 pt; selective emphasis: one accent (gold or the role color) on the thing the title is about, grey for context; no more than four colors on a chart.

**Bumper statement (implication line).** Content slides end with a one-line implication in italic, 11 pt, above the footnote: "Implication: …". It states what the slide means for Calvary's choices, so the "so what" is explicit even when the title is a finding.

**Status / next-steps slides.** Answer the five questions in order: what happened, what is next, what needs attention, what we need from you (decisions needed). Decisions needed are always stated explicitly, never implied.

**Appendix exception (engagement lead, 2026-10-10):** appendix slides that exist to be referenced or shared as content (full tables, method notes, data lists) may carry a plain descriptive header instead of an action title. Main-deck slides never do.

**Every slide:** source citation (the sourcing rule in §4), page number, consistent title position, fonts and alignment. The checklist before any deck is final: leads with conclusions; MECE sections; exec summary stands alone; titles alone tell the story; one message per slide; every element supports the title; every data point sourced; fonts and alignment consistent; 30-second comprehension per slide; conclusions specific and actionable; "so what" clear for every data point.

## 6. Emphasis and tone

**Voice (engagement lead, CP2):** this is a pro bono engagement two weeks old, delivered by a corporate volunteer to a nonprofit leadership team. Lead with what Calvary has built and with options it can choose; state the clouds on the horizon plainly but with humility and a path through them; avoid labels like "exposed" or "dependent" in headlines (prefer "concentrated", "reliance", "headroom", "opportunity"); credit the team where the data shows strength. The consulting materials keep the same courtesy with full analytical candor.

- One idea per slide; the headline is the takeaway and the body proves it.
- Verdicts use plain words: "concentrated", "durable", "one-time", "under pressure". The CP2 voice ruling above wins over the earlier verdict-word list, so "exposed", "dependent", "dependency" and "failure" are not used as labels in any deliverable (fix cycle, 2026-10-11).
- Funder status is part of the message: a funder is named as a prospect in leadership materials only after its open status is checked on its own page (`config/guideline_notes.csv` `open_status`), and closed funders and giving channels are never presented as grant prospects.
- Caveats are visible, short, and in text_muted under the chart, never hidden in notes.
- Provisional items (core peers, reconstructed FY24–25 government share, medium-confidence interlocks) are labeled "provisional", "reconstructed" or "unconfirmed" on the slide where they appear.
