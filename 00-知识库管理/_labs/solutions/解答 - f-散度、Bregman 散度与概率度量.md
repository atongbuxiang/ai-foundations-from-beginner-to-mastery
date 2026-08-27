---
type: solution
status: draft
area: [math/information-theory, math/statistics, math/geometry, ai/generative-models]
topic: "f-散度、Bregman 散度与概率度量"
exercise: "[[习题 - f-散度、Bregman 散度与概率度量]]"
prerequisites: ["[[f-散度、Bregman 散度与概率度量]]"]
related: ["[[信息论与统计学习接口 MOC]]", "[[练习与测验 MOC]]"]
sources: ["Csiszar-1967-f-Divergence", "Nowozin-Cseke-Tomioka-2016-fGAN", "Bregman-1967-Relaxation-Method", "Sriperumbudur-et-al-2010-Kernel-Metrics", "Gretton-et-al-2012-MMD", "Arjovsky-Chintala-Bottou-2017-WGAN", "Su-6016-fGAN", "Su-6280-Wasserstein-WGAN", "Su-8244-WGAN-Distance"]
created: 2026-08-19
updated: 2026-08-19
---

# 解答 - f-散度、Bregman 散度与概率度量

> [!warning] 使用边界
> “距离更小”只有在对象、函数类/ground cost、population/empirical 层和 estimator 全部固定后才可比较。训练 surrogate 与理论 probability metric 同名，不表示它们数值相等。

## A. 识别与复述

### INFO-DIST-A01

divergence 通常要求 nonnegative 和 identity of indiscernibles；pseudometric 还要求 symmetry/triangle 但允许不同对象距离零；metric 再要求零点只在相同对象。

- KL：divergence；不 symmetric，无 triangle；
- JS：symmetric divergence，JS 本身一般不满足 triangle；
- $\sqrt{\operatorname{JS}}$：在标准 equal-weight definition 下是 metric；
- TV：probability measures 上的 metric；
- squared Euclidean：symmetric divergence，但平方破坏 triangle；Euclidean norm 才是 metric；
- $W_p$：finite $p$th-moment probability space 上、ground $d$ 为 metric 时是 metric；
- MMD：kernel mean embedding distance；kernel characteristic 时对 distributions 是 metric，否则通常 pseudometric。

### INFO-DIST-A02

$$
D_f(P\|Q)=E_Qf(dP/dQ)
$$

依赖 likelihood/density ratio，通常不使用 $x,y$ 在 sample space 中相距多远。

$$
B_F(u,v)=F(u)-F(v)-\nabla F(v)^\top(u-v)
$$

依赖 vector coordinates 与 convex potential，表示 tangent approximation gap。

$$
\gamma_\mathcal F(P,Q)=\sup_{g\in\mathcal F}|E_Pg-E_Qg|
$$

依赖 test-function class，表示在这组 observables 下的最大 expectation discrepancy。

TV 同时是 $f$-divergence 与 bounded-function IPM；KL 是 $f$-divergence，也是在 simplex negative entropy/指数族 log-partition 上的 Bregman divergence。

### INFO-DIST-A03

在 $D_f(P\|Q)=E_Qf(p/q)$ convention 下：

| 对象 | $f(t)$ |
|---|---|
| forward KL | $t\log t$ |
| reverse KL | $-\log t$ |
| Pearson $\chi^2$ | $(t-1)^2$ |
| squared Hellinger | $(\sqrt t-1)^2$ |
| TV | $\tfrac12|t-1|$ |
| JS | $\tfrac12[t\log\frac{2t}{1+t}+\log\frac2{1+t}]$ |

令 $\tilde f(t)=f(t)+a(t-1)$：

$$
E_Q\tilde f(p/q)
=D_f+a\left[\int p-\int q\right]
=D_f.
$$

所以 generator 有 affine gauge。

## B. 手算与构造

### INFO-DIST-B01

forward KL：

$$
D(P\|Q)
=0.75\log1.5+0.25\log0.5
\approx0.130812.
$$

reverse：

$$
D(Q\|P)
=0.5\log\frac{0.5}{0.75}
+0.5\log\frac{0.5}{0.25}
\approx0.143841.
$$

数值不同。

$$
\operatorname{TV}=\frac12(|0.75-0.5|+|0.25-0.5|)=0.25.
$$

squared Hellinger（无 $1/2$ convention）：

$$
(\sqrt{0.75}-\sqrt{0.5})^2
+(\sqrt{0.25}-\sqrt{0.5})^2
\approx0.068148.
$$

$M=(0.625,0.375)$：

$$
\operatorname{JS}
=\tfrac12D(P\|M)+\tfrac12D(Q\|M)
\approx0.033822.
$$

Pinsker 右侧：

$$
\sqrt{D(P\|Q)/2}\approx0.255746,
$$

确有 $0.25\le0.255746$。

### INFO-DIST-B02

对

$$
F(u)=\sum_i u_i\log u_i,
\quad \nabla F(q)_i=1+\log q_i,
$$

且 $\sum(p_i-q_i)=0$：

$$
\begin{aligned}
B_F(P,Q)
&=\sum_ip_i\log p_i-\sum_iq_i\log q_i
-\sum_i(1+\log q_i)(p_i-q_i)\\
&=\sum_ip_i\log(p_i/q_i)\\
&=0.130812.
\end{aligned}
$$

若 $G(u)=\tfrac12\|u\|^2$：

$$
B_G(P,Q)=\frac12\|P-Q\|^2
=\frac12(0.25^2+(-0.25)^2)=0.0625.
$$

quadratic potential 的 Hessian constant，Bregman gap 变 squared Euclidean 并 symmetric；negative entropy curvature 随 coordinates/probabilities 变化，产生 ratio 与方向性。

### INFO-DIST-B03

$\theta\ne0$ 时 point masses mutually singular：

$$
D(P\|Q)=D(Q\|P)=+\infty,
$$

$$
\operatorname{JS}(P,Q)=\log2,
\qquad \operatorname{TV}(P,Q)=1.
$$

唯一 coupling 把 $0$ 搬到 $\theta$：

$$
W_1(P,Q)=|\theta|.
$$

MMD 展开：

$$
\operatorname{MMD}^2
=k(0,0)+k(\theta,\theta)-2k(0,\theta)
=2-2e^{-\theta^2/(2\sigma^2)}.
$$

当 $\theta\to0$，$W_1$ 与 RBF-MMD 趋零；JS/TV 对所有非零 $\theta$ 保持最大，KL 保持 infinite，到 $\theta=0$ 才跳为零。

## C. 推导与证明

### INFO-DIST-C01

令 $r=dP/dQ$。因 $E_Qr=1$：

$$
D_f(P\|Q)=E_Qf(r)\ge f(E_Qr)=f(1)=0.
$$

若 $f$ 严格凸，equality 要求 $r$ constant $Q$-a.s.；其 expectation 为 1，故 $r=1$、$P=Q$。

令 channel $K$ 作用于 $X$。在 reference joint $Q(dx)K(dy\mid x)$ 下，output ratio 为

$$
r_Y(Y)=E_Q[r_X(X)\mid Y].
$$

因此

$$
\begin{aligned}
D_f(P_Y\|Q_Y)
&=E_{Q_Y}f(E_Q[r_X\mid Y])\\
&\le E_QE[f(r_X)\mid Y]\\
&=D_f(P_X\|Q_X).
\end{aligned}
$$

这是 conditional Jensen 版 DPI。

### INFO-DIST-C02

Fenchel inequality：

$$
f(t)+f^*(u)\ge ut.
$$

令 $t=p/q,u=T(x)$，乘 $q$ 并积分：

$$
D_f(P\|Q)
\ge E_PT-E_Qf^*(T).
$$

若 function class 足够大、$T^*(x)\in\partial f(p/q)$ measurable/integrable，取 supremum可达到 equality。受限 neural class 通常只能给 lower bound。

对 $f(t)=t\log t$：

$$
f^*(u)=\sup_{t>0}[ut-t\log t].
$$

stationarity $u-(\log t+1)=0$，故 $t=e^{u-1}$，

$$
f^*(u)=e^{u-1}.
$$

所以

$$
D(P\|Q)
=\sup_T\{E_PT-E_Qe^{T-1}\}.
$$

这与 Donsker–Varadhan 的 $E_PT-\log E_Qe^T$ 是相关但不同的 variational representation，不能混写 objective。

### INFO-DIST-C03

指数族 log ratio：

$$
\log\frac{p_\eta}{p_{\eta'}}
=(\eta-\eta')^\top T-A(\eta)+A(\eta').
$$

在 $p_\eta$ 下取期望并用 $E_\eta T=\nabla A(\eta)$：

$$
D(p_\eta\|p_{\eta'})
=A(\eta')-A(\eta)-\nabla A(\eta)^\top(\eta'-\eta)
=B_A(\eta',\eta).
$$

RKHS 中 reproducing property 给

$$
E_Pg(X)=\langle g,E_Pk(X,\cdot)\rangle_\mathcal H
=\langle g,\mu_P\rangle.
$$

于是

$$
\sup_{\|g\|\le1}\langle g,\mu_P-\mu_Q\rangle
=\|\mu_P-\mu_Q\|_\mathcal H.
$$

平方并展开 inner products：

$$
\operatorname{MMD}^2
=E k(X,X')+E k(Y,Y')-2E k(X,Y).
$$

## D. 边界、反例与纠错

### INFO-DIST-D01

定义 Jeffreys/symmetrized KL：

$$
J(p,q)=D(\operatorname{Ber}(p)\|\operatorname{Ber}(q))
+D(\operatorname{Ber}(q)\|\operatorname{Ber}(p)).
$$

取 $p=0.1,q=0.2,r=0.9$（nats）：

$$
J(p,r)\approx3.515559,
$$

$$
J(p,q)\approx0.081093,
\qquad J(q,r)\approx2.508463.
$$

因此

$$
J(p,r)>J(p,q)+J(q,r)\approx2.589556,
$$

违反 triangle inequality。对称只补了 metric 公理之一。

### INFO-DIST-D02

若 population law nonatomic continuous，两个 independent finite samples 几乎必然没有完全相同的点。令

$$
A=\{X_1,\ldots,X_n\}.
$$

first empirical measure $\widehat P_n(A)=1$；second sample 无点落在有限 zero-population set $A$，几乎必然 $\widehat Q_m(A)=0$。所以

$$
\operatorname{TV}(\widehat P_n,\widehat Q_m)=1.
$$

即使两组都来自同一个 population。empirical plug-in TV 在此不一致地反映了离散 supports，而非 population difference；需要 smoothing、restricted function class 或专门 estimator/assumptions。

### INFO-DIST-D03

linear kernel feature map 是 $\phi(x)=x$，mean embedding 只是 $E[X]$。取

$$
P=\delta_0,
\qquad Q=\tfrac12\delta_{-1}+\tfrac12\delta_1.
$$

两者 mean 都为 0，故

$$
\operatorname{MMD}_{\rm linear}(P,Q)=0,
$$

但 distributions 明显不同。linear kernel 非 characteristic。RBF kernel 在 $\mathbb R$ 上 characteristic，理论 population MMD 为零 iff distributions 相同；finite estimator 仍有 sampling error，bandwidth 仍影响 power。

## E. AI 迁移

### INFO-DIST-E01

五层应分开：

1. population JS：$\operatorname{JS}(P_{data},P_G)$；
2. theoretical variational supremum over all admissible critics；
3. restricted neural critic population optimum；
4. finite train empirical objective及其 generalization；
5. alternating optimizer达到的 discriminator/generator surrogate。

train objective 下降可能来自 discriminator undertraining、overfit、generator loss reparameterization 或 game cycling，不必等量对应 population JS。应使用 held-out critic/evaluation samples、capacity/optimization diagnostics、multiple seeds，并把 generator surrogate 按公式命名。

### INFO-DIST-E02

**图像小平移。** 若 pixel/feature ground metric确实表达 perceptual小位移，可考虑 Wasserstein/OT 或 geometry-aware feature IPM；raw Euclidean ground cost 未必符合语义，高维 empirical OT 成本高。

**语言模型 likelihood。** normalized conditional probability已有，held-out token/byte NLL/cross-entropy最直接，对应 forward KL；Wasserstein 不替代 proper log score，tokenizer/reduction要统一。

**高维 embeddings two-sample test。** characteristic-kernel MMD、energy distance 或 classifier two-sample test；kernel/bandwidth和 null calibration 必须预先/validation选择，报告 sample size、dimension与 test power。若只关心 mean shift，linear MMD 可能足够但不能声称检验所有分布差异。

选择不是按“高级程度”，而是按 downstream function class、geometry、估计预算与单位。

### INFO-DIST-E03

- weight clipping：粗略限制参数，不等价于固定全局 Lipschitz constant，可能降低 critic capacity；
- spectral normalization：控制各线性层 operator norm，结合 activation 可给 global upper bound，但可能松、受 convolution implementation影响；
- gradient penalty：只在 sampled/interpolated points约束 gradient norm，不能保证全空间 1-Lipschitz；
- exact ball：理论 supremum over all 1-Lipschitz functions，neural class达不到。

报告至少含：ground metric/feature scaling、critic architecture、每层 norm、penalty sampling、inner steps/convergence、train/held-out critic values、generalization gap、batch-size sensitivity与 seeds。另用 empirical OT（注明 regularization/debiasing）和 characteristic MMD作不同结构 baseline；不得把三者数值直接横比为同一单位。

## 完成标准

面对任意“distance loss”，你应先判断它属于 density ratio、convex coordinate、test-function 还是 transport geometry，再写 population definition、estimator 和 training surrogate 三层；只有这些对象都对齐，数值结论才可解释。
