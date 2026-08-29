---
type: source
status: active
area: [sources, neural-networks, mixup, vicinal-risk]
source_type: paper
title: "mixup: Beyond Empirical Risk Minimization"
author: "Hongyi Zhang; Moustapha Cisse; Yann N. Dauphin; David Lopez-Paz"
year: 2018
url: "https://openreview.net/pdf?id=r1Ddp1-Rb"
venue: "ICLR 2018"
accessed: 2026-08-24
source_tier: A
license: "OpenReview conference paper；本库仅保存独立摘要、必要公式与链接"
scope_role: original-method
temporal_role: foundational
related: ["[[Mixup、Manifold Mixup 与插值正则]]"]
created: 2026-08-24
updated: 2026-08-29
---

# Zhang et al.：Mixup

> [!abstract] 来源定位
> 论文以样本对的输入与标签凸组合定义 mixup，并把它解释为 vicinal distribution 上的训练原则。它承担原始方法、Beta mixing 与基准证据；“样本间线性行为”是所施加的归纳偏置，不是自然数据流形必然线性的定理。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| MX-C1 | $\tilde x=\lambda x_i+(1-\lambda)x_j$、$\tilde y=\lambda y_i+(1-\lambda)y_j$ | 定义 | 同一 $\lambda$ 与合法标签空间 | 精确 |
| MX-C2 | soft-target CE 对 label 线性 | 代数 | fixed mixed prediction | 精确 |
| MX-C3 | 所有 input chords 都是语义有效样本 | 几何外推 | manifold intrusion/结构对象 | 错误 |
| MX-C4 | 原论文多任务 improvement 适用于任意 modality | 经验外推 | pairing/augmentation/model 依赖 | 不成立 |
