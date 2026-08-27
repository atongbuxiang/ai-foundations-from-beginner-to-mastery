---
type: source
status: draft
area: [sources, math/numerical-analysis, numerical-linear-algebra]
source_type: course-notes
title: "Notes for Math 221, Lecture 7: Least Squares, Householder and Givens QR"
author: James Demmel
year: 2024
url: "https://people.eecs.berkeley.edu/~demmel/ma221_Fall24/Lectures/Lecture_07.pdf"
accessed: 2026-08-15
source_tier: A
license: "作者公开课程讲义；知识库仅保存独立摘要、推导映射与链接"
scope_role: canonical-worked-analysis
temporal_role: foundational-teaching
aliases: [Demmel-2024-Householder-Givens-QR]
related: ["[[Householder 与 Givens 变换]]", "[[QR 分解]]", "[[数值稳定性]]", "[[稳定最小二乘与正规方程的风险]]"]
created: 2026-08-15
updated: 2026-08-15
---

# Demmel：Householder、Givens 与正交变换稳定性

> [!abstract] 来源定位
> Berkeley Math 221 讲义给出 Householder 反射构造稠密 QR、Givens 平面旋转逐元素消元，以及“正交变换序列为何后向稳定”的证明主线。本来源承担本章的经典理论与算法边界；具体软件存储契约由 LAPACK 来源承担。

## 核心映射

| ID | 断言或工具 | 纳入位置 |
|---|---|---|
| DQ1 | $H=I-2uu^T$ 是正交、对称的超平面反射 | [[Householder 与 Givens 变换]]第三节 |
| DQ2 | 选择 $u\propto x\pm\|x\|e_1$ 可把向量尾部一次消成零 | 第四、五节 |
| DQ3 | QR 不显式形成每个 $H_k$，而以向量和标量紧凑存储 | 第六、七节 |
| DQ4 | Givens 旋转只混合两个坐标，适合稀疏、增量和结构化消元 | 第十至十二节 |
| DQ5 | 连续施加近似正交变换可解释为对邻近矩阵执行精确正交变换 | 第十五节 |
| DQ6 | Householder/Givens QR 的正交性缺陷保持在舍入误差量级，而朴素 Gram–Schmidt 可能受条件数放大 | 第十五、十六节 |
| DQ7 | block Householder 用矩阵乘降低数据移动，算法评价不能只数 flops | 第十八节 |

## 证据边界

- “后向稳定”绑定标准浮点模型、无溢出/下溢灾难和适用规模条件；
- $O(u)$ 隐藏维度与实现常数，正文使用 $c(m,n)u$ 而不伪造统一常数；
- 正交变换不放大二范数误差，不等于输入列空间在近秩亏处条件良好；
- 稀疏 fill-in、通信规避和 GPU kernel 行为需要对具体实现另行验证。

## 生成节点

- [x] [[Householder 与 Givens 变换]]
- [x] [[实验 - Householder 符号、Givens 缩放与 QR 正交性]]
