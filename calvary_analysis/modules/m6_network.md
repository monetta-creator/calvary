# M6 readout: network analysis

Script `scripts/06_m6_network.py`. Tables `chart_data/m6_01_central_funders.csv`, `m6_04_board_interlocks.csv`, `m6_05_relationship_paths.csv`; charts `charts/m6_02_cofunding_overlap.png`, `m6_03_network.png`. Insights M6-01 to M6-03.

## Question
Which funders sit at the center of the web around Calvary and its peers, which peers share Calvary's funders, how much do board interlocks add, and how strong is the relationship path to each candidate funder?

## Method
- Bipartite graph: funders × 19 recipients (Calvary + 18 provisional peers), edges = filed grants TY2020–24 (990-PF, Schedule I; landscape exclusions applied). Degree = organizations funded; betweenness on the unweighted graph.
- Co-funding overlap per peer: shared institutional funders with Calvary (DAF sponsors excluded), Jaccard, and the peer's institutional funders that do not fund Calvary.
- Board interlocks from `fact_org_relationships` (`shared_board_member`), restricted to links touching Calvary, a peer or a named comparator. Person records are matched in Prompt 1 only on an exact normalized name plus a corroborating signal; **leadership materials use high-confidence links only; medium links are labeled "unconfirmed" and go to the consulting team.** No names are stored in the analysis outputs (person_id only).
- Relationship-path score per candidate funder (0–1): 0.40 × peers funded (cap 12) + 0.25 × close peers funded (peers sharing ≥5 institutional funders with Calvary; cap 8) + 0.25 × Calvary's current institutional funders whose grantee sets overlap the candidate's by ≥2 (cap 20) + 0.10 × any high-confidence board link. Consulting variant adds 0.05 for a medium link.

## Findings
1. **Central funders** (M6-01): 330 funders connect the 19 organizations. By organizations funded: GWCF 18, Benevity/AOGF 18, Schwab DAF 16, Cafritz 14, Vanguard 13, NPT 13, United Way NCA 13, Blackbaud Giving Fund 11, Venable Foundation 10, Bank of America 10, Abell 9, T. Rowe Price Program 8, Fowler 8, Gifts for the Homeless 8. Every one of these funds Calvary except Venable, T. Rowe Price, Gifts for the Homeless and (further down) Capital Area Food Bank, America's Charities, JPMorgan Chase, Clark. Calvary is in the core of the web, not at its edge.
2. **Overlap** (M6-02): Calvary shares the most institutional funders with Miriam's Kitchen (17), DASH (14), House of Ruth DC (14), New Endeavors by Women (12) and My Sister's Place (12). The longest lists of institutional funders Calvary lacks belong to House of Ruth MD (81), House of Ruth DC (69), Miriam's Kitchen (48), N Street Village (45), Community of Hope (33), Doorways (29).
3. **Board interlocks are thin** (M6-03): Calvary has 8 shared-board links in filings, 1 at high confidence (Clean Power Institute, not a funder) and 7 at medium confidence (Washington Area Women's Foundation, United Way NCA, United Way of Central Maryland, DAVIS Construction Foundation, Charter School Incubator Initiative, Miriam's Kitchen, Dress for Success). Across all 19 organizations, 27 interlocks touch a funder, 3 at high confidence. `candidate_interlocks` (low confidence) has one row touching the peer set and none touching Calvary. The 17 board-employer overlaps noted in Prompt 1 (Capital One, DAVIS, Venable, KPMG, Baker Tilly…) come from annual-report board lists and are a stronger lead than filings, but they are corporate relationships, not foundation boards.
4. **Paths** (m6_05): the strongest paths to non-funders run through peers: Venable (10 peers, 9 close, 22 overlapping co-funders), T. Rowe Price Program (8/7/16), JPMorgan Chase (7/7/15), Capital Area Food Bank, America's Charities, Clark (5/5/14), Give Lively, Schattner, Bunting, Bechtel. Among current funders the deepest embedded are GWCF, Cafritz, Abell, Fowler, Bank of America and United Way NCA.

## Charts and tables
`m6_02_cofunding_overlap`, `m6_03_network` (58 funders of 3+ organizations; PNG), `m6_01_central_funders.csv`, `m6_03_network_nodes.csv`, `m6_04_board_interlocks.csv`, `m6_05_relationship_paths.csv`.

## Caveats
- The graph covers DMV funders' filings; corporate giving and DAF-routed individual gifts are only partly visible.
- Interlocks depend on name matching; a medium-confidence match may be two different people. Treat as leads.
- Path weights are analyst choices (documented in the manifest note); M7 lets them be reweighted.

## Confidence
High on the graph and overlap counts; high that board paths are thin; medium on the path-strength construct.
