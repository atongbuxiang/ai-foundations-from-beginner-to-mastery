---
type: source
status: active
area: [sources, representation-learning, deep-learning]
source_type: review
title: "Representation Learning: A Review and New Perspectives"
author: [Yoshua Bengio, Aaron Courville, Pascal Vincent]
year: 2013
url: "https://doi.org/10.1109/TPAMI.2013.50"
accessed: 2026-08-23
source_tier: A
license: "IEEE review; retain citation and independent exposition"
venue: "IEEE TPAMI 35(8), 1798–1828"
scope_role: primary
temporal_role: classical-foundation
related: ["[[表示学习的任务、表示与下游风险]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Representation Learning: A Review and New Perspectives

> [!abstract] 来源定位
> 系统组织 representation learning、deep architectures、autoencoders、probabilistic models、manifold priors 与“好表示”开放问题。本库调用其历史和设计原则；downstream risk、task family 与现代自监督结论另立统计合同。

## 本库调用

1. representation 是从 raw input 到 feature space 的 learned map；
2. prior、architecture 与 objective 共同决定保留或删除的信息；
3. disentangling、smoothness 与 manifold 直觉不是无条件保证；
4. pretext success 必须由 downstream 与 shift protocol 验收；
5. representation quality 必须相对于 task family 定义。
