import csv, os
OUT = os.path.dirname(os.path.abspath(__file__))

# document short names (relative paths)
D = {
 "op_deck": "decks_md/executive_one_pager.md",
 "ld": "decks_md/leadership_deck.md",
 "cd": "decks_md/consulting_deck.md",
 "apA": "decks_md/appendix_A_calvary_government.md",
 "apB": "decks_md/appendix_B_peers_comparators.md",
 "apC": "decks_md/appendix_C_funders_pipeline.md",
 "apD": "decks_md/appendix_D_data_methods.md",
 "op": "reports/executive_one_pager.md",
 "es": "reports/executive_summary.md",
 "ff": "reports/full_findings.md",
 "meth": "reports/methodology.md",
 "rec": "reports/recommendations.md",
 "br": "reports/board_readout.md",
 "cb": "reports/consulting_briefing.md",
 "verdict": "recommendations/funding_pressure_verdict.md",
 "strat": "recommendations/strategic_recommendations.md",
 "plan": "recommendations/action_plan_90day.csv",
 "pipe": "recommendations/funder_pipeline.csv",
 "reg": "insight_register.csv",
 "m1": "modules/m1_calvary_trajectory.md", "m2": "modules/m2_government_exposure.md",
 "m3": "modules/m3_peer_benchmarking.md", "m4": "modules/m4_funder_landscape.md",
 "m5": "modules/m5_funder_gaps.md", "m6": "modules/m6_network.md", "m7": "modules/m7_pipeline.md",
 "m8": "modules/m8_expansion_scan.md", "m9": "modules/m9_need_capacity.md", "m10": "modules/m10_comparator_profiles.md",
 "lspine": "storylines/leadership_headline_spine.md", "cspine": "storylines/consulting_headline_spine.md",
 "aspine": "storylines/appendix_headline_spine.md",
 "readme": "README.md", "cp3": "checkpoints/cp3_memo.md",
}

M = []  # metric_id, metric, doc, location, value, note
def add(mid, metric, rows):
    for doc, loc, val, *note in rows:
        M.append([mid, metric, D[doc], loc, val, note[0] if note else ""])

add(1, "Real revenue growth FY19->FY25 (%)", [
 ("op","What Calvary has built","59% in real terms"),("op_deck","slide 1","not stated on the one-page slide"),
 ("es","§1","59% in real terms"),("br","Opening","up 59% in real terms since FY19"),("ff","Summary M1; M1 finding 1","59%"),
 ("m1","Findings 1","59%"),("reg","M1-01 evidence","Revenue $2.49M FY19 -> $4.97M FY25 (growth % not stated)"),
 ("lspine","#3","59% in real terms"),("cspine","#6","59% in real terms"),("ld","slides 2, 3","59% (2024 dollars)"),("cd","slide 7","+59% real FY19->FY25"),
 ("apA","slide 4 table","Revenue 2024$: FY19 $3,051,134 -> FY25 $4,840,626 (=+58.7%)"),
])
add(2, "Revenue FY19 and FY25 ($M)", [
 ("op","What Calvary has built","$2.49M -> $4.97M (paired with 'real terms' growth; figures are nominal)"),("es","§1","$2.49M -> $4.97M"),
 ("ld","slide 3","$2.49M -> $4.97M labelled '2024 dollars'","nominal figures mislabelled as real; 2024$ values are $3.05M -> $4.84M"),
 ("cd","slide 7","$1.45M (FY11) -> $4.97M (FY25) nominal; chart FY19 2,486,678 / 3,051,134 real"),
 ("m1","Findings table","FY19 $2.49M; FY25 $4.97M"),("ff","M1 table","FY19 $2.49M; FY25 $4.97M"),("reg","M1-01 evidence","$2.49M FY19 -> $4.97M FY25"),
 ("apA","slides 2, 4","FY19 $2,486,678; FY25 $4,967,995; real $3,051,134 / $4,840,626"),("meth","§3.3","FY25 $4,967,995"),
])
add(3, "Beds 2022 and 2025", [
 ("op","What Calvary has built","68 (2022) -> 124 (2025)"),("es","§1","68 (2022) -> 124 (2025)"),("br","Opening","68 -> 124"),
 ("ff","Purpose; M9 finding 3","68 -> 124; 94 TH, 16 PSH, 14 RRH"),("m9","Findings 3","68 -> 124"),("reg","M9-02","124 beds"),
 ("ld","slides 2, 3","68 -> 124"),("cd","slide 58","2022 68; 2023 98; 2024 107; 2025 124"),("lspine","#3","124 beds"),("cspine","#49","124 beds"),
])
add(4, "Share of DC transitional-housing beds (%)", [
 ("op","What Calvary has built","6.8%"),("es","§1","6.8% (2.5% three years earlier)"),("br","Opening","almost 7%"),
 ("ff","Summary M9; M9 finding 3","6.8% (up from 2.5%)"),("m9","Findings 3","6.8%, up from 2.5%"),("reg","M9-02","7%"),
 ("ld","slides 2, 3","6.8% (2.5% in 2022)"),("cd","slide 58","2022 2.5%; 2023 4.9%; 2024 3.5%; 2025 6.8%"),
])
add(5, "Recurring government award base ($M) and year", [
 ("op","What Calvary has built","about $4.1M a year (no year)"),("es","§1","about $4.1M a year"),("br","Opening","about $4.1M a year"),
 ("verdict","Evidence table","$4.1M (2024): OVSJG $0.91M, CoC $1.76M, DHS $1.42M"),("rec","§1","$4.1M award base"),("cb","§2","$4.1M award base"),
 ("m2","Findings 1","$0.9M (2019) -> $4.1M (2024)"),("ff","Summary M2; M2 finding 1","$4.1M (2024), up from $0.9M (2019)"),("reg","M2-01","$0.9M (2019) -> about $4.1M (2024)"),
 ("lspine","#5","$4.1M a year"),("cspine","#12","$0.9M (2019) to $4.1M (2024)"),("ld","slides 1, 2, 5","$4.1M award base / $4.1M a year"),("cd","slides 14, 63","$4.1M (2024)"),
 ("apA","slides 10-12","2024 components: OVSJG $913,401; CoC $1,761,352; DHS $1,423,664 (= $4.10M)"),
])
add(6, "Funders with filed grants TY2020-24", [
 ("op","What Calvary has built","50"),("es","§1","50"),("br","Opening","Fifty"),("m1","Findings 4; A3","50 funders, $4.43M"),("reg","M1-04 evidence","50 funders"),
 ("ld","slide 3","50 funders"),("cd","slide 12","$4.43M from 50 funders"),("apA","slide 6","Fifty funders"),("apB","slide 6","Funders 50; institutional 42"),("meth","A3","138 rows from 50 funders, $4.43M"),("apD","slide 12","138 rows from 50 funders, $4.43M"),
])
add(7, "Government share FY22-24 mean (%)", [
 ("es","§2","53% on average for FY22-24"),("rec","§1","53%"),("cb","§2","53%"),("verdict","Verdict; Evidence","53%"),("m3","Findings table","53%"),("ff","M3 table/finding 1; verdict copy","53%"),
 ("reg","M3-01","53%"),("op_deck","slide 1","53% FY22-24"),("ld","slides 2, 4","53%"),("cd","slides 22, 63","52.5% (chart) / 53%"),("apB","slide 4","53%"),("cspine","#19","53%"),
])
add(8, "Government share FY25 (%)", [
 ("es","§2","58%"),("rec","§1","58%"),("verdict","Verdict","58%"),("strat","Goal","58%"),("m1","Findings table","58%"),("ff","M1 table","58%"),("reg","M1-01 evidence","line 1e 58% FY25"),
 ("cd","slides 8, 9, 63","58%"),("apA","slides 3, 22","58% / 58.2%"),("apB","slide 9","58%"),
])
add(9, "Government share range since FY15 (%-%) and yearly shares", [
 ("es","§2","40-61% every year since FY15"),("m1","Findings 1; table","40-61%; table FY19 49%, FY21 50%, FY22 61%, FY23 51%, FY24 45%, FY25 58%"),
 ("ff","M1 finding 1 vs M1 table","text 40-61%; table FY19 51%, FY21 51%, FY22 64%, FY23 55%, FY24 45%, FY25 58%","table uses 990 revenue as denominator for audit-basis government (mixed basis); contradicts own text and m1"),
 ("ff","Consistency notes #1","says readout table gives 51%, 64%, 55% (stale; readout now gives 50/61/51)"),
 ("reg","M1-01","40%-61%; 37% FY14 -> 50% FY21 -> 61% FY22 -> 51% FY23; 45% FY24, 58% FY25"),("cp3","§2","40-61% (audited gov ÷ audited revenue; was 44-64% with mixed denominator)"),
 ("ld","slide 4","40-61%"),("cd","slides 8, 9","FY15 41 ... FY22 61, FY23 51, FY24 45, FY25 58"),("apA","slide 3","audit basis FY13 40% ... FY22 61%, FY23 51%; line-1e FY22 64%, FY23 55%"),("apB","slide 9","Calvary between 40% and 61% every year"),("cspine","#7","40-61%"),
])
add(10, "Peer rank ('Nth of 19')", [
 ("es","§2","11th of 19"),("br","Funding picture","11th of 19"),("rec","§1","11th of 19"),("cb","§2","11th of 19"),("verdict","Evidence","11th of 19"),("m3","Findings 1 (no rank stated)","-"),
 ("ff","Summary; verdict copy; register summary","11th of 19 / 11 of 19"),("ff","Consistency notes #5","stale: says readout gives no rank and register says 75-94%"),
 ("reg","M3-01","11 of 19; DV providers 70-89%"),("cp3","§2","11th of 19 (not 12th)"),("op_deck","slide 1","11th of 19"),("ld","slides 2, 4","11th of 19"),("cd","slide 22","11th of 19 (chart position 9th-lowest of 21 incl. LA rows)"),("cspine","#19","11th of 19"),
])
add(11, "DC sector percentile", [
 ("es","§2","near the median of DC's human-services sector"),("verdict","Evidence","57th (DC sector FY23), 46th (national women's/DV FY22)"),("m3","Findings 1","57th DC; 46th national"),("ff","Summary M3","57th DC, 46th national"),
 ("reg","M3-02","57% percentile DC (n=163); 57% size-matched; 46% national women's"),("ld","slide 4","57th percentile"),("cd","slides 23, 63","57th / 46th"),("apB","slide 11","57th / 57th / 46th"),("cspine","#20","57th / 46th"),
])
add(12, "Share of award base through TCP (%)", [
 ("op","Verdict","74% of the base"),("es","§2","TCP carries 74% of the base"),("br","Funding picture","about three-quarters"),("rec","§1","74% of a $4.1M award base"),("cb","§2","74% of a $4.1M award base"),
 ("verdict","Verdict; Evidence","about 74% of recurring award base"),("strat","§1","74%"),("m2","Findings 1","about 74%"),("ff","M2 finding 1","about 74%"),
 ("op_deck","slide 1","74% of a $4.1M award base"),("ld","slides 2, 5","74% of a $4.1M award base / TCP carries 74% of the base"),("cd","slide 63","74% of the $4.1M recurring award base"),
 ("apA","slide 22 / m2 method","FY25 ceiling apportionment CoC 41% + DHS 33% = 74% of $4.29M FY25-aligned ceilings; on the 2024 $4.10M base TCP = (1.76+1.42)/4.10 = 78%","74% and $4.1M are on different bases"),
])
add(13, "OVSJG FY26 award ($M)", [
 ("es","§2","$1.05M in FY26"),("m2","Findings 1","$0.37M (FY20) -> $1.05M (FY26)"),("m3","Findings 6","$1.05M"),("ff","M2 finding 1","$1.05M (FY26)"),("reg","M2-01; M2-04","$1.05M FY26; $1.05M of $96.7M"),
 ("ld","slide 5","$0.37M (FY20) -> $1.05M (FY26)"),("cd","slides 14, 30","$1.05M; $1,050,651"),("apA","slides 10, 21","$1,050,651 (FY2026)"),("cspine","#27","$1.05M"),
 ("verdict","Evidence (2024 base)","OVSJG $0.91M (2024)"),
])
add(14, "HUD CoC award ($M) and year label", [
 ("es","§2","$1.77M in FY2025"),("m2","Findings 1","$0.24M (2019) -> $1.77M (FY2025)"),("m3","Findings 6","$1.77M"),("ff","M2 finding 1","$1.77M (FY2025)"),("reg","M2-01; M2-04","$1.77M (FY2025 awards); $1.77M of $33.5M"),
 ("verdict","Evidence","HUD CoC via TCP $1.76M (2024)"),("ld","slide 5","$0.24M (2019) -> $1.77M (FY2025), three projects"),("cd","slides 14, 19, 30","$240K (2019) -> $1.77M (FY2025); $1,766,814"),
 ("apA","slide 11","competition 2024 $1,761,352 (Calvary FY25); 2025 $1,766,814 (Calvary FY26)"),
])
add(15, "DHS/TCP award ($M)", [
 ("es","§2","$1.42M in FY2024"),("verdict","Evidence","$1.42M"),("m2","Findings 1","$1.42M (FY2024: TH $830K, Sisters Rise $593K)"),("ff","M2 finding 1","$1.42M"),("reg","M2-01","$1.42M in FY2024"),
 ("ld","slide 5","$1.42M in FY2024 ($830K + $593K)"),("cd","slides 14, 15","$1.42M (FY2024 only); $830K; $593K"),("apA","slide 12","$830,384 + $593,280 = $1,423,664"),
])
add(16, "Filed grants per year ($M-$M) and funders per year", [
 ("es","§2","$0.64-1.17M a year from 26-29 funders"),("verdict","Evidence","$0.64-1.17M/yr; 26-29 funders/yr"),("br","Funding picture","about a million a year, 26 to 29 funders"),("rec","§1","about $1M a year from 26-29 funders"),("cb","§2","~$1M/yr from 26-29 funders"),
 ("m1","Findings 4","~$1M/yr from 26-29 funders"),("ff","M1 finding 4","~$1M/yr from 26-29 funders"),("reg","M1-04","near $1M a year from 26-29 funders"),
 ("ld","slide 6","$0.64-1.17M a year from 26-29 funders"),("cd","slide 12","TY2020 $637K (27 funders) ... TY2024 $1.17M (26)"),("cspine","#11","near $1M a year from 26-29 funders"),
])
add(17, "GWCF share of five-year filed grants (%) and top-five share", [
 ("op","Verdict","one of them 27%"),("es","§2","27%; top five 63%"),("verdict","Verdict; Evidence","27%; top five 63%"),("rec","§1","27%"),("cb","§2","GWCF 27%"),("m1","Findings 4","27% ($1.21M of $4.43M); top five 63%; HHI 1,168"),
 ("ff","M1 finding 4","27%; 63%"),("reg","M1-04","27%; top five 63%; HHI 1168"),("ld","slides 1, 6","27%; top five 63%"),("cd","slides 12, 63","27%, top five 63%"),("apA","slide 6","27.2%; top ten 79%; cumulative at rank 5 = 63.4%"),("cspine","#11","27%"),
])
add(18, "DAF receipts five years ($M) and DAF share (%)", [
 ("es","§2; §3","about $1.1M over five years; Calvary 25%"),("op","Opportunities 4","Calvary 25%"),("m1","Findings 4","$1.09M over five years"),("m3","Findings 4","Calvary 25%"),("m4","Findings 4","$1.1M over five years (25% of filed grants)"),
 ("strat","§2","Fidelity, Benevity and Schwab route $1.1M over five years"),("reg","M1-04; M4-04","DAF $1.09M; $1.1M, 25%"),("ld","slides 6, 14","$1.1M; 25%"),("cd","slides 12, 28, 35","$1.09M; 25%; $1.1M (Benevity $512K, Fidelity $314K, Schwab $128K)"),("apB","slide 6","DAF $1.09M; DAF share 25%"),
])
add(19, "FY25 deficit ($K)", [
 ("op","Verdict","$607K"),("es","§2","$607K"),("br","Funding picture","$607K"),("verdict","Verdict","$607K"),("rec","§1","$607K"),("cb","§2","-$607K"),("strat","§3","$607K on $5.58M expenses"),
 ("m1","Findings","-$607K"),("m2","Scenarios baseline","-$607K"),("ff","M1","-$607K"),("reg","M1-02","$607K"),("ld","slides 1, 2, 7, 10","-$607K"),("cd","slides 10, 20, 63","-$607K"),("apA","slides 4, 22","-$607,326"),
])
add(20, "Event contributions FY24, FY25 and drop", [
 ("op","Verdict","event income down $483K"),("es","§2","$483K drop"),("br","Funding picture","$538K to $55K"),("verdict","Verdict; Evidence","$538K -> $55K"),("rec","§1","down $483K"),("cb","§2","-$483K"),("strat","§2","$483K drop"),
 ("m1","Findings 3","$538K -> $55K"),("ff","M1 finding 3; D3","$538K -> $55K; net +$219K"),("reg","M1-03","$538,070 FY24, $54,730 FY25; $483K drop"),("ld","slides 1, 7, 19","-$483K; $538K -> $55K; FY24 level ($538K)"),("cd","slides 11, 65","$538K -> $55K; +$219K net"),("apA","slide 5","$538,070 -> $54,730; net $218,588"),
])
add(21, "Months of cash FY25, FY21, FY24", [
 ("op","Verdict","4.4 months"),("es","§2","4.4, down from 7.5 in FY21"),("verdict","Verdict","4.4 (7.5 in FY21)"),("m1","Findings table","FY19 5.8, FY21 7.5, FY22 6.3, FY23 5.0, FY24 5.2, FY25 4.4"),("m3","Findings 3","5.2 FY24, 4.4 FY25"),
 ("ff","M1 table; M3","5.2 / 4.4 / 7.5"),("reg","M1-02; M3-04","4.4 vs 7.5; 5.2 FY2024"),("ld","slides 1, 7, 22","4.4; 7.5 in FY21; 'Calvary holds 4.4 today' with FY2024 peer figures"),("cd","slides 10, 26","FY20 6.3, FY21 7.5 ... FY24 5.2, FY25 4.4; chart 5.23"),
 ("apA","slide 4","FY21 7.5; FY24 5.2; FY25 4.4"),("apB","slide 4","Calvary 5.2 (FY24); 5.5 FY22-24 mean"),("cspine","#9, #23","7.5 to 4.4; 5.2 months FY24"),
])
add(22, "FY24 surplus", [
 ("m1","Findings table","+$507K"),("ff","M1 table","+$507K"),("ld","slide 7","FY24 was +$507K"),("cd","slide 10","FY24 +$507K; chart 506,540"),("apA","slide 4","$506,540"),
])
add(23, "OVSJG Victim Services approved FY24-FY27 ($M) and Mayor's proposed cuts", [
 ("es","§2","$55-56M through FY2027; Mayor -$5.8M (FY26), -$5.6M (FY27)"),("verdict","Evidence","$55.9M FY25, $55.4M FY26, $55.3M FY27; -$5.8M, -$5.6M"),("cb","§2","flat at $55M through FY2027"),("strat","§4","OVSJG $55M pool"),
 ("m2","Findings 4","$45.5M FY24 -> $55.9M -> $55.4M -> $55.3M; Mayor FY26 $50.1M (-10.4%)"),("ff","M2 finding 4","same as m2"),("reg","M2-03","$45.5M, $55.9M, $55.4M, $55.3M; Mayor FY26 $50.1M"),
 ("meth","A4 S1","10.4% ($5.8M of $55.9M)"),("ld","slide 9","flat at $55M; $45.5M -> $55.9M -> $55.4M -> $55.3M; -$5.8M and -$5.6M"),("cd","slides 17, 18","same; actual $41.3M FY24, $47.9M FY25; Council +$3.5M and +$6.0M"),
 ("apA","slides 17-20","approved FY23 $41.8M, FY24 $45.5M, FY25 $55.9M, FY26 $55.4M, FY27 $55.3M; Mayor -$5.84M to $50.1M (FY26), -$5.60M to $49.9M (FY27); -$5,842,000 / -$5,596,000"),
])
add(24, "DHS homeless-services budget figures", [
 ("es","§2","DHS homeless-services and PSH budgets flat to rising"),("m2","Findings 4","continuum $170M (FY24) -> $206M (FY26) -> $194M (FY27); PSH $145-166M"),("ff","M2 finding 4","same"),("reg","M2-03","$170M FY24 -> $206M FY26; PSH ~$145-166M"),
 ("strat","§1","DHS PSH budget $145-166M, 25x the DC CoC pool"),("ld","slide 9","$170M -> $206M -> $194M"),("cd","slide 17","$170M -> $206M -> $194M; PSH $153M -> $145M -> $148M -> $166M"),
 ("apA","slides 17, 18","continuum approved FY23 $178.0M, FY24 $170.0M, FY25 $178.7M, FY26 $205.9M, FY27 $193.7M; PSH $162.6M/$152.9M/$144.8M/$147.6M/$166.2M"),("apC","slide 46","GOV-DC-3 DHS PSH local lines $145-166M"),
])
add(25, "OVSJG under-spend (%)", [
 ("es","§2","9-14% below approved"),("m2","Findings 4","9-14%"),("ff","M2 finding 4","9-14%"),("reg","M2-03 implication","9-14%"),("strat","§5","9-14%"),("ld","slide 9","9-14%"),("apA","slide 17","9-14%; actual $41.3M and $47.9M"),("meth","A4 S2","FY2024 under-spend 9%"),
])
add(26, "Ceilings vs recognized FY24 and FY25 ($ and %)", [
 ("op","Clouds","about two-thirds"),("es","§2","$2.62M of $3.6M; $2.89M of $4.3M"),("rec","§1","67-73%"),("strat","§1","$3.6M / $4.3M vs $2.62M / $2.89M"),("verdict","Evidence","FY24 73%, FY25 67%"),
 ("m2","Findings 2","$3.6M vs $2.62M (73%); $4.3M vs $2.89M (67%)"),("ff","M2 finding 2; D1","same; gap $0.9-1.4M/yr"),("reg","M2-02","73%-67%; $3.60M vs $2.62M; $4.29M vs $2.89M; gap $1-1.4M/yr"),
 ("ld","slides 2, 11, 24","two-thirds; 73% / 67%; ~$1M a year"),("cd","slides 16, 65","$3.60M vs $2.62M (73%); $4.29M vs $2.89M (67%)"),("apA","slide 15","$3,595,278 / $2,621,203 (73%); $4,289,967 / $2,892,598 (67%)"),("meth","A5, D1","$3.6M / $4.3M vs $2.62M / $2.89M; 67-73%"),
])
add(27, "Scenario losses S1-S6 ($, % revenue) and months of cash after a year", [
 ("op","Clouds","OVSJG cut ~$67K; DHS/TCP ~$960K (19%); combined under two months"),("es","§2","$67K; $168K; $178K; $366K; $960K (19%); under two months"),("br","Clouds","$67K; $366K; $960K (a fifth)"),
 ("rec","§1","67K; 168K; 178K; 366K; 960K (19%); combined $1.31M (26%), 1.7 months"),("cb","§2","$67K; $960K; combined $1.31M -> 1.7 months"),
 ("verdict","Scenario table","-67K (1%) 3.1; -168K (3%) 3.0; -178K (4%) 2.9; -366K (7%) 2.7; -960K (19%) 2.1; -1.31M (26%) 1.7; baseline 3.1"),
 ("m2","Scenario table","identical to verdict"),("ff","M2 scenario table","identical"),("reg","M2-05","$0.96M (19%); $1.31M; 1.7 months; OVSJG -10% $0.07M; CoC -15% $0.18M"),
 ("ld","slide 10","identical; deficits -$1,567K / -$1,914K"),("cd","slide 20","identical plus net deficits and months to zero"),("apA","slide 22","$67,311 (1.4%); $168,277 (3.4%); $178,144 (3.6%); $365,762 (7.4%); $959,935 (19.3%); $1,306,356 (26.3%)"),("cspine","#18","$67-168K; $366K; $960K; $1.31M"),
])
add(28, "Months to zero cash, baseline", [
 ("verdict","Verdict","about 41 months"),("m2","Findings 6","about 41 months"),("ff","M2; verdict copy","about 41 months"),("cd","slide 20","41 (baseline); 39/36/36/31/23/20"),("apA","slide 22","41; 39; 36; 36; 31; 23; 20"),("ld","slide 10","burns cash at about $50K a month (no months-to-zero figure)"),
])
add(29, "DMV funders to DC sector: annual, five-year ($M), DAF share", [
 ("es","§3","about $132M a year"),("br","Opportunities","about $132M a year"),("cb","§2","$132M/yr (58% DAF)"),("m4","Findings 1","about $132M/yr; $660M; 58% DAF; 42% ($276M) institutional"),
 ("ff","Summary M4; M4 finding 1","$132M; $660M; 58%; 42% ($260M)","$260M is wrong: 42% of $660M = $277M; m4 says $276M"),("reg","M4-01","$132.10M/yr; $660.49M; 58% DAF; 42% from 555"),("cp3","§2","$660M / $132M a year (not $620M / $124M)"),
 ("ld","slide 16","$132M a year; $660M TY2020-24, 58% via DAFs"),("cd","slide 32","about $132M a year; $660M; 58%"),("apC","slide 2","$660M; 58.2% DAF ($384.2M)"),("lspine","#13","$132M a year"),("cspine","#28","$132M; 58%"),
])
add(30, "Institutional funders in landscape", [
 ("m4","Findings 1","555"),("ff","Summary M4; M4 finding 1","555"),("ff","Consistency notes #7","stale: 'readout says 561'"),("reg","M4-01","555"),("cp3","§2","555"),("cd","slide 32","555 institutional funders"),
])
add(31, "Funders giving to 3+ peers and 2+ peers (not Calvary)", [
 ("es","§3","23 give to three or more"),("br","Opportunities","Twenty-three"),("cb","§2","23"),("m5","Findings 1","23 (3+); 75 (2+)"),("ff","M5","23; 75"),("reg","M5-01","23; 75"),("lspine","#13","23"),("cspine","#33","Twenty-three"),
 ("ld","slide 16","23 (chart shows 14 bars, 3+ peers)"),("cd","slide 37","23 (chart 23 bars); 'Appendix C lists all 75'"),("apC","slide 10","75 of 2+; 23 of 3+"),
])
add(32, "Clark Charitable figures", [
 ("op","Opportunities 3","$7.8M to five peers, median $250K"),("es","§3","$7.8M to five peers, median $250K"),("br","Opportunities","five of those peers $7.8M"),("strat","§2","5 peers, median $250K, $32.8M to DC's sector"),
 ("m4","Findings 2","$32.8M to 20 DC organizations, 5 core peers"),("m5","Findings 1","5 peers, $7.8M, median $250K"),("m7","Tier 1","0.82, typical grant $250K, 5 peers"),("ff","M4; M5; M7","$32.8M/20 orgs/5 peers; $7.8M; $250K"),("reg","M5-01","5 peers, $7.8M"),
 ("plan","row 3","typical $250K; DC-sector $32.8M; 5 peers"),("op_deck","slide 1","$7.8M to five peers, median $250K"),("ld","slide 16","$7.8M to five peers, median $250K"),("cd","slides 33, 48","$32.8M, 20 DC orgs, 5 peers; $250K"),("apC","slides 3, 19, 47","$32.77M; 20 recipients; median $250,000; 5 peers"),
])
add(33, "Lapsed funders count and historic total", [
 ("es","§3","12 former funders have lapsed"),("cb","§2","12 lapsed"),("m5","Findings 2","12; $255K"),("ff","Summary M5; M5 finding 2","12; $255K"),("reg","M5-02","12; $0.26M"),("cd","slide 38","Twelve; $255K"),("apC","slide 16","Twelve; $256K (table sums to $256,150)"),("cspine","#34","Twelve; $255K"),
])
add(34, "Current funders with headroom", [
 ("es","§3","15"),("cb","§2","15"),("m5","Findings 3","15"),("ff","M5","15"),("reg","M5-03","15"),("cd","slide 39","Fifteen"),("apC","slide 17","Fifteen"),("cspine","#35","Fifteen"),
])
add(35, "CRM verifiable share and total; corporate no-filing total", [
 ("cb","§3","44% verifiable"),("strat","§2","$2.6M of the CRM's $10.6M has no public filing"),("m5","Findings 6","$10.56M, 160 funders; $4.63M (44%, 25 funders); $2.55M (92 funders) corporate/no filing"),
 ("ff","M5 finding 6","same as m5"),("reg","M5-04","44% of $10.6M; corporate $2.6M; see-attached $1.3M"),("meth","A3; §2.4","160 funders, $10.56M; 25 confirmed, 92 not exempt filer"),("cd","slide 40","44% of $10.6M; $4.63M/25; $2.55M/92; $1.28M; $1.61M; $0.48M"),("apC","slide 25","44% of $10.56M"),("cspine","#36","44% of $10.6M"),
])
add(36, "Network funder count; shared funders (MK, DASH, HoR DC); not-shared counts", [
 ("es","§3","17 with Miriam's Kitchen; 14 each with DASH and House of Ruth DC"),("m6","Findings 1-2","330 funders; 17/14/14; NEW 12, MSP 12; not shared HoR MD 81, HoR DC 69, MK 48, NSV 45, CoH 33, Doorways 29"),
 ("ff","M6","330; 17/14/14; 81/69/48/45"),("ff","Consistency notes #10","stale: 'readout says 324'"),("reg","M6-01; M6-02","330; 17/14/14"),("cp3","§2","M6 330 funders"),
 ("ld","slide 17","17; 14 each; HoR DC 69, HoR MD 81"),("cd","slides 42, 43","330; 58 fund 3+; 17/14/14/12/12; 81/69/48/45"),("apB","slide 16","17/14/14; 48/9/69 ..."),("apC","slide 27","330 implied; top 25 listed"),
])
add(37, "Board links counts (total, high, medium)", [
 ("br","If asked","one high-confidence overlap, not with a funder"),("es","§3","board overlaps are a thin channel"),("m6","Findings 3","Calvary 8 links: 1 high, 7 medium; across all 19 orgs 27 touch a funder, 3 high"),
 ("ff","M6 finding 3","8; 1 high; 7 medium; 27 touch a funder, 3 high"),("reg","M6-03","8 links; 1 high; 7 medium"),("ld","slide 17","one high-confidence link, not a funder"),("cd","slides 44-45","1 high Calvary + 7 medium (table shows 24 rows, 3 high)"),
 ("apC","slide 29","56 interlocks touching Calvary, peers and comparators: 4 high, 52 medium (CSV: 33 touch a funder, 27 of them non-Calvary, 3 high)"),("cspine","#39","one high; seven medium"),
])
add(38, "Pipeline rows and tier counts", [
 ("es","§5","Eleven Tier 1 targets"),("op","Next","eleven Tier 1 targets"),("br","Plan","Eleven Tier 1"),("rec","§2","182 rows; Tier 1 (11); Tier 2 (40); Tier 3 (131)"),("cb","§2","182 rows; 11 Tier 1"),
 ("m7","Result","182 rows; 11 / 40 / 131"),("pipe","tier column","182 rows; 11 / 40 / 131"),("plan","rows","11 rows"),("reg","M7-01","182: 11 / 40 / 131"),("cp3","§2","Tier 1 = 11; 182 rows; action plan 11 rows"),
 ("ff","Summary M7; M7 finding 1","Tier 1 list of 12 incl. Frontier Co-op (0.60); 'Readout and register differ on counts'","stale"),("ff","Insight register summary M7-01","182 rows: 12 Tier 1, 40 Tier 2, 131 Tier 3","stale; also note #11 says 12/39/131"),
 ("ld","slides 18, 20, 25","eleven named targets; 11-row table; 182 rows"),("cd","slides 46-48, 50","11 Tier 1; 182 candidates"),("apC","slides 47, 61","182 rows: 11 / 40 / 131; 11 Tier 1 targets"),("meth","C3","182 rows"),("lspine","#16","Eleven"),("cspine","#41","Eleven rows reach Tier 1"),
])
add(39, "Expansion pool figures", [
 ("op","Opportunities 5","$30M and $21M a year"),("es","§3","$30M, $21M; health $84M"),("strat","§4","$30M; $21M; $84M (206 funders); $9.7M; $4M"),("m8","Findings table","housing $32.4M; education $93.7M; workforce $30.4M; BH $20.7M; DV $4.5M; health $84.2M (206); aging $9.7M; veterans $7.7M; reentry $1.0M; maternal $4.2M; near total ~$149M"),
 ("ff","M8","same as m8"),("reg","M8-01","$149.22M/yr near; $84.15M/yr health, 206 funders"),("op_deck","slide 1","$30M and $21M"),("ld","slide 21","chart: 30,396,443; 20,685,130; 84,151,297 (education shown in appendix)"),("cd","slides 53, 54","education $94M; workforce $30M; BH $21M; DV $4.5M; health $84M (206); aging $9.7M; veterans $7.7M; reentry $1.0M; maternal $4.2M"),("apC","slide 66","$32.4M/$93.7M/$30.4M/$20.7M/$4.5M/$84.2M/$9.7M/$7.7M/$1.0M/$4.2M"),
])
add(40, "Federal notices count", [
 ("m8","Findings 4","36 relevant notices"),("m7","Result table","12 federal opportunities in Tier 3"),("rec","§2","12 federal notices in Tier 3"),("ff","M8","36"),("reg","M8-02","36"),("cd","slide 55","36 (agency table sums to 36)"),("apC","slide 67","36 notices, 13 agencies"),("cspine","#47","36"),
])
add(41, "Ward poverty rates", [
 ("es","§1","Wards 7 and 8: 23% and 31% vs 15%"),("br","Opening","poverty is double the city rate"),("m9","Findings table","Ward 7 22.9%; Ward 8 30.6%; DC 15.4%; female 24.8/31.7/16.3"),("ff","Summary M9; M9 table","30.6% (DC 15.4%); table same"),("reg","M9-01","Ward 8 31%, Ward 7 23%, DC 15%; female 32%"),
 ("ld","slide 3","Ward 8 31% vs 15%"),("cd","slide 57","31% / 23% / 15%; female 32/25/16"),
])
add(42, "DC PIT counts 2016 and 2025", [
 ("m9","Findings 2","8,350 (2016) -> 5,138 (2025)"),("ff","M9","8,350 -> 5,138"),("reg","M9-02","8,350 -> 5,138"),("cd","slide 58","8,350 (2016); 5,138 (2025)"),("cspine","#49","8,350 -> 5,138"),
])
add(43, "Calvary institutional funder count; institutional grants % revenue; peers' %", [
 ("es","§3","42 institutional funders; 12% vs 6-8% at N Street Village and House of Ruth DC"),("m3","Findings table/4","42; 12%; NSV 6%, HoR DC 8%, MK 11%, Samaritan Inns 27%"),("ff","M3","42; 12%; 6-8%; 27%"),("reg","M3-05","42; 12% vs 8% HoR DC, 6% NSV, 11% MK; Samaritan 27%"),
 ("ld","slide 14","42 funders; 12%; 6-8%; 27%; chart 12.4%"),("cd","slide 28","12% with 42 funders; Samaritan 27% with 14"),("apB","slide 6","42 institutional; 12.4%"),("cspine","#25","12%"),
])
add(44, "DWC revenue 2014 and 2024; government share 24%->57%; months of cash; growth multiple", [
 ("es","§3","scaled more than five-fold with government rising to 57%"),("m10","Table; Trajectory","$6.3M (FY2014) -> $34.4M (FY2024); 24% -> 57%; months of cash 2.1/3.1/3.1/2.4; revenue x5.5"),("m3","Findings table/5","DWC 57%; 2.4 months"),
 ("ff","M10","$6.3M -> $34.4M; 24% -> 57%; x5.5; 2-3 months of cash"),("reg","M10-01","$6.31M -> $34.40M; 24% -> 57%; magnitude '6x scale, 57% government'; implication 2-3 months"),("cp3","§2","DWC x5.5"),
 ("ld","slides 13, 23","Scaled 3x since 2018 with government rising to 57%, 2-3 months of cash; $6M (2014) -> $34M (2024), 24% -> 57%, 2.4 months"),("cd","slides 60, 61","$6.3M, 24% -> $34.4M, 57%; 2.4 months"),
 ("apB","slides 17, 18","$6.3M -> $34.4M; 24% -> 57%; 5.5 times; months of cash 1.8-4.4 (2.4 in FY2024)"),("cspine","#50","$6M to $34M; 57%"),("meth","§3.3","FY2024 revenue $34,403,997"),
])
add(45, "CBWC/SheWorks revenue and shares", [
 ("m10","Table","FY2023 $1.38M 88%; FY2024 $1.49M 85%; FY2025 $1.84M 70%; months of cash 28.5/4.8/8.2"),("m3","Findings table","$1.5M (FY24); 86% (FY22-24 mean); 4.8 months"),("ff","M10; M3","same"),("reg","M10-02","70% at $1.84M, down from 88%; private $169K -> $558K"),
 ("cd","slide 61","$1.84M (FY2025); 70% (88% in FY2023); 8.2 months"),("apB","slides 4-5, 21","$1.5M; 86%; latest 85%; 4.8; table $1,377,300/$1,486,733/$1,840,152; 88/85/70%"),("meth","§3.3","~$1.8M"),("cspine","#51","88% government"),
])
add(46, "Reserve target ($M) and private revenue target ($M->$M)", [
 ("op","Recommendations","about $2.8M; about $3M within three years"),("es","§4","about $2.8M; $2.1M (FY25) to $3.0M"),("br","Plan","about $2.8M"),("rec","§4","about $2.8M; $2.1M -> $3.0M; 58% -> ~50%"),("strat","Goal; §3","$2.8M at FY25 expenses; $2.1M -> $3.0M; 58% -> roughly 50%"),
 ("op_deck","slide 1","~$2.8M; ~$3M"),("ld","slides 2, 22, 25","~$2.1M to ~$3M; about $2.8M; $3M / 50% target"),("cd","slide 64","~$2.8M; ~$2.1M -> ~$3.0M"),
])
add(47, "Deck slide counts as stated", [
 ("op","What comes next","leadership deck (21 slides), consulting deck (55), four appendix decks"),("op_deck","slide 1","leadership deck (22 content slides), consulting deck (55 content slides)"),("cb","§1","leadership spine (22 slides); consulting spine (55)"),
 ("readme","Deliverables","leadership 22 content slides plus five section dividers; consulting 55 content slides plus dividers and continuations"),("cp3","§1","leadership 22 content + 5 dividers (26 total); consulting 55 + dividers/continuations (66 total); appendices A 22, B 21, C 69, D 33 (145)"),
 ("lspine","list","22 numbered headlines incl. title and closing; 5 dividers named"),("ld","export; slide 26","26 slides in export = 22 spine slides + 4 dividers (no divider before slide 3); slide 26 says 'Consulting deck: 55 slides'"),
 ("cd","export; slide 66","66 slides; slide 66 says 'Appendix A (17 slides), B (12), C (21), D (24, method notes A1-D3)'"),("apA","export","22 slides"),("apB","export","21 slides"),("apC","export","69 slides"),("apD","export","33 slides"),
 ("aspine","items","m3_00 'two slides' (export 4); m4_00 top 50 'two slides' (4); m5_01 'three slides' (6); m7_00 'six slides' (14)"),
])
add(48, "Tier 1 list of names", [
 ("pipe","tier=1","Abell; GWCF; Clark Charitable; OVSJG; Cafritz; HUD CoC via TCP; DHS via TCP; Fowler; MGAC; Schattner; America's Charities"),("plan","11 rows","same 11"),("m7","Tier 1","same 11 (Frontier Co-op -> Tier 2)"),("rec","§2 table","same 11"),("reg","M7-01","7 institutional: Abell, GWCF, Clark, Cafritz, Fowler, Schattner, America's Charities (+ gov/corporate)"),
 ("ff","M7 finding 1","same 11 plus Frontier Co-op (0.60) = 12","stale"),("ff","Insight register summary M7-01 (stale note #11)","names United Way NCA, Bank of America, Venable, Cohen, Bernstein, Washington Home among Tier 1 institutional targets"),
 ("ld","slide 20","same 11"),("cd","slides 48, 50","same 11"),("apC","slides 47, 61","same 11"),("op","Opportunities 2-3","upgrade GWCF, Cafritz, Abell, Fowler, United Way NCA, Bank of America; open Clark, Schattner, Cohen, Bernstein, Washington Home (mixes Tier 1 and Tier 2 names, not labelled as Tier 1)"),
])
add(49, "Number of OVSJG / CoC projects named", [
 ("m2","Findings 1, 3","CoC three projects; seven streams"),("ld","slide 5","CoC three projects; OVSJG two transitional-housing grants"),("cd","slide 15","Seven streams: 2 DHS, 3 CoC, 2 OVSJG"),("apA","slides 10, 11, 16","OVSJG Reach Up TH + New Foundations TH; CoC Sister Circle PSH, Reach Up, New Foundations 2; seven streams"),
 ("pipe","rows 4, 6, 7","OVSJG (Reach Up, New Foundations); CoC (Sister Circle, Reach Up, New Foundations 2); DHS (TH contract, Sisters Rise)"),("es","§4","defend the three CoC renewals"),("cspine","#13","Seven streams"),
])
add(50, "Landscape concentration claims: 'six of the 25 largest'; 'top 10 = 55%'", [
 ("m4","Findings 2","top 10 give about half; 6 of the 25 largest fund Calvary"),("ff","Summary M4; M4 finding 2","about half; 6 of the 25 largest"),("ff","Consistency notes #8","register 55% vs readout 'about half'"),("reg","M4-02","top 10 = 55%; 6 of top 25"),("cp3","§2","top 10 = 55%"),
 ("cd","slide 33","headline 55%; body 'Top 10 = about half'; six of the 25 largest"),("cspine","#29","Ten funders supply 55%; six of the 25 largest"),("apC","slide 3","top 50 include 8 that fund Calvary (top-25 rows show 6 with a Calvary amount); m4_04 cum share at rank 10 = 55.2%"),
])

with open(os.path.join(OUT, "consistency_matrix.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["metric_id","metric","document","location","value_as_written","note"]); w.writerows(M)

DIS = [
 # metric_id, metric, documents_involved, values, severity, note
 (1, "Real revenue growth FY19->FY25", "reports/executive_one_pager.md; reports/executive_summary.md; decks_md/leadership_deck.md slide 3; decks_md/appendix_A slide 4", "59% real; one-pager/summary pair it with nominal $2.49M -> $4.97M (nominal growth = 100%); leadership slide 3 labels $2.49M -> $4.97M as '2024 dollars'", "substantive", "Leadership slide 3 mislabels nominal revenue as 2024 dollars; real values are $3.05M -> $4.84M (+59%). One-pager and executive summary pair the real growth rate with nominal endpoints without saying so."),
 (2, "Revenue FY19 and FY25 basis label", "decks_md/leadership_deck.md slide 3; decks_md/appendix_A slide 4; modules/m1", "'$2.49M -> $4.97M, 2024 dollars' vs appendix A real $3,051,134 -> $4,840,626", "substantive", "Same issue as metric 1: basis label wrong on the leadership slide."),
 (4, "Share of DC TH beds", "reports/board_readout.md; insight_register.csv M9-02; others", "'almost 7%' / '7%' vs 6.8%", "rounding", ""),
 (5, "Recurring award base year label", "reports/executive_one_pager.md; reports/executive_summary.md; reports/board_readout.md; decks one-pager slide 1 vs modules/m2, insight_register", "'about $4.1M a year' (no year) vs '$4.1M (2024)'; executive summary lists OVSJG FY26 $1.05M + CoC FY2025 $1.77M + DHS FY2024 $1.42M (= $4.24M) next to 'TCP carries 74% of the base'", "wording", "Mixed award years in the executive summary; full_findings note #13 already flags that decks should not mix them."),
 (9, "Government share by year / range basis", "reports/full_findings.md M1 table vs its own text, modules/m1 table, decks_md/appendix_A slide 3, checkpoints/cp3_memo", "full_findings table FY19 51%, FY21 51%, FY22 64%, FY23 55% (audit gov ÷ 990 revenue) vs m1/appendix A audit basis 49%, 50%, 61%, 51%; text in all docs says 40-61%", "substantive", "full_findings M1 table still carries the mixed-denominator shares the CP3 consistency pass removed (range would be 44-64%). Consistency note #1 in full_findings is also stale (claims the readout gives 51/64/55)."),
 (10, "Peer rank and DV range", "reports/full_findings.md insight-register summary and consistency note #5 vs insight_register.csv M3-01, modules/m3", "full_findings copy of M3-01: DV providers 75-94% and Samaritan Inns philanthropy-led; register now 70-89% and Samaritan Inns mixed", "substantive", "Stale register text reproduced in full_findings; rank 11th of 19 is consistent everywhere."),
 (12, "Share of award base through TCP", "all documents quoting '74% of a $4.1M award base' (exec one-pager, executive summary, recommendations, consulting briefing, verdict, strategic recs, one-pager deck slide 1, leadership slides 2 and 5, consulting slide 63) vs decks_md/appendix_A slide 22 and modules/m2 method", "74% = CoC 41% + DHS 33% of FY25-aligned ceilings ($4.29M); on the 2024 award base ($4.10M: 0.91 + 1.76 + 1.42) TCP = 78%", "substantive", "Percentage and dollar base come from different years; either quote 74% of the $4.3M FY25 ceilings or 78% of the $4.1M 2024 base."),
 (13, "OVSJG award quoted", "recommendations/funding_pressure_verdict.md evidence ($0.91M, 2024) vs executive summary, m2, decks ($1.05M, FY26)", "$0.91M (2024) vs $1.05M (FY26)", "wording", "Different award years, both labelled; not a contradiction but the two are mixed across documents."),
 (14, "HUD CoC award and year label", "recommendations/funding_pressure_verdict.md ($1.76M, 2024) vs others ($1.77M, 'FY2025')", "$1.76M (2024 competition) vs $1.77M (2025 competition, labelled FY2025, = Calvary FY26 per lag rule)", "rounding", "Different competition years; the 'FY2025' label is HUD's competition year, which the method note maps to Calvary FY26."),
 (17, "GWCF share", "decks_md/appendix_A slide 6 (27.2%) vs all others (27%)", "27.2% vs 27%", "rounding", ""),
 (18, "DAF receipts", "modules/m1, consulting slide 12, appendix B ($1.09M) vs executive summary, m4, strategic recs, leadership deck ($1.1M)", "$1.09M vs $1.1M", "rounding", ""),
 (21, "Months of cash basis on reserve slide", "decks_md/leadership_deck.md slide 22", "'Calvary holds 4.4 today' (FY25) beside peer figures footnoted FY2024 (Calvary FY24 = 5.2)", "wording", "Mixed years on one slide; footnote says FY2024."),
 (23, "OVSJG pool shorthand", "reports/consulting_briefing.md, decks_md/leadership_deck.md slide 9, strategic recs ('$55M', 'flat at $55M') vs executive summary ('$55-56M') vs m2/appendix A ($55.9M/$55.4M/$55.3M; $45.5M FY24)", "'flat at $55M' vs $45.5M -> $55.9M -> $55.4M -> $55.3M", "wording", "'Flat' describes FY25-FY27 only; FY24 was $45.5M."),
 (23, "Mayor's cut precision", "decks_md/appendix_A slides 19-20 (-$5.84M / -$5,842,000; -$5.60M / -$5,596,000) vs others (-$5.8M / -$5.6M)", "-$5.84M vs -$5.8M; -$5.60M vs -$5.6M", "rounding", ""),
 (26, "D1 gap size", "insight_register.csv M2-02 ('$1-1.4M/yr') vs full_findings D1, discoveries log copy, appendix D slide 31 ('$0.9-1.4M/yr') vs leadership slide 24 ('~$1M a year')", "$1-1.4M vs $0.9-1.4M vs ~$1M", "rounding", "FY24 gap = $0.97M."),
 (27, "Scenario % of revenue", "decks_md/appendix_A slide 22 (1.4%, 3.4%, 3.6%, 7.4%, 19.3%, 26.3%) vs verdict/m2/decks (1%, 3%, 4%, 7%, 19%, 26%)", "3.6% shown as 4%; otherwise rounding", "rounding", ""),
 (29, "Institutional dollars to DC sector", "reports/full_findings.md M4 finding 1 ($260M) vs modules/m4 ($276M) and chart_data m4_01 (sum $276.3M)", "$260M vs $276M", "substantive", "full_findings figure does not equal 42% of $660M."),
 (30, "Institutional funder count", "reports/full_findings.md consistency note #7 ('readout says 561') vs full_findings body, m4, register, cp3 (555)", "561 (stale note) vs 555", "wording", "Stale consistency note; body figures agree."),
 (31, "Funders of 3+ peers shown", "decks_md/leadership_deck.md slide 16 chart (14 bars) vs headline/text (23)", "14 plotted vs 23 claimed", "wording", "Chart is truncated to the top 14; the number in the headline matches m5_01."),
 (33, "Lapsed funders historic total", "modules/m5, full_findings, consulting slide 38, consulting spine ($255K) vs appendix C slide 16 ($256K; table sums to $256,150) vs register ($0.26M)", "$255K vs $256K vs $0.26M", "rounding", "$256,150 rounds to $256K; $255K is a rounding slip."),
 (36, "Network funder count", "reports/full_findings.md consistency note #10 ('readout says 324') vs m6, register, cp3, consulting slide 42 (330)", "324 (stale note) vs 330", "wording", "Stale note only."),
 (37, "Board interlock totals", "modules/m6 and full_findings ('across all 19 organizations, 27 interlocks touch a funder, 3 at high confidence') vs decks_md/appendix_C slide 29 ('56 interlocks ... 4 high, 52 medium') vs chart_data m6_04 (56 rows; 33 touch a funder; 27 of those are non-Calvary; 3 high among funder rows; 4 high overall)", "27 funder-touching (non-Calvary) / 3 high vs 56 total / 4 high", "wording", "Both reproducible from m6_04 but on different filters; the readout's '27' excludes Calvary's own 6 funder-touching rows and the sentence says 'across all 19 organizations'. Consulting slides 44-45 show 24 of the 56 rows without saying the table is truncated."),
 (38, "Pipeline tier counts", "reports/full_findings.md (M7 summary, M7 finding 1, insight-register summary, consistency note #11) vs recommendations/funder_pipeline.csv, modules/m7, insight_register.csv, recommendations.md, cp3 memo, all decks", "full_findings: Tier 1 list of 12 incl. Frontier Co-op (0.60); register summary '12 Tier 1, 40 Tier 2'; note #11 '12 / 39 / 131' vs 11 / 40 / 131 everywhere else", "substantive", "full_findings was not updated after the CP3 reclassification (Frontier Co-op -> Tier 2, T. Rowe Price -> DAF channel)."),
 (40, "Federal notices vs pipeline federal rows", "modules/m7 and recommendations.md ('12 federal notices', Tier 3) vs m8, register, decks ('36 relevant notices')", "12 vs 36", "wording", "Different scopes (pipeline rows vs expansion scan); neither document says 12 is a subset of 36."),
 (41, "Ward poverty rounding", "insight_register M9-01, executive summary, consulting slide 57 (31% / 23% / 15%) vs m9 table (30.6% / 22.9% / 15.4%)", "rounded vs one-decimal", "rounding", ""),
 (43, "Institutional grants ÷ revenue", "decks_md/appendix_B slide 6 and leadership slide 14 chart (12.4%) vs text (12%)", "12.4% vs 12%", "rounding", ""),
 (44, "DWC growth multiple", "insight_register.csv M10-01 magnitude ('6x scale') vs m10, full_findings, appendix B, cp3 ('x5.5' / '5.5 times') vs executive summary ('more than five-fold') vs leadership slide 13 ('Scaled 3x since 2018')", "6x vs 5.5x vs 3x (2018 base)", "rounding", "34.4/6.31 = 5.45x; '6x' over-rounds. '3x since 2018' is a different base year (11.6 -> 34.4 = 2.97x) and is correct on that base."),
 (44, "DWC months of cash range", "modules/m10, full_findings, leadership slide 13 ('2-3 months') vs appendix B slides 17-18 ('1.8-4.4 throughout'; table 2.1-4.4 FY2014-24)", "2-3 vs 1.8-4.4", "wording", "FY2020 (4.4) and FY2023 (1.8) fall outside '2-3'."),
 (44, "DWC donor-list count", "decks_md/consulting_deck.md slide 61 ('280 names on the 2023 list') vs modules/m10 ('2023 donor list 202 organizations, 2025 list 148') vs appendix B slide 20 ('donor lists carry 280 names'; annual-report rows 350, funders 280)", "280 on the 2023 list vs 202 (2023) + 148 (2025) = 280 distinct across both lists", "wording", "Consulting slide 61 attributes the combined count to the 2023 list."),
 (45, "CBWC 'latest' government share", "decks_md/appendix_B slide 5 ('Gov. share latest 85%') vs appendix B slide 21, consulting slide 61, m10, register (FY2025 70%)", "85% (FY2024) labelled 'latest' vs 70% (FY2025)", "wording", "Benchmark 'latest' column is FY2024 for every organization; the label reads as the most recent filing."),
 (47, "Leadership deck slide count", "reports/executive_one_pager.md ('21 slides') vs decks one-pager slide 1, consulting briefing ('22 content slides' / '22 slides') vs README and cp3 ('22 content slides plus five section dividers', '26 total') vs leadership export (26 slides = 22 spine slides incl. title and closing + 4 dividers; the 'Where Calvary stands' divider named in the spine is absent)", "21 vs 22 vs 22+5=27 vs 26 actual", "substantive", "22 + 5 dividers cannot total 26; the built deck has 4 dividers. '21 slides' in the one-pager report counts content excluding the title."),
 (47, "Appendix deck slide counts", "decks_md/consulting_deck.md slide 66 ('Appendix A 17 slides, B 12, C 21, D 24') vs checkpoints/cp3_memo and exports (A 22, B 21, C 69, D 33)", "17/12/21/24 vs 22/21/69/33", "substantive", "Consulting closing slide understates every appendix; the numbers match neither total slides nor unique headlines (A 19, B 16 unique)."),
 (47, "Appendix C/B slide counts in spine", "storylines/appendix_headline_spine.md ('m3_00 two slides', 'm4_00 top 50 two slides', 'm5_01 three slides', 'm7_00 six slides') vs exports (4, 4, 6, 14)", "planned vs built counts", "wording", "Spine was written before the table pagination; not user-facing."),
 (47, "Consulting deck slide count on leadership closing slide", "decks_md/leadership_deck.md slide 26 ('Consulting deck: 55 slides') vs cp3/README (55 content + dividers and continuations = 66 total)", "55 vs 66 total", "wording", "'55' is the content-slide count; the slide does not say so."),
 (47, "Benchmark table organization count", "modules/m3, reports/full_findings.md, storylines/appendix_headline_spine.md ('20 organizations', '20 small multiples') vs decks_md/appendix_B slides 4-5, 9-10 ('all 21 organizations') vs chart_data m3_00 (21 rows: Calvary + 18 peers + 2 comparators)", "20 vs 21", "substantive", "Calvary + 18 + 2 = 21; the '20' in the module and report is wrong (or excludes Calvary without saying so)."),
 (48, "Tier 1 list", "reports/full_findings.md (12 names incl. Frontier Co-op; register summary naming United Way NCA, Bank of America, Venable, Cohen, Bernstein, Washington Home) vs pipeline CSV, action plan, m7, recommendations, all decks (11 names)", "12 vs 11; stale names", "substantive", "Same root cause as metric 38."),
 (48, "Tier 1 scores", "modules/m7 and recommendations.md (MGAC 0.70; Fowler typical $33K) vs consulting slide 48, appendix C slide 47, pipeline CSV (MGAC 0.69 / 0.695; Fowler $33K in column, $32K in 'why'; CSV 32,500)", "0.70 vs 0.69; $33K vs $32K", "rounding", ""),
 (50, "Top-10 concentration wording", "modules/m4, full_findings, consulting slide 33 body ('about half') vs register M4-02, cp3, consulting slide 33 headline, consulting spine ('55%'); m4_04 cumulative share at rank 10 = 55.2%", "about half vs 55%", "wording", ""),
 (50, "Majors funding Calvary", "decks_md/appendix_C slide 3 ('top 50 include 8 that already fund Calvary') vs m4/register/consulting ('6 of the 25 largest')", "8 of 50 vs 6 of 25", "wording", "Different bases; the top-25 rows of the appendix table show 6 with a Calvary amount, so both hold."),
]
DIS.sort(key=lambda r: r[0])
with open(os.path.join(OUT, "disagreements.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["metric_id","metric","documents_involved","values","severity","note"]); w.writerows(DIS)
print(len(M), "matrix rows;", len(DIS), "disagreements;", sum(1 for d in DIS if d[4]=="substantive"), "substantive")
