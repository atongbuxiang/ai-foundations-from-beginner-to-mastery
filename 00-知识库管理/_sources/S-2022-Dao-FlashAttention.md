---
type: source
status: verified
area: [sources, ai/transformers, flashattention, io]
source_type: paper
title: "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness"
author: "Tri Dao et al."
year: 2022
url: "https://arxiv.org/abs/2205.14135"
accessed: 2026-08-24
source_tier: A
license: "arXiv; independent summary only"
scope_role: algorithm-paper
related: ["[[FlashAttention、精确计算与 IO Awareness]]", "[[Attention 的二次复杂度、内存与 IO 瓶颈]]"]
created: 2026-08-24
updated: 2026-08-26
---

# FlashAttention：Tiling、Online Softmax 与 HBM IO

> [!abstract] 来源定位
> FlashAttention 通过 tiling 和 online softmax 避免把完整 $n\times n$ scores/weights 写回 HBM，在目标算术语义下计算 exact attention，并分析两级存储模型的 IO。

## 调用边界

- “exact”指无模型近似，不是 bitwise 与所有实现相同；
- 算术 pair 数仍为二次，峰值中间存储和 HBM traffic 可显著降低；
- 论文速度数字限定 GPU、shape、版本与 end-to-end 协议。

## 核验记录

- 2026-08-26 核对 arXiv:2205.14135 v2 元数据：标题、五位作者、首次提交日期 2022-05-27；
- 摘要明确把方法定位为利用 tiling 减少 HBM↔SRAM 读写的 IO-aware exact attention；
- 本课程不把论文在特定 BERT/GPT-2/LRA 设置下的速度倍数外推到任意推理服务。
