// Theme for all Calvary decks: executable version of storylines/design_system.md.
// Hex without '#'. Fonts from the safe list (Arial) so LibreOffice QA renders true to width.
const THEME = {
  name: "Calvary Funding Engagement",
  headFontFace: "Arial",
  bodyFontFace: "Arial",
  colors: {
    dk1: "1F1B1D",      // text
    lt1: "FFFFFF",      // surface
    dk2: "41242F",      // ink (brand plum): titles, dark slides
    lt2: "F6F3F4",      // surface_2: card tint
    accent1: "A03F7E",  // government / Calvary
    accent2: "B8810C",  // institutional philanthropy
    accent3: "0F9ACB",  // DAF / named comparators
    accent4: "CF5A2C",  // individuals / events
    accent5: "3B6FD8",  // other revenue
    accent6: "D39F28",  // brand gold: emphasis
    hlink: "41242F",
    folHlink: "8C8488",
  },
};
const HEX = {
  ink: "41242F", gold: "D39F28", goldLight: "FFDD7F", text: "1F1B1D", text2: "5C5458", muted: "8C8488", grid: "E6E2E4",
  surface: "FFFFFF", surface2: "F6F3F4", government: "A03F7E", institutional: "B8810C", daf: "0F9ACB", individuals: "CF5A2C",
  other: "3B6FD8", peer: "B9B2B6", negative: "B23A48", positive: "2E7D5B",
};
module.exports = { THEME, HEX };
