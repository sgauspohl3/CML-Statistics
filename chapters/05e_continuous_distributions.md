# Continuous Distributions

The six continuous distributions that show up most often in practice.

## Normal

The "bell curve" — pervasive due to the **Central Limit Theorem**.

$$X \sim \mathcal{N}(\mu, \sigma^2)$$

PDF:

$$f(x) = \dfrac{1}{\sigma\sqrt{2\pi}}\exp\!\left(-\dfrac{(x-\mu)^2}{2\sigma^2}\right)$$

Symmetric about $\mu$; obeys the ~68/95/99.7 rule (proportion within $\pm1\sigma$, $\pm2\sigma$, $\pm3\sigma$).

*Examples:* measurement errors, heights, IQ scores.

```{code-cell} python
from scipy import stats

X = stats.norm(loc=0, scale=1)   # standard normal

print(f"P(-1 < X < 1) = {X.cdf(1) - X.cdf(-1):.4f}")    # ~0.6827
print(f"P(-2 < X < 2) = {X.cdf(2) - X.cdf(-2):.4f}")    # ~0.9545
print(f"99th percentile = {X.ppf(0.99):.4f}")
```

## Exponential

Models the **time between events** in a Poisson process (memoryless).

$$X \sim \text{Exp}(\lambda)$$

PDF: $f(x) = \lambda e^{-\lambda x}, \;\; x \ge 0$. Mean = $1/\lambda$, Variance = $1/\lambda^2$.

**Memoryless property:** $P(X > s + t \mid X > s) = P(X > t)$. Past waiting time tells you nothing about future waiting time.

```{code-cell} python
from scipy import stats

X = stats.expon(scale=1/2)   # rate lambda = 2 -> scale = 1/lambda
print(f"P(X < 1)  = {X.cdf(1):.4f}")
print(f"Mean      = {X.mean():.4f}")
```

## Gamma

Generalizes the exponential — models the **sum of $k$ exponential waiting times**.

$$X \sim \text{Gamma}(k, \theta)$$

with shape $k$ and scale $\theta$ (or rate $\beta = 1/\theta$). PDF:

$$f(x) = \dfrac{x^{k-1}e^{-x/\theta}}{\Gamma(k)\theta^k}, \;\; x > 0$$

Mean = $k\theta$, Variance = $k\theta^2$. When $k = 1$ it reduces to the exponential.

*Examples:* total wait time for $k$ events, rainfall amounts, insurance claim sizes.

```{code-cell} python
from scipy import stats
X = stats.gamma(a=3, scale=2)   # shape=3, scale=2
print(f"Mean = {X.mean()}, Var = {X.var()}")
```

## Weibull

The flexible workhorse of **reliability and survival analysis**.

$$X \sim \text{Weibull}(k, \lambda)$$

PDF:

$$f(x) = \dfrac{k}{\lambda}\left(\dfrac{x}{\lambda}\right)^{k-1} e^{-(x/\lambda)^k}$$

The shape parameter controls hazard behavior:

- $k < 1$: decreasing hazard (infant mortality)
- $k = 1$: constant hazard (reduces to Exponential)
- $k > 1$: increasing hazard (wear-out)

```{code-cell} python
from scipy import stats
X = stats.weibull_min(c=1.5, scale=10)
print(f"Mean = {X.mean():.2f}")
```

## Uniform

Every value in $[a, b]$ is equally likely.

$$X \sim \text{Uniform}(a, b)$$

PDF: $f(x) = \dfrac{1}{b - a}$ for $a \le x \le b$. Mean = $(a+b)/2$, Variance = $(b-a)^2/12$.

*Examples:* random number generators, "no prior information" models.

## Logistic

Bell-shaped like the normal but with **heavier tails**.

PDF:

$$f(x) = \dfrac{e^{-(x-\mu)/s}}{s\left(1 + e^{-(x-\mu)/s}\right)^2}$$

Mean = $\mu$, Variance = $\dfrac{s^2 \pi^2}{3}$.

The logistic CDF is the **sigmoid function** — the foundation of logistic regression.
