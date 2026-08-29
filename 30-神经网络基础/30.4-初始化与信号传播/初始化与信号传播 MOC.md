---
type: moc
status: active
area: [neural-networks/initialization]
prerequisites: ["[[激活函数、门控与非线性 MOC]]", "[[期望、方差与矩]]"]
related: ["[[神经网络基础完整课程地图与掌握标准]]", "[[归一化、尺度与统计量 MOC]]"]
created: 2026-08-23
updated: 2026-08-29
---
# 初始化与信号传播 MOC
| ID | 节点 | 出口 | 状态 |
|---|---|---|---|
| NN-25 | [[方差传播与宽层均值场近似]] | moment recursion | draft + A–E 闭环 |
| NN-26 | [[Xavier、Glorot 初始化]] | fan-average scaling | draft + A–E 闭环 |
| NN-27 | [[Kaiming、He 初始化]] | ReLU scaling | draft + A–E 闭环 |
| NN-28 | [[反向梯度方差与 Fan-In_Fan-Out 权衡|反向梯度方差与 Fan-In/Fan-Out 权衡]] | backward variance | draft + A–E 闭环 |
| NN-29 | [[相关传播、Edge of Chaos 与临界初始化]] | correlation dynamics | draft + A–E 闭环 |
| NN-30 | [[正交初始化与 Dynamical Isometry]] | Jacobian spectrum | draft + A–E 闭环 |
| NN-31 | [[偏置、输出层与零初始化的对称性边界]] | symmetry breaking | draft + A–E 闭环 |
| NN-32 | [[LSUV、Fixup 与现代初始化诊断]] | modern audit | draft + A–E 闭环 |

## 当前迁移与学习状态

- [[neural_network_foundations_teaching_contract_audit.py]]已复核 NN-25—32 的两遍路线、问题链、对象账本、$\mathcal I_\square$ 共享 $4\to8$ fixture 与公式七问；
- 前半卷闭合 ReLU $q=2\to r=1$、Xavier/He 和 fan 乘积；后半卷闭合 $c_0=1/2\to0.608998$、半正交 ReLU 的 rank-2 反例、zero-head/skip 梯度与 LSUV/Fixup 两类校准；
- 当前为 **8/8 现行教学迁移、8/8 正文、8/8 A—E 题解、8/8 正式图，30.4 材料门 `regression-passed`**；
- 全章为 **60/64 已迁移、4/64 pending、分卷材料门 7/8**，30.8 前半卷 `in-progress`，个人仍为 **0/8 / `not-attempted`**；下一批 NN-61—64。
