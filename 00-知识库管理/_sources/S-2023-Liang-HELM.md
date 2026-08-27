---
type: source
status: verified
area: [sources, language-models, evaluation, benchmarks]
source_type: paper
title: "Holistic Evaluation of Language Models"
author: "Percy Liang et al."
year: 2023
url: "https://openreview.net/forum?id=iO4LZibEqW"
accessed: 2026-08-26
source_tier: P1
license: "TMLR paper; independent summary"
scope_role: holistic-evaluation-framework
related: ["[[语言模型评估对象、任务单位与 Benchmark 合同]]", "[[能力—行为—系统评估协议与证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# HELM：场景、适配、指标与透明复现

> [!abstract] 来源定位
> HELM 把语言模型评估组织为 scenario、adaptation、metric 与 model deployment 的显式组合，并强调多场景、多指标、缺口披露与原始 prompt/completion 透明。本库用它建立评估对象和运行 manifest；不把“holistic”解释成已经覆盖所有能力与风险。

## 调用边界

- 同一数据集可因 prompt/adaptation/parser 不同而形成不同测量；
- 多指标应保留向量与 trade-off，不应无权重压成总分；
- 公开 leaderboard 是带版本的观察，不是模型的永恒属性；
- 框架维护状态、模型 API 与场景内容会变化，复现必须固定 release/commit。
