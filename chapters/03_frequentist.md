# 3. Frequentist Statistical Analysis

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

## The frequentist workflow

```
Start
  ↓
Compile / Clean Data
  ↓
Exploratory Data Analysis (EDA)
  ↓
Fit Distribution to Data
  ↓
Test
  ↓
Accept / Reject
  ↓
End
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

## Feature clustering and distribution fitting

### Grouping criteria

| Variable | Group by |
|--|--|
| Thickness measurements | NPS, schedule, component type, replacements |
| Corrosion rates | NPS, component type, zone, orientation, outliers |

### Distribution fitting

Two main targets:

**Thickness:**

- First inspection (or one prior to current)
- Last inspection
- Corrosion rate can be inferred from thickness evolution if dates align.

**Corrosion rates:**

- Fit based on existing corrosion rates.
- STCR, LTCR, rates from nominal.

```{note}
**You generally cannot fit until after clustering.** Mixing populations produces multi-modal distributions that no single parametric family fits well.
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
