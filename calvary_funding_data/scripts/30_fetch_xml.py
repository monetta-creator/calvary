"""Phase 4 bulk pull: e-filed 990 / 990-EZ / 990-PF XML for the XML scope, via lib.xmlstore.XmlStore.

Scope
  EINs: clean/dim_universe_membership.csv rule_id in SCOPE_RULES, plus every EIN in interim/core_peer_candidates.csv.
  Returns: interim/efile_index_universe.csv rows with TAX_PERIOD >= 202012 (TY2020 onward) and RETURN_TYPE in
  990/990EZ/990PF. One return per EIN + TAX_PERIOD + RETURN_TYPE: the latest submission, ordered by
  (release_year, OBJECT_ID). SUB_DATE is only a year from the 2022 index on, so it can't order submissions;
  OBJECT_ID starts with the processing year + julian day, so it sorts by submission. Superseded object ids are kept
  in the manifest. Amended flags come from the XML itself (script 50).
  Calvary (521307706): its older XMLs already in raw/xml/gt/ (TY2014-TY2019) are added as well.
  Named comparators (rule NC1, config/named_comparators.csv): TY2014-TY2019 e-filed returns are listed from the
  GivingTuesday efilexml index API (raw/gt/{stamp}_efilexml_{ein}.json; reused if present unless --refresh-older),
  fetched through XmlStore, and added to the manifest. One return per EIN + TaxYear + FormType: the highest ObjectId.

Fetch
  XmlStore.get: cached raw file -> GivingTuesday S3 (20 req/s total) -> IRS ZIP range read. PooledXmlStore below
  only changes the IRS fallback to keep one open RemoteZip per ZIP, so each fallback member costs one range request
  instead of a fresh central-directory read (5-6 MB each for 2026_TEOS_XML_05B/08A). Resumable: cached files are
  reused. Progress goes to logs/build_log.md every ~2,000 files.

Output: interim/xml_manifest.csv
  object_id, ein, tax_year, return_type, release_year, path, fetch_source, bytes, status, plus tax_period,
  xml_batch_id, taxpayer_name, scope_rules, n_submissions, superseded_object_ids, fetch_action, error.

Usage: .venv/bin/python scripts/30_fetch_xml.py [--limit N] [--workers 16] [--refresh-older]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd
from remotezip import RemoteZip

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import CLEAN, INTERIM, RAW, RateLimiter, latest_raw, log, norm_ein, rel, save_raw  # noqa: E402
from lib.xmlstore import GT_S3, IRS_XML, XmlStore, _read_member  # noqa: E402

SCOPE_RULES = {"SUBJ", "CP1", "NC1", "DCS1", "F1", "F2", "F3", "DAF1", "KF1", "KF2"}
CALVARY = "521307706"
MANIFEST = INTERIM / "xml_manifest.csv"
MANIFEST_COLS = ["object_id", "ein", "tax_year", "return_type", "release_year", "path", "fetch_source", "bytes",
                 "status", "tax_period", "xml_batch_id", "taxpayer_name", "scope_rules", "n_submissions",
                 "superseded_object_ids", "fetch_action", "error"]
LOG_EVERY = 2000
GT_API = "https://990-infrastructure.gtdata.org/irs-data/efilexml"
OLDER_TY = range(2014, 2020)   # TY2014-TY2019: before the TY2020+ IRS index window
OLDER_FORMS = {"990", "990EZ", "990PF"}


def ty_from_period(tp: str) -> int:
    """IRS tax year from YYYYMM period end: YYYY if the period ends in December, else YYYY - 1."""
    y, m = int(tp[:4]), int(tp[4:6])
    return y if m == 12 else y - 1


class PooledXmlStore(XmlStore):
    """XmlStore with two changes:
    - get(): GT objects that start with a UTF-8 byte-order mark are accepted. The base check
      `content.lstrip().startswith(b"<")` rejects them, so they fell through to the IRS ZIP (same bytes, 4 req/s).
      Many returns from some e-file vendors carry a BOM (~6k of the first 22k fetched).
    - _from_irs(): one open RemoteZip handle per IRS ZIP (reads serialized per ZIP by a lock)."""

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._handles: dict[str, RemoteZip] = {}
        self._hlocks: dict[str, threading.Lock] = {}

    def get(self, object_id, ein, tax_year, release_year=None, batch_id=None):
        oid = str(object_id)
        if oid in self.local:
            return self.local[oid], "cached"
        self.gt_rl.wait()
        r = self.s.get(GT_S3.format(oid=oid), timeout=120)
        if r.status_code == 200 and r.content.lstrip(b"\xef\xbb\xbf \t\r\n").startswith(b"<"):
            p = save_raw("xml/gt", f"{ein}_TY{tax_year}_{oid}_public", r.content, "xml")
            with self._lock:
                self.local[oid] = p
            return p, "gt_s3"
        p, how = self._from_irs(oid, ein, tax_year, release_year, batch_id)
        if p:
            with self._lock:
                self.local[oid] = p
        return p, how

    def _from_irs(self, object_id, ein, tax_year, release_year, batch_id):
        for zname in self._candidate_zips(release_year, batch_id, object_id):
            try:
                mem = self.members(zname)
            except Exception:  # noqa: BLE001
                continue
            if object_id not in mem:
                continue
            with self._lock:
                lk = self._hlocks.setdefault(zname, threading.Lock())
            with lk:
                z = self._handles.get(zname)
                if z is None:
                    z = RemoteZip(f"{IRS_XML}/{zname[:4]}/{zname}.zip", session=self.s)
                    self._handles[zname] = z
                self.irs_rl.wait()
                data = _read_member(z, mem[object_id])
            p = save_raw("xml/irs", f"{ein}_TY{tax_year}_{zname}_{object_id}_public", data, "xml")
            return p, f"irs:{zname}"
        return None, "not_found_irs"


def origin_of(p: Path) -> str:
    """fetch_source for a file on disk: gt_s3, or irs:{ZIP} parsed from the raw file name."""
    s = str(p)
    if "/xml/irs/" in s:
        m = re.search(r"_(\d{4}_TEOS_XML_\w{3})_\d{18}_public\.xml$", p.name)
        return f"irs:{m.group(1)}" if m else "irs"
    return "gt_s3"


def named_eins() -> list[str]:
    u = pd.read_csv(CLEAN / "dim_universe_membership.csv", dtype=str)
    return sorted(set(u.loc[u["rule_id"] == "NC1", "ein"].map(norm_ein)))


def older_rows(ein: str) -> list[dict]:
    """Latest return per TaxYear + FormType for TY2014-TY2019 from the newest raw GT efilexml index for this EIN."""
    p = latest_raw("gt", f"efilexml_{ein}.json")
    if p is None:
        return []
    res = (json.loads(p.read_text(encoding="utf-8")).get("body") or {}).get("results") or []
    res = [x for x in res if str(x.get("TaxYear", "")).isdigit() and int(x["TaxYear"]) in OLDER_TY
           and x.get("FormType") in OLDER_FORMS]
    out = []
    for (ty, ft), g in pd.DataFrame(res).groupby(["TaxYear", "FormType"]) if res else []:
        g = g.assign(o=g["ObjectId"].astype("int64")).sort_values("o")
        last = g.iloc[-1]
        out.append({"object_id": last["ObjectId"], "ein": ein, "tax_year": int(ty), "return_type": ft,
                    "release_year": "", "tax_period": str(last["TaxPeriodEndDate"]).replace("-", "")[:6],
                    "xml_batch_id": "", "taxpayer_name": last["OrganizationName"],
                    "n_submissions": len(g), "superseded_object_ids": ";".join(g["ObjectId"].iloc[:-1])})
    return out


def fetch_older_named(store: XmlStore, refresh: bool) -> list[str]:
    """GT efilexml index (one keyless call per named-comparator EIN, reused unless refresh) -> XmlStore.get for
    TY2014-TY2019 returns. Returns log lines."""
    lines = []
    rl = RateLimiter(0.9)   # GT API: 300 requests / 5 minutes
    for ein in named_eins():
        if refresh or latest_raw("gt", f"efilexml_{ein}.json") is None:
            rl.wait()
            r = store.s.get(GT_API, params={"ein": ein}, timeout=60)
            save_raw("gt", f"efilexml_{ein}", r.content, "json")
            lines.append(f"- GT efilexml index {ein}: HTTP {r.status_code}")
        rows = older_rows(ein)
        got = []
        for x in rows:
            p, how = store.get(x["object_id"], ein, x["tax_year"])
            got.append(f"TY{x['tax_year']} {x['return_type']} {x['object_id']} {how if p else 'NOT FOUND'}")
        lines.append(f"- {ein} TY{OLDER_TY.start}-TY{OLDER_TY.stop - 1}: {len(rows)} returns in GT index"
                     + (": " + "; ".join(got) if got else ""))
    return lines


def build_targets() -> tuple[pd.DataFrame, int, int]:
    u = pd.read_csv(CLEAN / "dim_universe_membership.csv", dtype=str)
    u["ein"] = u["ein"].map(norm_ein)
    u = u[u["rule_id"].isin(SCOPE_RULES)]
    rules = u.groupby("ein")["rule_id"].agg(lambda s: ";".join(sorted(set(s)))).to_dict()
    cp = pd.read_csv(INTERIM / "core_peer_candidates.csv", dtype=str)
    for e in cp["ein"].map(norm_ein):
        rules[e] = ";".join(x for x in [rules.get(e, ""), "core_peer_candidate"] if x)
    ix = pd.read_csv(INTERIM / "efile_index_universe.csv", dtype=str)
    ix["ein"] = ix["ein"].map(norm_ein)
    ix = ix[ix["ein"].isin(rules) & (ix["TAX_PERIOD"] >= "202012")
            & ix["RETURN_TYPE"].isin(["990", "990EZ", "990PF"])].copy()
    ix["ord"] = ix["release_year"].astype(int) * 10**18 + ix["OBJECT_ID"].astype("int64")
    ix = ix.sort_values("ord")
    rows = []
    for (ein, tp, rt), g in ix.groupby(["ein", "TAX_PERIOD", "RETURN_TYPE"], sort=False):
        last = g.iloc[-1]
        rows.append({
            "object_id": last["OBJECT_ID"], "ein": ein, "tax_year": ty_from_period(tp), "return_type": rt,
            "release_year": last["release_year"], "tax_period": tp,
            "xml_batch_id": last["XML_BATCH_ID"] if isinstance(last["XML_BATCH_ID"], str) else "",
            "taxpayer_name": last["TAXPAYER_NAME"], "scope_rules": rules[ein], "n_submissions": len(g),
            "superseded_object_ids": ";".join(g["OBJECT_ID"].iloc[:-1]),
        })
    t = pd.DataFrame(rows)
    # Calvary's older returns already on disk (TY2014-TY2019), outside the TY2020+ index window
    have = set(t["object_id"])
    for p in sorted((RAW / "xml" / "gt").glob(f"*_{CALVARY}_TY*_public.xml")):
        m = re.search(r"_TY(\d{4})_(\d{18})_public\.xml$", p.name)
        if m and int(m.group(1)) <= 2019 and m.group(2) not in have:
            t.loc[len(t)] = {"object_id": m.group(2), "ein": CALVARY, "tax_year": int(m.group(1)),
                             "return_type": "990", "release_year": "", "tax_period": "", "xml_batch_id": "",
                             "taxpayer_name": "CALVARY WOMENS SERVICES INC", "scope_rules": rules.get(CALVARY, "SUBJ"),
                             "n_submissions": 1, "superseded_object_ids": ""}
            have.add(m.group(2))
    # named comparators' older returns (TY2014-TY2019), when fetched to disk by fetch_older_named()
    on_disk = {p.name[: -len("_public.xml")].rsplit("_", 1)[-1] for p in (RAW / "xml").glob("*/*_public.xml")}
    for ein in named_eins():
        for x in older_rows(ein):
            if x["object_id"] in on_disk and x["object_id"] not in have:
                t.loc[len(t)] = {**x, "scope_rules": rules.get(ein, "NC1")}
                have.add(x["object_id"])
    n_scope = len(rules)
    n_filing = t["ein"].nunique()
    return t, n_scope, n_filing


def write_manifest(done: dict, targets: pd.DataFrame):
    m = targets.copy()
    for c in ("path", "fetch_source", "bytes", "status", "fetch_action", "error"):
        m[c] = m["object_id"].map(lambda o, c=c: done.get(o, {}).get(c, ""))
    m.loc[m["status"] == "", "status"] = "pending"
    m = m.sort_values(["ein", "tax_year", "return_type"])[MANIFEST_COLS]
    tmp = MANIFEST.with_suffix(".tmp")
    m.to_csv(tmp, index=False)
    tmp.replace(MANIFEST)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--refresh-older", action="store_true",
                    help="call the GT efilexml index again for named comparators' TY2014-TY2019 returns")
    a = ap.parse_args()

    store = PooledXmlStore(gt_rate=20.0, irs_rate=4.0)
    older = fetch_older_named(store, a.refresh_older)
    log("30_fetch_xml: named comparators TY2014-TY2019", "\n".join(older) or "- no NC1 EINs")
    print("\n".join(older))
    targets, n_scope, n_filing = build_targets()
    if a.limit:
        targets = targets.head(a.limit)
    by_type = targets["return_type"].value_counts().to_dict()
    log("30_fetch_xml: targets",
        f"- scope EINs {n_scope:,}; EINs with a TY2020+ e-filed 990/EZ/PF in the index {n_filing:,}\n"
        f"- returns {len(targets):,} (latest per EIN+period+type) {by_type}; with >1 submission "
        f"{int((targets['n_submissions'] > 1).sum()):,}\n- GT S3 at 20 req/s, IRS ZIP fallback 4 req/s; {a.workers} threads")
    print(f"targets {len(targets):,} {by_type}")

    done: dict[str, dict] = {}
    t0 = time.time()
    stats = Counter()

    def one(r):
        oid = r["object_id"]
        cached = oid in store.local
        try:
            p, how = store.get(oid, r["ein"], r["tax_year"], int(r["release_year"]) if r["release_year"] else None,
                               r["xml_batch_id"] or None)
        except Exception as ex:  # noqa: BLE001
            return oid, {"status": "error", "error": repr(ex)[:200], "fetch_action": "failed"}
        if p is None:
            return oid, {"status": "not_found", "error": how, "fetch_action": "failed"}
        return oid, {"path": rel(p), "fetch_source": origin_of(p) if how == "cached" else how,
                     "bytes": p.stat().st_size, "status": "ok", "fetch_action": "cached" if cached else "downloaded"}

    recs = targets.to_dict("records")
    for attempt in (1, 2):
        todo = [r for r in recs if done.get(r["object_id"], {}).get("status") != "ok"]
        if not todo:
            break
        with ThreadPoolExecutor(max_workers=a.workers) as ex:
            futs = [ex.submit(one, r) for r in todo]
            for i, f in enumerate(as_completed(futs), 1):
                oid, d = f.result()
                done[oid] = d
                stats[(d["status"], d.get("fetch_source", ""), d["fetch_action"])] += 1
                if i % LOG_EVERY == 0:
                    mb = sum(x.get("bytes", 0) or 0 for x in done.values()) / 1e6
                    el = time.time() - t0
                    msg = (f"- pass {attempt}: {i:,}/{len(todo):,} done in {el / 60:.1f} min ({i / el:.1f}/s); "
                           f"{mb:,.0f} MB on disk for done files; ok {sum(1 for x in done.values() if x['status'] == 'ok'):,}, "
                           f"not_found {sum(1 for x in done.values() if x['status'] == 'not_found'):,}, "
                           f"error {sum(1 for x in done.values() if x['status'] == 'error'):,}")
                    log("30_fetch_xml: progress", msg)
                    print(msg, flush=True)
                    write_manifest(done, targets)
        if attempt == 1:
            n_err = sum(1 for x in done.values() if x["status"] == "error")
            if n_err:
                print(f"retrying {n_err} errors", flush=True)
                time.sleep(10)

    m = write_manifest(done, targets)
    ok = m[m["status"] == "ok"]
    src = ok["fetch_source"].str.split(":").str[0].value_counts().to_dict()
    new_mb = ok.loc[ok["fetch_action"] == "downloaded", "bytes"].astype(float).sum() / 1e6
    lines = [
        f"- returns {len(m):,}; ok {len(ok):,}; not_found {int((m['status'] == 'not_found').sum()):,}; "
        f"error {int((m['status'] == 'error').sum()):,}",
        f"- by source (ok): {src}; downloaded this run {int((ok['fetch_action'] == 'downloaded').sum()):,} "
        f"({new_mb:,.0f} MB), reused cache {int((ok['fetch_action'] == 'cached').sum()):,}",
        f"- total XML bytes in manifest {ok['bytes'].astype(float).sum() / 1e6:,.0f} MB; elapsed {(time.time() - t0) / 60:.1f} min",
        f"- manifest -> {rel(MANIFEST)}",
    ]
    bad = m[m["status"] != "ok"]
    if len(bad):
        lines.append(f"- not fetched by release year: {bad['release_year'].value_counts().sort_index().to_dict()}; "
                     f"sample errors: {bad['error'].value_counts().head(3).to_dict()}")
    log("30_fetch_xml: done", "\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
