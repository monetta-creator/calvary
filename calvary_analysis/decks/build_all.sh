#!/bin/sh
# Rebuild the Calvary decks: PPTX (editable source) -> pdf/ (the deliverable) -> qa/<deck>/ (PDF copy + slide JPGs),
# then run the headline check on each deck. Self-contained: needs node (npm install in this folder), LibreOffice
# (soffice), poppler (pdftoppm, pdfinfo) and the data build's Python venv for the headline check.
#
#   ./build_all.sh                      all seven decks
#   ./build_all.sh leadership appendix_C  only these
#   NO_CHECK=1 ./build_all.sh           skip the headline check
set -eu
DECKS_DIR=$(cd "$(dirname "$0")" && pwd)
ANALYSIS=$(dirname "$DECKS_DIR")
PY="$(dirname "$ANALYSIS")/calvary_funding_data/.venv/bin/python"
export NODE_PATH="$DECKS_DIR/node_modules"

for tool in node soffice pdftoppm pdfinfo; do
  command -v "$tool" >/dev/null 2>&1 || { echo "missing: $tool (see calvary_analysis/README.md, Decks)"; exit 1; }
done
[ -d "$NODE_PATH" ] || { echo "run 'npm install' in $DECKS_DIR first"; exit 1; }

# deck key -> build script, output file stem, headline spine (and appendix letter for the appendix spine)
info() {
  case "$1" in
    leadership) echo "build_leadership.js leadership_deck leadership_headline_spine.md -" ;;
    consulting) echo "build_consulting.js consulting_deck consulting_headline_spine.md -" ;;
    onepager)   echo "build_onepager.js executive_one_pager - -" ;;
    appendix_A) echo "build_appendix_A.js appendix_A_calvary_government appendix_headline_spine.md A" ;;
    appendix_B) echo "build_appendix_B.js appendix_B_peers_comparators appendix_headline_spine.md B" ;;
    appendix_C) echo "build_appendix_C.js appendix_C_funders_pipeline appendix_headline_spine.md C" ;;
    appendix_D) echo "build_appendix_D.js appendix_D_data_methods appendix_headline_spine.md D" ;;
    *) echo "unknown deck: $1 (leadership consulting onepager appendix_A..appendix_D)" >&2; exit 1 ;;
  esac
}

[ $# -gt 0 ] || set -- leadership consulting onepager appendix_A appendix_B appendix_C appendix_D
cd "$DECKS_DIR"
mkdir -p pdf
failed=0
for key in "$@"; do
  set -- $(info "$key")
  script=$1; stem=$2; spine=$3; letter=$4
  node "$script" >/dev/null
  soffice --headless --convert-to pdf --outdir pdf "$stem.pptx" >/dev/null 2>&1
  mkdir -p "qa/$key" && rm -f "qa/$key"/slide-*.jpg
  cp "pdf/$stem.pdf" "qa/$key/"
  pdftoppm -jpeg -scale-to 801 "pdf/$stem.pdf" "qa/$key/slide"
  pages=$(pdfinfo "pdf/$stem.pdf" | awk '/^Pages/{print $2}')
  result="not checked"
  if [ -z "${NO_CHECK:-}" ] && [ "$spine" != "-" ]; then
    if [ "$letter" = "-" ]; then
      out=$("$PY" "$ANALYSIS/scripts/lib/headline_check.py" "$stem.pptx" "$ANALYSIS/storylines/$spine" 2>&1) || failed=1
    else
      out=$("$PY" "$ANALYSIS/scripts/lib/headline_check.py" "$stem.pptx" "$ANALYSIS/storylines/$spine" --appendix="$letter" 2>&1) || failed=1
    fi
    result=$(printf '%s\n' "$out" | tail -1)
  fi
  echo "$key: $pages pages; $result"
done
[ "$failed" -eq 0 ] || { echo "headline check failed: run scripts/lib/headline_check.py on the deck above for details"; exit 1; }
