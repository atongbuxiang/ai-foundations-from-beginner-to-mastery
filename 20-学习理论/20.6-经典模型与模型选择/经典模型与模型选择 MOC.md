---
type: moc
status: active
area: [learning-theory/classical-models]
prerequisites: ["[[学习问题、决策与风险 MOC]]", "[[数据依赖复杂度、间隔与快率 MOC]]"]
assessment: "[[阶段测验 - 经典模型与模型选择（20.6）]]"
solution: "[[阶段测验解答 - 经典模型与模型选择（20.6）]]"
experiment: "[[实验 - 经典模型与模型选择累计复现门]]"
related: ["[[学习理论完整课程地图与掌握标准]]", "[[正定核、RKHS 与表示定理]]", "[[资格考 - 学习理论 I：从风险到算法依赖泛化（20.1—20.5）]]", "[[表示学习、度量学习与自监督 MOC]]"]
created: 2026-08-20
updated: 2026-08-28
---

# 经典模型与模型选择 MOC

> [!abstract] 本卷任务
> 以 risk、inductive bias、identifiability、stability 与 evaluation 为主线重新学习经典模型；不写成 API 手册，也不把 optimization convergence 当 statistical guarantee。

| ID | 节点 | 状态 |
|---|---|---|
| LT-41 | [[偏差—方差—噪声分解]] | draft + A–E 闭环 |
| LT-42 | [[正则化、交叉验证与模型选择]] | draft + A–E 闭环 |
| LT-43 | [[线性回归的统计学习理论]] | draft + A–E 闭环 |
| LT-44 | [[逻辑回归、复合损失与概率分类]] | draft + A–E 闭环 |
| LT-45 | [[支持向量机、最大间隔与核方法]] | draft + A–E 闭环 |
| LT-46 | [[核岭回归与 Gaussian Process 接口]] | draft + A–E 闭环 |
| LT-47 | [[决策树、分裂准则与剪枝]] | draft + A–E 闭环 |
| LT-48 | [[Bagging、Random Forest 与 Boosting]] | draft + A–E 闭环 |
| LT-49 | [[PCA 的统计估计与主子空间风险]] | draft + A–E 闭环 |
| LT-50 | [[K-Means、聚类风险与不可辨识性]] | draft + A–E 闭环 |
| LT-51 | [[潜变量模型、混合模型与 EM]] | draft + A–E 闭环 |
| LT-52 | [[模型可辨识性、选择与 Misspecification]] | draft + A–E 闭环 |

当前为 **12/12 正文，12/12 习题与独立详解，0/12 经真实作答验收**。

## 卷级材料门：MODEL-CUM-01

本卷现已建立[[阶段测验 - 经典模型与模型选择（20.6）|MODEL-CUM-01]]、[[阶段测验解答 - 经典模型与模型选择（20.6）|独立封存详解]]与[[实验 - 经典模型与模型选择累计复现门|三轨累计复现门]]。三轨分别以 diagonal fixed-design ridge 与 exact validation selection、六点 logistic/SVM/tree/bootstrap/boosting、对称 PCA/K-Means/mixture-EM/AIC-BIC 贯通十二节点；25 分钟口试、240 分钟闭卷、scorer nonce、跨轨 blind、非法合同、48 小时与 14 天迁移防止只背算法列表。

[[classical_models_cumulative_contract_audit.py]]不导入生成函数，独立复算谱 risk/selection、margin/tree/bootstrap/boost、PCA/K-Means/EM/selection arithmetic，并检查 canonical/固定 blind 双跑、SVG/XML/hash、输入保护与状态面。

本卷材料为 `regression-passed`；它建成时把全章卷级材料门推进到 **6/10**。全章当前已经是 **10/10 卷级材料门与 2/2 资格考材料门（LT-QUAL-01 / LT-QUAL-02）**；个人仍为 **0/10、0/2 / `not-attempted`**。正式认证还要求 `LT-QUAL-01 retained`，当前该个人前置未满足；下一步是按前置顺序执行个人证据。
