---
type: source
status: active
area: [sources, learning-theory, no-free-lunch]
source_type: paper
title: "The Lack of A Priori Distinctions Between Learning Algorithms"
author: David H. Wolpert
year: 1996
url: "https://doi.org/10.1162/neco.1996.8.7.1341"
accessed: 2026-08-20
source_tier: A
license: "MIT Press copyrighted article; retain citation, independent summary and DOI link only"
venue: Neural Computation 8(7), 1341–1390
scope_role: original-theory
temporal_role: classical-foundation
related: ["[[No-Free-Lunch 与归纳偏置]]", "[[S-1984-Valiant-Theory-of-the-Learnable]]", "[[统计学习问题的对象合同]]"]
created: 2026-08-20
updated: 2026-08-20
---

# The Lack of A Priori Distinctions Between Learning Algorithms

> [!abstract] 来源定位
> Wolpert 1996 研究 off-training-set error，并形式化在对 target functions/priors 作对称平均时学习算法之间缺乏先验优势的若干意义。本库用它审计“算法无条件优越”的表述；LT-15 的具体 $1/7$—$1/8$ adversarial-distribution theorem 与证明常数则采用标准教材版本，避免把不同 NFL 定理揉成一句口号。

## 元数据与纳入

- DOI：[10.1162/neco.1996.8.7.1341](https://doi.org/10.1162/neco.1996.8.7.1341)；
- 正式引用：Wolpert, D. H. (1996), *The Lack of A Priori Distinctions Between Learning Algorithms*, Neural Computation 8(7), 1341–1390；
- 核心对象：off-training-set error、target/prior average、algorithm comparison；
- 当前调用者：[[No-Free-Lunch 与归纳偏置]]。

## 断言审计

| 断言 | 判断 |
|---|---|
| 无 target/prior 偏好时不能无条件排序所有算法 | 采用 |
| NFL 说明真实任务上所有算法表现相同 | 否定 |
| NFL 说明学习不可能 | 否定；它说明成功必须依赖任务结构/先验偏好 |
| 训练误差小本身足以推出未知点误差小 | 否定 |
| 架构、表示、augmentation 与 optimizer 都可编码归纳偏置 | 采用，具体效果仍需定理或实验 |

## 与教材 NFL 的边界

教材版本固定任意算法与有限样本量，再构造一个 realizable distribution，使算法以常数概率承受常数总体错误；Wolpert 论文强调 target/prior average 下的对称性。二者共享“没有无条件优越学习器”的主题，但概率空间、平均对象与命题形式不同。

## 已生成与后续调用

- [x] [[No-Free-Lunch 与归纳偏置]]：两类 NFL 分层、量词、构造与 AI 误读；
- [ ] [[深度泛化证据地图与开放问题]]：机制假设如何打破对称平均。
