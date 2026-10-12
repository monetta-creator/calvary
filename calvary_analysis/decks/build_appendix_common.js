// Shared helpers for the four appendix decks (build_appendix_A.js ... build_appendix_D.js).
// Wraps lib/deck.js (unchanged) with the slide patterns from build_consulting.js plus side-by-side tables.
const fs = require("fs");
const path = require("path");
const { parse } = require("csv-parse/sync");
const D = require("./lib/deck");
const { HEX, M, W, BODY_Y, BODY_H } = D;

const ROOT = path.resolve(__dirname, "..");          // calvary_analysis/
const PROJECT = path.resolve(ROOT, "..");           // folder holding calvary_funding_data/ and calvary_analysis/
const CHART_W = 8.0, CARD_X = M + CHART_W + 0.3, CARD_W = W - M - CARD_X, FULL_W = W - 2 * M;

// Read any CSV under the project root (relative path).
function readAny(rel) { return parse(fs.readFileSync(path.join(PROJECT, rel), "utf8"), { columns: true, skip_empty_lines: true }); }
function readText(rel) { return fs.readFileSync(path.join(PROJECT, rel), "utf8"); }

// Title-case organization names that arrive in upper case; leave mixed-case names alone.
const KEEP_UPPER = new Set(["DC", "NCA", "USA", "US", "LLC", "LLP", "II", "III", "IV", "GWCF", "DASH", "SAFE", "TCP", "HUD", "DHS", "OVSJG", "AAMC", "MGAC", "IMF", "CBWC", "DWC", "LA", "MD", "VA", "NY", "UA", "PC", "AOGF", "NPT", "YMCA", "YWCA", "KPMG", "RCLCO", "AARP", "PNC", "CFC", "FEMA", "EFSP", "SNAP", "PSH", "TH", "DV", "EHV", "CRM", "CPF", "SLFRF", "PPP", "FBO", "NW", "SE", "NE", "SW", "ACS", "DCHA", "DBH", "DOES", "TANF", "ERAP", "FRSP", "VOCA", "ESG", "CDBG", "FY", "CSX", "AT&T", "SAIC", "GEICO", "IBM", "MGM", "CPMG", "UNCF", "AFL-CIO", "NFL", "NBA", "SEIU", "WGL"]);
const LOWER = new Set(["of", "the", "and", "for", "in", "on", "at", "to", "a", "an", "by"]);
const SPECIAL = { JPMORGAN: "JPMorgan", PAYPAL: "PayPal", IMPACTASSETSINC: "ImpactAssets Inc", IMPACTASSETS: "ImpactAssets", BLACKROCK: "BlackRock", FEDEX: "FedEx", MCDONALDS: "McDonalds", "MCDONALD'S": "McDonald's" };
function tc(s) {
  s = String(s == null ? "" : s).trim();
  if (!s || /[a-z]/.test(s)) return s;
  let i = 0;
  return s.split(/(\s+)/).map(tok => {
    if (/^\s+$/.test(tok)) return tok;
    const idx = i++;
    if (SPECIAL[tok]) return SPECIAL[tok];
    if (KEEP_UPPER.has(tok.replace(/[.,;:()]/g, ""))) return tok;
    const low = tok.toLowerCase();
    if (idx > 0 && LOWER.has(low)) return low;
    return low.replace(/(^|[-/(&.])([a-z])/g, (m, p, c) => p + c.toUpperCase()).replace(/'S\b/g, "'s");
  }).join("");
}
// Truncate at a word boundary with an ellipsis.
function trunc(s, n = 70) {
  s = String(s == null ? "" : s).replace(/\s+/g, " ").trim();
  if (s.length <= n) return s;
  const cut = s.slice(0, n - 1); const sp = cut.lastIndexOf(" ");
  return (sp > n * 0.6 ? cut.slice(0, sp) : cut).replace(/[,;:\s]+$/, "") + "…";
}
const num = D.num;
function usd(v) { v = num(v); return v == null ? "—" : (v < 0 ? "−$" : "$") + Math.round(Math.abs(v)).toLocaleString("en-US"); }
function money(v, d = 2) { v = num(v); if (v == null) return "—"; const a = Math.abs(v), sg = v < 0 ? "−" : ""; if (a >= 1e6) return `${sg}$${(a / 1e6).toFixed(d)}M`; if (a >= 1e3) return `${sg}$${Math.round(a / 1e3).toLocaleString("en-US")}K`; return `${sg}$${Math.round(a)}`; }
function pct(v, d = 0) { v = num(v); return v == null ? "—" : `${(v * 100).toFixed(d)}%`; }
function n0(v) { v = num(v); return v == null ? "—" : Math.round(v).toLocaleString("en-US"); }
function yn(v) { return v === "True" || v === true ? "yes" : v === "False" || v === false ? "no" : (v || "—"); }
function ty(v) { v = num(v); return v == null ? "—" : `TY${Math.round(v)}`; }

// Native-looking table at an arbitrary position (same style as D.table).
function tbl(slide, header, rows, { x = M, y = BODY_Y, w = FULL_W, colW, fontSize = 9, align } = {}) {
  const hdr = header.map((h, j) => ({ text: h, options: { bold: true, color: HEX.ink, fill: { color: HEX.surface2 }, fontSize, valign: "middle", align: align ? align[j] : "left" } }));
  const body = rows.map(r => r.map((c, j) => ({ text: c == null ? "" : String(c), options: { fontSize, color: HEX.text, valign: "top", align: align ? align[j] : "left", bold: !!(r._bold) } })));
  slide.addTable([hdr, ...body], { x, y, w, colW, border: { type: "solid", pt: 0.5, color: HEX.grid }, fontFace: "Arial", autoPage: false, margin: 0.04, objectName: "table" });
}

function pngRatio(file) {
  const p = path.join(ROOT, "charts", file.endsWith(".png") ? file : `${file}.png`);
  const b = fs.readFileSync(p); return b.readUInt32BE(16) / b.readUInt32BE(20);
}
// Same as D.image (aspect-fit inside the box) but sets alt text, so no absolute file path lands in the slide XML.
function img(slide, file, { x = M, y = BODY_Y, w = 8.0, h = BODY_H } = {}) {
  const name = file.endsWith(".png") ? file : `${file}.png`;
  const p = path.join(ROOT, "charts", name);
  const r = pngRatio(name); let iw = w, ih = h;
  if (w / h > r) iw = h * r; else ih = w / r;
  slide.addImage({ path: p, x, y, w: iw, h: ih, objectName: name, altText: `Chart ${name.replace(/\.png$/, "")} (charts/${name})` });
}
function yr(v) { v = num(v); return v == null ? "—" : String(Math.round(v)); }

function makeDeck(title, subject) {
  const { pres } = D.newDeck(title, subject);
  const ctx = { pres, sec: null };
  ctx.section = (t) => { pres.addSection({ title: t }); ctx.sec = t; return t; };
  ctx.title = (t, sub) => D.titleSlide(pres, t, sub, ctx.sec);
  ctx.head = (headline) => D.headlineSlide(pres, headline, ctx.sec);
  // PNG left + optional commentary card right.
  ctx.png = (headline, png, cardTitle, lines, foot, { wide = 0.4, cardFont = 11 } = {}) => {
    const s = ctx.head(headline);
    if (lines) {
      const r = pngRatio(png), maxW = CHART_W + wide;
      const iw = Math.min(maxW, BODY_H * r);
      img(s, png, { x: M, y: BODY_Y, w: iw, h: BODY_H });
      const cx = M + iw + 0.3;
      D.card(s, { x: cx, y: BODY_Y, w: W - M - cx, h: BODY_H, title: cardTitle, lines, fontSize: cardFont });
    } else {
      // centre a full-width image
      const r = pngRatio(png), iw = Math.min(FULL_W, BODY_H * r), ih = iw / r;
      img(s, png, { x: (W - iw) / 2, y: BODY_Y, w: iw, h: ih });
    }
    D.footnote(s, foot); return s;
  };
  // Native chart left + optional card right.
  ctx.nat = (headline, spec, cardTitle, lines, foot, { cardFont = 11 } = {}) => {
    const s = ctx.head(headline);
    const w = lines ? CHART_W : FULL_W;
    D.chart(s, spec.type || "bar", spec.labels, spec.series, Object.assign({ x: M, y: BODY_Y, w, h: BODY_H }, spec.opts || {}));
    if (lines) D.card(s, { x: CARD_X, y: BODY_Y, w: CARD_W, h: BODY_H, title: cardTitle, lines, fontSize: cardFont });
    D.footnote(s, foot); return s;
  };
  // Paginated full-width table (D.table).
  ctx.table = (headline, header, rows, colW, foot, { rowsPerSlide = 12, fontSize = 9 } = {}) => {
    const total = colW.reduce((a, b) => a + b, 0);
    if (total > 12.13 + 1e-6) throw new Error(`colW total ${total} > 12.13 for: ${headline}`);
    D.table(pres, ctx.sec, headline, header, rows, { colW, rowsPerSlide, fontSize, foot });
  };
  return ctx;
}

module.exports = { D, HEX, M, W, BODY_Y, BODY_H, CHART_W, CARD_X, CARD_W, FULL_W, readAny, readText, tc, trunc, num, usd, money, pct, n0, yn, ty, yr, tbl, img, makeDeck, pngRatio };
