"""Phase 1: structured extraction from the user-provided files in inputs/ (read-only).

Usage: .venv/bin/python scripts/02_extract_inputs.py
Reads:  inputs/*.pdf, inputs/*.xlsx, sources/input_inventory.csv (run 01_inventory_inputs.py first)
Writes: raw/inputs_extracted/  (deterministic file names; a rerun overwrites with identical content)
  text/<stem>.txt                  pdftotext -layout for every PDF
  audit_financials.csv             SOA + SFP line items, long format, per fiscal year per document
  audit_tieout_checks.csv          QC: do revenue/expense/balance-sheet lines sum to their printed totals
  sefa_federal_awards.csv          Schedule of Expenditures of Federal Awards rows (only FY23 audit has one)
  form990_pdf_financials.csv       Part I, Part VIII, Part IX line 25, Part X key lines per readable 990 PDF
  form990_pdf_people.csv           Part VII Section A (names, titles, hours, role flags, reportable comp)
  form990_pdf_schedule_i.csv       Schedule I rows (TY2024 render only)
  funder_mentions.csv              organizations named as supporters (annual reports, support page, audit notes)
  individual_donor_band_counts.csv individual donors as counts per gift band (names never stored)
  board_lists.csv                  board members + leadership staff with the affiliation Calvary prints
  annual_report_metrics.csv        program metrics and revenue/expense % splits
  crm_funders_2023_2026.csv        CRM export rows as-is + funder_name_norm, org_type_guess, source_id, notes
                                   (INTERNAL; GIFT_TOTAL window unconfirmed, may be lifetime)
  strategic_plan_targets.csv       quantified goals and reported results from the strategic plans/reports

`page` columns are 1-based PDF page indexes (not the printed page numbers).

line_item_std vocabulary (audit_financials.csv)
  Statement of Activities (statement=SOA)
    rev_contributions_private      contributions and grants / individual, foundation and corporate grants
    rev_gov_unspecified            "Government grants" (level not split; notes say DC + HUD via TCP + FEMA)
    rev_gov_federal_and_local      "Federal and local government contracts" (mixed levels)
    rev_gov_federal                federal grants (incl. COVID-19), federal entitlements
    rev_gov_state_local            state and local government contributions and grants
    rev_inkind                     contributed services and materials, in-kind services, in-kind goods
    rev_special_events_net         fundraising event revenue shown net of direct costs
    rev_investment                 interest and investment income
    rev_other                      miscellaneous / other income
    rev_ppp_forgiveness            PPP loan forgiveness (forgiveness of debt)
    rev_released_from_restrictions net assets released (zero in the total column)
    rev_total_before_releases      subtotal printed before releases (unlabeled in BSB audits)
    rev_total                      total revenue and support
    exp_program_detail             a single program's expense (line_item keeps the program name)
    exp_program_total, exp_mgmt_general, exp_fundraising, exp_support_total, exp_total
    change_in_net_assets, net_assets_beginning, net_assets_end
  Statement of Financial Position (statement=SFP; net_asset_class=n/a except net-asset lines)
    cash, restricted_cash, pledges_receivable, grants_receivable, other_current_asset,
    total_current_assets, fixed_assets_gross, accumulated_depreciation, fixed_assets_net, other_asset,
    total_other_assets, total_assets, total_current_liabilities, debt, other_liability,
    total_noncurrent_liabilities, total_liabilities, net_assets_without_donor_restrictions,
    net_assets_with_donor_restrictions, net_assets_total, total_liabilities_and_net_assets
  Rows whose line_item starts with "(derived)" are computed from printed lines (noted); everything else is
  as printed. "Unrestricted"/"Temporarily restricted" columns map to without/with donor restrictions.
"""
from __future__ import annotations

import csv
import itertools
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import pdfplumber

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import INPUTS, RAW, SOURCES, append_md, log, norm_name, rel, today  # noqa: E402

OUT = RAW / "inputs_extracted"
TEXT = OUT / "text"
INV = SOURCES / "input_inventory.csv"
RETRIEVED = today()

AMT = re.compile(r"^\(?-?\$?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?\.?\)?$")


# ---------------------------------------------------------------- helpers
def load_inventory() -> dict[str, dict]:
    with open(INV, newline="", encoding="utf-8") as f:
        return {r["filename"]: r for r in csv.DictReader(f)}


def sid_for(inv, fname) -> str:
    return inv[fname]["source_id"]


def layout_page(pdf: Path, page: int) -> str:
    return subprocess.run(["pdftotext", "-layout", "-f", str(page), "-l", str(page), str(pdf), "-"],
                          capture_output=True, text=True, check=True).stdout


def plain_text(pdf: Path, first: int | None = None, last: int | None = None) -> str:
    cmd = ["pdftotext"]
    if first:
        cmd += ["-f", str(first)]
    if last:
        cmd += ["-l", str(last)]
    return subprocess.run(cmd + [str(pdf), "-"], capture_output=True, text=True, check=True).stdout


def to_num(tok: str) -> float | None:
    t = tok.strip().replace("$", "").replace(",", "")
    if t in ("-", "–", "—", "-0-"):
        return 0.0
    neg = t.startswith("(") and t.endswith(")")
    t = t.strip("()").rstrip(".")
    if not re.fullmatch(r"-?\d+(\.\d+)?", t):
        return None
    v = float(t)
    return -v if neg else v


def fmt(v):
    if v is None or v == "":
        return ""
    return int(v) if float(v).is_integer() else v


def write_csv(name: str, fields: list[str], rows: list[dict]) -> Path:
    p = OUT / name
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    return p


# ---------------------------------------------------------------- 1. text dumps
def dump_texts() -> int:
    TEXT.mkdir(parents=True, exist_ok=True)
    n = 0
    for p in sorted(INPUTS.glob("*.pdf")):
        subprocess.run(["pdftotext", "-layout", str(p), str(TEXT / f"{p.stem}.txt")], check=True)
        n += 1
    return n


# ---------------------------------------------------------------- 2. audits
# Each statement: (pdf_page, statement, [(fiscal_year, net_asset_class, is_prior), ...]) in printed column order.
W, R, T, NA = "without_donor_restrictions", "with_donor_restrictions", "total", "n/a"
AUDITS = {
    "FY15-Audited-Financial-Statements.pdf": [
        (5, "SFP", [(2015, NA, False), (2014, NA, True)]),
        (6, "SOA", [(2015, W, False), (2015, R, False), (2015, T, False), (2014, T, True)])],
    "2016-Audited-Financial-Statements.pdf": [
        (5, "SFP", [(2016, NA, False), (2015, NA, True)]),
        (6, "SOA", [(2016, W, False), (2016, R, False), (2016, T, False), (2015, T, True)])],
    "2017-Audited-Financial-Statements-Calvary-Women_s-Services.pdf": [
        (5, "SFP", [(2017, NA, False), (2016, NA, True)]),
        (6, "SOA", [(2017, W, False), (2017, R, False), (2017, T, False), (2016, T, True)])],
    "CWS-FY18-Audit-.pdf": [
        (5, "SFP", [(2018, NA, False), (2017, NA, True)]),
        (6, "SOA", [(2018, W, False), (2018, R, False), (2018, T, False)]),
        (7, "SOA", [(2017, W, True), (2017, R, True), (2017, T, True)])],
    "2019-Audited-Financial-Statements-CWS.pdf": [
        (4, "SFP", [(2019, NA, False), (2018, NA, True)]),
        (5, "SOA", [(2019, W, False), (2019, R, False), (2019, T, False)]),
        (6, "SOA", [(2018, W, True), (2018, R, True), (2018, T, True)])],
    "2020-Audited-Financial-Statements-CWS.pdf": [
        (4, "SFP", [(2020, NA, False), (2019, NA, True)]),
        (5, "SOA", [(2020, W, False), (2020, R, False), (2020, T, False)]),
        (6, "SOA", [(2019, W, True), (2019, R, True), (2019, T, True)])],
    "2021-Audited-Financial-Statements-CWS.pdf": [
        (5, "SFP", [(2021, NA, False)]),
        (6, "SOA", [(2021, W, False), (2021, R, False), (2021, T, False)])],
    "Calvary-Womens-Services-Inc.-9.30.23-FS.pdf": [
        (6, "SFP", [(2023, NA, False), (2022, NA, True)]),
        (7, "SOA", [(2023, W, False), (2023, R, False), (2023, T, False)]),
        (8, "SOA", [(2022, W, True), (2022, R, True), (2022, T, True)])],
}
SKIP_LINE = re.compile(r"accompanying notes|integral part|^\s*-?\s*\d+\s*-?\s*$|EXHIBIT|CALVARY WOMEN|"
                       r"STATEMENTS? OF|FOR THE YEARS? ENDED|^\s*YEAR ENDED|AS OF SEPTEMBER|SEPTEMBER 30, \d{4}( AND)?|"
                       r"SUMMARIZED FINANCIAL|^\s*(Temporarily|Without|With|Donor|Restrictions|Unrestricted|"
                       r"Restricted|Total)(\s+(Temporarily|Without|With|Donor|Restrictions|Unrestricted|Restricted|"
                       r"Total))*\s*$", re.I)
HEADING_SECTIONS = [
    (r"^REVENUE", "revenue"), (r"^EXPENSES", "expenses"), (r"^Program Services:?$", "program"),
    (r"^Support(ing)? Services:?$", "support"), (r"^ASSETS$", "assets"), (r"^CURRENT ASSETS", "current_assets"),
    (r"^(FIXED ASSETS|PROPERTY AND EQUIPMENT)", "fixed_assets"), (r"^OTHER ASSETS", "other_assets"),
    (r"^INVESTMENTS", "other_assets"), (r"^LIABILITIES AND NET ASSETS", "liabilities"),
    (r"^CURRENT LIABILITIES", "current_liabilities"),
    (r"^(LONG-TERM|NON-CURRENT|OTHER) LIABILITIES", "noncurrent_liabilities"), (r"^COMMITMENTS", None),
    (r"^NET ASSETS$", "net_assets"),
]


def split_amounts(line: str):
    """Split a layout line into (label, [amount tokens]) reading numbers from the right."""
    toks = line.split()
    nums = []
    while toks:
        t = toks[-1]
        if t == "$":
            toks.pop()
            continue
        if t.startswith("$") and len(t) > 1:
            t = t[1:]
        if AMT.match(t) or t in ("-", "–", "—"):
            nums.insert(0, t)
            toks.pop()
        else:
            break
    label = " ".join(toks)
    label = re.sub(r"[.…·]{2,}.*$", "", label).strip(" .…$")
    label = re.sub(r"\s+", " ", label)
    # numbers-only rows that are just column-year headers ("2015  2014")
    if not label and nums and all(re.fullmatch(r"(19|20)\d\d", n) for n in nums):
        return "", []
    return label, nums


def std_soa(label: str, section: str, unlabeled_ctx: str) -> str:
    l = label.lower()
    if not label:
        return {"before_releases": "rev_total_before_releases", "after_releases": "rev_total",
                "after_expenses": "exp_total"}.get(unlabeled_ctx, "unlabeled")
    rules = [
        (r"^(contributions and grants|grants and contributions|individual, foundation and corporate)",
         "rev_contributions_private"),
        (r"^government grants", "rev_gov_unspecified"),
        (r"^federal and local government contracts", "rev_gov_federal_and_local"),
        (r"^federal (grants|entitlements)", "rev_gov_federal"),
        (r"^state and local government", "rev_gov_state_local"),
        (r"contributed services|in-kind", "rev_inkind"),
        (r"fundraising event", "rev_special_events_net"),
        (r"interest income|investment income", "rev_investment"),
        (r"miscellaneous revenue|other income", "rev_other"),
        (r"forgiveness of debt", "rev_ppp_forgiveness"),
        (r"net assets released", "rev_released_from_restrictions"),
        (r"^total revenue", "rev_total"),
        (r"^total program", "exp_program_total"),
        (r"^program services$", "exp_program_total"),
        (r"management and general", "exp_mgmt_general"),
        (r"^fundraising$", "exp_fundraising"),
        (r"^total support", "exp_support_total"),
        (r"^total expenses", "exp_total"),
        (r"change in net assets", "change_in_net_assets"),
        (r"net assets,? (at )?beginning", "net_assets_beginning"),
        (r"net assets,? (at )?end", "net_assets_end"),
    ]
    for pat, std in rules:
        if re.search(pat, l):
            return std
    if section == "program":
        return "exp_program_detail"
    return "unmapped"


def std_sfp(label: str, section: str, prev_std: str, has_dollar: bool) -> str:
    l = label.lower()
    if not label:
        if prev_std == "accumulated_depreciation":
            return "fixed_assets_net"
        if section in ("fixed_assets",) and prev_std in ("other_asset",):
            return "fixed_assets_gross"
        if has_dollar:
            return "total_assets" if section in ("assets", "current_assets", "fixed_assets", "other_assets") \
                else "total_liabilities_and_net_assets"
        if prev_std in ("net_assets_with_donor_restrictions", "net_assets_without_donor_restrictions"):
            return "net_assets_total"
        return "unlabeled"
    rules = [
        (r"^cash and cash equivalents", "cash"), (r"^restricted cash", "restricted_cash"),
        (r"pledges receivable", "pledges_receivable"), (r"grants receivable", "grants_receivable"),
        (r"^total current assets", "total_current_assets"),
        (r"accumulated depreciation", "accumulated_depreciation"),
        (r"^(net fixed assets|property and equipment, net)", "fixed_assets_net"),
        (r"^property and equipment, at cost", "fixed_assets_gross"),
        (r"^total other assets", "total_other_assets"),
        (r"^total assets", "total_assets"),
        (r"^total current liabilities", "total_current_liabilities"),
        (r"^total (non-current|other|long-term) liabilities", "total_noncurrent_liabilities"),
        (r"^total liabilities and net assets", "total_liabilities_and_net_assets"),
        (r"^total liabilities$", "total_liabilities"),
        (r"^(unrestricted|without donor restrictions)", "net_assets_without_donor_restrictions"),
        (r"^(temporarily restricted|with donor restrictions)", "net_assets_with_donor_restrictions"),
        (r"^total net assets", "net_assets_total"),
        (r"long-term debt|mortgage payable|loans payable", "debt"),
    ]
    for pat, std in rules:
        if re.search(pat, l):
            return std
    if section in ("current_assets",):
        return "other_current_asset"
    if section in ("assets", "fixed_assets", "other_assets"):
        return "other_asset"
    if section in ("liabilities", "current_liabilities", "noncurrent_liabilities"):
        return "other_liability"
    return "unmapped"


def parse_statement(pdf: Path, page: int, statement: str, cols: list) -> tuple[list[dict], list[str]]:
    lines = layout_page(pdf, page).splitlines()
    out, warn = [], []
    section, pending, prev_std, unl_ctx = "", "", "", ""
    for raw in lines:
        if not raw.strip() or SKIP_LINE.search(raw.strip()):
            continue
        label, nums = split_amounts(raw)
        has_dollar = "$" in raw
        if not nums:
            heading = None
            for pat, sec in HEADING_SECTIONS:
                if re.search(pat, label, re.I):
                    heading = (sec,)
                    break
            if heading:
                if heading[0]:
                    section = heading[0]
                # a heading followed by dot leaders is a line item whose amounts sit on the next line
                pending = label if re.search(r"[.…]{4,}", raw) else ""
            else:
                pending = (pending + " " + label).strip() if pending else label
            continue
        # attach a pending label: wrapped label ("Contributed services and" / "materials ...") or leader line
        if pending and (not label or label[:1].islower()):
            label = (pending + " " + label).strip()
        elif pending and label:
            # pending was a heading-like line without numbers we did not recognise; keep as section hint
            pass
        pending = ""
        if len(nums) != len(cols):
            if len(nums) < len(cols) and label == "" and len(nums) == 1:
                continue  # stray page number
            warn.append(f"{pdf.name} p{page} {statement}: '{label}' has {len(nums)} amounts, expected {len(cols)}")
            continue
        if statement == "SOA":
            if label and re.search(r"net assets released", label, re.I):
                unl_ctx = "after_releases"
            elif label and section in ("revenue", "") and not re.search(r"^total", label, re.I):
                unl_ctx = "before_releases"
            elif label and re.search(r"^fundraising$", label, re.I):
                unl_ctx = "after_expenses"
            std = std_soa(label, section, unl_ctx)
            if not label and unl_ctx == "before_releases":
                unl_ctx = "subtotal_done"
            if re.search(r"^EXPENSES", label):
                section = "expenses"
        else:
            std = std_sfp(label, section, prev_std, has_dollar)
        if std in ("unlabeled", "unmapped"):
            warn.append(f"{pdf.name} p{page} {statement}: unmapped line '{label}'")
        for (fy, cls, prior), tok in zip(cols, nums):
            v = to_num(tok)
            out.append(dict(page=page, fiscal_year=fy, tax_year=fy - 1, statement=statement,
                            line_item=label or f"(unlabeled subtotal after '{prev_label_txt(out)}')",
                            line_item_std=std, net_asset_class=cls, amount=fmt(v),
                            is_prior_year_comparative=prior, notes="" if label else "unlabeled printed subtotal"))
        prev_std = std
        if statement == "SOA" and std == "exp_total":
            section = "after_expenses"
        if statement == "SOA" and section == "revenue" and std == "rev_total":
            section = "expenses"
    return out, warn


def prev_label_txt(rows):
    for r in reversed(rows):
        if not r["line_item"].startswith("(unlabeled"):
            return r["line_item"]
    return ""


def extract_audits(inv) -> tuple[list[dict], list[str]]:
    rows, warns = [], []
    for fname, stmts in AUDITS.items():
        pdf = INPUTS / fname
        sid = sid_for(inv, fname)
        for page, st, cols in stmts:
            got, w = parse_statement(pdf, page, st, cols)
            warns += w
            for r in got:
                r.update(source_id=sid, document=fname)
            rows += got
        # derived total liabilities where the SFP does not print one
        sfp = [r for r in rows if r["document"] == fname and r["statement"] == "SFP"]
        for fy in sorted({r["fiscal_year"] for r in sfp}):
            yr = [r for r in sfp if r["fiscal_year"] == fy]
            stds = {r["line_item_std"] for r in yr}
            if "total_liabilities" not in stds:
                def g(s):
                    return sum(float(r["amount"]) for r in yr if r["line_item_std"] == s and r["amount"] != "")
                if "total_noncurrent_liabilities" in stds:
                    v = g("total_current_liabilities") + g("total_noncurrent_liabilities")
                    basis = "total current liabilities + total non-current liabilities"
                else:
                    v = g("total_current_liabilities") + g("debt") * 0
                    lt = [r for r in yr if r["line_item_std"] == "debt" and "net of current" in r["line_item"].lower()]
                    v += sum(float(r["amount"]) for r in lt)
                    basis = "total current liabilities + long-term debt"
                rows.append(dict(source_id=sid, document=fname, page=yr[0]["page"], fiscal_year=fy, tax_year=fy - 1,
                                 statement="SFP", line_item="(derived) Total liabilities",
                                 line_item_std="total_liabilities", net_asset_class=NA, amount=fmt(v),
                                 is_prior_year_comparative=yr[0]["is_prior_year_comparative"],
                                 notes=f"derived: not printed; {basis}"))
    return rows, warns


def tieouts(rows) -> list[dict]:
    """Check printed totals against component lines, per document x fiscal year x column class."""
    checks = []
    key = lambda r: (r["document"], r["source_id"], r["fiscal_year"], r["statement"], r["net_asset_class"])
    groups = defaultdict(list)
    for r in rows:
        groups[key(r)].append(r)

    def add(k, check, comp, printed, note=""):
        doc, sid, fy, st, cls = k
        diff = None if printed is None or comp is None else round(comp - printed, 2)
        checks.append(dict(source_id=sid, document=doc, fiscal_year=fy, statement=st, net_asset_class=cls,
                           check=check, components_sum=fmt(comp), printed_total=fmt(printed),
                           difference=fmt(diff), result="n/a" if diff is None else ("tie" if abs(diff) < 1.5 else "NO TIE"),
                           notes=note))

    for k, rs in sorted(groups.items(), key=lambda kv: tuple(str(x) for x in kv[0])):
        st = k[3]

        def vals(std):
            return [float(r["amount"]) for r in rs if r["line_item_std"] == std and r["amount"] != ""]

        def one(std):
            v = vals(std)
            return v[-1] if v else None
        if st == "SOA":
            rev_std = [s for s in {r["line_item_std"] for r in rs} if s.startswith("rev_")
                       and s not in ("rev_total", "rev_total_before_releases")]
            comp = sum(sum(vals(s)) for s in rev_std)
            add(k, "revenue lines sum to total revenue", comp, one("rev_total"))
            pt = one("exp_program_total")
            det = vals("exp_program_detail")
            if det:
                add(k, "program lines sum to total program services", sum(det), pt)
            comp = (pt or 0) + (one("exp_mgmt_general") or 0) + (one("exp_fundraising") or 0)
            add(k, "program + M&G + fundraising = total expenses", comp, one("exp_total"))
            if one("rev_total") is not None and one("exp_total") is not None:
                add(k, "total revenue - total expenses = change in net assets",
                    one("rev_total") - one("exp_total"), one("change_in_net_assets"))
            if one("net_assets_beginning") is not None:
                add(k, "beginning net assets + change = ending net assets",
                    one("net_assets_beginning") + (one("change_in_net_assets") or 0), one("net_assets_end"))
        else:
            ta, tl, tna = one("total_assets"), one("total_liabilities"), one("net_assets_total")
            if tl is not None and tna is not None:
                derived = any(r["line_item"].startswith("(derived)") for r in rs)
                add(k, "total liabilities + net assets = total assets", tl + tna, ta,
                    "total liabilities derived" if derived else "")
            w_, r_ = one("net_assets_without_donor_restrictions"), one("net_assets_with_donor_restrictions")
            if w_ is not None and r_ is not None:
                add(k, "net assets without + with restrictions = total net assets", w_ + r_, tna)
            if one("total_liabilities_and_net_assets") is not None:
                add(k, "total assets = total liabilities and net assets", ta, one("total_liabilities_and_net_assets"))
    return checks


# ---------------------------------------------------------------- 3. SEFA
SEFA_DOCS = {"Calvary-Womens-Services-Inc.-9.30.23-FS.pdf": (31, 2023)}


def find_sefa_pages(pdf: Path) -> list[int]:
    hits = []
    with pdfplumber.open(pdf) as doc:
        for i, p in enumerate(doc.pages, 1):
            t = p.extract_text() or ""
            if re.search(r"SCHEDULE OF EXPENDITURES OF FEDERAL AWARDS", t) and re.search(r"Assistance|CFDA", t) \
                    and re.search(r"TOTAL EXPENDITURES OF FEDERAL AWARDS", t, re.I):
                hits.append(i)
    return hits


def extract_sefa(inv) -> tuple[list[dict], list[str]]:
    rows, notes = [], []
    for fname in AUDITS:
        pdf = INPUTS / fname
        pages = find_sefa_pages(pdf)
        if fname not in SEFA_DOCS:
            notes.append(f"{fname}: SEFA {'FOUND (unexpected) on ' + str(pages) if pages else 'none'}")
            continue
        page, fy = SEFA_DOCS[fname]
        if page not in pages:
            notes.append(f"{fname}: expected SEFA on p{page}, detector found {pages}")
        agency = passthru = ""
        lines = layout_page(pdf, page).splitlines()
        i = 0
        while i < len(lines):
            s = re.sub(r"\s+", " ", lines[i]).strip()
            i += 1
            if not s:
                continue
            if re.match(r"^(U\.S\.|United States) Department", s) or re.match(r"^U\.S\. ", s):
                agency, passthru = s, ""
                continue
            m = re.match(r"^Pass-?through from (.+)$", s, re.I)
            if m:
                passthru = m.group(1).strip()
                continue
            if re.match(r"^(Total|TOTAL)", s):
                continue
            m = re.match(r"^(.+?)\s+(\d{2}\.\d{3})\s*(.*?)\s*\$?\s*([\d,]+)$", s)
            if m and agency:
                prog, aln, rest, amt = m.groups()
                rows.append(dict(source_id=sid_for(inv, fname), document=fname, page=page, fiscal_year=fy,
                                 federal_agency=agency, pass_through_entity=passthru, program_name=prog.strip(),
                                 assistance_listing=aln, pass_through_award_id=rest.strip(),
                                 amount=fmt(to_num(amt)), amount_to_subrecipients="",
                                 notes="no subrecipient column in SEFA; pass-through as printed"))
        tot = re.search(r"TOTAL EXPENDITURES OF FEDERAL AWARDS\s+\$?\s*([\d,]+)", layout_page(pdf, page))
        if tot:
            s = sum(float(r["amount"]) for r in rows if r["document"] == fname)
            notes.append(f"{fname}: SEFA {len(rows)} programs sum {s:,.0f} vs printed total {tot.group(1)}")
    return rows, notes


# ---------------------------------------------------------------- 4. Form 990 PDFs
F990 = {  # filename -> tax year (verified against inventory)
    "2015-Form-990-Calvary-Women_s-Services.pdf": 2014,
    "2016-Form-990-Calvary-Women_s-Services.pdf": 2015,
    "Calvary-Womens-Service-2018-990.pdf": 2017,
    "2019-990-Form-990-CWS.pdf": 2018,
    "2020-Form-990-CWS.pdf": 2019,
    "Calvary Womens Services Inc - Full Filing - Nonprofit Explorer - ProPublica.pdf": 2024,
}
PART1 = [  # (line, label regex, n values)
    ("3", r"Number of voting members of the governing body", 1),
    ("4", r"Number of independent voting members", 1),
    ("5", r"Total number of individuals employed", 1),
    ("6", r"Total number of volunteers", 1),
    ("8", r"Contributions and grants \(Part VIII", 2),
    ("9", r"Program service revenue \(Part VIII", 2),
    ("10", r"Investment income \(Part VIII", 2),
    ("11", r"Other revenue \(Part VIII", 2),
    ("12", r"Total revenue\s*[-—–]+\s*add lines 8 through 11", 2),
    ("13", r"Grants and similar amounts paid", 2),
    ("14", r"Benefits paid to or for members", 2),
    ("15", r"Salaries, other compensation, employee benefits", 2),
    ("16a", r"Professional fundraising fees", 2),
    ("16b", r"Total fundraising expenses \(Part IX", 1),
    ("17", r"Other expenses \(Part IX", 2),
    ("18", r"Total expenses\. Add lines 13", 2),
    ("19", r"Revenue less expenses\. Subtract line 18", 2),
    ("20", r"Total assets \(Part X", 2),
    ("21", r"Total liabilities \(Part X", 2),
    ("22", r"Net assets or fund balances\. Subtract", 2),
]
PART8 = [  # ordered anchors on the Part VIII token stream: (line, regex)
    ("1a", r"Federated campaigns"), ("1b", r"Membership dues"), ("1c", r"Fundraising events"),
    ("1d", r"Related organizations"), ("1e", r"Government grants \(contributions\)"),
    ("1f", r"All other contributions"), ("1g", r"Noncash contributions included"),
    ("1h", r"Total\.? Add lines 1a ?- ?1f"), ("2_hdr", r"Business Code"), ("2f", r"All other program service revenue"),
    ("2g", r"Total\.? Add lines 2a ?[-–] ?2f"), ("3", r"Investment income \(including dividends"),
    ("4", r"Income from investment of tax-exempt bond"), ("5", r"Royalties"), ("6a", r"Gross rents"),
    ("6b", r"Less: rental"), ("6c", r"Rental income or"), ("6d", r"Net rental income or \(loss\)"),
    ("7a", r"Gross amount"), ("7b", r"Less: cost or"), ("7c", r"(?<!Net )Gain or \(loss\)"),
    ("7d", r"Net gain or \(loss\)"), ("8a", r"Gross income from fundraising events"),
    ("8b", r"Less: direct expenses"), ("8c", r"Net income or \(loss\) from fundraising events"),
    ("9a", r"Gross income from gaming"), ("9b", r"Less: direct expenses"),
    ("9c", r"Net income or \(loss\) from gaming"), ("10a", r"Gross sales of inventory"),
    ("10b", r"Less: cost of goods sold"), ("10c", r"Net income or \(loss\) from sales of inventory"),
    ("11_hdr", r"Business Code"), ("11d", r"All other revenue"), ("11e", r"Total\.? Add lines 11a ?[-–] ?11d"),
    ("12", r"Total revenue\.? See instructions"),
]
P8_KEEP = {"1a", "1b", "1c", "1d", "1e", "1f", "1g", "1h", "2g", "3", "4", "5", "6d", "7d", "8a", "8b", "8c", "9c",
           "10c", "11e", "12"}
P8_LABEL = {"1a": "Federated campaigns", "1b": "Membership dues", "1c": "Fundraising events",
            "1d": "Related organizations", "1e": "Government grants (contributions)",
            "1f": "All other contributions, gifts, grants", "1g": "Noncash contributions included in 1a-1f",
            "1h": "Total contributions (1a-1f)", "2g": "Total program service revenue", "3": "Investment income",
            "4": "Income from tax-exempt bond proceeds", "5": "Royalties", "6d": "Net rental income",
            "7d": "Net gain or (loss) from sales of assets", "8a": "Gross income from fundraising events",
            "8b": "Fundraising events direct expenses", "8c": "Net income from fundraising events",
            "9c": "Net income from gaming", "10c": "Net income from sales of inventory",
            "11e": "Total miscellaneous revenue", "12": "Total revenue"}
STRIP_PHRASES = [r"Part IV,? line \d+", r"lines? 1a ?[-–] ?1f:?", r"lines? 2a ?[-–] ?2f", r"lines? 11a ?[-–] ?11d",
                 r"line 1c", r"512 ?- ?514", r"lines 3, 4, and 7d", r"Form 990 \(\d{4}\)", r"Page \d+",
                 r"\b\d{6} \d{2}-\d{2}-\d{2}\b", r"\b\d{8} \d{6} \d{5}(\.\d{3})?\b", r"\b\d{4}\.\d{5}\b",
                 r"Cat\. No\. \w+", r"\(i\)|\(ii\)", r"\b(?:[A-D])\b(?= \()"]
PART10 = [  # (label regex, std)
    (r"Cash\s*[-—–]+\s*non-interest-bearing", "cash_non_interest_bearing"),
    (r"Savings and temporary cash investments", "savings_temp_cash"),
    (r"Pledges and grants receivable, net", "pledges_grants_receivable"),
    (r"Less: accumulated depreciation", "land_buildings_equipment_net"),
    (r"Total assets\. Add lines 1 through 15", "total_assets"),
    (r"Accounts payable and accrued expenses", "accounts_payable_accrued"),
    (r"Secured mortgages and notes payable", "secured_mortgages_notes"),
    (r"Total liabilities\. Add lines 17 through 25", "total_liabilities"),
    (r"(Net assets without donor restrictions|Unrestricted net assets)", "net_assets_without_donor_restrictions"),
    (r"(Net assets with donor restrictions|Temporarily restricted net assets)", "net_assets_with_donor_restrictions"),
    (r"Permanently restricted net assets", "net_assets_permanently_restricted"),
    (r"Total net assets or fund balances", "net_assets_total"),
    (r"Total liabilities and net assets/fund balances", "total_liabilities_and_net_assets"),
]


def squeeze(s: str) -> str:
    s = re.sub(r"(?:\s*[.~•·]){3,}", " ", s)  # dot / tilde leaders
    return re.sub(r"\s+", " ", s).strip()


def find_pages(texts: list[str], pattern: str) -> list[int]:
    return [i for i, t in enumerate(texts, 1) if re.search(pattern, t)]


def trailing_amounts(s: str, n: int) -> list[str]:
    toks = s.replace("|", " ").split()
    out = []
    while toks and len(out) < n:
        t = toks.pop()
        if t == "$":
            continue
        if AMT.match(t):
            out.insert(0, t)
        else:
            break
    return out


def token_stream(pdf_path: Path, pages: list[int]) -> str:
    """Upright words ordered by visual row then x, joined into one string (rows separated by ' ¶ ')."""
    parts = []
    with pdfplumber.open(pdf_path) as doc:
        for pg in pages:
            ws = [w for w in doc.pages[pg - 1].extract_words(x_tolerance=1.5, y_tolerance=2, extra_attrs=["upright"])
                  if w["upright"]]
            for row in cluster_rows(ws):
                parts.append(" ".join(w["text"] for w in row))
    return " ¶ ".join(parts)


def cluster_rows(ws, tol=3.5):
    ws = sorted(ws, key=lambda w: (w["top"] + w["bottom"]) / 2)
    rows, cur, cy = [], [], None
    for w in ws:
        c = (w["top"] + w["bottom"]) / 2
        if cy is None or abs(c - cy) <= tol:
            cur.append(w)
            cy = c if cy is None else (cy * (len(cur) - 1) + c) / len(cur)
        else:
            rows.append(sorted(cur, key=lambda w: w["x0"]))
            cur, cy = [w], c
    if cur:
        rows.append(sorted(cur, key=lambda w: w["x0"]))
    return rows


def part8_values(stream: str) -> tuple[dict, list[str]]:
    s = re.sub(r"(?:\s*[.~•·]){3,}", " ", stream)
    warn = []
    pos, hits = 0, []
    for code, pat in PART8:
        m = re.compile(pat, re.I).search(s, pos)
        if not m:
            warn.append(f"anchor {code} not found")
            continue
        hits.append((code, m.start(), m.end()))
        pos = m.end()
    vals = {}
    for i, (code, st, en) in enumerate(hits):
        seg = s[en: hits[i + 1][1] if i + 1 < len(hits) else len(s)]
        for pat in STRIP_PHRASES:
            seg = re.sub(pat, " ", seg)
        if i + 1 < len(hits):  # the next line's printed line number ("3", "6 a", "11 a") sits before its label
            num = re.match(r"\d+", hits[i + 1][0])
            if num:
                seg = re.sub(rf"(?:^|\s){num.group(0)}\s*[a-h]?[\s¶]*$", " ", seg)
        note = ""
        if code == "8a":
            m = re.search(r"including \$\s*([-\d,.]+)\s*of", seg)
            if m:
                note = f"includes-$ note {m.group(1)} (contributions reported on 1c) skipped"
                seg = seg[:m.start()] + " " + seg[m.end():]
        seg = re.sub(rf"(?<!\S){re.escape(code)}(?!\S)", " ", seg)  # box code token
        amts = [t for t in seg.replace("|", " ").replace("$", " ").split()
                if AMT.match(t) and not re.fullmatch(r"(19|20)\d\d", t)]
        if code in P8_KEEP:
            vals[code] = (amts, note)
    return vals, warn


def part10_line(lines: list[str], label: str):
    for ln in lines:
        s = squeeze(ln)
        m = re.search(rf"(?<!\S)(\d{{1,2}}[a-c]?)?\s*(?:b\s+)?{label}", s, re.I)
        if not m:
            continue
        rest = s[m.end():].replace("|", " ").split()
        code = None
        # the box code printed between beginning-of-year and end-of-year columns
        for j, t in enumerate(rest):
            if re.fullmatch(r"\d{1,2}[a-c]?", t) and not (AMT.match(t) and j + 1 >= len(rest)):
                if j + 1 < len(rest) and AMT.match(rest[j + 1]):
                    code = j
        boy = eoy = None
        if code is not None:
            before = [t for t in rest[:code] if AMT.match(t)]
            after = [t for t in rest[code + 1:] if AMT.match(t)]
            boy = before[-1] if before else None
            eoy = after[0] if after else None
        else:
            am = [t for t in rest if AMT.match(t)]
            if len(am) >= 2:
                boy, eoy = am[-2], am[-1]
        return (m.group(1) or ""), boy, eoy
    return None


def extract_990(inv) -> tuple[list[dict], list[str]]:
    rows, warns = [], []
    for fname, ty in F990.items():
        pdf = INPUTS / fname
        sid = sid_for(inv, fname)
        if int(inv[fname]["tax_year"]) != ty:
            warns.append(f"{fname}: inventory tax_year {inv[fname]['tax_year']} != {ty}")
        n = int(inv[fname]["pages"])
        texts = [layout_page(pdf, i) for i in range(1, n + 1)]

        def add(part, line, label, col, val, page, note=""):
            rows.append(dict(source_id=sid, document=fname, page=page, tax_year=ty, fiscal_year=ty + 1, part=part,
                             line=line, line_label=label, column=col, amount=fmt(to_num(val)) if val else "",
                             notes=note))
        # Part I
        p1 = [p for p in find_pages(texts, r"Part I\s+Summary") if re.search(r"Total revenue", texts[p - 1])]
        if not p1:
            warns.append(f"{fname}: Part I not in text layer (page 1 scanned)")
        else:
            pg = p1[0]
            lines = [squeeze(l) for l in texts[pg - 1].splitlines()]
            for code, pat, k in PART1:
                hit = next((l for l in lines if re.search(pat, l, re.I)), None)
                if not hit:
                    warns.append(f"{fname}: Part I line {code} not found")
                    continue
                am = trailing_amounts(hit, k)
                lab = re.search(pat, hit, re.I).group(0)
                if k == 1:
                    add("I", code, lab, "current_year", am[-1] if am else "", pg)
                else:
                    cols = ("beginning_of_year", "end_of_year") if code in ("20", "21", "22") else ("prior_year", "current_year")
                    if len(am) == 2:
                        add("I", code, lab, cols[0], am[0], pg)
                        add("I", code, lab, cols[1], am[1], pg)
                    else:
                        warns.append(f"{fname}: Part I line {code} got {am}")
        # Part VIII
        p8 = [p for p in find_pages(texts, r"Part VIII\s+Statement of Revenue")]
        if p8:
            pages = [p8[0]] + ([p8[0] + 1] if not re.search(r"Total revenue\.?\s+See instructions", texts[p8[0] - 1])
                               else [])
            vals, w = part8_values(token_stream(pdf, pages))
            warns += [f"{fname} Part VIII: {x}" for x in w]
            for code, (amts, note) in vals.items():
                if not amts:
                    continue
                if code == "12":
                    for col, v in zip(["A_total", "B_related_exempt", "C_unrelated_business", "D_excluded"], amts[:4]):
                        add("VIII", code, P8_LABEL[code], col, v, pages[0], note)
                else:
                    add("VIII", code, P8_LABEL[code], "A_total" if code not in ("1a", "1b", "1c", "1d", "1e", "1f",
                                                                                "1g", "8a", "8b") else "inner_box",
                        amts[0], pages[0], note)
        # Part IX line 25
        p9 = find_pages(texts, r"Part IX\s+Statement of Functional Expenses")[:1]
        for pg in (p9 + [p9[0] + 1] if p9 else []):
            for l in texts[pg - 1].splitlines():
                s = squeeze(l)
                if re.search(r"Total functional expenses\. Add lines 1 through 24e", s):
                    am = trailing_amounts(s, 4)
                    for col, v in zip(["A_total", "B_program", "C_mgmt_general", "D_fundraising"], am):
                        add("IX", "25", "Total functional expenses", col, v, pg)
        # Part X
        p10 = find_pages(texts, r"Part X\s+Balance Sheet")
        if p10:
            lines = texts[p10[0] - 1].splitlines()
            lines = lines[next(i for i, l in enumerate(lines) if re.search(r"Part X\s+Balance Sheet", l)):]
            lines += texts[p10[0]].splitlines()  # TY2024 render continues Part X on the next PDF page
            for pat, std in PART10:
                got = part10_line(lines, pat)
                if not got:
                    continue
                code, boy, eoy = got
                if not boy and not eoy:
                    continue
                code = "10c" if std == "land_buildings_equipment_net" else (code or std)
                add("X", code, std, "beginning_of_year", boy, p10[0])
                add("X", code, std, "end_of_year", eoy, p10[0])
    return rows, warns


def check_990(rows) -> list[dict]:
    """Internal 990 ties: Part VIII 1a-1f = 1h; Part VIII line 12 components; Part I 8/12/18 vs VIII/IX."""
    out = []
    by = defaultdict(dict)
    for r in rows:
        if r["amount"] != "":
            by[(r["document"], r["source_id"], r["tax_year"])][(r["part"], r["line"], r["column"])] = float(r["amount"])
    for (doc, sid, ty), d in sorted(by.items(), key=lambda kv: kv[0][2]):
        def g(part, line, col):
            return d.get((part, line, col), 0.0)

        def add(check, comp, printed):
            diff = round(comp - printed, 2)
            out.append(dict(source_id=sid, document=doc, fiscal_year=ty + 1, statement=f"990 TY{ty}",
                            net_asset_class="", check=check, components_sum=fmt(comp), printed_total=fmt(printed),
                            difference=fmt(diff), result="tie" if abs(diff) < 1.5 else "NO TIE", notes=""))
        add("Part VIII 1a-1f = 1h", sum(g("VIII", c, "inner_box") for c in ("1a", "1b", "1c", "1d", "1e", "1f")),
            g("VIII", "1h", "A_total"))
        comp = sum(g("VIII", c, "A_total") for c in ("1h", "2g", "3", "4", "5", "6d", "7d", "8c", "9c", "10c", "11e"))
        add("Part VIII line 12 = 1h+2g+3+4+5+6d+7d+8c+9c+10c+11e", comp, g("VIII", "12", "A_total"))
        add("Part VIII 8a - 8b = 8c", g("VIII", "8a", "inner_box") - g("VIII", "8b", "inner_box"),
            g("VIII", "8c", "A_total"))
        if ("I", "12", "current_year") in d:
            add("Part I line 12 = Part VIII line 12", g("I", "12", "current_year"), g("VIII", "12", "A_total"))
            add("Part I line 8 = Part VIII 1h", g("I", "8", "current_year"), g("VIII", "1h", "A_total"))
            add("Part I line 18 = Part IX line 25(A)", g("I", "18", "current_year"), g("IX", "25", "A_total"))
            add("Part I line 20 EOY = Part X total assets EOY", g("I", "20", "end_of_year"),
                g("X", "16", "end_of_year"))
        add("Part IX 25: B + C + D = A", g("IX", "25", "B_program") + g("IX", "25", "C_mgmt_general")
            + g("IX", "25", "D_fundraising"), g("IX", "25", "A_total"))
    return out


# ---------------------------------------------------------------- 5. Part VII-A people
ROLE_ORDER = ["individual_trustee_or_director", "institutional_trustee", "officer", "key_employee",
              "highest_compensated_employee", "former"]
ROLE_KEYS = [("Individual", ROLE_ORDER[0]), ("Institutional", ROLE_ORDER[1]), ("Officer", ROLE_ORDER[2]),
             ("Keyemployee", ROLE_ORDER[3]), ("Highest", ROLE_ORDER[4]), ("Former", ROLE_ORDER[5])]
ROW_JUNK = re.compile(r"Form 990|Page \d|Part VII|Section A|CALVARY WOMEN|52-1307706|Name and title|Average|"
                      r"Sub-?total|Subtotal|\(A\)|LHA|^\d{6}\b|\d{8} \d{6}")


def role_bands(page) -> list[tuple[float, float, str]]:
    """Column x-ranges for Part VII position checkboxes: rotated header text (CCH) or header images (render)."""
    groups = defaultdict(list)
    for c in page.chars:
        if not c.get("upright", True):
            groups[round(c["x0"])].append(c)
    bands = []
    for x, cs in sorted(groups.items()):
        txt = "".join(c["text"] for c in sorted(cs, key=lambda c: -c["top"])).replace(" ", "")
        for key, role in ROLE_KEYS:
            if txt.startswith(key) or (key == "Keyemployee" and txt.startswith("Key")):
                bands.append((x - 3, x + 9, role))
                break
    # CCH splits two-line headers ("Highest compensated / employee") into two rotated runs; keep first per role
    seen, out = set(), []
    for b in bands:
        if b[2] not in seen:
            seen.add(b[2])
            out.append(b)
    if len(out) >= 4:
        return out
    imgs = sorted([im for im in page.images if im["height"] > 20 and im["width"] < 25 and 240 < im["x0"] < 380],
                  key=lambda im: im["x0"])
    if len(imgs) == 6:
        return [(im["x0"] - 1, im["x1"] + 1, role) for im, role in zip(imgs, ROLE_ORDER)]
    return []


def extract_part7(inv) -> tuple[list[dict], list[str]]:
    rows, warns = [], []
    for fname, ty in F990.items():
        pdf = INPUTS / fname
        n = int(inv[fname]["pages"])
        texts = [layout_page(pdf, i) for i in range(1, n + 1)]
        pages = [i for i in find_pages(texts, r"Part VII\s+(Compensation of Officers|Section A)")
                 if re.search(r"\(1\)|\(\d+\)\s+[A-Z]", texts[i - 1]) or re.search(r"Section A", texts[i - 1])]
        pages = [p for p in pages if p < n * 0.5]  # main form only
        if pages:
            pages = list(range(pages[0], pages[-1] + 2))  # render splits pages; include one spill page
        with pdfplumber.open(pdf) as doc:
            tokens, bands = [], []
            for pg in pages:
                page = doc.pages[pg - 1]
                b = role_bands(page)
                bands = b or bands
                ws = [w for w in page.extract_words(x_tolerance=1.5, y_tolerance=2, extra_attrs=["upright"])
                      if w["upright"]]
                for row in cluster_rows(ws):
                    txt = " ".join(w["text"] for w in row)
                    tokens.append((pg, row, txt, bands))
                    if re.search(r"1b\s+Sub-?total|Sub-?Total", txt):
                        break
                else:
                    continue
                break
        people, cur = [], None
        for pg, row, txt, bands in tokens:
            if re.search(r"Sub-?total|Sub-?Total", txt):
                break
            if re.match(r"^\(\d+\)$", row[0]["text"]) and row[0]["x0"] < 80:
                cur = dict(page=pg, n=int(row[0]["text"].strip("()")), name_row=row[1:], rows=[], bands=bands)
                people.append(cur)
                continue
            if cur is not None:
                cur["rows"].append(row)
        for p in people:
            bands = p["bands"]
            bmin = min(b[0] for b in bands) if bands else 250
            bmax = max(b[1] for b in bands) if bands else 360
            allw = p["name_row"] + [w for r in p["rows"] for w in r]
            hours = next((w["text"] for w in allw if re.fullmatch(r"\d{1,2}\.\d{2}", w["text"])), "")
            name = " ".join(w["text"] for w in p["name_row"] if w["x1"] < bmin and not re.fullmatch(r"[\d.]+", w["text"]))
            title_rows = []
            for r in p["rows"]:
                txt = " ".join(w["text"] for w in r if w["x1"] < bmin and not re.fullmatch(r"\.+", w["text"]))
                if not txt or ROW_JUNK.search(" ".join(w["text"] for w in r)) or re.search(r"[a-z]", txt):
                    continue
                if re.fullmatch(r"[\d.,\s]+", txt):
                    continue
                title_rows.append(txt)
            title = " ".join(t for i, t in enumerate(title_rows) if i == 0 or t != title_rows[i - 1])
            flags = []
            for w in allw:
                if w["text"] == "X" and bmin - 3 <= (w["x0"] + w["x1"]) / 2 <= bmax + 3:
                    cx = (w["x0"] + w["x1"]) / 2
                    best = min(bands, key=lambda b: 0 if b[0] <= cx <= b[1] else min(abs(cx - b[0]), abs(cx - b[1])))
                    if best[2] not in flags:
                        flags.append(best[2])
            amts = sorted([w for w in allw if w["x0"] > bmax + 5 and AMT.match(w["text"])
                           and not re.fullmatch(r"\d{1,2}\.\d{2}", w["text"])], key=lambda w: w["x0"])
            comp = fmt(to_num(amts[0]["text"])) if amts else ""
            if not name or not flags:
                warns.append(f"{fname} ({p['n']}): name='{name}' flags={flags}")
            rows.append(dict(source_id=sid_for(inv, fname), tax_year=ty, name=name, title=title, avg_hours=hours,
                             role_flags=";".join(sorted(flags, key=ROLE_ORDER.index)), reportable_comp=comp,
                             document=fname, page=p["page"], line_no=p["n"]))
        if not people:
            warns.append(f"{fname}: no Part VII rows found")
    return rows, warns


# ---------------------------------------------------------------- 6. Schedule I (TY2024 render)
def extract_schedule_i(inv) -> list[dict]:
    fname = "Calvary Womens Services Inc - Full Filing - Nonprofit Explorer - ProPublica.pdf"
    pdf = INPUTS / fname
    out = []
    with pdfplumber.open(pdf) as doc:
        for i, page in enumerate(doc.pages, 1):
            t = page.extract_text() or ""
            if not re.search(r"Part III\s+Grants and Other Assistance to Domestic Individuals", t):
                continue
            ws = page.extract_words(x_tolerance=1.5, y_tolerance=2)
            p3 = [w for w in ws if w["text"] == "III"]
            top3 = p3[0]["top"] if p3 else 0
            ws = [w for w in ws if w["top"] >= top3 - 2]
            hdr = {}
            for w in ws:
                if w["text"] in ("(b)", "(c)", "(d)", "(e)", "(f)") and w["text"] not in hdr:
                    hdr[w["text"]] = w["x0"]
            rows = cluster_rows(ws)
            for j, r in enumerate(rows):
                if not re.fullmatch(r"\(\d+\)", r[0]["text"]) or len(r) < 3:
                    continue
                typ, nums, val, desc, desc_x = [], [], "", [], None
                for w in r[1:]:
                    t = w["text"]
                    if AMT.match(t) and not desc:
                        nums.append(w)
                    elif not nums:
                        typ.append(t)
                    elif not val and t.upper() in ("FMV", "BOOK", "COST", "APPRAISAL", "OTHER"):
                        val = t
                    else:
                        desc.append(t)
                        desc_x = w["x0"] if desc_x is None else desc_x
                if j + 1 < len(rows) and not re.fullmatch(r"\(\d+\)", rows[j + 1][0]["text"]):
                    for w in rows[j + 1]:
                        if "(b)" in hdr and w["x1"] < hdr["(b)"]:
                            typ.append(w["text"])
                        elif desc_x is not None and w["x0"] >= desc_x - 3:
                            desc.append(w["text"])
                if len(nums) < 2:
                    continue
                amt = nums[1]
                is_cash = "(d)" in hdr and amt["x0"] < hdr["(d)"] - 4
                out.append(dict(source_id=sid_for(inv, fname), document=fname, page=i, tax_year=2024,
                                schedule_part="III", type_of_assistance=" ".join(typ),
                                number_of_recipients=nums[0]["text"],
                                cash_grant=fmt(to_num(amt["text"])) if is_cash else "",
                                noncash_assistance="" if is_cash else fmt(to_num(amt["text"])),
                                valuation_method=val, noncash_description=" ".join(desc)))
    return out


# ---------------------------------------------------------------- 7. funders and donor bands
AR15 = "Calvary-Women_s-Services-FY2015-Annual-Report.pdf"
CFS = "Corporate & Foundation Support - Calvary Women's Services.pdf"
# FY15 donor list: (page, column crop bbox) in reading order
AR15_COLS = [(5, (620, 120, 785, 700)), (5, (785, 120, 935, 700)), (5, (935, 120, 1152, 700)),
             (6, (40, 30, 205, 700)), (6, (205, 30, 365, 700)), (6, (365, 30, 560, 700))]
# Names rendered only as logo images on the support page, read visually (see notes column).
CFS_LOGOS = {0: "Positive Change Project", 1: "Capital One", 2: "MGAC"}
CORP_FDN = re.compile(r"bank of america|wells fargo|walmart|tjx|mgm resorts|morrison & foerster|miller & chevalier|"
                      r"venable|gannett|bj.s|qlarant|td bank|baker botts|latham", re.I)
TYPE_OVERRIDES = {"international monetary fund": "intergovernmental",
                  "world bank community connections fund": "intergovernmental",
                  "dchfa": "government", "bipartisan policy center": "nonprofit",
                  "center for nonprofit advancement": "association", "positive change project": "unknown",
                  "omidyar network": "foundation", "nina mclemore": "corporation", "anonymous": "anonymous",
                  "battelle": "nonprofit", "bracewell": "corporation", "pepco": "corporation",
                  "edelman public relations": "corporation", "key": "corporation", "amazon": "corporation"}


def org_type(name: str, default: str) -> str:
    n = name.lower().replace("*", "").strip()
    if n in TYPE_OVERRIDES:
        return TYPE_OVERRIDES[n]
    if re.search(r"church|parish|catholic|lutheran|presbyterian|tzedakah|synagogue|congregation|ministr", n):
        return "congregation"
    if re.search(r"department|office of|government|federal emergency|housing and urban|district of columbia|"
                 r"agency|council", n):
        return "government"
    if re.search(r"foundation|\bfund\b|trust\b", n):
        return "corporate_foundation" if CORP_FDN.search(n) else "foundation"
    if re.search(r"united way|junior league|association|club\b|guild|chapter|\bcrew\b|league|collective", n):
        return "association"
    if re.search(r"\b(llp|l\.l\.p|llc|inc|corp|corporation|company|companies|group|l\.p|p\.l\.l\.c|bank|"
                 r"consult\w*|realty|studios?|hotels?|systems|partners|strategy|capital|toyota|program|cares|"
                 r"construction|science|services|relations)\b", n):
        return "corporation"
    return default


def band_bounds(raw: str):
    m = re.search(r"\$([\d,]+)\s*(?:and above|\+)", raw)
    if m:
        return int(m.group(1).replace(",", "")), ""
    m = re.search(r"\$([\d,]+)\s*(?:to|-|–)\s*\$?([\d,]+)", raw)
    if m:
        return int(m.group(1).replace(",", "")), int(m.group(2).replace(",", ""))
    return "", ""


def col_lines(page, bbox):
    """Text lines inside a column crop, with first-char font and top."""
    c = page.crop(bbox)
    out = []
    for l in c.extract_text_lines(return_chars=True, strip=True):
        if not l["text"].strip():
            continue
        out.append(dict(text=re.sub(r"\s+", " ", l["text"].replace("\xa0", " ")).strip(), top=l["top"],
                        x0=l["x0"], x1=l["x1"], font=l["chars"][0]["fontname"].split("+")[-1],
                        size=l["chars"][0]["size"]))
    return out


def extract_ar15_donors(inv):
    sid = sid_for(inv, AR15)
    funders, bands = [], defaultdict(int)
    section = band = ""
    with pdfplumber.open(INPUTS / AR15) as doc:
        entries = []  # (page, section, band, text)
        for pg, bbox in AR15_COLS:
            lines = col_lines(doc.pages[pg - 1], bbox)
            prev_top, prev_entry = None, None
            for l in lines:
                t, f = l["text"], l["font"]
                if f.endswith("Bold") and not f.endswith("BoldItalic"):
                    if re.match(r"Corporate partners|groups and other", t):
                        section = "Corporate partners, associations, faith groups and other organizations"
                    elif re.match(r"Individuals and families", t):
                        section = "Individuals and families"
                    prev_top = None
                    continue
                if f.endswith("BoldItalic") and t.startswith("$"):
                    band, prev_top = t, None
                    continue
                if not section or not band:
                    continue
                # wrapped entry: tighter leading (9.0pt) than between entries (10.7pt)
                if prev_entry is not None and prev_top is not None and l["top"] - prev_top < 10.0:
                    prev_entry[3] = prev_entry[3] + " " + t
                else:
                    prev_entry = [pg, section, band, t]
                    entries.append(prev_entry)
                prev_top = l["top"]
    for pg, sec, bnd, name in entries:
        lo, hi = band_bounds(bnd)
        if sec.startswith("Individuals"):
            bands[(bnd, lo, hi)] += 1
            continue
        funders.append(dict(source_id=sid, document=AR15, page=pg, report_year=2015, fiscal_year=2015,
                            funder_name_raw=name, funder_name_norm=norm_name(name),
                            org_type_guess=org_type(name, "unknown"), gift_band_raw=bnd, band_min=lo, band_max=hi,
                            in_kind_flag="", truncated=False, section_heading=sec,
                            notes="anonymous organizational donor" if name == "Anonymous" else ""))
    band_rows = [dict(source_id=sid, document=AR15, report_year=2015, gift_band_raw=b, band_min=lo, band_max=hi,
                      individual_count=n) for (b, lo, hi), n in bands.items()]
    return funders, band_rows, entries


def extract_support_page(inv):
    sid = sid_for(inv, CFS)
    rows, warns = [], []
    tiers = {"Empower", "Change", "Hope", "Support"}
    with pdfplumber.open(INPUTS / CFS) as doc:
        # page 1: left column (Empower + logos), right column (Change)
        p1 = doc.pages[0]
        logos = sorted([im for im in p1.images if im["x0"] < 300 and im["top"] > 440], key=lambda im: im["top"])
        layout = [(1, (85, 260, 305, 660), None), (1, (305, 260, 525, 660), None),
                  (2, (85, 20, 305, 490), None), (2, (305, 20, 520, 490), None), (2, (520, 20, 612, 490), "Support"),
                  (2, (85, 515, 305, 760), "Institutional Support"), (2, (305, 515, 525, 760), "Institutional Support")]
        clip_edge = max(c["x1"] for c in doc.pages[1].chars if c["x0"] > 520 and c["top"] < 490)
        for pg, bbox, fixed in layout:
            page = doc.pages[pg - 1]
            lines = col_lines(page, bbox)
            items = [(l["top"], l["text"], l["x1"]) for l in lines]
            if pg == 1 and bbox[0] < 100:
                items += [(im["top"], f"[logo {i}]", im["x1"]) for i, im in enumerate(logos)]
            items.sort()
            tier = fixed
            for top, text, x1 in items:
                if text in tiers and fixed is None:
                    tier = text
                    continue
                if not tier or (text.isupper() and (text in "INSTITUTIONAL SUPPORT CORPORATE PARTNERS PROGRAM"
                                                    or text == "LEARN MORE")):
                    continue  # section banners (letter-spaced caps); all-caps names such as KPMG LLP are kept
                note, trunc = "", False
                m = re.fullmatch(r"\[logo (\d)\]", text)
                if m:
                    text = CFS_LOGOS.get(int(m.group(1)), f"unidentified logo {m.group(1)}")
                    note = "name shown only as a logo image; transcribed visually"
                if bbox[0] >= 520:
                    note = (note + "; " if note else "") + "third column of Support tier (alphabetical continuation)"
                    if x1 >= clip_edge - 7.5:  # a continuation would have shown at least one glyph otherwise
                        trunc = True
                        note += "; text runs to the clipped page edge, name likely cut (re-fetch live page)"
                sec = "Institutional Support" if tier == "Institutional Support" else f"Corporate Partners Program: {tier}"
                name = text.rstrip("*").strip()
                rows.append(dict(source_id=sid, document=CFS, page=pg, report_year=2023, fiscal_year="",
                                 funder_name_raw=text, funder_name_norm=norm_name(name),
                                 org_type_guess=org_type(name, "foundation" if tier == "Institutional Support"
                                                         else "corporation"),
                                 gift_band_raw=tier, band_min="", band_max="",
                                 in_kind_flag=text.endswith("*"), truncated=trunc, section_heading=sec,
                                 notes=(note + "; " if note else "") + "cumulative list 'over the years', current as of "
                                                                     "September 2023; no amounts"))
    return rows, warns


AUDIT_GRANTORS = [
    (r"Community Partnership", "The Community Partnership for the Prevention of Homelessness (TCP)", "nonprofit"),
    (r"Office of Victim Services and Justice Grants", "DC Office of Victim Services and Justice Grants (OVSJG)",
     "government"),
    (r"D\.C\. Government|U\.S\. and D\.C\. Governments", "District of Columbia Government", "government"),
    (r"U\.S\.? Department of Housing and Urban Development", "U.S. Department of Housing and Urban Development",
     "government"),
    (r"Federal Emergency Management Agency", "Federal Emergency Management Agency (FEMA)", "government"),
]


def extract_audit_grantors(inv):
    rows = []
    for fname in AUDITS:
        pdf = INPUTS / fname
        fy = int(inv[fname]["fiscal_year"])
        n = int(inv[fname]["pages"])
        for pat, name, typ in AUDIT_GRANTORS:
            for pg in range(1, n + 1):
                t = re.sub(r"\s+", " ", plain_text(pdf, pg, pg))
                m = re.search(pat, t)
                if not m:
                    continue
                ctx = t[max(0, m.start() - 160): m.end() + 200]
                heading = "audit note: government grants / grants receivable"
                note = "named in audit notes as a source of government grant funding"
                if fname in SEFA_DOCS and pg == SEFA_DOCS[fname][0]:
                    heading, note = "audit SEFA (federal agency or pass-through)", "named in SEFA; see sefa_federal_awards.csv"
                if re.search(r"subsequent|February 2022", ctx, re.I) and "3.3 million" in ctx:
                    note = "subsequent-events note: $3.3M multi-year grant for Sisters Rise received Feb 2022"
                    heading = "audit note: subsequent events"
                elif "receivable" in ctx.lower() and "amounts due" in ctx.lower():
                    heading = "audit note: grants receivable"
                rows.append(dict(source_id=sid_for(inv, fname), document=fname, page=pg, report_year=fy,
                                 fiscal_year=fy, funder_name_raw=m.group(0), funder_name_norm=norm_name(name),
                                 org_type_guess=typ, gift_band_raw="", band_min="", band_max="", in_kind_flag="",
                                 truncated=False, section_heading=heading, notes=f"{note}; canonical: {name}"))
                break
    return rows


# ---------------------------------------------------------------- 8. boards and leadership
# (filename, page, report_year, column crops, style). Styles say which font carries title vs affiliation.
BOARDS = [
    ("Calvary-Women_s-Services-FY2017-Annual-Report.pdf", 5, 2017, [(0, 80, 300, 560), (300, 80, 612, 560)], "fy17"),
    ("Calvary-Womens-Services-2020-Annual-Report.pdf", 2, 2020, [(600, 100, 792, 560)], "ar20"),
    ("Calvary-2021-AR-Working-C.pdf", 3, 2021, [(0, 90, 262, 560), (262, 90, 612, 560)], "ar21"),
    ("Calvary-FY23-Annual-Report-.pdf", 8, 2023, [(0, 100, 330, 600), (330, 100, 550, 600), (550, 100, 792, 600)],
     "ar23"),
]
LEADER = re.compile(r"\b(Director|Chief|Deputy|Executive|Sr\. Manager|Senior Manager|Officer)\b")


def font_style(fn: str) -> str:
    fn = fn.split("+")[-1]
    bold = bool(re.search(r"Bold|-(6|7|8|9)00", fn))
    ital = bool(re.search(r"Italic|-It\b|It$", fn))
    return "bolditalic" if bold and ital else ("bold" if bold else ("italic" if ital else "regular"))


def styled_lines(page, bbox):
    c = page.crop(bbox)
    chars = sorted(c.chars, key=lambda ch: (round(ch["top"]), ch["x0"]))
    out = []
    for top, grp in itertools.groupby(chars, key=lambda ch: round(ch["top"])):
        runs = []
        for ch in grp:
            st = font_style(ch["fontname"])
            t = ch["text"].replace("\xa0", " ")
            if runs and runs[-1][0] == st:
                runs[-1][1] += t
            else:
                runs.append([st, t])
        runs = [(st, re.sub(r"\s+", " ", t)) for st, t in runs if t.strip() or st == "regular"]
        if "".join(t for _, t in runs).strip():
            out.append((top, runs))
    return out


def extract_boards(inv):
    rows = []
    for fname, page, ry, crops, style in BOARDS:
        sid = sid_for(inv, fname)
        with pdfplumber.open(INPUTS / fname) as doc:
            pg = doc.pages[page - 1]
            role = "board"
            for bbox in crops:  # role carries over: a heading in one column governs the next column too
                entries, prev_top, prev_bold = [], None, False
                for top, runs in styled_lines(pg, bbox):
                    text = "".join(t for _, t in runs).strip()
                    h = re.sub(r"[\s\-–]+$", "", text)
                    if re.fullmatch(r"(20\d\d )?BOARD OF DIRECTORS", h, re.I):
                        role = "board"
                        continue
                    if re.fullmatch(r"Officers", h, re.I):
                        role = "board_officer"
                        continue
                    if re.fullmatch(r"Members", h, re.I):
                        role = "board_member"
                        continue
                    if re.fullmatch(r"(20\d\d )?(LEADERSHIP )?STAFF|Leadership Staff", h, re.I):
                        role = "staff_leadership" if "leader" in h.lower() else "staff"
                        continue
                    starts = (runs[0][0] in ("bold",)) if style != "fy17" else ("," in text)
                    # FY23: a bold line within 14pt of a bold line is a wrapped title ("Immediate / Past President")
                    if style == "ar23" and starts and prev_bold and prev_top is not None and top - prev_top < 14:
                        starts = False
                    if starts:
                        entries.append(dict(role=role, runs=list(runs)))
                    elif entries:
                        entries[-1]["runs"] += [(st, (" " if k == 0 else "") + t) for k, (st, t) in enumerate(runs)]
                    prev_top, prev_bold = top, runs[0][0] == "bold"
                for e in entries:
                    runs, role = e["runs"], e["role"]
                    bold = "".join(t for st, t in runs if st == "bold").strip()
                    ital = "".join(t for st, t in runs if st == "italic").strip()
                    reg = "".join(t for st, t in runs if st == "regular").strip()
                    name = title = aff = ""
                    if style == "fy17":
                        parts = [x.strip() for x in reg.split(",")]
                        name = parts[0]
                        if role == "staff":
                            title = ital
                        else:
                            title = parts[1] if len(parts) > 1 else ""
                            aff = ital
                    elif style == "ar20":  # bold name, regular title, then italic affiliation (may wrap)
                        name = bold.rstrip(",").strip()
                        seen_it, t_parts, a_parts = False, [], []
                        for st, t in runs:
                            if st == "bold":
                                continue
                            seen_it = seen_it or st == "italic"
                            (a_parts if seen_it else t_parts).append(t)
                        title, aff = "".join(t_parts), "".join(a_parts)
                    elif style == "ar21":
                        name, title, aff = bold, ital, reg.strip(" ,")
                    elif style == "ar23":
                        nm, _, tt = bold.partition(",")
                        name, title, aff = nm.strip(), tt.strip(), reg
                        if aff.lower() == "ex-officio":
                            title, aff = "Ex-Officio", ""
                    name = re.sub(r"\s+", " ", name).strip()
                    title = re.sub(r"\s+", " ", title).strip(" ,")
                    aff = re.sub(r"\s+", " ", aff).strip(" ,")
                    if role == "staff" and not LEADER.search(title):
                        continue  # FY17 lists all staff; keep leadership titles only
                    if role.startswith("staff"):
                        role = "staff_leadership"
                    if not title and role == "board_member":
                        title = "Board Member"
                    rows.append(dict(source_id=sid, document=fname, report_year=ry, name=name, board_title=title,
                                     listed_affiliation=aff, role_type=role, page=page))
    return rows


# ---------------------------------------------------------------- 9. annual report metrics
WORDNUM = {"three": 3, "four": 4, "eight": 8, "eighty": 80, "half": 50}
METRICS = {  # filename -> [(metric, regex with one group, unit, note)]
    AR15: [
        ("women_served", r"More than (\d+) women lived at Calvary in 2015", "women", "more than"),
        ("pct_moved_to_permanent_housing", r"(\d+)% of women moved to permanent housing", "percent", ""),
        ("pct_sister_circle_kept_housing", r"(\d+)% of women in our Sister Circle program maintained", "percent", ""),
        ("pct_maintained_recovery", r"(\d+)% of women maintained their recovery", "percent", ""),
        ("therapy_sessions", r"More than (\d+) psychotherapy sessions", "sessions", "more than"),
        ("pct_engaged_education", r"(\d+)% of women engaged in Life Skills", "percent", "LEAP classes"),
        ("pct_jobprogram_secured_employment", r"(\d+)% of women who participated in Step Up DC secured", "percent",
         "Step Up DC"),
        ("pct_retained_job_3_months", r"(\d+)% of women who secured employment had retained", "percent", ""),
        ("pct_secured_income", r"(\d+)% of women secured income", "percent", ""),
        ("volunteers", r"family of (\d+) volunteers", "volunteers", ""),
        ("volunteer_hours", r"volunteers contributed over ([\d,]+) hours", "hours", "over"),
        ("volunteer_fte_equivalent", r"additional (three) full-time staff", "FTE", "stated in words"),
    ],
    "Calvary-Women_s-Services-FY2017-Annual-Report.pdf": [
        ("transitional_housing_units", r"Transitional housing, providing (\d+) units", "units", ""),
        ("permanent_housing_units", r"Permanent housing, providing (\d+) units", "units", ""),
        ("women_served", r"for a total of (\d+) women", "women", ""),
        ("pct_income_employment_or_benefits", r"(\d+)% of women received income", "percent", ""),
        ("pct_maintained_recovery", r"(\d+)% of women maintained their recovery", "percent", ""),
        ("pct_engaged_education", r"(\d+)% of women engaged in Life Skills", "percent", ""),
        ("nights_safe_housing", r"Over ([\d,]+) nights of safe housing", "nights", "over"),
        ("meals_served", r"Over ([\d,]+) nutritious meals", "meals", "over"),
        ("therapy_sessions", r"Over (\d+) therapy sessions", "sessions", "over"),
        ("education_class_hours", r"Over (\d+) hours of Life Skills", "hours", "over"),
        ("pct_completers_ended_homelessness", r"completed our programs, (\d+)% successfully ended", "percent", ""),
        ("jobprogram_participants", r"(\d+) women participated in Step Up DC", "women", ""),
        ("pct_jobprogram_secured_employment", r"more than (\d+)% of women secured part", "percent", "more than"),
        ("volunteers", r"family of (\d+) volunteers", "volunteers", ""),
        ("volunteer_fte_equivalent", r"equal to (four) full", "FTE", "stated in words"),
        ("pct_donations_direct_to_women", r"(Eighty) percent of donations go directly", "percent", "stated in words"),
        ("revenue_total_stated", r"Revenue: \$([\d,]+)", "USD", "audit FY17 total revenue is $2,432,385"),
        ("expenses_total_stated", r"Expenses: \$([\d,]+)", "USD", ""),
    ],
    "Calvary-Womens-Services_FY18-Annual-Report.pdf": [
        ("women_served", r"Calvary served over (\d+) women", "women", "over"),
        ("pct_completers_moved_home", r"More than (\d+)% of women who completed our programs moved", "percent",
         "more than"),
        ("nights_safe_housing", r"over ([\d,]+) nights of safe housing", "nights", "over"),
        ("meals_served", r"more than ([\d,]+) nutritious meals", "meals", "more than"),
        ("pct_relapse_group_kept_sobriety", r"More than (\d+)% of women who attended", "percent", "more than"),
        ("therapy_sessions", r"over (\d+) sessions with a therapist", "sessions", "over"),
        ("education_class_hours", r"over (\d+) hours of education", "hours", "over"),
        ("pct_engaged_education", r"Over (\d+)% of women participated in our education", "percent", "over"),
        ("volunteers", r"Over (\d+) volunteers contributed", "volunteers", "over"),
        ("volunteer_fte_equivalent", r"equal to (\d+) full-time", "FTE", ""),
        ("volunteer_and_inkind_value", r"donated goods was nearly \$([\d,]+)", "USD", "nearly"),
        ("pct_interviewees_secured_job", r"More than (\d+)% of women who participated in job interviews", "percent",
         "more than"),
        ("job_search_hours", r"more than (\d+) hours of supervised job search", "hours", "more than"),
        ("revenue_total_stated", r"2018 Revenue \$([\d,]+)", "USD", ""),
        ("expenses_total_stated", r"2018 Expenses \$([\d,]+)", "USD", ""),
    ],
    "Calvary-Womens-Services-2020-Annual-Report.pdf": [
        ("total_housing_units", r"(\d+) ●? ?total units of housing", "units", ""),
        ("transitional_housing_units", r"Transitional housing, providing (\d+) units", "units", ""),
        ("permanent_housing_units", r"Permanent housing, providing (\d+) units", "units", ""),
        ("women_served", r"for a total of (\d+) women", "women", ""),
        ("pct_income_employment_or_benefits", r"(\d+)% of women received income", "percent", ""),
        ("pct_maintained_recovery", r"(\d+)% of women maintained their recovery", "percent", ""),
        ("pct_engaged_education", r"(\d+)% of women engaged in Life Skills", "percent", ""),
        ("pct_jobprogram_secured_employment", r"(\d+)% of women who participated in our Step Up DC", "percent", ""),
        ("pct_completers_ended_homelessness", r"completed our programs, (\d+)% successfully", "percent", ""),
        ("nights_safe_housing", r"Over ([\d,]+) nights of safe housing", "nights", "over"),
        ("meals_served", r"Over ([\d,]+) nutritious meals", "meals", "over"),
        ("therapy_sessions", r"Over (\d+) therapy sessions", "sessions", "over"),
        ("education_class_hours", r"Over (\d+) hours of Life Skills", "hours", "over"),
        ("volunteers", r"family of (\d+) volunteers", "volunteers", ""),
        ("new_volunteers", r"including (\d+) new volunteers", "volunteers", ""),
        ("volunteer_hours", r"over ([\d,]+) hours of service", "hours", "over"),
        ("pct_funding_philanthropy", r"With (half) of our funding coming from philanthropy", "percent", "'half'"),
        ("revenue_total_stated", r"2020 Revenue \$([\d,]+)", "USD", ""),
        ("expenses_total_stated", r"2020 Expenses \$([\d,]+)", "USD", ""),
    ],
    "Calvary-2021-AR-Working-C.pdf": [
        ("beds_good_hope_transitional", r"Good Hope Transitional Housing\s*—\s*(\d+) beds", "beds", ""),
        ("beds_reach_up_transitional", r"Reach Up Transitional Housing\s*—\s*(\d+) beds", "beds", ""),
        ("units_reach_up_rental_assistance", r"Reach Up Rental Assistance Program\s*—\s*(\d+) units", "units", ""),
        ("beds_sister_circle_psh", r"Sister Circle\s*—\s*(\d+) beds", "beds", ""),
        ("units_sisters_rise_psh", r"Sisters Rise\s*—\s*(\d+) units", "units", ""),
        ("nights_safe_housing", r"more than ([\d,]+) nights of safe housing", "nights", "more than"),
        ("women_short_term_housing", r"(\d+) women lived in our short-?\s?term", "women", ""),
        ("women_permanent_housing", r"and (\d+) in our permanent housing", "women", ""),
        ("therapy_sessions", r"more than (\d+) therapy sessions", "sessions", "more than"),
        ("nurse_one_on_one_sessions", r"over (\d+) one-on-one sessions with women", "sessions", "over"),
        ("education_class_hours", r"nearly (\d+) hours of volunteer-led", "hours", "nearly"),
        ("jobprogram_avg_starting_wage", r"average starting wage of over \$(\d+)", "USD per hour", "over"),
        ("jobprogram_avg_weekly_earnings", r"average of \$(\d+) each week", "USD per week", ""),
        ("jobprogram_virtual_workshops", r"hosted (eight) virtual career workshops", "workshops", "stated in words"),
        ("volunteers", r"family of (\d+) volunteers", "volunteers", ""),
        ("volunteer_hours", r"provided over ([\d,]+) hours of service", "hours", "over"),
        ("volunteer_value", r"volunteer services was over \$([\d,]+)", "USD", "over"),
        ("virtual_5k_raised", r"raising more than \$([\d,]+)", "USD", "more than"),
        ("new_dv_housing_capacity", r"new housing program for (\d+) women", "women", ""),
        ("pct_funding_philanthropy", r"With (half) of our funding coming from philanthropy", "percent", "'half'"),
        ("revenue_total_stated", r"2021 Revenue \$([\d,]+)", "USD", ""),
        ("expenses_total_stated", r"2021 Expenses \$([\d,]+)", "USD", "audit FY21 total expenses $3,411,954"),
    ],
    "Calvary-FY23-Annual-Report-.pdf": [
        ("volunteers", r"grew to (\d+) individuals in 2023", "volunteers", ""),
        ("pct_volunteer_growth_yoy", r"a (\d+)% increase from the year prior", "percent", ""),
        ("pct_exec_team_black", r"(\d+)% of our executive team identifies as Black\.", "percent", ""),
        ("pct_exec_team_lgbtq", r"(\d+)% of our executive team identifies as LGBTQ", "percent", ""),
        ("pct_staff_black_or_poc", r"(\d+)% of our staff team identifies", "percent", ""),
        ("women_served", r"Calvary served (\d+)", "women", "across six housing sites"),
        ("pct_capacity_growth_since_2021", r"expanded our capacity by (\d+)%", "percent", ""),
        ("volunteer_hours", r"Volunteers logged ([\d,]+) hours", "hours", ""),
        ("nights_safe_housing", r"([\d,]+)\+ nights of safe housing", "nights", "46,400+"),
        ("beds_added_dv", r"(\d+)\s+e*beds added", "beds", ""),
        ("pct_completers_stably_housed", r"(\d+)% of women who completed our housing programs", "percent", ""),
        ("pct_engaged_mental_health", r"(\d+)%\s+(?:of women living\s+)?at Calvary engaged in mental health",
         "percent", ""),
        ("therapy_sessions", r"Nearly (\d+) therapy sessions", "sessions", "nearly"),
        ("meals_served", r"([\d,]+)\+ nutritious meals", "meals", "50,800+"),
        ("pct_engaged_education", r"(\d+)% of women participated in educational", "percent", ""),
        ("pct_jobprogram_secured_employment", r"(\d+)% of women who completed Calvary’s employment", "percent", ""),
        ("pct_jobprogram_attendance_growth", r"saw an (\d+)% increase in attendees", "percent", "Step Up DC"),
        ("pct_therapy_sessions_growth_yoy", r"nearly (\d+)% year-?\s?over-year growth", "percent", "nearly"),
        ("pct_funding_private", r"With about (half) of our funding coming from private donors", "percent", "'about half'"),
        ("revenue_total_stated", r"2023 Revenue \$([\d,]+)", "USD",
         "equals audit without-donor-restriction column incl. releases; audit total revenue $4,807,645"),
        ("expenses_total_stated", r"2023 Expenses \$([\d,]+)", "USD", ""),
    ],
    "Calvary-FY23-Annual-Report-Flyer.pdf": [
        ("pct_engaged_education", r"(\d+)% of residents participated in educational", "percent", ""),
        ("nights_safe_housing", r"([\d,]+)\+ nights of safe housing", "nights", "46,400+"),
        ("therapy_sessions", r"Nearly (\d+)", "sessions", "nearly"),
        ("pct_engaged_mental_health", r"(\d+)% of women living at Calvary engaged in mental", "percent", ""),
        ("meals_served", r"([\d,]+)\+ nutritious meals", "meals", "50,800+"),
        ("beds_added_dv", r"(\d+) beds added", "beds", ""),
        ("volunteer_hours", r"Volunteers logged ([\d,]+) hours", "hours", ""),
        ("pct_jobprogram_secured_employment", r"(\d+)% of women who completed Calvary’s employment", "percent", ""),
        ("pct_completers_stably_housed", r"(\d+)% of women who completed our programs secured", "percent", ""),
        ("women_served", r"Calvary served (\d+) women", "women", ""),
    ],
    "Calvary-FY24-Annual-Report-at-Glance-Final.pdf": [
        ("nights_safe_housing", r"([\d,]+)\+ nights of safe housing", "nights", "48,100+"),
        ("volunteer_hours", r"Volunteers logged ([\d,]+)", "hours", ""),
        ("pct_engaged_mental_health", r"(\d+)% of women living at Calvary engaged in mental", "percent", ""),
        ("pct_maintained_sobriety", r"(\d+)% of women maintained their sobriety", "percent", ""),
        ("meals_served", r"([\d,]+) nutritious meals", "meals", ""),
        ("pct_transitional_in_education", r"(\d+)% of women in transitional housing participate", "percent", ""),
        ("women_served", r"Calvary served (\d+)", "women", ""),
        ("therapy_sessions", r"(\d[\d,]*) (?:therapy sessions )?provided on-? ?site", "sessions", ""),
        ("pct_income_at_exit", r"(\d+)% of women have income when they leave", "percent", ""),
        ("pct_completers_stably_housed", r"Over (\d+)% of women who completed our programs secured", "percent", "over"),
    ],
}
# Values drawn as vector graphics (no text layer); read visually from the page.
METRICS_VISUAL = {
    "Calvary-FY23-Annual-Report-.pdf": [("pct_board_women", 90, "percent", 4), ("pct_board_black_or_poc", 50, "percent", 4)],
}
# Pie/bar charts: (page, kind, region bbox, [(category, keyword located on page)])
PIES = {
    AR15: [(5, "revenue", (40, 180, 560, 450), [("Public Funds", "Public"), ("Foundations & Corporations", "Foundations"),
                                                 ("Individuals & Families", "Individuals"), ("In-Kind Donations", "In-Kind"),
                                                 ("Other", "Other")]),
           (5, "expenses", (200, 505, 560, 565), [("Programs", "Programs"), ("Fundraising", "Fundraising"),
                                                  ("Management & General", "Management")])],
    "Calvary-Women_s-Services-FY2017-Annual-Report.pdf": [
        (4, "revenue", (60, 210, 415, 445), [("Public", "Public"), ("Corporations", "Corporations"),
                                             ("Foundations", "Foundations"), ("Individuals and Major Donors", "Individuals"),
                                             ("Pro Bono/In-Kind", "Pro"), ("Other", "Other")]),
        (4, "expenses", (60, 465, 415, 700), [("Programs", "Programs"), ("Fundraising", "Fundraising"),
                                              ("Administrative", "Administrative")])],
    "Calvary-Womens-Services_FY18-Annual-Report.pdf": [
        (3, "revenue", (30, 165, 560, 310), [("Public Funds", "Public"), ("Foundations & Corporations", "Foundations"),
                                             ("Individuals & Families", "Individuals"),
                                             ("Donated Goods & Services", "Donated"), ("Other", "Other")]),
        (3, "expenses", (30, 375, 560, 450), [("Programs and Services", "Programs"), ("Fundraising", "Fundraising"),
                                              ("Management and General", "Management")])],
    "Calvary-Womens-Services-2020-Annual-Report.pdf": [
        (6, "revenue", (300, 170, 792, 400), [("Public Funds", "Public"), ("Foundations & Corporations", "Foundations"),
                                              ("Individuals & Families", "Individuals"), ("Other", "Other"),
                                              ("Donated Goods & Services", "Donated")]),
        (6, "expenses", (200, 450, 792, 545), [("Programs and Services", "Programs"), ("Fundraising", "Fundraising"),
                                               ("Management and General", "Management")])],
    "Calvary-2021-AR-Working-C.pdf": [
        (12, "revenue", (330, 140, 560, 340), [("Other", "Other"), ("Donated Goods & Services", "Donated"),
                                               ("Individuals & Families", "Individuals"),
                                               ("Foundations & Corporations", "Foundations"), ("Public Funds", "Public")]),
        (12, "expenses", (180, 400, 560, 500), [("Management and General", "Management"),
                                                ("Fundraising & Events", "Fundraising"),
                                                ("Programs and Services", "Programs")])],
    "Calvary-FY23-Annual-Report-.pdf": [
        (7, "revenue", (400, 140, 792, 310), [("Other", "Other"), ("Donated Goods & Services", "Donated"),
                                              ("Individuals & Families", "Individuals"),
                                              ("Foundations & Corporations", "Foundations"), ("Public Funds", "Public")]),
        (7, "expenses", (250, 395, 792, 500), [("Management & General", "Management"), ("Fundraising", "Fundraising"),
                                               ("Programs", "Programs")])],
}
# Visually verified chart values, used only as a QC comparison for the spatial matcher.
PIE_EXPECTED = {
    (AR15, "revenue"): [43, 32, 19, 5, 1], (AR15, "expenses"): [80, 18, 2],
    ("Calvary-Women_s-Services-FY2017-Annual-Report.pdf", "revenue"): [38, 18, 17, 19, 7, 1],
    ("Calvary-Women_s-Services-FY2017-Annual-Report.pdf", "expenses"): [80, 17, 3],
    ("Calvary-Womens-Services_FY18-Annual-Report.pdf", "revenue"): [42, 28, 21, 8, 1],
    ("Calvary-Womens-Services_FY18-Annual-Report.pdf", "expenses"): [80, 16, 4],
    ("Calvary-Womens-Services-2020-Annual-Report.pdf", "revenue"): [47, 22, 19, 9, 3],
    ("Calvary-Womens-Services-2020-Annual-Report.pdf", "expenses"): [83, 12, 5],
    ("Calvary-2021-AR-Working-C.pdf", "revenue"): [1, 4, 20, 20, 55],
    ("Calvary-2021-AR-Working-C.pdf", "expenses"): [7, 14, 79],
    ("Calvary-FY23-Annual-Report-.pdf", "revenue"): [1, 4, 16, 34, 45],
    ("Calvary-FY23-Annual-Report-.pdf", "expenses"): [8, 17, 75],
}


def pct_tokens(words):
    out = []
    for i, w in enumerate(words):
        m = re.fullmatch(r"(\d{1,3})%", w["text"])
        if m:
            out.append((int(m.group(1)), w))
        elif re.fullmatch(r"\d{1,3}", w["text"]) and any(
                o["text"].startswith("%") and abs(o["top"] - w["top"]) < 12 and -4 <= o["x0"] - w["x1"] < 12
                for o in words):
            out.append((int(w["text"]), w))
    return out


def extract_pies(fname, specs):
    rows, warns = [], []
    with pdfplumber.open(INPUTS / fname) as doc:
        for page, kind, bbox, cats in specs:
            words = doc.pages[page - 1].crop(bbox).extract_words(x_tolerance=1.5, y_tolerance=2)
            pcts = pct_tokens(words)
            locs = []
            for cat, kw in cats:
                w = next((w for w in words if w["text"].startswith(kw)), None)
                locs.append(w)
            if any(l is None for l in locs) or len(pcts) < len(cats):
                warns.append(f"{fname} p{page} {kind}: labels found {sum(l is not None for l in locs)}/{len(cats)}, "
                             f"% tokens {len(pcts)}")
                continue

            def ctr(w):
                return ((w["x0"] + w["x1"]) / 2, (w["top"] + w["bottom"]) / 2)

            best = None
            for perm in itertools.permutations(range(len(pcts)), len(cats)):
                d = sum(((ctr(locs[i])[0] - ctr(pcts[j][1])[0]) ** 2 + (ctr(locs[i])[1] - ctr(pcts[j][1])[1]) ** 2) ** .5
                        for i, j in enumerate(perm))
                if best is None or d < best[0]:
                    best = (d, perm)
            got = [pcts[j][0] for j in best[1]]
            exp = PIE_EXPECTED.get((fname, kind))
            qc = "matches visual check" if exp == got else f"DIFFERS from visual check {exp}"
            if exp != got:
                warns.append(f"{fname} {kind} pie: extracted {got} vs visual {exp}")
            for (cat, _), v in zip(cats, got):
                rows.append(dict(metric=f"{kind}_share_{norm_name(cat).replace(' ', '_')}", value=v, unit="percent",
                                 notes=f"chart category '{cat}' (p{page}); label-to-value by nearest position; {qc}"))
            if sum(got) != 100:
                warns.append(f"{fname} {kind} pie sums to {sum(got)}")
    return rows, warns


def text_blocks(page, gap=12):
    """Group words into visual text boxes (Canva/InDesign layouts): split rows at wide gaps, then stack lines
    that overlap horizontally and sit within ~one line height of each other."""
    ws = page.extract_words(x_tolerance=1.5, y_tolerance=2)
    lines = []
    for r in cluster_rows(ws, tol=2.5):
        seg = [r[0]]
        for w in r[1:]:
            if w["x0"] - seg[-1]["x1"] > gap:
                lines.append(seg)
                seg = [w]
            else:
                seg.append(w)
        lines.append(seg)
    lines = sorted([dict(x0=min(w["x0"] for w in g), x1=max(w["x1"] for w in g), top=min(w["top"] for w in g),
                         bottom=max(w["bottom"] for w in g), text=" ".join(w["text"] for w in g)) for g in lines],
                   key=lambda l: l["top"])
    blocks = []
    for l in lines:
        h = l["bottom"] - l["top"]
        for b in blocks:
            last = b["lines"][-1]
            if -2 <= l["top"] - last["bottom"] <= max(8, 0.9 * h) and min(l["x1"], b["x1"]) - max(l["x0"], b["x0"]) > 0:
                b["lines"].append(l)
                b["x0"], b["x1"] = min(b["x0"], l["x0"]), max(b["x1"], l["x1"])
                break
        else:
            blocks.append(dict(lines=[l], x0=l["x0"], x1=l["x1"]))
    return [" ".join(x["text"] for x in b["lines"]) for b in blocks]


def extract_metrics(inv):
    rows, warns = [], []
    for fname, specs in METRICS.items():
        sid = sid_for(inv, fname)
        ry = int(inv[fname]["fiscal_year"])
        pdf = INPUTS / fname
        txt = re.sub(r"\s+", " ", plain_text(pdf).replace("\xa0", " ").replace("﻿", ""))
        with pdfplumber.open(pdf) as doc:
            blocks = " ¶ ".join(b for p in doc.pages for b in text_blocks(p))
        hay = txt + " ¶ " + blocks
        for metric, pat, unit, note in specs:
            m = re.search(pat, hay)
            if not m:
                warns.append(f"{fname}: metric {metric} not found")
                continue
            raw = m.group(1)
            v = WORDNUM.get(raw.lower(), None)
            v = v if v is not None else fmt(to_num(raw))
            ctx = re.sub(r"\s*¶\s*", " ", m.group(0))
            rows.append(dict(source_id=sid, document=fname, report_year=ry, metric=metric, value=v, unit=unit,
                             notes="; ".join(x for x in (note, f"text: '{ctx[:90]}'") if x)))
        for metric, v, unit, page in METRICS_VISUAL.get(fname, []):
            rows.append(dict(source_id=sid, document=fname, report_year=ry, metric=metric, value=v, unit=unit,
                             notes=f"p{page}: value drawn as vector graphic (no text layer); transcribed visually"))
    for fname, specs in PIES.items():
        got, w = extract_pies(fname, specs)
        warns += w
        for r in got:
            r.update(source_id=sid_for(inv, fname), document=fname, report_year=int(inv[fname]["fiscal_year"]))
        rows += got
    if inv.get("Calvary-FY23-Annual-Report-Flyer.pdf", {}).get("status") == "duplicate":
        ar = {(r["metric"], r["value"]) for r in rows if r["document"] == "Calvary-FY23-Annual-Report-.pdf"}
        for r in rows:
            if r["document"] == "Calvary-FY23-Annual-Report-Flyer.pdf":
                same = (r["metric"], r["value"]) in ar
                r["notes"] = ("same value in FY23 annual report (duplicate source); " if same
                              else "NOT in FY23 annual report; ") + r["notes"]
    return rows, warns


# ---------------------------------------------------------------- 10. QC, notes, main
def name_in_layout(pdf: Path, page: int, name: str) -> bool:
    t = re.sub(r"\s+", " ", layout_page(pdf, page)).lower()
    parts = [name.rstrip("*").strip().lower()]
    if parts[0] not in t:  # wrapped names: each half must be present
        words = parts[0].split()
        for k in range(1, len(words)):
            a, b = " ".join(words[:k]), " ".join(words[k:])
            if a in t and b in t:
                return True
        return False
    return True


def match_key(n: str) -> str:
    n = norm_name(n)
    return re.sub(r"\b(foundation|charitable|fund|llp|lp|inc|community connections)\b", " ", n).split() and \
        " ".join(re.sub(r"\b(foundation|charitable|llp|lp|inc)\b", " ", n).split())


def affil_matches(aff: str, funder: str, truncated: bool) -> bool:
    a, f = match_key(aff), match_key(funder)
    if not a or not f or len(a) < 3 or len(f) < 3:
        return False
    if a == f or a.startswith(f + " ") or f.startswith(a + " "):
        return True
    if truncated and a.startswith(f):
        return True
    ta, tf = a.split(), f.split()
    return len(ta) >= 2 and len(tf) >= 2 and ta[:2] == tf[:2]


def md_once(fname: str, heading: str, text: str):
    p = Path(__file__).resolve().parents[1] / fname
    cur = p.read_text(encoding="utf-8") if p.exists() else ""
    if f"## {heading}\n" in cur:
        return False
    append_md(fname, heading, text)
    return True


def main():
    inv = load_inventory()
    OUT.mkdir(parents=True, exist_ok=True)
    n_text = dump_texts()

    audit, w_a = extract_audits(inv)
    checks = tieouts(audit)
    sefa, n_sefa = extract_sefa(inv)
    f990, w_f = extract_990(inv)
    checks += check_990(f990)
    people, w_p = extract_part7(inv)
    sched_i = extract_schedule_i(inv)
    ar_f, bands, _ = extract_ar15_donors(inv)
    cfs, w_c = extract_support_page(inv)
    gov_m = extract_audit_grantors(inv)
    boards = extract_boards(inv)
    metrics, w_m = extract_metrics(inv)
    crm, crm_stats = extract_crm(inv)
    strat, w_s = extract_strategic(inv)

    # SEFA vs Statement of Activities federal lines (FY23)
    fed = sum(float(r["amount"]) for r in audit if r["document"] in SEFA_DOCS and r["fiscal_year"] == 2023
              and r["line_item_std"] == "rev_gov_federal" and r["net_asset_class"] == T)
    sefa_tot = sum(float(r["amount"]) for r in sefa)
    checks.append(dict(source_id="input_fy23_audit", document=next(iter(SEFA_DOCS)), fiscal_year=2023,
                       statement="SEFA vs SOA", net_asset_class=T, check="SEFA total = SOA federal revenue lines",
                       components_sum=fmt(sefa_tot), printed_total=fmt(fed), difference=fmt(sefa_tot - fed),
                       result="tie" if abs(sefa_tot - fed) < 1.5 else "NO TIE",
                       notes="SOA: Federal grants - COVID-19 + Federal entitlements and other federal funds"))
    # Part VII-A compensation total for TY2024 (printed 1d = 641,070)
    comp24 = sum(float(r["reportable_comp"] or 0) for r in people if r["tax_year"] == 2024)
    checks.append(dict(source_id="input_propublica_990_ty2024", document=next(k for k, v in F990.items() if v == 2024),
                       fiscal_year=2025, statement="990 TY2024", net_asset_class="",
                       check="Part VII-A reportable comp rows sum to line 1d(D)", components_sum=fmt(comp24),
                       printed_total=641070, difference=fmt(comp24 - 641070),
                       result="tie" if abs(comp24 - 641070) < 1.5 else "NO TIE", notes="printed 1d read from text"))

    funders = ar_f + cfs + gov_m
    # every annual-report / support-page name must appear in that page's layout text
    miss = [r for r in ar_f + cfs if "logo" not in r["notes"]
            and not name_in_layout(INPUTS / r["document"], r["page"], r["funder_name_raw"])]

    AF = ["source_id", "document", "page", "fiscal_year", "tax_year", "statement", "line_item", "line_item_std",
          "net_asset_class", "amount", "is_prior_year_comparative", "notes"]
    files = {
        "audit_financials.csv": (AF, audit),
        "audit_tieout_checks.csv": (["source_id", "document", "fiscal_year", "statement", "net_asset_class", "check",
                                     "components_sum", "printed_total", "difference", "result", "notes"], checks),
        "sefa_federal_awards.csv": (["source_id", "document", "page", "fiscal_year", "federal_agency",
                                     "pass_through_entity", "program_name", "assistance_listing",
                                     "pass_through_award_id", "amount", "amount_to_subrecipients", "notes"], sefa),
        "form990_pdf_financials.csv": (["source_id", "document", "page", "tax_year", "fiscal_year", "part", "line",
                                        "line_label", "column", "amount", "notes"], f990),
        "form990_pdf_people.csv": (["source_id", "tax_year", "name", "title", "avg_hours", "role_flags",
                                    "reportable_comp", "document", "page", "line_no"], people),
        "form990_pdf_schedule_i.csv": (["source_id", "document", "page", "tax_year", "schedule_part",
                                        "type_of_assistance", "number_of_recipients", "cash_grant",
                                        "noncash_assistance", "valuation_method", "noncash_description"], sched_i),
        "funder_mentions.csv": (["source_id", "document", "page", "report_year", "fiscal_year", "funder_name_raw",
                                 "funder_name_norm", "org_type_guess", "gift_band_raw", "band_min", "band_max",
                                 "in_kind_flag", "truncated", "section_heading", "notes"], funders),
        "individual_donor_band_counts.csv": (["source_id", "document", "report_year", "gift_band_raw", "band_min",
                                              "band_max", "individual_count", "notes"],
                                             [dict(r, notes="count of printed listings; a couple or household "
                                                            "listed together counts as one; 'Anonymous' included")
                                              for r in bands]),
        "board_lists.csv": (["source_id", "document", "report_year", "name", "board_title", "listed_affiliation",
                             "role_type", "page"], boards),
        "annual_report_metrics.csv": (["source_id", "document", "report_year", "metric", "value", "unit", "notes"],
                                      metrics),
        "crm_funders_2023_2026.csv": (CRM_COLS + ["funder_name_norm", "org_type_guess", "source_id",
                                                  "gift_total_window", "notes"], crm),
        "strategic_plan_targets.csv": (["source_id", "document", "plan_period", "goal_area", "target_text",
                                        "target_value", "target_unit", "target_year", "reported_result_text",
                                        "reported_value", "notes"], strat),
    }
    counts = {}
    for name, (fields, rows) in files.items():
        write_csv(name, fields, rows)
        counts[name] = len(rows)

    bad = [c for c in checks if c["result"] != "tie"]
    warns = w_a + w_f + w_p + w_c + w_m + w_s
    lines = [f"- text dumps: {n_text} files in {rel(TEXT)}"]
    lines += [f"- {rel(OUT / k)}: {v} rows" for k, v in counts.items()]
    lines += [f"- tie-out checks: {len(checks) - len(bad)}/{len(checks)} tie"]
    lines += [f"  - NO TIE: {c['document']} FY{c['fiscal_year']} {c['statement']} {c['net_asset_class']}: "
              f"{c['check']} ({c['components_sum']} vs {c['printed_total']})" for c in bad]
    lines += [f"- SEFA: {x}" for x in n_sefa]
    lines += [f"- CRM export: {crm_stats['rows']} orgs, GIFT_TOTAL ${crm_stats['gift_total']:,.2f}, "
              f"{crm_stats['gifts']} gifts, last-gift dates {crm_stats['first']} to {crm_stats['last']}; "
              f"{crm_stats['n_inconsistent']} rows have NUM_GIFTS=1 but GIFT_TOTAL != LAST_CONTRIB_AMT; "
              f"GIFT_TOTAL window recorded as unconfirmed"]
    lines += [f"- funder names verified in layout text: {len(ar_f) + len(cfs) - len(miss)}/{len(ar_f) + len(cfs)}"
              + (f"; missing: {[r['funder_name_raw'] for r in miss]}" if miss else "")]
    lines += [f"- WARNING: {x}" for x in warns if "Part I not in text layer" not in x]
    lines += [f"- note: {x}" for x in warns if "Part I not in text layer" in x]
    log("02_extract_inputs", "\n".join(lines))
    print("\n".join(lines))
    write_notes(audit, f990, sefa, ar_f, cfs, boards, metrics, bands)
    write_notes_crm_strat(crm, crm_stats, strat, boards, ar_f, cfs)


def write_notes_crm_strat(crm, st, strat, boards, ar_f, cfs):
    tot = st["gift_total"]
    top = sorted(crm, key=lambda r: -float(r["GIFT_TOTAL"]))
    top10 = sum(float(r["GIFT_TOTAL"]) for r in top[:10])
    by_type = defaultdict(float)
    for r in crm:
        by_type[r["org_type_guess"]] += float(r["GIFT_TOTAL"])
    keys_site = {match_key(r["funder_name_raw"].rstrip("*")) for r in cfs}
    keys_ar15 = {match_key(r["funder_name_raw"]) for r in ar_f}

    def listed(k, pool):
        return any(k == j or k.startswith(j + " ") or j.startswith(k + " ") for j in pool)
    on_site = sum(1 for r in crm if listed(match_key(r["last_name"]), keys_site))
    on_ar15 = sum(1 for r in crm if listed(match_key(r["last_name"]), keys_ar15))
    board_aff = {b["listed_affiliation"] for b in boards if b["listed_affiliation"] and b["role_type"] != "staff_leadership"}
    board_hits = sorted({f"{r['last_name']} (${float(r['GIFT_TOTAL']):,.0f})" for r in crm for a in board_aff
                         if affil_matches(a, r["last_name"], False)})
    h16 = next(r for r in strat if r["plan_period"] == "2016-2019" and r["goal_area"] == "housing")
    h21 = next(r for r in strat if r["plan_period"] == "2021-2024" and r["goal_area"] == "housing")
    notes = [
        f"- CRM export (internal): {st['rows']} organizations, GIFT_TOTAL ${tot:,.0f} over {st['gifts']} gifts. "
        f"Top 10 hold {top10 / tot:.0%}: " + ", ".join(f"{r['last_name']} ${float(r['GIFT_TOTAL']):,.0f}"
                                                       for r in top[:10]) + ".",
        "- CRM GIFT_TOTAL by org_type_guess: " + ", ".join(f"{k} ${v:,.0f}" for k, v in
                                                          sorted(by_type.items(), key=lambda kv: -kv[1])) + ".",
        f"- CRM vs public lists: {on_site} of {st['rows']} CRM orgs match a name on the Sept 2023 support page; "
        f"{on_ar15} match the FY15 AR list. {st['n_inconsistent']} rows show NUM_GIFTS=1 with GIFT_TOTAL above "
        "the last gift, so GIFT_TOTAL and NUM_GIFTS may cover different windows.",
        f"- CRM orgs matching a board-listed employer: {', '.join(board_hits)}.",
        f"- Strategic plans: 2016-2019 target {h16['target_value']} new PSH units; report: {h16['reported_value']} new "
        f"housing slots (all types). 2021-2024 target {h21['target_value']} units; internal final report: "
        f"{h21['reported_value']} units (printed components sum to 64). Fundraising staff held at 6 positions with "
        "'limited growth' (2021-2024 report). Reach Up (2019) was funded by TCP 10 beds, HUD 6, OVSJG 15 (first "
        "OVSJG award).",
    ]
    md_once("notes_for_analysis.md", "Inputs (Phase 1): CRM export and strategic plans", "\n".join(notes))
    md_once("open_questions.md", "Inputs (Phase 1): CRM export",
            "- `Foundation & Corporate Funders_2023-2026.xlsx`: does GIFT_TOTAL (and NUM_GIFTS) cover only gifts "
            "dated in the 2023-2026 window, or lifetime giving? "
            f"{st['n_inconsistent']} rows have NUM_GIFTS=1 but GIFT_TOTAL > LAST_CONTRIB_AMT (e.g. John E. Fowler "
            "Memorial Foundation: 1 gift, last $40,000, total $310,000). Recorded as 'unconfirmed' until you confirm. "
            "Also: is the window gift date or fiscal year?")


def write_notes(audit, f990, sefa, ar_f, cfs, boards, metrics, bands):
    # government share of total revenue by fiscal year, from the most recent audit covering that year
    latest = {}
    for r in audit:
        if r["statement"] == "SOA" and r["net_asset_class"] == T:
            latest.setdefault(r["fiscal_year"], set()).add(r["document"])
    order = list(AUDITS)
    gov_lines = []
    for fy in sorted(latest):
        doc = max(latest[fy], key=order.index)
        rs = [r for r in audit if r["document"] == doc and r["fiscal_year"] == fy and r["statement"] == "SOA"
              and r["net_asset_class"] == T]
        tot = next(float(r["amount"]) for r in rs if r["line_item_std"] == "rev_total")
        gov = sum(float(r["amount"]) for r in rs if r["line_item_std"].startswith("rev_gov"))
        ppp = sum(float(r["amount"]) for r in rs if r["line_item_std"] == "rev_ppp_forgiveness")
        gov_lines.append(f"FY{fy % 100:02d} {gov / tot:.0%}" + (f" (+PPP {ppp / tot:.0%})" if ppp else ""))
    ty24 = {(r["line"], r["column"]): float(r["amount"]) for r in f990 if r["tax_year"] == 2024 and r["amount"] != ""}
    gov24 = ty24.get(("1e", "inner_box"), 0) / ty24.get(("12", "A_total"), 1)

    # board affiliations that match an organization on a funder list
    flist = [(r["funder_name_raw"].rstrip("*"), r["truncated"],
              f"FY15 AR {r['gift_band_raw']}" if r["document"] == AR15 else f"2023 site {r['gift_band_raw']}")
             for r in ar_f + cfs]
    overlaps = defaultdict(lambda: ["", set(), set()])
    for b in boards:
        if not b["listed_affiliation"] or b["role_type"] == "staff_leadership":
            continue
        for fn, tr, src in flist:
            if affil_matches(b["listed_affiliation"], fn, tr):
                o = overlaps[match_key(b["listed_affiliation"]).split()[0]]
                o[0] = b["listed_affiliation"]
                o[1].add(str(b["report_year"]))
                o[2].add(src + (f" as '{fn}' (truncated)" if tr else ""))
    ov_txt = "; ".join(f"{v[0]} (board {'/'.join(sorted(v[1]))}; {', '.join(sorted(v[2]))})"
                       for _, v in sorted(overlaps.items()))

    # FY15 AR org list vs 2023 support page
    k15 = {match_key(r["funder_name_raw"]) for r in ar_f if r["funder_name_raw"] != "Anonymous"}
    k23 = {match_key(r["funder_name_raw"].rstrip("*")) for r in cfs}
    both = {k for k in k15 if any(k == j or k.startswith(j + " ") or j.startswith(k + " ") for j in k23)}
    ind = {r["gift_band_raw"]: r["individual_count"] for r in bands}

    notes = [
        f"- Government share of total revenue (audits, total column; latest audit per year): {', '.join(gov_lines)}. "
        f"TY2024 990 (FY25): line 1e government grants {gov24:.0%} of total revenue.",
        "- FY22 (comparative in FY23 audit): total revenue $9.26M incl. $3.60M 'Federal and local government "
        "contracts'; net assets +$4.32M; property and equipment, net $2.74M (FY21) -> $6.33M (FY22). No FY22 audit "
        "in inputs.",
        "- FY19 audit restates FY18 with special events shown net: contributions $1,173,337 -> $870,472 + events "
        "net $219,885; total revenue $2,352,225 -> $2,269,245; expenses $2,350,586 -> $2,267,606.",
        "- SEFA appears only in the FY23 audit (single audit; $937,999 federal; major program ALN 21.027 SLFRF via "
        "OVSJG; not a low-risk auditee). FY17-FY20 audits state Calvary was not subject to a single audit; FY21 audit "
        "is silent despite $1.98M 'federal and local government contracts'.",
        "- TY2019 990 counts the $327,200 PPP forgiveness inside line 1e government grants ($2,166,119 = audit "
        "government grants $1,838,919 + PPP).",
        "- FY23 annual report '2023 Revenue $5,423,322' is the audit's without-donor-restriction column incl. "
        "releases; audit total revenue is $4,807,645. FY21 AR expenses $3,411,994 vs audit $3,411,954; FY17 AR revenue "
        "$2,433,568 vs audit $2,432,385.",
        f"- Board-listed employers that also appear on a funder list ({len(overlaps)}): {ov_txt}.",
        f"- FY15 AR lists {len(k15)} named organizations; {len(both)} also appear (name match) on the Sept 2023 "
        f"support page, which lists {len(k23)}. FY15 AR individual listings by band: "
        + ", ".join(f"{k}: {v}" for k, v in ind.items()) + ".",
        "- Only the FY15 annual report carries a donor list; FY17-FY23 reports point to the website instead.",
        "- TY2024 990 Part I prior-year column gives FY24 totals (revenue $5,817,167; expenses $5,310,627), the "
        "only FY24 financials in the inputs. FY25 shows a $607,326 deficit.",
    ]
    md_once("notes_for_analysis.md", "Inputs (Phase 1)", "\n".join(notes))
    qs = [
        "- `Calvary-FY24-Annual-Report-at-Glance-Final.pdf` says 'At a glance | 2024' but was created 2025-11-12, "
        "after FY25 closed. Is it FY24 (Oct 2023-Sep 2024) or FY25? Stored as FY24 for now.",
        "- Inputs have no FY22 or FY24 audit and no 990 PDFs for TY2020-TY2023. Do you have them, or should the build "
        "rely on e-file XML / the FAC for those years?",
        "- FY21 audit has no Uniform Guidance section. Was a single audit performed for FY21 or FY22 (federal "
        "spending may have exceeded $750k)? If yes, can you share it?",
        "- The TY2016 990 PDF is one scanned page (Part I only). Fine to rely on e-file XML for TY2016, or do you "
        "want the page transcribed?",
    ]
    md_once("open_questions.md", "Inputs (Phase 1)", "\n".join(qs))



# ---------------------------------------------------------------- 11. CRM export (organizational donors)
CRM = "Foundation & Corporate Funders_2023-2026.xlsx"
CRM_COLS = ["last_name", "city", "state", "LAST_CONTRIB_AMT", "LAST_CONTRIB_DATE", "GIFT_TOTAL", "NUM_GIFTS"]
CRM_TYPE_OVERRIDES_RAW = {  # printed name -> org_type_guess where the name alone misleads (normalized at load)
    "DCHFA": "government", "International Monetary Fund (IMF)": "other",
    "World Bank Community Connections Fund": "corporate_matching", "America's Charities": "corporate_matching",
    "The Blackbaud Giving Fund": "corporate_matching", "Give Lively Foundation": "daf_sponsor",
    "Charities Aid Foundation of America": "daf_sponsor", "PayPal Giving Fund": "daf_sponsor",
    "Renaissance Charitable": "daf_sponsor", "Schwab Charitable Fund": "daf_sponsor",
    "Vanguard Charitable": "daf_sponsor", "Frontier Co-op Giving Fund": "corporate",
    "Mink-Ling Family Charitable Fund": "foundation", "Omidyar Network": "foundation",
    "Christian Women's Fellowship": "faith", "Ionia R. Whipper Home": "other",
    "Health Equity Fund": "foundation", "Builders Initiative": "foundation",
    "National Institute for Health Care Management": "other", "American Institutes for Research": "other",
    "National Resource Center on Domestic Violence": "civic",
    "DC Coalition Against Domestic Violence (DCCADV)": "civic", "Center for Nonprofit Advancement": "civic",
    "Congressional Sports for Charity": "civic", "Metropolitan Washington DC Drifters": "civic",
    "Alpha Chi Omega, Gamma Theta": "civic", "Zonta Club of Washington Foundation": "civic",
    "Junior League of Washington": "civic", "CREW Washington DC": "civic",
    "Association of American Medical Colleges (AAMC)": "civic", "American Clean Power": "civic",
    "Biotechnology Innovation Organization (BIO)": "civic", "Bessemer Trust": "corporate",
    "The Cortale Group at LPL Financial": "corporate", "RCLCO Foundation": "corporate",
    "Principal Foundation": "corporate", "Qlarant Foundation": "corporate",
}
CRM_TYPE_OVERRIDES = {norm_name(k): v for k, v in CRM_TYPE_OVERRIDES_RAW.items()}
CORP_FDN_CRM = re.compile(r"bank of america|mgm resorts|morrison & foerster|miller & chevalier|venable|kirkland|"
                          r"td bank|principal|qlarant|rclco", re.I)


def crm_org_type(name: str) -> tuple[str, str]:
    n = norm_name(name)
    if n in CRM_TYPE_OVERRIDES:
        return CRM_TYPE_OVERRIDES[n], "override"
    l = name.lower()
    if re.search(r"match|employee|giving campaign|easymatch", l):
        return "corporate_matching", "name rule"
    if re.search(r"donor.advised|giving fund|^(fidelity|schwab|vanguard) charitable", l):
        return "daf_sponsor", "name rule"
    if re.search(r"church|fellowship|parish|ministr|congregation|synagogue|temple", l):
        return "faith", "name rule"
    if re.search(r"foundation|\bfund\b|trust\b", l):
        return ("corporate", "name rule (corporate foundation)") if CORP_FDN_CRM.search(l) else ("foundation", "name rule")
    if re.search(r"club|league|association|sorority|coalition|council", l):
        return "civic", "name rule"
    return "corporate", "default (business name)"


def extract_crm(inv) -> tuple[list[dict], dict]:
    import openpyxl
    sid = sid_for(inv, CRM)
    wb = openpyxl.load_workbook(INPUTS / CRM, read_only=True, data_only=True)
    ws = wb.worksheets[0]
    it = ws.iter_rows(values_only=True)
    hdr = [str(c) for c in next(it)]
    assert hdr == CRM_COLS, f"unexpected CRM columns {hdr}"
    rows = []
    for vals in it:
        if all(v is None for v in vals):
            continue
        r = {k: ("" if v is None else (v.date().isoformat() if hasattr(v, "date") else v)) for k, v in zip(hdr, vals)}
        typ, basis = crm_org_type(str(r["last_name"]))
        flags = []
        try:
            last, tot, n = float(r["LAST_CONTRIB_AMT"]), float(r["GIFT_TOTAL"]), int(r["NUM_GIFTS"])
            if n == 1 and abs(tot - last) > 0.5:
                flags.append("NUM_GIFTS=1 but GIFT_TOTAL != LAST_CONTRIB_AMT (total may cover a longer window)")
            if n >= 15 and tot / n < 1000:
                flags.append("many small gifts: pattern of payroll/employee giving")
            if str(r["city"]).strip().lower() == "princeton" and str(r["state"]).strip() == "NJ":
                flags.append("Princeton NJ address is common to matching-gift processors")
        except (TypeError, ValueError):
            flags.append("non-numeric amount field")
        r.update(funder_name_norm=norm_name(str(r["last_name"])), org_type_guess=typ, source_id=sid,
                 gift_total_window="unconfirmed", notes="; ".join([f"type basis: {basis}"] + flags))
        rows.append(r)
    wb.close()
    stats = dict(rows=len(rows), gift_total=sum(float(r["GIFT_TOTAL"]) for r in rows),
                 gifts=sum(int(r["NUM_GIFTS"]) for r in rows),
                 first=min(r["LAST_CONTRIB_DATE"] for r in rows), last=max(r["LAST_CONTRIB_DATE"] for r in rows),
                 n_inconsistent=sum("NUM_GIFTS=1 but" in r["notes"] for r in rows))
    return rows, stats


# ---------------------------------------------------------------- 12. strategic plans
SP16, SP16R = "Calvary Strategic Plan 2016-2019 (1).pdf", "Strategic Plan 2016-2019 Report (1).pdf"
SP21, SP21R = "Calvary Strategic Plan 2021-2024 FINAL (1).pdf", "2021-2024 Strategic Plan Final Report_internal (1).pdf"
# (plan doc, report doc, plan_period, goal_area, target regex, target unit, target_year, result regex, notes)
# Value = first number in the matched text; regexes run on whitespace-collapsed pdftotext output.
STRAT = [
    (SP16, SP16R, "2016-2019", "housing", r"add at least \d+ new permanent supportive housing units", "PSH units",
     2019, r"exceeded its goal and opened \d+ new housing slots for single women, increasing its capacity by over \d+%",
     "result counts all new slots (transitional, PSH, short-term subsidy), not PSH only"),
    (None, SP16R, "2016-2019", "housing (government funding)", None, "", "",
     r"Secured three government funded grants to open Reach Up, a \d+ bed transitional housing program[^●]*", ""),
    (None, SP16R, "2016-2019", "housing (funding by source)", None, "", "",
     r"Reach Up funded by The Community Partnership \(\d+ beds\), HUD \(\d+ beds\), and Office of Victims Services "
     r"and Justice Grants/OVSJG \(\d+ beds\)[^●]*", "beds by funder: TCP 10, HUD 6, OVSJG 15"),
    (None, SP16R, "2016-2019", "housing (government funding)", None, "", "",
     r"Secured additional HUD funding to open \d+ beds of short-term subsidized housing[^●]*", ""),
    (None, SP16R, "2016-2019", "housing (government funding)", None, "", "",
     r"Secured additional funding from HUD to expand Sister Circle permanent supportive housing from \d+ to \d+ slots",
     "value = slots before expansion; after = 16"),
    (SP16, SP16R, "2016-2019", "employment", r"expand the size and scope of the employment search and placement "
     r"program to serve more women", "", "", r"Joined the collaborative at Skyland Workforce Center in summer \d{4}[^●]*",
     "no numeric target"),
    (SP16, SP16R, "2016-2019", "communications / leadership", r"strategic communications expertise beyond Calvary.s "
     r"current capacity", "", "", r"Full-time Communications Manager resourced by Woodside Strategies for one year "
     r"with foundation grant funding", "no numeric target"),
    (SP16, None, "2016-2019", "funding mix", r"Seek new sources of funding, including the possibility of additional "
     r"government funding that won.t impose onerous limitations on our program model", "", "", None,
     "diversification goal, no numeric target"),
    (None, SP16R, "2016-2019", "funding mix", None, "", "", r"first time applying for and receiving funding from OVSJG",
     "first OVSJG funding"),
    (SP21, SP21R, "2021-2024", "housing", r"Add at least \d+ new housing units for women", "housing units", 2024,
     r"Added \d+ housing units \(\d+ TH, \d+ PSH, \d+ RRH\)",
     "components printed as 18 TH + 15 PSH + 31 RRH = 64, not 66; report says the plan guided Calvary through 2025"),
    (SP21, SP21R, "2021-2024", "data and evaluation", r"Improve our capacity for data management and outcome "
     r"evaluation", "", "", r"Hired new staff position; created dashboard with key performance indicators", ""),
    (SP21, SP21R, "2021-2024", "employment", r"Create more pathways to employment", "", "",
     r"Added second staff position for workforce; unfunded FY\d{4}", "workforce position unfunded in FY2026"),
    (SP21, SP21R, "2021-2024", "case management", r"strengthen our intensive and personalized case management", "", "",
     r"Maintained 1:\d+ case manager to client ratio", "value = clients per case manager"),
    (SP21, SP21R, "2021-2024", "leadership / staffing", r"Design and implement staff structure that offers leadership "
     r"from middle management positions", "", "", r"Hired and/or promoted \d+ into executive or senior "
     r"leadership/management positions \(\d+% black women leaders\)", "value = people hired/promoted; 90% Black women"),
    (SP21, SP21R, "2021-2024", "board", r"drive strategic recruitment for its Board of Directors and leadership staff",
     "", "", None, "final report leaves the accomplishment cell blank"),
    (SP21, SP21R, "2021-2024", "communications", r"Fully fund and staff our strategic communications plan", "", "",
     r"Hired communications manager position", ""),
    (SP21, SP21R, "2021-2024", "fundraising", r"invest in the continued growth of our fundraising program", "", "",
     r"Maintained fundraising staff positions \(\d+\) and expense budget; limited growth over period",
     "value = fundraising staff positions"),
    (SP21, None, "2021-2024", "funding mix", r"Seek new sources of funding, staying focused and strategic in funding our "
     r"work through a diversity of sources", "", "", None, "diversification goal, no numeric target"),
]


def norm_text(pdf: Path) -> str:
    t = plain_text(pdf).replace("‐", "-").replace("–", "-").replace("’", "'").replace("‐", "-")
    t = re.sub(r"\s+", " ", t)
    # the report table splits cells across columns; join the internal report's two-column rows
    return t


def first_num(s: str):
    """First number in the text that is not a year (2017, FY2026)."""
    for m in re.finditer(r"(?<![\w])(?:FY)?(\d[\d,]*(?:\.\d+)?)", s or ""):
        v = m.group(1).rstrip(",.")
        if re.fullmatch(r"(19|20)\d\d", v):
            continue
        return fmt(to_num(v))
    return ""


def extract_strategic(inv) -> tuple[list[dict], list[str]]:
    rows, warns, cache = [], [], {}

    def text(doc):
        if doc not in cache:
            cache[doc] = norm_text(INPUTS / doc)
        return cache[doc]
    for plan, rep, period, area, tpat, unit, tyear, rpat, note in STRAT:
        tt = rt = ""
        if plan and tpat:
            m = re.search(tpat.replace("’", "'"), text(plan), re.I)
            if m:
                tt = m.group(0).strip()
            else:
                warns.append(f"{plan}: target '{tpat[:40]}' not found")
        if rep and rpat:
            m = re.search(rpat, text(rep), re.I)
            if m:
                rt = m.group(0).strip(" ●")
            else:
                warns.append(f"{rep}: result '{rpat[:40]}' not found")
        rv = first_num(rt)
        if rt.startswith("Maintained 1:"):
            rv = first_num(rt.split(":", 1)[1])
        rows.append(dict(source_id=sid_for(inv, plan or rep), document=plan or rep, plan_period=period,
                         goal_area=area, target_text=tt, target_value=first_num(tt) if tt else "",
                         target_unit=unit, target_year=tyear, reported_result_text=rt, reported_value=rv,
                         notes="; ".join(x for x in (note, f"result from {sid_for(inv, rep)}" if rep and plan and rt
                                                     else "") if x)))
    return rows, warns


if __name__ == "__main__":
    main()
