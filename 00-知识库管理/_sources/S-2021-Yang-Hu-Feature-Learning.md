---
type: source
status: verified
area: [sources, feature-learning, infinite-width, parameterization]
source_type: paper
title: "Tensor Programs IV: Feature Learning in Infinite-Width Neural Networks"
author: [Greg Yang, Edward J. Hu]
year: 2021
url: "https://proceedings.mlr.press/v139/yang21c.html"
accessed: 2026-08-23
source_tier: A
license: "PMLR open proceedings; retain citation"
venue: "ICML 2021, PMLR 139"
scope_role: primary
temporal_role: modern-theory
related: ["[[Mean-Field、Feature Learning 与训练 Regime]]", "[[NTK、Lazy Training 与 Kernel Regime]]", "[[Standard、NTK 与 Mean-field 参数化]]", "[[μP 的 Maximal Update 与宽度尺度推导]]"]
created: 2026-08-23
updated: 2026-08-23
---
# Feature Learning in Infinite-Width Neural Networks
> [!abstract] 来源定位
> 研究不同 parameterization 的无限宽训练极限，指出标准/NTK 参数化的相应极限不保留 feature learning，并构造可在极限中发生最大 feature update 的参数化。本库调用“infinite width 不等于 fixed kernel”和 parameterization-defined regime。
## 本库调用
1. kernel vs feature-learning dichotomy；
2. parameterization 的决定性；
3. transfer/Word2Vec 等 feature-dependent 对照；
4. maximal-update 极限；
5. finite-width 趋势的实验接口。
