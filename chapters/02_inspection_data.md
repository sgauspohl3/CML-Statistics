# 2. Inspection Data and Analysis

## Inspection basics

The basic process of inspection and thickness data analysis follows a consistent sequence:

1. **Equipment info** — component types, nominal thicknesses, baseline info.
2. **CML selection** — damage mechanisms, representative locations, pipe size, accessibility.
3. **Data collection** — UT spot, UT grid, RT scans, variability, detection capability.
4. **Data analysis** — corrosion rate calculation, anomalies, outlier detection.
5. **Decision** — remaining life, next inspection date, replacement planning.

The downstream statistical analyses are only as good as the upstream sampling and data collection.

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
**Over-group** → multi-modal data, inflated variance, masks aggressive segments.

**Under-group** → small $n$ per circuit, wide uncertainty, limits pooled methods.
```

### CML & TML hierarchy

```
Piping Circuit
├── Line 1
│   ├── CML1
│   │   ├── TML1 → MP1, MP2, ...
│   │   ├── TML2 → MP1, MP2, ...
│   │   └── TML3 → MP1, MP2, ...
│   └── CML2
│       └── ...
└── Line 2
    └── ...
```

### Why taxonomy matters

Reliable statistical analysis depends on understanding where data comes from. Proper taxonomy enables:

- Identification of corrosion patterns (uniform vs. localized)
- Detection of outliers and anomalies
- Correct grouping of data for population analysis
- Sub-population separation (NPS, component type)

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

## Probability of detection

### Detection-limited vs. sizing-limited

- **Detection-limited** — point measurement; single transducer footprint. Worst feature may never be touched. Geometric POD dominates.
- **Sizing-limited** — full-coverage scan (PAUT C-scan, AUT). Feature is detected; measurement error is the dominant uncertainty.

### Geometric POD — a sobering example

A 0.5" transducer on a 6" × 6" CML with a known 0.5" pit:

$$\text{POD} \approx 1.1\% \text{ per single reading}$$

Most of the surface is never sampled — motivating grid inspection and adequate sample size.

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
