---
type: source
status: draft
area: [math/foundations, math/induction, math/combinatorics, math/proof]
source_type: textbook
title: "Book of Proof: Counting and Mathematical Induction"
author: "Richard Hammack"
year: 2025
url: "https://richardhammack.github.io/BookOfProof/index.html"
accessed: "2026-08-19"
source_tier: A
license: "CC BY-NC-ND 4.0；本卡仅保存独立摘要、短公式与章节定位"
site_category: [mathematics, proofs, induction, combinatorics]
series: "Book of Proof, Third Edition 3.4"
series_order: 5
scope_role: core
temporal_role: foundational
related: ["[[数学语言、逻辑与证明 MOC]]", "[[数学归纳、递归与组合计数]]", "[[S-2025-Hammack-Book-of-Proof-Proof-Methods]]", "[[S-2025-Hammack-Book-of-Proof-Relations-Functions]]", "[[S-2024-MIT-6.1200J-Predicates-Sets-Proofs]]"]
created: 2026-08-19
updated: 2026-08-19
---

# Book of Proof：Counting 与 Mathematical Induction

> [!abstract] 来源定位
> Hammack《Book of Proof》第3章提供lists、乘法/加减原理、排列、subsets、Pascal/binomial、容斥、multisets、pigeonhole与combinatorial proof；第10章提供ordinary/strong induction、smallest counterexample和Fibonacci案例。两章共同承担MATH-05的正式教材骨架。

## 元数据与纳入

- 作者页：[Book of Proof, Third Edition](https://richardhammack.github.io/BookOfProof/index.html)
- PDF：[Main.pdf](https://richardhammack.github.io/BookOfProof/Main.pdf)
- 版本：作者页说明2025-02-05发布3.4修订；
- Chapter 3：Counting，p. 65起；
- Chapter 10：Mathematical Induction，p. 180起；
- 证据角色：正式定义、proof templates、典型例题和组合论证；
- AI迁移、loop invariant、memoized computation DAG和beam search由本课程补入。

## 章节映射

| 章节 | 主题 | MATH-05调用 |
|---|---|---|
| 3.1 | Lists | Ordered objects与repetition |
| 3.2 | Multiplication Principle | Sequential choices |
| 3.3 | Addition/Subtraction | Disjoint cases与complement |
| 3.4 | Factorials/Permutations | Ordered no-repetition |
| 3.5 | Counting Subsets | Binomial coefficients |
| 3.6 | Pascal/Binomial | Recurrence与combinatorial proof |
| 3.7 | Inclusion–Exclusion | Overlap correction |
| 3.8 | Counting Multisets | Stars and bars接口 |
| 3.9 | Division/Pigeonhole | Multiplicity与collision |
| 3.10 | Combinatorial Proof | Bijection/double counting |
| 10.1 | Induction | Base、step、closure |
| 10.2 | Strong Induction | All-smaller hypothesis |
| 10.3 | Smallest Counterexample | Well-ordering form |
| 10.5 | Fibonacci | Recurrence与induction |

## 核心断言

| ID | 断言 | 类型 | 当前用途 |
|---|---|---|---|
| C1 | Base与uniform successor step推出所有自然数cases | Induction principle | MATH-05 proof contract |
| C2 | Strong induction与ordinary induction证明能力等价 | Theorem | Recursive decomposition |
| C3 | Smallest counterexample利用well-ordering重写induction | Method | Failure-object proof |
| C4 | Addition/product principles依赖disjointness与choice multiplicity | Counting theorem | Object modeling |
| C5 | Pascal identity、binomial theorem与inclusion–exclusion可用combinatorial proof | Theorem/method | Counting–recurrence bridge |
| C6 | Pigeonhole把finite map的size mismatch转成collision existence | Theorem | Hash/representation接口 |

## 本课程补严

1. 把induction看成base与step的index reachability，显式审计stride residues；
2. 增加structural/mutual induction和strengthened invariant；
3. 区分recursion、recurrence与induction；
4. 用well-founded measure分离termination与partial correctness；
5. 引入loop/state invariant；
6. 区分recursive tree和memoized DAG的实际成本；
7. 为stars-and-bars、bijection与double counting补足representation multiplicity；
8. 把自回归序列空间、beam search和DP作为AI迁移。

## 限制与保留意见

- 本卡不把教材例题原文搬入笔记，只保留章节定位与独立重建；
- 结构归纳、程序验证和Master theorem不是该书这两章的完整主线，需要MIT/算法教材补充；
- Infinite cardinality、advanced generating functions与analytic combinatorics不纳入MATH-05；
- 组合公式应用前仍需独立定义对象、顺序、重复和encoding multiplicity。

## 已生成与后续调用

- [x] [[数学归纳、递归与组合计数]]
- [x] [[习题 - 数学归纳、递归与组合计数]]
- [x] [[解答 - 数学归纳、递归与组合计数]]
- [x] [[实验 - 归纳覆盖、递归调用与组合计数审计]]
- [ ] [[渐近记号、增长率与复杂度]]：递归树和Master theorem的正式量词

## 交叉核对

- MIT 6.1200J Lectures 2/3：ordinary/strong induction；
- MIT 6.1200J Lecture 7：recurrence、Hanoi、selection/merge sort与recursion tree；
- MIT 6.1200J Lectures 15–17：counting techniques；
- [[S-2018-Su-5861-Seq2Seq与Beam-Search]]：AI search-tree案例。
