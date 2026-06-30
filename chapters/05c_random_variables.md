# Random Variables

A **random variable (RV)** is a function mapping outcomes to numbers. It lets us do arithmetic with uncertainty.

## Discrete vs. continuous

**Discrete RV** — countable outcomes (dice roll, # of emails today).

- Described by a **PMF** (probability mass function): $P(X = x)$.

**Continuous RV** — uncountable outcomes (height, time, temperature).

- Described by a **PDF** (probability density function): $f(x)$.
- For continuous RVs, $P(X = x) = 0$ for any single $x$. Instead:

$$P(a \le X \le b) = \int_a^b f(x)\,dx$$

## The CDF works for both

The **cumulative distribution function** is defined for any RV:

$$F(x) = P(X \le x)$$

For discrete RVs it's a step function; for continuous RVs it's smooth.

## Expectation and variance

$$E[X] = \sum_x x\, p(x) \quad \text{or} \quad \int x f(x)\, dx$$

$$\text{Var}(X) = E[(X - E[X])^2]$$

The expectation is the long-run average; the variance measures how far typical values stray from it.
