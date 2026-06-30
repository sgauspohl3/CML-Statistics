# Properties of Estimators

What makes one estimator better than another? Four standard criteria.

## The four properties

**Unbiased:** $E[\hat\theta] = \theta$. On average, the estimator hits the true value.

**Consistent:** $\hat\theta \to \theta$ as $n \to \infty$. With enough data, the estimator converges to the truth.

**Efficient:** low variance compared to other unbiased estimators. Among the unbiased options, this one is the most precise.

**Robust:** not overly sensitive to outliers or assumption violations.

## The bias–variance tradeoff

These properties can conflict. A slightly biased estimator with much lower variance often produces better overall predictions than an unbiased high-variance one.

The mean squared error decomposes cleanly:

$$\text{MSE} = \text{bias}^2 + \text{variance}$$

This is the central insight behind regularization, ridge regression, shrinkage estimators, and most of modern machine learning. Accepting a little bias to win a lot of variance is often the right trade.
