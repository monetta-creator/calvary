"""Phase 4 web staging: fact_grants rows from Calvary's site, core-peer supporter lists and funder grant
lists, plus in-kind evidence for assumption A2.

Reads
  interim/web_calvary_funders.csv   (script 43: Calvary support page, annual reports, sponsor lists, posts)
  interim/web_pages.csv + raw files (script 44: peer and funder pages)
  config/web_queries.yaml           (per-page parse specs: peers[].pages[].parse, funders[].pages[].parse,
                                     recipients, inkind_evidence)
  config/core_peers.csv             (recipient EINs)
Writes
  interim/stage_fact_grants__web.csv   one row per funder -> recipient -> year mention (fact_grants columns)
  interim/web_inkind_evidence.csv      funder, finding, evidence_url, quote (<= 200 chars), classification
  interim/web_peer_donor_band_counts.csv  entries not identified as organizations, counted per band (no names)
  interim/web_parse_report.csv         per-page parse counts (QC)

Parse types (config `parse:` entries)
  layout_columns  multi-column PDF donor lists (pdftotext -layout); column starts detected per page;
                  indented lines are continuations; "$X+" style lines are gift bands
  lines           one entry per text line between start/end (HTML honor rolls); band lines as above
  md_table        Tavily markdown table rows "| [Name](url) | purpose | period | area | $amount |"
  records         line records anchored on a date line (Graham Fund layout); field offsets in config
  blocks          name = the line before an anchor line (e.g. GWCF partner Q&A pages); context lines after
  explicit        hand-listed mentions, each verified against the page text with a regex (press releases)

Rules
  - Peer pages: entries are funders, recipient = the peer. Funder pages: entries are recipients; keep rows
    naming Calvary or a core peer; when the list has < 300 rows and whole_list: true, also keep DC
    homelessness / DV / women's-services grantees (keyword test on name + context).
  - Individuals are never stored: entries failing the organization test are only counted per band.
  - amount only when stated; else band; else amount_kind=unknown. funder_ein left blank (Phase 5).
  - confidence: high when the funder itself states the amount; medium for named lists and
    recipient-stated amounts; low for single-source inferences flagged in notes.
"""
from __future__ import annotations

import csv
import importlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import (CONFIG, INTERIM, ROOT, append_md, log, norm_ein, norm_name,  # noqa: E402
                        today)
from lib.tagging import tag_text  # noqa: E402

W43 = importlib.import_module("43_web_calvary")
RETRIEVED = today()
CALVARY_EIN = "521307706"
STAGE = INTERIM / "stage_fact_grants__web.csv"
FIELDS = ["grant_id", "funder_id", "funder_ein", "funder_name_raw", "recipient_ein", "recipient_name_raw",
          "recipient_name_norm", "recipient_city", "recipient_state", "recipient_zip5", "tax_year", "fiscal_year",
          "grant_date", "year_basis", "amount", "amount_band_min", "amount_band_max", "amount_kind",
          "cumulative_flag", "purpose_text", "program_area_tags", "source_type", "object_id", "source_id",
          "match_method", "match_score", "retrieved_date", "confidence", "basis",
          "x_report_year", "x_gift_band_raw", "x_section", "x_in_kind_flag", "x_page_id", "x_source_url",
          "x_recipient_key", "x_whole_list_keep", "x_notes"]
BAND = re.compile(r"^\$\s?[\d,]+(?:\.\d+)?\s*(?:\+|and above|and up|or more|plus)?(?:\s*(?:-|–|—|to)\s*\$?\s?[\d,]+)?\s*"
                  r"(?:\+)?$|^(?:gifts? of )?up to \$[\d,]+$|^under \$[\d,]+$", re.I)
BAND_PREFIX = re.compile(r"^(\$\s?[\d,]+\s*(?:\+|and above|or more|(?:-|–|—|to)\s*\$?\s?[\d,]+))\s+(\S.*)$")
WHOLE_STRONG = re.compile(r"homeless|shelter|domestic violence|intimate partner|survivors? of|sexual assault|"
                          r"trafficking|transitional housing|supportive housing|eviction", re.I)
WHOLE_KW = re.compile(r"homeless|shelter|domestic violence|intimate partner|\bDV\b|survivors?\b|sexual assault|"
                      r"trafficking|\bwomen\b|\bwoman\b|\bwomen.s\b|transitional housing|supportive housing|"
                      r"house of ruth|eviction", re.I)


# ---------------------------------------------------------------- recipients
def load_recipients(q: dict) -> dict[str, dict]:
    peers = {}
    with open(CONFIG / "core_peers.csv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            peers[norm_ein(r["ein"])] = r["name"]
    rec = {"calvary": dict(ein=CALVARY_EIN, name="Calvary Women's Services", city="Washington", state="DC",
                           alias=re.compile(q["recipients"]["calvary"], re.I))}
    for p in q["peers"]:
        alias = q["recipients"].get(p["id"])
        if alias:
            rec[p["id"]] = dict(ein=norm_ein(p["ein"]), name=peers.get(norm_ein(p["ein"]), p["name"]),
                                city="", state="", alias=re.compile(alias, re.I))
    return rec


def match_recipient(name: str, rec: dict) -> str | None:
    for k, r in rec.items():
        if r["alias"].search(name):
            return k
    return None


# ---------------------------------------------------------------- helpers
def money(s) -> int | None:
    if s is None:
        return None
    m = re.search(r"\$?\s?([\d,]+(?:\.\d+)?)\s*(million|m\b|k\b)?", str(s), re.I)
    if not m:
        return None
    v = float(m.group(1).replace(",", ""))
    if m.group(2) and m.group(2).lower() in ("million", "m"):
        v *= 1_000_000
    elif m.group(2) and m.group(2).lower() == "k":
        v *= 1_000
    return int(round(v))


def band_bounds(raw: str):
    lo, hi = W43.band_bounds(raw)
    if lo == "" and hi == "":
        m = re.match(r"^\$\s?([\d,]+)\s*\+?$", raw.strip())
        if m:
            lo = int(m.group(1).replace(",", ""))
    return lo, hi


def clean_entry(t: str) -> tuple[str, str]:
    """Strip markers and parenthetical notes; returns (name, note)."""
    note = []
    t = t.replace("’", "'").replace("‘", "'")
    for m in re.findall(r"\(([^)]*)\)", t):
        if re.search(r"employee|match|in[- ]kind|pro bono|in memory|in honor|gifts?|\d", m, re.I):
            note.append(m)
            t = t.replace(f"({m})", "")
    m = re.search(r"\s+(in memory of|in honor of|in honour of|honoring|remembering|in loving memory)\b.*$", t, re.I)
    if m:
        t = t[:m.start()]
        note.append("tribute text removed (names an individual)")
    t = re.sub(r"[*†‡^]+", "", t)
    t = re.sub(r"\s+", " ", t).strip(" ,;.-–•·|")
    return t, "; ".join(note)


HEADING_WORDS = re.compile(r"\b(DONORS?|GIFTS|COMMITTEE|COUNCIL|GROUPS|SPOTLIGHT|AMBASSADORS|PARTNERS|SUPPORTERS|"
                           r"SPONSORS?|VOLUNTEERS?|THANK|SOCIETY|CIRCLE|MEMBERS|LEADERSHIP|BOARD|STAFF|REPORT|CLUBS|"
                           r"FAITH|GIVING|FUNDERS|GRANT|FEDERAL|STATE|LOCAL|BASED|FUNDING|SUPPORT|CORPORATE|INDIVIDUAL|"
                           r"ORGANIZATIONS|BUSINESSES|FOUNDATIONS|GOVERNMENT|HONOR|ROLL)\b")


def not_a_name(n: str, strict: bool = True) -> bool:
    """Narrative fragments, headings and reversed graphic text are not donor names. strict=False (funder
    grantee lists) skips the all-caps heading tests, which would drop names such as "DC SAFE"."""
    if len(n) > 90 or re.search(r"[“”\"~:;!?]|\.\s+[A-Z]|\b(I|we|our|you|your|us)\b", n):
        return True
    if n[:1].islower() or re.search(r"(&|,| and| of| the)$", n) or re.search(r"www\.|\.org/|\.com/|https?:", n):
        return True
    if not strict:
        return False
    letters = [c for c in n if c.isalpha()]
    if letters and all(c.isupper() for c in letters) and len(n.split()) == 1 and len(letters) > 6:
        return True  # a single capitalized heading word ("LEADERSHIP"); acronyms are short
    if letters and all(c.isupper() for c in letters) and len(n.split()) >= 2:
        if HEADING_WORDS.search(n) or not W43.ORG_KW.search(n):
            return True
    return False


def year_of(s) -> int | None:
    m = re.search(r"(20\d\d)", str(s or ""))
    return int(m.group(1)) if m else None


def date_iso(s) -> str:
    m = re.search(r"(\d{1,2})/(\d{1,2})/(20\d\d)", str(s or ""))
    return f"{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}" if m else ""


# ---------------------------------------------------------------- parsers -> entries
# entry: dict(name, band, amount, year, date, purpose, context, section, note)
def region(text: str, spec: dict) -> str:
    lines = text.split("\n")
    i0 = 0
    if spec.get("start"):
        i0 = next((i for i, l in enumerate(lines) if re.search(spec["start"], l.lstrip("\f"))), None)
        if i0 is None:
            return ""
    i1 = len(lines)
    if spec.get("end"):
        i1 = next((i for i in range(i0 + 1, len(lines)) if re.search(spec["end"], lines[i].lstrip("\f"))),
                  len(lines))
    return "\n".join(lines[i0:i1])


def p_layout_columns(text: str, spec: dict) -> list[dict]:
    reg = region(text, spec)
    skip = re.compile(spec.get("skip", r"(?!x)x"), re.I)
    min_gap = spec.get("min_gap", 2)
    out, band, section = [], spec.get("band", ""), spec.get("section", "")
    for page in reg.split("\f"):
        lines = [l.rstrip() for l in page.split("\n")]
        chunks = []  # (line_no, start_col, text)
        for ln, l in enumerate(lines):
            pos = 0
            for part in re.split(r"(\s{%d,})" % min_gap, l):
                if part and not part.isspace():
                    chunks.append((ln, pos, part.strip()))
                pos += len(part)
        if not chunks:
            continue
        starts = Counter(c[1] for c in chunks)
        thr = max(3, int(spec.get("col_min_share", 0.08) * len(set(c[0] for c in chunks))))
        cand = sorted(s for s, n in starts.items() if n >= thr)
        cols = []
        for s in cand:  # merge starts within 5 chars (continuation indents)
            if not cols or s - cols[-1] > spec.get("indent_max", 5):
                cols.append(s)
        if not cols:
            cols = [0]

        def col_of(pos):
            k = 0
            for i, s in enumerate(cols):
                if pos >= s - 1:
                    k = i
            return k
        bycol = defaultdict(list)
        for ln, pos, t in chunks:
            c = col_of(pos)
            bycol[c].append((ln, pos - cols[c], t))
        for c in sorted(bycol):
            prev = None
            for ln, indent, t in sorted(bycol[c]):
                if skip.search(t):
                    prev = None
                    continue
                bp = BAND_PREFIX.match(t)
                if bp and not BAND.match(t):
                    band, prev, t = bp.group(1).strip(), None, bp.group(2).strip()
                if BAND.match(t) or (spec.get("band_re") and re.search(spec["band_re"], t)):
                    band, prev = t, None
                    continue
                if re.search(spec.get("section_re", r"(?!x)x"), t):
                    prev, band, section = None, spec.get("section_band", ""), t
                    continue
                cont = indent >= 2 or t[:1].islower() or bool(CONT_WORD.match(t)) or \
                    (prev is not None and re.search(r"(&|\band|\bof|\bthe|,|/|-)$", prev["name"]))
                if cont and prev is not None and ln - prev["_ln"] <= 2:
                    prev["name"] += " " + t
                    prev["parts"].append(t)
                    prev["_ln"] = ln
                    continue
                prev = dict(name=t, band=band, _ln=ln, section=section, parts=[t])
                out.append(prev)
    return merge_wraps(out) if spec.get("merge_wraps", True) else out


def person_like(t: str) -> bool:
    """A fragment that reads as a personal name ("Kim Clendenin", "Mary & John Smith")."""
    toks = t.replace(",", " ").split()
    if not 1 <= len(toks) <= 5 or W43.ORG_KW.search(t):
        return False
    return all(re.fullmatch(r"[A-Z][a-z'’\-]+|[A-Z]\.?|and|&|Dr\.?|Jr\.?|Sr\.?|II|III|Mc[A-Z][a-z]+", x) for x in toks)


def strip_person_prefix(e: dict) -> tuple[str, str]:
    """If a wrapped entry starts with a personal-name fragment followed by an organization, keep the
    organization only (people-data rule)."""
    parts = e.get("parts") or [e.get("name", "")]
    if len(parts) > 1 and person_like(parts[0]):
        rest = " ".join(parts[1:])
        if W43.is_org_name(clean_entry(rest)[0]):
            return rest, "leading personal-name fragment removed"
        return "", ""
    return e.get("name", ""), ""


def merge_wraps(entries: list[dict]) -> list[dict]:
    """Join a non-organization fragment with the next entry when the joined text reads as an organization
    ("Greater Washington" + "Community Foundation"; "Aluise Friend Family" + "Charity Fund")."""
    out = []
    i = 0
    while i < len(entries):
        e = entries[i]
        if i + 1 < len(entries):
            n = entries[i + 1]
            joined = e["name"] + " " + n["name"]
            near = abs(n.get("_ln", 0) - e.get("_ln", 0)) <= 2 and n.get("band") == e.get("band")
            # only join when the second fragment is a generic organizational tail ("Community Foundation") or the
            # first ends with a connector; never glue a person's name onto an organization ("X Y" + "Seekers Church")
            tail_ok = bool(CONT_WORD.match(n["name"])) or bool(re.search(r"(&|\band|\bof|\bthe|,|/|-)$", e["name"]))
            if near and tail_ok and not W43.is_org_name(clean_entry(e["name"])[0]) and \
                    W43.is_org_name(clean_entry(joined)[0]) and \
                    (not person_like(e["name"]) or re.search(r"(&|\band|\bof|\bthe|,|/|-)$", e["name"])):
                out.append(dict(e, name=joined, parts=e.get("parts", [e["name"]]) + n.get("parts", [n["name"]])))
                i += 2
                continue
        out.append(e)
        i += 1
    return out


def p_lines(text: str, spec: dict) -> list[dict]:
    reg = region(text, spec)
    skip = re.compile(spec.get("skip", r"(?!x)x"), re.I)
    out, band, section = [], spec.get("band", ""), spec.get("section", "")
    for l in reg.split("\n")[0 if spec.get("include_start") else 1:]:
        t = l.strip()
        if not t or skip.search(t):
            continue
        if BAND.match(t) or (spec.get("band_re") and re.search(spec["band_re"], t)):
            band = t
            continue
        if spec.get("section_re") and re.search(spec["section_re"], t):
            section = t
            continue
        parts = re.split(spec["split"], t) if spec.get("split") else [t]
        for p in parts:
            p = p.strip()
            if not p:
                continue
            if out and re.search(r"(&|\band|\bof|,)$", out[-1]["name"]) and out[-1]["band"] == band:
                out[-1]["name"] += " " + p
                out[-1]["parts"].append(p)
                continue
            out.append(dict(name=p, band=band, section=section, parts=[p]))
    return merge_wraps(out) if spec.get("merge_wraps", True) else out


CONT_WORD = re.compile(r"^(?:(?:Community|Family|Charitable|Memorial|Charity|Employee|Gift)\s+)*(?:Foundation|Fund|Trust|"
                       r"Gift Fund|Giving Program|Giving Fund|Giving Campaign|Program|Campaign|Incorporated|Inc\.?|LLC|"
                       r"LLP|Corporation|Company|Associates|Endowment)(?:\b[,.]?.{0,25})?$|^Capital Area$")
GENERIC = re.compile(r"^(the )?(foundation|fund|trust|charitable fund|inc\.?|llc|llp|of donors|donors|supporters|"
                     r"partners|sponsors|thank you|association|corporation|company|in-kind.*|businesses|"
                     r"foundations?|corporate partners?|government|communications|community foundation|giving|"
                     r"development|(fund|foundation|trust),? inc\.?|county,? inc\.?|.*giving monthly donations|"
                     r"(family|charitable|memorial|endowment|services endowment|scholarship)\s+(foundation|fund)(,? inc\.?)?|"
                     r"donate|healthcare|housing|incorporated|management|programs?|circle|healing)$",
                     re.I)
MD_ROW = re.compile(r"^\|\s*\[([^\]]+)\]\([^)]*\)\s*\|(.*)\|\s*$")


def p_md_table(text: str, spec: dict) -> list[dict]:
    out = []
    for l in region(text, spec).split("\n"):
        m = MD_ROW.match(l.strip())
        if not m:
            continue
        cells = [c.strip() for c in m.group(2).split("|")]
        e = dict(name=m.group(1).strip())
        for k, idx in spec["cols"].items():
            e[k] = cells[idx] if idx < len(cells) else ""
        out.append(e)
    return out


def p_records(text: str, spec: dict) -> list[dict]:
    lines = [l.strip() for l in region(text, spec).split("\n") if l.strip()]
    anc = re.compile(spec["anchor"])
    out = []
    for i, l in enumerate(lines):
        if anc.fullmatch(l):
            e = {}
            for k, off in spec["fields"].items():
                j = i + off
                e[k] = lines[j] if 0 <= j < len(lines) else ""
            out.append(e)
    return out


def p_blocks(text: str, spec: dict) -> list[dict]:
    lines = [l.strip() for l in region(text, spec).split("\n") if l.strip()]
    anc = re.compile(spec["anchor"])
    out = []
    for i, l in enumerate(lines):
        if anc.search(l) and i > 0:
            out.append(dict(name=lines[i - 1], context=" ".join(lines[i + 1:i + 1 + spec.get("context_lines", 3)])))
    return out


def p_explicit(text: str, spec: dict) -> list[dict]:
    flat = re.sub(r"\s+", " ", text)
    out = []
    for r in spec["rows"]:
        m = re.search(r["verify"], flat)
        if not m:
            out.append(dict(name=r.get("name", ""), _failed=f"verify regex not found: {r['verify'][:60]}"))
            continue
        e = {k: v for k, v in r.items() if k != "verify"}
        e["quote"] = m.group(0)[:200]
        out.append(e)
    return out


PARSERS = {"layout_columns": p_layout_columns, "lines": p_lines, "md_table": p_md_table, "records": p_records,
           "blocks": p_blocks, "explicit": p_explicit}


# ---------------------------------------------------------------- rows
def base_row(**kw) -> dict:
    r = {k: "" for k in FIELDS}
    r.update(year_basis="report_year", retrieved_date=RETRIEVED, basis="documented", **kw)
    return r


def set_recipient(r: dict, key: str | None, rec: dict, raw_name: str):
    r["recipient_name_raw"] = raw_name
    r["recipient_name_norm"] = norm_name(raw_name)
    if key:
        r["recipient_ein"] = rec[key]["ein"]
        r["recipient_city"] = rec[key]["city"]
        r["recipient_state"] = rec[key]["state"]
        r["match_method"] = "alias_regex" if key != "calvary" or "calvary" in norm_name(raw_name) else "subject"
        r["x_recipient_key"] = key


def calvary_rows(rec: dict) -> tuple[list[dict], dict]:
    rows, stats = [], Counter()
    p = INTERIM / "web_calvary_funders.csv"
    if not p.exists():
        return rows, stats
    with open(p, newline="", encoding="utf-8") as f:
        src = list(csv.DictReader(f))
    for s in src:
        name, note = clean_entry(s["funder_name_raw"])
        if not name or name.lower().startswith("anonymous"):
            stats["anonymous_skipped"] += 1
            continue
        sid = s["source_id"]
        if sid == "web_calvary_corp_found_support":
            st, cum = "support_page", 1
        elif "annual_report" in sid:
            st, cum = "annual_report", 0
        else:
            st, cum = "web", 1 if re.search(r"cumulative|over the years|since", s["section_heading"] + s["notes"], re.I) else 0
        r = base_row(funder_name_raw=name, source_type=st, source_id=sid, cumulative_flag=cum,
                     x_report_year=s["report_year"], x_gift_band_raw=s["gift_band_raw"],
                     x_section=s["section_heading"], x_in_kind_flag=s["in_kind_flag"], x_source_url=s["document"]
                     if s["document"].startswith("http") else "", x_notes="; ".join(x for x in (s["notes"], note) if x))
        set_recipient(r, "calvary", rec, "Calvary Women's Services")
        r["match_method"] = "subject"
        if s["fiscal_year"]:
            r["fiscal_year"] = s["fiscal_year"]
            r["tax_year"] = int(s["fiscal_year"]) - 1
        else:
            r["fiscal_year"] = s["report_year"]
        lo, hi = s["band_min"], s["band_max"]
        if lo and hi and lo == hi:  # a stated amount (posts)
            r["amount"] = lo
        else:
            r["amount_band_min"], r["amount_band_max"] = lo, hi
        ik = str(s["in_kind_flag"]).lower() == "true"
        if s.get("cumulative_hint"):
            r["cumulative_flag"] = 1 if str(s["cumulative_hint"]).lower() == "true" else 0
        if s.get("quote"):
            r["x_notes"] = (r["x_notes"] + f"; quote: {s['quote']}").strip("; ")
        if s.get("amount_kind_hint"):
            r["amount_kind"] = s["amount_kind_hint"]
        elif ik and st == "support_page":
            r["amount_kind"] = "mixed"
            r["x_notes"] = (r["x_notes"] + "; marked * 'includes in-kind contributions'").strip("; ")
        elif ik:
            r["amount_kind"] = "noncash"
        elif re.search(r"in-kind|donated .*items|goods", s["notes"], re.I) and not re.search(r"grants? and in-kind",
                                                                                          s["notes"], re.I):
            r["amount_kind"] = "noncash"
        elif re.search(r"grants? and in-kind", s["notes"], re.I):
            r["amount_kind"] = "mixed"
        elif r["amount"] and re.search(r"grant", s["notes"] + s["section_heading"], re.I):
            r["amount_kind"] = "cash"
        else:
            r["amount_kind"] = "unknown"
        r["confidence"] = "medium"
        r["purpose_text"] = s.get("purpose_hint") or (s["notes"] if re.search(r"support|program|launch|fund", s["notes"],
                                                                              re.I) and st != "support_page" else "")
        r["program_area_tags"] = tag_text(r["purpose_text"], default_other=False) if r["purpose_text"] else ""
        rows.append(r)
        stats[st] += 1
    return rows, stats


def page_rows(pg: dict, idx: dict, rec: dict, q: dict) -> tuple[list[dict], dict, list[dict]]:
    """Rows for one configured page. Returns (rows, report, band_counts)."""
    rep = dict(page_id=pg["id"], group=pg["group"], entity=pg["entity_id"], entries=0, kept=0, orgs_dropped=0,
               not_matched=0, status="")
    meta = idx.get(pg["id"])
    if not meta or not meta.get("raw_path"):
        rep["status"] = "not fetched"
        return [], rep, []
    text = page_text(meta)
    rows, bands = [], Counter()
    for spec in pg.get("parse", []):
        entries = PARSERS[spec["type"]](text, spec)
        rep["entries"] += len(entries)
        n_total = len(entries)
        for e in entries:
            if e.get("_failed"):
                rep["status"] += e["_failed"] + "; "
                continue
            raw, pnote = strip_person_prefix(e)
            name, note = clean_entry(raw)
            mm = re.match(r"^(.+?)\s+(?:and|&)\s+(.+)$", name)
            if mm and person_like(mm.group(1)) and len(mm.group(1).split()) >= 2:
                if W43.is_org_name(mm.group(2)) and not person_like(mm.group(2)):
                    name, pnote = mm.group(2), "leading personal name removed"
                elif not re.search(r"foundation|fund|trust", name, re.I):
                    continue  # "<person> and <fragment>": not an organization
            note = "; ".join(x for x in (note, pnote) if x)
            if not name or name.lower().startswith("anonymous") or GENERIC.match(name) or \
                    not_a_name(name, strict=pg["group"] == "peer"):
                continue
            if pg["group"] == "peer" and pg["entity_id"] in rec and rec[pg["entity_id"]]["alias"].search(name):
                continue  # the peer itself ("House of Ruth Board & Staff")
            year = e.get("year") or year_of(e.get("period")) or year_of(e.get("date")) or spec.get("year") or \
                pg.get("year")
            if spec.get("min_year") and year and int(year) < spec["min_year"]:
                continue
            if spec.get("keep_bands") is False:
                e["band"] = ""
            amount = money(e.get("amount")) if e.get("amount") not in (None, "") else None
            band = e.get("band", "") or spec.get("band", "")
            lo, hi = band_bounds(band) if band else ("", "")
            r = base_row(source_id=meta["source_id"], x_page_id=pg["id"], x_source_url=pg["url"],
                         x_report_year=pg.get("year") or year or "", x_gift_band_raw=band,
                         x_section=spec.get("section") or e.get("section", "") or spec.get("heading", ""),
                         fiscal_year=year or "", grant_date=date_iso(e.get("date")),
                         cumulative_flag=1 if (spec.get("cumulative") or re.search(r"over (two|three|\d) years|"
                                                                                 r"multi-?year", str(e.get("purpose", "")),
                                                                                 re.I)) else 0)
            if r["grant_date"]:
                r["year_basis"] = "award_year"
            purpose = e.get("purpose", "") or spec.get("purpose", "")
            r["purpose_text"] = re.sub(r"\s+", " ", purpose).strip()[:300]
            r["program_area_tags"] = tag_text(r["purpose_text"] + " " + e.get("context", ""), default_other=False)
            notes = [x for x in (note, e.get("note", ""), spec.get("note", ""),
                                 f"quote: {e['quote']}" if e.get("quote") else "") if x]
            if pg["group"] == "peer":
                # entries are funders; the peer is the recipient
                if not (spec.get("org_list") and not W43.PERSONISH.search(name)) and not W43.is_org_name(name):
                    rep["orgs_dropped"] += 1
                    bands[(band or "(no band)", lo, hi)] += 1
                    continue
                r["funder_name_raw"] = e.get("funder", name) if spec["type"] == "explicit" else name
                key = pg["entity_id"]
                set_recipient(r, key, rec, e.get("recipient", pg["entity_name"]) if spec["type"] == "explicit"
                              else rec[key]["name"] if key in rec else pg["entity_name"])
                r["match_method"] = "page_owner"
                r["source_type"] = spec.get("source_type") or ("annual_report" if pg.get("kind") == "annual_report"
                                                              else "support_page" if pg.get("kind") == "support_page"
                                                              else "web")
                r["confidence"] = spec.get("confidence", "medium")
            else:
                # entries are recipients; the page's funder is the funder
                key = e.get("recipient_key") or match_recipient(name, rec)
                ctx = e.get("context", "") + " " + purpose
                keep_whole = bool(spec.get("whole_list") and n_total < 300 and
                                  (WHOLE_KW.search(name) or WHOLE_STRONG.search(ctx)))
                if keep_whole and e.get("location") and not re.search(r"Washington, DC|District of Columbia",
                                                                       e["location"]):
                    keep_whole = False  # whole-list keeps are limited to DC grantees when a location is given
                if not key and not keep_whole:
                    rep["not_matched"] += 1
                    continue
                r["funder_name_raw"] = e.get("funder") or spec.get("funder") or pg.get("funder_name") or \
                    pg["entity_name"]
                set_recipient(r, key, rec, name)
                if not key:
                    r["match_method"] = "whole_list_keyword"
                    r["x_whole_list_keep"] = 1
                    if e.get("location"):
                        r["recipient_city"] = e["location"].split(",")[0].strip()
                        st = re.search(r",\s*([A-Z]{2})\b", e["location"])
                        r["recipient_state"] = st.group(1) if st else ("DC" if "District of Columbia" in
                                                                         e["location"] else "")
                r["source_type"] = spec.get("source_type", "web")
                r["confidence"] = spec.get("confidence") or ("high" if amount is not None else "medium")
                if key and spec.get("ambiguous", {}).get(key):
                    notes.append(spec["ambiguous"][key])
                    r["confidence"] = "medium"
            if re.search(r"in-kind|in kind", str(e.get("section", "")), re.I):
                e.setdefault("amount_kind", "noncash")
                notes.append("listed under an in-kind section")
            if amount is not None:
                r["amount"] = amount
                r["amount_kind"] = e.get("amount_kind") or spec.get("amount_kind", "cash")
            else:
                r["amount_band_min"] = e.get("amount_band_min", lo)
                r["amount_band_max"] = e.get("amount_band_max", hi)
                r["amount_kind"] = e.get("amount_kind") or spec.get("amount_kind_no_amount", "unknown")
            r["x_notes"] = "; ".join(notes)
            rows.append(r)
    rep["kept"] = len(rows)
    rep["status"] = rep["status"] or "ok"
    band_rows = [dict(source_id=meta["source_id"], page_id=pg["id"], recipient=pg["entity_name"],
                      report_year=pg.get("year", ""), gift_band_raw=b, band_min=lo, band_max=hi,
                      entries_not_identified_as_orgs=n) for (b, lo, hi), n in bands.items()]
    return rows, rep, band_rows


def page_text(meta: dict) -> str:
    p = ROOT / meta["raw_path"]
    if p.suffix == ".pdf":
        return W43.pdf_text(p)
    if p.suffix == ".json":
        d = json.loads(p.read_text(encoding="utf-8"))
        return "\n\n".join((r.get("raw_content") or "") for r in d.get("results", []))
    return W43.html_text(p.read_bytes())


# ---------------------------------------------------------------- in-kind evidence
def inkind_rows(q: dict, idx: dict) -> list[dict]:
    out = []
    for ev in q.get("inkind_evidence", []):
        meta = idx.get(ev["page_id"]) if ev.get("page_id") else None
        if ev.get("page_id") and ev["page_id"].startswith("calvary_"):
            p = INTERIM / "web_text" / f"{ev['page_id']}.txt"
            text = p.read_text(encoding="utf-8") if p.exists() else ""
        elif meta and meta.get("raw_path"):
            text = page_text(meta)
        else:
            text = ""
        flat = re.sub(r"\s+", " ", text)
        m = re.search(ev["quote_re"], flat) if text and ev.get("quote_re") else None
        out.append(dict(funder=ev["funder"], crm_gift_total=ev.get("crm_gift_total", ""), finding=ev["finding"],
                        evidence_url=ev["url"], quote=(m.group(0)[:200] if m else ""),
                        classification=ev["classification"], confidence=ev.get("confidence", "medium"),
                        source_id=(meta or {}).get("source_id", ev.get("source_id", "")),
                        retrieved_date=RETRIEVED, notes=ev.get("notes", "") + ("" if m else
                                                                               " [quote regex not matched]")))
    return out


def dry_run(page_id: str):
    """Print the parsed rows for one page (development aid): --page ID"""
    q = W43.load_queries()
    rec = load_recipients(q)
    with open(INTERIM / "web_pages.csv", newline="", encoding="utf-8") as f:
        idx = {r["page_id"]: r for r in csv.DictReader(f)}
    pp = q.get("page_parse", {}) or {}
    for grp, key in (("peer", "peers"), ("funder", "funders")):
        for ent in q.get(key, []):
            for pg in ent.get("pages", []):
                if pg["id"] == page_id:
                    cfg = pp.get(pg["id"], {})
                    pg = dict(pg, parse=cfg.get("parse", pg.get("parse")), year=cfg.get("year", pg.get("year")))
                    pg2 = dict(pg, group=grp, entity_id=ent["id"], entity_name=ent["name"],
                               funder_name=ent.get("funder_name", ent["name"]))
                    rows, rep, b = page_rows(pg2, idx, rec, q)
                    for r in rows:
                        print(r["x_gift_band_raw"] or r["amount"], "|", r["funder_name_raw"], "->",
                              r["recipient_name_raw"], "|", r["fiscal_year"], r["grant_date"], "|",
                              r["purpose_text"][:50], "|", r["x_section"][:30], r["x_notes"][:60])
                    print(rep)
                    print("band counts (non-org entries):", [(x["gift_band_raw"], x["entries_not_identified_as_orgs"])
                                                            for x in b])


def main():
    if "--page" in sys.argv:
        return dry_run(sys.argv[sys.argv.index("--page") + 1])
    q = W43.load_queries()
    rec = load_recipients(q)
    with open(INTERIM / "web_pages.csv", newline="", encoding="utf-8") as f:
        idx = {r["page_id"]: r for r in csv.DictReader(f)}
    rows, cstats = calvary_rows(rec)
    reports, bands = [], []
    pp = q.get("page_parse", {}) or {}
    for grp, key in (("peer", "peers"), ("funder", "funders")):
        for ent in q.get(key, []):
            for pg in ent.get("pages", []):
                cfg = pp.get(pg["id"], {})
                pg = dict(pg, parse=cfg.get("parse", pg.get("parse")), skip_reason=cfg.get("skip"),
                          year=cfg.get("year", pg.get("year")))
                if not pg.get("parse"):
                    reports.append(dict(page_id=pg["id"], group=grp, entity=ent["id"], entries=0, kept=0,
                                        orgs_dropped=0, not_matched=0,
                                        status=pg.get("skip_reason", "no parse spec")))
                    continue
                pg2 = dict(pg, group=grp, entity_id=ent["id"], entity_name=ent["name"],
                           funder_name=ent.get("funder_name", ent["name"]))
                r, rep, b = page_rows(pg2, idx, rec, q)
                rows += r
                reports.append(rep)
                bands += b
    # de-duplicate exact repeats (same funder, recipient, year, source, amount)
    seen, uniq = set(), []
    for r in rows:
        k = (norm_name(r["funder_name_raw"]), r["recipient_ein"] or r["recipient_name_norm"], str(r["fiscal_year"]),
             r["source_id"], str(r["amount"]), str(r["amount_band_min"]), r["purpose_text"][:40])
        if k in seen:
            continue
        seen.add(k)
        uniq.append(r)
    rows = uniq
    W43.write_csv(STAGE, FIELDS, rows)
    W43.write_csv(INTERIM / "web_parse_report.csv",
                  ["page_id", "group", "entity", "entries", "kept", "orgs_dropped", "not_matched", "status"], reports)
    W43.write_csv(INTERIM / "web_peer_donor_band_counts.csv",
                  ["source_id", "page_id", "recipient", "report_year", "gift_band_raw", "band_min", "band_max",
                   "entries_not_identified_as_orgs"], bands)
    ik = inkind_rows(q, idx)
    W43.write_csv(INTERIM / "web_inkind_evidence.csv",
                  ["funder", "crm_gift_total", "finding", "evidence_url", "quote", "classification", "confidence",
                   "source_id", "retrieved_date", "notes"], ik)
    summarize(rows, reports, ik, cstats, q, rec)


def core_key(n: str) -> str:
    k = norm_name(n)
    k = re.sub(r"\b(foundation|fund|charitable|trust|incorporated|group|corporation|company|employee giving program|"
               r"giving program|matching gifts?( program)?|community impact|includes employee gifts|the)\b", " ", k)
    return re.sub(r"\s+", " ", k).strip()


def calvary_funder_keys() -> set[str]:
    keys = set()
    for p, col in [(ROOT / "raw" / "inputs_extracted" / "crm_funders_2023_2026.csv", "last_name"),
                   (ROOT / "raw" / "inputs_extracted" / "funder_mentions.csv", "funder_name_raw"),
                   (INTERIM / "web_calvary_funders.csv", "funder_name_raw")]:
        if p.exists():
            with open(p, newline="", encoding="utf-8") as f:
                for r in csv.DictReader(f):
                    if r.get(col):
                        keys.add(core_key(r[col]))
    keys.discard("")
    return keys


def funder_line(rows, sid, label):
    rr = [r for r in rows if r["source_id"] == sid and r["x_recipient_key"]]
    if not rr:
        return f"- {label}: no Calvary or peer rows."
    amts = sorted(int(r["amount"]) for r in rr if r["amount"] != "")
    peers = sorted({r["x_recipient_key"] for r in rr} - {"calvary"})
    calv = [int(r["amount"]) for r in rr if r["x_recipient_key"] == "calvary" and r["amount"] != ""]
    top = sorted(((int(r["amount"]), r["recipient_name_raw"]) for r in rr if r["amount"] != ""), reverse=True)[:4]
    return (f"- {label}: {len(peers)} core peers plus Calvary, {len(rr)} grants of ${amts[0]:,}-${amts[-1]:,}; "
            f"Calvary ${sum(calv):,}; largest: " + "; ".join(f"{n} ${a:,}" for a, n in top) + ".")


def analysis_notes(rows: list[dict], ik: list[dict], rec: dict) -> tuple[str, str]:
    cal = calvary_funder_keys()
    peer_rows = [r for r in rows if r["recipient_ein"] and r["recipient_ein"] != CALVARY_EIN]
    by = defaultdict(set)
    names = {}
    for r in peer_rows:
        k = core_key(r["funder_name_raw"])
        if len(k) < 3:
            continue
        by[k].add(r["x_recipient_key"])
        names.setdefault(k, r["funder_name_raw"])
    common = sorted(((len(v), names[k], sorted(v)) for k, v in by.items() if len(v) >= 2 and k not in cal),
                    key=lambda x: (-x[0], x[1]))
    shared = sorted(((len(v), names[k]) for k, v in by.items() if len(v) >= 3 and k in cal), key=lambda x: -x[0])
    new = [r for r in rows if str(r["fiscal_year"]) in ("2025", "2026") and r["source_type"] == "web"
           and r["amount"] != "" and r["x_recipient_key"]]
    cal_new = [r for r in new if r["recipient_ein"] == CALVARY_EIN]
    lines = ["Source: interim/stage_fact_grants__web.csv (scripts 43-45). Peer lists are each peer's latest posted "
             "annual report or supporters page (FY2023-FY2025); funder lists are published 2024-2026 grant lists.",
             f"- Funders on lists for 2 or more core peers but not on any Calvary list (CRM, Phase 1 mentions or the "
             f"web pages): {len(common)}. Top: " + "; ".join(f"{n} ({c} peers)" for c, n, _ in common[:20]) + ". "
             "Only 6 peers post donor lists (NSV, House of Ruth DC, MSP, Community of Hope, Coalition for the "
             "Homeless, Heartly House), so overlap counts are low.",
             f"- Funders shared by Calvary and 3 or more peers: " + "; ".join(f"{n} ({c})" for c, n in shared[:12]) + ".",
             f"- 2025-2026 grants with funder-published amounts: {len(new)} rows; to Calvary: " +
             "; ".join(f"{r['funder_name_raw']} ${int(r['amount']):,} ({r['grant_date'] or r['fiscal_year']}, "
                       f"{r['purpose_text'][:40]})" for r in cal_new) + ".",
             funder_line(rows, "web_funder_cafritz_recent", "Cafritz Recent Grants (Summer 2025-Spring 2026)"),
             funder_line(rows, "web_funder_graham_recent", "Philip L. Graham Fund recent grants (2024-2026)"),
             "- The Graham Fund's $200,000 over two years to Calvary (2025-11-13) matches the CRM's last gift of $100,000 "
             "on 2025-11-26 (first installment). For Cafritz, the CRM shows 6 gifts totalling $1,090,000 (last $25,000 on "
             "2026-05-18); the Summer 2025 $100,000 award may be paid in installments (not verified).",
             "- Health Equity Fund (GWCF, from the DC-GHMSI/CareFirst MOU) funded Calvary in the 2022 inaugural round "
             "and again in the October 2024 multi-year round; My Sister's Place is the only other core peer in both rounds.",
             "- A FY22 single audit (Sept 30, 2022) is posted on Candid (docs.candid.org/A133). Its SEFA total is "
             "$4,067,718 (SLFRF via OVSJG $3,583,885). That is $3,000 off the FAC figure of $4,064,718 currently "
             "labelled FY23, so the FAC record may be the FY22 audit. Staged in interim/web_new_audit_*.csv.",
             "- Bank of America Neighborhood Builders, Capital One, Wells Fargo, CareFirst and UWNCA publish no "
             "2024-2026 DC grantee lists that name Calvary or the peers. Meyer, Abell, Clark-Winchcole, Bainum and "
             "WAWF publish no per-grantee lists for 2024-2026."]
    q_lines = ["- Health Equity Fund ($801,000 in the CRM): the web evidence identifies it as the Greater Washington Community "
               "Foundation's Health Equity Fund (cash grants; Calvary in the 2022 and Oct 2024 rounds). Should the CRM "
               "rows be re-attributed to GWCF (EIN 237343119) as funder of record?",
               "- MGAC ($712,730): Calvary and MGAC both describe pro bono project management (the 2013 Good Hope Road "
               "renovation, recent permits work) alongside donations and Hope Gala sponsorship. Can Calvary confirm "
               "how much of the CRM total is valued in-kind services?",
               "- Capital One ($367,340): cash Impact Initiative grants plus pro bono projects and gift matching. Is "
               "matching or pro bono value included in the CRM total?",
               "- FY24 and FY25 audits are not on calvaryservices.org, Candid or the web. The FY22 single audit was "
               "found on Candid. Can Calvary share FY24/FY25 audits and any FY24/FY25 annual report beyond the 'At a "
               "Glance' sheet?"]
    return "\n".join(lines), "\n".join(q_lines)


def summarize(rows, reports, ik, cstats, q, rec):
    by_type = Counter(r["source_type"] for r in rows)
    by_conf = Counter(r["confidence"] for r in rows)
    with_amt = sum(1 for r in rows if r["amount"] != "")
    with_band = sum(1 for r in rows if r["amount"] == "" and (r["amount_band_min"] != "" or r["amount_band_max"] != ""))
    to_cal = [r for r in rows if r["recipient_ein"] == CALVARY_EIN]
    to_peer = [r for r in rows if r["recipient_ein"] and r["recipient_ein"] != CALVARY_EIN]
    whole = [r for r in rows if r["x_whole_list_keep"]]
    fails = [f"{r['page_id']} ({r['status']})" for r in reports if r["status"] not in ("ok",)]
    lines = [f"- staged rows {len(rows)}: by source_type {dict(by_type)}; confidence {dict(by_conf)}",
             f"- amount stated {with_amt}; band only {with_band}; unknown {len(rows) - with_amt - with_band}",
             f"- recipient Calvary {len(to_cal)}; core peers {len(to_peer)} "
             f"({len({r['recipient_ein'] for r in to_peer})} peers); whole-list keyword keeps {len(whole)}",
             f"- Calvary-site rows by type {dict(cstats)}",
             f"- pages parsed {sum(1 for r in reports if r['status'] == 'ok')}/{len(reports)}; "
             f"not parsed or failed: " + "; ".join(fails)[:1500],
             f"- in-kind evidence rows {len(ik)}: " + "; ".join(f"{e['funder']}={e['classification']}" for e in ik)]
    tot = W43.WebFetcher().usage_total()
    lines.append(f"- Tavily usage to date (manifest, scripts 43-44): search {tot['search']}/300, extract "
                 f"{tot['extract']}/200; plus 1 exploratory search during development (same query as "
                 f"cal_audit_fy24; response not saved). HTTP GETs {tot['http']}.")
    notes, qs = analysis_notes(rows, ik, rec)
    existing = (ROOT / "notes_for_analysis.md").read_text(encoding="utf-8")
    if "## Web funder data" not in existing or "--notes" in sys.argv:
        append_md("notes_for_analysis.md", "Web funder data", notes)
        append_md("open_questions.md", "Web funder data (Phase 4)", qs)
        lines.append("- appended notes_for_analysis.md 'Web funder data' and open_questions.md")
    else:
        lines.append("- notes already present (rerun with --notes to append again)")
    log("45_stage_web_grants", "\n".join(lines))
    print("\n".join(lines))
    print(notes)


if __name__ == "__main__":
    main()
