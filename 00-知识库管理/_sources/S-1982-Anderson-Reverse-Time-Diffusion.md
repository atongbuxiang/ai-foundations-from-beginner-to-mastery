---
type: source
status: verified
area: [sources, stochastic-processes, reverse-time, diffusion]
source_type: paper
title: "Reverse-time diffusion equation models"
author: "Brian D. O. Anderson"
year: 1982
url: "https://doi.org/10.1016/0304-4149(82)90051-5"
venue: "Stochastic Processes and their Applications 12(3):313–326"
accessed: 2026-08-25
source_tier: A
license: "出版页面；本库仅保存独立摘要、必要公式与链接"
scope_role: foundational
temporal_role: foundational
related: ["[[Reverse-time SDE、时间反演与 Score Drift]]", "[[S-2021-Song-Score-SDE]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Anderson：Reverse-time diffusion equation models

> [!abstract] 来源定位
> 这是 reverse-time diffusion 的经典一级来源之一。50.7 用它约束“时间反演”是过程级定理，而不是把 forward drift 的时间下标倒过来；现代 score-based 公式还需与 Song et al. 的记号、假设和生成方向逐项对齐。

## 课程调用

- 反向过程需由原过程的 transition/density 与 regularity 决定；
- state-independent isotropic diffusion 时，反向 drift 出现 $-g(t)^2\nabla\log p_t$（以 $t$ 从终点向起点积分的记法）；
- state-dependent diffusion 还会有扩散矩阵散度修正，不能套标量公式；
- 定理针对理想连续过程，不包含 learned-score error 或数值离散误差。

## 引用纪律

任何 reverse SDE 公式都必须同句声明时间变量的前进方向。若改用 $\tau=1-t$，先作 $dt=-d\tau$ 的变量替换，再写 drift；禁止一边用 $t:1\downarrow0$ 的公式，一边让 solver 以正步长按 $0\uparrow1$ 解释。
