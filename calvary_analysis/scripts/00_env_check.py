"""Environment check: every clean table loads, row counts match the data quality report,
reviewer-guide self-checks pass, packages are importable. Writes a section to analysis_log.md."""
import importlib
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import CLEAN, DATA, CALVARY, DWC, load, log  # noqa: E402

EXPECTED = {}
txt = (DATA / "reports" / "data_quality.md").read_text()
for m in re.finditer(r"^\| (\w+) \| (\d+) \|$", txt, re.M):
    EXPECTED.setdefault(m.group(1), int(m.group(2)))   # entity_aliases appears twice: 231,647 parsed rows (first) vs 231,678 physical lines

lines = []
ok = True
tables = sorted(p.stem for p in CLEAN.glob("*.csv"))
for t in tables:
    first = pd.read_csv(CLEAN / f"{t}.csv", nrows=0).columns[0]
    n = len(pd.read_csv(CLEAN / f"{t}.csv", usecols=[first], low_memory=False))   # pandas count: quoted newlines break wc -l
    exp = EXPECTED.get(t)
    flag = "" if exp is None or exp == n else f"  MISMATCH expected {exp}"
    if flag:
        ok = False
    lines.append(f"{t}: {n:,} rows{flag}")

fin = load("fact_org_financials", usecols=["ein", "fiscal_year", "preferred", "total_revenue"])
checks = {
    "Calvary FY25 revenue 4,967,995": int(fin[(fin.ein == CALVARY) & (fin.fiscal_year == 2025) & (fin.preferred == 1)].total_revenue.iloc[0]) == 4967995,
    "DWC FY2024 revenue 34,403,997": int(fin[(fin.ein == DWC) & (fin.fiscal_year == 2024) & (fin.preferred == 1)].total_revenue.iloc[0]) == 34403997,
}
g = load("fact_gov_awards", usecols=["recipient_ein", "source_type", "fiscal_year", "program_name", "amount"])
checks["FY23 audit SEFA sums to 937,999"] = int(g[(g.recipient_ein == CALVARY) & (g.source_type == "audit_sefa") & (g.fiscal_year == 2023)].amount.sum()) == 937999
ov = g[(g.recipient_ein == CALVARY) & (g.source_type == "dc_ovsjg") & (g.fiscal_year == 2026)].set_index("program_name").amount
checks["OVSJG FY2026 New Foundations 543,056 / Reach Up 507,595"] = sorted(ov.astype(int).tolist()) == [507595, 543056]
geo = pd.read_csv(CLEAN / "dim_geo.csv", usecols=["geo_level", "ward", "poverty_rate"])
checks["Ward 8 poverty 0.306"] = round(float(geo[(geo.geo_level == "ward") & (geo.ward.astype(str).str.startswith("8"))].poverty_rate.iloc[0]), 3) == 0.306
gr = load("fact_grants", usecols=["funder_ein", "recipient_ein", "tax_year", "amount"])
checks["Cafritz TY2024 grant 170,000"] = int(gr[(gr.funder_ein == "526036989") & (gr.recipient_ein == CALVARY) & (gr.tax_year == 2024)].amount.sum()) == 170000
for k, v in checks.items():
    lines.append(f"self-check {'PASS' if v else 'FAIL'}: {k}")
    ok &= v

for pkg in ["pandas", "numpy", "matplotlib", "networkx", "pptx", "yaml", "shapely"]:
    try:
        m = importlib.import_module(pkg)
        lines.append(f"{pkg} {getattr(m, '__version__', '')}")
    except Exception as e:  # noqa: BLE001
        lines.append(f"{pkg} MISSING ({e})"); ok = False

lines.append(f"raw/ present: {(DATA / 'raw').exists()}")
lines.append(f"RESULT: {'OK' if ok else 'PROBLEMS'}")
log("00_env_check", lines)
print("\n".join(lines))
sys.exit(0 if ok else 1)
