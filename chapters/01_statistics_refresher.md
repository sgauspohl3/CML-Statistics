# 1. Statistics Refresher

## Statistics introduction

### Why use statistics?

Statistics is the discipline of **reasoning under uncertainty**. Without it, data is just numbers.

- **Summarize** — describe the sample through descriptive statistics.
- **Identify** — trends, patterns, and relationships in available data.
- **Infer** — make inferences about a population from the sample.
- **Predict** — model and predict future behavior from available data.

### Why understand statistics?

Statistics are powerful and easily misused. Common pitfalls:

- **Susceptible to manipulation** — cherry-picked samples, p-hacking, pre-determined conclusions.
- **Misleading visualizations** — visuals can imply trends that aren't there.
- **Correlation ≠ causation** — variables may appear correlated without any causal relationship.
- **Understand the underlying model** — all models are wrong, but some are useful, and some are more useful than others.

## Responsible statistics

The difference between deceptive and responsible reporting:

| ✗ Deceptive | ✓ Responsible |
|--|--|
| "X scored significantly better than Y" | "Median savings was \$340 (n = 430, 95% CI [\$210, \$470]); 28% of users saw no benefit or net loss." |

Key principles:

- **Ethical and transparent** — share data, code, methods; understand and report biases or incomplete data.
- **Quantify uncertainty** — understand confidence and error in estimates.
- **Measured vs. inferred** — report what is observed vs. what is estimated or assumed.
- **Document assumptions** — distributional assumptions, data cleaning, software versions, random seeds.

## The Rumsfeld matrix

> *Know what you know, and know what you do not know.*

|                 | **Aware** | **Unaware** |
|-----------------|-----------|-------------|
| **Known** | **Known knowns** — we are aware and we understand them. *Ex: observed corrosion of known damage mechanisms.* | **Unknown knowns** — we know what could happen, but have not observed it. *Ex: a damage mechanism we know exists but have not yet detected.* |
| **Unknown** | **Known unknowns** — we are aware, but do not fully understand. *Ex: observed corrosion of an unknown or misattributed damage mechanism.* | **Unknown unknowns** — we are not aware, and we do not have prior knowledge. *Ex: corrosion that is completely unexpected and unobserved.* |

```{important}
**Unknown unknowns are unknowable by definition.** No statistical method can detect or quantify a risk never observed or conceived. The only mitigation is to inspect everything in every way — which is impractical.

The goal of statistical analysis is to **move risks from unknowns to knowns** using prior knowledge and data.
```

## Probability and statistics primer

Four interlocking domains, all built on the foundation of the **sample**:

- **Descriptive statistics** — summarize what's in front of you.
- **Probability** — the language of uncertainty.
- **Inferential statistics** — reason from samples to populations.
- **Predictive statistics** — model future behavior.

## Samples and populations

- **Population** — every member of the group of interest. Usually impractical to measure in full.
- **Sample** — a subset chosen to represent the population; what is actually measured.
- **Variable** — the characteristic recorded for each sample (thickness, height, failure time).

### Notation: parameters vs. statistics

| | Population (parameter) | Sample (statistic) |
|--|--|--|
| Size | $N$ | $n$ |
| Mean | $\mu$ | $\bar{x}$ |
| Variance | $\sigma^2$ | $s^2$ |
| Std deviation | $\sigma$ | $s$ |

## Sampling methods and bias

### Common sampling methods

- **Simple random** — every unit equally likely.
- **Stratified** — sample within strata (lower variance).
- **Cluster** — sample whole groups (cheaper).
- **Systematic** — every $k$-th element.

### Sampling bias

A sample is meant to represent the population, but truly representative samples may not always be possible. **Bias is not always bad**, but be aware of it.

- **Selection bias** — sampling only where you expect to find something. *For CMLs, this is generally desired.*
- **Non-response bias** — those who don't reply differ from those who do.
- **Survivorship bias** — only the survivors are visible in the data.

## Law of Large Numbers

The sample mean → population mean as $n \to \infty$.

$$\bar{X}_n \xrightarrow{p} \mu \;\; \text{as} \;\; n \to \infty$$

More data = more reliable estimates (in expectation).

## Central Limit Theorem

The **sample mean** is approximately Normal — *regardless of the population distribution* — provided the population has finite variance:

$$\bar{X}_n \;\dot\sim\; \mathcal{N}\!\left(\mu, \frac{\sigma^2}{n}\right)$$

This is the foundation for classical inference: z-tests, t-tests, confidence intervals.

```{note}
Read left → right with increasing $n$: at $n=2$ the sampling distribution is still very skewed and the Normal overlay fits poorly. By $n=30$ it is tight, centered on $\mu$, and well-approximated by the Normal.
```

## Descriptive statistics

### Measures of central tendency

- **Mean** — sensitive to outliers. Best for symmetric, unimodal distributions.
- **Median** — robust to outliers. Always at the 50th percentile.
- **Mode** — value(s) with highest frequency. The only summary for categorical data.

### Measures of variability

- **Variance and standard deviation** — average distance from the mean. Most common spread statistic. Sensitive to outliers.
- **Range** — entire spread including outliers. Very sensitive to outliers.
- **Interquartile range (IQR)** — Q3 minus Q1. Robust to outliers.

### Shape of distributions

**Skewness** — distribution asymmetry:

- **Left-skewed** — long left tail; mean < median.
- **Symmetric** — skew ≈ 0; mean ≈ median.
- **Right-skewed** — long right tail; mean > median.

**Kurtosis** — tail weight:

- **Leptokurtic** — heavy tails, sharp peak.
- **Mesokurtic** — normal-like tails.
- **Platykurtic** — light tails, flat peak.

## Plotting data

### Histogram

Bins data into ranges, counts per bin. Reveals at a glance:

- Shape and modality
- Center and spread
- Outliers
- Skew

A histogram is always a great place to begin exploratory data analysis.

```python
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

np.random.seed(42)
data = np.random.normal(loc=50, scale=10, size=500)

sns.histplot(data, kde=True, color='blue', alpha=0.6)
plt.show()
```

```{warning}
**Bin size matters.** Too few bins hides structure; too many adds noise. Try a few before drawing conclusions.
```

### Empirical CDF (ECDF)

Proportion of data ≤ x.

- Every data point is a step.
- No binning decisions.
- Less intuitive shape representation, but ideal for comparing distributions.

```python
import pandas as pd
import numpy as np
import seaborn as sns

np.random.seed(42)
dist1 = np.random.normal(loc=50, scale=10, size=500)
dist2 = np.random.normal(loc=60, scale=15, size=500)

df = pd.DataFrame({
    'value': np.concatenate([dist1, dist2]),
    'distribution': ['Dist 1 (μ=50, σ=10)'] * 500 + ['Dist 2 (μ=60, σ=15)'] * 500
})

sns.ecdfplot(data=df, x='value', hue='distribution', linewidth=2.5)
plt.show()
```

### Probability plots

Check normality (or fit to other distributions) by visually checking linearity.

```python
import numpy as np
import matplotlib.pyplot as plt
import pingouin as pg

np.random.seed(42)
data = np.random.normal(loc=50, scale=10, size=100)

fig, ax = plt.subplots(figsize=(7, 7))
pg.qqplot(data, dist='norm', confidence=0.95, ax=ax)
plt.show()
```

Try different distributions, or cluster the data, if fit is not good.

## Probability

### Core concept

Describes the likelihood of an event occurring. In inspection, it represents the chance that a given thickness value or corrosion rate occurs within the circuit population.

### Frequentist definition

$P(A)$ is the limit of the fraction of outcomes in $A$ over $n$ total outcomes as $n \to \infty$.

### Kolmogorov's three axioms

Probabilities are valid measures of likelihood if they satisfy:

1. Probabilities are bounded between 0 and 1.
2. The sample space has total probability 1.
3. For disjoint events, probabilities add.

### Probability rules

- **Complement:** $P(A^c) = 1 - P(A)$
- **Addition:** $P(A \cup B) = P(A) + P(B) - P(A \cap B)$
- **Multiplication (independent):** $P(A \cap B) = P(A) \cdot P(B)$
- **Conditional:** $P(A \mid B) = P(A \cap B) / P(B)$
- **Law of total probability:** $P(A) = \sum_i P(A \mid B_i) P(B_i)$

## Probability distributions

A **probability distribution** describes the likelihood of different outcomes in a random experiment.

- **Random variable** — a variable whose value is determined by chance.
- **PMF** — probability mass function (discrete distributions): $P(X = x)$.
- **PDF** — probability density function (continuous distributions): density at each value.
- **CDF** — cumulative distribution function: $P(X \le x)$.

### Distribution roadmap

| Variable type | Support | Distributions |
|--|--|--|
| Discrete | Finite | Binomial, Bernoulli |
| Discrete | Infinite | Poisson |
| Continuous | Bounded | Uniform, Beta |
| Continuous | Positive | Gamma, Lognormal, Weibull |
| Continuous | Infinite | Normal, Logistic, Gumbel |

### Discrete: Uniform, Binomial, Bernoulli, Poisson

```{note}
For each distribution: parameters, support, PMF, CDF, mean, variance. Add the formal definitions in production; this wireframe stub keeps the high-level descriptions only.
```

- **Discrete Uniform** — all discrete outcomes equally likely (dice roll). Commonly used as an uninformative prior in Bayesian analysis.
- **Binomial** — number of successes in a fixed number of independent trials. *Example: probability of detection.*
- **Bernoulli** — outcomes of a single experiment. Sum of iid Bernoullis is Binomial.
- **Poisson** — number of events in a fixed interval of time (or other interval).

### Continuous: Uniform, Normal, Half-Normal, Lognormal, Beta, Exponential, Gamma, Weibull

- **Uniform** — all outcomes equally likely on a continuous interval. Common Bayesian uninformative prior.
- **Normal** — symmetric bell curve; other distributions converge to it (CLT).
- **Half-Normal** — folded normal, strictly positive. Common for error measurement.
- **Lognormal** — log of the variable is normal. Positive only. Used for growth.
- **Beta** — flexible, bounded on $[0, 1]$. Conjugate prior for Bernoulli and Binomial.
- **Exponential** — time between events, constant-rate. Memoryless.
- **Gamma** — flexible right-skewed, positive. Generalizes the exponential.
- **Weibull** — most flexible time-to-failure distribution. Shape parameter $k$ determines failure behavior.

## Relationships between distributions

Distributions form a connected web. Key relationships:

- Normal ↔ Beta, Exponential, Half-Normal, Lognormal
- Bernoulli → Binomial → Poisson
- Exponential → Gamma → Weibull → Gumbel
- Normal → Cauchy, Student's t, Chi-Squared

Transforms, sums/convolutions, limits, and special cases all link these. Transformed distributions may be used as **conjugate priors** for Bayesian analysis, and related distributions can aid in fitting.

## Choosing the right distribution

Selecting the correct distribution dictates the performance of inferences and predictions. Consider:

- **Data type** — discrete vs. continuous.
- **Support / range** — $[0,1]$ (Beta), $[0, \infty)$ (Exp/Lognormal/Gamma), $(-\infty, \infty)$ (Normal).
- **Shape** — symmetric (Normal), right-skewed (Lognormal/Exp), U-shaped (Beta with $\alpha, \beta < 1$).
- **Measurement generation** — counts (Poisson/Binomial), times (Exp/Gamma), growth (Lognormal).

| Scenario | Distribution |
|--|--|
| Counts in fixed trials | Binomial |
| Counts over time/space | Poisson |
| Time between events | Exponential |
| Positive, right-skewed measurements | Lognormal |
| Symmetric measurements | Normal |
| Proportions/probabilities | Beta |

## Fitting distributions

### Method of Moments (MoM)

Express the distribution moments as functions and solve using sample moments.

- Not always practical or analytically possible.
- Quick and computationally simple.
- Generally the poorest estimator.
- Good as an **initial estimate** for MLE.

### Least Squares Estimation (LSE)

Linearize the distribution equation and use least squares to find parameters of the line of best fit.

1. **Transform** the data (e.g., Bernard's approximation for $F$, with $a = 0.3$).
2. **Perform regression** on the linearized form.
3. **Solve** for the original parameters from the regression coefficients.

### Maximum Likelihood Estimation (MLE)

Choose the parameters that make the observed data most probable under the assumed distribution.

- Asymptotically efficient.
- Workhorse for most modern statistical models.

## Goodness of fit

Compare an empirical distribution against the theoretical one. P-P and Q-Q plots emphasize different parts:

| | P-P Plot | Q-Q Plot |
|--|--|--|
| **Compares** | Empirical CDF vs. theoretical CDF | Empirical quantiles vs. theoretical quantiles |
| **Emphasizes** | Center of the distribution | Tails — extreme values, outliers |
| **Use for** | Detecting overall shape mismatch, location/scale shifts | Detecting tail behavior |

### Statistical tests

Tests give a p-value for whether the fit is acceptable. $H_0$: data was drawn from the candidate distribution. Large test statistic → reject $H_0$ → fit is poor.

- **Kolmogorov–Smirnov (KS)** — sensitive to the center.
- **Anderson–Darling (AD)** — weighted KS; extra weight to the tails.

### Information criteria

Rank competing distributions on the same data. Reward fit, penalize complexity. **Lower is better.**

$$\text{AIC} = 2k - 2\ln(\hat{L})$$
$$\text{BIC} = k\ln(n) - 2\ln(\hat{L})$$

$k$ = parameters, $n$ = sample size, $\hat{L}$ = maximum likelihood. BIC penalizes complexity more heavily as $n$ grows.

## Confidence intervals

A 95% CI means: if we repeated the procedure many times, ~95% of the intervals would contain the true $\mu$.

| Method | Strengths | Weakness |
|--|--|--|
| **Standard error (t)** | Fast, simple; uses Student's t with $n-1$ df. | Assumes symmetric, normal-shaped likelihood. Poor for small $n$ or skewed parameters. |
| **Wald** | Fast; needs only MLE and its standard error. | Same as standard error. |
| **Profile likelihood** | Honors actual shape of the likelihood; reliable for small $n$, skewed/bounded parameters. | More computation — evaluate likelihood across a grid. |
| **Bootstrap** | Distribution-free; works for any estimator. | Computationally heavy; quality depends on sample representativeness. |

```python
# Bootstrap example
B = 10000
boot_means = [rng.choice(data, size=len(data), replace=True).mean()
              for _ in range(B)]
lo, hi = np.percentile(boot_means, [2.5, 97.5])
```

## Hypothesis testing

The classical framework:

1. **State $H_0$ and $H_1$** — null (status quo) and alternative.
2. **Choose test statistic** — with a known distribution under $H_0$.
3. **Compute p-value** — $P(\text{data this extreme} \mid H_0 \text{ true})$.
4. **Compare to $\alpha$** — typically 0.05.
5. **Reject or fail to reject** — never "accept" $H_0$.

### Common tests

- **One-sample t-test** — is the mean a target value?
- **Two-sample t-test** — do two group means differ?
- **Paired t-test** — before/after on same units.
- **Chi-squared** — categorical associations.

### What p does NOT tell you

Common misreadings:

- ✗ "p = 0.03 means 3% chance $H_0$ is true."
- ✗ "p > 0.05 means there's no effect."
- ✗ "A smaller p means a bigger effect."
- ✗ "p = 0.049 and p = 0.051 are categorically different."

## On the p-value and error estimation

|                        | $H_0$ true | $H_0$ false |
|------------------------|------------|-------------|
| **Reject $H_0$** | Type I error ($\alpha$) | Correct (power = $1-\beta$) |
| **Fail to reject** | Correct | Type II error ($\beta$) |

- **Type I (false positive)** — claim an effect that isn't real. Controlled by $\alpha$.
- **Type II (false negative)** — miss a real effect. Aim for power $1 - \beta \ge 0.80$.

### What you actually want vs. what p gives you

- **What p gives you:** $P(\text{significant} \mid H_0 \text{ true})$
- **What you actually want:** $P(H_0 \text{ true} \mid \text{significant})$

This gap is one of the main reasons Bayesian methods are worth knowing.

## Censored and truncated data

### Censoring

Value is bounded but not exact.

- **Right-censored:** $X > c$ (subject still "alive" at study end).
- **Left-censored:** $X < c$ (below detection limit).
- **Interval-censored:** $a < X < b$.

### Truncation

Observations outside a range are **completely missing** — e.g. eliminating thickness readings that show growth.

```{important}
The key difference: **censored data contributes partial information; truncated data is missing entirely.** Ignoring either produces biased estimates.
```
