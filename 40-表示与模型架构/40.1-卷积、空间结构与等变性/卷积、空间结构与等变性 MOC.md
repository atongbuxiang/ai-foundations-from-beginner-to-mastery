---
type: moc
status: active
area: [architecture, cnn, equivariance]
prerequisites: ["[[多线性映射、张量与缩并]]", "[[数列、极限与完备性的直觉]]", "[[残差连接、深度与稳定性 MOC]]"]
related: ["[[表示与模型架构完整课程地图与掌握标准]]", "[[循环网络、记忆与状态空间模型 MOC]]"]
created: 2026-08-24
updated: 2026-08-29
---

# 卷积、空间结构与等变性 MOC

> [!abstract] 当前主线
> 本卷从“局部模式应否跨位置复用”发动，而不是从 CNN 名称表发动。首波用同一个 $\mathcal C_\square$ 信号依次建立结构偏置、离散相关、平移交换关系和多通道资源账；下一波将把采样、感受野、现代 block 与群等变接到同一合同。

## 两遍路线

- **第一遍：** ARCH-01 → 02 → 03 → 04，只要求能从结构任务写出窗口算术、解释共享与等变、算对 tensor shape；
- **第二遍：** 回到 boundary/stride/dilation/groups、反例与资源口径，再进入 ARCH-05—08；
- **状态边界：** ARCH-01—04 的材料迁移为 4/64 中的首波，个人仍为 `not-attempted`。

| ID | 节点 | 学习出口 | 状态 |
|---|---|---|---|
| ARCH-01 | [[结构化输入、归纳偏置与架构比较坐标]] | structure–symmetry–cost contract | `regression-passed` material / `not-attempted` learner |
| ARCH-02 | [[离散卷积、互相关与边界约定]] | exact local operator | `regression-passed` material / `not-attempted` learner |
| ARCH-03 | [[局部连接、参数共享与平移等变性]] | equivariance proof | `regression-passed` material / `not-attempted` learner |
| ARCH-04 | [[通道、卷积核、步幅、填充与膨胀的形状账本]] | tensor/FLOP ledger | `regression-passed` material / `not-attempted` learner |
| ARCH-05 | [[池化、下采样、混叠与不变性边界]] | sampling audit | draft + A–E 闭环 |
| ARCH-06 | [[堆叠卷积、感受野与有效感受野]] | receptive-field derivation | draft + A–E 闭环 |
| ARCH-07 | [[CNN 阶段、残差块与深度可分离卷积]] | backbone budget audit | draft + A–E 闭环 |
| ARCH-08 | [[群卷积、等变网络与 CNN 证据地图]] | symmetry/evidence audit | draft + A–E 闭环 |

当前为 **8/8 旧正文与题解存在、4/8 现行教学迁移、0/8 个人学习验收**。ARCH-01—04 已通过[[architecture_teaching_contract_audit.py]]；ARCH-05—08 尚待迁移，因此 40.1 材料门仍为 0/8，下一施工点为 ARCH-05—08。
