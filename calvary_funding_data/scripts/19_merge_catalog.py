"""Phase 2 merge: combine sources/catalog_parts/{area}.csv|.md into sources/api_catalog.csv and .md.

Usage: python scripts/19_merge_catalog.py
Rerun after any probe script refreshes its catalog part.
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import SOURCES, log, today

PARTS = SOURCES / "catalog_parts"
AREAS = ["filings", "federal", "dc_hud", "context"]  # display order
COLS = ["name", "area", "base_url", "auth_required", "auth_env_var", "rate_limit", "key_endpoints",
        "fields_of_interest", "years_covered", "coverage_gaps", "sample_request", "sample_status",
        "probe_date", "feeds_tables", "source_id", "notes"]


def main():
    frames, problems = [], []
    for area in AREAS:
        p = PARTS / f"{area}.csv"
        if not p.exists():
            problems.append(f"missing {p.name}")
            continue
        d = pd.read_csv(p, dtype=str).fillna("")
        if list(d.columns) != COLS:
            problems.append(f"{p.name}: column mismatch {sorted(set(d.columns) ^ set(COLS))}")
            d = d.reindex(columns=COLS, fill_value="")
        frames.append(d)
    cat = pd.concat(frames, ignore_index=True)
    dup = cat[cat.duplicated(["name", "area"], keep=False)]
    if len(dup):
        problems.append(f"duplicate name+area rows: {dup.name.tolist()}")
    cat.to_csv(SOURCES / "api_catalog.csv", index=False, encoding="utf-8")

    # markdown: header, status summary, then each area's narrative part verbatim
    counts = cat.sample_status.value_counts().to_dict()
    lines = [
        "# API and data source catalog", "",
        f"Merged {today()} from `sources/catalog_parts/` by `scripts/19_merge_catalog.py`. "
        f"{len(cat)} sources probed across {len(frames)} areas. Status counts: "
        + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())) + ".", "",
        "Keys are read from environment variables only (names in `auth_env_var`); sample requests show "
        "`$VAR` placeholders, never values.", "",
        "## Status summary", "",
        "| Area | Source | Auth | Status | Years covered |",
        "|---|---|---|---|---|",
    ]
    for r in cat.itertuples():
        yrs = str(r.years_covered).replace("|", "/")[:60]
        lines.append(f"| {r.area} | {r.name} | {r.auth_required} | {r.sample_status} | {yrs} |")
    for area in AREAS:
        p = PARTS / f"{area}.md"
        lines += ["", "---", ""]
        lines.append(p.read_text(encoding="utf-8").strip() if p.exists() else f"## {area}\n\n_Narrative part missing._")
    (SOURCES / "api_catalog.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    msg = f"- api_catalog.csv: {len(cat)} rows; status {counts}"
    if problems:
        msg += "\n- problems: " + "; ".join(problems)
    log("19_merge_catalog", msg)
    print(msg)


if __name__ == "__main__":
    main()
