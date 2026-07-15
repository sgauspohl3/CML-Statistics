# Introduction

This class is about democratizing statistics and cml analysis for mechanical integrity practitioners

A practical course on statistical analysis of Corrosion Monitoring Location (CML) data for mechanical integrity engineers.

These notes accompany the *CML Statistical Analysis* training session at the API Inspection and Mechanical Integrity Summit. The aim is to teach **just enough statistics** to apply it responsibly to inspection data — and then to walk through the actual workflow end-to-end on a real piping circuit, twice: once with frequentist methods, once with Bayesian.

```{epigraph}
Statistics without understanding leads to misuse; practice without theory leads to blind application.
```

The course balances theory and practice 50/50. Each chapter mixes intuition, mathematics, and runnable Python — the front matter helps you get the Python environment in place, the course proper builds the statistical foundation, and the worked-example chapters apply that foundation to a real SWS feed circuit.

## About the Author

Samuel Gauspohl is a cool dude, right?

```{image} ../images/headshot.png
:alt: This guy....
:width: 500px
:align: center
```


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


## About this class

This class balances **theory and practice** — just enough of each to build real understanding without overwhelming or over-simplifying.

```{epigraph}
Statistics without understanding leads to misuse; practice without theory leads to blind application.
```

```{image} ../images/class.png
:width: 500px
:align: center
```

### Theory (50%)

- Enough theory to understand the underlying concepts.
- Not so much that it becomes dry or difficult to follow.
- Covers: statistical distributions, probability, inference, model structure.

### Practical (50%)

- Enough examples and hands-on exercises to show concepts in action.
- Will not cover every possible scenario or edge case.
- Covers: Python walkthroughs, real inspection data, coded examples.

## Prerequisites and learning objectives

### Prerequisites

Foundational knowledge of the following is assumed:

- Refining and/or chemical processes
- Process equipment
- Inspection techniques
- Math
- Computer usage

### Learning objectives

By the end of the class, you should be able to:

- Understand basic statistical concepts used in CML analysis
- Use basic Python programming to conduct analysis
- Evaluate a circuit using frequentist methods
- Evaluate a circuit using Bayesian methods
- Understand a CML statistical analysis given to you

## The answer to everything in statistics: *it depends*

> *"What distribution should I fit?"* — Depends on the morphology, sample size, and goal.
>
> *"How many CMLs do I need?"* — Depends on the method, the variability, the risk you'll accept.
>
> *"Bayesian or frequentist?"* — Depends on what you know going in, and what you'll do with the answer.

There's rarely one right answer. Knowing statistics doesn't *give* you the answer — it lets you **ask better questions** and pick a better analysis for the situation.
