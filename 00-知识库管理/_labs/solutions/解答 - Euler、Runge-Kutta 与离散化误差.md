---
type: solution
status: draft
area: [math/ode, math/numerical-analysis, ai/neural-ode, ai/generative-modeling]
topic: "Euler、Runge-Kutta 与离散化误差"
exercise: "[[习题 - Euler、Runge-Kutta 与离散化误差]]"
related: ["[[Euler、Runge-Kutta 与离散化误差]]", "[[ODE、动力系统与 SDE MOC]]", "[[练习与测验 MOC]]"]
created: 2026-08-19
updated: 2026-08-19
---

# 解答 - Euler、Runge–Kutta 与离散化误差

> [!important] 误差约定
> 除非另行说明，以下 $d_{n+1}$ 指从精确状态出发、做一次数值步得到的未归一化缺陷，$\tau_{n+1}=d_{n+1}/h$，$e_n=y(t_n)-y_n$ 指网格点全局误差。符号正负不影响阶，但每道计算题都固定使用“精确值减数值值”。

## A. 识别、定义与公式结构

### DYN-RK-A01

1. **四类状态对象**

   - exact trajectory 是初值问题的连续解 $t\mapsto y(t)$；
   - exact flow step 是 $\Phi_{t_n,t_{n+1}}(y(t_n))=y(t_{n+1})$；
   - numerical grid state 是递推产生的有限序列 $y_0,y_1,\ldots,y_N$；
   - dense output 是在已接受网格步内部构造的插值函数 $\widetilde y(t)$。它依赖具体插值公式，不自动等于 exact trajectory。

2. one-step method 只用当前状态生成下一状态，可写为

   $$
   y_{n+1}=y_n+h_n\Psi(t_n,y_n,h_n).
   $$

   $\Psi$ 是 increment function。对 Euler，$\Psi=f(t_n,y_n)$；对 RK，它综合若干 stage slope。

3. exact-start defect 为

   $$
   d_{n+1}
   =y(t_{n+1})-
   \{y(t_n)+h_n\Psi(t_n,y(t_n),h_n)\}.
   $$

4. normalized local truncation error 为 $\tau_{n+1}=d_{n+1}/h_n$。因此同一方法的 $d=O(h^{p+1})$ 对应 $\tau=O(h^p)$。

5. global grid error 是 $e_n=y(t_n)-y_n$，它包含之前每一步缺陷经动力系统放大、衰减或旋转后的累计结果。

6. consistency 要求单步格式在 $h\to0$ 时逼近微分方程，例如 $\Psi(t,y,0)=f(t,y)$；order $p$ 通常指 $d=O(h^{p+1})$ 并在稳定性条件下得到 fixed-horizon global $e_n=O(h^p)$；convergence 是当最大步长趋零时数值解趋于精确解。

7. finite-horizon perturbation stability 控制两个受扰离散轨迹在有限时间窗中的距离；absolute stability 则针对测试方程 $y'=\lambda y$，要求放大因子满足 $|R(h\lambda)|\le1$。前者服务于收敛证明，后者解释衰减模态是否被数值格式错误放大。

8. NFE 是 vector-field evaluations；accepted step 更新解和时间；rejected step 不更新已接受状态，但其 stage evaluations 仍计入 NFE 与墙钟成本。

9. model error 来自 $f_\theta$ 与目标动力学不同；discretization error 来自用有限步数逼近给定 $f_\theta$ 的流；roundoff 来自有限精度运算。三者不能由同一个 tolerance 统一代表。

“Euler local error 是 $O(h^2)$”通常把 local error 定义为未归一化 defect；“是 $O(h)$”通常指 defect 除以 $h$ 后的 local truncation error。两者不矛盾，矛盾只会出现在省略定义时。

### DYN-RK-A02

四个常用方法为

$$
\begin{aligned}
\text{Euler: }&y_{n+1}=y_n+h f(t_n,y_n),\\
\text{Heun: }&k_1=f(t_n,y_n),\quad
k_2=f(t_n+h,y_n+hk_1),\\
&y_{n+1}=y_n+\frac h2(k_1+k_2),\\
\text{midpoint: }&k_1=f(t_n,y_n),\quad
k_2=f(t_n+h/2,y_n+hk_1/2),\\
&y_{n+1}=y_n+hk_2.
\end{aligned}
$$

Classical RK4 为

$$
\begin{aligned}
k_1&=f(t_n,y_n),\\
k_2&=f(t_n+h/2,y_n+hk_1/2),\\
k_3&=f(t_n+h/2,y_n+hk_2/2),\\
k_4&=f(t_n+h,y_n+hk_3),\\
y_{n+1}&=y_n+\frac h6(k_1+2k_2+2k_3+k_4).
\end{aligned}
$$

一般 $s$-stage RK 写成

$$
k_i=f\!\left(t_n+c_i h,
y_n+h\sum_{j=1}^s a_{ij}k_j\right),
\qquad
y_{n+1}=y_n+h\sum_{i=1}^s b_i k_i.
$$

$A=(a_{ij})$ 规定 stage 间依赖，$c_i$ 规定 stage time，$b_i$ 规定最终组合。explicit RK 要求 $A$ 严格下三角；internal consistency 是 $c=A\mathbf1$。

在 $c=A\mathbf1$ 下，至四阶的经典条件是

$$
\begin{array}{c|l}
1&b^\top\mathbf1=1\\
2&b^\top c=1/2\\
3&b^\top c^{\circ2}=1/3,\quad b^\top Ac=1/6\\
4&b^\top c^{\circ3}=1/4,\quad
b^\top CAc=1/8,\quad
b^\top A(c^{\circ2})=1/12,\quad
b^\top A^2c=1/24,
\end{array}
$$

其中 $C=\operatorname{diag}(c)$，幂 $\circ$ 是逐元素幂。对 $y'=\lambda y$，消去 stage 得

$$
R(z)=1+zb^\top(I-zA)^{-1}\mathbf1,\qquad z=h\lambda.
$$

stage 数只是计算图的宽度，并不强制系数满足 rooted-tree order conditions。例如任取四个 stage 却令 $b=(1,0,0,0)^\top$，方法退化为 Euler，只有一阶。

### DYN-RK-A03

embedded pair 共享 stages，却用 $b$ 与 $\widehat b$ 形成两个不同阶的结果；差值 $\delta=y_{n+1}^{[p]}-y_{n+1}^{[q]}$ 是 local error estimator，而非已知的 global error。

对 component $i$，常用尺度

$$
s_i=\operatorname{atol}_i+
\operatorname{rtol}\max(|y_{n,i}|,|y_{n+1,i}|),
$$

以及

$$
\operatorname{err}
=\sqrt{\frac1d\sum_{i=1}^d(\delta_i/s_i)^2}.
$$

$\operatorname{err}\le1$ 时通常 accept。controller 用 $h_{\rm new}=\eta h\operatorname{err}^{-1/(q+1)}$，再 clipping；PI controller 还结合上一步误差以减少步长振荡。dense output在步内插值；event root依赖它或专用根定位，max step 可防止跨过未解析结构。FSAL 复用前一步末 stage 作为下一步首 stage，因此 NFE 不总等于 stage 数乘 accepted steps。

tolerance sweep 检查结论是否随 rtol/atol 收紧而稳定；reference solution 需要更高精度、不同方法或解析解，避免共同偏差。continuous sensitivity/adjoint 对连续 ODE 目标求导；discrete adjoint 对实际 solver computation graph 求 $\nabla J_h$；checkpoint 保存部分 forward states，在内存与重算误差之间折中。

四个指标属于四层：$\operatorname{err}\le1$ 是本步 estimator 的加权判据；success 表示实现未触发失败条件；NFE 是成本代理；task loss 是下游任务指标。它们没有任何两者逻辑等价。

## B. 手算、构造与数值量级

### DYN-RK-B01

精确解为 $y(t)=e^t$。从 $y(t_n)=e^{t_n}$ 出发，Euler 一步给 $e^{t_n}(1+h)$，所以

$$
d_{n+1}=e^{t_n}(e^h-1-h)
=e^{t_n}\left(\frac{h^2}{2}+\frac{h^3}{6}+O(h^4)\right).
$$

递推 $y_{n+1}=(1+h)y_n$ 给 $y_N=(1+h)^N=(1+h)^{1/h}$。又

$$
\frac1h\log(1+h)
=1-\frac h2+\frac{h^2}{3}+O(h^3),
$$

故

$$
y_N
=e\exp\!\left(-\frac h2+\frac{h^2}{3}+O(h^3)\right)
=e\left(1-\frac h2+\frac{11}{24}h^2+O(h^3)\right).
$$

因此

$$
e-y_N=\frac e2h-\frac{11e}{24}h^2+O(h^3)
=\frac e2h+O(h^2).
$$

在 fixed horizon 上约有 $N=1/h$ 个 $O(h^2)$ defects；经稳定传播后总量为 $N O(h^2)=O(h)$，这就是 local 与 global 阶相差一阶的来源。

对 linear test equation，Heun 与 midpoint 具有同一 stability polynomial

$$
R_2(z)=1+z+\frac{z^2}{2},
$$

而 RK4 为

$$
R_4(z)=1+z+\frac{z^2}{2}+\frac{z^3}{6}+\frac{z^4}{24}.
$$

取 $h=1/2$、做两步：

$$
\begin{array}{c|c|c}
\text{方法}&y_2&|e-y_2|\\\hline
\text{Heun}&1.625^2=2.640625&0.077656828459\ldots\\
\text{midpoint}&1.625^2=2.640625&0.077656828459\ldots\\
\text{RK4}&1.6484375^2=2.71734619140625&0.000935637053\ldots
\end{array}
$$

Heun 与 midpoint 对 nonlinear ODE 并不等价；这里只因 $y'=y$ 的结果完全由共同的 $R_2$ 决定。

### DYN-RK-B02

一阶条件给 $b_1+b_2=1$；因 $c=(0,a)^\top$，二阶条件给 $b^\top c=ab_2=1/2$。所以

$$
b_2=\frac1{2a},\qquad b_1=1-\frac1{2a},\qquad a\ne0.
$$

三个常用选择为

$$
\begin{array}{c|ccc}
&a&b_1&b_2\\\hline
\text{Heun}&1&1/2&1/2\\
\text{midpoint}&1/2&0&1\\
\text{Ralston}&2/3&1/4&3/4.
\end{array}
$$

对 $y'=y^2,y_0=1$，

$$
k_1=1,\qquad
k_2=(1+ah)^2=1+2ah+a^2h^2.
$$

于是

$$
\begin{aligned}
y_1
&=1+h(b_1k_1+b_2k_2)\\
&=1+h(b_1+b_2)+2ab_2h^2+a^2b_2h^3\\
&=1+h+h^2+\frac a2h^3.
\end{aligned}
$$

若 defect 定义为 exact minus numerical，则

$$
d_1=\left(1-\frac a2\right)h^3+O(h^4).
$$

只对这个 IVP 和这个初始点，取 $a=2$ 可精确匹配 $h^3$ 系数，此时 $(b_1,b_2)=(3/4,1/4)$。这不使方法成为普适三阶：二 stage explicit RK 不可能满足三阶所需的全部独立条件，例如 $b^\top Ac=1/6$ 在此结构下恒为 $0$。它只消除了此问题上若干 elementary differentials 的特定组合。

### DYN-RK-B03

有

$$
k_1=-2,\qquad y_{n+1}^{[1]}=1+0.1(-2)=0.8,
$$

$$
k_2=-2(0.8)=-1.6,\qquad
y_{n+1}^{[2]}=1+\frac{0.1}{2}(-2-1.6)=0.82.
$$

取 $\delta=0.82-0.8=0.02$。scale 为

$$
s=10^{-3}+10^{-2}\max(1,0.82)=0.011,
$$

所以

$$
\operatorname{err}=\frac{0.02}{0.011}=1.81818\ldots>1.
$$

该步被拒绝。无 clipping 时

$$
h_{\rm new}
=0.9(0.1)(1.81818\ldots)^{-1/2}
=0.0667458\ldots.
$$

100维例子的 weighted RMS 为

$$
\sqrt{\frac{9^2}{100}}=0.9,
$$

因而接受；max norm 为 $9$，因而拒绝。这表明 RMS 允许少数 component 超标，是否合适取决于任务语义。

最后，$\delta$ 只是当前步、当前pair的 estimator；它可能有估计偏差、之后还会累计，并受 stability、roundoff、尺度选择和解的非光滑性影响。因此不能据此推出 endpoint global error $<10^{-2}$。

## C. 证明、阶条件与可微求解

### DYN-RK-C01

把精确一步写为

$$
y(t_{n+1})=y(t_n)+h\Psi(t_n,y(t_n),h)+d_{n+1}.
$$

减去数值一步，得到

$$
e_{n+1}=e_n+h\{\Psi(t_n,y(t_n),h)-\Psi(t_n,y_n,h)\}+d_{n+1}.
$$

取范数并用 Lipschitz 条件与 defect bound：

$$
\|e_{n+1}\|\le(1+hL_\Psi)\|e_n\|+Ch^{p+1}.
$$

令 $a=1+hL_\Psi$，从 $e_0=0$ 迭代得

$$
\|e_n\|
\le Ch^{p+1}\sum_{j=0}^{n-1}a^j
=\frac C{L_\Psi}h^p\{(1+hL_\Psi)^n-1\}.
$$

由 $1+x\le e^x$，

$$
\|e_n\|
\le\frac C{L_\Psi}
\left(e^{L_\Psi(t_n-t_0)}-1\right)h^p.
$$

若 $L_\Psi=0$，直接得到 $\|e_n\|\le nCh^{p+1}=C(t_n-t_0)h^p$，也等于上式在 $L_\Psi\to0$ 的极限。

假设的职责如下：fixed horizon 使指数常数不随 $h$ 发散；solution/field smoothness 用于一致 defect bound；包含两条轨迹的 bounded invariant region 使 $C,L_\Psi$ 统一；exact arithmetic 暂时排除了每步 roundoff forcing。若轨迹逸出 region，证明中的统一常数就失效。

对 variable steps，

$$
\|e_{n+1}\|
\le(1+L_\Psi h_n)\|e_n\|+C h_n^{p+1}.
$$

令 $H=\max_n h_n$，则 $h_n^{p+1}\le H^p h_n$。离散 Grönwall 给

$$
\max_{t_n\le T}\|e_n\|
\le C e^{L_\Psi(T-t_0)}
H^p\sum_n h_n
O(\|e_0\|)
\le C_T H^p.
$$

multistep method 的状态包含多个历史值；必须控制起步误差和伴随齐次差分方程的 root condition。仅把它伪装成标量 one-step recurrence 会遗漏 zero-stability，因此不能直接完成 Dahlquist 型收敛理论。

### DYN-RK-C02

对光滑 $f$，stage 在 $h=0$ 附近展开为

$$
k_i=f+h c_i(f_t+f_yf)+O(h^2),
$$

其中用了 $c_i=\sum_j a_{ij}$。于是 RK 一步为

$$
y_{n+1}=y_n+h(b^\top\mathbf1)f
+h^2(b^\top c)(f_t+f_yf)+O(h^3).
$$

与 exact Taylor

$$
y(t+h)=y+hf+\frac{h^2}{2}(f_t+f_yf)+O(h^3)
$$

比较，得到 $b^\top\mathbf1=1$ 与 $b^\top c=1/2$。

Classical RK4 有

$$
c=(0,1/2,1/2,1)^\top,\qquad
b=(1/6,1/3,1/3,1/6)^\top.
$$

逐项验算：

$$
\begin{aligned}
b^\top\mathbf1&=1,&b^\top c&=1/2,\\
b^\top c^{\circ2}&=1/3,&b^\top Ac&=1/6,\\
b^\top c^{\circ3}&=1/4,&b^\top CAc&=1/8,\\
b^\top A(c^{\circ2})&=1/12,&b^\top A^2c&=1/24.
\end{aligned}
$$

例如 $Ac=(0,0,1/4,1/2)^\top$，$A(c^{\circ2})=(0,0,1/8,1/4)^\top$，$A^2c=(0,0,0,1/4)^\top$，代入 $b$ 即得后三个非平凡等式。

对 $y'=\lambda y$，逐级代入 stages 或使用 stability function，得到

$$
R_4(z)=1+z+\frac{z^2}{2}+\frac{z^3}{6}+\frac{z^4}{24}.
$$

它只在 $z\to0$ 时以 $O(z^5)$ 逼近 $e^z$。多项式在 $z\to-\infty$ 时反而发散，所以“是 Taylor polynomial”绝不意味着全复平面准确或 A-stable。

$$
\begin{array}{c|ccc}
z&|R_E(z)|&|R_2(z)|&|R_4(z)|\\\hline
-1&0&0.5&0.375\\
-2&1&1&1/3\\
-3&2&2.5&1.375
\end{array}
$$

$z=-1$ 三者均不放大；$z=-2$ 时 Euler/RK2 仅在边界上，不能再现严格衰减，RK4 衰减；$z=-3$ 三者都不稳定。

| Order 验收 | Absolute stability 验收 |
|---|---|
| 比较一般光滑 ODE 的 Taylor/B-series 系数 | 固定 $z=h\lambda$ 检查 $|R(z)|\le1$ |
| 结论是 $h\to0$ 的 asymptotic order | 结论是有限步长下某模态是否被放大 |
| 依赖 $A,b,c$ 满足 rooted-tree conditions | 依赖 stability region 是否覆盖问题谱 |
| 高阶不保证大步稳定 | 大 stability region 不自动给高阶 |

### DYN-RK-C03

精确解与目标梯度为

$$
y(T)=e^{\theta T},\qquad
\frac{dJ}{d\theta}
=(e^{\theta T}-c)T e^{\theta T}.
$$

Euler 令 $q=1+h\theta$，有 $y_N=q^N$，因此

$$
\frac{dJ_h}{d\theta}
=(q^N-c)\frac{d q^N}{d\theta}
=(q^N-c)Nhq^{N-1}
=(q^N-c)Tq^{N-1}.
$$

离散 computation graph 为 $y_{n+1}=qy_n$。令 $\lambda_n=\partial J_h/\partial y_n$，则

$$
\lambda_N=y_N-c,\qquad
\lambda_n=q\lambda_{n+1}.
$$

参数梯度累计为

$$
\frac{dJ_h}{d\theta}
=\sum_{n=0}^{N-1}\lambda_{n+1}\frac{\partial y_{n+1}}{\partial\theta}
=\sum_{n=0}^{N-1}h\lambda_{n+1}y_n.
$$

由于 $y_n=q^n$ 且 $\lambda_{n+1}=(y_N-c)q^{N-n-1}$，每项都是 $h(y_N-c)q^{N-1}$；共 $N$ 项，恰好得到上式的 analytic derivative。

再由

$$
q^N
=\exp\!\left[\frac Th\log(1+h\theta)\right]
=e^{\theta T}
\exp\!\left[-\frac12\theta^2Th+O(h^2)\right],
$$

可知 $y_N-y(T)=O(h)$。同样 $q^{N-1}=e^{\theta T}\{1+O(h)\}$，故只要 $T,\theta,c$ 固定且不在导致高阶偶然抵消的退化点，$\nabla J_h-\nabla J=O(h)$。

central finite difference of $J_h$ 验证的是 $dJ_h/d\theta$，不是连续目标的 $dJ/d\theta$。continuous adjoint 对连续流求导；discrete adjoint 对已经选择的有限步 solver 求导；若 backward 时重新积分且不复用 forward path，adaptive grid、roundoff 与不可逆数值流可能使重建状态偏离原 forward states，进而产生额外 gradient mismatch。checkpoint adjoint通过保存部分 forward states降低该风险。

## D. 反例、错误诊断与系统审计

### DYN-RK-D01

1. **假。** $N=T/h$ 个 $O(h^2)$ local defects 通常累积成 $O(h)$ global error；$y'=y$ 即为反例。
2. **缺条件。** 需要 increment map 的稳定/Lipschitz 控制和轨迹留在统一 region。若小扰动可被每步无限放大，仅 consistency 不够。
3. **假。** 四 stage 只给四个 slope；系数仍须满足八个至四阶条件。令最终权重只取首 stage 就退化为 Euler。
4. **假。** order 只规定渐近指数，error constant、问题导数、stability 与 roundoff 均可不同。
5. **假。** weighted RMS 可让少数分量超过 1；100维单分量为 9 时 RMS 仅 0.9。
6. **假。** success 通常只说明算法到达终点、未触发步长下溢等失败；不构成 global error certificate。
7. **假。** 对 $y'=-10y$ 与 $h=0.2$，Euler factor $1-2=-1$，破坏 positivity；$h>0.2$ 时绝对值还大于 1。
8. **假。** dense interpolant 有自己的 degree/order；低阶插值可降低步内精度，event root 的误差还受横截条件影响。
9. **假。** Euler 给 $J_h$；continuous adjoint给 $J$。只有 $h\to0$ 且满足一致收敛等条件时两者梯度才趋近。
10. **假。** NFE 降低可能来自更平滑场、变小的动力尺度、宽松容差、更多 rejection accounting 差异或实现变化；单次 NFE 还不等于 wall time、trajectory error 或 task quality。

### DYN-RK-D02

1. 取 $y'=-100y$。Euler defect 在 $h\to0$ 确为 $O(h^2)$，但若 $h=0.03$，$R(-3)=-2$，每步把幅值翻倍。修复是检查 $h\lambda$ 是否落在 stability region，或切换 stiff solver；修复后仍不能声称 model error 小。

2. $g(t)=(t-1/4)(t-3/4)$ 在 $t=0,1$ 都为正，却在步内两次过零；只检查端点符号会漏掉两个 events。限制 max step、使用可靠 dense output并细分可降低风险；仍不能在无 root-separation/transversality 条件下保证发现任意触碰根或高频根。

3. normalized error 向量 $(9,0,\ldots,0)\in\mathbb R^{100}$ 的 RMS 为 0.9，步骤被接受。可用 component-specific atol、max norm或为关键变量加权；仍不能把 local normalized bound当成 endpoint global bound。

4. 取 $y'=\mathbf1_{t\ge1/2}$。跨越 $1/2$ 的一步内，$f$ 对 $t$ 不光滑，高阶 Taylor 导数不存在，classical RK order proof的前提断裂。应把 discontinuity 注册为 event并在其处截断、重启；重启后只在每个 smooth segment 内恢复阶结论。

5. 对 $y'=y$ 连续减小 $h$，truncation error先按 $h^p$ 下降；当每步舍入累计与 reference error 主导后，曲线进入平台甚至回升。应做 precision sweep、compensated diagnostics并换用更可靠 reference；这只能识别 numerical floor，不能证明解析解或模型正确。

五个例子分别打破“高阶必稳定、端点必见 event、平均尺度保护每个分量、名义高阶不需光滑、步越小越准”五个常见误推。

### DYN-RK-D03

现有证据只能支持：“在未完整记录的某次实现中，solver返回success；测得平均NFE由80降至20；validation loss下降。”其余结论都越层。

最小审计如下：

1. 固定并记录库、版本、method、rtol、atol向量、norm、initial/max/min step、dense-output/event设置、precision、device与随机种子。
2. success 只证明按实现定义到达终点，不证明 $10^{-3}$ global relative error。
3. NFE下降可能来自轨迹更易积分，也可能来自动力幅值塌缩、容差尺度改变、错误漏计 rejected steps、FSAL/批处理差异；必须同时报告 accepted/rejected steps与wall time。
4. 对 rtol/atol、max step、method和float32/64作 sweep，查看 state、gradient、loss 与结论排序是否收敛。
5. 分别报告 endpoint error、accepted-grid max error、dense-query error、event time error、task loss，不能只留一个总分。
6. continuous stability研究流对状态扰动的响应；absolute stability研究 solver 的 $R(h\lambda)$；training stability研究优化轨迹、loss/gradient波动。三者分别取证。
7. 若目标是实际 deployed solver，优先以 discrete adjoint 为基线；continuous adjoint测试连续目标；checkpoint adjoint用于内存—重算折中，并报告 checkpoint policy。
8. 对同一个 frozen accepted-step computation 用 central finite difference 检查 $\nabla J_h$；若检查 continuous gradient，则用独立高精度 reference。反向重算应与保存的 forward states逐点比较。
9. adaptive accept/reject 是 computed program 的分支；小参数变化可能改变步网格，使有限精度 map分段光滑甚至在边界附近不连续。需报告branch sensitivity。
10. solver card至少包含：问题/数据批、时间区间、状态尺度、solver+版本、全部 tolerance、precision、NFE记账、rejections、wall time、reference、误差定义、gradient mode、checkpoint、event/dense设置、硬件和seed。

只有 sweep 显示各指标进入稳定平台、reference 独立且 gradient audit 通过后，才能在指定问题、区间、精度和实现内声称“观察到约 $10^{-3}$ 的数值一致性”；仍不能无条件提升为 continuous model 的全局理论稳定性。

## E. AI迁移、综合推导与研究设计

### DYN-RK-E01

令 $h=T/N$，先引入对共同场 $f$ 做 Euler 的中间轨迹

$$
z_{k+1}=z_k+h f(t_k,z_k),\qquad z_0=y_0.
$$

模型轨迹满足

$$
h_{k+1}^{(N)}=h_k^{(N)}+hF_k^{(N)}(h_k^{(N)}).
$$

记 $r_k=h_k^{(N)}-z_k$，则

$$
\begin{aligned}
\|r_{k+1}\|
&\le(1+hL)\|r_k\|
+h\|F_k^{(N)}(h_k^{(N)})-f(t_k,h_k^{(N)})\|\\
&\le(1+hL)\|r_k\|+h\varepsilon_N.
\end{aligned}
$$

若 $r_0=0$，离散 Grönwall 给

$$
\max_{k\le N}\|r_k\|
\le
\begin{cases}
\dfrac{e^{LT}-1}{L}\varepsilon_N,&L>0,\\
T\varepsilon_N,&L=0.
\end{cases}
$$

另一方面，在 $f$ 对时间/状态足够光滑且轨迹留在有界 region时，Euler convergence 给

$$
\max_k\|z_k-y(t_k)\|\le C_T h.
$$

三角不等式因此得到

$$
\max_k\|h_k^{(N)}-y(t_k)\|
\le C_T\left(\frac1N+\varepsilon_N\right),
$$

其中 $T$ 可吸收到常数。还需 initial alignment $\|h_0^{(N)}-y_0\|\to0$；若不为零，bound需再加 $e^{LT}\|h_0^{(N)}-y_0\|$。

若 $\varepsilon_N\not\to0$，至多得到与该 ODE 相距 $O(\varepsilon_N)$ 的 tube，不能声称收敛到它。untied arbitrary blocks 未必共享随深度 refinement 的场；BatchNorm 让单样本更新依赖 batch statistics且训练/推理场不同；dropout引入随机更新，需要随机过程或均方分析；hard routing造成不连续/非 Lipschitz 分支。

合格的 depth-refinement 实验应从同一个 continuous parameterization $f_\theta(t,h)$ 采样 $N,2N,4N$ 个 blocks，共享参数或有可证明一致的插值；固定 $T$、初值和训练目标，报告相邻深度轨迹差、对高精度 ODE reference 的误差、$N^{-1}$ slope及任务指标。简单复制、插值或额外训练一个原网络的层并不自动形成同一 refinement family。

### DYN-RK-E02

一个可复现 benchmark 可以这样预注册：

1. **问题。** 主问题取有解析解的 nonstiff $y'=\theta y$；辅问题取二维平滑旋转/阻尼系统，另设一个有已知 crossing 的 event case。
2. **fixed refinement。** 对 Euler/Heun/RK4 使用相同 $N=2^k$，拟合 endpoint 与 max-grid error 的 log–log slope，期望分别趋近 1/2/4。
3. **adaptive sweep。** embedded RK 使用至少五组 rtol/atol；同时限制 max step，报告 accepted/rejected steps和总NFE。
4. **reference。** 解析解优先；无解析解时使用更高 precision、不同方法家族和至少两个数量级更紧 tolerance，并验证 reference 间一致。
5. **梯度。** 冻结参数点，对 $J_h$ 用高精度 central difference；比较 discrete backprop、continuous adjoint、checkpoint adjoint。另用解析 continuous gradient标识 discretization gap。
6. **轨迹。** 保存 forward accepted states；reverse重算时在同一时刻比较 state mismatch，并记录是否复用了 forward grid。
7. **分账。** trajectory endpoint/max error、event time、dense query error、task metric和gradient relative error分别画图。
8. **精度。** float32与float64在相同设置下对照；若 mixed precision，记录 stage/accumulator/parameter dtype。
9. **性能。** NFE、rejection、peak memory、wall time分开，并经过warm-up、多次重复和同步设备计时。
10. **验收。** 预先要求 observed order处于理论值附近、tightening tolerance后reference差下降、finite difference与discrete gradient在阈值内、结论排序在相邻两档设置不翻转。

failure 包括：误差进入roundoff floor、solver branch频繁翻转、event漏检、continuous/discrete gradients不随 refinement靠拢，或性能差异小于重复波动。最终结论必须限定为 smooth、nonstiff、指定时间区间、状态region、库版本和硬件；不得外推到 stiff、discontinuous 或训练分布外问题。

### DYN-RK-E03

理想连续关系是

$$
\Phi_{t,t+h}(x)
=x+\int_t^{t+h}v_\theta(s,x(s))\,ds,
$$

$$
\bar v_h(t,x)
=\frac{\Phi_{t,t+h}(x)-x}{h},
\qquad
F_h(x)=x+h\bar v_h(t,x)=\Phi_{t,t+h}(x).
$$

但这里的 average velocity 沿真实曲线平均，并依赖起点、时间与步长。把 instantaneous $v(t,x)$ 乘大 $h$、把任意 learned average 当 instantaneous field、把 trained finite map当 exact flow，都会遗漏 path dependence或compositional constraints。

三种路线的误差账本为：

- 高阶积分 instantaneous field：field estimation error + solver truncation/stability + roundoff；
- 学习 $\bar v_h$：step-conditioned model error + training-target/quadrature error + 一步实现误差；
- distill $F_h$：teacher/distillation error + map approximation error + 多步 composition/distribution-shift error。

精确自治流满足 semigroup；非自治流应写 two-parameter composition $\Phi_{t+h_1,t+h_1+h_2}\circ\Phi_{t,t+h_1}$。learned $F_h$ 一般不满足

$$
F_{h_1+h_2}=F_{h_2}\circ F_{h_1},
$$

故应把 composition residual 纳入训练或至少评估。

训练时随机采样 $h$ 并显式输入 $(t,h)$，覆盖多个 NFE budgets；测试时保留未见过的步长、非均匀 step schedules与多种composition partitions。每个设置分别报告 velocity/score estimation error、target quadrature error、solver error、最终sample quality和likelihood estimator error。

continuous likelihood 或 probability-flow claim 只有在模型确实定义了足够正则的连续 vector field、divergence积分与ODE flow一致且数值误差受控时成立；一个任意 finite-step map 不会自动继承该解释。训练审计应以 deployed discrete program 的 gradient 为 discrete-adjoint基线，用 finite difference抽检，再研究它与continuous gradient是否随 step refinement靠拢。

最终报告 NFE–quality–wall-time Pareto frontier，而不是单点“更快更好”。谨慎的结论模板是：

> 在指定数据、时间参数化、步长集合、precision和实现下，方法A在相同NFE预算上取得更好的经验指标；composition residual与离散gradient audit满足预注册阈值。该结果不证明 learned map 是某个唯一连续流，也不外推到未测试步长、stiff区域或continuous-likelihood精度。

## 自检结论

- 15个ID均已逐题作答；
- local defect、normalized truncation error与global error已分开；
- order、absolute stability、task accuracy与gradient object已分账；
- 数值结论均带 fixed-horizon、smooth/nonstiff、region或implementation边界。
