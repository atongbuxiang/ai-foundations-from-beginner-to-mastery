---
type: concept
status: draft
area: [math/ode, math/numerical-analysis, ai/neural-ode, ai/generative-modeling]
aliases: [Euler 方法, Runge-Kutta 方法, ODE 数值积分, 一步法, local truncation error, adaptive ODE solver]
prerequisites: ["[[常微分方程、初值问题与解的存在唯一性]]", "[[Taylor 展开与余项]]", "[[误差传播、条件估计与停止准则]]", "[[Lyapunov 稳定性与能量函数]]"]
related: ["[[ODE、动力系统与 SDE MOC]]", "[[线性 ODE 与矩阵指数]]", "[[刚性系统、绝对稳定域与隐式方法]]", "[[自动微分：前向、反向与高阶模式]]", "[[一阶最优性条件与梯度下降]]", "[[实验 - ODE 阶数、自适应步长与离散梯度审计]]"]
sources: ["MIT-18.330-2012-ODE-Numerics", "Hairer-Norsett-Wanner-Solving-ODE-I", "SciPy-solve_ivp", "Chen-et-al-2018-Neural-ODE", "Zhuang-et-al-2020-Adaptive-Checkpoint-Adjoint", "Su-6261-Optimization-Dynamics-Global", "Su-10958-Instant-Average-Velocity"]
created: 2026-08-19
updated: 2026-08-27
---

# Euler、Runge–Kutta 与离散化误差

> [!abstract] 本章主问题
> ODE solver 不是把导数公式“照着算很多次”，而是在有限步长上近似 exact flow。若一步 exact-start defect 为 $O(h^{p+1})$，且数值一步映射对 state perturbation 稳定，那么固定时窗内约 $O(1/h)$ 个局部误差累积为 $O(h^p)$ global error。Euler 用一个起点斜率得到一阶，Heun/explicit midpoint 用两个 stage 达到二阶，classical RK4 用四个 stage 达到四阶；adaptive solver 再用共享 stages 的 embedded pair 估计局部误差并调整步长。Order、absolute stability、floating-point behavior、global accuracy 与可微训练梯度是五张不同的账。

> [!important] 与相邻章节的分工
> [[常微分方程、初值问题与解的存在唯一性]]负责 exact IVP 是否定义良好；[[误差传播、条件估计与停止准则]]提供通用误差账本；本章负责 nonstiff one-step methods 的构造、阶数、有限时 convergence、自适应控制与 differentiation。[[刚性系统、绝对稳定域与隐式方法]]将系统研究 stiff modes、A/L-stability、implicit solve 与完整稳定域；本章只建立必要的 test-equation 预览。

## 学习目标

完成本章后，你应当能够：

1. 区分 exact solution、exact flow、numerical grid values 与 dense output；
2. 从 Volterra integral equation 推出一步法；
3. 用 forward difference、Taylor expansion 与左矩形 quadrature 三种方式解释 Euler；
4. 定义 one-step map、increment function、local defect、normalized truncation error 与 global error；
5. 解释 local $O(h^{p+1})$ 为什么通常只给 global $O(h^p)$；
6. 用 discrete Grönwall 完成 one-step convergence proof；
7. 推导 Euler 的 local defect 主项 $\frac12h^2(f_t+f_yf)$；
8. 推导 Heun 与 explicit midpoint 的二阶条件；
9. 读写 explicit Runge–Kutta 的 Butcher tableau；
10. 从 Taylor matching 推出一、二阶 RK order conditions；
11. 正确写出 classical RK4 的四个 stages 与加权更新；
12. 解释高阶、NFE、memory、低存储与 FSAL 的成本差异；
13. 用 step doubling / Richardson 做误差估计与外推；
14. 解释 embedded RK pair 怎样共享 stages；
15. 构造 atol–rtol weighted error norm；
16. 推导 adaptive step controller 的指数；
17. 区分 tolerance、local error estimate 与 global error guarantee；
18. 解释 rejected step、PI controller、max step 与 event detection；
19. 审计 dense output、discontinuity、positivity 与 invariant preservation；
20. 分析 truncation–roundoff trade-off；
21. 写出 variable-step global error bound；
22. 由 test equation 推出 Euler、Heun 与 RK4 的 stability function；
23. 区分 finite-horizon perturbation stability 与 absolute stability；
24. 判断 ResNet 何时只是 Euler-like、何时形成 refinement family；
25. 区分 ideal continuous objective 与 computed discrete objective；
26. 推导 Euler solver 的 discrete adjoint；
27. 推导 continuous adjoint equation并解释数值重积分误差；
28. 审计 Neural ODE 的 tolerance、NFE、checkpoint 与 gradient contract；
29. 解释 finite-NFE velocity 与 instantaneous vector field 的差别；
30. 设计一份可复现、不可越界的 ODE solver 报告。

> [!question] 初学者读完必须能回答
> 1. Exact flow、grid state、dense output 与 accepted path 分别是什么？
> 2. 为什么 local defect $O(h^{p+1})$ 通常只给 global error $O(h^p)$？
> 3. Discrete Grönwall 在 local-to-global 证明中控制哪一种放大？
> 4. Runge–Kutta stage 为什么不是“在同一步反复套 Euler”？
> 5. Embedded high/low pair、atol–rtol norm 与 step controller 怎样配合？
> 6. 为什么 tolerance 只约束局部 estimator，不是 global/task accuracy 定理？
> 7. Continuous adjoint、discrete adjoint 与 computed gradient 为什么需要分别验收？

## 机制总览

先用下图回答一个视觉问题：**一步 local defect 怎样累积成 global error，RK stages 如何构造高阶，自适应控制究竟控制哪一张误差账？**

![[00-知识库管理/_assets/figures/dynamics/fig-runge-kutta-error-adaptivity-v2.svg|880]]

> [!figure] 图 10.9.5｜Local-to-global 误差、RK stages 与 embedded adaptivity
> A 把一步 exact-start defect $O(h^{p+1})$、固定时窗约 $N\asymp1/h$ 个步和离散稳定递推连接到 global error $O(h^p)$；B 在 $[t_n,t_n+h]$ 内画出多个 stage slopes，并以 $y_{n+1}=y_n+h\sum_i b_i k_i$ 表示 order-condition 加权；C 从共享 stages 的 high/low update 得到 scaled error norm，再执行 accept/reject 与 $h$ 更新，并把 state、event、dense output 与 gradient 另行列账。来源：独立绘制；理论接口参考 one-step convergence、Runge–Kutta order conditions 与 embedded adaptivity；生成脚本：[[plot_dynamics_numerics_transport_v2.py]]；确定性机制图，无随机种子。

**怎样读图。** A 先从误差递推 $e_{n+1}\le(1+Lh)e_n+Ch^{p+1}$ 读起，consistency 给局部项，stability/Gronwall 控制传播；B 再把 RK 看成同一步内对 vector field 的结构化多点查询，而不是把 Euler 当作黑箱重复；C 最后用 atol/rtol 定义 componentwise scale，读取局部 embedded difference，接受或拒绝后再检查 true global state error、events、NFE 和梯度一致性。

**适用边界（图没有证明什么）。** 图假设适合一步法的光滑 nonstiff 问题，不给 discontinuity、event、DAE 或 stiffness 下的完整结论。Embedded difference 不是 exact local error，controller 公式还受 safety factor、PI history 与 order convention 影响。小 tolerance 不保证全局任务损失、守恒、positivity 或 continuous-adjoint gradient 自动准确。

> [!note] 课程位置
> DYN-01—04 研究的是精确连续系统：解是否存在、传播子怎样写、轨道是否稳定、能量怎样下降。本章第一次承认计算机不能直接存取整条 exact flow，只能用有限次 vector-field evaluation 构造离散一步映射。核心任务不是背 Euler/RK 系数，而是建立“精确一步—数值一步—局部缺陷—误差传播—全局误差”的完整账本；DYN-06 随后会说明，高阶和收敛并不足以处理 stiff mode。

> [!tip] 建议两遍阅读
> **第一遍**只计算 $y'=-y$：写出 Euler、Heun、RK4 的 stability polynomial，在 $h=1/2$ 上走两步，并用步长减半观察误差斜率。**第二遍**再进入一般 one-step convergence、RK order conditions、embedded pair、自适应控制、dense output、roundoff 与 continuous/discrete adjoint。第一遍的目标是能逐项回答“误差从哪一步产生、怎样传播、为何少一阶”，而不是先记住几十个 solver 名称。

## 本章的推导问题链

1. Exact solution 满足积分方程，为什么数值方法可以理解成对一步轨迹积分的近似？
2. Exact flow、numerical one-step map、stage state、grid state 与 dense output 分别是什么对象？
3. 从 exact state 起步后的一步偏差为什么叫 local defect，它与 global grid error 为什么不能混用？
4. Euler、Heun 与 RK4 怎样通过更多 stage/更精确的 Taylor matching 提高 local order？
5. 为什么 $N\asymp1/h$ 个 $O(h^{p+1})$ local defects 在稳定传播后通常形成 $O(h^p)$ global error？
6. 怎样通过 step halving 的误差比估计 observed order，而不把偶然的小误差当作高阶？
7. 为什么高 order、absolute stability、自适应 tolerance、浮点可靠性和 gradient accuracy 必须分成五张账？

## 贯穿算例：同一条衰减曲线上的三种离散传播子

取最小线性问题

$$
y'=-y,
\qquad y(0)=1,
\qquad 0\le t\le1.
$$

精确解为 $y(t)=e^{-t}$。它没有刚性、事件或非线性求解，因而所有误差都可以明确归因于时间离散本身。

### 符号与对象账本

| 对象 | 类型 | 本例中的值/作用 | 不可直接称为 |
|---|---|---|---|
| $\Phi_h$ | exact one-step flow | $\Phi_h(y)=e^{-h}y$ | 数值更新公式 |
| $F_h$ | numerical one-step map | $F_h(y)=R(-h)y$ | exact flow |
| $R(z)$ | stability function/polynomial | 方法作用于 $y'=\lambda y$ 后的放大因子 | 一般非线性系统的完整稳定性定理 |
| $d_{n+1}$ | exact-start local defect | $\Phi_h(y(t_n))-F_h(y(t_n))$ | 已传播到终点的 global error |
| $e_n$ | global grid error | $y(t_n)-y_n$ | embedded local estimator |
| $p$ | global order | Euler/Heun/RK4 分别为 $1,2,4$ | 单次实验自动证明的阶数 |
| NFE | vector-field evaluation count | 每固定步通常为 $1,2,4$ | 总 wall time 或精度的充分统计量 |

### 第一步：把三个方法都压成一个标量放大因子

对 $y'=\lambda y$ 令 $z=h\lambda$。三种方法的一步更新分别是

$$
\begin{aligned}
R_E(z)&=1+z,\\
R_H(z)&=1+z+\frac{z^2}{2},\\
R_4(z)&=1+z+\frac{z^2}{2}+\frac{z^3}{6}+\frac{z^4}{24}.
\end{aligned}
$$

本例 $\lambda=-1$，所以 $z=-h$。这些多项式正好是 $e^z$ 在原点的不同阶截断，但这个巧合只直接适用于线性 test equation；一般非线性 RK order 仍要匹配 rooted-tree/Taylor 条件。

### 第二步：先看一步 local defect

若本步从精确值 $y(t_n)$ 起步，

$$
\boxed{
d_{n+1}
=\bigl[e^{-h}-R(-h)\bigr]y(t_n).
}
$$

在 $h=1/2$ 时，括号中的三个系数为

| 方法 | $e^{-h}-R(-h)$ | 首个未匹配项 | local defect 阶 |
|---|---:|---:|---:|
| Euler | $0.106530660$ | $h^2/2$ | $O(h^2)$ |
| Heun | $-0.018469340$ | $-h^3/6$ | $O(h^3)$ |
| RK4 | $-0.000240174$ | $-h^5/120$ | $O(h^5)$ |

符号只表示数值一步落在精确终点的哪一侧；order 由 $h\to0$ 时的幂决定，不能由一次误差正负决定。

### 第三步：固定 $T=1$ 走两步

当 $h=1/2$、$N=2$ 时，

$$
y_N=R(-1/2)^2,
\qquad y(1)=e^{-1}\approx0.367879441.
$$

| 方法 | 一步因子 $R(-1/2)$ | 两步结果 $y_2$ | 终点绝对误差 |
|---|---:|---:|---:|
| Euler | $0.5$ | $0.25$ | $0.117879441$ |
| Heun | $0.625$ | $0.390625$ | $0.022745559$ |
| RK4 | $0.606770833$ | $0.368170844$ | $0.000291403$ |

这张表展示的是同一固定步长上的误差，不是“RK4 在任何成本预算下永远最好”。RK4 每步调用四次 $f$，还可能受 stability、memory、event 和硬件实现限制。

### 第四步：用步长减半观察 global order

定义终点误差

$$
E(h)=\left|e^{-1}-R(-h)^{1/h}\right|,
$$

这里仅取 $1/h$ 为整数。若 $E(h)\approx Ch^p$，则

$$
p_{\rm obs}(h)=\log_2\frac{E(h)}{E(h/2)}\longrightarrow p.
$$

| 方法 | $E(1/2)$ | $E(1/4)$ | $E(1/8)$ | 两次 $p_{\rm obs}$ |
|---|---:|---:|---:|---:|
| Euler | $1.1788\times10^{-1}$ | $5.1473\times10^{-2}$ | $2.4271\times10^{-2}$ | $1.195,\ 1.085$ |
| Heun | $2.2746\times10^{-2}$ | $4.6496\times10^{-3}$ | $1.0538\times10^{-3}$ | $2.290,\ 2.141$ |
| RK4 | $2.9140\times10^{-4}$ | $1.4758\times10^{-5}$ | $8.3075\times10^{-7}$ | $4.303,\ 4.151$ |

Observed order 尚未恰好等于整数，是因为高阶余项仍存在；继续减半时才逐渐进入 asymptotic regime。步长过小时，roundoff 又会破坏斜率，所以“越小越好”也有边界。

## 核心公式七问：local defect 怎样变成 global error

对一般一步映射 $F_h$，把 $e_n=y(t_n)-y_n$ 插入并加减 $F_h(t_n,y(t_n))$：

$$
\boxed{
e_{n+1}
=\underbrace{\Phi_h(t_n,y(t_n))-F_h(t_n,y(t_n))}_{d_{n+1}}
+\underbrace{F_h(t_n,y(t_n))-F_h(t_n,y_n)}_{\text{旧误差的传播}}.
}
$$

若 $\|d_{n+1}\|\le C_dh^{p+1}$ 且 $F_h$ 对 state 满足 $\|F_h(u)-F_h(v)\|\le(1+Lh)\|u-v\|$，离散 Grönwall 给固定时窗上的 $\max_n\|e_n\|=O(h^p)$。

1. **解决什么问题？** 把“每一步从精确起点有多准”升级为“真实数值递推走很多步后有多准”。
2. **对象与形状？** $e_n,d_{n+1}\in\mathbb R^d$；$\Phi_h,F_h:\mathbb R^d\to\mathbb R^d$；范数和常数必须在同一状态空间与时间区间声明。
3. **从哪里来？** 对 exact update 和 numerical update 相减，再加减从 exact state 启动的 numerical update。
4. **需要什么条件？** Local consistency、一步映射的 perturbation stability、有限时间窗和足够 regularity；variable step 还要控制 $h_{\max}$ 与步长序列。
5. **怎样检查？** 分别做 one-step defect 测试与 fixed-$T$ step-halving；后者的 log-log slope 才对应 global order。
6. **怎样误读？** $N\times O(h^{p+1})$ 只是直觉，若旧误差被强烈放大就不能直接相加；adaptive estimator 小也不是 global/task error 定理。
7. **AI 中怎样调用？** Neural ODE 和 flow model 必须同时报告 tolerance、accepted steps/NFE、状态误差代理及 discrete/continuous gradient 审计；不能只写 solver 名称。

> [!success] 第一遍停靠线
> 合上正文后，应能从 $y'=-y$ 独立写出三个 $R(z)$，在 $h=1/2$ 上算出两步结果，并解释为什么 Euler/Heun/RK4 的 local defect 分别是 $O(h^2),O(h^3),O(h^5)$，global order 却是 $1,2,4$。若只能背“RK4 四阶”而无法写误差递推，请先不要进入 adaptive solver 与 adjoint 部分。

## 一、首先固定“求解的对象”

考虑 nonautonomous IVP

$$
\dot y(t)=f(t,y(t)),
\qquad
y(t_0)=y_0,
\qquad
y(t)\in\mathbb R^d.
$$

在网格

$$
t_0<t_1<\cdots<t_N=T,
\qquad
h_n=t_{n+1}-t_n
$$

上，至少有四个不同对象。

| 对象 | 记号 | 含义 |
|---|---|---|
| exact trajectory | $y(t)$ | IVP 的精确解 |
| exact flow step | $\Phi_{t_{n+1},t_n}$ | 把 exact state 从 $t_n$ 送到 $t_{n+1}$ |
| numerical grid state | $y_n$ | 算法在 $t_n$ 返回的近似 |
| dense output | $\widetilde y(t)$ | 在 accepted grid points 之间构造的插值近似 |

正确的数值目标是

$$
y_n\approx y(t_n),
$$

而不是让数组“看起来平滑”。如果 solver 还要定位 event、计算 integral loss 或反向传播，中间的 dense output 与 stage states 也成为算法合同的一部分。

## 二、从积分方程看一步传播

Exact solution满足

$$
y(t_{n+1})
=y(t_n)
+\int_{t_n}^{t_{n+1}}f(s,y(s))\,ds.
$$

因此一步数值方法的本质是近似 unknown integral：

$$
\int_{t_n}^{t_{n+1}}f(s,y(s))\,ds.
$$

困难有两层：

1. integrand 随 time 变化；
2. integrand 还依赖未知 trajectory $y(s)$。

Runge–Kutta 方法用若干 internal stage states 预测同一步内的 trajectory位置，再对相应 slopes 做 quadrature-like 加权。这个视角比“背系数表”更接近方法本质。

## 三、Forward Euler 的三种推导

### 3.1 Forward difference

用

$$
\dot y(t_n)
\approx
\frac{y(t_{n+1})-y(t_n)}{h_n},
$$

再代入 $\dot y=f(t,y)$：

$$
y_{n+1}
=y_n+h_nf(t_n,y_n).
$$

### 3.2 Taylor expansion

若 exact solution足够光滑，

$$
y(t_n+h)
=y(t_n)+h\dot y(t_n)+O(h^2).
$$

代入 $\dot y=f(t,y)$ 并把 exact state 替成 current numerical state：

$$
y_{n+1}=y_n+hf(t_n,y_n).
$$

### 3.3 Left-rectangle quadrature

把 exact integral近似为

$$
\int_{t_n}^{t_n+h}f(s,y(s))\,ds
\approx
h f(t_n,y(t_n)).
$$

这给出同一公式。三种推导分别强调 derivative approximation、Taylor truncation 与 trajectory integral。

### 3.4 几何意义

Euler 沿起点 tangent vector走一条直线：

$$
y_n
\longmapsto
y_n+h f(t_n,y_n).
$$

真正轨迹会在步内弯曲。步长越大，忽略 curvature 的代价通常越大；但“减小 $h$”能否修复问题还取决于 regularity、stability 与 floating point。

## 四、一般 one-step method

写成

$$
y_{n+1}
=y_n+h_n\Psi(t_n,y_n,h_n),
$$

其中 $\Psi$ 称 increment function。也可把整步写成

$$
y_{n+1}=F_{h_n}(t_n,y_n).
$$

Forward Euler对应

$$
\Psi(t,y,h)=f(t,y).
$$

One-step 的意思是 $y_{n+1}$ 只依赖当前 $y_n$ 与本步信息；它可以在内部有许多 stages。Multistep methods会显式依赖 $y_{n-1},y_{n-2},\ldots$，其 zero-stability 需要单独理论，本章不展开。

## 五、三种“局部误差”约定必须先声明

文献对 local truncation error 的归一化并不统一。本章固定以下记号。

### 5.1 Exact-start one-step defect

$$
d_{n+1}
=y(t_{n+1})-y(t_n)
-h_n\Psi(t_n,y(t_n),h_n).
$$

它问：

> 如果本步从 exact state 起步，走完一步后偏离 exact endpoint 多远？

Order-$p$ one-step method满足

$$
\|d_{n+1}\|
\le C h_n^{p+1}.
$$

### 5.2 Normalized local truncation error

有些教材定义

$$
\tau_{n+1}
=\frac{d_{n+1}}{h_n},
$$

于是 order $p$ 写成

$$
\tau_{n+1}=O(h_n^p).
$$

看到“local error是 $O(h^p)$ 还是 $O(h^{p+1})$”时，先查有没有除以 $h$。

### 5.3 Global grid error

$$
e_n=y(t_n)-y_n.
$$

Convergence研究的是在固定 $T$ 下

$$
\max_{0\le n\le N}\|e_n\|
\to0
\qquad
(\max_n h_n\to0).
$$

通常 order-$p$ method给

$$
\max_n\|e_n\|=O(h^p).
$$

## 六、Euler 的 local defect 主项

对 vector-valued nonautonomous ODE，

$$
\ddot y
=\frac d{dt}f(t,y(t))
=f_t(t,y)+f_y(t,y)f(t,y).
$$

Taylor expansion给

$$
\begin{aligned}
y(t_n+h)
&=y(t_n)+h f(t_n,y(t_n))\\
&\quad+\frac{h^2}{2}
\left[f_t+f_yf\right]_{(t_n,y(t_n))}
+O(h^3).
\end{aligned}
$$

Euler exact-start defect因而是

$$
\boxed{
d_{n+1}
=\frac{h^2}{2}
\left[f_t+f_yf\right]_{(t_n,y(t_n))}
+O(h^3)
}.
$$

所以 Euler 是 order $1$：

$$
d_{n+1}=O(h^2),
\qquad
e_n=O(h).
$$

> [!warning] 不要漏掉 $f_t$
> 只有 autonomous system $f(y)$ 才没有 explicit time derivative。对 schedule-driven Neural ODE、diffusion ODE 与 control input，$f_t$ 往往不可忽略。

## 七、Local order 为什么少一阶变成 global order

假设 $\Psi$ 对 state uniform Lipschitz：

$$
\|\Psi(t,u,h)-\Psi(t,v,h)\|
\le L_\Psi\|u-v\|
$$

在 exact/numerical trajectories经过的region成立。由 defect定义，

$$
y(t_{n+1})
=y(t_n)+h\Psi(t_n,y(t_n),h)+d_{n+1}.
$$

减去 numerical update：

$$
e_{n+1}
=e_n
+h\left[
\Psi(t_n,y(t_n),h)-\Psi(t_n,y_n,h)
\right]
+d_{n+1}.
$$

取 norm：

$$
\|e_{n+1}\|
\le
(1+hL_\Psi)\|e_n\|
+C h^{p+1}.
$$

迭代或使用 discrete Grönwall：

$$
\begin{aligned}
\|e_n\|
&\le
(1+hL_\Psi)^n\|e_0\|\\
&\quad+
C h^{p+1}
\sum_{j=0}^{n-1}(1+hL_\Psi)^j.
\end{aligned}
$$

若 $e_0=0$ 且 $nh\le T-t_0$，

$$
(1+hL_\Psi)^n
\le e^{L_\Psi(T-t_0)}.
$$

当 $L_\Psi>0$ 时，

$$
\boxed{
\|e_n\|
\le
\frac{C}{L_\Psi}
\left(e^{L_\Psi(T-t_0)}-1\right)h^p
}.
$$

$L_\Psi=0$ 时，几何和退化为

$$
\|e_n\|
\le C(T-t_0)h^p.
$$

### 7.1 少一阶的直觉

固定时窗需要

$$
N\asymp\frac{T-t_0}{h}
$$

步。每步注入 $O(h^{p+1})$ defect，粗略相加得到

$$
\frac1hO(h^{p+1})=O(h^p).
$$

严格证明还要乘上 perturbation propagation factor；不能只数步数。

### 7.2 证明真正用了什么

- Exact solution足够光滑，保证 local defect；
- $\Psi$ 在相关region uniform Lipschitz；
- 数值轨道没有离开验证region；
- 时间区间固定；
- exact initial value 或已把 initial error单独加入；
- exact arithmetic，roundoff另算。

## 八、Consistency、convergence 与 stability

这三个词不能互换。

### Consistency

Exact-start defect在 $h\to0$ 时足够快消失：

$$
\frac{\|d_{n+1}\|}{h}\to0.
$$

### Convergence

固定时窗内 global grid error消失：

$$
\max_n\|y(t_n)-y_n\|\to0.
$$

### Finite-horizon perturbation stability

两条 numerical trajectories从 $u_0,v_0$ 出发时，

$$
\|u_n-v_n\|
\le C_T\|u_0-v_0\|,
$$

且 $C_T$ 不随 $h\to0$ 爆炸。

### Absolute stability

对 test equation

$$
y'=\lambda y
$$

研究固定 $z=h\lambda$ 下 long-time iteration是否衰减。这是 DYN-06 的主角。

> [!danger] 两种 stability
> Convergence proof中的 stability控制有限时窗内perturbation传播；absolute stability研究decaying modes在无限步迭代中是否被numerical method错误放大。名称相同，对象不同。

## 九、怎样从数据估计 observed order

若

$$
E(h)\approx C h^p,
$$

把步长减半：

$$
\frac{E(h)}{E(h/2)}
\approx2^p.
$$

Observed order为

$$
\widehat p
=\log_2\frac{E(h)}{E(h/2)}.
$$

### 9.1 何时看不到理论 slope

- $h$ 太大，尚未进入 asymptotic regime；
- $h$ 太小，roundoff或reference error主导；
- exact solution不够光滑；
- discontinuity没有对齐；
- error恰好发生 cancellation；
- 用低阶 dense output测量高阶 grid method；
- adaptive run没有可比的 refinement parameter；
- reference solution本身不够精确。

Observed slope是implementation audit，不是仅凭四个点证明一般order theorem。

## 十、Improved Euler / Heun 方法

先用 Euler预测 endpoint：

$$
k_1=f(t_n,y_n),
$$

$$
\widetilde y_{n+1}
=y_n+h k_1.
$$

再在预测endpoint取 slope：

$$
k_2
=f(t_n+h,\widetilde y_{n+1}).
$$

最后平均两端 slopes：

$$
\boxed{
y_{n+1}
=y_n+\frac h2(k_1+k_2)
}.
$$

它是 explicit trapezoidal / Heun method，不要与需要解 nonlinear equation的 implicit trapezoidal rule混淆。

### 10.1 二阶推导

在 $(t_n,y_n)$ 处展开：

$$
k_2
=f+h f_t+h f_yf+O(h^2).
$$

所以

$$
\frac12(k_1+k_2)
=f+\frac h2(f_t+f_yf)+O(h^2).
$$

更新为

$$
y_{n+1}
=y_n+h f+\frac{h^2}{2}(f_t+f_yf)+O(h^3),
$$

与 exact Taylor expansion匹配到 $h^2$，故 local defect $O(h^3)$、global error $O(h^2)$。

## 十一、Explicit midpoint 方法

先估计 midpoint state：

$$
k_1=f(t_n,y_n),
$$

$$
k_2
=f\left(
t_n+\frac h2,
y_n+\frac h2k_1
\right).
$$

用 midpoint slope走完整一步：

$$
\boxed{
y_{n+1}=y_n+h k_2
}.
$$

展开：

$$
k_2
=f+\frac h2f_t+\frac h2f_yf+O(h^2),
$$

所以同样二阶。

### 11.1 同阶不等于同方法

Heun与explicit midpoint：

- 都使用 2 次 function evaluations；
- 都有 order 2；
- 对linear test equation有相同stability polynomial；
- 但 stage locations、error constants与nonlinear behavior并不完全相同。

“阶数相同”只说明 leading asymptotic power，不说明误差常数、稳定域、结构保持或实际成本相同。

## 十二、Runge–Kutta 的一般结构

一个 $s$-stage RK method写成

$$
k_i
=f\left(
t_n+c_i h,\,
y_n+h\sum_{j=1}^{s}a_{ij}k_j
\right),
\qquad i=1,\ldots,s,
$$

$$
y_{n+1}
=y_n+h\sum_{i=1}^{s}b_i k_i.
$$

系数放入 Butcher tableau：

$$
\begin{array}{c|c}
c&A\\
\hline
&b^\top
\end{array}.
$$

若

$$
a_{ij}=0
\qquad(j\ge i),
$$

每个 stage只依赖已算出的前面 stages，方法是 explicit RK。否则 stages通常需要联立求解，属于 implicit RK，留给 DYN-06。

### 12.1 Internal consistency

通常要求

$$
c_i=\sum_{j=1}^{s}a_{ij},
$$

即

$$
c=A\mathbf1.
$$

它让 stage time与沿constant vector field走到的内部state比例一致。

## 十三、从 Taylor matching 推导 RK order conditions

为简化记号，以下假设 $c=A\mathbf1$。

### 13.1 一阶

所有 stages在 $h\to0$ 时

$$
k_i=f+O(h).
$$

所以

$$
y_{n+1}
=y_n+h\left(\sum_i b_i\right)f+O(h^2).
$$

匹配 exact $hf$ 需要

$$
\boxed{b^\top\mathbf1=1}.
$$

### 13.2 二阶

Stage expansion为

$$
k_i
=f+h c_i f_t
+h\left(\sum_j a_{ij}\right)f_yf
+O(h^2).
$$

由 $c_i=\sum_j a_{ij}$，

$$
k_i
=f+h c_i(f_t+f_yf)+O(h^2).
$$

加权后：

$$
y_{n+1}
=y_n+h(b^\top\mathbf1)f
+h^2(b^\top c)(f_t+f_yf)
+O(h^3).
$$

匹配 exact coefficient $1/2$：

$$
\boxed{
b^\top\mathbf1=1,
\qquad
b^\top c=\frac12
}.
$$

### 13.3 三、四阶条件概览

用 componentwise powers $c^2,c^3$ 与 $C=\operatorname{diag}(c)$，三阶还需

$$
b^\top c^2=\frac13,
\qquad
b^\top Ac=\frac16.
$$

四阶再需

$$
b^\top c^3=\frac14,
$$

$$
b^\top CAc=\frac18,
\qquad
b^\top A c^2=\frac1{12},
\qquad
b^\top A^2c=\frac1{24}.
$$

从高阶起，不同 elementary differentials形成 rooted trees；每棵tree对应一个order condition。Butcher theory把大量 multivariate chain-rule terms组织为组合结构。本章要求理解一、二阶推导并能核对三、四阶表，不要求初学者从零枚举所有 rooted trees。

## 十四、Classical RK4

四个 stages为

$$
k_1=f(t_n,y_n),
$$

$$
k_2
=f\left(
t_n+\frac h2,
y_n+\frac h2k_1
\right),
$$

$$
k_3
=f\left(
t_n+\frac h2,
y_n+\frac h2k_2
\right),
$$

$$
k_4
=f(t_n+h,y_n+h k_3).
$$

更新为

$$
\boxed{
y_{n+1}
=y_n+\frac h6
\left(k_1+2k_2+2k_3+k_4\right)
}.
$$

Butcher tableau：

$$
\begin{array}{c|cccc}
0&0&0&0&0\\
\frac12&\frac12&0&0&0\\
\frac12&0&\frac12&0&0\\
1&0&0&1&0\\
\hline
&\frac16&\frac13&\frac13&\frac16
\end{array}.
$$

它满足四阶条件，因此

$$
d_{n+1}=O(h^5),
\qquad
e_n=O(h^4).
$$

### 14.1 为什么权重不是 Simpson rule 的直接复制

$1,2,2,1$ 看起来像 quadrature weights，但 $k_2,k_3$ 在不同预测state上取值。RK4同时近似time quadrature与unknown trajectory；它不能只靠一维quadrature公式证明order 4。

## 十五、Order 与成本

对 explicit RK：

| 方法 | Stages / nominal NFE | Global order |
|---|---:|---:|
| Euler | 1 | 1 |
| Heun | 2 | 2 |
| explicit midpoint | 2 | 2 |
| classical RK4 | 4 | 4 |

高阶方法常允许更大 $h$ 达到同一accuracy，但每步更贵。真实成本还包括：

- rejected steps；
- event/dense-output evaluations；
- vector field内部的network cost；
- memory traffic与stage storage；
- batching/parallelism；
- backward pass与checkpoint；
- stiffness导致的稳定性限制。

### 15.1 FSAL

某些 embedded RK pairs具有 first-same-as-last 性质：本步最后一个 stage在 accepted step后可复用为下一步第一个 stage。它能节省一次 NFE，但 rejected step、event reset或vector field改变时可能不能复用。

### 15.2 Low-storage RK

一般公式似乎要保存全部 stages；特殊系数结构允许用少量工作向量递推。Low-storage改变memory schedule，不改变数学order，但 floating-point路径可能变化。

## 十六、Step doubling 与 Richardson extrapolation

设某 order-$p$ method在同一 interval上：

$$
Y_h=y(T)+C h^p+O(h^{p+1}),
$$

$$
Y_{h/2}=y(T)+C\left(\frac h2\right)^p+O(h^{p+1}).
$$

两者之差：

$$
Y_{h/2}-Y_h
=-C h^p(1-2^{-p})+O(h^{p+1}).
$$

Fine solution的leading error可估为

$$
Y_{h/2}-y(T)
\approx
-\frac{Y_{h/2}-Y_h}{2^p-1}.
$$

Richardson-corrected值：

$$
\boxed{
Y_R
=Y_{h/2}
+\frac{Y_{h/2}-Y_h}{2^p-1}
}.
$$

若 asymptotic expansion成立，它可消去 $h^p$ 主项。

### 16.1 Step-local 使用

在同一步上比较：

- 一个 full step $h$；
- 两个 half steps $h/2$。

两条路径的差可估 local error，但需要额外function evaluations。Embedded RK的目标是在同一组 stages上得到类似信息。

## 十七、Embedded Runge–Kutta pairs

共享同一组 $A,c$ 与 stages $k_i$，使用两组weights：

$$
y_{n+1}^{[p]}
=y_n+h\sum_i b_i k_i,
$$

$$
y_{n+1}^{[q]}
=y_n+h\sum_i \widehat b_i k_i,
\qquad q<p.
$$

差值

$$
\delta_{n+1}
=y_{n+1}^{[p]}-y_{n+1}^{[q]}
$$

作为 local error estimator。若 lower method order为 $q$，通常

$$
\delta_{n+1}=O(h^{q+1}).
$$

常见记号如 $5(4)$ 表示一对五阶/四阶formula；具体实现可能用高阶值前进，并用低阶估计控制误差。

> [!warning] Embedded difference不是 exact error
> 它依赖leading terms不发生异常 cancellation、solution足够smooth、stages处于适用region。Estimator需要校准和安全系数。

## 十八、atol–rtol 误差尺度

对第 $i$ 个state component，定义尺度

$$
s_i
=\operatorname{atol}_i
+\operatorname{rtol}
\max\left(
|y_{n,i}|,
|y_{n+1,i}|
\right).
$$

Weighted RMS error norm：

$$
\operatorname{err}
=
\sqrt{
\frac1d
\sum_{i=1}^{d}
\left(
\frac{\delta_i}{s_i}
\right)^2
}.
$$

典型 acceptance rule为

$$
\operatorname{err}\le1.
$$

### 18.1 两项的角色

- 当 state component接近零，atol防止分母也接近零；
- 当state幅值较大，rtol提供相对尺度。

若不同components单位或重要性差异很大，应使用componentwise atol，甚至task-specific norm。

### 18.2 RMS 的边界

RMS允许少数components超过单位尺度，只要平均仍小。Safety-critical component可能要额外检查 max norm：

$$
\max_i\frac{|\delta_i|}{s_i}.
$$

“solver通过默认 tolerance”不是物理单位无关的陈述。

## 十九、Adaptive step-size controller

若 estimator满足

$$
\operatorname{err}(h)
\approx C h^{q+1},
$$

希望新步长使 error约等于 $1$：

$$
1
\approx
\operatorname{err}(h)
\left(\frac{h_{\rm new}}h\right)^{q+1}.
$$

因此

$$
\boxed{
h_{\rm new}
=h\,
\operatorname{err}^{-1/(q+1)}
}.
$$

实际使用 safety factor与clipping：

$$
h_{\rm new}
=h\,
\operatorname{clip}
\left(
f_{\min},
f_{\max},
\eta\operatorname{err}^{-1/(q+1)}
\right),
$$

其中 $0<\eta<1$。

### 19.1 为什么需要 clipping

- Err极小时避免步长突然暴涨；
- Err极大时避免过激缩小；
- 减少accept/reject振荡；
- 保护event、discontinuity与model region。

### 19.2 Rejected step

若 $\operatorname{err}>1$：

1. 不接受candidate state；
2. 减小 $h$；
3. 从相同 $(t_n,y_n)$ 重算；
4. 记录 rejected NFE。

Rejected computation不是“没发生”，它仍消耗时间，也可能影响可微程序的control flow。

### 19.3 PI controller

只用当前 err 的 proportional controller容易振荡。PI-like controller还使用前一步accepted error：

$$
h_{n+1}
=h_n\eta
\operatorname{err}_n^{-\alpha}
\operatorname{err}_{n-1}^{\beta}.
$$

具体 $\alpha,\beta$ 依method与实现选择；不能在没有版本合同的情况下假定所有solver相同。

## 二十、Tolerance 不等于 global accuracy

Adaptive solver通常控制的是：

$$
\text{scaled local estimator}\lesssim1.
$$

它不自动给

$$
\|y_N-y(T)\|\le\operatorname{rtol}.
$$

原因包括：

1. Local errors会经 dynamics传播；
2. Estimator只是近似；
3. atol/rtol是component scaling，不是单一global norm；
4. Dense output可能是另一阶；
5. Event time有root-finding error；
6. Model error与parameter error未计入；
7. Roundoff与nondeterministic kernels未计入；
8. Chaotic/unstable flow会放大极小local defects；
9. Adaptive controller可能触及min/max step或iteration limit。

### 20.1 怎样验证 tolerance

至少做：

- tolerance sweep；
- 与更严格reference run比较；
- 报告endpoint与trajectory metrics；
- 报告accepted/rejected steps与NFE；
- 检查task metric是否也收敛；
- 对不同solver交叉验证；
- 对events单独报告time/state error。

## 二十一、Dense output 与 event detection

### 21.1 Dense output

若只保存 $(t_n,y_n)$，linear interpolation通常会降低中间时刻精度。高阶 RK solver可用stages构造 continuous extension：

$$
\widetilde y_n(t_n+\theta h),
\qquad
0\le\theta\le1.
$$

Dense-output order应单独声明；它不必等于grid update order。

### 21.2 Event

给定

$$
g(t,y(t))=0,
$$

solver常在 accepted step两端检查sign change，再用dense output定位root。

需要声明：

- terminal或nonterminal；
- crossing direction；
- root tolerance；
- simultaneous events处理；
- reset map；
- maximum step。

如果 $g$ 在一步内cross偶数次而端点同号，纯sign-change检测可能全部漏掉。限制 max step或使用问题结构才可降低风险。

## 二十二、Discontinuity 与 nonsmooth dynamics

Classical order证明依赖高阶smoothness。若 $f$、input或trajectory derivative在 $t_*$ 不光滑：

- 跨越 $t_*$ 的一步local expansion失效；
- observed order可能下降；
- adaptive estimator会频繁拒步；
- dense output可能产生伪振荡；
- continuous adjoint需要jump conditions。

最佳做法通常是把known discontinuity加入grid：

$$
t_n=t_*,
$$

在两侧分别积分，并显式应用reset/jump map。

ReLU vector field对state可Lipschitz却非 $C^1$；这足以支持uniqueness，但高阶 RK 的classical order需要轨道如何穿越activation boundaries的更细分析。

## 二十三、Numerical method 不自动保持模型结构

Exact flow可能保持：

- positivity；
- probability simplex；
- norm；
- energy；
- symplectic form；
- invariant manifold；
- monotonicity。

Generic explicit RK不自动逐项保持。例：

$$
y'=-\lambda y,
\qquad y_0>0.
$$

Euler给

$$
y_{n+1}=(1-h\lambda)y_n.
$$

当

$$
1<h\lambda<2
$$

时 amplitude仍衰减，但sign交替，positivity已丢失。

结构保持需要：

- 更小step；
- projection；
- positivity-preserving / SSP method；
- symplectic或geometric integrator；
- problem-specific transformation；
- implicit method。

这些方法的完整理论不由“order高”替代。

## 二十四、Truncation 与 roundoff 的 U-shaped trade-off

在 exact arithmetic中，减小 $h$ 通常降低 truncation error：

$$
E_{\rm trunc}(h)\approx C h^p.
$$

但步数约为 $T/h$。若每步roundoff为 $O(u)$：

- worst-case coherent accumulation约 $O(u/h)$；
- 独立随机式heuristic约 $O(u/\sqrt h)$。

Worst-case模型下：

$$
E_{\rm total}(h)
\approx C h^p+\frac{D u}{h}.
$$

最小点量级满足

$$
h_{\rm opt}
\asymp
\left(
\frac{Du}{pC}
\right)^{1/(p+1)}.
$$

所以 $h\to0$ 在floating point中不保证error无限下降。

### 24.1 AI 里的额外误差

- mixed-precision vector field；
- nondeterministic reductions；
- quantized weights；
- stochastic layers；
- approximate normalization；
- learned field本身的model error。

Solver order只描述离散化层，不能吞掉这些项。

## 二十五、Variable-step global error

令

$$
H=\max_n h_n,
\qquad
\sum_n h_n=T-t_0.
$$

若每步

$$
\|d_{n+1}\|
\le C h_n^{p+1}
\le C H^p h_n,
$$

且 perturbation propagation满足uniform Lipschitz bound，则

$$
\|e_N\|
\le
C e^{L(T-t_0)}
\sum_n H^p h_n.
$$

因此

$$
\boxed{
\|e_N\|
\le
C(T-t_0)e^{L(T-t_0)}H^p
}.
$$

Variable step本身不破坏 one-step order，但需要：

- step ratios不触发实现特例；
- local constants uniform；
- accepted states留在regular region；
- controller最终让 $H\to0$；
- rejected steps不改变数学accepted path。

## 二十六、Absolute stability 的最小预览

对

$$
y'=\lambda y,
\qquad
z=h\lambda,
$$

RK method产生

$$
y_{n+1}=R(z)y_n.
$$

一般stability function为

$$
\boxed{
R(z)
=1+z\,b^\top(I-zA)^{-1}\mathbf1
}.
$$

Explicit RK的 $A$ strictly lower triangular，因而 $R(z)$ 是polynomial。

### 26.1 三个例子

Euler：

$$
R_E(z)=1+z.
$$

Heun与explicit midpoint：

$$
R_2(z)
=1+z+\frac{z^2}{2}.
$$

Classical RK4：

$$
R_4(z)
=1+z+\frac{z^2}{2}
+\frac{z^3}{6}
+\frac{z^4}{24}.
$$

Absolute stability region为

$$
\mathcal S
=\{z\in\mathbb C:|R(z)|\le1\}.
$$

Order $p$意味着

$$
R(z)=e^z+O(z^{p+1})
\qquad(z\to0),
$$

但它只约束原点附近。大负 $z$ 是否stable是另一问题。

### 26.2 Accuracy 与 stability的分离

即使 $|R(z)|<1$：

- phase/amplitude可能很不准确；
- stiff slow manifold可能被过度damp；
- nonnormal system仍有matrix effects；
- nonlinear dynamics不由单一eigenvalue完整决定。

反之，local truncation error小也不能补救 $|R(z)|>1$ 的长期放大。

## 二十七、刚性的边界留给下一章

若Jacobian同时含：

- 很快衰减的large negative modes；
- task关心的slow modes，

explicit method可能因stability而被迫使用远小于accuracy需求的step。这称为stiffness现象的一种典型表现。

本章只记住：

$$
\text{step choice}
=
\min(
\text{accuracy requirement},
\text{stability requirement}
).
$$

下一章[[刚性系统、绝对稳定域与隐式方法]]将系统处理：

- 完整stability regions；
- A-stability与Dahlquist barrier；
- L-stability；
- backward Euler、trapezoidal、implicit RK/BDF；
- nonlinear solve与Jacobian；
- stiffness detection；
- nonnormal/pseudospectral边界。

## 二十八、ResNet：从形式类比到 refinement theorem

Residual block

$$
h_{k+1}
=h_k+\Delta t\,F_k(h_k)
$$

形式上类似 Euler：

$$
y_{k+1}
=y_k+\Delta t\,f(t_k,y_k).
$$

要把一族deep networks称为某个ODE的consistent discretization，需要：

1. 固定physical interval $[0,T]$；
2. depth $N\to\infty$ 时 $\Delta t=T/N\to0$；
3. $F_k$ 来自共同regular field的sample或一致近似；
4. parameters随refinement有compatible scaling；
5. local defect与perturbation stability uniform；
6. normalization、stochasticity与data-dependent routing被纳入state/model；
7. 比较的是同一input、同一output functional。

固定depth、untied blocks、默认step 1的network只能称 Euler-like architecture，不自动继承ODE flow、invertibility或convergence theorem。

## 二十九、Neural ODE 的 forward solver contract

设

$$
\dot y=f_\theta(t,y),
\qquad
\widehat y_T
=\operatorname{ODESolve}
(f_\theta,y_0,t_0,T,\text{method},\text{tol}).
$$

Model prediction实际依赖：

$$
\widehat y_T
=\widehat\Phi_{\theta,\mathcal A,\eta}(y_0),
$$

其中 $\mathcal A$ 是solver algorithm，$\eta$ 包含tolerances、step限制和event policy。

必须报告：

- method与版本；
- fixed/adaptive；
- rtol、atol与component scales；
- first/max/min step；
- accepted/rejected steps；
- NFE；
- dense output/events；
- forward precision；
- failure policy；
- tolerance sweep下的task metric。

### 29.1 NFE 不是独立质量指标

低NFE可能来自：

- vector field平滑；
- tolerance宽松；
- method高阶；
- dynamics被训练得容易积分；
- solver漏掉快速现象；
- trajectory错误但task loss不敏感。

因此NFE必须与error/tolerance/task metric共同报告。

## 三十、Continuous sensitivity 与 adjoint

令

$$
\dot y=f(t,y,\theta),
\qquad
J(\theta)=\ell(y(T)).
$$

Continuous sensitivity

$$
S(t)=\frac{\partial y(t)}{\partial\theta}
$$

满足

$$
\dot S
=f_yS+f_\theta.
$$

若参数维度大，直接传播 $S$ 很贵。定义continuous adjoint

$$
a(t)=\frac{\partial J}{\partial y(t)}.
$$

对terminal loss：

$$
\dot a(t)
=-f_y(t,y,\theta)^\top a(t),
\qquad
a(T)=\nabla_y\ell(y(T)).
$$

Parameter gradient为

$$
\boxed{
\frac{dJ}{d\theta}
=\int_{t_0}^{T}
f_\theta(t,y,\theta)^\top a(t)\,dt
}.
$$

这是 ideal continuous problem的公式。若有running loss或parameter regularizer，还要加相应source terms。

## 三十一、Euler 的 discrete adjoint

实际 forward computation为

$$
y_{n+1}
=y_n+h f(t_n,y_n,\theta).
$$

定义

$$
\lambda_n
=\frac{\partial J_h}{\partial y_n},
\qquad
J_h=\ell(y_N).
$$

Chain rule给

$$
\lambda_N
=\nabla\ell(y_N),
$$

$$
\boxed{
\lambda_n
=
\left(
I+h f_y(t_n,y_n,\theta)
\right)^\top
\lambda_{n+1}
}.
$$

Parameter gradient：

$$
\boxed{
\frac{dJ_h}{d\theta}
=
\sum_{n=0}^{N-1}
h f_\theta(t_n,y_n,\theta)^\top
\lambda_{n+1}
}.
$$

这正是对actual discrete computation graph做reverse mode。

### 31.1 两个gradient为何finite $h$ 下不同

Continuous adjoint求

$$
\nabla J,
\qquad
J=\ell(\Phi_\theta(y_0));
$$

Discrete adjoint求

$$
\nabla J_h,
\qquad
J_h=\ell(\widehat\Phi_{\theta,h}(y_0)).
$$

即使

$$
J_h\to J,
$$

finite $h$ 下通常

$$
\nabla J_h\ne\nabla J.
$$

需要额外regularity和uniform convergence才能交换“离散极限”与“参数微分”。

## 三十二、Continuous adjoint 重积分的数值边界

Memory-efficient adjoint实现可能：

1. Forward只保存少量checkpoints；
2. Backward重新积分state；
3. 同时积分adjoint与parameter accumulator。

风险包括：

- Backward reconstructed trajectory不等于forward accepted trajectory；
- Dissipative forward dynamics反向可能不稳定；
- Adaptive steps在反向重新选择；
- Event/reset需要jump adjoint；
- Nonsmooth activations与solver branches使gradient不光滑；
- Forward/adjoint tolerances不同；
- Roundoff和interpolation累积。

Checkpoint方法在memory与trajectory一致性之间折中。关键不是“continuous adjoint一定错”或“discrete backprop一定最好”，而是明确：

- 对哪个objective求导；
- 复用了哪些forward states；
- backward solver怎样配置；
- gradient是否通过finite difference / discrete adjoint交叉验证。

## 三十三、Adaptive solver 本身也是程序

Adaptive execution包含：

- error比较；
- accept/reject branch；
- step clipping；
- event branch；
- NFE-dependent control flow。

因此 $\theta\mapsto\widehat y_T$ 可能在step sequence改变处 nonsmooth。常见选择：

1. 把accepted discrete path视为固定程序并反传；
2. 忽略controller derivative，只对accepted stages反传；
3. 求ideal continuous gradient；
4. 用implicit/adjoint理论并做checkpoint；
5. 通过tolerance sweep检查训练是否依赖solver artifact。

每种选择对应不同gradient estimator，不能统称“ODE的精确梯度”。

## 三十四、有限步生成：瞬时速度与平均位移

Continuous vector field给 instantaneous velocity：

$$
v(t,x).
$$

Exact finite-step displacement满足

$$
x(t+h)-x(t)
=\int_t^{t+h}v(s,x(s))\,ds.
$$

平均速度是

$$
\overline v_{t,h}
=\frac1h
\int_t^{t+h}v(s,x(s))\,ds.
$$

Euler用

$$
v(t,x(t))
$$

近似 $\overline v_{t,h}$。当 $h$ 不小，这两者可以差很多。Diffusion/flow model减少NFE时，有三条不同路线：

- 保留instantaneous field，使用更高阶solver；
- 直接学习step-conditioned average/displacement；
- distill整个finite-step map。

三者的training target、semigroup consistency与refinement behavior不同。不能把learned finite-step map无条件解释为同一个instantaneous ODE。

## 三十五、Solver error 的完整账本

$$
\text{task output error}
\leftarrow
\begin{cases}
\text{data / observation error},\\
\text{modeling error},\\
\text{parameter estimation error},\\
\text{time discretization error},\\
\text{adaptive estimation / stopping error},\\
\text{event / interpolation error},\\
\text{roundoff / precision error},\\
\text{gradient estimation error}.
\end{cases}
$$

ODE solver order只控制其中一层。可信报告至少包含：

| 层 | 建议指标 |
|---|---|
| trajectory | endpoint、max-grid、integral error |
| solver | accepted/rejected steps、NFE、wall time |
| scale | rtol、atol vector、norm |
| stability | failed steps、min step、state blow-up |
| events | time/state residual |
| gradient | finite-difference/discrete-adjoint discrepancy |
| task | loss、accuracy、sample/control metric |
| robustness | solver/tolerance/precision sweep |

## 三十六、方法选择流程

~~~mermaid
flowchart TD
    A["IVP well posed?"] -->|no| A0["先修正模型"]
    A -->|yes| B{"nonstiff且smooth?"}
    B -->|yes| C{"只需教学/粗精度?"}
    C -->|yes| D["Euler / RK2 + refinement audit"]
    C -->|no| E["embedded RK pair + adaptive control"]
    B -->|unknown| F["tolerance/NFE/Jacobian audit"]
    F -->|出现stiff迹象| G["进入 DYN-06 implicit/stiff solver"]
    E --> H{"events / invariants / gradients?"}
    H --> I["补 dense output、event、structure、adjoint合同"]
~~~

## 三十七、常见错误与最小反例

### 错误 1：Local error与global error同阶

Euler local defect $O(h^2)$，固定时窗global error通常 $O(h)$。

### 错误 2：Order高就能用任意大step

Order只约束 $h\to0$ 附近；absolute stability region仍有限。

### 错误 3：Heun就是implicit trapezoidal

Heun用Euler predictor，完全explicit；implicit trapezoidal含未知 $y_{n+1}$。

### 错误 4：RK4公式少写 $1/6$

正确更新必须是

$$
\frac h6(k_1+2k_2+2k_3+k_4).
$$

### 错误 5：四个stages就是四阶

Order由algebraic conditions决定，不由stage count自动决定。

### 错误 6：rtol就是最终相对误差

它只进入local scaled estimator，global/task error需实测或另证。

### 错误 7：Accepted step保证每个component达标

Weighted RMS可能允许少数component超标。

### 错误 8：减小step总会改善

Roundoff、reference error和nonsmoothness会形成error floor。

### 错误 9：Grid order等于dense-output order

Continuous extension有自己的order。

### 错误 10：没检测到event就是没发生

一步内偶数次crossing可让端点同号。

### 错误 11：Exact flow保持positive，任意RK也保持

Euler对 $y'=-\lambda y$ 在 $1<h\lambda<2$ 已会换号。

### 错误 12：ResNet写成残差形式就收敛到ODE

缺少共同field、refinement与uniform stability。

### 错误 13：Continuous adjoint就是actual program gradient

它对ideal continuous objective求导；finite-step computation有discrete adjoint。

### 错误 14：NFE越少模型越好

低NFE可能来自宽松tolerance或漏解快速变化。

### 错误 15：实验slope等于一般证明

Slope只验收指定problem、steps与precision。

## 三十八、推导检查清单

- [ ] 声明了 exact/numerical/dense-output 对象
- [ ] 声明 local defect是否除以 $h$
- [ ] Local order写成 $O(h^{p+1})$
- [ ] Global theorem列出smoothness、Lipschitz与fixed horizon
- [ ] 使用 discrete Grönwall而非“直接乘步数”
- [ ] RK stages的time/state arguments完整
- [ ] Butcher内部一致性 $c=A\mathbf1$ 已检查
- [ ] Embedded estimator order与controller exponent匹配
- [ ] atol/rtol包含component scale
- [ ] Tolerance不冒充global guarantee
- [ ] Stability与accuracy分账
- [ ] Dense output/event单独报告
- [ ] Roundoff floor已考虑
- [ ] Continuous/discrete gradient对象已命名
- [ ] AI结论包含solver、NFE、precision和task metric

## 三十九、掌握层级

### Level 1：识别与手算

- 能写Euler、Heun、midpoint、RK4；
- 能区分local/global error；
- 能读Butcher tableau。

### Level 2：证明

- 能推Euler local defect；
- 能推Heun/midpoint二阶；
- 能重建discrete-Grönwall global error proof。

### Level 3：算法

- 能实现fixed-step RK；
- 能用embedded pair做accept/reject；
- 能正确缩放atol/rtol与记录NFE。

### Level 4：诊断

- 能识别pre-asymptotic、roundoff floor、event miss与order reduction；
- 能区分accuracy/stability/stiffness；
- 能做tolerance/refinement sweep。

### Level 5：AI迁移

- 能审计ResNet refinement；
- 能区分continuous/discrete adjoint；
- 能为Neural ODE或flow sampler写solver-aware实验合同。

## 四十、自测问题

1. Exact flow与numerical one-step map有什么区别？
2. 为什么积分方程自然导向quadrature-like method？
3. Euler的三种推导分别强调什么？
4. Local defect为什么要从exact state起步？
5. 两种local truncation error约定差一个什么因子？
6. Euler defect中为什么出现 $f_t+f_yf$？
7. Local $p+1$ 到global $p$ 的严格桥梁是什么？
8. Convergence proof的Lipschitz条件施加在哪个对象上？
9. Finite-horizon stability与absolute stability有何区别？
10. Observed order为什么用error ratio的base-2 log？
11. Heun与implicit trapezoidal有何不同？
12. Explicit midpoint为何二阶？
13. Butcher tableau的 $A,b,c$ 各是什么？
14. $c=A\mathbf1$ 表示什么？
15. 一、二阶RK条件是什么？
16. RK4的四个stage为何不能只解释为Simpson quadrature？
17. Stage count为何不等于order？
18. Step doubling如何估计fine solution error？
19. Embedded pair为何能节省NFE？
20. Controller exponent为何与estimator local power相关？
21. atol与rtol分别在什么尺度主导？
22. Weighted RMS可能漏掉什么？
23. Rejected step为什么仍要计成本？
24. Tolerance为什么不等于global error？
25. Dense output为何需要自己的order？
26. Event为何可能在一步内被漏掉？
27. Discontinuity为什么导致order reduction？
28. Euler怎样破坏positivity？
29. Roundoff为什么让过小step变坏？
30. Variable-step global bound为什么由 $H=\max h_n$ 控制？
31. RK stability function怎样从Butcher coefficients得到？
32. Order condition只约束 $R(z)$ 的哪个区域？
33. Stiffness为什么会让step受稳定性而非accuracy控制？
34. ResNet要成为ODE refinement family还缺什么？
35. Continuous adjoint与discrete adjoint分别对哪个objective求导？
36. Adaptive controller为什么会让computed map nonsmooth？
37. Instantaneous velocity与finite-step average velocity如何联系？
38. NFE报告为什么必须配error/task metric？

## 四十一、来源与证据边界

1. MIT 18.330, [Methods for Ordinary Differential Equations](https://ocw.mit.edu/courses/18-330-introduction-to-numerical-analysis-spring-2012/a9d2bd9be098f0ada172af40379a17cc_MIT18_330S12_Chapter5.pdf)：Euler/RK、local/global error、consistency、finite-horizon stability与test-equation入口；
2. Hairer, Nørsett & Wanner, [Solving Ordinary Differential Equations I: Nonstiff Problems](https://archive-ouverte.unige.ch/unige%3A12346)：Runge–Kutta、error estimation、step control、dense output与nonstiff solver的正式专著主线；
3. SciPy, [solve_ivp official documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html)：当前RK23/RK45/DOP853接口、rtol/atol、dense output与event语义的工程合同；
4. Chen et al., [Neural Ordinary Differential Equations](https://proceedings.neurips.cc/paper_files/paper/2018/file/69386f6bb1dfed68692a24c8686939b9-Paper.pdf), NeurIPS 2018：black-box ODE solver与adjoint sensitivity训练框架；
5. Zhuang et al., [Adaptive Checkpoint Adjoint Method for Gradient Estimation in Neural ODE](https://proceedings.mlr.press/v119/zhuang20a.html), ICML 2020：forward/reverse trajectory mismatch、checkpoint与adaptive gradient estimation的特定框架；
6. 苏剑林，[从动力学角度看优化算法（三）：一个更整体的视角](https://spaces.ac.cn/archives/6261)：ODE、numerical update与optimization trajectory的中文入口；
7. 苏剑林，[生成扩散模型漫谈（三十）：从瞬时速度到平均速度](https://spaces.ac.cn/archives/10958)：finite-step average velocity、低NFE generation与instantaneous-field区别的问题入口。

> [!info] 证据分工
> MIT与Hairer–Nørsett–Wanner承担one-step convergence、RK theory、error estimation和adaptive integration的正式数学证据；SciPy文档只承担当前软件接口语义；NeurIPS/ICML原论文承担Neural ODE与adaptive checkpoint adjoint的特定训练框架；科学空间承担optimizer/diffusion velocity的中文问题入口。本章自行组织local-to-global离散Grönwall证明、continuous/discrete objective分账和solver-aware AI claim ladder，不把默认tolerance、有限slope实验、软件成功返回或博客类比提升为一般accuracy/stability theorem。

## 四十二、配套训练与实验

- 习题：[[习题 - Euler、Runge-Kutta 与离散化误差]]
- 详解：[[解答 - Euler、Runge-Kutta 与离散化误差]]
- 数值复现：[[实验 - ODE 阶数、自适应步长与离散梯度审计]]
- 分卷导航：[[ODE、动力系统与 SDE MOC]]
- 前置：[[常微分方程、初值问题与解的存在唯一性]]、[[Lyapunov 稳定性与能量函数]]
- 后继：[[刚性系统、绝对稳定域与隐式方法]]
