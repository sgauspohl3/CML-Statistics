# Inspection Data and Analysis

## Inspection basics

The basic process of inspection and thickness data analysis follows a consistent sequence:

1. **Equipment info** — component types, nominal thicknesses, baseline info.
2. **CML selection** — damage mechanisms, representative locations, pipe size, accessibility.
3. **Data collection** — UT spot, UT grid, RT scans, variability, detection capability.
4. **Data analysis** — corrosion rate calculation, anomalies, outlier detection.
5. **Decision** — remaining life, next inspection date, replacement planning.

The downstream statistical analyses are only as good as the upstream sampling and data collection.

```{figure} ../images/flow-inspection.png
:name: flow-inspection
:alt: flow-inspection
:width: 700px
:align: center

General flow of inspection data
```

## Population and CML taxonomy

### Defining the population

CMLs in a circuit must be **exchangeable** — similar enough to compare and infer effectively.

Group by:

- Material & heat treatment
- Process fluid composition & phase
- Operating temperature and pressure
- Active damage mechanism(s)
- Flow regime & geometry

```{warning}
**Under-group** → multi-modal data, inflated variance, masks aggressive segments.

**Over-group** → small $n$ per circuit, wide uncertainty, limits pooled methods.
```

### CML & TML hierarchy

```{figure} ../images/cml-hierarchy.png
:name: cml-hierarchy
:alt: CML-hierarchy
:width: 700px
:align: center

Hierarchy from Circuit to Measurement Point. System would be above circuit.
```

### Why taxonomy matters

Reliable statistical analysis depends on understanding where data comes from. Proper taxonomy enables:

- Identification of corrosion patterns (uniform vs. localized)
- Detection of outliers and anomalies
- Correct grouping of data for population analysis
- Sub-population separation (NPS, component type)

::::{grid} 3
:gutter: 2

:::{grid-item}
```{figure} ../images/cml-hierarchy2.png
:name: cml-hierarchy2

CML Hierarchy Visual
```
:::

:::{grid-item}
```{figure} ../images/cml-taxonomy-azimuths.png
:name: cml-taxonomy-azimuths

Azimuths at clock positions
```
:::

:::{grid-item}
```{figure} ../images/cml-taxonomy-elbow-bands.png
:name: cml-taxonomy-elbow-bands

Common bands for an elbow
```
:::

:::{grid-item}
```{figure} ../images/cml-taxonomy-red-bands.png
:name: cml-taxonomy-red-bands

Common bands for a reducer
```
:::

:::{grid-item}
```{figure} ../images/cml-taxonomy-tees.png
:name: cml-taxonomy-tees

Types of tees
```
:::

:::{grid-item}
```{figure} ../images/cml-taxonomy-tee-bands.png
:name: cml-taxonomy-tee-bands

Common bands for a tee
```
:::

::::

### Data collection levels

- **Circuit level** — piping circuit ID, CML identification.
- **Component level** — pipe size (NPS), schedule (nominal thickness), component type.
- **Measurement level** — test point locations, multiple readings per CML.
- **Special programs** — injection/mix points, dead legs, high-risk zones.

## Sampling and recording

### What is recorded matters

| Recording method | Properties | Recommendation |
|--|--|--|
| **All readings** | Statistically richest. Preserves within-CML distribution. | **Preferred.** |
| **Average only** | Masks within-CML variance; dilutes real pits. | Avoid where possible. |
| **Minimum value** | Sample of order statistics, not raw thickness. | May need EVA instead of mean-based methods. |

```{important}
Match the statistical method to the reporting convention. Applying mean-based regression to a dataset of minima produces systematically biased results.
```

### Key objectives for effective sampling

- Multiple readings (MP) per TML.
- Multiple TMLs per CML.
- Reduces measurement noise.
- CV should be < 10% within TML.

```{warning}
Eliminating growth (thicker) readings in IDMS is a form of **truncation**. Including them reduces variance, excluding them increases it. This generally biases corrosion rate estimates upward.
```

### Worked example: computing the CV of a TML

Suppose at a single TML we take five UT readings:

| Reading | Thickness (in) |
|--|--|
| 1 | 0.286 |
| 2 | 0.291 |
| 3 | 0.288 |
| 4 | 0.282 |
| 5 | 0.293 |

**Step 1 — Compute the mean:**

$$\bar{x} = \frac{0.286 + 0.291 + 0.288 + 0.282 + 0.293}{5} = 0.288$$

**Step 2 — Compute the sample standard deviation:**

$$s = \sqrt{\frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar{x})^2}$$

The squared deviations:

| $x_i$ | $x_i - \bar{x}$ | $(x_i - \bar{x})^2$ |
|--|--|--|
| 0.286 | -0.002 | 0.000004 |
| 0.291 | +0.003 | 0.000009 |
| 0.288 | 0.000 | 0.000000 |
| 0.282 | -0.006 | 0.000036 |
| 0.293 | +0.005 | 0.000025 |

Sum = 0.000074. So:

$$s = \sqrt{\frac{0.000074}{4}} = \sqrt{0.0000185} \approx 0.0043$$

**Step 3 — Compute CV:**

$$\text{CV} = \frac{s}{\bar{x}} = \frac{0.0043}{0.288} \approx 0.015 = 1.5\%$$

**Step 4 — Compare against thresholds:**

- CV = 1.5% — well below the 10% rule of thumb. ✓ Pass.
- Maximum deviation: 0.006" — below the ±0.030" flag. ✓ Pass.
- Maximum % deviation: 2.1% — below the ±10% flag. ✓ Pass.

This TML is acceptable. If CV had exceeded 10%, the inspector would investigate: localized pitting, calibration issues, or improper probe placement.

```python
import numpy as np
readings = np.array([0.286, 0.291, 0.288, 0.282, 0.293])
m = readings.mean()
s = readings.std(ddof=1)
cv = s / m
print(f"Mean: {m:.4f}, SD: {s:.4f}, CV: {cv:.1%}")
```

```{exercise}
:label: cv-exercise

For a CML with the following five readings, compute the CV and decide whether it passes the 10% threshold.

| Reading | Thickness (in) |
|--|--|
| 1 | 0.245 |
| 2 | 0.242 |
| 3 | 0.248 |
| 4 | 0.240 |
| 5 | 0.243 |
```

```{solution} cv-exercise
:class: dropdown

Mean: $\bar{x} = 0.2436$

Sample SD: $s = \sqrt{\frac{1}{4}\sum(x_i - \bar{x})^2} \approx 0.00305$

CV: $s/\bar{x} \approx 1.25\%$ — well below 10%. **Pass.**
```

## CML allocation

### Approaches

| Approach | How it works | Sample size |
|--|--|--|
| **Rule-based** | CMLs allocated based on length, configuration, consequence, corrosion rates, etc. | Significant if random; smaller if biased. |
| **Damage mechanism based** | CMLs in "susceptible" areas where damage mechanisms are expected. | Smaller sample size required (biased locations, random measurements). |

```{epigraph}
Goal is NOT just data collection. Goal is to confirm damage mechanisms and detect risk before it leads to failure.
```

### Biased vs. random sampling

Sampling must represent the actual corrosion behavior of the piping circuit.

| Random sampling | Biased sampling |
|--|--|
| May miss damage zones | Focused on damage mechanisms |
| Can underestimate risk | Captures critical damage |
| No focus on worst-case | Targets high-risk locations |

## Variability in inspection

A major contribution to thickness data problems is variation at the examination point due to the entire measurement process.

```{figure} ../images/cml-variance.png
:name: cml-variance
:alt: CML Variance
:width: 700px
:align: center

Variance sources for a CML
```

### Sources of variability

- **Measurement method** — UT vs. RT.
- **Inspection approach** — spot vs. grid vs. scan.
- **Probe placement** — TP location variation.
- **Operator skill** — calibration and technique.
- **Local corrosion variation** — real non-uniform thinning.
- **Temperature effects** — elevated temp UT doubles standard deviation.

### Typical variability ranges

| Surface condition | Typical variability |
|--|--|
| Smooth surface, calibrated, trained operator | ±5–10 mils |
| Moderate field surface condition | ±10–20 mils |
| Rough/corroded surface | ±20–50 mils (≈ 4 yr of corrosion at 5 mil/yr) |

### Impact on analysis

High variability → noisy data → can hide:

- True onset of localized corrosion
- Real corrosion rate changes

Typical CV at a single test point: **~10%** — for 6" SCH40 pipe, this is ± 0.030".

## Inspection technique

### UT vs. RT — measurement methods

| Aspect | UT (Spot) | RT (Profile) |
|--|--|--|
| Coverage | Single point | Section profile / area |
| Precision | High (CV ~1–5%) | Lower (more variable min) |
| Localized corrosion | May miss pitting | Better detection |
| Speed | Fast | Slower, permits needed |
| Best for | General corrosion circuits | Localized / pitting corrosion |

UT Grid and UT Scan provide intermediate options — area coverage with quantitative readings.

```{important}
**Method → Data Quality → Analysis Validity.** The inspection method chosen determines baseline variability, the ability to detect localized damage, and the ability to size defects.
```

```{figure} ../images/cml-rt-variability.png
:name: cml-rt-variability
:alt: RT Variability
:width: 700px
:align: center

RT is great at capturing if corrosion is happening, but has high variability when it comes to measurement numbers
```

## Probability of detection

### Detection-limited vs. sizing-limited

- **Detection-limited** — point measurement; single transducer footprint. Worst feature may never be touched. Geometric POD dominates.
- **Sizing-limited** — full-coverage scan (PAUT C-scan, AUT). Feature is detected; measurement error is the dominant uncertainty.

```{figure} ../images/pod-replace.png
:name: pod-replace
:alt: POD
:width: 700px
:align: center

Probability of Detection of a damaged area
```

### Geometric POD — a sobering example

A 0.5" transducer on a 6" × 6" CML with a known 0.5" pit:

$$\text{POD} \approx \frac{\text{transducer area}}{\text{CML area}} = \frac{\pi (0.25)^2}{36} \approx 0.55\%$$

per single placement. Most of the surface is never sampled — this is what motivates **grid inspection** and **adequate sample size**.

### Inspection effectiveness categories (API RP 581)

| Category | Effectiveness | Confidence |
|--|--|--|
| A | Highly Effective | 80–100% |
| B | Usually Effective | 60–80% |
| C | Fairly Effective | 40–60% |
| D | Poorly Effective | 20–40% |
| E | Ineffective | < 20% |

## Basic analysis of thickness data

IDMS should be able to perform most basic analyses based on API standards.

### Point-to-point vs. circuit analysis

| Aspect | Point-to-Point | Circuit |
|--|--|--|
| Scope | Individual CML | Full dataset |
| Variability | Higher noise | Statistically smoothed |
| Outlier detection | Limited | Better via probability plots |
| Best for | Localized damage follow-up | General corrosion circuits |

### Corrosion rates

$$\text{CR} = \frac{t_{\text{prev}} - t_{\text{curr}}}{\Delta \text{years}} \quad \text{(inches/year)}$$

- **Short Term (STCR)** — last two readings; detects recent acceleration.
- **Long Term (LTCR)** — baseline to current; stable estimate for planning.

### Worked example: computing STCR and LTCR

A 6" SCH40 elbow has the following inspection history:

| Reading | Date | Thickness (in) |
|--|--|--|
| 1 (baseline) | 2008-03-15 | 0.280 |
| 2 | 2013-04-02 | 0.265 |
| 3 | 2018-05-10 | 0.247 |
| 4 | 2023-06-20 | 0.228 |

**Long-term corrosion rate** (baseline to current):

$$\text{LTCR} = \frac{t_1 - t_4}{\Delta t_{1\to4}} = \frac{0.280 - 0.228}{2023.5 - 2008.2} = \frac{0.052}{15.3} \approx 0.0034 \text{ in/yr} = 3.4 \text{ mpy}$$

**Short-term corrosion rate** (last two readings):

$$\text{STCR} = \frac{t_3 - t_4}{\Delta t_{3\to4}} = \frac{0.247 - 0.228}{2023.5 - 2018.4} = \frac{0.019}{5.1} \approx 0.0037 \text{ in/yr} = 3.7 \text{ mpy}$$

**Compare:**

$$\frac{\text{STCR}}{\text{LTCR}} = \frac{3.7}{3.4} = 1.09 = 109\%$$

This is below the 150% flag, so no immediate concern about acceleration. Both rates indicate the elbow has been corroding steadily at ~3.5 mpy over its life.

**Remaining life** to a $t_{\min}$ of 0.180:

$$\text{RL} = \frac{t_{\text{curr}} - t_{\min}}{\text{CR}} = \frac{0.228 - 0.180}{0.0034} \approx 14 \text{ years}$$

Per API 570, the next inspection is set to no later than half the remaining life:

$$\text{Next inspection} \le \frac{14}{2} = 7 \text{ years}$$

```python
import pandas as pd

readings = pd.DataFrame({
    'date': pd.to_datetime(['2008-03-15', '2013-04-02', '2018-05-10', '2023-06-20']),
    'thickness': [0.280, 0.265, 0.247, 0.228]
})
readings['years'] = (readings['date'] - readings['date'].iloc[0]).dt.days / 365.25

# LTCR: baseline to current
ltcr = (readings['thickness'].iloc[0] - readings['thickness'].iloc[-1]) / \
       (readings['years'].iloc[-1] - readings['years'].iloc[0])

# STCR: last two readings
stcr = (readings['thickness'].iloc[-2] - readings['thickness'].iloc[-1]) / \
       (readings['years'].iloc[-1] - readings['years'].iloc[-2])

print(f"LTCR: {ltcr*1000:.1f} mpy")
print(f"STCR: {stcr*1000:.1f} mpy")
print(f"STCR/LTCR: {stcr/ltcr:.0%}")
```

### Data quality flags

- Average of test points within exam point > ±10% or ±0.030"
- Current reading > 10% or > 0.020" from previous reading
- Band variation > ±12.5%
- STCR / LTCR > 150% (N/A for rates < 5 mpy)
- STCR > threshold (e.g., 15 mpy) — verify before acting

### Limiting component and next inspection

The **limiting component** is the CML with the shortest remaining life — it drives the interval for the whole circuit.

$$\text{Remaining Life} = \frac{t_{\text{actual}} - t_{\text{required}}}{\text{CR}}$$

$$\text{Next Inspection} \le \tfrac{1}{2} \times \text{Remaining Life} \quad \text{(API 570)}$$

Adjust based on risk class, data confidence, and variability (CV). **High CV → shorter interval.**
