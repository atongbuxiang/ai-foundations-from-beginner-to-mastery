---
type: moc
status: active
area: [neural-networks/normalization]
prerequisites: ["[[初始化与信号传播 MOC]]"]
related: ["[[神经网络基础完整课程地图与掌握标准]]", "[[残差连接、深度与稳定性 MOC]]"]
created: 2026-08-23
updated: 2026-08-29
---
# 归一化、尺度与统计量 MOC
| ID | 节点 | 出口 | 状态 |
|---|---|---|---|
| NN-33 | [[归一化的对象、轴与不变性]] | axis contract | draft + A–E 闭环 |
| NN-34 | [[BatchNorm 前向统计与训练—推理差异]] | train/eval statistics | draft + A–E 闭环 |
| NN-35 | [[BatchNorm 反向传播、尺度不变性与噪声]] | coupled gradients | draft + A–E 闭环 |
| NN-36 | [[LayerNorm 的逐样本几何与反向传播]] | per-token normalization | draft + A–E 闭环 |
| NN-37 | [[RMSNorm、均值移除与缩放不变性]] | RMS-only scaling | draft + A–E 闭环 |
| NN-38 | [[InstanceNorm、GroupNorm 与 WeightNorm]] | normalization taxonomy | draft + A–E 闭环 |
| NN-39 | [[Pre-Norm、Post-Norm 与归一化放置]] | placement Jacobian | draft + A–E 闭环 |
| NN-40 | [[小批量、混合精度、分布式与因果归一化边界]] | systems boundary | draft + A–E 闭环 |

## 当前迁移与学习状态

- [[neural_network_foundations_teaching_contract_audit.py]]已复核 NN-33—40 的两遍路线、问题链、对象账本、$\mathcal N_\square$ 共享张量、BN/LN/RMSNorm 数值链、归一化族、残差放置与系统边界；
- 当前为 **8/8 现行教学迁移、8/8 正文、8/8 A—E 题解、8/8 正式图，30.5 材料门 `regression-passed`**；
- 全章为 **44/64 已迁移、20/64 pending、分卷材料门 5/8**，30.6 前半卷 `in-progress`，个人仍为 **0/8 / `not-attempted`**；下一批 NN-45—48。

NN-33—40 共 120 题与逐题详解已经形成静态课程闭环；其中后半从 RMSNorm 的几何与 VJP，推进到 Instance/Group/WeightNorm 的对象分类、Pre/Post-Norm 的精确 Jacobian，以及小批量、混合精度、分布式和因果统计边界。`draft` 只表示材料成稿，不表示学习者已经闭卷掌握。
