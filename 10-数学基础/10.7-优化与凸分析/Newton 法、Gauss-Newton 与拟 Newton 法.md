---
type: concept
status: draft
area: [math/optimization, math/second-order-methods, ai/training]
aliases: [Newton法, Gauss-Newton, 拟Newton法, BFGS, L-BFGS, Newton-CG]
prerequisites: ["[[Hessian、二阶微分与曲率]]", "[[一阶最优性条件与梯度下降]]", "[[光滑性、强凸性与条件数]]", "[[共轭梯度法]]"]
related: ["[[优化与凸分析 MOC]]", "[[自适应优化方法]]", "[[投影、约束与可行方向]]", "[[Lagrange 乘子与 KKT 条件]]", "[[误差传播、条件估计与停止准则]]"]
sources: ["Boyd-Vandenberghe-2004-Convex-Optimization", "Nocedal-Wright-2006-Numerical-Optimization", "Dennis-Schnabel-1996-Numerical-Methods", "Liu-Nocedal-1989-LBFGS", "Stanford-EE364A-Unconstrained", "Stanford-CS205L-Nonlinear-Least-Squares", "Su-10588-Hessian-Adaptive-LR"]
created: 2026-08-19
updated: 2026-08-27
---

# Newton 法、Gauss-Newton 与拟 Newton 法

> [!abstract] 本章主问题
> 二阶法不是“显式求 Hessian 的逆”，而是构造局部二次模型、近似求解线性系统，并用 line search 或 trust region 判断这个局部模型能走多远。Newton 使用 objective 的 Hessian；Gauss–Newton 利用 least-squares/composite 结构丢掉 residual-weighted 二阶项；BFGS/L-BFGS 从相邻梯度差学习曲率。三者的局部速度、正定性、内存、噪声耐受和失败证书不同，不能只凭“比一阶法快”互换。

## 学习目标

完成本章后，你应当能够：

1. 从 Taylor 二次模型和线性化驻点方程两条路线推出 Newton step；
2. 解释 Hessian 正定、负曲率、奇异和病态分别意味着什么；
3. 推导 Newton decrement、预测下降和下降方向条件；
4. 写出局部二次收敛的明确假设与误差递推；
5. 区分 full step、damped Newton、modified Newton 与 trust-region Newton；
6. 把 Newton step 实现为线性求解而非矩阵求逆；
7. 用 HVP、CG、负曲率检测和 forcing term 构造 inexact Newton；
8. 从非线性最小二乘推导 exact Hessian 与 Gauss–Newton matrix；
9. 判断 Gauss–Newton 在 small residual、affine residual 和 rank deficiency 下的行为；
10. 推导 BFGS、inverse-BFGS、SR1 与 L-BFGS 的 secant 结构；
11. 说明 curvature condition $s^Ty>0$ 为什么保护 BFGS 正定性；
12. 区分 exact Hessian、GGN、Fisher、empirical Fisher 与 gradient-square EMA；
13. 比较 factorization、Krylov、preconditioning 和 limited-memory 的成本；
14. 写出可审计的二阶优化实验与停止合同；
15. 对深度网络中的“二阶法”主张保留结构、批次与数值边界。

> [!question] 初学者读完必须能回答
> 1. Newton step 怎样同时从二次 Taylor 模型和线性化 stationarity equation 推出？
> 2. 为什么实现应解 $H_kp=-g_k$ 而不是显式形成 $H_k^{-1}$？
> 3. Hessian 正定、负曲率、奇异和病态分别会怎样影响子问题与下降性？
> 4. 非线性最小二乘 Hessian 怎样分解，Gauss–Newton 具体丢掉了哪一项？
> 5. BFGS/L-BFGS 的 secant pair $(s_k,y_k)$ 在学习什么，$s_k^Ty_k>0$ 又保护什么？
> 6. inner linear residual、predicted reduction、actual reduction 与 trust ratio 为什么必须分别验收？
> 7. exact Hessian、GGN、Fisher、empirical Fisher 与 gradient-square EMA 为什么不能互称“二阶矩阵”？

## 阅读前检查：本章不重复什么

- Hessian、二阶方向导数、HVP、GGN/Fisher 的定义见[[Hessian、二阶微分与曲率]]；
- smooth/strongly-convex 常数和 condition number 见[[光滑性、强凸性与条件数]]；
- CG 的 Krylov 子空间与 SPD 条件见[[共轭梯度法]]；
- 本章新增的是**一步怎样求、怎样全局化、何时加速、用什么 residual 验收**。

> [!note] 课程位置
> OPT-09 已把 $M_t$ 解释为算法选择的 movement metric；本章追问何时它真的来自 objective 的局部二次模型。Newton 使用 exact Hessian，Gauss–Newton 使用 residual Jacobian 结构，BFGS/L-BFGS 用 secant pairs 学习曲率。共同骨架是“选 curvature → 解线性/二次子问题 → 检查模型是否值得接受”，而不是显式求逆。

> [!tip] 建议两遍阅读
> **第一遍**在同一个 affine least-squares quadratic 上验证 Newton 一步到解、Gauss–Newton 等于 exact Hessian、BFGS secant pair 记录 $Hs$。**第二遍**再进入局部二次收敛、line search/trust region、inexact Newton–CG、negative curvature 和 noisy secant updates。每个“二阶”结论都要标出 curvature matrix、inner residual 与 outer acceptance。

## 本章的推导问题链

1. 二阶 Taylor model 与线性化 stationarity equation 为什么产生同一个 $H_kp=-g_k$？
2. $H_k\succ0$、indefinite、singular 与 ill-conditioned 分别怎样改变子问题？
3. 为什么数学上写 $H^{-1}g$，实现上却必须解 linear system？
4. Gauss–Newton 的 $J^TJ$ 丢掉了 exact Hessian 中哪一项；何时该项恰为零？
5. BFGS 的 $s_k,y_k$ 怎样编码 secant equation，$s_k^Ty_k>0$ 保护什么？
6. inner solve 很准为什么仍不能替代 line-search/trust-region acceptance？

## 贯穿算例续：Newton 一步到达的点为什么仍可能不可行

继续使用

$$
f(x)=\frac12x^THx-b^Tx,
\qquad
H=\operatorname{diag}(1,4),
\qquad
b=(1,5/2)^T.
$$

在任意 $x$，

$$
g(x)=Hx-b,
\qquad
\nabla^2f(x)=H.
$$

unconstrained minimizer 是 $u=H^{-1}b=(1,5/8)^T$。后续加上 $C=\{x\ge0,\mathbf1^Tx\le1\}$ 时，$u$ 不可行；这会精确说明“Newton 把无约束一阶方程解对”与“原约束问题解对”不是同一个命题。

### 符号与对象账本

| 符号 | 层级 | 本例/含义 | 验收量 |
|---|---|---|---|
| $m_k(p)$ | local model | $f_k+g_k^Tp+\tfrac12p^TH_kp$ | predicted reduction |
| $H_k$ | exact objective Hessian | 恒为 $H$ | inertia/conditioning |
| $p_k$ | subproblem solution | solve $H_kp=-g_k$ | linear residual |
| $J_k^TJ_k$ | Gauss–Newton matrix | 本例等于 $H$ | residual/Jacobian rank |
| $(s_k,y_k)$ | secant data | $y_k=g_{k+1}-g_k$ | $s_k^Ty_k$ |
| $B_k$ | approximate curvature | BFGS/SR1 构造 | SPD/approximation error |
| $\rho_k$ | trust ratio | actual/predicted reduction | outer acceptance |

### Newton step 的精确闭合

从任意 $x_k$ 解

$$
Hp_k=-g_k=-(Hx_k-b),
$$

得到

$$
p_k=H^{-1}b-x_k=u-x_k,
$$

所以 full step

$$
x_{k+1}=x_k+p_k=u
$$

一次到达 unconstrained optimum。这里“一步”来自 objective 本身就是恒定 Hessian quadratic，不是 Newton 对一般非线性函数的全局承诺。

在 $x_0=0$，

$$
g_0=-b,
\qquad
p_0=u=\begin{pmatrix}1\\5/8\end{pmatrix}.
$$

Newton decrement 为

$$
\lambda_N^2=g_0^TH^{-1}g_0
=b^TH^{-1}b
=\frac{41}{16}.
$$

模型预测下降

$$
\frac12\lambda_N^2=\frac{41}{32}
$$

也恰等于 $f(0)-f(u)$。一般非二次问题中 predicted 与 actual reduction 不会自动相同。

### 把同一函数写成 affine least squares

令

$$
A=\operatorname{diag}(1,2),
\qquad
c=\begin{pmatrix}1\\5/4\end{pmatrix}.
$$

则 $A^TA=H$、$A^Tc=b$，并且

$$
\frac12\|Ax-c\|^2
=\frac12x^THx-b^Tx+\frac12\|c\|^2.
$$

常数不改变 optimizer。residual $r(x)=Ax-c$ 是 affine，二阶导数为零，所以 exact Hessian

$$
\nabla^2\!\left(\frac12\|r(x)\|^2\right)
=J^TJ+\sum_i r_i(x)\nabla^2r_i(x)
=A^TA=H.
$$

本例中 Gauss–Newton 不是近似而是精确；对 nonlinear residual，第二项一般不为零，small residual 或结构条件才可能使忽略合理。

### 一个 secant pair 到底记录什么

quadratic 上任取 displacement $s$，gradient difference 恒为

$$
y=g(x+s)-g(x)=Hs.
$$

例如 $s=(1,1)^T$ 时

$$
y=(1,4)^T,
\qquad
s^Ty=5>0.
$$

BFGS 用 $B_{k+1}s_k=y_k$ 让近似 curvature 在已观察方向上匹配 exact $H$；$s^Ty>0$ 在标准 BFGS 更新中保护 SPD。它没有凭一个 pair 恢复所有未观测方向，mini-batch 改变还会使 $y$ 同时含 sampling noise。

### 核心公式七问：Newton linear solve

对

$$
H_kp_k=-g_k,
$$

逐项回答：

1. **目的：**最小化局部二次模型，或把 stationarity equation 线性化后归零；
2. **对象：**$H_k$ 是 curvature operator，$g_k$ 是当前 residual，$p_k$ 是待求 displacement；
3. **来路：**对 $m_k(p)=f_k+g_k^Tp+\tfrac12p^TH_kp$ 关于 $p$ 求导；
4. **步骤：**通过 factorization/Krylov solve 求 $p$，不显式形成 $H_k^{-1}$；
5. **读法：**寻找一个经 curvature 缩放后恰好抵消当前 gradient 的位移；
6. **检查：**报告 $\|H_kp_k+g_k\|$、descent sign $g_k^Tp_k$、predicted reduction 与实际接受比例；
7. **去路：**OPT-11 把 $x_k+p\in C$ 加入子问题，OPT-12 得到 saddle-point KKT system；large-scale AI 中则由 HVP–CG 近似 solve。

> [!warning] 三层 residual 不能互换
> $\|Hp+g\|$ 小只说明 inner linear system 解得准；若 Hessian indefinite，$p$ 仍可能不是 descent direction；即使 model subproblem 合理，full step 也可能因远离局部可信区而失败。必须分开记录 curvature/model、inner solve 与 line-search/trust acceptance。

> [!success] 第一遍停靠线
> 合上笔记后，能从任意 $x_k$ 推出 Newton full step 一次到 $u=(1,5/8)^T$，并在 $x_0=0$ 算出 $\lambda_N^2=41/16$ 与预测下降 $41/32$；能构造 $A,c$ 使 Gauss–Newton 精确等于 $H$，并用 $s=(1,1)$ 得到 $y=(1,4),s^Ty=5$。还必须指出 $u\notin C$，因此无约束 solve 尚未完成后续问题。

## 零、统一对象：局部模型、子问题、接受规则

在 $x_k$ 处记

$$
g_k=\nabla f(x_k),\qquad H_k=\nabla^2f(x_k).
$$

二阶 Taylor 模型是

$$
m_k(p)=f(x_k)+g_k^Tp+\frac12p^TH_kp.
$$

一个可靠的二阶算法至少有三层：

1. **模型层**：用 $H_k$、Gauss–Newton、BFGS 或其他 $B_k$ 表示 curvature；
2. **求解层**：精确/近似求 $B_kp=-g_k$，或解 trust-region 子问题；
3. **全局化层**：用 line search/trust ratio 决定接受多少步。

先用下图回答一个视觉问题：**二阶法究竟使用哪一个曲率矩阵、怎样求解局部子问题，又靠什么规则决定这一步可以走多远？**

![[00-知识库管理/_assets/figures/optimization/fig-newton-gn-quasinewton-v2.svg|880]]

> [!figure] 图 10.7.10｜局部二次模型、三类曲率对象与三层验收
> A 以 Newton 局部二次模型的 minimizer 定义 step，并把 $H_kp=-g_k$ 画成线性求解而非矩阵求逆；B 对比分目标 Hessian、Gauss–Newton 的 $J^TJ$ 和 BFGS/L-BFGS 的 secant curvature；C 将 model choice、inner solve residual 与 line-search/trust-region acceptance 分成三个验收层。来源：独立绘制；生成脚本：[[plot_metric_constrained_optimization_v2.py]]；确定性结构示意，无随机种子。

**怎样读图。** A 先问局部模型是否 convex、linear solve 是否可接受；B 对 least squares 明确 residual-weighted second-derivative term 是否被保留，并对 BFGS 检查 curvature pair；C 不能用 inner residual 代替 outer acceptance，只有迭代进入 attraction region 且 Hessian regularity 等假设成立时，才开始读取局部超线性或二次速率。

**适用边界（图没有证明什么）。** 一维二次模型不呈现高维负曲率、非正规 Krylov 行为与 preconditioning。Gauss–Newton 仅在 residual/Jacobian 结构合适时近似良好；rank deficiency 仍需 damping 或 trust region。Secant condition 不保证 noisy minibatch 下的稳定曲率。图也不证明二阶法在任意深网、硬件预算或 wall-clock 比一阶法更优。

> [!warning] 永远不要显式计算 $H_k^{-1}$
> 数学式 $p=-H^{-1}g$ 是对象说明；数值实现应解 $Hp=-g$。显式 inverse 通常更贵、更不稳定，也会破坏 sparse/structured solve。

## 一、Newton step 的两条推导

### 1.1 最小化二次模型

若 $H_k\succ0$，则 $m_k$ 严格凸，令其对 $p$ 的 gradient 为零：

$$
\nabla_pm_k(p)=g_k+H_kp=0.
$$

所以

$$
H_kp_k^{\mathrm N}=-g_k,
\qquad
x_{k+1}=x_k+p_k^{\mathrm N}.
$$

这一步在 quadratic objective 上一次到达解：若

$$
f(x)=\frac12x^TAx-b^Tx+c,\qquad A\succ0,
$$

则 $g=Ax-b,H=A$，于是 $x+p=A^{-1}b$，与起点无关（忽略有限精度）。

### 1.2 解线性化的驻点方程

最优性方程是 $F(x)=\nabla f(x)=0$。在 $x_k$ 线性化：

$$
F(x_k+p)\approx F(x_k)+J_F(x_k)p
=g_k+H_kp.
$$

令近似为零仍得到 $H_kp=-g_k$。这条路线说明 Newton 本质上也是 root-finding；但 root-finding 只追求 stationary point，若 Hessian 非正定，它不保证朝局部最小值走。

## 二、下降、预测下降与 Newton decrement

若 $H_k\succ0$，

$$
g_k^Tp_k^{\mathrm N}
=-g_k^TH_k^{-1}g_k<0
$$

（只要 $g_k\ne0$），所以 Newton direction 是 descent direction。

定义 Newton decrement：

$$
\lambda(x_k)^2
=g_k^TH_k^{-1}g_k
=p_k^TH_kp_k.
$$

把 $p_k$ 代入模型：

$$
m_k(p_k)-m_k(0)
=g_k^Tp_k+\frac12p_k^TH_kp_k
=-\frac12\lambda(x_k)^2.
$$

因此 $\lambda^2/2$ 是**二次模型预测的目标下降**。在合适 convex/self-concordant 条件下，它还能成为靠近最优解的证书；在一般非凸问题或 indefinite Hessian 下，不能机械使用。

### 2.1 仿射不变性

对 nonsingular $x=Az$，精确 Newton step 按坐标变换一致；Euclidean gradient norm 则会被 $A$ 改变。这是 Newton 几何的优点。但 damping、有限精度、近似 curvature、preconditioner 和 trust norm 可能重新引入坐标依赖。

## 三、为什么局部会二次收敛

设 $x^*$ 满足 $\nabla f(x^*)=0$。在 $x^*$ 邻域假设：

1. $H(x)$ nonsingular，且 $\|H(x)^{-1}\|\le1/m$；
2. Hessian 是 $M$-Lipschitz：$\|H(x)-H(y)\|\le M\|x-y\|$；
3. 初值已足够接近 $x^*$，并接受 full step。

令 $e_k=x_k-x^*$。由积分形式

$$
g(x_k)-g(x^*)
=\int_0^1H(x^*+te_k)e_k\,dt.
$$

Newton 更新给

$$
e_{k+1}
=e_k-H(x_k)^{-1}g(x_k)
$$

$$
=H(x_k)^{-1}
\int_0^1[H(x_k)-H(x^*+te_k)]e_k\,dt.
$$

取范数并用 Lipschitz 条件：

$$
\|e_{k+1}\|
\le\frac1m\int_0^1M(1-t)\|e_k\|^2dt
=\frac{M}{2m}\|e_k\|^2.
$$

这就是 local quadratic convergence：误差近似平方。但它没有说“任意初值”“任意非凸函数”或“近似线性求解也自动平方收敛”。

> [!important] 先进入 basin，才谈二次速度
> Newton 的经典图景有两个阶段：远处用 damping/line search 获得稳定下降；进入曲率可靠的邻域后接受 $\alpha_k=1$，才出现二次阶段。

## 四、全局化：模型不可靠时如何收住一步

### 4.1 damped Newton 与 Armijo backtracking

先算 descent direction $p_k$，再从 $\alpha=1$ 开始缩小，直到

$$
f(x_k+\alpha p_k)
\le f(x_k)+c_1\alpha g_k^Tp_k,
\qquad 0<c_1<1.
$$

若 Hessian SPD，Newton direction 可配合这一 line search。靠近解时通常 full step 被接受。

### 4.2 modified Hessian

若 $H_k$ indefinite 或 near-singular，可用

$$
B_k=H_k+\tau_kI\succ0
$$

解 $B_kp=-g_k$。$\tau$ 太小不能消除 negative curvature；太大则退化成约 $-(1/\tau)g$ 的小梯度步。修改规则要报告最小 eigenvalue/Cholesky failure、$\tau$ 和 solve residual。

### 4.3 trust region

直接限制模型只在半径内使用：

$$
\min_{\|p\|\le\Delta_k}
g_k^Tp+\frac12p^TH_kp.
$$

用实际与预测下降比

$$
\rho_k=
\frac{f(x_k)-f(x_k+p_k)}{m_k(0)-m_k(p_k)}
$$

决定接受并扩大/缩小 $\Delta_k$：$\rho$ 接近 $1$ 表示模型可信；$\rho\le0$ 表示模型预测方向甚至错了。indefinite Hessian 在 trust region 中不是灾难，negative-curvature direction 反而可帮助离开 saddle。

### 4.4 line search 与 trust region 的区别

- line search：先固定 direction，再选长度；要求 direction 通常先是 descent；
- trust region：同时选择方向和长度；可处理 indefinite model；
- 二者都只是 global convergence mechanism，不改变 local curvature 对象的定义。

## 五、inexact Newton：真正的大规模实现

### 5.1 线性残差

不必精确解 $H_kp=-g_k$。令

$$
r_k=H_kp_k+g_k,
$$

并要求 forcing condition

$$
\|r_k\|\le\eta_k\|g_k\|,
\qquad 0\le\eta_k<1.
$$

代表性局部结论是：

- $\eta_k\le\bar\eta<1$：通常保留 local linear convergence；
- $\eta_k\to0$：可得到 superlinear；
- $\eta_k=O(\|g_k\|)$：在 Hessian Lipschitz 等条件下可恢复 quadratic order。

inner solve 过精而 outer model 尚不可靠会浪费计算；太粗则 direction 与预测下降失真。forcing term 是内外迭代的预算接口。

### 5.2 Newton–CG 与 HVP

若 $H_k\succ0$，CG 只需产品 $H_kv$，无需存矩阵。第 $j$ 次 inner iteration 在 Krylov 空间

$$
\mathcal K_j(H_k,g_k)
=\operatorname{span}\{g_k,H_kg_k,\ldots,H_k^{j-1}g_k\}
$$

近似解。自动微分可算 HVP；preconditioner $M\approx H$ 用来压缩 spectrum。

若检测到 $d^TH_kd\le0$，ordinary CG 的 SPD 理论失效；truncated Newton 可停止并返回当前 step 或 negative-curvature direction，再交给 trust region/line search。不能把 “CG 没收敛” 一概归因于 iteration 不够。

### 5.3 两种 residual 不要混淆

| residual | 含义 | 不能单独证明 |
|---|---|---|
| $\|H_kp_k+g_k\|$ | inner linear system 解得多准 | objective 一定下降 |
| $\|\nabla f(x_k)\|$ | outer stationarity | local/global minimum |
| trust ratio $\rho_k$ | local model 预测质量 | 最终解全局最优 |

## 六、Gauss–Newton：利用 residual 结构

考虑 nonlinear least squares：

$$
f(\theta)=\frac12\|r(\theta)\|_2^2
=\frac12\sum_{i=1}^mr_i(\theta)^2,
$$

其中 $J=\partial r/\partial\theta\in\mathbb R^{m\times d}$。链式法则给

$$
\nabla f=J^Tr,
$$

$$
\nabla^2f
=J^TJ+\sum_{i=1}^mr_i\nabla^2r_i.
$$

Gauss–Newton 丢掉第二项，用

$$
B_{\mathrm{GN}}=J^TJ\succeq0,
$$

并解

$$
J^TJp=-J^Tr.
$$

### 6.1 更可靠的推导：先线性化 residual

$$
r(\theta+p)\approx r+Jp.
$$

于是解线性 least-squares 子问题

$$
\min_p\frac12\|r+Jp\|^2.
$$

其 normal equation 正是 $J^TJp=-J^Tr$。数值上优先直接对 $J$ 用 QR/LSQR，而不是显式形成 $J^TJ$，因为 normal equation 会平方 condition number。

### 6.2 何时近似好

- residual $r_i$ 本身 affine：$\nabla^2r_i=0$，GN 就是 exact Hessian；
- 解附近 residual 很小：被丢弃项由 $r_i$ 加权；
- residual 不小但二阶导较弱：仍可能有效；
- $J$ rank deficient：$J^TJ$ singular，step 不唯一/不稳定，需要 damping、minimum norm 或 rank-revealing solve。

### 6.3 Levenberg–Marquardt

用 damping：

$$
(J^TJ+\lambda I)p=-J^Tr.
$$

等价于 regularized linearized residual problem：

$$
\min_p\frac12\|r+Jp\|^2+\frac\lambda2\|p\|^2.
$$

$\lambda$ 大时接近小 gradient step；小且 $J$ 满秩时接近 GN。它是 step regularization，不自动等于给原 objective 加固定 L2 penalty。

## 七、GGN、Fisher 与 empirical Fisher：名字相似，对象不同

若 loss 是 $\ell(z(\theta),y)$，令 model-output Jacobian 为 $J_z$，output-space Hessian 为 $H_\ell$，generalized Gauss–Newton 为

$$
G=J_z^TH_\ell J_z.
$$

当 $\ell$ 对 $z$ convex 时 $G\succeq0$。它忽略 model output 的二阶导项。对于合适 probabilistic model 与 loss，expected Fisher 可与 expected GGN/Hessian 联系；empirical Fisher 常指 observed sample scores 的 outer products，通常不等于 GGN。Adam 的 EMA$(g^2)$ 又只保留 trajectory-dependent diagonal raw moments。

> [!warning] PSD 不等于“更精确”
> GGN/GN 的 PSD 让 descent solve 更稳定，却有意丢掉 negative curvature；exact Hessian 能表达 saddle 方向，但也要求能正确处理 indefinite system。

## 八、拟 Newton：从梯度差学习曲率

令

$$
s_k=x_{k+1}-x_k,
\qquad
y_k=g_{k+1}-g_k.
$$

由 gradient 的一阶展开，$y_k\approx H_*s_k$。拟 Newton 构造 $B_{k+1}\approx\nabla^2f$ 满足 secant equation：

$$
B_{k+1}s_k=y_k.
$$

若直接近似 inverse $P_{k+1}\approx H^{-1}$，则要求

$$
P_{k+1}y_k=s_k.
$$

一个 secant pair 只约束矩阵沿一个方向；更新式还需要 symmetry、最小改变和正定性等原则。

### 8.1 BFGS Hessian update

$$
B_{k+1}
=B_k-
\frac{B_ks_ks_k^TB_k}{s_k^TB_ks_k}
+\frac{y_ky_k^T}{y_k^Ts_k}.
$$

若 $B_k\succ0$ 且 $y_k^Ts_k>0$，则 $B_{k+1}\succ0$。curvature condition 表示沿实际 displacement 的平均 curvature 为正；strong Wolfe line search 在常见 smooth optimization 条件下帮助保证它。

### 8.2 inverse-BFGS update

令 $\rho_k=1/(y_k^Ts_k)$：

$$
P_{k+1}
=(I-\rho_ks_ky_k^T)P_k(I-\rho_ky_ks_k^T)
+\rho_ks_ks_k^T.
$$

step 为 $p_k=-P_kg_k$。这条式避免每步解 dense system，但完整 $P_k$ 仍需 $O(d^2)$ memory。

### 8.3 SR1

$$
B_{k+1}=B_k+
\frac{(y_k-B_ks_k)(y_k-B_ks_k)^T}
{(y_k-B_ks_k)^Ts_k}.
$$

SR1 不强保 SPD，因而可表达 indefinite curvature；分母太小时必须 skip update。它常更适合 trust-region framework，不宜直接假定 direction 总下降。

## 九、L-BFGS：只保存最近的 secant pairs

完整 BFGS 的 $O(d^2)$ memory 对大模型不可行。L-BFGS 保存最近 $q$ 对 $(s_i,y_i)$，通过 two-loop recursion 计算

$$
p_k=-P_kg_k
$$

而不显式存 $P_k$。memory 约 $O(qd)$，每步递归也是 $O(qd)$，常取 $q\ll d$。

### 9.1 two-loop recursion 的计算合同

1. 从新到旧计算 $\alpha_i=\rho_i s_i^Tq$，令 $q\leftarrow q-\alpha_i y_i$；
2. 用 scalar/diagonal $P_k^{(0)}$ 得 $r=P_k^{(0)}q$；
3. 从旧到新计算 $\beta_i=\rho_i y_i^Tr$，令 $r\leftarrow r+s_i(\alpha_i-\beta_i)$；
4. 返回 $p=-r$。

常用初始尺度

$$
P_k^{(0)}=\gamma_kI,
\qquad
\gamma_k=\frac{s_{k-1}^Ty_{k-1}}{y_{k-1}^Ty_{k-1}}.
$$

### 9.2 L-BFGS 不是“小内存 Newton”

- 它只从 optimizer trajectory 的 secant pairs 学曲率；
- stochastic gradients 会污染 $y_k=g_{k+1}-g_k$；
- line search 需要多次 objective/gradient evaluation，在 huge mini-batch training 中代价高；
- memory 小意味着只记有限方向，不恢复完整 Hessian；
- 在 deterministic smooth problems 上很强，不代表默认适合所有深网训练。

## 十、代表性收敛结论及边界

| 方法 | 代表性局部/全局结论 | 关键条件 |
|---|---|---|
| full Newton | local quadratic | nonsingular Hessian、Hessian Lipschitz、近初值、full step |
| damped Newton | global descent + local quadratic | convex/strong convex level set、backtracking、SPD Hessian 等 |
| inexact Newton | linear/superlinear/quadratic随 $\eta_k$ | forcing term、local regularity |
| Gauss–Newton | small-residual 下快速局部收敛 | Jacobian rank、residual/second derivative 条件、globalization |
| BFGS | 常见条件下 global convergence 到 stationary，local superlinear | smoothness、line search、curvature、deterministic gradients |
| L-BFGS | large-scale smooth optimization 的 limited-memory convergence | convexity/curvature、line search 与 pair quality |

任何一行都不能直接推出 nonconvex deep network 的 global optimum。

## 十一、计算成本与数值选择

| 路线 | memory | 主要计算 | 适合结构 | 主要风险 |
|---|---:|---:|---|---|
| dense Newton + factorization | $O(d^2)$ | factorization 约 $O(d^3)$ | 中小型 dense | indefinite/病态、存储 |
| sparse Newton | sparsity-dependent | sparse factorization | 图/稀疏约束 | fill-in 与 ordering |
| Newton–CG | vectors + HVP | 多次 HVP | 超大维、matrix-free | negative curvature、inner budget |
| Gauss–Newton | $J$ operator | JVP/VJP、QR/LSQR | least squares/composite | rank deficiency、residual 不小 |
| BFGS | $O(d^2)$ | matvec/update | 中等维 deterministic | pair quality |
| L-BFGS | $O(qd)$ | two-loop | 大规模 full-batch/smooth | noisy secant、line-search cost |

conditioning 决定 inner iteration/roundoff amplification；preconditioning 是算法组成，不应藏在实现细节里。

## 十二、AI 接口

### 12.1 神经网络训练

可用 mini-batch HVP、GGN/Fisher blocks、K-FAC/Shampoo-style structured approximations 或 L-BFGS。但需报告：

- curvature batch 是否与 gradient batch 相同；
- damping 与 trust rule；
- HVP/linear-solve iteration 与 residual；
- negative-curvature handling；
- optimizer state memory 与 wall-clock；
- 训练 objective 之外的 validation/generalization。

### 12.2 influence 与隐式微分

影响函数/implicit gradient 常需近似

$$
H^{-1}v.
$$

这也是 linear solve，而非 inverse。若 $H$ singular/indefinite、加入 damping 或 early-stop CG，估计对象已改变；应同时报告 solve residual 与 damping sensitivity。

### 12.3 nonlinear least squares

定位、bundle adjustment、calibration、inverse graphics 和某些 representation matching 天然有 residual 结构。应优先说明 residual 定义、weighting/robust loss、Jacobian rank 与单位，而不是只写“用了 LM”。

## 十三、失败边界与反例

1. $f(x)=x^3$：Newton 解 $f'(x)=0$ 的更新不具全局最小保证；
2. saddle 处 Hessian indefinite：Newton direction 可不是 descent；
3. $H$ singular：step 不唯一或不存在，需 regularization/null-space handling；
4. Gauss–Newton residual 大且 $\nabla^2r_i$ 强：丢弃项不能忽略；
5. normal equations：形成 $J^TJ$ 平方条件数；
6. BFGS 的 $s^Ty\le0$：正定性保护失效；
7. noisy gradient difference：$y_k$ 主要是 batch noise 而非 curvature；
8. inner residual 很小：仍不表示 local model 对真实 objective 可靠；
9. mixed precision：HVP/factorization 的精度与 overflow 可能改变 direction；
10. 训练 loss 更低：不能证明 generalization 或部署目标更好。

## 十四、可复核实验协议

### 14.1 known quadratic

构造可控 eigenvalues/eigenvectors 的 SPD quadratic，比较 GD、CG-Newton、BFGS、L-BFGS。报告 condition number、HVP count、linear residual、objective gap、coordinate rotation 与 precision。

### 14.2 nonlinear least squares

逐步增大 terminal residual 和 Jacobian rank deficiency，比较 exact Newton、GN、LM、QR/normal-equation solve；检查被丢弃 Hessian 项范数与 trust ratio。

### 14.3 nonconvex saddle

用含负 eigenvalue 的 quartic/saddle，比较 modified Newton、trust-region truncated CG 与 SPD GGN；记录负曲率检测和 escape 行为。

### 14.4 deep-model audit

按相同 processed tokens/FLOPs 及 wall-clock 两套预算比较 first/second-order 方法，记录 curvature construction、batch、damping、HVP、inner/outer residual、memory 和多 seed，而不是只画 epoch-loss。

## 十五、掌握标准

### Level 1：识别

- 分清 Newton、GN、GGN、BFGS、L-BFGS；
- 写出 descent、curvature 与 residual 条件。

### Level 2：手算

- 对二维 quadratic 算 Newton/decrement；
- 对小 residual problem 算 GN；
- 用一个 secant pair 算 BFGS update。

### Level 3：证明

- 重建 local quadratic convergence；
- 证明 $y^Ts>0$ 下 BFGS 保 SPD；
- 推导 exact least-squares Hessian 与 GN。

### Level 4：迁移

- 选择 factorization/Krylov/L-BFGS 并写成本；
- 对 curvature approximation 做结构审计；
- 用 inner residual、trust ratio 和 outer stationarity 联合验收。

## 十六、自检问题

1. Newton step 的 model 与 root-finding 推导有何不同含义？
2. 为什么 $H\succ0$ 时 Newton direction 下降？
3. $\lambda^2/2$ 表示真实 gap 还是 model prediction？
4. local quadratic convergence 缺哪个假设最容易失效？
5. modified Hessian 与 trust region 怎样处理负曲率？
6. forcing term 如何连接 inner 和 outer iteration？
7. GN 丢弃了哪一项，何时该项小？
8. 为什么不用 normal equations 直接实现 GN？
9. BFGS 的 secant equation 约束了几个方向？
10. L-BFGS 为什么不等于 exact/diagonal Newton？

## 十七、来源与证据边界

1. Boyd & Vandenberghe, [Stanford EE364A: Unconstrained Minimization](https://web.stanford.edu/class/ee364a/lectures/unconstrained.pdf)：Newton step/decrement、backtracking 与两阶段收敛；
2. Nocedal & Wright, *Numerical Optimization*, 2nd ed., 2006：line-search/trust-region Newton、inexact/truncated Newton、quasi-Newton 与 nonlinear least squares；
3. Dennis & Schnabel, *Numerical Methods for Unconstrained Optimization and Nonlinear Equations*, 1996：Newton 与 secant 方法的数值分析；
4. Liu & Nocedal, [On the Limited Memory BFGS Method for Large Scale Optimization](https://doi.org/10.1007/BF01589116), 1989：L-BFGS 原始算法与 scaling；
5. Stanford CS205L, [Lectures](https://web.stanford.edu/class/cs205l/lectures.html)：BFGS/SR1/L-BFGS、Gauss–Newton 与 Levenberg–Marquardt 的课程入口；
6. [[S-2024-Su-10588-Hessian近似与自适应学习率]]：gradient-square 与 curvature scale 的中文研究入口。

> [!info] 证据分工
> 正式教材、课程与原论文承担算法、收敛和数值条件；科学空间文章只用于审计“平方梯度近似 Hessian”的条件链，不承担 Newton/GN/BFGS 的一般等价性。

## 十八、配套训练

- 习题：[[习题 - Newton 法、Gauss-Newton 与拟 Newton 法]]
- 详解：[[解答 - Newton 法、Gauss-Newton 与拟 Newton 法]]
- 前驱：[[Hessian、二阶微分与曲率]]、[[一阶最优性条件与梯度下降]]
- 后继：[[投影、约束与可行方向]]、[[Lagrange 乘子与 KKT 条件]]
