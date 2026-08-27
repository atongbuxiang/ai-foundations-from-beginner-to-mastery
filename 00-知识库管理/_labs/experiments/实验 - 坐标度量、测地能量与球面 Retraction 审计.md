---
type: experiment
status: draft
area: [math/riemannian-geometry, math/manifold-optimization, math/numerical-analysis, ai/geometric-learning]
topic: "坐标度量、测地能量与球面 Retraction"
prerequisites: ["[[Riemann 几何、测地线与流形优化]]", "[[Euler、Runge-Kutta 与离散化误差]]", "[[投影、约束与可行方向]]"]
related: ["[[习题 - Riemann 几何、测地线与流形优化]]", "[[解答 - Riemann 几何、测地线与流形优化]]", "[[推导与实验 MOC]]"]
code: "[[00-知识库管理/_labs/code/riemannian_metric_geodesic_retraction_audit.py]]"
figure: "[[00-知识库管理/_assets/plots/geometry/plot-riemannian-metric-geodesic-retraction-v2.svg]]"
created: 2026-08-19
updated: 2026-08-23
---

# 实验 - 坐标度量、测地能量与球面 Retraction 审计

> [!abstract] 实验问题
> 本实验建立三个相互独立的 Riemannian computation 门：同一 Euclidean circle 在 polar metric 中的内蕴长度与 Cartesian polygon approximation 是否相容；同一 geodesic image 的不同参数为何 length 相同而 energy 不同；sphere 上 tangent Euler step、normalization retraction 与 exponential map 的误差阶究竟怎样分账。

先看图判断：坐标表达不变的长度、依赖参数化的能量，以及 sphere Euler/retraction/exponential-map 三类误差应如何分别验收？

![[00-知识库管理/_assets/plots/geometry/plot-riemannian-metric-geodesic-retraction-v2.svg|880]]

> [!figure] 实验图｜坐标度量、测地能量与球面更新
> A 比较 polar metric 积分与 Cartesian 内接多边形的圆周长；B 对同一曲线像比较常速与非常速参数的 length/energy；C 分开 tangent Euler 的 constraint residual、normalization retraction 对 Exp 的点误差与 retraction 自身的 feasibility。生成脚本：[[riemannian_metric_geodesic_retraction_audit.py]]；全确定性，并对解析恒等式与二/三阶律设断言。

**怎样读图。** A 验证同一内蕴长度的两种坐标计算；B 中 length 相同而 energy 增大定位的是参数速度不均；C 不能把 Euler 的二阶约束残差、retraction 的三阶局部点差与机器精度可行性混成一个“更新误差”。

**适用边界（图没有证明什么）。** Euclidean unit circle、固定圆弧和单位球面是解析校准模型；图不证明一般流形上的测地完备性、任意 retraction 的阶，或实际 Riemannian optimizer 的全局收敛。

> [!question] 本实验的判别问题
> 为什么坐标不变性、曲线参数化、约束可行性和对 exponential map 的局部逼近阶必须拥有不同证据账本？

> [!note] 一句话结论
> Track A 得到 circle chord length 二阶收敛且 polar integral 到舍入误差等于 $2\pi$；Track B 得到同像曲线长度同为 $1.4$，非常速参数的 energy 严格更大且 midpoint error 二阶；Track C 得到 tangent Euler constraint residual 为二阶、normalization 与 exact Exp 的点差为三阶，而 normalization feasibility 到机器精度为零。

## 一、复现合同

在知识库根目录运行：

```bash
python3 00-知识库管理/_labs/code/riemannian_metric_geodesic_retraction_audit.py
```

环境：Python 3 标准库，不依赖 NumPy、SciPy、Matplotlib 或网络。全部轨道确定性，无随机数。

双跑与哈希验收：

```bash
python3 00-知识库管理/_labs/code/riemannian_metric_geodesic_retraction_audit.py
python3 00-知识库管理/_labs/code/riemannian_metric_geodesic_retraction_audit.py --output /tmp/riemannian-audit.svg
cmp 00-知识库管理/_assets/plots/geometry/plot-riemannian-metric-geodesic-retraction-v2.svg /tmp/riemannian-audit.svg
```

当前 canonical SVG SHA-256：

```text
4ab14057b6a547958ecfe9823fe98d4847ff6cdc43db84f9a01656cd1fad7937
```

脚本内置 assertions：

- polar metric analytic circle length error $<10^{-13}$；
- polygon length observed order 在 $(1.99,2.01)$；
- reparameterized energy midpoint order 在 $(1.99,2.01)$；
- same-path length 与 constant-speed energy 到舍入误差正确；
- sphere Euler residual order 在 $(1.999,2.001)$；
- normalization–Exp error order 在 $(2.96,3.02)$；
- normalization feasibility residual $<4\times10^{-16}$。

## 二、Track A：坐标 metric 与 circle length

### 2.1 Analytic identity

Euclidean plane 的 polar metric 是

$$
ds^2=dr^2+r^2d\theta^2.
$$

unit circle $r=1$、$\theta\in[0,2\pi]$ 上

$$
\dot r=0,
\qquad
\dot\theta=1,
$$

所以

$$
L=\int_0^{2\pi}\sqrt{0^2+1^2\cdot1^2}\,d\theta=2\pi.
$$

这是使用 polar coordinate components 算同一个 Euclidean geometric length。

### 2.2 Cartesian polygon approximation

用 $N$ 个均匀 vertices 的 inscribed regular polygon：

$$
L_N=2N\sin\frac\pi N.
$$

Taylor expansion

$$
\sin\frac\pi N
=\frac\pi N-\frac1{6}\left(\frac\pi N\right)^3+O(N^{-5})
$$

给

$$
2\pi-L_N
=\frac{\pi^3}{3N^2}+O(N^{-4}).
$$

因此对 mesh $h=1/N$，误差应为 $O(h^2)$。

### 2.3 结果

使用

```text
N = 12, 24, 48, 96, 192, 384
```

得到

```text
circle_length_order    = 1.99972479
polar_metric_max_error = 3.286260152890e-14
```

前者验证 chord discretization 的二阶 truncation；后者只反映 Python floating accumulation，不是 geometry error。

> [!warning] 证据边界
> 这不证明“任意坐标算法都 coordinate invariant”。它只验证已知 polar metric、unit circle 与一种确定性 quadrature。一般 chart overlap 还需追踪 metric transformation 和 condition number。

## 三、Track B：同一 path 的 length–energy 分离

### 3.1 两个参数化

取 circle arc angle $\alpha=1.4$：

$$
\gamma_1(t)=(\cos\alpha t,\sin\alpha t),
$$

$$
\gamma_2(t)=(\cos\alpha t^2,\sin\alpha t^2),
\qquad t\in[0,1].
$$

二者 image 相同，且方向一致。

### 3.2 Length

Speeds 是

$$
\|\dot\gamma_1(t)\|=\alpha,
$$

$$
\|\dot\gamma_2(t)\|=2\alpha t.
$$

故

$$
L(\gamma_1)=\alpha,
$$

$$
L(\gamma_2)=\int_0^12\alpha t\,dt=\alpha.
$$

### 3.3 Energy

$$
E(\gamma_1)
=\frac12\int_0^1\alpha^2dt
=\frac12\alpha^2=0.98,
$$

$$
E(\gamma_2)
=\frac12\int_0^14\alpha^2t^2dt
=\frac23\alpha^2
=1.306\overline6.
$$

所以同一 path image 下 constant-speed parameter energy 更小。

### 3.4 Midpoint quadrature

对 $\gamma_2$ 的 quadratic energy integrand 使用 midpoint rule。Composite midpoint 对 smooth integrand 是二阶：

$$
|E-E_N|=O(N^{-2}).
$$

结果：

```text
energy_midpoint_order        = 2.00000000
constant_speed_energy        = 0.980000000000
reparameterized_energy       = 1.306666666667
reparameterized_length_error = 4.440892098501e-16
```

> [!important] 对 geodesic solver 的含义
> 优化 discrete energy 时，node timing 是 objective 的一部分。若 nodes 严重聚集，即使 path image 合理，energy 与 Euler–Lagrange residual 也会被参数化影响。应同时报告 length、energy、speed variance，并做 mesh refinement/reparameterization。

## 四、Track C：sphere 上的三个 finite-step 对象

### 4.1 设置

取

$$
x=(1,0,0)\in S^2,
\qquad
v=(0,1,0)\in T_xS^2.
$$

步长为 $t$。

### 4.2 Tangent Euler point

$$
y_E=x+tv=(1,t,0).
$$

它不在 sphere 上：

$$
\|y_E\|^2-1=t^2.
$$

因此 squared-norm constraint residual 是 exact $O(t^2)$。

### 4.3 Normalization retraction

$$
y_R=R_x(tv)
=\frac{(1,t,0)}{\sqrt{1+t^2}}.
$$

它在 exact arithmetic 中精确满足 $\|y_R\|=1$。

### 4.4 Exact exponential map

$$
y_{\operatorname{Exp}}
=\operatorname{Exp}_x(tv)
=(\cos t,\sin t,0).
$$

$y_R$ 的 great-circle angle 是 $\arctan t$，所以

$$
\|y_R-y_{\operatorname{Exp}}\|
\asymp |\arctan t-t|
=\frac13t^3+O(t^5).
$$

### 4.5 结果

```text
euler_constraint_order     = 2.00000000
retraction_exp_order       = 2.97089189
retraction_feasibility_max = 3.330669073875e-16
```

Observed third order 未精确等于 3，是因为拟合包含最大步 $t=0.4$ 等有限渐近区间；缩小步长会更接近 3，过小则会进入舍入区。

### 4.6 不能混账

| 对象 | 在 sphere 上？ | 与 initial tangent 一阶相容？ | 与 Exp 的当前点差 |
|---|---:|---:|---:|
| $x+tv$ | 否 | 是 | $O(t^2)$ |
| normalization $R_x(tv)$ | 是 | 是 | $O(t^3)$ |
| $\operatorname{Exp}_x(tv)$ | 是 | 是 | 0 |

“都朝 $v$ 方向走”不能替代 finite-step 区分。

## 五、失败门与排错顺序

若 assertion 失败，按顺序检查：

1. **Track A order**：是否把 $h=1/N$ 写反、误用外接 polygon、误差取了 signed negative；
2. **Track B energy**：是否漏 $1/2$、把 speed 当 coordinate derivative而不是 geometric norm；
3. **Track B length**：是否对 $2\alpha t$ 忘记绝对值或改变了 interval；
4. **Track C Euler**：constraint residual 是 $\|y\|^2-1$，若用 $\|y\|-1$ 仍为二阶但常数不同；
5. **Track C retraction**：是否先把非 tangent vector作为 $v$；
6. **Order window**：是否包含太大步导致 pre-asymptotic，或太小步导致 roundoff；
7. **Artifact**：是否改变 label/float formatting 导致 hash变化但数学值不变。

## 六、改参任务

### 6.1 Radius 与 coordinates

把 unit circle 改半径 $R=0.3,2,10$，验证：

$$
G_{\theta\theta}=R^2,
\qquad
L=2\pi R,
$$

而 normalized relative polygon error 的二阶不变。

### 6.2 Reparameterization family

改成 $\phi(t)=t^p$，$p>0$。推导

$$
E_p
=\frac12\alpha^2p^2\int_0^1t^{2p-2}dt
=\frac{\alpha^2p^2}{2(2p-1)}
$$

要求 $p>1/2$ 才有 finite energy。验证 $p=1$ 最小，并研究 $p\downarrow1/2$ 的 quadrature condition。

### 6.3 非单位 tangent

令 $\|v\|=a$，验证

$$
\|x+tv\|^2-1=a^2t^2,
$$

且 normalization–Exp 的 leading error 与 $a^3t^3$ 同阶。

### 6.4 从 analytic sphere 到 learned decoder

把 Track C 换成 decoder $g(z)$：

- 计算 $G=J_g^\top J_g$；
- 报告 $\lambda_{\min}$ 与 $\kappa$；
- 用 multiple shooting/path discretization；
- 增加 endpoint、energy、speed 和 mesh refinement；
- 在 rank-collapse region 预期触发 failure，而不是只加 damping 隐藏退化。

## 七、证据边界与状态

本实验使用 analytic synthetic objects，能验证：

- 实现是否保持已知 coordinate-length identity；
- quadrature order 是否匹配解析展开；
- sphere 三种 update 的 feasibility/error orders。

不能验证：

- 任意 manifold 的 geodesic solver 全局正确；
- learned decoder metric 代表真实 data semantics；
- 某种 retraction 在所有 objective 上优于 Exp 或其他 retraction；
- RGD 在未检查 smoothness/step/lower-bound 时收敛。

当前状态仍为 `draft / composed / not-attempted`：canonical artifact 已生成并双跑一致，但学习者尚未完成改参、故障注入、解释和 delayed reproduction。
