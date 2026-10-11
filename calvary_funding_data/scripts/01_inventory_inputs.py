"""Phase 1: inventory the user-provided PDFs in inputs/ and register each as a source.

Usage: .venv/bin/python scripts/01_inventory_inputs.py
Writes: sources/input_inventory.csv (one row per input file: PDFs + the CRM .xlsx export); upserts input_* rows
in sources/source_registry.csv.
Inputs are read-only. Idempotent: rerunning rewrites the same CSV and upserts the same registry rows.

Facts that the text layer does not carry (document type, publisher, what each file feeds) come from the
DOCS table below. Periods are detected from header text wherever a text layer exists and are cross-checked
against DOCS; any disagreement is logged and the detected value wins.
"""
from __future__ import annotations

import csv
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import INPUTS, SOURCES, log, register_source, rel, sha256_file  # noqa: E402

OUT = SOURCES / "input_inventory.csv"
FIELDS = ["filename", "doc_type", "apparent_publisher", "document_date", "tax_year", "fiscal_year",
          "period_start", "period_end", "pages", "text_extractable", "entities_mentioned", "data_contained",
          "feeds_tables", "status", "duplicate_of", "source_id", "sensitivity", "notes"]

CWS = "Calvary Women's Services, Inc."
GRF = "Gelman, Rosenberg & Freedman (auditor)"
BSB = "Burdette Smith & Bish LLC (auditor)"

# filename -> descriptive facts. tax_year/fiscal_year here are expectations; detection overrides.
DOCS = {
    "2015-Form-990-Calvary-Women_s-Services.pdf": dict(
        source_id="input_990_ty2014", doc_type="form_990", publisher=CWS, fy=2015,
        data="Form 990 TY2014 with schedules; Parts III-XII text; Part VII-A officers/directors",
        feeds="fact_org_financials;fact_roles;dim_person", status="partial",
        notes="Filename uses fiscal year. Page 1 (Part I summary, signature) is a scanned image with no text "
              "layer; Parts II onward are text. Tax period read from 'Form 990 (2014)' page headers + Sept FYE."),
    "2016-Form-990-Calvary-Women_s-Services.pdf": dict(
        source_id="input_990_ty2015", doc_type="form_990", publisher=CWS, fy=2016,
        data="Form 990 TY2015 with schedules; Parts III-XII text; Part VII-A",
        feeds="fact_org_financials;fact_roles;dim_person", status="partial",
        notes="Filename uses fiscal year. Page 1 is a scanned image (no Part I text). Tax period from "
              "'Form 990 (2015)' page headers + Sept FYE."),
    "2017-Form-990-Calvary-Women_s-Services.pdf": dict(
        source_id="input_990_ty2016_p1", doc_type="form_990", publisher=CWS, fy=2017,
        data="Form 990 TY2016 page 1 only (Part I summary + signature block), scanned",
        feeds="fact_org_financials", status="unreadable",
        notes="Single scanned page, no text layer; not OCR'd. Visually: tax year beginning OCT 1, 2016 and "
              "ending SEP 30, 2017 (TY2016 = FY17), total revenue 2,259,177, total expenses 2,076,427. "
              "Use the TY2016 e-file XML instead.",
        manual_period=("2016-10-01", "2017-09-30", 2016)),
    "Calvary-Womens-Service-2018-990.pdf": dict(
        source_id="input_990_ty2017", doc_type="form_990", publisher=CWS, fy=2018,
        data="Form 8879-EO + Form 990 TY2017 with schedules; Part I-XII text; Part VII-A",
        feeds="fact_org_financials;fact_roles;dim_person", status="ok",
        notes="Filename uses fiscal year (FY18 = TY2017). Page 1 is Form 8879-EO."),
    "2019-990-Form-990-CWS.pdf": dict(
        source_id="input_990_ty2018", doc_type="form_990", publisher=CWS, fy=2019,
        data="Form 990 TY2018 with schedules; Parts III-XII text; Part VII-A",
        feeds="fact_org_financials;fact_roles;dim_person", status="partial",
        notes="Filename uses fiscal year. Page 1 is a scanned image (no Part I text). Tax period from "
              "'Form 990 (2018)' page headers + Sept FYE."),
    "2020-Form-990-CWS.pdf": dict(
        source_id="input_990_ty2019", doc_type="form_990", publisher=CWS, fy=2020,
        data="Form 990 TY2019 with schedules; Part I-XII text; Part VII-A",
        feeds="fact_org_financials;fact_roles;dim_person", status="ok",
        notes="Filename uses fiscal year (FY20 = TY2019)."),
    "Calvary Womens Services Inc - Full Filing - Nonprofit Explorer - ProPublica.pdf": dict(
        source_id="input_propublica_990_ty2024", doc_type="form_990",
        publisher="ProPublica Nonprofit Explorer (IRS e-file public visual render)", fy=2025,
        data="Form 990 TY2024 full filing render incl. Schedules A, B (restricted), D, G, I, J, O",
        feeds="fact_org_financials;fact_roles;dim_person", status="ok",
        notes="ObjectId 202631539349300848, e-file submission 2026-06-02; newest filing, not in e-file indexes "
              "checked so far. Checkboxes are graphics: Part VII role flags derived from X-mark positions.",
        doc_date="2026-06-02"),
    "FY15-Audited-Financial-Statements.pdf": dict(
        source_id="input_fy15_audit", doc_type="audit", publisher=GRF, fy=2015,
        data="Audited FS FY15 with FY14 summarized comparatives; SFP, SOA, functional expenses, cash flows, notes",
        feeds="fact_org_financials;fact_gov_awards;dim_funder", status="ok",
        notes="No SEFA. Note 3 names government grantors (TCP; DC Government; HUD)."),
    "2016-Audited-Financial-Statements.pdf": dict(
        source_id="input_fy16_audit", doc_type="audit", publisher=GRF, fy=2016,
        data="Audited FS FY16 with FY15 summarized comparatives",
        feeds="fact_org_financials;fact_gov_awards;dim_funder", status="ok",
        notes="No SEFA. Note 3 names TCP, DC Government, HUD, FEMA."),
    "2017-Audited-Financial-Statements-Calvary-Women_s-Services.pdf": dict(
        source_id="input_fy17_audit", doc_type="audit", publisher=GRF, fy=2017,
        data="Audited FS FY17 with FY16 summarized comparatives",
        feeds="fact_org_financials;fact_gov_awards;dim_funder", status="ok",
        notes="No SEFA; note states Calvary was not subject to a Uniform Guidance single audit for FY17."),
    "CWS-FY18-Audit-.pdf": dict(
        source_id="input_fy18_audit", doc_type="audit", publisher=BSB, fy=2018,
        data="Audited FS FY18 and FY17 (two-year SOA)",
        feeds="fact_org_financials;fact_gov_awards;dim_funder", status="ok",
        notes="No SEFA; not subject to single audit FY18/FY17. Several subtotal lines are unlabeled."),
    "2019-Audited-Financial-Statements-CWS.pdf": dict(
        source_id="input_fy19_audit", doc_type="audit", publisher=BSB, fy=2019,
        data="Audited FS FY19 and FY18 (FY18 reclassified: special events shown net)",
        feeds="fact_org_financials;fact_gov_awards;dim_funder", status="ok",
        notes="No SEFA; not subject to single audit. FY18 comparative differs from FY18 audit (events net)."),
    "2020-Audited-Financial-Statements-CWS.pdf": dict(
        source_id="input_fy20_audit", doc_type="audit", publisher=BSB, fy=2020,
        data="Audited FS FY20 and FY19; PPP loan forgiveness note",
        feeds="fact_org_financials;fact_gov_awards;dim_funder", status="ok",
        notes="No SEFA; not subject to single audit. PPP $327,200 recognized as forgiveness of debt."),
    "2021-Audited-Financial-Statements-CWS.pdf": dict(
        source_id="input_fy21_audit", doc_type="audit", publisher="Independent auditor (firm not named in text layer)",
        fy=2021, data="Audited FS FY21 (single year)",
        feeds="fact_org_financials;fact_gov_awards;dim_funder", status="ok",
        notes="No SEFA and no Uniform Guidance statement despite $1.98M federal and local government "
              "contracts. Subsequent-events note: $3.3M multi-year OVSJG grant for Sisters Rise (Feb 2022)."),
    "Calvary-Womens-Services-Inc.-9.30.23-FS.pdf": dict(
        source_id="input_fy23_audit", doc_type="audit", publisher="Independent auditor (firm not named in text layer)",
        fy=2023, data="Audited FS FY23 and FY22 + Uniform Guidance single audit: SEFA, findings",
        feeds="fact_org_financials;fact_gov_awards;dim_funder", status="ok",
        notes="SEFA on PDF p31 (printed p28): Treasury via OVSJG, HUD via TCP, DHS/FEMA EFSP, USDA via DC DHS. "
              "Major program ALN 21.027; not a low-risk auditee; no findings."),
    "Calvary-Women_s-Services-FY2015-Annual-Report.pdf": dict(
        source_id="input_fy15_annual_report", doc_type="annual_report", publisher=CWS, fy=2015,
        data="Program metrics; revenue/expense % splits; donor list by gift band (orgs + individuals)",
        feeds="dim_funder;fact_grants;fact_org_financials", status="ok",
        notes="Only annual report in the set with a donor list. Individuals stored as band counts only."),
    "Calvary-Women_s-Services-FY2017-Annual-Report.pdf": dict(
        source_id="input_fy17_annual_report", doc_type="annual_report", publisher=CWS, fy=2017,
        data="Program metrics; revenue/expense % pies; board with affiliations; full staff list",
        feeds="fact_org_financials;fact_roles;dim_person;fact_org_relationships", status="ok",
        notes="No donor list (says list of funders available on request)."),
    "Calvary-Womens-Services_FY18-Annual-Report.pdf": dict(
        source_id="input_fy18_annual_report", doc_type="annual_report", publisher=CWS, fy=2018,
        data="2018 at a glance metrics; revenue/expense % splits",
        feeds="fact_org_financials", status="ok",
        notes="No donor or board list; points to calvaryservices.org/about/corporate."),
    "Calvary-Womens-Services-2020-Annual-Report.pdf": dict(
        source_id="input_fy20_annual_report", doc_type="annual_report", publisher=CWS, fy=2020,
        data="Program metrics; revenue/expense % splits; 2020 board with affiliations; leadership staff",
        feeds="fact_org_financials;fact_roles;dim_person;fact_org_relationships", status="ok",
        notes="Totals match FY20 audit (rev $3,908,836; exp $3,228,518)."),
    "Calvary-2021-AR-Working-C.pdf": dict(
        source_id="input_fy21_annual_report", doc_type="annual_report", publisher=CWS, fy=2021,
        data="Program metrics; revenue/expense % splits; 2021 board with affiliations; leadership staff",
        feeds="fact_org_financials;fact_roles;dim_person;fact_org_relationships", status="ok",
        notes="Filename says 'Working-C' (a working draft label). Expense total $3,411,994 vs audit $3,411,954."),
    "Calvary-FY23-Annual-Report-.pdf": dict(
        source_id="input_fy23_annual_report", doc_type="annual_report", publisher=CWS, fy=2023,
        data="Program metrics; revenue/expense % splits; 2023 board with affiliations; DEI percentages",
        feeds="fact_org_financials;fact_roles;dim_person;fact_org_relationships", status="ok",
        notes="'2023 Revenue $5,423,322' equals the audit's without-donor-restriction column incl. releases, "
              "not total revenue ($4,807,645). Board DEI % (90%, 50%) are vector graphics, transcribed visually."),
    "Calvary-FY23-Annual-Report-Flyer.pdf": dict(
        source_id="input_fy23_ar_flyer", doc_type="annual_report_summary", publisher=CWS, fy=2023,
        data="FY23 at-a-glance metrics (subset of FY23 annual report)",
        feeds="", status="duplicate", duplicate_of="Calvary-FY23-Annual-Report-.pdf",
        notes="Every figure also appears in the FY23 annual report; extracted anyway and flagged."),
    "Calvary-FY24-Annual-Report-at-Glance-Final.pdf": dict(
        source_id="input_fy24_ar_glance", doc_type="annual_report_summary", publisher=CWS, fy=2024,
        data="'At a glance | 2024' program metrics",
        feeds="", status="ok",
        notes="Fiscal year assumed FY24 from filename/title; PDF created 2025-11-12 (after FY25 close), so "
              "it may describe FY25. Confidence medium."),
    "Corporate & Foundation Support - Calvary Women's Services.pdf": dict(
        source_id="input_corp_found_support_2023", doc_type="web_export", publisher=CWS + " (website printout)",
        fy=None, data="Corporate Partners Program tiers (Empower/Change/Hope/Support) and Institutional Support list",
        feeds="dim_funder;fact_grants", status="partial",
        notes="Browser print of calvaryservices.org Corporate & Foundation Support page, 'Current as of "
              "September 2023' (footer (c) 2026). Third column of the Support tier is clipped at the page edge; "
              "three Empower-tier names are logo images. Cumulative 'over the years' list, no amounts or years.",
        doc_date="2023-09"),
    "Foundation & Corporate Funders_2023-2026.xlsx": dict(
        source_id="input_crm_funders_2023_2026", doc_type="crm_export",
        publisher=CWS + " (donor CRM export)", fy=None, sensitivity="internal", doc_date="2026-10-05",
        data="One sheet, one row per organizational donor: name, city, state, last gift amount/date, gift total, "
             "number of gifts",
        feeds="dim_funder;fact_grants", status="ok",
        notes="Sheet 'Listings_2026-10-05_01-03-55 (1'; export date from sheet name. All rows are organizations "
              "('last_name' holds the org name). GIFT_TOTAL window unconfirmed: may be lifetime, not 2023-2026. "
              "period_start/end = range of LAST_CONTRIB_DATE."),
    "Calvary Strategic Plan 2016-2019 (1).pdf": dict(
        source_id="input_strategic_plan_2016_2019", doc_type="strategic_plan", publisher=CWS, fy=None,
        data="2016-2019 strategic plan: directions (Housing, Livelihood, Leadership), actions, guideposts, values",
        feeds="", status="ok", notes="Plan period 2016-2019. Context for analysis, not a fact table."),
    "Strategic Plan 2016-2019 Report (1).pdf": dict(
        source_id="input_strategic_plan_2016_2019_report", doc_type="strategic_plan_report", publisher=CWS,
        fy=None, data="Results against the 2016-2019 plan (housing slots, Reach Up funding by source, Step Up DC, "
                      "communications)",
        feeds="", status="ok", notes="Slide deck export. Context for analysis."),
    "Calvary Strategic Plan 2021-2024 FINAL (1).pdf": dict(
        source_id="input_strategic_plan_2021_2024", doc_type="strategic_plan", publisher=CWS, fy=None,
        data="2021-2024 strategic plan: Creating More Housing, Strengthening Our Leadership, Telling Our Story",
        feeds="", status="ok",
        notes="PDF metadata title reads 'Calvary Strategic Plan 2020-2023 FINAL DRAFT'; cover says 2021-2024."),
    "2021-2024 Strategic Plan Final Report_internal (1).pdf": dict(
        source_id="input_strategic_plan_2021_2024_report_internal", doc_type="strategic_plan_report",
        publisher=CWS, fy=None, sensitivity="internal",
        data="Final report on the 2021-2024 plan: actions vs accomplishments (housing units added, leadership hires, "
             "fundraising staff)",
        feeds="", status="ok",
        notes="Marked internal. Says the plan guided Calvary through 2025. Housing units 66 = '18 TH, 15 PSH, "
              "31 RRH' as printed (components sum to 64)."),
    "CWS-Donor-Privacy-Policy.pdf": dict(
        source_id="input_donor_privacy_policy", doc_type="policy", publisher=CWS, fy=None,
        data="Donor privacy policy (no sale/sharing of donor names or information)",
        feeds="", status="ok",
        notes="Basis for storing individual donors as band counts only."),
}

# Entity patterns scanned in every text layer -> short display names for entities_mentioned.
ENTITY_PATTERNS = [
    (r"Community Partnership", "The Community Partnership for the Prevention of Homelessness (TCP)"),
    (r"Office of Victim Services and Justice Grants|OVSJG", "DC Office of Victim Services and Justice Grants (OVSJG)"),
    (r"Department of Human Services", "DC Department of Human Services (DHS)"),
    (r"Housing and Urban Development|\bHUD\b", "U.S. Department of Housing and Urban Development (HUD)"),
    (r"Federal Emergency Management|\bFEMA\b", "Federal Emergency Management Agency (FEMA)"),
    (r"Department of the Treasury", "U.S. Department of the Treasury"),
    (r"Department of Homeland Security", "U.S. Department of Homeland Security"),
    (r"Department of Agriculture", "U.S. Department of Agriculture"),
    (r"Paycheck Protection", "SBA Paycheck Protection Program"),
    (r"Interagency Council on Homelessness", "DC Interagency Council on Homelessness"),
    (r"Department of Health Care Finance", "DC Department of Health Care Finance"),
    (r"GELMAN|Gelman|GRFCPA", "Gelman, Rosenberg & Freedman"),
    (r"BURDETTE SMITH|Burdette Smith|BSBLLC", "Burdette Smith & Bish LLC"),
    (r"JM&M", "JM&M (preparer)"),
]


def xlsx_summary(p: Path):
    """(sheet count, cell text, extractable note, (min date, max date) of LAST_CONTRIB_DATE)."""
    import openpyxl
    wb = openpyxl.load_workbook(p, read_only=True, data_only=True)
    texts, dates, nrows = [], [], 0
    for ws in wb.worksheets:
        hdr = None
        for row in ws.iter_rows(values_only=True):
            if hdr is None:
                hdr = [str(c) for c in row]
                continue
            nrows += 1
            texts.append(" ".join("" if c is None else str(c) for c in row))
            if "LAST_CONTRIB_DATE" in hdr and row[hdr.index("LAST_CONTRIB_DATE")] is not None:
                dates.append(str(row[hdr.index("LAST_CONTRIB_DATE")])[:10])
    n = len(wb.worksheets)
    wb.close()
    return n, "\n".join(texts), f"yes (spreadsheet, {n} sheet, {nrows} data rows)", \
        ((min(dates), max(dates)) if dates else ("", ""))


def pdf_pages(p: Path) -> int:
    out = subprocess.run(["pdfinfo", str(p)], capture_output=True, text=True).stdout
    m = re.search(r"^Pages:\s+(\d+)", out, re.M)
    return int(m.group(1)) if m else 0


def pdf_created(p: Path) -> str:
    out = subprocess.run(["pdfinfo", "-isodates", str(p)], capture_output=True, text=True).stdout
    m = re.search(r"^CreationDate:\s+(\d{4}-\d{2}-\d{2})", out, re.M)
    return m.group(1) if m else ""


def page_texts(p: Path, n: int) -> list[str]:
    return [subprocess.run(["pdftotext", "-layout", "-f", str(i), "-l", str(i), str(p), "-"],
                           capture_output=True, text=True).stdout for i in range(1, n + 1)]


MONTHS = {m: i for i, m in enumerate(["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT",
                                      "NOV", "DEC"], 1)}


def _d(s: str) -> str | None:
    """'OCT 1, 2019' / 'SEP 30, 2020' / '10-01-2024' -> ISO date."""
    s = s.strip().upper()
    m = re.match(r"(\d{2})-(\d{2})-(\d{4})", s)
    if m:
        return f"{m.group(3)}-{m.group(1)}-{m.group(2)}"
    m = re.match(r"([A-Z]{3})[A-Z]*\.?\s+(\d{1,2}),?\s*(\d{4})", s)
    if m and m.group(1) in MONTHS:
        return f"{m.group(3)}-{MONTHS[m.group(1)]:02d}-{int(m.group(2)):02d}"
    return None


def detect_period(doc_type: str, text: str):
    """Return (period_start, period_end, tax_year, fiscal_year, basis) from header text, or Nones."""
    t = re.sub(r"[ \t]+", " ", text)
    if doc_type == "form_990":
        m = re.search(r"tax year beginning\s+([A-Z]{3}\s+\d{1,2},\s*\d{4}|\d{2}-\d{2}-\d{4})\s*,?\s*and ending\s+"
                      r"([A-Z]{3}\s+\d{1,2},\s*\d{4}|\d{2}-\d{2}-\d{4})", t, re.I)
        if m:
            s, e = _d(m.group(1)), _d(m.group(2))
            if s and e:
                return s, e, int(s[:4]), int(e[:4]), "Form 990 page 1 header"
        m = re.search(r"Form 990 \((\d{4})\)", t)
        if m:
            ty = int(m.group(1))
            return f"{ty}-10-01", f"{ty + 1}-09-30", ty, ty + 1, "'Form 990 (YYYY)' page header + Sept 30 FYE"
    if doc_type == "audit":
        m = re.search(r"(?:YEARS? ENDED|AS OF)\s+SEPTEMBER 30,\s*(\d{4})|^\s*SEPTEMBER 30,\s*(\d{4})", t, re.I | re.M)
        if m:
            fy = int(m.group(1) or m.group(2))
            return f"{fy - 1}-10-01", f"{fy}-09-30", fy - 1, fy, "audit title 'September 30, YYYY'"
    if doc_type in ("annual_report", "annual_report_summary"):
        m = (re.search(r"(\d{4})\s+Annual Report", t) or re.search(r"Annual Report\s+(\d{4})", t)
             or re.search(r"AT A GLANCE\s*\|\s*(\d{4})", t))
        if m:
            fy = int(m.group(1))
            return f"{fy - 1}-10-01", f"{fy}-09-30", fy - 1, fy, "report title year taken as fiscal year"
    return None, None, None, None, ""


def audit_report_date(texts: list[str]) -> str | None:
    for t in texts[:6]:
        m = re.search(r"^\s*((?:January|February|March|April|May|June|July|August|September|October|November|"
                      r"December)\s+\d{1,2},\s+\d{4})\s*$", t, re.M)
        if m:
            return _d(m.group(1))
    return None


def main():
    files = sorted(p for p in INPUTS.iterdir() if p.suffix.lower() in (".pdf", ".xlsx"))
    rows, problems = [], []
    unknown = [p.name for p in files if p.name not in DOCS]
    if unknown:
        problems.append(f"input files without a DOCS entry (skipped): {unknown}")
    for p in files:
        meta = DOCS.get(p.name)
        if not meta:
            continue
        if p.suffix.lower() == ".xlsx":
            n, full, extractable, xl_range = xlsx_summary(p)
        else:
            n = pdf_pages(p)
            texts = page_texts(p, n)
            full = "\n".join(texts)
            with_text = sum(1 for t in texts if len(t.strip()) > 50)
            extractable = "yes" if with_text == n else ("no" if with_text == 0 else f"partial ({with_text}/{n} pages)")

        ps, pe, ty, fy, basis = detect_period(meta["doc_type"], full)
        if meta["doc_type"] == "crm_export":
            ps, pe, basis = xl_range[0], xl_range[1], "range of LAST_CONTRIB_DATE (gift-total window unconfirmed)"
        if meta.get("manual_period"):
            ps, pe, ty = meta["manual_period"]
            fy, basis = ty + 1, "read visually from scanned page 1 (no text layer)"
        if fy and meta.get("fy") and fy != meta["fy"]:
            problems.append(f"{p.name}: detected fiscal_year {fy} != expected {meta['fy']}")
        if not fy and meta.get("fy"):
            fy, ty = meta["fy"], meta["fy"] - 1
            ps, pe, basis = f"{ty}-10-01", f"{fy}-09-30", "expected value (no period text found)"

        doc_date = meta.get("doc_date")
        date_basis = "stated"
        if not doc_date and meta["doc_type"] == "audit":
            doc_date = audit_report_date(texts)
            date_basis = "auditor report date"
        if not doc_date:
            doc_date, date_basis = pdf_created(p), "PDF creation date"

        ents = [CWS]
        for pat, name in ENTITY_PATTERNS:
            if re.search(pat, full) and name not in ents:
                ents.append(name)

        notes = meta["notes"]
        if basis:
            notes += f" Period basis: {basis}."
        notes += f" document_date basis: {date_basis}."
        row = dict(filename=p.name, doc_type=meta["doc_type"], apparent_publisher=meta["publisher"],
                   document_date=doc_date, tax_year=ty or "", fiscal_year=fy or "",
                   period_start=ps or "", period_end=pe or "", pages=n, text_extractable=extractable,
                   entities_mentioned="; ".join(ents), data_contained=meta["data"], feeds_tables=meta["feeds"],
                   status=meta["status"], duplicate_of=meta.get("duplicate_of", ""), source_id=meta["source_id"],
                   sensitivity=meta.get("sensitivity", "public"), notes=notes)
        rows.append(row)

        period = f"FY{fy} (TY{ty}, {ps} to {pe})" if fy else "no fiscal period"
        cite = f"{CWS}, {p.name.rsplit('.', 1)[0]} ({meta['doc_type']}, {period}). User-provided PDF."
        unit = "sheets" if p.suffix.lower() == ".xlsx" else "pages"
        register_source(meta["source_id"], f"{meta['doc_type']}: {p.name}", f"inputs/{p.name}",
                        meta["publisher"], cite,
                        f"{n} {unit}; text {extractable}; sha256 {sha256_file(p)[:16]}; status {meta['status']}; "
                        f"sensitivity {meta.get('sensitivity', 'public')}")

    SOURCES.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    by_status = {}
    for r in rows:
        by_status[r["status"]] = by_status.get(r["status"], 0) + 1
    msg = (f"- {rel(OUT)}: {len(rows)} rows ({', '.join(f'{k}={v}' for k, v in sorted(by_status.items()))})\n"
           f"- registered {len(rows)} input_* sources\n"
           + ("".join(f"- WARNING: {x}\n" for x in problems) if problems else "- period checks: all match\n"))
    log("01_inventory_inputs", msg)
    print(msg)


if __name__ == "__main__":
    main()
