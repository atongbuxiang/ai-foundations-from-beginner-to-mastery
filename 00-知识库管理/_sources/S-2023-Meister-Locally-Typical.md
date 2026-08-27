---
type: source
status: verified
area: [sources, language-models, sampling]
source_type: paper
title: "Locally Typical Sampling"
author: "Clara Meister; Tiago Pimentel; Gian Wiher; Ryan Cotterell"
year: 2023
url: "https://aclanthology.org/2023.tacl-1.7/"
accessed: 2026-08-26
source_tier: P1
license: "TACL paper; independent summary"
scope_role: typical-decoding
related: ["[[Top-k、Top-p、Typical 与 Min-p 截断采样]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Locally Typical Sampling：局部信息量接近条件熵

> [!abstract] 来源定位
> 论文按 token surprisal $-\log p(v)$ 与当前条件熵的偏差构造候选集合，再重归一化采样。课程采用其明确定义，并与只按概率名次/累计质量截断的方法比较。

“典型”是相对于模型当前分布的局部信息论条件，不等同于世界事实、人工自然度或全序列典型集。
