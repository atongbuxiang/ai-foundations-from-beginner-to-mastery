---
type: source
status: verified
area: [sources, ai/scaling-laws, data-repetition, data-constraints]
source_type: paper
title: "Scaling Data-Constrained Language Models"
author: "Niklas Muennighoff et al."
year: 2025
url: "https://www.jmlr.org/papers/v26/24-1000.html"
accessed: 2026-08-26
source_tier: A
license: "JMLR paper; independent summary only"
scope_role: core-data
temporal_role: active-research
related: ["[[数据质量、重复、混合与有效 Token]]", "[[过训练、推理成本与多目标最优规模]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Scaling Data-Constrained Language Models

> [!abstract] 来源定位
> 论文通过约 400 次训练、最高 9B 参数与 900B 训练 tokens，研究 unique data 受限后的重复训练价值，并提出考虑 repeated tokens 与 excess parameters 的 compute-optimal 经验律。

## 可调用证据

- 在其协议与 compute 范围内，最多约 4 epochs 的重复数据相对独特数据造成的 loss 差异很小；
- 重复继续增加后，新增 compute 的边际价值最终趋弱；
- repeated token 不能永远按 unique token 的同一价值计数；
- 加入 code 或调整过滤是缓解 data scarcity 的实验干预，而非免费增加等价数据。

## 边界

- “4 epochs”是论文设置内的经验观察，不是任意数据/模型的安全常数；
- 数据污染、记忆、下游指标与分布漂移可能早于 validation loss 报警；
- effective token 依赖 epoch、domain、quality、模型与训练时域，不是通用货币。
