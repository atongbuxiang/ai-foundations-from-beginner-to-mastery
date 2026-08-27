---
type: source
status: verified
area: [sources, generative-models, gan, game-dynamics]
source_type: paper
title: "Which Training Methods for GANs do actually Converge?"
author: "Lars Mescheder; Andreas Geiger; Sebastian Nowozin"
year: 2018
url: "https://arxiv.org/abs/1801.04406"
venue: "ICML 2018"
accessed: 2026-08-25
source_tier: A
license: "论文页面；本库仅保存独立摘要、必要公式与链接"
scope_role: convergence-boundary
temporal_role: foundational
related: ["[[Minimax 动力学、旋转、阻尼与局部收敛]]", "[[GAN 稳定化方法、受控比较与证据地图]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Mescheder et al.：GAN 局部收敛与反例

> [!abstract] 来源定位
> 论文用低维流形/Dirac-GAN 等原型展示未正则 GAN、有限 critic updates 的 WGAN/WGAN-GP 不保证收敛，并证明特定 zero-centered penalties/instance noise 下的局部结果。课程采用其 Jacobian 与反例，不把局部简化模型定理外推为现代大网络全局保证。

## 断言审计

| 断言 | 类型 | 条件/边界 | 课程判断 |
|---|---|---|---|
| 纯旋转 Jacobian 可导致 simultaneous GDA 绕圈/发散 | 线性局部分析 | 指定 game 与步长 | 精确 |
| 有限 discriminator updates 的 WGAN-GP 总收敛 | 普遍主张 | 存在反例 | 错误 |
| zero-centered penalty 可给局部收敛 | 定理 | 论文正则、局部与正则性条件 | 有条件成立 |
| 实验稳定等于已到 Nash equilibrium | 诊断外推 | 指标有限 | 不成立 |

