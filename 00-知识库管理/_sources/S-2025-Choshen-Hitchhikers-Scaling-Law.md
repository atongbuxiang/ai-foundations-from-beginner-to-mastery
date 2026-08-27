---
type: source
status: verified
area: [sources, ai/scaling-laws, estimation, extrapolation]
source_type: paper
title: "A Hitchhiker's Guide to Scaling Law Estimation"
author: "Leshem Choshen, Yang Zhang, Jacob Andreas"
year: 2025
url: "https://proceedings.mlr.press/v267/choshen25a.html"
accessed: 2026-08-26
source_tier: A
license: "ICML paper; independent summary only"
scope_role: estimation-guide
temporal_role: active-research
related: ["[[经验 Scaling Law、幂律拟合与不可约项]]", "[[Scaling 实验设计、外推不确定性与证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# A Hitchhiker's Guide to Scaling Law Estimation

> [!abstract] 来源定位
> 论文汇集 485 个公开预训练模型、估计逾千条 scaling laws，并比较实际估计选择。课程用它补充 2025 年经验 best practices，特别是 intermediate checkpoints 与相近尺度训练点的价值。

## 可调用证据

- 只用 final checkpoint 会浪费学习曲线中的信息；
- 使用 intermediate checkpoints 可在论文数据上显著改善估计；
- 与 target 尺度更接近的模型通常给更准确预测；
- optimizer、dataset 与 architecture 比较都需要一致估计 protocol。

## 边界

- 公开模型汇编包含不同训练协议与报告误差；
- 相近尺度更准确不是“永远只取最大 proxy”的定理；
- best practice 仍需通过当前 family 的 held-out scales 预注册验证。
