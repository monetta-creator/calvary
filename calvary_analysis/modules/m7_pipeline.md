# M7 readout: opportunity pipeline and scoring

Script `scripts/07_m7_pipeline.py`; weights and tier cutoffs in `config/scoring_weights.yaml`. Outputs `recommendations/funder_pipeline.csv` (also `chart_data/m7_00_funder_pipeline.csv`) and `recommendations/action_plan_90day.csv`; charts `m7_02_pipeline_scores`, `m7_03_tier1_score_breakdown`. Insight M7-01.

## Question
Which funders and programs should Calvary pursue first, and on what evidence?

## Method
Candidate base = M5 (current funders with headroom, lapsed funders, peer-funder gaps, DC-sector majors) joined to M6 relationship paths and the M4 landscape. DAF sponsors are excluded (a channel, not a grantmaker); the T. Rowe Price Program is scored like a DAF. Seven dimensions scored 0–1, weighted (mission fit 0.20, peer giving 0.20, regional giving 0.10, award size 0.15, accessibility 0.10, durability 0.10, relationship 0.15):

| Dimension | Evidence |
|---|---|
| Mission fit | funder issue tags (housing/DV/women = 1.0; behavioral health/workforce/health 0.7; general operating 0.6) plus the share of its DC-sector dollars whose purpose names housing/DV/women |
| Peer giving | core peers funded TY2020–24, capped at 8 |
| Regional giving | dollars to DC-sector organizations, log scale $50K → $10M |
| Award size | median grant to peers (else median DC-sector grant), log scale $5K → $250K |
| Accessibility | funder type and breadth (community foundation 0.85; public charity grantmaker 0.75; private foundation 0.70 / 0.50 / 0.30 by number of DC recipients); −0.15 for "see attached" filers; −0.30 for in-kind or workplace-giving channels |
| Durability | years funding peers and years active in the DC sector |
| Relationship | M6 path strength + 0.35 current funder + 0.20 lapsed + 0.15 on Calvary's CRM/lists |

Tiers: **Tier 1** score ≥ 0.62 and typical grant ≥ $25K (max 20); **Tier 2** score ≥ 0.48; **Tier 3** the rest. Government rows (OVSJG, DHS/TCP, HUD CoC, DHS PSH, HUD CPF) and corporate CRM relationships (≥$50K, no public filing) carry analyst scores (basis = inferred). Federal Grants.gov notices are Tier 3 by default.

## Result (182 rows; Tier 1 = 11, Tier 2 = 40, Tier 3 = 131)
| Track | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|
| Institutional: steward / upgrade | 4 (Abell, GWCF, Cafritz, Fowler) | 12 | 22 |
| Institutional: new | 3 (Clark Charitable, Schattner, America's Charities) | 15 (Venable, JPMorgan Chase, Gifts for the Homeless, Capital Area Food Bank, Weinberg, Give Lively, The Washington Home, Cohen, Viragh, Arlington CF, Coca-Cola, Morrison & Foerster, Meyer, Eugene B. Casey, ImpactAssets) | 97 |
| DAF channel | – | 1 (T. Rowe Price Program) | – |
| Corporate (CRM) | 1 (MGAC) | 10 (IMF, Reservoir, Latham & Watkins, UnitedHealth, …) | – |
| Government DC | 2 (OVSJG grants; DHS/TCP contracts) | 1 (DHS PSH expansion) | – |
| Government federal | 1 (HUD CoC via TCP) | 1 (HUD CPF renewal) | 12 opportunities |

**Tier 1 (11 rows):** Abell (0.86), GWCF (0.85), Clark Charitable (0.82, typical grant $250K, 5 peers, no Calvary grant), OVSJG (0.80), Cafritz (0.78), HUD CoC via TCP (0.78), DHS/TCP (0.72), Fowler (0.72), MGAC (0.70, corporate), Schattner (0.67), America's Charities (0.64). The T. Rowe Price Program is scored as a donor-advised channel (Tier 2) and Frontier Co-op falls to Tier 2 under the score cutoff.

**90-day plan** (`action_plan_90day.csv`): government rows by day 30 (confirm FY26 award letters and draw-down against ceilings; FY27 renewal calendar); upgrade asks to current majors by day 45 (multi-year general operating at the funder's peer-level amount); warm introductions and LOIs for Clark, Schattner, America's Charities by day 60–90; corporate cash-vs-in-kind quantification. Owner roles: CEO + board chair for ≥$100K and government rows; development director otherwise.

## Caveats
- Scores rank evidence, not fit with funder guidelines; the approved web pull on Tier 1–2 guidelines and deadlines is merged into the pipeline (`application_process`, `next_deadline_or_cycle`, `guidelines_url`, `guidelines_basis`; notes in `config/guideline_notes.csv`).
- Several high-count gap funders are in-kind or workplace channels (penalized, not removed).
- Government and corporate scores are analyst judgment.
- Weights are editable; rerun `07_m7_pipeline.py` after changing `config/scoring_weights.yaml`.

## Confidence
Medium: the ordering is robust to moderate weight changes (the same ten institutional names stay in Tiers 1–2); exact ranks are not.
