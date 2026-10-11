"""Phase 5: people (dim_person, fact_roles, candidate_interlocks) and fact_org_relationships.

People. Role rows come from interim/stage_fact_roles__*.csv (990 Part VII-A, 990-EZ, 990-PF officers, and
board lists in Calvary's annual reports). Names are normalized (case, punctuation, honorifics, suffixes);
first / middle initial / last / suffix are parsed.
  - Within one organization, the same normalized name across years is one person (filings carry no ids,
    but the same name on the same board is the standard assumption).
  - Across organizations, two people are linked only when the normalized names match exactly AND at least
    one corroborating signal holds:
        same_metro      both organizations in the DC MSA (DC/MD/VA counties of CBSA 47900)
        overlap_years   role years overlap (within 1 year)
        middle_initial  both records carry the same middle initial
        suffix          both records carry the same suffix
    Common names (first+last shared by people at > 5 organizations in the role data) need two signals,
    one of them middle_initial or suffix. Links that fail go to clean/candidate_interlocks.csv for review.
  - match_confidence: high = middle_initial/suffix + another signal; medium = one signal on an uncommon
    name or two non-name signals; low = candidate only.

Relationships (fact_org_relationships):
  grant                 funder EIN -> recipient EIN, per tax year, summed from fact_grants (non-cumulative rows)
  daf_sponsor_grant     same, when the funder is a DAF sponsor (universe daf_sponsors)
  pass_through_funding  pass-through EIN -> recipient EIN from fact_gov_awards
  schedule_r_related    from interim/stage_fact_org_relationships__*.csv
  shared_board_member   organizations sharing a linked person (board member, officer, key employee, foundation
                        trustee, or person listed in Calvary's reports incl. staff); confidence = the
                        person-level match confidence; signals in notes

Usage: python scripts/64_people_relationships.py
"""
import hashlib
import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import CLEAN, CONFIG, INTERIM, log, norm_ein, today
def fold_notes(df, xcols):
    """Fold x_* columns into one 'k=v; k=v' string per row (vectorized)."""
    out = pd.Series("", index=df.index)
    for c in xcols:
        v = df[c].fillna("").astype(str).fillna("")   # pandas 3 keeps NaN through astype(str)
        keep = ~v.isin(["", "nan", "<NA>", "None"])
        piece = (c[2:] + "=" + v).where(keep, "")
        sep = pd.Series(np.where((out != "") & keep, "; ", ""), index=df.index)
        out = out + sep + piece
    return out


from lib.specs import columns

HONORIFIC = {"mr", "mrs", "ms", "miss", "dr", "rev", "reverend", "hon", "honorable", "sister", "father", "prof", "the"}
SUFFIX = {"jr", "sr", "ii", "iii", "iv", "v", "esq", "phd", "md", "cpa", "jd", "mba", "dds", "rn", "cfp", "pe"}


def parse_name(raw: str):
    s = re.sub(r"\(.*?\)", " ", str(raw or "")).lower()
    s = re.sub(r"[^a-z\s,'-]", " ", s).replace("'", "")
    if "," in s:   # "last, first middle" -> "first middle last"
        a, _, b = s.partition(",")
        if b.strip() and not set(b.split()) <= SUFFIX:
            s = f"{b} {a}"
    toks = [t.strip("-") for t in s.replace(",", " ").split() if t.strip("-")]
    toks = [t for t in toks if t not in HONORIFIC]
    suffix = " ".join(t for t in toks if t in SUFFIX)
    toks = [t for t in toks if t not in SUFFIX]
    if not toks:
        return "", "", "", "", ""
    first, last = toks[0], toks[-1] if len(toks) > 1 else ""
    mids = toks[1:-1]
    mi = mids[0][0] if mids else ""
    norm = " ".join([first] + ([mi] if mi else []) + ([last] if last else []) + ([suffix] if suffix else []))
    return norm, first, mi, last, suffix


def pid(*parts) -> str:
    return "P" + hashlib.sha1("|".join(parts).encode()).hexdigest()[:10]


def read(p):
    return pd.read_csv(p, dtype=str, keep_default_na=False, low_memory=False) if Path(p).exists() else pd.DataFrame()


def people():
    frames = [read(p).assign(x_stage_file=p.name) for p in sorted(INTERIM.glob("stage_fact_roles__*.csv"))]
    r = pd.concat([f for f in frames if len(f)], ignore_index=True) if frames else pd.DataFrame()
    if r.empty:
        return r, pd.DataFrame(), pd.DataFrame()
    r["ein"] = r.ein.map(norm_ein)
    parsed = r.name_display.map(parse_name)
    r["name_norm"], r["first_name"], r["middle_initial"], r["last_name"], r["suffix"] = zip(*parsed)
    r = r[r.name_norm != ""]
    r["yr"] = pd.to_numeric(r.tax_year.replace("", np.nan), errors="coerce").fillna(
        pd.to_numeric(r.fiscal_year.replace("", np.nan), errors="coerce") - 1)
    # prefer XML over PDF for the same org/year/person
    r["_rank"] = r.source_id.map(lambda s: 1 if str(s).startswith("bulk_") else 2)
    # deterministic order (input order varies with multiprocessing in scripts/50): the same person listed twice in
    # one return with different titles keeps the same row on every run
    sort_cols = [c for c in ["_rank", "ein", "yr", "name_norm", "role_type", "title", "avg_hours_per_week",
                             "reportable_comp_org", "name_display", "source_id", "object_id"] if c in r]
    rest = sorted(c for c in r.columns if c not in sort_cols and c != "yr")
    r = r.sort_values(sort_cols + rest, kind="mergesort", na_position="last")   # full-row order: no ties left
    r = r.drop_duplicates(["ein", "yr", "name_norm", "role_type"], keep="first")

    org = read(CLEAN / "dim_org.csv").set_index("ein") if (CLEAN / "dim_org.csv").exists() else pd.DataFrame()
    msa = pd.read_csv(CONFIG / "dmv_counties.csv", dtype=str)
    msa_fips = set(msa[msa.in_msa == "true"].county_geoid)
    in_msa = r.ein.map(org.county_fips).isin(msa_fips) if len(org) else pd.Series(False, index=r.index)
    r["in_msa"] = in_msa.values

    # within-org person keys
    r["org_person"] = r.ein + "|" + r.name_norm
    op = r.groupby("org_person").agg(ein=("ein", "first"), name_norm=("name_norm", "first"),
                                     first=("first_name", "first"), last=("last_name", "first"),
                                     mi=("middle_initial", "first"), suffix=("suffix", "first"),
                                     ymin=("yr", "min"), ymax=("yr", "max"), in_msa=("in_msa", "first"))
    fl = op["first"] + " " + op["last"]
    common = fl.map(op.groupby(fl).ein.nunique()) > 5

    parent = {k: k for k in op.index}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    cands, links = [], []
    for name, grp in op.groupby("name_norm"):
        if grp.ein.nunique() < 2 or len(grp) > 60:
            continue
        keys = list(grp.index)
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                a, b = op.loc[keys[i]], op.loc[keys[j]]
                if a.ein == b.ein:
                    continue
                sig = []
                if a.in_msa and b.in_msa:
                    sig.append("same_metro")
                if not (np.isnan(a.ymin) or np.isnan(b.ymin)) and a.ymin <= b.ymax + 1 and b.ymin <= a.ymax + 1:
                    sig.append("overlap_years")
                if a.mi and a.mi == b.mi:
                    sig.append("middle_initial")
                if a.suffix and a.suffix == b.suffix:
                    sig.append("suffix")
                strong = any(s in sig for s in ("middle_initial", "suffix"))
                is_common = bool(common.get(keys[i]) or common.get(keys[j]))
                if strong and len(sig) >= 2:
                    conf = "high"
                elif (not is_common and len(sig) >= 1) or (len(sig) >= 2 and not is_common):
                    conf = "medium"
                elif is_common and strong and len(sig) >= 2:
                    conf = "medium"
                else:
                    conf = "low"
                rec = {"org_person_a": keys[i], "org_person_b": keys[j], "name_norm": name, "ein_a": a.ein,
                       "ein_b": b.ein, "signals": ";".join(sig), "common_name": int(is_common),
                       "match_confidence": conf}
                if conf == "low":
                    cands.append(rec)
                else:
                    links.append(rec)
                    parent[find(keys[i])] = find(keys[j])
    op["root"] = [find(k) for k in op.index]
    op["person_id"] = op.root.map(lambda k: pid(k))
    link_df = pd.DataFrame(links)
    conf_by_root, sig_by_root = {}, {}
    for rec in links:
        root = find(rec["org_person_a"])
        prev = conf_by_root.get(root, "high")
        conf_by_root[root] = "medium" if "medium" in (prev, rec["match_confidence"]) else "high"
        sig_by_root.setdefault(root, set()).update(x for x in rec["signals"].split(";") if x)
    r["person_id"] = r.org_person.map(op.person_id)

    disp = r.groupby("person_id").name_display.agg(lambda s: s.value_counts().index[0])
    persons = op.groupby("person_id").agg(name_norm=("name_norm", "first"), first_name=("first", "first"),
                                          middle_initial=("mi", "first"), last_name=("last", "first"),
                                          suffix=("suffix", "first"), n_orgs=("ein", "nunique"), root=("root", "first"))
    persons["n_filings"] = r.groupby("person_id").size()
    persons["name_display"] = disp
    persons["match_notes"] = persons.apply(
        lambda p: "single organization" if p.n_orgs == 1 else
        f"linked across {p.n_orgs} orgs; exact normalized name + signals "
        f"{'+'.join(sorted(sig_by_root.get(p.root, [])))}; match_confidence={conf_by_root.get(p.root, 'medium')}", axis=1)
    person_conf = {pid_: conf_by_root.get(root, "") for pid_, root in persons.root.items()}
    person_sig = {pid_: "+".join(sorted(sig_by_root.get(root, []))) for pid_, root in persons.root.items()}
    dim_person = persons.reset_index().reindex(columns=columns("dim_person"))

    r["role_id"] = ["R" + hashlib.sha1(f"{a}|{b}|{c}|{d}".encode()).hexdigest()[:12]
                    for a, b, c, d in zip(r.person_id, r.ein, r.yr, r.role_type)]
    xcols = [c for c in r.columns if c.startswith("x_") and c != "x_stage_file"]
    notes = fold_notes(r, xcols) if xcols else ""
    roles = r.reindex(columns=columns("fact_roles")).assign(notes=notes)
    cand = pd.DataFrame(cands)
    if len(cand):
        cand["person_id_a"] = cand.org_person_a.map(op.person_id)
        cand["person_id_b"] = cand.org_person_b.map(op.person_id)
        cand = cand.drop(columns=["org_person_a", "org_person_b"])
    return roles, dim_person, (cand, link_df, op, person_conf, person_sig)


def relationships(roles, op_bundle):
    rel = []
    uni = read(CLEAN / "dim_universe_membership.csv")
    daf = set(uni[uni.universe == "daf_sponsors"].ein)
    names = read(CLEAN / "dim_org.csv").set_index("ein").org_name.to_dict() if (CLEAN / "dim_org.csv").exists() else {}
    g = read(CLEAN / "fact_grants.csv")
    if len(g):
        g = g[(g.funder_ein != "") & (g.recipient_ein != "") & (pd.to_numeric(g.cumulative_flag, errors="coerce").fillna(0) == 0)]
        g["amt"] = pd.to_numeric(g.amount, errors="coerce")
        a = g.groupby(["funder_ein", "recipient_ein", "tax_year"], as_index=False).agg(
            amount=("amt", "sum"), n=("grant_id", "size"), src=("source_id", lambda s: ";".join(sorted(set(s))[:3])))
        rel.append(pd.DataFrame({
            "org_a_ein": a.funder_ein, "org_b_ein": a.recipient_ein,
            "rel_type": np.where(a.funder_ein.isin(daf), "daf_sponsor_grant", "grant"), "direction": "a_to_b",
            "tax_year": a.tax_year, "amount": a.amount.round(), "evidence": a.n.map(lambda n: f"{n} grant row(s)"),
            "person_id": "", "source_id": a.src, "confidence": "high", "basis": "derived"}))
    ga = read(CLEAN / "fact_gov_awards.csv")
    if len(ga) and "pass_through_ein" in ga:
        ga = ga[(ga.pass_through_ein != "") & (ga.recipient_ein != "")]
        if len(ga):
            ga["amt"] = pd.to_numeric(ga.amount, errors="coerce")
            b = ga.groupby(["pass_through_ein", "recipient_ein", "fiscal_year"], as_index=False).agg(
                amount=("amt", "sum"), prog=("program_name", lambda s: "; ".join(sorted(set(s))[:3])),
                src=("source_id", lambda s: ";".join(sorted(set(s))[:3])))
            rel.append(pd.DataFrame({
                "org_a_ein": b.pass_through_ein, "org_b_ein": b.recipient_ein, "rel_type": "pass_through_funding",
                "direction": "a_to_b", "tax_year": b.fiscal_year, "amount": b.amount.round(), "evidence": b.prog,
                "person_id": "", "source_id": b.src, "confidence": "high", "basis": "derived"}))
    for p in sorted(INTERIM.glob("stage_fact_org_relationships__*.csv")):
        s = read(p)
        if len(s):
            s = s.reindex(columns=columns("fact_org_relationships") + [c for c in s.columns if c.startswith("x_")])
            rel.append(s)
    if len(roles):
        cand, links, op, person_conf, person_sig = op_bundle
        multi = roles.groupby("person_id").ein.nunique()
        multi = multi[multi > 1].index
        rr = roles[roles.person_id.isin(multi)].copy()
        rr["yr"] = pd.to_numeric(rr.tax_year, errors="coerce").fillna(pd.to_numeric(rr.fiscal_year, errors="coerce") - 1)
        rows = []
        for person, grp in rr.groupby("person_id"):
            by_org = grp.groupby("ein").yr.agg(["min", "max"])
            orgs = list(by_org.index)
            for i in range(len(orgs)):
                for j in range(i + 1, len(orgs)):
                    a, b = by_org.loc[orgs[i]], by_org.loc[orgs[j]]
                    lo, hi = max(a["min"], b["min"]), min(a["max"], b["max"])
                    rows.append({"org_a_ein": orgs[i], "org_b_ein": orgs[j], "rel_type": "shared_board_member",
                                 "x_person_match_signals": person_sig.get(person, ""),
                                 "direction": "undirected", "tax_year": int(hi) if hi == hi else "",
                                 "amount": "", "person_id": person,
                                 "evidence": f"same person in filings; years {int(a['min']) if a['min'] == a['min'] else ''}-"
                                             f"{int(a['max']) if a['max'] == a['max'] else ''} vs "
                                             f"{int(b['min']) if b['min'] == b['min'] else ''}-{int(b['max']) if b['max'] == b['max'] else ''}"
                                             f"{'' if lo <= hi + 1 else ' (no overlap)'}",
                                 "source_id": "bulk_irs_xml", "confidence": person_conf.get(person) or "medium",
                                 "basis": "inferred"})
        if rows:
            rel.append(pd.DataFrame(rows))
    if not rel:
        return pd.DataFrame(columns=columns("fact_org_relationships"))
    out = pd.concat(rel, ignore_index=True).fillna("")
    out["org_a_name"] = out.org_a_ein.map(names).fillna(out.get("org_a_name", ""))
    out["org_b_name"] = out.org_b_ein.map(names).fillna(out.get("org_b_name", ""))
    key = out[["org_a_ein", "org_b_ein", "rel_type", "tax_year", "person_id", "evidence"]].astype(str).agg("|".join, axis=1)
    out["rel_id"] = ["L" + hashlib.sha1(f"{k}|{o}".encode()).hexdigest()[:12] for k, o in zip(key, key.groupby(key).cumcount())]
    xcols = [c for c in out.columns if c.startswith("x_")]
    notes = fold_notes(out, xcols) if xcols else ""
    return out.reindex(columns=columns("fact_org_relationships")).assign(notes=notes)


def main():
    roles, dim_person, bundle = people()
    rel = relationships(roles, bundle)
    roles.to_csv(CLEAN / "fact_roles.csv", index=False)
    dim_person.to_csv(CLEAN / "dim_person.csv", index=False)
    cand = bundle[0] if isinstance(bundle, tuple) else pd.DataFrame()
    if cand.empty:
        cand = pd.DataFrame(columns=["name_norm", "ein_a", "ein_b", "signals", "common_name", "match_confidence",
                                     "person_id_a", "person_id_b"])
    cand.to_csv(CLEAN / "candidate_interlocks.csv", index=False)
    rel.to_csv(CLEAN / "fact_org_relationships.csv", index=False)
    multi = (dim_person.n_orgs.astype(float) > 1).sum() if len(dim_person) else 0
    msg = (f"- fact_roles {len(roles):,}; dim_person {len(dim_person):,} (multi-org {multi:,}); "
           f"candidate_interlocks {len(cand):,}; fact_org_relationships {len(rel):,} "
           f"{rel.rel_type.value_counts().to_dict() if len(rel) else {}}")
    log("64_people_relationships", msg)
    print(msg)


if __name__ == "__main__":
    main()
