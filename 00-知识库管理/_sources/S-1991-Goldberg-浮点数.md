---
type: source
status: draft
area: [sources, math/numerical-analysis, computer-systems]
source_type: tutorial-paper
title: "What Every Computer Scientist Should Know About Floating-Point Arithmetic"
author: David Goldberg
year: 1991
url: "https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html"
accessed: 2026-08-15
source_tier: A
license: "ACM 论文经授权重印于 Oracle 文档；知识库只保存独立摘要、公式映射与链接"
scope_role: canonical
temporal_role: foundational
aliases: [Goldberg-1991-Floating-Point]
related: ["[[浮点数与舍入误差]]", "[[数值线性代数 MOC]]"]
created: 2026-08-15
updated: 2026-08-15
---

# Goldberg：每个计算机科学家都应知道的浮点知识

> [!abstract] 来源定位
> 这是浮点数入门到系统语义的经典主来源。它从有限格式、ulp 与相对误差出发，区分 guard digit 与正确舍入，深入讨论 cancellation、IEEE 特殊值、次正规数、异常与编译器。正文关于“减法可精确但暴露旧误差”的表述、Sterbenz 型结论和稳定公式改写均由此核验。

## 元数据

- 原论文：`ACM Computing Surveys`, 23(1), 1991。
- 当前入口：[Oracle HTML 重印](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html)。
- PDF：[Oracle 授权重印 PDF](https://docs.oracle.com/cd/E19957-01/800-7895/800-7895.pdf)。

## 核心映射

| ID | 断言 | 纳入位置 |
|---|---|---|
| G1 | 有限位必须舍入多数实数 | [[浮点数与舍入误差]]第一节 |
| G2 | ulp 与相对误差是不同尺度 | 第七节 |
| G3 | guard digit 不等于完整正确舍入 | 第六/十节 |
| G4 | catastrophic cancellation 常暴露先前误差 | 第十节 |
| G5 | 相差因子不超过 2 的浮点数相减可精确 | Sterbenz 引理 |
| G6 | 二次方程与平方差可稳定改写 | 第十节 |
| G7 | signed zero、Inf、NaN、denormal | 第四节 |

## 独立核验重点

### 消去不是“减法器突然很差”

来源用先平方再相减的例子说明：最终减法可精确，但被减数已经带有乘法舍入。前导位消失后，旧误差成为结果的主要部分。本库据此强制区分良性与灾难性消去。

### 正确舍入

guard digit 只保证某类加减误差较小；正确舍入要求输出等于“精确结果按当前模式舍入”的结果。现代误差模型采用后者作为基本语义。

## 视觉与文本核验

- 已抽取全文并定位格式、ulp、guard digits、cancellation、exact rounding、特殊值与 denormalized numbers；
- 已渲染并目视检查 PDF 第 5–14 页，公式、图 1 与 cancellation 小节排版正常；
- 未复制长段原文，正文均为独立重写与再推导。

## 生成节点

- [x] [[浮点数与舍入误差]]
- [x] [[习题 - 浮点数与舍入误差]]
- [x] [[解答 - 浮点数与舍入误差]]
- [x] [[实验 - 浮点求和次序与灾难性消去]]

