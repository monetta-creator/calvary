"""Approved Phase 3 web pull: guidelines, application process and deadlines for Tier 1 and Tier 2 institutional
funders in the pipeline, via the Tavily search API (key from the environment; never written to disk).
Writes sources/web_tier1_guidelines.csv (raw hits, snippets) and sources/source_registry_extension.csv."""
import datetime as dt
import os
import sys
import time
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import ANALYSIS, log  # noqa: E402

S = "11_web_tier1_guidelines"
key = os.environ.get("TAVILY_API_KEY")
if not key:
    sys.exit("TAVILY_API_KEY not set in the environment")
from tavily import TavilyClient  # noqa: E402
client = TavilyClient(api_key=key)

pipe = pd.read_csv(ANALYSIS / "recommendations" / "funder_pipeline.csv", dtype={"funder_id": str})
sel = pipe[(pipe.tier <= 2) & pipe.funder_type.isin(["private_foundation", "community_foundation", "public_charity_grantmaker", "corporate_foundation", "federated_giving"])
           & ~pipe.track.str.startswith("daf")].sort_values(["tier", "rank"]).head(32)
out_dir = ANALYSIS / "sources"; out_dir.mkdir(exist_ok=True)
today = dt.date.today().isoformat()
rows, reg = [], []
for _, r in sel.iterrows():
    name = str(r.funder_name).title().replace("'S", "'s").replace(" Inc", "")
    q = f"{name} grant guidelines how to apply deadline"
    try:
        res = client.search(query=q, search_depth="basic", max_results=4, include_answer=False)
        hits = res.get("results", [])
    except Exception as e:  # noqa: BLE001
        hits = []; rows.append({"funder_id": r.funder_id, "funder_name": r.funder_name, "tier": r.tier, "query": q, "rank": 0, "url": "", "title": f"ERROR {type(e).__name__}", "snippet": "", "score": None, "retrieved_date": today})
    for i, h in enumerate(hits, 1):
        rows.append({"funder_id": r.funder_id, "funder_name": r.funder_name, "tier": r.tier, "query": q, "rank": i, "url": h.get("url", ""), "title": h.get("title", ""),
                     "snippet": (h.get("content", "") or "")[:700].replace("\n", " "), "score": h.get("score"), "retrieved_date": today})
        if i == 1:
            reg.append({"source_id": f"web_guidelines_{r.funder_id}", "name": f"{name}: grant guidelines (web search)", "url_or_file": h.get("url", ""), "publisher": name,
                        "retrieved_date": today, "license_or_citation": "Web page; cite by URL", "notes": "Tavily search top hit; used for application process and deadline notes in the pipeline"})
    time.sleep(0.4)
hits_df = pd.DataFrame(rows).sort_values(["tier", "funder_name", "rank"])
hits_df.to_csv(out_dir / "web_tier1_guidelines.csv", index=False)
pd.DataFrame(reg).sort_values("source_id").to_csv(out_dir / "source_registry_extension.csv", index=False)
print(hits_df.groupby("funder_name").size().to_string())
log(S, [f"Tavily guideline search for {len(sel)} Tier 1-2 institutional funders; {len(hits_df)} hits; registry extension {len(reg)} rows"])
