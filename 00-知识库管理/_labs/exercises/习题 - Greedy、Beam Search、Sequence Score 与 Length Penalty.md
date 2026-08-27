---
type: exercise
status: verified
area: [language-models, decoding]
topic: "[[Greedy、Beam Search、Sequence Score 与 Length Penalty]]"
solution: "[[解答 - Greedy、Beam Search、Sequence Score 与 Length Penalty]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Greedy、Beam Search、Sequence Score 与 Length Penalty

## A. 识别与复述

### LM50-A01
区分 greedy、beam search 与 exact sequence argmax。

### LM50-A02
区分 active beams 与 completed hypotheses。

### LM50-A03
解释 search error、model error 与 task-metric error。

## B. 手算与构造

### LM50-B01
首步 $p(A)=.6,p(B)=.4$；后续最优条件概率为 $p(x\mid A)=.5,p(y\mid B)=.9$。比较 greedy 与全局最佳两步序列。

### LM50-B02
候选序列 raw log-score 分别为 $s_1=-3$、长度 3；$s_2=-4$、长度 8。按 $s/|y|^{.7}$ 排序。

### LM50-B03
给 beam width 2 的一步候选分数 $(-.2,-.5,-1.3)$，第二步扩展分别为第一项 $(-.4,-1.0)$、第二项 $(-.1,-.3)$；写出累计分与保留项。

## C. 推导与证明

### LM50-C01
证明 greedy 等于 beam width 1，但不等于一般的序列 MAP。

### LM50-C02
证明最大化概率乘积等价于最大化 log-probability 之和。

### LM50-C03
说明 length normalization 为何可能改变 raw-probability argmax，并给反例。

## D. 边界、反例与纠错

### LM50-D01
反驳“beam 越宽，生成质量必然越好”。

### LM50-D02
审计“首个 EOS 出现就停止整个 beam search”的实现。

### LM50-D03
解释 exposure bias 为什么不等于 beam search 的错误。

## E. AI 迁移

### LM50-E01
为 beam decoder 设计逐步 trace schema。

### LM50-E02
设计 translation 与 open-ended story 上的 decoding 对照。

### LM50-E03
给在线系统写 beam width 的质量—成本选择规则。

独立完成后查看[[解答 - Greedy、Beam Search、Sequence Score 与 Length Penalty]]。
