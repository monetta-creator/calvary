# Decisions log: the engagement lead's rulings

Dated rulings that shape how work is done here, with the reason for each. `CLAUDE.md` states the rules; this file keeps the history behind them so a new analyst (or a new Claude session, which starts with no memory of earlier sessions) can tell a deliberate choice from an accident. Add a row whenever the lead rules on something that should outlive the conversation.

## Scope and data (CP1, 2026-10-10)

| Ruling | Reason |
|---|---|
| The 18 core peers are provisional. Results that depend on them say so, and they change in one config file (`calvary_funding_data/config/core_peers.csv`) | Nobody inside Calvary has confirmed the set yet |
| Downtown Women's Center (Los Angeles) and the CBWC Empowerment Institute / SheWorks appear in every analysis as named comparators, even DC-only views | Direct request from Calvary's CEO: DWC is the national model for women-only homeless services, and SheWorks is a program design the CEO is watching |
| Prompt 1 documents stay untouched. Where they are stale, the correction lives in the analysis (`docs/memory_reconciliation.md`) | The data foundation was reviewed and rebuild-tested as delivered |
| Gates and TCP are excluded from the funder landscape (`calvary_analysis/config/landscape_exclusions.csv`) | Gates funds global and research recipients. TCP is a pass-through intermediary, not a funder |
| Stress-test cut levels and pipeline weights live in config files, not code | The lead wants to change assumptions without touching scripts |

## Voice, sourcing and craft (CP2, 2026-10-10)

| Ruling | Reason |
|---|---|
| "Always lean recommendations. This is a pro bono project … Approach findings with humility and positive framing, while being real about the clouds on the horizon." Lead with what Calvary has built, frame risks as clouds with a path, offer options | The lead is a corporate volunteer two weeks into the relationship, and Calvary's leadership is sensitive to an outsider's verdict |
| No "exposed", "failure", "dependency" as labels | Same reason. Use concentration, reliance, headroom, opportunity |
| No semicolons in slide titles ("lazy and weak"). A semicolon means two thoughts, so write one sentence | Titles must pass the "so what" test and read as one claim |
| "All slides with data should be rigorously sourced, footnoted, or with detailed methodology in the appendix of the respective deck" | The decks go to Calvary's board and to a consulting team, so every number must be defensible back to a public document |
| Appendix slides that exist as reference content (tables, method notes) may use plain descriptive headers | They are looked up, not presented |
| "We just need to work with what we have and make reasonable assumptions about the data." Assume, log it with a confidence level, and keep building | The lead has no inside knowledge of Calvary's records (CRM field meanings, report years, missing audits) |
| Medium-confidence board links appear only in consulting materials, labelled "unconfirmed" | A name match may be two different people |
| Deck craft: answer first (Situation–Complication–Resolution executive summary), action titles of 20 words or fewer, one message per slide, an implication line, decisions named on the closing slide | Adopted from the lead's consulting reference material |

## Deliverables and presentation (2026-10-11)

| Ruling | Reason |
|---|---|
| Cosmetic edits arrive as a screenshot plus a description and are visual only (no content changes). A formatting rule given on one slide applies to every slide and every deck | The lead wants consistency without having to find every instance |
| Appendix deck covers read "Appendix C: Funder Pipelines" style (short title in white, detail in the gold subtitle) | Shorter covers |
| House chart style: no gridlines, black x and y axes, bold axis and data labels, a 1 px black outline on bars, overlapping labels pulled apart with leader lines | The grey gridlines were distracting; the lead liked the outlined bars and asked for them everywhere |
| **PDFs are the deliverable.** The PPTX files are the editable source | Native charts render correctly only in PowerPoint and LibreOffice; other viewers (Keynote, Quick Look, VS Code's Office viewer) drop the styling |
| Every deliverable answers the CEO's first question on its main surface ("who are these 19 organizations?") | Stated as a principle while reviewing the network page: context first, fine print behind a label |
| The interactive network page is the **Calvary Grantmaker Web**: "Funder" wording, framed honestly as public IRS filings of grantmakers (one component of nonprofit funding, in service of finding additional funding sources) | The lead wanted the data's scope upfront: individuals, companies giving directly and government agencies do not file these grant lists |
| The Grantmaker Web is a single self-contained HTML file (opens offline by double-click); the published claude.ai copy is not maintained | The lead presents from the file and shares it directly |

## Review fix cycle (2026-10-11)

| Ruling | Reason |
|---|---|
| Fix every review finding row by row, record each in `calvary_analysis/reports/review/fix_log.md`, then have an independent read-only pass re-verify before the register is marked verified | Same separation of authoring and review that produced the review |
| Only Schattner is named as a new prospect in leadership materials; Bunting and Bechtel (Tier 3, no public process) are not plan targets; funders of exactly three peers are labelled as depending on the provisional peer set | A funder is named only after its open status is checked on its own page |
| The FY25 event "collapse" was a 990 reclassification (line 1c → 8a); the $3.0M private-revenue target was rebuilt without an events component | Receipts held at $596K → $533K |
| Stress-test losses are reported as ranges, never single points | The stream split of FY25 revenue is not public |

## Repository (2026-10-12)

| Ruling | Reason |
|---|---|
| The repository moves to the lead's work GitHub, and Claude Code at work connects to it | Work continues from the work environment |
| Durable context lives in the repository (`CLAUDE.md`, `docs/decisions.md`, `.claude/skills/`), not in a personal Claude memory | Personal memory does not travel between machines |
| The root holds only `CLAUDE.md`, `README.md`, `setup.sh`, `docs/` and the two project folders. Calvary's documents live once, in `calvary_funding_data/inputs/` | The root had duplicate copies of client documents |
| The work copy leaves out Calvary's two internal documents (the CRM export and the internal 2021–24 plan report) and starts a fresh history, published as the single-branch `work-handoff` branch of the original repository | Calvary's internal documents should not sit on the lead's employer's systems. A fresh history means they are not in old commits either |
