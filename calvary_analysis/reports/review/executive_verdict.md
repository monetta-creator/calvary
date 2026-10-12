# Executive verdict on the Calvary funding analysis

Independent review, 2026-10-10. One page. Detail in `audit_report.md`, `adversarial_review.md`, `review_findings.csv`.

## Ready for the board after specific fixes. Not ready as it stands.

**What is solid.** The data foundation and the arithmetic hold. Every module script reruns and regenerates the committed chart data; every number on the one-pager and the leadership deck, the full stress-test table and every pipeline score reproduce from the clean tables with independent code. The verdict's rating, moderate-to-high pressure driven by channel concentration and liquidity rather than by the government share, survives every alternative I could build: the TCP channel carries $1.8–2.2M of FY25 government revenue under any split, the FY25 deficit and 4.4 months of cash are real, and Calvary's peer rank (11th of 19, 12th after swapping three peers) supports "typical" better than the sector percentile does. Guardrails hold in every deliverable.

**What must change before the board sees it** (eighteen material rows in `review_findings.csv`, R01–R18; the five that change decisions first):

1. **Clark Charitable Foundation closed on 31 December 2025** (its own FAQ). It is the lead new-foundation target on the one-pager and Tier 1 row 3. Remove it and add a first-party "open to new applicants" check before any funder is named (R16, R17).
2. **The FY25 "event collapse" is a 990 presentation change.** Gala receipts moved from line 1c to line 8a; total event receipts were $596K in FY24 and $533K in FY25. The 2025 gala took place inside FY25. Drop "restore the event line", rebuild the $3M target without its +$0.4M events component, and close flag D3 (R15).
3. **The $960K DHS-loss figure is a point estimate the audited years contradict.** Streams are not drawn at a common rate (CoC drew 28–62% of its ceiling in FY22–23), so quote the stream-specific losses as ranges (DHS lost about $0.65–1.1M; combined about $1.05–1.5M) and keep the headline that the TCP channel is the cloud (R01, R14).
4. **Tier 1 and the named prospects.** America's Charities is a workplace-giving federation, not a foundation; Schattner and Abell are invitation-only; Cohen, Bernstein and The Washington Home depend on three provisional peers each. Tier 1 becomes nine rows with funder-specific steps (R06, R08, R10, R17).
5. **Labels on the leadership deck.** "74% of a $4.1M base" (78% on that base), "$2.49M → $4.97M, 2024 dollars" (nominal), "124 beds, 6.8% of TH beds" (two bases), the "57th percentile" method line (the comparison set is organizations that report a government line; against all filers Calvary is in the top quarter), and the one "high confidence" board link (not high) (R02, R03, R05, R07, R12, R13).

Also before release: redact one cached web snippet in `sources/web_tier1_guidelines.csv` that holds a contact's name and address (R04); regenerate the stale `full_findings.md` (R11); add the capacity evidence the data already holds, a six-person fundraising team and an unfunded workforce position, to the 90-day plan and the expansion slide (R09); and re-date the federal clouds (FY2026 CoC NOFO, EHV ends 31 December 2026, FY27 OVSJG restoration mostly one-time) (R18).

**Why "fixes", not "rework".** None of the eighteen items requires new data, a new model or a new storyline. Thirteen are wording, labelling or list edits; three (scenarios as ranges, the event story, the sector method line) are one-slide rewrites with the numbers already computed in this review; two (Clark, America's Charities) remove rows. The team's own machinery (edit config, rerun scripts, rebuild decks) can carry every fix, and the register's draft rows can then be marked verified. Expect one working day of edits plus deck rebuilds and a short re-verification pass on the changed slides.

**What I could not check.** Calvary's FY24–25 audits and TCP agreements (not public), the DC-500 FY2026 CoC priority listing (not posted), and the PNG charts as pixels (the data behind them reproduces).

**Credit where due.** The traceability design, the one-source-per-stream discipline, the audit-basis correction for government share, the honest handling of the three flags and the restraint of the leadership materials are better than most work of this kind. The errors found are the kind that a public-records analysis without the client's documents will make; the fixes are short.
