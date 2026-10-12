// Appendix B: Peers and named comparators. Follows storylines/appendix_headline_spine.md (Appendix B, items 1-12).
const path = require("path");
const C = require("./build_appendix_common");
const { D, HEX, M, W, BODY_Y, BODY_H, FULL_W, tc, trunc, num, usd, money, pct, n0, yr, tbl } = C;

const SRC990 = "IRS Form 990 e-file returns (GivingTuesday, NCCS, IRS SOI, ProPublica); Calvary audits FY13–FY23; fact_org_financials";
const SRCGR = "Funders' 990-PF grants paid and Schedule I rows (IRS e-file via GivingTuesday); fact_grants, dim_funder";
const ref = (o) => o.replace("DWC (Los Angeles)", "DWC (LA, reference)").replace("CBWC Inst. / SheWorks (LA)", "CBWC Inst. / SheWorks (LA, reference)");
const TIER = { "1a_dc_women_homeless": "1a · DC women's homelessness", "1b_dc_dv": "1b · DC DV survivors", "2_dc_homeless_recovery": "2 · DC homelessness and recovery", "2_dc_ward78": "2 · Ward 7/8 presence", "3_dmv_women_dv": "3 · DMV women/DV outside DC", subject: "subject", named_comparator: "named comparator (LA)" };

(async () => {
  const X = C.makeDeck("Appendix B: Peers and named comparators", "Appendix B of the Calvary funding analysis");
  const pres = X.pres;

  // 1. Title
  X.section("Appendix B");
  X.title("Appendix B: Peers and Comparators",
    "Appendix B · Peers and named comparators · pro bono funding analysis for Calvary Women's Services. Core peers are provisional; DWC and the CBWC Empowerment Institute (SheWorks) are Los Angeles reference rows. Method notes B1–B3 and D2 are in Appendix D.");

  // 2. Core peers
  X.section("Peer set and benchmark");
  const cp = C.readAny("calvary_funding_data/config/core_peers.csv");
  X.table("The 18 provisional core peers were chosen for model similarity in four tiers and can be swapped by editing one file.",
    ["Organization", "Tier", "Status", "Rationale"],
    cp.map(r => [r.name, TIER[r.tier] || r.tier, r.status, trunc(r.rationale, 130)]),
    [2.9, 2.5, 1.0, 5.73],
    { source: "IRS EO BMF and e-file index; calvary_funding_data/config/core_peers.csv; calvary_funding_data/reports/core_peers_proposal.md", method: "score (women focus, DV, homelessness, recovery, Ward 7/8, DC, size) plus a relevance gate and judgment; swap = edit core_peers.csv and rerun", chart: null, note: "D2" },
    { rowsPerSlide: 9, fontSize: 10 });

  // 3. Benchmark table, two slides
  const bt = D.readCsv("m3_00_benchmark_table");
  const btFoot = { source: `${SRC990}; ${SRCGR}`, method: "government share = line 1e ÷ revenue (Calvary audit basis FY≤2023); FY2022–24 means; real CAGR in 2024 dollars; core peers provisional", chart: "m3_00", note: "B1, B2" };
  const RT = (t) => t.startsWith("government") ? "gov.-anchored" : t.startsWith("philanthropy") ? "philanthropy-led" : "mixed";
  X.table(`The benchmark table gives every metric for all ${bt.length} organizations: size, government share, growth and liquidity.`,
    ["Organization", "Tier", "Revenue FY2024", "Gov. share FY22–24", "Gov. share latest", "Real CAGR FY19–24", "Months of cash FY24", "Months of cash FY22–24", "Program service share", "Fundraising cost per private $", "Resilience type"],
    bt.map(r => [ref(r.org), (TIER[r.tier] || r.tier).split(" · ")[0], money(r.revenue_fy2024, 1), pct(num(r.gov_share_fy2022_24_mean)), pct(num(r.gov_share_latest)), pct(num(r.real_cagr_fy2019_24), 1), num(r.months_of_cash_fy2024) == null ? "—" : num(r.months_of_cash_fy2024).toFixed(1), num(r.months_of_cash_fy2022_24_mean) == null ? "—" : num(r.months_of_cash_fy2022_24_mean).toFixed(1), pct(num(r.program_service_share_fy2022_24)), num(r.fundraising_cost_per_private_dollar_fy2022_24) == null ? "—" : `$${num(r.fundraising_cost_per_private_dollar_fy2022_24).toFixed(2)}`, RT(r.resilience_type)]),
    [2.85, 1.35, 0.9, 0.85, 0.8, 0.85, 0.8, 0.85, 0.85, 0.95, 1.08], btFoot, { rowsPerSlide: 11, fontSize: 9.5 });
  X.table(`The benchmark table gives every metric for all ${bt.length} organizations: the institutional funder base and DAF share.`,
    ["Organization", "Filed grants TY2020–24", "Funders", "Institutional funders", "Institutional $", "DAF $", "DAF share of filed", "Institutional $ ÷ revenue", "Note"],
    bt.map(r => [ref(r.org), money(r.filed_grants_ty2020_24), n0(r.funders), n0(r.institutional_funders), money(r.institutional_amount), money(r.daf_amount), pct(num(r.daf_share_of_filed)), pct(num(r.institutional_per_revenue_dollar), 1), trunc(r.note, 70)]),
    [2.95, 1.1, 0.75, 0.95, 1.05, 0.9, 0.9, 1.0, 2.53],
    { source: SRCGR, method: "TY2020–24, non-cumulative; institutional vs DAF via dim_funder.funder_type; depth = institutional $ ÷ FY2020–24 revenue; DMV funders' filings only", chart: "m3_00", note: "B2" },
    { rowsPerSlide: 11, fontSize: 9.5 });

  // 4. Trajectories: PNG + table
  X.section("Trajectories and distributions");
  X.png("Most organizations' government share has been stable since FY2017, except Samaritan Inns (down) and DWC and House of Ruth MD (up).", "m3_05_gov_share_trajectories", null, null,
    { source: SRC990, method: "line 1e ÷ total revenue, Calvary on the audit basis FY17–FY23; one organization per panel", chart: "m3_05", note: "B1" });
  const tr = D.readCsv("m3_05_gov_share_trajectories");
  const orgs = [...new Set(tr.map(r => r.org))].sort((a, b) => (a === "Calvary" ? -1 : b === "Calvary" ? 1 : /LA\)/.test(a) - /LA\)/.test(b) || a.localeCompare(b)));
  const tys = [...new Set(tr.map(r => yr(r.fiscal_year)))].sort();
  X.table("Government-share trajectories for all 21 organizations, FY2017–FY2025, show Calvary between 40% and 61% every year.",
    ["Organization", ...tys.map(y => `FY${y.slice(2)}`)],
    orgs.map(o => [ref(o), ...tys.map(y => { const r = tr.find(x => x.org === o && yr(x.fiscal_year) === y); return r ? pct(num(r.gov_share)) : "—"; })]),
    [3.13, ...tys.map(() => 1.0)],
    { source: SRC990, method: "line 1e ÷ total revenue on preferred rows; Calvary FY17–FY23 audit basis; '—' = no filing in the data", chart: "m3_05", note: "B1" },
    { rowsPerSlide: 11, fontSize: 10 });

  // 5. Sector distributions: PNG + table
  const sdist = D.readCsv("m3_07_sector_distributions");
  s = X.head("Among organizations that report government revenue Calvary sits at the 57th percentile in DC and the 46th nationally, and in the top quarter of all filers.");
  C.img(s, "m3_07_sector_distributions", { x: M, y: BODY_Y, w: 7.4, h: 3.4 });
  D.card(s, { x: 8.3, y: BODY_Y, w: W - M - 8.3, h: 3.25, title: "Reading the distributions", fontSize: 11, lines: [
    "Percentiles compare Calvary with organizations that report government revenue; against all filers (no line counted as 0%) it is 84th in DC and 74th in both national universes.",
    "Benchmark years chosen for filing coverage: national universes fall below 15 filers after FY2022.",
    "Calvary's FY2023 share here is line-1e based (51%)."] });
  tbl(s, ["Universe", "Year", "n reporting", "p25", "Median", "p75", "Calvary", "Percentile (reporters)", "n all filers", "Percentile (all filers)", "Median revenue"],
    sdist.map(r => [r.label.replace(/, FY\d+/, ""), `FY${yr(r.fiscal_year)}`, n0(r.n), pct(num(r.p25)), pct(num(r.median)), pct(num(r.p75)), pct(num(r.calvary_gov_share)), `${Math.round(num(r.calvary_percentile) * 100)}th`, n0(r.n_all_filers), `${Math.round(num(r.calvary_percentile_all_filers) * 100)}th`, money(r.median_revenue)]),
    { x: M, y: 5.3, w: FULL_W, colW: [2.9, 0.7, 0.9, 0.75, 0.8, 0.75, 0.85, 1.3, 0.9, 1.3, 1.18], fontSize: 9.5, align: ["left", "left", "right", "right", "right", "right", "right", "right", "right", "right", "right"] });
  D.footnote(s, { source: `${SRC990}; dim_universe_membership`, method: "990 line 1e basis; percentile among organizations reporting government revenue, all-filers percentile counts no line as 0%; universe rules in config/universes.yaml (dc_sector FY2023, size_matched and national_women FY2022)", chart: "m3_07", note: "B1" });

  // 6. Case studies: PNG + table
  X.png("The case studies show three paths: Samaritan Inns replaced government, N Street Village grew private giving alongside it, and DWC scaled with it.", "m3_08_case_studies_mix", null, null,
    { source: SRC990, method: "revenue mix by year from preferred 990 rows; government = line 1e", chart: "m3_08", note: "B1" });
  const cs = D.readCsv("m3_08_case_studies_mix");
  X.table("The four case studies' revenue mix by year: Miriam's Kitchen grew on almost no government money and Samaritan Inns shifted to program revenue.",
    ["Organization", "Fiscal year", "Total revenue", "Government", "Private contributions", "Program service", "Other", "Government share"],
    cs.map(r => [ref(r.short), `FY${yr(r.fiscal_year)}`, usd(r.total_revenue), usd(r.government), usd(r.private_contributions), usd(r.program_service), usd(r.other), pct(num(r.gov_share))]),
    [2.6, 1.0, 1.55, 1.45, 1.6, 1.45, 1.2, 1.28],
    { source: SRC990, method: "government = line 1e (may understate where contracts are booked as program revenue, e.g. Samaritan Inns FY24–25)", chart: "m3_08", note: "B1" },
    { rowsPerSlide: 16, fontSize: 9 });

  // 7. Peer pools
  const pools = D.readCsv("m3_09_peer_pools").sort((a, b) => num(b.ovsjg_fy2026) - num(a.ovsjg_fy2026) || a.org.localeCompare(b.org));
  s = X.head("OVSJG and CoC awards to peers show the DV peers drawing $3.2–5.3M each from OVSJG while Calvary is one of the larger CoC sub-recipients.");
  const pr = pools.slice().reverse();
  D.chart(s, "bar", pr.map(r => r.org), [
    { name: "OVSJG awards DC FY2026", values: pr.map(r => num(r.ovsjg_fy2026)), color: HEX.government },
    { name: "HUD CoC awards FY2025", values: pr.map(r => num(r.hud_coc_fy2025)), color: HEX.daf }],
    { x: M, y: BODY_Y, w: 5.6, h: BODY_H, barDir: "bar", catFontSize: 8.5 });
  tbl(s, ["Organization", "OVSJG DC FY2026", "HUD CoC FY2025", "Revenue FY2024", "OVSJG ÷ revenue", "CoC ÷ revenue"],
    pools.map(r => [r.org, usd(r.ovsjg_fy2026), usd(r.hud_coc_fy2025), money(r.revenue_fy2024, 1), pct(num(r.ovsjg_share_of_revenue)), pct(num(r.coc_share_of_revenue))]),
    { x: 6.4, y: BODY_Y, w: 6.33, colW: [1.75, 1.05, 1.05, 0.9, 0.8, 0.78], fontSize: 9, align: ["left", "right", "right", "right", "right", "right"] });
  s.addText("DC pools only: peers with no OVSJG or CoC award are omitted, and the LA comparators have no rows by construction.",
    { x: 6.4, y: 5.0, w: 6.33, h: 0.6, fontSize: 9.5, color: HEX.text2, margin: 0, isTextBox: true, valign: "top" });
  D.footnote(s, { source: "DC OVSJG FY2026 award list; HUD CoC FY2025 awards (DC-500); fact_gov_awards, fact_org_financials", method: "award amounts as listed; shares = award ÷ FY2024 revenue (award and revenue years differ)", chart: "m3_09", note: "A2" });

  // 8. Co-funding overlap
  const ov = D.readCsv("m6_02_cofunding_overlap");
  X.table("Co-funding overlap between Calvary and each peer is highest with Miriam's Kitchen (17 shared institutional funders), DASH and House of Ruth DC (14 each).",
    ["Peer", "Shared funders", "Shared institutional", "Peer's funders", "Peer's institutional", "Jaccard (all)", "Jaccard (institutional)", "Calvary funders also funding peer", "Peer institutional funders not funding Calvary"],
    ov.map(r => [r.org, r.shared_funders, r.shared_institutional_funders, r.peer_funders, r.peer_institutional_funders, num(r.jaccard_all).toFixed(2), num(r.jaccard_institutional).toFixed(2), pct(num(r.share_of_calvary_funders_also_funding_peer)), r.peer_institutional_funders_not_calvary]),
    [2.53, 1.0, 1.1, 1.0, 1.1, 1.0, 1.1, 1.6, 1.7],
    { source: SRCGR, method: "funder sets from filed grants TY2020–24; institutional excludes DAF sponsors; LA comparators omitted (DMV funders' filings only)", chart: "m6_02", note: "C2" },
    { rowsPerSlide: 18, fontSize: 9.5 });

  // 9. DWC trajectory
  X.section("Named comparators");
  const ct = D.readCsv("m10_01_comparator_trajectories");
  const dwc = ct.filter(r => r.ein === "311597223").sort((a, b) => num(a.fiscal_year) - num(b.fiscal_year));
  const f = dwc[0], l = dwc[dwc.length - 1];
  X.png(`DWC's revenue rose from ${money(f.total_revenue, 1)} to ${money(l.total_revenue, 1)} between FY2014 and FY2024 as its government share rose from ${pct(num(f.gov_share))} to ${pct(num(l.gov_share))}.`,
    "m10_01_comparator_trajectories", "DWC (LA, reference)", [
      "Private contributions tripled ($4.0M → $12.8M) but fell from 64% to 37% of revenue.",
      "Program service revenue (social enterprise, rental) about 5%.",
      "Months of cash 1.8–4.4 throughout (2.4 in FY2024).",
      "Fiscal year = calendar year; government = 990 line 1e."],
    { source: "IRS 990 e-file returns (GivingTuesday, ProPublica, IRS SOI); fact_org_financials", method: "government = Part VIII line 1e; labels show government share; DWC FY = calendar year, CBWC FYE June", chart: "m10_01", note: "B3" }, { wide: 0.6 });
  X.table("DWC's filings show revenue up 5.5 times in a decade on 1.8–4.4 months of cash, which is the scale-with-government path.",
    ["Fiscal year", "Total revenue", "Government", "Private contributions", "Program service", "Other", "Government share", "Total expenses", "Net assets", "Months of cash"],
    dwc.map(r => [`FY${yr(r.fiscal_year)}`, usd(r.total_revenue), usd(r.government), usd(r.private_contributions), usd(r.program_service), usd(r.other), pct(num(r.gov_share)), usd(r.total_expenses), usd(r.net_assets_eoy), num(r.months_of_cash).toFixed(1)]),
    [0.9, 1.35, 1.3, 1.35, 1.2, 1.0, 1.05, 1.35, 1.38, 1.25],
    { source: "IRS 990 e-file returns (GivingTuesday, ProPublica, IRS SOI); fact_org_financials", method: "preferred 990 rows; government = line 1e; fiscal year ends December", chart: "m10_01", note: "B3" },
    { rowsPerSlide: 11, fontSize: 10 });

  // 10. DWC federal programs
  const fp = D.readCsv("m10_02_dwc_federal_programs").sort((a, b) => num(b.amount) - num(a.amount));
  const fpTot = fp.reduce((a, r) => a + num(r.amount), 0), fpPT = fp.filter(r => num(r.pass_through) === 1 || r.pass_through === "True").reduce((a, r) => a + num(r.amount), 0);
  s = X.head(`DWC's federal programs by assistance listing, FY2020–25, total ${money(fpTot, 1)}, ${Math.floor(fpPT / fpTot * 100)}% passed through, led by HUD CoC at ${money(fp[0].amount, 1)}.`);
  C.img(s, "m10_02_dwc_federal_programs", { x: M, y: BODY_Y, w: 5.9, h: 3.4 });
  const fpRows = fp.map(r => [r.assistance_listing, trunc(tc(r.program_name), 48), usd(r.amount), r.years, num(r.pass_through) === 1 || r.pass_through === "True" ? "yes" : "no"]);
  const fpT = ["", "Total", usd(fpTot), "", ""]; fpT._bold = true; fpRows.push(fpT);
  tbl(s, ["Listing", "Program", "Expenditures FY2020–25", "Years", "Pass-through"], fpRows,
    { x: 6.75, y: BODY_Y, w: 5.98, colW: [0.7, 2.55, 1.2, 0.6, 0.93], fontSize: 9, align: ["left", "left", "right", "right", "left"] });
  s.addText("These are the federal channels Calvary uses (CoC, ESG, VOCA, SNAP E&T, EFSP, Community Project Funding), at about five times the scale, routed through LA County and LAHSA rather than TCP.",
    { x: M, y: 5.35, w: 5.9, h: 1.0, fontSize: 10, color: HEX.text2, margin: 0, isTextBox: true, valign: "top" });
  D.footnote(s, { source: "Federal Audit Clearinghouse single-audit SEFA for DWC, FY2020–25; fact_gov_awards (source_type fac)", method: "expenditures summed by assistance listing across audit years; pass-through flag as reported", chart: "m10_02", note: "B3" });

  // 11. DWC funder evidence
  const fs3 = D.readCsv("m10_03_comparator_funder_sources");
  const fs4 = D.readCsv("m10_04_dwc_dmv_funders").sort((a, b) => num(b.amount) - num(a.amount));
  const fs5 = D.readCsv("m10_05_dwc_named_grants").sort((a, b) => num(b.amount) - num(a.amount) || a.funder_name_raw.localeCompare(b.funder_name_raw));
  const dmvTot = fs4.reduce((a, r) => a + num(r.amount), 0);
  const ar = fs3.find(r => r.recipient_ein === "311597223" && r.source_type === "annual_report");
  s = X.head(`DWC's donor lists carry ${n0(ar.funders)} names, but DMV funders' filings show only ${money(dmvTot, 1)} of grants to it.`);
  const who = (e) => e === "311597223" ? "DWC" : "CBWC Inst. / SheWorks";
  tbl(s, ["Recipient", "Source type", "Rows", "Funders", "Amount known"], fs3.map(r => [who(r.recipient_ein), r.source_type.replace(/_/g, " "), r.rows, r.funders, num(r.amount_known) ? usd(r.amount_known) : "bands only"]),
    { x: M, y: BODY_Y, w: 5.9, colW: [1.7, 1.4, 0.7, 0.8, 1.3], fontSize: 9, align: ["left", "left", "right", "right", "right"] });
  tbl(s, ["DMV funder (filed grants TY2020–25)", "Amount", "Years"], fs4.map(r => [trunc(tc(r.funder_name_raw), 48), usd(r.amount), r.years]),
    { x: M, y: 3.85, w: 5.9, colW: [3.9, 1.2, 0.8], fontSize: 9, align: ["left", "right", "right"] });
  tbl(s, ["Announced grant (web source)", "Year", "Amount"], fs5.map(r => [trunc(tc(r.funder_name_raw), 55), yr(r.fiscal_year), usd(r.amount)]),
    { x: 6.83, y: BODY_Y, w: 5.9, colW: [3.9, 0.8, 1.2], fontSize: 9, align: ["left", "left", "right"] });
  s.addText("Annual-report and gala lists carry giving bands, not amounts. DAF grants to LA organizations are not captured, because Schedule I rows were kept for DC/MD/VA recipients only.",
    { x: 6.83, y: 4.35, w: 5.9, h: 1.0, fontSize: 10, color: HEX.text2, margin: 0, isTextBox: true, valign: "top" });
  D.footnote(s, { source: "DWC annual reports and donor lists, gala pages, funder announcements; DMV funders' 990-PF / Schedule I; fact_grants", method: "web rows carry amounts only where a funder announced one; DMV filings aggregated by funder name as filed", chart: "m10_03, m10_04, m10_05", note: "B3" });

  // 12. CBWC / SheWorks
  const cb = ct.filter(r => r.ein === "882046704").sort((a, b) => num(a.fiscal_year) - num(b.fiscal_year));
  s = X.head(`The CBWC Empowerment Institute's three filings show government falling from ${pct(num(cb[0].gov_share))} to ${pct(num(cb[cb.length - 1].gov_share))} of revenue, and SheWorks itself starts after the last one.`);
  tbl(s, ["Fiscal year (FYE June)", "Total revenue", "Government", "Private contributions", "Program service", "Government share", "Total expenses", "Net assets", "Months of cash"],
    cb.map(r => [`FY${yr(r.fiscal_year)}`, usd(r.total_revenue), usd(r.government), usd(r.private_contributions), usd(r.program_service), pct(num(r.gov_share)), usd(r.total_expenses), usd(r.net_assets_eoy), num(r.months_of_cash).toFixed(1)]),
    { x: M, y: BODY_Y, w: FULL_W, colW: [1.6, 1.4, 1.4, 1.5, 1.3, 1.2, 1.4, 1.3, 1.03], fontSize: 10.5, align: ["left", "right", "right", "right", "right", "right", "right", "right", "right"] });
  D.card(s, { x: M, y: 3.25, w: 5.9, h: 3.25, title: "What is known about SheWorks", fontSize: 11, lines: [
    "A workforce program of the institute (Carson, CA; founded 2022), not a separate entity.",
    "Announced October 2025; first cohort of about 30 women, January–May 2026, at the L.A. Care / Blue Shield Promise Community Resource Center in Long Beach.",
    "Stipends, childcare and ride credits; the LA County Federation of Labor is a partial funder and the health plans host in kind.",
    "No FAC or USAspending awards; its funding appears only in TY2025+ filings."] });
  D.card(s, { x: 6.83, y: 3.25, w: 5.9, h: 3.25, title: "What transfers to Calvary", fontSize: 11, lines: [
    "Program design: cohort model, stipends, childcare and transport, employer and health-plan partners, system-impacted women as a named population (an upgrade path for Step Up DC).",
    "Partner structure: labor federation plus health plans as a corporate-partnership pattern.",
    "Not a funding model to copy: the parent is more government-reliant than Calvary."] });
  D.footnote(s, { source: "IRS 990 e-file returns (fact_org_financials); institute, partner and press web pages (fact_grants web rows); modules/m10_comparator_profiles.md", method: "government = line 1e; months of cash as filed; program facts as published by the institute and partners", chart: "m10_01", note: "B3" });

  await D.finish(pres, path.join(__dirname, "appendix_B_peers_comparators.pptx"));
})();
