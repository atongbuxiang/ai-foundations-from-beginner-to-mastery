---
type: source
status: draft
area: [sources, math/numerical-analysis, numerical-linear-algebra]
source_type: course-notes
title: "Notes for Math 221, Lecture 3"
author: James Demmel
year: 2023
url: "https://people.eecs.berkeley.edu/~demmel/ma221_Fall23/Lectures/Lecture_03.pdf"
accessed: 2026-08-15
source_tier: A
license: "作者课程公开讲义；知识库仅保存独立摘要、推导映射与链接"
scope_role: canonical
temporal_role: foundational-current-teaching
aliases: [Demmel-2023-Math221-Error-Analysis]
related: ["[[前向误差与后向误差]]", "[[条件数]]", "[[矩阵范数]]"]
created: 2026-08-15
updated: 2026-08-15
---

# Demmel：Math 221 条件数、残差与后向误差讲义

> [!abstract] 来源定位
> Berkeley Math 221 的课程讲义把标量的一阶条件分析推广到矩阵问题，并从残差直接证明线性系统的最小二范数后向扰动。它承担本章“从微积分到线性代数”的教学桥梁和可计算验收视角。

## 核心映射

| ID | 断言 | 纳入位置 |
|---|---|---|
| D1 | 标量相对条件数为 $|f'(x)x/f(x)|$ | [[前向误差与后向误差]]第六节 |
| D2 | 后向稳定形式为 $\operatorname{alg}(x)=f(x+\delta x)$ | 第五、十三节 |
| D3 | 线性系统误差满足 $\boldsymbol x-\widehat{\boldsymbol x}=\boldsymbol A^{-1}\boldsymbol r$ | 第七节 |
| D4 | 最小 $\|\boldsymbol E\|_2$ 可由秩一矩阵达到 | 第七节 |
| D5 | 条件估计可比显式求逆便宜，验收不应要求形成 $A^{-1}$ | 第十四节 |

## 视觉与文本核验

- 已渲染并目视检查 PDF 第 1 页和第 10 页；
- 第 1 页确认后向扰动—Jacobian—条件数链；
- 第 10 页确认残差公式、最小矩阵扰动证明和条件估计的计算动机；
- 讲义中的 $O(\varepsilon)$ 是定性稳定性语言，本章的具体线性系统公式单独给出精确常数与范数。

## 生成节点

- [x] [[前向误差与后向误差]]
- [x] [[实验 - 小残差、大前向误差与条件数]]

