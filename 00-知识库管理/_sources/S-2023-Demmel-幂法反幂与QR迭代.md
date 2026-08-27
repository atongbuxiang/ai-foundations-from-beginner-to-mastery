---
type: source
status: draft
area: [sources, math/numerical-linear-algebra, math/spectral-methods]
source_type: course-notes
title: "Notes for Ma221 Lectures 9–10: Eigenvalue algorithms"
author: James Demmel
year: 2023
url: "https://people.eecs.berkeley.edu/~demmel/ma221_Fall23/Lectures/Lecture_09.pdf"
accessed: 2026-08-15
source_tier: A
license: "作者公开课程讲义；知识库仅保存独立摘要、推导映射与链接"
scope_role: canonical-worked-analysis
temporal_role: foundational-teaching
aliases: [Demmel-2023-Power-Inverse-QR-Iteration]
related: ["[[幂法、反幂法与 Rayleigh 商迭代]]", "[[Hessenberg 化与 QR 特征值算法]]", "[[Schur 分解]]", "[[矩阵扰动]]"]
created: 2026-08-15
updated: 2026-08-15
---

# Demmel：从幂法到移位 QR 迭代

> [!abstract] 来源定位
> Berkeley Math 221 第九至十讲把幂法、反幂法、正交迭代、移位 QR 和 Rayleigh 商迭代组织成一条递进路线。该来源承担收敛因子的经典推导、正交迭代与 QR 迭代等价性，以及对称 RQI 局部三次收敛的教学证明。

## 核心映射

| ID | 断言或工具 | 纳入位置 |
|---|---|---|
| EI-D1 | 若 $|\lambda_1|>|\lambda_2|$ 且初始向量含主方向，幂法方向误差按 $|\lambda_2/\lambda_1|^k$ 衰减 | [[幂法、反幂法与 Rayleigh 商迭代]]第五节 |
| EI-D2 | 反幂法等于对 $(A-\sigma I)^{-1}$ 做幂法，目标是离 $\sigma$ 最近的特征值 | 第九、十节 |
| EI-D3 | 正交迭代把单向量幂法推广到不变子空间 | 第十九节 |
| EI-D4 | QR 迭代与从 $I$ 出发的正交迭代相联系，移位引入反幂机制 | [[Hessenberg 化与 QR 特征值算法]]第八至十节 |
| EI-D5 | 对称矩阵的 Rayleigh 商误差是角误差的二阶量，结合反幂步骤给出局部三次收敛 | [[幂法、反幂法与 Rayleigh 商迭代]]第十三节 |
| EI-D6 | 非正规谱问题的可靠性必须结合左右特征向量、残差和伪谱解释 | 两章的边界章节 |

## 配套讲义

- [Lecture 9：幂法、反幂法、正交迭代与移位 QR](https://people.eecs.berkeley.edu/~demmel/ma221_Fall23/Lectures/Lecture_09.pdf)
- [Lecture 10：对称特征问题、Rayleigh 商迭代与三次收敛](https://people.eecs.berkeley.edu/~demmel/ma221_Fall23/Lectures/Lecture_10.pdf)

## 证据边界

- 简洁收敛率首先在对角或可对角化矩阵上成立；非正规矩阵还会出现特征向量基条件数和暂态放大；
- 随机初始化“几乎不会正交”是概率陈述，不是有限样本中的绝对保证；
- RQI 的三次收敛依赖实对称/复 Hermitian、接近单特征对和足够准确的线性求解；
- 迭代中 $(A-\mu I)$ 越接近奇异并不自动造成方向失败，但线性求解误差必须受控。

## 生成节点

- [x] [[幂法、反幂法与 Rayleigh 商迭代]]
- [x] [[Hessenberg 化与 QR 特征值算法]]
- [x] [[实验 - 谱间隙、移位与 Rayleigh 商迭代收敛]]

