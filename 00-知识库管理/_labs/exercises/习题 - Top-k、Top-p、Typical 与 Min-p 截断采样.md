---
type: exercise
status: verified
area: [language-models, decoding]
topic: "[[Top-k、Top-p、Typical 与 Min-p 截断采样]]"
solution: "[[解答 - Top-k、Top-p、Typical 与 Min-p 截断采样]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Top-k、Top-p、Typical 与 Min-p 截断采样

## A. 识别与复述

### LM51-A01
用统一 support-and-renormalize 形式写四种截断。

### LM51-A02
比较 top-$k$ 与 top-$p$ 的固定量和自适应量。

### LM51-A03
说明 locally typical 的 surprisal distance 与 min-$p$ 的相对阈值。

## B. 手算与构造

### LM51-B01
对降序概率 $(.34,.23,.16,.11,.07,.04,.03,.02)$，求 top-3 与 top-$p=.75$ support 并重归一化。

### LM51-B02
对同一分布与 min-$p$ 系数 $\alpha=.2$ 求阈值、support 和保留质量。

### LM51-B03
对概率 $(.5,.25,.125,.125)$ 计算熵 $H$（自然对数）及每个 token 的 $|{-\log p_i}-H|$ 排序。

## C. 推导与证明

### LM51-C01
证明截断重归一化后的概率和为 1，并写出被删质量。

### LM51-C02
构造 temperature 与 top-$p$ 不交换的具体数值例子。

### LM51-C03
证明 top-$p$ support 大小随分布平坦化可以增大，但无需对所有分布严格单调。

## D. 边界、反例与纠错

### LM51-D01
反驳“top-$k=50$ 在所有 prompt 上保留相同比例概率质量”。

### LM51-D02
为何“min-$p$ 有论文”不足以断言它普遍优于 top-$p$？

### LM51-D03
审计同时开启 top-$k$、top-$p$、min-$p$ 却不记录顺序的报告。

## E. AI 迁移

### LM51-E01
设计小词表 support 单元测试。

### LM51-E02
设计公平比较四种截断的多任务实验。

### LM51-E03
为在线系统设计 support-collapse 告警。

独立完成后查看[[解答 - Top-k、Top-p、Typical 与 Min-p 截断采样]]。
