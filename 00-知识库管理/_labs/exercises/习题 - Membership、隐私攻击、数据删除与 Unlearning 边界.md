---
type: exercise
status: verified
area: [language-models, privacy, membership-inference, unlearning]
topic: "[[Membership、隐私攻击、数据删除与 Unlearning 边界]]"
solution: "[[解答 - Membership、隐私攻击、数据删除与 Unlearning 边界]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Membership、隐私攻击、数据删除与 Unlearning 边界

## A. 识别与复述

### LM66-A01
写出 membership inference 的 $H_0/H_1$，并说明“记录单位”为什么必须固定。

### LM66-A02
区分 TPR、FPR、AUC 与 PPV；隐私审计为什么特别看低 FPR？

### LM66-A03
区分数据库删除、exact retraining、certified removal 与 empirical unlearning。

## B. 手算与构造

### LM66-B01
成员基率 $\pi=.001$，攻击 TPR $=.6$、FPR $=.01$，计算阳性预测 PPV。

### LM66-B02
10000 个 non-members 中有 4 个误报，200 个 members 中有 70 个命中，计算 FPR、TPR 与经验 precision（按这个评估样本比例）。

### LM66-B03
给定原模型、unlearned 模型和重训模型在四个 probe 上的输出概率分别为 $(.9,.7,.3,.2)$、$(.5,.5,.4,.2)$、$(.45,.55,.35,.25)$，计算 unlearned 与 retrain 的平均绝对差。

## C. 推导与证明

### LM66-C01
推导 Bayes 公式下 PPV 与基率、TPR、FPR 的关系。

### LM66-C02
解释 Neyman–Pearson 似然比检验为何在固定 FPR 下是自然的成员攻击。

### LM66-C03
证明“两个模型 benchmark accuracy 相等”不能推出它们对任意观察者分布接近。

## D. 边界、反例与纠错

### LM66-D01
反驳“AUC=.5，所以模型满足隐私保证”。

### LM66-D02
构造“目标字符串不再生成但成员仍可推断”的反例。

### LM66-D03
一次删除只更新训练数据库和向量库，旧 checkpoint 与缓存仍在线。判断是否完成并说明理由。

## E. AI 迁移

### LM66-E01
为低 FPR 成员审计设计 sampling、threshold 与 interval 协议。

### LM66-E02
给一个 RAG+adapter 系统写删除 lineage 清单。

### LM66-E03
比较 full retraining 与 SISA/近似 unlearning 的成本—保证—效用决策表。

独立完成后查看[[解答 - Membership、隐私攻击、数据删除与 Unlearning 边界]]。
