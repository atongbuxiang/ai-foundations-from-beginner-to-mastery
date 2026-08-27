---
type: source
status: verified
area: [sources, supervised-finetuning, data-quality]
source_type: paper
title: "LIMA: Less Is More for Alignment"
author: "Chunting Zhou et al."
year: 2023
url: "https://arxiv.org/abs/2305.11206"
accessed: 2026-08-26
source_tier: P1
license: "Paper; independent summary"
scope_role: small-curated-sft-case
temporal_role: empirical-hypothesis
related: ["[[指令数据质量、混合、多轮状态与选择偏差]]", "[[监督微调、Teacher Forcing 与 Response-only Loss]]"]
created: 2026-08-26
updated: 2026-08-26
---

# LIMA：少量精选 SFT 的经验案例

> [!abstract] 来源定位
> LIMA 以少量精选 prompt–response 和标准监督损失研究 SFT，并提出 superficial alignment hypothesis。课程把它作为“质量可能比数量更关键”的可证伪案例，而不是预训练能力或所有模型只需少量对齐数据的普遍定理。

数据选择、base model、人工偏好评估和比较对象共同决定结论；必须披露 curator、来源、去重、选择预算与 rejected pool。

