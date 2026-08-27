---
type: source
status: verified
area: [sources, automatic-differentiation, second-order-methods]
source_type: paper
title: "Fast Exact Multiplication by the Hessian"
author: [Barak A. Pearlmutter]
year: 1994
url: "https://doi.org/10.1162/neco.1994.6.1.147"
accessed: 2026-08-23
source_tier: A
venue: "Neural Computation 6(1):147–160"
scope_role: primary
temporal_role: foundational
related: ["[[Gradient Checking、Checkpointing 与高阶微分边界]]", "[[Hessian、二阶微分与曲率]]", "[[Hessian-vector Product、共轭梯度与隐式二阶步]]"]
created: 2026-08-23
updated: 2026-08-23
---
# Pearlmutter 1994：Fast Exact Hessian–Vector Products
> [!abstract] 来源定位
> 不物化 Hessian 而计算 $Hv$ 的经典原始论文。其 $R$-operator/方向传播观点是当代 forward-over-reverse HVP 的理论核心。本库保留“快速精确”的限定：精确指链式法则而非无浮点误差，快速是相对 full Hessian materialization 的复杂度结构。
