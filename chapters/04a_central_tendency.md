# Central Tendency

The "typical" value of a dataset can be defined in several ways, each appropriate in different settings.

## The three measures

**Mean** (arithmetic average) — sensitive to outliers.

$$\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i$$

**Median** — middle value when data is sorted; robust to outliers.

**Mode** — most frequent value; useful for categorical or discrete data.

## When to use which

- **Symmetric data** → mean is fine.
- **Skewed data** (income, house prices) → median is more representative.
- **Categorical data** → mode.

```{code-cell} python
import numpy as np
from scipy import stats

data = [2, 4, 4, 4, 5, 5, 7, 9, 100]   # contains an outlier

print(f"Mean:   {np.mean(data):.2f}")        # 15.56 — pulled by 100
print(f"Median: {np.median(data):.2f}")      # 5.00 — robust
print(f"Mode:   {stats.mode(data, keepdims=False).mode}")  # 4
```

Notice how the single outlier (100) pulls the mean up by a factor of three, while the median is unaffected. This is why median income is a more honest summary than mean income.
