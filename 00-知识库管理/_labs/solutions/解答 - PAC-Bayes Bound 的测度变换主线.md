---
type: solution
status: draft
area: [learning-theory/pac-bayes, measure-change]
topic: "[[PAC-Bayes Bound 的测度变换主线]]"
exercise: "[[习题 - PAC-Bayes Bound 的测度变换主线]]"
prerequisites: ["[[PAC-Bayes Bound 的测度变换主线]]"]
related: ["[[PAC-Bayes 先验、后验与数据依赖边界]]", "[[Occam 界、编码长度与先验权重]]"]
created: 2026-08-23
updated: 2026-08-28
---

# 解答 - PAC-Bayes Bound 的测度变换主线

> [!warning] 适用域
> 以下主定理按 i.i.d. binary 0–1 loss、data-independent prior、Gibbs predictor 与 nats convention 作答。

## A. 识别与复述

### LT-PBMC-A01

$$
\widehat R_S(Q)
=\mathbb E_{h\sim Q}\frac1m\sum_{i=1}^m\ell(h,Z_i),
\qquad
R(Q)=\mathbb E_{h\sim Q}\mathbb E_Z\ell(h,Z).
$$

对 \(q,p\in[0,1]\)，

$$
\operatorname{kl}(q\|p)
=q\log\frac qp+(1-q)\log\frac{1-q}{1-p}
$$

是在 Bernoulli outcome space 上的 scalar KL。若 \(Q\ll P\)，

$$
\operatorname{KL}(Q\|P)
=\int\log\frac{dQ}{dP}\,dQ
$$

是在 hypothesis space 上的 measure KL。前者比较 empirical/population error probabilities；后者衡量 posterior 相对 prior 的测度变化。

### LT-PBMC-A02

对每个与 \(S\) 独立的 \(P\) 和 \(\delta\in(0,1)\)，

$$
\mathbb P_S\left[
\forall Q,\ 
\operatorname{kl}(\widehat R_S(Q)\|R(Q))
\le
\frac{\operatorname{KL}(Q\|P)+\log((m+1)/\delta)}m
\right]\ge1-\delta.
$$

\(\forall Q\) 位于 high-probability event 内，所以 event 建立后可把任意 data-dependent \(Q_S\) 代入，不需再 union bound。

### LT-PBMC-A03

- Gibbs：每次预测采 \(h\sim Q\)，risk 为 \(\mathbb E_QR(h)\)；
- majority vote：对 posterior predictions 投票，是 deterministic aggregate；
- posterior mean network：用 mean parameters \(\mu_Q\)，非线性下不等于 mean prediction；
- MAP：选择 density/probability 最大的单个 hypothesis。

PAC-Bayes-kl 直接控制第一项。binary majority vote 可另用 \(R(B_Q)\le2R(Q)\)；其余一般无无条件 conversion。

## B. 手算与数值判断

### LT-PBMC-B01

$$
\begin{aligned}
\operatorname{KL}(Q\|P)
&=
\frac14\log\frac{1/4}{1/2}
+\frac12\log\frac{1/2}{1/3}
+\frac14\log\frac{1/4}{1/6}\\
&=
\frac14\log\frac12
+\frac12\log\frac32
+\frac14\log\frac32\\
&\approx-0.17329+0.20273+0.10137\\
&=\boxed{0.13081\text{ nats}}.
\end{aligned}
$$

### LT-PBMC-B02

$$
\log\frac{1001}{0.05}
=\log(20020)
\approx9.90449.
$$

所以

$$
c
=\frac{8+9.90449}{1000}
\approx\boxed{0.0179045}.
$$

零经验风险时

$$
R(Q)\le1-e^{-c}
\approx1-0.982255
=\boxed{0.017745}.
$$

### LT-PBMC-B03

Pinsker 给

$$
\sqrt{\frac c2}
=\sqrt{0.00895225}
\approx\boxed{0.094616}.
$$

相对 exact zero-risk bound：

$$
\frac{0.094616}{0.017745}
\approx\boxed{5.33}.
$$

这是为何 empirical risk 很小时不应过早丢掉 inverse binary KL。

## C. 推导与证明

### LT-PBMC-C01

令 \(r=dQ/dP\)。则

$$
\begin{aligned}
\mathbb E_Qf-\operatorname{KL}(Q\|P)
&=\mathbb E_Q\left[f-\log r\right]\\
&=\mathbb E_Q\log\left(\frac{e^f}{r}\right)\\
&\le
\log\mathbb E_Q\left[\frac{e^f}{r}\right]\\
&=\log\int_{\{r>0\}}e^f\,dP\\
&\le\log\mathbb E_Pe^f.
\end{aligned}
$$

第三行是 concave \(\log\) 的 Jensen inequality。最后保留不等号，因为 \(Q\ll P\) 不要求 \(P\ll Q\)；\(P\) 可能在 \(\{r=0\}\) 上还有质量。移项即得结论。若 \(Q\not\ll P\)，KL 约定为 infinity，inequality 退化为平凡真。

### LT-PBMC-C02

固定 \(h\)，记 \(p=R(h)\)、\(K=m\widehat R_S(h)\sim\mathrm{Bin}(m,p)\)。期望为

$$
\sum_{k=0}^m
{m\choose k}p^k(1-p)^{m-k}
e^{m\operatorname{kl}(k/m\|p)}.
$$

第 \(k\) 项化简为

$$
{m\choose k}
\left(\frac km\right)^k
\left(1-\frac km\right)^{m-k}.
$$

它是参数 \(k/m\) 的 binomial distribution 在 \(k\) 处的概率，故不超过 \(1\)。共有 \(m+1\) 项，和不超过 \(m+1\)。\(k=0,m\) 用 \(0^0=1\) 的连续延拓解释。

### LT-PBMC-C03

令

$$
M(S)
=\mathbb E_{h\sim P}
e^{m\operatorname{kl}(\widehat R_S(h)\|R(h))}.
$$

因 \(P\) 与 \(S\) 独立，Tonelli 与 C02 给

$$
\mathbb E_SM(S)\le m+1.
$$

Markov：

$$
\mathbb P\left(M(S)\le\frac{m+1}{\delta}\right)
\ge1-\delta.
$$

在该 event 内，对任意 \(Q\) 和

$$
f(h)=m\operatorname{kl}(\widehat R_S(h)\|R(h))
$$

使用 C01：

$$
\mathbb E_Qf
\le\operatorname{KL}(Q\|P)+\log\frac{m+1}{\delta}.
$$

再由 Bernoulli KL joint convexity：

$$
\operatorname{kl}(\widehat R_S(Q)\|R(Q))
\le
\mathbb E_Q\operatorname{kl}(\widehat R_S(h)\|R(h)).
$$

除以 \(m\) 得主定理。因为 good event 与 \(Q\) 无关，结论 simultaneous over all \(Q\)。

## D. 边界、反例与纠错

### LT-PBMC-D01

Gaussian \(P\) 对单点 \(\{w\}\) 的质量为零，而 \(\delta_w(\{w\})=1\)。所以

$$
Q\not\ll P,
\qquad
\operatorname{KL}(Q\|P)=+\infty.
$$

右侧无限，不能提供 nonvacuous bound。要使用 continuous prior，通常选择有 density 且 support 被 \(P\) 覆盖的 noisy posterior。

### LT-PBMC-D02

标准 proof 在

$$
\mathbb E_S\mathbb E_{h\sim P}e^{f(S,h)}
=\mathbb E_{h\sim P}\mathbb E_Se^{f(S,h)}
$$

处使用 \(P\) 与 \(S\) 的独立性。训练后设 \(P_S=Q_S\) 破坏该交换。形式上 KL=0 只是把 data dependence 藏进 prior，没有控制其选择复杂度。合法路线是 independent prior、split prior、fixed mixture/union budget 或 specialized data-dependent-prior theorem。

### LT-PBMC-D03

令

$$
G=
\begin{cases}
1,&\text{probability }1/2,\\
-1,&\text{probability }1/2.
\end{cases}
$$

则

$$
|\mathbb EG|=0,
\qquad
\mathbb E|G|=1,
\qquad
\mathbb P(|G|=1)=1.
$$

所以 signed expectation 小不能推出 realized gap 或 expected absolute gap 小。

## E. AI 迁移

### LT-PBMC-E01

最小 report：

1. certificate dataset 与 \(m\)；
2. bounded loss definition；
3. prior family、参数与独立性证据；
4. posterior family、mean/covariance 与 support；
5. sampling algorithm \(W\sim Q\)；
6. empirical Gibbs-risk estimate；
7. Monte Carlo sample size 与 upper confidence correction；
8. analytic/numerical \(\operatorname{KL}(Q\|P)\)；
9. \(\delta\) 及多重选择预算；
10. inverse-kl implementation/tolerance；
11. resulting risk bound；
12. deployed predictor 是 Gibbs、vote 还是 center。

缺少第 12 项会使 certificate object 与实际系统错位。

### LT-PBMC-E02

\(\widehat R_S(h_{\mu_Q})\) 只评估一个 center network，而 theorem 需要

$$
\widehat R_S(Q)
=\mathbb E_{W\sim Q}\widehat R_S(h_W).
$$

合法 estimator 是采样 \(W_1,\ldots,W_K\overset{\rm iid}{\sim}Q\)，计算

$$
\widetilde R
=\frac1K\sum_{k=1}^K\widehat R_S(h_{W_k}),
$$

再为有限 \(K\) 加 upper confidence correction。若部署 center network，仍需独立 conversion theorem。

### LT-PBMC-E03

固定 \(q\in[0,1]\)、\(c\ge0\)。要找最大 \(p\in[q,1]\) 使

$$
\operatorname{kl}(q\|p)\le c.
$$

procedure：

1. 若 \(c=0\)，返回 \(q\)；
2. 若 \(q=1\)，只能返回 \(1\)；
3. 若 \(q=0\)，可直接返回 \(1-e^{-c}\)；
4. 否则在 \([q,1-\varepsilon_{\rm machine}]\) 上 binary search；
5. 对 \(p\ge q\)，\(\operatorname{kl}(q\|p)\) 单调不减；
6. 中点若 KL \(\le c\)，移动 lower endpoint，否则移动 upper；
7. 以 interval width 或 KL residual 为停止条件；
8. 用 \(\log1p\) 计算 \(\log(1-p)\) 防止边界 cancellation；
9. 最终返回 feasible lower endpoint，保持 upper-certificate 保守性。
