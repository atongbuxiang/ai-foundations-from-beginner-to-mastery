---
type: exercise
status: verified
area: [language-models, pretraining-data, packing]
topic: "[[Packing、文档边界、Position ID 与 Loss Mask]]"
solution: "[[解答 - Packing、文档边界、Position ID 与 Loss Mask]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Packing、文档边界、Position ID 与 Loss Mask

## A. 识别与复述

### LM22-A01
区分 padding batching、concatenated stream 与 contamination-free packing。

### LM22-A02
Packing 为什么需要装箱、relation、position、label 四份合同？

### LM22-A03
reset 与 continuous position IDs 分别改变什么？

## B. 手算与构造

### LM22-B01
长度 `[6,5,4,3,2]`、bin capacity 10，用 first-fit decreasing 装箱并算利用率。

### LM22-B02
两文档长度 2、3，以 query 为行写 $5\times5$ block-causal relation。

### LM22-B03
对 `[a,EOS | b,c,EOS]` 写 inputs、next labels 与阻止跨文档 target 的 loss mask。

## C. 推导与证明

### LM22-C01
证明 $R_{ij}=1\{j\le i\}1\{d_i=d_j\}$ 为下三角块对角。

### LM22-C02
给出 packed 与逐文档 forward 等价的充分条件。

### LM22-C03
说明全局 $N/D$ 如何保持每有效 token 等权；per-bin mean 为何不同。

## D. 边界、反例与纠错

### LM22-D01
反驳“loss ignore 边界后无需 block attention”。

### LM22-D02
构造 continuous position 使同一文档因 pack 前缀长度改变 logits 的例子。

### LM22-D03
反驳“padding 减少 50% 就保证 wall time 减少 50%”。

## E. AI 迁移

### LM22-E01
设计 packed/unpacked logit equivalence test。

### LM22-E02
为 CLM/MLM/Prefix 三类目标分别写 packed relation。

### LM22-E03
审计只写 `packing=True`、无边界策略和 position IDs 的训练配置。

独立完成后查看[[解答 - Packing、文档边界、Position ID 与 Loss Mask]]。

