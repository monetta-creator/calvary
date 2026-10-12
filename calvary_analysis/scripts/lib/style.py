"""Chart style for the Calvary engagement. The palette and rules are documented in
storylines/design_system.md; this module is the executable version.

Roles, not hues: every chart picks colors by what the series *is* (government, institutional
philanthropy, DAF, individuals/events, other) so an entity keeps its color across all charts.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.collections import PathCollection  # noqa: E402
from matplotlib.colors import to_hex  # noqa: E402
from matplotlib.container import BarContainer  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

from .common import CHARTS, AS_OF  # noqa: E402

# Brand (from the client template): used for ink, titles, dark surfaces, accents. Not for data series.
INK = "#41242F"          # Calvary plum: titles, primary text, dark slide backgrounds
GOLD = "#D39F28"         # Calvary gold: accent, highlights, logo
GOLD_LIGHT = "#FFDD7F"
TEAL_LIGHT = "#B1E1E9"

# Text tokens
TEXT = "#1F1B1D"
TEXT_2 = "#5C5458"
TEXT_MUTED = "#8C8488"
GRID = "#E6E2E4"
SURFACE = "#FFFFFF"
SURFACE_2 = "#F6F3F4"    # card / band tint

# Categorical data palette (validated with the dataviz skill's validate_palette.js, light mode,
# adjacent pairs: lightness band, chroma floor, CVD separation, normal-vision floor and 3:1 contrast all pass).
SERIES = {
    "government": "#A03F7E",      # slot 1: berry (brand-adjacent plum)
    "institutional": "#B8810C",   # slot 2: gold (foundations, corporate foundations, federated, community fdns)
    "daf": "#0F9ACB",             # slot 3: teal (donor-advised fund sponsors)
    "individuals": "#CF5A2C",     # slot 4: brick (individuals, events, residual private)
    "other": "#3B6FD8",           # slot 5: slate blue (program/investment/other revenue)
}
CALVARY_COLOR = SERIES["government"]   # Calvary as an entity on peer charts
PEER_COLOR = "#B9B2B6"                 # peers as a muted set
NAMED_COLOR = SERIES["daf"]            # DWC / SheWorks reference rows
HIGHLIGHT = GOLD
NEGATIVE = "#B23A48"                   # status: deficit / cut (only where the color means bad)
POSITIVE = "#2E7D5B"                   # status: surplus / restored

# Sequential ramp (one hue, light -> dark) for magnitude (maps, heat tables): berry family
SEQUENTIAL = ["#F7E6F0", "#E9BFD9", "#D693BD", "#BF669E", "#A03F7E", "#7A2A5E", "#521A40"]
# Diverging (cut vs. increase): brick <-> neutral <-> teal
DIVERGING = ["#CF5A2C", "#E9A98E", "#F3E6E0", "#D9D5D7", "#CFE9F3", "#7CC3E0", "#0F9ACB"]

FONT = "Arial"


def apply() -> None:
    plt.rcParams.update({
        "font.family": FONT,
        "font.size": 10,
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.titlecolor": INK,
        "axes.labelsize": 9.5,
        "axes.labelcolor": TEXT_2,
        "axes.edgecolor": GRID,
        "axes.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "grid.color": GRID,
        "grid.linewidth": 0.8,
        "grid.linestyle": "-",
        "xtick.color": TEXT_2,
        "ytick.color": TEXT_2,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.frameon": False,
        "legend.fontsize": 9,
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "lines.linewidth": 2.0,
        "lines.solid_capstyle": "round",
        "lines.solid_joinstyle": "round",
        "figure.dpi": 100,
        "text.parse_math": False,   # dollar signs in titles and notes are money, not TeX
    })


def fig(w: float = 10, h: float = 5.6):
    apply()
    return plt.subplots(figsize=(w, h))


def money_axis(ax, unit: str = "M", axis: str = "y") -> None:
    if unit == "M":
        f = FuncFormatter(lambda v, _: f"${v/1e6:,.1f}M" if abs(v) < 10e6 else f"${v/1e6:,.0f}M")
    elif unit == "K":
        f = FuncFormatter(lambda v, _: f"${v/1e3:,.0f}K")
    else:
        f = FuncFormatter(lambda v, _: f"${v:,.0f}")
    (ax.yaxis if axis == "y" else ax.xaxis).set_major_formatter(f)


def pct_axis(ax, axis: str = "y") -> None:
    (ax.yaxis if axis == "y" else ax.xaxis).set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0%}"))


BAR_OUTLINE = 0.5  # pt; about 1.4 px at 200 dpi, which reads as a 1 px line once the PNG is scaled onto a slide


def _declutter(figure, ax) -> tuple[int, list[str]]:
    """Nudge data labels that overlap an earlier label: try small offsets up, down, right, left (6-30 pt) and keep the
    first that clears every placed label and stays in the figure. White labels sit inside marks and are never moved.
    Returns (labels moved, labels still overlapping)."""
    from matplotlib.text import Annotation
    from matplotlib.transforms import Bbox
    R = figure.canvas.get_renderer()
    fig_bb = figure.bbox
    placed, moved, stuck = [], 0, []
    for coll in ax.collections:  # scatter dots are taken too, so a label never sits on another point
        if isinstance(coll, PathCollection) and len(coll.get_offsets()):
            sizes = coll.get_sizes() if len(coll.get_sizes()) else [36]
            for i, xy in enumerate(ax.transData.transform(coll.get_offsets())):
                r = (sizes[i % len(sizes)] ** 0.5) * figure.dpi / 72 / 2
                placed.append(Bbox.from_extents(xy[0] - r, xy[1] - r, xy[0] + r, xy[1] + r))
    texts = [t for t in ax.texts if t.get_visible() and t.get_text().strip() and t.get_transform() != ax.transAxes]
    pad = lambda bb: bb.expanded(1.04, 1.18)
    clear = lambda bb: not any(bb.overlaps(p) for p in placed) and fig_bb.contains(bb.x0, bb.y0) and fig_bb.contains(bb.x1, bb.y1)
    for t in texts:
        bb = pad(t.get_window_extent(R))
        if clear(bb):
            placed.append(bb); continue
        white = to_hex(t.get_color()).lower() == "#ffffff"
        is_off = isinstance(t, Annotation) and t.anncoords == "offset points"
        if white or not (is_off or t.get_transform() == ax.transData):
            stuck.append(t.get_text()); placed.append(bb); continue
        home = t.xyann if is_off else t.get_position()
        done = False
        for step in (6, 9, 12, 16, 20, 25, 30):
            for dx, dy in ((0, step), (0, -step), (step, 0), (-step, 0)):
                if is_off:
                    t.xyann = (home[0] + dx, home[1] + dy)
                else:  # data-coordinate text: shift by points in display space
                    px = ax.transData.transform(home) + [dx * figure.dpi / 72, dy * figure.dpi / 72]
                    t.set_position(ax.transData.inverted().transform(px))
                nb = pad(t.get_window_extent(R))
                if clear(nb):
                    placed.append(nb); moved += 1; done = True
                    if is_off and t.arrow_patch is None and step >= 9:  # a thin line back to its point keeps attribution clear
                        from matplotlib.patches import FancyArrowPatch
                        t.arrowprops = dict(arrowstyle="-", color=TEXT_MUTED, lw=0.6, shrinkA=0, shrinkB=4)
                        t._arrow_relpos = (0.5, 0.5)
                        t.arrow_patch = FancyArrowPatch((0, 0), (1, 1), **t.arrowprops)
                    break
            if done:
                break
        if not done:
            if is_off:
                t.xyann = home
            else:
                t.set_position(home)
            stuck.append(t.get_text()); placed.append(bb)
    return moved, stuck


def polish(figure, name: str = "") -> None:
    """House axis style, applied to every chart just before it is saved (engagement lead, 2026-10-11): no grid lines,
    black x and y axis lines and ticks, bold black tick labels, axis labels and data labels, a 1 px black outline on
    bars (replacing the white gaps), and data labels nudged off each other and off scatter dots. Notes placed in axes
    coordinates (e.g. "Labels: government share") keep their weight. Charts with their axes switched off are untouched."""
    figure.canvas.draw()  # materialize tick labels so their weight can be set
    for leg in [a.get_legend() for a in figure.axes] + list(figure.legends):  # bar swatches match the outlined bars
        for h in (getattr(leg, "legend_handles", []) if leg else []):
            if isinstance(h, Rectangle):
                h.set_edgecolor(TEXT)
                h.set_linewidth(BAR_OUTLINE)
    grey = {to_hex(TEXT_2).lower(), to_hex(TEXT_MUTED).lower()}
    for ax in figure.axes:
        if not ax.axison:
            continue
        ax.grid(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color(TEXT)
            ax.spines[side].set_linewidth(0.9)
        ax.tick_params(which="both", colors=TEXT)
        for t in ax.get_xticklabels() + ax.get_yticklabels() + [ax.xaxis.label, ax.yaxis.label]:
            t.set_fontweight("bold")
            t.set_color(TEXT)
        for t in ax.texts:  # data labels
            if t.get_transform() == ax.transAxes:
                continue
            t.set_fontweight("bold")
            if to_hex(t.get_color()).lower() in grey:
                t.set_color(TEXT)
        for cont in ax.containers:  # 1 px black outline on every bar and stacked segment; none on empty segments
            if isinstance(cont, BarContainer):
                for p in cont.patches:
                    p.set_edgecolor(TEXT)
                    p.set_linewidth(0 if p.get_height() == 0 or p.get_width() == 0 else BAR_OUTLINE)
        moved, stuck = _declutter(figure, ax)
        if moved or stuck:
            print(f"  labels {name or '?'}: moved {moved}" + (f"; still overlapping: {stuck}" if stuck else ""))


def finish(figure, ax, chart_id: str, title: str, source: str, note: str | None = None,
           subtitle: str | None = None) -> Path:
    """Title (figure-left, bold, ink), optional subtitle, source + as-of footer; save PNG at 200 dpi."""
    import textwrap
    width_in = figure.get_size_inches()[0]
    tw = textwrap.fill(title, width=int(width_in * 9.5))
    n_title = tw.count("\n") + 1
    top = 1 - 0.042 * n_title - (0.03 if subtitle else 0) - 0.015
    figure.text(0.01, 0.985, tw, fontsize=12.5, fontweight="bold", color=INK, va="top", ha="left")
    if subtitle:
        figure.text(0.01, 0.985 - 0.042 * n_title, subtitle, fontsize=9.5, color=TEXT_2, va="top", ha="left")
    foot = f"Source: {source}. Data as of {AS_OF}. Chart {chart_id}."
    if note:
        foot = f"{textwrap.fill(note, width=int(width_in * 15))}\n{foot}"
    n_foot = foot.count("\n") + 1
    figure.text(0.01, 0.005, foot, fontsize=7.5, color=TEXT_MUTED, va="bottom", ha="left")
    polish(figure, chart_id)
    figure.tight_layout(rect=(0, 0.02 + 0.022 * n_foot, 1, top))
    CHARTS.mkdir(exist_ok=True)
    out = CHARTS / f"{chart_id}.png"
    figure.savefig(out, dpi=200)
    plt.close(figure)
    return out


def label_bar_tips(ax, bars, fmt=lambda v: f"${v/1e6:,.1f}M", color=TEXT_2, inside=False, fontsize=8.5):
    for b in bars:
        v = b.get_height() if b.get_width() < b.get_height() or b.get_x() == 0 else b.get_width()
        if b.get_height() and abs(b.get_height()) >= abs(b.get_width()):
            x, y = b.get_x() + b.get_width() / 2, b.get_y() + b.get_height()
            ax.annotate(fmt(b.get_height()), (x, y), xytext=(0, -12 if inside else 3), textcoords="offset points",
                        ha="center", va="bottom" if not inside else "top", fontsize=fontsize,
                        color="white" if inside else color)
        else:
            x, y = b.get_x() + b.get_width(), b.get_y() + b.get_height() / 2
            ax.annotate(fmt(b.get_width()), (x, y), xytext=(-4 if inside else 4, 0), textcoords="offset points",
                        ha="right" if inside else "left", va="center", fontsize=fontsize,
                        color="white" if inside else color)
