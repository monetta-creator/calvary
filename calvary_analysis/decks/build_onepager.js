// Executive one-pager: a single slide (Markdown twin in reports/executive_one_pager.md).
const D = require("./lib/deck");
const { HEX, M, W, BODY_Y } = D;
const path = require("path");

(async () => {
  const { pres } = D.newDeck("Calvary Women's Services: funding position and opportunities, one page", "Executive one-pager");
  pres.addSection({ title: "One page" });
  const s = D.headlineSlide(pres, "Calvary has become a system-level provider whose funding needs a better shape and a deeper cushion, not a smaller share.", "One page");
  const colW = (W - 2 * M - 0.6) / 3, y = BODY_Y - 0.2, h = 4.55;
  D.card(s, { x: M, y, w: colW, h, title: "The verdict", lines: [
    "**Public funding at about half of revenue is typical for DC peers (53% FY22–24, 11th of 19).",
    "The shape is the issue: three streams, two through TCP, which carries 74% of a $4.1M award base.",
    "Private grants have held near $1M a year from the same funders, and one partner is 27%.",
    "FY25: −$607K, event income −$483K, 4.4 months of cash (7.5 in FY21).",
    "**Clouds: a cut is proposed every spring (restored twice), losing the DHS/TCP contract would cost ~$960K, and Calvary recognized about two-thirds of known award ceilings in FY24–25.",
    "Rating: moderate-to-high pressure from concentration and liquidity, not from the share.",
  ], fontSize: 11 });
  D.card(s, { x: M + colW + 0.3, y, w: colW, h, title: "The top opportunities", lines: [
    "**Draw every awarded dollar and confirm the DHS and Sisters Rise contracts with TCP (day 30).",
    "**Upgrade current partners to multi-year: GWCF (Health Equity Fund successor), Cafritz (Mar 1 / Jul 1 / Nov 1), Abell, Fowler, United Way NCA, Bank of America (day 45).",
    "**Open foundations that fund Calvary's peers: Clark Charitable ($7.8M to five peers, median $250K), Schattner, Cohen, Bernstein, The Washington Home, and re-engage Many Hands, World Bank CCF and Jane Bancroft Robinson (day 60–90).",
    "**Restore the event line and start a major-gifts / DAF program (peers raise 40–50% of filed grants via DAFs, Calvary 25%).",
    "**Formalize workforce and behavioral health: $30M and $21M a year of nearby DMV grant pools, without changing the mission.",
  ], fontSize: 11 });
  D.card(s, { x: M + 2 * (colW + 0.3), y, w: colW, h, title: "Headline recommendations and next steps", lines: [
    "**A six-month reserve target (~$2.8M) and a plan to close the FY25 gap in the FY26 budget.",
    "**An annual advocacy and monitoring calendar for the spring budget season, with monthly draw-down tracking.",
    "**A private-revenue goal of ~$3M within three years, bringing the public share to about half at flat public funding.",
    "Next come your reactions, then the FY24–25 audits, the TCP subgrant agreements and the FY25 gala calendar, then a working session to turn the eleven Tier 1 targets into assignments.",
    "What follows: the leadership deck (22 content slides), the consulting deck (55 content slides), appendix decks A–D, and four reports.",
  ], fontSize: 11 });
  D.bumper(s, "Calvary has built the case, and the next five years need the public base fully drawn, the private base deeper, and a cushion for the spring.");
  D.footnote(s, { source: "IRS 990 and funders' 990-PF/Schedule I filings; Calvary audits FY13–FY23; DC OVSJG and HUD CoC award lists; DC Council oversight responses; DC budget books FY2024–27; HUD HIC/PIT; ACS 2020–24 — all in the engagement's clean tables (calvary_funding_data/clean)", method: "every figure maps to a chart-data file and a registered source; core peers are provisional; FY24–25 government figures rest on the 990", chart: "m1_02, m2_01, m2_07, m5_01, m7_00, m8_01" });
  await D.finish(pres, path.join(__dirname, "executive_one_pager.pptx"));
})();
