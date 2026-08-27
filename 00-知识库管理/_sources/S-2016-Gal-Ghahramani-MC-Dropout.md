---
type: source
status: active
area: [sources, bayesian-deep-learning, mc-dropout, posterior-predictive]
source_type: paper
title: "Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning"
author: [Yarin Gal, Zoubin Ghahramani]
year: 2016
url: "https://proceedings.mlr.press/v48/gal16.html"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and approximation conditions"
venue: "ICML 2016"
scope_role: primary
temporal_role: modern-method
related: ["[[Dropout 的方差、共适应解释与 Bayesian 边界]]", "[[Bayesian Posterior Predictive、Ensemble 与近似边界]]"]
created: 2026-08-23
updated: 2026-08-24
---

# Dropout as a Bayesian Approximation

> [!abstract] 来源定位
> 把特定 dropout 训练/推断过程联系到近似 Bayesian inference，并用多次随机前向传播近似 predictive moments。本库调用其近似对象与 Monte Carlo 协议；不把任意带 dropout 网络都称为精确 posterior sampling。

## 本库调用

1. 近似 posterior family 与训练目标的关联；
2. test-time dropout 多次前向传播形成 Monte Carlo mixture；
3. 样本数控制 MC error，不修复 posterior approximation bias；
4. dropout rate、weight decay 与 likelihood precision 属于模型合同；
5. OOD、calibration 与 model misspecification 需要外部证据。
