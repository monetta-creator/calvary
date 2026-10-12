"""Phase 4 web pull: Calvary's own site (support page, financials page, WordPress media library) plus
Tavily searches for Calvary audits/annual reports hosted elsewhere.

Also holds the shared web helpers (WebFetcher: cached Tavily search/extract + polite HTTP GET, budget
counter, fetch manifest) used by scripts 44 and 45 via importlib.

Steps
  1. GET the live Corporate & Foundation Support page (calvaryservices.org/about/corporate/) -> raw/web.
  2. GET the financials page (calvaryservices.org/financials) -> raw/web; list every linked PDF.
  3. GET the WordPress media library (wp-json/wp/v2/media?mime_type=application/pdf) -> raw/web, to find
     PDFs uploaded but not linked from the financials page.
  4. Classify PDFs; keep annual reports, audits, 990s and funder/sponsor lists. A PDF counts as "already
     in inputs/" when its filename matches an inputs/ file and the server's Content-Length equals the
     local size; otherwise it is downloaded to raw/web.
  5. Tavily searches (config/web_queries.yaml: calvary.searches) for FY22/FY24/FY25 audits and FY24/FY25
     annual reports hosted off-site; any Calvary audit/annual-report PDF found is downloaded.
  6. Extract:
       - support page: funder names by tier with in-kind flag  -> interim/web_calvary_funders.csv
       - new annual reports: organizational donors by gift band (individuals as band counts only)
         -> interim/web_calvary_funders.csv, interim/web_calvary_donor_band_counts.csv
       - new audits: SOA/SFP lines + government-grant notes -> interim/web_new_audit_financials.csv;
         SEFA rows -> interim/web_new_audit_sefa.csv (same columns as raw/inputs_extracted/ files)
       - document list -> interim/web_calvary_docs.csv
  7. Register a web_ source per page/PDF and log counts and Tavily usage.

Usage:
  [ -f ~/.config/calvary/keys.env ] && set -a && . ~/.config/calvary/keys.env && set +a
  .venv/bin/python scripts/43_web_calvary.py [--refresh]
Tavily responses are cached through interim/web_fetch_manifest.csv: a rerun reuses the saved raw
response for the same query/URL unless --refresh is given (keeps reruns inside the Tavily budget).
"""
from __future__ import annotations

import csv
import hashlib
import importlib
import json
import re
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote, urlparse

import yaml

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import (CONFIG, INPUTS, INTERIM, RAW, ROOT, RateLimiter, env_key, log, norm_name,  # noqa: E402
                        register_source, rel, save_raw, session, sha256_file, today)

QUERIES = CONFIG / "web_queries.yaml"
MANIFEST = INTERIM / "web_fetch_manifest.csv"
MANIFEST_FIELDS = ["key", "kind", "label", "target", "raw_path", "retrieved_date", "status", "http_status",
                   "content_type", "bytes", "sha256", "api_calls", "notes"]
BUDGET = {"search": 300, "extract": 200}
RETRIEVED = today()
CALVARY_EIN = "521307706"


# =============================================================== shared web helpers
def slug(s: str, n: int = 80) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_")[:n]


def load_queries() -> dict:
    return yaml.safe_load(QUERIES.read_text(encoding="utf-8"))


class WebFetcher:
    """Cached Tavily search/extract and HTTP GET. Every response is saved untouched under raw/tavily or
    raw/web, and indexed in interim/web_fetch_manifest.csv (key -> raw file) so reruns reuse it."""

    def __init__(self, refresh: bool = False):
        self.refresh = refresh
        self.rows: dict[str, dict] = {}
        if MANIFEST.exists():
            with open(MANIFEST, newline="", encoding="utf-8") as f:
                for r in csv.DictReader(f):
                    self.rows[r["key"]] = r
        self.calls = {"search": 0, "extract": 0, "http": 0}
        self.cache_hits = 0
        self.http = session(retries=3, backoff=1.0)
        self.rl_http = RateLimiter(1.0)
        self.rl_tav = RateLimiter(2.0)
        self._client = None

    # ---- manifest
    def _save_manifest(self):
        MANIFEST.parent.mkdir(parents=True, exist_ok=True)
        with open(MANIFEST, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=MANIFEST_FIELDS, extrasaction="ignore")
            w.writeheader()
            w.writerows(self.rows.values())

    def _record(self, key, **kw):
        row = {k: "" for k in MANIFEST_FIELDS}
        row.update(key=key, retrieved_date=RETRIEVED, **kw)
        # cumulative api_calls per key (a refreshed key adds to the earlier count)
        prev = self.rows.get(key)
        if prev and prev.get("api_calls"):
            row["api_calls"] = str(int(prev["api_calls"] or 0) + int(row.get("api_calls") or 0))
        self.rows[key] = row
        self._save_manifest()
        return row

    def _cached(self, key):
        r = self.rows.get(key)
        if r and not self.refresh and r.get("raw_path") and (ROOT / r["raw_path"]).exists():
            self.cache_hits += 1
            return r
        return None

    def usage_total(self) -> dict:
        tot = {"search": 0, "extract": 0, "http": 0}
        for r in self.rows.values():
            k = r["kind"]
            if k in tot and r.get("api_calls"):
                tot[k] += int(r["api_calls"])
        return tot

    # ---- Tavily
    @property
    def client(self):
        if self._client is None:
            from tavily import TavilyClient
            key = env_key("TAVILY_API_KEY")
            if not key:
                raise SystemExit("TAVILY_API_KEY not set; source ~/.config/calvary/keys.env")
            self._client = TavilyClient(api_key=key)
        return self._client

    def _budget_ok(self, kind, n=1):
        used = self.usage_total()[kind]
        if used + n > BUDGET[kind]:
            print(f"  ! Tavily {kind} budget reached ({used}/{BUDGET[kind]}); skipping")
            return False
        return True

    def search(self, qid: str, query: str, **params) -> dict | None:
        params = {k: v for k, v in params.items() if v is not None}
        params.setdefault("max_results", 10)
        h = hashlib.sha1(json.dumps([query, params], sort_keys=True).encode()).hexdigest()[:10]
        key = f"search:{qid}:{h}"
        c = self._cached(key)
        if c:
            return json.loads((ROOT / c["raw_path"]).read_text(encoding="utf-8"))
        if not self._budget_ok("search"):
            return None
        self.rl_tav.wait()
        try:
            resp = self.client.search(query, **params)
            status = "ok"
        except Exception as e:  # noqa: BLE001
            resp, status = {"query": query, "params": params, "error": str(e)[:500]}, "failed"
        resp_saved = {"_request": {"query": query, "params": params, "qid": qid}, **resp}
        p = save_raw("tavily", f"search_{qid}", resp_saved, "json")
        self.calls["search"] += 1
        self._record(key, kind="search", label=qid, target=query, raw_path=rel(p), status=status,
                     api_calls="1", notes=f"{len(resp.get('results', []))} results")
        return resp_saved

    def extract(self, label: str, url: str, depth: str = "basic", fmt: str = "markdown") -> dict | None:
        key = f"extract:{depth}:{url}"
        c = self._cached(key)
        if c:
            d = json.loads((ROOT / c["raw_path"]).read_text(encoding="utf-8"))
            return d
        if not self._budget_ok("extract"):
            return None
        self.rl_tav.wait()
        try:
            resp = self.client.extract(url, extract_depth=depth, format=fmt, timeout=60)
            ok = bool(resp.get("results"))
            status = "ok" if ok else "no_content"
        except Exception as e:  # noqa: BLE001
            resp, status = {"url": url, "error": str(e)[:500]}, "failed"
        resp_saved = {"_request": {"url": url, "extract_depth": depth, "format": fmt, "label": label}, **resp}
        p = save_raw("tavily", f"extract_{label}", resp_saved, "json")
        self.calls["extract"] += 1
        n = sum(len(r.get("raw_content") or "") for r in resp.get("results", []))
        self._record(key, kind="extract", label=label, target=url, raw_path=rel(p), status=status,
                     bytes=str(n), api_calls="1")
        return resp_saved

    # ---- HTTP
    def get(self, label: str, url: str, ext: str | None = None, timeout: int = 60,
            headers: dict | None = None) -> dict:
        """GET url and save the body to raw/web. Returns the manifest row (+ 'path')."""
        key = f"http:{url}"
        c = self._cached(key)
        if c:
            return {**c, "path": ROOT / c["raw_path"]}
        self.rl_http.wait()
        try:
            r = self.http.get(url, timeout=timeout, headers=headers or {})
            ctype = r.headers.get("content-type", "")
            if ext is None:
                ext = "pdf" if ("pdf" in ctype or url.lower().endswith(".pdf")) else \
                    "json" if "json" in ctype else "html"
            body = r.content
            status = "ok" if r.status_code == 200 else f"http_{r.status_code}"
            if ext == "pdf" and not body[:5] == b"%PDF-":
                status = "not_pdf" if r.status_code == 200 else status
        except Exception as e:  # noqa: BLE001
            self.calls["http"] += 1
            row = self._record(key, kind="http", label=label, target=url, status="failed",
                               notes=str(e)[:200], api_calls="1")
            return {**row, "path": None}
        p = save_raw("web", label, body, ext)
        self.calls["http"] += 1
        row = self._record(key, kind="http", label=label, target=r.url if r.url != url else url,
                           raw_path=rel(p), status=status, http_status=str(r.status_code),
                           content_type=ctype[:60], bytes=str(len(body)), sha256=sha256_file(p),
                           api_calls="1", notes="" if r.url == url else f"redirected from {url}")
        return {**row, "path": p}

    def head_size(self, url: str) -> int | None:
        self.rl_http.wait()
        try:
            r = self.http.head(url, timeout=30, allow_redirects=True)
            v = r.headers.get("content-length")
            return int(v) if v else None
        except Exception:  # noqa: BLE001
            return None

    def summary(self) -> str:
        tot = self.usage_total()
        return (f"this run: Tavily search {self.calls['search']}, extract {self.calls['extract']}, HTTP GET "
                f"{self.calls['http']}, cache hits {self.cache_hits}; cumulative (manifest): search "
                f"{tot['search']}/{BUDGET['search']}, extract {tot['extract']}/{BUDGET['extract']}, "
                f"HTTP {tot['http']}")


def html_text(content: bytes | str) -> str:
    """Visible text of an HTML document (scripts/styles/nav dropped), one block per line."""
    import lxml.html
    d = lxml.html.fromstring(content)
    for bad in d.xpath("//script|//style|//noscript|//svg"):
        bad.drop_tree()
    for el in d.xpath("//br|//p|//div|//li|//h1|//h2|//h3|//h4|//h5|//h6|//tr|//td|//th|//a|//span"):
        el.tail = ("\n" + el.tail) if el.tail else "\n"
    for img in d.xpath("//img[@alt]"):
        alt = (img.get("alt") or "").strip()
        if alt:
            img.tail = f"\n[img: {alt}]\n" + (img.tail or "")
    t = d.text_content()
    t = re.sub(r"[ \t\xa0]+", " ", t)
    return "\n".join(l.strip() for l in t.splitlines() if l.strip())


def pdf_text(p: Path, layout: bool = True) -> str:
    cmd = ["pdftotext"] + (["-layout"] if layout else []) + [str(p), "-"]
    try:
        return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        return ""


def ex02():
    """Phase 1 extraction module (scripts/02_extract_inputs.py), for its audit statement parser."""
    return importlib.import_module("02_extract_inputs")


# =============================================================== organization-name test (people-data rule)
ORG_KW = re.compile(
    r"\b(foundations?|fund|funds|trusts?|charitable|charities|philanthrop\w*|giving|grants?|endowment|"
    r"inc|incorporated|llc|llp|lp|ltd|pllc|pc|corp|corporation|company|companies|co|bank|bancorp|banking|"
    r"credit union|church|churches|parish|cathedral|chapel|congregation|synagogue|temple|mosque|ministr\w*|"
    r"diocese|archdiocese|catholic|lutheran|methodist|presbyterian|episcopal|baptist|jewish|unitarian|quaker|"
    r"friends meeting|association|assn|society|club|league|council|guild|chapter|sorority|fraternity|union|"
    r"cooperative|co-op|alliance|coalition|network|institute|university|college|school|schools|academy|"
    r"hospital|health|healthcare|medical|clinic|pharmacy|group|partners|partnership|capital|services|"
    r"solutions|systems|technologies|technology|tech|consulting|consultants|realty|real estate|properties|"
    r"development|developers|construction|builders|architects|architecture|engineering|engineers|law|"
    r"lawyers|attorneys|insurance|financial|finance|investments|investors|advisors|advisory|management|"
    r"enterprises|holdings|international|global|industries|studio|studios|restaurant|restaurants|hotel|hotels|"
    r"resorts|media|communications|press|publishing|federal|government|department|office|county|city|"
    r"district|agency|administration|commission|authority|bureau|ministry|embassy|united way|rotary|"
    r"kiwanis|lions|junior league|center|centre|initiative|project|program|programs|collaborative|"
    r"collective|federation|board|committee|corps|endowment|grantmakers|community|communities|employees|"
    r"staff|friends of|nonprofit|org|associates|brands|markets|market|foods|food|stores|store|motors|"
    r"energy|electric|power|gas|utilities|airlines|airways|labs|laboratories|pharmaceuticals|therapeutics|"
    r"bio|sciences|science|research|ventures|equity|securities|mortgage|title|lending|homes|housing|"
    r"apartments|residential|commercial|design|designs|marketing|advertising|agency|events|catering|"
    r"cafe|coffee|bakery|kitchen|brewing|brewery|wines|spirits|beverage|beverages|fitness|sports|"
    r"team|club|clubs|lodge|legion|vfw|aarp|ymca|ywca|scouts|girl scouts|boy scouts|fellowship|productions|"
    r"mission|missions|outreach|cares|care|relief|aid|services|ministries)\b", re.I)
KNOWN_CORPS = {
    "amazon", "google", "microsoft", "apple", "meta", "facebook", "ibm", "oracle", "salesforce", "deloitte",
    "kpmg", "pwc", "ey", "ernst young", "accenture", "booz allen hamilton", "lockheed martin", "northrop grumman",
    "boeing", "raytheon", "rtx", "general dynamics", "leidos", "saic", "verizon", "comcast", "at t", "t mobile",
    "target", "walmart", "costco", "giant", "giant food", "safeway", "whole foods", "whole foods market",
    "trader joes", "harris teeter", "wegmans", "starbucks", "nordstrom", "macys", "tjx", "marshalls",
    "td bank", "pnc", "truist", "m t bank", "citi", "citibank", "jpmorgan chase", "chase", "wells fargo",
    "bank america", "morgan stanley", "goldman sachs", "freddie mac", "fannie mae", "capital one",
    "kaiser permanente", "carefirst", "carefirst bluecross blueshield", "unitedhealthcare", "aetna", "cigna",
    "humana", "amerigroup", "medstar", "johns hopkins", "inova", "pfizer", "gilead", "danaher", "hilton",
    "marriott", "altria", "pepsico", "coca cola", "nike", "uber", "lyft", "doordash", "instacart", "airbnb",
    "pepco", "exelon", "washington gas", "dominion energy", "bge", "constellation", "jbg smith", "bozzuto",
    "whiting turner", "gensler", "hickok cole", "fannie", "freddie", "nationals", "washington nationals",
    "washington commanders", "monumental sports", "dc united", "washington spirit", "events dc",
    "the washington post", "washington post", "bloomberg", "politico", "axios", "nbc4", "wusa9", "wtop",
    "battelle", "nielsen", "stout", "schnabel", "mgac", "dchfa", "ecs", "key", "amtrak", "metro", "wmata",
    "clark construction", "davis construction", "hogan lovells", "covington", "arnold porter", "wilmerhale",
    "kirkland ellis", "skadden", "sidley", "venable", "dla piper", "akin", "akin gump", "crowell moring",
    "jones day", "white case", "latham watkins", "williams connolly", "pillsbury", "arent fox", "bracewell",
    "nelson mullins", "kroll", "edelman", "chemonics", "qlarant", "cvs", "walgreens", "rite aid", "ups",
    "fedex", "home depot", "lowes", "ikea", "best buy", "staples", "office depot", "ross", "old navy",
    "gap", "patagonia", "rei", "lush", "sephora", "ulta", "dove", "unilever", "procter gamble", "p g",
    "johnson johnson", "j j", "merck", "abbvie", "astrazeneca", "novartis", "sanofi", "genentech", "amgen",
    "biogen", "medtronic", "abbott", "hca", "adventist healthcare", "sibley", "georgetown", "howard",
    "gwu", "american university", "catholic university", "world bank", "imf", "international monetary fund",
    "idb", "inter american development bank", "aarp", "nfl", "nba", "mlb", "nhl", "wnba", "mls",
    "hbo", "netflix", "disney", "warner bros discovery", "discovery", "national geographic", "sirius xm",
    "iheartmedia", "radio one", "urban one", "tv one", "bet", "cbs", "abc", "nbc", "fox", "cnn", "npr",
    "pbs", "weta", "wamu", "accenture", "wiley", "mintz", "regeneron", "totem", "nielsen", "battelle", "pepsico",
    "deloitte", "costco", "radici", "polsinelli", "stout", "schnabel", "sheamoisture", "guidehouse", "smithbucklin",
    "boeing", "intel", "wegmans", "underwraps", "jll", "kpmg", "edelman",
}
PERSONISH = re.compile(r"^(mr|mrs|ms|dr|drs|rev|hon|the honorable|sen|rep|judge|prof)\.?\s|\bfamily$|\b(and|&) (mr|mrs)\b"
                       r"|^(the )?estate of\b|\bestate$"
                       r"|^anonymous|^in (memory|honor) of|\b(jr|sr|ii|iii|iv|esq)\.?$", re.I)


# keywords that are also common surnames: "Lynne Church", "Sara Bank" read as people, not organizations
SURNAME_KW = {"church", "chapel", "temple", "bank", "law", "mission", "union", "guild", "press", "care", "aid", "power",
              "gas", "title", "homes", "design", "energy", "market", "store", "team", "board", "office", "city",
              "county", "center", "community", "project", "program", "network", "alliance", "capital", "group",
              "partners", "media", "studio", "tech", "bio", "science", "research", "lending", "equity", "health",
              "food", "foods", "relief", "lodge", "legion", "corps", "college", "school", "academy", "fellowship",
              "mortgage", "financial", "development", "management", "advisors", "associates", "events", "kitchen",
              "coffee", "cafe", "bakery", "sports", "fitness", "outreach", "staff", "members", "employees"}


def _surname_like(n: str) -> bool:
    toks = n.replace(",", "").split()
    if not 2 <= len(toks) <= 3:
        return False
    last = toks[-1].lower().strip(".")
    if last not in SURNAME_KW:
        return False
    first = toks[0]
    mid_ok = len(toks) == 2 or re.fullmatch(r"[A-Z]\.?", toks[1])
    return bool(re.fullmatch(r"[A-Z][a-z]{1,12}", first)) and bool(mid_ok) and not ORG_KW.search(" ".join(toks[:-1]))


# named donor-advised fund accounts and personal trusts are individuals' giving vehicles: counted, not named
DAF_PERSONAL = re.compile(r"\b(charitable (gift |giving )?(fund|account)|giving (fund|account)|philanthropic fund|gift fund|"
                          r"family (giving )?fund|donor[- ]advised fund|donor advisor fund|donor fund|"
                          r"irrevocable trust|revocable trust|living trust|charitable gift trust|gift trust)\b|"
                          r"\bfund at (fidelity|schwab|vanguard)", re.I)
DAF_SPONSOR = re.compile(r"^(fidelity charitable|schwab charitable|vanguard charitable|national philanthropic trust|"
                         r"american endowment foundation|daffy|ayco charitable|goldman sachs philanthropy fund|"
                         r"bank of america charitable gift fund|morgan stanley global impact|ubs donor)", re.I)


def is_org_name(name: str) -> bool:
    """True when a donor-list line reads as an organization. Conservative: unknown multi-word names without
    an organizational keyword are treated as possible individuals and dropped (people-data rule)."""
    n = re.sub(r"\s+", " ", (name or "").replace("*", "").replace("†", "")).strip(" ,;.-–•·")
    if not n or len(n) < 2 or len(n) > 120:
        return False
    if DAF_SPONSOR.search(n):
        return True
    if DAF_PERSONAL.search(n):
        return False
    if re.search(r"\b(family foundation|family charitable foundation)\b", n, re.I):
        return True
    if PERSONISH.search(n):
        return False
    if re.search(r"\b(in memory|in honor|memorial gift)\b", n, re.I) and not ORG_KW.search(n):
        return False
    nn = norm_name(n)
    if DAF_SPONSOR.search(n):
        return True
    if DAF_PERSONAL.search(n):
        return False
    if nn in KNOWN_CORPS or nn in known_org_names():
        return True
    if _surname_like(n):
        return False
    if ORG_KW.search(n):
        return True
    toks = n.split()
    if len(toks) == 1:
        # a lone capitalized word is usually a wrapped surname; keep only acronyms, CamelCase or digits
        return bool(re.fullmatch(r"[A-Z0-9&.-]{2,}|[A-Z][a-z]+[A-Z]\w*|\w*\d\w*", n)) and \
            not re.match(r"^(Mc|Mac|O')[A-Z]", n) and n.lower() not in ("anonymous", "and", "the")
    if all(t.isupper() and len(t) >= 2 for t in toks if t.isalpha()):  # acronyms: "KPMG LLP", "DC SAFE"
        return True
    return False


_KNOWN = None


def known_org_names() -> set[str]:
    """Normalized organization names already known to the project (CRM, Phase 1 mentions, funder matches)."""
    global _KNOWN
    if _KNOWN is None:
        s = set()
        for p, col in [(RAW / "inputs_extracted" / "crm_funders_2023_2026.csv", "funder_name_norm"),
                       (RAW / "inputs_extracted" / "funder_mentions.csv", "funder_name_norm"),
                       (INTERIM / "known_funder_matches.csv", "name_norm")]:
            if p.exists():
                with open(p, newline="", encoding="utf-8") as f:
                    for r in csv.DictReader(f):
                        if r.get(col):
                            s.add(r[col])
        _KNOWN = s
    return _KNOWN



# =============================================================== Calvary specifics
SUPPORT_URL = "https://www.calvaryservices.org/about/corporate/"
FIN_URL = "https://calvaryservices.org/financials"
MEDIA_API = "https://www.calvaryservices.org/wp-json/wp/v2/media?mime_type=application/pdf&per_page=100&page={}"

# filename -> (doc_type, fiscal_year, source_id); filled for PDFs the classifier keeps
DOC_RULES = [  # (regex on filename, doc_type)
    (r"audit|financial-statements|audited|-FS(-\d)?\.pdf$", "audit"),
    (r"990", "form_990"),
    (r"annual-report|-AR[.-]|Annual-Design|At-Glance|AR-Working", "annual_report"),
    (r"Sponsors|Corporate-Partner|Partners-Program|Newsletter|Year-End-Report|Hope-Gala-Sponsorship", "funder_list"),
]


def classify(fname: str) -> str | None:
    for pat, t in DOC_RULES:
        if re.search(pat, fname, re.I):
            return t
    return None


def fy_guess(fname: str, upload_year: str) -> int | None:
    m = re.search(r"FY ?(\d{2,4})", fname, re.I)
    if m:
        y = int(m.group(1))
        return 2000 + y if y < 100 else y
    m = re.search(r"9\.30\.(\d{2})", fname)
    if m:
        return 2000 + int(m.group(1))
    m = re.search(r"(20\d\d)", fname)
    if m:
        return int(m.group(1))
    return None


def step_site(wf: WebFetcher):
    docs = []
    sup = wf.get("calvary_corporate_foundation_support", SUPPORT_URL, ext="html")
    register_source("web_calvary_corp_found_support", "Calvary Women's Services: Corporate & Foundation Support "
                    "(live page)", SUPPORT_URL, "Calvary Women's Services, Inc.", "Public web page",
                    "Live page; states 'Current as of September 2023'; cumulative 'over the years' list; "
                    "'*' marks in-kind. Supersedes the clipped PDF printout input_corp_found_support_2023.",
                    retrieved_date=RETRIEVED)
    fin = wf.get("calvary_financials", FIN_URL, ext="html")
    register_source("web_calvary_financials", "Calvary Women's Services: Financials page", FIN_URL,
                    "Calvary Women's Services, Inc.", "Public web page",
                    "Lists annual reports, audits and 990s by year; newest linked audit is FY23 (9.30.23).",
                    retrieved_date=RETRIEVED)
    import lxml.html
    linked = {}
    if fin.get("path"):
        d = lxml.html.fromstring(fin["path"].read_bytes())
        for a in d.xpath("//a[@href]"):
            h = a.get("href")
            if h.lower().endswith(".pdf"):
                linked[h] = a.text_content().strip()
    media = {}
    for pg in range(1, 6):
        m = wf.get(f"calvary_wp_media_pdf_p{pg}", MEDIA_API.format(pg), ext="json")
        if not m.get("path") or m["status"] != "ok":
            break
        try:
            js = json.loads(m["path"].read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            break
        if not isinstance(js, list) or not js:
            break
        for it in js:
            media[it["source_url"]] = it.get("date", "")[:10]
        # WP can return fewer than per_page items on a non-final page (hidden items), so page until an
        # empty list or an error status (page past the end returns HTTP 400)
    register_source("web_calvary_wp_media", "Calvary Women's Services WordPress media library (PDF listing)",
                    MEDIA_API.format(1), "Calvary Women's Services, Inc.", "Public WordPress REST API",
                    "Used only to find uploaded PDFs not linked from the financials page.", retrieved_date=RETRIEVED)
    local = {p.name: p.stat().st_size for p in INPUTS.glob("*.pdf")}
    urls = sorted(set(linked) | set(media))
    seen_sha = {}
    for u in urls:
        fname = unquote(urlparse(u).path.rsplit("/", 1)[-1])
        dtype = classify(fname)
        row = dict(url=u, filename=fname, linked_from_financials=u in linked, link_text=linked.get(u, ""),
                   upload_date=media.get(u, ""), doc_type=dtype or "other", in_inputs="", remote_bytes="",
                   local_bytes=local.get(fname, ""), raw_path="", sha256="", source_id="", fiscal_year="",
                   status="")
        if not dtype:
            row["status"] = "skipped_not_relevant"
            docs.append(row)
            continue
        if fname in local:
            size = wf.head_size(u)
            row["remote_bytes"] = size or ""
            if size == local[fname]:
                row.update(in_inputs=True, status="already_in_inputs")
                docs.append(row)
                continue
        row["in_inputs"] = False
        g = wf.get(f"calvary_{slug(fname[:-4], 70)}", u, ext="pdf")
        row.update(raw_path=g.get("raw_path", ""), sha256=g.get("sha256", ""), status=g["status"],
                   remote_bytes=g.get("bytes", row["remote_bytes"]))
        # identical bytes to an inputs/ file under another name -> duplicate
        if g.get("sha256"):
            for p in INPUTS.glob("*.pdf"):
                if p.stat().st_size == int(g["bytes"] or 0) and sha256_file(p) == g["sha256"]:
                    row.update(in_inputs=True, status=f"duplicate_of_input:{p.name}")
        if g.get("sha256") and g["sha256"] in seen_sha and not row["in_inputs"]:
            row.update(status=f"duplicate_of_web:{seen_sha[g['sha256']]}")
        elif g.get("sha256"):
            seen_sha[g["sha256"]] = u
        fy = fy_guess(fname, row["upload_date"])
        row["fiscal_year"] = fy or ""
        row["source_id"] = f"web_calvary_{slug(fname[:-4].lower(), 60)}"
        docs.append(row)
    return docs


def step_posts(wf: WebFetcher, q: dict) -> list[dict]:
    """Calvary blog/press posts that name funders (config calvary.posts) -> raw/web HTML + text."""
    out = []
    for p in q["calvary"].get("posts", []):
        g = wf.get(f"calvary_{p['id']}", p["url"], ext="html")
        sid = f"web_calvary_{p['id']}"
        txt = html_text(g["path"].read_bytes()) if g.get("path") and g["status"] == "ok" else ""
        if txt:
            title = next((l for l in txt.splitlines() if len(l) > 20), p["id"])[:120]
            register_source(sid, f"Calvary Women's Services post: {title}", p["url"], "Calvary Women's Services, Inc.",
                            "Public web page", f"blog/press post {p['year']}; raw: {g.get('raw_path')}",
                            retrieved_date=RETRIEVED)
        out.append(dict(p, source_id=sid, raw_path=g.get("raw_path", ""), status=g["status"], text=txt))
    return out


def extract_post_mentions(posts: list[dict], q: dict) -> tuple[list[dict], list[str]]:
    rows, notes = [], []
    for p in posts:
        if not p["text"]:
            notes.append(f"{p['id']}: no text ({p['status']})")
            continue
        flat = re.sub(r"\s+", " ", p["text"])
        for spec in p.get("named_lists", []):
            names = parse_named_list(p["text"], spec)
            for n in names:
                rows.append(dict(source_id=p["source_id"], document=p["url"], page="", report_year=p["year"],
                                 fiscal_year="", funder_name_raw=n, funder_name_norm=norm_name(n), org_type_guess="",
                                 gift_band_raw=spec.get("band", ""), band_min="", band_max="", in_kind_flag="",
                                 truncated=False, section_heading=spec["heading"], notes=spec.get("note", "")))
            notes.append(f"{p['id']} [{spec['heading']}]: {len(names)}")
        for m in p.get("mentions", []):
            mm = re.search(m["pattern"], flat)
            if not mm:
                notes.append(f"{p['id']}: mention '{m['name']}' pattern not found")
                continue
            amt = m.get("amount")
            lo, hi = (amt, amt) if amt else (m.get("band_min", ""), m.get("band_max", ""))
            rows.append(dict(source_id=p["source_id"], document=p["url"], page="", report_year=m.get("year", p["year"]),
                             fiscal_year="", funder_name_raw=m["name"], funder_name_norm=norm_name(m["name"]),
                             org_type_guess="", gift_band_raw=m.get("band", ""), band_min=lo, band_max=hi,
                             in_kind_flag=m.get("in_kind", ""), truncated=False,
                             section_heading="post: " + m.get("kind", "narrative mention"),
                             notes=(m.get("note", "") + (f"; amount stated: ${amt:,}" if amt else "")).strip("; "),
                             amount_kind_hint=m.get("amount_kind", ""), cumulative_hint=m.get("cumulative", ""),
                             purpose_hint=m.get("purpose", ""), quote=mm.group(0)[:200]))
    return rows, notes


def step_offsite_search(wf: WebFetcher, q: dict, docs: list[dict]):
    """Tavily searches for Calvary audits/annual reports not on calvaryservices.org/financials."""
    hits = []
    known = {d["url"] for d in docs}
    for s in q["calvary"]["searches"]:
        resp = wf.search(s["id"], s["query"], **s.get("params", {}))
        if not resp:
            continue
        for r in resp.get("results", []):
            hits.append(dict(qid=s["id"], url=r["url"], title=r.get("title", ""), score=r.get("score", "")))
    keep, rejected = [], []
    for h in hits:
        u = h["url"]
        if u in known or not u.lower().endswith(".pdf"):
            continue
        if not re.search(r"calvary", u + h["title"], re.I):
            continue
        if not re.search(r"audit|financial|annual|990|report", u + h["title"], re.I):
            continue
        known.add(u)
        fname = unquote(urlparse(u).path.rsplit("/", 1)[-1])
        g = wf.get(f"calvary_offsite_{slug(fname[:-4], 60)}", u, ext="pdf")
        head = pdf_text(ROOT / g["raw_path"], layout=False)[:6000] if g.get("raw_path") else ""
        if not re.search(r"CALVARY WOMEN", head, re.I):
            rejected.append(f"{fname} ({h['qid']}: not a Calvary Women's Services document)")
            continue
        keep.append(dict(url=u, filename=fname, linked_from_financials=False, link_text=h["title"][:80],
                         upload_date="", doc_type=classify(fname) or "other", in_inputs=False,
                         remote_bytes=g.get("bytes", ""), local_bytes="", raw_path=g.get("raw_path", ""),
                         sha256=g.get("sha256", ""), source_id=f"web_calvary_offsite_{slug(fname[:-4].lower(), 50)}",
                         fiscal_year=fy_guess(fname, "") or "", status=g["status"] + f"; found by {h['qid']}"))
    return hits, keep, rejected


# --------------------------------------------------------------- support page parse
def parse_support_page(path: Path) -> list[dict]:
    import lxml.html
    d = lxml.html.fromstring(path.read_bytes())
    rows = []
    sid = "web_calvary_corp_found_support"
    for sec in d.xpath("//div[contains(@class,'corporate-table-section')]"):
        t = sec.xpath(".//div[contains(@class,'corporate-partners-title')]")
        if not t:
            continue
        tier = t[0].text_content().strip()
        for p in sec.xpath(".//div[contains(@class,'corporate-partner') and not(contains(@class,'title'))"
                           " and not(contains(@class,'intro')) and not(contains(@class,'learn'))]"):
            img = p.xpath(".//img/@alt")
            inkind = bool(p.xpath(".//span[contains(@class,'in-kind')]"))
            name = (img[0] if img else p.text_content()).replace("*", "").strip()
            if not name:
                continue
            rows.append(dict(source_id=sid, tier=tier, section_heading=f"Corporate Partners Program: {tier}",
                             funder_name_raw=name, in_kind_flag=inkind, shown_as_logo=bool(img)))
    inst = d.xpath("//div[contains(@class,'corporate-table-title') and normalize-space()='Institutional Support']"
                   "/following-sibling::div[contains(@class,'corporate-table')][1]//div[contains(@class,'corporate-partner')]")
    for p in inst:
        name = p.text_content().replace("*", "").strip()
        if name:
            rows.append(dict(source_id=sid, tier="Institutional Support", section_heading="Institutional Support",
                             funder_name_raw=name, in_kind_flag=bool(p.xpath(".//span[contains(@class,'in-kind')]")),
                             shown_as_logo=False))
    out = []
    for r in rows:
        out.append(dict(source_id=r["source_id"], document=SUPPORT_URL, page="", report_year=2023, fiscal_year="",
                        funder_name_raw=r["funder_name_raw"], funder_name_norm=norm_name(r["funder_name_raw"]),
                        org_type_guess="", gift_band_raw=r["tier"], band_min="", band_max="",
                        in_kind_flag=r["in_kind_flag"], truncated=False, section_heading=r["section_heading"],
                        notes="cumulative list 'over the years', current as of September 2023; no amounts"
                              + ("; shown as logo (name from alt text)" if r["shown_as_logo"] else "")))
    return out


# --------------------------------------------------------------- annual-report donor lists
BAND_RE = re.compile(r"^\$[\d,]+(?:\s*(?:and above|\+|or more)|\s*(?:-|–|to)\s*\$?[\d,]+)", re.I)


def band_bounds(raw: str):
    m = re.search(r"\$([\d,]+)\s*(?:and above|\+|or more)", raw, re.I)
    if m:
        return int(m.group(1).replace(",", "")), ""
    m = re.search(r"\$([\d,]+)\s*(?:to|-|–)\s*\$?([\d,]+)", raw)
    if m:
        return int(m.group(1).replace(",", "")), int(m.group(2).replace(",", ""))
    m = re.search(r"(?:up to|under)\s*\$([\d,]+)", raw, re.I)
    if m:
        return "", int(m.group(1).replace(",", ""))
    return "", ""


def calvary_cfg_docs(q: dict) -> dict:
    return {d["filename"]: d for d in q["calvary"].get("documents", [])}


def extract_ar_donors(docs: list[dict], q: dict) -> tuple[list[dict], list[dict], list[str]]:
    """Organizational donors by gift band from new annual-report PDFs (Phase 1 approach: column crops in
    reading order, bold section headings, '$' band headings, wrapped names joined by tight leading).
    Hints per document in config/web_queries.yaml (calvary.documents[].donor_list). Individuals are
    counted per band, never named."""
    import pdfplumber
    cfg = calvary_cfg_docs(q)
    funders, bands, notes = [], defaultdict(int), []
    for d in docs:
        c = cfg.get(d["filename"])
        if not c or not c.get("donor_list") or not d.get("raw_path") or not d.get("source_id"):
            continue
        spec = c["donor_list"]
        skip_font = re.compile(spec.get("skip_fonts", r"(?!x)x"))
        wrap = float(spec.get("wrap_gap", 9.5))
        section = band = ""
        entries = []  # [page, section, band, text]
        with pdfplumber.open(ROOT / d["raw_path"]) as doc:
            for pg, bbox in spec["columns"]:
                crop = doc.pages[pg - 1].crop(tuple(bbox))
                prev_top, prev = None, None
                for l in crop.extract_text_lines(return_chars=True, strip=True):
                    t = re.sub(r"\s+", " ", l["text"].replace("\xa0", " ")).strip()
                    if not t:
                        continue
                    font = l["chars"][0]["fontname"].split("+")[-1]
                    size = l["chars"][0]["size"]
                    if skip_font.search(font) or size > spec.get("max_size", 12):
                        continue
                    if re.search(spec["org_section_re"], t, re.I):
                        section, band, prev_top = "org", "", None
                        continue
                    if re.search(spec["ind_section_re"], t, re.I):
                        section, band, prev_top = "ind", "", None
                        continue
                    if BAND_RE.match(t):
                        band, prev_top = t, None
                        continue
                    if "Bold" in font or not section or not band:
                        continue  # other headings / intro text
                    cont = re.match(spec.get("cont_re", r"^(Foundation|Fund|Trust|Charitable Trust|Connections Fund|"
                                                          r"Associates\b.*|Inc\.?|LLP|LLC)$"), t)
                    if prev is not None and prev_top is not None and (l["top"] - prev_top < wrap or cont):
                        prev[3] = prev[3] + " " + t
                    else:
                        prev = [pg, section, band, t]
                        entries.append(prev)
                    prev_top = l["top"]
        n_org = 0
        for pg, sec, bnd, name in entries:
            lo, hi = band_bounds(bnd)
            if sec == "ind":
                bands[(d["source_id"], d["filename"], c["report_year"], bnd, lo, hi)] += 1
                continue
            n_org += 1
            funders.append(dict(source_id=d["source_id"], document=d["filename"], page=pg,
                                report_year=c["report_year"], fiscal_year=c.get("fiscal_year", ""),
                                funder_name_raw=name, funder_name_norm=norm_name(name), org_type_guess="",
                                gift_band_raw=bnd, band_min=lo, band_max=hi, in_kind_flag="", truncated=False,
                                section_heading=spec.get("section_heading", "donor list"),
                                notes="anonymous organizational donor" if name.lower() == "anonymous" else ""))
        n_ind = sum(v for k, v in bands.items() if k[1] == d["filename"])
        notes.append(f"{d['filename']}: {n_org} org donor entries, {n_ind} individual entries (counted only)")
    band_rows = [dict(source_id=s, document=f, report_year=y, gift_band_raw=b, band_min=lo, band_max=hi,
                      individual_count=n) for (s, f, y, b, lo, hi), n in bands.items()]
    return funders, band_rows, notes


def parse_named_list(text: str, spec: dict) -> list[str]:
    """Organization names from a plain-text block between spec.start and spec.end (regexes, first match).
    Cells are split on 3+ spaces (layout text). spec.join maps a fragment to its continuation line;
    spec.drop lists exact cells to ignore. With org_list: true (the source labels the list as companies or
    organizations) only person-like cells are dropped; otherwise each cell must pass is_org_name()."""
    lines = text.splitlines()
    i0 = next((i for i, l in enumerate(lines) if re.search(spec["start"], l)), None)
    if i0 is None:
        return []
    i1 = next((i for i in range(i0 + 1, len(lines)) if spec.get("end") and re.search(spec["end"], lines[i])),
              len(lines))
    skip = re.compile(spec.get("skip", r"(?!x)x"), re.I)
    cells = []
    for l in lines[i0 + (0 if spec.get("include_start") else 1):i1]:
        if not l.strip() or skip.search(l):
            continue
        for c in re.split(spec.get("split", r"\s{3,}|\t+"), l.strip()):
            c = re.sub(r"[\uf000-\uf8ff]", "", c)
            c = re.sub(r"\s+", " ", c).strip(" •·●▪-–|")
            if c:
                cells.append(c)
    joins = spec.get("join", {}) or {}
    out = []
    for c in cells:
        if c in (spec.get("drop") or []) or c in joins.values():
            continue
        out.append(c + " " + joins[c] if c in joins else c)
    keep = []
    for c in out:
        if spec.get("org_list"):
            if not PERSONISH.search(c) and c.lower() != "anonymous":
                keep.append(c)
        elif is_org_name(c):
            keep.append(c)
    return list(dict.fromkeys(keep))


def extract_named_lists(docs: list[dict], q: dict) -> tuple[list[dict], list[str]]:
    cfg = calvary_cfg_docs(q)
    rows, notes = [], []
    for d in docs:
        c = cfg.get(d["filename"])
        if not c or not d.get("raw_path") or not d.get("source_id"):
            continue
        txt = None
        for spec in c.get("named_lists", []):
            txt = txt or pdf_text(ROOT / d["raw_path"])
            names = parse_named_list(txt, spec)
            for n in names:
                rows.append(dict(source_id=d["source_id"], document=d["filename"], page="",
                                 report_year=c["report_year"], fiscal_year=c.get("fiscal_year", ""),
                                 funder_name_raw=n, funder_name_norm=norm_name(n), org_type_guess="",
                                 gift_band_raw=spec.get("band", ""), band_min=spec.get("band_min", ""),
                                 band_max=spec.get("band_max", ""), in_kind_flag="", truncated=False,
                                 section_heading=spec["heading"], notes=spec.get("note", "")))
            notes.append(f"{d['filename']} [{spec['heading']}]: {len(names)}")
        for m in c.get("mentions", []):
            txt = txt or pdf_text(ROOT / d["raw_path"])
            flat = re.sub(r"\s+", " ", txt)
            if re.search(m["pattern"], flat):
                rows.append(dict(source_id=d["source_id"], document=d["filename"], page="",
                                 report_year=c["report_year"], fiscal_year=c.get("fiscal_year", ""),
                                 funder_name_raw=m["name"], funder_name_norm=norm_name(m["name"]),
                                 org_type_guess="", gift_band_raw="", band_min="", band_max="",
                                 in_kind_flag=m.get("in_kind", ""), truncated=False,
                                 section_heading="narrative mention", notes=m.get("note", "")))
            else:
                notes.append(f"{d['filename']}: mention '{m['name']}' pattern not found")
    return rows, notes


# --------------------------------------------------------------- new audits
_ABBR_PROTECT = [("D.C.", "D_C_"), ("U.S.", "U_S_"), ("Inc.", "Inc_"), ("No.", "No_")]


def sentences(t: str) -> list[str]:
    for a, b in _ABBR_PROTECT:
        t = t.replace(a, b)
    out = re.split(r"(?<=[.;])\s+(?=[A-Z(])", t)
    res = []
    for s_ in out:
        for a, b in _ABBR_PROTECT:
            s_ = s_.replace(b, a)
        res.append(s_.strip())
    return res


GOV_NOTE = re.compile(r"government|Community Partnership|District of Columbia|\bD\.C\.|HUD\b|Housing and Urban|"
                      r"FEMA|Emergency Food|Victim Services|Department of|OVSJG|\bDHS\b|federal", re.I)
GOV_CTX = re.compile(r"grant|contract|award|revenue|receivable|funded|funding|reimburs", re.I)
GOV_EXCL = re.compile(r"Government Auditing Standards|OMB Circular|Uniform Guidance|Accounting Standards|"
                      r"incorporated in|Internal Revenue|income tax|Title 2 U\.S\.|Code of Federal Regulations|"
                      r"de minimis|indirect cost rate|auditor|our audit|we (?:have )?(?:audited|performed)|following table", re.I)


def extract_new_audits(docs: list[dict], q: dict) -> tuple[list[dict], list[dict], list[str]]:
    """SOA/SFP lines via the Phase 1 statement parser (page/column spec in web_queries.yaml),
    government-grant note sentences (statement=NOTE), and SEFA rows (Phase 1 SEFA logic)."""
    import pdfplumber
    m02 = ex02()
    cfg = calvary_cfg_docs(q)
    fin, sefa, notes = [], [], []
    cls = {"W": m02.W, "R": m02.R, "T": m02.T, "NA": m02.NA}
    for d in docs:
        c = cfg.get(d["filename"])
        if not c or not c.get("audit") or not d.get("raw_path") or not d.get("source_id"):
            continue
        a, p, fy = c["audit"], ROOT / d["raw_path"], c["fiscal_year"]
        for page, st, cols in a.get("statements", []):
            # "(Note 3)" references would be read as amounts by the Phase 1 parser; strip them first
            orig = m02.layout_page
            m02.layout_page = lambda pdf, pg, _o=orig: re.sub(r"\((?:Notes?|NOTES?)\s+[\dA-Z]+(?:\s*(?:,|and|&)\s*[\dA-Z]+)*\)",
                                                              "", _o(pdf, pg))
            try:
                got, warn = m02.parse_statement(p, page, st, [(y, cls[k], pr) for y, k, pr in cols])
            finally:
                m02.layout_page = orig
            notes += [w.replace(p.name, d["filename"]) for w in warn]
            for r in got:
                r.update(source_id=d["source_id"], document=d["filename"])
            fin += got
        # SEFA (same parse as scripts/02_extract_inputs.extract_sefa)
        for page in a.get("sefa_pages", []):
            agency = passthru = ""
            lay = m02.layout_page(p, page)
            n0 = len(sefa)
            for raw in lay.splitlines():
                s_ = re.sub(r"\s+", " ", raw).strip()
                if not s_:
                    continue
                if re.match(r"^(U\.S\.|United States) Department", s_) or re.match(r"^U\.S\. ", s_):
                    agency, passthru = s_, ""
                    continue
                m = re.match(r"^Pass-?through from (.+)$", s_, re.I)
                if m:
                    passthru = m.group(1).strip()
                    continue
                if re.match(r"^(Total|TOTAL)", s_):
                    continue
                m = re.match(r"^(.+?)\s+(\d{2}\.\d{3})\s*(.*?)\s*\$?\s*([\d,]+)$", s_)
                if m and agency:
                    prog, aln, rest, amt = m.groups()
                    sefa.append(dict(source_id=d["source_id"], document=d["filename"], page=page, fiscal_year=fy,
                                     federal_agency=agency, pass_through_entity=passthru,
                                     program_name=prog.strip(), assistance_listing=aln,
                                     pass_through_award_id=rest.strip(), amount=m02.fmt(m02.to_num(amt)),
                                     amount_to_subrecipients="",
                                     notes="no subrecipient column in SEFA; pass-through as printed"))
            tot = re.search(r"TOTAL EXPENDITURES OF FEDERAL AWARDS\s+\$?\s*([\d,]+)", lay)
            ssum = sum(float(r["amount"]) for r in sefa[n0:])
            notes.append(f"{d['filename']}: SEFA p{page} {len(sefa) - n0} programs sum {ssum:,.0f} vs printed "
                         f"total {tot.group(1) if tot else '?'}")
        if not a.get("sefa_pages"):
            notes.append(f"{d['filename']}: no SEFA in the PDF")
        # government-grant note sentences
        note_pages = a.get("note_pages")
        with pdfplumber.open(p) as doc:
            for i, pg in enumerate(doc.pages, 1):
                if note_pages and not (note_pages[0] <= i <= note_pages[1]):
                    continue
                t = re.sub(r"\s+", " ", pg.extract_text() or "")
                for sent in sentences(t):
                    if GOV_NOTE.search(sent) and GOV_CTX.search(sent) and not GOV_EXCL.search(sent) \
                            and 40 < len(sent) < 900:
                        amts = re.findall(r"\$\s?([\d,]{4,}(?:\.\d+)?)", sent)
                        fin.append(dict(source_id=d["source_id"], document=d["filename"], page=i, fiscal_year=fy,
                                        tax_year=fy - 1, statement="NOTE", line_item=sent[:500],
                                        line_item_std="note_government_grants", net_asset_class="n/a",
                                        amount=amts[0].replace(",", "") if len(amts) == 1 else "",
                                        is_prior_year_comparative=False,
                                        notes=("amounts in sentence: " + "; ".join(amts)) if len(amts) > 1
                                        else "government-grant note sentence (as printed)"))
    return fin, sefa, notes


def write_csv(p: Path, fields: list[str], rows: list[dict]):
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


FUNDER_FIELDS = ["source_id", "document", "page", "report_year", "fiscal_year", "funder_name_raw", "funder_name_norm",
                 "org_type_guess", "gift_band_raw", "band_min", "band_max", "in_kind_flag", "truncated",
                 "section_heading", "notes", "amount_kind_hint", "cumulative_hint", "purpose_hint", "quote"]
SEFA_FIELDS = ["source_id", "document", "page", "fiscal_year", "federal_agency", "pass_through_entity",
               "program_name", "assistance_listing", "pass_through_award_id", "amount", "amount_to_subrecipients",
               "notes"]
FIN_FIELDS = ["source_id", "document", "page", "fiscal_year", "tax_year", "statement", "line_item", "line_item_std",
              "net_asset_class", "amount", "is_prior_year_comparative", "notes"]
DOC_FIELDS = ["url", "filename", "doc_type", "fiscal_year", "linked_from_financials", "link_text", "upload_date",
              "in_inputs", "remote_bytes", "local_bytes", "raw_path", "sha256", "source_id", "status"]


def main():
    refresh = "--refresh" in sys.argv
    q = load_queries()
    wf = WebFetcher(refresh=refresh)
    docs = step_site(wf)
    hits, off, rejected = step_offsite_search(wf, q, docs)
    docs += off
    cfg = calvary_cfg_docs(q)
    for d in docs:
        if str(d["status"]).startswith("duplicate_of"):
            d["source_id"] = ""
            continue
        if d.get("source_id") and d.get("raw_path"):
            c = cfg.get(d["filename"], {})
            d["source_id"] = c.get("source_id", d["source_id"])
            if c.get("fiscal_year"):
                d["fiscal_year"] = c["fiscal_year"]
            register_source(d["source_id"], f"Calvary {d['doc_type']}: {d['filename']}", d["url"],
                            "Calvary Women's Services, Inc.", "Public PDF on calvaryservices.org" if
                            "calvaryservices.org" in d["url"] else "Public PDF",
                            f"{c.get('note', '')} raw: {d['raw_path']}; status {d['status']}".strip(),
                            retrieved_date=RETRIEVED)
    write_csv(INTERIM / "web_calvary_docs.csv", DOC_FIELDS, docs)
    posts = step_posts(wf, q)
    pdir = INTERIM / "web_text"
    pdir.mkdir(parents=True, exist_ok=True)
    for p in posts:
        if p["text"]:
            (pdir / f"calvary_{p['id']}.txt").write_text(p["text"], encoding="utf-8")

    sup = [r for r in wf.rows.values() if r["key"] == f"http:{SUPPORT_URL}"]
    funders = parse_support_page(ROOT / sup[0]["raw_path"]) if sup else []
    if sup:
        (pdir / "calvary_support_page.txt").write_text(html_text((ROOT / sup[0]["raw_path"]).read_bytes()),
                                                       encoding="utf-8")
    ar_f, band_rows, ar_notes = extract_ar_donors(docs, q)
    nl_f, nl_notes = extract_named_lists(docs, q)
    po_f, po_notes = extract_post_mentions(posts, q)
    ar_notes += nl_notes + po_notes
    nl_f += po_f
    funders += ar_f + nl_f
    write_csv(INTERIM / "web_calvary_funders.csv", FUNDER_FIELDS, funders)
    write_csv(INTERIM / "web_calvary_donor_band_counts.csv",
              ["source_id", "document", "report_year", "gift_band_raw", "band_min", "band_max", "individual_count"],
              band_rows)
    fin, sefa, a_notes = extract_new_audits(docs, q)
    write_csv(INTERIM / "web_new_audit_financials.csv", FIN_FIELDS, fin)
    write_csv(INTERIM / "web_new_audit_sefa.csv", SEFA_FIELDS, sefa)

    # compare live support page with the Phase 1 PDF extraction
    p1 = []
    with open(RAW / "inputs_extracted" / "funder_mentions.csv", newline="", encoding="utf-8") as f:
        p1 = [r for r in csv.DictReader(f) if r["source_id"] == "input_corp_found_support_2023"]
    live = [r for r in funders if r["source_id"] == "web_calvary_corp_found_support"]
    live_n = {r["funder_name_norm"] for r in live}
    trunc = [r for r in p1 if r["truncated"] == "True"]
    fixed = []
    for r in trunc:
        full = [x["funder_name_raw"] for x in live if x["funder_name_norm"].startswith(r["funder_name_norm"][:8])]
        fixed.append(f"{r['funder_name_raw']} -> {full[0] if full else '?'}")
    p1_n = {r["funder_name_norm"] for r in p1}
    only_live = sorted(r["funder_name_raw"] for r in live if r["funder_name_norm"] not in p1_n)

    new_docs = [d for d in docs if d["status"] not in ("already_in_inputs", "skipped_not_relevant")
                and not str(d["status"]).startswith("duplicate_of_input")]
    lines = [
        f"- support page: {len(live)} organizations ({sum(1 for r in live if r['in_kind_flag'])} flagged in-kind); "
        f"Phase 1 PDF had {len(p1)} ({len(trunc)} truncated). Names absent from the PDF parse: {len(only_live)}",
        f"- truncated names recovered: {'; '.join(fixed)}",
        f"- PDFs seen: {len(docs)} (financials page links + WP media library + off-site search); kept as new: "
        f"{len(new_docs)}: " + "; ".join(f"{d['filename']} [{d['doc_type']}, {d['status']}]" for d in new_docs),
        f"- off-site search hits: {len(hits)} results; Calvary PDFs kept: {len(off)}; rejected: "
        + ("; ".join(rejected) or "none"),
        f"- annual-report donors: {len(ar_f)} org rows; named lists/mentions {len(nl_f)} rows; individual "
        f"band-count rows {len(band_rows)}; "
        + "; ".join(ar_notes),
        f"- new audits: {len(fin)} financial/note rows, {len(sefa)} SEFA rows; " + "; ".join(a_notes[:12]),
        f"- {wf.summary()}",
    ]
    log("43_web_calvary", "\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
