---
type: concept
status: verified
area: [generative-models, vae, importance-sampling]
aliases: [IWAE, VAE似然估计与推断缺口]
node_id: GEN-13
prerequisites: ["[[VAE 的 ELBO、变分后验与重参数化梯度]]", "[[Monte Carlo、重要性采样与方差缩减]]", "[[凸函数、Jensen 不等式与上图集]]"]
related: ["[[Posterior Collapse、率失真与解码器容量]]", "[[Monte Carlo、重要性采样与方差缩减]]"]
sources: ["[[S-2021-Su-8791-VAE估计样本概率密度]]", "[[S-2015-Burda-IWAE]]"]
exercises: ["[[习题 - IWAE、重要性权重与推断缺口]]"]
solutions: ["[[解答 - IWAE、重要性权重与推断缺口]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-vae-iwae-gap-ladder-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# IWAE、重要性权重与推断缺口

> [!abstract] 本节主问题
> 从 $q_\phi(z\mid x)$ 抽多份 latent 并计算 importance weight，可以构造 evidence 的无偏密度估计器与一族更紧的 log 下界。但“密度估计无偏”“log 估计无偏”“$K$ 增大训练一定更好”“bound gap 就是 encoder 不够强”是四个不同命题，只有第一个一般成立。

## 一、从 evidence 的换测度开始

固定 $x$，若 support 条件满足，定义

$$
w(z)=\frac{p_\theta(x,z)}{q_\phi(z\mid x)}.
$$

则

$$
\mathbb E_{q_\phi}[w(Z)]
=\int q_\phi(z\mid x)\frac{p_\theta(x,z)}{q_\phi(z\mid x)}dz
=p_\theta(x).
$$

取 iid $z_1,\ldots,z_K\sim q_\phi(z\mid x)$，

$$
\widehat p_K(x)=\frac1K\sum_{k=1}^Kw_k
$$

是 $p_\theta(x)$ 的无偏 estimator。这不意味着 $\log\widehat p_K$ 对 $\log p_\theta(x)$ 无偏。

## 二、IWAE 下界

定义

$$
\mathcal L_K(x)=
\mathbb E_{z_{1:K}\sim q_\phi}
\left[\log\left(\frac1K\sum_{k=1}^K
\frac{p_\theta(x,z_k)}{q_\phi(z_k\mid x)}\right)\right].
$$

Jensen 给出

$$
\mathcal L_K(x)\le
\log\mathbb E[\widehat p_K(x)]
=\log p_\theta(x).
$$

$K=1$ 时恰为 ordinary ELBO。标准条件下有

$$
\mathcal L_1\le\mathcal L_2\le\cdots\le\log p_\theta(x),
$$

且 proposal 合适、矩条件成立时趋近 log evidence。“bound 随 $K$ 紧”是 expectation 层面的结论；一次运行的 $\log\widehat p_K$ 不必随 $K$ 单调。

## 三、为什么 log estimator 向下偏

由于 $\log$ concave：

$$
\mathbb E[\log\widehat p_K]\le
\log\mathbb E[\widehat p_K]
=\log p_\theta(x).
$$

delta method 给出大 $K$ 近似偏差

$$
\mathbb E[\log\widehat p_K]-\log p(x)
\approx-\frac{\operatorname{Var}(w)}
{2K\,p(x)^2}.
$$

所以 weight coefficient of variation 决定收敛速度。若少数样本承担几乎全部权重，名义 $K$ 很大而有效样本量仍很小：

$$
\operatorname{ESS}=
\frac{(\sum_k w_k)^2}{\sum_k w_k^2}\in[1,K].
$$

## 四、归一化权重与 posterior expectation

令

$$
\widetilde w_k=\frac{w_k}{\sum_jw_j}.
$$

则 $\sum_k\widetilde w_k f(z_k)$ 是 posterior expectation 的 self-normalized importance estimator。它一般有有限样本 bias，但一致。不要把“evidence estimator 无偏”错误传给“normalized posterior estimator 无偏”。

## 五、四类缺口必须分账

对给定数据与训练程序，可以拆成：

### 5.1 Model gap

模型族的最佳 $p_\theta(x)$ 与真实 $p_*(x)$ 仍有差距。再完美的 inference 也无法修复错误 likelihood 或 decoder family。

### 5.2 Approximation / family gap

即使为每个 $x$ 单独优化，所选 $\mathcal Q$ 也无法表示真 posterior，例如 diagonal Gaussian 逼近强相关或多峰分布。

### 5.3 Amortization gap

共享 encoder 给出的 $q_\phi(z\mid x)$ 不如“对该 $x$ 单独优化 variational parameters”所得最佳 $q_x^*$。

### 5.4 Optimization 与 Monte Carlo gap

训练没有到达目标最优，或 finite $L/K$ 带来随机误差。它们不是 variational family 的表达限制。

常用诊断是固定 $\theta$，以 amortized $q_\phi$ 初始化每个样本的局部变分参数并继续优化：改善部分估计 amortization/optimization 问题；剩余 posterior KL 才接近 family gap，但仍需可信的 exact/高精度基准。

## 六、训练 IWAE 与用 IWAE 评价不是同一件事

- **评价**：固定 $\theta,\phi$，用大 $K$ 估计 test log likelihood；
- **训练**：对 $\mathcal L_K$ 的 $\theta,\phi$ 求梯度，改变 learned model 与 inference network。

增加 $K$ 通常让 objective 对 $\theta$ 更接近 likelihood，但 inference-network gradient 的 signal-to-noise 可能恶化；不能从 bound monotonicity 推出有限算力下训练单调改善。

## 七、一个有限离散核对

用 GEN-10 的例子，观察 $x=1$。取 proposal $q(z=1\mid x)=0.5$：

$$
w(0)=0.12/0.5=0.24,\qquad
w(1)=0.32/0.5=0.64.
$$

故 $\mathbb E_qw=0.44=p(x=1)$。$K=1$ 的 ELBO 为

$$
\tfrac12\log0.24+\tfrac12\log0.64
=\log\sqrt{0.1536}\approx-0.936,
$$

而 exact $\log0.44\approx-0.821$。若 $q$ 取 exact posterior $(3/11,8/11)$，两种 weight 都等于 $0.44$，所有 $K$ 的下界立即等于 evidence。

## 八、科学空间研读框

[[S-2021-Su-8791-VAE估计样本概率密度]]把 VAE sample density 写成 importance average，适合作为从 encoder proposal 到 evidence estimate 的入口；[[S-2015-Burda-IWAE]]定义 multi-sample bound。本节补齐 density estimator 与 log estimator 的 bias 区别、ESS、support、单次非单调性和四类 gap。

记号映射：文章若把 decoder joint 写为 $p(x\mid z)p(z)$、proposal 写为 $q(z\mid x)$，与本卷一致；若只给 $\widehat p$ 数值，本卷还要求报告 $K$、重复次数、log-sum-exp、ESS 与不确定性。

## 九、图：从 exact evidence 到有限估计的梯子

先看图回答：哪一层是确定的模型量，哪一层是期望下界，哪一层是随机实现？family gap 与 amortization gap 分别需要怎样的对照才能隔离？

![[00-知识库管理/_assets/figures/generative-models/fig-vae-iwae-gap-ladder-v1.svg|900]]

> [!figure] 图 50.2-05　evidence、IWAE bound、随机估计与推断缺口
> 左侧按模型量—期望目标—有限样本实现分层；右侧把 approximation、amortization、optimization/MC gap 画成不同实验对照。来源：依据 IWAE 与 amortized variational inference 定义独立绘制。

**怎样读图**：不要把所有竖直距离都叫 ELBO gap。先固定 $\theta$，再明确比较的是 exact posterior、family-optimal $q_x^*$、amortized $q_\phi$ 还是一次 Monte Carlo 估计。

**图没有证明什么**：图不证明增大 $K$ 总能改善训练，也不证明 ESS 是 posterior accuracy 的充分指标；它建立需要测量的对象。

## 十、本节回顾

- $\widehat p_K$ 对 density 无偏，$\log\widehat p_K$ 对 log evidence 通常向下偏；
- $\mathcal L_K$ 是随 $K$ 收紧的期望下界，单次估计不保证单调；
- ESS 暴露 weight degeneracy，但不是全部质量诊断；
- model、family、amortization、optimization/MC gap 需要不同对照；
- IWAE 训练与大 $K$ likelihood 评价是两种用途。

## 十一、练习与独立详解

- [[习题 - IWAE、重要性权重与推断缺口]]
- [[解答 - IWAE、重要性权重与推断缺口]]
