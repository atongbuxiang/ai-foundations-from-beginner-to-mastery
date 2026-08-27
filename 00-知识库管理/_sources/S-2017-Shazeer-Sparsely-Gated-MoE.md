---
type: source
status: draft
area: [sources, ai/moe, conditional-compute]
source_type: paper
title: "Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer"
author: "Noam Shazeer et al."
year: 2017
url: "https://arxiv.org/abs/1701.06538"
accessed: 2026-08-24
source_tier: A
license: "arXiv; independent summary only"
scope_role: foundational-paper
related: ["[[条件计算、专家混合与稀疏激活]]", "[[Router、Gate、Top-k 与稀疏组合]]", "[[MoE 负载均衡辅助损失与偏置]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Sparsely-Gated Mixture-of-Experts

> [!abstract] 来源定位
> 早期大规模稀疏门控 MoE 主来源：trainable sparse gate、Expert FFNs、noisy routing、负载均衡目标与分布式条件计算。

## 调用边界

- “总参数大、每样本计算小”是结构账本；论文规模/质量/效率数字限定其 LSTM、任务和集群；
- gate、capacity、通信和训练稳定不是由稀疏激活定义自动解决；
- 历史优先权只在论文明确范围内表述，不把它写成所有 MoE 思想的起点。
