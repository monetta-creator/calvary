# M4 readout: funder landscape (DC and DMV)

Script `scripts/04_m4_landscape.py`. Landscape table `chart_data/m4_00_funder_landscape_table.csv`; charts `charts/m4_*.png`. Insights M4-01 to M4-05.

## Question
Who funds Calvary's space in DC and the DMV, at what scale, how concentrated is it, and how has it moved TY2020–24?

## Method
- Base: `fact_grants` rows from funders' own filings (990-PF grants paid, Schedule I), TY2020–24, non-cumulative, excluding two funders listed in `config/landscape_exclusions.csv` (the Gates Foundation, whose DC recipients are global-development and research organizations and which is in the data only because it appears in Calvary's CRM; and TCP, a government pass-through).
- Lens A: grants to the 1,027 `dc_sector` organizations (DC public charities in homelessness, housing, DV, human services and adjacent NTEE codes). Lens B: grants to DC/MD/VA recipients whose purpose text is tagged housing, DV or women.
- Funder types from `dim_funder`; DAF sponsors (Fidelity, Schwab, Benevity/AOGF, NPT, Vanguard…) are donor intermediaries and are reported separately from institutional decision-makers.
- Institutional landscape table: one row per institutional funder with dollars, recipients, years active, median/p75/max grant, mission-tagged dollars, whether it funds Calvary, number of core peers funded, "see attached" years, and DMV/DC share of all its giving.

## Findings
1. **Scale** (M4-01): about $132M a year flows from DMV funders into DC-sector organizations ($660M TY2020–24), 58% of it through DAF sponsors and 42% ($276M) from 555 institutional funders. Institutional dollars to the sector ran $50–52M a year in TY2020–23 and $72M in TY2024 even with partial TY2024 filings.
2. **Concentration** (M4-02): the top 10 institutional funders give about half of institutional dollars to the DC sector. Of the 25 largest, 6 already fund Calvary (GWCF, Cafritz, Bank of America, United Way NCA, Jane Bancroft Robinson, Abell). The largest non-funders are Clark Charitable ($32.8M to 20 DC organizations, 5 core peers), JPMorgan Chase Foundation ($18.0M, mostly matching gifts), Wal-Mart, Annie E. Casey, Weinberg, Morningstar, Diana Davis Spencer, Meyer, Capital Area Food Bank, Wells Fargo, Bernstein, The Washington Home, Schattner, Cohen.
3. **Grant size** (M4-03): the median institutional grant to a DC-sector organization is ~$15K (private foundations $10K, community foundations $40K); six-figure grants are the top decile. A $0.5M/yr increase in institutional revenue is a handful of six-figure, multi-year relationships, not dozens of $10K grants.
4. **DAF channel** (M4-04): Fidelity Charitable moved $179M into DC-sector organizations in five years, NPT $80M, Benevity $49M, Schwab $36M. This is individual-donor money routed through sponsors; Calvary's $1.1M over five years (25% of its filed grants) tracks its major donors.
5. **Purpose** (M4-05): most institutional money is general operating or untagged; dollars whose purpose names housing, DV or women are a minority. The biggest mission-tagged funders in the DMV (Weinberg, The Community Foundation, Clark, Wells Fargo, Abell) are mostly Maryland and Virginia foundations, several of which give little in DC.

## Charts
`m4_01_dc_sector_by_year`, `m4_03_top_institutional_funders`, `m4_04_concentration`, `m4_05_grant_size_by_type`, `m4_06_daf_sponsors`, `m4_07_purpose_tags`, `m4_08_mission_tagged_funders`; tables `m4_00_funder_landscape_table.csv`, `m4_02_dc_sector_by_funder_type.csv`.

## Caveats
- Funder tax years; TY2024 partial, TY2025 excluded.
- "See attached" filers (476 returns / 667 rows, ~$3.5B DMV-wide) have no recipient names, so a few large DC funders (Philip L. Graham, Clark-Winchcole, Bank of America in some years) are under-counted.
- Corporate giving without a foundation vehicle is invisible here (it appears only in Calvary's CRM and peers' donor lists).
- The sector universe includes DC-based national organizations; Gates is excluded for this reason, and a few other research-oriented recipients remain.

## Confidence
High on totals, concentration and grant sizes; medium on purpose tags (keyword-based) and on the mission-tagged lens.
