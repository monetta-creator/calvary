# Fix cycle: canonical wording and numbers (2026-10-11)

Every edit for `review_findings.csv` uses the statements below, so the decks and reports say the same thing. Numbers come from the rerun analysis (chart data and register as of 2026-10-11) unless a row says otherwise. Tone rules still apply: lead with what the data shows and what Calvary has built, state risks as clouds with a path, offer options, no semicolons in headlines, avoid "exposed", "failure", "dependency" as labels.

## Material findings

**R01 stress test as ranges.** Stream-level losses are ranges across three ways of splitting FY25 recognized government revenue across streams (ceiling share; CoC at its audited FY22-23 draw rate with DHS the residual; ceiling share without Sisters Rise). Canonical figures (`chart_data/m2_07_scenarios.csv`, `revenue_loss_low/high`):
- OVSJG -10%: $67K-$100K. OVSJG -25%: $168K-$250K. CoC -15%: $99K-$207K. One CoC project (New Foundations 2) lost: $204K-$424K.
- **DHS/TCP contract not renewed: about $0.65M-$1.13M a year (13-23% of revenue), leaving 1.9-2.4 months of cash after a year.**
- **Combined (OVSJG -25%, CoC -15%, DHS lost): about $1.05M-$1.47M (21-30% of revenue), leaving 1.5-2.0 months of cash after a year.**
- Say once where the DHS figure appears: the DHS point estimate depends on how revenue splits across streams; a floor case with OVSJG and CoC fully drawn nearly removes it. The headline stands: **the TCP channel is the cloud** (CoC and DHS together are $1.8-2.2M under every split).
- Replaces: "$960K", "$0.96M", "19% of revenue", "$1.31M", "$1.3M", "1.7 months" when they describe these scenarios.

**R02 TCP share.** Use one basis everywhere: **"about three-quarters (78% of the $4.1M 2024 award base)"**, footnote chart m2_01. Replaces "74%".

**R03 revenue growth.** **"$2.49M (FY19) to $4.97M (FY25) in nominal dollars, +59% after inflation"** (in 2024 dollars $3.05M to $4.84M). Never label $2.49M/$4.97M as 2024 dollars.

**R05 board links.** **"No high-confidence board links in public filings."** The one link once labelled high (Calvary and Clean Power Institute) spans board terms that never overlap and is now medium/unconfirmed; Clean Power Institute has no filed grants, so it is not a funder. Medium links stay in consulting materials only, labelled unconfirmed. Conclusion stands and is stronger: boards are a thin channel; paths run through shared funders and peers.

**R06 + R16 Tier 1.** Tier 1 is **nine rows**: five foundations (William S. Abell, Greater Washington Community Foundation, Cafritz, John Edward Fowler, Robert I. Schattner), three government streams (OVSJG; HUD CoC via TCP; DHS via TCP) and one corporate partner (MGAC). Replaces "eleven Tier 1", "11 Tier 1", "seven institutional".
- **America's Charities** is a workplace-giving federation already paying Calvary, not a grantmaker: a Tier 2 channel; step "confirm Calvary's enrollment in the CFC and employer campaigns and its designation code".
- **Clark Charitable Foundation** (legal name of the A. James & Alice B. Clark Foundation) **closed: its own FAQ says it was sunsetting and operational until 31 December 2025, and it takes no unsolicited proposals.** Remove it from every prospect list and next step. Where its money is described: "Clark's $7.8M to five peers and $32.8M to DC's sector in TY2020-24 were a spend-down; historic, now closed." It inflates the 2020-24 landscape and gap totals.
- Leadership materials name a funder only after its open status is checked on its own page (`config/guideline_notes.csv` `open_status`).

**R07 sector percentile.** **"57th percentile among DC human-services organizations that report government revenue; against all filers (no government line counted as 0%) Calvary is in the top quarter (84th in DC, 74th nationally)."** The "typical" claim leans on the peer rank: **11th of 19** DC-area organizations.

**R08 + N03 upgrade steps.** Template ("multi-year general-operating grant at the funder's peer-level amount") fits **Cafritz** ($170K to Calvary vs $250K largest to a peer) and **Fowler** ($40K vs $50K) only.
- **Abell: steward and renew.** Largest grant to Calvary **$270K (TY2021)**; latest filed grant $25K (TY2023); Calvary's records show a further $25K in March 2025. Abell is invitation-only with no consecutive-year requests: ask its staff when a next request is welcome and what it would fund. (The review's "$270K in TY2023" read two fields together; corrected as N03.)
- **GWCF: two conversations.** A successor to the Health Equity Fund support behind its $458K, and a core general-operating request.

**R09 capacity.** Calvary held its fundraising staff at **six positions** with limited growth over 2021-24, and **its second workforce position is unfunded in FY2026** (Calvary's 2021-24 strategic plan report; internal document, use in Calvary-facing materials only). The 90-day plan is sequenced for that team: month 1 government confirmations (CEO and board chair), month 2 two current-funder conversations a fortnight (development director), month 3 introductions. In the expansion options, funding the workforce position is the first cost of the workforce option.

**R10 peer-set sensitivity.** Three funders give to **four or more peers: Schattner, Bunting Family Foundation, Brendan & Helen Bechtel Foundation** (Clark is closed). **Only Schattner is named as a new prospect in leadership materials** (Tier 1, typical grant $60K, invitation-only). Bunting and Bechtel are Tier 3 (typical grants $10K and $25K, little other DC giving, no public application process; checked 2026-10-11): describe them, if at all, as "two smaller family foundations that fund four peers" and never as plan targets. Three-peer names (Cohen, Bernstein, The Washington Home and nine others) are labelled **"depends on the provisional peer set"**; swapping three provisional peers drops them and moves Calvary from 11th to 12th of 19. Cohen is also invitation-only. Confirm the peer set with Calvary before outreach.

**R11 full findings.** `reports/full_findings.md` is regenerated from the current register, module readouts and chart data; the orphan chart id `m1_04_surplus_net_assets` is removed (its CSV is deleted).

**R12 beds.** **"124 beds across transitional, permanent supportive and rapid-rehousing programs; its 94 transitional beds are 6.8% of the District's."** For 2022 (not 2019): 68 beds in all programs (45 transitional, 16 permanent supportive, 7 rapid-rehousing); the 45 transitional beds were 2.5% of the District's.

**R13 channels on the leadership peer-funder slide.** Of the 23 funders that give to three or more peers but not Calvary, **six are channels** (Gifts for the Homeless, T. Rowe Price Program, Capital Area Food Bank, America's Charities, JPMorgan Chase matching gifts, Give Lively), **Clark has closed and Venable is closed to new applicants**; **15 choose their own grantees.** Leadership chart shows grantmakers only, or says so in one bullet.

**R14 draw-down.** The audited FY22 and FY23 single audits already show CoC expenditure at **28% (FY22) and 58% (FY23)** of the prior year's CoC award ceilings, so the gap is specific to the CoC stream and predates FY24 (the 2021 Reach Up expansion award, $1.22M reallocated to $0.42M in 2022, explains part). Recommendation 1 reads: **"reconcile CoC draw-down first (the audited years already show the gap there), then DHS."** Confidence stays medium.

**R15 events.** **"Event receipts held near $0.53-0.60M (FY24 $596K, FY25 $533K); the FY25 990 presented gala receipts as fundraising-event income (line 8a, with $259K of direct costs netted) instead of contributions (line 1c)."** The 2025 gala took place on 23 April 2025 (inside FY25) and the 2026 gala raised over $620K. Drop "restore the event line" from opportunities and the 90-day plan (keep "confirm the FY26 gala date" as a small check). **The $3.0M private-revenue target stands on new arithmetic: from about $2.1M (FY25) via institutional upgrades and peer-funder introductions +$0.5M, major-donor and DAF giving +$0.3M, and earned or billable program revenue +$0.1-0.3M (optional), which is +$0.9-1.1M; events held near $0.5M, so no restoration component.** Flag D3 is closed (resolved from the 990 itself). The deficit (-$607K) and cash (4.4 months) facts stand; replace "FY25 thinned the cushion" language with those facts. Replaces "$483K event-income drop", "event collapse", "$0.8M contributions drop" explanations.

**R17 open status.** First-party pages, October 2026: **Schattner** does not consider unsolicited requests; **Abell** invitation-only; **Venable** accepts DC applications only from grantees of the last two years or invited organizations (closed to new applicants; Calvary qualifies only if its recent gifts came from the Foundation rather than the firm); **Meyer** closed to new applicants in 2026. For invitation-only funders the step is **"secure an invitation through a named peer or co-funder; no LOI"**. Slide 20 shows open status.

**R18 federal and DC dates (October 2026).** The FY2025 CoC NOFO was enjoined and FY2025 renewals were paid in full; **the live exposure is the FY2026 CoC NOFO** (protected renewals 60% of demand, a $1.3B transitional-housing and services set-aside, applications closed 30 September 2026, awards expected about December 2026, litigation pending). **HUD's 29 September 2026 notice ends the EHV program**: families leased on 30 September 2026 convert to non-reissuable tenant-protection vouchers by 31 December 2026, so Sisters Rise's voucher base cannot be rebuilt. **The FY2027 OVSJG restoration is $5.1M one-time plus $0.5M recurring**, so the FY2028 base is exposed again. Each strengthens "the TCP channel" and "the spring budget season" messages.

## New findings from the fix-cycle test

**N01 World Bank Community Connections Fund** is not a lapsed funder: its one filed grant to Calvary was a **one-time $100K capital-campaign grant (TY2022)**, and staff giving through the fund continued to July 2026 in Calvary's records. It is an employee-giving channel. **Lapsed funders are now 11, who once gave $0.16M ($156,150)** (replaces "12", "$255K", "$256K", "$0.26M").

**N02 Many Hands** requires an operating budget of $500K-$5M; Calvary spent $5.58M in FY2025, so **it is not eligible for the January 2027 cycle** unless both FY2026 actual expenses and the FY2027 budget fall to $5M. Remove it from re-engage steps.

## Minor findings

- **M01** "22 of 23" where the 23 three-peer funders are counted as itemized/supportable.
- **M02** Two Baltimore funders' grants to a Baltimore namesake ($131,906) are excluded (`config/grant_exclusions.csv`); the network now has **328 funders** (was 330) and $69.9M; My Sister's Place's institutional figures fall slightly.
- **M03** Pipeline rules now documented in `config/scoring_weights.yaml` (DAF-like channels capped at Tier 2; typical-grant fallback; current funders under $10K dropped). Consulting slide 47 says so.
- **M04** Chart-data source tables complete; orphan CSV deleted; footnotes fixed where they cite m2_01 for the TCP share (now correct basis) and on leadership slide 22.
- **M05** Counts: leadership deck **22 headline slides plus 4 dividers (26 slides)**; appendix decks **22, 21, 70 and 33 slides** (Appendix C gained a page when the status column was added).
- **M06** The 2019 OVSJG value adds two Reach Up records ($292,000 and $368,935) that may be one award recorded twice; series quoted from 2020 ($0.6M), with a footnote on 2019.
- **M07** Fix in place: "21 organizations" (not 20) in the benchmark; lapsed total per N01; DWC grew **5.5x since FY2014** ($6.3M to $34.4M) and **3x since FY2018** ($11.6M), never "6x"; "280 names" means both 2023 lists combined; "Benevity, Fidelity and Schwab add $0.95M" ($1.1M is all eight DAF sponsors).
- **M08** Bank of America and JPMorgan Chase are labelled **matching-gift channels** with a corporate-relationship path (no tier change).
- **M09** TCP is excluded as a **pass-through intermediary**; there is no itemized TCP Schedule I list to fall back on, so TCP agreements are the only route to FY25-26 DHS values.
- **M10** Headline check has an appendix mode (`--appendix=A..D`); appendix reference headers are exempt from the word limit and spine drift is a warning.
- **M11** Pointers to `reports/review_report.md` now point to `reports/review/`.
- **M12** Median grant: **"under $1K"** ($570 over 601 grant rows).
- **M13** Slide 39 states the filter: **"among current funders that also fund two or more peers"** (20 over all current institutional funders; 27 with DAF sponsors).
