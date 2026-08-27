---
type: source
status: verified
area: [sources, optimization, learning-rate, batch-size]
source_type: blog
title: "当Batch Size增大时，学习率该如何变化？"
author: 苏剑林
year: 2024
url: "https://spaces.ac.cn/archives/10542"
accessed: 2026-08-26
source_tier: C
license: "科学空间页面声明 CC BY-NC-SA；本库仅保存独立摘要、必要短公式与链接"
scope_role: chinese-derivation-entry
related: ["[[学习率、局部损失变化与相对更新尺度]]", "[[Critical Batch、隐式偏置与 SGD 证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# 苏剑林：Batch Size 与 Learning Rate 缩放

> [!abstract] 来源定位
> 文章用局部 Taylor、梯度均值/协方差与 Hessian 近似讨论 batch 增大时线性律、方根律及其过渡。课程采用推导坐标，不把局部近似写成全训练定律。

## 课程采用

- 区分每 step、每样本、每 token 和固定训练预算；
- 将 full gradient、sampling covariance、Hessian quadratic term 分账；
- 把线性/方根缩放写成不同噪声与曲率 regime 的候选，而非冲突口号；
- 要求对 SGD、Adam、Muon 分别重新定义更新方向与有效步长。
