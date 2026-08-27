---
type: source
status: active
area: [sources, deep-generalization, uniform-convergence]
source_type: paper
title: "Uniform convergence may be unable to explain generalization in deep learning"
author: [Vaishnavh Nagarajan, J. Zico Kolter]
year: 2019
url: "https://proceedings.neurips.cc/paper/2019/hash/05e97c207235d63ceb1db43c60db7bbb-Abstract.html"
accessed: 2026-08-23
source_tier: A
license: "NeurIPS proceedings; retain citation"
venue: "Advances in Neural Information Processing Systems 32"
scope_role: primary
temporal_role: modern-theory
related: ["[[深度泛化证据地图与开放问题]]", "[[VC 维、一致收敛与 ERM 泛化]]"]
created: 2026-08-23
updated: 2026-08-23
---
# Uniform Convergence May Be Unable to Explain
> [!abstract] 来源定位
> 展示若干已有深网 uniform-convergence bounds 的反常 sample-size trend，并构造过参数化线性/神经设置，使某类 two-sided uniform convergence 即使限制到 GD 输出仍 vacuous。本库保留标题中的“may”与定理量词，不将其写成全部一致收敛或学习理论的不可能性。
## 本库调用
1. numerical vacuity 之外的 trend failure；
2. two-sided supremum 的坏点主导；
3. algorithm-dependent restriction 的反例；
4. 结论范围与量词；
5. stability/other tools 的开放接口。

