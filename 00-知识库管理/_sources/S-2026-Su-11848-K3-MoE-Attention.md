---
type: source
status: draft
area: [sources, scientific-spaces, moe, contemporary-architecture]
source_type: blog
title: "简单谈谈K3的MoE和Attention"
author: "苏剑林"
year: 2026
url: "https://spaces.ac.cn/archives/11848"
accessed: 2026-08-24
source_tier: C
license: "Science Space; independent notes, no article mirroring"
scope_role: contemporary-system-report
related: ["[[细粒度专家、共享专家与动态激活]]", "[[MoE 门控归一化、证据地图与开放问题]]", "[[MLA、潜变量缓存与推理成本证据]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 科学空间：K3 的 Stable LatentMoE 与 QB

> [!abstract] 来源定位
> 文章报告 K3 采用 Stable LatentMoE、RMSNorm 稳定化、Quantile Balancing 与分桶近似全局 quantile，并解释 896 选 16 下的工程取舍。

## Claim audit

- 这是模型开发者的当代系统说明 `E/H`，不是独立 benchmark 或通用配方；
- RMSNorm 的稳定/benchmark 作用和“平衡 shared/routed 比例”分别是观察与机制猜测；
- histogram quantile 的 bin 数、通信收益与均衡效果限定 K3 分布、规模和基础设施。
