"""Namespace-stripped, schema-version-agnostic parser for e-filed 990 / 990-EZ / 990-PF XML.

One code path for every schema version (validated 2014v6.0-2024v5.5 in scripts/11_eval_xml_tooling.py): element
local names only, relative paths, no version branching.

Every file is read with lxml iterparse:
  - repeating grant rows (Schedule I RecipientTable, 990-PF GrantOrContributionPdDurYrGrp /
    GrantOrContriApprvForFutGrp) are converted to dicts as they close, then cleared and removed, so DAF sponsors with
    100k+ Schedule I rows stream in constant memory;
  - children of ReturnData other than the forms used here (other schedules, attached statements) are dropped when
    they close;
  - the remaining tree (header + form + Schedule I/R minus grant rows) is queried with ElementPath.

extract(path, keep_states=None) returns a dict of sections; scripts/50_parse_xml.py turns it into staging rows.
"""
from __future__ import annotations

import calendar
import re
import unicodedata
from collections import Counter
from pathlib import Path

from lxml import etree

KEEP_FORMS = {"IRS990", "IRS990EZ", "IRS990PF", "IRS990ScheduleI", "IRS990ScheduleR"}
STREAM = {
    ("IRS990ScheduleI", "RecipientTable"): "schedule_i",
    ("SupplementaryInformationGrp", "GrantOrContributionPdDurYrGrp"): "pf_grants_paid",
    ("SupplementaryInformationGrp", "GrantOrContriApprvForFutGrp"): "pf_grants_approved_future",
}
TRUE = {"x", "1", "true"}

OFFICER_RE = re.compile(r"(?i)\b(president|pres|vice|vp|ceo|cfo|coo|cio|chief|treasurer|treas|secretary|secy|sec|"
                        r"chair|chairman|chairwoman|chairperson|chr|executive director|exec dir|exec\. dir|"
                        r"officer|controller|comptroller|executive|founder)\b")
DIRECTOR_RE = re.compile(r"(?i)\b(director|dir|trustee|trustees|tr|ttee|board|member|governor|manager|"
                         r"co-trustee|cotrustee)\b")
STAFF_DIRECTOR_RE = re.compile(r"(?i)\b(executive|exec|managing|program|development|finance|operations|"
                               r"grants|communications|associate|assistant)\.?\s+dir(ector)?\b")
# names in the 990-PF RecipientPersonNm field that are clearly organizations
ORG_NAME_RE = re.compile(
    r"(?i)\b(foundation|fdn|fund|funds|church|school|schools|university|univ|college|academy|institute|society|"
    r"association|assn|center|centre|ctr|council|inc|incorporated|corp|corporation|llc|trust|alliance|league|club|"
    r"ministry|ministries|museum|library|hospital|clinic|services|united way|ymca|ywca|charity|charities|"
    r"charitable|coalition|committee|organization|project|program|programs|network|partnership|federation|"
    r"guild|chapter|lodge|temple|synagogue|mosque|parish|diocese|cathedral|congregation|mission|shelter|house|"
    r"home|homes|habitat|red cross|salvation army|scouts|boy scouts|girl scouts|board|department|dept|city of|"
    r"county|state of|town of|village|government|authority|commission|district|pta|pto|athletic|athletics|band|"
    r"boosters|theatre|theater|orchestra|symphony|opera|ballet|festival|arts|kitchen|pantry|food bank|hospice|"
    r"rescue|humane|spca|aid|relief|friends of|initiative|campaign|collaborative|consortium|partners|group|"
    r"company|co|international|national|america|american|alumni|fellowship|conservancy|ministerios|parochial|"
    r"seminary|prep|elementary|high school|middle school|montessori|daycare|preschool|center for|institute for|"
    r"public|radio|television|tv|news|press|journal|research|health|medical|cancer|heart|diabetes|alzheimer|"
    r"memorial|cemetery|veterans|legion|vfw|rotary|kiwanis|lions|elks|knights|order of|sisters|brothers of|"
    r"educat\w*|foundati\w*|booster\w*|parenthood|democracy|peace|outreach|recovery|youth|kids|children|families|"
    r"women|womens|animal\w*|wildlife|conserv\w*|environment\w*|scholarship\w*|ministr\w*|volunteer\w*|fire|"
    r"ems|police|sheriff|squad|ptsa|robotics|literacy|music|dance|choir|chorus|ensemble|players|productions|"
    r"gallery|zoo|aquarium|food|meals|cares|caring|support|solutions|corps|legacy|heritage|history|historical|"
    r"preservation|cases|change|ventures|enterprises|unlimited|usa|us|dc|nova)\b")
# lump-sum rows that point to an attachment instead of naming a grantee ("SEE ATTACHED SCHEDULE", "VARIOUS")
PLACEHOLDER_RE = re.compile(
    r"(?i)(\bsee\s+(the\s+)?(attached|attachment|statement|stmt|schedule|list|listing|exhibit|supplement\w*|"
    r"addendum|pdf)\b|\battached\s+(schedule|list|listing|statement|sheet)\b|\bper\s+attach\w*|"
    r"\b(schedule|statement|list)\s+attached\b|\bvarious\b|^\s*(statement|schedule|attachment)\s*[\w-]{0,4}\s*$)")


def is_placeholder(name: str | None, purpose: str | None) -> bool:
    if name and name.strip():
        return bool(PLACEHOLDER_RE.search(name))
    return bool(PLACEHOLDER_RE.search(purpose or ""))


CHARITY_STATUS_RE = re.compile(r"(?i)(\bpc\b|\bpf\b|\bpof\b|\bso\b|\bgov|public|charit|501|509|170|exempt|"
                               r"\bnc\b|school|church|university|hospital|operating)")


# ---------------------------------------------------------------- small helpers
def local(tag) -> str:
    return tag.rsplit("}", 1)[-1] if isinstance(tag, str) else ""


def txt(node, path: str) -> str | None:
    if node is None:
        return None
    v = node.findtext(path)
    if v is None:
        return None
    v = " ".join(v.split())
    return v or None


def amt(node, path: str) -> int | None:
    v = txt(node, path)
    if v is None:
        return None
    try:
        return int(round(float(v.replace(",", ""))))
    except ValueError:
        return None


def flag(node, path: str) -> int | None:
    v = txt(node, path)
    if v is None:
        return None
    return 1 if v.lower() in TRUE else 0


def biz_name(node) -> str | None:
    """Concatenate BusinessNameLine1Txt + BusinessNameLine2Txt (older tags without Txt also accepted)."""
    if node is None:
        return None
    parts = [txt(node, t) for t in ("BusinessNameLine1Txt", "BusinessNameLine1", "BusinessNameLine2Txt",
                                    "BusinessNameLine2")]
    s = " ".join(p for p in parts if p)
    return s or None


def zip5(z: str | None) -> str | None:
    if not z:
        return None
    d = re.sub(r"\D", "", z)
    return d[:5] if len(d) >= 5 else None


def addr(node, us: str, foreign: str) -> dict:
    """City/state/zip5/country of a US or foreign address child (street is never returned here)."""
    a = node.find(us) if node is not None else None
    if a is not None:
        return {"city": txt(a, "CityNm") or txt(a, "City"), "state": txt(a, "StateAbbreviationCd") or txt(a, "State"),
                "zip5": zip5(txt(a, "ZIPCd") or txt(a, "ZIPCode")), "country": "US"}
    f = node.find(foreign) if node is not None else None
    if f is not None:
        return {"city": txt(f, "CityNm") or txt(f, "City"), "state": None, "zip5": None,
                "country": txt(f, "CountryCd") or txt(f, "Country")}
    return {"city": None, "state": None, "zip5": None, "country": None}


def norm_person(name: str | None) -> str:
    """Person-name key: ascii fold, lowercase, drop punctuation, honorifics and degrees. Keeps initials and jr/sr/ii."""
    if not name:
        return ""
    s = unicodedata.normalize("NFKD", str(name)).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z0-9 ]+", " ", s.replace("'", ""))
    drop = {"mr", "mrs", "ms", "miss", "dr", "rev", "hon", "esq", "phd", "md", "cpa", "jd", "dds", "mba", "rn",
            "the", "honorable", "reverend", "prof"}
    return " ".join(t for t in s.split() if t not in drop)


def last_day(d: str | None) -> str | None:
    if not d or len(d) < 7:
        return None
    y, m = int(d[:4]), int(d[5:7])
    return f"{y:04d}-{m:02d}-{calendar.monthrange(y, m)[1]:02d}"


def schema_version(path: Path) -> str | None:
    with open(path, "rb") as f:
        head = f.read(4096).decode("utf-8", "ignore")
    m = re.search(r'returnVersion="([^"]+)"', head)
    return m.group(1) if m else None


# ---------------------------------------------------------------- streamed grant rows
def _grant_row(el, kind: str) -> dict:
    if kind == "schedule_i":
        name = biz_name(el.find("RecipientBusinessName")) or biz_name(el.find("RecipientNameBusiness"))
        a = addr(el, "USAddress", "ForeignAddress")
        cash, non = amt(el, "CashGrantAmt"), amt(el, "NonCashAssistanceAmt")
        return {"name": name, "person_field": 0, "ein": txt(el, "RecipientEIN"), **a,
                "cash": cash, "noncash": non, "purpose": txt(el, "PurposeOfGrantTxt"),
                "irc_section": txt(el, "IRCSectionDesc"), "valuation": txt(el, "ValuationMethodUsedDesc"),
                "noncash_desc": txt(el, "NonCashAssistanceDesc")}
    person = txt(el, "RecipientPersonNm")
    name = biz_name(el.find("RecipientBusinessName")) or person
    a = addr(el, "RecipientUSAddress", "RecipientForeignAddress")
    return {"name": name, "person_field": 1 if (person and not biz_name(el.find("RecipientBusinessName"))) else 0,
            "ein": None, **a, "cash": amt(el, "Amt"), "noncash": None,
            "purpose": txt(el, "GrantOrContributionPurposeTxt"),
            "relationship": txt(el, "RecipientRelationshipTxt"),
            "foundation_status": txt(el, "RecipientFoundationStatusTxt")}


def recipient_kind(g: dict) -> str:
    """org / org_in_person_field / individual_redacted for 990-PF rows; Schedule I Part II rows are always org."""
    if not g.get("person_field"):
        return "org"
    name = g.get("name") or ""
    if ORG_NAME_RE.search(name) or CHARITY_STATUS_RE.search(g.get("foundation_status") or ""):
        return "org_in_person_field"
    if len(name.split()) == 1:   # single tokens are acronyms / org short names, not personal names
        return "org_in_person_field"
    return "individual_redacted"


# ---------------------------------------------------------------- main entry
def extract(path: Path, keep_states: set[str] | None = None) -> dict:
    """Parse one return. keep_states: if set, Schedule I rows outside these states are tallied, not returned."""
    out = {"grants": [], "grant_stats": Counter(), "filtered_by_state": Counter(), "filtered_amt_by_state": Counter()}
    counters: Counter = Counter()
    root = None
    for _, el in etree.iterparse(str(path), events=("end",), huge_tree=True, remove_comments=True):
        tag = local(el.tag)
        el.tag = tag
        parent = el.getparent()
        if parent is None:
            root = el
            continue
        ptag = local(parent.tag)
        kind = STREAM.get((ptag, tag))
        if kind:
            counters[kind] += 1
            n = counters[kind]
            g = _grant_row(el, kind)
            anc = [local(a.tag) for a in el.iterancestors()][::-1]
            g["xpath"] = "/" + "/".join(anc + [f"{tag}[{n}]"])
            g["seq"] = n
            g["source_type"] = kind
            s = out["grant_stats"]
            s[f"{kind}_n"] += 1
            s[f"{kind}_cash"] += g["cash"] or 0
            s[f"{kind}_noncash"] += g["noncash"] or 0
            if kind == "schedule_i" and keep_states is not None and (g["state"] or "") not in keep_states:
                st = g["state"] or (g["country"] or "??")
                out["filtered_by_state"][st] += 1
                out["filtered_amt_by_state"][st] += (g["cash"] or 0) + (g["noncash"] or 0)
            else:
                out["grants"].append(g)
            el.clear()
            parent.remove(el)
            continue
        if ptag == "ReturnData" and tag not in KEEP_FORMS:
            el.clear()
            parent.remove(el)
    if root is None:
        raise ValueError("empty document")
    out["return_version"] = root.get("returnVersion")
    hdr = root.find("ReturnHeader")
    rd = root.find("ReturnData")
    if hdr is None or rd is None:
        raise ValueError("missing ReturnHeader/ReturnData")
    out["header"] = _header(hdr)
    f990, fez, fpf = rd.find("IRS990"), rd.find("IRS990EZ"), rd.find("IRS990PF")
    form = "990" if f990 is not None else "990EZ" if fez is not None else "990PF" if fpf is not None else None
    if form is None:
        raise ValueError("no IRS990/IRS990EZ/IRS990PF element")
    out["form"] = form
    f = {"990": f990, "990EZ": fez, "990PF": fpf}[form]
    out["is_amended"] = flag(f, "AmendedReturnInd") or flag(hdr, "AmendedReturnInd") or 0
    out["fin"] = {"990": _fin_990, "990EZ": _fin_ez, "990PF": _fin_pf}[form](f)
    out["fin"]["x_initial_return"] = flag(f, "InitialReturnInd")
    out["fin"]["x_final_return"] = flag(f, "FinalReturnInd") or flag(f, "TerminateOperationsInd")
    out["profile"] = {"990": _profile_990, "990EZ": _profile_ez, "990PF": _profile_pf}[form](f)
    out["roles"] = {"990": _roles_990, "990EZ": _roles_ez, "990PF": _roles_pf}[form](f)
    si = rd.find("IRS990ScheduleI")
    out["sched_i_p3"] = _sched_i_p3(si) if si is not None else []
    out["sched_i_meta"] = ({"total_501c3_cnt": amt(si, "Total501c3OrgCnt"), "total_other_cnt": amt(si, "TotalOtherOrgCnt")}
                           if si is not None else {})
    sr = rd.find("IRS990ScheduleR")
    out["related"] = _sched_r(sr) if sr is not None else []
    out["has_sched"] = {"I": si is not None, "R": sr is not None}
    return out


# ---------------------------------------------------------------- header
def _header(h) -> dict:
    filer = h.find("Filer")
    us = filer.find("USAddress") if filer is not None else None
    fa = filer.find("ForeignAddress") if filer is not None else None
    a = us if us is not None else fa
    street = " ".join(x for x in (txt(a, "AddressLine1Txt"), txt(a, "AddressLine2Txt")) if x) if a is not None else None
    return {
        "ein": txt(filer, "EIN"),
        "name": biz_name(filer.find("BusinessName")) if filer is not None else None,
        "tax_yr": txt(h, "TaxYr"), "period_begin": txt(h, "TaxPeriodBeginDt"), "period_end": txt(h, "TaxPeriodEndDt"),
        "return_type_cd": txt(h, "ReturnTypeCd"),
        "street": street or None,
        "city": txt(a, "CityNm") if a is not None else None,
        "state": (txt(a, "StateAbbreviationCd") or txt(a, "ProvinceOrStateNm")) if a is not None else None,
        "zip5": zip5(txt(a, "ZIPCd")) if us is not None else None,
        "country": "US" if us is not None else (txt(fa, "CountryCd") if fa is not None else None),
    }


# ---------------------------------------------------------------- financials
def _sum(*vals):
    v = [x for x in vals if x is not None]
    return sum(v) if v else None


def _first(*vals):
    for v in vals:
        if v is not None:
            return v
    return None


def _fin_990(f) -> dict:
    return {
        "total_revenue": _first(amt(f, "CYTotalRevenueAmt"), amt(f, "TotalRevenueGrp/TotalRevenueColumnAmt")),
        "contributions_total": _first(amt(f, "TotalContributionsAmt"), amt(f, "CYContributionsGrantsAmt")),
        "federated_campaigns": amt(f, "FederatedCampaignsAmt"),
        "membership_dues": amt(f, "MembershipDuesAmt"),
        "fundraising_event_contributions": amt(f, "FundraisingAmt"),
        "related_org_contributions": amt(f, "RelatedOrganizationsAmt"),
        "government_grants": amt(f, "GovernmentGrantsAmt"),
        "other_contributions": amt(f, "AllOtherContributionsAmt"),
        "noncash_contributions": amt(f, "NoncashContributionsAmt"),
        "program_service_revenue": _first(amt(f, "TotalProgramServiceRevenueAmt"), amt(f, "CYProgramServiceRevenueAmt")),
        "investment_income": amt(f, "CYInvestmentIncomeAmt"),
        "special_events_net": amt(f, "NetIncmFromFundraisingEvtGrp/TotalRevenueColumnAmt"),
        "other_revenue": amt(f, "CYOtherRevenueAmt"),
        "total_expenses": _first(amt(f, "CYTotalExpensesAmt"), amt(f, "TotalFunctionalExpensesGrp/TotalAmt")),
        "program_expenses": amt(f, "TotalFunctionalExpensesGrp/ProgramServicesAmt"),
        "management_expenses": amt(f, "TotalFunctionalExpensesGrp/ManagementAndGeneralAmt"),
        "fundraising_expenses": amt(f, "TotalFunctionalExpensesGrp/FundraisingAmt"),
        "grants_paid": amt(f, "CYGrantsAndSimilarPaidAmt"),
        "compensation_total": amt(f, "CYSalariesCompEmpBnftPaidAmt"),
        "total_assets_eoy": _first(amt(f, "TotalAssetsEOYAmt"), amt(f, "TotalAssetsGrp/EOYAmt")),
        "total_liabilities_eoy": _first(amt(f, "TotalLiabilitiesEOYAmt"), amt(f, "TotalLiabilitiesGrp/EOYAmt")),
        "net_assets_eoy": _first(amt(f, "NetAssetsOrFundBalancesEOYAmt"), amt(f, "TotalNetAssetsFundBalanceGrp/EOYAmt")),
        "cash_savings_eoy": _sum(amt(f, "CashNonInterestBearingGrp/EOYAmt"), amt(f, "SavingsAndTempCashInvstGrp/EOYAmt")),
        "x_gross_receipts": amt(f, "GrossReceiptsAmt"),
        "x_py_total_revenue": amt(f, "PYTotalRevenueAmt"),
        "x_py_total_expenses": amt(f, "PYTotalExpensesAmt"),
        "x_p8_investment_income_line3": amt(f, "InvestmentIncomeGrp/TotalRevenueColumnAmt"),
        "x_fundraising_gross_income": amt(f, "FundraisingGrossIncomeAmt"),
        "x_grants_domestic_orgs": amt(f, "GrantsToDomesticOrgsGrp/TotalAmt"),
        "x_grants_domestic_indiv": amt(f, "GrantsToDomesticIndividualsGrp/TotalAmt"),
        "x_grants_foreign": amt(f, "ForeignGrantsGrp/TotalAmt"),
        "x_comp_current_officers": amt(f, "CompCurrentOfcrDirectorsGrp/TotalAmt"),
        "x_other_salaries": amt(f, "OtherSalariesAndWagesGrp/TotalAmt"),
        "x_total_assets_boy": amt(f, "TotalAssetsBOYAmt"),
        "x_net_assets_boy": amt(f, "NetAssetsOrFundBalancesBOYAmt"),
        "x_unrelated_business_revenue": amt(f, "TotalRevenueGrp/UnrelatedBusinessRevenueAmt"),
        "x_donor_advised_fund_ind": flag(f, "DonorAdvisedFundInd"),
        "x_grants_to_orgs_ind": flag(f, "GrantsToOrganizationsInd"),
    }


def _fin_ez(f) -> dict:
    return {
        "total_revenue": amt(f, "TotalRevenueAmt"),
        "contributions_total": amt(f, "ContributionsGiftsGrantsEtcAmt"),
        "membership_dues": amt(f, "MembershipDuesAmt"),
        "program_service_revenue": amt(f, "ProgramServiceRevenueAmt"),
        "investment_income": amt(f, "InvestmentIncomeAmt"),
        "special_events_net": amt(f, "SpecialEventsNetIncomeLossAmt"),
        "other_revenue": amt(f, "OtherRevenueTotalAmt"),
        "total_expenses": amt(f, "TotalExpensesAmt"),
        "program_expenses": amt(f, "TotalProgramServiceExpensesAmt"),
        "grants_paid": amt(f, "GrantsAndSimilarAmountsPaidAmt"),
        "compensation_total": amt(f, "SalariesOtherCompEmplBnftAmt"),
        "total_assets_eoy": amt(f, "Form990TotalAssetsGrp/EOYAmt"),
        "total_liabilities_eoy": amt(f, "SumOfTotalLiabilitiesGrp/EOYAmt"),
        "net_assets_eoy": _first(amt(f, "NetAssetsOrFundBalancesGrp/EOYAmt"), amt(f, "NetAssetsOrFundBalancesEOYAmt")),
        "cash_savings_eoy": amt(f, "CashSavingsAndInvestmentsGrp/EOYAmt"),
        "x_gross_receipts": amt(f, "GrossReceiptsAmt"),
        "x_fundraising_gross_income": amt(f, "FundraisingGrossIncomeAmt"),
        "x_ez_cash_includes_investments": 1,
    }


def _fin_pf(f) -> dict:
    a = f.find("AnalysisOfRevenueAndExpenses")
    b = f.find("Form990PFBalanceSheetsGrp")
    si = f.find("SupplementaryInformationGrp")
    return {
        "total_revenue": amt(a, "TotalRevAndExpnssAmt"),
        "contributions_total": amt(a, "ContriRcvdRevAndExpnssAmt"),
        # same scope as 990 Part I line 10 (interest, dividends, net gain on asset sales): PF lines 3 + 4a + 6a, col (a)
        "investment_income": _sum(amt(a, "InterestOnSavRevAndExpnssAmt"), amt(a, "DividendsRevAndExpnssAmt"),
                                  amt(a, "NetGainSaleAstRevAndExpnssAmt")),
        "other_revenue": amt(a, "OtherIncomeRevAndExpnssAmt"),
        "total_expenses": amt(a, "TotalExpensesRevAndExpnssAmt"),
        "grants_paid": amt(a, "ContriPaidRevAndExpnssAmt"),
        # same scope as 990 Part I line 15: PF lines 13-15, col (a)
        "compensation_total": _sum(amt(a, "CompOfcrDirTrstRevAndExpnssAmt"), amt(a, "OthEmplSlrsWgsRevAndExpnssAmt"),
                                   amt(a, "PensionEmplBnftRevAndExpnssAmt")),
        "total_assets_eoy": amt(b, "TotalAssetsEOYAmt"),
        "total_liabilities_eoy": amt(b, "TotalLiabilitiesEOYAmt"),
        "net_assets_eoy": _first(amt(b, "TotNetAstOrFundBalancesEOYAmt"), amt(b, "TotalNetAstOrFundBalancesEOYAmt")),
        "cash_savings_eoy": _sum(amt(b, "CashEOYAmt"), amt(b, "SavAndTempCashInvstEOYAmt")),
        "pf_fmv_assets_eoy": _first(amt(f, "FMVAssetsEOYAmt"), amt(b, "TotalAssetsEOYFMVAmt")),
        "pf_total_grants_paid": _first(amt(si, "TotalGrantOrContriPdDurYrAmt"), amt(a, "ContriPaidDsbrsChrtblAmt")),
        "pf_qualifying_distributions": amt(f, "PFQualifyingDistributionsGrp/QualifyingDistributionsAmt"),
        "pf_contributions_received": amt(a, "ContriRcvdRevAndExpnssAmt"),
        "x_pf_grants_paid_total_line3a": amt(si, "TotalGrantOrContriPdDurYrAmt"),
        "x_pf_approved_future_total_line3b": amt(si, "TotalGrantOrContriApprvFutAmt"),
        "x_pf_contri_paid_disbursed_col_d": amt(a, "ContriPaidDsbrsChrtblAmt"),
        "x_pf_total_disbursements_col_d": amt(a, "TotalExpensesDsbrsChrtblAmt"),
        "x_pf_total_operating_expenses": amt(a, "TotOprExpensesRevAndExpnssAmt"),
        "x_pf_interest": amt(a, "InterestOnSavRevAndExpnssAmt"),
        "x_pf_dividends": amt(a, "DividendsRevAndExpnssAmt"),
        "x_pf_net_gain_sale_assets": amt(a, "NetGainSaleAstRevAndExpnssAmt"),
        "x_pf_gross_rents": amt(a, "GrossRentsRevAndExpnssAmt"),
        "x_pf_net_investment_income": amt(a, "NetInvestmentIncomeAmt"),
        "x_pf_comp_officers": amt(a, "CompOfcrDirTrstRevAndExpnssAmt"),
        "x_pf_other_salaries": amt(a, "OthEmplSlrsWgsRevAndExpnssAmt"),
        "x_pf_pension_benefits": amt(a, "PensionEmplBnftRevAndExpnssAmt"),
        "x_pf_distributable_amount": amt(f, "DistributableAmountGrp/DistributableAsAdjustedAmt"),
        "x_pf_min_investment_return": amt(f, "MinimumInvestmentReturnGrp/MinimumInvestmentReturnAmt"),
        "x_pf_total_assets_eoy_fmv": amt(b, "TotalAssetsEOYFMVAmt"),
        "x_pf_operating_foundation_ind": flag(f, "StatementsRegardingActyGrp/PrivateOperatingFoundationInd"),
        "x_pf_4947a1_trust_ind": flag(f, "Organization4947a1TrtdPFInd"),
    }


# ---------------------------------------------------------------- profile
def _profile_990(f) -> dict:
    progs = []
    for node in (f, f.find("ProgSrvcAccomActy2Grp"), f.find("ProgSrvcAccomActy3Grp")):
        if node is None:
            continue
        d = txt(node, "Desc")
        if d or amt(node, "ExpenseAmt") is not None:
            progs.append({"desc": d, "expense": amt(node, "ExpenseAmt"), "grants": amt(node, "GrantAmt"),
                          "revenue": amt(node, "RevenueAmt")})
    return {
        "mission": txt(f, "ActivityOrMissionDesc"), "mission_part3": txt(f, "MissionDesc"), "programs": progs,
        "program_other_expense": amt(f, "TotalOtherProgSrvcExpenseAmt"),
        "program_total_expense": amt(f, "TotalProgramServiceExpensesAmt"),
        "website": txt(f, "WebsiteAddressTxt"), "formation_year": txt(f, "FormationYr"),
        "legal_domicile_state": txt(f, "LegalDomicileStateCd") or txt(f, "LegalDomicileCountryCd"),
        "employee_count": amt(f, "TotalEmployeeCnt"), "volunteer_count": amt(f, "TotalVolunteersCnt"),
        "voting_members": amt(f, "VotingMembersGoverningBodyCnt"),
        "principal_officer": txt(f, "PrincipalOfficerNm"),
    }


def _profile_ez(f) -> dict:
    progs = []
    for g in f.findall("ProgramSrvcAccomplishmentGrp"):
        progs.append({"desc": txt(g, "DescriptionProgramSrvcAccomTxt"), "expense": amt(g, "ProgramServiceExpensesAmt"),
                      "grants": amt(g, "GrantsAndAllocationsAmt"), "revenue": None})
    progs.sort(key=lambda p: -(p["expense"] or 0))
    return {
        "mission": txt(f, "PrimaryExemptPurposeTxt"), "mission_part3": None, "programs": progs[:3],
        "program_other_expense": None, "program_total_expense": amt(f, "TotalProgramServiceExpensesAmt"),
        "website": txt(f, "WebsiteAddressTxt"), "formation_year": None, "legal_domicile_state": None,
        "employee_count": None, "volunteer_count": None, "voting_members": None, "principal_officer": None,
    }


def _profile_pf(f) -> dict:
    progs = []
    g = f.find("SummaryOfDirectChrtblActyGrp")
    if g is not None:
        for i in range(1, 5):
            d = txt(g, f"Description{i}Txt")
            if d:
                progs.append({"desc": d, "expense": amt(g, f"Expenses{i}Amt"), "grants": None, "revenue": None})
    progs.sort(key=lambda p: -(p["expense"] or 0))
    return {
        "mission": None, "mission_part3": None, "programs": progs[:3], "program_other_expense": None,
        "program_total_expense": None, "website": txt(f, "StatementsRegardingActyGrp/WebsiteAddressTxt"),
        "formation_year": None, "legal_domicile_state": None, "employee_count": None, "volunteer_count": None,
        "voting_members": None, "principal_officer": None,
    }


# ---------------------------------------------------------------- roles
def _title_flags(title: str | None) -> tuple[int, int]:
    t = title or ""
    is_off = 1 if OFFICER_RE.search(t) else 0
    is_dir = 1 if DIRECTOR_RE.search(STAFF_DIRECTOR_RE.sub(" ", t)) else 0
    return is_off, is_dir


def _person(g) -> tuple[str | None, int]:
    p = txt(g, "PersonNm")
    if p:
        return p, 0
    return biz_name(g.find("BusinessName")), 1


def _path(el) -> str:
    return el.getroottree().getpath(el)


def _roles_990(f) -> list[dict]:
    out = []
    for i, g in enumerate(f.findall("Form990PartVIISectionAGrp"), 1):
        name, is_biz = _person(g)
        flags = {
            "is_officer": flag(g, "OfficerInd") or 0,
            "is_director_trustee": 1 if (flag(g, "IndividualTrusteeOrDirectorInd") or flag(g, "InstitutionalTrusteeInd")) else 0,
            "is_key_employee": flag(g, "KeyEmployeeInd") or 0,
            "is_highest_comp": flag(g, "HighestCompensatedEmployeeInd") or 0,
            "is_former": flag(g, "FormerOfcrDirectorTrusteeInd") or 0,
        }
        title = txt(g, "TitleTxt")
        if flags["is_officer"]:
            rt = "officer"
        elif flags["is_key_employee"]:
            rt = "key_employee"
        elif flags["is_director_trustee"]:
            rt = "board"
        elif flags["is_highest_comp"]:
            rt = "highest_compensated"
        else:  # former only (or no box checked): fall back to the title
            o, _ = _title_flags(title)
            rt = "officer" if o else "board"
        out.append({"name_display": name, "is_business": is_biz, "title": title, "role_type": rt, **flags,
                    "avg_hours_per_week": txt(g, "AverageHoursPerWeekRt"),
                    "x_hours_related_org": txt(g, "AverageHoursPerWeekRltdOrgRt"),
                    "reportable_comp_org": amt(g, "ReportableCompFromOrgAmt"),
                    "x_comp_related_org": amt(g, "ReportableCompFromRltdOrgAmt"),
                    "x_other_comp": amt(g, "OtherCompensationAmt"),
                    "x_institutional_trustee": flag(g, "InstitutionalTrusteeInd") or 0,
                    "x_part": "990_part_vii_a", "x_flags_basis": "checkbox", "xpath": _path(g), "seq": i})
    return out


def _roles_ez(f) -> list[dict]:
    out = []
    for i, g in enumerate(f.findall("OfficerDirectorTrusteeEmplGrp"), 1):
        name, is_biz = _person(g)
        title = txt(g, "TitleTxt")
        o, d = _title_flags(title)
        out.append({"name_display": name, "is_business": is_biz, "title": title,
                    "role_type": "officer" if o else "board", "is_officer": o, "is_director_trustee": d,
                    "is_key_employee": None, "is_highest_comp": None, "is_former": None,
                    "avg_hours_per_week": txt(g, "AverageHrsPerWkDevotedToPosRt") or txt(g, "AverageHoursPerWeekRt"),
                    "reportable_comp_org": amt(g, "CompensationAmt"),
                    "x_benefits": amt(g, "EmployeeBenefitProgramAmt"),
                    "x_expense_allowance": amt(g, "ExpenseAccountOtherAllwncAmt"),
                    "x_part": "990ez_part_iv", "x_flags_basis": "title_regex", "xpath": _path(g), "seq": i})
    return out


def _roles_pf(f) -> list[dict]:
    out = []
    info = f.find("OfficerDirTrstKeyEmplInfoGrp")
    if info is None:
        return out
    for i, g in enumerate(info.findall("OfficerDirTrstKeyEmplGrp"), 1):
        name, is_biz = _person(g)
        title = txt(g, "TitleTxt")
        o, d = _title_flags(title)
        out.append({"name_display": name, "is_business": is_biz, "title": title,
                    "role_type": "foundation_officer" if o else "foundation_trustee",
                    "is_officer": o, "is_director_trustee": d if (d or not o) else 0,
                    "is_key_employee": None, "is_highest_comp": None, "is_former": None,
                    "avg_hours_per_week": txt(g, "AverageHrsPerWkDevotedToPosRt"),
                    "reportable_comp_org": amt(g, "CompensationAmt"),
                    "x_benefits": amt(g, "EmployeeBenefitProgramAmt"),
                    "x_expense_allowance": amt(g, "ExpenseAccountOtherAllwncAmt"),
                    "x_part": "990pf_officers", "x_flags_basis": "title_regex", "xpath": _path(g), "seq": i})
    for i, g in enumerate(info.findall("CompensationHighestPaidEmplGrp"), 1):
        name, is_biz = _person(g)
        if not name or name.strip().upper() in ("NONE", "N/A", "NA"):
            continue
        out.append({"name_display": name, "is_business": is_biz, "title": txt(g, "TitleTxt"),
                    "role_type": "highest_compensated", "is_officer": 0, "is_director_trustee": 0,
                    "is_key_employee": None, "is_highest_comp": 1, "is_former": None,
                    "avg_hours_per_week": txt(g, "AverageHrsPerWkDevotedToPosRt"),
                    "reportable_comp_org": amt(g, "CompensationAmt"),
                    "x_benefits": amt(g, "EmployeeBenefitsAmt"), "x_expense_allowance": amt(g, "ExpenseAccountAmt"),
                    "x_part": "990pf_highest_paid_employees", "x_flags_basis": "section", "xpath": _path(g), "seq": i})
    return out


# ---------------------------------------------------------------- Schedule I Part III, Schedule R
def _sched_i_p3(si) -> list[dict]:
    out = []
    for i, g in enumerate(si.findall("GrantsOtherAsstToIndivInUSGrp"), 1):
        out.append({"grant_type": txt(g, "GrantTypeTxt"), "recipient_cnt": amt(g, "RecipientCnt"),
                    "cash": amt(g, "CashGrantAmt"), "noncash": amt(g, "NonCashAssistanceAmt"),
                    "valuation": txt(g, "ValuationMethodUsedDesc"), "noncash_desc": txt(g, "NonCashAssistanceDesc"),
                    "xpath": _path(g)})
    return out


SCHED_R = {
    "IdDisregardedEntitiesGrp": ("I", "disregarded_entity"),
    "IdRelatedTaxExemptOrgGrp": ("II", "related_tax_exempt_org"),
    "IdRelatedOrgTxblPartnershipGrp": ("III", "related_org_taxable_partnership"),
    "IdRelatedOrgTxblCorpTrGrp": ("IV", "related_org_taxable_corp_or_trust"),
    "TransactionsRelatedOrgGrp": ("V", "transaction_with_related_org"),
}


def _org_name(g) -> str | None:
    for c in g:
        t = c.tag if isinstance(c.tag, str) else ""
        if t.endswith("Name") and not t.startswith("DirectControlling"):
            n = biz_name(c) or (" ".join((c.text or "").split()) or None)
            if n:
                return n
    return None


def _sched_r(sr) -> list[dict]:
    out = []
    for g in sr:
        tag = g.tag if isinstance(g.tag, str) else ""
        if tag not in SCHED_R:
            continue
        part, kind = SCHED_R[tag]
        dce = biz_name(g.find("DirectControllingEntityName"))
        if not dce and flag(g, "DirectControllingNACd"):
            dce = "N/A"
        a = addr(g, "USAddress", "ForeignAddress")
        out.append({
            "part": part, "kind": kind, "name": _org_name(g),
            "ein": txt(g, "EIN") or txt(g, "RelatedOrganizationEIN") or txt(g, "OtherOrganizationEIN"),
            "state": a["state"], "country": a["country"],
            "primary_activity": txt(g, "PrimaryActivitiesTxt"),
            "legal_domicile": txt(g, "LegalDomicileStateCd") or txt(g, "LegalDomicileForeignCountryCd"),
            "direct_controlling_entity": dce,
            "exempt_code_section": txt(g, "ExemptCodeSectionTxt"),
            "public_charity_status": txt(g, "PublicCharityStatusTxt"),
            "controlled_org": flag(g, "ControlledOrganizationInd"),
            "entity_type": txt(g, "EntityTypeTxt"),
            "predominant_income": txt(g, "PredominantIncomeDesc") or txt(g, "PredominateIncomeDesc"),
            "share_total_income": amt(g, "ShareOfTotalIncomeAmt"),
            "share_eoy_assets": amt(g, "ShareOfEOYAssetsAmt"),
            "ownership_pct": txt(g, "OwnershipPct"),
            "total_income": amt(g, "TotalIncomeAmt"), "eoy_assets": amt(g, "EndOfYearAssetsAmt"),
            "transaction_type": txt(g, "TransactionTypeTxt"),
            "amount": amt(g, "InvolvedAmt"),
            "amount_method": txt(g, "MethodOfAmountDeterminationTxt"),
            "xpath": _path(g),
        })
    return out
