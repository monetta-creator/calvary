# Data quality report

Generated 2026-10-10 by `scripts/70_quality_checks.py`.

## 1. Row counts

| table | rows |
|---|---|
| dim_org | 105189 |
| dim_funder | 8928 |
| dim_period | 28 |
| dim_geo | 246 |
| dim_program_area | 13 |
| dim_person | 48563 |
| fact_org_financials | 150461 |
| fact_grants | 928658 |
| fact_gov_awards | 40300 |
| fact_opportunities | 286 |
| fact_policy_events | 297 |
| fact_roles | 163473 |
| fact_org_relationships | 544041 |
| entity_aliases | 231647 |
| dim_universe_membership | 17210 |
| supp_calvary_individual_donor_bands | 4 |
| supp_calvary_program_metrics | 178 |
| supp_calvary_strategic_targets | 18 |
| supp_crm_cash_verification | 160 |
| supp_dc_budget_lines | 5172 |
| supp_hic_projects | 1257 |
| supp_homeless_counts | 49393 |
| candidate_interlocks | 1270 |
| entity_aliases | 231678 |


### Rows per source (fact tables)

| table | source_id | rows |
|---|---|---|
| fact_org_financials | bulk_irs_soi_extract | 78109 |
| fact_org_financials | bulk_gt_datalake | 24026 |
| fact_org_financials | bulk_nccs_efile | 22573 |
| fact_org_financials | api_propublica | 18279 |
| fact_org_financials | bulk_irs_xml | 7457 |
| fact_org_financials | web_calvary_fy14_audit | 2 |
| fact_org_financials | input_990_ty2014 | 1 |
| fact_org_financials | input_fy15_audit | 1 |
| fact_org_financials | input_990_ty2015 | 1 |
| fact_org_financials | input_fy16_audit | 1 |
| fact_org_financials | input_fy17_audit | 1 |
| fact_org_financials | input_990_ty2017 | 1 |
| fact_org_financials | input_fy18_audit | 1 |
| fact_org_financials | input_990_ty2018 | 1 |
| fact_org_financials | input_fy19_audit | 1 |
| fact_org_financials | input_990_ty2019 | 1 |
| fact_org_financials | input_fy20_audit | 1 |
| fact_org_financials | input_fy21_audit | 1 |
| fact_org_financials | web_calvary_fy22_audit | 1 |
| fact_org_financials | input_fy23_audit | 1 |
| fact_org_financials | input_propublica_990_ty2024 | 1 |
| fact_grants | bulk_gt_datalake | 792368 |
| fact_grants | bulk_irs_xml | 134519 |
| fact_grants | web_nc_dwc_ar_2024 | 202 |
| fact_grants | input_crm_funders_2023_2026 | 160 |
| fact_grants | web_peer_hordc_ar_2025 | 160 |
| fact_grants | web_peer_coh_funders | 151 |
| fact_grants | web_nc_dwc_ar_web | 148 |
| fact_grants | web_peer_heartly_ar_fy25 | 145 |
| fact_grants | input_corp_found_support_2023 | 98 |
| fact_grants | web_calvary_corp_found_support | 98 |
| fact_grants | web_peer_nsv_ar_fy25 | 96 |
| fact_grants | web_peer_nsv_ar_fy24 | 93 |
| fact_grants | input_fy15_annual_report | 73 |
| fact_grants | web_calvary_fy14_annual_report | 72 |
| fact_grants | web_calvary_hope_awards_2017_sponsorship | 40 |
| fact_grants | web_calvary_hope_gala_2025_sponsorship | 39 |
| fact_grants | web_peer_msp_impact_fy23 | 35 |
| fact_grants | web_nc_dwc_gala_2026 | 29 |
| fact_grants | web_peer_cfh_ar_2025 | 26 |
| fact_grants | web_funder_graham_recent | 14 |
| fact_grants | web_funder_cafritz_recent | 12 |
| fact_grants | web_funder_gwcf_hef_partners | 6 |
| fact_grants | input_fy23_audit | 5 |
| fact_grants | input_fy16_audit | 4 |
| fact_grants | input_fy17_audit | 4 |
| fact_gov_awards | bulk_usaspending | 17895 |
| fact_gov_awards | api_dcgis_pass | 9988 |
| fact_gov_awards | api_fac | 9851 |
| fact_gov_awards | api_dcgis_ovsjg_grants | 1267 |
| fact_gov_awards | bulk_treasury_slfrf | 461 |
| fact_gov_awards | doc_dc_council_oversight | 442 |
| fact_gov_awards | doc_hud_coc_awards | 270 |
| fact_gov_awards | doc_ovsjg_recipients | 118 |
| fact_gov_awards | input_fy23_audit | 4 |
| fact_gov_awards | web_calvary_fy22_audit | 4 |
| fact_opportunities | api_grantsgov | 286 |
| fact_policy_events | doc_dc_budget_fy2026 | 62 |
| fact_policy_events | doc_dc_budget_fy2024 | 55 |
| fact_policy_events | doc_dc_council_budget_reports | 55 |
| fact_policy_events | doc_dc_budget_fy2025 | 52 |
| fact_policy_events | doc_dc_budget_fy2027 | 48 |
| fact_policy_events | doc_dc_bsa | 25 |
| fact_roles | bulk_gt_datalake | 126196 |
| fact_roles | bulk_irs_xml | 37195 |
| fact_roles | input_fy21_annual_report | 23 |
| fact_roles | input_fy20_annual_report | 21 |
| fact_roles | input_fy17_annual_report | 19 |
| fact_roles | input_fy23_annual_report | 19 |
| fact_org_relationships | bulk_gt_datalake | 447164 |
| fact_org_relationships | bulk_irs_xml | 92763 |
| fact_org_relationships | bulk_usaspending | 3652 |
| fact_org_relationships | doc_hud_coc_awards | 89 |
| fact_org_relationships | web_peer_coh_funders | 44 |
| fact_org_relationships | web_nc_dwc_ar_2024 | 42 |
| fact_org_relationships | web_peer_hordc_ar_2025 | 41 |
| fact_org_relationships | web_calvary_fy14_annual_report | 34 |
| fact_org_relationships | web_nc_dwc_ar_2024;web_nc_dwc_ar_web | 29 |
| fact_org_relationships | input_fy15_annual_report | 26 |
| fact_org_relationships | web_peer_heartly_ar_fy25 | 20 |
| fact_org_relationships | web_nc_dwc_ar_web | 19 |
| fact_org_relationships | doc_dc_council_oversight | 14 |
| fact_org_relationships | web_peer_msp_impact_fy23 | 12 |
| fact_org_relationships | web_peer_nsv_ar_fy25 | 11 |
| fact_org_relationships | web_peer_nsv_ar_fy24;web_peer_nsv_ar_fy25 | 10 |
| fact_org_relationships | bulk_gt_datalake;bulk_irs_xml | 10 |
| fact_org_relationships | web_peer_nsv_ar_fy24 | 10 |
| fact_org_relationships | web_funder_cafritz_recent | 10 |
| fact_org_relationships | web_funder_graham_recent | 9 |
| fact_org_relationships | web_peer_cfh_ar_2025 | 7 |
| fact_org_relationships | web_funder_gwcf_hef_2022_some | 3 |
| fact_org_relationships | web_nc_dwc_ar_2024;web_nc_dwc_gala_2026 | 3 |
| fact_org_relationships | web_nc_dwc_ar_2024;web_nc_dwc_ar_web;web_nc_dwc_gala_2025 | 2 |
| fact_org_relationships | input_fy15_annual_report;web_calvary_step_up_dc_2016 | 2 |


## 2. Missing-value rates (share of empty cells per column; columns > 0% only)

| table | column | null_rate |
|---|---|---|
| dim_org | org_name | 6.3% |
| dim_org | org_name_bmf | 6.3% |
| dim_org | dba_name | 45.5% |
| dim_org | street | 6.3% |
| dim_org | city | 6.3% |
| dim_org | state | 6.4% |
| dim_org | zip5 | 6.3% |
| dim_org | county_fips | 85.0% |
| dim_org | ward | 98.3% |
| dim_org | tract_geoid | 89.9% |
| dim_org | lat | 89.9% |
| dim_org | lon | 89.9% |
| dim_org | geo_method | 85.0% |
| dim_org | ntee_cd | 21.2% |
| dim_org | ntee3 | 21.2% |
| dim_org | ntee_label | 23.2% |
| dim_org | subsection | 6.3% |
| dim_org | foundation_code | 6.3% |
| dim_org | org_class | 6.3% |
| dim_org | ruling_year | 6.3% |
| dim_org | website | 94.6% |
| dim_org | mission | 98.6% |
| dim_org | fye_month | 90.7% |
| dim_org | latest_tax_year | 90.7% |
| dim_org | latest_return_type | 90.7% |
| dim_org | bmf_revenue_amt | 21.0% |
| dim_org | universes | 85.0% |
| dim_funder | ein | 9.8% |
| dim_funder | state | 9.8% |
| dim_funder | county_fips | 12.1% |
| dim_funder | ward | 89.9% |
| dim_funder | issue_focus_tags | 50.7% |
| dim_funder | universes | 11.7% |
| dim_funder | source_id | 38.8% |
| dim_period | cpi_u_us | 7.1% |
| dim_period | cpi_u_dc_metro | 60.7% |
| dim_period | deflator_to_2024_us | 7.1% |
| dim_period | notes | 35.7% |
| dim_period | x_deflator_to_2024_dc_metro | 60.7% |
| dim_period | x_cpi_us_series | 7.1% |
| dim_period | x_cpi_dc_series | 60.7% |
| dim_geo | state_fips | 0.8% |
| dim_geo | county_fips | 2.4% |
| dim_geo | tract_geoid | 15.4% |
| dim_geo | ward | 13.0% |
| dim_geo | female_poverty_rate | 0.8% |
| dim_geo | median_hh_income | 3.7% |
| dim_geo | rent_burden_30plus_share | 0.8% |
| dim_geo | rent_burden_50plus_share | 0.8% |
| dim_geo | female_hh_no_spouse_share | 0.8% |
| dim_geo | female_poverty_rate_moe | 0.8% |
| dim_geo | median_hh_income_moe | 6.9% |
| dim_geo | rent_burden_30plus_share_moe | 0.8% |
| dim_geo | rent_burden_50plus_share_moe | 0.8% |
| dim_geo | female_hh_no_spouse_share_moe | 0.8% |
| dim_geo | x_state_abbr | 98.4% |
| dim_geo | x_county_geoid | 2.4% |
| dim_geo | x_cbsa_code | 90.2% |
| dim_geo | x_in_msa | 89.4% |
| dim_geo | x_in_scope | 90.7% |
| dim_geo | x_metro_division | 90.7% |
| dim_geo | x_metro_division_code | 90.7% |
| dim_geo | x_central_outlying | 90.7% |
| dim_geo | x_scope_note | 98.4% |
| dim_geo | x_ward_majority_pop_share | 16.3% |
| dim_geo | x_split_ward | 16.3% |
| dim_geo | x_in_service_area | 13.0% |
| dim_geo | x_outside_dmv | 0.4% |
| dim_geo | x_named_comparator_ein | 98.8% |
| dim_geo | x_adult_female_poverty_rate | 0.8% |
| dim_geo | x_adult_female_poverty_rate_moe | 0.8% |
| dim_geo | x_female_hh_family_poverty_rate | 4.5% |
| dim_geo | x_female_hh_family_poverty_rate_moe | 4.5% |
| dim_geo | x_female_veteran_share | 0.4% |
| dim_geo | x_female_veteran_share_moe | 0.4% |
| dim_geo | x_female_living_alone_share_of_householders | 0.8% |
| dim_geo | x_female_living_alone_share_of_householders_moe | 0.8% |
| dim_geo | x_median_hh_income_annotation | 93.1% |
| dim_geo | x_county_fips_3 | 2.4% |
| dim_program_area | keywords | 7.7% |
| dim_program_area | ntee3_codes | 15.4% |
| dim_program_area | assistance_listings | 38.5% |
| dim_person | middle_initial | 72.6% |
| dim_person | last_name | 0.2% |
| dim_person | suffix | 95.6% |
| fact_org_financials | object_id | 64.1% |
| fact_org_financials | is_amended | 79.1% |
| fact_org_financials | total_revenue | 0.0% |
| fact_org_financials | contributions_total | 7.8% |
| fact_org_financials | federated_campaigns | 84.5% |
| fact_org_financials | membership_dues | 77.0% |
| fact_org_financials | fundraising_event_contributions | 84.2% |
| fact_org_financials | related_org_contributions | 84.6% |
| fact_org_financials | government_grants | 83.9% |
| fact_org_financials | other_contributions | 82.3% |
| fact_org_financials | noncash_contributions | 84.1% |
| fact_org_financials | program_service_revenue | 48.1% |
| fact_org_financials | investment_income | 4.1% |
| fact_org_financials | special_events_net | 50.2% |
| fact_org_financials | other_revenue | 42.4% |
| fact_org_financials | total_expenses | 15.1% |
| fact_org_financials | program_expenses | 95.7% |
| fact_org_financials | management_expenses | 96.8% |
| fact_org_financials | fundraising_expenses | 96.8% |
| fact_org_financials | grants_paid | 28.5% |
| fact_org_financials | compensation_total | 65.6% |
| fact_org_financials | total_assets_eoy | 15.0% |
| fact_org_financials | total_liabilities_eoy | 15.4% |
| fact_org_financials | net_assets_eoy | 15.0% |
| fact_org_financials | cash_savings_eoy | 60.3% |
| fact_org_financials | pf_fmv_assets_eoy | 52.6% |
| fact_org_financials | pf_total_grants_paid | 52.6% |
| fact_org_financials | pf_qualifying_distributions | 87.4% |
| fact_org_financials | pf_contributions_received | 60.2% |
| fact_org_financials | gov_share_of_revenue | 85.1% |
| fact_org_financials | months_of_cash | 76.8% |
| fact_org_financials | revenue_growth_yoy | 52.3% |
| fact_org_financials | program_expense_ratio | 95.8% |
| fact_org_financials | total_revenue_real_2024 | 0.1% |
| fact_org_financials | government_grants_real_2024 | 83.9% |
| fact_org_financials | total_expenses_real_2024 | 15.1% |
| fact_org_financials | notes | 0.0% |
| fact_grants | funder_ein | 0.1% |
| fact_grants | recipient_ein | 27.5% |
| fact_grants | recipient_name_raw | 4.0% |
| fact_grants | recipient_name_norm | 4.8% |
| fact_grants | recipient_city | 5.0% |
| fact_grants | recipient_state | 2.3% |
| fact_grants | recipient_zip5 | 7.0% |
| fact_grants | tax_year | 0.2% |
| fact_grants | fiscal_year | 0.0% |
| fact_grants | grant_date | 100.0% |
| fact_grants | amount | 0.2% |
| fact_grants | amount_band_min | 99.9% |
| fact_grants | amount_band_max | 100.0% |
| fact_grants | amount_real_2024 | 1.0% |
| fact_grants | purpose_text | 0.4% |
| fact_grants | program_area_tags | 0.4% |
| fact_grants | object_id | 0.2% |
| fact_grants | match_score | 49.1% |
| fact_gov_awards | recipient_ein | 9.1% |
| fact_gov_awards | recipient_uei | 31.1% |
| fact_gov_awards | awarding_agency | 0.1% |
| fact_gov_awards | funding_agency | 52.1% |
| fact_gov_awards | program_name | 8.6% |
| fact_gov_awards | assistance_listing | 28.9% |
| fact_gov_awards | award_id | 19.7% |
| fact_gov_awards | award_type | 20.9% |
| fact_gov_awards | pass_through_entity | 58.1% |
| fact_gov_awards | pass_through_ein | 76.0% |
| fact_gov_awards | period_start | 60.3% |
| fact_gov_awards | period_end | 60.3% |
| fact_gov_awards | fiscal_year | 0.1% |
| fact_gov_awards | amount_real_2024 | 5.2% |
| fact_opportunities | eligibility_text | 15.7% |
| fact_opportunities | award_floor | 55.6% |
| fact_opportunities | award_ceiling | 48.3% |
| fact_opportunities | estimated_total_funding | 46.9% |
| fact_opportunities | expected_awards | 50.0% |
| fact_opportunities | close_date | 6.3% |
| fact_opportunities | forecast_award_date | 66.4% |
| fact_policy_events | event_date | 2.7% |
| fact_policy_events | agency | 0.3% |
| fact_policy_events | program_code | 33.3% |
| fact_policy_events | funding_stream | 20.2% |
| fact_policy_events | amount | 40.4% |
| fact_policy_events | prior_amount | 42.8% |
| fact_policy_events | amount_change | 11.1% |
| fact_roles | tax_year | 0.1% |
| fact_roles | title | 0.0% |
| fact_roles | is_key_employee | 62.9% |
| fact_roles | is_highest_comp | 61.2% |
| fact_roles | is_former | 62.9% |
| fact_roles | avg_hours_per_week | 0.7% |
| fact_roles | reportable_comp_org | 0.1% |
| fact_roles | object_id | 0.1% |
| fact_org_relationships | org_a_name | 0.6% |
| fact_org_relationships | org_b_ein | 0.2% |
| fact_org_relationships | org_b_name | 3.1% |
| fact_org_relationships | tax_year | 0.1% |
| fact_org_relationships | amount | 2.8% |
| fact_org_relationships | person_id | 99.2% |
| fact_org_relationships | notes | 96.9% |
| entity_aliases | alias_name_norm | 0.0% |
| entity_aliases | alias_city | 3.6% |
| entity_aliases | alias_state | 5.5% |
| entity_aliases | canonical_id | 40.4% |
| entity_aliases | canonical_name | 40.4% |
| dim_universe_membership | city | 0.0% |
| dim_universe_membership | state | 0.0% |
| dim_universe_membership | zip5 | 0.0% |
| dim_universe_membership | county_fips | 0.2% |
| dim_universe_membership | ntee_cd | 6.5% |
| dim_universe_membership | ntee3 | 6.5% |
| dim_universe_membership | subsection | 0.0% |
| dim_universe_membership | foundation_code | 0.0% |
| dim_universe_membership | ruling_yyyymm | 0.0% |
| dim_universe_membership | bmf_revenue_amt | 38.8% |
| dim_universe_membership | bmf_asset_amt | 7.9% |
| dim_universe_membership | bmf_tax_period | 7.8% |
| dim_universe_membership | latest_efile_tax_period | 38.0% |
| dim_universe_membership | latest_efile_return_type | 38.0% |


## 3. Duplicate primary keys

| table | key | duplicate_rows |
|---|---|---|
| dim_org | ein | 0 |
| dim_funder | funder_id | 0 |
| dim_period | year | 0 |
| dim_geo | geo_id | 0 |
| dim_program_area | program_area | 0 |
| dim_person | person_id | 0 |
| dim_universe_membership | universe+ein+rule_id | 0 |
| fact_org_financials | ein+fiscal_year+fye_month+return_type+source_id+object_id | 0 |
| fact_grants | grant_id | 0 |
| fact_gov_awards | award_row_id | 0 |
| fact_opportunities | opportunity_id | 0 |
| fact_policy_events | event_id | 0 |
| fact_roles | role_id | 0 |
| fact_org_relationships | rel_id | 0 |


## 4. Calvary financial reconciliation across sources

One row per fiscal year (FYE Sept 30) and source. `diff_vs_xml` = total revenue relative to the e-filed XML where available, else to the preferred row. Audits differ from 990s by design (in-kind treatment, release of restrictions); differences >1% are flagged, not corrected.

| fiscal_year | return_type | source_id | total_revenue | total_expenses | net_assets_eoy | government_grants | diff_vs_xml | flag |
|---|---|---|---|---|---|---|---|---|
| 2011 | 990 | api_propublica | 1445107.0 | 1065764.0 | 1117933.0 | nan | 0.0 |  |
| 2011 | 990 | bulk_irs_soi_extract | 1445107.0 | 1065764.0 | 1117933.0 | nan | 0.0 |  |
| 2012 | 990 | api_propublica | 2021027.0 | 1144102.0 | 2171801.0 | nan | 0.0 |  |
| 2012 | 990 | bulk_irs_soi_extract | 2021027.0 | 1144102.0 | 2171801.0 | nan | 0.0 |  |
| 2013 | 990 | api_propublica | 1886681.0 | 1464641.0 | 2593841.0 | nan | 0.0 |  |
| 2013 | 990 | bulk_irs_soi_extract | 1886681.0 | 1464641.0 | 2593841.0 | nan | 0.0 |  |
| 2013 | audit | web_calvary_fy14_audit | 2056534.0 | 1634494.0 | 2593841.0 | 813088.0 | 0.09 | DIFF>1% |
| 2014 | 990 | api_propublica | 2072635.0 | 1705571.0 | 2960905.0 | nan | 0.0 |  |
| 2014 | 990 | bulk_irs_soi_extract | 2072635.0 | 1705571.0 | 2960905.0 | nan | 0.0 |  |
| 2014 | audit | web_calvary_fy14_audit | 2217472.0 | 1850408.0 | 2960905.0 | 829432.0 | 0.0699 | DIFF>1% |
| 2015 | 990 | api_propublica | 2008601.0 | 1879006.0 | 3090500.0 | nan | 0.0 |  |
| 2015 | 990 | bulk_gt_datalake | 2008601.0 | 1879006.0 | 3090500.0 | 888295.0 | 0.0 |  |
| 2015 | 990 | bulk_irs_soi_extract | 2008601.0 | 1879006.0 | 3090500.0 | nan | 0.0 |  |
| 2015 | 990 | bulk_nccs_efile | 2008601.0 | nan | nan | 888295.0 | 0.0 |  |
| 2015 | 990_pdf | input_990_ty2014 | nan | nan | nan | 888295.0 | nan |  |
| 2015 | audit | input_fy15_audit | 2173996.0 | 2044401.0 | 3090500.0 | 888295.0 | 0.0823 | DIFF>1% |
| 2016 | 990 | api_propublica | 1990443.0 | 1989199.0 | 3091744.0 | nan | 0.0 |  |
| 2016 | 990 | bulk_gt_datalake | 1990443.0 | 1989199.0 | 3091744.0 | 932814.0 | 0.0 |  |
| 2016 | 990 | bulk_irs_soi_extract | 1990443.0 | 1989199.0 | 3091744.0 | nan | 0.0 |  |
| 2016 | 990 | bulk_nccs_efile | 1990443.0 | nan | nan | 932814.0 | 0.0 |  |
| 2016 | 990_pdf | input_990_ty2015 | nan | nan | nan | 932814.0 | nan |  |
| 2016 | audit | input_fy16_audit | 2130506.0 | 2129262.0 | 3091744.0 | 932814.0 | 0.0704 | DIFF>1% |
| 2017 | 990 | api_propublica | 2259177.0 | 2076427.0 | 3274494.0 | nan | 0.0 |  |
| 2017 | 990 | bulk_gt_datalake | 2259177.0 | 2076427.0 | 3274494.0 | 965548.0 | 0.0 |  |
| 2017 | 990 | bulk_irs_soi_extract | 2259177.0 | 2076427.0 | 3274494.0 | nan | 0.0 |  |
| 2017 | 990 | bulk_nccs_efile | 2259177.0 | nan | nan | 965548.0 | 0.0 |  |
| 2017 | audit | input_fy17_audit | 2432385.0 | 2249635.0 | 3274494.0 | 965548.0 | 0.0767 | DIFF>1% |
| 2018 | 990 | api_propublica | 2153899.0 | 2152260.0 | 3276133.0 | nan | 0.0 |  |
| 2018 | 990 | bulk_gt_datalake | 2153899.0 | 2152260.0 | 3276133.0 | 979272.0 | 0.0 |  |
| 2018 | 990 | bulk_irs_soi_extract | 2153899.0 | 2152260.0 | 3276133.0 | nan | 0.0 |  |
| 2018 | 990 | bulk_nccs_efile | 2153899.0 | nan | nan | 979272.0 | 0.0 |  |
| 2018 | 990_pdf | input_990_ty2017 | 2153899.0 | 2152260.0 | 3276133.0 | 979272.0 | 0.0 |  |
| 2018 | audit | input_fy18_audit | 2352225.0 | 2350586.0 | 3276133.0 | 979272.0 | 0.0921 | DIFF>1% |
| 2019 | 990 | api_propublica | 2486678.0 | 2403977.0 | 3358790.0 | nan | 0.0 |  |
| 2019 | 990 | bulk_gt_datalake | 2486678.0 | 2403977.0 | 3358790.0 | 1256102.0 | 0.0 |  |
| 2019 | 990 | bulk_irs_soi_extract | 2486678.0 | 2403977.0 | 3358790.0 | nan | 0.0 |  |
| 2019 | 990 | bulk_nccs_efile | 2486678.0 | nan | nan | 1256102.0 | 0.0 |  |
| 2019 | 990_pdf | input_990_ty2018 | nan | nan | nan | 1256102.0 | nan |  |
| 2019 | audit | input_fy19_audit | 2584467.0 | 2501810.0 | 3358790.0 | 1256102.0 | 0.0393 | DIFF>1% |
| 2020 | 990 | api_propublica | 3896046.0 | 3215728.0 | 4039108.0 | nan | 0.0 |  |
| 2020 | 990 | bulk_gt_datalake | 3896046.0 | 3215728.0 | 4039108.0 | 2166119.0 | 0.0 |  |
| 2020 | 990 | bulk_irs_soi_extract | 3896046.0 | 3215728.0 | 4039108.0 | nan | 0.0 |  |
| 2020 | 990 | bulk_nccs_efile | 3896046.0 | nan | nan | 2166119.0 | 0.0 |  |
| 2020 | 990_pdf | input_990_ty2019 | 3896046.0 | 3215728.0 | 4039108.0 | 2166119.0 | 0.0 |  |
| 2020 | audit | input_fy20_audit | 3908836.0 | 3228518.0 | 4039108.0 | 2166119.0 | 0.0033 |  |
| 2021 | 990 | api_propublica | 3851984.0 | 3334967.0 | 4555754.0 | nan | 0.0 |  |
| 2021 | 990 | bulk_gt_datalake | 3851984.0 | 3334967.0 | 4555754.0 | 503222.0 | 0.0 |  |
| 2021 | 990 | bulk_irs_soi_extract | 3851984.0 | 3334967.0 | 4555754.0 | nan | 0.0 |  |
| 2021 | 990 | bulk_nccs_efile | 3851984.0 | nan | nan | 503222.0 | 0.0 |  |
| 2021 | audit | input_fy21_audit | 3928601.0 | 3411954.0 | 4555754.0 | 1981161.0 | 0.0199 | DIFF>1% |
| 2022 | 990 | api_propublica | 8867250.0 | 4550205.0 | 8872799.0 | nan | 0.0 |  |
| 2022 | 990 | bulk_gt_datalake | 8867250.0 | 4550205.0 | 8872799.0 | 5685504.0 | 0.0 |  |
| 2022 | 990 | bulk_irs_soi_extract | 8867250.0 | 4550205.0 | 8872799.0 | nan | 0.0 |  |
| 2022 | audit | web_calvary_fy22_audit | 9264137.0 | 4947092.0 | 8872799.0 | 5685504.0 | 0.0448 | DIFF>1% |
| 2023 | 990 | api_propublica | 4456814.0 | 5130964.0 | 8198649.0 | nan | 0.0 |  |
| 2023 | 990 | bulk_gt_datalake | 4456814.0 | 5130964.0 | 8198649.0 | 2460897.0 | 0.0 |  |
| 2023 | 990 | bulk_irs_soi_extract | 4456814.0 | 5130964.0 | 8198649.0 | nan | 0.0 |  |
| 2023 | audit | input_fy23_audit | 4807645.0 | 5481795.0 | 8198649.0 | 2460897.0 | 0.0787 | DIFF>1% |
| 2024 | 990 | bulk_gt_datalake | 5817167.0 | 5310627.0 | 8705189.0 | 2621203.0 | 0.0 |  |
| 2025 | 990 | bulk_gt_datalake | 4967995.0 | 5575321.0 | 8098765.0 | 2892598.0 | 0.0 |  |
| 2025 | 990_pdf | input_propublica_990_ty2024 | 4967995.0 | 5575321.0 | 8098765.0 | 2892598.0 | 0.0 |  |


## 5. CRM funders vs 990-PF grants to Calvary (assumption A2: cash unless contradicted)

Counts: {'not_exempt_filer': 92, 'no_filing_rows': 29, 'confirmed_in_window': 25, 'attachment_only_list': 7, 'confirmed_earlier_only': 7}. Full table: `clean/supp_crm_cash_verification.csv`. confirmed_in_window = the funder's own 990-PF/Schedule I lists grants to Calvary in TY2023+ (cash). Amounts differ from CRM totals because TY2025 returns are mostly unfiled and the CRM window is Oct 2023-Oct 2026.

| funder_name_raw | funder_ein | org_class | crm_total | filing_grants_ty2022plus | filing_grant_years | ratio_filing_to_crm | cash_verified | web_inkind_classification |
|---|---|---|---|---|---|---|---|---|
| Morris & Gwendolyn Cafritz Foundation | 526036989 | private_foundation | 1090000.0 | 360000.0 | 2020,2021,2022,2023,2024 | 0.33 | confirmed_in_window | nan |
| Health Equity Fund | 237343119 | public_charity | 801000.0 | 966500.0 | 2020,2021,2022,2023,2024 | 1.21 | confirmed_in_window | cash |
| MGAC |  |  | 712730.0 | nan | nan | nan | not_exempt_filer | unclear |
| Philip L. Graham Fund | 526051781 | private_foundation | 633500.0 | nan | nan | nan | attachment_only_list | nan |
| William S. Abell Foundation | 521435573 | private_foundation | 532500.0 | 25000.0 | 2021,2023 | 0.05 | confirmed_in_window | nan |
| Clark-Winchcole Foundation | 526058340 | private_foundation | 480000.0 | nan | nan | nan | attachment_only_list | nan |
| The Leafglen Foundation | 352599437 | private_foundation | 467000.0 | 315000.0 | 2020,2021,2022,2023,2024,2025 | 0.67 | confirmed_in_window | nan |
| Capital One | 113276603 | private_foundation | 367340.0 | nan | nan | nan | no_filing_rows | unclear |
| Bank of America Charitable Foundation | 200721133 | private_foundation | 327500.0 | 30000.0 | 2020,2021,2022,2023 | 0.09 | confirmed_in_window | nan |
| John E. Fowler Memorial Foundation | 516019469 | private_foundation | 310000.0 | 80000.0 | 2020,2023,2025 | 0.26 | confirmed_in_window | nan |
| World Bank Community Connections Fund | 421559999 | public_charity | 261580.0 | 100000.0 | 2022 | 0.38 | confirmed_earlier_only | cash |
| Rapoport Family Foundation | 133369901 | private_foundation | 261250.0 | 40000.0 | 2020,2022,2023 | 0.15 | confirmed_in_window | nan |
| TD Bank Community Relations/Charitable Foundation | 141864317 | private_foundation | 254750.0 | nan | nan | nan | no_filing_rows | nan |
| Frontier Co-op Giving Fund |  |  | 250000.0 | nan | nan | nan | not_exempt_filer | nan |
| Principal Foundation | 421312301 | private_foundation | 200000.0 | nan | nan | nan | no_filing_rows | nan |
| International Monetary Fund (IMF) |  |  | 156484.0 | nan | nan | nan | not_exempt_filer | nan |
| Reservoir Communications Group LLC |  |  | 155000.0 | nan | nan | nan | not_exempt_filer | nan |
| Corina Higginson Trust | 526055743 | private_foundation | 149015.0 | 46500.0 | 2020,2021,2022,2023,2024,2025 | 0.31 | confirmed_in_window | nan |
| Northrop Grumman Corporation | 956095343 | private_foundation | 146040.0 | nan | nan | nan | no_filing_rows | nan |
| Max and Victoria Dreyfus Foundation | 131687573 | private_foundation | 145000.0 | 5000.0 | 2020,2022 | 0.03 | confirmed_earlier_only | nan |
| DAVIS Construction | 873514845 | private_foundation | 117405.0 | nan | nan | nan | no_filing_rows | nan |
| Latham & Watkins LLP |  |  | 115000.0 | nan | nan | nan | not_exempt_filer | nan |
| Dimick Foundation | 526038149 | private_foundation | 109500.0 | 10000.0 | 2020,2021,2022,2024 | 0.09 | confirmed_in_window | nan |
| Hearst Foundations | 136161746 | private_foundation | 100000.0 | nan | nan | nan | no_filing_rows | nan |
| Association of American Medical Colleges (AAMC) | 362169124 | public_charity | 99106.0 | 56500.0 | 2020,2021,2022,2023,2024 | 0.57 | confirmed_in_window | nan |
| WHF Foundation | 541871583 | public_charity | 99000.0 | nan | nan | nan | no_filing_rows | nan |
| Nancy Peery Marriott Foundation | 522003744 | private_foundation | 94500.0 | 20000.0 | 2024,2025 | 0.21 | confirmed_in_window | nan |
| Kay Family Foundation | 521045650 | private_foundation | 87000.0 | nan | nan | nan | attachment_only_list | nan |
| Qlarant Foundation | 200065799 | public_charity | 83500.0 | 20000.0 | 2023 | 0.24 | confirmed_in_window | nan |
| UnitedHealth Group Employee Giving Campaign |  |  | 78983.0 | nan | nan | nan | not_exempt_filer | nan |
| Venable Foundation | 521283255 | public_charity | 75000.0 | nan | nan | nan | no_filing_rows | nan |
| Morrison & Foerster Foundation | 943006979 | public_charity | 74000.0 | nan | nan | nan | no_filing_rows | nan |
| Sulica Fund |  |  | 70060.0 | nan | nan | nan | not_exempt_filer | nan |
| Herb Block Foundation | 260008276 | private_foundation | 65000.0 | nan | nan | nan | attachment_only_list | nan |
| Altria Corporate Services |  |  | 61615.0 | nan | nan | nan | not_exempt_filer | nan |
| Courembis Companies |  |  | 57825.0 | nan | nan | nan | not_exempt_filer | nan |
| CareFirst Committment |  |  | 57500.0 | nan | nan | nan | not_exempt_filer | nan |
| Bill & Melinda Gates Foundation | 562618866 | private_foundation | 55023.0 | nan | nan | nan | no_filing_rows | nan |
| The Hyde Foundation |  |  | 50000.0 | nan | nan | nan | not_exempt_filer | nan |
| Salt River Project (SRP) |  |  | 47500.0 | nan | nan | nan | not_exempt_filer | nan |


## 6. Grant parser check: Calvary's donor-list foundations in parsed 990-PF / Schedule I data

| foundation | funder_ein | parsed_grant_rows_all_recipients | rows_to_calvary | calvary_amount | tax_years_to_calvary |
|---|---|---|---|---|---|
| Meyer | 530241716 | 1254 | 0 | 0 |  |
| Philip L. Graham | 526051781 | 10 | 0 | 0 |  |
| Abell | 521435573 | 449 | 2 | 295000 | 2021,2023 |
| Venable (Venable Baetjer & Howard Foundation, Schedule I) | 521283255 | 979 | 0 | 0 |  |
| Rapoport | 133369901 | 29 | 3 | 50000 | 2020,2022,2023 |
| Baxt | 522006746 | 149 | 4 | 10000 | 2020,2021,2023,2024 |
| Cafritz | 526036989 | 2361 | 5 | 450000 | 2020,2021,2022,2023,2024 |
| Clark-Winchcole | 526058340 | 5 | 0 | 0 |  |
| Leafglen | 352599437 | 40 | 6 | 390000 | 2020,2021,2022,2023,2024,2025 |
| Fowler | 516019469 | 456 | 3 | 120000 | 2020,2023,2025 |


A foundation with parsed rows but none to Calvary in TY2020+ is a funding-pattern observation, not a parser failure (e.g., listed on the 'over the years' support page only).

## 7. Unmatched entity names and their share of grant dollars

Grant dollars exclude cumulative rows. 'See attached' placeholder rows (667 rows, $3,497,262,549) and grants to individuals (37,472 rows; names redacted) are reported separately, since they cannot have a recipient EIN.

- Named organizational recipients in DC/MD/VA (the analysis focus): 378,839 rows, $39,615,220,917; without recipient EIN 76,801 rows, $3,972,062,391 (10.0% of dollars).
- All named organizational recipients (incl. national/global grants of non-DMV known Calvary funders such as the Gates Foundation): 890,128 rows, $97,826,055,788; without recipient EIN 217,421 rows, $27,063,273,605 (27.7% of dollars).
- All non-cumulative rows: 928,204 rows, $101,615,645,610; without recipient EIN 255,496 rows, $30,851,614,671 (30.4% of dollars).
- Funders without an EIN (corporations, government, unnamed): 1,190 rows across 877 funder ids.


Top unmatched DC/MD/VA recipients by dollars (typically government units, public schools and universities' sub-units, churches, or name variants):

| recipient_name_raw | recipient_state | amt |
|---|---|---|
| INTERNATIONAL BANK FOR RECONSTRUCTION AND DEVELOPMENT | DC | 847756890.0 |
| COMMONWEALTH FOUNDATION FOR CANCER RESEARCH | VA | 258044310.0 |
| VCU School of Medicine | VA | 158025000.0 |
| WASHINGTON INSTITUTE FOR EDUCATION AND RESEARCH | DC | 90700000.0 |
| UNIVERSITY OF MARYLAND BALTIMORE | MD | 84001192.0 |
| [individual - name redacted] | MD | 62892741.0 |
| University of Virginia School of Data Science | VA | 40000000.0 |
| FRALIN BIOMEDICAL RESEARCH INSTITUTE | VA | 37525000.0 |
| Institute for Advanced Learning and Research | VA | 35510016.0 |
| INTER-AMERICAN DEVELOPMENT BANK | DC | 29083543.0 |
| NATIONAL INSTITUTES OF HEALTH | MD | 28755849.0 |
| NATIONAL STUDENT CLEARINGHOUSE RESEARCH CENTER | VA | 27658165.0 |
| EDUCATION STRATEGY GROUP LLC | MD | 27635952.0 |
| INTERNATIONAL DEVELOPMENT ASSOCIATION | DC | 23500000.0 |
| [individual - name redacted] | VA | 21198756.0 |
| FRAYM INC | VA | 20044062.0 |
| NOVAVAX INC | MD | 20000000.0 |
| INNOVATIONS FOR POVERTY ACTION | DC | 19610894.0 |
| CHARLOTTESVILLE COMMUNITY DEVELOPMENT CORP | VA | 19008215.0 |
| INTERNATIONAL FINANCE CORPORATION | DC | 17766395.0 |
| International Union for Conservation of Nature and | DC | 16904457.0 |
| UVA SCHOOL OF DATA SCIENCE | VA | 16500000.0 |
| THE NATURE CONSERVANCY (TNC) | VA | 14860020.0 |
| COLERIDGE INITIATIVE INCORPORATED | MD | 14692125.0 |
| OLD DOMINION MUSEUM FOUNDATION | VA | 14664000.0 |


Recipient match methods:

| match_method | count |
|---|---|
| exact_ein | 259492 |
| unmatched | 248149 |
| given | 200384 |
| exact_name_city | 155406 |
| exact_name_state | 31828 |
| fuzzy_name_city | 25134 |
| redacted_individual | 7349 |
| exact_name_national | 906 |
| manual | 10 |


## 8. Person matching

- People 48,563; linked across 2+ organizations 2,036 (by confidence {'medium': 1439, 'high': 597}); low-confidence candidate pairs for manual review: 1,270 (`clean/candidate_interlocks.csv`).

## 9. Known coverage gaps

- 990-N / non-filers: 660 sector orgs have no return since TY2020 in the BMF or e-file index (990-N postcard filers or inactive): no financials or governance data.
- XML fetch: 0 of 31,483 targeted returns not retrieved; by tax year: {'2014': 2, '2015': 2, '2016': 2, '2017': 2, '2018': 2, '2019': 2, '2020': 4973, '2021': 5450, '2022': 5775, '2023': 6118, '2024': 6219, '2025': 2936}.
- Paper filers: returns filed on paper have no XML; financials rely on SOI/ProPublica where present.
- Recent years: TY2024 returns are partially released (IRS 2025-2026 batches); TY2025 returns are mostly not yet filed (fiscal years ending mid-2026 have extensions into 2027).
- Calvary audits for FY22, FY24, FY25 were not provided; FY22 comes from the FY23 audit's comparative column.
- FAC audit-year 2023 record for Calvary repeats FY22 SEFA amounts; FY23 audit PDF shows $937,999 (both kept, flagged).
- USAspending shows little of the DC pass-through money (SLFRF, CoC via TCP, EFSP); FAC and DC sources cover it.
- DHS provider-level grant lists for 2025-2026 were not posted (Excel attachments missing); TCP Schedule I is the fallback.
- Corporate giving (non-foundation) appears only where Calvary or a peer lists it (no public filing).
- Individual donors are deliberately excluded except as counts per gift band (Calvary donor privacy policy).

## 10. Portability

- Files with absolute paths, usernames or key-shaped strings: none
- Non-UTF-8 files: none

