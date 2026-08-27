---
type: source
status: draft
area: [sources, ai/moe, stability, transfer]
source_type: paper
title: "ST-MoE: Designing Stable and Transferable Sparse Expert Models"
author: "Barret Zoph et al."
year: 2022
url: "https://arxiv.org/abs/2202.08906"
accessed: 2026-08-24
source_tier: A
license: "arXiv; independent summary only"
scope_role: design-guide
related: ["[[MoE 门控归一化、证据地图与开放问题]]", "[[MoE 负载均衡辅助损失与偏置]]"]
created: 2026-08-24
updated: 2026-08-24
---

# ST-MoE：稳定性与迁移设计

> [!abstract] 来源定位
> ST-MoE 系统审查稀疏 Expert 模型的训练不稳定、router z-loss、fine-tuning 与 transfer，并报告 269B 总参数/32B dense-compute 级配置。

## 调用边界

- z-loss、初始化和 fine-tuning 技巧限定相应 parameterization；
- “compute comparable”需核对 activated MAC、通信和硬件；
- 多任务结果是强经验来源，但不构成所有 MoE 变体的稳定性定理。
