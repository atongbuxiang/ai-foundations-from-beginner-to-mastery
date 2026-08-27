---
type: source
status: verified
area: [sources, ai/scaling-laws, language-models]
source_type: paper
title: "Scaling Laws for Neural Language Models"
author: "Jared Kaplan et al."
year: 2020
url: "https://arxiv.org/abs/2001.08361"
accessed: 2026-08-26
source_tier: A
license: "arXiv paper; independent summary only"
scope_role: core
temporal_role: foundational
related: ["[[渐近记号、增长率与复杂度]]", "[[S-2023-Su-9607-量子化假设与尺度定律]]", "[[S-2022-Hoffmann-计算最优训练]]"]
created: 2026-08-19
updated: 2026-08-26
---

# Scaling Laws for Neural Language Models

> [!abstract] 来源定位
> 论文在其Transformer模型族、数据与训练制度中研究cross-entropy loss随非embedding参数量$N$、数据量$D$与compute $C$的经验幂律，并据此提出compute allocation。MATH-08把它当作高质量有限尺度实证，而不是对任意模型或无限规模的无条件渐近定理。

## 核心断言

- 在其他瓶颈受控的制度内，loss对$N,D,C$呈经验power-law关系；
- 参数、数据与compute需要共同扩展，固定某一瓶颈会进入diminishing returns；
- 经验拟合可用于所研究范围内的预测与预算讨论。

## 证据边界

- Exponent和常数来自指定模型族与训练流程；
- 论文自身说明loss最终不能无限降至负值，地板/饱和必须考虑；
- 对finite window的精确fit不等于$n\to\infty$证明；
- 后续Hoffmann等以不同IsoFLOP设计修订了compute-optimal allocation；
- 本章不背诵具体指数，而训练变量控制、拟合窗口和外推审计。
