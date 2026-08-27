---
type: concept
status: draft
area: [math/convex-analysis, math/inequalities, ai/loss-functions]
aliases: [凸函数, Convex Function, Jensen 不等式, Epigraph]
prerequisites: ["[[凸集、凸组合与分离超平面]]", "[[多元函数、偏导数与方向导数]]", "[[Hessian、二阶微分与曲率]]", "[[期望、方差与矩]]"]
related: ["[[优化与凸分析 MOC]]", "[[最大熵原理与指数族]]", "[[交叉熵与 KL 散度]]", "[[次梯度、共轭函数与 Fenchel 对偶]]"]
sources: ["Boyd-Vandenberghe-2004-Ch3", "Stanford-EE364A-Convex-Functions", "MIT-6.253-Lectures-2-4", "MIT-18.125-Jensen", "Su-9070-LogSumExp-Inequalities"]
created: 2026-08-19
updated: 2026-08-27
---

# 凸函数、Jensen 不等式与上图集

> [!abstract] 本章主问题
> 凸函数把“图像不高于两点 chord”提升为一套等价语言：epigraph 是凸集、任意直线限制凸、一阶切平面是全局下界、二阶 Hessian 半正定、非线性平均满足 Jensen。它让局部最优成为全局最优，却只对正确 domain 和参数变量成立；一个 loss 对 logits 凸，不代表对深网权重凸。

## 学习目标

完成本章后，你应当能够：

1. 用 chord inequality 定义 convex/strictly convex function；
2. 解释 effective domain 为什么必须 convex；
3. 使用 extended-value formulation 合并 objective 与 convex constraint；
4. 证明 $f$ convex 当且仅当 $\operatorname{epi}f$ convex；
5. 用 line restriction 判断多元函数 convexity；
6. 推导 differentiable convex function 的一阶 supporting-hyperplane condition；
7. 推导 twice-differentiable function 的 Hessian PSD 判据；
8. 区分 convex、strictly convex、strongly convex 与 quasiconvex；
9. 证明 finite Jensen，并写出随机变量版本的可积性条件；
10. 判断 Jensen equality，计算 Jensen gap；
11. 使用非负和、affine composition、pointwise supremum、composition rule 与 perspective；
12. 避免“两个凸函数复合仍凸”等错误；
13. 证明 norm、quadratic、exponential、negative log 与 logsumexp 的 convexity；
14. 推导 logsumexp 的 softmax gradient 与 covariance Hessian；
15. 审计 cross-entropy、attention、variational bound 和 deep loss 中的 convexity 声明。

> [!question] 初学者读完必须能回答
> 1. chord inequality 为什么还必须连同 convex effective domain 一起定义？
> 2. $f$ convex 与 $\operatorname{epi}f$ convex、所有直线 restriction convex 怎样等价？
> 3. differentiable 一阶支撑条件与 twice-differentiable Hessian PSD 条件怎样推出？
> 4. convex、strictly convex、strongly convex 与 quasiconvex 的结论强度有何差别？
> 5. Jensen 的有限加权和与随机变量版本需要哪些可积性条件，等号何时成立？
> 6. 非负和、affine composition、supremum、monotone composition 与 perspective 的保凸规则如何核对？
> 7. logsumexp 为什么凸，其 softmax gradient 与 covariance Hessian 怎样连接 AI loss？

## 阅读前检查

- [[凸集、凸组合与分离超平面]]：convex combination、epigraph 所在空间与 separation；
- [[多元函数、偏导数与方向导数]]：domain、gradient、directional slice；
- [[Hessian、二阶微分与曲率]]：Hessian quadratic form；
- [[期望、方差与矩]]：随机变量、expectation 与 Jensen 的概率语言。

> [!note] 课程位置
> OPT-02 研究“允许选择哪些点”的凸几何；本章研究“沿这些点之间的线段，目标值怎样弯曲”。凸函数把局部支撑线升级成全局下界，使局部极小不再是坏陷阱，并为 OPT-04 的次梯度、OPT-05 的曲率常数以及后续一阶复杂度证明提供共同语言。AI 中最关键的边界是：一个损失对 prediction/logits 凸，不代表它对生成这些量的深网参数凸。

> [!tip] 建议两遍阅读
> **第一遍**只在贯穿二次函数上往返 chord、epigraph、一阶支撑、Hessian 和 Jensen 五种语言。**第二遍**再系统学习 composition、perspective、logsumexp、strict/strong/quasiconvex 的区别。每次声称“凸”时，都要把变量和 domain 一起念出来。

## 本章的推导问题链

1. 集合的线段闭包怎样转化为函数值相对 chord 的不等式？
2. 为什么 $f$ convex 等价于 epigraph convex？
3. 可微时，局部 tangent 为什么会成为对所有 $y$ 成立的全局下界？
4. 二次可微时，为什么沿每个方向的非负曲率等价于 Hessian PSD？
5. finite convex combination 怎样递推成 Jensen，随机变量版本又多了哪些可积性条件？
6. 把 convex objective 与 convex-set indicator 相加后，怎样得到统一的 extended-value problem？

## 贯穿算例续：同一二次目标的五种凸性语言

仍令

$$
q(x)=\frac12\|x-a\|_2^2,
\qquad
a=\begin{pmatrix}1\\1\end{pmatrix},
\qquad
C=\operatorname{conv}\{0,e_1,e_2\}.
$$

定义 extended-value objective

$$
F(x)=q(x)+\delta_C(x).
$$

那么 $\operatorname{dom}F=C$，且 $\min_xF(x)$ 与 $\min_{x\in C}q(x)$ 是同一个问题。这里的 $+\infty$ 是数学上禁止不可行点的编码，不是训练代码中应真的产生的浮点数。

### 符号与对象账本

| 符号 | 类型 | 本例含义 | 不可混淆对象 |
|---|---|---|---|
| $q(x)$ | finite-valued function | 平滑平方距离 | 单个样本 loss/部署 metric |
| $\delta_C(x)$ | extended-value function | 可行域 indicator | 0–1 指示随机变量 |
| $F=q+\delta_C$ | proper convex function | 合并目标和约束 | 数值程序直接计算的普通 loss |
| $\operatorname{epi}F$ | $\mathbb R^3$ 中的集合 | $F$ 图像上方区域 | sublevel set |
| $\nabla q(x)=x-a$ | primal gradient | 当前点的局部线性系数 | projection residual $a-x$ 的相反数 |
| $\nabla^2q(x)=I$ | Hessian/线性算子 | 所有方向曲率均为 1 | 任意神经网络参数 Hessian |
| $J_\theta(x,y)$ | Jensen gap | chord 高度减函数值 | optimization gap $F(x)-F^*$ |

### 语言一：精确 chord identity

令 $m=\theta x+(1-\theta)y$。平方范数恒等式给出

$$
\boxed{
\theta q(x)+(1-\theta)q(y)-q(m)
=\frac{\theta(1-\theta)}2\|x-y\|_2^2
\ge0.
}
$$

因此 $q$ convex；当 $x\ne y$ 且 $\theta\in(0,1)$ 时 gap 严格为正，所以它甚至 strictly convex。注意 strict convexity 的结论是对当前变量 $x$ 而言，不会穿过任意非线性 reparameterization 自动保留。

### 语言二与三：一阶支撑和 Hessian

直接求导：

$$
\nabla q(x)=x-a,
\qquad
\nabla^2q(x)=I\succeq0.
$$

而精确 Taylor 展开为

$$
q(y)=q(x)+\nabla q(x)^T(y-x)+\frac12\|y-x\|_2^2.
$$

删去最后一个非负项，就得到凸函数的一阶支撑条件

$$
q(y)\ge q(x)+\nabla q(x)^T(y-x).
$$

这里“tangent 在图像下方”不是视觉猜测，而是由一个明确的平方余项证明。

### 语言四：epigraph 与 indicator

$q$ 的 epigraph convex；OPT-02 已证明 $C$ convex，所以 $\delta_C$ convex，非负和规则进一步给 $F=q+\delta_C$ convex。于是对任意可行 $x,y$，其中间点仍可行且

$$
F(\theta x+(1-\theta)y)
\le\theta F(x)+(1-\theta)F(y).
$$

若某个端点不可行，右侧含 $+\infty$，不等式仍在 extended-real 意义下成立；这正是 domain 信息没有被丢掉的好处。

### 语言五：一个可手算的 Jensen gap

取 $x=e_1$、$y=e_2$、$\theta=1/2$。两端都在 $C$，且

$$
q(e_1)=q(e_2)=\frac12,
\qquad
q\!\left(\frac{e_1+e_2}{2}\right)=\frac14.
$$

因此

$$
\frac12q(e_1)+\frac12q(e_2)
-q\!\left(\frac{e_1+e_2}{2}\right)
=\frac14.
$$

这里的 $1/4$ 是这两个端点与该混合权重下的 Jensen gap；它恰好等于本例最优值只是数值巧合，二者定义和参照对象不同。

### 核心公式七问：精确 Jensen gap

对

$$
J_\theta(x,y)
=\theta q(x)+(1-\theta)q(y)
-q(\theta x+(1-\theta)y)
=\frac{\theta(1-\theta)}2\|x-y\|^2,
$$

逐项回答：

1. **目的：**同时证明 convexity，并定量说明混合带来的 chord gap；
2. **对象：**$x,y$ 是同一 domain 中的输入，$\theta$ 是 convex-combination 权重；
3. **来路：**展开三个平方项，关于 $a$ 的一次项完全抵消；
4. **步骤：**先合并 $\|\theta(x-a)+(1-\theta)(y-a)\|^2$，再收集成 $\|x-y\|^2$；
5. **读法：**端点越远、混合越均衡，当前二次函数的 Jensen gap 越大；
6. **检查：**$x=y$ 或 $\theta\in\{0,1\}$ 时 gap 必须为 0；交换 $x,y$ 并把 $\theta$ 换成 $1-\theta$ 不变；
7. **去路：**OPT-05 会把右侧的精确系数推广为 strong-convexity 下界，OPT-06 会把同一曲率用于梯度下降速率。

> [!warning] AI 中的变量边界
> $q$ 对 mixture weights $x$ convex；若 $x=x_\theta$ 由深网产生，复合函数 $q(x_\theta)$ 对参数 $\theta$ 一般非凸。类似地，cross-entropy 对 logits convex，也不推出整网训练问题 convex。必须逐次声明“对谁凸”。

> [!success] 第一遍停靠线
> 合上笔记后，能从平方展开独立重建 chord identity、一阶支撑式与 Hessian $I$；能用 $e_1,e_2$ 手算 Jensen gap $1/4$；还能解释 $F=q+\delta_C$ 为什么把约束吸收到 domain 中，以及为什么这不等于程序应计算 `inf`。达不到时，先不要进入次梯度和共轭。

## 零、同一个函数的四张“身份证”

考虑

$$
f(x)=e^x.
$$

你可以用四种方式识别它 convex：

1. chord：

$$
e^{\theta x+(1-\theta)y}
\le\theta e^x+(1-\theta)e^y;
$$

2. epigraph：图像上方区域 convex；
3. first order：

$$
e^y\ge e^x+e^x(y-x);
$$

4. second order：

$$
f''(x)=e^x>0.
$$

Jensen 又把 chord 扩展到随机平均：

$$
e^{E[X]}\le E[e^X].
$$

这四种语言分别适合 definition、几何、优化证书和微分计算；真正掌握是能在它们之间转换，而不是只背 $f''\ge0$。

先用下图回答一个视觉问题：**chord、切线、Jensen gap 与 logsumexp Hessian 为什么是同一凸性的四种接口？**

![[00-知识库管理/_assets/figures/optimization/fig-convex-functions-jensen-epigraph-v2.svg|880]]

> [!figure] 图 10.7.3｜凸函数 chord/Jensen 几何与 logsumexp 曲率
> A 在一维凸曲线上同时画出端点 chord 与局部 supporting tangent；B 把“先平均再过函数”与“先过函数再平均”画成两条路径；C 给出 logsumexp、softmax gradient 与 categorical-covariance Hessian。来源：独立绘制；生成脚本：[[plot_convex_foundations_v2.py]]；确定性结构示意，无随机种子。

**怎样读图。** A 记住函数图像位于 chord 下、任意一阶支撑线之上；B 比较两条路径终点得到 Jensen inequality，并把 gap 归因于输入 spread 与函数 curvature；C 沿导数链检查 Hessian 半正定，从而确认对 logits 的凸性。

**适用边界（图没有证明什么）。** A 是可微一维示意，凸函数可以不可微且定义在一般向量空间；Jensen 需要 $X$ 与 $f(X)$ 的适当可积性，严格凸下等号仍需考虑 a.s. 常值/affine region；logsumexp 对 logits 凸不推出对产生 logits 的深网权重凸。

## 一、定义：图像位于 chord 下方

> [!definition] convex function
> 函数 $f:\mathbb R^n\to\mathbb R\cup\{+\infty\}$ 称 convex，若 $\operatorname{dom}f$ convex，且对任意 $x,y\in\operatorname{dom}f$、$\theta\in[0,1]$：
> $$
> f(\theta x+(1-\theta)y)
> \le\theta f(x)+(1-\theta)f(y).
> $$

右侧是端点函数值的线性插值，即 chord height；左侧是中间输入的实际函数值。

### 1.1 concave function

$f$ concave 当且仅当 $-f$ convex，等价于不等号反向。maximum likelihood 中 log-likelihood 常 concave，于是 maximize concave 等价于 minimize convex negative log-likelihood。

### 1.2 strict convexity

若对 $x\ne y$、$\theta\in(0,1)$ 总有严格不等式

$$
f(\theta x+(1-\theta)y)
<\theta f(x)+(1-\theta)f(y),
$$

则 $f$ strictly convex。

strict convexity 在 convex feasible set 上保证至多一个 minimizer：若两个不同 minimizers 存在，midpoint 的函数值会严格更低，矛盾。

### 1.3 strong convexity 先只区分

$f$ 是 $\mu$-strongly convex（相对 Euclidean norm），若

$$
f(y)
\ge f(x)+\nabla f(x)^T(y-x)
+\frac\mu2\|y-x\|_2^2.
$$

strong convexity 给 uniform quadratic curvature；strict convexity 不一定给任何统一 $\mu>0$。例如 $x^4$ strictly convex，但在 0 附近 Hessian 为 0，不是 globally strongly convex。

完整条件数与收敛结果留给[[光滑性、强凸性与条件数]]。

## 二、domain 与 extended-value 不能省略

函数

$$
f(x)=-\log x
$$

只在 $(0,\infty)$ 上定义并 convex。若把 domain 漏掉，拿负数点做 convex combination，表达式没有意义。

集合 $C$ 的 indicator

$$
\delta_C(x)=
\begin{cases}
0,&x\in C,\\
+\infty,&x\notin C
\end{cases}
$$

当且仅当 $C$ convex 时是 convex extended-value function。于是

$$
\min_{x\in C}f(x)
\quad\Longleftrightarrow\quad
\min_x f(x)+\delta_C(x).
$$

这允许用一个函数同时携带 objective 和 feasible geometry；但计算实现中仍需 projection/prox/barrier，而不是把 `inf` 送入普通算子。

## 三、epigraph：把函数凸性化成集合凸性

定义 epigraph

$$
\operatorname{epi}f
=\{(x,t)\in\mathbb R^{n+1}:t\ge f(x)\}.
$$

> [!theorem] epigraph characterization
> $f$ convex 当且仅当 $\operatorname{epi}f$ 是 convex set。

### 3.1 从函数到 epigraph

取 $(x,s),(y,t)\in\operatorname{epi}f$，所以 $s\ge f(x),t\ge f(y)$。则

$$
\begin{aligned}
f(\theta x+(1-\theta)y)
&\le\theta f(x)+(1-\theta)f(y)\\
&\le\theta s+(1-\theta)t.
\end{aligned}
$$

因此其 convex combination 仍在 epigraph。

### 3.2 从 epigraph 到函数

取 boundary points $(x,f(x))$ 与 $(y,f(y))$。epigraph convex 给

$$
(\theta x+(1-\theta)y,
\theta f(x)+(1-\theta)f(y))
\in\operatorname{epi}f,
$$

正是 convex inequality。

### 3.3 epigraph reformulation

$$
\min_x f(x)
$$

等价于

$$
\min_{x,t}t
\quad\text{s.t.}\quad
f(x)\le t.
$$

若 $f$ convex，则 epigraph constraint convex。max、norm、absolute value 和 logsumexp 常借 auxiliary variable 变成 epigraph constraints。

## 四、sublevel set 与 quasiconvex 边界

对 $\alpha\in\mathbb R$，sublevel set

$$
C_\alpha=\{x:f(x)\le\alpha\}.
$$

若 $f$ convex，$x,y\in C_\alpha$，则

$$
f(\theta x+(1-\theta)y)
\le\theta f(x)+(1-\theta)f(y)
\le\alpha,
$$

所以 $C_\alpha$ convex。

反向不成立。函数

$$
f(x)=x^3
$$

在 $\mathbb R$ 上所有 sublevel sets 都是 intervals，故 quasiconvex；但

$$
f''(x)=6x
$$

在负半轴为负，不 convex。quasiconvex optimization 可有 convex sublevel geometry，却没有完整 chord/first-order structure。

## 五、line restriction：多元问题降成一元

> [!theorem] line characterization
> $f$ 在 convex domain 上 convex，当且仅当对每个 $x$ 和方向 $v$，一元函数
> $$
> g(t)=f(x+tv)
> $$
> 在其 domain
> $$
> \{t:x+tv\in\operatorname{dom}f\}
> $$
> 上 convex。

正向是把两点放在一条直线上；反向则任取 $x,y$，令 $v=y-x$，对 $g$ 使用一元 convex inequality。

这条原则很实用：

- Hessian directional curvature 为 $v^T\nabla^2f(x)v$；
- matrix function 可沿 $X+tH$ 检查；
- 反例只需找到一个方向 slice 非凸；
- 随机 direction test 是诊断，不是对所有方向的证明。

## 六、一阶 characterization：切平面是全局下界

设 $f$ differentiable、domain open convex。

> [!theorem] first-order condition
> $f$ convex 当且仅当
> $$
> f(y)\ge f(x)+\nabla f(x)^T(y-x),
> \qquad\forall x,y.
> $$

### 6.1 convex 推出切平面下界

令

$$
g(t)=f(x+t(y-x)).
$$

convexity 对 $t\in(0,1]$ 给

$$
g(t)\le(1-t)g(0)+tg(1).
$$

整理：

$$
g(1)\ge g(0)+\frac{g(t)-g(0)}t.
$$

令 $t\downarrow0$：

$$
f(y)\ge f(x)+\nabla f(x)^T(y-x).
$$

### 6.2 一阶下界推出 convexity

令 $z=\theta x+(1-\theta)y$。分别在 $z$ 处对 $x,y$ 用下界：

$$
f(x)\ge f(z)+\nabla f(z)^T(x-z),
$$

$$
f(y)\ge f(z)+\nabla f(z)^T(y-z).
$$

乘 $\theta,1-\theta$ 相加，linear terms 抵消，得到

$$
\theta f(x)+(1-\theta)f(y)\ge f(z).
$$

### 6.3 local minimum 自动 global

若 $x^*$ 是 differentiable convex $f$ 的 unconstrained stationary point：

$$
\nabla f(x^*)=0,
$$

则对任意 $y$：

$$
f(y)\ge f(x^*)+
\nabla f(x^*)^T(y-x^*)=f(x^*).
$$

更一般地，convex function 在 convex feasible set 上任意 local minimizer 都 global：若存在更优 $y$，则从 $x^*$ 朝 $y$ 的任意小 convex combination 都更优，否定 local optimality。

## 七、二阶 characterization：Hessian PSD

设 $f$ twice differentiable，domain open convex。

> [!theorem] second-order condition
> $f$ convex 当且仅当
> $$
> \nabla^2f(x)\succeq0,
> \qquad\forall x\in\operatorname{dom}f.
> $$

对任意 line restriction $g(t)=f(x+tv)$：

$$
g''(t)
=v^T\nabla^2f(x+tv)v.
$$

所有 directions 上 $g''\ge0$ 等价于 Hessian PSD。

### 7.1 PSD 不等于 positive definite everywhere

$f(x)=x^4$ convex 且 strictly convex，但

$$
f''(0)=0.
$$

所以 strict convexity 不要求 Hessian 在每一点 positive definite。若 Hessian $\succeq\mu I$，才是 $\mu$-strong convexity 的充分/相应等价条件。

### 7.2 Hessian 判据是变量相关的

$f(x)=x^2$ 对 $x$ convex。重参数化 $x=u^3-u$ 后，

$$
g(u)=(u^3-u)^2
$$

未必 globally convex。convexity 不在任意 nonlinear coordinate change 下保持。

## 八、Jensen 不等式

### 8.1 finite Jensen

若 $f$ convex，$\theta_i\ge0,\sum_i\theta_i=1$，则

$$
\boxed{
f\!\left(\sum_{i=1}^k\theta_i x_i\right)
\le\sum_{i=1}^k\theta_i f(x_i).
}
$$

证明用二点定义 induction：把前 $k-1$ 个点先归一化平均，再与第 $k$ 个点做一次二点 convex combination。

### 8.2 随机变量版本

若 $X$ 可积、取值落在 convex domain，并且 $f(X)$ 的 expectation 有定义，则

$$
\boxed{
f(E[X])\le E[f(X)].
}
$$

一般证明可用 supporting hyperplane/subgradient：在 $E[X]$ 处取 $g\in\partial f(E[X])$，

$$
f(X)\ge f(E[X])+g^T(X-E[X]),
$$

取 expectation 后 linear term 为 0。

### 8.3 equality

若 $f$ strictly convex 且 $X$ non-degenerate（不几乎处处为常数），通常 strict：

$$
f(E[X])<E[f(X)].
$$

一般 convex $f$ 的 equality 可在 $X$ 的 support 落于 $f$ 的 affine region 时发生。例如 $f(x)=|x|$ 且 $X\ge0$ a.s.，即使 $X$ 随机也可取等。

### 8.4 Jensen gap 与 variance 的局部关系

一维 twice differentiable $f$，若 $X$ 集中在 $\mu=E[X]$ 附近，Taylor 给

$$
E[f(X)]-f(E[X])
\approx\frac12f''(\mu)\operatorname{Var}(X).
$$

这是局部近似，不是无条件等式。若 $m\le f''\le M$ 在 relevant interval，则可给

$$
\frac m2\operatorname{Var}(X)
\le E[f(X)]-f(E[X])
\le\frac M2\operatorname{Var}(X).
$$

## 九、Jensen 的 AI/概率接口

### 9.1 negative log 与 likelihood

$-\log x$ convex，因此对正随机变量 $W$：

$$
-\log E[W]\le E[-\log W].
$$

等价于

$$
\log E[W]\ge E[\log W]
$$

（log concave）。ELBO、importance-weighted bounds 和 mixture code 都依赖这种方向；写错曲率就会把 lower bound 变 upper bound。

### 9.2 averaging logits 与 averaging probabilities

softmax nonlinear，所以

$$
\operatorname{softmax}(E[Z])
\ne E[\operatorname{softmax}(Z)]
$$

一般成立。ensemble logits、probabilities 和 losses 是不同 averaging protocol。

### 9.3 stochastic training

若 $f$ convex，

$$
f(E[X])\le E[f(X)]
$$

表示 parameter averaging 的 objective 不高于 average objective；但深网 loss 通常对参数非凸，此结论不能机械用于 checkpoint averaging。局部 basin 或 function-space averaging 需另证。

## 十、保凸 calculus

### 10.1 nonnegative weighted sum

若 $f_i$ convex，$a_i\ge0$，则

$$
f(x)=\sum_i a_if_i(x)
$$

convex。负权重会翻转 curvature，不能无条件使用。

### 10.2 affine precomposition

若 $f$ convex，则

$$
g(x)=f(Ax+b)
$$

convex，因为 affine map 保持 convex combinations。

这解释了 linear predictor 上 convex loss 的 convexity；若 predictor 换成 deep network，就失去 affine precomposition。

### 10.3 pointwise maximum/supremum

若每个 $f_i$ convex，则

$$
f(x)=\max_i f_i(x)
$$

convex，因为

$$
\operatorname{epi}f
=\bigcap_i\operatorname{epi}f_i.
$$

无限 family 的 pointwise supremum 在 proper domain 上也 convex。pointwise minimum 一般不保凸。

### 10.4 composition rule

标量 outer $h$ convex 且 nondecreasing，inner $g$ convex，则

$$
h\circ g
$$

convex。若 $h$ convex nonincreasing，则需要 $g$ concave。

证明对 nondecreasing case：

$$
g(\theta x+(1-\theta)y)
\le\theta g(x)+(1-\theta)g(y),
$$

先用 $h$ monotonicity，再用 $h$ convexity。

“convex composed with convex”若没有 monotonicity 就可能失败。例如

$$
h(u)=u^2,
\qquad
g(x)=x^2-1,
$$

两者 convex，但

$$
(x^2-1)^2
$$

在 0 附近二阶导为负，不 convex。

### 10.5 perspective

若 $f$ convex，perspective

$$
g(x,t)=t f(x/t),
\qquad t>0
$$

convex。它把 ratios、relative entropy、quadratic-over-linear 与 conic reformulation 连接：

$$
f(u)=u^2
\Longrightarrow
g(x,t)=\frac{x^2}{t}.
$$

### 10.6 partial minimization 的条件

若 $F(x,y)$ jointly convex，$C$ convex，定义

$$
g(x)=\inf_{y\in C}F(x,y),
$$

则在适当 proper 条件下 $g$ convex。epigraph 是 joint epigraph 与 constraint 的 projection；但 closedness/attainment 可能丢失。

## 十一、基本 convex functions

### 11.1 affine function

$$
f(x)=a^Tx+b
$$

同时 convex 和 concave，chord equality 恒成立。

### 11.2 norms

triangle inequality 与 positive homogeneity 给

$$
\|\theta x+(1-\theta)y\|
\le\theta\|x\|+(1-\theta)\|y\|.
$$

所以任意 norm convex。

### 11.3 quadratic

$$
f(x)=\frac12x^TQx+b^Tx+c
$$

Hessian 为对称部分

$$
\nabla^2f=\frac{Q+Q^T}{2}.
$$

通常先令 $Q$ symmetric；$f$ convex 当且仅当 $Q\succeq0$。

### 11.4 exponential 与 negative log

$$
e^x:\quad f''=e^x>0,
$$

$$
-\log x:\quad f''=\frac1{x^2}>0,
\quad x>0.
$$

### 11.5 negative entropy

在 positive orthant：

$$
f(x)=\sum_i x_i\log x_i
$$

Hessian

$$
\nabla^2f=\operatorname{diag}(1/x_i)\succ0.
$$

在 simplex 上它是 negative Shannon entropy；entropy 本身 concave。

## 十二、logsumexp：AI 中最重要的 convex smooth max

定义

$$
\operatorname{LSE}(x)
=\log\sum_{i=1}^ne^{x_i}.
$$

### 12.1 max bounds

令 $m=\max_i x_i$。则

$$
e^m\le\sum_ie^{x_i}\le ne^m,
$$

所以

$$
\boxed{
m\le\operatorname{LSE}(x)\le m+\log n.
}
$$

temperature version

$$
\operatorname{LSE}_\tau(x)
=\tau\log\sum_i e^{x_i/\tau}
$$

满足 approximation gap 至多 $\tau\log n$。

### 12.2 gradient 是 softmax

$$
\frac{\partial\operatorname{LSE}}{\partial x_i}
=\frac{e^{x_i}}{\sum_je^{x_j}}
=p_i.
$$

所以

$$
\nabla\operatorname{LSE}(x)=p=\operatorname{softmax}(x).
$$

### 12.3 Hessian 是 categorical covariance

$$
\nabla^2\operatorname{LSE}(x)
=\operatorname{diag}(p)-pp^T.
$$

对任意 $v$：

$$
v^T\nabla^2\operatorname{LSE}(x)v
=\sum_ip_iv_i^2-\left(\sum_ip_iv_i\right)^2
=\operatorname{Var}_{I\sim p}(v_I)
\ge0.
$$

因此 LSE convex。

### 12.4 为什么不 strictly convex on $\mathbb R^n$

对常数 $c$：

$$
\operatorname{LSE}(x+c\mathbf1)
=c+\operatorname{LSE}(x).
$$

沿 $\mathbf1$ 方向是 affine，Hessian 满足

$$
(\operatorname{diag}p-pp^T)\mathbf1=0.
$$

所以 full space 上没有 strict/strong convexity；在 quotient/固定 gauge 子空间才可能有更强结构。

### 12.5 数值稳定实现

$$
\operatorname{LSE}(x)
=m+\log\sum_ie^{x_i-m}.
$$

这是 algebraically identical 的稳定改写，避免 exponent overflow。convexity theorem 不保证 floating-point naive implementation 稳定。

[[S-2022-Su-9070-logsumexp不等式]]提供 max bound、temperature 与 Jensen 的中文入口；本章用 gradient/Hessian、domain 和严格凸性边界补齐正式结构。

## 十三、cross-entropy 的凸性到底对谁成立

对 target class $y$ 和 logits $z\in\mathbb R^K$：

$$
\ell(z,y)
=\operatorname{LSE}(z)-z_y.
$$

convex function 减 affine 仍 convex，因此对 logits $z$ convex；Hessian 与 LSE 相同 PSD。

若 logits 是 affine model

$$
z=Wx+b,
$$

对 $(W,b)$ 的 empirical sum 仍 convex（无 hidden nonlinear layer）。若

$$
z=f_\theta(x)
$$

是 deep network，affine-precomposition rule 失效，loss 对 $\theta$ 一般非凸。

因此以下三个命题不同：

1. loss 对 prediction/logits convex；
2. loss 对最后一层参数 convex（固定 features）；
3. loss 对全部 network parameters convex。

只证明第 1 条不能声称第 3 条。

## 十四、convex optimization 的全局结构

标准 convex optimization problem 要求：

$$
\min_x f_0(x)
$$

其中 $f_0$ convex；inequality constraints

$$
f_i(x)\le0
$$

的 $f_i$ convex；equality constraints

$$
h_j(x)=0
$$

必须 affine。于是 feasible set 是 convex sublevel sets 与 affine sets 的 intersection。

为什么 equality 必须 affine：若 $h$ convex non-affine，$h(x)=0$ level set 可像 sphere 一样非凸。

在这个结构下：

- local minimizer 是 global；
- strict convex objective 给至多一个 minimizer；
- first-order/subgradient condition 可成为 global certificate；
- separation 导出 dual lower bound；
- 但 existence、conditioning 和算法效率仍需 closedness/coercivity/smoothness 等。

convex 不等于“容易到常数时间”，也不等于数值稳定；它提供结构，不消除 dimension、oracle cost 或 ill-conditioning。

## 十五、DCP 与“可识别的凸性”

Disciplined Convex Programming 使用一组 atoms 的 curvature、sign 与 monotonicity composition rules 验证表达式。它是充分规则系统：

- 通过规则的表达式有 convexity certificate；
- 未通过不等于数学上一定非凸，可能需要 reformulation；
- 在参数被误标 sign、domain 或 variable 时，规则结论也会变；
- solver acceptance 不证明 problem instance feasible 或 well-conditioned。

对 AI pipeline，最好分别保存：symbolic objective、DCP canonicalization、solver status、primal/dual residual 和原尺度 metric。

## 十六、常见错误与纠正

| 错误 | 问题 | 纠正 |
|---|---|---|
| $f''\ge0$ 是凸性的定义 | 只适用于足够光滑一维/line | 定义是 chord；导数是判据 |
| convex function 必可微 | $|x|$, max | 用 subgradient/epigraph |
| strict convex 等于 strong convex | $x^4$ | strong 需要 uniform quadratic lower bound |
| 所有 sublevel sets convex 就说明 convex | $x^3$ | 只推出 quasiconvex |
| 两个 convex functions 复合仍 convex | $(x^2-1)^2$ | 检查 outer monotonicity |
| pointwise minimum 保凸 | 双井可由两个 bowls 的 min 产生 | maximum/supremum 才无条件保凸 |
| Jensen 可随意交换任何非线性与期望 | 曲率/可积性未查 | 先写 convex/concave 与 domain |
| LSE strictly convex | shift direction affine | Hessian 有 $\mathbf1$ null direction |
| CE convex，所以深网训练凸 | 变量偷换 | 只对 logits/线性参数成立 |
| convex 说明 solver 一定快且稳定 | conditioning/oracle/dimension | 另报复杂度与数值证书 |

## 十七、你应能独立重建的统一链

$$
\text{chord inequality}
\Longleftrightarrow
\operatorname{epi}f\text{ convex},
$$

对于 differentiable $f$：

$$
f(y)\ge f(x)+\nabla f(x)^T(y-x),
$$

对于 twice differentiable $f$：

$$
\nabla^2f(x)\succeq0,
$$

对于 random convex combinations：

$$
f(E[X])\le E[f(X)].
$$

四式不是四个孤立定理，而是同一“平均输入不会高于平均输出”的几何结构。

下一章[[次梯度、共轭函数与 Fenchel 对偶]]将把 differentiable tangent 下界推广到不可微 convex functions，并把所有 affine lower bounds 的最优组合组织成 conjugate/dual。

## 习题与解答

- [[习题 - 凸函数、Jensen 不等式与上图集]]：15 道 A—E 分层训练；
- [[解答 - 凸函数、Jensen 不等式与上图集]]：四种凸性证明、Jensen gap、composition 反例、logsumexp 与 AI 审计。

## 参考来源

- Boyd & Vandenberghe, [*Convex Optimization*](https://stanford.edu/~boyd/cvxbook/)，Chapter 3；
- Stanford EE364A, [Convex Functions lecture](https://see.stanford.edu/Course/EE364A/93)；
- MIT 6.253, [Convex Analysis and Optimization lecture notes](https://ocw.mit.edu/courses/6-253-convex-analysis-and-optimization-spring-2012/pages/lecture-notes/)；
- MIT 18.125, [Convex Functions and Jensen’s Inequality](https://ocw.mit.edu/courses/18-125-measure-and-integration-fall-2003/resources/18125_lec14/)；
- [[S-2022-Su-9070-logsumexp不等式]]。
