# Visual design guide

Use this guide to make restrained editorial figures. Adapt to the data and the target journal rather than applying a decorative preset.

## Canvas and typography

- Common starting widths: 89 mm for one column and 183 mm for two columns. Choose height from content; avoid needlessly square panels.
- Design at final publication size. Typical final text is 7–9 pt, with panel labels around 9–11 pt and bold.
- Use a neutral sans-serif typeface consistently. Use mathematical notation only where it adds meaning.
- Prefer sentence case and concise axis labels with units, for example `Concentration (µM)`.
- Place panel labels `a`, `b`, `c` consistently at the upper-left. Panel order should match the narrative and caption.

## Marks and axes

- Use thin, consistent strokes (roughly 0.6–0.9 pt at final size) and marks large enough to survive reduction.
- Remove top and right spines unless they carry information. Use faint grid lines only when quantitative lookup benefits.
- Begin bars at zero. A nonzero baseline can be valid for points or lines, but disclose breaks and avoid exaggerating effects.
- Do not use 3D, gradients, shadows, glossy effects, dual y-axes, or unexplained smoothing.
- Show exact observations where feasible. For dense data, use transparency, small multiples, hexbin/density, or a representative subsample that is explicitly disclosed.

## Color and encoding

Default qualitative palette:

| Role | Hex |
|---|---|
| Blue | `#0072B2` |
| Orange | `#E69F00` |
| Green | `#009E73` |
| Vermilion | `#D55E00` |
| Purple | `#CC79A7` |
| Sky blue | `#56B4E9` |
| Yellow | `#F0E442` |
| Black | `#1A1A1A` |

This palette is generally color-vision-friendly, but test the actual combinations and contrast. Reinforce important groups with shape, line style, direct labels, or facets. Use sequential maps for magnitude and diverging maps only around a meaningful center. Avoid rainbow maps.

## Multi-panel composition

- Align plotting regions, baselines, and shared axes. Use shared legends when mappings are identical.
- Allocate space by information density rather than forcing equal panel sizes.
- Keep repeated axis limits identical when comparison is intended; otherwise label the difference clearly.
- Separate panels with whitespace, not boxes. Put explanatory prose in the caption rather than inside the plotting region.
- Use insets only when they clarify scale or mechanism; mark the referenced region and do not hide contradictory data.
