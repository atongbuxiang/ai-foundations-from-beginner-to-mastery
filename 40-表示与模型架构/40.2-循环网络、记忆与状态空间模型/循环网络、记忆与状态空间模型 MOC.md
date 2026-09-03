---
type: moc
status: active
area: [architecture, sequence-models, ssm]
related: ["[[表示与模型架构完整课程地图与掌握标准]]", "[[科学空间 - 第四章专题来源地图]]"]
created: 2026-08-24
updated: 2026-09-03
---

# 循环网络、记忆与状态空间模型 MOC

| ID | 节点 | 学习出口 | 状态 |
|---|---|---|---|
| ARCH-09 | [[序列因果性、隐藏状态与递推计算]] | state contract | regression-passed material / learner `not-attempted` |
| ARCH-10 | [[Vanilla RNN、BPTT 与梯度消失爆炸]] | temporal Jacobian | regression-passed material / learner `not-attempted` |
| ARCH-11 | [[LSTM 的记忆单元、门控与梯度通道]] | gated memory | regression-passed material / learner `not-attempted` |
| ARCH-12 | [[GRU、门控递推与 RNN 结构比较]] | gate comparison | regression-passed material / learner `not-attempted` |
| ARCH-13 | [[连续与离散线性状态空间模型]] | discretization | regression-passed material / learner `not-attempted` |
| ARCH-14 | [[状态空间的递推—卷积对偶与并行扫描]] | recurrence/convolution duality | regression-passed material / learner `not-attempted` |
| ARCH-15 | [[HiPPO、S4 与结构化长记忆]] | projection-to-SSM derivation | regression-passed material / learner `not-attempted` |
| ARCH-16 | [[选择性状态空间、Mamba 与证据边界]] | selective-state audit | regression-passed material / learner `not-attempted` |

 当前为 **8/8 现行教学迁移、8/8 A—E 题解闭环、8/8 `regression-passed` material**；全章累计为 **ARCH-01—24（24/64）**，分卷材料门为 **3/8**，40.3 已完成 8/8。两波以 $\mathcal S_\square$ 贯通状态碰撞、BPTT、LSTM/GRU、ZOH、recurrence/convolution/scan、HiPPO/S4 与 selective path，并由[[architecture_teaching_contract_audit.py]]独立复算八幅正式图和精确数值。个人学习状态为 `not-attempted`，下一施工点为 ARCH-25—32。

## 可复算审计

- [[00-知识库管理/_labs/code/architecture_sequence_ssm_audit.py]]：小规模确定性复算 state recurrence、BPTT finite difference、LSTM/GRU 门控、ZOH、递推—卷积一致性、scan 结合律、rank-one inverse 与 selective retention。
