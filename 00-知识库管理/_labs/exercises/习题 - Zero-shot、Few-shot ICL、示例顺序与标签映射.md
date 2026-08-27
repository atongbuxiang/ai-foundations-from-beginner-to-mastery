---
type: exercise
status: verified
area: [language-models, in-context-learning, demonstrations]
topic: "[[Zero-shot、Few-shot ICL、示例顺序与标签映射]]"
solution: "[[解答 - Zero-shot、Few-shot ICL、示例顺序与标签映射]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Zero-shot、Few-shot ICL、示例顺序与标签映射

## A. 识别与复述

### LM34-A01
给出 zero-shot、one-shot、few-shot 与 ICL 的操作定义。

### LM34-A02
列出 demonstration 同时传递的六类信息。

### LM34-A03
区分 deployment parameter update 与 prompt-conditioned activation/state change。

## B. 手算与构造

### LM34-B01
四种排列准确率 0.8、0.7、0.5、0.4；计算均值、中位数、范围与最好值。

### LM34-B02
$K=4$ 和 $K=8$ 各有多少排列？说明何时可枚举。

### LM34-B03
构造 positive/negative 到 A/B 的一致 label permutation 测试。

## C. 推导与证明

### LM34-C01
形式化 permutation equivariance success，并说明它测什么。

### LM34-C02
说明“随机 labels 仍有效”为什么不推出正确映射永远无用。

### LM34-C03
推导从测试集选最佳顺序为何改变 estimand。

## D. 边界、反例与纠错

### LM34-D01
构造 few-shot 提升完全来自答案格式而非 input-label mapping 的反例。

### LM34-D02
反驳“示例集合相同，所以顺序不应影响 causal LM”。

### LM34-D03
审计一个 semantic retrieval 选择 demos 却未报告 encoder/index 的实验。

## E. AI 迁移

### LM34-E01
设计 correct/random/permuted-label 与 format-only 的因子实验。

### LM34-E02
给长 prompt 设计固定 $K$ 与固定 token budget 两套对照。

### LM34-E03
写一份 demonstration selector 的训练—验证—测试隔离协议。

独立完成后查看[[解答 - Zero-shot、Few-shot ICL、示例顺序与标签映射]]。
