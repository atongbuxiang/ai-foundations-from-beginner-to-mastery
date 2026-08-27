---
type: source
status: active
area: [sources, learning-theory, em, latent-variable-models]
source_type: paper
title: "Maximum Likelihood from Incomplete Data via the EM Algorithm"
author: [Arthur P. Dempster, Nan M. Laird, Donald B. Rubin]
year: 1977
url: "https://doi.org/10.1111/j.2517-6161.1977.tb01600.x"
accessed: 2026-08-23
source_tier: A
license: "JRSS B article; retain citation and independent derivations"
venue: "Journal of the Royal Statistical Society B 39(1), 1–38"
scope_role: primary
temporal_role: classical-foundation
related: ["[[潜变量模型、混合模型与 EM]]", "[[最大似然估计与 MAP]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Maximum Likelihood from Incomplete Data via the EM Algorithm

> [!abstract] 来源定位
> Dempster、Laird 与 Rubin系统化 incomplete-data maximum likelihood 的 EM algorithm，并建立 likelihood monotonicity主线。本库用它推导 exact E-step、Q-function、M-step与 generalized EM 的对象合同。

## 本库调用

1. observed likelihood通过 latent/complete data marginalization得到；
2. E-step计算 current parameter下 complete log-likelihood的 conditional expectation；
3. exact M-step最大化 Q-function，产生 observed likelihood不降；
4. monotonicity不是 global optimality、parameter uniqueness或 statistical consistency；
5. missing data、finite mixtures与factor models共享算法形式，但可辨识条件不同。
