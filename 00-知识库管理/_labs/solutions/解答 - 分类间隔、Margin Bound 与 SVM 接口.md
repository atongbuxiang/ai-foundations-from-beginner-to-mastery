---
type: solution
status: draft
area: [learning-theory/margin, classification/svm]
topic: "[[习题 - 分类间隔、Margin Bound 与 SVM 接口]]"
prerequisites: ["[[分类间隔、Margin Bound 与 SVM 接口]]"]
related: ["[[支持向量机、最大间隔与核方法]]", "[[覆盖数、Metric Entropy 与 Chaining 入口]]"]
created: 2026-08-23
updated: 2026-08-23
---

# 解答 - 分类间隔、Margin Bound 与 SVM 接口

> [!warning] 约定
> tie 事件 $Yf(X)=0$ 计为分类错误；Rademacher complexity 使用 signed $1/m$ convention，contraction 使用正文 factor-$2$ 安全版本。

## A. 识别与复述

### LT-MAR-A01

Binary functional margin：

$$
\rho_f(x,y)=yf(x).
$$

Affine-linear geometric margin：

$$
\rho^{\rm geo}_{w,b}(x,y)
=\frac{y(\langle w,x\rangle+b)}{\|w\|_2},
\qquad w\ne0.
$$

当 $(w,b)\mapsto(cw,cb)$、$c>0$：functional margin 乘 $c$；分母也乘 $c$，所以 geometric margin 不变。

### LT-MAR-A02

$$
\phi_\gamma(u)=
\begin{cases}
1,&u\le0,\\
1-u/\gamma,&0<u<\gamma,\\
0,&u\ge\gamma.
\end{cases}
$$

逐点 sandwich 为

$$
\mathbf1\{u\le0\}
\le\phi_\gamma(u)
\le\mathbf1\{u\le\gamma\}.
$$

### LT-MAR-A03

- margin generalization：由 sample margin distribution、class complexity、sampling 与 confidence 控制 population classification error；
- SVM optimization：在给定 features/class 与 regularization 下求一个 convex objective 的 minimizer；
- surrogate calibration：surrogate excess risk 是否及如何推出 $0$-$1$ excess risk。

三者分别是统计、优化与 decision-theoretic 接口，不能相互替代。

## B. 手算与数值判断

### LT-MAR-B01

margins 为

$$
(-0.4,0.1,0.3,0.8,1.2).
$$

误分类按 $\rho\le0$：只有 $-0.4$，所以 training error 为

$$
\frac15=0.2.
$$

$\gamma=0.5$ 时，$\rho\le0.5$ 的有前三个，所以低 margin 比例为

$$
\frac35=0.6.
$$

ramp values：

$$
1,quad1-0.1/0.5=0.8,quad1-0.3/0.5=0.4,quad0,quad0.
$$

平均 ramp loss：

$$
\frac{1+0.8+0.4}{5}=\boxed{0.44}.
$$

它位于 training error 0.2 与低 margin proportion 0.6 之间。

### LT-MAR-B02

$$
\langle w,x\rangle+b
=3\cdot2+4\cdot1-1=9.
$$

$y=+1$，functional margin 是 9。$\|w\|_2=5$，geometric margin 是

$$
\frac95=1.8.
$$

整体乘 10 后，functional margin 为 90，weight norm 为 50，geometric margin仍为

$$
\frac{90}{50}=1.8.
$$

### LT-MAR-B03

complexity term：

$$
\frac4\gamma\widehat{\mathfrak R}
=\frac4{0.5}(0.02)=0.16.
$$

confidence term：

$$
3\sqrt{\frac{\log(2/0.05)}{2(1000)}}
=3\sqrt{\frac{\log40}{2000}}
\approx3(0.04295)
\approx0.1288.
$$

所以

$$
R_{01}(f)
\le0.08+0.16+0.1288
=\boxed{0.3688}.
$$

该值低于 1，因而 nontrivial，但仍显著高于经验低 margin rate。

## C. 推导与证明

### LT-MAR-C01

对 $u\le0$，ramp 为 1，与 error indicator相等；对 $0<u<\gamma$，error indicator 为 0、ramp 在 $(0,1)$、low-margin indicator 为 1；对 $u\ge\gamma$，ramp 为 0，并不超过 low-margin indicator。故 sandwich 成立。

ramp 连续分段线性，三段 slope 分别为 $0,-1/\gamma,0$。任意两点间的 secant slope 绝对值不超过最大局部 slope，故

$$
|\phi_\gamma(u)-\phi_\gamma(v)|
\le\frac1\gamma|u-v|.
$$

也可按两点是否跨越 breakpoints 分段用 triangle inequality 证明。

### LT-MAR-C02

定义

$$
\mathcal M=\{(x,y)\mapsto yf(x):f\in\mathcal F\}.
$$

在固定 sample 上，

$$
\begin{aligned}
\widehat{\mathfrak R}_S(\mathcal M)
&=\mathbb E_\sigma\sup_f\frac1m\sum_i\sigma_i y_i f(X_i)\\
&=\mathbb E_{\tilde\sigma}\sup_f\frac1m\sum_i\tilde\sigma_i f(X_i)\\
&=\widehat{\mathfrak R}_{S_X}(\mathcal F),
\end{aligned}
$$

因为 $\tilde\sigma_i=\sigma_i y_i$ 仍是 iid Rademacher signs。

对 $[0,1]$-valued ramp-loss class，risk theorem 给出

$$
P\phi_\gamma(yf(x))
\le P_m\phi_\gamma(yf(x))
+2\widehat{\mathfrak R}_S(\phi_\gamma\circ\mathcal M)
+3\sqrt{\frac{\log(2/\delta)}{2m}}.
$$

中心化 ramp 后，factor-$2$ contraction 与 $L=1/\gamma$ 给出

$$
\widehat{\mathfrak R}_S(\phi_\gamma\circ\mathcal M)
\le\frac2\gamma\widehat{\mathfrak R}_{S_X}(\mathcal F).
$$

最后用两端 sandwich：

$$
\begin{aligned}
P(Yf\le0)
&\le P\phi_\gamma(Yf)\\
&\le P_m\phi_\gamma(Yf)
+\frac4\gamma\widehat{\mathfrak R}_{S_X}(\mathcal F)
+3\sqrt{\frac{\log(2/\delta)}{2m}}\\
&\le P_m(Yf\le\gamma)
+\frac4\gamma\widehat{\mathfrak R}_{S_X}(\mathcal F)
+3\sqrt{\frac{\log(2/\delta)}{2m}}.
\end{aligned}
$$

### LT-MAR-C03

对可分数据，最大化

$$
\min_i\frac{y_i(\langle w,x_i\rangle+b)}{\|w\|}
$$

有正尺度不识别性。选择规范化

$$
\min_i y_i(\langle w,x_i\rangle+b)=1,
$$

目标变成最大化 $1/\|w\|$，即最小化 $\frac12\|w\|^2$，约束为每个 functional margin至少 1。这得到 hard-margin primal。

不可分时加 $\xi_i\ge0$：

$$
y_if_i\ge1-\xi_i.
$$

固定 $(w,b)$ 后，为使 $C\sum\xi_i$ 最小，

$$
\xi_i=\max\{0,1-y_if_i\}.
$$

代回得到

$$
\min_{w,b}\frac12\|w\|^2+C\sum_i(1-y_if_i)_+.
$$

## D. 边界、反例与纠错

### LT-MAR-D01

取五个样本。分类器 A 的 margins：

$$
(0.1,1,1,1,1),
$$

分类器 B 的 margins：

$$
(0.1,0.11,0.12,0.13,4).
$$

二者 training error 都为 0，minimum margin 都是 0.1。但在 $\gamma=0.5$ 时，A 的低 margin rate 是 $1/5$，B 是 $4/5$。minimum 无法描述 margin tail。

### LT-MAR-D02

fixed-$\gamma$ theorem 的 probability event 只保证预先固定的一个阈值。若对无穷多个 $\gamma$ 看完数据后挑最小 bound，所选 $\gamma$ 与 sample 耦合，原事件不保证同时成立。

若预声明 finite grid $\Gamma$、$|\Gamma|=K$，对每个阈值使用 $\delta/K$，union bound 后以至少 $1-\delta$ 概率所有网格 bound 同时成立。confidence term改为

$$
3\sqrt{\frac{\log(2K/\delta)}{2m}}.
$$

此时可合法取网格上的最小值。

### LT-MAR-D03

logits 乘 100 使每个 functional margin 与候选 $\gamma$ 都乘 100。若 class radius/norm $B$ 也乘 100，complexity penalty 的关键比值

$$
\frac{B}{\gamma}
$$

不变。若固定 $\gamma$ 不变，经验低 margin rate可能下降，但 $\widehat{\mathfrak R}(100\mathcal F)=100\widehat{\mathfrak R}(\mathcal F)$，complexity 同时放大。只报 margin 变大是 scale manipulation。

## E. AI 迁移

### LT-MAR-E01

记录表至少包括：

1. encoder id/version 与是否独立于 probe sample；
2. sample unit、$m$、iid/依赖假设；
3. feature norm $R$ 或 empirical energy；
4. head norm $B$ 与 bias bound；
5. 每个样本 signed margin、margin CDF/quantiles；
6. 预声明 $\gamma$ grid；
7. empirical low-margin rate；
8. complexity convention 与数值；
9. confidence $\delta$ 及多阈值/超参数选择修正；
10. binary/multiclass loss 与 calibration statement。

### LT-MAR-E02

multiclass margin：

$$
\rho_f(x,y)=f_y(x)-\max_{k\ne y}f_k(x).
$$

binary scalar contraction 不足，因为需要替换：

1. scalar score class → vector-valued logit class；
2. scalar Lipschitz metric → 指定 $\ell_2/\ell_\infty$ 等 vector norm 与 dual geometry；
3. binary complexity → vector contraction/multiclass dimension，可能显式依赖类别数 $K$。

max 还耦合所有非真类坐标，不能对每类独立取 supremum 后相加。

### LT-MAR-E03

由 Lipschitz 性，任意 $\|\Delta\|\le\varepsilon$：

$$
Yf(x+\Delta)
\ge Yf(x)-|f(x+\Delta)-f(x)|
\ge Yf(x)-L_x\varepsilon>0.
$$

所以预测符号不翻转。这只是单点 sufficient condition。robust population bound 还要控制

$$
P\left(\exists\|\Delta\|\le\varepsilon:
Yf(X+\Delta)\le0\right),
$$

需要 robust loss class 的 uniform complexity、真实 $L_x$ certificate、attack/perturbation set、sampling law 与 confidence。
