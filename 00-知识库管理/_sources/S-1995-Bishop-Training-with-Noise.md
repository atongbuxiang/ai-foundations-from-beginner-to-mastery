---
type: source
status: active
area: [sources, neural-networks, noise-injection, regularization]
source_type: paper
title: "Training with Noise is Equivalent to Tikhonov Regularization"
author: "Christopher M. Bishop"
year: 1995
url: "https://doi.org/10.1162/neco.1995.7.1.108"
venue: "Neural Computation 7(1)"
accessed: 2026-08-29
source_tier: A
license: "MIT Press article；本库仅保存独立摘要、必要结论与链接"
scope_role: noise-theory
temporal_role: foundational
related: ["[[DropConnect、权重噪声与激活噪声]]"]
created: 2026-08-24
updated: 2026-08-29
---

# Bishop：Noise Injection 与 Tikhonov Regularization

> [!abstract] 来源定位
> 论文在小噪声展开及平方误差等条件下，把输入噪声训练联系到含网络一阶导数的广义 Tikhonov regularizer。它承担“噪声可诱导平滑 penalty”的经典来源；等价具有损失、噪声幅度和展开阶数边界，不能简化为任意噪声都等于普通 $L_2$ weight decay。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| BTN-C1 | 小输入噪声的 expected loss 可作二阶展开 | 分析 | 光滑性与有限 moments | 成立 |
| BTN-C2 | 平方误差下可出现 Jacobian/Tikhonov 型 penalty | 理论 | 论文设置 | 原范围成立 |
| BTN-C3 | 任意有限噪声与某个简单 penalty 全局精确相等 | 外推 | 高阶项与非线性存在 | 错误 |
| BTN-C4 | 噪声位置不影响诱导 regularizer | 对象混淆 | input/activation/weight 的 Jacobian 不同 | 错误 |
