---
type: exercise
status: draft
area: [architecture, transformer, encoder-decoder, cross-attention]
topic: "[[Encoder–Decoder 与 Cross-Attention]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Encoder–Decoder 与 Cross-Attention]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - Encoder–Decoder 与 Cross-Attention

## A. 识别与复述

### ARCH-ED-A01
写出 encoder–decoder 的条件概率分解与 encoder memory shape。

### ARCH-ED-A02
按顺序列出标准 decoder layer 的三个子层，并说明每层外部 shape。

### ARCH-ED-A03
区分 source padding、target causal 与 target loss mask。

## B. 手算与建模

### ARCH-ED-B01
给定 $B=2,T_t=5,T_s=7,h=4,d_h=16$，写出 cross-attention 的 Q/K/V、score 与输出 shapes。

### ARCH-ED-B02
一条 source 有 3 个有效 token、pad 到 5，target 长 4。写出 cross-attention 可见矩阵；它是否是三角形？

### ARCH-ED-B03
若 $T_s=128,T_t=32,d=512$，计算 cross-attention 两次 pairwise contraction 的 MAC 数（$B=1$）。

## C. 推导与证明

### ARCH-ED-C01
从矩阵乘法推导 cross-attention 输出为什么回到 target 轴而非 source 轴。

### ARCH-ED-C02
证明固定 encoder memory 时，cross K/V 可在逐步生成中预投影复用；列出会破坏复用的架构变化。

### ARCH-ED-C03
推导标准 encoder–decoder decoder layer 相对 decoder-only layer 多出的主参数量。

## D. 边界、反例与纠错

### ARCH-ED-D01
构造把 target causal triangle 错加到 cross-attention 上而屏蔽合法 source 的例子。

### ARCH-ED-D02
反驳：“Cross-attention 权重高的 source token 就是答案的忠实原因。”

### ARCH-ED-D03
说明把 source 与 target 拼接成单栈后，为何不能仍宣称计算图与标准 encoder–decoder 完全相同。

## E. AI 迁移

### ARCH-ED-E01
为翻译模型写 source/target mask 与 cache 的端到端测试表。

### ARCH-ED-E02
设计 source ablation、counterfactual replacement 与引用验证实验，检验条件生成是否真正使用 source。

### ARCH-ED-E03
为 encoder–decoder 与 decoder-only 条件生成做公平比较，列出预算与系统控制变量。

## 解答入口

[[解答 - Encoder–Decoder 与 Cross-Attention]]
