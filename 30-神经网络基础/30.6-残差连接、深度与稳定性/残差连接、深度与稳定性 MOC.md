---
type: moc
status: active
area: [neural-networks/residual-stability]
prerequisites: ["[[归一化、尺度与统计量 MOC]]", "[[线性 ODE 与矩阵指数]]"]
related: ["[[神经网络基础完整课程地图与掌握标准]]", "[[Embedding、权重共享与输出参数化 MOC]]"]
created: 2026-08-23
updated: 2026-08-23
---
# 残差连接、深度与稳定性 MOC
| ID | 节点 | 出口 | 状态 |
|---|---|---|---|
| NN-41 | [[残差学习、恒等捷径与退化问题]] | identity shortcut | draft + A–E 闭环 |
| NN-42 | [[残差块 Jacobian 与梯度直通]] | $I+J_F$ | draft + A–E 闭环 |
| NN-43 | [[ResNet 的 ODE 与离散动力系统视角]] | Euler interpretation | draft + A–E 闭环 |
| NN-44 | [[残差缩放、Lipschitz 界与深度稳定性]] | perturbation control | draft + A–E 闭环 |
| NN-45 | [[Pre-Activation、Pre-Norm 与 Post-Norm 残差]] | placement | draft + A–E 闭环 |
| NN-46 | [[Highway、Dense Connection 与 Skip 结构比较]] | skip taxonomy | draft + A–E 闭环 |
| NN-47 | [[ReZero、Fixup、DeepNorm 与深网缩放]] | ultra-deep scaling | draft + A–E 闭环 |
| NN-48 | [[深度、有效路径与稳定性证据地图]] | evidence ledger | draft + A–E 闭环 |

当前为 **8/8 正文、8/8 A—E 题解闭环、0/8 真实验收**。NN-41—48 共 120 题与逐题详解已经形成静态课程闭环：从 identity baseline、$I+J_F$、ResNet–Euler 与缩放稳定性，推进到 activation/norm placement、add/gate/concat/cross-scale skip、ReZero/Fixup/DeepNorm，以及 depth 坐标—有效路径—证据层的卷终审计。`draft` 只表示材料完备，学习者仍需闭卷、重做与迁移验收；下一批进入 NN-49—52。
