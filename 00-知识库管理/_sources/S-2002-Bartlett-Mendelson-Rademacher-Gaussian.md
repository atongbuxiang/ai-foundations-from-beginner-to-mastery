---
type: source
status: active
area: [sources, learning-theory, empirical-process]
source_type: paper
title: "Rademacher and Gaussian Complexities: Risk Bounds and Structural Results"
author: [Peter L. Bartlett, Shahar Mendelson]
year: 2002
url: "https://www.jmlr.org/papers/v3/bartlett02a.html"
accessed: 2026-08-23
source_tier: A
license: "JMLR article; retain citation, independent derivations, and official article/PDF links"
venue: "Journal of Machine Learning Research 3, 463–482"
scope_role: primary
temporal_role: classical-foundation
related: ["[[Ghost Sample、对称化与经验过程入口]]", "[[Rademacher 复杂度与经验复杂度]]", "[[收缩引理与 Lipschitz 损失复合]]", "[[范数约束线性类的复杂度]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Rademacher and Gaussian Complexities

> [!abstract] 来源定位
> Bartlett 与 Mendelson 2002 系统研究 Rademacher/Gaussian data-dependent complexity、风险界和函数类组合结构，并展示其在线性类、SVM、决策树与神经网络中的接口。本库用它校准“随机符号拟合能力—风险界—结构运算”的主线；具体常数按每个节点明确采用的定义重新推导。

## 元数据与纳入

- 论文主页：[JMLR](https://www.jmlr.org/papers/v3/bartlett02a.html)；
- 官方全文：[PDF](https://jmlr.org/papers/volume3/bartlett02a/bartlett02a.pdf)；
- 正式引用：Bartlett, P. L. & Mendelson, S. (2002), JMLR 3, 463–482；
- 证据角色：data-dependent complexity 与 general risk bound 的原始主干之一；
- 版权边界：不复制原图或长段文字，只记录独立定义、证明、例子和链接。

## 本库调用的断言

1. ghost-sample symmetrization 可把总体—经验偏差上界为随机符号过程；
2. empirical Rademacher complexity 条件于真实样本，反映该样本上的函数值几何；
3. convex hull、线性组合、Lipschitz composition 等结构运算有相应复杂度演算规则；
4. complexity penalty 与 empirical loss 可组合成 high-probability risk certificate；
5. data-dependent 不等于自动 tight：还要计算数值、处理置信修正并核对 sampling/loss contract。

> [!warning] 常数与 convention
> 文献可能在 $1/m$ 或 $2/m$、signed supremum 或 absolute supremum、one-sided 或 two-sided gap 上采用不同定义。课程所有定理先固定 convention，再追踪常数；不能只按“Rademacher bound”名称拼接公式。

## 后续调用

- [[Ghost Sample、对称化与经验过程入口]]：双样本与随机交换；
- [[Rademacher 复杂度与经验复杂度]]：定义、Massart lemma 与风险界；
- [[收缩引理与 Lipschitz 损失复合]]：loss composition；
- [[范数约束线性类的复杂度]]：dual norm 计算；
- [[分类间隔、Margin Bound 与 SVM 接口]]和[[局部 Rademacher 复杂度与快收敛率]]。
