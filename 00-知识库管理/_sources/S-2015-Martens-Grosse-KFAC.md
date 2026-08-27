---
type: source
status: verified
area: [sources, curvature, natural-gradient, kronecker]
source_type: paper
title: "Optimizing Neural Networks with Kronecker-factored Approximate Curvature"
author: [James Martens, Roger Grosse]
year: 2015
url: "https://proceedings.mlr.press/v37/martens15.html"
venue: "ICML 2015, PMLR 37:2408–2417"
accessed: 2026-08-26
source_tier: A
scope_role: primary
temporal_role: foundational
related: ["[[K-FAC、Kronecker 分块与阻尼合同]]", "[[自然梯度、KL 局部几何与坐标不变性]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Martens–Grosse：K-FAC

> [!abstract] 来源定位
> K-FAC 的原始来源。方法以层为块，把 Fisher block 中 activation 与 preactivation-gradient 的二阶乘积近似分离为两个较小矩阵的 Kronecker product，从而获得非对角且可逆的近似。

## 课程采用

线性层 $s=Wa$ 的样本梯度满足 $\nabla_W\ell=\delta a^T$，向量化后为 $a\otimes\delta$，故 block outer product 为

$$
(aa^T)\otimes(\delta\delta^T).
$$

K-FAC 用 $\mathbb E[aa^T]\otimes\mathbb E[\delta\delta^T]$ 近似乘积的期望。这里包含 layer-block、跨样本/空间共享、独立性与 Fisher 估计等假设。Factored damping 不等于给完整 Kronecker block 精确加 $\lambda I$；inverse refresh、EMA 与 norm constraint 都属于算法合同。
