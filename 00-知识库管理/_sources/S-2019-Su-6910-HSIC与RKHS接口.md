---
type: source
status: draft
area: [sources, math/rkhs, ai/dependence-measures, math/functional-analysis]
source_type: blog
title: "HSIC简介：一个有意思的判断相关性的思路"
author: 苏剑林
year: 2019
url: "https://spaces.ac.cn/archives/6910"
accessed: 2026-08-19
source_tier: C
license: "科学空间站点声明存在版本差异；仅保存独立摘要、短公式与链接"
site_category: [数学研究]
scope_role: bridge
temporal_role: classical-exposition
related: ["[[Banach 空间、Hilbert 空间与正交投影]]", "[[有界算子、紧算子与谱理论基础]]", "[[正定核、RKHS 与表示定理]]", "[[互信息与依赖性]]", "[[f-散度、Bregman 散度与概率度量]]"]
created: 2026-08-19
updated: 2026-08-19
---

# HSIC简介：一个有意思的判断相关性的思路

> [!abstract] 来源定位
> 文章用核特征函数与采样期望直观引出 HSIC。课程只采用“函数空间—正交展开—kernel trick—经验估计”的问题链，并明确修正“任意核都能由 HSIC=0 判独立”的过强表述；正式 RKHS、cross-covariance operator与 characteristic kernel条件留 GEO-06/07。

## 元数据与纳入

- 正式引用：苏剑林，2019-08-26，《HSIC简介：一个有意思的判断相关性的思路》；
- 页面：[https://spaces.ac.cn/archives/6910](https://spaces.ac.cn/archives/6910)；
- 当前调用者：[[Banach 空间、Hilbert 空间与正交投影]]、[[有界算子、紧算子与谱理论基础]]与[[正定核、RKHS 与表示定理]]；
- 文章自述偏通俗，本卡不把其省略条件的叙述当正式 theorem。

## 核心问题

对 test functions $f,g$，依赖可由

$$
C[f,g]=\mathbb E[f(X)g(Y)]
-\mathbb E[f(X)]\mathbb E[g(Y)]
$$

探测。若把 test functions组织进 RKHS，cross-covariance可成为 Hilbert–Schmidt operator，HSIC是相应 squared norm，并可由 kernel evaluations估计。

## 断言与课程判断

| ID | 断言 | 条件/边界 | 判断 |
|---|---|---|---|
| C1 | Function families可作为依赖probes | 需足够rich的class与integrability | 采用 |
| C2 | Kernel expansion可把basis sums化为kernel expectations | positive kernel/RKHS与operator条件 | 待GEO-07补严 |
| C3 | HSIC可由samples和Gram matrices估计 | estimator有biased/unbiased variants | 采用并分型 |
| C4 | 任意kernel均有HSIC=0 iff independence | 需要 characteristic/universal 等条件 | 不采用 |
| C5 | HSIC数值可跨kernel直接解释相关强度 | scale/bandwidth/kernel与estimator依赖 | 不采用 |

## 课程补严

- Hilbert space不自动是RKHS；evaluation continuity是额外条件；
- “kernel eigenfunctions形成basis”需要 compact/self-adjoint integral operator与measure条件；
- Mercer expansion不是任意kernel/domain上无条件成立；
- population HSIC、finite-sample estimator和optimization loss分开；
- bandwidth、centering、sample dependence与null calibration需审计。

## 已生成与后续调用

- [x] [[Banach 空间、Hilbert 空间与正交投影]]：Hilbert/RKHS/point-evaluation边界；
- [x] [[正定核、RKHS 与表示定理]]：reproducing property、kernel mean、HSIC/MMD正式条件；
- [x] [[有界算子、紧算子与谱理论基础]]：Hilbert–Schmidt/cross-covariance operator 与 empirical HSIC contract。

## 交叉验证

- Gretton et al., *Measuring Statistical Dependence with Hilbert-Schmidt Norms*；
- Sriperumbudur et al., characteristic kernels与probability embeddings；
- MIT 18.102 Hilbert/Riesz；RKHS正式教材与原论文留 GEO-07。
