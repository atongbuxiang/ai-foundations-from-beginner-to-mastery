---
type: source
status: active
area: [sources, neural-networks/residual-stability, dynamical-systems]
source_type: paper
title: "Stable Architectures for Deep Neural Networks"
author: "Eldad Haber; Lars Ruthotto"
year: 2018
url: "https://arxiv.org/abs/1705.03341"
venue: "Inverse Problems 34(1), 2018"
accessed: 2026-08-23
source_tier: A
license: "author preprint；本库仅保存独立摘要、必要公式与链接"
scope_role: core
temporal_role: foundational
related: ["[[ResNet 的 ODE 与离散动力系统视角]]", "[[残差缩放、Lipschitz 界与深度稳定性]]", "[[刚性系统、绝对稳定域与隐式方法]]"]
created: 2026-08-23
updated: 2026-08-29
---

# Haber–Ruthotto：Stable Architectures

> [!abstract] 来源定位
> 论文从动力系统、well-posedness 与离散稳定性分析深网，并据此提出受结构约束的架构。它支持“稳定性需要谱/动力条件而非只看 skip 是否存在”；不把特定稳定架构的实验提升为所有任务的最优性。

## 课程采用的核心区分

1. forward perturbation stability；
2. backward/adjoint stability；
3. numerical-scheme stability；
4. optimization stability；
5. statistical generalization。

这些对象有关联，但不是同一个定理。对线性 test equation，连续系统稳定还不足以保证显式离散稳定；step size 与 stability region 必须进入合同。

## 断言表

| ID | 断言 | 条件/边界 | 本库判断 |
|---|---|---|---|
| STA-C1 | 深网可视作非线性动力系统参数估计 | 明确 state/update 后 | 成立 |
| STA-C2 | 离散稳定性影响 forward/backward propagation | 指定 norm、step 与 Jacobian spectrum | 成立 |
| STA-C3 | residual form 单独保证稳定 | $I+hJ_F$ 仍可落在不稳定区 | 不成立 |
| STA-C4 | 稳定架构无表达代价 | 结构约束会限制 solution space | 不成立 |
