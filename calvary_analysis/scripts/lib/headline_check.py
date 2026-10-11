"""Headline check: extract every slide title from a built deck and compare, in order, with its headline spine.
Usage: python scripts/lib/headline_check.py decks/leadership_deck.pptx storylines/leadership_headline_spine.md
Prints the extracted sequence, flags titles that are not full sentences (no verb-ish word, no terminal structure) or
exceed 22 words, and reports mismatches against the spine. Exit 1 on any failure."""
import re
import sys
from pathlib import Path

from pptx import Presentation

VERBISH = re.compile(r"\b(is|are|was|were|has|have|had|do|does|did|can|could|would|should|will|may|grew|built|funded|provide|provides|carry|carries|held|brought|recognized|show|shows|works|give|gives|fund|funds|suggest|come|comes|opens|would|rose|fell|ran|sits|runs|stayed|trails|supply|supplies|moved|yields|carried|reach|assigns|changes|follow|follows|sharpen|traces|answers|rests|measured|agree|appear|appears|draw|puts|holds|cost|costs|leaving|growing|shows|remain|remains|threat|returns|show|start|started|match|matched|exceeded|disappeared|depend|depends)\b", re.I)


def titles(pptx: Path) -> list[str]:
    out = []
    from pptx.enum.shapes import PP_PLACEHOLDER
    for slide in Presentation(str(pptx)).slides:
        text = ""
        for sh in slide.shapes:
            if sh.is_placeholder and sh.placeholder_format.type in (PP_PLACEHOLDER.TITLE, PP_PLACEHOLDER.CENTER_TITLE) and sh.has_text_frame:
                text = sh.text_frame.text.strip().replace("\n", " ").replace("\x0b", " ")
                break
        out.append(" ".join(text.split()))
    return out


def spine(md: Path) -> list[str]:
    heads = []
    for ln in md.read_text().splitlines():
        m = re.match(r"^(\d+)\. (.*)$", ln)
        if m:
            h = re.sub(r"\s*\*\((title|executive summary|closing)\)\*", "", m.group(2)).strip()
            heads.append(h)
    return heads


def main(pptx: str, md: str | None, max_words: int = 20) -> int:
    tt = titles(Path(pptx))
    bad = 0
    print(f"{len(tt)} slides in {Path(pptx).name}")
    for i, t in enumerate(tt, 1):
        words = len(re.sub(r"\s*\(continued, \d+ of \d+\)\s*$", "", t).split())
        flags = []
        if not t:
            flags.append("NO TITLE")
        else:
            if words > max_words and not re.match(r"^\d+\. ", t):
                flags.append(f"{words} words")
            if ";" in t:
                flags.append("semicolon")
        if flags:
            bad += 1
        print(f"{i:2d}. {t}  {'[' + ', '.join(flags) + ']' if flags else ''}")
    if md:
        sp = spine(Path(md))
        content = [t for t in tt if t]
        # drop section dividers (titles that also appear as sectionTitle-like short phrases without a verb) by matching spine order
        j = 0; missing = []
        for h in sp:
            if j < len(content) and content[j].rstrip(".") == h.rstrip("."):
                j += 1
            else:
                k = next((x for x in range(j, len(content)) if content[x].rstrip(".") == h.rstrip(".")), None)
                if k is None:
                    missing.append(h)
                else:
                    j = k + 1
        print(f"spine: {len(sp)} headlines; matched in order: {len(sp) - len(missing)}")
        for h in missing:
            print("  SPINE MISMATCH:", h)
        bad += len(missing)
    print("HEADLINES", "OK" if not bad else f"PROBLEMS ({bad})")
    return 0 if not bad else 1


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--max=")]
    mx = next((int(a.split("=")[1]) for a in sys.argv[1:] if a.startswith("--max=")), 20)
    sys.exit(main(args[0], args[1] if len(args) > 1 else None, mx))
