---
type: moc
status: active
area: [learning-theory/online]
prerequisites: ["[[PAC 学习与有限假设类 MOC]]", "[[镜像下降、Bregman 几何与自然梯度]]"]
assessment: "[[阶段测验 - 在线学习、Boosting 与序列预测（20.9）]]"
solution: "[[阶段测验解答 - 在线学习、Boosting 与序列预测（20.9）]]"
experiment: "[[实验 - 在线学习、Boosting 与序列预测累计复现门]]"
related: ["[[学习理论完整课程地图与掌握标准]]", "[[校准、不确定性与分布偏移 MOC]]", "[[深度泛化理论接口与开放边界 MOC]]"]
created: 2026-08-20
updated: 2026-08-29
---

# 在线学习、Boosting 与序列预测 MOC

> [!abstract] 本卷任务
> 从 batch population risk 切换到 sequential protocol、comparator 与 regret；连接 experts、OCO、perceptron、boosting、online-to-batch，并在 bandit 入口处停止。

| ID | 节点 | 关键出口 | 状态 |
|---|---|---|---|
| LT-69 | [[在线学习协议、Regret 与 Comparator]] | sequential object contract | draft + A–E 闭环 |
| LT-70 | [[Experts、Weighted Majority 与 Multiplicative Weights]] | expert regret proof | draft + A–E 闭环 |
| LT-71 | [[Online Gradient Descent 与 Mirror Descent]] | geometry-aware regret | draft + A–E 闭环 |
| LT-72 | [[随机、对抗与自适应序列的区别]] | adversary filtration contract | draft + A–E 闭环 |
| LT-73 | [[Perceptron Mistake Bound 与 Margin]] | finite mistake certificate | draft + A–E 闭环 |
| LT-74 | [[Boosting、弱学习与指数损失]] | weak-to-strong reduction | draft + A–E 闭环 |
| LT-75 | [[Online-to-Batch Conversion]] | regret-to-risk bridge | draft + A–E 闭环 |
| LT-76 | [[Bandit Feedback 与强化学习接口]] | partial-information boundary | draft + A–E 闭环 |

当前为 **8/8 正文、8/8 A—E 习题与独立详解，0/8 经真实作答验收**。

## 卷级材料门：ONLINE-CUM-01

本卷现已建立[[阶段测验 - 在线学习、Boosting 与序列预测（20.9）|ONLINE-CUM-01]]、[[阶段测验解答 - 在线学习、Boosting 与序列预测（20.9）|独立封存详解]]与[[实验 - 在线学习、Boosting 与序列预测累计复现门|三轨累计复现门]]。三轨分别以 full-information Hedge/OGD/adversary visibility、Perceptron/AdaBoost 双势能、online-to-batch/UCB/IPS/RL boundary 串起 LT-69—76；25 分钟口试、240 分钟闭卷、scorer nonce、跨轨 blind、非法合同、48 小时与 14 天迁移防止把更新式背诵误当成对协议边界的掌握。

[[online_boosting_cumulative_contract_audit.py]]不导入生成函数，独立复算 Hedge/OGD、Perceptron/AdaBoost、online-to-batch/UCB/IPS 锚点，并检查 canonical/固定 blind 双跑、SVG/XML/hash、输入保护和状态面。

本卷材料为 `regression-passed`；它建成时把全章卷级材料门推进到 **9/10**。全章当前已经是 **10/10 卷级材料门与 2/2 资格考材料门（LT-QUAL-01 / LT-QUAL-02）**；个人仍为 **0/10、0/2 / `not-attempted`**。正式认证要求 `REL-CUM-01 retained`，当前个人前置未满足；下一步是按前置顺序执行个人证据。
