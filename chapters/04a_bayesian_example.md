# Example — Bayesian CML Analysis

## Download Data
A complete walkthrough of the Bayesian workflow on a real piping circuit. This is the same as in Chapter 4. 

Please download the dataset used in this example and place in your project folder:
<a href="../_static/TR_596-example2.xlsx" download>TR_596-example2.xlsx</a>

<br>

The accompanying P&ID and Isometric drawings
<a href="../_static/SWS-PID.pdf" download>SWS-PID.pdf</a><br>
<a href="../_static/SWS-ISOs.pdf" download>SWS-ISOs.pdf</a>

```{note}
The same circuit is reanalyzed in chapter 6 using Bayesian methods.
```

## The Circuit: SWS-FEED

- Recently re-circuitized as the company switched from line-based to circuit-based inspections.
- Primarily **4" and 6" SCH40 carbon steel piping**, with a few SCH80 and SBC.
- Damage mechanisms of concern: **sour water corrosion (erosion)** and **ammonium bisulfide corrosion** in parts.
- SBCs and drain lines have already been removed for your convenience. 


### Supporting Documents

#### P&ID

```{figure} ../images/PFD.png
:name: PFD2
:alt: PFD for Example
:width: 700px
:align: center

P&ID of example circuit SWS-FEED, Sour water feed.
```

#### ISOs

```{raw} html
   <iframe src="../_static/isometric_gallery.html"
           width="100%" height="500"
           style="border:none;">
   </iframe>
```


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
## Selecting Priors
Where did we get the priors from? Good question.

**Structure:**

- **$T_0$ per CML** — drawn from a Normal prior centered on the nominal thickness for that component type, with a width reflecting manufacturing tolerance (+/- 12.5% is 6 $\sigma$).
- **$C_r$ per CML** — drawn from a Gamma prior shared across all CMLs (this is the "pool").
- **$\sigma$** — measurement noise; Half-Normal with up to 30mil variance
- **Likelihood** — observed thickness ~ Normal($T_0 - C_r \cdot t$, $\sigma$). — linear relationship

```{figure} ../images/numpyro-plate.png
:name: numpyro-plate1
:alt: NumPyro model
:width: 800px
:align: center

Visual representation of partial pooled model.
```

## On Corrosion Rate Priors
A good idea to have a library of corrosion rate distributions. When observing corrosion in your facility's IDMS system, attribute CMLs to certain damage mechanisms. Try to cluster and find fits for specific damage mechanisms at certain ranges of conditions. If this is not possible, try to calculate best and worst case corrosion rates for the damage mechanism of interest, and then create a distribution that contains 95% of its area within those two bounds.

## Clustering by Corrosion Zones

Clustering by zone is similar to clustering by feature type, but with a caveat:

```{warning}
If clustering by corrosion zone, consider **separating the circuit** because the partial-pooled model has CMLs drawing from each other. If CMLs in different zones are not similar, it may not be worth comparing and drawing from a single pool.

The example below clusters only by feature.
```

```{figure} ../images/numpyro-plate2.png
:name: numpyro-plate2
:alt: NumPyro model2
:width: 800px
:align: center

Visual representation of partial pooled model clustered by corrosion zone.
```

## Prior Predictive Checks

NumPyro does not have built in prior predictive inference like PyMC or libraries outside of Python. The prior predictive check was ran in PyMC and the results are below:

All of the priors look good, but variance might be a little low. Below is an example prior predictive check from PyMC

```{figure} ../images/example-bhm-prior-predictive.png
:name: example-bhm-prior-predictive
:alt: example-bhm-prior-predictive
:width: 800px
:align: center

Prior predictive checks using PyMC
```

Prior predictive checks are not always required, but it can help save a lot of computational time from divergences in later inferences.


## Running the Model

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

## Analyzing Results

Standard ArviZ artifacts for diagnosing and interpreting the fit:

- **Forest plots** of $T_0$ and $C_r$ across CMLs — see which CMLs differ from the pool.
- **Trace plots** — confirm chains are mixing.
- **Posterior predictive overlay** on the observed thickness data.
- **Residuals** by CML and over time.
- **Chains** — visual confirmation of convergence.

```{note} The graphs are below, but the clean version of the code to produce the charts have not been finished yet. 
This will be available at a later date.
```

```{figure} ../images/example-bhm-forest-global.png
:name: example-bhm-forest-global
:alt: example-bhm-forest-global
:width: 800px
:align: center

Global prior vs posterior for global variables
```

The model looks good here as far as overall priors. Let's look a bit deeper at individual CML posterior rates.

<br><br>

```{figure} ../images/example-bhm-forest.png
:name: example-bhm-forest
:alt: example-bhm-forest
:width: 800px
:align: center

Forest plot of posterior corrosion rates by CML
```

This looks a little busy, so let's separate by cluster.

<br>

```{figure} ../images/example-bhm-forest-cluster.png
:name: example-bhm-forest-cluster
:alt: example-bhm-forest-cluster
:width: 800px
:align: center

Global prior vs posterior for posterior corrosion rates by CML, separated by cluster
```

This is easy to read. Anything that we see with a higher than expected corrosion rate?

<br>

```{figure} ../images/example-bhm-trajectory.png
:name: example-bhm-trajectory
:alt: example-bhm-trajectory
:width: 800px
:align: center

Selection of 6 CML trajectories with 94% HDI filled in
```

The model produces bands that are expected, though some of the fittings have readings that do not fit within the model, residuals. Let's take a look at some residuals.

```{figure} ../images/example-bhm-rope.png
:name: example-bhm-rope
:alt: example-bhm-rope
:width: 800px
:align: center

Residuals across features
```

It seems some of the fittings had higher residuals. 


## Final Results

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

This is not because Bayesian methods are magic; it's because they let you encode prior knowledge and produce per-CML uncertainty rather than forcing you to pick one rate and one thickness.
```

## Try on Your Own


```{exercise}
:label: cml-057-retirement2

What is the expected retirement date (lower HDI) of CML 057?
```

```{solution} cml-057-retirement
:class: dropdown

*[2068]*
```