---
type: source
status: verified
area: [sources, ai/moe, systems, inference]
source_type: paper
title: "DeepSpeed-MoE: Advancing Mixture-of-Experts Inference and Training"
author: "Samyam Rajbhandari et al."
year: 2022
url: "https://arxiv.org/abs/2201.05596"
accessed: 2026-08-24
source_tier: A
license: "arXiv/ICML; independent summary only"
scope_role: training-inference-system
related: ["[[Expert Parallel、All-to-All 与通信成本]]", "[[条件计算、专家混合与稀疏激活]]", "[[Tensor、Pipeline、Sequence 与 Expert Parallel]]", "[[通信 Roofline、非确定性与分布式训练证据地图]]"]
created: 2026-08-24
updated: 2026-08-24
---

# DeepSpeed-MoE：训练与推理系统

> [!abstract] 来源定位
> DeepSpeed-MoE 讨论 Expert/tensor/data parallel 组合、模型压缩与大规模 MoE inference，实现层面补齐“激活参数少但总权重难部署”的矛盾。

## 调用边界

- latency/cost speedup 是特定 quality-equivalent baseline 与系统版本的 `E`；
- 总参数驻留、网络、batch 和 weight movement 可使小 batch inference 与训练表现不同；
- 压缩后的模型不再只是同一 MoE 的执行优化，质量误差需另账。
