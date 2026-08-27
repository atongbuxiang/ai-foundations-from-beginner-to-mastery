---
type: source
status: draft
area: [sources, math/numerical-analysis, numerical-linear-algebra]
source_type: research-paper
title: "Numerical Stability of Algorithms at Extreme Scale and Low Precisions"
author: Nicholas J. Higham
year: 2021
url: "https://eprints.maths.manchester.ac.uk/2833/"
accessed: 2026-08-15
source_tier: A
license: "作者机构公开预印本；知识库仅保存独立摘要、推导映射与链接"
scope_role: canonical
temporal_role: foundational-current-bridge
aliases: [Higham-2021-Extreme-Low-Precision]
related: ["[[浮点数与舍入误差]]", "[[前向误差与后向误差]]", "[[数值稳定性]]"]
created: 2026-08-15
updated: 2026-08-15
---

# Higham：极端规模与低精度下的数值稳定性

> [!abstract] 来源定位
> 该论文把经典最坏舍入界带到超大规模与半精度环境：统一给出 $u$、$\gamma_n$、标准浮点模型、点积界，并说明 blocking、FMA、扩展精度与概率误差分析为何可让实际误差远小于朴素 $nu$ 预期。

## 核心映射

| ID | 断言 | 纳入位置 |
|---|---|---|
| H1 | $u=2^{-p}$（binary round-to-nearest） | [[浮点数与舍入误差]]第七节 |
| H2 | $\gamma_n=nu/(1-nu)$ | 第十二节 |
| H3 | $\operatorname{fl}(x\circ y)=(x\circ y)(1+\delta)$ | 第八节 |
| H4 | $|\widehat{x^Ty}-x^Ty|\le\gamma_n|x|^T|y|$ | 第十四节 |
| H5 | FP16/BF16 的精度与正规范围对照 | 第三/十六节 |
| H6 | blocking 可降低有效误差深度 | 第十三/十四节 |
| H7 | 最坏界失去保证不等于实际计算必败 | 第十二节 |

## 教学价值

论文表 2 同时列出 significand bits、exponent bits、$u$、最小正规数与最大数，非常适合纠正“位宽只对应一个精度”这一初学者误区。

## 视觉与文本核验

- 已抽取全文并定位标准模型、$\gamma_n$、格式表、blocked inner product 与 summation；
- 已渲染并目视检查 PDF 第 1–10 页，表 2、公式 (1.4)、点积界与 Figure 1 清晰；
- 本章只采用经典确定性部分；概率误差分析留给后续专题。

## 生成节点

- [x] [[浮点数与舍入误差]]
- [x] [[实验 - 浮点求和次序与灾难性消去]]

