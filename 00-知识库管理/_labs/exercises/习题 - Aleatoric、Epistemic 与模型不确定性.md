---
type: exercise
status: draft
area: [learning-theory/uncertainty, aleatoric, epistemic]
topic: "[[Aleatoric、Epistemic 与模型不确定性]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[Aleatoric、Epistemic 与模型不确定性]]"]
related: ["[[解答 - Aleatoric、Epistemic 与模型不确定性]]", "[[Bayesian Posterior Predictive、Ensemble 与近似边界]]"]
solution: "[[解答 - Aleatoric、Epistemic 与模型不确定性]]"
created: 2026-08-23
updated: 2026-08-23
---

# 习题 - Aleatoric、Epistemic 与模型不确定性

> [!abstract] 训练目标
> 能先声明随机对象与知识状态，再使用总方差或 entropy/MI 分解；能识别 likelihood 错设、model-form、approximation 与 shift 被一个 uncertainty 数字掩盖的情形。

## A. 识别与复述

### LT-UNC-A01

写出 uncertainty contract 的五项：预测对象、条件信息、知识主体、functional 与行动。对“模型对这张图很不确定”补全合同。

### LT-UNC-A02

区分 observation noise、label ambiguity、parameter/function、model-form、approximation 与 distribution-shift uncertainty；各给一个可缓解动作。

### LT-UNC-A03

为什么 aleatoric 只能相对于给定信息集称为“不可约”？为什么 OOD 与 epistemic 不是同义词？

## B. 手算与局部推导

### LT-UNC-B01

三个等权 regression members 的均值为 $(0,1,2)$，成员内方差为 $(1,4,1)$。计算 predictive mean、within、between 与 total variance。

### LT-UNC-B02

对 heteroscedastic Gaussian NLL
$$
\ell(s)=\tfrac12e^{-s}r^2+\tfrac12s
$$
求一、二阶导数，求固定非零残差 $r$ 的最优 $s$；解释 $r=0$ 的退化趋势。

### LT-UNC-B03

两个等权二分类成员分别给 $p_1(Y=1)=0.9$、$p_2(Y=1)=0.1$。计算 mixture predictive entropy、成员平均 entropy 与 mutual information（用自然对数）。

## C. 证明与反例

### LT-UNC-C01

从加减条件均值开始，完整证明
$$
\operatorname{Var}(Y\mid x,D)
=E[\operatorname{Var}(Y\mid x,\Theta)]
+\operatorname{Var}(E[Y\mid x,\Theta]).
$$

### LT-UNC-C02

构造一个加入额外传感器 $Z$ 后 $\operatorname{Var}(Y\mid X,Z)<\operatorname{Var}(Y\mid X)$ 的例子，说明 aleatoric 的信息集依赖。

### LT-UNC-C03

分别构造 OOD 但成员低分歧、in-distribution 但高分歧的例子；解释为什么单一 ensemble variance 不能定义 OOD。

## D. 审计与诊断

### LT-UNC-D01

异方差回归模型在均值系统偏低的区域输出很大 $\sigma(x)$。设计 residual、coverage、likelihood 与 counterfactual diagnostics，判断 variance 是否在吸收 bias。

### LT-UNC-D02

论文把 predictive entropy 称为 aleatoric、mutual information 称为 epistemic，却不说明成员生成。列出理论解释所缺的 posterior/ensemble 合同。

### LT-UNC-D03

为 active learning 审计“选择最高 entropy 样本”的策略。如何区分不可约 label ambiguity、可缩减知识不足、群组覆盖与 batch redundancy？

## E. 研究与迁移

### LT-UNC-E01

为自动驾驶感知建立 uncertainty source × mitigation 矩阵，覆盖遮挡、传感器噪声、罕见天气、模型错设、推断近似与反馈 shift。

### LT-UNC-E02

为 LLM 设计区分 token entropy、answer disagreement、事实未知、题目歧义与 evaluator uncertainty 的研究；给出可证伪 metrics。

### LT-UNC-E03

写一份 uncertainty claim card：允许的最强结论、模型/信息集条件、校准/coverage/utility 证据，以及禁止使用的模糊表述。
