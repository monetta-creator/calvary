"""Geocode organization address overrides (config/org_address_overrides.csv) with the Census Geocoder.

Some BMF streets are mailing or residential addresses (e.g. a small organization's officer's home); for those,
config/org_address_overrides.csv gives the organization's office address from its filing or website.
Output interim/org_geo_overrides.csv (ein, street_used, county_fips, tract_geoid, lat, lon, geo_method),
applied by scripts/63_build_dims.py on top of interim/stage_org_geo__context.csv.

Usage: python scripts/47_geocode_address_overrides.py
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import CONFIG, INTERIM, log, save_raw, session, today

URL = "https://geocoding.geo.census.gov/geocoder/geographies/address"


def main():
    ov = pd.read_csv(CONFIG / "org_address_overrides.csv", dtype=str)
    s, rows = session(), []
    for r in ov.itertuples():
        params = {"street": r.street, "city": r.city, "state": r.state, "zip": r.zip5,
                  "benchmark": "Public_AR_Current", "vintage": "Current_Current", "format": "json"}
        resp = s.get(URL, params=params, timeout=60)
        save_raw("census_geocoder", f"override_{r.ein}", resp.content, "json")
        m = (resp.json().get("result", {}).get("addressMatches") or [None])[0]
        out = {"ein": r.ein, "street_used": r.street, "address_source": "config_override", "geo_method": "census_geocoder",
               "source_id": "api_census_geocoder", "retrieved_date": today()}
        if m:
            tr = m["geographies"]["Census Tracts"][0]
            out.update(county_fips=tr["STATE"] + tr["COUNTY"], tract_geoid=tr["GEOID"],
                       lat=m["coordinates"]["y"], lon=m["coordinates"]["x"], match_quality="match")
        else:
            out.update(match_quality="no_match", geo_method="unresolved")
        rows.append(out)
    pd.DataFrame(rows).to_csv(INTERIM / "org_geo_overrides.csv", index=False)
    log("47_geocode_address_overrides", "\n".join(f"- {r['ein']}: {r['match_quality']} {r.get('tract_geoid', '')}" for r in rows))
    print(rows)


if __name__ == "__main__":
    main()
