---
type: source
status: active
area: [sources, learning-theory, decision-trees, cart]
source_type: book
title: "Classification and Regression Trees"
author: [Leo Breiman, Jerome H. Friedman, Richard A. Olshen, Charles J. Stone]
year: 1984
url: "https://books.google.com/books?id=8k1DvQEACAAJ"
accessed: 2026-08-23
source_tier: A
license: "Chapman & Hall monograph; retain citation and independent derivations"
edition: "First edition"
scope_role: primary-textbook
temporal_role: classical-foundation
related: ["[[决策树、分裂准则与剪枝]]", "[[Bagging、Random Forest 与 Boosting]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Classification and Regression Trees

> [!abstract] 来源定位
> CART 专著把 recursive binary partition、classification/regression impurity、maximal-tree growth、cost-complexity pruning 与 honest error estimation组织成完整方法。它是本库树模型统计对象、greedy construction 与 pruning path 的经典骨架。

## 元数据与纳入

- 书目信息：[Google Books](https://books.google.com/books?id=8k1DvQEACAAJ)；
- ISBN：978-0-412-04841-8；
- 正式引用：Breiman, L., Friedman, J. H., Olshen, R. A. & Stone, C. J. (1984), Chapman & Hall；
- 证据角色：axis-aligned recursive partitions、leaf prediction、impurity decrease 与 minimal cost-complexity pruning；
- 边界：modern consistency、honesty、conditional inference 与 feature-importance bias 需后续专门理论。

## 本库调用的断言

1. regression/classification trees 通过 recursive splits 构造 piecewise-constant predictors；
2. split criterion 是 weighted node impurity decrease；
3. cost-complexity criterion 在 empirical fit 与 terminal-node count 之间取舍；
4. growing、pruning 与 estimating error 是不同数据使用环节；
5. greedy tree 不是 global optimal partition 的同义词。
