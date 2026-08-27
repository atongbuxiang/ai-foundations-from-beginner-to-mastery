---
type: source
status: verified
area: [sources, tensor-programs, ntk, infinite-width]
source_type: paper
title: "Tensor Programs II: Neural Tangent Kernel for Any Architecture"
author: [Greg Yang]
year: 2020
url: "https://arxiv.org/abs/2006.14548"
code: "https://github.com/thegregyang/NTK4A"
accessed: 2026-08-26
source_tier: A
scope_role: primary-theory
temporal_role: modern-theory
related: ["[[Standard、NTK 与 Mean-field 参数化]]", "[[Tensor Programs、坐标检查与无限宽极限]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Tensor Programs II：初始化 NTK 极限

> [!abstract] 来源定位
> 论文证明一大类随机初始化网络的 NTK 在宽度趋于无穷时收敛到确定性极限，并给出 Tensor Programs 计算框架。本卷主要调用其对象合同与 Simple GIA Check，而不把标题中的“any architecture”误读成无条件覆盖所有程序、所有宽度路径和整个训练过程。

## 正文采用

- 初始化时 kernel 的随机性可在规定宽度极限下消失；
- forward 中使用权重、backward 中使用转置时，朴素 gradient-independence assumption 可能失败；
- Simple GIA Check 是判断独立性捷径能否给出正确极限的结构检查；
- covariance recursion、shape ratio 与 shared-weight 使用方式必须进入 theorem contract。

## 限制

该论文的初始化 NTK 结论与训练动力学结论分开；训练期间的 kernel-gradient-descent 极限由 Tensor Programs IIb 补上。确定性无限宽 kernel 也不说明有限网络已足够宽，更不自动说明 feature learning 的有限宽优势或劣势。

