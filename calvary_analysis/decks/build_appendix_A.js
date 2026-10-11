// Appendix A: Calvary and government funding. Follows storylines/appendix_headline_spine.md (Appendix A, items 1-17).
const path = require("path");
const C = require("./build_appendix_common");
const { D, HEX, M, W, BODY_Y, BODY_H, FULL_W, tc, trunc, num, usd, money, pct, n0, yr, tbl } = C;

const SRC990 = "IRS Form 990 e-file returns (GivingTuesday, NCCS, IRS SOI, ProPublica), Calvary 990 PDFs and audits FY13–FY23; fact_org_financials";
const SRC_OVSJG = "DC OVSJG award lists FY2019–2026 (DC Open Data, OVSJG recipient lists); fact_gov_awards (source_type dc_ovsjg)";
const SRC_COC = "HUD Continuum of Care award lists, DC-500, competition years 2019–FY2025; fact_gov_awards (source_type hud_coc)";
const SRC_BUDGET = "DC Approved Budget and Financial Plan books FY2024–FY2027, Council committee budget reports, Budget Support Acts";

(async () => {
  const X = C.makeDeck("Appendix A: Calvary and government funding", "Appendix A of the Calvary funding analysis");
  const pres = X.pres;

  // 1. Title
  X.section("Appendix A");
  X.title("Appendix A: Calvary and Government Funding",
    "Appendix A · Calvary and government funding · pro bono funding analysis for Calvary Women's Services. Method notes A1–A6 are in Appendix D.");

  // 2. Reconciliation table
  X.section("Trajectory");
  const rec = C.readAny("calvary_funding_data/reports/calvary_financials_reconciliation.csv");
  const fys = [...new Set(rec.map(r => r.fiscal_year))].sort();
  const recRows = fys.map(fy => {
    const rs = rec.filter(r => r.fiscal_year === fy);
    const f990 = rs.filter(r => r.return_type !== "audit" && num(r.total_revenue) != null);
    const aud = rs.find(r => r.return_type === "audit");
    const base = f990.length ? num(f990[0].total_revenue) : null;
    const maxDiff = Math.max(...f990.map(r => Math.abs(num(r.diff_vs_xml) || 0)));
    const na990 = f990.map(r => num(r.net_assets_eoy)).find(v => v != null);
    return [`FY${fy.slice(2)}`, usd(base), String(f990.length), pct(maxDiff, 1), aud ? usd(aud.total_revenue) : "no audit", aud ? pct(num(aud.diff_vs_xml), 1) : "—",
      aud ? (num(aud.net_assets_eoy) === na990 ? "yes" : "no") : "—"];
  });
  X.table("Calvary's revenue series agrees across five sources within 1% in every year, so the trajectory rests on firm ground.",
    ["Fiscal year", "Total revenue (990)", "990 sources with revenue", "Largest 990-source difference", "Audit total revenue", "Audit difference", "Audit net assets = 990"],
    recRows, [1.2, 1.9, 1.7, 1.9, 1.9, 1.5, 2.0],
    { source: "IRS 990 XML (GivingTuesday), IRS SOI, ProPublica, NCCS e-file tables, Calvary 990 PDFs and audits; calvary_funding_data/reports/calvary_financials_reconciliation.csv", method: "difference = source revenue vs e-filed XML; audits differ 0–9% by design (GAAP in-kind and special-event presentation)", chart: null, note: "A1" },
    { rowsPerSlide: 15, fontSize: 10 });

  // 3. m1_03
  const gs = D.readCsv("m1_03_gov_share_two_measures");
  X.table("Government revenue on the audit basis exceeded 990 line 1e by $1.48M in FY21 and matched it in FY22 and FY23.",
    ["Fiscal year", "Government (audit)", "Audit total revenue", "Share (audit)", "Government (990 line 1e)", "990 total revenue", "Share (line 1e)", "Audit − line 1e"],
    gs.map(r => [r.fy_label, usd(r.gov_audit), usd(r.audit_total_revenue), pct(num(r.gov_share_audit)), usd(r.gov_line_1e), usd(r.total_revenue_990), pct(num(r.gov_share_line_1e)),
      num(r.gov_audit) != null && num(r.gov_line_1e) != null ? usd(num(r.gov_audit) - num(r.gov_line_1e)) : "—"]),
    [1.1, 1.6, 1.6, 1.2, 1.9, 1.6, 1.3, 1.83],
    { source: "Calvary audited financial statements FY13–FY23 and IRS 990 Part VIII line 1e; fact_org_financials", method: "share = government revenue ÷ total revenue on each basis; FY24–25 have no public audit", chart: "m1_03", note: "A1" },
    { rowsPerSlide: 13, fontSize: 10.5 });

  // 4. m1_01 + m1_04 + m1_05
  const rv = D.readCsv("m1_01_revenue_expenses"); const sd = D.readCsv("m1_04_surplus_deficit");
  X.table("Revenue, expenses, net assets, cash and months of cash by year show the FY22 capital event and the FY23 and FY25 deficits.",
    ["Fiscal year", "Total revenue", "Total expenses", "Surplus / deficit", "Revenue (2024 $)", "Net assets (year end)", "Cash and savings", "Months of cash"],
    rv.map(r => { const s = sd.find(x => x.fiscal_year === r.fiscal_year) || {}; return [r.fy_label, usd(r.total_revenue), usd(r.total_expenses), usd(r.surplus_deficit), usd(r.total_revenue_real_2024), usd(s.net_assets_eoy), usd(s.cash_savings_eoy), num(s.months_of_cash) == null ? "—" : num(s.months_of_cash).toFixed(1)]; }),
    [1.1, 1.6, 1.6, 1.6, 1.6, 1.8, 1.6, 1.23],
    { source: `${SRC990}; dim_period (CPI-U)`, method: "preferred 990 row per year; 2024 dollars via CPI-U; months of cash = cash and savings ÷ (expenses ÷ 12); FY22 includes the $3.68M SLFRF award", chart: "m1_01, m1_04, m1_05", note: "A1" },
    { rowsPerSlide: 15, fontSize: 10 });

  // 5. m1_06 events: PNG + table
  const ev = D.readCsv("m1_06_events");
  let s = X.head("Event contributions and net event income by year show the FY25 collapse against positive net income.");
  C.img(s, "m1_06_event_income", { x: M, y: BODY_Y + 0.2, w: 7.2, h: 4.4 });
  tbl(s, ["Fiscal year", "Event contributions (line 1c)", "Net special-event income (line 8c)"], ev.map(r => [r.fy_label, usd(r.event_contributions_line_1c), usd(r.special_events_net)]),
    { x: 8.1, y: BODY_Y, w: 4.63, colW: [1.0, 1.8, 1.83], fontSize: 10, align: ["left", "right", "right"] });
  D.footnote(s, { source: "IRS 990 Part VIII lines 1c and 8c; fact_org_financials", method: "as reported; line 8c = gross event income less direct event expenses (discovery flag D3: confirm FY25 gala timing)", chart: "m1_06", note: "A1" });

  // 6. m1_07 full table
  const fc = D.readCsv("m1_07_calvary_funder_concentration").sort((a, b) => num(a.rank) - num(b.rank));
  const top10 = num(fc[9].cum_share);
  X.table(`Fifty funders filed grants to Calvary in TY2020–24 and the top ten supplied ${Math.round(top10 * 100)}% of the dollars.`,
    ["Rank", "Funder", "Funder type", "Filed grants TY2020–24", "Tax years", "Grants", "Share", "Cumulative share"],
    fc.map(r => [r.rank, trunc(tc(r.funder_name), 60), r.funder_type.replace(/_/g, " "), usd(r.amount), r.years, r.n_grants, pct(num(r.share), 1), pct(num(r.cum_share), 1)]),
    [0.6, 4.4, 2.0, 1.7, 0.9, 0.8, 0.8, 0.93],
    { source: "Funders' 990-PF grants paid and Schedule I rows naming Calvary (IRS e-file via GivingTuesday); fact_grants, dim_funder", method: "TY2020–24, cumulative rows excluded, aggregated by funder EIN; DAF sponsors included and typed; HHI 1,168", chart: "m1_07", note: "A3" },
    { rowsPerSlide: 14, fontSize: 10 });

  // 7. OVSJG detail
  X.section("Government streams");
  const sm = D.readCsv("m2_01_stream_map");
  const ov = sm.filter(r => r.stream.startsWith("OVSJG"));
  ov.forEach(r => { r.fiscal_year = yr(r.fiscal_year); });
  const ovYears = [...new Set(ov.map(r => r.fiscal_year))].sort();
  const sumOv = (det, y) => ov.filter(r => r.detail === det && r.fiscal_year === y).reduce((a, r) => a + num(r.amount), 0);
  const ot = D.readCsv("m2_01b_one_time_awards");
  ot.forEach(r => { r.fiscal_year = yr(r.fiscal_year); });
  const slfrf = ot.find(r => r.stream.startsWith("SLFRF"));
  s = X.head("OVSJG awards to Calvary rose from $369K to $1.05M between DC FY2020 and FY2026, with the one-time $3.68M building award in FY2022.");
  D.chart(s, "bar", ovYears.map(y => `FY${y.slice(2)}`), [
    { name: "Reach Up TH", values: ovYears.map(y => sumOv("OVSJG: Reach Up TH", y)), color: HEX.government },
    { name: "New Foundations TH", values: ovYears.map(y => sumOv("OVSJG: New Foundations TH", y)), color: HEX.other }],
    { x: M, y: BODY_Y, w: 6.4, h: BODY_H, stacked: true, valFmt: "$#,##0,\"K\"" });
  tbl(s, ["DC FY", "Reach Up TH", "New Foundations TH", "Recurring total", "One-time"], ovYears.map(y => {
    const ru = sumOv("OVSJG: Reach Up TH", y), nf = sumOv("OVSJG: New Foundations TH", y);
    return [y, usd(ru), nf ? usd(nf) : "—", usd(ru + nf), slfrf && slfrf.fiscal_year === y ? `${usd(slfrf.amount)} SLFRF` : "—"];
  }), { x: 7.25, y: BODY_Y, w: 5.48, colW: [0.6, 1.05, 1.25, 1.15, 1.43], fontSize: 9.5, align: ["left", "right", "right", "right", "right"] });
  s.addText("FY2019 and FY2022 Reach Up totals combine two awards each ($292,000 + $368,935; $368,935 + $99,500). FY2024–26 lists label all Calvary grants Local; the FY23 SEFA shows SLFRF pass-through.",
    { x: 7.25, y: 5.3, w: 5.48, h: 0.9, fontSize: 9.5, color: HEX.text2, margin: 0, isTextBox: true, valign: "top" });
  D.footnote(s, { source: SRC_OVSJG, method: "one source per stream; DC fiscal year = Calvary fiscal year; the SLFRF building award is excluded from the recurring base", chart: "m2_01, m2_01b", note: "A2" });

  // 8. CoC detail
  const coc = sm.filter(r => r.stream.startsWith("HUD CoC")); coc.forEach(r => { r.fiscal_year = yr(r.fiscal_year); });
  const cYears = [...new Set(coc.map(r => r.fiscal_year))].sort();
  const projects = ["CoC: Sister Circle PSH", "CoC: Reach Up", "CoC: New Foundations 2"];
  const pc = [HEX.government, HEX.daf, HEX.institutional];
  const sumC = (p, y) => coc.filter(r => r.detail === p && r.fiscal_year === y).reduce((a, r) => a + num(r.amount), 0);
  s = X.head("HUD CoC awards to Calvary's three projects rose from $240K (2019) to $1.77M (FY2025) through TCP.");
  D.chart(s, "bar", cYears.map(y => String(y)), projects.map((p, i) => ({ name: p.replace("CoC: ", ""), values: cYears.map(y => sumC(p, y)), color: pc[i] })),
    { x: M, y: BODY_Y, w: 6.4, h: BODY_H, stacked: true, valFmt: "$#,##0,\"K\"" });
  tbl(s, ["Competition year", "Sister Circle PSH", "Reach Up", "New Foundations 2", "Total", "Calvary FY"], cYears.map(y => {
    const v = projects.map(p => sumC(p, y)); const t = v.reduce((a, b) => a + b, 0);
    return [y, ...v.map(x => x ? usd(x) : "—"), usd(t), `FY${String(Number(y) + 1).slice(2)}`];
  }), { x: 7.25, y: BODY_Y, w: 5.48, colW: [0.85, 0.95, 0.95, 1.0, 1.0, 0.73], fontSize: 9.5, align: ["left", "right", "right", "right", "right", "left"] });
  s.addText("TCP is the applicant; each project is stored once as a subaward with TCP as pass-through. Reach Up fell from $1.22M (2021) to $0.42M (2022) under TCP reallocation and expanded in 2024.",
    { x: 7.25, y: 4.6, w: 5.48, h: 1.0, fontSize: 9.5, color: HEX.text2, margin: 0, isTextBox: true, valign: "top" });
  D.footnote(s, { source: SRC_COC, method: "HUD competition year t aligned to Calvary operating year t+1 (coc_award_lag_years: 1 in config/scenarios.yaml)", chart: "m2_01", note: "A2" });

  // 9. DHS detail
  const dur = D.readCsv("m2_03_stream_durability");
  const dhs = sm.filter(r => r.stream.startsWith("DHS")).sort((a, b) => num(b.amount) - num(a.amount));
  s = X.head("DC's FY2024 oversight responses are the only public record of Calvary's DHS contracts: $830K for transitional housing and $593K for Sisters Rise.");
  tbl(s, ["Contract (via TCP)", "DC FY", "Amount", "Capacity", "Renewal mechanism", "Durability rating (analyst judgment)"], dhs.map(r => {
    const d = dur.find(x => x.detail === r.detail) || {};
    return [r.detail.replace("DHS/TCP: ", ""), r.fiscal_year, usd(r.amount), /Sisters/.test(r.detail) ? "25 units" : "45 beds", trunc(d.renewal_mechanism, 120), trunc(d.durability_risk, 130)];
  }).concat([["Total", "2024", usd(dhs.reduce((a, r) => a + num(r.amount), 0)), "", "", ""]]),
    { x: M, y: BODY_Y, w: FULL_W, colW: [2.0, 0.8, 1.2, 1.0, 3.3, 3.83], fontSize: 9.5 });
  D.card(s, { x: M, y: 3.7, w: FULL_W, h: 2.5, title: "Why this stream rests on one public data point", fontSize: 11.5, lines: [
    "Provider amounts appear only in the Council's FY2024 oversight responses (pp 111–112); DHS provider lists for 2025–2026 were not posted.",
    "TCP's own 990s do not itemize provider payments on Schedule I, so they cannot fill the other years.",
    "Every other year of this stream is unknown, not zero; the scenario baseline carries the FY2024 value forward (dhs_assumed_flat_from_fy2024).",
    "Sisters Rise is absent from the 2025 Housing Inventory Count (discovery flag D2); TCP subgrant agreements FY2023–FY2026 would close it."] });
  D.footnote(s, { source: "DC Council FY2024 performance oversight responses (DHS); fact_gov_awards (source_type dc_oversight); supp_hic_projects", method: "contract ceilings as reported; durability ratings are analyst judgment (basis = inferred)", chart: "m2_01, m2_03", note: "A2" });

  // 10. SEFA table (values from calvary_funding_data/notes_for_analysis.md §2)
  s = X.head("Calvary's single audits for FY22 and FY23 show $4.07M and $0.94M of federal expenditures, almost all passed through DC agencies and TCP.");
  const sefa = [
    ["State and Local Fiscal Recovery Funds (SLFRF)", "21.027", "DC OVSJG", 3583885, 440677],
    ["HUD Continuum of Care", "14.235", "TCP", 415830, 390649],
    ["Emergency Food and Shelter Program (EFSP)", "—", "FEMA", 48889, 67684],
    ["SNAP Employment and Training", "—", "DC DHS", 19114, 38989]];
  const t22 = sefa.reduce((a, r) => a + r[3], 0), t23 = sefa.reduce((a, r) => a + r[4], 0);
  const sefaRows = sefa.map(r => [r[0], r[1], r[2], usd(r[3]), pct(r[3] / t22, 1), usd(r[4]), pct(r[4] / t23, 1)]);
  const tot = ["Total federal expenditures", "", "", usd(t22), "100%", usd(t23), "100%"]; tot._bold = true; sefaRows.push(tot);
  tbl(s, ["Program", "Assistance listing", "Passed through", "FY22", "Share", "FY23", "Share"], sefaRows,
    { x: M, y: BODY_Y, w: FULL_W, colW: [4.0, 1.4, 1.6, 1.5, 0.9, 1.5, 1.23], fontSize: 11, align: ["left", "left", "left", "right", "right", "right", "right"] });
  D.card(s, { x: M, y: 4.1, w: FULL_W, h: 2.0, title: "Reading the SEFA", fontSize: 12, lines: [
    "SEFA lines are expenditures in the audited fiscal year, not awards; they are never added to OVSJG or CoC award amounts.",
    "FAC's 'audit year 2023' record repeats the FY22 lines; the FY23 audit PDF ($937,999) is used and both are kept, flagged.",
    "FY17–FY20 audits state Calvary was not subject to a single audit; the FY21 audit is silent; FY24–FY25 audits are not public."] });
  D.footnote(s, { source: "Calvary audited financial statements FY22 (via Candid) and FY23, Federal Audit Clearinghouse; fact_gov_awards (source_type audit_sefa); notes_for_analysis.md §2", method: "expenditures as audited; shares of each year's total", chart: null, note: "A2" });

  // 11. One-time awards
  const otTotal = ot.reduce((a, r) => a + num(r.amount), 0);
  const otName = (t) => /^Economic Development/.test(t) ? "HUD Economic Development Initiative, Community Project Funding" : /^Section 4/.test(t) ? "HUD Section 4 Capacity Building (LISC subaward)" : t.replace("(Ppp)", "(PPP)");
  const otRows = ot.slice().sort((a, b) => num(b.amount) - num(a.amount)).map(r => [trunc(otName(r.stream), 70), yr(r.fiscal_year), r.year_basis, r.source_type, usd(r.amount)]);
  const otTot = ["Total one-time", "", "", "", usd(otTotal)]; otTot._bold = true; otRows.push(otTot);
  s = X.head(`One-time awards (SLFRF, PPP, HUD CPF, LISC) total ${money(otTotal)} and are excluded from the recurring base.`);
  tbl(s, ["Award", "Year", "Year basis", "Source", "Amount"], otRows, { x: M, y: BODY_Y, w: FULL_W, colW: [5.6, 1.0, 1.6, 1.8, 2.13], fontSize: 11, align: ["left", "left", "left", "left", "right"] });
  D.card(s, { x: M, y: 4.0, w: FULL_W, h: 2.2, title: "What each award was", fontSize: 12, lines: [
    "SLFRF via OVSJG: the New Foundations building (FY2022); it drives the FY22 revenue spike.",
    "HUD Community Project Funding (14.251): $200,000 awarded 2023 for a capital project, $76,866 outlaid in the data.",
    "SBA Paycheck Protection Program loan (2020) and a $25,000 LISC capacity-building subaward (2017).",
    "No DHCD award appears in the government-award data, so none is listed."] });
  D.footnote(s, { source: "DC OVSJG award lists; USAspending (SBA, HUD); fact_gov_awards", method: "one-time = capital, pandemic or single-year awards; excluded from recurring stream totals and scenarios", chart: "m2_01b", note: "A2" });

  // 12. m2_02
  const cv = D.readCsv("m2_02_ceilings_vs_recognized");
  X.table("The award-ceiling alignment uses DC fiscal years directly, HUD competition years lagged one year, and the FY2024 DHS value carried forward.",
    ["Calvary FY", "OVSJG", "HUD CoC (lagged)", "DHS / TCP", "Other federal", "SLFRF spent", "Known ceilings", "Recognized government", "Basis", "Recognized ex SLFRF ÷ ceilings"],
    cv.map(r => [r.fy_label, usd(r.ovsjg_award), usd(r.coc_award_lagged), num(r.dhs_award) == null ? "unknown" : usd(r.dhs_award), usd(r.other_federal), usd(r.slfrf_expenditure), usd(r.award_ceiling_known), usd(r.recognized_gov_revenue), r.recognized_basis, pct(num(r.ratio_recognized_ex_slfrf_to_ceiling))]),
    [0.9, 1.1, 1.2, 1.1, 1.0, 1.1, 1.2, 1.3, 1.1, 2.03],
    { source: "fact_gov_awards (OVSJG, HUD CoC, DC oversight, audit SEFA) and fact_org_financials (audits to FY23, 990 line 1e FY24–25)", method: "CoC year t → Calvary FY t+1; DHS FY2024 carried forward; EFSP/SNAP at audited FY23 level; DHS unknown before FY2024 (flag D1)", chart: "m2_02", note: "A5" },
    { rowsPerSlide: 7, fontSize: 10.5 });

  // 13. m2_03
  X.table("Seven streams carry distinct renewal mechanisms and risks.",
    ["Stream", "First → latest", "Funding source", "Renewal mechanism", "Durability risk (judgment)"],
    dur.map(r => [r.detail, `${money(r.first_amount)} (${r.first_year}) → ${money(r.latest_amount)} (${r.latest_year})`, trunc(r.funding_source, 80), trunc(r.renewal_mechanism, 90), trunc(r.durability_risk, 110)]),
    [2.1, 2.1, 2.5, 2.6, 2.83],
    { source: "fact_gov_awards, fact_policy_events, supp_hic_projects (HUD HIC 2024–2025)", method: "first and latest observed award per stream; risk ratings are analyst judgment (basis = inferred)", chart: "m2_03", note: "A2" },
    { rowsPerSlide: 7, fontSize: 10 });

  // 14. m2_04: PNG + pivot table
  X.section("DC budget and pools");
  X.png("Since pandemic money ended, DC's four budget lines behind Calvary's local streams have held flat to rising, with OVSJG under-spending 9–14%.",
    "m2_04_dc_budget_context", "Approved vs actual", [
      "OVSJG P02303 approved $45.5M (FY24), $55.9M (FY25), $55.4M (FY26), $55.3M (FY27); actual $41.3M and $47.9M in FY24–FY25.",
      "DHS continuum approved $170M (FY24) → $206M (FY26) → $194M (FY27).",
      "PSH approved $145M–$166M FY25–FY27.",
      "DV services $2.9M–$3.4M approved; the Mayor's FY26 proposal ($2.8M) was not enacted."],
    { source: `${SRC_BUDGET}; supp_dc_budget_lines`, method: "sums of activity-level total rows per program code; proposed = Mayor's FY2026 proposal as reported by Council committees", chart: "m2_04", note: "A6" }, { wide: 0.6 });
  const bc = D.readCsv("m2_04_dc_budget_context");
  const groups = [...new Set(bc.map(r => r.group))].sort();
  const byears = [...new Set(bc.map(r => r.fiscal_year))].sort();
  const stages = ["approved", "actual", "proposed"];
  const pivot = [];
  groups.forEach(g => stages.forEach(st => {
    const rs = bc.filter(r => r.group === g && r.budget_stage === st); if (!rs.length) return;
    pivot.push([trunc(g, 60), st, ...byears.map(y => { const r = rs.find(x => x.fiscal_year === y); return r ? money(r.amount, 1) : "—"; })]);
  }));
  X.table("DC budget lines for OVSJG, the DHS continuum, PSH and DV services by stage and year show approved budgets flat to rising through FY2027.",
    ["Budget line", "Stage", ...byears.map(y => `FY${y}`)], pivot, [3.5, 1.0, ...byears.map(() => 1.09)],
    { source: `${SRC_BUDGET}; supp_dc_budget_lines`, method: "activity-level totals; each book carries two years of actuals and two approved years; proposed = Mayor's FY2026 proposal", chart: "m2_04", note: "A6" },
    { rowsPerSlide: 12, fontSize: 10.5 });

  // 15. m2_06: PNG + table of OVSJG events >= $2M
  X.png("In each of the last two budget seasons the Mayor proposed cuts to OVSJG Victim Services grants and the Council restored them.", "m2_06_policy_timeline", "Pattern", [
    "FY26: Mayor −$5.84M to $50.1M; Council committee +$3.5M and a +$6.03M enhancement ($3.9M one-time).",
    "FY27: Mayor −$5.60M to $49.9M; Council +$5.1M one-time restoration.",
    "DHS lines move by larger amounts in both directions, driven by family rehousing (FRSP), ERAP and PSH vouchers."],
    { source: `${SRC_BUDGET}; fact_policy_events`, method: "events of $1M or more touching homeless, PSH, DV and victim-services lines, FY2024–FY2027", chart: "m2_06", note: "A6" }, { wide: 0.6 });
  const pe = D.readCsv("m2_06_policy_timeline")
    .filter(r => r.agency.startsWith("Office of Victim") && r.event_date && Math.abs(num(r.amount_change) || 0) >= 2e6)
    .sort((a, b) => (a.event_date + a.event_id).localeCompare(b.event_date + b.event_id));
  X.table(`${pe.length === 14 ? "Fourteen" : pe.length} budget events of $2M or more touched Calvary's OVSJG Victim Services line since 2023.`,
    ["Date", "Budget FY", "Stage", "Event", "Change"],
    pe.map(r => [r.event_date, `FY${r.fiscal_year}`, r.event_type.replace("budget_", ""), trunc(r.description, 95), usd(r.amount_change)]),
    [1.1, 1.0, 1.1, 7.43, 1.5],
    { source: `${SRC_BUDGET}; fact_policy_events`, method: "OVSJG events with a dated budget stage and |change| ≥ $2M; P02303 and its PS0023 subtotal are separate printed rows; DHS events are in chart_data/m2_06", chart: "m2_06", note: "A6" },
    { rowsPerSlide: 14, fontSize: 9.5 });

  // 16. m2_05
  const ps = D.readCsv("m2_05_pool_shares");
  X.table("Calvary held 0.7–1.5% of the OVSJG pool outside FY22's building award and moved from 1.1% (2019) to 5.3% (2025) of the DC CoC pool.",
    ["Year", "All OVSJG awards", "Calvary OVSJG", "of which recurring", "Calvary share of OVSJG", "DC CoC awards (DC-500)", "Calvary CoC", "Calvary share of CoC"],
    ps.map(r => [yr(r.fiscal_year), usd(r.ovsjg_total), usd(r.ovsjg_calvary), usd(r.ovsjg_calvary_recurring), pct(num(r.ovsjg_share), 1), num(r.coc_total) == null ? "—" : usd(r.coc_total), num(r.coc_calvary) == null ? "—" : usd(r.coc_calvary), num(r.coc_share) == null ? "—" : pct(num(r.coc_share), 1)]),
    [0.8, 1.7, 1.5, 1.5, 1.5, 1.8, 1.5, 1.83],
    { source: "DC OVSJG award lists (all recipients) and HUD CoC award lists (all DC-500 projects); fact_gov_awards", method: "Calvary ÷ pool total by year; OVSJG by DC FY, CoC by competition year as listed (Calvary CoC column follows the m2_05 alignment)", chart: "m2_05", note: "A2" },
    { rowsPerSlide: 8, fontSize: 11 });

  // 17. Scenarios
  const sp = D.readCsv("m2_07_scenario_parameters"); const sc = D.readCsv("m2_07_scenarios");
  s = X.head("The six scenarios and their parameters are reproducible from config/scenarios.yaml.");
  const pfmt = (p, v) => /share|gov_share/.test(p) ? pct(num(v), 1) : p === "baseline_fy" ? `FY${yr(v).slice(2)}` : usd(v);
  const PL = { baseline_fy: "Baseline year", total_revenue: "Total revenue", total_expenses: "Total expenses", baseline_surplus_deficit: "Surplus / deficit", cash_eoy: "Cash at year end", recognized_gov_revenue: "Recognized government revenue", gov_share: "Government share", alloc_ovsjg: "Apportioned: OVSJG", alloc_coc: "Apportioned: HUD CoC", alloc_dhs: "Apportioned: DHS / TCP", alloc_other: "Apportioned: other federal", nf2_share_of_coc: "New Foundations 2 share of CoC", cost_avoidance_share: "Cost-avoidance share (net view)" };
  tbl(s, ["Baseline parameter (FY25)", "Value"], sp.map(r => [PL[r.parameter] || r.parameter.replace(/_/g, " "), pfmt(r.parameter, r.value)]),
    { x: M, y: BODY_Y, w: 3.9, colW: [2.6, 1.3], fontSize: 9.5, align: ["left", "right"] });
  tbl(s, ["Scenario", "Revenue loss", "% of revenue", "Deficit (gross)", "Deficit (net)", "Cash after 12m (net, months)", "Months to zero (net)"],
    sc.map(r => [r.scenario, usd(r.revenue_loss), pct(num(r.loss_pct_of_total_revenue), 1), usd(r.deficit_gross), usd(r.deficit_net_of_cost_avoidance), num(r.months_of_cash_after_12m_net).toFixed(1), num(r.months_until_cash_zero_net).toFixed(0)]),
    { x: 4.8, y: BODY_Y, w: 7.93, colW: [2.5, 0.9, 0.75, 1.0, 1.0, 0.95, 0.83], fontSize: 9.5, align: ["left", "right", "right", "right", "right", "right", "right"] });
  s.addText("Cuts: S1 OVSJG 10%; S2 OVSJG 25%; S3 CoC 15%; S4 New Foundations 2 lost (30.8% of CoC); S5 DHS/TCP 100%; S6 S2 + S3 + S5. Net view: 50% of a lost stream's revenue is avoidable cost (cost_avoidance_share). Stream amounts are recognized FY25 government revenue apportioned by FY-aligned award ceilings.",
    { x: 4.8, y: 4.75, w: 7.93, h: 1.3, fontSize: 10, color: HEX.text2, margin: 0, isTextBox: true, valign: "top" });
  D.footnote(s, { source: "fact_gov_awards, fact_org_financials (FY25 990); config/scenarios.yaml", method: "apportioned stream amounts × configured cuts; cash after 12 months and months to zero as computed in scripts/02_m2_exposure.py", chart: "m2_07", note: "A4" });

  await D.finish(pres, path.join(__dirname, "appendix_A_calvary_government.pptx"));
})();
