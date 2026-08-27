---
type: source
status: verified
area: [sources, tensor-programs, ntk, training-dynamics]
source_type: paper
title: "Tensor Programs IIb: Architectural Universality of Neural Tangent Kernel Training Dynamics"
author: [Greg Yang, Etai Littwin]
year: 2021
url: "https://arxiv.org/abs/2105.03703"
accessed: 2026-08-26
source_tier: A
venue: "ICML 2021"
scope_role: primary-theory
temporal_role: modern-theory
related: ["[[Standard、NTK 与 Mean-field 参数化]]", "[[Tensor Programs、坐标检查与无限宽极限]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Tensor Programs IIb：NTK 训练动力学

> [!abstract] 来源定位
> 论文把固定有限步 SGD 动力学写入 Tensor Program，证明规定 NTK 参数化下，一大类架构的无限宽训练遵循由无限宽 NTK 决定的函数空间 kernel gradient descent。

## 正文采用

- “lazy/kernel regime”是参数化、学习率、时间尺度和极限次序共同定义的训练对象；
- 初始化 kernel 有极限，不足以推出训练全过程使用同一 kernel；IIb 补的是训练动力学；
- 宽层通常沿固定比例共同趋于无穷，不能把任意先后取极限或 width–depth 联合缩放默认为同一结果；
- 有限网络可用 hidden-feature change、NTK drift 与跨宽曲线检查其离极限的距离。

## 证据边界

“架构普适”受论文所定义的程序类、参数化与训练时域约束；它不等于所有现代算子、权重共享、离散路由、长期训练或宽深联合极限都已覆盖。

