# Checkpoint C: <topic> (built PDF and review)

*<date>. PDF: `calvary_analysis/decks/pdf/<file>.pdf` (<n> pages). Source: `decks/build_<slug>.js`.*

## What it says in three lines
1. <...>
2. <...>
3. <...>

## QA checklist (all must pass before sending)
| Check | How | Result |
|---|---|---|
| Headlines: full sentences, 20 words or fewer, no semicolons, match the spine | `decks/build_all.sh <key>` (runs `scripts/lib/headline_check.py`) | |
| Every chart and number traces to chart data and the source registry | `scripts/lib/trace.py` prints TRACE OK | |
| Every data slide has a source / method / chart-ID footnote | read the slide images | |
| Numbers match the insight register and the other decks | compare against `insight_register.csv` and `reports/review/fix_spec.md` | |
| Every named funder's open status is first-party checked and not closed or a channel | `config/guideline_notes.csv` | |
| Tone: no "exposed", "failure", "dependency" as labels; what Calvary built comes first | grep the build script and the PDF text | |
| Audience data rules (no person-level data; Calvary-internal only for Calvary readers) | `storylines/audiences.md` | |
| Visual: no overlaps, cut-off text or hidden chart labels | every image in `decks/qa/<key>/` | |
| Anything leaving the team: guardrail scan | `REVIEW_OUT=<scratch> python reports/review/scripts/guardrail_scan.py` | |

## Caveats on the slides
- <provisional items and how they are labelled>

## What I would do next
- <...>

## Decisions needed
1. <approve to share / changes>
