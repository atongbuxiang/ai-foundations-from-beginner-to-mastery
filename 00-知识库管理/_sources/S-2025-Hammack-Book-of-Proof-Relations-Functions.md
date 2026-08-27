---
type: source
status: draft
area: [math/foundations, math/functions, math/relations, math/proof]
source_type: textbook
title: "Book of Proof: Relations and Functions"
author: "Richard Hammack"
year: 2025
url: "https://richardhammack.github.io/BookOfProof/index.html"
accessed: "2026-08-19"
source_tier: A
license: "CC BY-NC-ND 4.0；本卡仅保存独立摘要、短公式与章节定位"
site_category: [mathematics, proofs, functions, relations]
series: "Book of Proof, Third Edition 3.4"
series_order: 4
scope_role: "core"
temporal_role: "foundational"
related: ["[[数学语言、逻辑与证明 MOC]]", "[[函数、映射、关系与等价类]]", "[[集合、元素与集合运算]]", "[[必要条件、充分条件与证明方法]]", "[[S-2025-Hammack-Book-of-Proof-Logic]]", "[[S-2025-Hammack-Book-of-Proof-Proof-Methods]]"]
created: 2026-08-19
updated: 2026-08-19
---

# Book of Proof：Relations 与 Functions

> [!abstract] 来源定位
> Hammack《Book of Proof》第11—12章是MATH-04的正式教材主线：第11章从binary relation进入relation properties、equivalence relation、equivalence classes、partitions与modular classes；第12章系统处理function、injective/surjective、composition、inverse、image与preimage。课程在此基础上补入quotient well-definedness、factorization和AI映射合同。

## 元数据与纳入

- 作者页：[Book of Proof, Third Edition](https://richardhammack.github.io/BookOfProof/index.html)
- PDF：[Main.pdf](https://richardhammack.github.io/BookOfProof/Main.pdf)
- 当前版本：作者页说明2025-02-05发布3.4小修订版；
- Chapter 11：Relations，pp. 201起；
- Chapter 12：Functions，pp. 223起；
- 范围角色：MATH-04正式定义、例题与证明路径；
- 证据边界：AI例子和商上的factorization为本课程迁移/补充，不冒充原书直接结论。

## 章节结构

| 章节 | 子主题 | 本库调用 |
|---|---|---|
| 11.1 | Relations | $R\subseteq A\times B$、infix notation |
| 11.2 | Properties of Relations | Reflexive、symmetric、transitive |
| 11.3 | Equivalence Relations | “视为相同”的三项合同 |
| 11.4 | Equivalence Classes and Partitions | classes相同或不交、partition correspondence |
| 11.5 | Integers Modulo $n$ | 商集与代表元的基础例子 |
| 11.6 | Relations Between Sets | 跨集合relation接口 |
| 12.1 | Functions | 函数、graph、domain/codomain |
| 12.2 | Injective and Surjective | 碰撞与覆盖 |
| 12.3 | Pigeonhole Principle Revisited | 有限基数接口 |
| 12.4 | Composition | 类型顺序、结合律 |
| 12.5 | Inverse Functions | 双射与inverse |
| 12.6 | Image and Preimage | 子集的forward/pullback |

## 核心断言

| ID | 断言 | 类型 | 当前用途 |
|---|---|---|---|
| C1 | Relation可表示为Cartesian product的subset | Definition | Function作为特殊relation |
| C2 | Equivalence relation由reflexive、symmetric、transitive组成 | Definition | Classes与quotient |
| C3 | Equivalence classes形成partition，partition反生relation | Theorem | 商结构骨架 |
| C4 | Function的injectivity与surjectivity分别控制碰撞和codomain coverage | Definition/theorem | Mapping audit |
| C5 | Bijective function具有inverse function | Theorem | Flow与编码接口 |
| C6 | Image与preimage承担不同集合运算性质 | Theorem/examples | MATH-04逐元素证明 |

## 本课程的补严

1. 把function明确定为domain、codomain与graph的typed object；
2. 区分preimage notation与inverse function；
3. 系统证明$f^{-1}$保持并、交、补，而$f$对交通常只有包含；
4. 增加left inverse/right inverse与单双射的方向；
5. 把quotient上的representative independence提升为独立proof obligation；
6. 给出constant-on-classes factorization theorem；
7. 用classifier、softmax、flow、random pipeline与parameter symmetry做AI迁移；
8. 用完整finite enumeration交叉检查Bell number、集合律与descending maps。

## 限制与保留意见

- 教材主要面向proof入门，不以AI或quotient universal property为主线；
- 不同教材对partial function和codomain是否纳入function identity的约定可能不同，本库局部声明；
- 教材例题可支持学习路线，但本库正文与解答保持独立表述，不复制原文；
- 书中cardinality后续内容留给组合计数/无限集合接口，本节点不扩张范围。

## 已生成与后续调用

- [x] [[函数、映射、关系与等价类]]
- [x] [[习题 - 函数、映射、关系与等价类]]
- [x] [[解答 - 函数、映射、关系与等价类]]
- [x] [[实验 - 有限映射、逆像恒等式与商上良定义性审计]]
- [ ] [[数学归纳、递归与组合计数]]：有限函数计数与pigeonhole接口

## 交叉核对

- MIT 6.1200J Spring 2024 Lecture 15：relations、total functions、injective/surjective、equivalence relation与partitions；
- [[S-2024-MIT-6.1200J-Predicates-Sets-Proofs]]；
- [[S-2018-Su-5776-NICE流模型]]：bijection在AI生成模型中的调用；
- [[S-2020-Su-7681-L2正则与尺度不变性]]：parameter-to-function map的fibers；
- [[S-2024-Su-10347-位置编码与置换对称]]：equivariance与symmetry边界。
