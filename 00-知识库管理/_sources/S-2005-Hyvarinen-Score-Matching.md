---
type: source
status: verified
area: [sources, generative-models, score-matching, statistics]
source_type: paper
title: "Estimation of Non-Normalized Statistical Models by Score Matching"
author: "Aapo Hyvärinen"
year: 2005
url: "https://www.jmlr.org/papers/v6/hyvarinen05a.html"
venue: "JMLR 6"
accessed: 2026-08-25
source_tier: A
license: "JMLR 开放论文；本库仅保存独立摘要、必要公式与链接"
scope_role: foundational
temporal_role: foundational
related: ["[[Score Matching、分部积分与配分函数消去]]", "[[去噪 Score Matching、Tweedie 公式与条件期望]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Hyvärinen：Score Matching

> [!abstract] 来源定位
> 原始 score matching 以数据变量的 log-density 梯度定义 Fisher divergence，并借分部积分把未知数据 score 消去。它同时消去 $Z_\theta$，但要求连续变量、足够光滑以及明确的 boundary contract。

## 定理骨架

令 $s_\theta=\nabla_x\log p_\theta$、$s_*=\nabla_x\log p_*$：

$$
J(\theta)=\frac12E_{p_*}\|s_\theta-s_*\|^2.
$$

在边界项消失时，去掉与 $\theta$ 无关常数：

$$
J(\theta)\equiv
E_{p_*}\left[\frac12\|s_\theta(X)\|^2+
\nabla\!\cdot s_\theta(X)\right].
$$

## 不能省略的条件

- $p_*$ 与模型 score 可微并可积；
- 分部积分的 boundary flux 消失；
- 连通 support 上 score 相同只确定密度到常数，再由归一化固定；
- 离散数据、带边界 support 和奇异流形不能照搬欧氏公式；
- 目标可计算不等于 Hessian trace 便宜或 estimator 低方差。

