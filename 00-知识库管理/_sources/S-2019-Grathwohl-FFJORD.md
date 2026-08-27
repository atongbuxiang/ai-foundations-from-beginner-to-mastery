---
type: source
status: verified
area: [sources, generative-models, continuous-normalizing-flows]
source_type: paper
title: "FFJORD: Free-form Continuous Dynamics for Scalable Reversible Generative Models"
author: "Will Grathwohl; Ricky T. Q. Chen; Jesse Bettencourt; Ilya Sutskever; David Duvenaud"
year: 2019
url: "https://arxiv.org/abs/1810.01367"
venue: "ICLR 2019"
accessed: 2026-08-25
source_tier: A
scope_role: foundational
temporal_role: foundational
related: ["[[Continuous Normalizing Flow、Liouville 与 FFJORD]]"]
created: 2026-08-25
updated: 2026-08-25
---
# Grathwohl et al.：FFJORD

> [!abstract] 来源定位
> CNF 将离散 $\log|\det J|$ 改成沿 ODE 的 divergence integral；FFJORD 用 Hutchinson estimator 近似 trace，放宽 triangular architecture。课程保留 solver error、trace variance、NFE 和 continuous/discrete adjoint gap。

$$\frac d{dt}\log p_t(z_t)=-\nabla\cdot f_\theta(z_t,t).$$

Hutchinson 对 trace 在 probe 随机性上无偏，不表示 ODE 解、参数梯度或最终 log-likelihood 在有限容差下无偏；“one-pass sampling”仍包含自适应 solver 的多次 vector-field evaluations。

