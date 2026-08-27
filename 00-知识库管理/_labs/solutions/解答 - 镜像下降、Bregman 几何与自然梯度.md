---
type: solution
status: draft
area: [math/optimization, math/information-geometry, ai/training]
topic: "镜像下降、Bregman 几何与自然梯度"
exercise: "[[习题 - 镜像下降、Bregman 几何与自然梯度]]"
related: ["[[镜像下降、Bregman 几何与自然梯度]]", "[[优化与凸分析 MOC]]"]
created: 2026-08-19
updated: 2026-08-19
---

# 解答 - 镜像下降、Bregman 几何与自然梯度

> [!warning] 使用顺序
> 先声明 movement geometry、坐标和采样分布，再写 inverse/preconditioner。凡是 finite step、damping、近似 Fisher 或 stochastic estimate，都要重新审计理想化 invariance。

## A. 识别与复述

### OPT-MIRROR-A01

对 differentiable strictly convex $\psi$：

$$
D_\psi(x,y)
=\psi(x)-\psi(y)-\langle\nabla\psi(y),x-y\rangle.
$$

mirror map 是 $x\mapsto\nabla\psi(x)$，dual coordinate $\theta=\nabla\psi(x)$。更新：

$$
x_{t+1}
=\arg\min_{x\in\mathcal X}
\left\{\eta_t\langle g_t,x\rangle+D_\psi(x,x_t)\right\}.
$$

interior/unconstrained 时

$$
\nabla\psi(x_{t+1})
=\nabla\psi(x_t)-\eta_tg_t.
$$

$D_\psi\ge0$ 且 strict convex 时仅在 $x=y$ 为零，但一般不 symmetric、无 triangle inequality，所以是 divergence 而非 metric。其 local Hessian 才定义 infinitesimal quadratic geometry。把 dual coordinate 映回 primal 还需把 $(\nabla\psi)^{-1}$ 限制在 gradient image，或采用 Legendre-type assumptions；strict convexity 本身不保证 onto 整个 dual space。

### OPT-MIRROR-A02

exact Fisher：

$$
F(\theta)
=\mathbb E_{x\sim q}
\mathbb E_{y\sim p_\theta(\cdot|x)}
[s_\theta s_\theta^T],
\qquad
s_\theta=\nabla_\theta\log p_\theta(y|x).
$$

empirical Fisher：

$$
\widehat F_{\rm emp}
=\frac1n\sum_i
s_\theta(x_i,y_i)s_\theta(x_i,y_i)^T,
$$

其中 $y_i$ 来自 dataset，不是当前 model。GGN：

$$
G_{\rm GN}
=\mathbb E[J_\theta^TH_\ell J_\theta].
$$

对 negative log-likelihood 与相匹配的 exponential-family output，exact Fisher 与 GGN可相等。empirical Fisher 接近 exact Fisher 还需 data distribution接近 model、sampling/large-sample 等条件；一般不相等。

### OPT-MIRROR-A03

- Euclidean gradient：$\ell_2$ local movement；
- preconditioned gradient：固定/给定 quadratic metric $H$，方向 $-H^{-1}g$；
- mirror descent：global Bregman divergence $D_\psi$ 与 constraints；
- natural gradient：model-distribution local KL，即 exact Fisher metric；
- AdaGrad：由 cumulative coordinate/full-matrix gradient statistics产生 time-varying regularizer；
- Muon：矩阵参数上与 spectral-norm steepest direction/polarized gradient 相关。

后四者都“改变 geometry”，但定义对象不同；只有证明 metric/potential/update相合，才能宣称等价。

## B. 手算与构造

### OPT-MIRROR-B01

quadratic potential：

$$
D_\psi(x,x_t)
=\frac12(x-x_t)^TH(x-x_t).
$$

无约束 stationarity：

$$
\eta g_t+H(x_{t+1}-x_t)=0,
$$

所以

$$
x_{t+1}=x_t-\eta H^{-1}g_t.
$$

有 convex constraint $\mathcal X$：

$$
x_{t+1}
=\arg\min_{x\in\mathcal X}
\frac12\|x-(x_t-\eta H^{-1}g_t)\|_H^2,
$$

是 $H$-metric projection，不是一般 Euclidean projection。

数值上

$$
H^{-1}g_t=
\begin{bmatrix}1&0\\0&1/4\end{bmatrix}
\begin{bmatrix}2\\-4\end{bmatrix}
=\begin{bmatrix}2\\-1\end{bmatrix},
$$

故

$$
x_{t+1}
=\begin{bmatrix}1\\1\end{bmatrix}
-\frac12\begin{bmatrix}2\\-1\end{bmatrix}
=\begin{bmatrix}0\\3/2\end{bmatrix}.
$$

### OPT-MIRROR-B02

raw multiplicative weights：

$$
\tilde x_i=x_{t,i}e^{-\eta g_{t,i}}.
$$

因 $\eta=\log2$：

$$
e^{-\eta g}=(1/2,1,2).
$$

所以

$$
\tilde x=(1/4,1/3,1/3),
\qquad
Z=\frac14+\frac13+\frac13=\frac{11}{12}.
$$

归一化：

$$
x_{t+1}
=\left(\frac3{11},\frac4{11},\frac4{11}\right).
$$

三项严格正且和为 $1$。第三项虽初始最小，但 gradient 为负，multiplicative factor $2$ 使其上升。

### OPT-MIRROR-B03

Bernoulli logit score：

$$
\partial_\theta\log p_\theta(y)
=y-p.
$$

因此

$$
F_\theta=\mathbb E[(y-p)^2]=p(1-p).
$$

当 $p=1/4$：

$$
F_\theta=\frac3{16},
\qquad
\delta\theta_{\rm NG}
=-\frac{3/8}{3/16}=-2.
$$

换用 probability coordinate $p$。Bernoulli Fisher：

$$
F_p=\frac1{p(1-p)}=\frac{16}{3}.
$$

gradient chain rule：

$$
\frac{\partial\mathcal L}{\partial p}
=\frac{\partial\mathcal L/\partial\theta}
{\partial p/\partial\theta}
=\frac{3/8}{3/16}=2.
$$

故

$$
\delta p_{\rm NG}
=-F_p^{-1}\cdot2
=-\frac38.
$$

由 logit direction induced tangent：

$$
\delta p
=\frac{\partial p}{\partial\theta}\delta\theta
=\frac3{16}(-2)=-\frac38.
$$

二者一致；这是 infinitesimal tangent statement，finite step $\theta\mapsto\theta-2$ 后的实际 $\Delta p$ 不等于线性化 $-3/8$。

## C. 推导与证明

### OPT-MIRROR-C01

展开：

$$
\begin{aligned}
&D_\psi(x,z)-D_\psi(x,y)-D_\psi(y,z)\\
&=\langle\nabla\psi(y)-\nabla\psi(z),x-y\rangle.
\end{aligned}
$$

mirror subproblem first-order optimality：任意 $x\in\mathcal X$，

$$
\left\langle
\eta g_t+\nabla\psi(x_{t+1})-\nabla\psi(x_t),
x-x_{t+1}
\right\rangle\ge0.
$$

移项并把 three-point identity 用在

$$
\langle\nabla\psi(x_{t+1})-\nabla\psi(x_t),
x-x_{t+1}\rangle
$$

得到

$$
\eta\langle g_t,x_{t+1}-x\rangle
\le
D_\psi(x,x_t)
-D_\psi(x,x_{t+1})
-D_\psi(x_{t+1},x_t).
$$

最后一项非负，是 mirror step 的 movement penalty。

### OPT-MIRROR-C02

将

$$
\langle g_t,x_t-x\rangle
=\langle g_t,x_t-x_{t+1}\rangle
+\langle g_t,x_{t+1}-x\rangle
$$

与 C01 合并。strong convexity 给

$$
D_\psi(x_{t+1},x_t)
\ge\frac\sigma2\|x_{t+1}-x_t\|^2.
$$

Hölder–Young：

$$
\langle g_t,x_t-x_{t+1}\rangle
-\frac{\sigma}{2\eta}\|x_{t+1}-x_t\|^2
\le\frac{\eta}{2\sigma}\|g_t\|_*^2.
$$

故

$$
\langle g_t,x_t-x\rangle
\le
\frac{D_\psi(x,x_t)-D_\psi(x,x_{t+1})}{\eta}
+\frac{\eta}{2\sigma}\|g_t\|_*^2.
$$

求和 telescope：

$$
\sum_{t=1}^T\langle g_t,x_t-x\rangle
\le\frac{R^2}{\eta}
+\frac{\eta G^2T}{2\sigma}.
$$

对 $\eta$ 求最小：

$$
\eta^*=\frac{R\sqrt{2\sigma}}{G\sqrt T}.
$$

代回：

$$
\operatorname{Regret}_T
\le
\sqrt2\,RG\sqrt{\frac T\sigma}.
$$

若 loss convex，function regret 不超过 linearized regret。unknown horizon 时可取 $\eta_t\propto1/\sqrt t$ 或 doubling trick。

### OPT-MIRROR-C03

local trust-region：

$$
\min_\delta g^T\delta
\quad\text{s.t. }\frac12\delta^TF\delta\le\varepsilon.
$$

Lagrangian stationarity $g+\lambda F\delta=0$，故

$$
\delta=-\lambda^{-1}F^{-1}g.
$$

boundary决定

$$
\lambda
=\sqrt{\frac{g^TF^{-1}g}{2\varepsilon}},
$$

所以 normalized direction 为

$$
\delta
=-\sqrt{\frac{2\varepsilon}{g^TF^{-1}g}}F^{-1}g.
$$

令 $\theta=\phi(\alpha)$，$J=\partial\theta/\partial\alpha$ invertible：

$$
g_\alpha=J^Tg_\theta,
\qquad F_\alpha=J^TF_\theta J.
$$

于是

$$
\begin{aligned}
J F_\alpha^{-1}g_\alpha
&=J(J^TF_\theta J)^{-1}J^Tg_\theta\\
&=F_\theta^{-1}g_\theta.
\end{aligned}
$$

因此两坐标中的 natural tangent vector 表示同一 distributional direction。证明用了 exact tensor transformation、invertibility 与 infinitesimal linearization。

## D. 反例与失败边界

### OPT-MIRROR-D01

即使 Euclidean potential

$$
\psi(x)=\frac12x^2
$$

产生的 Bregman divergence

$$
D_\psi(x,y)=\frac12(x-y)^2
$$

是 symmetric，它也不满足 triangle inequality。取 $x=0,y=1,z=2$：

$$
D(0,2)=2,
$$

但

$$
D(0,1)+D(1,2)=\frac12+\frac12=1.
$$

所以 squared Euclidean distance 不是 metric。negative entropy还一般有

$$
D_{\rm KL}(p\|q)\ne D_{\rm KL}(q\|p),
$$

进一步失败 symmetry。

### OPT-MIRROR-D02

令 Bernoulli probability只依赖 $s=a+b$。设 $q=p(1-p)$，则

$$
F_{a,b}
=q
\begin{bmatrix}1&1\\1&1\end{bmatrix},
$$

rank 为 $1$；direction $(1,-1)$ 不改变 distribution。若 gradient $g=c(1,1)^T$，inverse 不存在。pseudoinverse：

$$
F^\dagger
=\frac1{4q}
\begin{bmatrix}1&1\\1&1\end{bmatrix},
$$

给 minimum-Euclidean-norm solution

$$
\delta^\dagger
=-\frac{c}{2q}(1,1)^T.
$$

所有满足 $\delta_a+\delta_b=-c/q$ 的解产生同一 first-order distribution tangent。

damping 后：

$$
\delta_\lambda
=-(F+\lambda I)^{-1}g
=-\frac c{2q+\lambda}(1,1)^T.
$$

它 shrink identifiable direction，也给 null-space Euclidean尺度。若把 $a,b$ 重新缩放，identity matrix 不按 $J^TIJ$ tensor law变换，故 direction不再 exact invariant。

### OPT-MIRROR-D03

取 Bernoulli model $p_\theta(y=1)=0.1$，数据却全部 $y_i=1$。logit score $y-p$。

exact Fisher：

$$
F= p(1-p)=0.09.
$$

empirical Fisher：

$$
\widehat F_{\rm emp}
=\frac1n\sum_i(1-0.1)^2=0.81.
$$

相差 $9$ 倍。empirical matrix仍是 PSD、可反映 observed-gradient scale，作为 preconditioner可能稳定训练；但它不是 current model KL 的 Hessian，不能继承 exact natural-gradient trust-region与 invariance解释。报告时必须叫清名字。

## E. AI 迁移

### OPT-MIRROR-E01

对每个 token/input 的 gating distribution $w\in\Delta_K$：

$$
\tilde w_{k}
=w_{k}\exp[-\eta(\widehat g_k+\rho_k)],
\qquad
w_k^+=\frac{\tilde w_k}{\sum_j\tilde w_j},
$$

其中 $\rho$ 可来自 load-balancing constraint 的 multiplier/gradient。协议：

1. 从 $w_k>0$ 初始化或加入 $\epsilon/K$ mixing，避免 zero support 永久死亡；
2. 在 log weights 上减 max 后做 log-sum-exp；
3. 区分 per-token simplex 与 batch/global capacity constraint，后者可能需 dual variable；
4. 报告 stochastic gradient variance、expert load histogram、entropy与 dropped tokens；
5. held-out distribution上审计 load、quality与 tail experts；
6. 若 top-$k$ hard routing，soft mirror update后还有 discrete projection/selection，理论需另行处理。

### OPT-MIRROR-E02

实现合同：

1. 明确 objective 是 minimize loss 还是 maximize return；
2. state expectation用 old-policy visitation、replay distribution或 on-policy sample；
3. KL 写 $D_{\rm KL}(\pi_{\rm old}\|\pi_\theta)$ 还是反向；
4. exact/model Fisher expectation怎样近似；
5. 用 autodiff Fisher-vector product，做数值 symmetry/PSD sanity check；
6. CG iteration、residual与 preconditioner；
7. damping $\lambda$ 与原因；
8. 由 target radius scale direction；
9. backtracking line search同时检查 surrogate improvement和 measured KL；
10. 报告 predicted quadratic KL vs actual KL；
11. advantage estimator bias/variance、GAE parameters与 normalization；
12. policy stochasticity、seed与 episode confidence interval。

small CG residual不消除 advantage statistical error；measured KL合格也不证明 return 单调，除非相应 assumptions/estimation bounds成立。

### OPT-MIRROR-E03

要证明 natural gradient，必须给：

$$
p_\theta,\quad
D_{\rm KL}(p_\theta\|p_{\theta+\delta}),
\quad F(\theta),\quad
\delta\propto-F^{-1}g.
$$

要证明 mirror descent，必须给 convex potential $\psi$、domain、orientation $D_\psi(\theta,\theta_t)$，并证明实际 update 解相应 argmin。

要证明 spectral steepest descent，必须给 matrix movement norm：

$$
\min_{\|\Delta W\|_2\le\epsilon}
\langle G,\Delta W\rangle
$$

并证明 polar/orthogonalized update解该 linear oracle。Muon最直接属于第三种解释；除非额外构造前两者，不能改名。

可证伪实验：

1. 对 function-equivalent layer rescaling/reparameterization，比较 induced function/KL step；exact natural direction应 first-order接近 invariant；
2. 测 actual KL quadratic prediction，判断是否 Fisher trust region；
3. 测 update 是否满足 spectral-norm constrained linear optimum；
4. 尝试 reconstruct fixed potential，检查 cyclic monotonicity/integrability；
5. 分离 Newton–Schulz次数、momentum/scaling，看 geometry claim 是否随 implementation改变。
