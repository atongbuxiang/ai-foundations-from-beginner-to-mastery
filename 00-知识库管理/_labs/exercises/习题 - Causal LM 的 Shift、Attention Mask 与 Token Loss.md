---
type: exercise
status: verified
area: [language-models, causal-lm, loss-contract]
topic: "[[Causal LM 的 Shift、Attention Mask 与 Token Loss]]"
solution: "[[解答 - Causal LM 的 Shift、Attention Mask 与 Token Loss]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Causal LM 的 Shift、Attention Mask 与 Token Loss

## A. 识别与复述

### LM10-A01
分别说明 shift、attention relation、loss mask 的职责。

### LM10-A02
给出批大小 $B$、长度 $L$、词表 $V$ 时 inputs、logits、labels、loss mask 的形状。

### LM10-A03
为什么 prompt token 可以可见但不计 loss？

## B. 手算与构造

### LM10-B01
对 `[BOS,a,b,EOS]` 写 inputs、labels 与三个计分位置。

### LM10-B02
写出 $L=4$ 的 causal relation 矩阵；再加入最后一位 padding 的 key/query 约束。

### LM10-B03
设备 A 有 80 tokens、均损 1.2，B 有 20 tokens、均损 2.0；计算正确全局均值和错误设备均值。

## C. 推导与证明

### LM10-C01
证明全局规约 numerator/denominator 与把所有有效 token 直接求平均等价。

### LM10-C02
说明 softmax 前加 $-\infty$ 如何令屏蔽位置权重为 0；有限大负数有什么数值边界？

### LM10-C03
证明未来 token 变化不应影响过去 logits 是因果 relation 的必要 metamorphic property。

## D. 边界、反例与纠错

### LM10-D01
构造 double shift 导致预测错两位的例子。

### LM10-D02
反驳“padding 已从 loss 忽略，所以无需 attention padding mask”。

### LM10-D03
指出只用下三角 mask 进行多文档 packing 的潜在泄漏。

## E. AI 迁移

### LM10-E01
写一个不依赖 loss 下降的三步防未来泄漏测试。

### LM10-E02
为 prompt–answer SFT 画 input、next labels、attention relation 与 loss region。

### LM10-E03
审计一个训练日志只有 `loss=2.1`、没有 numerator 和有效 token 数的分布式实验。

独立完成后查看[[解答 - Causal LM 的 Shift、Attention Mask 与 Token Loss]]。

