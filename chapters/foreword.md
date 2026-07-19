# Introduction

Welcome to the 2026 API Inspection and Mechanical Integrity Summit! I am glad you decided to take my class, and I hope you can get something out of it. These notes will provide additional context, information, and examples to better understand the concepts presented in this course. It is not required, and all this information will be available after the course as well. 

## About the Author

Samuel Gauspohl has worked a variety of roles focusing on mechanical integrity and reliability at several refinery and petrochemical facilities in the capacities of both owner-operator engineer and consultant. He has developed ground-up mechanical integrity programs and led multiple employers/clients to world class performance. Focus areas include: PSM, mechanical integrity, risk-based inspection, fitness for service, corrosion and damage mechanism assessments, inspection, and NDE. 

Samuel holds a BS degree in Materials Science and Engineering from Georgia Institute of Technology and current API 510, API 570, API 580, and API 653 certifications.

```{figure} ../images/headshot.png
:alt: This guy....
:width: 300px
:align: center

What a nerd...
```

## About This Class

This class is about democratizing statistics and CML analysis for mechanical integrity practitioners. There are many companies offering solutions in regards to CML optimization. They all perform some sort of analysis to determine what CMLs should be inspected at whichever date. This class should allow you to perform similat analyses, or at the very least, understand enough of the analysis to ask the right questions and direct the analysis. 

This course is focused primarily on the analysis aspect, and I do not want to go deep into the optimization, even though optimization is probably your end goal. Why? Well optimization is a discussion that all owner-operator mechanical integrity practitioners need to have about risk tolerance. Ultimately, this class cannot do the risk analysis for you, but it should give you some solid statistical background to bring actual insight to the risk discussion.

## Theory and Application

This class balances **theory and practice** — just enough of each to build real understanding without overwhelming or over-simplifying.


```{epigraph}
Statistics without understanding leads to misuse; practice without theory leads to blind application.
```

```{figure} ../images/class.png
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

This book assumes foundational knowledge of:

- Refining and/or chemical processes
- Process equipment
- Inspection techniques
- Math (algebra, basic calculus helps)
- Basic computer usage

### Learning objectives

By the end of this course you should be able to:

- Understand the basic statistical concepts
- Use basic Python to conduct analysis
- Evaluate a circuit using frequentist methods
- Evaluate a circuit using Bayesian methods
- Read and evaluate a CML statistical analysis someone else has produced


Pretty ambitious goals of this class, right? Well I'm an ambitious guy, so let's see how this goes. Strap in and enjoy the ride.

## The answer to everything in statistics: *It Depends*

This is going to be annoying, but 90% of the questions you may think about asking, especially when it comes to applying statistical concepts is, *it depends*. There is usually no one right answer, and there is usually more than one way to arrive at a similar answer. Analyses of the same data may lead to different answers. Knowing statistics doesn't *give* you the answer — it lets you **make more informed analyses** and pick better methods based on the available data or ask the right questions when receiving an analysis. 

> *"What distribution should I fit?"* — It Depends.
>
> *"How many CMLs do I need?"* — It Depends.
>
> *"Bayesian or frequentist?"* — You guessed it... It Depends.

Hopefully you guys won't get too annoyed at me whenever I answer that, *it depends*. Maybe one of you guys can make a tally and see how many times I say it. I just said it 6 times, so there's a head start.
