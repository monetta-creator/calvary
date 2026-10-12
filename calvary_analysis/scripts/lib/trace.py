"""Trace test: every chart referenced in readouts, storylines, reports and the insight register has chart data;
every chart-data CSV's source_ids exist in the source registry; every PNG has a manifest row.
Run: python scripts/lib/trace.py  (exit 1 on any failure)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.common import ANALYSIS, CHART_DATA, CHARTS, MANIFEST, REGISTER, registry_ids  # noqa: E402

PAT = re.compile(r"\bm(?:\d{1,2})_\d{2}[a-z]?_[a-z0-9_]+")


def main() -> int:
    problems: list[str] = []
    man = pd.read_csv(MANIFEST, dtype=str)
    reg = registry_ids()
    have_csv = {p.stem for p in CHART_DATA.glob("m*.csv")}
    have_png = {p.stem for p in CHARTS.glob("*.png")}
    # 1. manifest rows <-> csv files
    for cid in man.chart_id:
        if cid not in have_csv:
            problems.append(f"manifest row without CSV: {cid}")
    for cid in have_csv - set(man.chart_id):
        problems.append(f"CSV without manifest row: {cid}")
    # 2. source_ids in registry
    for _, r in man.iterrows():
        for sid in str(r.source_ids).split(";"):
            if sid and sid != "nan" and sid not in reg:
                problems.append(f"{r.chart_id}: source_id not in registry: {sid}")
    # 3. PNGs: each has a CSV with the same id, or an explicit mapping in config/png_data_map.csv
    pmap = pd.read_csv(ANALYSIS / "config" / "png_data_map.csv", dtype=str).fillna("")
    mapped = {r.png: [x for x in r.chart_data_ids.split(";") if x] for _, r in pmap.iterrows()}
    for png in have_png:
        if png in have_csv:
            continue
        ids = mapped.get(png)
        if not ids:
            problems.append(f"PNG without chart data: {png} (add a row to config/png_data_map.csv)")
        else:
            for cid in ids:
                if cid not in have_csv:
                    problems.append(f"png_data_map: {png} -> missing CSV {cid}")
    # 4. references in markdown and the register
    refs: set[str] = set()
    for folder in ["modules", "storylines", "reports", "recommendations", "checkpoints"]:
        for p in (ANALYSIS / folder).glob("*.md"):
            refs |= set(PAT.findall(p.read_text()))
    if REGISTER.exists():
        reg_df = pd.read_csv(REGISTER, dtype=str)
        for _, r in reg_df.iterrows():
            for cid in str(r.chart_ids).split(";"):
                if cid and cid != "nan" and cid not in have_csv and cid not in have_png:
                    problems.append(f"register {r.insight_id}: unknown chart {cid}")
    for cid in sorted(refs):
        if cid not in have_csv and cid not in have_png and cid.replace("_summary_numbers", "") not in have_csv:
            problems.append(f"referenced in markdown but missing: {cid}")
    print(f"charts: {len(have_png)} PNG, {len(have_csv)} CSV, {len(man)} manifest rows; references checked: {len(refs)}")
    for p in problems:
        print("PROBLEM:", p)
    print("TRACE", "OK" if not problems else f"FAILED ({len(problems)})")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
