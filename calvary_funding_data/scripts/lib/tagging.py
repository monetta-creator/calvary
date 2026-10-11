"""Program-area tagging shared by all scripts. Vocabulary: config/program_areas.yaml."""
from __future__ import annotations

import re
from functools import lru_cache

import yaml

from .common import CONFIG


@lru_cache(maxsize=1)
def _vocab():
    v = yaml.safe_load((CONFIG / "program_areas.yaml").read_text())
    pats = {}
    for tag, d in v.items():
        kws = [k for k in d.get("keywords", []) if k]
        if kws:
            pats[tag] = re.compile(r"(?i)\b(?:" + "|".join(re.escape(k) for k in kws) + r")\b")
    ntee = {code: tag for tag, d in v.items() for code in d.get("ntee3", [])}
    aln = {}
    for tag, d in v.items():
        for a in d.get("assistance_listings", []):
            aln.setdefault(a, []).append(tag)
    return list(v), pats, ntee, aln


def tag_text(text: str | None, default_other: bool = True) -> str:
    """';'-joined program-area tags for free text, in vocabulary order. Empty text -> '' ."""
    order, pats, _, _ = _vocab()
    if not text or not str(text).strip():
        return ""
    hits = [t for t in order if t in pats and pats[t].search(str(text))]
    return ";".join(hits) if hits else ("other" if default_other else "")


def tag_ntee(ntee: str | None) -> str:
    _, _, ntee_map, _ = _vocab()
    return ntee_map.get(str(ntee or "")[:3], "")


def tag_assistance_listing(aln: str | None) -> str:
    _, _, _, aln_map = _vocab()
    return ";".join(aln_map.get(str(aln or "").strip(), []))
