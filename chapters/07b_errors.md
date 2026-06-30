# Type I and Type II Errors

Hypothesis tests can fail in two ways.

## The error table

|                        | $H_0$ true                  | $H_0$ false                  |
|------------------------|-----------------------------|------------------------------|
| **Reject $H_0$**       | Type I error ($\alpha$)     | Correct (power = $1-\beta$)  |
| **Fail to reject $H_0$** | Correct                   | Type II error ($\beta$)      |

**Type I (false positive)** — claim an effect that isn't real. Controlled by $\alpha$ (typically 0.05).

**Type II (false negative)** — miss a real effect. Controlled by $\beta$; **power** $= 1 - \beta$ (typically aim for 0.80).

## The tradeoff

Lowering $\alpha$ raises $\beta$, all else equal. The only way to reduce *both* error rates is to increase **sample size**.

```{code-cell} python
from statsmodels.stats.power import TTestIndPower

analysis = TTestIndPower()
n = analysis.solve_power(effect_size=0.5, alpha=0.05, power=0.8)
print(f"Required sample size per group: {n:.0f}")
```

A **power analysis** before collecting data tells you how many observations you'll need to reliably detect an effect of a given size. Skipping this step is one of the most common (and expensive) mistakes in applied research.
