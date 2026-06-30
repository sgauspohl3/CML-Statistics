# Responsible Statistics

Good statistical practice is as much about discipline as it is about technique.

## Be ethical and transparent

- Share data, code, and methods so others can reproduce your work.
- Disclose conflicts of interest and funding sources.
- Don't selectively report results that favor a hypothesis.

## Separate what you measured from what you inferred

Be explicit about which numbers came from observation and which came from estimation:

- **Measured** — data points, raw counts, direct observations.
- **Inferred** — parameters, predictions, confidence intervals.

## Quantify and report uncertainty

A point estimate alone (e.g., "mean = 5.2") is incomplete. Always pair estimates with uncertainty: confidence intervals, standard errors, or full posterior distributions.

## Document assumptions, inputs, and methods

Reproducibility starts with documenting:

- Distributional assumptions (e.g., "we assumed normality")
- Data cleaning decisions (outliers, missing values)
- Software, versions, random seeds

```{code-cell} python
import numpy as np
from scipy import stats

# Bad:  "the average is 5.2"
# Good: report estimate + uncertainty + sample size + method

data = np.random.normal(5, 2, 50)
mean = data.mean()
sem  = stats.sem(data)
ci   = stats.t.interval(0.95, len(data)-1, loc=mean, scale=sem)

print(f"Mean = {mean:.2f}, 95% CI = [{ci[0]:.2f}, {ci[1]:.2f}], n = {len(data)}")
```
