---
type: source
status: draft
area: [sources, ai/attention, algorithms/complexity]
source_type: blog
title: "线性Attention的探索：Attention必须有个Softmax吗？"
author: 苏剑林
year: 2020
url: "https://spaces.ac.cn/archives/7546"
accessed: 2026-08-19
source_tier: C
license: "科学空间站点声明存在版本差异；仅保存独立摘要、短公式与链接"
site_category: [信息时代, attention]
scope_role: bridge
temporal_role: foundational
related: ["[[渐近记号、增长率与复杂度]]", "[[实验 - 增长率、有限窗口与 Attention 成本审计]]"]
created: 2026-08-19
updated: 2026-08-19
---

# 线性Attention的探索：Attention必须有个Softmax吗？

> [!abstract] 来源定位
> 文章从标准Attention的$T\times T$中间矩阵进入，讨论替换归一化/相似度并利用矩阵结合律先计算$K^\top V$，从而把关于序列长度的二次依赖改成近线性依赖。它是MATH-08连接渐近语言与真实operation graph的中文问题入口，不独立承担Big-$O$定义、所有线性Attention方法的结论或硬件性能保证。

## 纳入判定

- 范围角色：`bridge`；
- 年代角色：`foundational`；
- 调用目的：训练“先写shape、再重关联、最后比较资源”的复杂度审计；
- 不承担：一般渐近定理、统一的线性Attention质量结论和wall-clock结论。

## 结构摘要

$$
\operatorname{softmax}(QK^\top)V
\quad\longrightarrow\quad
\phi(Q)\bigl(\phi(K)^\top V\bigr).
$$

若$Q,K\in\mathbb R^{T\times r}$、$V\in\mathbb R^{T\times d}$，先形成$QK^\top$需要$\Theta(T^2r)$级work并产生$T\times T$对象；重关联后两个乘法约为$\Theta(Trd)$。这只在feature map、normalization与因果实现合法时成立。

## 核心断言与核验

| ID | 断言 | 类型 | 条件/边界 | 当前判断 |
|---|---|---|---|---|
| C1 | 标准dense Attention对序列长度含二次score矩阵 | operation shape | dense all-pairs、显式或逻辑访问全部pairs | 已核验 |
| C2 | 去掉/替换Softmax后可利用结合律先算$K^\top V$ | 代数机制 | 不能把非线性Softmax直接穿过乘法 | 已核验 |
| C3 | 固定feature/width时序列依赖可降到线性 | 渐近结论 | $r,d$相对$T$固定，含normalization与causal账 | 条件性成立 |
| C4 | 线性复杂度必然更快或更好 | 工程/质量外推 | 硬件、常数、数值稳定与表达质量未统一 | 不成立 |

## 限制与保留意见

- “线性Attention”是方法族，不是单一算法；
- 标准Softmax的非线性阻止直接使用普通结合律；
- Feature rank若随$T$增长，线性结论需重写；
- Causal streaming、denominator、mask与backward各有额外义务；
- FLOP减少不自动降低memory traffic或wall-clock；
- 本地不复制原文，只保留独立推导骨架与边界。

## 当前调用

- [x] [[渐近记号、增长率与复杂度]]；
- [x] [[实验 - 增长率、有限窗口与 Attention 成本审计]]；
- [ ] 后续长上下文/高效Attention专题。

