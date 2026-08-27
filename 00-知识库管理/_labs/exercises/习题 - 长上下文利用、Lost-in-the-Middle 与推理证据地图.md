---
type: exercise
status: verified
area: [language-models, long-context, evaluation]
topic: "[[长上下文利用、Lost-in-the-Middle 与推理证据地图]]"
solution: "[[解答 - 长上下文利用、Lost-in-the-Middle 与推理证据地图]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - 长上下文利用、Lost-in-the-Middle 与推理证据地图

## A. 识别与复述

### LM40-A01
区分 declared、trained、numerically supported 与 effective context。

### LM40-A02
区分 single retrieval、multi-needle、multi-hop 与 aggregation。

### LM40-A03
Lost-in-the-Middle 提供的是哪类证据，不提供什么机制结论？

## B. 手算与构造

### LM40-B01
给定某任务在 8K/16K/32K 的最坏位置准确率 0.9/0.82/0.68，阈值 0.8；求保守 $T_{eff}$。

### LM40-B02
构造长度固定但 evidence position 为 start/middle/end 的三份样本。

### LM40-B03
构造固定 $K$ 改长度和固定长度改 $K$ 两个 ICL 对照。

## C. 推导与证明

### LM40-C01
形式化 $A(T,r,q,d)$ 与基于最坏位置的 $T_{eff}$。

### LM40-C02
说明 declared context 不推出 effective context。

### LM40-C03
说明 single-needle 满分不推出 multi-hop/aggregation 满分。

## D. 边界、反例与纠错

### LM40-D01
反驳“观察 U 形曲线就证明 RoPE 是原因”。

### LM40-D02
构造字符长度相同但 tokenizer token 长度不同的比较失败。

### LM40-D03
审计只在末尾放 needle、只报声明上限平均数的评测。

## E. AI 迁移

### LM40-E01
设计 length × position × task × distractor 完整矩阵。

### LM40-E02
为 synthetic RULER 与真实长文 QA 写互补证据协议。

### LM40-E03
写长上下文模型的 tokenizer、位置缩放、kernel、KV 与 truncation manifest。

独立完成后查看[[解答 - 长上下文利用、Lost-in-the-Middle 与推理证据地图]]。
