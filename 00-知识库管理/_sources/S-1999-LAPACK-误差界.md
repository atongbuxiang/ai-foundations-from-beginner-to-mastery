---
type: source
status: draft
area: [sources, math/numerical-analysis, numerical-linear-algebra, software]
source_type: official-software-guide
title: "LAPACK Users' Guide, Third Edition: Accuracy and Stability"
author: [E. Anderson, Z. Bai, C. Bischof, S. Blackford, J. Demmel, J. Dongarra, J. Du Croz, A. Greenbaum, S. Hammarling, A. McKenney, D. Sorensen]
year: 1999
url: "https://www.netlib.org/lapack/lug/node72.html"
accessed: 2026-08-15
source_tier: A
license: "Netlib 官方在线手册；知识库仅保存独立摘要、公式映射与链接"
scope_role: canonical-implementation-bridge
temporal_role: foundational-software-contract
aliases: [LAPACK-LUG-Accuracy-Stability]
related: ["[[前向误差与后向误差]]", "[[数值稳定性]]", "[[稳定求解线性方程组]]"]
created: 2026-08-15
updated: 2026-08-15
---

# LAPACK：误差界、条件估计与计算解验收

> [!abstract] 来源定位
> LAPACK Users' Guide 把误差分析落实为可计算接口：残差、范数型和分量型后向误差、条件估计、前向误差界与迭代改进。它承担本章的工程验收规范，而不是只作为历史引用。

## 核心映射

| ID | 断言 | 纳入位置 |
|---|---|---|
| L1 | 计算残差后必须按 $A,\widehat x,b$ 的尺度归一化 | [[前向误差与后向误差]]第七、十四节；[[稳定求解线性方程组]]第十二节 |
| L2 | 联合范数型后向误差可写成残差除以 $\|A\|\|\widehat x\|+\|b\|$ | 第七节 |
| L3 | 分量型后向误差为 $\max_i |r_i|/(|A||\widehat x|+|b|)_i$ | [[前向误差与后向误差]]第九节；[[稳定求解线性方程组]]第十二节 |
| L4 | 分量型分析保留稀疏零结构和小分量信息 | 第九节 |
| L5 | 专家驱动同时估计条件数、前向误差和后向误差，并执行迭代改进 | [[稳定求解线性方程组]]第十二至十五节 |
| L6 | 条件数可用估计替代精确计算，避免显式形成逆矩阵 | [[稳定求解线性方程组]]第十三节 |

## 证据边界

- 在线手册承担 LAPACK 的误差量定义与接口意图；
- 本章只描述概念和经典公式，不保证任意当前语言封装暴露相同字段；
- 具体例程、参数名和版本行为应在使用相应库时重新核对；
- “残差小”只有经过匹配的尺度与条件数解释后才成为准确性证据。

## 生成节点

- [x] [[前向误差与后向误差]]
- [x] [[实验 - 小残差、大前向误差与条件数]]
- [x] [[稳定求解线性方程组]]
- [x] [[实验 - 选主元、后向误差与迭代改进]]
