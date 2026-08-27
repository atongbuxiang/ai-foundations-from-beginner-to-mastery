---
type: moc
status: active
area: [learning-theory/deep-generalization]
prerequisites: ["[[数据依赖复杂度、间隔与快率 MOC]]", "[[稳定性、压缩、PAC-Bayes 与信息泛化 MOC]]", "[[表示学习、度量学习与自监督 MOC]]"]
related: ["[[学习理论完整课程地图与掌握标准]]", "[[数学基础十卷完备性审计与学习状态总表]]"]
created: 2026-08-20
updated: 2026-08-23
---

# 深度泛化理论接口与开放边界 MOC

> [!abstract] 本卷任务
> 以证据地图而不是单一口号解释深网泛化：插值、benign overfitting、implicit bias、norm/margin bounds、NTK 与 feature learning 各自只在特定 regime 中成立。

| ID | 节点 | 关键出口 | 状态 |
|---|---|---|---|
| LT-77 | [[插值、双下降与经典偏差方差边界]] | interpolation phenomenology | draft + A–E 闭环 |
| LT-78 | [[过参数化与 Benign Overfitting]] | spectrum/noise conditions | draft + A–E 闭环 |
| LT-79 | [[隐式偏置、最大间隔与优化选择]] | algorithm selects interpolant | draft + A–E 闭环 |
| LT-80 | [[范数、平坦性、Sharpness 与参数化不变性]] | proxy invariance audit | draft + A–E 闭环 |
| LT-81 | [[神经网络容量与 Norm-Based Bound]] | depth/norm capacity | draft + A–E 闭环 |
| LT-82 | [[NTK、Lazy Training 与 Kernel Regime]] | fixed-feature regime | draft + A–E 闭环 |
| LT-83 | [[Mean-Field、Feature Learning 与训练 Regime]] | moving-feature regime | draft + A–E 闭环 |
| LT-84 | [[深度泛化证据地图与开放问题]] | theorem/experiment/hypothesis ledger | draft + A–E 闭环 |

当前为 **8/8 正文、8/8 A–E 习题与独立详解，0/8 经真实作答验收**。LT-77—84 已形成“插值现象 → 算法选解 → norm/margin 容量 → kernel/rich regime → 证据地图”的静态闭环；本卷不把任何单一解释升级为“深度学习泛化定律”。下一步执行 LT-01—84 全量静态审计，再进入真实作答验收。
