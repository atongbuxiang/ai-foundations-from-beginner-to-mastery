---
type: exercise
status: draft
area: [architecture, graph-neural-networks, expressivity]
topic: "[[聚合器、可辨识性与 Graph Isomorphism Network]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - 聚合器、可辨识性与 Graph Isomorphism Network]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - 聚合器、可辨识性与 Graph Isomorphism Network

## A. 识别与复述

### ARCH-GIN-A01
定义多重集聚合器在给定定义域上的 injectivity，并解释碰撞为何不可由后续 MLP 修复。

### ARCH-GIN-A02
分别说明 mean、max、sum 的主要信息保留与损失。

### ARCH-GIN-A03
写出 GIN 更新式，并说明 $1+\epsilon$ 的角色。

## B. 手算与建模

### ARCH-GIN-B01
为 mean 构造两组 cardinality 不同但输出相同的二维向量多重集。

### ARCH-GIN-B02
为逐坐标 max 构造两组不同二维多重集，使输出相同但元素支持不同。

### ARCH-GIN-B03
取标量 $h_i=2$、邻居 $\{1,1,3\}$、$\epsilon=0.5$，MLP 暂取恒等，计算一层 GIN 输入与输出。

## C. 推导与证明

### ARCH-GIN-C01
证明把多重集中每个元素重复 $k$ 次不改变 mean。

### ARCH-GIN-C02
在有限标签集和最大 multiplicity $M$ 下，构造一种 injective sum encoding。

### ARCH-GIN-C03
说明 injective aggregation、update、readout 如何使 GIN 模拟 1-WL 的一轮细化。

## D. 边界、反例与纠错

### ARCH-GIN-D01
给出裸 sum 的碰撞，反驳“sum 本身总是 injective”。

### ARCH-GIN-D02
反驳：“GIN 可以区分所有非同构图。”

### ARCH-GIN-D03
说明为何 LSTM aggregator 即使训练时随机排列，也不是逐次严格 permutation invariant。

## E. AI 迁移

### ARCH-GIN-E01
设计 sum/mean/max/learned pooling 的合成可辨识实验。

### ARCH-GIN-E02
为实际浮点 GIN 设计近碰撞与数值稳定性测试。

### ARCH-GIN-E03
写一个 graph-classification 聚合器消融协议，避免把参数量差异误当聚合器优势。

## 解答入口

[[解答 - 聚合器、可辨识性与 Graph Isomorphism Network]]

