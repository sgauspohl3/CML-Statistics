# Why Statistics?

## What statistics is for

Statistics is the discipline of reasoning under uncertainty. Its four core purposes are:

- **Summarize data** — collapse thousands or millions of observations into a handful of numbers (mean, spread, shape) that a human can reason about.
- **Identify trends and patterns** — separate signal from noise; detect relationships between variables.
- **Make inferences** — use a *sample* to draw conclusions about a larger *population* we can't fully observe.
- **Make predictions** — forecast future values, classify unseen cases, or estimate unobserved quantities.

Without statistics, data is just numbers.

```{code-cell} python
import numpy as np

# 10,000 daily temperatures collapsed to a few summary numbers
temps = np.random.normal(loc=72, scale=8, size=10_000)

print(f"Mean:     {temps.mean():.2f}")
print(f"Std dev:  {temps.std():.2f}")
print(f"Min/Max:  {temps.min():.2f} / {temps.max():.2f}")
```

## Why understanding statistics matters

Statistics can be manipulated when the audience doesn't understand them. Common manipulations to watch for:

- **Cherry-picked samples** — choosing data that supports a conclusion
- **Misleading visualizations** — truncated y-axes, dual axes, 3D pie charts
- **Conflating correlation with causation**
- **p-hacking** — running many tests, reporting only the "significant" ones
- **Selection bias** — the data collection process itself filters out cases

Statistical literacy is the main defense against being misled — by advertisers, headlines, papers, and yourself.
