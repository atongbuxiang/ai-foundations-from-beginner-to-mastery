---
type: exercise
status: draft
area: [generative-models, likelihood]
topic: "[[最大似然、交叉熵与前向 KL]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - 最大似然、交叉熵与前向 KL]]"
created: 2026-08-25
updated: 2026-08-25
---

# 习题 - 最大似然、交叉熵与前向 KL

## A. 识别与复述

### GEN03-A01
写出 dataset likelihood、log-likelihood、平均 NLL 和 population risk，并说明它们的随机性。

### GEN03-A02
“MLE 最小化 forward KL”的准确等价类型是什么？列出至少三个条件。

### GEN03-A03
区分 approximation、estimation、optimization、protocol 和 sampling error。

## B. 手算与建模

### GEN03-B01
Bernoulli 数据 10 个 1、5 个 0。求 MLE、平均 NLL，并说明边界数据全为 1 时发生什么。

### GEN03-B02
$P_*=(1/2,1/3,1/6)$，$Q=(1/2,1/4,1/4)$。用自然对数计算 cross-entropy 与 forward KL，并验证差为 $H(P_*)$。

### GEN03-B03
两个条件的频率为 $(0.8,0.2)$，conditional NLL 分别为 $(0.1,1.0)$ nat。求总体 conditional NLL；部署权重换为 $(0.3,0.7)$ 后再求。

## C. 推导与证明

### GEN03-C01
从定义完整推导 $H(P_*,P_\theta)=H(P_*)+D_{KL}(P_*\Vert P_\theta)$。

### GEN03-C02
证明 categorical 模型的 population cross-entropy 在 $q=p_*$ 处最小，并讨论零概率坐标。

### GEN03-C03
推导条件 cross-entropy 分解为条件熵加对条件 KL 的 $P_*(C)$ 加权平均。

## D. 边界、反例与纠错

### GEN03-D01
解释为什么连续数据的经验分布与普通 Lebesgue-density 模型之间的 KL 可能为无穷，不能机械写经验 KL 等式。

### GEN03-D02
构造“held-out NLL 较低但部署样本较差”的合理机制，不允许只写“指标不完美”。

### GEN03-D03
反驳：“forward KL mode-covering，所以 MLE 模型绝不会漏模式。”

## E. AI 迁移

### GEN03-E01
审计一个语言模型训练 loss：token mask、sequence weighting、padding、log base 和 reduction 如何改变 estimand？

### GEN03-E02
设计实验把 NLL 改善分解到频繁 token、稀有 token、序列长度和条件组别。

### GEN03-E03
为图像生成比较设计 likelihood—quality—coverage 三指标协议，并写出不能从任一单指标推出的结论。

## 解答入口

[[解答 - 最大似然、交叉熵与前向 KL]]

