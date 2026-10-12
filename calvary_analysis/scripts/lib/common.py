"""Shared helpers for the Prompt 2 analysis scripts.

Every script reads only from ../calvary_funding_data/clean/ and writes to calvary_analysis/.
Paths are resolved relative to this file, so the project can move between machines.
"""
from __future__ import annotations

import csv
import datetime as dt
import fcntl
import os
from pathlib import Path

import pandas as pd

ANALYSIS = Path(__file__).resolve().parents[2]          # calvary_analysis/
PROJECT = ANALYSIS.parent                                # project root
DATA = PROJECT / "calvary_funding_data"
CLEAN = DATA / "clean"
SOURCES = DATA / "sources"
CHART_DATA = ANALYSIS / "chart_data"
CHARTS = ANALYSIS / "charts"
MODULES = ANALYSIS / "modules"
REGISTER = ANALYSIS / "insight_register.csv"
LOG = ANALYSIS / "analysis_log.md"
MANIFEST = CHART_DATA / "_manifest.csv"

CALVARY = "521307706"
DWC = "311597223"
SHEWORKS = "882046704"          # California Black Women's Collective Empowerment Institute (runs SheWorks)
NAMED = [DWC, SHEWORKS]
AS_OF = "2026-10-10"            # retrieval date of the Prompt 1 build

EIN_COLS = {"ein", "funder_ein", "recipient_ein", "pass_through_ein", "org_a_ein", "org_b_ein",
            "ein_a", "ein_b", "funder_id", "person_id", "person_id_a", "person_id_b", "recipient_uei"}


GRANT_EXCLUSIONS = ANALYSIS / "config" / "grant_exclusions.csv"   # mis-attributed grant rows, dropped on every load


def load(table: str, usecols: list[str] | None = None, **kw) -> pd.DataFrame:
    """Read a clean table with EIN-like columns kept as strings. fact_grants rows listed in config/grant_exclusions.csv
    (e.g. grants to a namesake organization in another city) are dropped here, so every module agrees."""
    path = CLEAN / f"{table}.csv"
    excl = table == "fact_grants" and GRANT_EXCLUSIONS.exists()
    cols = usecols if not (excl and usecols is not None and "grant_id" not in usecols) else list(usecols) + ["grant_id"]
    header = pd.read_csv(path, nrows=0).columns if cols is None else cols
    dtype = {c: str for c in header if c in EIN_COLS}
    df = pd.read_csv(path, usecols=cols, dtype=dtype, low_memory=False, **kw)
    if excl:
        df = df[~df.grant_id.isin(set(pd.read_csv(GRANT_EXCLUSIONS, dtype=str).grant_id))]
        if cols is not usecols:
            df = df.drop(columns="grant_id")
    return df


def universe(name: str) -> list[str]:
    um = load("dim_universe_membership", usecols=["universe", "ein"])
    return sorted(um.loc[um.universe == name, "ein"].unique().tolist())


def core_peers() -> pd.DataFrame:
    """The 18 provisional core peers with tier and name, in config order."""
    df = pd.read_csv(DATA / "config" / "core_peers.csv", dtype={"ein": str})
    return df


def peer_set() -> pd.DataFrame:
    """Calvary + 18 core peers + 2 named comparators, with short labels and a group column."""
    cp = core_peers()[["ein", "name", "tier"]].assign(group="core_peer")
    nc = pd.read_csv(DATA / "config" / "named_comparators.csv", dtype={"ein": str})[["ein", "name"]]
    nc = nc.assign(tier="named_comparator", group="named_comparator")
    cal = pd.DataFrame([{"ein": CALVARY, "name": "Calvary Women's Services", "tier": "subject", "group": "calvary"}])
    df = pd.concat([cal, cp, nc], ignore_index=True)
    df["short"] = df["name"].map(SHORT_NAMES).fillna(df["name"])
    return df


SHORT_NAMES = {
    "Calvary Women's Services": "Calvary",
    "N Street Village": "N Street Village",
    "House of Ruth (DC)": "House of Ruth DC",
    "Open Arms Housing": "Open Arms Housing",
    "New Endeavors by Women": "New Endeavors by Women",
    "District Alliance for Safe Housing (DASH)": "DASH",
    "My Sister's Place": "My Sister's Place",
    "DC SAFE": "DC SAFE",
    "Samaritan Inns": "Samaritan Inns",
    "Christ House": "Christ House",
    "Everyone Home DC": "Everyone Home DC",
    "Coalition for the Homeless": "Coalition for the Homeless",
    "Thrive DC": "Thrive DC",
    "Miriam's Kitchen": "Miriam's Kitchen",
    "Community of Hope": "Community of Hope",
    "Covenant House Washington DC": "Covenant House DC",
    "Doorways for Women and Families": "Doorways (VA)",
    "House of Ruth Maryland": "House of Ruth MD",
    "Heartly House": "Heartly House (MD)",
    "Downtown Women's Center (DWC)": "DWC (Los Angeles)",
    "California Black Women's Collective Empowerment Institute (runs SheWorks)": "CBWC Inst. / SheWorks (LA)",
}

# Display names for the most connected funders (legal names in dim_funder); used on the m6_03 network and the web explorer.
FUNDER_SHORT = {"110303001": "Fidelity Charitable", "237343119": "Greater Washington Community Fdn", "810739440": "Benevity",
                "311640316": "Schwab Charitable", "526036989": "Cafritz Foundation", "232888152": "Vanguard Charitable",
                "237825575": "National Philanthropic Trust", "530234290": "United Way NCA", "460942102": "Blackbaud Giving Fund",
                "521283255": "Venable Foundation", "200721133": "Bank of America Fdn", "521435573": "Abell Foundation"}


def deflators() -> pd.Series:
    """CPI-U US deflator to 2024 dollars, indexed by calendar year (fiscal-year-end year)."""
    p = pd.read_csv(CLEAN / "dim_period.csv")
    return p.set_index("year")["deflator_to_2024_us"]


def registry_ids() -> set[str]:
    ids = set(pd.read_csv(SOURCES / "source_registry.csv", usecols=["source_id"])["source_id"])
    ext = ANALYSIS / "sources" / "source_registry_extension.csv"
    if ext.exists():
        ids |= set(pd.read_csv(ext, usecols=["source_id"])["source_id"])
    return ids


# ---------------------------------------------------------------- chart data + manifest

def save_chart_data(df: pd.DataFrame, chart_id: str, title: str, source_tables: list[str],
                    source_ids: list[str], script: str, notes: str = "") -> Path:
    """Write chart_data/<chart_id>.csv with provenance columns, and register it in _manifest.csv."""
    CHART_DATA.mkdir(exist_ok=True)
    out = df.copy()
    out["source_tables"] = ";".join(source_tables)
    out["source_ids"] = ";".join(sorted(set(source_ids)))
    path = CHART_DATA / f"{chart_id}.csv"
    out.to_csv(path, index=False)
    row = {"chart_id": chart_id, "title": title, "source_tables": ";".join(source_tables),
           "source_ids": ";".join(sorted(set(source_ids))), "script": script, "rows": len(out),
           "notes": notes, "written": dt.datetime.now().strftime("%Y-%m-%d %H:%M")}
    _upsert_csv(MANIFEST, row, key="chart_id")
    return path


def _upsert_csv(path: Path, row: dict, key: str) -> None:
    """Replace the row with the same key or append; file-locked so parallel scripts don't clobber."""
    path.parent.mkdir(exist_ok=True)
    lock = path.with_suffix(".lock")
    with open(lock, "w") as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        rows = []
        if path.exists():
            with open(path, newline="") as f:
                rows = [r for r in csv.DictReader(f) if r.get(key) != row[key]]
        rows.append(row)
        fields = list(row.keys())
        for r in rows:
            for k in r:
                if k not in fields:
                    fields.append(k)
        rows.sort(key=lambda r: r[key])
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
        fcntl.flock(lf, fcntl.LOCK_UN)


# ---------------------------------------------------------------- insight register

REGISTER_COLS = ["insight_id", "module", "finding", "evidence_summary", "chart_ids", "source_tables",
                 "magnitude", "confidence", "implication_for_calvary", "audience", "status"]


def register_insight(insight_id: str, module: str, finding: str, evidence_summary: str, chart_ids: list[str],
                     source_tables: list[str], magnitude: str, confidence: str, implication: str,
                     audience: str = "both", status: str = "draft") -> None:
    assert confidence in {"high", "medium", "low"}, confidence
    assert audience in {"leadership", "consulting", "both"}, audience
    row = {"insight_id": insight_id, "module": module, "finding": finding, "evidence_summary": evidence_summary,
           "chart_ids": ";".join(chart_ids), "source_tables": ";".join(source_tables), "magnitude": magnitude,
           "confidence": confidence, "implication_for_calvary": implication, "audience": audience, "status": status}
    # A rerun keeps a reviewed status ("verified") when the finding itself has not changed; a changed finding goes
    # back to "draft" so it is re-checked.
    if REGISTER.exists():
        old = pd.read_csv(REGISTER, dtype=str).fillna("").set_index("insight_id")
        if insight_id in old.index and status == "draft":
            prev = old.loc[insight_id]
            if all(str(prev[k]) == str(row[k]) for k in ("finding", "evidence_summary", "magnitude")):
                row["status"] = prev["status"] or status
    _upsert_csv(REGISTER, row, key="insight_id")


# ---------------------------------------------------------------- log

def log(script: str, lines: list[str]) -> None:
    """Append a timestamped section to analysis_log.md (file-locked)."""
    lock = LOG.with_suffix(".lock")
    with open(lock, "w") as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        with open(LOG, "a") as f:
            f.write(f"\n### {dt.datetime.now():%Y-%m-%d %H:%M} — {script}\n")
            for ln in lines:
                f.write(f"- {ln}\n")
        fcntl.flock(lf, fcntl.LOCK_UN)


def money(x: float, unit: str = "M", nd: int = 2) -> str:
    if pd.isna(x):
        return "n/a"
    if unit == "M":
        return f"${x/1e6:,.{nd}f}M"
    if unit == "K":
        return f"${x/1e3:,.0f}K"
    return f"${x:,.0f}"
