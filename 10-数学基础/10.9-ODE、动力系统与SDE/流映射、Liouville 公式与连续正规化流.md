---
type: concept
status: draft
area: [math/ode, math/dynamical-systems, math/probability, ai/generative-modeling, ai/neural-ode]
aliases: [ODE 流, flow map, Liouville formula, instantaneous change of variables, continuous normalizing flow, CNF, FFJORD]
prerequisites: ["[[常微分方程、初值问题与解的存在唯一性]]", "[[线性 ODE 与矩阵指数]]", "[[Euler、Runge-Kutta 与离散化误差]]", "[[随机变量变换与密度换元]]", "[[迹、行列式与体积]]", "[[Jacobian、JVP 与 VJP]]"]
related: ["[[ODE、动力系统与 SDE MOC]]", "[[连续性方程与守恒律]]", "[[刚性系统、绝对稳定域与隐式方法]]", "[[逆矩阵、线性求解与隐式微分]]", "[[实验 - 流映射、Liouville 与随机迹审计]]"]
sources: ["Teschl-ODE-Dynamical-Systems", "Chen-et-al-2018-Neural-ODE", "Grathwohl-et-al-2019-FFJORD", "Hutchinson-1989-Trace-Estimator", "Dupont-et-al-2019-Augmented-Neural-ODE", "Rezende-Mohamed-2015-Normalizing-Flows", "Su-5776-NICE", "Su-9280-Diffusion-ODE", "Su-10958-Instant-Average-Velocity"]
created: 2026-08-19
updated: 2026-08-27
---

# 流映射、Liouville 公式与连续正规化流

> [!abstract] 本章主问题
> 在唯一解且对初值可微的条件下，ODE 不只产生一条轨迹，还在不同时间切片之间产生流映射 $\phi_{s,t}$。它的 Jacobian $J_{s,t}$ 满足变分方程，行列式满足 Liouville 公式
> $$
> \det J_{s,t}(x_s)
> =\exp\!\left(\int_s^t \operatorname{div}f(\tau,x_\tau)\,d\tau\right)>0.
> $$
> 概率质量守恒于是迫使沿轨迹的 log-density 满足
> $$
> \frac{d}{dt}\log p_t(x_t)=-\operatorname{div}f(t,x_t).
> $$
> Continuous normalizing flow（CNF）正是把状态与这条 log-density ODE 一起积分。公式本身是精确流的结论；有限步求解、随机 trace 估计和训练梯度仍有各自的误差与条件。

> [!important] 与相邻章节的分工
> DYN-01 已建立 existence、uniqueness、maximal solution 与 blow-up；DYN-05—06 已建立 finite-step solver、误差、刚性和梯度对象。本章从“每个初值有唯一轨迹”升级到“所有初值组成可微映射”，再建立体积与密度公式。[[连续性方程与守恒律]]将从欧拉坐标完整推导 $\partial_t p+\nabla\cdot(pf)=0$、弱形式与 characteristics；本章只使用它的沿轨迹结果，不提前替代 PDE 主章。

先用下图回答一个视觉问题：**唯一可微流怎样搬运整片状态，Jacobian 体积变化如何化为 divergence，而 CNF 需要同时积分和验收哪些量？**

![[00-知识库管理/_assets/figures/dynamics/fig-flow-liouville-cnf-v2.svg|880]]

> [!figure] 图 10.9.7｜Flow map、Liouville 体积公式与 CNF 增广 ODE
> A 将同一时间切片上的多点经 $\phi_{s,t}$ 一致搬运，列出 identity、composition、no-crossing/injectivity 与 backward-completeness 的满射边界；B 从变分方程 $\dot J=(D_xf)J$ 经 Jacobi formula 得到 $d\log\det J/dt=\operatorname{tr}(D_xf)=\nabla\cdot f$ 与正 determinant；C 同时积分 $\dot x=f_\theta$ 和 $d\log p_t(x_t)/dt=-\nabla\cdot f_\theta$，并把 exact/Hutchinson trace、solver 与 likelihood/gradient 列为独立账。来源：独立绘制；理论接口参考 differentiable flows、Liouville formula、instantaneous change of variables 与 Hutchinson trace estimator；生成脚本：[[plot_dynamics_numerics_transport_v2.py]]；确定性结构示意，无随机种子。

**怎样读图。** A 先把“一个数组轨迹”升级为“共同时间区间上的映射族”，uniqueness 给局部 no-crossing，但全空间 inverse 还要 backward completeness；B 再对初值求导，沿变分方程追踪 infinitesimal shape，用 trace 只压缩 volume change；C 最后把 state 与 log-density 组成 augmented ODE，明确 trace estimator 的 probe、JVP/VJP、reuse/stop-gradient 和 ODE tolerance。

**适用边界（图没有证明什么）。** Injectivity 不自动给整个 $\mathbb R^d$ 上 surjectivity；$\det J>0$ 也不等于无 shape distortion 或轨迹稳定。CNF 公式针对 exact differentiable flow，有限步 map 可能不保 exact inverse/likelihood。Hutchinson estimator 无偏不代表单样本低方差，support/topology 与同维 no-crossing 表达限制仍存在。

> [!note] 课程位置
> DYN-01—06 都以一条或有限条数值轨迹为中心。本章把视角提升为“所有初值同时怎样移动”：唯一性先把轨迹组织成 flow map，可微初值依赖再产生 Jacobian，Jacobi formula 把矩阵变化压成体积变化，概率换元最后把体积变化翻成 log-density。DYN-08 将从控制体与弱形式重新推导同一密度演化，检查 Lagrangian 与 Eulerian 两种语言是否闭合。

> [!tip] 建议两遍阅读
> **第一遍**只计算一个二维仿射流：先求 $\phi_t$、$D\phi_t$ 和 $\det D\phi_t$，再推前标准 Gaussian，最后核对 $d\log p_t(X_t)/dt=-\nabla\cdot f$。**第二遍**再进入非自治两参数流、共同存在域、反向完备性、一般变分方程、Hutchinson、离散可逆性、CNF support/topology 与梯度误差。第一遍要掌握的是“轨迹—切向量—体积—密度”四层对象，而不是只背 instantaneous change-of-variables 公式。

## 本章的推导问题链

1. 为什么“每个初值都有唯一解”还不等于已经得到全空间上的 global diffeomorphism？
2. Flow map $\phi_{s,t}$ 的输入输出是什么，composition law 为什么来自 uniqueness？
3. 对初值求导为什么得到变分方程 $\dot J=(D_xf)J$，而不是参数敏感度方程？
4. Jacobi determinant formula 怎样把矩阵 ODE 压缩成 $d\log\det J/dt=\operatorname{tr}(D_xf)$？
5. 为什么 divergence 只控制 infinitesimal volume，不控制所有 singular values、shape distortion 或稳定性？
6. 概率质量守恒怎样迫使沿轨迹的 log-density 与 log-volume 一增一减？
7. Hutchinson、ODE solver、likelihood 与 gradient 为什么是四个需要独立审计的误差层？

## 贯穿算例：仿射流怎样把圆形 Gaussian 压成移动椭圆

令

$$
\dot x=Ax+b,
\qquad
A=\begin{bmatrix}1&0\\0&-2\end{bmatrix},
\qquad
b=\begin{bmatrix}1\\0\end{bmatrix},
\qquad x(0)=a.
$$

第一个坐标向右平移并指数扩张，第二个坐标指数收缩；总体积由两个方向的净效应决定。

### 符号与对象账本

| 对象 | 类型 | 本例中的值/作用 | 不可直接称为 |
|---|---|---|---|
| $a$ | initial state/material label | $a\in\mathbb R^2$ | 时间 $t$ 的随机状态 |
| $\phi_t(a)$ | autonomous flow map | 从时刻 $0$ 把所有初值搬到 $t$ | 单条数组轨迹 |
| $J_t(a)$ | initial-state Jacobian | $D_a\phi_t(a)\in\mathbb R^{2\times2}$ | vector-field Jacobian $D_xf=A$ |
| $\det J_t$ | oriented volume factor | $e^{-t}$ | 每个方向都收缩的证明 |
| $p_0,p_t$ | initial/pushed densities | $p_t=(\phi_t)_\#p_0$ | 单条 trajectory probability |
| $\ell_t$ | pathwise log-density | $\ell_t=\log p_t(X_t)$ | 固定 $x$ 处的 $\partial_t\log p_t(x)$ |
| $\varepsilon^TA\varepsilon$ | stochastic trace estimate | probe 相关 | determinant 或 divergence 的自动精确值 |

### 第一步：解出整张 flow map，而不只是一条轨迹

两个坐标分别满足

$$
\dot x_1=x_1+1,
\qquad
\dot x_2=-2x_2.
$$

因此

$$
\boxed{
\phi_t(a)
=
\begin{bmatrix}
e^t(a_1+1)-1\\
e^{-2t}a_2
\end{bmatrix}.
}
$$

这里 $a$ 仍是变量，所以公式描述所有初值。直接代入可检查

$$
\phi_0=I,
\qquad
\phi_t\circ\phi_s=\phi_{t+s},
\qquad
\phi_t^{-1}=\phi_{-t}.
$$

本例在正负时间都全局存在，故确实是 $\mathbb R^2$ 上的 global diffeomorphism；一般 ODE 不能从局部 uniqueness 直接跳到这个结论。

### 第二步：变分方程追踪切向量与体积

对 $a$ 求导：

$$
J_t=D_a\phi_t(a)
=
\begin{bmatrix}
e^t&0\\
0&e^{-2t}
\end{bmatrix}.
$$

它满足

$$
\dot J_t=AJ_t,
\qquad J_0=I.
$$

两个 principal direction 的伸缩因子是 $e^t$ 与 $e^{-2t}$，所以

$$
\boxed{
\det J_t=e^t e^{-2t}=e^{-t}.
}
$$

另一方面

$$
\nabla\cdot f=\operatorname{tr}A=1-2=-1,
$$

Liouville 公式给

$$
\det J_t
=\exp\left(\int_0^t-1\,ds\right)
=e^{-t},
$$

与直接计算完全一致。总体积收缩不妨碍第一个方向扩张；trace/determinant 丢失了 anisotropic shape 信息。

### 第三步：推前标准 Gaussian

令随机初值

$$
X_0\sim\mathcal N(0,I_2),
\qquad X_t=\phi_t(X_0).
$$

仿射变换保持 Gaussian，因此

$$
X_t\sim\mathcal N(m_t,\Sigma_t),
$$

其中

$$
m_t=
\begin{bmatrix}e^t-1\\0\end{bmatrix},
\qquad
\Sigma_t=
\begin{bmatrix}e^{2t}&0\\0&e^{-4t}\end{bmatrix}.
$$

显式 density 为

$$
\boxed{
p_t(x)
=\frac{e^t}{2\pi}
\exp\left\{-\frac12\left[
e^{-2t}\bigl(x_1-(e^t-1)\bigr)^2
+e^{4t}x_2^2
\right]\right\}.
}
$$

因为 $\det\Sigma_t=e^{-2t}$，Gaussian normalization 的 $\det(\Sigma_t)^{-1/2}$ 正好贡献 $e^t$；这就是 flow volume $e^{-t}$ 的倒数。

### 第四步：沿轨迹核对 instantaneous change of variables

有限时间换元给

$$
p_t(\phi_t(a))\det J_t=p_0(a).
$$

代入 $\det J_t=e^{-t}$：

$$
\log p_t(\phi_t(a))
=\log p_0(a)+t.
$$

因此

$$
\boxed{
\frac d{dt}\log p_t(X_t)
=1
=-\nabla\cdot f(X_t).
}
$$

CNF 在这个例子中只需同时积分

$$
\dot X_t=AX_t+b,
\qquad
\dot\ell_t=1.
$$

注意 $\dot\ell_t$ 是沿 moving sample 的全导数，不是固定坐标点上的 $\partial_t\log p_t(x)$。

### 第五步：同一 trace 的两种 Hutchinson probe

对任意满足 $\mathbb E[\varepsilon\varepsilon^T]=I$ 的 probe，

$$
\mathbb E[\varepsilon^TA\varepsilon]=\operatorname{tr}A=-1.
$$

本例若 $\varepsilon_i$ 为独立 Rademacher，则 $\varepsilon_i^2=1$，所以

$$
\varepsilon^TA\varepsilon
=\varepsilon_1^2-2\varepsilon_2^2
=-1
$$

对每次抽样都精确，方差为零。若改用标准 Gaussian probe，估计量为 $\varepsilon_1^2-2\varepsilon_2^2$，仍无偏，但

$$
\operatorname{Var}(\varepsilon^TA\varepsilon)
=2\|A\|_F^2
=2(1+4)=10.
$$

这不是说 Rademacher 对所有网络 Jacobian 都零方差；这里只因 $A$ 恰好 diagonal。它准确展示了“相同均值合同，不同 estimator variance”。

## 核心公式七问：Liouville 公式怎样连接 Jacobian 与 divergence

$$
\boxed{
\frac d{dt}\log\det D_a\phi_t(a)
=\operatorname{tr}D_xf(t,\phi_t(a))
=\nabla\cdot f(t,\phi_t(a)).
}
$$

1. **解决什么问题？** 不必跟踪 Jacobian 的每个元素，就能得到 infinitesimal volume 的累计变化。
2. **对象与形状？** $D_a\phi_t,J_t,D_xf\in\mathbb R^{d\times d}$；determinant、trace 与 divergence 为标量。
3. **从哪里来？** 先由初值微分得 $\dot J=(D_xf)J$，再用 Jacobi formula $d\log\det J/dt=\operatorname{tr}(J^{-1}\dot J)$ 和 trace cyclicity。
4. **需要什么条件？** 共同存在的唯一 $C^1$ flow、对初值可微以及讨论区间上可逆的 $J$；global onto 还需反向 completeness。
5. **怎样检查？** 同时比较直接 determinant、divergence 时间积分与 finite change-of-variables；本例三者都是 $e^{-t}$。
6. **怎样误读？** $\det J>0$ 不保证各方向都收缩、不保证轨迹稳定，也不保证有限步 solver 精确保可逆。
7. **AI 中怎样调用？** CNF 用它更新 log-density；高维实现还需声明 exact/stochastic trace、probe policy、solver tolerance、support 与 gradient contract。

> [!success] 第一遍停靠线
> 合上正文后，应能从 $A,b$ 独立求出 $\phi_t,J_t,\det J_t$，解释为什么一个方向扩张但总体积仍以 $e^{-t}$ 收缩；随后写出推前 Gaussian 的 $m_t,\Sigma_t,p_t$，并核对沿轨迹 log-density 以速率 $1$ 增长。若把 $\operatorname{tr}A=-1$ 误读为“每个方向都收缩”，请回到 $J_t$ 的两个对角元素。

## 学习目标

完成本章后，应能：

1. 区分 solution curve、flow map、autonomous flow、nonautonomous two-parameter process；
2. 写出并证明 $\phi_{s,s}=I$ 与 composition law；
3. 说明 uniqueness 为什么给单射，以及为什么单射不自动给整个 $\mathbb R^d$ 上的满射；
4. 从 ODE 对初值求导得到 variational equation；
5. 用 Jacobi 公式完整推导 Liouville 公式；
6. 解释 $\det J>0$ 的 orientation-preserving 结论及其条件；
7. 从有限维 change of variables 推导 instantaneous log-density equation；
8. 区分 density 沿轨迹的全导数与固定空间点的偏导数；
9. 将 CNF 写成状态—log-density 的增广 ODE；
10. 推导 Hutchinson trace estimator 的无偏性与 Rademacher/Gaussian 方差；
11. 说明如何用 VJP/JVP 计算 $\varepsilon^T J_f\varepsilon$ 而不形成完整 Jacobian；
12. 用 $x'=-x^3$ 识别“前向单射但不 onto $\mathbb R$”的完整性边界；
13. 用非正规线性流区分 shape distortion、transient stretch 与 volume change；
14. 解释 ODE flow 的 no-crossing、topology 与同维表达限制；
15. 审计一个 CNF 的 support、solver、trace、likelihood、sampling 与 gradient claim。

> [!question] 初学者读完必须能回答
> 1. Solution curve 与 flow map 的输入输出有何不同？
> 2. Uniqueness 为什么给 injectivity，却不自动给全空间 surjectivity？
> 3. 变分方程 $\dot J=(D_xf)J$ 怎样从初值微分导出？
> 4. Jacobi formula 如何推出 $d\log\det J/dt=\nabla\cdot f$？
> 5. Divergence 为什么控制 volume，却不等同于 trajectory stability？
> 6. CNF 的 state/log-density 增广 ODE 怎样写？
> 7. Trace estimator、solver、likelihood 与 gradient 各需哪些独立证据？

## 零、对象地图：一条轨迹、一个流和一族密度不是同一个对象

考虑非自治 ODE

$$
\dot x(t)=f(t,x(t)),
\qquad x(s)=x_s,
\qquad x(t)\in\Omega\subseteq\mathbb R^d.
$$

至少有五层对象：

| 层 | 记号 | 输入与输出 | 需要的条件 |
|---|---|---|---|
| 单条解 | $t\mapsto x(t;s,x_s)$ | 固定 $(s,x_s)$，输出轨迹 | existence |
| 唯一轨迹 | 同上 | 相同初值不能分叉 | uniqueness |
| 流映射 | $\phi_{s,t}:x_s\mapsto x(t;s,x_s)$ | 搬运一整片状态 | 对所有讨论初值共同存在 |
| 可微流 | $D_x\phi_{s,t}$ | 搬运切向量与局部体积 | $f$ 对 $x$ 至少 $C^1$ 等初值依赖条件 |
| 分布搬运 | $(\phi_{s,t})_\#\mu_s=\mu_t$ | 搬运 probability law | 可测性；写 density 还需绝对连续/换元条件 |

这里 $\#$ 表示 pushforward：若 $X_s\sim\mu_s$，则

$$
X_t=\phi_{s,t}(X_s)
\quad\Longrightarrow\quad
X_t\sim(\phi_{s,t})_\#\mu_s.
$$

> [!warning] 第一条防混淆线
> “ODE 对一个初值求出了数组”并不说明在某个开放集上存在共同流；“存在唯一流”不说明对初值可微；“可微且 Jacobian 非奇异”也不自动说明映射 onto 整个 $\mathbb R^d$；“精确流可逆”更不说明某个有限步离散程序仍精确可逆。

## 一、非自治流映射与两参数 composition law

### 1.1 定义

设每个 $x_s$ 在 $s$ 到 $t$ 之间都有唯一解，定义

$$
\phi_{s,t}(x_s):=x(t;s,x_s).
$$

$s$ 是起始时间，$t$ 是终止时间。非自治系统需要两个时间指标，因为同样持续时间的演化可能取决于日历时间：

$$
f(t,x)=a(t)x
$$

在区间 $[0,1]$ 与 $[10,11]$ 上一般不是同一映射。

### 1.2 恒等律

零时间演化不改变状态：

$$
\phi_{s,s}(x)=x,
\qquad
\phi_{s,s}=\operatorname{Id}.
$$

### 1.3 组合律

若 $s\le u\le t$ 且相关解存在，则

$$
\boxed{
\phi_{u,t}\circ\phi_{s,u}=\phi_{s,t}.
}
$$

证明不能只写“显然”。取 $x_s$，令

$$
y=\phi_{s,u}(x_s).
$$

轨迹 $r\mapsto x(r;s,x_s)$ 在 $r=u$ 的值是 $y$；而 $r\mapsto x(r;u,y)$ 也是从 $(u,y)$ 出发的解。由 uniqueness，两条解在共同区间上相同，所以在 $t$ 时刻

$$
\phi_{u,t}(\phi_{s,u}(x_s))
=x(t;u,y)
=x(t;s,x_s)
=\phi_{s,t}(x_s).
$$

composition law 的真正来源是 uniqueness；没有 uniqueness，同一中间状态之后可能选择不同分支，便不能得到单值的演化算子。

### 1.4 自治系统才可压成一个参数

若 $f$ 不显含时间，记

$$
\phi_t(x):=\phi_{0,t}(x).
$$

时间平移不改变方程，因此在共同存在域上

$$
\phi_{t+s}=\phi_t\circ\phi_s.
$$

若所有解对 $t\in\mathbb R$ 全局存在，则

$$
\phi_0=I,
\qquad
\phi_{-t}=\phi_t^{-1},
$$

从而得到一参数群。若只保证 $t\ge0$ 的前向存在，则通常只有 semigroup，不能随意写 $\phi_{-t}$。

### 1.5 非自治系统也能增广成自治系统

令

$$
z=(\tau,x),
\qquad
\dot\tau=1,
\qquad
\dot x=f(\tau,x).
$$

这是 $d+1$ 维自治系统。它统一理论语言，但增加了状态维数；实现或密度建模时必须说明是否把时间坐标视作随机变量。通常 CNF 的时间是外部控制量，不对时间维建 density。

## 二、唯一性给出什么样的可逆性

### 2.1 共同存在域上的单射

固定 $s<t$。若 $x_s\ne y_s$ 却有

$$
\phi_{s,t}(x_s)=\phi_{s,t}(y_s)=z,
$$

则两条轨迹在时刻 $t$ 相遇。把 $z$ 作为 $t$ 时刻初值向后看，uniqueness 要求共同区间上的解相同，于是在 $s$ 时刻也应有 $x_s=y_s$，矛盾。因此

$$
\boxed{\phi_{s,t}\text{ 在共同存在域上是单射。}}
$$

这就是“精确 ODE 轨迹不能相交”的数学含义。它不是说曲线在画面投影中不能重叠，也不是说不同时间的同一周期轨道不能回到同一点；它说的是：同一时刻、同一完整状态不能由两个不同初态到达。

### 2.2 逆映射的正确写法

若从每个终点 $z$ 出发都能反向延拓回 $s$，则

$$
\phi_{s,t}^{-1}=\phi_{t,s}.
$$

但这里的定义域/值域必须写清：一般最稳妥的结论是

$$
\phi_{s,t}:D_{s,t}\longrightarrow \phi_{s,t}(D_{s,t})
$$

在其像上可逆，而不是无条件声称它是 $\mathbb R^d\to\mathbb R^d$ 的双射。

### 2.3 反例：$x'=-x^3$ 前向全局，却不 onto 整条实线

考虑

$$
\dot x=-x^3,
\qquad x(0)=x_0.
$$

分离变量得

$$
\frac{dx}{x^3}=-dt.
$$

对 $x_0\ne0$ 积分：

$$
-\frac1{2x(t)^2}+\frac1{2x_0^2}=-t,
$$

所以

$$
\boxed{
\phi_t(x_0)=\frac{x_0}{\sqrt{1+2tx_0^2}},
\qquad t\ge0.
}
$$

它对每个 $x_0\in\mathbb R$、每个 $t\ge0$ 都存在，且严格递增，因此单射。但是固定 $t>0$ 时

$$
|\phi_t(x_0)|<\frac1{\sqrt{2t}},
$$

并且 $|x_0|\to\infty$ 时趋近边界。因此

$$
\phi_t(\mathbb R)
=\left(-\frac1{\sqrt{2t}},\frac1{\sqrt{2t}}\right),
$$

它不是 onto $\mathbb R$。

为什么？反向方程等价于

$$
\dot x=x^3,
$$

它会 finite-time blow-up。前向 completeness 不等于双向 completeness。

> [!important] 可逆性结论阶梯
> 1. uniqueness：在共同存在域上 no crossing / 单射；
> 2. $C^1$ 初值依赖且 $\det J\ne0$：局部微分同胚；
> 3. 有反向解：映射与其像之间可逆；
> 4. 对所有初终点双向全局存在：才可称整个状态空间上的 global diffeomorphism。

## 三、初值扰动怎样传播：变分方程

### 3.1 从有限差分到切向量

固定 $s$ 与初值 $x_s$。将初值沿方向 $v$ 扰动：

$$
x_s(\varepsilon)=x_s+\varepsilon v.
$$

对应轨迹为

$$
x_\varepsilon(t)=\phi_{s,t}(x_s+\varepsilon v).
$$

若 $f$ 对状态为 $C^1$，并满足保证解对初值可微的局部条件，定义

$$
\xi(t)
=\left.\frac{d}{d\varepsilon}x_\varepsilon(t)\right|_{\varepsilon=0}.
$$

对 ODE 求导：

$$
\begin{aligned}
\dot\xi(t)
&=\left.\frac{d}{d\varepsilon}
f(t,x_\varepsilon(t))\right|_{\varepsilon=0}\\
&=D_xf(t,x(t))\,\xi(t),
\end{aligned}
$$

初值为

$$
\xi(s)=v.
$$

所以无限小扰动服从沿基准轨迹的时变线性系统。

### 3.2 Jacobian 矩阵形式

定义 flow Jacobian

$$
J_{s,t}(x_s):=D_{x_s}\phi_{s,t}(x_s)\in\mathbb R^{d\times d}.
$$

因为任意 $v$ 都有 $\xi(t)=J_{s,t}v$，故

$$
\boxed{
\frac{d}{dt}J_{s,t}
=D_xf(t,x_t)J_{s,t},
\qquad J_{s,s}=I.
}
$$

这就是 first variational equation。注意矩阵乘法顺序：$D_xf$ 在左，$J$ 在右。

### 3.3 链式法则与 Jacobian composition

由

$$
\phi_{s,t}=\phi_{u,t}\circ\phi_{s,u}
$$

及链式法则，

$$
J_{s,t}(x_s)
=J_{u,t}(x_u)J_{s,u}(x_s),
\qquad x_u=\phi_{s,u}(x_s).
$$

因此 determinant 乘法分解：

$$
\det J_{s,t}
=\det J_{u,t}\det J_{s,u}.
$$

取 log 后，局部 log-volume change 对时间可加，这正是连续 flow 比逐层 determinant 更容易累积的结构来源。

### 3.4 参数灵敏度不是初值 Jacobian

若 $f=f_\theta$，参数切向量

$$
S(t)=\frac{\partial x(t)}{\partial\theta}
$$

满足

$$
\dot S
=D_xf_\theta(t,x)S+D_\theta f_\theta(t,x),
\qquad S(s)=\frac{\partial x_s}{\partial\theta}.
$$

多出的 forcing $D_\theta f$ 很重要。$J_{s,t}$ 描述 state-to-state 变形；$S$ 描述 parameter-to-state sensitivity。CNF density 公式使用前者的 divergence，不是参数 Jacobian 的 trace。

## 四、Liouville 公式：从矩阵 ODE 到体积 ODE

### 4.1 Jacobi determinant formula

对可逆可微矩阵路径 $J(t)$，

$$
\frac{d}{dt}\det J(t)
=\det J(t)\operatorname{tr}\bigl(J(t)^{-1}\dot J(t)\bigr).
$$

等价地，

$$
\frac{d}{dt}\log\det J(t)
=\operatorname{tr}\bigl(J(t)^{-1}\dot J(t)\bigr).
$$

本章稍后会证明 $\det J>0$，所以不需要绝对值；对一般矩阵换元，常写 $\log|\det J|$。

### 4.2 代入变分方程

令

$$
A(t):=D_xf(t,x_t).
$$

因为 $\dot J=AJ$，

$$
J^{-1}\dot J=J^{-1}AJ.
$$

迹在相似变换下不变：

$$
\operatorname{tr}(J^{-1}AJ)=\operatorname{tr}(A).
$$

因此

$$
\frac{d}{dt}\log\det J_{s,t}
=\operatorname{tr}D_xf(t,x_t).
$$

向量场的 divergence 定义为

$$
\operatorname{div}f(t,x)
=\nabla_x\cdot f(t,x)
=\sum_{i=1}^d\frac{\partial f_i}{\partial x_i}(t,x)
=\operatorname{tr}D_xf(t,x).
$$

于是

$$
\frac{d}{dt}\log\det J_{s,t}
=\operatorname{div}f(t,x_t).
$$

从 $s$ 积到 $t$，并用 $J_{s,s}=I$：

$$
\log\det J_{s,t}-\log1
=\int_s^t\operatorname{div}f(\tau,x_\tau)d\tau.
$$

最终得到

$$
\boxed{
\det D\phi_{s,t}(x_s)
=\exp\!\left(
\int_s^t\operatorname{div}f(\tau,x_\tau)d\tau
\right).
}
$$

### 4.3 为什么 determinant 不会变号

指数恒正，因此

$$
\det D\phi_{s,t}(x_s)>0.
$$

这同时给出：

- $J_{s,t}$ 在存在区间上不会奇异；
- 流在每一点附近是 local diffeomorphism；
- 从 identity 连续演化而来的精确 ODE flow 保持 orientation；
- determinant 不可能穿过零后变负。

这里的逻辑依赖可微流与公式成立。它不声称任意可逆网络都 orientation preserving，也不声称数值离散 map 的 determinant 必为正。

### 4.4 微小体积元的解释

在 $x_s$ 附近取由向量 $v_1,\dots,v_d$ 张成的微小平行体，初始有向体积为

$$
\det[v_1,\dots,v_d].
$$

流后切向量变成

$$
J_{s,t}v_1,\dots,J_{s,t}v_d,
$$

所以体积乘以

$$
\det J_{s,t}.
$$

瞬时相对体积增长率为 divergence：

$$
\lim_{h\to0}
\frac{\det J_{t,t+h}-1}{h}
=\operatorname{div}f(t,x_t).
$$

> [!note] divergence 不是轨迹稳定性的同义词
> $\operatorname{div}f<0$ 只说明局部总体积收缩；某些方向仍可拉伸。稳定性需要控制 individual directions、Lyapunov exponents 或 norm，而 trace 只记录它们的总和。

## 五、三个精确例子

### 5.1 一维 affine flow

考虑

$$
\dot x=a(t)x+b(t).
$$

令

$$
\alpha(s,t)=\exp\!\left(\int_s^t a(\tau)d\tau\right).
$$

variation of constants 给出

$$
\phi_{s,t}(x_s)
=\alpha(s,t)x_s
+\int_s^t\alpha(u,t)b(u)du.
$$

对初值求导：

$$
J_{s,t}=\alpha(s,t).
$$

而 divergence 就是

$$
\frac{\partial}{\partial x}(a(t)x+b(t))=a(t).
$$

Liouville 公式精确恢复 $J_{s,t}=e^{\int a}$。平移项 $b$ 搬动位置，却不改变局部长度或 density scaling。

### 5.2 线性多维 flow

对

$$
\dot x=Ax,
$$

有

$$
\phi_{s,t}(x_s)=e^{(t-s)A}x_s,
\qquad
J_{s,t}=e^{(t-s)A}.
$$

Liouville 给出经典恒等式

$$
\boxed{
\det(e^{(t-s)A})
=e^{(t-s)\operatorname{tr}A}.
}
$$

不需要 $A$ 可对角化。trace 控制总体积，奇异值控制各方向长度。

取非正规矩阵

$$
A=
\begin{bmatrix}
-1&8\\
0&-2
\end{bmatrix}.
$$

则

$$
e^{tA}
=\begin{bmatrix}
e^{-t}&8(e^{-t}-e^{-2t})\\
0&e^{-2t}
\end{bmatrix},
$$

而

$$
\det e^{tA}=e^{-3t}.
$$

单位正方形可被强烈剪切、某个方向甚至 transiently stretched，但面积仍严格按 $e^{-3t}$ 缩小。于是

$$
\text{shape change}\ne\text{volume change}\ne\text{trajectory stability}.
$$

### 5.3 非线性 $x'=-x^3$

上一节已得到

$$
\phi_t(x_0)=\frac{x_0}{\sqrt{1+2tx_0^2}}.
$$

直接求导：

$$
J_t(x_0)
=\frac{1}{(1+2tx_0^2)^{3/2}}.
$$

另一方面

$$
\operatorname{div}f(x)=f'(x)=-3x^2.
$$

沿轨迹

$$
x(\tau)^2=\frac{x_0^2}{1+2\tau x_0^2}.
$$

所以

$$
\begin{aligned}
\int_0^t-3x(\tau)^2d\tau
&=-3\int_0^t\frac{x_0^2}{1+2\tau x_0^2}d\tau\\
&=-\frac32\log(1+2tx_0^2).
\end{aligned}
$$

指数化恰得

$$
\det J_t=(1+2tx_0^2)^{-3/2}.
$$

这个例子同时说明：Jacobian 处处正、映射局部可逆、前向单射，仍不等于 onto $\mathbb R$。

## 六、从体积换元到密度换元

### 6.1 先写有限时间公式

假设 $X_s$ 有 density $p_s$，且 $X_t=\phi_{s,t}(X_s)$。对足够好的可逆流，有限维换元公式为

$$
p_t(x_t)
=p_s(x_s)
\left|\det D\phi_{s,t}(x_s)\right|^{-1},
\qquad x_t=\phi_{s,t}(x_s).
$$

由于精确 ODE flow 的 determinant 为正，可写

$$
\boxed{
p_t(x_t)\det J_{s,t}(x_s)=p_s(x_s).
}
$$

这是“同一小团概率质量不变”的表达：

$$
p_s(x_s)dV_s
=p_t(x_t)dV_t,
\qquad
dV_t=(\det J_{s,t})dV_s.
$$

### 6.2 取 log

$$
\log p_t(x_t)
=\log p_s(x_s)-\log\det J_{s,t}(x_s).
$$

代入 Liouville：

$$
\boxed{
\log p_t(x_t)
=\log p_s(x_s)
-\int_s^t\operatorname{div}f(\tau,x_\tau)d\tau.
}
$$

### 6.3 瞬时换元公式

对 $t$ 求全导数：

$$
\boxed{
\frac{d}{dt}\log p_t(x_t)
=-\operatorname{div}f(t,x_t)
=-\operatorname{tr}D_xf(t,x_t).
}
$$

左端是沿随流粒子的 material derivative：

$$
\frac{d}{dt}\log p_t(x_t)
=\partial_t\log p_t(x_t)
+\nabla_x\log p_t(x_t)^Tf(t,x_t).
$$

它不是固定 $x$ 处的 $\partial_t\log p_t(x)$。

### 6.4 与连续性方程的预告

把上式乘开：

$$
\partial_t p+f^T\nabla p=-p\,\nabla\cdot f.
$$

移项即

$$
\partial_t p+\nabla\cdot(pf)=0.
$$

本章用它确认对象一致；控制体积分、弱形式、边界通量、measure solution 与 characteristics 的完整推导见[[连续性方程与守恒律]]。

## 七、Continuous Normalizing Flow 的建模合同

### 7.1 离散 flow 与连续 flow

离散 normalizing flow 以可逆映射序列

$$
z_K=T_K\circ\cdots\circ T_1(z_0)
$$

搬运 density：

$$
\log p_K(z_K)
=\log p_0(z_0)
-\sum_{k=1}^K\log|\det DT_k(z_{k-1})|.
$$

CNF 令 transformation 由 ODE 定义：

$$
\dot z=f_\theta(t,z),
\qquad z(t_0)=z_0,
$$

并将 determinant 的离散累加替换为 divergence 的时间积分。

### 7.2 增广 ODE

定义

$$
\ell(t)=\log p_t(z(t)).
$$

则

$$
\boxed{
\frac{d}{dt}
\begin{bmatrix}
z\\\ell
\end{bmatrix}
=
\begin{bmatrix}
f_\theta(t,z)\\
-\operatorname{tr}D_zf_\theta(t,z)
\end{bmatrix}.
}
$$

从 base 到 data：

$$
z_0\sim p_0,
\quad z_1=\phi_{0,1}(z_0)
$$

用于采样。计算 data likelihood 常反向积分：给定 $x=z_1$，恢复 $z_0$ 并计算

$$
\log p_1(x)
=\log p_0(z_0)
-\int_0^1\operatorname{div}f_\theta(t,z_t)dt.
$$

反向积分时符号应由积分上下限统一处理，不应靠记忆随意翻转。

### 7.3 base、target 与支持集

若 $p_0$ 是 $\mathbb R^d$ 上处处正的 Lebesgue density，且 $\phi$ 是 $\mathbb R^d$ 上的 global diffeomorphism，则 $p_1$ 也在 $\mathbb R^d$ 上处处正并保持 full dimension。它不能精确产生：

- 真正落在低维流形上的 singular law；
- 需要撕裂/粘合状态空间才能得到的映射；
- 不同输入在有限时刻精确合并的 deterministic map。

数据加噪、dequantization、surjective/augmented flow 或显式 observation model 可以改变任务，但必须声明改变了什么概率对象。

### 7.4 条件 CNF

条件向量 $c$ 固定时可写

$$
\dot z=f_\theta(t,z;c).
$$

对每个 $c$，divergence 是对 $z$ 求：

$$
\operatorname{div}_z f_\theta(t,z;c),
$$

不是把 context 坐标也计入随机状态。若 $c$ 本身也被动力学演化并建联合密度，则必须重新定义联合状态与 base law。

## 八、为什么 trace 比 determinant 更便于连续时间计算

对一般 dense $d\times d$ Jacobian，显式形成矩阵要存储 $O(d^2)$ 元素，通用 determinant 约需 $O(d^3)$ 算术。CNF 使用

$$
\operatorname{tr}D_xf=\sum_i\frac{\partial f_i}{\partial x_i},
$$

避免通用 determinant，但“trace 很便宜”仍不是无条件事实：

- 若逐个坐标用 reverse-mode 求 diagonal，可能需要 $d$ 次反向传播；
- 特殊架构可让 divergence 解析可算；
- stochastic trace estimator 可把成本变成少量 Jacobian-vector/vector-Jacobian products；
- estimator 只降低单次代数成本，可能增加方差与 ODE RHS 噪声。

## 九、Hutchinson 随机迹估计

### 9.1 无偏性

令 $A\in\mathbb R^{d\times d}$，随机向量 $\varepsilon$ 满足

$$
\mathbb E[\varepsilon]=0,
\qquad
\mathbb E[\varepsilon\varepsilon^T]=I.
$$

定义

$$
\widehat\tau=\varepsilon^TA\varepsilon.
$$

用 trace trick：

$$
\varepsilon^TA\varepsilon
=\operatorname{tr}(\varepsilon^TA\varepsilon)
=\operatorname{tr}(A\varepsilon\varepsilon^T).
$$

取期望：

$$
\mathbb E\widehat\tau
=\operatorname{tr}\left(A\mathbb E[\varepsilon\varepsilon^T]\right)
=\operatorname{tr}A.
$$

所以

$$
\boxed{
\mathbb E[\varepsilon^TA\varepsilon]=\operatorname{tr}A.
}
$$

### 9.2 非对称 Jacobian 只通过对称部分进入二次型

写

$$
A=S+K,
\qquad
S=\frac{A+A^T}{2},
\qquad
K=\frac{A-A^T}{2}.
$$

因为 $K^T=-K$，

$$
\varepsilon^TK\varepsilon=0.
$$

故

$$
\varepsilon^TA\varepsilon=\varepsilon^TS\varepsilon,
\qquad
\operatorname{tr}A=\operatorname{tr}S.
$$

variance 公式应对 $S$ 写，而不是在非对称 $A$ 上机械套对称矩阵公式。

### 9.3 Rademacher 方差

若 $\varepsilon_i$ 独立且

$$
\mathbb P(\varepsilon_i=1)
=\mathbb P(\varepsilon_i=-1)=\frac12,
$$

则 $\varepsilon_i^2=1$，于是

$$
\widehat\tau
=\sum_iS_{ii}+2\sum_{i<j}S_{ij}\varepsilon_i\varepsilon_j.
$$

均值是 $\operatorname{tr}S$。不同 unordered pair 的交叉项期望为零，所以

$$
\boxed{
\operatorname{Var}(\widehat\tau_{\rm Rad})
=4\sum_{i<j}S_{ij}^2
=2\sum_{i\ne j}S_{ij}^2.
}
$$

对 diagonal $S$，Rademacher estimator 的方差恰为零。

### 9.4 Gaussian 方差

若 $\varepsilon\sim\mathcal N(0,I)$，则对称二次型有

$$
\boxed{
\operatorname{Var}(\widehat\tau_{\rm Gau})
=2\|S\|_F^2.
}
$$

它包含 diagonal 能量，因此在同一矩阵上常比 Rademacher 方差大；“常”不是所有下游程序误差的绝对排序，因为随机数实现、vectorization 与训练优化也会影响总成本。

### 9.5 多探针平均

取 $m$ 个独立 probe：

$$
\overline\tau_m
=\frac1m\sum_{k=1}^m\varepsilon_k^TA\varepsilon_k.
$$

则

$$
\mathbb E\overline\tau_m=\operatorname{tr}A,
\qquad
\operatorname{Var}(\overline\tau_m)
=\frac1m\operatorname{Var}(\widehat\tau).
$$

standard deviation 按 $m^{-1/2}$ 降低，不是 $m^{-1}$。

## 十、怎样不形成 Jacobian 计算 $\varepsilon^TJ_f\varepsilon$

### 10.1 JVP 路线

先算

$$
u=J_f\varepsilon
$$

作为 JVP，再算

$$
\varepsilon^Tu.
$$

forward-mode 对输入维和输出维相近的 vector field 很自然。

### 10.2 VJP 路线

注意标量

$$
g(x)=\varepsilon^Tf(x).
$$

若把 $\varepsilon$ 视作不依赖 $x$ 的常量，

$$
\nabla_xg(x)
=J_f(x)^T\varepsilon.
$$

于是

$$
\varepsilon^T J_f\varepsilon
=\bigl(J_f^T\varepsilon\bigr)^T\varepsilon
=\nabla_x(\varepsilon^Tf(x))^T\varepsilon.
$$

一次 reverse-mode VJP 即可得到 probe quadratic form。

> [!warning] stop-gradient 条件
> probe $\varepsilon$ 在对 $x$ 求导时必须当作常量。若错误地让 probe 依赖 $x$，product rule 会引入额外项，估计量不再是目标 divergence。

### 10.3 exact trace 与 stochastic trace 的选择

| 条件 | 优先考虑 |
|---|---|
| $d$ 小，需高精度 likelihood/evaluation | exact diagonal/trace |
| 架构的 divergence 有解析结构 | exact structured trace |
| $d$ 大，训练可容忍随机梯度 | Hutchinson/FFJORD |
| off-diagonal symmetric energy很大 | 增加 probes、variance reduction或改架构 |
| 需要可重复评估 | 固定 seeds 并报告 Monte Carlo uncertainty，必要时 exact/reference subset |

## 十一、随机 trace 与自适应 ODE 求解器的语义

### 11.1 一条 ODE 的 RHS 应该是什么函数

确定性 CNF 的增广 RHS 是

$$
F(t,z,\ell)
=\left(f_\theta(t,z),-\operatorname{tr}J_f(t,z)\right).
$$

用 Hutchinson 后，给定 probe $\varepsilon$ 得到随机近似

$$
F_\varepsilon(t,z,\ell)
=\left(f_\theta(t,z),-\varepsilon^TJ_f(t,z)\varepsilon\right).
$$

如果一次完整 solve 内固定 $\varepsilon$，那么 conditional on $\varepsilon$，solver 看见的是一条确定 RHS。若每次 RHS evaluation 都重新采样，solver 实际看见跳动/噪声函数；classical adaptive local-error estimator 的平滑假设与 step rejection 语义会改变。

因此至少要记录：

- probe distribution；
- 每条样本、每个 batch 还是整个 solve 共享；
- accepted/rejected step 重算时是否复用；
- forward/backward pass 是否复用；
- 训练和评估的 probe 数；
- 报告的是 conditional solver error 还是同时含 Monte Carlo error。

### 11.2 “无偏 trace”不自动推出“无偏 likelihood”

在固定 trajectory 上，$\widehat{\operatorname{tr}J}$ 可无偏。但实际程序里：

- trajectory $z(t)$ 可能由 estimator、参数和自适应 branch 共同影响；
- log-density 经过有限步非线性积分；
- likelihood 又经过 $\exp$、dataset average 或 optimization；
- stochastic gradient 的目标可能含 reuse/resampling 语义。

所以必须明确无偏性的对象和条件，不能从 pointwise trace estimator 直接跳到训练后模型或 exp-density 的无偏性。

## 十二、离散求解器可能破坏精确流的结构

### 12.1 Euler residual map 可以折叠

Forward Euler 一步是

$$
\Psi_h(x)=x+hf(x).
$$

其 Jacobian 为

$$
D\Psi_h(x)=I+hD f(x).
$$

即使精确 flow 对所有有限时间都 orientation preserving，$\det(I+hDf)$ 也可能为零或负。

一维例子：

$$
f(x)=-x^3,
\qquad
\Psi_h(x)=x-hx^3.
$$

导数

$$
\Psi_h'(x)=1-3hx^2
$$

在 $|x|=1/\sqrt{3h}$ 为零，并在外侧为负；一步 Euler map 会折叠，而精确 flow 不会。

### 12.2 一个充分的全局注入条件

若 $f$ 是全局 $L$-Lipschitz，且 $hL<1$，则

$$
\begin{aligned}
\|\Psi_h(x)-\Psi_h(y)\|
&=\|x-y+h(f(x)-f(y))\|\\
&\ge(1-hL)\|x-y\|.
\end{aligned}
$$

因此 $\Psi_h$ 单射。给定 $z$，方程

$$
x=z-hf(x)
$$

的右端是 contraction，Banach fixed-point 又给出唯一解，所以在 $\mathbb R^d$ 上还是满射。于是 $hL<1$ 是 Euler residual block 成为 global bi-Lipschitz map 的一个充分条件。

它通常很保守，也要求全局 Lipschitz；不能把局部 Jacobian norm 小于 $1/h$ 的采样证据替代全局结论。

### 12.3 数值可逆不等于重新积分能回到原点

即使每一步离散 map 数学上可逆，用 adaptive solver 从 $t_0$ 积到 $t_1$ 再反向积分也可能因以下原因不回到起点：

- forward/backward 采用不同网格；
- local errors 在不同方向累计；
- reject/accept branch 不同；
- floating-point 舍入；
- stiff backward dynamics 放大误差；
- event、clipping 或非光滑模块。

所以 reconstruction error 是数值诊断，不是 exact flow theorem 的否定或证明。

## 十三、拓扑与表达能力边界

### 13.1 no-crossing 限制

同维、唯一 ODE flow 不能把两个不同点精确合并。因而某些 ordinary map 可以实现、同维 flow 却不能实现的变换包括一维 $x\mapsto x^2$：它把 $x$ 与 $-x$ 合并，且改变 orientation。

### 13.2 连通性与洞

homeomorphism/diffeomorphism 保持基本拓扑性质：连通集的像仍连通，不能凭光滑可逆变换撕裂或粘合。概率上要更谨慎：一个处处正 density 可用极低密度“桥”近似视觉上的两个簇，所以有限样本看见分离簇不证明支持集严格不连通。

### 13.3 augmentation 为什么有帮助

把状态从 $\mathbb R^d$ 提升到 $\mathbb R^{d+k}$：

$$
\tilde x(0)=(x,0),
\qquad
\dot{\tilde x}=\tilde f_\theta(t,\tilde x),
$$

高维轨迹可绕开低维中必须相交的几何障碍；最后再投影到目标输出。Augmented Neural ODE 因而可扩展表示能力。

但 projection 本身不是 $d+k$ 维可逆 flow，所以：

- 分类/回归表示可直接使用 projection；
- 若做 exact likelihood，必须说明 latent/augmented variables 的概率模型与边缘化；
- “加维后表达更强”不等于任意 likelihood 都仍能 tractably exact 计算。

## 十四、CNF 的完整误差账本

一次 CNF 训练或评估至少有七类误差：

| 误差 | 对象 | 典型诊断 |
|---|---|---|
| model approximation | $f_\theta$ 是否能表示目标 transport | 增宽/改架构/augmentation，对照 held-out metric |
| state discretization | $z_h(t)$ vs exact $z(t)$ | tolerance/step refinement、reference solve |
| divergence approximation | exact trace vs stochastic/structured estimate | exact small-d benchmark、probe sweep、variance |
| log-density quadrature | $\ell_h$ vs 沿轨迹积分 | 与 state 同步的 augmented refinement |
| finite precision | 舍入与 reduction | precision sweep、reproducibility |
| reverse/reconstruction | 反向积分误差 | round trip 与 grid/tolerance 日志 |
| gradient mismatch | continuous/discrete/checkpoint/stochastic objective | same-objective finite difference、adjoint residual |

### 14.1 为什么只报告 NFE 不够

NFE 没有包含：

- 每次 RHS 中 exact trace 还是几次 VJP；
- rejected steps；
- backward/adjoint solve；
- Jacobian/linear solve（stiff method）；
- batch/vectorization；
- probe 数与方差；
- 达到的 state/log-density/likelihood error。

合格比较需要 equal-error 与 full-cost。

### 14.2 stiff CNF

若 $D_xf$ 含大负实部或强 time-scale separation，状态可能靠近慢流形，但 explicit solver 仍受稳定性限制。此时 exact divergence formula 不变；改变的是计算它的 solver 合同。需回到[[刚性系统、绝对稳定域与隐式方法]]检查 A/L-stability、Newton–Krylov、preconditioning 与 reverse dynamics。

## 十五、训练、采样与 likelihood 是三个不同任务

### 15.1 采样

输入 base sample $z_0$，只需前向求 $z_1$。若不需要 likelihood，可不积分 $\ell$；但这不再验证 density 计算。

### 15.2 likelihood evaluation

输入 data $x=z_1$，需要反向恢复 $z_0$ 并计算 log-density correction。应报告：

- base log-density；
- divergence scheme；
- forward/reverse tolerance；
- exact/stochastic evaluation probes；
- bits/dim 或 NLL 的单位与 dequantization 常数；
- Monte Carlo standard error。

### 15.3 training

训练还需对数值程序求参数梯度。常见对象：

1. 对 exact continuous objective 的形式 adjoint；
2. 对 finite adaptive program 的 discrete differentiation；
3. checkpoint/recompute 近似；
4. 对固定/重采样 probe 的 stochastic gradient。

它们可在 tolerance 收紧时接近，但有限容差下不是同一个函数的同一梯度。必须像 DYN-05 那样声明 target objective 并做 same-objective finite-difference check。

## 十六、常见错误与最小反例

| 错误说法 | 反例/修正 |
|---|---|
| existence 自动给 flow | $x'=\sqrt{|x|},x(0)=0$ 非唯一，不能定义单值 flow |
| forward global 自动给 $\mathbb R^d$ 上双射 | $x'=-x^3$ 的像是有界开区间 |
| $\det J\ne0$ 自动给 global inverse | 只给 local inverse；还需 global injectivity/surjectivity |
| divergence 负说明所有方向稳定 | 非正规线性流可在面积收缩时 transient stretch |
| divergence 为零说明状态不变 | rotation/shear 都可 volume preserving 而持续运动 |
| exact flow 可逆，所以 Euler 也可逆 | $x-hx^3$ 会折叠 |
| Hutchinson 无偏，所以单次 estimate 准确 | 方差可很大；无偏不等于小误差 |
| trace estimator 无偏，所以最终 likelihood 无偏 | nonlinear solver/trajectory/exp/optimization需单独分析 |
| CNF 可表示任意 map | 同维唯一流有 topology/no-crossing限制 |
| 数值 round trip 不为零说明理论不可逆 | adaptive grid与离散误差足以造成 mismatch |
| NFE 更低说明方法更快更准 | trace/VJP、rejection、linear solve与误差门未计入 |

## 十七、从科学空间文章进入，但不止于文章

[[S-2018-Su-5776-NICE流模型]]提供离散可逆变换与 log-determinant 的中文生成模型入口；本章把它提升为“finite change of variables → infinitesimal trace integral”的统一视角。[[S-2022-Su-9280-硬刚扩散ODE]]中由 Jacobian 与小步密度变化进入 ODE 的推导，适合建立问题直觉；本章补上 flow existence、初值可微、Liouville determinant 及 solver error 条件。[[S-2025-Su-10958-瞬时速度与平均速度]]提醒 learned instantaneous velocity、finite-step average velocity 与具体 sampler map 不应混为一谈；本章进一步说明换掉 vector field 或离散 map，也就换掉了 density transport 对象。

证据分工为：

- Teschl 承担 IVP dependence、autonomous flow 与 dynamical-system 标准理论；
- Chen et al. 承担 Neural ODE/CNF 的原始 AI 框架与 instantaneous change-of-variables；
- Grathwohl et al. 承担 FFJORD 用 Hutchinson estimator 扩展 CNF 的原始方法；
- Hutchinson 原论文承担随机 trace estimator 的历史来源；
- Rezende–Mohamed 承担离散 normalizing flow/change-of-variables 的生成建模原始脉络；
- Dupont et al. 承担同维 Neural ODE topology limitation 与 augmentation；
- 科学空间承担中文问题入口，不单独承担全局微分同胚、Liouville 或 numerical unbiasedness 的一般定理。

## 十八、算法框架：一个可审计的 CNF 程序

```text
Inputs:
    data x1 or base sample z0
    vector field f_theta(t, z; context)
    time interval [t0, t1]
    exact or stochastic divergence policy
    solver, atol/rtol/max_step, precision

RHS(t, [z, ell], probe):
    velocity = f_theta(t, z)
    if exact:
        divergence = trace(d velocity / d z)
    else:
        # probe is constant with respect to z
        divergence = probe^T (d velocity / d z) probe
    return [velocity, -divergence]

Sampling:
    z0 ~ p0
    integrate RHS from t0 to t1
    return z1; optionally ell1

Likelihood:
    set z(t1)=x1
    integrate augmented dynamics to t0 with consistent signs
    return log p0(z0) - integral_{t0}^{t1} divergence dt

Audit:
    refine tolerance/step
    compare exact trace on small dimension
    sweep probes/seeds
    log accepted/rejected steps and VJP count
    round-trip states
    finite-difference the same computed objective
```

## 十九、claim ladder：一条 CNF 结论怎样逐级升级

| 等级 | 可说什么 | 至少需要 |
|---|---|---|
| L0 formula | 写出增广 ODE | 符号和对象一致 |
| L1 local theorem | 在局部条件下有可微流和 Liouville | regularity、存在区间、定义域 |
| L2 numerical reproduction | 实现复现解析/高精 reference | refinement、state/logp双误差 |
| L3 stochastic trace evidence | estimator均值/方差符合理论 | exact trace、seed/probe sweep |
| L4 likelihood evidence | held-out NLL在误差门内稳定 | evaluation protocol与MC uncertainty |
| L5 generative evidence | sample quality/coverage在预算下可靠 | 多指标、同等计算预算、失败样本 |
| L6 general claim | 跨数据/架构/solver可迁移 | 多设置、理论边界与独立复核 |

“模型能运行”通常只在 L1—L2；不能直接写成“可扩展、可逆且 likelihood 精确”。

## 二十、最小掌握检查

### 概念检查

1. 为什么非自治系统要写 $\phi_{s,t}$ 而不是只写 $\phi_t$？
2. no crossing 的证明到底用了 existence 还是 uniqueness？
3. $x'=-x^3$ 为什么处处 $J>0$ 却不是 $\mathbb R\to\mathbb R$ 双射？
4. 为什么 divergence 是 local volume rate，而不是最大拉伸率？
5. 沿轨迹的 $d\log p_t(x_t)/dt$ 与 $\partial_t\log p_t(x)$ 有何差别？
6. Hutchinson 的无偏性需要什么二阶矩条件？
7. Rademacher variance 为什么不含 diagonal？
8. 一次 solve 内重新采样 probe 会改变什么程序对象？

### 推导检查

应能闭卷写出：

$$
\dot J=D_xf\,J,
\qquad J(s)=I,
$$

$$
\frac d{dt}\log\det J
=\operatorname{tr}(J^{-1}\dot J)
=\operatorname{tr}D_xf,
$$

$$
\frac d{dt}\log p_t(x_t)
=-\operatorname{tr}D_xf(t,x_t),
$$

以及

$$
\mathbb E[\varepsilon^TA\varepsilon]=\operatorname{tr}A.
$$

### 实现检查

应能在小维系统中同时完成：

- 用 exact flow/analytic Jacobian 验证 Liouville；
- 同步积分 state 与 log-density 并做阶数/容差 refinement；
- 枚举 Rademacher probes 验证均值和 variance；
- 对 exact/stochastic divergence 分别记录 VJP 数与误差；
- 区分 exact-flow theorem 与 finite solver behavior。

## 二十一、学习闭环与后继接口

1. 先手推线性 $x'=Ax$ 与非线性 $x'=-x^3$；
2. 完成[[习题 - 流映射、Liouville 公式与连续正规化流]]的 A—C 题；
3. 独立运行[[实验 - 流映射、Liouville 与随机迹审计]]，改矩阵、初值、步数与 probe 分布；
4. 完成 D—E 题，写一张真实 CNF paper/implementation solver card；
5. 间隔一周闭卷重推 Liouville 与 instantaneous change-of-variables；
6. 进入[[连续性方程与守恒律]]，把沿轨迹公式升级为 Eulerian PDE、control-volume 与弱形式。

> [!summary] 本章压缩
> 唯一解把逐点轨迹组织为 composition-consistent 的流；$C^1$ 初值依赖把无限小扰动组织为 $\dot J=DfJ$；Jacobi determinant formula 把矩阵演化压缩为 $d\log\det J/dt=\operatorname{div}f$；概率质量守恒再把体积变化翻成 $d\log p/dt=-\operatorname{div}f$。CNF 的数学核心只有这四步，但可信实现还必须补上全局存在/逆、support/topology、state/logp 离散误差、trace estimator 方差与 gradient-objective 一致性。

## 参考与来源

- Gerald Teschl, *Ordinary Differential Equations and Dynamical Systems*：初值依赖、自治流与动力系统标准理论。
- Chen, Rubanova, Bettencourt & Duvenaud, *Neural Ordinary Differential Equations*, NeurIPS 2018：Neural ODE、CNF 与瞬时换元原始框架。
- Grathwohl et al., *FFJORD: Free-form Continuous Dynamics for Scalable Reversible Generative Models*, ICLR 2019：Hutchinson trace estimator 在 CNF 中的可扩展使用。
- Hutchinson, *A Stochastic Estimator of the Trace of the Influence Matrix for Laplacian Smoothing Splines*, 1989：Rademacher 随机迹估计。
- Rezende & Mohamed, *Variational Inference with Normalizing Flows*, ICML 2015：离散可逆变换与变分 flow。
- Dupont, Doucet & Teh, *Augmented Neural ODEs*, NeurIPS 2019：同维 ODE flow 的拓扑表达限制与 augmentation。
- [[S-2018-Su-5776-NICE流模型]]、[[S-2022-Su-9280-硬刚扩散ODE]]、[[S-2025-Su-10958-瞬时速度与平均速度]]：中文问题入口与 AI 迁移线索。
