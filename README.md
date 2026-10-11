# Calvary Women's Services funding engagement

Pro bono funding-strategy work for Calvary Women's Services (DC, EIN 52-1307706), built from public records. Two folders:

| Folder | What it is | Start with |
|---|---|---|
| `calvary_funding_data/` | Prompt 1: the data foundation (25 clean tables, source registry, data quality and reviewer guide, rebuild scripts) | `calvary_funding_data/README.md`, then `reports/reviewer_guide.md` |
| `calvary_analysis/` | Prompt 2: analysis modules, recommendations, decks and reports | `calvary_analysis/README.md`, then `reports/executive_summary.md` |

Also at this level: `input_map.md` (where every Prompt 2 input lives), `memory_reconciliation.md` (differences between the build's saved memory and its files, with rulings), the client template `2019 CalvaryPPT_White.pptx`, and copies of Calvary's documents that are also in `calvary_funding_data/inputs/`.

Everything is Markdown, CSV, PNG or PPTX with relative paths, so the folder moves between machines. Python 3.12 (`calvary_funding_data/.venv`), Node (for the decks) and LibreOffice (for slide rendering) are the only tools needed. Data as of 2026-10-10.
