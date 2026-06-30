# Goodness of Fit

How well does a proposed distribution actually fit the data? Always check before relying on a fitted model.

## Visual checks

- **Q-Q plot** — quantiles of data vs. quantiles of the candidate distribution. A straight line is a good fit.
- **P-P plot** — cumulative probabilities of data vs. cumulative probabilities of the candidate.
- **ECDF overlay** — empirical CDF on top of the fitted CDF.

Visual checks come first. If a Q-Q plot shows a clear curve, no formal test will save the fit.

## Formal tests

- **Kolmogorov–Smirnov (KS)** — max distance between empirical and theoretical CDF.
- **Anderson–Darling** — weighted KS, more sensitive to tails.
- **Chi-squared** — for binned or categorical data.

## Model selection criteria

For comparing multiple candidate distributions, lower is better:

$$\text{AIC} = 2k - 2\ln(\hat{L})$$
$$\text{BIC} = k\ln(n) - 2\ln(\hat{L})$$

where $k$ is the number of parameters and $\hat{L}$ is the maximized likelihood.

```{code-cell} python
from scipy import stats
import numpy as np

data = np.random.normal(0, 1, 500)

# Fit a normal, then test it
mu, sigma = stats.norm.fit(data)
ks_stat, p_value = stats.kstest(data, "norm", args=(mu, sigma))

print(f"KS test: stat = {ks_stat:.3f}, p = {p_value:.3f}")
```
