---
type: source
status: draft
area: [sources, ai/moe, systems, parallelism]
source_type: paper
title: "Tutel: Adaptive Mixture-of-Experts at Scale"
author: "Changho Hwang et al."
year: 2022
url: "https://arxiv.org/abs/2206.03382"
accessed: 2026-08-24
source_tier: A
license: "arXiv; independent summary only"
scope_role: systems-paper
related: ["[[Expert Parallel、All-to-All 与通信成本]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Tutel：Adaptive MoE Parallelism

> [!abstract] 来源定位
> Tutel/Flex 研究动态 Expert workload 下的 adaptive parallelism、pipelining、layout 与大规模 MoE kernel/通信。

## 调用边界

- 单层与端到端 speedup 必须保留设备数、baseline、网络和模型；
- identical layout/自适应执行是系统设计，不改变 MoE 数学函数的前提需检查 dtype/order；
- 动态负载使平均吞吐与尾部同步成本不同，二者都应报告。
