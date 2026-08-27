---
type: solution
status: draft
area: [math/probability, math/stochastic-processes, math/sde, math/pde, ai/generative-modeling]
topic: "Fokker-Planck 方程与概率流 ODE"
exercise: "[[习题 - Fokker-Planck 方程与概率流 ODE]]"
related: ["[[Fokker-Planck 方程与概率流 ODE]]", "[[ODE、动力系统与 SDE MOC]]", "[[练习与测验 MOC]]", "[[实验 - Fokker-Planck、概率流与score误差审计]]"]
created: 2026-08-19
updated: 2026-08-19
---

# 解答 - Fokker-Planck 方程与概率流 ODE

> [!important] 判断顺序
> 先问 operator 作用在 test function 还是 density，再问 weak/classical 与 boundary；然后区分 stationary divergence-free current 与 detailed-balance zero current；最后才把 diffusion current 除以 density构造 probability flow。任何“等价”都必须注明只在 one-time marginals 层成立。

## A. 对象、generator 与 Kolmogorov 方程

### DYN-FP-A01

对象与连接如下。

| 对象 | 定义 | 连接 |
|---|---|---|
| transition kernel | $P_{s,t}(x,A)=\mathbb P(X_t\in A\mid X_s=x)$ | Chapman–Kolmogorov |
| transition density | $P_{s,t}(x,dy)=p(s,x;t,y)dy$ | 需要 absolute continuity |
| evolution operator | $P_{s,t}\varphi(x)=\int\varphi(y)P_{s,t}(x,dy)$ | 作用 observable |
| generator | $\mathcal L_t\varphi=\lim_{h\downarrow0}(P_{t,t+h}\varphi-\varphi)/h$ | Itô formula |
| adjoint | $\int(\mathcal L\varphi)p=\int\varphi(\mathcal L^\ast p)$ | boundary-dependent |
| marginal law | $\mu_t=\mu_0P_{0,t}$ | 不要求 density |
| density | $\mu_t(dx)=p_t(x)dx$ | FPE 若存在 |
| current | $J=ap-\frac12\nabla\cdot(Dp)$ | $\partial_tp+\nabla\cdot J=0$ |
| score | $s_t=\nabla\log p_t$ | 需 $p_t>0$ 可微 |
| PF velocity | $v=J/p$ | $\partial_tp+\nabla\cdot(vp)=0$ |
| path law | function-space law | marginals只是一组投影 |

相邻连接公式：

$$
P_{s,t}\varphi(x)
=
\int\varphi(y)p(s,x;t,y)dy,
$$

$$
\mu_t(A)=\int P_{s,t}(x,A)\mu_s(dx),
$$

$$
\partial_tP_{s,t}\varphi
=
P_{s,t}\mathcal L_t\varphi
$$

在合适 domain 下，

$$
\partial_tp_t=\mathcal L_t^\ast p_t,
$$

$$
J=ap-\frac12\nabla\cdot(Dp),
\qquad
v=J/p.
$$

若 density 不存在，$\mu_t$ 与 kernel 仍可作为 measures；forward equation 可写 measure-valued weak form：

$$
\frac d{dt}\int\varphi\,d\mu_t
=
\int\mathcal L_t\varphi\,d\mu_t.
$$

若 score 不存在，canonical $J/p$ 的 pointwise probability-flow 表达也可能不存在，但 distributional FPE 仍可能有意义。

### DYN-FP-A02

Generator：

$$
\mathcal L\varphi(x)
=
(\alpha+\beta x)\varphi'(x)
+\frac12(\gamma+\delta x)^2\varphi''(x).
$$

逐项：

$$
\mathcal L1=0,
$$

$$
\mathcal Lx=\alpha+\beta x,
$$

$$
\mathcal Lx^2
=
2x(\alpha+\beta x)+(\gamma+\delta x)^2
$$

即

$$
\mathcal Lx^2
=
\gamma^2+(2\alpha+2\gamma\delta)x
+(2\beta+\delta^2)x^2.
$$

对 $x^3$：

$$
\begin{aligned}
\mathcal Lx^3
&=
3x^2(\alpha+\beta x)
+3x(\gamma+\delta x)^2\\
&=
3\gamma^2x
+(3\alpha+6\gamma\delta)x^2
+(3\beta+3\delta^2)x^3.
\end{aligned}
$$

令 $m_k=\mathbb E[X_t^k]$：

$$
m_1'
=
\alpha+\beta m_1,
$$

$$
m_2'
=
\gamma^2+(2\alpha+2\gamma\delta)m_1
+(2\beta+\delta^2)m_2,
$$

$$
m_3'
=
3\gamma^2m_1
+(3\alpha+6\gamma\delta)m_2
+(3\beta+3\delta^2)m_3.
$$

由于 drift affine、diffusion affine，$\mathcal L$ 把 degree-$k$ polynomial 映到不超过 degree $k$，所以所有 finite polynomial moment systems 都 triangularly close，只要相应 moments 存在。

Fokker–Planck differential expression：

$$
\partial_tp
=
-\partial_x[(\alpha+\beta x)p]
+\frac12\partial_{xx}[(\gamma+\delta x)^2p].
$$

但 differential expression 没说明 state domain、absorbing/reflecting boundary、operator domain 或 explosion behavior；这些决定真正的 generator realization。

当 $\delta=0$：

$$
m_1'=\alpha+\beta m_1.
$$

若 $\beta\ne0$：

$$
m_1(t)
=
e^{\beta t}m_1(0)
+\frac{\alpha}{\beta}(e^{\beta t}-1).
$$

Variance $V$ 满足

$$
V'=2\beta V+\gamma^2.
$$

故

$$
V(t)
=
e^{2\beta t}V(0)
+\frac{\gamma^2}{2\beta}(e^{2\beta t}-1)
$$

对 $\beta\ne0$；$\beta=0$ 时

$$
m_1(t)=m_1(0)+\alpha t,
\qquad
V(t)=V(0)+\gamma^2t.
$$

### DYN-FP-A03

Tower property 与 Markov property 给

$$
\begin{aligned}
\mathbb E[u(t,X_t)\mid\mathcal F_s]
&=
\mathbb E[
\mathbb E[\psi(X_T)\mid\mathcal F_t]
\mid\mathcal F_s]\\
&=
\mathbb E[\psi(X_T)\mid\mathcal F_s]
=u(s,X_s)
\end{aligned}
$$

对 $s<t$。所以 $u(t,X_t)$ 是 martingale。

Itô formula：

$$
du(t,X_t)
=
\left(
\partial_tu+\mathcal L_tu
\right)dt
+\nabla u^\top B\,dW_t.
$$

Martingale 的 finite-variation drift 必须为0：

$$
\boxed{
\partial_tu+\mathcal L_tu=0
},
$$

terminal condition：

$$
u(T,x)=\psi(x).
$$

对 transition density $p(s,x;T,y)$，backward equation 作用在 $(s,x)$：

$$
\partial_sp+\mathcal L_s^{(x)}p=0.
$$

Forward equation作用在 terminal $(t,y)$：

$$
\partial_tp=(\mathcal L_t^{(y)})^\ast p.
$$

Backward PDE 传播 conditional expectation；FPE 传播 marginal/transition density；reverse-time SDE 则是另一个带反向 filtration与修正 drift 的 stochastic process，留给 DYN-12。

Arithmetic Brownian：

$$
dX_t=\mu dt+\sigma dW_t.
$$

令 $\tau=T-t$，条件分布给

$$
u(t,x)
=
\mathbb E[
(x+\mu\tau+\sigma\sqrt\tau Z)^2
]
=
(x+\mu\tau)^2+\sigma^2\tau.
$$

计算

$$
u_x=2(x+\mu\tau),
\quad
u_{xx}=2,
$$

$$
u_t=-2\mu(x+\mu\tau)-\sigma^2.
$$

因此

$$
u_t+\mu u_x+\frac12\sigma^2u_{xx}=0,
$$

且 $u(T,x)=x^2$。

## B. Adjoint、弱形式与 boundary

### DYN-FP-B01

Dynkin weak form：

$$
\frac d{dt}\int\varphi p\,dx
=
\int
\left[
a_i\partial_i\varphi
+\frac12D_{ij}\partial_{ij}\varphi
\right]p\,dx,
$$

采用 Einstein summation。

Drift 一次分部积分：

$$
\int a_ip\,\partial_i\varphi\,dx
=
-\int\varphi\,\partial_i(a_ip)dx
+\int_{\partial\Omega}\varphi a_ipn_i\,dS.
$$

Diffusion 两次分部积分后，interior 项为

$$
\frac12\int\varphi\,\partial_{ij}(D_{ij}p)dx,
$$

另有两层 boundary terms。若 $\varphi$ compactly supported，interior derivation 不见边界；若要求实际 domain 上的 mass balance，边界不能忽略。

因此

$$
\boxed{
\partial_tp
=
-\partial_i(a_ip)
+\frac12\partial_i\partial_j(D_{ij}p)
}.
$$

定义

$$
J_i
=
a_ip-\frac12\partial_j(D_{ij}p),
$$

则

$$
\partial_tp+\partial_iJ_i=0.
$$

Product expansion：

$$
\begin{aligned}
\partial_i\partial_j(D_{ij}p)
&=
D_{ij}\partial_{ij}p
+(\partial_iD_{ij})\partial_jp
+(\partial_jD_{ij})\partial_ip\\
&\quad+
(\partial_{ij}D_{ij})p.
\end{aligned}
$$

求和且 $D$ symmetric 时中间两个一阶项可重新组合，但不会一般消失。

一维反例取 $D(x)=1+x^2$、$p(x)=1$ 在局部：

$$
\partial_{xx}(Dp)=2,
$$

而

$$
D\partial_{xx}p=0.
$$

二者不同。

Compactly supported test function 适合 distributional interior equation；whole space 需要 $p,J$ 等衰减；bounded domain 需指定 no-flux、absorbing、periodic 或其他 boundary condition 才构成完整 forward problem。

### DYN-FP-B02

对任意 $\Omega$：

$$
\frac d{dt}M(t)
=
\frac d{dt}\int_\Omega p\,dx
=
-\int_{\partial\Omega}J\cdot n\,dS.
$$

1. Reflecting/no-flux：
   $$
   J\cdot n=0
   $$
   pointwise，故 $M'(t)=0$。

2. Periodic：成对边界的 outward normals 相反，periodic flux 值相同，surface integrals 抵消，故质量守恒。

3. Absorbing/killed：outward flux 可为正，故
   $$
   M(t)=\mathbb P(\tau_{\partial\Omega}>t)
   $$
   是 survival probability。Absorbed mass
   $$
   A(t)=1-M(t)
   $$
   放在 cemetery state $\dagger$ 后，总概率
   $$
   M(t)+\mathbb P(X_t=\dagger)=1.
   $$

4. Prescribed flux：
   $$
   M'(t)
   =
   -\int_{\Gamma_{\rm out}}J\cdot n\,dS
   -\int_{\Gamma_{\rm in}}J\cdot n\,dS,
   $$
   其中 inflow 部分 $J\cdot n<0$ 会增加质量。

Finite-volume audit 应直接记录 boundary face fluxes $J_{1/2},J_{N+1/2}$ 并验证

$$
M^{n+1}-M^n
=
-\Delta t
\left(
J_{N+1/2}-J_{1/2}
\right).
$$

若本应 reflecting，却误设 $p=0$ ghost cells，diffusive gradient通常产生 outward flux；质量 drift 会与该 boundary flux精确对应，从而暴露实现错误。

### DYN-FP-B03

一维 FPE：

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

Stationary 仅给

$$
\partial_xJ_\infty=0,
$$

所以 $J_\infty=C$。只有 boundary/detailed-balance 条件才令 $C=0$。

Zero current：

$$
(b^2p)'=2ap.
$$

于是

$$
\frac{p'}p
=
\frac{2a}{b^2}
-\frac{(b^2)'}{b^2}.
$$

积分：

$$
p_\infty(x)
=
C\,b(x)^{-2}
\exp\left[
\int^x\frac{2a(y)}{b(y)^2}dy
\right].
$$

还需：

- $p_\infty\ge0$ 且可归一化；
- $b^2>0$ 或对退化点分类；
- 所选 boundary 与 zero current兼容；
- SDE 不 explosion；
- density属于 forward operator domain。

取

$$
a(x)=-\kappa x,
\qquad
b^2(x)=\sigma^2(1+x^2).
$$

则

$$
\int\frac{2a}{b^2}dx
=
-\frac{\kappa}{\sigma^2}\log(1+x^2).
$$

所以

$$
p_\infty(x)
\propto
(1+x^2)^{-(1+\kappa/\sigma^2)}.
$$

Tail 约为

$$
|x|^{-2(1+\kappa/\sigma^2)}.
$$

在 whole line 可积需

$$
2(1+\kappa/\sigma^2)>1,
$$

即

$$
\kappa/\sigma^2>-1/2.
$$

若 $\kappa>0$ 自动满足。

在 circle/periodic domain，$\partial_xJ=0$ 允许 $J=C\ne0$，对应持续定向 probability circulation；stationary density 不等于 detailed balance。

## C. 可解模型与 equilibrium

### DYN-FP-C01

Transition density：

$$
p(t,x\mid x_0)
=
\frac1{\sqrt{2\pi\sigma^2t}}
\exp\left[
-\frac{(x-x_0-\mu t)^2}{2\sigma^2t}
\right].
$$

令 $y=x-x_0-\mu t$。直接微分可得

$$
\partial_xp=-\frac{y}{\sigma^2t}p,
$$

$$
\partial_{xx}p
=
\left(
\frac{y^2}{\sigma^4t^2}
-\frac1{\sigma^2t}
\right)p.
$$

时间导数整理后满足

$$
\partial_tp
=
-\mu\partial_xp
+\frac{\sigma^2}{2}\partial_{xx}p.
$$

Weak initial condition：对 bounded continuous $\varphi$，

$$
\int\varphi(x)p(t,x\mid x_0)dx
=
\mathbb E[
\varphi(x_0+\mu t+\sigma\sqrt tZ)
]
\to
\varphi(x_0).
$$

所以 measures weakly趋于 $\delta_{x_0}$。

Current：

$$
J=\mu p-\frac{\sigma^2}{2}\partial_xp.
$$

对 $\varphi=x$：

$$
\mathcal Lx=\mu
\quad\Rightarrow\quad
\frac d{dt}\mathbb E[X_t]=\mu.
$$

对 $\varphi=x^2$：

$$
\mathcal Lx^2=2\mu x+\sigma^2.
$$

对 $\varphi=e^{i\xi x}$：

$$
\mathcal L\varphi
=
\left(
i\mu\xi-\frac12\sigma^2\xi^2
\right)\varphi.
$$

故 characteristic function满足 scalar ODE，解为

$$
\mathbb E[e^{i\xi X_t}]
=
e^{i\xi x_0}
\exp\left[
\left(i\mu\xi-\frac12\sigma^2\xi^2\right)t
\right].
$$

Backward equation对起点变量 $x_0$：

$$
\partial_tu+\mu u_x+\frac12\sigma^2u_{xx}=0
$$

按 terminal-time convention书写。

当 $\sigma\to0$：

$$
\partial_tp+\mu\partial_xp=0,
$$

即 deterministic translation continuity equation。Pointwise 对 $x\ne x_0$ 的 $p(t,x)\to0$ 没告诉质量去哪了；只有 weak convergence 捕捉收缩到 Dirac 的单位质量。

### DYN-FP-C02

OU FPE：

$$
\partial_tp
=
-\partial_x[\kappa(m-x)p]
+\frac{\sigma^2}{2}\partial_{xx}p.
$$

Exact transition：

$$
X_t\mid X_s=x
\sim
\mathcal N\left(
m+(x-m)e^{-\kappa(t-s)},
\frac{\sigma^2}{2\kappa}
(1-e^{-2\kappa(t-s)})
\right).
$$

因此 conditional mean/variance分别满足

$$
\dot m_t=\kappa(m-m_t),
$$

$$
\dot V_t=-2\kappa V_t+\sigma^2.
$$

Gaussian ansatz

$$
p(t,x)
=
\frac1{\sqrt{2\pi V_t}}
\exp\left[-\frac{(x-m_t)^2}{2V_t}\right]
$$

代入 PDE 后，$1,(x-m_t),(x-m_t)^2$ 系数分别给 normalization、上述 mean ODE 与 variance ODE。

Zero current：

$$
\kappa(m-x)p_\infty
-\frac{\sigma^2}{2}p_\infty'=0.
$$

积分得到

$$
p_\infty
\propto
\exp\left[
-\frac{\kappa(x-m)^2}{\sigma^2}
\right],
$$

即 variance $\sigma^2/(2\kappa)$。

若从 stationary law 出发：

$$
\operatorname{Cov}(X_s,X_t)
=
\frac{\sigma^2}{2\kappa}e^{-\kappa|t-s|}.
$$

Backward generator：

$$
\mathcal L\varphi
=
\kappa(m-x)\varphi'
+\frac12\sigma^2\varphi''.
$$

Stationary score：

$$
s_\infty(x)
=
-\frac{2\kappa}{\sigma^2}(x-m).
$$

Canonical PF velocity：

$$
v_\infty
=
\kappa(m-x)-\frac12\sigma^2s_\infty
=0.
$$

所以 probability-flow ODE 的 stationary samples不动；但 stationary OU SDE 仍不断随机波动，且

$$
[X]_t=\sigma^2t.
$$

这再次证明同 stationary marginal 不等于同 path law。

### DYN-FP-C03

常数 SPD $M$ 下：

$$
B=\sqrt{2\beta^{-1}M},
\qquad
D=2\beta^{-1}M.
$$

FPE：

$$
\partial_tp
=
\nabla\cdot(M\nabla U\,p)
+\beta^{-1}\nabla\cdot(M\nabla p).
$$

Current：

$$
J=-M\nabla U\,p-\beta^{-1}M\nabla p.
$$

对

$$
\pi=Z^{-1}e^{-\beta U}
$$

有

$$
\nabla\pi=-\beta\pi\nabla U,
$$

从而 $J_\pi=0$。

概念区分：

- invariance：$\mathcal L^\ast\pi=0$；
- reversibility：transition semigroup 对 $L^2(\pi)$ self-adjoint/detailed balance；
- ergodicity：长期时间平均/分布忘记初值；
- convergence rate：spectral gap、log-Sobolev、coupling 等定量性质。

一个 zero-current density通常给 reversibility，但仍需 process/domain 条件；invariance 本身不推出唯一、ergodic 或快速 mixing。

若 $M=M(x)$，Itô current 为

$$
J=bp-\beta^{-1}\nabla\cdot(Mp).
$$

令 $p=\pi$，有

$$
\nabla\cdot(M\pi)
=
(\nabla\cdot M)\pi
-\beta M\nabla U\,\pi.
$$

要使 $J=0$，应取

$$
\boxed{
b
=
-M\nabla U
+\beta^{-1}\nabla\cdot M
}
$$

在 Euclidean Itô coordinates 下。遗漏 correction 会改变 invariant law。

Preconditioner 可改善某些方向的 local conditioning，但 mixing 取决于 global geometry、barriers、state dependence与discretization；不能仅凭“像 natural gradient”声称全局加速。

Equilibrium audit除 histogram外还应检查 autocorrelation/IACT、transition conditional moments、detailed-balance flow、multiple initializations、barrier crossing与discretization stationary bias。

## D. Probability flow 与数值

### DYN-FP-D01

Current：

$$
J_i
=
a_ip-\frac12\partial_j(D_{ij}p).
$$

在 $p>0$：

$$
v_i
=
\frac{J_i}{p}
=
a_i-\frac1{2p}\partial_j(D_{ij}p).
$$

Product rule：

$$
\frac1p\partial_j(D_{ij}p)
=
\partial_jD_{ij}
+D_{ij}\partial_j\log p.
$$

所以

$$
v
=
a-\frac12\nabla\cdot D-\frac12D\nabla\log p.
$$

形状：

$$
a,v,\nabla\cdot D,\nabla\log p\in\mathbb R^d,
$$

$$
D\in\mathbb R^{d\times d},
\qquad
D\nabla\log p\in\mathbb R^d.
$$

由于 $vp=J$：

$$
\partial_tp
=
-\nabla\cdot J
=
-\nabla\cdot(vp).
$$

同 marginal 的证明责任：

1. SDE law 有 density并满足 FPE；
2. canonical $v$ 定义良好；
3. ODE flow推送 initial density并满足 continuity equation；
4. 同 initial/boundary 下 continuity equation解唯一。

若 $p=0$，$J/p$ 可发散或未定义；只能在 support interior、通过 extension 或 measure-valued formulation处理。

Gauge example：二维 radial Gaussian $p(x)$，取 rotation

$$
u(x)=\omega(-x_2,x_1).
$$

因为 $\nabla\cdot u=0$，且 $u\cdot\nabla p=0$，

$$
\nabla\cdot(up)=0.
$$

所以 $v+u$ 与 $v$ 产生同 density evolution，却有旋转轨迹。

Scalar $D=b^2$：

$$
v
=
a-\frac12(b^2)'
-\frac12b^2\partial_x\log p.
$$

第一项 correction 不能遗漏。

### DYN-FP-D02

SDE marginal：

$$
X_t=X_0+\sigma W_t,
$$

$$
p_t=\mathcal N(0,v_t),
\qquad
v_t=v_0+\sigma^2t.
$$

Score：

$$
s_t(x)=-\frac{x}{v_t}.
$$

PF ODE：

$$
\dot Z_t
=
-\frac12\sigma^2s_t(Z_t)
=
\frac{\sigma^2}{2v_t}Z_t.
$$

积分：

$$
\log\frac{Z_t}{Z_0}
=
\frac12
\int_0^t
\frac{\sigma^2}{v_0+\sigma^2s}ds
=
\frac12\log\frac{v_t}{v_0}.
$$

故

$$
Z_t=Z_0\sqrt{\frac{v_t}{v_0}}.
$$

若 $Z_0\sim\mathcal N(0,v_0)$，则

$$
Z_t\sim\mathcal N(0,v_t),
$$

与 SDE fixed-time marginal相同。

对 $s\le t$：

$$
\operatorname{Cov}(X_s,X_t)
=
\operatorname{Var}(X_0)+\sigma^2\operatorname{Cov}(W_s,W_t)
=
v_0+\sigma^2s.
$$

PF：

$$
\operatorname{Cov}(Z_s,Z_t)
=
\frac{\sqrt{v_sv_t}}{v_0}\operatorname{Var}(Z_0)
=
\sqrt{v_sv_t}.
$$

Quadratic variation：

$$
[X]_t=\sigma^2t,
\qquad
[Z]_t=0
$$

对 smooth PF path。

Conditional transitions：

$$
X_t\mid X_s=x
\sim
\mathcal N(x,\sigma^2(t-s)),
$$

而

$$
Z_t\mid Z_s=x
=
x\sqrt{\frac{v_t}{v_s}}
$$

是 deterministic Dirac transition。

PF scaling factor随 $t$ 增长且保持 sign。对 positive threshold $c$，PF hit-before-$T$ 由 initial $Z_0$ 和 monotone scaling决定；SDE 可从更低初值随机越过并返回。因此 endpoint exceedance相同不保证 hitting probability相同。

只看 fixed-time histograms、mean/variance、terminal FID 类指标无法区分。最小 path-law audit至少加入两个时刻 cross covariance、realized QV 和一个 hitting/maximum functional。

### DYN-FP-D03

Cells $C_i$、faces $x_{i+1/2}$。取 face drift $a_{i+1/2}$：

$$
p_{i+1/2}^{\rm up}
=
\begin{cases}
p_i,&a_{i+1/2}\ge0,\\
p_{i+1},&a_{i+1/2}<0.
\end{cases}
$$

Flux：

$$
J_{i+1/2}
=
a_{i+1/2}p_{i+1/2}^{\rm up}
-D\frac{p_{i+1}-p_i}{\Delta x}.
$$

Update：

$$
p_i^{n+1}
=
p_i^n
-\frac{\Delta t}{\Delta x}
(J_{i+1/2}^n-J_{i-1/2}^n).
$$

乘 $\Delta x$ 对 $i$ 求和，interior faces telescoping：

$$
M^{n+1}-M^n
=
-\Delta t
(J_{N+1/2}-J_{1/2}).
$$

No-flux 直接设两个 boundary flux为0。

一个保守的 positivity 条件形如

$$
\Delta t
\left(
\frac{\max|a|}{\Delta x}
+\frac{2D}{\Delta x^2}
\right)
\le1.
$$

其中 advection restriction 是 $O(\Delta x)$，diffusion restriction 是 $O(\Delta x^2)$；常数依 scheme/boundary而异。

Diagnostics：

$$
e_{L^1}
=
\sum_i|p_i-p_{\rm exact}(x_i)|\Delta x,
$$

$$
e_{\rm mass}=|\sum_ip_i\Delta x-1|,
$$

$$
m_-=\sum_i\max(-p_i,0)\Delta x,
$$

以及 mean/variance error。

OU refinement使用 exact Gaussian mean/variance与density；每次把 $\Delta x$ 减半，同时按稳定条件减小 $\Delta t$，报告 observed order。

误差分工：

- FPE grid：spatial/time truncation与boundary truncation；
- SDE particles：time discretization加 $M^{-1/2}$ MC；
- PF ODE：score/model加 ODE step/tolerance；
- density histogram/KDE：额外 density-estimation bias。

高维 tensor grid 成本指数增长；particles避免 full grid，但 pointwise density/score估计变难。

## E. AI、likelihood 与研究审计

### DYN-FP-E01

Exact velocity：

$$
v=f-\frac12g^2s.
$$

若 $\widehat s=s+e$：

$$
\delta v
:=
\widehat v-v
=
-\frac12g^2e.
$$

True density满足

$$
\partial_tp+\nabla\cdot(vp)=0.
$$

代入 learned field：

$$
\boxed{
\partial_tp+\nabla\cdot(\widehat vp)
=
-\frac12g^2\nabla\cdot(pe)
}.
$$

Small weighted score MSE

$$
\mathbb E_p\|e\|^2
$$

不直接控制 $\nabla\cdot(pe)$、tail、flow Jacobian、long-time amplification或 density metric；需额外 regularity/stability theorem。

误差账：

1. population score vs learned score；
2. learned continuous velocity vs target continuous velocity；
3. finite-step computed flow vs learned continuous flow；
4. finite samples/divergence estimator。

Experiment axes：

- exact score，$h=2^{-k}$：只测 solver bias；
- $\widehat s=(1+\varepsilon)s$，用高精度 solver：测 score bias；
- 二维 grid $(\varepsilon,h)$：检测 interaction。

Gaussian noising 中 $v_t=v_0+\sigma^2t$。若 score乘 $1+\varepsilon$：

$$
\dot Z
=
\frac12\sigma^2(1+\varepsilon)\frac Z{v_t}.
$$

所以

$$
Z_T
=
Z_0
\left(
\frac{v_T}{v_0}
\right)^{(1+\varepsilon)/2}.
$$

Final variance：

$$
\widehat V_T
=
v_0
\left(
\frac{v_T}{v_0}
\right)^{1+\varepsilon}.
$$

Relative error：

$$
\frac{\widehat V_T}{v_T}-1
=
\left(
\frac{v_T}{v_0}
\right)^\varepsilon-1.
$$

可证伪 thresholds 示例：

- exact-score step halving observed order 在理论区间；
- $\varepsilon=0$ final variance relative error小于 $10^{-4}$；
- predicted analytic score-bias curve relative discrepancy小于1%；
- mass normalization误差小于 $10^{-10}$；
- path-law claim不得由 marginal tests通过。

### DYN-FP-E02

ODE continuity equation：

$$
\partial_tp+\nabla\cdot(v_\theta p)=0.
$$

沿 characteristic：

$$
\frac d{dt}\log p_t(Z_t)
=
-\nabla\cdot v_\theta(t,Z_t).
$$

积分：

$$
\log p_T(Z_T)
=
\log p_0(Z_0)
-\int_0^T\nabla\cdot v_\theta(t,Z_t)dt.
$$

反向用于 data likelihood 时，必须按实际积分方向一致记录 signs 与 base endpoint。

若

$$
v_\theta=f-\frac12g(t)^2s_\theta,
$$

则

$$
\nabla\cdot v_\theta
=
\nabla\cdot f
-\frac12g(t)^2
\operatorname{tr}
\left(
\nabla_xs_\theta
\right).
$$

Hutchinson 用 random probe $\epsilon$：

$$
\mathbb E[
\epsilon^\top
(\nabla_xs_\theta)
\epsilon
]
=
\operatorname{tr}(\nabla_xs_\theta)
$$

当 $\mathbb E[\epsilon\epsilon^\top]=I$。它估计 score Jacobian trace，不估计完整 score/model error。

误差：

| 层 | 来源 |
|---|---|
| probe | finite probes、distribution、reuse |
| state | ODE local/global error |
| log-density | divergence quadrature与同步误差 |
| model | $s_\theta-s$ |
| arithmetic | dtype/roundoff |

Adaptive rejection 时若每次 trial resample probe，accepted path的 random estimator 与 solver control相互作用并改变程序；固定 probe降低trajectory内随机噪声但改变 covariance。必须声明并用同目标 FD/replicates 验收。

Exact baseline 可用 linear Gaussian PF：

$$
\dot z=A(t)z,
\qquad
\nabla\cdot v=\operatorname{tr}A(t),
$$

其 matrix fundamental solution与 Gaussian covariance/logdet均可解析比较。

“Exact likelihood”通常指 continuous change-of-variables identity；finite tolerance、approximate score与random trace使实际数值只是 estimate，必须报告误差。

### DYN-FP-E03

一个合格 DYN-11 方案可定义 forward SDE：

$$
dX_t=f(t,X_t)dt+g(t)dW_t,
\qquad
X_0\sim p_{\rm data}.
$$

**数学对象**

- state/noise dimension、Itô、initial law；
- $D=g^2I$；
- population $p_t,s_t$ 与 learned $s_\theta$；
- FPE：
  $$
  \partial_tp=-\nabla\cdot(fp)+\frac12g^2\Delta p;
  $$
- current：
  $$
  J=fp-\frac12g^2\nabla p;
  $$
- PF：
  $$
  \dot Z=f-\frac12g^2s_t.
  $$

**Endpoint**

- data可 singular，训练/likelihood从 $t=\varepsilon>0$ 开始；
- 报告 $\varepsilon$ 与 dequantization/noise floor；
- 检查 score norm、velocity Jacobian、solver NFE随 $\varepsilon$。

**Analytical baselines**

- Brownian Gaussian noising；
- OU/VP linear Gaussian；
- exact covariance、score、PF factor、log-density。

**三层 metrics**

- marginal：mean/covariance、sliced tests、held-out likelihood；
- transition：conditional covariance或 two-time law；
- path：QV、maximum/hitting、autocorrelation。

**误差分账**

- score approximation；
- ODE step/tolerance；
- divergence probe；
- finite sample；
- endpoint truncation；
- reference-solver uncertainty。

**Ablations**

- exact/perturbed/learned score；
- fixed/adaptive solver；
- tolerance/NFE；
- probe count/distribution/reuse；
- $\varepsilon$ endpoint；
- state/noise dimension。

**留给 DYN-12**

- reverse-time drift theorem；
- reverse Brownian filtration；
- score-matching objective如何恢复 population score；
- prior-to-data generative correctness；
- predictor–corrector/reverse sampler。

**失败停止条件**

- exact Gaussian baseline不收敛；
- mass/normalization drift超阈值；
- step refinement plateau且高于 reference uncertainty；
- score perturbation不符合 analytic toy；
- likelihood对probe/solver选择无稳定区；
- 用 marginal evidence越级声称 path correctness。

Research acceptance checklist：

~~~text
[ ] forward Ito SDE, D=B B^T, initial law fixed
[ ] generator and adjoint derived with indices
[ ] current and boundary contract explicit
[ ] FPE weak/classical layer stated
[ ] probability-flow velocity includes div D correction
[ ] density positivity/support issue handled
[ ] Gaussian/OU exact marginal and likelihood baseline passed
[ ] marginal, transition, and path diagnostics separated
[ ] exact-score step refinement passed
[ ] perturbed-score accurate-solver curve passed
[ ] divergence probe and ODE/logp errors separated
[ ] endpoint epsilon/dequantization reported
[ ] finite-step likelihood not called exact without qualifier
[ ] reverse-time claims deferred to DYN-12
~~~
