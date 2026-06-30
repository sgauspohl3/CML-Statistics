# LLN and CLT

Two theorems are the foundation of nearly all classical inference.

## Law of Large Numbers

As sample size $n \to \infty$, the sample mean **converges to** the population mean:

$$\bar{X}_n \xrightarrow{p} \mu \;\; \text{as} \;\; n \to \infty$$

More data → more reliable estimates, in expectation.

```{warning}
LLN doesn't say small samples are unbiased — only that bias and variance shrink as $n$ grows. With a small $n$, anything can happen.
```

```{code-cell} python
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)
rolls = np.random.randint(1, 7, size=10_000)
running_mean = np.cumsum(rolls) / np.arange(1, len(rolls) + 1)

plt.plot(running_mean)
plt.axhline(3.5, color="red", linestyle="--", label="True mean = 3.5")
plt.xscale("log")
plt.xlabel("Number of rolls")
plt.ylabel("Running mean")
plt.legend()
plt.show()
```

## Central Limit Theorem

The distribution of the **sample mean** approaches normal as $n$ grows, *regardless of the underlying distribution* (provided variance is finite):

$$\bar{X}_n \;\dot\sim\; \mathcal{N}\!\left(\mu, \frac{\sigma^2}{n}\right)$$

This is the foundation for z-tests, t-tests, and most analytical confidence intervals.

**Rule of thumb:** $n \ge 30$ is often "large enough," but heavily skewed distributions may need more.

```{code-cell} python
import numpy as np
import matplotlib.pyplot as plt

# Underlying distribution is very skewed (exponential),
# but the sampling distribution of the mean looks normal.
means = [np.random.exponential(scale=2, size=50).mean() for _ in range(10_000)]

plt.hist(means, bins=50, edgecolor="black", alpha=0.7)
plt.title("Sampling distribution of the mean (n=50) — looks Normal")
plt.show()
```

```{important}
The CLT is *not* a statement about the data — it's a statement about the **sample mean**. Your raw data can be wildly non-normal; the means of repeated samples will still tend toward normality.
```
