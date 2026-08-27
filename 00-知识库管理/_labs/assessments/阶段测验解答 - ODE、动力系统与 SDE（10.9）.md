---
type: assessment-solution
status: draft
area: [math/ode, math/dynamical-systems, math/sde, ai/generative-modeling]
assessment_id: DYN-CUM-01
assessment: "[[阶段测验 - ODE、动力系统与 SDE（10.9）]]"
scope: [DYN-01, DYN-02, DYN-03, DYN-04, DYN-05, DYN-06, DYN-07, DYN-08, DYN-09, DYN-10, DYN-11, DYN-12]
related: ["[[ODE、动力系统与 SDE MOC]]", "[[练习与测验 MOC]]", "[[推导与实验 MOC]]", "[[实验 - ODE、动力系统与 SDE 累计复现门]]"]
created: 2026-08-19
updated: 2026-08-19
---

# 阶段测验解答 - ODE、动力系统与 SDE（10.9）

> [!warning] 使用顺序
> 先在 240 分钟内独立完成[[阶段测验 - ODE、动力系统与 SDE（10.9）]]，冻结原稿并完成指定计算轨道，再打开本解答。读懂解答不等于会做；必须标出原答案中第一个无依据的等号、第一次对象偷换或第一个遗漏条件，并在 48 小时后空白重建。

> [!abstract] 评分思想
> 本卷最重要的不是最终数字，而是对象和结论边界。把 exact flow、solver map、SDE path、marginal density 与 learned score 混成一个对象，即使后续代数恰好正确，也不能得到对应的理论分。等价推导可以得分；但必须给出足以检查的假设、关键中间式和验收量。

## 一、A 区：定义、对象与条件

### 第 1 题解答：适定性与随机对象（5 分）

每项 0.5 分。只判断、不对错误命题作最小修正，至多得该项一半。

1. **错误。** $f$ 连续在经典 Peano 条件下可给局部存在，但不保证唯一；常用充分条件是对 state 局部 Lipschitz。例 $x'=2\sqrt{|x|},x(0)=0$ 可等待任意时间后离开零。
2. **正确。** 例如 $x'=x^2,x(0)=1$ 的解 $x(t)=1/(1-t)$ 在 $t=1$ blow up，虽在每个 $[0,T)$、$T<1$ 上都是良好 classical solution。
3. **正确。** 若两个轨迹在同一时刻相交，从交点重启便得到同一 IVP；唯一性迫使它们在共同存在域上重合。由此得到固定时刻 flow map 的 injectivity，但 surjectivity 还要反向延拓。
4. **正确。** 对 $C^1$ autonomous vector field，若 Jacobian 的谱严格位于左半平面，linearization theorem 给 local asymptotic stability；这是假设 hyperbolicity 后的局部结论。
5. **错误。** $\dot V\le0$ 只给 nonincrease。要推出趋于 equilibrium，需 positive definiteness、适当紧性，并分析 $\{\dot V=0\}$ 中最大不变集；若要唯一极限还需更多结构。
6. **错误。** Brownian path 几乎处处 nowhere differentiable；连续性不意味着 classical differentiability。
7. **正确。** 在标准细化确定性 partition 上，平方增量和趋于区间长度，而绝对增量和发散；这正是 Itô calculus 不可用普通有限变差链式法则的原因。
8. **错误。** 标准 Itô integral 先对 adapted/predictable、平方可积 integrand 定义。允许依赖未来增量会破坏条件均值为零和标准 isometry 的论证；那将进入 anticipative calculus 等另一理论。
9. **错误。** strong solution 指在给定概率空间和 Brownian motion 上构造、对噪声适应的解；strong convergence 指数值解与 exact solution 在同一 coupling 下的路径误差速率。
10. **正确。** 一时刻边缘族不决定跨时间 coupling。$W_t$ 与 $\sqrt t Z$（固定 $Z\sim\mathcal N(0,1)$）都有 $\mathcal N(0,t)$ marginal，但前者 quadratic variation 为 $t$，后者为零。

> [!tip] 第一个诊断门
> 若第 1、3、4 项混淆，回到[[常微分方程、初值问题与解的存在唯一性]]与[[相图、平衡点与局部稳定性]]；若第 7—10 项混淆，回到[[随机过程、Brownian 运动与二次变差]]和[[Itô 引理与随机微分方程]]。

### 第 2 题解答：线性系统、相图与 Lyapunov（5 分）

1. 可由 power series
   $$e^{tA}=\sum_{k=0}^\infty\frac{t^kA^k}{k!}$$
   定义，也可把它定义为 fundamental matrix $\Phi'=A\Phi,\Phi(0)=I$ 的唯一解。若 $A=V\Lambda V^{-1}$ 可对角化，则 $e^{tA}=Ve^{t\Lambda}V^{-1}$；缺陷矩阵不能只保留 eigenvalues，Jordan nilpotent 会产生 polynomial factor。
2. eigenvalues 控制 asymptotic modes，但非正规矩阵的 eigenvectors 可高度不正交。不同模态在 Euclidean geometry 中可发生暂态相长，故 spectral abscissa $<0$ 不推出 $\|e^{tA}\|_2$ 单调。
3. 若 equilibrium hyperbolic，即 Jacobian 无零实部 eigenvalue，则 stable/unstable dimensions 和 local qualitative phase portrait 由线性化稳定决定。出现纯虚或零实部时，linear part 在中心方向没有足够的一阶判别力；相同 Jacobian 可配上向内、中心或向外的高阶项。
4. stability 要求初值近则以后一直近；attractivity 要求轨迹趋于 equilibrium；asymptotic stability 是二者同时成立；exponential stability 进一步给 $\|x(t)-x_*\|\le Me^{-\alpha t}\|x_0-x_*\|$ 这类定量速率。
5. 轨迹只在保持 $\dot V=0$ 时才能把 $V$ 的非下降耗散“用尽”。零导数集合中的点可能立即离开该集合，因此 LaSalle 取其中 largest invariant set，而不能把整个集合都当作极限集。

### 第 3 题解答：ODE 求解器合同（5 分）

1. 对 order-$p$ one-step method，足够光滑时一步 local defect 通常为 $O(h^{p+1})$；在 fixed horizon、稳定传播下约 $T/h$ 个缺陷累计为 global error $O(h^p)$。variable-step 情形通常由 $H=\max_n h_n$ 控制，而不是只看平均步长。
2. consistency 说明离散差分在 $h\to0$ 时逼近 differential equation；zero-stability 控制起始/舍入/local defects 不被 recurrence 无界放大。多步法中二者共同给 convergence，只有 consistency 不够。
3. stability region 是给定数值方法对 $y'=\lambda y$ 的 $z=h\lambda$ amplification 性质。stiffness 是问题与求解目标的 operational relation：真实解可按慢尺度变化，但 explicit stability 被快速衰减模态迫使使用远小于 accuracy 所需的步长。
4. A-stable 表示整个左半平面包含在 stability region；L-stable 还要求 $R(z)\to0$ 当 $z\to-\infty$，能强烈抹去 fast modes。trapezoidal rule A-stable 但非 L-stable，因为 $R(z)\to-1$。
5. 至少记录 method、step/tolerance、accepted/rejected steps、NFE、Jacobian/linear solve、error estimate、真实/参考误差、event/boundary 状态、termination code 与 non-finite/stagnation。只有 success flag 无法区分“完成积分”和“达到任务精度”。

### 第 4 题解答：流、密度与生成动力学（5 分）

1. $\phi_{s,t}:x_s\mapsto x_t$ 是 state-space map；$J=\partial\phi_{s,t}/\partial x_s$ 是线性化矩阵；$\det J$ 是局部 oriented volume ratio；$\nabla\cdot f=\operatorname{tr}(\nabla f)$ 是向量场在当前时空点的 instantaneous volume expansion rate。
2. 无源 continuity equation 的 conservative form 为
   $$\partial_t\rho+\nabla\cdot(\rho v)=0.$$
   展开后为
   $$D_t\rho:=\partial_t\rho+v\cdot\nabla\rho=-\rho\nabla\cdot v.$$
3. CNF 公式
   $$\frac d{dt}\log p_t(X_t)=-\nabla\cdot f(t,X_t)$$
   是沿 characteristic 的 total/material derivative，不是固定 $x$ 的 $\partial_t\log p_t(x)$。
4. Fokker–Planck 描述 SDE 的 marginal density/law 演化。probability-flow ODE 被构造为共享相同 one-time marginals；它一般不共享 transition kernel、path law 或 quadratic variation。
5. 当 $D=D(t)$ 与 state 无关，score $s_t=\nabla\log p_t$ 下
   $$v_{\rm PF}=f-\frac12Ds_t,$$
   而正常递增反向时钟的 reverse-SDE drift 是
   $$b_{\rm rev}=-f+Ds_t.$$
   前者是确定性 PF ODE 的 half-score correction，后者是仍带 diffusion 的 reverse SDE 的 full-score correction。

## 二、B 区：手算、构造与数值解释

### 第 5 题解答：非正规线性流、瞬态与采样（8 分）

#### 5.1 矩阵指数与轨迹（2.5 分）

设

$$
e^{tA}=\begin{bmatrix}a(t)&b(t)\\0&d(t)\end{bmatrix}.
$$

由 $\Phi'=A\Phi$ 和 $\Phi(0)=I$，先得

$$
a(t)=e^{-t},\qquad d(t)=e^{-3t}.
$$

右上角满足

$$
b'(t)=-b(t)+10e^{-3t},\qquad b(0)=0.
$$

乘积分因子 $e^t$：

$$
\frac d{dt}(e^tb)=10e^{-2t},
$$

所以

$$
b(t)=5(e^{-t}-e^{-3t}).
$$

因此

$$
e^{tA}=\begin{bmatrix}
e^{-t}&5(e^{-t}-e^{-3t})\\
0&e^{-3t}
\end{bmatrix},
$$

$$
x(t)=e^{tA}x(0)
=\begin{bmatrix}
5(e^{-t}-e^{-3t})\\e^{-3t}
\end{bmatrix}.
$$

#### 5.2 暂态长度（1.5 分）

当 $t_*=\tfrac12\log3$ 时

$$
e^{-t_*}=\frac1{\sqrt3},
\qquad
e^{-3t_*}=\frac1{3\sqrt3}.
$$

故

$$
x(t_*)=
\begin{bmatrix}
\dfrac{10}{3\sqrt3}\\[3pt]
\dfrac1{3\sqrt3}
\end{bmatrix},
$$

$$
\|x(t_*)\|_2
=\sqrt{\frac{100+1}{27}}
=\frac{\sqrt{101}}{3\sqrt3}
\approx1.934>1=\|x(0)\|_2.
$$

这已经构造出一个具体 initial direction 的 transient growth，因此也给出 $\|e^{t_*A}\|_2>1$ 的下界。

#### 5.3 渐近稳定与暂态不矛盾（1 分）

$A$ 是 triangular，eigenvalues 为 $-1,-3$，所以原点 asymptotically/exponentially stable。稳定性描述 $t\to\infty$ 的衰减；非正规耦合 $10$ 可先把第二坐标注入第一坐标，造成有限时间 Euclidean amplification。暂态增长不等于长期不稳定。

#### 5.4 方向长度与总体积（1 分）

Liouville formula 给

$$
\det(e^{tA})=e^{t\operatorname{tr}A}=e^{-4t}.
$$

两个 singular values 的乘积等于 $e^{-4t}$；其中一个可暂时大于 1，只要另一个收缩得更强。故 directional stretching、shape shear 和 total volume contraction 是三个不同对象。

#### 5.5 exact sampling 与 Euler replacement（2 分）

zero-order-hold 且无输入时

$$
x_{k+1}=A_dx_k,
\qquad
A_d=e^{hA}
=\begin{bmatrix}
e^{-h}&5(e^{-h}-e^{-3h})\\0&e^{-3h}
\end{bmatrix}.
$$

其 eigenvalues 由 spectral mapping 得

$$
e^{-h},\qquad e^{-3h}.
$$

Euler replacement 是

$$
I+hA=
\begin{bmatrix}1-h&10h\\0&1-3h\end{bmatrix},
$$

它只是一阶近似，每步 local matrix error 为 $O(h^2)$，fixed horizon global state error通常为 $O(h)$；其 eigenvalues $1-h,1-3h$ 还引入方法自己的 absolute-stability restriction。exact continuous stability 不自动保证任意 $h$ 的 Euler map 稳定或 injective。

### 第 6 题解答：局部稳定、Lyapunov 与 LaSalle（7 分）

#### 6.1 线性分类（1.5 分）

system matrix 为

$$
A=\begin{bmatrix}0&1\\-1&-1\end{bmatrix}.
$$

characteristic polynomial 是 $\lambda^2+\lambda+1$，所以

$$
\lambda_{1,2}=\frac{-1\pm i\sqrt3}{2}.
$$

两者实部为 $-1/2$，原点是 asymptotically stable spiral/focus；线性系统还全局 exponentially stable。

#### 6.2 能量导数（1.5 分）

$$
V(q,v)=\frac12(q^2+v^2)
$$

给出

$$
\dot V=q\dot q+v\dot v
=qv+v(-q-v)
=-v^2\le0.
$$

因此

$$
\{\dot V=0\}=\{(q,v):v=0\},
$$

是整条 $q$ 轴，不只含 equilibrium。

#### 6.3 最大不变集（2 分）

若轨迹想永久留在 $v=0$，必须同时有

$$
\dot v=-q-v=-q=0.
$$

故 $q=0$，largest invariant subset 只有 $\{(0,0)\}$。$V$ positive definite 且 radially unbounded，其 sublevel sets compact；LaSalle 因而给每条轨迹趋于原点，即 global asymptotic stability。

#### 6.4 证书能力与系统性质（1 分）

这个 Euclidean $V$ 不能满足某个 $c>0$ 下的 $\dot V\le-cV$：在 $(q,0)$、$q\ne0$ 时左边为 0，而右边严格为负。可是这只说明**这个候选函数和这个度量没有给出该 pointwise certificate**；系统矩阵 Hurwitz，存在 $P\succ0$ 解 Lyapunov equation，从而可用 $V_P=x^TPx$ 证明指数稳定。

#### 6.5 离散能量必须重验（1 分）

Euler map 是 $x_{k+1}=(I+hA)x_k$。应直接检查

$$
\Delta_hV(x)=V((I+hA)x)-V(x),
$$

或所选 $P$ 下

$$
(I+hA)^TP(I+hA)-P\preceq0,
$$

并同时检查 spectral radius、step refinement 与 state error。continuous $\dot V\le0$ 不能删除 $O(h^2)$ 离散项。

### 第 7 题解答：刚性模态与四种方法（8 分）

#### 7.1 Stability functions（2 分）

对 $z=h\lambda$：

$$
R_{\rm EE}(z)=1+z,
$$

$$
R_{\rm RK4}(z)=1+z+\frac{z^2}{2}+\frac{z^3}{6}+\frac{z^4}{24},
$$

$$
R_{\rm BE}(z)=\frac1{1-z},
\qquad
R_{\rm Trap}(z)=\frac{1+z/2}{1-z/2}.
$$

每个式子既是 test-equation amplification factor，也是讨论 absolute stability 的对象；不能把它直接当成一般 nonlinear solver 的完整误差。

#### 7.2 显式稳定步长（1.5 分）

Euler 要求

$$
|1-40h|<1,
$$

所以

$$
0<h<\frac2{40}=0.05.
$$

classical RK4 的负实轴 boundary 为 $-2.7853$，因此

$$
0<h<\frac{2.7853}{40}\approx0.0696325.
$$

若只要求 non-growth，端点可作非严格讨论；长期衰减验收应使用严格不等式。

#### 7.3 两种隐式方法（1.5 分）

$h=0.1$ 时 $z=-4$：

$$
R_{\rm BE}(-4)=\frac1{5}=0.2,
$$

$$
R_{\rm Trap}(-4)=\frac{1-2}{1+2}=-\frac13.
$$

两者 magnitude 都小于 1，但 trapezoidal 产生 sign alternation。更极端地，$z\to-\infty$ 时 BE 的 factor 趋零，而 trapezoidal 趋 $-1$；所以 A-stability 不等于 stiff decay 的 L-stability。

#### 7.4 错误的大步显式法（1 分）

Euler 在 $h=0.1$ 时

$$
R_{\rm EE}(-4)=-3,
$$

数值解交替并按 $3^k$ 放大，尽管 exact solution 按 $e^{-40t}$ 衰减。这是 solver instability，不是 original model instability。

#### 7.5 公平比较与隐式成本（2 分）

至少固定/报告：

- 同一 $T$、初值和输出节点；
- method、step/tolerance、accepted/rejected steps 与 NFE；
- reference construction、终点/最大网格误差和 stability failure；
- 对 implicit method，再记 Newton iterations、Jacobian evaluations/factorizations、linear iterations、preconditioner setup/reuse、failed solves 与 wall time。

同样 10 步，BE 可能每步需要多个 nonlinear/linear iterations；只按 step count 会系统低估成本。另一方面，若 explicit method 因 stability 被迫走数百步，只比较单步便也不公平。

### 第 8 题解答：OU 边缘、score、current 与反向漂移（7 分）

#### 8.1 边缘与 score（1.5 分）

$t=\log2$ 时

$$
e^{-t}=\frac12,
\qquad
e^{-2t}=\frac14.
$$

所以

$$
m_t=1,
\qquad
s_t^2=1+\frac34=\frac74.
$$

Gaussian score 为

$$
s_t(x):=\partial_x\log p_t(x)
=-\frac{x-m_t}{s_t^2}
=-\frac47(x-1).
$$

#### 8.2 Current 与 probability-flow velocity（1.5 分）

这里 $f(x)=-x$、$D=2$。一维 current 是

$$
j=fp-\frac12\partial_x(Dp)
=-xp-\partial_xp.
$$

用 $\partial_xp=p\,s_t(x)$：

$$
j_t(x)=\left[-x-s_t(x)\right]p_t(x)
=\left[-x+\frac47(x-1)\right]p_t(x).
$$

因此

$$
v_t(x)=\frac{j_t(x)}{p_t(x)}
=-x-s_t(x)
=-x+\frac47(x-1).
$$

#### 8.3 Reverse drift（1 分）

正常递增反向时钟下

$$
b_{\rm rev}(t,x)=-f(x)+D s_t(x)
=x+2s_t(x)
=x-\frac87(x-1).
$$

这里的 $t$ 是对应的 forward time；真正写 $Y_s$ 时要代 $t=T-s$，不能把时钟符号省略后混用。

#### 8.4 在均值处比较（1 分）

在 $x=m_t=1$：

$$
s_t(1)=0,
\qquad
v_t(1)=-1,
\qquad
b_{\rm rev}(t,1)=1.
$$

PF ODE 沿 forward time 搬运 $p_t$；reverse SDE 沿反向时钟从 $p_T$ 搬回 $p_0$，且仍带随机扩散。二者时钟、noise 和 path law 都不同，漂移不应相等。

#### 8.5 Score bias 与 solver bias 分账（2 分）

若使用 $\widehat s=1.1s$，连续极限本身的 PF velocity/reverse drift 就已错误。步长 $h\to0$ 只能收敛到**错误向量场/SDE**的精确解，marginal moments、density、likelihood 或 reverse endpoint 可留下非零 error floor。减半 Euler 步长可降低 discretization error，却不会自动消除 score approximation error；必须独立做 score calibration/denoising validation、exact-score oracle comparison 与 refinement extrapolation。

## 三、C 区：推导、证明与统一结构

### 第 9 题解答：Picard–Lindelöf、Gronwall 与 continuation（8 分）

#### 9.1 积分方程与 contraction（2 分）

IVP

$$
\dot x(t)=f(t,x(t)),\qquad x(0)=x_0
$$

等价于

$$
x(t)=x_0+\int_0^t f(s,x(s))\,ds.
$$

在 $C([0,\delta];\mathbb R^d)$ 上定义

$$
(\Phi x)(t)=x_0+\int_0^t f(s,x(s))\,ds.
$$

sup norm 下

$$
\|\Phi x-\Phi y\|_\infty
\le \sup_{t\le\delta}\int_0^tL\|x(s)-y(s)\|ds
\le L\delta\|x-y\|_\infty.
$$

取 $L\delta<1$ 即 contraction。完整 self-map 论证还需选闭球 $B(x_0,R)$ 并使 $\delta\sup\|f\|\le R$；只写 contraction factor 而不说明 map 的空间和 self-map，扣条件分。

#### 9.2 Uniqueness 与 continuous dependence（2 分）

若 $x,y$ 分别从 $x_0,y_0$ 出发，则

$$
x(t)-y(t)=x_0-y_0+
\int_0^t[f(s,x(s))-f(s,y(s))]ds.
$$

因此

$$
u(t):=\|x(t)-y(t)\|
\le u(0)+L\int_0^tu(s)ds.
$$

Gronwall 给

$$
\|x(t)-y(t)\|
\le e^{Lt}\|x_0-y_0\|.
$$

若 $x_0=y_0$，右边为零，得到 uniqueness；若初值略变，则轨迹在 fixed horizon 上按显式 Lipschitz factor 连续变化，得到 continuous dependence。两者来自同一个差分不等式，但结论对象不同。

#### 9.3 Linear growth 与 global continuation（2 分）

由积分方程和 growth：

$$
\|x(t)\|
\le\|x_0\|+at+b\int_0^t\|x(s)\|ds.
$$

当 $b>0$ 时，可把常数并入 $u(t)+a/b$，得到

$$
\|x(t)\|
\le\left(\|x_0\|+\frac ab\right)e^{bt}-\frac ab.
$$

当 $b=0$ 时直接有 $\|x(t)\|\le\|x_0\|+at$。故任意有限 $T$ 上 state 有界；结合局部存在唯一和系数在相应 compact cylinder 上的控制，可在端点附近重启并逐段延拓，排除由 state escaping to infinity 引起的有限时 blow-up。这里题设其实给了 global Lipschitz，更直接支持全局延拓；仍必须写出 bound，不能把“local theorem”口头升级成 global。

#### 9.4 Proper Lyapunov bound 的增量（2 分）

沿解

$$
\frac d{dt}V(x(t))
=\nabla V(x(t))^Tf(t,x(t))
\le-\alpha V(x(t)).
$$

再次用 Gronwall：

$$
V(x(t))\le e^{-\alpha t}V(x_0).
$$

properness 使 bounded sublevel sets compact，因此该证书既给 forward boundedness，也给 energy decay；若 $V$ 与 $\|x-x_*\|^2$ 上下等价，还给 exponential state stability。它仍不替代 local existence/uniqueness 的 regularity 条件，也不证明任意 numerical solver 保留该能量，更不自动说明 learned approximation 满足同一 inequality。

### 第 10 题解答：从可微流到守恒密度与 CNF（8 分）

#### 10.1 Variational equation 与 Liouville（2.5 分）

flow 满足

$$
\partial_t\phi_{0,t}(x_0)=f(t,\phi_{0,t}(x_0)).
$$

对 $x_0$ 求导，chain rule 给

$$
\dot J_t=(\nabla_xf)(t,X_t)J_t,
\qquad J_0=I.
$$

在 $J_t$ 可逆的区间，Jacobi formula 为

$$
\frac d{dt}\det J_t
=\det J_t\operatorname{tr}(J_t^{-1}\dot J_t).
$$

代入 variational equation，并用 trace cyclicity：

$$
\operatorname{tr}(J_t^{-1}(\nabla f)J_t)
=\operatorname{tr}(\nabla f)
=\nabla\cdot f.
$$

于是

$$
\frac d{dt}\log|\det J_t|
=\nabla\cdot f(t,X_t).
$$

积分后 $\det J_t=\exp(\int_0^t\nabla\cdot f(s,X_s)ds)>0$，但这是建立在 classical differentiable flow 和共同存在域上的结论。

#### 10.2 换元与沿轨迹 log density（1.5 分）

质量守恒的 finite change of variables 是

$$
p_t(\phi_{0,t}(x_0))|\det J_t|=p_0(x_0).
$$

取 log：

$$
\log p_t(X_t)=\log p_0(x_0)-\log|\det J_t|.
$$

沿时间求导即得

$$
\frac d{dt}\log p_t(X_t)
=-\nabla\cdot f(t,X_t).
$$

注意这不是声称固定空间点的 $\partial_t\log p=-\nabla\cdot f$；还缺 advection term。

#### 10.3 Strong form 与 weak form（2 分）

chain rule 给

$$
\frac d{dt}\log p_t(X_t)
=\partial_t\log p_t(X_t)
+f(t,X_t)\cdot\nabla\log p_t(X_t).
$$

乘以 $p$ 并整理：

$$
\partial_tp+f\cdot\nabla p+p\nabla\cdot f=0,
$$

即

$$
\partial_tp+\nabla\cdot(pf)=0.
$$

对 compactly supported smooth test function $\psi$，空间分部积分得

$$
\frac d{dt}\int\psi(x)p_t(x)dx
=\int\nabla\psi(x)\cdot f(t,x)p_t(x)dx,
$$

在有边界时还要保留/按 boundary condition 消去 boundary flux term。

#### 10.4 Boundary ledger（1 分）

- periodic boundary：两端/相对面 flux 抵消，总质量守恒；
- no-flux boundary：$pf\cdot n=0$，域内总质量守恒；
- open boundary：$d\int_\Omega p/dt=-\int_{\partial\Omega}pf\cdot n$，流入流出必须记账，不能把 mass drift 一律叫数值误差。

#### 10.5 Exact theorem 不自动传给 solver map（1 分）

Euler map $F_h(x)=x+hf(t,x)$ 的 Jacobian 是 $I+h\nabla f$；粗步长可使 determinant 为零或变号，造成 folding，即使 exact flow 始终 orientation-preserving。RK 也有自己的 finite-step map 和误差。至少检查 step refinement 下的 state/global error、$\det\nabla F_h$ 或 injectivity proxy、log-density residual、mass/flux ledger 和 event/boundary miss 中两项。

### 第 11 题解答：Itô—Fokker–Planck—概率流—反向时间（9 分）

#### 11.1 Itô formula 与 generator（2 分）

对 $\varphi(t,x)\in C^{1,2}$：

$$
d\varphi(t,X_t)
=\left[
\partial_t\varphi
+f^T\nabla\varphi
+\frac12\operatorname{tr}(D\nabla^2\varphi)
\right]dt
+(\nabla\varphi)^TG\,dW_t.
$$

二阶 trace 项来自 $dX_i\,dX_j=D_{ij}dt$，亦即 Brownian quadratic variation；ordinary chain rule 会漏掉它。time-homogeneous test function 的 generator 为

$$
\mathcal L\varphi
=f^T\nabla\varphi
+\frac12\operatorname{tr}(D\nabla^2\varphi).
$$

若 $\varphi$ 含时，还使用 $\partial_t+\mathcal L$。

#### 11.2 从 weak evolution 到 Fokker–Planck（2 分）

适当可积与 adapted 条件下，Itô integral 均值为零，所以

$$
\frac d{dt}\mathbb E[\varphi(X_t)]
=\mathbb E[(\mathcal L\varphi)(X_t)].
$$

写成密度积分：

$$
\frac d{dt}\int\varphi p\,dx
=\int f_i\partial_i\varphi\,p\,dx
+\frac12\int D_{ij}\partial_{ij}\varphi\,p\,dx.
$$

一次和两次分部积分后

$$
\int\varphi\left[
-\partial_i(f_ip)
+\frac12\partial_{ij}(D_{ij}p)
\right]dx.
$$

由 test functions 的任意性，得到

$$
\partial_tp=-\nabla\cdot(fp)
+\frac12\sum_{i,j}\partial_{ij}(D_{ij}p).
$$

若 regularity 不足，这一等式应保留为 weak/distributional form，不能假装 pointwise classical derivatives 都存在。

#### 11.3 Current、PF velocity 与 reverse drift（2.5 分）

定义

$$
[\nabla\cdot(Dp)]_i=\sum_j\partial_j(D_{ij}p).
$$

Fokker–Planck 可写为

$$
\partial_tp=-\nabla\cdot j,
$$

其中

$$
j=fp-\frac12\nabla\cdot(Dp).
$$

若 $p>0$，令 deterministic velocity $v=j/p$：

$$
v=f-\frac1{2p}\nabla\cdot(Dp).
$$

则 $\partial_tp+\nabla\cdot(pv)=0$，因此其 ODE 在适当条件下复制同一 marginal density path。

对 $Y_s=X_{T-s}$ 使用正常递增的 $s$，reverse diffusion matrix 在对应 forward time 相同，drift 为

$$
b_{\rm rev}(t,x)
=-f(t,x)+\frac1{p_t(x)}\nabla\cdot(D(t,x)p_t(x)).
$$

若用 decreasing-$t$ notation 写采样公式，符号会随 $dt<0$ 表达改变；评分接受等价约定，但必须先定义时钟，不能只凭记忆抄正负号。

#### 11.4 State-independent diffusion 的 score form（1 分）

若 $D=D(t)$ 与 $x$ 无关，

$$
\frac1p\nabla\cdot(Dp)=D\nabla\log p=Ds_t.
$$

故

$$
v_{\rm PF}=f-\frac12Ds_t,
\qquad
b_{\rm rev}=-f+Ds_t.
$$

half score 属于无噪声 probability-flow ODE；full score 属于仍含 $G\,d\bar W$ 的 reverse SDE。把二者互换会改变 Fokker–Planck 方程。

#### 11.5 Marginal、path 与 DSM（1.5 分）

- forward SDE 与其 PF ODE：共享 one-time marginals；通常不共享 transition kernel、path law，且前者 quadratic variation 为 $\int Ddt$，后者有限变差、quadratic variation 为零；
- 从正确 $p_T$ 初始化、使用 exact score 的 reverse SDE：在定理条件下复现 forward process 的 time-reversed path law，而不仅是末端 marginal；
- 一种 DSM objective 是
  $$
  \mathbb E\left[\lambda(t)\left\|s_\theta(t,X_t)-\nabla_{x_t}\log p(X_t\mid X_0)\right\|^2\right].
  $$
  对每个 $(t,X_t=x)$，平方损失最优解是 conditional expectation
  $$
  \mathbb E[\nabla_x\log p(X_t\mid X_0)\mid X_t=x]
  =\nabla_x\log p_t(x),
  $$
  即 marginal score；这依赖可交换求导/积分与 support regularity。

## 四、D 区：反例、失败边界与纠错

### 第 12 题解答：四个最小失败机制（8 分）

每题 2 分：具体对象 0.75，验证 0.75，最小修正 0.5。其他正确、同等简洁的反例也得满分。

#### 12.1 连续不推出唯一（2 分）

取

$$
x'=2\sqrt{|x|},\qquad x(0)=0.
$$

$f(x)$ 连续但在零点不 local Lipschitz。对任意 $c\ge0$，

$$
x_c(t)=
\begin{cases}
0,&0\le t\le c,\\
(t-c)^2,&t\ge c
\end{cases}
$$

都是 $C^1$ solution；另有恒零解。它推翻“continuous vector field 自动给 unique IVP/flow”。最小修正是加入 state local-Lipschitz 等 uniqueness condition；Peano continuity只支持 existence。

#### 12.2 连续稳定不推出 Euler 稳定（2 分）

取

$$
y'=-100y.
$$

exact solution $e^{-100t}y_0$ 指数衰减。Euler 用 $h=0.03$ 时

$$
y_{n+1}=(1-3)y_n=-2y_n,
$$

故 magnitude 按 $2^n$ 增长。它推翻“stable ODE 可用任意 explicit step”。最小修正是要求 $h\lambda$ 落在 method stability region，并另做 accuracy refinement。

#### 12.3 零导数集合不等于极限集（2 分）

用第 6 题 oscillator：

$$
V=\tfrac12(q^2+v^2),\qquad\dot V=-v^2.
$$

$\{\dot V=0\}$ 是整条 $v=0$ 轴，但在 $(q,0)$、$q\ne0$ 处 $\dot v=-q\ne0$，轨迹立即离开。它推翻“$\dot V=0$ 的所有点都是 equilibrium/limit points”。最小修正是找 largest invariant subset，并检查 compactness/positive-definiteness 等 LaSalle 条件。

#### 12.4 相同 marginal 不等于相同过程（2 分）

令

$$
X_t=W_t,
\qquad
Y_t=\sqrt t\,Z,
$$

其中固定 $Z\sim\mathcal N(0,1)$。对每个 $t$，二者都服从 $\mathcal N(0,t)$；但

$$
[X]_T=T,
\qquad
[Y]_T=0,
$$

因为 $Y$ 是一条随机但 finite-variation 的确定形状曲线。故 marginals 不决定 path law。等价地，在 reverse diffusion 中把 full-score 改成 PF half-score、却仍保留 noise，会改变 probability current 与 marginals。最小修正是分别验收 marginal PDE、transition/coupling 与 quadratic variation，并匹配 drift 的 noise coefficient。

### 第 13 题解答：连续生成模型报告审计（7 分）

#### 13.1 Well-posedness 与 global flow（1.5 分）

低 training loss 没有提供：vector field 对 state 的 local/global Lipschitz 或 one-sided condition、measurability/time regularity、growth bound、domain invariance、boundary behavior、finite-time blow-up 排除、backward completeness。局部 unique flow 只给 diffeomorphism onto image；要声称整个 state space 上 global bijection，还要共同 forward/backward existence 与适当 surjectivity。

#### 13.2 Likelihood ledger（1.5 分）

至少分开：

- state trajectory error 与 log-density augmented-state error；
- exact divergence 与 Hutchinson/trace-estimator variance/bias；
- adaptive tolerance、dense output、event/end-time 与 stiffness error；
- continuous CNF likelihood 与 finite-solver likelihood；
- terminal/base density evaluation 与 finite precision。

应做 coupled refinement、独立 trace probes、mass/change-of-variables residual 和 solver/status审计。`success` 只表示软件按接口终止，不表示 exact likelihood。

#### 13.3 样本图不能认证的量（1.5 分）

20-step cherry-picked samples 不能认证 marginal score $L^2(p_t)$ error、rare modes/support coverage、reverse transition law、likelihood、calibration、terminal mismatch、discretization convergence、seed variability或训练数据记忆。至少要有 held-out quantitative metrics、multi-seed interval、exact/controlled toy oracle、step refinement 和 mode/coverage diagnostics。

#### 13.4 “相同过程”的最小修正（1 分）

应写：在 exact score、正确初始化和 regularity 条件下，PF ODE 被构造为与 forward SDE 具有相同 one-time marginal density path。它通常不是同一个随机过程：PF ODE 的条件轨迹为 finite variation，SDE 有非零 quadratic variation，transition kernel 和 path law不同。

#### 13.5 最小验证与可接受结论（1.5 分）

一个合格最小方案：固定 compute/NFE，扫描 steps/tolerances；至少三到五个训练 seeds 与独立 sampling seeds；held-out likelihood或分布指标；report mean/interval；记录 solver failures、non-finite、mode drop、boundary/endpoint issue；toy problem 上用 analytic score/density 分离 model 与 solver error。

可接受改写示例：

> 在所报告数据、seed 与 20-step solver 合同下，该模型达到给定 held-out 指标和样本质量；step refinement 显示剩余 finite-step gap 为某区间。当前实验不证明 learned field 全局可逆或 score 精确；PF ODE 与 SDE 只在所述条件下共享 one-time marginals，其 path laws 仍不同。

## 五、E 区：AI 迁移与研究合同

### 第 14 题解答：连续时间生成模型的端到端合同（10 分）

下面给出一份可得满分的参考合同。选择 CNF、flow matching 或 diffusion 的其他自洽方案同样可得分。

#### 14.1 对象、端点与解概念（1 分）

- data $X_0\sim p_{\rm data}$ 位于 $\mathbb R^d$ 或明确的 constrained domain；time $t\in[\varepsilon,T]$，其中 $\varepsilon>0$ 是否用于避开 singular endpoint 必须预注册；
- forward VP SDE 例：
  $$dX_t=-\tfrac12\beta(t)X_tdt+\sqrt{\beta(t)}dW_t;$$
- base endpoint 用真实 $p_T$、可计算近似 Gaussian，或明确记录 terminal mismatch；
- forward/reverse 使用 strong/weak SDE solution，PF sampler使用 Carathéodory/classical ODE solution；不能把数值数组本身定义为 exact solution。

#### 14.2 Well-posedness 与支持边界（1.5 分）

- $\beta$ 可测、有界且非负；learned score/vector field 对 state 至少 local Lipschitz，配合 linear-growth/dissipativity 排除 finite-time explosion；
- 若 state 有 simplex、sphere 或 bounded support，说明 tangent/no-flux/reflecting boundary，而不是默认 $\mathbb R^d$ 公式；
- 检查 endpoint score 是否发散、data distribution 是否 singular、反向 drift 在 $t\downarrow0$ 是否仍 integrable；
- 对 CNF 另检查 forward/backward completeness、divergence integrability 和 topology/support limitation。

“神经网络连续”不是充分的 unique/global-flow 证明；ReLU field 的 local Lipschitz 可用，但 global growth、time dependence 和 domain 仍需单独处理。

#### 14.3 训练对象与条件期望层（1.5 分）

例如用 DSM：

$$
\min_\theta\mathbb E_{t,X_0,X_t}
\left[\lambda(t)\|s_\theta(t,X_t)-\nabla_{x_t}\log p(X_t\mid X_0)\|^2\right].
$$

必须区分：

1. analytic conditional target；
2. population square-loss optimum $\mathbb E[target\mid X_t=x]=\nabla\log p_t(x)$；
3. finite-data/finite-capacity optimizer output $s_\theta$；
4. sampler 实际调用的 parameterization（score、noise、$x_0$ 或 $v$）及转换系数。

flow matching 同理：conditional velocity target 不等于 marginal velocity本身，后者是 conditional expectation；finite network只近似它。

#### 14.4 Solver contract（1.5 分）

- reverse SDE 可用 EM/Milstein/高阶弱法，声明时间网格、noise coupling、endpoint rule；PF ODE 可用 RK/adaptive/implicit method，声明 atol/rtol、norm、max NFE；
- 预扫描 stiffness，尤其小噪声 endpoint、large guidance 与 fast schedule；必要时换 L-stable implicit/semilinear/exponential method并记录 nonlinear/linear solve；
- 报 accepted/rejected steps、NFE、score calls、wall time、non-finite/event/budget status；
- 至少一次 step/tolerance refinement，不把固定 20 步结果叫 continuous limit。

#### 14.5 六类误差分账（1.5 分）

| 层 | 典型验收 |
|---|---|
| model/score error | held-out DSM、analytic toy score、calibration by time/SNR |
| terminal mismatch | 比较真实 $p_T$ 与 chosen base 的 moments/KL 或可计算 bound |
| discretization | coupled step refinement、exact-score oracle、strong/weak/marginal metric |
| divergence/trace | exact small-$d$ trace、独立 probes、probe-count interval |
| Monte Carlo | fixed seeds、MCSE/confidence interval、effective sample count |
| finite precision | non-finite、mixed-precision residual、repeatability与精度升级 |

只有 discretization 随 $h\to0$ 消失；score 与 terminal mismatch可能形成 error floor。总误差表必须允许出现“某层主导，继续减步无收益”的结论。

#### 14.6 Gradient 对象（1 分）

若实际训练/微调用 finite solver，discrete adjoint/backprop 得到 $\nabla J_h$。用相同 fixed noise、同一 step schedule 的 central finite difference 或 tangent/adjoint inner-product test 验收它；再通过 $h\downarrow0$ 比较 $J_h$ 和 gradient 的 refinement gap，才讨论 continuous $\nabla J$。continuous adjoint 与 adaptive forward trajectory mismatch、checkpoint/interpolation、SDE noise coupling都要记录。

#### 14.7 评价与公平性（1 分）

预注册：held-out NLL/ELBO 或适用的 distribution metric、precision/recall 或 mode coverage、sample quality、calibration/OOD；训练 seeds 与采样 seeds 分离，报告均值和区间；固定 compute、score NFE、sampler budget 和 hyperparameter search budget；真实 wall time/hardware另列，不能用 NFE 代替全部成本。

#### 14.8 Failure states、回退与结论边界（1 分）

至少四类：

1. non-finite/state explosion：缩短区间、regularize field、换稳定 solver；
2. solver budget/stagnation：记录未收敛，不伪装 success，改容差/implicit/preconditioner；
3. score endpoint divergence或 mode collapse：调整 weighting/parameterization、保留 $\varepsilon$、增加 coverage audit；
4. terminal mismatch/step-refinement floor：改善 forward schedule/base，不能只减步；
5. trace variance过大：增加独立 probes或改 exact/structured divergence；
6. gradient check失败：冻结随机性、核对 $J_h$ 对象与 adjoint implementation。

有限样本上的低 loss、样本好看、某个 seed 的 FID/NLL 或 solver success 都不能升级为 global well-posedness、exact likelihood、score consistency或 universal superiority theorem。

## 六、评分后的学习处方

| 失分集中区 | 最可能的知识断点 | 回链 |
|---|---|---|
| 1、9 | existence、uniqueness、continuation、Gronwall量词 | [[常微分方程、初值问题与解的存在唯一性]] |
| 2、5、6 | 非正规瞬态、linearization、Lyapunov/LaSalle | [[线性 ODE 与矩阵指数]]、[[相图、平衡点与局部稳定性]]、[[Lyapunov 稳定性与能量函数]] |
| 3、7 | local/global error、stability region、stiff damping | [[Euler、Runge-Kutta 与离散化误差]]、[[刚性系统、绝对稳定域与隐式方法]] |
| 4、10 | flow、Jacobian、density、boundary ledger | [[流映射、Liouville 公式与连续正规化流]]、[[连续性方程与守恒律]] |
| 1、11、12 | Brownian path、Itô correction、marginal/path law | [[随机过程、Brownian 运动与二次变差]]、[[Itô 引理与随机微分方程]] |
| 8、11、13 | Fokker–Planck、PF、reverse clock、score系数 | [[Fokker-Planck 方程与概率流 ODE]]、[[时间反演、score 与扩散生成动力学]] |
| 14 | continuous model、finite solver与研究证据混账 | [[ODE、动力系统与 SDE MOC]]与[[实验 - ODE、动力系统与 SDE 累计复现门]] |

重做时不要从整章开始重读。先定位第一个断点，再完成：定义口述一次、关键式空白推导一次、最小反例一次、陌生 AI 情境迁移一次。只有在这些证据都独立留下后，才讨论状态升级。
