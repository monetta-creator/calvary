# Prompt 2 of 2: Analysis, Recommendations, and Deliverables for the Calvary Women's Services Funding Survey

## Your role and scope

You are the lead analyst on a pro bono strategy engagement for **Calvary Women's Services** (EIN 52-1307706), a Washington, DC nonprofit serving women experiencing homelessness in Wards 7 and 8.

A previous session (Prompt 1) built a clean, documented dataset in this project. Your job is to turn that data into analysis, recommendations, and a full suite of deliverables: Markdown reports, chart files, and PowerPoint decks.

Two questions anchor the engagement:

1. **Exposure:** To what extent is Calvary under funding pressure because of its reliance on government money (federal and DC)?
2. **Opportunity:** What other funding exists, at every tier and from every source type, that fits Calvary's current mission or a plausible expansion of it? Which opportunities should Calvary pursue first, and how?

## Session setup

**Model and mode.** This session runs on Fable 5.1 at high effort and starts in plan mode.

**Plan mode covers orientation.** While in plan mode, locate the inputs, read Claude Code memory and compare it with the project files, profile the clean tables, and draft the analysis plan. Present the plan for approval with these sections:
1. Input map (each input and where you found it)
2. Memory reconciliation (every difference, with proposed severity and resolution)
3. Data profile (what the data can and cannot support)
4. Proposed analysis modules
5. Early signals and open questions for me

**Plan approval is the real CP1.** My approval, with any rulings on memory differences and module changes, is the main decision point. After approval, write `input_map.md`, `memory_reconciliation.md`, and the analysis plan to disk exactly as approved, then send a brief CP1 confirmation and continue into Phase 2 once I acknowledge it.

**Skills.** Check the skills available in this environment before starting. If one covers this workflow (plan-mode analysis, Fable sessions, deck building, PPTX, or charting), load it and follow it. Where a skill and this prompt conflict, follow this prompt and note the conflict in the plan.

**Subagent models.** Keep the judgment work in this main Fable session: analysis design, the insight register, flags to me, recommendations, scoring, and the storylines. Route high-volume production to subagents on Opus 5.5: rendering chart batches, building appendix slides, running visual QA, and assembling profiles. Run the Phase 6 independent review as a separate subagent with no access to this session's history.

## How to approach this work

**You design the analysis.** You can see the data; I have not seen it yet. Read what Prompt 1 produced, judge what it can and cannot support, and build the analysis around the strongest evidence. The anchor questions and deliverables in this prompt are fixed. Everything between them is yours to decide: which modules to run, which comparisons matter, which charts tell the story, and where the surprises are.

**Let the data lead.** The anchor questions and candidate modules in this prompt are a starting frame. If the evidence points somewhere this prompt does not anticipate, follow it and explain why. If the data cannot answer part of a question, say so plainly and show what it would take to answer it.

**Bring new findings to me as they emerge.** When you find something interesting, surprising, or direction-changing (an unexpected funder pattern, a peer that diversified in an unusual way, a data anomaly that changes a conclusion, a new opportunity type), flag it to me right away. Keep the flag short: what you found, the evidence, why it matters, and what you propose to do about it. Log every flag in `discoveries_log.md` with the date, finding, evidence, proposed action, and my response. Continue with work the flag does not affect. Hold any change in direction or scope until I weigh in. Include all open flags in the next checkpoint memo.

**Every number traces to its source.** Each figure in a report or deck must link to a chart-data CSV, which links to a clean table from Prompt 1, which links to a source in the source registry.

**Use subagents** for independent analysis modules and for the independent review in Phase 6.

## Locate your inputs (do this first)

The project folder was built in an earlier session, and its folder and file names may differ from the descriptions in this prompt. This prompt describes each input by what it contains. Search the project (list directories, glob, and grep file contents) to find the actual location of each one.

**Inputs to locate:**

| Input | What it contains | Likely signals |
|---|---|---|
| Project README | Project purpose, folder map, rebuild instructions | Top-level Markdown file describing the project |
| Clean tables | Final analysis-ready CSVs: organization and funder dimensions, financials by year, grants, government awards, opportunities, policy events, people and roles, organization relationships, universe membership | CSVs keyed on EIN; names beginning with `dim_` or `fact_` |
| Data dictionary | Definitions of every table and column | CSV or Markdown listing table and column names with definitions |
| Source registry | Every source with ID, URL or file, publisher, retrieved date | CSV with source IDs referenced by the clean tables |
| API catalog | What each API returned, coverage, and limits | Markdown or CSV describing endpoints |
| Data quality report | Row counts, missing values, reconciliation, coverage gaps | Markdown report on data quality |
| Data inventory report | Summary of what was collected per universe and year | Markdown report summarizing the dataset |
| Analysis notes | Patterns and anomalies Prompt 1 flagged for analysis | Markdown file of notes or observations for the analysis |
| Open questions | Items Prompt 1 flagged for my input | Markdown file of open questions |
| Build scripts | Scripts that rebuilt the clean tables from raw data | Numbered Python scripts |
| Requirements file | Python dependencies | `requirements.txt` or equivalent |
| Raw data | Untouched API responses and downloads (may be absent on this machine) | Large folder of JSON, XML, ZIP, or downloaded files |
| Build log | What ran, row counts, failures, decisions | Markdown log |
| Client template | A PowerPoint file from Calvary with its logo | Likely named `2019 CalvaryPPT_White.pptx`; search for any `.pptx` if absent |
| Client data (optional) | Internal Calvary data such as a budget, funder list, or grant history | Spreadsheets or documents from the client |

Write `input_map.md` at the project root: each input, its actual path, a one-line description of what you found, and anything missing or ambiguous. Use the paths in this map for the rest of the work. If an input is missing, note it in the map and in your CP1 memo, then continue with what exists.

### Reconcile memory against the project files

The Prompt 1 session saved context about this project to Claude Code memory. Read everything available in memory for this project (CLAUDE.md files and any saved memory entries), then compare it against what you found in the project files.

Differences are likely. Memory may describe a file, table, count, decision, or finding that the files show differently, or the files may contain things memory never recorded. Log every difference in `memory_reconciliation.md` with these columns:

`item, what_memory_says, what_the_files_show, likely_explanation, proposed_severity, proposed_resolution`

Use these severity levels as a proposal:
- **High:** affects a finding, a number, a universe definition, or which data is trustworthy.
- **Medium:** affects where something lives or how a table should be read.
- **Low:** naming, wording, or a stale detail with no effect on the analysis.

Flag every difference, including low-severity ones. I will decide which ones need my input. Until I respond, treat the project files as the working source of truth, and avoid building any analysis on an item marked High. Summarize the reconciliation in the CP1 memo.

## Environment check

This session may be running on a different machine from Prompt 1. Confirm that the clean tables load and that their row counts match the data inventory report. Note whether raw data is present. Install the packages in the requirements file plus what you need for charts and decks (e.g., pandas, matplotlib, networkx, python-pptx). If a PPTX or document skill is available in this environment, read it before building decks. Log the environment state in an analysis log.

## Checkpoints

This work has three checkpoints. At each one, write the checkpoint memo, send me a short summary, and **stop and wait for my response** before continuing. Keep each memo short enough for me to read in five minutes or less.

| Checkpoint | When | Memo contents |
|---|---|---|
| **CP1: Analysis plan** | Plan-mode approval, then a brief confirmation once files are written | The input map summary, the memory reconciliation (all differences with proposed severity), what the data supports, proposed modules, early signals, open data gaps, and anything you want me to decide |
| **CP2: Findings and recommendations** | End of Phase 3 | Top findings from the insight register, the funding-pressure verdict, draft recommendations and tiering, and the proposed storyline for each deck |
| **CP3: Draft deliverables** | End of Phase 5 | Locations of draft decks and reports, slide counts, open issues, and anything you want feedback on before final review |

## Phase 1: Orientation and analysis plan

- Read every input you located. Profile the clean tables: coverage by universe, years, and source; completeness; and the strength of each dataset.
- Write an analysis plan containing:
  - The questions the data can answer, ranked by strength of evidence.
  - Proposed analysis modules, each with its purpose, input tables, methods, expected outputs, and how it serves the two anchor questions.
  - Early signals you noticed while profiling.
  - Gaps, weak spots, and how you will handle them.
- **→ CP1.**

### Candidate modules (starting menu; add, merge, or drop based on the data)

- **Calvary financial trajectory:** revenue mix over time, government share, concentration in single streams, liquidity, and growth.
- **Government exposure and stress testing:** stream-by-stream mapping against the policy timeline, with scenario modeling of cuts at different levels.
- **Peer benchmarking:** Calvary against each comparison universe on revenue mix, size, growth, and resilience; identification of peers that diversified successfully and how.
- **Funder landscape:** who funds this space in the DC region, at what scale, how concentrated, and how giving has shifted over time.
- **Funder gap analysis:** funders who support Calvary's peers and do not yet support Calvary.
- **Network analysis:** the funder-grantee network and board interlocks; central funders, co-funding clusters, and relationship paths from Calvary's current circle to target funders.
- **Opportunity pipeline:** open and forecast public opportunities, plus foundation and corporate programs, matched to Calvary's programs.
- **Mission-expansion scan:** funding pools that open up with adjacent programs (aging, women veterans, reentry, maternal health, workforce, behavioral health, or others the data surfaces), with the distance from current operations.

## Phase 2: Run the analysis

For each approved module:
- Write numbered analysis scripts that read from the clean tables.
- Save every chart's underlying data as a CSV.
- Render charts as PNGs using a consistent visual style (see the Phase 5 design system).
- Write a module readout (one Markdown file per module): question, method, findings, chart references, caveats, and confidence.
- Log every finding in an insight register as you go.

**Insight register columns:** `insight_id, module, finding, evidence_summary, chart_ids, source_tables, magnitude, confidence (high/medium/low), implication_for_calvary, audience (leadership / consulting / both), status (draft/verified)`

## Phase 3: Recommendations

Build recommendations from the findings. Design the scoring approach around the data you actually have, and document it so I can adjust it. At minimum, produce:

- **The funding-pressure verdict:** a clear statement of how exposed Calvary is, with the key evidence and scenario results.
- **A scored and tiered funder pipeline** (CSV). Score on the dimensions the data supports (e.g., mission fit, evidence of regional and peer giving, award size, accessibility, durability, relationship paths). Put the weights in a config file so I can change them and rerun. Assign tiers: **Tier 1** pursue now, **Tier 2** cultivate over 6–12 months, **Tier 3** long-term or expansion-dependent.
- **A 90-day action plan** (CSV): Tier 1 targets with next step, owner role, deadline, and relationship path where one exists.
- **Strategic recommendations** covering diversification targets, mission-expansion options with trade-offs, and risk mitigation for government exposure.

For relationship paths based on board interlocks, use only person matches rated high confidence in Prompt 1's data. Keep candidate matches in the consulting materials, labeled as unconfirmed.

- **→ CP2.**

## Phase 4: Storyline

Write the narrative in Markdown before building any slides.

- **Leadership storyline** — the argument for Calvary's leadership and board, one line per slide: headline (a full-sentence takeaway), supporting evidence, and chart reference.
- **Consulting storyline** — the same for the consulting team deck, with full methods and evidence.

### Headline rules (apply to every slide in every deck)

- Every headline is a complete sentence.
- Every headline states the slide's main point or key takeaway. Topic labels ("Revenue Mix," "Peer Comparison") fail this rule; takeaways ("Government grants made up a growing share of Calvary's revenue over the period") pass it.
- Reading only the headlines, start to finish, tells the full story of the deck. Write the headline sequence first and test it on its own before adding slide content.
- The slide body proves the headline. Anything on the slide that does not support the headline moves to another slide or the appendix.

Save each deck's headline sequence as a standalone `headline_spine` Markdown file alongside its storyline.

## Phase 5: Build the deliverables

### Two audiences, two tracks

**Leadership and board track** — Calvary's executives and board. Clear, direct, and decision-oriented. Plain language, with one idea per slide. Lead with the verdict and the recommendations; keep methods brief and point to the consulting materials for depth. Target roughly 15–25 slides.

**Consulting team track** — the strategy team. Analytical and rigorous. Full methods, assumptions, sensitivity tests, data limitations, peer and network detail, and the complete scored pipeline. Length follows content.

### Deliverable set

I want a large body of material. Err toward producing more: more charts, more cuts of the data, more supporting detail. Adjust the split if the findings call for it, and explain any change at CP3.

**Executive one-pager**
- A single page for Calvary leadership that summarizes the funding-pressure verdict, the top opportunities, and the headline recommendations, and sets up the further analysis to come. Deliver it as a one-slide PPTX and as Markdown.

**Decks**
- Leadership and board deck
- Consulting deep-dive deck
- Appendix deck covering data and methods

**Appendix policy:** lean heavily on the appendix. Keep the main decks tight and move supporting analysis there: every module's full charts, additional cuts by universe and year, peer profiles, funder profiles, the full scored pipeline, network detail, sensitivity tests, data coverage, and methods. Each appendix slide follows the same headline rules. The appendix can be as long as the material warrants; split it into multiple files by topic if it grows large.

**Reports (Markdown)**
- Executive summary (2–3 pages, leadership audience)
- Full findings report (consulting audience, all modules)
- Methodology (sources, universes, methods, limitations)
- Recommendations (verdict, pipeline, 90-day plan, strategic options)

**Readouts (Markdown)**
- Board readout talking points
- Consulting team briefing

**Supporting files**
- Both storylines, the design system, analysis scripts, chart data, charts, module readouts, the insight register, the pipeline, the action plan, and the scoring config

Organize these new outputs in a clear structure that fits the existing project's conventions. Record where everything lives in the project README.

### Design system

The client template contains little beyond the logo, so create your own styles. Extract the logo (and brand colors, if the file has a usable palette), then design an original, clean, modern visual system for this engagement. Write the design system to a Markdown file before building slides: palette, typography, slide layouts, chart style, and how emphasis is shown.

- Choose the chart type that best fits each finding. Consider bar, line, slope, waterfall, small multiples, stacked area for revenue mix, network diagrams, Sankey flows for funding streams, and maps of Wards 7 and 8.
- Use native, editable PowerPoint charts for simple bar and line charts so the consulting team can edit them. Use high-resolution images for complex visuals such as networks and maps.
- Every chart slide gets a full-sentence headline, a source line naming the dataset, and an as-of date.
- Use the same visual system across all decks and reports.

### Visual QA

Render every deck to images (e.g., convert PPTX to PDF to PNG with LibreOffice) and inspect each slide for text overflow, overlapping elements, unreadable charts, inconsistent styling, and broken layout. Fix and re-render until clean.

Then run a headline check: extract every headline from each finished deck in order and read the list on its own. Confirm each headline is a complete sentence stating a takeaway and that the list tells the full story. Rewrite any headline that fails.

- **→ CP3.**

## Phase 6: Independent review

Run a separate review agent that has not seen the analysis process. Give it the input map, the deliverables, the insight register, and the clean tables. Its job:

- Check every number in every deck and report against the chart data and clean tables.
- Test whether each headline follows from its evidence, and whether each deck's headlines alone tell its full story.
- Flag overstated claims, missing caveats, and contradictions between documents.
- Confirm that board-interlock references in leadership materials use only high-confidence matches.

Write its findings to a review report, fix every issue, and record the fixes. Mark insights `verified` in the register once checked.

## Portability

The full project moves between machines and may be picked up by another Claude Code session.
- Markdown, CSV, PNG, and PPTX only.
- Relative paths everywhere; no usernames or absolute paths in any output.
- Analysis scripts rerunnable from the clean tables with a pinned requirements file.
- Update the project README with a section describing the analysis outputs, where they live, how to rerun them, and where to change the scoring weights. Keep `input_map.md` current.

## Definition of done

- All three checkpoints passed with my sign-off.
- Every approved module has scripts, chart data, charts, and a readout.
- The insight register is complete, with every insight verified.
- Recommendations include the verdict, the tiered pipeline, the 90-day plan, and strategic options.
- Decks, reports, and readouts exist for both audiences, pass visual QA, and pass the independent review.

---

## Optional: instructions for a review session (second model)

Use this section if a second model is brought in after the deliverables are complete. In that case your role is reviewer and strategist, and the existing outputs are your starting point.

1. Read the project README, `input_map.md`, `memory_reconciliation.md`, and Claude Code memory to orient yourself, then locate and read the analysis plan, the insight register, all module readouts, the recommendations report, and both storylines.
2. Challenge the analysis: identify findings that are weakly supported, alternative explanations, analyses that should have been run, and opportunities the pipeline missed.
3. Stress-test the recommendations: test each Tier 1 target and strategic option against the evidence and against Calvary's capacity.
4. Sharpen the storyline: propose a stronger argument structure and better headlines where warranted.
5. Write a second-review memo with your findings, ranked by impact, and **stop for my approval** before changing any deliverable.
