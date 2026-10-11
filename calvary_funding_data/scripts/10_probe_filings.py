"""Phase 2 recon, area "filings": probe filing data sources and download Phase 3/4 reference files.

Sections (run all, or pick with --only):
  bmf        IRS EO BMF state files (DC, MD, VA) + national region files eo1-eo4 -> raw/irs_bmf/
  irs_index  IRS Form 990 XML index CSVs, release years 2021-2026 -> raw/irs_xml_index/
  propublica ProPublica Nonprofit Explorer API v2: org, search filters, pagination cap, rate behavior
  gt         GivingTuesday 990 Data Infrastructure API + data lake; Calvary's GT XMLs -> raw/xml/gt/
  gt_marts   GivingTuesday bulk data marts listing (no download)
  remotezip  HTTP range-read test on an IRS batch ZIP; Calvary TY2023/TY2024 member -> raw/xml/irs/
  soi        IRS SOI annual extract: list files, download latest 990 + 990-PF extracts -> raw/irs_soi/
  pages      Save NCCS and Charity Navigator reference pages -> raw/web_filings/
  volume     Phase 4 volume estimate: IRS index x DMV BMF

Usage: .venv/bin/python scripts/10_probe_filings.py [--only bmf,irs_index,...] [--refresh]
Run remotezip and volume in the same invocation (volume uses the remotezip compression ratio).
Large reference downloads are skipped if a raw copy already exists, unless --refresh.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import statistics
import struct
import sys
import time
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from remotezip import RemoteFetcher, RemoteZip

from lib.common import (RAW, RateLimiter, log, norm_ein, raw_path, register_source, rel, save_raw,
                        session, sha256_file)

CALVARY = "521307706"
IRS_XML = "https://apps.irs.gov/pub/epostcard/990/xml"
IRS_SOI = "https://www.irs.gov/pub/irs-soi"
INDEX_YEARS = list(range(2021, 2027))
BMF_FILES = ["eo_dc.csv", "eo_md.csv", "eo_va.csv", "eo1.csv", "eo2.csv", "eo3.csv", "eo4.csv"]
PP = "https://projects.propublica.org/nonprofits/api/v2"
GT = "https://990-infrastructure.gtdata.org"
GT_S3 = "https://gt990datalake-rawdata.s3.amazonaws.com"

csv.field_size_limit(1 << 30)
REFRESH = False
S = session()


# ---------------------------------------------------------------- helpers
def existing_raw(source: str, desc: str, ext: str) -> Path | None:
    """Most recent raw/{source}/*_{desc}.{ext}, if any."""
    d = RAW / source
    hits = sorted(d.glob(f"*_{desc}.{ext}")) if d.exists() else []
    return hits[-1] if hits else None


def download(url: str, source: str, desc: str, ext: str) -> tuple[Path, bool]:
    """Stream a file untouched into raw/. Returns (path, downloaded_now)."""
    old = existing_raw(source, desc, ext)
    if old and not REFRESH:
        return old, False
    p = raw_path(source, desc, ext)
    with S.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        with open(p, "wb") as f:
            for chunk in r.iter_content(1 << 20):
                f.write(chunk)
    return p, True


def mb(n: float) -> str:
    return f"{n / 1e6:,.1f} MB"


def head(url: str, follow: bool = True) -> dict:
    r = S.head(url, allow_redirects=follow, timeout=60)
    return {"status": r.status_code, "bytes": int(r.headers.get("Content-Length", 0) or 0),
            "last_modified": r.headers.get("Last-Modified", ""), "final_url": r.url}


def read_index(year: int) -> list[dict]:
    p = existing_raw("irs_xml_index", f"index_{year}", "csv")
    if not p:
        raise SystemExit(f"index_{year}.csv not downloaded; run --only irs_index")
    with open(p, newline="", encoding="utf-8", errors="replace") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["_release_year"] = year
    return rows


def read_bmf(name: str) -> list[dict]:
    p = existing_raw("irs_bmf", name.replace(".csv", ""), "csv")
    if not p:
        raise SystemExit(f"{name} not downloaded; run --only bmf")
    with open(p, newline="", encoding="utf-8", errors="replace") as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------- BMF
def sec_bmf():
    register_source("bulk_irs_eo_bmf", "IRS Exempt Organizations Business Master File Extract (EO BMF)",
                    "https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf",
                    "Internal Revenue Service", "US government work, public domain",
                    "State files eo_dc/eo_md/eo_va.csv and region files eo1-eo4.csv from www.irs.gov/pub/irs-soi/. "
                    "Monthly refresh; one row per EIN.")
    lines, stats = [], {}
    doc, _ = download(f"{IRS_SOI}/eo-info.pdf", "irs_bmf", "eo-info", "pdf")  # field + code definitions
    lines.append(f"- documentation: {rel(doc)}")
    for name in BMF_FILES:
        p, new = download(f"{IRS_SOI}/{name}", "irs_bmf", name.replace(".csv", ""), "csv")
        rows = read_bmf(name)
        fnd = Counter(r.get("FOUNDATION", "") for r in rows)
        pf_found = sum(fnd[c] for c in ("02", "03", "04"))
        pf_req = sum(1 for r in rows if r.get("PF_FILING_REQ_CD") == "1")
        sub03 = sum(1 for r in rows if r.get("SUBSECTION") == "03")
        stats[name] = {"rows": len(rows), "bytes": p.stat().st_size, "foundation_02_03_04": pf_found,
                       "pf_filing_req_cd_1": pf_req, "subsection_03": sub03,
                       "sha256": sha256_file(p), "file": rel(p)}
        lines.append(f"- {name}: {len(rows):,} rows, {mb(p.stat().st_size)}, subsection 03 {sub03:,}, "
                     f"FOUNDATION 02/03/04 {pf_found:,}, PF_FILING_REQ_CD=1 {pf_req:,} "
                     f"({'downloaded' if new else 'reused'} {rel(p)})")
    cols = list(read_bmf("eo_dc.csv")[0].keys())
    cal = [r for r in read_bmf("eo_dc.csv") if r["EIN"] == CALVARY]
    lines.append(f"- columns ({len(cols)}): {', '.join(cols)}")
    lines.append(f"- Calvary row: {json.dumps({k: cal[0][k] for k in ('NAME', 'SUBSECTION', 'FOUNDATION', 'NTEE_CD', 'RULING', 'TAX_PERIOD', 'ASSET_AMT', 'INCOME_AMT', 'REVENUE_AMT', 'FILING_REQ_CD', 'PF_FILING_REQ_CD', 'ACCT_PD')}) if cal else 'NOT FOUND'}")
    # DMV PF filer counts, both definitions, and the overlap
    dmv = [r for n in ("eo_dc.csv", "eo_md.csv", "eo_va.csv") for r in read_bmf(n)]
    a = {r["EIN"] for r in dmv if r.get("FOUNDATION") in ("02", "03", "04")}
    b = {r["EIN"] for r in dmv if r.get("PF_FILING_REQ_CD") == "1"}
    lines.append(f"- DC+MD+VA: {len(dmv):,} rows; FOUNDATION 02/03/04 = {len(a):,} EINs; PF_FILING_REQ_CD=1 = "
                 f"{len(b):,}; both = {len(a & b):,}; either = {len(a | b):,}")
    log("10_probe_filings: bmf", "\n".join(lines))
    print("\n".join(lines))
    return stats


# ---------------------------------------------------------------- IRS XML index
def sec_irs_index():
    register_source("bulk_irs_xml_index", "IRS Form 990 Series e-file XML index files (index_{YEAR}.csv)",
                    "https://www.irs.gov/charities-non-profits/form-990-series-downloads",
                    "Internal Revenue Service", "US government work, public domain",
                    f"Release years {INDEX_YEARS[0]}-{INDEX_YEARS[-1]} from {IRS_XML}/{{YEAR}}/index_{{YEAR}}.csv. "
                    "Maps EIN to OBJECT_ID, TAX_PERIOD, RETURN_TYPE and (2023+) XML_BATCH_ID.")
    register_source("bulk_irs_xml", "IRS Form 990 Series e-file XML batch ZIPs",
                    "https://www.irs.gov/charities-non-profits/form-990-series-downloads",
                    "Internal Revenue Service", "US government work, public domain",
                    f"{IRS_XML}/{{YEAR}}/{{XML_BATCH_ID}}.zip; members are {{OBJECT_ID}}_public.xml. "
                    "Range requests supported, so single members can be read with remotezip.")
    lines = []
    for y in INDEX_YEARS:
        p, new = download(f"{IRS_XML}/{y}/index_{y}.csv", "irs_xml_index", f"index_{y}", "csv")
        rows = read_index(y)
        cols = [c for c in rows[0].keys() if not c.startswith("_")]
        rt = Counter(r.get("RETURN_TYPE", "") for r in rows)
        batches = Counter(r.get("XML_BATCH_ID", "") for r in rows)
        tp = Counter((r.get("TAX_PERIOD") or "")[:4] for r in rows)
        lines.append(f"- index_{y}.csv: {len(rows):,} rows, {mb(p.stat().st_size)}, sha256 {sha256_file(p)[:12]}, "
                     f"{'downloaded' if new else 'reused'} {rel(p)}\n"
                     f"  - columns: {', '.join(cols)}\n"
                     f"  - RETURN_TYPE: {dict(rt.most_common())}\n"
                     f"  - XML_BATCH_ID values: {len(batches)} ({', '.join(sorted(b or '(blank)' for b in batches))[:400]})\n"
                     f"  - TAX_PERIOD year: {dict(sorted(tp.items()))}")
    cal = []
    for y in INDEX_YEARS:
        cal += [r for r in read_index(y) if norm_ein(r.get("EIN")) == CALVARY]
    lines.append("- Calvary rows (all release years):")
    for r in sorted(cal, key=lambda r: r["TAX_PERIOD"]):
        lines.append("  - " + json.dumps({k: v for k, v in r.items() if k in (
            "_release_year", "RETURN_ID", "TAX_PERIOD", "SUB_DATE", "RETURN_TYPE", "OBJECT_ID",
            "XML_BATCH_ID", "DLN", "FILING_TYPE")}))
    log("10_probe_filings: irs_index", "\n".join(lines))
    print("\n".join(lines))
    return cal


# ---------------------------------------------------------------- ProPublica
class Timed:
    """No-retry session so 429s are visible; records status, latency and CDN cache status."""

    def __init__(self, per_sec: float):
        import requests
        self.s = requests.Session()
        self.s.headers.update(S.headers)
        self.rl = RateLimiter(per_sec)
        self.lat, self.codes, self.cache = [], Counter(), Counter()

    def get(self, url, **kw):
        self.rl.wait()
        t0 = time.monotonic()
        r = self.s.get(url, timeout=60, **kw)
        self.lat.append(time.monotonic() - t0)
        self.codes[r.status_code] += 1
        self.cache[r.headers.get("cf-cache-status", "-")] += 1
        if r.status_code == 429:
            time.sleep(10)
        return r

    def summary(self) -> str:
        if not self.lat:
            return "no requests"
        q = sorted(self.lat)
        return (f"{len(q)} requests, status {dict(self.codes)}, cf-cache-status {dict(self.cache)}, "
                f"latency median {statistics.median(q):.2f}s p90 {q[int(len(q) * .9) - 1]:.2f}s max {q[-1]:.2f}s")


def sec_propublica():
    register_source("api_propublica", "ProPublica Nonprofit Explorer API v2", PP + "/", "ProPublica",
                    "Cite ProPublica Nonprofit Explorer (https://projects.propublica.org/nonprofits/). "
                    "Underlying data: IRS EO BMF, IRS SOI annual extract, IRS e-file.",
                    "Keyless JSON. /organizations/{ein}.json and /search.json (q, state[id], ntee[id], c_code[id], page).")
    t = Timed(2.0)
    lines = []
    # org endpoint
    r = t.get(f"{PP}/organizations/{CALVARY}.json")
    save_raw("propublica", f"org_{CALVARY}", r.content, "json")
    org = r.json()
    fw, fwo = org["filings_with_data"], org["filings_without_data"]
    lines.append(f"- org {CALVARY}: HTTP {r.status_code}; filings_with_data {len(fw)} "
                 f"(tax_prd {min(f['tax_prd'] for f in fw)}-{max(f['tax_prd'] for f in fw)}); "
                 f"filings_without_data {len(fwo)} (tax_prd {sorted(f['tax_prd'] for f in fwo)}); "
                 f"latest_object_id {org['organization'].get('latest_object_id')}; "
                 f"org.tax_period {org['organization'].get('tax_period')}; data_source {org['organization'].get('data_source')}")
    lines.append(f"- per-filing fields ({len(fw[0])}): {', '.join(sorted(fw[0]))}")
    lines.append("- Calvary series (tax_prd -> totrevenue / totfuncexpns / totassetsend): " + "; ".join(
        f"{f['tax_prd']}: {f.get('totrevenue')} / {f.get('totfuncexpns')} / {f.get('totassetsend')}"
        for f in sorted(fw, key=lambda f: f["tax_prd"])))
    lines.append(f"- object_id keys in filings: {[k for k in fw[0] if 'object' in k.lower()] or 'none'}; "
                 f"pdf_url present on {sum(1 for f in fw if f.get('pdf_url'))}/{len(fw)}")

    # search filters + pagination cap
    probes = [
        ("search_dc_ntee5_p0", {"state[id]": "DC", "ntee[id]": "5"}),
        ("search_dc_ntee5_c3_p0", {"state[id]": "DC", "ntee[id]": "5", "c_code[id]": "3"}),
        ("search_md_ntee5_c3_p0", {"state[id]": "MD", "ntee[id]": "5", "c_code[id]": "3"}),
        ("search_va_ntee5_c3_p0", {"state[id]": "VA", "ntee[id]": "5", "c_code[id]": "3"}),
        ("search_dc_all_p0", {"state[id]": "DC"}),
        ("search_dc_all_p399", {"state[id]": "DC", "page": "399"}),
        ("search_dc_all_p400", {"state[id]": "DC", "page": "400"}),
        ("search_q_calvary_dc", {"q": "calvary", "state[id]": "DC"}),
        ("search_q_women_dc_ntee5_c3", {"q": "women", "state[id]": "DC", "ntee[id]": "5", "c_code[id]": "3"}),
    ]
    for desc, params in probes:
        r = t.get(f"{PP}/search.json", params=params)
        save_raw("propublica", desc, r.content, "json")
        d = r.json()
        lines.append(f"- {desc}: HTTP {r.status_code}, total_results {d.get('total_results')}, "
                     f"num_pages {d.get('num_pages')}, returned {len(d.get('organizations', []))}"
                     + (f", error '{d['error']}'" if d.get("error") else ""))
    rec = json.loads(existing_raw("propublica", "search_dc_ntee5_p0", "json").read_text())["organizations"][0]
    lines.append(f"- search record fields: {', '.join(rec)} (no financials; per-org call needed)")

    # page through ALL DC human services (ntee 5) orgs, all subsections
    first = json.loads(existing_raw("propublica", "search_dc_ntee5_p0", "json").read_text())
    eins, n_pages = {o["ein"] for o in first["organizations"]}, first["num_pages"]
    for page in range(1, n_pages + 1):
        r = t.get(f"{PP}/search.json", params={"state[id]": "DC", "ntee[id]": "5", "page": str(page)})
        save_raw("propublica", f"search_dc_ntee5_p{page}", r.content, "json")
        eins |= {o["ein"] for o in r.json().get("organizations", [])}
    lines.append(f"- paged DC ntee[id]=5 pages 0..{n_pages}: {len(eins):,} distinct EINs vs total_results "
                 f"{first['total_results']:,}")

    # a few org calls (cold cache) incl. two DC foundations, to see 990-PF filing fields
    for ein in ("530241716", "526036989", "520781600"):
        r = t.get(f"{PP}/organizations/{ein}.json")
        save_raw("propublica", f"org_{ein}", r.content, "json")
        if r.ok:
            d = r.json()
            f0 = (d.get("filings_with_data") or [{}])[0]
            lines.append(f"- org {ein} ({d['organization'].get('name')}): {len(d.get('filings_with_data', []))} with data, "
                         f"latest tax_prd {f0.get('tax_prd')}, formtype {f0.get('formtype')}, {len(f0)} fields")
        else:
            lines.append(f"- org {ein}: HTTP {r.status_code}")

    # XML link
    r = t.get("https://projects.propublica.org/nonprofits/download-xml",
              params={"object_id": org["organization"].get("latest_object_id")})
    meta = {"url": r.url, "status": r.status_code, "headers": {k: v for k, v in r.headers.items()
            if k.lower() in ("content-type", "cf-mitigated", "server", "content-length")}}
    save_raw("propublica", "download_xml_probe_meta", meta, "json")
    lines.append(f"- download-xml?object_id=...: HTTP {r.status_code}, cf-mitigated={r.headers.get('cf-mitigated')} "
                 "(Cloudflare browser challenge; not scriptable)")
    lines.append(f"- rate: {t.summary()}")
    log("10_probe_filings: propublica", "\n".join(lines))
    print("\n".join(lines))


# ---------------------------------------------------------------- GivingTuesday
GT_ENDPOINTS = ["efilexml", "990basic120fields", "bmf", "postcard", "pub78-deductible", "revoked"]


def s3_list(bucket_url: str, prefix: str, delimiter: str = "") -> list[dict]:
    out, token = [], None
    while True:
        params = {"list-type": "2", "prefix": prefix, "max-keys": "1000"}
        if delimiter:
            params["delimiter"] = delimiter
        if token:
            params["continuation-token"] = token
        r = S.get(bucket_url + "/", params=params, timeout=60)
        r.raise_for_status()
        save_raw("gt", f"s3_list_{prefix.replace('/', '_')}{'_' + str(len(out)) if out else ''}", r.content, "xml")
        out += [{"key": k, "modified": m, "bytes": int(s)} for k, m, s in
                re.findall(r"<Key>(.*?)</Key><LastModified>(.*?)</LastModified>.*?<Size>(\d+)</Size>", r.text)]
        m = re.search(r"<NextContinuationToken>(.*?)</NextContinuationToken>", r.text)
        if not m:
            return out
        token = m.group(1)


def sec_gt():
    register_source("api_gt_efilexml", "GivingTuesday 990 Data Infrastructure API: efilexml index",
                    f"{GT}/irs-data/efilexml?ein={{ein}}", "GivingTuesday Data Commons",
                    "GivingTuesday 990 Data Infrastructure; see https://990data.givingtuesday.org/data-use-license/",
                    "Keyless; 300 requests / 5 minutes. Index rows carry S3 URLs to raw IRS XML.")
    register_source("api_gt_990basic", "GivingTuesday 990 Data Infrastructure API: 990basic120fields",
                    f"{GT}/irs-data/990basic120fields?ein={{ein}}", "GivingTuesday Data Commons",
                    "GivingTuesday 990 Data Infrastructure; see https://990data.givingtuesday.org/data-use-license/",
                    "Keyless; one EIN per call; ~120 Form 990 header/Part I/VIII/IX fields per return.")
    register_source("api_gt_bmf", "GivingTuesday 990 Data Infrastructure API: bmf, postcard, pub78-deductible, revoked",
                    f"{GT}/irs-data/bmf?ein={{ein}}", "GivingTuesday Data Commons",
                    "GivingTuesday 990 Data Infrastructure; see https://990data.givingtuesday.org/data-use-license/",
                    "Keyless; one EIN per call. Mirrors IRS BMF, 990-N, Pub 78, revocations.")
    register_source("bulk_gt_datalake", "GivingTuesday 990 Data Lake (S3 gt990datalake-rawdata)",
                    GT_S3, "GivingTuesday Data Commons",
                    "GivingTuesday 990 Data Infrastructure; see https://990data.givingtuesday.org/data-use-license/",
                    "Anonymous S3 (no-sign-request). EfileData/XmlFiles/{OBJECT_ID}_public.xml, Indices/990xmls/, "
                    "EfileData/XmlZips mirror of IRS ZIPs, EfileData/Extracts mirror of SOI extracts.")
    t = Timed(0.9)  # 300 / 5 min = 1/s
    lines = []
    res = {}
    for ep in GT_ENDPOINTS:
        r = t.get(f"{GT}/irs-data/{ep}", params={"ein": CALVARY})
        save_raw("gt", f"{ep}_{CALVARY}", r.content, "json")
        body = r.json().get("body", {}) if r.ok else {}
        res[ep] = body.get("results", [])
        lines.append(f"- irs-data/{ep}?ein={CALVARY}: HTTP {r.status_code}, no_results {body.get('no_results')}")
    # behavior probes
    for desc, path, params in [
        ("docs_path_irs_data_underscore", "irs_data/efilexml", {"ein": CALVARY}),
        ("no_ein", "irs-data/990basic120fields", {}),
        ("state_filter_only", "irs-data/990basic120fields", {"state": "DC"}),
        ("two_eins_comma", "irs-data/990basic120fields", {"ein": f"{CALVARY},530241716"}),
        ("taxyear_param_ignored", "irs-data/990basic120fields", {"ein": CALVARY, "taxyear": "2021"}),
        ("undocumented_990pf", "irs-data/990pf", {"ein": CALVARY}),
    ]:
        r = t.get(f"{GT}/{path}", params=params)
        save_raw("gt", f"probe_{desc}", r.content, "json")
        try:
            j = r.json()
            b = j.get("body", j)
            note = b.get("error") or b.get("message") or f"no_results {b.get('no_results')}"
        except ValueError:
            note = r.text[:80]
        lines.append(f"- probe {desc} ({path} {params}): HTTP {r.status_code}, {str(note)[:120]}")

    ex = res["efilexml"]
    lines.append(f"- efilexml TaxYear set: {sorted(x['TaxYear'] for x in ex)}; IndexedOn max "
                 f"{max(x['IndexedOn'] for x in ex)}; columns: {', '.join(ex[0])}")
    b120 = res["990basic120fields"]
    lines.append(f"- 990basic120fields TAXYEAR set: {sorted(x['TAXYEAR'] for x in b120)}; {len(b120[0])} columns; "
                 f"rows with URL: {sum(1 for x in b120 if x.get('URL'))}; TY2021 TOTREVCURYEA "
                 f"{[x['TOTREVCURYEA'] for x in b120 if x['TAXYEAR'] == '2021']}")
    bm = res["bmf"]
    if bm:
        lines.append(f"- bmf: Date_Released {bm[0].get('Date_Released')}, tax_period {bm[0].get('tax_period')} "
                     "(stale vs IRS BMF)")

    # download Calvary's XMLs listed by efilexml, verify sha256
    for x in sorted(ex, key=lambda x: x["TaxYear"]):
        stem = x["URL"].rsplit("/", 1)[-1].rsplit(".", 1)[0]
        desc = f"{CALVARY}_TY{x['TaxYear']}_{stem}"
        old = existing_raw("xml/gt", desc, "xml")
        if old and not REFRESH:
            p = old
        else:
            r = S.get(x["URL"], timeout=60)
            r.raise_for_status()
            p = save_raw("xml/gt", desc, r.content, "xml")
        ok = sha256_file(p) == x["FileSha256"]
        lines.append(f"- XML TY{x['TaxYear']} {x['ObjectId']} ({x['ReturnVersion']}): {p.stat().st_size:,} B, "
                     f"sha256 {'matches' if ok else 'MISMATCH'} -> {rel(p)}")

    # data lake: index listing + per-object coverage for TY2021+ (Calvary and a random sample)
    idx = s3_list(GT_S3, "Indices/990xmls/")
    yearly = [o for o in idx if "/yearly/" in o["key"] and "created_on_" in o["key"]]
    latest_stamp = max(re.search(r"created_on_(\d{4}-\d{2}-\d{2})", o["key"]).group(1) for o in yearly)
    ly = [o for o in yearly if latest_stamp in o["key"]]
    lines.append(f"- data lake Indices/990xmls/: {len(idx)} objects; latest yearly build {latest_stamp}: " +
                 ", ".join(f"{o['key'].rsplit('/', 1)[-1][:4]} {mb(o['bytes'])}" for o in ly))
    zips = s3_list(GT_S3, "EfileData/XmlZips/")
    lines.append(f"- data lake EfileData/XmlZips/: {len(zips)} ZIPs, latest modified {max(o['modified'] for o in zips)[:10]}")
    cal_idx = []
    for y in INDEX_YEARS:
        cal_idx += [r for r in read_index(y) if r["EIN"] == CALVARY]
    for r in sorted(cal_idx, key=lambda r: r["TAX_PERIOD"]):
        h = head(f"{GT_S3}/EfileData/XmlFiles/{r['OBJECT_ID']}_public.xml")
        lines.append(f"- GT S3 XmlFiles {r['OBJECT_ID']} (TAX_PERIOD {r['TAX_PERIOD']}): HTTP {h['status']}, "
                     f"{h['bytes']:,} B, Last-Modified {h['last_modified']}")
    import random
    rng = random.Random(20261010)
    cov = {}
    for y in INDEX_YEARS:
        rows = [r for r in read_index(y) if r["RETURN_TYPE"] in ("990", "990EZ", "990PF")]
        sample = rng.sample(rows, 40)
        hits = 0
        for r in sample:
            hits += head(f"{GT_S3}/EfileData/XmlFiles/{r['OBJECT_ID']}_public.xml")["status"] == 200
            time.sleep(0.1)
        cov[y] = hits
    lines.append("- GT S3 per-object coverage, random 40 990/EZ/PF rows per IRS index release year: " +
                 ", ".join(f"{y}: {h}/40" for y, h in cov.items()))
    # latest release by batch: where does GT stop?
    by_b = defaultdict(list)
    for r in read_index(INDEX_YEARS[-1]):
        if r["RETURN_TYPE"] in ("990", "990EZ", "990PF"):
            by_b[r["XML_BATCH_ID"].upper()].append(r)
    parts = []
    for b in sorted(by_b):
        sample = rng.sample(by_b[b], 8)
        hits = 0
        for r in sample:
            hits += head(f"{GT_S3}/EfileData/XmlFiles/{r['OBJECT_ID']}_public.xml")["status"] == 200
            time.sleep(0.1)
        parts.append(f"{b[-3:]} {hits}/8")
    lines.append(f"- GT S3 coverage of release {INDEX_YEARS[-1]} by batch (8 rows each): " + ", ".join(parts))
    lines.append(f"- API rate: {t.summary()}")
    log("10_probe_filings: gt", "\n".join(lines))
    print("\n".join(lines))


def sec_gt_marts():
    """List GT bulk data marts (public S3 bucket gt990datalake-analytics-and-datamarts); no downloads."""
    url = "https://gt990datalake-analytics-and-datamarts.s3.amazonaws.com"
    register_source("bulk_gt_datamarts", "GivingTuesday 990 Data Marts (S3 gt990datalake-analytics-and-datamarts)",
                    url, "GivingTuesday Data Commons",
                    "GivingTuesday 990 Data Infrastructure; see https://990data.givingtuesday.org/data-use-license/",
                    "Anonymous S3. EfileDataMarts/{YYYY_MM_DD}_All_Years_{mart}.csv; national, all years, CSV only.")
    objs = s3_list(url, "EfileDataMarts/")
    latest = {}
    for o in objs:
        m = re.match(r"EfileDataMarts/(\d{4}_\d{2}_\d{2})_(.+)$", o["key"])
        if m and (m.group(2) not in latest or m.group(1) > latest[m.group(2)][0]):
            latest[m.group(2)] = (m.group(1), o["bytes"])
    want = ("990StandardFields", "990PFStandardFields", "990EZStandardFields", "Combined_DataMart",
            "990PFPart14Grants3A", "990PFPart14Grants3B", "ScheduleIPart2Grants", "990PFPart7p1Officers",
            "990Part1Missions", "990Part3Programs")
    lines = [f"- {len(objs)} objects under EfileDataMarts/; {len(latest)} distinct marts; latest build of key marts:"]
    for name, (d, b) in sorted(latest.items()):
        if any(w in name for w in want):
            lines.append(f"  - {d} {name}: {mb(b)}")
    log("10_probe_filings: gt_marts", "\n".join(lines))
    print("\n".join(lines))


# ---------------------------------------------------------------- IRS ZIPs / remotezip
def zip_tail_stats(url: str, size: int) -> dict:
    """Read only the ZIP end records (1-2 small range requests): member count, central directory size."""
    r = S.get(url, headers={"Range": "bytes=-65558"}, timeout=60)
    tail = r.content
    i = tail.rfind(b"PK\x05\x06")
    entries, cd_size, cd_off = struct.unpack("<HII", tail[i + 10:i + 20])
    used = len(tail)
    j = tail.rfind(b"PK\x06\x07")
    if j >= 0 and (entries == 0xFFFF or cd_size == 0xFFFFFFFF or cd_off == 0xFFFFFFFF):
        (z64_off,) = struct.unpack("<Q", tail[j + 8:j + 16])
        rec = S.get(url, headers={"Range": f"bytes={z64_off}-{z64_off + 55}"}, timeout=60).content
        used += len(rec)
        entries, _, cd_size, cd_off = struct.unpack("<QQQQ", rec[24:56])
    return {"zip_bytes": size, "entries": entries, "cd_bytes": cd_size, "probe_bytes": used}


_ZIPSTATS: dict | None = None


def zip_stats() -> dict:
    """ZIP name -> status/size/members/central-directory bytes, for the downloads page + index batch ids."""
    global _ZIPSTATS
    if _ZIPSTATS is not None:
        return _ZIPSTATS
    page = S.get("https://www.irs.gov/charities-non-profits/form-990-series-downloads", timeout=60)
    save_raw("irs_xml_index", "form-990-series-downloads_page", page.content, "html")
    urls = {u.rsplit("/", 1)[-1][:-4]: (u, "page") for u in
            re.findall(r'href="(https://apps\.irs\.gov/pub/epostcard/990/xml/\d{4}/[^"]+\.zip)"', page.text)}
    for y in INDEX_YEARS:
        for b in {r.get("XML_BATCH_ID", "") for r in read_index(y)} - {""}:
            urls.setdefault(b.upper(), (f"{IRS_XML}/{y}/{b.upper()}.zip", "index_only"))
    # the page omits some live ZIPs (e.g. 2022_TEOS_XML_02A): probe {YYYY}_TEOS_XML_{MM}{A-D}
    rl = RateLimiter(5.0)
    for y in INDEX_YEARS:
        for mm in range(1, 13):
            for part in "ABCD":
                name = f"{y}_TEOS_XML_{mm:02d}{part}"
                if name in urls:
                    continue
                rl.wait()
                url = f"{IRS_XML}/{y}/{name}.zip"
                if S.head(url, allow_redirects=False, timeout=60).status_code == 200:
                    urls[name] = (url, "probe_only")
    out = {}
    for name, (url, origin) in sorted(urls.items()):
        if int(re.search(r"/xml/(\d{4})/", url).group(1)) < INDEX_YEARS[0]:
            continue
        h = head(url, follow=False)
        st = {"url": url, "origin": origin, "status": h["status"], "last_modified": h["last_modified"]}
        if h["status"] == 200 and h["bytes"]:
            st.update(zip_tail_stats(url, h["bytes"]))
        out[name] = st
    _ZIPSTATS = out
    return out


class CountingFetcher(RemoteFetcher):
    """remotezip fetcher that counts range requests and bytes received."""
    stats = {"requests": 0, "bytes": 0}

    def fetch(self, data_range, stream=False):
        pb = super().fetch(data_range, stream)
        CountingFetcher.stats["requests"] += 1
        CountingFetcher.stats["bytes"] += len(pb)
        return pb


def remote_member(zip_url: str, object_id: str) -> tuple[bytes, dict]:
    CountingFetcher.stats = {"requests": 0, "bytes": 0}
    t0 = time.monotonic()
    with RemoteZip(zip_url, session=S, fetcher=CountingFetcher) as z:
        infos = z.infolist()
        cd = dict(CountingFetcher.stats)
        info = next(i for i in infos if i.filename.rsplit("/", 1)[-1].startswith(object_id))
        data = z.read(info.filename)
    return data, {"members": len(infos), "member_name": info.filename, "member_bytes": info.file_size,
                  "compressed": info.compress_size, "cd_requests": cd["requests"], "cd_bytes": cd["bytes"],
                  "total_requests": CountingFetcher.stats["requests"], "total_bytes": CountingFetcher.stats["bytes"],
                  "seconds": round(time.monotonic() - t0, 1), "sample_name": infos[0].filename,
                  "ratio": sum(i.file_size for i in infos) / max(1, sum(i.compress_size for i in infos)),
                  "avg_uncompressed": sum(i.file_size for i in infos) / max(1, len(infos))}


def sec_remotezip():
    lines = []
    stats = zip_stats()
    ok = {k: v for k, v in stats.items() if v["status"] == 200}
    lines.append(f"- {len(stats)} ZIP names for {INDEX_YEARS[0]}-{INDEX_YEARS[-1]} (downloads page + index batch ids); "
                 f"{len(ok)} reachable (HTTP 200, Accept-Ranges); not reachable: "
                 + (", ".join(f"{k} ({v['status']}, {v['origin']})" for k, v in stats.items() if v["status"] != 200)
                    or "none"))
    by_year = defaultdict(lambda: [0, 0, 0, 0])
    for k, v in ok.items():
        y = by_year[k[:4]]
        y[0] += 1; y[1] += v["zip_bytes"]; y[2] += v["entries"]; y[3] += v["cd_bytes"]
    for y, (n, zb, ent, cdb) in sorted(by_year.items()):
        lines.append(f"  - {y}: {n} ZIPs, {zb / 1e9:,.2f} GB, {ent:,} members, central directories {mb(cdb)}")
    for k, v in ok.items():
        lines.append(f"  - {k}: {mb(v['zip_bytes'])}, {v['entries']:,} members, CD {mb(v['cd_bytes'])}, "
                     f"{v['last_modified']}, {v['origin']}")
    for y in INDEX_YEARS:
        n_idx = len(read_index(y))
        n_zip = sum(v["entries"] for k, v in ok.items() if k.startswith(f"{y}_"))
        lines.append(f"  - release {y}: index rows {n_idx:,} vs ZIP members {n_zip:,} (diff {n_zip - n_idx:+,})")
    # split batches: index says 05A, IRS posts 05A + 05B. Which part holds the 05A-labelled rows?
    for y in (2025, 2026):
        a, b = f"{y}_TEOS_XML_05A", f"{y}_TEOS_XML_05B"
        if a in ok and b in ok:
            CountingFetcher.stats = {"requests": 0, "bytes": 0}
            with RemoteZip(ok[a]["url"], session=S, fetcher=CountingFetcher) as za, \
                    RemoteZip(ok[b]["url"], session=S, fetcher=CountingFetcher) as zb:
                na = {n.rsplit("/", 1)[-1].split("_")[0] for n in za.namelist()}
                nb = {n.rsplit("/", 1)[-1].split("_")[0] for n in zb.namelist()}
            lab = {r["OBJECT_ID"] for r in read_index(y) if r.get("XML_BATCH_ID", "").upper() == a}
            lines.append(f"  - {a} vs {b}: {len(na):,} / {len(nb):,} object ids, overlap {len(na & nb):,}; index rows "
                         f"labelled {a}: {len(lab):,}, found in {a} {len(lab & na):,}, in {b} {len(lab & nb):,} "
                         f"(read {mb(CountingFetcher.stats['bytes'])} of central directory)")
            gt_hits = {}
            for part, ids in ((a, na), (b, nb)):
                sample = sorted(ids)[::max(1, len(ids) // 10)][:10]
                gt_hits[part[-3:]] = sum(head(f"{GT_S3}/EfileData/XmlFiles/{i}_public.xml")["status"] == 200
                                         for i in sample)
            lines.append(f"    - GT S3 per-object presence, 10 members each: " +
                         ", ".join(f"{k} {v}/10" for k, v in gt_hits.items()))

    # Calvary TY2024 (TAX_PERIOD 202509) via range reads
    cal = [r for r in read_index(2026) if r["EIN"] == CALVARY and r["TAX_PERIOD"] == "202509"][0]
    zname = cal["XML_BATCH_ID"].upper()
    data, st = remote_member(ok[zname]["url"], cal["OBJECT_ID"])
    stem = st["member_name"].rsplit("/", 1)[-1].rsplit(".", 1)[0]
    desc = f"{CALVARY}_TY2024_{zname}_{stem}"
    old = existing_raw("xml/irs", desc, "xml")
    p = old if old and old.read_bytes() == data else save_raw("xml/irs", desc, data, "xml")  # no duplicate copies
    zb = ok[zname]["zip_bytes"]
    gt_copy = S.get(f"{GT_S3}/EfileData/XmlFiles/{cal['OBJECT_ID']}_public.xml", timeout=60)
    same = gt_copy.ok and gt_copy.content == data
    lines.append(f"- remotezip {zname} ({mb(zb)}, {st['members']:,} members, names like {st['sample_name']}): "
                 f"central directory {st['cd_requests']} requests / {mb(st['cd_bytes'])}; member {st['member_name']} "
                 f"{st['member_bytes']:,} B ({st['compressed']:,} B compressed); total {st['total_requests']} requests / "
                 f"{mb(st['total_bytes'])} = {100 * st['total_bytes'] / zb:.2f}% of the ZIP; {st['seconds']}s -> {rel(p)}")
    lines.append(f"- {zname}: mean member {st['avg_uncompressed'] / 1e3:,.1f} KB uncompressed, compression ratio "
                 f"{st['ratio']:.1f}x")
    lines.append(f"- GT S3 copy of {cal['OBJECT_ID']} byte-identical to the IRS ZIP member: {same}")

    # 2021-2023 rows carry no XML_BATCH_ID. Locate Calvary's 2023-release return by reading central directories,
    # starting with the month implied by the DLN julian day (right ~85% of the time on 2024-2026 rows).
    import datetime as _dt
    c23 = [r for r in read_index(2023) if r["EIN"] == CALVARY][0]
    month = (_dt.date(int(c23["OBJECT_ID"][:4]), 1, 1) + _dt.timedelta(int(c23["DLN"][5:8]) - 1)).month
    order = sorted((k for k in ok if k.startswith("2023_")), key=lambda k: (abs(int(k[14:16]) - month), k))
    CountingFetcher.stats = {"requests": 0, "bytes": 0}
    found, tried = None, []
    for k in order:
        tried.append(k)
        with RemoteZip(ok[k]["url"], session=S, fetcher=CountingFetcher) as z:
            if any(n.rsplit("/", 1)[-1].startswith(c23["OBJECT_ID"]) for n in z.namelist()):  # 2023 names carry a folder
                found = k
                break
    lines.append(f"- Calvary TY2021 {c23['OBJECT_ID']} (release 2023, no batch id; DLN day -> month {month:02d}): found in "
                 f"{found} after reading {len(tried)} central directories ({mb(CountingFetcher.stats['bytes'])})")
    log("10_probe_filings: remotezip", "\n".join(lines))
    print("\n".join(lines))
    return st


# ---------------------------------------------------------------- SOI annual extract
def sec_soi():
    register_source("bulk_irs_soi_extract", "IRS SOI Annual Extract of Tax-Exempt Organization Financial Data",
                    "https://www.irs.gov/statistics/soi-tax-stats-annual-extract-of-tax-exempt-organization-financial-data",
                    "Internal Revenue Service, Statistics of Income", "US government work, public domain",
                    "Yearly ZIPs {YY}eoextract990/990pf/990EZ.zip + {YY}eofinextractdoc.xlsx at www.irs.gov/pub/irs-soi/.")
    lines = []
    page = S.get("https://www.irs.gov/statistics/soi-tax-stats-annual-extract-of-tax-exempt-organization-financial-data",
                 timeout=60)
    save_raw("irs_soi", "annual_extract_page", page.content, "html")
    links = sorted(set(re.findall(r'href="(/pub/irs-soi/[^"]+\.(?:zip|xlsx|xls|dat|csv))"', page.text)))
    table = []
    for href in links:
        h = head("https://www.irs.gov" + href)
        f = href.rsplit("/", 1)[-1]
        table.append({"file": f, "url": "https://www.irs.gov" + href, "bytes": h["bytes"], "status": h["status"],
                      "last_modified": h["last_modified"]})
    yrs = sorted({re.match(r"(\d{2})", x["file"]).group(1) for x in table})
    lines.append(f"- {len(table)} files on page, year labels {yrs[0]}-{yrs[-1]}")
    for x in table:
        lines.append(f"  - {x['file']}: {mb(x['bytes'])} (HTTP {x['status']}, {x['last_modified']})")
    latest = yrs[-1]
    picks = [x for x in table if x["file"].lower() in (f"{latest}eoextract990.zip", f"{latest}eoextract990pf.zip",
                                                       f"{latest}eofinextractdoc.xlsx")]
    for x in picks:
        if x["bytes"] > 400e6:
            lines.append(f"- SKIP {x['file']}: {mb(x['bytes'])} > 400 MB")
            continue
        p, new = download(x["url"], "irs_soi", x["file"].rsplit(".", 1)[0], x["file"].rsplit(".", 1)[1])
        lines.append(f"- {'downloaded' if new else 'reused'} {x['file']} -> {rel(p)} sha256 {sha256_file(p)[:12]}")
        if p.suffix == ".zip":
            with zipfile.ZipFile(p) as z:
                for m in z.infolist():
                    with z.open(m) as fh:
                        rd = csv.reader(io.TextIOWrapper(fh, encoding="utf-8", errors="replace"))
                        hdr = next(rd)
                        ein_i = [h.upper() for h in hdr].index("EIN")
                        tp_i = next((i for i, h in enumerate(hdr) if h.lower() in ("tax_pd", "tax_prd")), None)
                        n, tps, hits = 0, Counter(), []
                        for row in rd:
                            n += 1
                            if tp_i is not None:
                                tps[row[tp_i][:4]] += 1
                            if norm_ein(row[ein_i]) == CALVARY:
                                hits.append(dict(zip(hdr, row)))
                    lines.append(f"  - member {m.filename}: {m.file_size / 1e6:,.1f} MB unzipped, {n:,} rows, "
                                 f"{len(hdr)} columns; tax period year mix {dict(sorted(tps.items()))}")
                    lines.append(f"  - columns: {', '.join(hdr)}")
                    for h in hits:
                        lines.append("  - Calvary row: " + json.dumps({k: h[k] for k in hdr[:6]} | {
                            k: h[k] for k in hdr if k.lower() in ("totrevenue", "totfuncexpns", "totassetsend",
                                                                    "totnetassetend", "totcntrbgfts", "totprgmrevnue")}))
                    if not hits and "pf" not in m.filename.lower():
                        lines.append("  - Calvary row: NOT FOUND")
    log("10_probe_filings: soi", "\n".join(lines))
    print("\n".join(lines))


# ---------------------------------------------------------------- reference pages (NCCS, Charity Navigator)
PAGES = {
    "nccs_catalogs_index": "https://nccs.urban.org/nccs/catalogs/",
    "nccs_catalog_core": "https://nccs.urban.org/nccs/catalogs/catalog-core.html",
    "nccs_catalog_efile": "https://nccs.urban.org/nccs/catalogs/catalog-efile.html",
    "nccs_catalog_bmf": "https://nccs.urban.org/nccs/catalogs/catalog-bmf.html",
    "nccs_datasets": "https://nccs.urban.org/nccs/datasets/",
    "charitynavigator_graphql_api": "https://www.charitynavigator.org/products-and-services/graphql-api/",
    "charitynavigator_developer": "https://developer.charitynavigator.org/",
    "gt_api_access_page": "https://990data.givingtuesday.org/asset-bank/",
    "gt_datalake_page": "https://990data.givingtuesday.org/access-via-aws-account-2/",
}
NCCS_HEADS = [
    "https://nccsdata.s3.us-east-1.amazonaws.com/processed_merged/core/2024/990combined/core_2024_990combined.csv",
    "https://nccsdata.s3.us-east-1.amazonaws.com/processed/core/2024/990/core_2024_990.csv",
    "https://nccsdata.s3.us-east-1.amazonaws.com/processed_merged/core/2023/990pf/core_2023_990pf.csv",
    "https://nccsdata.s3.us-east-1.amazonaws.com/geocoding/unified-bmf/latest/bmf_unified_geocoded.csv",
    "https://nccs-efile.s3.us-east-1.amazonaws.com/parsed/F9-P08-T00-REVENUE-2022.csv",
    "https://nccs-efile.s3.us-east-1.amazonaws.com/parsed/F9-P08-T00-REVENUE-2023.csv",
    "https://nccs-efile.s3.us-east-1.amazonaws.com/parsed/SI-P02-T00-GRANTS-US-ORGS-GOVTS-2022.csv",
]


def sec_pages():
    register_source("web_nccs_catalogs", "Urban Institute NCCS data catalogs (Core, E-file, BMF)",
                    "https://nccs.urban.org/nccs/catalogs/", "Urban Institute, National Center for Charitable Statistics",
                    "ODC-BY per Urban Institute data catalog; cite NCCS", "Recon only; no bulk download.")
    register_source("web_charitynavigator_api", "Charity Navigator GraphQL API terms",
                    "https://developer.charitynavigator.org/", "Charity Navigator",
                    "Charity Navigator API Terms of Use and Attribution Guidelines", "Needs API key; not signed up.")
    lines = []
    for desc, url in PAGES.items():
        r = S.get(url, timeout=60)
        save_raw("web_filings", desc, r.content, "html")
        lines.append(f"- {desc}: HTTP {r.status_code}, {len(r.content):,} B")
    for url in NCCS_HEADS:
        h = head(url)
        lines.append(f"- HEAD {url.split('.com/')[-1]}: HTTP {h['status']}, {mb(h['bytes'])}, {h['last_modified']}")
    # header row only (range read) of the merged Core panel, to document columns
    r = S.get(NCCS_HEADS[0], headers={"Range": "bytes=0-16383"}, timeout=60)
    save_raw("web_filings", "nccs_core_2024_990combined_first16KB", r.content, "csv")
    hdr = r.content.split(b"\n", 1)[0].decode("utf-8", "replace")
    lines.append(f"- NCCS core_2024_990combined header ({hdr.count(',') + 1} cols): {hdr[:600]}")
    # Charity Navigator keyless call
    r = S.post("https://api.charitynavigator.org/graphql", json={"query": "{ __typename }"}, timeout=60)
    save_raw("web_filings", "charitynavigator_graphql_keyless", r.content, "json")
    lines.append(f"- Charity Navigator GraphQL keyless POST: HTTP {r.status_code} {r.text[:120]!r}")
    log("10_probe_filings: pages", "\n".join(lines))
    print("\n".join(lines))


# ---------------------------------------------------------------- volume estimate
GROUPS = ("L", "P", "F", "I", "J", "W")


def tax_year(tax_period: str) -> int:
    """IRS tax year = year the accounting period begins (TAX_PERIOD is the YYYYMM it ends)."""
    yy, mm = int(tax_period[:4]), int(tax_period[4:6])
    return yy if mm == 12 else yy - 1


def sec_volume():
    lines = []
    dmv = {}
    for n in ("eo_dc.csv", "eo_md.csv", "eo_va.csv"):
        for r in read_bmf(n):
            dmv[r["EIN"]] = r
    pf = {e for e, r in dmv.items() if r["FOUNDATION"] in ("02", "03", "04") or r["PF_FILING_REQ_CD"] == "1"}
    dc_pc = {e for e, r in dmv.items() if r["STATE"] == "DC" and r["SUBSECTION"] == "03"
             and r["FOUNDATION"] not in ("02", "03", "04") and (r["NTEE_CD"] or " ")[0] in GROUPS}
    lines.append(f"- BMF sets: (a) DMV PF filers (FOUNDATION 02/03/04 or PF_FILING_REQ_CD=1) {len(pf):,} EINs; "
                 f"(b) DC 501(c)(3) public charities in NTEE {'/'.join(GROUPS)} {len(dc_pc):,} EINs")
    zs = {k: v for k, v in zip_stats().items() if v["status"] == 200}
    per_year = defaultdict(list)
    for k in zs:
        per_year[int(k[:4])].append(k)
    st = remote_member_stats_cache or {}
    ratio = st.get("ratio", 9.0)

    labelled = {y: {(r.get("XML_BATCH_ID") or "").upper() for r in read_index(y)} for y in INDEX_YEARS}

    def cands_of(r) -> list[str]:
        """ZIPs a row may sit in. 2021-2023 have no batch id; '05A' also covers the unlabelled '05B' part."""
        y, b = r["_release_year"], (r.get("XML_BATCH_ID") or "").upper()
        if not b:
            return per_year[y]
        return [b] + [z for z in per_year[y] if z[:-1] == b[:-1] and z != b and z not in labelled[y]]

    def zip_of(r):
        c = cands_of(r)
        return c[0] if len(c) == 1 else (c[0][:-1] + "*" if (r.get("XML_BATCH_ID") or "") else f"{r['_release_year']}_ANY")

    all_rows = [r for y in INDEX_YEARS for r in read_index(y)]
    for label, eins, types in (("a: DMV 990-PF filers", pf, ("990PF",)),
                               ("b: DC public charities L/P/F/I/J/W", dc_pc, ("990", "990EZ", "990PF"))):
        rows = [r for r in all_rows if r["EIN"] in eins and r["RETURN_TYPE"] in types]
        by_type = Counter(r["RETURN_TYPE"] for r in rows)
        by_ty = Counter(tax_year(r["TAX_PERIOD"]) for r in rows)
        by_rel = Counter(r["_release_year"] for r in rows)
        dup = len(rows) - len({(r["EIN"], r["TAX_PERIOD"], r["RETURN_TYPE"]) for r in rows})
        zips = Counter(zip_of(r) for r in rows)
        touched = set()
        for r in rows:
            touched |= set(cands_of(r))
        full = sum(zs[z]["zip_bytes"] for z in touched if z in zs)
        cd = sum(zs[z]["cd_bytes"] for z in touched if z in zs)
        members = 0.0
        for r in rows:  # mean compressed member size of the ZIP(s) it sits in
            members += statistics.mean((zs[c]["zip_bytes"] - zs[c]["cd_bytes"]) / zs[c]["entries"]
                                       for c in cands_of(r))
        gt_bytes = members * ratio
        lines.append(f"- ({label}) {len(rows):,} returns from {len({r['EIN'] for r in rows}):,} EINs; "
                     f"by type {dict(by_type)}; by tax year {dict(sorted(by_ty.items()))}; by release year "
                     f"{dict(sorted(by_rel.items()))}; same EIN+period+type repeats (amended/superseded) {dup:,}")
        latest = {}
        for r in rows:
            k = (r["EIN"], r["TAX_PERIOD"], r["RETURN_TYPE"])
            if k not in latest or r["OBJECT_ID"] > latest[k]["OBJECT_ID"]:
                latest[k] = r
        sc = Counter(tax_year(r["TAX_PERIOD"]) for r in latest.values())
        lines.append(f"  - after keeping the latest OBJECT_ID per EIN+TAX_PERIOD+type: {len(latest):,} returns; "
                     f"TY2020-TY2024 {sum(v for k, v in sc.items() if 2020 <= k <= 2024):,}")
        lines.append(f"  - ZIP batches: {len(touched)} distinct ZIPs touched "
                     f"({', '.join(f'{z} {n}' for z, n in sorted(zips.items()))})")
        lines.append(f"  - bytes: full ZIP downloads {full / 1e9:,.1f} GB; remotezip ~{(cd + members) / 1e6:,.0f} MB "
                     f"(central directories {mb(cd)} + members ~{mb(members)} compressed); GT S3 per-object "
                     f"~{mb(gt_bytes)} uncompressed")
    log("10_probe_filings: volume", "\n".join(lines))
    print("\n".join(lines))


remote_member_stats_cache: dict | None = None


# ---------------------------------------------------------------- main


def main():
    global REFRESH
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--refresh", action="store_true")
    a = ap.parse_args()
    REFRESH = a.refresh
    order = ["bmf", "irs_index", "propublica", "gt", "gt_marts", "remotezip", "soi", "pages", "volume"]
    pick = [x for x in a.only.split(",") if x] or order
    for name in order:
        if name in pick:
            fn = globals().get(f"sec_{name}")
            if fn is None:
                print(f"section {name} not implemented")
                continue
            print(f"\n===== {name} =====")
            res = fn()
            if name == "remotezip":
                globals()["remote_member_stats_cache"] = res


if __name__ == "__main__":
    main()
