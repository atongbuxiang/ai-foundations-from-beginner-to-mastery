---
type: moc
status: active
area: [architecture, graph-neural-networks]
related: ["[[表示与模型架构完整课程地图与掌握标准]]"]
created: 2026-08-24
updated: 2026-09-03
---

# 图表示与消息传递神经网络 MOC

> [!abstract] 分卷出口
> 从“图是节点重标号等价类”出发，能推导等变 MPNN、谱—空间 GCN、GIN/GAT 与 invariant readout；能严格区分 over-smoothing、over-squashing 和 1-WL 表达边界，并把模型定义、构图、split、实验和系统证据分层。

> [!info] 当前教学迁移
> ARCH-17—24 已以三节点路径 $\mathcal G_\square$ 和六环反例完成整卷迁移：从重标号矩阵、同步消息传递，走到过平滑/过挤压、GAT、图级 readout 与 1-WL 边界。本卷为 **8/8 `regression-passed` material**；全章为 **ARCH-01—24（24/64）**、材料门 **3/8**，个人仍为 `not-attempted`。

| ID | 节点 | 学习出口 | 状态 |
|---|---|---|---|
| ARCH-17 | [[图数据、节点重标号与置换对称性]] | graph symmetry contract | `regression-passed` material / learner `not-attempted` |
| ARCH-18 | [[消息传递神经网络的统一形式]] | message-passing derivation | `regression-passed` material / learner `not-attempted` |
| ARCH-19 | [[谱图卷积、空间图卷积与归一化邻接]] | spectral/spatial bridge | `regression-passed` material / learner `not-attempted` |
| ARCH-20 | [[聚合器、可辨识性与 Graph Isomorphism Network]] | multiset injectivity | `regression-passed` material / learner `not-attempted` |
| ARCH-21 | [[图网络深度、过平滑与过挤压]] | depth failure audit | `regression-passed` material / learner `not-attempted` |
| ARCH-22 | [[图注意力与结构偏置]] | graph attention | `regression-passed` material / learner `not-attempted` |
| ARCH-23 | [[图级读出、异构图与任务接口]] | invariant readout | `regression-passed` material / learner `not-attempted` |
| ARCH-24 | [[WL 表达界、反例与 GNN 证据地图]] | expressivity evidence | `regression-passed` material / learner `not-attempted` |

## 科学空间的使用边界

- [[S-2019-Su-7006-InfoMap社区发现]]：社区发现/随机游走任务桥，不替代 MPNN；
- [[S-2023-Su-9359-热方程自监督]]：扩散和平滑直觉桥，不把欧氏 PDE 等同图热方程；
- [[S-2022-Su-9147-Hubness]]：kNN 构图风险桥，不承担 WL/GNN 表达定理；
- GCN、MPNN、GIN、GAT、R-GCN、WL 及深层失效结论以原论文为一级来源。

## 静态材料

- 正文：8 / 8；
- 习题与独立详解：120 / 120；
- 正式图：8 / 8；
- 数值/组合审计：[[00-知识库管理/_labs/code/architecture_gnn_audit.py]]；
- 真实学习验收：尚未作答或评分。

## 当前施工边界

- 已迁移：ARCH-17—24，8/8；
- 本卷主线已闭合：用同一 $\mathcal G_\square$ 与六环/三角形反例贯通过平滑、过挤压、GAT、readout 与 1-WL；
- 分卷材料门：已通过八图、精确算例、链接与确定性回归，升级为 `regression-passed`；下一施工点为 ARCH-25—32。
