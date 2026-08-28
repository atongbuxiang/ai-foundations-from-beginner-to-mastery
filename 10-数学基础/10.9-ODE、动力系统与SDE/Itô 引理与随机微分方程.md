---
type: concept
status: draft
area: [math/probability, math/stochastic-processes, math/sde, math/numerical-analysis, ai/generative-modeling]
aliases: [Itô calculus, 伊藤引理, stochastic differential equation, 随机微分方程, Euler-Maruyama]
prerequisites: ["[[随机过程、Brownian 运动与二次变差]]", "[[期望、方差与矩]]", "[[协方差、相关性与条件期望]]", "[[随机变量的收敛与大数定律]]", "[[常微分方程、初值问题与解的存在唯一性]]", "[[Euler、Runge-Kutta 与离散化误差]]"]
related: ["[[ODE、动力系统与 SDE MOC]]", "[[Fokker-Planck 方程与概率流 ODE]]", "[[时间反演、score 与扩散生成动力学]]", "[[实验 - Itô 和、SDE 强弱误差与离散梯度审计]]"]
sources: ["MIT-15.070J-2013-Ito-Integral", "MIT-18.S096-2013-Ito-Calculus", "Oksendal-Stochastic-Differential-Equations", "Kloeden-Platen-Numerical-SDE", "Li-et-al-2020-Scalable-SDE-Gradients", "Kidger-et-al-2021-Neural-SDE-GAN", "Song-et-al-2021-Score-SDE", "Su-3762-Stochastic-Differential-Equation", "Su-9209-Diffusion-SDE"]
created: 2026-08-19
updated: 2026-08-27
---

# Itô 引理与随机微分方程

> [!abstract] 本章主问题
> 随机微分方程
> $$
> dX_t=a(t,X_t)\,dt+b(t,X_t)\,dW_t
> $$
> 不是把不可微的 $W_t$ 强行求导，而是以下积分方程的简写：
> $$
> X_t=X_0+\int_0^t a(s,X_s)\,ds+\int_0^t b(s,X_s)\,dW_s.
> $$
> 第二个积分由适应的左端点随机和在 $L^2$ 中定义。因为 Brownian quadratic variation 满足 $[W]_t=t$，链式法则会保留二阶项：
> $$
> df(t,X_t)
> =
> \left(
> f_t+af_x+\frac12b^2f_{xx}
> \right)dt
> +bf_x\,dW_t.
> $$
> 这不是符号修饰，而是决定 exact solution、drift conversion、density evolution、数值阶与神经 SDE 训练梯度的核心结构。

> [!important] 与相邻章节的分工
> [[随机过程、Brownian 运动与二次变差]]负责 filtration、Brownian path 与 $[W]_t=t$；本章负责 Itô integral、Itô formula、SDE 解概念、经典模型、Itô/Stratonovich 与 Euler–Maruyama。[[Fokker-Planck 方程与概率流 ODE]]才完整推导 generator 的伴随密度方程与同边缘 ODE；[[时间反演、score 与扩散生成动力学]]才处理反向 filtration、score drift 与生成采样。

先用下图回答一个视觉问题：**Itô integral 怎样由 adapted left sums 构造，quadratic variation 为什么保留链式法则二阶项，而 SDE 数值结果应按哪些对象验收？**

![[00-知识库管理/_assets/figures/dynamics/fig-ito-integral-sde-contract-v2.svg|880]]

> [!figure] 图 10.9.10a｜Itô 随机和、二阶 formula 与 SDE 合同
> A 用左端点 step integrand 表示 $\sum H_{t_i}\Delta W_i$，强调 $H_{t_i}$ 在该增量发生前可知，并列出零均值与 Itô isometry；B 从 $\Delta X=a\,dt+b\,dW$ 的平方尺度保留 $b^2dt$，得到 $df=(f_t+af_x+\frac12b^2f_{xx})dt+bf_xdW$；C 串联积分方程/filtration、适定性、coupled-path EM/Milstein 和 strong/weak/gradient diagnostics。来源：独立绘制；理论接口参考 Itô integral、isometry、Itô formula 与 numerical SDE；生成脚本：[[plot_stochastic_dynamics_v2.py]]；确定性证明地图，无随机种子。

**怎样读图。** A 先在 simple adapted process 上定义随机积分，利用 isometry 在 $L^2$ 中闭包；B 再按 $dt,dW,(dW)^2$ 尺度保留 Taylor 项，不能从 ordinary chain rule 猜结论；C 最后把微分记号还原为带 filtration 的 integral equation，数值细化必须复用/嵌套同一 Brownian path 才能测 strong error，weak error 则比较 law functional/expectation。

**适用边界（图没有证明什么）。** 图不覆盖 anticipating integrals、local time、jump SDE 或 rough paths；adaptedness 也不是一般积分存在的全部技术条件。Global Lipschitz/linear growth 是常用充分条件而非最弱条件。Euler–Maruyama 的 $1/2$ strong order 不是任意非光滑/非全局 Lipschitz SDE 的普适保证，positivity 和 invariant preservation需另查。

> [!note] 课程位置
> DYN-09 建立了 Brownian 的 $\sqrt{dt}$ 增量与非零 quadratic variation。本章把这些路径事实组织成随机积分和 SDE：先说明 $dX=a\,dt+b\,dW$ 是积分方程，再用 Itô formula 修正普通链式法则，最后区分 exact SDE、数值离散和梯度对象。DYN-11 将把本章的 generator 取 adjoint，得到 density 的 Fokker–Planck 方程。

> [!tip] 建议两遍阅读
> **第一遍**只解常系数 VP–OU：用 integrating factor 得到 conditional Gaussian，加入 Gaussian 初值求 marginal，再对 $X_t^2$ 用 Itô formula 核对二阶矩。**第二遍**再进入 Itô integral/isometry、强弱解、Itô–Stratonovich、一般多维 formula、Euler–Maruyama/Milstein、strong/weak convergence 与 neural-SDE gradient。第一遍必须能指出 ordinary chain rule 漏掉了哪一项。

## 本章的推导问题链

1. 为什么 $dX_t=a\,dt+b\,dW_t$ 必须还原为带 filtration 的积分方程？
2. Itô integral 为什么使用 adapted left sums，Itô isometry 控制什么收敛？
3. Brownian quadratic variation 怎样让 Taylor 展开中的 $(dX)^2$ 保留为 $b^2dt$？
4. Itô formula 的 generator 项如何同时控制期望、矩与下一章的 density PDE？
5. Linear SDE 怎样用 integrating factor 精确求解，条件分布与边缘分布为什么是两张账？
6. Euler–Maruyama 的一步均值/方差怎样与精确 transition 比较？
7. Strong error、weak error、distributional error 与 gradient error 为什么不能用同一个曲线替代？

## 贯穿算例：可解析的 variance-preserving OU 扩散

取

$$
\boxed{
dX_t=-X_t\,dt+\sqrt2\,dW_t,
\qquad
X_0\sim\mathcal N\!\left(2,\frac14\right),
}
$$

并令 $X_0$ 与 Brownian motion 独立。这是标准 VP SDE 在常数 $\beta=2$ 时的形式：drift 为 $-\frac12\beta X_t=-X_t$，diffusion scale 为 $\sqrt\beta=\sqrt2$。

### 符号与对象账本

| 对象 | 类型 | 本例中的值/作用 | 不可直接称为 |
|---|---|---|---|
| $X_0$ | random initial state | $\mathcal N(2,1/4)$ | 固定条件初值 $x_0$ |
| $W_t$ | Brownian driver | 与 $X_0$ 独立 | 每时刻独立 Gaussian |
| $a(x)$ | Itô drift | $-x$ | sample-path ordinary derivative |
| $b$ | diffusion coefficient | $\sqrt2$ | noise variance；后者为 $b^2dt$ |
| $q_{t|0}(\cdot|x_0)$ | conditional transition law | 固定 $X_0=x_0$ | marginal $p_t$ |
| $p_t$ | marginal law | 对 $X_0$ 再平均 | 单条 path distribution |
| $\mathcal L$ | generator | $-x\partial_x+\partial_{xx}$ | density 上的 adjoint $\mathcal L^*$ |
| $\widehat X_n$ | numerical state | Euler–Maruyama 网格值 | exact $X_{t_n}$ |

### 第一步：先把微分记号还原为积分方程

本例的定义是

$$
X_t
=X_0-\int_0^tX_s\,ds+\sqrt2\int_0^t dW_s.
$$

更有用的是乘 integrating factor $e^t$。Itô product rule 中 $e^t$ 是 finite variation，所以没有 cross-variation 项：

$$
d(e^tX_t)
=e^tX_tdt+e^tdX_t
=\sqrt2e^t dW_t.
$$

积分得到

$$
\boxed{
X_t=e^{-t}X_0+\sqrt2\int_0^t e^{-(t-s)}dW_s.
}
$$

### 第二步：区分 conditional law 与 marginal law

固定 $X_0=x_0$，Itô integral 是均值零 Gaussian，且由 isometry

$$
2\int_0^t e^{-2(t-s)}ds=1-e^{-2t}.
$$

因此

$$
\boxed{
X_t\mid X_0=x_0
\sim\mathcal N\!\left(e^{-t}x_0,\,1-e^{-2t}\right).
}
$$

也可重参数化为

$$
X_t=e^{-t}X_0+\sqrt{1-e^{-2t}}\,\varepsilon,
\qquad \varepsilon\sim\mathcal N(0,1).
$$

再对随机 $X_0\sim\mathcal N(2,1/4)$ 平均，得到

$$
\boxed{
p_t
=\mathcal N(m_t,v_t),
\qquad
m_t=2e^{-t},
\qquad
v_t=1-\frac34e^{-2t}.
}
$$

Conditional variance 从 $0$ 增到 $1$；marginal variance 从 $1/4$ 增到 $1$。两者不同，不能把训练时已知的 $q_{t|0}$ 当成未知数据边缘 $p_t$。

### 第三步：Itô formula 核对二阶矩

对 $f(x)=x^2$，ordinary chain rule 会写 $d(X_t^2)=2X_tdX_t$，但 Itô formula 还保留 $(dX_t)^2=2dt$：

$$
\boxed{
d(X_t^2)
=(-2X_t^2+2)dt
+2\sqrt2X_t\,dW_t.
}
$$

在可积条件下 stochastic integral 的期望为零，故

$$
\frac d{dt}\mathbb E[X_t^2]
=-2\mathbb E[X_t^2]+2.
$$

由显式 marginal，

$$
\mathbb E[X_t^2]
=m_t^2+v_t
=1+\frac{13}{4}e^{-2t}.
$$

其导数为 $-\frac{13}{2}e^{-2t}$，而右边

$$
-2\left(1+\frac{13}{4}e^{-2t}\right)+2
=-\frac{13}{2}e^{-2t},
$$

完全一致。若漏掉 Itô 的 $+2dt$，方差就不会趋向正确的 stationary value $1$。

### 第四步：Euler–Maruyama 先比较一步 transition

步长 $h$ 的 Euler–Maruyama 是

$$
\widehat X_{n+1}
=(1-h)\widehat X_n+\sqrt{2h}\,\xi_n,
\qquad \xi_n\overset{\mathrm{iid}}{\sim}\mathcal N(0,1).
$$

从固定 $x$ 出发，一步 numerical conditional mean/variance 为

$$
(1-h)x,
\qquad 2h,
$$

而 exact transition 是

$$
e^{-h}x,
\qquad1-e^{-2h}.
$$

在 $h=0.1$ 时：

| 对象 | EM | exact |
|---|---:|---:|
| mean factor | $0.9$ | $0.904837418$ |
| conditional variance | $0.2$ | $0.181269247$ |

这只是一步 distributional calibration。测 strong error 时必须让 coarse/fine 方法共享同一 Brownian path；各自重抽噪声只会测两个独立样本的差。

## 核心公式七问：Itô formula 为什么多出二阶项

对

$$
dX_t=a(t,X_t)dt+b(t,X_t)dW_t,
$$

有

$$
\boxed{
df(t,X_t)
=\left(f_t+af_x+\frac12b^2f_{xx}\right)dt
+bf_xdW_t.
}
$$

1. **解决什么问题？** 给 Brownian-driven process 上的复合函数提供正确链式法则，并定义 generator。
2. **对象与形状？** 一维时 $a,b,X$ 为标量；多维时 diffusion matrix 通过 $D=BB^T$ 与 Hessian contraction 进入。
3. **从哪里来？** Taylor 展开保留一阶 $dX$ 和二阶 $(dX)^2$；$dW=O_{\mathbb P}(\sqrt{dt})$ 使 $b^2(dW)^2$ 累积为 $b^2dt$。
4. **需要什么条件？** $f$ 至少具有相应 $C^{1,2}$ regularity，SDE/积分满足适应性与可积条件；更弱版本需另述。
5. **怎样检查？** 对 $f(x)=x,x^2,e^x$ 逐项核对；本例 $f=x^2$ 必须产生 $+2dt$ 并恢复正确 moment ODE。
6. **怎样误读？** $(dW)^2=dt$ 不是普通代数，$dt\,dW$ 和 $(dt)^2$ 的忽略也来自分割尺度，而非形式删除规则。
7. **AI 中怎样调用？** Neural SDE、diffusion 与 stochastic control 的 loss/gradient 必须匹配 Itô/Stratonovich 解释、连续模型和实际离散器；换解释会改变 drift。

> [!success] 第一遍停靠线
> 合上正文后，应能用 integrating factor 推出 OU 条件均值与方差，再从随机 Gaussian 初值得到 $m_t=2e^{-t}$、$v_t=1-\frac34e^{-2t}$；随后对 $X_t^2$ 写出完整 Itô differential 并解释 $+2dt$ 的来源。若把 $q_{t|0}$ 与 $p_t$ 写成同一对象，请先回到条件/边缘两步。

## 学习目标

完成本章后，应能：

1. 解释普通 Riemann–Stieltjes 积分为何不能直接处理 Brownian integrator；
2. 从 simple adapted process 定义 Itô integral；
3. 逐步证明 simple process 上的零均值与 Itô isometry；
4. 说明等距公式如何把积分延拓到平方可积 predictable integrands；
5. 推导 $\int_0^T W_t\,dW_t=(W_T^2-T)/2$；
6. 从 Taylor 展开与 quadratic variation 推导一维 Itô formula；
7. 写出一般 Itô process 和多维 Itô formula；
8. 把 SDE 微分记号还原成带 filtration 的积分方程；
9. 区分 strong/weak solution、pathwise uniqueness 与 uniqueness in law；
10. 说明 global Lipschitz 与 linear growth 为何足以保证强解适定；
11. 求解 arithmetic Brownian、geometric Brownian 与 Ornstein–Uhlenbeck；
12. 区分 Itô 与 Stratonovich，并正确转换 drift；
13. 区分 numerical strong error、weak error 与 distributional diagnostic；
14. 推导 scalar Euler–Maruyama 与 Milstein 更新；
15. 审计 neural SDE、扩散采样与 solver gradient 的连续/离散对象。

> [!question] 初学者读完必须能回答
> 1. 为什么普通 Riemann–Stieltjes 积分不能直接处理 Brownian integrator？
> 2. Simple adapted process 的 Itô integral 怎样定义，isometry 如何延拓它？
> 3. 为什么 $\int_0^T W_t\,dW_t=(W_T^2-T)/2$ 而不是 $W_T^2/2$？
> 4. Itô formula 的 $\frac12b^2f_{xx}$ 从哪个尺度极限产生？
> 5. Strong solution、weak solution、pathwise uniqueness 与 uniqueness in law 有何区别？
> 6. EM strong error 与 weak error 的耦合/观测对象有何不同？
> 7. Discrete tangent、finite difference 与 continuous gradient 为什么是三道不同检查？

## 零、为什么“对白噪声做 ODE”不是定义

形式上常把 SDE 写成

$$
\frac{dX_t}{dt}
=
a(t,X_t)+b(t,X_t)\,\xi_t,
\qquad
\xi_t=\frac{dW_t}{dt}.
$$

但 Brownian path almost surely nowhere differentiable，$\xi$ 只能理解为广义随机对象。若把上式交给普通 ODE solver，并在每个网格点采一个方差固定的 Gaussian，通常会犯量纲错误：长度为 $h$ 的 Brownian increment 应满足

$$
\Delta W\sim\mathcal N(0,h),
\qquad
\Delta W=O_{\mathbb P}(\sqrt h),
$$

而不是 $O_{\mathbb P}(h)$，也不是方差与 $h$ 无关。

真正定义必须从积分式开始：

$$
X_t
=X_0+\int_0^t a(s,X_s)\,ds
+\int_0^t b(s,X_s)\,dW_s.
$$

第一项是 ordinary time integral；第二项需要新的积分理论。三件事必须同时说明：

| 问题 | 数学合同 | 省略后的风险 |
|---|---|---|
| integrand 何时可用哪些信息 | filtration 与 adapted/predictable | 偷看未来噪声 |
| 随机和按什么意义收敛 | 通常先在 $L^2(\Omega)$ | 把 pathwise 图像误当定义 |
| 取样点怎样选 | Itô 用左端点；Stratonovich 用对称极限 | drift 被悄悄改变 |

## 一、为什么普通路径积分路线会断裂

### 1.1 有限变差 integrator 的经典结论

如果 $g$ 是有限变差函数，Riemann–Stieltjes 和

$$
\sum_i f(\tau_i)\bigl(g(t_{i+1})-g(t_i)\bigr)
$$

在适当条件下对标签 $\tau_i\in[t_i,t_{i+1}]$ 的选择不敏感。直观原因是 integrator 的总变差可控制误差。

Brownian path 在任何非退化区间上 almost surely 具有无限 total variation。故不能直接套这条道路。

### 1.2 标签选择现在会留下有限差异

对 partition $\Pi=\{0=t_0<\cdots<t_n=T\}$，比较

$$
L_\Pi=\sum_i W_{t_i}\Delta_iW
$$

与梯形和

$$
S_\Pi=\sum_i\frac{W_{t_i}+W_{t_{i+1}}}{2}\Delta_iW.
$$

两者差为

$$
S_\Pi-L_\Pi
=\frac12\sum_i(\Delta_iW)^2.
$$

当 mesh 消失时，右侧趋于 $T/2$，不是0。因此：

$$
L_\Pi\longrightarrow \frac12(W_T^2-T),
$$

$$
S_\Pi=\frac12W_T^2
$$

对每个 partition 已经由 telescope 精确成立。左端点与对称点定义了不同积分。

> [!warning] 第一个关键边界
> “网格足够细，左端点/中点就没有区别”只适用于经典有限变差情形；Brownian quadratic variation 恰好把每步的微小差异累积成 $O(1)$。

## 二、概率空间与 integrand space

固定满足 usual conditions 的 filtered probability space

$$
(\Omega,\mathcal F,(\mathcal F_t)_{t\in[0,T]},\mathbb P),
$$

并令 $W$ 是相对于该 filtration 的 Brownian motion。最基本的平方可积 integrand 条件是

$$
\mathbb E\int_0^T |H_t|^2\,dt<\infty.
$$

此外 $H$ 必须具有与 filtration 兼容的可测性。严格理论常用 predictable；很多入门陈述用 progressively measurable。核心因果要求是：时刻 $t$ 的系数不能依赖尚未发生的 Brownian increment。

记

$$
\|H\|_{\mathcal H^2}^2
:=
\mathbb E\int_0^T|H_t|^2\,dt.
$$

这是 integrand 的自然 Hilbert-space 范数。

> [!note] Adapted 还不总是全部技术条件
> 仅对每个 $t$ 有 $H_t\in\mathcal F_t$，未必自动给联合可测性。对连续或 càdlàg adapted processes，所需可测性通常可安全获得；一般过程应明确 predictable/progressive 假设。

## 三、第一步：对 simple adapted process 定义积分

### 3.1 Simple process

给定 deterministic partition

$$
0=t_0<t_1<\cdots<t_n=T,
$$

令

$$
H_t
=\sum_{i=0}^{n-1}H_i\mathbf1_{(t_i,t_{i+1}]}(t),
$$

其中

$$
H_i\in\mathcal F_{t_i},
\qquad
\mathbb E[H_i^2]<\infty.
$$

$H_i$ 在 increment $\Delta_iW=W_{t_{i+1}}-W_{t_i}$ 开始前已经知道。

定义

$$
\int_0^T H_t\,dW_t
:=
\sum_{i=0}^{n-1}H_i
\bigl(W_{t_{i+1}}-W_{t_i}\bigr).
$$

若只积到 $t$，则

$$
\int_0^tH_s\,dW_s
=
\sum_i H_i
\left(
W_{t_{i+1}\wedge t}-W_{t_i\wedge t}
\right).
$$

### 3.2 为什么必须是左端信息

由于

$$
H_i\in\mathcal F_{t_i}
$$

而 $\Delta_iW$ 独立于 $\mathcal F_{t_i}$，有

$$
\mathbb E[H_i\Delta_iW\mid\mathcal F_{t_i}]
=H_i\mathbb E[\Delta_iW\mid\mathcal F_{t_i}]
=0.
$$

若改用 $H_i=\Delta_iW$，它依赖未来端点，便得到

$$
\mathbb E[H_i\Delta_iW]
=\mathbb E[(\Delta_iW)^2]
=\Delta_it,
$$

零均值结构立刻消失。这不是小技术差别，而是 stochastic causality。

## 四、Itô isometry：构造的核心支点

### 4.1 零均值

由上一节条件期望，

$$
\mathbb E\left[\int_0^T H_t\,dW_t\right]
=\sum_i\mathbb E[H_i\Delta_iW]
=0.
$$

### 4.2 对角项

考虑平方：

$$
\mathbb E\left[
\left(\sum_iH_i\Delta_iW\right)^2
\right].
$$

对角项满足

$$
\mathbb E[H_i^2(\Delta_iW)^2]
=
\mathbb E\left[
H_i^2
\mathbb E[(\Delta_iW)^2\mid\mathcal F_{t_i}]
\right]
=
\mathbb E[H_i^2]\Delta_it.
$$

### 4.3 交叉项为何为0

若 $i<j$，则 $H_i\Delta_iW H_j$ 在 $\mathcal F_{t_j}$ 可测，而 $\Delta_jW$ 与 $\mathcal F_{t_j}$ 独立且条件均值为0：

$$
\begin{aligned}
\mathbb E[H_i\Delta_iW H_j\Delta_jW]
&=
\mathbb E\left[
H_i\Delta_iW H_j
\mathbb E[\Delta_jW\mid\mathcal F_{t_j}]
\right]\\
&=0.
\end{aligned}
$$

因此所有交叉项消失。

### 4.4 等距公式

合并得到

$$
\boxed{
\mathbb E\left[
\left(\int_0^T H_t\,dW_t\right)^2
\right]
=
\mathbb E\int_0^T H_t^2\,dt
}.
$$

更一般地，由 polarization，

$$
\mathbb E\left[
\left(\int_0^T H_t\,dW_t\right)
\left(\int_0^T K_t\,dW_t\right)
\right]
=
\mathbb E\int_0^T H_tK_t\,dt.
$$

这就是 Itô isometry。它说明映射

$$
H\mapsto \int_0^T H_t\,dW_t
$$

从 integrand 的 $\mathcal H^2$ 空间到随机变量的 $L^2(\Omega)$ 是等距线性算子。

## 五、第二步：由完备性延拓到一般平方可积 integrand

设 $H\in\mathcal H^2$，取 simple predictable processes $H^{(n)}$ 使

$$
\|H^{(n)}-H\|_{\mathcal H^2}\to0.
$$

由 Itô isometry，

$$
\mathbb E\left|
\int_0^T H_t^{(n)}\,dW_t
-
\int_0^T H_t^{(m)}\,dW_t
\right|^2
=
\|H^{(n)}-H^{(m)}\|_{\mathcal H^2}^2.
$$

右侧趋于0，所以积分序列在 $L^2(\Omega)$ 中 Cauchy。因为 $L^2$ 完备，存在唯一极限。定义

$$
\int_0^T H_t\,dW_t
:=
L^2\text{-}\lim_{n\to\infty}
\int_0^T H_t^{(n)}\,dW_t.
$$

等距公式保证极限不依赖近似序列。

> [!important] 构造逻辑
> 不是先假定逐路径积分存在，再去求期望；而是先在 simple adapted class 上定义，利用 isometry 控制误差，再在 $L^2$ 中完成化。

### 5.1 得到的过程是 martingale

令

$$
M_t=\int_0^tH_s\,dW_s.
$$

在平方可积条件下，$M$ 是 continuous square-integrable martingale，并满足

$$
\mathbb E[M_t^2]
=\mathbb E\int_0^tH_s^2\,ds.
$$

其 quadratic variation 为

$$
[M]_t=\int_0^tH_s^2\,ds,
$$

而 predictable quadratic variation 也等于右侧。更一般 local martingale 情形需要 localization，本章不展开。

### 5.2 一个容易混淆的方差结论

若 $H$ 是 deterministic，

$$
\int_0^T H_t\,dW_t
\sim
\mathcal N\left(0,\int_0^T H_t^2\,dt\right).
$$

若 $H$ 随机且 adapted，积分通常不再是 Gaussian。Itô isometry只给二阶矩，不给完整分布。

## 六、第一条必须会算的随机积分

考虑左端点和

$$
L_\Pi=\sum_iW_{t_i}\Delta_iW.
$$

恒等式

$$
W_{t_{i+1}}^2-W_{t_i}^2
=2W_{t_i}\Delta_iW+(\Delta_iW)^2
$$

求和给出

$$
W_T^2
=2L_\Pi+\sum_i(\Delta_iW)^2.
$$

沿 deterministic partitions 令 mesh 趋于0，利用

$$
\sum_i(\Delta_iW)^2\to T
$$

可得

$$
\boxed{
\int_0^TW_t\,dW_t
=\frac12(W_T^2-T)
}.
$$

ordinary calculus 猜测的 $W_T^2/2$ 少了 $T/2$。这就是 Itô correction 最小原型。

作为一致性检查，

$$
\mathbb E\left[\int_0^TW_t\,dW_t\right]=0,
$$

而

$$
\mathbb E\left[\frac12W_T^2\right]=\frac T2\ne0.
$$

## 七、一维 Itô formula：从 Taylor 展开看见二阶项

### 7.1 先对 $f(W_t)$ 推导

设 $f\in C^2$。对每个 increment，

$$
\Delta f
=f'(W_{t_i})\Delta_iW
+\frac12f''(W_{t_i})(\Delta_iW)^2
+R_i.
$$

求和后：

1. 一阶项趋于 $\int_0^T f'(W_t)\,dW_t$；
2. 二阶项因 quadratic variation 趋于
   $$
   \frac12\int_0^Tf''(W_t)\,dt;
   $$
3. 余项在适当正则性与 localization 下消失。

因此

$$
f(W_T)-f(W_0)
=
\int_0^Tf'(W_t)\,dW_t
+\frac12\int_0^Tf''(W_t)\,dt.
$$

微分记号是

$$
df(W_t)
=f'(W_t)\,dW_t+\frac12f''(W_t)\,dt.
$$

### 7.2 加上时间变量

若 $f\in C^{1,2}([0,T]\times\mathbb R)$，则

$$
\boxed{
df(t,W_t)
=
\left(f_t+\frac12f_{xx}\right)(t,W_t)\,dt
+f_x(t,W_t)\,dW_t
}.
$$

$C^{1,2}$ 表示对时间一阶、对空间二阶连续可微。时间 increment 是 $O(dt)$，Brownian increment 是 $O_{\mathbb P}(\sqrt{dt})$；所以空间二阶项与时间一阶项同阶。

## 八、一般一维 Itô process 的公式

若

$$
dX_t=a_t\,dt+b_t\,dW_t,
$$

则尺度账本给出

$$
(dX_t)^2
=a_t^2(dt)^2+2a_tb_t\,dt\,dW_t+b_t^2(dW_t)^2
=b_t^2\,dt.
$$

这不是逐点代数，而是 quadratic/cross variation 的速记。于是

$$
\boxed{
df(t,X_t)
=
\left(
f_t+a_tf_x+\frac12b_t^2f_{xx}
\right)(t,X_t)\,dt
+
b_tf_x(t,X_t)\,dW_t
}.
$$

积分形式为

$$
\begin{aligned}
f(t,X_t)-f(0,X_0)
&=
\int_0^t
\left(
f_s+a_sf_x+\frac12b_s^2f_{xx}
\right)(s,X_s)\,ds\\
&\quad+
\int_0^t b_sf_x(s,X_s)\,dW_s.
\end{aligned}
$$

### 8.1 Product rule

对 continuous Itô processes $X,Y$，

$$
d(X_tY_t)
=X_t\,dY_t+Y_t\,dX_t+d[X,Y]_t.
$$

最后一项是 ordinary product rule 没有的部分。若

$$
dX=a_Xdt+b_XdW,\qquad dY=a_Ydt+b_YdW,
$$

则

$$
d[X,Y]_t=b_Xb_Y\,dt.
$$

### 8.2 例：指数 martingale

取

$$
Z_t=\exp\left(\theta W_t-\frac12\theta^2t\right).
$$

Itô formula 给

$$
dZ_t=\theta Z_t\,dW_t.
$$

在适当可积条件下它是 martingale，且 $\mathbb E[Z_t]=1$。减去的 $\theta^2t/2$ 正是 quadratic-variation correction。

## 九、多维 Itô formula：矩阵形状必须清楚

令

$$
X_t\in\mathbb R^d,\qquad W_t\in\mathbb R^m,
$$

并设

$$
dX_t=a(t,X_t)\,dt+B(t,X_t)\,dW_t,
$$

其中

$$
a\in\mathbb R^d,\qquad B\in\mathbb R^{d\times m}.
$$

局部 covariance rate 是

$$
\operatorname{Cov}(dX_t\mid\mathcal F_t)
=B B^\top\,dt.
$$

对 scalar $f:[0,T]\times\mathbb R^d\to\mathbb R$，

$$
\boxed{
df(t,X_t)
=
\left[
\partial_tf
+a^\top\nabla f
+\frac12
\operatorname{tr}
\left(
BB^\top\nabla_x^2f
\right)
\right]dt
+
(\nabla f)^\top B\,dW_t
}.
$$

坐标形式的二阶项是

$$
\frac12
\sum_{i=1}^d\sum_{k=1}^d
(BB^\top)_{ik}\,
\partial_{x_i x_k}f.
$$

若 Brownian components 相关，必须先把 covariance rate 写清；不能继续机械使用 $dW^jdW^k=\delta_{jk}dt$。

> [!tip] 形状检查
> $\nabla f$ 视为 $d\times1$ 列向量，$B$ 是 $d\times m$，所以 $(\nabla f)^\top B$ 是 $1\times m$，恰好乘 $m\times1$ 的 $dW$。

## 十、SDE 是积分方程，不是符号字符串

考虑

$$
dX_t=a(t,X_t)\,dt+B(t,X_t)\,dW_t,
\qquad
X_0=\xi.
$$

完整声明至少包括：

1. 时间区间与状态/噪声维数；
2. filtered probability space；
3. $m$ 维 Brownian motion；
4. 初值 $\xi$ 的分布及其与噪声的关系；
5. coefficient 的可测性、正则性和增长条件；
6. Itô 或 Stratonovich 解释；
7. solution concept；
8. 是否要求 global/non-explosive；
9. 比较数值解时的 coupling 与误差指标。

积分方程是

$$
X_t
=\xi
+\int_0^t a(s,X_s)\,ds
+\int_0^t B(s,X_s)\,dW_s.
$$

一个解必须 adapted，积分必须存在，且等式通常要求对所有 $t$ 在一个概率1事件上成立。

## 十一、Strong/weak solution 与两种 uniqueness

### 11.1 Strong solution

概率空间、filtration、Brownian motion $W$ 与初值 $\xi$ 预先给定。若能在这些对象上构造 adapted $X$ 满足积分方程，则称 strong solution。

这里 strong 描述“解相对于给定噪声的构造关系”，不等于数值分析中的 strong convergence。

### 11.2 Weak solution

允许概率空间、filtration、Brownian motion 与 $X$ 一起作为解的一部分来构造，只要求它们的 joint law 满足 SDE。

这里 weak 也不是“近似”或“结论较差”；它是较宽的存在概念。

### 11.3 Pathwise uniqueness

在同一概率空间上，用同一个 Brownian motion 和同一个初值驱动两个解 $X,Y$。若

$$
\mathbb P(X_t=Y_t\ \forall t\in[0,T])=1,
$$

则称 pathwise uniqueness。

### 11.4 Uniqueness in law

任意两个 weak solutions 的 $X$ 过程具有相同 law。它不要求把两者放到同一噪声实现上逐路径相等。

| 术语 | 固定什么 | 比较什么 |
|---|---|---|
| strong solution | 给定空间与 Brownian noise | 是否能构造 adapted path |
| weak solution | 可更换空间与 noise | 是否存在某个 joint construction |
| pathwise uniqueness | 同一初值、同一 Brownian path | 两条 solution path |
| uniqueness in law | 可不同 construction | solution process 的 law |
| strong numerical error | 同一 underlying noise | exact/approximate path |
| weak numerical error | 不要求逐路径配对 | test-function expectation |

Yamada–Watanabe 理论连接 weak existence、pathwise uniqueness 与 strong existence，但这是正式随机分析定理，不能仅靠词义推出。

## 十二、全局适定性：为什么 Lipschitz 与 growth 条件出现

考虑 $a:[0,T]\times\mathbb R^d\to\mathbb R^d$ 与
$B:[0,T]\times\mathbb R^d\to\mathbb R^{d\times m}$。一个标准充分条件是存在 $L,K$ 使对所有 $t,x,y$：

$$
\|a(t,x)-a(t,y)\|
+\|B(t,x)-B(t,y)\|_F
\le L\|x-y\|,
$$

$$
\|a(t,x)\|^2+\|B(t,x)\|_F^2
\le K(1+\|x\|^2),
$$

并且 $\mathbb E\|\xi\|^2<\infty$。

则 SDE 存在唯一 non-explosive strong solution，且

$$
\mathbb E\sup_{0\le t\le T}\|X_t\|^2<\infty.
$$

### 12.1 Picard iteration 的随机版本

定义

$$
X_t^{(0)}=\xi,
$$

$$
X_t^{(n+1)}
=
\xi+\int_0^t a(s,X_s^{(n)})\,ds
+\int_0^t B(s,X_s^{(n)})\,dW_s.
$$

对相邻差，ordinary integral 用 Cauchy–Schwarz，stochastic integral 用 Doob/BDG inequality 与 Itô isometry，Lipschitz 条件把 coefficient 差控制为 path 差。短时间上得到 contraction 型估计，随后分段覆盖 $[0,T]$。

### 12.2 Uniqueness 的核心估计

若 $X,Y$ 同噪声同初值，则

$$
X_t-Y_t
=
\int_0^t(a(s,X_s)-a(s,Y_s))\,ds
+\int_0^t(B(s,X_s)-B(s,Y_s))\,dW_s.
$$

平方、取 supremum 和 expectation，再用 Lipschitz 与 BDG，可得到

$$
\mathbb E\sup_{u\le t}\|X_u-Y_u\|^2
\le
C\int_0^t
\mathbb E\sup_{r\le s}\|X_r-Y_r\|^2\,ds.
$$

Gronwall 推出左侧为0。

### 12.3 条件不是必要条件

- local Lipschitz 通常只保证 explosion time 之前的 pathwise uniqueness；
- linear growth 常用于排除 finite-time explosion；
- 有些 non-Lipschitz diffusion 仍有唯一强解；
- neural network coefficient 的局部 Lipschitz 不自动给 global growth；
- ReLU 网络可 Lipschitz，但未约束权重时常数可能很大；
- superlinear drift 下 plain Euler–Maruyama 甚至可能在 moments 上发散。

## 十三、三个经典模型

### 13.1 Arithmetic Brownian motion

$$
dX_t=\mu\,dt+\sigma\,dW_t,
\qquad X_0=x_0.
$$

直接积分：

$$
X_t=x_0+\mu t+\sigma W_t.
$$

因此

$$
X_t\sim\mathcal N(x_0+\mu t,\sigma^2t).
$$

### 13.2 Geometric Brownian motion

$$
dX_t=\mu X_t\,dt+\sigma X_t\,dW_t,
\qquad X_0>0.
$$

对 $f(x)=\log x$ 用 Itô formula：

$$
d\log X_t
=
\left(\mu-\frac12\sigma^2\right)dt+\sigma\,dW_t.
$$

所以

$$
\boxed{
X_t
=
X_0\exp\left[
\left(\mu-\frac12\sigma^2\right)t+\sigma W_t
\right]
}.
$$

它 almost surely 保持正值，且

$$
\mathbb E[X_t]=X_0e^{\mu t},
$$

$$
\operatorname{Var}(X_t)
=
X_0^2e^{2\mu t}
\left(e^{\sigma^2t}-1\right).
$$

若忘记 $-\sigma^2t/2$，均值会错误地多出 $e^{\sigma^2t/2}$。

### 13.3 Ornstein–Uhlenbeck process

$$
dX_t=\kappa(m-X_t)\,dt+\sigma\,dW_t,
\qquad\kappa>0.
$$

乘 integrating factor $e^{\kappa t}$：

$$
d(e^{\kappa t}X_t)
=
\kappa m e^{\kappa t}dt
+\sigma e^{\kappa t}dW_t.
$$

积分得

$$
X_t
=m+(X_0-m)e^{-\kappa t}
+\sigma\int_0^te^{-\kappa(t-s)}\,dW_s.
$$

若 $X_0$ deterministic，则

$$
\mathbb E[X_t]
=m+(X_0-m)e^{-\kappa t},
$$

$$
\operatorname{Var}(X_t)
=
\frac{\sigma^2}{2\kappa}
\left(1-e^{-2\kappa t}\right).
$$

长期极限是

$$
\mathcal N\left(m,\frac{\sigma^2}{2\kappa}\right).
$$

> [!warning] Positivity 不是 Euler 自动保留的
> GBM exact solution 始终为正，但 Euler–Maruyama factor
> $$
> 1+\mu h+\sigma\Delta W
> $$
> 有正概率为负。exact model property 与 discrete solver property 必须分开。

## 十四、Generator：通向 law evolution 的接口

对 time-homogeneous SDE

$$
dX_t=a(X_t)\,dt+B(X_t)\,dW_t,
$$

定义作用在光滑 test function 上的 infinitesimal generator：

$$
\boxed{
\mathcal Lf(x)
=a(x)^\top\nabla f(x)
+\frac12\operatorname{tr}
\left(
B(x)B(x)^\top\nabla^2f(x)
\right)
}.
$$

Itô formula 可写成

$$
df(X_t)
=\mathcal Lf(X_t)\,dt
+\nabla f(X_t)^\top B(X_t)\,dW_t.
$$

取 expectation，若 stochastic integral 的期望为0，则

$$
\mathbb E[f(X_t)]-\mathbb E[f(X_0)]
=
\mathbb E\int_0^t\mathcal Lf(X_s)\,ds.
$$

这就是 Dynkin formula 的基本形态。它研究 test-function expectation；DYN-11 会把 $\mathcal L$ 转移到 density 上得到 $\mathcal L^\ast$ 与 Fokker–Planck 方程。

## 十五、Itô 与 Stratonovich

### 15.1 两种离散极限

Itô integral 使用 non-anticipating left endpoint：

$$
\int_0^TH_t\,dW_t
=
\lim\sum_iH_{t_i}\Delta_iW.
$$

Stratonovich integral 用对称极限，记作

$$
\int_0^TH_t\circ dW_t
\approx
\lim\sum_i\frac{H_{t_i}+H_{t_{i+1}}}{2}\Delta_iW.
$$

对 continuous semimartingales，

$$
\int_0^TH_t\circ dW_t
=
\int_0^TH_t\,dW_t+\frac12[H,W]_T.
$$

Stratonovich calculus 保留 ordinary chain rule；代价是 drift 与 Itô 形式不同。

### 15.2 一维 drift conversion

Stratonovich SDE

$$
dX_t=a_S(X_t)\,dt+b(X_t)\circ dW_t
$$

等价的 Itô SDE 是

$$
\boxed{
dX_t
=
\left[
a_S(X_t)+\frac12b(X_t)b'(X_t)
\right]dt
+b(X_t)\,dW_t
}.
$$

反向转换为

$$
a_S=a_I-\frac12bb'.
$$

例如

$$
dX_t=\sigma X_t\circ dW_t
$$

的解是 $X_t=X_0e^{\sigma W_t}$。其 Itô 形式是

$$
dX_t=\frac12\sigma^2X_t\,dt+\sigma X_t\,dW_t.
$$

而

$$
dX_t=\sigma X_t\,dW_t
$$

的 Itô 解是 $X_0e^{\sigma W_t-\sigma^2t/2}$。同样的表面 noise term、不同解释，得到不同 law。

### 15.3 多维 conversion

令 $B_{\cdot j}$ 是 $B$ 的第 $j$ 个 noise vector field。坐标形式为

$$
a_I^i
=
a_S^i
+\frac12
\sum_{j=1}^m\sum_{k=1}^d
B_{kj}\,\partial_{x_k}B_{ij}.
$$

不能把它简化成不带 indices 的“$BB'/2$”后随意广播。

## 十六、Euler–Maruyama：最小可计算离散化

令均匀网格 $t_n=nh$，$\Delta W_n=W_{t_{n+1}}-W_{t_n}$。冻结左端点 coefficient：

$$
\boxed{
X_{n+1}
=
X_n+a(t_n,X_n)h
+B(t_n,X_n)\Delta W_n
},
$$

其中

$$
\Delta W_n\sim\mathcal N(0,hI_m)
$$

且不重叠 increments 独立。

这叫 Euler–Maruyama，不是 ordinary Euler 加一个方差固定的噪声。

### 16.1 Strong error

给 exact solution 与 approximation 同一个 Brownian path，典型终点指标是

$$
\left(
\mathbb E\|X_T-X_N\|^p
\right)^{1/p}.
$$

若它是 $O(h^q)$，称 strong order $q$。在标准 global Lipschitz 与足够矩条件下，Euler–Maruyama 一般有 strong order $1/2$。

它回答 pathwise functionals、trajectory tracking、coupled multilevel estimator 等问题。

### 16.2 Weak error

对一类 test functions $\varphi$，研究

$$
\left|
\mathbb E[\varphi(X_T)]
-
\mathbb E[\varphi(X_N)]
\right|.
$$

若是 $O(h^q)$，称 weak order $q$。足够光滑与增长条件下，Euler–Maruyama 常有 weak order1。

Weak convergence 不保证同一 Brownian path 上两条轨迹接近；strong convergence 通常可推出适当 Lipschitz test function 的 weak bound，但两种最优 order 不必相同。

### 16.3 Coupling 是 strong experiment 的一部分

跨步长比较时，先采 finest increments，再求和构成 coarse increments：

$$
\Delta W^{\text{coarse}}_j
=
\sum_{k\in\text{block }j}
\Delta W^{\text{fine}}_k.
$$

若每个 $h$ 独立重抽噪声，则测到的是两条不同随机路径的差，不能估计 strong discretization error。

## 十七、Milstein 与 stochastic Taylor

对 scalar autonomous Itô SDE

$$
dX_t=a(X_t)\,dt+b(X_t)\,dW_t,
$$

Milstein 更新为

$$
\boxed{
X_{n+1}
=X_n+a(X_n)h+b(X_n)\Delta W_n
+\frac12b(X_n)b'(X_n)
\left[
(\Delta W_n)^2-h
\right]
}.
$$

额外项正是下一阶 stochastic Taylor term。在标准光滑条件下，scalar Milstein 可达 strong order1。

若 $b$ 为常数，$b'=0$，Milstein 与 EM 公式重合；additive-noise 问题可能因此获得更高 strong order。

### 17.1 多维不是逐坐标照抄

多维 non-commutative noise 的高阶 scheme 会出现 iterated stochastic integrals 与 Lévy area。只有在 scalar noise、commutative vector fields 等特殊结构下才可简化。把 scalar Milstein correction 对每个矩阵元素广播，通常不是合法方法。

### 17.2 数值 theorem 的条件不可删除

- discontinuous/non-Lipschitz coefficient；
- superlinear growth；
- degenerate diffusion；
- boundary-hitting 与 positivity；
- rare event、stopping time、path maximum；
- adaptive step 对 Brownian path 的条件采样；
- low precision 与 PRNG stream；

都可能让标准 strong/weak order statement失效或不足。

## 十八、事件、边界与 adaptive solver

### 18.1 Endpoint 正确不等于 path functional 正确

两个 solver 可能有接近的 $X_T$ distribution，却对

$$
\tau=\inf\{t:X_t\ge c\},
\qquad
\sup_{s\le T}X_s
$$

产生明显不同误差。网格间 crossing 需要 Brownian bridge 或专门事件处理。

### 18.2 Adaptive refinement 必须保持 Brownian 一致性

若把区间 $[t,t+h]$ 拆成两半，两个子 increment 不能独立于原 coarse increment 重新采样；它们必须满足

$$
\Delta W_1+\Delta W_2=\Delta W.
$$

条件分布可由 Brownian bridge 构造。Brownian tree/virtual Brownian tree 让不同求值顺序共享同一 underlying path。

### 18.3 Stiffness 没有因随机项消失

drift stiff、diffusion multiplicative 或多尺度噪声时，显式 EM 可能受 stability 限制。strong stability、mean-square stability、A-stability 的 SDE 版本需要专门理论；不能照搬 deterministic RK order/stability chart。

## 十九、Neural SDE：模型、solver 与训练是三个对象

令

$$
dX_t=f_\theta(t,X_t)\,dt
+G_\theta(t,X_t)\,dW_t.
$$

参数化 drift/diffusion 只是 model class。实际训练还包含：

1. 初值/latent distribution；
2. observation model；
3. Brownian realization 与 batch stream；
4. numerical solver；
5. discrete loss $J_h(\theta)$；
6. gradient estimator；
7. model error、Monte Carlo error 与 discretization error。

### 19.1 Discretize-then-optimize

对 EM：

$$
X_{n+1}
=
X_n+f_\theta(t_n,X_n)h
+G_\theta(t_n,X_n)\Delta W_n.
$$

直接反向传播得到

$$
\nabla_\theta J_h,
$$

即离散程序的精确梯度，忽略 floating-point/AD 实现误差。有限差分同一个 $J_h$ 可以验收它。

但

$$
\nabla_\theta J_h
\ne
\nabla_\theta J
$$

在有限 $h$ 时一般成立。前者通过 finite difference 不代表 continuous objective gradient 已正确。

### 19.2 Pathwise sensitivity

对参数 $\theta$，若正则性允许，可对同一 Brownian realization 微分。以 scalar EM 为例：

$$
S_n=\frac{\partial X_n}{\partial\theta},
$$

$$
\begin{aligned}
S_{n+1}
&=
S_n
+\left(
\partial_xf_\theta S_n+\partial_\theta f_\theta
\right)h\\
&\quad+
\left(
\partial_xG_\theta S_n+\partial_\theta G_\theta
\right)\Delta W_n.
\end{aligned}
$$

这是 forward sensitivity，也是自动微分应复现的递推。

### 19.3 Continuous adjoint 不是自动免费

SDE 向后灵敏度牵涉 stochastic integral interpretation、reverse-time noise、trajectory reconstruction 和 numerical convergence。Li 等人的 stochastic adjoint 构造明确使用相应理论条件；它不是把 ODE adjoint 的 $dt$ 换成 $dW$ 就完成。

Kidger 等人的 neural SDE 将 Brownian input、numerical solution path 与 path discriminator组合成连续时间生成模型。其生成对象是 path distribution；只比较终点 histogram 会丢失核心结构。

## 二十、扩散模型接口：本章能说什么、暂时不能说什么

Forward diffusion 常写作

$$
dX_t=f(t,X_t)\,dt+g(t)\,dW_t.
$$

本章已经能检查：

1. $g(t)$ 的单位与 $\sqrt{dt}$ scaling；
2. coefficient 是否 adapted；
3. Itô interpretation；
4. finite-step sampler 是 EM、Milstein 还是其他方法；
5. solver strong/weak target；
6. 同一 Brownian path 的 refinement；
7. fixed-time marginal sampler 与 full process 的区别。

但本章还不能仅凭公式推出：

- marginal density 的 PDE；
- reverse-time drift；
- probability-flow ODE；
- learned score 误差怎样进入 sampler；
- reverse solver 是否产生数据分布。

这些分别属于 DYN-11 与 DYN-12。

## 二十一、实验结果：三个对象必须分开验收

配套实验 [[实验 - Itô 和、SDE 强弱误差与离散梯度审计]] 使用标准库、固定 seed 与 nested Brownian increments。

先用下图回答一个实验问题：**左端点 Itô 和、EM 的 strong/weak error 与离散梯度误差，是否分别呈现理论预期的收敛和对象差异？**

![[00-知识库管理/_assets/plots/dynamics/plot-ito-sde-numerics-gradient-v2.svg|880]]

> [!figure] 图 10.9.10b｜Itô 和、GBM strong/weak error 与离散梯度审计
> A 在 nested Brownian grids 上报告 left-sum Itô target RMSE 的 observed order $0.503$，并检查 midpoint–left correction 向 $1/2$ 收敛；B 对同一路径的 GBM exact terminal 与 Euler–Maruyama 给出 strong order $0.510$，同时以 expectation bias 给出 weak order $0.993$；C 比较 pathwise discrete-gradient gap（order $0.604$）与同一离散目标的 tangent–finite-difference 一致性。参数：seed `20260819`，6000 paths，$N_{\max}=512$，$\mu=0.35,\sigma=0.8$。来源：确定性模拟；数据与原断言：[[ito_sde_numerics_gradient_audit.py]]；v2 绘图脚本：[[plot_stochastic_experiments_v2.py]]。

**怎样读图。** 三栏横轴都从 fine 到 coarse $h$，纵轴为 log error，线的斜率对应 observed order。A 先验证积分 convention 的二次变差 correction；B 强误差必须逐路径耦合 exact/EM，weak bias 只比较期望；C 蓝线只证明 analytic tangent 与 finite difference 在同一 $J_h$ 上一致，红线才追踪 $J_h$ 向 continuous target 的 gap。

**适用边界（图没有证明什么）。** 这是一个 scalar GBM、固定 horizon、有限 Monte Carlo 样本的受控实验，不证明所有 SDE/solver 具有相同 order。Observed slope 受 pre-asymptotic range、sampling error 和 floating-point floor 影响。Finite difference agreement 不能证明 continuous gradient 正确；nested increments 也是 strong-error 可比性的实验设计条件。

### 21.1 Itô/Stratonovich 轨

对同一 Brownian path 比较

$$
L_N=\sum_iW_{t_i}\Delta_iW,
$$

$$
S_N=\sum_i\frac{W_{t_i}+W_{t_{i+1}}}{2}\Delta_iW.
$$

左端点对 Itô target 的 RMSE observed order 为

$$
0.50290522,
$$

而 $S_N=W_T^2/2$ 在 floating-point 中达到 machine identity；finest-grid 的平均 correction 为

$$
0.49931847.
$$

### 21.2 GBM strong/weak 轨

对

$$
dX_t=0.35X_t\,dt+0.8X_t\,dW_t
$$

使用同一 Brownian path 比较 EM 与 exact terminal。observed strong order 为

$$
0.50979058.
$$

弱均值 bias 使用解析式

$$
\left|
X_0(1+\mu h)^{T/h}
-
X_0e^{\mu T}
\right|,
$$

observed order 为

$$
0.99318241.
$$

同一个 method 对两个不同误差对象出现不同阶，正是 strong/weak 分工。

### 21.3 离散梯度轨

对 terminal squared loss 和 $\sigma$ sensitivity，递推梯度与 centered finite difference 的最大误差为

$$
5.50336221\times10^{-10}.
$$

这验证 $\nabla_\sigma J_h$。与此同时，pathwise gradient integrand 与 exact continuous counterpart 的 RMSE 仍按约

$$
h^{0.60363071}
$$

消失。两道门不可合并。

## 二十二、SDE 与神经随机动力学审计卡

~~~text
EQUATION
  state dimension d / noise dimension m
  Ito or Stratonovich
  drift a(t,x), diffusion B(t,x)
  units: a ~ state/time; B ~ state/sqrt(time)
  initial law and independence

INFORMATION
  probability space and filtration
  adapted / predictable coefficient
  no future Brownian increments
  Brownian component covariance

SOLUTION
  strong or weak solution
  pathwise uniqueness or uniqueness in law
  local/global existence and explosion policy
  moment and boundary properties

NUMERICS
  increment covariance h I
  EM / Milstein / specialized solver
  nested increments or Brownian tree
  strong / weak / event target
  bridge correction and adaptive-step contract
  dtype, seed, stream, tolerance, NFE

GRADIENT
  continuous objective J or discrete J_h
  tangent / backprop / stochastic adjoint
  same random numbers for comparisons
  finite difference validates which objective
  discretization and Monte Carlo error bars

AI CLAIM
  model process vs computed process
  endpoint marginal vs path law
  learned coefficient/score vs population object
  solver error vs statistical approximation error
~~~

## 二十三、常见错误与最短修正

| 错误 | 为什么错 | 最短修正 |
|---|---|---|
| $dW/dt$ 当普通 Gaussian function | Brownian 不可微 | 回到 Itô integral |
| 噪声每步乘 $h$ | variance 变成 $O(h^2)$ | 使用 $\sqrt h\,Z$ |
| 左端点、中点随意替换 | QV 留下 $O(1)$ correction | 声明 Itô/Stratonovich |
| $\int H\,dW$ 一律 Gaussian | 随机 integrand 可产生非 Gaussian law | isometry只承诺二阶矩 |
| strong solution 等于 strong error | 一个是解概念，一个是数值收敛 | 分开定义 |
| 同 seed 就是同 Brownian path | 不同分辨率耗用 stream 次序可不同 | finest increments/Brownian tree |
| EM 终点 histogram 正确就验收完成 | path event 与 coupling 未验收 | 增加 strong/path diagnostics |
| scalar Milstein 广播到矩阵 noise | 缺 iterated integral/Lévy area | 检查 commutativity |
| AD 通过 FD 就等于连续梯度正确 | 二者可能都只针对 $J_h$ | 再做 $h\to0$ gap |
| neural drift/diffusion 可训练就适定 | 可能不满足 growth/nonexplosion | 加结构约束与证书 |

## 二十四、最小掌握检查

### 概念

1. 为什么 simple integrand 的 coefficient 必须在 increment 开始前可测？
2. Itô isometry 是定义、定理还是延拓工具？
3. 随机 integrand 的 Itô integral 为什么未必 Gaussian？
4. $dW^2=dt$ 应按什么极限理解？
5. strong solution、pathwise uniqueness、strong numerical convergence 分别比较什么？
6. Itô 与 Stratonovich 的差为什么体现在 drift？
7. weak order1 是否意味着 sample paths 一阶接近？

### 闭卷推导

在不看正文时重建：

$$
\mathbb E\left(\int_0^TH_t\,dW_t\right)^2
=
\mathbb E\int_0^TH_t^2dt,
$$

$$
\int_0^TW_t\,dW_t
=\frac12(W_T^2-T),
$$

$$
df(t,X_t)
=
\left(f_t+af_x+\frac12b^2f_{xx}\right)dt
+bf_xdW_t,
$$

$$
X_t^{\mathrm{GBM}}
=
X_0e^{(\mu-\sigma^2/2)t+\sigma W_t},
$$

以及 scalar Milstein correction。

### 数值/研究检查

1. 用 nested increments 重现实验的 strong order；
2. 分别定义 endpoint strong RMSE 与 test-function weak bias；
3. 比较 left/trapezoid sums 并观察 $T/2$ correction；
4. 对 GBM 检查 positivity failure 与 moment bias；
5. 用 finite difference 验收同一 discrete loss；
6. 改变 $h$ 检查 discrete/continuous gradient gap；
7. 对 adaptive refinement 写出 Brownian bridge consistency。

## 二十五、学习闭环与后继接口

- 分层题：[[习题 - Itô 引理与随机微分方程]]；
- 独立详解：[[解答 - Itô 引理与随机微分方程]]；
- 复现实验：[[实验 - Itô 和、SDE 强弱误差与离散梯度审计]]；
- 下一章：[[Fokker-Planck 方程与概率流 ODE]]从 generator/Dynkin 接口推导 density evolution，并解释何时 stochastic process 与 deterministic probability flow 共享 marginals；
- 再下一章：[[时间反演、score 与扩散生成动力学]]处理 reverse-time drift、score estimation 与 finite-step generative sampler。

> [!check] 当前状态
> 正文、机制图、15道 A—E 题、逐题详解和三轨实验均为 composed；尚无学习者首次闭卷答案、独立改参复现与间隔复测，因此保持 draft，不记为 mastered。

## 二十六、来源分工与科学空间入口

- [MIT 15.070J, Itô integral for simple processes](https://ocw.mit.edu/courses/15-070j-advanced-stochastic-processes-fall-2013/resources/mit15_070jf13_lec15/)：simple adapted processes、Itô isometry 与 $L^2$ 构造；
- [MIT 18.S096, Itô Calculus](https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/resources/mit18_s096f13_lecnote18/)：Itô formula、经典例子与 SDE 入门；
- [Øksendal, Stochastic Differential Equations](https://link.springer.com/book/10.1007/978-3-642-14394-6)：Itô integral/formula、SDE existence、generator 与应用的正式教材；
- [Kloeden–Platen, Numerical Solution of Stochastic Differential Equations](https://link.springer.com/book/10.1007/978-3-662-12616-5)：stochastic Taylor、strong/weak approximation 与数值方法；
- [Li et al., Scalable Gradients for Stochastic Differential Equations](https://proceedings.mlr.press/v108/li20i.html)：stochastic adjoint、noise reconstruction 与 neural SDE gradient；
- [Kidger et al., Neural SDEs as Infinite-Dimensional GANs](https://proceedings.mlr.press/v139/kidger21b.html)：path-distribution generative modeling 与 neural SDE；
- [Song et al., Score-Based Generative Modeling through SDEs](https://arxiv.org/abs/2011.13456)：连续扩散生成的 SDE 主线；
- [[S-2016-Su-3762-随机微分方程]]：非线性 SDE、离散解释与路径积分问题入口；
- [[S-2022-Su-9209-扩散模型SDE篇]]：扩散模型的连续 SDE 与离散采样中文入口。

正式定义、适定性和数值收敛由课程、教材与原论文承担；科学空间负责中文问题意识与扩散建模接口。本章自行补齐 adaptedness、isometry proof、solution taxonomy、强弱误差、nested Brownian coupling 与离散梯度审计，不用形式路径积分替代 Itô theorem。
