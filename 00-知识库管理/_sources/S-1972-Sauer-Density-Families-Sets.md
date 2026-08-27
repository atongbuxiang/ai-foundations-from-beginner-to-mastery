---
type: source
status: active
area: [sources, combinatorics, learning-theory]
source_type: paper
title: "On the Density of Families of Sets"
author: [Norbert Sauer]
year: 1972
url: "https://doi.org/10.1016/0097-3165(72)90019-2"
accessed: 2026-08-20
source_tier: A
license: "Copyrighted journal article; retain bibliographic data, independent proof, and DOI only"
scope_role: primary
temporal_role: classical-foundation
related: ["[[增长函数与经验二分模式]]", "[[Sauer-Shelah 引理]]", "[[VC 一致收敛与泛化界]]"]
created: 2026-08-20
updated: 2026-08-20
---

# Sauer：集合族的密度

> [!abstract] 来源定位
> Sauer 证明了极值集合论中的核心二分：一个集合族若不能在某个规模上实现全部子集，其在更大有限集合上的迹数至多按固定次数多项式增长。学习理论把集合族解释为 binary hypotheses 的正类集合，得到增长函数上界。

## 元数据

- N. Sauer, “On the Density of Families of Sets,” *Journal of Combinatorial Theory, Series A*, 13, 145–147, 1972；
- DOI：[10.1016/0097-3165(72)90019-2](https://doi.org/10.1016/0097-3165(72)90019-2)；
- 原始语言：集合族及其在有限子集上的 traces；
- 课程语言：若 $\operatorname{VCdim}(\mathcal H)=d$，则
  $$
  \tau_{\mathcal H}(m)\le\sum_{i=0}^{d}{m\choose i}.
  $$

## 课程重建路线

本库不用“结论显然由组合论得到”的黑箱写法，而是固定最后一点，把 traces 分为“至少出现一种标签”的投影族和“两个标签都出现”的双实现族，证明递推

$$
T_d(m)\le T_d(m-1)+T_{d-1}(m-1),
$$

再由 Pascal 恒等式闭合归纳。

> [!important] 锐性
> $\{A\subseteq[m]:|A|\le d\}$ 恰有 $\sum_{i=0}^{d}{m\choose i}$ 个集合且 VC 维为 $d$，所以 binomial-sum 形式不能在只知道 $(m,d)$ 时统一改小。
