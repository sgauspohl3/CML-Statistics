# Frequentist Statistical Analysis

## API standards allowing statistical analysis

API standards permit statistical methods but don't prescribe a methodology — the verbiage is loose, requiring documentation and caution.

### API 510 §7.2.2

A statistical analysis may be used in the corrosion rate and remaining life calculations for pressure vessel sections. This may be applied for assessment of substituting an internal inspection (see 6.5.2.1b) or for determining the internal inspection interval. Care should be taken to ensure the statistical treatment reflects the actual condition of the vessel section, especially those subject to localized corrosion. **Statistical analysis may not be applicable to vessels with random but significant localized corrosion. The analysis method shall be documented.**

### API 570 §7.1.1 and §7.1.3

The owner/user may use either point-to-point analysis or a statistical analysis method — or a combination — to determine long-term and short-term corrosion rates.

The owner/user may elect to use a statistical analysis method (e.g., probability plots or related tools) to establish a representative corrosion rate, remaining life estimate, and/or re-inspection date. **Any statistical approach shall be documented.** Care shall be taken to ensure the statistical treatment reflects a reasonably conservative representation of the various pipe components within the circuit.

### API 574 §7.3.4

Although a statistical analysis can be performed on any circuit, the results may be misleading unless the circuit is well defined. Refer to Annex C for a more detailed description.

```{important}
**Neither API 570 nor API 574 prescribe concrete methodologies of statistical analysis.** They contain loose verbiage allowing it, insisting on documentation and caution. The methodology is up to the analyst.
```

## Exchangeability

Before any pooled analysis, the CMLs in a group must be **exchangeable**. This is the central assumption that justifies treating them as draws from a common distribution.

```{epigraph}
A set of random variables is exchangeable if their joint distribution is unchanged by any permutation of their labels.
```

In plain terms: if you relabeled CML-007 as CML-042 and vice versa, would the analysis still be valid? If yes, they're exchangeable. If no — for example because CML-007 sits in a high-velocity zone and CML-042 is in a dead leg — they're not, and forcing them into the same population corrupts both.

### Why exchangeability matters

A frequentist fit to a non-exchangeable population produces a multi-modal distribution that no parametric family captures well. The Bayesian hierarchical models in chapter 5 require exchangeability *within each level* of the hierarchy — the CMLs are exchangeable *given* their feature type, but the feature types themselves are not exchangeable with each other.

### Practical check

Group your CMLs by:

- Material and heat treatment
- Process exposure (fluid composition, phase, temperature)
- Active damage mechanism
- Geometry and flow regime

Within each resulting group, the CMLs should be exchangeable. The 88-CML example circuit in chapters 3a and 4a groups by feature (NPS × schedule × component type), which is a reasonable first cut.

```{warning}
**Exchangeability is a modeling assumption, not a property of the data.** You're stating that the CMLs in a group are similar enough to share a common distribution. If that statement is wrong, all downstream inference is wrong.
```

## The frequentist workflow

```{figure} ../images/flow-frequentist.png
:name: flow-frequentist
:alt: Frequentist Workflow
:width: 700px
:align: center

General frequentist statistical workflow
```

Each step is iterative — testing a poor fit may send you back to clustering, cleaning, or even data collection.

## Data cleanup

Before any statistical analysis, prepare the dataset:

- **All readings, all corrosion rates** — preserve maximum information.
- **First and last readings** — for LTCR.
- **Taxonomical features** — NPS, schedule, component type.
- **Convert time to years since in-service** — allows comparing corrosion rates despite replacements.
- **Adjust as necessary** — e.g., CML → CMLX for reducing tees to keep data analysis consistent.
- **Identify out-of-place features and analyze separately** — SBC, dead legs, mix points.
- **Flags and problem areas** — from simpler upstream analysis.

## Exploratory data analysis

EDA is the first contact with cleaned data — visualize before modeling.

Standard EDA artifacts on inspection data:

- Scatterplots of thickness vs. time, colored by feature.
- Top-N corrosion rates table.
- Closest-to-$t_{\min}$ table.
- Histograms of corrosion rates (including and excluding growth readings).
- Boxplots of corrosion rate by feature.
- Short-term vs. long-term corrosion rate comparison.

```{figure} ../images/eda-scatter.png
:name: eda-scatter
:alt: EDA Scatterplot
:width: 700px
:align: center

The best place to start with analysis is with a scatterplot
```

## Feature clustering and distribution fitting

### Grouping criteria

| Variable | Group by |
|--|--|
| Thickness measurements | NPS, schedule, component type, replacements |
| Corrosion rates | NPS, component type, zone, orientation, outliers |


```{figure} ../images/4-STD-FIT_violin.png
:name: violinplot
:alt: Comparative Violin Plots
:width: 700px
:align: center

Violin plots between first and last readings can show the distribution and where some measurement error may be occurring. 
```

### Distribution fitting

Two main targets:

**Thickness:**

- First inspection (or one prior to current)
- Last inspection
- Corrosion rate can be inferred from thickness evolution if dates align.

**Corrosion rates:**

- Fit based on existing corrosion rates.
- STCR, LTCR, rates from nominal.
- Alternatively, rate between two selected points on distributions at two distinct points in time

```{note}
**You generally cannot fit until after clustering.** Mixing populations produces multi-modal distributions that no single parametric family fits well.
```

## Why Gamma (not Normal) for corrosion rates

The frequentist analysis in chapter 4 fits **Gamma** to corrosion rates and **Normal** to current thickness. Why?

### Physical reasoning

Corrosion rates have three properties that rule out the Normal:

1. **Strictly positive.** A real corrosion rate cannot be negative — negative rates in your dataset are measurement noise, not signal. The Normal distribution puts probability mass below zero, which is nonphysical.

2. **Right-skewed.** Most CMLs in a circuit corrode at a modest rate; a few corrode much faster due to local geometry, deposits, or flow-induced shear. The distribution has a long right tail.

3. **Bounded modes near zero.** Even in heavily corroding circuits, the most common rate tends to be relatively small, with the higher rates as rare outliers.

The Gamma distribution has all three:

- Support $(0, \infty)$.
- Naturally right-skewed (skewness $= 2/\sqrt{\alpha}$).
- Mode at $(\alpha - 1)\beta$ for $\alpha > 1$, typically near zero for inspection data.

### Why Normal is fine for thickness

Current thickness, in contrast:

- Is bounded by $t_{\text{nom}}$ above and $t_{\min}$ below, so it can't go negative in practice.
- Reflects the cumulative effect of many small corrosion events over decades, which by the CLT tends toward symmetry.
- Has measurement noise that is approximately Normal.

So Normal works for thickness *most of the time*. The exception is heavily corroded features where thickness becomes skewed toward $t_{\min}$ — chapter 4 shows this happens with 6" SCH40 FIT in the example, and a Skew-Normal or GEV fits better.

```{note}
**The fit follows the physics.** When a distribution choice doesn't work, ask what physical property of the data the candidate distribution is failing to capture. Negative values, hard bounds, skewness, and tail behavior are the usual culprits.
```

## Method of Moments for Gamma — full derivation

The MoM estimators for the Gamma are simple enough to derive by hand.

The Gamma distribution with shape $\alpha$ and scale $\theta$ has:

$$E[X] = \alpha\theta \qquad \text{Var}(X) = \alpha\theta^2$$

**Step 1 — Express the parameters in terms of moments.**

Divide variance by mean:

$$\frac{\text{Var}(X)}{E[X]} = \frac{\alpha\theta^2}{\alpha\theta} = \theta$$

So:

$$\theta = \frac{\text{Var}(X)}{E[X]}$$

And from $E[X] = \alpha\theta$:

$$\alpha = \frac{E[X]}{\theta} = \frac{E[X]^2}{\text{Var}(X)}$$

**Step 2 — Replace population moments with sample moments.**

$$\hat\theta = \frac{s^2}{\bar{x}} \qquad \hat\alpha = \frac{\bar{x}^2}{s^2}$$

That's it. Two summary statistics ($\bar{x}$ and $s^2$) give you both Gamma parameters. The whole derivation hinges on the convenient observation that variance/mean cleanly isolates $\theta$.

This is why MoM is fast and computationally simple — no optimization required, just compute two numbers from the data and divide.

```{warning}
MoM doesn't guarantee a sensible result if the data is small or contaminated. For Gamma, sample variance must be positive (always is for $n \ge 2$ with distinct values), but the resulting $\hat\alpha$ can be unreasonably small if the data has a lot of zeros or near-zeros. Use MoM as a **starting estimate**, then refine with MLE.
```

## Determine remaining life

Get the representative corrosion rate and minimum remaining thickness from the fitted distributions.

### Choosing the scenario

You must select which thickness and which corrosion rate to combine. **Worst $t$ × worst CR is generally over-conservative.**

| Scenario | Combination | Interpretation |
|--|--|--|
| **1** | mean $t$ × mean CR | The expected number |
| **2** | mean $t$ × worst CR | Typical TML in a corrosive zone |
| **3** | worst $t$ × mean CR | Worst TML in an average environment |
| **4** | worst $t$ × worst CR | The conservative estimate |

Scenario choice should reflect the **risk tolerance and physical reality** of the circuit. Use the worst case only where it's appropriate — e.g., at reducers before a pump, or specific tees with known aggressive damage.

```{note}
This is the core decision in frequentist remaining-life work. The Bayesian chapter shows how a hierarchical model can produce a more nuanced answer per-CML rather than asking you to pick one of four global scenarios.
```
