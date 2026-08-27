---
type: source
status: draft
area: [sources, math/numerical-linear-algebra, math/krylov-methods]
source_type: course-notes
title: "Notes for Ma221 Lecture 13: Krylov subspace methods"
author: James Demmel
year: 2023
url: "https://people.eecs.berkeley.edu/~demmel/ma221_Fall23/Lectures/Lecture_13.pdf"
accessed: 2026-08-15
source_tier: A
license: "作者公开课程讲义；知识库仅保存独立摘要、推导映射与链接"
scope_role: canonical-worked-analysis
temporal_role: foundational-teaching
aliases: [Demmel-2023-Krylov-Arnoldi-Lanczos]
related: ["[[Lanczos 方法]]", "[[Arnoldi 方法]]", "[[Hessenberg 化与 QR 特征值算法]]", "[[幂法、反幂法与 Rayleigh 商迭代]]"]
created: 2026-08-15
updated: 2026-08-15
---

# Demmel：Krylov、Arnoldi 与 Lanczos 的投影主线

> [!abstract] 来源定位
> Berkeley Math 221 Lecture 13 从矩阵—向量乘黑盒出发，说明原始幂序列为何病态，再由正交基得到 Arnoldi Hessenberg 投影；对称性进一步把 Hessenberg 压缩为三对角 Lanczos 递推。它承担两个章节的主推导、成本和 Ritz 残差公式。

## 核心映射

| ID | 断言或工具 | 纳入位置 |
|---|---|---|
| K-D1 | $\mathcal K_k(A,q_1)=\operatorname{span}(q_1,Aq_1,\ldots,A^{k-1}q_1)$，但不应显式使用病态幂基 | 两章第三至五节 |
| K-D2 | Arnoldi 生成 $AV_k=V_kH_k+h_{k+1,k}v_{k+1}e_k^T$，$H_k$ 上 Hessenberg | [[Arnoldi 方法]]第六至八节 |
| K-D3 | 若 $A=A^T$，投影矩阵同时对称且 Hessenberg，故为三对角，得到三项 Lanczos 递推 | [[Lanczos 方法]]第五至七节 |
| K-D4 | $H_ky=\theta y$ 的 Ritz 向量 $V_ky$ 残差范数为 $|h_{k+1,k}e_k^Ty|$ | 两章 Ritz 章节 |
| K-D5 | Arnoldi 的主要额外成本为长正交化；Lanczos 的精确算术短递推依赖对称性 | 成本与失效边界 |
| K-D6 | Lanczos 极端 Ritz 值具有交错/单调结构，但浮点正交性丢失会改变现象 | [[Lanczos 方法]]收敛与有限精度章节 |

## 证据边界

- 三项递推的全局正交性首先是精确算术结论；浮点实现必须讨论重正交化和 ghost Ritz values；
- 小 Ritz 残差是后向/验收指标；非正规 Arnoldi 中不能无条件把它等同于小特征值前向误差；
- $k$ 次 matvec 不等于总成本只有 $k$ 次 matvec，Arnoldi 正交化、同步和存储可能主导；
- 讲义给出教学算法；生产重启、锁定和 shift-invert 契约由 Netlib/ARPACK 类来源补足。

## 生成节点

- [x] [[Lanczos 方法]]
- [x] [[Arnoldi 方法]]
- [x] 两章配套实验

