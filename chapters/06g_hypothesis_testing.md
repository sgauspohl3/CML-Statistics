# Hypothesis Testing

The classical machinery for asking: "is this effect real, or could it have happened by chance?"

## The framework

1. State the **null hypothesis** $H_0$ (status quo) and the **alternative** $H_1$.
2. Choose a **test statistic** with a known distribution under $H_0$.
3. Compute the **p-value**: probability of seeing data this extreme *if $H_0$ were true*.
4. Compare to significance level $\alpha$ (commonly 0.05).
5. **Reject $H_0$** if $p < \alpha$, else **fail to reject**.

```{important}
We never "accept" the null. We either reject it or fail to reject it. Absence of evidence is not evidence of absence.
```

## Common tests

- **One-sample t-test** — is the mean equal to some value?
- **Two-sample t-test** — are two group means different?
- **Paired t-test** — before/after on the same units.
- **Chi-squared** — categorical associations.
- **z-test** — proportions, or means with known variance.

```{code-cell} python
from scipy import stats
import numpy as np

group_A = np.random.normal(100, 15, 50)
group_B = np.random.normal(105, 15, 50)

t_stat, p_val = stats.ttest_ind(group_A, group_B)
print(f"t = {t_stat:.3f}, p = {p_val:.4f}")
```

The p-value, despite its ubiquity, is one of the most misunderstood quantities in statistics. We'll devote a full chapter to it in the next part.
