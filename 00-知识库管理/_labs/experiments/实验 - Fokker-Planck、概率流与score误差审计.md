---
type: experiment
status: draft
area: [math/probability, math/stochastic-processes, math/sde, math/pde, math/numerical-analysis, ai/generative-modeling]
topic: "Fokker-Planck、概率流与score误差"
prerequisites: ["[[Fokker-Planck 方程与概率流 ODE]]", "[[Itô 引理与随机微分方程]]", "[[连续性方程与守恒律]]"]
related: ["[[习题 - Fokker-Planck 方程与概率流 ODE]]", "[[推导与实验 MOC]]", "[[时间反演、score 与扩散生成动力学]]"]
code: "[[00-知识库管理/_labs/code/fokker_planck_probability_flow_audit.py]]"
figure: "[[00-知识库管理/_assets/plots/dynamics/plot-fokker-planck-probability-flow-v2.svg]]"
created: 2026-08-19
updated: 2026-08-23
---

# 实验 - Fokker-Planck、概率流与score误差审计

> [!abstract] 实验问题
> Fokker–Planck 与 probability-flow 至少需要三道独立证据：density solver 是否按 probability current 守恒质量并收敛；SDE 与 ODE 即使 one-time marginals相同，path law 是否仍不同；score/model bias 与 ODE finite-step bias 是否被分别测量。本实验用 standard-library 单脚本逐项验收。

先看图回答：守恒 FPE solver、相同 marginals 下的 SDE/PF ODE path law 和 score model bias 怎样分别留下可见误差？

![[00-知识库管理/_assets/plots/dynamics/plot-fokker-planck-probability-flow-v2.svg|880]]

> [!figure] 实验图｜FPE 守恒、概率流路径律与 score/solver 分账
> A 报告 OU Fokker–Planck 守恒有限体积的 $L^1$ 网格阶、质量漂移和最小密度；B 比较相同 one-time marginals 下 SDE 与 probability-flow ODE 的 realized QV；C 分开 score scale bias 和 exact-score Euler bias。生成脚本：[[plot_stochastic_experiments_v2.py]]，计算合同来自 [[fokker_planck_probability_flow_audit.py]]；固定 seed，并保留守恒、QV 与 solver-order 断言。

**怎样读图。** A 同时验 mass、positivity 与 convergence；B 的终端方差相同不能覆盖路径 QV 差异；C 中 $h\to0$ 只压低 exact-score solver curve，不会让错误 score 的连续流回到正确密度。

**适用边界（图没有证明什么）。** 一维 OU、no-flux 网格和乘性 score error 是校准模型；图不证明高维 learned score、复杂边界或 adaptive probability-flow solver 的一般可靠性。

> [!question] 本实验的判别问题
> 为什么密度守恒、终端边缘匹配和路径 law 正确是三种不同要求，score 偏差又不能被时间步细化修复？

## 一、复现合同

运行：

~~~bash
python3 00-知识库管理/_labs/code/fokker_planck_probability_flow_audit.py
~~~

环境：

- Python 3 standard library；
- seed：$20260819$；
- 无 NumPy/SciPy/PyTorch；
- 所有随机分辨率共享 finest Brownian increments；
- FPE 使用 conservative finite volume 与 no-flux boundary；
- 图由脚本确定性生成。

Canonical SVG SHA-256：

~~~text
0751975ea07b4ba7481fdd97608e4f4a33142656d0eb85d19ef460ff85d18013
~~~

脚本在 FPE order、mass、positivity、SDE/PF marginal variance、QV orders、score zero-error identity 或 exact-score Euler order 任一越界时非零退出。

## 二、轨道 A：守恒有限体积求解 OU FPE

### 2.1 方程与 exact density

SDE：

$$
dX_t=-\kappa X_tdt+\sigma dW_t,
$$

参数：

$$
\kappa=0.8,\qquad\sigma=0.7,
\qquad
X_0\sim\mathcal N(0,0.4),
\qquad
T=0.6.
$$

FPE：

$$
\partial_tp
=
-\partial_x(-\kappa xp)
+\frac{\sigma^2}{2}\partial_{xx}p.
$$

Current：

$$
J=-\kappa xp-\frac{\sigma^2}{2}\partial_xp.
$$

Exact variance：

$$
V_T
=
V_0e^{-2\kappa T}
+\frac{\sigma^2}{2\kappa}
(1-e^{-2\kappa T}).
$$

### 2.2 Scheme

Domain 为 $[-6,6]$，cell-centered density。Interior face：

$$
J_{i+1/2}
=
a_{i+1/2}p_{i+1/2}^{\rm up}
-D\frac{p_{i+1}-p_i}{\Delta x},
\qquad
D=\frac{\sigma^2}{2}.
$$

Update：

$$
p_i^{n+1}
=
p_i^n-\frac{\Delta t}{\Delta x}
(J_{i+1/2}-J_{i-1/2}).
$$

Boundary flux 直接设为0。时间步满足

$$
\Delta t
\left(
\frac{\max|a|}{\Delta x}
+\frac{2D}{\Delta x^2}
\right)
\le0.42.
$$

### 2.3 结果

| cells | steps | $L^1$ density error | mass error | minimum $p$ | variance |
|---:|---:|---:|---:|---:|---:|
| 80 | 77 | $4.48895767\times10^{-2}$ | $2.22\times10^{-16}$ | $5.52\times10^{-20}$ | 0.38461171 |
| 160 | 216 | $2.34541959\times10^{-2}$ | $2.22\times10^{-16}$ | $3.16\times10^{-20}$ | 0.36383531 |
| 320 | 681 | $1.20127035\times10^{-2}$ | 0 | $1.28\times10^{-20}$ | 0.35311450 |

Observed $L^1$ order：

$$
0.95090981.
$$

Upwind drift 给接近一阶的整体精度；conservative flux telescope 把 mass drift压到 machine level。

> [!warning] 这不是 positivity theorem 的替代
> 三个 grids 上 minimum为正是实现证据；一般 positivity仍依赖 CFL、coefficient、boundary与roundoff。

## 三、轨道 B：同 marginals、不同 quadratic variation

### 3.1 两个过程

Initial：

$$
X_0\sim\mathcal N(0,v_0),
\qquad
v_0=0.4.
$$

SDE：

$$
dX_t=\sigma dW_t,
\qquad\sigma=0.9.
$$

Probability-flow ODE：

$$
\dot Z_t
=
\frac{\sigma^2}{2(v_0+\sigma^2t)}Z_t,
$$

exact：

$$
Z_t=Z_0\sqrt{\frac{v_0+\sigma^2t}{v_0}}.
$$

两者理论 marginal：

$$
\mathcal N(0,v_0+\sigma^2t).
$$

### 3.2 Marginal 结果

本实验使用5000条 paths。$T=1$：

| 对象 | empirical terminal variance |
|---|---:|
| SDE | 1.21530017 |
| PF ODE | 1.23393644 |
| theory | 1.21000000 |

两者都在 finite-sample fluctuation内接近同一 theory。

Cross-time covariance 在 $(s,t)=(0.5,1)$：

~~~text
SDE empirical = 0.80557466
PF empirical  = 1.00646354
SDE theory    = 0.80500000
PF theory     = 0.98693971
~~~

相同 marginal variances 没有固定 cross-time covariance。

### 3.3 QV refinement

| $N$ | mean SDE QV | mean PF ODE QV |
|---:|---:|---:|
| 16 | $8.03979313\times10^{-1}$ | $1.42914927\times10^{-2}$ |
| 32 | $8.07419689\times10^{-1}$ | $7.14646385\times10^{-3}$ |
| 64 | $8.06708586\times10^{-1}$ | $3.57332182\times10^{-3}$ |
| 128 | $8.10341478\times10^{-1}$ | $1.78667215\times10^{-3}$ |
| 256 | $8.08478437\times10^{-1}$ | $8.93337481\times10^{-4}$ |
| 512 | $8.08793575\times10^{-1}$ | $4.46668916\times10^{-4}$ |

Orders with $h=1/N$：

$$
p_{\rm SDE}=-0.00157771,
$$

$$
p_{\rm PF}=0.99996808.
$$

SDE QV趋于 $\sigma^2T=0.81$；smooth ODE partition squared increments按 $h$ 消失。

## 四、轨道 C：score bias 与 solver bias

### 4.1 Controlled score perturbation

True Gaussian score：

$$
s_t(x)=-\frac{x}{v_0+\sigma^2t}.
$$

使用

$$
\widehat s_t=(1+\varepsilon)s_t.
$$

即使 continuous ODE 精确求解，最终 variance relative error仍为

$$
r(\varepsilon)
=
\left(
\frac{v_T}{v_0}
\right)^\varepsilon-1.
$$

结果：

| $\varepsilon$ | relative variance error |
|---:|---:|
| -0.20 | -0.19858969 |
| -0.10 | -0.10478477 |
| -0.05 | -0.05384186 |
| 0 | 0 |
| 0.05 | 0.05690577 |
| 0.10 | 0.11704981 |
| 0.20 | 0.24780027 |

Score error不是 solver step error。

### 4.2 Exact-score solver sweep

固定 exact score，用 forward Euler 求 probability-flow ODE。对 terminal variance relative error拟合得到：

$$
p_{\rm Euler}=1.00375713.
$$

这条 curve 随 $h\to0$ 消失；上一节 $\varepsilon\ne0$ 的 continuous bias不会。

## 五、实验结论

~~~text
FPE L1 order             = 0.95090981
max FPE mass error       = 2.22044605e-16
SDE QV order             = -0.00157771
PF ODE QV order          = 0.99996808
final variance theory    = 1.21000000
exact-score Euler order  = 1.00375713
svg_sha256               = 0751975ea07b4ba7481fdd97608e4f4a33142656d0eb85d19ef460ff85d18013
~~~

由此分别验收：

1. FPE 的 conservative density computation；
2. same-marginal 不等于 same-path；
3. exact-score numerical convergence；
4. inaccurate-score continuous-model bias。

## 六、改参复现任务

至少完成两项：

1. 把 OU domain 从 $[-6,6]$ 缩到 $[-2,2]$，观察 reflecting boundary bias；
2. 故意使用 $p=0$ boundary，核对 lost mass 与 boundary flux；
3. 把 finite-volume CFL factor提到1.2，观察 negative density；
4. 将 drift 改为 constant，比较 exact translated Gaussian；
5. 增加 PF/SDE hitting-threshold experiment；
6. 把 score error改为 state-dependent $e(x)$；
7. 对 $\varepsilon$ 与 $h$ 建二维 error surface；
8. 用 central drift flux比较 oscillation/positivity；
9. 增加 particle KDE，分离 MC 与 bandwidth bias。

## 七、解释边界

本实验提供：

- 一维 smooth OU FPE 的受控 conservative example；
- Gaussian noising SDE/PF 同 marginal 的计算证据；
- QV 与 cross-time covariance 的 path-law反例；
- score/solver 双轴的 exact analytic separation。

本实验不提供：

- 任意 FPE weak/classical solution theorem；
- 高维 density solver可扩展性；
- learned neural score 的生成误差 bound；
- reverse-time SDE正确性；
- probability-flow global diffeomorphism保证；
- 学习者 mastered 证据。

## 八、复现记录

> [!check] 2026-08-19 canonical run
> 两次独立复跑输出与 SVG SHA-256 完全一致；脚本 assertions、两幅 SVG 的 XML 解析和 Sharp PNG 视觉终检均已通过。
