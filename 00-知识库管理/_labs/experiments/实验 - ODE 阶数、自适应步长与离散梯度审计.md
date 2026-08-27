---
type: experiment
status: draft
area: [labs, math/ode, math/numerical-analysis, ai/neural-ode]
prerequisites: ["[[Euler、Runge-Kutta 与离散化误差]]", "[[常微分方程、初值问题与解的存在唯一性]]", "[[Taylor 展开与余项]]"]
related: ["[[推导与实验 MOC]]", "[[习题 - Euler、Runge-Kutta 与离散化误差]]", "[[Lyapunov 稳定性与能量函数]]"]
sources: ["MIT-18.330-ODE", "Hairer-Norsett-Wanner-ODE-I", "Chen-2018-Neural-ODE", "Zhuang-2020-ACA"]
code: "[[00-知识库管理/_labs/code/ode_solver_order_adjoint_audit.py]]"
figure: "[[00-知识库管理/_assets/plots/dynamics/plot-ode-order-adaptivity-gradient-v2.svg]]"
created: 2026-08-19
updated: 2026-08-23
---

# 实验 - ODE 阶数、自适应步长与离散梯度审计

> [!abstract] 实验结论
> 同一份 deterministic script 完成了三层互不替代的审计。Track A 在 $y'=y$ 上测得 Euler、Heun、RK4 的 endpoint observed order 分别为 $0.964922,1.969326,3.966230$。Track B 对 $y'=2t\cos(t^2)$ 收紧 Euler–Heun 容差，最大 accepted-node error 从 $5.43\times10^{-4}$ 降至 $1.03\times10^{-7}$，同时 NFE 从 $978$ 增到 $94480$。Track C 证明 discrete gradient 与 finite difference of $J_h$ 在 $10^{-9}$ 内吻合，但与 continuous gradient 的差距仍按一阶消失。三条证据分别回答“method的渐近阶”“adaptive program在本问题上的经验表现”“实际离散目标的反向实现是否正确”。

## 研究问题

本实验不把 solver 当成一个只有 success/failure 的黑箱，而是问：

1. 理论 global order 能否从一族 refinement observations 中恢复？
2. 高阶优势是在同一步长、同一误差定义下观察到的吗？
3. adaptive local estimator 的 accept/reject 如何转化为真实成本与经验 global error？
4. tolerance 收紧是否单调改善当前 smooth nonstiff test problem？
5. discrete adjoint/analytic gradient 应该和哪个 finite difference 比较？
6. “gradient implementation正确”为什么不等于“continuous gradient已经准确”？
7. 能否仅用标准库生成机器断言、数据表和 self-contained SVG？

## 三个待验证命题

> [!hypothesis] 预注册假设
> 1. 对固定时域 $T=1$，Euler、Heun、RK4 的 endpoint error log–log slope 分别落在 $[0.90,1.05]$、$[1.90,2.05]$、$[3.85,4.10]$；
> 2. 对指定 chirp IVP，rtol 从 $10^{-3}$ 收紧到 $10^{-7}$ 时，最大 accepted-node error 严格下降，但 NFE 明显上升；
> 3. Euler computed objective 的 analytic/discrete gradient 与 central finite difference of同一个 $J_h$ 相差小于 $2\times10^{-9}$；
> 4. 该 discrete gradient 与 continuous gradient 的差距按 $O(h)$ 消失，观测 slope 落在 $[0.80,1.05]$。

若其中任一 assertion 失败，脚本非零退出，不生成“通过”结论。

## Track A：固定步 refinement 与 observed order

### A.1 问题选择

取

$$
y'=y,\qquad y(0)=1,\qquad 0\le t\le1,
$$

精确 endpoint 为 $y(1)=e$。这个问题有三个优点：

- exact reference 不依赖另一个 numerical solver；
- 所有 derivatives smooth，classical order theorem 的前提成立；
- 对 RK method，结果能由 stability polynomial独立复核。

它不是 stiff benchmark，也没有 event、discontinuity 或 vector-valued scaling；因此不能承担这些方向的结论。

### A.2 方法与公平比较

比较 explicit Euler、Heun 与 classical RK4。三者使用同一组

$$
N\in\{8,16,32,64,128\},
\qquad h=1/N,
$$

同一初值、同一时间区间、同一 float64 运算和同一 endpoint absolute error：

$$
E(h)=|y_N-e|.
$$

这里比较的是“相同步数”而不是“相同 NFE”或“相同 wall time”。Euler每步1次 field evaluation，Heun每步2次，RK4每步4次。若研究 cost–accuracy frontier，横轴必须改为NFE或wall time。

### A.3 Observed order

对观测对 $(h_j,E_j)$，最小二乘拟合

$$
\log E_j=\alpha+p_{\rm obs}\log h_j.
$$

不能只用某一个 error 很小就宣称高阶；order 是 refinement family 的 asymptotic scaling。

### A.4 结果

| Method | $E(1/8)$ | $E(1/128)$ | fitted order |
|---|---:|---:|---:|
| Euler | $1.524973\times10^{-1}$ | $1.054281\times10^{-2}$ | $0.964922$ |
| Heun | $6.440590\times10^{-3}$ | $2.749014\times10^{-5}$ | $1.969326$ |
| RK4 | $4.984042\times10^{-6}$ | $8.384093\times10^{-11}$ | $3.966230$ |

所有 slopes 都进入预注册区间。其解释是：在这一 smooth、nonstiff、fixed-horizon、roundoff尚未主导的 regime 中，经验结果与一、二、四阶 global convergence 一致。

> [!warning] 不能推出什么
> 这不证明 RK4 在相同 NFE 下一定优于 Heun，不证明 RK4 对 stiff mode stable，也不证明任何 method 对 discontinuous forcing 保持名义阶。

## Track B：adaptive Euler–Heun 的局部决策与全局观测

### B.1 问题选择

取

$$
y'=2t\cos(t^2),\qquad y(0)=0,\qquad 0\le t\le4,
$$

所以

$$
y(t)=\sin(t^2).
$$

随着 $t$ 增大，phase $t^2$ 振荡加快；它能让 adaptive controller 调整步长，同时仍保留 exact reference。

### B.2 Embedded pair

每次 trial step 共用

$$
k_1=f(t_n,y_n),\qquad
k_2=f(t_n+h,y_n+hk_1).
$$

低阶 Euler 与高阶 Heun 值为

$$
y_{n+1}^{[1]}=y_n+hk_1,\qquad
y_{n+1}^{[2]}=y_n+\frac h2(k_1+k_2).
$$

估计量

$$
\delta=y_{n+1}^{[2]}-y_{n+1}^{[1]}
$$

使用 scalar scale

$$
s=\operatorname{atol}
+\operatorname{rtol}max(|y_n|,|y_{n+1}^{[2]}|),
\qquad
\operatorname{err}=|\delta|/s.
$$

$\operatorname{err}\le1$ 接受高阶值，否则拒绝。lower order $q=1$，controller 为

$$
h_{\rm new}=h\,
\operatorname{clip}_{[0.2,5]}
\left(0.9\operatorname{err}^{-1/2}\right),
$$

另设 $h_{\max}=0.5$。这里没有使用 PI history，目的是保持机制透明。

### B.3 容差组合

设置

$$
\operatorname{rtol}\in\{10^{-3},10^{-5},10^{-7}\},
\qquad
\operatorname{atol}=0.01\operatorname{rtol}.
$$

这使解接近零时仍有 absolute scale。每个 trial step调用两次 $f$；被拒步同样计入 NFE。

### B.4 结果

| rtol | atol | accepted | rejected | NFE | endpoint error | max node error |
|---:|---:|---:|---:|---:|---:|---:|
| $10^{-3}$ | $10^{-5}$ | 467 | 22 | 978 | $3.4373\times10^{-4}$ | $5.4290\times10^{-4}$ |
| $10^{-5}$ | $10^{-7}$ | 4716 | 24 | 9480 | $5.6105\times10^{-6}$ | $7.9762\times10^{-6}$ |
| $10^{-7}$ | $10^{-9}$ | 47211 | 29 | 94480 | $7.3461\times10^{-8}$ | $1.0315\times10^{-7}$ |

误差单调下降，成本约每收紧两个数量级增加十倍。这是该 pair、controller、scale和test IVP 的经验 cost–accuracy curve，不是一般复杂度定理。

### B.5 为什么步数看起来很多

Euler–Heun pair 的 estimator 由 $O(h^2)$ 差值控制；要求 local normalized error进入很紧阈值时，步长大致按 tolerance 的平方根收缩。因此低阶 pair 在 $10^{-7}$ 级容差下付出数万步并不反常。

生产级 RK45/DOP853 会用更高阶pair、FSAL与更成熟 controller；本实验刻意保留低阶 pair，使 exponent、rejection 和 NFE 都能手算。

### B.6 仍需哪些审计

虽然有 exact solution，本 track 仍只在 accepted nodes测量误差，未测：

- dense-output query error；
- event time error；
- vector-valued weighted RMS 对关键 component 的稀释；
- discontinuity附近的 order reduction；
- float32 roundoff floor；
- solver对参数变化导致的 branch switching。

因此 $\operatorname{err}\le1$ 不是 global certificate；这里只有运行后与 exact solution 对照才得到 global observations。

## Track C：离散目标、离散梯度与连续极限

### C.1 连续对象

考虑

$$
y'=\theta y,\qquad y(0)=1,\qquad T=1,\qquad \theta=0.7,
$$

以及

$$
J(\theta)=\frac12(y(1)-1.5)^2.
$$

精确解和连续梯度为

$$
y(1)=e^\theta,\qquad
g=(e^\theta-1.5)e^\theta.
$$

### C.2 实际离散对象

Euler 用 $h=1/N$ 得到

$$
y_N=(1+h\theta)^N,
$$

$$
J_h(\theta)=\frac12\left((1+h\theta)^N-1.5\right)^2.
$$

它的 exact/discrete derivative 是

$$
g_h
=\left((1+h\theta)^N-1.5\right)
(1+h\theta)^{N-1}.
$$

最后一个 factor没有 $N h$，因为 $T=Nh=1$。该式也可由 discrete adjoint recursion逐步得到。

### C.3 两个不同的误差

实验同时计算

$$
E_{\rm implementation}=|g_h-\operatorname{FD}(J_h)|,
$$

$$
E_{\rm discretization}=|g_h-g|.
$$

central finite difference 使用

$$
\operatorname{FD}(J_h)
=\frac{J_h(\theta+10^{-5})-J_h(\theta-10^{-5})}{2\times10^{-5}}.
$$

第一项检查“代码是否对实际 finite-step program 求了正确导数”；第二项检查“该 program 的梯度离 continuous objective 还有多远”。

### C.4 结果

| $N$ | $h$ | $g_h$ | $|g_h-g|$ | $|g_h-\mathrm{FD}(J_h)|$ |
|---:|---:|---:|---:|---:|
| 4 | 0.25 | 0.658830569 | $3.7574\times10^{-1}$ | $8.73\times10^{-11}$ |
| 8 | 0.125 | 0.820823206 | $2.1375\times10^{-1}$ | $1.76\times10^{-10}$ |
| 16 | 0.0625 | 0.920028952 | $1.1454\times10^{-1}$ | $1.35\times10^{-10}$ |
| 32 | 0.03125 | 0.975202680 | $5.9368\times10^{-2}$ | $1.57\times10^{-10}$ |
| 64 | 0.015625 | 1.004337660 | $3.0233\times10^{-2}$ | $5.29\times10^{-10}$ |
| 128 | 0.0078125 | 1.019313738 | $1.5257\times10^{-2}$ | $9.11\times10^{-10}$ |

discrete gradient从最粗网格开始就与 $J_h$ 的 finite difference 高度吻合；但此时它与 continuous gradient 相差 $0.376$。所以“gradient check通过”必须连同被检查的 objective一起说。

对 $|g_h-g|$ 拟合得到约一阶 slope，与 Euler离散化一致。continuous gradient不是错误答案；它回答的是另一个目标。只有 refinement 后两个目标与梯度才趋于一致。

## 统一图

先看图判断：固定步长收敛阶、自适应误差控制与离散梯度一致性分别验收哪一个对象？为什么 NFE 少或 finite-difference 一致都不等于连续目标已准确？

![[00-知识库管理/_assets/plots/dynamics/plot-ode-order-adaptivity-gradient-v2.svg|880]]

> [!figure] 实验图｜ODE 阶数、自适应步长与离散梯度三道门
> A 比较 Euler、Heun、RK4 的 endpoint error 斜率；B 展示 adaptive Euler–Heun 的 accepted/rejected steps、NFE 与节点误差；C 分开 $|g_h-g|$ 与离散 tangent 对 $J_h$ 的有限差分误差。生成脚本：[[ode_solver_order_adjoint_audit.py]]；确定性解析例子，并对三种阶、容差扫描与梯度一致性设断言。

**怎样读图。** A 的 slope 只在进入渐近区后解释 method order；B 同时看误差和成本，不把容差当作全局误差上界；C 中蓝线接近零说明实现正确求了 $g_h$，红线随 $h$ 下降才说明离散目标向连续目标靠近。

**适用边界（图没有证明什么）。** 使用标量光滑 ODE 与手写嵌入式控制器；不覆盖刚性、事件、复杂容差控制或生产 adjoint 实现。图不证明 neural ODE 训练的梯度、内存和 wall-time 具有同样规律。

> [!question] 本实验的判别问题
> 怎样把方法阶、adaptive controller 的局部合同、离散程序梯度和连续问题梯度分成四个可独立失败的对象？

图的三块不能横向互相替代：

- A 的 slope 说明 asymptotic order；
- B 的表说明一次指定 adaptive policy 的经验成本与误差；
- C 的两条曲线说明 implementation gap 与 continuous–discrete gap是不同对象。

## 环境与复现

| 项目 | 配置 |
|---|---|
| Python | 3.9.6，standard library only |
| Randomness | 无 |
| Primary arithmetic | Python float / IEEE-754 binary64 |
| Reference | Track A/C解析式；Track B解析式 $\sin(t^2)$ |
| 图格式 | 脚本直接生成 self-contained SVG |
| 输出 | stdout表格、assertions、SVG |

脚本：

`00-知识库管理/_labs/code/ode_solver_order_adjoint_audit.py`

复现命令：

~~~bash
python3 00-知识库管理/_labs/code/ode_solver_order_adjoint_audit.py
~~~

确定性检查：脚本连续执行两次后，stdout 完全相同，SVG 的 SHA-256 均为

~~~text
f3ea36d7db2b95ec63c4b426740658943b4ba31845456eaad7946a0cfb6f5b2d
~~~

## Machine assertions

~~~text
0.90 < observed_order(Euler) < 1.05
1.90 < observed_order(Heun) < 2.05
3.85 < observed_order(RK4) < 4.10
max_node_error strictly decreases across tolerance sweep
max |discrete_gradient - FD(J_h)| < 2e-9
0.80 < observed_order(|g_h-g|) < 1.05
~~~

全部通过。

## 误差账本

| 层级 | 本实验如何控制 | 尚未覆盖 |
|---|---|---|
| Model error | 使用定义明确、带解析解的真实 field | learned field/data error |
| Fixed-step discretization | exact endpoint + refinement slope | stiff stability、long horizon |
| Adaptive local estimate | explicit pair与scale | estimator calibration theorem |
| Adaptive global error | 运行后对 exact nodes 比较 | 运行前 certificate |
| Roundoff | float64且当前未到明显floor | float32/mixed precision sweep |
| Gradient implementation | analytic $g_h$ + FD of $J_h$ | 大型autodiff graph |
| Continuous–discrete gradient | exact $g$ + refinement | adaptive branch derivative |
| Cost | NFE、accepted/rejected counts | device wall time、memory |

## 对 Neural ODE 实验的迁移

将本实验迁移到 Neural ODE 时，最低限度应保留以下结构：

1. 冻结模型参数后做 solver refinement，避免训练变化污染 solver comparison；
2. 同时报告 state、task和gradient metrics；
3. 对 deployed solver objective用 discrete backprop/adjoint与 FD检查；
4. 对 continuous claim使用独立高精度 trajectory/gradient reference；
5. 记录 forward accepted grid，并检查 reverse重算是否回到同一 states；
6. NFE必须包括 rejected steps，并与wall time、memory分开；
7. 对 tolerance、max step、method、precision 至少做二维以上 sweep；
8. adaptive branch改变时，把map看作 piecewise-defined program，而不是默认处处光滑。

## 结论边界

本实验支持：

- 三个指定 RK methods 在指定 smooth scalar IVP 上的 observed orders；
- 指定 Euler–Heun controller 对 chirp问题的 tolerance–cost–error observations；
- Euler computed objective 的解析离散梯度实现；
- discrete gradient向continuous gradient的一阶靠拢；
- 图、表和 assertions 可由无随机脚本复现。

本实验不支持：

- adaptive local tolerance 是一般 global error upper bound；
- RK4在相同成本下总是最佳；
- 这些 explicit methods适合 stiff systems；
- continuous adjoint与discrete adjoint在有限步长完全相同；
- Neural ODE训练loss、泛化或robustness结论；
- 任意event、dense output或discontinuous dynamics的精度结论。

## 失败判据与后续扩展

出现以下任一项时，复现失败：

1. observed order 未落入预注册区间；
2. tolerance 收紧反而使 exact-reference max error上升；
3. finite-difference gap超过阈值；
4. 连续—离散gradient gap不随 refinement下降；
5. 连续执行两次的stdout或SVG hash不同；
6. SVG不能通过 XML parser 或标准 renderer。

后续可扩展为：

- 用 Dormand–Prince 5(4) 比较高阶 pair 和 FSAL；
- 加入 $y'=-1000(y-\cos t)-\sin t$ 观察 stiffness boundary；
- 加入 event crossing 与 dense interpolant order；
- 对 adaptive accepted-step branches 做 parameter perturbation map；
- 对 Neural ODE 比较 continuous、discrete 与 checkpoint adjoints；
- 对 GPU batch dynamics测量 NFE之外的wall time与divergence。

## 复现记录

| 日期 | 环境 | 结果 | 状态 |
|---|---|---|---|
| 2026-08-19 | Python 3.9.6 standard library；脚本两次一致；SVG通过xmllint并由Sharp渲染目检 | 三 tracks 的全部 assertions 通过 | reproduced-once |

> [!warning] 状态语义
> reproduced-once 表示当前机器上的脚本、数据与断言一致，不表示习题已由读者独立完成，也不把经验曲线升级为无条件 theorem。
