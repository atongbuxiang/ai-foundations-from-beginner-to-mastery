---
type: exercise
status: draft
area: [architecture, transformer, decoder-only, prefix-lm]
topic: "[[Decoder-Only、Prefix 与架构家族比较]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Decoder-Only、Prefix 与架构家族比较]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - Decoder-Only、Prefix 与架构家族比较

## A. 识别与复述

### ARCH-FAM-A01
写出架构家族的 relation、Q/K/V source、objective、outlet 四栏分类法。

### ARCH-FAM-A02
分别写出 encoder-only、decoder-only 与 encoder–decoder 的核心可见关系。

### ARCH-FAM-A03
说明为什么“单栈”不等于“整条序列全 causal”。

## B. 手算与建模

### ARCH-FAM-B01
对 prefix 长 $P=2$、suffix 长 $S=3$，写出 $5\times5$ prefix-LM 可见矩阵。

### ARCH-FAM-B02
对 [source(3);target(2)] 的纯 causal decoder，写 target rows 对 source/target 的可见性，并给出只监督 target 的 loss mask。

### ARCH-FAM-B03
证明正对角下三角 attention matrix 满秩；再说明为何可能有效秩仍低。

## C. 推导与证明

### ARCH-FAM-C01
用分块矩阵写 prefix-LM relation，并证明 prefix rows 不依赖 suffix values。

### ARCH-FAM-C02
比较拼接式单栈与 encoder–decoder 的 source 表示、层间读取和 cache 生命周期。

### ARCH-FAM-C03
给出一个“可见信息集合相同，但参数化与计算图不同”的最小例子。

## D. 边界、反例与纠错

### ARCH-FAM-D01
反驳：“Causal attention 满秩，所以 decoder-only 必然比 encoder 更强。”

### ARCH-FAM-D02
构造 attention mask 相同但 loss mask 不同、从而训练目标不同的两个模型。

### ARCH-FAM-D03
指出只按相同层数比较 encoder–decoder 与 decoder-only 的不公平之处。

## E. AI 迁移

### ARCH-FAM-E01
为理解、条件生成和在线服务三个场景建立架构选择表。

### ARCH-FAM-E02
设计检验 Science Space decoder-only 低秩猜想的受控实验。

### ARCH-FAM-E03
写一份固定总参数、训练 FLOPs、数据与 context 的家族比较协议。

## 解答入口

[[解答 - Decoder-Only、Prefix 与架构家族比较]]
