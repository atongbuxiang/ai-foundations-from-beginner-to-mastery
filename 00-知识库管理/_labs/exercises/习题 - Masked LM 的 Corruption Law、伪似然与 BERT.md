---
type: exercise
status: verified
area: [language-models, masked-language-modeling, pseudo-likelihood]
topic: "[[Masked LM 的 Corruption Law、伪似然与 BERT]]"
solution: "[[解答 - Masked LM 的 Corruption Law、伪似然与 BERT]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Masked LM 的 Corruption Law、伪似然与 BERT

## A. 识别与复述

### LM11-A01
区分 clean sequence、mask set、corrupted input 与 targets。

### LM11-A02
为什么 `[MASK]` 出现位置不等于全部 loss 位置？

### LM11-A03
区分随机 MLM risk、PLL 与 normalized joint likelihood。

## B. 手算与构造

### LM11-B01
长度 100 序列按 BERT 15%×80/10/10 的期望，分别有多少 mask、random、unchanged target？

### LM11-B02
对 `the red fox` 构造逐位置 PLL 的三个 corrupted inputs，并写总分公式。

### LM11-B03
两个样本 masked token 数为 1 与 4、总 NLL 为 2 与 4；比较 per-example mean 后平均与全 token mean。

## C. 推导与证明

### LM11-C01
推导固定 corrupted context 下 log loss 的总体最优条件分布。

### LM11-C02
说明多位置同时 mask 时，最优条件为何一般不同于 $p(X_i\mid X_{-i})$。

### LM11-C03
写出二元变量条件 odds ratio 的兼容性约束，并解释任意神经条件表未必满足它。

## D. 边界、反例与纠错

### LM11-D01
反驳“BERT 的 80/10/10 就是 MLM 的定义”。

### LM11-D02
反驳“pseudo-perplexity 与 causal perplexity 数值可直接比较”。

### LM11-D03
指出动态 mask 验证集未固定 seed 对模型选择的影响。

## E. AI 迁移

### LM11-E01
为 MLM collator 设计五条 property tests。

### LM11-E02
比较 subword-independent mask 与 whole-word mask 对中文/英文 fertility 的潜在影响。

### LM11-E03
审计“MLM 准确率高，所以模型获得规范化文本联合分布”的主张。

独立完成后查看[[解答 - Masked LM 的 Corruption Law、伪似然与 BERT]]。

