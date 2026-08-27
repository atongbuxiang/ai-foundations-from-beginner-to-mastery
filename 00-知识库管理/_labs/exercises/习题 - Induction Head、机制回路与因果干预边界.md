---
type: exercise
status: verified
area: [language-models, mechanistic-interpretability, induction-heads]
topic: "[[Induction Head、机制回路与因果干预边界]]"
solution: "[[解答 - Induction Head、机制回路与因果干预边界]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Induction Head、机制回路与因果干预边界

## A. 识别与复述

### LM36-A01
定义 prefix matching 与 copying 两项 induction criterion。

### LM36-A02
区分 QK 路径与 OV 路径。

### LM36-A03
区分 necessity、sufficiency、mediation 与 redundancy。

## B. 手算与构造

### LM36-B01
对序列 A B C A ? 标出 current A、earlier A、被复制 B。

### LM36-B02
给一个只高 attention 但对 B logit 为负贡献的反例。

### LM36-B03
构造 repeated-random-token 的最小 clean/corrupted/patch 实验。

## C. 推导与证明

### LM36-C01
从 attention 输出与 unembedding 写 direct logit contribution。

### LM36-C02
解释 previous-token head 与 induction head 怎样组合实现 AB…A→B。

### LM36-C03
证明单头消融小不推出该头没有功能。

## D. 边界、反例与纠错

### LM36-D01
反驳“注意力图就是模型解释”。

### LM36-D02
反驳“两层 attention-only 精确回路证明所有大模型 ICL”。

### LM36-D03
指出零向量 ablation 的分布外风险并给替代对照。

## E. AI 迁移

### LM36-E01
设计 prefix/copy scores 与 matched control heads 的分析。

### LM36-E02
设计 ablation、activation patch 和路径恢复比例报告。

### LM36-E03
为“某 head 负责翻译 ICL”写一份证据升级路线。

独立完成后查看[[解答 - Induction Head、机制回路与因果干预边界]]。
