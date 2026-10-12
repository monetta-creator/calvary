"""Phase 4, area dc_hud: DC and HUD CoC award records -> interim/stage_fact_gov_awards__dc.csv

Sections (all read raw files; PASS also queries DC GIS and saves every response to raw/dc_gov/):
  ovsjg_layer : DC GIS OVSJG Grant Recipients layer 35, every row FY2016-FY2025. Field labels are
                swapped in the layer: AGENCY holds the grantee, ORGANIZATIONNAME the project title.
  ovsjg_pdf   : OVSJG funding-recipient PDFs FY2024-FY2026. FY2024/FY2025 rows that match a layer row
                (FY + amount + grantee name) enrich it (funding source, period, page) instead of
                adding a duplicate; unmatched PDF rows and all FY2026 rows are added.
  dhs_oversight: provider-level DHS grant/contract tables in the DC Council performance-oversight
                pre-hearing responses (2024, 2025, 2026 cycles); TCP is the intermediary where the
                table says so.
  pass        : PASS purchase orders (deduped for the AA0 sub-office fan-out) and payments
                (aggregated per supplier x FY x agency x PO) for suppliers that match universe EINs.
  hud_coc     : HUD CoC DC-500 project-level awards: AwardComp 2019-2024, FY2025 award rounds;
                GIW FY2024/FY2026 add grant numbers and FY2025 applicants. TCP is prime and the
                project sponsor named in the project title is the subrecipient.

Name matching: norm_name exact, then rapidfuzz token_set_ratio >= 92, against universes dc_sector,
dmv_sector, core_peers (+ calvary); TCP (EIN 521681401) is a manual known alias.

Usage: .venv/bin/python scripts/36_parse_dc_awards.py [--refresh-pass]
  --refresh-pass  re-query PASS even if raw PASS pulls from this script already exist
"""
from __future__ import annotations

import argparse
import csv
import glob
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

import pandas as pd
import pdfplumber
from rapidfuzz import fuzz, process

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import (CLEAN, INTERIM, RAW, RateLimiter, latest_raw, log, norm_name,  # noqa: E402
                        register_source, rel, save_raw, session)

OUT = INTERIM / "stage_fact_gov_awards__dc.csv"
TCP_EIN = "521681401"
TCP_NAME = "The Community Partnership for the Prevention of Homelessness"
CALVARY_EIN = "521307706"
OVSJG = "DC Office of Victim Services and Justice Grants (OVSJG)"
DHS = "DC Department of Human Services (DHS)"
LOGS: list[str] = []
CHECKS: list[str] = []


# ---------------------------------------------------------------- helpers
def money(s) -> int | None:
    """'$ 4 75,000' / '$543,055.72' / '296,038.45' -> int USD (half-up). None for blanks/N/A/-."""
    if s is None:
        return None
    t = str(s).replace(" ", "").replace("$", "")
    if t in ("", "-", "N/A", "n/a", "NA"):
        return None
    t = re.sub(r"[^\d.,-]", "", t)
    # '232.765.77' (typo in source) -> treat all but the last dot as thousands separators
    if t.count(".") > 1:
        head, tail = t.rsplit(".", 1)
        t = head.replace(".", "") + "." + tail
    t = t.replace(",", "")
    if not re.fullmatch(r"-?\d+(\.\d+)?", t):
        return None
    return int(Decimal(t).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def is_money_cell(s: str) -> bool:
    s = (s or "").strip()
    return bool(s) and ("$" in s or bool(re.fullmatch(r"[\d,]+\.\d\d", s)))


def clean_ws(s) -> str:
    return re.sub(r"\s+", " ", str(s or "")).strip()


def file_date(p: Path) -> str:
    m = re.match(r"(\d{4})(\d{2})(\d{2})T", p.name)
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else ""


def raw1(source: str, pattern: str) -> Path:
    hits = sorted(glob.glob(str(RAW / source / f"*{pattern}")))
    if not hits:
        raise FileNotFoundError(f"raw/{source}/*{pattern}")
    return Path(hits[-1])


def row_id(*parts) -> str:
    return hashlib.sha1("|".join(str(p) for p in parts).encode()).hexdigest()[:16]


# ---------------------------------------------------------------- name matching
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


class Matcher:
    UNIVERSES = ("dc_sector", "dmv_sector", "core_peers", "calvary")

    def __init__(self):
        d = pd.read_csv(CLEAN / "dim_universe_membership.csv", dtype=str)
        d = d[d.universe.isin(self.UNIVERSES)].drop_duplicates("ein").copy()
        d["norm"] = d.org_name_bmf.map(norm_name)
        d["rev"] = pd.to_numeric(d.bmf_revenue_amt, errors="coerce").fillna(0)
        self.df = d.reset_index(drop=True)
        self.by_norm: dict[str, list[int]] = defaultdict(list)
        for i, n in enumerate(self.df.norm):
            self.by_norm[n].append(i)
        self.choices = list(self.df.norm)
        self.cache: dict[str, tuple] = {}

    @staticmethod
    def variants(raw: str) -> list[str]:
        s = clean_ws(raw)
        s = re.sub(r"\([^)]*(\)|$)", " ", s)          # parentheticals, also unclosed ones
        s = clean_ws(s)
        out = [s]
        for sep in [r"\bd\.?b\.?a\.?\b", r"\bt/a\b", r"/"]:
            parts = [clean_ws(x) for x in re.split(sep, s, flags=re.I) if clean_ws(x)]
            if len(parts) > 1:
                out += parts
        out.append(re.sub(r",?\s*the$", "", s, flags=re.I))   # 'Metro DC Community Center Inc., The'
        seen, res = set(), []
        for v in out:
            if v and v not in seen:
                seen.add(v)
                res.append(v)
        return res

    def _best(self, idxs: list[int], q: str) -> int:
        return sorted(idxs, key=lambda i: (self.df.state[i] != "DC", -fuzz.ratio(q, self.df.norm[i]),
                                           -self.df.rev[i]))[0]

    def match(self, raw: str) -> tuple[str, str, str, int]:
        """-> (ein, bmf_name, method, score). Blank ein when unmatched."""
        if raw in self.cache:
            return self.cache[raw]
        res = ("", "", "unmatched", 0)
        n0 = norm_name(raw)
        alias = next((a for v in [n0] + [norm_name(x) for x in self.variants(raw)] for rx, a in MANUAL_ALIASES
                      if re.search(rx, v)), None)
        if re.search(r"community partnership( for the prevention of homelessness)?|^tcp$", n0):
            res = (TCP_EIN, "COMMUNITY PARTNERSHIP FOR THE PREVENTION OF HOMELESSNESS", "manual_known_ein", 100)
        elif alias:
            res = (alias[0], alias[1], "manual_alias", 100)
        else:
            vs = [norm_name(v) for v in self.variants(raw)]
            full_q = vs[0] if vs else ""
            for q in vs:
                if q in self.by_norm:
                    i = self._best(self.by_norm[q], q)
                    res = (self.df.ein[i], self.df.org_name_bmf[i], "exact_norm_name", 100)
                    break
            else:
                best = None
                for q in vs:
                    qt = set(q.split())
                    if len(qt) < 2:
                        continue
                    hits = process.extract(q, self.choices, scorer=fuzz.token_set_ratio, score_cutoff=92, limit=15)
                    ok = [(sc, i) for _, sc, i in hits if fuzzy_ok(q, self.df.norm[i],
                                                                     trunc=len(clean_ws(raw)) >= 28 and q == full_q,
                                                                     raw=raw)]
                    if ok:
                        top = max(sc for sc, _ in ok)
                        i = self._best([i for sc, i in ok if sc == top], q)
                        cand = (self.df.ein[i], self.df.org_name_bmf[i], "fuzzy_token_set", int(round(top)))
                        if best is None or cand[3] > best[3]:
                            best = cand
                if best:
                    res = best
        self.cache[raw] = res
        return res


M: Matcher | None = None


def base_row(**kw) -> dict:
    r = {k: "" for k in COLS}
    r.update(kw)
    return r


def attach_match(r: dict, name: str) -> dict:
    ein, bmf, method, score = M.match(name)
    r["recipient_ein"] = ein
    r["x_match_method"] = method
    r["x_match_score"] = score if ein else ""
    r["x_matched_bmf_name"] = bmf
    r["x_recipient_name_norm"] = norm_name(name)
    return r


COLS = ["award_row_id", "recipient_ein", "recipient_uei", "recipient_name_raw", "awarding_agency", "funding_agency",
        "program_name", "assistance_listing", "award_id", "award_type", "flow_type", "pass_through_entity",
        "pass_through_ein", "period_start", "period_end", "fiscal_year", "fiscal_year_basis", "amount", "amount_type",
        "source_type", "source_id", "source_page", "conflict_flag", "retrieved_date", "confidence", "basis",
        "x_match_method", "x_match_score", "x_matched_bmf_name", "x_recipient_name_norm", "x_section",
        "x_funding_source_raw", "x_funding_mix", "x_purpose_text", "x_agency_code", "x_document",
        "x_corroborating_source_id", "x_corroborating_page", "x_issue_date", "x_capacity", "x_clients_served",
        "x_ytd", "x_component", "x_project_status", "x_sponsor_name", "x_prime_recipient_name",
        "x_pass_through_inferred", "x_po_status", "x_po_version", "x_commodity", "x_n_payments",
        "x_first_payment_date", "x_last_payment_date", "x_pass_incomplete_fy", "x_notes"]


# ---------------------------------------------------------------- OVSJG funding source -> federal listing
FED_SOURCES = [  # (regex, ALN, federal funding agency, label)
    (r"\bVOCA\b|Victim Assistance Formula", "16.575", "U.S. DOJ Office for Victims of Crime", "VOCA"),
    (r"\bVAWA\b|STOP VAWA", "16.588", "U.S. DOJ Office on Violence Against Women", "STOP VAWA"),
    (r"\bSASP\b|Sexual Assault Services Formula", "16.017", "U.S. DOJ Office on Violence Against Women", "SASP"),
    (r"\bBYRNE\b|Byrne Memorial", "16.738", "U.S. DOJ Bureau of Justice Assistance", "Byrne JAG"),
    (r"TITLE II\b|Title II Formula", "16.540", "U.S. DOJ Office of Juvenile Justice and Delinquency Prevention",
     "JJDP Title II"),
    (r"TITLE V\b|Delinquency Prevention Grants", "16.548",
     "U.S. DOJ Office of Juvenile Justice and Delinquency Prevention", "Title V Delinquency Prevention"),
    (r"\bRSAT\b|Residential Substance Abuse Treatment", "16.593", "U.S. DOJ Bureau of Justice Assistance", "RSAT"),
    (r"Coverdell", "16.742", "U.S. DOJ National Institute of Justice", "Coverdell"),
    (r"\bARPA\b", "21.027", "U.S. Department of the Treasury", "ARPA SLFRF"),
]
LOCAL_RX = re.compile(r"local|\bVAF\b|Crime Victims Assistance Fund|Access to Justice|ONSE|Capacity Building", re.I)


def fix_split_caps(s: str) -> str:
    """'L ocal' / 'P rogram' / 'O NSE' artifacts from the FY2026 PDF text layer."""
    return re.sub(r"\b([A-Z]) (?=[A-Za-z])", r"\1", clean_ws(s))


def classify_funding(src: str):
    """-> (assistance_listing ';'-joined, funding_agency, mix local/federal/local+federal/unknown)."""
    src = fix_split_caps(src)
    alns, agencies = [], []
    for rx, aln, ag, _ in FED_SOURCES:
        if re.search(rx, src, re.I) and aln not in alns:
            alns.append(aln)
            agencies.append(ag)
    local = bool(LOCAL_RX.search(src))
    mix = ("local+federal" if alns and local else "federal" if alns else "local" if local else "unknown")
    return ";".join(alns), "; ".join(dict.fromkeys(agencies)), mix


# ---------------------------------------------------------------- 1. OVSJG layer 35
def ovsjg_layer() -> list[dict]:
    paths = sorted(glob.glob(str(RAW / "dc_gov" / "*_dcgis_ovsjg_grant_recipients_all_p*.json")))
    # keep only the latest run's pages
    stamp = max(Path(p).name.split("_")[0] for p in paths)
    paths = [Path(p) for p in paths if Path(p).name.startswith(stamp)]
    feats = []
    for p in paths:
        feats += [(p, f["attributes"]) for f in json.loads(p.read_text())["features"]]
    dup = Counter((clean_ws(a["AGENCY"]), clean_ws(a["ORGANIZATIONNAME"]), a["FY"], a["AWARDAMOUNT"],
                   clean_ws(a["ABSTRACT"])) for _, a in feats)
    rows = []
    for p, a in feats:
        grantee = clean_ws(a["AGENCY"])            # swapped label: AGENCY = grantee
        title = clean_ws(a["ORGANIZATIONNAME"])    # swapped label: ORGANIZATIONNAME = project title
        k = (grantee, title, a["FY"], a["AWARDAMOUNT"], clean_ws(a["ABSTRACT"]))
        r = base_row(
            recipient_name_raw=grantee, awarding_agency=OVSJG, funding_agency="",
            program_name=title, award_id=f"OVSJG-L35-{a['OBJECTID']}", award_type="grant",
            flow_type="dc_local_grant", fiscal_year=a["FY"], fiscal_year_basis="dc_fy",
            amount=money(a["AWARDAMOUNT"]), amount_type="award_amount", source_type="dc_ovsjg",
            source_id="api_dcgis_ovsjg_grants", source_page=f"layer35 OBJECTID {a['OBJECTID']}",
            conflict_flag=1 if dup[k] > 1 else 0, retrieved_date=file_date(p), confidence="high",
            basis="documented", x_section="ovsjg_layer", x_purpose_text=clean_ws(a["ABSTRACT"])[:500],
            x_agency_code="FO0", x_document=rel(p), x_funding_mix="unknown",
            x_notes=(f"{dup[k]} identical layer rows (grantee, title, FY, amount, abstract); possible duplicate entry"
                     if dup[k] > 1 else ""))
        rows.append(attach_match(r, grantee))
    LOGS.append(f"- OVSJG layer 35: {len(rows)} rows FY{min(r['fiscal_year'] for r in rows)}-"
                f"FY{max(r['fiscal_year'] for r in rows)}; AGENCY used as grantee, ORGANIZATIONNAME as project title "
                f"(labels swapped); {sum(1 for r in rows if r['conflict_flag'])} rows flagged as identical repeats")
    return rows


# ---------------------------------------------------------------- 2. OVSJG recipient PDFs
PDF_COLS = {  # FY -> field -> column index in the extracted table
    2024: dict(org=0, title=1, abstract=2, amount=3, source=4, period=5, issue=6),
    2025: dict(org=0, title=1, period=2, amount=3, source=4, dept=6, abstract=7),
    2026: dict(dept=0, org=1, title=2, period=3, amount=4, source=5, abstract=6, issue=7),
}
HEADER_RX = re.compile(r"^(Organization|External Organization|Department|Grant:|Project|Awarded)", re.I)


def parse_period(s: str):
    s = clean_ws(s)
    m = re.findall(r"(\d{1,2})/(\d{1,2})/(\d{2,4})", s)
    out = []
    for mo, dy, yr in m[:2]:
        yr = int(yr)
        yr = yr + 2000 if yr < 100 else yr
        out.append(f"{yr:04d}-{int(mo):02d}-{int(dy):02d}")
    return (out + ["", ""])[:2]


def ovsjg_pdf_rows() -> list[dict]:
    rows = []
    for fy in (2024, 2025, 2026):
        p = raw1("dc_gov", f"ovsjg_funding_recipients_FY{fy}.pdf")
        cols = PDF_COLS[fy]
        recs = []
        with pdfplumber.open(p) as pdf:
            texts = [pg.extract_text() or "" for pg in pdf.pages]
            for pi, pg in enumerate(pdf.pages, start=1):
                for tb in pg.extract_tables():
                    for cells in tb:
                        cells = [clean_ws(c) for c in cells]
                        amt = money(cells[cols["amount"]]) if is_money_cell(cells[cols["amount"]]) else None
                        if amt is None and any(HEADER_RX.match(c) for c in cells if c):
                            continue
                        if amt is None and not cells[cols["period"]] and not cells[cols["amount"]] and recs:
                            # page-break / overflow fragment: attach each non-empty cell to the nearest record
                            # whose same cell is empty (previous first, else keep for the next record)
                            last = recs[-1]
                            for j, c in enumerate(cells):
                                if not c:
                                    continue
                                if not last["cells"][j]:
                                    last["cells"][j] = c
                                    last["frag"].add(j)
                                elif j in last["frag"]:        # consecutive fragments of the same cell
                                    last["cells"][j] += " " + c
                            continue
                        if amt is None and cells[cols["org"]]:
                            # FY2024 p2 row with amount missing from the table layer: read it from the text line
                            org = cells[cols["org"]]
                            m = re.search(re.escape(org[:25]) + r".*?\$\s*([\d ,]+)\s*([A-Z][A-Z ,;:]*)", texts[pi - 1])
                            if m:
                                amt = money(m.group(1))
                                if not cells[cols["source"]]:
                                    cells[cols["source"]] = m.group(2).strip()
                            LOGS.append(f"- OVSJG FY{fy} PDF p{pi}: '{org[:40]}' amount from text layer: {amt}")
                        if amt is None:
                            continue
                        recs.append({"fy": fy, "page": pi, "cells": cells, "amount": amt, "path": p, "frag": set()})
        # orphan org fragments (record with empty org whose name came on following fragment rows) handled above
        n_before = len(rows)
        for rc in recs:
            c = rc["cells"]
            get = lambda k: fix_split_caps(c[cols[k]]) if k in cols else ""
            ps, pe = parse_period(get("period"))
            src = get("source")
            aln, fed_ag, mix = classify_funding(src)
            iss = parse_period(get("issue"))[0] if "issue" in cols else ""
            r = base_row(
                recipient_name_raw=clean_ws(c[cols["org"]]), awarding_agency=OVSJG,
                funding_agency=fed_ag if mix == "federal" else ("DC local funds; " + fed_ag if aln else "DC local funds"
                                                                if mix == "local" else ""),
                program_name=get("title"), assistance_listing=aln, award_type="grant",
                flow_type="subaward" if mix == "federal" else "dc_local_grant",
                pass_through_entity=OVSJG if mix == "federal" else "",
                period_start=ps, period_end=pe, fiscal_year=fy, fiscal_year_basis="dc_fy",
                amount=rc["amount"], amount_type="award_amount", source_type="dc_ovsjg",
                source_id="doc_ovsjg_recipients", source_page=rc["page"], conflict_flag=0,
                retrieved_date=file_date(rc["path"]), confidence="high", basis="documented",
                x_section="ovsjg_pdf", x_funding_source_raw=src, x_funding_mix=mix,
                x_purpose_text=get("abstract")[:500], x_agency_code="FO0", x_document=rel(rc["path"]),
                x_issue_date=iss, x_notes=("OVSJG department: " + get("dept")) if "dept" in cols and get("dept") else "")
            rows.append(attach_match(r, r["recipient_name_raw"]))
        tot = sum(r["amount"] for r in rows[n_before:])
        LOGS.append(f"- OVSJG FY{fy} PDF ({rel(p)}): {len(rows) - n_before} grant rows, total ${tot:,.0f}")
    return rows


def merge_ovsjg(layer: list[dict], pdf: list[dict]) -> list[dict]:
    """Enrich layer rows with matched FY2024/FY2025 PDF rows; add unmatched PDF rows and all FY2026 rows."""
    by_key = defaultdict(list)
    for r in layer:
        by_key[(r["fiscal_year"], r["amount"])].append(r)
    added, enriched, conflicts = [], 0, []
    for p in pdf:
        cands = [r for r in by_key.get((p["fiscal_year"], p["amount"]), []) if not r.get("_used")]
        best, bs = None, 0
        for r in cands:
            s = fuzz.token_set_ratio(norm_name(r["recipient_name_raw"]), norm_name(p["recipient_name_raw"]))
            if s > bs:
                best, bs = r, s
        if best is not None and bs >= 70:
            best["_used"] = True
            enriched += 1
            for k in ("assistance_listing", "funding_agency", "flow_type", "pass_through_entity", "period_start",
                      "period_end", "x_funding_source_raw", "x_funding_mix", "x_issue_date"):
                if p[k] != "":
                    best[k] = p[k]
            if not best["program_name"]:
                best["program_name"] = p["program_name"]
            best["x_corroborating_source_id"] = "doc_ovsjg_recipients"
            best["x_corroborating_page"] = p["source_page"]
        else:
            if p["fiscal_year"] in (2024, 2025):
                conflicts.append(f"FY{p['fiscal_year']} {p['recipient_name_raw'][:40]} ${p['amount']:,}")
                p["x_notes"] = (p["x_notes"] + "; " if p["x_notes"] else "") + \
                    "PDF row with no layer row of the same FY, amount and grantee"
            added.append(p)
    for r in layer:
        r.pop("_used", None)
    unl = [f"FY{r['fiscal_year']} {r['recipient_name_raw'][:40]} ${r['amount']:,}" for r in layer
           if r["fiscal_year"] in (2024, 2025) and not r["x_corroborating_source_id"]]
    LOGS.append(f"- OVSJG merge: {enriched} FY2024/FY2025 layer rows enriched from the PDFs (funding source, period, "
                f"issue date); {len(added)} PDF rows added ({sum(1 for a in added if a['fiscal_year'] == 2026)} FY2026); "
                f"PDF rows without a layer match: {len(conflicts)} {conflicts[:6]}; layer FY2024/25 rows without a PDF "
                f"match: {len(unl)} {unl[:6]}")
    return layer + added


# ---------------------------------------------------------------- 3. DHS oversight tables
def _cluster(vals, tol=3.0):
    out = []
    for v in sorted(vals):
        if not out or v - out[-1][-1] > tol:
            out.append([v])
        else:
            out[-1].append(v)
    return [sum(c) / len(c) for c in out]


def ruled_tables(page) -> list[list[list[str]]]:
    """Ruled-table cells by word centre (more reliable than pdfplumber's char-in-cell for merged cells).
    Empty columns are dropped."""
    words = page.extract_words()
    res = []
    for t in page.find_tables():
        xs = _cluster([c[0] for c in t.cells] + [c[2] for c in t.cells])
        rws = [(r.bbox[1], r.bbox[3]) for r in t.rows]
        x0, top, x1, bot = t.bbox
        grid = [[[] for _ in range(len(xs) - 1)] for _ in rws]
        for w in words:
            cy, cx = (w["top"] + w["bottom"]) / 2, (w["x0"] + w["x1"]) / 2
            if not (x0 - 1 <= cx <= x1 + 1 and top - 1 <= cy <= bot + 1):
                continue
            ri = next((i for i, (a, b) in enumerate(rws) if a - 0.5 <= cy <= b + 0.5), None)
            ci = next((i for i in range(len(xs) - 1) if xs[i] - 0.5 <= cx <= xs[i + 1] + 0.5), None)
            if ri is not None and ci is not None:
                grid[ri][ci].append(w)
        out = [[" ".join(w["text"] for w in sorted(c, key=lambda w: (round(w["top"]), w["x0"]))) for c in r]
               for r in grid]
        keep = [j for j in range(len(xs) - 1) if any(r[j] for r in out)]
        res.append([[r[j] for j in keep] for r in out])
    return res


POH = {"2024": "POH2024_DHS_responses", "2025": "POH2025_DHS_responses", "2026": "POH2026_DHS_responses"}
TOTAL_RX = re.compile(r"^(total|grand total|total erap grants|total budget|total youth)", re.I)
# (cycle, page, table index, section, amount labels [(fiscal_year, label)], options)
DHS_TABLES = [
    ("2024", 24, 1, "erap_arpa_grants", [(2023, "ARPA"), (2023, "ERA2"), (2023, "Local")], {"q": 43}),
    ("2024", 26, 0, "homelessness_prevention", [(2023, "FY23"), (2024, "FY24 YTD")], {"q": 48}),
    ("2024", 35, 1, "youth_dhs_direct_nonhousing", [(2023, "FY23 award"), (2024, "FY24 award")], {"q": 58}),
    ("2024", 35, 2, "youth_tcp_housing", [(2023, "FY23 grant"), (2024, "FY24 grant")], {"q": 58, "tcp": 1}),
    ("2024", 36, 0, "youth_tcp_housing", [(2023, "FY23 grant"), (2024, "FY24 grant")], {"q": 58, "tcp": 1}),
    ("2024", 36, 2, "youth_dhs_direct_housing", [(2023, "FY23 grant"), (2024, "FY24 grant")], {"q": 58}),
    ("2024", 37, 0, "youth_dhs_direct_housing", [(2023, "FY23 grant"), (2024, "FY24 grant")], {"q": 58}),
    ("2024", 59, 0, "psh_case_management", [(2023, "DHS local"), (2023, "Medicaid")], {"q": 88}),
    ("2024", 60, 0, "psh_case_management", [(2023, "DHS local"), (2023, "Medicaid")], {"q": 88}),
    ("2024", 111, 0, "singles_shelter_contracts", [(2024, "contract")], {"q": 77, "cap": 1}),
    ("2024", 112, 0, "singles_shelter_contracts", [(2024, "contract")], {"q": 77, "cap": 1}),
    ("2025", 40, 1, "erap_arpa_grants", [(2024, "ARPA"), (2024, "ERA2"), (2024, "Local")], {"q": 61}),
    ("2025", 49, 0, "homelessness_prevention", [(2024, "FY24"), (2025, "FY25 YTD")], {"q": 66}),
    ("2025", 67, 2, "youth_dhs_direct_nonhousing", [(2024, "FY24 award"), (2025, "FY25 award")], {"q": 80}),
    ("2025", 68, 0, "youth_dhs_direct_nonhousing", [(2024, "FY24 award"), (2025, "FY25 award")], {"q": 80}),
    ("2025", 68, 1, "youth_dhs_direct_housing", [(2024, "FY24 grant"), (2025, "FY25 grant")], {"q": 80}),
    ("2025", 69, 0, "youth_dhs_direct_housing", [(2024, "FY24 grant"), (2025, "FY25 grant")], {"q": 80}),
    ("2025", 69, 1, "youth_tcp_housing", [(2024, "FY24 grant"), (2025, "FY25 grant")], {"q": 80, "tcp": 1}),
    ("2025", 121, 1, "psh_case_management", [(2024, "DHS local"), (2024, "Medicaid")], {"q": 119}),
    ("2025", 131, 0, "dv_grantees", [(2024, "FY2024 total grant award"), (2025, "FY2025 total grant award")],
     {"q": 129}),
    ("2025", 132, 0, "dv_grantees", [(2024, "FY2024 total grant award"), (2025, "FY2025 total grant award")],
     {"q": 129}),
    ("2026", 138, 0, "dv_grantees", [(2026, "FY26 funding"), (2026, "Council one-time enhancement")], {"desc": 1}),
    ("2026", 139, 0, "dv_grantees", [(2026, "FY26 funding"), (2026, "Council one-time enhancement")], {"desc": 1}),
    ("2026", 140, 0, "dv_grantees", [(2026, "FY26 funding"), (2026, "Council one-time enhancement")], {"desc": 1}),
    ("2026", 141, 0, "dv_grantees", [(2026, "FY26 funding"), (2026, "Council one-time enhancement")], {"desc": 1}),
]
SECTION_META = {  # section -> (flow_type, award_type, program label, confidence)
    "erap_arpa_grants": ("", "grant", "Emergency Rental Assistance Program (ERAP) grants", "high"),
    "homelessness_prevention": ("dc_local_grant", "grant", "Homelessness Prevention Program (families)", "high"),
    "youth_dhs_direct_nonhousing": ("dc_local_grant", "grant", "Youth homelessness services (DHS direct, non-housing)",
                                    "high"),
    "youth_dhs_direct_housing": ("dc_local_grant", "grant", "Youth homelessness housing programs (DHS direct)", "high"),
    "youth_tcp_housing": ("subaward", "grant", "Youth homelessness housing programs (DHS sole-source grant to TCP)",
                          "high"),
    "psh_case_management": ("dc_contract", "contract", "Permanent Supportive Housing case management", "high"),
    "singles_shelter_contracts": ("dc_contract", "contract", "Singles shelter / housing provider contract", "medium"),
    "dv_grantees": ("dc_local_grant", "grant", "DHS domestic violence services grants", "high"),
}
ERAP_FUND = {"ARPA": ("21.027", "U.S. Department of the Treasury (ARPA SLFRF)", "subaward"),
             "ERA2": ("21.023", "U.S. Department of the Treasury (Emergency Rental Assistance)", "subaward"),
             "Local": ("", "DC local funds", "dc_local_grant")}


ZERO_ROWS = [0]


def dhs_oversight_rows() -> list[dict]:
    rows, ties = [], []
    pdfs = {}
    for cyc, pat in POH.items():
        p = raw1("dc_council", f"{pat}_*.pdf")
        pdfs[cyc] = (p, pdfplumber.open(p))
    last_provider: dict[tuple, str] = {}
    totals: dict[tuple, list] = defaultdict(lambda: [None, 0])  # (cycle, section, label) -> [printed, parsed]
    try:
        for cyc, page, ti, section, labels, opt in DHS_TABLES:
            p, pdf = pdfs[cyc]
            tables = ruled_tables(pdf.pages[page - 1])
            if ti >= len(tables):
                LOGS.append(f"- WARN DHS {cyc} p{page}: table {ti} not found")
                continue
            for cells in tables[ti]:
                money_idx = [j for j, c in enumerate(cells) if is_money_cell(c) or c.strip() in ("N/A", "-", "$-")]
                text_idx = [j for j, c in enumerate(cells) if c and j not in money_idx]
                if not money_idx:
                    continue
                if opt.get("cap"):     # capacity / clients columns follow the single amount column
                    money_idx = money_idx[:1]
                provider = cells[text_idx[0]] if text_idx and text_idx[0] < money_idx[0] else ""
                prog_cells = [cells[j] for j in text_idx[1:] if j < money_idx[0]]
                program = prog_cells[0] if prog_cells else ""
                desc = prog_cells[1] if opt.get("desc") and len(prog_cells) > 1 else ""
                if TOTAL_RX.match(provider):
                    for (fy, lab), j in zip(labels, money_idx):
                        totals[(cyc, section, lab)][0] = money(cells[j])
                    continue
                if not provider:
                    provider = last_provider.get((cyc, section), "")
                last_provider[(cyc, section)] = provider
                extra = {}
                if section == "psh_case_management":   # 2024 table: '# clients assigned', 'avg caseload' columns
                    extra = {"x_clients_served": prog_cells[0] if prog_cells else "",
                             "x_capacity": ("avg caseload 1:" + prog_cells[1]) if len(prog_cells) > 1 else ""}
                    program = ""
                if opt.get("cap"):
                    after = [c for c in cells[money_idx[0] + 1:]]
                    extra = {"x_capacity": after[0] if after else "", "x_clients_served": after[1] if len(after) > 1
                             else ""}
                for (fy, lab), j in zip(labels, money_idx):
                    amt = money(cells[j])
                    if amt is None:
                        continue
                    totals[(cyc, section, lab)][1] += amt
                    if amt == 0:
                        ZERO_ROWS[0] += 1
                        continue
                    flow, atype, prog_label, conf = SECTION_META[section]
                    aln, fund_ag, ptype = "", DHS, flow
                    pass_ent, pass_ein, notes = "", "", []
                    if section == "erap_arpa_grants":
                        aln, fund_ag, ptype = ERAP_FUND[lab]
                        if ptype == "subaward":
                            pass_ent = DHS
                    if section == "youth_tcp_housing":
                        pass_ent, pass_ein = TCP_NAME, TCP_EIN
                        notes.append("table header states DHS funds these programs through a sole-source grant "
                                     "to TCP, which subgrants to providers")
                    if section == "psh_case_management" and lab == "Medicaid":
                        aln, fund_ag, atype = "93.778", "Medicaid (DC Department of Health Care Finance / HHS CMS)", \
                            "direct_payment"
                        notes.append("Medicaid funding for PSH case management as reported by DHS")
                    if section == "dv_grantees" and re.search(r"FVPSA|Federal fund", provider + " " + desc, re.I):
                        aln, fund_ag, ptype, pass_ent = "93.671", "U.S. HHS Family Violence Prevention and Services " \
                                                                  "Act (FVPSA)", "subaward", DHS
                    if lab == "Council one-time enhancement":
                        notes.append("Council one-time FY2026 enhancement")
                    if "YTD" in lab:
                        notes.append("fiscal-year-to-date amount at the time of the response")
                    if section == "singles_shelter_contracts":
                        notes.append("question asked for FY23 and FY24-to-date; the attachment shows one contract "
                                     "amount; fiscal year assumed FY2024")
                    prov_clean = re.sub(r"\s*\((FVPSA|MOU)[^)]*\)?\s*", " ", provider).strip()
                    r = base_row(
                        recipient_name_raw=provider, awarding_agency=DHS, funding_agency=fund_ag,
                        program_name=f"{prog_label}: {program}" if program else prog_label,
                        assistance_listing=aln, award_type=atype, flow_type=ptype,
                        pass_through_entity=pass_ent, pass_through_ein=pass_ein, fiscal_year=fy,
                        fiscal_year_basis="dc_fy", amount=amt,
                        amount_type="expenditure" if lab == "Medicaid" else "award_amount",
                        source_type="dc_oversight", source_id="doc_dc_council_oversight", source_page=page,
                        conflict_flag=0, retrieved_date=file_date(p), confidence=conf, basis="documented",
                        x_section=section, x_funding_source_raw=lab,
                        x_funding_mix="federal" if ptype == "subaward" else ("local" if lab != "Medicaid" else
                                                                             "medicaid"),
                        x_purpose_text=desc[:500], x_agency_code="JA0", x_document=rel(p),
                        x_ytd=1 if "YTD" in lab else "", x_notes="; ".join(notes),
                        **extra)
                    attach_match(r, prov_clean or provider)
                    if r["recipient_ein"] == CALVARY_EIN and section == "singles_shelter_contracts":
                        r["x_pass_through_inferred"] = ("The Community Partnership (TCP): Calvary's FY2023 audit SEFA "
                                                        "lists TCP as pass-through for DHS funds; not stated on this "
                                                        "page")
                    r["award_row_id"] = row_id("dhs", cyc, page, ti, provider, program, fy, lab, amt)
                    rows.append(r)
        # shelter contract modifications (2025 cycle, Q102, pp 87-96): one row per contract period line
        p, pdf = pdfs["2025"]
        site = prov = ""
        seen = set()
        for page in range(86, 97):
            for ln in (pdf.pages[page - 1].extract_text() or "").splitlines():
                m = re.search(r"Site/Provi\w*\s+(.+?)\s*/\s*(.+)$", ln)
                if m:
                    site, prov = clean_ws(m.group(1)), clean_ws(m.group(2))
                    continue
                m = re.search(r"Site/Provi\w*\s+(.+?)\s*\((.+?)\)\s*$", ln)
                if m:
                    site, prov = clean_ws(m.group(1)), clean_ws(m.group(2))
                    continue
                for m in re.finditer(r"(\d{1,2}/\d{1,2}/\d{2,4})\s*-\s*(\d{1,2}/\d{1,2}//?\d{2,4})\s*\(([A-Z0-9-]+)\)?"
                                     r"\s*\)?\s*[:\-]\s*\$([\d,]+\.\d\d)(\s*Services Only)?", ln):
                    a, b, code, amt, svc = m.groups()
                    ps, pe = parse_period(a.replace("//", "/") + " " + b.replace("//", "/"))
                    key = (code, ps, pe, amt)
                    if key in seen:
                        continue
                    seen.add(key)
                    fy = int(pe[:4]) + (1 if int(pe[5:7]) >= 10 else 0) if pe else ""
                    # contract codes carry the provider in the code, e.g. 2306CC801E (Catholic Charities),
                    # 2413SNSTPHP (N Street Village Patricia Handy); a code repeated under another site keeps the
                    # first site's provider
                    r = base_row(
                        recipient_name_raw=prov, awarding_agency=DHS, funding_agency=DHS,
                        program_name=f"Singles shelter contract: {site}" + (" (services only)" if svc else ""),
                        award_id=code, award_type="contract", flow_type="dc_contract", period_start=ps,
                        period_end=pe, fiscal_year=fy, fiscal_year_basis="dc_fy", amount=money(amt),
                        amount_type="obligation", source_type="dc_oversight", source_id="doc_dc_council_oversight",
                        source_page=page, conflict_flag=0, retrieved_date=file_date(p), confidence="medium",
                        basis="documented", x_section="singles_shelter_contract_periods", x_agency_code="JA0",
                        x_document=rel(p),
                        x_notes="contract period line (Q102); periods overlap across modifications, so sums by FY "
                                "may double count; fiscal_year = DC FY of the period end date")
                    attach_match(r, prov)
                    r["award_row_id"] = row_id("dhs_mod", code, ps, pe, amt)
                    rows.append(r)
                for m in re.finditer(r"FY(\d\d)\s*-?\s*(?:([A-Za-z][A-Za-z .']+?)\s*)?:\s*\$([\d.,]+)", ln):
                    fy2, who, amt = m.groups()
                    who = clean_ws(who) or prov
                    key = ("sub", site, who, fy2, amt)
                    if key in seen or not re.search(r"Sub-|Grant|FY2\d", ln):
                        continue
                    seen.add(key)
                    r = base_row(
                        recipient_name_raw=who, awarding_agency=DHS, funding_agency=DHS,
                        program_name=f"Singles shelter sub-grant: {site}", award_type="grant", flow_type="subaward",
                        fiscal_year=2000 + int(fy2), fiscal_year_basis="dc_fy", amount=money(amt),
                        amount_type="award_amount", source_type="dc_oversight", source_id="doc_dc_council_oversight",
                        source_page=page, conflict_flag=0, retrieved_date=file_date(p), confidence="medium",
                        basis="documented", x_section="singles_shelter_subgrants", x_agency_code="JA0",
                        x_document=rel(p), x_notes="printed as 'Sub-Grant'; the grantor (likely TCP) is not stated")
                    attach_match(r, who)
                    r["award_row_id"] = row_id("dhs_sub", site, who, fy2, amt)
                    rows.append(r)
    finally:
        for _, pdf in pdfs.values():
            pdf.close()
    for (cyc, section, lab), (printed, parsed) in sorted(totals.items()):
        if printed is not None:
            ok = abs(printed - parsed) <= 2
            ties.append(f"{cyc} {section} [{lab}] printed ${printed:,} vs parsed ${parsed:,} -> "
                        f"{'tie' if ok else 'DIFF ' + format(parsed - printed, ',')}")
    CHECKS.extend(f"- DHS oversight tie-out: {t}" for t in ties)
    by = Counter((r["x_section"]) for r in rows)
    LOGS.append(f"- DHS oversight provider tables: {len(rows)} rows; by section {dict(by)}; $0 cells skipped: "
                f"{ZERO_ROWS[0]}")
    return rows


# ---------------------------------------------------------------- 4. PASS (POs + payments) for universe vendors
DCGIS = "https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Government_Operations/MapServer"
F_PO = ("PONUMBER,AGENCYCODE,AGENCY_ACRONYM,AGENCY_NAME,STATUS,CONTRACTNUMBER,SUPPLIER,ORDEREDDATE,CREATEDATE,"
        "POTOTAL,FISCALYEAR,POTITLE,COMMODITYCODE,COMMODITYNAME,OBJECT_ID")   # no REQUESTER (staff names)
SKIP_SUPPLIER = re.compile(r"calvary\s+health|mt\.?\s+calvary|mount\s+calvary", re.I)
S = None
RL = RateLimiter(2.0)


def arc(layer: int, desc: str, params: dict) -> list[dict]:
    """Paged DC GIS query; every page saved raw. Returns attribute dicts.
    Statistics queries ignore resultOffset on this server, so they are sent once and must stay under the
    1,000-row limit (callers split them); a repeated first record also stops paging."""
    global S
    S = S or session()
    out, offset, page, first = [], 0, 0, None
    is_stats = "outStatistics" in params
    while True:
        q = dict(params, f="json")
        if not is_stats:
            q.update(resultOffset=offset, resultRecordCount=1000)
        RL.wait()
        r = S.get(f"{DCGIS}/{layer}/query", params=q, timeout=180)
        r.raise_for_status()
        save_raw("dc_gov", f"{desc}_p{page}", r.content, "json")
        d = r.json()
        if "error" in d:
            raise RuntimeError(f"{desc}: {d['error']}")
        fs = [f["attributes"] for f in d.get("features", [])]
        if is_stats:
            if d.get("exceededTransferLimit"):
                raise OverflowError(desc)
            return fs
        if fs and first is not None and fs[0] == first:
            raise RuntimeError(f"{desc}: server repeated page {page}; pagination not honoured")
        first = fs[0] if fs else None
        out += fs
        if not (d.get("exceededTransferLimit") or len(fs) == 1000):
            break
        offset += len(fs)
        page += 1
    return out


def stats_safe(layer: int, desc: str, names: list[str], field: str, group: str, count_f: str, sum_f: str,
               extra=(), descs: list | None = None) -> list[dict]:
    """Grouped statistics for a list of supplier names, split into smaller IN() lists (then by fiscal year)
    whenever a response would exceed the 1,000-row limit."""
    try:
        d = f"{desc}"
        rows = arc(layer, d, stats_params(group, count_f, sum_f, where=sql_in(field, names), extra_stats=extra))
        descs.append(d)
        return rows
    except OverflowError:
        if len(names) > 1:
            h = len(names) // 2
            return (stats_safe(layer, desc + "a", names[:h], field, group, count_f, sum_f, extra, descs) +
                    stats_safe(layer, desc + "b", names[h:], field, group, count_f, sum_f, extra, descs))
        out = []
        for fy in range(2013, 2028):
            d = f"{desc}_fy{fy}"
            out += arc(layer, d, stats_params(group, count_f, sum_f, where=sql_in(field, names) +
                                              f" AND FISCALYEAR = '{fy}'", extra_stats=extra))
            descs.append(d)
        return out


def load_pages(stamp: str, desc: str) -> list[dict]:
    """All pages of one paged pull saved by arc() under a given run stamp."""
    out = []
    files = sorted((RAW / "dc_gov").glob(f"*_{desc}_p*.json"),
                   key=lambda x: int(re.search(r"_p(\d+)\.json$", x.name).group(1)))
    files = [f for f in files if f.name.split("_")[0] >= stamp]
    # keep only the newest copy of each page number
    best = {}
    for f in files:
        n = int(re.search(r"_p(\d+)\.json$", f.name).group(1))
        if n not in best or f.name > best[n].name:
            best[n] = f
    for n in sorted(best):
        out += [x["attributes"] for x in json.loads(best[n].read_text()).get("features", [])]
    return out


def stats_params(group: str, count_field: str, sum_field: str, where: str = "1=1", extra_stats=()) -> dict:
    st = [{"statisticType": "count", "onStatisticField": count_field, "outStatisticFieldName": "n"},
          {"statisticType": "sum", "onStatisticField": sum_field, "outStatisticFieldName": "amt"}] + list(extra_stats)
    return {"where": where, "groupByFieldsForStatistics": group, "outStatistics": json.dumps(st),
            "orderByFields": group}


def sql_in(field: str, names: list[str]) -> str:
    return f"{field} IN (" + ",".join("'" + n.replace("'", "''") + "'" for n in names) + ")"


def pass_pull(refresh: bool) -> dict:
    """Run (or reuse) the PASS pulls. A manifest saved last in raw/dc_gov/ lists the run stamp and the
    paged descriptors so a rerun without --refresh-pass reads exactly the same raw files."""
    man = latest_raw("dc_gov", "dcgis_pass_universe_manifest.json")
    if man and not refresh:
        m = json.loads(man.read_text())
        data = {k: [] for k in ("po_sup", "pay_sup", "po", "pay")}
        for k, descs in m["descs"].items():
            for d in descs:
                data[k] += load_pages(m["stamp"], d)
        data["manifest"] = man
        return data
    from lib.common import stamp as _stamp
    run = _stamp()
    descs = {"po_sup": ["dcgis_pass_po_suppliers_distinct"], "pay_sup": ["dcgis_pass_pay_suppliers_distinct"],
             "po": [], "pay": []}
    data = {"po_sup": arc(16, descs["po_sup"][0], {"where": "1=1", "returnDistinctValues": "true",
                                                   "outFields": "SUPPLIER", "orderByFields": "SUPPLIER",
                                                   "returnGeometry": "false"}),
            "pay_sup": arc(17, descs["pay_sup"][0], {"where": "1=1", "returnDistinctValues": "true",
                                                     "outFields": "SUPPLIERNAME", "orderByFields": "SUPPLIERNAME",
                                                     "returnGeometry": "false"})}
    vend_po = sorted(n for n in (s.get("SUPPLIER") for s in data["po_sup"]) if n and not SKIP_SUPPLIER.search(n)
                     and M.match(n)[0])
    vend_pay = sorted(n for n in (s.get("SUPPLIERNAME") for s in data["pay_sup"]) if n and
                      not SKIP_SUPPLIER.search(n) and M.match(n)[0])
    data["po"], data["pay"] = [], []
    for k in range(0, len(vend_po), 40):
        d = f"dcgis_pass_po_universe_b{k // 40}"
        descs["po"].append(d)
        data["po"] += arc(16, d, {"where": sql_in("SUPPLIER", vend_po[k:k + 40]), "outFields": F_PO,
                                  "orderByFields": "OBJECT_ID"})
    ext = [{"statisticType": "min", "onStatisticField": "PAYMENTDATE", "outStatisticFieldName": "first_dt"},
           {"statisticType": "max", "onStatisticField": "PAYMENTDATE", "outStatisticFieldName": "last_dt"}]
    for k in range(0, len(vend_pay), 10):
        data["pay"] += stats_safe(17, f"dcgis_pass_pay_universe_b{k // 10}", vend_pay[k:k + 10], "SUPPLIERNAME",
                                  "SUPPLIERNAME,FISCALYEAR,AGENCYCODE,AGENCY_NAME,PONUMBER", "OBJECTID",
                                  "PAYMENTAMOUNT", ext, descs["pay"])
    data["manifest"] = save_raw("dc_gov", "dcgis_pass_universe_manifest",
                                {"stamp": run, "descs": descs, "n_po_vendors": len(vend_po),
                                 "n_pay_vendors": len(vend_pay)}, "json")
    return data


def pass_rows(refresh: bool) -> list[dict]:
    rows = []
    data = pass_pull(refresh)
    rdate = file_date(data["manifest"])
    po_names = [s["SUPPLIER"] for s in data["po_sup"] if s.get("SUPPLIER")]
    pay_names = [s["SUPPLIERNAME"] for s in data["pay_sup"] if s.get("SUPPLIERNAME")]
    vend_po = {n: M.match(n) for n in po_names if not SKIP_SUPPLIER.search(n)}
    vend_po = {n: m for n, m in vend_po.items() if m[0]}
    vend_pay = {n: M.match(n) for n in pay_names if not SKIP_SUPPLIER.search(n)}
    vend_pay = {n: m for n, m in vend_pay.items() if m[0]}
    LOGS.append(f"- PASS: {len(po_names):,} distinct PO suppliers, {len(pay_names):,} distinct payment suppliers; "
                f"matched to universe/TCP EINs: {len(vend_po)} PO supplier strings "
                f"({len({m[0] for m in vend_po.values()})} EINs), {len(vend_pay)} payment supplier strings "
                f"({len({m[0] for m in vend_pay.values()})} EINs); PO methods "
                f"{dict(Counter(m[2] for m in vend_po.values()))}")
    fuzzy = sorted({(n, m[1], m[3]) for n, m in list(vend_po.items()) + list(vend_pay.items()) if m[2] ==
                    "fuzzy_token_set"})
    LOGS.append(f"- PASS fuzzy supplier matches ({len(fuzzy)}): " + "; ".join(f"{a} -> {b} ({c})" for a, b, c in
                                                                             fuzzy[:80]))
    # dedupe EOM (AA0) sub-office fan-out: one row per PONUMBER + FISCALYEAR + POTOTAL
    pos = data["po"]
    uniq = {}
    for r in pos:
        k = (r.get("PONUMBER"), r.get("FISCALYEAR"), r.get("POTOTAL"))
        uniq.setdefault(k, r)
    LOGS.append(f"- PASS POs for universe vendors: {len(pos):,} raw rows -> {len(uniq):,} after dedupe on PONUMBER + "
                f"FISCALYEAR + POTOTAL (repeats removed: {len(pos) - len(uniq):,}, almost all AA0 sub-office fan-out)")
    for (po, fy, tot), r in uniq.items():
        sup = r.get("SUPPLIER")
        ein, bmf, method, score = vend_po.get(sup, ("", "", "unmatched", 0))
        title = clean_ws(r.get("POTITLE"))
        comm = clean_ws(r.get("COMMODITYNAME"))
        grant = bool(re.search(r"grant|\bVS\b", title, re.I) or re.search(r"Grants", comm))
        aa0 = r.get("AGENCYCODE") == "AA0"
        fyi = int(fy) if fy and str(fy).isdigit() else ""
        row = base_row(
            recipient_ein=ein, recipient_name_raw=sup,
            awarding_agency=("Executive Office of the Mayor (AA0)" if aa0 else clean_ws(r.get("AGENCY_NAME")) +
                             f" ({r.get('AGENCY_ACRONYM') or r.get('AGENCYCODE')})"),
            program_name=title, award_id=po, award_type="grant" if grant else "contract",
            flow_type="dc_local_grant" if grant else "dc_contract", fiscal_year=fyi, fiscal_year_basis="dc_fy",
            amount=money(tot), amount_type="obligation", source_type="dc_pass", source_id="api_dcgis_pass",
            source_page=f"layer16 PONUMBER {po}", conflict_flag=0, retrieved_date=rdate,
            confidence="high" if not (fyi and fyi >= 2025) else "medium", basis="documented",
            x_match_method=method, x_match_score=score, x_matched_bmf_name=bmf, x_recipient_name_norm=norm_name(sup),
            x_section="pass_po", x_agency_code=r.get("AGENCYCODE"), x_document=rel(data["manifest"]),
            x_po_status=r.get("STATUS"), x_po_version=(re.search(r"-V(\d+)$", po or "") or [None, ""])[1],
            x_commodity=comm, x_pass_incomplete_fy=1 if fyi and fyi >= 2025 else "",
            x_notes=("EOM sub-office acronym dropped (AA0 POs repeat once per sub-office)" if aa0 else ""))
        row["award_row_id"] = row_id("pass_po", po, fy, tot)
        rows.append(row)
    po_kind = {r["award_id"]: (r["flow_type"], r["award_type"], r["program_name"]) for r in rows}
    import datetime as _dt
    iso = lambda ms: _dt.datetime.fromtimestamp(ms / 1000, _dt.timezone.utc).date().isoformat() if ms else ""
    for a in data["pay"]:
        sup = a.get("SUPPLIERNAME")
        ein, bmf, method, score = vend_pay.get(sup, ("", "", "unmatched", 0))
        fy = a.get("FISCALYEAR")
        fyi = int(fy) if fy and str(fy).isdigit() else ""
        po = a.get("PONUMBER") or ""
        flow, atype, title = po_kind.get(po, ("dc_contract", "contract", ""))
        row = base_row(
            recipient_ein=ein, recipient_name_raw=sup,
            awarding_agency=f"{clean_ws(a.get('AGENCY_NAME'))} ({a.get('AGENCYCODE')})", program_name=title,
            award_id=po, award_type=atype, flow_type=flow, fiscal_year=fyi, fiscal_year_basis="dc_fy",
            amount=money(a.get("AMT", a.get("amt"))), amount_type="outlay", source_type="dc_pass",
            source_id="api_dcgis_pass", source_page=f"layer17 PONUMBER {po or '(none)'} FY{fy}",
            conflict_flag=0, retrieved_date=rdate,
            confidence="high" if not (fyi and fyi >= 2025) else "medium", basis="derived",
            x_match_method=method, x_match_score=score, x_matched_bmf_name=bmf, x_recipient_name_norm=norm_name(sup),
            x_section="pass_payments", x_agency_code=a.get("AGENCYCODE"), x_document=rel(data["manifest"]),
            x_n_payments=a.get("N", a.get("n")), x_first_payment_date=iso(a.get("FIRST_DT", a.get("first_dt"))),
            x_last_payment_date=iso(a.get("LAST_DT", a.get("last_dt"))),
            x_pass_incomplete_fy=1 if fyi and fyi >= 2025 else "",
            x_notes="sum of PASS payment rows for this supplier, fiscal year, agency and PO; flow/award type copied "
                    "from the PO when it is in the universe PO pull, else defaulted to dc_contract")
        row["award_row_id"] = row_id("pass_pay", sup, fy, a.get("AGENCYCODE"), po)
        rows.append(row)
    LOGS.append(f"- PASS payments for universe vendors: {len(data['pay']):,} supplier x FY x agency x PO aggregates; "
                f"FY2025+ rows flagged x_pass_incomplete_fy=1 (PASS incomplete from FY2025, financial-system change)")
    return rows


# ---------------------------------------------------------------- 5. HUD CoC DC-500
COMPONENTS = ["PH - Permanent Supportive Housing", "PH - Rapid Re-housing", "Joint TH - Rapid Re-housing",
              "Joint TH & PH-RRH", "Transitional Housing", "Supportive Services Only", "HMIS", "Safe Haven",
              "CoC Planning Grant", "UFA Costs", "YHDP Replacement", "Permanent Housing"]
STATUS_RX = re.compile(r"(Renewal|New|Expansion|YHDP|Planning|Reallocation|Replacement|UFA)\s+project", re.I)
# known applicants that are themselves the sponsor (project title has no sponsor prefix)
SPONSOR_FIX = {"department of human services": "DC Department of Human Services",
               "dhs": "DC Department of Human Services"}


def split_sponsor(project: str, applicant: str) -> str:
    """Sponsor named in the project title ('Calvary Women's Services - Sister Circle'), else the applicant."""
    m = re.match(r"^(.+?)\s*-\s+(.+)$", project) or re.match(r"^(N Street Village)-(.+)$", project)
    if m and not re.search(r"\b(FY)?20\d\d\b", m.group(1)) and m.group(1).count("(") == m.group(1).count(")"):
        return clean_ws(m.group(1))
    return applicant


def coc_row(year, applicant, project, status, component, amount, page, path, source_id, extra_note=""):
    applicant = clean_ws(re.sub(r"\(DC-500\)", "", applicant))
    is_tcp = bool(re.search(r"community partnership", applicant, re.I))
    sponsor = split_sponsor(project, applicant)
    sponsor_is_tcp = bool(re.search(r"community partnership|^tcp$|^coc planning", sponsor, re.I))
    if is_tcp and not sponsor_is_tcp and sponsor != applicant:
        recip, flow, pte, pein = sponsor, "subaward", TCP_NAME, TCP_EIN
    else:
        recip, flow, pte, pein = (applicant or sponsor), "prime", "", ""
    r = base_row(
        recipient_name_raw=recip, awarding_agency="U.S. HUD Office of Community Planning and Development",
        funding_agency="U.S. Department of Housing and Urban Development",
        program_name=f"Continuum of Care Program: {project}", assistance_listing="14.267", award_type="grant",
        flow_type=flow, pass_through_entity=pte, pass_through_ein=pein, fiscal_year=year,
        fiscal_year_basis="federal_fy", amount=amount, amount_type="award_amount", source_type="hud_coc",
        source_id=source_id, source_page=page, conflict_flag=0, retrieved_date=file_date(path), confidence="high",
        basis="documented", x_section="hud_coc", x_document=rel(path), x_component=component,
        x_project_status=status, x_sponsor_name=sponsor, x_prime_recipient_name=applicant,
        x_funding_mix="federal",
        x_notes=("; ".join(x for x in ["fiscal_year = CoC competition year (federal FY of the NOFO)", extra_note] if x)))
    attach_match(r, recip)
    return r


def awardcomp(year: int) -> tuple[list[dict], int | None]:
    p = raw1("hud", f"hudx_CoC_AwardComp_DC-500_{year}.pdf")
    rows, total, comp, cur = [], None, "", None
    with pdfplumber.open(p) as pdf:
        for pi, pg in enumerate(pdf.pages, start=1):
            txt = pg.extract_text() or ""
            if pi == 1:
                m = re.search(r"Total Award:\s*\$([\d,]+)", txt)
                total = money(m.group(1)) if m else None
            words = pg.extract_words()
            lines = defaultdict(list)
            for w in words:
                lines[round(w["top"] / 2.5)].append(w)
            started = pi > 1
            for k in sorted(lines):
                ws = sorted(lines[k], key=lambda w: w["x0"])
                text = clean_ws(" ".join(w["text"] for w in ws))
                if text.startswith("Project level award summary"):
                    started = True
                    continue
                if not started or text.startswith(("HUD's", "*Specific", "¹Expansion")) or re.match(
                        r"^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),", text):
                    continue
                if text.startswith("Recipient Name"):
                    continue
                if text in COMPONENTS or (not any(w["x0"] > 285 for w in ws) and text in COMPONENTS):
                    if text != "Permanent Housing":
                        comp = text
                    continue
                rec = clean_ws(" ".join(w["text"] for w in ws if w["x0"] < 288))
                proj = clean_ws(" ".join(w["text"] for w in ws if 288 <= w["x0"] < 500))
                typ = clean_ws(" ".join(w["text"] for w in ws if 500 <= w["x0"] < 638))
                amt = clean_ws(" ".join(w["text"] for w in ws if w["x0"] >= 638))
                if typ or amt:
                    cur = {"rec": rec, "proj": proj, "typ": typ, "amt": money(amt), "comp": comp, "page": pi}
                    rows.append(cur)
                elif cur is not None:      # wrapped recipient / project line
                    if rec:
                        cur["rec"] = clean_ws(cur["rec"] + " " + rec)
                    if proj:
                        cur["proj"] = clean_ws(cur["proj"] + " " + proj)
    out = []
    for c in rows:
        if c["amt"] is None:
            if not re.match(r"^(Project Name|Appropriation Act|and their expansion)", c["proj"]):
                LOGS.append(f"- WARN AwardComp {year} p{c['page']}: no amount for '{c['proj']}'")
            continue
        st = STATUS_RX.search(c["typ"])
        out.append(coc_row(year, c["rec"], c["proj"], st.group(1).title() if st else c["typ"], c["comp"], c["amt"],
                           c["page"], p, "doc_hud_coc_awards"))
    s = sum(r["amount"] for r in out)
    CHECKS.append(f"- HUD AwardComp DC-500 {year}: {len(out)} projects, parsed ${s:,} vs printed total "
                  f"${total or 0:,} -> {'tie' if total == s else 'DIFF ' + format(s - (total or 0), ',')}")
    return out, total


def giw(fy: int) -> list[dict]:
    import openpyxl
    p = raw1("hud", f"hudgov_FY{fy}_DC-500_GIW.xlsx")
    ws = openpyxl.load_workbook(p, data_only=True, read_only=True).active
    rows, hdr = [], None
    for r in ws.iter_rows(values_only=True):
        if r and r[0] == "Applicant Name":
            hdr = [clean_ws(x) for x in r]
            continue
        if hdr and r and r[0] and r[1]:
            d = dict(zip(hdr, r))
            rows.append({"applicant": clean_ws(d["Applicant Name"]), "project": clean_ws(d["Project Name"]),
                         "grant": clean_ws(d["Grant Number"]), "component": clean_ws(d["Project Component"]),
                         "restriction": clean_ws(d.get("Restriction (DV or YHDP)")), "ara": d.get("Total ARA"),
                         "units": d.get("Total Units")})
    return rows


def proj_key(s: str) -> str:
    s = norm_name(re.sub(r"\(Expansion\)|\b(FY)?20\d\d\b|Application", " ", s, flags=re.I))
    return s.replace("reallocation", "").replace(" ", "")


def hud_rows() -> list[dict]:
    out = []
    for y in range(2019, 2025):
        rs, _ = awardcomp(y)
        out += rs
    # GIW: grant numbers. FY2024 GIW lists the FY2023-competition grants (suffix ..23xx), FY2026 GIW the FY2025 ones.
    giw24, giw26 = giw(2024), giw(2026)
    for comp_year, g in ((2023, giw24), (2025, giw26)):
        gmap = {proj_key(x["project"]): x for x in g}
        for r in out:
            if r["fiscal_year"] == comp_year:
                x = gmap.get(proj_key(r["program_name"].split(": ", 1)[1]))
                if x:
                    r["award_id"] = x["grant"]
    # FY2025 award rounds (no applicant printed): applicant from the FY2026 GIW, else the 2024 AwardComp recipient
    prior = {proj_key(r["program_name"].split(": ", 1)[1]): r for r in out if r["fiscal_year"] == 2024}
    g26 = {proj_key(x["project"]): x for x in giw26}
    for rnd, page in ((1, 12), (2, 22), (3, 37)):
        p = raw1("hud", f"hudgov_FY2025_CoC_award_round{rnd}.pdf")
        n0 = len(out)
        with pdfplumber.open(p) as pdf:
            txt = pdf.pages[page - 1].extract_text() or ""
        printed = None
        for ln in txt.splitlines():
            m = re.match(r"^(.+?)\s+CoC\s+\$([\d,]+)$", ln.strip())
            if m:
                proj, amt = clean_ws(m.group(1)), money(m.group(2))
                k = proj_key(proj)
                x, pr = g26.get(k), prior.get(k)
                applicant = x["applicant"] if x else (pr["x_prime_recipient_name"] if pr else "")
                r = coc_row(2025, applicant or split_sponsor(proj, ""), proj, "", (x or {}).get("component", "") or
                            (pr or {}).get("x_component", ""), amt, page, p, "doc_hud_coc_awards",
                            extra_note=f"FY2025 award round {rnd}; applicant from "
                                       + ("FY2026 GIW" if x else "2024 AwardComp" if pr else "project title"))
                if x:
                    r["award_id"] = x["grant"]
                if not applicant:
                    r["confidence"] = "medium"
                out.append(r)
            m = re.match(r"^DC-500 Total\s*:\s*\$([\d,]+)", ln.strip())
            if m:
                printed = money(m.group(1))
        s = sum(r["amount"] for r in out[n0:])
        CHECKS.append(f"- HUD FY2025 round {rnd} DC-500 (p{page}): {len(out) - n0} projects, parsed ${s:,} vs printed "
                      f"${printed or 0:,} -> {'tie' if s == printed else 'DIFF'}")
    # cross-check FY2024 AwardComp vs hud.gov FY2024 DC report (Reach Up split into base + expansion there)
    p = raw1("hud", "hudgov_CoC-2024-DC_Press.pdf")
    with pdfplumber.open(p) as pdf:
        txt = "\n".join(pg.extract_text() or "" for pg in pdf.pages)
    press = defaultdict(int)
    for ln in txt.splitlines():
        m = re.match(r"^(.+?)\s+CoC\s+\$([\d,]+)$", ln.strip())
        if m:
            press[proj_key(m.group(1))] += money(m.group(2))
    ac = {proj_key(r["program_name"].split(": ", 1)[1]): r["amount"] for r in out if r["fiscal_year"] == 2024}
    diffs = [k for k in set(ac) | set(press) if ac.get(k) != press.get(k)]
    CHECKS.append(f"- HUD FY2024 AwardComp vs hud.gov DC report: {len(ac)} vs {len(press)} projects, "
                  f"total ${sum(ac.values()):,} vs ${sum(press.values()):,}; project-level differences "
                  f"{len(diffs)}: {sorted(diffs)[:8]}")
    for r in out:
        r["award_row_id"] = row_id("coc", r["fiscal_year"], r["program_name"], r["amount"], r["source_page"])
    LOGS.append(f"- HUD CoC DC-500: {len(out)} project rows ({dict(Counter(r['fiscal_year'] for r in out))}); "
                f"flow {dict(Counter(r['flow_type'] for r in out))}")
    return out


# ---------------------------------------------------------------- main
def main():
    global M
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh-pass", action="store_true")
    ap.add_argument("--no-pass", action="store_true", help=argparse.SUPPRESS)  # development only
    ap.add_argument("--no-log", action="store_true", help=argparse.SUPPRESS)   # development only
    args = ap.parse_args()
    M = Matcher()
    layer = ovsjg_layer()
    pdfr = ovsjg_pdf_rows()
    ovs = merge_ovsjg(layer, pdfr)
    for r in ovs:
        r["award_row_id"] = r["award_row_id"] or row_id("ovsjg", r["source_id"], r["source_page"], r["fiscal_year"],
                                                        r["recipient_name_raw"], r["program_name"], r["amount"])
    dhs = dhs_oversight_rows()
    hud = hud_rows()
    pas = [] if args.no_pass else pass_rows(args.refresh_pass)
    rows = ovs + dhs + hud + pas
    # program-area tags (as an x_ column) from program + purpose text
    from lib.tagging import tag_text
    for r in rows:
        r.setdefault("x_program_area_tags", "")
        r["x_program_area_tags"] = tag_text(f"{r['program_name']} {r['x_purpose_text']}")
    cols = COLS + ["x_program_area_tags"]
    # duplicates check
    ids = Counter(r["award_row_id"] for r in rows)
    dup_ids = [k for k, v in ids.items() if v > 1]
    full = Counter(tuple(str(r.get(c, "")) for c in cols if c != "award_row_id") for r in rows)
    dup_full = sum(v - 1 for v in full.values() if v > 1)
    CHECKS.append(f"- duplicates: award_row_id collisions {len(dup_ids)}; fully identical rows {dup_full}")
    if dup_ids:
        seen = set()
        out = []
        for r in rows:
            if r["award_row_id"] in seen:
                continue
            seen.add(r["award_row_id"])
            out.append(r)
        LOGS.append(f"- dropped {len(rows) - len(out)} rows with repeated award_row_id")
        rows = out
    rows.sort(key=lambda r: (r["source_type"], str(r["fiscal_year"]), r["recipient_name_raw"], str(r["amount"])))
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    # ---- checks: Calvary OVSJG rows vs recon
    cal = sorted((r["fiscal_year"], r["program_name"], r["amount"]) for r in rows
                 if r["recipient_ein"] == CALVARY_EIN and r["source_type"] == "dc_ovsjg")
    exp = {(2019, 368935), (2019, 292000), (2020, 368935), (2021, 368935), (2022, 3680675), (2022, 368935),
           (2022, 99500), (2023, 438500), (2023, 402540), (2024, 482528), (2024, 430873), (2025, 519656),
           (2025, 478622), (2026, 543056), (2026, 507595)}
    got = {(a, c) for a, b, c in cal}
    CHECKS.append(f"- Calvary OVSJG rows: {len(cal)} (FY2019-FY2025 layer {sum(1 for x in cal if x[0] <= 2025)}, "
                  f"FY2026 PDF {sum(1 for x in cal if x[0] == 2026)}); match recon: "
                  f"{'yes' if got == exp and len(cal) == 15 else 'NO missing ' + str(exp - got) + ' extra ' + str(got - exp)}")
    # ---- match rate for provider names in DC documents (non-PASS rows; PASS rows are matched by construction)
    nm = [r for r in rows if r["source_type"] != "dc_pass"]
    names = {}
    for r in nm:
        names.setdefault(r["recipient_name_raw"], r["recipient_ein"])
    m_names = sum(1 for v in names.values() if v)
    m_rows = sum(1 for r in nm if r["recipient_ein"])
    amt_all = sum(r["amount"] or 0 for r in nm)
    amt_m = sum(r["amount"] or 0 for r in nm if r["recipient_ein"])
    by_src = {}
    for st in sorted({r["source_type"] for r in nm}):
        sub = [r for r in nm if r["source_type"] == st]
        sn = {}
        for r in sub:
            sn.setdefault(r["recipient_name_raw"], r["recipient_ein"])
        by_src[st] = f"{sum(1 for v in sn.values() if v)}/{len(sn)} names, {sum(1 for r in sub if r['recipient_ein'])}" \
                     f"/{len(sub)} rows"
    meth = Counter(r["x_match_method"] for r in nm)
    CHECKS.append(f"- provider-name match rate (non-PASS): {m_names}/{len(names)} distinct names "
                  f"({m_names / max(len(names), 1):.0%}), {m_rows}/{len(nm)} rows, "
                  f"{amt_m / max(amt_all, 1):.0%} of dollars; by source {by_src}; methods {dict(meth)}")
    fz = sorted({(r["recipient_name_raw"], r["x_matched_bmf_name"], r["x_match_score"]) for r in nm
                 if r["x_match_method"] == "fuzzy_token_set"})
    LOGS.append(f"- fuzzy name matches in DC/HUD documents ({len(fz)}): " +
                "; ".join(f"{a} -> {b} ({c})" for a, b, c in fz))
    summary = Counter((r["source_type"], r["x_section"]) for r in rows)
    (print if args.no_log else (lambda t: log("36_parse_dc_awards", t)))("\n".join(
        [f"- wrote {rel(OUT)}: {len(rows):,} rows; by source/section: " +
         "; ".join(f"{a}/{b} {n}" for (a, b), n in sorted(summary.items())),
         "- decisions: OVSJG flow_type dc_local_grant unless the stated funding source is federal only (then "
         "subaward with OVSJG as pass-through); assistance_listing filled only from the stated funding source (VOCA "
         "16.575, STOP VAWA 16.588, SASP 16.017, Byrne JAG 16.738, JJDP Title II 16.540, Title V 16.548, RSAT 16.593, "
         "Coverdell 16.742, ARPA -> SLFRF 21.027); DHS ERAP ARPA/ERA2 shares are subawards (21.027/21.023); "
         "HUD CoC rows: TCP-applicant projects -> recipient = sponsor in the project title, flow subaward, "
         "pass-through TCP; other applicants -> prime; fiscal_year = CoC competition year (federal_fy)."]
        + LOGS + CHECKS))
    for c in CHECKS:
        print(c)
    print(f"wrote {rel(OUT)} rows={len(rows)}")


if __name__ == "__main__":
    main()
