# M7 readout: opportunity pipeline and scoring

Script `scripts/07_m7_pipeline.py`; weights and tier cutoffs in `config/scoring_weights.yaml`. Outputs `recommendations/funder_pipeline.csv` (also `chart_data/m7_00_funder_pipeline.csv`) and `recommendations/action_plan_90day.csv`; charts `m7_02_pipeline_scores`, `m7_03_tier1_score_breakdown`. Insight M7-01.

## Question
Which funders and programs should Calvary pursue first, and on what evidence?

## Method
Candidate base = M5 (current funders with headroom, lapsed funders, peer-funder gaps, DC-sector majors) joined to M6 relationship paths and the M4 landscape. DAF sponsors are excluded (a channel, not a grantmaker); the T. Rowe Price Program is scored like a DAF. Current funders that gave Calvary under $10K over TY2020–24 are dropped before scoring. Seven dimensions scored 0–1, weighted (mission fit 0.20, peer giving 0.20, regional giving 0.10, award size 0.15, accessibility 0.10, durability 0.10, relationship 0.15):

| Dimension | Evidence |
|---|---|
| Mission fit | funder issue tags (housing/DV/women = 1.0; behavioral health/workforce/health 0.7; general operating 0.6) plus the share of its DC-sector dollars whose purpose names housing/DV/women |
| Peer giving | core peers funded TY2020–24, capped at 8 |
| Regional giving | dollars to DC-sector organizations, log scale $50K → $10M |
| Award size | median grant to peers (else median DC-sector grant, then Calvary's largest grant), log scale $5K → $250K |
| Accessibility | funder type and breadth (community foundation 0.85; public charity grantmaker 0.75; private foundation 0.70 / 0.50 / 0.30 by number of DC recipients); −0.15 for "see attached" filers; −0.30 for in-kind or workplace-giving channels |
| Durability | years funding peers and years active in the DC sector |
| Relationship | M6 path strength + 0.35 current funder + 0.20 lapsed + 0.15 on Calvary's CRM/lists |

Tiers: **Tier 1** score ≥ 0.62 and typical grant ≥ $25K (max 20); **Tier 2** score ≥ 0.48; **Tier 3** the rest. Channels (DAF-like, workplace, matching-gift, in-kind, online and employee giving) and funders closed to new applicants are capped at Tier 2; closed funders are kept in the file for the record (Tier 3, track "excluded: closed funder"), never as prospects; funders Calvary is not eligible for sit in Tier 3 with the reason. Status comes from `open_status` in `config/guideline_notes.csv`, checked on each funder's own page (October 2026). These rules are documented in `config/scoring_weights.yaml`. Government rows (OVSJG, DHS/TCP, HUD CoC, DHS PSH, HUD CPF) and corporate CRM relationships (≥$50K, no public filing) carry analyst scores (basis = inferred). Federal Grants.gov notices are Tier 3 by default.

## Result (182 rows; Tier 1 = 9, Tier 2 = 39, Tier 3 = 134)
| Track | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|
| Institutional: steward / upgrade | 4 (Abell, GWCF, Cafritz, Fowler) | 9 | 22 |
| Institutional: new | 1 (Schattner) | 10 (The Washington Home, Cohen, Viragh, Arlington CF, Coca-Cola, Morrison & Foerster, Eugene B. Casey, ImpactAssets; Venable and Meyer, closed to new applicants) | 97 |
| Channels | – | 8 (T. Rowe Price Program, donor-advised; America's Charities, workplace giving; JPMorgan Chase and Bank of America, matching gifts with a corporate-relationship path; Gifts for the Homeless and Capital Area Food Bank, in-kind; Give Lively, online giving; World Bank CCF, employee giving) | – |
| Closed or not eligible | – | – | 3 (Clark, closed; Weinberg and Many Hands, not eligible) |
| Corporate (CRM) | 1 (MGAC) | 10 (Frontier Co-op, IMF, Reservoir, Latham & Watkins, UnitedHealth, …) | – |
| Government DC | 2 (OVSJG grants; DHS/TCP contracts) | 1 (DHS PSH expansion) | – |
| Government federal | 1 (HUD CoC via TCP) | 1 (HUD CPF renewal) | 12 opportunities |

**Tier 1 (9 rows):** five foundations, three government streams and one corporate partner: Abell (0.86), GWCF (0.85), OVSJG (0.80), Cafritz (0.78), HUD CoC via TCP (0.78), DHS/TCP (0.72), Fowler (0.72), MGAC (0.70, corporate), Schattner (0.67). Clark Charitable Foundation (the A. James & Alice B. Clark Foundation) would score 0.82 but has closed: its own FAQ says it was sunsetting and operational until 31 December 2025, and it takes no unsolicited proposals. America's Charities is a workplace-giving federation already paying Calvary, not a grantmaker, so it sits in Tier 2 as a channel. The T. Rowe Price Program is capped at Tier 2 as a donor-advised channel and Frontier Co-op falls to Tier 2 under the score cutoff.

**90-day plan** (`action_plan_90day.csv`): sequenced for a fundraising team Calvary held at six positions with limited growth over 2021–24 (Calvary's 2021–24 strategic plan report; internal, Calvary-facing use only). Month 1, government confirmations by day 30 (FY26 award letters, draw-down against ceilings with CoC reconciled first, FY27 renewal calendar), owned by the CEO and board chair. Month 2, two current-funder conversations a fortnight (development director): Abell, steward and renew (largest grant $270K in TY2021, latest filed $25K in TY2023, a further $25K in March 2025 in Calvary's records; invitation-only with no consecutive-year requests, so ask its staff when a next request is welcome and what it would fund); GWCF, a successor to the Health Equity Fund support behind its $458K plus a core general-operating request; Cafritz ($170K vs $250K largest to a peer) and Fowler ($40K vs $50K), a multi-year general-operating grant at the funder's peer-level amount; MGAC, cash vs in-kind. Month 3, introductions: Schattner is invitation-only, so the step is to secure an invitation through a named peer or co-funder (no LOI). Tier 2 channel step: confirm Calvary's enrollment in the CFC and employer campaigns and its designation code (America's Charities). Small check: confirm the FY26 gala date. Owner roles: CEO + board chair for ≥$100K and government rows; development director otherwise.

## Caveats
- Scores rank evidence, not fit with funder guidelines; the approved web pull on Tier 1–2 guidelines and deadlines is merged into the pipeline (`application_process`, `next_deadline_or_cycle`, `guidelines_url`, `guidelines_basis`, `open_status`; notes in `config/guideline_notes.csv`).
- High-count gap funders that are channels are labelled as channels and capped at Tier 2 (penalized, not removed); Clark is kept for the record only.
- Leadership materials name a funder only after its open status is checked on its own page. Invitation-only funders get an introduction through a named peer or co-funder that leads to an invitation (Schattner, Cohen), or a question to staff where Calvary is a current grantee (Abell); never an LOI.
- Three-peer names (The Washington Home, Cohen) depend on the provisional peer set (`peer_set_note`).
- Government and corporate scores are analyst judgment.
- Weights are editable; rerun `07_m7_pipeline.py` after changing `config/scoring_weights.yaml`.

## Confidence
Medium: the ordering is robust to moderate weight changes (9 or 10 of the top ten institutional rows stay in the top ten under ±0.05 changes, `m7_05_sensitivity`); exact ranks are not.
