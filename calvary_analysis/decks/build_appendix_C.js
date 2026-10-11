// Appendix C: Funders, gaps, network and pipeline. Follows storylines/appendix_headline_spine.md (Appendix C, items 1-21).
const path = require("path");
const C = require("./build_appendix_common");
const { D, HEX, M, W, BODY_Y, BODY_H, FULL_W, tc, trunc, num, usd, money, pct, n0, yn, ty, yr, tbl } = C;

const SRCLAND = "Funders' 990-PF grants paid and Schedule I rows TY2020–24 (IRS e-file via GivingTuesday); fact_grants, dim_funder, dim_universe_membership";
const SRCGR = "Funders' 990-PF grants paid and Schedule I rows TY2020–24 (IRS e-file via GivingTuesday); fact_grants, dim_funder";
const ft = (t) => String(t || "").replace(/_/g, " ");
const WORDS = ["Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen", "Twenty"];
const TENS = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"];
const word = (n) => n < 21 ? WORDS[n] : n < 100 ? TENS[Math.floor(n / 10)] + (n % 10 ? "-" + WORDS[n % 10].toLowerCase() : "") : String(n);
const noEmail = (s) => String(s || "").replace(/;?\s*email [^\s]+@[^\s]+ before \w+/gi, "").replace(/[^\s()]+@[^\s()]+/g, "").replace(/\s+\)/g, ")");
const nm = (s) => trunc(tc(s), 52);

(async () => {
  const X = C.makeDeck("Appendix C: Funders, gaps, network and pipeline", "Appendix C of the Calvary funding analysis");
  const pres = X.pres;

  // 1. Title
  X.section("Appendix C");
  X.title("Appendix C: Funder Pipelines",
    "Appendix C · Funders, gaps, network and pipeline · pro bono funding analysis for Calvary Women's Services. Core peers are provisional. Method notes C1–C3 and D1 are in Appendix D.");

  // 2. DC sector by year and funder type
  X.section("Landscape");
  const by = D.readCsv("m4_01_dc_sector_by_year").sort((a, b) => num(a.tax_year) - num(b.tax_year));
  const bt = D.readCsv("m4_02_dc_sector_by_funder_type").sort((a, b) => num(b.amount) - num(a.amount));
  const tot = bt.reduce((a, r) => a + num(r.amount), 0);
  const dafShare = num(bt.find(r => r.funder_type === "daf_sponsor").amount) / tot;
  let s = X.head(`Grants to the DC sector by year and funder type total ${money(tot, 0)} over TY2020–24, ${pct(dafShare)} of it through DAF sponsors.`);
  D.chart(s, "bar", by.map(r => ty(r.tax_year)), [
    { name: "Institutional and other funders", values: by.map(r => num(r.institutional_and_other)), color: HEX.institutional },
    { name: "DAF sponsors", values: by.map(r => num(r.daf_sponsors)), color: HEX.daf }], { x: M, y: BODY_Y, w: 5.4, h: BODY_H, stacked: true });
  tbl(s, ["Funder type", "TY2020–24 amount", "Funders", "Grants", "Median grant", "Share"],
    bt.map(r => [ft(r.funder_type), money(r.amount, 1), n0(r.funders), n0(r.grants), usd(r.median_grant), pct(num(r.share), 1)]),
    { x: 6.3, y: BODY_Y, w: 6.43, colW: [2.0, 1.25, 0.75, 0.75, 0.95, 0.73], fontSize: 10, align: ["left", "right", "right", "right", "right", "right"] });
  tbl(s, ["Tax year", "Funders", "Recipients"], by.map(r => [ty(r.tax_year), n0(r.funders), n0(r.recipients)]),
    { x: 6.3, y: 4.6, w: 3.6, colW: [1.2, 1.2, 1.2], fontSize: 10, align: ["left", "right", "right"] });
  D.footnote(s, { source: SRCLAND, method: "grants to the 1,027 dc_sector organizations, non-cumulative, landscape exclusions applied (Gates, TCP); funder tax years, TY2024 partial", chart: "m4_01, m4_02", note: "C1" });

  // 3. Top 50 landscape table
  const lt = D.readCsv("m4_00_funder_landscape_table").sort((a, b) => num(a.rank) - num(b.rank)).slice(0, 50);
  const ltCal = lt.filter(r => r.gives_to_calvary === "True").length;
  X.table(`The 50 largest institutional funders of DC's sector, with Calvary status and peers funded, include ${ltCal} that already fund Calvary.`,
    ["Rank", "Funder", "Type", "State", "DC-sector $ TY2020–24", "DC recipients", "Median grant", "Max grant", "To Calvary", "Peers funded", "See-attached years"],
    lt.map(r => [r.rank, nm(r.funder_name), ft(r.funder_type), r.state, money(r.dc_sector_amount), r.dc_sector_recipients, usd(r.median_grant), money(r.max_grant), num(r.calvary_amount) ? money(r.calvary_amount) : "—", r.peers_funded, r.placeholder_years]),
    [0.5, 3.4, 1.65, 0.5, 1.15, 0.8, 0.9, 0.85, 0.85, 0.7, 0.83],
    { source: SRCLAND, method: "institutional = not a DAF sponsor; ranked by DC-sector dollars; see-attached years = returns with unnamed grant lists", chart: "m4_00", note: "C1" },
    { rowsPerSlide: 14, fontSize: 9 });

  // 4. Grant sizes
  const gsz = D.readCsv("m4_05_grant_size_by_type").sort((a, b) => num(a["50%"]) - num(b["50%"]));
  const g = (t) => gsz.find(r => r.funder_type === t);
  s = X.head(`Grant-size distributions by funder type put the median grant at ${money(g("private_foundation")["50%"])} for private foundations and ${money(g("community_foundation")["50%"])} for community foundations.`);
  C.img(s, "m4_05_grant_size_by_type", { x: M, y: BODY_Y, w: 6.5, h: 3.2 });
  tbl(s, ["Funder type", "Grants", "p25", "Median", "p75", "p90", "Mean"],
    gsz.map(r => [ft(r.funder_type), n0(r.count), usd(r["25%"]), usd(r["50%"]), usd(r["75%"]), usd(r["90%"]), usd(r.mean)]),
    { x: 7.35, y: BODY_Y, w: 5.38, colW: [1.5, 0.6, 0.6, 0.65, 0.65, 0.7, 0.68], fontSize: 9, align: ["left", "right", "right", "right", "right", "right", "right"] });
  s.addText("The 90th percentile runs from $79K (private foundations) to $259K (DAF sponsors). Corporate-foundation medians are small because matching gifts dominate their counts.",
    { x: 7.35, y: 4.0, w: 5.38, h: 1.0, fontSize: 10.5, color: HEX.text2, margin: 0, isTextBox: true, valign: "top" });
  D.footnote(s, { source: SRCLAND, method: "percentiles of individual grant amounts to dc_sector recipients, TY2020–24, by dim_funder.funder_type", chart: "m4_05", note: "C1" });

  // 5. DAF sponsors
  const daf = D.readCsv("m4_06_daf_sponsors").sort((a, b) => num(b.total) - num(a.total));
  const ycols = ["2020.0", "2021.0", "2022.0", "2023.0", "2024.0"];
  X.table(`DAF sponsors' grants to the DC sector by year are led by Fidelity Charitable at ${money(daf[0].total, 0)} over TY2020–24.`,
    ["DAF sponsor", ...ycols.map(c => `TY${c.slice(0, 4)}`), "Total TY2020–24"],
    daf.map(r => [nm(r.funder_name), ...ycols.map(c => money(r[c], 1)), money(r.total, 1)]),
    [3.9, 1.3, 1.3, 1.3, 1.3, 1.3, 1.63],
    { source: "DAF sponsors' Schedule I rows (IRS e-file via GivingTuesday), kept for DC/MD/VA recipients; fact_grants, dim_funder", method: "grants to dc_sector recipients by sponsor and tax year; DAF money is individual donors' decisions routed through sponsors", chart: "m4_06", note: "C1" },
    { rowsPerSlide: 8, fontSize: 11 });

  // 6. Purpose tags and mission-tagged funders
  const tags = D.readCsv("m4_07_purpose_tags").sort((a, b) => num(b.amount) - num(a.amount));
  const mt = D.readCsv("m4_08_mission_tagged_funders").sort((a, b) => num(b.amount) - num(a.amount) || a.funder_name.localeCompare(b.funder_name)).slice(0, 13);
  s = X.head("Purpose tags and mission-tagged funders show most institutional dollars untagged or general operating, and several of the largest mission-tagged funders giving little in DC.");
  tbl(s, ["Purpose tag", "Institutional $", "Grants", "Funders", "Share of tagged $"],
    tags.map(r => [ft(r.tag), money(r.amount, 1), n0(r.grants), n0(r.funders), pct(num(r.share_of_tagged_dollars), 1)]),
    { x: M, y: BODY_Y, w: 5.2, colW: [1.7, 1.1, 0.7, 0.7, 1.0], fontSize: 9, align: ["left", "right", "right", "right", "right"] });
  tbl(s, ["Mission-tagged funder (DMV grants)", "Tagged $", "of which DC", "DC share", "Funds Calvary", "Peers"],
    mt.map(r => [trunc(tc(r.funder_name), 40), money(r.amount, 1), money(r.dc_amount, 1), pct(num(r.dc_share)), yn(r.gives_to_calvary), r.peers_funded]),
    { x: 6.1, y: BODY_Y, w: 6.63, colW: [2.75, 0.85, 0.85, 0.7, 0.85, 0.63], fontSize: 9, align: ["left", "right", "right", "right", "left", "right"] });
  D.footnote(s, { source: `${SRCGR}; dim_program_area`, method: "keyword tags on grant purpose text (a grant can carry several tags); right table: DMV recipients, purpose tagged housing, DV or women, top 13 by tagged dollars", chart: "m4_07, m4_08", note: "C1" });

  // 7. Peer funders not funding Calvary (G1)
  X.section("Gaps");
  const g1 = D.readCsv("m5_01_peer_funders_not_calvary").sort((a, b) => num(b.peers_funded) - num(a.peers_funded) || num(b.peer_amount) - num(a.peer_amount) || a.funder_name.localeCompare(b.funder_name));
  const g1three = g1.filter(r => num(r.peers_funded) >= 3).length;
  X.table(`All ${g1.length} institutional funders of two or more peers lack a filed grant to Calvary, and ${g1three} of them fund three or more.`,
    ["Funder", "Type", "State", "Peers", "Peer $ TY2020–24", "Median peer grant", "Max peer grant", "Last peer TY", "Itemized TY2023+", "Peers funded"],
    g1.map(r => [trunc(tc(r.funder_name), 42), ft(r.funder_type), r.state, r.peers_funded, money(r.peer_amount), usd(r.median_peer_grant), usd(r.max_peer_grant), ty(r.last_peer_ty), yn(r.itemized_ty2023plus), trunc(r.peers_list, 48)]),
    [2.7, 1.45, 0.5, 0.5, 0.95, 0.85, 0.85, 0.7, 0.75, 2.88],
    { source: SRCGR, method: "G1: funders of ≥2 of the 18 provisional peers with no Calvary row TY2020–24; DAF sponsors excluded; itemized TY2023+ = the absence is current", chart: "m5_01", note: "C1" },
    { rowsPerSlide: 13, fontSize: 8.5 });

  // 8. Lapsed
  const lp = D.readCsv("m5_02_lapsed_funders").sort((a, b) => a.status.localeCompare(b.status) || num(b.total) - num(a.total) || a.funder_name.localeCompare(b.funder_name));
  const lapsed = lp.filter(r => r.status.startsWith("lapsed")), unclear = lp.length - lapsed.length;
  X.table(`${word(lapsed.length)} lapsed former funders once gave Calvary ${money(lapsed.reduce((a, r) => a + num(r.total), 0))} and ${unclear === 1 ? "one more is" : `${unclear} more are`} unclear because no itemized TY2023+ filing is in the data.`,
    ["Funder", "Type", "First TY", "Last TY", "Total to Calvary", "Years", "Last grant", "Peers funded TY2020–24", "Status"],
    lp.map(r => [nm(r.funder_name), ft(r.funder_type), ty(r.first_ty), ty(r.last_ty), usd(r.total), r.years, usd(r.last_amount), r.peers_funded_ty2020_24, r.status.startsWith("lapsed") ? "lapsed" : "unclear"]),
    [3.9, 1.9, 0.8, 0.8, 1.15, 0.6, 1.0, 1.0, 0.98],
    { source: "Funders' 990-PF / Schedule I rows naming Calvary, all years (IRS e-file via GivingTuesday); fact_grants, dim_funder", method: "G2 lapsed: last Calvary grant ≤ TY2022 and the funder filed itemized lists in TY2023+ with no Calvary row; unclear: no itemized TY2023+ filing in the data", chart: "m5_02", note: "C1" },
    { rowsPerSlide: 13, fontSize: 9.5 });

  // 9. Headroom
  const hd = D.readCsv("m5_03_current_funder_headroom").sort((a, b) => num(b.headroom_to_max_peer_grant) - num(a.headroom_to_max_peer_grant) || a.funder_name.localeCompare(b.funder_name));
  const hdN = hd.filter(r => num(r.headroom_to_max_peer_grant) > 0).length;
  X.table(`${word(hdN)} current funders have headroom: each has written a larger single grant to a core peer than to Calvary.`,
    ["Funder", "Type", "Calvary total TY2020–24", "Calvary years", "Largest to Calvary", "Last TY", "Peers funded", "Median peer grant", "Largest to a peer", "Headroom (largest)"],
    hd.map(r => [nm(r.funder_name), ft(r.funder_type), usd(r.calvary_total), r.calvary_years, usd(r.calvary_max), ty(r.last_ty), n0(r.peers_funded), usd(r.median_peer_grant), usd(r.max_peer_grant), usd(r.headroom_to_max_peer_grant)]),
    [3.2, 1.6, 1.05, 0.7, 0.95, 0.7, 0.65, 0.95, 1.0, 1.33],
    { source: SRCGR, method: "G3: largest single grant to any core peer vs largest to Calvary, TY2020–24 (a peer's larger grant may be capital or restricted)", chart: "m5_03", note: "C1" },
    { rowsPerSlide: 13, fontSize: 9 });

  // 10. DC majors not Calvary
  const mj = D.readCsv("m5_04_dc_majors_not_calvary").sort((a, b) => num(b.dc_sector_amount) - num(a.dc_sector_amount) || a.funder_name.localeCompare(b.funder_name));
  X.table(`${word(mj.length)} institutional funders gave $500K or more to DC-sector organizations in TY2020–24 with no filed grant to Calvary, led by ${tc(mj[0].funder_name).replace(/ Inc$/, "")} (${money(mj[0].dc_sector_amount, 1)}).`,
    ["Funder", "Type", "State", "DC-sector $", "DC recipients", "Median grant", "Max grant", "Peers funded", "Mission share", "Itemized TY2023+", "See-attached years"],
    mj.map(r => [nm(r.funder_name), ft(r.funder_type), r.state, money(r.dc_sector_amount, 1), r.dc_sector_recipients, usd(r.median_grant), money(r.max_grant), r.peers_funded, pct(num(r.mission_share)), yn(r.itemized_ty2023plus), r.placeholder_years]),
    [3.1, 1.6, 0.5, 0.9, 0.8, 0.85, 0.85, 0.7, 0.75, 0.8, 1.28],
    { source: SRCLAND, method: "G4: institutional funders with ≥ $500K to dc_sector organizations TY2020–24 and no Calvary row; mission share = DC-sector $ tagged housing/DV/women", chart: "m5_04", note: "C1" },
    { rowsPerSlide: 14, fontSize: 9 });

  // 11. Web-list-only gaps
  const wl = D.readCsv("m5_05_web_list_gaps").sort((a, b) => num(b.peers_listed) - num(a.peers_listed) || a.funder_name.localeCompare(b.funder_name));
  X.table(`${word(wl.length)} funders appear on two or more peer donor lists but on no Calvary list or filing, mostly corporations without public filings.`,
    ["Funder (as listed)", "Funder type", "Peer donor lists naming it"],
    wl.map(r => [nm(r.funder_name), r.funder_type === "other" ? "other (corporate / no filing)" : ft(r.funder_type), r.peers_listed]),
    [5.5, 4.0, 2.63],
    { source: "Peers' annual reports and donor web pages (six peers publish lists); fact_grants (web rows)", method: "G5: named on ≥ 2 peer lists, absent from Calvary's lists, CRM and filed grants; lists are undated and carry no amounts", chart: "m5_05", note: "C1" },
    { rowsPerSlide: 16, fontSize: 10 });

  // 12. CRM reconciliation
  const cr = D.readCsv("m5_06_crm_reconciliation").sort((a, b) => num(b.crm_total) - num(a.crm_total));
  const crTot = cr.reduce((a, r) => a + num(r.crm_total), 0), crConf = num(cr.find(r => r.status === "confirmed_in_window").crm_total);
  const CRL = { confirmed_in_window: "Confirmed in the funder's TY2023+ filing", not_exempt_filer: "Corporate or other, no public filing", no_filing_rows: "Exempt filer, no Calvary row found", attachment_only_list: "'See attached' filer (recipients unnamed)", confirmed_earlier_only: "Confirmed in earlier years only" };
  s = X.head(`The CRM reconciliation by status confirms ${pct(crConf / crTot)} of the ${money(crTot)} in CRM-recorded institutional giving in funders' own filings.`);
  C.img(s, "m5_06_crm_reconciliation", { x: M, y: BODY_Y, w: 6.5, h: 3.0 });
  const crRows = cr.map(r => [CRL[r.status] || r.status, n0(r.funders), usd(r.crm_total), pct(num(r.crm_total) / crTot)]);
  const crT = ["Total", n0(cr.reduce((a, r) => a + num(r.funders), 0)), usd(crTot), "100%"]; crT._bold = true; crRows.push(crT);
  tbl(s, ["Verification status", "Funders", "CRM total", "Share"], crRows, { x: 7.3, y: BODY_Y, w: 5.43, colW: [2.7, 0.8, 1.2, 0.73], fontSize: 10, align: ["left", "right", "right", "right"] });
  s.addText("CRM totals are cumulative over an unconfirmed 2023–26 window (assumption A1) and assumed cash unless contradicted (A2); they are never added to filed annual grants.",
    { x: 7.3, y: 4.2, w: 5.43, h: 1.0, fontSize: 10, color: HEX.text2, margin: 0, isTextBox: true, valign: "top" });
  D.footnote(s, { source: "Calvary CRM export (foundation and corporate funders, 2023–26) vs funders' 990-PF / Schedule I; supp_crm_cash_verification", method: "each CRM funder matched to its own filings and assigned one verification status", chart: "m5_06", note: "C1" });

  // 13. Network: PNG + top 25 table
  X.section("Network");
  const cf = D.readCsv("m6_01_central_funders").sort((a, b) => num(b.recipients) - num(a.recipients) || num(b.amount) - num(a.amount) || a.funder_name.localeCompare(b.funder_name)).slice(0, 25);
  const cfNot = cf.filter(r => r.funds_calvary !== "True");
  {
    const s = X.head("Calvary sits inside the same funder web as its peers rather than at its edge.");
    D.wideImage(s, "m6_03_network", { title: "Reading the network", place: C.img, lines: [
      "Nodes: Calvary, the 18 provisional peers and the funders of three or more of them.",
      "Edges: filed grants TY2020–24; edge width = dollars.",
      "Most of the best-connected funders already fund Calvary; the next table lists the 25 most connected."] });
    D.footnote(s, { source: SRCGR, method: "bipartite graph funders × 19 recipients; concentric layout (hub funders inner ring, peers outer ring); landscape exclusions applied", chart: "m6_03, m6_01", note: "C2" });
  }
  X.table(`The 25 most connected funders in the network (filed grants TY2020–24)`,
    ["Rank", "Funder", "Type", "Organizations funded (of 19)", "Filed grants $", "Grants", "Betweenness", "Funds Calvary"],
    cf.map((r, i) => [i + 1, nm(r.funder_name), ft(r.funder_type), r.recipients, money(r.amount, 2), r.grants, num(r.betweenness).toFixed(3), yn(r.funds_calvary)]),
    [0.6, 4.2, 2.0, 1.4, 1.2, 0.8, 1.0, 0.93],
    { source: SRCGR, method: "degree = organizations funded among Calvary + 18 peers; betweenness on the unweighted bipartite graph; DAF sponsors included as channels", chart: "m6_01", note: "C2" },
    { rowsPerSlide: 13, fontSize: 9.5 });

  // 14. Board interlocks
  const il = D.readCsv("m6_04_board_interlocks").sort((a, b) => (a.confidence === "high" ? 0 : 1) - (b.confidence === "high" ? 0 : 1) || (a.subject === "Calvary" ? 0 : 1) - (b.subject === "Calvary" ? 0 : 1) || a.subject.localeCompare(b.subject) || a.other_name.localeCompare(b.other_name) || a.rel_id.localeCompare(b.rel_id));
  const ilHigh = il.filter(r => r.confidence === "high").length;
  X.table(`Of the ${il.length} board interlocks touching Calvary, peers and comparators, only ${ilHigh} are high confidence and the ${il.length - ilHigh} medium rows are labeled unconfirmed.`,
    ["Subject", "Linked organization", "Linked org is a funder", "Pipeline candidate", "Confidence", "Tax year", "Filing years, subject vs linked org"],
    il.map(r => [r.subject, trunc(tc(r.other_name), 46), yn(r.other_is_funder), yn(r.other_is_candidate), r.confidence === "high" ? "high" : "medium (unconfirmed)", yr(r.tax_year), trunc(String(r.evidence).replace(/^same person in filings; years /, ""), 44)]),
    [1.9, 3.4, 1.0, 0.9, 1.6, 0.7, 2.63],
    { source: "IRS 990 Part VII officer and board lists (IRS e-file via GivingTuesday); fact_org_relationships (shared_board_member), dim_person (person_id only)", method: "same person in both filings: exact normalized name plus a corroborating signal; no names shown; leadership materials use high confidence only", chart: "m6_04", note: "C2" },
    { rowsPerSlide: 14, fontSize: 8.5 });

  // 15. Relationship paths
  const rp = D.readCsv("m6_05_relationship_paths").sort((a, b) => num(b.path_strength) - num(a.path_strength) || num(b.peers_funded) - num(a.peers_funded) || a.funder_name.localeCompare(b.funder_name));
  X.table(`Relationship-path scores for all ${rp.length} candidates are highest for funders that already give to many of Calvary's peers and co-funders.`,
    ["Funder", "Type", "Gap category", "Peers funded", "Close peers", "Overlapping co-funders", "Board links (high / medium)", "Path strength", "Consulting variant"],
    rp.map(r => [nm(r.funder_name), ft(r.funder_type), trunc(r.gap_category, 40), r.peers_funded, r.close_peers_funded, r.calvary_cofunders_overlapping, `${r.board_links_high} / ${r.board_links_medium}`, num(r.path_strength).toFixed(2), num(r.path_strength_consulting).toFixed(2)]),
    [3.4, 1.65, 2.3, 0.7, 0.7, 0.95, 0.95, 0.7, 0.78],
    { source: `${SRCGR}; fact_org_relationships`, method: "0.40×peers (cap 12) + 0.25×close peers (cap 8) + 0.25×overlapping co-funders (cap 20) + 0.10×high board link; consulting adds 0.05 for a medium link", chart: "m6_05", note: "C2" },
    { rowsPerSlide: 14, fontSize: 9 });

  // 16. Scoring configuration
  X.section("Pipeline");
  const yaml = C.readText("calvary_analysis/config/scoring_weights.yaml");
  const block = (name) => { const m = yaml.match(new RegExp(`^${name}:\\s*\\n((?:[ ]{2}.*\\n?)+)`, "m")); return m ? m[1].split("\n").filter(l => /^\s{2}\w/.test(l)) : []; };
  const kv = (line) => { const m = line.match(/^\s*([\w-]+):\s*([^#]+?)\s*(?:#\s*(.*))?$/); return m ? { k: m[1], v: m[2], c: m[3] || "" } : null; };
  const one = (name) => { const m = yaml.match(new RegExp(`^${name}:\\s*([^#\\n]+?)\\s*(?:#\\s*(.*))?$`, "m")); return m ? { v: m[1], c: m[2] || "" } : { v: "—", c: "" }; };
  const weights = block("weights").map(kv).filter(Boolean);
  const H16 = "The scoring configuration weights seven dimensions and sets the tier cutoffs in one editable file, config/scoring_weights.yaml.";
  const foot16 = { source: "calvary_analysis/config/scoring_weights.yaml; inputs chart_data/m5_00_candidate_funders.csv and m6_05_relationship_paths.csv", method: "weighted sum of seven 0–1 scores; in-kind channels −0.30, see-attached filers −0.15; rerun scripts/07_m7_pipeline.py after edits", chart: "m7_00", note: "C3" };
  const scale = (v) => { const m = String(v).match(/min_amount:\s*(\d+),\s*max_amount:\s*(\d+)/); return m ? `${usd(m[1])} → ${usd(m[2])} (log-linear)` : v; };
  s = X.head(H16);
  tbl(s, ["Dimension", "Weight", "What it scores (comment in the file)"], weights.map(w => [ft(w.k), w.v, trunc(w.c, 120)]),
    { x: M, y: BODY_Y, w: FULL_W, colW: [2.0, 0.8, 9.33], fontSize: 10, align: ["left", "right", "left"] });
  const tiers = block("tiers").map(kv).filter(Boolean), rb = block("relationship_bonus").map(kv).filter(Boolean);
  tbl(s, ["Tier rule or relationship bonus", "Value"], [...tiers.map(t => [`tiers: ${ft(t.k)}`, /award/.test(t.k) ? usd(t.v) : t.v]), ...rb.map(t => [`relationship bonus: ${ft(t.k)}`, t.v])],
    { x: M, y: 4.3, w: 5.9, colW: [4.4, 1.5], fontSize: 9.5, align: ["left", "right"] });
  tbl(s, ["Scale or penalty", "Value"], [["award size scale (median peer grant)", scale(one("award_size_scale").v)], ["regional scale (DC-sector dollars)", scale(one("regional_scale").v)], ["peer giving cap (peers for a score of 1)", one("peer_giving_cap").v], ["placeholder penalty ('see attached')", `−${one("placeholder_penalty").v}`], ["in-kind / workplace channel penalty", `−${one("in_kind_penalty").v}`]],
    { x: 6.83, y: 4.3, w: 5.9, colW: [3.3, 2.6], fontSize: 9.5, align: ["left", "right"] });
  D.footnote(s, foot16);
  s = X.head(`${H16} (continued, 2 of 2)`);
  const acc = block("accessibility_scores").map(kv).filter(Boolean);
  tbl(s, ["Accessibility by funder type", "Score", "Note"], acc.map(a => [ft(a.k), a.v, trunc(a.c, 50)]), { x: M, y: BODY_Y, w: 5.9, colW: [2.3, 0.7, 2.9], fontSize: 9.5, align: ["left", "right", "left"] });
  const gov = yaml.split("\n").filter(l => /^\s*- \{id: GOV/.test(l)).map(l => ({ id: (l.match(/id: ([\w-]+)/) || [])[1], name: (l.match(/name: "([^"]+)"/) || [])[1], score: (l.match(/score: ([\d.]+)/) || [])[1], tier: (l.match(/tier: (\d)/) || [])[1] }));
  tbl(s, ["Analyst-scored government row", "Score", "Tier"], gov.map(r => [`${r.id}: ${trunc(r.name, 70)}`, r.score, r.tier]), { x: 6.83, y: BODY_Y, w: 5.9, colW: [4.6, 0.65, 0.65], fontSize: 9.5, align: ["left", "right", "right"] });
  s.addText("Channels: in-kind or workplace channels (Gifts for the Homeless, Capital Area Food Bank, America's Charities, Give Lively) take the in-kind penalty; the T. Rowe Price Program is scored like a DAF sponsor. Corporate CRM relationships (≥ $50K, no public filing) are also analyst-scored.",
    { x: 6.83, y: 4.3, w: 5.9, h: 1.6, fontSize: 10.5, color: HEX.text2, margin: 0, isTextBox: true, valign: "top" });
  D.footnote(s, foot16);

  // 17. Complete pipeline
  const pl = D.readCsv("m7_00_funder_pipeline").sort((a, b) => num(a.rank) - num(b.rank));
  const tc1 = pl.filter(r => r.tier === "1").length, tc2 = pl.filter(r => r.tier === "2").length, tc3 = pl.filter(r => r.tier === "3").length;
  X.table(`The complete pipeline, Tier 1 to Tier 3, ranks ${pl.length} rows: ${tc1} in Tier 1, ${tc2} in Tier 2 and ${tc3} in Tier 3.`,
    ["#", "Funder or program", "Track", "Tier", "Score", "Typical grant", "Peers", "Why"],
    pl.map(r => [r.rank, trunc(tc(r.funder_name), 46), trunc(r.track, 36), r.tier, num(r.score).toFixed(2), num(r.typical_grant) ? money(r.typical_grant) : "—", num(r.peers_funded) == null ? "—" : n0(r.peers_funded), trunc(r.why, 52)]),
    [0.45, 3.4, 2.4, 0.45, 0.55, 0.85, 0.55, 3.48],
    { source: "recommendations/funder_pipeline.csv (= chart_data/m7_00); config/scoring_weights.yaml", method: "weighted score, tiers: T1 ≥ 0.62 and median peer grant ≥ $25K; T2 ≥ 0.48; government and corporate rows analyst-scored (basis = inferred)", chart: "m7_00", note: "C3" },
    { rowsPerSlide: 13, fontSize: 9 });

  // 18. 90-day plan
  const ap = D.readCsv("m7_01_action_plan_90day").sort((a, b) => num(a.rank) - num(b.rank));
  X.table(`The 90-day action plan gives each of the ${ap.length} Tier 1 targets a next step, an owner role and a deadline.`,
    ["#", "Target", "Track", "Next step", "Owner role", "By", "Application cycle"],
    ap.map(r => [r.rank, trunc(tc(r.funder_name), 44), trunc(r.track, 30), trunc(r.next_step, 105), r.owner_role, r.deadline, trunc(r.next_deadline_or_cycle || "—", 40)]),
    [0.4, 2.4, 1.6, 4.0, 1.3, 1.0, 1.43],
    { source: "recommendations/action_plan_90day.csv; config/guideline_notes.csv (sources/web_tier1_guidelines.csv)", method: "deadlines relative to plan start; owner roles, not people; cycles from the analyst-reviewed web pull", chart: "m7_01", note: "C3" },
    { rowsPerSlide: 11, fontSize: 8.5 });

  // 19. Guideline notes
  const gn = D.readCsv("m7_04_guideline_notes");
  const bc = (b) => gn.filter(r => r.basis === b).length;
  X.table(`Application-process notes for ${gn.length} Tier 1–2 funders from the reviewed web pull: ${bc("web (first-party)")} first-party, ${bc("web (third-party)")} third-party and ${bc("no usable hit; analyst note")} analyst notes.`,
    ["Funder", "Application process", "Next deadline or cycle", "Basis", "Analyst note"],
    gn.map(r => [trunc(r.funder_name, 44), trunc(noEmail(r.application_process), 110), trunc(r.next_deadline_or_cycle || "—", 50), r.basis, trunc(r.note || "—", 60)]),
    [2.3, 4.4, 1.9, 1.5, 2.03],
    { source: "Funder web pages found by the approved Tier 1–2 search (sources/web_tier1_guidelines.csv, source_registry_extension.csv); config/guideline_notes.csv", method: "every hit hand-reviewed; third-party and misdirected hits not treated as first-party guidelines", chart: "m7_04", note: "C3" },
    { rowsPerSlide: 9, fontSize: 8.5 });

  // 20. Sensitivity
  const sv = D.readCsv("m7_05_sensitivity");
  const maxShift = Math.max(...sv.map(r => num(r.mean_abs_rank_shift_top30)));
  const minOverlap = Math.min(...sv.map(r => num(r.top10_overlap)));
  X.table(`Rank sensitivity to weight changes is low, since no ±0.05 change moves the top 30 more than ${maxShift.toFixed(1)} places on average.`,
    ["Change", "Mean rank shift (top 30)", "Top-10 overlap", "Tier 1–2 added", "Tier 1–2 dropped"],
    sv.map(r => [r.change, num(r.mean_abs_rank_shift_top30).toFixed(2), r.top10_overlap, r.tier12_added, r.tier12_dropped]),
    [4.6, 2.0, 1.8, 1.8, 1.93],
    { source: "chart_data/m7_05_sensitivity.csv (scripts/13_m7_sensitivity.py); config/scoring_weights.yaml", method: "each weight ±0.05 with renormalization, tier-2 cutoff ±0.05; institutional rows only (government, corporate and federal rows have fixed scores)", chart: "m7_05", note: "C3" },
    { rowsPerSlide: 16, fontSize: 9.5 });

  // 21. Expansion scan + federal notices
  X.section("Expansion");
  const ex = D.readCsv("m8_01_expansion_scan").sort((a, b) => num(a.distance_rank) - num(b.distance_rank) || num(b.dmv_amount_per_year) - num(a.dmv_amount_per_year));
  X.table("The expansion scan table and the relevant federal notices show large near pools in workforce and behavioral health and thin direct federal competition.",
    ["Area", "Distance", "Calvary today", "DMV tagged $/yr", "Funders ($100K+)", "Median grant", "Federal notices", "Peer and comparator models"],
    ex.map(r => [r.label.replace(/ \(core\)$/, ""), r.distance, trunc(r.calvary_now, 55), money(r.dmv_amount_per_year, 1), `${n0(r.funders)} (${n0(r.funders_100k_plus)})`, usd(r.median_grant), n0(r.federal_opps), trunc(r.peer_examples, 60)]),
    [2.1, 0.75, 2.55, 1.0, 1.0, 0.8, 0.75, 3.18],
    { source: "Funders' 990-PF / Schedule I TY2020–24 (fact_grants, dim_program_area); Grants.gov (fact_opportunities); fact_policy_events; config/expansion_areas.yaml", method: "DMV institutional grants whose purpose carries the tag, TY2020–24 ÷ 5; general operating excluded; distance ratings are analyst judgment", chart: "m8_01", note: "D1" },
    { rowsPerSlide: 10, fontSize: 9 });
  const fo = D.readCsv("m8_02_federal_opportunities").sort((a, b) => a.funder_name.localeCompare(b.funder_name) || String(a.close_date).localeCompare(String(b.close_date)) || a.opportunity_number.localeCompare(b.opportunity_number));
  const agencies = new Set(fo.map(r => r.funder_name)).size;
  X.table(`The ${fo.length} relevant federal notices come from ${agencies} agencies and offices, led by DOJ justice programs and HUD, with few direct fits for Calvary.`,
    ["Opportunity", "Title", "Agency", "Status", "Award ceiling", "Close date", "Area tags"],
    fo.map(r => [r.opportunity_number, trunc(r.title, 62), trunc(r.funder_name, 40), r.status, num(r.award_ceiling) ? money(r.award_ceiling, 1) : "—", r.close_date || "—", ft(r.program_area_tags).replace(/;/g, ", ")]),
    [1.6, 3.8, 2.5, 0.85, 0.9, 0.95, 1.53],
    { source: "Grants.gov posted and forecasted opportunities; fact_opportunities", method: "research, tribal, rural and overseas notices removed; HUD, VA, DOL, DOJ, ACF, SAMHSA, USDA, Treasury and ACL kept; snapshot as of the data date", chart: "m8_02", note: "D1" },
    { rowsPerSlide: 12, fontSize: 8.5 });

  await D.finish(pres, path.join(__dirname, "appendix_C_funders_pipeline.pptx"));
})();
