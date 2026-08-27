---
type: source
status: draft
area: [sources, math/numerical-analysis, numerical-linear-algebra, software]
source_type: official-software-documentation
title: "LAPACK 3.12.1: DGEQRF, DLARFG and DLARTG"
author: [LAPACK project, Edward Anderson]
year: 2025
url: "https://www.netlib.org/lapack/explore-html/d0/da1/group__geqrf.html"
accessed: 2026-08-15
source_tier: A
license: "Netlib 官方在线文档；知识库仅保存独立摘要、接口映射与链接"
scope_role: canonical-implementation-contract
temporal_role: current-software-contract
aliases: [LAPACK-QR-Householder-Givens]
related: ["[[Householder 与 Givens 变换]]", "[[QR 分解]]", "[[稳定最小二乘与正规方程的风险]]"]
created: 2026-08-15
updated: 2026-08-15
---

# LAPACK：QR 反射器、紧凑存储与安全平面旋转

> [!abstract] 来源定位
> LAPACK 把理论正交变换落实为软件契约：`xGEQRF` 以 elementary reflectors 计算 QR，矩阵上三角保存 $R$、下三角与 `TAU` 保存 $Q$；`xLARTG` 通过安全缩放生成平面旋转，避免直接平方和造成溢出或下溢。

## 核心映射

| ID | 官方契约 | 纳入位置 |
|---|---|---|
| LQ1 | `DGEQRF` 计算 $A=Q[R;0]$，$Q$ 是正交矩阵 | [[Householder 与 Givens 变换]]第六节 |
| LQ2 | $Q=H_1H_2\cdots H_k$，$H_i=I-\tau_i v_i v_i^T$ | 第七节 |
| LQ3 | `A` 的上三角存 $R$，对角线下方与 `TAU` 共同表示反射器 | 第七节 |
| LQ4 | block reflector 通过 `LARFT/LARFB` 组织为高强度矩阵运算 | 第十八节 |
| LQ5 | `DLARTG` 生成 $c,s,r$，满足 $c^2+s^2=1$ 并把第二分量消零 | 第十、十三节 |
| LQ6 | `DLARTG` 对极端尺度使用缩放，避免 $f^2+g^2$ 的 overflow/underflow | 第十三节与实验 |

## 接口边界

- 本节点记录 LAPACK 3.12.1 在线文档所示契约；语言封装可能使用不同名称和布局；
- `GEQRF` 默认不显式返回完整 $Q$，需要专用生成或应用例程；
- `LARTG` 的符号约定必须与调用代码一致，不能把另一种 $2\times2$ 旋转布局直接混用；
- 官方例程的安全缩放不能替代输入 NaN/Inf、秩亏和任务容差检查。

## 官方入口

- [`DGEQRF`](https://www.netlib.org/lapack/explore-html/d3/d69/dgeqrf_8f_source.html)
- [`DLARTG`](https://www.netlib.org/lapack/explore-html/da/dd3/group__lartg_ga86f8f877eaea0386cdc2c3c175d9ea88.html)

## 生成节点

- [x] [[Householder 与 Givens 变换]]
- [x] [[实验 - Householder 符号、Givens 缩放与 QR 正交性]]
