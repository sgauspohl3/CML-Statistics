# Variability

Center alone is never enough. Two datasets with identical means can behave entirely differently.

## Variance and standard deviation

**Variance** — average squared deviation from the mean.

- Population: $\sigma^2 = \frac{1}{N}\sum (x_i - \mu)^2$
- Sample: $s^2 = \frac{1}{n-1}\sum (x_i - \bar{x})^2$

```{note}
The sample variance divides by $n-1$, not $n$. This is **Bessel's correction**, and it produces an unbiased estimator of the population variance.
```

**Standard deviation** — square root of variance; same units as the data.

$$\sigma = \sqrt{\sigma^2}, \qquad s = \sqrt{s^2}$$

## Other useful measures

- **Range** — max minus min.
- **IQR** (interquartile range) — Q3 minus Q1; robust to outliers.
- **MAD** (median absolute deviation) — another robust measure.

```{code-cell} python
import numpy as np

data = np.array([2, 4, 4, 4, 5, 5, 7, 9])

# numpy uses ddof=0 (population) by default — set ddof=1 for sample
print(f"Pop variance:  {np.var(data, ddof=0):.2f}")
print(f"Sample var:    {np.var(data, ddof=1):.2f}")
print(f"Pop std:       {np.std(data, ddof=0):.2f}")
print(f"Sample std:    {np.std(data, ddof=1):.2f}")
```
