"""Cached reference data shared by Phase 5 scripts (regenerable; cache lives in interim/)."""
from __future__ import annotations

import pandas as pd

from .common import INTERIM, latest_raw, norm_ein, norm_name

BMF_COLS = ["EIN", "NAME", "ICO", "STREET", "CITY", "STATE", "ZIP", "SUBSECTION", "FOUNDATION", "RULING",
            "NTEE_CD", "REVENUE_AMT", "ASSET_AMT", "TAX_PERIOD", "PF_FILING_REQ_CD"]


def bmf_national(refresh: bool = False) -> pd.DataFrame:
    """National EO BMF (eo1-eo4) with ein, name_norm, city_norm, zip5, ntee3. Cached as a pickle."""
    cache = INTERIM / "bmf_national.pkl"
    srcs = [latest_raw("irs_bmf", f"eo{i}.csv") for i in range(1, 5)]
    if cache.exists() and not refresh and all(cache.stat().st_mtime > s.stat().st_mtime for s in srcs):
        return pd.read_pickle(cache)
    b = pd.concat([pd.read_csv(s, dtype=str, usecols=BMF_COLS, keep_default_na=False) for s in srcs],
                  ignore_index=True)
    b["ein"] = b.EIN.map(norm_ein)
    b = b.drop_duplicates("ein").drop(columns=["EIN"])
    b["name_norm"] = b.NAME.map(norm_name)
    b["city_norm"] = b.CITY.str.upper().str.replace(r"[^A-Z ]", "", regex=True).str.strip()
    b["zip5"] = b.ZIP.str[:5]
    b["ntee3"] = b.NTEE_CD.str[:3]
    b.to_pickle(cache)
    return b


def city_norm(s: pd.Series) -> pd.Series:
    return s.fillna("").astype(str).str.upper().str.replace(r"[^A-Z ]", "", regex=True).str.strip()
