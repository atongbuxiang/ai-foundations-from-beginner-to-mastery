---
type: exercise
status: verified
area: [language-models, peft, adapters, prompts, ia3]
topic: "[[Adapter、Prompt Tuning、Prefix Tuning 与 IA3]]"
solution: "[[解答 - Adapter、Prompt Tuning、Prefix Tuning 与 IA3]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Adapter、Prompt Tuning、Prefix Tuning 与 IA3

## A. 识别与复述

### LM31-A01
五类 PEFT 分别修改输入、权重、模块、KV 还是通道？

### LM31-A02
Prompt tuning 与 prefix tuning 的注入深度有何不同？

### LM31-A03
为什么 trainable parameter 少不等于 serving 成本低？

## B. 手算与构造

### LM31-B01
$d=100,L=4,p=5,r=2$，算 prompt、per-layer KV prefix、每层一个 adapter 的参数。

### LM31-B02
写 bottleneck adapter 前向并核对形状。

### LM31-B03
给 $K,V,h_{ff}$ 与三个 scaling vectors，写 IA3 广播后的张量形状。

## C. 推导与证明

### LM31-C01
证明无非线性 adapter 在受限结构下可折为线性更新，并说明一般边界。

### LM31-C02
推导 prefix 增加的每层 KV 元素数。

### LM31-C03
说明相同参数量为何不推出相同函数族。

## D. 边界、反例与纠错

### LM31-D01
反驳“soft prompt 是一段可读自然语言”。

### LM31-D02
反驳“IA3 只学向量，所以功能变化一定小”。

### LM31-D03
指出动态多任务 serving 中 LoRA/Prefix/Adapter 的不同瓶颈。

## E. AI 迁移

### LM31-E01
设计五类 PEFT 的参数—显存—延迟—质量矩阵。

### LM31-E02
为 prompt/prefix 写 context 与 KV cache 审计。

### LM31-E03
审计只比较默认超参数单点的 PEFT 排名。

独立完成后查看[[解答 - Adapter、Prompt Tuning、Prefix Tuning 与 IA3]]。

