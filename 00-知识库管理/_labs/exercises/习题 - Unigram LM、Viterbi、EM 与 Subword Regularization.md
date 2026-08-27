---
type: exercise
status: verified
area: [language-models, tokenization, unigram-lm]
topic: "[[Unigram LM、Viterbi、EM 与 Subword Regularization]]"
solution: "[[解答 - Unigram LM、Viterbi、EM 与 Subword Regularization]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Unigram LM、Viterbi、EM 与 Subword Regularization

## A. 识别与复述

### LM06-A01
区分路径概率、字符串边缘概率与路径后验。

### LM06-A02
Viterbi、forward 与 sampling 分别输出什么？

### LM06-A03
为什么 Unigram tokenizer 的独立假设不是 Transformer LM 的独立假设？

## B. 手算与构造

### LM06-B01
$p(a)=.4,p(b)=.3,p(ab)=.2$，算 `ab` 的 marginal、MAP 与两路径后验。

### LM06-B02
词表 `a:.5, aa:.3`，枚举 `aa` 路径并算 Viterbi cost $-\log p$。

### LM06-B03
对上题 $\alpha=.5$ 的温度化采样，算两路径未归一权重和概率。

## C. 推导与证明

### LM06-C01
推导 forward recurrence 与 edge posterior $\gamma_{ij}$。

### LM06-C02
由期望完整数据 log-likelihood 推导固定词表的 M-step 归一化更新。

### LM06-C03
证明 marginal NLL 不大于 MAP path NLL。

## D. 边界、反例与纠错

### LM06-D01
反驳“Viterbi 概率就是字符串概率”。

### LM06-D02
反驳“$\alpha\to0$ 时每个 token 均匀”。

### LM06-D03
构造 coverage hole 并说明 forward/log-space 会返回什么。

## E. AI 迁移

### LM06-E01
设计枚举小 lattice 的 sampling oracle。

### LM06-E02
审计“subword regularization 提升鲁棒性”的实验。

### LM06-E03
说明词表 pruning 需记录哪些效用、覆盖与 held-out 指标。

独立完成后查看[[解答 - Unigram LM、Viterbi、EM 与 Subword Regularization]]。

