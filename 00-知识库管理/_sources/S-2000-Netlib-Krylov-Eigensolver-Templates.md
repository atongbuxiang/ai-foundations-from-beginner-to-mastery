---
type: source
status: draft
area: [sources, math/numerical-linear-algebra, software/eigensolvers]
source_type: technical-book
title: "Templates for the Solution of Algebraic Eigenvalue Problems"
author: "Bai, Demmel, Dongarra, Ruhe, van der Vorst et al."
year: 2000
url: "https://www.netlib.org/utk/people/JackDongarra/etemplates/index.html"
accessed: 2026-08-15
source_tier: A
license: "Netlib 在线技术书；知识库仅保存独立摘要、公式映射与链接"
scope_role: implementation-and-finite-precision-contract
temporal_role: foundational-software-methodology
aliases: [Netlib-Eigensolver-Templates]
related: ["[[Lanczos 方法]]", "[[Arnoldi 方法]]", "[[矩阵扰动]]"]
created: 2026-08-15
updated: 2026-08-15
---

# Netlib Templates：Ritz 验收、重正交化与重启

> [!abstract] 来源定位
> Netlib 的代数特征值模板系统整理 Arnoldi/Lanczos 的基本关系、残差、存储成本、重正交化、谱变换和重启。它主要承担有限精度和生产算法边界，而不是取代正文中的初学者推导。

## 核心映射

| ID | 来源事实 | 纳入位置 |
|---|---|---|
| NET-K1 | Arnoldi 是对 Krylov 空间的正交投影，$V_k^*AV_k=H_k$ | [[Arnoldi 方法]]基本算法 |
| NET-K2 | Ritz 残差可由最后一个 Hessenberg 系数和小特征向量末分量低成本获得 | 两章停止准则 |
| NET-K3 | Arnoldi 存储约为 $nk+k^2/2$，正交化成本随 $k^2n$ 增长 | [[Arnoldi 方法]]成本章节 |
| NET-K4 | Lanczos 只对最近两向量正交；收敛方向会在舍入误差下重新进入基，产生重复 Ritz 值 | [[Lanczos 方法]]有限精度章节 |
| NET-K5 | full、selective 和 local reorthogonalization 是不同成本—可靠性方案 | 同上 |
| NET-K6 | shift-invert 把移位附近特征值映为变换后的极端特征值，但每步需线性求解 | 两章谱变换章节 |

## 入口

- [Arnoldi 基本算法](https://netlib.org/utk/people/JackDongarra/etemplates/node216.html)
- [Lanczos 重正交化](https://www.netlib.org/utk/people/JackDongarra/etemplates/node108.html)
- [Lanczos/两侧方法收敛与 shift-invert](https://netlib.org/utk/people/JackDongarra/etemplates/node246.html)

## 证据边界

- 这是经典算法模板，不固定当前某个 Python/GPU API；
- “通常先收敛极端值”是谱多项式过滤行为，不保证任意初向量、重根或非正规问题的相同轨迹；
- 重启能控制内存，但选择保留的子空间决定信息损失，不能描述成免费压缩；
- 任何库封装都必须单独报告 `which`、`ncv`/子空间大小、容差、最大迭代、收敛对数和残差。

## 生成节点

- [x] [[Lanczos 方法]]有限精度与重启章节
- [x] [[Arnoldi 方法]]成本、重启和 shift-invert 章节

