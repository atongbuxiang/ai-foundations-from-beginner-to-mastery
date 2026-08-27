---
type: source
status: active
area: [sources, lazy-training, scaling]
source_type: paper
title: "On Lazy Training in Differentiable Programming"
author: [Lenaic Chizat, Edouard Oyallon, Francis Bach]
year: 2019
url: "https://proceedings.neurips.cc/paper_files/paper/2019/hash/ae614c557843b1df326cb29c57225459-Abstract.html"
accessed: 2026-08-23
source_tier: A
license: "NeurIPS proceedings; retain citation"
venue: "Advances in Neural Information Processing Systems 32"
scope_role: primary
temporal_role: modern-theory
related: ["[[NTK、Lazy Training 与 Kernel Regime]]", "[[Mean-Field、Feature Learning 与训练 Regime]]"]
created: 2026-08-23
updated: 2026-08-23
---
# On Lazy Training in Differentiable Programming
> [!abstract] 来源定位
> 说明 lazy training 不只由神经网络过参数化触发，也与常被隐式忽略的模型 scaling 有关；给出 nonlinear path 与 linearized path 的接近界，并展示实际深 CNN 进入更 lazy regime 时性能可能下降。本库调用 scaling 边界与 lazy/rich 对照。
## 本库调用
1. lazy training 的 scaling 起源；
2. nonlinear/linearized path distance；
3. kernel-equivalent regime；
4. “宽/参数多”并非充分条件；
5. lazy regime 的经验局限。

