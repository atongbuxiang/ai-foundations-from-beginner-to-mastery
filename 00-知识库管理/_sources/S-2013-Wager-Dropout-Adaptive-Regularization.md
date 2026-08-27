---
type: source
status: draft
area: [sources, neural-networks, dropout, adaptive-regularization]
source_type: paper
title: "Dropout Training as Adaptive Regularization"
author: "Stefan Wager; Sida Wang; Percy Liang"
year: 2013
url: "https://proceedings.neurips.cc/paper_files/paper/2013/hash/38db3aed920cf82ab059bfccbd02be6a-Abstract.html"
venue: "NeurIPS 2013"
accessed: 2026-08-24
source_tier: A
license: "NeurIPS proceedings paper；本库仅保存独立摘要、必要结论与链接"
scope_role: theory-boundary
temporal_role: foundational
related: ["[[Dropout 的方差、共适应解释与 Bayesian 边界]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Wager、Wang、Liang：Dropout 作为自适应正则

> [!abstract] 来源定位
> 论文把 feature noising 置于广义线性模型中分析，并给出与 Fisher-scaled、自适应 $L_2$ 正则的一阶联系。它承担“Dropout 可诱导数据依赖 penalty”的正式证据；其 GLM 与近似条件不能直接外推为任意非凸深网的精确显式正则项。

## 证据边界

平方损失线性模型可直接把 expected noisy risk 分解为 clean risk 与 feature-weighted quadratic penalty；论文更一般的 GLM 结果依赖局部/一阶近似。深网中 mask 可改变激活区间、normalization 统计、optimization noise 和表示学习，不能只用一个 $L_2$ 比喻概括。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| WAR-C1 | 线性平方损失下 feature dropout 产生精确加权二次 penalty | 代数 | 独立 Bernoulli feature masks | 精确 |
| WAR-C2 | GLM 下可得到 adaptive regularization 联系 | 近似理论 | 论文假设与一阶展开 | 原范围成立 |
| WAR-C3 | 任意深网 Dropout 都严格等价普通 weight decay | 过度外推 | 激活、层次与数据依赖 | 错误 |
| WAR-C4 | penalty 解释自动证明泛化改善 | 证据混淆 | 仍需风险假设与实验 | 不成立 |
