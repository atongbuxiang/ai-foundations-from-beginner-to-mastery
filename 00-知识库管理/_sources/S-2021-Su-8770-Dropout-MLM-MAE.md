---
type: source
status: draft
area: [sources, neural-networks, dropout, self-supervised-learning]
source_type: blog
title: "Dropout视角下的MLM和MAE：一些新的启发"
author: "苏剑林"
year: 2021
url: "https://spaces.ac.cn/archives/8770"
accessed: 2026-08-24
source_tier: C
license: "科学空间页面声明 CC BY-NC-SA；本库仅保存独立摘要、必要短公式与链接"
scope_role: problem-entry
temporal_role: modern-perspective
related: ["[[Dropout 的方差、共适应解释与 Bayesian 边界]]", "[[遮蔽预测、Teacher–Student 与自监督目标]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 苏剑林：Dropout 视角下的 MLM 与 MAE

> [!abstract] 来源定位
> 文章从随机遮蔽/信息删除的共同结构重新观察 Dropout、MLM 与 MAE，并据此提出目标一致性和防过拟合启发。它适合作为跨任务问题入口；MLM corruption、MAE patch masking 与隐层 Bernoulli dropout 的概率对象、重建目标和 evaluation protocol 仍必须分开。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| SDM-C1 | 三类方法都可含随机信息删除 | 结构类比 | 指明被删对象与目标 | 成立 |
| SDM-C2 | 因都使用 mask，三者训练目标相同 | 对象外推 | prediction target/condition 不同 | 错误 |
| SDM-C3 | corruption 视角可启发一致性与正则化设计 | 研究入口 | 需独立实验/理论验收 | 有价值 |
| SDM-C4 | 博客类比替代原论文的泛化或 Bayesian 证明 | 证据层混淆 | 需要正式来源 | 不成立 |
