# M8 readout: mission-expansion scan

Script `scripts/08_m8_expansion.py`; area definitions and distance ratings in `config/expansion_areas.yaml`. Tables `chart_data/m8_01_expansion_scan.csv`, `m8_02_federal_opportunities.csv`; chart `m8_01_expansion_scan`. Insights M8-01, M8-02.

## Question
Which funding pools open up if Calvary formalizes or adds adjacent programs, and how far is each from current operations?

## Method
For each program area in `dim_program_area`: DMV institutional grant dollars TY2020–24 whose purpose text carries the tag (DAF sponsors and landscape exclusions removed), funders active and funders at $100K+, median grant, federal Grants.gov notices after removing research, tribal, rural and overseas notices and keeping relevant agencies (HUD, VA, DOL, DOJ, ACF, SAMHSA, USDA, Treasury, ACL), DC policy events, and an analyst distance rating: core, near (already delivered in some form), medium (same clients, new capability or credential), far (new population or licensing).

## Findings
| Area | Distance | DMV $/yr (tagged) | Funders ($100K+) | Federal notices | Calvary today | Models |
|---|---|---|---|---|---|---|
| Housing and homelessness | core | $32.4M | 391 (104) | 9 | TH 94, PSH 16, RRH 14 | N Street Village, DWC |
| Education and life skills | near | $93.7M | 744 (271) | 5 | LEAP | N Street Village, Thrive DC |
| Workforce and employment | near | $30.4M | 181 (66) | 6 | Step Up DC; SNAP E&T | SheWorks (stipends, childcare, employer partners); DWC MADE |
| Behavioral health and recovery | near | $20.7M | 251 (84) | 17 | On-site therapy, recovery | Samaritan Inns; N Street Village |
| DV and victim services | near | $4.5M | 161 (34) | 3 | DV-designated site; OVSJG | DASH, My Sister's Place, DC SAFE |
| Physical health | medium | $84.2M | 697 (206) | 0 | Meals, partnerships | Community of Hope (FQHC), Christ House, DWC clinic |
| Aging and older adults | medium | $9.7M | 153 (34) | 2 | Older PSH residents | DWC; The Washington Home |
| Women veterans | medium | $7.7M | 152 (34) | 5 | None documented | Access Housing DC; VA GPD |
| Reentry | medium | $1.0M | 39 (8) | 5 | Served, not named | SheWorks; OVSJG reentry |
| Maternal and family health | far | $4.2M | 60 (12) | 3 | Single women only | Community of Hope, House of Ruth |

1. **Near pools are substantial** (M8-01): education, workforce, behavioral health and DV together carry about $149M a year of tagged DMV institutional grants. Calvary already runs programs in each; formalizing them (named program, outcomes, credentials) opens funders without changing the mission. The education figure is dominated by schools and scholarships, so its practical share for Calvary is small; workforce and behavioral health are the real near pools.
2. **Health is the largest medium-distance pool** ($84M/yr, 206 funders at $100K+). The peer models are partnerships (DWC's clinic with JWCH; Community of Hope's FQHC), not building a clinic. A behavioral-health certification that allows Medicaid billing would turn therapy from a cost into program-service revenue (Samaritan Inns' path).
3. **Aging, veterans and reentry pools are small** in DMV philanthropy; their money is federal (VA GPD, DOL HVRP, DOJ reentry) and program-specific. Reentry fits Calvary's population (OVSJG runs reentry grants) but the private pool is $1M/yr.
4. **Federal direct competition is thin** (M8-02): 36 relevant notices in the feed, mostly HUD programs that flow through DC (ROSS, CDBG, housing counseling), DOJ BJA/OJJDP behavioral-health and reentry, SAMHSA forecasts, DOL VETS HVRP (includes homeless women veterans), VA grants. Realistic direct federal targets: HUD CPF earmark renewal, DOL HVRP (if a veterans track is added), SAMHSA treatment/recovery (with a licensed partner).

## Trade-offs for the recommendations
- **Workforce (near, recommended):** SheWorks-style cohort model inside Step Up DC; unlocks DOES/WIOA and workforce funders; modest cost; outcomes are easy to show.
- **Behavioral health (near, recommended with a credential decision):** DBH certification or a partner agreement converts therapy to billable revenue; staffing and compliance cost; the biggest earned-revenue lever.
- **DV formalization (near):** Calvary already holds a DV-designated site; a formal DV program and VOCA eligibility deepen the OVSJG relationship and open DV funders (DC SAFE, DASH pattern) but add reporting burden.
- **Health partnership (medium):** on-site clinic hours with an FQHC (Community of Hope is a peer and Ward 8 neighbor); low capital, opens health funders.
- **Aging (medium):** an older-women track in PSH; small pool, strong narrative.
- **Families / maternal (far, not recommended):** new population, licensing, mission change.

## Caveats
Tagged dollars understate what funders would give (general operating excluded); distance ratings are judgment; federal notices are a snapshot.

## Confidence
Medium.
