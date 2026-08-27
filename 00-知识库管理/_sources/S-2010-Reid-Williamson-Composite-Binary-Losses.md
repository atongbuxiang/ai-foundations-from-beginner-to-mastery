---
type: source
status: active
area: [sources, learning-theory, proper-losses, probability-estimation]
source_type: paper
title: "Composite Binary Losses"
author: [Mark D. Reid, Robert C. Williamson]
year: 2010
url: "https://www.jmlr.org/papers/v11/reid10a.html"
accessed: 2026-08-23
source_tier: A
license: "JMLR article; retain citation, official links, and independent derivations"
venue: "Journal of Machine Learning Research 11, 2387–2422"
scope_role: primary
temporal_role: modern-foundation
related: ["[[逻辑回归、复合损失与概率分类]]", "[[概率校准、Proper Scoring Rule 与可靠性图]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Composite Binary Losses

> [!abstract] 来源定位
> Reid 与 Williamson 把 binary class-probability estimation loss 与 link function 组合成 proper composite loss，并系统连接 properness、classification calibration、convexity 与 Bregman divergence。它承担本库“log loss 为什么估计概率，而 hinge loss 主要估计决策符号”的正式接口。

## 元数据与纳入

- 论文主页：[JMLR](https://www.jmlr.org/papers/v11/reid10a.html)；
- 官方全文：[PDF](https://www.jmlr.org/papers/volume11/reid10a/reid10a.pdf)；
- 正式引用：Reid, M. D. & Williamson, R. C. (2010), *JMLR* 11, 2387–2422；
- 证据角色：proper composite representation、link、conditional risk 与 probability estimation；
- 本库对 binary log loss 的 entropy + KL identity 独立手推。

## 本库调用的断言

1. proper loss 的 conditional risk 在真实 class probability 处最小；
2. strict properness 给唯一 probability target；
3. composite loss 把 probability-space loss 与 real-valued link 连接；
4. properness、convexity、classification calibration 与 label-noise robustness 是不同性质。

