---
type: source
status: active
area: [sources, probability, learning-theory]
source_type: paper
title: "Probability Inequalities for Sums of Bounded Random Variables"
author: Wassily Hoeffding
year: 1963
url: "https://doi.org/10.1080/01621459.1963.10500830"
accessed: 2026-08-20
source_tier: A
license: "Publisher-copyrighted article; retain citation, independent derivations and DOI link only"
venue: Journal of the American Statistical Association 58(301), 13–30
scope_role: backbone
temporal_role: classical-foundation
related: ["[[浓缩不等式]]", "[[泛化间隙与浓缩不等式接口]]", "[[有限假设类、Union Bound 与一致收敛]]"]
created: 2026-08-20
updated: 2026-08-20
---

# Probability Inequalities for Sums of Bounded Random Variables

> [!abstract] 来源定位
> Hoeffding 1963 为独立有界随机变量和的尾概率提供指数上界。本库在概率卷推导 MGF/Chernoff 主线，在学习理论中只调用一个清楚的 corollary：对抽样前固定且损失落在 $[0,1]$ 的 predictor，经验风险以 $e^{-2m\varepsilon^2}$ 量级集中到总体风险。data-dependent learner 需要 union/uniform/stability 等额外步骤。

## 元数据与纳入

- 正式引用：Hoeffding, W. (1963), *Probability Inequalities for Sums of Bounded Random Variables*, JASA 58(301), 13–30；
- DOI：[10.1080/01621459.1963.10500830](https://doi.org/10.1080/01621459.1963.10500830)；
- 当前调用者：[[浓缩不等式]]、[[泛化间隙与浓缩不等式接口]]、[[有限假设类、Union Bound 与一致收敛]]；
- 版权边界：不保存原文副本，只保留独立证明、公式与引用。

## 课程采用的形式

若 $X_1,\ldots,X_m$ 独立且 $X_i\in[a_i,b_i]$，则

$$
\Pr\left(
\sum_i(X_i-\mathbb EX_i)\ge t
\right)
\le
\exp\left(
-\frac{2t^2}{\sum_i(b_i-a_i)^2}
\right).
$$

若 $X_i\in[0,1]$ i.i.d.，对均值有两侧形式

$$
\Pr(|\overline X-\mathbb EX|>\varepsilon)
\le2e^{-2m\varepsilon^2}.
$$

学习理论中令 $X_i=\ell(h,Z_i)$，但成立前必须固定 $h$。

## 断言审计

| 断言 | 条件 | 课程判断 |
|---|---|---|
| 有界独立和有 sub-Gaussian tail | 独立、边界确定 | 采用 |
| 任意训练输出 $h_S$ 都可直接代入 fixed-$h$ bound | $h_S$ 依同一 $S$ | 否定 |
| $[0,1]$ loss 的半径只依 $m,\delta$ | fixed query/predictor | 采用 |
| Hoeffding 利用了真实方差 | 只用 range，可能较松 | 否定 |
| 数据相关时原常数照搬 | 产品结构缺失 | 否定 |

## 已生成与后续调用

- [x] [[浓缩不等式]]：Hoeffding lemma、MGF 与 range-sensitive theorem；
- [x] [[泛化间隙与浓缩不等式接口]]：fixed hypothesis 风险证书；
- [x] [[有限假设类、Union Bound 与一致收敛]]：有限次 simultaneous control；
- [ ] LT-13：agnostic ERM 的 $1/\varepsilon^2$ 样本复杂度。

