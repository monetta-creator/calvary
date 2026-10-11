"""Phase 0: create folder tree, copy user PDFs into inputs/, seed documentation files.

Usage: python scripts/00_setup.py [--src ../pdf-data]
Idempotent: existing files in inputs/ are not overwritten; seeded docs are only created if absent.
"""
import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import (ROOT, INPUTS, RAW, CLEAN, SOURCES, REPORTS, LOGS, CONFIG,
                        BUILD_LOG, log, env_key)

SEED = {
    "notes_for_analysis.md": "# Notes for analysis\n\nPatterns, anomalies and questions observed during the data build. "
                             "Observations only; no verdicts.\n",
    "open_questions.md": "# Open questions\n\nItems needing the engagement lead's input.\n",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=str(ROOT.parent / "pdf-data"))
    a = ap.parse_args()

    for d in (INPUTS, RAW, CLEAN, SOURCES, REPORTS, LOGS, CONFIG):
        d.mkdir(parents=True, exist_ok=True)

    if not BUILD_LOG.exists():
        BUILD_LOG.write_text("# Build log\n\nAppend-only record of what ran, row counts, failures and decisions.\n",
                             encoding="utf-8")
    for name, text in SEED.items():
        p = ROOT / name
        if not p.exists():
            p.write_text(text, encoding="utf-8")

    src = Path(a.src)
    copied = skipped = 0
    if src.exists():
        for f in sorted(src.glob("*.pdf")):
            dst = INPUTS / f.name
            if dst.exists():
                skipped += 1
                continue
            shutil.copy2(f, dst)
            copied += 1

    keys = {k: bool(env_key(k)) for k in ("TAVILY_API_KEY", "FAC_API_KEY", "CENSUS_API_KEY")}
    log("00_setup", f"- inputs/: copied {copied}, already present {skipped}\n"
                    f"- API keys present: " + ", ".join(f"{k}={'yes' if v else 'no'}" for k, v in keys.items()))
    print(f"copied={copied} skipped={skipped} keys={keys}")


if __name__ == "__main__":
    main()
