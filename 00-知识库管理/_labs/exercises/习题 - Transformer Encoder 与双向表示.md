---
type: exercise
status: draft
area: [architecture, transformer, encoder, bidirectional]
topic: "[[Transformer Encoder 与双向表示]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Transformer Encoder 与双向表示]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - Transformer Encoder 与双向表示

## A. 识别与复述

### ARCH-ENC-A01
给出 encoder 输入、每层输出和最终输出的标准 shapes；说明为什么最终仍有 $T$ 行。

### ARCH-ENC-A02
精确定义“双向可见”，并列出它不表示的两件事。

### ARCH-ENC-A03
区分 encoder 架构、MLM objective、corruption recipe 与 downstream head。

## B. 手算与建模

### ARCH-ENC-B01
序列有效长度为 3、右侧 padding 到 5。写出有效 query 的 key-padding 可见矩阵，并说明 padding query rows 如何处理。

### ARCH-ENC-B02
给定三个有效 token states $(1,0),(3,2),(2,4)$ 和两个 padding states，计算 masked mean pooling。

### ARCH-ENC-B03
对 $V=30000,d=768,T=512$，计算 token embedding 主参数量与 learned absolute position embedding 主参数量。

## C. 推导与证明

### ARCH-ENC-C01
证明在没有位置/segment 非对称项、mask 随置换同步变化时，self-attention encoder 对 token 置换等变。

### ARCH-ENC-C02
说明 key-padding 只屏蔽列时，为什么 padding query row 仍可能非零；写出保证 pooled output 不受其影响的条件。

### ARCH-ENC-C03
推导标准 encoder block 的主要 MAC 项，并解释双向 mask 为什么不自动减少 dense pair count。

## D. 边界、反例与纠错

### ARCH-ENC-D01
构造忽略 padding 的 mean pooling 随 padding 长度变化的反例。

### ARCH-ENC-D02
反驳：“Encoder 双向读取，所以它使用了现实世界的未来信息并完成了因果推断。”

### ARCH-ENC-D03
给出一个没有 position encoding 时，两条不同顺序序列无法被 permutation-invariant pooling 区分的例子。

## E. AI 迁移

### ARCH-ENC-E01
为一个文本分类 encoder 写 padding invariance、置换敏感性和 pooling 正确性的测试计划。

### ARCH-ENC-E02
设计 [CLS]、masked mean 与 attention pooling 的公平比较。

### ARCH-ENC-E03
为 BERT 风格结果写 evidence card，避免把 objective、数据与架构贡献混为一谈。

## 解答入口

[[解答 - Transformer Encoder 与双向表示]]
