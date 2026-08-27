---
type: solution
status: draft
area: [math/riemannian-geometry, math/manifold-optimization, ai/geometric-learning]
topic: "Riemann 几何、测地线与流形优化"
exercise: "[[习题 - Riemann 几何、测地线与流形优化]]"
prerequisites: ["[[Riemann 几何、测地线与流形优化]]"]
related: ["[[练习与测验 MOC]]", "[[实验 - 坐标度量、测地能量与球面 Retraction 审计]]"]
created: 2026-08-19
updated: 2026-08-19
---

# 解答 - Riemann 几何、测地线与流形优化

> [!abstract] 使用方式
> 本文是独立详解，不以“见正文”代替推导。先闭卷完成 [[习题 - Riemann 几何、测地线与流形优化]]，保留原稿和时间，再逐项比对。评分重点不是公式数量，而是对象类型、条件、local/global 边界和 numerical evidence 的证据强度。

## A01 解答：八类对象的类型合同

| 对象 | domain → codomain | 依赖 | 坐标表示 | global boundary |
|---|---|---|---|---|
| $g$ | 每个 $p$ 上 $T_pM\times T_pM\to\mathbb R$ | smooth manifold + chosen metric | SPD matrix $G(x)$ | 不唯一；components 随 chart 变 |
| $d_g$ | $M\times M\to[0,\infty)$ | $g$ + path infimum | 通常无 closed form | 跨 components 可取 $+\infty$ 的扩展 convention；minimizer 未必存在 |
| $df_p$ | $T_pM\to\mathbb R$ | smooth $f$ | row/covector components $\partial_i f$ | 不依赖 metric |
| $\operatorname{grad}f(p)$ | point $p\mapsto T_pM$ | $df+g$ | $G^{-1}\partial f$ | metric-dependent |
| $\nabla$ | vector fields $(X,Y)\mapsto\nabla_XY$ | chosen connection | $\Gamma^k_{ij}$ | connection 不必来自 metric；$\Gamma$ 非 tensor |
| $\operatorname{Exp}_p$ | neighborhood in $T_pM\to M$ | Levi–Civita/geodesic flow | solve geodesic ODE | 一般仅 local diffeomorphism；有 cut locus |
| $\operatorname{Log}_p$ | normal neighborhood in $M\to T_pM$ | local inverse of Exp | BVP/closed form | 可多值、不连续或不存在 |
| $R$ | $TM\to M$ locally/globally | algorithmic choice | normalize/QR/polar 等 | 只要求一阶相容，不唯一 |
| $\mathcal T$ | $T_xM\to T_{R_x(\eta)}M$ | path/retraction + choice | projection/differential/parallel | 未必 isometric 或 exact parallel |

六个判断：

1. **错。** 同一 $\mathbb R^d$ 可配 $I$ 或 $e^{2\phi(x)}I$；smooth structure 只规定可微性。
2. **对。** $df_p(v)=v[f]$ 不需 metric；gradient 由 $g(\operatorname{grad}f,v)=df(v)$ 定义。
3. **错。** $d_g$ 输入 points；tangent vectors 用 $g_p$ 比较。
4. **错。** Sphere 上 $\operatorname{Exp}_p$ 把多个长度/方向送到同一点，antipode 尤其不唯一。
5. **错。** Retraction 只是 $R_x(0)=x$、$DR_x(0)=id$。Sphere normalization 与 standard metric 的 Exp 不相等。
6. **错。** Normal coordinates 可令任意 Riemannian manifold 在一点 $\Gamma=0$；sphere 仍有正 curvature。

## A02 解答：五组层级

### Curve 与参数

Curve image 是 subset $\gamma([a,b])$；parametrized curve 还记录访问顺序和速度；constant-speed 是特定参数选择。$\gamma(t)$ 与 $\gamma(t^2)$ 可有同像同向同长而 energy 不同。

### Geodesic 层级

- energy/length critical 是 first variation 为零；
- affinely parametrized energy-critical curve 满足 $\nabla_{\dot\gamma}\dot\gamma=0$；
- sufficiently short geodesic segment 局部 minimizing；
- global minimizing 还要实现两端点 distance；
- great circle 走过 antipode 后继续的 segment 是 geodesic 但非 minimizing。

### Completeness 与 compactness

$\mathbb R^d$ Euclidean complete、geodesically complete但非 compact。Open ball Euclidean 非 complete。Compact Riemannian manifold 必 complete。Hopf–Rinow 对 connected finite-dimensional Riemannian manifold 给 metric completeness、geodesic completeness、Exp 全定义和 closed-bounded compact 的等价，并保证 minimizing geodesic。Infinite-dimensional manifolds 上这些等价一般失败，不能迁移。

### 三类点间比较

Ambient distance 依 embedding；intrinsic distance 是 manifold curve length 的 infimum；semantic similarity 是 task-dependent score。Sphere 上 chord $2\sin(\theta/2)$ 与 geodesic angle $\theta$ 已给前两者不同；第三者甚至未必满足 metric axioms。

### 四类优化方向

- Riemannian gradient：inner-product metric 的 Riesz representative；
- natural gradient：Fisher metric 的特殊 Riemannian gradient；
- preconditioned direction：$P^{-1}\nabla f$，只有 $P$ 作为 smooth SPD field 并正确解释时才对应 metric；
- mirror descent：用 Bregman divergence/dual coordinates 做 finite update，一般不等于 Riemannian Exp step。

## A03 解答：constraint 与 decoder 合同

### Regular equality constraint

令 $c:\mathbb R^D\to\mathbb R^m$，$Dc(x)$ full row rank，$M=c^{-1}(0)$，则

$$
\dim M=D-m,
\qquad
T_xM=\ker Dc(x).
$$

配 induced metric 时

$$
P_x=I-Dc(x)^\top
[Dc(x)Dc(x)^\top]^{-1}Dc(x),
$$

$$
\operatorname{grad}f=P_x\nabla\bar f.
$$

有限更新需 projection/retraction；regular rank 是 manifold 前提。Tangent norm、$df(v)$ 与 objective 是 invariant；matrix components 和 $P$ 的坐标矩阵依表示。

### Decoder pullback

$g:\mathbb R^d\to\mathbb R^D$ full column rank 时，

$$
G(z)=J_g(z)^\top J_g(z)
$$

正定。Gradient 要解 $Gv=\partial f$；finite update 若 latent domain 是 open Euclidean set可直接加 components，但若另有 latent constraint 仍需 retraction。Sampled full rank 只是在样本点的 numerical fact；不证明 whole-domain immersion、injectivity、properness 或 population manifold。

“可计算”不等于“条件良好”：若 $\sigma_{\min}(J_g)$ 很小，则 $\kappa(G)=\kappa(J_g)^2$ 很大；若 rank collapse，$G$ singular；若 network 非 smooth 或 stochastic output metric 未定义，Riemannian assumptions 也缺失。

## B01 解答：polar plane

Jacobian

$$
J_F=
\begin{bmatrix}
\cos\theta&-r\sin\theta\\
\sin\theta&r\cos\theta
\end{bmatrix},
$$

故

$$
G=J_F^\top J_F
=\begin{bmatrix}1&0\\0&r^2\end{bmatrix}.
$$

若 $y=F(x)$、$v_y=J_Fv_x$，Cartesian $G_y=I$，所以

$$
G_x=J_F^\top G_yJ_F.
$$

Inverse metric $g^{rr}=1$、$g^{\theta\theta}=r^{-2}$。唯一非零 derivative 是 $\partial_rg_{\theta\theta}=2r$。代入

$$
\Gamma^k_{ij}
=\frac12g^{k\ell}
(\partial_ig_{j\ell}+\partial_jg_{i\ell}-\partial_\ell g_{ij})
$$

得

$$
\Gamma^r_{\theta\theta}=-r,
\qquad
\Gamma^\theta_{r\theta}
=\Gamma^\theta_{\theta r}=\frac1r.
$$

Geodesic equations：

$$
\ddot r-r\dot\theta^2=0,
\qquad
\ddot\theta+2\dot r\dot\theta/r=0.
$$

Radial line $\theta=\theta_0$ 且 $r=at+b$ 满足两式。Circle $r=R$、$\dot\theta\ne0$ 代第一式给 $-R\dot\theta^2\ne0$，不是 geodesic。

$G$ 与 $\Gamma$ 是 coordinate-dependent；Riemann curvature tensor 对 Euclidean plane 为零。$r=0$ 时 polar map 的 Jacobian rank 从 2 降到 1，故坐标失效；换 Cartesian chart metric 仍为 $I$。

## B02 解答：sphere

Constraint $c(x)=\tfrac12(x^\top x-1)$，$Dc(x)v=x^\top v$，故

$$
T_xS^{n-1}=\ker x^\top.
$$

对 ambient $a$：

$$
a_T=(I-xx^\top)a,
\qquad
a_N=(x^\top a)x.
$$

$f=-c^\top x$ 的 ambient gradient $-c$，故

$$
\operatorname{grad}f=-(I-xx^\top)c.
$$

令 $r=\|v\|$、$u=v/r$。Great-circle solution of $\ddot\gamma=-r^2\gamma$ with initial $(x,v)$ 是

$$
\operatorname{Exp}_x(v)=\cos r\,x+\sin r\,u.
$$

Normalization 满足 $R_x(0)=x$。令 $h(t)=R_x(tv)$，因 $x^\top v=0$：

$$
h(t)=\frac{x+tv}{\sqrt{1+t^2r^2}},
\qquad
h'(0)=v.
$$

所以是 retraction。展开：

$$
R_x(tv)
=x+tv-\frac12t^2r^2x-\frac12t^3r^2v+O(t^4),
$$

$$
\operatorname{Exp}_x(tv)
=x+tv-\frac12t^2r^2x-\frac16t^3r^2v+O(t^4).
$$

差为

$$
-\frac13t^3r^2v+O(t^4)=O(t^3).
$$

Euler point residual：

$$
\|x+tv\|^2-1=t^2r^2.
$$

Stationarity 要 $(I-xx^\top)c=0$，故 $x=\pm c/\|c\|$（$c\ne0$）。直接比较 $f=-c^\top x$：正向点值 $-\|c\|$ 为 global minimum，负向点值 $+\|c\|$ 为 global maximum。

## B03 解答：conformal metric

若 $G=e^{2\phi}I$，则

$$
G^{-1}=e^{-2\phi}I,
\qquad
\sqrt{\det G}=e^{d\phi},
$$

$$
\operatorname{grad}_gf=e^{-2\phi}\nabla f.
$$

Derivative

$$
\partial_i g_{j\ell}=2e^{2\phi}(\partial_i\phi)\delta_{j\ell}.
$$

乘 $g^{k\ell}=e^{-2\phi}\delta^{k\ell}$ 后：

$$
\Gamma^k_{ij}
=\delta^k_j\partial_i\phi
+\delta^k_i\partial_j\phi
-\delta_{ij}\partial^k\phi.
$$

所以

$$
\ddot x^k
+2(\nabla\phi\cdot\dot x)\dot x^k
-\|\dot x\|_2^2\partial^k\phi=0.
$$

$\phi$ 常数时只是所有长度乘 $e^\phi$，Christoffel 为零，geodesic images 是 straight lines。

$d=1$ 时 $ds^2=e^{2\phi(x)}dx^2$。令

$$
y(x)=\int_{x_0}^xe^{\phi(s)}ds,
$$

则 $dy=e^\phi dx$，所以 $ds^2=dy^2$。

$d\ge2$ 时逐点可取 $H=e^\phi I$，但要有 $dy^a=H^a_i dx^i$，每个 1-form 必须 closed/integrable。一般

$$
d(e^\phi dx^a)=e^\phi d\phi\wedge dx^a\ne0.
$$

故逐点 factorization 不自动积分成 coordinate map；curvature 提供更深的 obstruction。

## C01 解答：length 与 energy

令 $\tilde\gamma(s)=\gamma(\varphi(s))$，$\varphi:[c,d]\to[a,b]$ smooth、严格递增、onto。则

$$
\dot{\tilde\gamma}=\dot\gamma(\varphi(s))\varphi'(s),
$$

$$
L(\tilde\gamma)
=\int_c^d\|\dot\gamma(\varphi(s))\|\varphi'(s)ds
=\int_a^b\|\dot\gamma(t)\|dt.
$$

由 Cauchy–Schwarz：

$$
L^2
\le(b-a)\int_a^b\|\dot\gamma\|^2dt
=2(b-a)E.
$$

等号当且仅当 speed 与常数函数线性相关，即 speed a.e. constant。

例：unit circle 上

$$
\gamma_1(t)=(\cos\alpha t,\sin\alpha t),
$$

$$
\gamma_2(t)=(\cos\alpha t^2,\sin\alpha t^2),
\quad t\in[0,1].
$$

两者 $L=\alpha$，但 $E_1=\alpha^2/2$、$E_2=2\alpha^2/3$。因此 discretized energy optimizer可能同时优化 path image 和 node timing；要用 equal-time discretization、speed penalty 或 reparameterization 控制。

若 $\varphi$ 严格递减，speed 多出 $|\varphi'|$，length 仍不变；但 endpoints 交换，velocity orientation 反向。Energy 仍受非均匀速度影响。

## C02 解答：Levi–Civita 与 first variation

Metric compatibility 给三式：

$$
Xg(Y,Z)=g(\nabla_XY,Z)+g(Y,\nabla_XZ),
$$

及循环置换。取前两式相加减第三式，再用 torsion-free

$$
\nabla_XY-\nabla_YX=[X,Y]
$$

消去反向导数，得到

$$
\begin{aligned}
2g(\nabla_XY,Z)
={}&Xg(Y,Z)+Yg(Z,X)-Zg(X,Y)\\
&-g(X,[Y,Z])+g(Y,[Z,X])+g(Z,[X,Y]).
\end{aligned}
$$

右侧完全由 $g,X,Y,Z$ 确定；对所有 $Z$ 的 pairing 唯一决定 $\nabla_XY$，故至多一个 connection。存在性由反过来定义并验证公理得到。

Coordinate fields commute。令 $X=\partial_i,Y=\partial_j,Z=\partial_k$：

$$
2g_{k\ell}\Gamma^\ell_{ij}
=\partial_i g_{jk}+\partial_j g_{ik}-\partial_k g_{ij},
$$

再乘 inverse metric 得 standard Christoffel formula。

Geodesic speed：

$$
\frac d{dt}g(T,T)=2g(\nabla_TT,T)=0.
$$

对 variation $\Gamma(s,t)$，$T=\partial_t\Gamma$、$V=\partial_s\Gamma$。Torsion-free 且 coordinate variation fields commute 给

$$
\nabla_VT=\nabla_TV.
$$

于是

$$
\frac d{ds}E
=\int g(\nabla_VT,T)dt
=\int g(\nabla_TV,T)dt.
$$

Metric compatibility 与 integration by parts：

$$
\delta E
=\left[g(V,T)\right]_a^b
-\int g(V,\nabla_TT)dt.
$$

Fixed endpoints 令边界项为零；任意 compactly supported $V$ 下变分为零，fundamental lemma 给 $\nabla_TT=0$。

条件账：交换 $\nabla_VT$ 使用 torsion-free；导数内积使用 compatibility；去边界项使用 fixed endpoints；fundamental lemma 使用足够 smooth/可构造 variations。

## C03 解答：gradient projection 与下降率

对 $v\in T_xM$：

$$
df_x(v)=D\bar f(x)[v]
=\langle\nabla\bar f(x),v\rangle
=\langle P_x\nabla\bar f(x),v\rangle.
$$

$P_x\nabla\bar f\in T_xM$，由 gradient 唯一性：

$$
\operatorname{grad}f=P_x\nabla\bar f.
$$

Local minimizer $x_*$ 对任意 tangent $v$ 可取 curve $\gamma$ 实现该初速度；$(f\circ\gamma)'(0)=0$，故 $df(v)=0$，再由 positive definite metric 得 gradient 为零。

令 $g_k=\operatorname{grad}f(x_k)$、$\eta=-\alpha g_k$。Upper model 给

$$
f(x_{k+1})
\le f(x_k)-\alpha\|g_k\|^2
+\frac L2\alpha^2\|g_k\|^2.
$$

若 $\alpha\le1/L$：

$$
f(x_{k+1})\le f(x_k)-\frac\alpha2\|g_k\|^2.
$$

求和并用 $f(x_K)\ge f_{\inf}$：

$$
\frac\alpha2\sum_{k=0}^{K-1}\|g_k\|^2
\le f(x_0)-f_{\inf}.
$$

最小项不超过平均：

$$
\min_{k<K}\|g_k\|^2
\le\frac{2(f(x_0)-f_{\inf})}{\alpha K}.
$$

Gradient 小只表示近似 first-order stationary，非凸情形可能是 saddle/max。若 upper model 失败，大步可增大 objective；若无 lower bound，telescoping 无有限总预算，不能得该 bound。

## D01 解答：八条错误声明

1. **错。** Polar plane $G=\operatorname{diag}(1,r^2)$ varying 但 curvature zero。修正：用 curvature tensor/sectional curvature，不看 entries。
2. **错。** Great circle 超过 antipode。修正：geodesic 局部 minimizing；global 要检查 cut locus/completeness/path class。
3. **错。** Normal coordinates 任一点可令 $\Gamma(p)=0$。修正：curvature 涉及 first derivatives/quadratic combinations，且 tensorially invariant。
4. **错。** Sampled full rank 只给有限点 immersion evidence。还缺 uniform rank、injectivity、properness/global topology；诊断 singular-value grid/adversarial search/self-intersection。
5. **错。** PSD 允许 zero eigenvalue。Riemannian 要 PD；诊断 $\lambda_{\min}$、rank 和 condition over domain。
6. **错。** Tangent is first-order feasible；sphere residual $\|x+tv\|^2-1=t^2\|v\|^2$。用 retraction并报告 residual。
7. **错。** Fisher 可因 symmetry singular；approximations/damping改变 invariance。诊断 spectrum、rank、reparameterized function update。
8. **错。** Sphere normalization 与 Exp 三阶开始不同；finite-step objective/trajectory可不同。比较 local error order、cost和 convergence assumptions。

## D02 解答：completeness 反例组

1. $\mathbb R^d$ Euclidean complete、geodesically complete、closed bounded sets compact，但 whole space 非 bounded，故非 compact。
2. Open unit ball 非 complete。Cauchy sequence $(1-1/n)e_1$ 趋向缺失 boundary；radial geodesic 在有限 affine time 达 boundary，不能在 manifold 内延拓。任意两个 interior points 的 straight segment仍实现 distance，这也说明“非完备”不等于“每对点都无 minimizer”。若要 infimum 不取到，可取 punctured plane 中连接 $(-1,0)$ 与 $(1,0)$：Euclidean length infimum为 2，但 straight segment穿过缺失原点，任何可行 curve length严格大于2，故不实现。
3. Sphere 从北极到南极有无穷多 minimizing semicircles；同一 great circle 绕额外一圈仍是 geodesic，但 length 大于 $\pi$，非 minimizing。

一般 metric space 中 closed+bouned不推出 compact，例如 infinite-dimensional Hilbert space 的 closed unit ball。Hopf–Rinow 在 connected finite-dimensional complete Riemannian manifold 中加入局部有限维几何与 geodesic completeness，才恢复 properness。

## D03 解答：VAE geodesic 声明审计

### 1. Decoder/rank 账

检查 $J_g$ 是否在整条 path 和 neighborhood full rank；报告 $\lambda_{\min}(J_g^\top J_g)$ 与 condition。Sampled success 不能证明 global immersion/embedding。

### 2. Output geometry 账

VAE decoder 是 distribution。若只用 mean Jacobian，忽略 variance change，必须把结论降为 “mean-decoder induced geometry”。若用 stochastic metric，需明确 expected displacement/KL/Fisher 定义。

### 3. Solver 账

报告 discretization、multiple starts、endpoint residual、gradient/ODE residual、speed variance、mesh refinement 和 compute。Energy 低于直线只说明优于一个 baseline，不证明 global minimum。

### 4. Local/global 账

存在多个 homotopy/path minima、cut-like regions和 solver local minima。需要 lower bound/certificate 或充分问题结构才可说 global minimizing。

### 5. Geometry identifiability 账

Reconstruction/training objective 通常不唯一识别 latent chart/metric；不同 decoders 可拟合同一 finite data。需要 controlled synthetic truth、held-out local distances或 external geometry measurements。

### 6. Semantic 账

需预定义 downstream/human evaluation、blind comparison、effect size与 uncertainty。Smooth-looking images 是探索证据。

最小复现：analytic immersion + known sphere/paraboloid metric；rank-collapse negative control；straight/graph/multiple-start baselines；mesh refinement；metric spectrum；fixed seeds and artifact hash。允许结论可降为：“在审计区域和给定 discretization 下，solver 找到一条相对 straight baseline 具有更低 chosen energy 的 path。”

## E01 解答：decoder geodesic benchmark

一个可执行设计：

1. 取 $g(u,v)=(u,v,a(u^2+v^2))$，analytic $G=J_g^\top J_g$；再取 $\tilde g(u,v)=(u^2,v,a(u^2+v^2))$ 产生 $u=0$ rank collapse。
2. Regular region要求 $\lambda_{\min}(G)\ge\tau$；collapse track 单独预期失败，不用 damping 偷换问题。
3. 端点按 Euclidean separation、curvature exposure 和是否穿越 $u=0$ 分层；每对用 straight、graph、随机 Bézier/multiple starts。
4. 指标：Riemannian length/energy、speed coefficient of variation、endpoint residual、discrete Euler–Lagrange residual、iterations/evaluations/time。
5. 扫 $\lambda_{\min},\kappa(G)$，把 solver error 对 condition 作图。
6. $N=16,32,64,128$ refinement；比较 path length和node interpolation convergence。
7. 固定 seed、排序、SVG float formatting；脚本 assertions 检查 analytic metric symmetry/rank、regular track convergence、collapse detection。
8. 结论只支持 synthetic geometry/implementation；semantic superiority 要真实 task evidence。

## E02 解答：Stiefel algorithm comparison

取 $Y\in\operatorname{St}(n,r)$，若 objective 只依赖 span则主对象应为 Grassmann。Frobenius metric 下

$$
P_Y(A)=A-Y\operatorname{sym}(Y^\top A).
$$

四方法：

- Euclidean projected GD：ambient step 后用 chosen nearest/polar projection；
- QR-RGD：tangent step后 `qf`，固定 $R$ diagonal positive；
- polar-RGD：$(Y+Z)[(Y+Z)^\top(Y+Z)]^{-1/2}$；
- penalty：ambient minimize $f(Y)+\mu\|Y^\top Y-I\|_F^2$。

记录 $f$、$\|\operatorname{grad}f\|$、$\|Y^\top Y-I\|_F$、step length、factorization cost/time。Gauge-invariant error用 projector distance

$$
\|YY^\top-Y_*Y_*^\top\|_F
$$

或 principal angles，不逐列比较。扫 objective condition、$n/r$、batch noise与学习率；同等 wall-clock和同等 constraint tolerance都要比较。一次 task胜负只说明该实现/预算/metric下的经验结果。

## E03 解答：natural-gradient audit

选小型 softmax/logistic model，使 output states 可枚举并 exact expectation：

$$
F(\theta)=\sum_y p_\theta(y)s_\theta(y)s_\theta(y)^\top.
$$

构造 redundant parameterization，例如 logits 同加常数不改 distribution，Fisher 沿该方向 singular。比较：

- exact Fisher；
- empirical Fisher（用 observed labels 的 score outer products）；
- GGN；
- $F+\lambda I$；
- block diagonal approximation。

做 invertible reparameterization $\theta=\psi(\eta)$。理想 infinitesimal natural direction应在 function/distribution tangent 中相容；但 finite step $\theta-\alpha F^{-1}\nabla L$ 不等于在新坐标做加法后精确映回，因为 Euler discretization非 invariant。比较 distribution change/KL，而非 raw parameter vector。

报告 eigen spectrum、numerical rank、$\lambda$、linear-solve residual、direction angle、predicted decrease、actual loss、KL step、memory/time。Symmetry track 应触发 singular assertion；damping track必须显示 metric改变。结论边界：Fisher natural gradient是 parameter-manifold geometry；它不施加 sphere/Stiefel feasibility，也不自动等于 mirror descent 或任意 preconditioner。

## 评分量表

| 维度 | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| 对象类型 | 混淆 point/tangent/cotangent | 能识别但漏 domain | 大体准确 | 全部写明 base point/domain/codomain |
| 条件 | 无条件套公式 | 偶尔补条件 | 主要条件齐 | 能指出删除条件后的反例 |
| 推导 | 只报结果 | 有关键公式 | 证明链完整 | 还能解释每步用到哪项假设 |
| local/global | 全部混用 | 能口头区分 | 正确用于例题 | 能用 cut/completeness/solver 证据审计 |
| 数值证据 | 单次图形 | 有 residual | 有 refinement/assertion | 还有 condition、negative control 与 hash |
| AI 声明 | 直接外推 | 有免责声明 | 分 theorem/estimate/observation | 给可执行 claim ladder 与 falsification |

满分 18。达到 14 只表示本轮书面材料较好；仍需闭卷、改参复现与间隔重做才能升级掌握状态。
