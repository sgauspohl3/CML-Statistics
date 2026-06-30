# Discrete Distributions

Two workhorses cover most discrete situations.

## Binomial

The **Binomial** distribution models the number of "successes" in $n$ independent trials, each with success probability $p$.

$$X \sim \text{Binomial}(n, p)$$

PMF:

$$P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}$$

Mean = $np$, Variance = $np(1-p)$.

*Examples:* number of heads in 10 coin flips; number of defective items in a batch.

```{code-cell} python
from scipy import stats
import numpy as np

n, p = 10, 0.3
X = stats.binom(n, p)

print(f"P(X = 3)     = {X.pmf(3):.4f}")
print(f"P(X <= 3)    = {X.cdf(3):.4f}")
print(f"Mean, Var    = {X.mean()}, {X.var()}")

samples = X.rvs(size=10_000)
print(f"Empirical mean: {samples.mean():.2f}")
```

## Poisson

The **Poisson** distribution models the number of events in a fixed interval when events occur independently at a constant average rate $\lambda$.

$$X \sim \text{Poisson}(\lambda)$$

PMF:

$$P(X = k) = \dfrac{\lambda^k e^{-\lambda}}{k!}$$

Mean = Variance = $\lambda$ (a memorable identity).

*Examples:* customers arriving per hour, typos per page, earthquakes per year.

```{code-cell} python
from scipy import stats

lam = 4   # average 4 events per interval
X = stats.poisson(lam)

print(f"P(X = 0) = {X.pmf(0):.4f}")
print(f"P(X >= 6) = {1 - X.cdf(5):.4f}")
print(f"Mean = {X.mean()}, Var = {X.var()}")
```
