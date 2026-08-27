---
type: source
status: verified
area: [sources, mcmc, langevin, numerical-analysis]
source_type: paper
title: "Exponential Convergence of Langevin Distributions and Their Discrete Approximations"
author: "Gareth O. Roberts; Richard L. Tweedie"
year: 1996
url: "https://www.jstor.org/stable/3318418"
venue: "Bernoulli 2(4)"
accessed: 2026-08-25
source_tier: A
license: "论文元数据；本库仅保存独立摘要、必要公式与链接"
scope_role: foundational
temporal_role: foundational
related: ["[[Langevin、ULA、MALA 与平稳分布]]", "[[Predictor–Corrector 与 Score-based 生成程序]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Roberts–Tweedie：Langevin 扩散及其离散近似

> [!abstract] 来源定位
> 论文研究 Langevin diffusion、naive Euler discretization 与 Metropolis-adjusted chain 的收敛。对本卷最关键的反例是：连续扩散具有良好不变分布，并不保证 ULA 的粗步长链有同一平稳律，甚至不保证稳定遍历。

## 一维 Gaussian 校准例

对 $\pi=N(0,1)$，以

$$
X_{k+1}=X_k-\frac h2X_k+\sqrt h\,\xi_k
$$

作 ULA。当 $0<h<4$ 时它是 AR(1)，平稳方差为

$$
v_h=\frac{h}{1-(1-h/2)^2}=\frac1{1-h/4},
$$

一般不等于 1；$h\to0$ 才消除离散偏差。MALA 用非对称 proposal ratio 的 MH 接受率校正 invariant law，但接受拒绝会增加成本，且 mixing 仍需诊断。

