# Glossary

This glossary covers terminology used throughout the book. It is split into three sections: **inspection terms**, **statistics and modeling terms**, and **mathematical symbols**.

## Inspection terms

```{glossary}
CML
  **Corrosion Monitoring Location.** A designated area on piping systems where periodic examinations are conducted to directly assess and monitor the condition of the piping system using a variety of examination methods and techniques based on damage mechanism susceptibility. A CML is a logical entity — the *place* being monitored — and may contain multiple TMLs.

TML
  **Thickness Monitoring Location.** A specific physical point within a CML where a measurement is recorded. A single CML can contain several TMLs (e.g., 12 o'clock, 3 o'clock, 6 o'clock, 9 o'clock on a pipe section).

MP
  **Measurement Point.** An individual UT reading taken at a TML. Multiple MPs per TML reduce measurement noise.

NPS
  **Nominal Pipe Size.** Standard pipe size designation (e.g., 4", 6", 24"). Determines outer diameter but not wall thickness.

SCH
  **Schedule.** Standard wall thickness classification (SCH 10, 40, 80, 160, XS, XXS). Determines nominal wall thickness for a given NPS.

SBC
  **Small Bore Connection.** Piping branches typically ≤ 2" NPS off a main line. Often used for instrument taps, drains, vents. Statistically distinct from the main line and usually analyzed separately.

IDMS
  **Inspection Data Management System.** Software used to store, organize, and analyze inspection data. Examples: Meridium, PCMS, Antea, Visions.

UT
  **Ultrasonic Testing.** Non-destructive method using sound waves to measure thickness. The most common method for CML inspection.

RT
  **Radiographic Testing.** Non-destructive method using X-rays or gamma rays. Provides a profile view rather than a point measurement.

PAUT
  **Phased Array Ultrasonic Testing.** UT variant that uses a multi-element transducer for area scanning. Offers better coverage than spot UT.

AUT
  **Automated Ultrasonic Testing.** UT performed by an automated scanner rather than a hand-held probe. Provides repeatable area coverage.

STCR
  **Short-Term Corrosion Rate.** Corrosion rate computed from the second-to-last and last thickness readings. Sensitive to recent changes.

LTCR
  **Long-Term Corrosion Rate.** Corrosion rate computed from the first (baseline) and last thickness readings. Stable estimate for planning.

t_nom
  **Nominal thickness.** Manufacturer's specified wall thickness for a given NPS and schedule, before any corrosion or wear.

t_min
  **Minimum required thickness.** The thinnest wall the component can safely have under design conditions. Below this, the component must be retired or repaired.

t_actual
  **Current thickness.** The most recent measured wall thickness at a CML.

CR
  **Corrosion Rate.** The rate at which wall thickness is decreasing, typically expressed in mils per year (mpy) or inches per year. Positive = thinning.

mpy
  **Mils per year.** A mil is 0.001 inch. The standard unit for corrosion rate in US oil and gas inspection. 5 mpy = 0.005 in/yr.

POD
  **Probability of Detection.** The probability that an inspection technique detects a flaw of a given size. A key input to risk-based inspection.

RBI
  **Risk-Based Inspection.** A methodology that allocates inspection effort based on calculated risk (probability of failure × consequence of failure). Codified in API RP 580 and API RP 581.

EVA
  **Extreme Value Analysis.** Statistical methods for analyzing the maxima or minima of a dataset, rather than the bulk. Useful for predicting worst-case pit depths.

CV
  **Coefficient of Variation.** Sample standard deviation divided by sample mean ($s / \bar{x}$). Unitless measure of relative spread. A CV < 10% within a TML is generally acceptable.

API 510
  **API Pressure Vessel Inspection Code.** Standard for in-service inspection, rating, repair, and alteration of pressure vessels.

API 570
  **API Piping Inspection Code.** Standard for in-service inspection, repair, alteration, and rerating of piping systems.

API 574
  **API Inspection Practices for Piping System Components.** Recommended practice for inspecting piping components in operating service.

API RP 580
  **API Risk-Based Inspection.** Recommended practice giving the framework and minimum requirements for an RBI program.

API RP 581
  **API Risk-Based Inspection Methodology.** Quantitative methodology for implementing RBI.

Damage mechanism
  The underlying physical or chemical process causing material degradation. Examples: general corrosion, pitting, MIC (microbiologically influenced corrosion), CUI (corrosion under insulation), erosion-corrosion.

Dead leg
  A section of piping with little or no flow. Often subject to higher corrosion rates due to stagnant water accumulation, microbial activity, or trapped reactive species.

Mix point
  A location where two streams of different chemistry, temperature, or phase combine. Often shows accelerated corrosion downstream.

Injection point
  A location where chemicals or process fluids are injected into a piping circuit. Often shows enhanced corrosion in a defined downstream zone.
```

## Statistics and modeling terms

```{glossary}
PMF
  **Probability Mass Function.** Function giving the probability that a discrete random variable takes a particular value: $P(X = x)$.

PDF
  **Probability Density Function.** Function describing the relative likelihood of values for a continuous random variable. Density at a point, not probability.

CDF
  **Cumulative Distribution Function.** Function giving the probability that a random variable is less than or equal to a value: $F(x) = P(X \le x)$.

ECDF
  **Empirical Cumulative Distribution Function.** The CDF computed directly from data — each observation becomes a step.

CLT
  **Central Limit Theorem.** Result stating that the distribution of the sample mean approaches Normal as $n \to \infty$, regardless of the underlying distribution (assuming finite variance).

LLN
  **Law of Large Numbers.** Result stating that the sample mean converges to the population mean as sample size increases.

CI
  **Confidence Interval** (frequentist) or **Credible Interval** (Bayesian). The two are NOT interchangeable — see chapter 1 and chapter 4 for the distinction.

MoM
  **Method of Moments.** A parameter estimation method that sets sample moments equal to population moments and solves. Fast but generally the least precise.

MLE
  **Maximum Likelihood Estimation.** Parameter estimation by maximizing the probability of the observed data under the assumed distribution. Asymptotically efficient — the workhorse of frequentist statistics.

LSE
  **Least Squares Estimation.** Parameter estimation by minimizing the sum of squared residuals. For linear regression with Normal errors, LSE equals MLE.

AIC
  **Akaike Information Criterion.** Model comparison metric: $\text{AIC} = 2k - 2\ln(\hat{L})$. Lower is better. Penalizes complexity less than BIC.

BIC
  **Bayesian Information Criterion.** Model comparison metric: $\text{BIC} = k\ln(n) - 2\ln(\hat{L})$. Lower is better. Penalizes complexity more than AIC, especially for large $n$.

KS test
  **Kolmogorov-Smirnov test.** Goodness-of-fit test comparing an empirical CDF to a theoretical one. Sensitive to the center of the distribution.

AD test
  **Anderson-Darling test.** Goodness-of-fit test similar to KS but weighting the tails more heavily. Often more sensitive than KS for detecting bad fits in the tails.

P-P plot
  **Probability-Probability plot.** Diagnostic plot comparing empirical CDF to theoretical CDF. Emphasizes the center of the distribution.

Q-Q plot
  **Quantile-Quantile plot.** Diagnostic plot comparing empirical quantiles to theoretical quantiles. Emphasizes the tails.

MCMC
  **Markov Chain Monte Carlo.** A family of algorithms for sampling from arbitrary probability distributions by constructing a Markov chain whose stationary distribution is the target.

HMC
  **Hamiltonian Monte Carlo.** An MCMC method that uses gradient information to propose efficient moves. Far more efficient than random-walk methods in high dimensions.

NUTS
  **No-U-Turn Sampler.** An adaptive variant of HMC that automatically chooses trajectory length. The default in modern probabilistic programming libraries (Stan, PyMC, NumPyro).

ESS
  **Effective Sample Size.** The equivalent number of independent draws represented by an autocorrelated MCMC sample. Higher = more precise estimates.

R̂
  **R-hat (potential scale reduction factor).** MCMC convergence diagnostic comparing within-chain to between-chain variance. Target R̂ < 1.01.

MCSE
  **Monte Carlo Standard Error.** Uncertainty in posterior estimates arising from finite MCMC sampling. Smaller MCSE = more precise summary statistics.

HDI
  **Highest Density Interval.** The narrowest credible interval containing a given probability mass (e.g., 94% HDI). Differs from a quantile-based interval when the posterior is skewed.

Conjugate prior
  A prior distribution that, combined with a given likelihood, produces a posterior in the same family as the prior. Example: Beta is conjugate to Binomial.

Posterior
  $P(\theta \mid Y)$. The probability distribution of parameters given the observed data. The output of a Bayesian analysis.

Prior
  $P(\theta)$. The probability distribution of parameters before seeing the data. Encodes domain knowledge.

Likelihood
  $P(Y \mid \theta)$. The probability of the observed data given the parameters. Not a probability distribution over $\theta$.

Evidence
  $P(Y)$. The marginal probability of the data. The normalizing constant in Bayes' theorem. Often the hardest piece to compute, which is why MCMC is needed.

Prior predictive
  $P(\tilde{Y})$. Distribution of data the model expects *before* seeing any data. Useful for sanity-checking priors.

Posterior predictive
  $P(\tilde{Y} \mid Y)$. Distribution of new data the model expects *after* updating on observed data. Used for model checking and forecasting.

Exchangeability
  A property of a sequence of random variables: their joint distribution is unchanged under any permutation of indices. The central assumption justifying pooled analysis.

Pooling
  Sharing statistical strength across groups. Three regimes: no pooling, complete pooling, and partial pooling (hierarchical).

Shrinkage
  The effect of pulling individual group estimates toward a population mean. The signature behavior of hierarchical Bayesian models.

Hierarchical model
  A Bayesian model in which parameters at one level are themselves drawn from distributions whose parameters are estimated. Enables partial pooling.

Divergence
  In HMC/NUTS, a numerical failure indicating that the sampler couldn't follow the posterior geometry. Even a few divergences are a warning sign — fix them with reparameterization or tighter priors.

Funnel
  A pathological posterior shape common in hierarchical models, where group-level standard deviation and individual deviations create varying-curvature geometry. Fixed by non-centered parameterization.

Non-centered parameterization
  A reparameterization of a hierarchical model that separates the location and scale of individual parameters from their standardized values. Cures the funnel pathology.

LOO-CV
  **Leave-One-Out Cross-Validation.** Estimates a model's out-of-sample predictive accuracy by predicting each observation from a model fit to all others. Approximated efficiently with PSIS-LOO.

ELPD
  **Expected Log Pointwise Predictive Density.** The metric underlying LOO-CV and WAIC. Higher = better out-of-sample fit.

Type I error
  False positive — rejecting a true null hypothesis. Controlled by significance level $\alpha$.

Type II error
  False negative — failing to reject a false null hypothesis. Controlled by sample size and effect size; complement is statistical power.

Censoring
  An observation is known to lie in some range but its exact value is not. Distinct from truncation.

Truncation
  Observations outside a range are entirely missing from the dataset. Distinct from censoring.
```

## Mathematical symbols

```{glossary}
$X$, $Y$
  Random variables. Capital letters by convention.

$x$, $y$
  Specific values that a random variable can take.

$N$, $n$
  Population size ($N$) and sample size ($n$).

$\mu$
  Population mean.

$\bar{x}$
  Sample mean.

$\sigma$
  Population standard deviation.

$\sigma^2$
  Population variance.

$s$
  Sample standard deviation.

$s^2$
  Sample variance.

$\hat{\theta}$
  Estimator of parameter $\theta$. The hat indicates "estimate" rather than the true value.

$\theta$
  Generic parameter (or vector of parameters) of a distribution.

$\alpha$
  Generally a shape parameter (Gamma, Beta), or a significance level for hypothesis testing.

$\beta$
  Generally a scale parameter (Gamma) or a shape parameter (Beta, Weibull). Also the Type II error rate.

$\eta$
  Weibull scale parameter.

$\lambda$
  Rate parameter (Poisson, Exponential).

$\nu$
  Degrees of freedom (Student's $t$, chi-squared).

$\Gamma(\cdot)$
  The Gamma function. $\Gamma(n) = (n-1)!$ for positive integer $n$.

$\Phi(\cdot)$
  Standard Normal CDF.

$\phi(\cdot)$
  Standard Normal PDF.

$\sim$
  "Distributed as." For example, $X \sim \mathcal{N}(0, 1)$ means $X$ is distributed as standard Normal.

$\propto$
  "Proportional to." Used to indicate equality up to a normalizing constant. Common in Bayes: $p(\theta \mid Y) \propto p(Y \mid \theta) p(\theta)$.

$E[X]$
  Expected value of $X$. Also written $\mathbb{E}[X]$ or $\mu_X$.

$\text{Var}(X)$
  Variance of $X$.

$\text{Cov}(X, Y)$
  Covariance of $X$ and $Y$.

$\rho$
  Correlation coefficient.

$P(A)$
  Probability of event $A$.

$P(A \mid B)$
  Conditional probability of $A$ given $B$.

$p(\cdot)$
  Generic probability density or mass function.

$\mathcal{N}(\mu, \sigma^2)$
  Normal distribution with mean $\mu$ and variance $\sigma^2$. Sometimes parameterized with standard deviation instead.

$\mathcal{N}^+(0, \sigma^2)$
  Half-Normal distribution with scale $\sigma$.

$\text{Beta}(\alpha, \beta)$
  Beta distribution.

$\text{Gamma}(\alpha, \beta)$
  Gamma distribution. Watch the parameterization — shape/scale vs. shape/rate.

$\text{Weibull}(\beta, \eta)$
  Weibull distribution with shape $\beta$ and scale $\eta$.

$\text{Binomial}(n, p)$
  Binomial distribution.

$\text{Poisson}(\lambda)$
  Poisson distribution.

$\text{Bernoulli}(p)$
  Bernoulli distribution.

$T_0$
  In the example CML model: thickness of a CML at time of installation.

$C_r$
  In the example CML model: corrosion rate of a CML, expressed in inches per year (positive = thinning).

$t$
  Time, typically years in service.
```
