---
type: source
status: verified
area: [sources, ai/optimization, mean-field]
source_type: blog
title: "重新思考学习率与 Batch Size（二）：平均场"
author: 苏剑林
year: 2025
url: "https://spaces.ac.cn/archives/11280"
accessed: 2026-08-26
source_tier: C
license: "科学空间页面声明 CC BY-NC-SA；本库仅保存独立摘要、必要短公式与链接"
scope_role: supporting
related: ["[[梯度噪声协方差、Noise Scale 与 SDE 近似]]"]
created: 2026-08-26
updated: 2026-08-26
---

# 科学空间：学习率与 Batch Size（二）平均场

> [!abstract] 来源定位
> 文章继续从平均场/连续近似讨论 learning-rate–batch coupling。本卷采用其研究问题与推导视角，但把 diffusion limit、有限步离散系统和实际训练三层分账。

## 课程补严

离散 SGD 增量的条件 covariance 是 $\eta^2C/B$；若令连续时间 $t=k\eta$，对应 Euler–Maruyama diffusion 振幅为 $\sqrt{\eta/B}C^{1/2}$。这一匹配是二阶矩尺度的局部近似，不声明离散轨迹逐点等于 SDE，也不自动覆盖无放回采样、动量、裁剪和时变数据分布。

## 已核对的课程接口

- 原文用 mean-field 近似降低非线性更新（特别是 SignSGD/SoftSignSGD 一类）下学习率—batch 关系的计算负担；平均场是方法性假设，不是无需验证的精确恒等式；
- 后续推广到 Adam/Muon 的可行性不能倒推当前简化已经证明这些优化器的通用 scaling law；相关性、逐坐标非线性、动量时标和有限 batch 尾部都可能破坏闭式近似；
- 本章只采用“先列 estimator、再声明 closure、最后与离散实验对照”的工作流，并在 [[梯度噪声协方差、Noise Scale 与 SDE 近似]] 中把条件 covariance、连续时间和有限步轨迹分账。

核对入口：[科学空间原文](https://spaces.ac.cn/archives/11280)；访问日 2026-08-26。
