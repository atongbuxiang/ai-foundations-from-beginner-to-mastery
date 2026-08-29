---
type: source
status: active
area: [sources, neural-networks, spectral-normalization, lipschitz, gan]
source_type: paper
title: "Spectral Normalization for Generative Adversarial Networks"
author: "Takeru Miyato; Toshiki Kataoka; Masanori Koyama; Yuichi Yoshida"
year: 2018
url: "https://openreview.net/pdf?id=B1QRgziT-"
venue: "ICLR 2018"
accessed: 2026-08-24
source_tier: A
license: "OpenReview conference paper；本库仅保存独立摘要、必要公式与链接"
scope_role: operator-norm-control
temporal_role: foundational
related: ["[[Jacobian、Gradient Penalty 与 Lipschitz 正则接口]]", "[[正交初始化与 Dynamical Isometry]]"]
created: 2026-08-24
updated: 2026-08-29
---

# Miyato et al.：Spectral Normalization

> [!abstract] 来源定位
> 论文用 weight matrix 的主奇异值归一化控制 discriminator 各线性层的欧氏 operator norm，并以 power iteration 近似。它承担 spectral normalization 方法来源；卷积 operator 的实际谱、残差相加、normalization state 和全网 bound slack 需另行审计。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| SN-C1 | 线性层欧氏 Lipschitz 常数是谱范数 | 线性代数 | 2-norm | 精确 |
| SN-C2 | composition 常数可由层常数乘积上界 | 分析 | 每层 uniform bound | 正确但可很松 |
| SN-C3 | 一步 power iteration 总给精确主奇异值 | 数值外推 | gap、warm start、迭代误差 | 错误 |
| SN-C4 | 每层归一化自动给 tight network certificate | bound 外推 | residual/branch/activation slack | 错误 |
