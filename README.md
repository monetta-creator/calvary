# Calvary Women's Services funding engagement

Pro bono funding-strategy work for Calvary Women's Services (Washington DC, EIN 52-1307706), built from public records plus documents Calvary shared. Two questions anchor it: how much pressure Calvary's reliance on government funding creates, and which other funding fits its mission. Data as of 2026-10-10, revised after an independent review on 2026-10-11.

## What is here

| Path | What it is | Start with |
|---|---|---|
| `calvary_analysis/decks/pdf/` | **The deliverables**: leadership deck, consulting deck, one-pager, Appendices A–D (PDF) | `leadership_deck.pdf` |
| `calvary_analysis/web/Calvary_Grantmaker_Web.html` | Interactive map of the grantmakers around Calvary and 18 peers: one self-contained file, opens offline | download and double-click |
| `calvary_analysis/` | Analysis modules, findings register, recommendations, deck sources, reports | `calvary_analysis/README.md`, then `reports/executive_summary.md` |
| `calvary_funding_data/` | The data foundation: 25 clean tables, source registry, Calvary's documents (`inputs/`), data-quality and reviewer guides | `calvary_funding_data/README.md`, then `reports/reviewer_guide.md` |
| `docs/` | `decisions.md` (every ruling and why), `input_map.md`, `memory_reconciliation.md`, `briefs/` (the three engagement briefs) | `decisions.md` |
| `CLAUDE.md` | House rules and how an analyst (person or Claude) approaches a new request | read before working |
| `.claude/skills/` | Project skills for Claude Code: `new-deck`, `deck-edits`, `calvary-data` | loaded by Claude Code |
| `setup.sh` | One-time setup on a new machine | `./setup.sh` |

## Getting a copy

**From the work repository** (once it exists): `git clone <work repository URL> calvary`, then `cd calvary` and `./setup.sh`.

**Moving it into a work or enterprise GitHub.** The original private repository (`monetta-creator/calvary`) has a branch, `work-handoff`, made for this. It has its own fresh history and leaves out Calvary's two internal documents (see Data handling). Cloning only that branch downloads only that clean history, never the older commits:

```sh
# 1. On the work machine, clone just the clean branch. Sign in to the GitHub account that can read the
#    original repository when asked (`gh auth login`, or a personal access token as the password).
git clone --single-branch --branch work-handoff --no-tags https://github.com/monetta-creator/calvary.git calvary
cd calvary
git branch -m work-handoff main

# 2. Create an empty repository in the work GitHub (no README, no .gitignore), then point the copy at it.
git remote set-url origin <work repository URL>
git push -u origin main

# 3. Set up the environment.
./setup.sh
```

Check before the first push: `git log --oneline | wc -l` should print 1, and `ls calvary_funding_data/inputs | grep -c -e "Corporate Funders" -e "_internal"` should print 0.

## Setting up

```sh
./setup.sh                     # or: SKIP_DECKS=1 ./setup.sh  for Python and data only
```

`setup.sh` creates the Python 3.12 environment in `calvary_funding_data/.venv` and installs the pinned packages. It also rebuilds the two large tables, which are stored in parts (see `calvary_funding_data/clean/_parts/REJOIN.md`), installs the deck tooling and runs a self-check that ends with `TRACE OK`. It needs:
- **Python 3.12**: `uv` is recommended; `python3.12` also works.
- **Node 18+**: to rebuild decks.
- **LibreOffice** (`soffice`) and **poppler** (`pdftoppm`, `pdfinfo`): to render the decks. On macOS: `brew install --cask libreoffice` and `brew install poppler`.

The clone is about 260 MB. The raw downloads behind the data foundation (7 GB) are not in the repository and are not needed: every analysis runs from `calvary_funding_data/clean/`.

## Working with Claude Code

Open the repository folder in Claude Code. `CLAUDE.md` and the skills in `.claude/skills/` load automatically. Personal Claude memory does not travel between machines, so everything a new session needs is in the repository:
- the house rules and the analyst's approach (`CLAUDE.md`);
- the lead's rulings and their reasons (`docs/decisions.md`);
- the data traps and rerun order (`calvary-data` skill);
- the checkpointed process for a new deliverable (`new-deck` skill);
- the visual-edit workflow (`deck-edits` skill).

Ask for a new deliverable in plain words ("I want a deck explaining X"). The analyst comes back with options before building anything.

## Data handling

Two of Calvary's documents are internal: the CRM export (`Foundation & Corporate Funders_2023-2026.xlsx`) and the 2021–24 strategic plan report (`2021-2024 Strategic Plan Final Report_internal (1).pdf`). They are left out of the work copy (`work-handoff`) and listed in `.gitignore`, so they are not re-added by accident. The engagement lead holds them. Everything built from them stays: the reconciled CRM table (`clean/supp_crm_cash_verification.csv`) and the findings in the decks and reports. Only a full rebuild of the data foundation from its inputs (`calvary_funding_data/run_all.sh`, scripts 01 and 02) needs the originals; all analysis, decks and the web page run from `clean/`.

`calvary_funding_data/clean/` also holds person-level tables built from public filings (`dim_person`, `fact_roles`, `candidate_interlocks`). Keep the repository private, and run the guardrail scan described in `CLAUDE.md` before any copy or page goes beyond the team.

Everything is Markdown, CSV, PNG, PDF or PPTX with relative paths, so the folder moves between machines.
