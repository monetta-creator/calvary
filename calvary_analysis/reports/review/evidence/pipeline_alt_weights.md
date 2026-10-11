# Alternative weightings: Tier 1 / Tier 2 membership changes vs funder_pipeline.csv

Baseline (file): Tier 1 = 11 rows (7 institutional), Tier 2 = 40 rows (28 institutional).
Only rows with numeric component scores are re-scored; government / CRM-corporate / opportunity rows keep their file score and tier. Tier rule applied: Tier 1 iff score >= 0.62 and typical_grant >= min award (cap 20); Tier 2 iff score >= 0.48.
The undocumented script rule that holds daf_like_channels (311709466) at Tier 2 is kept in these scenarios so it does not show up as a spurious change.
Scenario (d) caveat: s_relationship is clipped at 1.0 in the file, so for rows at 1.0 the true effect of removing the 0.35 bonus is at most 0.0525 and may be smaller (the un-clipped path strength is not in the pipeline file).
Scores shown to 3 dp. Names truncated to 40 characters.

| scenario | weights / change | Tier 1 n | Tier 2 n | Tier 1 added | Tier 1 dropped | Tier 2 added (from Tier 3) | Tier 2 dropped (to Tier 3) |
|---|---|---|---|---|---|---|---|
| (a) equal weights 1/7 | all seven 0.1429 | 12 | 47 | 421559999 WORLD BANK COMMUNITY CONNECTIONS FUND (0.622) | none | 521270464 THE MORNINGSTAR PHILANTHROPIC FOUNDATION (0.528); 526047356 DIANE & NORMAN BERNSTEIN FOUNDATION (0.518); 521951681 ANNIE E CASEY FOUNDATION (0.511); 136163174 PEPSICO FOUNDATION INC (0.499); 460563684 WORKDAY FOUNDATION (0.498); 522166327 DONORS TRUST INC (0.492); 521691418 ENGLAND FAMILY FOUNDATION INC (0.488); 526055743 CORINA HIGGINSON TRUST (0.486) | none |
| (b) size matters | award 0.30 mission 0.20 peer 0.15 rel 0.15 regional 0.10 access 0.05 durab 0.05 | 12 | 47 | 421559999 WORLD BANK COMMUNITY CONNECTIONS FUND (0.627); 526037034 THE HARRY & JEANETTE WEINBERG FOUNDATION (0.620) | 541517707 AMERICAS CHARITIES (0.600) | 411367441 WELLS FARGO FOUNDATION (0.600); 136163174 PEPSICO FOUNDATION INC (0.583); 460563684 WORKDAY FOUNDATION (0.578); 522166327 DONORS TRUST INC (0.546); 521953832 RICHARD E AND NANCY P MARRIOTT FOUNDATIO (0.538); 521186071 MARTHAS TABLE (0.520); 275370859 MATAN FAMILY FOUNDATION INC (0.516); 541896244 JACK KENT COOKE FOUNDATION (0.510); 540597601 PUBLIC WELFARE FOUNDATION INC (0.509); 823941326 LUMINATE FOUNDATION INC (0.497); 541991343 AKERSON FAMILY FOUNDATION (0.488); 113737220 CORNERSTONE FOUNDATION INC (0.485); 810723895 RAST FOUNDATION (0.484); 521270464 THE MORNINGSTAR PHILANTHROPIC FOUNDATION (0.484); 800424607 WALLACE GLOBAL FUND II (0.483); 854228861 EDWARD AND KATHLEEN QUINN FAMILY (0.483) | 810693451 GIVE LIVELY FOUNDATION INC (0.478); 526038149 DIMICK FOUNDATION (0.461); 562305290 CAROL AND GENE LUDWIG FAMILY FOUNDATION (0.458); 812118591 CONGRESSIONAL SPORTS FOR CHARITY (0.452); 262048480 IMPACTASSETS INC (0.450); 943006979 MORRISON & FOERSTER FOUNDATION (0.438); 201173866 OMIDYAR NETWORK FUND INC (0.426); 520846147 WALTER A BLOEDORN FOUNDATION (0.401) |
| (c) relationship-light | rel 0.05, award 0.25, others as file | 11 | 53 | 526037034 THE HARRY & JEANETTE WEINBERG FOUNDATION (0.632) | 541517707 AMERICAS CHARITIES (0.620) | 136163174 PEPSICO FOUNDATION INC (0.562); 460563684 WORKDAY FOUNDATION (0.561); 411367441 WELLS FARGO FOUNDATION (0.559); 522166327 DONORS TRUST INC (0.556); 521186071 MARTHAS TABLE (0.531); 521270464 THE MORNINGSTAR PHILANTHROPIC FOUNDATION (0.524); 521953832 RICHARD E AND NANCY P MARRIOTT FOUNDATIO (0.517); 113737220 CORNERSTONE FOUNDATION INC (0.503); 540597601 PUBLIC WELFARE FOUNDATION INC (0.500); 346516969 W ONEIL FOUNDATION (0.500); 522028612 WASHINGTON AREA WOMENS FOUNDATION INC (0.499); 474329394 REVADA FOUNDATION (0.490); 275370859 MATAN FAMILY FOUNDATION INC (0.489); 131624103 YWCA USA INC (0.487); 020762730 RALPH S AND FRANCES R DWECK FAMILY FOUND (0.484); 800424607 WALLACE GLOBAL FUND II (0.484); 541896244 JACK KENT COOKE FOUNDATION (0.483) | 562305290 CAROL AND GENE LUDWIG FAMILY FOUNDATION (0.470); 812118591 CONGRESSIONAL SPORTS FOR CHARITY (0.470); 201173866 OMIDYAR NETWORK FUND INC (0.429); 520846147 WALTER A BLOEDORN FOUNDATION (0.426) |
| (d) no current-funder bonus (-0.0525 where gives_to_calvary) | file weights; score - 0.35*0.15 for current funders | 11 | 35 | none | none | none | 201173866 OMIDYAR NETWORK FUND INC (0.459); 812118591 CONGRESSIONAL SPORTS FOR CHARITY (0.457); 273818431 JANE BANCROFT ROBINSON FOUNDATION INC (0.450); 562305290 CAROL AND GENE LUDWIG FAMILY FOUNDATION (0.430); 520846147 WALTER A BLOEDORN FOUNDATION (0.429) |
| (e) tier1_min_award = $50,000 | file weights; min award 50,000 | 6 | 45 | none | 521435573 WILLIAM S ABELL FOUNDATION INC (0.857); 237343119 GREATER WASHINGTON COMMUNITY FOUNDATION (0.847); 526036989 MORRIS AND GWENDOLYN CAFRITZ FOUNDATION (0.780); 516019469 JOHN EDWARD FOWLER MEMORIAL FOUNDATION (0.717); 541517707 AMERICAS CHARITIES (0.638) | none | none |
| (f) tier1_min_award = $10,000 | file weights; min award 10,000 | 14 | 37 | 521283255 VENABLE BAETJER AND HOWARD FOUNDATION (0.780); 530234290 UNITED WAY OF THE NATIONAL CAPITAL AREA (0.710); 362169124 ASSOCIATION OF AMERICAN MEDICAL COLLEGES (0.683) | none | none | none |

## Top 15 by score: (a) equal weights 1/7

| # | funder_id | funder | type | file tier | new tier | file score | new score | typical grant |
|---|---|---|---|---|---|---|---|---|
| 1 | 237343119 | GREATER WASHINGTON COMMUNITY FOUNDATION | community_foundation | 1 | 1 | 0.847 | 0.861 | 32,525 |
| 2 | 521435573 | WILLIAM S ABELL FOUNDATION INC | private_foundation | 1 | 1 | 0.857 | 0.838 | 25,000 |
| 3 | 521512330 | CLARK CHARITABLE FOUNDATION INC | private_foundation | 1 | 1 | 0.820 | 0.832 | 250,000 |
| 4 | 526036989 | MORRIS AND GWENDOLYN CAFRITZ FOUNDATION | private_foundation | 1 | 1 | 0.780 | 0.804 | 36,250 |
| 5 | GOV-DC-1 | DC OVSJG Victim Services grants (Reach U | government | 1 | 1 | 0.800 | 0.800 |  |
| 6 | GOV-FED-1 | HUD Continuum of Care via TCP (Sister Ci | government | 1 | 1 | 0.780 | 0.780 |  |
| 7 | 521283255 | VENABLE BAETJER AND HOWARD FOUNDATION | public_charity_grantmaker | 2 | 2 | 0.780 | 0.768 | 12,500 |
| 8 | 530234290 | UNITED WAY OF THE NATIONAL CAPITAL AREA | federated_giving | 2 | 2 | 0.710 | 0.741 | 19,163 |
| 9 | 516019469 | JOHN EDWARD FOWLER MEMORIAL FOUNDATION | private_foundation | 1 | 1 | 0.717 | 0.733 | 32,500 |
| 10 | GOV-DC-2 | DHS homeless services via TCP (TH contra | government | 1 | 1 | 0.720 | 0.720 |  |
| 11 | 237049738 | JPMORGAN CHASE FOUNDATION | corporate_foundation | 2 | 2 | 0.712 | 0.710 | 100 |
| 12 | 362169124 | ASSOCIATION OF AMERICAN MEDICAL COLLEGES | public_charity_grantmaker | 2 | 2 | 0.683 | 0.696 | 20,000 |
| 13 | CRM:MGAC | MGAC | corporate (no public filing) | 1 | 1 | 0.695 | 0.695 | 237,577 |
| 14 | 521800778 | ROBERT I SCHATTNER FOUNDATION INC | private_foundation | 1 | 1 | 0.673 | 0.676 | 60,000 |
| 15 | 200721133 | BANK OF AMERICA CHARITABLE FOUNDATION IN | corporate_foundation | 2 | 2 | 0.654 | 0.660 | 100 |

## Top 15 by score: (b) size matters

| # | funder_id | funder | type | file tier | new tier | file score | new score | typical grant |
|---|---|---|---|---|---|---|---|---|
| 1 | 521512330 | CLARK CHARITABLE FOUNDATION INC | private_foundation | 1 | 1 | 0.820 | 0.853 | 250,000 |
| 2 | GOV-DC-1 | DC OVSJG Victim Services grants (Reach U | government | 1 | 1 | 0.800 | 0.800 |  |
| 3 | 521435573 | WILLIAM S ABELL FOUNDATION INC | private_foundation | 1 | 1 | 0.857 | 0.784 | 25,000 |
| 4 | GOV-FED-1 | HUD Continuum of Care via TCP (Sister Ci | government | 1 | 1 | 0.780 | 0.780 |  |
| 5 | 237343119 | GREATER WASHINGTON COMMUNITY FOUNDATION | community_foundation | 1 | 1 | 0.847 | 0.776 | 32,525 |
| 6 | 526036989 | MORRIS AND GWENDOLYN CAFRITZ FOUNDATION | private_foundation | 1 | 1 | 0.780 | 0.721 | 36,250 |
| 7 | GOV-DC-2 | DHS homeless services via TCP (TH contra | government | 1 | 1 | 0.720 | 0.720 |  |
| 8 | CRM:MGAC | MGAC | corporate (no public filing) | 1 | 1 | 0.695 | 0.695 | 237,577 |
| 9 | 521283255 | VENABLE BAETJER AND HOWARD FOUNDATION | public_charity_grantmaker | 2 | 2 | 0.780 | 0.677 | 12,500 |
| 10 | 521800778 | ROBERT I SCHATTNER FOUNDATION INC | private_foundation | 1 | 1 | 0.673 | 0.669 | 60,000 |
| 11 | 516019469 | JOHN EDWARD FOWLER MEMORIAL FOUNDATION | private_foundation | 1 | 1 | 0.717 | 0.660 | 32,500 |
| 12 | 421559999 | WORLD BANK COMMUNITY CONNECTIONS FUND | public_charity_grantmaker | 2 | 1 | 0.601 | 0.627 | 100,000 |
| 13 | 530234290 | UNITED WAY OF THE NATIONAL CAPITAL AREA | federated_giving | 2 | 2 | 0.710 | 0.627 | 19,163 |
| 14 | 526037034 | THE HARRY & JEANETTE WEINBERG FOUNDATION | private_foundation | 2 | 1 | 0.588 | 0.620 | 75,000 |
| 15 | 510486987 | MANY HANDS INC | public_charity_grantmaker | 2 | 2 | 0.575 | 0.613 | 75,000 |

## Top 15 by score: (c) relationship-light

| # | funder_id | funder | type | file tier | new tier | file score | new score | typical grant |
|---|---|---|---|---|---|---|---|---|
| 1 | 521512330 | CLARK CHARITABLE FOUNDATION INC | private_foundation | 1 | 1 | 0.820 | 0.870 | 250,000 |
| 2 | GOV-DC-1 | DC OVSJG Victim Services grants (Reach U | government | 1 | 1 | 0.800 | 0.800 |  |
| 3 | 521435573 | WILLIAM S ABELL FOUNDATION INC | private_foundation | 1 | 1 | 0.857 | 0.798 | 25,000 |
| 4 | 237343119 | GREATER WASHINGTON COMMUNITY FOUNDATION | community_foundation | 1 | 1 | 0.847 | 0.795 | 32,525 |
| 5 | GOV-FED-1 | HUD Continuum of Care via TCP (Sister Ci | government | 1 | 1 | 0.780 | 0.780 |  |
| 6 | 526036989 | MORRIS AND GWENDOLYN CAFRITZ FOUNDATION | private_foundation | 1 | 1 | 0.780 | 0.731 | 36,250 |
| 7 | GOV-DC-2 | DHS homeless services via TCP (TH contra | government | 1 | 1 | 0.720 | 0.720 |  |
| 8 | 521283255 | VENABLE BAETJER AND HOWARD FOUNDATION | public_charity_grantmaker | 2 | 2 | 0.780 | 0.705 | 12,500 |
| 9 | 521800778 | ROBERT I SCHATTNER FOUNDATION INC | private_foundation | 1 | 1 | 0.673 | 0.696 | 60,000 |
| 10 | CRM:MGAC | MGAC | corporate (no public filing) | 1 | 1 | 0.695 | 0.695 | 237,577 |
| 11 | 516019469 | JOHN EDWARD FOWLER MEMORIAL FOUNDATION | private_foundation | 1 | 1 | 0.717 | 0.664 | 32,500 |
| 12 | 530234290 | UNITED WAY OF THE NATIONAL CAPITAL AREA | federated_giving | 2 | 2 | 0.710 | 0.644 | 19,163 |
| 13 | 237049738 | JPMORGAN CHASE FOUNDATION | corporate_foundation | 2 | 2 | 0.712 | 0.633 | 100 |
| 14 | 526037034 | THE HARRY & JEANETTE WEINBERG FOUNDATION | private_foundation | 2 | 1 | 0.588 | 0.632 | 75,000 |
| 15 | 521593963 | GIFTS FOR THE HOMELESS | public_charity_grantmaker | 2 | 2 | 0.690 | 0.632 | 6,488 |

## Top 15 by score: (d) no current-funder bonus (-0.0525 where gives_to_calvary)

| # | funder_id | funder | type | file tier | new tier | file score | new score | typical grant |
|---|---|---|---|---|---|---|---|---|
| 1 | 521512330 | CLARK CHARITABLE FOUNDATION INC | private_foundation | 1 | 1 | 0.820 | 0.820 | 250,000 |
| 2 | 521435573 | WILLIAM S ABELL FOUNDATION INC | private_foundation | 1 | 1 | 0.857 | 0.804 | 25,000 |
| 3 | GOV-DC-1 | DC OVSJG Victim Services grants (Reach U | government | 1 | 1 | 0.800 | 0.800 |  |
| 4 | 237343119 | GREATER WASHINGTON COMMUNITY FOUNDATION | community_foundation | 1 | 1 | 0.847 | 0.794 | 32,525 |
| 5 | GOV-FED-1 | HUD Continuum of Care via TCP (Sister Ci | government | 1 | 1 | 0.780 | 0.780 |  |
| 6 | 521283255 | VENABLE BAETJER AND HOWARD FOUNDATION | public_charity_grantmaker | 2 | 2 | 0.780 | 0.780 | 12,500 |
| 7 | 526036989 | MORRIS AND GWENDOLYN CAFRITZ FOUNDATION | private_foundation | 1 | 1 | 0.780 | 0.728 | 36,250 |
| 8 | GOV-DC-2 | DHS homeless services via TCP (TH contra | government | 1 | 1 | 0.720 | 0.720 |  |
| 9 | 237049738 | JPMORGAN CHASE FOUNDATION | corporate_foundation | 2 | 2 | 0.712 | 0.712 | 100 |
| 10 | CRM:MGAC | MGAC | corporate (no public filing) | 1 | 1 | 0.695 | 0.695 | 237,577 |
| 11 | 521593963 | GIFTS FOR THE HOMELESS | public_charity_grantmaker | 2 | 2 | 0.690 | 0.690 | 6,488 |
| 12 | 521800778 | ROBERT I SCHATTNER FOUNDATION INC | private_foundation | 1 | 1 | 0.673 | 0.673 | 60,000 |
| 13 | 516019469 | JOHN EDWARD FOWLER MEMORIAL FOUNDATION | private_foundation | 1 | 1 | 0.717 | 0.664 | 32,500 |
| 14 | 530234290 | UNITED WAY OF THE NATIONAL CAPITAL AREA | federated_giving | 2 | 2 | 0.710 | 0.657 | 19,163 |
| 15 | 541517707 | AMERICAS CHARITIES | public_charity_grantmaker | 1 | 1 | 0.638 | 0.638 | 38,529 |

## Top 15 by score: (e) tier1_min_award = $50,000

| # | funder_id | funder | type | file tier | new tier | file score | new score | typical grant |
|---|---|---|---|---|---|---|---|---|
| 1 | 521435573 | WILLIAM S ABELL FOUNDATION INC | private_foundation | 1 | 2 | 0.857 | 0.857 | 25,000 |
| 2 | 237343119 | GREATER WASHINGTON COMMUNITY FOUNDATION | community_foundation | 1 | 2 | 0.847 | 0.847 | 32,525 |
| 3 | 521512330 | CLARK CHARITABLE FOUNDATION INC | private_foundation | 1 | 1 | 0.820 | 0.820 | 250,000 |
| 4 | GOV-DC-1 | DC OVSJG Victim Services grants (Reach U | government | 1 | 1 | 0.800 | 0.800 |  |
| 5 | 526036989 | MORRIS AND GWENDOLYN CAFRITZ FOUNDATION | private_foundation | 1 | 2 | 0.780 | 0.780 | 36,250 |
| 6 | GOV-FED-1 | HUD Continuum of Care via TCP (Sister Ci | government | 1 | 1 | 0.780 | 0.780 |  |
| 7 | 521283255 | VENABLE BAETJER AND HOWARD FOUNDATION | public_charity_grantmaker | 2 | 2 | 0.780 | 0.780 | 12,500 |
| 8 | GOV-DC-2 | DHS homeless services via TCP (TH contra | government | 1 | 1 | 0.720 | 0.720 |  |
| 9 | 516019469 | JOHN EDWARD FOWLER MEMORIAL FOUNDATION | private_foundation | 1 | 2 | 0.717 | 0.717 | 32,500 |
| 10 | 237049738 | JPMORGAN CHASE FOUNDATION | corporate_foundation | 2 | 2 | 0.712 | 0.712 | 100 |
| 11 | 530234290 | UNITED WAY OF THE NATIONAL CAPITAL AREA | federated_giving | 2 | 2 | 0.710 | 0.710 | 19,163 |
| 12 | CRM:MGAC | MGAC | corporate (no public filing) | 1 | 1 | 0.695 | 0.695 | 237,577 |
| 13 | 521593963 | GIFTS FOR THE HOMELESS | public_charity_grantmaker | 2 | 2 | 0.690 | 0.690 | 6,488 |
| 14 | 362169124 | ASSOCIATION OF AMERICAN MEDICAL COLLEGES | public_charity_grantmaker | 2 | 2 | 0.683 | 0.683 | 20,000 |
| 15 | 521800778 | ROBERT I SCHATTNER FOUNDATION INC | private_foundation | 1 | 1 | 0.673 | 0.673 | 60,000 |

## Top 15 by score: (f) tier1_min_award = $10,000

| # | funder_id | funder | type | file tier | new tier | file score | new score | typical grant |
|---|---|---|---|---|---|---|---|---|
| 1 | 521435573 | WILLIAM S ABELL FOUNDATION INC | private_foundation | 1 | 1 | 0.857 | 0.857 | 25,000 |
| 2 | 237343119 | GREATER WASHINGTON COMMUNITY FOUNDATION | community_foundation | 1 | 1 | 0.847 | 0.847 | 32,525 |
| 3 | 521512330 | CLARK CHARITABLE FOUNDATION INC | private_foundation | 1 | 1 | 0.820 | 0.820 | 250,000 |
| 4 | GOV-DC-1 | DC OVSJG Victim Services grants (Reach U | government | 1 | 1 | 0.800 | 0.800 |  |
| 5 | 526036989 | MORRIS AND GWENDOLYN CAFRITZ FOUNDATION | private_foundation | 1 | 1 | 0.780 | 0.780 | 36,250 |
| 6 | GOV-FED-1 | HUD Continuum of Care via TCP (Sister Ci | government | 1 | 1 | 0.780 | 0.780 |  |
| 7 | 521283255 | VENABLE BAETJER AND HOWARD FOUNDATION | public_charity_grantmaker | 2 | 1 | 0.780 | 0.780 | 12,500 |
| 8 | GOV-DC-2 | DHS homeless services via TCP (TH contra | government | 1 | 1 | 0.720 | 0.720 |  |
| 9 | 516019469 | JOHN EDWARD FOWLER MEMORIAL FOUNDATION | private_foundation | 1 | 1 | 0.717 | 0.717 | 32,500 |
| 10 | 237049738 | JPMORGAN CHASE FOUNDATION | corporate_foundation | 2 | 2 | 0.712 | 0.712 | 100 |
| 11 | 530234290 | UNITED WAY OF THE NATIONAL CAPITAL AREA | federated_giving | 2 | 1 | 0.710 | 0.710 | 19,163 |
| 12 | CRM:MGAC | MGAC | corporate (no public filing) | 1 | 1 | 0.695 | 0.695 | 237,577 |
| 13 | 521593963 | GIFTS FOR THE HOMELESS | public_charity_grantmaker | 2 | 2 | 0.690 | 0.690 | 6,488 |
| 14 | 362169124 | ASSOCIATION OF AMERICAN MEDICAL COLLEGES | public_charity_grantmaker | 2 | 1 | 0.683 | 0.683 | 20,000 |
| 15 | 521800778 | ROBERT I SCHATTNER FOUNDATION INC | private_foundation | 1 | 1 | 0.673 | 0.673 | 60,000 |

## Tier 1 institutional rows if s_relationship were 0.5 (original weights)

| funder_id | funder | s_relationship | score | score at rel=0.5 | still Tier 1? |
|---|---|---|---|---|---|
| 521435573 | WILLIAM S ABELL FOUNDATION INC | 1.000 | 0.857 | 0.782 | yes |
| 237343119 | GREATER WASHINGTON COMMUNITY FOUNDATION | 1.000 | 0.847 | 0.772 | yes |
| 521512330 | CLARK CHARITABLE FOUNDATION INC | 0.498 | 0.820 | 0.820 | yes |
| 526036989 | MORRIS AND GWENDOLYN CAFRITZ FOUNDATION | 1.000 | 0.780 | 0.705 | yes |
| 516019469 | JOHN EDWARD FOWLER MEMORIAL FOUNDATION | 1.000 | 0.717 | 0.642 | yes |
| 521800778 | ROBERT I SCHATTNER FOUNDATION INC | 0.408 | 0.673 | 0.687 | yes |
| 541517707 | AMERICAS CHARITIES | 0.702 | 0.638 | 0.608 | NO (falls to Tier 2) |

## Tier 2 institutional rows that would enter Tier 1 if s_relationship were 0.5 (original weights, min award $25K)

- 526037034 THE HARRY & JEANETTE WEINBERG FOUNDATION: 0.588 -> 0.626
