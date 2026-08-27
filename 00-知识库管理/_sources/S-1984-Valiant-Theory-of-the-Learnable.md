---
type: source
status: active
area: [sources, learning-theory, computational-learning-theory]
source_type: paper
title: "A Theory of the Learnable"
author: Leslie G. Valiant
year: 1984
url: "https://doi.org/10.1145/1968.1972"
accessed: 2026-08-20
source_tier: A
license: "ACM-copyrighted article; retain citation, historical summary and DOI link only"
venue: Communications of the ACM 27(11), 1134–1142
scope_role: historical-backbone
temporal_role: classical-foundation
related: ["[[PAC 学习定义与样本复杂度]]", "[[可实现情形的一致 ERM 保证]]", "[[No-Free-Lunch 与归纳偏置]]"]
created: 2026-08-20
updated: 2026-08-20
---

# A Theory of the Learnable

> [!abstract] 来源定位
> Valiant 1984 把“可学习”放进明确的 learning protocol、概率近似和合理计算步数中，是计算学习理论的历史起点。课程用它解释 PAC 思想为何同时关心 information 与 computation；现代教材中的 realizable/agnostic PAC 定义、样本复杂度记号和 ERM 定理则由后续标准化框架承担，不把原始论文的具体 protocol 与现代版本逐字等同。

## 元数据与纳入

- 正式引用：Valiant, L. G. (1984), *A Theory of the Learnable*, CACM 27(11), 1134–1142；
- DOI：[10.1145/1968.1972](https://doi.org/10.1145/1968.1972)；
- 可读历史副本可从大学课程页面获得，但本库不重新分发；
- 当前调用者：[[PAC 学习定义与样本复杂度]]、[[可实现情形的一致 ERM 保证]]；
- 证据角色：历史动机、protocol/computation 思想，不作为现代 agnostic PAC 常数的唯一来源。

## 历史贡献的课程表达

1. 学习必须先指定信息如何取得，即 learning protocol；
2. 输出不需永远完全正确，而需以高概率在未知分布上近似正确；
3. 样本数与计算步数应随问题规模、精度和置信参数合理增长；
4. 不同 concept classes 的可学习性是可证明、可反驳的数学问题；
5. distribution-free 不等于没有归纳偏置：concept class 与 protocol 本身就是偏置。

## 现代化时必须补严

| 项目 | 原始历史语境 | 本课程现代合同 |
|---|---|---|
| 数据 | 特定 example oracle/protocol | 常用 $S\sim P^m$，另列 query/online variants |
| target | concept learning | 一般 loss 与 risk minimization |
| assumption | 以可实现概念为主 | realizable 与 agnostic 分列 |
| 输出 | recognition rule | proper/improper randomized learner |
| 资源 | polynomial examples/time | 统计样本复杂度与计算复杂度分账 |

## 断言账本

| 断言 | 当前判断 |
|---|---|
| Valiant 1984 奠定计算化“可学习”研究路线 | 采用 |
| 今天所有称 PAC 的定义都与原文 protocol 完全相同 | 不采用 |
| PAC 只关心样本数、不关心计算 | 历史上不准确；现代统计 PAC 常先单列 sample complexity |
| distribution-free 允许 learner 没有 class/protocol 假设 | 否定 |
| 经验成功一次就构成 learnability | 否定，缺全量词与算法保证 |

## 已生成与后续调用

- [x] [[PAC 学习定义与样本复杂度]]：历史—现代分层；
- [x] [[可实现情形的一致 ERM 保证]]：有限类的现代 finite-sample theorem；
- [ ] LT-15：inductive bias 与 No-Free-Lunch；
- [ ] LT-16：information lower bound 与 computational separation。
