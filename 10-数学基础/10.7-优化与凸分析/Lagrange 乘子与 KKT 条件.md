---
type: concept
status: draft
area: [math/optimization, math/constrained-optimization, math/convex-analysis, ai/learning]
aliases: [拉格朗日乘子, KKT条件, 互补松弛, constraint qualification, KKT residual]
prerequisites: ["[[投影、约束与可行方向]]", "[[一阶最优性条件与梯度下降]]", "[[Hessian、二阶微分与曲率]]"]
related: ["[[优化与凸分析 MOC]]", "[[弱对偶、强对偶与 Slater 条件]]", "[[最大熵原理与指数族]]", "[[Newton 法、Gauss-Newton 与拟 Newton 法]]"]
sources: ["Boyd-Vandenberghe-2004-Convex-Optimization", "Nocedal-Wright-2006-Numerical-Optimization", "Bertsekas-1999-Nonlinear-Programming", "MIT-6.253-Convex-Analysis-Optimization", "Stanford-EE364A-Duality", "Stanford-EE364A-Equality-Constrained", "Su-3552-Maximum-Entropy"]
created: 2026-08-19
updated: 2026-08-27
---

# Lagrange 乘子与 KKT 条件

> [!abstract] 本章主问题
> KKT 条件把“没有可行下降方向”改写成一组可计算证书：primal feasible、dual feasible、stationarity、complementary slackness。它在 constraint qualification 下是局部最优的必要条件；在 convex objective、convex inequalities 与 affine equalities下又是全局充分条件。没有 CQ 时最优点可能不存在任何 multiplier；在非凸问题中满足 KKT 也可能是 maximum 或 saddle。因此必须把条件方向、约束符号、active set、二阶曲率和数值 residual 一起报告。

## 学习目标

完成本章后，你应当能够：

1. 固定 inequality sign convention 并正确写 Lagrangian；
2. 从 equality tangent space 推导 multiplier stationarity；
3. 从 active-constraint normal cone 推导 inequality multipliers；
4. 完整写出四组 KKT 条件；
5. 解释 complementary slackness 的方向与 weakly active constraints；
6. 区分 LICQ、MFCQ 与 convex Slater condition 的角色；
7. 构造“局部最优但 KKT 失败”的无 CQ 反例；
8. 证明 KKT 在 convex problem 中的 global sufficiency；
9. 区分 KKT necessity、sufficiency、strong duality 和 multiplier existence；
10. 用 critical cone 写二阶必要/充分条件；
11. 推导 equality-constrained Newton/KKT linear system；
12. 解释 multiplier 的 sensitivity/shadow-price 含义及条件；
13. 从 KKT 推导 hard/soft-margin SVM 的 support-vector 结构；
14. 连接 maximum entropy 的 exponential-form solution；
15. 构造 scale-aware KKT residual 与 AI 约束训练验收协议。

> [!question] 初学者读完必须能回答
> 1. inequality 写成 $g_i(x)\le0$ 时，Lagrangian 与 multiplier sign 应怎样配套？
> 2. equality-constrained optimum 的目标梯度为何必须属于 constraint-normal span？
> 3. primal feasibility、dual feasibility、stationarity 与 complementary slackness 各自检查什么？
> 4. inactive、active 与 weakly active constraint 的 multiplier/constraint product 怎样解释？
> 5. LICQ、MFCQ 与 Slater condition 分别在哪一类结论中使用？
> 6. 为什么 KKT 在一般非凸问题中只是 CQ 下的必要条件，而在 convex problem 中可以成为全局充分条件？
> 7. scale-aware KKT residual、critical-cone curvature、strong duality 与 multiplier sensitivity 为什么必须分别报告？

> [!note] 课程位置
> OPT-11 已把约束最优性写成 $-\nabla f(x^*)\in N_C(x^*)$；本章把抽象 normal cone 展开成 active constraint gradients 的非负组合，并加入 primal feasibility、dual feasibility 与 complementary slackness。KKT 因而不是一条“求导等于零”的公式，而是一份 primal–dual 证书。OPT-13 会再问这份证书怎样产生 dual lower bound 与何时 zero gap。

> [!tip] 建议两遍阅读
> **第一遍**固定 $g_i(x)\le0$ convention，在下方三角形 quadratic 上逐项核对四组 KKT、Slater 与 multiplier scaling。**第二遍**再进入 LICQ/MFCQ、CQ failure、critical-cone 二阶条件、KKT linear system 与 sensitivity。每写一个 multiplier，先标出它对应哪条 constraint 以及该 constraint 的缩放。

## 本章的推导问题链

1. equality feasible directions 为什么迫使 objective gradient 落入 equality-normal span？
2. inequality 中为什么只有 active constraints 能贡献 nonzero normal multiplier？
3. sign convention $g_i\le0$ 怎样决定 Lagrangian 中 $+\lambda_i g_i$ 与 $\lambda_i\ge0$？
4. primal、dual、stationarity、complementarity 四组条件分别排除哪类错误？
5. CQ 在“local optimum 推 KKT”中做什么，convexity 又在“KKT 推 global optimum”中做什么？
6. constraint 缩放为何改变 multiplier 数值，却不应改变物理 normal force 与 optimizer？

## 贯穿算例收束：四组 KKT 如何同时闭合

考虑

$$
\min_x
f(x)=\frac12x^THx-b^Tx,
\qquad
H=\operatorname{diag}(1,4),
\qquad
b=(1,5/2)^T,
$$

满足三条 inequalities

$$
g_0(x)=x_1+x_2-1\le0,
$$

$$
g_1(x)=-x_1\le0,
\qquad
g_2(x)=-x_2\le0.
$$

OPT-11 已求得

$$
x^*=\begin{pmatrix}1/2\\1/2\end{pmatrix},
\qquad
f(x^*)=-\frac98.
$$

### 符号与对象账本

| 符号 | 对象 | 本例值 | 检查层 |
|---|---|---:|---|
| $x$ | primal variable | $\mathbb R^2$ | feasibility/objective |
| $g_0,g_1,g_2$ | inequality functions | budget、两条 nonnegativity | sign/scaling |
| $\lambda_i$ | dual multipliers | $(1/2,0,0)$ | dual feasibility |
| $\mathcal A(x^*)$ | active set | $\{0\}$ | 哪些法向能进入 stationarity |
| $\mathcal L(x,\lambda)$ | Lagrangian | $f+\sum_i\lambda_i g_i$ | primal–dual coupling |
| $r_{\mathrm{stat}}$ | stationarity residual | $\nabla_x\mathcal L$ | 一阶平衡 |
| $r_{\mathrm{comp}}$ | complementarity residual | $\lambda\odot g(x)$ | active/slack 配对 |

### 第一步：active set 与 gradient

在 $x^*$，

$$
g_0(x^*)=0,
\qquad
g_1(x^*)=g_2(x^*)=-\frac12.
$$

所以只有预算 constraint active。objective gradient 是

$$
\nabla f(x^*)=Hx^*-b
=\begin{pmatrix}-1/2\\-1/2\end{pmatrix}.
$$

active normal 为

$$
\nabla g_0=(1,1)^T.
$$

因此选择

$$
\lambda^*=\begin{pmatrix}1/2\\0\\0\end{pmatrix}
$$

即可用 active outward normal 平衡 objective gradient。

### 第二步：四组 KKT 逐项验算

1. **primal feasibility**

$$
g(x^*)=\begin{pmatrix}0\\-1/2\\-1/2\end{pmatrix}\le0.
$$

2. **dual feasibility**

$$
\lambda^*=\begin{pmatrix}1/2\\0\\0\end{pmatrix}\ge0.
$$

3. **stationarity**

$$
\begin{aligned}
\nabla_x\mathcal L(x^*,\lambda^*)
&=\nabla f(x^*)
+\frac12\nabla g_0(x^*)\\
&=(-1/2,-1/2)^T+(1/2,1/2)^T\\
&=0.
\end{aligned}
$$

4. **complementary slackness**

$$
\lambda^*\odot g(x^*)
=\begin{pmatrix}(1/2)0\\0(-1/2)\\0(-1/2)\end{pmatrix}
=0.
$$

四项缺一不可：只满足 stationarity 可能不可行；只满足 primal feasibility 可能 objective 很差；乘子为负会把 outward normal 方向用反；active constraint 若与 multiplier product 不为零则没有互补。

### 为什么本例的 KKT 足以证明 global optimum

$H\succ0$，所以 $f$ strongly convex；三个 $g_i$ 都 affine，问题 convex。并且

$$
\bar x=(1/4,1/4)^T
$$

满足

$$
g_0(\bar x)=-1/2<0,
\qquad
g_1(\bar x)=g_2(\bar x)=-1/4<0,
$$

因此 Slater condition 成立。KKT 在这里既有 multiplier existence，也足以证明唯一 global optimizer。逻辑要按方向读：一般非凸问题中，即使四组 KKT 都成立，也仍可能是 maximum 或 saddle。

### constraint scaling 会怎样改变 multiplier

若把同一预算约束改写为

$$
\widetilde g_0(x)=2(x_1+x_2-1)\le0,
$$

其 gradient 变成 $2(1,1)^T$。为保持 stationarity，multiplier 变为

$$
\widetilde\lambda_0^*=\frac14.
$$

乘积保持不变：

$$
\widetilde\lambda_0^*\nabla\widetilde g_0
=\lambda_0^*\nabla g_0
=\frac12(1,1)^T.
$$

所以 multiplier 数值不能脱离 constraint units 直接比较；数值 residual 也应做 scale-aware normalization。

### 核心公式七问：KKT 四组条件

对 $g_i(x)\le0$ convention，

$$
g(x^*)\le0,
\quad
\lambda^*\ge0,
\quad
\nabla f(x^*)+J_g(x^*)^T\lambda^*=0,
\quad
\lambda^*\odot g(x^*)=0,
$$

逐项回答：

1. **目的：**把约束一阶最优性拆成可分别计算的 primal–dual residuals；
2. **对象：**$x^*$ 是 primal candidate，$\lambda^*$ 与每条 inequality 一一对应；
3. **来路：**normal-cone condition 加上 active normals 的非负生成表示；
4. **步骤：**先查 feasibility/active set，再解 stationarity multipliers，最后查 sign 与 complementarity；
5. **读法：**objective gradient 被 active constraint normals 平衡，inactive constraints 不施加一阶法向力；
6. **检查：**本例四组 residual 精确为零；缩放 constraint 后 multiplier 反向缩放；
7. **去路：**OPT-13 将 $\inf_x\mathcal L(x,\lambda)$ 变成 dual function，数值 solver 则把四组量作为独立停止证书。

> [!warning] 必要性、充分性和强对偶不可混写
> “local optimum + CQ ⇒ KKT”是必要性方向；“convex problem + KKT ⇒ global optimum”是充分性方向；Slater 在 convex duality中还支持 zero gap/dual attainment 的相应结论。非凸 KKT 点仍需 critical-cone 二阶分析。不要因为本例三者同时成立，就省略任一假设。

> [!success] 第一遍停靠线
> 合上笔记后，能从 $x^*$ 算出 active set、gradient 与 $\lambda^*=(1/2,0,0)$，逐项写完四组 KKT 并验证 $f(x^*)=-9/8$；能给出 Slater point $(1/4,1/4)$，并解释预算约束乘 2 后 multiplier 为何变成 $1/4$。若只会写 stationarity 一行，尚未形成 KKT 证书。

## 零、统一问题与符号

本章固定写法：

$$
\begin{aligned}
\min_x\quad &f(x)\\
\text{s.t.}\quad &g_i(x)\le0,\quad i=1,\ldots,m,\\
&h_j(x)=0,\quad j=1,\ldots,p.
\end{aligned}
$$

Lagrangian 定义为

$$
\mathcal L(x,\lambda,\nu)
=f(x)+\sum_{i=1}^m\lambda_i g_i(x)
+\sum_{j=1}^p\nu_jh_j(x),
$$

其中

$$
\lambda_i\ge0,
\qquad
\nu_j\in\mathbb R.
$$

若把 inequality 写成 $g_i\ge0$，multiplier 的符号和 Lagrangian 符号都必须一起改变。

先用下图回答一个视觉问题：**活跃约束的法向量怎样平衡目标梯度，四组 KKT 条件又在什么假设下分别成为必要或充分证书？**

![[00-知识库管理/_assets/figures/optimization/fig-lagrange-kkt-v2.svg|880]]

> [!figure] 图 10.7.12｜活跃法向平衡、四组 KKT 证书与逻辑方向
> A 在可行域边界将 $\nabla f$ 与带非负 multiplier 的 active normals 画成 stationarity 平衡；B 依次列出 primal feasibility、dual feasibility、stationarity 与 complementary slackness；C 分开“local optimum + CQ 推 KKT”“convex problem + KKT 推 global optimum”以及“nonconvex KKT point 仍需 critical-cone curvature”。来源：独立绘制；生成脚本：[[plot_metric_constrained_optimization_v2.py]]；确定性结构示意，无随机种子。

**怎样读图。** A 先固定 inequality sign convention，再检查 multiplier 的符号和 inactive constraint 的零乘子；B 把四个 residual 分开缩放和报告，任何一项缺失都不是完整 KKT certificate；C 沿箭头方向读取 theorem，CQ 服务于必要性，convexity 服务于充分性，非凸分类还要加入二阶条件。

**适用边界（图没有证明什么）。** 平面法向平衡省略了 equality normals、退化 active set 与 multiplier nonuniqueness。CQ 失败时局部最优点可能没有 multiplier；非凸 KKT 点可能是 maximum、saddle 或 degenerate point。KKT 成立本身不等于 strong duality、primal/dual attainment、second-order sufficiency，也不保证有限精度求解器的 residual 已足够小。

## 一、先看 equality：gradient 为什么是约束法向量组合

考虑

$$
\min f(x)\quad\text{s.t. }h(x)=0,
$$

令 $J_h(x)\in\mathbb R^{p\times d}$ 的第 $j$ 行是 $\nabla h_j(x)^T$。在 regular point，tangent directions 满足

$$
J_h(x^*)d=0.
$$

局部最优要求

$$
\nabla f(x^*)^Td=0,
\qquad \forall d\in\ker J_h(x^*).
$$

线性代数恒等式

$$
(\ker J_h)^\perp=\operatorname{range}(J_h^T)
$$

给出某个 $\nu^*$ 使

$$
\nabla f(x^*)+J_h(x^*)^T\nu^*=0.
$$

这就是

$$
\nabla_x\mathcal L(x^*,\nu^*)=0.
$$

若 equality gradients linearly independent，multiplier 通常唯一；redundant equalities 会让 multiplier 不唯一，但 $x^*$ 仍可唯一。

## 二、再看 inequalities：只有 active constraint 产生一阶法向力

active set：

$$
\mathcal A(x^*)=\{i:g_i(x^*)=0\}.
$$

若 $g_i(x^*)<0$，小扰动通常仍有 slack，该 constraint 不限制 local tangent。对 regular point，feasible tangent/linearized cone 的 polar 由：

- equality normals $\nabla h_j$ 的任意线性组合；
- active inequality outward normals $\nabla g_i$ 的非负组合

生成。由

$$
-\nabla f(x^*)\in N_C(x^*)
$$

得到

$$
\nabla f(x^*)
+\sum_i\lambda_i^*\nabla g_i(x^*)
+\sum_j\nu_j^*\nabla h_j(x^*)=0,
$$

其中 $\lambda_i^*\ge0$，且 inactive constraints 的 $\lambda_i^*=0$。

## 三、KKT 四组条件

一个 primal-dual triple $(x^*,\lambda^*,\nu^*)$ 满足：

### 3.1 primal feasibility

$$
g_i(x^*)\le0,\qquad h_j(x^*)=0.
$$

### 3.2 dual feasibility

$$
\lambda_i^*\ge0.
$$

equality multiplier $\nu$ 无符号限制。

### 3.3 stationarity

$$
\nabla f(x^*)
+\sum_i\lambda_i^*\nabla g_i(x^*)
+\sum_j\nu_j^*\nabla h_j(x^*)=0.
$$

### 3.4 complementary slackness

$$
\lambda_i^*g_i(x^*)=0,
\qquad \forall i.
$$

它表示：

- 若 $g_i(x^*)<0$，必有 $\lambda_i^*=0$；
- 若 $\lambda_i^*>0$，必有 $g_i(x^*)=0$；
- 若 $g_i(x^*)=0$，仍可能 $\lambda_i^*=0$，称 weakly active。

> [!warning] complementary slackness 不是“二者只有一个为零”
> 二者可以同时为零。active set 不等于 positive-multiplier set；这一区别会影响 critical cone 与 active-set identification。

## 四、constraint qualification：KKT 推导里不可删除的桥

KKT necessity 需要把真实 tangent cone 与 linearized constraint cone 对齐。CQ 就是这座桥。

### 4.1 LICQ

在 $x^*$，集合

$$
\{\nabla g_i(x^*):i\in\mathcal A(x^*)\}
\cup
\{\nabla h_j(x^*)\}_{j=1}^p
$$

linearly independent。LICQ 强、易解释，并常给 multiplier uniqueness。

### 4.2 MFCQ

要求 equality gradients independent，并存在方向 $d$ 使

$$
\nabla h_j(x^*)^Td=0,
\qquad
\nabla g_i(x^*)^Td<0
\quad(i\in\mathcal A).
$$

即能在保持 equalities 一阶不变的同时，严格走入所有 active inequalities 内部。MFCQ 比 LICQ 弱，但仍能支持 multiplier existence/boundedness 等局部结果。

### 4.3 Slater condition

对 convex problem，若存在 relative-interior point $\bar x$ 满足

$$
g_i(\bar x)<0,
\qquad h_j(\bar x)=0
$$

（并处理 affine-hull/domain 技术条件），称 strict feasible/Slater。它是 convex duality 的核心 CQ，常保证 strong duality 与 dual attainment/KKT existence；详细结论留给[[弱对偶、强对偶与 Slater 条件]]。

### 4.4 无 CQ 时 KKT 可失败

考虑

$$
\min_x f(x)=x
\quad\text{s.t. }g(x)=x^2\le0.
$$

唯一 feasible point 是 $x^*=0$，所以它当然是 global minimum。但

$$
f'(0)=1,\qquad g'(0)=0.
$$

stationarity 要求

$$
1+\lambda\cdot0=0,
$$

无任何 $\lambda\ge0$ 能满足。这里 active constraint gradient 为零，CQ 失败。

> [!important] 最优点先于 KKT
> “找不到 multiplier”可能是 CQ/数值问题，不等于点不是最优；“找到 KKT 点”在非凸问题中也不等于点是最小。

## 五、KKT 的必要性与充分性要分开说

### 5.1 非线性一般问题

若 $(x^*)$ 是 local minimum，函数足够 smooth 且某个合适 CQ 成立，则存在 multipliers 使 KKT 成立：这是**必要性**。

反向一般不成立。例如 unconstrained $f(x)=-x^2$ 在 $x=0$ 满足 stationarity（即空约束 KKT），却是 local maximum。

### 5.2 convex problem 的充分性

假设：

- $f$ convex differentiable；
- 每个 $g_i$ convex differentiable；
- $h_j$ affine；
- $(x^*,\lambda^*,\nu^*)$ 满足 KKT。

对任意 feasible $x$，由 convexity：

$$
f(x)\ge f(x^*)+\nabla f(x^*)^T(x-x^*).
$$

stationarity 给

$$
\nabla f(x^*)
=-\sum_i\lambda_i^*\nabla g_i(x^*)
-\sum_j\nu_j^*\nabla h_j(x^*).
$$

convex $g_i$ 有

$$
\nabla g_i(x^*)^T(x-x^*)
\le g_i(x)-g_i(x^*).
$$

affine equality 在两个 feasible points 间差为零，于是

$$
f(x)-f(x^*)
\ge-\sum_i\lambda_i^*[g_i(x)-g_i(x^*)].
$$

因 $g_i(x)\le0$、$\lambda_i^*\ge0$ 且 $\lambda_i^*g_i(x^*)=0$，右侧非负，故 $f(x)\ge f(x^*)$。所以 KKT point 是 global optimum。

注意：这项**充分性**本身不需要 Slater；Slater 常用于保证最优解处存在 multiplier/KKT 和 strong duality。

## 六、二阶条件：KKT 点到底像 minimum 还是 saddle

定义 Lagrangian Hessian：

$$
\nabla_{xx}^2\mathcal L(x^*,\lambda^*,\nu^*)
=\nabla^2f(x^*)
+\sum_i\lambda_i^*\nabla^2g_i(x^*)
+\sum_j\nu_j^*\nabla^2h_j(x^*).
$$

critical cone 可写成 tangent directions 中一阶 objective 不变的部分：

$$
\mathcal C(x^*,\lambda^*)=
\left\{d:
\begin{array}{l}
\nabla h_j^Td=0,\\
\nabla g_i^Td=0\quad\text{若 }\lambda_i^*>0,\\
\nabla g_i^Td\le0\quad\text{若 }g_i=0,\lambda_i^*=0
\end{array}
\right\}.
$$

在适当 CQ/regularity 下：

- second-order necessary condition：

$$
d^T\nabla_{xx}^2\mathcal L\,d\ge0,
\qquad \forall d\in\mathcal C;
$$

- second-order sufficient condition（代表性形式）：对所有 nonzero critical $d$，

$$
d^T\nabla_{xx}^2\mathcal L\,d>0,
$$

则 $x^*$ 是 strict local minimum（完整定理还需相应 CQ/regularity）。

只检查 full-space Hessian $\nabla^2f\succeq0$ 既可能太强，也可能漏掉 constraint curvature；应该检查 Lagrangian Hessian 在 critical directions 上的曲率。

## 七、KKT linear system：约束 Newton 的计算骨架

先看 quadratic/equality-constrained step：

$$
\min_p\quad g^Tp+\frac12p^THp
\quad\text{s.t. }Ap=-c.
$$

Lagrangian stationarity 与 constraint 给

$$
\begin{bmatrix}
H&A^T\\
A&0
\end{bmatrix}
\begin{bmatrix}
p\\\nu
\end{bmatrix}
=-
\begin{bmatrix}
g\\c
\end{bmatrix}.
$$

这是 saddle-point/KKT system，通常 symmetric indefinite；不能直接套只适用于 SPD 的 CG。可选：

- symmetric-indefinite factorization；
- Schur complement；
- null-space/reduced Hessian；
- MINRES 类 Krylov 加 block preconditioner；
- regularized/augmented system。

### 7.1 Schur complement（$H\succ0$）

由

$$
p=-H^{-1}(g+A^T\nu)
$$

代入 $Ap=-c$：

$$
AH^{-1}A^T\nu=c-AH^{-1}g.
$$

不要显式形成 $H^{-1}$；每次通过 solve 应用。$A$ rank deficiency 会导致 multiplier nonuniqueness 和 Schur system singular。

### 7.2 infeasible-start Newton

对 equality constraints，可同时线性化 stationarity 与 feasibility residual，求 KKT step。停止不能只看 objective；要联合看

$$
r_{\mathrm{dual}}=\nabla f(x)+A^T\nu,
\qquad
r_{\mathrm{pri}}=Ax-b.
$$

这连接[[Newton 法、Gauss-Newton 与拟 Newton 法]]和后续 primal-dual/interior-point 方法。

## 八、multiplier 的 sensitivity 含义

把 inequality 写成资源上界

$$
g_i(x)\le u_i
$$

等价于 $g_i(x)-u_i\le0$。Lagrangian 项为 $\lambda_i(g_i-u_i)$。在 value function 可微、regularity 与 stable active set 等条件下，

$$
\frac{\partial p^*(u)}{\partial u_i}\approx-\lambda_i^*.
$$

放宽上界会让最小值不增，$\lambda_i$ 是 marginal shadow price。若 multiplier 不唯一、value function 不可微、active set 跳变或 problem nonconvex，这只能解释为 subgradient/local sensitivity，不是无条件因果效应。

### 8.1 约束缩放会缩放 multiplier

把 $g_i\le0$ 改写成 $a g_i\le0$（$a>0$），同一 stationarity 中 multiplier 变为 $\lambda_i/a$。因此 raw multiplier magnitude 不能跨不同单位/缩放直接比较；应报告 normalized constraint 与 sensitivity convention。

## 九、例一：带非负约束的最小二乘

$$
\min_x\frac12\|Ax-b\|^2
\quad\text{s.t. }x\ge0.
$$

按 $-x_i\le0$ 写，Lagrangian：

$$
\mathcal L=\frac12\|Ax-b\|^2-\lambda^Tx.
$$

KKT：

$$
x\ge0,\quad\lambda\ge0,
$$

$$
A^T(Ax-b)-\lambda=0,
$$

$$
\lambda_i x_i=0.
$$

所以若 $x_i>0$，对应 gradient coordinate 必为零；若 $x_i=0$，gradient coordinate $\lambda_i\ge0$，表示向负方向下降却不可行。这与 normal-cone 条件完全一致。

## 十、例二：soft-margin SVM 的 support vectors

primal：

$$
\min_{w,b,\xi}
\frac12\|w\|^2+C\sum_{i=1}^n\xi_i
$$

$$
\text{s.t. }
1-\xi_i-y_i(w^Tx_i+b)\le0,
\qquad
-\xi_i\le0.
$$

令 multipliers 分别为 $\alpha_i\ge0,\mu_i\ge0$。stationarity：

$$
w=\sum_i\alpha_i y_ix_i,
$$

$$
\sum_i\alpha_i y_i=0,
$$

$$
C-\alpha_i-\mu_i=0
\quad\Rightarrow\quad0\le\alpha_i\le C.
$$

complementarity：

$$
\alpha_i[1-\xi_i-y_i(w^Tx_i+b)]=0,
$$

$$
\mu_i\xi_i=0.
$$

因此 $\alpha_i>0$ 的样本必须在 margin constraint 上 active，是 support vectors；但 active sample 仍可能 $\alpha_i=0$（退化情形）。

## 十一、例三：maximum entropy 与 exponential family

在有限支持上最大化 entropy，等价于最小化

$$
f(p)=\sum_xp(x)\log p(x),
$$

满足 normalization 与 moments：

$$
\sum_xp(x)=1,\qquad
\sum_xp(x)T(x)=\tau,\qquad p(x)\ge0.
$$

若解在 positive interior，nonnegativity multipliers 为零。对 $p(x)$ 的 stationarity 给

$$
1+\log p(x)+\nu+\eta^TT(x)=0,
$$

于是

$$
p(x)\propto\exp\{-\eta^TT(x)\}.
$$

重新命名参数即可得 exponential family。若 optimum 在 boundary，不能忽略 $p(x)\ge0$ 的 multipliers/extended-value 处理；若 moments 在 marginal-polytope boundary，finite natural parameter 可能不存在。详见[[最大熵原理与指数族]]。

## 十二、KKT residual：数值上怎样说“近似满足”

定义代表性 residual：

### 12.1 primal

$$
r_{\mathrm{pri}}
=\begin{bmatrix}
[g(x)]_+\\h(x)
\end{bmatrix},
$$

其中 $[a]_+=\max(a,0)$ 逐坐标。

### 12.2 dual feasibility

$$
r_{\mathrm{df}}=[-\lambda]_+.
$$

### 12.3 stationarity

$$
r_{\mathrm{stat}}
=\nabla_x\mathcal L(x,\lambda,\nu).
$$

### 12.4 complementarity

$$
r_{\mathrm{comp}}=\lambda\odot g(x).
$$

报告时至少给 norm 与 scale：

$$
\frac{\|r_{\mathrm{stat}}\|}
{1+\|\nabla f\|+\|J_g^T\lambda\|+\|J_h^T\nu\|},
$$

以及 constraint-specific relative/absolute tolerances。单一 max residual 会隐藏不同单位，单一 objective change 更不能替代 KKT residual。

> [!warning] 小 KKT residual 不等于问题解决完毕
> 还需检查：CQ/conditioning、二阶类型、duality gap（若适用）、global/nonconvex 状态、linear-solve backward error 与部署指标。

## 十三、penalty、augmented Lagrangian 与 KKT 的关系

- quadratic penalty $f+\frac\rho2\|h\|^2$：有限 $\rho$ 通常不 exact feasible，且大 $\rho$ 病态；
- exact $\ell_1$ penalty：在 multiplier/regularity 条件下足够大 penalty 可 exact，但不可微；
- augmented Lagrangian：同时更新 multiplier 与 penalty，改善纯 penalty 病态；
- barrier：从 strict interior 接近 boundary，产生 perturbed complementarity；
- primal-dual/interior-point：直接跟踪 KKT residual/central path。

这些方法的目标是求 KKT point，不表示任意 penalty stationary point 自动满足原问题 KKT。

## 十四、AI 约束问题的审计

### 14.1 fairness/privacy/resource constraints

把 empirical disparity、privacy proxy、latency/FLOPs 写成 $g_i(\theta)\le0$ 后，应先问：

- constraint estimator 是否有 sampling error/bias；
- feasible set 是否 nonempty；
- gradient 是否可得且尺度合理；
- multiplier 更新是否稳定；
- train constraint 与 population/deployment constraint 是否错位。

empirical KKT 不证明 population fairness/privacy。

### 14.2 constrained generation/RL

policy/decoder 参数化使 problem 通常 nonconvex，KKT 只给 local stationarity。constraint expectation 的 Monte Carlo noise 同时污染 primal residual 和 multiplier gradient；应给 confidence interval/held-out constraint evaluation。

### 14.3 bilevel/implicit systems

inner KKT system 常被微分以得到 hypergradient。若 inner solve residual 大、active set 不稳定、KKT Jacobian singular 或 strict complementarity 失败，implicit derivative 可能不可靠；必须把 solve residual 传到 outer error budget。

### 14.4 SVM/max entropy 的教学边界

这两例是 convex/structured，KKT 有全局意义；把同样推导复制到深网参数后只保留 local necessary interpretation，不能沿用 global optimum 结论。

## 十五、常见误区

1. **任何 local optimum 都满足 KKT**：还需 CQ；
2. **满足 KKT 就是 global optimum**：只在相应 convex 条件下；
3. **active constraint 的 multiplier 必正**：可为零；
4. **equality multiplier 必非负**：它自由取符号；
5. **Slater 是 KKT sufficient 的必要条件**：KKT 点的 convex sufficiency 本身不靠 Slater；Slater帮助存在性/strong duality；
6. **Hessian 只看 $\nabla^2f$**：约束二阶条件看 Lagrangian Hessian；
7. **全空间 PSD 才是 constrained minimum**：只需 critical directions 的曲率；
8. **大 multiplier 必是重要 constraint**：缩放/单位会改变 magnitude；
9. **小 feasibility residual 等于 KKT**：还缺 stationarity/dual/complementarity；
10. **empirical constraints 满足即部署约束满足**：还有 statistical/generalization gap。

## 十六、掌握标准

### Level 1：识别

- 固定符号并写四组 KKT；
- 区分 active、positive multiplier 与 weakly active。

### Level 2：手算

- 求 equality/inequality multipliers；
- 算 primal/dual/stationarity/complementarity residual；
- 推导简单 SVM/max-entropy stationarity。

### Level 3：证明

- 从 tangent/normal 推 KKT；
- 构造 CQ failure；
- 证明 convex KKT sufficiency；
- 在 critical cone 上检查 second-order condition。

### Level 4：迁移

- 选择 CQ 并说明理由；
- 解/预条件 KKT system；
- 为 noisy AI constraints 写 scale-aware primal-dual 验收。

## 十七、自检问题

1. $g\le0$ convention 下为什么 $\lambda\ge0$？
2. equality multiplier 为什么自由符号？
3. active constraint 为什么可能 multiplier 为零？
4. LICQ、MFCQ、Slater 各解决哪类桥接问题？
5. $x^2\le0$ 反例为何无 KKT multiplier？
6. convex KKT sufficient 的逐步证明用了哪些条件？
7. critical cone 为什么区别 $\lambda_i>0$ 与 $=0$？
8. KKT matrix 为什么通常 indefinite？
9. shadow price 为什么依赖 constraint scaling？
10. SVM 的 $0<\alpha_i<C$ 表示什么几何状态？

## 十八、来源与证据边界

1. Boyd & Vandenberghe, [Stanford EE364A: Duality](https://web.stanford.edu/class/ee364a/lectures/duality.pdf)：Lagrangian、KKT、Slater 与 sensitivity；
2. Boyd & Vandenberghe, [Equality Constrained Minimization](https://web.stanford.edu/class/ee364a/lectures/equality.pdf)：KKT linear system、feasible/infeasible-start Newton；
3. MIT OCW, [6.253 Convex Analysis and Optimization](https://ocw.mit.edu/courses/6-253-convex-analysis-and-optimization-spring-2012/resources/lecture-notes/)：normal cone、constraint qualification 与 convex duality；
4. Nocedal & Wright, *Numerical Optimization*, 2nd ed., 2006：LICQ/MFCQ、二阶条件、SQP 与 numerical KKT systems；
5. Bertsekas, *Nonlinear Programming*, 2nd ed., 1999：multipliers、tangent cones 与 sensitivity；
6. [[S-2015-Su-3552-最大熵原理]]：Lagrange multiplier 推 maximum-entropy exponential form 的中文入口。

> [!info] 证据分工
> 正式课程与教材承担 KKT 的方向、CQ、二阶条件和数值求解；科学空间文章提供 maximum-entropy 的 AI/概率建模入口，reference measure、boundary、CQ 与 duality 条件由课程补齐。

## 十九、配套训练

- 习题：[[习题 - Lagrange 乘子与 KKT 条件]]
- 详解：[[解答 - Lagrange 乘子与 KKT 条件]]
- 前驱：[[投影、约束与可行方向]]、[[Newton 法、Gauss-Newton 与拟 Newton 法]]
- 后继：[[弱对偶、强对偶与 Slater 条件]]
