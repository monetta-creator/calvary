"""Grantmaker web explorer (page title "Calvary Grantmaker Web"): export the m6 funder-recipient network (filed grants TY2020-24) into an interactive page.

Same graph as scripts/06_m6_network.py (same filters, same landscape exclusions), with every funder of Calvary or a
core peer, per-year grant dollars on each link, and short display names. Writes two copies of one page:
  web/Calvary_Grantmaker_Web.html    self-contained: d3 and fonts embedded from web/vendor/, opens offline by double-click
  web/publish/funder_network.html    the same page without <html>/<head>/<body>, loading d3 and fonts from CDNs, for the claude.ai artifact
Public filings only: no CRM data, no people, no board links (review finding R05), no pipeline tiers (R16/R17 pending).
Run: calvary_funding_data/.venv/bin/python calvary_analysis/web/build_network_page.py
"""
import base64
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

WEB = Path(__file__).resolve().parent
sys.path.insert(0, str(WEB.parent / "scripts"))
from lib.common import ANALYSIS, AS_OF, CALVARY, CHART_DATA, FUNDER_SHORT, core_peers, load, peer_set  # noqa: E402

YEARS = [2020, 2021, 2022, 2023, 2024]
STANDALONE = "Calvary_Grantmaker_Web.html"
GROUPS = {"1a_dc_women_homeless": "DC women's homelessness", "1b_dc_dv": "DC domestic violence",
          "2_dc_homeless_recovery": "DC homelessness and recovery", "2_dc_ward78": "DC Wards 7–8",
          "3_dmv_women_dv": "Maryland and Virginia: women and domestic violence"}
D3_CDN = "https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js"
TYPE_LABEL = {"private_foundation": "Private foundation", "community_foundation": "Community foundation",
              "corporate_foundation": "Corporate foundation", "daf_sponsor": "Donor-advised fund sponsor",
              "federated_giving": "Federated giving (United Way and similar)", "public_charity_grantmaker": "Public charity grantmaker",
              "other": "Other grantmaker"}
# Status notes that change how a funder should be read. Source: independent review, reports/review/review_findings.csv.
NOTES = {"521512330": "Winding down: the A. James & Alice B. Clark Foundation's own FAQ says it is sunsetting, operational until 31 Dec 2025, "
                      "and takes no unsolicited proposals (independent review finding R16, verified 2026-10-10)."}
WORD_FIX = {"jpmorgan": "JPMorgan", "fdn": "Foundation", "tr": "Trust", "fd": "Fund", "chrtbl": "Charitable", "assn": "Association"}
SMALL = {"of", "the", "and", "for", "in", "at", "by", "to", "on", "a", "an", "de"}
UPPER = {"DC", "NCA", "USA", "US", "PNC", "AARP", "IBM", "CSX", "MGM", "UPS", "BB&T", "TD", "KPMG", "RCLCO", "AOL", "II", "III", "IV", "YMCA", "NW", "SE", "NE", "SW", "LLC", "LLP", "PC"}


def display_name(legal: str) -> str:
    s = re.sub(r"[,\s]+(INC|INCORPORATED|CORP|CORPORATION)\.?$", "", str(legal).strip(), flags=re.I)
    words = []
    for i, w in enumerate(s.split()):
        lw = w.lower()
        if lw in WORD_FIX:
            words.append(WORD_FIX[lw])
        elif w.upper() in UPPER:
            words.append(w.upper())
        elif i and lw in SMALL:
            words.append(lw)
        else:
            words.append("-".join(p[:1].upper() + p[1:].lower() for p in w.split("-")))
    return " ".join(words) if words else str(legal)


def build_data() -> dict:
    ps = peer_set().set_index("ein")
    subjects = [CALVARY] + sorted(core_peers().ein)
    gr = load("fact_grants", usecols=["funder_id", "recipient_ein", "tax_year", "amount", "cumulative_flag", "source_type"])
    excl = pd.read_csv(ANALYSIS / "config" / "landscape_exclusions.csv", dtype=str)
    gr = gr[(gr.cumulative_flag != 1) & gr.source_type.isin(["pf_grants_paid", "schedule_i"]) & gr.tax_year.between(2020, 2024)
            & gr.recipient_ein.isin(subjects) & ~gr.funder_id.isin(set(excl.funder_id))]
    df = load("dim_funder", usecols=["funder_id", "funder_name", "funder_type"]).drop_duplicates("funder_id").set_index("funder_id")
    links = gr.groupby(["funder_id", "recipient_ein"]).agg(amount=("amount", "sum"), grants=("amount", "size")).reset_index()
    by_year = gr.groupby(["funder_id", "recipient_ein", "tax_year"]).amount.sum()
    fun = links.groupby("funder_id").agg(orgs=("recipient_ein", "nunique"), amount=("amount", "sum"), grants=("grants", "sum")).reset_index()
    cal_funders = set(links[links.recipient_ein == CALVARY].funder_id)

    # Reconcile with the published network table before writing anything.
    m6 = pd.read_csv(CHART_DATA / "m6_01_central_funders.csv", dtype={"funder_id": str}).set_index("funder_id")
    chk = fun.set_index("funder_id")
    assert set(chk.index) == set(m6.index), "funder set differs from m6_01_central_funders"
    assert (chk.orgs == m6.recipients.reindex(chk.index)).all(), "organization counts differ from m6_01"
    assert ((chk.amount - m6.amount.reindex(chk.index)).abs() < 0.5).all(), "dollar totals differ from m6_01"
    assert (chk.grants == m6.grants.reindex(chk.index)).all(), "grant counts differ from m6_01"

    nodes = pd.read_csv(CHART_DATA / "m6_03_network_nodes.csv", dtype={"node": str}).set_index("node")
    rx, ry = nodes.x.abs().max(), nodes.y.abs().max()  # the chart's ellipse; angle is read on the unit circle
    angle = {e: float(np.arctan2(nodes.loc[e, "y"] / ry, nodes.loc[e, "x"] / rx)) for e in subjects if e != CALVARY}
    # Who the 19 are: place and one-line description (web/org_profiles.csv), group, and size and government share from the
    # peer benchmark table (m3_00, the Appendix B numbers).
    prof = pd.read_csv(WEB / "org_profiles.csv", dtype={"ein": str}).set_index("ein")
    bench = pd.read_csv(CHART_DATA / "m3_00_benchmark_table.csv", dtype={"ein": str}).set_index("ein")
    tier = core_peers().set_index("ein").tier
    assert set(subjects) <= set(prof.index) and set(subjects) <= set(bench.index), "every organization needs a profile and a benchmark row"
    num = lambda v, nd: None if pd.isna(v) else round(float(v), nd)
    orgs = [{"id": e, "name": ps.loc[e, "short"], "legal": ps.loc[e, "name"], "calvary": e == CALVARY, "angle": round(angle.get(e, 0.0), 4),
             "place": prof.loc[e, "place"], "what": prof.loc[e, "what"], "group": "Calvary" if e == CALVARY else GROUPS[tier[e]],
             "revenue": num(bench.loc[e, "revenue_fy2024"], 0), "revYear": int(bench.loc[e, "latest_fy"]), "gov": num(bench.loc[e, "gov_share_fy2022_24_mean"], 3)}
            for e in subjects]
    funders = []
    for r in fun.sort_values(["orgs", "amount"], ascending=False).itertuples():
        legal = df.funder_name.get(r.funder_id, r.funder_id)
        ftype = df.funder_type.get(r.funder_id, "other") if pd.notna(df.funder_type.get(r.funder_id)) else "other"
        funders.append({"id": r.funder_id, "name": FUNDER_SHORT[r.funder_id].replace(" Fdn", " Foundation") if r.funder_id in FUNDER_SHORT else display_name(legal), "legal": display_name(legal),
                        "type": ftype, "orgs": int(r.orgs), "amount": round(float(r.amount)), "grants": int(r.grants),
                        "calvary": r.funder_id in cal_funders, "note": NOTES.get(r.funder_id, "")})
    out_links = [{"f": r.funder_id, "o": r.recipient_ein, "amount": round(float(r.amount)), "grants": int(r.grants),
                  "years": [round(float(by_year.get((r.funder_id, r.recipient_ein, y), 0.0))) for y in YEARS]}
                 for r in links.sort_values(["funder_id", "recipient_ein"]).itertuples()]
    return {"asOf": AS_OF, "years": YEARS, "typeLabels": TYPE_LABEL, "orgs": orgs, "funders": funders, "links": out_links,
            "totals": {"funders": len(funders), "orgs": len(orgs), "links": len(out_links), "amount": round(float(links.amount.sum())),
                       "funders3": int((fun.orgs >= 3).sum()), "calvaryFunders": len(cal_funders)}}


def main() -> None:
    data = build_data()
    page = (WEB / "network_page.template.html").read_text()
    assert page.count("/*__DATA__*/null") == 1
    page = page.replace("/*__DATA__*/null", json.dumps(data, separators=(",", ":")).replace("</", "<\\/"))
    (WEB / "publish").mkdir(exist_ok=True)
    (WEB / "publish" / "funder_network.html").write_text(page)
    (WEB / STANDALONE).write_text(standalone(page))
    t = data["totals"]
    print(f"funders {t['funders']} (3+ orgs: {t['funders3']}), orgs {t['orgs']}, links {t['links']}, ${t['amount']:,}; "
          f"Calvary funders {t['calvaryFunders']}; wrote web/{STANDALONE} and web/publish/funder_network.html")


def standalone(page: str) -> str:
    """Full document with d3 and the fonts embedded, so the file opens offline by double-click (web/vendor/README.md)."""
    vendor = WEB / "vendor"
    d3_tag = f'<script src="{D3_CDN}"></script>'
    font_links = re.findall(r'<link rel="(?:preconnect|stylesheet)" href="https://fonts\.(?:googleapis|gstatic)\.com[^>]*>\n', page)
    assert page.count(d3_tag) == 1 and len(font_links) == 3, "template's CDN tags changed"
    d3_js = (vendor / "d3-7.9.0.min.js").read_text()
    assert "</script" not in d3_js
    faces = []
    for family, f in json.loads((vendor / "fonts" / "fonts.json").read_text()).items():
        b64 = base64.b64encode((vendor / "fonts" / f["file"]).read_bytes()).decode()
        faces.append(f'@font-face {{ font-family: "{family}"; font-style: normal; font-weight: {f["weight"]}; font-display: swap; '
                     f'src: url(data:font/woff2;base64,{b64}) format("woff2"); unicode-range: {f["unicode_range"]}; }}')
    for link in font_links:
        page = page.replace(link, "")
    page = page.replace(d3_tag, f"<script>/* d3 7.9.0, ISC license: web/vendor/LICENSE-d3.txt */\n{d3_js}</script>")
    head, body = page.split("<!--__BODY__-->", 1)
    head = head.replace("<style>\n", "<style>\n/* Bricolage Grotesque and Public Sans, SIL OFL 1.1: web/vendor/fonts/ */\n" + "\n".join(faces) + "\n", 1)
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            f'{head}</head>\n<body>{body}</body>\n</html>\n')


if __name__ == "__main__":
    main()
