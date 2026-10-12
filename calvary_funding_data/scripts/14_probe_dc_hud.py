"""Phase 2 recon, area "dc_hud": DC government, DC Council and HUD/regional homelessness sources.

Reruns the discovery-confirmed downloads and probes:
  dcgis   : DC Open Data (ArcGIS Hub search API + DCAT feed); DC GIS layers for 2022 wards,
            2020 tracts, homeless shelters / service facilities, OVSJG Grant Recipients (all rows),
            PASS purchase orders / payments / contracts (Calvary, TCP and peer queries + FY stats)
  budget  : DC CFO approved budget chapters + appendix tables FY2024-FY2027 for JA0 DHS, FO0 OVSJG,
            RM0 DBH, DB0 DHCD, HY0 DCHA payment/subsidy, CF0 DOES, HG0 DMHHS; logs a keyword page
            index and program/activity codes per PDF
  council : OVSJG published recipient lists; DC Council performance-oversight responses and
            budget-oversight attachments (DHS, ICH, OVSJG, DBH, DHCD, DCHA, DOES); committee
            budget reports; Council Budget Office change charts; Budget Support Act texts;
            logs Calvary / peer page hits per document
  hud     : HUD User AHAR 2025 PIT/HIC by CoC workbooks; HUD Exchange DC-500 CoC award, HIC and
            PopSub reports; hud.gov FY2024 DC award report, FY2025 award announcements, DC-500 GIWs;
            MWCOG "Homelessness in Metropolitan Washington" reports 2023-2026

Writes raw/dc_gov/, raw/dc_council/, raw/hud/, source registry rows and build-log entries.
No keys needed. The DC Council LIMS API needs a token and is not called.

  misc    : probe-only pages (OCP portal, grants clearinghouse, TCP/ICH/DC PIT hub, LIMS API status)

Usage: .venv/bin/python scripts/14_probe_dc_hud.py [--only dcgis,budget,council,hud,misc] [--skip-large]
  --skip-large  skip the two big oversight attachment bundles (DHS 2025 ~35 MB, DBH 2025 ~13 MB)
"""
from __future__ import annotations

import argparse
import html as htmlmod
import io
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import urljoin

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import (USER_AGENT, RateLimiter, log, norm_name, register_source, rel, save_raw,
                        session, sha256_file, today)

PROBE_DATE = today()
S = session()
RL = RateLimiter(2.0)
# huduser.gov sits behind an AWS WAF that challenges non-browser UAs; this UA still identifies us.
HUDUSER_UA = f"Mozilla/5.0 (compatible; {USER_AGENT})"

SUMMARY: dict[str, list[str]] = defaultdict(list)
BYTES: dict[str, int] = defaultdict(int)
FAILS: list[str] = []

CALVARY_RE = re.compile(r"calvary\s+wom[ae]n", re.I)
PEERS = {
    "N Street Village": r"n\.?\s*street\s+village",
    "Miriam's Kitchen": r"miriam'?s\s+kitchen",
    "Friendship Place": r"friendship\s+place",
    "Pathways to Housing DC": r"pathways\s+to\s+housing",
    "House of Ruth": r"house\s+of\s+ruth",
    "My Sister's Place": r"my\s+sister'?s\s+place",
    "DASH": r"district\s+alliance\s+for\s+safe\s+housing|\bDASH\b",
    "Community of Hope": r"community\s+of\s+hope",
    "New Endeavors by Women": r"new\s+endeavors\s+by\s+women",
    "Coalition for the Homeless": r"coalition\s+for\s+the\s+homeless",
    "SOME": r"so\s+others\s+might\s+eat|\bSOME\b,?\s+inc",
    "Catholic Charities": r"catholic\s+charities",
    "Christ House": r"christ\s+house",
    "Thrive DC": r"thrive\s+dc",
    "The Community Partnership (TCP)": r"community\s+partnership\s+for\s+the\s+prevention|\bTCP\b",
}
PEER_RE = {k: re.compile(v, re.I) for k, v in PEERS.items()}


# ---------------------------------------------------------------- helpers
def fetch(url: str, source: str, desc: str, ext: str, params: dict | None = None,
          ua: str | None = None, timeout: int = 180, expect_pdf: bool = False) -> tuple[Path | None, bytes | None]:
    """GET url, save the untouched body to raw/{source}/ on HTTP 200. Returns (path, body)."""
    RL.wait()
    headers = {"User-Agent": ua} if ua else None
    try:
        r = S.get(url, params=params, headers=headers, timeout=timeout)
    except Exception as e:  # network error
        FAILS.append(f"{desc}: {type(e).__name__} {e}"[:200])
        return None, None
    if r.status_code != 200:
        FAILS.append(f"{desc}: HTTP {r.status_code} {r.url}"[:250])
        return None, None
    body = r.content
    if expect_pdf and not body.startswith(b"%PDF"):
        FAILS.append(f"{desc}: not a PDF ({r.headers.get('content-type')}) {r.url}"[:250])
        return None, None
    p = save_raw(source, desc, body, ext)
    BYTES[source] += len(body)
    return p, body


def pdf_pages_text(path: Path) -> list[str]:
    """Fast per-page text with pypdfium2; empty strings for image-only pages."""
    import pypdfium2 as pdfium
    out = []
    try:
        doc = pdfium.PdfDocument(str(path))
        for i in range(len(doc)):
            try:
                tp = doc[i].get_textpage()
                out.append(tp.get_text_range() or "")
            except Exception:
                out.append("")
        doc.close()
    except Exception as e:
        FAILS.append(f"pdf text {path.name}: {e}"[:200])
    return out


def page_hits(pages: list[str], rx: re.Pattern) -> list[int]:
    return [i + 1 for i, t in enumerate(pages) if rx.search(t)]


def compress(nums: list[int], limit: int = 25) -> str:
    """1,2,3,7 -> '1-3,7' (truncated)."""
    if not nums:
        return "-"
    runs, start, prev = [], nums[0], nums[0]
    for n in nums[1:]:
        if n == prev + 1:
            prev = n
            continue
        runs.append(f"{start}-{prev}" if start != prev else f"{start}")
        start = prev = n
    runs.append(f"{start}-{prev}" if start != prev else f"{start}")
    s = ",".join(runs[:limit])
    return s + (",..." if len(runs) > limit else "")


def text_profile(path: Path, label: str, section: str, extra: dict[str, re.Pattern] | None = None):
    """Log page count, text coverage, Calvary and peer page hits for a PDF."""
    pages = pdf_pages_text(path)
    n = len(pages)
    texty = sum(1 for t in pages if len(t.strip()) > 80)
    cal = page_hits(pages, CALVARY_RE)
    peers = {k: len(page_hits(pages, rx)) for k, rx in PEER_RE.items()}
    peer_s = ", ".join(f"{k} {v}" for k, v in peers.items() if v)
    line = (f"- {label}: {n} pp ({texty} with text); Calvary pages: {compress(cal)}"
            + (f"; peer page counts: {peer_s}" if peer_s else ""))
    if extra:
        for k, rx in extra.items():
            line += f"; {k}: {compress(page_hits(pages, rx), 15)}"
    SUMMARY[section].append(line)
    return pages


def calvary_lines(pages: list[str], width: int = 160, limit: int = 12) -> list[str]:
    out = []
    for i, t in enumerate(pages):
        for ln in t.splitlines():
            if CALVARY_RE.search(ln):
                out.append(f"p{i + 1}: {' '.join(ln.split())[:width]}")
                if len(out) >= limit:
                    return out
    return out


# ---------------------------------------------------------------- 1. DC Open Data / DC GIS
HUB_SEARCH = "https://opendata.dc.gov/api/search/v1/collections/dataset/items"
DCAT = "https://opendata.dc.gov/api/feed/dcat-us/1.1.json"
DCGIS = "https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA"
LAYERS = {
    "wards_2022": "Administrative_Other_Boundaries_WebMercator/MapServer/53",
    "census_tracts_2020": "Demographic_WebMercator/MapServer/8",
    "homeless_shelters": "Public_Service_WebMercator/MapServer/25",
    "homeless_service_facilities": "Public_Service_WebMercator/MapServer/6",
    "ovsjg_grant_recipients": "Public_Safety_WebMercator/MapServer/35",
    "pass_contracts": "Government_Operations/MapServer/37",
    "pass_purchase_orders": "Government_Operations/MapServer/16",
    "pass_payments": "Government_Operations/MapServer/17",
}
# Field lists exclude DC staff names, e-mails and phone numbers carried by some layers.
F_WARDS = "WARD,NAME,REP_NAME,WARD_ID,LABEL,STUSAB,SUMLEV,GEOID,GEOCODE,STATE"
F_PO = ("PONUMBER,AGENCYCODE,AGENCY_ACRONYM,AGENCY_NAME,STATUS,CONTRACTNUMBER,SUPPLIER,ORDEREDDATE,CREATEDATE,"
        "POTOTAL,FISCALYEAR,POTITLE,COMMODITYCODE,COMMODITYNAME,REQUISTIONNUMBER")
F_PAY = ("AGENCYCODE,AGENCY_ACRONYM,AGENCY_NAME,CONTRACTNUMBER,SUPPLIERNAME,INVOICENUMBER,PONUMBER,VOUCHERNUMBER,"
         "VOUCHERAMOUNT,PAYMENTDATE,PAYMENTAMOUNT,FISCALYEAR,TRANSACTION_CODE,PAYMENTTYPE,INVOICEDATE,OBJECTID")
F_CON = ("PROCUREMENTMETHODDESCRIPTION,AGENCY_ACRONYM,AGENCY_NAME,AGENCY,AWARDDATE,CONTRACTAMOUNT,ENDDATE,CONTRACTNUMBER,"
         "STARTDATE,CONTRACTSTATUS,TITLE,FISCALYEAR,MARKETTYPE,COMMODITYCODE,COMMODITYDESCRIPTION,CURRENTOPTIONPERIOD,"
         "TOTALOPTIONPERIODS,SUPPLIER,DESCRIPTION,CONTRACTTYPEDESCRIPTION,VENDORCITY,VENDORSTATE,CONTRACT_DETAILS_LINK,OBJECTID")
HUB_QUERIES = ["ward 2022", "census tracts 2020", "homeless", "shelter", "contracts", "purchase orders",
               "grants", "budget", "victim"]
PEER_SUPPLIER_LIKE = {
    "N Street Village": "%N STREET VILLAGE%", "Miriam's Kitchen": "%MIRIAM%KITCHEN%",
    "Friendship Place": "%FRIENDSHIP PLACE%", "Pathways to Housing": "%PATHWAYS TO HOUSING%",
    "House of Ruth": "%HOUSE OF RUTH%", "My Sister's Place": "%MY SISTER%PLACE%",
    "DASH": "%ALLIANCE FOR SAFE HOUSING%", "Community of Hope": "%COMMUNITY OF HOPE%",
    "New Endeavors by Women": "%NEW ENDEAVORS%", "Coalition for the Homeless": "%COALITION FOR THE HOMELESS%",
    "SOME": "%SO OTHERS MIGHT EAT%", "Catholic Charities": "%CATHOLIC CHARITIES%",
    "Christ House": "%CHRIST HOUSE%", "TCP": "%COMMUNITY PARTNERSHIP%",
}


def arc_query(layer_key: str, desc: str, where: str, out_fields: str = "*", geojson: bool = False,
              extra: dict | None = None, paginate: bool = False) -> list[dict]:
    """Query a DC GIS layer; save every page raw. Returns feature attribute dicts."""
    url = f"{DCGIS}/{LAYERS[layer_key]}/query"
    feats, offset, page = [], 0, 0
    while True:
        params = {"where": where, "outFields": out_fields, "f": "geojson" if geojson else "json",
                  "returnGeometry": "true" if geojson else "false", "outSR": "4326",
                  "orderByFields": "OBJECTID" if layer_key != "pass_purchase_orders" else "OBJECT_ID"}
        if extra:
            params.update(extra)
            if "outStatistics" in extra:
                params.pop("orderByFields", None)
        if paginate:
            params.update({"resultOffset": offset, "resultRecordCount": 1000})
        p, body = fetch(url, "dc_gov", f"dcgis_{layer_key}_{desc}" + (f"_p{page}" if paginate else ""),
                        "geojson" if geojson else "json", params=params)
        if body is None:
            break
        d = json.loads(body)
        if "error" in d:
            FAILS.append(f"dcgis {layer_key} {desc}: {d['error']}"[:250])
            break
        fs = d.get("features", [])
        feats += [f.get("properties") if geojson else f.get("attributes") for f in fs]
        more = d.get("exceededTransferLimit") or (d.get("properties") or {}).get("exceededTransferLimit")
        if not (paginate and (more or len(fs) == 1000)):
            break
        offset += len(fs)
        page += 1
    return feats


def stats_query(layer_key: str, desc: str, where: str, group: str, count_field: str, sum_field: str):
    stats = json.dumps([{"statisticType": "count", "onStatisticField": count_field, "outStatisticFieldName": "n"},
                        {"statisticType": "sum", "onStatisticField": sum_field, "outStatisticFieldName": "amt"}])
    return arc_query(layer_key, desc, where, extra={"groupByFieldsForStatistics": group, "outStatistics": stats})


def run_dcgis():
    sec = "14_probe_dc_hud: DC Open Data / DC GIS"
    out = SUMMARY[sec]
    # Hub search API
    for q in HUB_QUERIES:
        p, body = fetch(HUB_SEARCH, "dc_gov", f"hub_search_{q.replace(' ', '_')}", "json",
                        params={"q": q, "limit": 25})
        if body:
            d = json.loads(body)
            titles = [f["properties"].get("title") for f in d.get("features", [])][:6]
            out.append(f"- hub search '{q}': numberMatched {d.get('numberMatched')}; top: {'; '.join(titles)}")
    p, body = fetch(DCAT, "dc_gov", "dcat_us_1_1_feed", "json")
    if body:
        ds = json.loads(body).get("dataset", [])
        hits = [x.get("title") for x in ds if re.search(r"homeless|shelter|ovsjg|contract|purchase|payment|ward|budget",
                                                         x.get("title", ""), re.I)]
        out.append(f"- DCAT feed: {len(ds)} datasets; {len(hits)} titles match homeless/contract/ward/budget terms")
    # layer metadata
    for k, path in LAYERS.items():
        p, body = fetch(f"{DCGIS}/{path}", "dc_gov", f"dcgis_{k}_layer_meta", "json", params={"f": "json"})
        if body:
            m = json.loads(body)
            out.append(f"- layer {k} ({path}): name '{m.get('name')}', {len(m.get('fields') or [])} fields, "
                       f"maxRecordCount {m.get('maxRecordCount')}")
    # boundaries
    w = arc_query("wards_2022", "all_geojson", "1=1", geojson=True, out_fields=F_WARDS)
    out.append(f"- wards_2022 GeoJSON: {len(w)} features; WARD values {sorted(x.get('WARD') for x in w)}")
    t = arc_query("census_tracts_2020", "all_geojson", "1=1", geojson=True,
                  out_fields="TRACT,GEOID,NAME,POP100,HU100,ALAND,AWATER")
    out.append(f"- census_tracts_2020 GeoJSON: {len(t)} features (fields TRACT, GEOID, NAME, POP100, HU100, ALAND, AWATER)")
    # homeless facilities
    sh = arc_query("homeless_shelters", "all_geojson", "1=1", geojson=True,
                   out_fields="NAME,ADDRESS,ZIPCODE,WARD,OWNER_RENTER,PROVIDER,TYPE,SUBTYPE,STATUS,NUMBER_OF_BEDS,"
                              "AGES_SERVED,LGBTQ_FOCUSED,LAST_UPDATED_BY_DHS,MAR_ID,GIS_ID,OBJECTID")
    beds = sum((x.get("NUMBER_OF_BEDS") or 0) for x in sh if x.get("STATUS") == "Active")
    cal_sh = [x.get("NAME") for x in sh if CALVARY_RE.search(str(x.get("PROVIDER")) + str(x.get("NAME")))]
    out.append(f"- homeless_shelters: {len(sh)} rows, active beds {beds:,.0f}; Calvary rows: {cal_sh or 'none'} "
               f"(layer covers DHS low-barrier/TH shelters only)")
    hf = arc_query("homeless_service_facilities", "all_geojson", "1=1", geojson=True)
    cal_hf = [x.get("NAME") for x in hf if CALVARY_RE.search(json.dumps(x))]
    out.append(f"- homeless_service_facilities: {len(hf)} rows; Calvary rows: {cal_hf or 'none'}")
    # OVSJG grant recipients (full table; ORGANIZATIONNAME holds the project title, AGENCY the grantee)
    og = arc_query("ovsjg_grant_recipients", "all", "1=1", paginate=True)
    fys = defaultdict(lambda: [0, 0.0])
    for x in og:
        fys[x.get("FY")][0] += 1
        fys[x.get("FY")][1] += x.get("AWARDAMOUNT") or 0
    out.append(f"- ovsjg_grant_recipients: {len(og)} rows; FY counts "
               + ", ".join(f"{k}: {v[0]} (${v[1]/1e6:,.1f}M)" for k, v in sorted(fys.items(), key=lambda z: z[0] or 0)))
    cal = sorted((x for x in og if CALVARY_RE.search(str(x.get("AGENCY")))), key=lambda z: (z.get("FY") or 0))
    out.append("- ovsjg_grant_recipients Calvary rows (AGENCY field = grantee): "
               + "; ".join(f"FY{x['FY']} {x['ORGANIZATIONNAME']} ${x['AWARDAMOUNT']:,.0f}" for x in cal))
    # PASS: Calvary
    po = arc_query("pass_purchase_orders", "calvary", "UPPER(SUPPLIER) LIKE '%CALVARY WOM%'", out_fields=F_PO)
    out.append(f"- PASS purchase orders, supplier like CALVARY WOM: {len(po)} rows: "
               + "; ".join(f"FY{x['FISCALYEAR']} {x['AGENCY_ACRONYM']} {x['POTITLE'][:45]} ${x['POTOTAL']:,.0f}"
                           for x in sorted(po, key=lambda z: (z['FISCALYEAR'] or '', z['PONUMBER'] or ''))))
    pay = arc_query("pass_payments", "calvary", "UPPER(SUPPLIERNAME) LIKE '%CALVARY WOM%'", out_fields=F_PAY, paginate=True)
    agg = defaultdict(float)
    for x in pay:
        agg[(x.get("FISCALYEAR"), x.get("AGENCY_ACRONYM"))] += x.get("PAYMENTAMOUNT") or 0
    out.append(f"- PASS payments to CALVARY WOM*: {len(pay)} rows; by FY/agency: "
               + "; ".join(f"FY{k[0]} {k[1]} ${v:,.0f}" for k, v in sorted(agg.items(), key=lambda z: (z[0][0] or '', z[0][1] or ''))))
    con = arc_query("pass_contracts", "calvary", "UPPER(SUPPLIER) LIKE '%CALVARY%'", out_fields=F_CON)
    out.append(f"- PASS contracts (OCP awards >= $100K), supplier like CALVARY: {len(con)} rows")
    # PASS: TCP (DHS intermediary) and peers, aggregates
    tcp = arc_query("pass_purchase_orders", "tcp_rows", "UPPER(SUPPLIER) LIKE '%COMMUNITY PARTNERSHIP%'",
                    out_fields=F_PO, paginate=True)
    tagg = defaultdict(float)
    for x in tcp:
        tagg[(x.get("FISCALYEAR"), x.get("AGENCY_ACRONYM"))] += x.get("POTOTAL") or 0
    out.append(f"- PASS POs to THE COMMUNITY PARTNERSHIP: {len(tcp)} rows; DHS by FY: "
               + ", ".join(f"FY{k[0]} ${v/1e6:,.1f}M" for k, v in sorted(tagg.items(), key=lambda z: z[0][0] or '') if k[1] == "DHS"))
    peer_lines, fanout = [], 0
    for name, like in PEER_SUPPLIER_LIKE.items():
        if name == "TCP":
            rows = tcp
        else:
            rows = arc_query("pass_purchase_orders", f"peer_{norm_name(name).replace(' ', '_')}",
                             f"UPPER(SUPPLIER) LIKE '{like}'", out_fields=F_PO, paginate=True)
        # EOM (agency code AA0) POs repeat once per EOM sub-office acronym; dedupe on PO number + version
        uniq = {(r.get("PONUMBER"), r.get("FISCALYEAR"), r.get("POTOTAL")): r for r in rows}
        fanout += len(rows) - len(uniq)
        tot = sum(r.get("POTOTAL") or 0 for r in uniq.values())
        yrs = sorted({r.get("FISCALYEAR") for r in uniq.values() if r.get("FISCALYEAR")})
        ags = sorted({r.get("AGENCYCODE") for r in uniq.values() if r.get("AGENCYCODE")})
        peer_lines.append(f"{name}: {len(uniq)} POs ${tot/1e6:,.1f}M, FY{yrs[0] if yrs else '-'}-{yrs[-1] if yrs else '-'}, "
                          f"agency codes {'/'.join(ags) or '-'}")
    out.append(f"- PASS PO duplicate rows removed for peers (AA0 sub-office fan-out): {fanout}")
    out.append("- PASS PO totals by peer supplier (all years): " + "; ".join(peer_lines))
    # coverage stats
    for k, grp, cf, sf in [("pass_purchase_orders", "FISCALYEAR", "OBJECT_ID", "POTOTAL"),
                           ("pass_contracts", "FISCALYEAR", "OBJECTID", "CONTRACTAMOUNT"),
                           ("pass_payments", "FISCALYEAR", "OBJECTID", "PAYMENTAMOUNT")]:
        rows = stats_query(k, "fy_stats", "1=1", grp, cf, sf)
        yrs = sorted(r.get(grp) for r in rows if r.get(grp))
        n = sum(r.get("N") or r.get("n") or 0 for r in rows)
        out.append(f"- {k}: {n:,} rows, FISCALYEAR {yrs[0] if yrs else '-'}-{yrs[-1] if yrs else '-'}")
    for sid, name, url, notes in [
        ("api_dc_opendata_hub", "DC Open Data (ArcGIS Hub) search API and DCAT-US feed", HUB_SEARCH,
         "Hub search /api/search/v1/collections/dataset/items?q=; DCAT feed /api/feed/dcat-us/1.1.json"),
        ("api_dcgis_boundaries", "DC GIS 2022 wards and 2020 census tracts (MapServer query)",
         f"{DCGIS}/{LAYERS['wards_2022']}", "Wards from 2022 (layer 53); Census Tracts 2020 (Demographic layer 8); f=geojson outSR=4326"),
        ("api_dcgis_homeless_facilities", "DC GIS Homeless Shelter Locations and Homeless Service Facilities",
         f"{DCGIS}/{LAYERS['homeless_shelters']}", "Public_Service_WebMercator layers 25 (shelters, DHS-sourced) and 6 (service facilities)"),
        ("api_dcgis_ovsjg_grants", "DC GIS OVSJG Grant Recipients layer", f"{DCGIS}/{LAYERS['ovsjg_grant_recipients']}",
         "FY2016-FY2025 award rows; ORGANIZATIONNAME holds the project title and AGENCY the grantee name (labels swapped)"),
        ("api_dcgis_pass", "DC OCP PASS purchase orders, payments and contracts (DC GIS layers)",
         f"{DCGIS}/Government_Operations/MapServer", "Layers 16 (POs > $2,500), 17 (payments), 37 (contracts >= $100K, OCP agencies)"),
    ]:
        register_source(sid, name, url, "DC Office of the Chief Technology Officer / DC GIS; source agencies OCP, OVSJG, DHS",
                        "DC Open Data terms (CC BY 4.0 per opendata.dc.gov)", notes)


# ---------------------------------------------------------------- 2. DC budget books
CFO = "https://cfo.dc.gov"
CFO_ROOTS = {2027: f"{CFO}/node/1822601", 2026: f"{CFO}/node/1778906", 2025: f"{CFO}/node/1712181"}
AGENCY_RE = re.compile(r"\b(JA0|FO0|RM0|DB0|HY0|CF0|HG0)\b")
FY2024_PAGES = {
    "JA0": "2024-ja0-department-human-services", "FO0": "2024-fo0-office-victim-services-and-justice-grants",
    "RM0": "2024-rm0-department-behavioral-health", "DB0": "2024-db0-department-housing-and-community-development",
    "HY0": "2024-hy0-housing-authority-subsidy", "CF0": "2024-cf0-department-employment-services",
    "HG0": "2024-hg0-deputy-mayor-health-and-human-services",
}
ATT = f"{CFO}/sites/default/files/dc/sites/ocfo/publication/attachments"
# discovery-confirmed direct URLs where an agency page links another year's files
BUDGET_FALLBACK = {
    (2024, "JA0"): [f"{ATT}/ja_dhs_chapter_2024j.pdf", f"{ATT}/ja_dhs_tables_2024j.pdf"],
    (2024, "RM0"): [f"{ATT}/rm_dbh_tables_2024j.pdf", f"{ATT}/rm_dbh_crosswalk_2024j.pdf", f"{ATT}/rm_dbh_chapter_2023j_0.pdf"],
    (2025, "CF0"): [f"{ATT}/cf0_does_chapter_2025j.pdf", f"{ATT}/cf_does_tables_2025j.pdf"],
}
BUDGET_KEYWORDS = {
    "homeless": re.compile(r"homeless", re.I),
    "PSH": re.compile(r"permanent\s+supportive\s+housing", re.I),
    "victim_svcs": re.compile(r"victim\s+services", re.I),
    "rent_supp": re.compile(r"local\s+rent\s+supplement|LRSP", re.I),
    "ICH": re.compile(r"interagency\s+council\s+on\s+homelessness", re.I),
    "tbl_prog_activity": re.compile(r"Table\s+[A-Z]{2}0-4\b"),
    "sched_30PBB": re.compile(r"30-PBB"),
    "budget_changes": re.compile(r"Enhance/Reduce|Technical Adjustment|One-Time|Mayor.s Proposed Budget", re.I),
}
STAGE_RE = re.compile(r"FY\s?(20\d\d)\s+(Approved|Proposed)\s+Budget\s+(?:and\s+Financial\s+Plan|Program|Division|is\s+presented)"
                      r"|agency.s\s+FY\s?(20\d\d)\s+(approved|proposed)\s+budget", re.I)
# activity rows in the four layouts seen FY2024-FY2027 (chapter Table XX0-4 and appendix Schedule 30-PBB)
CODE_RES = [
    re.compile(r"\(([A-Z0-9]{4,6})\)\s+([A-Za-z][A-Za-z0-9 ,&/'\-\.:]+?)\s+(?=-?\d[\d,]*\s)"),          # (H03010) Name 1,234
    re.compile(r"\b([A-Z]{1,3}\d{3,5})-\s?([A-Z][A-Z0-9 ,&/'\-\.:()]+?)\s+(?=-?\d[\d,]*\s|N/A)"),       # H03010-NAME 1,234
]
LINE_CODE_RE = re.compile(r"^([A-Z][A-Z0-9 ,&/'\-\.:()]+?)\s+([A-Z]{1,3}\d{3,5}|\d{4})\s+-?\d[\d,]*\s")  # NAME H03010 1,234
CODE_KEEP = re.compile(r"homeless|supportive|shelter|family serv|adult serv|victim|rent supp|housing|"
                       r"behavioral|crisis|domestic|interagency|youth serv|prevention|rapid|rehousing|re-housing", re.I)


def activity_codes(pages: list[str]) -> dict[str, str]:
    codes: dict[str, str] = {}
    for t in pages:
        flat = " ".join(t.split())
        for rx in CODE_RES:
            for c, nm in rx.findall(flat):
                nm = " ".join(nm.split()).strip(" -")
                if CODE_KEEP.search(nm) and c not in codes:
                    codes[c] = nm[:60]
        for ln in t.splitlines():
            m = LINE_CODE_RE.match(ln.strip())
            if m and CODE_KEEP.search(m.group(1)) and m.group(2) not in codes:
                codes[m.group(2)] = " ".join(m.group(1).split())[:60]
    return codes


def cfo_agency_pages(fy: int) -> dict[str, str]:
    """Crawl an approved-budget root -> cluster pages -> agency pages; returns {agency_code: page_url}."""
    p, body = fetch(CFO_ROOTS[fy], "dc_gov", f"cfo_budget_fy{fy}_clusters", "html")
    if not body:
        return {}
    h = body.decode("utf-8", "ignore")
    found = {}
    for a, title in re.findall(r'href="(/node/\d+)" title="(20\d\d [^"]+)"', h):
        p2, b2 = fetch(urljoin(CFO, a), "dc_gov", f"cfo_budget_fy{fy}_cluster_{a.split('/')[-1]}", "html")
        if not b2:
            continue
        for a2, t2 in re.findall(r'href="(/node/\d+)" title="(20\d\d [^"]+)"', b2.decode("utf-8", "ignore")):
            m = AGENCY_RE.search(t2)
            if m:
                found[m.group(1)] = urljoin(CFO, a2)
    return found


def run_budget():
    sec = "14_probe_dc_hud: DC budget books (CFO approved chapters)"
    out = SUMMARY[sec]
    targets: dict[tuple[int, str], list[str]] = {}
    for fy in (2027, 2026, 2025):
        pages = cfo_agency_pages(fy)
        out.append(f"- FY{fy} approved: agency pages found {sorted(pages)}")
        for ag, url in sorted(pages.items()):
            p, body = fetch(url, "dc_gov", f"cfo_budget_fy{fy}_{ag}_page", "html")
            if not body:
                continue
            pdfs = sorted(set(re.findall(r'href="([^"]+\.pdf)"', body.decode("utf-8", "ignore"))))
            keep = [urljoin(CFO, x) for x in pdfs if re.search(r"(chapter|tables|crosswalk)", x) and str(fy) in x]
            targets[(fy, ag)] = keep or BUDGET_FALLBACK.get((fy, ag), [])
            if not keep:
                out.append(f"  - FY{fy} {ag}: agency page links no FY{fy} chapter/tables ({[x.split('/')[-1] for x in pdfs]}); "
                           f"using fallback {[x.split('/')[-1] for x in targets[(fy, ag)]]}")
    for ag, slug in FY2024_PAGES.items():
        p, body = fetch(f"{CFO}/publication/{slug}", "dc_gov", f"cfo_budget_fy2024_{ag}_page", "html")
        pdfs = sorted(set(re.findall(r'href="([^"]+\.pdf)"', body.decode("utf-8", "ignore")))) if body else []
        keep = [urljoin(CFO, x) for x in pdfs if re.search(r"(chapter|tables|crosswalk)", x) and "2024" in x]
        targets[(2024, ag)] = keep + [u for u in BUDGET_FALLBACK.get((2024, ag), []) if u not in keep]
    for (fy, ag), urls in sorted(targets.items()):
        for u in urls:
            fname = u.split("/")[-1].rsplit(".", 1)[0]
            p, body = fetch(u, "dc_gov", f"cfo_budget_fy{fy}_{ag}_{fname}", "pdf", expect_pdf=True)
            if not p:
                continue
            pages = pdf_pages_text(p)
            texty = sum(1 for t in pages if len(t.strip()) > 200)
            m = STAGE_RE.search(" ".join(" ".join(pages[:3]).split()))
            stage = (f"{(m.group(2) or m.group(4)).title()} FY{m.group(1) or m.group(3)}" if m
                     else ("image-only, needs OCR" if texty == 0 else "stage?"))
            kw = "; ".join(f"{k} {compress(page_hits(pages, rx), 12)}" for k, rx in BUDGET_KEYWORDS.items())
            codes = activity_codes(pages)
            code_s = "; ".join(f"{c} {n}" for c, n in sorted(codes.items())[:45])
            out.append(f"- FY{fy} {ag} {u.split('/')[-1]} [{stage}; {len(pages)} pp, {texty} with text]: {kw}"
                       + (f"\n  - activity codes: {code_s}" if code_s else ""))
    for fy in (2024, 2025, 2026, 2027):
        register_source(f"doc_dc_budget_fy{fy}", f"DC FY{fy} Approved Budget and Financial Plan, agency chapters and appendix tables",
                        CFO_ROOTS.get(fy, f"{CFO}/node/1826371"), "DC Office of the Chief Financial Officer, Office of Budget and Planning",
                        "Public government document", "Agencies JA0, FO0, RM0, DB0, HY0, CF0, HG0; chapter + appendix tables (+ crosswalk where posted)")


# ---------------------------------------------------------------- 3. DC Council + OVSJG lists + BSA
WP = "https://dccouncil.gov/wp-content/uploads/"
COUNCIL_PAGES = ["performance-oversight-2024", "performance-oversight-2025", "performance-oversight-2026",
                 "budget-oversight-2025", "budget-oversight-2027", "human-services-11", "human-services-12",
                 "human-services-13", "human-services-14", "housing-3", "housing-5", "housing-6", "housing-7",
                 "housing-8", "health-14", "health-15", "health-16", "health-17", "judiciary-public-safety-9",
                 "judiciary-public-safety-10", "judiciary-public-safety-11", "judiciary-public-safety-12"]
# (cycle, agency, doc type, path under wp-content/uploads, large?)
COUNCIL_DOCS = [
    # performance oversight (pre-hearing responses)
    ("POH2024", "DHS", "responses", "2024/08/Pre-Hearing-Responses-DHS-02.28.2024.pdf", False),
    ("POH2024", "ICH", "responses", "2024/08/Pre-Hearing-Responses-ICH-02.27.2024.pdf", False),
    ("POH2024", "ICH", "attachments", "2024/08/Pre-Hearing-Attachments-ICH-02.27.2024.pdf", False),
    ("POH2024", "OVSJG", "responses", "2024/08/OVSJG-FY23-24-Oversight-Pre-Hearing-Questions_final.pdf", False),
    ("POH2024", "DBH", "responses", "2024/08/FY-23-Oversight-Pre-Hearing-Responses.-DBH_UPDATED.pdf", False),
    ("POH2025", "DHS", "responses", "2025/03/DHS-Combined-POH-Responses-3.3.2025.pdf", False),
    ("POH2025", "DHS", "attachments", "2025/03/dhsatt25.pdf", True),
    ("POH2025", "ICH", "responses", "2025/03/ICH-Response-_2025-03-04-SUBMISSION.pdf", False),
    ("POH2025", "ICH", "attachments", "2025/03/ichatt.pdf", False),
    ("POH2025", "OVSJG", "responses", "2025/04/FINAL-OVSJG-FY24-25-Prehearing-questions.pdf", False),
    ("POH2025", "DBH", "attachments", "2025/02/dbhatt.pdf", True),
    ("POH2026", "DHS", "responses", "2026/03/DHS-Responses-to-Pre-FY25-POH-Questions-FINAL.pdf", False),
    ("POH2026", "OVSJG", "responses", "2026/03/OVSJG-POH-FY25-26-Responses.pdf", False),
    ("POH2026", "OVSJG", "attachments", "2026/03/ovsjgatt.pdf", False),
    ("POH2026", "DHCD", "responses", "2026/03/DHCD-Reponses-to-POH-Pre-Questions-.pdf", False),
    # budget oversight Attachment I (contracts & grants) and III (grants/federal payments)
    ("BO_FY24", "JA0", "att_I_contracts_grants", "2023/03/JA0_FY24_Attachment-I.pdf", False),
    ("BO_FY24", "FO0", "att_I_contracts_grants", "2023/03/FO0_FY24_Attachment-I.pdf", False),
    ("BO_FY24", "RM0", "att_I_contracts_grants", "2023/03/RM0_FY24_Attachment-I.pdf", False),
    ("BO_FY25", "JA0", "att_I_contracts_grants", "2024/04/JA0_FY25_-Attachment-I-Contracts-Grants.pdf", False),
    ("BO_FY25", "DB0", "att_I_contracts_grants", "2024/04/DB0-Attachment-I-Contracts-Grants.pdf", False),
    ("BO_FY26", "JA0", "att_I_contracts_grants", "2025/06/JA0_FY26-Attachment-I.pdf", False),
    ("BO_FY26", "JA0", "att_III_grants", "2025/06/JA0_FY26-Attachment-III-Grants-Federal-Payments-Lapses.pdf", False),
    ("BO_FY26", "FO0", "att_I_contracts_grants", "2025/06/FO0_FY26_Attachment-I.pdf", False),
    ("BO_FY26", "RM0", "att_I_contracts_grants", "2025/06/RM0_FY26_Attachment-I.pdf", False),
    ("BO_FY26", "DB0", "att_I_contracts_grants", "2025/06/DB0-Attachment-I-Contracts-Grants.pdf", False),
    ("BO_FY26", "CF0", "att_I_contracts_grants", "2025/06/CF0_FY26_-Attachment-I.pdf", False),
    ("BO_FY27", "JA0", "att_I_contracts_grants", "2026/04/JA0_FY27_Attachment-I.pdf", False),
    ("BO_FY27", "JA0", "att_III_grants", "2026/04/JA0_FY27_Attachment-III.pdf", False),
    ("BO_FY27", "FO0", "att_I_contracts_grants", "2026/04/FO0_FY27_Attachment-I.pdf", False),
    ("BO_FY27", "DB0", "att_I_contracts_grants", "2026/04/DB0_FY27_Attachment-I-Contracts-Grants.pdf", False),
    ("BO_FY27", "CF0", "att_I_contracts_grants", "2026/04/CF0_FY27_Attachment-I.pdf", False),
    ("BO_FY27", "OVSJG", "budget_prehearing_responses", "2026/05/FY27-OVSJG-Budget-Pre-Hearing-Questions_FINAL.pdf", False),
    # committee budget reports posted on dccouncil.gov
    ("BR_FY25", "Housing (DHS, DHCD, DCHA, ICH)", "committee_budget_report",
     "2024/05/Circulation-Draft-Budget-Report-Committee-on-Housing-FY25-05.08.2024.pdf", False),
    ("BR_FY25", "JPS (OVSJG)", "committee_budget_report", "2024/05/JPS-FY-25-Budget-Report-DRAFT.pdf", False),
]
OB = "https://www.dccouncilbudget.com"
OB_DOCS = [
    ("BR_FY26", "Human Services (DHS, ICH)", "committee_budget_report",
     "/s/Human-Services_FY26-Budget-Recommendations-and-Report-Circulation-Draft_updaetd-622pm.pdf"),
    ("BR_FY26", "Housing (DHCD, DCHA)", "committee_budget_report",
     "/s/Housing_FY26-Budget-Recommendations-and-Report-Updated-circulation-draft.pdf"),
    ("BR_FY26", "JPS (OVSJG)", "committee_budget_report", "/s/JPS_FY26-Budget-Recommendations-and-Report-Revised-Draft-624am.pdf"),
    ("BR_FY26", "Health (DBH)", "committee_budget_report", "/s/Health_FY26-Budget-Recommendations-and-Report-Revised-Draft-1.pdf"),
    ("BR_FY27", "All agencies", "council_operating_changes_chart",
     "/s/Net-Operating-Budget-Adjustments-Chart-2nd-Reading-Circulation_final_6212026.pdf"),
    ("BR_FY27", "All agencies", "lba_changes_1st_to_2nd_reading",
     "/s/LBA-Budget-Adjustments-Showing-Changes-Between-1st-and-2nd-Reading_final_6212026.pdf"),
    ("BR_FY27", "BSA", "bsa_committee_print_packet", "/s/B26-661-FY27-BSA-COMMITTEE-PACKET.pdf"),
    ("BR_FY27", "Housing (DHCD, DCHA)", "committee_budget_report", "/s/FY27-Committee-on-Housing-Budget-Report-Markup-Draft_revised.pdf"),
    ("BR_FY27", "Health (DBH)", "committee_budget_report", "/s/DRAFT-FY2027-Committee-on-Health-Budget-Recommendations-Report.pdf"),
    ("BR_FY27", "JPS (OVSJG)", "committee_budget_report", "/s/52226-FY2027-JPS-Budget-Report_DRAFT_Recirculated-with-Tables.pdf"),
]
BSA = [("FY2024", "laws/25-50"), ("FY2025", "laws/25-217"), ("FY2026", "laws/26-55"), ("FY2027_emergency", "acts/26-416")]
OVSJG_PAGE = "https://ovsjg.dc.gov/page/ovsjg-funding-recipients"


def run_council(skip_large: bool):
    sec = "14_probe_dc_hud: DC Council oversight, OVSJG lists, budget reports, BSA"
    out = SUMMARY[sec]
    # OVSJG published recipient lists FY24-FY26
    p, body = fetch(OVSJG_PAGE, "dc_gov", "ovsjg_funding_recipients_page", "html")
    if body:
        links = re.findall(r'href="([^"]+\.pdf)"[^>]*>(FY\s?2?\d+[^<]*Recipients)', body.decode("utf-8", "ignore"))
        out.append(f"- OVSJG funding-recipients page lists {len(links)} annual PDFs: {[t for _, t in links]}")
        for u, t in links:
            m = re.search(r"FY\s?(20)?(\d\d)", t)
            if m and int(m.group(2)) >= 24:
                fy = f"FY20{m.group(2)}"
                pp, b = fetch(urljoin("https://ovsjg.dc.gov", htmlmod.unescape(u)), "dc_gov",
                              f"ovsjg_funding_recipients_{fy}", "pdf", expect_pdf=True)
                if pp:
                    pages = text_profile(pp, f"OVSJG recipients {fy}", sec)
                    for ln in calvary_lines(pages, limit=6):
                        out.append(f"  - {ln}")
    register_source("doc_ovsjg_recipients", "OVSJG annual funding recipient lists (FY2016-FY2026 PDFs)", OVSJG_PAGE,
                    "DC Office of Victim Services and Justice Grants", "Public government document",
                    "FY2024-FY2026 downloaded; earlier years linked on the same page")
    # Council WP pages (discovery provenance)
    for slug in COUNCIL_PAGES:
        fetch("https://dccouncil.gov/wp-json/wp/v2/pages", "dc_council", f"wp_page_{slug}", "json",
              params={"slug": slug, "_fields": "id,link,date,title,content"})
    for cycle, ag, kind, path, large in COUNCIL_DOCS:
        if large and skip_large:
            out.append(f"- skipped (--skip-large): {cycle} {ag} {kind} {path}")
            continue
        p, body = fetch(WP + path, "dc_council", f"{cycle}_{ag}_{kind}_{Path(path).stem}"[:110], "pdf", expect_pdf=True)
        if p:
            pages = text_profile(p, f"{cycle} {ag} {kind} ({path.split('/')[-1]}, {len(body)/1e6:.1f} MB)", sec)
            for ln in calvary_lines(pages, limit=8):
                out.append(f"  - {ln}")
    for cycle, ag, kind, path in OB_DOCS:
        p, body = fetch(OB + path, "dc_council", f"{cycle}_{kind}_{Path(path).stem}"[:110], "pdf", expect_pdf=True)
        if p:
            pages = text_profile(p, f"{cycle} {ag} {kind} ({path.split('/')[-1]}, {len(body)/1e6:.1f} MB)", sec,
                                 extra={"homeless pp": BUDGET_KEYWORDS["homeless"], "PSH pp": BUDGET_KEYWORDS["PSH"]})
            for ln in calvary_lines(pages, limit=6):
                out.append(f"  - {ln}")
    for slug in ("fy-2026-budget", "fy-2027-budget"):
        fetch(f"{OB}/{slug}", "dc_council", f"council_budget_office_{slug}_page", "html")
    # Budget Support Acts (HTML full text with subtitle structure)
    for fy, path in BSA:
        p, body = fetch(f"https://code.dccouncil.gov/us/dc/council/{path}", "dc_council", f"bsa_{fy}_{path.replace('/', '_')}", "html")
        if body:
            h = body.decode("utf-8", "ignore")
            title = re.search(r"<title>([^<|]+)", h)
            subs = re.findall(r"SUBTITLE\s+[A-Z]+\.\s+([A-Z][A-Z0-9 ,'&\-\.]+)", re.sub(r"<[^>]+>", " ", h))
            rel_subs = [s.strip() for s in subs if re.search(r"HOMELESS|SHELTER|HOUSING|RENT|VICTIM|SUPPORTIVE|BEHAVIORAL|TANF|HUMAN SERV", s)]
            out.append(f"- BSA {fy} ({title.group(1).strip() if title else path}): {len(subs)} subtitles; relevant: "
                       + "; ".join(dict.fromkeys(rel_subs)))
    register_source("doc_dc_council_oversight", "DC Council performance-oversight responses and budget-oversight attachments",
                    "https://dccouncil.gov/committee-oversight/", "Council of the District of Columbia (agency submissions)",
                    "Public government document", "DHS, ICH, OVSJG, DBH, DHCD, DOES; 2024-2026 cycles; Attachment I = contracts & grants")
    register_source("doc_dc_council_budget_reports", "DC Council committee budget reports and Council Budget Office change charts",
                    f"{OB}/fy-2027-budget", "Council of the District of Columbia / Office of the Budget Director",
                    "Public government document", "FY2025 (dccouncil.gov), FY2026 and FY2027 (dccouncilbudget.com)")
    register_source("doc_dc_bsa", "DC Budget Support Acts FY2024-FY2027 (D.C. Law Library full text)",
                    "https://code.dccouncil.gov/us/dc/council/laws/26-55", "Council of the District of Columbia",
                    "Public law text", "Laws 25-50, 25-217, 26-55; Act 26-416 (FY2027 emergency)")


# ---------------------------------------------------------------- 4. HUD / MWCOG
AHAR25 = "https://www.huduser.gov/portal/datasets/ahar/2025-ahar-part-1-pit-estimates-of-homelessness-in-the-us.html"
HUDX = "https://files.hudexchange.info/reports/published/"
HUDGOV = "https://www.hud.gov/sites"
MWCOG_DOC = ("https://www.mwcog.org/documents/2026/05/13/homelessness-in-metropolitan-washington-results-and-"
             "analysis-from-the-annual-point-in-time-pit-count-of-persons-experiencing-homelessness-featured-"
             "publications-homelessness/")


def run_hud():
    sec = "14_probe_dc_hud: HUD CoC / PIT / HIC and MWCOG"
    out = SUMMARY[sec]
    p, body = fetch(AHAR25, "hud", "huduser_ahar_2025_part1_page", "html", ua=HUDUSER_UA)
    files = []
    if body:
        files = re.findall(r'href="(/portal/sites/default/files/xls/[^"]+)"', body.decode("utf-8", "ignore"))
        out.append(f"- AHAR 2025 Part 1 page data files: {[f.split('/')[-1] for f in files]}")
    for f in files:
        if re.search(r"(PIT-Counts-by-CoC|HIC-Counts-by-CoC)", f):
            fn = f.split("/")[-1]
            pp, b = fetch(urljoin("https://www.huduser.gov", f), "hud", f"huduser_{fn.rsplit('.', 1)[0]}",
                          fn.rsplit(".", 1)[1], ua=HUDUSER_UA)
            if pp:
                try:
                    import pandas as pd
                    eng = "pyxlsb" if fn.endswith(".xlsb") else "openpyxl"
                    xl = pd.ExcelFile(pp, engine=eng)
                    sheets = xl.sheet_names
                    latest = sheets[0] if sheets else None
                    df = xl.parse(latest, header=0) if latest else None
                    dc = df[df.iloc[:, 0].astype(str).str.startswith("DC-500")] if df is not None else None
                    want = ["Overall Homeless", "Sheltered ES Homeless", "Sheltered TH Homeless", "Unsheltered Homeless",
                            "Overall Homeless Individuals", "Overall Chronically Homeless Individuals",
                            "Total Year-Round Beds (ES, TH, SH)", "Total Year-Round Beds (TH)",
                            "Total Year-Round Beds (PSH)", "Total Year-Round Beds (RRH)"]
                    cols = [c for c in want if df is not None and c in df.columns]
                    vals = {c: dc[c].iloc[0] for c in cols} if dc is not None and len(dc) else {}
                    gender = {}
                    for sh in sheets[:2]:
                        gcols = [c for c in xl.parse(sh, nrows=1).columns if re.search(r"Wom[ae]n|Female", str(c))]
                        gender[sh] = len(gcols)
                    vals["gender_columns_by_sheet"] = gender
                    out.append(f"- {fn}: {len(sheets)} sheets ({sheets[0]}..{sheets[-1]}); DC-500 rows in '{latest}': "
                               f"{0 if dc is None else len(dc)}; {vals}")
                except Exception as e:
                    out.append(f"- {fn}: downloaded; read failed {type(e).__name__}: {e}"[:200])
    register_source("bulk_hud_ahar_pit_hic", "HUD AHAR 2025 Part 1: PIT and HIC counts by CoC, 2007-2025", AHAR25,
                    "HUD Office of Policy Development and Research (HUD User)", "Public domain (U.S. Government work)",
                    "2007-2025-PIT-Counts-by-CoC.xlsb (one sheet per year) and 2007-2025-HIC-Counts-by-CoC.xlsx")
    # CoC award reports (CoC-level project lists)
    for y in range(2019, 2025):
        pp, b = fetch(f"{HUDX}CoC_AwardComp_CoC_DC-500-{y}_DC_{y}.pdf", "hud", f"hudx_CoC_AwardComp_DC-500_{y}", "pdf", expect_pdf=True)
        if pp:
            pages = pdf_pages_text(pp)
            tot = re.search(r"Total Award:\s*\$?([\d,]+)", " ".join(pages))
            out.append(f"- AwardComp DC-500 {y}: total ${tot.group(1) if tot else '?'}; Calvary lines: "
                       + " | ".join(calvary_lines(pages, 140, 8)))
    pp, b = fetch(f"{HUDGOV}/dfiles/CPD/documents/CoC/CoC-2024-DC_Press.pdf", "hud", "hudgov_CoC-2024-DC_Press", "pdf", expect_pdf=True)
    if pp:
        out.append("- hud.gov FY2024 DC award report: " + " | ".join(calvary_lines(pdf_pages_text(pp), 120, 8)))
    for r, path in [(1, "/default/files/OCHCO/documents/ALL-Press-Round-1.pdf"), (2, "/default/files/OCHCO/documents/ALL_Press_Round_2.pdf"),
                    (3, "/default/files/OCHCO/documents/ALL-Press-Round-3.pdf")]:
        pp, b = fetch(HUDGOV + path, "hud", f"hudgov_FY2025_CoC_award_round{r}", "pdf", expect_pdf=True)
        if pp:
            pages = pdf_pages_text(pp)
            dc = page_hits(pages, re.compile(r"DC-500|District of Columbia CoC"))
            out.append(f"- FY2025 CoC award announcement round {r}: {len(pages)} pp; DC-500 pages {compress(dc)}; Calvary: "
                       + (" | ".join(calvary_lines(pages, 120, 6)) or "none"))
    for fy in (2024, 2026):
        pp, b = fetch(f"{HUDGOV}/dfiles/CPD/documents/CoC/FY-{fy}-DC-500-GIW.xlsx", "hud", f"hudgov_FY{fy}_DC-500_GIW", "xlsx")
        if pp:
            try:
                import pandas as pd
                xl = pd.ExcelFile(pp, engine="openpyxl")
                hits = []
                for sh in xl.sheet_names:
                    df = xl.parse(sh, header=None)
                    for _, row in df.iterrows():
                        line = " | ".join(str(v) for v in row.tolist() if pd.notna(v) and str(v).strip())
                        if CALVARY_RE.search(line):
                            hits.append(line[:160])
                out.append(f"- FY{fy} DC-500 GIW: sheets {xl.sheet_names}; Calvary rows {len(hits)}: " + " || ".join(hits[:6]))
            except Exception as e:
                out.append(f"- FY{fy} DC-500 GIW read failed: {e}"[:200])
    register_source("doc_hud_coc_awards", "HUD CoC Program awards for DC-500 (HUD Exchange award reports, hud.gov award reports, GIWs)",
                    "https://www.hudexchange.info/programs/coc/awards-by-cocs/", "HUD Office of Community Planning and Development",
                    "Public domain (U.S. Government work)",
                    "AwardComp 2019-2024 (project rows: recipient | project | type | amount); FY2024 DC press report; FY2025 award rounds 1-3; FY2024/FY2026 GIW")
    # HIC (project-level) and PopSub reports
    for y in (2022, 2023, 2024, 2025):
        pp, b = fetch(f"{HUDX}CoC_HIC_CoC_DC-500-{y}_DC_{y}.pdf", "hud", f"hudx_CoC_HIC_DC-500_{y}", "pdf", expect_pdf=True)
        if pp:
            pages = pdf_pages_text(pp)
            out.append(f"- HIC DC-500 {y}: {len(pages)} pp; Calvary rows: " + " | ".join(calvary_lines(pages, 130, 10)))
    for y in (2024, 2025):
        pp, b = fetch(f"{HUDX}CoC_PopSub_CoC_DC-500-{y}_DC_{y}.pdf", "hud", f"hudx_CoC_PopSub_DC-500_{y}", "pdf", expect_pdf=True)
        if pp:
            out.append(f"- PopSub DC-500 {y}: {len(pdf_pages_text(pp))} pp")
    register_source("doc_hud_hic_dc500", "HUD CoC Housing Inventory Count and Population/Subpopulation reports, DC-500",
                    "https://www.hudexchange.info/programs/coc/coc-housing-inventory-count-reports/",
                    "HUD Office of Community Planning and Development", "Public domain (U.S. Government work)",
                    "HIC 2022-2025 (project-level provider/facility/bed rows); PopSub 2024-2025")
    # MWCOG
    p, body = fetch(MWCOG_DOC, "hud", "mwcog_pit_reports_page", "html")
    if body:
        h = body.decode("utf-8", "ignore")
        links = [(htmlmod.unescape(u), " ".join(htmlmod.unescape(re.sub("<[^>]+>", " ", t)).split()))
                 for u, t in re.findall(r'<a[^>]+href="(/file\.aspx[^"]+)"[^>]*>(.*?)</a>', h, re.S)]
        out.append(f"- MWCOG report page lists {len(links)} annual reports")
        for u, t in links:
            m = re.search(r"(20\d\d) Point-in-Time", t)
            if m and int(m.group(1)) >= 2023:
                pp, b = fetch(urljoin("https://www.mwcog.org", u), "hud", f"mwcog_homelessness_metro_washington_{m.group(1)}_PIT",
                              "pdf", expect_pdf=True)
                if pp:
                    text_profile(pp, f"MWCOG {m.group(1)} PIT report ({len(b)/1e6:.1f} MB)", sec,
                                 extra={"DC pages": re.compile(r"District of Columbia", re.I),
                                        "ward pp": re.compile(r"\bWard\s+[1-8]\b")})
    register_source("doc_mwcog_pit", "MWCOG Homelessness in Metropolitan Washington (annual PIT report)", MWCOG_DOC,
                    "Metropolitan Washington Council of Governments", "Public document; cite MWCOG",
                    "2023-2026 reports downloaded; 2007-2022 linked on the same page")


# ---------------------------------------------------------------- 5. probe-only sources (no data pulled)
PROBE_ONLY = [
    ("web_ocp_transparency_portal", "dc_gov", "ocp_transparency_portal", "https://contracts.ocp.dc.gov/contracts/search",
     "DC OCP Contracts and Procurement Transparency Portal", "DC Office of Contracting and Procurement",
     "JavaScript single-page app over the PASS data exposed as DC GIS layers 16/17/37; use api_dcgis_pass instead"),
    ("web_dc_grants_clearinghouse", "dc_gov", "moca_community_grant_program", "https://communityaffairs.dc.gov/content/community-grant-program",
     "DC grants clearinghouse (Mayor's Office of Community Affairs / Serve DC; formerly OPGS)", "DC Mayor's Office of Community Affairs",
     "funding-opportunity notices only; no award amounts; opgs.dc.gov redirects here"),
    ("web_tcp_ich", "hud", "tcp_homelessness_in_dc", "https://community-partnership.org/homelessness-in-dc/",
     "The Community Partnership (DC CoC lead / DHS intermediary) and DC ICH public pages", "The Community Partnership for the Prevention of Homelessness; DC ICH",
     "no provider-level bed or funding tables published; use HUD HIC reports and Council oversight responses"),
    ("web_tcp_ich", "hud", "ich_pit_release", "https://ich.dc.gov/release/mayor-bowser-releases-annual-point-time-count-results",
     None, None, None),
    ("web_tcp_ich", "hud", "dcpit_hub_search", "https://www.dcpit.org/api/search/v1/collections/all/items?limit=50", None, None, None),
]
LIMS_API = "https://lims.dccouncil.gov/api/v2/PublicData/LegislationDetails/B26-0661"


def run_misc():
    sec = "14_probe_dc_hud: probe-only sources"
    out = SUMMARY[sec]
    for sid, src, desc, url, name, pub, notes in PROBE_ONLY:
        p, body = fetch(url, src, f"probe_{desc}", "json" if "/api/" in url else "html")
        out.append(f"- {desc}: {'HTTP 200, ' + format(len(body), ',') + ' B' if body else 'failed'} ({url})")
        if name:
            register_source(sid, name, url, pub, "Public web page", notes)
    RL.wait()
    r = S.get(LIMS_API, timeout=60)
    out.append(f"- DC Council LIMS API v2 ({LIMS_API}): HTTP {r.status_code} '{r.text[:60]}' (token required; not used)")
    register_source("api_dc_lims", "DC Council LIMS public data API (v2)", "https://lims.dccouncil.gov/api/v2/PublicData/",
                    "Council of the District of Columbia", "Public data; token required",
                    f"probe only: HTTP {r.status_code} without token; no data pulled")


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="dcgis,budget,council,hud,misc")
    ap.add_argument("--skip-large", action="store_true")
    a = ap.parse_args()
    groups = [g.strip() for g in a.only.split(",") if g.strip()]
    if "dcgis" in groups:
        run_dcgis()
    if "budget" in groups:
        run_budget()
    if "council" in groups:
        run_council(a.skip_large)
    if "hud" in groups:
        run_hud()
    if "misc" in groups:
        run_misc()
    for sec, lines in SUMMARY.items():
        log(sec, "\n".join(lines))
        print(f"\n### {sec}\n" + "\n".join(lines))
    tot = sum(BYTES.values())
    tail = (f"- bytes saved this run: " + ", ".join(f"raw/{k} {v/1e6:,.1f} MB" for k, v in sorted(BYTES.items()))
            + f"; total {tot/1e6:,.1f} MB\n- failures ({len(FAILS)}): " + ("; ".join(FAILS) if FAILS else "none"))
    log("14_probe_dc_hud: run summary", tail)
    print("\n" + tail)


if __name__ == "__main__":
    main()
