# The Rumsfeld Matrix

A simple 2×2 framework for **epistemic awareness** — what do we know about what we know?

|                       | **Aware**        | **Unaware**        |
|-----------------------|------------------|--------------------|
| **Known**             | Known knowns     | Unknown knowns     |
| **Unknown**           | Known unknowns   | Unknown unknowns   |

## The four quadrants

**Known knowns** — facts we possess and know we possess.
*Example:* the sample size of our dataset.

**Known unknowns** — things we know we don't know, and can plan for.
*Example:* next month's sales — we don't know them, but we know we need to forecast them.

**Unknown knowns** — assumptions and biases baked into our thinking that we haven't surfaced.
*Example:* assuming data is normally distributed without checking; using a model trained on data that doesn't represent production.

```{warning}
The "unknown knowns" quadrant is often the most dangerous for statisticians. The assumptions you don't realize you're making are the ones that bite.
```

**Unknown unknowns** — risks we haven't even conceived of.
*Example:* a black swan event, a confounding variable nobody thought to measure.

## Why it matters

Good statistical practice converts:

- **Unknown unknowns → known unknowns** through diagnostics, exploratory data analysis, and sensitivity analysis.
- **Unknown knowns → known knowns** by documenting assumptions explicitly.
