---
type: solution
status: draft
area: [learning-theory/scale-sensitive-dimension, regression/generalization]
topic: "[[习题 - Fat-Shattering、回归与 Lipschitz 风险]]"
prerequisites: ["[[Fat-Shattering、回归与 Lipschitz 风险]]"]
related: ["[[分类间隔、Margin Bound 与 SVM 接口]]", "[[覆盖数、Metric Entropy 与 Chaining 入口]]"]
created: 2026-08-23
updated: 2026-08-23
---

# 解答 - Fat-Shattering、回归与 Lipschitz 风险

> [!warning] 尺度约定
> 本解答沿用正文的两侧各留 $\gamma$ margin，即正侧至少 $r_i+\gamma$、负侧至多 $r_i-\gamma$。若文献使用 $\gamma/2$，所有尺度下标需同步换算。

## A. 识别与复述

### LT-FAT-A01

$x_1,ldots,x_d$ 被 $\gamma$-fat-shattered，当且仅当

$$
\exists r_1,ldots,r_d\in\mathbb R,
\quad
\forall s\in\{-1,+1\}^d,
\quad
\exists f_s\in\mathcal F,
\quad
\forall i,
$$

满足

$$
s_i(f_s(x_i)-r_i)\ge\gamma.
$$

关键是 thresholds 在 sign pattern 之前固定；函数可随整个 pattern 改变。

### LT-FAT-A02

- VC dimension：binary class 实现所有 $0/1$ patterns；
- pseudo-dimension：实值 class 相对逐点 fixed thresholds 实现所有高/低 patterns，但不要求统一 positive gap；
- fat-shattering profile：对每个 $\gamma>0$，要求离 thresholds 至少 $\gamma$，保留 resolution 信息。

因此 fat$_\gamma\le$Pdim；对 binary class 与 $0<\gamma\le1/2$，正文 convention 下 fat$_\gamma=$VCdim。

### LT-FAT-A03

若 $\gamma_1\le\gamma_2$：

$$
\operatorname{fat}_{\gamma_2}(\mathcal F)
\le\operatorname{fat}_{\gamma_1}(\mathcal F).
$$

若 $\mathcal F\subseteq\mathcal G$：

$$
\operatorname{fat}_\gamma(\mathcal F)
\le\operatorname{fat}_\gamma(\mathcal G).
$$

对 $a>0$：

$$
\operatorname{fat}_\gamma(a\mathcal F)
=\operatorname{fat}_{\gamma/a}(\mathcal F).
$$

对固定 $g$：

$$
\operatorname{fat}_\gamma(\mathcal F+g)
=\operatorname{fat}_\gamma(\mathcal F).
$$

## B. 手算与数值判断

### LT-FAT-B01

常数值域宽度为 4。一个点能被 $\gamma$-fat-shatter 的必要充分条件是可在某 threshold 两侧各留 $\gamma$，即

$$
2\gamma\le4.
$$

当 $\gamma=1$，取 threshold 0，functions $c=2$ 与 $c=-2$ 实现正负 pattern，所以至少能 shatter 1 点。两个点上的 mixed pattern 无法由同一个 constant 实现，故

$$
\boxed{\operatorname{fat}_1=1}.
$$

当 $\gamma=3$，需要总 gap 6，超过 range width 4，连一个点也不能 shatter：

$$
\boxed{\operatorname{fat}_3=0}.
$$

### LT-FAT-B02

$$
\left(\frac{BR}{\gamma}\right)^2
=\left(\frac{3\cdot2}{0.5}\right)^2
=12^2=144.
$$

结合 ambient/pseudo-dimension ceiling $p=100$：

$$
\operatorname{fat}_{0.5}
\le\min\{100,144\}
=\boxed{100}
$$

（忽略 affine bias/不同 convention 的常数）。

### LT-FAT-B03

由 amplitude scaling：

$$
\operatorname{fat}_2(4\mathcal F)
=\operatorname{fat}_{2/4}(\mathcal F)
=\operatorname{fat}_{0.5}(\mathcal F)
=\boxed{25}.
$$

## C. 推导与证明

### LT-FAT-C01

**尺度：**任何满足 margin $\gamma_2$ 的同一 witnesses 都满足较小 $\gamma_1$，故 dimension 随尺度不增。

**缩放：**若 $f_s,r_i$ 在 $\mathcal F$ 中以 margin $\gamma/a$ 作 witnesses，则 $af_s,ar_i$ 满足

$$
s_i(af_s(x_i)-ar_i)
=a s_i(f_s(x_i)-r_i)
\ge\gamma.
$$

反向除以 $a$，得到 equality。

**平移：**若 $f_s,r_i$ 是原类 witnesses，则 $f_s+g$ 与 thresholds $r_i+g(x_i)$ 满足

$$
s_i[(f_s(x_i)+g(x_i))-(r_i+g(x_i))]
=s_i(f_s(x_i)-r_i)
\ge\gamma.
$$

反向平移 $-g$，得到 equality。

### LT-FAT-C02

对每组 Rademacher signs $\sigma$，fat definition 给出 $f_\sigma$，使

$$
\sigma_i(f_\sigma(x_i)-r_i)\ge\gamma.
$$

于是

$$
\sup_f\frac1d\sum_i\sigma_if(x_i)
\ge
\frac1d\sum_i\sigma_if_\sigma(x_i)
\ge
\gamma+\frac1d\sum_i\sigma_i r_i.
$$

对 signs 取期望，因 $\mathbb E\sigma_i=0$：

$$
\widehat{\mathfrak R}_{x_{1:d}}(\mathcal F)
\ge\gamma.
$$

### LT-FAT-C03

对 norm-constrained linear class 与 $\|x_i\|\le R$：

$$
\widehat{\mathfrak R}_{x_{1:d}}(\mathcal F_B)
\le\frac B d\sqrt{\sum_{i=1}^d\|x_i\|^2}
\le\frac{BR}{\sqrt d}.
$$

若这 $d$ 点被 $\gamma$-fat-shattered，C02 又给出 complexity 至少 $\gamma$。合并：

$$
\gamma\le\frac{BR}{\sqrt d}
\quad\Longrightarrow\quad
d\le\left(\frac{BR}{\gamma}\right)^2.
$$

对所有可 shattered 的 $d$ 取 supremum即得

$$
\operatorname{fat}_\gamma(\mathcal F_B)
\le(BR/\gamma)^2.
$$

## D. 边界、反例与纠错

### LT-FAT-D01

若允许 thresholds 随 sign pattern $s$ 改变，则即便 class 只有一个固定函数 $f_0$，对任意点数与任意 $s$ 都可选

$$
r_{i,s}=f_0(x_i)-s_i\gamma.
$$

于是

$$
s_i(f_0(x_i)-r_{i,s})
=s_i(s_i\gamma)=\gamma.
$$

单函数类将“shatter”任意多点，definition 完全失去容量区分力。这说明量词 $\exists r\,\forall s$ 不能颠倒为 $\forall s\,\exists r$。

### LT-FAT-D02

常数类由连续参数 $c\in[-B,B]$ 索引，却最多 fat-shatter 一个点；当 $\gamma>B$ 时连一个点也不能。连续/infinite parameter cardinality 不等于能独立操纵多个 sample coordinates。capacity 取决于 restriction geometry 与 resolution。

### LT-FAT-D03

squared loss 差商为

$$
\frac{|(u-y)^2-(v-y)^2|}{|u-v|}
=|u+v-2y|,
$$

在全实轴无上界，不能取 $L=1$。若 $|u|,|v|,|y|\le B$，可取 $L=4B$，loss range 至多 $4B^2$。此时先用 fat/cover 得 score complexity，再用 $4B$ contraction，并按 loss range 使用正确 concentration；或使用专门 unbounded/localized regression theorem。

## E. AI 迁移

### LT-FAT-E01

Frozen embedding $h(x)$ 上的 linear head $f_w=\langle w,h(x)\rangle$：

$$
\|w\|\le B,\quad\|h(x)\|\le R
\Rightarrow
\operatorname{fat}_\gamma\lesssim
\min\{p,(BR/\gamma)^2\}.
$$

然后选择完整 fat-to-cover theorem：

$$
\operatorname{fat}_{c\varepsilon}
\Rightarrow
\log N(\varepsilon,\mathcal F,d_S)
\Rightarrow
\widehat{\mathfrak R}_S(\mathcal F)
$$

（Dudley integral），再由 $L$-Lipschitz bounded loss 得

$$
P\ell_f
\le P_m\ell_f
+4L\widehat{\mathfrak R}_S(\mathcal F)
+\text{confidence}.
$$

缺失/需声明的常数包括 fat convention、cover metric/log factors、output/loss range、bias、confidence、encoder independence 与 threshold/candidate selection。

### LT-FAT-E02

pairwise preference 只读取

$$
g_f(x^+,x^-)=f(x^+)-f(x^-).
$$

公共 shift $f\mapsto f+c$ 不改变 $g_f$，所以绝对 reward level 不可识别。应研究 difference class

$$
\Delta\mathcal F
=\{(x^+,x^-)\mapsto f(x^+)-f(x^-):f\in\mathcal F\},
$$

在 pair sampling metric 下的 fat/cover/Rademacher complexity，并审计同一 item 重复出现在 pairs 导致的 dependency。

### LT-FAT-E03

Diffusion score $s_\theta(x,t)\in\mathbb R^d$ 需要 vector-valued capacity，因为随机过程与 loss 同时跨 output coordinates。至少要声明：

1. output norm 及 dual norm；
2. $(X,T,\text{noise})$ 的 sample unit 与 weighting；
3. target score 的 tail/moment；
4. squared-loss prediction/target range或 localized moment condition；
5. time-conditioned class 是否共享参数；
6. vector contraction/covering theorem。

scalar fat dimension不能自动处理这些 coupling。
