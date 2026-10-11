"""Phase 5: resolve organization names in staged grant and award rows to EINs; build clean/entity_aliases.csv.

Names come from every interim/stage_fact_grants__*.csv (recipients and funders) and
interim/stage_fact_gov_awards__*.csv (recipients, pass-through entities). Matching is per unique
(name_norm, city, state) against the national EO BMF, in tier order:
  exact_ein           an EIN given in the source that exists in the BMF (Schedule I recipient EIN, filer EIN)
  manual              config/funder_match_overrides.csv
  exact_name_city     normalized name + city + state equal (unique, or largest by assets)
  known_funder        reviewed match from interim/known_funder_matches.csv (scripts/22), funders only
  exact_name_state    normalized name + state equal, unique in state
  exact_name_national normalized name unique nationally, source gives no state
  fuzzy_name_city     rapidfuzz token_sort_ratio >= 92, same state + city, first word equal
  unmatched
Outputs:
  interim/name_resolution.csv   (role, name_norm, city_norm, state) -> ein, match_method, match_score
  clean/entity_aliases.csv      one row per observed raw variant -> canonical entity
Usage: python scripts/61_resolve_entities.py
"""
import sys
from pathlib import Path

import pandas as pd
from rapidfuzz import fuzz, process

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import CLEAN, CONFIG, INTERIM, log, norm_ein, norm_name
from lib.refdata import bmf_national, city_norm


def collect() -> pd.DataFrame:
    parts = []
    for p in sorted(INTERIM.glob("stage_fact_grants__*.csv")):
        g = pd.read_csv(p, dtype=str, keep_default_na=False)
        rec = pd.DataFrame({"role": "recipient", "name_raw": g.get("recipient_name_raw", ""),
                            "city": g.get("recipient_city", ""), "state": g.get("recipient_state", ""),
                            "given_ein": g.get("recipient_ein", ""), "source_id": g.get("source_id", "")})
        fun = pd.DataFrame({"role": "funder", "name_raw": g.get("funder_name_raw", ""),
                            "city": g.get("x_funder_city", ""), "state": g.get("x_funder_state", ""),
                            "given_ein": g.get("funder_ein", ""), "source_id": g.get("source_id", "")})
        parts += [rec, fun]
    for p in sorted(INTERIM.glob("stage_fact_gov_awards__*.csv")):
        g = pd.read_csv(p, dtype=str, keep_default_na=False)
        if "__dc" in p.name and "x_recipient_state" not in g:
            g["x_recipient_state"] = "DC"   # DC award lists name DC-area providers without an address
        parts.append(pd.DataFrame({"role": "recipient", "name_raw": g.get("recipient_name_raw", ""),
                                   "city": g.get("x_recipient_city", ""), "state": g.get("x_recipient_state", ""),
                                   "given_ein": g.get("recipient_ein", ""), "source_id": g.get("source_id", "")}))
        if "pass_through_entity" in g:
            parts.append(pd.DataFrame({"role": "pass_through", "name_raw": g.pass_through_entity, "city": "",
                                       "state": "", "given_ein": g.get("pass_through_ein", ""),
                                       "source_id": g.get("source_id", "")}))
    n = pd.concat(parts, ignore_index=True).fillna("")
    n = n[n.name_raw.str.strip() != ""]
    n["name_norm"] = n.name_raw.map(norm_name)
    n["city_norm"] = city_norm(n.city)
    n["state"] = n.state.str.upper().str.strip()
    n["given_ein"] = n.given_ein.map(lambda e: norm_ein(e) or "")
    return n


def main():
    names = collect()
    bmf = bmf_national()
    bmf["assets"] = pd.to_numeric(bmf.ASSET_AMT, errors="coerce").fillna(0)
    ein_set = set(bmf.ein)
    ov = pd.read_csv(CONFIG / "funder_match_overrides.csv", dtype=str)
    overrides = {r.name_norm: r for r in ov.itertuples()}

    # deterministic representative spelling per key (input order varies with multiprocessing in scripts/50)
    names = names.sort_values(["role", "name_norm", "city_norm", "state", "given_ein", "name_raw", "source_id"],
                              kind="mergesort")
    keys = names.groupby(["role", "name_norm", "city_norm", "state", "given_ein"], as_index=False).agg(
        n_occurrences=("name_raw", "size"), name_raw=("name_raw", "first"),
        source_ids=("source_id", lambda s: ";".join(sorted(set(s))[:5])))
    by_ncs = bmf.sort_values("assets", ascending=False).drop_duplicates(["name_norm", "city_norm", "STATE"]) \
                .set_index(["name_norm", "city_norm", "STATE"]).ein.to_dict()
    kfm = pd.read_csv(INTERIM / "known_funder_matches.csv", dtype=str)
    kfm = kfm[kfm.accept.isin(["yes", "inferred"])]
    known = {r.name_norm: (norm_ein(r.ein), r.match_method) for r in kfm.itertuples()}
    n_counts = bmf.groupby("name_norm").ein.agg(["first", "size"])
    by_n = n_counts[n_counts["size"] == 1]["first"].to_dict()
    ns_counts = bmf.groupby(["name_norm", "STATE"]).ein.agg(["first", "size"])
    by_ns = ns_counts[ns_counts["size"] == 1]["first"].to_dict()
    # fuzzy candidates indexed by (state, city, first word of name) -> (names, eins)
    bmf["tok0"] = bmf.name_norm.str.split().str[0].fillna("")
    pools = {k: (g.name_norm.tolist(), g.ein.tolist()) for k, g in bmf.groupby(["STATE", "city_norm", "tok0"])}

    res = []
    for r in keys.itertuples():
        ein, how, score = "", "unmatched", 0.0
        if r.given_ein and r.given_ein in ein_set:
            ein, how, score = r.given_ein, "exact_ein", 100
        elif r.name_norm in overrides:
            o = overrides[r.name_norm]
            if o.ein != "none":
                ein, how, score = norm_ein(o.ein), "manual", 100
            else:
                how = "manual_reject"
        elif r.role == "funder" and r.name_norm in known:
            ein, how, score = known[r.name_norm][0], "known_funder", 95
        elif (r.name_norm, r.city_norm, r.state) in by_ncs:
            ein, how, score = by_ncs[(r.name_norm, r.city_norm, r.state)], "exact_name_city", 100
        elif (r.name_norm, r.state) in by_ns:
            ein, how, score = by_ns[(r.name_norm, r.state)], "exact_name_state", 97
        elif not r.state and r.name_norm in by_n and len(r.name_norm.split()) >= 2:
            ein, how, score = by_n[r.name_norm], "exact_name_national", 90
        else:
            if r.name_norm and r.state:
                names_, eins_ = pools.get((r.state, r.city_norm, r.name_norm.split()[0]), ([], []))
                best = process.extractOne(r.name_norm, names_, scorer=fuzz.token_sort_ratio,
                                          score_cutoff=92) if names_ else None
                if best:
                    ein, how, score = eins_[best[2]], "fuzzy_name_city", round(best[1], 1)
        res.append((ein, how, score))
    keys[["ein", "match_method", "match_score"]] = pd.DataFrame(res, index=keys.index)
    keys.to_csv(INTERIM / "name_resolution.csv", index=False)

    from lib.privacy import person_like
    drop = (keys.ein == "") & (keys.role == "recipient") & keys.name_raw.map(person_like)
    keys = keys[~drop]   # individuals: never written to entity_aliases or name_resolution
    keys.to_csv(INTERIM / "name_resolution.csv", index=False)
    canon = bmf.set_index("ein").NAME.to_dict()
    al = keys.assign(entity_kind=keys.role.map({"funder": "funder"}).fillna("org"),
                     canonical_id=keys.ein,
                     canonical_name=keys.ein.map(canon).fillna(""),
                     alias_name_raw=keys.name_raw, alias_name_norm=keys.name_norm,
                     alias_city=keys.city_norm.str.title(), alias_state=keys.state)
    al = al.groupby(["alias_name_raw", "alias_name_norm", "alias_city", "alias_state", "entity_kind", "canonical_id",
                     "canonical_name", "match_method", "match_score"], as_index=False).agg(
        n_occurrences=("n_occurrences", "sum"), source_ids=("source_ids", "first"))
    al.to_csv(CLEAN / "entity_aliases.csv", index=False)

    stats = keys.groupby(["role", "match_method"]).n_occurrences.sum().unstack(fill_value=0)
    log("61_resolve_entities", f"- unique name keys {len(keys):,}; alias rows {len(al):,}\n- occurrences by method:\n"
        + stats.to_string())
    print(stats.to_string())


if __name__ == "__main__":
    main()
