---
type: source
status: verified
area: [sources, optimization, numerical-methods]
source_type: textbook
title: "Numerical Optimization, Second Edition"
author: [Jorge Nocedal, Stephen J. Wright]
year: 2006
url: "https://link.springer.com/book/10.1007/978-0-387-40065-5"
accessed: 2026-08-26
source_tier: A
scope_role: foundational
temporal_role: reference
related: ["[[Newton、Damping、Trust Region 与 Levenberg–Marquardt]]", "[[Hessian-vector Product、共轭梯度与隐式二阶步]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Nocedal–Wright：Numerical Optimization

> [!abstract] 来源定位
> Trust region、CG/inexact Newton、nonlinear least squares 与 Levenberg–Marquardt 的权威教材骨架。课程采用 quadratic model、actual/predicted reduction、Cauchy decrease、damping 与 residual 条件；具体深网实现和 stochastic evidence 另行审计。

## 课程采用

- Newton step 只在 Hessian 可逆且局部模型可信时直接使用；
- trust-region ratio 同时控制接受/拒绝与半径调整，不能只看 loss 是否下降；
- $B+\lambda I$ 的 regularized solve 与固定半径 trust-region 有拉格朗日乘子联系，但算法状态不必相同；
- nonlinear least squares 的 Gauss–Newton/LM 保留 residual Jacobian 与遗漏二阶项；
- truncated CG 必须记录 residual、negative curvature、boundary hit 和预条件成本。

## 证据边界

教材定理依赖平滑、有界 level set、充分 model decrease 等条件；它不自动给 stochastic minibatch Hessian、低精度 HVP 或任意深网全局收敛保证。
