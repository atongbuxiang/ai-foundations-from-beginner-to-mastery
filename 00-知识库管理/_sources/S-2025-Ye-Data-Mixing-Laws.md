---
type: source
status: verified
area: [sources, ai/scaling-laws, data-mixtures]
source_type: paper
title: "Data Mixing Laws: Optimizing Data Mixtures by Predicting Language Modeling Performance"
author: "Jiasheng Ye, Peiju Liu, Tianxiang Sun, Jun Zhan, Yunhua Zhou, Xipeng Qiu"
year: 2025
url: "https://openreview.net/forum?id=jjCB27TMK3"
accessed: 2026-08-26
source_tier: A
license: "ICLR paper; independent summary only"
scope_role: mixture-method
temporal_role: active-research
related: ["[[数据质量、重复、混合与有效 Token]]", "[[Scaling 实验设计、外推不确定性与证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Data Mixing Laws

> [!abstract] 来源定位
> 论文把预训练 mixture proportions 作为显式变量，用小规模 runs 拟合 domain-loss 与混合比例的函数，再嵌套 step/model scaling 预测更大训练。课程用它说明“数据量相同”远不足以定义数据实验。

## 可调用证据

- mixture vector 位于 simplex，不是一个 token-count 标量；
- 各 domain loss 对 mixture 的响应可不同，整体指标还依赖 evaluation weights；
- 论文在其 RedPajama/模型协议中用拟合曲线选择 mixture，并报告 1B、100B-token 级验证；
- continual training 中 mixture 还与遗忘约束相互作用。

## 边界

- unseen-mixture 预测仍绑定观测 domain、函数族与尺度范围；
- 整体 validation loss 好不保证每个 domain 或安全属性都好；
- mixture tuning 产生 search/selection compute，必须纳入总账。
