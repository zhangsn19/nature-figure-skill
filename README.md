# Nature Figure Skill

A Codex skill for turning research data into accurate, reproducible, publication-ready scientific figures with a restrained Nature/Science-like editorial aesthetic.

It combines decision guidance with executable Matplotlib tooling. The skill prioritizes scientific integrity, visible raw data, accessible color, editable vector output, and a reproducible record of every transformation. It is not affiliated with or endorsed by Nature Portfolio or Science/AAAS.

## Highlights

- Routes plot design, statistical integrity, and final quality control through focused guidance.
- Includes reusable Matplotlib helpers for journal-scale dimensions, typography, panel labels, p-value brackets, and export.
- Includes a zero-seaborn CLI for scatter, line, box, violin, and histogram plots from CSV/TSV/Excel data.
- Produces SVG, PDF, 600 dpi PNG, and machine-readable figure notes.
- Uses an accessible qualitative palette and editable SVG text.

## Install

Copy or clone this folder to `~/.codex/skills/nature-figure`, then start a new Codex turn so the skill can be discovered.

Requirements:

```bash
python -m pip install -r requirements.txt
```

## Use with Codex

```text
Use $nature-figure to create a two-panel publication figure from results.csv.
Panel a should show all observations by treatment; panel b should show the paired change.
Export SVG, PDF, and 600 dpi PNG, and document every assumption.
```

Codex reads [`SKILL.md`](SKILL.md), inspects the supplied data, loads only the relevant references, and creates a reproducible figure package.

## Direct CLI

```bash
python scripts/plot_data.py results.csv \
  --kind box \
  --x treatment \
  --y response \
  --y-label "Response (a.u.)" \
  --output figures/figure_1
```

Try the included data with `examples/demo.csv`. The CLI preserves input order for categorical axes, overlays raw observations on distribution summaries, and writes a JSON audit record beside every figure.

For multi-panel or domain-specific figures, import `scripts/nature_style.py` into a custom plotting script.

## Scope

This skill is for quantitative, data-grounded figures. It deliberately avoids fabricated data, decorative scientific illustration, and image edits that could compromise scientific evidence. A named journal's current author instructions remain authoritative for exact submission requirements.

## License

MIT
