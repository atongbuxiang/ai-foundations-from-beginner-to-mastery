---
type: source
status: active
area: [sources, deep-generalization, memorization]
source_type: paper
title: "Understanding Deep Learning Requires Rethinking Generalization"
author: [Chiyuan Zhang, Samy Bengio, Moritz Hardt, Benjamin Recht, Oriol Vinyals]
year: 2017
url: "https://openreview.net/forum?id=Sy8gdB9xx"
accessed: 2026-08-23
source_tier: A
license: "OpenReview/ICLR paper; retain citation"
venue: "ICLR 2017 Oral"
scope_role: primary
temporal_role: modern-theory
related: ["[[深度泛化证据地图与开放问题]]", "[[插值、双下降与经典偏差方差边界]]"]
created: 2026-08-23
updated: 2026-08-23
---
# Understanding Deep Learning Requires Rethinking Generalization
> [!abstract] 来源定位
> 通过真实/随机 labels 与随机 inputs 的系统实验展示现代网络和 SGD 的 memorization 能力，并给出有限样本表达性构造。本库调用“architecture/zero-train-error 不足以解释泛化”的现象证据；不把实验外推为所有 algorithm/data-dependent 理论的否定。
## 本库调用
1. random-label memorization；
2. explicit regularization 消融；
3. finite-sample expressivity；
4. phenomenon 与 mechanism 分层；
5. 过度全称解读的边界。

