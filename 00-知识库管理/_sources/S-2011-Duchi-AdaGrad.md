---
type: source
status: verified
area: [sources, optimization, adaptive-methods, online-learning]
source_type: paper
title: "Adaptive Subgradient Methods for Online Learning and Stochastic Optimization"
author: "John Duchi; Elad Hazan; Yoram Singer"
year: 2011
url: "https://jmlr.org/papers/v12/duchi11a.html"
venue: "JMLR 12(61):2121–2159"
accessed: 2026-08-26
source_tier: A
license: "JMLR 论文；本库仅保存独立摘要、必要公式与链接"
scope_role: foundational
temporal_role: historical-foundational
related: ["[[AdaGrad、累计平方梯度与稀疏几何]]", "[[自适应优化方法]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Duchi、Hazan、Singer：AdaGrad

> [!abstract] 来源定位
> AdaGrad 的正式来源。论文从在线/随机优化的 variable metric 与 proximal geometry 推出自适应更新，并给出 data-dependent regret guarantees；“稀有特征得到较大步长”是结果直觉，不替代约束、正则项和证明条件。

## 课程采用

- 对角形式的累计量 $G_{t,ii}=\sum_{s\le t}g_{s,i}^2$；
- 预条件方向 $G_t^{-1/2}g_t$ 与坐标频率直觉；
- full-matrix 与 diagonal 版本的对象差异；
- regret bound 依赖凸性、可行域与在线序列合同，不外推为深网全局收敛定理。

## 断言审计

| 断言 | 等级 | 边界 |
|---|---|---|
| 累计平方梯度定义了随数据改变的 metric | 定义/推导 | 需声明 full/diagonal、regularization 与投影 |
| 稀有非零坐标通常保留较大有效步长 | 条件性解释 | 还依赖梯度幅值而不只出现次数 |
| AdaGrad 在所有非平稳任务上都会停滞 | 经验外推 | 累计量单调增长是真；训练效果需另证 |

## 复算要求

从一维与二维在线线性损失出发，手算累计量、有效步长和 regret 项；再构造“稀有但巨大梯度”反例，阻止把频率与尺度混为一谈。
