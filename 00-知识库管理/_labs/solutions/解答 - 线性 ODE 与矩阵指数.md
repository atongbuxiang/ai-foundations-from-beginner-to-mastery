---
type: solution
status: draft
area: [math/ode, math/linear-systems, ai/state-space-models]
topic: "线性 ODE 与矩阵指数"
exercise: "[[习题 - 线性 ODE 与矩阵指数]]"
related: ["[[线性 ODE 与矩阵指数]]", "[[ODE、动力系统与 SDE MOC]]", "[[实验 - 稳定非正规系统的矩阵指数瞬态]]"]
created: 2026-08-19
updated: 2026-08-19
---

# 解答 - 线性 ODE 与矩阵指数

> [!warning] 使用顺序
> 先独立恢复传播公式，再打开解答。会算 $e^{tA}$ 不等于理解线性动力学：必须能解释 basis independence、time ordering、input convolution、transient growth、hold assumption 与 sampling identifiability。

## A. 识别与复述

### DYN-LIN-A01

齐次线性系统是

$$
x'=A(t)x;
$$

其解满足superposition。非齐次系统

$$
x'=A(t)x+g(t)
$$

的解集通常是affine set。autonomous表示右端不显含time；time-varying linear system允许 $A=A(t)$。$x'=Ax+b$ 是affine而非homogeneous linear。input-output form为

$$
x'=Ax+Bu,
\qquad y=Cx+Du.
$$

若matrix solution $X'=A(t)X$ 在interval上处处invertible，则 $X$ 是fundamental matrix。它的determinant

$$
W(t)=\det X(t)
$$

称Wronskian。normalized transition是

$$
\Phi(t,s)=X(t)X(s)^{-1}.
$$

核心性质：

$$
\Phi(s,s)=I,
$$

$$
\Phi(t,r)\Phi(r,s)=\Phi(t,s),
$$

$$
\Phi(t,s)^{-1}=\Phi(s,t),
$$

$$
\partial_t\Phi(t,s)=A(t)\Phi(t,s),
$$

$$
\partial_s\Phi(t,s)=-\Phi(t,s)A(s).
$$

若 $R$ constant invertible，则 $XR$ 也是fundamental matrix；任意两组fundamental matrices都具有这种关系。但right factor在

$$
(X(t)R)(X(s)R)^{-1}
$$

中消去，所以 $\Phi$ 由system和两个times唯一决定。

### DYN-LIN-A02

| 对象 | 时间含义 | 结论尺度 |
|---|---|---|
| real $\lambda$ | $e^{\lambda t}$ growth/decay | 单一eigenmode |
| $a\pm ib$ | $e^{at}$ envelope与frequency $b$ | 二维real oscillatory mode |
| size-$r$ Jordan chain | $t^ke^{\lambda t}$，$0\le k<r$ | finite-time polynomial factor |
| $\alpha(A)=\max\operatorname{Re}\lambda$ | asymptotic exponential rate | long-time |
| $\omega(A)=\lambda_{\max}((A+A^*)/2)$ | 最大instantaneous Euclidean growth rate | $t=0$/local-in-time |
| normal $A$ | $\|e^{tA}\|_2=e^{\alpha(A)t}$ | spectrum完全控制2-norm |
| ill-conditioned $V$ | $\|e^{tA}\|\le\kappa(V)e^{\alpha t}$ 的large prefactor | modal sensitivity |
| nonnormality | decaying modes可先constructively interfere | finite-time transient |

$\alpha(A)<0$ 是asymptotic/exponential stability statement；$\omega(A)>0$ 说明存在initially growing direction；$\sup_t\|e^{tA}\|$ 才直接度量worst finite-time gain。它们不能互换。

### DYN-LIN-A03

在ZOH下：

$$
u(t)=u_k,
\qquad t\in[k\Delta,(k+1)\Delta),
$$

有

$$
x_{k+1}=\bar A x_k+\bar B u_k,
\qquad y_k=Cx_k+Du_k,
$$

其中

$$
\bar A=e^{\Delta A},
\qquad
\bar B=\int_0^\Delta e^{sA}B\,ds.
$$

“exact”表示：constant $A,B$、ZOH input和exact arithmetic下，recurrence state等于continuous solution在sample times的值。它不表示arbitrary input、floating-point matrix exponential或learned model都exact。

若 $x_0=0$：

$$
y_k=\sum_{j=0}^{k}K_{k-j}u_j,
$$

其中

$$
K_0=D,
\qquad
K_\ell=C\bar A^{\ell-1}\bar B,\quad\ell\ge1.
$$

spectral mapping是

$$
\mu=e^{\Delta\lambda}.
$$

于是 $\operatorname{Re}\lambda<0\Leftrightarrow|\mu|<1$；但 $\lambda$ 与 $\lambda+2\pi ik/\Delta$ 给同一 $\mu$，产生sampling aliasing和log-branch ambiguity。

五层误差分别是：linear/LTI model mismatch；input hold/interpolation error；matrix-exponential computation/roundoff；sampling、similarity与hidden-mode identifiability；held-out prediction/generalization。前一层通过不替代后一层。

## B. 手算与构造

### DYN-LIN-B01

对distinct diagonal entries的upper-triangular matrix：

$$
\boxed{
e^{tA}=
\begin{bmatrix}
e^{-t}&2(e^{-t}-e^{-2t})\\
0&e^{-2t}
\end{bmatrix}.}
$$

因此

$$
x(t)=e^{tA}e_2
=
\begin{bmatrix}
2(e^{-t}-e^{-2t})\\e^{-2t}
\end{bmatrix}.
$$

直接求导：

$$
x_1'=-2e^{-t}+4e^{-2t},
\qquad
x_2'=-2e^{-2t}.
$$

另一方面

$$
Ax=
\begin{bmatrix}
-x_1+2x_2\\-2x_2
\end{bmatrix}
=
\begin{bmatrix}
-2e^{-t}+4e^{-2t}\\-2e^{-2t}
\end{bmatrix},
$$

与derivative一致；$x(0)=e_2$。

取 $X(t)=e^{tA}$：

$$
W(t)=\det e^{tA}
=e^{-t}e^{-2t}=e^{-3t}.
$$

又 $\operatorname{tr}A=-3$，所以

$$
W(t)=W(0)e^{t\operatorname{tr}A}=e^{-3t}.
$$

transition matrix为

$$
\Phi(t,s)=e^{(t-s)A}.
$$

于是

$$
\Phi(t,r)\Phi(r,s)
=e^{(t-r)A}e^{(r-s)A}
=e^{(t-s)A}
=\Phi(t,s).
$$

### DYN-LIN-B02

写

$$
A=-I+N,
\qquad
N=\begin{bmatrix}0&4\\0&0\end{bmatrix},
\qquad N^2=0.
$$

故

$$
e^{tA}=e^{-t}(I+tN)
=e^{-t}
\begin{bmatrix}1&4t\\0&1\end{bmatrix}.
$$

对 $x_0=e_2$：

$$
x(t)=e^{-t}
\begin{bmatrix}4t\\1\end{bmatrix}.
$$

first component $q(t)=4te^{-t}$，

$$
q'(t)=4e^{-t}(1-t),
$$

所以在 $t=1$ 达最大值 $4/e$。

$$
\|x(1)\|_2
=\frac{\sqrt{16+1}}{e}
=\frac{\sqrt{17}}e
\approx1.517>1=\|x(0)\|_2.
$$

但两个eigenvalues都是 $-1$，所以 $\alpha(A)=-1$，且 $x(t)\to0$。这正是“finite transient不否定asymptotic decay”。

Hermitian/symmetric part是

$$
\frac{A+A^{\mathsf T}}2
=
\begin{bmatrix}-1&2\\2&-1\end{bmatrix},
$$

eigenvalues为 $1,-3$，故

$$
\omega(A)=1>0.
$$

这说明存在某个initial direction立刻增长；它不要求题目给定的 $e_2$ 也在 $t=0$ 立刻增长。事实上 $e_2$ 初始energy derivative为负，但Jordan coupling稍后把第二分量转入第一分量，仍造成finite-time norm超过initial norm。

### DYN-LIN-B03

这里 $A=-1,B=2$。取 $d=\Delta=\log2$：

$$
\bar A=e^{-d}=\frac12,
$$

$$
\bar B=\int_0^de^{-s}2\,ds
=2(1-e^{-d})=1.
$$

所以exact recurrence为

$$
x_{k+1}=\frac12x_k+u_k.
$$

从 $x_0=0$：

$$
x_1=1,
\qquad
x_2=\frac12,
\qquad
x_3=\frac14+1=\frac54.
$$

$C=1,D=0$，因此

$$
K_0=0,
\qquad
K_\ell=\left(\frac12\right)^{\ell-1},
\quad\ell\ge1.
$$

forward Euler给

$$
x_{k+1}^{E}
=(1-d)x_k^E+2du_k.
$$

于是

$$
x_1^E=2d,
$$

$$
x_2^E=2d(1-d),
$$

$$
x_3^E=2d\bigl((1-d)^2+1\bigr).
$$

数值约为

$$
(1.3863, 0.4254, 1.5168),
$$

与exact sampled states $(1,0.5,1.25)$ 不同。Euler只是一阶approximation。

最后

$$
e^{-\Delta}=1-\Delta+O(\Delta^2),
$$

$$
2(1-e^{-\Delta})
=2\Delta+O(\Delta^2),
$$

与continuous coefficients吻合。

## C. 推导与证明

### DYN-LIN-C01

若 $X,Y$ 都是fundamental matrices，令

$$
R(t)=X(t)^{-1}Y(t).
$$

则

$$
\begin{aligned}
R'
&=-X^{-1}X'X^{-1}Y+X^{-1}Y'\\
&=-X^{-1}AXX^{-1}Y+X^{-1}AY=0.
\end{aligned}
$$

所以 $R(t)=R$ constant，并且 $Y=XR$。两者可逆使 $R$ invertible。

由 $\Phi(t,s)=X(t)X(s)^{-1}$：

$$
\Phi(t,r)\Phi(r,s)
=X(t)X(r)^{-1}X(r)X(s)^{-1}
=\Phi(t,s),
$$

并且

$$
\Phi(t,s)^{-1}
=X(s)X(t)^{-1}
=\Phi(s,t).
$$

对 $s$ 求导：

$$
\begin{aligned}
\partial_s\Phi(t,s)
&=X(t)\frac d{ds}X(s)^{-1}\\
&=-X(t)X(s)^{-1}X'(s)X(s)^{-1}\\
&=-\Phi(t,s)A(s).
\end{aligned}
$$

令 $W=\det X$。Jacobi formula给

$$
W'=W\operatorname{tr}(X^{-1}X')
=W\operatorname{tr}(X^{-1}AX)
=W\operatorname{tr}A.
$$

scalar ODE求解得

$$
\boxed{
W(t)=W(s)
\exp\left(\int_s^t\operatorname{tr}A(\tau)d\tau\right).}
$$

transition integral equation为

$$
\Phi(t,s)=I+\int_s^tA(\tau)\Phi(\tau,s)d\tau.
$$

前三个nontrivial orders是

$$
\int_s^tA(\tau_1)d\tau_1,
$$

$$
\int_s^t\int_s^{\tau_1}
A(\tau_1)A(\tau_2)d\tau_2d\tau_1,
$$

$$
\int_s^t\int_s^{\tau_1}\int_s^{\tau_2}
A(\tau_1)A(\tau_2)A(\tau_3)
d\tau_3d\tau_2d\tau_1.
$$

若所有different-time matrices pairwise commute，product对variables symmetric；ordered simplex占hypercube的 $1/k!$，所以第 $k$ 阶等于

$$
\frac1{k!}
\left(\int_s^tA(\tau)d\tau\right)^k.
$$

求和得到普通matrix exponential。

对二段例子，$A_1^2=A_2^2=0$，故

$$
e^{A_2}e^{A_1}
=(I+A_2)(I+A_1)
=\begin{bmatrix}1&1\\1&2\end{bmatrix}.
$$

而

$$
e^{A_1+A_2}
=\begin{bmatrix}\cosh1&\sinh1\\\sinh1&\cosh1\end{bmatrix}.
$$

例如左上元素分别为 $1$ 与 $\cosh1>1$，所以不相等。断裂点正是 $A_1A_2\ne A_2A_1$。

### DYN-LIN-C02

候选time-varying solution是

$$
x(t)=\Phi(t,s)x_s
+\int_s^t\Phi(t,\tau)g(\tau)d\tau.
$$

在 $t=s$ 它等于 $x_s$。用 $\partial_t\Phi=A(t)\Phi$ 和Leibniz rule：

$$
\begin{aligned}
x'
&=A(t)\Phi(t,s)x_s+Phi(t,t)g(t)\\
&\quad+
\int_s^tA(t)\Phi(t,\tau)g(\tau)d\tau\\
&=A(t)x(t)+g(t).
\end{aligned}
$$

uniqueness完成证明。

对LTI system，$\Phi(t,\tau)=e^{(t-\tau)A}$，所以

$$
y(t)=Ce^{tA}x_0
+\int_0^tCe^{(t-\tau)A}Bu(\tau)d\tau
+Du(t).
$$

dynamic causal kernel为

$$
K(r)=Ce^{rA}B,
\qquad r\ge0.
$$

若 $\|e^{tA}\|\le Me^{-\beta t}$，则

$$
\begin{aligned}
\|x(t)\|
&\le Me^{-\beta t}\|x_0\|
+\int_0^tMe^{-\beta(t-\tau)}\|B\|U d\tau\\
&=Me^{-\beta t}\|x_0\|
+\frac{M\|B\|U}{\beta}(1-e^{-\beta t})\\
&\le Me^{-\beta t}\|x_0\|
+\frac{M\|B\|}{\beta}U.
\end{aligned}
$$

discrete recurrence反复代入：

$$
x_1=\bar Ax_0+\bar Bu_0,
$$

$$
x_2=\bar A^2x_0+\bar A\bar Bu_0+\bar Bu_1,
$$

归纳得

$$
x_k=\bar A^kx_0+
\sum_{j=0}^{k-1}\bar A^{k-1-j}\bar Bu_j.
$$

代入output并取 $x_0=0$：

$$
y_k=Du_k+
\sum_{j=0}^{k-1}C\bar A^{k-1-j}\bar Bu_j.
$$

continuous convolution依赖 $\Phi(t,\tau)$ 只通过difference $t-\tau$，这来自constant $A$；discrete convolution依赖同一 $\bar A$ 每步重复，即time-invariant recurrence。时变系统一般得到two-time kernel，而不是ordinary shift-invariant convolution。

### DYN-LIN-C03

在一个sample interval，令local time $r\in[0,\Delta]$：

$$
x(\Delta)=e^{\Delta A}x(0)
+\int_0^\Delta e^{(\Delta-\tau)A}B u_kd\tau.
$$

换元 $s=\Delta-\tau$ 得

$$
\bar A=e^{\Delta A},
\qquad
\bar B=\int_0^\Delta e^{sA}Bds.
$$

考虑augmented state $z=[x;u_k]$，其interval内满足

$$
z'=
\begin{bmatrix}A&B\\0&0\end{bmatrix}z.
$$

bottom state保持constant；top state的solution正是上述variation-of-constants。因此传播矩阵必须为

$$
\exp\left(
\Delta\begin{bmatrix}A&B\\0&0\end{bmatrix}
\right)
=\begin{bmatrix}\bar A&\bar B\\0&I\end{bmatrix}.
$$

series给

$$
e^{\Delta A}=I+\Delta A+\frac{\Delta^2}{2}A^2+O(\Delta^3),
$$

以及

$$
\begin{aligned}
\bar B
&=\int_0^\Delta
\left(I+sA+\frac{s^2}{2}A^2+\cdots\right)Bds\\
&=\Delta B+\frac{\Delta^2}{2}AB
+\frac{\Delta^3}{6}A^2B+O(\Delta^4).
\end{aligned}
$$

matrix-function spectral mapping theorem给

$$
\sigma(e^{\Delta A})
=\{e^{\Delta\lambda}:\lambda\in\sigma(A)\}.
$$

而

$$
e^{\Delta(\lambda+2\pi ik/\Delta)}
=e^{\Delta\lambda}e^{2\pi ik}
=e^{\Delta\lambda}.
$$

要选一个continuous generator，至少需要固定sampling interval、选择matrix-log branch，并用先验把imaginary parts限制在一个Nyquist strip，例如

$$
-\frac\pi\Delta
<\operatorname{Im}\lambda
<\frac\pi\Delta.
$$

还要确保 $\bar A$ 的spectrum/Jordan structure允许所需real logarithm，并处理noise。即使这些条件满足，得到的是在所选branch和model class中的candidate，不是无先验绝对唯一性。

## D. 反例与失败边界

### DYN-LIN-D01

1. **假。** $A=[[-1,K],[0,-2]]$ 在large $K$ 时有transient amplification。修正：normal $A$ 时 $\|e^{tA}\|_2=e^{\alpha t}$；一般Hurwitz只保证最终exponential decay bound。

2. **假。** 上述 $A_K$ 对所有 $K$ 有相同eigenvalues $-1,-2$，但off-diagonal response $K(e^{-t}-e^{-2t})$ 随 $K$ 改变。还需Jordan/eigenvector geometry。

3. **假。** diagonalizable matrix的eigenvector matrix $V$ 可极端ill-conditioned。$Ve^{t\Lambda}V^{-1}$ 是exact identity，不保证floating-point route stable。

4. **假。** continuity只给integration legitimacy；若different-time $A$ 不交换，Peano–Baker products有order。修正：pairwise commutativity是普通 $e^{\int A}$ 的常用充分条件。

5. **假。** discrete eigenvalues只确定continuous frequencies modulo $2\pi/\Delta$；matrix logarithm也有branch/real-existence问题。必须增加branch和frequency-band assumptions。

6. **假。** exactness只针对ZOH-represented input。arbitrary input在interval内变化时，要么精确积分真实input，要么承认hold/interpolation error。

### DYN-LIN-D02

因为

$$
e^{tA}=\operatorname{diag}(e^{-t},e^{-2t}),
$$

zero-state kernel是

$$
K(t)=Ce^{tA}B
=e_2^{\mathsf T}
\begin{bmatrix}e^{-t}&0\\0&e^{-2t}\end{bmatrix}e_1
=0.
$$

所以任意input都只进入first state，而output只读取second state；zero-state dynamic output恒为零。

但若 $x_0=e_2$ 且 $u=0$：

$$
x(t)=e^{-2t}e_2,
\qquad
y(t)=e^{-2t}.
$$

这说明second mode可被initial condition观察到，却不能由given input激发；first mode可被input激发，却被given output annihilate。

例如改成

$$
B=\begin{bmatrix}1\\1\end{bmatrix},
\qquad
C=\begin{bmatrix}1&1\end{bmatrix},
$$

则

$$
K(t)=e^{-t}+e^{-2t},
$$

两个modes都visible。

所以long-memory claim至少要检查 $B$ 是否excite slow mode、$C$ 是否read it、coefficients是否因cancellation过小，以及training/precision是否保留该mode。仅把hidden eigenvalue放在unit circle附近不够。

### DYN-LIN-D03

令

$$
J=\begin{bmatrix}0&-1\\1&0\end{bmatrix},
\qquad
\nu_k=\omega+2\pi k.
$$

则

$$
A_k=-I+\nu_kJ,
$$

且 $I,J$ commute，所以

$$
e^{A_k}=e^{-1}e^{\nu_kJ}
=e^{-1}
\begin{bmatrix}
\cos\nu_k&-\sin\nu_k\\
\sin\nu_k&\cos\nu_k
\end{bmatrix}.
$$

由于sine/cosine是 $2\pi$ periodic：

$$
e^{A_k}=e^{-1}R(\omega)
$$

与 $k$ 无关。integer-time observations因此只看到同一个sampled rotation-decay matrix。

减少ambiguity的方法包括：

- 以已知bandlimit约束 $|\nu|<\pi/\Delta$，并提高sampling rate；
- 加入noninteger或irregular gaps；理想情况下一个与base interval比例为irrational的gap可打破integer alias family；
- 使用continuous-time sensor/derivative observations；
- 在learning objective中明确frequency prior/log branch。

所有 $e^{A_k}$ 都被solver正确算出且确实相同；失败来自observation map many-to-one，所以是identifiability而非numerical error。

## E. AI 迁移

### DYN-LIN-E01

一份linear SSM audit可包含：

**连续模型。** 报告 $A,B,C,D$、units、state dimension、real/complex parameterization、是否diagonal/normal/structured，以及original HiPPO construction是否time-varying。

**采样合同。** 报告 $\Delta$ distribution、ZOH/interpolation rule、$\bar A,\bar B$ algorithm；irregular gaps必须逐gap recompute或说明approximation。

**动力学。** 同时报 $\alpha(A)$、$\rho(\bar A)$、$\omega(A)$、$\sup_{t\le T}\|e^{tA}\|$ estimate与long-horizon state norm。只报eigenvalues不够。

**mode visibility。** 检查impulse kernel中的mode residues，验证slow modes确实由 $B$ 激发、由 $C$ 读取，并报告cancellation。

**实现等价。** 对同一inputs比较sequential recurrence、direct kernel convolution和FFT implementation，记录relative error、precision、kernel truncation与sequence length。

**公平实验。** 匹配parameter count、training tokens、FLOPs、wall-clock与memory；增加held-out longer sequences、new gaps、missing samples和frequency-alias stress data。

可反驳criteria示例：

1. recurrence与convolution在FP64下relative discrepancy $<10^{-10}$，FP32下 $<10^{-5}$；否则implementation claim失败；
2. tolerance/precision refinement后primary metric变化 $<0.1$ percentage point；否则收益可能来自numerical artifact；
3. 在parameter/FLOP-matched baseline上，多个seeds的long-context gain confidence interval仍不含zero；
4. 对Nyquist-near frequencies提高sampling rate后prediction一致；若alias stress下崩溃，不能声称continuous frequency已identified。

### DYN-LIN-E02

对trajectory $z(t)$ 加small perturbation $\varepsilon\delta z(t)$：

$$
\frac d{dt}(z+\varepsilon\delta z)
=f(t,z+\varepsilon\delta z).
$$

一阶Taylor展开：

$$
f(t,z+\varepsilon\delta z)
=f(t,z)+\varepsilon J_f(t,z)\delta z+o(\varepsilon).
$$

减去base equation、除以 $\varepsilon$ 并取limit：

$$
\delta z'=J_f(t,z(t))\delta z.
$$

令 $A(t)=J_f(t,z(t))$，则

$$
\delta z(t)=\Phi(t,s)\delta z(s),
$$

且

$$
\begin{aligned}
\Phi(t,s)
&=I+\int_s^tA(\tau_1)d\tau_1\\
&\quad+\int_s^t\int_s^{\tau_1}
A(\tau_1)A(\tau_2)d\tau_2d\tau_1+\cdots.
\end{aligned}
$$

若所有different-time Jacobians commute，才有

$$
\Phi(t,s)=\exp\left(\int_s^tA(\tau)d\tau\right).
$$

取正文的piecewise $A_1,A_2$，真实sensitivity是

$$
e^{A_2}e^{A_1},
$$

而average/integrated Jacobian route给 $e^{A_1+A_2}$，两者不同。交换两个time segments还会得到 $e^{A_1}e^{A_2}$，再次不同。

average Jacobian eigenvalues删除了ordering、eigenvector rotation和state-dependent sampling path。它可以是local summary或approximation feature，但必须通过Magnus/truncation/error experiment等额外分析才能支持whole-trajectory claim。

### DYN-LIN-E03

可以采用三因素controlled design。

**模型组：**

1. continuous-parameter SSM，以ZOH exact $\bar A,\bar B$；
2. 同参数量的direct discrete RNN，自由学习 $\bar A,\bar B$；
3. Euler-like residual recurrence $x_{k+1}=x_k+\Delta(Ax_k+Bu_k)$；
4. exact-discrete SSM但固定uniform gaps；
5. continuous SSM使用真实irregular gaps。

**控制变量：** 匹配state size、readout、nonlinearity、optimizer、training tokens、parameter count；同时分别做FLOP-matched和wall-clock-matched runs。对continuous models记录exponential/kernel generation cost，不能把它藏在precomputation中。

**sampling matrix：** 在multiple $\Delta$ 上train/test，加入near-Nyquist sinusoids、aliased frequency pairs、missing observations与out-of-range gaps。若continuous sharing是真正收益，它应在重新采样/irregular gaps下比direct discrete baseline更稳定。

**numerical checks：** FP64 reference、FP32/BF16 runs、matrix-exponential refinement、spectral mapping residual、recurrence–convolution discrepancy、kernel truncation sweep与long-horizon overflow log。

**判别逻辑：**

- exact-discrete优于Euler而continuous/direct-discrete相近：收益主要来自propagator accuracy；
- continuous model只在irregular/new gaps获益：支持time-sharing/interpolation interpretation；
- 优势在compute-matched后消失：原收益主要来自budget；
- near-Nyquist test中多个continuous generators不可区分：必须报告aliasing，不得声称identified frequency；
- recurrence与convolution不一致：先修implementation，不能比较model quality。

最终报告task metric、long-horizon error、frequency error、NFE/kernel cost、wall-clock、memory、seed interval和all failures，使三种收益来源能够分别被推翻。

