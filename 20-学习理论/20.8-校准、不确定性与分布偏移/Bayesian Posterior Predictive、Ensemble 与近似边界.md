---
type: theorem
status: draft
area: [learning-theory/posterior-predictive, ensembles, bayesian-deep-learning]
aliases: [Posterior Predictive Distribution, Deep Ensemble, Approximate Bayesian Prediction]
node_id: LT-63
prerequisites: ["[[Bayesian 推断与后验预测]]", "[[Monte Carlo、重要性采样与方差缩减]]", "[[Aleatoric、Epistemic 与模型不确定性]]", "[[Bagging、Random Forest 与 Boosting]]"]
related: ["[[概率校准、Proper Scoring Rule 与可靠性图]]", "[[Conformal Prediction 与有限样本 Coverage]]", "[[模型可辨识性、选择与 Misspecification]]", "[[OOD、鲁棒性与因果不变性的边界]]"]
sources: ["[[S-2016-Gal-Ghahramani-MC-Dropout]]", "[[S-2017-Lakshminarayanan-Deep-Ensembles]]", "[[S-2019-Maddox-SWAG]]", "[[S-2019-Ovadia-Uncertainty-Shift]]", "[[S-2023-Wimmer-Aleatoric-Epistemic]]"]
exercises: ["[[习题 - Bayesian Posterior Predictive、Ensemble 与近似边界]]"]
solutions: ["[[解答 - Bayesian Posterior Predictive、Ensemble 与近似边界]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-posterior-ensemble-approx-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# Bayesian Posterior Predictive、Ensemble 与近似边界

> [!abstract] 本章主问题
> posterior predictive 是“先按 posterior 对模型加权，再对未来结果积分”的明确概率对象；MC dropout、SWAG 与 deep ensemble 是不同的计算/算法近似。把多个输出平均可以改善风险，但只有在先验、似然、posterior approximation 与成员生成机制声明后，predictive spread 才能被解释。

## 一、学习目标

完成本章后，应能：

1. 从 Bayes 公式推导 posterior predictive；
2. 区分 parameter posterior、function distribution 与 predictive distribution；
3. 推导 regression mixture 的均值与 within/between variance；
4. 说明分类为何应在 probability space 平均；
5. 推导 Monte Carlo predictive estimator 与 standard error；
6. 区分 MC error、posterior approximation error 与 model misspecification；
7. 说明 MC dropout、SWAG 和 deep ensemble 各自在近似什么；
8. 分析成员相关性、effective ensemble size 与 diminishing returns；
9. 设计 in-distribution、shift、calibration 与 compute 公平评估；
10. 写出不能从“ensemble 更好”推出的 Bayesian 声明。

## 二、Bayesian Model 的三层

给定参数 $\theta$：

$$
p(D\mid\theta)
=\prod_{i=1}^n p(y_i\mid x_i,\theta),
\qquad
p(\theta)
\text{ 为 prior}.
$$

posterior：

$$
\boxed{
p(\theta\mid D)
=
\frac{p(D\mid\theta)p(\theta)}
{\int p(D\mid\vartheta)p(\vartheta)\,d\vartheta}.
}
$$

三种对象不可混写：

1. $p(\theta\mid D)$：parameter-space uncertainty；
2. 由 $\theta\mapsto f_\theta$ 推出的 function distribution；
3. $p(y_*\mid x_*,D)$：把 observation law 也积分后的 future outcome distribution。

参数对称可能使第一层多峰，却不产生显著函数分歧。

## 三、Posterior Predictive

由全概率公式：

$$
\boxed{
p(y_*\mid x_*,D)
=
\int
p(y_*\mid x_*,\theta)
p(\theta\mid D)\,d\theta.
}
$$

它不是把 posterior mean parameter 代入：

$$
p(y_*\mid x_*,E[\Theta\mid D])
$$

一般不等于上述积分。非线性模型中“先预测再平均”和“先平均参数再预测”不可交换。

### 3.1 为什么不等

若 Bernoulli probability 为 $\sigma(\theta x)$，

$$
E_\Theta[\sigma(\Theta x)]
\ne
\sigma(E[\Theta]x)
$$

一般由非线性直接可见。posterior mean 还可能落在两个高概率 modes 之间的低密度区域。

## 四、Regression Mixture 的均值

设

$$
Y_*\mid x,\theta
\sim
\mathcal N(\mu_\theta(x),\sigma_\theta^2(x)).
$$

posterior predictive mixture mean：

$$
\boxed{
\bar\mu(x)
=E_{\theta\mid D}[\mu_\theta(x)].
}
$$

若有 $M$ 个样本 $\theta_m$：

$$
\widehat\mu_M(x)
=
\frac1M\sum_{m=1}^M\mu_m(x).
$$

## 五、Regression Mixture 的总方差

全方差公式：

$$
\operatorname{Var}(Y_*\mid x,D)
=E[\sigma_\Theta^2(x)]
+\operatorname{Var}(\mu_\Theta(x)).
$$

Monte Carlo 形式：

$$
\boxed{
\widehat v_M(x)
=
\frac1M\sum_{m=1}^M
\left(\sigma_m^2(x)+\mu_m^2(x)\right)
-
\widehat\mu_M^2(x).
}
$$

第一部分包含成员内噪声，第二部分通过二阶矩减均值平方自动包含成员间均值分歧。

> [!warning] Mixture 通常不是单个 Gaussian
> 报告 $\widehat\mu\pm1.96\sqrt{\widehat v}$ 等价于再做 Gaussian moment matching；多峰或偏斜 mixture 下可能严重误导，应直接用 mixture quantile 或 samples。

## 六、Classification 要平均概率

第 $m$ 个成员输出

$$
p_m(y=k\mid x).
$$

mixture predictive probability 是

$$
\boxed{
\bar p_k(x)
=
\frac1M\sum_{m=1}^M p_{m,k}(x).
}
$$

若先平均 logits $z_m$ 再 softmax：

$$
\operatorname{softmax}\!\left(
\frac1M\sum_m z_m
\right),
$$

得到的是另一个组合规则，通常不等于概率 mixture。logit 还有加常数不变性，跨成员尺度也未必可比。

## 七、Probability Averaging 的一个例子

两个二分类成员：

$$
p_1(Y=1\mid x)=0.99,
\qquad
p_2(Y=1\mid x)=0.01.
$$

mixture 给

$$
\bar p=0.5.
$$

这不是说每个成员内部噪声很大，而是成员对标签完全分歧。若两个成员都给 $0.5$，mixture 也为 $0.5$，但不确定性的层级来源不同。

## 八、Monte Carlo Estimator

若

$$
\theta_m\stackrel{\mathrm{iid}}{\sim}q(\theta\mid D),
$$

对任意 integrable quantity $g(\theta)$：

$$
\widehat I_M
=\frac1M\sum_{m=1}^M g(\theta_m),
\qquad
I_q=E_q[g(\Theta)].
$$

则

$$
E[\widehat I_M]=I_q,
\qquad
\operatorname{Var}(\widehat I_M)
=\frac{\operatorname{Var}_q(g)}{M}.
$$

估计 standard error：

$$
\widehat{\operatorname{SE}}
=\sqrt{\frac{\widehat{\operatorname{Var}}(g)}{M}}.
$$

这里无偏是相对于 $q$ 的积分；若 $q\ne p(\theta\mid D)$，增加 $M$ 只能缩小 MC error，不能消除 approximation bias。

## 九、相关样本与 Effective Size

若成员量 $G_m=g(\theta_m)$ 方差相同、两两相关系数近似 $\rho$，则平均的方差：

$$
\operatorname{Var}(\bar G)
=
\sigma_G^2
\left(
\rho+\frac{1-\rho}{M}
\right).
$$

可定义近似有效成员数：

$$
M_{\rm eff}
\approx
\frac{M}{1+(M-1)\rho}.
$$

当 $\rho>0$，新增高度相似成员的收益快速饱和。成员数量不能替代 diversity、correlation 与 compute 报告。

## 十、Exact Bayes 与四类近似

| 方法 | 成员如何产生 | 近似对象 | 主要边界 |
|---|---|---|---|
| exact/高精度 posterior sampling | 从明确定义 posterior 采样 | $p(\theta\mid D)$ | 深网通常不可行 |
| variational inference | 优化 $q_\phi$ | 特定 divergence 下的 posterior | family/divergence bias |
| MC dropout | test-time mask samples | 特定 dropout variational view | 训练合同和 rate 依赖 |
| SWAG | SGD 轨迹 Gaussian | 局部低秩+对角 weight law | 局部、Gaussian、subspace |
| deep ensemble | 独立初始化/数据顺序训练 | algorithm-induced function mixture | 一般不是 posterior samples |
| bootstrap ensemble | 重采样数据后训练 | sampling variability + algorithm | 数据依赖单位与偏差 |

“Bayesian-like”经验行为不等于 exact Bayesian posterior。

## 十一、MC Dropout 的合同

MC dropout 在推断时保留随机 mask：

$$
\widehat p(y\mid x,D)
=
\frac1M\sum_{m=1}^M
p(y\mid x,\widetilde\theta_m).
$$

必须披露：

- 训练时 dropout placement/rate；
- prior/weight-decay/likelihood 对应；
- test-time 哪些层随机；
- BatchNorm 是否冻结；
- samples 数与 MC error；
- mask 是否跨 token/time 共享。

对一个任意 pretrained network 临时打开 dropout，不自动得到论文意义下的 posterior approximation。

## 十二、SWAG 的合同

SWAG 从 SGD iterates $\theta_t$ 估计均值与 covariance：

$$
q_{\rm SWAG}(\theta)
\approx
\mathcal N(
\bar\theta,
\Sigma_{\rm diag}+\Sigma_{\rm low-rank}
).
$$

从中采样权重并平均 predictions。重要细节：

1. 收集轨迹的学习率和时间窗；
2. covariance rank；
3. sample scale；
4. 每个 weight sample 的 BatchNorm statistics；
5. 局部 Gaussian 是否覆盖多个 function modes。

## 十三、Deep Ensemble 的合同

典型成员：

$$
\widehat\theta_m
=\mathcal A(D,\xi_m),
$$

其中 $\xi_m$ 包含 initialization、data order、augmentation 与 optimizer randomness。最终

$$
\bar p(y\mid x)
=\frac1M\sum_m p_{\widehat\theta_m}(y\mid x).
$$

它常有很强经验表现，但成员权重由训练算法隐式决定，不是 Bayes 公式给出的 posterior weights。若所有 runs 落入同一 basin，ensemble 可能低估 plausible function diversity；若成员模型错设相同，也可能一致地过度自信。

## 十四、Ensemble 为什么可能改善 Proper Risk

对真实标签 $y$，NLL 使用

$$
-\log\left(\frac1M\sum_m p_m(y)\right).
$$

由于 $-\log$ 是凸函数：

$$
-\log\left(\frac1M\sum_m p_m(y)\right)
\le
\frac1M\sum_m-\log p_m(y).
$$

因此 mixture 的逐样本 NLL 不超过成员 NLL 平均。但这不保证：

- 优于每一个最强成员；
- calibration error 必然更低；
- 0–1 accuracy 必然更高；
- shift 下仍成立相同排序；
- disagreement 等于真实 epistemic uncertainty。

## 十五、三个误差账户

对目标 posterior predictive $I_p$ 与实际估计 $\widehat I_M$：

$$
\widehat I_M-I_p
=
\underbrace{\widehat I_M-I_q}_{\text{MC error}}
+
\underbrace{I_q-I_p}_{\text{posterior approximation}}
+
\underbrace{I_p-I^*}_{\text{model misspecification}}.
$$

- 增大 $M$ 主要影响第一项；
- 更好的 inference family/optimizer 影响第二项；
- 改变 likelihood、features、model class 或 data mechanism 才可能处理第三项。

这条分账是本章最重要的审计工具。

## 十六、Posterior Predictive Check 不等于预测 Coverage

posterior predictive check 从 fitted model 生成复制数据：

$$
\theta^{\rm rep}\sim p(\theta\mid D),
\qquad
Y^{\rm rep}\sim p(y\mid\theta^{\rm rep}),
$$

再比较 discrepancy。它帮助发现模型无法复现的结构，但使用当前模型与数据，不能自动提供频率学有限样本 coverage，也不能证明模型真实。

## 十七、Shift 下的评估矩阵

至少沿 shift severity $s$ 报告：

$$
\text{accuracy}(s),\ 
\text{NLL}(s),\
\text{Brier}(s),\
\text{ECE}(s),\
\text{risk--coverage}(s).
$$

还要固定或披露：

- architecture 与 member count；
- per-member 与 total compute；
- search budget；
- posterior/ensemble sample generation；
- calibration data；
- shift generator 与 real-world provenance；
- subgroup 与 repeated-source dependence。

只在 clean test 上表现好，不支持 deployment uncertainty claim。

## 十八、图：对象、近似与误差账户

先看图回答：把 ensemble size 从 5 增至 50，究竟能缩小哪一种误差，哪些误差可能完全不变？

![[00-知识库管理/_assets/figures/learning-theory/fig-posterior-ensemble-approx-v2.svg|900]]

> [!figure] 图 20.8-03　Posterior predictive、近似家族与三类误差
> 左栏给出 prior–likelihood–posterior–predictive 链；中栏比较 MC dropout、SWAG 与 deep ensemble 的成员生成；右栏分开 MC、posterior approximation、misspecification 与 shift evaluation。来源：依据 Gal–Ghahramani、Lakshminarayanan et al.、Maddox et al. 与 Ovadia et al. 独立绘制；确定性 SVG，由 [[plot_calibration_uncertainty_v2.py]] 生成。

**怎样读图**：先确认目标是否真是某个 posterior predictive，再检查成员从什么分布/算法产生，最后把 samples 数、近似偏差和模型错设分别问责。

**图没有证明什么**：图没有证明 deep ensemble 成员是 posterior samples，也没有证明模型分歧在任意 OOD 或 distribution shift 下都与错误概率单调对应。

## 十九、AI 接口

### 19.1 Foundation Model Serving

多个 checkpoints、prompts 或 sampling seeds 是不同 ensemble axes。必须说明是 weight ensemble、prompt ensemble 还是 output sampling；三者不共享同一 Bayesian 解释。

### 19.2 LLM Self-Consistency

对 reasoning paths 多次采样并投票可改善部分任务，但反映的是指定 decoder distribution 与 prompt 下的答案分布。模型可能对同一错误答案高度一致。

### 19.3 科学机器学习

参数 posterior、numerical discretization error、surrogate approximation 与 observation noise 应分别建模；只加 ensemble 不能覆盖 PDE 模型偏差。

### 19.4 Active/Online Decision

exploration bonus 若来自 ensemble variance，需检查成员相关性、更新频率与 support coverage；未经校准的 bonus 可能导致过度或不足探索。

## 二十、常见错误

1. 用 posterior mean parameter 替代 posterior predictive；
2. 平均 logits 冒充概率 mixture；
3. 把 deep ensemble 称为 exact Bayesian；
4. 认为更多 samples 会修复 model misspecification；
5. 忽略成员相关性；
6. 用 mean ± 1.96 sd 近似任意多峰 mixture；
7. 不重估 SWAG sample 的 BatchNorm；
8. 临时打开 dropout 就宣称 MC dropout posterior；
9. clean calibration 外推到 shift；
10. 只报 total ensemble 性能，不报 compute 和 strongest member。

## 二十一、最小记忆

> [!summary]
> - posterior predictive 是 likelihood 对 posterior 的积分；
> - 参数平均、logit 平均与概率平均通常不同；
> - mixture variance = within-model + between-model；
> - MC samples 只消除对既定 $q$ 的积分误差；
> - MC dropout、SWAG、deep ensemble 的成员生成与理论身份不同；
> - uncertainty claim 必须同时审计近似、错设、相关性、shift 与 compute。

## 二十二、掌握标准

### A. 定义

能区分 posterior、function distribution、predictive mixture 与 algorithmic ensemble。

### B. 推导

能推导 posterior predictive、mixture moments、probability averaging、MC standard error 与相关性方差。

### C. 反例

能构造 parameter averaging 失败、ensemble 一致过度自信及 mixture Gaussian summary 失败的例子。

### D. 实验

能在相同 compute 合同下比较 single、MC dropout、SWAG 与 deep ensemble，并画 shift severity curves。

### E. 迁移

能为实际 AI 服务把模型样本、output samples、calibration 与 abstention 组织成可复现且不过度 Bayesian 化的报告。

## 二十三、练习与独立详解

- [[习题 - Bayesian Posterior Predictive、Ensemble 与近似边界]]
- [[解答 - Bayesian Posterior Predictive、Ensemble 与近似边界]]

## 参考来源

- [[S-2016-Gal-Ghahramani-MC-Dropout]]
- [[S-2017-Lakshminarayanan-Deep-Ensembles]]
- [[S-2019-Maddox-SWAG]]
- [[S-2019-Ovadia-Uncertainty-Shift]]
- [[S-2023-Wimmer-Aleatoric-Epistemic]]
