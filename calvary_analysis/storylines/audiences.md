# Audiences: who reads what, and what each needs

Every new deliverable names its audience from this file at Checkpoint A (`.claude/skills/new-deck/SKILL.md`). The audience decides the length, the tone, which data may appear and which checks run. When a piece serves two audiences, build it for the stricter one and put the rest in an appendix.

Data classes used below:
- **Public:** IRS filings, government award lists, budget books, HUD and Census data, funders' own web pages. Everything in `calvary_funding_data/clean/` except the rows marked internal.
- **Calvary-internal:** Calvary's own documents and records: the CRM export (`Foundation & Corporate Funders_2023-2026.xlsx` → `supp_crm_cash_verification`), the internal 2021–24 strategic plan report, Calvary's audits as supplied. Calvary may see them. Nobody else may.
- **Person-level:** `dim_person`, `fact_roles`, candidate interlocks, any named individual. Never shown by name in any deliverable. Board links appear only as organization pairs with a confidence label.

## 1. Calvary's CEO, as first reader

| | |
|---|---|
| Who | The CEO opens the work first and decides what goes to the board. Has no background in the method and limited time. |
| Decides | Whether the framing is fair to Calvary, what goes to the board, and which recommendations to pursue. |
| Time | 5 minutes for a first look, 20 minutes for a deck. |
| Needs first | Context before conclusions: who the 19 organizations are, what "funder" means here, what the data covers and leaves out, then the answer. The first two questions a newcomer would ask must be answered on the main surface, not behind a link. |
| Leave out | Scores, weights, method detail (move it to an appendix or an info panel). |
| Tone | What Calvary has built first, the clouds plainly with a path through them, options rather than prescriptions. No "exposed", "failure" or "dependency" as labels. |
| Data allowed | Public and Calvary-internal. No person-level data. |
| Existing pieces | `decks/pdf/executive_one_pager.pdf`, `reports/executive_summary.md`, `web/Calvary_Grantmaker_Web.html`. |

## 2. Calvary leadership and board

| | |
|---|---|
| Who | Calvary's board and senior staff, in a meeting or reading a pre-read. |
| Decides | Reserve policy, the private-revenue target, which expansion options to scope, who owns the Tier 1 asks. |
| Time | A 20–30 minute agenda slot, 22 headline slides at most. |
| Needs first | An executive summary in Situation–Complication–Resolution form, then one message per slide, and a closing slide that names the decisions needed. |
| Leave out | Medium-confidence board links. Funders whose open status is unverified. Peer-set-dependent names unless labelled. Pipeline scores. Anything that reads as a judgment on a peer organization. |
| Tone | As for the CEO. Credit the team where the data shows strength. |
| Data allowed | Public and Calvary-internal, the latter only when it changes a decision (for example staffing capacity). No person-level data. |
| Checks | Headline spine (`headline_check.py`, 20 words, no semicolons), sourcing footnote on every data slide, funder open status checked, numbers match the insight register. |
| Existing pieces | `decks/pdf/leadership_deck.pdf`, `reports/board_readout.md`, `storylines/leadership_*`. |

## 3. Development director and fundraising staff

| | |
|---|---|
| Who | The staff who make the asks. |
| Decides | Who to call this month, in what order, with what ask. |
| Time | Works from it for weeks. Wants lists, not argument. |
| Needs first | The funder, its status (open, invitation only, closed, channel), the deadline or cycle, the relationship path, the ask size and the owner. |
| Leave out | The verdict argument, peer benchmarks, method notes. |
| Tone | Practical and specific. Every row is actionable or labelled as not actionable. |
| Data allowed | Public and Calvary-internal (CRM matches are useful here). Person-level only as "a shared board member (unconfirmed)", never by name. |
| Checks | Open status and checked date on every named funder, deadlines from the funder's own page, sequenced for the team's capacity (six fundraising positions). |
| Existing pieces | `recommendations/action_plan_90day.csv`, `funder_pipeline.csv`, `decks/pdf/appendix_C_funders_pipeline.pdf`, the Grantmaker Web page. |

## 4. The consulting team

| | |
|---|---|
| Who | The engagement lead and volunteer colleagues who pick up and extend the work. |
| Decides | What to analyze next, what to recommend, what to fix. |
| Time | Reads everything; needs to be able to rerun it. |
| Needs first | The verdict and its evidence, then every module, the method, the caveats and the open items. |
| Leave out | Nothing analytical. Person names stay out here too. |
| Tone | Full analytical candor with the same courtesy toward Calvary and its peers. Medium-confidence items labelled "unconfirmed". |
| Data allowed | Public and Calvary-internal. Person-level only as IDs. |
| Existing pieces | `decks/pdf/consulting_deck.pdf`, `reports/full_findings.md`, `reports/methodology.md`, `reports/consulting_briefing.md`, `insight_register.csv`. |

## 5. Reference and review readers

| | |
|---|---|
| Who | Anyone checking a number: an independent reviewer, an auditor, a future analyst. |
| Decides | Whether a figure holds up. |
| Needs first | Complete tables, method notes, sources and how to rerun. |
| Rules | Appendix slides may use plain descriptive headers instead of action titles. Every table carries its source and method footnote. |
| Existing pieces | `decks/pdf/appendix_A..D_*.pdf`, `reports/methodology.md`, `reports/review/`. |

## 6. Funders and other outside readers (not yet produced)

| | |
|---|---|
| Who | A foundation program officer, a coalition partner or the public, reading something Calvary chooses to share. |
| Decides | Whether to fund or partner with Calvary. |
| Needs first | Calvary's case: need in Wards 7 and 8, what Calvary has built, outcomes, and what a grant would do. |
| Leave out | Everything internal: deficits framed as risk, the stress test, draw-down questions, pipeline scores and tiers, other funders' prospects, peer comparisons that rank named peers, CRM figures, the internal plan report, person-level data. |
| Tone | Calvary's own voice, approved by Calvary before it leaves. |
| Data allowed | Public only, plus anything Calvary explicitly approves. |
| Rule | Nothing goes to an outside reader without the engagement lead's and Calvary's sign-off. Run the guardrail scan (`reports/review/scripts/guardrail_scan.py` with `REVIEW_OUT` set to a scratch folder) first. |

## 7. Shareable pages

The Grantmaker Web page (`web/Calvary_Grantmaker_Web.html`) may be passed around, so it holds public filings only: no CRM data, no people, no board links, no pipeline tiers or scores. Funder status tags come from funders' own pages. Treat any new shareable page the same way.
