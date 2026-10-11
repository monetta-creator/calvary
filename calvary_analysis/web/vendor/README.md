# Vendored files for the Calvary Grantmaker Web

Embedded into `../Calvary_Grantmaker_Web.html` by `../build_network_page.py` so the page opens offline from disk.
The published artifact (`../publish/funder_network.html`) loads the same d3 build from cdnjs and the fonts from Google Fonts instead.

| File | Source | SHA-256 | License |
|---|---|---|---|
| `d3-7.9.0.min.js` | https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js (byte-identical to jsDelivr `d3@7.9.0/dist/d3.min.js`) | f2094bbf6141b359722c4fe454eb6c4b0f0e42cc10cc7af921fc158fceb86539 | ISC, `LICENSE-d3.txt` |
| `fonts/BricolageGrotesque.woff2` | Google Fonts, variable font, Latin subset (retrieved 2026-10-11) | 85f55a58a31e61a2e19e8bb25fed503181bf2a6b4cab76c589992cfaac377447 | SIL OFL 1.1, `fonts/OFL-BricolageGrotesque.txt` |
| `fonts/PublicSans.woff2` | Google Fonts, variable font, Latin subset (retrieved 2026-10-11) | c1b6da516e0062e9c2f341b3a51dd2d621d946da72f06c6cfe05fd9d2dd8622d | SIL OFL 1.1, `fonts/OFL-PublicSans.txt` |

`fonts/fonts.json` holds the weight range and unicode-range each `@font-face` declares.
