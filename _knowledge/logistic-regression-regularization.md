---
title: Regularization
description: L1 and L2 penalties, sparsity, and regularized gradient updates.
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

**Purpose:** Reduce overfitting by penalizing model complexity, typically through large weights.
**Idea:** Prefer a model with smaller weights that generalizes better, even if its training loss is slightly higher.

---

## Objective
**Maximizing log-likelihood:**

$$
\boxed{
\hat\theta=\arg\max_\theta
\left[
\sum_{i=1}^{m}\log P(y^{(i)}\mid x^{(i)};\theta)
-\alpha R(\theta)
\right]
}
$$

**Equivalently, minimizing average loss:**

$$
\boxed{
\hat\theta=\arg\min_\theta
\left[
\frac{1}{m}\sum_{i=1}^{m}L_{\mathrm{CE}}^{(i)}
+\lambda R(\theta)
\right]
}
$$

Where:
- $$R(\theta)$$: regularization penalty
- $$\alpha,\lambda$$: regularization strengths
- Larger regularization strength $$\rightarrow$$ stronger penalty on weights
- The bias $$b$$ is typically excluded from regularization.

The coefficients depend on whether the data term is summed or averaged. For equivalent objectives, $$\alpha=m\lambda$$.

---

## L2 Regularization (Ridge)
**Definition:** Penalizes the sum of squared weights.

$$
\boxed{
R(w)=\|w\|_2^2=\sum_{j=1}^{n}w_j^2
}
$$

**Regularized objective:**

$$
J(w,b)=\frac{1}{m}\sum_{i=1}^{m}L_{\mathrm{CE}}^{(i)}
+\lambda\sum_{j=1}^{n}w_j^2
$$

**Properties:**
- Encourages smaller weights without usually forcing them to exactly zero.
- Smooth and differentiable, making gradient-based optimization straightforward.
- Can improve generalization and reduce sensitivity to individual features.

**Regularization gradient:**

$$
\frac{\partial}{\partial w_j}\lambda R(w)=2\lambda w_j
$$

---

## L1 Regularization (Lasso)
**Definition:** Penalizes the sum of absolute weights.

$$
\boxed{
R(w)=\|w\|_1=\sum_{j=1}^{n}|w_j|
}
$$

**Regularized objective:**

$$
J(w,b)=\frac{1}{m}\sum_{i=1}^{m}L_{\mathrm{CE}}^{(i)}
+\lambda\sum_{j=1}^{n}|w_j|
$$

**Properties:**
- Encourages **sparsity**: some weights become exactly zero.
- Performs implicit feature selection by eliminating some features.
- Not differentiable at $$w_j=0$$; sub-gradient or other suitable optimization methods can be used.

**Regularization gradient for $$w_j\neq0$$:**

$$
\frac{\partial}{\partial w_j}\lambda R(w)
=\lambda\operatorname{sign}(w_j)
$$

---

## Comparison

| Property          | L1 (Lasso)                          | L2 (Ridge)                  |
| ----------------- | ----------------------------------- | --------------------------- |
| Penalty           | $$\sum_j\lvert w_j\rvert$$            | $$\sum_j w_j^2$$              |
| Effect            | Pushes some weights to exactly zero | Shrinks weights toward zero |
| Sparsity          | Encourages sparse models            | Usually dense models        |
| Feature selection | Yes, implicitly                     | Generally no                |
| Differentiability | Not at zero                         | Everywhere                  |
| Typical use       | Many irrelevant features            | Many contributing features  |

**Key takeaway:**
- **Gradient Descent:** Determines how to update parameters.
- **Regularization:** Changes the objective being optimized.
- **L1:** Encourages sparse weights and feature selection.
- **L2:** Encourages small weights and smoother optimization.

**Gradient update with L2 regularization:**

$$
w_j\leftarrow w_j-\eta
\left[
\frac{\partial L_{\mathrm{data}}}{\partial w_j}
+2\lambda w_j
\right]
$$

The additional term $$2\lambda w_j$$ pulls weights toward zero during training.
