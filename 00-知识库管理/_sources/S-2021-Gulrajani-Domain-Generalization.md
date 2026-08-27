---
type: source
status: active
area: [sources, domain-generalization, benchmarking]
source_type: paper
title: "In Search of Lost Domain Generalization"
author: [Ishaan Gulrajani, David Lopez-Paz]
year: 2021
url: "https://openreview.net/forum?id=lQdXeXDoWtI"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and benchmark conditions"
venue: "ICLR 2021"
scope_role: primary
temporal_role: benchmark-audit
related: ["[[Domain Adaptation 与 Domain Generalization Bound]]"]
created: 2026-08-23
updated: 2026-08-23
---

# In Search of Lost Domain Generalization

> [!abstract] 来源定位
> 在统一实现、数据增强和 model-selection protocol 下重评 domain-generalization algorithms，强调简单 ERM 基线与选择规则。本库调用其 benchmark hygiene；不把有限 benchmarks 的排序外推为 DG 不可能或普遍方法定理。

## 本库调用

1. domain-balanced sampling 与 augmentation；
2. target-domain validation 会泄漏 DG setting；
3. oracle selection 与 IID/source validation 必须分账；
4. search budget 和 implementation quality 可改变排名；
5. 多目标域/重复 seeds 与负结果同样报告。
