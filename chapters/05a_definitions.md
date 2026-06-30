# Definitions

The basic vocabulary:

- **Experiment** — a process with uncertain outcome (rolling a die).
- **Sample space ($\Omega$)** — set of all possible outcomes ($\{1,2,3,4,5,6\}$).
- **Event ($A$)** — a subset of the sample space ("even" = $\{2,4,6\}$).
- **Probability $P(A)$** — a number in $[0, 1]$ expressing how likely $A$ is.

## Kolmogorov's axioms

All of probability rests on three axioms:

1. $P(A) \ge 0$ for any event $A$.
2. $P(\Omega) = 1$ — something must happen.
3. For disjoint events: $P(A \cup B) = P(A) + P(B)$.

Everything else — conditional probability, Bayes' theorem, expectation, the central limit theorem — follows from these three rules and a bit of measure theory.
