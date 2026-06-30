# Confidence Intervals

A confidence interval quantifies uncertainty about an estimate.

## What a 95% CI means

If we repeated the entire procedure many times, about 95% of the intervals we constructed would contain the true parameter.

```{warning}
A 95% CI does **not** mean "there is a 95% probability that the true value lies in this interval." That's a Bayesian credible interval — a different object with a different meaning. Frequentist intervals are about the procedure's long-run performance, not about a probability statement on any single interval.
```

## Analytical CI for the mean

**$\sigma$ known, or large $n$:**

$$\bar{x} \pm z_{1-\alpha/2}\,\frac{\sigma}{\sqrt{n}}$$

**$\sigma$ unknown, small $n$ (use the t-distribution):**

$$\bar{x} \pm t_{1-\alpha/2,\, n-1}\,\frac{s}{\sqrt{n}}$$

```{code-cell} python
import numpy as np
from scipy import stats

data = np.random.normal(loc=10, scale=2, size=30)

mean = data.mean()
sem  = stats.sem(data)
ci   = stats.t.interval(0.95, df=len(data)-1, loc=mean, scale=sem)

print(f"Mean = {mean:.2f}, 95% CI = [{ci[0]:.2f}, {ci[1]:.2f}]")
```

## Bootstrap CIs

When analytical CIs are intractable, **resample with replacement** from the data, compute the statistic each time, and take percentiles of the resulting distribution.

The bootstrap works for *any* statistic — medians, ratios, complex estimators — with no distributional assumptions.

```{code-cell} python
import numpy as np

rng = np.random.default_rng(0)
data = rng.normal(loc=10, scale=2, size=30)

B = 10_000
boot_means = [rng.choice(data, size=len(data), replace=True).mean()
              for _ in range(B)]

ci_low, ci_high = np.percentile(boot_means, [2.5, 97.5])
print(f"Bootstrap 95% CI for the mean: [{ci_low:.2f}, {ci_high:.2f}]")
```
