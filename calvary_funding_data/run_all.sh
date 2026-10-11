#!/usr/bin/env bash
# Rebuild the dataset.
#   ./run_all.sh            rebuild clean/ from raw/ + saved API responses (no network)
#                           Pull-only scripts (34 FAC, 43/44 web, 47 address geocode) are not rerun; their
#                           staging files in interim/ are reused.
#   ./run_all.sh pull       full run: probes, downloads and API pulls, then rebuild
# Keys (pull mode) are read from the environment; optionally from ~/.config/calvary/keys.env:
#   TAVILY_API_KEY FAC_API_KEY CENSUS_API_KEY DC_MAR_API_KEY
set -euo pipefail
cd "$(dirname "$0")"
PY=.venv/bin/python
[ -x "$PY" ] || { echo "create the venv first: uv venv --python 3.12 .venv && uv pip install --python .venv/bin/python -r requirements.txt"; exit 1; }
[ -f "$HOME/.config/calvary/keys.env" ] && { set -a; . "$HOME/.config/calvary/keys.env"; set +a; }
MODE="${1:-rebuild}"
# rebuild mode must not re-append observations to notes_for_analysis.md / open_questions.md
[ "$MODE" = "pull" ] || export CALVARY_NO_NOTES=1
run() { echo "==> $*"; "$PY" -W ignore "$@"; }

if [ "$MODE" = "pull" ]; then
  run scripts/00_setup.py
  run scripts/10_probe_filings.py
  run scripts/11_eval_xml_tooling.py
  run scripts/12_probe_federal.py
  run scripts/14_probe_dc_hud.py
  run scripts/16_probe_context.py
  run scripts/19_merge_catalog.py
fi

# inputs (user PDFs / CRM export in inputs/)
run scripts/01_inventory_inputs.py
run scripts/02_extract_inputs.py

# universes (20 -> 21 -> 22 -> 20: known-funder matches feed universe KF1/KF2)
run scripts/20_build_universes.py
[ "$MODE" = "pull" ] && run scripts/21_core_peer_candidates.py
run scripts/22_match_known_funders.py
run scripts/20_build_universes.py

if [ "$MODE" = "pull" ]; then
  run scripts/30_fetch_xml.py
  run scripts/34_pull_fac.py          # first: builds interim/uei_ein_map.csv used by 33
  run scripts/33_pull_usaspending.py
  run scripts/35_pull_grantsgov.py
  run scripts/40_geocode_orgs.py --no-notes
  run scripts/41_pull_soi_extracts.py
  run scripts/42_pull_propublica.py
  run scripts/43_web_calvary.py
  run scripts/44_web_peers_funders.py
  run scripts/46_web_named_comparators.py
  run scripts/47_geocode_address_overrides.py
fi

# parse raw -> staging
run scripts/36_parse_dc_awards.py
run scripts/37_parse_dc_budget.py
run scripts/38_parse_hud_counts.py
run scripts/39_build_geo_period.py --no-notes
# stage-only passes over saved raw responses (no network)
[ "$MODE" = "pull" ] || run scripts/33_pull_usaspending.py --only stage
[ "$MODE" = "pull" ] || run scripts/35_pull_grantsgov.py
[ "$MODE" = "pull" ] || run scripts/40_geocode_orgs.py --no-notes
[ "$MODE" = "pull" ] || run scripts/41_pull_soi_extracts.py --only stage
[ "$MODE" = "pull" ] || run scripts/42_pull_propublica.py --only stage
[ "$MODE" = "pull" ] || run scripts/46_web_named_comparators.py --only stage
run scripts/45_stage_web_grants.py
run scripts/50_parse_xml.py
run scripts/51_qc_xml.py

# model
run scripts/60_stage_inputs.py
run scripts/61_resolve_entities.py
run scripts/62_build_facts.py
run scripts/63_build_dims.py
run scripts/64_people_relationships.py
run scripts/63_build_dims.py          # second pass: dim_funder/dim_org pick up relationship-derived EINs
run scripts/70_quality_checks.py
run scripts/80_docs.py
echo "done: clean/ rebuilt ($MODE)"
