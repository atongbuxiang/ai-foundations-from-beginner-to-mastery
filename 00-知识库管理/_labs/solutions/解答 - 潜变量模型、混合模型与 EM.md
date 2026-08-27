---
type: solution
status: draft
area: [learning-theory/latent-variable-models, mixture-models, em]
topic: "[[习题 - 潜变量模型、混合模型与 EM]]"
prerequisites: ["[[潜变量模型、混合模型与 EM]]"]
related: ["[[模型可辨识性、选择与 Misspecification]]", "[[K-Means、聚类风险与不可辨识性]]"]
created: 2026-08-23
updated: 2026-08-23
---

# 解答 - 潜变量模型、混合模型与 EM

> [!warning] 解题原则
> 每一步先标出固定对象：E-step固定 (\theta^{(t)}) 优化 (q)，M-step固定 (q^{(t)}) 改善 (\theta)。bound tightness与likelihood monotonicity是代数结论；MLE存在、parameter convergence、global optimality、identifiability与consistency需要额外条件。

## A. 识别与复述

### LT-EM-A01

- (X)：实际观测random variable；
- (Z)：模型引入但未直接观测的latent variable；
- (\theta)：索引joint laws的固定未知parameter，不是每个样本一个hidden draw；
- (p_\theta(z\mid x))：给定 (x) 与parameter后对 (Z) 的conditional distribution；
- complete-data likelihood：把 (x,z) 都当已知时的 (p_\theta(x,z))；
- observed likelihood：把latent variable marginalize：
  $$
  p_\theta(x)=\sum_zp_\theta(x,z)
  $$
  或积分。

在mixture中responsibility (\gamma_{ik}=P_\theta(Z_i=k\mid X_i)) 是posterior probability，不是已观测标签，也不自动对应人类类别。

### LT-EM-A02

| 方法 | latent/inference step | parameter step | 主要误差来源 |
|---|---|---|---|
| exact EM | $q^{(t)}=p_{\theta^{(t)}}(z\mid x)$ | exact maximize $Q$ | local/singular/statistical问题仍在 |
| generalized EM | exact posterior常见 | 只要求 $Q$ 不下降 | inner optimization未完全收敛 |
| variational EM | 在受限 (q\in\mathcal Q) 中maximize ELBO | maximize/改善同一ELBO | variational gap |
| Monte Carlo EM | sampling近似E-step expectation | 对随机近似 $Q$ 优化 | Monte Carlo error，需schedule/control |
| amortized inference | (q_\phi(z\mid x)) 由共享network输出 | jointly/stochastically优化 (\theta,\phi) | approximation + amortization + optimization gap |

variational/amortized方法通常保证的是所实现ELBO的改善，不是exact observed likelihood每步单调。

### LT-EM-A03

逻辑强度不同：

1. monotonicity：(\ell(\theta^{t+1})\ge\ell(\theta^t))；
2. value convergence：若上界有限，monotone values可收敛；
3. iterate convergence：整个 (\theta^t) 收敛到一个point；
4. stationary point：limit满足适当一阶条件；
5. local maximum：邻域内不小于其他points；stationary也可能是saddle/boundary；
6. global maximum：全parameter space最优；
7. statistical consistency：随fresh samples (n\to\infty)，estimator接近population target。

前一个通常不推出后一个。mixture likelihood无界时，甚至value convergence的前提也可能失败。

## B. 手算与数值判断

### LT-EM-B01

共同variance与weights相同，component 2 responsibility为

$$
\gamma_2(x)
=
\frac{\phi(x;2,1)}{\phi(x;0,1)+\phi(x;2,1)}.
$$

在 (x=0)：

$$
\frac{e^{-2}}{1+e^{-2}}
=\frac1{1+e^2}
\approx\boxed{0.119203}.
$$

在 (x=2)：

$$
\frac1{1+e^{-2}}
\approx\boxed{0.880797}.
$$

两者加和为1来自模型关于midpoint 1的symmetry。responsibility不是0/1，即使point恰落在某component mean上也仍考虑另一component density。

### LT-EM-B02

令 (N_2=\sum_i\gamma_{i2}=0.1+0.5+0.9=1.5)。所以

$$
\pi_2^{\rm new}=N_2/n=1.5/3=\boxed{0.5}.
$$

mean：

$$
\mu_2^{\rm new}
=\frac{0.1(-2)+0.5(0)+0.9(2)}{1.5}
=\frac{1.6}{1.5}
=\boxed{\frac{16}{15}\approx1.0667}.
$$

variance使用new mean：

$$
(\sigma_2^2)^{\rm new}
=\frac{\sum_i\gamma_{i2}(x_i-16/15)^2}{1.5}.
$$

也可用 weighted second moment：

$$
\frac{0.1(4)+0.5(0)+0.9(4)}{1.5}
-\left(\frac{16}{15}\right)^2
=\frac{8}{3}-\frac{256}{225}
=\boxed{\frac{344}{225}\approx1.5289}.
$$

### LT-EM-B03

直接计算 (e^{1000}) 会overflow。取 (m=\max(a,b)=1000)：

$$
\log(e^a+e^b)
=m+\log(e^{a-m}+e^{b-m}).
$$

所以

$$
=1000+\log(1+e^{-1})
\approx1000+0.3132617
=\boxed{1000.313262}.
$$

一般公式为

$$
\operatorname{LSE}(a_1,\ldots,a_K)
=m+\log\sum_ke^{a_k-m}.
$$

## C. 推导与证明

### LT-EM-C01

对support compatible的任意 (q(z))：

$$
\begin{aligned}
\log p_\theta(x)
&=\sum_zq(z)\log p_\theta(x)\\
&=\sum_zq(z)\log\frac{p_\theta(x,z)}{p_\theta(z\mid x)}.
\end{aligned}
$$

插入 (q(z))：

$$
\begin{aligned}
\log p_\theta(x)
&=\sum_zq(z)\log\frac{p_\theta(x,z)}{q(z)}
+\sum_zq(z)\log\frac{q(z)}{p_\theta(z\mid x)}\\
&=E_q[\log p_\theta(x,Z)]+H(q)
+D_{\rm KL}(q\|p_\theta(\cdot\mid x)).
\end{aligned}
$$

定义

$$
\mathcal F(q,\theta)=E_q[\log p_\theta(x,Z)]+H(q).
$$

KL非负，所以 (\mathcal F\le\log p_\theta(x))；且当且仅当

$$
q(z)=p_\theta(z\mid x)
$$

（在 (q)-a.s./support意义下）取等。exact E-step在当前 (\theta^{(t)}) 选这个posterior，因此current bound tight。

### LT-EM-C02

令

$$
q^{(t)}(z)=p_{\theta^{(t)}}(z\mid x).
$$

于是

$$
\ell(\theta^{(t)})
=\mathcal F(q^{(t)},\theta^{(t)}).
$$

若 exact M-step最大化 (\mathcal F(q^{(t)},\theta))，或 generalized M-step至少选择 (\theta^{(t+1)}) 使

$$
\mathcal F(q^{(t)},\theta^{(t+1)})
\ge
\mathcal F(q^{(t)},\theta^{(t)}),
$$

则由ELBO性质

$$
\begin{aligned}
\ell(\theta^{(t+1)})
&\ge\mathcal F(q^{(t)},\theta^{(t+1)})\\
&\ge\mathcal F(q^{(t)},\theta^{(t)})\\
&=\ell(\theta^{(t)}).
\end{aligned}
$$

固定 (q^{(t)}) 时 entropy (H(q^{(t)})) 与 (\theta) 无关，所以改善

$$
Q(\theta\mid\theta^{(t)})
=E_{q^{(t)}}[\log p_\theta(x,Z)]
$$

等价于改善 (\mathcal F)。注意若E-step不是exact current posterior，起点bound未必tight，不能用同一链条证明observed likelihood单调。

### LT-EM-C03

GMM complete expected log-likelihood中与component (k) 有关的部分为

$$
Q_k
=\sum_i\gamma_{ik}
\left[
\log\pi_k
-\frac12\log|\Sigma_k|
-\frac12(x_i-\mu_k)^\top\Sigma_k^{-1}(x_i-\mu_k)
\right]
+\text{const}.
$$

定义effective count

$$
N_k=\sum_i\gamma_{ik}.
$$

对weights在 (\sum_k\pi_k=1) 下用Lagrange multiplier，得

$$
\boxed{\pi_k^{\rm new}=N_k/n}.
$$

对 (\mu_k) 求导并令零：

$$
\boxed{
\mu_k^{\rm new}
=\frac1{N_k}\sum_i\gamma_{ik}x_i.
}
$$

对 covariance 的standard Gaussian likelihood optimization给出

$$
\boxed{
\Sigma_k^{\rm new}
=\frac1{N_k}\sum_i\gamma_{ik}
(x_i-\mu_k^{\rm new})(x_i-\mu_k^{\rm new})^\top.
}
$$

它们分别是soft counts、weighted first moment与weighted centered second moment。若 covariance tied/diagonal/isotropic，需在相应constraint下重新优化，不能照抄full-covariance式。

## D. 边界、反例与纠错

### LT-EM-D01

mixture density

$$
p_\theta(x)=\sum_{k=1}^K\pi_kf(x;\eta_k).
$$

对任意permutation (\sigma)：

$$
\sum_k\pi_{\sigma(k)}f(x;\eta_{\sigma(k)})
=\sum_j\pi_jf(x;\eta_j).
$$

所以 observed likelihood完全相同。不同runs可能把同一个geometric component编号为1或2；若直接平均“component 1 mean”，可能把互换后的不同components混合，得到任何run都不存在的中间值。应先用permutation-invariant summaries或posterior relabel/alignment，并承认语义还需外部识别。

### LT-EM-D02

在univariate GMM中选择一个component mean等于某 observation (x_j)，令variance (\sigma^2\downarrow0)，并保持其weight (\pi>0)。该point的component density为

$$
\pi\phi(x_j;x_j,\sigma^2)
=\frac{\pi}{\sqrt{2\pi}\sigma}\to\infty.
$$

其他components仍可给其余observations正density，因此total log-likelihood可趋于无穷。于是unconstrained finite MLE可能不存在。

这不是普通“困在有限的差local maximum”：它是objective沿boundary/singular sequence无界。variance floor、penalized likelihood、proper prior或constrained covariance能改变问题，但必须报告新objective。

### LT-EM-D03

至少有以下缺口：

1. monotone likelihood可能趋向finite value但parameters在level set中cycling；
2. limit point可能只是stationary point或saddle；
3. 不同initialization可到不同local maxima；
4. global maximum未被保证；
5. Gaussian mixture likelihood可能因variance collapse无界，MLE不存在；
6. label switching使parameter representation不唯一；
7. components接近时weak identification导致slow/unstable estimates；
8. numerical stopping tolerance只说明increments小；
9. model可能misspecified；
10. fixed-(n) algorithm convergence不等于 (n\to\infty) statistical consistency。

严谨报告应分别给 likelihood trace、gradient/stationarity residual、multiple starts、degeneracy checks与held-out predictive diagnostics。

## E. AI 迁移

### LT-EM-E01

mixture-of-experts可写

$$
p(y\mid x)
=\sum_{z=1}^Kp_\theta(z\mid x)
p_\theta(y\mid x,z).
$$

(Z) 是expert routing。若可计算 (p(z\mid x,y))，exact E-step产生posterior responsibilities并对expected complete log-likelihood更新router/experts。learned amortized router (q_\phi(z\mid x,y)) 或 (q_\phi(z\mid x)) 会引入approximation/amortization gap；joint SGD通常不再是closed-form exact EM。hard routing把soft posterior替换为point assignment，改变optimization geometry，可能产生dead experts与discontinuous assignments。还要加入load balancing/capacity penalties，这已是修改后的training objective。

### LT-EM-E02

VAE同样最大化

$$
\mathcal L(x;\theta,\phi)
=E_{q_\phi(z\mid x)}[\log p_\theta(x,z)]
+H(q_\phi(z\mid x)).
$$

与exact EM的共同点是ELBO/KL分解；差别是：

- true posterior常不可解，(q_\phi) 受variational family限制；
- 一个encoder共享跨observations映射，产生amortization gap；
- (\theta,\phi) 通常用mini-batch stochastic gradients交替或联合更新；
- decoder M-step不一定exact maximize；
- 单步observed likelihood monotonicity通常没有；
- reparameterization/score estimators引入sampling noise。

因此VAE训练曲线是stochastic ELBO estimate，不应被称为exact EM likelihood trace。

### LT-EM-E03

审计协议：

1. 写出 observed/latent variables、joint law与target functional；
2. 列出label permutation及其他equivalences；
3. 明确anchor/conditional-independence/noise assumptions，并做可反驳性检查；
4. 多initializations，报告likelihood/ELBO、matched parameters与predictions分布；
5. 检查boundary、collapsed classes、near-zero weights与weak separation；
6. 用independent expert labels或gold subset评价latent-label calibration，不用training assumptions自证；
7. 对class prevalence、confusion/noise matrix做sensitivity analysis；
8. inner loop选择 (K)、priors、regularization，outer data评价；
9. 不把component编号直接命名为语义；先alignment并给uncertainty；
10. domain/time shift下重新验证anchors、prevalence与calibration。
