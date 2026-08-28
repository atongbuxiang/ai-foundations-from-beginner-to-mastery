---
type: solution
status: draft
area: [learning-theory/ensembles, random-forests, boosting]
topic: "[[Bagging、Random Forest 与 Boosting]]"
exercise: "[[习题 - Bagging、Random Forest 与 Boosting]]"
prerequisites: ["[[Bagging、Random Forest 与 Boosting]]"]
related: ["[[决策树、分裂准则与剪枝]]", "[[在线学习、Boosting 与序列预测 MOC]]"]
created: 2026-08-23
updated: 2026-08-28
---

# 解答 - Bagging、Random Forest 与 Boosting

> [!warning] 解题原则
> “更多模型”不是独立信息的同义词。分析 ensemble 时要分清训练集随机性、algorithm/bootstrap随机性、成员相关性、序列依赖和 selection reuse；再判断极限 \(B\to\infty\) 究竟消除了哪一种误差。

## A. 识别与复述

### LT-ENS-A01

给定 realized dataset \(S\)，设 \(\Theta\) 表示 bootstrap、feature subsampling等 algorithmic randomness。

- **ideal bagged predictor**：
  $$
  f_{\mathrm{bag}}(x;S)=E_\Theta[f(x;S,\Theta)\mid S];
  $$
- **finite-\(B\) bagging**：
  $$
  \widehat f_B(x;S)=\frac1B\sum_{b=1}^Bf(x;S,\Theta_b);
  $$
- **infinite random forest**：给定 \(S\) 与规定的 tree-randomization law，对随机树预测取 conditional expectation；
- **repeated-dataset expectation**：再对 \(S\sim P^n\) 取 expectation，研究 sampling behavior。

增加 \(B\) 只让 finite ensemble更接近给定 \(S\) 下的 algorithmic expectation，conditional Monte Carlo variance通常按 \(1/B\) 下降。它不增加独立 observations，不消除 \(S\) 导致的 bias/variance，也不修复 distribution shift。

### LT-ENS-A02

| 方法 | member怎样产生 | 并行性 | aggregation | 直接优化对象 |
|---|---|---:|---|---|
| bagging | bootstrap/resampled data上独立拟合 base learner | 高 | 平均/投票 | 每个成员各自的训练 loss；整体通常无单一 stagewise loss |
| random forest | bootstrap或subsample，加 node-level random feature candidates | 高 | 平均/投票 | randomized tree induction |
| AdaBoost | 按前轮错误更新 sample weights，再拟合 weak learner | 低 | \(\operatorname{sign}\sum_m\alpha_m h_m\) | stagewise exponential loss |
| gradient boosting | 对当前 ensemble 的 negative functional gradient/pseudo-residual拟合新 learner | 低 | additive sum | chosen differentiable empirical loss 的 stagewise下降 |

bagging/forest主要通过随机化与平均处理不稳定 learners；boosting是依赖前一状态的 sequential function-space optimization。

### LT-ENS-A03

对 observation \(i\)，OOB prediction只聚合那些 bootstrap sample未包含 \(i\) 的 trees，因此 \(y_i\) 没有直接参与这些 trees 的拟合，避免普通 resubstitution prediction。

但整份 OOB record仍来自同一个 dataset。若反复用它选择 features、depth、tree count、calibration、threshold或 model family，选择过程会适配 OOB noise；相关 users/time groups也可能在 in-bag trees中泄漏。故 OOB适合 efficient internal estimation/diagnostics，不是可无限查询的 independent final test。

## B. 手算与数值判断

### LT-ENS-B01

某 observation 在一次 draw中未被抽中的概率为 \(99/100\)，100次有放回抽样都未抽中：

$$
\left(\frac{99}{100}\right)^{100}
=0.99^{100}
\approx\boxed{0.366032}.
$$

所以被至少抽中一次的概率为

$$
\boxed{1-0.366032=0.633968}.
$$

当 \(n\to\infty\)，

$$
\left(1-\frac1n\right)^n\to e^{-1}\approx0.367879,
$$

与 \(n=100\) 的 0.366032 已很接近。注意 63.2% 是 expected unique inclusion proportion，不是每个 bootstrap sample恰好含 63.2 个 unique rows。

### LT-ENS-B02

exchangeable members 的 ensemble variance：

$$
\operatorname{Var}(\bar f_B)
=v\left[\rho+\frac{1-\rho}{B}\right].
$$

代入 \(v=16,\rho=0.2,B=25\)：

$$
16\left(0.2+\frac{0.8}{25}\right)
=16(0.232)
=\boxed{3.712}.
$$

当 \(B\to\infty\)：

$$
\boxed{\operatorname{Var}(\bar f_\infty)=16\times0.2=3.2}.
$$

剩余 floor 来自 member covariance；树再多也不能靠平均消掉共同波动。

### LT-ENS-B03

AdaBoost coefficient：

$$
\alpha
=\frac12\log\frac{1-\varepsilon}{\varepsilon}
=\frac12\log4
=\boxed{\log2\approx0.693147}.
$$

normalizer：

$$
Z=2\sqrt{\varepsilon(1-\varepsilon)}
=2\sqrt{0.2\cdot0.8}
=\boxed{0.8}.
$$

更新 \(w_i'\propto w_i\exp[-\alpha y_i h(x_i)]\)。所以分类正确时乘

$$
e^{-\alpha}=1/2,
$$

分类错误时乘

$$
e^{\alpha}=2,
$$

然后整体除以 \(Z\) 归一化。

## C. 推导与证明

### LT-ENS-C01

记 finite bagged prediction 为 \(\widehat f_B(S,\Theta_{1:B})\)。对 dataset randomness 与 algorithmic randomness应用 total variance：

$$
\operatorname{Var}(\widehat f_B)
=\operatorname{Var}_S\!\left(
E_\Theta[\widehat f_B\mid S]
\right)
+E_S\!\left[
\operatorname{Var}_\Theta(\widehat f_B\mid S)
\right].
$$

第一项是 ideal bagged procedure随训练集变化的 sampling variance；第二项是给定 \(S\) 后只因有限 random members产生的 Monte Carlo variance。

若条件于 \(S\)，members \(f_b(x)\) iid、variance 为 \(v_S(x)\)，则

$$
\operatorname{Var}_\Theta\left(
\frac1B\sum_{b=1}^B f_b(x)\middle|S
\right)
=\frac1{B^2}\sum_{b=1}^Bv_S(x)
=\boxed{\frac{v_S(x)}B}.
$$

因此 \(B\to\infty\) 只消去第二项；第一项、bias与irreducible noise仍在。

### LT-ENS-C02

设每个 member variance为 \(v\)，任意不同 members的 correlation为 \(\rho\)，于是 covariance为 \(\rho v\)。则

$$
\begin{aligned}
\operatorname{Var}(\bar f_B)
&=\operatorname{Var}\left(\frac1B\sum_{b=1}^Bf_b\right)\\
&=\frac1{B^2}\left[
Bv+B(B-1)\rho v
\right]\\
&=\boxed{v\left[\rho+\frac{1-\rho}{B}\right]}.
\end{aligned}
$$

independent component随 \(1/B\) 消失，而共同 component趋于 \(\rho v\)。random forest 的 feature subsampling试图降低成员相关性，但过强随机化也可能削弱单棵树；因此要在 strength 与 correlation之间权衡。

### LT-ENS-C03

令当前 additive score 为 \(F_{m-1}(x)\)，新 weak classifier \(h_m\in\{-1,+1\}\)。AdaBoost选择 \(\alpha\) 以最小化

$$
\sum_i\exp[-y_i(F_{m-1}(x_i)+\alpha h_m(x_i))].
$$

定义 normalized current weights

$$
w_i^{(m)}
=\frac{\exp[-y_iF_{m-1}(x_i)]}
{\sum_j\exp[-y_jF_{m-1}(x_j)]},
$$

weighted error \(\varepsilon_m=\sum_{i:y_i\ne h_m(x_i)}w_i^{(m)}\)。忽略与 \(\alpha\) 无关的因子，stage objective为

$$
Z_m(\alpha)
=(1-\varepsilon_m)e^{-\alpha}
+\varepsilon_m e^{\alpha}.
$$

令导数为零：

$$
-(1-\varepsilon_m)e^{-\alpha}
+\varepsilon_m e^{\alpha}=0,
$$

得到

$$
\boxed{
\alpha_m=\frac12\log\frac{1-\varepsilon_m}{\varepsilon_m}
}.
$$

代回得

$$
\boxed{Z_m=2\sqrt{\varepsilon_m(1-\varepsilon_m)}}.
$$

weight update为

$$
w_i^{(m+1)}
=\frac{w_i^{(m)}e^{-\alpha_m y_i h_m(x_i)}}{Z_m}.
$$

从 \(F_0=0,w_i^{(1)}=1/n\) 递推：

$$
\frac1n\sum_i e^{-y_iF_M(x_i)}
=\prod_{m=1}^M Z_m.
$$

又因为 \(\mathbf 1\{y_iF_M(x_i)\le0\}\le e^{-y_iF_M(x_i)}\)，所以

$$
\boxed{
\widehat R_{01}(F_M)
\le \frac1n\sum_i e^{-y_iF_M(x_i)}
=\prod_m Z_m
}.
$$

这是 training bound，不是 distribution-free test guarantee；generalization仍需 capacity/margin/selection分析。

## D. 边界、反例与纠错

### LT-ENS-D01

bootstrap只从 empirical distribution

$$
\widehat P_n=\frac1n\sum_{i=1}^n\delta_{Z_i}
$$

重复抽样。它重新加权已观察到的 \(n\) 个 atoms，没有观察任何新 label、user或environment。一个 size-\(n\) bootstrap sample平均只含约

$$
n(1-e^{-1})\approx0.632n
$$

个 unique observations，其余是 duplicates。它的价值是模拟 estimator 对 empirical perturbations的响应、随机化 unstable learner并进行 uncertainty approximation，不是制造独立训练信息。

### LT-ENS-D02

给定 dataset \(S\)，树数趋于无穷只使 forest收敛到

$$
f_\infty(x;S)=E_\Theta[T(x;S,\Theta)\mid S].
$$

这是 conditional algorithmic average，不是 Bayes predictor。其 error仍可能来自：

- tree/feature representation bias；
- finite \(S\) 的 sampling uncertainty；
- labels中的 irreducible noise；
- member correlation导致的 variance floor；
- hyperparameter/feature selection reuse；
- covariate、label或concept shift。

因此增加 trees通常先降低 Monte Carlo noise，随后 prediction趋于稳定平台；平台不必为零，test error甚至会因不当 selection或 shift很高。

### LT-ENS-D03

“bagging只降 variance、boosting只降 bias”至多是粗略倾向。反例机制包括：

1. bagging averaging nonlinear/unstable learners会平滑 decision boundary，既可能降低也可能引入 bias；
2. bootstrap有效训练分布和 duplicate weights改变了 base learner target；
3. random feature subsampling既降 correlation/variance，也可能削弱 strong-feature access并增加 bias；
4. boosting继续加深/加轮数可降低 approximation bias，也会增加 sensitivity/variance；
5. shrinkage、row/column subsampling与early stopping可同时改变 bias与variance；
6. exponential、logistic、ranking等 loss选择改变的不是单纯 bias，而是 surrogate target与错误权重；
7. label noise下 AdaBoost 强调难例，可能放大 variance并改变 boundary；
8. post-hoc calibration改变 probability predictions与 proper-score behavior。

必须针对 fixed data-generating process、loss与完整 tuning procedure分析，而不是给 algorithm贴永久标签。

## E. AI 迁移

### LT-ENS-E01

普通 row bootstrap/OOB会让同一 user 的其他记录进入某棵树的 in-bag sample，也可能让未来记录帮助预测过去，导致 identity与temporal leakage。可采用：

1. 最外层按 user group 划分，并以时间向前的 test window验收；
2. outer-train 内按 user/block bootstrap，而非独立 row bootstrap；
3. OOB只把整个未抽中的 user/block视为 OOB；
4. tuning、feature engineering、threshold与calibration在 inner grouped/time-respecting folds完成；
5. final outer test保持 untouched，并分别报告新用户、已知用户未来期与 shift subgroup。

若 production目标是“已知用户下一时刻”，split unit与estimand应明确反映它；不能把更容易的新旧记录混合任务当作同一评估。

### LT-ENS-E02

一个 gradient-boosted reward-model protocol：

- **target/loss**：对同一 prompt 的 chosen–rejected pairs 使用 pairwise logistic loss，并记录 ties/annotator uncertainty；
- **sampling**：prompt为 group，pair权重避免一个 prompt产生大量 pairs 后支配 objective；
- **capacity**：限制 depth/min leaf，使用 learning-rate shrinkage、row/feature subsampling与 regularization；
- **selection**：在 prompt-grouped validation上 early stopping，所有 candidate rounds共享预先定义的 selection rule；
- **calibration**：在独立 calibration fold上检查 pairwise probability、Brier/log loss和 subgroup reliability；
- **test**：untouched prompts、time split、source/domain split，并检查近重复与 annotator泄漏；
- **policy shift**：在新 policy/challenge set上检查 reward hacking、length/style shortcut、OOD ranking和 uncertainty；
- **deployment**：报告 latency、missing features、monitoring与 rollback threshold。

offline ranking好不等于 policy optimization后仍有效，因为新 policy 会主动寻找 reward model 的 extrapolation漏洞。

### LT-ENS-E03

生产 ensemble 报告至少应包含：

- randomness来源：bootstrap、row/feature subsampling、seed与 nondeterministic implementation；
- tree/round count convergence：prediction、proper score、latency随成员数的曲线；
- member error/correlation或 diversity diagnostics，以及 random forest 的 strength–correlation tradeoff；
- OOB被用于哪些 tuning/importance/calibration决策，final test是否独立；
- accuracy/AUC之外的 log loss、Brier、calibration、threshold-specific utility与 subgroup指标；
- impurity/permutation/conditional importance及跨 seeds/time的 stability；
- depth、memory、batch/online latency、energy/cost与 fallback；
- data/schema/prevalence/concept shift监控和重训触发；
- training/validation/test的 user、time、document group contract；
- reproducible hyperparameters、code/data version与 uncertainty intervals。

只有把 estimator、selection procedure与 deployment distribution一并记录，ensemble表现才可复核。
