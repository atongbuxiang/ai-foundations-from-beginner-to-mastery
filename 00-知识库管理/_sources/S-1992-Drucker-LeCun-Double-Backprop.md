---
type: source
status: draft
area: [sources, neural-networks, jacobian-regularization, double-backprop]
source_type: paper
title: "Improving Generalization Performance Using Double Backpropagation"
author: "Harris Drucker; Yann LeCun"
year: 1992
url: "https://doi.org/10.1109/72.165600"
venue: "IEEE Transactions on Neural Networks 3(6)"
accessed: 2026-08-24
source_tier: A
license: "IEEE journal article；本库仅保存独立摘要、必要结论与链接"
scope_role: historical-jacobian-penalty
temporal_role: foundational
related: ["[[Jacobian、Gradient Penalty 与 Lipschitz 正则接口]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Drucker、LeCun：Double Backpropagation

> [!abstract] 来源定位
> 论文把与输入敏感性/Jacobian 有关的附加能量加入标准训练，并通过再次反向传播优化。它承担输入导数正则的经典来源；现代 autodiff 的 `create_graph`、向量输出范数估计、鲁棒性与全局 Lipschitz 证书需要分别说明。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| DBP-C1 | 优化输入梯度 penalty 需要对梯度再求参数导数 | 算法 | 二阶/混合偏导可计算 | 精确 |
| DBP-C2 | 局部输入敏感性可作为训练正则 | 方法 | 声明输出/loss、norm、采样点 | 成立 |
| DBP-C3 | finite training points 的小梯度证明 global Lipschitz | 全局外推 | domain 未全覆盖 | 错误 |
| DBP-C4 | gradient penalty 必然提升泛化 | 经验外推 | strength/optimization/task 依赖 | 不成立 |
