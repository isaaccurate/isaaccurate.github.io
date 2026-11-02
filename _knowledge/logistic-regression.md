---
title: Logistic Regression
description: Binary and multiclass classification with sigmoid and softmax models.
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

$$
\hat c=\arg\max_{c\in C}P(c|d)
$$

$$P(c\mid d)$$ is the posterior

**Input**: document $$d$$ and a fixed set of classes $$C=\{c_1,c_2,\dots,c_j\}$$

**Output**: predicted class $$\hat y\in C$$

Baseline supervised ML tool for classification and the foundation of neural networks and an important analytic tool in natural and social sciences

---

## Learning the Weights
- Need to find $$w$$ and $$b$$ to minimize the distance between our estimate $$\hat y^i$$ and true $$y^i$$
- [Loss Function]({{ '/knowledge/logistic-regression-loss/' | relative_url }})
- [Optimization Algorithms]({{ '/knowledge/logistic-regression-optimization/' | relative_url }})
- [Scaling Input Features]({{ '/knowledge/logistic-regression-feature-scaling/' | relative_url }})
- [Regularization]({{ '/knowledge/logistic-regression-regularization/' | relative_url }})

---

## Binary Classification
Given input/output pairs: $$(x^i,y^i)$$

**Input**: observation $$x^i$$ represented by a feature vector $$\{x_1,x_2,\dots,x_n\}$$

**Weights**: for each feature $$x^i$$ we have a corresponding weight $$w_i$$ indicating importance of $$x_i$$

**Output**: predicted class $$\hat y^i\in\{0,1\}$$

$$
z=(\sum^n_{i=1}w_ix_i)+b=w\cdot x+b
$$

Pass $$z$$ through the sigmoid/logistic function to get a probability as the output

$$
P(y=1)=\sigma(z)=\frac{1}{1+e^{-z}}=\frac{1}{1+\exp(-z)}
$$

$$
P(y=0)=1-\sigma(z)=1-\frac{1}{1+e^{-z}}=\frac{\exp(-z)}{1+\exp(-z)}
$$

Turn the probability into a classifier where $$0.5$$ here is called the **decision boundary**

$$
\hat{y} =
\begin{cases}
1 & \text{if } P(y=1\mid x) > 0.5&&\text{if $z>0$} \\
0 & \text{otherwise}&&\text{if $z\leq0$}
\end{cases}
$$

---

## Multinomial Logistic Regression
We use multinomial logistic regression if we have more than 2 classes
Probability of everything must still sum to 1

Uses a different classification function: **softmax** function
- Takes a vector $$z=[z_1,z_2,\dots,z_k]$$ of $$k$$ arbitrary values where each dimension represents a class
- Outputs a probability distribution
- Each value in the range $$[0,1]$$ where all values sum up to 1

**Gold labels**:

$$
[0,0,\dots,1,0,0]
$$

**Predicted values**:

$$
[0.1, 0.05,\dots,0.08,0,0.07]
$$

**Softmax**:

$$
\text{softmax}(z_i)=\frac{e^{z_i}}{\sum^k_{j=1}e^{z_j}}
$$

where $$1\leq i \leq k$$, the denominator normalizes all values into probabilities
