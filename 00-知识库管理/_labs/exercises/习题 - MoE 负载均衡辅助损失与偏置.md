---
type: exercise
status: draft
area: [architecture, moe, load-balancing]
topic: "[[MoE 负载均衡辅助损失与偏置]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - MoE 负载均衡辅助损失与偏置]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - MoE 负载均衡辅助损失与偏置

## A. 识别与复述

### ARCH-AUX-A01
定义 hard frequency $f_i$ 与 mean soft probability $P_i$。

### ARCH-AUX-A02
说明 $E\sum_i f_iP_i$ 为什么是 proxy 而不是 hard capacity 本身。

### ARCH-AUX-A03
区分 load-balancing loss 与 Router z-loss 的优化对象。

## B. 手算与建模

### ARCH-AUX-B01
对 $f=[0.75,0.25],P=[0.7,0.3],E=2$ 计算归一化均衡项。

### ARCH-AUX-B02
对完全均匀与全部集中两种情况，分别计算 $E\sum_i f_iP_i$。

### ARCH-AUX-B03
若 $T=4,E=2,\lambda=0.01,f=[0.75,0.25]$，在 stop-grad $f$ 下求 $\partial L/\partial p_{ti}$ 的直接系数。

## C. 推导与证明

### ARCH-AUX-C01
从 softmax Jacobian 推导 $L_{bal}$ 对单个 logit $z_{tj}$ 的梯度。

### ARCH-AUX-C02
在 $f=P$ 且 $\sum_iP_i=1$ 时，证明均匀分布最小化 $E\sum_iP_i^2$。

### ARCH-AUX-C03
写出 capacity constraint 的拉格朗日松弛，解释辅助项与约束优化的关系。

## D. 边界、反例与纠错

### ARCH-AUX-D01
反驳：“负载越均匀，任务质量一定越好。”

### ARCH-AUX-D02
说明相同 $\lambda$ 为何跨代码库未必等价。

### ARCH-AUX-D03
构造逐序列完美均衡会压制真实专业化的情形。

## E. AI 迁移

### ARCH-AUX-E01
设计 $\lambda$ sweep 的最小实验与报告指标。

### ARCH-AUX-E02
设计检验 token/microbatch/sequence/global 四种统计粒度的实验。

### ARCH-AUX-E03
写出监控 Router collapse 的 dashboard 指标。

## 解答入口

[[解答 - MoE 负载均衡辅助损失与偏置]]

