---
type: moc
status: active
area: [architecture, cnn, equivariance]
prerequisites: ["[[多线性映射、张量与缩并]]", "[[数列、极限与完备性的直觉]]", "[[残差连接、深度与稳定性 MOC]]"]
related: ["[[表示与模型架构完整课程地图与掌握标准]]", "[[循环网络、记忆与状态空间模型 MOC]]"]
created: 2026-08-24
updated: 2026-09-03
---

# 卷积、空间结构与等变性 MOC

> [!abstract] 当前主线
> 本卷从“局部模式应否跨位置复用”发动，而不是从 CNN 名称表发动。两波用同一个 $\mathcal C_\square$ 教学族依次建立结构偏置、离散相关、平移交换、多通道资源账、采样混叠、感受野、现代 block 与群等变证据边界。

## 两遍路线

- **第一遍：** ARCH-01 → 02 → 03 → 04，只要求能从结构任务写出窗口算术、解释共享与等变、算对 tensor shape；
- **第二遍：** 回到 boundary/stride/dilation/groups、反例与资源口径，再沿 ARCH-05—08 完成 sampling—RF—stage—group 证明链；
 - **状态边界：** 本卷 ARCH-01—08 为 8/8 `regression-passed`；全章现行教学迁移已推进至 ARCH-01—24（24/64），40.1—40.3 材料门占全章 3/8，个人仍为 `not-attempted`。

| ID | 节点 | 学习出口 | 状态 |
|---|---|---|---|
| ARCH-01 | [[结构化输入、归纳偏置与架构比较坐标]] | structure–symmetry–cost contract | `regression-passed` material / `not-attempted` learner |
| ARCH-02 | [[离散卷积、互相关与边界约定]] | exact local operator | `regression-passed` material / `not-attempted` learner |
| ARCH-03 | [[局部连接、参数共享与平移等变性]] | equivariance proof | `regression-passed` material / `not-attempted` learner |
| ARCH-04 | [[通道、卷积核、步幅、填充与膨胀的形状账本]] | tensor/FLOP ledger | `regression-passed` material / `not-attempted` learner |
| ARCH-05 | [[池化、下采样、混叠与不变性边界]] | sampling audit | `regression-passed` material / `not-attempted` learner |
| ARCH-06 | [[堆叠卷积、感受野与有效感受野]] | receptive-field derivation | `regression-passed` material / `not-attempted` learner |
| ARCH-07 | [[CNN 阶段、残差块与深度可分离卷积]] | backbone budget audit | `regression-passed` material / `not-attempted` learner |
| ARCH-08 | [[群卷积、等变网络与 CNN 证据地图]] | symmetry/evidence audit | `regression-passed` material / `not-attempted` learner |

 当前本卷为 **8/8 现行教学迁移、全章 3/8 分卷材料门、0/8 个人学习验收**；全章为 **ARCH-01—24（24/64）**。ARCH-01—08 已通过[[architecture_teaching_contract_audit.py]]的结构、题解、链接、独立数值与八图双跑回归；40.1 材料为 `regression-passed`，当前施工点已移至 ARCH-25—32，个人保持 `not-attempted`。
