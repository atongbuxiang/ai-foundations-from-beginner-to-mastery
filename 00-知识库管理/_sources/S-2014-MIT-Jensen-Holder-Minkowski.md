---
type: source
status: draft
area: [sources, math/inequalities, math/analysis, math/probability]
source_type: course
title: "MIT 18.125 Lecture 14 and MIT 18.175 Lecture 5: Jensen, Hölder, Cauchy and Minkowski"
author: "Jeff Viaclovsky; Scott Sheffield; MIT OpenCourseWare"
year: 2014
url: "https://ocw.mit.edu/courses/18-125-measure-and-integration-fall-2003/resources/18125_lec14/"
accessed: 2026-08-19
source_tier: A
license: "MIT OpenCourseWare; individual resources以课程页面声明为准"
site_category: [mathematical-analysis, probability, inequalities]
series: "MIT 18.125 Measure and Integration / MIT 18.175 Theory of Probability"
scope_role: core
temporal_role: foundational
related: ["[[基本不等式与界的构造]]", "[[期望、方差与矩]]", "[[凸函数、Jensen 不等式与上图集]]", "[[内积空间]]"]
created: 2026-08-19
updated: 2026-08-19
---

# MIT：Jensen、Hölder、Cauchy与Minkowski

> [!abstract] 来源定位
> MIT 18.125 Lecture 14把convex functions、Jensen、Hölder与Minkowski放在同一分析课程单元；MIT 18.175 Lecture 5把Jensen、Hölder与Cauchy–Schwarz放进expectation/integration主线，并明确以normalized Young inequality证明Hölder。本卡承担MATH-06的正式定理骨架；初学者有限维证明、等号、slack ledger、AI形状与浮点实验由本课程补写。

## 元数据

- MIT 18.125资源页：[Lecture 14: Convex Functions; Jensen; Hölder; Minkowski](https://ocw.mit.edu/courses/18-125-measure-and-integration-fall-2003/resources/18125_lec14/)；
- MIT 18.175讲义：[Lecture 5: More Integration and Expectation](https://ocw.mit.edu/courses/18-175-theory-of-probability-spring-2014/1c016821763783c34c48816b1ac66969_MIT18_175S14_Lecture5.pdf)；
- 18.125层级：研究生Measure and Integration；
- 18.175层级：Theory of Probability；
- 本库使用：稳定定理、证明路线和概率接口，不复制讲义全文。

## 核心断言

| ID | 断言 | 条件 | 证据位置 | 当前用途 |
|---|---|---|---|---|
| C1 | Convex $\phi$满足$\phi(\int f\,d\mu)\le\int\phi(f)\,d\mu$ | probability measure、integrability | 18.175 Lecture 5 p.9 | Jensen期望接口 |
| C2 | Hölder以conjugate $p,q$控制$\int|fg|$ | $1/p+1/q=1$、相应$L^p/L^q$有限 | 18.175 p.9；18.125 L14 | Hölder正式主线 |
| C3 | Scalar Young是normalized Hölder proof的核心 | nonnegative inputs、conjugate exponents | 18.175 p.9 | MATH-06逐步证明 |
| C4 | Cauchy–Schwarz是$p=q=2$特例 | finite $L^2$ norms | 18.175 p.9 | 内积/期望接口 |
| C5 | Minkowski给$L^p$ triangle | $p\ge1$及可积性 | 18.125 L14 | 有限维$p$-norm证明 |

## 课程采用的证明路线

### Jensen

讲义强调以经过$\mathbb Ef$的affine supporting line从下方支撑convex函数：

$$
\phi(x)\ge L(x),
\qquad
\phi(\mathbb Ef)=L(\mathbb Ef).
$$

积分后affine函数可穿过expectation，从而得到Jensen。

### Hölder

先归一化

$$
\|f\|_p=\|g\|_q=1,
$$

再逐点用

$$
|fg|
\le
\frac{|f|^p}{p}
+\frac{|g|^q}{q}.
$$

积分后右端等于1，最后缩放回原范数。

### Cauchy

$p=q=2$时Hölder退化为Cauchy–Schwarz。MATH-06另给非负二次式证明，以便从同一证明直接读出线性相关等号条件。

## 本课程补严

- 先在$\mathbb R^n$上建立有限和版本，再开放测度/概率接口；
- 对零范数、端点$p=1,q=\infty$和$p<1$失败分别处理；
- 区分“期望存在”“有限”“扩展实数定义”；
- 每条界记录equality与slack；
- 加入范数换算的dimension factor；
- 加入Attention、LSE、线性层与稳定浮点实现；
- 有限实验只做diagnostic，不替代讲义中的一般证明。

## 限制与边界

- 18.125是研究生测度论语境，不适合作为零基础读者第一遍唯一材料；
- 18.175单页提纲给证明idea，不展开所有有限维中间步骤；
- 课程讲义不直接证明深网鲁棒性、ELBO tightness或Attention训练后统计；
- Infinite-dimensional $L^p$完备性和a.e. equivalence属于后续分析课程，不在MATH-06展开。

## 已生成与后续调用

- [x] [[基本不等式与界的构造]]；
- [x] [[习题 - 基本不等式与界的构造]]；
- [x] [[解答 - 基本不等式与界的构造]]；
- [x] [[实验 - 不等式松弛、等号与数值稳定性审计]]；
- [x] [[期望、方差与矩]]下游接口；
- [x] [[凸函数、Jensen 不等式与上图集]]下游接口。

## 交叉验证

- Boyd & Vandenberghe, Convex Optimization, Chapter 3；
- [[S-2011-Su-1420-经典不等式更正]]；
- [[S-2022-Su-9070-logsumexp不等式]]；
- [[内积空间]]中的抽象Cauchy–Schwarz证明。
