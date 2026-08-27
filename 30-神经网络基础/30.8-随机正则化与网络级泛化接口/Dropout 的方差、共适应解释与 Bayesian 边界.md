---
type: framework
status: draft
area: [neural-networks/regularization, dropout, variance, bayesian-boundary, uncertainty]
aliases: [Dropout Evidence Boundaries, MC Dropout Boundary]
node_id: NN-58
prerequisites: ["[[Dropout 的随机掩码、期望与 Inverted Scaling]]", "[[期望、方差与矩]]", "[[变分推断、ELBO 与证据分解]]", "[[Bayesian Posterior Predictive、Ensemble 与近似边界]]"]
related: ["[[容量界、稳定性界与 PAC-Bayes 的比较]]", "[[概率校准、Proper Scoring Rule 与可靠性图]]", "[[遮蔽预测、Teacher–Student 与自监督目标]]", "[[DropConnect、权重噪声与激活噪声]]"]
sources: ["[[S-2014-Srivastava-Dropout]]", "[[S-2013-Wager-Dropout-Adaptive-Regularization]]", "[[S-2016-Gal-Ghahramani-MC-Dropout]]", "[[S-2015-Kingma-Variational-Dropout]]", "[[S-2021-Su-8770-Dropout-MLM-MAE]]"]
exercises: ["[[习题 - Dropout 的方差、共适应解释与 Bayesian 边界]]"]
solutions: ["[[解答 - Dropout 的方差、共适应解释与 Bayesian 边界]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-dropout-variance-evidence-boundaries-v2.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# Dropout 的方差、共适应解释与 Bayesian 边界

> [!abstract] 本章主问题
> Dropout 有多种互补解释：它给 activations 注入异方差乘性噪声；在某些线性/广义线性问题中，expected noisy risk 可化成数据依赖正则项；在指定 prior、variational family、likelihood 与训练目标下，又可与近似 Bayesian inference 建立联系。“减少共适应”和“隐式集成”是有用直觉，但不是无需条件的数学定理。必须标明自己站在哪一层证据上。

## 一、学习目标

读完本节，你应能：

1. 推导随机输入经过 Dropout 后的无条件方差；
2. 推导线性 score 的条件方差与 score 间 covariance；
3. 在线性平方损失下精确分解 expected noisy risk；
4. 区分精确代数、局部近似、机制假说和经验结果；
5. 解释“减少共适应”为何不是可直接检验的单一定理；
6. 区分 deterministic evaluation、子网络 ensemble 与 MC Dropout；
7. 写出 MC predictive mean、variance 与 entropy/MI proxy；
8. 说明 Monte Carlo error、variational bias、model misspecification 与 calibration error 的不同来源；
9. 设计不确定性和正则化机制的公平验收。

## 二、从固定输入推广到随机输入

上一节条件于固定 $x$ 推导了

$$
Y=\frac MqX,
\qquad
M\sim\operatorname{Bernoulli}(q).
$$

现在令 $X$ 本身是随机变量，且与 $M$ 独立：

$$
\mathbb E[X]=\mu,
\qquad
\operatorname{Var}(X)=\sigma^2.
$$

一阶矩：

$$
\mathbb E[Y]
=\frac1q\mathbb E[M]\mathbb E[X]
=\mu.
$$

二阶矩：

$$
\mathbb E[Y^2]
=\frac1{q^2}\mathbb E[M^2]\mathbb E[X^2]
=\frac1q(\sigma^2+\mu^2).
$$

所以

$$
\operatorname{Var}(Y)
=\frac{\sigma^2+\mu^2}{q}-\mu^2
$$

$$
\boxed{
\operatorname{Var}(Y)
=\frac{\sigma^2+p\mu^2}{q}
}.
$$

方差包含两部分：原数据 variation 被放大为 $\sigma^2/q$，非零均值又引入 $p\mu^2/q$ 的 mask variation。只在 $p=0$ 时恢复原方差。

## 三、线性 Score 的条件方差

固定向量 $x\in\mathbb R^d$，逐 feature 独立 masks：

$$
\widetilde x_i=\frac{m_i}{q}x_i.
$$

线性 score

$$
u=w^\mathsf T\widetilde x
=\sum_{i=1}^dw_i\frac{m_i}{q}x_i.
$$

条件均值为

$$
\mathbb E[u\mid x]=w^\mathsf Tx.
$$

独立 masks 让交叉 covariance 为零，因此

$$
\boxed{
\operatorname{Var}(u\mid x)
=\frac pq\sum_{i=1}^dw_i^2x_i^2
}.
$$

它不是各向同性的 $\sigma^2\|w\|^2$；噪声强度随 $x_i^2$ 改变，所以 Dropout 是 input-dependent、multiplicative、heteroscedastic noise。

## 四、多个 Scores 之间会相关

令另一 score

$$
v=a^\mathsf T\widetilde x.
$$

它与 $u$ 共享同一 feature masks，于是

$$
\boxed{
\operatorname{Cov}(u,v\mid x)
=\frac pq\sum_iw_i a_i x_i^2
}.
$$

即便每个 $m_i$ 独立，不同输出 units 也会因为共同读取同一个 masked input 而相关。若每个 output–input connection 使用独立 mask，边际方差可相同，cross-output covariance 却会改变；这正是下一节 DropConnect 比较的核心。

## 五、精确例子：平方损失中的自适应二次正则

考虑线性预测

$$
\widehat t=w^\mathsf T\widetilde x
$$

和平方损失

$$
\ell=(t-\widehat t)^2.
$$

用 bias–variance 恒等式：

$$
\mathbb E_m[(t-w^\mathsf T\widetilde x)^2]
=\left(t-\mathbb E_m[w^\mathsf T\widetilde x]\right)^2
+\operatorname{Var}_m(w^\mathsf T\widetilde x).
$$

代入前面的均值和方差：

$$
\boxed{
\mathbb E_m\ell
=(t-w^\mathsf Tx)^2
+\frac pq\sum_iw_i^2x_i^2
}.
$$

对数据集 $\{(x_n,t_n)\}_{n=1}^N$ 求和，附加项为

$$
\frac pq\sum_iw_i^2\sum_nx_{ni}^2.
$$

它像 feature-scale-dependent $L_2$，而不是统一系数的 ordinary weight decay。若某 feature 平方幅度更大，对应 weight penalty 更强。

> [!important] 这是哪里精确
> 上式在线性 predictor、独立 Bernoulli feature masks 和平方损失下精确。对 logistic GLM 可得到局部/Fisher-scaled 联系；对深层 ReLU/Transformer，mask 会改变激活区、attention、normalization 与优化轨迹，不能宣布“Dropout 就等于某个固定 $L_2$”。

## 六、小噪声展开的统一视角

把 corrupted object 写成

$$
u+\varepsilon,
\qquad
\mathbb E[\varepsilon]=0,
\qquad
\operatorname{Cov}(\varepsilon)=\Sigma.
$$

若 loss 对 $u$ 二阶可微，在小噪声下

$$
\mathbb E[\ell(u+\varepsilon)]
\approx
\ell(u)
+\frac12\operatorname{tr}
\left(
\nabla_u^2\ell(u)\Sigma
\right).
$$

这说明诱导 penalty 同时依赖：

- 噪声 covariance $\Sigma$；
- loss/网络对被扰动对象的 curvature；
- 扰动位置；
- 展开点和数据分布。

若高阶项不可忽略、Hessian 不稳定或 mask 是大幅离散跳变，二阶式只是局部近似。

## 七、“减少共适应”是什么证据

原始 Dropout 论文用“阻止 units 过度 co-adapt”解释其作用。这个直觉提示：若 feature 总依赖少数同伴同时存在，随机删除同伴会迫使它在更多上下文中有用。

但“共适应”没有唯一操作定义。候选指标包括：

- activations 的 covariance/correlation；
- feature ablation 后的性能下降；
- 单元对 mask pattern 的敏感度；
- representation redundancy/effective rank；
- conditional mutual information；
- 单元组合的可替代性。

这些指标不等价。相关性下降可能只是方差/尺度变化；冗余上升也可能提高鲁棒性。因此正确表述是机制假说：

> 在指定架构、mask placement 和任务上，Dropout 可能通过降低对特定 feature conjunction 的依赖改善 held-out risk。

要支持它，需要预注册指标、无 Dropout 对照、matched capacity/compute、rate sweep 与干预实验，而不是只看最终 accuracy。

## 八、“指数多个子网络集成”为什么只是近似叙述

每个 mask realization $m$ 定义一个共享参数的 thinned function

$$
f_{\theta,m}(x).
$$

mask 数量可呈指数增长，但它们：

- 共享同一组参数；
- 不是独立训练的 ensemble members；
- 训练时通过随机梯度共同耦合；
- 权重并非每个子网分别达到其最优；
- deterministic evaluation 一般不等于
  $\mathbb E_m[f_{\theta,m}(x)]$。

仿射层的 preactivation 均值可精确匹配，特殊正齐次结构也可能保持某些关系；一般深网含 bias、normalization、attention 和多个 nonlinearities，不可把局部匹配外推到整个 predictor。

## 九、MC Dropout 到底计算什么

MC Dropout 在 evaluation 数据上保留 Dropout 随机性，采样

$$
m^{(1)},\ldots,m^{(S)},
$$

得到 predictive distributions

$$
p_s(y\mid x)=p(y\mid x,\theta,m^{(s)}).
$$

Monte Carlo predictive mean 为

$$
\boxed{
\bar p(y\mid x)
=\frac1S\sum_{s=1}^Sp_s(y\mid x)
}.
$$

对标量回归输出 $f_s$：

$$
\widehat\mu=\frac1S\sum_sf_s,
$$

$$
\widehat v_{\rm model}
=\frac1{S-1}\sum_s(f_s-\widehat\mu)^2.
$$

若 observation model 还含噪声方差 $\sigma_{\rm obs}^2$，predictive variance 账中要另加它；mask variation 不能自动等同全部 aleatoric/epistemic uncertainty。

## 十、分类中的 Entropy 与 MI Proxy

分类时常报告 predictive entropy：

$$
H[\bar p]
=-\sum_c\bar p_c\log\bar p_c.
$$

以及

$$
\widehat I
=H[\bar p]
-\frac1S\sum_{s=1}^SH[p_s].
$$

后者衡量 sampled predictors 之间的分歧，在指定近似 Bayesian 解释下可作为 mutual-information estimator。脱离该解释，它仍是一个 ensemble-disagreement statistic，但不能自动叫作“真实 epistemic uncertainty”。

## 十一、Bayesian 解释需要哪些条件

Gal–Ghahramani 路线把特定 Dropout network、weight decay、likelihood 和 variational objective 联系到受限 posterior approximation。要做 Bayesian claim，至少声明：

1. prior 是什么；
2. variational family 如何由 masks/weights 参数化；
3. 优化目标是否对应所称 ELBO/近似；
4. weight decay、drop rate、likelihood precision 怎样映射；
5. test-time samples 是否来自训练所定义的 approximate posterior；
6. predictive likelihood 是否包含 observation noise；
7. calibration/OOD 指标是否独立验证。

仅仅“evaluation 时多开几次 Dropout”只能证明采到了一个随机 predictor family，不能证明采自精确 posterior。

## 十二、四类误差不要混账

### 12.1 Monte Carlo Error

有限 $S$ 导致 sample mean 误差；在独立有限方差下典型尺度是

$$
O(S^{-1/2}).
$$

增加样本可降低它。

### 12.2 Variational Approximation Bias

posterior family 受限或 objective 近似导致。增加 $S$ 只更精确积分这个近似分布，不能消除 family bias。

### 12.3 Model Misspecification

likelihood、architecture、data assumptions 错误。即使精确 posterior 也可能给出错误/过度自信预测。

### 12.4 Evaluation/Calibration Error

有限 held-out sample、adaptive tuning、distribution shift 与指标选择造成。它需要独立数据和置信区间。

“MC curves 已收敛”只支持第一项足够小，不支持其余三项消失。

## 十三、实现边界：不要把整个模型切回 Train

为了 MC Dropout，粗暴调用整个模型 `train()` 可能同时：

- 让 BatchNorm 使用 batch statistics；
- 更新 running buffers；
- 打开其他随机模块；
- 改变缓存、量化或路由行为。

正确协议通常是保持模型其余部分 evaluation，仅选择性开启 Dropout modules，并验证 buffer 不变。对 LayerNorm 虽无 running state，也仍需检查其他随机层。

## 十四、公平验收协议

### Regularization 轨道

固定数据、有效训练 token、architecture、optimizer family、调参预算与增强；比较 no-dropout、不同 $p$/placement/granularity。报告：

- train/validation/test NLL 与 gap；
- calibration、rare/group metrics；
- 收敛步数与 wall time；
- activation/update norms；
- 预注册 co-adaptation proxies；
- 多 seed 与置信区间。

### Uncertainty 轨道

与 deterministic、deep ensemble、其他 approximate inference 比较：

- proper scoring rules：NLL/Brier；
- calibration：reliability/ECE 及区间；
- selective risk/coverage；
- OOD benchmark 的明确 shift family；
- $S$–quality–latency 曲线；
- MC、approximation 与数据误差分账。

不能用同一个 validation set 同时选 rate、temperature、sample count 和报告最终 calibration 而不校正 selection bias。

## 十五、常见误区

1. **“Dropout 方差只等于 $p/q$”**：还乘输入/权重尺度；
2. **“共适应已被严格定义并证明减少”**：它通常是机制解释；
3. **“Dropout 就是 ordinary $L_2$”**：精确 penalty 依数据和问题；
4. **“deterministic eval 是精确 ensemble mean”**：非线性一般否定；
5. **“MC variance 就是真实 epistemic uncertainty”**：需要 posterior/model 条件；
6. **“增加 MC samples 可修复 posterior bias”**：只能降低积分误差；
7. **“MC Dropout 应把全模型设为 train”**：会混入 BatchNorm 等状态变化；
8. **“不确定性高就一定检测 OOD”**：仍需明确 shift 与实证。

## 十六、图：三层证据不能越级

先看图回答：随机输入方差为什么多出 $p\mu^2/q$？平方损失下哪一步使 penalty 成为精确等式？右栏为什么把 stochastic predictor、MC moments、variational family 与 calibrated posterior 分成四级？

![[00-知识库管理/_assets/figures/neural-networks/fig-dropout-variance-evidence-boundaries-v2.svg|900]]

> [!figure] 图 30.8-02　Dropout 的方差账、平方损失 penalty 与 Bayesian 证据阶梯
> 左栏从随机输入 moments 推到线性 score variance；中栏给出平方线性模型的 exact expected-risk decomposition；右栏把“有随机预测器”到“校准的 posterior claim”拆成逐级增加的证明义务。来源：依据 Srivastava et al.、Wager et al.、Gal–Ghahramani、Kingma et al. 与本节独立推导绘制；由 [[00-知识库管理/_labs/code/plot_random_regularization_foundations_v2.py]] 确定性生成。

**怎样读图**：先判断公式属于 moment、expected risk 还是 posterior 层；再核对精确等式的模型/损失条件；最后检查 MC sample 增加实际减少的是哪一项误差。

**图没有证明什么**：图不证明 Dropout posterior 已校准，不证明共适应是唯一作用机制，也不证明线性平方损失的 penalty 形式在任意深网中保持精确。

## 十七、最小验收

1. 推导 $\operatorname{Var}(Y)=(\sigma^2+p\mu^2)/q$；
2. 推导线性 score variance 与两 score covariance；
3. 重建平方损失 expected-risk 分解；
4. 说明 GLM/深网外推边界；
5. 把共适应转化为可检验但不唯一的指标；
6. 区分 deterministic eval、共享参数子网与 MC mixture；
7. 写出 MC mean、variance、entropy 与 MI proxy；
8. 分开四类误差；
9. 解释 selective Dropout eval 的状态要求；
10. 设计 regularization/uncertainty 两条公平验收轨道。

> [!summary]
> Dropout 的基础事实是异方差乘性噪声；在线性平方损失中，它精确诱导 feature-weighted quadratic penalty，在更一般模型中通常只能得到条件化近似或经验机制。MC Dropout 可以积分一个指定随机 predictor family，但更多 samples 只降低 Monte Carlo error，不会自动修复 variational bias、model misspecification 或 calibration。任何“共适应、集成、Bayesian”解释都必须附上对象、假设与证据等级。

- [[随机正则化与网络级泛化接口 MOC]]
- [[习题 - Dropout 的方差、共适应解释与 Bayesian 边界]]
- [[解答 - Dropout 的方差、共适应解释与 Bayesian 边界]]
