---
type: source
status: draft
area: [sources, neural-networks, dropout, regularization]
source_type: paper
title: "Dropout: A Simple Way to Prevent Neural Networks from Overfitting"
author: "Nitish Srivastava; Geoffrey Hinton; Alex Krizhevsky; Ilya Sutskever; Ruslan Salakhutdinov"
year: 2014
url: "https://www.jmlr.org/papers/v15/srivastava14a.html"
venue: "JMLR 15"
accessed: 2026-08-24
source_tier: A
license: "JMLR open-access paper；本库仅保存独立摘要、必要公式与链接"
scope_role: core
temporal_role: foundational
related: ["[[Dropout 的随机掩码、期望与 Inverted Scaling]]", "[[Dropout 的方差、共适应解释与 Bayesian 边界]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Srivastava et al.：Dropout

> [!abstract] 来源定位
> 论文系统化定义随机删除 units/connections 的 Dropout，讨论训练时 thinned networks、测试时权重缩放近似和多个任务上的经验结果。它承担历史方法与实验来源；本库使用 inverted scaling 重写当前实现合同，并不把“防止共适应”或“平均指数多个模型”升级为任意深网的精确定理。

## 方法边界

- 原始叙述常在训练时不放大保留激活、测试时乘 keep probability；现代 inverted dropout 把比例移到训练时；
- 对线性 preactivation，可匹配条件期望；经过非线性或多层随机组合后，单一 deterministic pass 一般不等于 stochastic predictors 的算术平均；
- 原论文的经验优势绑定数据、架构、placement、rate 与当时训练设置；
- unit、channel、token 或 path mask 是不同随机结构，不能仅靠名称互换。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| DO-C1 | Bernoulli mask 可定义一族共享参数的随机子网络 | 结构 | 明确 mask 位置与粒度 | 成立 |
| DO-C2 | inverted scaling 保持被 mask 张量的条件均值 | 概率 | mask 独立、keep rate $q>0$ | 精确 |
| DO-C3 | eval 网络严格等于所有随机深网输出的算术平均 | 非线性外推 | 一般 $E[f(X)]\ne f(E[X])$ | 错误 |
| DO-C4 | Dropout 必然改善任意任务的泛化 | 经验外推 | 架构、数据与调参依赖 | 不成立 |
