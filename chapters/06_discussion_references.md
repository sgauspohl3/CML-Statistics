# 6. Discussion and References

## Comparing the two approaches

The two worked examples analyzed the **same SWS feed circuit** with the **same dataset**. The differences in the conclusions came from the methodology, not the data.

| Aspect | Frequentist | Bayesian |
|--|--|--|
| **Unit of analysis** | Feature-level distributions | Per-CML parameters with pooling |
| **Uncertainty** | Confidence intervals, scenario combinations | Full posterior distributions |
| **Prior knowledge** | Discarded (or implicit in scenario choice) | Explicitly encoded |
| **Output for remaining life** | Four scenarios × 6 features = 24 numbers | Per-CML credible intervals (88 CMLs) |
| **Worst-case behavior** | Globally applied → over-conservative | Per-CML; CMLs that look fine, look fine |
| **Computational cost** | Low — closed-form fitting | Higher — MCMC sampling |
| **Communication** | p-values and CIs | Posterior plots, credible intervals |
| **Diagnostics** | KS, AD, AIC/BIC | R̂, ESS, divergences, posterior predictive checks |

## When to use which

```{epigraph}
There's rarely one right answer. Knowing statistics doesn't give you the answer — it lets you ask better questions and pick a better analysis for the situation.
```

### Use frequentist methods when:

- The dataset is large enough that priors would barely matter.
- You need a quick screening analysis.
- The audience expects p-values and confidence intervals.
- The circuit is genuinely homogeneous and well-described by a single distribution.
- Computational resources or time are limited.

### Use Bayesian methods when:

- You have meaningful prior knowledge (nominal thicknesses, expected corrosion rates from similar circuits, damage mechanism understanding).
- The dataset has very uneven sampling per CML (some CMLs with 60+ readings, some with 2).
- You need **per-CML** answers rather than population-level summaries.
- You want to combine information across CMLs without forcing the same answer on all of them.
- Communicating uncertainty in a defensible way matters.
- You're willing to invest in model specification and diagnostics.

### Use both when:

- Auditors or standards bodies expect the traditional analysis.
- The Bayesian result is your real answer, and the frequentist analysis is the cross-check.
- Disagreements between the two tell you something useful about model specification or data quality.

## Limitations and cautions

### Both approaches share limitations

- **Statistical analysis cannot detect unknown unknowns.** If a damage mechanism wasn't sampled, no method can recover it.
- **Garbage in, garbage out.** Both methods assume the data is what it claims to be. Bad CML allocation, biased sampling, or measurement errors propagate through everything.
- **Localized corrosion** that wasn't captured by sampling is invisible to both methods.
- **The model is not the territory.** Fitted parameters describe the data, not the underlying physics.

### Specific to frequentist

- The four-scenario approach forces a global choice. Real circuits have varying levels of corrosivity that this approach cannot represent.
- Worst-case combinations are often unrealistic and erode program credibility.
- p-values are widely misinterpreted by audiences.

### Specific to Bayesian

- Prior specification is consequential and must be defensible. A bad prior is hard to recover from with little data.
- Convergence diagnostics are non-negotiable — undiagnosed sampler failure produces confidently wrong answers.
- Computational cost is higher; complex models can take hours to fit.
- The learning curve is steeper.

## Recommendations for practice

1. **Always document your method.** Both API 510 and API 570 require this. Methodology choices matter as much as numerical results.
2. **Match the analysis to the data.** A handful of readings per CML doesn't justify a complex hierarchical model; thousands of readings across a heterogeneous circuit doesn't justify a single-distribution fit.
3. **Visualize before modeling.** EDA catches data quality issues that no statistical method can.
4. **Report uncertainty, not just point estimates.** A remaining-life number without a credible or confidence interval is half a sentence.
5. **Cross-check.** Run a frequentist analysis as a sanity check on a Bayesian one (and vice versa). Disagreement is informative.
6. **Engage the SMEs.** Statistical analysis is a tool that supports engineering judgment, not a replacement for it.

## References

### API standards

- **API 510** — Pressure Vessel Inspection Code: In-service Inspection, Rating, Repair, and Alteration.
- **API 570** — Piping Inspection Code: In-service Inspection, Rating, Repair, and Alteration of Piping Systems.
- **API RP 571** — Damage Mechanisms Affecting Fixed Equipment in the Refining Industry.
- **API RP 574** — Piping Inspection Practices for Piping System Components.
- **API RP 580** — Risk-Based Inspection.
- **API RP 581** — Risk-Based Inspection Methodology.
- **API RP 653** — Tank Inspection, Repair, Alteration, and Reconstruction.

### Gysbers Inspectioneering articles

A.C. Gysbers, *A Discussion on the Piping Thickness Management Process*, Inspectioneering Journal:

- Part 1 — Overview (Sep/Oct 2012)
- Part 2 — Determining Corrosion Monitoring Locations (Nov/Dec 2012)
- Part 3 — Data Collection with Ultrasonics and Radiography (Jan/Feb 2013)
- Part 4 — Collecting Quality Thickness Data (May/Jun 2013)
- Part 5 — Circuit Thickness Data Analysis (Sep/Oct 2013)

A.C. Gysbers, *Recording Thickness Data During Thickness Monitoring Inspections*, Inspectioneering Journal (Sep/Oct 2015).

### Statistics texts

```{bibliography}
```

### Patents

- Sparago, US 12,007,227 B2 — relevant prior art for statistical CML analysis.

## Further reading

- *Bayesian Modeling and Computation in Python* — Martin, Kumar, and Lao. Especially Chapter 1 for the workflow framing used in this course.
- *Statistical Rethinking* — McElreath. The single best book for building Bayesian intuition.
- *All of Statistics* — Wasserman. Compact, modern, mathematically serious frequentist reference.

## Acknowledgments

Course developed by Samuel Gauspohl (Accenture, Industry X) for the API Inspection and Mechanical Integrity Summit.

Contact: samuel.gauspohl@accenture.com
