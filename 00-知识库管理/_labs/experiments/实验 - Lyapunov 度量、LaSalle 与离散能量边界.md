---
type: experiment
status: draft
area: [labs, math/ode, math/dynamical-systems, math/numerical-analysis]
prerequisites: ["[[Lyapunov 稳定性与能量函数]]", "[[相图、平衡点与局部稳定性]]", "[[线性 ODE 与矩阵指数]]"]
related: ["[[推导与实验 MOC]]", "[[习题 - Lyapunov 稳定性与能量函数]]", "[[Euler、Runge-Kutta 与离散化误差]]"]
sources: ["Teschl-ODE-Dynamical-Systems", "MIT-Underactuated-Lyapunov"]
code: "[[00-知识库管理/_labs/code/lyapunov_certificate_audit.py]]"
figure: "[[00-知识库管理/_assets/plots/dynamics/plot-lyapunov-metric-lasalle-discrete-v2.svg]]"
created: 2026-08-19
updated: 2026-08-23
---

# 实验 - Lyapunov 度量、LaSalle 与离散能量边界

> [!abstract] 实验结论
> 同一个实验复现了三种最容易被混淆的现象。第一，Hurwitz 非正规系统的欧氏 norm square 最多先放大到初值的 $2.1456$ 倍，但 Lyapunov equation 构造的 $P$-energy 从第一刻起严格下降。第二，阻尼振子在初值 $(q,p)=(1.5,0)$ 处满足 $\dot E(0)=0$，却有 $\dot p(0)=-1.5$，所以该点立刻离开零导数集；LaSalle 必须求 largest invariant subset。第三，连续系统 $\dot x=-x$ 始终稳定，但 explicit Euler 在 $h=2$ 处翻转：$h=0.5,1.8$ 的 energy 下降，$h=2.2$ 到第 20 步已放大 $1469.77$ 倍。

## 研究问题

能否用一个无随机性、只依赖 Python 标准库的可复现实验，同时回答：

1. $A$ Hurwitz 为什么不保证 Euclidean norm 逐时刻下降？
2. Tailored quadratic Lyapunov metric 怎样消除这种表面矛盾？
3. $\dot V(x)=0$ 为什么只是一条瞬时条件，而不等于 state 停住？
4. LaSalle 的 largest invariant subset 在数值轨道上表现为什么？
5. Continuous-time 的 $L_fV<0$ 为什么不自动迁移为 Euler map 的 $\Delta V<0$？
6. 图、解析恒等式与 machine assertions 如何形成交叉验收？

## 预注册判断

> [!hypothesis] 假设
> - Track A 的初始 Euclidean norm-square derivative 为 $3>0$，且有限时窗内 peak ratio 大于 $1.5$；
> - 同一轨道的 $V_P=x^\top Px$ 每一步采样都严格下降，矩阵方程残差为零到浮点精度；
> - Track B 在 $t=0$ 有 $\dot E=0$ 但 $\dot p\ne0$，轨道最终靠近原点；
> - 阻尼振子的 RK4 sampled energy 不出现超过 $10^{-12}$ 的上跳；
> - Track C 在 $k=20$ 时，$h=0.5,1.8$ 的 energy ratio 小于 $1$，而 $h=2.2$ 的 ratio 大于 $1$；
> - 所有 assertions 必须由脚本自动执行，图只负责解释而不负责替代判据。

## Track A：非正规系统与 tailored metric

### A.1 系统

考虑

$$
\dot x=Ax,
\qquad
A=
\begin{pmatrix}
-1&6\\
0&-2
\end{pmatrix},
\qquad
x_0=\frac1{\sqrt2}
\begin{pmatrix}1\\1\end{pmatrix}.
$$

$A$ upper triangular，故

$$
\sigma(A)=\{-1,-2\}.
$$

它是 Hurwitz matrix，所有解最终 exponential decay。

### A.2 Exact trajectory

由 triangular matrix exponential，

$$
e^{At}
=
\begin{pmatrix}
e^{-t}&6(e^{-t}-e^{-2t})\\
0&e^{-2t}
\end{pmatrix}.
$$

所以

$$
x_1(t)
=\frac1{\sqrt2}
\left(7e^{-t}-6e^{-2t}\right),
\qquad
x_2(t)
=\frac1{\sqrt2}e^{-2t}.
$$

本 track 不需要 numerical integrator；曲线直接由 exact expression 采样。

### A.3 Euclidean energy 的暂态增长

令

$$
W(x)=\|x\|_2^2.
$$

则

$$
\dot W=x^\top(A+A^\top)x.
$$

对选定 $x_0$，

$$
A+A^\top
=
\begin{pmatrix}
-2&6\\
6&-4
\end{pmatrix},
$$

于是

$$
\dot W(0)
=\frac12(-2+6+6-4)
=3>0.
$$

这并不否定 asymptotic stability；它只否定“Euclidean norm 必须单调下降”。

### A.4 Lyapunov equation 的定制度量

取 $Q=I$，解

$$
A^\top P+PA=-I.
$$

得到

$$
P=
\begin{pmatrix}
\frac12&1\\
1&\frac{13}{4}
\end{pmatrix}.
$$

由于

$$
P_{11}=\frac12>0,
\qquad
\det P=\frac58>0,
$$

有 $P\succ0$。定义

$$
V_P(x)=x^\top Px,
$$

则

$$
\dot V_P
=x^\top(A^\top P+PA)x
=-\|x\|_2^2<0
$$

对每个 $x\ne0$ 成立。

因此：

$$
\text{Euclidean norm transient growth}
\quad\not\Rightarrow\quad
\text{instability}.
$$

真正的稳定证书是“存在一个与 dynamics 相配的 positive-definite metric”，而不是“任意预选 norm 都逐时刻下降”。

### A.5 测量

| 量 | 定义 |
|---|---|
| Euclidean curve | $\|x(t)\|^2/\|x_0\|^2$ |
| Lyapunov curve | $V_P(x(t))/V_P(x_0)$ |
| peak transient | $\max_{0\le t\le5}\|x(t)\|^2/\|x_0\|^2$ |
| monotonicity audit | $\max_k[V_P(t_{k+1})-V_P(t_k)]$ |
| algebra audit | $\|A^\top P+PA+I\|_{\max}$ |

## Track B：LaSalle 的零导数集不是静止点集

### B.1 阻尼振子

取

$$
\dot q=p,
\qquad
\dot p=-q-0.4p,
\qquad
(q(0),p(0))=(1.5,0).
$$

物理能量

$$
E(q,p)=\frac12(q^2+p^2)
$$

满足

$$
\dot E
=q\dot q+p\dot p
=-0.4p^2\le0.
$$

### B.2 瞬时零导数不等于保持不变

在 $t=0$，

$$
p(0)=0
\quad\Longrightarrow\quad
\dot E(0)=0.
$$

但

$$
\dot p(0)=-q(0)-0.4p(0)=-1.5.
$$

所以轨道立即获得非零 velocity，并离开

$$
Z=\{(q,p):p=0\}.
$$

要一直留在 $Z$ 中，必须同时有

$$
p=0,\qquad \dot p=-q=0.
$$

故 largest invariant subset 为

$$
M=\{(0,0)\}.
$$

图中橙色虚线画的是 normalized dissipation $0.4p^2/E(0)$。它在初始时刻和以后多次穿过零，并不妨碍蓝色 energy curve 整体下降；只有当整条轨道永久留在零耗散集合中，才属于 $M$。

### B.3 Numerical contract

| 项目 | 值 |
|---|---|
| solver | fixed-step classical RK4 |
| step | $0.002$ |
| horizon | $20$ |
| initial state | $(1.5,0)$ |
| displayed sampling | 每 10 个 solver steps |
| monotonicity acceptance | maximum one-step energy increase $\le10^{-12}$ |
| endpoint acceptance | $\|(q(20),p(20))\|<0.05$ |

Numerical monotonicity 不是 LaSalle theorem 的证明；它用于检查实现与解析机制是否一致。正式结论仍来自 compact sublevel、invariance 与 largest invariant subset。

## Track C：Continuous derivative 与 discrete difference

### C.1 连续系统

取

$$
\dot x=-x,
\qquad
V(x)=\frac12x^2.
$$

则

$$
\dot V=-x^2=-2V,
$$

所以

$$
V(t)=e^{-2t}V(0).
$$

### C.2 Explicit Euler

Euler update 为

$$
x_{k+1}
=x_k+h(-x_k)
=(1-h)x_k.
$$

离散 energy difference 为

$$
\begin{aligned}
\Delta V
&=V(x_{k+1})-V(x_k)\\
&=\frac12\left((1-h)^2-1\right)x_k^2\\
&=\frac12h(h-2)x_k^2.
\end{aligned}
$$

所以：

$$
\Delta V<0
\iff0<h<2;
$$

$$
\Delta V=0
\iff h=0\ \text{或}\ h=2;
$$

$$
\Delta V>0
\iff h>2.
$$

$h=2$ 时 multiplier 为 $-1$，state 等幅换号；它不是 asymptotically stable。图用

$$
\log_{10}\frac{V_k}{V_0}
$$

显示 $h=0.5,1.8,2.2$ 的 20 步行为。

### C.3 与 AI 系统的对应

这一标量例子直接对应：

- Neural ODE 的 vector field certificate；
- 把 continuous model 部署为 fixed-step residual block；
- 把 gradient flow 离散为 gradient descent；
- 用 solver tolerance/step policy 产生实际 update map。

在每种情况下，continuous claim 与 discrete claim 都必须分开写。步长不是实现细节，而是 theorem object 的一部分。

## 环境与复现

| 项目 | 值 |
|---|---|
| Python | 3.9.6 |
| 第三方依赖 | 无；只使用标准库 |
| 随机性 | 无 |
| Track A | exact matrix-exponential expression |
| Track B | 手写 fixed-step RK4 |
| Track C | exact Euler recurrence |
| 图格式 | 脚本直接生成 self-contained SVG |
| code SHA-256 | 257ef09bb88b8a2af906fa9fad034940d1bce79ab3cf0456412b184d2db4539f |
| SVG SHA-256 | 71f8a80cca7af02ee8d98b2b0f1e0a1dae98a20a075dc9c0effdbd0bc1744f23 |

复现命令：

~~~bash
python3 "00-知识库管理/_labs/code/lyapunov_certificate_audit.py"
~~~

代码：[lyapunov_certificate_audit.py](../code/lyapunov_certificate_audit.py)

## 结果

先看图回答：欧氏范数暂态增长、定制 Lyapunov 度量下降、LaSalle 最大不变集与 Euler 离散能量分别证明什么？

![[00-知识库管理/_assets/plots/dynamics/plot-lyapunov-metric-lasalle-discrete-v2.svg|880]]

> [!figure] 实验图｜Lyapunov 度量、LaSalle 不变集与离散步长边界
> A 展示非正规稳定系统中欧氏量先增，而解 Lyapunov 方程得到的 $P$-能量严格降；B 比较阻尼振子的能量与 $\dot E=0$ 集合；C 对同一连续稳定系统扫描 Euler 步长导致的能量衰减或发散。生成脚本：[[lyapunov_certificate_audit.py]]；解析/确定性构造，并对方程残差、单调性、不变集和步长阈值设断言。

**怎样读图。** A 说明证书依赖 metric；B 中某时刻 $\dot E=0$ 不等于轨道停留，必须求该集合内最大不变子集；C 把连续导数符号与一步差分符号分开，读取 $0<h<2$ 的严格下降区。

**适用边界（图没有证明什么）。** 只覆盖线性非正规系统、一个阻尼振子与显式 Euler；图不证明任意候选能量函数都可找到，也不把连续 Lyapunov 证书自动转化为任意离散优化器的稳定证书。

> [!question] 本实验的判别问题
> 为什么稳定性必须绑定所选度量、最大不变集和离散时间映射，而不能只看欧氏范数或连续能量导数？

### Track A

| 指标 | 结果 |
|---|---:|
| $\dot{\|x\|^2}(0)$ | $3.0$ |
| peak Euclidean norm-square ratio | $2.1456129255$ |
| $t=5$ Euclidean ratio | $0.0010994885$ |
| $t=5$ $P$-energy ratio | $0.0001919569$ |
| maximum sampled $P$-energy increment | $-1.10058\times10^{-6}$ |
| Lyapunov equation max-entry residual | $0$ |

Peak ratio 大于 $2$，表明 transient 并非肉眼噪声；而 maximum increment 仍为负，表明采样到的 $P$-energy 每一步都下降。解析恒等式

$$
\dot V_P=-\|x\|^2
$$

进一步把 finite samples 升级为 exact continuous statement。

### Track B

| 指标 | 结果 |
|---|---:|
| $\dot E(0)$ | $0$ |
| $\dot p(0)$ | $-1.5$ |
| $\|(q(20),p(20))\|$ | $0.0306168160$ |
| final / initial energy | $0.0004166175$ |
| maximum RK4 one-step energy increment | $-7.36373\times10^{-13}$ |

初始零导数与非零 acceleration 同时出现，直接展示 $Z\ne M$。终点接近原点与 LaSalle 结论一致，但不是独立证明 global convergence。

### Track C

| step size | multiplier $1-h$ | $V_{20}/V_0$ | 结论 |
|---:|---:|---:|---|
| $0.5$ | $0.5$ | $9.09495\times10^{-13}$ | monotone decay |
| $1.8$ | $-0.8$ | $1.32923\times10^{-4}$ | sign oscillation，energy decay |
| $2.2$ | $-1.2$ | $1469.771568$ | energy growth |

三条 curves 来自同一个 continuous ODE。差异完全由 update map 的 step size 造成。

### Machine acceptance

脚本执行了以下核心 assertions：

~~~text
nonnormal_initial_norm_sq_derivative > 0
nonnormal_peak_norm_sq_ratio > 1.5
p_energy_max_step_increase < 0
lyapunov_equation_max_residual < 1e-14
oscillator_initial_energy_derivative == 0
oscillator_initial_p_derivative != 0
oscillator_max_step_energy_increase <= 1e-12
oscillator_final_norm < 0.05
Euler h=0.5,1.8 decrease; h=2.2 grows
~~~

全部通过。

## 三种现象的统一解释

### Metric 不是唯一的

稳定性是 dynamics 的性质；某个候选 $V$ 是否下降则是 dynamics 与 scalar geometry 的配对性质。Euclidean energy 失败，并不意味着不存在别的证书。

### Zero derivative 不是 zero vector field

$$
\dot V(x)=0
$$

只表示 vector field 在该点与 $V$ 的 gradient 正交，或 gradient 本身退化。它没有说

$$
f(x)=0.
$$

因此 LaSalle 必须从 zero-derivative set 中继续筛出 invariant motions。

### Discretization 改变演化对象

Continuous flow 是一族 maps $\varphi_t$；Euler 是另一个 map $F_h$。两者在 $h\to0$ 时局部相近，但 fixed finite $h$ 下需要不同 inequality：

$$
L_fV<0
\quad\text{vs}\quad
V(F_h(x))-V(x)<0.
$$

## 结论边界

本实验支持：

- 指定非正规 $2\times2$ system 与指定初值上的 Euclidean transient；
- 指定 $P,Q$ 的 exact Lyapunov equation identity；
- 指定阻尼振子、初值和 RK4 配置下的 numerical behavior；
- 阻尼振子 zero-derivative set 与 largest invariant subset 的解析区分；
- 标量 Euler map 对任意 state 的 exact step-size boundary。

本实验不支持：

- 任意 Hurwitz matrix 都有相同 transient factor；
- 数值曲线单独证明 LaSalle theorem；
- RK4 对任意步长都 energy diminishing；
- continuous Lyapunov function 自动适用于任意 integrator；
- AI 模型的 sample loss、task accuracy 或 deployment robustness；
- 从 regional certificate 推断 global basin。

## 失败判据与扩展

若发生以下任一项，应视为复现失败：

1. Lyapunov equation residual 超过 $10^{-14}$；
2. $P$-energy sampled increment 非负；
3. oscillator energy 上跳超过 $10^{-12}$；
4. $h=2.2$ 的 Euler energy 没有增长；
5. SVG 无法由标准 renderer 打开；
6. hash 改变但没有同步代码、图与记录。

可进一步扩展：

- 扫描 nonnormal coupling $K$，研究 peak transient 与 $\kappa(P)$；
- 对阻尼振子比较 physical energy 与带交叉项的 strict certificate；
- 比较 Euler、RK4、implicit Euler 的 discrete Lyapunov regions；
- 为 learned vector field 加入 finite sample violation 与 interval verifier；
- 在 DYN-05 中把 step-size boundary 推广为 absolute stability region。

## 复现记录

| 日期 | 环境 | 结果 | 状态 |
|---|---|---|---|
| 2026-08-19 | Python 3.9.6，standard library；SVG 经 Sharp rasterize 后目检 | 三 tracks 的全部 assertions 通过；机制与解析式一致 | reproduced-once |

> [!warning] 状态语义
> reproduced-once 只表示当前机器成功执行并目检一次。配套习题与详解仍是 draft / not-attempted；读者完成独立推导与盲测前，不升级掌握状态。
