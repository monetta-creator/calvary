"""Shared helpers: paths, EIN/name normalization, raw writer, source registry, build log, HTTP."""
from __future__ import annotations

import csv
import contextlib
import datetime as dt
import fcntl
import hashlib
import json
import os
import re
import threading
import time
import unicodedata
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

ROOT = Path(__file__).resolve().parents[2]
INPUTS = ROOT / "inputs"
RAW = ROOT / "raw"
CLEAN = ROOT / "clean"
SOURCES = ROOT / "sources"
REPORTS = ROOT / "reports"
LOGS = ROOT / "logs"
CONFIG = ROOT / "config"

REGISTRY = SOURCES / "source_registry.csv"
REGISTRY_FIELDS = [
    "source_id", "name", "url_or_file", "publisher", "retrieved_date",
    "license_or_citation", "notes",
]
BUILD_LOG = LOGS / "build_log.md"
USER_AGENT = "calvary-funding-research/0.1 (pro bono nonprofit research)"

_lock = threading.Lock()


@contextlib.contextmanager
def _file_lock(name: str):
    """Cross-process lock so parallel scripts can safely append to shared files."""
    LOGS.mkdir(parents=True, exist_ok=True)
    with _lock, open(LOGS / f".{name}.lock", "w") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)


# ---------- time ----------
def today() -> str:
    return dt.date.today().isoformat()


def stamp() -> str:
    return dt.datetime.now().strftime("%Y%m%dT%H%M%S")


# ---------- keys ----------
def env_key(name: str) -> str | None:
    """Read an API key from the environment. Never log or persist the value."""
    v = os.environ.get(name, "").strip()
    return v or None


# ---------- normalization ----------
def norm_ein(x) -> str | None:
    if x is None:
        return None
    s = re.sub(r"\D", "", str(x))
    if not s or len(s) > 9:
        return None
    return s.zfill(9)


_LEGAL = r"\b(inc|incorporated|corp|corporation|co|company|llc|llp|ltd|lp|pc|pllc|the|of|and|a)\b"
_ABBR = {
    "fdn": "foundation", "fndtn": "foundation", "found": "foundation",
    "assn": "association", "assoc": "association", "ctr": "center", "cntr": "center",
    "svcs": "services", "svc": "services", "serv": "services", "intl": "international",
    "natl": "national", "comm": "community", "cmty": "community", "univ": "university",
    "dc": "dc", "wash": "washington", "st": "saint", "mt": "mount", "chrch": "church",
}


def norm_name(name: str | None) -> str:
    """Lowercase, ascii-fold, expand common abbreviations, drop legal suffixes and punctuation."""
    if not name:
        return ""
    s = unicodedata.normalize("NFKD", str(name)).encode("ascii", "ignore").decode()
    s = s.lower().replace("&", " and ").replace("'", "")
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    s = " ".join(_ABBR.get(t, t) for t in s.split())
    s = re.sub(_LEGAL, " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    toks = s.split()
    half = len(toks) // 2
    if half >= 2 and len(toks) % 2 == 0 and toks[:half] == toks[half:]:
        # "X Y X Y" -> "X Y": filings that print the full name in both name lines. Single words are left alone
        # ("Arm & Arm", "Johnson & Johnson", "Walla Walla" are real names).
        s = " ".join(toks[:half])
    return s


# ---------- raw writer ----------
def raw_path(source: str, desc: str, ext: str) -> Path:
    d = RAW / source
    d.mkdir(parents=True, exist_ok=True)
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", desc)[:120]
    return d / f"{stamp()}_{safe}.{ext.lstrip('.')}"


def save_raw(source: str, desc: str, content, ext: str = "json") -> Path:
    """Write an untouched response to raw/{source}/. Bytes are written as-is; dict/list as JSON."""
    p = raw_path(source, desc, ext)
    if isinstance(content, (bytes, bytearray)):
        p.write_bytes(content)
    elif isinstance(content, (dict, list)):
        p.write_text(json.dumps(content, ensure_ascii=False, indent=1), encoding="utf-8")
    else:
        p.write_text(str(content), encoding="utf-8")
    return p


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(p: Path) -> str:
    """Project-relative path string for anything written to outputs."""
    return str(Path(p).resolve().relative_to(ROOT))


# ---------- source registry ----------
def register_source(source_id: str, name: str, url_or_file: str, publisher: str,
                    license_or_citation: str = "", notes: str = "",
                    retrieved_date: str | None = None) -> str:
    """Upsert a source row keyed by source_id. Returns source_id."""
    with _file_lock("registry"):
        rows = []
        if REGISTRY.exists():
            with open(REGISTRY, newline="", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
        row = {
            "source_id": source_id, "name": name, "url_or_file": url_or_file,
            "publisher": publisher, "retrieved_date": retrieved_date or today(),
            "license_or_citation": license_or_citation, "notes": notes,
        }
        rows = [r for r in rows if r["source_id"] != source_id] + [row]
        rows.sort(key=lambda r: r["source_id"])
        with open(REGISTRY, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=REGISTRY_FIELDS)
            w.writeheader()
            w.writerows(rows)
    return source_id


# ---------- build log ----------
def log(section: str, text: str) -> None:
    """Append a timestamped entry to logs/build_log.md."""
    with _file_lock("buildlog"):
        BUILD_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(BUILD_LOG, "a", encoding="utf-8") as f:
            f.write(f"\n### {dt.datetime.now().strftime('%Y-%m-%d %H:%M')} — {section}\n{text.rstrip()}\n")


# ---------- HTTP ----------
class RateLimiter:
    """Simple min-interval limiter, thread-safe."""

    def __init__(self, per_sec: float):
        self.interval = 1.0 / per_sec
        self._next = 0.0
        self._l = threading.Lock()

    def wait(self):
        with self._l:
            now = time.monotonic()
            if now < self._next:
                time.sleep(self._next - now)
            self._next = max(now, self._next) + self.interval


def session(retries: int = 5, backoff: float = 1.5) -> requests.Session:
    s = requests.Session()
    r = Retry(total=retries, backoff_factor=backoff,
              status_forcelist=(429, 500, 502, 503, 504),
              allowed_methods=("GET", "POST", "HEAD"))
    s.mount("https://", HTTPAdapter(max_retries=r, pool_maxsize=16))
    s.mount("http://", HTTPAdapter(max_retries=r, pool_maxsize=16))
    s.headers["User-Agent"] = USER_AGENT
    return s


def append_md(filename: str, heading: str, text: str) -> None:
    """Locked append to a root-level shared markdown file (notes_for_analysis.md, open_questions.md)."""
    assert filename in ("notes_for_analysis.md", "open_questions.md")
    if os.environ.get("CALVARY_NO_NOTES"):   # rebuild mode: don't re-append observations already recorded
        return
    with _file_lock("mdappend"):
        with open(ROOT / filename, "a", encoding="utf-8") as f:
            f.write(f"\n## {heading}\n{text.rstrip()}\n")


def latest_raw(source: str, suffix: str) -> Path | None:
    """Newest raw/{source}/{stamp}_{suffix} file (timestamps sort lexicographically), or None."""
    hits = sorted((RAW / source).glob(f"*_{suffix}"))
    return hits[-1] if hits else None


INTERIM = ROOT / "interim"   # regenerable intermediate files (not portable, not final)
