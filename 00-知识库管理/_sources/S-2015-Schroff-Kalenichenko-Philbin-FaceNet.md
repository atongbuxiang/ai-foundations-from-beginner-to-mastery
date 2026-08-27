---
type: source
status: active
area: [sources, metric-learning, triplet-loss, retrieval]
source_type: paper
title: "FaceNet: A Unified Embedding for Face Recognition and Clustering"
author: [Florian Schroff, Dmitry Kalenichenko, James Philbin]
year: 2015
url: "https://openaccess.thecvf.com/content_cvpr_2015/html/Schroff_FaceNet_A_Unified_2015_CVPR_paper.html"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and theorem conditions"
venue: "CVPR 2015"
scope_role: primary
temporal_role: modern-method
related: ["[[度量学习、相似性与检索风险]]", "[[正负样本、Batch 依赖与梯度估计]]"]
created: 2026-08-23
updated: 2026-08-23
---

# FaceNet: A Unified Embedding for Face Recognition and Clustering

> [!abstract] 来源定位
> 直接学习 compact Euclidean embedding，并用 online triplet mining 服务 verification、recognition 与 clustering。本库用它说明 geometry、triplet loss、mining policy 与 deployment threshold 不可分割。

## 本库调用

1. triplet margin 比较 anchor-positive 与 anchor-negative distance；
2. easy triplets 可能给 zero gradient；
3. overly hard 或 noisy negatives 可能引入不稳或 shortcut；
4. verification、ranking 与 clustering 不是同一 metric；
5. identity leakage 必须按 subject split 审计；
