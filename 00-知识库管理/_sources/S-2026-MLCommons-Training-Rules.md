---
type: source
status: verified
area: [sources, benchmarking, training-systems, rules]
source_type: official-documentation
title: "MLPerf Training Rules"
author: MLCommons
year: 2026
url: "https://github.com/mlcommons/training_policies/blob/master/training_rules.adoc"
accessed: 2026-08-26
source_tier: B
scope_role: current-benchmark-contract
temporal_role: current
related: ["[[Checkpoint 选择、验证泄漏与 Compute-matched 比较]]", "[[训练实验协议、事故记录与因果证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# MLCommons：MLPerf Training Rules

> [!abstract] 来源定位
> 当前 Training benchmark 的正式规则来源，定义 run、计时、目标质量、合规与结果聚合。易变条款绑定访问日期。

## 本卷调用

- wall-clock 计时从规则规定的数据触达/训练起点到达到目标质量；
- result 与 run、有效与失败、closed/open division 不得混淆；
- evaluation cadence 和 target crossing 会影响观测 time-to-quality；
- 本库只借用协议结构，不冒称内部实验为 MLPerf 合规结果。

## 边界

规则会更新；任何数值阈值、允许优化或 aggregation 细节使用前需回查对应 benchmark version。
