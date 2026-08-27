---
type: source
status: verified
area: [sources, generative-models, rectified-flow, optimal-transport]
source_type: paper
title: "Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow"
author: "Xingchao Liu; Chengyue Gong; Qiang Liu"
year: 2022
url: "https://arxiv.org/abs/2209.03003"
venue: "arXiv:2209.03003"
accessed: 2026-08-25
source_tier: A
license: "论文页面；本库仅保存独立摘要、必要公式与链接"
scope_role: foundational
temporal_role: foundational
related: ["[[Rectified Flow、ReFlow 与轨迹直化]]", "[[S-2023-Su-9497-构建ODE一般步骤下]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Liu et al.：Rectified Flow

> [!abstract] 来源定位
> 论文以端点 coupling 的直线插值和非线性最小二乘学习运输 ODE。其理论主张包括 rectification 产生具有相同端点边缘的确定性 coupling，并使 convex transport costs 不增加；递归 rectification（ReFlow）用于进一步直化。

## 课程调用

对 $(X_0,X_1)$ 的某个 coupling，设 $X_t=(1-t)X_0+tX_1$，回归目标为 $X_1-X_0$。population field 是条件平均，而非逐对端点速度的可逆索引。

## 三层结论

1. **路径设计**：teacher conditional segments 是直线；
2. **总体 ODE**：回归场保持所需 marginal evolution，并诱导新的 deterministic endpoint coupling；
3. **有限实现**：一阶 Euler 是否足够由 learned field 的沿轨迹变化、网络误差与训练结果共同决定。

论文报告近直轨迹和单步高质量是经验结果；不能把它改写为“Rectified Flow 理论上一 Euler 步总是精确”。
