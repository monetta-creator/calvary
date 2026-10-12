// Write the deck palette (theme.js THEME.colors) into the PowerPoint theme part after pptxgenjs saves a deck.
// pptxgenjs sets fonts but always writes Office's default color scheme, so theme colors (chart defaults, "accent 1" in
// the PowerPoint picker) would otherwise be Office blue and orange. Uses jszip, which pptxgenjs already installs.
const fs = require("fs");
const JSZip = require("jszip");

const SLOTS = ["dk1", "lt1", "dk2", "lt2", "accent1", "accent2", "accent3", "accent4", "accent5", "accent6", "hlink", "folHlink"];
const xmlAttr = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

function colorScheme(theme) {
  const missing = SLOTS.filter((k) => !/^[0-9A-Fa-f]{6}$/.test(String(theme.colors[k] || "")));
  if (missing.length) throw new Error(`theme.js THEME.colors needs six-digit hex values for: ${missing.join(", ")}`);
  const slots = SLOTS.map((k) => `<a:${k}><a:srgbClr val="${theme.colors[k].toUpperCase()}"/></a:${k}>`).join("");
  return `<a:clrScheme name="${xmlAttr(theme.name)}">${slots}</a:clrScheme>`;
}

async function setThemeColors(pptxPath, theme) {
  const zip = await JSZip.loadAsync(fs.readFileSync(pptxPath));
  const parts = Object.keys(zip.files).filter((p) => /^ppt\/theme\/theme\d+\.xml$/.test(p));
  if (!parts.length) throw new Error(`${pptxPath}: no ppt/theme/theme*.xml part`);
  const scheme = colorScheme(theme);
  for (const part of parts) {
    const xml = await zip.file(part).async("string");
    if (!/<a:clrScheme\b/.test(xml)) throw new Error(`${pptxPath}: ${part} has no color scheme to replace`);
    zip.file(part, xml.replace(/<a:clrScheme\b[\s\S]*?<\/a:clrScheme>/, scheme));
  }
  fs.writeFileSync(pptxPath, await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" }));
}

module.exports = { setThemeColors };
