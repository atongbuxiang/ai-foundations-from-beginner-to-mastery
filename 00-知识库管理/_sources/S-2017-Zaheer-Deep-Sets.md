---
type: source
status: draft
area: [sources, architecture/sets, invariance]
source_type: paper
title: "Deep Sets"
author: "Manzil Zaheer, Satwik Kottur, Siamak Ravanbakhsh, Barnabas Poczos, Ruslan Salakhutdinov, Alexander J. Smola"
year: 2017
url: "https://proceedings.neurips.cc/paper/2017/hash/f22e4747da1aa27e363d86d40ff442fe-Abstract.html"
accessed: 2026-08-24
source_tier: A
scope_role: primary
related: ["[[图数据、节点重标号与置换对称性]]", "[[图级读出、异构图与任务接口]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Zaheer 等：Deep Sets

> [!abstract] 来源定位
> 给出集合输入的 permutation-invariant / equivariant 结构，是邻居聚合与图级 readout 的集合函数接口来源。

## 课程使用纪律

典型不变形式为 $\rho(\sum_{x\in X}\phi(x))$。课程只在相应定义域、连续性/可数性与容量假设下调用表示结论；不把“sum 架构”写成对任意无界多重集、有限宽网络都无条件精确的万能定理。

