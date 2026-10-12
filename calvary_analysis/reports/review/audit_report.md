# Audit report: is the work correct?

Independent review (Prompt 3, Pass 1), 2026-10-10. Reviewer had no part in Prompts 1–2. Deliverables were read before the process files. Paths are relative to `calvary_analysis/`; recomputation code is in `scripts/` (this folder) and the row-level evidence in `evidence/`. Coverage by area and depth is in `review_coverage.csv`; every finding is a row in `review_findings.csv`.

## Overall judgment

**The arithmetic is sound; the interpretation has four material cracks.** Every module script reruns cleanly and regenerates the committed chart data; 100% of the one-pager and leadership-deck numbers, the full stress-test table and every Tier 1–2 pipeline score reproduce from the clean tables with independent code. Where numbers are wrong they are wrong in their labels or bases (nominal called real, 74% computed on a different base than the one named, all beds paired with a transitional-only share), not in their computation. The material problems are elsewhere: a stress-test apportionment the audited years contradict; a FY25 "event collapse" that is a 990 presentation change the data already shows; a lead prospect that closed in December 2025; and a sector-percentile method described as the opposite of what was run. The verdict's rating survives all of them. The decision-facing lists (Tier 1, the named prospects, the 90-day steps) do not survive intact.

## Ratings by deliverable

| Deliverable | Rating | Basis |
|---|---|---|
| `decks/executive_one_pager.pptx`, `reports/executive_one_pager.md` | **verified with caveats** | All figures reproduce or are rounding. Four need relabelling or softening: 74% of $4.1M (R02), 124 beds vs 6.8% (R12), event income −$483K (R15), $960K DHS loss as a point (R01). Clark named as the lead prospect (R16). |
| `decks/leadership_deck.pptx` | **verified with caveats** | 22/22 headlines match the spine; validator passes; all numbers reproduce. Slides 2, 3, 5, 7, 10, 11, 16, 17, 19, 20 carry the issues in R01–R03, R05, R06, R08, R12, R13, R15, R16. |
| `decks/consulting_deck.pptx` | **verified with caveats** | 55/55 headlines; validator passes; 25% sample of data slides reproduces except the sector-distribution method line (R07), "all 23 itemized" (M01), slide 66 appendix counts (M05), the Clean Power Institute row (R05) and the Clark rows (R16). |
| `decks/appendix_A–D.pptx` | **verified with caveats** | Validator passes; sampled cells reproduce (`evidence/recompute_m3to10.csv`); headline flags are by design (M10); appendix C inherits R05 and R16. |
| `reports/executive_summary.md` | **verified with caveats** | Same numbers as the leadership deck; same caveats. |
| `reports/full_findings.md` | **failed** | Stale after the CP3 consistency pass: mixed-denominator shares, 12 Tier 1 rows, $260M lens A, dead notes and an orphan chart reference (R11). Regenerate. |
| `reports/methodology.md` | **verified with caveats** | Accurate on what was done except the sector-distribution rule (R07), the TCP Schedule I rationale (M09) and three pipeline rules documented only in code (M03). |
| `reports/recommendations.md`, `recommendations/strategic_recommendations.md`, `recommendations/action_plan_90day.csv` | **verified with caveats** | Numbers consistent with the register; actionability problems in R06, R08, R09, R15, R16, R17. |
| `recommendations/funding_pressure_verdict.md` | **verified with caveats** | Evidence table reproduces; the rating stands; scenario table needs ranges (R01); 74% basis (R02). |
| `recommendations/funder_pipeline.csv` | **verified with caveats** | 154/154 scores and all components reproduce; two Tier 1 rows are not pursuable as written (Clark, America's Charities). |
| `insight_register.csv` | **verified with caveats** | Regenerates identically; M1-03 (events), M2-05 (scenario point estimates), M3-02 (method), M6-03 (high link) and M7-01 (Tier 1 names) need the fixes above before being marked verified. |
| `reports/board_readout.md`, `reports/consulting_briefing.md` | **verified with caveats** | Consistent with the deck; inherit R15 and R16 ("Clark Charitable, which gave five peers $7.8M"). |
| `chart_data/`, `_manifest.csv`, `config/png_data_map.csv` | **verified with caveats** | 58/60 CSVs regenerate identically; one orphan CSV; module-wide source_ids (M04). |
| `modules/*.md` | **verified with caveats** | Read through the consistency matrix and the register; "20 organizations" (M07). |
| People-data guardrails | **failed on one item** | No personal name in any deliverable; one cached web snippet in `sources/web_tier1_guidelines.csv` holds a contact's name and street address (R04). |

## 1. Reproducibility (1a)

Run in a scratch mirror of `calvary_analysis/` with `calvary_funding_data/` symlinked read-only; nothing in the project was written.

- `00_env_check.py`: 25 tables load, row counts match `data_quality.md`, six reviewer-guide self-checks pass, packages present.
- `01`–`10`, `12`, `13`: all exit 0.
- Chart data: 58 of 60 regenerated CSVs identical to the committed files; `m6_03_network_nodes` differs (layout coordinates and row order; a seed is set but node order is not sorted before writing); the committed folder holds `m1_04_surplus_net_assets.csv` from an earlier run that no script writes. `_manifest.csv` differs only by that orphan row.
- `funder_pipeline.csv`, `action_plan_90day.csv`, `insight_register.csv`: identical.
- `trace.py`: OK on the committed folder; fails on the clean regeneration because `full_findings.md` references the orphan chart id.
- `headline_check.py`: leadership 22/22 and consulting 55/55 match their spines; one-pager OK; appendix decks report 10/10/38/13 title flags (reference headers over 20 words and dividers), allowed by the CP3 note.
- pptx validator: all seven decks pass.

## 2. Independent recomputation (1b)

Code in `scripts/recompute_m1m2m9.py`, `scripts/pipeline_review.py`, `scripts/alt_apportionment.py` and the M3–M10 scripts (evidence CSVs). All read only `calvary_funding_data/clean/` and the config files.

**One-pager and leadership deck (M1, M2, M9):** 208 items; 107 exact, 96 rounding, 5 label or basis mismatches (R02, R03, R12, M07 ×2). Government share by year (41, 44, 40, 42, 49, 55, 50, 61, 51, 45, 58), FY22–24 mean 52.5%, filed grants $4,433,659 from 50 funders, GWCF 27.2%, top five 63.4%, HHI 1,168, every slide-6 bar, the stream map, ceilings $3,595,278 and $4,289,967 (73% and 67%), every scenario loss, deficit and months-of-cash value, ward indicators, PIT counts and bed shares reproduce. Months of cash after a year = (cash + baseline result − 0.5 × loss) ÷ (FY25 expenses ÷ 12), with the denominator not reduced for avoided cost; stated and reproduced.

**Stress test:** reproduces as built. The apportionment key fails against the audited SEFA (section 4 of `adversarial_review.md`, R01).

**Pipeline:** 154/154 institutional scores within 0.0005; all four formula-based components reproduce for every row; the tier rule holds for 153/154 (T. Rowe Price capped at Tier 2 by a script rule, M03); peers funded, peer amounts, medians, DC-sector dollars and recipients, gives-to-Calvary and itemized flags recomputed from `fact_grants` for 17 Tier 1–2 funders, 17/17 match. Median peer grant is the median over grant rows; per-peer totals are 2–7× higher (Abell $82.5K, GWCF $183K, Cafritz $150K); no tier changes either way.

**M3–M10 (leadership slides 13–23; 25% consulting sample covering every module; appendix B and C cells):** 643 items tested; 628 exact, 10 rounding, 5 mismatches; appendix B and C: 544 cells sampled (every 10th), 263 recomputed, 261 exact and 2 rounding. Material: the sector-distribution method (R07). Minor: Miriam's Kitchen "tripled since FY18" is 2.4× nominal; "all 23" is 22 of 23 (M01); corporate-foundation median $570 shown as $1K (M12); DWC "3× since 2018" is 2.97× nominal and 2.4× real; the 36 federal notices are a curated list (a mechanical filter gives 41). Several figures reproduce only under conventions the slides do not state: headroom 15 (non-DAF funders of 2+ peers, M13); lapsed 12 and $256K (DAF sponsors excluded); M8 area pools (recipient in DC/MD/VA rather than DMV funders; grants tagged both an area and general operating still count); appendix B6–7 do not apply the landscape exclusions. Peer ranks (11th on share, 3rd on growth, 5th on cash, 2nd on institutional depth), landscape totals, top-20 funders, DAF sponsors, gap counts, CRM statuses, network counts, expansion pools and comparator figures reproduce.

**Conventions:** audit basis, one source per stream, CoC lag, non-cumulative rows, exclusions, DAF separation and EIN aggregation are applied as stated. Two caveats: the audit-basis denominator is the audit's own revenue (range 39.7–61.4%, shown as 40–61%); OVSJG 2019 sums two records from the same source (M06).

**Reviewer-guide §4:** 6 of 6 pass.

## 3. Traceability (1c)

40 numbers across the one-pager, both decks, two appendix decks, `full_findings.md` and `executive_summary.md`. 36 chains complete (24 verbatim in the CSV, 12 clean derivations); 4 break: slide 5's 74% (cited chart yields 78%), slide 22's $2.8M (not in the cited charts), full findings' 1,027 organizations (universe size, not in the chart), appendix D's 231,647 alias rows (no chart id; verified directly). All 118 manifest source_ids resolve to a registry row with URL or file and publisher. Pattern: source_ids are module-wide rather than chart-specific, and several named tables' ids are missing, so the chain from table to registry is loose for those charts (M04). Detail in `evidence/trace_sample.csv` and `evidence/trace_report.md`.

## 4. Consistency (1d)

50 metrics across 36 documents (`evidence/consistency_matrix.csv`, 505 cells). Headline numbers agree everywhere. Eleven substantive disagreements: `full_findings.md` stale (R11); the 74%/$4.1M basis (R02); slide 3's "2024 dollars" (R03); slide counts (M05); "20 organizations" vs 21 (M07). Thirteen rounding and fifteen wording differences are listed in `evidence/consistency_disagreements.csv`.

## 5. Entity and interlock matches (1e)

2,078 grant rows to Calvary and the 18 peers from 331 funders: no funder split across ids; no namesake merges among the Tier 1 funders (Clark Charitable vs Clark-Winchcole, Abell vs The Abell Foundation, Eugene vs Annie E. Casey all separate); 38 of a 40-row sample plausible, 2 doubtful, 0 wrong; one recipient misattribution ($131,906 to My Sister's Place from Baltimore-area funders, M02). Interlocks: the single "high confidence" Calvary link is overstated and its funder flag inconsistent (R05); the seven medium links are labelled unconfirmed and confined to consulting and appendix materials; `candidate_interlocks` has no Calvary rows. Detail in `evidence/entities_report.md` (person ids only, no names).

## 6. People-data guardrails (1f)

138 text files and the seven decks (text export and raw XML) scanned against 48,563 `dim_person` names. 722 raw hits: 568 inside organization names (founder-named foundations), 154 artefacts of three non-person `dim_person` rows and punctuation spans; leadership materials 13 hits, all organization names. One real breach: a Tavily snippet cached in `sources/web_tier1_guidelines.csv` (row 58) with a foundation contact's name and street address (R04). Zero absolute paths, usernames or key material; the two `~/.config/calvary/keys.env` mentions are documentation. Medium-confidence interlock organizations appear in leadership files only as funders or peers.

## 7. Headlines and claims (1g)

Both decks' headlines read in order tell their stories and each headline follows from its slide, with the exceptions already listed: slide 3's label, slides 2/5's 74%, slide 10's point estimates, slide 11's "the audits would settle it" (the FY22–23 SEFA already says much), slide 16's channel-led chart without a caveat, slide 17's high-confidence link, slide 20's "foundation" label on a workplace-giving federation, and slide 7/19's event story (R15). The humble, recommendation-led tone is not a defect; every cloud the data shows is stated somewhere in the leadership deck except the two the team did not see (the Clark closure and the event reclassification) and the dated federal items in R18.

## 8. Known caveats: disclosed where they should be?

| Caveat | Disclosed | Adequate? |
|---|---|---|
| D1–D3 rest on Calvary's documents | Leadership slides 11, 24; consulting 65; reports | D1 yes; D2 yes (now resolvable: EHV ends 31 Dec 2026); D3 is resolvable from the 990 itself (R15), so the request to Calvary is no longer needed |
| Peers provisional | Every peer chart and footnote | Yes; the swap shows what moves (R10) |
| Line 1e as audit-equivalent FY24–25 | Consulting slides 4, 9; methodology | Yes |
| DHS one public year carried forward | Slides 5, 11, 15; scenarios.yaml | Yes, but the scenario table does not carry the caveat into the $960K figure (R01) |
| TY2024 partial filings | Slide 6 footnote; methodology | Yes |
| Corporate giving CRM-documented, cash-unverified | Slide 40; Tier 1 MGAC row | Yes |

## 9. How far can the numbers be trusted?

- **Trust as written:** Calvary's financial history, government share series, filed-grant base and concentration, stream amounts by year, pool shares, DC budget lines, peer ranks on share, growth, cash and institutional depth, landscape totals, network counts, ward and PIT figures, comparator profiles, pipeline arithmetic.
- **Trust with the stated caveat:** ceilings vs recognized (as a question), government share FY24–25 (line 1e), the FY24 DHS value.
- **Do not quote as written:** the $960K DHS loss and the other stream-specific scenario losses (quote ranges); the FY25 event-income drop; Clark as a prospect; America's Charities as a foundation; the 57th-percentile claim without naming the comparison set; "74% of a $4.1M base"; "$2.49M → $4.97M, 2024 dollars"; "124 beds, 6.8% of TH beds" as one phrase.
