---
type: source
status: verified
area: [sources, masked-language-modeling, pseudo-likelihood, evaluation]
source_type: paper
title: "Masked Language Model Scoring"
author: "Julian Salazar, Davis Liang, Toan Q. Nguyen, Katrin Kirchhoff"
year: 2020
url: "https://arxiv.org/abs/1910.14659"
accessed: 2026-08-26
source_tier: P1
license: "论文；本库保存独立摘要、公式与链接"
scope_role: primary
temporal_role: pseudo-log-likelihood
related: ["[[Masked LM 的 Corruption Law、伪似然与 BERT]]", "[[NLL、Perplexity、Bits-per-Byte 与 Tokenizer 公平比较]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Masked Language Model Scoring

> [!abstract] 来源定位
> 论文用逐位置 mask 的 pseudo-log-likelihood (PLL) 为 MLM 序列评分。课程用它区分“随机 corruption 下的训练 loss”与“把每个位置依次 mask 的派生评分”；PLL 不自动成为规范化 joint log-likelihood。

$$
PLL(x)=\sum_{i=1}^{T}\log p_\theta(x_i\mid x_{-i}).
$$

计算通常需要 $T$ 次 masked forward 或专门近似。Pseudo-perplexity 的 denominator 与 tokenizer 仍需声明；不同条件分布族未必兼容于同一个全局 joint distribution。

