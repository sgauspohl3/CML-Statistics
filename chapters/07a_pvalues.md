# The p-value

## What it is

The p-value is the probability of observing data at least as extreme as ours, *assuming the null hypothesis is true*.

In symbols: $p = P(\text{data this extreme} \mid H_0)$.

## What it isn't

```{warning}
Five common misuses:

1. "p = 0.03 means there's a 3% chance the null is true." **Wrong.** The p-value is $P(\text{data} \mid H_0)$, not $P(H_0 \mid \text{data})$.
2. "p > 0.05 means there's no effect." Only means you couldn't detect one with this sample.
3. Treating p = 0.049 and p = 0.051 as categorically different.
4. **p-hacking** — running many tests, reporting only the significant ones.
5. Confusing **statistical significance** with **practical significance**.
```

## The 0.05 threshold is arbitrary

Ronald Fisher proposed 0.05 as a convention, not a law of nature. There's nothing magical about it. Modern guidance: report effect sizes and confidence intervals *alongside* p-values, and be skeptical of any analysis that hinges on the difference between 0.048 and 0.052.
