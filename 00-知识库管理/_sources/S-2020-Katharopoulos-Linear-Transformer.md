---
type: source
status: draft
area: [sources, ai/transformers, linear-attention]
source_type: paper
title: "Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention"
author: "Angelos Katharopoulos et al."
year: 2020
url: "https://arxiv.org/abs/2006.16236"
accessed: 2026-08-24
source_tier: A
license: "arXiv; independent summary only"
scope_role: method-paper
related: ["[[核特征、线性 Attention 与结合律重排]]", "[[状态空间的递推—卷积对偶与并行扫描]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Linear Transformer：Kernel Feature 与递归状态

> [!abstract] 来源定位
> 将非负相似度写成 $\phi(q)^\top\phi(k)$ 后，可先累计 $S=\sum\phi(k)v^\top$ 与 $z=\sum\phi(k)$；causal 版本成为固定维递推状态。

## 调用边界

- 结合律是 `I`，但相似度替换通常改变模型；
- 分母必须保留并审计接近零的数值情形；
- causal 训练的顺序状态需要 scan/kernel 才能同时获得并行和内存优势。
