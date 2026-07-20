# Bayesian Statistical Analysis

## End-to-End Bayesian Workflow

```{figure} ../images/flow-bayesian.png
:name: flow-bayesian
:alt: Bayesian Workflow
:width: 700px
:align: center

End-to-end Bayesian analysis workflow
```

Each box is iterative — failed diagnostics or bad posterior predictive checks send you back to model definition.

## Bayes' Theorem

$$P(H \mid E) = \frac{P(E \mid H) \cdot P(H)}{P(E)}$$

| Term | Name | Meaning |
|--|--|--|
| $P(H \mid E)$ | **Posterior** | What you know now. A weighted compromise — large $n$ → likelihood dominates; small $n$ → prior contributes. |
| $P(E \mid H)$ | **Likelihood** | What the data says. Probability of the data given parameter values. |
| $P(H)$ | **Prior** | What you knew before. Engineering judgment, history, or physics-based predictions. |
| $P(E)$ | **Evidence** | The normalizer. Ensures the posterior integrates to one. |

```{epigraph}
Posterior ∝ Likelihood × Prior
```

In inspection: prior is what you expected the corrosion rate to be; likelihood is what the readings actually showed; posterior is your updated belief — used for predictions about remaining life.

## Forward Propagation vs. Inference

Bayes' theorem solves the **inverse problem**: going from observed data back to parameters.

### Forward (Darameters to Data)

Given known or assumed parameter values, compute the distribution of observable outcomes. Straightforward — requires only sampling from the likelihood.

$$H \text{ known} \to E \text{ predicted}, \quad \text{sample from } p(E \mid H)$$

### Inverse / Inference (Data to Parameters)

Given observed data, infer the distribution of unknown parameters. The **core Bayesian task** — and the harder direction.

$$E \text{ observed} \to H \text{ inferred}, \quad \text{recover } p(H \mid E) \text{ via Bayes}$$

## Computing the Posterior

How $p(H \mid E)$ is computed depends on model complexity:

| Method | When to use | Mechanism |
|--|--|--|
| **Conjugate** | Prior + likelihood form a conjugate pair (Beta-Binomial, Normal-Normal). | Closed-form; posterior in the same family as the prior. |
| **Numerical** | Low dimension (≤ 2 parameters). | Evaluate the evidence integral on a grid and normalize. `scipy.integrate.quad / dblquad`. |
| **MCMC** | Multi-parameter, hierarchical models. | Sample directly from the posterior — no closed form needed. NUTS (NumPyro, PyMC, Stan); JAGS (Gibbs). |

## A Worked Conjugate Update — Beta-Binomial

The simplest closed-form Bayesian update. See the widget below and use the sliders to see how prior, likelihood, and posterior interact with each other. Sliders for prior $\alpha$ and $\beta$, plus the observed data (successes and failures). Live overlay of prior, likelihood, and posterior.

- Watch a strong prior get overwhelmed by lots of data.
- Watch a weak prior update dramatically on even one observation.
- See how skew of the posterior tracks skew of the prior + data combo.

```{raw} html
<iframe src="../_static/beta_binomial_update.html"
        width="100%" height="640"
        style="border:none;">
</iframe>
```

### Setup

Imagine we want to estimate the **detection probability** $\theta$ of an inspection technique. Before testing, we have a weak prior belief: maybe somewhere in the middle, but we're not sure. Model this as a $\text{Beta}(2, 2)$ prior:

- Mean: $\alpha/(\alpha+\beta) = 2/4 = 0.5$
- Mode: near 0.5
- Width: moderate

We then run 10 trials and observe 7 successes. The likelihood is Binomial:

$$P(7 \mid 10, \theta) = \binom{10}{7} \theta^7 (1-\theta)^3$$

### The update

The Beta is the **conjugate prior** for the Binomial — meaning posterior is also Beta, with a beautifully simple update rule:

$$\text{Beta}(\alpha, \beta) + \text{Binomial}(s \text{ successes}, f \text{ failures}) \implies \text{Beta}(\alpha + s, \beta + f)$$

So our $\text{Beta}(2, 2)$ prior plus 7 successes and 3 failures gives:

$$\text{Beta}(2 + 7, 2 + 3) = \text{Beta}(9, 5)$$

- Posterior mean: $9/14 \approx 0.64$
- Posterior mode: $(9-1)/(9+5-2) = 8/12 \approx 0.67$
- Much narrower than the prior — the data dominates.

```{figure} ../images/conjugate_beta_binomial.png
:name: beta-binomial
:alt: Beta-Binomial conjugate update
:width: 700px
:align: center

Example of Beta-Binomial conjugate update
```

The visualization shows all three pieces: the wide prior, the likelihood (scaled for overlay), and the posterior — a weighted compromise. Notice that the posterior peak sits between the prior peak (0.5) and the data's maximum likelihood estimate (0.7), closer to the data because we had 10 observations and only 4 "pseudo-observations" worth of prior.

### Why This Matters

The math is clean: $\alpha$ and $\beta$ are interpretable as **pseudo-counts of successes and failures**. A $\text{Beta}(2, 2)$ prior is equivalent to having seen 1 prior success and 1 prior failure (the +1 in each parameter comes from the symmetry to a uniform). Real data accumulates on top of those pseudo-counts.

This intuition extends. Most conjugate pairs work the same way — pick a prior that summarizes your domain knowledge as if it were data, then let the actual data update it.

```{note}
**When does conjugacy still matter?** It can be very helpful when distributions work out as a pair of conjugates, but that rarely happens, and MCMC is generally used for real-world applications.
```

## Markov Chain Monte Carlo

The idea behind MCMC is easiest to see in its simple cousin: plain old Monte Carlo. 
Suppose we want to estimate $\pi$. Drop random points in a unit square, and count the fraction that land inside the inscribed circle. That fraction converges to π/4 — no MCMC needed, because we can sample the target distribution directly. MCMC extends this idea to distributions we can't sample from directly, using a Markov chain whose stationary distribution is the one we want.

```{raw} html
<iframe src="../_static/pi_monte_carlo.html"
        width="100%" height="620"
        style="border:none;">
</iframe>
```

- **Monte Carlo** — independent random draws. What this widget does. Each point is drawn independently from a uniform distribution.
- **Markov Chain Monte Carlo** — the next sample depends on the current one via a transition rule. Used for sampling from complicated distributions where independent sampling is impossible.

### Simplified MCMC

- **Random walk** — initial sample is the starting point for the next sample, until rejection criteria are met.
- Rejection criteria based on the credible interval.
- Diverging chains require redesign.
- Posterior estimated from the final cumulative sample of the Markov chain.
- Generally **impossible to solve analytically** — that's why we sample.

```{figure} ../images/mcmc.png
:name: mcmc
:alt: Random Walk
:width: 700px
:align: center

Visualization of a random walk
```

### Not All MCMC is the Same

| Method | Strength | Weakness | Tools |
|--|--|--|--|
| **Metropolis-Hastings** | Simple models; pedagogy; when gradients aren't available. | Slow in high dimensions — strong autocorrelation, low effective $n$. | Hand-rolled · emcee |
| **Gibbs** | Conjugate hierarchical models with tractable full conditionals. | Correlated parameters → zig-zags through narrow ridges; slow mixing. | JAGS · BUGS · WinBUGS |
| **Hamiltonian** | High-dimensional, correlated spaces. Fewer steps than random walk. | Manual tuning of step size and trajectory length. | Custom HMC implementations |
| **NUTS** | **Default for hierarchical Bayesian models.** Robust, efficient, minimal tuning. | Still needs gradients; not for discrete parameters without reformulation. | Stan · PyMC · NumPyro |

```{note}
NUTS (No U-Turn Sampler) is HMC that auto-picks trajectory length and stops when the path doubles back. Step size auto-tunes during warm-up. **This is the workhorse of modern Bayesian inference.**
```

## How to Choose a Prior

Each strategy enables certain features in the overall model — this is a **key decision point**.

| Strategy | What it does | Example |
|--|--|--|
| **Conjugate** | Pairs of prior + likelihood whose posterior is in the same family as the prior. Lovely math, but rare for complex models. Convenience is a poor reason to choose a prior. | Beta with Binomial; Gamma with Poisson. |
| **Objective** | Aim for priors that let the data dominate. Useful as a default for routine analyses. "Noninformative" is often a marketing term. | Jeffreys' prior — invariant under reparameterization. |
| **Maximum entropy** | The most uncertain distribution consistent with what you know. Encodes constraints without smuggling in extra structure. | Given only a known mean, MaxEnt gives the Exponential. |
| **Weakly informative** | Mild regularization. Rules out absurd values; keeps the data in charge. **Pragmatic default for modern Bayesian workflows.** | Normal(0, 2.5) on standardized regression coefficients. |

## Everything is a Distribution

In a Bayesian model, every quantity is uncertain — and every quantity has a distribution:

- **Corrosion rate** — a distribution, not a single number.
- **Nominal thickness** — a distribution centered on the engineering nominal, with width reflecting manufacturing tolerance and historical readings.
- **Measurement** — a distribution incorporating UT noise and local variability.

This is the conceptual shift from frequentist work. The output of analysis is not point estimates plus error bars; it is **distributions of beliefs**.

```{figure} ../images/bayes2.png
:name: bayes2
:alt: bayes2
:width: 700px
:align: center

Everything is a distribution if you look for it.
```

## Target Acceptance

In the world of manufacturing, often times you might hear about "six sigma", and being within the six standard deviations above and below expectation. That is 99%. Forget that in the Bayesian world. Unless your model is perfect, it is probably going to diverge. That's why you will typically see 94% HDI. Why 94% and not 95% like typical frequentist applications? Beats me, but I would guess it has something to do with the Bayesians being different. 

## Predictive Distributions

The posterior is not the only output. The model can also generate data it expects to see. This is very useful if you want to simulate data as well. 

### Prior Predictive

$$p(Y^*) = \int p(Y^* \mid \theta) \, p(\theta) \, d\theta$$

Sample parameters from the prior, then sample data through the likelihood. Tells you what your priors imply in the observable space — **where you can actually judge them.**

**Use to:** catch absurd implications; calibrate priors with domain experts.

#### Prior Predictive Check on the SWS-FEED Model

Before running MCMC on the example circuit, ask: what does the model predict if we just sample from the priors?

The model has:

- $T_0 \sim \text{Normal}(\mu_{\text{nom}}, \sigma_{\text{nom}})$ per CML — centered on nominal thickness for that feature.
- $C_r \sim \text{Gamma}(\alpha=4.2, \beta=6.25\times10^{-4})$ — implies mean ≈ 2.6 mpy, SD ≈ 1.3 mpy.
- $\sigma \sim \text{HalfNormal}(0.03)$ — measurement noise.

Sampling 1000 prior predictive trajectories and looking at the implied thickness at $t = 30$ years:

- Predicted thickness range: roughly $t_{\text{nom}} - 0.10$ to $t_{\text{nom}} + 0.02$ inches.
- 95% of trajectories above 0.18".
- No trajectory predicts impossibly negative thickness — Gamma prior on $C_r$ prevents it.

Compare against what's plausible. For a 6" SCH40 fitting with $t_{\text{nom}} = 0.28$" and $t_{\min} = 0.18$":

- A CML reaching $t_{\min}$ within 30 years would have $C_r \approx 0.0033 = 3.3$ mpy.
- Our prior puts ~30% mass above 3 mpy — slightly aggressive but defensible.

This is the check. If the prior predictive said every CML would reach $t_{\min}$ in 5 years, the prior is too aggressive. If it said no CML would lose 5 mils in 50 years, too tight. The current priors are reasonable.

```python
# Pseudocode for the check
prior_samples = sample_from_priors(n=1000)
prior_predictive_y = simulate_observations(prior_samples)
plot_distribution(prior_predictive_y)
# Compare against domain knowledge: t_nom, t_min, typical mpy
```

### Posterior Predictive

$$p(\tilde Y \mid Y) = \int p(\tilde Y \mid \theta) \, p(\theta \mid Y) \, d\theta$$

Sample parameters from the posterior, then sample data through the likelihood. Predictions automatically carry the posterior's uncertainty — **no manual error bars required.**

**Use to:** check fit; generate forecasts; score the model.

## Before and After Inference

Specifying a model and pressing "sample" is **not** the workflow — it's only a part of it.

A complete Bayesian analysis includes:

- **Pre-inference** — prior predictive checks. Do the priors imply plausible data? If not, fix priors before fitting.
- **During inference** — numerical diagnostics. Did the sampler converge? Are the chains exploring the same posterior?
- **Post-inference** — posterior predictive checks. Does the fitted model recreate the patterns in the observed data?
- **Across models** — model comparison. How does each candidate generalize? Should you average instead of pick?
- **Communication** — visual and numerical summaries tailored to the audience. *Posteriors are easier to share than p-values.*

## Diagnosing Model Inference

If the sampler didn't converge, essentially your model did not work. **Check the chains first.**

| Diagnostic | What it is | Watch for |
|--|--|--|
| **ESS** (Effective sample size) | How many independent draws your autocorrelated chain is worth. Aim for ESS in the hundreds per parameter. | ESS = 50 with 4000 draws → painful autocorrelation. |
| **R̂** (Potential scale reduction) | Compares within-chain to between-chain variance. Should be ~1.0. | R̂ > 1.01 → chains haven't agreed; re-run longer or rethink the model. |
| **MCSE** (Monte Carlo standard error) | Uncertainty in posterior estimates from finite sampling. Lower = more precise summaries. | Posterior mean reported with MCSE smaller than the resolution you care about. |
| **Trace plots** | Chains should overlap and look like fuzzy caterpillars without drifts or stuck regions. | Visible trends or jumps → reparameterize or extend warm-up. |
| **Rank plots** | If chains agree, ranks of draws across chains should be ~uniform per bin. | Stair-step rank histograms → chains exploring different regions. |
| **Divergences (HMC)** | Symptoms of pathological posterior geometry. Don't ignore — even a few signal trouble. | Funnel posteriors in hierarchical models — reparameterize. |

## The Funnel Pathology and Reparameterization

The most common geometric pathology in hierarchical Bayesian models is **Neal's funnel** — a posterior shape that looks like a narrow horn opening into a wide bell.

```{figure} ../images/funnel.png
:name: funnel
:alt: Neal's funnel
:width: 600px
:align: center

Looks just like a funnel right?
```

It happens because hierarchical models have parameters at multiple scales: a group-level standard deviation $\tau$ and individual-level deviations $\eta_i$. Their joint posterior looks like a funnel — when $\tau$ is small, the $\eta_i$ are tightly constrained near zero (narrow neck); when $\tau$ is large, they spread out (wide mouth).

NUTS struggles in this geometry. The step size that works at the wide end is too large for the narrow end (rejections + divergences), and the step size that works at the narrow end is too small for the wide end (autocorrelation).

### The Fix: Non-Centered Parameterization

Instead of:

$$\eta_i \sim \text{Normal}(\mu, \tau)$$

write:

$$\eta_i^* \sim \text{Normal}(0, 1) \qquad \eta_i = \mu + \tau \cdot \eta_i^*$$

The standardized $\eta_i^*$ are independent of $\tau$, so the posterior geometry becomes a well-behaved cylinder instead of a funnel. The reparameterization is mathematically equivalent — same posterior, different sampling geometry.

```python
# Centered (often diverges in NumPyro)
eta = numpyro.sample("eta", dist.Normal(mu, tau))

# Non-centered (well-behaved)
eta_std = numpyro.sample("eta_std", dist.Normal(0, 1))
eta = numpyro.deterministic("eta", mu + tau * eta_std)
```

```{tip}
**Rule of thumb:** if your hierarchical model has divergences, reach for non-centered parameterization first. It fixes the funnel pathology more often than any other single change.
```

## Comparing Models

Estimate each model's out-of-sample predictive accuracy and combine when it helps.

| Tool | What it does |
|--|--|
| **LOO-CV** | Leave-one-out cross-validation. Approximated efficiently in practice with Pareto-smoothed importance sampling (PSIS-LOO) — no need to refit $n$ times. |
| **ELPD** | Expected log pointwise predictive density. The actual score behind LOO and WAIC. Higher = better out-of-sample fit. |
| **Pareto $\hat{k}$** | Diagnostic for the PSIS-LOO approximation. $\hat{k} > 0.7$ for an observation → approximation unreliable there; consider refitting. |
| **LOO-PIT** | Leave-one-out probability integral transform. Graphical check: under a well-fit model, LOO-PIT values look ~Uniform(0,1). |
| **Model averaging** | Combine models by weight (stacking, pseudo-BMA+) instead of picking one. **Often beats any single model.** |

## Pooling

When groups are present in data, **pooling** decisions are one of the most consequential modeling choices you make. There are three approaches.

The widget below gives an example of pooling effects. Use the slider to move towards or awy from the population. 

```{raw} html
<iframe src="../_static/partial_pooling.html"
        width="100%" height="520"
        style="border:none;">
</iframe>
```


### Unpooled (No Pooling)

Fit each group separately. No information shared.

$$\theta_g \sim \text{independent prior} \quad \text{for each group } g$$

**When to use:** plenty of data per group; you genuinely believe the groups don't share structure.

**Issues:** data-poor groups have wide credible intervals dominated by the prior. With $n=2$ readings on a CML, the unpooled posterior is barely better than the prior.

```{figure} ../images/unpooled.png
:name: unpooled-data
:alt: Unpooled Data
:width: 400px
:align: center

Example of complete unpooling
```

### Pooled (Complete Pooling)

One set of parameters for everyone. Group identity ignored.

$$\theta \sim \text{prior} \quad \text{(shared)}$$

**When to use:** the groups are truly identical, or you have no reason to suspect they differ.

**Issues:** if groups *do* differ, you're forcing them all to look the same. Real corrosive zones get masked by the average of the whole circuit.

Fit each group separately. No information shared.

$$\theta_g \sim \text{independent prior} \quad \text{for each group } g$$

**When to use:** plenty of data per group; you genuinely believe the groups don't share structure.

**Issues:** data-poor groups have wide credible intervals dominated by the prior. With $n=2$ readings on a CML, the unpooled posterior is barely better than the prior.

```{figure} ../images/pooled.png
:name: pooled-data
:alt: pooled-data
:width: 400px
:align: center

Example of complete pooling
```

### Partial Pooling (Hierarchical)

The middle ground. Each group has its own parameter, but those parameters are drawn from a shared distribution whose own parameters are also estimated.

$$\mu, \tau \sim \text{hyperprior}$$
$$\theta_g \sim \text{Normal}(\mu, \tau) \quad \text{for each group } g$$

The data tells the model how similar the groups are, via $\tau$. Small $\tau$ → groups are nearly identical → behaves like complete pooling. Large $\tau$ → groups are very different → behaves like no pooling.

```{figure} ../images/partialpooled.png
:name: partial-pooled
:alt: partial-pooling
:width: 400px
:align: center

Example of partial pooled
```

### The Shrinkage Effect

```{figure} ../images/pooling.png
:name: pooling
:alt: Pooling comparison
:width: 800px
:align: center

Unpooled vs Pooled vs Partial Pooled
```

This is the central insight of hierarchical modeling. Look at the figure:

- **Unpooled (left):** small groups (G1, G3, G4 with n=2-6) have wide error bars and individual estimates that scatter. The estimate for G1 sits at ~7 with a CI ranging from ~6 to ~8 — wide and not very informative.
- **Pooled (middle):** every group gets the same point estimate at the overall mean. This works for G5 and G6 (close to truth) but fails for G1 and G4 (truth is far from the pool mean).
- **Partial pooling (right):** estimates for small groups are **shrunk toward the pooled mean** — but only as much as the data warrants. G5 and G6 (large $n$) barely move from their unpooled estimates. G1 and G4 (small $n$) get pulled substantially toward the population mean.



### Why Partial Pooling is Effective for CMLs

Real piping circuits have wildly uneven sampling:

- A few well-instrumented CMLs with 10+ readings spanning decades.
- Many CMLs with 3-5 readings.
- Newly-installed CMLs with 1-2 readings.

```{important}
**Partial pooling shines exactly when some groups have lots of data and others have very little** — the data-rich groups inform priors that stabilize the data-poor ones. A newly-installed CML inherits its baseline expectation from the rest of the circuit, instead of having to be estimated from its own two data points.
```

The Bayesian example in chapter 4a uses partial pooling on per-CML corrosion rates. The shrinkage stabilizes the data-poor CMLs without forcing them to match the data-rich ones — a balance frequentist methods can only awkwardly approximate.

## Hierarchical Partial-Pooled Model

The model used in the example chapter is a **hierarchical partial-pooled** model:

- **Customizable** — hierarchy structured based on SME input. Variables shown are examples; other distributions can be modeled.
- **Pooling** — at the individual CML level and/or by cluster.
- **Life prediction and anomaly detection** — leans on priors in the absence of historical data.
- **Adept at capturing anomalies** that do not fit with the rest of the pool.
- **Uncertainty quantification** — built-in.

### Structure

For $i$ CMLs with $j$ observations each:

```
i:    cml index
i × j: observations
```

Parameters at the CML level (e.g., $T_0$, $C_r$ per CML) are drawn from group-level distributions whose parameters are themselves estimated.

```{figure} ../images/numpyro-plate.png
:name: numpyro-plate
:alt: NumPyro model
:width: 800px
:align: center

Visual representation of partial pooled model.
```

### Why Linear

At the level of data typically present for CMLs, utilizing anything other than a line could potentially over-fit the model. An over-fit model may still be useful for inference data, but will be useless for predictive models. 


## Determine Relevant Details

From the posterior, derive the things you actually need:

- **Remaining life** — per CML, with credible intervals.
- **Corrosion rate** — per CML, distribution rather than point estimate.
- **Residuals** — observed minus posterior predictive median.
- **Model diagnostics** — convergence and predictive checks summarized for the report.


## Probabilistic Programming Languages

For Python, PyMC and NumPyro are the most common choices. NumPyro is typically faster, but PyMC is easier to use. This class uses NumPyro due to speed limitations. PyMC did have a recent update which allowed use of a NumPyro sampler which would speed things up, but there was not enough time to refactor the code. 


| Tool | Style | Notes |
|--|--|--|
| **PyMC** | `with` context manager; NUTS by default. | Easier to use; more documentation. |
| **NumPyro** | Plain function + JAX; explicit `obs`/`sample` plates. | Faster; requires less computing power. |

### PyMC Example

```python
import pymc as pm
import numpy as np

t = data["years_in_service"].values
y = data["thickness"].values
T0_prior_mean = data["nominal_t"].values

with pm.Model() as model:
    # Priors
    T0 = pm.Normal("T0", mu=T0_prior_mean, sigma=0.05, shape=len(t))
    Cr = pm.Gamma("Cr", alpha=4.2, beta=1600)
    sigma = pm.HalfNormal("sigma", sigma=0.01)

    # Likelihood
    mu = T0 - Cr * t
    pm.Normal("y", mu=mu, sigma=sigma, observed=y)

    # Inference
    idata = pm.sample(1000, tune=1000, chains=4, target_accept=0.9)
```

### NumPyro Example

```python
import numpyro
import numpyro.distributions as dist
from numpyro.infer import MCMC, NUTS
from jax import random

numpyro.set_host_device_count(4)

def model(t, T0_prior_mean, y=None):
    with numpyro.plate("cml", len(t)):
        T0 = numpyro.sample("T0", dist.Normal(T0_prior_mean, 0.05))
    Cr = numpyro.sample("Cr", dist.Gamma(4.2, 1600.))
    sigma = numpyro.sample("sigma", dist.HalfNormal(0.01))

    mu = T0 - Cr * t
    numpyro.sample("y", dist.Normal(mu, sigma), obs=y)

kernel = NUTS(model, target_accept_prob=0.9)
mcmc = MCMC(kernel, num_warmup=1000, num_samples=1000, num_chains=4)
mcmc.run(random.PRNGKey(0), t, T0_prior_mean, y=y)
```

```{note}
**Structural differences to be aware of:**
- PyMC uses a `with` block; NumPyro defines a plain function.
- Gamma parameters: PyMC takes (α, β); NumPyro takes (concentration, rate) — same call here.
- Parallel chains: NumPyro requires `set_host_device_count` before any JAX operation.
```

## Expected Results

These are just some of the things from an inference model you might encounter. We will touch more on these in the example later.

**Diagnostic Plots**

```{figure} ../images/bhm-diagnostic.png
:name: bhm-diagnostic
:alt: bhm-diagnostic
:width: 300px
:align: center

Chains
```

<br><br>

**Posterior Forest Plots**

```{figure} ../images/bhm-forest.png
:name: bhm-forest
:alt: bhm-forest
:width: 500px
:align: center

Forest plot of posterior corrosion rates. A clear outlier is shown.
```

<br><br>

**Trajectory Plots**

```{figure} ../images/bhm-trajectory.png
:name: bhm-trajectory
:alt: bhm-trajectory
:width: 600px
:align: center

Trajectory plot showing estimated remaining life of CML with observed readings and 94% HDI.
```

<br><br>

**Residual Plots**

```{figure} ../images/bhm-rope.png
:name: bhm-rope
:alt: bhm-rope
:width: 600px
:align: center

Residual plot for model.
```


## Beyond the Basic Model

The model used in chapter 6 is a Normal-Gamma hierarchical model — simple, fast, and good enough for most CML circuits. But the Bayesian toolkit has more to offer when the data demands it. Keep in mind, it can also be *ANY* model you can dream of. If you want to use a normal distribution for corrosion rate, go for it. It may not work, but it can be done. 

### Categorical and Dirichlet Distributions

Some inspection data is categorical, not numerical: damage mechanism class, root cause category, corrosion morphology type. The **Categorical** distribution handles single categorical outcomes, and the **Dirichlet** is its multi-category conjugate prior (generalization of the Beta to more than two outcomes).

*When you'd reach for it:* modeling the probability distribution over damage mechanisms in a circuit, or learning the mix of "general" / "pitting" / "MIC" corrosion patterns from a labeled dataset.

### Bayesian Additive Regression Trees (BART)

When the relationship between predictors and outcomes is unknown and possibly non-linear, **BART** offers a flexible nonparametric Bayesian approach. It fits a sum of weak decision trees with priors on tree depth and leaf values.

*When you'd reach for it:* if you suspect corrosion rate depends on a combination of process variables like corrosion under insulation (insulation, temperature, coating age) in a complicated way that no simple parametric model captures.

```{figure} ../images/bart_cui_tree.png
:name: bart-cui-tree
:alt: BART
:width: 800px
:align: center

Part of a BART tree for a CUI model
```

### Time Series Models

Time series methods (autoregressive models, state-space models, Gaussian processes) become relevant when:

- Inspection cadence is fine-grained enough to detect time trends.
- Process upsets cause step-changes in corrosion rate.
- You want to forecast future thickness, not just estimate average rate.

The linear-trend model in chapter 6 is effectively a degenerate time series — it assumes a single constant rate. Real data sometimes shows acceleration, deceleration, or seasonality that a richer time series model would capture.

```{note}
These are **mentions, not recommendations.** For most CML programs, the basic hierarchical model in chapter 6 is the right tool. Reach for these extensions only when the basic model demonstrably fails — diagnosed via posterior predictive checks that fail in specific, interpretable ways.
```

## A Note on Bayesian Decision Theory

This course focuses on **inference** — figuring out the distribution of parameters from data. But once you have a posterior, you often have to make a **decision**: replace this CML now, schedule the next inspection, choose between maintenance strategies.

Bayesian **decision theory** formalizes this. You specify a *utility function* (or equivalently a *loss function*) that encodes the consequences of each possible action under each possible world state. Then you choose the action that maximizes expected utility, integrated over the posterior:

$$a^* = \arg\max_a \int U(a, \theta) \, p(\theta \mid Y) \, d\theta$$

For CML work, this would mean weighing the cost of replacement against the probability and consequence of leak, weighted by the posterior on corrosion rate.

```{note}
**This course doesn't go further into decision theory** — it's a substantial subject on its own. But know that the posterior is *not the final answer*; it's the input to whatever decision you actually need to make. Treating the posterior as the deliverable, rather than as the input to a decision, is a common gap in practice.

For further reading: *Bayesian Modeling and Computation in Python* (Martin, Kumar, Lao) chapter on decision-theoretic concepts, and the broader literature on risk-based inspection (API RP 580/581) for the inspection-specific framing.
```
