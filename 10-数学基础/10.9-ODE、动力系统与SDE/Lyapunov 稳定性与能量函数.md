---
type: concept
status: draft
area: [math/ode, math/dynamical-systems, ai/optimization, ai/control]
aliases: [Lyapunov 函数, 李雅普诺夫函数, Lyapunov direct method, energy certificate, LaSalle invariance principle]
prerequisites: ["[[相图、平衡点与局部稳定性]]", "[[全微分与 Fréchet 导数]]", "[[二次型与正定矩阵]]", "[[Kronecker 积、向量化与矩阵方程]]"]
related: ["[[ODE、动力系统与 SDE MOC]]", "[[一阶最优性条件与梯度下降]]", "[[光滑性、强凸性与条件数]]", "[[非凸优化、鞍点与深度网络损失地形]]", "[[Euler、Runge-Kutta 与离散化误差]]", "[[实验 - Lyapunov 度量、LaSalle 与离散能量边界]]"]
sources: ["Teschl-ODE-Dynamical-Systems", "MIT-Underactuated-Lyapunov", "Chang-et-al-2019-Neural-Lyapunov-Control", "Yang-et-al-2024-Lyapunov-Stable-Neural-Control", "Su-6261-Optimization-Dynamics-Global", "Su-6316-Energy-GAN"]
created: 2026-08-19
updated: 2026-08-23
---

# Lyapunov 稳定性与能量函数

> [!abstract] 本章主问题
> Lyapunov 方法不求出每条轨道，而是寻找一个标量“高度” $V(x)$：它在目标平衡点最低，并沿所有允许轨道不增加。正定 $V$ 与 $\dot V\le0$ 给出Lyapunov stability；严格 $\dot V<0$ 或LaSalle零导数集只含目标平衡点时给出asymptotic stability；若 $V$ 与 $\|x-x_*\|^2$ 双边可比且 $\dot V$ 有统一quadratic decay，则得到exponential stability。全局结论还必须控制sublevel set的有界性、forward completeness与其他invariant sets。

> [!important] 与相邻章节的分工
> [[相图、平衡点与局部稳定性]]已经定义四级稳定并用Jacobian判断hyperbolic equilibrium；本章研究怎样构造和验证nonlinear scalar certificate，尤其处理linearization未决或需要basin/robustness信息的情形。[[Euler、Runge-Kutta 与离散化误差]]将系统研究离散化；本章只证明continuous energy下降不自动成为discrete energy下降。

## 学习目标

完成本章后，你应当能够：

1. 区分physical energy、optimization objective、Lyapunov function、barrier function与energy-based model中的“energy”；
2. 定义positive definite、positive semidefinite、proper/coercive与radially unbounded scalar function；
3. 计算Lie derivative $L_fV=\nabla V^\top f$；
4. 从sublevel-set geometry证明Lyapunov direct method；
5. 精确区分 $\dot V\le0$、$\dot V<0$、$\dot V\le-\alpha V$ 与quadratic state bound能推出什么；
6. 用class-$\mathcal K$ bounds组织一般nonlinear stability estimate；
7. 证明Lyapunov sublevel set的forward invariance；
8. 把有界sublevel set变成region-of-attraction inner certificate；
9. 陈述LaSalle invariance principle并找出 $\{\dot V=0\}$ 中的largest invariant subset；
10. 用damped oscillator解释semidefinite energy derivative为何仍可推出attraction；
11. 说明pure rotation为何让同一energy只证明stable而非attractive；
12. 推导continuous algebraic Lyapunov equation的积分解；
13. 证明Hurwitz matrix与positive-definite quadratic Lyapunov certificate等价；
14. 从 $P,Q$ 的eigenvalue bounds读出state exponential rate与overshoot；
15. 解释Euclidean norm增长与tailored Lyapunov metric下降可以同时发生；
16. 为gradient flow、preconditioned flow与momentum flow选择候选能量；
17. 用PL/strong convexity把objective descent升级为rate；
18. 审计learned/neural Lyapunov function的sampling、verification与domain边界；
19. 区分continuous derivative certificate与discrete one-step difference certificate；
20. 写出一份local/regional/global、deterministic/robust/stochastic分层的AI稳定声明。

> [!question] 初学者读完必须能回答
> 1. Physical energy、objective、Lyapunov function 与 barrier function 有何区别？
> 2. 正定、proper/coercive 与 radially unbounded 分别控制什么？
> 3. 为什么 $V>0,\dot V\le0$ 先给 stability，而不自动给 attraction？
> 4. Strict decay、$\dot V\le-\alpha V$ 与 quadratic bounds 分别升级什么结论？
> 5. LaSalle 为什么必须寻找 $\{\dot V=0\}$ 中最大不变子集？
> 6. Lyapunov sublevel set 怎样给 forward invariance 与 basin inner certificate？
> 7. Continuous $L_fV$、discrete $\Delta V$ 与 learned certificate 为什么不能互相替代？

## 阅读前边界

- stable、attractive、asymptotically stable、exponentially stable的量词定义见[[相图、平衡点与局部稳定性]]；
- positive-definite matrix、Rayleigh quotient与eigenvalue bounds见[[二次型与正定矩阵]]和[[Rayleigh 商与极值表征]]；
- Sylvester/Lyapunov equation的vec表示、唯一性与结构算法见[[Kronecker 积、向量化与矩阵方程]]；
- gradient descent、PL、strong convexity与离散rate见[[一阶最优性条件与梯度下降]]、[[光滑性、强凸性与条件数]]；
- 本章以autonomous deterministic ODE为主；SDE下Itô generator会多出二阶项，留给DYN-10。

先用下图回答一个视觉问题：**一个标量函数怎样约束所有未来轨道，导数强度怎样决定稳定结论，而连续、离散和学习证书为何要分开？**

![[00-知识库管理/_assets/figures/dynamics/fig-lyapunov-energy-certificate-v2.svg|880]]

> [!figure] 图 10.9.4｜子水平集不变性、LaSalle 与三类证书
> A 用 nested sublevel sets $\Omega_c=\{x:V(x)\le c\}$ 和向内轨道表示 $V>0,\dot V\le0$ 对未来状态的约束，并连接 bounded sublevel、forward completeness 与 regional certificate；B 按 $\dot V\le0$、严格负与 $\dot V\le-\alpha V$ 排列 stability、asymptotic stability 与 exponential rate，同时把 semidefinite case 接到 LaSalle 的最大不变子集；C 区分 continuous ODE 的 $L_fV$、discrete map 的一步差分与 learned $V_\theta$ 的 domain verification。来源：独立绘制；理论接口参考 Lyapunov direct method、LaSalle invariance 与 continuous/discrete stability theory；生成脚本：[[plot_dynamics_foundations_v2.py]]；确定性证明地图，无随机种子。

**怎样读图。** A 先用 $V$ 的正定性把“离目标多远”编码为高度，再用导数符号证明轨道不能逃向更高子水平集；B 按不等式强度逐级读结论，若只有 semidefinite decay，必须继续分析零导数集合的 invariant dynamics；C 最后确认验证对象，ODE 的 Lie derivative、数值步进器的一步能量差和神经证书在给定 domain 上的全量不等式是三件事。

**适用边界（图没有证明什么）。** 图不提供候选 $V$ 的构造算法，也不证明 sampling-based training 覆盖连续 domain。Properness、compactness、forward completeness 和不变性不是装饰条件；缺失它们时不能把 local/regional 结论夸大为 global。Continuous-time decay 不保证任意离散步长下仍下降，SDE 还要把 $L_f$ 换为含二阶项的 Itô generator。

## 零、为什么一个标量可能控制整个向量系统

考虑

$$
\dot x=f(x),
\qquad x\in D\subseteq\mathbb R^n,
$$

并把equilibrium平移到原点：

$$
f(0)=0.
$$

直接求 $x(t;x_0)$ 往往困难；但若存在 $V:D\to\mathbb R$ 满足：

1. $V(0)=0$，离开原点后 $V(x)>0$；
2. 沿每条trajectory，$V(x(t))$ 不增加；

那么trajectory不能从一个低sublevel set穿到更高sublevel set。一个scalar function由此把无穷多初值、所有未来时间和整个vector field压缩成一个可验证的不等式。

这不是dimension reduction意义上的“恢复完整轨道”：不同states可以有相同 $V$。Lyapunov function只需要证明某种long-time property，而不需要编码phase、orientation或到达路径。

### 0.1 两类方法的逻辑区别

**Lyapunov indirect method**：先linearize，再从Jacobian spectrum判断local stability。

**Lyapunov direct method**：直接在nonlinear system上寻找 $V$ 并验证sign conditions，不必显式求解，也不要求Jacobian hyperbolic。

“Direct”不是说候选函数容易找到；它只表示证明不经过完整trajectory solution或linearization equivalence。

## 一、先把五种“能量”分开

### 1.1 Physical energy

Mechanical system中的kinetic加potential energy由物理结构给出。Conservative system可能满足 $\dot E=0$；damping加入后常有 $\dot E\le0$。

Physical energy可以成为Lyapunov function，但不是所有physical energy都在目标点positive definite，也不是所有stable system都有自然机械能。

### 1.2 Lyapunov function

Lyapunov function是**certificate**：只要满足规定的positivity、decay、domain和compactness条件即可。它不必是守恒量，不必有物理单位，也通常不唯一。

### 1.3 Optimization objective

对gradient flow，objective gap常可作为Lyapunov candidate；对momentum或game dynamics，单独loss未必单调。Objective是问题想优化的量，Lyapunov function是证明dynamics性质的量，二者可能相同，也可能完全不同。

### 1.4 Barrier function

Barrier certificate主要证明trajectory不会进入unsafe set；Lyapunov certificate主要证明靠近或收敛到target。二者都使用沿流不等式，但集合几何与结论不同。本章不展开完整safety/control-barrier theory。

### 1.5 Energy-based model中的energy

生成模型常用

$$
p_\theta(x)\propto e^{-E_\theta(x)}
$$

定义unnormalized density。这里 $E_\theta$ 是sample ranking/log-density potential；它不自动满足：

- 在某个dynamical equilibrium处positive definite；
- 沿联合GAN/EBM training dynamics单调下降；
- 对parameter trajectory给stability certificate。

因此科学空间的“能量视角”适合建立生成模型直觉，但“energy”一词不能替代Lyapunov条件。

## 二、函数的四种几何性质

### 2.1 Positive definite

相对原点，$V$ positive definite若

$$
V(0)=0,
\qquad
V(x)>0\quad(x\ne0).
$$

在local theorem中，只需在某个neighborhood内成立。

### 2.2 Positive semidefinite

若

$$
V(0)=0,
\qquad
V(x)\ge0,
$$

则称positive semidefinite。它可能在非零点取零，因此仅凭它通常不能把“低energy”变成“靠近原点”。

例：

$$
V(x,y)=x^2
$$

在整条 $y$-axis上都为零，不是相对原点positive definite。

### 2.3 Radially unbounded / coercive

在 $\mathbb R^n$ 上，若

$$
\|x\|\to\infty
\Longrightarrow
V(x)\to\infty,
$$

则称radially unbounded或coercive。对continuous $V$，这保证每个finite sublevel set

$$
\Omega_c=\{x:V(x)\le c\}
$$

有界；再结合closedness，得到compactness。

### 2.4 Properness

更一般地，map $V:D\to\mathbb R$ 称proper，若compact set的preimage为compact。Euclidean全空间上，continuous radially unbounded function通常给properness；在manifold、open domain或带boundary的空间中，应直接检查sublevel compactness，而不是机械套“径向无界”。

> [!warning] Positive definite不等于proper
> $V$ 可以只在原点取零，却在某条通往无穷的路径上保持有界甚至趋近零。Local stability只需要small sublevel geometry；global attraction必须额外排除“沿低能山谷逃向无穷”。

## 三、沿流导数：Lie derivative

若 $V\in C^1(D)$，沿solution $x(t)$ 用chain rule：

$$
\frac d{dt}V(x(t))
=\nabla V(x(t))^\top\dot x(t)
=\nabla V(x(t))^\top f(x(t)).
$$

定义

$$
L_fV(x)
:=\nabla V(x)^\top f(x).
$$

常简写为 $\dot V(x)$，但它不是“把 $V$ 对某个自由time变量求偏导”；它是directional derivative沿vector field的值。

### 3.1 Sign dictionary

| 条件 | 沿trajectory的含义 | 单独可支持的结论 |
|---|---|---|
| $L_fV=0$ | $V$ conserved | 可能stable，也可能没有稳定信息 |
| $L_fV\le0$ | $V$ nonincreasing | 配合positive definite给stability |
| $L_fV<0$ for $x\ne0$ | 严格耗散 | 配合local条件给asymptotic stability |
| $L_fV\le-\alpha V$ | $V(t)\le e^{-\alpha t}V(0)$ | 是energy exponential decay；state rate还需bounds |
| $L_fV\le-c\|x\|^2$ | state-weighted耗散 | 配合quadratic $V$ bounds给state exponential stability |

### 3.2 Sign只在声明domain内有效

若只验证

$$
L_fV(x)<0
$$

在 $\|x\|<r$，就只能作local/regional声明。数值网格、training samples或finite dataset上sign正确，不等于整个continuous region上sign正确。

## 四、Lyapunov direct method：稳定性定理

### 4.1 Local stability theorem

设 $f$ locally Lipschitz，$f(0)=0$。若存在含原点的open neighborhood $D$ 与 $V\in C^1(D)$，使

$$
V(0)=0,
\qquad
V(x)>0\quad(x\in D\setminus\{0\}),
$$

以及

$$
L_fV(x)\le0
\quad(x\in D),
$$

则原点Lyapunov stable。

若进一步

$$
L_fV(x)<0
\quad(x\in D\setminus\{0\}),
$$

则原点locally asymptotically stable。

### 4.2 Stability部分的几何证明

给定足够小的 $\varepsilon>0$，使closed ball

$$
\overline B_\varepsilon\subset D.
$$

由于 $V$ continuous且在sphere

$$
S_\varepsilon=\{x:\|x\|=\varepsilon\}
$$

上strictly positive，而 $S_\varepsilon$ compact，所以minimum存在：

$$
m_\varepsilon
=\min_{\|x\|=\varepsilon}V(x)>0.
$$

由 $V(0)=0$ 与continuity，可选 $\delta\in(0,\varepsilon)$，使

$$
\|x_0\|<\delta
\Longrightarrow
V(x_0)<m_\varepsilon.
$$

因为 $L_fV\le0$，

$$
V(x(t))\le V(x_0)<m_\varepsilon.
$$

若trajectory第一次到达 $S_\varepsilon$，则该时刻 $V\ge m_\varepsilon$，矛盾。因此它始终留在 $B_\varepsilon$，这正好恢复Lyapunov stability的 $\varepsilon$–$\delta$ 量词。

### 4.3 Strict derivative如何给attraction

直觉上，若 $L_fV<0$ away from origin，trajectory不能永远停留在一个与原点隔开的compact annulus中。严格论证选择

$$
A_{r,\varepsilon}
=\{x:r\le\|x\|\le\varepsilon\}
$$

并利用compactness得到

$$
\max_{x\in A_{r,\varepsilon}}L_fV(x)<0.
$$

若trajectory永远不进入 $B_r$，$V$ 就会以统一负速率下降并最终变成负数，与 $V\ge0$ 矛盾。因此它进入任意small $B_r$；结合stability可推出 $x(t)\to0$。

> [!note] Compactness不是装饰
> 从“每一点strictly negative”升级到“整个annulus上uniformly bounded away from zero”依赖continuity与compactness。删掉它，pointwise sign未必给足够的uniform decay。

## 五、一般comparison bounds与指数稳定

### 5.1 Class-$\mathcal K$ functions

Continuous function $\alpha:[0,a)\to[0,\infty)$ 称class $\mathcal K$，若

$$
\alpha(0)=0
$$

且strictly increasing。若domain为 $[0,\infty)$ 且 $\alpha(r)\to\infty$，称class $\mathcal K_\infty$。

对positive-definite $V$，常建立

$$
\alpha_1(\|x\|)
\le V(x)
\le \alpha_2(\|x\|).
$$

这些bounds把scalar energy重新翻译为state distance。

### 5.2 General asymptotic certificate

若在neighborhood中存在class-$\mathcal K$ functions $\alpha_1,\alpha_2,\alpha_3$，使

$$
\alpha_1(\|x\|)
\le V(x)
\le\alpha_2(\|x\|),
$$

$$
L_fV(x)
\le-\alpha_3(\|x\|),
$$

则得到local asymptotic stability。若bounds global且 $\alpha_1\in\mathcal K_\infty$ 并保证forward completeness，则可升级global。

### 5.3 Quadratic bounds给state exponential rate

若存在positive constants $c_1,c_2,c_3$，使

$$
c_1\|x\|^2
\le V(x)
\le c_2\|x\|^2,
$$

以及

$$
L_fV(x)\le-c_3\|x\|^2,
$$

则

$$
L_fV(x)
\le-\frac{c_3}{c_2}V(x).
$$

积分得到

$$
V(x(t))
\le e^{-(c_3/c_2)t}V(x_0).
$$

再用两侧quadratic bounds：

$$
c_1\|x(t)\|^2
\le e^{-(c_3/c_2)t}c_2\|x_0\|^2,
$$

所以

$$
\boxed{
\|x(t)\|
\le
\sqrt{\frac{c_2}{c_1}}
e^{-\frac{c_3}{2c_2}t}
\|x_0\|
}.
$$

### 5.4 为什么 $L_fV\le-\alpha V$ 还不够单独宣布state exponential

它直接给

$$
V(t)\le e^{-\alpha t}V(0).
$$

但若 $V$ 与state distance的关系不是quadratic，state rate可能改变。例如 $V(x)=|x|^4$ 的exponential decay只给 $|x|$ 以四次根后的rate。要匹配标准state exponential stability定义，必须明确comparison bounds。

## 六、Sublevel sets与forward invariance

### 6.1 基本命题

令

$$
\Omega_c=\{x\in D:V(x)\le c\}.
$$

若 $L_fV\le0$ 在 $\Omega_c$ 上成立，solutions唯一并在该集合中可延拓，则 $\Omega_c$ forward invariant：

$$
x_0\in\Omega_c
\Longrightarrow
x(t;x_0)\in\Omega_c,
\quad t\ge0.
$$

因为沿停留在集合内的轨道 $V$ nonincreasing，它不可能第一次穿过 $V=c$ 进入 $V>c$。

### 6.2 Invariance怎样帮助global existence

若 $\Omega_c$ compact且包含初值，trajectory被困在compact subset中。对locally Lipschitz vector field，continuation theorem通常允许solution不断延拓，排除finite-time escape。

所以完整逻辑是：

$$
\text{decay inequality}
\Rightarrow
\text{sublevel invariance}
\Rightarrow
\text{bounded trajectory}
\Rightarrow
\text{continuation}
\Rightarrow
\text{long-time conclusion}.
$$

只写第一箭头而不检查后续条件，是很多global proof的断点。

## 七、用sublevel set估计region of attraction

### 7.1 Regional certificate

假设在某region $D$ 内：

- $V$ positive definite；
- $\Omega_c\subset D$ compact；
- $L_fV<0$ on $\Omega_c\setminus\{0\}$。

则

$$
\Omega_c\subseteq\mathcal B(0).
$$

也就是说，sublevel set给basin of attraction的**内近似**。

### 7.2 Worked scalar example

考虑

$$
\dot x=-x+x^3.
$$

取

$$
V(x)=\frac12x^2.
$$

则

$$
\dot V=x(-x+x^3)
=-x^2+x^4
=-x^2(1-x^2).
$$

在 $|x|<1$ 严格为负。Sublevel

$$
V(x)<\frac12
$$

正好等于 $|x|<1$，因此得到

$$
(-1,1)\subseteq\mathcal B(0).
$$

结合phase line可知本例估计恰好tight；一般候选函数给出的sublevel只是一种conservative inner approximation。

### 7.3 为什么最大化 $c$ 仍不等于求出真实basin

固定candidate $V$ 时，可以寻找最大 $c$ 使sublevel留在decay region；但真实basin boundary未必是某个 $V$-level set。换candidate、degree或metric会改变可证region。计算得到large certificate也不自动证明optimality。

## 八、LaSalle invariance principle

Strict negativity往往太强。Mechanical damping常只消耗velocity energy，使 $\dot V=0$ 包含一整条position set；但其中多数state不能永远停留。LaSalle正是把“瞬间zero derivative”和“永远留在zero derivative set”分开。

### 8.1 Regional statement

设 $\Omega$ 是compact forward-invariant set，$f$ locally Lipschitz，$V\in C^1$，并且

$$
L_fV(x)\le0
\quad\forall x\in\Omega.
$$

定义

$$
E=\{x\in\Omega:L_fV(x)=0\}.
$$

令 $M$ 是 $E$ 中largest invariant subset。则每条从 $\Omega$ 出发的trajectory都满足

$$
\operatorname{dist}(x(t),M)\to0.
$$

若 $M=\{0\}$，再结合positive-definite $V$给出的stability，就得到原点asymptotically stable。

### 8.2 “Largest invariant subset”怎样找

不能只解代数方程 $L_fV=0$。正确流程：

1. 求zero-derivative set $E$；
2. 把system dynamics限制到 $E$；
3. 检查哪些points的完整forward trajectory始终留在 $E$；
4. 这些trajectory的union才是 $M$。

### 8.3 Damped oscillator

考虑

$$
\dot q=p,
\qquad
\dot p=-q-\gamma p,
\qquad \gamma>0.
$$

取mechanical energy

$$
V(q,p)=\frac12(q^2+p^2).
$$

则

$$
\dot V
=q\dot q+p\dot p
=qp+p(-q-\gamma p)
=-\gamma p^2\le0.
$$

Zero-derivative set是

$$
E=\{(q,p):p=0\}.
$$

但若 $p=0,q\ne0$，

$$
\dot p=-q\ne0,
$$

trajectory立刻离开 $E$。因此 $E$ 中largest invariant subset只有 $(0,0)$。因为 $V$ radially unbounded，所有sublevels compact且invariant；LaSalle给global asymptotic stability。

这个energy derivative是semidefinite，不能直接用strict direct theorem；但系统实际还exponentially stable。要从Lyapunov inequality直接得到exponential rate，可改用带cross term的quadratic $x^TPx$。

### 8.4 Pure rotation反例

对

$$
\dot x=-y,
\qquad
\dot y=x,
$$

同样取

$$
V=\frac12(x^2+y^2).
$$

此时

$$
\dot V=0
$$

在整个plane成立，所以 $E=M=\mathbb R^2$。LaSalle只说trajectory趋近整个plane——这是空信息。Positive-definite conserved $V$仍可证明原点stable，但不能证明attractive。

### 8.5 Convergence to a set不等于convergence to a point

对

$$
\dot x=-x,
\qquad
\dot y=0,
$$

取 $V=(x^2+y^2)/2$，有 $\dot V=-x^2$。Largest invariant zero-derivative set是整条 $x=0$；每条trajectory趋近其中的 $(0,y_0)$，而非指定原点。若AI系统存在symmetry-induced minimum manifold，这种“趋近集合”比“参数趋于唯一点”更符合真实结论。

## 九、LaSalle证明骨架：为什么omega-limit set出现

设trajectory被困在compact $\Omega$。因为 $V(x(t))$ nonincreasing且下有界，存在limit

$$
V(x(t))\to V_\infty.
$$

Compactness保证trajectory存在accumulation points，组成nonempty compact omega-limit set $\omega(x_0)$。Flow continuity与autonomy使 $\omega(x_0)$ invariant。

若某个limit point $z$ 满足 $L_fV(z)<0$，continuity会在其附近给uniform negative bound；trajectory反复靠近该neighborhood就迫使 $V$ 继续下降一个fixed amount，与 $V\to V_\infty$ 矛盾。因此

$$
\omega(x_0)\subseteq E.
$$

由于omega-limit set本身invariant，

$$
\omega(x_0)\subseteq M.
$$

这给出distance-to-$M$ convergence。完整定理的技术细节围绕precompactness、flow invariance和limit-set性质展开。

## 十、线性系统的quadratic Lyapunov theorem

考虑

$$
\dot x=Ax.
$$

取symmetric $P\succ0$，定义

$$
V(x)=x^TPx.
$$

则

$$
\dot V
=x^T(A^TP+PA)x.
$$

### 10.1 Algebraic Lyapunov equation

给定symmetric $Q\succ0$，continuous algebraic Lyapunov equation是

$$
\boxed{
A^TP+PA=-Q
}.
$$

若存在 $P\succ0$ 解，则

$$
\dot V=-x^TQx<0
$$

对 $x\ne0$ 成立，所以原点globally exponentially stable，$A$ 必须Hurwitz。

### 10.2 Hurwitz $A$ 如何构造 $P$

若 $A$ Hurwitz，对任意 $Q\succ0$ 定义

$$
P=
\int_0^\infty e^{A^Tt}Qe^{At}\,dt.
$$

Exponential stability保证integral converges。对任意 $x\ne0$，

$$
x^TPx
=\int_0^\infty
(e^{At}x)^TQ(e^{At}x)\,dt>0,
$$

所以 $P\succ0$。

再计算

$$
A^TP+PA
=\int_0^\infty
\frac d{dt}
\left(e^{A^Tt}Qe^{At}\right)dt.
$$

由于 $e^{At}\to0$，

$$
A^TP+PA
=\left[e^{A^Tt}Qe^{At}\right]_0^\infty
=-Q.
$$

因此得到等价定理：

$$
\boxed{
A\text{ Hurwitz}
\iff
\forall Q\succ0,
\ \exists!P\succ0:
A^TP+PA=-Q
}.
$$

“对任意 $Q$”可弱化为“存在一组 $P,Q\succ0$ 满足等式”来判断Hurwitz；任意 $Q$ 版本说明candidate可系统构造。

### 10.3 Uniqueness从哪里来

若 $P_1,P_2$ 都解同一equation，$H=P_1-P_2$ 满足

$$
A^TH+HA=0.
$$

向量化后的operator spectrum由

$$
\lambda_i(A)+\overline{\lambda_j(A)}
$$

组成。Hurwitz时这些sums不为zero，所以homogeneous equation只有 $H=0$。完整matrix-equation结构与数值算法见[[Kronecker 积、向量化与矩阵方程]]。

### 10.4 从 $P,Q$ 读出rate

Rayleigh bounds给

$$
\lambda_{\min}(P)\|x\|^2
\le V(x)
\le\lambda_{\max}(P)\|x\|^2,
$$

以及

$$
\dot V
=-x^TQx
\le-\lambda_{\min}(Q)\|x\|^2
\le-\frac{\lambda_{\min}(Q)}
{\lambda_{\max}(P)}V.
$$

所以

$$
\boxed{
\|x(t)\|
\le
\sqrt{\kappa_2(P)}
\exp\left(
-\frac{\lambda_{\min}(Q)}
{2\lambda_{\max}(P)}t
\right)
\|x_0\|
}.
$$

这个bound通常conservative；$Q$ 的选择会改变 $P$、metric geometry和bound。

## 十一、为什么Euclidean norm增长不反驳Lyapunov下降

考虑nonnormal stable matrix

$$
A=
\begin{bmatrix}
-1&6\\0&-2
\end{bmatrix}.
$$

Euclidean energy

$$
V_I(x)=\|x\|^2
$$

满足

$$
\dot V_I=x^T(A^T+A)x.
$$

而

$$
A^T+A=
\begin{bmatrix}
-2&6\\6&-4
\end{bmatrix}
$$

有positive eigenvalue，所以存在方向使Euclidean norm瞬间增长。

但取 $Q=I$ 解Lyapunov equation，可得

$$
P=
\begin{bmatrix}
\frac12&1\\[2pt]
1&\frac{13}{4}
\end{bmatrix}\succ0.
$$

于是tailored energy

$$
V_P=x^TPx
$$

严格满足

$$
\dot V_P=-\|x\|^2<0.
$$

所以“state在Euclidean metric中暂态放大”与“在另一个equivalent Lyapunov metric中单调下降”可以同时为真。Lyapunov function没有承诺所有常用norm单调。

## 十二、Quadratic certificate不是唯一，也不是坐标无关的同一矩阵

### 12.1 Nonuniqueness

不同 $Q\succ0$ 产生不同 $P\succ0$。若 $V$ 是Lyapunov function且 $\phi$ strictly increasing、$\phi(0)=0$、$\phi'>0$，则适当条件下

$$
\widetilde V=\phi\circ V
$$

仍是Lyapunov function，因为

$$
L_f\widetilde V=\phi'(V)L_fV.
$$

所以找不到某个candidate只说明candidate失败，不说明system不稳定。

### 12.2 Coordinate change

若 $x=Tz$，

$$
x^TPx=z^T(T^TPT)z.
$$

同一个geometric quadratic form在新coordinates中的matrix变成 $T^TPT$。直接比较raw entries或condition number时必须说明coordinates和norm。

### 12.3 Scaling

若 $V$ 合格，则 $cV$ 对任意 $c>0$ 也合格。未经normalization的“Lyapunov loss数值更小”没有跨candidate比较意义；应比较verified region、decay margin、conditioning与verification cost。

## 十三、Converse Lyapunov theorem告诉我们什么

在适当regularity与stability条件下，若equilibrium asymptotically stable，就存在某种Lyapunov function；若uniformly exponentially stable，通常可获得带quadratic-type bounds与strict decay的smooth certificate。

Converse theorem的意义是：Lyapunov方法不只是偶然的sufficient trick，而在合适function class中能刻画stability。

它不意味着：

- 给定简单polynomial或neural architecture一定表示得出certificate；
- 有限训练或local optimizer能找到它；
- verification在高维中容易；
- 任意稳定概念都共享同一regularity和global assumptions。

一个启发式converse construction是

$$
V(x)=\int_0^\infty \|\varphi_t(x)\|^2dt,
$$

若integral收敛。沿flow可形式化得到

$$
V(\varphi_s(x))
=\int_s^\infty\|\varphi_t(x)\|^2dt,
$$

所以

$$
\frac d{ds}V(\varphi_s(x))
=-\|\varphi_s(x)\|^2.
$$

但实际计算该integral需要知道whole future flow，正说明“存在certificate”与“容易构造certificate”是两回事。

## 十四、Gradient flow：objective何时真是Lyapunov function

考虑

$$
\dot\theta=-\nabla L(\theta),
$$

并令 $\theta_*$ 是target minimizer。自然candidate是

$$
V(\theta)=L(\theta)-L(\theta_*).
$$

沿flow：

$$
\dot V
=\nabla L(\theta)^T\dot\theta
=-\|\nabla L(\theta)\|^2\le0.
$$

### 14.1 仅有objective下降还缺什么

要让 $V$ 相对 $\theta_*$ positive definite，需要

$$
L(\theta)>L(\theta_*)
$$

对region内其他points成立。若minimum不唯一或存在parameter symmetry，$V$ 只相对minimum set positive semidefinite。

要让 $\dot V$ negative definite，需要region内没有其他stationary points。Nonconvex loss中saddles、maxima与flat stationary points都会落入

$$
\{\dot V=0\}=\{\nabla L=0\}.
$$

因此LaSalle最多先给convergence to largest invariant stationary subset；要宣布趋于指定minimum，还需landscape、basin与compactness条件。

### 14.2 PL inequality给objective exponential rate

若在relevant region满足Polyak–Łojasiewicz inequality

$$
\frac12\|\nabla L(\theta)\|^2
\ge\mu\bigl(L(\theta)-L_*\bigr),
$$

则

$$
\dot V
=-\|\nabla L\|^2
\le-2\mu V.
$$

所以

$$
V(t)\le e^{-2\mu t}V(0).
$$

这是objective-gap rate。若还要parameter-distance rate，需要quadratic growth、strong convexity或error bound把 $V$ 与 $\|\theta-\theta_*\|^2$ 联系。

### 14.3 Strong convexity加smoothness

若 $L$ 是 $\mu$-strongly convex且 $L_s$-smooth，

$$
\frac\mu2\|\theta-\theta_*\|^2
\le V(\theta)
\le\frac{L_s}{2}\|\theta-\theta_*\|^2.
$$

结合 $\dot V\le-2\mu V$，可得一种state bound

$$
\|\theta(t)-\theta_*\|
\le
\sqrt{\frac{L_s}{\mu}}
e^{-\mu t}
\|\theta(0)-\theta_*\|.
$$

它不是gradient flow exact rate的唯一或最紧表达，但清楚展示了energy-to-state translation。

### 14.4 Flat minimum与慢收敛

对

$$
L(x)=\frac14x^4,
\qquad
\dot x=-x^3,
$$

取 $V=L$，

$$
\dot V=-x^6.
$$

它strictly negative away fromzero，证明asymptotic stability；但不存在local uniform $\dot V\le-\alpha V$，因为

$$
\frac{-\dot V}{V}=4x^2\to0.
$$

这与实际polynomial state decay一致。

## 十五、Preconditioned、natural与mirror-like continuous flow

考虑state-dependent positive-definite metric

$$
\dot\theta=-G(\theta)^{-1}\nabla L(\theta),
\qquad G(\theta)\succ0.
$$

则

$$
\dot L
=-\nabla L^T G^{-1}\nabla L\le0.
$$

这覆盖continuous natural-gradient或variable-metric直觉。但rate与robustness依赖uniform metric bounds：若

$$
mI\preceq G(\theta)\preceq MI,
$$

则

$$
\frac1M\|\nabla L\|^2
\le
\nabla L^TG^{-1}\nabla L
\le
\frac1m\|\nabla L\|^2.
$$

若 $G$ singular、ill-conditioned、estimated from data或time varying，单调与rate必须重新核验。Discrete natural gradient/mirror descent还涉及step size、Bregman geometry和approximate solves，不能只复制continuous derivative。

## 十六、Momentum与damped second-order flow

考虑

$$
\dot q=v,
\qquad
\dot v=-\nabla U(q)-\gamma v,
\qquad \gamma>0.
$$

自然total energy是

$$
E(q,v)
=U(q)-U(q_*)+\frac12\|v\|^2.
$$

沿flow：

$$
\dot E
=\nabla U(q)^Tv
+v^T(-\nabla U(q)-\gamma v)
=-\gamma\|v\|^2\le0.
$$

### 16.1 LaSalle条件

Zero-derivative set是 $v=0$。要始终留在其中，还需

$$
\dot v=-\nabla U(q)=0.
$$

所以largest invariant subset包含所有stationary pairs

$$
(q,0),
\qquad\nabla U(q)=0.
$$

若某compact invariant sublevel内只有target $q_*$ 一个stationary point，LaSalle给趋于 $(q_*,0)$。Nonconvex $U$ 若含其他critical points，就不能从energy descent宣布唯一minimum convergence。

### 16.2 为什么state必须增广

Momentum dynamics的完整state是 $(q,v)$。只在parameter space画 $q$ trajectory会发生projection crossings，也无法用只依赖 $q$ 的objective解释kinetic energy。科学空间的动力学视角在这里提供了有价值的state-selection直觉；严格结论仍必须在phase space验证。

### 16.3 Discrete momentum不是这条ODE的自动继承者

Heavy-ball、Nesterov与不同splitting schemes对 $(q,v)$ 的更新矩阵不同。Continuous $E$下降不保证任意step下discrete $E_k$下降；离散算法可能需要modified energy或完全不同的potential。

## 十七、博弈、Hamiltonian与dissipation

对bilinear descent–ascent

$$
\dot x=-y,
\qquad
\dot y=x,
$$

quadratic $V=(x^2+y^2)/2$ 是conserved quantity。它只证明bounded/stable center，不证明convergence。

加入damping

$$
\dot x=-y-\gamma x,
\qquad
\dot y=x-\gamma y
$$

后，

$$
\dot V=-\gamma(x^2+y^2)=-2\gamma V,
$$

于是得到global exponential sink。

一般game dynamics可分解为dissipative与rotational components；找到某个player loss下降，并不意味着joint state的common Lyapunov function存在。GAN/EBM的“能量地形”与联合training stability尤其不能混写。

## 十八、Continuous与discrete Lyapunov条件

### 18.1 Continuous condition

对

$$
\dot x=f(x),
$$

检查

$$
L_fV(x)=\nabla V(x)^Tf(x).
$$

### 18.2 Discrete condition

对map

$$
x_{k+1}=F(x_k),
$$

正确对象是finite difference

$$
\Delta V(x)
=V(F(x))-V(x).
$$

Discrete asymptotic certificate要求在目标region内

$$
\Delta V(x)<0
\quad(x\ne0),
$$

而不是只检查continuous directional derivative。

### 18.3 Scalar Euler边界

对stable ODE

$$
\dot x=-x,
\qquad V(x)=\frac12x^2,
$$

continuous derivative为

$$
\dot V=-x^2<0.
$$

Forward Euler给

$$
x_{k+1}=(1-h)x_k.
$$

因此

$$
\Delta V
=\frac12\left((1-h)^2-1\right)x^2
=\frac12h(h-2)x^2.
$$

只有

$$
0<h<2
$$

时同一 $V$ strictly decreases。$h>2$ 时continuous system仍stable，但discrete energy增长。

### 18.4 Linear discrete Lyapunov equation

对

$$
x_{k+1}=A_dx_k,
$$

quadratic certificate满足

$$
A_d^TPA_d-P=-Q,
\qquad P,Q\succ0.
$$

$A_d$ Schur stable当且仅当对任意 $Q\succ0$ 存在唯一 $P\succ0$。它与continuous equation

$$
A^TP+PA=-Q
$$

形式相似但不是同一方程。

## 十九、Time-varying Lyapunov function

对nonautonomous system

$$
\dot x=f(t,x),
$$

允许candidate显含time：

$$
V=V(t,x).
$$

沿trajectory的total derivative为

$$
\dot V
=\partial_tV(t,x)
+\nabla_xV(t,x)^Tf(t,x).
$$

遗漏 $\partial_tV$ 会得到错误sign。要证明uniform stability/rate，comparison bounds还应对time uniform，例如

$$
c_1\|x\|^2\le V(t,x)\le c_2\|x\|^2
$$

中的constants不能随 $t$ 恶化。

在input-conditioned Neural ODE中，若input固定为parameter，可研究family $f_x(z)$；若input随time变化，就应使用nonautonomous或input-to-state语言，而不是把每个瞬间的frozen equilibrium certificate拼成global theorem。

## 二十、Robustness与common Lyapunov function

考虑uncertain family

$$
\dot x=f_\alpha(x),
\qquad \alpha\in\mathcal A.
$$

若存在单一 $V$ 和uniform bounds，使

$$
L_{f_\alpha}V(x)
\le-\alpha_3(\|x\|)
$$

对所有 $\alpha\in\mathcal A$ 成立，则得到common Lyapunov certificate与uniform robustness statement。

逐个parameter都有自己的 $V_\alpha$ 不自动给arbitrarily switching family稳定；switching时certificate本身可能跳变。Common certificate通常更强，也可能conservative。

### 20.1 Additive disturbance与ultimate bound

若

$$
\dot x=f(x)+G(x)u
$$

且只能证明

$$
\dot V
\le-\alpha(\|x\|)+\sigma(\|u\|),
$$

那么nonzero persistent input一般不再让state趋于exact origin；更合理的结论是input-dependent ultimate bound或input-to-state stability。不能把扰动项在推导中直接丢掉。

## 二十一、Stochastic dynamics为什么需要新公式

若

$$
dX_t=b(X_t)dt+\Sigma(X_t)dW_t,
$$

不能把Brownian path当ordinary differentiable trajectory。Itô formula给drift generator

$$
\mathcal LV
=\nabla V^Tb
+\frac12\operatorname{tr}
\left(\Sigma\Sigma^T\nabla^2V\right).
$$

即使deterministic part满足 $\nabla V^Tb<0$，diffusion二阶项也可能抵消耗散。Stochastic stability还要区分almost sure、in probability、mean-square与invariant distribution；完整处理留给DYN-09—11。

## 二十二、怎样寻找Lyapunov candidate

### 22.1 Physical structure

- kinetic + potential energy；
- electrical/storage energy；
- entropy或free energy；
- conserved quantity加dissipation correction。

### 22.2 Optimization structure

- objective gap $L-L_*$；
- distance to solution set；
- objective加velocity/cross terms的potential；
- primal-dual gap或weighted residual。

### 22.3 Linearization seed

若 $J_*$ Hurwitz，选 $Q\succ0$ 解

$$
J_*^TP+PJ_*=-Q
$$

并用 $V(u)=u^TPu$ 作为nonlinear local candidate。Higher-order remainder足够小时，strict decay仍成立；扩大sublevel可估计regional basin。

### 22.4 Algebraic search

对polynomial dynamics与polynomial candidate，可把positive/negative conditions松弛为sum-of-squares constraints，再用semidefinite programming搜索。SOS positivity是充分条件，不是所有nonnegative polynomial都SOS；degree、multiplier与numerical tolerance都会影响certificate。

### 22.5 Neural candidate

可用neural network表示 $V_\phi(x)$ 或controller/certificate pair。常见结构确保

$$
V_\phi(0)=0,
\qquad V_\phi(x)\ge\varepsilon\|x\|^2,
$$

但derivative condition仍需覆盖continuous region。Chang等人的neural Lyapunov control采用learner–falsifier寻找counterexamples；后续工作使用branch-and-bound或bound propagation做post-hoc verification。

> [!warning] Training loss不是formal certificate
> 在finite samples上让 $V>0$、$L_fV<0$，只说明这些samples通过。若没有Lipschitz cover、interval bound、SMT、MILP、branch-and-bound、SOS或其他全域验证，不能宣称整个region稳定。

## 二十三、Learned dynamics中的四层对象

### Layer 1：模型

声明 $f_\theta$、state space、equilibrium、domain与input convention。

### Layer 2：Candidate

声明 $V_\phi$ architecture、normalization、positive-definite mechanism与smoothness。

### Layer 3：Verification

在连续region上验证：

$$
V_\phi(x)\ge\alpha_1(\|x\|),
\qquad
L_{f_\theta}V_\phi(x)
\le-\alpha_3(\|x\|).
$$

同时记录solver tolerance、bound relaxation、unverified cells与counterexamples。

### Layer 4：Task performance

Prediction accuracy、robustness、control cost、latency与generalization仍需独立empirical evidence。Stability certificate不自动意味着representation useful、classifier accurate或controller optimal。

## 二十四、常见错误与最小反例

### 错误 1：$V\ge0$ 就是Lyapunov function

修复：还需相对target的definiteness、沿流derivative、domain与solution条件。

### 错误 2：$\dot V\le0$ 自动推出asymptotic stability

修复：pure rotation中 $V=r^2/2$ conserved，只能证明stable。使用strict negativity或LaSalle分析largest invariant zero set。

### 错误 3：$\dot V=0$ 的点都会成为limit points

修复：zero-derivative set中多数points可能瞬间离开；LaSalle看largest invariant subset。

### 错误 4：Positive definite + strict decrease自动global

修复：需要global domain、forward completeness和bounded/precompact trajectories；properness是常用充分条件。

### 错误 5：$\dot V\le-\alpha V$ 自动给标准state exponential rate

修复：先得到energy rate，再用quadratic或class-$\mathcal K$ bounds翻译为state distance。

### 错误 6：找不到quadratic $V$，所以nonlinear system unstable

修复：quadratic candidate class可能太窄；nonlinear/higher-degree certificate仍可能存在。

### 错误 7：Euclidean norm暂态增长，所以没有Lyapunov function

修复：nonnormal stable system可在tailored metric中monotone下降。

### 错误 8：Continuous energy下降，所以Euler/optimizer也下降

修复：离散系统检查 $V(F(x))-V(x)$；step size会改变sign。

### 错误 9：Objective下降，所以参数趋于唯一minimum

修复：检查minimum set、其他stationary points、compactness与error bounds。

### 错误 10：Energy-based model的energy就是training Lyapunov function

修复：density potential与parameter dynamics certificate是不同对象。

### 错误 11：Neural Lyapunov penalty很小，所以已证明稳定

修复：average/sample penalty不排除unsampled violation；需要region-wide verification与margin。

### 错误 12：Deterministic certificate直接适用于SDE

修复：Itô generator包含Hessian–diffusion项，稳定概念也要重新声明。

## 二十五、验证清单

对任何Lyapunov stability声明逐项回答：

1. System是autonomous、nonautonomous、discrete还是stochastic？
2. Target是point、set、orbit还是distribution？
3. $f(0)=0$ 是否精确成立？
4. $V$ 的domain与smoothness是什么？
5. $V(0)=0$ 如何保证？
6. Positive definite是analytic proof还是sampled observation？
7. $L_fV$ 或 $\Delta V$ 怎样计算？
8. Sign condition覆盖哪个region？
9. Zero-derivative set与largest invariant subset分别是什么？
10. Sublevel是否closed、bounded、contained in domain？
11. Forward completeness从哪里来？
12. 结论是local、regional还是global？
13. Rate是energy、state、objective gap还是distance to set？
14. Disturbance/parameter/input是否uniform处理？
15. Numerical/learned verification的residual、margin与unresolved cells是什么？

## 二十六、结论强度阶梯

### Level 0：Candidate intuition

“这个量像energy且simulation中下降。”只能提出candidate。

### Level 1：Pointwise sampled check

在finite samples上验证positivity/decay，得到测试证据，不是连续region theorem。

### Level 2：Local analytic certificate

在neighborhood上证明positive definite与nonpositive/negative derivative，给local stability/asymptotic stability。

### Level 3：Regional invariant certificate

证明compact sublevel forward invariant，并分析zero set，得到basin inner approximation。

### Level 4：Global/robust certificate

加入properness/forward completeness或uniform common certificate，得到global或uncertainty-uniform结论。

### Level 5：Verified learned system

对neural model在明确continuous region上完成formal verification，报告margins、solver与counterexample search。

### Level 6：AI system claim

再加入discretization、noise、finite precision、data distribution与task metrics，才可评价实际训练/部署系统。

## 二十七、掌握层级

### Level 1：定义与计算

- 能判断positive definite、semidefinite与proper；
- 能计算 $L_fV$；
- 能分开strict/non-strict derivative。

### Level 2：直接证明

- 能重建sphere minimum与sublevel invariance证明；
- 能用quadratic bounds推出state exponential bound；
- 能声明local/global条件。

### Level 3：Invariant-set reasoning

- 能求 $E=\{\dot V=0\}$；
- 能找largest invariant subset；
- 能用LaSalle区分point convergence与set convergence。

### Level 4：Linear与optimization接口

- 能构造Lyapunov integral并证明matrix equation；
- 能从 $P,Q$ 给rate；
- 能审计gradient flow、PL、momentum energy与nonnormal metric。

### Level 5：AI证书审计

- 能区分sample penalty与formal verification；
- 能区分continuous、discrete与stochastic generator；
- 能设计candidate–falsifier–verification–task evaluation流水线。

## 二十八、自测问题

1. Lyapunov function与physical energy有什么逻辑关系？
2. Positive definite为什么不自动proper？
3. $L_fV$ 为什么是directional derivative？
4. Direct method的sphere minimum $m_\varepsilon$起什么作用？
5. Strict derivative proof为什么用compact annulus？
6. Class-$\mathcal K$ bounds如何把energy翻译为state distance？
7. 为什么state exponential rate中指数有 $1/2$ factor？
8. Sublevel invariance需要在哪个region验证sign？
9. ROA certificate为什么通常只是inner approximation？
10. LaSalle为何不只解 $\dot V=0$？
11. Damped oscillator的zero-derivative set与largest invariant subset分别是什么？
12. Pure rotation为何只有stability？
13. $x'=-x,y'=0$为什么只趋近一条set？
14. Hurwitz matrix如何通过integral构造 $P$？
15. Lyapunov equation uniqueness与Sylvester spectrum有什么关系？
16. Nonnormal transient为何不否定tailored metric下降？
17. Converse theorem不解决哪个计算难题？
18. Gradient flow objective gap何时positive definite？
19. PL给的是哪一种rate？
20. Momentum为什么需要state $(q,v)$？
21. Continuous与discrete Lyapunov inequality分别是什么？
22. Time-varying $V$ 为什么多出 $\partial_tV$？
23. Common certificate为何比pointwise parameter certificates强？
24. SDE为什么多出Hessian term？
25. Neural Lyapunov training为什么必须配falsification/verification？

## 二十九、来源与证据边界

1. Gerald Teschl, [Ordinary Differential Equations and Dynamical Systems](https://www.mat.univie.ac.at/~gerald/ftp/book-ode/)：flow、invariant set、fixed-point stability与Lyapunov direct method的正式教材主线；
2. MIT Underactuated Robotics, [Lyapunov Analysis](https://underactuated.mit.edu/lyapunov.html)：local/global direct method、LaSalle、sublevel ROA、linear Lyapunov equation、common certificate与computational search；
3. Chang, Roohi & Gao, [Neural Lyapunov Control](https://proceedings.neurips.cc/paper_files/paper/2019/hash/2647c1dba23bc0e0f9cdf75339e120d2-Abstract.html), NeurIPS 2019：learner–falsifier框架与neural certificate/control联合学习；
4. Yang et al., [Lyapunov-stable Neural Control for State and Output Feedback](https://proceedings.mlr.press/v235/yang24f.html), ICML 2024：learned controller/certificate的post-hoc branch-and-bound verification与ROA证书；
5. 苏剑林，[从动力学角度看优化算法（三）：一个更整体的视角](https://spaces.ac.cn/archives/6261)：gradient trajectory、ODE与优化动力学的中文问题入口；
6. 苏剑林，[能量视角下的GAN模型（一）：GAN＝“挖坑”＋“跳坑”](https://spaces.ac.cn/archives/6316)：生成模型energy landscape的中文直觉入口，用于与Lyapunov energy严格区分。

> [!info] 证据分工
> Teschl与MIT承担direct method、LaSalle、linear equation和ROA的正式条件；NeurIPS/ICML原论文承担neural certificate学习与formal verification的特定框架；科学空间承担optimization/GAN energy的中文问题入口。本章自行组织energy-to-state bounds、continuous/discrete/stochastic对象分账和AI claim ladder，不把sampled penalty、博客类比或benchmark结果提升为一般稳定定理。

## 三十、配套训练与实验

- 习题：[[习题 - Lyapunov 稳定性与能量函数]]
- 详解：[[解答 - Lyapunov 稳定性与能量函数]]
- 数值复现：[[实验 - Lyapunov 度量、LaSalle 与离散能量边界]]
- 分卷导航：[[ODE、动力系统与 SDE MOC]]
- 前置：[[相图、平衡点与局部稳定性]]、[[Kronecker 积、向量化与矩阵方程]]
- 后继：[[Euler、Runge-Kutta 与离散化误差]]、[[刚性系统、绝对稳定域与隐式方法]]
