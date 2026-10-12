# Adversarial review: is the work right?

Independent review (Prompt 3, Pass 2), 2026-10-10. Built on the audited numbers in `audit_report.md` and the row-level findings in `review_findings.csv`. Paths are relative to `calvary_analysis/`. Evidence files are in `evidence/`; recomputation scripts in `scripts/`.

Materiality bar (fixed before the review): a number on the one-pager or leadership deck that is wrong or unsupported; a Tier 1 or Tier 2 membership change; a change to the verdict or its rating; a stress-test loss that moves more than 10%; a 90-day action Calvary cannot take as written; any people-data breach.

## 1. Material challenges, ranked by their effect on Calvary's decisions

### C1. The lead new-foundation target closed ten months ago (R16)

**Claim.** Clark Charitable Foundation is the first new foundation to open: $7.8M to five peers, median grant $250K, warm introduction, LOI by day 90. It is on the one-pager, leadership slides 2, 16, 19 and 20, and in every report.

**Challenge.** Clark Charitable Foundation Inc. (EIN 521512330) is the legal name of the A. James & Alice B. Clark Foundation. Its own FAQ page says it "is in the process of sunsetting and will be operational until December 31, 2025" and does not accept unsolicited proposals. I fetched the page myself. The TY2020–24 grants in the data were the spend-down. The web pull logged "no usable hit" for Clark and the analyst note still sent it to the top of the list.

**Confidence.** High.

**Fix.** Remove Clark from Tier 1 and every prospect list; label its $32.8M in the landscape as historic and closed; add an "open to new applicants (first-party, date)" column to `config/guideline_notes.csv` and require it before any funder is named in leadership materials. With C3 below, Tier 1 falls from eleven rows to nine.

### C2. The FY25 "event collapse" is a 990 presentation change (R15)

**Claim.** Event contributions fell from $538K to $55K, the largest single private swing; it may be a calendar change; restore the event line to the FY24 level; events supply +$0.4M of the $3M private-revenue target.

**Challenge.** The clean table already holds the answer. In FY25 Calvary reported $477,959 of gala receipts on line 8a (gross fundraising-event income, kept in `fact_org_financials.notes`) instead of line 1c, netting $259,371 of direct costs on line 8c (+$218,588). Total event receipts:

| FY | line 1c | line 8a gross | total receipts | line 8c net |
|---|---|---|---|---|
| 2023 | $457,758 | $61,170 | $518,928 | −$149,059 |
| 2024 | $538,070 | $57,780 | $595,850 | −$177,248 |
| 2025 | $54,730 | $477,959 | $532,689 | +$218,588 |

The dip is $63K, not $483K. The 2025 gala took place on 23 April 2025, inside FY25, and the 2026 gala raised over $620K (public record). The reclassification also explains about $420K of the "$0.8M contributions drop" and about $259K of the fall in reported revenue; expenses move by the same amount, so the $607K deficit and the 4.4 months of cash stand.

**Confidence.** High.

**Fix.** Rewrite the FY25 story (deficit and cash are real; the event line is not), drop "restore the event line" from the opportunities and the 90-day plan, rebuild the $3M target without the +$0.4M events component or state where it comes from instead, and close flag D3 as resolved from the filing.

### C3. The stress-test point estimates rest on an apportionment the audited years contradict (R01, R14)

**Claim.** Losing the DHS/TCP contract costs $960K (19% of revenue); CoC −15% $178K; one CoC project $366K; combined $1.31M. FY25 government revenue is split across streams by award-ceiling share (OVSJG 23%, CoC 41%, DHS 33%).

**Challenge.** The split assumes every stream is drawn at the same rate. The audited SEFA in FY22 and FY23 shows CoC expenditure at 28% and 58% of the lag-1 CoC ceiling (62% and 34% at lag 0), while recognized government revenue exceeded the known non-DHS ceilings in both years. Streams are not drawn evenly, and the CoC under-draw predates FY24. Four defensible splits of FY25 recognized government revenue:

| Scenario | A team: ceiling share | B: OVSJG full, CoC at SEFA draw rate, DHS residual | C: Sisters Rise gone, ceiling share | D: OVSJG and CoC full, DHS residual |
|---|---|---|---|---|
| S3 CoC −15% | $178K | $99K (−44%) | $207K (+16%) | $264K (+48%) |
| S4 one CoC project | $366K | $204K (−44%) | $424K (+16%) | $542K (+48%) |
| S5 DHS lost | $960K | $1,125K (+17%) | $650K (−32%) | $26K (−97%) |
| S6 combined | $1,306K | $1,474K (+13%) | $1,052K (−19%) | $540K (−59%) |

Every stream-specific loss moves by more than the 10% bar under at least one defensible alternative. What survives every split: CoC plus DHS (the TCP channel) carries $1.8–2.2M of FY25 government revenue, so "protect the TCP channel first" is right. Also, the "two-thirds recognized" question on slide 11 is presented as new and answerable only by Calvary's audits; the FY22–23 SEFA already locates the gap in the CoC stream (the 2021 Reach Up expansion award of $1.22M, reallocated to $0.42M in 2022, is part of the story).

**Confidence.** High that the point estimates are unsupported; medium on which alternative is closest (B and C are the most defensible).

**Fix.** Show S3–S6 as ranges (DHS lost about $0.65–1.1M; combined about $1.05–1.5M) or re-apportion with the SEFA draw rate for CoC and a residual for DHS; add the FY22–23 SEFA comparison to slide 11; keep "the TCP channel is the cloud" as the headline; reframe recommendation 1 as "reconcile CoC draw-down first".

### C4. "Typical for the sector" depends on a comparison set the deck misdescribes (R07)

**Claim.** Calvary sits at the 57th percentile of DC's human-services sector (median 37%, n=163) and the 57th and 46th percentiles nationally; method: organizations with no government line counted at 0%.

**Challenge.** The script keeps only organizations whose 990 reports a government line and drops the rest (990-EZ filers and 990 filers with a null line). That is the opposite of the stated method. Under the stated method Calvary is at the 84th percentile in DC and the 74th in both national universes, with medians near zero:

| Universe, year | as shown (orgs with a government line) | all filers, no line = 0% | orgs with government > 0 |
|---|---|---|---|
| DC sector FY2023 | n=162, median 37%, Calvary 57th | n=425, median 0%, Calvary 84th | n=140, median 51%, Calvary 51st |
| Size-matched FY2022 | n=333, median 55%, 57th | n=555, median 3%, 74th | n=294, median 61%, 51st |
| National women's FY2022 | n=541, median 65%, 46th | n=1,123, median 0%, 74th | n=434, median 72%, 33rd |

The numbers shown are right for the set actually used, and that set is a reasonable one ("organizations that take government money"). But the method line is wrong, and a board member who asks "typical compared with whom?" deserves the answer. The peer rank (11th of 19, 12th after a peer swap) is the stronger support for "typical" and is unaffected.

**Confidence.** High on the fact; medium on impact.

**Fix.** Correct the method line; say "among organizations that report government revenue" on slide 4; add one sentence in the consulting deck that against all filers Calvary is in the top quarter of government reliance; lean the "typical" claim on the peer rank.

### C5. Tier 1 and the named prospects are less robust than the sensitivity slide says (R06, R10, R17)

**Claim.** Moving any weight by 0.05 changes ranks but not the ten institutional names in Tiers 1–2; eleven Tier 1 targets; open Schattner, Cohen, Bernstein, The Washington Home.

**Challenge.** Three tests the team did not run:

- **Peer swap** (Community of Hope, Covenant House DC and Heartly House out; Pathways to Housing DC, Volare and Carpenter's Shelter in; scripts 03–07 rerun in a scratch mirror): Calvary's rank 11 → 12 of 19; America's Charities leaves Tier 1 (0.638 → 0.608); the 3+ peer gap list loses Cohen, Bernstein, The Washington Home, Pew, Kaplan and Collins and gains Marriott, Holland-Iribe and Morrison & Foerster; Tier 2 loses Jane Bancroft Robinson and Omidyar, gains Annie E. Casey and Revada. Verdict, months-of-cash rank (5th) and institutional-depth rank (2nd) unchanged.
- **Alternative weightings** (`evidence/pipeline_alt_weights.md`): America's Charities drops from Tier 1 under three of six schemes and when its relationship score is set to 0.5; Weinberg (Maryland-focused) enters under relationship-light weights; raising the Tier 1 award floor to $50K leaves only Clark and Schattner among institutional rows. Tier 1 is driven by the $25K award floor and the current-funder bonus more than by the weights.
- **First-party access** (October 2026 pages): Schattner and Abell are invitation-only; Venable accepts DC applications only from recent grantees or invitees; Meyer was closed to new applicants in 2026. The "request guidelines / submit an LOI" step does not exist at these funders.

America's Charities is the clearest problem: a workplace-giving federation already paying Calvary, labelled "foundation" on leadership slide 20 with an LOI next step.

**Confidence.** High.

**Fix.** Move America's Charities to a channel line; on leadership materials name only funders of four or more peers (Clark excepted as closed; Schattner, Bechtel, Bunting qualify) or label three-peer names as peer-set-dependent; replace "submit an LOI" with "secure an invitation through a named peer or co-funder" for invitation-only funders; mark Venable and Meyer closed to new applicants.

### C6. The plan does not use the capacity evidence the data holds (R08, R09)

**Claim.** Eleven targets each have an owner and a deadline; upgrade asks at the funder's peer-level amount; formalize workforce with a SheWorks-style cohort inside Step Up DC.

**Challenge.** `supp_calvary_strategic_targets` records that fundraising staff were held at six with limited growth over 2021–24 and that the second workforce position is unfunded in FY2026. No deliverable uses either fact. The plan gives the development director six Tier 1 asks, three lapsed-funder calls and the event rebuild inside 90 days, and recommends growing the program Calvary just defunded. Two of the four "upgrade" asks are not upgrades: Abell's largest grant to Calvary is $270K (TY2023) against a $25K median and $225K maximum to peers; GWCF's $458K is Health Equity Fund money.

**Confidence.** High that the evidence is unused; medium on how much it changes the plan.

**Fix.** Add a capacity line and sequencing to slide 19 and the action plan; write funder-specific steps for Abell (steward and renew after the 2023 grant) and GWCF (Health Equity Fund successor plus core support); note the unfunded workforce position as the first cost of the workforce option.

### C7. One high-confidence board link is not high confidence (R05)

**Claim.** One high-confidence shared-board link (Clean Power Institute), not with a funder.

**Challenge.** The label rests on a middle initial and same metro; the tenures (2019–21 vs 2023–24) do not overlap and the first+last name appears on other person rows. The organization has no grants to anyone in the data, yet its funder flag is "yes" in the consulting deck and appendix C (universe membership) and "no" in the leadership deck. Relabelling it medium leaves Calvary with no high-confidence board links in filings, which makes the slide's point (boards are a thin channel) stronger, not weaker.

**Confidence.** High.

### C8. Three dated claims need re-dating (R18)

The FY2025 CoC NOFO shift was enjoined and FY2025 renewals were paid in full; the live exposure is the FY2026 NOFO (protected renewals cut to 60% of demand, applications closed 30 September 2026, awards expected about December 2026, litigation pending). HUD's 29 September 2026 notice ends the EHV program on 31 December 2026 with non-reissuable tenant-protection vouchers, so Sisters Rise's voucher base cannot be rebuilt. The FY2027 OVSJG restoration is $5.1M one-time plus $0.5M recurring, so the FY2028 base is exposed again. None contradicts the verdict; each belongs on slides 9, 15 and 22 and in the advocacy calendar. The Health Equity Fund has about $10M of $95M uncommitted and no successor announced (the deck's "ask about a successor" is right; "no successor announced" is more accurate).

### C9. Presentation errors on the leadership deck (R02, R03, R12, R13)

"74% of a $4.1M award base" mixes bases (78% on the $4.1M base; 74% on the $4.3M FY25-aligned ceilings). Slide 3 labels nominal revenue as 2024 dollars. "124 beds, 6.8% of DC's transitional-housing beds" mixes all bed types (124) with transitional only (94). Slide 16's prospect chart is led by in-kind and workplace channels without the caveat the consulting deck carries. Each is a one-line fix; each is a number a board member could check and find wrong.

## 2. Judgment calls tested (2a)

| Judgment call | Test | What moved | Ruling |
|---|---|---|---|
| Verdict weights channel concentration and liquidity over the share | Re-read against every recomputed number; alternative stories below | Nothing: concentration (TCP $1.8–2.2M of FY25 government revenue under every split), FY25 deficit and 4.4 months of cash all reproduce | Holds |
| Line 1e as audit-equivalent for FY24–25 | Audit vs 1e in FY22–23 (equal); program-service revenue FY24–25 (zero); FY21 anomaly | No sign of contracts booked outside 1e in FY24–25; the FY21 case remains the caveat | Holds, with the caveat stated |
| CoC lagged one year; DHS FY2024 carried forward | SEFA CoC expenditure vs lag-0 and lag-1 ceilings FY22–23 | Neither lag reproduces expenditure (28–62%); the ceiling is not a proxy for recognized revenue | Alignment is reasonable; using ceilings as the apportionment key is not (C3) |
| Apportionment by ceiling share; 50% cost avoidance; severities | Four alternative splits; months-of-cash formula | S3–S6 move 13–97% (C3); the net-cash formula reproduces; 50% is a stated parameter | Fails on the split; the parameter and severities are defensible |
| One source per stream | Rows summed across source_type anywhere? | None found; OVSJG 2019 sums two records from the same source (minor M06) | Holds |
| Gates and TCP exclusions | Gates recipients in dc_sector; TCP Schedule I rows | Gates exclusion justified; TCP has one Schedule I row ($3M, TY2023), so the rationale text is wrong but the exclusion is harmless (M09) | Holds; reword |
| T. Rowe Price as a DAF channel; DAF channels out of the pipeline | Tier rule check; its score 0.624 and $25K typical would qualify for Tier 1 | Capped at Tier 2 by a script rule not in the yaml (M03) | Holds; document |
| Weights and tier cutoffs | Six alternative schemes plus a relationship-score test | America's Charities fragile; Weinberg and World Bank CCF enter under some schemes; award floor dominates | Tier 1 holds except America's Charities and Clark; say that the floor, not the weights, drives Tier 1 |
| Provisional peer set | Three peers swapped, scripts 03–07 rerun | Rank 11 → 12; America's Charities out of Tier 1; six three-peer names leave the gap list | Verdict holds; named three-peer prospects do not (C5) |
| Guideline rows with no usable hit; basis labels | First-party pages fetched for nine funders | Clark closed; Abell and Schattner invitation-only; Venable and Meyer restricted; Cafritz, Fowler, Many Hands, America's Charities confirmed | "No usable hit" rows carried the two largest errors (C1, C5) |
| Filing lag in TY2024 | Itemized-TY2023+ test; CRM cross-check | Test works (22 of 23, not 23); Venable and America's Charities are in the CRM, so "lag" is right for them; "flat since TY2023" remains partly lag | Holds; fix the count |

## 3. Execution realism (2b)

| Tier 1 target | Ask vs peer median | Cycle fit in 90 days | Owner load | Path in the data | Verdict |
|---|---|---|---|---|---|
| Abell | Calvary already receives far above the $25K median ($270K in TY2023) | Invitation-only; no consecutive-year requests | Development director | Current funder, CRM | Steward, do not "upgrade" |
| GWCF | $458K is Health Equity Fund; core median $33K | Fund-specific cycles; HEF about 88% committed, no successor announced | Development director | Current funder; gala honoree relationship (public record) | Right target, wrong ask text |
| Clark | — | Closed 31 Dec 2025 | — | — | Remove |
| Cafritz | $170K vs $250K peer max | 1 Nov or 1 Mar deadline; one application per 12 months | Development director | Current funder | Fits |
| Fowler | $40K vs $50K | Rolling | Development director | Current funder | Fits (small headroom) |
| OVSJG, CoC, DHS via TCP | — | Day 30 confirmations | CEO + board chair | Existing | Fits |
| MGAC | CRM $713K cumulative, cash vs in-kind unknown | — | CEO + board chair | CRM | Fits as a stewardship step |
| Schattner | $60K median | Does not consider unsolicited requests | Development director | Four peers | Introduction, not LOI |
| America's Charities | Donor-designated pass-through | Campaign enrollment | Development director | Already in CRM | Not a grant target |

The 90-day plan has no calendar anchor, so cycle fit cannot be judged for Bank of America (2027 dates unposted), United Way NCA (September pre-screen) or Venable (1 February). Anchor the plan to a start date. The development director's load (six asks, three re-engagement calls, the event rebuild) is heavy for a six-person fundraising team that the strategic-plan report describes as held flat.

## 4. Missed or underrated opportunities (2c)

- **Many Hands** is confirmed open (applications 4–15 January 2027), Calvary is eligible ($79.5K cumulative, under the $100K cap), the Impact Grant is $100K+. It sits in Tier 2 behind closed or invitation-only names. A judgment fix: promote it to the day-60 list.
- **The two swap-in peers' funders.** Swapping peers surfaced Marriott, Holland-Iribe and Morrison & Foerster as three-peer funders; Morrison & Foerster is already in Calvary's CRM ($74K). A data fix: the gap list should be run on a broadened or confirmed peer set before outreach.
- **Weinberg** has the highest mission fit in Tier 2 and enters Tier 1 under relationship-light weights; its small-grants program is Maryland and Pennsylvania only, so this is a weight artefact, correctly scored low on access. No change.
- **DHS PSH expansion (GOV-DC-3, Tier 2)** is underrated relative to the Clark-shaped hole: the local PSH budget is $145–166M, Calvary holds 16 PSH units, and the FY2026 CoC NOFO's set-aside favours transitional housing and services, which is Calvary's model. A judgment call for the team, not a scoring error.
- **Government share by channel.** The team's best single improvement would be to ask Calvary for the TCP subgrant agreements and to split line 1e by stream in the audits (the FY22 and FY23 audits already contain SEFA CoC lines the analysis did not use). This is a data gap with a cheap fix.

## 5. External reality check (2d)

Sixty-five pages logged in `evidence/external_sources.csv` (registry-extension format; no identifiers in any query). Summary: Health Equity Fund QUALIFY (about $84M of $95M committed; no successor or wind-down announced); CoC QUALIFY (re-date to FY2026); EHV CONFIRM with update (program ends 31 Dec 2026); OVSJG FY26–27 CONFIRM (restoration mostly one-time); DHS continuum QUALIFY ($206M and $194M confirmed; the $170M FY2025 figure needs its basis stated, actual was $178.8M; the TCP purchase-order claim has no public corroboration); foundations mixed (Clark CONTRADICT; Abell, Schattner, Venable, Meyer QUALIFY; Cafritz, Fowler, Many Hands, America's Charities CONFIRM); Calvary news NOT FOUND beyond gala dates and amounts and a board-officer change.

## 6. Alternative stories (2e)

**(i) The pressure is lower than stated.** The FY25 private drop is mostly a 990 presentation change: event receipts were flat at $0.53–0.60M, and about $420K of the "contributions down $0.8M" is the same reclassification. The "two-thirds recognized" gap is partly an artefact of using award ceilings for a stream (CoC) that has never been drawn near its ceiling, and partly the carry-forward of a Sisters Rise contract whose voucher program had already ended; take Sisters Rise out and FY25 recognition is 78% of ceilings and the combined worst case falls to about $1.05M. DC's pools are flat to rising, the Council has restored every cut, and filed institutional grants are not flat but oscillating upward ($0.64M in TY2020 to $1.17M in TY2024, partial). On this reading the verdict should be "moderate".

**(ii) The pressure is higher than stated.** Against all filers in its sector Calvary is in the top quarter of government reliance, not at the median. The TCP channel carries $1.8–2.2M of FY25 government revenue under every split, and both its streams face dated federal shocks: the EHV program ends on 31 December 2026 (so Sisters Rise's $593K is gone, not at risk), and the FY2026 CoC NOFO cuts protected renewals to 60% of demand with awards due about December 2026. The FY2027 OVSJG restoration is mostly one-time. The lead new-foundation prospect is closed, the Health Equity Fund (27% of five years of filed grants through GWCF) is 88% committed with no successor, three of the other named prospects are invitation-only, the fundraising team is flat at six, and the baseline already burns $50K a month. On this reading the verdict should be "high".

**(iii) The pipeline is pointed at the wrong funders.** Tier 1 is four current funders (two of which cannot be "upgraded" as written), three public streams Calvary already holds, one corporate relationship, a closed foundation, an invitation-only foundation and a workplace-giving federation. The scoring rewards peer count and relationship, so it surfaces funders Calvary already has and channels that are not grantmakers, while the only confirmed open window with a six-figure grant (Many Hands) sits in Tier 2 and DHS PSH expansion sits at 0.55. The right list is shorter: GWCF (successor conversation), Cafritz (1 March), Fowler, Many Hands (January), introductions to Schattner and Abell, and a PSH expansion project in the FY2026 CoC and DHS processes.

**Ruling.** The evidence supports parts of (ii) and (iii) and the first half of (i). The rating "moderate-to-high, driven by channel concentration and liquidity" survives: the concentration is real and now better dated, and the cash facts stand. Two components of the story do not survive: the event collapse (a presentation change) and the Clark-led new-foundation list. The pipeline is not pointed at the wrong funders so much as at a few that cannot be approached as written; after removing Clark and America's Charities and rewriting the Abell and GWCF steps, the remaining list is sound. I would not change the rating. I would change what the deck says is new in FY25, how the DHS loss is quoted, and who is on the first page.

## 7. What a skeptical reader will ask

- "You say typical. Typical compared with whom?" Answer with the peer rank and the corrected method line (C4).
- "Clark closed last year. Who checked the list?" Answer with the new first-party column (C1).
- "Where did the gala money go?" Answer with the line 8a figure (C2).
- "Is $960K a forecast?" Answer with the range and the SEFA evidence (C3).
- "Who is going to do all this by day 45?" Answer with the capacity line (C6).
