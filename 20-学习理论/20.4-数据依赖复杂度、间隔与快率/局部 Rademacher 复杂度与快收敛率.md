---
type: theorem
status: draft
area: [learning-theory/local-complexity, statistical-rates]
aliases: [Local Rademacher Complexity, Sub-Root Fixed Point, Fast Rates]
node_id: LT-31
prerequisites: ["[[Rademacher 复杂度与经验复杂度]]", "[[覆盖数、Metric Entropy 与 Chaining 入口]]", "[[光滑性、强凸性与条件数]]"]
related: ["[[正则化 ERM 的稳定性]]", "[[核岭回归与 Gaussian Process 接口]]", "[[正则化、交叉验证与模型选择]]", "[[神经网络容量与 Norm-Based Bound]]"]
sources: ["[[S-2005-Bartlett-Bousquet-Mendelson-Local-Rademacher]]", "[[S-2002-Bartlett-Mendelson-Rademacher-Gaussian]]", "[[S-2018-Mohri-Rostamizadeh-Talwalkar-Foundations-ML]]"]
exercises: ["[[习题 - 局部 Rademacher 复杂度与快收敛率]]"]
solutions: ["[[解答 - 局部 Rademacher 复杂度与快收敛率]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-local-rademacher-fixed-point-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# 局部 Rademacher 复杂度与快收敛率

> [!abstract] 本章主问题
> 全局 Rademacher complexity 让所有函数参与 supremum，包括风险极差、远离最优解的函数；但 ERM 的候选解在证明后期通常被限制在一个小 excess-risk/variance 区域。局部复杂度研究
> $$
> \mathcal G(r)
> =\{g\in\operatorname{star}(\mathcal G,0):Pg^2\le r\}
> $$
> 上的随机过程，并用 sub-root envelope $\psi(r)$ 的 fixed point
> $$
> \psi(r^*)=r^*
> $$
> 找到自洽误差尺度。若再有 Bernstein/curvature 条件把 variance 与 mean excess risk 连接，excess risk 可从全局 $m^{-1/2}$ 型改善到某些问题中的 $m^{-1}$ 型。localization 本身不是快率保证；class、loss、noise、curvature、star hull、peeling 和 empirical radius 都是 theorem 的组成部分。

> [!question] 初学者读完必须能回答
> 1. 为什么“只看好函数”不能直接用未知 population risk 定义并计算？
> 2. excess loss 与 parameter distance 为什么不是同一个对象？
> 3. sub-root 的定义是什么，fixed point 为什么给出自洽 radius？
> 4. Bernstein condition 怎样把二阶波动转换成一阶 excess risk？
> 5. 为什么 $\sqrt{d/m}$ 的 local expression 能在 fixed point 后变成 $d/m$？

## 一、学习目标

1. 定义 excess-loss class、star hull 与 population/empirical local slices；
2. 区分 global complexity 与 localized complexity；
3. 定义 sub-root function 并证明 fixed point 的基本支配性质；
4. 解释 peeling、weighting 与 empirical inflation 的角色；
5. 写出 Bernstein/variance–expectation 条件；
6. 用 toy model 求解 fixed point 并读取 $d/m$ rate；
7. 区分 optimization curvature、statistical curvature 与 parameter identifiability；
8. 审计 low-noise classification、kernel regression、interpolation 与 deep learning claims。

## 二、先定义正确的 Excess-Loss 对象

设 risk minimizer

$$
f^*\in\arg\min_{f\in\mathcal F}P\ell_f,
\qquad
\ell_f(z)=\ell(f,z).
$$

定义 excess loss

$$
g_f(z)=\ell_f(z)-\ell_{f^*}(z).
$$

构成 class

$$
\mathcal G=\{g_f:f\in\mathcal F\}.
$$

对每个 $f$，population mean 是 excess risk：

$$
Pg_f
=P\ell_f-P\ell_{f^*}
\ge0.
$$

但 $g_f(z)$ **不必逐点非负**。某个 $f$ 可在部分样本上比 $f^*$ loss 更小，只是总体平均不能更低。

### 2.1 为什么不能只局部化 parameter ball

参数距离

$$
\|\theta-\theta^*\|
$$

只有在以下条件下才可转成 risk/function distance：

- parameterization 可识别或已 quotient symmetries；
- loss 有 curvature；
- feature/design covariance 不退化；
- norm 与 prediction geometry 相容。

深网中的 permutation、positive rescaling 与 flat directions 使“参数很远”仍可能是同一函数。所以 local empirical-process theory优先局部化 loss/function geometry。

## 三、为什么 Global Bound 可能过松

全局 complexity 是

$$
\mathfrak R_m(\mathcal G)
=\mathbb E_{S,\sigma}
\sup_{g\in\mathcal G}
\frac1m\sum_i\sigma_i g(Z_i).
$$

它必须允许 supremum 选择任意 $g$，包括：

- excess risk 很大；
- variance 很大；
- 与 ERM 最终输出不可能同时竞争的函数；
- 只在 class 远端增加的高振荡函数。

global uniform convergence 常给出

$$
P g_{\widehat f}
\lesssim\mathfrak R_m(\mathcal G)
+\sqrt{\frac{\log(1/\delta)}m},
$$

典型为 $m^{-1/2}$。但一旦已知 candidate 的 excess risk 很小，它所在的 loss slice 可能简单得多。

## 四、Population Local Complexity

一种常见局部化方式使用二阶矩：

$$
\mathcal G(r)
=\{g\in\mathcal G:Pg^2\le r\}.
$$

定义

$$
\mathfrak R_m(\mathcal G(r))
=\mathbb E_{S,\sigma}
\sup_{g\in\mathcal G(r)}
\frac1m\sum_i\sigma_i g(Z_i).
$$

随 $r$ 减小，允许函数减少，因此 complexity 不增。

### 4.1 Star Hull

定义

$$
\operatorname{star}(\mathcal G,0)
=\{\alpha g:g\in\mathcal G,\ 0\le\alpha\le1\}.
$$

star hull 允许把任意函数沿着射线缩向 0。它带来关键 scaling：若一个远端函数 $g$ 的二阶矩大于 $r$，可缩放到局部边界，并在 weighted/peeling proof 中代表该方向。

> [!important] 为什么不是随意扩大 class
> star hull 确实可能增大 class，但它制造了 radius scaling regularity，使一个 fixed point 能同时控制多个 shells。付出可控 enlargement，换取 uniform proof 结构。

## 五、图解：局部切片、Fixed Point 与 Rate

先回答：**图中 $r^*$ 左侧和右侧，$\psi(r)$ 与 $r$ 的大小关系分别是什么？**

![[00-知识库管理/_assets/figures/learning-theory/fig-local-rademacher-fixed-point-v2.svg|900]]

> [!figure] 图 20.4.7｜Global class、sub-root fixed point 与 fast-rate 条件
> 左栏显示围绕 risk optimum 的局部 loss geometry；中栏以 $\psi(r)$ 与对角线交点定义自洽 radius；右栏强调 $m^{-1}$ 型改善还需 Bernstein/curvature。来源：依据 local Rademacher 主线独立绘制；确定性 SVG，由 [[plot_rademacher_advanced_v2.py]] 生成。

**怎样读图。** 如果在 radius $r$ 内的随机波动上界 $\psi(r)$ 已小于 $r$，该 radius 足以“容纳自己的 estimation error”；固定点是最小稳定尺度的代表。

**适用边界（图没有证明什么）。** 图没有说所有问题都有唯一 risk minimizer、所有 fixed point 可计算、任意 nonconvex ERM 都达到 global optimum，或 real deep networks 自动满足 Bernstein condition。

## 六、Sub-Root Function

函数 $\psi:[0,\infty)\to[0,\infty)$ 称为 sub-root，如果：

1. $\psi$ nondecreasing；
2. $r\mapsto\psi(r)/\sqrt r$ 在 $r>0$ 上 nonincreasing。

第二条表示 $\psi$ 的增长不快于 $\sqrt r$ 型。

### 6.1 Fixed Point

在非退化条件下，sub-root function 有唯一 positive fixed point $r^*$：

$$
\psi(r^*)=r^*.
$$

对 $r\ge r^*$，由 sub-root 性：

$$
\frac{\psi(r)}{\sqrt r}
\le
\frac{\psi(r^*)}{\sqrt{r^*}}
=\sqrt{r^*},
$$

所以

$$
\psi(r)
\le\sqrt{rr^*}
\le r.
$$

最后一步因 $r\ge r^*$。因此一旦 radius 超过 fixed point，local fluctuation 不再大于 radius 本身。

## 七、Toy Fixed Point：从 $\sqrt{rd/m}$ 到 $d/m$

假设某个 $d$-dimensional local class 满足

$$
\psi(r)
=c\sqrt{\frac{rd}{m}}
+c'\frac dm.
$$

忽略常数看 fixed point：

$$
r
\asymp\sqrt{\frac{rd}{m}}+\frac dm.
$$

令 $t=\sqrt r$、$a=c\sqrt{d/m}$、$b=c'd/m$，则

$$
t^2=at+b.
$$

positive root 是

$$
t
=\frac{a+\sqrt{a^2+4b}}2,
\qquad
r^*=t^2.
$$

由于 $a^2\asymp d/m$ 且 $b\asymp d/m$，得到

$$
\boxed{r^*\asymp\frac dm.}
$$

这解释了快率机制：local complexity 本身仍含 square root，但 radius 同时出现在左右两边，fixed point 把平方根自洽闭合。

## 八、Bernstein / Variance–Expectation 条件

local second moment 必须与我们想控制的 mean excess risk 连接。一类条件是：存在 $B>0$、$\beta\in[0,1]$，使所有 $g\in\mathcal G$ 满足

$$
\boxed{
Pg^2
\le B(Pg)^\beta.}
$$

有时写 variance $\operatorname{Var}(g)$ 而非 second moment；若 $g$ bounded，两者可在适当常数下转换。

### 8.1 $\beta$ 的含义

- $\beta=0$：二阶波动只有常数 bound，通常对应 slow-rate regime；
- $0<\beta<1$：intermediate rate；
- $\beta=1$：variance 与 mean 线性相连，是典型 fast-rate 条件。

在 bounded $0$-$1$ excess-loss 或 low-noise classification 中可出现 Bernstein-like behavior；在 strongly convex regression 中，curvature 也可把 prediction distance 与 excess risk 相连。

> [!warning] Strong convexity 不等于自动 Bernstein
> optimization objective 对参数 strong convex，还需 data distribution/design 把 parameter curvature 传到 population prediction loss；regularizer 产生的 curvature 也可能不等于 task excess-risk curvature。

## 九、Peeling：让局部结论对整个类同时成立

如果只在固定 radius $r$ 上证明 concentration，ERM 的实际 radius 又未知，会产生 circularity。peeling 把 class 分层：

$$
\mathcal G_k
=\{g:2^{k-1}r<Pg^2\le2^kr\}.
$$

对每个 shell 分配 failure probability，例如

$$
\delta_k\propto\frac\delta{(k+1)^2},
$$

再 union bound。每个 shell 用对应 local complexity，最后 fixed point 同时支配所有层。

另一种等价 proof language 是对 $g$ 除以 weight

$$
w(g)\asymp Pg\vee r
$$

并对 weighted class 使用 uniform concentration。两者都在解决同一问题：**radius 是未知且由 estimator 自适应选择的。**

## 十、Schematic Excess-Risk Bound

在 bounded loss、适当 star-shaped excess class、sub-root upper envelope、Bernstein condition 与 ERM/approximate ERM 条件下，典型结论形如

$$
\boxed{
P\ell_{\widehat f}-P\ell_{f^*}
\lesssim
r^*
+\frac{b\log(1/\delta)}m
+\text{optimization error}.}
$$

更一般 oracle inequality 形如

$$
P\ell_{\widehat f}
\lesssim
\inf_{f\in\mathcal F}P\ell_f
+r^*
+\frac{b\log(1/\delta)}m.
$$

$\lesssim$ 隐藏的常数依赖 theorem 的 $B,\beta$、range、star hull 与 ERM approximation。此处用于理解机制，具体应用必须引用完整版本。

## 十一、Population Radius 为什么不可直接计算

$Pg^2$ 与 $Pg$ 依赖未知 $P$。实际 data-dependent certificate 常用 empirical slice：

$$
\widehat{\mathcal G}(r)
=\{g:P_mg^2\le r\},
$$

并计算

$$
\widehat{\mathfrak R}_S(\widehat{\mathcal G}(r)).
$$

但不能把 $P$ 机械换成 $P_m$：

- 真正的 low-variance functions 可能因随机波动被排除；
- empirical-low-variance functions 可能 population variance 很大；
- slice 本身依赖 sample；
- 用同一 signs approximate supremum 又有 Monte Carlo/optimization error。

正式结果通过 inflated empirical radius、star hull、comparison theorem 与额外 confidence constants 解决。课程不把 naive plug-in 称为 certificate。

## 十二、例子一：Strongly Convex Squared-Loss Regression

考虑 fixed features、population covariance 良好条件下的 linear regression：

$$
f_w(x)=\langle w,x\rangle,
\qquad
\ell_w(x,y)=(y-\langle w,x\rangle)^2.
$$

若 $w^*$ 是 population minimizer，适当 noise orthogonality 下 excess risk 为

$$
P(\ell_w-\ell_{w^*})
=P\langle w-w^*,X\rangle^2.
$$

这本身就是 prediction $L_2(P)$ distance squared。半径 $r$ 的 local set 对应 ellipsoid，而不是整个 weight ball。其 local complexity 可按 covariance effective dimension 缩小，并在良好 noise/tail 条件下产生约 $d/m$ excess-risk rate。

边界包括：

- heavy-tailed $X,Y$ 使 concentration 失效；
- covariance singular 时 parameter 不可识别，但 prediction risk仍可能可控；
- overparameterized/interpolating 时需 minimum-norm bias 或 effective rank 工具。

## 十三、例子二：Low-Noise Classification

若 $\eta(x)=P(Y=1\mid X=x)$ 很少接近 $1/2$，Bayes decision boundary 周围 probability mass 小。Tsybakov/Massart-type low-noise assumptions 可把 disagreement probability、variance 与 excess classification risk 连接，从而允许 fast rates。

但“训练数据容易分类”不是 low-noise condition：

- 它可能来自过强模型记忆；
- empirical margin 大不保证 population conditional probability 远离 $1/2$；
- label noise 与 covariate shift 会改变条件。

## 十四、AI 应用接口

### 14.1 Kernel/RKHS

localization 可结合 Gram spectrum：低 risk radius 下，有效 eigen-directions 少于全 RKHS ball。fixed point 往往与 effective dimension

$$
\sum_j\frac{\lambda_j}{\lambda_j+\lambda}
$$

相联系。但 kernel 与 $\lambda$ 的 data-adaptive selection 要纳入模型选择。

### 14.2 Interpolation

训练 loss 为 0 只说明 estimator 位于 empirical zero-loss set；这个 set 可能：

- 在 population metric 下很小；
- 也可能包含大量任意振荡 functions。

local theory 是否有用取决于 implicit bias、norm、data geometry 与 noise，不是“插值所以局部”。

### 14.3 Fine-Tuning 与 Tangent Approximation

如果能证明 fine-tuning 始终位于预训练模型周围的 function/Jacobian neighborhood，local complexity 可能比全网络类小。但仅观察 parameter displacement 小不够；还需 uniform linearization error、Jacobian norm、sample independence 与 loss curvature。

### 14.4 Post-Hoc Basin Claim

训练后画出一条二维 loss landscape 并发现“平坦 basin”，不能直接当作 local Rademacher bound。二者分别是：

- 低维切片上的 parameter loss visualization；
- loss-function class 在随机 sample/sign process 下的 uniform complexity。

## 十五、常见误区

> [!danger] 误区 1：局部化就是只看训练误差小的模型
> 训练误差筛选是 sample-adaptive；必须由 empirical local theorem 处理 selection 与 radius inflation。

> [!danger] 误区 2：local complexity 小就必有 $m^{-1}$
> 还需 variance–mean/Bernstein、curvature 或 low-noise 条件。

> [!danger] 误区 3：fixed point 是优化算法的收敛点
> 它是 statistical error scale，不是 gradient descent parameter fixed point。

> [!danger] 误区 4：参数附近等于函数附近
> 非识别、rescaling 与 data-null directions 会破坏对应。

> [!danger] 误区 5：写出 $r^*$ 就已可计算
> $\psi$ 可能依赖未知 $P$、supremum optimization 与 constants；data-dependent upper estimator 仍需证明与数值验收。

## 十六、本节最小闭环

应用 local theory 前，应完成：

1. 定义 $f^*$ 与 excess-loss class $\mathcal G$；
2. 选择 localization functional：$Pg^2$、variance、excess risk 或 metric radius；
3. 说明是否使用 star hull；
4. 给出 local Rademacher upper envelope $\psi(r)$；
5. 验证 sub-root 性并求 fixed point；
6. 验证 Bernstein/curvature/noise condition；
7. 用 peeling/weighting 得到 uniform statement；
8. 若用 empirical radius，引用相应 comparison theorem；
9. 把 optimization error 与 statistical error 分账；
10. 实际判断 bound 是否 nonvacuous。

## 十七、连接

- 前置：[[覆盖数、Metric Entropy 与 Chaining 入口]]、[[Rademacher 复杂度与经验复杂度]]；
- 下一节：[[Fat-Shattering、回归与 Lipschitz 风险]]；
- 算法角度：[[正则化 ERM 的稳定性]]；
- 模型：[[核岭回归与 Gaussian Process 接口]]；
- 深网边界：[[神经网络容量与 Norm-Based Bound]]；
- 训练：[[习题 - 局部 Rademacher 复杂度与快收敛率]]；
- 解答：[[解答 - 局部 Rademacher 复杂度与快收敛率]]。
