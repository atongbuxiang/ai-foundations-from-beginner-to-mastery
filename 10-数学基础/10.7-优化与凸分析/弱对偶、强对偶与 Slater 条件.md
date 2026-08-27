---
type: concept
status: draft
area: [math/optimization, math/convex-analysis, math/duality, ai/certification]
aliases: [Lagrange 对偶, 弱对偶, 强对偶, Slater 条件, 对偶间隙, primal-dual certificate]
prerequisites: ["[[Lagrange 乘子与 KKT 条件]]", "[[次梯度、共轭函数与 Fenchel 对偶]]", "[[凸集、凸组合与分离超平面]]"]
related: ["[[优化与凸分析 MOC]]", "[[近端算子、复合优化与稀疏正则]]", "[[最大熵原理与指数族]]", "[[率失真、信息瓶颈与最小描述长度]]"]
sources: ["Boyd-Vandenberghe-2004-Convex-Optimization", "Stanford-EE364A-Duality", "MIT-6.253-Duality", "Rockafellar-1970-Convex-Analysis", "Bertsekas-2009-Convex-Optimization-Theory", "Wainwright-Jordan-2008-Exponential-Families", "Su-3552-Maximum-Entropy"]
created: 2026-08-19
updated: 2026-08-27
---

# 弱对偶、强对偶与 Slater 条件

> [!abstract] 本章主问题
> Lagrange duality 把每个 dual-feasible multiplier 变成 primal optimal value 的可验证下界；因此任意 primal-feasible 点与 dual-feasible 点之间的 gap 都是可计算的 suboptimality certificate。弱对偶几乎不需要 convexity，总有 $d^*\le p^*$；强对偶 $d^*=p^*$ 则需要结构。对 convex inequalities、affine equalities 和适当 relative-interior strict feasibility，Slater condition 是最常用的充分条件，并通常带来 dual attainment 与 KKT multipliers。严格可行不是必要条件，写出 formal dual 也不等于 gap 为零或 supremum 被取得。

## 学习目标

完成本章后，你应当能够：

1. 从 Lagrangian 定义 dual function，并解释为什么它总是 concave；
2. 逐行证明 weak duality；
3. 区分 primal/dual feasible、optimal value、attainment 与 unboundedness；
4. 用 primal–dual gap 证明一个可行点的 objective suboptimality 上界；
5. 正确陈述 convex Slater condition，包括 relative interior 与 affine constraints 的细化；
6. 区分 strong duality、dual attainment、KKT existence 与 KKT sufficiency；
7. 解释 separation/perturbation value function 怎样产生 multiplier；
8. 从 Lagrangian 推导 least-norm、linear program、Lasso 与 SVM 的 dual；
9. 从 conjugate 推导 composite Fenchel dual；
10. 用 saddle-point/minimax 语言重述 zero duality gap；
11. 构造 positive duality gap、nonattainment 与 Slater 非必要的例子；
12. 解释 nonconvex dual 下界为什么仍可能有用；
13. 使用 Farkas-type certificate 证明 linear infeasibility；
14. 审计 numerical primal/dual residual、gap 和 constraint scaling；
15. 把 dual certificates 用于 sparse learning、robust bounds、maximum entropy 和 AI relaxation。

> [!question] 初学者读完必须能回答
> 1. dual function 为什么是对 primal variable 取 infimum，而不是只在 feasible set 上取？
> 2. 为什么 dual function 总是 concave，且每个 dual-feasible 点都给 primal optimum 下界？
> 3. weak duality 怎样逐行推出 $d^*\le p^*$，它为什么不要求 primal convex？
> 4. primal–dual gap 怎样成为 feasible primal point 的可计算 suboptimality certificate？
> 5. strong duality、primal attainment、dual attainment 与 multiplier existence 有何区别？
> 6. convex Slater condition 为什么要写 relative interior，affine equality 又怎样处理？
> 7. positive gap、zero gap without attainment、infeasibility certificate 与 numerical residual 为什么必须分别报告？

## 阅读前检查：本章不重复什么

- [[Lagrange 乘子与 KKT 条件]]已完成 normal-cone 推导、四组 KKT、CQ 和二阶条件；
- [[次梯度、共轭函数与 Fenchel 对偶]]已定义 conjugate/Fenchel–Young，并给 formal Fenchel template；
- 本章新增的是：**dual 为什么给 bound、何时 tight、是否 attained、怎样形成可计算 certificate**。

> [!note] 课程位置
> OPT-12 已经在一个候选点上验证 KKT；本章把同一组 multiplier 解释成一条对所有 primal 点都成立的 lower bound。学习顺序必须是“固定 multiplier → 对全部 primal domain 取 infimum → 得到 dual function → 最大化 lower bound”，而不是先背 dual 形式再猜符号。OPT-14 会把不可微结构交给 prox，OPT-15 再改变 movement geometry。

> [!tip] 建议两遍阅读
> **第一遍**只推导下方二维 quadratic 的 dual function，核对 $\lambda^*=(1/2,0,0)^T$ 为什么把 lower bound 推到 $-9/8$。**第二遍**再学习 relative-interior Slater、perturbation value、Fenchel/Lasso dual、positive gap 与 nonattainment。每次使用 dual certificate，都要先核对 primal feasibility、dual feasibility 和求内层 infimum 的误差。

## 本章的推导问题链

1. 为什么固定一个 $\lambda\ge0$ 后，$L(x,\lambda)$ 在每个 feasible $x$ 上都不超过原 objective？
2. 为什么还要对整个 primal domain 取 infimum，而不能只在当前 iterate 上评价 Lagrangian？
3. dual function 为什么必为 concave，哪怕 primal problem 非凸？
4. weak duality 只用了什么；strong duality 又额外需要什么？
5. zero gap、primal attainment、dual attainment 与 multiplier existence 为什么是四个命题？
6. 数值上怎样把 objective gap、constraint residual、dual residual 与 inner-solve error 分开报告？

## 贯穿算例：KKT multiplier 怎样变成全局下界

继续使用第三波的 constrained quadratic：

$$
\begin{aligned}
\min_x\quad
&f(x)=\frac12x^THx-b^Tx,\\
\text{s.t.}\quad
&g_0(x)=x_1+x_2-1\le0,\\
&g_1(x)=-x_1\le0,\qquad g_2(x)=-x_2\le0,
\end{aligned}
$$

其中

$$
H=\operatorname{diag}(1,4),
\qquad
b=(1,5/2)^T.
$$

已知 primal optimum 与 KKT multiplier 为

$$
x^*=(1/2,1/2)^T,
\qquad
\lambda^*=(1/2,0,0)^T,
\qquad
p^*=f(x^*)=-9/8.
$$

### 符号与对象账本

| 对象 | 类型 | 本例中的值或作用 | 不能与什么混淆 |
|---|---|---|---|
| $x$ | primal variable | 在 $\mathbb R^2$ 中被内层最小化 | 当前 solver iterate |
| $\lambda\ge0$ | dual variable | 给三个 inequalities 定价 | primal penalty 超参数 |
| $L(x,\lambda)$ | 二元函数 | objective 加带符号 constraint residual | dual function |
| $g_D(\lambda)$ | dual function | $\inf_xL(x,\lambda)$ | 只评价某个 $x$ 的 Lagrangian |
| $p^*,d^*$ | 两侧最优值 | 本例均为 $-9/8$ | 两侧 optimizer 本身 |
| primal–dual gap | certificate | feasible upper bound 减 dual lower bound | 单独的 KKT residual |

### 第一步：把三条 constraints 放进 Lagrangian

$$
L(x,\lambda)
=\frac12x^THx-b^Tx
+\lambda_0(x_1+x_2-1)
-\lambda_1x_1-\lambda_2x_2.
$$

定义

$$
c(\lambda)
=b-\lambda_0(1,1)^T+\lambda_1e_1+\lambda_2e_2.
$$

于是

$$
L(x,\lambda)=\frac12x^THx-c(\lambda)^Tx-\lambda_0.
$$

由于 $H\succ0$，固定 $\lambda$ 后的内层问题有唯一解

$$
x(\lambda)=H^{-1}c(\lambda).
$$

代回得到 dual function：

$$
\boxed{
g_D(\lambda)
=-\frac12c(\lambda)^TH^{-1}c(\lambda)-\lambda_0,
\qquad
\lambda\ge0.
}
$$

这里的负二次型说明 $g_D$ 是 concave；更一般地，dual function 的 concavity 来自 affine functions 的逐点下确界。

### 第二步：代入 multiplier，闭合零 gap

在

$$
\lambda^*=(1/2,0,0)^T
$$

处，

$$
c(\lambda^*)=(1/2,2)^T,
\qquad
H^{-1}c(\lambda^*)=(1/2,1/2)^T=x^*.
$$

因此

$$
\begin{aligned}
g_D(\lambda^*)
&=-\frac12\left[
\left(\frac12\right)^2+\frac{2^2}{4}
\right]-\frac12\\
&=-\frac58-\frac12\\
&=-\frac98
=p^*.
\end{aligned}
$$

这不是先假设 strong duality 再得到的等式：$x^*$ primal feasible、$\lambda^*$ dual feasible，而两侧数值相同；weak duality 的夹逼已经足以证明两者分别最优。

作为对照，若取合法但较差的 $\lambda=0$，

$$
g_D(0)=-\frac{41}{32},
$$

于是 $x^*$ 与该 lower bound 组成的 gap 为

$$
-\frac98-\left(-\frac{41}{32}\right)=\frac5{32}.
$$

它仍是正确 certificate，只是没有最优 multiplier 给出的零 gap 紧。

### 第三步：Slater 在本例中检查什么

取

$$
\bar x=(1/4,1/4)^T.
$$

三条 inequality 的值为

$$
\left(-\frac12,-\frac14,-\frac14\right),
$$

全部严格小于零。objective 与 constraints 均 convex，domain 为全空间，故 Slater 成立；本例因此满足 strong duality，并存在最优 multiplier。注意 Slater 是便于验证的充分条件，而上面的零 gap 数值证书本身已经直接证明这一个实例。

### 核心公式七问：dual function

对

$$
g_D(\lambda)=\inf_xL(x,\lambda),
\qquad \lambda\ge0,
$$

逐项回答：

1. **目的：**把每个 dual-feasible multiplier 变成 primal optimum 的可验证 lower bound；
2. **对象：**$\lambda$ 是 dual variable，取 infimum 的 $x$ 仍是 primal variable；
3. **来路：**feasible $x$ 上有 $L(x,\lambda)\le f(x)$，再对全部 $x$ 取 infimum；
4. **步骤：**先固定 $\lambda$，精确或带证书地解内层问题，再最大化所得 concave function；
5. **读法：**dual optimization 在所有合法 lower bounds 中寻找最紧的一条；
6. **检查：**必须验证 multiplier sign、内层 infimum、primal feasibility 与 gap 单位；仅写 formal dual 不够；
7. **去路：**OPT-14 的 Lasso/composite dual、maximum entropy、约束训练和 verification 都依赖这种 lower-bound 语言。

> [!warning] 数值证书边界
> 若内层 infimum 只近似求解，把 $L(\tilde x,\lambda)$ 当成 $g_D(\lambda)$ 通常不合法，因为前者是 dual function 的上界而非所需下界。若 primal point 不可行，objective 与 dual value 的差也不能直接当作 suboptimality certificate。应同时报告可行性残差、dual feasibility、inner-solve lower bound 与 absolute/relative gap。

> [!success] 第一遍停靠线
> 合上笔记后，能从三条 inequalities 重建 $L(x,\lambda)$ 和 $c(\lambda)$；无提示推出 $g_D(\lambda)$；分别算出 $g_D(0)=-41/32$、$g_D(\lambda^*)=-9/8$ 与 gap $5/32,0$；并能解释为什么“值相等”“两侧取得最优解”“Slater 成立”是相关但不同的判断。

## 零、统一 primal problem 与扩展值约定

考虑

$$
\begin{aligned}
p^*=\inf_x\quad &f_0(x)\\
\text{s.t.}\quad &f_i(x)\le0,\quad i=1,\ldots,m,\\
&h_j(x)=0,\quad j=1,\ldots,p,
\end{aligned}
$$

共同 domain 记为 $\mathcal D$。采用：

- primal infeasible：$p^*=+\infty$；
- primal unbounded below：$p^*=-\infty$；
- “optimal solution exists” 比 $p^*$ finite 更强：infimum 可能不 attained。

Lagrangian：

$$
L(x,\lambda,\nu)
=f_0(x)+\sum_{i=1}^m\lambda_if_i(x)
+\sum_{j=1}^p\nu_jh_j(x),
$$

其中 dual feasibility 要 $\lambda\ge0$，$\nu$ free。

先用下图回答一个视觉问题：**dual multiplier 怎样生成全局下界，零 gap 与解被取得为何不同，怎样把两侧可行点组合成可计算证书？**

![[00-知识库管理/_assets/figures/optimization/fig-duality-slater-certificate-v2.svg|880]]

> [!figure] 图 10.7.13｜Dual 下界、value/attainment 分层与 primal–dual gap
> A 将 $g(\lambda,\nu)=\inf_xL(x,\lambda,\nu)$ 画成 primal objective 的一族全局下界；B 分开 weak-only 的 $d^*<p^*$、strong duality 且 dual optimum attained、以及 $\sup g=p^*$ 但 maximizing multiplier 不存在；C 要求 primal/dual 两侧先可行，再用 $f_0(x)-g(\lambda,\nu)$ 控制 suboptimality，并标出 convex relative-interior Slater 的作用。来源：独立绘制；生成脚本：[[plot_advanced_optimization_v2.py]]；确定性结构示意，无随机种子。

**怎样读图。** A 对固定 multiplier 先在整个 domain 上取 infimum，由 weak duality 得到下界；B 把“两个数相等”与“supremum 是否有 maximizer”分开，空心点只表示未取得；C 先核对 constraint residual 和 multiplier sign，再计算 gap。只有在相应 convex/Slater 条件下，才把 tight lower bound 与 KKT multiplier 连接起来。

**适用边界（图没有证明什么）。** 一维下界图不展示 extended-value、unbounded 或 infeasible 情形；Slater 是常用充分条件而非强对偶必要条件。Zero gap 不自动给 primal/dual attainment；formal dual 也可能数值上难解。有限精度下若 primal/dual 不可行，原始 gap 不能直接当作严格 certificate，必须连同缩放后的 residual 和误差界报告。

## 一、dual function：先对 primal variable 取 infimum

定义

$$
g(\lambda,\nu)
=\inf_{x\in\mathcal D}L(x,\lambda,\nu).
$$

它可能取 $-\infty$。注意顺序：给定 multipliers 后，对全部 domain $\mathcal D$ 取 infimum，而不是只对 primal-feasible $x$ 取。

### 1.1 为什么 $g$ 总是 concave

对固定 $x$，$L(x,\lambda,\nu)$ 关于 $(\lambda,\nu)$ 是 affine。任意一族 affine functions 的 pointwise infimum 是 concave。直接证明：令 $z=(\lambda,\nu)$，$t\in[0,1]$：

$$
g(tz_1+(1-t)z_2)
=\inf_x[tL(x,z_1)+(1-t)L(x,z_2)]
$$

$$
\ge t\inf_xL(x,z_1)+(1-t)\inf_xL(x,z_2)
=tg(z_1)+(1-t)g(z_2).
$$

这个结论不要求 primal convex。dual problem 因而总是 concave maximization over a convex set $\lambda\ge0$，即按标准语言属于 convex optimization problem。

## 二、weak duality：为什么每个 dual-feasible 点都给下界

若 $\tilde x$ primal feasible 且 $\lambda\ge0$，则

$$
f_i(\tilde x)\le0,
\qquad h_j(\tilde x)=0,
$$

所以

$$
L(\tilde x,\lambda,\nu)
=f_0(\tilde x)+\sum_i\lambda_if_i(\tilde x)
\le f_0(\tilde x).
$$

另一方面

$$
g(\lambda,\nu)=\inf_xL(x,\lambda,\nu)
\le L(\tilde x,\lambda,\nu).
$$

合并：

$$
g(\lambda,\nu)\le f_0(\tilde x).
$$

对所有 primal feasible $\tilde x$ 取 infimum：

$$
g(\lambda,\nu)\le p^*.
$$

dual problem 是

$$
d^*=\sup_{\lambda\ge0,\nu}g(\lambda,\nu),
$$

所以

$$
\boxed{d^*\le p^*.}
$$

这就是 weak duality。它只用了 sign convention 和 feasibility，没有用 convexity、differentiability、Slater 或 KKT。

## 三、primal–dual gap：直接可用的误差证书

给定 primal-feasible $\tilde x$ 与 dual-feasible $(\tilde\lambda,\tilde\nu)$，定义

$$
\operatorname{gap}
=f_0(\tilde x)-g(\tilde\lambda,\tilde\nu)\ge0.
$$

由

$$
g(\tilde\lambda,\tilde\nu)\le p^*\le f_0(\tilde x)
$$

得到

$$
0\le f_0(\tilde x)-p^*
\le f_0(\tilde x)-g(\tilde\lambda,\tilde\nu).
$$

因此 gap 不只是一张漂亮图：它给当前 primal point 的 objective suboptimality 上界，而且不要求已经知道 $p^*$。

> [!warning] gap 有前提
> 若 $\tilde x$ 不 primal feasible 或 $\tilde\lambda$ 不 dual feasible，上式不是合法 certificate。数值 solver 必须同时报告 feasibility residual；把轻微不可行点的 objective 直接与 dual bound 相减，可能得到伪小 gap 甚至负 gap。

### 3.1 relative gap

常见 scale-aware 形式：

$$
\operatorname{relgap}
=\frac{f_0(\tilde x)-g(\tilde\lambda,\tilde\nu)}
{1+|f_0(\tilde x)|+|g(\tilde\lambda,\tilde\nu)|}.
$$

但若 objective 可平移/单位不同，relative gap 的解释也会改变；应同时保留 absolute gap 与原始物理单位。

## 四、strong duality、zero gap 与 attainment

### 4.1 三个不同命题

1. **strong duality**：$d^*=p^*$；
2. **primal attainment**：存在 $x^*$ 取得 $p^*$；
3. **dual attainment**：存在 $(\lambda^*,\nu^*)$ 取得 $d^*$。

数值相等不保证任何一侧 supremum/infimum attained。一个 sequence 的 dual values 可趋向 $p^*$，却没有 finite optimal multiplier。

### 4.2 weak duality 的“夹逼”结构

若找到 primal feasible $x^*$ 和 dual feasible $(\lambda^*,\nu^*)$，且

$$
f_0(x^*)=g(\lambda^*,\nu^*),
$$

则由 weak duality，二者分别就是 primal/dual optimum，且 strong duality 成立。这是 primal–dual certificate 的核心。

## 五、Slater condition：最常用的 convex strong-duality 条件

假设：

- $f_0,f_1,\ldots,f_m$ 是 convex functions；
- equalities $h_j(x)=a_j^Tx-b_j$ 是 affine；
- problem proper，$p^*$ finite；
- 存在 $\bar x\in\operatorname{relint}\mathcal D$，满足

$$
f_i(\bar x)<0\quad\forall i,
\qquad h_j(\bar x)=0.
$$

这就是基本 Slater condition。典型结论：

$$
d^*=p^*,
$$

并在标准有限维条件下存在 dual-optimal multipliers；若 primal optimum attained，则最优性可由 KKT 完整刻画。

### 5.1 为什么用 relative interior

若 domain 或 equality constraints 把问题限制在低维 affine hull，全空间 interior 可能为空。relative interior 才表示“在实际可变化的 affine hull 内不贴 domain 边界”。例如 simplex 在 $\mathbb R^d$ 中 interior 为空，但 relative interior 是所有 coordinates 严格正的概率向量。

### 5.2 affine inequality 的细化

若某些 $f_i$ 本身 affine，常见 refined Slater 只要求 nonlinear convex inequalities strict，而 affine inequalities只需 feasible；它们的 boundary 不会产生同样的曲率/domain pathology。使用具体 theorem 时要写清版本，不能把“所有 constraints strict”当唯一形式。

### 5.3 Slater 是充分而非必要

问题

$$
\min_x x^2\quad\text{s.t. }x=0
$$

没有 inequality strict-feasibility 问题，strong duality 成立。另一些 inequality representation 即使不存在 strict point，也可能 zero gap。Slater 的价值是易检查、强结论；它不是 strong duality 的逻辑充要条件。

## 六、为什么 Slater 会带来 zero gap：分离几何骨架

定义 achievable upper set：

$$
\mathcal A=\left\{(u,v,t):
\exists x\in\mathcal D,
\quad f_i(x)\le u_i,
\quad h(x)=v,
\quad f_0(x)\le t
\right\}.
$$

primal optimum 是点 $(0,0,p^*)$ 与该 convex set 的下边界。对 $t<p^*$，点 $(0,0,t)$ 不在 $\mathcal A$。separation theorem 给一个 supporting hyperplane；其 coefficients 可正规化成 $(\lambda,\nu,1)$，并由 upper-set 方向推出 $\lambda\ge0$。分离不等式重排后正是

$$
g(\lambda,\nu)\ge p^*.
$$

再由 weak duality $g\le p^*$，得到 equality。

Slater/relative-interior regularity 防止分离 hyperplane 的 objective coefficient 退化为零，并帮助保证 multiplier finite/attained。完整证明需要 closure 与 relative-interior 细节；这里的关键是：**strong duality 是 convex separation 的结果，不是把 KKT 等式形式上消元得到的。**

## 七、perturbation value function 与 multiplier sensitivity

定义约束扰动：

$$
v(u,w)=\inf_x\left\{
f_0(x):f_i(x)\le u_i,\ h(x)=w
\right\}.
$$

原问题 $p^*=v(0,0)$。在 convex/regular setting，optimal multipliers 给 $v$ 在原点的 supporting affine lower bound：

$$
v(u,w)
\ge v(0,0)-{\lambda^*}^Tu-{\nu^*}^Tw.
$$

若 $v$ differentiable：

$$
\nabla_uv(0,0)=-\lambda^*,
\qquad
\nabla_wv(0,0)=-\nu^*.
$$

这严格限定了 shadow price 解释：multiplier 是 optimal-value function 对 RHS perturbation 的 subgradient/gradient，而不是某个 constraint 的无条件因果效应。

## 八、例一：least-norm equality problem

考虑

$$
\min_x\frac12\|x\|^2
\quad\text{s.t. }Ax=b.
$$

Lagrangian：

$$
L(x,\nu)=\frac12\|x\|^2+\nu^T(Ax-b).
$$

对 $x$ 取 infimum，stationarity 给

$$
x=-A^T\nu.
$$

代回：

$$
g(\nu)
=-\frac12\|A^T\nu\|^2-b^T\nu.
$$

dual：

$$
\max_\nu -\frac12\|A^T\nu\|^2-b^T\nu.
$$

若 $A$ full row rank，dual stationarity 给

$$
AA^T\nu=-b,
$$

所以 primal

$$
x^*=A^T(AA^T)^{-1}b.
$$

若 rank deficient，multiplier 可不唯一，但 $x^*$ 是 unique minimum-norm solution；应使用 solve/pseudoinverse，并区分 primal uniqueness 与 dual uniqueness。

## 九、例二：Lasso dual 与稀疏学习 certificate

primal：

$$
\min_x
\frac12\|Ax-b\|^2+\lambda\|x\|_1,
\qquad\lambda>0.
$$

引入 $r=Ax-b$：

$$
\min_{x,r}\frac12\|r\|^2+\lambda\|x\|_1
\quad\text{s.t. }r=Ax-b.
$$

用 multiplier $u$ 写

$$
L(x,r,u)
=\frac12\|r\|^2+\lambda\|x\|_1
+u^T(Ax-b-r).
$$

对 $r$ 取 infimum：$r=u$，贡献 $-\frac12\|u\|^2$。对 $x$ 取 infimum：

$$
\inf_x\{\lambda\|x\|_1+(A^Tu)^Tx\}
=
\begin{cases}
0,&\|A^Tu\|_\infty\le\lambda,\\
-\infty,&\text{otherwise}.
\end{cases}
$$

所以 dual：

$$
\max_u
-\frac12\|u\|^2-b^Tu
\quad\text{s.t. }\|A^Tu\|_\infty\le\lambda.
$$

任意 primal $x$ 与 dual-feasible $u$ 给 gap。若从 residual $r=Ax-b$ 构造 $u=\alpha r$，可选最大缩放使 $\|A^Tu\|_\infty\le\lambda$，立刻获得训练中的 lower bound。

### 9.1 support certificate

KKT/Fenchel equality 给

$$
-A^Tu\in\lambda\partial\|x\|_1.
$$

若 $x_j\ne0$：

$$
A_j^Tu=-\lambda\operatorname{sign}(x_j).
$$

若 $|A_j^Tu|<\lambda$，则必有 $x_j=0$。这是 dual coordinate 对 sparse support 的证书；finite tolerance 时必须保留 margin。

## 十、Fenchel dual：复合结构的统一推导

考虑

$$
\min_x f(Ax)+g(x),
$$

其中 $f,g$ proper closed convex。引入 $z=Ax$：

$$
L(x,z,y)=f(z)+g(x)+y^T(Ax-z).
$$

对 $z$ 取 infimum：

$$
\inf_z[f(z)-y^Tz]=-f^*(y).
$$

对 $x$ 取 infimum：

$$
\inf_x[g(x)+(A^Ty)^Tx]
=-g^*(-A^Ty).
$$

dual：

$$
\max_y -f^*(y)-g^*(-A^Ty).
$$

zero gap 仍需 qualification，例如存在 $x\in\operatorname{ri}(\operatorname{dom}g)$ 使 $Ax\in\operatorname{ri}(\operatorname{dom}f)$。formal conjugate algebra 本身只生成 candidate dual。

## 十一、saddle point 与 minimax 语言

weak duality是一般 minimax inequality：

$$
\sup_{\lambda\ge0,\nu}\inf_xL(x,\lambda,\nu)
\le
\inf_x\sup_{\lambda\ge0,\nu}L(x,\lambda,\nu).
$$

右侧对 infeasible $x$ 会因 multiplier 放大 constraint violation 而变为 $+\infty$；对 feasible $x$ 等于 $f_0(x)$，因此右侧是 $p^*$。

若存在 saddle point $(x^*,\lambda^*,\nu^*)$：

$$
L(x^*,\lambda,\nu)
\le L(x^*,\lambda^*,\nu^*)
\le L(x,\lambda^*,\nu^*)
$$

对所有相应变量成立，则 primal/dual optimal 且 zero gap。convex–concave、closedness/compactness 或 Slater 等条件帮助交换 inf/sup；不可无条件交换。

## 十二、Farkas certificate：证明线性系统不可行

一个版本：恰有一个系统成立：

1. 存在 $x\ge0$ 使 $Ax=b$；
2. 存在 $y$ 使

$$
A^Ty\ge0,
\qquad b^Ty<0.
$$

若两者同时成立，则

$$
b^Ty=(Ax)^Ty=x^TA^Ty\ge0,
$$

与 $b^Ty<0$ 矛盾。分离定理保证 primal infeasible 时存在这样的 $y$。因此 dual vector 不只给 objective bound，也可给 infeasibility certificate。

## 十三、positive gap、nonattainment 与退化例子

### 13.1 一个可完全手算的 positive gap：三角形 Max-Cut

令 $x_i\in\{-1,1\}$ 表示三角形 $K_3$ 的两个分区：

$$
C(x)=\frac12\sum_{i<j}(1-x_ix_j).
$$

最多切开两条边，故 $\max C=2$。把它写成 minimization：

$$
\min_x
-\frac32+\frac12(x_1x_2+x_2x_3+x_3x_1)
\quad\text{s.t. }x_i^2=1.
$$

所以 $p^*=-2$。对三个 equalities 引入 free multipliers $\nu_i$：

$$
L(x,\nu)
=-\frac32-\sum_i\nu_i+x^TM(\nu)x,
$$

$$
M(\nu)=
\begin{bmatrix}
\nu_1&1/4&1/4\\
1/4&\nu_2&1/4\\
1/4&1/4&\nu_3
\end{bmatrix}.
$$

若 $M(\nu)\succeq0$，则 $\inf_xL=-3/2-\sum_i\nu_i$；否则沿 negative-eigenvalue direction 有 $\inf_xL=-\infty$。dual 因而是

$$
\max_\nu-\frac32-\sum_i\nu_i
\quad\text{s.t. }M(\nu)\succeq0.
$$

由 permutation symmetry 可把任意 feasible multipliers 平均成 $\nu_1=\nu_2=\nu_3=a$ 而不改变 objective。此时 $M$ 的 eigenvalues 为

$$
a+\frac12,\qquad a-\frac14,\qquad a-\frac14.
$$

PSD 要 $a\ge1/4$，最优取 $a=1/4$：

$$
d^*=-\frac32-\frac34=-\frac94.
$$

因此

$$
\boxed{d^*=-\frac94<-2=p^*,\qquad p^*-d^*=\frac14.}
$$

这是 Lagrangian/semidefinite relaxation 的 structural gap。若换 formulation，dual bound 可能变化；**duality gap 依赖 primal representation，而不只依赖可行点集合的口头描述。**

### 13.2 nonconvex 也可能 zero gap

考虑

$$
\min_x x^2\quad\text{s.t. }x^2=1.
$$

primal $p^*=1$。Lagrangian：

$$
L(x,\nu)=(1+\nu)x^2-\nu.
$$

若 $\nu\ge-1$，$g(\nu)=-\nu$；否则 $g=-\infty$。dual 在 $\nu=-1$ 取得 $d^*=1$。所以 nonconvex 不自动意味着 positive gap。

### 13.3 zero gap 但 dual optimum 不 attained

分析 convex problem

$$
\min_x x\quad\text{s.t. }x^2\le0.
$$

唯一 feasible point 是 $0$，故 $p^*=0$。当 $\lambda>0$：

$$
g(\lambda)
=\inf_x(x+\lambda x^2)
=-\frac1{4\lambda}.
$$

$\lambda=0$ 时 $g=-\infty$，而

$$
d^*=\sup_{\lambda>0}-\frac1{4\lambda}=0=p^*.
$$

只有 $\lambda\to\infty$ 才接近 $0$；dual optimum 不 attained，KKT stationarity $1+2\lambda x=0$ 在 $x=0$ 也无 finite solution。这里 Slater/CQ 失败。数值表现正是 gap 下降而 $\|\lambda_k\|$ 发散。

> [!note] 反例的教学目的
> 三个例子分别拆开 positive gap、nonconvex zero gap 与 zero-gap nonattainment，使 convexity、value equality、attainment、KKT existence 和 formulation 不再被混成一句话。

## 十四、nonconvex dual 为什么仍有价值

即使 primal nonconvex：

- weak dual lower bound 仍成立；
- maximization of $g$ 可形成 convex relaxation；
- gap 可量化 relaxation looseness；
- branch-and-bound 用 lower bound 剪枝；
- SDP/Lagrangian relaxations 可给 combinatorial or neural verification bounds。

但：

- $d^*<p^*$ 时再精确求 dual 也不能消掉 relaxation gap；
- dual solution 未必恢复 primal optimizer；
- different formulations 有不同 dual bounds；
- 用 sample/linear relaxations 得到的 bound 只对其假设和 perturbation set 有效。

## 十五、AI 接口

### 15.1 maximum entropy 与 variational inference

moment constraints 的 multipliers成为 exponential-family natural parameters；log-partition 是 dual objective 的核心。Slater/relative-interior 解释 boundary moments 为何可能需要 diverging natural parameters。ELBO 也是 lower bound，但其 gap 来源是 posterior KL；不能把所有“下界”都叫 Lagrange dual。

### 15.2 sparse/structured learning

Lasso/Group Lasso dual feasibility 产生训练 stopping certificate 和 safe screening。primal objective plateau 不说明已最优；small certified gap 才说明 objective error 小。screening 还需用 dual-feasible construction 和 margin，不能直接按小 gradient 删除 feature。

### 15.3 robustness 与 verification

对 adversarial/robust inner problem，dual relaxation可给 worst-case objective 的 bound。要报告：relaxation family、bound direction、dual feasibility、numerical gap，以及 bound 是 sample-specific 还是 population statement。

### 15.4 constrained neural training

primal nonconvex 时，multiplier updates 仍可找 local saddle/KKT point，但 Slater+convex strong duality 通常不适用。empirical fairness/resource constraints 的 dual gap 也不自动成为 population guarantee。

### 15.5 decomposition

dualizing coupling constraints 可让 data shards/agents 独立 minimize local Lagrangians，再由 multipliers协调资源。若 local infimum 不准确、dual nonsmooth 或 primal recovery 未做，dual value 收敛不等于产生可部署 primal solution。

## 十六、数值验收合同

至少同时报告：

1. primal objective $p_k=f_0(x_k)$；
2. dual value $d_k=g(\lambda_k,\nu_k)$；
3. primal feasibility $\|[f(x_k)]_+\|,\|h(x_k)\|$；
4. dual feasibility $\|[-\lambda_k]_+\|$ 和 dual-domain constraints；
5. absolute/relative gap；
6. stationarity/complementarity residual；
7. multiplier norm、constraint scaling 与 active set；
8. inner infimum $g$ 是否 exact/inexact；
9. primal/dual attainment evidence；
10. nonconvex relaxation gap 与 primal recovery quality。

若 $g$ 由 inner iterative minimization近似，computed value 未必是真正 lower bound；需要 inner lower bound 或控制误差方向。

## 十七、常见误区

1. **写出 dual 就有 strong duality**：formal dual 只保证 weak duality；
2. **dual function 需要 primal convex才 concave**：不需要；
3. **zero gap 表示两侧 optimizer 都存在**：value equality 与 attainment 不同；
4. **Slater 是 strong duality 必要条件**：它是常用充分条件；
5. **strict feasible 只看全空间 interior**：低维 domain 要 relative interior；
6. **small gap 无需 feasibility**：不可行点不能直接用标准 certificate；
7. **dual optimum 总能恢复 primal**：nonunique/nonconvex/relaxed 情况均可能失败；
8. **multiplier magnitude 可跨单位比较**：constraint scaling 会反向缩放 multiplier；
9. **ELBO、GAN variational bound 都是同一种 Lagrange dual**：lower-bound mechanism不同；
10. **nonconvex dual 没用**：它仍可给 lower bound，但可能有 structural gap。

## 十八、掌握标准

### Level 1：识别

- 写出 $L,g,d^*$ 与 gap；
- 区分 weak/strong/attainment/Slater。

### Level 2：手算

- 推导 least-norm、LP、Lasso dual；
- 构造 primal/dual feasible pair 并算 gap。

### Level 3：证明

- 证明 $g$ concave 与 weak duality；
- 用 separation 解释 Slater；
- 从 conjugate 推 composite Fenchel dual。

### Level 4：迁移

- 给 sparse/robust problem 构造 certificate；
- 区分 relaxation、optimization 与 statistical gap；
- 审计 inexact dual value 的 bound direction。

## 十九、自检问题

1. 为什么 $g$ 对 multipliers concave，即使 primal nonconvex？
2. weak duality 的每个不等号用了什么？
3. primal-feasible 与 dual-feasible pair 怎样给 suboptimality bound？
4. strong duality 与 dual attainment 有何区别？
5. Slater 为什么写 relative interior？
6. KKT point 的 convex sufficiency 为什么不需要 Slater，而 KKT existence 常需要？
7. Lasso dual 的 $\ell_\infty$ constraint 从哪里来？
8. Fenchel dual 的 qualification 在哪一步缺失会出问题？
9. multiplier 与 perturbation value function 的 derivative 有何关系？
10. nonconvex dual bound 怎样用于 verification，不能证明什么？

## 二十、来源与证据边界

1. Boyd & Vandenberghe, [Stanford EE364A: Duality](https://web.stanford.edu/class/ee364a/lectures/duality.pdf)：Lagrangian/dual function、weak/strong duality、Slater、KKT 与 sensitivity；
2. MIT OCW, [6.253 Convex Analysis and Optimization](https://ocw.mit.edu/courses/6-253-convex-analysis-and-optimization-spring-2012/pages/lecture-notes/) Lectures 8–12：min-common/max-crossing、strong duality、Farkas/Fenchel/conic duality 与 existence；
3. Rockafellar, *Convex Analysis*, 1970：relative interior、separation 与 conjugate duality 的严格理论；
4. Bertsekas, *Convex Optimization Theory*, 2009：perturbation、duality 与 optimality；
5. Wainwright & Jordan, *Graphical Models, Exponential Families, and Variational Inference*, 2008：log-partition/marginal polytope/maximum entropy duality；
6. [[S-2015-Su-3552-最大熵原理]]：maximum entropy 与 Lagrange multiplier 的中文 AI 入口。

> [!info] 证据分工
> Stanford/MIT、Rockafellar/Bertsekas 承担 strong duality、attainment、Slater 和 separation；科学空间只承担 maximum-entropy 问题入口。任何 deep/nonconvex zero-gap 声明必须另有定理或可验证 certificate。

## 二十一、配套训练

- 习题：[[习题 - 弱对偶、强对偶与 Slater 条件]]
- 详解：[[解答 - 弱对偶、强对偶与 Slater 条件]]
- 前驱：[[Lagrange 乘子与 KKT 条件]]、[[次梯度、共轭函数与 Fenchel 对偶]]
- 后继：[[近端算子、复合优化与稀疏正则]]、[[非凸优化、鞍点与深度网络损失地形]]
