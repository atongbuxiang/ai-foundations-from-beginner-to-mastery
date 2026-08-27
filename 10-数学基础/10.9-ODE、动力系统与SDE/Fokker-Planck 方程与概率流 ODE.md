---
type: concept
status: draft
area: [math/probability, math/stochastic-processes, math/sde, math/pde, ai/generative-modeling]
aliases: [Fokker–Planck equation, Kolmogorov forward equation, 概率流常微分方程, probability flow ODE]
prerequisites: ["[[Itô 引理与随机微分方程]]", "[[连续性方程与守恒律]]", "[[流映射、Liouville 公式与连续正规化流]]", "[[协方差、相关性与条件期望]]", "[[多元函数、偏导数与方向导数]]", "[[梯度、方向导数与最陡方向]]"]
related: ["[[ODE、动力系统与 SDE MOC]]", "[[时间反演、score 与扩散生成动力学]]", "[[随机过程、Brownian 运动与二次变差]]", "[[实验 - Fokker-Planck、概率流与score误差审计]]"]
sources: ["MIT-8.592J-2011-Kolmogorov-Equations", "MIT-18.642-2024-Stochastic-Processes-II", "Pavliotis-Stochastic-Processes-Applications", "Risken-Fokker-Planck", "Oksendal-Stochastic-Differential-Equations", "Song-et-al-2021-Score-SDE", "Albergo-et-al-2024-Stochastic-Interpolants", "Su-3762-Stochastic-Differential-Equation", "Su-9209-Diffusion-SDE", "Su-9228-Probability-Flow-ODE", "Su-9280-Diffusion-ODE"]
created: 2026-08-19
updated: 2026-08-23
---

# Fokker-Planck 方程与概率流 ODE

> [!abstract] 本章主问题
> 对 Itô SDE
> $$
> dX_t=a(t,X_t)\,dt+B(t,X_t)\,dW_t,
> \qquad
> D=BB^\top,
> $$
> generator 先描述 test function 的期望怎样变化：
> $$
> \frac d{dt}\mathbb E[\varphi(X_t)]
> =
> \mathbb E[(\mathcal L_t\varphi)(X_t)].
> $$
> 将导数通过分部积分转移到 density $p_t$，得到 Fokker–Planck：
> $$
> \partial_t p
> =
> -\nabla\cdot(ap)
> +\frac12\sum_{i,j}\partial_{ij}(D_{ij}p).
> $$
> 它又可写成 continuity equation $\partial_tp=-\nabla\cdot(vp)$。一个 canonical probability-flow velocity 是
> $$
> v
> =
> a-\frac1{2p}\nabla\cdot(Dp).
> $$
> 当 $D=g(t)^2I$ 时，
> $$
> v=a-\frac12g(t)^2\nabla\log p_t.
> $$
> 该 ODE 在适当条件下与 SDE 共享每个时刻的 marginal density，却不共享 transition law、quadratic variation 或 sample paths。

> [!important] 与相邻章节的分工
> [[Itô 引理与随机微分方程]]负责 stochastic integral、generator 与 SDE 解；[[连续性方程与守恒律]]负责 deterministic density transport。本章用 adjoint 把二者接起来，并推导 probability-flow ODE。[[时间反演、score 与扩散生成动力学]]才处理 backward filtration、reverse-time SDE、score training 与从 prior 回到 data 的完整生成链。

先用下图回答一个视觉问题：**Itô generator 怎样经 adjoint 变成 density PDE，扩散 current 如何改写为概率流速度，而“同 marginals”究竟没有保留什么？**

![[00-知识库管理/_assets/figures/dynamics/fig-fokker-planck-probability-flow-v2.svg|880]]

> [!figure] 图 10.9.11a｜Generator adjoint、probability current 与同边缘路径差异
> A 从 Itô formula 得到 generator identity $d\mathbb E\varphi(X_t)/dt=\mathbb E[\mathcal L_t\varphi(X_t)]$，再以 test functions 和 boundary terms 转成 $\partial_tp=\mathcal L_t^*p$；B 将 Fokker–Planck 写为 $\partial_tp=-\nabla\cdot J$，由 $v=J/p=a-[\nabla\cdot(Dp)]/(2p)$ 得到 canonical probability-flow velocity，并标出 state-dependent $D$ correction；C 定性对比 SDE 的 nonzero QV 与 probability-flow ODE 的 deterministic/zero-QV path。来源：独立绘制；理论接口参考 Kolmogorov generator、Fokker–Planck adjoint 与 probability-flow ODE；生成脚本：[[plot_stochastic_dynamics_v2.py]]；定性路径示意，无随机种子。

**怎样读图。** A 先明确 $\mathcal L$ 作用在 observables，$\mathcal L^*$ 作用在 density，分部积分的边界项决定 PDE domain；B 再把 drift/diffusion current 合并成 $J=vp$，在 $p>0$ 区域定义 velocity，isotropic spatially constant diffusion 才简化为 $a-\frac12g^2\nabla\log p$；C 最后只比较 one-time marginals，不能把它外推到 transition kernel、cross-time covariance、QV 或 hitting-time law。

**适用边界（图没有证明什么）。** 图省略退化 diffusion、弱 density、boundary singularities 与 probability-current nonuniqueness 的技术条件。State-dependent $D$ 不能漏掉 product-rule/$\nabla\cdot D$ 项；$p=0$ 处的 velocity 需要谨慎定义。Exact same-marginal theorem 依赖 exact score/coefficients 与 well-posed PDE/ODE，不包含 learned score 或 finite-step solver error。

## 学习目标

完成本章后，应能：

1. 区分 transition kernel、Markov semigroup、generator 与 marginal density；
2. 从 Itô formula 推出 Dynkin formula；
3. 写出 backward Kolmogorov equation 及 terminal condition；
4. 用 test functions 与两次分部积分推导 Fokker–Planck 弱形式；
5. 写出多维 state-dependent diffusion 的正确坐标公式；
6. 把 Fokker–Planck 写成概率 current 的守恒律；
7. 区分 no-flux、absorbing、periodic 与 whole-space boundary contract；
8. 证明 Brownian、constant drift 与 OU 的 density 满足对应 PDE；
9. 求一维 zero-current stationary density；
10. 推导 overdamped Langevin 的 Gibbs stationary law；
11. 从 diffusion current 构造 canonical probability-flow velocity；
12. 解释 state-dependent $D$ 中的 $\nabla\cdot D$ correction；
13. 证明 probability-flow ODE 与 SDE 的 one-time marginals 相同的条件链；
14. 说明同 marginals 不等于同 path law；
15. 分离 score approximation、density/model 与 ODE solver error。

> [!question] 初学者读完必须能回答
> 1. Markov semigroup、generator、transition kernel 与 marginal density 有何区别？
> 2. Itô/Dynkin formula 怎样给 test-function 期望演化？
> 3. 两次分部积分怎样产生 Fokker–Planck 的 diffusion term？
> 4. Boundary condition 为什么是 adjoint PDE 的组成部分？
> 5. Probability current $J$ 与 velocity $v=J/p$ 怎样构造？
> 6. State-dependent $D$ 时为什么必须包含 $\nabla\cdot D$ correction？
> 7. Probability-flow ODE 与 SDE 共享哪些 marginals，又不共享哪些 path statistics？

## 零、从单条随机路径升级到 law evolution

DYN-10 回答了：

$$
\text{给定一条 Brownian realization，}X_t\text{ 怎样满足积分方程？}
$$

本章改问：

$$
\text{当 }\omega\text{ 遍历样本空间时，}X_t\text{ 的分布怎样变化？}
$$

四层对象不能混合：

| 层 | 对象 | 回答的问题 |
|---|---|---|
| sample path | $t\mapsto X_t(\omega)$ | 一次随机实验怎样运动？ |
| transition law | $P_{s,t}(x,dy)$ | 已知 $X_s=x$，未来怎样分布？ |
| marginal law | $\mu_t=\mathcal L(X_t)$ | 固定时刻总体怎样分布？ |
| density | $p_t=d\mu_t/dx$ | 若绝对连续，概率质量怎样按空间表示？ |

Fokker–Planck 只直接描述 marginal density。它不恢复完整 multi-time law；若 process 不是 Markov，仅知道所有 $p_t$ 更远远不够。

## 一、Transition kernel 与 Markov semigroup

对 time-homogeneous Markov process，transition kernel 写为

$$
P_t(x,A)
=
\mathbb P(X_t\in A\mid X_0=x).
$$

它作用在 bounded measurable test function 上：

$$
(P_t\varphi)(x)
=
\mathbb E_x[\varphi(X_t)].
$$

Chapman–Kolmogorov 对应 semigroup law：

$$
P_{t+s}=P_tP_s.
$$

若 initial law 是 $\mu_0$，则

$$
\mu_t(A)
=\int P_t(x,A)\,\mu_0(dx).
$$

若有 transition density $p(t,y\mid x)$：

$$
(P_t\varphi)(x)
=
\int\varphi(y)p(t,y\mid x)\,dy.
$$

> [!warning] 两个变量承担不同角色
> 在 $p(t,y\mid x)$ 中，$x$ 是起点变量，$y$ 是终点变量。Backward equation 对 $x$ 作用；forward equation 对 $y$ 作用。把它们都写成 $x$ 是最常见的符号混乱来源。

## 二、Generator 是 semigroup 的无穷小导数

对适当 domain 中的 $\varphi$，定义

$$
(\mathcal L\varphi)(x)
:=
\lim_{h\downarrow0}
\frac{(P_h\varphi)(x)-\varphi(x)}h.
$$

对 Itô diffusion

$$
dX_t=a(X_t)dt+B(X_t)dW_t,
\qquad
D(x)=B(x)B(x)^\top,
$$

Itô formula 给

$$
\boxed{
\mathcal L\varphi
=
a^\top\nabla\varphi
+\frac12\operatorname{tr}
\left(D\nabla^2\varphi\right)
}.
$$

Generator 作用在 observable $\varphi$ 上，不直接作用在 density 上。它的 domain、boundary conditions 与函数空间是 operator 的一部分；只写 differential expression 还不是完整 operator。

### 2.1 Dynkin formula

Itô formula：

$$
\varphi(X_t)-\varphi(X_0)
=
\int_0^t(\mathcal L\varphi)(X_s)ds
+\int_0^t\nabla\varphi(X_s)^\top B(X_s)dW_s.
$$

在使 stochastic integral 期望为0的可积条件下：

$$
\boxed{
\mathbb E[\varphi(X_t)]
-
\mathbb E[\varphi(X_0)]
=
\int_0^t
\mathbb E[(\mathcal L\varphi)(X_s)]ds
}.
$$

若可微：

$$
\frac d{dt}\mathbb E[\varphi(X_t)]
=
\mathbb E[(\mathcal L\varphi)(X_t)].
$$

这是 pathwise Itô calculus 与 density PDE 之间的桥。

## 三、Backward Kolmogorov equation

固定 terminal time $T$ 与 payoff $\psi$，定义

$$
u(t,x)
=
\mathbb E[\psi(X_T)\mid X_t=x].
$$

Markov property 给

$$
u(t,X_t)
=
\mathbb E[\psi(X_T)\mid\mathcal F_t],
$$

所以该过程是 martingale。对 $u(t,X_t)$ 用 Itô formula，drift 必须为0：

$$
\boxed{
\partial_tu(t,x)
+\mathcal L_tu(t,x)
=0,
\qquad
u(T,x)=\psi(x)
}.
$$

这是 backward Kolmogorov equation。它向较早时间传播“从当前状态出发的未来期望”。

若 time-homogeneous，$u(t,x)=P_{T-t}\psi(x)$。等价地，

$$
\frac d{dt}P_t\psi
=
\mathcal LP_t\psi
$$

在适当 domain 中成立。

> [!note] Backward 不等于 reverse-time SDE
> Backward Kolmogorov 是对起点变量/terminal payoff 的 PDE。DYN-12 的 reverse-time SDE 是一个以反向 filtration 驱动的新随机过程；二者不能仅凭“backward”一词等同。

## 四、Fokker–Planck 的弱形式

设 $X_t$ 有 density $p(t,x)$。Dynkin differential 变为

$$
\frac d{dt}
\int_{\mathbb R^d}\varphi(x)p(t,x)\,dx
=
\int_{\mathbb R^d}
(\mathcal L_t\varphi)(x)p(t,x)\,dx.
$$

定义 formal adjoint $\mathcal L_t^\ast$：

$$
\int(\mathcal L_t\varphi)p\,dx
=
\int\varphi(\mathcal L_t^\ast p)\,dx,
$$

前提是 boundary terms 按所声明的条件消失或被正确保留。于是

$$
\int
\varphi(x)
\left[
\partial_tp-\mathcal L_t^\ast p
\right]dx
=0.
$$

对所有 compactly supported smooth $\varphi$ 成立，得到 distributional/weak equation：

$$
\boxed{
\partial_tp=\mathcal L_t^\ast p
}.
$$

这个 test-function identity 比“假设 $p$ 很光滑再逐点相等”更基础。

## 五、两次分部积分得到多维公式

Generator：

$$
\mathcal L_t\varphi
=
\sum_i a_i\partial_i\varphi
+\frac12\sum_{i,j}D_{ij}\partial_{ij}\varphi.
$$

### 5.1 Drift 项

一次分部积分：

$$
\int a_i(\partial_i\varphi)p\,dx
=
-\int\varphi\,\partial_i(a_ip)\,dx
$$

加上 boundary term。whole space 下常要求衰减足够快；bounded domain 则必须指定边界。

### 5.2 Diffusion 项

对每个 $i,j$ 做两次分部积分：

$$
\int D_{ij}p\,\partial_{ij}\varphi\,dx
=
\int\varphi\,\partial_{ij}(D_{ij}p)\,dx
$$

同样忽略或处理 boundary terms。

所以

$$
\boxed{
\partial_t p
=
-\sum_{i=1}^d\partial_i(a_i p)
+\frac12
\sum_{i=1}^d\sum_{j=1}^d
\partial_i\partial_j(D_{ij}p)
}.
$$

这就是 Kolmogorov forward/Fokker–Planck equation。

> [!warning] State-dependent diffusion 的 product rule
> 正确项是 $\partial_{ij}(D_{ij}p)$，不是无条件写成 $D_{ij}\partial_{ij}p$。后者只有 $D$ 对空间常数时才成立。

## 六、概率 current 与局部守恒

定义 row-wise divergence：

$$
[\nabla\cdot(Dp)]_i
:=
\sum_j\partial_j(D_{ij}p).
$$

定义 probability current：

$$
\boxed{
J
=
ap-\frac12\nabla\cdot(Dp)
}.
$$

则 Fokker–Planck 可写为

$$
\boxed{
\partial_tp+\nabla\cdot J=0
}.
$$

对 fixed control volume $\Omega$：

$$
\frac d{dt}\int_\Omega p\,dx
=
-\int_{\partial\Omega}J\cdot n\,dS.
$$

概率不会凭空消失；它通过 boundary flux 离开或进入。

### 6.1 四种 boundary contract

| 边界 | 条件 | 质量含义 |
|---|---|---|
| whole space | $J$ 与 $p$ 足够快衰减 | infinity flux 为0 |
| periodic | 两端/对面 flux 抵消 | 总质量守恒 |
| reflecting/no-flux | $J\cdot n=0$ | domain 内质量守恒 |
| absorbing | 常见 $p=0$ 或 killed-process 条件 | interior survival mass 可下降 |

Absorbing 情形若只看 domain 内 density，积分小于1代表尚未被吸收的 survival probability；要恢复总概率1，需加入 cemetery/absorbed mass。

## 七、一维公式与 stationary current

一维 Itô SDE：

$$
dX_t=a(X_t)dt+b(X_t)dW_t.
$$

Fokker–Planck：

$$
\partial_tp
=
-\partial_x(ap)
+\frac12\partial_{xx}(b^2p).
$$

Current：

$$
J=ap-\frac12\partial_x(b^2p).
$$

Stationary density $p_\infty$ 满足

$$
\partial_xJ_\infty=0,
$$

所以 $J_\infty$ 是常数。Stationary 不自动意味着 $J_\infty=0$；在 periodic non-equilibrium systems 中可有持续环流。

若 whole-line natural boundary 或 reflecting boundary 强制 zero current：

$$
\partial_x(b^2p_\infty)=2ap_\infty.
$$

展开并除以 $b^2p_\infty$：

$$
\partial_x\log p_\infty
=
\frac{2a}{b^2}
-\partial_x\log b^2.
$$

因此

$$
\boxed{
p_\infty(x)
\propto
\frac1{b(x)^2}
\exp\left(
\int^x\frac{2a(y)}{b(y)^2}\,dy
\right)
}
$$

前提是它可归一化且 boundary/current 条件成立。

## 八、三个可手算例子

### 8.1 Brownian motion 与 heat equation

$$
dX_t=\sigma dW_t.
$$

这里 $a=0,D=\sigma^2$：

$$
\partial_tp
=
\frac{\sigma^2}{2}\partial_{xx}p.
$$

若 $X_0=x_0$，fundamental solution 是

$$
p(t,x\mid x_0)
=
\frac1{\sqrt{2\pi\sigma^2t}}
\exp\left[
-\frac{(x-x_0)^2}{2\sigma^2t}
\right].
$$

当 $t\downarrow0$，它不是逐点变成 ordinary function $\delta_{x_0}$，而是在 distributions/weak measure 意义下趋于 Dirac mass。

### 8.2 Constant drift-diffusion

$$
dX_t=\mu dt+\sigma dW_t.
$$

PDE：

$$
\partial_tp
=
-\mu\partial_xp
+\frac{\sigma^2}{2}\partial_{xx}p.
$$

解为 translated heat kernel：

$$
X_t\sim\mathcal N(x_0+\mu t,\sigma^2t).
$$

Drift 移动 mean，diffusion 增长 variance。

### 8.3 Ornstein–Uhlenbeck

$$
dX_t=\kappa(m-X_t)dt+\sigma dW_t.
$$

PDE：

$$
\partial_tp
=
-\partial_x[\kappa(m-x)p]
+\frac{\sigma^2}{2}\partial_{xx}p.
$$

Zero-current stationary condition：

$$
\kappa(m-x)p_\infty
-\frac{\sigma^2}{2}\partial_xp_\infty
=0.
$$

所以

$$
\partial_x\log p_\infty
=
\frac{2\kappa(m-x)}{\sigma^2}.
$$

积分：

$$
p_\infty(x)
\propto
\exp\left[
-\frac{\kappa}{\sigma^2}(x-m)^2
\right],
$$

即

$$
\mathcal N\left(m,\frac{\sigma^2}{2\kappa}\right).
$$

## 九、Overdamped Langevin 与 Gibbs law

考虑

$$
dX_t
=
-\nabla U(X_t)dt
+\sqrt{\frac2\beta}\,dW_t.
$$

这里

$$
D=\frac2\beta I.
$$

Current：

$$
J
=
-p\nabla U
-\frac1\beta\nabla p.
$$

取

$$
\pi(x)=Z^{-1}e^{-\beta U(x)},
$$

则

$$
\nabla\pi=-\beta\pi\nabla U,
$$

所以 $J_\pi=0$。只要

$$
Z=\int e^{-\beta U(x)}dx<\infty
$$

且 boundary/regularity 合法，$\pi$ 是 stationary density。

> [!important] Stationary、invariant 与 convergence to equilibrium
> 验证 $\mathcal L^\ast\pi=0$ 只证明 invariant candidate。任意 initial law 是否收敛到 $\pi$、收敛速率、是否唯一，还需要 irreducibility、confinement、spectral gap、Lyapunov/minorization 等额外理论。

## 十、Forward 与 backward equation 的 adjoint 分工

对 transition density $p(s,x;t,y)$：

- backward equation 对起点 $(s,x)$ 作用：
  $$
  \partial_s p+\mathcal L_s^{(x)}p=0;
  $$
- forward equation 对终点 $(t,y)$ 作用：
  $$
  \partial_t p=(\mathcal L_t^{(y)})^\ast p.
  $$

它们表达同一个 Markov transition family 的两个观察方向。

| 方向 | 固定 | 演化 | operator |
|---|---|---|---|
| backward | terminal payoff/time | starting state/time | $\mathcal L$ |
| forward | initial law/time | terminal density/time | $\mathcal L^\ast$ |

Feynman–Kac 会把 potential/source 加入 backward PDE；first-passage probability也常由 backward equation求解。本章只建立接口，不展开完整边值问题。

## 十一、Score 是 density 的局部对数斜率

当 $p_t(x)>0$ 且可微，定义 score：

$$
s_t(x)
:=
\nabla_x\log p_t(x)
=
\frac{\nabla p_t(x)}{p_t(x)}.
$$

它不是模型参数的 gradient，也不是单样本 loss gradient，而是对 state variable $x$ 的 density gradient。

在边界衰减充分时：

$$
\mathbb E_{p_t}[s_t(X_t)]
=
\int\nabla p_t(x)dx
=0.
$$

更一般 Stein identity：

$$
\mathbb E_{p}
[
\nabla\cdot\phi(X)+\phi(X)^\top s(X)
]
=0
$$

仍依赖 boundary term 消失。

若 $p=0$、含 singular component 或只在低维 manifold 上有质量，ordinary Lebesgue score 可能不存在。加 Gaussian noise 后 $t>0$ 常得到平滑正 density，但靠近 singular endpoint 时 score 可变得很大。

## 十二、把 diffusion current 改写为 velocity

Fokker–Planck current 是

$$
J
=
ap-\frac12\nabla\cdot(Dp).
$$

只要 $p>0$，定义 canonical current velocity：

$$
\boxed{
v
:=
\frac Jp
=
a-\frac1{2p}\nabla\cdot(Dp)
}.
$$

于是

$$
\partial_tp+\nabla\cdot(vp)=0.
$$

利用 product rule：

$$
[\nabla\cdot(Dp)]_i
=
p\sum_j\partial_jD_{ij}
+\sum_jD_{ij}\partial_jp.
$$

因此

$$
\boxed{
v
=
a
-\frac12\nabla\cdot D
-\frac12D\nabla\log p
}.
$$

这里

$$
(\nabla\cdot D)_i=\sum_j\partial_jD_{ij}.
$$

> [!warning] 不能漏掉 $\nabla\cdot D$
> 只有 $D$ 对 state 不变时，它才为0。对 multiplicative/state-dependent diffusion，直接写 $a-\frac12D\,s$ 会得到错误的 density flux。

## 十三、Probability-flow ODE

一旦 $p_t$ 与 $v_t$ 已知，考虑 deterministic ODE：

$$
\boxed{
\frac{dZ_t}{dt}
=v(t,Z_t)
}.
$$

若其 flow 存在唯一，并且 initial law $Z_0\sim p_0$，则 ODE density $\rho_t$ 满足 continuity equation：

$$
\partial_t\rho+\nabla\cdot(v\rho)=0.
$$

而 SDE density $p_t$ 经上一节也满足：

$$
\partial_tp+\nabla\cdot(vp)=0.
$$

若该 PDE 在所选函数类与 boundary contract 下唯一，且

$$
\rho_0=p_0,
$$

则

$$
\boxed{
\rho_t=p_t
\quad\text{for every fixed }t
}.
$$

这就是 probability-flow ODE 的同 marginal 原理。

证明链有四个责任：

1. SDE 确有 density $p_t$；
2. $p_t>0$ 或 velocity 在零密度处有合理 extension；
3. $v$ 足够正则，使 ODE/continuity equation 定义良好；
4. continuity equation 的解在所声明类中唯一。

不能只做形式代入就自动得到 global flow theorem。

## 十四、Diffusion model 的常见特例

若

$$
dX_t=f(t,X_t)dt+g(t)dW_t,
$$

其中 $g(t)$ 是 scalar，noise isotropic，则

$$
D(t)=g(t)^2I,
\qquad
\nabla\cdot D=0.
$$

Probability-flow velocity：

$$
\boxed{
v(t,x)
=
f(t,x)
-\frac12g(t)^2
\nabla_x\log p_t(x)
}.
$$

因此 ODE 是

$$
\frac{dZ_t}{dt}
=
f(t,Z_t)
-\frac12g(t)^2s_t(Z_t).
$$

这里 score 是 population marginal score。实际模型使用 $s_\theta$：

$$
\widehat v_\theta
=
f-\frac12g^2s_\theta.
$$

这已经改变 velocity field；有限步 solver 又进一步改变 computed map。

## 十五、最清楚的同边缘反例：Brownian noising

设

$$
X_0\sim\mathcal N(0,v_0),
\qquad
dX_t=\sigma dW_t.
$$

SDE marginal：

$$
p_t=\mathcal N(0,v_t),
\qquad
v_t=v_0+\sigma^2t.
$$

Score：

$$
s_t(x)=-\frac{x}{v_t}.
$$

Probability-flow ODE：

$$
\frac{dZ_t}{dt}
=
-\frac12\sigma^2s_t(Z_t)
=
\frac{\sigma^2}{2v_t}Z_t.
$$

直接求解：

$$
\boxed{
Z_t
=
Z_0\sqrt{\frac{v_t}{v_0}}
}.
$$

若 $Z_0\sim\mathcal N(0,v_0)$，则

$$
Z_t\sim\mathcal N(0,v_t),
$$

与 SDE marginal 完全相同。

但两者 path law 明显不同：

$$
[X]_t=\sigma^2t,
\qquad
[Z]_t=0
$$

对 smooth ODE path。对 $s<t$：

$$
\operatorname{Cov}(X_s,X_t)
=v_0+\sigma^2s,
$$

$$
\operatorname{Cov}(Z_s,Z_t)
=\sqrt{v_sv_t}.
$$

同样的 diagonal variances，完全不同的 cross-time covariance。

## 十六、Probability-flow velocity 不是唯一的

Density evolution只约束

$$
\nabla\cdot(vp).
$$

若向 velocity 加 $u$，且

$$
\nabla\cdot(up)=0,
$$

则 $v+u$ 产生同一 continuity equation。高维中可存在非零 divergence-free probability current。

所以 canonical $v=J/p$ 是由 SDE current 直接选出的自然代表，不代表“所有同 marginal ODE 中唯一的那个”。

一维且 boundary flux 固定时，自由度小得多；高维旋转流则展示明显 gauge freedom。

## 十七、Likelihood 与 instantaneous change of variables

沿 probability-flow ODE

$$
\dot Z_t=v(t,Z_t),
$$

若 flow 是可微 diffeomorphism，连续性方程给

$$
\frac d{dt}\log p_t(Z_t)
=
-\nabla\cdot v(t,Z_t).
$$

所以

$$
\log p_T(Z_T)
=
\log p_0(Z_0)
-\int_0^T\nabla\cdot v(t,Z_t)dt.
$$

这把 probability-flow ODE 接到 continuous normalizing flow。

但“可计算 likelihood”仍有多本账：

1. score $s_\theta$ 是否等于 population score；
2. velocity 的 divergence 是否精确或用 Hutchinson estimate；
3. state 与 log-density 是否用一致 solver；
4. finite tolerance 与 roundoff；
5. endpoint/support 是否 regular；
6. model density 与 data density 是否同一 object。

有限 NFE 的 likelihood estimate 不是无条件“exact likelihood”。

## 十八、Score error 与 solver error 必须分账

令

$$
\widehat s=s+e.
$$

在 state-independent isotropic diffusion 下：

$$
\widehat v-v
=
-\frac12g^2e.
$$

把 true density $p$ 代入 approximate continuity equation，PDE residual 为

$$
\partial_tp+\nabla\cdot(\widehat vp)
=
-\frac12g^2\nabla\cdot(pe).
$$

所以 small pointwise/L2 score error 如何变成 density error，还依赖：

- $p$ 的权重与 tails；
- error 的 divergence/regularity；
- flow stability；
- dimension 与 time horizon；
- endpoint singularity；
- solver。

若把 solver step $h\to0$，只会逼近错误 velocity $\widehat v$ 的 continuous flow；它不会修复 score/model bias。

反过来，即使 score exact，finite-step ODE 仍有 discretization bias。实验必须至少包含：

$$
\text{exact score + step refinement}
$$

与

$$
\text{score perturbation + accurate solver}
$$

两条轴。

## 十九、Singular initial law 与 smoothing 边界

Data distribution 可能集中在低维 manifold 上，没有 $\mathbb R^d$ Lebesgue density。此时 $p_0$ 与 $s_0=\nabla\log p_0$ 不存在于普通意义。

非退化 Gaussian diffusion 对任意 $t>0$ 常产生 smooth positive density，但：

1. $t\downarrow0$ 时 score 可能爆大；
2. probability-flow velocity 可能变 stiff/singular；
3. ODE flow 在 closed interval $[0,T]$ 的 global regularity不能由 $t>0$ 局部性质自动推出；
4. likelihood at exact data endpoint 需 dequantization/noise floor 等额外建模；
5. degenerate diffusion 未必在所有方向 smoothing。

这解释 diffusion implementation 常避开 exact endpoint $\varepsilon=0$，但具体 cutoff 仍是 model/numerical choice。

## 二十、Fokker–Planck 的数值方法

### 20.1 直接解 density PDE

一维 current form：

$$
\partial_tp=-\partial_xJ
$$

适合 finite volume：

$$
p_i^{n+1}
=
p_i^n
-\frac{\Delta t}{\Delta x}
\left(
J_{i+1/2}^n-J_{i-1/2}^n
\right).
$$

内部 flux telescope，所以总质量只由 boundary flux 改变。Drift 可用 upwind，diffusion 用 centered gradient。

验收：

- mass conservation；
- nonnegativity；
- CFL/parabolic time-step；
- boundary flux；
- grid convergence；
- stationary density；
- entropy/free-energy trend（若 theorem 支持）。

### 20.2 Monte Carlo particles

模拟 SDE particles 并估计 density/moments：

- dimension 扩展较好；
- 有 $M^{-1/2}$ sampling error；
- density/tail/score估计在高维困难；
- path functionals自然。

### 20.3 Probability-flow particles

求解 ODE：

- 给定 initial sample 后 trajectory deterministic；
- 可调用 ODE solver 与 change-of-variables；
- 需要 score/density-dependent velocity；
- 无 Brownian sampling variance不等于无 model/solver error；
- path statistics不再代表原 SDE。

三条路线解决不同对象，不应只按“哪张 histogram 好看”比较。

## 二十一、实验：三道不可合并的验收门

配套实验 [[实验 - Fokker-Planck、概率流与score误差审计]]。

先用下图回答一个实验问题：**守恒 FPE 是否网格收敛，同边缘 SDE/ODE 是否仍有不同 quadratic variation，score 与 solver bias 能否被分开识别？**

![[00-知识库管理/_assets/plots/dynamics/plot-fokker-planck-probability-flow-v2.svg|880]]

> [!figure] 图 10.9.11b｜守恒 FPE、同边缘不同 QV 与 score/solver 分账
> A 对一维 OU Fokker–Planck 使用 no-flux finite volume，在 $N=80,160,320$ 网格上得到 $L^1$ observed order $0.951$，最大 mass drift $2.22\times10^{-16}$ 且 density 非负；B 在同终端方差约 $1.210$ 下，SDE realized QV 随 refinement 保持常数（order $-0.002$），probability-flow ODE QV 按一阶趋零；C 扫描 score multiplicative error 对终端方差的偏差，并另报告 exact-score Euler solver order $1.004$。参数：seed `20260819`，5000 paths。来源：确定性模拟；数据与原断言：[[fokker_planck_probability_flow_audit.py]]；v2 绘图脚本：[[plot_stochastic_experiments_v2.py]]。

**怎样读图。** A 从 fine 到 coarse $dx$ 读密度误差，并用 mass/min-density 作为 conservation/positivity 旁证；B 横轴从 coarse 到 fine $N$，红线常数说明 stochastic QV 不消失，绿线下降说明 smooth ODE path 的 QV 趋零；C 红线穿过零 score error，蓝色文字的 solver order 只描述 exact-score 时的步长 bias，二者不可相互抵消。

**适用边界（图没有证明什么）。** 实验使用一维 Gaussian/OU 可解基准和特定 first-order schemes，不证明高维、非线性、state-dependent diffusion 或复杂边界下同样表现。Monte Carlo variance、domain truncation 与 grid range 都会影响结果。相同 terminal variance/histogram 不证明完整 marginals 或 path law 一致；score-bias 曲线也不是任意网络误差的普适响应函数。

### 21.1 守恒 FPE

对 zero-mean OU

$$
dX_t=-0.8X_tdt+0.7dW_t,
\qquad
X_0\sim\mathcal N(0,0.4),
$$

在 $[-6,6]$ 用 no-flux finite volume推进到 $T=0.6$。$N=80,160,320$ 的 $L^1$ density errors 为

$$
4.48896\times10^{-2},
\quad
2.34542\times10^{-2},
\quad
1.20127\times10^{-2},
$$

observed order：

$$
0.95090981.
$$

最大 mass drift 为 $2.22\times10^{-16}$，最小 density 保持非负。

### 21.2 同边缘、不同路径

对 $v_0=0.4,\sigma=0.9,T=1$，SDE 与 exact probability flow 的 terminal empirical variances 分别为

$$
1.21530017,\qquad1.23393644,
$$

理论均为

$$
1.21.
$$

但 partition QV 随 refinement 的 orders 为

$$
-0.00157771
$$

与

$$
0.99996808.
$$

前者趋于 $\sigma^2T=0.81$，后者按 $1/N$ 消失。

### 21.3 Score 与 solver 分账

若把 Gaussian score 乘以 $1+\varepsilon$，continuous probability-flow 最终 variance relative error 是

$$
\left(
\frac{v_T}{v_0}
\right)^\varepsilon-1.
$$

$\varepsilon=0.1$ 时误差约11.7%。即使 ODE 精确积分也不会消失。另一方面 exact-score forward Euler 的 variance error observed order 为

$$
1.00375713.
$$

Step refinement 只能消除后一种误差。

## 二十二、Density 与 probability-flow 审计卡

~~~text
SDE
  Ito or Stratonovich
  drift a(t,x), diffusion B(t,x), D = B B^T
  state/noise dimension and initial law
  existence, uniqueness, nonexplosion

GENERATOR
  domain and boundary conditions
  L phi = a · grad phi + 1/2 tr(D Hess phi)
  Dynkin integrability / localization

FORWARD PDE
  weak or classical solution
  L* and all derivatives on D_ij p
  current J = a p - 1/2 div(D p)
  whole-space / periodic / reflecting / absorbing
  mass, positivity, regularity, uniqueness

PROBABILITY FLOW
  density positive where J/p is used
  v = a - 1/2 div D - 1/2 D score
  continuity-equation and ODE well-posedness
  canonical velocity vs divergence-free alternatives
  same one-time marginals, not same path law

AI MODEL
  population score vs learned score
  score error metric and weighting
  continuous learned flow vs finite-step solver
  divergence estimator and likelihood error
  endpoint/noise-floor/dequantization policy

NUMERICS
  finite volume / particles / ODE
  mass and positivity
  boundary and CFL/tolerance
  grid/step refinement
  Monte Carlo interval
  exact-score and perturbed-score controls
~~~

## 二十三、常见错误与最短修正

| 错误 | 为什么错 | 最短修正 |
|---|---|---|
| $\mathcal L$ 就是 Fokker–Planck operator | 前者作用 test function | density 上用 $\mathcal L^\ast$ |
| Forward/backward 只是时间符号不同 | 作用变量与条件不同 | 写清起点/终点变量 |
| $\partial_{ij}(D_{ij}p)=D_{ij}\partial_{ij}p$ | state-dependent $D$ 有 product terms | 保留 divergence form |
| Stationary 必有 $J=0$ | periodic nonequilibrium 可有环流 | 分开 $\nabla\cdot J=0$ 与 $J=0$ |
| FPE 自动守恒质量 | boundary flux 可能非零 | 写 control-volume balance |
| Same marginals 等于 same process | FDD/QV 可不同 | 比较 cross-time covariance |
| Probability flow 唯一 | 可加 weighted divergence-free velocity | 声明 canonical current velocity |
| $v=a-\frac12Ds$ 总正确 | state-dependent $D$ 漏 $\nabla\cdot D$ | 用 $J/p$ 推导 |
| Learned score 小误差必有小生成误差 | 还依赖 divergence、tails、stability | 指定 theorem/metric |
| 减小 ODE step 能修复 score | 只逼近错误连续场 | score/solver 双轴实验 |
| Data manifold 上总有 score | 可能无 Lebesgue density | $t>0$ smoothing/noise floor |
| ODE likelihood 无数值误差 | state/logp/divergence均需计算 | 完整 likelihood ledger |

## 二十四、最小掌握检查

### 概念

1. Generator 与 adjoint 分别作用在哪个对象？
2. Backward/forward Kolmogorov 的变量与条件有何不同？
3. 为什么 weak FPE 从 test functions 开始？
4. Probability current 怎样编码 boundary mass change？
5. Stationary 与 detailed balance 有何区别？
6. Score 在 $p=0$ 或 singular law 上有什么问题？
7. 为什么 probability-flow ODE 只承诺 marginals？

### 闭卷推导

在不看正文时重建：

$$
\mathcal L\varphi
=a^\top\nabla\varphi
+\frac12\operatorname{tr}(D\nabla^2\varphi),
$$

$$
\partial_tp
=
-\partial_i(a_ip)
+\frac12\partial_{ij}(D_{ij}p),
$$

$$
J=ap-\frac12\nabla\cdot(Dp),
$$

$$
v=a-\frac12\nabla\cdot D-\frac12D\nabla\log p,
$$

以及 Brownian noising probability flow

$$
Z_t=Z_0\sqrt{\frac{v_0+\sigma^2t}{v_0}}.
$$

### 数值/研究检查

1. Finite-volume flux 是否 telescope？
2. Boundary flux 与 mass drift 是否一致？
3. SDE/PF 是否同时匹配 marginal moments？
4. Cross-time covariance/QV 是否被单独报告？
5. Exact-score solver refinement是否收敛？
6. Perturbed-score accurate-solver实验是否存在？
7. Likelihood是否同步积分 divergence？

## 二十五、学习闭环与后继接口

- 分层题：[[习题 - Fokker-Planck 方程与概率流 ODE]]；
- 独立详解：[[解答 - Fokker-Planck 方程与概率流 ODE]]；
- 复现实验：[[实验 - Fokker-Planck、概率流与score误差审计]]；
- 下一章：[[时间反演、score 与扩散生成动力学]]将推导 reverse-time drift，连接 score matching、forward noising、reverse SDE/PF ODE 与 finite-step generative sampler。

> [!check] 当前状态
> 正文、机制图、15道 A—E 题、逐题详解和三轨实验均为 composed；尚无学习者首次闭卷答案、独立改参复现与间隔复测，因此保持 draft，不记为 mastered。

## 二十六、来源分工与科学空间入口

- [MIT 8.592J, forward/backward Kolmogorov lecture](https://ocw.mit.edu/courses/8-592j-statistical-physics-in-biology-spring-2011/pages/lecture-notes/)：drift-diffusion、forward/backward equation 与 boundary problem；
- [MIT 18.642, Stochastic Processes II](https://ocw.mit.edu/courses/18-642-topics-in-mathematics-with-applications-in-finance-fall-2024/mit18_642_f24_lec14_1.pdf)：Brownian transition density、heat/Fokker–Planck 与概率守恒；
- [Pavliotis, Stochastic Processes and Applications](https://www.ma.imperial.ac.uk/~pavl/PavliotisBook.pdf)：diffusion、Fokker–Planck、Langevin、stationary/reversible process 的正式主线；
- [Risken, The Fokker–Planck Equation](https://link.springer.com/book/10.1007/978-3-642-61544-3)：一维/多维 FPE、stationary solutions与应用；
- [Song et al., Score-Based Generative Modeling through SDEs](https://arxiv.org/abs/2011.13456)：score SDE 与 probability-flow ODE 原始 AI 框架；
- [Albergo et al., Stochastic Interpolants](https://proceedings.mlr.press/v235/albergo24a.html)：continuity/Fokker–Planck、flow/diffusion统一接口；
- [[S-2016-Su-3762-随机微分方程]]：transition probability、SDE 与 PDE 的中文问题入口；
- [[S-2022-Su-9209-扩散模型SDE篇]]：扩散 SDE、score 与连续采样入口；
- [[S-2022-Su-9228-概率流ODE]]：从 Fokker–Planck 到同边缘 ODE 的中文推导入口；
- [[S-2022-Su-9280-硬刚扩散ODE]]：density 小步变化、扩散 ODE 与数值困难入口。

正式 adjoint、PDE、stationarity 与 probability-flow 等价由课程、教材和原论文承担；科学空间负责中文问题意识。本章自行补齐 weak-form derivation、state-dependent diffusion correction、boundary/current、same-marginal counterexample、score/solver 双误差与守恒数值实验。
