// Leadership and board deck (22 slides): storylines/leadership_headline_spine.md and leadership_storyline.md.
// Craft rules from design_system.md §5b: SCR executive summary up front, action titles ≤ 2 lines, one message per slide,
// bold-claim/evidence cards, a bumper (implication) line on content slides, decisions needed on the next-steps slide.
const D = require("./lib/deck");
const { HEX, M, W, BODY_Y, BODY_H } = D;
const path = require("path");
const tc = (s) => String(s).replace(/\b\w+/g, w => w[0] + w.slice(1).toLowerCase()).replace(/ Inc\b/g, "").replace(/'S\b/g, "'s");
// Visual-QA helpers: word-boundary truncation with an ellipsis; headline size step-down so long titles stay on two lines.
const trunc = (s, n) => { s = String(s == null ? "" : s); if (s.length <= n) return s; const cut = s.slice(0, n); const sp = cut.lastIndexOf(" "); return (sp > n * 0.6 ? cut.slice(0, sp) : cut).replace(/[\s,;:(–\-\/]+$/, "") + "…"; };
function fitTitles(pres) {
  pres._slides.forEach(sl => {
    if (!sl._slideLayout || sl._slideLayout._name !== "HEADLINE") return;
    const o = sl._slideObjects.find(x => x.options && x.options.placeholder === "title"); if (!o) return;
    const runs = Array.isArray(o.text) ? o.text : [{ text: String(o.text), options: {} }];
    const len = runs.map(r => r.text).join("").length;
    const size = len > 205 ? 18 : Math.max(17, Math.min(21, Math.floor(162 * 21 / len)));
    if (size >= 21) return;
    o.options.fontSize = size; runs.forEach(r => { r.options = Object.assign({}, r.options, { fontSize: size }); });
  });
}

(async () => {
  const { pres } = D.newDeck("Calvary's funding today, and the opportunities ahead", "Leadership and board deck");
  const S = (t) => pres.addSection({ title: t });
  const CHART_W = 8.0, CARD_X = M + CHART_W + 0.3, CARD_W = W - M - CARD_X;
  const pipe = D.readCsv("m7_00_funder_pipeline");
  const nT1 = pipe.filter(r => r.tier === "1").length;
  const words = { 11: "Eleven", 12: "Twelve", 13: "Thirteen" }[nT1] || String(nT1);

  // 1 title
  S("Opening");
  D.titleSlide(pres, "Calvary's funding today, and the opportunities ahead", "A pro bono look at Calvary Women's Services' public and private funding, built from public records, for discussion with leadership and the board.", "Opening");

  // 2 executive summary (SCR, bold-claim / evidence-bullet)
  let s = D.headlineSlide(pres, "Calvary has become a system-level provider whose funding needs a better shape and a deeper cushion, not a smaller share.", "Opening");
  D.claimBullets(s, [
    { claim: "Situation: Calvary has built a stronger organization, funded mostly by public partners.", bullets: ["Revenue up 59% in real terms FY19→FY25; inventory 68 → 124 beds, 6.8% of DC's transitional-housing beds", "Public funding is about half of revenue (53% FY22–24), typical for DC peers (11th of 19)"] },
    { claim: "Complication: the money arrives in a concentrated shape, private support has held flat, and FY25 thinned the cushion.", bullets: ["Three public streams, two through TCP, carry 74% of a $4.1M award base; the DHS contract is the largest and least documented", "Foundation grants steady at ~$1M a year, one partner 27%; FY25: −$607K, event income −$483K, 4.4 months of cash", "Calvary recognized only about two-thirds of its known award ceilings as revenue in FY24–25"] },
    { claim: "Resolution: draw every awarded dollar, grow private support alongside the public base, and hold a reserve.", bullets: [`A 90-day plan on four fronts with ${words.toLowerCase()} Tier 1 targets: upgrade GWCF, Cafritz, Abell, Fowler; open Clark, Schattner; confirm the TCP contracts`, "Target: private revenue from ~$2.1M to ~$3M in three years, a six-month reserve, and workforce / behavioral-health formalization", "What we need from you: reactions, the FY24–25 audits, the TCP agreements, and the FY25 gala calendar"] },
  ], { x: M, y: BODY_Y - 0.15, w: W - 2 * M, h: BODY_H + 0.55, claimSize: 18, bulletSize: 15 });
  D.footnote(s, { source: "all modules M1–M10; figures carry chart IDs on the slides that follow", method: "Situation–Complication–Resolution; bold lines are the argument, bullets the evidence", chart: "m1_01, m2_01, m2_07, m7_00" });

  // 3 what Calvary has built
  S("Where Calvary stands");
  s = D.headlineSlide(pres, "In five years Calvary has grown revenue 59% in real terms and its housing inventory to 124 beds.", "Where Calvary stands");
  D.statTiles(s, [
    { value: "+59%", label: "Real revenue growth FY19 → FY25 ($2.49M → $4.97M, 2024 dollars)" },
    { value: "124 beds", label: "Housing inventory 2025, up from 68 in 2022; 6.8% of DC's transitional-housing beds (2.5% in 2022)" },
    { value: "3 streams", label: "Public partners: DC OVSJG, HUD Continuum of Care via TCP, DC DHS via TCP" },
    { value: "50 funders", label: "Foundations and donor-advised sponsors with filed grants to Calvary, TY2020–24" },
  ], { y: BODY_Y, h: 2.4 });
  s.addText("Calvary did this while serving the two wards with the deepest need in the city: Ward 8's poverty rate is 31% against 15% citywide, and a third of renters in Wards 7 and 8 pay more than half their income in rent.", { x: M, y: 4.5, w: W - 2 * M, h: 1.2, fontSize: 15, color: HEX.text, margin: 0, isTextBox: true });
  D.bumper(s, "the case for Calvary to funders is strong and quantified, and the question is how to fund the next five years as well as the last five.");
  D.footnote(s, { source: "IRS Form 990 returns FY2011–FY2025 (GivingTuesday / ProPublica / IRS SOI) in fact_org_financials; HUD Housing Inventory Count 2022–2025 in supp_hic_projects; ACS 2020–24 by ward in dim_geo", method: "revenue deflated with CPI-U to 2024 dollars; beds = HIC total_beds for Calvary projects", chart: "m1_01, m9_03, m9_01", note: "A1" });

  // 4 revenue mix
  s = D.headlineSlide(pres, "Public partners funded most of that growth and now provide about half of revenue, typical for DC peers.", "Where Calvary stands");
  const mix = D.readCsv("m1_02_revenue_mix");
  D.chart(s, "bar", mix.map(r => r.fy_label), [
    { name: "Government (audit basis; 990 line 1e for FY24–25)", values: mix.map(r => D.num(r.government)), color: HEX.government },
    { name: "Private contributions (foundations, corporate, individuals)", values: mix.map(r => D.num(r.private_contributions_ex_events)), color: HEX.institutional },
    { name: "Event contributions", values: mix.map(r => D.num(r.event_contributions)), color: HEX.individuals },
    { name: "Other revenue", values: mix.map(r => Math.max(0, D.num(r.other_revenue) || 0)), color: HEX.other },
  ], { x: M, y: BODY_Y, w: CHART_W, h: BODY_H, stacked: true });
  D.card(s, { x: CARD_X, y: BODY_Y, w: CARD_W, h: BODY_H, title: "What the chart says", lines: ["**The share is typical.", "Government ran 40–61% every year since FY15; 53% on average for FY22–24.", "11th of 19 DC-area organizations; 57th percentile of DC's human-services sector.", "**Growth came with it.", "The FY22 spike was a one-time $3.68M award to buy the New Foundations building."], fontSize: 11.5 });
  D.bumper(s, "the share itself is not the problem to solve, and the shape of the public money and the private base are.");
  D.footnote(s, { source: "Calvary audited financial statements FY15–FY23 (government revenue) and IRS 990 returns, fact_org_financials", method: "government share = audited government contracts and grants ÷ audited revenue; 990 line 1e ÷ 990 revenue for FY24–25", chart: "m1_02", note: "A1" });

  // 5 stream map
  s = D.headlineSlide(pres, "The question is the shape of the public money, since three streams, two through one intermediary, carry $4.1M a year.", "Where Calvary stands");
  const sm = D.readCsv("m2_01_stream_map");
  const years = [...new Set(sm.map(r => r.fiscal_year))].sort();
  const streams = ["OVSJG (DC local)", "HUD CoC via TCP (federal)", "DHS via TCP (DC local)", "Other federal pass-through"];
  const colors = [HEX.government, HEX.daf, HEX.institutional, HEX.other];
  D.chart(s, "bar", years, streams.map((st, i) => ({ name: st, color: colors[i], values: years.map(y => sm.filter(r => r.stream === st && r.fiscal_year === y).reduce((a, r) => a + (D.num(r.amount) || 0), 0)) })), { x: M, y: BODY_Y, w: CHART_W, h: BODY_H, stacked: true });
  D.card(s, { x: CARD_X, y: BODY_Y, w: CARD_W, h: BODY_H, title: "Three channels, one hub", lines: ["**TCP carries 74% of the base.", "HUD CoC via TCP: $0.24M (2019) → $1.77M (FY2025), three projects.", "DHS via TCP: $1.42M in FY2024 (transitional housing $830K, Sisters Rise $593K); other years not public.", "**OVSJG is direct and growing.", "$0.37M (FY20) → $1.05M (FY26), two transitional-housing grants."], fontSize: 11.5 });
  D.bumper(s, "the relationship with TCP matters as much as any single program, and the DHS contract is the stream to document first.");
  D.footnote(s, { source: "DC OVSJG award lists FY2019–2026; HUD CoC award lists (TCP as applicant); DC Council oversight responses FY2024; Calvary single audits — fact_gov_awards", method: "one source per stream, never summed across sources; OVSJG and DHS by DC fiscal year, CoC by competition year; one-time awards excluded", chart: "m2_01", note: "A2" });

  // 6 private concentration
  s = D.headlineSlide(pres, "Private support has held steady near $1M a year in grants, with one partner providing more than a quarter.", "Where Calvary stands");
  const fc = D.readCsv("m1_07_calvary_funder_concentration").slice(0, 10).reverse();
  D.chart(s, "bar", fc.map(r => trunc(tc(r.funder_name), 44)), [{ name: "Filed grants TY2020–24", values: fc.map(r => D.num(r.amount)), color: HEX.institutional }], { x: M, y: BODY_Y, w: CHART_W, h: BODY_H, barDir: "bar", valFmt: "$#,##0,\"K\"", dataLabels: true, showLegend: false, catFontSize: 8 });
  D.card(s, { x: CARD_X, y: BODY_Y, w: CARD_W, h: BODY_H, title: "Steady, and concentrated", lines: ["**$0.64–1.17M a year from 26–29 funders.", "Grants named in funders' own filings, TY2020–24.", "**One partner is 27%; the top five are 63%.", "GWCF, including the time-limited Health Equity Fund.", "Donor-advised sponsors (Benevity, Fidelity, Schwab) add $1.1M over five years: individual donors' money."], fontSize: 11.5 });
  D.bumper(s, "the Health Equity Fund's finite life makes a successor conversation with GWCF timely, and the base needs more names and deeper grants.");
  D.footnote(s, { source: "Funders' IRS 990-PF and Schedule I filings TY2020–24 naming Calvary (GivingTuesday / IRS e-file), fact_grants and dim_funder", method: "non-cumulative rows, aggregated by funder EIN; TY2024 filings partly released", chart: "m1_07, m1_08", note: "A3" });

  // 7 FY25
  s = D.headlineSlide(pres, "After a strong FY24, FY25 brought a $607K deficit, a $483K event-income drop, and 4.4 months of cash.", "Where Calvary stands");
  D.statTiles(s, [
    { value: "−$607K", label: "FY25 operating result (revenue $4.97M, expenses $5.58M); FY24 was +$507K", color: HEX.negative },
    { value: "$538K → $55K", label: "Event contributions FY24 → FY25 (990 line 1c); net event income turned positive, so timing may explain part of it", size: 28 },
    { value: "4.4 months", label: "Cash and savings ÷ monthly expenses at FY25 year-end, down from 7.5 months in FY21" },
  ], { y: BODY_Y, h: 2.4 });
  s.addText("These are clouds on the horizon rather than a verdict on the year: FY24 was unusually strong and the event line may be a calendar change. They do mean there is little room to absorb a public-funding shock.", { x: M, y: 4.5, w: W - 2 * M, h: 1.2, fontSize: 15, color: HEX.text, margin: 0, isTextBox: true });
  D.bumper(s, "the plan that follows starts with cash and draw-down, because a thin cushion turns a survivable cut into a crisis.");
  D.footnote(s, { source: "IRS 990 returns FY2021–FY2025, fact_org_financials", method: "months of cash = cash_savings_eoy ÷ (total_expenses ÷ 12)", chart: "m1_04, m1_05, m1_06", note: "A1" });

  // 8 DC budget context
  S("The clouds on the horizon");
  D.sectionSlide(pres, "The clouds on the horizon", "DC's budgets have held, the Council has restored every proposed cut, and the real risk sits in one channel.", "The clouds on the horizon");
  s = D.headlineSlide(pres, "DC's budgets behind Calvary's local funding have held through FY2027, but a cut is proposed every spring.", "The clouds on the horizon");
  D.image(s, "m2_04_dc_budget_context", { x: M, y: BODY_Y, w: CHART_W + 0.3, h: BODY_H });
  D.card(s, { x: CARD_X + 0.3, y: BODY_Y, w: CARD_W - 0.3, h: BODY_H, title: "Stable pools, annual threat", lines: ["**OVSJG Victim Services grants are flat at $55M.", "$45.5M (FY24) → $55.9M (FY25) → $55.4M (FY26) → $55.3M (FY27) approved.", "Mayor proposed −$5.8M (FY26) and −$5.6M (FY27); the Council restored both.", "**DHS homeless services rose.", "$170M (FY24) → $206M (FY26) → $194M (FY27); actual OVSJG spending runs 9–14% under approved."], fontSize: 11 });
  D.bumper(s, "the local risk is annual and political, which an advocacy calendar can manage, and it is not a structural decline.");
  D.footnote(s, { source: "DC budget books FY2024–FY2027 (OCFO Schedule 30-PBB, agency chapters) and Council committee reports — supp_dc_budget_lines, fact_policy_events", method: "activity-level totals by program code; approved vs actual vs Mayor's proposal", chart: "m2_04, m2_06", note: "A6" });

  // 9 scenarios
  s = D.headlineSlide(pres, "Calvary can absorb the headline cuts, but losing the DHS contract through TCP is the cloud to plan for.", "The clouds on the horizon");
  const sc = D.readCsv("m2_07_scenarios");
  const rows = sc.map(r => [r.scenario, r.scenario_id === "S0" ? "–" : `−${D.fmtK(D.num(r.revenue_loss))}`, r.scenario_id === "S0" ? "–" : D.fmtPct(D.num(r.loss_pct_of_total_revenue)), `−${D.fmtK(-D.num(r.deficit_gross))}`, D.num(r.months_of_cash_after_12m_net).toFixed(1)]);
  const hdr = ["Scenario (FY25 baseline)", "Revenue loss", "% of revenue", "Deficit (gross)", "Months of cash after a year (net)"].map(h => ({ text: h, options: { bold: true, color: HEX.ink, fill: { color: HEX.surface2 }, fontSize: 11 } }));
  s.addTable([hdr, ...rows.map((r, i) => r.map(c => ({ text: c, options: { fontSize: 11, color: HEX.text, bold: i >= 5 } })))], { x: M, y: BODY_Y, w: W - 2 * M, colW: [4.6, 1.8, 1.6, 1.9, 2.2], border: { type: "solid", pt: 0.5, color: HEX.grid }, fontFace: "Arial", margin: 0.06, objectName: "scenario table" });
  s.addText("Reading: an OVSJG cut of the size proposed in FY26 costs about $67K; a lost DHS/TCP contract costs about $960K. The net column assumes half of a lost stream's revenue is avoidable cost. Even the baseline burns cash at about $50K a month.", { x: M, y: 4.6, w: W - 2 * M, h: 0.9, fontSize: 12.5, color: HEX.text2, margin: 0, isTextBox: true });
  D.bumper(s, "protect the TCP-channel contract first, and the OVSJG budget season is survivable with a reserve and a voice in the coalition.");
  D.footnote(s, { source: "fact_gov_awards (award ceilings by stream) and fact_org_financials (FY25 990); parameters in config/scenarios.yaml", method: "FY25 recognized government revenue apportioned to streams by FY-aligned award ceilings; cuts applied to the apportioned amounts", chart: "m2_07", note: "A4" });

  // 10 ceilings vs recognized
  s = D.headlineSlide(pres, "Calvary recognized about two-thirds of its known award ceilings in FY24–25, the first place to look.", "The clouds on the horizon");
  const cv = D.readCsv("m2_02_ceilings_vs_recognized").filter(r => ["FY24", "FY25"].includes(r.fy_label));
  D.chart(s, "bar", cv.map(r => r.fy_label), [
    { name: "Known award ceilings (OVSJG + CoC + DHS + other)", values: cv.map(r => D.num(r.award_ceiling_known)), color: HEX.peer },
    { name: "Recognized government revenue (990 line 1e)", values: cv.map(r => D.num(r.recognized_gov_revenue)), color: HEX.government },
  ], { x: M, y: BODY_Y, w: CHART_W, h: BODY_H, dataLabels: true, gapWidth: 80 });
  D.card(s, { x: CARD_X, y: BODY_Y, w: CARD_W, h: BODY_H, title: "A question, not a finding", lines: ["**FY24: $2.62M of $3.6M (73%). FY25: $2.89M of $4.3M (67%).", "Ceilings are awards, not revenue: timing, draw rates and cost-reimbursement limits all lower the figure.", "The DHS value is public for FY2024 only and is carried into FY25.", "**The audits would settle it.", "Calvary's FY24 and FY25 audits and its TCP subgrant agreements answer this in an afternoon."], fontSize: 11.5 });
  D.bumper(s, "undrawn awards are the cheapest revenue there is, and a draw-down reconciliation is the first task in the 90-day plan.");
  D.footnote(s, { source: "fact_gov_awards aligned to Calvary's fiscal year (DC FY direct; HUD competition year lagged one year; DHS FY2024 carried forward); fact_org_financials", method: "ratio = recognized government revenue ÷ sum of known award ceilings", chart: "m2_02", note: "A5" });

  // 11 peers paths
  S("What peers show");
  D.sectionSlide(pres, "What peers show", "Organizations with Calvary's profile have grown on more than one model; the closest fit is to grow private support alongside a stable public base.", "What peers show");
  s = D.headlineSlide(pres, "Peers show three workable paths, and N Street Village's, growing private support beside a stable public base, fits Calvary best.", "What peers show");
  D.image(s, "m3_08_case_studies_mix", { x: M, y: BODY_Y, w: CHART_W + 0.6, h: BODY_H });
  D.card(s, { x: CARD_X + 0.6, y: BODY_Y, w: CARD_W - 0.6, h: BODY_H, title: "Three paths", lines: ["**Samaritan Inns", "Government 72% → 11% while revenue held, replaced by program revenue.", "**N Street Village", "~40% government, grew on private money; 8 months of cash.", "**Miriam's Kitchen", "Philanthropy-led, tripled since FY18.", "**DWC (LA)", "Scaled 3× since 2018 with government rising to 57%, on 2–3 months of cash."], fontSize: 11 });
  D.bumper(s, "the N Street Village path fits Calvary's model and size, and Samaritan Inns shows the earned-revenue option.");
  D.footnote(s, { source: "IRS 990 returns of 18 provisional DC-area peers and 2 Los Angeles comparators, fact_org_financials", method: "government = 990 line 1e; peers chosen for model similarity (config/core_peers.csv, provisional)", chart: "m3_08, m3_01", note: "B1" });

  // 12 institutional depth
  s = D.headlineSlide(pres, "Calvary already works its foundation funders harder than most peers, so the headroom is deeper grants, donors and earned revenue.", "What peers show");
  const bt = D.readCsv("m3_00_benchmark_table").filter(r => D.num(r.institutional_per_revenue_dollar) != null).sort((a, b) => D.num(a.institutional_per_revenue_dollar) - D.num(b.institutional_per_revenue_dollar));
  D.chart(s, "bar", bt.map(r => r.org), [{ name: "Institutional grants ÷ revenue, 2020–24", values: bt.map(r => D.num(r.institutional_per_revenue_dollar)), color: HEX.institutional }], { x: M, y: BODY_Y, w: CHART_W, h: BODY_H, barDir: "bar", valFmt: "0%", dataLabels: true, showLegend: false, catFontSize: 8 });
  D.card(s, { x: CARD_X, y: BODY_Y, w: CARD_W, h: BODY_H, title: "Depth, not count", lines: ["**Calvary: 42 funders; grants equal to 12% of revenue.", "Typical peer 6–8% (N Street Village, House of Ruth DC); only Samaritan Inns (27%) is far ahead.", "**Donor-advised funds are the gap.", "25% of Calvary's filed grants vs 51% at N Street Village and 41% at Miriam's Kitchen."], fontSize: 11.5 });
  D.bumper(s, "more applications have limited headroom, and bigger multi-year grants, a major-gifts program and billable program revenue are the levers.");
  D.footnote(s, { source: "Funders' 990-PF and Schedule I filings TY2020–24 naming each organization (fact_grants, dim_funder); 990 revenue FY2020–24 (fact_org_financials)", method: "institutional = all funder types except DAF sponsors; DMV funders' filings only", chart: "m3_06", note: "B2" });

  // 13 the money is there
  S("Where the opportunities are");
  D.sectionSlide(pres, "Where the opportunities are", "The money exists in DC's funder community, and most of it already flows to organizations that share Calvary's funders.", "Where the opportunities are");
  s = D.headlineSlide(pres, "DMV funders give DC's sector $132M a year, and 23 of them already fund three or more of Calvary's peers.", "Where the opportunities are");
  const gaps = D.readCsv("m5_01_peer_funders_not_calvary").filter(r => D.num(r.peers_funded) >= 3).slice(0, 14).reverse();
  D.chart(s, "bar", gaps.map(r => trunc(tc(r.funder_name), 42)), [{ name: "Core peers funded (of 18)", values: gaps.map(r => D.num(r.peers_funded)), color: HEX.institutional }], { x: M, y: BODY_Y, w: CHART_W, h: BODY_H, barDir: "bar", valFmt: "0", dataLabels: true, showLegend: false, catFontSize: 8 });
  D.card(s, { x: CARD_X, y: BODY_Y, w: CARD_W, h: BODY_H, title: "Warm cold prospects", lines: ["**$660M flowed to DC's sector in TY2020–24, 58% via donor-advised funds.", "**Clark Charitable: $7.8M to five peers, median grant $250K, no Calvary grant yet.", "Schattner, Cohen, Bernstein and The Washington Home each fund 3–4 peers at $25–75K.", "Venable and America's Charities are already in Calvary's records; the filing gap is lag."], fontSize: 11.5 });
  D.bumper(s, "these funders already fund Calvary's model, and the ask is an introduction, not a case for the cause.");
  D.footnote(s, { source: "Funders' 990-PF and Schedule I filings TY2020–24 (fact_grants, dim_funder, dim_universe_membership); landscape exclusions in config/landscape_exclusions.csv", method: "gap = funder names 2+ core peers and no Calvary row in TY2020–24 filings; DAF sponsors excluded", chart: "m5_01, m4_01", note: "C1" });

  // 14 network
  s = D.headlineSlide(pres, "Calvary sits inside the funder web, so the next funders are one introduction away through peers that share its funders.", "Where the opportunities are");
  D.wideImage(s, "m6_03_network", { title: "Closest neighbors", lines: ["**17 shared funders with Miriam's Kitchen; 14 each with DASH and House of Ruth DC.", "House of Ruth DC (69) and House of Ruth MD (81) have the longest lists of funders Calvary lacks.", "**Board overlaps are thin in public filings.", "One high-confidence link, not a funder; introductions run through shared funders and peers."] });
  D.bumper(s, "ask the closest peers for introductions to the funders they share with each other but not yet with Calvary.");
  D.footnote(s, { source: "fact_grants (funders of Calvary and 18 peers, TY2020–24), fact_org_relationships (board links by person match confidence)", method: "bipartite funder–recipient graph; funders of 3+ organizations shown; high-confidence board links only in this deck", chart: "m6_03, m6_02", note: "C2" });

  // 15 90-day plan
  S("A plan to consider");
  D.sectionSlide(pres, "A plan to consider", `Four fronts over 90 days, ${words.toLowerCase()} named targets, and two policy choices for the board.`, "A plan to consider");
  s = D.headlineSlide(pres, "We suggest a 90-day plan that draws every awarded dollar, upgrades partners, opens new foundations and restores the event line.", "A plan to consider");
  const cw = (W - 2 * M - 0.9) / 4;
  [["1. Draw every awarded dollar", ["**Day 30", "Reconcile award ceilings to revenue for FY24–26", "Confirm the DHS contract and Sisters Rise status with TCP", "Defend the three CoC renewals; scope a PSH expansion project"]],
   ["2. Upgrade current partners", ["**Day 45", "Multi-year general-operating asks to GWCF, Cafritz, Abell, Fowler, United Way NCA, Bank of America", "Ask GWCF about a Health Equity Fund successor", "Cafritz deadlines: Mar 1, Jul 1, Nov 1"]],
   ["3. Open new foundations", ["**Day 60–90", "Clark Charitable first, via the peers it funds", "Schattner, Cohen, Bernstein, The Washington Home", "Re-engage Many Hands (January window), World Bank CCF, Jane Bancroft Robinson"]],
   ["4. Restore the event line", ["**Day 45", "Confirm whether the FY25 gala moved across the fiscal year", "Set the FY26 event at the FY24 level ($538K)", "Start a named major-gifts and DAF program"]],
  ].forEach(([t, lines], i) => D.card(s, { x: M + i * (cw + 0.3), y: BODY_Y, w: cw, h: 3.1, title: t, lines, fontSize: 12 }));
  D.bumper(s, "front 1 costs nothing and may be worth the most, and fronts 2–4 are the private-revenue plan that moves the share toward half.");
  D.footnote(s, { source: "recommendations/strategic_recommendations.md, built from modules M1–M7", method: "recommendations are options for Calvary's leadership to weigh, drawn from the evidence in this deck", chart: "m7_01" });

  // 16 Tier 1 table
  s = D.headlineSlide(pres, `${words} Tier 1 targets come with a next step, an owner and a deadline.`, "A plan to consider");
  const plan = D.readCsv("m7_01_action_plan_90day");
  const prow = plan.map(r => [r.track.startsWith("institutional") ? tc(r.funder_name) : String(r.funder_name), r.track.split(":")[0].replace("government_dc", "DC public").replace("government_federal", "federal public").replace("institutional", "foundation"), r.next_step, r.owner_role, r.deadline, String(r.next_deadline_or_cycle || "").split(" (")[0]]);
  const ph = ["Target", "Track", "Next step", "Owner", "By", "Application cycle"].map(h => ({ text: h, options: { bold: true, color: HEX.ink, fill: { color: HEX.surface2 }, fontSize: 9.5 } }));
  s.addTable([ph, ...prow.map(r => r.map(c => ({ text: c, options: { fontSize: 8.5, color: HEX.text } })))], { x: M, y: BODY_Y - 0.15, w: W - 2 * M, colW: [2.9, 1.0, 4.6, 1.4, 0.85, 1.38], border: { type: "solid", pt: 0.5, color: HEX.grid }, fontFace: "Arial", margin: 0.035, objectName: "tier1 table" });
  D.bumper(s, "owners and dates are proposals for the working session, and the scoring weights behind the tiers are editable in one file.");
  D.footnote(s, { source: "recommendations/funder_pipeline.csv and action_plan_90day.csv (from fact_grants, dim_funder, fact_org_relationships, the CRM reconciliation and a reviewed web pull of funder guidelines)", method: "seven weighted dimensions in config/scoring_weights.yaml; Tier 1 = score ≥ 0.62 and typical grant ≥ $25K; public rows carry analyst scores", chart: "m7_01, m7_04", note: "C3" });

  // 17 expansion
  s = D.headlineSlide(pres, "Formalizing workforce and behavioral health opens the largest nearby pools without changing the mission.", "A plan to consider");
  const ex = D.readCsv("m8_01_expansion_scan").filter(r => r.tag !== "education").reverse();
  D.chart(s, "bar", ex.map(r => r.label.includes(`(${r.distance})`) ? r.label : `${r.label} (${r.distance})`), [{ name: "DMV institutional grants naming the area, $/yr", values: ex.map(r => D.num(r.dmv_amount_per_year)), color: HEX.institutional }], { x: M, y: BODY_Y, w: CHART_W, h: BODY_H, barDir: "bar", valFmt: "$#,##0,,\"M\"", dataLabels: true, showLegend: false, catFontSize: 8 });
  D.card(s, { x: CARD_X, y: BODY_Y, w: CARD_W, h: BODY_H, title: "Options and trade-offs", lines: ["**Workforce (near): a SheWorks-style cohort inside Step Up DC; opens DOES and workforce funders.", "**Behavioral health (near): a credential or billing partner turns therapy into program revenue.", "**Health (medium): clinic hours with an FQHC partner (Community of Hope is a Ward 8 peer).", "DV formalization raises the public share; families would be a mission change and is not suggested."], fontSize: 11 });
  D.bumper(s, "pick two near options to scope this year, and health is a partnership conversation, not a build.");
  D.footnote(s, { source: "fact_grants purpose text tagged with dim_program_area keywords (DMV institutional funders, TY2020–24); fact_opportunities; config/expansion_areas.yaml", method: "dollars whose purpose names the area (general operating excluded, so pools are understated); distance ratings are analyst judgment; education shown in the appendix", chart: "m8_01", note: "D1" });

  // 18 reserve and calendar
  s = D.headlineSlide(pres, "A six-month reserve and an annual advocacy calendar would make the spring budget season routine.", "A plan to consider");
  const half = (W - 2 * M - 0.3) / 2;
  D.card(s, { x: M, y: BODY_Y, w: half, h: 3.1, title: "Reserve policy", lines: ["**Target six months of expenses, about $2.8M; Calvary holds 4.4 today.", "Peers with Calvary's mix hold more: Doorways 12, Everyone Home DC 10, N Street Village 8; government-anchored DV providers hold about one.", "Treat the Health Equity Fund and other time-limited sources as one-time in the budget.", "Close the FY25 gap in the FY26 budget with the private tracks plus a cost plan."], fontSize: 13 });
  D.card(s, { x: M + half + 0.3, y: BODY_Y, w: half, h: 3.1, title: "Advocacy and monitoring calendar", lines: ["**March–July is the season: proposal, markups, vote.", "Mayor's budget March–April (cuts proposed in FY26 and FY27); committee markups May–June; Council vote June–July (restorations).", "Join the coalition testimony that restored the victim-services line twice.", "Track draw-down against ceilings monthly; watch OVSJG under-spend, TCP's DHS purchase orders, the CoC NOFO and the EHV sunset."], fontSize: 13 });
  D.bumper(s, "two board decisions: adopt a reserve target, and put the advocacy calendar on the board's own calendar.");
  D.footnote(s, { source: "fact_org_financials (months of cash, 20 organizations), fact_policy_events (DC budget calendar FY2024–FY2027)", method: "months of cash = cash and savings ÷ monthly expenses, FY2024", chart: "m3_04, m2_06", note: "A6, B1" });

  // 19 comparators
  s = D.headlineSlide(pres, "The Los Angeles comparators show scale with government (DWC) and a program design to borrow (SheWorks).", "A plan to consider");
  D.image(s, "m10_01_comparator_trajectories", { x: M, y: BODY_Y, w: CHART_W + 0.4, h: BODY_H });
  D.card(s, { x: CARD_X + 0.4, y: BODY_Y, w: CARD_W - 0.4, h: BODY_H, title: "What transfers", lines: ["**DWC", "$6M (2014) → $34M (2024), government 24% → 57%, 99% pass-through federal money, 2.4 months of cash.", "Transferable: the PSH pipeline, the clinic partnership, the MADE enterprise.", "**SheWorks", "Cohort model with stipends, childcare, transport and labor and health-plan partners; a design for Step Up DC, not a funding model."], fontSize: 11 });
  D.bumper(s, "borrow DWC's housing-development and partnership playbook and SheWorks' program design, and do not copy either funding mix.");
  D.footnote(s, { source: "IRS 990 returns (fact_org_financials); Federal Audit Clearinghouse single audits (fact_gov_awards); organization web pages and funder announcements (fact_grants web rows)", method: "government = 990 line 1e; DWC fiscal year is the calendar year; CBWC fiscal year ends June", chart: "m10_01, m10_02", note: "B3" });

  // 20 documents
  S("Closing");
  s = D.headlineSlide(pres, "The FY24–25 audits, the TCP agreements and the FY25 gala calendar would sharpen every number in this deck.", "Closing");
  const third = (W - 2 * M - 0.6) / 3;
  [["FY24 and FY25 audited statements", ["**Resolves the ceilings-vs-recognized question (~$1M a year).", "Government revenue on the audit basis for the two latest years", "Whether single audits were filed"]],
   ["TCP subgrant agreements FY2023–FY2026", ["**Resolves the DHS contract values and the Sisters Rise / EHV status.", "Renewal terms for the largest single stream", "Draw-down terms and schedules"]],
   ["FY25 event calendar and CRM notes", ["**Resolves whether the gala moved across the fiscal year.", "Cash vs in-kind in the corporate relationships (MGAC, Capital One, IMF)", "Lapsed funders' gifts routed through DAFs"]],
  ].forEach(([t, lines], i) => D.card(s, { x: M + i * (third + 0.3), y: BODY_Y, w: third, h: 2.6, title: t, lines, fontSize: 13 }));
  D.bumper(s, "with these three documents the government picture rests on Calvary's own numbers rather than on public reconstruction.");
  D.footnote(s, { source: "discoveries_log.md (flags D1–D3) and open_questions.md part B from the data build", method: "each document maps to a flag raised during the analysis", chart: "m2_02, m2_03, m1_06" });

  // 21 next steps (status pattern: done / next / decisions needed)
  s = D.headlineSlide(pres, "The next steps are your reactions, the three documents, and a working session that turns Tier 1 into assignments.", "Closing");
  [["What has been done", ["Ten analysis modules on 25 public-record tables", "Verdict, scored pipeline (182 rows), 90-day plan, expansion options", "Every figure traced to a chart-data file and a public source"]],
   ["What comes next", ["Week 1: leadership reactions to the framing, targets and options", "Week 2: the three documents", "Week 3: working session to assign Tier 1 owners and dates", "Day 30 / 45 / 60–90 milestones from the action plan"]],
   ["Decisions needed from you", ["Adopt (or adjust) the verdict framing and the $3M / 50% target", "Confirm the Tier 1 list and owners", "Pick two expansion options to scope", "Adopt a reserve target and the advocacy calendar"]],
  ].forEach(([t, lines], i) => D.card(s, { x: M + i * (third + 0.3), y: BODY_Y, w: third, h: 2.8, title: t, lines, fontSize: 13 }));
  D.bumper(s, "nothing here is final until Calvary's team has weighed it, and the consulting team keeps the pipeline and charts current as decisions land.");
  D.footnote(s, { source: "recommendations/action_plan_90day.csv", method: "deadlines are relative to the start of the plan", chart: "m7_01" });

  // 22 appendix pointer
  s = D.headlineSlide(pres, "Every figure traces to a chart-data file and a public source, and the consulting and appendix decks carry the methods.", "Closing");
  D.bullets(s, [
    "Consulting deck: 55 slides with every module, method and the complete scored pipeline.",
    "Appendix A: Calvary and government funding. Appendix B: peers and named comparators. Appendix C: funders, gaps, network and pipeline. Appendix D: data and methods (method notes A1–D3).",
    "Reports: executive summary, full findings, methodology, recommendations; board talking points and consulting briefing.",
    "Every chart ID (e.g., m2_02) is a CSV in chart_data/ whose source IDs point to the public documents in the source registry; scoring weights live in config/scoring_weights.yaml.",
    `Data as of ${D.AS_OF}. Core peers are provisional; FY24–25 government figures rest on the 990 until the audits are shared.`,
  ], { fontSize: 15.5, h: BODY_H });
  D.footnote(s, { source: "calvary_analysis/README.md", method: "traceability checked by scripts/lib/trace.py", chart: "all" });

  fitTitles(pres);
  await D.finish(pres, path.join(__dirname, "leadership_deck.pptx"));
})();
