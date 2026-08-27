---
type: solution
status: draft
area: [math/probability, math/stochastic-processes, math/sde, math/numerical-analysis, ai/generative-modeling]
topic: "Itô 引理与随机微分方程"
exercise: "[[习题 - Itô 引理与随机微分方程]]"
related: ["[[Itô 引理与随机微分方程]]", "[[ODE、动力系统与 SDE MOC]]", "[[练习与测验 MOC]]", "[[实验 - Itô 和、SDE 强弱误差与离散梯度审计]]"]
created: 2026-08-19
updated: 2026-08-19
---

# 解答 - Itô 引理与随机微分方程

> [!important] 判断顺序
> 先确定 filtration、integral interpretation 与 solution concept；再做 Itô calculation；随后区分 exact process、numerical process 和 target functional；最后才讨论 AI。每次出现 strong/weak 都必须写清它修饰的是 solution 还是 numerical convergence。

## A. 定义、因果与等距

### DYN-ITO-A01

完整 object card 如下。

| 层 | 必须声明 | 作用 |
|---|---|---|
| 基础概率对象 | $(\Omega,\mathcal F,(\mathcal F_t),\mathbb P)$ | 定义“almost surely”和信息流 |
| 状态/噪声 | $X_t\in\mathbb R^d,W_t\in\mathbb R^m$ | 固定矩阵形状 |
| Brownian contract | $W$ 相对于 $(\mathcal F_t)$ 是 Brownian | 未来 increment 独立于当前信息 |
| 初值 | $\xi\in\mathcal F_0$、矩条件、与未来 increments 的关系 | 决定初始 law 与可积性 |
| coefficient | $a:[0,T]\times\mathbb R^d\to\mathbb R^d$，$B:[0,T]\times\mathbb R^d\to\mathbb R^{d\times m}$ | 定义 drift 与 local covariance |
| 正则性 | joint measurability、Lipschitz、growth 或替代条件 | existence、uniqueness、nonexplosion |
| 积分解释 | Itô 或 Stratonovich | 决定 drift correction |
| 解 | strong/weak，global/maximal | 决定固定或可更换哪些概率对象 |
| uniqueness | pathwise/in law | 决定比较 path 还是 law |
| 数值 | scheme、step/tolerance、Brownian coupling | 定义 computed process |
| 误差 | strong、weak、path-event | 决定验收对象 |
| AI | $a_\theta,B_\theta$、loss、gradient、solver | 分离 model/statistical/numerical error |

微分记号

$$
dX_t=a(t,X_t)dt+B(t,X_t)dW_t
$$

只显示局部形式。它没有单独编码 filtration、初值与 noise 的 joint construction、coefficient 条件、Itô/Stratonovich、solution concept 或 numerical method。完整含义必须还原为

$$
X_t
=\xi+\int_0^ta(s,X_s)ds
+\int_0^tB(s,X_s)dW_s
$$

并附上上述合同。

### DYN-ITO-A02

按定义，

$$
I:=\int_0^TH_tdW_t
=H_0(W_{t_1}-W_{t_0})
+H_1(W_{t_2}-W_{t_1}).
$$

记

$$
\Delta_0W=W_{t_1}-W_{t_0},
\qquad
\Delta_1W=W_{t_2}-W_{t_1}.
$$

因为 $H_i\in\mathcal F_{t_i}$，且 $\Delta_iW$ 独立于 $\mathcal F_{t_i}$、条件均值为0，

$$
\mathbb E[H_i\Delta_iW]
=
\mathbb E\left[
H_i\mathbb E[\Delta_iW\mid\mathcal F_{t_i}]
\right]=0.
$$

故 $\mathbb E[I]=0$。

展开平方：

$$
I^2
=H_0^2(\Delta_0W)^2
+H_1^2(\Delta_1W)^2
+2H_0H_1\Delta_0W\Delta_1W.
$$

对 cross term，$H_0H_1\Delta_0W$ 在 $\mathcal F_{t_1}$ 可测，因此

$$
\begin{aligned}
\mathbb E[H_0H_1\Delta_0W\Delta_1W]
&=
\mathbb E\left[
H_0H_1\Delta_0W
\mathbb E[\Delta_1W\mid\mathcal F_{t_1}]
\right]\\
&=0.
\end{aligned}
$$

对 diagonal term，

$$
\mathbb E[H_i^2(\Delta_iW)^2]
=
\mathbb E[H_i^2](t_{i+1}-t_i).
$$

所以

$$
\mathbb E[I^2]
=
\mathbb E[H_0^2](t_1-t_0)
+\mathbb E[H_1^2](t_2-t_1)
=
\mathbb E\int_0^TH_t^2dt.
$$

取 $H_0=1,H_1=W_{t_1}$，利用 $\mathbb E[W_{t_1}^2]=t_1$：

$$
\operatorname{Var}(I)
=t_1+t_1(T-t_1).
$$

若错误地取 $H_1=\Delta_1W$，则 $H_1\notin\mathcal F_{t_1}$。并且

$$
\mathbb E[H_1\Delta_1W]
=\mathbb E[(\Delta_1W)^2]
=T-t_1\ne0.
$$

零均值证明与 cross-term 的条件期望结构都失去依据。

本题用 deterministic partition 定义 simple process。若 partition endpoints 是 stopping times，可建立更一般的 elementary predictable processes，但要额外检查 stopping-time measurability、boundedness/localization；不能仅把随机网格代进 deterministic proof。

### DYN-ITO-A03

1. **错误。** Adapted 只说明固定 $t$ 的 $H_t$ 对 $\mathcal F_t$ 可测；predictable 是对 predictable $\sigma$-field 的联合可测。连续或 left-continuous adapted process 可推出 predictable，但一般 adapted process 需额外条件。

2. **错误。** Deterministic $h$ 给
   $$
   \int h\,dW\sim\mathcal N(0,\int h^2dt).
   $$
   但
   $$
   \int_0^TW_t\,dW_t=\frac12(W_T^2-T)
   $$
   不是 Gaussian。

3. **错误。** Brownian path 无限 total variation，普通 Riemann–Stieltjes theorem 不适用。Itô integral 先由 adapted sums 在 $L^2(\Omega)$ 中构造。

4. **错误。** 对 $H=W$，
   $$
   S_\Pi-L_\Pi
   =\frac12\sum_i(\Delta_iW)^2\to\frac T2.
   $$

5. **错误。** Isometry 是 expectation identity：
   $$
   \mathbb E\left|\int H\,dW\right|^2
   =\mathbb E\int H^2dt.
   $$
   它不是随机变量逐样本相等。

6. **错误。** Strong solution 固定 probability space 和 Brownian motion；strong numerical convergence 比较同一 noise 下 exact/approximate path。

7. **错误。** Weak solution 允许 probability space 与 Brownian motion 作为 construction 的一部分；它不表达误差大小。

8. **错误。** 同 seed 但不同循环次数、batch/device、adaptive rejection 都会改变 PRNG 消耗。跨网格 strong comparison 应由同一 finest increments 聚合，或使用 Brownian tree。

9. **错误。** 正确含义是沿合适 partition
   $$
   \sum_i(\Delta_iW)^2\to T,
   $$
   例如在 $L^2$ 中；单步 $(\Delta W)^2$ 不是确定的 $\Delta t$。

10. **错误。** Endpoint law 不能验收 hitting time、maximum、joint-time covariance 或 strong coupling。至少补充 transition/path diagnostics 与相应误差。

## B. Itô integral 与 Itô formula

### DYN-ITO-B01

先对 step functions $f,g$。$(I_f,I_g)$ 是 finitely many Gaussian increments 的线性变换，所以联合 Gaussian。一般 $L^2$ deterministic functions 可用 step approximations；对应 Gaussian vectors 在 $L^2$ 中收敛，特征函数极限仍是 Gaussian。

均值与 covariance 为

$$
\mathbb E[I_f]=\mathbb E[I_g]=0,
$$

$$
\operatorname{Var}(I_f)=\int_0^Tf(t)^2dt,
$$

$$
\operatorname{Var}(I_g)=\int_0^Tg(t)^2dt,
$$

$$
\operatorname{Cov}(I_f,I_g)=\int_0^Tf(t)g(t)dt.
$$

联合 Gaussian 下，独立等价于 covariance 为0。因此

$$
I_f\perp I_g
\quad\Longleftrightarrow\quad
\langle f,g\rangle_{L^2}=0.
$$

取 $f(t)=1,g(t)=t$：

$$
\operatorname{Var}(I_f)=T,
\quad
\operatorname{Var}(I_g)=\frac{T^3}{3},
\quad
\operatorname{Cov}(I_f,I_g)=\frac{T^2}{2}.
$$

故 covariance matrix 为

$$
\begin{pmatrix}
T&T^2/2\\
T^2/2&T^3/3
\end{pmatrix}.
$$

Gaussian conditioning 给

$$
I_g\mid I_f=b
\sim
\mathcal N\left(
\frac{T}{2}b,
\frac{T^3}{12}
\right).
$$

若 $g$ 换成随机 adapted $G_t$，在平方可积条件下仍有

$$
\mathbb E\int G\,dW=0,
\qquad
\mathbb E\left(\int G\,dW\right)^2
=\mathbb E\int G^2dt.
$$

与 deterministic $f$ 的 covariance isometry 也可保留适当形式。但积分通常不再 Gaussian，所以“零 covariance 推出独立”和 Gaussian conditional formula 不再自动成立。

### DYN-ITO-B02

逐步恒等式

$$
W_{t_{i+1}}^2-W_{t_i}^2
=2W_{t_i}\Delta_iW+(\Delta_iW)^2
$$

给

$$
L_\Pi
=
\frac12W_T^2-\frac12\sum_i(\Delta_iW)^2.
$$

Brownian quadratic variation 沿 deterministic mesh-zero partitions 在 $L^2$ 中趋于 $T$，所以

$$
L_\Pi
\xrightarrow{L^2}
\frac12(W_T^2-T).
$$

梯形和满足精确 telescope：

$$
\begin{aligned}
S_\Pi
&=
\frac12\sum_i(W_{t_i}+W_{t_{i+1}})
(W_{t_{i+1}}-W_{t_i})\\
&=\frac12(W_T^2-W_0^2)
=\frac12W_T^2.
\end{aligned}
$$

因此其 convergence 是平凡的 pathwise equality。

Itô integral 的均值为0。由于 $W_T\sim\mathcal N(0,T)$，

$$
\operatorname{Var}(W_T^2)=2T^2.
$$

故

$$
\operatorname{Var}\left(\int_0^TW_tdW_t\right)
=\frac14(2T^2)=\frac{T^2}{2}.
$$

Itô isometry 给同一答案：

$$
\mathbb E\left(\int_0^TW_tdW_t\right)^2
=\int_0^T\mathbb E[W_t^2]dt
=\int_0^Tt\,dt
=\frac{T^2}{2}.
$$

Stratonovich integral 为

$$
\int_0^TW_t\circ dW_t=\frac12W_T^2,
$$

且

$$
\int_0^TW_t\circ dW_t
-
\int_0^TW_tdW_t
=\frac T2.
$$

当 $T=2$：

$$
\int_0^2W_tdW_t=\frac12(W_2^2-2),
$$

$$
\int_0^2W_t\circ dW_t=\frac12W_2^2,
$$

correction 为1，Itô integral variance 为2。

ordinary chain rule 会预言 $d(W^2/2)=W\,dW$，从而漏掉 $dt/2$。一个非零 correction 已足以否定其无条件适用。

### DYN-ITO-B03

一维 Itô formula：

$$
df(t,X_t)
=
\left(f_t+a_tf_x+\frac12b_t^2f_{xx}\right)dt
+b_tf_xdW_t.
$$

对 $f(x)=x^3$：

$$
d(X_t^3)
=
\left(3X_t^2a_t+3X_tb_t^2\right)dt
+3X_t^2b_tdW_t.
$$

对 $f(x)=e^{\lambda x}$：

$$
d(e^{\lambda X_t})
=
e^{\lambda X_t}
\left(
\lambda a_t+\frac12\lambda^2b_t^2
\right)dt
+\lambda b_te^{\lambda X_t}dW_t.
$$

对 $f(t,x)=tx^2$，有

$$
f_t=x^2,\quad f_x=2tx,\quad f_{xx}=2t.
$$

所以

$$
d(tX_t^2)
=
\left[
X_t^2+2tX_ta_t+tb_t^2
\right]dt
+2tX_tb_tdW_t.
$$

若

$$
dY_t=c_tdt+d_tdW_t,
$$

则 product rule 给

$$
d(X_tY_t)
=X_tdY_t+Y_tdX_t+d[X,Y]_t,
$$

且

$$
d[X,Y]_t=b_td_tdt.
$$

因此

$$
d(XY)
=
(Xc+Ya+bd)dt+(Xd+Yb)dW.
$$

取 $X=W$：

$$
d(W_t^2-t)=2W_tdW_t.
$$

又

$$
d(W_t^3)=3W_t^2dW_t+3W_tdt,
$$

$$
d(3tW_t)=3W_tdt+3tdW_t,
$$

故

$$
d(W_t^3-3tW_t)
=3(W_t^2-t)dW_t.
$$

二者均为 local martingale。在任意有限 $T$ 上，Brownian 有全部 Gaussian moments；对应 integrands 满足所需平方可积性，例如

$$
\mathbb E\int_0^T W_t^2dt<\infty,
$$

$$
\mathbb E\int_0^T(W_t^2-t)^2dt<\infty.
$$

故 stochastic integrals 是 square-integrable martingales，两个过程为 true martingales。

## C. SDE 解、经典模型与多维公式

### DYN-ITO-C01

对 $f(x)=\log x$：

$$
d\log X_t
=
\frac1{X_t}dX_t
-\frac12\frac1{X_t^2}(dX_t)^2.
$$

由于 $(dX_t)^2=\sigma^2X_t^2dt$，

$$
d\log X_t
=
\left(\mu-\frac12\sigma^2\right)dt+\sigma dW_t.
$$

积分并指数化：

$$
X_t
=x_0
\exp\left[
\left(\mu-\frac12\sigma^2\right)t+\sigma W_t
\right].
$$

利用 Gaussian MGF：

$$
\mathbb E[X_t]=x_0e^{\mu t},
$$

$$
\mathbb E[X_t^2]
=x_0^2e^{2\mu t+\sigma^2t},
$$

$$
\operatorname{Var}(X_t)
=x_0^2e^{2\mu t}(e^{\sigma^2t}-1).
$$

对 $s\le t$，条件于 $\mathcal F_s$：

$$
\mathbb E[X_t\mid\mathcal F_s]
=X_se^{\mu(t-s)}.
$$

于是

$$
\mathbb E[X_sX_t]
=e^{\mu(t-s)}\mathbb E[X_s^2]
=x_0^2e^{\mu(s+t)+\sigma^2s}.
$$

所以

$$
\operatorname{Cov}(X_s,X_t)
=x_0^2e^{\mu(s+t)}
\left(e^{\sigma^2s}-1\right).
$$

exact solution 是正数乘指数，故 almost surely 对所有有限 $t$ 为正。

EM step：

$$
X_{n+1}=X_n(1+\mu h+\sigma\sqrt h Z_n).
$$

条件于 $X_n>0$，一步变负概率是

$$
\mathbb P(X_{n+1}<0\mid X_n>0)
=
\Phi\left(
-\frac{1+\mu h}{|\sigma|\sqrt h}
\right),
$$

当 $\sigma\ne0$。

Itô 转 Stratonovich 使用

$$
a_S(x)=a_I(x)-\frac12b(x)b'(x).
$$

这里 $b(x)=\sigma x$，故

$$
dX_t
=
\left(\mu-\frac12\sigma^2\right)X_tdt
+\sigma X_t\circ dW_t.
$$

对纯 multiplicative noise：

$$
dX=\sigma XdW
\quad\Rightarrow\quad
X_t=X_0e^{\sigma W_t-\sigma^2t/2},
\quad
\mathbb E[X_t]=X_0.
$$

而

$$
dX=\sigma X\circ dW
\quad\Rightarrow\quad
X_t=X_0e^{\sigma W_t},
\quad
\mathbb E[X_t]=X_0e^{\sigma^2t/2}.
$$

### DYN-ITO-C02

重写为

$$
dX_t+\kappa X_tdt=\kappa mdt+\sigma dW_t.
$$

乘 $e^{\kappa t}$：

$$
d(e^{\kappa t}X_t)
=\kappa me^{\kappa t}dt+\sigma e^{\kappa t}dW_t.
$$

所以对 $s<t$：

$$
X_t
=m+(X_s-m)e^{-\kappa(t-s)}
+\sigma\int_s^te^{-\kappa(t-u)}dW_u.
$$

给定 $X_s=x$，最后 stochastic integral 是 mean-zero Gaussian，variance 为

$$
\sigma^2\int_s^te^{-2\kappa(t-u)}du
=
\frac{\sigma^2}{2\kappa}
\left(1-e^{-2\kappa(t-s)}\right).
$$

因此

$$
X_t\mid X_s=x
\sim
\mathcal N\left(
m+(x-m)e^{-\kappa(t-s)},
\frac{\sigma^2}{2\kappa}
(1-e^{-2\kappa(t-s)})
\right).
$$

令 $t-s\to\infty$ 得 stationary law：

$$
\pi=\mathcal N\left(m,\frac{\sigma^2}{2\kappa}\right).
$$

若 $X_0\sim\pi$，过程 stationary，且

$$
\operatorname{Cov}(X_s,X_t)
=
\frac{\sigma^2}{2\kappa}e^{-\kappa|t-s|}.
$$

EM：

$$
X_{n+1}
=
(1-\kappa h)X_n+\kappa hm+\sigma\sqrt h Z_n.
$$

中心化 $Y_n=X_n-m$：

$$
Y_{n+1}=(1-\kappa h)Y_n+\sigma\sqrt hZ_n.
$$

存在有限 stationary variance 需

$$
|1-\kappa h|<1
\quad\Longleftrightarrow\quad
0<\kappa h<2.
$$

令 stationary variance 为 $v_h$：

$$
v_h=(1-\kappa h)^2v_h+\sigma^2h,
$$

所以

$$
v_h
=\frac{\sigma^2h}{1-(1-\kappa h)^2}
=\frac{\sigma^2}{2\kappa-\kappa^2h}.
$$

它大于 exact $\sigma^2/(2\kappa)$，并在 $h\to0$ 时收敛。OU 同时有 exact transition、fast mean reversion 与长期 Gaussian invariant law，故可分开检查 stability、transient strong error 和 invariant-measure bias。

### DYN-ITO-C03

对 $f(x)=c^\top x$，Hessian 为0：

$$
d(c^\top X_t)
=c^\top AX_tdt+c^\top BdW_t.
$$

对 $f(x)=\|x\|^2=x^\top x$：

$$
\nabla f=2x,\qquad\nabla^2f=2I.
$$

所以

$$
d\|X_t\|^2
=
\left(
2X_t^\top AX_t+\operatorname{tr}(BB^\top)
\right)dt
+2X_t^\top BdW_t.
$$

令 $m_t=\mathbb E[X_t]$，stochastic integral 期望为0：

$$
\dot m_t=Am_t.
$$

对 $M_t=\mathbb E[X_tX_t^\top]$，matrix product rule 给

$$
\dot M_t=AM_t+M_tA^\top+BB^\top.
$$

协方差 $P_t=M_t-m_tm_t^\top$ 满足同样的非齐次 Lyapunov ODE：

$$
\dot P_t=AP_t+P_tA^\top+BB^\top.
$$

Generator：

$$
\mathcal Lf(x)
=(Ax)^\top\nabla f(x)
+\frac12\operatorname{tr}(BB^\top\nabla^2f(x)).
$$

若 $A$ Hurwitz，stationary covariance $P_\infty$ 是

$$
AP_\infty+P_\infty A^\top+BB^\top=0
$$

的唯一 PSD 解。

若 $Q\in\mathbb R^{m\times m}$ 正交，

$$
(BQ)(BQ)^\top=BB^\top,
$$

所以 generator 与 Markov law 相同。若同时把 Brownian motion 旋转为 $Q^\top W$，也可构造等价 noise representation。

但固定同一个 coordinate-wise $W$ 时，$B\,dW$ 与 $BQ\,dW$ 通常不逐路径相同。相同 $BB^\top$ 决定局部 covariance/generator，不决定某个指定 noise-coordinate coupling。

## D. 适定性与数值分析

### DYN-ITO-D01

**(a)** $-\tanh x$ 的 derivative 绝对值至多1；$1+\frac12\sin x$ 的 derivative 绝对值至多 $1/2$。两者 global Lipschitz 且 bounded，故满足 linear growth。标准 theorem 直接适用。

**(b)** $x^3$ smooth，故 local Lipschitz；derivative $3x^2$ 无界，所以不 global Lipschitz。并且 $|x|^3$ 违反 linear growth。标准 global theorem 不能直接使用。向外 superlinear drift 还提示 explosion 风险，需要 Feller/Lyapunov 等独立分析。

**(c)** $-x^3$ 仍只 local Lipschitz且违反 linear growth，故同一标准 theorem 仍不能直接使用。但

$$
2x(-x^3)+1=-2x^4+1
$$

在大 $|x|$ 时强烈向内。取 $V(x)=x^2$ 的 generator 可建立 dissipative moment bound，从而有机会证明 nonexplosion。符号改变了动力学，尽管 growth order 相同。

**(d)** ReLU global 1-Lipschitz 且 linear growth。$|x|^{1/2}$ 在0附近不是 local Lipschitz，只是 $1/2$-Hölder。因此普通 global-Lipschitz theorem 不适用。不能由此直接断言 nonuniqueness；一维 Yamada–Watanabe 型条件可在某些 $1/2$-Hölder diffusion 下给 pathwise uniqueness，需调用对应定理。

逻辑上：

$$
\text{充分条件失败}
\not\Rightarrow
\text{结论失败}.
$$

它只表示当前 theorem 无法认证。

Neural drift 的 global-control 设计包括：

1. 对每层做 spectral normalization，控制 global Lipschitz constant；
2. 用 bounded activation/output，例如 $\tanh$ envelope；
3. 参数化 dissipative drift
   $$
   f_\theta(x)=-\lambda x+r_\theta(x)
   $$
   并约束 $x^\top r_\theta(x)$；
4. 对 diffusion 做 bounded/linear-growth parameterization；
5. 用 Lyapunov loss 加形式验证或全局 bound；
6. 将 unconstrained network 限制在 compact invariant domain 并严谨处理 boundary。

### DYN-ITO-D02

GBM exact terminal：

$$
X_T
=X_0\exp\left[
(\mu-\sigma^2/2)T+\sigma W_T
\right].
$$

EM terminal 是

$$
X_N
=X_0\prod_{n=0}^{N-1}
(1+\mu h+\sigma\Delta W_n),
\qquad Nh=T.
$$

Strong error 必须让 product 与 exact exponential 使用同一组 increments，且 $W_T=\sum_n\Delta W_n$。

利用 increment mean zero 与 independence：

$$
\mathbb E[X_{n+1}\mid X_n]
=X_n(1+\mu h),
$$

故

$$
\mathbb E[X_N]=X_0(1+\mu h)^N.
$$

用 $N=T/h$：

$$
\begin{aligned}
(1+\mu h)^{T/h}
&=
\exp\left[
\frac{T}{h}\log(1+\mu h)
\right]\\
&=
\exp\left[
\mu T-\frac12\mu^2Th+O(h^2)
\right].
\end{aligned}
$$

所以 weak mean bias 的首项是

$$
\left|
\mathbb E[X_N]-\mathbb E[X_T]
\right|
=
\frac12X_0e^{\mu T}\mu^2T\,h+O(h^2).
$$

一般 multiplicative-noise EM 缺少 Milstein 中

$$
\frac12bb'
\left((\Delta W)^2-h\right)
$$

这一 $L^2$ 尺度为 $O(h)$ 的局部随机项；跨 $T/h$ 步累积后得到典型 strong order $1/2$。严格结论仍需 theorem 条件。

Nested coupling：先采

$$
\delta W_k\sim\mathcal N(0,h_{\min}),
$$

然后 coarse increment 定义为 block sum

$$
\Delta W_j^{(h)}
=\sum_{k\in\mathcal B_j}\delta W_k.
$$

这样所有 resolution 表示同一 Brownian path。若每个网格独立重抽，差值包含两条独立 SDE path 的 intrinsic variance；即使 scheme exact，差也不会趋于0。

Weak audit 可取：

$$
\varphi_1(x)=x,\qquad
\varphi_2(x)=x^2,\qquad
\varphi_3(x)=\mathbf1_{\{x>K\}}
$$

或平滑化 indicator。前两者检查 moments，第三个检查 tail probability；non-smooth test function 的理论 order 可能不同。

Monte Carlo standard error 约按 $M^{-1/2}$ 消失，是 sampling uncertainty；time-discretization bias 按 $h^q$ 消失，是 scheme error。报告应使用 replicate/batch estimate 给 MC error bar，并在多个 $h$ 上拟合 bias。

有限 $h$ 时 EM 有小概率变负；当 $h\to0$ 时该 defect 可消失到不影响某类 weak test functions 的极限。这不表示 positivity-sensitive finite-step application 可以忽略它。

### DYN-ITO-D03

Scalar Milstein：

$$
X_{n+1}
=X_n+a(X_n)h+b(X_n)\Delta W_n
+\frac12b(X_n)b'(X_n)
\left[(\Delta W_n)^2-h\right].
$$

因为

$$
\mathbb E[(\Delta W_n)^2-h]=0,
$$

中心化使 correction 不偷偷加入 $O(h)$ mean drift；它描述 quadratic variation 围绕其 compensator 的 fluctuation。

GBM 中 $a(x)=\mu x,b(x)=\sigma x,b'(x)=\sigma$：

$$
X_{n+1}
=X_n
\left[
1+\mu h+\sigma\Delta W_n
+\frac12\sigma^2
\left((\Delta W_n)^2-h\right)
\right].
$$

若 $b$ constant，则 $b'=0$，Milstein 与 EM 公式相同。对 additive noise，EM 因结构可拥有高于一般 multiplicative case 的 strong rate。

在标准充分光滑条件下：

| 方法 | 典型 strong order | 典型 weak order |
|---|---:|---:|
| Euler–Maruyama | $1/2$ | $1$ |
| scalar Milstein | $1$ | $1$ |

Milstein 的优势主要是 strong order；若要更高 weak order 需专门 weak schemes。

多维 noise 下 stochastic Taylor 出现

$$
I_{jk}
=
\int_{t_n}^{t_{n+1}}
\int_{t_n}^{s}dW_u^j\,dW_s^k.
$$

当 $j\ne k$，其 antisymmetric 部分与 Lévy area 有关，不能只由 terminal $\Delta W$ 恢复。若 diffusion vector fields 的 Lie brackets 为0，即概念上 commute，某些 iterated-integral combinations 可简化；仍需针对所用 scheme 验证精确条件。

不能只用 endpoint RMSE 的 benchmark 可加入 barrier hitting：

$$
\tau_c=\inf\{t:X_t\ge c\}.
$$

报告 endpoint strong error、weak moments、$\mathbb P(\tau_c\le T)$ 和 hitting-time bias，并对网格间 crossing 使用 bridge correction。

## E. AI、梯度与研究审计

### DYN-ITO-E01

写

$$
F_n(X,\theta)
=X+f_\theta(t_n,X)h+g_\theta(t_n,X)\Delta W_n.
$$

令 $S_n=\partial_\theta X_n$。Chain rule 给

$$
\begin{aligned}
S_{n+1}
&=
S_n
+\left[
\partial_xf_\theta(t_n,X_n)S_n
+\partial_\theta f_\theta(t_n,X_n)
\right]h\\
&\quad+
\left[
\partial_xg_\theta(t_n,X_n)S_n
+\partial_\theta g_\theta(t_n,X_n)
\right]\Delta W_n.
\end{aligned}
$$

若初值依赖参数，$S_0=\partial_\theta X_0$；否则 $S_0=0$。

对 differentiable terminal loss：

$$
\partial_\theta J_h
=
\mathbb E\left[
\nabla\ell(X_N)^\top S_N
\right].
$$

Forward sensitivity 成本随 parameter dimension 增长，适合参数少、输出多或需要完整 Jacobian。Reverse-mode backprop 成本更接近 scalar loss 的一次反传，适合参数很多，但需存储/重建 trajectory 与 noise。

Centered finite difference：

$$
g_{\mathrm{FD}}
=
\frac{
\widehat J_h(\theta+\varepsilon)
-
\widehat J_h(\theta-\varepsilon)
}{2\varepsilon}.
$$

正负扰动必须复用同一 Brownian increments 与同一 initial samples，即 common random numbers；否则 $O(M^{-1/2})$ Monte Carlo noise 被除以 $\varepsilon$ 放大。

该检验只比较

$$
g_{\mathrm{AD}}
\quad\text{与}\quad
\nabla_\theta J_h.
$$

它不能证明

$$
\nabla_\theta J_h
\to\nabla_\theta J
$$

的速度或交换 derivative/expectation/limit 的合法性。

Continuous-gap audit 应在 nested Brownian paths 上计算

$$
\left(
\mathbb E
\|
G_h(\omega)-G_{\mathrm{ref}}(\omega)
\|^2
\right)^{1/2}
$$

或 expectation bias，其中 $G_{\mathrm{ref}}$ 来自 exact solution、经验证的高精度 method 或独立 theorem；随后对 $h$ 做 log–log slope。

Adaptive solver 的 noise reconstruction 至少保持：

1. 子 increments 之和等于父 increment；
2. 条件 covariance 符合 Brownian bridge；
3. 求值/rejection 顺序改变时，同一 time query 返回同一 path value；
4. 正反向/adjoint 所需 noise 与 forward path 一致。

Backprop-through-solver 对实际 discrete program 的梯度直接，但内存随 step count 增长。Stochastic adjoint 可减少存储，却要求正确的 backward stochastic calculus、noise reconstruction、coefficient regularity与solver convergence。两者都仍有 finite-tolerance gradient error。

### DYN-ITO-E02

公式

$$
X_t=\alpha(t)X_0+\sigma(t)\varepsilon
$$

在固定 $t$ 时定义 conditional marginal sampler

$$
\mathcal L(X_t\mid X_0).
$$

若未说明不同 $t$ 的 $\varepsilon$ 如何 coupling，它没有定义 FDD 或 path law。

在有限网格 $t_1,\ldots,t_n$ 上可构造：

1. shared noise：
   $$
   X_{t_i}^{\mathrm{shared}}
   =\alpha_iX_0+\sigma_i\varepsilon;
   $$
2. independent-time noise：
   $$
   X_{t_i}^{\mathrm{ind}}
   =\alpha_iX_0+\sigma_i\varepsilon_i,
   \qquad
   \varepsilon_i\overset{iid}{\sim}\mathcal N(0,I).
   $$

每个固定 $t_i$ 的 conditional marginal 相同，但 conditional cross-time covariance 分别为

$$
\operatorname{Cov}(X_{t_i},X_{t_j}\mid X_0)
=\sigma_i\sigma_jI
$$

与0。故 increment variance 和 path regularity完全不同。

恢复 Markov diffusion 至少需要 transition kernels 或等价的 drift、diffusion、Brownian noise、filtration、initial law 和 solution uniqueness；还需说明 coefficient 条件确保所写 SDE 真正定义过程。

给出

$$
dX=fdt+g\,dW
$$

后，本章可审计：

- Itô/Stratonovich；
- dimension 与 local covariance $gg^\top$；
- adaptedness 与 $\sqrt{dt}$ scaling；
- existence/uniqueness 的充分条件；
- EM/Milstein 更新；
- strong/weak numerical target；
- nested Brownian coupling 与 gradient target。

仍需后续章节处理：

- generator adjoint 与 Fokker–Planck；
- probability-flow ODE 的同 marginal 条件；
- reverse-time drift；
- score 的角色与 regularity；
- learned reverse process 的分布误差。

训练/采样报告应至少分账：

| 误差 | 对象 | 检查 |
|---|---|---|
| score/model error | learned vs population coefficient | held-out denoising/score proxy、model ablation |
| approximation error | function class/optimization | capacity、seed、optimization residual |
| solver bias | finite $h$/tolerance | refinement 与 reference solver |
| Monte Carlo error | finite trajectories | standard error/confidence interval |
| path mismatch | multi-time law/event | covariance、signature、hitting metrics |

Probability-flow ODE 若在条件成立时与 SDE 共享 one-time marginals，仍有 deterministic conditional trajectory，而 reverse SDE 保留 Brownian path randomness；其 FDD、quadratic variation 和 path functionals不同。

### DYN-ITO-E03

一个合格方案可取

$$
dX_t
=
\left[-\lambda X_t+r_\theta(t,X_t)\right]dt
+\operatorname{diag}
\left(
\sigma_{\min}+\operatorname{softplus}
(q_\theta(t,X_t))
\right)dW_t.
$$

选择 Itô interpretation。若论文以 Stratonovich 实现，必须用

$$
a_I^i
=a_S^i
+\frac12\sum_{j,k}B_{kj}\partial_{x_k}B_{ij}
$$

记录等价 drift。

可复现方案如下。

**数学卡**

- $X\in\mathbb R^d,W\in\mathbb R^m$；
- initial law、filtration、Itô integral；
- spectral-normalized $r_\theta,q_\theta$；
- diffusion 上下界与 linear growth；
- dissipativity
  $$
  x^\top a_\theta(t,x)
  \le C-\gamma\|x\|^2
  $$
  作为 nonexplosion/moment 证据。

**Noise 与 solver**

- counter-based PRNG key 包含 run/trajectory/noise-coordinate；
- Brownian tree 由 time interval key 决定；
- adaptive rejection 不改变既有 path query；
- 保存 solver、tolerance、dtype、NFE、accepted/rejected steps；
- threshold event 使用 Brownian bridge 或更高精度 reference。

**三类数值门**

1. Strong：
   $$
   (\mathbb E\|X_T^h-X_T^{\rm ref}\|^2)^{1/2};
   $$
2. Weak：mean、second moment、smooth tail proxy；
3. Path-event：
   $\mathbb P(\tau_c\le T)$、maximum 与 hitting-time distribution。

**梯度门**

1. 固定 discrete trajectory samples，AD 对 centered FD；
2. nested refinement 下 $\nabla J_h-\nabla J_{\rm ref}$；
3. common random numbers；
4. 报告 FD step-size sweep，排除 cancellation/truncation 两端。

**Baselines**

- OU exact transition 检查 additive noise；
- GBM exact terminal 检查 multiplicative noise；
- fixed-step EM/Milstein 与 adaptive solver；
- zero-diffusion neural ODE boundary。

**Ablations**

- solver family 与 tolerance；
- Itô/Stratonovich conversion 开/关；
- noise dimension $m$；
- drift spectral norm/dissipativity；
- diffusion floor/cap；
- bridge event correction；
- backprop vs stochastic adjoint。

**停止条件**

- refinement 不降 error；
- same-time Brownian query 不一致；
- FD gradient error 超阈值；
- moment/explosion/NaN rate 超阈值；
- event estimate 被 MC interval 完全淹没；
- conclusion 对 solver/tolerance 极度敏感。

**可证伪主张**

“在预注册 tolerance range 内，相对 reference，terminal weak bias 小于1%，hitting probability absolute error 小于0.02，discrete gradient relative error 小于 $10^{-5}$。”

**不允许越级**

- endpoint marginal 相近不能称 path law 正确；
- discrete FD 通过不能称 continuous adjoint 正确；
- finite benchmark 优胜不能称任意 SDE 可识别；
- empirical no-explosion 不能替代理论 nonexplosion。

Research acceptance checklist：

~~~text
[ ] SDE dimension, filtration, initial law, Ito/Stratonovich fixed
[ ] drift/diffusion regularity and nonexplosion evidence
[ ] equivalent drift conversion independently checked
[ ] Brownian tree query/rejection/device invariance tested
[ ] OU and GBM exact baselines passed
[ ] strong, weak, and hitting-event refinement curves reported
[ ] bridge/event policy reported
[ ] J_h gradient passed common-random-number finite difference
[ ] continuous/reference gradient gap decreases under refinement
[ ] MC confidence intervals separated from solver bias
[ ] solver/tolerance/noise/regularization ablations complete
[ ] failure stop conditions evaluated
[ ] claims restricted to measured object
[ ] density claims deferred to DYN-11
[ ] reverse/score claims deferred to DYN-12
~~~
