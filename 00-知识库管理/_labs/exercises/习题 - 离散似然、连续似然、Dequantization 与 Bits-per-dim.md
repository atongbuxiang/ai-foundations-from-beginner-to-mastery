---
type: exercise
status: draft
area: [generative-models, likelihood, image-generation]
topic: "[[离散似然、连续似然、Dequantization 与 Bits-per-dim]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - 离散似然、连续似然、Dequantization 与 Bits-per-dim]]"
created: 2026-08-25
updated: 2026-08-25
---

# 习题 - 离散似然、连续似然、Dequantization 与 Bits-per-dim

## A. 识别与复述

### GEN06-A01
区分离散 mass、连续 point density 与 bin probability。

### GEN06-A02
uniform dequantization 优化的是 exact discrete likelihood 还是 lower bound？何时取等？

### GEN06-A03
BPD 的 log base、维度、bin width 与 bound 方向分别是什么？

## B. 手算与建模

### GEN06-B01
一维离散 $X\in\{0,1}$，连续密度在 bins $[0,1),[1,2)$ 上常数分别为 0.3、0.7。求离散 mass 和两点 BPD。

### GEN06-B02
一个 2×2 RGB 图的模型质量为 $2^{-60}$。求 BPD；若误按 4 pixels 归约会报多少？

### GEN06-B03
像素从 unit-bin $Y=X+U$ 缩放为 $Z=Y/256$。写 log-density 关系与每维 bits 常数。

## C. 推导与证明

### GEN06-C01
用 Jensen 完整推导 uniform dequantization lower bound。

### GEN06-C02
用 importance identity 推导 variational dequantization bound，并证明 gap 是 KL。

### GEN06-C03
证明 dequantization log-likelihood lower bound 转成 BPD 后是不小于 true discrete BPD 的上界。

## D. 边界、反例与纠错

### GEN06-D01
构造连续 density 在训练离散点处越来越高但每个合理 bin mass 不改善的尖峰序列。

### GEN06-D02
解释为什么 noise 支持越出 $[0,1)^D$ 会破坏无歧义 floor 解码，并给反例。

### GEN06-D03
反驳：“模型 A 的 continuous NLL 比 B 小，所以其 discrete BPD 必然更小。”列出至少四项需对齐协议。

## E. AI 迁移

### GEN06-E01
审计两篇 CIFAR-10 likelihood 报告：列预处理、dequantizer、bits 常数、维度和 test estimator。

### GEN06-E02
设计数值实验测量 uniform 与 variational dequantization gap，说明如何近似 bin integral。

### GEN06-E03
为连续 Flow 的 sample→pixel 后处理写 round/floor、clip、域外拒绝与颜色尺度合同。

## 解答入口

[[解答 - 离散似然、连续似然、Dequantization 与 Bits-per-dim]]

