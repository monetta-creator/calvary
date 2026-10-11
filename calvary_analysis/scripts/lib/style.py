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
