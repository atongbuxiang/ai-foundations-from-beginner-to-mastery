---
type: exercise
status: verified
area: [language-models, span-corruption, t5]
topic: "[[Span Corruption、Sentinel Token 与 T5 Seq2Seq 目标]]"
solution: "[[解答 - Span Corruption、Sentinel Token 与 T5 Seq2Seq 目标]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Span Corruption、Sentinel Token 与 T5 Seq2Seq 目标

## A. 识别与复述

### LM12-A01
列出 sentinel 的占位、配对、分隔与生成控制四种角色。

### LM12-A02
为什么 span corruption 不只是“连续多个 `[MASK]`”？

### LM12-A03
分别说明 encoder self、decoder self、cross-attention 的 relation。

## B. 手算与构造

### LM12-B01
对 `a b c d e f g` 删除 `[b,c]` 与 `[f]`，构造 source 与 target。

### LM12-B02
$T=100$、删除 $N=15$ tokens、形成 $K=5$ spans；忽略 EOS，算 source 与 target 近似长度。

### LM12-B03
给 target `[s0,b,c,s1,f,s2,EOS]`，写 decoder inputs/labels 的 shift。

## C. 推导与证明

### LM12-C01
证明在 sentinel 唯一、顺序一致且 target 边界完备时 source–target 可重建 clean sequence。

### LM12-C02
推导 $L_{source}=T-N+K$，并给 target 长度公式的约定依赖。

### LM12-C03
写出 span-corruption 总体风险对 clean data、span sampler 与 decoder target 的三层期望。

## D. 边界、反例与纠错

### LM12-D01
构造重复使用同一 sentinel 导致 target 对齐歧义的例子。

### LM12-D02
指出截断 source/target 可能制造的三种不可逆错误。

### LM12-D03
反驳“15% noise density 相同就代表两个 T5 corruption 任务相同”。

## E. AI 迁移

### LM12-E01
为 span sampler 与 reconstruct 函数设计六条 property tests。

### LM12-E02
分析平均 span 长度对 encoder/decoder FLOPs 和训练信号粒度的影响。

### LM12-E03
审计一个中文 T5 复现只写“沿用 T5 objective”而未给 tokenizer/sentinel/sampler 配置。

独立完成后查看[[解答 - Span Corruption、Sentinel Token 与 T5 Seq2Seq 目标]]。

