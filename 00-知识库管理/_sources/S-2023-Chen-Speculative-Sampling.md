---
type: source
status: verified
area: [sources, language-models, speculative-decoding]
source_type: paper
title: "Accelerating Large Language Model Decoding with Speculative Sampling"
author: "Charlie Chen et al."
year: 2023
url: "https://arxiv.org/abs/2302.01318"
accessed: 2026-08-26
source_tier: P1
license: "Paper; independent summary"
scope_role: independent-speculative-sampling
related: ["[[Speculative Decoding、Acceptance 与分布精确性]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Speculative Sampling：独立提出的 modified rejection sampling

> [!abstract] 来源定位
> 论文同样以小 draft 和大 target 的并行评分加速自回归采样，通过修正 rejection sampling 保持 target 分布。课程用作独立一级证据和实现边界交叉核验。

加速倍数依 draft/target 相似、验证批量、内存带宽和并发；acceptance 高也不必然改善高并发吞吐。
