# CML Statistical Analysis

A practical course on statistical analysis of Corrosion Monitoring Location (CML) data for mechanical integrity engineers.

These notes accompany the *CML Statistical Analysis* training session at the API Inspection and Mechanical Integrity Summit. The aim is to teach **just enough statistics** to apply it responsibly to inspection data — and then to walk through the actual workflow end-to-end on a real piping circuit, twice: once with frequentist methods, once with Bayesian.

## How this book is organized

```{epigraph}
Statistics without understanding leads to misuse; practice without theory leads to blind application.
```

Six chapters, balanced 50/50 between theory and applied practice:

1. **Introduction and Setup** — what to expect, prerequisites, learning objectives, and getting your Python environment running.
2. **Statistics Refresher** — descriptive statistics, probability, distributions, inference, hypothesis testing, censoring/truncation.
3. **Inspection Data and Analysis** — CML taxonomy, sampling, variability, inspection techniques, probability of detection, and basic IDMS analysis.
4. **Frequentist Statistical Analysis** — the classical workflow: data cleanup, EDA, clustering, distribution fitting, remaining life. With a full worked example on an SWS feed circuit.
5. **Bayesian Statistical Analysis** — Bayes' theorem, MCMC, hierarchical pooling, NumPyro workflow, diagnostics. With the same SWS feed circuit reanalyzed Bayesian.
6. **Discussion and References** — comparing approaches, when to use which, and where to read further.

## Prerequisites

This book assumes foundational knowledge of:

- Refining and/or chemical processes
- Process equipment
- Inspection techniques
- Math (algebra, basic calculus helps)
- Computer usage

## Learning objectives

By the end you should be able to:

- Understand the basic statistical concepts used in CML analysis
- Use basic Python to conduct analysis
- Evaluate a circuit using frequentist methods
- Evaluate a circuit using Bayesian methods
- Read and critically evaluate a CML statistical analysis someone else has produced
