---
type: source
status: verified
area: [sources, optimization, stochastic-processes]
source_type: paper
title: "Stochastic Gradient Descent as Approximate Bayesian Inference"
author: [Stephan Mandt, Matthew D. Hoffman, David M. Blei]
year: 2017
url: "https://jmlr.org/papers/v18/17-214.html"
accessed: 2026-08-26
source_tier: A
license: "JMLR article, CC BY 4.0"
venue: "JMLR 18(134):1–35"
scope_role: primary
related: ["[[梯度噪声协方差、Noise Scale 与 SDE 近似]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Mandt、Hoffman、Blei 2017：SGD 的局部随机过程近似

> [!abstract] 来源定位
> 论文在常学习率、局部二次损失与近似平稳噪声等假设下，把 SGD 近似为 Ornstein–Uhlenbeck 过程并讨论近似 Bayesian inference。课程调用 diffusion scaling 和 Lyapunov covariance equation，同时把“SGD 就是 posterior sampler”保留为强条件下的近似解释。

## 课程调用

- $t=k\eta$ 时间缩放下，diffusion 振幅随 $\sqrt{\eta/B}$ 变化；
- 局部二次模型的 stationary covariance；
- learning rate、batch size、curvature 与 noise covariance 的联合影响；
- 连续近似的误差来源。

## 必须保留的条件

常/缓变 learning rate、足够小步长、局部二次近似、噪声矩有限且近似平稳、Markov/diffusion 近似可接受。深网全程、无放回采样、强非 Gaussian 噪声与跨 basin 跃迁不能由局部 OU 模型自动覆盖。

