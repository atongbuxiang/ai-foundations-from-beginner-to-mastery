---
type: moc
status: active
area: [neural-networks/normalization]
prerequisites: ["[[初始化与信号传播 MOC]]"]
related: ["[[神经网络基础完整课程地图与掌握标准]]", "[[残差连接、深度与稳定性 MOC]]"]
created: 2026-08-23
updated: 2026-08-23
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

当前为 **8/8 正文、8/8 A—E 题解闭环、0/8 真实验收**。NN-33—40 共 120 题与逐题详解已经形成静态课程闭环；其中后半从 RMSNorm 的几何与 VJP，推进到 Instance/Group/WeightNorm 的对象分类、Pre/Post-Norm 的精确 Jacobian，以及小批量、混合精度、分布式和因果统计边界。`draft` 只表示材料成稿，不表示学习者已经闭卷掌握。下一批进入 30.6 的 NN-41—44。
