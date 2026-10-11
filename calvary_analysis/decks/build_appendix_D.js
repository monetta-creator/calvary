// Appendix D: Data and methods. Follows storylines/appendix_headline_spine.md (Appendix D, items 1-24).
// Method-note text is condensed from reports/methodology.md §5 and the module readouts (modules/*.md); every slide cites both.
const path = require("path");
const C = require("./build_appendix_common");
const { D, HEX, M, W, BODY_Y, BODY_H, FULL_W, trunc, num, usd, money, pct, n0, tbl } = C;

const METH = "calvary_analysis/reports/methodology.md";
// Parse the first Markdown table after a heading that matches `re` (cells stripped of backticks and bold).
function mdTable(text, re) {
  const lines = text.split("\n"); let i = lines.findIndex(l => re.test(l)); if (i < 0) throw new Error(`heading not found: ${re}`);
  while (i < lines.length && !/^\|/.test(lines[i])) i++;
  const rows = [];
  for (; i < lines.length && /^\|/.test(lines[i]); i++) {
    const cells = lines[i].replace(/^\||\|$/g, "").split("|").map(c => c.trim().replace(/`/g, "").replace(/\*\*/g, ""));
    if (cells.every(c => /^:?-+:?$/.test(c))) continue;
    rows.push(cells);
  }
  return { header: rows[0], rows: rows.slice(1) };
}
// Bullet list after a heading (lines starting with "- ").
function mdBullets(text, re) {
  const lines = text.split("\n"); let i = lines.findIndex(l => re.test(l)); const out = [];
  for (i++; i < lines.length && !/^#{1,3} /.test(lines[i]); i++) if (/^- /.test(lines[i])) out.push(lines[i].slice(2).replace(/`/g, "").replace(/\*\*/g, ""));
  return out;
}
const scrub = (s) => String(s).replace(/~\/\.config\/calvary\/keys\.env/g, "user config file").replace(/\/Users\/[^\s)]+/g, "(local path)");

(async () => {
  const X = C.makeDeck("Appendix D: Data and methods", "Appendix D of the Calvary funding analysis");
  const meth = C.readText(METH);

  // 1. Title
  X.section("Appendix D");
  X.title("Appendix D documents the inputs, universes, measures, assumptions and method notes behind every figure.",
    "Appendix D · Data and methods · pro bono funding analysis for Calvary Women's Services. Method notes A1–D3 are the numbers that slide footnotes cite in Appendices A–C.");

  // 2. Input map
  X.section("Inputs and data quality");
  const im = mdTable(C.readText("input_map.md"), /^# Input map/);
  X.table("The input map lists each input and where it lives, and every input the brief described was found.",
    ["Input", "Location (relative to the project root)", "What was found", "Missing or ambiguous"],
    im.rows.map(r => [r[0], trunc(scrub(r[1]), 70), trunc(scrub(r[2]), 110), trunc(scrub(r[3]), 70)]),
    [1.9, 3.0, 4.6, 2.63],
    { source: "input_map.md (written at CP1)", method: "inventory of every input named in the analysis brief; paths are relative; API keys stay outside the project and are never written to outputs", chart: null, note: "D2" },
    { rowsPerSlide: 9, fontSize: 8.5 });

  // 3. Universes
  const un = mdTable(meth, /^### 3\.1 Universes/);
  X.table("Universe rules and sizes run from Calvary alone to 7,705 DMV funders, with 15,812 distinct EINs across all universes.",
    ["Universe", "EINs", "Rules (EINs)", "Definition"], un.rows.map(r => [r[0], r[1], r[2], trunc(r[3], 150)]),
    [1.9, 0.8, 2.2, 7.23],
    { source: "IRS EO Business Master File and e-file index (releases 2021–2026); calvary_funding_data/reports/universe_summary.md; config/universes.yaml", method: "rules applied by scripts/20_build_universes.py; size band 0.5–2× Calvary's TY2022–24 median revenue ($4,967,995)", chart: null, note: "D2" },
    { rowsPerSlide: 10, fontSize: 9.5 });

  // 4. Source registry
  const reg = C.readAny("calvary_funding_data/sources/source_registry.csv");
  const ext = C.readAny("calvary_analysis/sources/source_registry_extension.csv");
  const complete = [...reg, ...ext].every(r => String(r.url_or_file).trim() && String(r.retrieved_date).trim());
  const byPrefix = {}; reg.forEach(r => { const k = r.source_id.split("_")[0]; byPrefix[k] = (byPrefix[k] || 0) + 1; });
  const PFX = { web: "web pages: Calvary, peers, comparators, funders", input: "client-provided files", api: "API pulls", bulk: "bulk downloads", doc: "government documents", ref: "reference" };
  let s = X.head(`The source registry covers ${reg.length} sources plus ${ext.length} web guideline pages, ${complete ? "each" : "most"} with a URL or file and retrieval date.`);
  tbl(s, ["Acquisition type (source_id prefix)", "Sources"], Object.entries(byPrefix).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])).map(([k, v]) => [`${k}_ (${PFX[k] || k})`, String(v)])
    .concat([["Registry extension: web guideline pages (Phase 3 pull)", String(ext.length)]]),
    { x: M, y: BODY_Y, w: 4.9, colW: [3.9, 1.0], fontSize: 10, align: ["left", "right"] });
  const pubT = (() => { const t = meth.split("**By publisher type**")[1]; return mdTable("x\n" + t, /^x$/); })();
  tbl(s, ["Publisher type", "Sources", "Publishers", "Examples"], pubT.rows.map(r => [r[0], r[1], r[2], trunc(r[3], 48)]),
    { x: 5.8, y: BODY_Y, w: 6.93, colW: [2.9, 0.75, 0.85, 2.43], fontSize: 9, align: ["left", "right", "right", "left"] });
  s.addText(`Every row in the registry and its extension carries a URL or file path and a retrieval date (all ${[...new Set([...reg, ...ext].map(r => r.retrieved_date))].join(", ")}). The API catalog records 65 sources probed: 55 ok, 4 ok with no results, 3 blocked pending a key (skipped as not needed), 2 not applicable, 1 failed.`,
    { x: M, y: 4.5, w: 4.9, h: 1.9, fontSize: 10, color: HEX.text2, margin: 0, isTextBox: true, valign: "top" });
  D.footnote(s, { source: "calvary_funding_data/sources/source_registry.csv; calvary_analysis/sources/source_registry_extension.csv; sources/api_catalog.md (via methodology.md §2.2)", method: "counts by source_id prefix and by publisher group; extension rows come from the analyst-reviewed Tier 1–2 guideline pull", chart: null, note: "D2" });

  // 5. Data quality (three slides)
  const dq = C.readText("calvary_funding_data/reports/data_quality.md");
  const rc = mdTable(dq, /^## 1\. Row counts/).rows.filter((r, i, a) => a.findIndex(x => x[0] === r[0]) === i);
  const H5 = "Data quality: row counts, reconciliation results, match rates and known gaps are documented for every table.";
  const foot5 = { source: "calvary_funding_data/reports/data_quality.md §1, §4, §7–§9; reports/reviewer_guide.md §2 (via methodology.md §2.4–2.5)", method: "pandas row counts (never line counts); checks run by the data build's quality script and the analysis environment check", chart: null, note: "D3" };
  s = X.head(H5);
  const half = Math.ceil(rc.length / 2);
  [rc.slice(0, half), rc.slice(half)].forEach((part, k) => tbl(s, ["Clean table", "Rows"], part.map(r => [r[0], n0(r[1])]),
    { x: M + k * 4.2, y: BODY_Y, w: 3.9, colW: [2.7, 1.2], fontSize: 9.5, align: ["left", "right"] }));
  D.card(s, { x: 9.0, y: BODY_Y, w: W - M - 9.0, h: 4.6, title: "Counting notes", fontSize: 10.5, lines: [
    "entity_aliases has 231,647 parsed rows; its 231,678 physical lines include 31 quoted names with line breaks.",
    "fact_gov_awards shows the same effect: 40,300 rows in 42,958 lines.",
    "fact_grants (567 MB) and fact_org_relationships (101 MB) are read with selected columns.",
    "No duplicate primary keys."] });
  D.footnote(s, foot5);
  s = X.head(`${H5} (continued, 2 of 3)`);
  const qc = mdTable(meth, /^### 2\.4 Prompt 1 quality checks/);
  tbl(s, ["Check", "Result"], qc.rows.map(r => [r[0], trunc(r[1], 150)]), { x: M, y: BODY_Y, w: FULL_W, colW: [4.4, 7.73], fontSize: 9 });
  D.footnote(s, foot5);
  s = X.head(`${H5} (continued, 3 of 3)`);
  D.card(s, { x: M, y: BODY_Y, w: 5.9, h: BODY_H - 0.2, title: "Reconciliation and match rates", fontSize: 10.5, lines: [
    "Calvary's revenue: one row per fiscal year and source FY2011–FY2025; 990-family sources agree, audits differ 0–9% by design (Appendix A, slide 2).",
    "FY21: audit government revenue $1,981,161 vs 990 line 1e $503,222.",
    "CRM: of 160 funders, 25 confirmed in window, 7 earlier only, 7 attachment-only lists, 29 with no filing rows, 92 not exempt filers.",
    "Unmatched recipients: 76,801 rows and $3,972,062,391 (10.0% of DC/MD/VA named-recipient dollars) lack an EIN; 'see attached' rows (667, $3,497,262,549) reported separately.",
    "Person matching: 48,563 people; 2,036 linked across organizations (597 high, 1,439 medium); 1,270 low-confidence pairs held back."] });
  D.card(s, { x: 6.83, y: BODY_Y, w: 5.9, h: BODY_H - 0.2, title: "Known coverage gaps", fontSize: 10, lines: mdBullets(dq, /^## 9\. Known coverage gaps/).map(b => /^XML fetch/.test(b) ? "XML fetch: 0 of 31,483 targeted returns not retrieved." : trunc(b, 130)) });
  D.footnote(s, foot5);

  // 6. Memory reconciliation
  const mr = mdTable(meth, /^## 8\. Memory reconciliation summary/);
  X.table("Memory reconciliation found eight differences, none affecting a finding.",
    ["#", "Item", "Memory said", "Files show", "Severity", "Ruling (2026-10-10)"],
    mr.rows.map(r => [r[0], r[1], trunc(r[2], 60), trunc(r[3], 95), trunc(r[4], 40), trunc(r[5], 80)]),
    [0.35, 1.9, 2.3, 3.6, 1.5, 2.48],
    { source: "memory_reconciliation.md (CP1); methodology.md §8", method: "project memory compared with project files; files are the working source of truth; no item rated High", chart: null, note: "D3" },
    { rowsPerSlide: 8, fontSize: 8.5 });

  // 7-21. Method notes
  X.section("Method notes");
  function note(id, headline, question, method, caveats, confidence, cite) {
    const s = X.head(headline);
    D.card(s, { x: M, y: BODY_Y, w: 7.6, h: BODY_H - 0.15, title: `Question: ${question}`, fontSize: 11.5, lines: method });
    D.card(s, { x: 8.5, y: BODY_Y, w: W - M - 8.5, h: 2.85, title: "Caveats", fontSize: 11, lines: caveats });
    D.card(s, { x: 8.5, y: BODY_Y + 3.0, w: W - M - 8.5, h: BODY_H - 0.15 - 3.0, title: "Confidence", fontSize: 11, lines: [confidence] });
    D.footnote(s, { source: `${METH} §5 ${id}; ${cite.readout}; ${cite.config}`, method: cite.method, chart: cite.chart, note: id });
  }
  note("A1", "Method note A1: government share uses the audit basis through FY23 and 990 line 1e for FY24–25, which matched the audits in FY22–23.",
    "how large is government money in Calvary's revenue, and how reliable is each measure?", [
      "Revenue, expenses, net assets and cash come from fact_org_financials preferred 990 rows, one per fiscal year; five sources agree within 1%.",
      "Government revenue: audit basis (contracts and grants) FY13–FY23; 990 Part VIII line 1e FY24–FY25.",
      "Line 1e misses contracts booked as program revenue: the FY21 audit shows $1,981,161 against $503,222 on line 1e.",
      "Private contributions ex-events = contributions total − government − line 1c events; institutional giving is measured from funders' filings instead (A3).",
      "Real values: CPI-U annual average, base 2024, by the calendar year in which the fiscal year ends.",
      "Peers: line 1e ÷ total revenue on preferred rows, FY2015–FY2025."],
    ["No FY24 or FY25 audits are public; those years rest on the 990.", "The 990 cannot split individuals from foundations in private contributions.", "Months of cash is comparable from FY2020."],
    "High on revenue, margin, liquidity and government share through FY23; medium on the FY24–25 government share (990 only).",
    { readout: "modules/m1_calvary_trajectory.md", config: "no config file (preferred-row ranking set in the data build)", method: "share = government revenue ÷ total revenue on the stated basis", chart: "m1_01–m1_06" });
  note("A2", "Method note A2: each government stream uses one source, never summed, with DC fiscal years as Calvary's and CoC years lagged one.",
    "which government streams fund Calvary, and how big is each?", [
      "OVSJG: award lists, DC FY2019–2026.",
      "HUD CoC via TCP: award lists, competition years 2019–FY2025; each project is stored once as a subaward with TCP as pass-through.",
      "DHS provider contracts via TCP: Council oversight responses, DC FY2024 only.",
      "Small federal pass-throughs (EFSP, SNAP E&T): audited SEFA lines.",
      "One-time money listed separately: SLFRF $3.68M, PPP $327K, HUD CPF $200K.",
      "Calendars: DC FY = Calvary FY; CoC competition year t → Calvary operating year t+1; SEFA = expenditure in the audited year; the FAC 'audit year 2023' record duplicates FY22, so the FY23 audit PDF ($937,999) is used.",
      "Stream durability (annual, renewal, at-risk) is an analyst rating."],
    ["DHS/TCP amounts are public for FY2024 only; other years are unknown, not zero.", "The one-year CoC lag is an assumption set in config.", "Federal policy risk (2025 CoC NOFO, EHV sunset) is only partly in the data."],
    "High on the stream map, pool shares and DC budget lines; durability ratings are judgment.",
    { readout: "modules/m2_government_exposure.md", config: "config/scenarios.yaml (coc_award_lag_years)", method: "one source_type per stream from fact_gov_awards", chart: "m2_01, m2_01b, m2_03, m2_05" });
  note("A3", "Method note A3: filed grants to Calvary come from funders' own filings for TY2020–24, exclude cumulative rows and aggregate by funder EIN.",
    "which institutions fund Calvary, and how concentrated is that base?", [
      "fact_grants 990-PF and Schedule I rows naming Calvary, TY2020–24, non-cumulative, aggregated by funder EIN.",
      "The base is 138 rows from 50 funders, $4.43M.",
      "Concentration = each funder's share of five-year filed grants plus a Herfindahl index (1,168).",
      "GWCF is the largest filed funder at $1,206,500 under two raw spellings on one EIN; the Health Equity Fund is attributed to GWCF as funder of record.",
      "CRM export: 160 funders, $10.56M, treated as cumulative over an unconfirmed 2023–26 window (assumption A1) and as cash unless contradicted (A2); checked against each funder's filings and never added to filed annual grants."],
    ["Funder tax years do not align with Calvary's fiscal year.", "TY2024 filings are partial and TY2025 mostly unfiled, so 'flat' after TY2023 is partly filing lag.", "The CRM covers institutional gifts only."],
    "High on the concentration of filed grants.",
    { readout: "modules/m1_calvary_trajectory.md", config: "calvary_funding_data/config/funder_match_overrides.csv", method: "funder share = funder total ÷ $4.43M; HHI on shares", chart: "m1_07, m1_08" });
  note("A4", "Method note A4: scenarios split FY25 government revenue by ceiling share and apply configured cuts, and the net view treats half as avoidable cost.",
    "what happens to revenue, deficit and cash if government streams are cut?", [
      "Baseline: FY25 recognized government revenue ($2.89M) apportioned by ceiling share: OVSJG 23%, CoC 41%, DHS 33%, other 2%.",
      "Each scenario applies its cuts to those stream amounts; gross = the revenue loss; net assumes 50% of a lost stream's revenue is avoidable program cost.",
      "Outputs: revenue loss, deficit, months of cash after a year and months until cash runs out.",
      "Parameters: baseline_fiscal_year 2025; cost_avoidance_share 0.5; dhs_assumed_flat_from_fy2024 true; coc_award_lag_years 1.",
      "S1 OVSJG −10%; S2 OVSJG −25%; S3 CoC −15%; S4 New Foundations 2 lost; S5 DHS/TCP not renewed; S6 combined. Levels set by the CP1 ruling."],
    ["Stream shares come from award ceilings, not Calvary's ledger.", "The DHS value is the FY2024 figure carried forward.", "Cost avoidance of 50% is an assumption."],
    "Medium: apportionment and carry-forward assumptions drive the stream amounts.",
    { readout: "modules/m2_government_exposure.md", config: "config/scenarios.yaml", method: "scenario arithmetic in scripts/02_m2_exposure.py", chart: "m2_07" });
  note("A5", "Method note A5: award ceilings are aligned to Calvary's fiscal year and compared with recognized revenue, not substituted for it.",
    "does Calvary recognize the government money it is awarded?", [
      "Ceilings come from the A2 sources, aligned to Calvary's fiscal year: DC FY = Calvary FY, CoC lagged one year, DHS FY2024 carried forward.",
      "They are compared with recognized government revenue (990 line 1e for FY24–25) in m2_02.",
      "Result, discovery flag D1: FY24 ceilings $3.6M vs $2.62M recognized; FY25 $4.3M vs $2.89M.",
      "Approved at CP2 as a medium-confidence finding labeled 'ceilings vs recognized'.",
      "Possible explanations: undrawn awards, timing, cost-reimbursement limits or an overstated DHS carry-forward; the data cannot distinguish them."],
    ["DHS values before FY2024 are unknown, so earlier ceilings are understated.", "EFSP and SNAP E&T are held at the audited FY23 level."],
    "Medium. The FY24 and FY25 audits and TCP subgrant agreements would resolve it.",
    { readout: "modules/m2_government_exposure.md", config: "config/scenarios.yaml (dhs_assumed_flat_from_fy2024, coc_award_lag_years)", method: "ratio = recognized government revenue ex SLFRF ÷ known ceilings", chart: "m2_02" });
  note("A6", "Method note A6: DC budget lines are activity-level totals from the budget books, and policy events add Council reports and Budget Support Acts.",
    "are the DC pools Calvary draws on growing or shrinking, and when are they cut?", [
      "supp_dc_budget_lines (5,172 rows): activity-level totals from the DC Approved Budget and Financial Plan books FY2024–FY2027, approved vs actual vs Mayor's proposal; each book carries two years of actuals and two approved years.",
      "fact_policy_events (297 rows): dated changes from the budget books, Council committee budget reports, Council Budget Office change charts and the Budget Support Acts FY2024–FY2027.",
      "Committee recommendations the Council did not enact stay as budget_proposed.",
      "Budget tables tie to printed totals (257 of 257).",
      "Lines tracked: OVSJG Victim Services grants, the DHS homeless-services continuum and local PSH, alongside DCHA, DBH, DHCD and DOES."],
    ["The Mayor's proposals are as reported by Council committees.", "Actual spending is available only for years with a later book."],
    "High on the DC budget lines.",
    { readout: "modules/m2_government_exposure.md", config: "no config file", method: "sums of activity-level 'total' rows per program code", chart: "m2_04, m2_05, m2_06" });
  note("B1", "Method note B1: peer metrics use preferred 990 rows, FY2022–24 government-share means and FY2019–24 real growth that skips the FY22 award.",
    "how does Calvary compare with its peers on mix, size, growth and liquidity?", [
      "Preferred 990 rows FY2015–FY2025 for Calvary, the 18 provisional peers and the two named comparators.",
      "Government share: line 1e ÷ total revenue (Calvary FY≤2023 on the audit basis); FY2022–24 means smooth reporting breaks such as Coalition for the Homeless FY23 and Samaritan Inns FY24.",
      "Real growth: CAGR of 2024-dollar revenue FY2019 → FY2024.",
      "Months of cash: cash and savings ÷ monthly expenses.",
      "Typology on the three-year mean: government-anchored ≥65%, mixed 35–65%, philanthropy-led <35%.",
      "Sector distributions: dc_sector FY2023 (n=163), size_matched FY2022 (n=334), national_women FY2022 (n=542), chosen for filing coverage."],
    ["Core peers are provisional.", "Line 1e understates government where contracts are booked as program revenue (possibly Samaritan Inns FY24–25)."],
    "High for shares, growth, liquidity and sector percentiles; medium for the typology of diversifiers.",
    { readout: "modules/m3_peer_benchmarking.md", config: "calvary_funding_data/config/core_peers.csv, config/universes.yaml", method: "metrics in scripts/03_m3_peers.py", chart: "m3_00, m3_05, m3_07, m3_08" });
  note("B2", "Method note B2: the funder base counts filed grants naming each organization, separates DAF sponsors and measures depth per revenue dollar.",
    "how deep is each organization's institutional funder base?", [
      "Funder base: 990-PF and Schedule I rows naming each organization, TY2020–24, non-cumulative.",
      "Split: institutional vs DAF via dim_funder.funder_type (Fidelity, Schwab, Benevity/AOGF, NPT, Vanguard and others are DAF sponsors).",
      "Measures: institutional-funder count, DAF share of filed grants, and depth = institutional dollars ÷ FY2020–24 revenue.",
      "Diversifier case studies use line-1e mix trajectories (m3_08)."],
    ["Only DMV funders' filings are present, so the LA comparators' local funders are not captured.", "TY2024 filings are partial."],
    "Medium for funder-base depth.",
    { readout: "modules/m3_peer_benchmarking.md", config: "calvary_funding_data/config/core_peers.csv", method: "depth = institutional $ ÷ revenue", chart: "m3_00, m3_06" });
  note("B3", "Method note B3: comparator profiles combine 990 trajectories, single-audit federal programs and web funder evidence, and each closes with what transfers to Calvary.",
    "what can Calvary learn from DWC and SheWorks?", [
      "Financials: trajectory, mix and months of cash from preferred 990 rows (line 1e for government).",
      "DWC federal programs: FAC single-audit SEFA FY2020–25.",
      "Funder evidence: DWC donor lists and gala pages (2023, 2025), funders' press releases and announced grants, and DMV funders' filings.",
      "SheWorks: program evidence from the parent's and partners' web pages.",
      "Both appear as Los Angeles reference rows on every peer table and chart."],
    ["DWC's fiscal year is the calendar year.", "Line 1e is the only government measure for both.", "LA-area funders are partly captured (no amounts on web lists).", "The CBWC Institute has three filings; SheWorks launched after the last one."],
    "High on DWC's trajectory and federal programs; medium on funder lists and the SheWorks parent.",
    { readout: "modules/m10_comparator_profiles.md", config: "calvary_funding_data/config/named_comparators.csv", method: "profiles built by scripts/10_m10_profiles.py", chart: "m10_01–m10_05" });
  note("C1", "Method note C1: the landscape uses two lenses on filed grants with two exclusions, and five gap categories test whether an absence is current.",
    "who funds Calvary's space, and which of those funders do not yet fund Calvary?", [
      "Base: filed grants TY2020–24, non-cumulative; exclusions: Gates Foundation (global and research recipients) and TCP (public pass-through).",
      "Lens A: grants to the 1,027 dc_sector organizations. Lens B: grants to DC/MD/VA recipients whose purpose is tagged housing, DV or women.",
      "DAF sponsors are reported separately from institutional funders.",
      "'Funds Calvary' = any filed grant naming Calvary TY2020–24; 'itemized TY2023+' = the funder filed itemized lists recently, so a missing Calvary grant is current.",
      "G1 peer funders (≥2 peers); G2 lapsed (last grant ≤TY2022); G3 headroom (larger grant to a peer); G4 DC-sector majors (≥$500K); G5 peer donor lists only; plus the CRM reconciliation."],
    ["'See attached' filers (667 rows, about $3.5B) have no recipient names.", "Corporate giving without a foundation is invisible in filings.", "A filing gap may be a DAF-routed gift or a corporate match."],
    "High on totals, concentration and filing-based gaps; medium on purpose tags and headroom.",
    { readout: "modules/m4_funder_landscape.md, modules/m5_funder_gaps.md", config: "config/landscape_exclusions.csv", method: "scripts/04_m4_landscape.py and 05_m5_gaps.py", chart: "m4_00–m4_08, m5_00–m5_06" });
  note("C2", "Method note C2: the network is a funder-by-recipient graph of filed grants, with rated interlocks and a 0–1 path score.",
    "which funders sit closest to Calvary's network, and are there board links to them?", [
      "Graph: bipartite, funders × 19 recipients (Calvary + 18 provisional peers); edges = filed grants TY2020–24 with exclusions; degree = organizations funded; betweenness on the unweighted graph.",
      "Overlap per peer: shared institutional funders (DAF sponsors excluded), Jaccard similarity, and the peer's institutional funders that do not fund Calvary.",
      "Interlocks: shared_board_member links touching Calvary, a peer or a comparator; person records linked only on an exact normalized name plus a corroborating signal; outputs store person_id only, never names.",
      "CP1 ruling: leadership materials use high-confidence links only; medium links are labeled unconfirmed.",
      "Path strength = 0.40 × peers funded (cap 12) + 0.25 × close peers (cap 8) + 0.25 × overlapping co-funders (cap 20) + 0.10 × any high-confidence board link; consulting variant +0.05 for a medium link."],
    ["Corporate and DAF-routed individual gifts are only partly visible.", "A medium-confidence match may be two different people."],
    "High on the graph and overlap counts; medium on the path-strength construct.",
    { readout: "modules/m6_network.md", config: "config/landscape_exclusions.csv (path weights documented in the m6_05 manifest note)", method: "scripts/06_m6_network.py", chart: "m6_01–m6_05" });
  note("C3", "Method note C3: the pipeline scores candidates on seven weights from one config file and adds analyst-scored government and corporate rows.",
    "which funders should Calvary pursue first?", [
      "Candidates: the M5 gap and current-funder base joined to M6 paths and the M4 landscape; DAF sponsors excluded; the T. Rowe Price Program scored like a DAF.",
      "Weights: mission fit 0.20, peer giving 0.20, regional giving 0.10, award size 0.15, accessibility 0.10, durability 0.10, relationship 0.15.",
      "Tiers: Tier 1 score ≥ 0.62 and median peer grant ≥ $25,000 (max 20); Tier 2 ≥ 0.48; Tier 3 the rest.",
      "Analyst-scored rows: five government rows (OVSJG 0.80, HUD CoC 0.78, DHS 0.72, DHS PSH 0.55, HUD CPF 0.45) and corporate CRM relationships ≥ $50K; Grants.gov notices default to Tier 3.",
      "Web pull: 32 Tier 1–2 funders searched, 128 hits, hand-reviewed into 27 guideline notes (13 first-party, 7 third-party, 7 analyst notes).",
      "Sensitivity: each weight ±0.05 (renormalized) and each tier cutoff ±0.05."],
    ["Scores rank evidence, not fit with funder guidelines.", "Government and corporate scores are judgment.", "In-kind channels are penalized, not removed."],
    "Medium: the ordering is robust to moderate weight changes; exact ranks are not.",
    { readout: "modules/m7_pipeline.md", config: "config/scoring_weights.yaml, config/guideline_notes.csv", method: "scripts/07_m7_pipeline.py, 12_merge_guidelines.py, 13_m7_sensitivity.py", chart: "m7_00–m7_05" });
  note("D1", "Method note D1: the expansion scan measures tagged DMV grant dollars, funders and federal notices per area and rates each area's distance.",
    "which adjacent program areas would open new funding pools, and how far are they from what Calvary runs today?", [
      "For each tag in dim_program_area: DMV institutional grant dollars TY2020–24 whose purpose text carries the tag (DAF sponsors and exclusions removed).",
      "Funders active, funders at $100K+, median grant, DC policy events, and peer and comparator examples.",
      "Federal Grants.gov notices after dropping research, tribal, rural and overseas notices and keeping HUD, VA, DOL, DOJ, ACF, SAMHSA, USDA, Treasury and ACL.",
      "Distance: core; near = already delivered in some form; medium = same clients, new capability or credential; far = new population or licensing.",
      "Ratings: housing core; DV, behavioral health, workforce and education near; physical health, aging, women veterans and reentry medium; maternal and family health far."],
    ["Tagged dollars understate what funders would give (general operating excluded).", "Distance ratings are judgment.", "Federal notices are a snapshot."],
    "Medium.",
    { readout: "modules/m8_expansion_scan.md", config: "config/expansion_areas.yaml", method: "scripts/08_m8_expansion.py", chart: "m8_01, m8_02" });
  note("D2", "Method note D2: universes are rule-built from IRS master files, and the 18 provisional peers change with one config edit.",
    "who is Calvary compared with, and how robust is that choice?", [
      "Universes are built from the IRS EO BMF and e-file index with rules in config/universes.yaml (sizes on the universes slide).",
      "Peer candidates: 36 named DC-area seeds plus a sweep of DC/DMV sector charities with revenue ≥ $750K and a shelter/DV NTEE code or a women-focused name.",
      "Score: women focus 3, DV 2, homeless/housing 2, recovery or mental health 1, Ward 7/8 2, DC 1, size similarity up to 2; homeless or DV language must appear in the filing text.",
      "The 18 peers have not been formally reviewed and are labeled provisional in every output; thirteen alternates are listed in the proposal.",
      "Swap: edit core_peers.csv, rerun 20_build_universes.py, then the analysis scripts from 03 onward.",
      "Peer-dependent outputs that move with the set: B1–B2 benchmarks, gap categories G1 and G3, the network and path strength, and pipeline peer-giving and relationship scores."],
    ["Benchmark years differ by universe (dc_sector FY2023; national universes FY2022) because filing coverage collapses afterwards."],
    "Provisional by design; sector percentiles are reported alongside peer ranks.",
    { readout: "modules/m3_peer_benchmarking.md; calvary_funding_data/reports/core_peers_proposal.md", config: "calvary_funding_data/config/core_peers.csv, config/universes.yaml", method: "rules and scores as documented in the proposal", chart: null });

  // D3: documents + limitations table
  s = X.head("Method note D3: the main limitations are known and bounded, and six documents from Calvary would close the largest of them.");
  D.card(s, { x: M, y: BODY_Y, w: 6.4, h: BODY_H - 0.15, title: "Documents requested from Calvary", fontSize: 10.5, lines: [
    "FY24 and FY25 audits, including any single audits: closes the audit-basis government share for FY24–25 and flag D1.",
    "TCP subgrant agreements FY2023–FY2026: closes the DHS/TCP stream (public for one year only) and flags D1 and D2.",
    "CRM export definitions: window, gift-date basis and the in-kind share of the largest corporate relationships (assumptions A1 and A2).",
    "Sisters Rise / EHV status in FY25: closes flag D2.",
    "FY25 gala timing: closes flag D3.",
    "SheWorks program-level budget and funders."] });
  D.card(s, { x: 7.3, y: BODY_Y, w: W - M - 7.3, h: BODY_H - 0.15, title: "Discovery flags (all approved as proposed at CP2)", fontSize: 10.5, lines: [
    "D1: recognized 67–73% of known award ceilings in FY24–FY25; medium confidence, labeled 'ceilings vs recognized'.",
    "D2: Sisters Rise absent from the 2025 HIC; DHS stream rated 'at risk', FY2024 value kept in the baseline.",
    "D3: event contributions $538K → $55K while net event income turned positive; reported as the largest single swing.",
    "The full limitation list (29 items, each with its mitigation) follows."] });
  D.footnote(s, { source: `${METH} §5 D3 and §9; discoveries_log.md; modules/*.md (Caveats)`, method: "limitations consolidated from the module readouts and the data-build reports; duplicates merged", chart: null, note: "D3" });
  const lim = mdTable(meth, /^## 9\. Limitations/);
  X.table("Method note D3: each of the 29 limitations carries the mitigation used in the analysis.",
    ["#", "Limitation", "Mitigation used"], lim.rows.map(r => [r[0], trunc(r[1], 140), trunc(r[2], 140)]),
    [0.4, 5.9, 5.83],
    { source: `${METH} §9; modules/*.md (Caveats); calvary_funding_data/reports/data_quality.md`, method: "one row per limitation; mitigations are the steps actually taken", chart: null, note: "D3" },
    { rowsPerSlide: 10, fontSize: 8.5 });

  // 22. Insight register
  X.section("Registers and reruns");
  const ir = C.readAny("calvary_analysis/insight_register.csv");
  const statuses = [...new Set(ir.map(r => r.status))];
  X.table(`The insight register lists all ${ir.length} findings with confidence and verification status, and ${statuses.length === 1 ? `all are ${statuses[0]}` : "statuses vary"} pending the independent review.`,
    ["ID", "Finding", "Confidence", "Audience", "Status", "Charts"],
    ir.map(r => [r.insight_id, trunc(r.finding, 112), r.confidence, r.audience, r.status, trunc(r.chart_ids.replace(/;/g, ", "), 42)]),
    [0.7, 7.3, 0.85, 0.85, 0.6, 1.83],
    { source: "calvary_analysis/insight_register.csv (written by each module script)", method: "one row per finding with evidence summary, chart IDs, source tables, magnitude, confidence and implication (full text in the CSV)", chart: null, note: "D3" },
    { rowsPerSlide: 12, fontSize: 8.5 });

  // 23. Discoveries log
  const dl = mdTable(C.readText("calvary_analysis/discoveries_log.md"), /^# Discoveries log/);
  s = X.head(`The discoveries log records every flag and its resolution: ${["no", "one", "two", "three", "four", "five"][dl.rows.length] || dl.rows.length} flags, ${dl.rows.every(r => /approved/.test(r[6])) ? "all approved as proposed at CP2" : "see the response column"}.`);
  tbl(s, ["#", "Finding", "Why it matters", "Proposed action", "Response"], dl.rows.map(r => [r[0], trunc(r[2], 260), trunc(r[4], 260), trunc(r[5], 230), r[6]]),
    { x: M, y: BODY_Y, w: FULL_W, colW: [0.45, 3.5, 3.5, 3.0, 1.68], fontSize: 10 });
  D.footnote(s, { source: "calvary_analysis/discoveries_log.md (evidence column cites chart_data/m2_02, supp_hic_projects, fact_org_financials)", method: "one entry per flag: date, finding, evidence, why it matters, proposed action, response", chart: "m2_02, m2_03, m1_06", note: "D3" });

  // 24. How to rerun
  const so = mdTable(meth, /^## 7\. Reproducibility/);
  const H24 = "How to rerun: scripts, requirements, config files and the trace test reproduce every figure from the clean tables.";
  X.table(H24, ["Script", "Does", "Reads config"], so.rows.map(r => [r[0], r[1], r[2]]), [3.4, 6.2, 2.53],
    { source: `${METH} §6–§7; calvary_analysis/requirements.txt; scripts/lib/trace.py`, method: "run 00, then 01–10, 12, 13 and lib/trace.py with calvary_funding_data/.venv/bin/python; skip 11 (network pull) on a rerun", chart: null, note: "D3" },
    { rowsPerSlide: 15, fontSize: 9.5 });
  s = X.head(`${H24} (what to edit)`);
  const ed = mdTable(meth.split("**What to edit for each change:**")[1] ? "x\n" + meth.split("**What to edit for each change:**")[1] : meth, /^x$/);
  tbl(s, ["To change", "Edit", "Then rerun"], ed.rows, { x: M, y: BODY_Y, w: FULL_W, colW: [2.6, 4.6, 4.93], fontSize: 10 });
  D.card(s, { x: M, y: 4.2, w: FULL_W, h: 2.2, title: "Environment and trace test", fontSize: 10.5, lines: [
    "Python 3.12 in calvary_funding_data/.venv; analysis packages pinned in calvary_analysis/requirements.txt (pandas, matplotlib, networkx, python-pptx, pyyaml, shapely, markitdown, tavily-python).",
    "Scripts read only calvary_funding_data/clean/ (and raw/geo for the ward map) and resolve paths from their own location.",
    "scripts/lib/trace.py checks chart ID → chart_data CSV → clean table → source registry and prints TRACE OK or the problems."] });
  D.footnote(s, { source: `${METH} §7; calvary_funding_data/README.md (Rebuild)`, method: "each script appends to analysis_log.md and rewrites its chart data, manifest rows and insight rows", chart: null, note: "D3" });

  await D.finish(X.pres, path.join(__dirname, "appendix_D_data_methods.pptx"));
})();
