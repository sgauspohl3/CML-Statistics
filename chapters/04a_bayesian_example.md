# Example — Bayesian CML Analysis

The same SWS feed circuit from chapter 3a, now analyzed Bayesian.

## The circuit (recap)

- SWS feed — recently re-circuitized.
- Primarily 4" and 6" SCH40 carbon steel piping.
- Potential for sour water corrosion (erosion) and ammonium bisulfide corrosion.

Same data, same circuit. Only the modeling approach changes.

## Model in NumPyro

A hierarchical partial-pooled model with per-CML initial thickness $T_0$ and corrosion rate $C_r$:

```python
def thickness_model(t, cml, comp_type, nominal_t0_by_type,
                    nominal_sd_by_type, C, y=None):
    with numpyro.plate("cmls", C):
        T_0 = numpyro.sample(
            "T_0",
            dist.Normal(
                loc=nominal_t0_by_type[comp_type],
                scale=nominal_sd_by_type[comp_type],
            ),
        )
        C_r = numpyro.sample(
            "C_r",
            dist.Gamma(concentration=GAMMA_SHAPE_CR, rate=GAMMA_RATE_CR),
        )
    sigma = numpyro.sample("sigma", dist.HalfNormal(SIGMA_HN_SCALE))
    T_t = numpyro.deterministic("T_t", T_0[cml] - C_r[cml] * t)
    with numpyro.plate("obs", t.shape[0]):
        numpyro.sample("y", dist.Normal(T_t, sigma), obs=y)
```

**Structure:**

- **$T_0$ per CML** — drawn from a Normal prior centered on the nominal thickness for that component type, with a width reflecting manufacturing tolerance.
- **$C_r$ per CML** — drawn from a Gamma prior shared across all CMLs (this is the "pool").
- **$\sigma$** — measurement noise; Half-Normal.
- **Likelihood** — observed thickness ~ Normal($T_0 - C_r \cdot t$, $\sigma$).

## Clustering by corrosion zones

Clustering by zone is similar to clustering by feature type, but with a caveat:

```{warning}
If clustering by corrosion zone, consider **separating the circuit** because the partial-pooled model has CMLs drawing from each other. If CMLs in different zones are not similar, it may not be worth comparing and drawing from a single pool.

The example below clusters only by feature.
```

## Running the model

```python
from numpyro.infer import MCMC, NUTS, Predictive
import arviz as az
import numpy as np
import jax.numpy as jnp
from jax import random

# MCMC
kernel = NUTS(thickness_model, target_accept_prob=0.95)
mcmc = MCMC(
    kernel,
    num_warmup=N_WARMUP,
    num_samples=N_SAMPLES,
    num_chains=N_CHAINS,
    chain_method="parallel",   # use "sequential" if your CPU has issues
    progress_bar=True,
)

model_kwargs = dict(
    t=jnp.asarray(t_arr),
    cml=jnp.asarray(cml_arr),
    comp_type=jnp.asarray(comp_type),
    nominal_t0_by_type=jnp.asarray(nominal_t0_by_type),
    nominal_sd_by_type=jnp.asarray(nominal_sd_by_type),
    C=C,
)

mcmc.run(random.PRNGKey(SEED), y=jnp.asarray(y_arr), **model_kwargs)
mcmc.print_summary(exclude_deterministic=True)

# Posterior predictive
posterior = mcmc.get_samples()
predictive = Predictive(thickness_model, posterior_samples=posterior)
ppc = predictive(random.PRNGKey(SEED + 1), **model_kwargs)

# ArviZ InferenceData
idata = az.from_numpyro(
    mcmc,
    posterior_predictive=ppc,
    coords={"cml_idx": np.arange(C)},
    dims={"T_0": ["cml_idx"], "C_r": ["cml_idx"]},
)
```

## Analyzing results

Standard ArviZ artifacts for diagnosing and interpreting the fit:

- **Forest plots** of $T_0$ and $C_r$ across CMLs — see which CMLs differ from the pool.
- **Trace plots** — confirm chains are mixing.
- **Posterior predictive overlay** on the observed thickness data.
- **Residuals** by CML and over time.
- **Chains** — visual confirmation of convergence.

```{note}
This section will be expanded with rendered ArviZ plots in the final version. Each of the five "Analyzing Results" slides in the deck becomes one subsection with the plot, its interpretation, and what to look for.
```

## Final results

Per-CML retirement schedule, sorted by lower HDI bound:

| CML | Feature | n | $t_{\min}$ | In-service | Latest reading | $C_r$ mean | $T_0$ mean | Retire (lower HDI) | Retire date (lower HDI) | Remaining yrs (lower HDI) |
|--|--|--|--|--|--|--|--|--|--|--|
| 023X | 4" SCH40 FIT | 4 | 0.122 | 2013-01-01 | 2015-10-01 | 2.818 | 0.2266 | 20.5 | 2033-06-15 | 17.7 |
| 023 | 6" SCH40 FIT | 16 | 0.18 | 2013-01-01 | 2015-10-01 | 2.627 | 0.2823 | 21.6 | 2034-08-08 | 18.9 |
| 009 | 6" SCH40 FIT | 60 | 0.18 | 2000-01-01 | 2023-06-01 | 2.644 | 0.2896 | 37.1 | 2037-01-31 | 13.7 |
| 008 | 6" SCH40 FIT | 57 | 0.18 | 2000-01-01 | 2023-06-01 | 2.230 | 0.2770 | 38.0 | 2037-12-23 | 14.5 |
| 012 | 6" SCH40 FIT | 27 | 0.18 | 2005-01-01 | 2015-10-01 | 2.118 | 0.2879 | 33.3 | 2038-04-15 | 22.5 |
| 076 | 6" SCH40 FIT | 48 | 0.18 | 2000-01-01 | 2023-06-01 | 2.561 | 0.2993 | 39.6 | 2039-07-29 | 16.1 |
| 121 | 6" SCH40 FIT | 60 | 0.18 | 2005-01-01 | 2019-09-01 | 2.325 | 0.2855 | 35.7 | 2040-09-23 | 21.1 |
| 090 | 4" SCH40 PIPE | 12 | 0.122 | 2005-01-01 | 2019-03-01 | 2.257 | 0.2376 | 35.8 | 2040-10-12 | 21.6 |
| 104 | 4" SCH40 FIT | 60 | 0.122 | 2005-01-01 | 2019-09-01 | 2.841 | 0.2449 | 35.8 | 2040-11-05 | 21.2 |
| 007 | 6" SCH40 FIT | 57 | 0.18 | 2000-01-01 | 2023-08-01 | 2.230 | 0.2833 | 41.4 | 2041-05-20 | 17.8 |

```{important}
**By constructing a model and utilizing available information, the retirement date — even at the lower HDI — is significantly extended from the frequentist analysis.**

The frequentist worst-case scenario suggested ~40 CMLs would retire by 2035. The Bayesian model, leveraging the same data plus engineering knowledge of nominal thicknesses and the population of corrosion rates, produces a much more nuanced — and credible — schedule.

This is not because Bayesian methods are magic; it's because they let you encode prior knowledge and produce per-CML uncertainty rather than forcing you to pick one of four global scenarios.
```
