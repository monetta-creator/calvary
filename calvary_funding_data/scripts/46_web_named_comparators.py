"""Phase 4 web pull + staging: funders of the named comparators (config/named_comparators.csv, rule NC1).

The named comparators (Downtown Women's Center, Los Angeles, EIN 311597223) are funded mostly from outside the
DMV funder universe, so their own supporter lists / annual reports and foundation grant announcements that
name them are pulled here. Everything is configured under `named_comparators:` in config/web_queries.yaml.

Steps (run all, or pick with --only)
  search  Tavily searches (entity.searches) -> raw/tavily/ via the script-43 WebFetcher (cached in
          interim/web_fetch_manifest.csv; reruns reuse the saved response). Hits -> interim/web_named_search_hits.csv
  pages   entity.pages fetched by method (http GET -> raw/web/, tavily extract -> raw/tavily/, auto = GET then
          extract), via script 44 fetch_page(). Text -> interim/web_text/{page_id}.txt. One web_nc_ source per page.
          Index -> interim/web_named_pages.csv
  stage   pages[].parse specs parsed with the script-45 parsers and row builder (group "peer": entries are
          funders, recipient = the comparator) -> interim/stage_fact_grants__web_named.csv (fact_grants columns
          as interim/stage_fact_grants__web.csv). Entries that do not read as organizations are only counted
          per gift band -> interim/web_named_donor_band_counts.csv (no names).

Budget: at most 30 Tavily searches and 15 Tavily extracts for this script (labels prefixed nc_, counted from the
fetch manifest across runs); a call over the cap is skipped.

Rules (as script 45): organizations only, never individuals' names; amount only when stated, else gift band,
else amount_kind unknown; source_type annual_report for annual/impact reports, web for other pages and
announcements; funder_ein left blank (resolved in Phase 5).

Usage:
  [ -f ~/.config/calvary/keys.env ] && set -a && . ~/.config/calvary/keys.env && set +a
  .venv/bin/python scripts/46_web_named_comparators.py [--only search,pages,stage] [--refresh]
"""
from __future__ import annotations

import argparse
import importlib
import re
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import INTERIM, ROOT, log, norm_ein, register_source, today  # noqa: E402

W43 = importlib.import_module("43_web_calvary")
W44 = importlib.import_module("44_web_peers_funders")
W45 = importlib.import_module("45_stage_web_grants")

RETRIEVED = today()
CAP = {"search": 30, "extract": 15}
PREFIX = "nc_"
HITS = INTERIM / "web_named_search_hits.csv"
PAGES = INTERIM / "web_named_pages.csv"
STAGE = INTERIM / "stage_fact_grants__web_named.csv"
BANDS = INTERIM / "web_named_donor_band_counts.csv"
TEXT_DIR = INTERIM / "web_text"


class CappedFetcher(W43.WebFetcher):
    """WebFetcher with a per-script cap on Tavily calls (labels starting with nc_ / page_nc_)."""

    def used(self, kind: str) -> int:
        return sum(int(r.get("api_calls") or 0) for r in self.rows.values()
                   if r["kind"] == kind and re.match(rf"(page_)?{PREFIX}", r.get("label", "")))

    def _budget_ok(self, kind, n=1):
        if kind in CAP and self.used(kind) + n > CAP[kind]:
            print(f"  ! script-46 Tavily {kind} cap reached ({self.used(kind)}/{CAP[kind]}); skipping")
            return False
        return super()._budget_ok(kind, n)


def entities(q: dict) -> list[dict]:
    return q.get("named_comparators") or []


# ---------------------------------------------------------------- extra parser + people guard
def p_pdf_words(text: str, spec: dict) -> list[dict]:
    """Multi-column PDF donor lists from word coordinates (pdfplumber), for layouts where pdftotext -layout joins
    neighbouring columns with a single space. Columns = x0 values shared by >= col_min_words words; lines =
    words within 1.5pt of the same top; a line within wrap_gap pt below the previous line of the same column
    continues that entry; lines in a band_font (or matching the script-45 BAND regex) are gift bands. Columns
    are read left to right, pages in order, and the band carries over."""
    import pdfplumber
    out, band, section = [], spec.get("band", ""), spec.get("section", "")
    skip = re.compile(spec.get("skip", r"(?!x)x"), re.I)
    band_font = re.compile(spec.get("band_font", r"(?!x)x"))
    with pdfplumber.open(spec["_path"]) as pdf:
        for pno in spec["pages"]:
            ws = [w for w in pdf.pages[pno - 1].extract_words(extra_attrs=["fontname", "size"])
                  if w["size"] <= spec.get("max_size", 12)]
            starts = Counter(round(w["x0"]) for w in ws)
            cols = []
            for x in sorted(x for x, n in starts.items() if n >= spec.get("col_min_words", 20)):
                if not cols or x - cols[-1] > 20:
                    cols.append(x)

            def col_of(x):
                k = 0
                for i, s in enumerate(cols):
                    if x >= s - 3:
                        k = i
                return k
            by_col = {}
            for w in ws:
                by_col.setdefault(col_of(w["x0"]), []).append(w)
            for c in sorted(by_col):
                lines = []
                for w in sorted(by_col[c], key=lambda w: (w["top"], w["x0"])):
                    if lines and abs(w["top"] - lines[-1][0]) <= 1.5:
                        lines[-1][1].append(w)
                    else:
                        lines.append([w["top"], [w]])
                prev = None
                for top, wl in lines:
                    wl.sort(key=lambda w: w["x0"])
                    t = re.sub(r"\s+", " ", " ".join(w["text"] for w in wl)).strip()
                    if not t or skip.search(t):
                        prev = None
                        continue
                    if band_font.search(wl[0]["fontname"]) or W45.BAND.match(t):
                        band, prev = t, None
                        continue
                    if prev is not None and 0 < top - prev["_top"] <= spec.get("wrap_gap", 9.6):
                        prev["name"] += " " + t
                        prev["parts"].append(t)
                        prev["_top"] = top
                        continue
                    prev = dict(name=t, band=band, section=section, parts=[t], _top=top)
                    out.append(prev)
    return out


W45.PARSERS["pdf_words"] = p_pdf_words
_not_a_name = W45.not_a_name


def not_a_name_initials(n: str, strict: bool = True) -> bool:
    """Script-45 not_a_name(), except that a middle initial ("The Ralph M. Parsons Foundation", "Conrad N. Hilton
    Foundation") is not read as a sentence break. Patched into script 45's module for this process only."""
    return _not_a_name(re.sub(r"\b([A-Z])\.(?=\s+[A-Z])", r"\1", n), strict)


W45.not_a_name = not_a_name_initials

# Script 45's page_rows() reads "<A> and <B Foundation>" as "<person> and <org>" and keeps only <B Foundation>,
# which truncates couples' foundations and firm names ("The John & Marilyn Wells Family Foundation",
# "Munger, Tolles & Olson LLP"). Before page_rows(), the connector of such names is joined with zero-width joiners
# (so the split regex does not match); restore_connectors() puts the spaces back after the people guard.
ZWJ = "‍"
ORG_TAIL = re.compile(r"\b(Foundation|Fund|Trust|Charities|LLP|L\.?L\.?C\.?|L\.?P\.?|Inc\.?|Co\.?|Company|Partners|"
                      r"Associates)(,? (Inc\.?|L\.?P\.?|LLC)| of [A-Z]{2})?\.?$")


def protect_connectors(name: str) -> str:
    m = re.match(r"^(.+?)\s+(and|&)\s+(.+)$", name)
    if m and ORG_TAIL.search(m.group(3)) and not re.match(r"(?i)the\s", m.group(3)) and \
            not re.search(r"\s(and|&)\s", m.group(3)) and len(m.group(1).replace(",", " ").split()) <= 4:
        return f"{m.group(1)}{ZWJ}{m.group(2)}{ZWJ}{m.group(3)}"
    return name


def restore_connectors(name: str) -> str:
    return re.sub(f"{ZWJ}(and|&){ZWJ}", r" \1 ", name)


def _wrap(parser, single_part: bool):
    def run(text, spec):
        out = parser(text, spec)
        for e in out:
            if e.get("name"):
                e["name"] = protect_connectors(re.sub(r"\s+", " ", e["name"]).strip())
                if single_part or len(e.get("parts", [])) <= 1:
                    e["parts"] = [e["name"]]
        return out
    return run


# coordinate-parsed wraps are one donor name: keep a single part so strip_person_prefix() does not drop the
# first line ("Otis and Bettina" + "Chandler Foundation")
W45.PARSERS["pdf_words"] = _wrap(p_pdf_words, single_part=True)
W45.PARSERS["lines"] = _wrap(W45.p_lines, single_part=False)

SEP = re.compile(r"(\s+(?:and|&)\s+|\s+[–—-]\s+|,\s+(?!(?:Inc|LLC|LLP|L\.?P|Ltd|Co|APLC|PLLC|PC|N\.?A)\b))")
PERSON_RE = re.compile(r"^(?:Dr\.? |Mr\.? |Ms\.? |Mrs\.? )?[A-Z][a-z'’-]+(?: [A-Z]\.?)?(?: [A-Z][a-z'’-]+){1,2}$")
NOT_PERSON = re.compile(r"\b(Region|District|County|California|Angeles|Southern|Northern|Greater|Valley|City|Housing|"
                        r"Solutions|Studios|Pictures|Films|Productions|Group|Bank|Partners|Holdings|Brands|Media|"
                        r"Health|Care|Capital|Realty|Properties|Hospital|Center|Women|Network|Alliance|Development|"
                        r"Economic|Services|Program|Programs|Shelter|Food|Emergency|Office|Department|Board|Commission|"
                        r"Council|Foundation|Fund|Association|Institute|Club|Management|Wealth|Asset|Society|Church|"
                        r"University|College|School|Systems|Technology|Consulting|Industries|International|"
                        r"Enterprises|Ventures|Communities|Insurance|Labor|Federation|Workforce)\b")
# organization words a kept fragment must carry once a personal name was removed next to it
STRONG_ORG = re.compile(r"\b(Foundation|Fund|Funds|Trust|Charities|Charitable|Inc|LLC|LLP|L\.?P|Ltd|Company|Co|Corp|"
                        r"Corporation|Bank|Group|District|County|Department|Office|Program|Association|Society|Church|"
                        r"Temple|Center|University|College|School|Institute|Club|Partners|Alliance|Network|Council|"
                        r"Board|Commission|Authority|Agency|Services|Health|Hospital|Studios|Pictures|Films|"
                        r"Productions|Entertainment|Capital|Management|Realty|Properties|Communities|Builders|Brokers|"
                        r"Consulting|Solutions|Federation|America)\b")


def is_person(p: str) -> bool:
    return bool(PERSON_RE.match(p)) and not NOT_PERSON.search(p) and not W43.is_org_name(p)


def strip_people(name: str) -> str:
    """People-data guard for joint credits ("Bank of America and <First Last>", "<First Last> – <firm>",
    "<office>, <First M. Last>"): drop the parts that read as a personal name and keep the organization parts
    (which must carry an organization word) with their original separators. Returns '' when none remains."""
    toks = SEP.split(name)
    parts, seps = toks[0::2], toks[1::2]
    if len(parts) <= 1 or not any(is_person(p.strip()) for p in parts):
        return name
    keep = [i for i, p in enumerate(parts) if not is_person(p.strip()) and W43.is_org_name(p.strip())
            and STRONG_ORG.search(p)]
    out = ""
    for i in keep:
        out += (seps[i - 1] if out else "") + parts[i]
    return out.strip(" ,&-–—")


def band_from_label(raw: str) -> tuple:
    """'$1M +' / '$1M+' -> (1000000, '')."""
    m = re.match(r"^\$\s?(\d+(?:\.\d+)?)\s*M\s*\+?$", (raw or "").strip(), re.I)
    return (int(float(m.group(1)) * 1_000_000), "") if m else ("", "")


def all_pages(q: dict) -> list[dict]:
    out = []
    for ent in entities(q):
        for pg in ent.get("pages", []):
            assert pg["id"].startswith(PREFIX), f"page id must start with {PREFIX}: {pg['id']}"
            out.append(dict(pg, group="peer", entity_id=ent["id"], entity_name=ent["name"],
                            entity_ein=norm_ein(ent["ein"])))
    return out


# ---------------------------------------------------------------- steps
def step_search(wf, q: dict) -> list[str]:
    hits = []
    for ent in entities(q):
        for s in ent.get("searches", []):
            assert s["id"].startswith(PREFIX), f"search id must start with {PREFIX}: {s['id']}"
            resp = wf.search(s["id"], s["query"], **s.get("params", {}))
            hits += W44.flatten(resp, "named_comparator", ent["id"], s["id"])
    for h in hits:
        h["query"] = next(s["query"] for e in entities(q) for s in e.get("searches", []) if s["id"] == h["qid"])
    W43.write_csv(HITS, ["group", "entity_id", "qid", "query", "rank", "url", "title", "score", "snippet"], hits)
    register_source("api_tavily_search", "Tavily Search API (search results and snippets)",
                    "https://api.tavily.com/search", "Tavily", "Tavily API terms of service",
                    "Queries in config/web_queries.yaml; raw responses in raw/tavily/search_*.json",
                    retrieved_date=RETRIEVED)
    n_q = sum(len(e.get("searches", [])) for e in entities(q))
    return [f"- searches configured {n_q}; hits {len(hits)} ({len({h['url'] for h in hits})} distinct URLs) "
            f"-> {HITS.relative_to(ROOT)}"]


def step_pages(wf, q: dict) -> list[str]:
    TEXT_DIR.mkdir(parents=True, exist_ok=True)
    index = []
    for pg in all_pages(q):
        r = W44.fetch_page(wf, pg)
        sid = pg.get("source_id") or f"web_{pg['id']}"
        if r["raw_path"]:
            txt = W44.page_text({"raw_path": r["raw_path"]})
            (TEXT_DIR / f"{pg['id']}.txt").write_text(txt, encoding="utf-8")
            register_source(sid, pg.get("title") or f"{pg['entity_name']}: {pg.get('kind', 'page')} "
                            f"{pg.get('year', '')}".strip(), pg["url"], pg.get("publisher") or pg["entity_name"],
                            "Public PDF" if r["raw_path"].endswith(".pdf") else "Public web page",
                            f"{pg.get('kind', '')}; year {pg.get('year', '')}; fetched via {r['method_used']}; "
                            f"raw: {r['raw_path']}", retrieved_date=RETRIEVED)
        index.append(dict(page_id=pg["id"], source_id=sid, entity_id=pg["entity_id"], entity_ein=pg["entity_ein"],
                          kind=pg.get("kind", ""), year=pg.get("year", ""), url=pg["url"],
                          method_used=r["method_used"], raw_path=r["raw_path"], status=r["status"],
                          text_chars=r["text_chars"], retrieved_date=RETRIEVED))
    W43.write_csv(PAGES, list(index[0].keys()) if index else ["page_id"], index)
    bad = [f"{i['page_id']} ({i['status']})" for i in index if not i["raw_path"] or i["text_chars"] < 200]
    return [f"- pages listed {len(index)}, fetched {sum(1 for i in index if i['raw_path'])} -> {PAGES.relative_to(ROOT)}",
            "- failed/empty: " + ("; ".join(bad) if bad else "none")]


def step_stage(q: dict) -> list[str]:
    idx = {}
    if PAGES.exists():
        idx = {r["page_id"]: r for r in pd.read_csv(PAGES, dtype=str, keep_default_na=False).to_dict("records")}
    rec = {e["id"]: dict(ein=norm_ein(e["ein"]), name=e["name"], city=e.get("city", ""), state=e.get("state", ""),
                         alias=re.compile(e["alias"], re.I)) for e in entities(q)}
    rows, reports, bands = [], [], []
    n_people_stripped = n_people_dropped = 0
    for pg in all_pages(q):
        if not pg.get("parse"):
            continue
        meta = idx.get(pg["id"]) or {}
        for spec in pg["parse"]:
            if spec["type"] == "pdf_words" and meta.get("raw_path"):
                spec["_path"] = str(ROOT / meta["raw_path"])
        r, rep, b = W45.page_rows(pg, idx, rec, q)
        kept = []
        for x in r:
            x["match_method"] = "page_owner"
            x["x_recipient_key"] = pg["entity_id"]
            name = strip_people(x["funder_name_raw"])
            # script 45 kept only the tail of "<person> and <tail>": keep it only when it reads as an organization
            if "leading personal name removed" in x["x_notes"] and not STRONG_ORG.search(name):
                name = ""
            if not name:
                n_people_dropped += 1
                continue
            if name != x["funder_name_raw"]:
                n_people_stripped += 1
                x["x_notes"] = "; ".join(v for v in (x["x_notes"], "personal name removed from a joint credit") if v)
            x["funder_name_raw"] = restore_connectors(name)
            band = x["x_gift_band_raw"]
            if band in (pg.get("tier_bands") or {}):   # sponsor tiers priced on the same page
                lo, hi = pg["tier_bands"][band]
                x["amount_band_min"], x["amount_band_max"] = lo, hi if hi is not None else ""
                x["x_notes"] = "; ".join(v for v in (x["x_notes"], pg.get("tier_note", "")) if v)
            elif band and x["amount_band_min"] in ("", None) and x["amount_band_max"] in ("", None):
                x["amount_band_min"], x["amount_band_max"] = band_from_label(band)
            if pg.get("year_basis"):
                x["year_basis"] = pg["year_basis"]
            kept.append(x)
        rows += kept
        rep["kept"] = len(kept)
        reports.append(rep)
        bands += b
    df = pd.DataFrame(rows, columns=W45.FIELDS)
    n0 = len(df)
    df = df.drop_duplicates()
    df.to_csv(STAGE, index=False)
    pd.DataFrame(bands, columns=["source_id", "page_id", "recipient", "report_year", "gift_band_raw", "band_min",
                                 "band_max", "entries_not_identified_as_orgs"]).to_csv(BANDS, index=False)
    lines = [f"- staged {len(df):,} rows -> {STAGE.relative_to(ROOT)} (exact duplicates dropped {n0 - len(df)}); "
             f"recipients {df.recipient_ein.value_counts().to_dict()}",
             f"- by source_type {df.source_type.value_counts().to_dict()}; amount_kind "
             f"{df.amount_kind.value_counts().to_dict()}; with amount {int((df.amount.astype(str) != '').sum())}, "
             f"with band {int((df.amount_band_min.astype(str) + df.amount_band_max.astype(str) != '').sum())}",
             f"- by fiscal_year {df.fiscal_year.value_counts().sort_index().to_dict()}",
             f"- non-organization entries counted per band only: {sum(b['entries_not_identified_as_orgs'] for b in bands)} "
             f"-> {BANDS.relative_to(ROOT)}; joint credits with a personal name: {n_people_stripped} trimmed to the "
             f"organization, {n_people_dropped} dropped",
             "- per page (entries, kept, dropped as non-org, status): " + "; ".join(
                 f"{r['page_id']} {r['entries']}/{r['kept']}/{r['orgs_dropped']}/{r['status']}" for r in reports)]
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="search,pages,stage")
    ap.add_argument("--refresh", action="store_true", help="call Tavily / GET again instead of reusing raw")
    a = ap.parse_args()
    todo = a.only.split(",")
    q = W43.load_queries()
    wf = CappedFetcher(refresh=a.refresh)
    lines = []
    if "search" in todo:
        lines += step_search(wf, q)
    if "pages" in todo:
        lines += step_pages(wf, q)
    if "stage" in todo:
        lines += step_stage(q)
    lines.append(f"- {wf.summary()}; script-46 totals: search {wf.used('search')}/{CAP['search']}, "
                 f"extract {wf.used('extract')}/{CAP['extract']}")
    log(f"46_web_named_comparators ({a.only})", "\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
