"""Phase 3: match organizations named as Calvary funders (CRM export, annual reports, support page) to EINs.

Matching tiers, applied in order to the national EO BMF:
  exact_name_state   normalized name equal, same state (when the source gives a state)       score 100
  exact_name_unique  normalized name equal, single national hit (or a single DMV hit)        score 97
  fuzzy_name_state   rapidfuzz token_sort_ratio >= 92 within the stated state (or DC/MD/VA)  score = ratio
  manual             config/funder_match_overrides.csv (accept yes/inferred/no)
  corp_foundation    "<name> foundation" / "<name> charitable foundation" exact, for corporate names;
                     inferred link from a company to its foundation                           accept=inferred
Rows typed as government or anonymous are skipped. Matches with accept in (yes, inferred) enter universe
calvary_known_funders (rule KF1) so their 990-PF / Schedule I filings are parsed.

Output: interim/known_funder_matches.csv
Usage: python scripts/22_match_known_funders.py
"""
import sys
from pathlib import Path

import pandas as pd
from rapidfuzz import fuzz, process

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import INTERIM, RAW, latest_raw, log, norm_ein, norm_name

SKIP_TYPES = {"government", "intergovernmental", "anonymous"}
DMV = {"DC", "MD", "VA"}


def load_names() -> pd.DataFrame:
    crm = pd.read_csv(RAW / "inputs_extracted" / "crm_funders_2023_2026.csv", dtype=str)
    crm = crm.rename(columns={"last_name": "name_raw", "org_type_guess": "type_guess"})[
        ["name_raw", "city", "state", "type_guess", "source_id"]]
    fm = pd.read_csv(RAW / "inputs_extracted" / "funder_mentions.csv", dtype=str)
    fm = fm[fm.truncated.astype(str).str.lower() != "true"]
    fm = fm.rename(columns={"funder_name_raw": "name_raw", "org_type_guess": "type_guess"})[
        ["name_raw", "type_guess", "source_id"]].assign(city="", state="")
    allr = pd.concat([crm, fm], ignore_index=True).fillna("")
    allr = allr[~allr.type_guess.isin(SKIP_TYPES)]
    allr["name_norm"] = allr.name_raw.map(norm_name)
    allr = allr[allr.name_norm != ""]
    # one row per (name_norm, state); keep provenance
    g = allr.groupby(["name_norm", "state"], as_index=False).agg(
        name_raw=("name_raw", "first"), city=("city", "first"), type_guess=("type_guess", "first"),
        source_ids=("source_id", lambda s: ";".join(sorted(set(s)))))
    # a name seen with and without state: keep only the stated-state row
    stated = set(g[g.state != ""].name_norm)
    return g[(g.state != "") | ~g.name_norm.isin(stated)].reset_index(drop=True)


def main():
    names = load_names()
    cols = ["EIN", "NAME", "CITY", "STATE", "FOUNDATION", "SUBSECTION", "ASSET_AMT", "REVENUE_AMT", "NTEE_CD"]
    bmf = pd.concat([pd.read_csv(latest_raw("irs_bmf", f"eo{i}.csv"), dtype=str, usecols=cols, keep_default_na=False)
                     for i in range(1, 5)], ignore_index=True)
    bmf["ein"] = bmf.EIN.map(norm_ein)
    bmf["name_norm"] = bmf.NAME.map(norm_name)
    bmf["assets"] = pd.to_numeric(bmf.ASSET_AMT, errors="coerce").fillna(0)
    by_name = bmf.groupby("name_norm")
    ovp = Path(__file__).resolve().parents[1] / "config" / "funder_match_overrides.csv"
    overrides = {r.name_norm: r for r in pd.read_csv(ovp, dtype=str).itertuples()} if ovp.exists() else {}

    def pick(hits: pd.DataFrame) -> pd.Series:
        return hits.sort_values("assets", ascending=False).iloc[0]

    out = []
    for r in names.itertuples():
        res = {"name_raw": r.name_raw, "name_norm": r.name_norm, "city": r.city, "state": r.state,
               "type_guess": r.type_guess, "source_ids": r.source_ids}
        hits = by_name.get_group(r.name_norm) if r.name_norm in by_name.groups else bmf.iloc[0:0]
        m = None
        if r.state and len(hits[hits.STATE == r.state]):
            m, how, score = pick(hits[hits.STATE == r.state]), "exact_name_state", 100
        elif len(hits) == 1 or (len(hits) > 1 and len(hits[hits.STATE.isin(DMV)]) == 1):
            m = hits.iloc[0] if len(hits) == 1 else hits[hits.STATE.isin(DMV)].iloc[0]
            how, score = "exact_name_unique", 97
        if m is None:
            pool = bmf[bmf.STATE == r.state] if r.state else bmf[bmf.STATE.isin(DMV)]
            tok = r.name_norm.split()[0]
            pool = pool[pool.name_norm.str.split().str[0] == tok]   # first word must agree
            best = process.extractOne(r.name_norm, pool.name_norm, scorer=fuzz.token_sort_ratio, score_cutoff=92)
            if best:
                m, how, score = pool.loc[best[2]], "fuzzy_name_state", round(best[1], 1)
        accept = "yes" if m is not None else "no"
        if m is None and r.type_guess in ("corporate", "corporation", "corporate_matching", "corporate_foundation"):
            for suffix in ("foundation", "charitable foundation", "foundation inc", "giving foundation"):
                key = norm_name(f"{r.name_raw} {suffix}")
                if key in by_name.groups:
                    m, how, score, accept = pick(by_name.get_group(key)), "corp_foundation", 90, "inferred"
                    break
        ov = overrides.get(r.name_norm)
        if ov is not None:
            if ov.ein == "none":
                m, how, score, accept = None, "manual_reject", 0, "no"
            else:
                hit = bmf[bmf.ein == norm_ein(ov.ein)]
                m = hit.iloc[0] if len(hit) else None
                how, score, accept = "manual", 100, ov.accept
        if m is not None:
            res.update(ein=m.ein, bmf_name=m.NAME, bmf_city=m.CITY, bmf_state=m.STATE, foundation_code=m.FOUNDATION,
                       subsection=m.SUBSECTION, ntee_cd=m.NTEE_CD, match_method=how, match_score=score, accept=accept)
        else:
            res.update(match_method=how if ov is not None else "unmatched", match_score=0, accept="no")
        res["confidence"] = {"exact_name_state": "high", "manual": "high", "exact_name_unique": "medium",
                             "fuzzy_name_state": "medium", "corp_foundation": "low"}.get(res["match_method"], "")
        if res["match_method"] == "manual" and res.get("accept") == "inferred":
            res["confidence"] = "medium"
        if res["match_method"] == "exact_name_unique" and r.state and res.get("bmf_state") != r.state:
            res["confidence"] = "low" if res.get("bmf_state") not in DMV else "medium"
            res["notes"] = f"source state {r.state} vs BMF state {res.get('bmf_state')}"
        out.append(res)
    o = pd.DataFrame(out)
    o.to_csv(INTERIM / "known_funder_matches.csv", index=False)
    summ = o.groupby(["match_method", "accept"]).size().to_dict()
    log("22_match_known_funders", f"- names {len(o)}; outcomes {summ}; accepted EINs "
        f"{o[o.accept.isin(['yes', 'inferred'])].ein.nunique()}")
    print(summ)
    print(o[o.accept != "no"][["name_raw", "state", "bmf_name", "bmf_state", "match_method", "match_score"]]
          .head(60).to_string(index=False))


if __name__ == "__main__":
    main()
