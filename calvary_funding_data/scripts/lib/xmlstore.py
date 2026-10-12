"""Object-addressed store for e-filed 990 XML.

get(object_id, ein, tax_year, release_year, batch_id) returns a local path, trying in order:
  1. an existing raw file  raw/xml/{gt|irs}/*_{object_id}_public.xml
  2. GivingTuesday data lake (anonymous S3)           -> raw/xml/gt/
  3. IRS batch ZIP via HTTP range reads (remotezip)    -> raw/xml/irs/
Raw files keep the convention {stamp}_{ein}_TY{tax_year}_{object_id}_public.xml (irs: ..._{zip}_{object_id}...).
IRS ZIP names are probed once and cached in interim/irs_zip_list.csv; each ZIP's central directory is read
once and cached in interim/irs_zip_members/{zip}.csv.
"""
from __future__ import annotations

import csv
import threading
from pathlib import Path

import struct
import zipfile

import inflate64
from remotezip import RemoteZip

from .common import INTERIM, RAW, RateLimiter, save_raw, session

GT_S3 = "https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{oid}_public.xml"
IRS_XML = "https://apps.irs.gov/pub/epostcard/990/xml"


def _read_member(z: zipfile.ZipFile, name: str) -> bytes:
    """Read a ZIP member, handling Deflate64 (method 9), which zipfile can't decompress, via inflate64."""
    info = z.getinfo(name)
    if info.compress_type != 9:
        return z.read(name)
    z.fp.seek(info.header_offset)
    hdr = z.fp.read(30)
    fn_len, extra_len = struct.unpack("<HH", hdr[26:30])
    z.fp.seek(info.header_offset + 30 + fn_len + extra_len)
    raw = z.fp.read(info.compress_size)
    return inflate64.Inflater().inflate(raw)


class XmlStore:
    def __init__(self, gt_rate: float = 20.0, irs_rate: float = 4.0):
        self.s = session()
        self.gt_rl = RateLimiter(gt_rate)
        self.irs_rl = RateLimiter(irs_rate)
        self._lock = threading.Lock()
        self._zip_locks: dict[str, threading.Lock] = {}
        self.local: dict[str, Path] = {}
        for p in (RAW / "xml").glob("*/*_public.xml"):
            oid = p.name[: -len("_public.xml")].rsplit("_", 1)[-1]
            self.local.setdefault(oid, p)
        self._zip_list: dict[int, list[str]] | None = None
        self._members: dict[str, dict[str, str]] = {}
        (INTERIM / "irs_zip_members").mkdir(parents=True, exist_ok=True)

    # ---------------- IRS ZIP helpers
    def zip_list(self, year: int) -> list[str]:
        with self._lock:
            if self._zip_list is None:
                self._zip_list = {}
                p = INTERIM / "irs_zip_list.csv"
                if p.exists():
                    for r in csv.DictReader(open(p, encoding="utf-8")):
                        self._zip_list.setdefault(int(r["year"]), []).append(r["zip"])
            if year not in self._zip_list:
                found = []
                for mm in range(1, 13):
                    for part in "ABCD":
                        name = f"{year}_TEOS_XML_{mm:02d}{part}"
                        r = self.s.head(f"{IRS_XML}/{year}/{name}.zip", timeout=30)
                        if r.status_code == 200:
                            found.append(name)
                        elif part != "A":
                            break
                self._zip_list[year] = found
                p = INTERIM / "irs_zip_list.csv"
                new = not p.exists()
                with open(p, "a", newline="", encoding="utf-8") as f:
                    w = csv.writer(f)
                    if new:
                        w.writerow(["year", "zip"])
                    w.writerows([[year, z] for z in found])
            return self._zip_list[year]

    def members(self, zname: str) -> dict[str, str]:
        """object_id -> member name inside the ZIP (central directory read once, then cached)."""
        with self._lock:
            if zname in self._members:
                return self._members[zname]
            lk = self._zip_locks.setdefault(zname, threading.Lock())
        with lk:
            if zname in self._members:
                return self._members[zname]
            cache = INTERIM / "irs_zip_members" / f"{zname}.csv"
            if cache.exists():
                mem = {r["object_id"]: r["member"] for r in csv.DictReader(open(cache, encoding="utf-8"))}
            else:
                year = zname[:4]
                with RemoteZip(f"{IRS_XML}/{year}/{zname}.zip", session=self.s) as z:
                    names = z.namelist()
                mem = {n.rsplit("/", 1)[-1].split("_")[0]: n for n in names if n.endswith(".xml")}
                with open(cache, "w", newline="", encoding="utf-8") as f:
                    w = csv.writer(f)
                    w.writerow(["object_id", "member"])
                    w.writerows(sorted(mem.items()))
            with self._lock:
                self._members[zname] = mem
            return mem

    def _candidate_zips(self, release_year: int | None, batch_id: str | None, object_id: str) -> list[str]:
        cands = []
        if batch_id:
            b = batch_id.upper()
            cands.append(b)
            if b.endswith("A"):
                cands.append(b[:-1] + "B")   # index label '05A' also covers the unlabelled '05B' part
        yrs = [release_year] if release_year else []
        yrs += [int(object_id[:4])]
        for y in dict.fromkeys(yrs):
            for z in self.zip_list(y):
                if z not in cands:
                    cands.append(z)
        return cands

    def _from_irs(self, object_id, ein, tax_year, release_year, batch_id) -> tuple[Path | None, str]:
        for zname in self._candidate_zips(release_year, batch_id, object_id):
            try:
                mem = self.members(zname)
            except Exception as ex:  # noqa: BLE001
                continue
            if object_id in mem:
                self.irs_rl.wait()
                with RemoteZip(f"{IRS_XML}/{zname[:4]}/{zname}.zip", session=self.s) as z:
                    data = _read_member(z, mem[object_id])
                p = save_raw("xml/irs", f"{ein}_TY{tax_year}_{zname}_{object_id}_public", data, "xml")
                return p, f"irs:{zname}"
        return None, "not_found_irs"

    # ---------------- public
    def get(self, object_id: str, ein: str, tax_year, release_year: int | None = None,
            batch_id: str | None = None) -> tuple[Path | None, str]:
        oid = str(object_id)
        if oid in self.local:
            return self.local[oid], "cached"
        self.gt_rl.wait()
        r = self.s.get(GT_S3.format(oid=oid), timeout=120)
        body = r.content.removeprefix(b"\xef\xbb\xbf").lstrip()   # some GT files start with a UTF-8 BOM
        if r.status_code == 200 and body.startswith(b"<"):
            p = save_raw("xml/gt", f"{ein}_TY{tax_year}_{oid}_public", r.content, "xml")
            with self._lock:
                self.local[oid] = p
            return p, "gt_s3"
        p, how = self._from_irs(oid, ein, tax_year, release_year, batch_id)
        if p:
            with self._lock:
                self.local[oid] = p
        return p, how
