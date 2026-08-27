---
type: source
status: active
area: [sources, learning-theory, adaptive-data-analysis, mutual-information]
source_type: paper
title: "Controlling Bias in Adaptive Data Analysis Using Information Theory"
author: [Daniel Russo, James Zou]
year: 2016
url: "https://proceedings.mlr.press/v51/russo16.html"
accessed: 2026-08-23
source_tier: A
license: "PMLR proceedings; retain citation, independent derivations, and official links"
venue: "AISTATS 2016, PMLR 51"
scope_role: primary
temporal_role: modern-foundation
related: ["[[互信息与信息论泛化界]]", "[[训练集、验证集、测试集与自适应复用]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Controlling Bias in Adaptive Data Analysis Using Information Theory

> [!abstract] 来源定位
> Russo 与 Zou 用 mutual information 衡量一个自适应选择结果泄露了多少关于被复用数据的信息，并据此控制 selection bias。它是把 sample–output information 从单次学习扩展到 adaptive model/feature/query selection 的关键接口。

## 元数据与纳入

- 论文主页：[PMLR](https://proceedings.mlr.press/v51/russo16.html)；
- 官方全文：[PDF](https://proceedings.mlr.press/v51/russo16/russo16.pdf)；
- 正式引用：Russo, D. & Zou, J. (2016), *AISTATS*, PMLR 51；
- 证据角色：adaptive selection bias、information usage 与 transcript-level auditing。

## 本库调用的断言

1. 即使每个统计量单独无偏，依赖同一数据自适应选择其索引也会产生 bias；
2. selection rule 与数据之间的 mutual information 可作为平均自适应代价；
3. 多轮 transcript 应用 chain rule 记账，而不是只数最终输出；
4. information bound 是 distribution-dependent expectation statement，不等于 worst-case privacy guarantee；
5. 降低输出精度、随机化与限制 query transcript 可能降低信息使用，但会引入效用权衡。

## 后续调用

- [[互信息与信息论泛化界]]：adaptive validation 与 transcript composition；
- [[训练集、验证集、测试集与自适应复用]]：选择偏差的机制解释。

