---
type: source
status: verified
area: [sources, pretraining-data, data-mixture, group-dro]
source_type: paper
title: "DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining"
author: "Sang Michael Xie et al."
year: 2023
url: "https://arxiv.org/abs/2305.10429"
accessed: 2026-08-26
source_tier: P1
license: "NeurIPS paper; independent summary"
scope_role: mixture-optimization
temporal_role: active-method
related: ["[[数据混合、温度采样、重加权与域损失]]", "[[数据版本、Provenance、有效 Token 与证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# DoReMi：数据域重加权

> [!abstract] 来源定位
> DoReMi 用小 proxy 和 group DRO 风格 excess loss 信号学习 domain weights，再据此重采样训练大模型。课程调用三阶段协议、simplex 权重和 proxy-to-target 外推边界；论文性能只在其 Pile/GLaM 域、模型尺度和预算内成立。

Mixture search 的 proxy/reference 训练成本、clipping/smoothing、domain taxonomy 与 evaluation aggregation 均须入账。

