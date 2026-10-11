"""Phase 4: IRS SOI annual extracts (990, 990-EZ, 990-PF) -> long financial series for every universe EIN.

STAGES (run all, or pick with --only):
  download       every {YY}eo*extract990/990ez/990pf ZIP + {YY}eofinextractdoc for YY=12..24 -> raw/irs_soi/
                 (file list from the SOI page; files already in raw/irs_soi/ are reused, incl. the 2024 990/990-PF)
  nccs_download  NCCS e-file Part VIII tables F9-P08-T00-REVENUE-{2009..2022}.csv -> raw/nccs/ (2.1 GB), plus a
                 HEAD check of NCCS Core 990-PF files (they share the SOI 990-PF 2016-2018 gap, so not downloaded)
  stage          SOI rows (source_id bulk_irs_soi_extract) + NCCS Part VIII rows (source_id bulk_nccs_efile)
                 for universe EINs -> interim/stage_fact_org_financials__soi.csv

Usage: .venv/bin/python scripts/41_pull_soi_extracts.py [--only download,nccs_download,stage]

WHY NCCS. No SOI extract year carries Form 990 Part VIII line 1e (government grants) or the other 1a-1g lines.
The bulk source for them is the NCCS e-file Part VIII table (parsed from e-filed XML; Form 990 e-filers only;
TAX_YEAR = IRS tax year; 2023 not published). Those rows are staged in the same file with their own source_id
(bulk_nccs_efile) so row-level provenance is kept: federated_campaigns 1a, membership_dues 1b,
fundraising_event_contributions 1c, related_org_contributions 1d, government_grants 1e, other_contributions 1f,
noncash_contributions 1g, contributions_total 1h, program_service_revenue 2g, investment_income 3,
special_events_net 8c, other_revenue 11e, total_revenue 12 (all column A). NCCS has no period end: it is taken from
the SOI 990 row for the same EIN + tax_year (x_period_from=soi), else from the IRS e-file index by OBJECT_ID
(x_period_from=irs_index); rows with neither are dropped. XML omits zero lines, so absent Part VIII lines are set
to 0 when line 12 is reported. One return per EIN + tax_year: the highest OBJECT_ID (latest filed).

YEAR LABELS. The extract label YY is the SOI *processing* year: the 24 990 extract is mostly tax periods ending
2023. Every row's tax period (tax_pd / tax_prd / taxpd, YYYYMM = period END) gives
fiscal_year = YYYY, fye_month = MM, tax_year = YYYY if MM == 12 else YYYY - 1, tax_period_end = last day of MM.
One EIN + period can appear in several processing years (late or re-processed returns). The staged row is the one
from the LATEST processing year (last row within a file); x_soi_n_versions counts the copies and
x_soi_versions_differ = 1 when their total_revenue differs.

FILE FORMATS. 12-17: space-delimited .dat; 18-23: CSV with a UTF-8 BOM; 24: CSV. Headers are lowercased and
these aliases applied: tax_prd / taxprd / taxpd / a_tax_prd -> tax_pd; elf / e-file / elfcd -> efile;
subcd -> subseccd. No 990-PF extract exists for processing years 17, 18, 19 (not on the SOI page, 404 at the
expected URLs, not in the GivingTuesday mirror), so 990-PF tax periods ending ~2016-2018 are thin.

FIELD MAPPING (SOI documentation workbooks {YY}eofinextractdoc; "+" = sum of the listed lines, populated only when
every component column exists in that year's file; a fact field with no SOI source is left blank).

| fact field              | 990 extract (Form 990)                                   | 990-EZ extract           | 990-PF extract                     | years / caveats |
|-------------------------|----------------------------------------------------------|--------------------------|------------------------------------|-----------------|
| total_revenue           | totrevenue (VIII-12A)                                    | totrevnue (I-9)          | totrcptperbks (I-12a)              | all |
| contributions_total     | totcntrbgfts (VIII-1h)                                   | totcntrbs (I-1)          | grscontrgifts (I-1a)               | all |
| program_service_revenue | totprgmrevnue (VIII-2g)                                  | prgmservrev (I-2)        | -                                  | all |
| membership_dues         | -                                                        | duesassesmnts (I-3)      | -                                  | 990: not in extract |
| investment_income       | invstmntinc (VIII-3)                                     | othrinvstinc (I-4)       | intrstrvnue + dividndsamt (I-3,4)  | all |
| special_events_net      | netincfndrsng (VIII-8c)                                  | netincfndrsng (I-6d, events+gaming) | -                       | all |
| other_revenue           | miscrevtot11e (VIII-11e, misc revenue only)              | othrevnue (I-8)          | -                                  | all |
| total_expenses          | totfuncexpns (IX-25A)                                    | totexpns (I-17)          | totexpnspbks (I-26a)               | all |
| grants_paid             | grntstogovt + grnsttoindiv + grntstofrgngovt (IX-1..3A, = Part I line 13) | -       | contrpdpbks (I-25a)                | 990: 13-24 only |
| compensation_total      | compnsatncurrofcr + compnsatnandothr + othrsalwages + pensionplancontrb + othremplyeebenef + payrolltx (IX-5..10A, = Part I line 15) | - | - | 990: 13-24 only |
| total_assets_eoy        | totassetsend (X-16B)                                     | totassetsend (II-25B)    | totassetsend (II-16b, book)        | all |
| total_liabilities_eoy   | totliabend (X-26B)                                       | totliabend (II-26B)      | totliabend (II-23b)                | all |
| net_assets_eoy          | totnetassetend (X-33B)                                   | totnetassetsend (II-27B), else networthend (I-21) | tfundnworth (SOI doc: Pt II-31 col b) | all |
| cash_savings_eoy        | nonintcashend + svngstempinvend (X-1B, X-2B)             | -                        | - (x_pf_cash_nonint_eoy only)      | 990: 13-24 only |
| pf_fmv_assets_eoy       | -                                                        | -                        | fairmrktvaleoy (II-16c), else fairmrktvalamt (header I) | PF |
| pf_total_grants_paid    | -                                                        | -                        | contrpdpbks (I-25a)                | PF |
| pf_contributions_received | -                                                      | -                        | grscontrgifts (I-1a)               | PF |
| pf_qualifying_distributions | -                                                    | -                        | NOT IN SOI (see below)             | blank |
| government_grants       | NOT IN SOI (no Part VIII-1e field in any year 12-24)     | -                        | -                                  | blank; on NCCS rows (1e) |
| federated_campaigns, fundraising_event_contributions, related_org_contributions, other_contributions, noncash_contributions | NOT IN SOI | - | - | blank; on NCCS rows (1a,1c,1d,1f,1g) |
| program/management/fundraising_expenses | NOT IN SOI (extract carries Part IX column A only) | -          | -                                  | blank |

Extra x_ columns: x_soi_processing_year, x_efile (E/P or Y/N as filed), x_subseccd, x_soi_n_versions,
x_soi_versions_differ, x_soi_file; 990-PF: x_pf_operating_cd, x_pf_tax_yr_reported (SOI TAX_YR),
x_pf_disbursements_exempt_purpose (totexpnsexempt, I-26d: the main component of qualifying distributions),
x_pf_qlfydistrib_opfdn (qlfydistribtot, the Part XIV/XIII line 2e operating-foundation test; 0 for most
non-operating foundations, so it is NOT mapped to pf_qualifying_distributions), x_pf_distributable_amount
(distribamt), x_pf_net_investment_income (netinvstinc), x_pf_cash_nonint_eoy (othrcashamt),
x_pf_grants_approved_future (grntapprvfut, 13+). NCCS rows: x_nccs_file_year, x_nccs_n_returns (e-filed returns
for that EIN + tax_year before keeping the latest), x_period_from, x_return_version.
"""
from __future__ import annotations

import argparse
import calendar
import re
import sys
import zipfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import (CLEAN, INTERIM, RAW, latest_raw, log, norm_ein, raw_path, register_source, rel, save_raw,
                        session, sha256_file)

SOI_PAGE = "https://www.irs.gov/statistics/soi-tax-stats-annual-extract-of-tax-exempt-organization-financial-data"
IRS = "https://www.irs.gov"
SOURCE_ID = "bulk_irs_soi_extract"
OUT = INTERIM / "stage_fact_org_financials__soi.csv"
CALVARY = "521307706"
S = session()

ALIASES = {"tax_prd": "tax_pd", "taxprd": "tax_pd", "taxpd": "tax_pd", "a_tax_prd": "tax_pd",
           "elf": "efile", "e-file": "efile", "elfcd": "efile", "subcd": "subseccd"}

# fact field -> list of canonical SOI columns (summed when more than one); first-non-null lists in COALESCE
MAP = {
    "990": {
        "total_revenue": ["totrevenue"], "contributions_total": ["totcntrbgfts"],
        "program_service_revenue": ["totprgmrevnue"], "investment_income": ["invstmntinc"],
        "special_events_net": ["netincfndrsng"], "other_revenue": ["miscrevtot11e"],
        "total_expenses": ["totfuncexpns"],
        "grants_paid": ["grntstogovt", "grnsttoindiv", "grntstofrgngovt"],
        "compensation_total": ["compnsatncurrofcr", "compnsatnandothr", "othrsalwages", "pensionplancontrb",
                               "othremplyeebenef", "payrolltx"],
        "total_assets_eoy": ["totassetsend"], "total_liabilities_eoy": ["totliabend"],
        "net_assets_eoy": ["totnetassetend"], "cash_savings_eoy": ["nonintcashend", "svngstempinvend"],
    },
    "990EZ": {
        "total_revenue": ["totrevnue"], "contributions_total": ["totcntrbs"],
        "program_service_revenue": ["prgmservrev"], "membership_dues": ["duesassesmnts"],
        "investment_income": ["othrinvstinc"], "special_events_net": ["netincfndrsng"],
        "other_revenue": ["othrevnue"], "total_expenses": ["totexpns"],
        "total_assets_eoy": ["totassetsend"], "total_liabilities_eoy": ["totliabend"],
    },
    "990PF": {
        "total_revenue": ["totrcptperbks"], "contributions_total": ["grscontrgifts"],
        "investment_income": ["intrstrvnue", "dividndsamt"], "total_expenses": ["totexpnspbks"],
        "grants_paid": ["contrpdpbks"], "total_assets_eoy": ["totassetsend"], "total_liabilities_eoy": ["totliabend"],
        "net_assets_eoy": ["tfundnworth"], "pf_total_grants_paid": ["contrpdpbks"],
        "pf_contributions_received": ["grscontrgifts"],
        "x_pf_disbursements_exempt_purpose": ["totexpnsexempt"], "x_pf_qlfydistrib_opfdn": ["qlfydistribtot"],
        "x_pf_distributable_amount": ["distribamt"], "x_pf_net_investment_income": ["netinvstinc"],
        "x_pf_cash_nonint_eoy": ["othrcashamt"], "x_pf_grants_approved_future": ["grntapprvfut"],
    },
}
COALESCE = {
    "990EZ": {"net_assets_eoy": ["totnetassetsend", "networthend"]},
    "990PF": {"pf_fmv_assets_eoy": ["fairmrktvaleoy", "fairmrktvalamt"]},
}
CODE_COLS = {"990": ["efile", "subseccd"], "990EZ": ["efile", "subseccd"],
             "990PF": ["efile", "subseccd", "operatingcd", "tax_yr"]}

MONEY = ["total_revenue", "contributions_total", "federated_campaigns", "membership_dues",
         "fundraising_event_contributions", "related_org_contributions", "government_grants", "other_contributions",
         "noncash_contributions", "program_service_revenue", "investment_income", "special_events_net",
         "other_revenue", "total_expenses", "program_expenses", "management_expenses", "fundraising_expenses",
         "grants_paid", "compensation_total", "total_assets_eoy", "total_liabilities_eoy", "net_assets_eoy",
         "cash_savings_eoy", "pf_fmv_assets_eoy", "pf_total_grants_paid", "pf_qualifying_distributions",
         "pf_contributions_received"]
KEYS = ["ein", "tax_year", "fiscal_year", "fye_month", "tax_period_end", "return_type", "object_id", "is_amended",
        "source_id", "retrieved_date", "confidence", "basis"]


# ---------------------------------------------------------------- download
def page_links() -> list[str]:
    p = latest_raw("irs_soi", "annual_extract_page.html")
    if p is None:
        r = S.get(SOI_PAGE, timeout=60)
        r.raise_for_status()
        p = save_raw("irs_soi", "annual_extract_page", r.content, "html")
    txt = p.read_text(encoding="utf-8", errors="replace")
    return sorted(set(re.findall(r'href="(/pub/irs-soi/\d{2}eo[^"]*extract[^"]*\.(?:zip|xlsx|xls))"', txt)))


def stage_download():
    lines = []
    for href in page_links():
        fname = href.rsplit("/", 1)[-1]
        stem, ext = fname.rsplit(".", 1)
        old = latest_raw("irs_soi", fname)
        if old:
            lines.append(f"- reused {fname} -> {rel(old)}")
            continue
        p = raw_path("irs_soi", stem, ext)
        with S.get(IRS + href, stream=True, timeout=300) as r:
            r.raise_for_status()
            with open(p, "wb") as f:
                for chunk in r.iter_content(1 << 20):
                    f.write(chunk)
        lines.append(f"- downloaded {fname} -> {rel(p)} ({p.stat().st_size / 1e6:,.1f} MB, sha256 {sha256_file(p)[:12]})")
        print(lines[-1], flush=True)
    lines.append("- no 990-PF extract for processing years 17-19: not linked on the SOI page; "
                 "{17eofinextract990pf,18eoextract990pf,19eoextract990pf}.zip return 404; GT mirror has none")
    log("41_pull_soi_extracts: download", "\n".join(lines))


# ---------------------------------------------------------------- read + map
def extract_files() -> list[tuple[str, int, Path]]:
    out = []
    for p in sorted((RAW / "irs_soi").glob("*.zip")):
        m = re.search(r"_(\d{2})eo(?:fin)?extract(990pf|990ez|ez|990)\.zip$", p.name, re.I)
        if not m:
            continue
        kind = m.group(2).lower()
        form = {"990pf": "990PF", "990ez": "990EZ", "ez": "990EZ", "990": "990"}[kind]
        out.append((form, 2000 + int(m.group(1)), p))
    # keep the newest raw copy per (form, year)
    best = {}
    for form, yr, p in out:
        best[(form, yr)] = p if (form, yr) not in best or p.name > best[(form, yr)].name else best[(form, yr)]
    return sorted((f, y, p) for (f, y), p in best.items())


def canon(c: str) -> str:
    c = c.strip().lstrip("﻿").lower()
    return ALIASES.get(c, c)


def read_extract(form: str, path: Path, eins: set[str]) -> tuple[pd.DataFrame, int, list[str]]:
    want = {"ein", "tax_pd"} | set(CODE_COLS[form])
    for cols in MAP[form].values():
        want |= set(cols)
    for cols in COALESCE.get(form, {}).values():
        want |= set(cols)
    with zipfile.ZipFile(path) as z:
        member = z.infolist()[0]
        with z.open(member) as fh:
            first = fh.readline().decode("utf-8-sig", errors="replace")
        is_csv = "," in first
        header = [canon(c) or f"_blank{i}"  # the 20 990 CSV has 5 unnamed trailing columns
                  for i, c in enumerate(first.rstrip("\r\n").split(",") if is_csv else first.split())]
        present = [c for c in header if c in want]
        kw = dict(dtype=str, keep_default_na=False, chunksize=250_000, encoding="latin-1", header=0,
                  names=header, usecols=present)
        kw.update(sep=",") if is_csv else kw.update(sep=r"\s+")
        frames, n = [], 0
        with z.open(member) as fh:
            for ch in pd.read_csv(fh, **kw):
                n += len(ch)
                e = ch["ein"].str.strip().str.zfill(9)
                ch = ch[e.isin(eins)].copy()
                ch["ein"] = e[e.isin(eins)]
                frames.append(ch)
    df = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=present)
    return df, n, present


def num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s.astype(str).str.strip().replace({"": None}), errors="coerce")


def map_rows(form: str, df: pd.DataFrame, present: list[str]) -> pd.DataFrame:
    out = pd.DataFrame({"ein": df["ein"]})
    for field, cols in MAP[form].items():
        if all(c in present for c in cols):
            vals = pd.concat([num(df[c]) for c in cols], axis=1)
            out[field] = vals.sum(axis=1, min_count=1)
        else:
            out[field] = pd.NA
    for field, cols in COALESCE.get(form, {}).items():
        v = pd.Series(pd.NA, index=df.index, dtype="Float64")
        for c in cols:
            if c in present:
                v = v.fillna(num(df[c]))
        out[field] = v
    tp = df["tax_pd"].astype(str).str.strip().str[:6]
    out["x_tax_pd_raw"] = tp
    out["x_efile"] = df["efile"].str.strip() if "efile" in present else ""
    out["x_subseccd"] = df["subseccd"].str.strip() if "subseccd" in present else ""
    if form == "990PF":
        out["x_pf_operating_cd"] = df["operatingcd"].str.strip() if "operatingcd" in present else ""
        out["x_pf_tax_yr_reported"] = df["tax_yr"].str.strip() if "tax_yr" in present else ""
    return out


def period_fields(tp: pd.Series) -> pd.DataFrame:
    ok = tp.str.fullmatch(r"(19|20)\d{2}(0[1-9]|1[0-2])")
    yyyy = pd.to_numeric(tp.str[:4].where(ok), errors="coerce").astype("Int64")
    mm = pd.to_numeric(tp.str[4:6].where(ok), errors="coerce").astype("Int64")
    tax_year = yyyy.where(mm == 12, yyyy - 1)
    end = [f"{y}-{m:02d}-{calendar.monthrange(int(y), int(m))[1]:02d}" if pd.notna(y) else ""
           for y, m in zip(yyyy, mm)]
    return pd.DataFrame({"tax_year": tax_year, "fiscal_year": yyyy, "fye_month": mm, "tax_period_end": end},
                        index=tp.index)




def universe_eins() -> set[str]:
    u = pd.read_csv(CLEAN / "dim_universe_membership.csv", dtype=str, usecols=["ein"])
    return set(u.ein.map(norm_ein).dropna())


def finish(st: pd.DataFrame, source_id: str, confidence: str = "high", basis: str = "documented") -> pd.DataFrame:
    st = st.copy()
    for c in ("object_id", "is_amended"):
        if c not in st:
            st[c] = ""
    st["source_id"] = source_id
    st["confidence"] = confidence
    st["basis"] = basis
    for c in MONEY:
        if c not in st:
            st[c] = pd.NA
        st[c] = pd.to_numeric(st[c], errors="coerce").round().astype("Int64")
    for c in st.columns:
        if c.startswith("x_pf_") and c not in ("x_pf_operating_cd", "x_pf_tax_yr_reported"):
            st[c] = pd.to_numeric(st[c], errors="coerce").round().astype("Int64")
    return st


def build_soi(eins: set[str], lines: list[str]) -> pd.DataFrame:
    register_source(SOURCE_ID, "IRS SOI Annual Extract of Tax-Exempt Organization Financial Data", SOI_PAGE,
                    "Internal Revenue Service, Statistics of Income", "US government work, public domain",
                    "Yearly ZIPs {YY}eoextract990/990ez/990pf.zip (YY=12-24; no 990-PF for 17-19) + "
                    "{YY}eofinextractdoc. YY = processing year. Staged by scripts/41_pull_soi_extracts.py.")
    parts = []
    for form, yr, p in extract_files():
        df, n, present = read_extract(form, p, eins)
        m = map_rows(form, df, present)
        m["return_type"] = form
        m["x_soi_processing_year"] = yr
        m["x_soi_file"] = p.name.split("_", 1)[1]
        m["retrieved_date"] = pd.Timestamp(p.name[:8]).date().isoformat()
        m["_ord"] = range(len(m))
        missing = [f for f, cols in MAP[form].items() if not all(c in present for c in cols)]
        lines.append(f"- {form} {yr} ({p.name.split('_', 1)[1]}): {n:,} rows read, {len(m):,} universe rows"
                     + (f"; fields absent this year: {', '.join(missing)}" if missing else ""))
        print(lines[-1], flush=True)
        parts.append(m)
    allr = pd.concat(parts, ignore_index=True)
    allr = pd.concat([allr, period_fields(allr["x_tax_pd_raw"])], axis=1)
    bad = allr.fiscal_year.isna()
    if bad.any():
        lines.append(f"- dropped {int(bad.sum()):,} SOI rows with an unparseable tax period")
        allr = allr[~bad]
    # copies across processing years: keep the latest processing year, last row within a file
    allr = allr.sort_values(["x_soi_processing_year", "_ord"])
    g = allr.groupby(["ein", "tax_period_end", "return_type"])
    allr["x_soi_n_versions"] = g["ein"].transform("size")
    allr["x_soi_versions_differ"] = (g["total_revenue"].transform("nunique") > 1).astype(int)
    st = allr.drop_duplicates(["ein", "tax_period_end", "return_type"], keep="last").drop(columns="_ord")
    lines.append(f"- SOI: {len(st):,} rows, {st.ein.nunique():,} EINs; {len(allr) - len(st):,} older-processing-year "
                 f"copies dropped; {int((st.x_soi_versions_differ == 1).sum()):,} rows whose copies disagree on "
                 "total_revenue")
    return finish(st, SOURCE_ID)


# ---------------------------------------------------------------- NCCS e-file Part VIII (government grants)
NCCS_SOURCE_ID = "bulk_nccs_efile"
NCCS_EFILE = "https://nccs-efile.s3.us-east-1.amazonaws.com/parsed/F9-P08-T00-REVENUE-{y}.csv"
NCCS_PF_CORE = "https://nccsdata.s3.us-east-1.amazonaws.com/processed_merged/core/{y}/990pf/core_{y}_990pf.csv"
NCCS_YEARS = range(2009, 2023)  # 2023 returns 404 (recon)
NCCS_MAP = {  # Form 990 Part VIII column A
    "federated_campaigns": "F9_08_REV_CONTR_FED_CAMP",            # 1a
    "membership_dues": "F9_08_REV_CONTR_MEMBSHIP_DUE",            # 1b
    "fundraising_event_contributions": "F9_08_REV_CONTR_FUNDR_EVNT",  # 1c
    "related_org_contributions": "F9_08_REV_CONTR_RLTD_ORG",      # 1d
    "government_grants": "F9_08_REV_CONTR_GOVT_GRANT",            # 1e
    "other_contributions": "F9_08_REV_CONTR_OTH",                 # 1f
    "noncash_contributions": "F9_08_REV_CONTR_NONCSH",            # 1g (memo, included in 1a-1f)
    "contributions_total": "F9_08_REV_CONTR_TOT",                 # 1h
    "program_service_revenue": "F9_08_REV_PROG_TOT_TOT",          # 2g
    "investment_income": "F9_08_REV_OTH_INVEST_INCOME_TOT",       # 3
    "special_events_net": "F9_08_REV_OTH_FUNDR_NET_TOT",          # 8c
    "other_revenue": "F9_08_REV_MISC_TOT_TOT",                    # 11e
    "total_revenue": "F9_08_REV_TOT_TOT",                         # 12
}


def stage_nccs_download():
    """NCCS e-file Part VIII tables (the bulk source for Part VIII line 1e government grants, TY2009-TY2022),
    plus a HEAD check showing NCCS Core 990-PF has the same 2016-2018 gap as the SOI 990-PF extracts."""
    register_source(NCCS_SOURCE_ID, "NCCS E-file parsed tables: Form 990 Part VIII revenue (F9-P08-T00-REVENUE)",
                    "https://nccs.urban.org/nccs/catalogs/catalog-efile.html",
                    "Urban Institute, National Center for Charitable Statistics",
                    "ODC-BY per Urban Institute data catalog; cite NCCS",
                    "parsed/F9-P08-T00-REVENUE-{2009..2022}.csv on nccs-efile S3; one row per e-filed return "
                    "(OBJECTID), TAX_YEAR = IRS tax year. Used for government_grants and the Part VIII "
                    "contribution lines that the SOI extract lacks. Staged by scripts/41_pull_soi_extracts.py.")
    lines = []
    for y in NCCS_YEARS:
        name = f"F9-P08-T00-REVENUE-{y}"
        old = latest_raw("nccs", f"{name}.csv")
        if old:
            lines.append(f"- reused {name}.csv -> {rel(old)}")
            continue
        p = raw_path("nccs", name, "csv")
        with S.get(NCCS_EFILE.format(y=y), stream=True, timeout=600) as r:
            r.raise_for_status()
            with open(p, "wb") as f:
                for chunk in r.iter_content(1 << 22):
                    f.write(chunk)
        lines.append(f"- downloaded {name}.csv -> {rel(p)} ({p.stat().st_size / 1e6:,.1f} MB)")
        print(lines[-1], flush=True)
    rows = []
    for y in range(2012, 2025):
        r = S.head(NCCS_PF_CORE.format(y=y), timeout=60)
        rows.append({"year": y, "url": NCCS_PF_CORE.format(y=y), "status": r.status_code,
                     "bytes": int(r.headers.get("Content-Length", 0) or 0),
                     "last_modified": r.headers.get("Last-Modified", "")})
    p = save_raw("nccs", "core_990pf_head_check", rows)
    lines.append(f"- NCCS Core 990-PF merged file sizes ({rel(p)}): "
                 + "; ".join(f"{x['year']} {x['bytes'] / 1e6:.1f} MB" for x in rows))
    lines.append("- NCCS Core 990-PF 2016-2018 files are 0.5-8.6 MB vs 69-84 MB in other years: the same gap as the "
                 "SOI 990-PF extracts, so no NCCS 990-PF download")
    log("41_pull_soi_extracts: nccs_download", "\n".join(lines))


def irs_index_periods(eins: set[str]) -> pd.DataFrame:
    """OBJECT_ID -> TAX_PERIOD from the IRS e-file index CSVs (releases 2021-2026) already in raw/irs_xml_index/."""
    frames = []
    for yr in range(2021, 2027):
        p = latest_raw("irs_xml_index", f"index_{yr}.csv")
        if p is None:
            continue
        d = pd.read_csv(p, dtype=str, usecols=["EIN", "TAX_PERIOD", "RETURN_TYPE", "OBJECT_ID"],
                        keep_default_na=False, encoding="utf-8", encoding_errors="replace")
        d["ein"] = d.EIN.str.strip().str.zfill(9)
        frames.append(d[d.ein.isin(eins) & (d.RETURN_TYPE == "990")][["OBJECT_ID", "TAX_PERIOD"]])
    return pd.concat(frames).drop_duplicates("OBJECT_ID") if frames else pd.DataFrame(columns=["OBJECT_ID",
                                                                                              "TAX_PERIOD"])


def build_nccs(eins: set[str], soi: pd.DataFrame, lines: list[str]) -> pd.DataFrame:
    """Part VIII rows for universe 990 e-filers. NCCS has TAX_YEAR but no period end, so the period comes from the
    SOI 990 row for the same EIN + tax_year (x_period_from=soi), else from the IRS e-file index by OBJECT_ID
    (x_period_from=irs_index); rows with neither are dropped. The XML omits zero lines, so absent Part VIII lines are
    filled with 0 when the return reports line 12 (total revenue)."""
    cols = ["OBJECTID", "ORG_EIN", "RETURN_TYPE", "TAX_YEAR", "RETURN_VERSION"] + list(NCCS_MAP.values())
    parts = []
    for y in NCCS_YEARS:
        p = latest_raw("nccs", f"F9-P08-T00-REVENUE-{y}.csv")
        if p is None:
            lines.append(f"- NCCS {y}: raw file missing (run --only nccs_download)")
            continue
        n = kept = 0
        for ch in pd.read_csv(p, dtype=str, usecols=cols, chunksize=250_000, encoding="utf-8",
                              encoding_errors="replace"):
            n += len(ch)
            e = ch.ORG_EIN.str.strip().str.zfill(9)
            keep = e.isin(eins) & (ch.RETURN_TYPE.str.strip() == "990")
            ch = ch[keep].copy()
            ch["ein"] = e[keep]
            ch["retrieved_date"] = pd.Timestamp(p.name[:8]).date().isoformat()
            ch["x_nccs_file_year"] = y
            kept += len(ch)
            parts.append(ch)
        lines.append(f"- NCCS {y}: {n:,} rows read, {kept:,} universe 990 rows")
        print(lines[-1], flush=True)
    if not parts:
        return pd.DataFrame()
    d = pd.concat(parts, ignore_index=True)
    d["object_id"] = d.OBJECTID.str.extract(r"(\d{18})$")[0]
    d["tax_year"] = pd.to_numeric(d.TAX_YEAR, errors="coerce").astype("Int64")
    out = d[["ein", "object_id", "tax_year", "retrieved_date", "x_nccs_file_year"]].copy()
    out["x_return_version"] = d.RETURN_VERSION
    for f, c in NCCS_MAP.items():
        out[f] = pd.to_numeric(d[c], errors="coerce")
    has12 = out.total_revenue.notna()
    for f in NCCS_MAP:
        if f != "total_revenue":
            out.loc[has12, f] = out.loc[has12, f].fillna(0)
    # one return per EIN + tax_year: the latest-filed OBJECT_ID (amended/superseding returns are filed later)
    out = out.sort_values(["ein", "tax_year", "object_id"])
    out["x_nccs_n_returns"] = out.groupby(["ein", "tax_year"]).ein.transform("size")
    out = out.drop_duplicates(["ein", "tax_year"], keep="last")
    # period end
    s9 = soi[soi.return_type == "990"].drop_duplicates(["ein", "tax_year"], keep="last")[
        ["ein", "tax_year", "tax_period_end", "fiscal_year", "fye_month", "total_revenue"]].rename(
        columns={"total_revenue": "_soi_rev"})
    out = out.merge(s9, on=["ein", "tax_year"], how="left")
    out["x_period_from"] = out.tax_period_end.notna().map({True: "soi", False: ""})
    miss = out.tax_period_end.isna()
    if miss.any():
        idx = irs_index_periods(eins).rename(columns={"OBJECT_ID": "object_id"})
        fill = out.loc[miss, ["object_id"]].merge(idx, on="object_id", how="left")
        pf = period_fields(fill.TAX_PERIOD.fillna("").astype(str).str[:6])
        pf.index = out.index[miss]
        ok = pf.fiscal_year.notna() & (pf.tax_year == out.loc[miss, "tax_year"])
        for c in ("tax_period_end", "fiscal_year", "fye_month"):
            out.loc[pf.index[ok], c] = pf.loc[ok, c]
        out.loc[pf.index[ok], "x_period_from"] = "irs_index"
    n_drop = int(out.tax_period_end.isna().sum())
    rev_match = (out._soi_rev == out.total_revenue)[out._soi_rev.notna()]
    out = out[out.tax_period_end.notna()].drop(columns="_soi_rev")
    out["return_type"] = "990"
    out["fiscal_year"] = out.fiscal_year.astype("Int64")
    out["fye_month"] = out.fye_month.astype("Int64")
    lines += [
        f"- NCCS: {len(out):,} rows staged, {out.ein.nunique():,} EINs, tax years "
        f"{int(out.tax_year.min())}-{int(out.tax_year.max())}; period from SOI match "
        f"{int((out.x_period_from == 'soi').sum()):,}, from IRS index {int((out.x_period_from == 'irs_index').sum()):,}; "
        f"dropped {n_drop:,} with no period; {int((out.x_nccs_n_returns > 1).sum()):,} EIN-years had >1 return "
        "(kept the latest OBJECT_ID)",
        f"- NCCS total_revenue equals SOI total_revenue on {rev_match.mean():.1%} of {len(rev_match):,} matched rows",
    ]
    return finish(out, NCCS_SOURCE_ID)


# ---------------------------------------------------------------- write + QC
def stage_build():
    eins = universe_eins()
    lines = [f"- universe EINs: {len(eins):,}"]
    soi = build_soi(eins, lines)
    nc = build_nccs(eins, soi, lines)
    st = pd.concat([soi, nc], ignore_index=True) if len(nc) else soi
    xcols = sorted(c for c in st.columns if c.startswith("x_"))
    st = st[KEYS + MONEY + xcols].sort_values(["ein", "tax_period_end", "return_type", "source_id"])
    st.to_csv(OUT, index=False)

    dup = st.duplicated(["ein", "tax_period_end", "return_type", "source_id"]).sum()
    qc = []
    for sid in (SOURCE_ID, NCCS_SOURCE_ID):
        cal = st[(st.ein == CALVARY) & (st.source_id == sid)].set_index("tax_year")
        for ty, want in {2020: 3_851_984, 2021: 8_867_250}.items():
            got = cal.total_revenue.get(ty)
            qc.append(f"{sid} TY{ty} " + ("not present" if got is None or pd.isna(got) else
                                          f"{int(got):,} {'OK' if got == want else 'MISMATCH (want ' + format(want, ',') + ')'}"))
    s = st[st.source_id == SOURCE_ID]
    pf = s[s.return_type == "990PF"]
    tyr = pd.to_numeric(pf.x_pf_tax_yr_reported, errors="coerce")
    lines += [
        f"- wrote {len(st):,} rows to {rel(OUT)} (SOI {len(s):,}; NCCS {len(st) - len(s):,})",
        f"- duplicate (ein, tax_period_end, return_type, source_id): {dup}",
        f"- Calvary total_revenue QC: {'; '.join(qc)}",
        f"- 990-PF SOI TAX_YR equals derived tax_year on {(tyr == pf.tax_year).mean():.1%} of rows",
        "- rows by fiscal_year (period-end year) x return_type / source:",
        "```", pd.crosstab(st.fiscal_year, [st.source_id.str.replace("bulk_", ""), st.return_type],
                           margins=True).to_string(), "```",
    ]
    u = pd.read_csv(CLEAN / "dim_universe_membership.csv", dtype=str, usecols=["universe", "ein"])
    for sid, d in st.groupby("source_id"):
        have = d.groupby("ein").fiscal_year.nunique()
        lines.append(f"- coverage, {sid} (EINs with >=1 row / universe EINs; org-years; median years per covered org):")
        for name, grp in u.groupby("universe"):
            h = have[have.index.isin(set(grp.ein))]
            lines.append(f"  - {name}: {len(h):,}/{grp.ein.nunique():,}; {int(h.sum()):,}; "
                         f"{h.median() if len(h) else 0:.0f}")
    log("41_pull_soi_extracts: stage", "\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="download,nccs_download,stage")
    a = ap.parse_args()
    todo = a.only.split(",")
    if "download" in todo:
        stage_download()
    if "nccs_download" in todo:
        stage_nccs_download()
    if "stage" in todo:
        stage_build()
