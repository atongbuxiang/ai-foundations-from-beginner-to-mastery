---
type: source
status: verified
area: [sources, implicit-bias, gradient-descent, max-margin]
source_type: paper
title: "The Implicit Bias of Gradient Descent on Separable Data"
author: [Daniel Soudry, Elad Hoffer, Mor Shpigel Nacson, Suriya Gunasekar, Nathan Srebro]
year: 2018
url: "https://jmlr.org/papers/v19/18-188.html"
accessed: 2026-08-23
source_tier: A
license: "Open JMLR article; retain citation and theorem conditions"
venue: "JMLR 19(70)"
scope_role: primary
temporal_role: modern-theory
related: ["[[隐式偏置、最大间隔与优化选择]]"]
created: 2026-08-23
updated: 2026-08-26
---
# Implicit Bias of GD on Separable Data
> [!abstract] 来源定位
> 证明 homogeneous linear separable logistic-type 问题中 GD predictor direction 趋向 hard-margin SVM。本库分开 loss→0、norm→∞ 与 direction convergence；不无条件外推深网/Adam。
## 本库调用
1. separable logistic dynamics；
2. max-margin direction；
3. exponential-tail loss；
4. support-vector asymptotics；
5. slow directional convergence。

## 已核对断言与边界

- 主结论的基准对象是线性可分数据上的无显式正则 logistic regression、homogeneous linear predictor 与 gradient descent；预测方向趋向 hard-margin SVM，而参数范数本身发散；
- 论文还讨论特定单调尾部损失、多类问题和受限深网层设置，但这不等于任意深网、Adam 或有限训练预算自动具有相同隐式偏置；
- direction convergence 很慢，必须把 training error、loss、norm 与 normalized direction 四条轨迹分开；本章据此约束 [[Critical Batch、隐式偏置与 SGD 证据地图]] 的外推范围。

核对入口：[JMLR 论文页](https://jmlr.org/papers/v19/18-188.html)；访问日 2026-08-26。
