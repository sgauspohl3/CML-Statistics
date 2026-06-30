# Relationships Between Distributions

The distributions you've met form a web of connections. Many are special cases or limits of others.

## Key connections

- **Binomial → Normal** (de Moivre–Laplace): for large $n$, $\text{Binomial}(n,p) \approx \mathcal{N}(np, np(1-p))$.
- **Binomial → Poisson**: for large $n$ and small $p$ with $np = \lambda$ fixed, Binomial → $\text{Poisson}(\lambda)$.
- **Poisson ↔ Exponential**: if events arrive as a Poisson process with rate $\lambda$, the inter-arrival times are Exponential($\lambda$).
- **Exponential → Gamma**: sum of $k$ iid Exponential($\lambda$) is Gamma($k$, $1/\lambda$).
- **Exponential → Weibull**: Weibull with shape $k=1$ is Exponential.
- **Gamma → Chi-squared**: $\chi^2_k$ is Gamma($k/2$, $2$).
- **Normal → Chi-squared**: sum of $k$ squared standard normals is $\chi^2_k$.
- **Sum of independent Normals** is Normal.
- **Logistic** ≈ Normal but with heavier tails.

## A worked example: Binomial → Normal

```{code-cell} python
import numpy as np
from scipy import stats

n, p = 1000, 0.3
binom = stats.binom(n, p)
normal_approx = stats.norm(loc=n*p, scale=np.sqrt(n*p*(1-p)))

print(f"Binomial P(X <= 320): {binom.cdf(320):.4f}")
print(f"Normal approx:        {normal_approx.cdf(320):.4f}")
```

The two are nearly identical — for $n = 1000$ and $p = 0.3$, the normal approximation works beautifully.
