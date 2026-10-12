"""Phase 4 web pull: core peers' supporter pages / annual reports, DMV foundation grantee lists, and
in-kind evidence pages for the A2 assumption.

Steps (all queries and curated page lists live in config/web_queries.yaml)
  1. Tavily searches: peers (templates x 18 core peers + extras), funders (15 DMV funders), inkind (4 CRM
     funders). Raw responses -> raw/tavily/. Flattened hits -> interim/web_search_hits.csv for review.
  2. Pages: each curated page is fetched by method
       http    direct GET (PDF or HTML) -> raw/web/
       tavily  Tavily extract -> raw/tavily/ (for JS-rendered pages or when GET is blocked)
       auto    GET first; Tavily extract when GET fails or the HTML has < 1,500 chars of visible text
     Derived plain text -> interim/web_text/{page_id}.txt (regenerable from raw).
  3. Register one web_ source per page; write interim/web_pages.csv (page index used by script 45).

Usage:
  [ -f ~/.config/calvary/keys.env ] && set -a && . ~/.config/calvary/keys.env && set +a
  .venv/bin/python scripts/44_web_peers_funders.py [--refresh] [--searches-only]
"""
from __future__ import annotations

import csv
import importlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import INTERIM, RAW, ROOT, log, norm_name, register_source, today  # noqa: E402

W43 = importlib.import_module("43_web_calvary")
RETRIEVED = today()
TEXT_DIR = INTERIM / "web_text"

is_org_name = W43.is_org_name


# ---------------------------------------------------------------- fetching
def page_text(row: dict) -> str:
    """Plain text for a fetched page from its raw file (PDF via pdftotext, HTML via lxml, Tavily JSON)."""
    p = ROOT / row["raw_path"]
    if not p.exists():
        return ""
    if p.suffix == ".pdf":
        return W43.pdf_text(p)
    if p.suffix == ".json" and "tavily" in str(p):
        d = json.loads(p.read_text(encoding="utf-8"))
        return "\n\n".join((r.get("raw_content") or "") for r in d.get("results", []))
    if p.suffix in (".html", ".htm"):
        return W43.html_text(p.read_bytes())
    return p.read_text(encoding="utf-8", errors="replace")


def fetch_page(wf, pg: dict) -> dict:
    url, pid = pg["url"], pg["id"]
    method = pg.get("method", "auto")
    is_pdf = url.lower().split("?")[0].endswith(".pdf") or pg.get("pdf")
    out = dict(page_id=pid, url=url, method_used="", raw_path="", status="", text_chars=0)
    if method in ("http", "auto"):
        g = wf.get(f"page_{pid}", url, ext="pdf" if is_pdf else None)
        ok = g.get("status") == "ok" and g.get("raw_path")
        txt = page_text(g) if ok else ""
        if ok and (method == "http" or is_pdf or len(txt) >= pg.get("min_chars", 1500)):
            out.update(method_used="http", raw_path=g["raw_path"], status="ok", text_chars=len(txt))
            return out
        out.update(status=f"http:{g.get('status')}; chars {len(txt)}")
    if method in ("tavily", "auto"):
        r = wf.extract(f"page_{pid}", url, depth=pg.get("depth", "basic"))
        key = f"extract:{pg.get('depth', 'basic')}:{url}"
        row = wf.rows.get(key, {})
        if r and row.get("raw_path"):
            txt = page_text(row)
            st = "ok" if txt.strip() else "no_content"
            out.update(method_used="tavily", raw_path=row["raw_path"], status=st if not out["status"] else
                       f"{out['status']} -> tavily {st}", text_chars=len(txt))
    return out


def run_searches(wf, q: dict) -> list[dict]:
    hits = []
    tmpl = q.get("peer_query_templates", [])
    for peer in q.get("peers", []):
        searches = list(peer.get("searches", []))
        if not peer.get("skip_templates"):
            for i, t in enumerate(tmpl):
                searches.append(dict(id=f"peer_{peer['id']}_t{i + 1}", query=t["query"].format(**peer),
                                     params=fmt_params(t.get("params", {}), peer)))
        for s in searches:
            resp = wf.search(s["id"], s["query"], **s.get("params", {}))
            hits += flatten(resp, "peer", peer["id"], s["id"])
    for grp in ("funders", "inkind"):
        for ent in q.get(grp, []):
            for s in ent.get("searches", []):
                resp = wf.search(s["id"], s["query"], **s.get("params", {}))
                hits += flatten(resp, grp, ent["id"], s["id"])
    return hits


def fmt_params(v, ent):
    if isinstance(v, str):
        return v.format(**ent)
    if isinstance(v, list):
        return [fmt_params(x, ent) for x in v]
    if isinstance(v, dict):
        return {k: fmt_params(x, ent) for k, x in v.items()}
    return v


def flatten(resp, group, ent, qid):
    if not resp:
        return []
    return [dict(group=group, entity_id=ent, qid=qid, rank=i + 1, url=r.get("url", ""),
                 title=(r.get("title") or "")[:150], score=round(float(r.get("score") or 0), 3),
                 snippet=re.sub(r"\s+", " ", r.get("content") or "")[:300])
            for i, r in enumerate(resp.get("results", []))]


def all_pages(q: dict) -> list[dict]:
    pages = []
    for grp, key in (("peer", "peers"), ("funder", "funders"), ("inkind", "inkind")):
        for ent in q.get(key, []):
            for pg in ent.get("pages", []):
                pages.append(dict(pg, group=grp, entity_id=ent["id"], entity_name=ent["name"],
                                  entity_ein=str(ent.get("ein", "") or "")))
    return pages


def main():
    refresh = "--refresh" in sys.argv
    q = W43.load_queries()
    wf = W43.WebFetcher(refresh=refresh)
    hits = run_searches(wf, q)
    W43.write_csv(INTERIM / "web_search_hits.csv",
                  ["group", "entity_id", "qid", "rank", "url", "title", "score", "snippet"], hits)
    register_source("api_tavily_search", "Tavily Search API (search results and snippets)",
                    "https://api.tavily.com/search", "Tavily", "Tavily API terms of service",
                    "Queries in config/web_queries.yaml; raw responses in raw/tavily/search_*.json",
                    retrieved_date=RETRIEVED)
    if "--searches-only" in sys.argv:
        print(wf.summary(), len(hits), "hits")
        log("44_web_peers_funders (searches only)", f"- hits {len(hits)}\n- {wf.summary()}")
        return
    TEXT_DIR.mkdir(parents=True, exist_ok=True)
    index = []
    for pg in all_pages(q):
        r = fetch_page(wf, pg)
        sid = pg.get("source_id") or f"web_{pg['group']}_{pg['id']}"
        if r["raw_path"]:
            txt = page_text({"raw_path": r["raw_path"]})
            (TEXT_DIR / f"{pg['id']}.txt").write_text(txt, encoding="utf-8")
            register_source(sid, pg.get("title") or f"{pg['entity_name']}: {pg.get('kind', 'page')} "
                            f"{pg.get('year', '')}".strip(), pg["url"], pg.get("publisher") or pg["entity_name"],
                            "Public web page" if not r["raw_path"].endswith(".pdf") else "Public PDF",
                            f"{pg.get('kind', '')}; year {pg.get('year', '')}; fetched via {r['method_used']}; "
                            f"raw: {r['raw_path']}", retrieved_date=RETRIEVED)
        index.append(dict(page_id=pg["id"], source_id=sid, group=pg["group"], entity_id=pg["entity_id"],
                          entity_name=pg["entity_name"], entity_ein=pg["entity_ein"], kind=pg.get("kind", ""),
                          year=pg.get("year", ""), url=pg["url"], method_used=r["method_used"],
                          raw_path=r["raw_path"], status=r["status"], text_chars=r["text_chars"],
                          retrieved_date=RETRIEVED))
    W43.write_csv(INTERIM / "web_pages.csv", list(index[0].keys()) if index else ["page_id"], index)
    ok = sum(1 for i in index if i["status"] == "ok" or i["status"].endswith("tavily ok"))
    by = {}
    for i in index:
        by.setdefault(i["group"], [0, 0])
        by[i["group"]][0] += 1
        by[i["group"]][1] += bool(i["raw_path"])
    lines = [f"- search hits {len(hits)}; pages listed {len(index)}, with content {ok}",
             "- by group (listed, fetched): " + ", ".join(f"{k} {v[0]}/{v[1]}" for k, v in by.items()),
             "- failed/empty: " + "; ".join(f"{i['page_id']} ({i['status']})" for i in index
                                             if not i["raw_path"] or i["text_chars"] < 200)[:1500],
             f"- {wf.summary()}"]
    log("44_web_peers_funders", "\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
