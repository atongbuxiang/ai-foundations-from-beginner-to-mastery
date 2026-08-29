---
type: source
status: active
area: [sources, neural-networks, residual-networks, initialization, transformers]
source_type: paper
title: "ReZero is All You Need: Fast Convergence at Large Depth"
author: "Thomas Bachlechner; Bodhisattwa Prasad Majumder; Huanru Henry Mao; Garrison W. Cottrell; Julian McAuley"
year: 2021
url: "https://proceedings.mlr.press/v161/bachlechner21a.html"
venue: "UAI 2021, PMLR 161"
accessed: 2026-08-29
source_tier: A
license: "PMLR paper；本库仅保存独立摘要、必要公式与链接"
scope_role: core
temporal_role: modern-foundational
related: ["[[ReZero、Fixup、DeepNorm 与深网缩放]]", "[[正交初始化与 Dynamical Isometry]]", "[[残差缩放、Lipschitz 界与深度稳定性]]"]
created: 2026-08-23
updated: 2026-08-29
---

# Bachlechner et al.：ReZero

> [!abstract] 来源定位
> ReZero 在每个 residual branch 前加入零初始化的可学习标量，使初始网络成为恒等映射并获得初始 dynamical-isometry 基线。它承担方法定义与论文实验；本库特别补充第一步参数梯度的分层结构，避免把“初始 Jacobian 为 $I$”误说成全部参数立刻学习。

## 方法合同

$$
x_{\ell+1}=x_\ell+\alpha_\ell F_\ell(x_\ell;\theta_\ell),
\qquad
\alpha_\ell(0)=0.
$$

因此初始 state Jacobian 为 $I$。但若上游梯度为 $g_{\ell+1}$，则

$$
\nabla_{\theta_\ell}\mathcal L
=\alpha_\ell J_{\theta_\ell}F_\ell^\mathsf T g_{\ell+1}=0,
$$

而

$$
\frac{\partial\mathcal L}{\partial\alpha_\ell}
=g_{\ell+1}^\mathsf T F_\ell(x_\ell)
$$

通常不为零。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| RZ-C1 | 零 gate 令初始状态映射为恒等 | 代数 | shortcut 真为 identity | 精确 |
| RZ-C2 | 初始输入—输出 Jacobian 奇异值均为 1 | 代数 | 同上且忽略非恒等首尾层 | 局部精确 |
| RZ-C3 | branch 内所有参数第一步都有梯度 | 梯度命题 | 被 $\alpha=0$ 乘掉 | 一般错误 |
| RZ-C4 | ReZero 普遍取代 normalization | 经验外推 | 任务、深度、优化和系统依赖 | 原论文不足以支持 |

## 失败边界

若 $F_\ell(x_\ell)$ 也被构造为精确零，则 $\partial\mathcal L/\partial\alpha_\ell$ 可能同时为零，形成第一步死锁。零初始化必须沿计算图逐参数审计。
