---
title: Scaling Input Features
description: Z-score standardization and min-max scaling for input features.
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

Spread of features could vary dramatically, necessary to normalize the features so its easier to learn the weight function

---

### Z-Score
For feature $$x_i$$:

$$
\mu_i = \frac{1}{m}\sum_{j=1}^{m} x_i^{(j)}
$$

$$
\sigma_i
=
\sqrt{
\frac{1}{m}
\sum_{j=1}^{m}
\left(x_i^{(j)}-\mu_i\right)^2
}
$$

Then scale:

$$
x_i' = \frac{x_i-\mu_i}{\sigma_i}
$$

- $$\mu_i$$: mean of feature $$i$$
- $$\sigma_i$$: standard deviation of feature $$i$$
- Result: feature has **mean $$0$$** and **standard deviation $$1$$**

---

### Min-Max Normalization

$$
x_i'
=
\frac{x_i-\min(x_i)}
{\max(x_i)-\min(x_i)}
$$

- Scales feature values to the range **$$[0,1]$$**
