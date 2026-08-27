---
type: source
status: active
area: [sources, domain-adaptation, h-delta-h]
source_type: paper
title: "A Theory of Learning from Different Domains"
author: [Shai Ben-David, John Blitzer, Koby Crammer, Alex Kulesza, Fernando Pereira, Jennifer Wortman Vaughan]
year: 2010
url: "https://doi.org/10.1007/s10994-009-5152-4"
accessed: 2026-08-23
source_tier: A
license: "Scholarly source; retain citation and theorem conditions"
venue: "Machine Learning"
scope_role: primary
temporal_role: foundational
related: ["[[Domain Adaptation 与 Domain Generalization Bound]]"]
created: 2026-08-23
updated: 2026-08-23
---

# A Theory of Learning from Different Domains

> [!abstract] 来源定位
> 建立 source risk、$\mathcal H\Delta\mathcal H$ divergence 与 joint ideal error $\lambda$ 的经典 domain-adaptation bound。本库完整保留不可观测 $\lambda$；不把低域分类准确率单独写成 target-risk 保证。

## 本库调用

1. hypothesis-class-relative distribution divergence；
2. disagreement triangle proof；
3. $R_T(h)\le R_S(h)+\frac12d_{\mathcal H\Delta\mathcal H}+\lambda$；
4. empirical divergence 还含 finite-sample complexity；
5. shared good hypothesis 是不可省略的 task-compatibility 条件。
