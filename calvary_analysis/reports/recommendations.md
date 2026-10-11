# Recommendations report

*For the consulting team and Calvary's leadership. Data as of 2026-10-10. This report brings together the verdict (`recommendations/funding_pressure_verdict.md`), the scored pipeline (`recommendations/funder_pipeline.csv`), the 90-day plan (`recommendations/action_plan_90day.csv`) and the strategic options (`recommendations/strategic_recommendations.md`). Every figure traces to a chart ID in `chart_data/` and from there to the source registry. Tone: these are options for Calvary's team to weigh, offered with respect for what they have built.*

## 1. The verdict

Calvary is under moderate-to-high funding pressure, driven by **channel concentration and liquidity** rather than by its government share. The share (53% of revenue on the FY22–24 average, 58% in FY25) is typical: 11th of 19 DC-area organizations doing similar work and near the median of DC's human-services sector. What is not typical is the combination of three public streams with two passing through one intermediary (TCP carries 74% of a $4.1M award base), a private base that has held steady at about $1M a year in filed grants from the same 26–29 funders (one partner 27%), and a cushion that thinned in FY25 (a $607K deficit, event income down $483K, 4.4 months of cash).

The clouds: DC's budgets behind Calvary's local money have held flat to rising through FY2027, but the Mayor proposed cuts to the victim-services and DV lines in each of the last two springs (the Council restored both); the federal side (CoC renewals, the EHV sunset behind Sisters Rise) is less predictable; and Calvary recognized only 67–73% of its known award ceilings as revenue in FY24–25, which may mean undrawn awards.

Scenario results on the FY25 baseline (`m2_07`): OVSJG −10% costs $67K; OVSJG −25% $168K; CoC renewals −15% $178K; one CoC project lost $366K; the DHS/TCP contract lost $960K (19% of revenue); the combined case $1.31M (26%), leaving about 1.7 months of cash after a year even with half of the lost costs avoided. The headline cuts are survivable; the TCP-channel contract is the one to plan for.

## 2. The scored and tiered pipeline

182 rows scored on seven dimensions (mission fit 0.20, peer giving 0.20, regional giving 0.10, award size 0.15, accessibility 0.10, durability 0.10, relationship 0.15), weights editable in `config/scoring_weights.yaml`; Tier 1 = score ≥ 0.62 and typical grant ≥ $25K; Tier 2 ≥ 0.48; Tier 3 the rest. Government and corporate rows carry analyst scores. Sensitivity (`m7_05`): ±0.05 on any weight moves ranks by about one place in the top 30 and keeps 9–10 of the top 10.

**Tier 1 (11):**

| # | Target | Track | Score | Typical grant | Application process (web pull, reviewed) |
|---|---|---|---|---|---|
| 1 | William S. Abell Foundation | steward / upgrade | 0.86 | $25K (largest to Calvary $270K) | current funder; work through the relationship |
| 2 | Greater Washington Community Foundation | steward / upgrade | 0.85 | $33K (largest $458K) | fund-specific cycles on the Grant Opportunities page; ask about a Health Equity Fund successor |
| 3 | Clark Charitable Foundation | new | 0.82 | $250K | relationship-based; approach via the five peers it funds |
| 4 | DC OVSJG Victim Services grants | government (DC) | 0.80 | — | annual continuation; budget calendar March–July |
| 5 | Morris & Gwendolyn Cafritz Foundation | steward / upgrade | 0.78 | $36K (largest $170K) | portal; deadlines March 1, July 1, November 1; one application per 12 months |
| 6 | HUD Continuum of Care via TCP | government (federal) | 0.78 | — | annual renewal in the DC CoC competition; scope a PSH expansion project |
| 7 | DHS homeless services via TCP | government (DC) | 0.72 | — | confirm FY25–26 contract values and the Sisters Rise / EHV status |
| 8 | John Edward Fowler Memorial Foundation | steward / upgrade | 0.72 | $33K (largest $40K) | accepts applications; rolling |
| 9 | MGAC | corporate (CRM) | 0.70 | ~$238K/yr in CRM | quantify cash vs pro bono; propose a multi-year sponsorship |
| 10 | Robert I. Schattner Foundation | new | 0.67 | $60K | no public guidelines found; approach via the four peers it funds |
| 11 | America's Charities | new (workplace giving) | 0.64 | $39K | workplace-giving federation; campaign enrollment, already in the CRM |

**Tier 2 (40)** includes Venable Foundation (10 peers; deadlines February 1, June 1, September 1; in the CRM), JPMorgan Chase Foundation (invitation only), United Way NCA (annual partnership application, pre-screening in September), AAMC, Bank of America (two RFP cycles; Stable Housing RFP May–June), Weinberg (Maryland focus), Many Hands (January window; lapsed), The Washington Home, Cohen (invitation only), Meyer (Interest Form), Eugene B. Casey (mail, no deadline), Jane Bancroft Robinson (East of the River focus; lapsed), the T. Rowe Price Program (donor-advised channel), nine corporate CRM relationships (IMF, Reservoir, Latham & Watkins, UnitedHealth, Frontier Co-op, …), DHS PSH expansion and HUD CPF renewal.

**Tier 3 (131)** includes the remaining peer-funder gaps, DC-sector majors with no mission link, and 12 federal notices (HUD ROSS and housing counseling, DOL VETS HVRP, DOJ BJA/OJJDP behavioral-health and reentry, SAMHSA forecasts).

## 3. The 90-day plan (`action_plan_90day.csv`)

| By | Front | Actions | Owner |
|---|---|---|---|
| Day 30 | Public base | Reconcile award ceilings to recognized revenue FY24–26; confirm FY26 award letters and draw-down status for OVSJG, CoC and DHS; confirm the Sisters Rise / EHV status with TCP; map the FY27 renewal calendar | CEO + board chair |
| Day 30 | Re-engagement | Calls to lapsed funders (World Bank CCF, Many Hands, Jane Bancroft Robinson) with FY25 impact data | Development director |
| Day 45 | Upgrades | Multi-year general-operating asks to Abell, GWCF, Cafritz (time to the next deadline), Fowler, then United Way NCA and Bank of America (Tier 2 cycles) | Development director; CEO for ≥$100K |
| Day 45 | Corporate | Quantify cash vs in-kind for MGAC (and Capital One, IMF); propose multi-year sponsorships | CEO + corporate relations lead |
| Day 45 | Events | Confirm whether the FY25 gala moved; set the FY26 event at the FY24 level | Development director |
| Day 60–90 | New foundations | Warm introductions to Clark Charitable and Schattner through shared peers and co-funders; request guidelines or invitations; LOIs in the next cycle; America's Charities enrollment | CEO + board chair (Clark); development director |

## 4. Strategic options

See `recommendations/strategic_recommendations.md` for the full text. In brief:

1. **Protect and fully draw the public base:** draw-down audit; TCP channel documented and diversified with a direct DHS line; CoC renewals defended and a PSH expansion scoped; OVSJG budget season on the calendar; a stream risk register.
2. **Rebuild private revenue on three tracks:** multi-year upgrades with current majors; new foundations that already fund peers; lapsed funders; the event line; a major-gifts and DAF program (peers raise 40–50% of filed grants through DAFs; Calvary 25%); corporate relationships converted to multi-year.
3. **Hold a reserve and stop the burn:** six months of expenses (about $2.8M); close the FY25 gap in the FY26 budget; treat time-limited sources (Health Equity Fund) as one-time.
4. **Expand near first:** workforce formalization (SheWorks-style cohort inside Step Up DC), a behavioral-health credential or billing partner (the Samaritan Inns path to program revenue), then an FQHC clinic partnership; DV formalization only with the higher public share understood; families/maternal not suggested.
5. **Mitigate government risk within government:** direct DHS relationship alongside TCP; HUD CPF and DHS PSH as channels; contract terms; monthly draw tracking; advocacy calendar; early-warning indicators (OVSJG under-spend, TCP's DHS purchase orders, CoC NOFO, EHV sunset).

**Target arithmetic:** private revenue from about $2.1M (FY25) to about $3.0M in three years (institutional +$0.5M, major donors/DAF +$0.3M, events +$0.4M, earned +$0.1–0.3M) brings the public share to roughly half at flat public funding, restores a surplus and rebuilds the reserve.

## 5. What would change these recommendations

- Calvary's FY24 and FY25 audits and TCP subgrant agreements (flag D1): if awards are being fully drawn, recommendation 1 shrinks to monitoring; if not, it is the largest single lever.
- Confirmation on Sisters Rise / EHV (flag D2): if the stream ended in FY25, the scenario baseline falls and recommendation 2's target rises.
- The FY25 gala calendar (flag D3): if the event moved, FY25's private drop is timing and the event line recovers on its own.
- A change in the provisional peer set would move the gap list and the rank but not the sector percentile or the verdict.
