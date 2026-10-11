// Shared deck builder for the Calvary engagement (pptxgenjs structured decks).
// Layouts, footnote block (source / method / trace), native charts from chart_data CSVs, paginated tables, image slides.
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");
const { parse } = require("csv-parse/sync");
const { THEME, HEX } = require("../theme");

const ROOT = path.resolve(__dirname, "..", "..");
const CHART_DATA = path.join(ROOT, "chart_data");
const CHARTS = path.join(ROOT, "charts");
const ASSETS = path.join(ROOT, "decks", "assets");
const AS_OF = "2026-10-10";
const W = 13.333, H = 7.5, M = 0.6;                 // 16:9 canvas, side margin
const HEAD_Y = 0.4, HEAD_H = 1.2, BODY_Y = 1.75, BODY_H = 4.35, BUMPER_Y = 6.2, FOOT_Y = 6.72;

function readCsv(id) {
  const p = path.join(CHART_DATA, `${id}.csv`);
  return parse(fs.readFileSync(p, "utf8"), { columns: true, skip_empty_lines: true });
}
function num(v) { const n = parseFloat(v); return Number.isFinite(n) ? n : null; }
function fmtM(v, d = 1) { return v == null ? "n/a" : `$${(v / 1e6).toFixed(d)}M`; }
function fmtK(v) { return v == null ? "n/a" : `$${Math.round(v / 1e3).toLocaleString()}K`; }
function fmtPct(v, d = 0) { return v == null ? "n/a" : `${(v * 100).toFixed(d)}%`; }
function xmlSafe(s) { return String(s).replace(/&/g, "&amp;"); }

function newDeck(title, subject) {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
  pres.title = title; pres.subject = subject || title; pres.author = "Pro bono analysis for Calvary Women's Services"; pres.company = "Calvary funding engagement";
  const C = pres.SchemeColor;
  const logoWhite = path.join(ASSETS, "logo_mark.png");
  const logoGold = path.join(ASSETS, "logo_chevron.png");
  // TITLE: ink background
  pres.defineSlideMaster({ title: "TITLE", background: { color: HEX.ink }, objects: [
    { placeholder: { options: { name: "title", type: "title", x: M, y: 2.0, w: W - 2 * M - 3.2, h: 1.9, fontSize: 38, bold: true, color: HEX.surface, valign: "bottom", align: "left", margin: 0 }, text: "Title" } },
    { placeholder: { options: { name: "body", type: "body", x: M, y: 4.05, w: W - 2 * M - 3.2, h: 1.6, fontSize: 17, color: HEX.goldLight, valign: "top", align: "left", margin: 0 }, text: "Subtitle" } },
    { image: { path: logoGold, x: W - 4.0, y: H - 2.5, w: 4.0, h: 2.5, altText: "Calvary Women's Services logo" } },
    { text: { text: `Prepared with public data as of ${AS_OF}`, options: { x: M, y: H - 0.8, w: 7, h: 0.4, fontSize: 11, color: HEX.muted, margin: 0 } } },
  ] });
  // SECTION: ink background divider
  pres.defineSlideMaster({ title: "SECTION", background: { color: HEX.ink }, objects: [
    { placeholder: { options: { name: "title", type: "title", x: M, y: 2.4, w: W - 2 * M, h: 1.5, fontSize: 34, bold: true, color: HEX.surface, valign: "bottom", align: "left", margin: 0 }, text: "Section" } },
    { placeholder: { options: { name: "body", type: "body", x: M, y: 4.05, w: W - 2 * M, h: 1.2, fontSize: 16, color: HEX.goldLight, valign: "top", align: "left", margin: 0 }, text: "Takeaway" } },
  ] });
  // HEADLINE: white content frame with footer + logo + slide number
  pres.defineSlideMaster({ title: "HEADLINE", background: { color: HEX.surface }, objects: [
    { placeholder: { options: { name: "title", type: "title", x: M, y: HEAD_Y, w: W - 2 * M, h: HEAD_H, fontSize: 21, bold: true, color: HEX.ink, valign: "top", align: "left", margin: 0 }, text: "Headline" } },
    { image: { path: logoWhite, x: W - 2.15, y: H - 0.95, w: 1.35, h: 0.86, altText: "Calvary Women's Services logo" } },
  ], slideNumber: { x: W - 0.65, y: H - 0.38, w: 0.5, h: 0.3, fontSize: 9, color: HEX.muted } });
  return { pres, C };
}

function footnote(slide, { source, method, chart, note }) {
  // Sourcing rule: source (publisher + clean table), method clause, trace line. 8.5-9 pt muted, bottom-left, up to three lines.
  const lines = [];
  if (source) lines.push({ text: `Source: ${source}`, options: { breakLine: true } });
  if (method) lines.push({ text: `Method: ${method}`, options: { breakLine: true } });
  const trace = [chart ? `Chart ${chart}` : null, `data as of ${AS_OF}`, note ? `method note ${note}` : null].filter(Boolean).join(" · ");
  lines.push({ text: trace, options: {} });
  slide.addText(lines, { x: M, y: FOOT_Y - 0.1, w: W - 2 * M - 2.0, h: 0.78, fontSize: 8.5, color: HEX.muted, valign: "bottom", margin: 0, isTextBox: true, objectName: "footnote" });
}

function titleSlide(pres, title, subtitle, section) {
  const s = pres.addSlide({ masterName: "TITLE", sectionTitle: section });
  s.addText(title, { placeholder: "title" }); s.addText(subtitle, { placeholder: "body" });
  return s;
}
function sectionSlide(pres, title, takeaway, section) {
  const s = pres.addSlide({ masterName: "SECTION", sectionTitle: section });
  s.addText(title, { placeholder: "title" }); s.addText(takeaway, { placeholder: "body" });
  return s;
}
function headlineSlide(pres, headline, section, notes) {
  const s = pres.addSlide({ masterName: "HEADLINE", sectionTitle: section });
  s.addText(headline, { placeholder: "title" });
  if (notes) s.addNotes(notes);
  return s;
}

function bullets(slide, items, { x = M, y = BODY_Y, w = W - 2 * M, h = BODY_H, fontSize = 14 } = {}) {
  const runs = items.map((t, i) => ({ text: t, options: { bullet: { indent: 18 }, breakLine: i < items.length - 1, paraSpaceAfter: 6 } }));
  slide.addText(runs, { x, y, w, h, fontSize, color: HEX.text, valign: "top", margin: 0, isTextBox: true, objectName: "bullets" });
}

function card(slide, { x, y, w, h, title, lines, fontSize = 12.5, tint = HEX.surface2, titleColor = HEX.ink }) {
  slide.addShape("rect", { x, y, w, h, fill: { color: tint }, line: { color: tint }, objectName: `card ${title}` });
  slide.addText(title, { x: x + 0.2, y: y + 0.15, w: w - 0.4, h: 0.5, fontSize: 14, bold: true, color: titleColor, margin: 0, isTextBox: true, valign: "top" });
  const runs = lines.map((t, i) => t.startsWith("**")
    ? { text: t.replace(/^\*\*/, ""), options: { bold: true, color: HEX.ink, breakLine: i < lines.length - 1, paraSpaceAfter: 3 } }
    : { text: t, options: { bullet: { indent: 18 }, breakLine: i < lines.length - 1, paraSpaceAfter: 4 } });
  slide.addText(runs, { x: x + 0.2, y: y + 0.7, w: w - 0.4, h: h - 0.85, fontSize, color: HEX.text, margin: 0, isTextBox: true, valign: "top" });
}

// Card as a band under a full-width chart: title on the left, then one column per claim (with its bullets) or per lone bullet.
function strip(slide, { x, y, w, h, title, lines, fontSize = 10.5, tint = HEX.surface2, titleW = 1.7 }) {
  slide.addShape("rect", { x, y, w, h, fill: { color: tint }, line: { color: tint }, objectName: `card ${title}` });
  slide.addText(title, { x: x + 0.2, y: y + 0.12, w: titleW - 0.2, h: h - 0.24, fontSize: 12, bold: true, color: HEX.ink, margin: 0, isTextBox: true, valign: "top" });
  const groups = [];
  lines.forEach(t => {
    const last = groups[groups.length - 1];
    if (!t.startsWith("**") && last && last[0].startsWith("**")) last.push(t); else groups.push([t]);
  });
  const gap = 0.3, x0 = x + titleW + 0.1, cw = (x + w - 0.2 - x0 - gap * (groups.length - 1)) / groups.length;
  groups.forEach((g, gi) => {
    const runs = g.map((t, i) => t.startsWith("**")
      ? { text: t.replace(/^\*\*/, ""), options: { bold: true, color: HEX.ink, breakLine: i < g.length - 1, paraSpaceAfter: 2 } }
      : { text: t, options: { bullet: { indent: 14 }, breakLine: i < g.length - 1, paraSpaceAfter: 2 } });
    slide.addText(runs, { x: x0 + gi * (cw + gap), y: y + 0.12, w: cw, h: h - 0.24, fontSize, color: HEX.text, margin: 0, isTextBox: true, valign: "top" });
  });
}

// Full-width chart with its commentary as a band underneath; for charts that need the whole width (the m6_03 network).
// IMG_H matches the PNG's drawn height so its fonts are true points. `place` lets the appendices use their own img().
const WIDE_IMG_H = 3.3;
function wideImage(slide, file, { title, lines, fontSize, place = image } = {}) {
  place(slide, file, { x: M, y: BODY_Y, w: W - 2 * M, h: WIDE_IMG_H });
  strip(slide, { x: M, y: BODY_Y + WIDE_IMG_H + 0.1, w: W - 2 * M, h: BODY_H - WIDE_IMG_H - 0.1, title, lines, fontSize });
}

function statTiles(slide, tiles, { y = BODY_Y + 0.1, h = 2.1 } = {}) {
  const n = tiles.length, gap = 0.3, w = (W - 2 * M - gap * (n - 1)) / n;
  tiles.forEach((t, i) => {
    const x = M + i * (w + gap);
    slide.addShape("rect", { x, y, w, h, fill: { color: HEX.surface2 }, line: { color: HEX.surface2 }, objectName: `tile ${t.label}` });
    const size = t.size || (String(t.value).length > 9 ? 26 : String(t.value).length > 6 ? 32 : 40);
    slide.addText(t.value, { x: x + 0.2, y: y + 0.15, w: w - 0.4, h: 1.0, fontSize: size, bold: true, color: t.color || HEX.ink, margin: 0, isTextBox: true, valign: "middle", fit: "shrink" });
    slide.addText(t.label, { x: x + 0.2, y: y + 1.25, w: w - 0.4, h: h - 1.35, fontSize: 11.5, color: HEX.text2, margin: 0, isTextBox: true, valign: "top" });
  });
}

function image(slide, file, { x = M, y = BODY_Y, w = 8.0, h = BODY_H } = {}) {
  const p = path.join(CHARTS, file.endsWith(".png") ? file : `${file}.png`);
  const dims = pngSize(p); let iw = w, ih = h;
  if (dims) { const r = dims.w / dims.h; if (w / h > r) iw = h * r; else ih = w / r; }
  slide.addImage({ path: p, x, y, w: iw, h: ih, objectName: path.basename(p, ".png"), altText: `charts/${path.basename(p)}` });
}
function pngSize(p) {
  try { const b = fs.readFileSync(p); return { w: b.readUInt32BE(16), h: b.readUInt32BE(20) }; } catch (e) { return null; }
}

// Native chart from chart data. series: [{name, values, color}], labels: [...]
function chart(slide, type, labels, series, { x = M, y = BODY_Y, w = 8.0, h = BODY_H, stacked = false, barDir = "col", valFmt = "$#,##0.0,,\"M\"", showLegend = true, catFontSize = 9, dataLabels = false, dataFmt = null, title = null, valMax = null, legendPos = "t", gapWidth = 60 } = {}) {
  const data = series.map(s => ({ name: s.name, labels, values: s.values }));
  const opts = {
    x, y, w, h, barDir, barGrouping: stacked ? "stacked" : "clustered", barGapWidthPct: gapWidth,
    chartColors: series.map(s => s.color),
    // House axis style (engagement lead, 2026-10-11; matches scripts/lib/style.py polish()): no grid lines, black x and y
    // axis lines, bold black axis and data labels.
    catAxisLabelColor: HEX.text, valAxisLabelColor: HEX.text, catAxisLabelFontSize: catFontSize, valAxisLabelFontSize: 9,
    catAxisLabelFontBold: true, valAxisLabelFontBold: true,
    catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt", dataLabelFontFace: "+mn-lt", legendFontFace: "+mn-lt",
    valGridLine: { style: "none" }, catGridLine: { style: "none" }, valAxisLineShow: true, catAxisLineShow: true,
    valAxisLineColor: HEX.text, catAxisLineColor: HEX.text, valAxisLineSize: 1, catAxisLineSize: 1,
    valAxisLabelFormatCode: valFmt, showLegend: showLegend && series.length > 1, legendPos, legendFontSize: 9, legendColor: HEX.text2,
    showValue: dataLabels, dataLabelColor: HEX.text, dataLabelFontSize: 8, dataLabelFontBold: true, dataLabelFormatCode: dataFmt || valFmt,
    dataLabelPosition: stacked ? "ctr" : (type === "line" ? "t" : "outEnd"),
    showTitle: !!title, title, titleColor: HEX.ink, titleFontSize: 11, titleFontFace: "+mn-lt",
    lineSize: 2, lineDataSymbol: "circle", lineDataSymbolSize: 7, lineDataSymbolLineColor: HEX.surface,
    plotArea: { fill: { color: HEX.surface } }, chartArea: { fill: { color: HEX.surface }, roundedCorners: false },
    valAxisMinVal: 0, objectName: title || "chart",
  };
  if (type !== "line") opts.dataBorder = { pt: 0.5, color: HEX.text };  // 1 px black outline on bars, as on the PNG charts
  if (valMax != null) opts.valAxisMaxVal = valMax;
  const t = type === "line" ? slide._presLayout ? "line" : "line" : type;
  slide.addChart(t === "bar" ? "bar" : t === "line" ? "line" : "bar", data, opts);
}

// Paginated table. rows: array of arrays (strings); header: array; colW: array of inches.
function table(pres, section, headline, header, rows, { colW, rowsPerSlide = 12, fontSize = 10, foot, notes } = {}) {
  const pages = []; for (let i = 0; i < rows.length; i += rowsPerSlide) pages.push(rows.slice(i, i + rowsPerSlide));
  if (!pages.length) pages.push([]);
  pages.forEach((page, pi) => {
    const s = headlineSlide(pres, pi === 0 ? headline : `${headline} (continued, ${pi + 1} of ${pages.length})`, section, notes);
    const hdr = header.map(h => ({ text: h, options: { bold: true, color: HEX.ink, fill: { color: HEX.surface2 }, fontSize, valign: "middle" } }));
    const body = page.map(r => r.map(c => ({ text: c == null ? "" : String(c), options: { fontSize, color: HEX.text, valign: "top" } })));
    s.addTable([hdr, ...body], { x: M, y: BODY_Y, w: W - 2 * M, colW, border: { type: "solid", pt: 0.5, color: HEX.grid }, fontFace: "Arial", autoPage: false, margin: 0.05, objectName: "table" });
    if (foot) footnote(s, foot);
  });
}

// Bumper statement: one-line implication in italic above the footnote (Bain pattern).
function bumper(slide, text) {
  slide.addText([{ text: "Implication: ", options: { bold: true, italic: true } }, { text, options: { italic: true } }],
    { x: M, y: BUMPER_Y, w: W - 2 * M - 2.0, h: 0.45, fontSize: 11, color: HEX.ink, margin: 0, isTextBox: true, valign: "middle", objectName: "bumper" });
}

// Bold-claim / evidence-bullet blocks (exec-summary format). blocks: [{claim, bullets:[...]}]
function claimBullets(slide, blocks, { x = M, y = BODY_Y, w = W - 2 * M, h = BODY_H, claimSize = 13, bulletSize = 11.5 } = {}) {
  const runs = [];
  blocks.forEach((b, bi) => {
    runs.push({ text: b.claim, options: { bold: true, fontSize: claimSize, color: HEX.ink, breakLine: true, paraSpaceBefore: bi ? 8 : 0, paraSpaceAfter: 2 } });
    b.bullets.forEach((t, i) => runs.push({ text: t, options: { bullet: { indent: 18 }, fontSize: bulletSize, color: HEX.text, breakLine: !(bi === blocks.length - 1 && i === b.bullets.length - 1), paraSpaceAfter: 2 } }));
  });
  slide.addText(runs, { x, y, w, h, margin: 0, isTextBox: true, valign: "top", objectName: "claims" });
}

async function finish(pres, file) {
  const { applyTheme } = require(process.env.PPTX_SKILL_APPLY_THEME);
  await pres.writeFile({ fileName: file });
  await applyTheme(file, THEME);
  console.log("wrote", file);
}

module.exports = { newDeck, titleSlide, sectionSlide, headlineSlide, bullets, card, strip, wideImage, statTiles, image, chart, table, footnote, bumper, claimBullets, finish, readCsv, num, fmtM, fmtK, fmtPct, xmlSafe, HEX, W, H, M, BODY_Y, BODY_H, BUMPER_Y, AS_OF };
