#!/usr/bin/env python3
"""Generate a reproducible, single-panel scientific figure from tabular data."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from nature_style import PALETTE, new_figure, save_figure


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create an honest, publication-oriented plot from CSV, TSV, or Excel data.")
    parser.add_argument("input", type=Path, help="CSV, TSV, XLS, or XLSX input")
    parser.add_argument("--kind", required=True, choices=("scatter", "line", "box", "violin", "hist"))
    parser.add_argument("--x", help="x column; required except for hist")
    parser.add_argument("--y", required=True, help="numeric y column")
    parser.add_argument("--group", help="optional grouping column")
    parser.add_argument("--sheet", help="Excel sheet name")
    parser.add_argument("--output", required=True, type=Path, help="output stem without extension")
    parser.add_argument("--width", default="single", help="single, double, or width in mm")
    parser.add_argument("--height-mm", type=float, help="explicit figure height in mm")
    parser.add_argument("--x-label")
    parser.add_argument("--y-label")
    parser.add_argument("--title")
    parser.add_argument("--log-y", action="store_true")
    parser.add_argument("--seed", type=int, default=2026, help="seed for display-only jitter")
    return parser.parse_args()


def read_table(path: Path, sheet: str | None) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".tsv", ".txt"}:
        return pd.read_csv(path, sep="\t")
    if suffix in {".xls", ".xlsx"}:
        return pd.read_excel(path, sheet_name=sheet or 0)
    raise ValueError("input must be CSV, TSV, TXT, XLS, or XLSX")


def ordered_values(series: pd.Series) -> list:
    if isinstance(series.dtype, pd.CategoricalDtype):
        present = set(series.dropna())
        return [item for item in series.cat.categories if item in present]
    return list(pd.unique(series.dropna()))


def groups_for(data: pd.DataFrame, group: str | None):
    if group is None:
        return [(None, data)]
    return [(value, data.loc[data[group] == value]) for value in ordered_values(data[group])]


def draw(args: argparse.Namespace, data: pd.DataFrame):
    width: str | float = args.width
    if width not in {"single", "double"}:
        width = float(width)
    fig, ax = new_figure(width, height_mm=args.height_mm)
    rng = np.random.default_rng(args.seed)

    if args.kind == "hist":
        for index, (name, frame) in enumerate(groups_for(data, args.group)):
            ax.hist(frame[args.y], bins="auto", histtype="step", lw=1.1, color=PALETTE[index % len(PALETTE)], label=name)
    elif args.kind in {"scatter", "line"}:
        for index, (name, frame) in enumerate(groups_for(data, args.group)):
            frame = frame.sort_values(args.x) if args.kind == "line" else frame
            color = PALETTE[index % len(PALETTE)]
            if args.kind == "scatter":
                ax.scatter(frame[args.x], frame[args.y], s=18, alpha=0.8, color=color, edgecolors="white", linewidths=0.35, label=name)
            else:
                ax.plot(frame[args.x], frame[args.y], marker="o", color=color, label=name)
    else:
        categories = ordered_values(data[args.x])
        values = [data.loc[data[args.x] == category, args.y].to_numpy(dtype=float) for category in categories]
        positions = np.arange(len(categories))
        if args.kind == "box":
            artists = ax.boxplot(values, positions=positions, widths=0.56, patch_artist=True, showfliers=False, medianprops={"color": "#1A1A1A"})
            for index, patch in enumerate(artists["boxes"]):
                patch.set_facecolor(PALETTE[index % len(PALETTE)])
                patch.set_alpha(0.42)
        else:
            artists = ax.violinplot(values, positions=positions, widths=0.72, showmeans=False, showmedians=True, showextrema=False)
            for index, body in enumerate(artists["bodies"]):
                body.set_facecolor(PALETTE[index % len(PALETTE)])
                body.set_edgecolor("#1A1A1A")
                body.set_alpha(0.42)
        for index, values_at_position in enumerate(values):
            jitter = rng.uniform(-0.13, 0.13, size=len(values_at_position))
            ax.scatter(index + jitter, values_at_position, s=12, color=PALETTE[index % len(PALETTE)], alpha=0.75, edgecolors="white", linewidths=0.3, zorder=3)
        ax.set_xticks(positions, [str(item) for item in categories])

    if args.group and args.kind in {"scatter", "line", "hist"}:
        ax.legend(title=args.group)
    if args.log_y:
        if (data[args.y] <= 0).any():
            raise ValueError("log-y requested but the y column contains zero or negative values")
        ax.set_yscale("log")
    default_x_label = args.x or "" if args.kind in {"scatter", "line"} else ""
    ax.set_xlabel(args.x_label if args.x_label is not None else default_x_label)
    ax.set_ylabel(args.y_label if args.y_label is not None else args.y)
    if args.title:
        ax.set_title(args.title)
    fig.tight_layout()
    return fig


def main() -> int:
    args = parse_args()
    if args.kind != "hist" and not args.x:
        raise ValueError(f"--x is required for {args.kind}")
    if args.group and args.kind in {"box", "violin"}:
        raise ValueError("--group is not used for box/violin plots; encode categories with --x")
    data = read_table(args.input, args.sheet)
    required = [args.y] + ([args.x] if args.kind != "hist" else []) + ([args.group] if args.group else [])
    missing_columns = [column for column in required if column not in data.columns]
    if missing_columns:
        raise ValueError(f"missing columns: {', '.join(missing_columns)}")

    original_rows = len(data)
    plot_data = data.dropna(subset=required).copy()
    plot_data[args.y] = pd.to_numeric(plot_data[args.y], errors="raise")
    if not len(plot_data):
        raise ValueError("no complete rows remain for plotting")
    if args.kind in {"scatter", "line"}:
        plot_data[args.x] = pd.to_numeric(plot_data[args.x], errors="raise")

    fig = draw(args, plot_data)
    written = save_figure(fig, args.output)
    plt.close(fig)

    notes_path = args.output.with_name(f"{args.output.name}_notes.json")
    notes_path.parent.mkdir(parents=True, exist_ok=True)
    notes = {
        "input": str(args.input.resolve()),
        "kind": args.kind,
        "columns": {"x": args.x, "y": args.y, "group": args.group},
        "rows_in_input": original_rows,
        "rows_plotted": len(plot_data),
        "rows_excluded_for_missing_plot_fields": original_rows - len(plot_data),
        "group_counts": plot_data[args.group].value_counts(dropna=False).to_dict() if args.group else None,
        "display_only_jitter_seed": args.seed if args.kind in {"box", "violin"} else None,
        "statistics": "No inferential statistics computed.",
        "outputs": [str(path) for path in written],
    }
    notes_path.write_text(json.dumps(notes, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    print("\n".join(str(path) for path in [*written, notes_path]))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
