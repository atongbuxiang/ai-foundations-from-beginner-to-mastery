---
type: source
status: draft
area: [sources, scientific-spaces, sparse-attention]
source_type: blog
title: "为节约而生：从标准Attention到稀疏Attention"
author: "苏剑林"
year: 2019
url: "https://spaces.ac.cn/archives/6853"
accessed: 2026-08-24
source_tier: C
license: "Science Space; independent notes, no article mirroring"
scope_role: intuition-and-implementation-bridge
related: ["[[局部、分块与稀疏 Attention]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 科学空间：从标准 Attention 到稀疏 Attention

> [!abstract] 来源定位
> 文章以 attention matrix/关联图解释 local、atrous 与 sparse pattern，并明确指出：在 dense 矩阵上只做 mask 功能正确，却不自动省时省显存；真正收益需要稀疏 kernel。

## Claim audit

- Pattern 的 edge 数与局部/膨胀关系可独立复算为 `I`；
- Keras/CUDA 的速度现象为当时实现下的 `E`；
- “多数任务主要局部相关”是归纳偏置直觉 `H`，不能替代任务消融。
