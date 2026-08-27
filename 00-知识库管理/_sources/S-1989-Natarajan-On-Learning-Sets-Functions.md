---
type: source
status: active
area: [sources, learning-theory, multiclass]
source_type: paper
title: "On Learning Sets and Functions"
author: "B. K. Natarajan"
year: 1989
url: "https://doi.org/10.1007/BF00114804"
accessed: 2026-08-23
source_tier: A
license: "Publisher-copyrighted article; retain bibliographic data, independent definitions and DOI/author links only"
venue: "Machine Learning 4, 67–97"
scope_role: primary
temporal_role: classical-foundation
related: ["[[多分类的 Natarajan 维与 Graph 维]]", "[[二分类统计学习基本定理]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Natarajan：On Learning Sets and Functions

> [!abstract] 来源定位
> Natarajan 1989 研究从样例学习集合与多值函数的条件，并引出后来以作者命名的多分类组合维。课程用现代记号陈述 Natarajan shattering：每个点固定两个不同标签，再要求类实现全部逐点二选一模式。

## 元数据

- B. K. Natarajan, “On Learning Sets and Functions,” *Machine Learning* 4, 67–97, 1989；
- DOI：[10.1007/BF00114804](https://doi.org/10.1007/BF00114804)；
- CMU 技术报告版本：[Some Results on Learning](https://www.ri.cmu.edu/pub_files/pub3/natarajan_b_k_1989_1/natarajan_b_k_1989_1.pdf)；
- 课程调用：[[多分类的 Natarajan 维与 Graph 维]]的历史来源与必要容量坐标。

## 本库调用的断言

1. 多分类自由度不能只由标签总数 $K$ 描述；关键是同一批输入上可联合实现哪些标签模式；
2. Natarajan 打散把 binary shattering 推广为逐点两标签见证；
3. 二分类时这一定义退化为普通 VC 维；
4. 现代 PAC sample-complexity、Graph 维关系和 ERM 细节由后续教材与论文校准，不全部归因于 1989 原文。

> [!warning] 历史与现代定理分层
> 原论文研究的学习框架与现代教材的统一 PAC 记号并非逐字相同。课程保留历史来源，但 quantitative bound 以明确写出的现代假设为准。
