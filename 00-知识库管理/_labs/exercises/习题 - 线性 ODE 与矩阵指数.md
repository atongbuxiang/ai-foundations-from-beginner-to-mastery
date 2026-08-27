---
type: exercise
status: draft
area: [math/ode, math/linear-systems, ai/state-space-models]
topic: "线性 ODE 与矩阵指数"
difficulty: [A, B, C, D, E]
prerequisites: ["[[线性 ODE 与矩阵指数]]"]
related: ["[[ODE、动力系统与 SDE MOC]]", "[[练习与测验 MOC]]", "[[矩阵函数与矩阵指数]]"]
solution: "[[解答 - 线性 ODE 与矩阵指数]]"
created: 2026-08-19
updated: 2026-08-19
---

# 习题 - 线性 ODE 与矩阵指数

> [!abstract] 训练目标
> 把 matrix exponential 从静态矩阵函数读成传播算子；能够从 fundamental matrix 重建时变传播，从 spectrum/Jordan/geometry 解释时间行为，从 variation of constants 推出 input convolution，并审计 continuous SSM 到 sampled recurrence 的全部假设。

> [!warning] 作答约定
> 必须区分 continuous $x(t)$、exact sampled value $x(t_k)$ 与 computed state $x_k$；使用“稳定”“精确”“等价”时，同时声明 norm、time range、input hold、sampling interval 和 numerical assumptions。

## A. 识别与复述

### DYN-LIN-A01

定义或解释 homogeneous/inhomogeneous、autonomous/time-varying、affine、input-state-output system、fundamental matrix $X(t)$、normalized transition $\Phi(t,s)$ 与 Wronskian。写出 $\Phi$ 的 identity、composition、inverse、$t$-derivative和 $s$-derivative，并说明 $X$ 不唯一而 $\Phi$ 唯一的原因。

### DYN-LIN-A02

建立以下对象到时间行为的字典：real eigenvalue、complex conjugate pair、Jordan chain、spectral abscissa $\alpha(A)$、numerical abscissa $\omega(A)$、normality、conditioned eigenvector basis 与 transient amplification。指出哪些结论是 asymptotic，哪些是 instantaneous 或 finite-time。

### DYN-LIN-A03

完整写出 continuous LTI SSM

$$
\dot x=Ax+Bu,
\qquad y=Cx+Du
$$

在 zero-order hold、sampling interval $\Delta$ 下的 discrete model。解释“exact discretization”的精确对象、recurrence–convolution equivalence、continuous/discrete spectral mapping、sampling aliasing，以及 model/hold/propagator/identifiability/statistical 五层误差。

## B. 手算与构造

### DYN-LIN-B01

令

$$
A=
\begin{bmatrix}
-1&2\\0&-2
\end{bmatrix}.
$$

1. 计算 $e^{tA}$；
2. 对 $x(0)=e_2$ 求 $x(t)$；
3. 验证 $x'=Ax$ 与初值；
4. 取 $X(t)=e^{tA}$，计算 Wronskian并与 $\exp(t\operatorname{tr}A)$ 比较；
5. 写出 $\Phi(t,s)$ 并验证 composition property。

### DYN-LIN-B02

考虑 nonnormal Jordan system

$$
A=
\begin{bmatrix}
-1&4\\0&-1
\end{bmatrix},
\qquad x(0)=e_2.
$$

1. 求 $e^{tA}$ 与 $x(t)$；
2. 找出 first component 的最大值及到达时间；
3. 证明 $\|x(1)\|_2>\|x(0)\|_2$，尽管 $\alpha(A)=-1$；
4. 计算 $\omega(A)$；
5. 解释 polynomial factor、asymptotic decay、instantaneous direction与finite-time amplification的关系。

### DYN-LIN-B03

考虑 scalar SSM

$$
\dot x=-x+2u,
\qquad y=x,
$$

取 $\Delta=\log2$，并在每个sample interval上zero-order hold。

1. 求 exact $\bar A,\bar B$；
2. 从 $x_0=0$ 和 inputs $(u_0,u_1,u_2)=(1,0,1)$ 计算 $x_1,x_2,x_3$；
3. 写出 convolution kernel $K_\ell$；
4. 写出同一步长的forward Euler recurrence并比较前三步；
5. 检验小 $\Delta$ limit中 $\bar A,\bar B$ 的一阶项。

## C. 推导与证明

### DYN-LIN-C01

对continuous $A(t)$：

1. 从两组 fundamental matrices证明它们相差constant invertible right factor；
2. 证明 $\Phi(t,r)\Phi(r,s)=\Phi(t,s)$、$\Phi(t,s)^{-1}=\Phi(s,t)$；
3. 推导 $\partial_s\Phi(t,s)=-\Phi(t,s)A(s)$；
4. 用 Jacobi formula 推导 Wronskian/Liouville formula；
5. 从 integral equation 写出 Peano–Baker series前三阶；
6. 证明 pairwise commutativity $A(t_1)A(t_2)=A(t_2)A(t_1)$ 时它化为 $\exp(\int_s^tA)$；
7. 用正文的 $A_1,A_2$ 二段系统验证无交换性时 naive formula失败。

### DYN-LIN-C02

1. 推导time-varying variation-of-constants formula；
2. 对 LTI input-output system推导causal kernel $K(t)=Ce^{tA}B$；
3. 若 $\|e^{tA}\|\le Me^{-\beta t}$ 且 $\|u\|_\infty\le U$，证明 uniform state bound；
4. 对discrete SSM从recurrence推导

$$
x_k=\bar A^kx_0+
\sum_{j=0}^{k-1}\bar A^{k-1-j}\bar Bu_j
$$

以及 output convolution；
5. 说明 continuous convolution与discrete convolution分别在哪一步使用time invariance。

### DYN-LIN-C03

对ZOH sampled LTI system：

1. 从 variation of constants 推导 $\bar A,\bar B$；
2. 证明augmented exponential block formula；
3. 推导 $\bar A=I+\Delta A+O(\Delta^2)$ 与 $\bar B=\Delta B+\frac12\Delta^2AB+O(\Delta^3)$；
4. 证明 $\sigma(\bar A)=e^{\Delta\sigma(A)}$；
5. 证明 $\lambda$ 与 $\lambda+2\pi ik/\Delta$ 产生相同sampled eigenvalue；
6. 解释在何种额外frequency strip/log-branch条件下才可讨论从 $\bar A$ 选取一个continuous generator。

## D. 反例与失败边界

### DYN-LIN-D01

判断并修正：

1. $\alpha(A)<0$，所以 $\|e^{tA}\|_2$ 必单调下降；
2. 两个矩阵有相同eigenvalues，所以有相同finite-time response；
3. $A$ diagonalizable，所以显式 $Ve^{t\Lambda}V^{-1}$ 数值可靠；
4. $A(t)$ continuous，所以 $\Phi(t,s)=\exp(\int_s^tA)$；
5. $\rho(\bar A)<1$，所以存在唯一real Hurwitz $A$ 满足 $\bar A=e^{\Delta A}$；
6. ZOH discretization exact，所以任意continuous input都被exact表示。

### DYN-LIN-D02

令

$$
A=\operatorname{diag}(-1,-2),
\qquad B=e_1,
\qquad C=e_2^{\mathsf T},
\qquad D=0.
$$

1. 计算zero-state input-output kernel并说明为何恒为零；
2. 取 $x_0=e_2$，计算zero-input output；
3. 说明同一个internal eigenvalue为何可能“不能被input激发”或“不能被output读取”；
4. 构造新的 $B,C$ 使两个modes都出现在kernel；
5. 反驳“$A$ 的 eigenvalues靠近unit circle便自动得到可用长记忆”。

### DYN-LIN-D03

取 $\Delta=1$，对任意integer $k$ 定义real generators

$$
A_k=
\begin{bmatrix}
-1&-(\omega+2\pi k)\\
\omega+2\pi k&-1
\end{bmatrix}.
$$

1. 计算 $e^{A_k}$ 并证明它与 $k$ 无关；
2. 说明sampled trajectory为何不能区分这些continuous frequencies；
3. 若training只观察integer times，设计一个额外采样/先验方案减少ambiguity；
4. 解释这为什么是identifiability failure，而不是matrix exponential solver error。

## E. AI 迁移

### DYN-LIN-E01

为一个用于long-sequence modeling的linear SSM建立审计协议。要求覆盖continuous parameterization、discretization/hold、$A/B/C$ mode visibility、recurrence与convolution一致性、nonnormal transient、kernel truncation、precision、irregular gaps、resource matching和held-out long-context标准。给出至少三条可被实验推翻的acceptance criteria。

### DYN-LIN-E02

对 Neural ODE trajectory $z'(t)=f(t,z(t))$：

1. 推导perturbation equation $\delta z'=J_f(t,z(t))\delta z$；
2. 写出其transition matrix与Peano–Baker representation；
3. 给出different-time Jacobians commute时的simplification；
4. 构造piecewise-constant noncommuting Jacobian说明order matters；
5. 说明为什么用average Jacobian的eigenvalues解释整条trajectory只是approximation。

### DYN-LIN-E03

设计实验区分以下三种收益来源：

1. continuous-time parameter sharing/irregular-time modeling；
2. exact ZOH discretization或更准确propagator；
3. 更大的计算/参数预算。

必须给出matched discrete RNN、Euler-like residual、exact-discrete SSM三类基线，规定sampling rates、tolerance/precision、parameter/FLOP matching、aliasing stress test、recurrence–convolution check、long-horizon metrics和失败日志。

