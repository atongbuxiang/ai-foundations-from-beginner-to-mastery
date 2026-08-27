---
type: exercise
status: draft
area: [math/statistics, ai/bayesian-inference]
topic: "Bayesian 推断与后验预测"
difficulty: [A, B, C, D, E]
prerequisites: ["[[Bayesian 推断与后验预测]]"]
related: ["[[概率论与数理统计 MOC]]", "[[练习与测验 MOC]]"]
solution: "[[解答 - Bayesian 推断与后验预测]]"
created: 2026-08-19
updated: 2026-08-19
---

# 习题 - Bayesian 推断与后验预测

> [!abstract] 训练目标
> 从 joint model 重建 posterior 与 predictive，掌握 conjugacy、Bayes action、credible region、partial pooling 和 predictive checking，并把模型不确定性、近似推断误差与计算误差分开。

## A. 识别与复述

### PROB-BAYES-A01

定义 prior、likelihood、evidence、posterior、prior predictive 与 posterior predictive。逐一说明它们在哪个空间上归一化，以及 likelihood 为什么不是参数分布。

### PROB-BAYES-A02

说明 posterior mean、median、MAP 分别对应 squared、absolute 与局部 0–1 loss。为什么 MAP 不是“最 Bayesian”的通用点估计？

### PROB-BAYES-A03

比较 credible interval、confidence interval、prior predictive check、posterior predictive check、held-out predictive evaluation 与 simulation-based calibration 的条件对象和用途。

## B. 手算与构造

### PROB-BAYES-B01

$Y_i\mid p\sim\operatorname{Bernoulli}(p)$，$p\sim\operatorname{Beta}(2,3)$。观测 $n=10,S=7$。求 posterior、mean、mode、variance、未来一次成功概率，以及未来 3 次恰有 2 次成功的 posterior predictive probability。

### PROB-BAYES-B02

$Y_i\mid\mu\sim N(\mu,4)$，prior $\mu\sim N(0,9)$。观测 $n=4,\bar y=3$。求 posterior mean/variance、95% equal-tail credible interval，以及未来新观测的 predictive mean/variance。

### PROB-BAYES-B03

三分类概率 $\pi\sim\operatorname{Dirichlet}(1,1,1)$，counts 为 $(4,2,0)$。求 posterior、posterior mean、未来两个样本类别 counts 的 Dirichlet–Multinomial probability，并解释 unseen class 为何仍有正预测概率。

## C. 推导与证明

### PROB-BAYES-C01

证明 squared posterior loss 的 Bayes action 是 posterior mean、absolute loss 的 Bayes action 是任一 posterior median。指出连续参数下 pointwise 0–1 loss 的问题。

### PROB-BAYES-C02

推导

$$
\operatorname{Var}(\widetilde Y\mid y)
=E[\operatorname{Var}(\widetilde Y\mid\Theta,y)\mid y]
+\operatorname{Var}(E[\widetilde Y\mid\Theta,y]\mid y).
$$

用它解释 plug-in predictive 为什么常低估 uncertainty，并给出非线性均值中 Jensen gap 的例子。

### PROB-BAYES-C03

证明 sequential updating 与 batch updating 在 conditional independence 下等价。再推导 posterior predictive Monte Carlo mixture 的 stable logsumexp 公式。

## D. 边界、反例与纠错

### PROB-BAYES-D01

用 $\theta>0$ 上 flat prior 与 $\phi=\log\theta$ 的坐标变换说明“无信息 flat prior”不具坐标不变性。解释 improper prior 为何可产生 proper posterior，却不能直接用于 Bayes factor。

### PROB-BAYES-D02

构造一个模型错设但 posterior 随 $n$ 极窄的例子，反驳“posterior 越窄，现实预测越可靠”。列出至少三种 sensitivity/check。

### PROB-BAYES-D03

反驳：“VAE encoder 输出 $q_\phi(z\mid x)$，因此 VAE 已经对所有 neural-network weights 做了完整 Bayesian inference。”写出正确的 parameter/latent/variational 对象。

## E. AI 迁移

### PROB-BAYES-E01

为 Bayesian neural classifier 写一份审计：weight prior 的 function-space 含义、symmetry、likelihood、推断近似、posterior predictive、calibration、OOD 与 MCSE。说明 deep ensemble 与 MC dropout 何时不能直接称 posterior draws。

### PROB-BAYES-E02

设计一个对 50 个小样本客户转化率进行 hierarchical partial pooling 的模型。写生成过程、关键 posterior predictive、no/complete/partial pooling 比较，以及 group-size imbalance 的诊断。

### PROB-BAYES-E03

设计 prior predictive、SBC、posterior predictive 与 held-out evaluation 四阶段实验，验证一个 count prediction model。每阶段说明能发现什么、不能证明什么。

## 提示

- B01：posterior 为 Beta$(9,6)$；
- B02：precision 相加，$n/\sigma^2=1$；
- B03：使用 Dirichlet–Multinomial 的 Gamma/Beta 函数形式；
- C03：log predictive density 是 log-average-exp；
- D01：density 变换带 Jacobian $d\theta/d\phi=e^\phi$。

## 解答入口

完成独立尝试后再打开：[[解答 - Bayesian 推断与后验预测]]。

