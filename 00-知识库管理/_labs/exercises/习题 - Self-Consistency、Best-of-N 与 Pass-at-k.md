---
type: exercise
status: verified
area: [language-models, reasoning, sampling]
topic: "[[Self-Consistency、Best-of-N 与 Pass-at-k]]"
solution: "[[解答 - Self-Consistency、Best-of-N 与 Pass-at-k]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Self-Consistency、Best-of-N 与 Pass-at-k

## A. 识别与复述

### LM38-A01
区分 self-consistency、pass-at-k 与 Best-of-N 的目标。

### LM38-A02
为什么 answer canonicalizer 属于估计器合同？

### LM38-A03
区分 oracle coverage、chosen success 与 selection regret。

## B. 手算与构造

### LM38-B01
五条答案 A,B,A,C,A；求 self-consistency 输出并说明其不保证正确。

### LM38-B02
独立单次正确率 0.6，三票多数正确概率是多少？

### LM38-B03
$n=5,c=2,k=3$，计算无放回 pass-at-k。

## C. 推导与证明

### LM38-C01
推导有放回 $1-(1-p)^k$。

### LM38-C02
推导固定池无放回组合估计式。

### LM38-C03
证明 chosen success 不超过 oracle coverage，并解释等号条件。

## D. 边界、反例与纠错

### LM38-D01
构造 pass-at-10 很高但用户 top-1 不改善的例子。

### LM38-D02
反驳“多数路径同意，所以答案经过概率校准”。

### LM38-D03
指出相关样本把 $N$ 夸大的原因，并用 $N_{eff}$ 作示意。

## E. AI 迁移

### LM38-E01
设计 oracle coverage、chosen accuracy 与 regret 的报告表。

### LM38-E02
设计答案/策略/首错位置三层多样性度量。

### LM38-E03
设计 token、verifier、latency 匹配的 anytime curve。

独立完成后查看[[解答 - Self-Consistency、Best-of-N 与 Pass-at-k]]。
