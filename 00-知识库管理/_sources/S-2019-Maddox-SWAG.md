---
type: source
status: verified
area: [sources, bayesian-deep-learning, swag, posterior-predictive]
source_type: paper
title: "A Simple Baseline for Bayesian Uncertainty in Deep Learning"
author: [Wesley J. Maddox, Timur Garipov, Pavel Izmailov, Dmitry Vetrov, Andrew Gordon Wilson]
year: 2019
url: "https://proceedings.neurips.cc/paper_files/paper/2019/hash/118921efba23fc329e6560b27861f0c2-Abstract.html"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and approximation conditions"
venue: "NeurIPS 2019"
scope_role: primary
temporal_role: modern-method
related: ["[[Bayesian Posterior Predictive、Ensemble 与近似边界]]"]
created: 2026-08-23
updated: 2026-08-23
---

# A Simple Baseline for Bayesian Uncertainty in Deep Learning

> [!abstract] 来源定位
> 用 SGD 轨迹统计构造低秩加对角 Gaussian weight posterior approximation，并通过采样平均预测。本库调用 SWAG 的 approximation contract；不把局部 Gaussian 或 trajectory covariance 当作真实 posterior 的无条件恢复。

## 本库调用

1. SGD iterates 的均值与低秩协方差估计；
2. weight-space sample 到 function-space predictive mixture；
3. BatchNorm statistics 的重估属于推断协议；
4. Gaussian/local/subspace 假设限制多峰 posterior 表达；
5. 增加 samples 只降低 MC error，不消除近似偏差。
