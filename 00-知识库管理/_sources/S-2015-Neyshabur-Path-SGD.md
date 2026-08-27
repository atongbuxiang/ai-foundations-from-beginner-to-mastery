---
type: source
status: active
area: [sources, path-norm, rescaling-invariance, optimization-geometry]
source_type: paper
title: "Path-SGD: Path-Normalized Optimization in Deep Neural Networks"
author: [Behnam Neyshabur, Ruslan Salakhutdinov, Nathan Srebro]
year: 2015
url: "https://proceedings.neurips.cc/paper/2015/hash/eaa32c96f620053cf442ad32258076b9-Abstract.html"
accessed: 2026-08-23
source_tier: A
license: "Open NeurIPS article; retain citation"
venue: "NeurIPS 2015"
scope_role: primary
temporal_role: modern-method
related: ["[[范数、平坦性、Sharpness 与参数化不变性]]", "[[神经网络容量与 Norm-Based Bound]]"]
created: 2026-08-23
updated: 2026-08-23
---
# Path-SGD
> [!abstract] 来源定位
> 提出对 ReLU node-wise rescaling 不变的 path-wise geometry 与 Path-SGD。本库调用 path product 的不变性动机；优化实证与泛化 tightness 分开。
## 本库调用
1. node rescaling；
2. path regularizer；
3. invariant geometry；
4. Path-SGD；
5. invariance 不等于 sufficient explanation。
