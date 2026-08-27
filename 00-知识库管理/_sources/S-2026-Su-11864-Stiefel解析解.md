---
type: source
status: verified
area: [sources, optimization, stiefel, matrix-manifolds]
source_type: blog
title: "Stiefel流形最速下降的解析解"
author: 苏剑林
year: 2026
url: "https://spaces.ac.cn/archives/11864"
accessed: 2026-08-26
source_tier: C
license: "科学空间站点声明存在版本差异；仅保存独立摘要与链接"
site_category: [信息时代]
scope_role: frontier-derivation
temporal_role: frontier-recent
related: ["[[Stiefel、谱球面、旋转 Muon 与约束更新]]", "[[Riemann 几何、测地线与流形优化]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Stiefel 流形最速下降的解析解

> [!abstract] 来源定位
> 这是 2026-08-17 发布的近期推导，讨论 Stiefel 约束下某类最速方向的解析表达。它提供前沿研究入口，但距访问日仅九天，尚不具备长期复现和独立验证积累。

## 分层采用

| 层 | 内容 | 证据状态 |
|---|---|---|
| 成熟基础 | Stiefel 定义、切空间、metric、projection、retraction | 由 [[S-2008-Absil-Matrix-Manifolds]] 支撑 |
| 本文推导 | 指定范数/metric/约束下的解析方向 | 按原假设重推并做小矩阵残差检验 |
| 工程结论 | 比迭代 SVD/NS 更快或更好训练 | 尚需公开实现、硬件账本和跨任务复现 |

## 使用警戒

“解析式”不等于数值上便宜：矩阵根、SVD、线性方程或投影的代价仍需展开。任何与 Muon 的关系都必须注明作用对象是 gradient、update 还是 parameter，并区分 tangent feasibility 与 finite-step feasibility。

