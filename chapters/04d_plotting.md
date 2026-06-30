# Plotting Distributions

Numerical summaries hide things that plots reveal. Two essential tools:

## Histogram

The histogram bins data into ranges and counts observations per bin. It shows shape, center, spread, modality, and outliers at a glance.

Bin choice matters: too few hides structure, too many adds noise. Common rules: Sturges, Freedman-Diaconis, Scott.

```{code-cell} python
import numpy as np
import matplotlib.pyplot as plt

data = np.random.normal(loc=0, scale=1, size=1000)

plt.hist(data, bins=30, edgecolor="black", alpha=0.7)
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.title("Histogram of sample data")
plt.show()
```

## Empirical CDF (ECDF)

The **empirical cumulative distribution function** plots the proportion of data ≤ x.

- No binning decisions — every data point gets a step.
- Excellent for comparing distributions.
- You can read percentiles off the y-axis directly.

$$\hat{F}_n(x) = \frac{1}{n}\sum_{i=1}^{n}\mathbb{1}\{x_i \le x\}$$

```{code-cell} python
import numpy as np
import matplotlib.pyplot as plt

data = np.random.normal(0, 1, 1000)

x = np.sort(data)
y = np.arange(1, len(x) + 1) / len(x)

plt.step(x, y, where="post")
plt.xlabel("Value")
plt.ylabel("ECDF F(x)")
plt.title("Empirical CDF")
plt.grid(True, alpha=0.3)
plt.show()
```

```{tip}
When comparing two distributions, overlay their ECDFs on a single plot. Differences in shape and shift become visually obvious in a way histograms struggle to convey.
```
