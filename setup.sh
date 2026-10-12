#!/bin/sh
# One-time setup after cloning: Python environment, rejoined data tables, deck tooling, and a self-check.
# Safe to rerun. Needs Python 3.12 (uv recommended), Node 18+, LibreOffice and poppler for the decks.
#
#   ./setup.sh            everything
#   SKIP_DECKS=1 ./setup.sh   Python and data only (no Node, LibreOffice or poppler needed)
set -eu
ROOT=$(cd "$(dirname "$0")" && pwd)
VENV="$ROOT/calvary_funding_data/.venv"
PY="$VENV/bin/python"

echo "1/4 Python environment ($VENV)"
if [ ! -x "$PY" ]; then
  if command -v uv >/dev/null 2>&1; then
    uv venv --python 3.12 "$VENV"
  elif command -v python3.12 >/dev/null 2>&1; then
    python3.12 -m venv "$VENV"
  else
    echo "   need Python 3.12: install uv (https://docs.astral.sh/uv/) or python3.12, then rerun"; exit 1
  fi
fi
if command -v uv >/dev/null 2>&1; then
  uv pip install --quiet --python "$PY" -r "$ROOT/calvary_funding_data/requirements.txt" -r "$ROOT/calvary_analysis/requirements.txt"
else
  "$PY" -m pip install --quiet -r "$ROOT/calvary_funding_data/requirements.txt" -r "$ROOT/calvary_analysis/requirements.txt"
fi

echo "2/4 Rejoin the two large tables (stored in parts; see calvary_funding_data/clean/_parts/REJOIN.md)"
CLEAN="$ROOT/calvary_funding_data/clean"
for t in fact_grants fact_org_relationships; do
  if [ ! -s "$CLEAN/$t.csv" ]; then
    cat "$CLEAN/_parts/$t.csv.part"* > "$CLEAN/$t.csv"
    echo "   rebuilt $t.csv"
  else
    echo "   $t.csv already present"
  fi
done

echo "3/4 Deck tooling"
if [ -n "${SKIP_DECKS:-}" ]; then
  echo "   skipped (SKIP_DECKS set)"
else
  if command -v npm >/dev/null 2>&1; then
    if [ -d "$ROOT/calvary_analysis/decks/node_modules" ]; then echo "   node_modules present"; else (cd "$ROOT/calvary_analysis/decks" && npm ci --silent); fi
  else
    echo "   Node not found: install Node 18+ to rebuild decks"
  fi
  for tool in soffice pdftoppm pdfinfo; do
    command -v "$tool" >/dev/null 2>&1 || echo "   missing $tool: on macOS, 'brew install --cask libreoffice' (soffice) and 'brew install poppler' (pdftoppm, pdfinfo)"
  done
fi

echo "4/4 Self-check"
(cd "$ROOT/calvary_analysis" && "$PY" scripts/00_env_check.py && "$PY" scripts/lib/trace.py | tail -1)
echo "Done. Read CLAUDE.md, then calvary_analysis/README.md. Deliverables are in calvary_analysis/decks/pdf/."
