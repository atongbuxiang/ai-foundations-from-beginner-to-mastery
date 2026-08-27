---
type: source
status: active
area: [sources, domain-adaptation, invariant-representation]
source_type: paper
title: "On Learning Invariant Representations for Domain Adaptation"
author: [Han Zhao, Rémi Tachet des Combes, Kun Zhang, Geoffrey J. Gordon]
year: 2019
url: "https://proceedings.mlr.press/v97/zhao19a.html"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and impossibility conditions"
venue: "ICML 2019"
scope_role: primary
temporal_role: critical-boundary
related: ["[[Domain Adaptation 与 Domain Generalization Bound]]", "[[OOD、鲁棒性与因果不变性的边界]]"]
created: 2026-08-23
updated: 2026-08-23
---

# On Learning Invariant Representations for Domain Adaptation

> [!abstract] 来源定位
> 说明在 label distributions 等不兼容条件下，强行匹配 invariant representations 可能增加 target error。本库用它约束“domain indistinguishable ⇒ transfer good”的误推；结论需按设定和 divergence 解读。

## 本库调用

1. input/representation invariance 与 label prediction 的张力；
2. label-marginal mismatch 可使对齐产生错误配对；
3. domain discrepancy 小并不足够；
4. task compatibility/conditional alignment 不可省；
5. representation map 可同时删除 domain 与 label information。
