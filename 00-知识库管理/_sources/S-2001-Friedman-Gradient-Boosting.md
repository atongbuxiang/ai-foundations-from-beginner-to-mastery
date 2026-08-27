---
type: source
status: active
area: [sources, learning-theory, gradient-boosting, function-space-optimization]
source_type: paper
title: "Greedy Function Approximation: A Gradient Boosting Machine"
author: [Jerome H. Friedman]
year: 2001
url: "https://doi.org/10.1214/aos/1013203451"
accessed: 2026-08-23
source_tier: A
license: "Annals of Statistics article; retain citation and independent derivations"
venue: "Annals of Statistics 29(5), 1189–1232"
scope_role: primary
temporal_role: classical-foundation
related: ["[[Bagging、Random Forest 与 Boosting]]", "[[一阶最优性条件与梯度下降]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Greedy Function Approximation: A Gradient Boosting Machine

> [!abstract] 来源定位
> Friedman 把 stagewise additive modeling解释为 function space 中的 steepest-descent approximation，使用 negative loss gradients 作为 pseudo-responses，并覆盖 squared、absolute、Huber 与 logistic criteria。它承担本库从 AdaBoost 特例进入一般 gradient boosting 的正式桥梁。

## 元数据与纳入

- 正式 DOI：[Project Euclid](https://doi.org/10.1214/aos/1013203451)；
- 正式引用：Friedman, J. H. (2001), *Annals of Statistics* 29(5), 1189–1232；
- 证据角色：functional gradient、pseudo-residual、line search、tree boosting、shrinkage/robust loss；
- 边界：finite-tree approximation、optimization path、statistical generalization 与 modern implementation regularizers必须分别说明。

## 本库调用的断言

1. gradient boosting 在当前 function estimate 上计算 negative empirical loss gradient；
2. base learner拟合 pseudo-residual 是对 functional descent direction 的 constrained approximation；
3. squared loss下 pseudo-residual等于 ordinary residual；
4. learning rate、tree depth、subsampling 与 stopping共同定义 estimator；
5. training loss下降不自动给 test-risk guarantee。
