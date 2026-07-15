# Statistics Refresher

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

```{image} ../images/rumsfeld.png
:alt: Rumsfeld Matrix
:width: 600px
:align: center
```


```{important}
**Unknown unknowns are unknowable by definition.** No statistical method can detect or quantify a risk never observed or conceived. The only mitigation is to inspect everything in every way — which is impractical.

The goal of statistical analysis is to **move risks from unknowns to knowns** using prior knowledge and data.
```
If you want to know how many whales are in the ocean (population), and you decide to figure this out by sampling with a bucket, you might shockingly discover that there are no whales in the ocean (if you trust your sampling). You have absence of evidence. Obviously, this is an extreme example, and you know that whales exist in the ocean. You have an unknown known; something you have not observed, but know is possible. This is also a demonstration of poor measurement or sampling technique as it would be impossible to fit even a baby whale in a bucket (how big is the biggest bucket?). Real sampling for population of whales is actually challenging with a combination of aerial sightings, acoustic surveys, and physical counting and marking. The absence of evidence is not evidence of absence.

## Samples and populations

- **Population** — every member of the group of interest. Usually impractical to measure in full.
- **Sample** — a subset chosen to represent the population; what is actually measured.
- **Variable** — the characteristic recorded for each sample (thickness, height, failure time).

```{image} ../images/population2.png
:alt: Population, Variable, and Sample
:width: 700px
:align: center
```

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

```{image} ../images/lln.png
:alt: Law of large numbers
:width: 600px
:align: center
```

## Central Limit Theorem

The **sample mean** is approximately Normal — *regardless of the population distribution* — provided the population has finite variance:

$$\bar{X}_n \;\dot\sim\; \mathcal{N}\!\left(\mu, \frac{\sigma^2}{n}\right)$$

This is the foundation for classical inference: z-tests, t-tests, confidence intervals.

```{image} ../images/clt.png
:alt: CLT — sampling distribution of the mean
:width: 700px
:align: center
```

Read left → right with increasing $n$: at $n=2$ the sampling distribution of the mean is still very skewed and a Normal overlay fits poorly. By $n=50$ it is tight, centered on $\mu$, and well-approximated by the Normal — even though the underlying distribution (Exponential) is heavily skewed.

```{raw} html
<iframe src="../_static/clt_exponential_demo.html"
        width="100%" height="850"
        style="border:1px solid #ddd; border-radius:8px;">
</iframe>
```

```{important}
The CLT is *not* a statement about the data — it's a statement about the **sample mean**. Your raw data can be wildly non-normal; the means of repeated samples will still tend toward normality.
```

## Descriptive statistics

### Measures of central tendency

- **Mean** — sensitive to outliers. Best for symmetric, unimodal distributions.
- **Median** — robust to outliers. Always at the 50th percentile.
- **Mode** — value(s) with highest frequency. The only summary for categorical data.

```{image} ../images/central_tendency.png
:alt: Central tendency on a skewed sample
:width: 500px
:align: center
```

On a skewed sample, the three measures separate. The mean is pulled by the long right tail, while the median sits at the 50th percentile regardless. The mode is the most common value.

### Measures of variability

- **Variance and standard deviation** — average distance from the mean. Most common spread statistic. Sensitive to outliers.
- **Range** — entire spread including outliers. Very sensitive to outliers.
- **Interquartile range (IQR)** — Q3 minus Q1. Robust to outliers.

For a sample with $n$ observations:

$$s^2 = \frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar{x})^2 \qquad s = \sqrt{s^2}$$

The denominator $n-1$ (rather than $n$) is **Bessel's correction**, which produces an unbiased estimator of the population variance.

```{image} ../images/variability.png
:alt: Variability comparison
:width: 600px
:align: center
```

Two distributions with the same mean but different spread. The wider $\sigma=12$ distribution has the same center but covers much more ground — the boxplot underneath shows the contrast in IQR clearly.

### Coefficient of variation (CV)

Standard deviation in absolute units depends on the scale of the variable. To compare spread across variables on different scales, normalize:

$$\text{CV} = \frac{s}{\bar{x}}$$

CV is unitless, often reported as a percentage. It's particularly useful in inspection work where pipe thickness varies by component size — a $\pm$ 0.030" variation is a different fraction of nominal for a 4" SCH40 pipe than for a 24" SCH80.

```{note}
**Rule of thumb in CML work:** A CV < 10% within a TML is generally acceptable. Higher CV suggests localized corrosion, measurement issues, or improper grouping.
```

### Shape: skewness

Skewness measures **asymmetry**:

$$g_1 = \frac{1}{n}\sum_{i=1}^{n}\left(\frac{x_i - \bar{x}}{s}\right)^3$$

- **Left-skewed** (negative skew) — long left tail; **mean < median**. Example: age at death.
- **Symmetric** — skew ≈ 0; mean ≈ median. Example: heights.
- **Right-skewed** (positive skew) — long right tail; **mean > median**. Example: incomes, corrosion rates.

```{image} ../images/skew.png
:alt: Skew of distributions
:width: 650px
:align: center
```

Note where the mean (dashed line) sits relative to the median (solid line) in each case. The position of mean relative to median is a quick visual check for skew direction.

### Shape: kurtosis

Kurtosis measures **tail weight** — how often extreme values appear:

$$g_2 = \frac{1}{n}\sum_{i=1}^{n}\left(\frac{x_i - \bar{x}}{s}\right)^4 - 3$$

- **Leptokurtic** — heavy tails, sharp peak. Example: financial returns, t-distribution with low df.
- **Mesokurtic** — normal-like tails. Example: many natural phenomena.
- **Platykurtic** — light tails, flat peak. Example: uniform distribution.

```{image} ../images/kurtosis.png
:alt: Kurtosis of distributions
:width: 650px
:align: center
```

Heavy-tailed distributions produce extreme outliers far more often than a Normal would predict. This matters in reliability work — a thickness reading 5σ below the fitted mean is almost impossible under a Normal model, but could be a one-in-a-thousand event under a t-distribution.

## Expectation, variance, and moments

For a random variable $X$, the **expectation** (mean) is

$$E[X] = \sum_x x \, p(x) \quad \text{(discrete)} \qquad E[X] = \int x \, f(x)\, dx \quad \text{(continuous)}$$

The **variance** is

$$\text{Var}(X) = E[(X - E[X])^2] = E[X^2] - E[X]^2$$

These are the **first two moments** of the distribution. Higher moments give skew (3rd) and kurtosis (4th).

### Linearity of expectation

For any constants $a, b$ and random variables $X, Y$:

$$E[aX + bY] = a\,E[X] + b\,E[Y]$$

Linearity holds **whether or not $X$ and $Y$ are independent** — this is what makes expectations easy to work with. Variance, in contrast, is not linear:

$$\text{Var}(aX + bY) = a^2\,\text{Var}(X) + b^2\,\text{Var}(Y) + 2ab\,\text{Cov}(X, Y)$$

If $X$ and $Y$ are independent, $\text{Cov}(X, Y) = 0$ and the cross-term vanishes.

## Independence and covariance

Two random variables $X$ and $Y$ are **independent** if knowing one tells you nothing about the other:

$$p(X, Y) = p(X) \cdot p(Y)$$

**Covariance** measures the direction of joint variation:

$$\text{Cov}(X, Y) = E[(X - E[X])(Y - E[Y])]$$

**Correlation** is the unitless version, scaled to $[-1, 1]$:

$$\rho_{X,Y} = \frac{\text{Cov}(X, Y)}{\sigma_X \sigma_Y}$$

```{warning}
**Independence implies zero correlation, but zero correlation does NOT imply independence.** Correlation only captures linear relationships. Two variables can be perfectly dependent but uncorrelated (e.g., $Y = X^2$ when $X$ is symmetric around zero).
```

Independence matters for inspection data because most statistical methods assume observations are independent. CML readings on the same circuit are often *not* independent — they share environment, material, and operating history. This is one of the motivations for the hierarchical Bayesian models in chapter 4.

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

```{image} ../images/bin_count.png
:alt: Effect of bin count
:width: 800px
:align: center
```

### Empirical CDF (ECDF)

Proportion of data ≤ x.

- Every data point is a step.
- No binning decisions.
- Less intuitive shape representation, but ideal for comparing distributions.

```python
import seaborn as sns
sns.ecdfplot(data, color='steelblue', linewidth=2.5)
```

```{image} ../images/ecdf.png
:alt: Empirical CDF
:width: 600px
:align: center
```

The horizontal lines at 25%, 50%, and 75% make it easy to read off the quartiles directly from the plot. To compare two distributions, overlay their ECDFs:

```{image} ../images/ecdf_compare.png
:alt: ECDF comparison
:width: 600px
:align: center
```

Differences in shape, shift, and spread all show up in one view.

### Probability plots

Check normality (or fit to other distributions) by visually checking linearity.

```python
import pingouin as pg
pg.qqplot(data, dist='norm', confidence=0.95)
```

```{image} ../images/qq_norm.png
:alt: Normal probability plot
:width: 500px
:align: center
```

A good fit produces a straight line along the diagonal. Systematic curvature suggests the candidate distribution doesn't match — try a different one, or look for sub-populations that should be clustered separately.

## Probability

### Core concept

Probability describes the likelihood of an event occurring. In inspection, it represents the chance that a given thickness value or corrosion rate occurs within the circuit population.

### Frequentist definition

$P(A)$ is the limit of the fraction of outcomes in $A$ over $n$ total outcomes as $n \to \infty$. *Long-run frequency interpretation.*

### Kolmogorov's three axioms

Probabilities are valid measures of likelihood if they satisfy:

1. $P(A) \ge 0$ for any event $A$.
2. $P(\Omega) = 1$ — something must happen.
3. For disjoint events: $P(A \cup B) = P(A) + P(B)$.

### Probability rules

- **Complement:** $P(A^c) = 1 - P(A)$
- **Addition:** $P(A \cup B) = P(A) + P(B) - P(A \cap B)$
- **Multiplication (independent):** $P(A \cap B) = P(A) \cdot P(B)$
- **Conditional:** $P(A \mid B) = P(A \cap B) / P(B)$
- **Law of total probability:** $P(A) = \sum_i P(A \mid B_i) P(B_i)$

### Bayes' theorem

The single most important formula in modern statistics:

$$P(A \mid B) = \frac{P(B \mid A)\,P(A)}{P(B)}$$

It tells you how to *update* your belief about $A$ after observing $B$. The prior $P(A)$ becomes the posterior $P(A \mid B)$, mediated by the likelihood $P(B \mid A)$.

#### A worked example: medical testing

Suppose a disease affects 1 in 1,000 people. A diagnostic test has:

- 99% sensitivity: $P(\text{positive} \mid \text{disease}) = 0.99$
- 95% specificity: $P(\text{negative} \mid \text{no disease}) = 0.95$, so $P(\text{positive} \mid \text{no disease}) = 0.05$

A patient tests positive. What's the probability they have the disease?

Apply Bayes' theorem:

$$P(\text{disease} \mid +) = \frac{P(+ \mid \text{disease}) \, P(\text{disease})}{P(+)}$$

The numerator is straightforward: $0.99 \times 0.001 = 0.00099$.

The denominator uses the law of total probability:

$$P(+) = P(+ \mid \text{D}) P(\text{D}) + P(+ \mid \text{no D}) P(\text{no D}) = 0.99 \times 0.001 + 0.05 \times 0.999 = 0.05094$$

So:

$$P(\text{disease} \mid +) = \frac{0.00099}{0.05094} \approx 0.019 \approx 2\%$$

**Despite a positive result from a 99%-sensitive test, the probability the patient is actually sick is only about 2%.** The low base rate (1 in 1,000) dominates the calculation. This is the **base rate fallacy**, and it's the most common error people make in interpreting test results.

The same logic applies to inspection: a single low thickness reading at a randomly chosen CML doesn't tell you much if your prior belief is that most of the circuit is fine. You need to update on the base rate of corroding CMLs, not just the reading itself.

## Probability distributions

A **probability distribution** describes the likelihood of different outcomes in a random experiment.

- **Random variable** — a variable whose value is determined by chance.
- **PMF** — probability mass function (discrete distributions): $P(X = x)$.
- **PDF** — probability density function (continuous distributions): density at each value.
- **CDF** — cumulative distribution function: $P(X \le x)$.

### Distribution roadmap

| Variable type | Support | Distributions |
|--|--|--|
| Discrete | Finite | Uniform, Binomial, Bernoulli |
| Discrete | Infinite | Poisson |
| Continuous | Bounded | Uniform, Beta |
| Continuous | Positive | Half-Normal, Lognormal, Exponential, Gamma, Weibull |
| Continuous | Infinite | Normal, Logistic |

The rest of this chapter walks through each in turn.

```{image} ../images/distribution-summary.png
:alt: Distributions
:width: 700px
:align: center
```

## Discrete distributions

### Discrete Uniform

All discrete outcomes equally likely. Used as an uninformative prior in Bayesian work.

| | |
|--|--|
| **Parameters** | $a$ (lower), $b$ (upper), both integers |
| **Support** | $x \in \{a, a+1, \ldots, b\}$ |
| **PMF** | $P(X = x) = \dfrac{1}{b - a + 1}$ |
| **CDF** | $F(x) = \dfrac{\lfloor x \rfloor - a + 1}{b - a + 1}$ |
| **Mean** | $\dfrac{a + b}{2}$ |
| **Variance** | $\dfrac{(b - a + 1)^2 - 1}{12}$ |

*Example: rolling a fair die — $a = 1$, $b = 6$.*

```{image} ../images/dist_uniform_discrete.png
:alt: Discrete uniform distribution
:width: 500px
:align: center
```

### Bernoulli

The outcomes of a **single trial** with two outcomes (success/failure). The atom from which the Binomial is built.

| | |
|--|--|
| **Parameters** | $p \in [0, 1]$ |
| **Support** | $x \in \{0, 1\}$ |
| **PMF** | $P(X = x) = p^x (1-p)^{1-x}$ |
| **CDF** | $F(x) = \begin{cases} 0 & x < 0 \\ 1-p & 0 \le x < 1 \\ 1 & x \ge 1 \end{cases}$ |
| **Mean** | $p$ |
| **Variance** | $p(1-p)$ |

*Example: a single inspection POD trial — pit detected or not detected.*

```{image} ../images/dist_bernoulli.png
:alt: Bernoulli distribution
:width: 500px
:align: center
```

### Binomial

Number of successes in $n$ independent Bernoulli trials.

| | |
|--|--|
| **Parameters** | $n$ (trials), $p \in [0, 1]$ (success probability) |
| **Support** | $x \in \{0, 1, \ldots, n\}$ |
| **PMF** | $P(X = x) = \binom{n}{x} p^x (1-p)^{n-x}$ |
| **Mean** | $np$ |
| **Variance** | $np(1-p)$ |

*Example: defective fittings in a batch of 100, where each has a 2% defect rate.*

```{image} ../images/dist_binomial.png
:alt: Binomial distribution
:width: 600px
:align: center
```

### Poisson

Number of events in a fixed interval, given a constant average rate. Limit of Binomial as $n \to \infty$, $p \to 0$, with $np = \lambda$ fixed.

| | |
|--|--|
| **Parameters** | $\lambda > 0$ (mean rate) |
| **Support** | $x \in \{0, 1, 2, \ldots\}$ |
| **PMF** | $P(X = x) = \dfrac{\lambda^x e^{-\lambda}}{x!}$ |
| **Mean** | $\lambda$ |
| **Variance** | $\lambda$ |

The fact that mean equals variance is the distinctive Poisson property — useful for sanity-checking whether count data is actually Poisson.

*Example: equipment failures per year, leaks per mile of pipe, defects per unit area.*

```{image} ../images/dist_poisson.png
:alt: Poisson distribution
:width: 600px
:align: center
```

## Continuous distributions

### Continuous Uniform

All values in $[a, b]$ equally likely.

| | |
|--|--|
| **Parameters** | $a < b$ (real) |
| **Support** | $x \in [a, b]$ |
| **PDF** | $f(x) = \dfrac{1}{b - a}$ |
| **CDF** | $F(x) = \dfrac{x - a}{b - a}$ |
| **Mean** | $\dfrac{a + b}{2}$ |
| **Variance** | $\dfrac{(b - a)^2}{12}$ |

*Example: noise injected uniformly in a range; "no prior information" Bayesian prior.*

```{image} ../images/dist_uniform_continuous.png
:alt: Continuous uniform distribution
:width: 600px
:align: center
```

### Normal

The bell curve — appears wherever many small effects add up (Central Limit Theorem).

| | |
|--|--|
| **Parameters** | $\mu$ (mean), $\sigma > 0$ (std) |
| **Support** | $x \in (-\infty, \infty)$ |
| **PDF** | $f(x) = \dfrac{1}{\sigma\sqrt{2\pi}}\exp\!\left(-\dfrac{(x-\mu)^2}{2\sigma^2}\right)$ |
| **Mean** | $\mu$ |
| **Variance** | $\sigma^2$ |

68–95–99.7 rule: ~68% of the mass within $\pm1\sigma$, ~95% within $\pm 2\sigma$, ~99.7% within $\pm 3\sigma$.

*Example: measurement errors, heights, sums of many small random effects.*

```{image} ../images/dist_normal.png
:alt: Normal distribution
:width: 650px
:align: center
```

### Half-Normal

Folded Normal — absolute value of a zero-centered Normal. Strictly positive.

| | |
|--|--|
| **Parameters** | $\sigma > 0$ |
| **Support** | $x \in [0, \infty)$ |
| **PDF** | $f(x) = \dfrac{\sqrt{2}}{\sigma\sqrt{\pi}}\exp\!\left(-\dfrac{x^2}{2\sigma^2}\right)$ |
| **Mean** | $\sigma\sqrt{2/\pi}$ |
| **Variance** | $\sigma^2(1 - 2/\pi)$ |

*Example: measurement error magnitudes, scale parameters in Bayesian models.*

```{image} ../images/dist_halfnormal.png
:alt: Half-Normal distribution
:width: 650px
:align: center
```

### Log-Normal

$\log X$ is Normal. Strictly positive, right-skewed.

| | |
|--|--|
| **Parameters** | $\mu$, $\sigma > 0$ (of the log) |
| **Support** | $x \in (0, \infty)$ |
| **PDF** | $f(x) = \dfrac{1}{x\sigma\sqrt{2\pi}}\exp\!\left(-\dfrac{(\ln x - \mu)^2}{2\sigma^2}\right)$ |
| **Mean** | $\exp\!\left(\mu + \sigma^2/2\right)$ |
| **Variance** | $\left[\exp(\sigma^2) - 1\right] \exp(2\mu + \sigma^2)$ |

*Example: rainfall amounts, financial returns, biological growth.*

```{image} ../images/dist_lognormal.png
:alt: Log-Normal distribution
:width: 650px
:align: center
```

### Beta

Flexible distribution on $[0, 1]$. The **conjugate prior** for the Bernoulli and Binomial — see chapter 4.

| | |
|--|--|
| **Parameters** | $\alpha > 0$, $\beta > 0$ |
| **Support** | $x \in [0, 1]$ |
| **PDF** | $f(x) = \dfrac{x^{\alpha-1}(1-x)^{\beta-1}}{B(\alpha, \beta)}$ |
| **Mean** | $\dfrac{\alpha}{\alpha + \beta}$ |
| **Variance** | $\dfrac{\alpha\beta}{(\alpha+\beta)^2(\alpha+\beta+1)}$ |

where $B(\alpha, \beta) = \frac{\Gamma(\alpha)\Gamma(\beta)}{\Gamma(\alpha + \beta)}$ is the beta function.

Shape changes dramatically with parameters: $\alpha = \beta = 1$ is uniform, $\alpha = \beta > 1$ is bell-shaped, $\alpha = \beta < 1$ is U-shaped, $\alpha \ne \beta$ is asymmetric.

*Example: proportions, probabilities of success, prior on POD in inspection work.*

```{image} ../images/dist_beta.png
:alt: Beta distribution
:width: 650px
:align: center
```

### Exponential

Time between events in a constant-rate Poisson process. **Memoryless** — the only continuous distribution with this property.

| | |
|--|--|
| **Parameters** | $\lambda > 0$ (rate), or equivalently $\theta = 1/\lambda$ (scale) |
| **Support** | $x \in [0, \infty)$ |
| **PDF** | $f(x) = \lambda e^{-\lambda x}$ |
| **CDF** | $F(x) = 1 - e^{-\lambda x}$ |
| **Mean** | $1/\lambda$ |
| **Variance** | $1/\lambda^2$ |

The memoryless property: $P(X > s + t \mid X > s) = P(X > t)$. *A component that has survived 10 years is no more likely to fail next year than a brand new one* — useful as a null model for failures, since real systems usually wear out and depart from this.

*Example: time between rare events; null model for failure times.*

```{image} ../images/dist_exponential.png
:alt: Exponential distribution
:width: 650px
:align: center
```

### Gamma

Generalizes the Exponential — sum of $\alpha$ Exponentials. The Exponential is Gamma with $\alpha = 1$.

| | |
|--|--|
| **Parameters** | $\alpha > 0$ (shape), $\beta > 0$ (scale), sometimes parameterized by rate $= 1/\beta$ |
| **Support** | $x \in (0, \infty)$ |
| **PDF** | $f(x) = \dfrac{x^{\alpha-1} e^{-x/\beta}}{\Gamma(\alpha)\beta^\alpha}$ |
| **Mean** | $\alpha\beta$ |
| **Variance** | $\alpha\beta^2$ |
| **Mode** | $(\alpha - 1)\beta$ for $\alpha \ge 1$ |

```{important}
**Conventions vary.** NumPy and SciPy use `shape` and `scale` ($\alpha$, $\beta$). NumPyro and Stan use `concentration` and `rate` ($\alpha$, $1/\beta$). Always verify which the library expects.
```

*Example: corrosion rates (chapter 3), waiting times for $k$ events, claim sizes.*

```{image} ../images/dist_gamma.png
:alt: Gamma distribution
:width: 650px
:align: center
```

### Weibull

Most flexible distribution for **time-to-failure** modeling. Shape parameter $\beta$ determines failure behavior over time.

| | |
|--|--|
| **Parameters** | $\beta > 0$ (shape), $\eta > 0$ (scale) |
| **Support** | $x \in [0, \infty)$ |
| **PDF** | $f(x) = \dfrac{\beta}{\eta}\!\left(\dfrac{x}{\eta}\right)^{\beta-1} \exp\!\left[-\!\left(\dfrac{x}{\eta}\right)^{\beta}\right]$ |
| **CDF** | $F(x) = 1 - \exp\!\left[-\!\left(\dfrac{x}{\eta}\right)^{\beta}\right]$ |
| **Mean** | $\eta\,\Gamma(1 + 1/\beta)$ |
| **Variance** | $\eta^2 \left[\Gamma(1 + 2/\beta) - \Gamma(1 + 1/\beta)^2\right]$ |

Hazard rate behavior:

- $\beta < 1$ — decreasing hazard (infant mortality).
- $\beta = 1$ — constant hazard (reduces to Exponential).
- $\beta > 1$ — increasing hazard (wear-out).

*Example: bearing failures, fatigue life, wind speeds.*

```{image} ../images/dist_weibull.png
:alt: Weibull distribution
:width: 650px
:align: center
```

## Relationships between distributions

Distributions form a connected web. Key relationships:

- **Binomial → Normal** (de Moivre–Laplace): for large $n$, $\text{Binomial}(n,p) \approx \mathcal{N}(np, np(1-p))$.
- **Binomial → Poisson**: large $n$, small $p$, fixed $np = \lambda$.
- **Poisson ↔ Exponential**: Poisson counts in time correspond to Exponential inter-arrival times.
- **Sum of $k$ Exponentials** = Gamma($k$, $1/\lambda$).
- **Exponential = Gamma**($\alpha = 1$) **= Weibull**($\beta = 1$).
- **Sum of independent Normals** is Normal.

```{note}
Transformed distributions are often used as **conjugate priors** for Bayesian analysis. Related distributions can aid in fitting if a simple model fails.
```

```{image} ../images/distribution-relationship.png
:alt: Relationship Between Select Distributions
:width: 700px
:align: center
```

## Choosing the right distribution

Selecting the correct distribution dictates the performance of inferences and predictions:

- **Data type** — discrete vs. continuous.
- **Support / range** — $[0,1]$ (Beta), $[0, \infty)$ (Exponential/Gamma/Weibull/Lognormal), $(-\infty, \infty)$ (Normal).
- **Shape** — symmetric (Normal), right-skewed (Gamma/Lognormal), U-shaped (Beta with $\alpha, \beta < 1$).
- **Mechanism** — counts (Poisson/Binomial), times (Exponential/Gamma), growth (Lognormal).

| Scenario | Distribution |
|--|--|
| Counts in fixed trials | Binomial |
| Counts over time/space | Poisson |
| Time between events | Exponential |
| Positive, right-skewed measurements | Lognormal, Gamma |
| Symmetric measurements | Normal |
| Proportions/probabilities | Beta |
| Time to failure | Weibull |

## Fitting distributions

### Method of Moments (MoM)

Express the distribution moments as functions of the parameters and solve using the sample moments.

For a Gamma($\alpha, \beta$): mean = $\alpha\beta$, variance = $\alpha\beta^2$. Solving:

$$\hat{\beta} = \frac{s^2}{\bar{x}}, \qquad \hat{\alpha} = \frac{\bar{x}}{\hat{\beta}} = \frac{\bar{x}^2}{s^2}$$

```python
import numpy as np
from scipy.stats import gamma

data = np.random.gamma(shape=3, scale=2, size=500)
m = data.mean()
v = data.var(ddof=1)
alpha_hat = m**2 / v
beta_hat = v / m
print(f"MoM: α = {alpha_hat:.2f}, β = {beta_hat:.2f}  (true: 3, 2)")
```

```{image} ../images/mom_gamma.png
:alt: MoM fit to Gamma
:width: 600px
:align: center
```

**Properties:**
- Not always practical or analytically possible.
- Quick and computationally simple.
- Generally the poorest estimator.
- Good as an **initial estimate** for MLE.

### Least Squares Estimation (LSE)

Linearize the distribution and use least squares.

For the Weibull, the CDF is $F(x) = 1 - \exp[-(x/\eta)^\beta]$. Taking $\ln$ twice:

$$\ln[-\ln(1 - F)] = \beta \ln(x) - \beta \ln(\eta)$$

This is linear in $\ln(x)$ with slope $\beta$ and intercept $-\beta\ln(\eta)$. Use Benard's approximation $\hat{F}_i = (i - 0.3)/(n + 0.4)$ for plotting positions.

```python
import numpy as np

data = np.array([25, 43, 53, 65, 76, 86, 95, 115, 132, 150])
n = len(data)
i = np.arange(1, n + 1)
F_i = (i - 0.3) / (n + 0.4)

X = np.log(np.sort(data))
Y = np.log(-np.log(1 - F_i))
coeffs = np.polyfit(X, Y, 1)
beta_hat = coeffs[0]
eta_hat = np.exp(-coeffs[1] / beta_hat)
```

```{image} ../images/lse_weibull.png
:alt: LSE fit to Weibull
:width: 500px
:align: center
```

**Properties:**
- Works when the distribution can be linearized.
- Provides an R² for fit assessment.
- For linear regression with normal errors, **LSE = MLE**.

### Maximum Likelihood Estimation (MLE)

Choose the parameters that make the observed data most probable under the assumed distribution.

$$\hat\theta_{\text{MLE}} = \arg\max_\theta \prod_{i=1}^{n} f(x_i;\theta) = \arg\max_\theta \sum_{i=1}^{n}\log f(x_i;\theta)$$

```python
from scipy.stats import weibull_min

c_mle, _, scale_mle = weibull_min.fit(data, floc=0)
print(f"MLE: β = {c_mle:.2f}, η = {scale_mle:.1f}")
```

```{image} ../images/mle_weibull.png
:alt: MLE fit to Weibull
:width: 600px
:align: center
```

**Properties:**
- Asymptotically efficient — for large $n$, no unbiased estimator has lower variance.
- Workhorse for most modern statistical models.
- Numerical optimization required for most distributions.

## Properties of estimators

What makes one estimator better than another? Four criteria:

- **Unbiased:** $E[\hat\theta] = \theta$. On average, hits the true value.
- **Consistent:** $\hat\theta \to \theta$ as $n \to \infty$. Converges to truth with enough data.
- **Efficient:** lowest variance among unbiased estimators.
- **Robust:** not overly sensitive to outliers or assumption violations.

### Bias-variance tradeoff

The mean squared error of any estimator decomposes:

$$\text{MSE} = \text{Bias}^2 + \text{Variance}$$

```{image} ../images/bias_variance.png
:alt: Bias-variance tradeoff
:width: 700px
:align: center
```

A slightly biased estimator with much lower variance often produces better overall predictions than an unbiased high-variance one. This is the foundation behind regularization, ridge regression, shrinkage estimators, and most of modern machine learning.

In CML work, a hierarchical Bayesian model deliberately introduces bias by pulling individual CML estimates toward a population mean — accepting bias to gain enormous variance reductions on data-poor CMLs.

## Goodness of fit

Compare an empirical distribution against the theoretical one. P-P and Q-Q plots emphasize different parts:

| | P-P Plot | Q-Q Plot |
|--|--|--|
| **Compares** | Empirical CDF vs. theoretical CDF | Empirical quantiles vs. theoretical quantiles |
| **Emphasizes** | Center of the distribution | Tails — extreme values, outliers |
| **Use for** | Detecting overall shape mismatch, location/scale shifts | Detecting tail behavior |

```{image} ../images/pp_plot.png
:alt: P-P Plot
:width: 600px
:align: center
```

```{image} ../images/qq_plot.png
:alt: Q-Q Plot
:width: 600px
:align: center
```

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

```{warning}
**Confidence intervals are about the procedure, not the parameter.** A specific 95% CI does NOT mean "there's a 95% probability the true value lies in this interval." That's a Bayesian credible interval — a different concept covered in chapter 4.
```

| Method | Strengths | Weakness |
|--|--|--|
| **Standard error (t)** | Fast, simple; uses Student's t with $n-1$ df. | Assumes symmetric, normal-shaped likelihood. Poor for small $n$ or skewed parameters. |
| **Wald** | Fast; needs only MLE and its standard error. | Same as standard error. |
| **Profile likelihood** | Honors actual shape of the likelihood; reliable for small $n$, skewed/bounded parameters. | More computation — evaluate likelihood across a grid. |
| **Bootstrap** | Distribution-free; works for any estimator. | Computationally heavy; quality depends on sample representativeness. |

### Bootstrap

```python
B = 10000
boot_means = [rng.choice(data, size=len(data), replace=True).mean()
              for _ in range(B)]
lo, hi = np.percentile(boot_means, [2.5, 97.5])
```

```{image} ../images/bootstrap_ci.png
:alt: Bootstrap CI
:width: 600px
:align: center
```

The bootstrap distribution of the estimator. Take the 2.5% and 97.5% percentiles to form the 95% CI.

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

```{image} ../images/error-types2.png
:alt: Error Types
:width: 700px
:align: center
```

```{image} ../images/error-types.png
:alt: Error Types
:width: 700px
:align: center
```

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

```{image} ../images/censoring_truncation.png
:alt: Censoring vs truncation
:width: 800px
:align: center
```

```{important}
The key difference: **censored data contributes partial information; truncated data is missing entirely.** Ignoring either produces biased estimates. In CML work, dropping "growth" readings (readings thicker than the previous one) is a form of truncation that biases corrosion rate estimates upward — see chapter 2.
```
