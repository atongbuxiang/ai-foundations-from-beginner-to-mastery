---
type: source
status: verified
area: [sources, neural-networks, optimization, weight-decay, adamw]
source_type: paper
title: "Decoupled Weight Decay Regularization"
author: "Ilya Loshchilov; Frank Hutter"
year: 2019
url: "https://openreview.net/pdf?id=Bkg6RiCqY7"
venue: "ICLR 2019"
accessed: 2026-08-24
source_tier: A
license: "OpenReview conference paper；本库仅保存独立摘要、必要结论与链接"
scope_role: optimizer-regularizer-boundary
temporal_role: modern-foundational
related: ["[[网络级正则化的交互、消融与证据地图]]", "[[自适应优化方法]]", "[[L2 正则、Coupled Decay 与 AdamW]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Loshchilov、Hutter：Decoupled Weight Decay

> [!abstract] 来源定位
> 论文区分把 $L_2$ penalty 加入 loss 后再经 optimizer preconditioner，与直接对参数做 multiplicative decay；二者对普通 SGD 可在尺度换算下等价，对 Adam 类方法一般不等价。它承担 optimizer—regularizer 边界案例。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| AWD-C1 | SGD 的 $L_2$ gradient 与 weight decay 可在系数换算下等价 | 代数 | 无自适应 preconditioner 等附加差异 | 条件成立 |
| AWD-C2 | Adam 的 loss-side $L_2$ 与 decoupled decay 一般不同 | 优化 | coordinatewise preconditioning | 成立 |
| AWD-C3 | `weight_decay` 参数名足以确定数学对象 | API 外推 | optimizer 实现可能不同 | 错误 |
| AWD-C4 | AdamW 自动解决所有正则化交互 | 经验外推 | schedule、normalization、参数组依赖 | 不成立 |
