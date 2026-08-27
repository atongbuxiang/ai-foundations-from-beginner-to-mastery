---
type: source
status: active
area: [sources, contrastive-learning, infonce, predictive-coding]
source_type: paper
title: "Representation Learning with Contrastive Predictive Coding"
author: [Aaron van den Oord, Yazhe Li, Oriol Vinyals]
year: 2018
url: "https://arxiv.org/abs/1807.03748"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and theorem conditions"
venue: "arXiv 1807.03748"
scope_role: primary
temporal_role: method-origin
related: ["[[对比学习、InfoNCE 与密度比]]", "[[正负样本、Batch 依赖与梯度估计]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Representation Learning with Contrastive Predictive Coding

> [!abstract] 来源定位
> CPC 以 context 预测 future latent，并提出 InfoNCE 式多候选 classification objective。本库调用其 density-ratio optimal score、log-K lower-bound ceiling 与 negative-sampling contract。

## 本库调用

1. positive 来自 joint 或 conditional，negatives 来自指定 marginal；
2. candidate-index classification 导出 softmax loss；
3. optimal score 只识别 density ratio 到 anchor-dependent additive term；
4. MI lower bound 有 sampling/model 条件且 ceiling 为 log K；
5. predictive-view 设计不能无条件外推到任意 augmentation；
