---
type: source
status: verified
area: [sources, generative-models, conditional-flow-matching, optimal-transport]
source_type: paper
title: "Improving and generalizing flow-based generative models with minibatch optimal transport"
author: "Alexander Tong; Kilian Fatras; Nikolay Malkin; Guillaume Huguet; Yanlei Zhang; Jarrid Rector-Brooks; Guy Wolf; Yoshua Bengio"
year: 2024
url: "https://arxiv.org/abs/2302.00482"
venue: "Transactions on Machine Learning Research"
accessed: 2026-08-25
source_tier: A
license: "论文页面；本库仅保存独立摘要、必要公式与链接"
scope_role: foundational
temporal_role: active-research
related: ["[[Conditional Flow Matching、Coupling 与最优传输路径]]", "[[S-2023-Lipman-Flow-Matching]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Tong et al.：Conditional Flow Matching 与 minibatch OT

> [!abstract] 来源定位
> 论文给出 generalized Conditional Flow Matching 家族，并研究 OT-CFM：通过 minibatch optimal-transport coupling 构造较简单的 conditional paths，在无需 source density evaluation 的条件下训练 CNF。

## 课程调用

- CFM 允许 source/target 为一般可采样分布，不必都能评估密度；
- endpoint coupling 是训练对象的一部分，会改变 conditional velocity 的方差；
- 当 true OT plan 可得时，OT-CFM 与 dynamic OT 有精确的理论接口；
- 实际 minibatch OT 是批内离散 assignment，不等于 population OT plan。

## 审计要求

比较 independent coupling 与 minibatch OT 时必须报告 batch size、cost、regularization/solver、是否 stop-gradient、配对重用方式和 ODE NFE。只看线段长度不足以证明 learned marginal trajectories 更直或生成质量更高。
