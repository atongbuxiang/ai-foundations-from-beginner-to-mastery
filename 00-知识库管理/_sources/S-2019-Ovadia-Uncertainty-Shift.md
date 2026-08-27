---
type: source
status: active
area: [sources, uncertainty, distribution-shift, evaluation]
source_type: paper
title: "Can You Trust Your Model's Uncertainty? Evaluating Predictive Uncertainty Under Dataset Shift"
author: [Yaniv Ovadia, Emily Fertig, Jie Ren, Zachary Nado, D. Sculley, Sebastian Nowozin, Joshua V. Dillon, Balaji Lakshminarayanan, Jasper Snoek]
year: 2019
url: "https://proceedings.neurips.cc/paper/2019/hash/8558cb408c1d76621371888657d2eb1d-Abstract.html"
accessed: 2026-08-23
source_tier: A
license: "Open scholarly source; retain citation and benchmark conditions"
venue: "NeurIPS 2019"
scope_role: primary
temporal_role: benchmark-audit
related: ["[[Bayesian Posterior Predictive、Ensemble 与近似边界]]", "[[Covariate、Label 与 Concept Shift]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Can You Trust Your Model's Uncertainty?

> [!abstract] 来源定位
> 系统比较多种 predictive uncertainty 方法在逐渐增强 dataset shift 下的表现。本库调用其 shift-aware evaluation principle；不把特定模型与数据集上的方法排名外推为普遍定理。

## 本库调用

1. in-distribution calibration 不推出 shift 下可靠；
2. shift severity curve 比单一 OOD 点更有信息；
3. accuracy、NLL、Brier 与 calibration error 需并列；
4. 方法排名依赖 architecture、dataset 与 shift generator；
5. uncertainty method 必须和 posterior approximation、ensemble size 与 compute 一起报告。
