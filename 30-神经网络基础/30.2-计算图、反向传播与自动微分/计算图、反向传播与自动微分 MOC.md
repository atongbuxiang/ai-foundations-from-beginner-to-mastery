---
type: moc
status: active
area: [neural-networks/backprop-autodiff]
prerequisites: ["[[前馈网络、感知机与表达能力 MOC]]", "[[多元链式法则与计算图]]"]
related: ["[[神经网络基础完整课程地图与掌握标准]]", "[[激活函数、门控与非线性 MOC]]"]
created: 2026-08-23
updated: 2026-08-23
---
# 计算图、反向传播与自动微分 MOC
| ID | 节点 | 出口 | 状态 |
|---|---|---|---|
| NN-09 | [[计算图、拓扑序与前向执行]] | executable DAG | draft + A–E 闭环 |
| NN-10 | [[局部微分、Jacobian、JVP 与 VJP]] | local linear actions | draft + A–E 闭环 |
| NN-11 | [[标量链式法则与反向传播递推]] | adjoint recursion | draft + A–E 闭环 |
| NN-12 | [[线性层与仿射层的反向传播]] | affine gradients | draft + A–E 闭环 |
| NN-13 | [[激活、分支、广播与梯度累加]] | graph semantics | draft + A–E 闭环 |
| NN-14 | [[Softmax–Cross-Entropy 的稳定融合反向]] | stable fused loss | draft + A–E 闭环 |
| NN-15 | [[Forward_Reverse AD、Tape 与复杂度|Forward/Reverse AD、Tape 与复杂度]] | AD mode selection | draft + A–E 闭环 |
| NN-16 | [[Gradient Checking、Checkpointing 与高阶微分边界]] | verification/memory | draft + A–E 闭环 |

当前为 **8/8 正文、8/8 A—E 题解闭环、0/8 真实验收**。NN-09—16 已完成正文、八张可复现教学图、120 题及逐题独立详解；下一批转入 30.3 的 NN-17—20。`not-attempted` 仍表示尚无学习者闭卷与迁移证据。
