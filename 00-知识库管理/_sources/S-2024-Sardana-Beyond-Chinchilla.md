---
type: source
status: verified
area: [sources, ai/scaling-laws, inference-cost, deployment]
source_type: paper
title: "Beyond Chinchilla-Optimal: Accounting for Inference in Language Model Scaling Laws"
author: "Nikhil Sardana, Jacob Portes, Sasha Doubov, Jonathan Frankle"
year: 2024
url: "https://proceedings.mlr.press/v235/sardana24a.html"
accessed: 2026-08-26
source_tier: A
license: "ICML paper; independent summary only"
scope_role: inference-aware
temporal_role: active-research
related: ["[[过训练、推理成本与多目标最优规模]]", "[[Chinchilla、Compute-optimal 参数与数据分配]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Beyond Chinchilla-Optimal

> [!abstract] 来源定位
> 论文把 inference demand 加入 Chinchilla-style 训练分配，并用 47 个不同规模/训练量的模型验证极端 tokens-per-parameter 区域。课程用它区分 training-compute optimum 与 train-plus-deploy optimum。

## 可调用证据

- 预计请求量增加时，较小模型训练更久可降低重复推理成本；
- total objective 需要训练成本、单次推理成本、请求量与目标 loss；
- 常见 token/parameter 区间拟合可能高估极端 overtraining 区域中额外 token 的作用；
- 论文分别讨论 compute 与现实成本口径。

## 边界

- 请求长度、batching、cache、硬件、latency 和服务利用率会改变推理成本；
- 47 个模型提供有价值验证，但不覆盖所有架构与极端比例；
- “smaller and longer”不是无条件配方，取决于服务量和质量约束。
