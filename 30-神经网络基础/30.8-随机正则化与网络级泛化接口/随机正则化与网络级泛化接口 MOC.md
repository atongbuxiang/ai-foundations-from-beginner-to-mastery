---
type: moc
status: active
area: [neural-networks/regularization]
prerequisites: ["[[学习问题、决策与风险 MOC]]", "[[残差连接、深度与稳定性 MOC]]"]
related: ["[[神经网络基础完整课程地图与掌握标准]]", "[[容量界、稳定性界与 PAC-Bayes 的比较]]"]
created: 2026-08-23
updated: 2026-08-29
---
# 随机正则化与网络级泛化接口 MOC
| ID | 节点 | 出口 | 状态 |
|---|---|---|---|
| NN-57 | [[Dropout 的随机掩码、期望与 Inverted Scaling]] | mask expectation | draft + A–E 闭环 |
| NN-58 | [[Dropout 的方差、共适应解释与 Bayesian 边界]] | evidence boundary | draft + A–E 闭环 |
| NN-59 | [[DropConnect、权重噪声与激活噪声]] | noise location | draft + A–E 闭环 |
| NN-60 | [[Stochastic Depth、DropPath 与有效深度]] | random paths | draft + A–E 闭环 |
| NN-61 | [[Label Smoothing、置信度与目标偏置]] | target change | draft + A–E 闭环 |
| NN-62 | [[Mixup、Manifold Mixup 与插值正则]] | interpolation prior | draft + A–E 闭环 |
| NN-63 | [[Jacobian、Gradient Penalty 与 Lipschitz 正则接口]] | local derivative penalty | draft + A–E 闭环 |
| NN-64 | [[网络级正则化的交互、消融与证据地图]] | causal audit | draft + A–E 闭环 |

## 当前迁移与学习状态

- [[neural_network_foundations_teaching_contract_audit.py]]已复核 NN-57—64 的两遍路线、问题链、对象账本与 $\mathcal D_\square$；前半闭合 Dropout/DropConnect/DropPath 的随机位置账，后半闭合 target smoothing、vicinal interpolation、Jacobian norm/probe 与 factorial interaction；
- 当前为 **8/8 现行教学迁移、8/8 正文、8/8 A—E 题解、8/8 正式图，30.8 材料门 `regression-passed`**；
- 全章为 **64/64 已迁移、0/64 pending、分卷材料门 8/8 `regression-passed`**，个人仍为 **0/8 / `not-attempted`**；下一材料施工点为 NN-CUM-01 现行合同重审。

NN-57—64 共 120 道节点题及逐题独立详解已经形成静态闭环，并已纳入[[阶段测验 - 神经网络基础（第三章）|NN-CUM-01]]与[[实验 - 神经网络基础累计复现门]]。`draft` 只表示材料组成，学习者仍需闭卷、重做与迁移验收。
