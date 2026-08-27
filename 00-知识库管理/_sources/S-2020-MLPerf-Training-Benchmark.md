---
type: source
status: verified
area: [sources, benchmarking, training-systems, time-to-quality]
source_type: paper
title: "MLPerf Training Benchmark"
author: "Mattson et al."
year: 2020
url: "https://proceedings.mlsys.org/paper_files/paper/2020/file/411e39b117e885341f25efb8912945f7-Paper.pdf"
accessed: 2026-08-26
source_tier: A
venue: MLSys
scope_role: benchmark-protocol
related: ["[[Checkpoint 选择、验证泄漏与 Compute-matched 比较]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Mattson 等：MLPerf Training Benchmark

> [!abstract] 来源定位
> MLPerf Training 用达到固定目标质量的 wall-clock time 组织系统比较，并正面处理随机训练的 time-to-solution 变异。

## 本卷调用

- 区分 throughput、step time 与 time-to-quality；
- 目标 quality、评估频率、计时起点、run aggregation 和未达标 run 必须写入协议；
- 系统优化若改变 convergence，不能只靠 tokens/s 宣称端到端加速；
- 对 stochastic runtime 使用多次有效运行与预设 aggregation。

## 边界

MLPerf 是特定 benchmark 合同，不等于任意研究问题的唯一公平标准；课程借用其 fixed-target 和 run-accounting 思想。
