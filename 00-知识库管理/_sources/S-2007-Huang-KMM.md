---
type: source
status: active
area: [sources, covariate-shift, kernel-mean-matching]
source_type: paper
title: "Correcting Sample Selection Bias by Unlabeled Data"
author: [Jiayuan Huang, Arthur Gretton, Karsten M. Borgwardt, Bernhard Schölkopf, Alexander J. Smola]
year: 2007
url: "https://papers.nips.cc/paper_files/paper/2006/hash/a2186aa7c086b46ad4e8bf81e2a3a19b-Abstract.html"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and kernel/overlap conditions"
venue: "NeurIPS 2006 proceedings"
scope_role: primary
temporal_role: foundational-method
related: ["[[重要性加权与 Covariate Shift 校正]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Correcting Sample Selection Bias by Unlabeled Data

> [!abstract] 来源定位
> 用 kernel mean matching 直接寻找 source sample weights，使加权 source feature mean 接近 unlabeled target。本库调用其 moment-matching route；有限 kernel features 的匹配不等于完整联合分布或条件机制相同。

## 本库调用

1. 无需分别估计两个高维 densities；
2. RKHS mean matching 与 weight constraints；
3. kernel richness、sample size 与 regularization 控制可辨信息；
4. weights clipping/bounds 改变 bias–variance；
5. label mechanism stability 仍是外部假设。
