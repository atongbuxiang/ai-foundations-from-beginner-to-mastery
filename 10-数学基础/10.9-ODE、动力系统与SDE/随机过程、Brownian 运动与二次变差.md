---
type: concept
status: draft
area: [math/probability, math/stochastic-processes, math/sde, ai/generative-modeling]
aliases: [随机过程与布朗运动, Brownian motion, Wiener process, quadratic variation, 二次变差]
prerequisites: ["[[样本空间、事件与概率公理]]", "[[随机变量、分布与分位数]]", "[[联合分布、边缘分布与独立性]]", "[[期望、方差与矩]]", "[[协方差、相关性与条件期望]]", "[[多元高斯分布]]", "[[随机变量的收敛与大数定律]]", "[[中心极限定理与 Delta 方法]]"]
related: ["[[ODE、动力系统与 SDE MOC]]", "[[Itô 引理与随机微分方程]]", "[[Fokker-Planck 方程与概率流 ODE]]", "[[连续性方程与守恒律]]", "[[实验 - Brownian 增量、路径粗糙性与时间耦合审计]]"]
sources: ["MIT-18.175-2016-Brownian-Motion", "MIT-15.070J-2013-Quadratic-Variation", "Durrett-PTE5-Brownian-Donsker", "Morters-Peres-Brownian-Motion", "Oksendal-Stochastic-Differential-Equations", "Song-et-al-2021-Score-SDE", "Su-3750-Random-Walk", "Su-9209-Diffusion-SDE"]
created: 2026-08-19
updated: 2026-08-27
---

# 随机过程、Brownian 运动与二次变差

> [!abstract] 本章主问题
> Brownian motion 不是“每个时刻各抽一个 Gaussian”这么简单，而是一整个具有特定时间耦合的随机连续函数：
> $$
> W_t-W_s\sim\mathcal N(0,t-s),
> \qquad
> 0\le s<t,
> $$
> 且不重叠时间段的增量相互独立。它的增量尺度是
> $$
> \Delta W=O_{\mathbb P}(\sqrt{\Delta t}),
> $$
> 因而普通导数的尺度 $\Delta W/\Delta t=O_{\mathbb P}(\Delta t^{-1/2})$ 爆炸，但平方增量恰好累计成有限时间：
> $$
> \sum_i(W_{t_{i+1}}-W_{t_i})^2
> \longrightarrow T.
> $$
> 这条非零 quadratic variation 是普通微积分失效、Itô 二阶修正项出现以及连续时间扩散噪声必须单独建模的根源。

> [!important] 与相邻章节的分工
> 本章定义随机过程、filtration、Brownian motion、路径正则性、total variation、quadratic/cross variation，并建立白噪声和扩散模型所需的最小接口。[[Itô 引理与随机微分方程]]才正式定义随机积分、Itô formula、SDE 解概念与 Euler–Maruyama；[[Fokker-Planck 方程与概率流 ODE]]才从 SDE 推导 density PDE。本章可以预告 $(dW_t)^2=dt$，但不会把它当作普通代数等式偷用。

先用下图回答一个视觉问题：**为什么 Brownian motion 必须作为整条时间耦合路径来定义，$\sqrt{dt}$ 增量尺度又怎样同时摧毁普通导数并留下有限二次变差？**

![[00-知识库管理/_assets/figures/dynamics/fig-brownian-process-quadratic-variation-v2.svg|880]]

> [!figure] 图 10.9.9｜Brownian 时间耦合、粗糙尺度与 quadratic variation
> A 用两条连续 sample paths 和多个共同时间切片强调 pointwise marginals 不决定 process law，并列出 stationary independent increments 与 $\operatorname{Cov}(W_s,W_t)=\min(s,t)$；B 用随 $\Delta t$ 变小的增量柱形表示 $\Delta W=O_{\mathbb P}(\sqrt{\Delta t})$ 与差商爆炸；C 从 partition、平方增量和到 $[W]_T=T$，并对比 continuous finite-variation path 的零 QV 与 Brownian 无限 total variation。来源：独立绘制；理论接口参考 Brownian motion、path regularity 与 quadratic-variation theory；生成脚本：[[plot_stochastic_dynamics_v2.py]]；定性路径示意，无随机种子。

**怎样读图。** A 先固定一条样本 $\omega$ 看整条 path，再固定 $t$ 看 marginal random variable，二者不可交换；B 用方差 $\operatorname{Var}(\Delta W)=\Delta t$ 读出 typical increment 尺度和 nowhere-differentiable 直觉；C 最后把大量 $O(\Delta t)$ 的平方增量相加，得到 $O(1)$ 时间极限，并把 $(dW)^2=dt$ 解释为分割极限记账而非普通代数。

**适用边界（图没有证明什么）。** 两条曲线不是模拟证据，也不证明 a.s. nowhere differentiability 或 quadratic variation 的完整定理；严谨结论需指定 partition 与收敛模式。相同 marginals 也可能通过许多不同 coupling 形成 process。Fractional Brownian、jump process 与 semimartingale 的 variation 结构不同，不能直接套用 Brownian 规则。

> [!note] 课程位置
> DYN-01—08 的路径由确定性初值和 vector field 唯一决定；概率只出现在“随机抽一个初值”时。本章第一次把随机性放进时间演化本身：同一初值也会因不同 $\omega$ 产生不同连续路径。这里先建立 Brownian 的时间耦合、filtration 与 quadratic variation；DYN-10 才把它作为 SDE 驱动源。若没有本章，后续的 $dW_t$、Itô 二阶项和 reverse diffusion 都只是无法审计的符号。

> [!tip] 建议两遍阅读
> **第一遍**只看 $[0,1]$ 的等距分割：写出独立增量分布，计算平方增量和的均值与方差，并解释为何差商爆炸而 quadratic variation 收敛。**第二遍**再进入 process law、filtration、martingale、Brownian bridge、scaling、Donsker、total variation、cross variation 与 white noise。第一遍要掌握的是“同一条 path 的跨时间 coupling”，不是每个时刻各自的 Gaussian histogram。

## 本章的推导问题链

1. 随机变量、stochastic process、finite-dimensional distributions、sample path 与 path law 分别固定了什么？
2. 为什么只知道 $W_t\sim\mathcal N(0,t)$ 不能推出 Brownian 的独立增量与连续路径？
3. Filtration 怎样表达“到 $t$ 时刻可用的信息”，adaptedness 为什么禁止偷看未来噪声？
4. $\operatorname{Var}(W_{t+h}-W_t)=h$ 怎样给出 $\Delta W=O_{\mathbb P}(\sqrt h)$？
5. 为什么 $\Delta W/h$ 随 $h\downarrow0$ 变得更大，而 $(\Delta W)^2$ 的累积却留下有限极限？
6. 平方增量和以哪种收敛模式趋于时间长度，$(dW)^2=dt$ 应如何解读？
7. 这条二次变差怎样在下一章产生 Itô formula 的 $\frac12b^2f_{xx}$？

## 贯穿算例：单位时间上的 Brownian 网格账本

在 $[0,1]$ 上取等距网格

$$
t_k=\frac{k}{N},
\qquad
\Delta W_k=W_{(k+1)/N}-W_{k/N},
\qquad k=0,\ldots,N-1.
$$

由 Brownian 定义，

$$
\Delta W_k\overset{\mathrm{iid}}{\sim}\mathcal N\!\left(0,\frac1N\right).
$$

### 符号与对象账本

| 对象 | 类型 | 本例中的值/作用 | 不可直接称为 |
|---|---|---|---|
| $W_t$ | random variable at time $t$ | $W_t\sim\mathcal N(0,t)$ | 整条 path law |
| $t\mapsto W_t(\omega)$ | sample path | 固定 $\omega$ 后的连续函数 | ordinary differentiable curve |
| $\mathcal F_t$ | information set | 到 $t$ 为止的事件 | 单个观测向量 |
| $\Delta W_k$ | Brownian increment | 方差 $1/N$ 的独立 Gaussian | 方差固定的每步噪声 |
| $Q_N$ | discrete quadratic variation | $\sum_k(\Delta W_k)^2$ | ordinary total variation |
| $V_N$ | discrete total variation | $\sum_k|\Delta W_k|$ | quadratic variation |
| $\xi_t$ | white-noise notation | $dW_t/dt$ 的 generalized sense | pointwise random function |

### 第一步：增量尺度不是 $dt$，而是 $\sqrt{dt}$

写成

$$
\Delta W_k=\frac1{\sqrt N}Z_k,
\qquad Z_k\overset{\mathrm{iid}}{\sim}\mathcal N(0,1).
$$

因此典型增量大小为 $N^{-1/2}=\sqrt{\Delta t}$。对应差商是

$$
\frac{\Delta W_k}{\Delta t}
=\sqrt N,Z_k,
$$

其方差为 $N$，网格越细反而越不稳定。这是 Brownian path 不应使用普通导数语言的最小尺度证据；完整 nowhere-differentiability 仍需更强的 almost-sure 论证。

### 第二步：平方增量恰好留下有限量

定义

$$
Q_N=\sum_{k=0}^{N-1}(\Delta W_k)^2
=\frac1N\sum_{k=0}^{N-1}Z_k^2.
$$

因为 $\mathbb E[Z_k^2]=1$、$\operatorname{Var}(Z_k^2)=2$，

$$
\boxed{
\mathbb E[Q_N]=1,
\qquad
\operatorname{Var}(Q_N)=\frac2N.
}
$$

于是

$$
\mathbb E[(Q_N-1)^2]=\frac2N\longrightarrow0,
$$

即 $Q_N\to1$ in $L^2$，从而也依概率收敛。对一般区间 $[0,T]$，相同计算给 $[W]_T=T$。

### 第三步：绝对增量和却发散

同一网格上的 total-variation proxy 为

$$
V_N=\sum_{k=0}^{N-1}|\Delta W_k|.
$$

利用 $\mathbb E|Z|=\sqrt{2/\pi}$，

$$
\mathbb E[V_N]
=N\frac1{\sqrt N}\sqrt{\frac2\pi}
=\sqrt{\frac{2N}{\pi}}\longrightarrow\infty.
$$

因此“连续”不等于“有限变差”或“光滑”。Brownian 的一阶绝对增量累积发散，二阶增量累积却有限，这正是 stochastic calculus 使用 quadratic variation 的原因。

### 第四步：时间 coupling 不能由边缘分布替代

若错误地令 $\widetilde W_t=\sqrt t,Z$ 并在所有时刻共享同一个 $Z$，仍有

$$
\widetilde W_t\sim\mathcal N(0,t),
$$

但

$$
\widetilde W_{t+h}-\widetilde W_t
=(\sqrt{t+h}-\sqrt t)Z
=O_{\mathbb P}(h)
$$

对 $t>0$ 过于平滑，quadratic variation 为零。相同 one-time marginals 并没有给出相同 SDE 驱动源。

### 第五步：预告 VP–OU 中真正使用的噪声

第四波后续统一模型会出现

$$
\eta_t=\sqrt2\int_0^t e^{-(t-s)}dW_s.
$$

Itô isometry 将给

$$
\operatorname{Var}(\eta_t)
=2\int_0^t e^{-2(t-s)}ds
=1-e^{-2t}.
$$

这里不能在每个 $t$ 独立重抽 $\eta_t$；一条 SDE path 的所有 $\eta_t$ 由同一 Brownian path 耦合。DYN-10 会正式定义这个随机积分。

## 核心公式七问：Brownian quadratic variation

$$
\boxed{
[W]_T
=\lim_{|\Pi|\to0}\sum_i(W_{t_{i+1}}-W_{t_i})^2
=T.
}
$$

1. **解决什么问题？** 描述连续粗糙路径在平方尺度上留下的累计变化，替代普通导数无法提供的信息。
2. **对象与形状？** 对一维 Brownian 是随机标量极限；多维情形还有 matrix-valued cross variation $[W^i,W^j]_t=\delta_{ij}t$。
3. **从哪里来？** 每个增量平方的期望为 $\Delta t_i$，独立 Gaussian 四阶矩控制总方差随 mesh 消失。
4. **需要什么条件？** 必须声明 partition 类与收敛模式；本算例证明的是确定性等距分割上的 $L^2$ 收敛。
5. **怎样检查？** 对等距网格核对 $\mathbb E Q_N=T$、$\operatorname{Var}Q_N=2T^2/N$，并与 finite-variation path 的零 QV 比较。
6. **怎样误读？** $(dW)^2=dt$ 不是每个无穷小样本上的代数恒等式，也不能推出 $|dW|=\sqrt{dt}$ 的确定值。
7. **AI 中怎样调用？** 扩散/SDE 模拟必须让噪声方差随 $h$ 缩放并在网格细化时复用同一 Brownian coupling；独立重抽整条路径会破坏 strong-error 与反向过程语义。

> [!success] 第一遍停靠线
> 合上正文后，应能从 $\Delta W_k=N^{-1/2}Z_k$ 推出差商方差 $N$、$\mathbb E Q_N=1$ 与 $\operatorname{Var}Q_N=2/N$，并用 shared-noise 反例说明逐时 Gaussian 边缘不定义 Brownian motion。若仍把 $(dW)^2=dt$ 当作普通微分乘法，请先重做平方增量和。

## 学习目标

完成本章后，应能：

1. 区分 stochastic process、finite-dimensional distributions、sample path 与 path law；
2. 解释 filtration、adaptedness、natural filtration、stopping time 与 martingale；
3. 从定义推出 Brownian covariance $\mathbb E[W_sW_t]=\min(s,t)$；
4. 写出任意有限组时刻的联合 Gaussian 分布；
5. 推导 Brownian bridge 的单时刻条件分布；
6. 证明 Brownian motion 是相对于自然 filtration 的 martingale；
7. 使用 stationary independent increments、scaling 与 time reversal；
8. 说明随机游走的单时刻 CLT 与 Donsker path-space convergence 的区别；
9. 区分连续、Hölder、可微、有限变差与二次变差；
10. 完整证明 Brownian quadratic variation 沿确定性细分在 $L^2$ 中趋于时间长度；
11. 证明连续有限变差路径的 quadratic variation 为0；
12. 推出 Brownian path 在任意非退化区间上具有无限 total variation；
13. 计算多维 Brownian 的 cross variation；
14. 正确解释 white noise 是 generalized derivative 而非普通函数；
15. 识别“相同逐时边缘、不同时间耦合”的扩散模型错误。

> [!question] 初学者读完必须能回答
> 1. Stochastic process、finite-dimensional distributions、sample path 与 path law 有何区别？
> 2. Brownian 的 stationary independent increments 如何导出 covariance $\min(s,t)$？
> 3. 单时刻 Gaussian marginals 为什么不足以定义 Brownian motion？
> 4. $\Delta W=O_{\mathbb P}(\sqrt{\Delta t})$ 为什么使普通差商发散？
> 5. Quadratic variation 为什么收敛到 $T$，有限变差连续路径却为零？
> 6. $(dW)^2=dt$ 应怎样解释，为什么不是普通微分代数？
> 7. 随机游走 CLT 与 Donsker path-space convergence 有何层次差别？

## 零、随机变量不够：我们需要一整条随机轨迹

普通随机变量 $X$ 只回答一次随机输出。连续时间系统需要同时描述

$$
X_0,X_{0.01},X_{0.02},\ldots
$$

之间怎样相关。随机过程是一个随机变量族

$$
\{X_t:t\in I\},
$$

定义在共同概率空间 $(\Omega,\mathcal F,\mathbb P)$ 上，并取值于状态空间 $E$：

$$
X_t:\Omega\to E.
$$

这里有两种都重要、但不能混淆的观察方向。

| 固定什么 | 变化什么 | 得到的对象 |
|---|---|---|
| 固定时刻 $t$ | $\omega$ 变化 | 随机变量 $X_t$ 及其 marginal law |
| 固定样本 $\omega$ | $t$ 变化 | sample path $t\mapsto X_t(\omega)$ |

一张固定时刻的 histogram 只能看到 marginal。SDE、hitting time、pathwise maximum、数值积分和生成采样依赖整条 path law。

### 0.1 最重要的反例：相同 marginals 不等于相同 process

对 $t>0$ 考虑三个过程，它们每个时刻都满足

$$
X_t\sim\mathcal N(0,t).
$$

1. Brownian motion：$X_t=W_t$；
2. shared-noise coupling：$X_t=\sqrt t\,Z$，其中整条路径共用一个 $Z\sim\mathcal N(0,1)$；
3. independent-time sampling：每个 $t$ 都重新独立抽 $X_t=\sqrt t\,Z_t$。

它们的 increment variance 完全不同：

$$
\operatorname{Var}(W_{t+h}-W_t)=h,
$$

$$
\operatorname{Var}(\sqrt{t+h}Z-\sqrt tZ)
=(\sqrt{t+h}-\sqrt t)^2=O(h^2),
$$

$$
\operatorname{Var}(\sqrt{t+h}Z_{t+h}-\sqrt tZ_t)
=2t+h.
$$

第二种在 $t>0$ 附近过于平滑；第三种在 $h\downarrow0$ 时增量甚至不趋于0，因此没有连续版本。三者逐时 histogram 相同，却不是同一个随机动力学。

## 一、过程的三层描述

### 1.1 Finite-dimensional distributions

对任意有限时刻

$$
t_1<\cdots<t_n,
$$

考察随机向量

$$
(X_{t_1},\ldots,X_{t_n}).
$$

这些联合分布的全体称为 finite-dimensional distributions，简称 FDDs。只给每个 $X_t$ 的一维 marginal 不足够；还必须给跨时间依赖。

一致的 FDDs 在适当条件下可由 Kolmogorov extension theorem 产生某个过程。但 extension theorem 先给坐标过程，不自动给连续 sample paths；连续版本还需要额外 regularity 论证。

### 1.2 Path law

若过程有连续路径，可把整条随机函数视为函数空间

$$
C([0,T];\mathbb R^d)
$$

上的随机元素。其分布是 path law。Donsker theorem 讨论的不是单个终点，而是随机游走插值后的 path law 在函数空间中收敛。

### 1.3 Modification 与 indistinguishability

两个过程 $X,Y$ 若对每个固定 $t$ 都有

$$
\mathbb P(X_t=Y_t)=1,
$$

称为 modifications。这里的零概率异常集可以依赖 $t$。

若

$$
\mathbb P(X_t=Y_t\ \text{对所有 }t\in[0,T])=1,
$$

称为 indistinguishable。Pathwise 定理通常需要后一种更强关系。对连续 modifications，可先在可数稠密时刻相等，再由连续性推出 indistinguishability。

## 二、Filtration：把“到时刻 $t$ 已知什么”写进数学

### 2.1 定义

Filtration 是递增的子 $\sigma$-代数族

$$
\mathcal F_s\subseteq\mathcal F_t\subseteq\mathcal F,
\qquad s\le t.
$$

$\mathcal F_t$ 表示到时刻 $t$ 可用的信息。它不只是“历史数据列表”，还包含由历史事件通过可数集合运算产生的全部可判定事件。

过程 $X_t$ 若对每个 $t$ 都是 $\mathcal F_t$-measurable，称为 adapted。直觉是：当前状态不偷看未来。

### 2.2 Natural filtration 与 usual augmentation

过程自身生成的自然 filtration 是

$$
\mathcal F_t^X
=\sigma(X_s:0\le s\le t).
$$

严格随机分析常把它补全所有 $\mathbb P$-零集并取 right-continuous augmentation。这些 usual conditions 会影响 stopping-time、optional sampling 等定理的规范表述；初学时不能把技术条件误当成无关装饰。

### 2.3 Stopping time

随机时间 $\tau$ 若对每个 $t$ 都满足

$$
\{\tau\le t\}\in\mathcal F_t,
$$

称为 stopping time。也就是说，到 $t$ 时刻能判断事件是否已经发生。首次到达

$$
\tau_a=\inf\{t\ge0:X_t=a\}
$$

在连续 adapted 过程的标准条件下是 stopping time；“最后一次到达”通常会依赖未来，未必是。

### 2.4 Martingale

若 $M_t$ adapted、可积，并且

$$
\mathbb E[M_t\mid\mathcal F_s]=M_s,
\qquad s\le t,
$$

则 $M$ 是 martingale。它表示在当前信息下，未来条件均值等于当前值。Martingale 是 conditional statement；只写 $\mathbb E[M_t]=\mathbb E[M_0]$ 远远不够。

## 三、标准 Brownian motion 的定义

实值过程 $W=\{W_t:t\ge0\}$ 称为 standard Brownian motion 或 Wiener process，若：

1. $W_0=0$ almost surely；
2. 对任意 $0\le t_0<t_1<\cdots<t_n$，增量
   $$
   W_{t_1}-W_{t_0},\ldots,W_{t_n}-W_{t_{n-1}}
   $$
   相互独立；
3. 对 $0\le s<t$，
   $$
   W_t-W_s\sim\mathcal N(0,t-s);
   $$
4. sample paths almost surely continuous。

前3条描述 FDD；第4条选择连续版本。不能由“每个时刻 $W_t\sim\mathcal N(0,t)$”单独推出独立增量或连续性。

### 3.1 Stationary increments 与 independent increments

Stationary increments 指增量分布只依赖长度：

$$
W_{s+h}-W_s\overset d=W_h.
$$

Independent increments 指不重叠时间区间上的增量独立。这是两个不同性质；平稳不等于独立。

### 3.2 带 drift 和 scale 的 Brownian motion

若

$$
X_t=x_0+\mu t+\sigma W_t,
$$

则

$$
X_t-X_s\sim\mathcal N(\mu(t-s),\sigma^2(t-s)).
$$

$\mu$ 的单位是 state/time，$\sigma$ 的单位是 state/$\sqrt{\text{time}}$。这个量纲差异预告了 $dt$ 与 $dW_t$ 不是同阶对象。

## 四、从定义推出联合 Gaussian 与 covariance kernel

### 4.1 均值与方差

由定义

$$
\mathbb E[W_t]=0,
\qquad
\operatorname{Var}(W_t)=t.
$$

若 $0\le s\le t$，写成

$$
W_t=W_s+(W_t-W_s).
$$

后一个增量独立于 $W_s$ 且均值为0，因此

$$
\begin{aligned}
\mathbb E[W_sW_t]
&=\mathbb E[W_s^2]
+\mathbb E[W_s(W_t-W_s)]\\
&=s.
\end{aligned}
$$

所以

$$
\boxed{
\operatorname{Cov}(W_s,W_t)=\min(s,t).
}
$$

### 4.2 为什么任意有限组时刻联合 Gaussian

对 $0<t_1<\cdots<t_n$，令独立 Gaussian 增量

$$
\Delta_i=W_{t_i}-W_{t_{i-1}},
\qquad t_0=0.
$$

则

$$
W_{t_k}=\sum_{i=1}^k\Delta_i.
$$

因此 $(W_{t_1},\ldots,W_{t_n})$ 是独立 Gaussian 向量的线性变换，故为 multivariate Gaussian，covariance matrix 为

$$
K_{ij}=\min(t_i,t_j).
$$

这说明 Brownian motion 是 zero-mean Gaussian process；对 Gaussian process，均值函数与 covariance kernel 已决定全部 FDDs。

### 4.3 三时刻手算

取

$$
t_1=\frac14,\qquad t_2=\frac12,\qquad t_3=1.
$$

则

$$
\begin{pmatrix}
W_{1/4}\\W_{1/2}\\W_1
\end{pmatrix}
\sim
\mathcal N\left(
0,
\begin{bmatrix}
1/4&1/4&1/4\\
1/4&1/2&1/2\\
1/4&1/2&1
\end{bmatrix}
\right).
$$

Covariance 不为0说明不同时间的状态高度相关；独立的是不重叠 increments，不是 levels。

## 五、条件分布、martingale 与 Markov 性

### 5.1 未来给定现在

由

$$
W_t=W_s+(W_t-W_s)
$$

以及未来增量独立于 $\mathcal F_s^W$，

$$
W_t\mid\mathcal F_s^W
\sim\mathcal N(W_s,t-s).
$$

于是

$$
\mathbb E[W_t\mid\mathcal F_s^W]=W_s,
$$

所以 $W_t$ 是 martingale。

更一般地，

$$
W_t^2-t
$$

也是 martingale，因为

$$
\mathbb E[W_t^2-t\mid\mathcal F_s]
=W_s^2-s.
$$

这个补偿项 $-t$ 正是 quadratic variation 在条件二阶矩中的影子。

### 5.2 Markov property

未来增量与全部过去独立，因此给定当前 $W_s$ 后，未来分布不再需要完整历史。转移核是

$$
p_{t-s}(y\mid x)
=\frac1{\sqrt{2\pi(t-s)}}
\exp\left[-\frac{(y-x)^2}{2(t-s)}\right].
$$

Martingale 与 Markov 是不同概念：martingale约束条件均值，Markov约束整个条件分布。

### 5.3 Brownian bridge 的单时刻条件分布

对 $0<s<t$，联合 Gaussian conditioning 给

$$
W_s\mid W_t=b
\sim
\mathcal N\left(
\frac{s}{t}b,
\frac{s(t-s)}{t}
\right).
$$

条件均值是连接 $(0,0)$ 与 $(t,b)$ 的直线，但条件路径仍有随机波动；“均值轨迹是直线”不等于“桥路径是直线”。

## 六、Brownian motion 的对称性与缩放

### 6.1 平移后的增量过程

对固定 $s\ge0$，

$$
\widetilde W_t=W_{s+t}-W_s
$$

仍是 Brownian motion，并与 $\mathcal F_s$ 独立。

### 6.2 反射对称

$$
-W_t
$$

仍是 Brownian motion，因为 centered Gaussian increment 关于0对称。

### 6.3 Brownian scaling

对 $c>0$，

$$
\widetilde W_t=\frac1{\sqrt c}W_{ct}
$$

仍是标准 Brownian motion。等价地，

$$
W_{ct}\overset{\mathrm{process}}=
\sqrt c\,W_t.
$$

这里是整个过程 FDD/path law 的等式，不只是单时刻方差相同。

### 6.4 有限时窗反演

固定 $T$，

$$
\widehat W_t=W_T-W_{T-t},
\qquad 0\le t\le T,
$$

作为正向参数 $t$ 的过程仍有 Brownian law。但它相对于原来的 forward filtration 不是“新鲜未来噪声”；time reversal 的 filtration 必须重新说明。DYN-12 会把这一点升级为 reverse diffusion 的 drift 修正。

## 七、多维 Brownian motion

$d$ 维标准 Brownian motion

$$
W_t=(W_t^{(1)},\ldots,W_t^{(d)})
$$

可由 $d$ 个独立一维 Brownian components 构造。其增量满足

$$
W_t-W_s\sim\mathcal N(0,(t-s)I_d).
$$

若 $\Sigma\succeq0$ 且 $LL^\top=\Sigma$，则

$$
X_t=\mu t+LW_t
$$

有

$$
X_t-X_s\sim
\mathcal N(\mu(t-s),(t-s)\Sigma).
$$

矩阵 $L$ 不唯一，但 law 只由 $\Sigma=LL^\top$ 决定。若训练或模拟需要与某一 latent coordinate 对齐，则不同 factor 可能产生不同 pathwise coupling，尽管单步 increment law 相同。

## 八、从随机游走到 Brownian motion

### 8.1 正确缩放从哪里来

令 $\xi_k$ 独立同分布，

$$
\mathbb E[\xi_k]=0,
\qquad
\operatorname{Var}(\xi_k)=1.
$$

随机游走

$$
S_n=\sum_{k=1}^n\xi_k
$$

在时间 $t$ 的扩散缩放是

$$
W^{(n)}_t
=\frac1{\sqrt n}S_{\lfloor nt\rfloor},
$$

再用分段线性或阶梯插值补齐时间。为什么空间除以 $\sqrt n$？因为

$$
\operatorname{Var}(S_{\lfloor nt\rfloor}/\sqrt n)
\to t.
$$

若除以 $n$，随机波动会塌缩到0；若不缩放，方差发散。

### 8.2 单时刻 CLT 还不是 Brownian theorem

对固定 $t$，中心极限定理给

$$
\frac{S_{\lfloor nt\rfloor}}{\sqrt n}
\Rightarrow\mathcal N(0,t).
$$

这只说明一个时刻。要得到整个 Brownian path，还需要：

1. 所有有限维联合分布收敛；
2. path laws tight，排除网格间剧烈逃逸；
3. 指定函数空间与拓扑，如 $C([0,T])$ 的 uniform topology 或 $D([0,T])$ 的 Skorokhod topology。

Donsker invariance principle 在适当 moment 条件下给出

$$
W^{(n)}\Rightarrow W
$$

的函数空间弱收敛。科学空间的随机游走文章提供扩散极限直觉；严格课程必须补上 scaling、FDD、tightness 与 topology，不能把“随机游走等价于 Brownian”理解成有限网格路径逐点相同。

### 8.3 连续性从何而来

Brownian FDD 本身不直接展示连续 sample path。Gaussian moment 给

$$
\mathbb E|W_t-W_s|^p
=C_p|t-s|^{p/2}.
$$

取 $p>2$，Kolmogorov continuity theorem 可推出存在连续 modification，并进一步给低于 $1/2$ 的 Hölder regularity。Brownian 定义通常直接选择这个连续版本。

## 九、路径到底有多粗糙

### 9.1 Increment 的自然尺度

因为

$$
W_{t+h}-W_t\sim\sqrt h\,Z,
\qquad Z\sim\mathcal N(0,1),
$$

所以典型增量是 $\sqrt h$，不是 $h$。差商是

$$
\frac{W_{t+h}-W_t}{h}
\sim\mathcal N\left(0,\frac1h\right).
$$

它的方差随 $h\downarrow0$ 发散。

### 9.2 固定时刻不可微与处处不可微

对任一固定 $t$，若差商 almost surely 收敛到有限导数，就必然依概率收敛；但其 law 为 $\mathcal N(0,1/h)$，不可能 tight 到有限随机变量。因此 Brownian path 在每个预先指定时刻可微的概率为0。

这还没有自动证明“同一条路径在所有不可数时刻都不可微”。更强定理是：

> Brownian sample path almost surely nowhere differentiable。

严格证明需把不可数时刻压缩到可数网格事件，并结合 Gaussian tail 与 Borel–Cantelli；不能把“每个固定 $t$ 的概率为0”直接与不可数并集交换。

### 9.3 Hölder threshold

对任意

$$
0<\alpha<\frac12,
$$

Brownian path 在紧区间上 almost surely 是 $\alpha$-Hölder：

$$
|W_t-W_s|
\le C_\alpha(\omega)|t-s|^\alpha.
$$

但它 almost surely 不是 $1/2$-Hölder。更精细的 modulus 含有

$$
\sqrt{h\log(1/h)}
$$

级别的修正。结论不是“Brownian 不连续”，而是“连续但接近 $1/2$ 阈值时非常粗糙”。

## 十、Total variation、$p$-variation 与 quadratic variation

### 10.1 Total variation

对连续路径 $x:[0,T]\to\mathbb R$，partition

$$
\Pi=\{0=t_0<\cdots<t_n=T\}
$$

上的一阶变差和是

$$
V_1(x;\Pi)
=\sum_{i=0}^{n-1}|x_{t_{i+1}}-x_{t_i}|.
$$

Total variation 定义为对所有有限 partitions 取 supremum：

$$
\operatorname{TV}_{[0,T]}(x)
=\sup_\Pi V_1(x;\Pi).
$$

绝对连续或 $C^1$ 路径满足

$$
\operatorname{TV}(x)
=\int_0^T|x'(t)|dt<\infty.
$$

### 10.2 $p$-variation

一般化为

$$
V_p(x;[0,T])
=\sup_\Pi\sum_i|\Delta_i x|^p.
$$

Brownian 的 variation index 是2：almost surely 对 $p>2$ 有有限 $p$-variation，而对 $p\le2$ 为无限。注意这一定义取所有 partitions 的 supremum。

### 10.3 Quadratic variation 不是 2-variation supremum

给定一列 mesh

$$
|\Pi_n|=\max_i(t_{i+1}^{(n)}-t_i^{(n)})\to0,
$$

quadratic variation 研究

$$
Q_{\Pi_n}(x)
=\sum_i(\Delta_i x)^2
$$

的极限，通常按 in probability、$L^2$ 或 almost surely 指定。它没有对所有 partitions 取 supremum，因此不能与 $V_2$ 混用。

对随机过程，partition 是否 deterministic、是否依赖路径、是否 nested，以及采用哪种 convergence mode，都属于 theorem contract。

## 十一、Brownian quadratic variation 的完整 $L^2$ 证明

固定 $T>0$，令 deterministic partition

$$
\Pi=\{0=t_0<t_1<\cdots<t_n=T\},
$$

并记

$$
\Delta_iW=W_{t_{i+1}}-W_{t_i},
\qquad
\Delta_it=t_{i+1}-t_i.
$$

定义

$$
Q_\Pi(W)=\sum_{i=0}^{n-1}(\Delta_iW)^2.
$$

### 11.1 期望恰好是 $T$

由于

$$
\Delta_iW\sim\mathcal N(0,\Delta_it),
$$

所以

$$
\mathbb E[(\Delta_iW)^2]=\Delta_it.
$$

求和得到

$$
\boxed{
\mathbb E[Q_\Pi(W)]
=\sum_i\Delta_it=T.
}
$$

这里没有近似；任意 partition 的期望都正好等于时间长度。

### 11.2 方差随 mesh 消失

若 $Z\sim\mathcal N(0,\sigma^2)$，则

$$
\mathbb E[Z^4]=3\sigma^4,
$$

因此

$$
\operatorname{Var}(Z^2)
=3\sigma^4-\sigma^4
=2\sigma^4.
$$

不重叠 Brownian increments 独立，所以平方也独立：

$$
\begin{aligned}
\operatorname{Var}(Q_\Pi(W))
&=\sum_i\operatorname{Var}((\Delta_iW)^2)\\
&=2\sum_i(\Delta_it)^2\\
&\le2|\Pi|\sum_i\Delta_it\\
&=2T|\Pi|.
\end{aligned}
$$

当 $|\Pi|\to0$，

$$
\mathbb E[(Q_\Pi(W)-T)^2]
=\operatorname{Var}(Q_\Pi(W))
\to0.
$$

故

$$
\boxed{
Q_{\Pi_n}(W)\xrightarrow{L^2}T
}
$$

并因此依概率收敛。记作

$$
[W]_T=T.
$$

### 11.3 Uniform partition 的误差尺度

若 $n$ 等长小区间，$\Delta t=T/n$，则

$$
\operatorname{Var}(Q_n)=\frac{2T^2}{n},
$$

$$
\operatorname{RMSE}(Q_n)
=T\sqrt{\frac2n}.
$$

所以单条有限网格 Brownian path 的 realized quadratic variation 不会精确等于 $T$；其典型随机误差只按 $n^{-1/2}$ 缩小。

### 11.4 Dyadic partitions 上的 almost-sure 收敛

取 $n=2^m$ 的 dyadic partitions。对任意 $\varepsilon>0$，Chebyshev inequality 给

$$
\mathbb P(|Q_{2^m}-T|>\varepsilon)
\le\frac{2T^2}{\varepsilon^2\,2^m}.
$$

右侧关于 $m$ 可求和。由 Borel–Cantelli，

$$
Q_{2^m}\to T
\qquad\text{almost surely}.
$$

这说明 stronger mode 依赖 partition sequence 的结构；不能仅从任意 partitions 的 $L^2$ 收敛，直接声称所有可能 partition families 同时 pathwise 收敛。

## 十二、为什么 Brownian total variation 必然无限

先证明一个确定性引理。

> [!theorem] 连续有限变差路径的平方和消失
> 若连续 $x$ 在 $[0,T]$ 上 total variation 有限，则对任意 mesh 趋于0的 partitions，
> $$
> \sum_i(\Delta_ix)^2\to0.
> $$

证明：由连续函数在紧区间上一致连续，

$$
\max_i|\Delta_ix|\to0.
$$

并且

$$
\sum_i(\Delta_ix)^2
\le
\left(\max_i|\Delta_ix|\right)
\sum_i|\Delta_ix|
\le
\left(\max_i|\Delta_ix|\right)\operatorname{TV}(x)
\to0.
$$

Brownian motion 沿 dyadic partitions almost surely 有

$$
\sum_i(\Delta_iW)^2\to T>0.
$$

所以 almost surely

$$
\boxed{
\operatorname{TV}_{[0,T]}(W)=\infty
}
$$

对每个 $T>0$ 成立。这个证明直接把“非零 quadratic variation”与“不能按 Riemann–Stieltjes 有限变差路径处理”连接起来。

> [!warning] 不能越界的推论
> 非零 quadratic variation 足以排除有限变差，但单靠这一点不等于完成 nowhere-differentiability theorem。一个函数可以在某些点可微而总体具有非零或异常变差；“处处不可微”需要更强路径论证。

## 十三、Cross variation 与多维噪声

### 13.1 定义与 polarization

给定过程 $X,Y$，cross variation 沿同一 partitions 定义为

$$
[X,Y]_T
=\lim_{|\Pi|\to0}
\sum_i\Delta_iX\,\Delta_iY.
$$

若相关极限存在，可由 polarization identity 写成

$$
\boxed{
[X,Y]_T
=\frac14\left([X+Y]_T-[X-Y]_T\right).
}
$$

### 13.2 独立 Brownian components

若 $W^{(i)},W^{(j)}$ 是独立标准 Brownian motions，则 $i\ne j$ 时

$$
[W^{(i)},W^{(j)}]_t=0,
$$

而

$$
[W^{(i)}]_t=t.
$$

简写为

$$
\boxed{
dW_t^{(i)}\,dW_t^{(j)}
=\delta_{ij}\,dt.
}
$$

若 $X_t=LW_t$，则 matrix quadratic covariation 是

$$
[X]_t=tLL^\top.
$$

因此 SDE 中真正控制局部 diffusion covariance 的是 $LL^\top$，而不是某个唯一矩阵平方根 $L$。

### 13.3 相关二维 Brownian

若

$$
\operatorname{Cov}(W_t^{(1)},W_t^{(2)})=\rho t,
$$

则

$$
[W^{(1)},W^{(2)}]_t=\rho t.
$$

实现中若声称独立噪声，却错误复用同一 random stream，cross variation 会暴露隐藏相关。

## 十四、$(dW)^2=dt$ 到底是什么意思

### 14.1 它不是逐点代数恒等式

$dW_t$ 不是普通无穷小实数，也不存在 ordinary derivative $\dot W_t$。表达式

$$
(dW_t)^2=dt
$$

是 quadratic-variation calculus 的记忆规则，表示离散和

$$
\sum_i(\Delta_iW)^2
$$

在细分极限中保留为时间，而不是每个单步都精确满足 $(\Delta_iW)^2=\Delta_it$。

### 14.2 尺度账本

在均方量级上：

| 项 | 典型尺度 | 对 $n\asymp1/\Delta t$ 项求和 |
|---|---:|---:|
| $\Delta t$ | $\Delta t$ | $O(1)$ |
| $\Delta W$ | $\sqrt{\Delta t}$ | 有随机抵消，形成 $O(1)$ Brownian 位移 |
| $(\Delta W)^2$ | $\Delta t$ | $O(1)$，形成 quadratic variation |
| $\Delta t\,\Delta W$ | $\Delta t^{3/2}$ | 均方意义消失 |
| $(\Delta t)^2$ | $\Delta t^2$ | 消失 |

这就是下一章 Taylor expansion 不能丢掉二阶 $(\Delta W)^2$ 的原因。

### 14.3 Ordinary smooth path 的对照

若 $x$ 可微，

$$
\Delta x=x'(t)\Delta t+o(\Delta t),
$$

所以

$$
\sum_i(\Delta x_i)^2
=O(\Delta t)\to0.
$$

普通链式法则之所以没有二阶累计项，是因为 smooth path 的 quadratic variation 为0。

## 十五、White noise：Brownian 的“导数”只能是广义对象

形式上常写

$$
\xi(t)=\frac{dW_t}{dt},
$$

并记

$$
\mathbb E[\xi(t)]=0,
\qquad
\mathbb E[\xi(t)\xi(s)]=\delta(t-s).
$$

但 Brownian path almost surely nowhere differentiable，所以 $\xi$ 不是普通 pointwise function。严格方式是把 white noise 看成 generalized random field：对测试函数 $\varphi\in L^2$，

$$
\langle\xi,\varphi\rangle
\sim\mathcal N(0,\|\varphi\|_{L^2}^2),
$$

并且

$$
\mathbb E[
\langle\xi,\varphi\rangle
\langle\xi,\psi\rangle]
=\langle\varphi,\psi\rangle_{L^2}.
$$

### 15.1 网格白噪声的 amplitude 为什么发散

在步长 $\Delta t$ 上，

$$
\Delta W_k\sim\mathcal N(0,\Delta t).
$$

若定义 piecewise-constant derivative proxy

$$
\xi_k=\frac{\Delta W_k}{\Delta t},
$$

则

$$
\operatorname{Var}(\xi_k)=\frac1{\Delta t}.
$$

网格越细，pointwise amplitude 越大；但积分

$$
\xi_k\Delta t=\Delta W_k
$$

仍有正确 $\sqrt{\Delta t}$ 尺度。若在不同时间步直接使用方差固定的“噪声速度”，连续极限会错误。

## 十六、Brownian simulation 的正确合同

### 16.1 固定网格模拟

给定

$$
0=t_0<\cdots<t_n=T,
$$

独立采样

$$
Z_i\sim\mathcal N(0,1),
$$

并递推

$$
W_{t_{i+1}}
=W_{t_i}+\sqrt{\Delta_it}\,Z_i.
$$

这会精确产生网格点上的 Brownian FDD，不是 Euler 近似；近似只发生在网格间 path 表示和后续 SDE 离散化。

### 16.2 线性插值不是网格间真实条件 law

已知端点 $W_{t_i},W_{t_{i+1}}$ 时，中间 Brownian path 是 Brownian bridge，而不是确定性直线。若只关心网格值，线性绘图可以；若要 barrier crossing、first passage 或 adaptive refinement，必须采样 bridge 或使用 Brownian tree。

### 16.3 Nested refinement

比较多个步长时，若每个分辨率重新抽独立路径，observed difference 同时包含 discretization 与 Monte Carlo path mismatch。更可审计的做法是：

1. 先生成最细 increments；
2. 相邻 increments 求和得到粗 increments；
3. 或使用 Brownian bridge/Brownian tree 保持同一 underlying path；
4. 固定 seed 只保证可重复，不自动保证跨分辨率耦合正确。

### 16.4 数值 precision 与 random generator

报告至少包括：

- PRNG 算法与 seed；
- Gaussian sampler 与 dtype；
- time grid 与非均匀步长；
- independent streams/counter-based key policy；
- 跨 batch/device 是否意外复用随机流；
- pathwise、weak-law 还是 distributional metric；
- 罕见事件是否需要 bridge correction。

## 十七、AI 接口：扩散边缘不等于扩散过程

### 17.1 单时刻 reparameterization 的边界

扩散模型常写

$$
X_t=\alpha_tX_0+\sigma_t\varepsilon,
\qquad
\varepsilon\sim\mathcal N(0,I).
$$

这很好地描述固定 $t$ 的 conditional marginal

$$
q_t(x_t\mid x_0).
$$

但若对每个 $t$ 重新独立抽 $\varepsilon_t$，得到的多时刻 joint law 通常不是连续扩散；若所有 $t$ 共用同一个 $\varepsilon$，又得到另一条过度相关路径。要声称某个 forward SDE，必须证明 transition kernels、increment covariance 或 SDE solution law 与这些 marginals 相容。

### 17.2 训练只采 marginals，采样却调用 path dynamics

Score training 常可随机抽 $t$ 和 noisy $X_t$，不显式模拟完整 forward path；这不意味着 path law 不重要。Reverse-time SDE、predictor–corrector 与 probability-flow ODE 都要调用明确的连续时间 dynamics。必须分开：

| 对象 | 训练/推理角色 |
|---|---|
| $q_t(x_t\mid x_0)$ | 固定时刻加噪监督 |
| $q(x_s,x_t\mid x_0)$ | 时间耦合与 transition |
| forward SDE | path law、generator 与 Fokker–Planck |
| learned score | marginal log-density gradient 的近似 |
| reverse sampler | 依赖 score、noise coupling 与数值求解器 |

### 17.3 Noise schedule 的量纲

若离散更新写成

$$
X_{k+1}
=X_k+b_k\Delta t+g_k\sqrt{\Delta t}\,Z_k,
$$

则 stochastic increment 必须带 $\sqrt{\Delta t}$。把 $g_kZ_k$ 直接当每步增量会使总方差随步数发散；把它乘 $\Delta t$ 又会使 diffusion 在连续极限中消失。

### 17.4 Common random numbers 与模型比较

比较两个 sampler 或两个步长时，共用 underlying Brownian increments 可显著降低差分方差。但这改变的是 evaluation coupling，不改变各自 marginal law。报告中应写明：

- 是否 paired paths；
- 是否同一 Brownian tree；
- 指标是 pathwise error、weak expectation 还是最终 sample quality；
- common randomness 是否只用于比较而非训练泄漏。

### 17.5 Brownian noise 不是“任何高斯扰动”

高斯只是 increment law 的一部分。Brownian 还要求：

- variance 与时间长度成正比；
- 不重叠 increments 独立；
- 时间一致的 joint Gaussian covariance；
- 连续路径版本。

Colored Gaussian noise、fractional Brownian motion、Ornstein–Uhlenbeck noise 与共享 latent noise 都可能是 Gaussian，却有不同 covariance、variation 和 calculus。

## 十八、三个反例把边界钉死

### 18.1 每个 marginal 正确，过程仍错误

前述

$$
W_t,\qquad \sqrt tZ,\qquad \sqrt tZ_t
$$

都有 $\mathcal N(0,t)$ marginals，但 increment variance 分别为 $h$、$O(h^2)$ 与 $2t+h$。

### 18.2 连续不等于可微

Brownian 连续，却 almost surely nowhere differentiable。Neural interpolation 若强制 path smooth，可能保留若干 marginals，却改变 hitting、quadratic variation 和 stochastic integral。

### 18.3 总方差对，不等于独立增量

可构造 Gaussian process 满足 $\operatorname{Var}(X_t)=t$，却令不同 increments 相关。只画 endpoint variance curve 不能证明是 Brownian；至少还要查

$$
\operatorname{Cov}(X_t-X_s,X_v-X_u)
$$

在不重叠区间是否为0。

## 十九、随机过程与扩散程序审计卡

~~~text
PROCESS
  probability space / state space / time index
  FDD or transition kernel
  path space and continuity/cadlag claim
  filtration and adaptedness

NOISE
  increment mean / covariance / independence
  sqrt(dt) scaling and units
  cross-component covariance
  PRNG / key / stream policy

LIMIT
  convergence object: endpoint / FDD / path law
  convergence mode: a.s. / probability / Lp / weak
  topology and interpolation
  partition deterministic/path-dependent/nested

NUMERICS
  finest Brownian increments or Brownian tree
  pathwise vs weak error
  bridge correction for events
  dtype / seed / batch-device independence

AI CLAIM
  marginal noising law vs full forward process
  population score vs learned score
  reverse SDE vs probability-flow ODE
  solver/NFE and common-randomness policy
~~~

## 二十、最小掌握检查

### 概念

1. 为什么一组 marginals 不能确定一个 process？
2. FDD、path、path law 分别是什么？
3. Adapted 与 independent increments 是同一性质吗？
4. Brownian levels 为什么相关，而 increments 可以独立？
5. Modification 与 indistinguishability 有何区别？
6. Total variation、2-variation supremum 与 quadratic variation 有何区别？
7. White noise 为什么不能当普通函数？

### 闭卷推导

在不看正文时重建：

$$
\operatorname{Cov}(W_s,W_t)=\min(s,t),
$$

$$
W_s\mid W_t=b
\sim
\mathcal N\left(\frac st b,\frac{s(t-s)}t\right),
$$

$$
\mathbb E[Q_\Pi]=T,
\qquad
\operatorname{Var}(Q_\Pi)
=2\sum_i(\Delta_it)^2,
$$

以及有限 total variation 推出 quadratic variation 为0的证明。

### 数值/研究检查

1. 用 nested increments 比较 $Q_n$、total variation 与差分斜率；
2. 验证 $Q_n$ 的 RMSE 约按 $n^{-1/2}$；
3. 检验不重叠 increments 的 covariance；
4. 比较 Brownian/shared-noise/independent-time 三种相同 marginal coupling；
5. 对多维噪声报告 realized cross variation；
6. 写清固定 seed 与正确 Brownian coupling 的区别。

## 二十一、学习闭环与后继接口

- 分层题：[[习题 - 随机过程、Brownian 运动与二次变差]]；
- 独立详解：[[解答 - 随机过程、Brownian 运动与二次变差]]；
- 复现实验：[[实验 - Brownian 增量、路径粗糙性与时间耦合审计]]；
- 下一章：[[Itô 引理与随机微分方程]]将从 simple adapted integrands 构造 Itô integral，证明 Itô isometry，并由 quadratic variation 推出二阶链式法则；
- 再下一章：[[Fokker-Planck 方程与概率流 ODE]]将把 path law 的 drift/diffusion 提升为 marginal density evolution。

> [!check] 当前状态
> 正文、机制图、15道 A—E 题、逐题详解和三轨实验均为 composed；没有学习者首次闭卷答案、独立改参复现与间隔复测，因此保持 draft，不记为 mastered。

## 二十二、来源分工与科学空间入口

- [MIT 18.175 Brownian motion lecture](https://math.mit.edu/~sheffield/2016175/Lecture24.pdf)：定义、独立增量、Gaussian process与基本路径性质；
- [MIT 15.070J Quadratic Variation](https://ocw.mit.edu/courses/15-070j-advanced-stochastic-processes-fall-2013/resources/mit15_070jf13_lec8/)：quadratic variation与随机积分前置；
- [Durrett, Probability: Theory and Examples](https://math.duke.edu/~rtd/PTE/PTE5_011119.pdf)：Brownian construction、Markov/martingale、path properties与Donsker theorem；
- [Mörters–Peres, Brownian Motion](https://www.mi.uni-koeln.de/~moerters/book/book.pdf)：Brownian path、随机游走联系与更深入理论；
- [Song et al., Score-Based Generative Modeling through SDEs](https://arxiv.org/abs/2011.13456)：连续扩散生成的原始AI接口；
- [[S-2016-Su-3750-随机游走模型]]：随机游走、扩散缩放与PDE的中文问题入口；
- [[S-2022-Su-9209-扩散模型SDE篇]]：扩散模型中SDE、离散更新与连续分析的中文入口。

正式定义、收敛模式和路径定理由课程/教材承担；科学空间文章负责提供随机游走与扩散生成的问题意识。本章自行补严 marginal/path-law 区分、partition contract、二次变差证明和可复现实验，不把形式路径积分或 $dW^2=dt$ 记忆式替代随机分析定理。
