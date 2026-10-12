"""Apply a headline spine to a deck build script: replace each old headline string (from a saved v1 spine)
with the corresponding v2 headline, matched by position. Usage:
python scripts/lib/apply_spine.py <old_spine.md> <new_spine.md> <build_script.js>
Prints how many headlines were replaced and lists any old headline not found in the script."""
import re
import sys
from pathlib import Path


def heads(md: Path) -> list[str]:
    out = []
    for ln in md.read_text().splitlines():
        m = re.match(r"^\d+\. (.*)$", ln)
        if m:
            out.append(re.sub(r"\s*\*\((title|executive summary|closing)\)\*", "", m.group(1)).strip())
    return out


def main(old: str, new: str, js: str) -> int:
    o, n = heads(Path(old)), heads(Path(new))
    assert len(o) == len(n), f"spine lengths differ: {len(o)} vs {len(n)}"
    s = Path(js).read_text()
    done, missing = 0, []
    for a, b in zip(o, n):
        if a == b:
            continue
        if a in s:
            s = s.replace(a, b); done += 1
        else:
            missing.append(a)
    Path(js).write_text(s)
    print(f"replaced {done} headlines in {Path(js).name}")
    for m in missing:
        print("NOT FOUND:", m[:100])
    return 0 if not missing else 1


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:4]))
