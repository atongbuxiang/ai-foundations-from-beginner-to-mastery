---
type: source
status: active
area: [sources, contrastive-learning, simclr, augmentation, batch]
source_type: paper
title: "A Simple Framework for Contrastive Learning of Visual Representations"
author: [Ting Chen, Simon Kornblith, Mohammad Norouzi, Geoffrey Hinton]
year: 2020
url: "https://proceedings.mlr.press/v119/chen20j.html"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and theorem conditions"
venue: "ICML 2020"
scope_role: primary
temporal_role: modern-method
related: ["[[正负样本、Batch 依赖与梯度估计]]", "[[数据增强、不变性、等变性与任务充分性]]"]
created: 2026-08-23
updated: 2026-08-23
---

# A Simple Framework for Contrastive Learning of Visual Representations

> [!abstract] 来源定位
> 展示 augmentation composition、projection head、normalization、temperature、batch size 与 training length 共同决定结果。本库用它建立 two-view in-batch NT-Xent 程序合同，而不把 ImageNet 经验提升为普遍定理。

## 本库调用

1. 同一 source sample 的 two views 构成 positive；
2. other in-batch views 构成 denominator candidates；
3. batch size 改变 negative set 与 population surrogate；
4. projection head 训练空间与 evaluation representation 可不同；
5. augmentation 与 split 决定 task validity 和 leakage；
