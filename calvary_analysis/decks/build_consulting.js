// Consulting team deck: 55 slides following storylines/consulting_headline_spine.md and consulting_storyline.md.
const D = require("./lib/deck");
const { HEX, M, W, BODY_Y, BODY_H } = D;
const path = require("path");
const CHART_W = 8.0, CARD_X = M + CHART_W + 0.3, CARD_W = W - M - CARD_X;
const tc = (s) => String(s).replace(/\b\w+/g, w => w[0] + w.slice(1).toLowerCase()).replace(/ Inc\b/g, "").replace(/'S\b/g, "'s");
// Visual-QA helpers: word-boundary truncation with an ellipsis; headline size step-down so long titles stay on two lines;
// negative value-axis floor for charts with negative values (lib chart() pins the minimum at 0); PNG aspect for centering.
const fs = require("fs");
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
function valMin(slide, v) { slide._slideObjects.filter(o => o._type === "chart").forEach(o => { o.options.valAxisMinVal = v; o.options.catAxisLabelPos = "low"; }); }
function pngRatio(file) { try { const b = fs.readFileSync(path.join(__dirname, "..", "charts", `${file}.png`)); return b.readUInt32BE(16) / b.readUInt32BE(20); } catch (e) { return 1.5; } }
function policyLabel(r) {
  const when = r.event_date ? String(r.event_date).slice(0, 7) : `FY${r.fiscal_year}`;
  let d = String(r.description);
  const m = d.match(/approved \(all funds\): (\S+) (.+?) \(as printed/);
  if (m) d = `${m[1]} ${m[2].toLowerCase().replace(/(^|[\s(-])\w/g, c => c.toUpperCase())}`;
  d = d.replace(/\s*\[.*$/, "").replace(/^Enhance: /, "");
  return `${when} ${r.event_type.replace("budget_", "")}: ${trunc(d, 50)}`;
}

(async () => {
  const { pres } = D.newDeck("Calvary funding analysis: consulting team deck", "Consulting deep dive");
  const SEC = (t, takeaway) => { pres.addSection({ title: t }); if (takeaway) D.sectionSlide(pres, t, takeaway, t); return t; };
  // helpers
  function pngSlide(sec, headline, png, cardTitle, lines, foot, { wide = 0.4 } = {}) {
    const s = D.headlineSlide(pres, headline, sec);
    if (lines) D.image(s, png, { x: M, y: BODY_Y, w: CHART_W + wide, h: BODY_H });
    else { const ih = 5.0, iw = Math.min(W - 2 * M, ih * pngRatio(png)); D.image(s, png, { x: (W - iw) / 2, y: BODY_Y - 0.05, w: iw, h: ih }); }
    if (lines) D.card(s, { x: CARD_X + wide, y: BODY_Y, w: CARD_W - wide, h: BODY_H, title: cardTitle, lines, fontSize: 11.5 });
    D.footnote(s, foot); return s;
  }
  function natSlide(sec, headline, spec, cardTitle, lines, foot) {
    const s = D.headlineSlide(pres, headline, sec);
    D.chart(s, spec.type || "bar", spec.labels, spec.series, Object.assign({ x: M, y: BODY_Y, w: CHART_W, h: BODY_H }, spec.opts || {}));
    if (lines) D.card(s, { x: CARD_X, y: BODY_Y, w: CARD_W, h: BODY_H, title: cardTitle, lines, fontSize: 11.5 });
    D.footnote(s, foot); return s;
  }
  function tableSlide(sec, headline, header, rows, colW, foot, { rowsPerSlide = 12, fontSize = 9.5 } = {}) {
    D.table(pres, sec, headline, header, rows, { colW, rowsPerSlide, fontSize, foot });
  }

  // ---------------- 1. Scope and method
  let sec = "1. Scope and method";
  pres.addSection({ title: sec });
  D.titleSlide(pres, "Calvary funding analysis: consulting team deck", "This analysis answers two questions for Calvary: how much pressure its government reliance creates, and which other funding fits. Full methods, evidence and the complete pipeline.", sec);
  tableSlide(sec, "The analysis rests on 25 public-record tables, with every row carrying a source and a retrieval date.",
    ["Table", "Grain", "Rows", "Main sources"], [
      ["fact_org_financials", "org × fiscal year × source", "150,461", "IRS 990 e-file XML (GivingTuesday), NCCS, IRS SOI, ProPublica, Calvary audits and 990 PDFs"],
      ["fact_grants", "grant record", "928,658", "990-PF grants paid, Schedule I (DMV funders, DAF sponsors filtered to DC/MD/VA), CRM export, annual reports, web lists"],
      ["fact_gov_awards", "award / subaward / expenditure", "40,300", "USAspending, FAC single audits, Calvary SEFA, Treasury SLFRF, DC OVSJG, DC Council oversight, DC PASS, HUD CoC"],
      ["fact_policy_events", "dated budget or policy change", "297", "DC budget books FY2024–FY2027, Council committee reports, Budget Support Act"],
      ["fact_opportunities", "open or forecast opportunity", "286", "Grants.gov"],
      ["fact_roles / dim_person", "person × org × year", "163,473 / 48,563", "990 Part VII, 990-EZ, 990-PF officers, Calvary annual reports (roles only)"],
      ["fact_org_relationships", "org pair × type × year", "544,041", "grants, DAF grants, pass-through, Schedule R, shared board members (confidence-rated)"],
      ["dim_org / dim_funder / dim_universe_membership", "organization / funder / universe rule", "105,189 / 8,928 / 17,210", "IRS BMF, e-file index, config rules"],
      ["dim_geo / dim_period", "ward, tract, county / year", "246 / 28", "ACS 2020–24, DC MAR, CPI-U"],
      ["supp_* (7 tables)", "various", "—", "HUD PIT/HIC, DC budget lines, Calvary program metrics, strategic targets, donor bands, CRM verification"],
    ], [3.0, 2.3, 1.6, 5.2], { source: "calvary_funding_data/README.md, reports/data_inventory.md, reports/data_quality.md", method: "Prompt 1 data build, QC'd and rebuild-tested; see appendix D", chart: "input_map", note: "D2" });
  tableSlide(sec, "Calvary is compared with 18 provisional DC-area peers, two Los Angeles comparators, and three universes of 163 to 542 organizations.",
    ["Universe", "Size", "Definition", "Used for"], [
      ["calvary", "1", "The subject organization", "All modules"],
      ["core_peers (provisional)", "18", "DC-area organizations serving homeless women, DV survivors, recovery; four tiers (DC women/homeless; DC DV; DC homeless/recovery and Ward 7/8; DMV women/DV)", "M3, M5, M6, M7"],
      ["named_comparators", "2", "Downtown Women's Center (LA) and the CBWC Empowerment Institute / SheWorks (LA), at the CEO's request", "Reference rows everywhere; M10"],
      ["dc_sector", "1,027", "DC public charities in homelessness, housing, DV, human services and adjacent NTEE codes", "M3 distributions; M4 landscape lens A"],
      ["size_matched", "566", "National shelter / DV / women's-center organizations with revenue 0.5–2× Calvary's", "M3 distributions"],
      ["national_women", "2,878", "National DV shelters, women's centers, women-named homeless/housing organizations", "M3 distributions"],
      ["dmv_funders", "7,705", "DC/MD/VA private foundations and grantmaking public charities", "M4–M7"],
      ["daf_sponsors", "15", "National DAF sponsors, Schedule I kept for DC/MD/VA recipients", "M4 (channel), excluded from the pipeline"],
    ], [2.4, 0.9, 5.6, 3.2], { source: "dim_universe_membership; config/universes.yaml; config/core_peers.csv", method: "rules in reports/universe_summary.md; peers swapped by editing core_peers.csv and rerunning", chart: "universe_summary", note: "D2" });
  const gs = D.readCsv("m1_03_gov_share_two_measures");
  natSlide(sec, "Government share uses the audit basis where audits exist, because the 990 line understated Calvary's contracts by $1.5M in FY21.",
    { type: "line", labels: gs.map(r => r.fy_label), series: [{ name: "Audit basis", values: gs.map(r => D.num(r.gov_share_audit)), color: HEX.government }, { name: "990 line 1e", values: gs.map(r => D.num(r.gov_share_line_1e)), color: HEX.peer }], opts: { valFmt: "0%", valMax: 0.8 } },
    "Measure choice", ["Audits FY13–FY23 report government contracts and grants together; the 990 line 1e reports government grants only.", "FY21: audit $1.98M vs line 1e $503K (contracts booked in line 1f).", "FY22 and FY23: identical on both measures, so FY24–25 line 1e is treated as audit-equivalent.", "Peers are compared on line 1e, the only measure available for them."],
    { source: "Calvary audited financial statements FY13–FY23 and IRS 990 returns, fact_org_financials", method: "share = government revenue ÷ total revenue on each basis", chart: "m1_03", note: "A1" });
  tableSlide(sec, "The limitations are known and bounded, from missing FY24–25 audits and one-year DHS values to partial filings and provisional peers.",
    ["Limitation", "Effect", "Mitigation"], [
      ["No public FY24/FY25 audits", "Government share for the two latest years rests on 990 line 1e", "Line 1e matched audits in FY22–23; ceilings-vs-recognized cross-check (A5); audits requested"],
      ["DHS/TCP contract values public for FY2024 only", "Award base understated in other years; scenario baseline carries FY2024 forward", "Flagged in every chart; TCP agreements requested"],
      ["TY2024 foundation filings partial, TY2025 mostly unfiled", "Recent private trends understated", "TY2020–23 as the trend window; TY2024 labeled 'arriving'"],
      ["'See attached' grant lists (667 rows, ~$3.5B DMV-wide)", "Some funders' grants have no recipient names", "Flagged per funder; accessibility penalty in scoring"],
      ["Provisional core peers", "Ranks move if the set changes", "Sector percentiles reported alongside; swap via config"],
      ["Interlock name matching", "Medium-confidence links may be different people", "Leadership materials use high confidence only; medium labeled unconfirmed"],
      ["Corporate giving without a foundation", "Invisible in filings", "CRM reconciliation; corporate track scored by analyst"],
    ], [3.4, 4.2, 4.5], { source: "reports/data_quality.md; module readouts (Caveats)", method: "each limitation maps to a mitigation used in the analysis", chart: "—", note: "D3" });

  // ---------------- 2. Calvary's trajectory
  sec = SEC("2. Calvary's trajectory", "Calvary grew on public partners; private giving held steady; FY25 thinned the cushion.");
  const rv = D.readCsv("m1_01_revenue_expenses");
  natSlide(sec, "Calvary's revenue grew 59% in real terms from FY19 to FY25, and the FY22 spike was a one-time building award.",
    { type: "line", labels: rv.map(r => r.fy_label), series: [{ name: "Revenue (2024 $)", values: rv.map(r => D.num(r.total_revenue_real_2024)), color: HEX.government }, { name: "Revenue (nominal)", values: rv.map(r => D.num(r.total_revenue)), color: HEX.peer }, { name: "Expenses (2024 $)", values: rv.map(r => D.num(r.total_expenses_real_2024)), color: HEX.individuals }] },
    "Trajectory", ["$1.45M (FY11) → $4.97M (FY25) nominal; +59% real FY19→FY25.", "FY22: $8.87M including the $3.68M SLFRF award that bought the New Foundations building.", "Expenses passed revenue in FY23 and FY25."],
    { source: "IRS 990 returns FY2011–FY2025 (fact_org_financials), CPI-U (dim_period)", method: "2024 dollars via CPI-U annual average by fiscal-year-end year", chart: "m1_01", note: "A1" });
  const mix = D.readCsv("m1_02_revenue_mix");
  natSlide(sec, "Government supplied 40–61% of revenue every year since FY15 and most of the growth.",
    { labels: mix.map(r => r.fy_label), series: [{ name: "Government", values: mix.map(r => D.num(r.government)), color: HEX.government }, { name: "Private contributions ex events", values: mix.map(r => D.num(r.private_contributions_ex_events)), color: HEX.institutional }, { name: "Event contributions", values: mix.map(r => D.num(r.event_contributions)), color: HEX.individuals }, { name: "Other revenue", values: mix.map(r => Math.max(0, D.num(r.other_revenue) || 0)), color: HEX.other }], opts: { stacked: true } },
    "Mix", ["Government share by year: " + mix.map(r => `${r.fy_label} ${Math.round(D.num(r.gov_share) * 100)}%`).join(", ") + ".", "Private contributions ex events = contributions total − government − line 1c events (the 990 does not split foundations from individuals)."],
    { source: "Calvary audits FY15–FY23 (government revenue) and IRS 990 returns, fact_org_financials", method: "government on the audit basis to FY23, line 1e FY24–25", chart: "m1_02", note: "A1" });
  natSlide(sec, "The audit basis and the 990 line agree except in FY21, so the FY24–25 figures can be read as audit-equivalent.",
    { type: "line", labels: gs.map(r => r.fy_label), series: [{ name: "Audit basis", values: gs.map(r => D.num(r.gov_share_audit)), color: HEX.government }, { name: "990 line 1e", values: gs.map(r => D.num(r.gov_share_line_1e)), color: HEX.peer }], opts: { valFmt: "0%", valMax: 0.8 } },
    "Reconciliation", ["FY21 audit government revenue $1,981,161; line 1e $503,222; line 1f $3,063,099.", "FY22: both $5,685,504. FY23: both $2,460,897.", "FY24 line 1e $2,621,203 (45%); FY25 $2,892,598 (58%)."],
    { source: "fact_org_financials (audit rows and preferred 990 rows)", method: "see method note A1", chart: "m1_03", note: "A1" });
  const sd = D.readCsv("m1_04_surplus_deficit");
  valMin(natSlide(sec, "Calvary ran deficits in two of the last three years, and its cash cushion fell from 7.5 to 4.4 months.",
    { labels: sd.map(r => r.fy_label), series: [{ name: "Surplus / deficit", values: sd.map(r => D.num(r.surplus_deficit)), color: HEX.government }], opts: { dataLabels: true, showLegend: false } },
    "Margin and cash", ["FY23 −$674K; FY24 +$507K; FY25 −$607K.", "Months of cash: " + sd.filter(r => D.num(r.months_of_cash) != null).slice(-6).map(r => `${r.fy_label} ${D.num(r.months_of_cash).toFixed(1)}`).join(", ") + ".", "Net assets $8.1M at FY25, mostly the building."],
    { source: "IRS 990 returns, fact_org_financials", method: "surplus = total revenue − total expenses; months of cash = cash and savings ÷ monthly expenses", chart: "m1_04, m1_05", note: "A1" }), -1000000);
  const ev = D.readCsv("m1_06_events");
  natSlide(sec, "Event contributions fell from $538K to $55K in FY25 while net event income turned positive, which suggests a calendar change.",
    { labels: ev.map(r => r.fy_label), series: [{ name: "Event contributions (line 1c)", values: ev.map(r => D.num(r.event_contributions_line_1c)), color: HEX.individuals }, { name: "Net special-event income (line 8c)", values: ev.map(r => D.num(r.special_events_net)), color: HEX.text2 }], opts: { valFmt: "$#,##0,\"K\"" } },
    "Flag D3", ["Line 1c: $458K (FY23), $538K (FY24), $55K (FY25).", "Line 8c net: negative every year through FY24, +$219K in FY25.", "Ask Calvary whether the FY25 gala moved across the fiscal-year line."],
    { source: "IRS 990 Part VIII lines 1c and 8c, fact_org_financials", method: "as reported", chart: "m1_06", note: "A1" });
  const fc = D.readCsv("m1_07_calvary_funder_concentration").slice(0, 12).reverse();
  natSlide(sec, "Filed institutional grants stayed near $1M a year from 26–29 funders, and GWCF supplied 27% of five years' total.",
    { labels: fc.map(r => trunc(tc(r.funder_name), 44)), series: [{ name: "Filed grants TY2020–24", values: fc.map(r => D.num(r.amount)), color: HEX.institutional }], opts: { barDir: "bar", valFmt: "$#,##0,\"K\"", dataLabels: true, showLegend: false, catFontSize: 8 } },
    "Concentration", ["$4.43M from 50 funders TY2020–24; institutional $3.34M, DAF sponsors $1.09M.", "GWCF 27%, top five 63%; HHI 1,168.", "By year: TY2020 $637K (27 funders) … TY2024 $1.17M (26), partial."],
    { source: "Funders' 990-PF / Schedule I rows naming Calvary, fact_grants; dim_funder", method: "non-cumulative rows, aggregated by funder EIN", chart: "m1_07, m1_08", note: "A3" });

  // ---------------- 3. Government exposure
  sec = SEC("3. Government exposure", "Three streams, one hub, stable pools with annual threats, and a draw-down question.");
  const sm = D.readCsv("m2_01_stream_map"); const yrs = [...new Set(sm.map(r => r.fiscal_year))].sort();
  const streams = ["OVSJG (DC local)", "HUD CoC via TCP (federal)", "DHS via TCP (DC local)", "Other federal pass-through"]; const scol = [HEX.government, HEX.daf, HEX.institutional, HEX.other];
  natSlide(sec, "Calvary's recurring government awards grew from $0.9M (2019) to $4.1M (2024) across OVSJG, HUD CoC and DHS via TCP.",
    { labels: yrs, series: streams.map((st, i) => ({ name: st, color: scol[i], values: yrs.map(y => sm.filter(r => r.stream === st && r.fiscal_year === y).reduce((a, r) => a + (D.num(r.amount) || 0), 0)) })), opts: { stacked: true } },
    "Streams", ["OVSJG recurring: $369K (FY20) → $1.05M (FY26).", "HUD CoC: $240K (2019) → $1.77M (FY2025).", "DHS/TCP: $1.42M (FY2024 only).", "One-time: SLFRF $3.68M, PPP $327K, HUD CPF $200K."],
    { source: "fact_gov_awards: dc_ovsjg, hud_coc, dc_oversight, audit_sefa rows for Calvary", method: "one source per stream; DC FY for OVSJG/DHS, HUD competition year for CoC", chart: "m2_01, m2_01b", note: "A2" });
  const dur = D.readCsv("m2_03_stream_durability");
  tableSlide(sec, "Seven streams carry different renewal risks, and the DHS contract and Sisters Rise are the least documented and the riskiest.",
    ["Stream", "First → latest", "Funding source", "Renewal mechanism", "Durability risk"], dur.map(r => [r.detail, `${D.fmtK(D.num(r.first_amount))} (${r.first_year}) → ${D.fmtK(D.num(r.latest_amount))} (${r.latest_year})`, r.funding_source, r.renewal_mechanism, r.durability_risk]),
    [2.3, 1.9, 2.4, 2.6, 2.9], { source: "fact_gov_awards, fact_policy_events, supp_hic_projects", method: "risk ratings are analyst judgment (basis = inferred)", chart: "m2_03", note: "A2" }, { rowsPerSlide: 8, fontSize: 8.5 });
  const cv = D.readCsv("m2_02_ceilings_vs_recognized").filter(r => ["FY24", "FY25"].includes(r.fy_label));
  natSlide(sec, "Calvary recognized 73% (FY24) and 67% (FY25) of its known award ceilings as revenue, a gap the audits would explain.",
    { labels: cv.map(r => r.fy_label), series: [{ name: "OVSJG awards", values: cv.map(r => D.num(r.ovsjg_award)), color: HEX.government }, { name: "HUD CoC (lagged)", values: cv.map(r => D.num(r.coc_award_lagged)), color: HEX.daf }, { name: "DHS/TCP (FY24 carried)", values: cv.map(r => D.num(r.dhs_award)), color: HEX.institutional }, { name: "Other federal", values: cv.map(r => D.num(r.other_federal)), color: HEX.other }], opts: { stacked: true } },
    "Ceilings vs recognized", ["FY24 ceilings $3.60M vs recognized $2.62M (73%).", "FY25 ceilings $4.29M vs $2.89M (67%).", "Flag D1: timing, draw rates, cost-reimbursement limits, or an overstated DHS carry-forward.", "Recognized revenue is the grey bar on the leadership slide; here the ceilings are stacked by stream."],
    { source: "fact_gov_awards aligned to Calvary FY; fact_org_financials", method: "CoC competition year t → Calvary FY t+1; DHS FY2024 carried forward; EFSP/SNAP at audited FY23 level", chart: "m2_02", note: "A5" });
  pngSlide(sec, "Since pandemic money ended, DC's homeless, PSH and victim-services budgets have held flat to rising through FY2027.", "m2_04_dc_budget_context", "Budget lines",
    ["OVSJG P02303 approved: $45.5M FY24, $55.9M FY25, $55.4M FY26, $55.3M FY27; actual $41.3M FY24, $47.9M FY25.", "DHS continuum $170M → $206M → $194M; PSH $153M → $145M → $148M → $166M.", "DV services $2.9–3.4M, cut proposed and restored twice."],
    { source: "supp_dc_budget_lines (DC budget books FY2024–FY2027, Council committee reports)", method: "activity-level totals by program code", chart: "m2_04", note: "A6" });
  const pe = D.readCsv("m2_06_policy_timeline");
  valMin(natSlide(sec, "The Mayor proposed victim-services and DV cuts in each of the last two springs, and the Council restored them.",
    { labels: pe.filter(r => Math.abs(D.num(r.amount_change)) >= 2e6).slice(-12).map(policyLabel), series: [{ name: "Change", values: pe.filter(r => Math.abs(D.num(r.amount_change)) >= 2e6).slice(-12).map(r => D.num(r.amount_change)), color: HEX.government }], opts: { barDir: "bar", valFmt: "$#,##0,,\"M\"", dataLabels: true, showLegend: false, catFontSize: 7 } },
    "Pattern", ["FY26: Mayor −$5.8M to Victim Services grants; Council +$3.5M committee and +$6.0M one-time enhancement.", "FY27: Mayor −$5.6M; Council restored.", "DHS DV services −$500K proposed in both years; restored.", "OVSJG under-spend vs approved is the quieter risk."],
    { source: "fact_policy_events (DC budget books, Council committee reports)", method: "events of $2M or more touching the homeless continuum, PSH, DV and victim-services lines", chart: "m2_06", note: "A6" }), -20000000);
  const sh = D.readCsv("m2_05_pool_shares").filter(r => D.num(r.ovsjg_share) != null);
  natSlide(sec, "Calvary holds about 1% of OVSJG awards and 5% of DC's CoC awards, so growth comes from winning projects.",
    { type: "line", labels: sh.map(r => r.fiscal_year), series: [{ name: "Share of DC CoC awards", values: sh.map(r => D.num(r.coc_share)), color: HEX.daf }, { name: "Share of OVSJG awards", values: sh.map(r => D.num(r.ovsjg_share)), color: HEX.government }], opts: { valFmt: "0.0%", valMax: 0.07 } },
    "Pools", ["OVSJG total awards $47M (FY20) → $97M (FY26); Calvary 0.7–1.5% (4.6% in FY22 with the building award).", "DC CoC awards $22M (2019) → $33.5M (FY2025); Calvary 1.1% → 5.3%."],
    { source: "fact_gov_awards: OVSJG award lists (all recipients) and HUD CoC awards (DC-500)", method: "Calvary ÷ pool total by year", chart: "m2_05", note: "A2" });
  const sc = D.readCsv("m2_07_scenarios"); const sp = Object.fromEntries(D.readCsv("m2_07_scenario_parameters").map(r => [r.parameter, D.num(r.value)]));
  tableSlide(sec, "OVSJG cuts cost $67–168K, a lost CoC project $366K, a lost DHS/TCP contract $960K, and the combined case $1.31M.",
    ["Scenario", "Revenue loss", "% revenue", "Deficit gross", "Deficit net (50% cost avoidance)", "Months of cash after 12m (net)", "Months to zero cash (net)"],
    sc.map(r => [r.scenario, r.scenario_id === "S0" ? "–" : `−${D.fmtK(D.num(r.revenue_loss))}`, r.scenario_id === "S0" ? "–" : D.fmtPct(D.num(r.loss_pct_of_total_revenue)), `−${D.fmtK(-D.num(r.deficit_gross))}`, `−${D.fmtK(-D.num(r.deficit_net_of_cost_avoidance))}`, D.num(r.months_of_cash_after_12m_net).toFixed(1), Number.isFinite(D.num(r.months_until_cash_zero_net)) ? D.num(r.months_until_cash_zero_net).toFixed(0) : "—"]),
    [3.4, 1.4, 1.1, 1.5, 1.9, 1.5, 1.3], { source: "fact_gov_awards, fact_org_financials; config/scenarios.yaml", method: `baseline FY25: revenue ${D.fmtM(sp.total_revenue, 2)}, expenses ${D.fmtM(sp.total_expenses, 2)}, cash ${D.fmtM(sp.cash_eoy, 2)}, government ${D.fmtM(sp.recognized_gov_revenue, 2)}; apportioned OVSJG ${D.fmtK(sp.alloc_ovsjg)}, CoC ${D.fmtK(sp.alloc_coc)}, DHS ${D.fmtK(sp.alloc_dhs)}`, chart: "m2_07", note: "A4" }, { fontSize: 9 });

  // ---------------- 4. Peers
  sec = SEC("4. Peer benchmarking", "Calvary is mid-pack on government share, fast on growth, average on cash, and above most peers on institutional depth.");
  const bt = D.readCsv("m3_00_benchmark_table");
  const bg = bt.filter(r => D.num(r.gov_share_fy2022_24_mean) != null).sort((a, b) => D.num(a.gov_share_fy2022_24_mean) - D.num(b.gov_share_fy2022_24_mean));
  natSlide(sec, "Calvary's 53% government share ranks 11th of 19 DC-area organizations, below every DC DV provider and above the philanthropy-led models.",
    { labels: bg.map(r => r.org), series: [{ name: "Government share FY22–24 mean", values: bg.map(r => D.num(r.gov_share_fy2022_24_mean)), color: HEX.government }], opts: { barDir: "bar", valFmt: "0%", dataLabels: true, showLegend: false, catFontSize: 8 } },
    "Typology", ["Government-anchored (≥65%): DC SAFE, Open Arms, My Sister's Place, Everyone Home DC, Heartly House, DASH, CBWC Institute.", "Mixed (35–65%): Coalition, House of Ruth MD, DWC, New Endeavors, House of Ruth DC, Calvary, Covenant House, Doorways, Samaritan Inns, N Street Village, Community of Hope.", "Philanthropy-led (<35%): Christ House, Thrive DC, Miriam's Kitchen."],
    { source: "fact_org_financials (990 line 1e; Calvary audit basis FY22–23)", method: "FY2022–24 mean; provisional peers; LA comparators as reference", chart: "m3_01", note: "B1" });
  pngSlide(sec, "Against the broader sector Calvary is typical, at the 57th percentile in DC and the 46th among national women's organizations.", "m3_07_sector_distributions", "Distributions",
    ["DC sector FY2023 (n=163): median 37%, Calvary 51% (57th percentile).", "Size-matched national FY2022 (n=334): median 56%, Calvary 61% (57th).", "National women's/DV FY2022 (n=542): median 65%, Calvary 61% (46th)."],
    { source: "fact_org_financials by universe (dim_universe_membership)", method: "organizations with no government line counted at 0%", chart: "m3_07", note: "B1" }, { wide: 0.2 });
  pngSlide(sec, "Peers grew past $10M with government (DWC, House of Ruth) or almost without it (Miriam's Kitchen), so size requires neither.", "m3_02_size_vs_gov_share", null, null,
    { source: "fact_org_financials: FY2024 revenue and FY2022–24 government share", method: "log revenue axis; typology bands shaded", chart: "m3_02", note: "B1" }, { wide: 4.0 });
  const bgr = bt.filter(r => D.num(r.real_cagr_fy2019_24) != null).sort((a, b) => D.num(a.real_cagr_fy2019_24) - D.num(b.real_cagr_fy2019_24));
  valMin(natSlide(sec, "Calvary's real growth of 13.8% a year since FY19 trails only My Sister's Place, DWC and DC SAFE among peers.",
    { labels: bgr.map(r => r.org), series: [{ name: "Real CAGR FY2019–24", values: bgr.map(r => D.num(r.real_cagr_fy2019_24)), color: HEX.government }], opts: { barDir: "bar", valFmt: "0.0%", dataLabels: true, showLegend: false, catFontSize: 8 } },
    "Growth", ["Endpoints FY2019 and FY2024 avoid Calvary's one-time FY22 award.", "CBWC Institute omitted (founded 2022)."],
    { source: "fact_org_financials, dim_period CPI-U", method: "compound annual growth of 2024-dollar revenue", chart: "m3_03", note: "B1" }), -0.1);
  const bc = bt.filter(r => D.num(r.months_of_cash_fy2024) != null).sort((a, b) => D.num(a.months_of_cash_fy2024) - D.num(b.months_of_cash_fy2024));
  natSlide(sec, "Calvary's 5.2 months of cash in FY24 is mid-pack, between DV providers at one month and Doorways at twelve.",
    { labels: bc.map(r => r.org), series: [{ name: "Months of cash FY2024", values: bc.map(r => D.num(r.months_of_cash_fy2024)), color: HEX.government }], opts: { barDir: "bar", valFmt: "0.0", dataLabels: true, showLegend: false, catFontSize: 8 } },
    "Liquidity", ["Calvary 5.2 (FY24), 4.4 (FY25).", "DC SAFE 0.9, Heartly House 1.0, New Endeavors 0.5, Covenant House 1.1.", "Doorways 12.1, Everyone Home DC 9.9, N Street Village 8.0."],
    { source: "fact_org_financials: cash_savings_eoy, total_expenses", method: "cash and savings ÷ monthly expenses", chart: "m3_04", note: "B1" });
  pngSlide(sec, "Most peers' government share has held since 2017, except Samaritan Inns (down) and DWC and House of Ruth MD (up).", "m3_05_gov_share_trajectories", null, null,
    { source: "fact_org_financials (990 line 1e; Calvary audit basis FY17–23)", method: "small multiples, one organization per panel", chart: "m3_05", note: "B1" }, { wide: 4.0 });
  const bi = bt.filter(r => D.num(r.institutional_per_revenue_dollar) != null).sort((a, b) => D.num(a.institutional_per_revenue_dollar) - D.num(b.institutional_per_revenue_dollar));
  natSlide(sec, "Calvary's institutional grants equal 12% of revenue, above all peers except Samaritan Inns, so the headroom is depth per funder.",
    { labels: bi.map(r => `${r.org} (${Math.round(D.num(r.institutional_funders))} funders)`), series: [{ name: "Institutional grants ÷ revenue 2020–24", values: bi.map(r => D.num(r.institutional_per_revenue_dollar)), color: HEX.institutional }], opts: { barDir: "bar", valFmt: "0%", dataLabels: true, showLegend: false, catFontSize: 8 } },
    "Depth and DAF share", ["Calvary 12% with 42 funders; Samaritan Inns 27% with 14.", "DAF share of filed grants: Calvary 25%; N Street Village 51%; Miriam's Kitchen 41%; House of Ruth DC 37%; Doorways 42%.", "DMV funders' filings only; LA comparators not comparable."],
    { source: "fact_grants, dim_funder, fact_org_financials", method: "institutional = non-DAF funders; dollars ÷ FY2020–24 revenue", chart: "m3_06", note: "B2" });
  pngSlide(sec, "Peers show three replicable paths: replacing government with program revenue, growing private alongside it, or scaling with it.", "m3_08_case_studies_mix", null, null,
    { source: "fact_org_financials (990 preferred rows; government = line 1e)", method: "revenue mix by year for four organizations", chart: "m3_08", note: "B1" }, { wide: 4.0 });
  const pools = D.readCsv("m3_09_peer_pools");
  natSlide(sec, "The DV peers draw $3–5M a year each from OVSJG, while Calvary's $1.05M makes it a mid-sized grantee.",
    { labels: pools.map(r => r.org), series: [{ name: "OVSJG awards DC FY2026", values: pools.map(r => D.num(r.ovsjg_fy2026)), color: HEX.government }, { name: "HUD CoC awards FY2025", values: pools.map(r => D.num(r.hud_coc_fy2025)), color: HEX.daf }], opts: { barDir: "bar", dataLabels: true, catFontSize: 8 } },
    "Shared pools", ["OVSJG FY2026: DASH $5.28M, DC SAFE $4.61M, My Sister's Place $3.81M, House of Ruth DC $3.17M, Calvary $1.05M.", "CoC FY2025: Christ House $2.98M, My Sister's Place $2.06M, Calvary $1.77M, House of Ruth DC $1.38M, DASH $1.38M."],
    { source: "fact_gov_awards: OVSJG FY2026 list; HUD CoC FY2025 awards", method: "DC pools only", chart: "m3_09", note: "A2" });

  // ---------------- 5. Landscape and gaps
  sec = SEC("5. Funder landscape and gaps", "A large, concentrated pool; most majors already fund Calvary; the gaps are specific and named.");
  const by = D.readCsv("m4_01_dc_sector_by_year");
  natSlide(sec, "DMV funders put about $132M a year into DC's homelessness and human-services organizations, 58% of it through donor-advised funds.",
    { labels: by.map(r => `TY${Math.round(D.num(r.tax_year))}`), series: [{ name: "Institutional funders", values: by.map(r => D.num(r.institutional_and_other)), color: HEX.institutional }, { name: "DAF sponsors", values: by.map(r => D.num(r.daf_sponsors)), color: HEX.daf }], opts: { stacked: true } },
    "Lens A", ["$660M TY2020–24 to 1,027 dc_sector organizations; 555 institutional funders.", "Institutional dollars $50–52M/yr TY2020–23, $72M in TY2024 (partial filings).", "Excludes Gates (global/research recipients) and TCP (pass-through): config/landscape_exclusions.csv."],
    { source: "fact_grants (990-PF / Schedule I TY2020–24) to dc_sector recipients; dim_funder", method: "funder tax years; TY2024 partial", chart: "m4_01, m4_02", note: "C1" });
  const lt = D.readCsv("m4_00_funder_landscape_table").slice(0, 20).reverse();
  natSlide(sec, "Ten institutional funders supply 55% of foundation dollars to DC's sector, and six of the 25 largest already fund Calvary.",
    { labels: lt.map(r => trunc(tc(r.funder_name), 40)), series: [{ name: "Dollars to DC sector TY2020–24", values: lt.map(r => D.num(r.dc_sector_amount)), color: HEX.institutional }], opts: { barDir: "bar", dataLabels: true, showLegend: false, catFontSize: 7.5 } },
    "Majors", ["Fund Calvary: GWCF, Cafritz, Bank of America, United Way NCA, Jane Bancroft Robinson, Abell.", "Do not: Clark ($32.8M, 20 DC orgs, 5 peers), JPMorgan Chase (matching), Wal-Mart, Casey, Weinberg, Morningstar, Diana Davis Spencer, Rast, Meyer, Capital Area Food Bank, Wells Fargo, Bernstein, PepsiCo, Washington Home.", "Top 10 = about half of institutional dollars (concentration curve in appendix C)."],
    { source: "fact_grants, dim_funder (landscape table m4_00)", method: "institutional = non-DAF; exclusions applied", chart: "m4_03, m4_04", note: "C1" });
  pngSlide(sec, "The typical foundation grant to a DC-sector organization is $10–25K, and six-figure grants are the top decile.", "m4_05_grant_size_by_type", "Grant size",
    ["Private foundations: median $10K, p90 $79K (n=3,288).", "Community foundations: median $40K, p90 $200K.", "DAF sponsors: median $25K, p90 $259K.", "Corporate foundations: median $1K (matching gifts), p90 $250K."],
    { source: "fact_grants to dc_sector recipients TY2020–24; dim_funder", method: "percentiles of grant size by funder type", chart: "m4_05", note: "C1" });
  const daf = D.readCsv("m4_06_daf_sponsors");
  natSlide(sec, "Fidelity Charitable alone moved $179M of donor-advised money into DC-sector organizations in five years.",
    { labels: daf.map(r => trunc(tc(r.funder_name), 44)), series: [{ name: "Grants to DC sector TY2020–24", values: daf.map(r => D.num(r.total)), color: HEX.daf }], opts: { barDir: "bar", dataLabels: true, showLegend: false, catFontSize: 8, valFmt: "$#,##0,,\"M\"", dataFmt: "$#,##0.0,,\"M\"" } },
    "DAF channel", ["DAF sponsors are intermediaries: the decisions sit with individual donors.", "Calvary's DAF receipts: $1.1M over five years (Benevity $512K, Fidelity $314K, Schwab $128K).", "Peers with Calvary's profile raise 40–50% of filed grants via DAFs."],
    { source: "fact_grants (DAF sponsors' Schedule I, DC/MD/VA recipients)", method: "by sponsor, TY2020–24", chart: "m4_06", note: "C1" });
  const pt = D.readCsv("m4_07_purpose_tags").filter(r => r.tag !== "other").slice(0, 10).reverse();
  natSlide(sec, "Most institutional money is general operating or untagged, and the largest mission-tagged funders are Maryland and Virginia foundations.",
    { labels: pt.map(r => r.tag.replace(/_/g, " ")), series: [{ name: "Institutional DC-sector dollars by purpose tag", values: pt.map(r => D.num(r.amount)), color: HEX.institutional }], opts: { barDir: "bar", dataLabels: true, showLegend: false } },
    "Purpose", ["'Other' (untagged) 47% of tagged dollars; general operating 20%; women 9%; housing 4%; DV smaller.", "Mission-tagged DMV funders: Weinberg, The Community Foundation (VA), Clark, Wells Fargo, Abell — most give little in DC (m4_08).", "Implication: target the DC general-support givers who already fund peers."],
    { source: "fact_grants purpose text tagged with dim_program_area keywords", method: "a grant can carry several tags", chart: "m4_07, m4_08", note: "C1" });
  const g1 = D.readCsv("m5_01_peer_funders_not_calvary").filter(r => D.num(r.peers_funded) >= 3).reverse();
  natSlide(sec, "Twenty-three institutional funders give to three or more of Calvary's peers but not Calvary, led by Clark Charitable.",
    { labels: g1.map(r => trunc(tc(r.funder_name), 34)), series: [{ name: "Core peers funded", values: g1.map(r => D.num(r.peers_funded)), color: HEX.institutional }], opts: { barDir: "bar", valFmt: "0", dataLabels: true, showLegend: false, catFontSize: 7.5, h: 4.75 } },
    "Gap list", ["All 23 filed itemized lists in TY2023+, so the absence is current.", "Venable (10 peers) and America's Charities (7) are in Calvary's CRM: filing lag.", "In-kind or workplace channels (Gifts for the Homeless, Capital Area Food Bank, Give Lively) are penalized in scoring.", "Appendix C lists all 75 funders of 2+ peers."],
    { source: "fact_grants (peers' and Calvary's filed grants TY2020–24), dim_funder", method: "no Calvary row in TY2020–24 filings; DAF sponsors excluded", chart: "m5_01", note: "C1" });
  const lp = D.readCsv("m5_02_lapsed_funders").filter(r => r.status.startsWith("lapsed")).reverse();
  natSlide(sec, "Twelve former funders that once gave $255K have filed grant lists since TY2023 with nothing for Calvary.",
    { labels: lp.map(r => `${trunc(tc(r.funder_name), 40)} (TY${Math.round(D.num(r.first_ty))}–${Math.round(D.num(r.last_ty))})`), series: [{ name: "Historic total to Calvary", values: lp.map(r => D.num(r.total)), color: HEX.individuals }], opts: { barDir: "bar", valFmt: "$#,##0,\"K\"", dataLabels: true, showLegend: false, catFontSize: 7.5 } },
    "Lapsed", ["World Bank CCF $100K (TY2022), Many Hands $55.5K (TY2020), Jane Bancroft Robinson $25K, Robert M. Fisher $25K, Junior League $15K …", "Max & Victoria Dreyfus unclear (no itemized TY2023+ return in the data).", "Check the CRM for gifts routed through DAFs before outreach."],
    { source: "fact_grants (all years naming Calvary; funders' TY2023+ returns)", method: "lapsed = last grant ≤TY2022 and funder itemized since", chart: "m5_02", note: "C1" });
  const hd = D.readCsv("m5_03_current_funder_headroom").filter(r => D.num(r.headroom_to_max_peer_grant) >= 5000 && D.num(r.calvary_max) >= 1000).slice(0, 10).reverse();
  natSlide(sec, "Fifteen of Calvary's current funders have written larger single grants to a peer than to Calvary.",
    { labels: hd.map(r => trunc(tc(r.funder_name), 42)), series: [{ name: "Largest grant to Calvary", values: hd.map(r => D.num(r.calvary_max)), color: HEX.government }, { name: "Largest grant to a core peer", values: hd.map(r => D.num(r.max_peer_grant)), color: HEX.peer }], opts: { barDir: "bar", valFmt: "$#,##0,\"K\"", dataLabels: true, catFontSize: 8 } },
    "Headroom", ["Cafritz $170K vs $250K; GWCF $458K vs $526K; Bank of America $15K vs $50K; United Way NCA $23K vs $56K; Fowler $40K vs $50K; Ludwig $25K vs $50K.", "A peer's larger grant may be capital or program-specific."],
    { source: "fact_grants TY2020–24", method: "largest single grants, not totals", chart: "m5_03", note: "C1" });
  const cr = D.readCsv("m5_06_crm_reconciliation");
  natSlide(sec, "Only 44% of the CRM's $10.6M in 2023–26 institutional giving is verifiable in funders' filings.",
    { labels: cr.map(r => r.status.replace(/_/g, " ")), series: [{ name: "CRM total by verification status", values: cr.map(r => D.num(r.crm_total)), color: HEX.institutional }], opts: { barDir: "bar", dataLabels: true, showLegend: false } },
    "CRM vs filings", ["Confirmed in TY2023+ filings: $4.63M, 25 funders.", "Corporate / no public filing: $2.55M, 92 funders (MGAC, IMF, Latham, Frontier Co-op, Reservoir).", "'See attached' filers: $1.28M (Philip L. Graham, Clark-Winchcole, Kay, Herb Block).", "Exempt filers with no Calvary row: $1.61M; earlier-only: $0.48M."],
    { source: "supp_crm_cash_verification (Calvary CRM export 2023–26 vs funders' filings)", method: "CRM totals cumulative over an unconfirmed window (assumptions A1–A2 of the data build)", chart: "m5_06", note: "C1" });

  // ---------------- 6. Network
  sec = SEC("6. Network", "Calvary is in the core of the funder web; paths run through shared funders and peers, not boards.");
  {
    const s = D.headlineSlide(pres, "Calvary sits inside the same funder web as its peers, and most of the best-connected funders already fund it.", sec);
    D.wideImage(s, "m6_03_network", { title: "Central funders",
      lines: ["By organizations funded: GWCF 18, Benevity 18, Schwab 16, Cafritz 14, Vanguard 13, NPT 13, United Way NCA 13, Blackbaud 11, Venable 10, Bank of America 10, Abell 9.", "330 funders connect the 19 organizations; 58 fund three or more."] });
    D.footnote(s, { source: "fact_grants (Calvary + 18 peers, TY2020–24), dim_funder", method: "bipartite graph; concentric layout; edge width = dollars", chart: "m6_03, m6_01", note: "C2" });
  }
  const ov = D.readCsv("m6_02_cofunding_overlap").reverse();
  natSlide(sec, "Calvary shares the most institutional funders with Miriam's Kitchen, DASH and House of Ruth DC.",
    { labels: ov.map(r => r.org), series: [{ name: "Shared institutional funders", values: ov.map(r => D.num(r.shared_institutional_funders)), color: HEX.institutional }, { name: "Peer's institutional funders not funding Calvary", values: ov.map(r => D.num(r.peer_institutional_funders_not_calvary)), color: HEX.peer }], opts: { barDir: "bar", valFmt: "0", dataLabels: true, catFontSize: 8, h: 4.75, gapWidth: 25 } },
    "Overlap", ["Shared: Miriam's Kitchen 17, DASH 14, House of Ruth DC 14, New Endeavors 12, My Sister's Place 12.", "Not shared: House of Ruth MD 81, House of Ruth DC 69, Miriam's Kitchen 48, N Street Village 45."],
    { source: "fact_grants, dim_funder", method: "institutional funders only (DAF sponsors excluded)", chart: "m6_02", note: "C2" });
  const il = D.readCsv("m6_04_board_interlocks").filter(r => r.subject === "Calvary" || r.other_is_funder === "True");
  tableSlide(sec, "Board interlocks are a thin channel, with one high-confidence Calvary link and seven medium-confidence leads to confirm.",
    ["Subject", "Linked organization", "Funder?", "Confidence (use)", "Years / evidence"], il.slice(0, 24).map(r => [r.subject, trunc(tc(r.other_name), 70), r.other_is_funder === "True" ? "yes" : "no", r.label, String(r.evidence).replace("same person in filings; ", "")]),
    [2.0, 3.9, 0.9, 2.6, 2.7], { source: "fact_org_relationships (shared_board_member), dim_person (person_id only; no names stored)", method: "exact normalized name plus a corroborating signal; leadership materials use high confidence only", chart: "m6_04", note: "C2" }, { fontSize: 8.5 });

  // ---------------- 7. Pipeline
  sec = SEC("7. Pipeline and scoring", "Seven weighted dimensions, editable in one file; 11 Tier 1 rows with next steps.");
  tableSlide(sec, "The pipeline scores 182 candidates on seven weighted dimensions that can be changed in one config file and rerun.",
    ["Dimension", "Weight", "Evidence (0–1 score)"], [
      ["Mission fit", "0.20", "Funder issue tags (housing/DV/women 1.0; behavioral health/workforce/health 0.7; general operating 0.6) + share of DC-sector dollars tagged housing/DV/women"],
      ["Peer giving", "0.20", "Core peers funded TY2020–24, capped at 8"],
      ["Regional giving", "0.10", "Dollars to DC-sector organizations, log scale $50K → $10M"],
      ["Award size", "0.15", "Median grant to peers (else DC-sector median), log scale $5K → $250K"],
      ["Accessibility", "0.10", "Funder type and breadth (community foundation 0.85 … narrow family foundation 0.30); −0.15 'see attached'; −0.30 in-kind channels; DAF-like 0.15"],
      ["Durability", "0.10", "Years funding peers and years active in the sector"],
      ["Relationship", "0.15", "M6 path strength + 0.35 current funder + 0.20 lapsed + 0.15 on CRM/lists"],
      ["Tiers", "—", "Tier 1: score ≥ 0.62 and typical grant ≥ $25K (max 20). Tier 2: ≥ 0.48. Tier 3: rest. Government and corporate rows: analyst scores."],
    ], [2.2, 1.0, 8.9], { source: "config/scoring_weights.yaml; chart_data/m5_00_candidate_funders.csv; m6_05_relationship_paths.csv", method: "weighted sum; rerun scripts/07_m7_pipeline.py after editing weights", chart: "m7_00", note: "C3" });
  const t1 = D.readCsv("m7_00_funder_pipeline").filter(r => r.tier === "1");
  tableSlide(sec, "Eleven rows reach Tier 1: four current majors, three new foundations, one corporate relationship and three public streams.",
    ["#", "Target", "Track", "Score", "Typical grant", "Why", "Relationship path"], t1.map(r => [r.rank, r.track.startsWith("institutional") ? tc(r.funder_name) : String(r.funder_name), r.track, D.num(r.score).toFixed(2), D.num(r.typical_grant) ? D.fmtK(D.num(r.typical_grant)) : "—", String(r.why), trunc(r.relationship_path, 110)]),
    [0.35, 2.5, 1.75, 0.5, 0.75, 3.05, 3.2], { source: "recommendations/funder_pipeline.csv", method: "see scoring table", chart: "m7_00", note: "C3" }, { rowsPerSlide: 13, fontSize: 8 });
  pngSlide(sec, "Peer giving and existing relationships drive Tier 1 scores, while award size separates the foundations that can move the numbers.", "m7_03_tier1_score_breakdown", null, null,
    { source: "chart_data/m7_00_funder_pipeline.csv", method: "weighted contribution of each dimension", chart: "m7_03", note: "C3" }, { wide: 4.0 });
  const plan = D.readCsv("m7_01_action_plan_90day");
  tableSlide(sec, "The 90-day plan gives each Tier 1 target a next step, an owner, a deadline and an application cycle.",
    ["Target", "Next step", "Owner", "By", "Application cycle"], plan.map(r => [r.track.startsWith("institutional") ? tc(r.funder_name) : String(r.funder_name), String(r.next_step), r.owner_role, r.deadline, String(r.next_deadline_or_cycle || "")]),
    [2.6, 5.0, 1.6, 1.0, 1.9], { source: "recommendations/action_plan_90day.csv; config/guideline_notes.csv (sources/web_tier1_guidelines.csv)", method: "deadlines relative to plan start; guideline basis labeled first-party / third-party / analyst note", chart: "m7_01, m7_04", note: "C3" }, { rowsPerSlide: 13, fontSize: 8 });
  const sens = D.readCsv("m7_05_sensitivity");
  tableSlide(sec, "Moving any weight or the tier cutoff by 0.05 changes ranks but not the ten institutional names in Tiers 1–2.",
    ["Change", "Mean rank shift (top 30)", "Top-10 overlap", "Tier 1–2 added", "Tier 1–2 dropped"], sens.map(r => [r.change, D.num(r.mean_abs_rank_shift_top30).toFixed(2), r.top10_overlap, r.tier12_added, r.tier12_dropped]),
    [4.0, 2.2, 1.8, 2.0, 2.1], { source: "chart_data/m7_05_sensitivity.csv", method: "each weight ±0.05 with renormalization; tier-2 cutoff ±0.05", chart: "m7_05", note: "C3" }, { rowsPerSlide: 16, fontSize: 9 });

  // ---------------- 8. Expansion
  sec = SEC("8. Mission expansion", "Near options first; health as a partnership; families not suggested.");
  const ex = D.readCsv("m8_01_expansion_scan").reverse();
  natSlide(sec, "Health and workforce funding pools are large and one step from Calvary's programs, while aging, veterans and reentry are small.",
    { labels: ex.map(r => r.label.includes(`(${r.distance})`) ? r.label : `${r.label} (${r.distance})`), series: [{ name: "DMV institutional grants naming the area, $/yr", values: ex.map(r => D.num(r.dmv_amount_per_year)), color: HEX.institutional }], opts: { barDir: "bar", dataLabels: true, showLegend: false, catFontSize: 8, valFmt: "$#,##0,,\"M\"", dataFmt: "$#,##0.0,,\"M\"" } },
    "Scan", ["Near: education $94M (schools dominate), workforce $30M, behavioral health $21M, DV $4.5M.", "Medium: health $84M (206 funders at $100K+), aging $9.7M, veterans $7.7M, reentry $1.0M.", "Far: maternal/family $4.2M."],
    { source: "fact_grants purpose tags (DMV institutional, TY2020–24); fact_opportunities; config/expansion_areas.yaml", method: "general operating excluded; distance ratings are analyst judgment", chart: "m8_01", note: "D1" });
  tableSlide(sec, "Each option carries a trade-off, from workforce and behavioral health at modest cost to DV formalization that raises government share.",
    ["Option", "Distance", "Pool evidence", "Upside", "Cost / risk"], [
      ["Formalize workforce (SheWorks-style cohort in Step Up DC)", "near", "$30M/yr tagged; DOES/WIOA; SNAP E&T held", "New funders and public contracts; outcomes story", "Program staff; partner management"],
      ["Behavioral-health credential or billing partner", "near", "$21M/yr tagged; Medicaid", "Therapy becomes program revenue (Samaritan Inns path)", "Compliance, staffing, 12–18 months"],
      ["DV program formalization (VOCA eligibility)", "near", "OVSJG $55M pool; DV peers 70–89% government", "Deeper OVSJG relationship; DV funders", "Reporting; raises government share"],
      ["FQHC clinic hours on site (Community of Hope; DWC/JWCH model)", "medium", "$84M/yr tagged; 206 funders at $100K+", "Health funders at low capital cost", "Partner dependence"],
      ["Older-women track in PSH", "medium", "$9.7M/yr; The Washington Home", "Narrative fit", "Small pool"],
      ["Women veterans / reentry", "medium", "small private pools; HVRP, BJA", "Program-specific federal money", "New compliance regimes"],
      ["Families / maternal", "far", "$4.2M/yr", "—", "Mission change; not suggested"],
    ], [3.4, 0.9, 2.8, 2.6, 2.4], { source: "modules/m8_expansion_scan.md; config/expansion_areas.yaml", method: "options and trade-offs are analyst judgment on the scan evidence", chart: "m8_01", note: "D1" }, { fontSize: 9 });
  const fo = D.readCsv("m8_02_federal_opportunities");
  const agg = {}; fo.forEach(r => { const k = r.funder_name.slice(0, 48); agg[k] = (agg[k] || 0) + 1; });
  tableSlide(sec, "Direct federal competition is thin, with 36 relevant notices, so the realistic channels remain HUD CoC and HUD CPF.",
    ["Agency", "Notices", "Examples"], Object.entries(agg).sort((a, b) => b[1] - a[1]).map(([k, n]) => [fo.find(r => r.funder_name.slice(0, 48) === k).funder_name, n, fo.filter(r => r.funder_name.slice(0, 48) === k).slice(0, 2).map(r => trunc(r.title, 58)).join("; ")]),
    [4.0, 1.0, 7.1], { source: "fact_opportunities (Grants.gov posted and forecasted)", method: "research, tribal, rural and overseas notices removed; relevant agencies kept", chart: "m8_02", note: "D1" }, { rowsPerSlide: 13, fontSize: 9 });

  // ---------------- 9. Need and capacity
  sec = SEC("9. Need and capacity", "The deepest need in the city; a shrinking system; a growing share for Calvary.");
  pngSlide(sec, "Calvary's home ward has twice the city's poverty rate and the highest female poverty in DC.", "m9_05_ward_map", "Ward indicators",
    ["Poverty: Ward 8 31%, Ward 7 23%, DC 15%. Female poverty: 32% / 25% / 16%.", "Renters paying 50%+: 33% / 32% / 24%. Unemployment: 13% / 13% / 6%.", "Female householder, no spouse: 30% / 29% / 13%."],
    { source: "dim_geo (ACS 2020–24, DC wards as state legislative districts; DC Open Data ward boundaries)", method: "five-year estimates; 90% MOE in the table", chart: "m9_01, m9_05", note: "—" }, { wide: -1.5 });
  const pit = D.readCsv("m9_02_dc_pit"); const hic = D.readCsv("m9_03_calvary_hic_share");
  natSlide(sec, "DC's homeless count fell from 8,350 (2016) to 5,138 (2025) while Calvary's inventory grew to 124 beds.",
    { type: "line", labels: pit.map(r => r.year), series: [{ name: "DC point-in-time count", values: pit.map(r => D.num(r.value)), color: HEX.government }], opts: { valFmt: "#,##0", showLegend: false } },
    "Capacity", hic.map(r => `${r.year}: ${Math.round(D.num(r.calvary_th_beds) + D.num(r.calvary_psh_beds) + D.num(r.calvary_rrh_beds))} beds, ${D.fmtPct(D.num(r.calvary_share_of_th), 1)} of DC TH beds`).concat(["Women-focused providers 2025: N Street Village 457, Open Arms 412, House of Ruth 388, New Endeavors 135, Calvary 124."]),
    { source: "supp_homeless_counts (HUD PIT, DC-500); supp_hic_projects (HUD HIC 2022–2025)", method: "beds = HIC total_beds by project type", chart: "m9_02, m9_03", note: "—" });

  // ---------------- 10. Comparators
  sec = SEC("10. Named comparators", "DWC shows scale with government; SheWorks shows a program design.");
  pngSlide(sec, "DWC grew from $6M to $34M in a decade as government rose to 57% of revenue, on thin cash.", "m10_01_comparator_trajectories", "DWC", ["FY2014 $6.3M, 24% government → FY2024 $34.4M, 57%.", "Federal FY2020–25 $21.6M: CoC $14.3M, ESG $3.5M, VOCA $2.7M; 99% pass-through.", "159 PSH units; clinic with JWCH; MADE enterprise; Rosa's Place (97 units) under construction."],
    { source: "fact_org_financials (IRS 990), fact_gov_awards (FAC single audits)", method: "government = line 1e; DWC fiscal year = calendar year", chart: "m10_01, m10_02", note: "B3" });
  tableSlide(sec, "The SheWorks parent started at 88% government and is diversifying fast, and SheWorks is a program design to borrow.",
    ["Item", "DWC (Los Angeles)", "CBWC Empowerment Institute / SheWorks (Carson, CA)"], [
      ["Revenue, latest", "$34.4M (FY2024)", "$1.84M (FY2025, FYE June)"],
      ["Government share", "57%", "70% (88% in FY2023)"],
      ["Months of cash", "2.4", "8.2"],
      ["Programs", "PSH (159 units), community housing, women's health clinic (JWCH), MADE paid transitional work", "Black Women's Think Tank, Conversations, Protecting Black Women and Girls; SheWorks cohort (Jan–May 2026, ~30 women; stipends, childcare, ride credits)"],
      ["Funders in the data", "280 names on the 2023 list; Hilton $1.53M, Blue Shield of CA Fdn $450K, Ahmanson $325K, Anthem $300K, LA County First District $3M; DMV funders: Bank of America $154K, Wells Fargo $100K", "LA County Federation of Labor (partial funding); L.A. Care and Blue Shield Promise (host sites, in kind); no FAC or USAspending awards"],
      ["What transfers", "Housing-development pipeline; clinic partnership; social enterprise; donor-base scale", "Cohort design and partner structure for Step Up DC"],
      ["What does not", "The mix (scaled with government on thin cash)", "The funding model (more government-dependent than Calvary)"],
    ], [2.2, 4.8, 5.1], { source: "fact_org_financials, fact_gov_awards, fact_grants web rows (annual reports, funder announcements)", method: "see M10 readout; DAF grants to LA organizations not captured", chart: "m10_01, m10_03, m10_05", note: "B3" }, { fontSize: 10.5 });

  // ---------------- 11. Verdict and recommendations
  sec = SEC("11. Verdict, recommendations and open items", "Moderate-to-high pressure from concentration and liquidity; five recommendation areas; three documents requested.");
  let s = D.headlineSlide(pres, "The verdict is moderate-to-high pressure, driven by channel concentration and liquidity rather than by the government share.", sec);
  D.statTiles(s, [{ value: "53%", label: "Government share FY22–24 mean (58% FY25); 11th of 19 peers; 57th percentile of the DC sector" }, { value: "74%", label: "Share of the $4.1M recurring award base that passes through TCP (CoC + DHS)" }, { value: "27%", label: "Share of five years of filed grants from one funder (GWCF incl. Health Equity Fund); top five 63%" }, { value: "4.4 mo", label: "Cash at FY25 year-end after a $607K deficit; 7.5 months in FY21" }], { y: BODY_Y, h: 2.4 });
  s.addText("Public funding at about half of revenue is typical for this work. The things to plan around are the shape of that funding (three streams, two through one intermediary), a private base that has held steady from the same funders, and a thinner cushion after FY25. DC's pools have held, with cuts proposed and restored each spring; the federal side (CoC renewals, EHV sunset) and the TCP channel are the larger uncertainties.", { x: M, y: 4.5, w: W - 2 * M, h: 1.5, fontSize: 14, color: HEX.text, margin: 0, isTextBox: true });
  D.footnote(s, { source: "recommendations/funding_pressure_verdict.md (evidence table with chart IDs)", method: "verdict synthesizes M1–M3 and M9", chart: "m1_02, m2_01, m1_07, m1_05" });
  s = D.headlineSlide(pres, "Five recommendation areas follow: protect and draw the public base, rebuild private revenue, hold a reserve, expand near, mitigate risk.", sec);
  const cw = (W - 2 * M - 1.2) / 5;
  [["1. Public base", ["Draw-down audit vs ceilings", "Confirm DHS / Sisters Rise with TCP", "Defend CoC renewals; scope PSH expansion", "OVSJG budget calendar"]],
   ["2. Private revenue", ["Multi-year upgrades: GWCF, Cafritz, Abell, Fowler, UWNCA, BoA", "Open Clark, Schattner, Cohen, Bernstein, Washington Home, Weinberg, Meyer", "Re-engage lapsed; restore events; major-gifts/DAF program"]],
   ["3. Reserve", ["Six months of expenses (~$2.8M)", "Close the FY25 gap in the FY26 budget", "Treat HEF as one-time"]],
   ["4. Expansion", ["Workforce cohort (SheWorks model)", "Behavioral-health credential decision", "FQHC partnership", "DV formalization only with eyes open"]],
   ["5. Risk mitigation", ["Direct DHS line alongside TCP; HUD CPF; DHS PSH", "Contract terms; monthly draw tracking", "Advocacy calendar; early-warning indicators"]],
  ].forEach(([t, lines], i) => D.card(s, { x: M + i * (cw + 0.3), y: BODY_Y, w: cw, h: 3.6, title: t, lines, fontSize: 11.5 }));
  s.addText("Target arithmetic: private revenue ~$2.1M (FY25) → ~$3.0M in three years (institutional +$0.5M, major donors/DAF +$0.3M, events +$0.4M, earned +$0.1–0.3M) takes the public share to about 50% at flat public funding.", { x: M, y: BODY_Y + 3.85, w: W - 2 * M, h: 0.6, fontSize: 12, color: HEX.text2, margin: 0, isTextBox: true });
  D.footnote(s, { source: "recommendations/strategic_recommendations.md", method: "recommendations are options for Calvary's leadership to weigh", chart: "—" });
  tableSlide(sec, "Three documents from Calvary would resolve the three open flags: the audits, the TCP agreements and the FY25 event calendar.",
    ["Flag", "Finding", "Why it matters", "Handling (approved CP2)", "Document that resolves it"], [
      ["D1", "Recognized 67–73% of known award ceilings in FY24–25", "~$1M/yr may be undrawn or the DHS carry-forward overstates FY25", "Medium confidence; labeled 'ceilings vs recognized'", "FY24/FY25 audits; TCP subgrant agreements"],
      ["D2", "Sisters Rise PSH (24 EHV units, $593K) absent from the 2025 HIC", "Part of FY25's drop may be a lost stream; baseline may be high", "DHS stream 'at risk'; FY2024 value kept in baseline", "TCP agreements; Calvary confirmation"],
      ["D3", "Event contributions $538K → $55K while net event income turned positive", "Explains most of the FY25 private drop; likely timing", "Reported as the largest swing", "FY25 gala calendar; CRM notes"],
    ], [0.6, 3.2, 3.0, 2.6, 2.7], { source: "discoveries_log.md; open_questions.md part B (data build)", method: "each flag logged with evidence, proposed action and response", chart: "m2_02, m2_03, m1_06" }, { fontSize: 11 });
  s = D.headlineSlide(pres, "The appendix decks carry every chart, table and method note, and the insight register tracks verification for all 36 findings.", sec);
  D.bullets(s, ["Appendix A: Calvary and government funding (17 slides). Appendix B: peers and named comparators (12). Appendix C: funders, gaps, network and pipeline (21). Appendix D: data and methods (24, method notes A1–D3).",
    "Reports: executive summary, full findings, methodology, recommendations; board readout talking points; consulting team briefing.",
    "Scoring weights: config/scoring_weights.yaml; scenarios: config/scenarios.yaml; peers: calvary_funding_data/config/core_peers.csv; exclusions: config/landscape_exclusions.csv.",
    "Traceability: chart ID → chart_data/<id>.csv → clean table → source registry; scripts/lib/trace.py checks the chain.",
    `Insight register: 36 findings, confidence high/medium/low, status draft until the independent review. Data as of ${D.AS_OF}.`], { fontSize: 15 });
  D.footnote(s, { source: "calvary_analysis/README.md; insight_register.csv", method: "—", chart: "all" });

  fitTitles(pres);
  await D.finish(pres, path.join(__dirname, "consulting_deck.pptx"));
})();
