---
type: source
status: verified
area: [sources, minhash, document-similarity, deduplication]
source_type: paper
title: "On the Resemblance and Containment of Documents"
author: "Andrei Z. Broder"
year: 1997
url: "https://doi.org/10.1109/SEQUEN.1997.666900"
accessed: 2026-08-26
source_tier: P1
license: "IEEE paper; independent summary and formulas"
scope_role: minhash-foundation
temporal_role: foundational
related: ["[[精确去重、MinHash、LSH 与近重复检测]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Broder：文档 resemblance 与 containment

> [!abstract] 来源定位
> 论文把文档转为 fingerprint/shingle 集合，以 Jaccard resemblance 和 containment 表达近重复，并用随机最小值签名估计。课程从 $\Pr[h_{min}(A)=h_{min}(B)]=J(A,B)$ 推导 MinHash，再单独分析 LSH candidate recall。

Shingle 定义、set/multiset、canonicalization 和短文档边界先于 hash；随机碰撞、有限签名与 LSH 只提供概率候选，不是 exact equivalence proof。

