---
type: source
status: draft
area: [sources, math/numerical-analysis]
source_type: course-notes
title: "Backwards Stability of Recursive Summation"
author: Steven G. Johnson
year: 2015
url: "https://math.mit.edu/~stevenj/18.335/summation-stability.pdf"
accessed: 2026-08-15
source_tier: A
license: "MIT 课程公开讲义；知识库仅保存独立摘要、推导映射与链接"
scope_role: worked-proof
temporal_role: foundational-teaching
aliases: [Johnson-2015-Recursive-Summation-Stability]
related: ["[[浮点数与舍入误差]]", "[[前向误差与后向误差]]", "[[数值稳定性]]"]
created: 2026-08-15
updated: 2026-08-15
---

# Johnson：递归求和的后向稳定性

> [!abstract] 来源定位
> 这份 MIT 18.335 两页讲义完整展示怎样“构造一组邻近输入，使浮点求和恰好等于其精确和”，并在 $1$ 范数下控制输入扰动。它是初学者学习后向分析证明结构的最小完整范例。

## 核心映射

| ID | 断言 | 纳入位置 |
|---|---|---|
| J1 | 后向分析需要先构造邻近输入，再证明其足够近 | [[前向误差与后向误差]]第十一节 |
| J2 | 递归求和可解释为对输入分量作小扰动后的精确求和 | 第十一节 |
| J3 | 证明选择 $1$ 范数可直接对应 $\sum_i|x_i|$ | 第十一节 |
| J4 | 输入先舍入到浮点集合时只增加同阶扰动项 | 第十一节与边界说明 |

## 视觉与文本核验

- 已渲染并目视检查 PDF 全部两页；
- 已确认邻近输入的构造、$1$ 范数估计和实数输入先舍入的扩展；
- 本章结合上一章的 $\gamma_n$ 语言重写结论，以便与求和条件数相乘。

## 生成节点

- [x] [[前向误差与后向误差]]

