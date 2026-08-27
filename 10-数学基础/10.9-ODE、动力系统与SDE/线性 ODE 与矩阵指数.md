---
type: concept
status: draft
area: [math/ode, math/linear-systems, ai/state-space-models]
aliases: [线性常微分方程, 线性动力系统, fundamental matrix, state transition matrix, linear ODE]
prerequisites: ["[[常微分方程、初值问题与解的存在唯一性]]", "[[矩阵函数与矩阵指数]]", "[[特征分解]]", "[[广义特征向量与 Jordan 结构]]", "[[矩阵范数]]"]
related: ["[[ODE、动力系统与 SDE MOC]]", "[[非正规矩阵、预解式与伪谱]]", "[[相图、平衡点与局部稳定性]]", "[[Euler、Runge-Kutta 与离散化误差]]", "[[流映射、Liouville 公式与连续正规化流]]", "[[实验 - 稳定非正规系统的矩阵指数瞬态]]"]
sources: ["MIT-18.03SC-Matrix-Exponentials", "Stanford-EE263-Linear-Dynamical-Systems", "Higham-Lin-2013-Matrix-Functions", "Gu-et-al-2020-HiPPO", "Gu-et-al-2022-S4", "Gu-et-al-2023-How-to-Train-HiPPO", "Su-10114-SSM-Linear-HiPPO"]
created: 2026-08-19
updated: 2026-08-27
---

# 线性 ODE 与矩阵指数

> [!abstract] 本章主问题
> 对常系数齐次系统 $\dot x=Ax$，矩阵指数 $e^{(t-s)A}$ 是把时刻 $s$ 的完整状态传播到时刻 $t$ 的 exact flow；特征值只描述渐近模态，Jordan 链决定额外的多项式因子，非正规特征向量几何决定有限时间放大。加入输入后，variation of constants 把响应写成“初值传播 + 因果卷积”；在零阶保持采样下，它精确变为离散 SSM，但这个“精确”依赖输入保持假设，也不消除 matrix-exponential 计算误差、采样 aliasing、参数不可辨识或统计泛化问题。

> [!important] 与前置章节的分工
> [[矩阵函数与矩阵指数]]已经回答 $e^A$ 如何定义、怎样计算与求 Fréchet 导数；本章不重写完整 matrix-function calculus，而是把 $e^{tA}$ 当作**动力系统传播算子**，研究 fundamental matrix、time-varying ordering、mode、forcing、stability、sampling 与 SSM。

## 学习目标

完成本章后，你应当能够：

1. 区分 homogeneous、inhomogeneous、autonomous、time-varying、affine 与 input-output linear systems；
2. 从 superposition 解释解空间为何是线性空间；
3. 定义 fundamental matrix、normalized state-transition matrix 与 Wronskian；
4. 证明 $\Phi(t,s)$ 的 identity、composition、inverse 与 differential properties；
5. 说明 constant $A$ 时为何 $\Phi(t,s)=e^{(t-s)A}$；
6. 写出 time-varying system 的 Peano–Baker series；
7. 解释 $e^{\int A}$ 何时成立、何时因 noncommutativity 失败；
8. 从 eigenvector、complex pair 与 Jordan chain 读出 exponential/oscillatory/polynomial modes；
9. 区分 spectral abscissa、exponential stability bound、numerical abscissa 与 transient growth；
10. 推导 variation-of-constants formula；
11. 把 input-output response 写成 causal Green kernel/convolution；
12. 推导 constant input equilibrium 与 bounded-input state bound；
13. 推导零阶保持下的 exact discrete matrices $\bar A,\bar B$；
14. 用 augmented exponential 避免 $A^{-1}$；
15. 证明 continuous eigenvalues 到 discrete eigenvalues 的 spectral mapping；
16. 解释 sampling aliasing 与 matrix logarithm nonuniqueness；
17. 推导 discrete SSM 的 recurrence–convolution equivalence；
18. 审计 HiPPO/S4、linear RNN 与 linearized Neural ODE 中的连续—离散声明。

> [!question] 初学者读完必须能回答
> 1. Fundamental matrix 与 normalized state-transition matrix 有何区别？
> 2. $\Phi(t,r)\Phi(r,s)=\Phi(t,s)$ 与逆性质怎样表达流的复合？
> 3. Variation of constants 如何分离初值传播与输入响应？
> 4. Eigenvalue、Jordan chain 与 nonnormal eigenbasis 分别控制什么时间行为？
> 5. 为什么 Hurwitz eigenvalues 不保证 Euclidean norm 单调衰减？
> 6. ZOH 下 $\bar A,\bar B$ 怎样精确推导，何时不能用 $A^{-1}$ 公式？
> 7. Exact sampling 为什么仍不消除 aliasing、matrix logarithm 非唯一与数值计算误差？

## 阅读前边界

- 一般 ODE 的 existence/uniqueness、Gronwall 与 maximal solution见[[常微分方程、初值问题与解的存在唯一性]]；
- matrix exponential 的 Jordan/Hermite/Cauchy 定义、缩放平方、action 与 Fréchet derivative见[[矩阵函数与矩阵指数]]；
- equilibrium classification 与 nonlinear linearization见[[相图、平衡点与局部稳定性]]；
- Lyapunov equation和energy certificate见[[Lyapunov 稳定性与能量函数]]；
- Euler/RK 的 order、stability region与step-size selection见[[Euler、Runge-Kutta 与离散化误差]]；
- 本章只建立线性 flow 的“解析传播—输入响应—精确采样—AI 状态空间”主线。

先用下图回答一个视觉问题：**状态转移、时间模态与零阶保持采样怎样组成同一条连续—离散传播链？**

![[00-知识库管理/_assets/figures/dynamics/fig-linear-ode-propagation-v2.svg|880]]

> [!figure] 图 10.9.2｜状态转移、谱时间行为与 ZOH 离散化
> A 用 $\Phi(t,s)$ 组织初值传播、composition/inverse 性质与 variation-of-constants 输入积分；B 将 $\operatorname{Re}\lambda$、Jordan chain 和 nonnormal basis 分别对应到渐近指数尾部、$t^je^{\lambda t}$ 因子和有限时间放大；C 从 $\dot x=Ax+Bu$ 经 $\bar A=e^{\Delta A}$ 与 $\bar B=\int_0^\Delta e^{\tau A}B\,d\tau$ 得到 ZOH 离散递推，并标出 recurrence/convolution 与 aliasing。来源：独立绘制；理论接口参考 linear systems、matrix functions 与 exact discretization；生成脚本：[[plot_dynamics_foundations_v2.py]]；确定性结构示意，无随机种子。

**怎样读图。** A 先把传播算子当作比单个解公式更基本的对象，composition 负责分段时间演化，variation of constants 把各时刻输入经 Green kernel 累加；B 再分清三个谱层次，不能只看 eigenvalue 实部解释短时间响应；C 最后在“输入每个采样间隔保持常数”的假设下推导 exact discrete matrices，再把状态递推展开为因果卷积。

**适用边界（图没有证明什么）。** 图主要针对有限维线性系统；时变 $A(t)$ 一般不能把 $\Phi$ 写成 $e^{\int A}$，除非相应矩阵可交换。ZOH 的“精确”只相对于 hold input model，不代表观测、参数或 exponential 计算无误，也不保证采样后可唯一恢复连续频率。非正规 transient 需要 norm、numerical abscissa 或 resolvent 的定量分析。

> [!note] 课程位置
> DYN-01 已证明在合适 regularity 与 growth 条件下，初值会选出唯一全局轨迹；本章把一般 $f$ 专门化为线性算子 $A$，第一次获得可计算的完整传播子 $\Phi(t,s)$。下一章不再只问“某个初值怎样走”，而要从 spectrum、trace/determinant 和 phase portrait 判断平衡点周围的全部轨道；DYN-04 再把显式传播压缩成无需解轨迹的标量证书。

> [!tip] 建议两遍阅读
> **第一遍**只对第一波统一振子完成 $A^2+A+I=0$、$e^{tA}$、一条初值轨迹和特征值四项手算。**第二遍**再进入一般 fundamental matrix、Peano–Baker、time ordering、variation of constants、ZOH、aliasing、非正规 transient 与 SSM。先看懂一个传播算子怎样同时编码解、旋转和衰减，再扩展到所有线性系统类型。

## 本章的推导问题链

1. 为什么线性系统不能只保存一条解，而要保存能传播任意初值的 fundamental matrix？
2. 归一化条件 $\Phi(s,s)=I$ 怎样消除 fundamental matrix 的右乘自由度？
3. 常矩阵 $A$ 时，幂级数为什么同时满足微分方程、初值和 semigroup composition？
4. Cayley–Hamilton 怎样把无限矩阵幂压缩到低维基底，从而手算 $e^{tA}$？
5. Eigenvalue 的实部/虚部、Jordan factor 与 nonnormal eigenbasis 分别控制哪种时间行为？
6. 输入项为什么要在每个过去时刻先注入、再由 $\Phi(t,s)$ 传播，形成 variation of constants？
7. ZOH 的 exact discretization 精确相对于什么假设，为什么仍有 exponential 计算、aliasing 和统计误差？

## 贯穿算例：同一振子的传播子、时间模态与体积收缩

沿用 DYN-01：

$$
\dot z=Az,
\qquad
A=
\begin{bmatrix}0&1\\-1&-1\end{bmatrix},
\qquad
z_0=(1,0)^T.
$$

### 符号与对象账本

| 对象 | 定义 | 本例中的值/作用 | 不可直接称为 |
|---|---|---|---|
| $A$ | infinitesimal generator | $\left[\begin{smallmatrix}0&1\\-1&-1\end{smallmatrix}\right]$ | 一步离散转移矩阵 |
| $e^{tA}$ | normalized propagator | 从 $0$ 传播到 $t$ | 逐元素 exponential |
| $\Phi(t,s)$ | state-transition matrix | $e^{(t-s)A}$ | 只属于某个初值的 trajectory |
| $\lambda_\pm$ | $A$ 的 eigenvalues | $-1/2\pm i\sqrt3/2$ | singular values |
| $\omega$ | oscillation frequency | $\sqrt3/2$ | spectral abscissa |
| $z(t)$ | propagated state | $e^{tA}z_0$ | phase portrait 全体 |
| $\det e^{tA}$ | oriented area scale | $e^{t\operatorname{tr}A}=e^{-t}$ | 单条轨迹的 norm |

### 第一步：Cayley–Hamilton 把所有高次幂折回 $I,A$

特征多项式是

$$
p(\lambda)=\lambda^2+\lambda+1,
$$

所以

$$
\boxed{A^2+A+I=0.}
$$

因此任何 $A^k$ 都能写成 $I$ 与 $A$ 的线性组合。与其逐项求无穷级数，不如先平移

$$
B=A+\frac12I,
\qquad
B^2=-\frac34I.
$$

$B$ 的平方像标量纯虚数一样闭合，这正是旋转三角函数出现的原因。

### 第二步：从标量指数模式得到矩阵指数

令

$$
\omega=\frac{\sqrt3}{2}.
$$

因为 $A=-\frac12I+B$ 且 $I,B$ 可交换，

$$
\boxed{
e^{tA}
=e^{-t/2}
\left[
I\cos(\omega t)
+\frac{2}{\sqrt3}B\sin(\omega t)
\right].
}
$$

展开为

$$
e^{tA}
=e^{-t/2}
\begin{bmatrix}
\cos(\omega t)+\frac1{\sqrt3}\sin(\omega t)
&\frac2{\sqrt3}\sin(\omega t)\\
-\frac2{\sqrt3}\sin(\omega t)
&\cos(\omega t)-\frac1{\sqrt3}\sin(\omega t)
\end{bmatrix}.
$$

两个检查缺一不可：$e^{0A}=I$；对上式求导后应等于 $Ae^{tA}$。

### 第三步：传播统一初值

乘以 $z_0=(1,0)^T$：

$$
\boxed{
z(t)=e^{-t/2}
\begin{bmatrix}
\cos(\omega t)+\frac1{\sqrt3}\sin(\omega t)\\[2mm]
-\frac2{\sqrt3}\sin(\omega t)
\end{bmatrix}.
}
$$

这条公式同时显示：振幅包络按 $e^{-t/2}$ 衰减，phase 按 $\omega$ 旋转。但“包络衰减”不能替代对每个 norm 的严格单调性判断；DYN-04 会用 Lyapunov derivative 做证书。

### 第四步：谱与体积各回答一件事

$$
\lambda_\pm=-\frac12\pm i\frac{\sqrt3}{2}
$$

给出衰减率与振荡频率。另一方面，Liouville determinant identity 给出

$$
\boxed{
\det e^{tA}=e^{t\operatorname{tr}A}=e^{-t}.
}
$$

它说明整个相平面的小面积按 $e^{-t}$ 收缩，而不是说每个向量长度都精确按 $e^{-t}$ 缩放。DYN-07 会把这条体积账接到 density evolution。

## 核心公式七问：$z(t)=e^{tA}z_0$ 究竟承诺了什么

1. **解决什么问题？** 给常系数 homogeneous IVP 的任意初值提供 exact state propagation。
2. **对象与形状？** $A\in\mathbb R^{d\times d}$，$e^{tA}\in\mathbb R^{d\times d}$，$z_0,z(t)\in\mathbb R^d$。
3. **从哪里来？** 矩阵幂级数满足 $\frac d{dt}e^{tA}=Ae^{tA}$ 与 $e^{0A}=I$；唯一性锁定它就是 flow。
4. **需要什么条件？** 这里 $A$ 为常矩阵；时变 $A(t)$ 一般需要 time-ordered propagator，不能随手写 $e^{\int A}$。
5. **怎样检查？** 检查初值、微分方程、semigroup $e^{(t+s)A}=e^{tA}e^{sA}$，并用 determinant/spectrum 做独立不变量核对。
6. **容易怎样误读？** 稳定 eigenvalues 不保证任意 norm 单调；公式精确也不表示数值计算 $e^{tA}v$ 无误。
7. **AI 中怎样调用？** 线性 SSM、局部 Neural ODE、ZOH discretization 与 convolution kernel 都调用传播作用；部署还必须记 sampling、input hold、matrix-function algorithm 与 parameter uncertainty。

> [!success] 第一遍停靠线
> 合上正文后，独立从 $A^2+A+I=0$ 推到 $B^2=-3I/4$，再写出 $e^{tA}$ 和 $z(t)$；能解释 $e^{-t/2}$、$\sqrt3/2$ 与 $e^{-t}$ 分别是 state mode 包络、角频率和面积缩放。若只能背最终矩阵，先不要进入 Peano–Baker 与 ZOH。

## 零、先把六类线性系统分开

### 0.1 齐次时变系统

$$
\dot x(t)=A(t)x(t).
$$

右端对 state 是 linear，但可以显含 time。若 $x_1,x_2$ 是解，$c_1x_1+c_2x_2$ 仍是解，这就是 superposition。

### 0.2 非齐次时变系统

$$
\dot x(t)=A(t)x(t)+g(t).
$$

解集一般不是 linear space，而是某个 particular solution 加 homogeneous solution space，因而是 affine set。

### 0.3 常系数 autonomous system

$$
\dot x(t)=Ax(t).
$$

$A$ 不随 time 变化，time translation symmetry使传播只依赖 $t-s$。

### 0.4 affine system

$$
\dot x=Ax+b.
$$

它不是关于 $x$ 的 linear map，除非 $b=0$；但可平移到 equilibrium，或增广 state 化为 homogeneous linear system。

### 0.5 input-state system

$$
\dot x=Ax+Bu.
$$

$u(t)$ 是外部输入，不是由 state equation 自动决定的未知量。只有声明 input function class/hold convention，问题才完整。

### 0.6 input-state-output system

$$
\dot x=Ax+Bu,
\qquad
y=Cx+Du.
$$

这里

$$
x\in\mathbb R^n,\quad
u\in\mathbb R^m,\quad
y\in\mathbb R^p,
$$

且

$$
A\in\mathbb R^{n\times n},
B\in\mathbb R^{n\times m},
C\in\mathbb R^{p\times n},
D\in\mathbb R^{p\times m}.
$$

内部 state mode 是否出现在 output 中，还取决于 $B,C$；只看 $A$ 的 spectrum不足以描述 input-output behavior。

## 一、为什么 fundamental matrix 是正确对象

考虑

$$
\dot x(t)=A(t)x(t),
\qquad A(t)\in\mathbb R^{n\times n}.
$$

若把 $n$ 个 vector solutions并排：

$$
X(t)=
\begin{bmatrix}
x_1(t)&\cdots&x_n(t)
\end{bmatrix},
$$

则

$$
\dot X(t)=A(t)X(t).
$$

> [!definition] Fundamental matrix
> 若 $X'(t)=A(t)X(t)$ 且 $X(t)$ 在 interval上可逆，则 $X$ 称该 homogeneous system 的 fundamental matrix。

它的columns是一组linearly independent solutions。任意初值 $x(s)=x_s$ 可写成

$$
x_s=X(s)c,
\qquad
c=X(s)^{-1}x_s,
$$

所以

$$
x(t)=X(t)X(s)^{-1}x_s.
$$

真正与初值传播有关、且不依赖选了哪一组basis solutions的对象是

$$
\boxed{
\Phi(t,s)=X(t)X(s)^{-1}.}
$$

### 1.1 为什么 fundamental matrix 不唯一

若 $X(t)$ 是 fundamental matrix，$R$ 是任意constant invertible matrix，则

$$
\widetilde X(t)=X(t)R
$$

仍满足

$$
\widetilde X'=A\widetilde X.
$$

反之，任意两组 fundamental matrices相差一个constant right factor：

$$
\widetilde X(t)=X(t)R.
$$

但是

$$
\widetilde X(t)\widetilde X(s)^{-1}
=X(t)RR^{-1}X(s)^{-1}
=\Phi(t,s),
$$

所以 normalized transition matrix 是basis-independent。

### 1.2 四条必须会证明的传播性质

$$
\boxed{\Phi(s,s)=I}
$$

$$
\boxed{\Phi(t,r)\Phi(r,s)=\Phi(t,s)}
$$

$$
\boxed{\Phi(t,s)^{-1}=\Phi(s,t)}
$$

$$
\boxed{
\partial_t\Phi(t,s)=A(t)\Phi(t,s).}
$$

composition proof只有一行：

$$
X(t)X(r)^{-1}X(r)X(s)^{-1}
=X(t)X(s)^{-1}.
$$

另外，对第二个time variable求导可得

$$
\boxed{
\partial_s\Phi(t,s)=-\Phi(t,s)A(s).}
$$

推导使用 inverse derivative：

$$
\frac d{ds}X(s)^{-1}
=-X(s)^{-1}X'(s)X(s)^{-1}
=-X(s)^{-1}A(s).
$$

### 1.3 Wronskian 与线性独立性不会中途丢失

定义

$$
W(t)=\det X(t).
$$

在 $X(t)$ 可逆处，Jacobi formula给

$$
\begin{aligned}
W'(t)
&=\det X(t)\operatorname{tr}(X(t)^{-1}X'(t))\\
&=W(t)\operatorname{tr}(X^{-1}AX)\\
&=\operatorname{tr}(A(t))W(t).
\end{aligned}
$$

因此

$$
\boxed{
W(t)=W(s)
\exp\left(\int_s^t\operatorname{tr}A(\tau)\,d\tau\right).}
$$

若 $W(s)\ne0$，则所有finite $t$ 上 $W(t)\ne0$。一组solutions不会在演化中突然变成linearly dependent。DYN-07 将把这个公式推广为 nonlinear flow 的 Jacobian-volume law。

## 二、常系数时，normalized fundamental matrix 就是矩阵指数

令 $A(t)\equiv A$。matrix exponential满足

$$
\frac d{dt}e^{(t-s)A}
=Ae^{(t-s)A},
\qquad
e^{0A}=I.
$$

由 DYN-01 的 uniqueness，normalized matrix IVP 的解唯一，因此

$$
\boxed{
\Phi(t,s)=e^{(t-s)A}.}
$$

于是

$$
\boxed{x(t)=e^{(t-s)A}x(s).}
$$

### 2.1 为什么这是 group，而不只是 forward semigroup

在 finite-dimensional ODE 中

$$
e^{tA}e^{sA}=e^{(t+s)A},
\qquad
(e^{tA})^{-1}=e^{-tA}.
$$

所以 $t\in\mathbb R$ 时形成one-parameter group。若只研究 $t\ge0$，常称 semigroup。无限维 PDE 中 backward operator可能不存在或不bounded，届时“semigroup vs group”会成为实质区别；本章不把finite-dimensional可逆性外推到所有演化方程。

### 2.2 “矩阵指数存在”与“数值上容易计算”是两件事

级数定义对每个方阵存在，但算法要区分：

- small/medium dense full $e^{tA}$：scaling-and-squaring/Padé 或 Schur；
- large sparse，只需 $e^{tA}v$：Krylov 或 exponential action；
- 要对 $A$ 求导：Fréchet derivative/adjoint action；
- 不用显式 Jordan basis 作一般浮点计算。

详细数值路线见[[矩阵函数与矩阵指数]]。

## 三、时变系统为什么不能随手写成 $e^{\int A}$

对

$$
x'=A(t)x,
$$

若猜

$$
\Phi(t,s)
=\exp\left(\int_s^tA(\tau)\,d\tau\right),
$$

对指数求导时会遇到：matrix exponent里面的matrix本身随 $t$ 变化，而且它一般不与其derivative交换。scalar calculus的

$$
\frac d{dt}e^{q(t)}=q'(t)e^{q(t)}
$$

不能无条件搬过来。

### 3.1 Picard iteration 给 Peano–Baker series

matrix integral equation是

$$
\Phi(t,s)
=I+\int_s^tA(\tau_1)\Phi(\tau_1,s)\,d\tau_1.
$$

反复代入：

$$
\begin{aligned}
\Phi(t,s)
&=I+\int_s^tA(\tau_1)\,d\tau_1\\
&\quad+
\int_s^t\int_s^{\tau_1}
A(\tau_1)A(\tau_2)
\,d\tau_2d\tau_1\\
&\quad+
\int_s^t\int_s^{\tau_1}\int_s^{\tau_2}
A(\tau_1)A(\tau_2)A(\tau_3)
\,d\tau_3d\tau_2d\tau_1+\cdots.
\end{aligned}
$$

later-time matrices出现在left side，这叫time ordering。

### 3.2 什么时候普通指数公式成立

若

$$
A(t_1)A(t_2)=A(t_2)A(t_1)
\qquad\forall t_1,t_2,
$$

则所有ordered products可自由换序，simplex integrals合并为factorials，从而

$$
\boxed{
\Phi(t,s)
=\exp\left(\int_s^tA(\tau)\,d\tau\right).}
$$

充分条件包括 $A(t)=a(t)A_0$，或全部 $A(t)$ 在同一固定basis中diagonal。

### 3.3 一个二段切换反例

令

$$
A_1=
\begin{bmatrix}0&1\\0&0\end{bmatrix},
\qquad
A_2=
\begin{bmatrix}0&0\\1&0\end{bmatrix},
$$

并令 $A(t)=A_1$ on $[0,1)$，$A(t)=A_2$ on $[1,2]$。由于 $A_1A_2\ne A_2A_1$，真实传播按时间顺序是

$$
\Phi(2,0)
=e^{A_2}e^{A_1}
=
\begin{bmatrix}1&0\\1&1\end{bmatrix}
\begin{bmatrix}1&1\\0&1\end{bmatrix}
=
\begin{bmatrix}1&1\\1&2\end{bmatrix}.
$$

而 naive expression是

$$
e^{A_1+A_2}
=e^{\left[\begin{smallmatrix}0&1\\1&0\end{smallmatrix}\right]}
=
\begin{bmatrix}
\cosh1&\sinh1\\
\sinh1&\cosh1
\end{bmatrix},
$$

两者不同。time-varying Jacobian的trajectory sensitivity也必须遵守同样的ordering。

## 四、从 spectrum 读 time mode，但不要只读 spectrum

### 4.1 Eigenvector mode

若

$$
Av=\lambda v,
$$

则

$$
e^{tA}v
=\sum_{k=0}^{\infty}\frac{t^kA^kv}{k!}
=e^{\lambda t}v.
$$

因此沿eigenvector：

- $\operatorname{Re}\lambda<0$：exponential decay；
- $\operatorname{Re}\lambda>0$：exponential growth；
- $\operatorname{Re}\lambda=0$：没有exponential envelope decay；
- $\operatorname{Im}\lambda$：oscillation frequency。

### 4.2 Complex conjugate pair 如何变成实振荡

实矩阵的non-real eigenvalues成conjugate pairs

$$
\lambda=a\pm ib.
$$

在相应二维real invariant subspace中，传播形如

$$
e^{at}
\begin{bmatrix}
\cos bt&-\sin bt\\
\sin bt&\cos bt
\end{bmatrix}
$$

再乘某个real coordinate transform。$a$ 控制envelope，$b$ 控制angular frequency；“complex state”不是产生oscillation的必要条件，real $2\times2$ block已经足够。

### 4.3 Jordan chain 带来 polynomial factor

对size-$r$ Jordan block

$$
J=\lambda I+N,
\qquad N^r=0,
$$

因为 $\lambda I$ 与 $N$ 交换：

$$
\boxed{
e^{tJ}
=e^{\lambda t}
\sum_{k=0}^{r-1}\frac{t^kN^k}{k!}.}
$$

所以 generalized eigenvector不是新exponential rate，而是在同一 $e^{\lambda t}$ 上附加

$$
1,t,\ldots,t^{r-1}.
$$

当 $\operatorname{Re}\lambda<0$，这些polynomial factors最终仍被exponential decay压过；但在finite time可显著放大。

### 4.4 Diagonalizable 不等于 numerical/modal explanation 可靠

若

$$
A=V\Lambda V^{-1},
$$

则

$$
e^{tA}=Ve^{t\Lambda}V^{-1}
$$

并有粗界

$$
\|e^{tA}\|
\le\kappa(V)e^{\alpha(A)t},
\qquad
\alpha(A)=\max_i\operatorname{Re}\lambda_i.
$$

若 $V$ ill-conditioned，mode coefficients可能很大且互相cancel；small perturbation也会剧烈改变eigenvectors。显式 diagonalization是exact algebra language，不是一般stable numerical algorithm。

## 五、长期稳定、有限时间放大与瞬时增长是三种问题

### 5.1 Hurwitz 判据

对固定finite-dimensional $A$，以下等价：

1. $\alpha(A)<0$；
2. $e^{tA}x_0\to0$ for every $x_0$；
3. 存在 $M\ge1,\beta>0$ 使

$$
\|e^{tA}\|\le Me^{-\beta t},
\qquad t\ge0.
$$

这样的 $A$ 称 Hurwitz。Jordan form证明：任选 $0<\beta<-\alpha(A)$，把有限次数polynomial factors吸收到constant $M$ 中。

### 5.2 Normal system 的二范数由 spectrum 精确控制

若 $A$ normal，则可unitarily diagonalize：

$$
\boxed{
\|e^{tA}\|_2=e^{\alpha(A)t}.}
$$

此时 $\alpha(A)<0$ 确实意味着operator 2-norm从 $1$ 单调decay。

### 5.3 Nonnormal system 可以先放大再衰减

取

$$
A_K=
\begin{bmatrix}
-1&K\\0&-2
\end{bmatrix}.
$$

虽然spectrum恒为 $\{-1,-2\}$，但

$$
e^{tA_K}
=
\begin{bmatrix}
e^{-t}&K(e^{-t}-e^{-2t})\\
0&e^{-2t}
\end{bmatrix}.
$$

在 $t=\log2$，off-diagonal response为 $K/4$。所以same eigenvalues不等于same finite-time dynamics。

### 5.4 Numerical abscissa 读瞬时 Euclidean growth

定义

$$
\omega(A)
=\lambda_{\max}\left(\frac{A+A^*}{2}\right).
$$

对 $x'=Ax$：

$$
\frac12\frac d{dt}\|x(t)\|_2^2
=x(t)^*\frac{A+A^*}{2}x(t).
$$

因此unit initial states的最大初始logarithmic growth rate由 $\omega(A)$ 控制。可能出现

$$
\alpha(A)<0
\quad\text{but}\quad
\omega(A)>0,
$$

即asymptotically stable却存在instantaneously growing direction。

> [!note] 四个不能互换的量
> $\alpha(A)$ 管asymptotic exponential rate；$M$ 管modal/nonnormal prefactor；$\omega(A)$ 管initial Euclidean growth；$\sup_{t\ge0}\|e^{tA}\|$ 管worst transient amplification。

完整数值曲线见[[实验 - 稳定非正规系统的矩阵指数瞬态]]与[[非正规矩阵、预解式与伪谱]]。

## 六、Variation of constants：输入在每个时刻都被传播

考虑time-varying inhomogeneous system

$$
x'(t)=A(t)x(t)+g(t),
\qquad x(s)=x_s.
$$

候选公式是

$$
\boxed{
x(t)=\Phi(t,s)x_s+
\int_s^t\Phi(t,\tau)g(\tau)\,d\tau.}
$$

解释：在time $\tau$ 注入的 infinitesimal state $g(\tau)d\tau$，需要由 $\Phi(t,\tau)$ 从 $\tau$ 传播到 $t$。

### 6.1 逐项验证

初值：

$$
x(s)=Ix_s+0=x_s.
$$

对 $t$ 求导，并用 Leibniz rule：

$$
\begin{aligned}
x'(t)
&=A(t)\Phi(t,s)x_s
+\Phi(t,t)g(t)\\
&\quad+
\int_s^tA(t)\Phi(t,\tau)g(\tau)\,d\tau\\
&=A(t)x(t)+g(t).
\end{aligned}
$$

由 uniqueness，该候选就是唯一解。

### 6.2 常系数版本

若 $A(t)\equiv A$：

$$
\boxed{
x(t)=e^{(t-s)A}x_s
+\int_s^t e^{(t-\tau)A}g(\tau)\,d\tau.}
$$

不要把第二项误写成 $e^{(t-s)A}\int_s^tg(\tau)d\tau$；不同injection times拥有不同propagation duration。

## 七、从 state response 到 causal convolution

考虑 LTI input-output system

$$
\dot x=Ax+Bu,
\qquad
y=Cx+Du.
$$

从 $s=0$：

$$
x(t)=e^{tA}x_0
+\int_0^te^{(t-\tau)A}Bu(\tau)\,d\tau.
$$

所以

$$
y(t)=Ce^{tA}x_0
+\int_0^tCe^{(t-\tau)A}Bu(\tau)\,d\tau
+Du(t).
$$

定义strictly proper state-to-output kernel

$$
K(t)=Ce^{tA}B,
\qquad t\ge0,
$$

则zero initial state的dynamic part是causal convolution：

$$
(K*u)(t)
=\int_0^tK(t-\tau)u(\tau)\,d\tau.
$$

### 7.1 为什么 spectrum 可能在 output 中“看不见”

若 $Av=\lambda v$ 但 $Cv=0$，沿 $v$ 的internal mode不出现在output；若left eigenvector $w^*$ 满足 $w^*B=0$，input也激发不了该mode。于是：

$$
\text{spectrum of }A
\not\Rightarrow
\text{all visible input-output modes}.
$$

controllability/observability将在后续高级控制接口中系统处理；本章先保留这个反例意识。

### 7.2 Constant input 的 equilibrium

若 $u(t)\equiv u_*$ 且 $A$ invertible，equilibrium满足

$$
0=Ax_*+Bu_*.
$$

所以

$$
\boxed{x_*=-A^{-1}Bu_*.}
$$

令 $z=x-x_*$，则 $z'=Az$，故

$$
x(t)=x_*+e^{tA}(x_0-x_*).
$$

若 $A$ Hurwitz，$x(t)\to x_*$。实现中不应显式形成 $A^{-1}$，而应解 $Ax_*=-Bu_*$。

### 7.3 Bounded input 的 state bound

若

$$
\|e^{tA}\|\le Me^{-\beta t}
$$

且 $\|u(t)\|\le U$，则

$$
\begin{aligned}
\|x(t)\|
&\le Me^{-\beta t}\|x_0\|
+M\|B\|U\int_0^te^{-\beta(t-\tau)}d\tau\\
&\le Me^{-\beta t}\|x_0\|
+\frac{M\|B\|}{\beta}U.
\end{aligned}
$$

这说明Hurwitz state dynamics对bounded input有uniform state bound；output还需乘 $C$ 并加入 $Du$。

## 八、零阶保持下的 exact sampling

令sampling interval为 $\Delta>0$，并假设

$$
u(t)=u_k,
\qquad t\in[k\Delta,(k+1)\Delta).
$$

variation of constants给

$$
x_{k+1}
=e^{\Delta A}x_k
+\int_0^\Delta e^{(\Delta-\tau)A}B\,d\tau\,u_k.
$$

定义

$$
\boxed{\bar A=e^{\Delta A},}
$$

$$
\boxed{
\bar B
=\int_0^\Delta e^{sA}B\,ds.}
$$

于是

$$
\boxed{x_{k+1}=\bar A x_k+\bar B u_k.}
$$

### 8.1 “Exact”究竟指什么

这个recurrence在以下合同下exact：

1. continuous model确实是constant $A,B$；
2. input在每个interval按zero-order hold保持；
3. $\bar A,\bar B$ 被精确计算；
4. 不计floating-point roundoff。

真实input在interval内变化时，ZOH 本身就是input approximation；matrix exponential算法也可能有数值误差。不能只看到“exact discretization”四个字便删除误差账本。

### 8.2 不要默认使用 $A^{-1}$

若 $A$ invertible：

$$
\bar B=A^{-1}(e^{\Delta A}-I)B.
$$

但 $A$ 可能singular/ill-conditioned。更稳健的结构公式是

$$
\boxed{
\exp\left(
\Delta
\begin{bmatrix}A&B\\0&0\end{bmatrix}
\right)
=
\begin{bmatrix}
\bar A&\bar B\\0&I
\end{bmatrix}.}
$$

### 8.3 小步长 sanity check

由series：

$$
\bar A=I+\Delta A+O(\Delta^2),
$$

$$
\bar B=\Delta B+\frac{\Delta^2}{2}AB+O(\Delta^3).
$$

所以first-order limit确实回到forward Euler，但finite $\Delta$ 的 exact matrices包含所有高阶传播。

### 8.4 Irregular sampling

若time gaps为 $\Delta_k=t_{k+1}-t_k$：

$$
x_{k+1}
=e^{\Delta_kA}x_k
+\left(\int_0^{\Delta_k}e^{sA}Bds\right)u_k.
$$

continuous parameterization天然允许重新计算不同gap的transition；但这只是modeling convenience，不自动保证对unseen gaps的statistical generalization。

## 九、连续 spectrum 如何映到离散 spectrum

spectral mapping theorem给

$$
\boxed{
\sigma(\bar A)
=\{e^{\Delta\lambda}:\lambda\in\sigma(A)\}.}
$$

若 $\lambda=a+ib$：

$$
|e^{\Delta\lambda}|=e^{\Delta a},
\qquad
\arg(e^{\Delta\lambda})=\Delta b\pmod{2\pi}.
$$

因此：

- continuous $\operatorname{Re}\lambda<0$ 对应 discrete $|\mu|<1$；
- continuous decay time scale由 $a$ 映成geometric factor $e^{\Delta a}$；
- frequency只在modulo $2\pi/\Delta$ 意义下可见。

### 9.1 Sampling aliasing

对任意integer $k$：

$$
e^{\Delta(\lambda+2\pi ik/\Delta)}
=e^{\Delta\lambda}.
$$

所以不同continuous frequencies产生同一sampled eigenvalue。仅从 $\bar A$ 一般不能唯一恢复 $A$；matrix logarithm存在branch ambiguity。

若额外限制continuous frequencies到Nyquist strip、固定log branch，并排除branch cut/pathology，才可能选定principal candidate：

$$
A=\frac1\Delta\log\bar A.
$$

这是带先验的identification，不是纯代数唯一性。

### 9.2 Stable discrete matrix 不代表你知道唯一 continuous generator

$\rho(\bar A)<1$ 表示discrete recurrence asymptotically stable；它可能来自许多不同continuous generators。更进一步，任意invertible discrete matrix是否存在real logarithm也有额外谱/Jordan条件。因此“先训练任意 $\bar A$，再无条件取real log得到continuous ODE”并不成立。

## 十、Discrete SSM 的 recurrence–convolution equivalence

令

$$
x_{k+1}=\bar A x_k+\bar B u_k,
\qquad
y_k=Cx_k+Du_k.
$$

递推展开：

$$
x_k
=\bar A^kx_0
+\sum_{j=0}^{k-1}
\bar A^{k-1-j}\bar B u_j.
$$

若 $x_0=0$：

$$
y_k
=Du_k+
\sum_{j=0}^{k-1}
C\bar A^{k-1-j}\bar B u_j.
$$

定义causal kernel

$$
K_0=D,
\qquad
K_\ell=C\bar A^{\ell-1}\bar B,
\quad \ell\ge1,
$$

则

$$
\boxed{
y_k=\sum_{j=0}^{k}K_{k-j}u_j.}
$$

同一个linear time-invariant model因此有两种计算视图：

| 视图 | 计算方式 | 典型优势 | 风险 |
|---|---|---|---|
| recurrence | 顺序更新state | streaming、constant state memory | time-parallelism有限 |
| convolution | 预计算kernel后卷积 | training可FFT/parallel | kernel生成、截断与conditioning |

数学等价不等于finite-precision、memory traffic和parallel runtime相同。

## 十一、Memory 不是“某个 eigenvalue 靠近 1”这么简单

若discrete eigenvalue $|\mu|<1$，scalar impulse response按 $|\mu|^k$ decay；$|\mu|$ 越接近 $1$，memory time scale越长。continuous rate $\lambda$ 对应

$$
\mu=e^{\Delta\lambda}.
$$

但sequence memory还取决于：

1. input是否通过 $B$ 激发该mode；
2. output是否通过 $C$ 读取该mode；
3. eigenvector/Jordan geometry是否带来transient或cancellation；
4. finite precision是否能分辨非常接近unit circle的decay；
5. training能否识别并优化这些parameters；
6. nonlinear gates/normalization是否改变linear analysis。

因此“所有eigenvalues靠近unit circle ⇒ 模型一定有好长记忆”不是定理。

## 十二、HiPPO、S4 与连续记忆接口

### 12.1 HiPPO 的问题是什么

HiPPO把持续到来的signal投影到一组随time更新的orthogonal polynomial basis上，并推导projection coefficients的online dynamics。某些构造产生linear ODE：

$$
\dot x(t)=A(t)x(t)+B(t)u(t).
$$

关键对象是“当前state怎样压缩过去function”，不只是任意stable matrix。

### 12.2 Time-varying 与 LTI 使用必须分层

原始projection derivation可产生time-varying dynamics；后续模型可能通过change of variables、time rescaling、particular initialization或直接把相关matrix用于LTI SSM。它们可能相互关联，但需要逐条检查：

- measure/basis是否仍相同；
- $A(t),B(t)$ 怎样变成constant $A,B$；
- discretization使用什么step/hold；
- 原approximation guarantee是否随变换保留。

不能因都叫“HiPPO matrix”便默认theorem自动迁移。

### 12.3 S4 的结构性主张

S4从linear state-space sequence model出发，利用structured parameterization把long convolution kernel计算转成更高效的结构问题。这里至少有四层：

1. continuous/discrete SSM identity；
2. HiPPO-inspired initialization/structure；
3. kernel generation的algebra and algorithm；
4. benchmark performance。

前两层的mathematical elegance不自动证明第四层对所有tasks成立；实验也不能反向证明所有continuous-time interpretation。

### 12.4 Diagonal state matrix 的收益与损失

若 $A$ diagonal，$e^{\Delta A}$ 与kernel可逐mode并行计算；但这是一种hypothesis-class restriction。它删除一般nonnormal coupling和Jordan geometry。complex diagonal modes可表达damped oscillations，却不等于一般real linear system的全部finite-time behavior。

## 十三、Linearized Neural ODE 是时变系统，不通常是 $e^{tA}$

对nonlinear trajectory

$$
\dot z=f(t,z),
$$

一个small perturbation $\delta z$ 满足first-order variational equation

$$
\delta\dot z(t)
=J_f(t,z(t))\delta z(t).
$$

记

$$
A(t)=J_f(t,z(t)).
$$

则sensitivity是time-varying transition matrix：

$$
\delta z(t)=\Phi(t,s)\delta z(s).
$$

一般不能写成

$$
\exp\left(\int_s^tJ_f(\tau,z(\tau))d\tau\right)
$$

除非different-time Jacobians commute或使用time-ordered exponential。把trajectory-average Jacobian直接指数化是一种approximation，需要error analysis，不是identity。

### 13.1 常系数局部线性化何时合理

在equilibrium $z_*$ 附近，若 $f$ autonomous 且

$$
f(z_*)=0,
$$

则

$$
\delta\dot z\approx J_f(z_*)\delta z
$$

使用constant Jacobian。它描述local infinitesimal behavior；离开neighborhood、跨越activation regions或trajectory本身快速变化时，constant approximation可能失效。

### 13.2 对 $A$ 求导不是简单左乘

若layer使用 $e^{\Delta A}$，parameter perturbation $E$ 的correct first variation是

$$
L_{\exp}(\Delta A,\Delta E)
=\int_0^1
e^{(1-r)\Delta A}
(\Delta E)
e^{r\Delta A}
dr.
$$

只有 $A$ 与 $E$ commute时才化为 $e^{\Delta A}\Delta E$。详证与adjoint computation见[[矩阵函数与矩阵指数]]、[[矩阵函数的 Fréchet 导数]]。

## 十四、连续参数化并不自动带来这些性质

| 常见主张 | 还缺什么 |
|---|---|
| $\operatorname{Re}\lambda(A)<0$，所以所有hidden norms单调下降 | normal/dissipative condition或energy metric |
| exact discretization，所以没有numerical error | hold error、matrix exponential error、roundoff |
| discrete recurrence来自continuous ODE，所以 $A$ uniquely identifiable | log branch、sampling rate、real-log条件 |
| diagonal SSM stable，所以一定有long memory | $B,C$ visibility、time scale、precision和training |
| continuous model可处理irregular sampling，所以能泛化到new gaps | data support、observation model与held-out gap experiment |
| linearized Neural ODE等于 $e^{\int J}$ | different-time Jacobian commutativity/time ordering |
| recurrence和convolution数学等价，所以runtime相同 | kernel generation、parallel hardware、sequence length |

## 十五、五层误差与声明账本

### 15.1 Model error

真实系统未必linear/time-invariant；latent state也可能不可辨识。

### 15.2 Input representation error

ZOH、first-order hold、interpolation与missing-data convention会改变 $\bar B$ 和实际trajectory。

### 15.3 Propagator computation error

$e^{\Delta A}$、action或augmented exponential是numerical output；报告algorithm、tolerance与residual/refinement。

### 15.4 Parameter and sampling identifiability

finite samples只看到 $e^{\Delta A}$ 的某些input-output consequences；aliasing、unobservable modes与similarity transforms会产生nonuniqueness。

### 15.5 Statistical validity

training fit、long-context benchmark、irregular-time generalization和robustness都需要held-out evidence；不由linear systems theorem自动提供。

## 十六、一个可执行的线性动力学审计

对于learned或designed linear SSM，至少报告：

1. continuous $A,B,C,D$ 与sampling interval/units；
2. discretization convention（ZOH/other）和 $\bar A,\bar B$ computation；
3. $\alpha(A)$、$\rho(\bar A)$ 与spectral mapping residual；
4. $\omega(A)$、sampled $\|e^{tA}\|$ 与transient peak；
5. semigroup residual

$$
\|e^{(t+s)A}-e^{tA}e^{sA}\|;
$$

6. augmented-exponential block residual；
7. recurrence vs direct convolution output difference；
8. refinement across precision/tolerance/step representation；
9. impulse/step response与mode visibility；
10. long-horizon state norm、NAN/overflow和worst samples。

本章直接复用[[实验 - 稳定非正规系统的矩阵指数瞬态]]作为nonnormal audit；后续 DYN-05/06 再建立solver order与stiffness实验。

## 十七、Claim ladder

| 已有证据 | 可以声称 | 仍不能声称 |
|---|---|---|
| $e^{tA}$ formula verified | constant linear IVP exact solution | computed result high accuracy |
| $\alpha(A)<0$ | asymptotic/exponential stability | norm monotonicity、small transient |
| $\omega(A)\le0$ | Euclidean norm nonincrease | fast asymptotic decay |
| ZOH matrices verified | held-input continuous/discrete equivalence | arbitrary input exactness |
| recurrence = convolution numerically | two implementations agree | model statistically adequate |
| sampled fit good | discrete input-output behavior fit | unique continuous generator |
| HiPPO/S4 theorem conditions matched | corresponding approximation/algorithm claim | universal long-context superiority |

## 十八、常见误区

1. **把 $e^{tA}$ 逐元素计算**：matrix exponential由matrix powers定义；
2. **把任意 fundamental matrix 当作 normalized transition**：必须乘 $X(s)^{-1}$；
3. **对time-varying system直接写 $e^{\int A}$**：需要different-time commutativity；
4. **只看eigenvalues画finite-time结论**：还需Jordan/eigenvector geometry；
5. **把Hurwitz等同于norm monotone**：nonnormal transient可先放大；
6. **把diagonalizable等同于numerically safe**：$V$ 可ill-conditioned；
7. **把input响应写成同一个传播时长**：每个 $\tau$ 要用 $e^{(t-\tau)A}$；
8. **默认 $A^{-1}(e^{\Delta A}-I)B$**：singular/ill-conditioned时用augmented exponential/action；
9. **把ZOH exactness扩展到arbitrary input**：hold assumption是合同一部分；
10. **从 $\bar A$ 唯一恢复 $A$**：matrix log有branch与real-existence问题；
11. **只凭 $A$ spectrum宣称memory**：还需 $B,C$ visibility；
12. **把original HiPPO time-varying derivation与LTI use混同**：逐项核对变换与guarantee；
13. **把linearized Neural ODE写成constant matrix exponential**：trajectory Jacobian通常time-varying；
14. **把exact algebra当exact floating-point result**：算法和conditioning仍需验收。

## 十九、掌握标准

### Level 1：对象识别

- 区分 $X(t)$、$\Phi(t,s)$、$e^{tA}$、$x(t)$ 与 sampled $x_k$；
- 区分 homogeneous/inhomogeneous、LTI/time-varying和state/output。

### Level 2：手算

- 对diagonal、rotation、Jordan/triangular $A$ 计算 $e^{tA}x_0$；
- 对scalar/low-dimensional SSM求 $\bar A,\bar B$ 与kernel。

### Level 3：证明

- 重建fundamental-matrix composition、Wronskian和variation of constants；
- 从Jordan form证明Hurwitz exponential bound；
- 证明recurrence–convolution与spectral mapping。

### Level 4：边界

- 构造noncommuting time-varying、nonnormal transient、unobservable mode与sampling aliasing反例；
- 不把algebraic exactness升级为numerical/statistical claim。

### Level 5：AI 迁移

- 审计HiPPO/S4/linear RNN的continuous–discrete contract；
- 为linearized Neural ODE保留time ordering；
- 用spectrum、transient、visibility、sampling和resource evidence共同评估linear state model。

## 二十、自测问题

1. Fundamental matrix为何不唯一而 $\Phi(t,s)$ 唯一？
2. $\partial_s\Phi(t,s)$ 为什么有负号？
3. Wronskian为何不会从nonzero变成zero？
4. constant $A$ 的传播为什么只依赖 $t-s$？
5. $A(t_1),A(t_2)$ 不交换时，哪一步破坏 $e^{\int A}$？
6. Jordan size如何转成 $t^ke^{\lambda t}$？
7. $\alpha(A)$、$\omega(A)$ 和transient peak分别回答什么？
8. Variation-of-constants中为什么是 $\Phi(t,\tau)g(\tau)$？
9. ZOH exact discretization的“exact”依赖哪些假设？
10. 为什么不用 $A^{-1}$ 计算 $\bar B$？
11. Continuous stability怎样映到unit disk？
12. Sampling为何使frequency只能modulo $2\pi/\Delta$识别？
13. Recurrence与convolution kernel怎样互推？
14. Stable hidden mode为何可能对output完全不可见？
15. Nonlinear Neural ODE的sensitivity为何通常是time-ordered system？

## 二十一、来源与证据边界

1. MIT 18.03SC, [Matrix Exponentials](https://ocw.mit.edu/courses/18-03sc-differential-equations-fall-2011/pages/unit-iv-first-order-systems/matrix-exponentials/)：general linear systems、fundamental matrix、existence/uniqueness和variation of parameters；
2. Stanford EE263, [Introduction to Linear Dynamical Systems archive](https://ee263.stanford.edu/archive/)：autonomous dynamics、matrix exponential、modes、input-output/convolution与state-space课程主线；
3. Higham & Lin, [Matrix Functions: A Short Course](https://eprints.maths.manchester.ac.uk/2067/)：matrix exponential定义、算法、action和Fréchet derivative前置；
4. Gu et al., [HiPPO](https://proceedings.neurips.cc/paper_files/paper/2020/hash/102f0bb6efb3a6128a3c750dd16729be-Abstract.html), NeurIPS 2020：continuous signal memory与polynomial projection dynamics；
5. Gu, Goel & Ré, [Efficiently Modeling Long Sequences with Structured State Spaces](https://openreview.net/forum?id=uYLFoz1vlAC), ICLR 2022：S4的structured SSM与long-sequence computation；
6. Gu et al., [How to Train your HiPPO](https://openreview.net/forum?id=klK17OQ3KB), ICLR 2023：time-varying HiPPO derivation与LTI SSM use之间的理论重审；
7. 苏剑林，[重温 SSM（一）：线性系统和 HiPPO 矩阵](https://spaces.ac.cn/archives/10114)：linear ODE、HiPPO与SSM的中文AI问题入口。

> [!info] 证据分工
> MIT/Stanford承担linear systems标准定义、传播与输入输出证明；Higham承担matrix exponential的函数演算与numerical boundary；HiPPO/S4原论文承担特定memory construction和structured algorithm；科学空间承担中文推导入口。本章的claim ladder、sampling identifiability、time-ordering与AI audit是课程组织，不把特定benchmark或形式类比升级为普适模型优越性定理。

## 二十二、配套训练

- 习题：[[习题 - 线性 ODE 与矩阵指数]]
- 详解：[[解答 - 线性 ODE 与矩阵指数]]
- 分卷导航：[[ODE、动力系统与 SDE MOC]]
- 复现实验：[[实验 - 稳定非正规系统的矩阵指数瞬态]]
- 后继：[[相图、平衡点与局部稳定性]]、[[Lyapunov 稳定性与能量函数]]、[[Euler、Runge-Kutta 与离散化误差]]
