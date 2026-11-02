---
title: Loss Function
description: Deriving binary cross-entropy from the Bernoulli likelihood.
date: '2026-11-01'
kind: Course note
tags:
- CSE 447
- NLP
- logistic regression
categories:
- machine-learning
math: true
---

[← Logistic regression overview]({{ '/knowledge/logistic-regression/' | relative_url }})

A distance estimator between estimated output and true output
Difference is $$L(\hat y, y)=\text{how much }\hat y=\sigma(z)\text{ differs from the true }y\in\{0,1\}$$

---

## Cross-entropy loss
- Negative log likelihood loss
- A case of conditional maximum likelihood estimation, choosing parameters $$w,b$$ that maximizes the log probability of the true $$y$$ labels in the training data given the observation $$x$$

---

### Derivation

We want to **maximize the probability of the correct label** $$P(y\mid \mathbf x)$$.

Since there are only two possible outcomes, $$y\in\{0,1\}$$, we can express the probability using a **Bernoulli distribution**:

$$
P(y\mid \mathbf x)
=
\hat y^y(1-\hat y)^{1-y}
$$

This automatically selects the correct probability:

$$
P(y\mid\mathbf x)
=
\begin{cases}
\hat y & y=1\\
1-\hat y & y=0
\end{cases}
$$

Instead of maximizing the likelihood directly, we maximize the **log-likelihood**. Since $$\log$$ is strictly increasing, this has the same optimum:

$$
\begin{aligned}
\log P(y\mid\mathbf x)
&= \log\left[\hat y^y(1-\hat y)^{1-y}\right] \\
&= y\log\hat y+(1-y)\log(1-\hat y)
\end{aligned}
$$

It is conventional to formulate training as a **minimization** problem, so we negate the log-likelihood:

$$
\boxed{
L_{\text{CE}}(\hat y,y)
=
-\left[
y\log\hat y+(1-y)\log(1-\hat y)
\right]
}
$$

This is the **binary cross-entropy (negative log-likelihood) loss**.

Substituting

$$
\hat y=\sigma(w\cdot x+b)
$$

gives:

$$
\boxed{
L_{\text{CE}}
=
-\left[
y\log\sigma(w\cdot x+b)
+
(1-y)\log\left(1-\sigma(w\cdot x+b)\right)
\right]
}
$$
