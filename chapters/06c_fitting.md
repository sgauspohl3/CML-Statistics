# Fitting Distributions

Three classic ways to fit a distribution's parameters to data.

## Method of Moments (MoM)

Match **sample moments** to **theoretical moments** and solve for parameters. Simple, not always efficient.

For a Normal: $\hat\mu = \bar{x}$, $\hat\sigma^2 = s^2$.

For Gamma($k, \theta$): mean = $k\theta$, variance = $k\theta^2$, so

$$\hat\theta = s^2 / \bar{x}, \qquad \hat{k} = \bar{x} / \hat\theta$$

```{code-cell} python
import numpy as np

data = np.random.gamma(shape=3, scale=2, size=10_000)

xbar, s2 = data.mean(), data.var(ddof=1)
theta_hat = s2 / xbar
k_hat     = xbar / theta_hat

print(f"MoM estimates: k = {k_hat:.2f}, theta = {theta_hat:.2f}  (true: 3, 2)")
```

## Least Squares Estimation (LSE)

Choose parameters to **minimize the sum of squared residuals** between observed and predicted values:

$$\hat\theta = \arg\min_\theta \sum_{i=1}^{n} \bigl(y_i - f(x_i; \theta)\bigr)^2$$

Standard for regression and curve fitting. For linear regression with normal errors, **LSE = MLE**.

```{code-cell} python
import numpy as np
from scipy.optimize import curve_fit

x = np.linspace(0, 10, 100)
y = 2.5 * np.exp(-0.3 * x) + np.random.normal(0, 0.1, 100)

def model(x, a, b):
    return a * np.exp(-b * x)

params, _ = curve_fit(model, x, y)
print(f"a = {params[0]:.3f}, b = {params[1]:.3f}")
```

## Maximum Likelihood Estimation (MLE)

Choose parameters that **maximize the likelihood** of the observed data:

$$\hat\theta_{\text{MLE}} = \arg\max_\theta \prod_{i=1}^{n} f(x_i;\theta) = \arg\max_\theta \sum_{i=1}^{n}\log f(x_i;\theta)$$

MLE is **asymptotically efficient** — for large $n$, no unbiased estimator has lower variance. It's the workhorse of modern statistics.

```{code-cell} python
from scipy import stats
import numpy as np

data = np.random.normal(loc=5, scale=2, size=1000)

# scipy's .fit uses MLE
mu_hat, sigma_hat = stats.norm.fit(data)
print(f"MLE: mu = {mu_hat:.2f}, sigma = {sigma_hat:.2f}")
```
