---
type: source
status: verified
area: [sources, tokenization, unigram-lm, nlp]
source_type: paper
title: "Subword Regularization: Improving Neural Network Translation Models with Multiple Subword Candidates"
author: "Taku Kudo"
year: 2018
url: "https://arxiv.org/abs/1804.10959"
accessed: 2026-08-26
source_tier: P1
license: "论文；本库仅保存独立摘要、公式与链接"
scope_role: foundational
temporal_role: unigram-subword
related: ["[[Unigram LM、Viterbi、EM 与 Subword Regularization]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Kudo：Unigram LM 与 Subword Regularization

> [!abstract] 来源定位
> 论文把分段视为潜变量，提出 unigram language model tokenizer，并在训练时从多个子词分段中采样作为正则。课程用它建立 lattice、Viterbi、边缘似然、EM/剪枝和分段采样的统一概率对象。

给字符串 $x$ 的合法分段集合 $\mathcal S(x)$，码本概率为 $p(v)$，则

$$
p(x)=\sum_{s\in\mathcal S(x)}\prod_{v\in s}p(v).
$$

Viterbi 最大化路径乘积；forward algorithm 计算路径和；sampling 从某个温度化后验抽路径。三者不能静默互换。原论文下游改进是 NMT 设置下的实验结论，不是所有 LM 的普遍定理。

