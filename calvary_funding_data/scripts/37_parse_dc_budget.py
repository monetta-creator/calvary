"""Phase 4, area dc_hud: DC budget lines FY2021-FY2027 and dated budget/policy events.

Reads only raw files saved by scripts/14_probe_dc_hud.py:
  raw/dc_gov/*_cfo_budget_fy{2024..2027}_{AG}_*.pdf   DC CFO approved budget chapters + appendix tables
  raw/dc_council/*BR_FY2*.pdf                          Council committee budget reports, FY2027 change chart
  raw/dc_council/*bsa_FY*.html                         Budget Support Acts (D.C. Law Library full text)

Writes
  interim/stage_dc_budget_lines__dc.csv       one row per fiscal_year x stage x agency x line x fund type
  interim/stage_fact_policy_events__dc.csv    fact_policy_events staging rows (YoY changes, change-table items,
                                              Council adjustments, committee changes, BSA subtitles, report items)

Parse sources by book (see sources/catalog_parts/dc_hud.md):
  FY2024, FY2025, FY2027 books: appendix Schedule 30-PBB (activity x fund; clean text). FY2025 chapters are
    garbled (broken font map) except CF0, so FY2025 change items come from the readable narrative (pypdfium2).
  FY2026 book: chapter Table XX0-4 (activity, all funds) + XX0-2 (agency by fund). The FY2026 appendix is
    image-only and is not OCRed; FY2026 approved activity values also appear in the FY2027 30-PBB.
  Council committee reports: Mayor's proposed activity amounts (budget_stage 'proposed', whole dollars) and
    committee variances for in-scope codes; a short curated list of dated report items (anchor text verified
    on the cited page at run time). FY2027 Council Net Operating Budget Adjustments Chart: activity-level Council
    changes (word-position parse). BSA subtitles on homelessness, LRSP, RRH, DV, TANF and DHS/DBH grants.
Agencies: JA0 DHS, FO0 OVSJG, RM0 DBH, DB0 DHCD, HY0 Housing Authority Subsidy/Payment (LRSP), CF0 DOES,
HG0 DMHHS (ICH staff).
Budget-line repeats across books are kept once (latest book); FY2024 old-code rows stay alongside the FY2025
book's restated FY2024 column, and x_preferred=1 marks one consistent set per FY x stage x program code.

Usage: .venv/bin/python scripts/37_parse_dc_budget.py
"""
from __future__ import annotations

import csv
import hashlib
import html as htmlmod
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import INTERIM, RAW, log, rel, today  # noqa: E402
from lib.tagging import tag_text  # noqa: E402

RETRIEVED = today()
OUT_LINES = INTERIM / "stage_dc_budget_lines__dc.csv"
OUT_EVENTS = INTERIM / "stage_fact_policy_events__dc.csv"

AGENCIES = {
    "JA0": "Department of Human Services",
    "FO0": "Office of Victim Services and Justice Grants",
    "RM0": "Department of Behavioral Health",
    "DB0": "Department of Housing and Community Development",
    "HY0": "Housing Authority Subsidy/Payment (DCHA; Local Rent Supplement)",
    "CF0": "Department of Employment Services",
    "HG0": "Office of the Deputy Mayor for Health and Human Services (ICH staff)",
}
BOOK_FYS = (2024, 2025, 2026, 2027)

# Local Budget Act second-reading dates = Council approval of each FY budget (printed in the BSA texts,
# e.g. "Fiscal Year 2025 Local Budget Act of 2024, passed on 2nd reading on June 12, 2024").
# Mayor's proposed budget dates = BSA introduced "on behalf of the Mayor" (Council reports / BSA packet).
# BSA law effective dates are printed in the "Law Information" block of each bsa_*.html.
# These are re-read from the raw files at run time; the dict holds the parse results.
DATES: dict[str, dict[int, str]] = {"enacted": {}, "proposed": {}, "bsa_effective": {}}

IN_SCOPE = {
    "JA0": {"H03002", "H03003", "H03004", "H03007", "H03008", "H03009", "H03010", "H03011", "H03012",
            "H03013", "H03014", "H03015", "H03016", "H03014-H03016", "H03017", "H03018", "H03019",
            "H03022", "H03023", "HS0030"},
    "FO0": {"P02303", "P04502", "PS0023", "PS0045"},
    "RM0": {"H04308", "H04504"},
    "HY0": {"R03903", "R03904", "R03905", "R03906", "R03907", "EC0039"},
}
# FY2024 (old chart of accounts) -> FY2025+ codes. Activity-level unless noted. Verified against the FY2025
# book's restated FY2024 approved column (logged as crosswalk checks).
OLD2NEW = {
    "JA0": {"5037": "H03002", "5039": "H03003", "5038": "H03004", "5023": "H03009", "5020": "H03007",
            "5014": "H03008", "5035": "H03010", "5032": "H03011", "5034": "H03012", "5024": "H03013",
            "5013": "H03014-H03016", "5027": "H03019", "5028": "H03018", "5029": "H03017",
            "5026": "H03022", "5021": "H03023", "5000": "HS0030", "2000": "HS0029", "1000": "AMP000",
            "100F": "AFO000"},
    "FO0": {"4010": "P02303", "4020": "P02301", "6040": "P04502", "4000": "PS0023", "1000": "AMP000"},
    "RM0": {"6507": "H04308", "6940": "H04308", "6625": "H04504"},
    # HY0 FY2024 divisions correspond to FY2025 activities (6000 subtotal = R03905 restated, etc.)
    "HY0": {"6000": "R03905", "7000": "R03907", "2000": "R03906", "4000": "R03903", "5000": "R03904"},
}

CODE_RE = re.compile(r"^(?:[A-Z]{1,4}\d{1,5}[A-Z]?|\d{3}[0-9F]|NA)$")
NUM_RE = re.compile(r"^-?\d{1,3}(?:,\d{3})*$|^-?\d+$")
SPLIT_NUM_RE = re.compile(r"-?\d{1,3}(?:,\d{3})+|-?\d+")

TIE_LOG: list[str] = []
WARN: list[str] = []


# ---------------------------------------------------------------- helpers
def latest(pattern: str, folder: str = "dc_gov") -> list[Path]:
    """Newest copy per file suffix (after the timestamp) for a glob under raw/{folder}/."""
    best: dict[str, Path] = {}
    for p in sorted((RAW / folder).glob(pattern)):
        key = p.name.split("_", 1)[1]
        best[key] = p
    return sorted(best.values())


_text_cache: dict[tuple, list[str]] = {}


def pdf_text(path: Path, x_tol: float | None = None) -> list[str]:
    key = (str(path), x_tol)
    if key not in _text_cache:
        import pdfplumber
        out = []
        with pdfplumber.open(path) as pdf:
            for pg in pdf.pages:
                out.append((pg.extract_text(x_tolerance=x_tol) if x_tol else pg.extract_text()) or "")
        _text_cache[key] = out
    return _text_cache[key]


def pdfium_text(path: Path) -> list[str]:
    key = (str(path), "pdfium")
    if key not in _text_cache:
        import pypdfium2 as pdfium
        d = pdfium.PdfDocument(str(path))
        out = []
        for i in range(len(d)):
            try:
                out.append(d[i].get_textpage().get_text_range() or "")
            except Exception:
                out.append("")
        d.close()
        _text_cache[key] = out
    return _text_cache[key]


def to_int(tok: str) -> int | None:
    t = tok.replace(",", "").replace("$", "").strip()
    neg = t.startswith("(") and t.endswith(")")
    t = t.strip("()")
    if not re.fullmatch(r"-?\d+(\.\d+)?", t):
        return None
    v = float(t)
    return int(round(-v if neg else v))


def num_tokens(tokens: list[str]) -> list[str]:
    """Split run-together thousands-formatted numbers ('913,4921,029,008' -> '913,492', '1,029,008')."""
    out = []
    for t in tokens:
        if NUM_RE.match(t) or not re.fullmatch(r"-?[\d,]+", t):
            out.append(t)
        else:
            out.extend(SPLIT_NUM_RE.findall(t))
    return out


def clean_name(s: str) -> str:
    return " ".join(s.replace("–", "-").split()).strip(" -:")


def ev_id(*parts) -> str:
    return "dcpe_" + hashlib.sha1("|".join(str(p) for p in parts).encode()).hexdigest()[:12]


def fund_type_of(name: str) -> str:
    n = name.lower()
    if n.startswith("local"):
        return "local"
    if "federal" in n:
        return "federal"
    if n.startswith("gross") or n == "total":
        return "total"
    return "special"


# ---------------------------------------------------------------- dates from raw docs
def read_dates():
    for p in latest("*bsa_FY*.html", "dc_council"):
        m = re.search(r"bsa_FY(\d{4})", p.name)
        fy = int(m.group(1))
        t = htmlmod.unescape(re.sub(r"<[^>]+>", " ", p.read_text(encoding="utf-8", errors="ignore")))
        t = re.sub(r"\s+", " ", t)
        m = re.search(rf"Fiscal Year {fy} Local Budget Act of \d{{4}}, passed on 2nd reading on (\w+ \d+, \d{{4}})", t)
        if m:
            DATES["enacted"][fy] = iso(m.group(1))
        m = re.search(r"Law Information.*?Effective (\w+\.? \d+, \d{4})", t)
        if m:
            DATES["bsa_effective"][fy] = iso(m.group(1))
    # Mayor's proposed budget: BSA introduced on behalf of the Mayor
    pats = [("BR_FY25_Housing", r"On (April \d+, 2024), Chairman Phil Mendelson introduced, on behalf of the Mayor", 2025),
            ("BR_FY26_committee_budget_report_Housing", r"On (June \d+, 2025), Chairman Phil Mendelson introduced, on behalf of the Mayor", 2026),
            ("BR_FY27_bsa_committee_print_packet", r"(April \d+, 2026) Bill 26-661, the .Fiscal Year 2027 Budget Support Act of 2026. is\s+introduced", 2027)]
    for key, rx, fy in pats:
        for p in latest(f"*{key}*.pdf", "dc_council"):
            txt = " ".join(" ".join(pdfium_text(p)[:120]).split())
            m = re.search(rx, txt)
            if m:
                DATES["proposed"][fy] = iso(m.group(1))


def iso(s: str) -> str:
    import datetime as dt
    s = s.replace("Sept.", "Sep.").replace(".", "")
    for fmt in ("%B %d, %Y", "%b %d, %Y"):
        try:
            return dt.datetime.strptime(s, fmt).date().isoformat()
        except ValueError:
            pass
    return ""


# ---------------------------------------------------------------- budget-line row builder
LINES: list[dict] = []


def add_line(**kw):
    base = dict(fiscal_year="", budget_stage="", agency_code="", agency="", program_code="", activity_code="",
                line_item="", fund_type="", amount="", document="", page="", source_id="",
                retrieved_date=RETRIEVED, confidence="high", basis="documented", x_level="", x_fund_detail="",
                x_table="", x_book_fy="", x_code_fy2025="", x_division_code="", x_units_printed="thousands",
                x_in_scope="", x_tieout="", x_preferred="")
    base.update(kw)
    ag = base["agency_code"]
    base["agency"] = base["agency"] or AGENCIES.get(ag, "")
    pc = base["program_code"]
    base["x_in_scope"] = "1" if (ag in IN_SCOPE and pc in IN_SCOPE[ag]) or base["x_level"] == "agency" else ""
    LINES.append(base)
    return base


def stage_cols(book_fy: int) -> list[tuple[int, str]]:
    return [(book_fy - 3, "actual"), (book_fy - 2, "actual"), (book_fy - 1, "approved"), (book_fy, "approved")]


# ---------------------------------------------------------------- Schedule 30-PBB (FY2024, FY2025, FY2027 books)
BOILER = re.compile(r"Approved Budget|District of Columbia|^Name|Taxes\)|Financial Plan|^\(Dollars|Program Summary"
                    r"|^[A-Z]-\d+$|Congressional|^July 20|^Human Support|^Public Safety and|^Economic Development"
                    r"|^Operations and Infrastructure|^Governmental Direction|Activity 30-PBB|^Public Education System")


def parse_30pbb(path: Path, book_fy: int, ag: str):
    pages = pdf_text(path)
    hdr = " ".join(t for t in pages if "30-PBB" in t)
    nfund = 7 if re.search(r"Private\s+Enterprise", hdr) else 6
    K = 5 + nfund
    fund_names = (["Local", "Other (Dedicated Taxes/Special Purpose)", "General Fund (Local + Other)", "Federal",
                   "Private", "Intra-District"] if nfund == 6 else
                  ["Local", "Other (Dedicated Taxes/Special Purpose)", "General Fund (Local + Other)", "Federal",
                   "Private", "Enterprise and Other", "Intra-District"])
    new_style = book_fy >= 2026
    doc = rel(path)
    sid = f"doc_dc_budget_fy{book_fy}"
    recs = []  # (level, code, name, div_code, div_name, nums, page)
    div_code, div_name = "", ""
    pending = []  # FY2027 style: activities waiting for their subtotal
    unparsed = 0
    for pi, txt in enumerate(pages, 1):
        if "30-PBB" not in txt or not re.search(r"Local\s+Other\s+General", txt):
            continue
        for ln in txt.splitlines():
            s = ln.strip()
            if not s or BOILER.search(s):
                continue
            toks = num_tokens(s.split())
            k = 0
            while k < len(toks) and NUM_RE.match(toks[-1 - k]):
                k += 1
            if k >= K:
                nums = [to_int(t) for t in toks[-K:]]
                label = " ".join(toks[:-K])
                if label.startswith("Total:"):
                    recs.append(("agency", "", clean_name(label[6:]), "", "", nums, pi))
                elif label.startswith("Subtotal:"):
                    nm = clean_name(label[9:])
                    if new_style:
                        m = re.match(r"([A-Z]{1,4}\d{2,5}[A-Z]?)-(.*)", nm)
                        dcode, dname = (m.group(1), clean_name(m.group(2))) if m else ("", nm)
                        for r in pending:
                            recs.append(r[:3] + (dcode, dname) + r[5:])
                        pending = []
                        recs.append(("division", dcode, dname, dcode, dname, nums, pi))
                    else:
                        recs.append(("division", div_code, nm or div_name, div_code, nm or div_name, nums, pi))
                        div_code, div_name = "", ""
                elif not label:
                    r = ("activity", "", "(no activity name printed)", div_code, div_name, nums, pi)
                    (pending if new_style else recs).append(r)
                else:
                    if new_style:
                        m = re.match(r"([A-Z]{1,4}\d{2,5}[A-Z]?)-(.*)", label)
                        code, nm = (m.group(1), clean_name(m.group(2))) if m else ("", clean_name(label))
                        pending.append(("activity", code, nm, "", "", nums, pi))
                    else:
                        parts = label.split()
                        code = parts[-1] if CODE_RE.match(parts[-1]) else ""
                        nm = clean_name(" ".join(parts[:-1]) if code else label)
                        recs.append(("activity", code, nm, div_code, div_name, nums, pi))
            elif k < 3 and not new_style:
                parts = s.split()
                if re.search(r"\bFY 20\d\d\b.*\bChange\b", s):
                    continue  # schedule column header
                if len(parts) >= 2 and CODE_RE.match(parts[-1]) and not s.startswith(("Subtotal", "Total")):
                    div_code, div_name = parts[-1], clean_name(" ".join(parts[:-1]))
                elif len(parts) >= 2:
                    unparsed += 1
                    WARN.append(f"30-PBB FY{book_fy} {ag} p{pi}: unparsed text line '{s[:80]}'")
            elif k >= 3:
                unparsed += 1
                WARN.append(f"30-PBB FY{book_fy} {ag} p{pi}: {k} numbers (< {K}) '{s[:80]}'")
    if pending:
        for r in pending:
            recs.append(r)
        WARN.append(f"30-PBB FY{book_fy} {ag}: {len(pending)} activities without subtotal")
    # ---- tie-outs
    tie_rows = {}
    years = stage_cols(book_fy)
    acts_by_div = defaultdict(list)
    for r in recs:
        if r[0] == "activity":
            acts_by_div[r[3] or r[4]].append(r)
    divs = [r for r in recs if r[0] == "division"]
    for d in divs:
        acts = acts_by_div.get(d[3] or d[4], [])
        ok = True
        deltas = []
        for j in range(4):
            sm = sum(a[5][j] for a in acts)
            delta = sm - d[5][j]
            deltas.append(delta)
            if abs(delta) > max(2, len(acts)):
                ok = False
        res = "pass" if ok and acts else ("fail" if acts else "")
        if acts:
            TIE_LOG.append(f"FY{book_fy} {ag} 30-PBB p{d[6]} division {d[1] or d[4]}: sum of {len(acts)} activities vs "
                           f"subtotal, deltas by column {deltas} ($000) -> {res}")
        tie_rows[id(d)] = res
        for a in acts:
            tie_rows[id(a)] = res
    tot = [r for r in recs if r[0] == "agency"]
    for t in tot:
        deltas = [sum(d[5][j] for d in divs) - t[5][j] for j in range(4)]
        res = "pass" if all(abs(x) <= max(2, len(divs)) for x in deltas) else "fail"
        TIE_LOG.append(f"FY{book_fy} {ag} 30-PBB p{t[6]} agency total: sum of {len(divs)} division subtotals, deltas "
                       f"{deltas} ($000) -> {res}")
        tie_rows[id(t)] = res
    fund_fail = 0
    for r in recs:
        f = r[5][5:]
        gen_ok = abs(f[0] + f[1] - f[2]) <= 1
        tot_ok = abs(f[2] + sum(f[3:]) - r[5][3]) <= 2
        if not (gen_ok and tot_ok):
            fund_fail += 1
            WARN.append(f"30-PBB FY{book_fy} {ag} p{r[6]} {r[1]} {r[2][:40]}: fund split does not tie "
                        f"(local+other={f[0]+f[1]} vs general={f[2]}; funds={f[2]+sum(f[3:])} vs approved={r[5][3]})")
    TIE_LOG.append(f"FY{book_fy} {ag} 30-PBB fund split (local+other=general; general+federal+private+enterprise+"
                   f"intra = FY{book_fy} approved): {len(recs) - fund_fail}/{len(recs)} rows tie")
    # ---- emit rows
    for r in recs:
        level, code, name, dcode, dname, nums, pi = r
        mapped = OLD2NEW.get(ag, {}).get(code if level == "activity" else dcode, "") if book_fy == 2024 else ""
        if level == "division" and book_fy == 2024:
            mapped = OLD2NEW.get(ag, {}).get(dcode, "")
        if level == "activity":
            line_item, pcode, acode = name, (mapped or code), code
        elif level == "division":
            line_item, pcode, acode = f"SUBTOTAL: {dname}", (mapped or dcode), ""
        else:
            line_item, pcode, acode = "AGENCY TOTAL", "", ""
        common = dict(agency_code=ag, program_code=pcode, activity_code=acode, line_item=line_item, document=doc,
                      page=pi, source_id=sid, x_level=level, x_table="30-PBB", x_book_fy=book_fy,
                      x_code_fy2025=mapped, x_division_code=dcode, x_tieout=tie_rows.get(id(r), ""))
        for j, (fy, stage) in enumerate(years):
            add_line(fiscal_year=fy, budget_stage=stage, fund_type="total", amount=nums[j] * 1000,
                     x_fund_detail="Gross funds", **common)
        f = nums[5:]
        ftie = "pass" if (abs(f[0] + f[1] - f[2]) <= 1 and abs(f[2] + sum(f[3:]) - nums[3]) <= 2) else "fail"
        for fname, v in zip(fund_names, f):
            if "General Fund" in fname or not v:
                continue
            ft = "local" if fname == "Local" else ("federal" if fname == "Federal" else "special")
            c2 = dict(common)
            c2["x_tieout"] = ftie
            add_line(fiscal_year=book_fy, budget_stage="approved", fund_type=ft, amount=v * 1000,
                     x_fund_detail=fname, **c2)
    return recs


# ---------------------------------------------------------------- chapter Table XX0-4 (FY2026 book)
T4_ROW = re.compile(r"(SUBTOTAL\s*)?\(([A-Z]{1,4}\d{2,5}[A-Z]?|\d{3}[0-9F])\)\s*((?:(?!\([A-Z]{1,4}\d{2,5}[A-Z]?\)|"
                    r"\(\d{3}[0-9F]\)).)*?)\s+((?:-?[\d,]+|N/A)(?:\s+(?:-?[\d,.]+|N/A)){9})(?=\s|$)")
T4_TOTAL = re.compile(r"TOTAL\s*APPROVED\s*OPERATING\s*BUDGET\s+((?:-?[\d,]+|N/A)(?:\s+(?:-?[\d,.]+|N/A)){9})")


def parse_chapter_t4(path: Path, book_fy: int, ag: str, emit: bool = True):
    pages = pdf_text(path, x_tol=1)
    doc = rel(path)
    sid = f"doc_dc_budget_fy{book_fy}"
    chunks = []
    for pi, txt in enumerate(pages, 1):
        if not re.search(rf"Table\s*{ag}-4", txt):
            continue
        if re.search(rf"Table\s*{ag}-4\s+contains", txt) is None and not re.search(r"Division/Program\s*and\s*Activity", txt):
            continue
        keep = []
        started = False
        for ln in txt.splitlines():
            if re.search(r"Division/Program\s*and\s*Activity", ln):
                started = True
                continue
            if not started:
                continue
            if re.match(r"\(Change is calculated|Note:", ln):
                break
            keep.append(ln)
        chunks.append((pi, " ".join(keep)))
    recs = []
    for pi, txt in chunks:
        txt = " ".join(num_tokens(txt.split()))
        for m in T4_ROW.finditer(txt):
            sub, code, name, nums = m.groups()
            vals = nums.split()
            d = [to_int(v) if v != "N/A" else 0 for v in vals[:4]]
            recs.append(("division" if sub else "activity", code, clean_name(name), d, pi))
        m = T4_TOTAL.search(txt)
        if m:
            vals = m.group(1).split()
            recs.append(("agency", "", "AGENCY TOTAL", [to_int(v) for v in vals[:4]], pi))
    # assign activities to the following SUBTOTAL; tie-out
    out, buf, divs = [], [], []
    tie = {}
    for r in recs:
        if r[0] == "activity":
            buf.append(r)
        elif r[0] == "division":
            deltas = [sum(a[3][j] for a in buf) - r[3][j] for j in range(4)]
            res = "pass" if buf and all(abs(x) <= max(2, len(buf)) for x in deltas) else ("fail" if buf else "")
            if buf:
                TIE_LOG.append(f"FY{book_fy} {ag} Table {ag}-4 p{r[4]} division {r[1]}: sum of {len(buf)} activities "
                               f"vs subtotal, deltas {deltas} ($000) -> {res}")
            for a in buf:
                out.append((a, r[1], r[2]))
                tie[id(a)] = res
            tie[id(r)] = res
            out.append((r, r[1], r[2]))
            divs.append(r)
            buf = []
        else:
            deltas = [sum(d[3][j] for d in divs) - r[3][j] for j in range(4)]
            res = "pass" if all(abs(x) <= max(2, len(divs)) for x in deltas) else "fail"
            TIE_LOG.append(f"FY{book_fy} {ag} Table {ag}-4 p{r[4]} agency total: sum of {len(divs)} divisions, "
                           f"deltas {deltas} ($000) -> {res}")
            tie[id(r)] = res
            out.append((r, "", ""))
    for a in buf:
        out.append((a, "", ""))
        WARN.append(f"Table {ag}-4 FY{book_fy}: activity {a[1]} has no subtotal")
    if not emit:
        return out
    for r, dcode, dname in out:
        level, code, name, d, pi = r
        if level == "activity":
            li, pc, ac = name, code, code
        elif level == "division":
            li, pc, ac = f"SUBTOTAL: {name}", code, ""
        else:
            li, pc, ac = "AGENCY TOTAL", "", ""
        for j, (fy, stage) in enumerate(stage_cols(book_fy)):
            add_line(fiscal_year=fy, budget_stage=stage, agency_code=ag, program_code=pc, activity_code=ac,
                     line_item=li, fund_type="total", amount=d[j] * 1000, document=doc, page=pi, source_id=sid,
                     x_level=level, x_fund_detail="Gross funds", x_table=f"{ag}-4", x_book_fy=book_fy,
                     x_division_code=dcode, x_tieout=tie.get(id(r), ""))
    return out


# ---------------------------------------------------------------- chapter Table XX0-2 (agency by revenue type)
T2_FUNDS = ["LOCAL FUNDS", "LOCAL FUND", "DEDICATED TAXES", "SPECIAL PURPOSE REVENUE FUNDS", "FEDERAL PAYMENTS",
            "FEDERAL GRANT FUNDS", "FEDERAL GRANT FUND - FPR", "FEDERAL MEDICAID PAYMENTS", "PRIVATE GRANT FUNDS",
            "PRIVATE GRANT FUND -FPR", "PRIVATE DONATIONS", "PRIVATE DONATIONS -FPR", "INTRA-DISTRICT FUNDS",
            "ENTERPRISE AND OTHER FUNDS", "GROSS FUNDS"]


def squash(s: str) -> str:
    return re.sub(r"[^A-Z]", "", s.upper().replace("&", "AND")).replace("SUPPLEMNT", "SUPPLEMENT")


T2_KEYS = {squash(f): f for f in T2_FUNDS}


def parse_chapter_t2(path: Path, book_fy: int, ag: str):
    pages = pdf_text(path, x_tol=1)
    doc = rel(path)
    sid = f"doc_dc_budget_fy{book_fy}"
    rows = []
    for pi, txt in enumerate(pages, 1):
        if not re.search(rf"Table\s*{ag}-2\b", txt) or not re.search(r"Appropriated\s*Fund", txt):
            continue
        seg = txt.split("Appropriated")[1] if "Appropriated" in txt else txt
        seg = re.split(r"\*\s*Percent\s*change", seg)[0]
        lines = seg.splitlines()[1:]
        acc = ""
        for ln in lines:
            toks = num_tokens(ln.split())
            k = 0
            while k < len(toks) and re.fullmatch(r"-?[\d,.]+|N/A", toks[-1 - k]):
                k += 1
            label = (acc + " " + " ".join(toks[:len(toks) - k])).strip()
            if k >= 6:
                key = squash(label)
                acc = ""
                changed = True
                while key not in T2_KEYS and changed:
                    changed = False
                    for pre in ("GENERALFUND", "FEDERALRESOURCES", "PRIVATEFUNDS", "INTRADISTRICTFUNDS",
                                "ENTERPRISEANDOTHERFUNDS", "APPROPRIATEDFUND"):
                        if key.startswith(pre) and key != pre:
                            key = key[len(pre):]
                            changed = True
                if key in T2_KEYS or re.match(r"(LOCAL|DEDICATED|SPECIALPURPOSE|FEDERAL|PRIVATE|INTRADISTRICT|"
                                                r"ENTERPRISE)", key):
                    vals = [to_int(t) for t in toks[len(toks) - k:][:4]]
                    nm = T2_KEYS.get(key) or re.sub(r"([a-z])([A-Z])", r"\1 \2", label.split(")")[-1]).upper()
                    rows.append((" ".join(nm.split()), vals, pi))
            else:
                acc = label
        break
    if not rows:
        WARN.append(f"Table {ag}-2 FY{book_fy}: not parsed ({path.name})")
        return []
    gross = [r for r in rows if r[0] == "GROSS FUNDS"]
    comps = [r for r in rows if r[0] != "GROSS FUNDS"]
    res = ""
    if gross:
        deltas = [sum(c[1][j] for c in comps) - gross[0][1][j] for j in range(4)]
        res = "pass" if all(abs(x) <= max(2, len(comps)) for x in deltas) else "fail"
        TIE_LOG.append(f"FY{book_fy} {ag} Table {ag}-2 p{gross[0][2]}: sum of {len(comps)} fund rows vs GROSS FUNDS, "
                       f"deltas {deltas} ($000) -> {res}")
    out = []
    for name, vals, pi in rows:
        for j, (fy, stage) in enumerate(stage_cols(book_fy)):
            if not vals[j] and name != "GROSS FUNDS":
                continue
            out.append(dict(fiscal_year=fy, budget_stage=stage, agency_code=ag, line_item="AGENCY TOTAL",
                            fund_type=fund_type_of(name), amount=vals[j] * 1000, document=doc, page=pi, source_id=sid,
                            x_level="agency", x_fund_detail=name.title().replace("Fpr", "FPR"), x_table=f"{ag}-2",
                            x_book_fy=book_fy, x_tieout=res))
    return out


# ---------------------------------------------------------------- event rows
EVENTS: list[dict] = []
STRICT_KW = re.compile(r"homeless|shelter|\bPSH\b|supportive housing|rapid re-?housing|rehousing|FRSP|ERAP|"
                       r"emergency rental|victim services|crime victim|victims? of (?:crime|domestic)|"
                       r"domestic violence|\bDV\b|voucher|LRSP|rent supplement|drop-in|"
                       r"Interagency Council|\bICH\b|DC Flex|\bTAH\b|STFH|\bHPP\b|transitional housing", re.I)
SCOPE_DIVS = {"JA0": {"FAMILYSERVICES"}, "FO0": {"VICTIMSERVICES"}, "HY0": None}  # None = all items


def add_event(**kw):
    base = dict(event_id="", event_date="", event_type="", jurisdiction="DC", agency="", program_code="",
                funding_stream="", description="", amount="", prior_amount="", amount_change="", fiscal_year="",
                program_area_tags="", source_id="", source_page="", confidence="high", basis="documented",
                retrieved_date=RETRIEVED, x_agency_code="", x_document="", x_record_kind="", x_date_basis="",
                x_fy26="", x_fy28="", x_fy29="", x_fy30="", x_fte="", x_scenario="", x_amounts_mentioned="")
    base.update(kw)
    if not base["agency"] and base["x_agency_code"]:
        base["agency"] = AGENCIES.get(base["x_agency_code"], base["x_agency_code"])
    base["program_area_tags"] = base["program_area_tags"] or tag_text(base["description"])
    base["event_id"] = ev_id(base["x_record_kind"], base["fiscal_year"], base["x_agency_code"], base["program_code"],
                             base["funding_stream"], base["description"][:160], base["amount_change"],
                             base["source_page"], base["x_document"])
    EVENTS.append(base)


def date_for(kind: str, fy: int) -> tuple[str, str]:
    if kind == "proposed":
        d = DATES["proposed"].get(fy, "")
        return d, ("BSA introduced on behalf of the Mayor (proposed budget transmittal)" if d else
                   "proposal date not printed in downloaded documents")
    d = DATES["enacted"].get(fy, "")
    return d, "Local Budget Act passed on 2nd reading (Council approval)"


# ---------------------------------------------------------------- chapter Table XX0-5 (budget change items)
T5_ITEM = re.compile(r"^(?P<text>.*?)\s+(?P<amt>-?[\d,]+)\s+(?P<fte>-?\d+\.\d)$")
T5_HDR = re.compile(r"^(?P<fund>[A-Z][A-Z \-/&'.]*?)\s*:\s*FY\s*(?P<fy>20\d\d)\s+(?P<what>.*?)\s+-?[\d,]+\s+-?\d+\.\d$")
FOOTER = re.compile(r"Approved Budget and Financial Plan|^[A-Z]-\d+$|^\(dollars in thousands\)|^Table [A-Z]{2}0-5", re.I)
T5_VERB = re.compile(r"^(Increase|Decrease|Enhance|Reduce|Transfer|Removal|Eliminate|Shift|Technical|Correct|"
                     r"No Change|Enhance/Reduce|Create)", re.I)


def match_division(main: str, cont: str, divs: dict[str, str]) -> tuple[str, str, str, str]:
    """Return (text_without_division, division_name, division_code, leftover_continuation)."""
    sm = squash(main)
    for key in sorted(divs, key=len, reverse=True):
        if sm.endswith(key):
            # strip the division words from the end of main
            n = 0
            words = main.split()
            for i in range(len(words), 0, -1):
                if squash(" ".join(words[i - 1:])) == key:
                    n = i - 1
                    break
            return " ".join(words[:n]), key, divs[key], cont
    for key in sorted(divs, key=len, reverse=True):
        for cut in range(len(key) - 1, 5, -1):
            if sm.endswith(key[:cut]) and squash(cont).startswith(key[cut:]):
                words = main.split()
                for i in range(len(words), 0, -1):
                    if squash(" ".join(words[i - 1:])) == key[:cut]:
                        rest = cont.split()
                        j = 0
                        while j < len(rest) and squash(" ".join(rest[:j + 1])) and key[cut:].startswith(squash(" ".join(rest[:j + 1]))):
                            j += 1
                        return " ".join(words[:i - 1]), key, divs[key], " ".join(rest[j:])
    return main, "", "", cont


DIVNAME: dict[str, str] = {"MULTIPLEPROGRAMS": "Multiple Programs"}


def parse_chapter_t5(path: Path, book_fy: int, ag: str, divs: dict[str, str]):
    pages = pdf_text(path, x_tol=1)
    items, fund, phase = [], "", ""
    for pi, txt in enumerate(pages, 1):
        if not re.search(rf"Table\s*{ag}-5\b", txt) or "DESCRIPTION" not in txt.upper():
            continue
        started = False
        for ln in txt.splitlines():
            s = " ".join(ln.split())
            if re.match(r"DESCRIPTION\s+DIVISION", s, re.I):
                started = True
                continue
            if not started or not s:
                continue
            if re.match(r"GROSS\s*FOR|\(Change is calculated|Note:", s, re.I):
                started = False
                break
            h = T5_HDR.match(s)
            if h:
                fund = clean_name(h.group("fund")).title()
                w = squash(h.group("what"))
                phase = ("council" if "MAYORSPROPOSED" in w else "done" if "DISTRICTSAPPROVED" in w else "proposed")
                continue
            m = T5_ITEM.match(s)
            if m and T5_VERB.match(m.group("text")):
                if m.group("text").lower().startswith("no change"):
                    continue
                items.append(dict(main=m.group("text"), cont="", amt=to_int(m.group("amt")), fte=m.group("fte"),
                                  fund=fund, phase=phase, page=pi))
            elif items and items[-1]["page"] == pi and not T5_VERB.match(s) and not FOOTER.search(s):
                items[-1]["cont"] = (items[-1]["cont"] + " " + s).strip()
    doc = rel(path)
    sid = f"doc_dc_budget_fy{book_fy}"
    kept = 0
    for it in items:
        text, dkey, dcode, cont = match_division(it["main"], it["cont"], divs)
        desc = clean_name(f"{text} {cont}")
        scope = SCOPE_DIVS.get(ag, set())
        in_scope = (scope is None) or (dkey in (scope or set())) or bool(STRICT_KW.search(desc))
        if not in_scope:
            continue
        if book_fy == 2027 and it["phase"] == "council":
            continue  # FY2027 Council-level changes are taken at activity level from the Council adjustments chart
        kind = "proposed" if it["phase"] == "proposed" else "enacted"
        d, basis = date_for(kind, book_fy)
        divname = DIVNAME.get(dkey, dkey.title())
        add_event(event_date=d, event_type="budget_proposed" if kind == "proposed" else "budget_revised",
                  x_agency_code=ag, program_code=dcode, funding_stream=it["fund"],
                  description=f"{desc} [division: {divname if dkey else 'not stated'}; "
                              f"{'Mayor proposed change' if kind == 'proposed' else 'Council change to Mayor proposal'}]",
                  amount_change=it["amt"] * 1000 if it["amt"] is not None else "", fiscal_year=book_fy,
                  source_id=sid, source_page=it["page"], x_document=doc,
                  x_record_kind=f"change_table_{ag}-5", x_date_basis=basis, x_fte=it["fte"],
                  confidence="high" if d else "medium")
        kept += 1
    return len(items), kept


# ---------------------------------------------------------------- FY2025 narrative change sentences (pypdfium2)
AMT_RE = re.compile(r"\$\s?([\d,]+(?:\.\d+)?)\s*(million|m\b)?", re.I)
NEG_RE = re.compile(r"\b(decrease|reduc|cut|eliminat|savings|offset by)\w*", re.I)


def parse_fy2025_narrative(path: Path, ag: str):
    pages = pdfium_text(path)
    doc = rel(path)
    start = next((i for i, t in enumerate(pages) if re.search(r"Mayor.s Proposed Budget", t)
                  and re.search(r"Increase:|Decrease:|Enhance:|Reduce:", t)), None)
    if start is None:
        return 0
    n = 0
    phase = "proposed"
    for i in range(start, len(pages)):
        t = pages[i]
        if i > start and re.search(rf"Table {ag}-7|Agency Performance Plan", t) and not re.search(r"\$\d", t):
            break
        if i == start:
            t = t[t.find("Proposed Budget"):]
        parts = re.split(r"(District.s Approved Budget)", t)
        for part in parts:
            if re.fullmatch(r"District.s Approved Budget", part):
                phase = "council"
                continue
            part = "\n".join(ln for ln in part.replace("\r", "\n").split("\n") if not FOOTER.search(ln.strip()))
            flat = " ".join(part.split())
            for s in re.split(r"(?<=\.)\s+(?=[A-Z])", flat):
                if "$" not in s or not STRICT_KW.search(s) or len(s) > 700:
                    continue
                if sum(ch.isalpha() for ch in s) < 0.6 * len(s):
                    continue  # garbled (font-mapped) fragment
                m = AMT_RE.search(s)
                if not m:
                    continue
                val = float(m.group(1).replace(",", "")) * (1e6 if m.group(2) else 1)
                sign = -1 if NEG_RE.search(s[:m.start()]) else 1
                kind = "proposed" if phase == "proposed" else "enacted"
                d, basis = date_for(kind, 2025)
                add_event(event_date=d, event_type="budget_proposed" if kind == "proposed" else "budget_revised",
                          x_agency_code=ag, description=clean_name(s)[:400], amount_change=int(round(sign * val)),
                          fiscal_year=2025, source_id="doc_dc_budget_fy2025", source_page=i + 1, x_document=doc,
                          x_record_kind="fy2025_change_narrative", x_date_basis=basis,
                          x_amounts_mentioned="; ".join(a.group(0) for a in AMT_RE.finditer(s)),
                          confidence="medium")
                n += 1
    return n


# ---------------------------------------------------------------- FY2027 Council Net Operating Budget Adjustments Chart
CHART_COLS = ["agency", "scenario", "appr_fund", "fund", "program", "costctr", "account", "comments"]
NUMTOK = re.compile(r"^\(?-?[\d,]+\)?$")


def parse_council_chart(path: Path):
    import pdfplumber
    doc = rel(path)
    state = {c: "" for c in CHART_COLS}
    out = []
    with pdfplumber.open(path) as pdf:
        for pi, pg in enumerate(pdf.pages, 1):
            ws = pg.extract_words(x_tolerance=1.5)
            hdr = [w for w in ws if 85 < w["top"] < 108]
            hx = {}
            difs = sorted(w["x0"] for w in hdr if w["text"] == "DIFS")
            for w in hdr:
                if w["text"] in ("Agency", "Scenario", "Comments", "FY26", "FY27", "FY28", "FY29", "FY30"):
                    hx[w["text"]] = w
            fte = [w for w in ws if w["text"] == "FTEs" and w["top"] < 110]
            if len(difs) < 5 or "Comments" not in hx or "FY27" not in hx:
                continue
            bounds = [hx["Agency"]["x0"] - 5, hx["Scenario"]["x0"] - 2] + [x - 2 for x in difs[:5]] + \
                     [hx["Comments"]["x0"] - 2, hx["FY26"]["x0"] - 20]
            numcols = [("FY26", hx["FY26"]["x1"]), ("FY27", hx["FY27"]["x1"]), ("FY28", hx["FY28"]["x1"]),
                       ("FY29", hx["FY29"]["x1"]), ("FY30", hx["FY30"]["x1"])]
            if fte:
                numcols.append(("FTE", fte[0]["x1"]))
            body = [w for w in ws if 108 < w["top"] < pg.height - 40]
            # anchor lines = lines with numbers in the amount columns
            anchors = []
            for w in body:
                if w["x0"] >= bounds[-1] and NUMTOK.match(w["text"]):
                    if anchors and abs(anchors[-1][0] - w["top"]) < 4:
                        anchors[-1][1].append(w)
                    else:
                        anchors.append([w["top"], [w]])
            anchors.sort(key=lambda a: a[0])
            if not anchors:
                continue
            tops = [a[0] for a in anchors]
            mids = [(tops[k] + tops[k + 1]) / 2 for k in range(len(tops) - 1)]
            bands = [[] for _ in anchors]
            for w in body:
                if w["x0"] >= bounds[-1]:
                    continue
                k = sum(1 for m in mids if w["top"] > m)
                bands[k].append(w)
            for k, (top, nums) in enumerate(anchors):
                cols = {c: [] for c in CHART_COLS}
                for w in sorted(bands[k], key=lambda w: (round(w["top"]), w["x0"])):
                    ci = max(0, min(len(CHART_COLS) - 1, sum(1 for b in bounds[1:-1] if w["x0"] >= b)))
                    cols[CHART_COLS[ci]].append(w["text"])
                txt = {c: " ".join(v) for c, v in cols.items()}
                vals = {}
                for w in nums:
                    name = min(numcols, key=lambda nc: abs(nc[1] - w["x1"]))[0]
                    vals[name] = to_int(w["text"])
                is_total = any("Total" in txt[c] for c in ("agency", "scenario", "appr_fund"))
                if is_total:
                    continue
                # forward-fill: agency/scenario/fund columns update when printed; a newly printed program,
                # cost center or account replaces that level and everything below it with this band's text
                for c in ("agency", "scenario", "appr_fund", "fund"):
                    if txt[c]:
                        state[c] = txt[c]
                low = ["program", "costctr", "account"]
                for li, c in enumerate(low):
                    if txt[c]:
                        for c2 in low[li:]:
                            state[c2] = txt[c2]
                        break
                rec = dict(state)
                rec["comments"] = txt["comments"]
                rec.update(vals)
                rec["page"] = pi
                out.append(rec)
    rows = 0
    in_scope_codes = set().union(*IN_SCOPE.values())
    for r in out:
        m = re.search(r"\(([A-Z]{2}0)\)", r["costctr"]) or re.search(r"\(([A-Z]{2}0)\)", r["program"] + r["account"])
        ag = m.group(1) if m else ""
        if ag not in AGENCIES:
            continue
        pm = re.match(r"([A-Z]{1,4}\d{2,5}[A-Z]?)\s*-\s*(.*)", r["program"])
        pcode, pname = (pm.group(1), clean_name(pm.group(2))) if pm else ("", clean_name(r["program"]))
        comment = clean_name(r["comments"])
        if not (pcode in in_scope_codes or ag == "HY0" or STRICT_KW.search(comment)):
            continue
        d, basis = date_for("enacted", 2027)
        scen = clean_name(r["scenario"])
        add_event(event_date=d, event_type="budget_revised", x_agency_code=ag, program_code=pcode,
                  funding_stream=clean_name(r["appr_fund"]).title(),
                  description=f"{comment} [{pcode} {pname}; {scen}]", amount_change=r.get("FY27", ""),
                  fiscal_year=2027, source_id="doc_dc_council_budget_reports", source_page=r["page"],
                  x_document=doc, x_record_kind="council_adjustments_chart_fy2027", x_date_basis=basis,
                  x_fy26=r.get("FY26", ""), x_fy28=r.get("FY28", ""), x_fy29=r.get("FY29", ""),
                  x_fy30=r.get("FY30", ""), x_fte=r.get("FTE", ""), x_scenario=scen)
        rows += 1
    return len(out), rows


# ---------------------------------------------------------------- Council committee report tables (Mayor's proposed)
CAMT = r"\(?\$\s?\(?[\d,]+\)?\)?|\$\s?-"
CROW = re.compile(rf"\b([A-Z]{{1,3}}\d{{4,5}}) - ((?:(?!\$|\b[A-Z]{{1,3}}\d{{4,5}} - |\b\d{{6}} - ).){{2,120}}?)\s*({CAMT})"
                  rf"\s+({CAMT})\s+({CAMT})\s+({CAMT})\s+({CAMT})")
# two-level tables (program parent L1 header, child activities, then a program total line)
CROW2 = re.compile(rf"\b([A-Z]{{1,3}}\d{{4,5}}) - ((?:(?!\$|\b[A-Z]{{1,3}}\d{{4,5}} - ).){{2,80}}?)\s+\d{{6}} - "
                   rf"(?:(?!\b[A-Z]{{1,3}}\d{{4,5}} - ).)*?TOTAL PROGRAM PARENT L1 FUNDS\s+({CAMT})\s+({CAMT})\s+({CAMT})"
                   rf"\s+({CAMT})\s+({CAMT})")
CODE_AGENCY = [(re.compile(r"^H030\d\d$"), "JA0"), (re.compile(r"^P0(23|45)\d\d$"), "FO0"),
               (re.compile(r"^H04(308|504)$"), "RM0"), (re.compile(r"^R039\d\d$"), "HY0")]
MARKUP: dict[str, str] = {}


def camt(s: str) -> int:
    s = s.replace(" ", "")
    if re.fullmatch(r"\$-", s):
        return 0
    neg = "(" in s
    v = int(re.sub(r"[^\d]", "", s) or 0)
    return -v if neg else v


def parse_committee_tables(path: Path, fy: int, committee: str):
    pages = pdfium_text(path)
    doc = rel(path)
    flat_all = " ".join(" ".join(t.split()) for t in pages)
    m = re.search(r"(?:COMMITTEE ACTION AND VOTE|Committee Action(?: and Vote)?)\s+On (?:[A-Z][a-z]+day, )?"
                  r"([A-Z][a-z]+ \d{1,2})(?:st|nd|rd|th)?, (20\d\d)", flat_all)
    MARKUP[path.name] = iso(f"{m.group(1)}, {m.group(2)}") if m else ""
    found = {}
    for pi, t in enumerate(pages, 1):
        flat = " ".join(t.replace("￾", "-").split())
        for mm in list(CROW2.finditer(flat)) + list(CROW.finditer(flat)):
            code, name = mm.group(1), clean_name(mm.group(2))
            ag = next((a for rx, a in CODE_AGENCY if rx.match(code)), "")
            if not ag or code not in IN_SCOPE.get(ag, set()):
                continue
            a = [camt(mm.group(k)) for k in range(3, 8)]
            if abs(a[2] + a[3] - a[4]) > 2:
                continue  # not the [actual, approved, proposed, variance, committee] layout
            if code in found:
                continue  # first table occurrence only (later attachments repeat it)
            found[code] = (ag, name, a, pi)
    for code, (ag, name, a, pi) in found.items():
        add_line(fiscal_year=fy, budget_stage="proposed", agency_code=ag, program_code=code, activity_code=code,
                 line_item=name, fund_type="total", amount=a[2], document=doc, page=pi,
                 source_id="doc_dc_council_budget_reports", x_level="activity", x_fund_detail="Gross funds",
                 x_table=f"Committee on {committee} report: agency operating budget by program", x_book_fy=fy,
                 x_units_printed="dollars", x_tieout="pass")
        if a[3] and fy < 2027:
            d = MARKUP.get(path.name) or DATES["enacted"].get(fy, "")
            add_event(event_date=d, event_type="budget_revised", x_agency_code=ag, program_code=code,
                      funding_stream="all funds",
                      description=f"Committee on {committee} recommended change to the Mayor's proposed FY{fy} budget "
                                  f"for {code} {name}",
                      amount=a[4], prior_amount=a[2], amount_change=a[3], fiscal_year=fy,
                      source_id="doc_dc_council_budget_reports", source_page=pi, x_document=doc,
                      x_record_kind="committee_report_variance", basis="documented",
                      x_date_basis="committee markup date" if MARKUP.get(path.name) else
                      "markup date not printed; Local Budget Act 2nd reading used",
                      confidence="high" if MARKUP.get(path.name) else "medium")
    return len(found)


# ---------------------------------------------------------------- Budget Support Act subtitles
BSA_KEEP = re.compile(r"HOMELESS|SHELTER|EMERGENCY HOUSING|RENT SUPPLEMENT|LRSP|RAPID RE-?HOUSING|REHOUSING|VICTIM|"
                      r"DOMESTIC VIOLENCE|HUMAN SERVICES|TANF|TARGETED OUTREACH|EMERGENCY RENTAL|CCNV|"
                      r"INTERAGENCY COUNCIL|PERMANENT SUPPORTIVE|PUBLIC HOUSING STABILITY")
BSA_AGENCY = [(re.compile(r"RENT SUPPLEMENT|LRSP|PUBLIC HOUSING"), "HY0"),
              (re.compile(r"BEHAVIORAL HEALTH|TARGETED OUTREACH"), "RM0"),
              (re.compile(r"VICTIMS OF DOMESTIC VIOLENCE FUND"), "DB0"),
              (re.compile(r"EMERGENCY HOUSING ASSISTANCE PROGRAM"), "OTA"),
              (re.compile(r"HUMAN SERVICES|TANF|RAPID|REHOUSING|SHELTER|CCNV|EMERGENCY RENTAL|HOMELESS"), "JA0")]


def strip_tags(s: str) -> str:
    return " ".join(htmlmod.unescape(re.sub(r"<[^>]+>", " ", s)).split())


def parse_bsa():
    n = 0
    for p in latest("*bsa_FY*.html", "dc_council"):
        fy = int(re.search(r"bsa_FY(\d{4})", p.name).group(1))
        t = p.read_text(encoding="utf-8", errors="ignore")
        law = strip_tags(re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S).group(1)).split(". Fiscal")[0]
        heads = list(re.finditer(r"<h([12])[^>]*>(.*?)</h\1>", t, re.S))
        title = ""
        for k, h in enumerate(heads):
            name = strip_tags(h.group(2))
            if h.group(1) == "1":
                title = name if name.startswith("TITLE") else title
                continue
            if not BSA_KEEP.search(name):
                continue
            body = strip_tags(t[h.end(): heads[k + 1].start() if k + 1 < len(heads) else len(t)])
            short = re.search(r"may be cited as the \"([^\"]+)\"", body)
            after = body[short.end():] if short else body
            after = re.sub(r"^\s*\.?\s*", "", after)
            sents = re.split(r"(?<=[.:])\s+(?=Sec\.|\(|[A-Z])", after)
            excerpt = " ".join(sents[:3])[:420]
            amts = sorted({a.group(0) for a in AMT_RE.finditer(body)}, key=body.find)
            amount = ""
            if len(amts) == 1:
                m = AMT_RE.match(amts[0])
                amount = int(round(float(m.group(1).replace(",", "")) * (1e6 if m.group(2) else 1))) or ""
            ag = next((a for rx, a in BSA_AGENCY if rx.search(name)), "")
            sub = name.split(".")[0].replace("SUBTITLE ", "")
            title_no = title.split(".")[0].replace("TITLE ", "")
            et = "program_launch" if re.search(r"\bPILOT\b|ESTABLISH", name) else "policy_change"
            add_event(event_date=DATES["bsa_effective"].get(fy, ""), event_type=et, x_agency_code=ag,
                      agency=AGENCIES.get(ag, "Office of the Tenant Advocate" if ag == "OTA" else ""),
                      description=clean_name(f"FY{fy} Budget Support Act ({law}), Title {title_no} Subtitle {sub} "
                                             f"'{name.split('. ', 1)[-1].title()}'"
                                             + (f" (cited as \"{short.group(1)}\")" if short else "")
                                             + f": {excerpt}"),
                      amount=amount, fiscal_year=fy, source_id="doc_dc_bsa",
                      source_page=f"Title {title_no}, Subtitle {sub}", x_document=rel(p),
                      x_record_kind="bsa_subtitle", x_date_basis="BSA law/act effective date (Law Information block)",
                      x_amounts_mentioned="; ".join(amts[:12]), confidence="high" if not amount else "medium")
            n += 1
    return n


# ---------------------------------------------------------------- curated committee-report items
# (report file key, PDF page, anchor text that must appear on that page, event_type, fiscal_year, agency,
#  program_code, factual description, amount, prior_amount, amount_change, date rule)
CURATED = [
    ("BR_FY25_Housing", 4, "$6.9 million boost in the Emergency Rental Assistance Program", "budget_revised", 2025,
     "JA0", "H03008", "Committee on Housing FY2025 recommendation: +$6.9 million for the Emergency Rental Assistance "
     "Program (ERAP), with transparency and program-reform requirements", "", "", 6_900_000, "markup"),
    ("BR_FY25_Housing", 4, "43 more residents with unmet needs to move into permanent supportive housing", "budget_revised",
     2025, "JA0", "H03012", "Committee on Housing FY2025 recommendation: $1.2 million so 43 more residents can move into "
     "permanent supportive housing", "", "", 1_200_000, "markup"),
    ("BR_FY25_Housing", 4, "homelessness prevention services to more residents in precarious living situations with a $1.8",
     "budget_revised", 2025, "JA0", "H03014-H03016", "Committee on Housing FY2025 recommendation: $1.8 million "
     "enhancement to extend homelessness prevention services", "", "", 1_800_000, "markup"),
    ("BR_FY25_Housing", 4, "funding 66 housing vouchers in the amount of $1.9 million", "budget_revised", 2025, "", "",
     "Committee on Housing FY2025 recommendation: $1.9 million for 66 housing vouchers for families exiting Rapid "
     "Rehousing", "", "", 1_900_000, "markup"),
    ("BR_FY25_Housing", 4, "Boosts the Street Outreach program", "budget_revised", 2025, "JA0", "H03004",
     "Committee on Housing FY2025 recommendation: $2 million for the DHS Street Outreach program", "", "", 2_000_000,
     "markup"),
    ("BR_FY25_Housing", 102, "$500,000 increase in domestic violence services at DHS", "budget_revised", 2025, "JA0",
     "H03007", "Committee on Housing FY2025 recommendation: $500,000 increase for DHS domestic violence services", "", "",
     500_000, "markup"),
    ("BR_FY25_JPS", 68, "The Mayor’s proposed FY 2025 operating budget for OVSJG is $78,995,940", "budget_proposed", 2025,
     "FO0", "", "Mayor's proposed FY2025 OVSJG operating budget $78,995,940 (24.7% below FY2024 approved), including an "
     "apparent $2.7 million reduction to Victim Services and elimination of Safe Housing for Gun Violence after ARPA "
     "funds ended", 78_995_940, "", "", "proposed"),
    ("BR_FY25_JPS", 71, "erroneously included $6.538 million", "budget_proposed", 2025, "FO0", "PS0023",
     "OVSJG FY2025 proposal erroneously included $6.538 million of already-spent federal VOCA funds, so proposed Victim "
     "Services funding was a $2.7 million decrease from FY2024", "", "", -2_700_000, "proposed"),
    ("BR_FY25_JPS", 71, "increases (800144) Victim Services by $1,000,000", "budget_revised", 2025, "FO0", "PS0023",
     "Committee on the Judiciary and Public Safety FY2025 recommendation: +$1,000,000 one-time for Victim Services "
     "(incl. $500,000 transfer for domestic violence services)", "", "", 1_000_000, "markup"),
    ("BR_FY26_committee_budget_report_Human-Services", 35, "from $2,488,397 to $1,988,397", "budget_proposed", 2026,
     "JA0", "H03007", "Mayor's proposed FY2026 budget reduced locally funded DHS Domestic Violence Services grants by "
     "$500,000, from $2,488,397 to $1,988,397", 1_988_397, 2_488_397, -500_000, "proposed"),
    ("BR_FY26_committee_budget_report_Human-Services", 36, "imposing a $930,545 cut", "budget_proposed", 2026, "JA0",
     "H03013", "Mayor's proposed FY2026 budget cut Permanent Supportive Housing Youth (extended transitional housing) "
     "from $3,778,914 to $2,848,369", 2_848_369, 3_778_914, -930_545, "proposed"),
    ("BR_FY26_committee_budget_report_Human-Services", 62, "exceeding FRSP’s approved budget of $60,116,101", "other",
     2025, "JA0", "H03017", "DHS projected about $134,000,000 FY2025 spending on the Family Re-housing Stabilization "
     "Program (FRSP), exceeding its approved budget of $60,116,101 by $73,923,302", "", 60_116_101, 73_923_302,
     "report"),
    ("BR_FY26_committee_budget_report_Human-Services", 63, "$47,300,000 cash infusion", "budget_revised", 2025, "JA0",
     "H03017", "FY2025 FRSP spending required a $47,300,000 cash infusion; FRSP spending rose 252 percent from "
     "$53,096,120 in FY2024", "", "", 47_300_000, "report"),
    ("BR_FY26_committee_budget_report_Human-Services", 69, "$23,652,388 in savings over the four-year financial plan",
     "policy_change", 2026, "JA0", "H03017", "FY2026 BSA rapid re-housing subtitle restricts FRSP case management to "
     "non-TANF households and makes it optional; OCFO projects $23,652,388 savings over four years ($9,115,983 in FY2026)",
     "", "", -9_115_983, "bsa"),
    ("BR_FY26_committee_budget_report_Human-Services", 4, "Human Services Grant Administration Amendment Act",
     "policy_change", 2026, "JA0", "", "Committee on Human Services proposed and funded the Human Services Grant "
     "Administration Amendment Act of 2025 requiring DHS to process grants and payments faster after delayed payments "
     "put youth homelessness providers at risk", "", "", "", "bsa"),
    ("BR_FY26_committee_budget_report_JPS", 108, "decreases (PS02303) Victim Services grants by", "budget_proposed",
     2026, "FO0", "P02303", "Mayor's proposed FY2026 budget decreased OVSJG Victim Services grants by $5,842,000 to a "
     "total of $50,079,000", 50_079_000, "", -5_842_000, "proposed"),
    ("BR_FY26_committee_budget_report_JPS", 105, "The Mayor’s proposed FY 2026 operating budget for OVSJG is $83,373,719",
     "budget_proposed", 2026, "FO0", "", "Mayor's proposed FY2026 OVSJG operating budget $83,373,719 (23.6% below "
     "FY2025 approved), including a $21,211,000 reduction to Access to Justice and $5,842,000 to Victim Services",
     83_373_719, "", "", "proposed"),
    ("BR_FY26_committee_budget_report_Health", 42, "provides $800,000 from the Opioid Abatement Fund", "program_launch",
     2026, "RM0", "", "FY2026 BSA subtitle requires DBH to award substance use and behavioral health targeted outreach "
     "grants by October 31, 2025, with $800,000 from the Opioid Abatement Fund for four priority locations", 800_000, "",
     "", "bsa"),
    ("BR_FY27_committee_budget_report_52226-FY2027-JPS", 93, "The Mayor’s proposed FY 2027 operating budget for OVSJG is $77,090,845",
     "budget_proposed", 2027, "FO0", "", "Mayor's proposed FY2027 OVSJG operating budget $77,090,845 (30.2% below FY2026 "
     "approved), including a $27,299,000 reduction to Access to Justice and $5,596,000 to Victim Services", 77_090_845,
     "", "", "proposed"),
    ("BR_FY27_committee_budget_report_52226-FY2027-JPS", 96, "includes $49,930,000 for (PS02303) Victim Services",
     "budget_proposed", 2027, "FO0", "P02303", "Mayor's proposed FY2027 budget included $49,930,000 for Victim Services "
     "grants, a $5,596,000 reduction from FY2026", 49_930_000, "", -5_596_000, "proposed"),
    ("BR_FY27_committee_budget_report_FY27-Committee-on-Housing", 33, "additional $27.7 million for the Local Rent",
     "budget_proposed", 2027, "HY0", "R03905", "Mayor's proposed FY2027 Housing Authority operating budget $206.1 million "
     "(+15.5%), driven by an additional $27.7 million for the Local Rent Supplement Program for committed project-based "
     "and existing tenant-based vouchers", "", "", 27_700_000, "proposed"),
    ("BR_FY27_committee_budget_report_DRAFT-FY2027-Committee-on-Health", 5, "Interagency Council on Homelessness with $183,836",
     "budget_revised", 2027, "HG0", "AMP030", "Committee on Health FY2027 recommendation: restore the Deputy Director of "
     "the Interagency Council on Homelessness ($183,836)", "", "", 183_836, "markup"),
]


def run_curated():
    n = 0
    for key, page, anchor, et, fy, ag, pcode, desc, amt, prior, chg, rule in CURATED:
        hits = latest(f"*{key}*.pdf", "dc_council")
        if not hits:
            WARN.append(f"curated: no file for {key}")
            continue
        p = hits[-1]
        pages = pdfium_text(p)
        norm = lambda s: " ".join(s.replace("’", "’").split())
        found = None
        for cand in [page] + [page + d for d in (-1, 1, -2, 2)]:
            if 1 <= cand <= len(pages) and norm(anchor) in norm(pages[cand - 1]):
                found = cand
                break
        if not found:
            WARN.append(f"curated: anchor not found near p{page} in {p.name[:60]}: '{anchor[:50]}'")
            continue
        if rule == "proposed":
            d, basis = date_for("proposed", fy)
        elif rule == "bsa":
            d, basis = DATES["bsa_effective"].get(fy, ""), "BSA law/act effective date"
        else:
            if p.name not in MARKUP:
                parse_markup(p)
            d = MARKUP.get(p.name, "")
            basis = "committee markup date" if d else "markup date not printed; Local Budget Act 2nd reading used"
            if rule == "report":
                basis = "committee report markup date (event date not stated in text)"
            d = d or DATES["enacted"].get(fy, "")
        add_event(event_date=d, event_type=et, x_agency_code=ag, program_code=pcode, description=desc, amount=amt,
                  prior_amount=prior, amount_change=chg, fiscal_year=fy, source_id="doc_dc_council_budget_reports",
                  source_page=found, x_document=rel(p), x_record_kind="committee_report_item", x_date_basis=basis,
                  confidence="high" if rule in ("proposed", "bsa", "markup") and d else "medium")
        n += 1
    return n


def parse_markup(p: Path):
    flat_all = " ".join(" ".join(t.split()) for t in pdfium_text(p))
    m = re.search(r"(?:COMMITTEE ACTION AND VOTE|Committee Action(?: and Vote)?)\s+On (?:[A-Z][a-z]+day, )?"
                  r"([A-Z][a-z]+ \d{1,2})(?:st|nd|rd|th)?, (20\d\d)", flat_all)
    MARKUP[p.name] = iso(f"{m.group(1)}, {m.group(2)}") if m else ""


# ---------------------------------------------------------------- year-over-year events from approved books
def yoy_events():
    n = 0
    by_book = defaultdict(dict)
    for r in LINES:
        if r["x_table"] not in ("30-PBB",) and not re.fullmatch(r"[A-Z]{2}0-[24]", r["x_table"]):
            continue
        if r["budget_stage"] != "approved":
            continue
        lvl = r["x_level"]
        if lvl == "agency":
            if r["fund_type"] not in ("total", "local") or (r["fund_type"] == "local" and not r["x_table"].endswith("-2")):
                continue
            if r["fund_type"] == "total" and r["x_table"].endswith("-2"):
                continue  # agency gross totals come from 30-PBB / XX0-4
            key = (r["x_book_fy"], r["agency_code"], "agency", "", r["fund_type"])
        else:
            if r["fund_type"] != "total" or not r["x_in_scope"]:
                continue
            key = (r["x_book_fy"], r["agency_code"], lvl, r["program_code"], "total")
        by_book[key][int(r["fiscal_year"])] = r
    for (book, ag, lvl, pcode, ft), d in sorted(by_book.items(), key=lambda kv: tuple(str(x) for x in kv[0])):
        cur, prev = d.get(book), d.get(book - 1)
        if not cur or not prev:
            continue
        a, b = int(cur["amount"]), int(prev["amount"])
        if a == 0 and b == 0:
            continue
        name = cur["line_item"] if lvl != "agency" else f"{AGENCIES[ag]} total"
        date, basis = date_for("enacted", book)
        stream = "all funds" if ft == "total" else "local funds"
        add_event(event_date=date, event_type="budget_enacted", x_agency_code=ag, program_code=pcode,
                  funding_stream=stream,
                  description=f"FY{book} approved budget vs FY{book - 1} approved ({stream}): {pcode + ' ' if pcode else ''}"
                              f"{name} (as printed in the FY{book} book{'; FY2024 code ' + cur['activity_code'] if book == 2024 and cur['activity_code'] else ''})",
                  amount=a, prior_amount=b, amount_change=a - b, fiscal_year=book, source_id=cur["source_id"],
                  source_page=cur["page"], basis="derived", x_document=cur["document"],
                  x_record_kind="yoy_approved_change", x_date_basis=basis)
        n += 1
    return n


# ---------------------------------------------------------------- dedupe, preference and checks for budget lines
def finalize_lines():
    # exact duplicates (same stage/year/line/fund/value from the same table) -> keep one
    seen, out = set(), []
    for r in LINES:
        k = (r["fiscal_year"], r["budget_stage"], r["agency_code"], r["x_level"], r["activity_code"], r["program_code"],
             r["line_item"], r["fund_type"], r["x_fund_detail"], r["x_table"], r["x_book_fy"])
        if k in seen:
            continue
        seen.add(k)
        out.append(r)
    # agency-level rows: per (fy, stage, agency) keep one source -- chapter Table XX0-2 (fund detail) over 30-PBB/XX0-4
    # totals, then the latest book
    grp = defaultdict(list)
    for r in out:
        if r["x_level"] == "agency":
            grp[(r["fiscal_year"], r["budget_stage"], r["agency_code"])].append(r)
    drop = set()
    for k, rs in grp.items():
        best = max(rs, key=lambda r: (r["x_table"].endswith("-2"), int(r["x_book_fy"])))
        src = (best["x_book_fy"], best["x_table"])
        for r in rs:
            if (r["x_book_fy"], r["x_table"]) != src:
                drop.add(id(r))
    out = [r for r in out if id(r) not in drop]
    # repeats of the same printed line across books: keep the latest book, log value disagreements
    rep = defaultdict(list)
    for r in out:
        if r["x_level"] == "agency" or r["budget_stage"] == "proposed":
            continue
        rep[(r["fiscal_year"], r["budget_stage"], r["agency_code"], r["x_level"], r["activity_code"] or r["program_code"],
             r["fund_type"], r["x_fund_detail"])].append(r)
    disagree = []
    for k, rs in rep.items():
        if len(rs) < 2:
            continue
        rs.sort(key=lambda r: int(r["x_book_fy"]), reverse=True)
        vals = [int(r["amount"]) for r in rs]
        if max(vals) - min(vals) > 2000:
            disagree.append(f"{k[0]} {k[1]} {k[2]} {k[4]} {k[5]}: " +
                            ", ".join(f"FY{r['x_book_fy']} book {int(r['amount']):,}" for r in rs))
        for r in rs[1:]:
            drop.add(id(r))
    out = [r for r in out if id(r) not in drop]
    # x_preferred: per (fy, stage, agency, level, FY2025-structure program code) the latest book's total is preferred;
    # fund-split rows stay preferred only if their book's total agrees with that preferred total (so preferred fund
    # rows always add up to the preferred total)
    pref = defaultdict(list)
    for r in out:
        pref[(r["fiscal_year"], r["budget_stage"], r["agency_code"], r["program_code"],
              (r["x_level"] + r["line_item"]) if not r["program_code"] else "")].append(r)
    for rs in pref.values():
        totals = {}
        for r in rs:
            if r["fund_type"] == "total":
                b = int(r["x_book_fy"])
                totals[b] = totals.get(b, 0) + int(r["amount"])
        best = max(totals) if totals else max(int(r["x_book_fy"]) for r in rs)
        best_total = totals.get(best)
        by_fund = defaultdict(list)
        for r in rs:
            b = int(r["x_book_fy"])
            if r["fund_type"] == "total":
                r["x_preferred"] = "1" if b == best else "0"
            else:
                ok = best_total is None or (b in totals and abs(totals[b] - best_total) <= 2000)
                r["x_preferred"] = "0"
                if ok:
                    by_fund[(r["fund_type"], r["x_fund_detail"])].append(r)
        for fr in by_fund.values():
            max(fr, key=lambda r: int(r["x_book_fy"]))["x_preferred"] = "1"
    return out, disagree


def crosswalk_checks(lines):
    """FY2024-book old-code FY2024 approved vs FY2025-book restated FY2024 approved (new codes)."""
    old = defaultdict(int)
    new = {}
    for r in lines:
        if r["fiscal_year"] != 2024 or r["budget_stage"] != "approved" or r["fund_type"] != "total":
            continue
        if r["x_book_fy"] == 2024 and r["x_code_fy2025"] and r["agency_code"] in IN_SCOPE:
            old[(r["agency_code"], r["x_code_fy2025"])] += int(r["amount"])
        if r["x_book_fy"] == 2025:
            new[(r["agency_code"], r["program_code"])] = int(r["amount"])
    out = []
    for k, v in sorted(old.items()):
        if k[1] == "H03014-H03016":
            nv = sum(new.get((k[0], c), 0) for c in ("H03014", "H03015", "H03016"))
        else:
            nv = new.get(k)
        if nv is None:
            continue
        out.append(f"{k[0]} {k[1]}: FY2024 book {v:,} vs FY2025 book restated {nv:,} (delta {nv - v:+,})")
    return out


# ---------------------------------------------------------------- main
LINE_COLS = ["fiscal_year", "budget_stage", "agency_code", "agency", "program_code", "activity_code", "line_item",
             "fund_type", "amount", "document", "page", "source_id", "retrieved_date", "confidence", "basis",
             "x_level", "x_fund_detail", "x_table", "x_book_fy", "x_code_fy2025", "x_division_code",
             "x_units_printed", "x_in_scope", "x_tieout", "x_preferred"]
EVENT_COLS = ["event_id", "event_date", "event_type", "jurisdiction", "agency", "program_code", "funding_stream",
              "description", "amount", "prior_amount", "amount_change", "fiscal_year", "program_area_tags",
              "source_id", "source_page", "confidence", "basis", "retrieved_date", "x_agency_code", "x_record_kind",
              "x_date_basis", "x_scenario", "x_fy26", "x_fy28", "x_fy29", "x_fy30", "x_fte", "x_amounts_mentioned",
              "x_document"]
COMMITTEE_REPORTS = [("BR_FY25_Housing", 2025, "Housing"), ("BR_FY25_JPS", 2025, "the Judiciary and Public Safety"),
                     ("BR_FY26_committee_budget_report_Human-Services", 2026, "Human Services"),
                     ("BR_FY26_committee_budget_report_Housing", 2026, "Housing"),
                     ("BR_FY26_committee_budget_report_JPS", 2026, "the Judiciary and Public Safety"),
                     ("BR_FY26_committee_budget_report_Health", 2026, "Health"),
                     ("BR_FY27_committee_budget_report_DRAFT-FY2027-Committee-on-Health", 2027, "Health"),
                     ("BR_FY27_committee_budget_report_FY27-Committee-on-Housing", 2027, "Housing"),
                     ("BR_FY27_committee_budget_report_52226-FY2027-JPS", 2027, "the Judiciary and Public Safety")]


def write_csv(path: Path, cols: list[str], rows: list[dict]):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def main():
    read_dates()
    stats = []
    t5_stats = []
    for fy in BOOK_FYS:
        for ag in AGENCIES:
            chapters = latest(f"*_cfo_budget_fy{fy}_{ag}_*chapter*.pdf")
            divs = {"MULTIPLEPROGRAMS": ""}
            if fy == 2026:
                for ch in chapters:
                    out = parse_chapter_t4(ch, fy, ag)
                    stats.append(f"FY{fy} {ag} Table {ag}-4 ({ch.name.split('_', 1)[1][-32:]}): {len(out)} lines")
                    for r, dcode, dname in out:
                        if r[0] == "division":
                            divs[squash(r[2])] = r[1]
                            DIVNAME.setdefault(squash(r[2]), r[2].title())
            else:
                for tb in [t for t in latest(f"*_cfo_budget_fy{fy}_{ag}_*tables*.pdf") if "2026o" not in t.name]:
                    recs = parse_30pbb(tb, fy, ag)
                    stats.append(f"FY{fy} {ag} 30-PBB ({tb.name.split('_', 1)[1][-32:]}): {len(recs)} lines")
                    for r in recs:
                        if r[0] == "division":
                            divs[squash(r[4])] = OLD2NEW.get(ag, {}).get(r[3], r[3]) if fy == 2024 else r[3]
                            DIVNAME.setdefault(squash(r[4]), r[4].title())
            if fy != 2025 or ag == "CF0":
                for ch in chapters:
                    for row in parse_chapter_t2(ch, fy, ag):
                        add_line(**row)
                    n_all, n_kept = parse_chapter_t5(ch, fy, ag, divs)
                    t5_stats.append(f"FY{fy} {ag} Table {ag}-5: {n_all} change lines, {n_kept} in scope")
            else:
                for ch in chapters:
                    if ag == "FO0":
                        t5_stats.append("FY2025 FO0: chapter change text is font-garbled (amounts missing); "
                                        "OVSJG FY2025 changes taken from the JPS committee report")
                        continue
                    n = parse_fy2025_narrative(ch, ag)
                    t5_stats.append(f"FY2025 {ag} narrative change sentences (pypdfium2): {n} in scope")
    n_comm = []
    for key, fy, comm in COMMITTEE_REPORTS:
        for p in latest(f"*{key}*.pdf", "dc_council"):
            n_comm.append(f"{key} -> {parse_committee_tables(p, fy, comm)} in-scope proposed activity rows "
                          f"(markup {MARKUP.get(p.name) or 'not printed'})")
    chart = latest("*Net-Operating-Budget-Adjustments-Chart*.pdf", "dc_council")
    chart_stat = parse_council_chart(chart[-1]) if chart else (0, 0)
    n_bsa = parse_bsa()
    n_cur = run_curated()
    n_yoy = yoy_events()
    lines, disagree = finalize_lines()
    xw = crosswalk_checks(lines)
    # events: drop exact duplicates by id
    seen, events = set(), []
    for e in EVENTS:
        if e["event_id"] in seen:
            continue
        seen.add(e["event_id"])
        events.append(e)
    lines.sort(key=lambda r: (r["agency_code"], int(r["fiscal_year"]), r["budget_stage"], str(r["x_book_fy"]),
                              r["x_level"], r["program_code"], r["fund_type"], r["x_fund_detail"]))
    events.sort(key=lambda e: (str(e["fiscal_year"]), e["event_date"], e["x_agency_code"], e["x_record_kind"],
                               e["program_code"]))
    write_csv(OUT_LINES, LINE_COLS, lines)
    write_csv(OUT_EVENTS, EVENT_COLS, events)
    # ---- checks
    key_cols = ("fiscal_year", "budget_stage", "agency_code", "x_level", "activity_code", "program_code", "line_item",
                "fund_type", "x_fund_detail", "x_book_fy", "x_table")
    dup = len(lines) - len({tuple(str(r[c]) for c in key_cols) for r in lines})
    ties = Counter("pass" if "-> pass" in t else "fail" for t in TIE_LOG if "->" in t)
    fails = [t for t in TIE_LOG if "-> fail" in t]
    cov = defaultdict(set)
    for r in lines:
        cov[(r["fiscal_year"], r["agency_code"])].add(f"{r['budget_stage']}:{r['fund_type']}")
    cov_lines = []
    for fy in range(2021, 2028):
        cov_lines.append(f"| FY{fy} | " + " | ".join(
            ",".join(sorted({s.split(':')[0][:4] + ('+funds' if any(x.split(':')[1] != 'total' and x.split(':')[0] == s.split(':')[0]
                                                                 for x in cov[(fy, ag)]) else '')
                             for s in cov[(fy, ag)]})) or "-" for ag in AGENCIES) + " |")
    ek = Counter(e["x_record_kind"] for e in events)
    et = Counter(e["event_type"] for e in events)
    log("37_parse_dc_budget: DC budget lines and policy events", "\n".join([
        f"- {rel(OUT_LINES)}: {len(lines):,} rows ({Counter(r['budget_stage'] for r in lines)}); "
        f"in-scope program/agency rows {sum(1 for r in lines if r['x_in_scope']):,}; duplicate keys {dup}",
        f"- {rel(OUT_EVENTS)}: {len(events):,} rows; by kind {dict(ek)}; by type {dict(et)}",
        "- parsed tables: " + "; ".join(stats),
        "- change items: " + "; ".join(t5_stats),
        f"- committee report tables: " + "; ".join(n_comm),
        f"- FY2027 Council adjustments chart: {chart_stat[0]} rows read, {chart_stat[1]} in-scope events",
        f"- BSA subtitles kept: {n_bsa}; curated committee-report items: {n_cur}; YoY approved-change events: {n_yoy}",
        f"- tie-outs: {ties.get('pass', 0)} pass, {ties.get('fail', 0)} fail"
        + (": " + " | ".join(fails) if fails else ""),
        "- tie-out detail (in-scope divisions): " + " | ".join(
            t for t in TIE_LOG if re.search(r"HS0030|PS0023|EC0039|5000|4000|6000|agency total|-2 p", t))[:6000],
        "- cross-book disagreements (same FY/stage/code, >$2K apart; later book preferred via x_preferred): "
        + (" | ".join(disagree[:40]) if disagree else "none"),
        "- FY2024 old-code -> FY2025 code crosswalk (FY2024 approved): " + " | ".join(xw),
        "- event dates: budget_enacted/budget_revised = Local Budget Act 2nd reading "
        f"{DATES['enacted']}; budget_proposed = BSA introduced on behalf of the Mayor {DATES['proposed']} "
        "(FY2024 proposal date not in downloaded docs -> blank); BSA policy rows = law/act effective date "
        f"{DATES['bsa_effective']}; committee items = markup date when printed, else Local Budget Act date",
        "- mapping: Table XX0-5 lines before 'Mayor's Proposed Budget' -> budget_proposed; lines between it and "
        "'District's Approved Budget' -> budget_revised (Council changes); FY2027 Council-level changes taken from "
        "the activity-level Council chart instead of JA0-5 to avoid double counting",
        "- coverage (stage[+funds] by FY x agency " + "/".join(AGENCIES) + "):\n" + "\n".join(cov_lines),
        f"- warnings ({len(WARN)}): " + " | ".join(WARN[:25]),
    ]))
    print(f"lines {len(lines)}  events {len(events)}  dup {dup}  ties {dict(ties)}")


if __name__ == "__main__":
    main()
