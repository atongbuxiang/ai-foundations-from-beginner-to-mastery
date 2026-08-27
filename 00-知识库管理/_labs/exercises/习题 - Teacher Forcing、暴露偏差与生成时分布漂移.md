---
type: exercise
status: draft
area: [generative-models, autoregressive, sequence-learning]
topic: "[[Teacher Forcing、暴露偏差与生成时分布漂移]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Teacher Forcing、暴露偏差与生成时分布漂移]]"
created: 2026-08-25
updated: 2026-08-25
---

# 习题 - Teacher Forcing、暴露偏差与生成时分布漂移

## A. 识别与复述

### GEN05-A01
分别写 $R_{TF}$ 与 rollout prefix distribution，指出期望测度哪里不同。

### GEN05-A02
为什么 Exposure Bias 不等于 Teacher Forcing MLE 在可实现极限下不一致？

### GEN05-A03
区分 label leakage、prefix distribution shift 与 sequence-level objective mismatch。

## B. 手算与建模

### GEN05-B01
真实序列为 00/11 各半。模型第一步 $q(1)=0.6$，第二步完全复制前缀。列模型 joint、总变差与 TF 第二步错误。

### GEN05-B02
每步所有可达前缀的 conditional TV 至多 0.02。用逐步 coupling 给长度 20 joint TV 的粗上界。

### GEN05-B03
两步数据有 $X_2=X_1$ 且边缘均匀。Scheduled Sampling 第二步完全使用独立模型前缀。求训练 pair 的 joint 与最优 $q(x_2\mid\hat x_1)$。

## C. 推导与证明

### GEN05-C01
证明 Teacher Forcing NLL 之和等于 joint NLL。

### GEN05-C02
在全前缀 conditional TV ≤ $\varepsilon$ 下，用最大耦合证明 joint TV ≤ $T\varepsilon$ 的截断上界。

### GEN05-C03
推导一般混合率 $\alpha$ 的两步 scheduled-sampling pair distribution，并说明何时仍等于真实 joint。

## D. 边界、反例与纠错

### GEN05-D01
构造一步误差不会累积、系统会自动恢复的序列模型，反驳“误差必然指数爆炸”。

### GEN05-D02
构造 TF loss 很低但一个稀有错误前缀会进入吸收循环的模型。

### GEN05-D03
为什么把模型 token 加入训练输入不自动“修复” distribution shift？至少从 estimand、target pairing、梯度三方面回答。

## E. AI 迁移

### GEN05-E01
设计 prefix perturbation benchmark，区分自然数据前缀、单 token 扰动和模型 rollout 前缀。

### GEN05-E02
比较 Teacher Forcing、scheduled sampling 与 sequence-level RL，写目标、estimator、bias/variance 和评测。

### GEN05-E03
为聊天模型的重复循环设计因果诊断：模型概率、top-$p$、EOS、cache 与 prompt shift 至少五组干预。

## 解答入口

[[解答 - Teacher Forcing、暴露偏差与生成时分布漂移]]

