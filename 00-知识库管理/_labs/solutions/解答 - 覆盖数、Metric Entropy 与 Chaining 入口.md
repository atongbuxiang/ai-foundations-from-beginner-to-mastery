---
type: solution
status: draft
area: [learning-theory/metric-entropy, empirical-process/chaining]
topic: "[[覆盖数、Metric Entropy 与 Chaining 入口]]"
exercise: "[[习题 - 覆盖数、Metric Entropy 与 Chaining 入口]]"
prerequisites: ["[[覆盖数、Metric Entropy 与 Chaining 入口]]"]
related: ["[[局部 Rademacher 复杂度与快收敛率]]", "[[Fat-Shattering、回归与 Lipschitz 风险]]"]
created: 2026-08-23
updated: 2026-08-28
---

# 解答 - 覆盖数、Metric Entropy 与 Chaining 入口

> [!warning] 约定
> packing 使用 pairwise distance $>\varepsilon$；cover 使用 closed balls；除非另说，centers 属于被覆盖集合。端点 convention改变个别有限例题，不改变主要 rate。

## A. 识别与复述

### LT-ENT-A01

- internal $\varepsilon$-cover：$C\subseteq T$，且每个 $t\in T$ 都有 $c\in C$ 满足 $d(t,c)\le\varepsilon$；
- covering number：所有 internal $\varepsilon$-covers 的最小 cardinality $N(\varepsilon,T,d)$；
- $\varepsilon$-packing：$A\subseteq T$ 中任意不同两点距离 $>\varepsilon$；
- packing number：最大 packing cardinality $M(\varepsilon,T,d)$；
- metric entropy：$H(\varepsilon,T,d)=\log N(\varepsilon,T,d)$。

### LT-ENT-A02

$$
d_S(f,g)
=\left(\frac1m\sum_i(f(X_i)-g(X_i))^2\right)^{1/2}.
$$

若 $f,g$ 在 sample points 上完全相同但在其他 $x$ 上不同，则 $f\ne g$ 而 $d_S(f,g)=0$。所以它是函数类上的 pseudometric，却是 restriction-vector quotient 上的 metric。

### LT-ENT-A03

Metric entropy 的输入是 metric space 与 resolution，输出是逼近所需中心数的对数；没有 probability distribution。Shannon entropy 的输入是 probability law，输出是平均信息/编码长度。两者都出现 logarithm，但对象与 theorem 不同。

## B. 手算与数值判断

### LT-ENT-B01

两个 centers $0.25,0.75$ 的 closed radius-$0.25$ balls 分别覆盖

$$
[0,0.5],\qquad[0.5,1].
$$

所以 $N\le2$。一个 radius-$0.25$ interval 最长覆盖长度 $0.5$，不可能同时覆盖 endpoints 0 与 1，故 $N\ge2$。因此

$$
\boxed{N(0.25,[0,1],|\cdot|)=2}.
$$

### LT-ENT-B02

记 $v_0=(0,0),v_1=(1,0),v_2=(0,1)$。normalized metric：

$$
d_S(v_0,v_1)=d_S(v_0,v_2)=\sqrt{\frac12},
\qquad
d_S(v_1,v_2)=1.
$$

当 $\varepsilon=0.6<1/\sqrt2$，每个 internal ball 只能覆盖自己，所以

$$
N(0.6)=3.
$$

当 $\varepsilon=0.8>1/\sqrt2$，以 $v_0$ 为 center 的一个 ball 同时覆盖 $v_1,v_2$，所以

$$
N(0.8)=1.
$$

### LT-ENT-B03

$$
\begin{aligned}
0.05+\sqrt{\frac{2\log1000}{400}}
&=0.05+\sqrt{0.0345388}\\
&\approx0.05+0.18585\\
&=\boxed{0.23585}.
\end{aligned}
$$

它是指定 $\varepsilon$ 的单尺度 upper bound；仍可对其他 $\varepsilon$ 优化。

## C. 推导与证明

### LT-ENT-C01

设 $A$ 是任意 $2\varepsilon$-packing，$C$ 是任意 $\varepsilon$-cover。若一个 cover center $c$ 同时覆盖不同 $a,a'\in A$，则

$$
d(a,a')\le d(a,c)+d(c,a')\le2\varepsilon,
$$

与 packing 要求 $>2\varepsilon$ 矛盾。所以 $|A|\le|C|$；对最大 packing 与最小 cover 取极值得

$$
M(2\varepsilon)\le N(\varepsilon).
$$

再取一个 maximal $\varepsilon$-packing $A$。若存在 $t\in T$ 满足 $d(t,a)>\varepsilon$ 对所有 $a\in A$，则 $A\cup\{t\}$ 仍是更大的 packing，矛盾。因此 $A$ 是 $\varepsilon$-cover，故

$$
N(\varepsilon)\le|A|\le M(\varepsilon).
$$

### LT-ENT-C02

对 $\varepsilon$-net $C_\varepsilon$，选 $\pi(f)$ 使 $d_S(f,\pi(f))\le\varepsilon$。对每组 signs：

$$
\sup_f\frac1m\sum_i\sigma_if_i
\le
\sup_{c\in C_\varepsilon}\frac1m\sum_i\sigma_ic_i
+
\sup_f\left|\frac1m\sum_i\sigma_i(f_i-\pi(f)_i)\right|.
$$

由 Cauchy–Schwarz，第二项至多

$$
\sqrt{\frac1m\sum_i\sigma_i^2}
\sup_f d_S(f,\pi(f))
\le\varepsilon.
$$

若每个 net restriction vector normalized $L_2$ norm 至多 $A$，Massart lemma 给出

$$
\widehat{\mathfrak R}_S(C_\varepsilon)
\le A\sqrt{\frac{2\log|C_\varepsilon|}{m}}.
$$

取最小 net 得

$$
\widehat{\mathfrak R}_S(\mathcal F)
\le\varepsilon+A\sqrt{\frac{2\log N(\varepsilon)}m}.
$$

### LT-ENT-C03

对 $\varepsilon_k=2^{-k}D$ 的 nets $C_k$：

$$
f=\pi_0(f)+\sum_{k=1}^K[\pi_k(f)-\pi_{k-1}(f)]+[f-\pi_K(f)].
$$

由 triangle inequality：

$$
\begin{aligned}
d_S(\pi_k(f),\pi_{k-1}(f))
&\le d_S(\pi_k(f),f)+d_S(f,\pi_{k-1}(f))\\
&\le\varepsilon_k+\varepsilon_{k-1}
=3\varepsilon_k.
\end{aligned}
$$

第 $k$ 层 increment 数至多 $N(\varepsilon_k)N(\varepsilon_{k-1})$。finite maximum bound 因此支付大致

$$
\frac{\varepsilon_{k-1}}{\sqrt m}
\sqrt{\log N(\varepsilon_k)}.
$$

dyadic sum 是 $\int\sqrt{\log N(\varepsilon)}d\varepsilon$ 的 Riemann-type 上和；末端 residual 用 $O(\varepsilon_K)$ 控制。优化停止尺度得到 truncated Dudley bound。

## D. 边界、反例与纠错

### LT-ENT-D01

取有限集合 $T=\{a_1,\ldots,a_n\}$。令

$$
d_1(a_i,a_j)=\mathbf1\{i\ne j\},
\qquad
d_2=0.01d_1.
$$

对同一 $\varepsilon=0.5$：在 $d_1$ 下每个 ball 只能覆盖一个点，$N=n$；在 $d_2$ 下任意一个 center 与所有点距离至多 0.01，$N=1$。同一集合的 cover size 可因 metric 相差 $n$ 倍。

### LT-ENT-D02

若

$$
\log N(\varepsilon)\asymp\varepsilon^{-p},
$$

则 integrand 为 $\varepsilon^{-p/2}$。

- $p<2$：$\int_0^D\varepsilon^{-p/2}d\varepsilon<\infty$；可令 cutoff 逼近 0，保留 $m^{-1/2}$ 型。
- $p=2$：积分为 $\log(D/\alpha)$；需正 cutoff，产生临界 log。
- $p>2$：积分约 $\alpha^{1-p/2}$，小尺度发散。平衡
  $$
  \alpha+m^{-1/2}\alpha^{1-p/2}
  $$
  得 $\alpha\asymp m^{-1/p}$，bound 也约 $m^{-1/p}$。

cutoff 防止为有限样本无意义地支付无限精细几何。

### LT-ENT-D03

经验 cover 依赖 $X_{1:m}$ 合法，因为 empirical Rademacher complexity 先条件于该 sample，再对独立 signs 取期望；外层 theorem 已处理 sample randomness。

但若用 labels/empirical loss 训练并挑出一个看起来很小的 subclass，该 class 的 selection 本身利用了噪声与 outcomes。把它当预先 fixed class 会漏掉 data-adaptive selection capacity；需 sample splitting、union bound/penalty、stability、PAC-Bayes 或其他 adaptive theorem。

## E. AI 迁移

### LT-ENT-E01

若 parameter net $C\subseteq\Theta$ 满足每个 $\theta$ 有 $c$ 使

$$
\|\theta-c\|_2\le\varepsilon/L_S,
$$

则

$$
d_S(f_\theta,f_c)
\le L_S\|\theta-c\|_2
\le\varepsilon.
$$

所以

$$
N(\varepsilon,\mathcal F,d_S)
\le N(\varepsilon/L_S,\Theta,\|\cdot\|_2).
$$

深网中可能过松的原因：layer Lipschitz products 巨大；parameter permutation/rescaling 使 parameter space 重复覆盖同一函数；activation/data-dependent null directions 未被 quotient；local sensitivity 不能 uniform 扩展到整域。

### LT-ENT-E02

对 vector score $s_\theta(x,t)\in\mathbb R^d$，可定义

$$
d_S(s,s')
=\left[
\frac1m\sum_{i=1}^m
\|s(X_i,T_i)-s'(X_i,T_i)\|_2^2
\right]^{1/2}.
$$

若换 $\ell_\infty$ output norm，cover 与 dual process都会改变。$(X_i,T_i)$ 的 sampling law、noise level weighting 与 repeated-times dependency 决定 sample unit。squared score loss不是全局 Lipschitz，需 bounded outputs/targets、clipping、localized variance 或 tail theorem后才能 contraction。

### LT-ENT-E03

两层网络审计至少记录：

1. 输入 radius 与 empirical metric；
2. 两层 spectral/Frobenius/path norm；
3. activation Lipschitz、homogeneity 与 range；
4. width/parameter covers怎样组合；
5. hidden-unit permutation 与 positive rescaling symmetry；
6. scalar/vector output norm；
7. parameter perturbation到 function perturbation的 uniform constant；
8. entropy growth 在 0 附近是否可积；
9. cutoff $\alpha$ 与数值优化；
10. loss contraction、confidence 与 hyperparameter selection。
