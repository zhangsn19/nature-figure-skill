# Statistical integrity

Read this before computing or displaying any summary, uncertainty, model fit, test, or significance mark.

## Preserve the experimental unit

Identify the independent experimental unit before calculating `n`. Technical replicates are not independent biological replicates. For paired or repeated observations, retain subject identifiers and show pairing or use an appropriate repeated-measures model. State what `n` represents.

## Summaries and uncertainty

- Show raw observations when feasible, together with a summary that matches the distribution and scientific question.
- For roughly symmetric continuous data, mean with a confidence interval may be useful. For skewed data, median and quantiles are often more honest.
- Label error bars explicitly as SD, SEM, confidence interval, credible interval, or another defined quantity. Never use a generic “error bars” label.
- Do not silently remove missing values or outliers. Report exclusions and the rule used. Distinguish absent observations from true zeroes.
- Bootstrap intervals should resample at the independent-unit level. For hierarchical or paired data, use a design-aware method.

## Tests, models, and annotations

- Compute a test only when its assumptions and experimental design are supported. Keep the exact test, sidedness, effect estimate, interval, multiple-testing correction, and sample sizes in the notes.
- Prefer effect sizes with uncertainty over stars alone. If significance marks are requested, include exact p-values when space allows and define the thresholds.
- Never infer significance from overlap of standard-error bars. Never add significance marks from values not present or reproducibly computed.
- Fit curves only when the model is scientifically justified. Distinguish fitted lines from visual smoothers and show uncertainty when appropriate.
- Do not connect unordered categories with lines or imply continuity that the experiment did not measure.

## Computational record

The plotting script should expose, not hide, preprocessing. Preserve category order, units, random seeds, package versions where material, and all parameters used for intervals, jitter, models, and tests. Cross-check the plotted row count and group summaries against an independent table before delivery.
