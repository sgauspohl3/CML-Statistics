# Preface

A practical course on statistical analysis of Corrosion Monitoring Location (CML) data for mechanical integrity engineers.

These notes accompany the *CML Statistical Analysis* training session at the API Inspection and Mechanical Integrity Summit. The aim is to teach **just enough statistics** to apply it responsibly to inspection data — and then to walk through the actual workflow end-to-end on a real piping circuit, twice: once with frequentist methods, once with Bayesian.

```{epigraph}
Statistics without understanding leads to misuse; practice without theory leads to blind application.
```

The course balances theory and practice 50/50. Each chapter mixes intuition, mathematics, and runnable Python — the front matter helps you get the Python environment in place, the course proper builds the statistical foundation, and the worked-example chapters apply that foundation to a real SWS feed circuit.

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

# Foreword

*[Placeholder — replace with your own words.]*

This book grew out of a training session I lead at the API Inspection and Mechanical Integrity Summit, and out of a frustration I've had for years with how statistical analysis of inspection data is usually taught and practiced.

The frustration is this: most CML statistical analysis in industry is either a black box embedded in an IDMS, or a half-remembered application of techniques from a college statistics class. Neither produces engineers who can defend their numbers when an auditor asks how the retirement schedule was derived, or who can recognize when a method is being misapplied.

This course is my attempt to close that gap. The structure deliberately mirrors how I think about the problem in practice:

- Start with the statistical foundation — not as an exhaustive textbook, but as the working vocabulary an analyst actually needs.
- Move into the realities of inspection data — CML allocation, measurement variability, sampling decisions — because the statistics is downstream of those choices.
- Walk through a full frequentist analysis end-to-end on a real circuit, including the points where the methodology forces uncomfortable trade-offs.
- Repeat the same analysis Bayesian, on the same circuit, with the same data — and show how the answers shift.

I am not a statistician. I am a metallurgist who got tired of seeing inspection programs make poor decisions because the analysis layer was treated as a formality. If this course helps even a few engineers ask better questions of their data, it will have been worth the effort.

— Samuel Gauspohl