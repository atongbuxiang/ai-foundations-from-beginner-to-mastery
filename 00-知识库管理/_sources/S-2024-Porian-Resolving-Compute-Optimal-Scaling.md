---
type: source
status: verified
area: [sources, ai/scaling-laws, compute-optimal, optimization]
source_type: paper
title: "Resolving Discrepancies in Compute-Optimal Scaling of Language Models"
author: "Tomer Porian, Mitchell Wortsman, Jenia Jitsev, Ludwig Schmidt, Yair Carmon"
year: 2024
url: "https://arxiv.org/abs/2406.19146"
accessed: 2026-08-26
source_tier: A
license: "arXiv / conference paper; independent summary only"
scope_role: reconciliation
temporal_role: active-research
related: ["[[Kaplan 参数数据律、联合拟合与有限区间]]", "[[IsoFLOP、训练算力口径与系统校正]]", "[[Scaling 实验设计、外推不确定性与证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Resolving Discrepancies in Compute-Optimal Scaling of Language Models

> [!abstract] 来源定位
> 论文复现 Kaplan-style 设置，并把 Kaplan/Chinchilla 分歧定位到 last-layer compute、warmup 时域和尺度依赖 optimizer tuning 等可干预因素。它直接支持“scaling law 也包含训练控制器”的课程主张。

## 可调用证据

- under-tuned 小/大模型会系统改变 compute-optimal frontier；
- warmup 若按固定 token/step 方式随规模改变，占用的有效训练比例也改变；
- 输出层/embedding 是否计入参数与 FLOPs 会在小尺度造成显著口径偏差；
- 修正这些因素后，研究设置可更接近 Chinchilla-style allocation；
- 最优学习率、batch 与 AdamW 状态也可随规模呈经验规律。

## 边界

- reconciliation 绑定论文复现的模型、数据、优化器和尺度；
- 与 Chinchilla 接近不证明未来架构永远保持相同指数；
- optimizer tuning 本身消耗 compute，必须进入实验总预算。
