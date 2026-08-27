---
type: source
status: verified
area: [sources, optimization, muon]
source_type: research-blog
title: "Muon: An Optimizer for Hidden Layers in Neural Networks"
author: [Keller Jordan, Yuchen Jin, Vlado Boza, Jiacheng You, Franz Cesista, Laker Newhouse, Jeremy Bernstein]
year: 2024
url: "https://kellerjordan.github.io/posts/muon/"
accessed: 2026-08-26
source_tier: B
scope_role: algorithm-origin-and-implementation
temporal_role: foundational-current
related: ["[[Muon 的动量、正交化与参数分组合同]]", "[[Muon 形状缩放、Update RMS 与版本差异]]", "[[Muon 的扩展证据、系统成本与迁移边界]]"]
---

# S-2024 Jordan - Muon

## 核心贡献

- 将 Muon 明确定义为：对二维 hidden-layer 参数的 SGD/Nesterov momentum update 做有限步 Newton–Schulz orthogonalization；
- 给出系数 $(3.4445,-4.7750,2.0315)$、Frobenius 归一化、5 步 BF16 参考实现；
- 明确 embedding、output head、bias/vector 等参数使用其他优化器，并讨论 Q/K/V 分组；
- 提供 NanoGPT、CIFAR 与 1.5B 早期实证和 FLOP-overhead 估算。

## 采用边界

算法定义和作者实现语义可直接引用；“rare directions”属于机制假说，速度结果限于所列任务、硬件、代码和调参环境。有限步多项式不是精确 SVD/polar，必须另报奇异值与正交残差。
