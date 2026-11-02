---
title: Optimization Algorithms
description: Gradients, stochastic and mini-batch updates, and convexity.
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

Updates $$w$$ and $$b$$ to minimize the loss

---

## Gradient descent
**Goal:** Find the model parameters $$\theta$$ that minimize the average loss over all training examples.

- **Parameters:** $$\theta=(w,b)$$
- **Prediction:** $$\hat y=f(x;\theta)$$
- **Gradient:** A vector pointing in the direction of the greatest increase in a function.
- **Gradient Descent:** Calculate the gradient of the loss function at the current parameters and move in the opposite direction to minimize loss.

**Objective function:**

$$
\boxed{
\hat{\theta}=\underset{\theta}{\arg\min}\frac{1}{m}\sum_{i=1}^{m}L_{\mathrm{CE}}\left(f(x^{(i)};\theta),y^{(i)}\right)
}
$$

Where:
- $$m$$: number of training examples
- $$f(x^{(i)};\theta)=\hat y^{(i)}$$: model prediction
- $$y^{(i)}$$: true label
- $$L_{\mathrm{CE}}(\hat y,y)$$: cross-entropy loss
- $$\hat\theta$$: parameters that minimize average loss

---

### Gradient
For multidimensional parameters, the gradient is a vector of partial derivatives:

$$
\nabla_\theta L=
\begin{bmatrix}
\frac{\partial L}{\partial w_1}\\
\frac{\partial L}{\partial w_2}\\
\vdots\\
\frac{\partial L}{\partial w_n}\\
\frac{\partial L}{\partial b}
\end{bmatrix}
$$

- Each partial derivative measures how the loss changes with respect to one parameter, holding others constant.
- The gradient combines these partial derivatives into the direction of steepest increase.
- Moving opposite the gradient decreases the loss locally for a sufficiently small step.

**Parameter update:**

$$
\boxed{\theta_{t+1}=\theta_t-\eta\nabla_\theta L}
$$

- $$\eta$$: learning rate, a hyper-parameter controlling step size
- $$\nabla_\theta L$$: gradient evaluated at the current parameters

---

### Gradient for Logistic Regression
The partial derivatives for binary logistic regression simplify to:

$$
\boxed{
\begin{aligned}
\frac{\partial L_{\mathrm{CE}}}{\partial w_j}
&=[\sigma(w\cdot x+b)-y]x_j\\
&=(\hat y-y)x_j\\[6pt]
\frac{\partial L_{\mathrm{CE}}}{\partial b}
&=\hat y-y
\end{aligned}
}
$$

**Parameter updates for one training example:**

$$
\begin{aligned}
w_j &\leftarrow w_j-\eta(\hat y-y)x_j\\
b &\leftarrow b-\eta(\hat y-y)
\end{aligned}
$$

---

## Stochastic Gradient Descent
Instead of calculating the gradient over the entire dataset, update parameters using one training example at a time.

**Algorithm:**
1. Initialize parameters $$\theta$$.
2. Repeat until the stopping criterion is met:
   - Shuffle training examples.
   - For each training tuple $$(x^{(i)},y^{(i)})$$:
     1. Compute prediction: $$\hat y^{(i)}=f(x^{(i)};\theta)$$
     2. Optionally compute loss: $$L(\hat y^{(i)},y^{(i)})$$
     3. Compute gradient: $$g=\nabla_\theta L(f(x^{(i)};\theta),y^{(i)})$$
     4. Update parameters: $$\theta\leftarrow\theta-\eta g$$
1. Return $$\theta$$.
**Properties:**
- Computationally cheap per update.
- Frequent updates can make training progress quickly.
- Single-example gradients are noisy, resulting in choppy movements.
- A decreasing learning rate can help improve convergence.

---

### Batch vs. Mini-Batch vs. SGD

| Method | Examples per update | Characteristics |
|---|---|---|
| Batch Gradient Descent | Entire dataset | Stable gradient, expensive updates |
| Stochastic Gradient Descent | 1 example | Fast but noisy updates |
| Mini-Batch Gradient Descent | $$B$$ examples | Balances stability and efficiency |


**Mini-batch gradient:**

$$
g_B=\frac{1}{B}\sum_{i\in\mathcal B}\nabla_\theta L^{(i)}
$$

Where:
- $$\mathcal B$$: selected mini-batch
- $$B=|\mathcal B|$$: mini-batch size
Common batch sizes include 32, 64, 128, 512, and 1024.

---

### Convexity of Logistic Regression
For standard logistic regression, cross-entropy loss is **convex with respect to model parameters**.
- Every local minimum is a global minimum.
- The global minimizer is not necessarily unique.
- With linearly separable data and no regularization, a finite minimum may not exist.
- SGD can converge toward a global optimum under suitable conditions, but is not unconditionally guaranteed to find an exact minimum.
