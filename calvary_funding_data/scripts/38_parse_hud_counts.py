"""Phase 4 parse, area dc_hud: homelessness counts (HUD PIT/HIC by CoC, DC-500 PopSub, MWCOG regional
report tables) and DC-500 project-level Housing Inventory Count.

Reads raw/hud/ only (downloaded by scripts/14_probe_dc_hud.py). Writes:
  interim/stage_homeless_counts__hud.csv  (supplementary; long format)
      coc_code, jurisdiction, year, measure, population, value, source_id, retrieved_date, confidence, basis, x_...
  interim/stage_hic_projects__hud.csv     (supplementary; one row per DC-500 HIC project line, 2022-2025)
      year, coc_code, organization_name, recipient_ein, project_name, project_type, total_beds, units,
      target_population, source_id, retrieved_date, confidence, basis, x_...

Sources (registered by script 14): bulk_hud_ahar_pit_hic (AHAR 2025 PIT and HIC by CoC workbooks),
doc_hud_hic_dc500 (HUD Exchange DC-500 HIC and PopSub PDFs), doc_mwcog_pit (MWCOG annual PIT reports).

Measure naming:
  PIT workbook   measure pit_{overall|sheltered_es|sheltered_th|sheltered_sh|sheltered_total|unsheltered};
                 population {all|individuals|people_in_families|family_households|veterans|unaccompanied_youth_u25|
                 ...} with prefix chronic_ for chronically homeless columns and '|{group}' for age/race subgroups.
  HIC workbook   measure hic_{beds_year_round|beds_year_round_non_dv|beds_year_round_hmis|hmis_participation_rate|
                 beds|units|beds_dedicated|beds_seasonal|beds_overflow|beds_total}__{project type};
                 population all / hh_with_children / hh_without_children / hh_only_children / veterans / youth / chronic.
  PopSub PDFs    measure popsub_{sheltered_es|sheltered_th|unsheltered|overall}; population '{unit}:{section}:{label}'.
  MWCOG reports  measure mwcog_persons / mwcog_family_households / mwcog_pct_of_adults; population per table.

Usage: .venv/bin/python scripts/38_parse_hud_counts.py
"""
from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd
import pdfplumber
from rapidfuzz import fuzz

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import CLEAN, CONFIG, INTERIM, RAW, log, norm_name, rel  # noqa: E402

HUD = RAW / "hud"
OUT_COUNTS = INTERIM / "stage_homeless_counts__hud.csv"
OUT_HIC = INTERIM / "stage_hic_projects__hud.csv"
SEC = "38_parse_hud_counts"

COCS = {  # CoC code -> MWCOG jurisdiction label (1:1 for these eight)
    "DC-500": "District of Columbia",
    "MD-600": "Prince George's County, MD",
    "MD-601": "Montgomery County, MD",
    "VA-600": "Arlington County, VA",
    "VA-601": "Fairfax County, VA",
    "VA-602": "Loudoun County, VA",
    "VA-603": "City of Alexandria, VA",
    "VA-604": "Prince William County, VA",
}
JUR_TO_COC = {v: k for k, v in COCS.items()}
TCP_EIN = "521681401"

LOG: dict[str, list[str]] = defaultdict(list)


def raw_file(pattern: str) -> Path:
    hits = sorted(HUD.glob(pattern))
    if not hits:
        raise FileNotFoundError(f"raw/hud/{pattern}")
    return hits[-1]


def retrieved(p: Path) -> str:
    s = p.name[:8]
    return f"{s[:4]}-{s[4:6]}-{s[6:8]}"


def slug(s: str) -> str:
    s = s.lower().replace("&", " and ").replace("+", " plus ")
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_")


def to_int(s):
    if s is None:
        return None
    s = str(s).replace(",", "").strip()
    if s in ("", "n/a", "N/A", "-"):
        return None
    try:
        return int(float(s))
    except ValueError:
        return None


# ===================================================================== 1. PIT by CoC (xlsb)
PIT_RE = re.compile(r"^(Overall|Sheltered ES|Sheltered TH|Sheltered SH|Sheltered Total|Unsheltered) "
                    r"(Chronically )?Homeless(?: (.+?))?(?: - (.+))?$")
PIT_POP = {
    None: "all", "Individuals": "individuals", "People in Families": "people_in_families",
    "Family Households": "family_households", "Veterans": "veterans",
    "Unaccompanied Youth (Under 25)": "unaccompanied_youth_u25",
    "Unaccompanied Youth Under 18": "unaccompanied_youth_u18",
    "Unaccompanied Youth Age 18-24": "unaccompanied_youth_18_24",
    "Parenting Youth (Under 25)": "parenting_youth_u25", "Parenting Youth Under 18": "parenting_youth_u18",
    "Parenting Youth Age 18-24": "parenting_youth_18_24", "Children of Parenting Youth": "children_of_parenting_youth",
}
ID_COLS = {"CoC Number", "CoC Name", "CoC Category", "Count Types"}


def parse_pit() -> tuple[list[dict], dict]:
    f = raw_file("*_huduser_2007-2025-PIT-Counts-by-CoC.xlsb")
    rd = retrieved(f)
    xl = pd.ExcelFile(f, engine="pyxlsb")
    rows, unknown, names = [], Counter(), {}
    years = sorted(int(s) for s in xl.sheet_names if re.fullmatch(r"20\d\d", s))
    missing = []
    for y in years:
        d = xl.parse(str(y))
        d = d[d["CoC Number"].isin(COCS)]
        found = set(d["CoC Number"])
        missing += [f"{c} {y}" for c in COCS if c not in found]
        for _, r in d.iterrows():
            coc = r["CoC Number"]
            names.setdefault(coc, r["CoC Name"])
            for col in d.columns:
                if col in ID_COLS:
                    continue
                v = r[col]
                if pd.isna(v) or str(v).strip() == "":
                    continue
                try:
                    v = float(v)
                except (TypeError, ValueError):
                    unknown[f"{col} (non-numeric {str(v)[:10]!r})"] += 1
                    continue
                m = PIT_RE.match(str(col).strip())
                if not m or m.group(3) not in PIT_POP:
                    unknown[col] += 1
                    continue
                status, chronic, pop, grp = m.groups()
                population = ("chronic_" if chronic else "") + PIT_POP[pop]
                if grp:
                    population += "|" + slug(grp)
                rows.append({
                    "coc_code": coc, "jurisdiction": r["CoC Name"], "year": y,
                    "measure": "pit_" + slug(status), "population": population, "value": int(round(float(v))),
                    "source_id": "bulk_hud_ahar_pit_hic", "retrieved_date": rd, "confidence": "high",
                    "basis": "documented", "x_document": rel(f), "x_sheet": str(y), "x_page": "",
                    "x_column_raw": col, "x_count_type": r.get("Count Types", "") if "Count Types" in d.columns else "",
                    "x_note": "",
                })
    LOG["pit"].append(f"- PIT by CoC ({rel(f)}): sheets {years[0]}-{years[-1]}; {len(rows):,} rows for "
                      f"{len(COCS)} CoCs; unparsed column names {len(unknown)}"
                      + (f" (e.g. {list(unknown)[:3]})" if unknown else "")
                      + f"; CoC-years absent: {missing or 'none'}")
    partial = sorted({(r['coc_code'], r['year'], r['x_count_type']) for r in rows
                      if 'partial' in str(r['x_count_type']).lower()})
    if partial:
        LOG["pit"].append("- partial unsheltered counts (Count Types): "
                          + "; ".join(f"{c} {y}" for c, y, _ in partial))
    LOG["pit"].append("- workbook has no gender columns in any year (only age, race/ethnicity, household and "
                      "subpopulation splits); DC gender comes from PopSub 2024 and the MWCOG 2025 DC narrative")
    return rows, names


# ===================================================================== 2. HIC by CoC (xlsx)
PT = {"ES": "es", "TH": "th", "SH": "sh", "RRH": "rrh", "PSH": "psh", "OPH": "oph", "DEM": "dem", "RRH & DEM": "rrh_dem"}


def pt_slug(g: str) -> str:
    """'ES, TH, SH' -> 'es_th_sh'; 'RRH & DEM' -> 'rrh_dem'."""
    parts = re.split(r"[,&]", g.replace(" ", ""))
    return "_".join(PT.get(p, slug(p)) for p in parts if p)


HH = {"with Children": "hh_with_children", "without Children": "hh_without_children",
      "with only Children": "hh_only_children"}


def hic_col(col: str) -> tuple[str, str, str] | None:
    """Map a HIC workbook column name to (measure_base, project_type_slug, population)."""
    c = " ".join(str(col).split())
    rules = [
        (r"^Total Year-Round Beds \((.+)\)$", "beds_year_round", "all"),
        (r"^Total Non-DV Year-Round Beds \((.+)\)$", "beds_year_round_non_dv", "all"),
        (r"^Total HMIS Year-Round Beds \((.+)\)$", "beds_year_round_hmis", "all"),
        (r"^HMIS Participation Rate(?: for Year-Round Beds)? \((.+)\)$", "hmis_participation_rate", "all"),
        (r"^Total Units for Households with Children \((.+)\)$", "units", "hh_with_children"),
        (r"^Total Seasonal Beds \((.+)\)$", "beds_seasonal", "all"),
        (r"^Total Overflow Beds \((.+)\)$", "beds_overflow", "all"),
        (r"^Total Emergency Shelter \(ES\) Beds \(excluding seasonal\+(?:overflow|O/V)\)$", "beds_year_round", "all", "ES"),
        (r"^Total Overflow/Voucher ES Beds$", "beds_overflow", "all", "ES"),
        (r"^Total Transitional Housing \(TH\) Beds$", "beds_year_round", "all", "TH"),
        (r"^Total Rapid Rehousing \(RRH\) Beds$", "beds_year_round", "all", "RRH"),
        (r"^Total Safe Haven \(SH\) Beds$", "beds_year_round", "all", "SH"),
        (r"^Total Chronic Homeless PSH Beds$", "beds_dedicated", "chronic", "PSH"),
    ]
    for rule in rules:
        m = re.match(rule[0], c)
        if m:
            g = rule[3] if len(rule) > 3 else m.group(1)
            return rule[1], pt_slug(g), rule[2]
    m = re.match(r"^Total Beds for Households (with Children|without Children|with only Children) \((.+)\)$", c)
    if m:
        return "beds", pt_slug(m.group(2)), HH[m.group(1)]
    m = re.match(r"^Dedicated (Veteran|Youth|Chronically Homeless) Beds \((.+)\)$", c)
    if m:
        return "beds_dedicated", pt_slug(m.group(2)), {"Veteran": "veterans", "Youth": "youth",
                                                        "Chronically Homeless": "chronic"}[m.group(1)]
    # 2007-2013 layout: "Total Year-Round ES Beds", "ES HMIS Participation Rate", "Total TH Beds for Households ..."
    m = re.match(r"^(ES|TH|RRH|SH|PSH) HMIS Participation Rate$", c)
    if m:
        return "hmis_participation_rate", pt_slug(m.group(1)), "all"
    m = re.match(r"^Total (Year-Round |Non-DV Year-Round |HMIS Year-Round |Seasonal |Overflow )?(ES|TH|RRH|SH|PSH) "
                 r"(Beds|Units)(?: for Households (with Children|without Children|with only Children))?$", c)
    if m:
        kind, ptyp, unit, hh = m.groups()
        base = {None: "beds_total", "Year-Round ": "beds_year_round", "Non-DV Year-Round ": "beds_year_round_non_dv",
                "HMIS Year-Round ": "beds_year_round_hmis", "Seasonal ": "beds_seasonal",
                "Overflow ": "beds_overflow"}[kind]
        if unit == "Units":
            base = "units"
        elif hh:
            base = "beds"
        return base, pt_slug(ptyp), HH.get(hh, "all") if hh else ("hh_with_children" if unit == "Units" else "all")
    return None


def parse_hic_coc(names: dict) -> list[dict]:
    f = raw_file("*_huduser_2007-2025-HIC-Counts-by-CoC.xlsx")
    rd = retrieved(f)
    xl = pd.ExcelFile(f)
    rows, unknown, dup_conflict = [], Counter(), []
    years = sorted(int(s) for s in xl.sheet_names if re.fullmatch(r"20\d\d", s))
    for y in years:
        head = xl.parse(str(y), header=None, nrows=3)
        hr = next(i for i in range(3) if str(head.iloc[i, 0]).strip().startswith("CoC"))
        d = xl.parse(str(y), header=hr)
        idc = d.columns[0]
        d = d[d[idc].astype(str).str.strip().isin(COCS)]
        seen = {}
        for _, r in d.iterrows():
            coc = str(r[idc]).strip()
            for col in d.columns[1:]:
                v = r[col]
                if pd.isna(v) or str(col).startswith("Unnamed"):
                    continue
                mp = hic_col(re.sub(r"\.\d+$", "", str(col)))
                if not mp:
                    unknown[col] += 1
                    continue
                base, ptyp, pop = mp
                measure = f"hic_{base}__{ptyp}"
                try:
                    fv = float(v)
                except (TypeError, ValueError):
                    unknown[f"{col} (non-numeric)"] += 1
                    continue
                val = round(fv, 4) if base == "hmis_participation_rate" else int(round(fv))
                k = (coc, measure, pop)
                if k in seen:
                    if seen[k] != val:
                        dup_conflict.append(f"{coc} {y} {col}")
                        measure += "__alt"
                    else:
                        continue
                seen[k] = val
                rows.append({
                    "coc_code": coc, "jurisdiction": names.get(coc, ""), "year": y, "measure": measure,
                    "population": pop, "value": val, "source_id": "bulk_hud_ahar_pit_hic", "retrieved_date": rd,
                    "confidence": "high", "basis": "documented", "x_document": rel(f), "x_sheet": str(y),
                    "x_page": "", "x_column_raw": " ".join(str(col).split()), "x_count_type": "",
                    "x_note": "HMIS participation rate is a share (0-1)" if base == "hmis_participation_rate" else "",
                })
    LOG["hic"].append(f"- HIC by CoC ({rel(f)}): sheets {years[0]}-{years[-1]}; {len(rows):,} rows; unparsed "
                      f"columns {len(unknown)}" + (f" ({list(unknown)[:4]})" if unknown else "")
                      + f"; same-measure columns with different values kept as '__alt': {len(dup_conflict)}")
    return rows


# ===================================================================== 3. PopSub PDFs (DC-500)
POPSUB_ROW = re.compile(r"^(?P<label>.+?)\s+(?P<a>[\d,]+)\s+(?P<b>[\d,]+)\s+(?P<c>[\d,]+)\s+(?P<d>[\d,]+)$")
POPSUB_SECTIONS = [
    (r"Summary by household type reported", "households", "household_type"),
    (r"Summary of persons in each household type", "persons", "household_type"),
    (r"Demographic summary by ethnicity and race", "persons", "race_ethnicity"),
    (r"Demographic summary by gender", "persons", "gender"),
    (r"Summary of chronically homeless households", "households", "chronic"),
    (r"Summary of chronically homeless persons", "persons", "chronic"),
    (r"Summary of all other populations", "persons", "subpopulation"),
]


def parse_popsub() -> list[dict]:
    rows = []
    for y in (2024, 2025):
        f = raw_file(f"*_hudx_CoC_PopSub_DC-500_{y}.pdf")
        rd = retrieved(f)
        sh_note = ("Safe Haven included in Transitional Housing" if y == 2024
                   else "Safe Haven included in Emergency Shelter")
        n0 = len(rows)
        with pdfplumber.open(f) as pdf:
            unit = section = None
            hh_ctx = ""
            for pi, pg in enumerate(pdf.pages):
                for ln in (pg.extract_text() or "").splitlines():
                    ln = ln.strip()
                    for rx, u, s in POPSUB_SECTIONS:
                        if re.match(rx, ln, re.I):
                            unit, section, hh_ctx = u, s, ""
                    m = POPSUB_ROW.match(ln)
                    if not m or not section:
                        continue
                    label = re.sub(r"[¹²³*]", "", m.group("label")).strip()
                    lab = slug(label)
                    if section == "household_type" and unit == "persons":
                        if lab.startswith("persons_in_households") or lab.startswith("total"):
                            hh_ctx = lab.replace("persons_in_households_", "")
                            pop = f"persons:household_type:{hh_ctx}"
                        else:
                            pop = f"persons:household_type:{hh_ctx}:{lab}"
                    else:
                        pop = f"{unit}:{section}:{lab}"
                    for key, meas in zip("abcd", ("popsub_sheltered_es", "popsub_sheltered_th",
                                                    "popsub_unsheltered", "popsub_overall")):
                        rows.append({
                            "coc_code": "DC-500", "jurisdiction": "District of Columbia CoC", "year": y,
                            "measure": meas, "population": pop, "value": to_int(m.group(key)),
                            "source_id": "doc_hud_hic_dc500", "retrieved_date": rd, "confidence": "high",
                            "basis": "documented", "x_document": rel(f), "x_sheet": "", "x_page": pi + 1,
                            "x_column_raw": label, "x_count_type": "", "x_note": sh_note,
                        })
        got = {r["population"]: r["value"] for r in rows[n0:] if r["measure"] == "popsub_overall"}
        tot = got.get("persons:household_type:total_homeless_persons")
        LOG["popsub"].append(f"- PopSub DC-500 {y} ({rel(f)}): {len(rows) - n0} rows; total persons {tot}; "
                             f"women {got.get('persons:gender:woman_girl_if_child', 'n/a')}")
        # check: gender rows sum to total
        g = sum(v for k, v in got.items() if k.startswith("persons:gender:") and not k.endswith(":total"))
        if any(k.startswith("persons:gender:") for k in got):
            LOG["checks"].append(f"- PopSub {y} gender rows sum {g} vs total {tot}: {'pass' if g == tot else 'FAIL'}")
    return rows


# ===================================================================== 4. MWCOG report tables
JUR_RX = [
    ("City of Alexandria, VA", re.compile(r"alexandria", re.I)),
    ("Arlington County, VA", re.compile(r"arlington", re.I)),
    ("District of Columbia", re.compile(r"district\s+of(\s+columbia)?", re.I)),
    ("Fairfax County, VA", re.compile(r"fairfax", re.I)),
    ("Loudoun County, VA", re.compile(r"loudoun", re.I)),
    ("Montgomery County, MD", re.compile(r"montgomery", re.I)),
    ("Prince George's County, MD", re.compile(r"prince\s+george", re.I)),
    ("Prince William County, VA", re.compile(r"prince\s+william", re.I)),
    ("Frederick City & County, MD", re.compile(r"frederick", re.I)),
    ("COG region", re.compile(r"^\s*(total|all\s+cog(\s+cocs)?|cog(\s+region)?|region)\b", re.I)),
]
NUM_TOK = r"(?:-?\$?[\d,]+(?:\.\d+)?%?|N/A|n/a)"
DATA_LINE = re.compile(rf"^(?P<name>.*?[A-Za-z'’.)].*?)?\s*(?P<nums>{NUM_TOK}(?:\s+{NUM_TOK})+)\s*$")


def resolve_jur(text: str) -> str | None:
    text = text.replace("’", "'")
    hits = [(m.start(), j) for j, rx in JUR_RX for m in [rx.search(text)] if m]
    if not hits:
        return None
    return sorted(hits)[-1][1]  # nearest to the end (the data line)


def is_num(t: str) -> bool:
    return bool(re.fullmatch(NUM_TOK, t))


def num_val(t: str):
    t = t.replace(",", "").replace("$", "")
    if t.lower() == "n/a" or t.endswith("%"):
        return None
    return int(float(t))


# Table selection by title (numbering changes between reports)
MW_TABLES = [
    # (title regex, kind, measure, population, columns)
    (r"^People Experiencing Literal Homelessness by Jurisdiction", "auto", "mwcog_persons", "all", None),
    (r"^\d{4} Persons in Families Experiencing Homelessness by Jurisdiction", "single_year", None, None,
     [("mwcog_family_households", "families"), ("mwcog_persons", "adults_in_families"),
      ("mwcog_persons", "children_in_families"), ("mwcog_persons", "persons_in_families")]),
    (r"^Change in Persons in Families Experiencing Homelessness", "years", "mwcog_persons", "persons_in_families", None),
    (r"^Households With Only Children", "years", "mwcog_persons", "households_with_only_children", None),
    (r"^(Comparison of )?Unsheltered Single Adults (Experiencing Homelessness )?By Jurisdiction", "years",
     "mwcog_persons", "unsheltered_single_adults", None),
    (r"^Single Adults Experiencing Chronic Homelessness by Jurisdiction", "years", "mwcog_persons",
     "chronic_single_adults", None),
    (r"^Veterans Experiencing Homelessness by Jurisdiction", "years", "mwcog_persons", "veterans", None),
]
BLOCK_COLS = [("mwcog_persons", "households_without_children"), ("mwcog_persons", "households_with_only_children"),
              ("mwcog_persons", "households_with_adults_and_children"), ("mwcog_persons", "all")]


def table_regions(pages: list[str]):
    """Yield (page_no, title, lines) for each 'Table N: title' block up to the 'Source:' line."""
    for pi, t in enumerate(pages):
        if len(re.findall(r"(?m)^\s*TABLE\s+\d+\s*:", t)) >= 3:
            continue  # table-of-contents page
        lines = t.splitlines()
        for i, ln in enumerate(lines):
            m = re.match(r"^\s*table\s+(\d+)\s*:\s*(.+)$", ln, re.I)
            if not m:
                continue
            body = []
            for ln2 in lines[i + 1:]:
                if re.match(r"^\s*Source", ln2):
                    break
                body.append(ln2)
            title = m.group(2).strip()
            # wrapped titles: the year range may be on the next line
            nxt = body[0] if body else ""
            if re.fullmatch(r"\s*(20\d\d\s*[-–]+\s*20\d\d|20\d\d)\*?\s*(\(Continued\))?\s*", nxt):
                title += " " + nxt.strip()
            yield pi + 1, title, body


def years_for(title: str, body: list[str], report_year: int) -> list[int]:
    m = re.search(r"(20\d\d)\s*[-–]+\s*(20\d\d)", title)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        if a < b <= report_year:
            return list(range(a, b + 1))
    for ln in body[:8]:
        ys = re.findall(r"(?<![-–\d])(20\d\d)(?![\d]|\s*[-–])", ln)
        ys = [int(x) for x in ys]
        if len(ys) >= 3 and ys == sorted(ys) and ys[-1] <= report_year:
            return ys
    return list(range(report_year - 4, report_year + 1))


def parse_rows_single(body: list[str]):
    """Rows of a one-row-per-jurisdiction table; name fragments may sit on lines above/below the numbers."""
    out, pending = [], []
    for ln in body:
        ln = ln.strip()
        if not ln:
            continue
        m = DATA_LINE.match(ln)
        nums = m.group("nums").split() if m else []
        if not m or len(nums) < 2:
            pending.append(ln)
            continue
        own = (m.group("name") or "").strip()
        jur = resolve_jur(own) if own else None
        if not jur:
            jur = resolve_jur(" ".join(pending[-3:] + [own]))
        if jur:
            out.append((jur, nums))
        pending = []
    return out


def parse_rows_block(body: list[str]):
    """Table 17/18 layout: blocks of 'YYYY a b c d' rows per jurisdiction, closed by a 'Percent Change' row."""
    out, frag, recs = [], [], []
    for ln in body:
        ln = ln.strip()
        if not ln:
            continue
        if re.search(r"Percent\s+Change", ln, re.I):
            jur = resolve_jur(" ".join(frag))
            if jur:
                out += [(jur, y, v) for y, v in recs]
            frag, recs = [], []
            continue
        m = re.match(rf"^(?P<pre>.*?)\b(?P<y>20\d\d)\s+(?P<nums>{NUM_TOK}(?:\s+{NUM_TOK}){{3}})\s*$", ln)
        if m and len(m.group("nums").split()) == 4:
            if m.group("pre").strip():
                frag.append(m.group("pre").strip())
            recs.append((int(m.group("y")), m.group("nums").split()))
        elif not re.search(r"Households|Jurisdiction|Children|Youth|All Persons", ln):
            frag.append(ln)
    return out


def parse_mwcog(pit_rows: list[dict]) -> list[dict]:
    rows, skipped = [], []
    checks = []
    for y in (2023, 2024, 2025, 2026):
        f = raw_file(f"*_mwcog_homelessness_metro_washington_{y}_PIT.pdf")
        rd = retrieved(f)
        with pdfplumber.open(f) as pdf:
            pages = [pg.extract_text() or "" for pg in pdf.pages]
        n0 = len(rows)
        block_acc = defaultdict(list)  # Table 17/18 spans two pages; check sums after both
        for page, title, body in table_regions(pages):
            spec = next((s for s in MW_TABLES if re.search(s[0], title, re.I)), None)
            if not spec:
                continue
            rx, kind, measure, population, cols = spec
            if kind == "auto":
                kind = "block" if any("Jurisdiction/Year" in b for b in body[:6]) else "years"
            tid = f"MWCOG {y} p{page} '{title[:70]}'"
            recs = []  # (jur, year, measure, population, value)
            if kind == "block":
                for jur, yr, nums in parse_rows_block(body):
                    for (ms, pop), t in zip(BLOCK_COLS, nums):
                        recs.append((jur, yr, ms, pop, num_val(t)))
                block_acc[title.split(" (Continued)")[0][:60]] += [(page, r) for r in recs]
            elif kind == "single_year":
                for jur, nums in parse_rows_single(body):
                    for (ms, pop), t in zip(cols, nums):
                        recs.append((jur, y, ms, pop, num_val(t)))
            else:
                yrs = years_for(title, body, y)
                for jur, nums in parse_rows_single(body):
                    if len(nums) < len(yrs):
                        continue
                    for yr, t in zip(yrs, nums):
                        recs.append((jur, yr, measure, population, num_val(t)))
            if kind != "block":
                keep_table(recs, [page] * len(recs), tid, title, f, rd, y, rows, checks, skipped)
        for t, items in block_acc.items():
            pgs = sorted({p for p, _ in items})
            keep_table([r for _, r in items], [p for p, _ in items], f"MWCOG {y} pp{pgs} '{t}'", t, f, rd, y,
                       rows, checks, skipped, block=True)
        # DC narrative gender-of-adults table (machine-readable only in the 2025 report)
        for pi, t in enumerate(pages):
            if "GENDER OF ADULTS" not in t:
                continue
            jur = None
            for pj in range(pi, max(pi - 12, -1), -1):
                if re.search(r"JURISDICTIONAL NARRATIVE REPORT\s*\n\s*DISTRICT OF COLUMBIA", pages[pj]):
                    jur = "District of Columbia"
                    break
            if not jur:
                skipped.append(f"MWCOG {y} p{pi + 1} gender table (jurisdiction not identified)")
                continue
            seg = t.split("GENDER OF ADULTS", 1)[1].splitlines()
            for ln in seg[1:]:
                m = re.match(r"^(?P<label>[A-Za-z][A-Za-z ().,\-]+?)\s+(?P<a>[\d.]+)%\s+(?P<b>[\d.]+)%\s*$", ln.strip())
                if not m:
                    if ln.strip().startswith("Age"):
                        break
                    continue
                for key, grp in (("a", "unaccompanied_adults"), ("b", "adults_in_families")):
                    r = mw_row(jur, y, "mwcog_pct_of_adults", f"{grp}|{slug(m.group('label'))}",
                               float(m.group(key)), f, rd, pi + 1, "DC narrative: Demographics: Gender of Adults", y)
                    r["x_note"] = "percent of adults counted (0-100)"
                    rows.append(r)
        LOG["mwcog"].append(f"- MWCOG {y} report ({rel(f)}): {len(rows) - n0} table cells kept")
    # keep one value per (jurisdiction, year, measure, population): latest report wins; log revisions
    best, revised, within = {}, [], []
    for r in sorted(rows, key=lambda r: (r["x_report_year"], -int(r["x_page"]))):
        k = (r["jurisdiction"], r["year"], r["measure"], r["population"])
        if k in best and best[k]["value"] != r["value"]:
            if best[k]["x_report_year"] != r["x_report_year"]:
                revised.append(f"{k[0]} {k[1]} {k[3]}: {best[k]['value']} (rpt {best[k]['x_report_year']}) -> "
                               f"{r['value']} (rpt {r['x_report_year']})")
            else:
                within.append(f"{k[0]} {k[1]} {k[3]} rpt {r['x_report_year']}: p{best[k]['x_page']} "
                              f"{best[k]['value']} vs p{r['x_page']} {r['value']}")
        best[k] = r
    out = list(best.values())
    for r in out:
        r["x_superseded_values"] = ""
    LOG["mwcog"].append(f"- MWCOG: {len(rows)} cells parsed across reports -> {len(out)} after keeping the latest "
                        f"report per jurisdiction/year/measure/population; values revised between reports: "
                        f"{len(revised)}" + (f" (e.g. {'; '.join(revised[:4])})" if revised else "")
                        + f"; same report, two tables disagree (earlier page kept): {len(within)}"
                        + (f" ({'; '.join(within[:4])})" if within else ""))
    LOG["mwcog"].append("- skipped tables (did not parse reliably): " + ("; ".join(skipped) or "none")
                        + "; source-inconsistent columns are kept with confidence medium and an x_note")
    LOG["mwcog"].append("- not parsed: figures/charts (demographic profiles, income, gender charts), Table 3 "
                        "population shares, Table 13/14 shelter status, TAY tables, Table 16 bed inventory, "
                        "Table 17 formerly homeless in PH, Appendix B narrative percentages except the 2025 DC "
                        "gender-of-adults table")
    LOG["checks"] += checks
    # DC: MWCOG vs HUD PIT overall
    hud = {(r["year"]): r["value"] for r in pit_rows if r["coc_code"] == "DC-500"
           and r["measure"] == "pit_overall" and r["population"] == "all"}
    diffs = []
    for r in out:
        if r["measure"] == "mwcog_persons" and r["population"] == "all" and r["coc_code"]:
            h = {(x["coc_code"], x["year"]): x["value"] for x in pit_rows if x["measure"] == "pit_overall"
                 and x["population"] == "all"}.get((r["coc_code"], r["year"]))
            if h is not None and h != r["value"]:
                diffs.append(f"{r['coc_code']} {r['year']}: MWCOG {r['value']:,} vs HUD {h:,}")
    LOG["checks"].append(f"- MWCOG total persons vs HUD PIT overall, CoC-years that differ: {len(diffs)}"
                         + (f": {'; '.join(sorted(diffs))}" if diffs else ""))
    dc = {r["year"]: r["value"] for r in out if r["coc_code"] == "DC-500" and r["measure"] == "mwcog_persons"
          and r["population"] == "all"}
    LOG["checks"].append("- DC-500 MWCOG vs HUD by year: " + ", ".join(
        f"{yr} {dc[yr]:,}/{hud.get(yr, 'n/a')}" for yr in sorted(dc)))
    return out


def mw_sum_check(recs) -> dict:
    """{(year, measure, population): [sum of listed jurisdictions, printed total, n jurisdictions]}"""
    by = defaultdict(lambda: [0, None, 0])
    for jur, yr, ms, pop, val in recs:
        if val is None:
            continue
        k = (yr, ms, pop)
        if jur == "COG region":
            by[k][1] = val
        else:
            by[k][0] += val
            by[k][2] += 1
    return by


def keep_table(recs, pages, tid, title, f, rd, report_year, rows, checks, skipped, block=False):
    """Keep a parsed table. Skip it when it does not parse (no total row, < 8 jurisdictions); keep columns
    whose listed jurisdictions do not add up to the printed total but flag them (source inconsistency)."""
    by = mw_sum_check(recs)
    jurs = {r[0] for r in recs if r[0] != "COG region"}
    if not by or len(jurs) < 8 or any(v[1] is None for v in by.values()):
        skipped.append(f"{tid} ({len(jurs)} jurisdictions, total row {'missing' if by else 'n/a'})")
        checks.append(f"- {tid}: not parsed reliably, skipped")
        return
    bad = {k: v for k, v in by.items() if v[0] != v[1]}
    row_bad = set()
    if block:  # household columns must add up to All Persons within each jurisdiction-year
        cells = defaultdict(dict)
        for jur, yr, ms, pop, val in recs:
            cells[(jur, yr)][pop] = val
        for k, c in cells.items():
            parts = [c.get(x) or 0 for x in ("households_without_children", "households_with_only_children",
                                             "households_with_adults_and_children")]
            if c.get("all") is not None and sum(parts) != c["all"]:
                row_bad.add(k)
    for (jur, yr, ms, pop, val), pg in zip(recs, pages):
        if val is None:
            continue
        r = mw_row(jur, yr, ms, pop, val, f, rd, pg, title, report_year)
        notes = []
        if (yr, ms, pop) in bad:
            v = bad[(yr, ms, pop)]
            notes.append(f"source column does not add up: listed jurisdictions {v[0]:,} vs printed total {v[1]:,}")
        if (jur, yr) in row_bad:
            notes.append("source row does not add up: household columns vs All Persons")
        if notes:
            r["confidence"] = "medium"
            r["x_note"] = "; ".join(notes)
        rows.append(r)
    msg = (f"pass ({len(by)} year/measure columns, {len(jurs)} jurisdictions + total)" if not bad and not row_bad
           else f"kept with flags: {len(bad)}/{len(by)} columns do not add up in the source ("
                + "; ".join(f"{k[0]} {k[2]} {v[0]:,} vs {v[1]:,}" for k, v in list(bad.items())[:3]) + ")"
                + (f"; {len(row_bad)} jurisdiction-years whose household columns do not add up" if row_bad else ""))
    checks.append(f"- {tid}: {msg}")


def mw_row(jur, yr, ms, pop, val, f, rd, page, title, report_year):
    return {
        "coc_code": JUR_TO_COC.get(jur, ""), "jurisdiction": jur, "year": yr, "measure": ms, "population": pop,
        "value": val, "source_id": "doc_mwcog_pit", "retrieved_date": rd, "confidence": "high",
        "basis": "documented", "x_document": rel(f), "x_sheet": "", "x_page": page,
        "x_column_raw": title[:120], "x_count_type": "", "x_note": "", "x_report_year": report_year,
    }


# ===================================================================== 5. EIN matcher (same rule as script 36)
# ---- shared fuzzy-match guard (identical in scripts 36 and 38) ----
GENERIC = set("services service center centre community dc washington district columbia inc foundation house "
              "program programs project housing homes home association of the and for national metropolitan "
              "greater capital area family families women youth health care new".split())
# tokens that, when present on only one side, usually mark a different legal entity
DISTINCT = set("foundation fund development organization auxiliary alumni friends maryland virginia montgomery "
               "prince county chapter pta booster trust endowment memorial loudoun fairfax arlington alexandria frederick "
               "baltimore howard massachusetts ny employee".split())
# words whose presence on only one side does not change the entity (location / legal / generic suffixes)
SOFT = set("dc washington district columbia greater metropolitan metro area national capital region inc the of "
           "and services service center programs program archdiocese".split())
STOP = set("for to in on at by a an the of and".split())
FUZZY_REJECT = {("us helping us", "we helping us"), ("hope home", "new home hope"),
                ("american psychiatric association", "american neuropsychiatric association"),
                ("community empowerment opp", "community empowerment group"),
                ("national capital chapter", "national capital area chapter")}
# acronyms / d.b.a. names of universe orgs that norm_name + fuzzy cannot reach (documented assumption)
MANUAL_ALIASES = [
    (r"^dash$|^dash inc$", ("711019574", "DISTRICT ALLIANCE FOR SAFE HOUSING INC")),
    (r"^dc safe$", ("412226446", "SURVIVORS AND ADVOCATES FOR EMPOWERMENT SAFE INC")),
    (r"^housing up$|transitional housing corporation d b a housing up", ("521675958",
                                                                         "TRANSITIONAL HOUSING CORPORATION")),
    (r"^edgewood brookland$", ("522246995", "EDGEWOOD-BROOKLAND FAMILY SUPPORT COLLABORATIVE")),
    (r"^wanda alston( house)?$", ("463159251", "WANDA ALSTON FOUNDATION")),
]


def _squash(s: str) -> str:
    return "".join(t[:-1] if t.endswith("s") and len(t) > 3 else t for t in s.split())


def fuzzy_ok(q: str, c: str, trunc: bool = False, raw: str = "") -> bool:
    """Guard applied to rapidfuzz token_set_ratio >= 92 hits (q = normalized query, c = normalized candidate).
    trunc: the raw query is long enough to have been cut off by the source (PASS ~30, HIC ~38 characters)."""
    if (q, c) in FUZZY_REJECT:
        return False
    if re.search(r"\b(llc|l\.l\.c|llp|pllc|lp)\b", raw, re.I):   # for-profit firms: exact matches only
        return False
    ql, cl = q.split(), c.split()
    if trunc and ql and ql[-1] not in cl:          # cut-off last word stands for the candidate word it starts
        full = next((x for x in cl if len(ql[-1]) >= 2 and x.startswith(ql[-1])), None)
        if full:
            ql = ql[:-1] + [full]
            q = " ".join(ql)
    if _squash(q) == _squash(c):                    # spacing / plural / apostrophe variants
        return True
    if fuzz.ratio(q, c) >= 95 and q[:4] == c[:4] and len(q) >= 12:   # typos
        return True
    qs, cs = set(ql), set(cl)
    if len(qs) < 2 or len(cs) < 2 or not ((qs & cs) - GENERIC):
        return False
    if (qs ^ cs) & DISTINCT:                        # one-sided entity marker (foundation, county, ...)
        return False
    if fuzz.ratio(q, c) >= 92 and q[:4] == c[:4]:
        return True
    if (cs - qs) <= SOFT and (qs - cs) <= SOFT:     # only location / legal / generic words differ
        return True
    if c.startswith(q + " "):                       # query is the leading part of the candidate name
        qc, cc = qs - STOP, cs - STOP
        core = {t for t in qc - GENERIC - SOFT if len(t) >= 3}
        if len(qc) >= 3 and len(qc) / len(cc) >= 0.6:
            return True
        if trunc and len(core) >= 2:
            return True
    return False


GOV_RX = re.compile(r"\b(dept|department|housing authority|veterans? affairs)\b", re.I)


def load_candidates() -> pd.DataFrame:
    u = pd.read_csv(CLEAN / "dim_universe_membership.csv", dtype=str)
    u = u[u.universe.isin(["dc_sector", "dmv_sector", "core_peers", "calvary"])].copy()
    u["rev"] = pd.to_numeric(u.bmf_revenue_amt, errors="coerce").fillna(0)
    u = u.sort_values(["ein", "universe"]).drop_duplicates("ein")
    u["nn"] = u.org_name_bmf.map(norm_name)
    u["ntok"] = u.nn.str.split().str.len()
    return u[u.nn != ""].reset_index(drop=True)


def clean_org(s: str) -> str:
    s = re.sub(r"\([^)]*(\)|$)", " ", s)
    s = re.sub(r"\s+-\s+(FRSP|RRH|PSH|TH|ES|The)\b.*$", " ", s)  # program suffix after the org name
    return " ".join(s.split()).strip(" ,-")


def expand_last(toks: list[str], cand: list[str]) -> str:
    t = toks[-1]
    if t not in cand and len(t) >= 3:
        full = next((x for x in cand if x.startswith(t)), None)
        if full:
            return " ".join(toks[:-1] + [full])
    return " ".join(toks)


class Matcher:
    def __init__(self):
        self.u = load_candidates()
        self.by_nn = self.u.groupby("nn")
        self.cache = {}

    def match(self, raw: str):
        if raw in self.cache:
            return self.cache[raw]
        c = clean_org(raw)
        nn = norm_name(c)
        res = ("", "unmatched", "", c)
        if re.search(r"community partnership", nn) and re.search(r"preve|direct serv|^community partnership$|tcp", nn + " " + raw.lower()):
            res = (TCP_EIN, "manual_known_ein", 100, c)
        elif any(re.search(rx, nn) for rx, _ in MANUAL_ALIASES):
            res = (next(a for rx, a in MANUAL_ALIASES if re.search(rx, nn))[0], "manual_alias", 100, c)
        elif nn in self.by_nn.groups:
            g = self.u.loc[self.by_nn.groups[nn]].copy()
            g["isdc"] = (g.state == "DC").astype(int)
            g = g.sort_values(["isdc", "rev"], ascending=False)
            res = (g.ein.iloc[0], "exact_norm_name", 100, c)
        elif len(nn.split()) >= 2:
            toks = nn.split()
            pre = self.u[(self.u.ntok >= 2) & (self.u.nn.map(lambda x: fuzz.token_set_ratio(nn, x)) >= 75)].copy()
            # names are cut off in the HIC PDF: let a truncated last token stand for the candidate token it starts
            trunc = len(raw) >= 30  # provider cells are cut at ~38 characters in the HIC PDFs
            pre["exp"] = pre.nn.map(lambda x: expand_last(toks, x.split()) if trunc else nn)
            pre["score"] = [fuzz.token_set_ratio(e, x) for e, x in zip(pre.exp, pre.nn)]
            cand = pre[pre.score >= 92]
            cand = cand[[fuzzy_ok(e, x, trunc=trunc, raw=raw) and (nn, x) not in FUZZY_REJECT
                         for e, x in zip(cand.exp, cand.nn)]].copy()
            if len(cand):
                cand["isdc"] = (cand.state == "DC").astype(int)
                cand["r2"] = cand.nn.map(lambda x: fuzz.ratio(nn, x))
                cand = cand.sort_values(["score", "isdc", "r2", "rev"], ascending=False)
                res = (cand.ein.iloc[0], "fuzzy_token_set", round(float(cand.score.iloc[0]), 1), c)
        self.cache[raw] = res
        return res


# ===================================================================== 6. DC-500 project-level HIC PDFs
HIC_SECTIONS = {"Emergency Shelter": "ES", "Safe Haven": "SH", "Transitional Housing": "TH",
                "Permanent Supportive Housing": "PSH", "Rapid Re-Housing": "RRH", "Other Permanent Housing": "OPH"}
HIC_COLS = ["family_units", "family_beds", "adult_only_beds", "child_only_beds", "seasonal", "overflow_voucher",
            "total_beds", "chronic_beds", "veteran_beds", "youth_beds"]
WOMEN_RX = re.compile(r"\bwom[ae]n'?s?\b|\bfemale\b|\bladies\b|\bgirls?\b", re.I)


def char_rows(chars, tol=2.0):
    rows = []
    for c in sorted(chars, key=lambda c: (round(c["top"], 1), c["x0"])):
        for r in rows:
            if abs(r["top"] - c["top"]) <= tol:
                r["chars"].append(c)
                break
        else:
            rows.append({"top": c["top"], "chars": [c]})
    for r in rows:
        r["chars"].sort(key=lambda c: c["x0"])
    return sorted(rows, key=lambda r: r["top"])


def chars_text(chs) -> str:
    out, prev = "", None
    for c in chs:
        if prev is not None and c["x0"] - prev["x1"] > 1.2 and not out.endswith(" "):
            out += " "
        out += c["text"]
        prev = c
    return " ".join(out.split())


def parse_hic_projects(matcher: Matcher, coc_hic: list[dict]):
    peers = pd.read_csv(CONFIG / "core_peers.csv", dtype=str)
    women_eins = set(peers.loc[peers.tier.str.startswith("1a"), "ein"]) | {"521307706"}
    dv_eins = set(peers.loc[peers.tier.str.startswith("1b"), "ein"])
    out = []
    for y in (2022, 2023, 2024, 2025):
        f = raw_file(f"*_hudx_CoC_HIC_DC-500_{y}.pdf")
        rd = retrieved(f)
        totals, summary = {}, {}
        with pdfplumber.open(f) as pdf:
            for pi, pg in enumerate(pdf.pages):
                sec = facx = unitx = None
                words = None
                seq = 0
                for r in char_rows(pg.chars):
                    t = chars_text(r["chars"])
                    for s, code in HIC_SECTIONS.items():
                        if re.fullmatch(re.escape(s) + r"( Subset of Total Bed Inventory)?", t):
                            sec = code
                    if pi == 0:  # summary page: CoC totals by program type
                        m = re.match(r"^(Emergency Shelter|Safe Haven|Transitional Housing|Permanent Supportive "
                                     r"Housing|Rapid Re-Housing|Other Permanent Housing)\*{0,2}\s+(.+)$", t)
                        if m and len(m.group(2).split()) == 10:
                            summary[HIC_SECTIONS[m.group(1)]] = m.group(2).split()
                        continue
                    if t.startswith("Provider Name"):
                        words = words or pg.extract_words()
                        ws = [w for w in words if abs(w["top"] - r["top"]) < 3]
                        facx = next(w["x0"] for w in ws if w["text"] == "Facility")
                        unitx = next(w["x0"] for w in ws if w["text"].startswith("Units"))
                        continue
                    if facx is None or sec is None:
                        continue
                    prov = chars_text([c for c in r["chars"] if c["x0"] < facx - 1])
                    fac = chars_text([c for c in r["chars"] if facx - 1 <= c["x0"] < unitx - 4])
                    nums = chars_text([c for c in r["chars"] if c["x0"] >= unitx - 4]).split()
                    if len(nums) != 10 or not all(re.fullmatch(r"[\d,]+|n/a", x) for x in nums):
                        continue
                    v = dict(zip(HIC_COLS, (to_int(x) for x in nums)))
                    if prov == "Total" and not fac:
                        totals[sec] = v
                        continue
                    seq += 1
                    ein, method, score, cleaned = matcher.match(prov)
                    fam, adu, chi = (v["family_beds"] or 0), (v["adult_only_beds"] or 0), (v["child_only_beds"] or 0)
                    hh = ("families" if fam and not adu and not chi else "adult_only" if adu and not fam and not chi
                          else "child_only" if chi and not fam and not adu else "mixed" if (fam or adu or chi)
                          else "unspecified_seasonal_overflow")
                    tp, tpb = hh, "derived"
                    if WOMEN_RX.search(prov + " " + fac) and hh in ("adult_only", "families"):
                        tp, tpb = ("single_women" if hh == "adult_only" else "women_with_children"), "inferred"
                    tot = v["total_beds"] or 0
                    for key, lab in (("youth_beds", "youth"), ("veteran_beds", "veterans"), ("chronic_beds", "chronic")):
                        if tot and v[key] == tot:
                            tp += f";{lab}"
                    yr_round = tot - (v["seasonal"] or 0) - (v["overflow_voucher"] or 0)
                    out.append({
                        "year": y, "coc_code": "DC-500", "organization_name": prov, "recipient_ein": ein,
                        "project_name": fac, "project_type": sec, "total_beds": tot, "units": v["family_units"],
                        "target_population": tp, "source_id": "doc_hud_hic_dc500", "retrieved_date": rd,
                        "confidence": "high", "basis": "documented", "x_page": pi + 1, "x_row_seq": seq,
                        "x_year_round_beds": yr_round, "x_beds_hh_children": v["family_beds"],
                        "x_beds_hh_no_children": v["adult_only_beds"], "x_beds_hh_only_children": v["child_only_beds"],
                        "x_seasonal_beds": v["seasonal"], "x_overflow_voucher_beds": v["overflow_voucher"],
                        "x_chronic_beds": v["chronic_beds"], "x_veteran_beds": v["veteran_beds"],
                        "x_youth_beds": v["youth_beds"], "x_household_type": hh, "x_target_population_basis": tpb,
                        "x_org_name_clean": cleaned, "x_match_method": method, "x_match_score": score,
                        "x_org_kind": "government" if GOV_RX.search(cleaned) and not ein else "",
                        "x_women_focused_org": int(ein in women_eins) if ein else 0,
                        "x_dv_focused_org": int(ein in dv_eins) if ein else 0,
                        "x_names_truncated_in_source": 1,
                        "x_document": rel(f),
                    })
        # checks: parsed project sums vs section Total rows, page-1 summary and the CoC workbook
        yrows = [r for r in out if r["year"] == y]
        wb = {(r["measure"]): r["value"] for r in coc_hic if r["coc_code"] == "DC-500" and r["year"] == y
              and r["population"] == "all"}
        for code in HIC_SECTIONS.values():
            prj = [r for r in yrows if r["project_type"] == code]
            if not prj and code not in totals:
                continue
            s_tot = sum(r["total_beds"] for r in prj)
            s_yr = sum(r["x_year_round_beds"] for r in prj)
            t_row = (totals.get(code) or {}).get("total_beds")
            sm = summary.get(code)
            sm_yr = to_int(sm[4]) if sm else None
            wbv = wb.get(f"hic_beds_year_round__{code.lower()}")
            ok = (t_row == s_tot) and (sm_yr in (None, s_yr)) and (wbv in (None, s_yr))
            LOG["checks"].append(f"- HIC projects {y} {code}: {len(prj)} projects; total beds {s_tot:,} vs Total row "
                                 f"{t_row}; year-round {s_yr:,} vs summary p1 {sm_yr} vs CoC workbook {wbv}: "
                                 f"{'pass' if ok else 'FAIL'}")
    return out


# ===================================================================== main
COUNT_FIELDS = ["coc_code", "jurisdiction", "year", "measure", "population", "value", "source_id", "retrieved_date",
                "confidence", "basis", "x_document", "x_sheet", "x_page", "x_column_raw", "x_count_type",
                "x_report_year", "x_note"]
HIC_FIELDS = ["year", "coc_code", "organization_name", "recipient_ein", "project_name", "project_type",
              "total_beds", "units", "target_population", "source_id", "retrieved_date", "confidence", "basis",
              "x_page", "x_row_seq", "x_year_round_beds", "x_beds_hh_children", "x_beds_hh_no_children",
              "x_beds_hh_only_children", "x_seasonal_beds", "x_overflow_voucher_beds", "x_chronic_beds",
              "x_veteran_beds", "x_youth_beds", "x_household_type", "x_target_population_basis", "x_org_name_clean",
              "x_match_method", "x_match_score", "x_org_kind", "x_women_focused_org", "x_dv_focused_org",
              "x_names_truncated_in_source", "x_document"]


def write(path: Path, rows: list[dict], fields: list[str]):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-log", action="store_true", help="do not append to logs/build_log.md (development runs)")
    args = ap.parse_args()
    pit, names = parse_pit()
    hic = parse_hic_coc(names)
    pops = parse_popsub()
    mw = parse_mwcog(pit)
    counts = pit + hic + pops + mw
    key = Counter((r["coc_code"], r["jurisdiction"], r["year"], r["measure"], r["population"], r["source_id"])
                  for r in counts)
    dups = [k for k, n in key.items() if n > 1]
    LOG["checks"].append(f"- stage_homeless_counts duplicate keys (coc, jurisdiction, year, measure, population, "
                         f"source): {len(dups)}" + (f" e.g. {dups[:3]}" if dups else ""))

    # recon cross-checks
    def get(coc, y, meas, pop="all"):
        return next((r["value"] for r in counts if r["coc_code"] == coc and r["year"] == y
                     and r["measure"] == meas and r["population"] == pop), None)
    exp = [("pit_overall", 5138), ("pit_sheltered_es", 3275), ("pit_sheltered_th", 1065), ("pit_unsheltered", 798),
           ("hic_beds_year_round__es_th_sh", 4965), ("hic_beds_year_round__th", 1385),
           ("hic_beds_year_round__psh", 12696), ("hic_beds_year_round__rrh", 6012)]
    res = [f"{m} {get('DC-500', 2025, m)} (exp {e}) {'pass' if get('DC-500', 2025, m) == e else 'FAIL'}" for m, e in exp]
    LOG["checks"].append("- DC-500 2025 recon values: " + "; ".join(res))

    matcher = Matcher()
    proj = parse_hic_projects(matcher, hic)
    pk = Counter((r["year"], r["project_type"], r["x_page"], r["x_row_seq"]) for r in proj)
    LOG["checks"].append(f"- stage_hic_projects duplicate keys (year, type, page, seq): {sum(1 for n in pk.values() if n > 1)}")
    cal = [r for r in proj if r["recipient_ein"] == "521307706"]
    c25 = sorted((r["project_type"], r["project_name"], r["total_beds"]) for r in cal if r["year"] == 2025)
    exp25 = sorted([("TH", "CWS - Transitional Housing -", 45), ("TH", "CWS - Reach Up OVSJG - T", 18),
                    ("TH", "CWS - New Foundations - TH", 17), ("TH", "CWS - Reach Up - TH IND -", 8),
                    ("TH", "CWS - Reach Up - TH IND -", 6), ("PSH", "CWS - Sister Circle - PSH IN", 16),
                    ("RRH", "CWS - Reach Up - RRH IND", 14)])
    sr24 = [r["total_beds"] for r in cal if r["year"] == 2024 and "Sisters Rise" in r["project_name"]]
    LOG["checks"].append(f"- Calvary HIC 2025 rows {c25 == exp25 and 'pass' or 'FAIL'} ({len(c25)} projects, "
                         f"{sum(x[2] for x in c25)} beds); 2024 Sisters Rise PSH {sr24} (exp [24])")

    write(OUT_COUNTS, counts, COUNT_FIELDS)
    write(OUT_HIC, proj, HIC_FIELDS)

    # match stats
    orgs = {}
    for r in proj:
        orgs.setdefault(r["x_org_name_clean"].lower(), r)
    n_org = len(orgs)
    n_m = sum(1 for r in orgs.values() if r["recipient_ein"])
    beds = sum(r["total_beds"] for r in proj)
    beds_m = sum(r["total_beds"] for r in proj if r["recipient_ein"])
    meth = Counter(r["x_match_method"] for r in orgs.values())
    gov = sum(1 for r in orgs.values() if r["x_org_kind"] == "government")
    fz = sorted({(r["organization_name"], r["recipient_ein"], r["x_match_score"]) for r in proj
                 if r["x_match_method"] == "fuzzy_token_set"})
    um = sorted({r["x_org_name_clean"] for r in proj if not r["recipient_ein"] and r["x_org_kind"] != "government"})
    LOG["match"].append(f"- HIC provider names (cleaned, distinct): {n_org}; matched {n_m} ({n_m / n_org:.0%}); "
                        f"methods {dict(meth)}; government providers (no EIN expected) {gov}; "
                        f"beds at matched providers {beds_m:,} of {beds:,} ({beds_m / beds:.0%})")
    LOG["match"].append("- fuzzy matches: " + "; ".join(f"{a} -> {b} ({s})" for a, b, s in fz))
    LOG["match"].append("- unmatched nonprofit providers (not in dc_sector/dmv_sector/core_peers by name): "
                        + "; ".join(um))
    LOG["match"].append("- matcher (shared with script 36): manual aliases (TCP 521681401; DASH, DC SAFE, Housing Up), "
                        "norm_name exact, then rapidfuzz token_set_ratio >= 92 (after expanding a truncated last "
                        "token for raw names >= 30 chars) accepted only when fuzzy_ok() holds: both names >= 2 "
                        "tokens, a shared non-generic token, no one-sided entity-marker token (foundation, fund, "
                        "maryland, county, ...), and token containment (ratio >= 0.5) or prefix or only soft "
                        "one-sided words or fuzz.ratio >= 90; reviewed reject list")

    by_src = Counter(r["source_id"] for r in counts)
    text = [f"- wrote {rel(OUT_COUNTS)}: {len(counts):,} rows ({dict(by_src)}); PIT {len(pit):,}, HIC by CoC "
            f"{len(hic):,}, PopSub {len(pops)}, MWCOG {len(mw)}",
            f"- wrote {rel(OUT_HIC)}: {len(proj):,} rows (" + ", ".join(
                f"{y}: {sum(1 for r in proj if r['year'] == y)}" for y in (2022, 2023, 2024, 2025)) + ")",
            "- HIC project PDFs: provider and facility names are truncated in the PDF itself (fixed-width "
            "report cells; same text in pdfplumber chars, pypdf and pdftotext); kept as printed. 'units' = family "
            "units (HIC reports units only for households with children). target_population is derived from "
            "the bed columns (household type, plus youth/veterans/chronic when all beds are dedicated) and "
            "set to single_women / women_with_children only when the provider or project name says women "
            "(basis in x_target_population_basis). x_women_focused_org = core peer tier 1a or Calvary; "
            "x_dv_focused_org = tier 1b (config/core_peers.csv)."]
    for k in ("pit", "hic", "popsub", "mwcog", "match", "checks"):
        text += LOG[k]
    if not args.no_log:
        log(SEC, "\n".join(text))
    print("\n".join(text))


if __name__ == "__main__":
    main()
