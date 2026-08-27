---
type: source
status: active
area: [sources, learning-theory, margin-theory]
source_type: paper
title: "Empirical Margin Distributions and Bounding the Generalization Error of Combined Classifiers"
author: [Vladimir Koltchinskii, Dmitry Panchenko]
year: 2002
url: "https://doi.org/10.1214/aos/1015362183"
accessed: 2026-08-23
source_tier: A
license: "Annals of Statistics article; retain citation, independent derivations, and DOI/article links"
venue: "The Annals of Statistics 30(1), 1–50"
scope_role: primary
temporal_role: classical-foundation
related: ["[[分类间隔、Margin Bound 与 SVM 接口]]", "[[局部 Rademacher 复杂度与快收敛率]]", "[[Boosting 与弱到强学习]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Empirical Margin Distributions and Generalization Error

> [!abstract] 来源定位
> Koltchinskii 与 Panchenko 以 empirical/Gaussian process 方法研究组合分类器的经验 margin distribution 与总体分类误差。本库用它校准“低 margin 经验比例 + 尺度相关复杂度”这条证据链；SVM 的优化几何、surrogate calibration 与现代深网 margin bound 另行分层。

## 元数据与纳入

- 正式引用：Koltchinskii, V. & Panchenko, D. (2002), *The Annals of Statistics* 30(1), 1–50；
- DOI：[10.1214/aos/1015362183](https://doi.org/10.1214/aos/1015362183)；
- 开放版本：[arXiv](https://arxiv.org/abs/math/0405343)；
- 证据角色：经验 margin distribution 风险界的原始主线；
- 版权边界：不复制原图或长段文字，只保留独立定义、证明接口与文献定位。

## 本库调用的断言

1. 分类风险可由训练样本中 margin 不超过阈值的比例与依赖阈值的 complexity penalty 控制；
2. margin threshold 越小，经验低 margin 比例通常降低，但 complexity 常按 $1/\gamma$ 增长；
3. 组合分类器的函数类结构与 margin distribution 必须一起进入界，不能只看最小训练 margin；
4. 对阈值做自适应选择需要统一化或额外 confidence budget；
5. empirical margin explanation 是有限样本统计陈述，不等同于 optimization dynamics 或 causal explanation。

> [!warning] 定义与常数
> 文献对 normalized margin、voting class、Gaussian/Rademacher process 与阈值网格有专门约定。本课程先用 bounded ramp loss 推出可审计的安全常数版，再把更尖锐结果标作加强项。

## 后续调用

- [[分类间隔、Margin Bound 与 SVM 接口]]：margin risk certificate 与 SVM 几何接口；
- [[局部 Rademacher 复杂度与快收敛率]]：低 margin/低噪声下的 localized refinement；
- [[Boosting 与弱到强学习]]：经验 margin distribution 与 ensemble complexity 分账。
