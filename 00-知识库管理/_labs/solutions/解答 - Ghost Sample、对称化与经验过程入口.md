---
type: solution
status: draft
area: [learning-theory/empirical-process, probability/symmetrization]
topic: "[[习题 - Ghost Sample、对称化与经验过程入口]]"
prerequisites: ["[[Ghost Sample、对称化与经验过程入口]]"]
related: ["[[Rademacher 复杂度与经验复杂度]]"]
created: 2026-08-23
updated: 2026-08-23
---

# 解答 - Ghost Sample、对称化与经验过程入口

> [!warning] 使用边界
> 先给每一步标注随机对象与关系符号，再看代数。$\le$、$\overset d=$ 与 expectation equality 在对称化中承担不同逻辑角色。

## A. 识别与复述

### LT-SYM-A01

$$
Pf=\mathbb E_{Z\sim P}f(Z),\quad
P_mf=m^{-1}\sum_if(Z_i),\quad
P_m'f=m^{-1}\sum_if(Z_i').
$$

$$
S\sim P^m,\qquad S'\sim P^m,\qquad S\perp S'.
$$

证明中 $S'$ 使 $Pf=\mathbb E_{S'}P_m'f$，把未知期望换为独立经验均值的条件期望。算法不接收 $S'$；真实验证集若被算法访问会改变输出依赖合同，不能称为 proof ghost。

### LT-SYM-A02

本节采用 signed $1/m$ convention：

$$
\widehat{\mathfrak R}_S(\mathcal F)
=\mathbb E_\sigma\sup_{f\in\mathcal F}
\frac1m\sum_i\sigma_if(Z_i),
$$

$$
\mathfrak R_m(\mathcal F)=\mathbb E_S\widehat{\mathfrak R}_S(\mathcal F).
$$

one-sided theorem：

$$
\mathbb E_S\sup_f(Pf-P_mf)
\le2\mathfrak R_m(\mathcal F).
$$

### LT-SYM-A03

1. **Inequality：**$\sup_f\mathbb E_{S'}X_f\le\mathbb E_{S'}\sup_fX_f$；
2. **Distributional equality：**pairwise exchangeability 使 $(\widetilde S,\widetilde S')\overset d=(S,S')$，从而插入 signs；
3. **Subadditivity：**$\sup_f(A_f+B_f)\le\sup_fA_f+\sup_fB_f$，把 double-sample process 拆成两项。

## B. 手算与数值判断

### LT-SYM-B01

| $\sigma$ | $f_1$ score | $f_2$ score | sup |
|---|---:|---:|---:|
| $(+,+)$ | 0 | $1/2$ | $1/2$ |
| $(+,-)$ | 0 | $1/2$ | $1/2$ |
| $(-,+)$ | 0 | $-1/2$ | 0 |
| $(-,-)$ | 0 | $-1/2$ | 0 |

所以

$$
\widehat{\mathfrak R}_S
=\frac14(1/2+1/2)=\frac14.
$$

### LT-SYM-B02

$$
\sqrt{\frac{\log20}{4000}}
\approx\sqrt{0.0007489}
\approx0.0274.
$$

population-complexity one-sided bound为

$$
2(0.04)+0.0274\approx0.1074.
$$

它是 gap radius，不是 population risk 本身；还需加 empirical risk。

### LT-SYM-B03

若样本是 $a$：

$$
Pf_a-P_1f_a=1/2-1=-1/2,
$$

$$
Pf_b-P_1f_b=1/2-0=1/2.
$$

sup 为 $1/2$；样本是 $b$ 时对称。因此左侧 expectation 为 $1/2$。

固定样本 $a$，$m=1$：$f_a$ signed score 为 $\sigma$，$f_b$ 为 0；$\mathbb E\max(\sigma,0)=1/2$。样本 $b$ 同理，所以 $\mathfrak R_1=1/2$，$2\mathfrak R_1=1$。不等式 $1/2\le1$ 成立但不紧。

## C. 推导与证明

### LT-SYM-C01

固定 $S$。因为 $P_mf$ 对 $S'$ 是常数：

$$
\begin{aligned}
\sup_f(Pf-P_mf)
&=\sup_f\left(\mathbb E_{S'}P_m'f-P_mf\right)\\
&=\sup_f\mathbb E_{S'}(P_m'f-P_mf)\\
&\le\mathbb E_{S'}\sup_f(P_m'f-P_mf).
\end{aligned}
$$

最后一步是 supremum-of-expectations inequality。再对 $S$ 取 expectation，用 Tonelli/Fubini（或可积性假设）得结论。

### LT-SYM-C02

令

$$
(\widetilde Z_i,\widetilde Z_i')=
\begin{cases}
(Z_i,Z_i'),&\sigma_i=1,\\
(Z_i',Z_i),&\sigma_i=-1.
\end{cases}
$$

因为每对是 iid product $P\otimes P$，交换 map 保持其分布；各坐标独立，故完整 pairs 的 product joint law 不变。并且

$$
f(\widetilde Z_i')-f(\widetilde Z_i)
=\sigma_i(f(Z_i')-f(Z_i))
$$

（按本 convention）。因此对任何 measurable functional，特别是 signed supremum，其 expectation 在交换前后相同。

### LT-SYM-C03

$$
\begin{aligned}
&\mathbb E_{S,S',\sigma}\sup_f
\frac1m\sum_i\sigma_i(f(Z_i')-f(Z_i))\\
&\le
\mathbb E\sup_f\frac1m\sum_i\sigma_if(Z_i')
+\mathbb E\sup_f\frac1m\sum_i(-\sigma_i)f(Z_i)\\
&=\mathfrak R_m(\mathcal F)+\mathfrak R_m(\mathcal F)
=2\mathfrak R_m(\mathcal F).
\end{aligned}
$$

对 absolute gap，令 $\mathcal F_\pm=\mathcal F\cup(-\mathcal F)$：

$$
\sup_{f\in\mathcal F}|(P-P_m)f|
=\sup_{g\in\mathcal F_\pm}(P-P_m)g.
$$

对 $\mathcal F_\pm$ 应用 one-sided theorem，得

$$
\mathbb E\sup_f|(P-P_m)f|
\le2\mathfrak R_m(\mathcal F_\pm).
$$

## D. 边界、反例与纠错

### LT-SYM-D01

令 $\xi$ 为 Rademacher variable，$X_1=\xi,X_2=-\xi$。则

$$
\sup_{j=1,2}\mathbb EX_j=0,
$$

但每个 realization 中 $\max(\xi,-\xi)=1$，所以

$$
\mathbb E\sup_jX_j=1.
$$

严格不等说明允许 maximizer 随随机结果改变会提高值。

### LT-SYM-D02

令 $(Z,Z')=(0,1)$ 几乎处处。交换后是 $(1,0)$，原联合分布集中在前一有序点，交换分布集中在后一有序点，二者不同。若随机插入 sign，signed difference 会随机取原差与反差，但这不再与原固定方向差同分布，所以关键 equality 失效。

### LT-SYM-D03

expectation upper bound只约束随机变量平均值。删除 $\mathbb E$ 等价于声称几乎处处 pointwise bound，没有依据。正确路线：证明目标 functional 对每个 sample coordinate 的 bounded difference，再用 McDiarmid/Bousquet/Talagrand concentration；或在额外方差/尾部条件下使用相应 empirical-process tail theorem。

## E. AI 迁移

### LT-SYM-E01

8 个 views 共享同一 latent image/content，彼此强相关。若当作 8 个 iid 单位，会把 $m$ 虚增 8 倍，使 $1/\sqrt m$ 项虚假缩小约 $\sqrt8$。正确独立单位是原始 image；可把 8-view augmentation mechanism并入单个 observation 的 randomized loss，或对 groups 做 block-level analysis。

### LT-SYM-E02

InfoNCE 中第 $i$ 项含其他 batch elements 作为 denominator negatives，所以 loss 不是 $m^{-1}\sum_i f(Z_i)$ 中每项只依赖 $Z_i$ 的形式。替换一个 observation 会同时改变多个 terms。可把整个 batch 当一个 independent super-observation，或把 pair/batch statistic写成 U/V-statistic并使用相应 decoupling/symmetrization。

### LT-SYM-E03

- 训练样本 $S$：真实 observations，决定 learner output；
- ghost $S'$：证明中的 iid 副本，算法不可见；
- 算法种子 $U$：初始化、dropout、sampling 等训练随机性；
- signs $\sigma$：交换编码/complexity probe，与真实 labels 无关。

混用会改变概率量词。例如把 $S'$ 当 validation 会让 learner 依赖它；把 $U$ 当 signs 无法利用 sample-pair exchangeability；把 adaptive prompts 当 iid $S$ 则采样 law 已变化。
