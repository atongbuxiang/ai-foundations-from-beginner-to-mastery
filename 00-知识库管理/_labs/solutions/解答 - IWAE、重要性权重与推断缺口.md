---
type: solution
status: draft
area: [generative-models, vae, importance-sampling]
topic: "[[IWAE、重要性权重与推断缺口]]"
exercise: "[[习题 - IWAE、重要性权重与推断缺口]]"
created: 2026-08-25
updated: 2026-08-25
---

# 解答 - IWAE、重要性权重与推断缺口

## A. 识别与复述

### GEN13-A01
$w(z)=p_\theta(x,z)/q_\phi(z\mid x)$；
$$
\widehat p_K=K^{-1}\sum_kw_k,\qquad
\mathcal L_K=E\log\widehat p_K.
$$
在 proposal 覆盖 joint support 时 $E\widehat p_K=p_\theta(x)$，而 $\mathcal L_K\le\log p_\theta(x)$。

### GEN13-A02
$\log$ 是严格凹函数，故
$$
E\log\widehat p_K\le\log E\widehat p_K=\log p(x).
$$
只有 estimator 几乎处处常数才取等。非线性变换通常不保无偏性。

### GEN13-A03
Model gap 是模型族与数据差；family gap 是最佳 $q\in\mathcal Q$ 与真 posterior 的差；amortization gap 是共享 encoder 与每样本 family-optimal $q_x^*$ 的差；optimization/MC gap 来自未收敛和有限随机估计。

## B. 手算与建模

### GEN13-B01
均值为 $\widehat p_4=.5$，log estimate 为 $\log.5\approx-.6931$。$\sum w=2,\sum w^2=1.30$，所以
$$
ESS=4/1.3\approx3.0769.
$$

### GEN13-B02
Evidence 为 $.15+.35=.5$。weights 为 $.15/.5=.3$ 与 $.35/.5=.7$。$K=1$ ELBO
$$
\tfrac12\log.3+\tfrac12\log.7
=\tfrac12\log.21\approx-.7803,
$$
低于 $\log.5\approx-.6931$。

### GEN13-B03
delta-method bias 约
$$
-\frac{.01}{2(100)(.2)^2}=-.00125.
$$
这是 log 单位的近似期望偏差，不是一次估计的误差界。

## C. 推导与证明

### GEN13-C01
线性期望给
$$
E\widehat p_K=K^{-1}\sum_kE_q[p(x,Z_k)/q(Z_k\mid x)]=p(x).
$$
再由 Jensen，
$$
\mathcal L_K=E\log\widehat p_K\le\log E\widehat p_K=\log p(x).
$$

### GEN13-C02
若 $q(z\mid x)=p(z\mid x)=p(x,z)/p(x)$，则
$$
w(z)=\frac{p(x,z)}{p(x,z)/p(x)}=p(x)
$$
在 posterior support 上为常数。因此任意 $K$ 的平均和 log 都精确。

### GEN13-C03
Posterior expectation 是
$$
E_{p(z\mid x)}f(z)=
\frac{E_q[w(Z)f(Z)]}{E_qw(Z)}.
$$
用样本均值比值得 $\sum_k\widetilde w_kf(z_k)$。分子、分母各自无偏不使比值无偏；由大数定律两者分别收敛，只要分母非零且矩条件成立，比值连续映射下一致。

## D. 边界、反例与纠错

### GEN13-D01
第一次抽到 $w_1=10$，则 $\widehat p_1=10$；第二次抽到 $w_2=.001$，$\widehat p_2=5.0005<10$，故 log 下降。理论单调性针对不同 $K$ 的期望 $\mathcal L_K$，不是嵌套样本的每条轨迹。

### GEN13-D02
固定计算预算时，大 $K$ 意味更少 batch/updates；对 inference network 的 gradient signal-to-noise 也可能下降。更紧是 objective expectation 的性质，不包含 optimizer、variance、wall-clock 与 model selection。

### GEN13-D03
真 posterior 有两模式，质量 $.9,.1$；proposal 是只覆盖第一模式的 posterior 条件分布。所有已采样权重可几乎相等，ESS 接近 $K$，但第二模式永不出现。ESS 只诊断 proposal 内的权重退化，不能发现 support 漏失。

## E. AI 迁移

### GEN13-E01
报告模型 checkpoint、test preprocess、proposal、$K$、batching、重复 seed、log-sum-exp、float dtype、per-example ESS/weight CV、均值/中位数、bootstrap CI 和失败率。区分 $\widehat p_K$、$\log\widehat p_K$ 与跨重复平均。

### GEN13-E02
冻结 $\theta$ 与 encoder architecture。以 $q_\phi(x)$ 参数初始化，对每个 test $x$ 单独优化 variational parameters，使用独立验证估计停止；局部 ELBO 改善估计 amortization+未收敛部分。再用更强 family 区分 family gap，并用大 $K$ 降 MC error。

### GEN13-E03
做同 $\theta$ 容量与总参数预算、仅换 encoder family 的对照；再做 decoder/model 参数重分配对照。报告 ELBO、large-$K$ likelihood、local-refinement gap、prior sample metrics 与 wall-clock，多 seed。只有 likelihood 的变化才能支持模型分布改善，而非只支持 bound 变紧。

