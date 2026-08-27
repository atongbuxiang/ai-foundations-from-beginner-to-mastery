---
type: source
status: draft
area: [sources, neural-networks, label-smoothing, classification]
source_type: paper
title: "Rethinking the Inception Architecture for Computer Vision"
author: "Christian Szegedy; Vincent Vanhoucke; Sergey Ioffe; Jon Shlens; Zbigniew Wojna"
year: 2016
url: "https://openaccess.thecvf.com/content_cvpr_2016/html/Szegedy_Rethinking_the_Inception_CVPR_2016_paper.html"
venue: "CVPR 2016"
accessed: 2026-08-24
source_tier: A
license: "CVF open-access paper；本库仅保存独立摘要、必要公式与链接"
scope_role: original-method
temporal_role: foundational
related: ["[[Label Smoothing、置信度与目标偏置]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Szegedy et al.：Label Smoothing 原始合同

> [!abstract] 来源定位
> 论文在 Inception 训练中提出 label-smoothing regularization，把 one-hot target 与固定 label prior 混合。它承担方法定义与原始视觉实验来源；本库单独推导交叉熵分解、最优概率与 logit margin，并不把单一 benchmark gain 升级为普遍校准或抗噪定理。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| LS0-C1 | target 可写成 $(1-\epsilon)y+\epsilon u$ | 定义 | 声明 $u$ 与是否含 true class | 精确 |
| LS0-C2 | smoothed CE 是 hard CE 与 prior CE 的凸组合 | 代数 | 相同 prediction 与 reduction | 精确 |
| LS0-C3 | Label Smoothing 必然改善所有任务的 calibration | 经验外推 | 数据、模型、$\epsilon$、shift 依赖 | 不成立 |
| LS0-C4 | 它只改变 optimization，不改变估计目标 | 对象混淆 | population optimum 被推向 $u$ | 错误 |
