# Universe summary

Built 2026-10-10 by `scripts/20_build_universes.py` from the IRS EO BMF and IRS e-file index (releases 2021–2026). Rules live in `config/universes.yaml`.

- Calvary revenue median TY2022–24: $4,967,995; size band $2,483,998–$9,935,990.
- Recent filing = BMF TAX_PERIOD or e-filed return period ≥ 202101.
- ZIP→county: Census 2020 ZCTA–county relationship, primary county by land area. Unresolved ZIPs among DMV-state rows: 31.

| Universe | Rule | EINs |
|---|---|---|
| calvary | SUBJ | 1 |
| calvary_known_funders | KF1 | 68 |
| calvary_known_funders | KF2 | 20 |
| core_peers | CP1 | 18 |
| daf_sponsors | DAF1 | 15 |
| dc_sector | DCS1 | 896 |
| dc_sector | DCS2 | 131 |
| dmv_funders | F1 | 5,855 |
| dmv_funders | F2 | 1,847 |
| dmv_funders | F3 | 3 |
| dmv_sector | DMV1 | 4,250 |
| dmv_sector | DMV2 | 660 |
| named_comparators | NC1 | 2 |
| national_women | NW1 | 1,118 |
| national_women | NW2 | 1,326 |
| national_women | NW3 | 8 |
| national_women | NW4 | 426 |
| size_matched | SZ1 | 566 |

| Universe | Distinct EINs |
|---|---|
| calvary | 1 |
| calvary_known_funders | 88 |
| core_peers | 18 |
| daf_sponsors | 15 |
| dc_sector | 1,027 |
| dmv_funders | 7,705 |
| dmv_sector | 4,910 |
| named_comparators | 2 |
| national_women | 2,878 |
| size_matched | 566 |

Distinct EINs across all universes: 15,812. E-file returns (periods ending 2020-12+) for these EINs: 45,305.
