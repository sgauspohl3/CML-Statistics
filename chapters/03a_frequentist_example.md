# Example — Frequentist CML Analysis

A complete walkthrough of the frequentist workflow on a real piping circuit.

## The circuit: SWS feed

- Recently re-circuitized as the company switched from line-based to circuit-based inspections.
- Primarily **4" and 6" SCH40 carbon steel piping**, with a few SCH80 and SBC.
- Damage mechanisms of concern: **sour water corrosion (erosion)** and **ammonium bisulfide corrosion** in parts.
- SBCs and drain lines have already been removed for your convenience. 


### Supporting documents

#### P&ID

```{figure} ../images/PFD.png
:name: PFD1
:alt: PFD for Example
:width: 700px
:align: center

PFD of example
```

#### ISOs

```{raw} html
   <iframe src="../_static/isometric_gallery.html"
           width="100%" height="500"
           style="border:none;">
   </iframe>
```


The dataset used in this example is available for download:
<a href="../_static/TR_596-example2.xlsx" download>TR_596-example2.xlsx</a>

```{note}
The same circuit is reanalyzed in chapter 6 using Bayesian methods.
```

## Data cleanup

Create corrosion rates for all measurements by pairing each reading with its predecessor at the same TML.

```python
import pandas as pd

df = pd.read_excel(FILE, sheet_name='Readings')

# Keep only TMLs read more than once
counts = df.groupby('TML')['reading'].nunique()
df = df[df['TML'].isin(counts[counts > 1].index)].copy()

# Sort within each TML by reading number so .shift() lines up
df = df.sort_values(['TML', 'reading']).reset_index(drop=True)

# Previous reading's measurement & time within the same TML
df['prev_measurement'] = df.groupby('TML')['measurement'].shift(1)
df['prev_time']        = df.groupby('TML')['Time'].shift(1)
df['prev_reading']     = df.groupby('TML')['reading'].shift(1)

# Compute rate where we have a previous reading
rates = df.dropna(subset=['prev_measurement']).copy()
rates['delta_thickness'] = rates['measurement'] - rates['prev_measurement']
rates['delta_time']      = rates['Time'] - rates['prev_time']
rates['corrosion_rate']  = -1 * rates['delta_thickness'] / rates['delta_time']
```

## Exploratory data analysis

### Scatterplot of all readings vs. time

Color by feature to see whether populations behave differently:

```python
import seaborn as sns
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12, 7))
fig.patch.set_alpha(0)
sns.scatterplot(
    data=df,
    x='Time', y='measurement',
    hue='Feature',
    palette='tab10',
    s=22, alpha=0.5, edgecolor='none',
    ax=ax,
)
ax.set_xlabel('Time (years)')
ax.set_ylabel('Thickness')
ax.set_title(f'All thickness readings vs. time, by feature  (n={len(df)})')
ax.legend(title='Feature', bbox_to_anchor=(1.02, 1), loc='upper left')
plt.show()
```

```{figure} ../images/eda-scatter.png
:name: eda-scatter2
:alt: EDA Scatterplot
:width: 700px
:align: center

Scatterplot of all thickness readings
```

### Highest corrosion rate areas

```python
top10 = result.sort_values('corrosion_rate', ascending=False).head(10).reset_index(drop=True)
top10.to_excel('top10_corrosion.xlsx', index=False)
```

| TML | CML | Feature | Corrosion rate |
|--|--|--|--|
| 081.E.06 | 081 | 4" SCH40 FIT | 0.015213 |
| 081.E.03 | 081 | 4" SCH40 FIT | 0.014402 |
| 021.D.09 | 021 | 6" SCH40 FIT | 0.008557 |
| ... | ... | ... | ... |

### Lowest remaining thickness

```python
df['rca'] = df['measurement'] - df['t_min']
closest = df.sort_values('rca').head(20).reset_index(drop=True)
closest.to_excel('closest_to_tmin.xlsx', index=False)
```

Identifies CMLs already operating near retirement thickness.

### Histogram of all corrosion rates

```python
sns.histplot(data=result, x='corrosion_rate', kde=True, color='blue', alpha=0.6)
plt.show()
```

```{note}
**Including vs. excluding growth.** Growth readings (positive $\Delta t$) represent measurement variation, not true thickening. Excluding them is a form of truncation that biases corrosion rate estimates upward. Show both versions and discuss.
```

```python
# Drop growth intervals
n_before = len(rates_all)
n_growth = (rates_all['delta_thickness'] > 0).sum()
rates = rates_all[rates_all['delta_thickness'] <= 0].copy()

sns.histplot(data=rates, x='corrosion_rate', kde=True, color='blue', alpha=0.6)
plt.show()
```

## Feature clustering

Cluster by feature: combination of NPS, schedule, and component type.

| Feature | f_idx |
|--|--|
| 4" SCH40 PIPE | 1 |
| 4" SCH40 FIT | 2 |
| 6" SCH40 PIPE | 3 |
| 6" SCH40 FIT | 4 |
| 4" SCH80 PIPE | 5 |
| 4" SCH80 FIT | 6 |

Replot scatterplots and corrosion rate distributions by cluster. Also compare **LTCR vs. STCR** within each cluster.

## Determine representative corrosion rate(s)

### Boxplot by cluster

```python
order = rates.groupby('Feature')['corrosion_rate'].median().sort_values().index.tolist()

fig, ax = plt.subplots(figsize=(11, 6))
sns.boxplot(
    data=result,
    x='corrosion_rate',
    y='Feature',
    order=order,
    orient='h',
    palette='viridis',
    ax=ax,
)
ax.axvline(0, color='red', linestyle='--', linewidth=1, alpha=0.7, label='no change')
ax.set_xlabel('Corrosion rate (" / year)')
ax.set_ylabel('Feature')
ax.set_title('Corrosion rate distribution by feature')
plt.tight_layout()
plt.show()
```

### Normal fit per feature

```python
from scipy import stats

features = sorted(rates['Feature'].unique())
fits = []

fig, axes = plt.subplots(2, 3, figsize=(15, 9))
axes = axes.flatten()

for ax, feat in zip(axes, features):
    x = rates.loc[rates['Feature'] == feat, 'corrosion_rate'].to_numpy()
    n = len(x)
    mu = x.mean()
    sigma = x.std(ddof=1)
    ks_stat, ks_p = stats.kstest(x, 'norm', args=(mu, sigma))
    fits.append({'Feature': feat, 'n': n, 'mean': mu, 'sd': sigma,
                 'KS_stat': ks_stat, 'KS_p': ks_p})
    sns.histplot(x, bins=30, stat='density', alpha=0.55,
                 color='steelblue', edgecolor='black', ax=ax)
    x_line = np.linspace(x.min() - sigma, x.max() + sigma, 400)
    ax.plot(x_line, stats.norm.pdf(x_line, mu, sigma),
            color='red', linewidth=2, label='Normal fit')
plt.tight_layout()
plt.show()
```

```{warning}
**Normal is generally a poor fit** for corrosion rates. Rates are bounded below at zero and right-skewed — a Gamma fits much better.
```

### Gamma fit per feature

```python
for ax, feat in zip(axes, features):
    x = rates.loc[rates['Feature'] == feat, 'corrosion_rate'].to_numpy()
    n = len(x)
    # MLE for Gamma with location fixed at 0
    shape, loc, scale = stats.gamma.fit(x, floc=0)
    ks_stat, ks_p = stats.kstest(x, 'gamma', args=(shape, 0, scale))
    # plot ...
```

**Generally a good fit** for corrosion rate data.

### Gamma fit summary

| Feature | n | shape | scale | mode | median | p2.5 | p97.5 |
|--|--|--|--|--|--|--|--|
| 4" SCH40 FIT | 463 | 2.33 | 0.00114 | 0.00151 | 0.00228 | 0.000400 | 0.00696 |
| 4" SCH40 PIPE | 156 | 1.83 | 0.000852 | 0.000711 | 0.00129 | 0.000164 | 0.00450 |
| 4" SCH80 FIT | 74 | 4.95 | 0.000674 | 0.00266 | 0.00312 | 0.00108 | 0.00685 |
| 4" SCH80 PIPE | 30 | 1.82 | 0.000865 | 0.000707 | 0.00130 | 0.000163 | 0.00454 |
| 6" SCH40 FIT | 578 | 2.38 | 0.000986 | 0.00136 | 0.00202 | 0.000364 | 0.00613 |
| 6" SCH40 PIPE | 108 | 2.18 | 0.000573 | 0.000676 | 0.00106 | 0.000172 | 0.00337 |

## Determine representative minimum thickness

### Normal fit per feature (current thickness)

```python
features = sorted(current['Feature'].unique())
fits = []

for ax, feat in zip(axes, features):
    sub = current[current['Feature'] == feat]
    x = sub['measurement'].to_numpy()
    n = len(x)
    mu = x.mean()
    sigma = x.std(ddof=1)
    ks_stat, ks_p = stats.kstest(x, 'norm', args=(mu, sigma))
    # ...
```

**Normal is generally a good fit** for current thickness — except 6" SCH40 FIT, due to high corrosion. In that case, the corrosion-rate features (Gamma) will dominate the remaining-life answer.

### Fitting alternatives for 6" SCH40 FIT

Because of the heavy corrosion, no symmetric distribution fits perfectly. Compare candidates:

```python
candidates = {
    'Normal':      stats.norm,
    'Skew-Normal': stats.skewnorm,
    'GEV':         stats.genextreme,
    'Logistic':    stats.logistic,
    "Student's t": stats.t,
}

results = []
for name, dist in candidates.items():
    params = dist.fit(x)
    k_params = len(params)
    ll = np.sum(dist.logpdf(x, *params))
    aic = 2 * k_params - 2 * ll
    bic = k_params * np.log(n) - 2 * ll
    ks_stat, ks_p = stats.kstest(x, dist.name, args=params)
    p_below_tmin = dist.cdf(t_min, *params)
    results.append({
        'distribution': name, 'params': tuple(round(p, 5) for p in params),
        'logL': ll, 'AIC': aic, 'BIC': bic,
        'KS_stat': ks_stat, 'KS_p': ks_p,
        'P(t<t_min)': p_below_tmin,
    })
```

**Skew-Normal wins** on AIC/BIC. Still not a great fit — but the best of the candidates.

## Determine remaining life

Combine the four scenarios:

| Feature | RL₁: mean $t$, mean $r$ | RL₂: mean $t$, 97.5% $r$ | RL₃: 2.5% $t$, mean $r$ | RL₄: 2.5% $t$, 97.5% $r$ |
|--|--|--|--|--|
| 4" SCH40 FIT | 34.91 | 13.25 | 21.00 | 7.97 |
| 4" SCH40 PIPE | 61.21 | 21.26 | 44.64 | 15.50 |
| 4" SCH80 FIT | 50.23 | 24.45 | 37.36 | 18.19 |
| 4" SCH80 PIPE | 115.81 | 40.07 | 88.50 | 30.62 |
| 6" SCH40 FIT | 30.31 | 11.60 | 9.77 | 3.74 |
| 6" SCH40 PIPE | 60.63 | 22.48 | 36.11 | 13.39 |

## Applying the worst-case corrosion rate to each TML

If you naively apply the worst-case CR to every TML:

- **88 CMLs total**
- **40 would retire** by 2035

This is **unrealistic** since the majority of the circuit is not corroding substantially.

```{important}
**Only apply the worst case where appropriate** — such as at the reducers before the pump, and at some of the tees where conditions justify it. Blanket application of worst-case scenarios produces over-conservative retirement schedules that destroy program credibility.

This is the central tension of frequentist analysis on inspection data: you must pick a scenario, and that scenario applies globally to a population that is not actually homogeneous. The Bayesian chapter shows the alternative.
```
