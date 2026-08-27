---
type: exercise
status: verified
area: [language-models, prefix-lm, unilm]
topic: "[[Prefix LM、UniLM 与序列到序列 Mask 合同]]"
solution: "[[解答 - Prefix LM、UniLM 与序列到序列 Mask 合同]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Prefix LM、UniLM 与序列到序列 Mask 合同

## A. 识别与复述

### LM13-A01
解释 Prefix LM relation 的四个块。

### LM13-A02
为什么“共享一个 Transformer”不等于“目标相同”？

### LM13-A03
比较单栈 Prefix LM 与 encoder–decoder 的 source、target 信息路径。

## B. 手算与构造

### LM13-B01
$P=2,S=3$，以 query 为行写 $5\times5$ relation。

### LM13-B02
对 `[s1,s2,SEP,BOS,y1,y2,EOS]` 标出为预测 `y1,y2,EOS` 所需的 logit positions 与 loss mask。

### LM13-B03
把 $P=0$ 与 $S=0$ 代入块 relation，解释退化情形及哪些目标失去定义。

## C. 推导与证明

### LM13-C01
证明 Prefix LM relation 下 prefix hidden states 不依赖 target token。

### LM13-C02
说明该 relation 足以参数化 $p(y\mid x)=\prod_s p(y_s\mid x,y_{<s})$。

### LM13-C03
推导 packed 两样本时 relation 应如何与 document block relation 取交集。

## D. 边界、反例与纠错

### LM13-D01
构造矩阵轴转置导致 source 读取 target 的泄漏。

### LM13-D02
反驳“prompt labels ignore 后，prompt 可见性怎样都无所谓”。

### LM13-D03
指出整串机械 shift 并全部计分如何偷偷加入 source LM loss。

## E. AI 迁移

### LM13-E01
设计四条 Prefix LM metamorphic tests。

### LM13-E02
分析 prefix prefill 与增量 suffix decoding 的 KV cache 合同。

### LM13-E03
审计“UniLM 统一三类目标，因此三类目标等价”的论证。

独立完成后查看[[解答 - Prefix LM、UniLM 与序列到序列 Mask 合同]]。

