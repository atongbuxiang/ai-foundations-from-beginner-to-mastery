---
type: moc
status: active
area: [architecture, sequence-models, ssm]
related: ["[[表示与模型架构完整课程地图与掌握标准]]", "[[科学空间 - 第四章专题来源地图]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 循环网络、记忆与状态空间模型 MOC

| ID | 节点 | 学习出口 | 状态 |
|---|---|---|---|
| ARCH-09 | [[序列因果性、隐藏状态与递推计算]] | state contract | draft + A–E 闭环 |
| ARCH-10 | [[Vanilla RNN、BPTT 与梯度消失爆炸]] | temporal Jacobian | draft + A–E 闭环 |
| ARCH-11 | [[LSTM 的记忆单元、门控与梯度通道]] | gated memory | draft + A–E 闭环 |
| ARCH-12 | [[GRU、门控递推与 RNN 结构比较]] | gate comparison | draft + A–E 闭环 |
| ARCH-13 | [[连续与离散线性状态空间模型]] | discretization | draft + A–E 闭环 |
| ARCH-14 | [[状态空间的递推—卷积对偶与并行扫描]] | recurrence/convolution duality | draft + A–E 闭环 |
| ARCH-15 | [[HiPPO、S4 与结构化长记忆]] | projection-to-SSM derivation | draft + A–E 闭环 |
| ARCH-16 | [[选择性状态空间、Mamba 与证据边界]] | selective-state audit | draft + A–E 闭环 |

当前为 **8/8 正文、8/8 A—E 题解闭环、0/8 真实学习验收**；ARCH-09—16 共 120 题、逐题独立详解和八张正式图已完成。科学空间 SSM 四篇已按“解释桥梁”纳入，LSTM/GRU/HiPPO/S4/Mamba 由原论文补足。下一学习点为 ARCH-17。

## 可复算审计

- [[00-知识库管理/_labs/code/architecture_sequence_ssm_audit.py]]：小规模确定性复算 state recurrence、BPTT finite difference、LSTM/GRU 门控、ZOH、递推—卷积一致性、scan 结合律、rank-one inverse 与 selective retention。
