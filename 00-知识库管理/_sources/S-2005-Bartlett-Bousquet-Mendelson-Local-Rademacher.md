---
type: source
status: active
area: [sources, learning-theory, local-complexity]
source_type: paper
title: "Local Rademacher Complexities"
author: [Peter L. Bartlett, Olivier Bousquet, Shahar Mendelson]
year: 2005
url: "https://doi.org/10.1214/009053605000000282"
accessed: 2026-08-23
source_tier: A
license: "Annals of Statistics article; retain citation, independent derivations, and official article/arXiv links"
venue: "The Annals of Statistics 33(4), 1497–1537"
scope_role: primary
temporal_role: classical-foundation
related: ["[[局部 Rademacher 复杂度与快收敛率]]", "[[覆盖数、Metric Entropy 与 Chaining 入口]]", "[[正则化 ERM 的稳定性]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Local Rademacher Complexities

> [!abstract] 来源定位
> Bartlett、Bousquet 与 Mendelson 以局部、经验 Rademacher averages 建立更细的误差界，并以 sub-root function、fixed point、star hull 与 empirical localization 处理可计算性。本库用它承担“全局类—局部切片—固定点—快率”的正式骨架。

## 元数据与纳入

- 正式引用：Bartlett, P. L., Bousquet, O. & Mendelson, S. (2005), *The Annals of Statistics* 33(4), 1497–1537；
- DOI：[10.1214/009053605000000282](https://doi.org/10.1214/009053605000000282)；
- 作者开放版本：[arXiv](https://arxiv.org/abs/math/0508275)；
- 证据角色：localized data-dependent complexity、sub-root fixed point 与 fast-rate proof 的原始主线；
- 版权边界：不复制原图或长段文字；课程用独立图、玩具固定点和分层证明说明。

## 本库调用的断言

1. 接近最优风险或具有较小方差/二阶矩的 loss difference 子类可能远小于全局类；
2. local complexity 常由 nondecreasing sub-root upper envelope 控制，其 fixed point 给出自洽误差尺度；
3. peeling、star hull 与 variance–expectation/Bernstein 条件是把局部随机过程转成 uniform excess-risk bound 的关键；
4. empirical local complexity 需要专门 theorem 与膨胀常数，不能直接用训练误差筛类后当作 fixed class；
5. 快于 $m^{-1/2}$ 的 rate 还需 curvature/noise/variance 条件，localization 名称本身不是保证。

> [!warning] 课程中的 schematic bound
> 正文会用 $\lesssim$ 展示 fixed-point 机制，并把常数依赖留在正式定理卡片中。不同 loss、star hull、sub-root envelope 与 empirical radius 的完整条件不可互换。

## 后续调用

- [[局部 Rademacher 复杂度与快收敛率]]：主证明机制；
- [[经典模型与模型选择 MOC]]：localized penalty 与 oracle inequality；
- [[神经网络容量与 Norm-Based Bound]]：为什么现代深网的 local certificate 仍需可验证几何。
