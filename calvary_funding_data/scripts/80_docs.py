"""Phase 6: documentation outputs generated from the clean tables.

  clean/data_dictionary.csv    table, column, type, definition, allowed_values, sources (every clean table + column)
  reports/data_inventory.md    plain-language inventory: entities per universe, years, rows, funders, dimensions
  source registry check        every source_id used in clean/ must exist in sources/source_registry.csv

Usage: python scripts/80_docs.py
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import CLEAN, REPORTS, SOURCES, log, today
from lib.specs import SPECS

NOTES_COL = ("notes", "str", "Source-specific extras as key=value pairs separated by '; ' (e.g. stage_file, "
             "match details, document notes)", "")
EXTRA = {
    "dim_universe_membership": [
        ("universe", "str", "Comparison universe (look up membership here; config/universes.yaml holds the rules)",
         "calvary|core_peers|named_comparators|dc_sector|dmv_sector|national_women|size_matched|"
         "dmv_funders|daf_sponsors|calvary_known_funders"),
        ("ein", "str", "EIN", ""), ("rule_id", "str", "Inclusion rule (config/universes.yaml)", ""),
        ("criteria", "str", "Rule description", ""), ("org_name_bmf", "str", "BMF legal name", ""),
        ("city", "str", "BMF city", ""), ("state", "str", "BMF state", ""), ("zip5", "str", "BMF ZIP", ""),
        ("county_fips", "str", "County from ZIP (Census ZCTA-county 2020, primary by land area) or city fallback", ""),
        ("geo_method", "str", "How county was assigned", "state_dc|zcta_primary_county|city_modal_county|unresolved|not_in_bmf"),
        ("in_dc_msa", "bool", "County is in the DC MSA (CBSA 47900) within DC/MD/VA", "True|False"),
        ("ntee_cd", "str", "BMF NTEE code", ""), ("ntee3", "str", "NTEE first 3 characters", ""),
        ("subsection", "str", "501(c) subsection", ""), ("foundation_code", "str", "BMF FOUNDATION code", ""),
        ("ruling_yyyymm", "str", "IRS ruling date YYYYMM", ""),
        ("bmf_revenue_amt", "int", "BMF revenue (latest return)", ""), ("bmf_asset_amt", "int", "BMF assets", ""),
        ("bmf_tax_period", "int", "BMF latest tax period YYYYMM", ""),
        ("latest_efile_tax_period", "int", "Latest e-filed return period in IRS index 2021-2026 (YYYYMM)", ""),
        ("latest_efile_return_type", "str", "Return type of that return", "990|990EZ|990PF"),
        ("recent_filing", "bool", "Return for a period ending 2021-01 or later exists", "True|False"),
        ("source_id", "str", "Sources", ""), ("retrieved_date", "date", "Build date", ""),
        ("basis", "str", "Basis", "derived"), ("confidence", "str", "Confidence in membership", "high|medium|low"),
    ],
    "ref_ntee_codes": [("ntee3", "str", "NTEE 3-character code", ""), ("ntee_label", "str", "IRS label", ""),
                       ("major_group", "str", "NTEE major group letter", ""), ("source_id", "str", "Source", "")],
    "candidate_interlocks": [
        ("name_norm", "str", "Normalized name shared by both role records", ""),
        ("ein_a", "str", "Organization A", ""), ("ein_b", "str", "Organization B", ""),
        ("signals", "str", "Corroborating signals found", "same_metro;overlap_years;middle_initial;suffix"),
        ("common_name", "int", "1 if first+last appears at >5 organizations", "0|1"),
        ("match_confidence", "str", "Always low here (not linked); review manually", "low"),
        ("person_id_a", "str", "dim_person id of A", ""), ("person_id_b", "str", "dim_person id of B", "")],
    "supp_crm_cash_verification": [
        ("funder_name_raw", "str", "Funder as named in Calvary's CRM export", ""), ("funder_ein", "str", "Resolved EIN", ""),
        ("org_class", "str", "dim_org.org_class of the funder", ""),
        ("crm_total", "float", "CRM GIFT_TOTAL (assumed window 2023-10..2026-10; assumption A1)", ""),
        ("filing_grants_ty2022plus", "float", "Grants to Calvary in the funder's 990-PF/Schedule I, TY2022+", ""),
        ("filing_grant_years", "str", "Tax years with grants to Calvary in filings", ""),
        ("ratio_filing_to_crm", "float", "filing_grants_ty2022plus / crm_total", ""),
        ("cash_verified", "str", "confirmed_in_window = funder's filings list grants to Calvary in TY2023+; "
         "confirmed_earlier_only = TY2020-2022 only; attachment_only_list = funder's recent returns itemize grants only "
         "as 'see attached'; no_filing_rows = itemized returns with no Calvary grant; not_exempt_filer = corporation, "
         "government or unmatched (no public filing to check)",
         "confirmed_in_window|confirmed_earlier_only|attachment_only_list|no_filing_rows|not_exempt_filer"),
        ("web_inkind_classification", "str", "Web evidence classification (interim/web_inkind_evidence.csv)", "cash|in_kind|unclear")],
    "supp_calvary_program_metrics": [
        ("source_id", "str", "Source document", ""), ("document", "str", "File name", ""),
        ("report_year", "int", "Report year as labeled", ""), ("metric", "str", "Metric", ""),
        ("value", "str", "Value as printed", ""), ("unit", "str", "Unit", ""), ("notes", "str", "Context", ""),
        ("retrieved_date", "date", "Build date", "")],
    "supp_calvary_strategic_targets": [
        ("source_id", "str", "Source document", ""), ("document", "str", "File name", ""),
        ("plan_period", "str", "Strategic plan period", ""), ("goal_area", "str", "Goal area", ""),
        ("target_text", "str", "Target as written", ""), ("target_value", "str", "Numeric target", ""),
        ("target_unit", "str", "Unit", ""), ("target_year", "str", "Target year", ""),
        ("reported_result_text", "str", "Reported result", ""), ("reported_value", "str", "Numeric result", ""),
        ("notes", "str", "Notes", ""), ("retrieved_date", "date", "Build date", "")],
    "supp_calvary_individual_donor_bands": [
        ("source_id", "str", "Source", ""), ("document", "str", "File", ""), ("report_year", "int", "Report year", ""),
        ("gift_band_raw", "str", "Gift band as printed", ""), ("band_min", "int", "Band minimum", ""),
        ("band_max", "int", "Band maximum", ""), ("individual_count", "int", "Individual/household listings (names not stored)", ""),
        ("notes", "str", "Notes", ""), ("retrieved_date", "date", "Build date", "")],
}
EXTRA.update({
    "supp_homeless_counts": [
        ("coc_code", "str", "HUD Continuum of Care code (DC-500, MD-600, ...)", ""),
        ("jurisdiction", "str", "Jurisdiction name", ""), ("year", "int", "Count year (PIT: January count)", ""),
        ("measure", "str", "Measure (e.g. PIT total/sheltered/unsheltered, HIC beds by type)", ""),
        ("population", "str", "Population or household type the measure covers", ""),
        ("value", "float", "Count", "")],
    "supp_hic_projects": [
        ("year", "int", "HIC year", ""), ("coc_code", "str", "CoC code", ""),
        ("organization_name", "str", "Project organization as listed", ""),
        ("recipient_ein", "str", "Matched EIN (blank if unmatched)", ""), ("project_name", "str", "Project", ""),
        ("project_type", "str", "HUD project type (ES/TH/PSH/RRH/OPH/SH)", ""), ("total_beds", "int", "Total beds", ""),
        ("units", "int", "Units", ""), ("target_population", "str", "Target population", "")],
    "supp_dc_budget_lines": [
        ("fiscal_year", "int", "DC fiscal year (Oct-Sep)", ""),
        ("budget_stage", "str", "Stage", "approved|proposed|revised|actual"), ("agency_code", "str", "DC agency code", ""),
        ("agency", "str", "Agency", ""), ("program_code", "str", "Program code", ""), ("activity_code", "str", "Activity code", ""),
        ("line_item", "str", "Line item label", ""), ("fund_type", "str", "Fund", "local|federal|special|total|..."),
        ("amount", "int", "Amount (USD)", ""), ("document", "str", "Budget document", ""), ("page", "str", "Page", "")],
})
for _t in ("supp_homeless_counts", "supp_hic_projects", "supp_dc_budget_lines"):
    EXTRA[_t] += [("source_id", "str", "Source", ""), ("retrieved_date", "date", "Retrieved", ""),
                  ("confidence", "str", "Confidence", "high|medium|low"),
                  ("basis", "str", "Basis", "documented|derived|inferred")]
SUPP_GENERIC = "See the producing script in scripts/ (named in sources/source_registry.csv notes or the build log)"


def main():
    rows = []
    for p in sorted(CLEAN.glob("*.csv")):
        t = p.stem
        if t == "data_dictionary":
            continue
        try:
            hdr = list(pd.read_csv(p, nrows=0).columns)
            srcs = pd.read_csv(p, usecols=["source_id"], dtype=str, keep_default_na=False).source_id \
                if "source_id" in hdr else pd.Series(dtype=str)
        except pd.errors.EmptyDataError:
            hdr, srcs = [], pd.Series(dtype=str)
        src_txt = ";".join(sorted({s for v in srcs.unique() for s in str(v).split(";") if s})[:12])
        spec = {c[0]: c for c in SPECS.get(t, []) + EXTRA.get(t, []) + [NOTES_COL]}
        generic = {"retrieved_date": ("date", "Date the underlying source was retrieved (ISO 8601)", ""),
                   "source_id": ("str", "Source; key into sources/source_registry.csv", ""),
                   "confidence": ("str", "Confidence in the value", "high|medium|low"),
                   "basis": ("str", "documented|derived|inferred (see README)", "documented|derived|inferred")}
        for c in hdr:
            if c in spec:
                col, typ, desc, allowed = spec[c]
            elif c in generic:
                col, (typ, desc, allowed) = c, generic[c]
            elif c.endswith("_moe"):
                col, typ, desc, allowed = c, "float", f"ACS margin of error (90%) for {c[:-4].removeprefix('x_')}", ""
            elif c.startswith("x_"):
                col, typ, desc, allowed = c, "str", (f"Supplementary field '{c[2:]}' from the staging script "
                                                     "(see its docstring); not part of the core spec"), ""
            else:
                col, typ, desc, allowed = c, "str", SUPP_GENERIC, ""
            rows.append({"table": t, "column": col, "type": typ, "definition": desc, "allowed_values": allowed,
                         "sources": src_txt})
    dd = pd.DataFrame(rows)
    dd.to_csv(CLEAN / "data_dictionary.csv", index=False)
    undocumented = dd[dd.definition == SUPP_GENERIC][["table", "column"]]

    # source registry check
    reg = set(pd.read_csv(SOURCES / "source_registry.csv", dtype=str).source_id)
    used = set()
    for p in CLEAN.glob("*.csv"):
        try:
            if "source_id" in pd.read_csv(p, nrows=0).columns:
                used |= {s for v in pd.read_csv(p, usecols=["source_id"], dtype=str, keep_default_na=False).source_id
                         for s in str(v).split(";") if s}
        except pd.errors.EmptyDataError:
            pass
    missing_src = sorted(used - reg)

    # inventory
    def rd(n):
        p = CLEAN / f"{n}.csv"
        try:
            return pd.read_csv(p, dtype=str, keep_default_na=False, low_memory=False) if p.exists() else pd.DataFrame()
        except pd.errors.EmptyDataError:
            return pd.DataFrame()
    uni, fin, gr, ga = rd("dim_universe_membership"), rd("fact_org_financials"), rd("fact_grants"), rd("fact_gov_awards")
    opp, pol, roles, rel = rd("fact_opportunities"), rd("fact_policy_events"), rd("fact_roles"), rd("fact_org_relationships")
    fun, per, org = rd("dim_funder"), rd("dim_person"), rd("dim_org")
    L = ["# Data inventory", "", f"Generated {today()} by `scripts/80_docs.py`. Plain-language summary of what is in `clean/`.", ""]
    L += ["## Organizations and universes", ""]
    if len(uni):
        u = uni.groupby("universe").ein.nunique().sort_values(ascending=False)
        L += [f"- {len(org):,} organizations in `dim_org` (every EIN in a universe or referenced by a fact table)."]
        L += [f"- `{k}`: {v:,} organizations" for k, v in u.items()]
    L += ["", "## Financial time series (`fact_org_financials`)", ""]
    if len(fin):
        pref = fin[fin.preferred == "1"]
        fy = pd.to_numeric(pref.fiscal_year, errors="coerce")
        L += [f"- {len(fin):,} rows ({len(pref):,} preferred org-years) for {fin.ein.nunique():,} organizations; "
              f"fiscal years {int(fy.min())}–{int(fy.max())}.",
              f"- Rows by source: {fin.source_id.str.split(';').str[0].value_counts().to_dict()}."]
    L += ["", "## Grants (`fact_grants`)", ""]
    if len(gr):
        amt = pd.to_numeric(gr.amount, errors="coerce")
        ty = pd.to_numeric(gr.tax_year, errors="coerce")
        L += [f"- {len(gr):,} grant rows, ${amt[gr.cumulative_flag != '1'].sum():,.0f} in annual (non-cumulative) amounts.",
              f"- By source type: {gr.source_type.value_counts().to_dict()}.",
              f"- Funder tax years: {int(ty.min()) if ty.notna().any() else '-'}–{int(ty.max()) if ty.notna().any() else '-'}.",
              f"- Distinct funders: {gr.funder_id.nunique():,}; distinct recipients with EIN: "
              f"{gr[gr.recipient_ein != ''].recipient_ein.nunique():,}.",
              f"- Grants to Calvary: {(gr.recipient_ein == '521307706').sum():,} rows."]
    L += ["", "## Government funding", ""]
    if len(ga):
        L += [f"- `fact_gov_awards`: {len(ga):,} rows; by source: {ga.source_type.value_counts().to_dict()}; "
              f"by flow: {ga.flow_type.value_counts().to_dict()}."]
    L += [f"- `fact_opportunities`: {len(opp):,} open/forecast federal opportunities.",
          f"- `fact_policy_events`: {len(pol):,} dated DC budget/policy events."]
    L += ["", "## Governance", ""]
    if len(per):
        L += [f"- `dim_person`: {len(per):,} people; `fact_roles`: {len(roles):,} role rows; "
              f"people linked across 2+ organizations: {(pd.to_numeric(per.n_orgs, errors='coerce') > 1).sum():,}."]
    if len(rel):
        L += [f"- `fact_org_relationships`: {len(rel):,} rows by type {rel.rel_type.value_counts().to_dict()}."]
    L += ["", "## Funders (`dim_funder`)", ""]
    if len(fun):
        L += [f"- {len(fun):,} funders by type: {fun.funder_type.value_counts().to_dict()}."]
    L += ["", "## Dimensions for slicing", "",
          "- Organization: NTEE (`ntee3`, `ntee_label`), org class, size (`bmf_revenue_amt`), geography (state, county, "
          "DC ward, tract), universe membership.",
          "- Time: `tax_year` / `fiscal_year` on every fact; `dim_period` maps calendar years to CPI deflators and "
          "federal/DC/Calvary fiscal-year labels.",
          "- Geography: `dim_geo` (nation, state, DC MSA, counties, DC wards, DC tracts) with ACS 2020-2024 context.",
          "- Program area: `program_area_tags` on grants, awards, opportunities and policy events (`dim_program_area`).",
          "- Funder type: `dim_funder.funder_type`.", "",
          "## Supplementary tables", ""]
    for p in sorted(CLEAN.glob("supp_*.csv")):
        try:
            n = sum(1 for _ in open(p, encoding="utf-8")) - 1
        except Exception:  # noqa: BLE001
            n = 0
        L.append(f"- `{p.name}`: {n:,} rows")
    (REPORTS / "data_inventory.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    msg = (f"- data_dictionary rows {len(dd):,}; undocumented columns {len(undocumented)}; "
           f"source_ids missing from registry: {missing_src or 'none'}")
    log("80_docs", msg)
    print(msg)
    if len(undocumented):
        print(undocumented.to_string(index=False))


if __name__ == "__main__":
    main()
