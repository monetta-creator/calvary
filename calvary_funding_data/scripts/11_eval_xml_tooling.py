"""Phase 2 recon, area "filings": evaluate XML tooling for Phase 4 parsing.

Steps (run all, or pick with --only):
  fetch        Test XMLs. Calvary TY2021-TY2023 990s, Meyer/Cafritz 990-PFs and Greater Washington Community
               Foundation 990s (Schedule I/R) from the GT data lake -> raw/xml/gt/; Meyer TY2023 990-PF by remotezip
               range read from the IRS ZIP -> raw/xml/irs/. Calvary TY2014-TY2020 + TY2024 come from script 10.
  concordance  NODC master concordance files at the current master commit -> raw/concordance/
  lxml         Hand-written, namespace-stripped lxml parser over every test XML; concordance coverage of each XML's
               leaf paths; schema versions seen.
  irsx         IRSx (PyPI irsx) in a throwaway venv built with `uv venv --python 3.12` under --scratch.

Usage: .venv/bin/python scripts/11_eval_xml_tooling.py [--only fetch,concordance,lxml,irsx] [--scratch DIR]
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

from lxml import etree

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import RAW, log, register_source, rel, save_raw, session

_spec = importlib.util.spec_from_file_location("p10", Path(__file__).parent / "10_probe_filings.py")
p10 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(p10)

S = session()
GT_S3 = "https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles"
REPO = "Nonprofit-Open-Data-Collective/irs-efile-master-concordance-file"
CONCORDANCE_FILES = [
    "concordance.csv", "README.md", "LICENSE.md", "CITATION.cff", "00-documentation/VARNAMES.md",
    "02-concordance-foundations/F990-PF-FULL.CSV",
    "draft-updates/DUCKDB-XPATH-REPORT.CSV",
    "draft-updates/XPATH-VERSION-COUNT.CSV",
    "draft-updates/MISSING-XPATHS-UNIQUE-FILE-ALL.CSV",
]

# (label, ein, tax_year, object_id, origin) ; origin gt = GT S3 object, irs:<ZIP> = remotezip from IRS batch ZIP
TEST_XMLS = [
    ("calvary_990", "521307706", 2021, "202322239349302102", "gt"),
    ("calvary_990", "521307706", 2022, "202401649349300215", "gt"),
    ("calvary_990", "521307706", 2023, "202542169349300419", "gt"),
    ("meyer_990pf", "530241716", 2021, "202233149349102223", "gt"),
    ("meyer_990pf", "530241716", 2022, "202303119349102405", "gt"),
    ("meyer_990pf", "530241716", 2023, "202443119349102189", "irs:2024_TEOS_XML_11A"),
    ("meyer_990pf", "530241716", 2024, "202512959349101021", "gt"),
    ("cafritz_990pf", "526036989", 2024, "202513399349100006", "gt"),
    ("gwcf_990", "237343119", 2023, "202520389349300807", "gt"),
    ("gwcf_990", "237343119", 2024, "202640449349302259", "gt"),
]


def xml_files() -> list[tuple[str, int, str, Path]]:
    """All test XMLs on disk: (label, tax_year, object_id, path)."""
    out = []
    for p in sorted((RAW / "xml").rglob("*_public.xml")):
        m = re.search(r"_(\d{9})_TY(\d{4})_.*?(\d{18})_public\.xml$", p.name)
        if not m:
            continue
        ein, ty, oid = m.group(1), int(m.group(2)), m.group(3)
        label = {"521307706": "calvary_990", "530241716": "meyer_990pf", "526036989": "cafritz_990pf",
                 "237343119": "gwcf_990"}.get(ein, ein)
        if not any(o[2] == oid for o in out):
            out.append((label, ty, oid, p))
    return sorted(out, key=lambda x: (x[0], x[1]))


# ---------------------------------------------------------------- fetch
def sec_fetch():
    lines = []
    for label, ein, ty, oid, origin in TEST_XMLS:
        if any(p.name.endswith(f"{oid}_public.xml") for p in (RAW / "xml").rglob("*.xml")):
            lines.append(f"- {label} TY{ty} {oid}: already in raw/xml")
            continue
        if origin == "gt":
            r = S.get(f"{GT_S3}/{oid}_public.xml", timeout=60)
            r.raise_for_status()
            p = save_raw("xml/gt", f"{ein}_TY{ty}_{oid}_public", r.content, "xml")
            lines.append(f"- {label} TY{ty} {oid}: GT S3 {len(r.content):,} B -> {rel(p)}")
        else:
            zname = origin.split(":", 1)[1]
            url = f"{p10.IRS_XML}/{zname[:4]}/{zname}.zip"
            data, st = p10.remote_member(url, oid)
            p = save_raw("xml/irs", f"{ein}_TY{ty}_{zname}_{oid}_public", data, "xml")
            lines.append(f"- {label} TY{ty} {oid}: remotezip {zname} member {st['member_bytes']:,} B; transferred "
                         f"{st['total_requests']} requests / {p10.mb(st['total_bytes'])} (central directory "
                         f"{p10.mb(st['cd_bytes'])}) -> {rel(p)}")
    log("11_eval_xml_tooling: fetch", "\n".join(lines))
    print("\n".join(lines))


# ---------------------------------------------------------------- concordance
def sec_concordance():
    meta = S.get(f"https://api.github.com/repos/{REPO}/commits/master", timeout=60)
    meta.raise_for_status()
    save_raw("concordance", "github_master_commit", meta.content, "json")
    sha = meta.json()["sha"]
    register_source("bulk_nodc_concordance", "NODC IRS e-file master concordance file",
                    f"https://github.com/{REPO}", "Nonprofit Open Data Collective",
                    "See repository LICENSE.md and CITATION.cff",
                    f"Pinned to commit {sha[:12]}. concordance.csv maps variable names to xpaths by schema version.")
    lines = [f"- commit {sha[:12]} ({meta.json()['commit']['author']['date']})"]
    for f in CONCORDANCE_FILES:
        url = f"https://raw.githubusercontent.com/{REPO}/{sha}/{f}"
        r = S.get(url, timeout=120)
        if not r.ok:
            lines.append(f"- {f}: HTTP {r.status_code}")
            continue
        desc = f"{sha[:8]}_" + f.replace("/", "__").rsplit(".", 1)[0]
        p = save_raw("concordance", desc, r.content, f.rsplit(".", 1)[1].lower())
        lines.append(f"- {f}: {len(r.content):,} B -> {rel(p)}")
    log("11_eval_xml_tooling: concordance", "\n".join(lines))
    print("\n".join(lines))


def load_concordance() -> list[dict]:
    p = sorted((RAW / "concordance").glob("*_concordance.csv"))[-1]
    with open(p, newline="", encoding="utf-8", errors="replace") as f:
        return list(csv.DictReader(f))


def load_csv(pattern: str) -> list[dict]:
    hits = sorted((RAW / "concordance").glob(pattern))
    if not hits:
        return []
    with open(hits[-1], newline="", encoding="utf-8", errors="replace") as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------- lxml
def strip_ns(path: Path) -> etree._Element:
    root = etree.parse(str(path)).getroot()
    for el in root.iter():
        if isinstance(el.tag, str):
            el.tag = etree.QName(el).localname
    return root


def t(node, xp: str):
    v = node.xpath(xp)
    if not v:
        return None
    v = v[0]
    return (v.text or "").strip() if hasattr(v, "text") else str(v)


def name_of(g) -> str | None:
    return (t(g, "RecipientBusinessName/BusinessNameLine1Txt") or t(g, "RecipientBusinessName/BusinessNameLine1")
            or t(g, "RecipientPersonNm") or t(g, "RecipientNameBusiness/BusinessNameLine1"))


def parse_return(path: Path) -> dict:
    """Hand-written parser. Namespace-stripped, relative xpaths, no schema-version branching."""
    r = strip_ns(path)
    out = {"returnVersion": r.get("returnVersion"), "TaxYr": t(r, "ReturnHeader/TaxYr"),
           "TaxPeriodBeginDt": t(r, "ReturnHeader/TaxPeriodBeginDt"), "TaxPeriodEndDt": t(r, "ReturnHeader/TaxPeriodEndDt"),
           "ReturnTypeCd": t(r, "ReturnHeader/ReturnTypeCd"), "EIN": t(r, "ReturnHeader/Filer/EIN"),
           "name": t(r, "ReturnHeader/Filer/BusinessName/BusinessNameLine1Txt")}
    rd = r.find("ReturnData")
    out["schedules"] = [c.tag for c in rd if isinstance(c.tag, str)]
    f = rd.find("IRS990")
    if f is not None:
        out |= {
            "CYTotalRevenueAmt": t(f, "CYTotalRevenueAmt"), "CYTotalExpensesAmt": t(f, "CYTotalExpensesAmt"),
            "mission": (t(f, "ActivityOrMissionDesc") or "")[:60],
            "P8_TotalContributionsAmt": t(f, "TotalContributionsAmt"),
            "P8_GovernmentGrantsAmt": t(f, "GovernmentGrantsAmt"),
            "P8_FundraisingAmt": t(f, "FundraisingAmt"),
            "P8_AllOtherContributionsAmt": t(f, "AllOtherContributionsAmt"),
            "P8_NoncashContributionsAmt": t(f, "NoncashContributionsAmt"),
            "P8_TotalProgramServiceRevenueAmt": t(f, "TotalProgramServiceRevenueAmt"),
            "P8_TotalRevenueColumnAmt": t(f, "TotalRevenueGrp/TotalRevenueColumnAmt"),
            "P9_TotalAmt": t(f, "TotalFunctionalExpensesGrp/TotalAmt"),
            "P9_ProgramServicesAmt": t(f, "TotalFunctionalExpensesGrp/ProgramServicesAmt"),
            "P9_ManagementAndGeneralAmt": t(f, "TotalFunctionalExpensesGrp/ManagementAndGeneralAmt"),
            "P9_FundraisingAmt": t(f, "TotalFunctionalExpensesGrp/FundraisingAmt"),
            "P9_GrantsToDomesticOrgs": t(f, "GrantsToDomesticOrgsGrp/TotalAmt"),
            "P7A_people": len(f.findall("Form990PartVIISectionAGrp")),
            "P7A_first": t(f, "Form990PartVIISectionAGrp/TitleTxt"),
        }
    si = rd.find("IRS990ScheduleI")
    if si is not None:
        g = si.findall("RecipientTable")
        out |= {"SI_grants": len(g), "SI_cash_total": sum(float(t(x, "CashGrantAmt") or 0) for x in g),
                "SI_first": name_of(g[0]) if g else None}
    sr = rd.find("IRS990ScheduleR")
    if sr is not None:
        out |= {"SR_related_exempt": len(sr.findall("IdRelatedTaxExemptOrgGrp")),
                "SR_related_txbl_corp": len(sr.findall("IdRelatedOrgTxblCorpTrGrp")),
                "SR_related_partnership": len(sr.findall("IdRelatedOrgTxblPartnershipGrp")),
                "SR_disregarded": len(sr.findall("IdDisregardedEntitiesGrp"))}
    pf = rd.find("IRS990PF")
    if pf is not None:
        g = pf.findall("SupplementaryInformationGrp/GrantOrContributionPdDurYrGrp")
        people = pf.findall("OfficerDirTrstKeyEmplInfoGrp/OfficerDirTrstKeyEmplGrp")
        out |= {
            "PF_TotalRevAndExpnssAmt": t(pf, "AnalysisOfRevenueAndExpenses/TotalRevAndExpnssAmt"),
            "PF_ContriPaidRevAndExpnssAmt": t(pf, "AnalysisOfRevenueAndExpenses/ContriPaidRevAndExpnssAmt"),
            "PF_FMVAssetsEOYAmt": t(pf, "FMVAssetsEOYAmt"),
            "PF_grants": len(g), "PF_grants_sum": sum(float(t(x, "Amt") or 0) for x in g),
            "PF_TotalGrantOrContriPdDurYrAmt": t(pf, "SupplementaryInformationGrp/TotalGrantOrContriPdDurYrAmt"),
            "PF_grants_with_name": sum(1 for x in g if name_of(x)),
            "PF_grants_with_purpose": sum(1 for x in g if t(x, "GrantOrContributionPurposeTxt")),
            "PF_grant_first": name_of(g[0]) if g else None,
            "PF_people": len(people),
            "PF_calvary_hits": [(name_of(x), t(x, "Amt")) for x in g if "CALVARY" in (name_of(x) or "").upper()],
        }
    return out


def leaf_paths(path: Path) -> set[str]:
    root = strip_ns(path)
    tree = etree.ElementTree(root)
    out = set()
    for el in root.iter():
        if isinstance(el.tag, str) and len(el) == 0:
            out.add(re.sub(r"\[\d+\]", "", tree.getpath(el)))
    return out


def sec_lxml():
    lines = []
    conc = load_concordance()
    pfc = load_csv("*F990-PF-FULL.csv")
    rep = load_csv("*DUCKDB-XPATH-REPORT.csv")
    norm = lambda x: re.sub(r"\[\d+\]", "", (x or "").strip())  # noqa: E731
    cxp = {norm(x["xpath"]) for x in conc if x["xpath"].strip()}
    pxp = {norm(x["xpath"]) for x in pfc if x["xpath"].strip()}
    allxp = cxp | pxp

    def vers(rows):
        return Counter(v for x in rows for v in re.split(r";+", x.get("versions") or "") if v)

    for nm, rows in (("concordance.csv (990, 990-EZ, schedules)", conc), ("F990-PF-FULL.CSV", pfc)):
        vv = vers(rows)
        lines.append(f"- {nm}: {len(rows):,} rows; form_type {dict(Counter(x.get('form_type') for x in rows))}; "
                     f"newest versions tagged: {', '.join(sorted(vv)[-4:]) or 'none'}; rows tagged with a 2021+ "
                     f"version {sum(1 for x in rows if re.search(r'202[1-9]v', x.get('versions') or '')):,}; "
                     f"latest_version mix {dict(Counter(x.get('latest_version') for x in rows).most_common(4))}")
    areas = {
        "Part VIII revenue": r"/IRS990/(TotalContributionsAmt|GovernmentGrantsAmt|ProgramServiceRevenueGrp|TotalRevenueGrp|FundraisingAmt|AllOtherContributionsAmt|FederatedCampaignsAmt|NoncashContributionsAmt)",
        "Part IX expenses": r"/IRS990/(TotalFunctionalExpensesGrp|GrantsToDomesticOrgsGrp|OtherSalariesAndWagesGrp|CompCurrentOfcrDirectorsGrp)",
        "Part VII-A people": r"/IRS990/Form990PartVIISectionAGrp/",
        "Schedule I": r"/IRS990ScheduleI/",
        "Schedule R": r"/IRS990ScheduleR/",
        "990-PF grants paid": r"/IRS990PF/SupplementaryInformationGrp/GrantOrContributionPdDurYrGrp",
        "990-PF officers": r"/IRS990PF/OfficerDirTrstKeyEmplInfoGrp",
    }
    lines.append("- xpaths in concordance + F990-PF-FULL by area: " +
                 "; ".join(f"{k} {sum(1 for x in allxp if re.search(v, x))}" for k, v in areas.items()))
    # DuckDB report = every xpath observed in the Oct 2025 e-file rebuild, with the versions it occurs in and
    # the concordance variable it maps to (blank = unmapped)
    rep = [x for x in rep if x["path_type"] == "DATA"]
    recent = [x for x in rep if re.search(r"202[34]v", x["schema_versions"])]
    lines.append(f"- DUCKDB-XPATH-REPORT (observed DATA xpaths, Oct 2025 rebuild): {len(rep):,}; seen in 2023/2024 "
                 f"schemas {len(recent):,}, of which mapped to a concordance variable "
                 f"{sum(1 for x in recent if x['variable_name']):,}")
    for k, v in areas.items():
        a = [x for x in recent if re.search(v, x["xpath"])]
        unm = [x["xpath"].rsplit("/", 1)[-1] for x in a if not x["variable_name"]]
        lines.append(f"  - {k}: {len(a)} xpaths seen in 2023/2024 schemas, unmapped {len(unm)}"
                     + (f" (e.g. {', '.join(unm[:4])})" if unm else ""))
    lines.append(f"  - all IRS990PF xpaths seen in 2023/2024: {sum(1 for x in recent if '/IRS990PF/' in x['xpath'])}, "
                 f"unmapped {sum(1 for x in recent if '/IRS990PF/' in x['xpath'] and not x['variable_name'])}")

    # parse every test XML
    versions = Counter()
    for label, ty, oid, path in xml_files():
        try:
            d = parse_return(path)
        except Exception as e:  # noqa: BLE001
            lines.append(f"- {label} TY{ty} {oid}: PARSE ERROR {e}")
            continue
        versions[d["returnVersion"]] += 1
        lp = leaf_paths(path)
        cov = len(lp & allxp) / max(1, len(lp))
        miss = sorted(lp - allxp)
        keep = {k: v for k, v in d.items() if k not in ("schedules", "name", "EIN", "TaxPeriodBeginDt") and v not in (None, "", [])}
        lines.append(f"- {label} TY{ty} {oid} [{d['returnVersion']}] TaxYr {d['TaxYr']} {d['TaxPeriodBeginDt']}..{d['TaxPeriodEndDt']}: "
                     f"{json.dumps(keep)}")
        lines.append(f"  - schedules: {', '.join(d['schedules'])}")
        lines.append(f"  - concordance covers {cov:.0%} of {len(lp)} leaf paths; e.g. missing: "
                     f"{', '.join(m.replace('/Return/ReturnData/', '') for m in miss[:4])}")
    lines.append(f"- schema versions seen: {dict(sorted(versions.items()))}")
    log("11_eval_xml_tooling: lxml", "\n".join(lines))
    print("\n".join(lines))


# ---------------------------------------------------------------- IRSx
IRSX_RUNNER = r'''
import json, sys, traceback
from irsx.xmlrunner import XMLRunner
from irsx.settings import version_is_supported
out = []
xr = XMLRunner()
for label, ty, oid, path in json.loads(sys.argv[1]):
    rec = {"label": label, "ty": ty, "oid": oid}
    try:
        f = xr.run_filing(oid, filepath=path)
        rec["version"] = f.get_version()
        rec["supported"] = version_is_supported(rec["version"])
        rec["schedules"] = f.list_schedules()
        res = f.get_result() or []
        rec["parsed_schedules"] = [s["schedule_name"] for s in res]
        rec["keyerrors"] = len(f.get_keyerrors() or [])
        rec["keyerror_sample"] = [k.get("element_path") or str(k) for k in (f.get_keyerrors() or [])][:3]
        for s in res:
            if s["schedule_name"] == "IRS990":
                p1 = s["schedule_parts"].get("part_i", {})
                p8 = s["schedule_parts"].get("part_viii", {})
                rec["IRS990_CYTotalRevenueAmt"] = p1.get("CYTtlRvnAmt")
                rec["IRS990_part_viii_keys"] = len(p8)
                rec["IRS990_groups"] = {k: len(v) for k, v in s["groups"].items()}
            if s["schedule_name"] == "IRS990PF":
                g = s["groups"].get("PFGrntOrCntrbtnPdDrYr", [])
                rec["PF_grants"] = len(g)
                rec["PF_grants_sum"] = sum(float(x.get("GrntOrCntrbtnPdDrYr_Amt") or 0) for x in g)
                rec["PF_parts"] = sorted(s["schedule_parts"])
                rec["PF_groups"] = {k: len(v) for k, v in s["groups"].items()}
            if s["schedule_name"] == "IRS990ScheduleI":
                rec["SI_grants"] = len(s["groups"].get("SkdIRcpntTbl", []))
            if s["schedule_name"] == "IRS990ScheduleR":
                rec["SR_groups"] = {k: len(v) for k, v in s["groups"].items()}
    except Exception as e:
        rec["error"] = repr(e)[:300]
        rec["trace"] = traceback.format_exc()[-400:]
    out.append(rec)
print(json.dumps(out))
'''


def sec_irsx(scratch: str):
    d = Path(scratch) / "irsx_venv"
    lines = []
    if not (d / "bin" / "python").exists():
        r = subprocess.run(["uv", "venv", "--python", "3.12", str(d)], capture_output=True, text=True)
        lines.append(f"- uv venv --python 3.12: rc {r.returncode}")
    r = subprocess.run(["uv", "pip", "install", "--python", str(d / "bin" / "python"), "irsx"],
                       capture_output=True, text=True)
    ver = subprocess.run([str(d / "bin" / "python"), "-c", "import irsx._version as v, sys; "
                          "print(v.__version__, sys.version.split()[0])"], capture_output=True, text=True)
    lines.append(f"- pip install irsx: rc {r.returncode}; irsx/python: {ver.stdout.strip() or ver.stderr[-200:]}")
    # also try a Python 3.13 venv, since the plan expected 3.13
    d13 = Path(scratch) / "irsx_venv313"
    if not (d13 / "bin" / "python").exists():
        subprocess.run(["uv", "venv", "--python", "3.13", str(d13)], capture_output=True, text=True)
    r13 = subprocess.run(["uv", "pip", "install", "--python", str(d13 / "bin" / "python"), "irsx"],
                         capture_output=True, text=True)
    ok13 = subprocess.run([str(d13 / "bin" / "python"), "-c", "import irsx.xmlrunner; print('ok')"],
                          capture_output=True, text=True)
    lines.append(f"- Python 3.13 venv: install rc {r13.returncode}, import {ok13.stdout.strip() or ok13.stderr[-120:]}")
    files = [(lab, ty, oid, str(p.resolve())) for lab, ty, oid, p in xml_files()
             if ty >= 2019 or lab != "calvary_990"]
    runner = Path(scratch) / "irsx_runner.py"
    runner.write_text(IRSX_RUNNER)
    res = subprocess.run([str(d / "bin" / "python"), str(runner), json.dumps(files)], capture_output=True, text=True,
                         cwd=scratch)
    try:
        recs = json.loads(res.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        lines.append(f"- runner failed: {res.stderr[-600:]}")
        recs = []
    for x in recs:
        if "error" in x:
            lines.append(f"- {x['label']} TY{x['ty']} {x['oid']}: ERROR {x['error']}")
            continue
        keep = {k: v for k, v in x.items() if k not in ("label", "ty", "oid", "schedules", "trace")}
        lines.append(f"- {x['label']} TY{x['ty']} {x['oid']}: {json.dumps(keep)[:900]}")
    log("11_eval_xml_tooling: irsx", "\n".join(lines))
    print("\n".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--scratch", default=tempfile.gettempdir())
    a = ap.parse_args()
    order = ["fetch", "concordance", "lxml", "irsx"]
    pick = [x for x in a.only.split(",") if x] or order
    for name in order:
        if name in pick:
            print(f"\n===== {name} =====")
            if name == "irsx":
                sec_irsx(a.scratch)
            else:
                globals()[f"sec_{name}"]()


if __name__ == "__main__":
    main()
