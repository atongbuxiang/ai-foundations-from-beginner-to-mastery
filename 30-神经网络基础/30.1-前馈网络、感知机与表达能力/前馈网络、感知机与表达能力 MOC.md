---
type: moc
status: active
area: [neural-networks/feedforward]
prerequisites: ["[[向量空间]]", "[[凸集、凸组合与分离超平面]]", "[[预测器、假设空间与学习算法]]"]
related: ["[[神经网络基础完整课程地图与掌握标准]]", "[[计算图、反向传播与自动微分 MOC]]"]
created: 2026-08-23
updated: 2026-08-29
---
# 前馈网络、感知机与表达能力 MOC
| ID | 节点 | 出口 | 状态 |
|---|---|---|---|
| NN-01 | [[人工神经元、仿射变换与决策超平面]] | neuron geometry | draft + A–E 闭环 |
| NN-02 | [[线性层、批量张量与参数计数]] | shape ledger | draft + A–E 闭环 |
| NN-03 | [[感知机模型、更新规则与线性可分性]] | threshold learning | draft + A–E 闭环 |
| NN-04 | [[多层感知机与逐层前向计算]] | function composition | draft + A–E 闭环 |
| NN-05 | [[XOR、隐藏表示与非线性必要性]] | nonlinear representation | draft + A–E 闭环 |
| NN-06 | [[万能逼近定理、紧集与逼近误差]] | approximation theorem | draft + A–E 闭环 |
| NN-07 | [[深度分离、线性区域与表达效率]] | depth efficiency | draft + A–E 闭环 |
| NN-08 | [[参数对称性、等价表示与可辨识边界]] | parameter quotient | draft + A–E 闭环 |

## 当前材料门与学习状态

- [[neural_network_foundations_teaching_contract_audit.py]] 已复核 NN-01—08 的课程位置、两遍路线、问题链、对象账本、共享 fixture 与公式七问；
- 第一链 $X_\star$ 贯通 affine score、batch dense、perceptron 与 paired ReLU；第二链 $X_\oplus$ 贯通 XOR、triangular hat、UAT、depth separation 与 parameter quotient；
- 当前为 **8/8 现行教学迁移、8/8 正文、8/8 A—E 题解、8/8 正式图，30.1 材料门 `regression-passed`**；
- 全章状态同步为 **64/64 已迁移、0/64 pending、分卷材料门 8/8 `regression-passed`**；个人仍为 **0/8 / `not-attempted`**；下一材料施工点为 NN-CUM-01 现行合同重审。
