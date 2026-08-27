---
type: exercise
status: draft
area: [math/probability, math/stochastic-processes, math/sde, math/numerical-analysis, ai/generative-modeling]
topic: "Itô 引理与随机微分方程"
difficulty: [A, B, C, D, E]
prerequisites: ["[[Itô 引理与随机微分方程]]", "[[随机过程、Brownian 运动与二次变差]]", "[[常微分方程、初值问题与解的存在唯一性]]", "[[Euler、Runge-Kutta 与离散化误差]]"]
related: ["[[ODE、动力系统与 SDE MOC]]", "[[练习与测验 MOC]]", "[[实验 - Itô 和、SDE 强弱误差与离散梯度审计]]"]
solution: "[[解答 - Itô 引理与随机微分方程]]"
created: 2026-08-19
updated: 2026-08-19
---

# 习题 - Itô 引理与随机微分方程

> [!abstract] 训练目标
> 从“会背 $dW^2=dt$”升级为能从适应随机和与条件期望重建 Itô integral；能对 scalar/multidimensional SDE 做链式法则、解概念和适定性审计；能把 exact model、finite-step solver、strong/weak error 与训练梯度分层。

> [!warning] 作答约定
> 每道随机积分题必须写 filtration/adaptedness；每道极限题必须写 convergence mode；每道 SDE 题必须声明 Itô/Stratonovich；每道数值题必须写 Brownian coupling；每道梯度题必须说明验证的是 $J$ 还是 $J_h$。

## A. 定义、因果与等距

### DYN-ITO-A01

为

$$
dX_t=a(t,X_t)\,dt+B(t,X_t)\,dW_t
$$

制作完整 object card，至少包括：

1. probability space、filtration、state/noise dimension；
2. Brownian motion 相对于哪个 filtration；
3. initial variable 的可测性、矩条件与独立性；
4. coefficient 的 measurability、adaptedness、Lipschitz/growth；
5. Itô 或 Stratonovich；
6. strong/weak solution；
7. pathwise uniqueness/uniqueness in law；
8. global/explosion policy；
9. numerical coupling、strong/weak target；
10. neural coefficient 情形下 model/solver/gradient 三层。

解释 differential notation 本身为何不包含上述合同。

### DYN-ITO-A02

在 partition

$$
0=t_0<t_1<t_2=T
$$

上令

$$
H_t=H_0\mathbf1_{(t_0,t_1]}(t)
+H_1\mathbf1_{(t_1,t_2]}(t),
$$

其中 $H_0\in\mathcal F_{t_0}$、$H_1\in\mathcal F_{t_1}$ 且平方可积。

1. 写出 $\int_0^TH_t\,dW_t$ 的定义；
2. 证明其均值为0；
3. 展开平方并证明 cross term 为0；
4. 推出 Itô isometry；
5. 取 $H_0=1,H_1=W_{t_1}$ 写出 variance；
6. 若把 $H_1$ 改成 $\Delta_1W$，指出哪一步失效；
7. 说明确定性 partition 与 stopping-time partition 的理论边界。

### DYN-ITO-A03

判断并修正下列命题：

1. adapted 就自动 predictable；
2. 任何 $\int H\,dW$ 都是 Gaussian；
3. Itô integral 是逐路径 Riemann–Stieltjes integral；
4. 左端点与中点在 mesh 消失时必然相同；
5. Itô isometry 给出 almost-sure equality；
6. strong solution 就是数值强收敛；
7. weak solution 表示近似误差较大；
8. 同一 seed 自动保证跨分辨率是同一 Brownian path；
9. $dW_t^2=dt$ 是每个时刻的普通代数恒等式；
10. endpoint distribution 正确就证明 SDE solver 正确。

每条至少给出一个公式、反例或正确条件。

## B. Itô integral 与 Itô formula

### DYN-ITO-B01

设 $f,g\in L^2([0,T])$ 为 deterministic functions，定义

$$
I_f=\int_0^Tf(t)\,dW_t,
\qquad
I_g=\int_0^Tg(t)\,dW_t.
$$

1. 证明 $(I_f,I_g)$ 联合 Gaussian；
2. 求均值、variance 与 covariance；
3. 何时 $I_f,I_g$ 独立？
4. 取 $f(t)=1$、$g(t)=t$ 算出完整 covariance matrix；
5. 求 $I_g\mid I_f=b$；
6. 解释若 $g(t)$ 换成随机 adapted $G_t$，哪些结论保留，哪些不保留。

### DYN-ITO-B02

沿 deterministic partitions 研究

$$
L_\Pi=\sum_iW_{t_i}\Delta_iW,
\qquad
S_\Pi=\sum_i\frac{W_{t_i}+W_{t_{i+1}}}{2}\Delta_iW.
$$

1. 用 telescope 分别求两者极限；
2. 说明 convergence mode；
3. 求 $\int_0^TW_t\,dW_t$ 的均值和 variance；
4. 用 Itô isometry 交叉验证 variance；
5. 求 $\int_0^T W_t\circ dW_t$；
6. 推导二者 correction；
7. 对 $T=2$ 写出全部数值常数；
8. 解释为何这道题已足以否定 ordinary chain rule。

### DYN-ITO-B03

设

$$
dX_t=a_t\,dt+b_t\,dW_t.
$$

1. 对 $f(t,x)=x^3$ 写出 differential；
2. 对 $f(t,x)=e^{\lambda x}$ 写出 differential；
3. 对 $f(t,x)=t x^2$ 写出 differential；
4. 若 $dY_t=c_tdt+d_tdW_t$，推导 $d(X_tY_t)$；
5. 求 $d[X,Y]_t$；
6. 令 $X=W$，证明 $W_t^2-t$ 与 $W_t^3-3tW_t$ 是 local martingales；
7. 给出使它们成为 true martingales 的可积性理由。

## C. SDE 解、经典模型与多维公式

### DYN-ITO-C01

对 Itô GBM

$$
dX_t=\mu X_tdt+\sigma X_tdW_t,
\qquad X_0=x_0>0,
$$

1. 用 $f(x)=\log x$ 求 exact solution；
2. 求 $\mathbb E[X_t]$、$\mathbb E[X_t^2]$ 与 variance；
3. 求 $\operatorname{Cov}(X_s,X_t)$，$s\le t$；
4. 证明 exact path 保持正值；
5. 写出 Euler–Maruyama 并计算单步变负的概率；
6. 把 Itô 方程转成等价 Stratonovich 方程；
7. 比较 $dX=\sigma X\,dW$ 与 $dX=\sigma X\circ dW$ 的均值。

### DYN-ITO-C02

对 Ornstein–Uhlenbeck SDE

$$
dX_t=\kappa(m-X_t)dt+\sigma dW_t,
\qquad \kappa>0,
$$

1. 用 integrating factor 求解；
2. 给定 deterministic $X_0=x_0$，求 conditional mean/variance；
3. 写出 transition law $X_t\mid X_s=x$；
4. 求 stationary distribution；
5. 若 $X_0$ 已服从 stationary law，求 covariance kernel；
6. 离散化 EM 并求其 stationary variance；
7. 比较 exact 与 EM stationary variance，给出稳定条件；
8. 说明为何这是检验 stochastic stiffness 与长期偏差的基本模型。

### DYN-ITO-C03

令 $X_t\in\mathbb R^d$ 满足

$$
dX_t=AX_tdt+B\,dW_t,
$$

其中 $W_t\in\mathbb R^m$，$A\in\mathbb R^{d\times d}$，
$B\in\mathbb R^{d\times m}$。

1. 对 $f(x)=c^\top x$ 用 Itô formula；
2. 对 $f(x)=\|x\|^2$ 用 Itô formula；
3. 推导 mean ODE；
4. 推导 second-moment/covariance ODE；
5. 写出 generator；
6. 当 $A$ Hurwitz 时写出 stationary covariance 的 Lyapunov equation；
7. 解释 $B$ 与 $BQ$（$Q$ 正交）为何给同一 generator；
8. 解释同一 $BB^\top$ 是否足以保证同一 strong coupling。

## D. 适定性与数值分析

### DYN-ITO-D01

逐一审计下列 scalar Itô SDE 是否直接满足 global Lipschitz 与 linear-growth theorem：

$$
\text{(a)}\quad dX_t=-\tanh(X_t)dt+(1+\tfrac12\sin X_t)dW_t,
$$

$$
\text{(b)}\quad dX_t=X_t^3dt+dW_t,
$$

$$
\text{(c)}\quad dX_t=-X_t^3dt+dW_t,
$$

$$
\text{(d)}\quad dX_t=\operatorname{ReLU}(X_t)dt+|X_t|^{1/2}dW_t.
$$

1. 分别检查 local/global Lipschitz；
2. 检查 linear growth；
3. 说明“标准定理不能直接用”与“不存在唯一解”的逻辑区别；
4. 对 (b)(c) 解释同为 cubic growth，dissipativity 如何改变 nonexplosion 研究；
5. 对 neural drift 给出至少三种可验证的 global-control 设计。

### DYN-ITO-D02

对 GBM 的 Euler–Maruyama：

$$
X_{n+1}=X_n(1+\mu h+\sigma\Delta W_n)
$$

完成以下任务：

1. 写 exact terminal 与同路径 strong error；
2. 推导 $\mathbb E[X_N]=X_0(1+\mu h)^N$；
3. 推导 weak mean bias 的一阶渐近展开；
4. 解释为何一般 strong order 是 $1/2$；
5. 写出 finest-to-coarse nested increment 构造；
6. 说明独立重抽每个网格会测到什么；
7. 设计至少三个 test functions 的 weak audit；
8. 区分 Monte Carlo standard error 与 time-discretization bias；
9. 解释 finite-h positivity failure 为何不与 weak convergence 矛盾。

### DYN-ITO-D03

对 scalar SDE

$$
dX_t=a(X_t)dt+b(X_t)dW_t
$$

1. 从 stochastic Taylor 的二阶项写出 Milstein；
2. 解释 $(\Delta W)^2-h$ 为什么必须中心化；
3. 对 GBM 写出具体更新；
4. 对 additive noise 说明为何与 EM 重合；
5. 比较 EM/Milstein 的典型 strong/weak order；
6. 对二维两噪声系统说明 iterated integral 与 Lévy area 从何出现；
7. 给出 commutative-noise 简化的概念条件；
8. 设计一个不能只用 endpoint RMSE 的 solver benchmark。

## E. AI、梯度与研究审计

### DYN-ITO-E01

令 neural SDE 的 EM step 为

$$
X_{n+1}
=X_n+f_\theta(t_n,X_n)h
+g_\theta(t_n,X_n)\Delta W_n,
$$

loss 为

$$
J_h(\theta)=\mathbb E[\ell(X_N)].
$$

1. 推导 forward sensitivity $S_n=\partial_\theta X_n$；
2. 写出 $\partial_\theta J_h$；
3. 说明 reverse-mode AD 与 forward sensitivity 分别适合什么形状；
4. 设计 centered finite-difference 验收并说明 common random numbers；
5. 解释该验收为何只证明 discrete gradient；
6. 设计 $h\to0$ continuous-gradient gap；
7. 若 adaptive solver 重建 Brownian noise，列出必须保持的三条一致性；
8. 比较 backprop-through-solver 与 stochastic adjoint 的内存、假设和误差对象。

### DYN-ITO-E02

有人只给出 fixed-time noising formula

$$
X_t=\alpha(t)X_0+\sigma(t)\varepsilon,
\qquad
\varepsilon\sim\mathcal N(0,I),
$$

并声称已定义 forward diffusion SDE。

1. 解释该公式实际定义了什么；
2. 构造 shared-$\varepsilon$ 与 independent-time 两种 coupling；
3. 说明两者可有相同 marginals 但不同 increments；
4. 列出恢复 Markov diffusion 至少还需哪些数据；
5. 若给出 $dX=fdt+g\,dW$，本章能审计哪些合同；
6. 哪些问题必须留给 Fokker–Planck 与 reverse-time 章节；
7. 设计训练/采样报告，分离 score/model/solver/Monte-Carlo error；
8. 解释 probability-flow ODE 与 reverse SDE 即使共享 marginals 也不是同一 path law。

### DYN-ITO-E03

设计一个可复现的 neural SDE 路径生成研究方案。模型应同时包含 multiplicative noise、adaptive solver 与 threshold-hitting metric。

报告必须包含：

1. mathematical SDE card；
2. Itô/Stratonovich 选择及 conversion；
3. existence/nonexplosion 证据；
4. Brownian tree 与 batch/device stream policy；
5. strong、weak、path-event 三类 solver audit；
6. bridge correction 或事件检测；
7. discrete-gradient FD 与 continuous-gap 两道门；
8. 至少一个 exact/linear SDE baseline；
9. ablation：solver、tolerance、noise dimension、drift/diffusion regularization；
10. 失败停止条件；
11. 可证伪的主张与不允许越级的主张；
12. 与 DYN-11/12 的接口。

最后给出一页 research acceptance checklist。
