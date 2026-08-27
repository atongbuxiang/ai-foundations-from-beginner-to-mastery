---
type: source
status: draft
area: [sources, math/numerical-analysis, numerical-linear-algebra]
source_type: technical-report
title: "An Introduction to the Quality of Computed Solutions"
author: Sven Hammarling
year: 2005
url: "https://eprints.maths.manchester.ac.uk/101/"
accessed: 2026-08-15
source_tier: A
license: "作者机构公开技术报告；知识库仅保存独立摘要、推导映射与链接"
scope_role: canonical
temporal_role: foundational
aliases: [Hammarling-2005-Quality-Computed-Solutions]
related: ["[[前向误差与后向误差]]", "[[条件数]]", "[[数值稳定性]]"]
created: 2026-08-15
updated: 2026-08-15
---

# Hammarling：计算解的质量导论

> [!abstract] 来源定位
> 这份报告以线性方程和二次方程为主例，系统区分前向误差、残差、后向误差与条件数，并给出“前向误差约由条件数乘后向误差控制”的经典教学链。它承担本章的概念主轴与线性系统最小矩阵扰动证明。

## 核心映射

| ID | 断言 | 纳入位置 |
|---|---|---|
| H1 | 前向分析问计算解离精确解多远 | [[前向误差与后向误差]]第三节 |
| H2 | 后向分析问计算解精确满足哪个邻近问题 | 第五节 |
| H3 | 线性系统残差为 $\boldsymbol r=\boldsymbol b-\boldsymbol A\widehat{\boldsymbol x}$ | 第七节 |
| H4 | 二范数下最小矩阵扰动满足 $\|\boldsymbol E\|_2=\|\boldsymbol r\|_2/\|\widehat{\boldsymbol x}\|_2$ | 第七节 |
| H5 | 条件数把后向误差放大为前向误差 | 第六、八节 |
| H6 | 小残差可能对应大前向误差，反之亦可 | 第四、七节与实验 |

## 关键例子

报告用一个接近奇异的 $2\times2$ 线性系统展示：某个明显偏离真解的向量可以有很小残差，而另一个很接近真解的向量可以有较大残差。这个例子迫使读者把“满足方程的程度”和“离真解的距离”分开。

它还从

$$
\boldsymbol E\widehat{\boldsymbol x}=\boldsymbol r
$$

构造

$$
\boldsymbol E
=\frac{\boldsymbol r\widehat{\boldsymbol x}^{*}}
{\widehat{\boldsymbol x}^{*}\widehat{\boldsymbol x}},
$$

并证明该构造在二范数下达到所有可行扰动的下界。这使“残差经过尺度化成为后向误差”不只是口号，而是一个可证明的最优化结论。

## 视觉与文本核验

- 已抽取全文并定位 Section 4.3 Error Analysis；
- 已渲染并目视检查 PDF 第 21–24 页；
- 线性系统例子、残差定义、最小扰动构造、条件数乘积关系和二次方程例子均清晰可读；
- 本库采用报告的数学结论，但重新组织符号、例子和中文推导，不复制原文叙述。

## 生成节点

- [x] [[前向误差与后向误差]]
- [x] [[实验 - 小残差、大前向误差与条件数]]

