---
type: source
status: active
area: [sources, learning-theory, finite-mixtures, identifiability]
source_type: paper
title: "Identifiability of Finite Mixtures"
author: [Henry Teicher]
year: 1963
url: "https://doi.org/10.1214/aoms/1177703862"
accessed: 2026-08-23
source_tier: A
license: "Annals of Mathematical Statistics article; retain citation"
venue: "Annals of Mathematical Statistics 34(4), 1265–1269"
scope_role: primary
temporal_role: classical-foundation
related: ["[[潜变量模型、混合模型与 EM]]", "[[模型可辨识性、选择与 Misspecification]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Identifiability of Finite Mixtures

> [!abstract] 来源定位
> Teicher研究有限 mixture distribution何时能由 observed mixture law识别 component family与mixing measure。本库用它区分 distribution identifiability、label permutation、finite-sample estimability与algorithm recovery。

## 本库调用

1. mixture identifiability是 parameter-to-distribution map 的性质；
2. component labels通常只可识别到 permutation；
3. 某些 finite normal/gamma mixture family在明确条件下可辨识；
4. identifiability不排除 likelihood singularity、weak separation或困难优化；
5. posterior responsibilities不是已观测“真实类别”的自动证明。
