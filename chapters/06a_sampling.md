# Samples, Populations, Sampling

The core distinction:

- **Population** — the full set of units we want to learn about (often unobservable).
- **Sample** — a subset we actually measure.
- **Parameter** — a number describing the population (e.g., $\mu$, $\sigma$).
- **Statistic** — a number computed from the sample (e.g., $\bar{x}$, $s$).

The goal of inference is to use **statistics** to estimate **parameters**.

## Sampling methods

- **Simple random sampling** — every unit equally likely.
- **Stratified** — partition into strata, sample within each (reduces variance).
- **Cluster** — sample whole groups (cheaper).
- **Systematic** — every $k$-th element.

```{warning}
Beware **sampling bias**: if your selection mechanism is related to what you're measuring, your estimates will be biased no matter how large the sample. A poll conducted online about internet usage will systematically miss the people who don't use the internet.
```

## A simulated example

```{code-cell} python
import numpy as np
np.random.seed(42)

population = np.random.normal(loc=100, scale=15, size=1_000_000)
sample = np.random.choice(population, size=100, replace=False)

print(f"Population mean: {population.mean():.2f}")
print(f"Sample mean:     {sample.mean():.2f}")
```

A sample of 100 from a population of a million gives a very reasonable estimate of the population mean. This isn't luck — it's the Law of Large Numbers at work.
