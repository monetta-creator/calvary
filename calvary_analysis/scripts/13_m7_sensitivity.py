"""M7 sensitivity: how Tier 1-2 membership and ranks move when each weight shifts by ±0.05 (renormalized)
and when the tier cutoffs move by ±0.05. Writes chart_data/m7_05_sensitivity.csv."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import ANALYSIS, log, save_chart_data  # noqa: E402

S = "13_m7_sensitivity"
CFG = yaml.safe_load(open(ANALYSIS / "config" / "scoring_weights.yaml"))
W0 = CFG["weights"]; T = CFG["tiers"]
pipe = pd.read_csv(ANALYSIS / "recommendations" / "funder_pipeline.csv", dtype={"funder_id": str})
inst = pipe[pipe.s_mission_fit.notna()].copy()
dims = list(W0.keys())
base_score = sum(W0[k] * inst[f"s_{k}"] for k in dims)
base_rank = base_score.rank(ascending=False, method="first")
base_t12 = set(inst.funder_id[base_score >= T["tier2_min_score"]])
rows = []
for k in dims:
    for d in (-0.05, 0.05):
        w = dict(W0); w[k] = max(0.0, w[k] + d); s = sum(w.values()); w = {kk: v / s for kk, v in w.items()}
        sc = sum(w[kk] * inst[f"s_{kk}"] for kk in dims)
        rk = sc.rank(ascending=False, method="first")
        t12 = set(inst.funder_id[sc >= T["tier2_min_score"]])
        top10_base = set(inst.funder_id[base_rank <= 10]); top10 = set(inst.funder_id[rk <= 10])
        rows.append({"change": f"{k} {d:+.2f} (renormalized)", "mean_abs_rank_shift_top30": float((rk - base_rank)[base_rank <= 30].abs().mean()),
                     "top10_overlap": len(top10 & top10_base), "tier12_added": len(t12 - base_t12), "tier12_dropped": len(base_t12 - t12)})
for d in (-0.05, 0.05):
    t12 = set(inst.funder_id[base_score >= T["tier2_min_score"] + d])
    rows.append({"change": f"tier2 cutoff {d:+.2f}", "mean_abs_rank_shift_top30": 0.0, "top10_overlap": 10, "tier12_added": len(t12 - base_t12), "tier12_dropped": len(base_t12 - t12)})
sens = pd.DataFrame(rows)
save_chart_data(sens, "m7_05_sensitivity", "Pipeline sensitivity: rank shifts and Tier 1-2 membership changes under ±0.05 weight and cutoff changes", [], [], S,
                "institutional rows only; government, corporate and federal rows carry fixed analyst scores")
print(sens.round(2).to_string())
log(S, [f"sensitivity: max mean rank shift in top 30 = {sens.mean_abs_rank_shift_top30.max():.2f}; min top-10 overlap = {sens.top10_overlap.min()}"])
