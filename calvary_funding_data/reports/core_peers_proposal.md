# Core peers proposal (Checkpoint 2)

Status: **provisional**. The list below is in `config/core_peers.csv`, and the downstream pulls use it. To change it, edit that file and rerun `scripts/20_build_universes.py`. Every candidate's 990 XML was fetched, so swapping peers needs no new downloads.

## How candidates were found
- **Named seeds:** 36 DC-area organizations known to serve homeless women, DV survivors, people in recovery, or Wards 7/8. They were matched against the full DC/MD/VA BMF, because several (e.g. Community of Hope, Thrive DC) carry health or food NTEE codes.
- **Data-driven:** DC/DMV sector public charities with revenue ≥ $750K and either a shelter/DV NTEE code or a women-focused name.
- **Evidence:** each candidate's latest e-filed 990 (mission, program descriptions, revenue, government grants), with the DC ward from the MAR 2 geocoder.
- **Score** (in `interim/core_peer_candidates.csv`):
  - women focus: 3
  - DV: 2
  - homeless/housing: 2
  - recovery or mental health: 1
  - Ward 7/8: 2
  - DC: 1
  - size similarity: up to 2, by log distance from Calvary's $4.97M
- **Relevance gate:** homeless or DV language must appear in the filing text. Final picks combine the score with judgment about model similarity.

## Proposed core peers (18)

| Tier | Organization | EIN | State/Ward | Revenue (latest) | Gov share | Rationale |
|---|---|---|---|---|---|---|
| 1a_dc_women_homeless | N Street Village | 521007373 | DC Ward 2 | $10.5M (TY2024) | 39% | Closest model match: housing, health and recovery services for homeless and low-income women in DC; about 2x Calvary's revenue |
| 1a_dc_women_homeless | House of Ruth (DC) | 521054102 | DC Ward 2 | $20.0M (TY2024) | 45% | Housing and services for women, children and families in DC, including DV survivors; large comparator ($20M) |
| 1a_dc_women_homeless | Open Arms Housing | 522040518 | DC Ward 5 | $2.5M (TY2024) | 77% | Permanent supportive housing for women experiencing homelessness, with a mental-health focus; small ($2.5M), 77% government |
| 1a_dc_women_homeless | New Endeavors by Women | 521547845 | DC Ward 2 | $3.1M (TY2024) | 82% | Transitional housing for homeless women in DC; similar size ($3.1M); 82% government |
| 1b_dc_dv | District Alliance for Safe Housing (DASH) | 711019574 | DC | $7.3M (TY2024) | 90% | Safe housing for DV and sexual-violence survivors in DC; Calvary's New Foundations site is also DV-designated; 90% government |
| 1b_dc_dv | My Sister's Place | 521263256 | DC Ward 1 | $8.3M (TY2024) | 83% | DC DV shelter and housing for survivors and children; similar size ($8.3M) |
| 1b_dc_dv | DC SAFE | 412226446 | DC | $6.9M (TY2024) | 94% | DV crisis response and emergency shelter in DC; OVSJG-funded like Calvary; 94% government |
| 2_dc_homeless_recovery | Samaritan Inns | 521474935 | DC Ward 1 | $6.2M (TY2024) | 11% | Recovery-oriented housing for homeless adults in DC; similar size ($6.2M) but only 11% government (contrast case) |
| 2_dc_homeless_recovery | Christ House | 521362103 | DC Ward 1 | $4.9M (TY2024) | 35% | Medical respite for people experiencing homelessness in DC; nearly identical revenue to Calvary ($4.9M) |
| 2_dc_homeless_recovery | Everyone Home DC | 520853501 | DC Ward 6 | $4.9M (TY2024) | 85% | DC homelessness prevention and housing; nearly identical revenue ($4.9M); 85% government |
| 2_dc_homeless_recovery | Coalition for the Homeless | 521245499 | DC Ward 2 | $7.5M (TY2024) | 92% | DC shelter and housing provider with women's programs; similar size ($7.5M); 92% government |
| 2_dc_homeless_recovery | Thrive DC | 521485474 | DC Ward 1 | $2.6M (TY2024) | 1% | DC homelessness services, including a women's program; small ($2.6M) and almost entirely private (contrast case) |
| 2_dc_homeless_recovery | Miriam's Kitchen | 521331552 | DC Ward 2 | $13.0M (TY2024) | 10% | Chronic homelessness and PSH case management in DC; philanthropy-led (10% government) with a large donor base |
| 2_dc_ward78 | Community of Hope | 521184749 | DC Ward 8 | $57.6M (TY2024) | 38% | Ward 8-based homelessness and health provider in Calvary's service area; large ($57.6M) |
| 2_dc_ward78 | Covenant House Washington DC | 133537709 | DC Ward 8 | $7.3M (TY2024) | 56% | Ward 8 shelter and crisis services (youth); similar size ($7.3M); same ward-level funders |
| 3_dmv_women_dv | Doorways for Women and Families | 541087829 | VA | $6.1M (TY2024) | 47% | Arlington VA: women, families and DV survivors experiencing homelessness; closest suburban analog ($6.1M) |
| 3_dmv_women_dv | House of Ruth Maryland | 521100236 | MD | $11.6M (TY2024) | 63% | Baltimore MD: DV services and housing for women and children; regional DV funder overlap ($11.6M) |
| 3_dmv_women_dv | Heartly House | 521186250 | MD | $5.1M (TY2024) | 79% | Frederick MD: DV and sexual-assault shelter and services; similar size ($5.1M) |

Tier key:
- 1a: DC, women-focused homelessness
- 1b: DC, DV survivors
- 2: DC homelessness and recovery at a similar size, or a Ward 7/8 presence
- 3: DMV women/DV housing outside DC

## Alternates (in the candidate file; swap in by editing config/core_peers.csv)

- **Bethany House Of Northern Virginia Inc** (510252177, VA): $0.7M. TO EMPOWER WOMEN ESCAPING DOMESTIC VIOLENCE THROUGH SAFE HOUSING & TRAUMA-INFORMED SERVICES.
- **Wanda Alston Foundation** (463159251, DC): $1.5M. TO ERADICATE HOMELESSNESS FOR LGBTQIA2S+ YOUTH AGES 18-24 AND TO ENSURE THAT THEY HAVE ACCESS TO SERVICES THAT IMPROVE THEIR OVERALL QUALITY
- **Interfaith Works Inc** (521072684, MD): $23.8M. SEE PART III, LINE 1.
- **Safe Sisters Circle** (825194511, DC): $0.9M. The Safe Sisters Circle is a 501c3 nonprofit that provides free culturally specific holistic and trauma-based services to black women surviv
- **Access Housing Inc Dc** (521918702, DC): $1.6M. Provide housing, job training and counseling services to homeless veterans.
- **Volare** (454888353, DC): $5.5M. VOLARE CREATES EQUITABLE HEALING AND DIGNIFIED EXPERIENCES FOR SURVIVORS OF CRIME BY PROVIDING FREE, TRAUMA-INFORMED ADVOCACY, THERAPEUTIC, 
- **Carpenters Shelter Inc** (541571849, VA): $5.8M. SUPPORT PEOPLE EXPERIENCING AND AT RISK OF HOMELESSNESS.
- **Sasha Bruce Youthwork Inc** (521006486, DC): $18.1M. SBY'S MISSION IS TO IMPROVE THE LIVES OF RUNAWAY, HOMELESS, AND UNSTABLE YOUTH AND THEIR FAMILIES.
- **Shelter House Inc** (521217106, VA): $19.8M. Prevent and end homelessness and domestic violence in Northern Virginia.
- **Life Deeds Inc** (900501580, MD): $5.8M. THE MISSION OF LIFE DEEDS, INC. IS TO PROVIDE COMPREHENSIVE QUALITY SERVICES TO RUNAWAY, HOMELESS, COMMITED, ABBUSED, NEGLETED AND AT-RISK Y
- **Pathways To Housing Dc** (371464353, DC): $19.4M. SEE PART III, LINE 1.
- **Friendship Place** (521925494, DC): $24.3M. Friendship Place is a leader in the Washington, DC, metro area in developing solutions to homelessness that have measurable results and a la
- **Some Inc** (237098123, DC): $43.4M. THE ORGANIZATION EXISTS TO HELP THE POOR AND HOMELESS BY PROVIDING FOR IMMEDIATE & LONG-TERM NEEDS.

## Universe sizes (at Checkpoint 2)

These sizes predate later additions: the `named_comparators` universe and NTEE P83 women's centers. Current sizes are in `reports/universe_summary.md`.

| Universe | Distinct EINs |
|---|---|
| calvary | 1 |
| core_peers | 18 |
| daf_sponsors | 15 |
| dc_sector | 1,024 |
| dmv_funders | 7,705 |
| dmv_sector | 4,890 |
| national_women | 2,452 |
| size_matched | 557 |

Full rule-level counts and filters: `reports/universe_summary.md` and `config/universes.yaml`.
