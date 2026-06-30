# Shape: Skew and Kurtosis

Beyond center and spread, the *shape* of a distribution tells you about asymmetry and tail behavior.

## Skew

Skew measures **asymmetry**.

- **Symmetric** (skew ≈ 0): mean ≈ median. Example: normal distribution.
- **Right-skewed / positive skew**: long tail to the right; **mean > median**. Examples: income, wait times, insurance claims.
- **Left-skewed / negative skew**: long tail to the left; **mean < median**. Examples: age at death in developed countries, exam scores with a ceiling.

Sample skewness:

$$g_1 = \frac{1}{n}\sum_{i=1}^{n}\left(\frac{x_i - \bar{x}}{s}\right)^3$$

```{code-cell} python
import numpy as np
from scipy import stats

right_skewed = np.random.exponential(scale=1, size=10_000)
left_skewed  = -np.random.exponential(scale=1, size=10_000)
symmetric    = np.random.normal(0, 1, size=10_000)

for name, d in [("symmetric", symmetric),
                ("right",     right_skewed),
                ("left",      left_skewed)]:
    print(f"{name:10s} skew = {stats.skew(d):+.2f}")
```

## Kurtosis

Kurtosis measures **tail weight** — how often extreme values appear.

- **Mesokurtic** — normal-like tails; excess kurtosis ≈ 0 (raw kurtosis ≈ 3).
- **Leptokurtic** — heavy tails, sharper peak; excess kurtosis > 0. More outliers than a normal distribution predicts. Examples: financial returns, t-distribution with low degrees of freedom.
- **Platykurtic** — light tails, flatter peak; excess kurtosis < 0. Fewer outliers than normal. Example: uniform distribution.

Excess kurtosis:

$$g_2 = \frac{1}{n}\sum_{i=1}^{n}\left(\frac{x_i - \bar{x}}{s}\right)^4 - 3$$

```{code-cell} python
import numpy as np
from scipy import stats

normal     = np.random.normal(0, 1, 100_000)
heavy_tail = np.random.standard_t(df=3, size=100_000)   # leptokurtic
uniform    = np.random.uniform(-1, 1, 100_000)          # platykurtic

for name, d in [("normal", normal), ("t(df=3)", heavy_tail), ("uniform", uniform)]:
    print(f"{name:10s} excess kurtosis = {stats.kurtosis(d):+.2f}")
```
