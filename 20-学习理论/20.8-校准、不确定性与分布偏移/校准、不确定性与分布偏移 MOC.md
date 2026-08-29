---
type: moc
status: active
area: [learning-theory/reliability]
prerequisites: ["[[学习问题、决策与风险 MOC]]", "[[概率论与数理统计 MOC]]"]
assessment: "[[阶段测验 - 校准、不确定性与分布偏移（20.8）]]"
solution: "[[阶段测验解答 - 校准、不确定性与分布偏移（20.8）]]"
experiment: "[[实验 - 校准、不确定性与分布偏移累计复现门]]"
related: ["[[学习理论完整课程地图与掌握标准]]", "[[表示学习、度量学习与自监督 MOC]]", "[[在线学习、Boosting 与序列预测 MOC]]"]
created: 2026-08-20
updated: 2026-08-29
---

# 校准、不确定性与分布偏移 MOC

> [!abstract] 本卷任务
> 把 accuracy、probability quality、coverage、uncertainty 与 shift robustness 分成不同可验证目标；每个 distribution-shift correction 都必须声明可识别假设。

| ID | 节点 | 关键出口 | 状态 |
|---|---|---|---|
| LT-61 | [[概率校准、Proper Scoring Rule 与可靠性图]] | calibration/scoring separation | draft + A–E 闭环 |
| LT-62 | [[Aleatoric、Epistemic 与模型不确定性]] | uncertainty taxonomy | draft + A–E 闭环 |
| LT-63 | [[Bayesian Posterior Predictive、Ensemble 与近似边界]] | source of predictive spread | draft + A–E 闭环 |
| LT-64 | [[Conformal Prediction 与有限样本 Coverage]] | exchangeable marginal coverage | draft + A–E 闭环 |
| LT-65 | [[Covariate、Label 与 Concept Shift]] | shift taxonomy | draft + A–E 闭环 |
| LT-66 | [[重要性加权与 Covariate Shift 校正]] | target-risk reweighting | draft + A–E 闭环 |
| LT-67 | [[Domain Adaptation 与 Domain Generalization Bound]] | discrepancy + shared task | draft + A–E 闭环 |
| LT-68 | [[OOD、鲁棒性与因果不变性的边界]] | robustness/causality separation | draft + A–E 闭环 |

当前为 **8/8 正文、8/8 A–E 习题与独立详解，0/8 经真实作答验收**。

## 卷级材料门：REL-CUM-01

本卷现已建立[[阶段测验 - 校准、不确定性与分布偏移（20.8）|REL-CUM-01]]、[[阶段测验解答 - 校准、不确定性与分布偏移（20.8）|独立封存详解]]与[[实验 - 校准、不确定性与分布偏移累计复现门|三轨累计复现门]]。三轨分别以 calibration/proper score/predictive mixture、split-conformal rank/importance weighting/overlap、domain discrepancy/OOD threshold/group risk 串起 LT-61—68；25 分钟口试、240 分钟闭卷、scorer nonce、跨轨 blind、非法合同、48 小时与 14 天迁移防止把“更可靠”写成无对象的总评。

[[calibration_shift_cumulative_contract_audit.py]]不导入生成函数，独立复算 Brier/total variance、conformal/importance、adaptation/OOD/group 数学锚点，并检查 canonical/固定 blind 双跑、SVG/XML/hash、输入保护和状态面。

本卷材料为 `regression-passed`；它建成时把全章卷级材料门推进到 **8/10**。全章当前已经是 **10/10 卷级材料门与 2/2 资格考材料门（LT-QUAL-01 / LT-QUAL-02）**；个人仍为 **0/10、0/2 / `not-attempted`**。正式认证要求 `REPR-CUM-01 retained`，当前个人前置未满足；下一步是按前置顺序执行个人证据。
