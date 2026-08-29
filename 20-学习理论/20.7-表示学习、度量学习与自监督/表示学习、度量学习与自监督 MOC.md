---
type: moc
status: active
area: [learning-theory/representation]
prerequisites: ["[[学习问题、决策与风险 MOC]]", "[[互信息与依赖性]]"]
assessment: "[[阶段测验 - 表示学习、度量学习与自监督（20.7）]]"
solution: "[[阶段测验解答 - 表示学习、度量学习与自监督（20.7）]]"
experiment: "[[实验 - 表示学习、度量学习与自监督累计复现门]]"
related: ["[[学习理论完整课程地图与掌握标准]]", "[[深度泛化理论接口与开放边界 MOC]]", "[[经典模型与模型选择 MOC]]", "[[校准、不确定性与分布偏移 MOC]]"]
created: 2026-08-20
updated: 2026-08-28
---

# 表示学习、度量学习与自监督 MOC

> [!abstract] 本卷任务
> 不把“预训练有效”当作表示理论。明确 pretext/downstream task、augmentation law、positive/negative sampling、batch coupling、collapse 与 evaluation protocol。

| ID | 节点 | 关键出口 | 状态 |
|---|---|---|---|
| LT-53 | [[表示学习的任务、表示与下游风险]] | representation contract | draft + A–E 闭环 |
| LT-54 | [[度量学习、相似性与检索风险]] | geometry/evaluation alignment | draft + A–E 闭环 |
| LT-55 | [[对比学习、InfoNCE 与密度比]] | objective interpretation | draft + A–E 闭环 |
| LT-56 | [[正负样本、Batch 依赖与梯度估计]] | batch changes objective | draft + A–E 闭环 |
| LT-57 | [[数据增强、不变性、等变性与任务充分性]] | augmentation validity | draft + A–E 闭环 |
| LT-58 | [[表示坍缩、非坍缩与可辨识边界]] | collapse certificates | draft + A–E 闭环 |
| LT-59 | [[遮蔽预测、Teacher–Student 与自监督目标]] | target-generation contract | draft + A–E 闭环 |
| LT-60 | [[Linear Probe、Fine-Tuning 与迁移评估]] | probe inference boundary | draft + A–E 闭环 |

当前为 **8/8 正文、8/8 A–E 题解闭环，0/8 经真实作答验收**。

## 卷级材料门：REPR-CUM-01

本卷现已建立[[阶段测验 - 表示学习、度量学习与自监督（20.7）|REPR-CUM-01]]、[[阶段测验解答 - 表示学习、度量学习与自监督（20.7）|独立封存详解]]与[[实验 - 表示学习、度量学习与自监督累计复现门|三轨累计复现门]]。三轨分别以 task-indexed representation/metric/retrieval/dependent views、exact candidate-index InfoNCE/batch gradient/false negatives、covariance/VICReg/EMA/masked target 串起 LT-53—60；25 分钟口试、240 分钟闭卷、scorer nonce、跨轨 blind、非法合同、48 小时与 14 天迁移防止把方法名或 benchmark 排名当作理论掌握。

[[representation_selfsupervised_cumulative_contract_audit.py]]不导入生成函数，独立复算 task risk、InfoNCE candidate law、softmax gradient、collision、谱秩、VICReg 与 teacher target 锚点，并检查 canonical/固定 blind 双跑、SVG/XML/hash、输入保护和状态面。

本卷材料为 `regression-passed`；它建成时把全章卷级材料门推进到 **7/10**。全章当前已经是 **10/10 卷级材料门与 2/2 资格考材料门（LT-QUAL-01 / LT-QUAL-02）**；个人仍为 **0/10、0/2 / `not-attempted`**。正式认证还要求 `MODEL-CUM-01 retained`，当前个人前置未满足；下一步是按前置顺序执行个人证据。
