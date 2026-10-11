"""M6: Network analysis. Funder-grantee network around Calvary and its peers (filed grants TY2020-24),
central funders, co-funding overlap between Calvary and each peer, board interlocks (high-confidence
for leadership materials; medium labeled unconfirmed for consulting), and relationship-path scores
for candidate funders (feeds M7)."""
import sys
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import style  # noqa: E402
from lib.common import ANALYSIS, CALVARY, FUNDER_SHORT, NAMED, core_peers, load, log, peer_set, register_insight, save_chart_data, universe  # noqa: E402

S = "06_m6_network"
ps = peer_set(); short = ps.set_index("ein")["short"]
peers = core_peers(); peer_eins = set(peers.ein); subjects = [CALVARY] + sorted(peer_eins)
GR = ["funder_id", "recipient_ein", "tax_year", "amount", "cumulative_flag", "source_type", "source_id"]
gr = load("fact_grants", usecols=GR)
excl = pd.read_csv(ANALYSIS / "config" / "landscape_exclusions.csv", dtype=str)
gr = gr[(gr.cumulative_flag != 1) & gr.source_type.isin(["pf_grants_paid", "schedule_i"]) & gr.tax_year.between(2020, 2024) & gr.recipient_ein.isin(subjects) & ~gr.funder_id.isin(set(excl.funder_id))]
df = load("dim_funder", usecols=["funder_id", "funder_name", "funder_type"]).set_index("funder_id")
gr["funder_type"] = gr.funder_id.map(df.funder_type).fillna("other")
src = sorted(gr.source_id.unique())
edges = gr.groupby(["funder_id", "recipient_ein"]).agg(amount=("amount", "sum"), grants=("amount", "size"), years=("tax_year", "nunique")).reset_index()
edges["funder_type"] = edges.funder_id.map(df.funder_type).fillna("other")
edges["is_daf"] = edges.funder_type == "daf_sponsor"

# ------------------------------------------------------------------ bipartite graph and centrality
G = nx.Graph()
for e in subjects:
    G.add_node(e, kind="recipient", label=short.get(e, e))
for _, r in edges.iterrows():
    G.add_node(r.funder_id, kind="funder", ftype=r.funder_type, label=df.funder_name.get(r.funder_id, r.funder_id))
    G.add_edge(r.funder_id, r.recipient_ein, weight=float(r.amount), grants=int(r.grants))
deg = dict(G.degree()); wdeg = dict(G.degree(weight="weight")); btw = nx.betweenness_centrality(G, weight=None, seed=7)
fun = edges.groupby("funder_id").agg(recipients=("recipient_ein", "nunique"), amount=("amount", "sum"), grants=("grants", "sum")).reset_index()
fun["funder_name"] = fun.funder_id.map(df.funder_name); fun["funder_type"] = fun.funder_id.map(df.funder_type).fillna("other")
fun["betweenness"] = fun.funder_id.map(btw); fun["funds_calvary"] = fun.funder_id.isin(set(edges[edges.recipient_ein == CALVARY].funder_id))
fun = fun.sort_values(["recipients", "amount"], ascending=False).reset_index(drop=True)
save_chart_data(fun, "m6_01_central_funders", "Funders ranked by how many of the 19 organizations (Calvary + 18 peers) they fund, with betweenness centrality", ["fact_grants", "dim_funder"], src, S,
                "bipartite graph funders x recipients, filed grants TY2020-24; betweenness on the unweighted graph")

# ------------------------------------------------------------------ m6_02 co-funding overlap: Calvary vs each peer
fsets = {e: set(edges[edges.recipient_ein == e].funder_id) for e in subjects}
inst_sets = {e: set(edges[(edges.recipient_ein == e) & ~edges.is_daf].funder_id) for e in subjects}
rows = []
for e in subjects:
    if e == CALVARY:
        continue
    a, b = fsets[CALVARY], fsets[e]; ai, bi = inst_sets[CALVARY], inst_sets[e]
    rows.append({"ein": e, "org": short[e], "shared_funders": len(a & b), "shared_institutional_funders": len(ai & bi), "peer_funders": len(b), "peer_institutional_funders": len(bi),
                 "jaccard_all": len(a & b) / len(a | b) if a | b else 0, "jaccard_institutional": len(ai & bi) / len(ai | bi) if ai | bi else 0,
                 "share_of_calvary_funders_also_funding_peer": len(a & b) / len(a) if a else 0,
                 "peer_institutional_funders_not_calvary": len(bi - ai)})
ov = pd.DataFrame(rows).sort_values("shared_institutional_funders", ascending=False)
save_chart_data(ov, "m6_02_cofunding_overlap", "Funder overlap between Calvary and each core peer (filed grants TY2020-24)", ["fact_grants", "dim_funder"], src, S)
d = ov.iloc[::-1]
f, ax = style.fig(10, 6.8)
y = np.arange(len(d)); h = 0.38
ax.barh(y + h / 2, d.shared_institutional_funders, h, color=style.SERIES["institutional"], label="Institutional funders shared with Calvary")
ax.barh(y - h / 2, d.peer_institutional_funders_not_calvary, h, color=style.PEER_COLOR, label="Peer's institutional funders that do not fund Calvary")
for yi, (a_, b_) in enumerate(zip(d.shared_institutional_funders, d.peer_institutional_funders_not_calvary)):
    ax.annotate(f"{int(a_)}", (a_, yi + h / 2), xytext=(3, 0), textcoords="offset points", va="center", fontsize=8, color=style.TEXT_2)
    ax.annotate(f"{int(b_)}", (b_, yi - h / 2), xytext=(3, 0), textcoords="offset points", va="center", fontsize=8, color=style.TEXT_2)
ax.set_yticks(y, d.org); ax.grid(axis="y", visible=False); ax.grid(axis="x", visible=True); ax.legend(loc="lower right"); ax.set_xlabel("Number of institutional funders (TY2020-24 filings)")
style.finish(f, ax, "m6_02_cofunding_overlap",
             f"Calvary shares the most institutional funders with {ov.iloc[0].org} ({int(ov.iloc[0].shared_institutional_funders)}) and {ov.iloc[1].org} ({int(ov.iloc[1].shared_institutional_funders)}); House of Ruth DC and House of Ruth MD have the longest lists of funders Calvary lacks",
             "fact_grants (990-PF and Schedule I rows naming Calvary and the 18 provisional core peers, TY2020-24); dim_funder",
             note="DAF sponsors excluded from the institutional counts. Core peers provisional.")

# ------------------------------------------------------------------ m6_03 network diagram (PNG)
# Drawn at the slides' full-width chart size (12.13 x 3.3 in, lib/deck.js wideImage) so font sizes are true points on the slide.
# Concentric layout, in inches: Calvary at the centre; hub funders (fund HUB+ of the 19 organizations) on an inner
# ellipse; peers on the middle ellipse, ordered by their angle around Calvary in a seed-11 spring layout; every other
# funder at the angle of the peers it funds, Calvary's funders inside the peer ring and the rest outside it.
HUB, RX, RY = 9, 6.6, 1.75
keep = set(fun[(fun.recipients >= 3)].funder_id) | set(subjects)
H = nx.Graph()  # built in sorted order: a subgraph view iterates a set, which moved the layout between runs
H.add_nodes_from((n, G.nodes[n]) for n in sorted(keep))
H.add_edges_from(sorted((u, v, d_) for u, v, d_ in G.edges(data=True) if u in keep and v in keep))
fn = [n for n in H.nodes if H.nodes[n]["kind"] == "funder"]
rn = [n for n in H.nodes if H.nodes[n]["kind"] == "recipient"]
sp = nx.spring_layout(H, k=0.42, iterations=200, seed=11, weight=None)
ell = lambda th, r: np.array([r * RX * np.cos(th), r * RY * np.sin(th)])
pr = sorted([n for n in rn if n != CALVARY], key=lambda n: np.arctan2(sp[n][1] - sp[CALVARY][1], sp[n][0] - sp[CALVARY][0]))
th_peer = {n: 2 * np.pi * (i + 0.5) / len(pr) for i, n in enumerate(pr)}
pos = {CALVARY: np.array([0.0, 0.0])} | {n: ell(th_peer[n], 0.78) for n in pr}
def bary_angle(n):
    v = sum(np.array([np.cos(th_peer[m]), np.sin(th_peer[m])]) for m in H.neighbors(n) if m in th_peer)
    return float(np.arctan2(v[1], v[0]))
def ring(group, r, jitter, offset):
    # Half the barycentre angle, half even spacing, so funders sit near their peers without stacking.
    group = sorted(group, key=lambda n: (bary_angle(n), n))
    for i, n in enumerate(group):
        pos[n] = ell(0.35 * bary_angle(n) + 0.65 * (2 * np.pi * i / len(group) + offset), r + jitter * ((i % 3) - 1))
ring([n for n in fn if deg[n] >= HUB], 0.40, 0.0, 0.2)
ring([n for n in fn if deg[n] < HUB and n in fsets[CALVARY]], 0.57, 0.05, 0.05)
ring([n for n in fn if deg[n] < HUB and n not in fsets[CALVARY]], 0.97, 0.04, 0.1)
P = np.array([pos[n] for n in H.nodes])
f = plt.figure(figsize=(12.13, 3.3)); style.apply()
ax = f.add_axes([0.0, 0.05, 1.0, 0.88]); ax.set_axis_off()
for u, v, d_ in H.edges(data=True):
    cal = CALVARY in (u, v)
    ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], color=style.CALVARY_COLOR if cal else style.GRID,
            lw=(0.5 + min(d_["weight"], 1e6) / 4e5) * (0.8 if cal else 0.6), alpha=0.75 if cal else 0.6, zorder=1.5 if cal else 1)
fc = [style.SERIES["daf"] if H.nodes[n].get("ftype") == "daf_sponsor" else (style.SERIES["institutional"] if n in fsets[CALVARY] else style.PEER_COLOR) for n in fn]
ax.scatter([pos[n][0] for n in fn], [pos[n][1] for n in fn], s=[14 + 5 * deg[n] for n in fn], c=fc, edgecolors="white", linewidths=0.6, zorder=2)
ax.scatter([pos[n][0] for n in rn], [pos[n][1] for n in rn], s=[230 if n == CALVARY else 110 for n in rn], c=[style.CALVARY_COLOR if n == CALVARY else style.INK for n in rn], edgecolors="white", linewidths=1.2, zorder=3)
ax.set_xlim(P[:, 0].min() - 0.03 * np.ptp(P[:, 0]), P[:, 0].max() + 0.03 * np.ptp(P[:, 0]))
ax.set_ylim(P[:, 1].min() - 0.06 * np.ptp(P[:, 1]), P[:, 1].max() + 0.06 * np.ptp(P[:, 1]))
from matplotlib.lines import Line2D  # noqa: E402
leg = f.legend(handles=[Line2D([], [], marker="o", lw=0, color=style.CALVARY_COLOR, ms=7, label="Calvary"), Line2D([], [], marker="o", lw=0, color=style.INK, ms=6, label="Core peer (provisional)"),
                        Line2D([], [], marker="o", lw=0, color=style.SERIES["institutional"], ms=5, label="Institutional funder that funds Calvary"), Line2D([], [], marker="o", lw=0, color=style.PEER_COLOR, ms=5, label="Institutional funder that does not"),
                        Line2D([], [], marker="o", lw=0, color=style.SERIES["daf"], ms=5, label="DAF sponsor")], loc="lower left", bbox_to_anchor=(0.0, 0.04), fontsize=7.5, frameon=False, handletextpad=0.2, labelspacing=0.3, borderpad=0)
f.text(0.0, 0.995, "Calvary sits inside the same funder web as its peers: the grey nodes are funders one step away, already giving to organizations Calvary shares funders with", fontsize=9, fontweight="bold", color=style.INK, va="top")
f.text(0.0, 0.0, f"Source: fact_grants (990-PF and Schedule I, TY2020-24) naming Calvary and 18 provisional core peers; dim_funder. Funders shown fund 3+ of the 19 organizations ({len(fn)} funders). Edge width = dollars. Data as of 2026-10-10. Chart m6_03_network.", fontsize=6.5, color=style.TEXT_MUTED, va="bottom")
# Labels: Calvary, all peers, the hub funders. Greedy placement: the first offset that clears nodes, earlier labels and the legend.
f.canvas.draw(); R = f.canvas.get_renderer()
lb = leg.get_window_extent(R)
taken = [(lb.x0, lb.y0, lb.x1, lb.y1)] + [(x - r, y - r, x + r, y + r) for (x, y), n in zip(ax.transData.transform(P), H.nodes) for r in [9 if n == CALVARY else (6 if n in rn else 3)]]
clear = lambda b: all(b[2] < t[0] or b[0] > t[2] or b[3] < t[1] or b[1] > t[3] for t in taken)
DIRS = [(0, 1, "center", "bottom"), (0, -1, "center", "top"), (1, 0, "left", "center"), (-1, 0, "right", "center"),
        (0.75, 0.75, "left", "bottom"), (-0.75, 0.75, "right", "bottom"), (0.75, -0.75, "left", "top"), (-0.75, -0.75, "right", "top")]
labels = [(CALVARY, "Calvary", 10, "bold", style.CALVARY_COLOR)] + [(n, short[n], 8.5, "bold", style.INK) for n in pr] \
    + [(n, FUNDER_SHORT[n], 7.5, "normal", style.TEXT_2) for n in sorted(FUNDER_SHORT, key=lambda n: (-deg[n], n)) if n in pos]
unplaced = []
for n, txt, fs, fw, col in labels:
    # Peers prefer the outer side of their ring (above in the top half, below in the bottom half).
    up = pos[n][1] >= 0
    dirs = sorted(DIRS, key=lambda d: 0 if (n in th_peer and d[1] == (1 if up else -1)) else 1) if n in th_peer else DIRS
    for rr in (8, 15, 24, 34, 46, 58):
        for dx, dy, ha, va in dirs:
            t = ax.annotate(txt, pos[n], xytext=(dx * rr, dy * rr), textcoords="offset points", ha=ha, va=va, fontsize=fs, fontweight=fw, color=col, zorder=5,
                            bbox=dict(boxstyle="square,pad=0.05", fc="white", ec="none", alpha=0.8),
                            arrowprops=dict(arrowstyle="-", color=style.TEXT_MUTED, lw=0.5, shrinkA=0, shrinkB=3) if rr > 12 else None)
            bb = t.get_window_extent(R); b = (bb.x0, bb.y0, bb.x1, bb.y1)
            if clear(b) and bb.x0 > 0 and bb.x1 < f.bbox.width:
                taken.append(b); break
            t.remove()
        else:
            continue
        break
    else:
        unplaced.append(txt)
assert not unplaced, f"m6_03 labels could not be placed without overlap: {unplaced}"
f.savefig(style.CHARTS / "m6_03_network.png", dpi=200); plt.close(f)
nodes_out = pd.DataFrame([{"node": n, "kind": H.nodes[n]["kind"], "label": H.nodes[n]["label"], "degree": deg[n], "x": pos[n][0], "y": pos[n][1]} for n in H.nodes])
save_chart_data(nodes_out, "m6_03_network_nodes", "Nodes and layout of the network diagram (funders of 3+ organizations)", ["fact_grants", "dim_funder"], src, S,
                f"concentric layout in inches: Calvary centre, hub funders ({HUB}+ organizations) inner ring, peers middle ring ordered by seed-11 spring-layout angle, other funders at the angle of the peers they fund")

# ------------------------------------------------------------------ board interlocks
rel = load("fact_org_relationships", usecols=["rel_id", "org_a_ein", "org_a_name", "org_b_ein", "org_b_name", "rel_type", "tax_year", "person_id", "confidence", "evidence", "source_id"])
sb = rel[rel.rel_type == "shared_board_member"].copy()
dmv_funders = set(universe("dmv_funders")) | set(universe("daf_sponsors")) | set(universe("calvary_known_funders"))
cand = pd.read_csv(ANALYSIS / "chart_data" / "m5_00_candidate_funders.csv", dtype={"funder_id": str})
cand_ids = set(cand.funder_id)
subj_set = set(subjects) | set(NAMED)
sb["touches_subject"] = sb.org_a_ein.isin(subj_set) | sb.org_b_ein.isin(subj_set)
sb["other_is_funder"] = (sb.org_a_ein.isin(dmv_funders | cand_ids) & sb.org_b_ein.isin(subj_set)) | (sb.org_b_ein.isin(dmv_funders | cand_ids) & sb.org_a_ein.isin(subj_set))
il = sb[sb.touches_subject].copy()
il["subject_ein"] = np.where(il.org_a_ein.isin(subj_set), il.org_a_ein, il.org_b_ein)
il["other_ein"] = np.where(il.org_a_ein.isin(subj_set), il.org_b_ein, il.org_a_ein)
il["other_name"] = np.where(il.org_a_ein.isin(subj_set), il.org_b_name, il.org_a_name)
il["subject"] = il.subject_ein.map(short).fillna(il.subject_ein)
il["other_is_funder"] = il.other_ein.isin(dmv_funders | cand_ids)
il["other_is_candidate"] = il.other_ein.isin(cand_ids)
il["use_in_leadership"] = il.confidence == "high"
il["label"] = np.where(il.confidence == "high", "high confidence", "unconfirmed (medium confidence)")
il = il.sort_values(["subject", "confidence", "other_name"])[["rel_id", "subject_ein", "subject", "other_ein", "other_name", "other_is_funder", "other_is_candidate", "confidence", "label", "use_in_leadership", "tax_year", "evidence", "person_id", "source_id"]]
save_chart_data(il, "m6_04_board_interlocks", "Shared-board links between Calvary / peers / named comparators and other organizations, with confidence", ["fact_org_relationships", "dim_person"], sorted(il.source_id.unique()), S,
                "person_id only (no names); leadership materials use high-confidence rows only; medium rows are labeled unconfirmed")
ci = load("candidate_interlocks")
ci_subj = ci[ci.ein_a.isin(subj_set) | ci.ein_b.isin(subj_set)]
cal_il = il[il.subject_ein == CALVARY]

# ------------------------------------------------------------------ relationship paths for candidate funders (feeds M7)
cal_inst = inst_sets[CALVARY]
close_peers = set(ov[ov.shared_institutional_funders >= 5].ein)
peer_recips = edges.groupby("funder_id").recipient_ein.apply(set)
rows = []
for fid in cand.funder_id:
    recips = peer_recips.get(fid, set()) - {CALVARY}
    cofunders = sum(1 for g in cal_inst if g != fid and len((peer_recips.get(g, set()) - {CALVARY}) & recips) >= 2)
    bi = il[(il.other_ein == fid)]
    rows.append({"funder_id": fid, "peers_funded": len(recips), "close_peers_funded": len(recips & close_peers), "calvary_cofunders_overlapping": cofunders,
                 "board_links_high": int((bi.confidence == "high").sum()), "board_links_medium": int((bi.confidence == "medium").sum()),
                 "board_link_subjects": "; ".join(sorted(set(bi.subject))), "betweenness": btw.get(fid, 0.0)})
paths = pd.DataFrame(rows)
paths["path_strength"] = (np.minimum(paths.peers_funded, 12) / 12 * 0.4 + np.minimum(paths.close_peers_funded, 8) / 8 * 0.25 + np.minimum(paths.calvary_cofunders_overlapping, 20) / 20 * 0.25
                          + np.minimum(paths.board_links_high, 1) * 0.10).round(3)
paths["path_strength_consulting"] = (paths.path_strength + np.minimum(paths.board_links_medium, 1) * 0.05).round(3)
paths = paths.merge(cand[["funder_id", "funder_name", "funder_type", "gap_category"]], on="funder_id", how="left").sort_values("path_strength", ascending=False)
save_chart_data(paths, "m6_05_relationship_paths", "Relationship-path scores for candidate funders: peers funded, close peers, overlapping co-funders, board links", ["fact_grants", "fact_org_relationships", "dim_funder"], src, S,
                "path_strength = 0.4*min(peers,12)/12 + 0.25*min(close peers,8)/8 + 0.25*min(overlapping co-funders,20)/20 + 0.10*(any high-confidence board link); consulting variant adds 0.05 for a medium link")

print(fun.head(25)[["funder_name", "funder_type", "recipients", "amount", "betweenness", "funds_calvary"]].to_string())
print(ov.to_string())
print(cal_il[["subject", "other_name", "other_is_funder", "confidence", "tax_year", "evidence"]].to_string())
print("peer interlocks with funders:", int((il.other_is_funder & (il.subject_ein != CALVARY)).sum()), "high:", int((il.other_is_funder & (il.confidence == 'high')).sum()))
print("candidate_interlocks touching subjects:", len(ci_subj))
print(paths.head(25)[["funder_name", "gap_category", "peers_funded", "close_peers_funded", "calvary_cofunders_overlapping", "board_links_high", "board_links_medium", "path_strength"]].to_string())

top_f = fun.iloc[0]
register_insight("M6-01", "M6", f"The funder web around Calvary and its peers has {len(fun)} funders; the most connected institutional funders (GWCF 18 of 19 organizations, Cafritz 14, Venable 10, Abell 9) already fund Calvary except Venable, and the DAF sponsors (Fidelity, Benevity, Schwab) connect almost everyone.",
                 "m6_01_central_funders", ["m6_03_network", "m6_01_central_funders"], ["fact_grants", "dim_funder"], f"{len(fun)} funders, {len(subjects)} orgs", "high",
                 "Calvary is already inside the core of the DC human-services funder web; the next funders are one step away through peers it shares funders with.", "both")
register_insight("M6-02", "M6", f"Calvary shares the most institutional funders with {ov.iloc[0].org} ({int(ov.iloc[0].shared_institutional_funders)}), {ov.iloc[1].org} ({int(ov.iloc[1].shared_institutional_funders)}) and {ov.iloc[2].org} ({int(ov.iloc[2].shared_institutional_funders)}); House of Ruth DC and House of Ruth MD have the longest lists of institutional funders Calvary lacks.",
                 "m6_02_cofunding_overlap", ["m6_02_cofunding_overlap"], ["fact_grants", "dim_funder"], "overlap", "high",
                 "Those peers' funder lists are the best-evidenced prospect lists: a funder that gives to three organizations with Calvary's profile is likely to consider a fourth.", "both")
register_insight("M6-03", "M6", f"Board interlocks are a thin channel: Calvary has {len(cal_il)} shared-board links in filings, {int((cal_il.confidence=='high').sum())} at high confidence (none with a funder); {int((cal_il.confidence=='medium').sum())} medium-confidence links include Washington Area Women's Foundation, United Way NCA, United Way of Central Maryland and Miriam's Kitchen.",
                 "m6_04_board_interlocks; candidate_interlocks has no Calvary rows", ["m6_04_board_interlocks"], ["fact_org_relationships", "candidate_interlocks"], f"{len(cal_il)} links", "high",
                 "Relationship paths in the leadership materials rest on shared funders, not boards; the medium-confidence links go to the consulting team as leads to confirm.", "both")
log(S, [f"graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges; funders {len(fun)}; Calvary interlocks {len(cal_il)}; paths scored for {len(paths)} candidates", "charts m6_02, m6_03 written; tables m6_01, m6_04, m6_05"])
