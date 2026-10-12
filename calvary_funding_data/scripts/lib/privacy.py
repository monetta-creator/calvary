"""Second-pass redaction of individuals named as grant recipients.

990-PF and Schedule I grant lists sometimes name individuals (scholarships, emergency aid). The XML parser
already blanks recipients it identifies as individuals; this pass catches the rest among recipients that did
NOT resolve to an EIN. A name is treated as a person when it has 2-4 words, carries no organization keyword,
and its first word is a first name seen at least 3 times among people in the governance filings
(interim/stage_fact_roles__*.csv). Erring toward redaction costs little: such rows have no EIN to join on.
"""
from __future__ import annotations

import re
from functools import lru_cache

import pandas as pd

from .common import INTERIM

REDACTED = "[individual - name redacted]"
_NOT_FIRST = {"st", "saint", "new", "the", "united", "first", "grace", "faith", "hope", "trinity", "mount", "christ",
              "holy", "good", "san", "los", "la", "el", "de", "see", "north", "south", "east", "west", "central",
              "virginia", "georgia", "carolina", "jackson", "washington", "lincoln", "franklin", "madison", "wesley",
              "austin", "brooke", "jordan", "victoria", "charlotte", "camden", "hudson", "sierra", "dakota"}
_ORG = re.compile(
    r"(?i)\b(foundation|fdn|fund|inc|llc|ltd|corp|company|co|trust|school|schools|elementary|middle|high|church|"
    r"parish|ministr\w*|university|univ|college|academy|institute|center|centre|association|assn|society|club|"
    r"council|hospital|library|museum|league|alliance|coalition|network|services|service|project|program|"
    r"partners|chapter|friends|committee|district|county|city|state|department|dept|board|authority|community|"
    r"house|housing|home|homes|place|village|shelter|kitchen|bank|group|initiative|campaign|united|national|"
    r"international|america|american|usa|us|organization|org|ymca|ywca|scouts|habitat|charities|charity|"
    r"mission|temple|synagogue|mosque|congregation|cathedral|diocese|pta|pto|band|orchestra|theatre|theater|"
    r"opera|ballet|festival|fellowship|cooperative|clinic|health|medical|research|studies|education|"
    r"educational|fire|rescue|police|sheriff|veterans|legion|post|lodge|order|sisters|brothers|media|radio|tv|"
    r"pbs|npr|news|public|scholarship|scholarships|cancer|memorial|attached|schedule|attachment|statement|"
    r"various|recipients|individuals|grants|of|for|and|the|at|in)\b")


@lru_cache(maxsize=1)
def first_names() -> frozenset:
    counts: dict[str, int] = {}
    for p in INTERIM.glob("stage_fact_roles__*.csv"):
        names = pd.read_csv(p, dtype=str, usecols=lambda c: c in {"name_display", "name"}, keep_default_na=False)
        col = names.columns[0]
        for t in names[col].str.lower().str.replace(r"[^a-z\s]", " ", regex=True).str.split().str[0].dropna():
            counts[t] = counts.get(t, 0) + 1
    return frozenset(k for k, v in counts.items() if v >= 3 and len(k) > 1) - _NOT_FIRST


def person_like(name: str) -> bool:
    if not isinstance(name, str) or not name.strip():
        return False
    toks = re.sub(r"[^A-Za-z\s'-]", " ", name).lower().split()
    return 2 <= len(toks) <= 4 and toks[0] in first_names() and not _ORG.search(name)
