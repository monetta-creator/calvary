# Review script. Paths resolve from this file: calvary_analysis/reports/review/scripts/ -> project root three levels up.
import os as _os, pathlib as _pl
_HERE = _pl.Path(__file__).resolve().parent
PROJECT_ROOT = str(_pl.Path(_os.environ.get("CALVARY_ROOT", _HERE.parents[3])))
REVIEW_OUT = _os.environ.get("REVIEW_OUT", str(_HERE.parent / "evidence"))
import os, re, csv, sys, zipfile, subprocess, html
from collections import defaultdict, Counter
import pandas as pd

ROOT = PROJECT_ROOT
OUT = REVIEW_OUT
AN = os.path.join(ROOT, "calvary_analysis")
EXTS = {".md", ".csv", ".yaml", ".yml", ".py", ".js", ".json", ".txt"}
PY = sys.executable

# ---------- file inventory ----------
def rel(p): return os.path.relpath(p, ROOT)

text_files = []
for dp, dns, fns in os.walk(AN):
    dns[:] = [d for d in dns if d not in ("node_modules", "__pycache__")]
    if rel(dp).startswith("calvary_analysis/reports/review"):
        dns[:] = []
        continue
    for fn in fns:
        if fn.endswith(".lock"): continue
        if os.path.splitext(fn)[1].lower() in EXTS:
            text_files.append(os.path.join(dp, fn))
for extra in ("docs/input_map.md", "README.md", "CLAUDE.md"):
    p = os.path.join(ROOT, extra)
    if os.path.exists(p): text_files.append(p)
text_files.sort()

pptx_files = sorted(
    os.path.join(AN, "decks", f) for f in os.listdir(os.path.join(AN, "decks")) if f.endswith(".pptx"))

# Build "documents": list of (file_rel, [(location, line_text), ...])
docs = []
for p in text_files:
    try:
        with open(p, encoding="utf-8", errors="replace") as f:
            lines = [(str(i + 1), l.rstrip("\n")) for i, l in enumerate(f)]
    except Exception as e:
        lines = [("0", f"<<unreadable: {e}>>")]
    docs.append((rel(p), lines))

ATTR_RE = re.compile(r'\b(?:descr|name|title|alt)="([^"]*)"')
T_RE = re.compile(r"<a:t[^>]*>([^<]*)</a:t>")
for p in pptx_files:
    r = rel(p)
    # markitdown text
    try:
        md = subprocess.run([PY, "-m", "markitdown", p], capture_output=True, text=True, check=True).stdout
    except Exception as e:
        md = f"<<markitdown failed: {e}>>"
    lines, slide = [], "0"
    for i, l in enumerate(md.splitlines()):
        m = re.match(r"<!-- Slide number: (\d+) -->", l)
        if m: slide = m.group(1)
        lines.append((f"slide{slide}:md:{i+1}", l))
    docs.append((r + "#markitdown", lines))
    # raw xml
    xl = []
    with zipfile.ZipFile(p) as z:
        for name in sorted(z.namelist()):
            if not name.startswith("ppt/"): continue
            if not (name.endswith(".xml") or name.endswith(".rels")): continue
            raw = z.read(name).decode("utf-8", errors="replace")
            # paragraph text: join a:t runs within each a:p
            for pi, para in enumerate(re.findall(r"<a:p\b.*?</a:p>", raw, flags=re.S)):
                t = html.unescape("".join(T_RE.findall(para)))
                if t.strip(): xl.append((f"{name}:p{pi+1}", t))
            for ai, a in enumerate(ATTR_RE.findall(raw)):
                a = html.unescape(a)
                if a.strip(): xl.append((f"{name}:attr{ai+1}", a))
            # whole raw for path/secret scanning (one chunk per 2000 chars)
            for ci in range(0, len(raw), 2000):
                xl.append((f"{name}:raw{ci//2000+1}", raw[ci:ci+2000]))
    docs.append((r + "#xml", xl))

print("text files:", len(text_files), "pptx:", len(pptx_files), file=sys.stderr)

# ---------- Check 1: names ----------
def norm(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()

dp = pd.read_csv(os.path.join(ROOT, "calvary_funding_data/clean/dim_person.csv"), dtype=str).fillna("")
name_index = {}  # normalized name -> set(person_ids)
for _, row in dp.iterrows():
    cands = set()
    for col in ("name_display", "name_norm"):
        n = norm(row[col])
        if len(n.split()) >= 2: cands.add(n)
    fn, ln = norm(row["first_name"]), norm(row["last_name"])
    if fn and ln and len(fn) > 1 and len(ln) > 1:
        cands.add(f"{fn} {ln}")
    for c in cands:
        name_index.setdefault(c, set()).add(row["person_id"])
max_len = max(len(k.split()) for k in name_index)
print("name variants:", len(name_index), "max tokens", max_len, file=sys.stderr)

dfund = pd.read_csv(os.path.join(ROOT, "calvary_funding_data/clean/dim_funder.csv"), dtype=str, usecols=["funder_name"]).fillna("")
dorg = pd.read_csv(os.path.join(ROOT, "calvary_funding_data/clean/dim_org.csv"), dtype=str, usecols=["org_name", "org_name_bmf", "dba_name"]).fillna("")
org_names = set()
def norm2(s):
    return norm(s.replace("&", " and ").replace("'s", "s").replace("’s", "s"))
for s in (dfund["funder_name"], dorg["org_name"], dorg["org_name_bmf"], dorg["dba_name"]):
    for v in s:
        for n in (norm(v), norm2(v)):
            if n: org_names.add(n)
org_names = sorted(org_names)
print("org names:", len(org_names), file=sys.stderr)

org_cache = {}
def orgs_containing(name):
    if name not in org_cache:
        pat = re.compile(r"\b" + re.escape(name) + r"\b")
        org_cache[name] = [o for o in org_names if pat.search(o)]
    return org_cache[name]

NONPERSON_IDS = {"P2e2f5b0a16": "dim_person row is a placeholder token, not a person (judged from name tokens)",
                 "Pb6f09c167b": "dim_person row is an organization fragment, not a person (judged from name tokens)",
                 "Pc733246cc9": "dim_person row is a parse artifact, not a person (judged from name tokens)"}
SEG_RE = re.compile(r"[^|<>\"\[\]{}]+")
def classify(name, line, line_norm, s, e, pids):
    line = html.unescape(line)
    line_norm = norm(line)
    # (a) exact org-name containment
    ln2 = norm2(line)
    for o in orgs_containing(name):
        if o in line_norm or o in ln2:
            return "org-name", "org name contains match"
    # (a') truncated org cell: segment ending in an ellipsis that is a prefix of an org name
    for m in SEG_RE.finditer(line):
        if m.start() <= s and m.end() >= e:
            seg = m.group(0).strip()
            if "…" in seg[len(seg)-max(1, e - m.start()) - 2:] or seg.endswith("…") or seg.endswith("..."):
                raw_pre = seg.split("…")[0].split("...")[0]
                pres = {norm(raw_pre), norm2(raw_pre)}
                if all(len(x) >= 6 for x in pres) and any(o.startswith(x) for o in orgs_containing(name) for x in pres):
                    return "org-name", "truncated org cell (prefix of org name)"
            break
    span = line[s:e]
    if re.search(r"[,;&'’.()/:]", span):
        return "person", "doubtful: match spans punctuation"
    for pid in pids:
        if pid in NONPERSON_IDS:
            return "person", "doubtful: " + NONPERSON_IDS[pid]
    return "person", ""

TOK_RE = re.compile(r"[A-Za-z0-9]+")
name_rows = []
for frel, lines in docs:
    for loc, line in lines:
        toks = [(m.group(0).lower(), m.start(), m.end()) for m in TOK_RE.finditer(line)]
        if len(toks) < 2: continue
        line_norm = norm(line)
        found = []
        i = 0
        n = len(toks)
        while i < n:
            best = None
            for L in range(min(max_len, n - i), 1, -1):
                cand = " ".join(t[0] for t in toks[i:i+L])
                if cand in name_index:
                    best = (L, cand); break
            if best:
                L, cand = best
                s, e = toks[i][1], toks[i+L-1][2]
                found.append((s, e, cand))
                i += L
            else:
                i += 1
        for s, e, cand in found:
            pids = sorted(name_index[cand])
            ctx = line[max(0, s-60):s] + "[NAME]" + line[e:e+60]
            ctx = ctx.replace("\n", " ")
            cls, note = classify(cand, line, line_norm, s, e, pids)
            name_rows.append({
                "file": frel, "line_or_slide": loc,
                "matched_name_person_id": ";".join(pids),
                "n_tokens": len(cand.split()),
                "context_60chars": ctx,
                "classification": cls, "note": note,
            })

def loc_key(loc):
    nums = re.findall(r"\d+", loc)
    return tuple(int(x) for x in nums) + (loc,)
name_rows.sort(key=lambda r: (r["file"], loc_key(r["line_or_slide"]), r["context_60chars"]))
with open(os.path.join(OUT, "names_hits.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["file", "line_or_slide", "matched_name_person_id", "n_tokens", "context_60chars", "classification", "note"])
    w.writeheader(); w.writerows(name_rows)

by_cls = Counter(r["classification"] for r in name_rows)
by_file = defaultdict(Counter)
for r in name_rows: by_file[r["file"]][r["classification"]] += 1
with open(os.path.join(OUT, "names_summary.md"), "w") as f:
    f.write("# Check 1: personal-name hits\n\n")
    f.write(f"Name variants indexed: {len(name_index)} (from {len(dp)} dim_person rows; name_display, name_norm, first+last).\n")
    f.write(f"Files scanned: {len(text_files)} text files + {len(pptx_files)} pptx (markitdown text and raw XML).\n\n")
    f.write("## Counts by classification\n\n| classification | hits |\n|---|---|\n")
    for k, v in sorted(by_cls.items()): f.write(f"| {k} | {v} |\n")
    f.write(f"| total | {len(name_rows)} |\n\n")
    f.write("## 'person' hits by note (sub-signal)\n\n| note | hits |\n|---|---|\n")
    for k, v in sorted(Counter(r["note"] or "(none: plain person-name match)" for r in name_rows if r["classification"] == "person").items()):
        f.write(f"| {k} | {v} |\n")
    f.write("\n## Counts by file\n\n| file | person | org-name | distinct person_ids (person) |\n|---|---|---|---|\n")
    for fr in sorted(by_file):
        pids = set()
        for r in name_rows:
            if r["file"] == fr and r["classification"] == "person":
                pids.update(r["matched_name_person_id"].split(";"))
        f.write(f"| {fr} | {by_file[fr]['person']} | {by_file[fr]['org-name']} | {len(pids)} |\n")
    f.write("\n## Most frequent person_ids classified 'person'\n\n| person_id(s) | hits | files |\n|---|---|---|\n")
    c = Counter(); files = defaultdict(set)
    for r in name_rows:
        if r["classification"] == "person":
            c[r["matched_name_person_id"]] += 1; files[r["matched_name_person_id"]].add(r["file"])
    for k, v in sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[:40]:
        f.write(f"| {k} | {v} | {len(files[k])} |\n")

# ---------- Check 2: paths ----------
PATH_PATS = ["/Users/", "/home/", "C:\\", "\\Users\\", "$HOME", "~/", "file://"]
path_rows = []
for frel, lines in docs:
    for loc, line in lines:
        for pat in PATH_PATS:
            for m in re.finditer(re.escape(pat), line):
                s = m.start()
                ctx = line[max(0, s-40):s+80].replace("\n", " ")
                cls = "hit"
                if pat == "~/" and line[s:s+len("~/.config/calvary/keys.env")] == "~/.config/calvary/keys.env":
                    cls = "allowed-doc-reference"
                path_rows.append({"file": frel, "line_or_location": loc, "pattern": pat, "context_80chars": ctx, "classification": cls})
path_rows.sort(key=lambda r: (r["file"], loc_key(r["line_or_location"]), r["pattern"], r["context_80chars"]))
with open(os.path.join(OUT, "path_hits.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["file", "line_or_location", "pattern", "context_80chars", "classification"])
    w.writeheader(); w.writerows(path_rows)

# ---------- Check 3: secrets ----------
SEC_PATS = ["tvly-", "TAVILY_API_KEY", "api_key", "apikey", "Bearer ", "secret", "token="]
HEX_RE = re.compile(r"(?i)(?:key.{0,40}?([A-Za-z0-9+/_\-=]{32,}))|(?:([A-Za-z0-9+/_\-=]{32,}).{0,40}?key)")
key_values = []
kp = os.path.expanduser("~/.config/calvary/keys.env")
if os.path.exists(kp):
    with open(kp) as f:
        for l in f:
            if "=" in l:
                v = l.split("=", 1)[1].strip().strip('"').strip("'")
                if len(v) >= 8: key_values.append(v)
sec_rows = []
for frel, lines in docs:
    for loc, line in lines:
        for pat in SEC_PATS:
            for m in re.finditer(re.escape(pat), line, flags=re.I if pat in ("api_key", "apikey", "secret") else 0):
                s = m.start()
                sec_rows.append({"file": frel, "line_or_location": loc, "pattern": pat,
                                 "context_80chars": line[max(0, s-40):s+80]})
        for m in HEX_RE.finditer(line):
            s = m.start()
            sec_rows.append({"file": frel, "line_or_location": loc, "pattern": "32+char-string-near-key",
                             "context_80chars": line[max(0, s-20):s+100]})
        for v in key_values:
            if v in line:
                sec_rows.append({"file": frel, "line_or_location": loc, "pattern": "KEYS_ENV_VALUE_PRESENT",
                                 "context_80chars": "<<redacted: actual key value found>>"})
keys_env_named = [rel(os.path.join(d, fn)) for d, _, fns in os.walk(AN) for fn in fns if fn == "keys.env"]
for k in keys_env_named:
    sec_rows.append({"file": k, "line_or_location": "-", "pattern": "file-named-keys.env", "context_80chars": ""})
sec_rows.sort(key=lambda r: (r["file"], loc_key(r["line_or_location"]), r["pattern"], r["context_80chars"]))
with open(os.path.join(OUT, "secrets_hits.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["file", "line_or_location", "pattern", "context_80chars"])
    w.writeheader(); w.writerows(sec_rows)

# ---------- Check 4: interlock placement ----------
il = pd.read_csv(os.path.join(AN, "chart_data/m6_04_board_interlocks.csv"), dtype=str).fillna("")
med = il[il["confidence"].str.lower() == "medium"]
med_orgs = sorted(set(med["other_name"]))
med_orgs = [o for o in med_orgs if o and o.lower() != "calvary"]
LEAD = ["calvary_analysis/decks/leadership_deck.pptx", "calvary_analysis/decks/executive_one_pager.pptx",
        "calvary_analysis/reports/executive_one_pager.md", "calvary_analysis/reports/executive_summary.md",
        "calvary_analysis/reports/board_readout.md"]
il_rows = []
for frel, lines in docs:
    base = frel.split("#")[0]
    if base not in LEAD: continue
    if frel.endswith("#xml"):
        lines = [(l, t) for l, t in lines if ":raw" not in l]
    for loc, line in lines:
        ln = norm(line)
        for o in med_orgs:
            if norm(o) in ln:
                il_rows.append({"file": frel, "location": loc, "organization": o, "context": line[:200]})
        for kw in ("medium confidence", "unconfirmed"):
            if kw in line.lower():
                il_rows.append({"file": frel, "location": loc, "organization": f"<keyword:{kw}>", "context": line[:200]})
il_rows.sort(key=lambda r: (r["file"], loc_key(r["location"]), r["organization"]))
with open(os.path.join(OUT, "interlock_placement.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["file", "location", "organization", "context"])
    w.writeheader(); w.writerows(il_rows)

# ---------- stats for report ----------
import json
stats = {
    "text_files": len(text_files), "pptx_files": len(pptx_files),
    "names_total": len(name_rows), "names_by_cls": dict(by_cls),
    "names_person_by_note": dict(Counter(r["note"] or "plain" for r in name_rows if r["classification"] == "person")),
    "paths_total": len(path_rows), "paths_by_cls": dict(Counter(r["classification"] for r in path_rows)),
    "paths_by_pattern": dict(Counter(r["pattern"] for r in path_rows if r["classification"] == "hit")),
    "secrets_total": len(sec_rows), "secrets_by_pattern": dict(Counter(r["pattern"] for r in sec_rows)),
    "keys_env_vars": len(key_values), "keys_env_named_files": keys_env_named,
    "medium_interlock_orgs": med_orgs, "interlock_rows": len(il_rows),
    "interlock_by_file": dict(Counter(r["file"] for r in il_rows)),
}
with open(os.path.join(OUT, "stats.json"), "w") as f: json.dump(stats, f, indent=1, sort_keys=True)
print(json.dumps(stats, indent=1, sort_keys=True))
