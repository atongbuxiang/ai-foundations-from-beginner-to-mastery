---
type: source
status: verified
area: [sources, statistics, benchmarking, reinforcement-learning]
source_type: paper
title: "Deep Reinforcement Learning at the Edge of the Statistical Precipice"
author: "Agarwal et al."
year: 2021
url: "https://papers.nips.cc/paper/2021/hash/f514cec81cb148559cf475e7426eed5e-Abstract.html"
accessed: 2026-08-26
source_tier: A
venue: NeurIPS
scope_role: robust-aggregation-and-uncertainty
related: ["[[随机种子、配对比较、置信区间与序贯决策]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Agarwal 等：有限运行基准的区间与分布

> [!abstract] 来源定位
> 论文针对 few-run、multi-task RL 提出 interval estimates、performance profiles 与 IQM 等更稳健报告方式。本卷迁移其统计思想，但不把 RL 特定聚合器机械用于单任务监督学习。

## 本卷调用

- 对跨任务标准化结果展示 performance profile，而非只给均值排名；
- 用 bootstrap interval 呈现 aggregate uncertainty；
- 同时报 tails/failure rate，避免高方差方法靠少数极值胜出；
- 聚合前先声明 task weighting 与 normalization。

## 边界

IQM 不是所有问题的默认 estimand；小样本 bootstrap 也依赖 resampling unit 与任务/seed 层级正确。
