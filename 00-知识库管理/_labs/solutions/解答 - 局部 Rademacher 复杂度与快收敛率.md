---
type: solution
status: draft
area: [learning-theory/local-complexity, statistical-rates]
topic: "[[局部 Rademacher 复杂度与快收敛率]]"
exercise: "[[习题 - 局部 Rademacher 复杂度与快收敛率]]"
prerequisites: ["[[局部 Rademacher 复杂度与快收敛率]]"]
related: ["[[正则化 ERM 的稳定性]]", "[[核岭回归与 Gaussian Process 接口]]"]
created: 2026-08-23
updated: 2026-08-28
---

# 解答 - 局部 Rademacher 复杂度与快收敛率

> [!warning] 解释边界
> 本解答中的 $r^*$ 计算展示 fixed-point mechanism；它不是脱离 boundedness、Bernstein、peeling 与 empirical comparison 条件的独立风险定理。

## A. 识别与复述

### LT-LOC-A01

若 $f^*$ 是 class 内 population risk minimizer，excess loss 为

$$
g_f(z)=\ell_f(z)-\ell_{f^*}(z),
$$

class 为 $\mathcal G=\{g_f:f\in\mathcal F\}$。二阶矩 local slice 可写

$$
\mathcal G(r)=\{g\in\mathcal G:Pg^2\le r\}.
$$

star hull 是

$$
\operatorname{star}(\mathcal G,0)
=\{\alpha g:g\in\mathcal G,0\le\alpha\le1\}.
$$

正式 local theorem 常在 star hull 与相应 slice 上工作，使远端方向可按 radius 缩放。

### LT-LOC-A02

$\psi:[0,\infty)\to[0,infty)$ 是 sub-root，如果它 nondecreasing 且 $\psi(r)/\sqrt r$ 在 $r>0$ nonincreasing。positive fixed point $r^*$ 满足 $\psi(r^*)=r^*$。对 $r\ge r^*$，

$$
\psi(r)\le\sqrt{rr^*}\le r.
$$

### LT-LOC-A03

- global complexity：对整个 $\mathcal G$ 取 supremum；
- population local complexity：对由未知 $P$ 定义的 $Pg^2\le r$ 等 slice 取 supremum；
- empirical local complexity：用 $P_mg^2$ 等 observable radius 定义 data-dependent slice。

第三种可估，但 class 本身依赖 sample，必须用专门 empirical-local theorem，不是简单 plug-in。

## B. 手算与数值判断

### LT-LOC-B01

令 $t=\sqrt r\ge0$。fixed point 方程为

$$
t^2=0.2t+0.01.
$$

positive root：

$$
t=\frac{0.2+\sqrt{0.04+0.04}}2
=\frac{0.2+\sqrt{0.08}}2
\approx0.241421.
$$

所以

$$
\boxed{r^*\approx0.058284}.
$$

### LT-LOC-B02

$d/m=20/2000=0.01$，因此

$$
\psi(r)=2\sqrt{0.01r}+0.03
=0.2\sqrt r+0.03.
$$

令 $t=\sqrt r$：

$$
t^2=0.2t+0.03,
$$

positive root 为

$$
t=\frac{0.2+\sqrt{0.04+0.12}}2
=\frac{0.2+0.4}2=0.3.
$$

故

$$
\boxed{r^*=0.09}.
$$

常数使它比裸 $d/m=0.01$ 大，但 asymptotic order 仍是 $d/m$。

### LT-LOC-B03

$$
\sqrt{d/m}
=\sqrt{100/10000}
=0.1,
$$

而

$$
d/m=0.01.
$$

local fast-rate scale 小 10 倍。这里只比较 rate terms；实际 bound constants、confidence 与 noise可能改变有限样本优势。

## C. 推导与证明

### LT-LOC-C01

因 $r\ge r^*$ 且 $\psi(r)/\sqrt r$ nonincreasing：

$$
\frac{\psi(r)}{\sqrt r}
\le
\frac{\psi(r^*)}{\sqrt{r^*}}
=\frac{r^*}{\sqrt{r^*}}
=\sqrt{r^*}.
$$

所以

$$
\psi(r)\le\sqrt{rr^*}.
$$

又因 $r^*\le r$，

$$
\sqrt{rr^*}\le\sqrt{r^2}=r.
$$

### LT-LOC-C02

对

$$
\psi(r)=a\sqrt r+b,
$$

令 $t=\sqrt r$，fixed point 为

$$
t^2-at-b=0.
$$

positive root：

$$
t=\frac{a+\sqrt{a^2+4b}}2,
$$

故

$$
\boxed{
r^*=\left(\frac{a+\sqrt{a^2+4b}}2\right)^2.}
$$

若 $a^2\asymp d/m$ 且 $b\asymp d/m$，则 $a\asymp\sqrt{d/m}$、$\sqrt{a^2+4b}\asymp\sqrt{d/m}$，所以 $t\asymp\sqrt{d/m}$，最终 $r^*\asymp d/m$。

### LT-LOC-C03

选 base radius $r_0$，定义 shells

$$
\mathcal G_k
=\{g:2^{k-1}r_0<Pg^2\le2^kr_0\},
\qquad k=1,2,\ldots
$$

为第 $k$ 层分配

$$
\delta_k=\frac{6\delta}{\pi^2(k+1)^2},
$$

则 $\sum_k\delta_k\le\delta$。对每层用 radius $2^kr_0$ 的 local complexity/concentration，并 union bound，得到所有 shells 同时成立的 event。

现在 estimator 落在哪个 shell 无需事先知道：在共同 event 上，对其实际 shell 使用对应 inequality。sub-root fixed point 再把各层 fluctuation 与 radius 比较，从而解除“先知道 estimator radius 才能选择 theorem”的 circularity。

## D. 边界、反例与纠错

### LT-LOC-D01

令 $Z\in\{a,b\}$ 等概率。设 $f^*$ 的 loss vector 为

$$
(\ell_{f^*}(a),\ell_{f^*}(b))=(0,1),
$$

另一个 $f$ 的 loss vector为

$$
(1,0.6).
$$

excess loss 是

$$
g_f=(1,-0.4),
$$

在 $b$ 上为负，但

$$
Pg_f=\frac{1-0.4}{2}=0.3>0.
$$

所以 population minimizer 只保证 mean excess risk 非负，不保证逐点 dominance。

### LT-LOC-D02

考虑

$$
P_m\ell_w+\frac\lambda2\|w\|^2.
$$

regularizer 使 empirical objective 对 parameter strong convex，却不自动说明：

- population task loss 对 predictions/parameters有相同 curvature；
- design covariance 不退化；
- surrogate excess risk 与 target excess risk calibrated；
- noise 满足 variance–mean relation；
- learned representation 固定。

例如所有 $X$ 都落在一个低维子空间，parameter 正交方向的 curvature完全来自 regularizer，但对 task prediction risk既不增加也不提供 distributional信息。需要单独证明 $Pg^2\le B(Pg)^\beta$ 或相应 curvature transfer。

### LT-LOC-D03

令 $\mathcal X$ 为无限集合、target 恒为 0，函数类包含所有 $\{0,1\}$-valued functions。对任意有限训练 sample，都存在大量函数在所有训练点输出 0、在 sample 外任意输出 0/1。它们 empirical loss 都为 0，但可有任意大的 population risk（取决于 sample 外设为 1 的区域）。

所以 zero empirical-loss set 可以非常复杂。要使 interpolation 进入 local theory，还需 norm/implicit bias、smoothness、compression 或 data geometry 把选中的 interpolant 限制在小 function class。

## E. AI 迁移

### LT-LOC-E01

Kernel ridge local audit：

1. Gram/population kernel eigenvalues；
2. regularization $\lambda$ 与 RKHS norm；
3. noise variance、sub-Gaussian/heavy-tail 条件；
4. squared-loss boundedness或 localized moment theorem；
5. effective dimension，例如 $\sum_j\lambda_j/(\lambda_j+\lambda)$；
6. local Rademacher envelope $\psi(r)$；
7. fixed point 与 confidence term；
8. approximate solver error；
9. kernel/$\lambda$ 是否用同一 validation data自适应选择；
10. certificate 的数值是否 nonvacuous。

### LT-LOC-E02

small parameter displacement 要转成 local generalization，需要：

- parameter-to-output uniform Lipschitz/Jacobian bound；
- parameter symmetries 已 quotient 或使用 function metric；
- linearization remainder 在整个 path/neighborhood受控；
- neighborhood radius 与 sample无不当自适应，或由 theorem处理；
- loss Lipschitz/curvature 与 range/tail；
- local class 的 Rademacher/covering bound；
- optimization确实留在该 neighborhood。

缺任一项，“参数走得少”都只是训练轨迹 observation。

### LT-LOC-E03

- 二维 loss landscape：选定两个 parameter directions 的 visualization，强烈依赖坐标与切片；
- Hessian sharpness：某个 parameter point 的局部二阶 operator，受 rescaling/reparameterization影响；
- local Rademacher complexity：一整个 local loss/function class 在 random signs 与 sample 上的 supremum。

flat Hessian 可能帮助建立 parameter perturbation bound，但还需 function metric、radius、sample process 与 curvature transfer。三者可在特定 theorem 中连接，却没有一般等价关系。
