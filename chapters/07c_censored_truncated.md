# Censored and Truncated Data

In the real world, data is often incomplete. Two important kinds of incompleteness:

## Censoring

The value of an observation is **not known precisely**, but is known to fall within some range.

- **Right-censored:** we know $X > c$ but not the exact value. *Example:* a patient is still alive when the study ends.
- **Left-censored:** we know $X < c$. *Example:* a measurement below the instrument's detection limit.
- **Interval-censored:** we know $a < X < b$.

## Truncation

Observations outside a range are **completely missing** — we don't even know they exist.

- **Right-truncated:** subjects with $X > c$ never enter the sample.
- **Left-truncated:** subjects with $X < c$ never enter. *Example:* a study of retirement age can only include people who lived long enough to retire.

```{important}
The key difference: **censored data contributes partial information; truncated data is missing entirely.**
```

## Impact and proper methods

**Ignoring censoring → biased estimates.** Computing mean lifetime on right-censored data underestimates the true mean — we treat survivors as if they had already failed.

**Ignoring truncation → biased estimates.** The sample is unrepresentative of the population.

**Proper methods:**

- **Survival analysis** — Kaplan–Meier estimator, Cox proportional hazards.
- **Tobit regression** — for censored continuous outcomes.
- **Maximum likelihood with censoring contributions** — likelihood includes $P(X > c)$ terms for censored points.
- **Truncated distributions** — adjust the PDF so it integrates to 1 over the observed range.

```{code-cell} python
# Kaplan-Meier for right-censored data
from lifelines import KaplanMeierFitter
import numpy as np

durations = np.array([5, 6, 6, 2.5, 4, 4, 9, 10])
event_observed = np.array([1, 0, 1, 1, 1, 0, 1, 0])   # 0 = censored

kmf = KaplanMeierFitter()
kmf.fit(durations, event_observed)
print(kmf.median_survival_time_)
```
