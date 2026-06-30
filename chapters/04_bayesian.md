# 4. Bayesian Statistical Analysis

## End-to-end Bayesian workflow

```
Define Model (priors + likelihood)
  ↓
Prior Predictive Checks
  ↓
Sample (MCMC)
  ↓
Diagnose (R̂, ESS, divergences)
  ↓
Posterior Predictive Checks
  ↓
Model Comparison / Averaging
  ↓
Communicate Results
```

Each box is iterative — failed diagnostics or bad posterior predictive checks send you back to model definition.

## Bayes' theorem

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

## Forward propagation vs. inference

Bayes' theorem solves the **inverse problem**: going from observed data back to parameters.

### Forward (parameters → data)

Given known or assumed parameter values, compute the distribution of observable outcomes. Straightforward — requires only sampling from the likelihood.

$$H \text{ known} \to E \text{ predicted}, \quad \text{sample from } p(E \mid H)$$

### Inverse / Inference (data → parameters)

Given observed data, infer the distribution of unknown parameters. The **core Bayesian task** — and the harder direction.

$$E \text{ observed} \to H \text{ inferred}, \quad \text{recover } p(H \mid E) \text{ via Bayes}$$

## Computing the posterior

How $p(H \mid E)$ is computed depends on model complexity:

| Method | When to use | Mechanism |
|--|--|--|
| **Conjugate** | Prior + likelihood form a conjugate pair (Beta-Binomial, Normal-Normal). | Closed-form; posterior in the same family as the prior. |
| **Numerical** | Low dimension (≤ 2 parameters). | Evaluate the evidence integral on a grid and normalize. `scipy.integrate.quad / dblquad`. |
| **MCMC** | Multi-parameter, hierarchical models. | Sample directly from the posterior — no closed form needed. NUTS (NumPyro, PyMC, Stan); JAGS (Gibbs). |

## Markov Chain Monte Carlo

### Simplified MCMC

- **Random walk** — initial sample is the starting point for the next sample, until rejection criteria are met.
- Rejection criteria based on the credible interval.
- Diverging chains require redesign.
- Posterior estimated from the final cumulative sample of the Markov chain.
- Generally **impossible to solve analytically** — that's why we sample.

### Not all MCMC is the same

| Method | Strength | Weakness | Tools |
|--|--|--|--|
| **Metropolis-Hastings** | Simple models; pedagogy; when gradients aren't available. | Slow in high dimensions — strong autocorrelation, low effective $n$. | Hand-rolled · emcee |
| **Gibbs** | Conjugate hierarchical models with tractable full conditionals. | Correlated parameters → zig-zags through narrow ridges; slow mixing. | JAGS · BUGS · WinBUGS |
| **Hamiltonian** | High-dimensional, correlated spaces. Fewer steps than random walk. | Manual tuning of step size and trajectory length. | Custom HMC implementations |
| **NUTS** | **Default for hierarchical Bayesian models.** Robust, efficient, minimal tuning. | Still needs gradients; not for discrete parameters without reformulation. | Stan · PyMC · NumPyro |

```{note}
NUTS (No U-Turn Sampler) is HMC that auto-picks trajectory length and stops when the path doubles back. Step size auto-tunes during warm-up. **This is the workhorse of modern Bayesian inference.**
```

## How to choose a prior

Each strategy enables certain features in the overall model — this is a **key decision point**.

| Strategy | What it does | Example |
|--|--|--|
| **Conjugate** | Pairs of prior + likelihood whose posterior is in the same family as the prior. Lovely math, but rare for complex models. Convenience is a poor reason to choose a prior. | Beta with Binomial; Gamma with Poisson. |
| **Objective** | Aim for priors that let the data dominate. Useful as a default for routine analyses. "Noninformative" is often a marketing term. | Jeffreys' prior — invariant under reparameterization. |
| **Maximum entropy** | The most uncertain distribution consistent with what you know. Encodes constraints without smuggling in extra structure. | Given only a known mean, MaxEnt gives the Exponential. |
| **Weakly informative** | Mild regularization. Rules out absurd values; keeps the data in charge. **Pragmatic default for modern Bayesian workflows.** | Normal(0, 2.5) on standardized regression coefficients. |

## Everything is a distribution

In a Bayesian model, every quantity is uncertain — and every quantity has a distribution:

- **Corrosion rate** — a distribution, not a single number.
- **Nominal thickness** — a distribution centered on the engineering nominal, with width reflecting manufacturing tolerance and historical readings.
- **Measurement** — a distribution incorporating UT noise and local variability.

This is the conceptual shift from frequentist work. The output of analysis is not point estimates plus error bars; it is **distributions of beliefs**.

## Predictive distributions

The posterior is not the only output. The model can also generate data it expects to see.

### Prior predictive

$$p(Y^*) = \int p(Y^* \mid \theta) \, p(\theta) \, d\theta$$

Sample parameters from the prior, then sample data through the likelihood. Tells you what your priors imply in the observable space — **where you can actually judge them.**

**Use to:** catch absurd implications; calibrate priors with domain experts.

### Posterior predictive

$$p(\tilde Y \mid Y) = \int p(\tilde Y \mid \theta) \, p(\theta \mid Y) \, d\theta$$

Sample parameters from the posterior, then sample data through the likelihood. Predictions automatically carry the posterior's uncertainty — **no manual error bars required.**

**Use to:** check fit; generate forecasts; score the model.

## Before and after inference

Specifying a model and pressing "sample" is **not** the workflow — it's only a part of it.

A complete Bayesian analysis includes:

- **Pre-inference** — prior predictive checks. Do the priors imply plausible data? If not, fix priors before fitting.
- **During inference** — numerical diagnostics. Did the sampler converge? Are the chains exploring the same posterior?
- **Post-inference** — posterior predictive checks. Does the fitted model recreate the patterns in the observed data?
- **Across models** — model comparison. How does each candidate generalize? Should you average instead of pick?
- **Communication** — visual and numerical summaries tailored to the audience. *Posteriors are easier to share than p-values.*

## Diagnosing model inference

If the sampler didn't converge, every downstream conclusion is suspect. **Check the chains first.**

| Diagnostic | What it is | Watch for |
|--|--|--|
| **ESS** (Effective sample size) | How many independent draws your autocorrelated chain is worth. Aim for ESS in the hundreds per parameter. | ESS = 50 with 4000 draws → painful autocorrelation. |
| **R̂** (Potential scale reduction) | Compares within-chain to between-chain variance. Should be ~1.0. | R̂ > 1.01 → chains haven't agreed; re-run longer or rethink the model. |
| **MCSE** (Monte Carlo standard error) | Uncertainty in posterior estimates from finite sampling. Lower = more precise summaries. | Posterior mean reported with MCSE smaller than the resolution you care about. |
| **Trace plots** | Chains should overlap and look like fuzzy caterpillars without drifts or stuck regions. | Visible trends or jumps → reparameterize or extend warm-up. |
| **Rank plots** | If chains agree, ranks of draws across chains should be ~uniform per bin. | Stair-step rank histograms → chains exploring different regions. |
| **Divergences (HMC)** | Symptoms of pathological posterior geometry. Don't ignore — even a few signal trouble. | Funnel posteriors in hierarchical models — reparameterize. |

## Comparing models

Estimate each model's out-of-sample predictive accuracy and combine when it helps.

| Tool | What it does |
|--|--|
| **LOO-CV** | Leave-one-out cross-validation. Approximated efficiently in practice with Pareto-smoothed importance sampling (PSIS-LOO) — no need to refit $n$ times. |
| **ELPD** | Expected log pointwise predictive density. The actual score behind LOO and WAIC. Higher = better out-of-sample fit. |
| **Pareto $\hat{k}$** | Diagnostic for the PSIS-LOO approximation. $\hat{k} > 0.7$ for an observation → approximation unreliable there; consider refitting. |
| **LOO-PIT** | Leave-one-out probability integral transform. Graphical check: under a well-fit model, LOO-PIT values look ~Uniform(0,1). |
| **Model averaging** | Combine models by weight (stacking, pseudo-BMA+) instead of picking one. **Often beats any single model.** |

## Pooling

When groups are present in data, **pooling** may be beneficial.

| Approach | Description | Drawback |
|--|--|--|
| **Unpooled** | Fit each group separately. No information shared. | High variance in small groups. |
| **Pooled** | One set of parameters for everyone. Group identity ignored. | High bias when groups truly differ. |
| **Partial pooling** | Hierarchical priors share information across groups via a higher level. **Best of both worlds — most real problems live here.** | More complex model specification. |

```{important}
**Partial pooling shines when some groups have lots of data and others have very little** — the data-rich groups inform priors that stabilize the data-poor ones. This is exactly the situation in most piping circuits: a few CMLs have decades of readings; many CMLs have just two or three.
```

## Hierarchical partial-pooled model

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

## Determine relevant details

From the posterior, derive the things you actually need:

- **Remaining life** — per CML, with credible intervals.
- **Corrosion rate** — per CML, distribution rather than point estimate.
- **Residuals** — observed minus posterior predictive median.
- **Model diagnostics** — convergence and predictive checks summarized for the report.

## Probabilistic programming languages

| Tool | Style | Notes |
|--|--|--|
| **PyMC** | `with` context manager; NUTS by default. | Easier to use; more documentation. |
| **NumPyro** | Plain function + JAX; explicit `obs`/`sample` plates. | Faster; requires less computing power. |

### PyMC example

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

### NumPyro example

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
