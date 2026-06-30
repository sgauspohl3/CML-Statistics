# Rules and Bayes' Theorem

From the axioms come the rules you use every day.

## The core rules

**Complement:** $P(A^c) = 1 - P(A)$

**Addition:** $P(A \cup B) = P(A) + P(B) - P(A \cap B)$

**Multiplication (independent events):** $P(A \cap B) = P(A) \cdot P(B)$

**Conditional probability:**

$$P(A \mid B) = \dfrac{P(A \cap B)}{P(B)}$$

**Law of total probability:** if $B_1, \ldots, B_n$ partition the sample space,

$$P(A) = \sum_i P(A \mid B_i) P(B_i)$$

## Bayes' theorem

The single most important formula in modern statistics:

$$P(A \mid B) = \frac{P(B \mid A)\,P(A)}{P(B)}$$

It tells you how to *update* your belief about $A$ after observing $B$. The prior $P(A)$ becomes the posterior $P(A \mid B)$, mediated by the likelihood $P(B \mid A)$.

```{code-cell} python
# Two dice — P(sum = 7)
import itertools

outcomes = list(itertools.product(range(1, 7), repeat=2))
favorable = [(a, b) for a, b in outcomes if a + b == 7]

print(f"P(sum=7) = {len(favorable)} / {len(outcomes)} = {len(favorable)/len(outcomes):.4f}")
```
