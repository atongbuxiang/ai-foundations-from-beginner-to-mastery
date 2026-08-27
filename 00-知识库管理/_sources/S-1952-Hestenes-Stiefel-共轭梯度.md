---
type: source
status: draft
area: [sources, math/numerical-linear-algebra, math/krylov-methods]
source_type: original-paper
title: "Methods of Conjugate Gradients for Solving Linear Systems"
author: "Magnus R. Hestenes and Eduard Stiefel"
year: 1952
url: "https://nvlpubs.nist.gov/nistpubs/jres/049/jresv49n6p409_A1b.pdf"
accessed: 2026-08-15
source_tier: A
license: "NIST/NBS 历史期刊公开 PDF；知识库保存独立摘要、推导映射与链接"
scope_role: original-algorithm
temporal_role: foundational
aliases: [Hestenes-Stiefel-1952-CG]
related: ["[[共轭梯度法]]", "[[Lanczos 方法]]", "[[Krylov 子空间与预条件]]"]
created: 2026-08-15
updated: 2026-08-15
---

# Hestenes–Stiefel：共轭梯度法的原始算法

> [!abstract] 来源定位
> 1952 年原始论文给出用共轭方向求解线性系统的有限步算法，并把它与消元、正交多项式和椭球几何联系起来。正文以现代 SPD、Krylov 与能量最小化语言重建算法；原论文承担历史与原创算法依据。

## 核心映射

| ID | 原始贡献 | 纳入位置 |
|---|---|---|
| HS-1 | 以相互共轭方向逐步消去误差分量 | [[共轭梯度法]]几何章节 |
| HS-2 | 精确算术中至多 $n$ 步得到 $n$ 维线性系统解 | 有限终止定理 |
| HS-3 | 算法只需矩阵作用、内积与向量递推 | 基本算法与成本 |
| HS-4 | 与消元和正交多项式存在结构联系 | Lanczos/Krylov 连接 |

## 证据边界

- 现代常用三项递推的数值行为需结合后续有限精度分析；
- “至多 $n$ 步”是精确算术陈述，浮点中共轭性会丢失且真残差可能与递推残差分离；
- 非对称或不定矩阵不满足本章 SPD 最小化框架，应选 MINRES、SYMMLQ、GMRES 等适配算法。

## 生成节点

- [x] [[共轭梯度法]]历史、共轭方向与有限终止章节
