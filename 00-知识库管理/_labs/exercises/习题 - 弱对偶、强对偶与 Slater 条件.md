---
type: exercise
status: draft
area: [math/optimization, math/duality, ai/certification]
topic: "弱对偶、强对偶与 Slater 条件"
difficulty: [A, B, C, D, E]
prerequisites: ["[[弱对偶、强对偶与 Slater 条件]]"]
related: ["[[优化与凸分析 MOC]]", "[[练习与测验 MOC]]"]
solution: "[[解答 - 弱对偶、强对偶与 Slater 条件]]"
created: 2026-08-19
updated: 2026-08-19
---

# 习题 - 弱对偶、强对偶与 Slater 条件

> [!abstract] 训练目标
> 能从 Lagrangian 构造下界，严格区分 value/attainment/qualification，用 gap 做 certificate，并审计 AI 中的 relaxation 与统计边界。

## A. 识别与复述

### OPT-DUAL-A01

对 $f_i(x)\le0,h_j(x)=0$ convention，定义 primal value、Lagrangian、dual function、dual problem、primal/dual feasibility 与 gap。说明哪些定义允许 extended value。

### OPT-DUAL-A02

分别陈述 weak duality、strong duality、primal attainment、dual attainment、Slater condition 与 KKT existence；画出它们之间成立和不成立的逻辑箭头。

### OPT-DUAL-A03

解释为什么 dual function 即使面对 nonconvex primal 仍 concave；再解释“dual problem 是 convex optimization problem”为什么不等于“它容易精确计算”。

## B. 手算与构造

### OPT-DUAL-B01

推导

$$
\min_x\frac12\|x-c\|^2
\quad\text{s.t. }Ax=b
$$

的 dual。给出 $A$ full row rank 时的 primal/dual optimizer，并讨论 rank deficient 时两侧 uniqueness。

### OPT-DUAL-B02

对

$$
\min_x\frac12\|Ax-b\|^2+\lambda\|x\|_1
$$

推导 dual。给定任意 $x$，构造由 residual 缩放得到的 dual-feasible $u$，写出 computable gap 与 coordinate screening 的严格条件。

### OPT-DUAL-B03

三角形 $K_3$ 的 cut objective 为

$$
C(x)=\frac12\sum_{1\le i<j\le3}(1-x_ix_j),
\qquad x_i^2=1.
$$

把问题写成 $\min -C(x)$，推导其 Lagrange dual并证明 $p^*=-2,d^*=-9/4$，所以 gap 为 $1/4$。

## C. 推导与证明

### OPT-DUAL-C01

逐行证明 dual function concave 与 weak duality。指出每个 inequality 使用了 infimum、multiplier sign 还是 primal feasibility。

### OPT-DUAL-C02

定义 perturbation/achievable upper set，用 separation theorem 给出 Slater 导出 strong duality 的证明骨架。解释 relative interior 与 separating hyperplane objective coefficient 非零的角色。

### OPT-DUAL-C03

从 introducing $z=Ax$ 推导

$$
\min_x f(Ax)+g(x)
$$

的 Fenchel dual；写出一个 relative-interior qualification，并证明 primal/dual optimal pair 的 Fenchel–Young equalities。

## D. 反例与失败边界

### OPT-DUAL-D01

分析 convex problem

$$
\min_x x\quad\text{s.t. }x^2\le0.
$$

证明 primal attained、$p^*=d^*=0$，但 dual supremum 不 attained，也不存在 finite KKT multiplier。

### OPT-DUAL-D02

分别给出：(a) Slater 不成立但 strong duality 成立；(b) strict feasibility 成立但因 objective 不 closed/attained 而 primal optimizer 不存在；(c) nonconvex 但 zero gap。逐一说明它们反驳了什么错误命题。

### OPT-DUAL-D03

构造一个“假的 numerical certificate”：primal point 不可行或 inner dual infimum 只被局部求解，却报告很小/负 gap。说明怎样修复成合法、带误差方向的 certificate。

## E. AI 迁移

### OPT-DUAL-E01

对 finite-support maximum entropy with moment constraints，推导 exponential-family dual。分析 target moment 位于 moment polytope relative interior 与 boundary 时，dual attainment/natural parameter 的区别。

### OPT-DUAL-E02

设计 neural-network robustness verification 的 dual-relaxation报告规范：bound direction、relaxation family、primal adversarial witness、dual feasibility、gap、numerical error 与 sample/population boundary。

### OPT-DUAL-E03

对 federated/resource-constrained learning，把 coupling constraint dualize 成 local subproblems。说明 dual ascent 的 subgradient、primal recovery、inexact local solve 与 statistical constraints 各自如何影响结论。

