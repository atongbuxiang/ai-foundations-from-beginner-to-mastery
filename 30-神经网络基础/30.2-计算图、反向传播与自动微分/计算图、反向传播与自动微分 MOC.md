---
type: moc
status: active
area: [neural-networks/backprop-autodiff]
prerequisites: ["[[前馈网络、感知机与表达能力 MOC]]", "[[多元链式法则与计算图]]"]
related: ["[[神经网络基础完整课程地图与掌握标准]]", "[[激活函数、门控与非线性 MOC]]"]
created: 2026-08-23
updated: 2026-08-29
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

## 当前材料门与学习状态

- [[neural_network_foundations_teaching_contract_audit.py]] 已复核 NN-09—16 的课程位置、两遍路线、问题链、对象账本、共享 $X_\diamond$ fixture 与公式七问；
- 前半卷闭合 affine-regression 的 forward $L=5.25$、JVP/VJP $2.5$ 与参数梯度；后半卷继续闭合 ReLU residual/broadcast VJP、stable CE $0.0255315$、logit directional derivative $-0.00123631$ 与 HVP $0.00123325$；
- 当前为 **8/8 现行教学迁移、8/8 正文、8/8 A—E 题解、8/8 正式图，30.2 材料门 `regression-passed`**；
- 全章状态为 **44/64 已迁移、20/64 pending、分卷材料门 5/8**；30.6 前半卷 `in-progress`，个人仍为 **0/8 / `not-attempted`**；下一批 NN-45—48。
