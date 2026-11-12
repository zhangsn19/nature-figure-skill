#!/usr/bin/env python3
"""Small Matplotlib helpers for publication-ready scientific figures."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Mapping, Sequence

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

MM_PER_INCH = 25.4
SINGLE_COLUMN_MM = 89.0
DOUBLE_COLUMN_MM = 183.0

PALETTE = (
    "#0072B2", "#E69F00", "#009E73", "#D55E00",
    "#CC79A7", "#56B4E9", "#F0E442", "#1A1A1A",
)


def set_style(base_font_size: float = 8.0) -> None:
    """Apply a restrained, vector-friendly scientific figure style."""
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": base_font_size,
        "axes.labelsize": base_font_size,
        "axes.titlesize": base_font_size + 1,
        "axes.linewidth": 0.75,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.prop_cycle": mpl.cycler(color=PALETTE),
        "xtick.labelsize": base_font_size - 1,
        "ytick.labelsize": base_font_size - 1,
        "xtick.major.size": 3,
        "ytick.major.size": 3,
        "xtick.major.width": 0.7,
        "ytick.major.width": 0.7,
        "legend.fontsize": base_font_size - 1,
        "legend.frameon": False,
        "lines.linewidth": 1.1,
        "lines.markersize": 4,
        "patch.linewidth": 0.7,
        "figure.dpi": 150,
        "savefig.dpi": 600,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
        "savefig.facecolor": "white",
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })


def figure_size(width: str | float = "single", *, aspect: float = 0.72, height_mm: float | None = None) -> tuple[float, float]:
    """Return a Matplotlib figure size in inches from millimetres."""
    if isinstance(width, str):
        choices = {"single": SINGLE_COLUMN_MM, "double": DOUBLE_COLUMN_MM}
        if width not in choices:
            raise ValueError("width must be 'single', 'double', or millimetres")
        width_mm = choices[width]
    else:
        width_mm = float(width)
    if width_mm <= 0 or aspect <= 0 or (height_mm is not None and height_mm <= 0):
        raise ValueError("dimensions and aspect must be positive")
    resolved_height = float(height_mm) if height_mm is not None else width_mm * aspect
    return width_mm / MM_PER_INCH, resolved_height / MM_PER_INCH


def new_figure(width: str | float = "single", *, aspect: float = 0.72, height_mm: float | None = None, **subplots_kwargs):
    """Create a styled figure and axes at a publication-oriented size."""
    set_style()
    return plt.subplots(figsize=figure_size(width, aspect=aspect, height_mm=height_mm), **subplots_kwargs)


def flatten_axes(axes) -> list:
    """Return a predictable list for scalar, list, or ndarray axes objects."""
    return list(np.asarray(axes, dtype=object).reshape(-1))


def label_panels(axes, labels: Sequence[str] | None = None, *, x: float = -0.16, y: float = 1.06, fontsize: float = 10) -> None:
    """Add consistent lowercase panel labels in axes coordinates."""
    items = flatten_axes(axes)
    resolved = list(labels) if labels is not None else [chr(97 + i) for i in range(len(items))]
    if len(resolved) != len(items):
        raise ValueError("the number of panel labels must match the axes")
    for ax, label in zip(items, resolved):
        ax.text(x, y, label, transform=ax.transAxes, fontsize=fontsize, fontweight="bold", va="top", ha="left")


def significance_text(p_value: float) -> str:
    """Return a compact conventional p-value label."""
    if not np.isfinite(p_value) or p_value < 0 or p_value > 1:
        raise ValueError("p_value must be finite and between 0 and 1")
    if p_value < 0.0001:
        return "p < 0.0001"
    return f"p = {p_value:.3g}"


def add_significance(ax, x1: float, x2: float, y: float, p_value: float, *, height: float | None = None, text: str | None = None) -> None:
    """Add a bracket for a p-value that was computed with a valid design."""
    span = np.diff(ax.get_ylim())[0]
    h = 0.025 * span if height is None else height
    ax.plot([x1, x1, x2, x2], [y, y + h, y + h, y], color="#1A1A1A", lw=0.8, clip_on=False)
    ax.text((x1 + x2) / 2, y + h, text or significance_text(p_value), ha="center", va="bottom")


def save_figure(fig, output_stem: str | Path, *, formats: Iterable[str] = ("svg", "pdf", "png"), dpi: int = 600, metadata: Mapping[str, str] | None = None) -> list[Path]:
    """Save vector masters and a high-resolution raster preview."""
    stem = Path(output_stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for raw_format in formats:
        fmt = raw_format.lower().lstrip(".")
        if fmt not in {"svg", "pdf", "png", "tif", "tiff"}:
            raise ValueError(f"unsupported output format: {raw_format}")
        path = stem.with_suffix(f".{fmt}")
        kwargs = {"format": fmt, "bbox_inches": "tight", "facecolor": "white"}
        if fmt in {"png", "tif", "tiff"}:
            kwargs["dpi"] = dpi
        if metadata and fmt in {"svg", "pdf", "png"}:
            kwargs["metadata"] = dict(metadata)
        fig.savefig(path, **kwargs)
        written.append(path)
    return written
