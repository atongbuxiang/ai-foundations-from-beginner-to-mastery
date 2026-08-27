---
type: source
status: draft
area: [sources, math/numerical-analysis, math/numerical-linear-algebra, ai-systems]
source_type: review-article
title: "Mixed Precision Algorithms in Numerical Linear Algebra"
author: Nicholas J. Higham, Theo Mary
year: 2022
url: "https://eprints.maths.manchester.ac.uk/2841/"
accessed: 2026-08-15
source_tier: A
license: "机构仓储公开综述；知识库仅保存独立摘要、推导映射与链接"
scope_role: canonical-mixed-precision-survey
temporal_role: modern-survey
aliases: [Higham-Mary-2022, Mixed-Precision-NLA]
related: ["[[迭代改进、混合精度与残差校正]]", "[[稳定求和、点积与矩阵乘法]]", "[[数值稳定性]]"]
created: 2026-08-15
updated: 2026-08-15
---

# Higham–Mary：混合精度数值线性代数

> [!abstract] 来源定位
> 该综述把低精度存储、运算、累加与输出作为不同契约，连接矩阵乘、矩阵分解、迭代改进和现代硬件。它是本库从经典误差分析迁移到 GPU/AI 数值契约的综合来源。

## 核心映射

| ID | 断言或工具 | 纳入位置 |
|---|---|---|
| MP-H1 | storage / product / accumulation / residual / output precision 必须分报 | 两个混合精度章节 |
| MP-H2 | 低精度可提供吞吐与带宽优势，高精度用于少数关键校验 | 算法设计原则 |
| MP-H3 | 混合精度成功的关键是可证的误差路径，不是单纯“把 dtype 改小” | AI 迁移 |
| MP-H4 | 动态范围、次正规数、溢出和舍入模式与 $u$ 同样重要 | 失效边界 |

## 使用边界

- 同名格式在不同硬件上可有不同乘法/累加语义，必须以实际内核契约为准；
- 理论精度保证不自动转化为端到端模型质量，仍需任务级验收；
- 加速比必须包含转换、通信、重启和回退成本。

## 生成节点

- [x] [[稳定求和、点积与矩阵乘法]]
- [x] [[迭代改进、混合精度与残差校正]]
