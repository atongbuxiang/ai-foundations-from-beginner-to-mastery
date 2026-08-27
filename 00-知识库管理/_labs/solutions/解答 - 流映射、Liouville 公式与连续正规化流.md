---
type: solution
status: draft
area: [math/ode, math/dynamical-systems, math/probability, ai/generative-modeling]
topic: "流映射、Liouville 公式与连续正规化流"
exercise: "[[习题 - 流映射、Liouville 公式与连续正规化流]]"
related: ["[[流映射、Liouville 公式与连续正规化流]]", "[[ODE、动力系统与 SDE MOC]]", "[[练习与测验 MOC]]", "[[实验 - 流映射、Liouville 与随机迹审计]]"]
created: 2026-08-19
updated: 2026-08-19
---

# 解答 - 流映射、Liouville 公式与连续正规化流

> [!important] 判断顺序
> 以下解答始终按“IVP 是否定义良好 → exact flow 在哪个集合上 → Jacobian/volume → density → finite solver → stochastic trace/gradient”作答。只要跳过其中一层，“可逆”“精确”“无偏”就很容易越界。

## A. 定义、条件与对象分层

### DYN-FLOW-A01

**Solution curve** $x(t;s,x_s)$ 是固定初始时间和初值后的一条候选轨迹。Existence 只保证至少有一条；uniqueness 才使符号成为单值对象。

在一批初值共享的存在区间上定义

$$
\phi_{s,t}(x_s)=x(t;s,x_s).
$$

非自治系统需保留 $s,t$ 两个时间。取 $s\le u\le t$，令 $y=\phi_{s,u}(x_s)$。轨迹 $x(r;s,x_s)$ 与 $x(r;u,y)$ 都在 $u$ 时刻经过 $y$，由 uniqueness 在共同区间相同，故

$$
\phi_{u,t}(\phi_{s,u}(x_s))=\phi_{s,t}(x_s).
$$

uniqueness 正好用在“同一中间初值只允许一条延续”。若只有 existence，可能选择不同分支，composition 不是单值等式。

对自治系统，时间平移允许写 $\phi_t=\phi_{0,t}$。若只前向存在，得到

$$
\phi_{t+s}=\phi_t\circ\phi_s,
\qquad s,t\ge0,
$$

即 semigroup。只有解对正负时间都全局存在，才有

$$
\phi_{-t}=\phi_t^{-1}
$$

和 global one-parameter group。

定义域应写成

$$
D_{s,t}=\{x_s:\text{从 }(s,x_s)\text{ 出发的解存在到 }t\}.
$$

uniqueness 给

$$
\phi_{s,t}:D_{s,t}\to\phi_{s,t}(D_{s,t})
$$

的单射。若 $f$ 对状态 $C^1$ 并有相应初值可微性，则 $D\phi$ 存在；Liouville 给 determinant 非零，于是 inverse function theorem 给局部微分同胚。若反向解存在，可称 diffeomorphism onto image。只有像等于整个 $\mathbb R^d$ 时才是全空间 global diffeomorphism。

Pushforward 定义为

$$
((\phi_{s,t})_\#\mu_s)(B)
=\mu_s(\phi_{s,t}^{-1}(B)).
$$

它只需映射可测，不要求 density；写 Jacobian density formula 才需同维、绝对连续与换元条件。

数值 map $\Psi_h$ 是算法一步，不是 exact $\phi_{t,t+h}$。它可有不同 composition、Jacobian、可逆性和 orientation。

责任表为：

| 条件 | 主要责任 | 不自动给出 |
|---|---|---|
| existence | 至少有轨迹 | 单值 flow |
| uniqueness | 单值演化、composition、no crossing | 可微性、全局存在 |
| $C^1$ 初值依赖 | variational equation、local differential structure | onto全空间 |
| forward completeness | 任意未来时间可走 | 任意过去时间可回 |
| two-sided completeness | 正负时间全局 flow group | 数值程序精确可逆 |

### DYN-FLOW-A02

$D_xf(t,x)$ 是 vector field 在一个时空点的局部线性化；$D\phi_{s,t}(x_s)$ 是把初始切向量搬到终点的累计 propagator；$D_\theta x(t)$ 是参数 sensitivity，满足带 $D_\theta f$ forcing 的方程。三者形状和对象均可能不同。

Determinant 是有向总体积倍数；trace 是线性算子的对角和；divergence 是 $\operatorname{tr}D_xf$；singular values 是各主轴的长度倍数。Liouville 只把 singular values 的乘积压成 divergence 积分，不能恢复每个方向。

沿轨迹全导数为

$$
\frac d{dt}\log p_t(x_t)
=\partial_t\log p_t(x_t)
+\nabla\log p_t(x_t)^Tf(t,x_t).
$$

固定空间点偏导只含第一项。把二者混淆会漏掉 advection。

Local volume contraction 是 $\nabla\cdot f<0$；trajectory stability 要控制单个扰动或 Lyapunov 函数。前者是 trace 信息，后者通常需 full Jacobian/symmetric part/长期动力学。

Density $p$ 是相对 Lebesgue measure 的 Radon–Nikodym derivative；落在曲线/曲面上的 singular law 在 ambient space 中没有普通 density。Pushforward measure 仍定义良好，但不能机械写 ambient-dimensional determinant density。

Finite formula：

$$
p_t(\phi_{s,t}(x))\det D\phi_{s,t}(x)=p_s(x).
$$

对时间微分才得到 instantaneous formula：

$$
\frac d{dt}\log p_t(x_t)=-\nabla\cdot f(t,x_t).
$$

连续性方程

$$
\partial_t p+\nabla\cdot(pf)=0
$$

是固定坐标的 Eulerian PDE；沿 characteristics 展开它可恢复上式，但 PDE 的弱形式和边界通量更广。

Divergence 为零但持续运动：二维 rotation

$$
f(x,y)=(-y,x),
\qquad \nabla\cdot f=0.
$$

Divergence 为负但某方向暂时拉伸：

$$
A=\begin{bmatrix}-1&8\\0&-2\end{bmatrix},
\qquad \operatorname{tr}A=-3,
$$

其中 shear 可使某些向量 norm 先增大，面积仍按 $e^{-3t}$ 缩小。

### DYN-FLOW-A03

一张合格 card 可写：

```yaml
task: train / likelihood / sample
state: z in R^d; context c fixed; optional k augmented coordinates
time: [0, 1]; direction declared per task
base: standard Gaussian; data: dequantization and scaling specified
field: architecture, activation, spectral/weight regularization, time embedding
divergence: exact / analytic structured / Hutchinson
probe: Rademacher; m_train=1; m_eval=32; one probe fixed per trajectory
solver: method, atol, rtol, max_step, precision, event policy
gradient: discrete / continuous adjoint / checkpoint; probe reuse declared
cost: accepted/rejected steps, NFE, VJP/JVP, backward solve, wall time, memory
errors: reference state/logp, tolerance sweep, probe SE, round trip, FD gradient
claims: existence/invertibility domain, support assumptions, augmentation semantics
```

只写 `dopri5, rtol=1e-5, NFE=80` 缺少至少：atol和state scaling、trace成本、probe语义、accepted/rejected计数、precision、time direction、base/data preprocessing、gradient对象、checkpoint、hardware/batch、达到的误差以及失败率。相同 NFE 的一次 RHS 可能是一次普通 forward，也可能含多次 VJP，不能据此复现 wall time 或 likelihood。

## B. 精确流、Jacobian 与密度手算

### DYN-FLOW-B01

方程

$$
x'+2x=e^t
$$

的一个 particular solution 是 $e^t/3$。因此

$$
\boxed{
\phi_{s,t}(x_s)
=e^{-2(t-s)}\left(x_s-\frac{e^s}{3}\right)
+\frac{e^t}{3}.
}
$$

令 $\alpha_{s,t}=e^{-2(t-s)}$、$q(t)=e^t/3$，则

$$
\phi_{s,t}(x)=\alpha_{s,t}(x-q(s))+q(t).
$$

由于 $\alpha_{u,t}\alpha_{s,u}=\alpha_{s,t}$，

$$
\begin{aligned}
\phi_{u,t}(\phi_{s,u}(x))
&=\alpha_{u,t}[\alpha_{s,u}(x-q(s))+q(u)-q(u)]+q(t)\\
&=\alpha_{s,t}(x-q(s))+q(t)\\
&=\phi_{s,t}(x).
\end{aligned}
$$

对初值求导：

$$
J_{s,t}=e^{-2(t-s)}.
$$

因为 $\partial f/\partial x=-2$，Liouville 也给

$$
J_{s,t}=\exp\int_s^t(-2)d\tau=e^{-2(t-s)}.
$$

若 $X_s\sim\mathcal N(m_s,\sigma_s^2)$，affine transformation 后

$$
m_t=e^{-2(t-s)}\left(m_s-\frac{e^s}{3}\right)+\frac{e^t}{3},
$$

$$
\sigma_t^2=e^{-4(t-s)}\sigma_s^2.
$$

沿对应点 $x_t=\phi_{s,t}(x_s)$，换元给

$$
\log p_t(x_t)
=\log p_s(x_s)-\log J_{s,t}
=\log p_s(x_s)+2(t-s).
$$

从 Gaussian 公式看，standardized residual 保持：

$$
\frac{x_t-m_t}{\sigma_t}
=\frac{x_s-m_s}{\sigma_s},
$$

而 normalizer $-\log\sigma_t=-\log\sigma_s+2(t-s)$，相同。

反向为

$$
x_s=\frac{e^s}{3}
+e^{2(t-s)}\left(x_t-\frac{e^t}{3}\right).
$$

系数 $e^{-2(t-s)}$ 对任意有限 $s,t\in\mathbb R$ 非零，且 affine map 的像是 $\mathbb R$，所以若方程允许任意正负时间（这里确实允许），它是 $\mathbb R$ 上 global diffeomorphism。

### DYN-FLOW-B02

分离变量得到

$$
\boxed{
\phi_t(x_0)=\frac{x_0}{\sqrt{1+2tx_0^2}},\qquad t\ge0.
}
$$

固定 $t>0$，极限为

$$
\lim_{x_0\to\pm\infty}\phi_t(x_0)
=\pm\frac1{\sqrt{2t}},
$$

故像是

$$
I_t=\left(-\frac1{\sqrt{2t}},\frac1{\sqrt{2t}}\right).
$$

Jacobian：

$$
\boxed{
J_t(x_0)=(1+2tx_0^2)^{-3/2}>0.
}
$$

又 $f'(x)=-3x^2$，所以

$$
\int_0^t f'(x(\tau))d\tau
=-\frac32\log(1+2tx_0^2),
$$

指数化恰得 $J_t$。

若 base 是 standard normal，

$$
\ell_0(x_0)=-\frac{x_0^2}{2}-\frac12\log(2\pi).
$$

因此沿轨迹

$$
\boxed{
\log p_t(\phi_t(x_0))
=-\frac{x_0^2}{2}-\frac12\log(2\pi)
+\frac32\log(1+2tx_0^2).
}
$$

从

$$
x=\frac{x_0}{\sqrt{1+2tx_0^2}}
$$

解得

$$
x_0=\frac{x}{\sqrt{1-2tx^2}},
\qquad |x|<\frac1{\sqrt{2t}}.
$$

并有

$$
\frac{dx_0}{dx}=(1-2tx^2)^{-3/2}.
$$

所以

$$
\boxed{
p_t(x)=
\frac{1}{\sqrt{2\pi}}
\exp\!\left(-\frac{x^2}{2(1-2tx^2)}\right)
(1-2tx^2)^{-3/2}
}
$$

在 $|x|<1/\sqrt{2t}$ 成立，支持外为零。

令 $\delta=1-2tx^2\downarrow0$。density 是

$$
C\delta^{-3/2}\exp\left(-\frac{x^2}{2\delta}\right).
$$

指数衰减快于任意多项式发散，所以 $p_t(x)\to0$。总概率没有堆成边界原子；只是无穷远初值被压到有限边界附近。

该例中 $J>0$ 只给 strictly increasing/local inverse；像仍是 $I_t$ 而非 $\mathbb R$。Gaussian base 的全空间支持经一个非 onto 映射可变成有界支持；“diffeomorphism保持全支持”需要全空间 onto 的额外条件。

### DYN-FLOW-B03

上三角矩阵指数为

$$
\boxed{
M(t)=e^{tA}
=\begin{bmatrix}
e^{-t}&8(e^{-t}-e^{-2t})\\
0&e^{-2t}
\end{bmatrix}.
}
$$

可由直接求解 $x_2(t)=e^{-2t}x_2(0)$，再代入 $x_1'+x_1=8x_2$ 得到。

$$
\operatorname{tr}A=-3,
\qquad
\det M(t)=e^{-3t}.
$$

令

$$
a=e^{-1/2},\quad d=e^{-1},\quad b=8(e^{-1/2}-e^{-1}).
$$

单位正方形四顶点像为

$$
(0,0),\quad(a,0),\quad(b,d),\quad(a+b,d).
$$

两条边向量是 $(a,0)^T$ 与 $(b,d)^T$，面积

$$
|ad|=e^{-3/2},
$$

与 Liouville 完全一致。

对 $v=e_2$，

$$
M(t)v=
\begin{bmatrix}
8(e^{-t}-e^{-2t})\\e^{-2t}
\end{bmatrix},
$$

$$
\|M(t)v\|_2
=\sqrt{64(e^{-t}-e^{-2t})^2+e^{-4t}}.
$$

在 $t=1/2$，第一分量约 $1.9092$、第二分量约 $0.3679$，norm 约 $1.944$，确实大于1。

这不与 eigenvalues $-1,-2$ 矛盾。Eigenvalues 控制 asymptotic modes；非正交 eigenvectors/shear 可产生 finite-time transient growth。

若 $X_0\sim\mathcal N(0,I)$，则

$$
X_t\sim\mathcal N(0,\Sigma_t),
\qquad
\Sigma_t=M(t)M(t)^T.
$$

具体为

$$
\Sigma_t=
\begin{bmatrix}
e^{-2t}+64(e^{-t}-e^{-2t})^2 & 8(e^{-t}-e^{-2t})e^{-2t}\\
8(e^{-t}-e^{-2t})e^{-2t} & e^{-4t}
\end{bmatrix}.
$$

$$
\det\Sigma_t=(\det M(t))^2=e^{-6t}.
$$

沿对应点，log-density correction 为

$$
-\log\det M(t)=3t.
$$

Trace 只给 covariance volume $\det\Sigma_t$；off-diagonal covariance 和主轴长宽比依赖完整 $M(t)M(t)^T$，不能由 $-3$ 重建。

## C. 定理推导与反例

### DYN-FLOW-C01

取方向 $v$ 与扰动轨迹

$$
x_\varepsilon(t)=\phi_{s,t}(x_s+\varepsilon v).
$$

由初值可微性和 chain rule，

$$
\xi(t)=\left.\partial_\varepsilon x_\varepsilon(t)\right|_0
$$

满足

$$
\dot\xi=D_xf(t,x(t))\xi,
\qquad \xi(s)=v.
$$

对所有 $v$ 同时写成

$$
\dot J_{s,t}=D_xf(t,x_t)J_{s,t},
\qquad J_{s,s}=I.
$$

composition law 来自 uniqueness：

$$
\phi_{s,t}=\phi_{u,t}\circ\phi_{s,u}.
$$

对初值用 chain rule：

$$
J_{s,t}(x_s)
=J_{u,t}(x_u)J_{s,u}(x_s).
$$

Jacobi formula 给

$$
\frac d{dt}\log\det J
=\operatorname{tr}(J^{-1}\dot J).
$$

代入 $\dot J=D_xfJ$，用 trace cyclicity：

$$
\operatorname{tr}(J^{-1}D_xfJ)
=\operatorname{tr}(D_xfJJ^{-1})
=\operatorname{tr}D_xf.
$$

从 $s$ 积分且 $\det J_{s,s}=1$：

$$
\det J_{s,t}
=\exp\int_s^t\operatorname{tr}D_xf(\tau,x_\tau)d\tau>0.
$$

因此 derivative 可逆；inverse function theorem 给每一点邻域内的 $C^1$ inverse。它是 local statement，不给像覆盖全空间。全局 surjectivity 还需 backward continuation/properness 等额外信息；$x'=-x^3$ 已是反例。

若 $\phi_{s,t}$ 在所讨论集合上是可逆 $C^1$ map，且 $\mu_s$ 有 Lebesgue density，则 change of variables 给

$$
p_t(\phi_{s,t}(x_s))\det J_{s,t}(x_s)=p_s(x_s).
$$

取 log 并对 $t$ 求导：

$$
\frac d{dt}\log p_t(x_t)
=-\frac d{dt}\log\det J_{s,t}
=-\operatorname{tr}D_xf(t,x_t).
$$

使用链条依次为：初值可微 + chain rule；uniqueness；chain rule；Jacobi formula；trace cyclicity；exponential positivity；inverse function theorem；change of variables。

### DYN-FLOW-C02

写 $A=S+K$，其中 $K=(A-A^T)/2$ 反对称。标量

$$
q=\varepsilon^TK\varepsilon
$$

满足

$$
q=q^T=\varepsilon^TK^T\varepsilon=-q,
$$

故 $q=0$，所以 $\varepsilon^TA\varepsilon=\varepsilon^TS\varepsilon$。

无偏性：

$$
\begin{aligned}
\mathbb E[\varepsilon^TA\varepsilon]
&=\mathbb E\operatorname{tr}(A\varepsilon\varepsilon^T)\\
&=\operatorname{tr}(A\mathbb E\varepsilon\varepsilon^T)\\
&=\operatorname{tr}A.
\end{aligned}
$$

Rademacher 情形，$\varepsilon_i^2=1$：

$$
\varepsilon^TS\varepsilon
=\operatorname{tr}S+2\sum_{i<j}S_{ij}\varepsilon_i\varepsilon_j.
$$

不同 unordered pairs 的乘积在期望下正交，且每项平方期望为1，因此

$$
\operatorname{Var}
=4\sum_{i<j}S_{ij}^2.
$$

Gaussian 情形可正交对角化 $S=Q\Lambda Q^T$。旋转后的 $g=Q^T\varepsilon$ 仍为 standard Gaussian，

$$
g^T\Lambda g=\sum_i\lambda_i g_i^2.
$$

独立且 $\operatorname{Var}(g_i^2)=2$，故

$$
\operatorname{Var}=2\sum_i\lambda_i^2=2\|S\|_F^2.
$$

独立平均用

$$
\operatorname{Var}\left(\frac1m\sum_{k=1}^mY_k\right)
=\frac1{m^2}\sum_k\operatorname{Var}(Y_k)
=\frac{\operatorname{Var}(Y_1)}m.
$$

取 $S=I_d$：Rademacher 每次恰得 $d$，方差0；Gaussian 方差 $2d$。

取

$$
S=\begin{bmatrix}0&M\\M&0\end{bmatrix}.
$$

真实 trace 为0，Rademacher 单 probe 为 $2M\varepsilon_1\varepsilon_2=\pm2M$。当 $M$ 大时每次绝对误差都大，但正负等概率，仍无偏。

训练 likelihood 是 estimator、trajectory、finite solver、nonlinear objective、parameter optimization 和 gradient sampling 的复合。Pointwise conditional trace 无偏只是一层，不能直接推出最终 log-likelihood、density、NLL 或训练后参数无偏。

### DYN-FLOW-C03

由 reverse triangle inequality 和 Lipschitz 性：

$$
\begin{aligned}
\|\Psi_h(x)-\Psi_h(y)\|
&=\|(x-y)+h(f(x)-f(y))\|\\
&\ge\|x-y\|-h\|f(x)-f(y)\|\\
&\ge(1-hL)\|x-y\|.
\end{aligned}
$$

若 $hL<1$，右端对 $x\ne y$ 为正，故单射。

给定 $z$，$\Psi_h(x)=z$ 等价于 fixed point

$$
x=T_z(x):=z-hf(x).
$$

$$
\|T_z(x)-T_z(y)\|\le hL\|x-y\|.
$$

在完备空间 $\mathbb R^d$ 上，$hL<1$ 使 $T_z$ 为 contraction，所以存在唯一 fixed point；即对每个 $z$ 恰有一个 preimage，故满射。

若 $z_i=\Psi_h(x_i)$，前面的下界给

$$
\|\Psi_h^{-1}(z_1)-\Psi_h^{-1}(z_2)\|
\le\frac1{1-hL}\|z_1-z_2\|.
$$

条件不是必要的，例如 $f(x)=x$、任意 $h>0$ 有 $\Psi_h(x)=(1+h)x$ 可逆，但 $hL=h$ 可大于1。

对 $f(x)=-x^3$：

$$
\Psi_h(x)=x-hx^3,
\qquad
\Psi_h'(x)=1-3hx^2.
$$

临界点是

$$
x=\pm\frac1{\sqrt{3h}}.
$$

中间 derivative 正、外侧负，map 出现局部极值并折叠。

一步时长为 $h$ 时，exact flow derivative 为

$$
(1+2h x_0^2)^{-3/2}>0,
$$

永不折叠。随着 $h\to0$，在任意固定有界状态集上 Euler map 逼近 exact flow，且 eventually derivative 保持正；但对全空间，$x$ 可随 $h^{-1/2}$ 增大，任意有限 $h$ 仍会在远处折叠。Local refinement 不能自动给 global uniform topology claim。

## D. 数值实现、实验与程序语义

### DYN-FLOW-D01

解析状态：

$$
x(t)=\frac{x_0}{\sqrt{1+2tx_0^2}}.
$$

因为 $\ell'=3x^2$，

$$
\ell(t)-\ell(0)
=3\int_0^t\frac{x_0^2}{1+2\tau x_0^2}d\tau
=\frac32\log(1+2tx_0^2).
$$

若 base 为 standard normal：

$$
\ell(0)=-\frac{x_0^2}{2}-\frac12\log(2\pi).
$$

因此

$$
\boxed{
\ell(t)=-\frac{x_0^2}{2}-\frac12\log(2\pi)
+\frac32\log(1+2tx_0^2).
}
$$

而

$$
-\log J_t=\frac32\log(1+2tx_0^2),
$$

所以增量相同。

RK4 对增广向量 $y=(x,\ell)$ 使用同一 stage：

$$
F(y)=(-x^3,3x^2).
$$

不要先更新 $x$ 再用另一个网格更新 $\ell$，否则验证的是 splitting program。对 $N$ 与 $2N$ 的误差 $e_N,e_{2N}$，observed order 可估为

$$
p_N=\log_2(e_N/e_{2N}).
$$

在 asymptotic regime 应趋近4；state 和 log-density 要分别计算。State 准确不保证沿轨迹积分的 divergence 准确，也不保证两者误差相关抵消，因此只报 state order 不能验证 NLL。

当误差接近 machine precision，舍入使 slope 失真；若 vector field/augmented equation stiff，显式 RK4 先受 stability 限制而不是显示四阶；若 adaptive tolerance 低于精度/trace noise floor，NFE 可能暴涨而 error 不再下降。

### DYN-FLOW-D02

**整条 trajectory 固定 probe**：给定 $\varepsilon$ 后，RHS 是确定函数

$$
F_\varepsilon(t,z)=(f(t,z),-\varepsilon^TJ_f(t,z)\varepsilon).
$$

若 $f$ 光滑，它也光滑。Rejected trial 重新计算同一点得到同值，classical local error estimator 至少在 conditional ODE 上有通常语义。随机性来自不同 trajectories/probes；forward/backward 可选择复用同一 probe。

**每个 accepted step 重采样**：每段 step 内可视为固定 ODE，但 accepted-step 边界处 RHS 跳变；adaptive controller 同时决定采样时刻，所得程序是 piecewise-random scheme。Rejection 时若 probe 固定到接受为止尚可定义；若重抽则转入第三种。

**每次 RHS evaluation 都重采样**：同一 $(t,z)$ 重算不再相同。Embedded pair 的高低阶差同时含 Monte Carlo noise，不再只估 discretization defect；rejection 也可能因随机数改变而“自愈/恶化”。这不是普通 deterministic adaptive ODE 的直接实现。

小维 protocol 可取 $d=4$ 的已知 dense Jacobian，或 nonlinear field 但自动微分 exact trace 可算。固定：

- dimensions $d=4,16,64$；
- seeds 至少100个独立 replicates；
- probes $m=1,4,16,64,256$；
- tolerance/step 至少四档；
- exact trace augmented solve 作为 reference；
- 同一 initial states 与 checkpoints；
- 报告 trace pointwise bias/variance、integrated logp bias/RMSE、state error、coverage interval、NFE/VJP/wall time；
- 分别比较 fixed-trajectory（冻结 $z(t)$）和 coupled solve（estimator进入实际程序）。

Confidence interval 可对 replicate 的 integrated logp mean 用

$$
\bar\ell\pm t_{0.975,R-1}\frac{s_\ell}{\sqrt R},
$$

并同时报告 individual-run RMSE，避免只看均值掩盖大方差。

### DYN-FLOW-D03

表格不能直接推出：A/B/C architecture相同、参数量相同、checkpoint相同、数据处理相同、NLL单位相同、NLL差异显著、C最好、A最快、NFE等价成本、tolerance相同、state error相同、trace error相同、round-trip代表likelihood error、任何模型 exact invertible、任何 estimator unbiased、训练预算相同、hardware/batch相同或 stiffness 相同。

**Equal-error**：先定义 held-out NLL/reference-state/logp error 门，再调各模型 tolerance/probes 直到达到共同门，比较 wall time、memory、VJP、failure rate。

**Equal-budget**：固定 wall time/energy/VJP budget 与硬件，允许各方法选择最优 tolerance/probes，比较 NLL、sample metric、round-trip 和置信区间。

真实成本可近似记录为

$$
C=C_fN_f+C_{\rm VJP}N_{\rm VJP}+C_{\rm JVP}N_{\rm JVP}
+C_{\rm linear}N_{\rm linear}+C_{\rm reject}N_{\rm reject},
$$

再用实测 wall time 校准；NFE 单独不能替代。

Evaluation 对每个 checkpoint 和 data batch 用多组独立 probes，报告 mean NLL、between-seed standard deviation/standard error 和 confidence interval；最好在小维或子集上同时给 exact trace bias。

Round-trip 是 forward/backward numerical composition误差；endpoint error 是对 reference trajectory 的状态误差；NLL error 还含 base point恢复、divergence和积分误差。三者相关但不等价。

Stiff 情形增加 accepted/rejected steps、min/max stepsize、Jacobian spectral/norm indicator、Newton/Krylov iterations、NJE/NLU、preconditioner setup/apply、nonlinear/linear residual 和 backward failure。

Gradient check 必须对同一 computed stochastic objective：固定 probe/seed与adaptive semantics，用中心差分比较 discrete program gradient；另做 tolerance refinement 研究 continuous/discrete gap。

不越界结论示例：

> 在所列 checkpoint、预处理和硬件上，C 在给定 wall-time budget 下取得最低 observed mean NLL；但由于未报告 seed/probe uncertainty 与统一 solver tolerances，0.01—0.03 的差异尚不能解释为统计显著或一般算法优势。B 的 round-trip 更小，不能单独证明其 NLL 更准确。

## E. AI 迁移、研究设计与综合审计

### DYN-FLOW-E01

原句包含至少五个不同 claim。

**Exactly invertible**：对 exact ODE flow，需要 existence、uniqueness、相关域的双向 completeness 和状态 regularity。若只在 flow image 上逆，应这样写；数值反向积分只能近似。

**Numerical round-trip**：需 tolerance/precision/grid/probe policy 下的误差曲线与 failure rate，不能由 exact theorem 代替。

**Exact likelihood**：若 exact divergence 与 exact integration不可得，程序通常只是 numerical approximation。应报告 state/logp refinement 和 evaluation uncertainty。

**Unbiased trace**：Hutchinson 对固定矩阵满足二阶矩条件时无偏；不自动使有限 solve、exp-density、NLL 或训练后参数无偏。要声明 probe reuse 与 coupling。

**Arbitrary continuous transformations**：同维 unique ODE flow 是 orientation-preserving homeomorphism/diffeomorphism（在相应条件下），不能实现合并、撕裂和 arbitrary non-injective map。Augmentation 可缓解但改变概率合同。

**Constant memory**：经典 continuous-adjoint 宣称通常是相对于保存所有 solver states；实际还有 parameters、activations within RHS、checkpoints、solver workspace与可能的 numerical mismatch。必须给 peak-memory measurement。

**Lower NFE means efficient**：需计算 trace VJP、backward solve、rejection、stiff linear solve、batch/hardware 和 equal-error wall time。

ReLU vector field 通常 locally Lipschitz，可能仍有 unique flow，但不处处 $C^1$；Liouville/divergence需用几乎处处/弱正则框架或光滑化后陈述。Clipping 可使 field 非光滑；event reset 可产生 hybrid jump map，不再是单一光滑 ODE flow；finite precision 只给计算程序。

改写示例：

> 在实验所覆盖的有界状态区间内，我们使用 locally Lipschitz 的向量场，并未观察到积分失败。相应 exact IVP 在标准条件下定义 injective flow；实现的 forward–backward round-trip 在 rtol/atol 指定后中位误差为……。训练使用每条 trajectory 固定的 Rademacher Hutchinson probe，它对固定 Jacobian trace 无偏；evaluation 用32 probes并报告 Monte Carlo SE。模型保持同维 ODE flow 的拓扑限制。相对基线，在相同 held-out NLL误差门和硬件上，总 wall time/peak memory为……；NFE与VJP计数同时报告。

### DYN-FLOW-E02

若“细圆环”指零厚度圆周，则它相对二维 Lebesgue measure 是 singular law；若指有非零厚度或加噪环带，则有二维 density。

**同维 CNF**：从 full-support Gaussian 经 $\mathbb R^2$ global diffeomorphism 后仍是 full-support二维 density。可把桥区 density 压得极小，近似两条视觉环，但不能精确变成零厚度或严格断开的支持。标准 change-of-variables 可算 likelihood。

**Augmented ODE + projection**：高维轨迹可绕开二维 no-crossing限制，projection 后可更灵活。但 projection 非可逆；若只做生成/分类可直接用，若要二维 exact likelihood 必须对被投影 latent coordinates 边缘化或设计专门 surjective likelihood，通常不再是简单 CNF 公式。

**Observation noise**：令 latent clean variable 在环结构上，再设

$$
x=y+\eta,
\qquad \eta\sim\mathcal N(0,\sigma^2I).
$$

$x$ 有二维平滑 density，通常甚至全空间正。Likelihood 需要对 latent $y$ 积分；若 latent flow 和 convolution 结构允许，可近似/变分计算。目标对象已从 clean singular law 变成 noisy observation law。

**低维 latent + observation model**：用一维 angle/ring-index latent 和二维 decoder/noise。它自然表达低维几何，但 likelihood 需积分/求和 latent，identifiability 与 decoder Jacobian/observation noise 要单独处理。

Sample quality 可用 coverage、ring occupancy、distance-to-manifold、多样性；density quality用 held-out log score、calibration与已知 synthetic KL/transport。两者不能互相替代。

有限样本图中两个簇之间没有点，只说明 bridge density 可能很小；不能证明严格为零。Full-support density 在有限样本中同样可能显示明显空隙。

### DYN-FLOW-E03

Claim–evidence matrix 可写为：

| claim | formal target | experiment | pass criterion | boundary |
|---|---|---|---|---|
| trace unbiased | $E\hat\tau(A)=\operatorname{tr}A$ | fixed matrices, many seeds | CI含真值且bias随replicates收缩 | 只对固定$A$与声明probe law |
| lower variance | $\operatorname{Var}\hat\tau\le c\operatorname{Var}\hat\tau_H$ | diagonal/dense/skew/low-rank/nonnormal族 | paired CI与effect size | 不从单一矩阵外推 |
| lower integrated logp RMSE | $E|\hat\ell-\ell^*|^2$ | fixed exact trajectory | probe/VJP budget曲线支配 | 不含trajectory coupling |
| better coupled CNF | computed solver objective | exact-trace reference, tolerance sweep | state/logp/NLL在同预算改善 | 依赖solver/probe reuse |
| faster | wall time/energy | same hardware/batch/precision | equal-error与equal-budget都报告 | NFE不是充分代理 |
| better generation | population/sample metrics | 多数据、多seed | CI、failure cases、coverage | 不推出likelihood更准 |
| general high-d advantage | quantified model/matrix class | dimension/architecture sweep | 预注册主要终点跨设置成立 | 明示失败族 |

矩阵族至少包括：

- diagonal：检验 Rademacher 零方差基线；
- dense symmetric：检验 off-diagonal energy；
- skew-symmetric：二次型与 trace 都应为零，检验实现；
- low-rank plus diagonal：检验结构利用；
- nonnormal nonsymmetric：确保先取 symmetric part 的理论一致性。

Small/medium dimension 形成完整 Jacobian exact trace；large dimension只比较 structured/exact可得子类或高精 reference。Sweep $d$、probe count、seed、precision、VJP budget；基线包括 Rademacher、Gaussian Hutchinson、架构允许时 exact structured trace。

两层实验：先冻结 exact trajectory，只测试 divergence estimator；再让 estimator 进入 coupled augmented solve，观察 adaptive branch 与 logp。固定每 solve probe、每 step与每 RHS重采样分别登记，不混成一个平均数。

训练层固定 optimizer/data order或做 paired seeds；报告 stochastic gradient variance、same-objective FD check、forward/backward reuse。最终指标同时含 NLL及MC SE、sample coverage/quality、wall time、peak memory、energy和失败率。

Negative results 必须保留，例如 diagonal 上新方法不如零方差 Rademacher、skew 部分不应贡献、某些 dimension 被setup cost主导、adaptive solver在RHS重采样时拒步失控。

证据升级：L0 写公式；L1 证明 target class 的bias/variance；L2 exact-trace复现；L3 coupled solver与gradient；L4 likelihood；L5生成/预算；L6多数据多架构独立复核。只有跨层通过后才可写一般“显著改进高维 CNF”。

## 总结性评分锚点

- 能写公式但不写定义域：至多 A/B 水平。
- 能完整证明 Liouville，但不能区分 onto 与 onto image：证明仍不合格。
- 能运行 CNF，但没有 exact-trace/reference/tolerance sweep：只算程序存在性证据。
- 能报告无偏与方差，却没声明 probe reuse 和 coupled trajectory：统计对象未闭合。
- 能同时守住 theorem、solver、estimator、likelihood 与 topology 五层边界，才达到可研读前沿 CNF/flow/diffusion 论文的理论水平。
