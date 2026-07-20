# Discussion and References

## Comparing the Two Approaches

The two worked examples analyzed the **same SWS feed circuit** with the **same dataset**. The differences in the conclusions came from the methodology, not the data.

| Aspect | Frequentist | Bayesian |
|--|--|--|
| **Unit of analysis** | Feature-level distributions | Per-CML parameters with pooling |
| **Uncertainty** | Confidence intervals, scenario combinations | Full posterior distributions |
| **Prior knowledge** | Discarded (or implicit in scenario choice) | Explicitly encoded |
| **Worst-case behavior** | Globally applied → over-conservative | Per-CML; CMLs that look fine, look fine |
| **Computational cost** | Low — closed-form fitting | Higher — MCMC sampling |
| **Communication** | p-values and CIs | Posterior plots, credible intervals |
| **Diagnostics** | KS, AD, AIC/BIC | R̂, ESS, divergences, posterior predictive checks |

## When to Use Which

```{epigraph}
There's rarely one right answer. Knowing statistics doesn't give you the answer — it lets you ask better questions and pick a better analysis for the situation.
```

### Use Frequentist Methods When:

- The dataset is large enough that priors would barely matter.
- You need a quick screening analysis.
- The audience expects p-values and confidence intervals.
- The circuit is genuinely homogeneous and well-described by a single distribution.
- Computational resources or time are limited.

### Use Bayesian Methods When:

- You have meaningful prior knowledge (nominal thicknesses, expected corrosion rates from similar circuits, damage mechanism understanding).
- The dataset has very uneven sampling per CML (some CMLs with 60+ readings, some with 2).
- You need **per-CML** answers rather than population-level summaries.
- You want to combine information across CMLs without forcing the same answer on all of them.
- Communicating uncertainty in a defensible way matters.
- You're willing to invest in model specification and diagnostics.

### Use Both When:

- Auditors or standards bodies expect the traditional analysis.
- The Bayesian result is your real answer, and the frequentist analysis is the cross-check.
- Disagreements between the two tell you something useful about model specification or data quality.

## Limitations and Cautions

### Both Approaches Share Limitations

- **Statistical analysis cannot detect unknown unknowns.** If a damage mechanism wasn't sampled, no method can recover it.
- **Garbage in, garbage out.** Both methods assume the data is what it claims to be. Bad CML allocation, biased sampling, or measurement errors propagate through everything. Though Bayesian models can be contextualized to use bad data as long as you understand what is bad about the data.
- **Localized corrosion** that wasn't captured by sampling is invisible to both methods.
- **The model is not the territory.** Fitted parameters describe the data, not the underlying physics.

### Specific to Frequentist

- Picking the right scenario of thickness to corrosion rate is the crux of the entire method. Real circuits have varying levels of corrosivity that this approach cannot represent.
- Worst-case combinations are often unrealistic and not any more useful than the analysis a standard IDMS does.
- p-values are widely misinterpreted by audiences.

### Specific to Bayesian

- Prior specification is consequential and must be reasonable and educated. A bad prior is hard to recover from with little data.
- Convergence diagnostics are non-negotiable — undiagnosed sampler failure produces confidently wrong answers.
- Computational cost is higher; complex models can take hours to fit.
- The learning curve is steeper. Do you guys think you're ready yet?

## Recommendations for Practice

1. **Always document your method.** Both API 510 and API 570 require this. Methodology choices matter as much as numerical results.
2. **Match the analysis to the data.** A handful of readings per CML doesn't justify a complex hierarchical model; thousands of readings across a heterogeneous circuit doesn't justify a single-distribution fit.
3. **Visualize before modeling.** EDA catches data quality issues that no statistical method can.
4. **Report uncertainty, not just point estimates.** A remaining-life number without a credible or confidence interval is half a sentence.
5. **Cross-check.** Run a frequentist analysis as a sanity check on a Bayesian one (and vice versa). Disagreement is informative.
6. **Engage the SMEs.** Statistical analysis is a tool that supports engineering judgment, not a replacement for it.

## Common Mistakes — An Appendix

A field guide to errors I've seen in CML analyses, both my own and others'. Useful as a checklist when reviewing someone else's work.

### Mistake 1 — Dropping Growth Readings Without Flagging the Truncation

The most common silent error. An inspector or IDMS quietly discards readings thicker than the previous one, on the grounds that "wall doesn't grow." The dataset then contains only intervals where thickness went down, which is **truncation** (chapter 1).

The consequence: corrosion rate estimates are biased upward, often by 20-40%. Remaining life estimates are correspondingly too short. The circuit looks worse than it is.

**The fix:** include growth readings. The mean corrosion rate including growth intervals is the unbiased estimate. If you want to model only "true" corrosion, do it explicitly with a censored, mixture, or gamma model that you individually filter out instead of destroying valuable data - which that data is also useful for contextualizing measurement variability.

### Mistake 2 — Mean-Based Regression on a Dataset of Minima

A subtler version of the same problem. If the IDMS only stores the minimum reading per CML inspection (or you intentionally only report that), you have a sample of order statistics — not raw thicknesses. Applying mean-based regression methods to this sample gives systematically biased results.

**The fix:** match the statistical method to the reporting convention. Either record average readings and use mean-based methods, or record minima and use extreme value methods (Gumbel, GEV) designed for order statistics.

### Mistake 3 — Forcing a Single Distribution on a Multi-Modal Circuit

A circuit with three pipe sizes and two component types has six sub-populations. Forcing one Normal (or one Gamma) onto the combined data produces a multi-modal fit that no parametric family captures well. KS p-values come back terrible. The analyst increases the model complexity, when the right move is to cluster first and fit second.

**The fix:** cluster by feature before fitting. If the clustered sub-populations still don't fit, *then* reach for a richer distribution. Chapter 4 shows the pattern.

### Mistake 4 — Applying Worst-Case Scenarios Globally

Frequentist remaining-life analyses often produce a "worst $t$ × worst CR" scenario for each feature. Applying this to every CML in the feature group is over-conservative — most CMLs are nowhere near the worst-case combination. Doing this across a circuit produces inspection schedules with dozens of CMLs flagged for reinspection, and the analysis does not leave you in a better position had you not made the effort.

**The fix:** apply worst-case scenarios only where physically justified — reducers before pumps, locations with known aggressive damage mechanisms, anywhere with corroborating evidence. Use mean-case scenarios elsewhere. Better still, use a Bayesian per-CML analysis (chapter 6) that gives a tailored answer for each location.

### Mistake 5 — Treating Credible Intervals as Confidence Intervals (and Vice Versa)

A 94% **credible** interval (Bayesian) does say "there's a 94% probability the true value lies in this interval" — *given the prior and model*. A 95% **confidence** interval (frequentist) does NOT say this. It says "if we repeated the procedure, ~95% of intervals would contain the true value."

These are different statements with different practical implications. Confusing them in a report can mislead the audience badly.

**The fix:** know which you're reporting. If you used a Bayesian method, call it a credible interval. If you used a frequentist method, call it a confidence interval. If audience confusion is likely, briefly explain the distinction in the report.

### Mistake 6 — Reporting MCMC Results Without Convergence Diagnostics

A Bayesian analysis without R̂, ESS, or divergence counts is not trustworthy. Untreated convergence failures produce confidently wrong posteriors — the chains agree with each other but disagree with the truth, because they're all stuck in the same wrong region.

**The fix:** always report R̂ (target < 1.01), ESS (target > 400 per parameter), and divergence count (target zero). If divergences appear, fix them (non-centered parameterization, tighter priors, more warm-up) before publishing the result.

### Mistake 7 — Ignoring Exchangeability When Pooling

Hierarchical models assume the units being pooled are exchangeable. If you pool CMLs across different damage mechanisms — say, sulfidic corrosion with chloride SCC — you're forcing the model to find a common distribution for two physically distinct processes. The result is a posterior that fits neither well.

**The fix:** group by exchangeable units. CMLs within the same feature type, same process exposure, and same damage mechanism are exchangeable. CMLs across these boundaries are not.

### Mistake 8 — Confusing Statistical Significance with Practical Significance

A finding can be statistically significant ($p < 0.05$) and practically irrelevant (effect size 0.001 mpy). A finding can be statistically non-significant ($p = 0.12$) and practically critical (effect size 5 mpy, but only 6 data points). The p-value is about evidence strength, not effect magnitude.

**The fix:** always report effect sizes alongside p-values. In inspection work, the practical question is "how does this change remaining life?" — answer that, not just whether the change is significant.

### Mistake 9 — Over Trusting Fitted Distributions in the Tails

Most fitting methods optimize for the bulk of the data. A Normal fit might pass a KS test but still wildly underpredict the probability of an extreme observation. In inspection, the extreme is exactly what you care about — the thinnest CML, the highest corrosion rate.

**The fix:** look at Q-Q plots, which emphasize the tails. If the tail behavior is bad, try a heavier-tailed distribution (t, GEV, skew-Normal) or fall back on order-statistic methods.

### Mistake 10 — Treating the Analysis as the Answer

The deepest mistake. An analysis is not the answer, it is the start of the journey. A statistical analysis is an input to a decision, not the decision itself. The output of the chapter 6 Bayesian model is a per-CML posterior — what to *do* with that posterior (replace now, inspect again in 5 years, accept current state) depends on consequence, risk tolerance, and engineering judgment.

**The fix:** see the note on Bayesian decision theory at the end of chapter 5. The posterior is not the final answer; it's the input to whatever decision actually needs to be made.



### API Standards and Practices

- **API 510** — Pressure Vessel Inspection Code: In-service Inspection, Rating, Repair, and Alteration.
- **API 570** — Piping Inspection Code: In-service Inspection, Rating, Repair, and Alteration of Piping Systems.
- **API RP 571** — Damage Mechanisms Affecting Fixed Equipment in the Refining Industry.
- **API RP 574** — Piping Inspection Practices for Piping System Components.
- **API RP 580** — Risk-Based Inspection.
- **API RP 581** — Risk-Based Inspection Methodology.


### Statistics Texts

```{bibliography}
```

## Further Reading

- *Bayesian Modeling and Computation in Python* — Martin, Kumar, and Lao. Especially Chapter 1 for the workflow framing used in this course.
- *Statistical Rethinking* — McElreath. The single best book for building Bayesian intuition.
- *All of Statistics* — Wasserman. Compact, modern, mathematically serious frequentist reference.

## Acknowledgments

Course developed by Samuel Gauspohl (Accenture, Industry X) for the API Inspection and Mechanical Integrity Summit.

Linkedin: www.linkedin.com/in/samuel-gauspohl

<!--Contact: samuel.gauspohl@accenture.com-->
