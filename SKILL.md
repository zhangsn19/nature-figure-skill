---
name: nature-figure
description: Create or refine publication-ready scientific data figures in a clean Nature/Science-like editorial style, including statistical plots, multi-panel layouts, and reproducible vector/high-resolution exports. Use for figures grounded in supplied research data; do not use for decorative scientific illustrations, graphical abstracts without quantitative data, or image manipulation that could alter scientific evidence.
---

# Nature Figure

Turn the user's data and scientific intent into an accurate, restrained, publication-ready figure. “Nature/Science-like” means an editorial visual standard, not imitation of a journal brand or a guarantee of acceptance.

## Work from evidence

- Inspect the source data, units, missingness, sample sizes, grouping, repeated measures, and uncertainty before plotting.
- Never invent measurements, labels, replicates, statistical results, or biological meaning. Keep raw data unchanged and write transformations into the reproducible plotting script.
- Ask only when an ambiguity would materially change the scientific claim. Otherwise make a conservative assumption and disclose it in the figure notes.
- Prefer plots that reveal distributions and individual observations. Avoid a bar chart of means when a dot, box, violin, interval, or estimation plot communicates the data better.
- Treat color, axis limits, filtering, aggregation, smoothing, and significance annotations as scientific choices—not decoration.

## Produce a complete figure package

Unless the user requests otherwise, deliver:

1. An editable plotting script that reads the original data.
2. SVG and PDF vector outputs, plus a 600 dpi PNG preview.
3. A short notes file recording input files, transformations, statistics, sample-size definition, uncertainty meaning, and any assumptions.

Use `scripts/nature_style.py` from the skill directory to set typography, dimensions, panel labels, significance brackets, and exports. For a straightforward single-panel CSV/TSV/XLSX plot, `scripts/plot_data.py` can generate the package directly; use `--help` before running it. For multi-panel or domain-specific figures, import the style helper into a custom script rather than forcing the data through the generic CLI.

Keep generated artifacts in a dedicated output directory. Do not overwrite source data or an existing figure unless explicitly asked.

## Choose and refine the design

- Read [references/visual-design.md](references/visual-design.md) when selecting geometry, dimensions, colors, typography, or multi-panel layout.
- Read [references/statistical-integrity.md](references/statistical-integrity.md) whenever computing summaries, uncertainty, fits, tests, or significance annotations.
- Read [references/figure-checklist.md](references/figure-checklist.md) before final delivery or when adapting a figure to a named journal.

Start with common editorial dimensions (89 mm single-column or 183 mm double-column), but verify the current target journal's author instructions when exact compliance is requested. Do not claim that a house style is officially endorsed.

## Final quality control

- Run the plotting script from a clean output directory and confirm it reproduces every deliverable.
- Inspect the rendered PNG at full size and thumbnail size. Check clipping, overlap, legibility, panel order, legend mapping, and whether patterns remain distinguishable without color.
- Confirm vector text remains editable, raster elements have sufficient effective resolution, and fonts are embedded or safely substituted.
- Cross-check plotted counts and summary values against the source data. Report warnings instead of silently dropping rows.
