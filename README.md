# Calvary Women's Services funding engagement

Pro bono funding-strategy work for Calvary Women's Services (DC, EIN 52-1307706), built from public records. Two folders:

| Folder | What it is | Start with |
|---|---|---|
| `calvary_funding_data/` | Prompt 1: the data foundation (25 clean tables, source registry, data quality and reviewer guide, rebuild scripts) | `calvary_funding_data/README.md`, then `reports/reviewer_guide.md` |
| `calvary_analysis/` | Prompt 2: analysis modules, recommendations, decks and reports | `calvary_analysis/README.md`, then `reports/executive_summary.md` |

Also at this level: `input_map.md` (where every Prompt 2 input lives), `memory_reconciliation.md` (differences between the build's saved memory and its files, with rulings), the client template `2019 CalvaryPPT_White.pptx`, and copies of Calvary's documents that are also in `calvary_funding_data/inputs/`.

## Getting a copy

The GitHub repository `monetta-creator/calvary` is private, so you need to be added as a collaborator before you can see or clone it.

1. Send the repository owner your GitHub username and ask to be added as a collaborator. Accept the invitation from GitHub's email, or at https://github.com/monetta-creator/calvary/invitations.
2. Clone it (needs Git and a GitHub sign-in):
   ```sh
   git clone https://github.com/monetta-creator/calvary.git
   cd calvary
   ```
   GitHub does not accept account passwords for Git. If Git asks for one, sign in with the GitHub CLI (`gh auth login`) or use a personal access token. SSH also works: `git clone git@github.com:monetta-creator/calvary.git`.
3. Get later updates with `git pull`.

The download is about 260 MB because it includes the cleaned data tables. The two largest tables are stored in parts; before rerunning any scripts, rejoin them as described in `calvary_funding_data/clean/_parts/REJOIN.md`.

Without Git: sign in to GitHub as a collaborator, open the repository and choose **Code → Download ZIP**.

**Only want the interactive map?** `calvary_analysis/web/Calvary_Grantmaker_Web.html` is a single self-contained file. On GitHub, open it and choose **Download raw file**, then double-click the download. It opens in any browser and works offline. GitHub shows the file's code rather than the page, so download it first.

## Working with the files

Everything is Markdown, CSV, PNG or PPTX with relative paths, so the folder moves between machines. Python 3.12 (`calvary_funding_data/.venv`), Node (for the decks) and LibreOffice (for slide rendering) are the only tools needed. Data as of 2026-10-10.
