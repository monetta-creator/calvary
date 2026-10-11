# Data inventory

Generated 2026-10-10 by `scripts/80_docs.py`. Plain-language summary of what is in `clean/`.

## Organizations and universes

- 105,189 organizations in `dim_org` (every EIN in a universe or referenced by a fact table).
- `dmv_funders`: 7,705 organizations
- `dmv_sector`: 4,910 organizations
- `national_women`: 2,878 organizations
- `dc_sector`: 1,027 organizations
- `size_matched`: 566 organizations
- `calvary_known_funders`: 88 organizations
- `core_peers`: 18 organizations
- `daf_sponsors`: 15 organizations
- `named_comparators`: 2 organizations
- `calvary`: 1 organizations

## Financial time series (`fact_org_financials`)

- 150,461 rows (88,451 preferred org-years) for 10,045 organizations; fiscal years 2002–2026.
- Rows by source: {'bulk_irs_soi_extract': 78109, 'bulk_gt_datalake': 24026, 'bulk_nccs_efile': 22573, 'api_propublica': 18279, 'bulk_irs_xml': 7457, 'web_calvary_fy14_audit': 2, 'input_990_ty2014': 1, 'input_fy15_audit': 1, 'input_990_ty2015': 1, 'input_fy16_audit': 1, 'input_fy17_audit': 1, 'input_990_ty2017': 1, 'input_fy18_audit': 1, 'input_990_ty2018': 1, 'input_fy19_audit': 1, 'input_990_ty2019': 1, 'input_fy20_audit': 1, 'input_fy21_audit': 1, 'web_calvary_fy22_audit': 1, 'input_fy23_audit': 1, 'input_propublica_990_ty2024': 1}.

## Grants (`fact_grants`)

- 928,658 grant rows, $101,615,645,610 in annual (non-cumulative) amounts.
- By source type: {'pf_grants_paid': 702373, 'schedule_i': 204344, 'pf_grants_approved_future': 20170, 'annual_report': 1053, 'support_page': 380, 'crm': 160, 'web': 149, 'audit_note': 29}.
- Funder tax years: 2012–2025.
- Distinct funders: 5,463; distinct recipients with EIN: 91,430.
- Grants to Calvary: 778 rows.

## Government funding

- `fact_gov_awards`: 40,300 rows; by source: {'usaspending': 17895, 'dc_pass': 9988, 'fac_sefa': 9851, 'dc_ovsjg': 1385, 'treasury_slfrf': 461, 'dc_oversight': 442, 'hud_coc': 270, 'audit_sefa': 8}; by flow: {'prime': 11720, 'subaward': 11520, 'dc_contract': 8682, 'pass_through_expenditure': 5367, 'dc_local_grant': 3011}.
- `fact_opportunities`: 286 open/forecast federal opportunities.
- `fact_policy_events`: 297 dated DC budget/policy events.

## Governance

- `dim_person`: 48,563 people; `fact_roles`: 163,473 role rows; people linked across 2+ organizations: 2,036.
- `fact_org_relationships`: 544,041 rows by type {'grant': 432430, 'daf_sponsor_grant': 90830, 'schedule_r_related': 12864, 'shared_board_member': 4162, 'pass_through_funding': 3755}.

## Funders (`dim_funder`)

- 8,928 funders by type: {'private_foundation': 5851, 'public_charity_grantmaker': 1766, 'other': 772, 'community_foundation': 179, 'corporate': 126, 'corporate_foundation': 106, 'federated_giving': 93, 'daf_sponsor': 15, 'civic_association': 9, 'government_agency': 6, 'faith': 5}.

## Dimensions for slicing

- Organization: NTEE (`ntee3`, `ntee_label`), org class, size (`bmf_revenue_amt`), geography (state, county, DC ward, tract), universe membership.
- Time: `tax_year` / `fiscal_year` on every fact; `dim_period` maps calendar years to CPI deflators and federal/DC/Calvary fiscal-year labels.
- Geography: `dim_geo` (nation, state, DC MSA, counties, DC wards, DC tracts) with ACS 2020-2024 context.
- Program area: `program_area_tags` on grants, awards, opportunities and policy events (`dim_program_area`).
- Funder type: `dim_funder.funder_type`.

## Supplementary tables

- `supp_calvary_individual_donor_bands.csv`: 4 rows
- `supp_calvary_program_metrics.csv`: 178 rows
- `supp_calvary_strategic_targets.csv`: 18 rows
- `supp_crm_cash_verification.csv`: 160 rows
- `supp_dc_budget_lines.csv`: 5,172 rows
- `supp_hic_projects.csv`: 1,257 rows
- `supp_homeless_counts.csv`: 49,393 rows
