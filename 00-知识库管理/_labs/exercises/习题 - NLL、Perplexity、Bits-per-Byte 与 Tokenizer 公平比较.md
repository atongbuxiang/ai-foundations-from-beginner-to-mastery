---
type: exercise
status: verified
area: [language-models, evaluation, perplexity]
topic: "[[NLL、Perplexity、Bits-per-Byte 与 Tokenizer 公平比较]]"
solution: "[[解答 - NLL、Perplexity、Bits-per-Byte 与 Tokenizer 公平比较]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - NLL、Perplexity、Bits-per-Byte 与 Tokenizer 公平比较

## A. 识别与复述

### LM15-A01
定义 total NLL、token-mean NLL、PPL 与 BPB，并注明 log base。

### LM15-A02
为什么 PPL 的“平均分支数”解释只是一种直觉？

### LM15-A03
列出跨 tokenizer 比较前必须锁定的概率对象与 denominator。

## B. 手算与构造

### LM15-B01
目标概率为 $0.5,0.25,0.125$，计算 total NLL（bits）、mean bits/token 与 PPL。

### LM15-B02
一段 100-byte 文本 total NLL 为 $50\ln2$ nats，算 BPB。

### LM15-B03
同一字符串概率 $10^{-6}$，tokenizer A/B 分别用 2/6 tokens；算两者 token PPL。

## C. 推导与证明

### LM15-C01
从平均 NLL 推导 PPL 的几何平均概率倒数形式。

### LM15-C02
证明若完整字符串概率相同，改变 token 数可任意改变 token PPL。

### LM15-C03
说明 sliding-window 中“每个目标恰计一次”如何保证 denominator 不随重叠重复增长。

## D. 边界、反例与纠错

### LM15-D01
反驳“同 tokenizer 就可直接比较 PPL”，给三个协议差异。

### LM15-D02
反驳“BPB 对任意 tokenizer 都自动公平可算”。

### LM15-D03
反驳“pseudo-perplexity 低于 causal PPL，所以 MLM 的联合建模更好”。

## E. AI 迁移

### LM15-E01
设计长文档 sliding-window evaluator 的四条单元测试。

### LM15-E02
为两种多语言 tokenizer 设计兼顾 BPB、fertility 与下游质量的比较。

### LM15-E03
审计一个表格中模型 PPL 较低、但 tokenizer 和 EOS 规则均不同的结论。

独立完成后查看[[解答 - NLL、Perplexity、Bits-per-Byte 与 Tokenizer 公平比较]]。

