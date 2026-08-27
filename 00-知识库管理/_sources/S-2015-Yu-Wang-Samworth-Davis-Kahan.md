---
type: source
status: active
area: [sources, learning-theory, pca, eigenspace-perturbation]
source_type: paper
title: "A Useful Variant of the Davis–Kahan Theorem for Statisticians"
author: [Yi Yu, Tengyao Wang, Richard J. Samworth]
year: 2015
url: "https://doi.org/10.1093/biomet/asv008"
accessed: 2026-08-23
source_tier: A
license: "Biometrika article; retain citation and independent derivations"
venue: "Biometrika 102(2), 315–323"
scope_role: primary
temporal_role: classical-foundation
related: ["[[PCA 的统计估计与主子空间风险]]", "[[特征向量与子空间扰动定理]]"]
created: 2026-08-23
updated: 2026-08-23
---

# A Useful Variant of the Davis–Kahan Theorem for Statisticians

> [!abstract] 来源定位
> 论文给出只依 population eigengap 的 Davis–Kahan 变体，直接连接 covariance estimation error 与 sample/population principal subspace distance。本库用它建立 PCA 的 gap-sensitive risk interface。

## 本库调用

1. eigenvector/subspace accuracy必须同时看 operator perturbation与 population eigengap；
2. repeated eigenvalues时 individual eigenvectors不可辨识，但整个 invariant subspace仍可估；
3. sign、rotation与basis choice不能进入 basis-invariant subspace loss；
4. perturbation bound本身不提供 covariance concentration，后者需要 tail/dependence assumptions。
