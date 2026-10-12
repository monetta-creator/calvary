// <Deck name> (<n> headline slides): storylines/<slug>_headline_spine.md and <slug>_storyline.md.
// Copy to calvary_analysis/decks/build_<slug>.js, then add the deck to decks/build_all.sh.
const D = require("./lib/deck");
const { HEX, M, W, BODY_Y, BODY_H } = D;
const path = require("path");

(async () => {
  const { pres } = D.newDeck("<Deck title>", "<subject line>");
  const S = (t) => pres.addSection({ title: t });
  const CHART_W = 8.0, CARD_X = M + CHART_W + 0.3, CARD_W = W - M - CARD_X;

  // 1 title
  S("Opening");
  D.titleSlide(pres, "<Deck title>", "<one-line subtitle: who it is for and what it covers>", "Opening");

  // 2 executive summary: bold claims carry the argument, bullets carry the numbers
  let s = D.headlineSlide(pres, "<Answer-first headline, a full sentence of 20 words or fewer.>", "Opening");
  D.claimBullets(s, [
    { claim: "Situation: <...>", bullets: ["<number, with its chart ID in the footnote>"] },
    { claim: "Complication: <...>", bullets: ["<...>"] },
    { claim: "Resolution: <...>", bullets: ["<...>"] },
  ], { claimSize: 18, bulletSize: 15 });
  D.footnote(s, { source: "<publisher and document; clean table>", method: "<measure in one clause>", chart: "<chart IDs>" });

  // 3 a chart slide: native chart from chart data, commentary card, implication, footnote
  s = D.headlineSlide(pres, "<Headline stating the takeaway.>", "<Section>");
  const rows = D.readCsv("<chart_id>");  // calvary_analysis/chart_data/<chart_id>.csv
  D.chart(s, "bar", rows.map(r => r.<label_column>), [
    { name: "<series name>", values: rows.map(r => D.num(r.<value_column>)), color: HEX.government },
  ], { x: M, y: BODY_Y, w: CHART_W, h: BODY_H, barDir: "bar", dataLabels: true, showLegend: false });
  D.card(s, { x: CARD_X, y: BODY_Y, w: CARD_W, h: BODY_H, title: "<card title>", lines: ["**<bold lead sentence>", "<evidence line>"] });
  D.bumper(s, "<what this means for Calvary's choices>.");
  D.footnote(s, { source: "<...>", method: "<...>", chart: "<chart_id>", note: "<method note, if any>" });

  // n closing: decisions needed, stated explicitly
  s = D.headlineSlide(pres, "<The next steps are ... and the decisions needed are ...>", "Closing");
  D.bullets(s, ["<decision 1>", "<decision 2>"]);

  await D.finish(pres, path.join(__dirname, "<file_stem>.pptx"));
})();
