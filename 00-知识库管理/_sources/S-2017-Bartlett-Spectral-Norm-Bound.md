---
type: source
status: active
area: [sources, deep-generalization, norm-bound]
source_type: paper
title: "Spectrally-normalized margin bounds for neural networks"
author: [Peter L. Bartlett, Dylan J. Foster, Matus J. Telgarsky]
year: 2017
url: "https://proceedings.neurips.cc/paper/2017/hash/b22b257ad0519d4500539da3c8bcf4dd-Abstract.html"
accessed: 2026-08-23
source_tier: A
license: "NeurIPS proceedings; retain citation"
venue: "Advances in Neural Information Processing Systems 30"
scope_role: primary
temporal_role: modern-theory
related: ["[[神经网络容量与 Norm-Based Bound]]"]
created: 2026-08-23
updated: 2026-08-23
---
# Spectrally-Normalized Margin Bounds
> [!abstract] 来源定位
> 以各层 spectral norms 的乘积、相对 Frobenius/参考矩阵距离与 margin 建立神经网络泛化界，并强调相较参数数更具结构的深度/宽度依赖。本库调用 bound architecture、perturbation/covering 思路与 margin 接口；精确公式按论文 theorem，不以教学示意式替代。
## 本库调用
1. spectral-product 增益；
2. layerwise perturbation 与 covering；
3. Frobenius/spectral 修正；
4. margin risk bridge；
5. 精确 theorem 与 schematic 的区分。

