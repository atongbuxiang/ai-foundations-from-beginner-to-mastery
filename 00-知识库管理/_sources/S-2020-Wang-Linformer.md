---
type: source
status: draft
area: [sources, ai/transformers, low-rank-attention]
source_type: paper
title: "Linformer: Self-Attention with Linear Complexity"
author: "Sinong Wang et al."
year: 2020
url: "https://arxiv.org/abs/2006.04768"
accessed: 2026-08-24
source_tier: A
license: "arXiv; independent summary only"
scope_role: method-paper
related: ["[[低秩投影与序列维压缩 Attention]]", "[[Attention 矩阵的秩、瓶颈与有效秩]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Linformer：沿序列轴压缩 K/V

> [!abstract] 来源定位
> Linformer 以投影把 K/V 的长度轴从 $n$ 压到 $k$，将 pairwise attention 变为 $n\times k$。线性长度成本以 $k$ 固定或缓慢增长为前提。

## 调用边界

- 参数投影、共享策略和最大长度会影响形状与泛化；
- 对 softmax attention matrix 的低秩观察和近似保证须保留论文假设；
- 小 singular tail 不自动保证最终输出误差小，仍受 V、softmax 和下游条件影响。
