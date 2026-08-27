---
type: source
status: draft
area: [sources, neural-networks, stochastic-depth, residual-networks]
source_type: paper
title: "Deep Networks with Stochastic Depth"
author: "Gao Huang; Yu Sun; Zhuang Liu; Daniel Sedra; Kilian Q. Weinberger"
year: 2016
url: "https://arxiv.org/abs/1603.09382"
doi: "https://doi.org/10.1007/978-3-319-46493-0_39"
venue: "ECCV 2016"
accessed: 2026-08-24
source_tier: A
license: "Author preprint；本库仅保存独立摘要、必要公式与链接"
scope_role: core
temporal_role: foundational
related: ["[[Stochastic Depth、DropPath 与有效深度]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Huang et al.：Stochastic Depth

> [!abstract] 来源定位
> 论文在 residual networks 中训练时随机 bypass residual blocks、测试时恢复完整深度，并使用随层下降的 survival probability。它承担 stochastic depth 的原始结构与实验来源；现代 per-sample inverted DropPath、Transformer placement 和 fused implementation 需要单独声明。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| SD-C1 | residual rail 允许随机删除 branch 而保持 shape | 结构 | identity/projection 对齐 | 成立 |
| SD-C2 | 活跃 branch 数是 Poisson-binomial 随机变量 | 概率 | 独立 Bernoulli block gates | 精确 |
| SD-C3 | mask 后乘零必然节省 branch 计算 | 系统外推 | 需真正短路而非先算后乘 | 错误 |
| SD-C4 | 原论文误差改善保证所有现代深网受益 | 经验外推 | 架构、数据与 rate 依赖 | 不成立 |
