---
type: source
status: active
area: [sources, learning-theory, algorithmic-stability]
source_type: paper
title: "Stability and Generalization"
author: [Olivier Bousquet, André Elisseeff]
year: 2002
url: "https://jmlr.org/papers/v2/bousquet02a.html"
accessed: 2026-08-23
source_tier: A
license: "JMLR article; retain citation, independent derivations, and official article/PDF links"
venue: "Journal of Machine Learning Research 2, 499–526"
scope_role: primary
temporal_role: classical-foundation
related: ["[[算法稳定性与替换一个样本]]", "[[正则化 ERM 的稳定性]]", "[[随机梯度算法的稳定性接口]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Stability and Generalization

> [!abstract] 来源定位
> Bousquet 与 Elisseeff 把学习算法对单个训练样本删除/替换的敏感性转成 generalization 与 leave-one-out bounds，并分析 regularization-based algorithms。它是本库“具体算法的敏感性，而非整个假设类的最坏容量”路线的原始骨架。

## 元数据与纳入

- 论文主页：[JMLR](https://jmlr.org/papers/v2/bousquet02a.html)；
- 官方全文：[PDF](https://www.jmlr.org/papers/volume2/bousquet02a/bousquet02a.pdf)；
- 正式引用：Bousquet, O. & Elisseeff, A. (2002), *JMLR* 2, 499–526；
- 证据角色：uniform/hypothesis/pointwise stability、generalization bias identity、bounded-loss high-probability bound 与 regularized Hilbert-space algorithms；
- 版权边界：不复制原图或长段文字；正文按 replace-one convention 独立重推。

## 本库调用的断言

1. stability 必须同时声明算法、损失、邻接关系和随机性量词；
2. uniform stability 可通过 ghost replacement identity 控制期望 generalization gap；
3. bounded loss 与 bounded differences 可进一步给出 high-probability statement；
4. 删除一个样本的稳定性与替换一个样本的稳定性相差至多一次三角不等式的常数；
5. convex loss 加 strongly convex regularizer 可把训练集扰动转成输出/损失扰动；
6. 稳定只控制 train–population gap，不单独保证 risk 很小。

> [!warning] 本库的 convention
> 原文核心定义以删除一个样本为主；本库 LT-33—35 以“同样大小的数据集只替换一个坐标”为邻接关系，并将对应 loss difference 直接记为 $\beta_m$。因此引用原文常数前必须先完成 deletion/replacement 换算。

## 后续调用

- [[算法稳定性与替换一个样本]]：定义、期望恒等式和经典 bounded-loss tail；
- [[正则化 ERM 的稳定性]]：strong convexity cancellation；
- [[随机梯度算法的稳定性接口]]：从 exact minimizer 过渡到 iterative algorithm。
