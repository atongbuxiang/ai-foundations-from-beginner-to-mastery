---
type: source
status: active
area: [sources, neural-networks, language-modeling, weight-tying]
source_type: paper
title: "Using the Output Embedding to Improve Language Models"
author: "Ofir Press; Lior Wolf"
year: 2017
url: "https://aclanthology.org/E17-2025/"
venue: "EACL 2017"
accessed: 2026-08-29
source_tier: A
license: "ACL Anthology paper；本库仅保存独立摘要、必要公式与链接"
scope_role: core
temporal_role: foundational
related: ["[[输入—输出权重共享与 Weight Tying]]", "[[Softmax 输出层、Logit 尺度与概率参数化]]"]
created: 2026-08-24
updated: 2026-08-29
---

# Press、Wolf：Output Embedding 与 Weight Tying

> [!abstract] 来源定位
> 论文分析语言模型 output weight matrix 作为词向量的性质，比较 tied/untied 更新规则，并在当时的 RNN 语言模型与翻译设置中报告参数减少和 perplexity 改善。它是输入—输出 tying 的经典原始来源；本库补齐现代矩阵 shape、共享梯度相加、projection 与 optimizer state 边界。

## 核心结构

若输入表 $E\in\mathbb R^{V\times d}$、输出矩阵 $U\in\mathbb R^{V\times d}$，direct tying 施加

$$
U=E.
$$

同一参数既被 lookup 使用，又作为全部类别的输出 prototypes。共享后的梯度是所有使用位置的 VJP 之和，不是只保留输入或输出其中一条。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| PW-C1 | tying 可减少一个词表规模矩阵 | 计数 | 输入/输出词表和维度对齐 | 精确 |
| PW-C2 | tied update 同时受 input/output 使用影响 | 计算图 | 同一 Parameter 对象 | 精确 |
| PW-C3 | tying 对所有语言模型都改善 perplexity | 经验外推 | 架构、tokenizer、scale 与调参依赖 | 原论文不足以支持 |
| PW-C4 | tying 不改变函数类，只省内存 | 结构误读 | $U=E$ 是参数约束 | 错误 |
