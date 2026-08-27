---
type: source
status: draft
area: [sources, scientific-spaces, transformer-vq]
source_type: blog
title: "VQ一下Key，Transformer的复杂度就变成线性了"
author: "苏剑林"
year: 2023
url: "https://spaces.ac.cn/archives/9844"
accessed: 2026-08-24
source_tier: C
license: "Science Space; independent notes, no article mirroring"
scope_role: method-explanation
related: ["[[局部、分块与稀疏 Attention]]", "[[核特征、线性 Attention 与结合律重排]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 科学空间：Transformer-VQ 的线性化入口

> [!abstract] 来源定位
> 文章从 key 聚类解释为何相同 codeword 的 softmax 项可聚合，并强调 causal cache/未来泄漏接口。误差可定位到 $K\to\hat K$ 的量化。

## Claim audit

- 按 codebook 聚合的代数重排为 `I`；
- 量化后不是原 dense-key attention；
- codebook=512、速度与任务结果为原论文设置下 `E`，不推广为所有 VQ attention。
