---
type: source
status: verified
area: [sources, optimization, tensor-preconditioning]
source_type: paper
title: "Shampoo: Preconditioned Stochastic Tensor Optimization"
author: [Vineet Gupta, Tomer Koren, Yoram Singer]
year: 2018
url: "https://proceedings.mlr.press/v80/gupta18a.html"
venue: "ICML 2018, PMLR 80:1842–1850"
accessed: 2026-08-26
source_tier: A
scope_role: primary
temporal_role: foundational
related: ["[[Shampoo、逆矩阵根与 Kronecker 预条件]]", "[[SOAP、二阶混合优化器与成本证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Gupta–Koren–Singer：Shampoo

> [!abstract] 来源定位
> Shampoo 的原始算法与 stochastic-convex 分析来源。它保留 tensor shape，为每个 mode 累计一个 Gram preconditioner；矩阵/张量根、指数和左右作用必须按 rank 与 convention 明确。

## 课程采用

对矩阵 gradient $G_t\in\mathbb R^{m\times n}$，二阶统计可写

$$
L_t=\epsilon I_m+\sum_{s\le t}G_sG_s^T,\qquad
R_t=\epsilon I_n+\sum_{s\le t}G_s^TG_s.
$$

经典矩阵更新使用左右 inverse fourth roots $L_t^{-1/4}G_tR_t^{-1/4}$；两侧组合产生整体 half-power 效果。高阶 tensor 的 mode 指数依 rank 调整。原论文的 convex regret、实验 per-step 成本与当代 distributed implementation 必须分开陈述。
