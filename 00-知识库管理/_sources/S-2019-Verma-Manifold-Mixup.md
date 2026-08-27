---
type: source
status: draft
area: [sources, neural-networks, manifold-mixup, representation-geometry]
source_type: paper
title: "Manifold Mixup: Better Representations by Interpolating Hidden States"
author: "Vikas Verma; Alex Lamb; Christopher Beckham; Amir Najafi; Ioannis Mitliagkas; David Lopez-Paz; Yoshua Bengio"
year: 2019
url: "https://proceedings.mlr.press/v97/verma19a.html"
venue: "ICML 2019"
accessed: 2026-08-24
source_tier: A
license: "PMLR open-access paper；本库仅保存独立摘要、必要结论与链接"
scope_role: hidden-space-extension
temporal_role: foundational
related: ["[[Mixup、Manifold Mixup 与插值正则]]", "[[Embedding 几何、相似度与各向异性]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Verma et al.：Manifold Mixup

> [!abstract] 来源定位
> 论文在随机 hidden layer 的 representation 上插值，并报告更平坦的类表示、决策边界和基准表现；同时在理想条件下分析表示 flattening。它承担 hidden-space 方法与原范围理论，不能证明 learned hidden chord 必然对应现实语义路径。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| MM-C1 | 可在选定 hidden layer 对 representations 与 targets 同步插值 | 定义 | suffix network、layer sampling 合同 | 精确 |
| MM-C2 | 原论文特定假设下得到 class-representation flattening | 理论 | 论文理想条件 | 原范围成立 |
| MM-C3 | 任意 hidden interpolation 都更接近数据 manifold | 命名外推 | learned coordinate 与语义未识别 | 错误 |
| MM-C4 | 不增加显著计算等同于无系统成本 | 系统外推 | activation storage/routing/compile 依赖 | 不成立 |
