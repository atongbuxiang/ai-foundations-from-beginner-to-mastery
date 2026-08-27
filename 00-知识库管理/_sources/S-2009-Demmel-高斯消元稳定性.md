---
type: source
status: draft
area: [sources, math/numerical-analysis, numerical-linear-algebra]
source_type: course-notes
title: "Notes for Math 221, Lecture 4: Gaussian Elimination"
author: James Demmel
year: 2009
url: "https://people.eecs.berkeley.edu/~demmel/ma221_Fall09/Lectures/Lecture_04.html"
accessed: 2026-08-15
source_tier: A
license: "作者公开课程讲义；知识库仅保存独立摘要、推导映射与链接"
scope_role: canonical-worked-analysis
temporal_role: foundational-teaching
aliases: [Demmel-2009-Gaussian-Elimination-Stability]
related: ["[[线性方程组、消元与 LU 分解]]", "[[稳定求解线性方程组]]", "[[数值稳定性]]", "[[条件数]]"]
created: 2026-08-15
updated: 2026-08-15
---

# Demmel：Gaussian 消元、选主元与稳定性

> [!abstract] 来源定位
> Berkeley Math 221 讲义把 Gaussian 消元从代数分解推进到可计算的稳定性分析：无主元消元如何被小 pivot 破坏、部分选主元为何限制乘子、因子误差如何组合到线性求解后向误差，以及 pivot growth 怎样进入最终前向误差预算。本节点承担 LU 稳定性主证明的课程来源。

## 核心映射

| ID | 断言或工具 | 纳入位置 |
|---|---|---|
| D1 | 小 pivot 会产生巨大 multiplier 和中间量，即使原矩阵条件良好 | [[稳定求解线性方程组]]第三节 |
| D2 | 部分选主元在当前列选择最大绝对值，使 $|\ell_{ik}|\le1$ | 第四、九节 |
| D3 | 计算因子满足类似 $|\Delta A|\lesssim n u\,|L||U|$ 的分量界 | 第六节 |
| D4 | 前代、回代误差与因子误差可合并成整个求解的后向误差 | 第五至七节 |
| D5 | pivot growth 把内部元素增长连接到后向误差，最终前向界还要乘 $\kappa(A)$ | 第八、九节 |
| D6 | GEPP 最坏增长可达指数级，但实际通常远小；不能把经验可靠写成无条件定理 | 第九、十节 |
| D7 | 更高精度残差与迭代改进可以在适用条件下恢复前向精度 | 第十四、十五节 |

## 术语边界

- 讲义使用的 growth factor 可写成 $\|\,|L||U|\,\|/\|A\|$；其他教材常用消元全过程最大元素比值 $\rho$。正文同时定义并明确二者相关但不完全相同；
- $O(nu)$ 表示一阶误差结构，正文在需要处使用 $\gamma_n=nu/(1-nu)$ 暴露适用条件；
- GEPP 的最坏界很大不等于典型输入必然失败，也不等于可以忽略构造性反例；
- 课程讲义承担理论路线，具体软件字段和专家驱动流程由[[S-1999-LAPACK-误差界]]承担。

## 生成节点

- [x] [[稳定求解线性方程组]]
- [x] [[实验 - 选主元、后向误差与迭代改进]]
