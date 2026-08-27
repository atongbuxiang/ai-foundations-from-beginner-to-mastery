---
type: moc
status: active
area: [neural-networks/initialization]
prerequisites: ["[[激活函数、门控与非线性 MOC]]", "[[期望、方差与矩]]"]
related: ["[[神经网络基础完整课程地图与掌握标准]]", "[[归一化、尺度与统计量 MOC]]"]
created: 2026-08-23
updated: 2026-08-23
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

当前为 **8/8 正文、8/8 A—E 题解闭环、0/8 真实验收**，NN-25—32 共 120 题与逐题详解已经形成完整静态课程闭环。下一卷进入 30.5 的 NN-33—36：归一化对象与轴、BatchNorm 前向统计、BatchNorm 反向传播，以及 LayerNorm 几何与反向传播。
