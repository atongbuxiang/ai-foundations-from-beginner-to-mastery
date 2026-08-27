---
type: solution
status: draft
area: [math/optimization, math/second-order-methods, ai/training]
topic: "Newton 法、Gauss-Newton 与拟 Newton 法"
exercise: "[[习题 - Newton 法、Gauss-Newton 与拟 Newton 法]]"
related: ["[[Newton 法、Gauss-Newton 与拟 Newton 法]]", "[[优化与凸分析 MOC]]"]
created: 2026-08-19
updated: 2026-08-19
---

# 解答 - Newton 法、Gauss-Newton 与拟 Newton 法

> [!warning] 使用顺序
> 每题先注明 curvature object 和 definiteness，再做 linear solve，最后才谈 convergence/acceptance；只算出一个 step 不代表该 step 应被接受。

## A. 识别与复述

### OPT-NEWTON-A01

二次模型

$$
m(p)=f(x)+g^Tp+\frac12p^THp
$$

的一阶条件是 $g+Hp=0$。若 $H\succ0$，这给唯一 model minimizer $p=-H^{-1}g$。

另一条路线令 $F(x)=\nabla f(x)$，线性化

$$
F(x+p)\approx F(x)+J_F(x)p=g+Hp=0.
$$

仍得同一方程。若 $H$ indefinite，$p$ 仍是线性化 root 的 Newton correction，但 $m(p)$ 没有 unconstrained minimum，且

$$
g^Tp=-g^TH^{-1}g
$$

符号不定。因此 root-finding interpretation 仍成立，model-minimization/descent interpretation 失效；需 trust region、modified Hessian 或 negative-curvature handling。

### OPT-NEWTON-A02

| 方法 | curvature object | PSD? | oracle/memory | 常用 globalizer |
|---|---|---|---|---|
| Newton | $\nabla^2f$ | 不一定 | Hessian/factorization 或 HVP | line search / trust region |
| GN | $J^TJ$ | 是 | residual JVP/VJP；可 QR/LSQR | damping / trust region |
| GGN | $J_z^TH_\ell J_z$ | 若 $H_\ell\succeq0$ 则是 | model Jacobian 与 output Hessian | damping / line search |
| BFGS | secant $B_k$ | $s^Ty>0$ 时可保 SPD | gradients；$O(d^2)$ | Wolfe line search |
| SR1 | secant rank-one | 不保 | gradients；$O(d^2)$ | trust region |
| L-BFGS | 最近 secant pairs 的 inverse action | pair 合格时通常 SPD | gradients；$O(qd)$ | line search |

GN/GGN 丢掉 model/residual 的二阶项；拟 Newton 不直接计算 Hessian，只拟合沿 trajectory 的 gradient differences。

### OPT-NEWTON-A03

- line search：固定 direction，选 $\alpha$；
- trust region：在 $\|p\|\le\Delta$ 内同时选方向/长度；
- modified Hessian/damping：令曲率 solve 更正定/可控；
- inner residual $\|Bp+g\|$：step 子问题解的精度；
- outer residual $\|\nabla f\|$：stationarity；
- trust ratio/Armijo：local model 对真实 objective 的可信度。

完整 iteration：固定 gradient/curvature batch与精度；构造 $B_k$；用带 preconditioner 的 solver 达到 forcing tolerance 或检测 negative curvature；由 line search/trust ratio 接受；记录 actual/predicted decrease；再检查 outer stationarity、step 与 objective/feasibility。任何 inner success 都不能跳过 outer acceptance。

## B. 手算与构造

### OPT-NEWTON-B01

写

$$
H=\begin{bmatrix}1&0\\0&9\end{bmatrix},
\quad
g(x)=\begin{bmatrix}x_1-2\\9x_2-18\end{bmatrix}.
$$

在 $x_0=0$：

$$
g_0=(-2,-18)^T.
$$

解 $Hp=-g$：

$$
p=(2,2)^T.
$$

Newton decrement：

$$
\lambda^2=g^TH^{-1}g
=(-2)^2+(-18)^2/9=4+36=40.
$$

预测下降为 $-\lambda^2/2=-20$。minimizer 解 $Hx=(2,18)^T$，确为 $(2,2)$；quadratic Taylor 模型就是原函数，所以实际下降也为 $20$。

### OPT-NEWTON-B02

$$
r(0)=(-1,-1)^T,
\qquad
J(0)=\begin{bmatrix}0\\2\end{bmatrix}.
$$

gradient：

$$
g=J^Tr=-2.
$$

GN matrix：

$$
J^TJ=4.
$$

又 $r_1''=2,r_2''=0$，所以 exact Hessian

$$
H=J^TJ+r_1r_1''=4-2=2.
$$

故

$$
p_{\rm GN}=-g/4=1/2,
\qquad
p_{\rm N}=-g/2=1.
$$

差异正来自 $\sum_i r_i\nabla^2r_i=-2$；此点 residual 不小，所以不能用 “近解 residual 小” 忽略它。

### OPT-NEWTON-B03

$$
Bs=s,\quad s^TBs=2,\quad y^Ts=3.
$$

$$
B_1=I-\frac{ss^T}{2}+\frac{yy^T}{3}
=\begin{bmatrix}1&0\\0&1\end{bmatrix}
-\frac12\begin{bmatrix}1&1\\1&1\end{bmatrix}
+\frac13\begin{bmatrix}4&2\\2&1\end{bmatrix}
$$

$$
=\begin{bmatrix}11/6&1/6\\1/6&5/6\end{bmatrix}.
$$

验证

$$
B_1s=(2,1)^T=y.
$$

矩阵 symmetric；leading minor $11/6>0$，determinant

$$
\frac{55-1}{36}=\frac32>0,
$$

故 SPD。若 $y=(-2,-1)$，则 $y^Ts=-3<0$，BFGS 正定性 theorem 不适用，且 update 的第二 rank-one term 为 negative denominator，可能产生 indefinite matrix；需 skip/damp/pair repair 或用 trust-region SR1。

## C. 推导与证明

### OPT-NEWTON-C01

令 $e_k=x_k-x^*$ 且 $g(x^*)=0$。full Newton：

$$
e_{k+1}=e_k-H(x_k)^{-1}[g(x_k)-g(x^*)].
$$

用 fundamental theorem of calculus（需要 gradient differentiable）：

$$
g(x_k)-g(x^*)=\int_0^1H(x^*+te_k)e_kdt.
$$

于是

$$
e_{k+1}=H(x_k)^{-1}\int_0^1
[H(x_k)-H(x^*+te_k)]e_kdt.
$$

inverse bound 用于 $\|H(x_k)^{-1}\|\le1/m$；Hessian Lipschitz 用于

$$
\|H(x_k)-H(x^*+te_k)\|
\le M(1-t)\|e_k\|.
$$

所以

$$
\|e_{k+1}\|
\le\frac Mm\int_0^1(1-t)dt\,\|e_k\|^2
=\frac{M}{2m}\|e_k\|^2.
$$

“足够近”保证整条线段仍在 regularity neighborhood、inverse bound 有效且 globalizer 接受 full step；若只接受 $\alpha<1$，递推多出 $(1-\alpha)e_k$，不再是同一 quadratic bound。

### OPT-NEWTON-C02

$$
f=\frac12\sum_ir_i^2.
$$

逐坐标：

$$
\partial_jf=\sum_ir_i\partial_jr_i,
$$

即 $g=J^Tr$。再微分：

$$
\partial_{kj}f
=\sum_i(\partial_kr_i)(\partial_jr_i)
+\sum_ir_i\partial_{kj}r_i,
$$

得到目标式。

线性化 $r(\theta+p)\approx r+Jp$，最小化 $\frac12\|r+Jp\|^2$ 的一阶条件是 $J^T(r+Jp)=0$，即 GN equation。

若 singular values 是 $\sigma_i(J)$，则 nonzero eigenvalues of $J^TJ$ 是 $\sigma_i^2$，故

$$
\kappa_2(J^TJ)=\kappa_2(J)^2.
$$

显式 normal equations 还会在形成 $J^TJ$ 时累积 rounding；QR/LSQR 直接对 $J$ 工作更可靠。

### OPT-NEWTON-C03

对任意 $z\ne0$：

$$
z^TB_+z
=z^TBz-
\frac{(z^TBs)^2}{s^TBs}
+\frac{(z^Ty)^2}{y^Ts}.
$$

把前两项视为 $B$-inner product 的 Cauchy remainder：

$$
z^TBz-\frac{(z^TBs)^2}{s^TBs}\ge0.
$$

若 remainder 为正，整体正；若 remainder 为零，则 $z$ 与 $s$ 在 $B$ metric 下共线，故 $z^Ty$ 是该非零比例乘 $s^Ty$，不为零，于是最后一项严格正。故 $B_+\succ0$。

strong Wolfe curvature condition

$$
|g_{k+1}^Tp_k|\le c_2|g_k^Tp_k|,\quad c_2<1
$$

配合 $s=\alpha p$ 与 $g_k^Tp<0$ 可推出

$$
y^Ts=\alpha(g_{k+1}^Tp-g_k^Tp)>0.
$$

若 $g_k,g_{k+1}$ 来自不同 noisy batches，该代数不能代表同一 smooth $f$ 沿同一 line 的 curvature；Wolfe theorem 的函数一致性假设已断裂。

## D. 反例与失败边界

### OPT-NEWTON-D01

取

$$
f(x,y)=\frac12x^2-\frac12y^2+2y.
$$

在 $(0,0)$，$g=(0,2)$、$H=\operatorname{diag}(1,-1)$。Newton solve 给 $p=(0,2)$，且

$$
g^Tp=4>0,
$$

是 ascent direction；更新到 $(0,2)$，那里 gradient 为零却是 saddle。

eigenvalue shift 取 $\tau>1$，$H+\tau I\succ0$，step 的 $y$ 分量为 $-2/(\tau-1)<0$，成为 descent，但大 $\tau$ 会很小。trust-region subproblem识别 $y$ 方向的 negative curvature；在半径 $\Delta$ 内会同时利用 linear term 与 boundary，给朝负 $y$ 的可控 step。前者抹去负曲率，后者显式利用负曲率。

### OPT-NEWTON-D02

- large residual：$\sum r_i\nabla^2r_i$ 可能主导，GN 偏差大；
- rank deficiency：$J^TJ$ singular，GN step 不唯一；
- negative curvature：exact Hessian 的负方向可能帮助离开 saddle，GN 有意丢掉；
- nonconvex robust/output loss：GGN 中 $H_\ell$ 也未必 PSD；
- normal equations：数值 conditioning 被平方；
- PSD 只表示 subproblem convex，不表示 curvature approximation 更接近 exact Hessian。

因此“稳定”与“准确”是两个属性；应比较 dropped term、rank、trust ratio 与 actual decrease。

### OPT-NEWTON-D03

设 true objective 在相邻点梯度差 $Hs=10^{-4}u$，但 independent mini-batch noise $\epsilon_{k+1}-\epsilon_k$ 的 norm 为 $10^{-1}$，则

$$
y=Hs+(\epsilon_{k+1}-\epsilon_k)
$$

几乎全是 noise，$s^Ty$ 可随机变号。

- pair filtering：丢掉 $s^Ty$ 太小/负的 pair，保护 SPD，但减少曲率信息；
- same batch：抵消一部分 sampling difference，但仍有 point-dependent sample curvature 与 bias；
- damping：把 $y$ 混向 $Bs$，提高正定性，不恢复丢失的真实 curvature；
- larger batch：降 variance，但提高单步成本，且 nonstationarity 仍在。

应直接记录 pair cosine、$s^Ty/(\|s\|\|y\|)$、skip rate 和 same-vs-different-batch sensitivity。

## E. AI 迁移

### OPT-NEWTON-E01

预注册示例：固定 gradient batch $B_g$ 与 curvature batch $B_H$，同时做 shared/disjoint ablation；HVP 用 FP32 accumulate；PCG forcing $\eta_k=\min(0.5,c\sqrt{\|g_k\|})$；检测 $d^THd\le\epsilon_{nc}\|d\|^2$ 时截断；preconditioner 单独报告 build/apply cost；用 trust ratio 调 damping/$\Delta$；inner 日志含 HVP count、relative residual、negative-curvature event，outer 含 gradient norm、actual/predicted decrease、accepted step、train/validation；按 processed examples、HVP-equivalent FLOPs 与 wall-clock三轴比较，多 seed。若用 GGN，应明确不检测 exact-Hessian negative curvature。

### OPT-NEWTON-E02

生成 $r(\theta)$，独立控制：加入不可消除 offset 改 terminal residual；让 Jacobian columns 接近 dependent 改 rank；加入 observation noise。方法：exact Newton+trust、QR-GN、formed-normal-equation GN、LM adaptive $\lambda$、L-BFGS+Wolfe。图：objective、parameter error、$\|\sum r_i\nabla^2r_i\|/\|J^TJ\|$、singular values、trust ratio、linear residual、function/JVP count、roundoff sensitivity。预期：residual 大时 GN 偏差增；rank 差时 normal equations 最先恶化；LM 稳但可能慢。

### OPT-NEWTON-E03

目标 $s=H^{-1}v$ 的估计误差可分为：

$$
\tilde s-s
=\underbrace{(H+\lambda I)^{-1}v-H^{-1}v}_{\text{damping bias}}
+\underbrace{\tilde s-(H+\lambda I)^{-1}v}_{\text{solve error}}
+\text{HVP/sample error}.
$$

CG truncation 由 residual 结合 $\kappa(H+\lambda I)$ 转成 solution error；indefinite/singular 时 ordinary CG contract 无效；curvature batch 改变的是所求 operator；outer influence scalar 还放大方向误差。应扫 $\lambda$、batch、tolerance，报告 residual 与 estimate stability，并用 small exact problem 校准，不能只说 “CG converged”。

