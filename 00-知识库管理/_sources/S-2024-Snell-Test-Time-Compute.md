---
type: source
status: verified
area: [sources, reasoning, test-time-compute]
source_type: paper
title: "Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters"
author: "Charlie Snell et al."
year: 2024
url: "https://arxiv.org/abs/2408.03314"
accessed: 2026-08-26
source_tier: P1
license: "Paper; independent summary"
scope_role: compute-allocation
related: ["[[Test-time Compute、Search、Verifier 与预算]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Test-time Compute 的难度自适应分配

> [!abstract] 来源定位
> 论文比较基于 process verifier 的搜索与自适应修改响应分布等推理扩展方式，强调最佳策略随题目难度变化，并在 FLOPs 匹配下讨论小模型推理预算与大模型的交换。

结论绑定 policy、verifier、题目分布和成本模型；token 数、FLOPs、调用次数、延迟、显存与并行吞吐不是同一个预算，不能混成单轴结论。
