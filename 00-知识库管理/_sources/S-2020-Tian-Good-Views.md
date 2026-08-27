---
type: source
status: active
area: [sources, contrastive-learning, augmentation, task-sufficiency]
source_type: paper
title: "What Makes for Good Views for Contrastive Learning?"
author: [Yonglong Tian, Chen Sun, Ben Poole, Dilip Krishnan, Cordelia Schmid, Phillip Isola]
year: 2020
url: "https://proceedings.neurips.cc/paper/2020/hash/4c2e5eaae9152079b9e95845750bb9ab-Abstract.html"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and theorem conditions"
venue: "NeurIPS 2020"
scope_role: primary
temporal_role: modern-theory
related: ["[[数据增强、不变性、等变性与任务充分性]]", "[[对比学习、InfoNCE 与密度比]]"]
created: 2026-08-23
updated: 2026-08-23
---

# What Makes for Good Views for Contrastive Learning?

> [!abstract] 来源定位
> 从 multiview/InfoMin 角度研究 view choice：两视图共享的信息不能只追求少，还必须保留目标任务所需信息。本库把它作为“增强强度存在任务依赖甜点区”的条件化证据，不把单一 ImageNet 结果外推到任意模态与任务。

## 本库调用

1. augmentation law 决定 positive joint，而不只是数据量；
2. 视图间冗余过多可能使 pretext 太容易；
3. 删除 task-relevant information 会产生不可逆 approximation gap；
4. “好视图”依赖 downstream task family；
5. MI 解释、有限样本估计和 downstream utility 必须分账。
