# Clean table specs (the contract between pull scripts and the clean/ model)

Phase 4 pull scripts write **staging** files to `interim/stage_{table}__{area}.csv`, using the columns below. A staging file may omit columns it can't fill, and may add extra columns prefixed `x_`.

Phase 5 merge scripts (`6x_`) union the staging files, assign ids, dedupe and write `clean/{table}.csv`.

Every fact and staging row carries `source_id`, `retrieved_date`, `confidence` (high/medium/low) and `basis` (documented/derived/inferred). Amounts are integer nominal USD. A `*_real_2024` column, CPI-U US annual average with base 2024, is added at merge, not in staging. Dates are ISO 8601. EINs are 9-digit strings.

Fiscal fields:
- `tax_year`: IRS tax year, the year the FY begins.
- `fiscal_year`: the year the FY ends.
- `fye_month`: the FY's end month, 1–12.
- `tax_period_end`: the period-end date, YYYY-MM-DD with the last day of the month.

Government fiscal years are stated explicitly with `fiscal_year_basis`: `federal_fy` (Oct–Sep), `dc_fy` (Oct–Sep), `org_fy` or `calendar`.

## Dimensions

**dim_org**: one row per nonprofit EIN.
ein, org_name, org_name_bmf, dba_name, street, city, state, zip5, county_fips, ward, tract_geoid, lat, lon, geo_method, ntee_cd, ntee3, ntee_label, subsection, foundation_code, org_class (public_charity / private_foundation / other_exempt), ruling_year, website, fye_month, latest_tax_year, latest_return_type, bmf_revenue_amt, is_calvary, source_id, retrieved_date

**dim_funder**: one row per funder, exempt or not.
funder_id (EIN when known, else `F` + 10-char hash of the normalized name), ein, funder_name, funder_type, state, county_fips, ward, issue_focus_tags, universes, n_grants, source_id, retrieved_date.
- funder_type: private_foundation / corporate_foundation / community_foundation / daf_sponsor / federated_giving / public_charity_grantmaker / corporate / government_agency / faith / civic_association / individual_aggregate / other

**dim_period**: one row per calendar year, 2000–2027.
year, cpi_u_us, cpi_u_dc_metro, deflator_to_2024_us, federal_fy_label, dc_fy_label, calvary_fiscal_year_label, notes, source_id

**dim_geo**: one row per geography.
geo_id, geo_level (nation / state / msa / county / ward / tract), state_fips, county_fips, tract_geoid, ward, name, acs_vintage, total_pop, poverty_rate, female_poverty_rate, median_hh_income, rent_burden_30plus_share, rent_burden_50plus_share, unemployment_rate, pct_black_nh, pct_hispanic, pct_white_nh, female_hh_no_spouse_share, veteran_share, disability_share, source_id, retrieved_date. MOEs are optional, as extra `*_moe` columns.

**dim_program_area**: tag vocabulary, from `config/program_areas.yaml`.
program_area, label, description, keywords, ntee3_codes, assistance_listings

**dim_universe_membership**: built by `scripts/20_build_universes.py`. See that script.

**dim_person**: canonical people from governance filings.
person_id, name_display, name_norm, first_name, middle_initial, last_name, suffix, n_orgs, n_filings, match_notes

## Facts

**fact_org_financials**: one row per org × fiscal year × source.
ein, tax_year, fiscal_year, fye_month, tax_period_end, return_type, object_id, is_amended, source_id, retrieved_date, preferred (1 = the preferred row for that org-year), conflict_flag, confidence, basis.

Then the money fields:
- **revenue:** total_revenue, contributions_total, federated_campaigns, membership_dues, fundraising_event_contributions, related_org_contributions, government_grants, other_contributions, noncash_contributions, program_service_revenue, investment_income, special_events_net, other_revenue
- **expenses:** total_expenses, program_expenses, management_expenses, fundraising_expenses, grants_paid, compensation_total
- **balance sheet:** total_assets_eoy, total_liabilities_eoy, net_assets_eoy, cash_savings_eoy
- **990-PF only:** pf_fmv_assets_eoy, pf_total_grants_paid, pf_qualifying_distributions, pf_contributions_received
- **derived** (basis=derived; computed only on preferred rows): gov_share_of_revenue, months_of_cash, revenue_growth_yoy, program_expense_ratio

**fact_grants**: one row per grant or gift record.
- **identity:** grant_id
- **funder:** funder_id, funder_ein, funder_name_raw
- **recipient:** recipient_ein, recipient_name_raw, recipient_name_norm, recipient_city, recipient_state, recipient_zip5
- **timing:** tax_year, fiscal_year, grant_date, year_basis (funder_tax_year / report_year / gift_date / award_year)
- **amount:** amount, amount_band_min, amount_band_max, amount_kind (cash / noncash / mixed / pledge / unknown), cumulative_flag (1 when the amount spans several years, e.g. CRM totals)
- **description:** purpose_text, program_area_tags
- **source:** source_type (pf_grants_paid / pf_grants_approved_future / schedule_i / crm / annual_report / support_page / web / gov_list), object_id, source_id
- **resolution and quality:** match_method, match_score, retrieved_date, confidence, basis

**fact_gov_awards**: one row per federal or DC award, subaward, expenditure line or budget-allocated grant.
- **identity:** award_row_id
- **recipient:** recipient_ein, recipient_uei, recipient_name_raw
- **agency and program:** awarding_agency, funding_agency, program_name, assistance_listing, award_id, award_type (grant / cooperative_agreement / contract / loan / direct_payment / other)
- **flow:** flow_type (prime / subaward / pass_through_expenditure / dc_local_grant / dc_contract), pass_through_entity, pass_through_ein
- **period:** period_start, period_end, fiscal_year, fiscal_year_basis
- **amount:** amount, amount_type (obligation / outlay / expenditure / award_amount / budget)
- **source and quality:** source_type (usaspending / fac_sefa / audit_sefa / treasury_slfrf / dc_ovsjg / dc_oversight / dc_pass / hud_coc / other), source_id, source_page, conflict_flag, retrieved_date, confidence, basis

**fact_opportunities**: one row per open or forecast opportunity.
- **identity:** opportunity_id, opportunity_number, title
- **funder:** funder_name, agency_code
- **status and listings:** status (posted / forecasted), assistance_listings
- **eligibility:** eligibility_codes, eligibility_text
- **funding:** award_floor, award_ceiling, estimated_total_funding, expected_awards
- **dates:** post_date, close_date, forecast_award_date
- **classification:** funding_category, program_area_tags, keyword_hits
- **source:** url, source_id, retrieved_date

**fact_policy_events**: one row per dated budget or policy change.
- **identity:** event_id, event_date, event_type (budget_proposed / budget_enacted / budget_revised / policy_change / program_launch / program_end / federal_award / federal_rule / other)
- **where:** jurisdiction (DC / federal / regional), agency, program_code
- **what:** funding_stream, description, amount, prior_amount, amount_change, fiscal_year, program_area_tags
- **source and quality:** source_id, source_page, confidence, basis

**fact_roles**: one row per person × org × filing year.
- **identity:** role_id, person_id, ein, org_name
- **filing:** tax_year, fiscal_year
- **role:** title, role_type (board / officer / key_employee / highest_compensated / foundation_trustee / foundation_officer / listed_in_report)
- **role flags:** is_officer, is_director_trustee, is_key_employee, is_highest_comp, is_former
- **hours and pay:** avg_hours_per_week, reportable_comp_org (as filed)
- **source:** source_id, object_id, retrieved_date

Never store addresses or contact details.

**fact_org_relationships**: one row per relationship between two organizations.
- **identity:** rel_id
- **parties:** org_a_ein, org_a_name, org_b_ein, org_b_name
- **relationship:** rel_type (grant / schedule_r_related / shared_board_member / fiscal_sponsorship / daf_sponsor_grant / pass_through_funding), direction (a_to_b / undirected)
- **details:** tax_year, amount, evidence, person_id
- **source and quality:** source_id, confidence, basis

**entity_aliases**: one row per observed name variant.
- **variant:** alias_name_raw, alias_name_norm, alias_city, alias_state
- **canonical entity:** entity_kind (org / funder), canonical_id, canonical_name
- **match:** match_method (exact_ein / exact_name_city / exact_name_state / fuzzy_name_city / manual / unmatched), match_score
- **provenance:** n_occurrences, source_ids
