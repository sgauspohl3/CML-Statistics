# ANOVA

**Analysis of Variance** compares means across **three or more groups** in a single test, avoiding the inflated error rate that comes from running many pairwise t-tests.

## The idea

ANOVA asks: is the variability *between groups* large relative to variability *within groups*?

Test statistic:

$$F = \frac{\text{MS}_{\text{between}}}{\text{MS}_{\text{within}}}$$

Under $H_0$ (all group means equal), $F$ follows an F-distribution. Large $F$ → reject.

## Post-hoc tests

A significant ANOVA tells you *some* group differs from others, but not *which*. To find that out, follow up with post-hoc tests like **Tukey's HSD**, which controls the family-wise error rate across all pairwise comparisons.

```{code-cell} python
from scipy import stats
import numpy as np

A = np.random.normal(10, 2, 30)
B = np.random.normal(11, 2, 30)
C = np.random.normal(13, 2, 30)

f_stat, p_val = stats.f_oneway(A, B, C)
print(f"F = {f_stat:.3f}, p = {p_val:.4f}")
```
