---
type: source
status: active
area: [sources, equivariance, group-convolution, symmetry]
source_type: paper
title: "Group Equivariant Convolutional Networks"
author: [Taco S. Cohen, Max Welling]
year: 2016
url: "https://proceedings.mlr.press/v48/cohenc16.html"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and theorem conditions"
venue: "ICML 2016"
scope_role: primary
temporal_role: classical-foundation
related: ["[[数据增强、不变性、等变性与任务充分性]]", "[[Lie 群、Lie 代数与对称性]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Group Equivariant Convolutional Networks

> [!abstract] 来源定位
> 给出离散群作用下 group convolution 的结构性等变设计。本库调用其 $h(gx)=\rho(g)h(x)$ 合同、weight sharing 与 invariant readout 接口；具体 sample-complexity 改善只在论文设定与相应假设下解释。

## 本库调用

1. invariant representation 与 equivariant feature map 不是同一对象；
2. architecture 可把 symmetry hard-code，而 augmentation 是训练分布修改；
3. pooling 可把等变 feature 变成不变 readout；
4. boundary/padding 与离散化可能破坏精确等变；
5. symmetry 必须由任务而不是视觉直觉指定。
