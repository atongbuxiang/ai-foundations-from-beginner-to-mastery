---
type: source
status: draft
area: [sources, math/numerical-analysis, numerical-linear-algebra]
source_type: textbook
title: "Accuracy and Stability of Numerical Algorithms, Second Edition"
author: Nicholas J. Higham
year: 2002
url: "https://doi.org/10.1137/1.9780898718027"
accessed: 2026-08-15
source_tier: A
license: "SIAM 版权教材；知识库只保存独立摘要、推导映射与书目信息"
scope_role: canonical
temporal_role: foundational
aliases: [Higham-2002-Accuracy-Stability]
related: ["[[浮点数与舍入误差]]", "[[前向误差与后向误差]]", "[[数值稳定性]]", "[[稳定求解线性方程组]]"]
created: 2026-08-15
updated: 2026-08-15
---

# Higham：数值算法的准确性与稳定性

> [!abstract] 来源定位
> 这是浮点误差分析、前向/后向误差、稳定性定义与经典算法误差界的规范教材来源。本库用它校准“算法稳定不等于问题条件良好”“后向稳定不保证病态问题高精度”等边界，并用书中的标准分析框架组织求和、多项式、线性方程与迭代改进案例。

## 核心映射

| ID | 断言或工具 | 纳入位置 |
|---|---|---|
| H1 | 浮点基本运算模型与 $\gamma_n$ 累积语言 | [[浮点数与舍入误差]] |
| H2 | 前向、后向与混合误差分析必须绑定问题和扰动模型 | [[前向误差与后向误差]]、[[数值稳定性]] |
| H3 | 后向稳定把计算输出解释为邻近数据的精确解 | [[数值稳定性]]第五节 |
| H4 | 前向误差由问题条件性和算法后向误差共同决定 | [[数值稳定性]]第七节 |
| H5 | 溢出、下溢、缩放和例外值不应被标准相对误差模型掩盖 | [[数值稳定性]]第十二节 |
| H6 | 结构型、范数型和分量型稳定性是不同承诺 | [[数值稳定性]]第十五节 |
| H7 | LU 求解需把选主元、因子增长、后向误差、条件估计和迭代改进放入同一验收链 | [[稳定求解线性方程组]]第六至十六节 |
| H8 | Householder/Givens 需区分局部参数生成误差、正交变换应用误差与整个 QR 的后向误差 | [[Householder 与 Givens 变换]]第五、十三至十六节 |

## 教学使用边界

- 正文重新组织定义、例子和证明，不复制教材段落；
- “稳定”在不同教材中有弱稳定、混合稳定、前向稳定等局部约定，正文每次都显式写出不等式，避免只靠术语；
- 具体 LU、QR、特征值和 SVD 的定理常数留给后续算法节点，本节点只建立统一判断语言；
- 概率舍入分析、随机舍入和极端规模现象由[[S-2021-Higham-极端规模与低精度稳定性]]补充。

## 生成节点

- [x] [[数值稳定性]]
- [x] [[实验 - 等价公式不等价稳定]]
- [x] [[稳定求解线性方程组]]
- [x] [[实验 - 选主元、后向误差与迭代改进]]
- [x] [[Householder 与 Givens 变换]]
- [x] [[实验 - Householder 符号、Givens 缩放与 QR 正交性]]
