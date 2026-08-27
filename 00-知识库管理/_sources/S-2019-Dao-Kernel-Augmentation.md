---
type: source
status: active
area: [sources, data-augmentation, kernels, generalization]
source_type: paper
title: "A Kernel Theory of Modern Data Augmentation"
author: [Tri Dao, Albert Gu, Alexander Ratner, Virginia Smith, Christopher De Sa, Christopher Ré]
year: 2019
url: "https://proceedings.mlr.press/v97/dao19b.html"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and theorem conditions"
venue: "ICML 2019"
scope_role: primary
temporal_role: modern-theory
related: ["[[数据增强、不变性、等变性与任务充分性]]"]
created: 2026-08-23
updated: 2026-08-23
---

# A Kernel Theory of Modern Data Augmentation

> [!abstract] 来源定位
> 在 kernel/model approximation 语境中刻画 augmentation 对 predictor 与 regularization 的作用。本库用它说明“增强等于更多 iid 样本”通常错误，并把 kernel-regime 结论与一般深网训练明确分开。

## 本库调用

1. augmented copies 条件依赖于同一 source unit；
2. augmentation 可改变 effective kernel/regularizer；
3. class-preserving 是假设，不是变换名字自带的性质；
4. empirical orbit average 与 population augmented risk 不同；
5. kernel 近似结论不能无条件升级为任意深网定理。
