---
type: source
status: draft
area: [sources, math/numerical-linear-algebra, math/svd]
source_type: original-paper
title: "Calculating the Singular Values and Pseudo-Inverse of a Matrix"
author: "Gene H. Golub and William Kahan"
year: 1965
url: "https://doi.org/10.1137/0702016"
accessed: 2026-08-15
source_tier: A
license: "SIAM 原始论文；知识库仅保存独立摘要、推导与链接"
scope_role: original-algorithm
temporal_role: foundational
aliases: [Golub-Kahan-1965-SVD]
related: ["[[SVD 算法与谱范数估计]]", "[[奇异值分解]]", "[[Moore-Penrose 伪逆]]"]
created: 2026-08-15
updated: 2026-08-15
---

# Golub–Kahan：先双对角化、再求奇异值

> [!abstract] 来源定位
> 1965 年原始工作建立了现代稠密 SVD 的核心两阶段结构：用左右酉/正交变换把一般矩阵化为双对角矩阵，再迭代对角化小带宽问题。它承担算法谱系与双对角化路线；当前软件选项由 LAPACK 文档核验。

## 核心映射

| ID | 原始贡献 | 纳入位置 |
|---|---|---|
| GK-1 | 构造 $B=U^*AV$ 的双对角约化，并保持奇异值 | [[SVD 算法与谱范数估计]]第五至八节 |
| GK-2 | 随后的迭代只需处理双对角矩阵 | 第九至十一节 |
| GK-3 | 左右奇异向量通过累计约化与迭代变换恢复 | 第十二节 |
| GK-4 | SVD 直接连接伪逆和稳定最小二乘 | AI/求解接口 |

## 证据边界

- 原论文说明算法思想，不承担 LAPACK 3.12.1 的工作区、覆盖输入和失败状态；
- 形成 $A^TA$ 的特征分解适合理论联系，不是计算微小奇异值的默认稳定算法；
- 稠密完整 SVD 与大规模截断 SVD 是不同任务，不能只按同一复杂度比较；
- 极小奇异值的相对精度还依赖输入结构、缩放与采用的 SVD 变体。

## 生成节点

- [x] [[SVD 算法与谱范数估计]]

