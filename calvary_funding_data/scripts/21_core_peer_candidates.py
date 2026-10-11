"""Phase 3: assemble core-peer candidates, fetch each candidate's latest 990 XML (GivingTuesday S3),
pull mission/program text and key financials, geocode DC addresses (MAR 2), and score candidates.

Outputs:
  interim/core_peer_candidates.csv     every candidate with evidence columns and score
  reports/core_peers_proposal.md       Checkpoint 2 proposal (recommended list + alternates)
Raw: raw/xml/gt/{stamp}_{ein}_TY{yr}_{object_id}_public.xml, raw/mar2/{stamp}_{ein}.json

Usage: python scripts/21_core_peer_candidates.py
Keys: DC_MAR_API_KEY (optional; without it DC ward is left blank).
"""
import math
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import quote

import pandas as pd
from lxml import etree

sys.path.insert(0, str(Path(__file__).parent))
from lib.xmlstore import XmlStore  # noqa: E402

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import (CLEAN, INTERIM, RAW, REPORTS, RateLimiter, env_key, log, norm_name, save_raw, session,
                        today)

GT_S3 = "https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{oid}_public.xml"
MAR = "https://datagate.dc.gov/mar/open/api/v2.2/locations/{addr}"
CALVARY = "521307706"

# Named seeds: organizations known to serve homeless women, DV survivors, recovery or Wards 7/8 in the DC area.
# Pattern is matched against lib.common.norm_name(BMF NAME) within the given state; norm_name drops
# stop words (of, the, and, a) and legal suffixes, so patterns are written in that normalized form.
SEEDS = [
    ("N Street Village", r"^n street village", "DC"),
    ("House of Ruth (DC)", r"^house ruth$", "DC"),
    ("District Alliance for Safe Housing (DASH)", r"district alliance for safe housing", "DC"),
    ("My Sister's Place", r"^my sisters place", "DC"),
    ("DC SAFE", r"^dc safe|^survivors advocates for empowerment", "DC"),
    ("Thrive DC", r"^thrive dc", "DC"),
    ("Friendship Place", r"^friendship place", "DC"),
    ("Miriam's Kitchen", r"^miriams kitchen", "DC"),
    ("So Others Might Eat (SOME)", r"^some$|^so others might eat", "DC"),
    ("Pathways to Housing DC", r"^pathways to housing dc|^pathways to housing d c", "DC"),
    ("Community of Hope", r"^community hope$", "DC"),
    ("Open Arms Housing", r"^open arms housing", "DC"),
    ("Samaritan Inns", r"^samaritan inns", "DC"),
    ("Christ House", r"^christ house", "DC"),
    ("Jubilee Housing", r"^jubilee housing", "DC"),
    ("Everyone Home DC", r"^everyone home dc|^community family life services", "DC"),
    ("Coalition for the Homeless / Housing Up", r"^housing up|^coalition for homeless", "DC"),
    ("Bright Beginnings", r"^bright beginnings", "DC"),
    ("Covenant House DC", r"^covenant house (washington|dc)", "DC"),
    ("Sasha Bruce Youthwork", r"^sasha bruce", "DC"),
    ("New Hope Ministries (DC)", r"^new hope ministries", "DC"),
    ("Community Connections", r"^community connections", "DC"),
    ("Mary's Center", r"^marys center", "DC"),
    ("Bread for the City", r"^bread for city", "DC"),
    ("Life Deeds", r"^life deeds", "MD"),
    ("Wanda Alston Foundation", r"^wanda alston", "DC"),
    ("Doorways for Women and Families", r"^doorways for women", "VA"),
    ("Bethany House of Northern Virginia", r"^bethany house", "VA"),
    ("Carpenter's Shelter", r"^carpenters shelter", "VA"),
    ("Shelter House (Fairfax)", r"^shelter house", "VA"),
    ("New Hope Housing (VA)", r"^new hope housing", "VA"),
    ("House of Ruth Maryland", r"^house ruth maryland", "MD"),
    ("Mission of Love / Shepherd's Table", r"^shepherds table", "MD"),
    ("Interfaith Works", r"^interfaith works", "MD"),
    ("Community Crisis Services / Family Crisis Center PG", r"^family crisis center", "MD"),
    ("Women Who Care Ministries", r"^women who care ministries", "MD"),
]
WARD78_ZIPS = {"20019", "20020", "20032"}
SHELTER_DV = {"L40", "L41", "P85", "P43", "I71", "P62", "I70", "I73", "F42"}
WOMEN_RE = re.compile(r"(?i)\b(?:women|womens|woman|sister|sisters|ladies|girls|ywca|house of ruth|survivors)\b")


def strip_ns(root):
    for el in root.iter():
        if isinstance(el.tag, str) and "}" in el.tag:
            el.tag = el.tag.split("}", 1)[1]
    return root


def first(root, *paths):
    for p in paths:
        v = root.xpath(f"string(({p})[1])")
        if v:
            return v.strip()
    return ""


def xml_facts(path: Path) -> dict:
    root = strip_ns(etree.parse(str(path), etree.XMLParser(huge_tree=True, recover=True)).getroot())
    progs = root.xpath("//IRS990/ProgSrvcAccomActy2Grp/DescriptionProgramSrvcAccomTxt | "
                       "//IRS990/ProgSrvcAccomActy3Grp/DescriptionProgramSrvcAccomTxt | "
                       "//IRS990/ProgSrvcAccomActyOtherGrp/DescriptionProgramSrvcAccomTxt")
    num = lambda p: pd.to_numeric(first(root, p) or None, errors="coerce")
    return {
        "mission": first(root, "//IRS990/ActivityOrMissionDesc", "//IRS990/MissionDesc", "//IRS990EZ/PrimaryExemptPurposeTxt"),
        "program_desc_1": first(root, "//IRS990/Desc", "//IRS990/ProgSrvcAccomActy2Grp/DescriptionProgramSrvcAccomTxt"),
        "programs_other": " | ".join((p.text or "").strip() for p in progs)[:1500],
        "website": first(root, "//IRS990/WebsiteAddressTxt", "//IRS990EZ/WebsiteAddressTxt"),
        "xml_total_revenue": num("//IRS990/CYTotalRevenueAmt | //IRS990EZ/TotalRevenueAmt"),
        "xml_gov_grants": num("//IRS990/GovernmentGrantsAmt"),
        "xml_contributions": num("//IRS990/CYContributionsGrantsAmt | //IRS990EZ/ContributionsGiftsGrantsEtcAmt"),
        "xml_street": first(root, "//Filer/USAddress/AddressLine1Txt"),
        "xml_zip": first(root, "//Filer/USAddress/ZIPCd")[:5],
    }


def main():
    m = pd.read_csv(CLEAN / "dim_universe_membership.csv", dtype=str)
    # seeds are matched against the full DC/MD/VA BMF: several obvious peers carry NTEE codes outside the
    # sector sets (e.g. health or food codes), so they would be missed if we searched universe EINs only
    from lib.common import latest_raw, norm_ein
    base = pd.concat([pd.read_csv(latest_raw("irs_bmf", f"eo_{st}.csv"), dtype=str, keep_default_na=False)
                      for st in ("dc", "md", "va")], ignore_index=True)
    base["ein"] = base.EIN.map(norm_ein)
    base["ntee3"] = base.NTEE_CD.str[:3]
    base["zip5"] = base.ZIP.str[:5]
    base["name_norm"] = base.NAME.map(norm_name)
    ix_all = []
    for yr in range(2021, 2027):
        d = pd.read_csv(latest_raw("irs_xml_index", f"index_{yr}.csv"), dtype=str, keep_default_na=False,
                        usecols=lambda c: c in {"EIN", "TAX_PERIOD", "SUB_DATE", "RETURN_TYPE", "OBJECT_ID", "XML_BATCH_ID"})
        d["release_year"] = yr
        ix_all.append(d[d.RETURN_TYPE.isin(["990", "990EZ"])])
    ix = pd.concat(ix_all, ignore_index=True)
    ix["ein"] = ix.EIN.map(norm_ein)
    ix["tp"] = ix.TAX_PERIOD
    sector = m[m.universe.isin(["dc_sector", "dmv_sector"])].drop_duplicates("ein")

    rows = {}
    for label, pat, st in SEEDS:
        hit = base[(base.STATE == st) & base.name_norm.str.contains(pat, regex=True, na=False)]  # noqa
        hit = hit.assign(rev=pd.to_numeric(hit.REVENUE_AMT, errors="coerce")).sort_values("rev", ascending=False)
        if hit.empty:
            rows[f"seed:{label}"] = {"seed_label": label, "ein": None, "seed_status": "not_found_in_universe_bmf"}
            continue
        e = hit.iloc[0].ein
        rows[e] = {"ein": e, "seed_label": label, "seed_status": "matched"}
    sec = sector.assign(rev=pd.to_numeric(sector.bmf_revenue_amt, errors="coerce"))
    data_driven = sec[(sec.rev >= 750_000) & (sec.recent_filing == "True") &
                      (sec.ntee3.isin(SHELTER_DV) | sec.org_name_bmf.str.contains(WOMEN_RE, na=False))]
    for e in data_driven.ein:
        rows.setdefault(e, {"ein": e, "seed_label": "", "seed_status": "data_driven"})
    rows.setdefault(CALVARY, {"ein": CALVARY, "seed_label": "Calvary (reference)", "seed_status": "subject"})

    cand = pd.DataFrame(rows.values())
    found = cand[cand.ein.notna()].merge(
        base[["ein", "NAME", "STREET", "CITY", "STATE", "zip5", "NTEE_CD", "ntee3", "REVENUE_AMT", "TAX_PERIOD"]],
        on="ein", how="left")

    # latest e-filed 990/990EZ per candidate
    ixc = ix[ix.ein.isin(found.ein) & ix.RETURN_TYPE.isin(["990", "990EZ"])].copy()
    ixc["tp"] = pd.to_numeric(ixc.tp, errors="coerce")
    latest = ixc.sort_values(["tp", "SUB_DATE"]).groupby("ein").tail(1)[
        ["ein", "OBJECT_ID", "tp", "RETURN_TYPE", "release_year", "XML_BATCH_ID"]]
    found = found.merge(latest, on="ein", how="left")

    s = session()
    rl = RateLimiter(8)
    store = XmlStore()

    def fetch(r):
        if pd.isna(r.OBJECT_ID):
            return r.ein, {}
        ty = int(str(int(r.tp))[:4]) - (0 if str(int(r.tp))[4:] == "12" else 1)
        p, how = store.get(r.OBJECT_ID, r.ein, ty, int(r.release_year), r.XML_BATCH_ID or None)
        if p is None:
            return r.ein, {"xml_status": how}
        try:
            return r.ein, {**xml_facts(p), "xml_status": "ok", "xml_tax_year": ty}
        except Exception as ex:  # noqa: BLE001
            return r.ein, {"xml_status": f"parse_error:{type(ex).__name__}"}

    with ThreadPoolExecutor(6) as pool:
        facts = dict(pool.map(fetch, found.itertuples()))
    found = found.join(pd.DataFrame.from_dict(facts, orient="index"), on="ein")

    # DC ward via MAR 2, using the 990 street address when present (BMF often holds a mailing address)
    key = env_key("DC_MAR_API_KEY")

    def ward(r):
        if r.STATE != "DC" or not key:
            return r.ein, {}
        street = r.xml_street if isinstance(r.xml_street, str) and r.xml_street else r.STREET
        if not isinstance(street, str) or not street or street.upper().startswith(("PO BOX", "P O BOX")):
            return r.ein, {"ward_status": "no_street"}
        rl.wait()
        resp = s.get(MAR.format(addr=quote(street)), params={"apikey": key}, timeout=30)
        save_raw("mar2", f"{r.ein}", resp.content, "json")
        try:
            res = resp.json().get("Result", {}).get("addresses") or []
            props = res[0].get("address", {}).get("properties", {}) if res else {}
            return r.ein, {"ward": props.get("Ward", ""), "mar_tract": props.get("CensusTract", ""),
                           "ward_status": "ok" if props else "no_match"}
        except Exception:  # noqa: BLE001
            return r.ein, {"ward_status": "parse_error"}

    with ThreadPoolExecutor(4) as pool:
        wards = dict(pool.map(ward, found.itertuples()))
    found = found.join(pd.DataFrame.from_dict(wards, orient="index"), on="ein")

    # scoring: transparent additive rubric, documented in the proposal
    text = (found.NAME.fillna("") + " " + found.get("mission", "").fillna("") + " " +
            found.get("program_desc_1", "").fillna("") + " " + found.get("programs_other", "").fillna(""))
    rev = pd.to_numeric(found.xml_total_revenue, errors="coerce").fillna(pd.to_numeric(found.REVENUE_AMT, errors="coerce"))
    cal_rev = 4_967_995
    found["s_women"] = text.str.contains(r"(?i)\bwomen\b|\bwoman\b|\bfemale\b|\bmothers\b", regex=True).astype(int) * 3
    found["s_dv"] = text.str.contains(r"(?i)domestic violence|intimate partner|survivor|abuse|trafficking", regex=True).astype(int) * 2
    found["s_homeless"] = text.str.contains(r"(?i)homeless|shelter|supportive housing|transitional housing|housing first", regex=True).astype(int) * 2
    found["s_recovery"] = text.str.contains(r"(?i)recovery|substance|addiction|sobriety|mental health", regex=True).astype(int)
    found["s_ward78"] = (found.ward.isin(["Ward 7", "Ward 8"]) | found.zip5.isin(WARD78_ZIPS)).astype(int) * 2
    found["s_dc"] = (found.STATE == "DC").astype(int)
    found["s_size"] = rev.map(lambda x: max(0, 2 - abs(math.log(x / cal_rev, 3))) if x and x > 0 else 0).round(2)
    found["score"] = found[[c for c in found.columns if c.startswith("s_")]].sum(axis=1)
    # relevance gate: homeless/housing or DV language must appear in name, mission or program text
    found["relevant"] = (found.s_homeless > 0) | (found.s_dv > 0)
    found["revenue_latest"] = rev
    found = found.sort_values("score", ascending=False)
    found.to_csv(INTERIM / "core_peer_candidates.csv", index=False)
    missing = cand[cand.ein.isna()]
    log("21_core_peer_candidates", f"- candidates {len(found)} (seeds matched {int((found.seed_status=='matched').sum())}, "
        f"data-driven {int((found.seed_status=='data_driven').sum())}); seeds not found: "
        f"{', '.join(missing.seed_label) or 'none'}; XML ok {int((found.xml_status=='ok').sum())}; "
        f"wards {int((found.ward_status=='ok').sum())}")
    show = found[found.relevant | (found.seed_status == "matched")]
    print(show[["ein", "NAME", "STATE", "ward", "revenue_latest", "score", "s_women", "s_dv", "s_homeless", "s_recovery", "seed_status"]].head(60).to_string(index=False))
    print("seeds not found:", missing.seed_label.tolist())


if __name__ == "__main__":
    main()
