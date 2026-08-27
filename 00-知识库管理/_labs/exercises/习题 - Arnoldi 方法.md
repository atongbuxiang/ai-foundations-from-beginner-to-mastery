---
type: exercise
status: draft
area: [math/numerical-linear-algebra, math/krylov-methods]
topic: "[[Arnoldi 方法]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[Lanczos 方法]]", "[[标准正交基与 Gram-Schmidt]]", "[[Schur 分解]]"]
related: ["[[解答 - Arnoldi 方法]]", "[[实验 - Arnoldi 非正规性、重正交与重启]]", "[[非正规矩阵]]"]
solution: "[[解答 - Arnoldi 方法]]"
created: 2026-08-15
updated: 2026-08-15
---

# 习题 - Arnoldi 方法

> [!abstract] 训练目标
> 从长递推和 Hessenberg 投影出发，掌握一般矩阵 Ritz 残差、有限精度正交化、非正规敏感性与重启设计，并能迁移到 JVP、GMRES 和矩阵函数。

## A. 识别与复述

### NLA-ARN-A01

比较 Arnoldi 与 Lanczos 的算子假设、投影结构、递推长度、正交化成本和可用误差理论。

### NLA-ARN-A02

写出 Arnoldi 分解的两种形式，标明 $Q_k,H_k,\bar H_k$ 的形状，并解释 $H_k$ 为何上 Hessenberg。

### NLA-ARN-A03

区分普通 Ritz、Schur 向量、harmonic Ritz、shift-and-invert 与 refined Ritz vector；分别指出它们试图解决的困难。

## B. 手算与构造

### NLA-ARN-B01

对正文矩阵

$$
A=\begin{bmatrix}1&1&0\\0&2&1\\0&0&3\end{bmatrix},\quad
q_1=(1,0,1)^T/\sqrt2,
$$

手算两步 Arnoldi，给出 $q_2,q_3$ 与 $\bar H_2$。

### NLA-ARN-B02

求 `B01` 中 $H_2$ 的 Ritz 值并与 $A$ 的特征值比较。解释为何越过 $[1,3]$ 不违反定理。

### NLA-ARN-B03

若 $h_{k+1,k}=0.02$、单位小特征向量末分量为 $0.15+0.20i$，计算 Ritz 残差范数。

### NLA-ARN-B04

稠密隐式算子维数 $n=2\times10^5$，子空间上限 $m=80$。估算双精度存储 $Q_m$ 的内存；估算一次 MGS 正交化到第 80 步所需的内积/axpy 向量遍历次数，并说明通信瓶颈。

### NLA-ARN-B05

对特征值 $1+4i,,2,,3-i$，分别按最大模与最大实部排序。说明稳定性分析若关心连续时间 $\dot x=Ax$ 应选哪个目标。

### NLA-ARN-B06

给定 $2\times2$ Jordan 块 $J=\begin{bmatrix}1&M\\0&1\end{bmatrix}$，计算 $J^k$。取 $M=100$，说明谱半径为 $1$ 为何不能界定有限时放大。

## C. 推导与证明

### NLA-ARN-C01

从逐列 MGS 推导 $AQ_k=Q_{k+1}\bar H_k$，并证明 $h_{ij}=0$ 当 $i>j+1$。

### NLA-ARN-C02

由 Arnoldi 分解和 $H_ky=\theta y$ 推导廉价 Ritz 残差公式，并证明 Galerkin 正交性。

### NLA-ARN-C03

证明若精确算术中 $h_{j+1,j}=0$，则 $\mathcal K_j(A,q_1)$ 是 $A$ 的不变子空间。

### NLA-ARN-C04

对 $A=V\Lambda V^{-1}$，证明

$$
p(A)=Vp(\Lambda)V^{-1},
$$

并说明 $\kappa(V)$ 为什么会破坏只按谱点设计的多项式收敛预测。

### NLA-ARN-C05

从 Arnoldi 关系推导 GMRES 小最小二乘

$$
\min_y\|\beta e_1-\bar H_ky\|_2.
$$

### NLA-ARN-C06

设 $q_1=b/\|b\|$。说明并推导 Krylov 矩阵函数近似

$$
f(A)b\approx\|b\|Q_kf(H_k)e_1.
$$

哪些步骤是精确恒等式，哪一步是截断近似？

## D. 边界、反例与纠错

### NLA-ARN-D01

构造一个非对称矩阵，使投影 Hessenberg 的远上三角元不能由三项递推忽略；解释强行 Lanczos 化会破坏什么。

### NLA-ARN-D02

说明为什么“Ritz 残差 $10^{-10}$，所以特征值有 10 位准确”对非正规矩阵不成立。给出应补充的条件/诊断。

### NLA-ARN-D03

比较一次 classical Gram–Schmidt、一次 MGS 与二次 MGS；纠正“同一公式所以浮点结果等价”的说法。

### NLA-ARN-D04

纠正“重启就是每 $m$ 步随机换一个新起点”。说明至少三种应保留的信息。

### NLA-ARN-D05

纠正“谱半径小于一就保证循环网络不会出现梯度爆发”。给出非正规暂态和奇异值视角。

## E. AI 迁移

### NLA-ARN-E01

只有 JVP 接口时，设计估计 Jacobian 最大实部特征值的 Arnoldi 实验；写出排序、残差、重启与非正规敏感性指标。

### NLA-ARN-E02

若同时有 JVP 与 VJP，说明如何估计简单特征值的左右条件数，以及为何这比只看右 Ritz 残差更可靠。

### NLA-ARN-E03

为 $\exp(tJ)v$ 设计 Krylov 近似与自适应策略。应改变子空间维数、时间步长还是两者？用什么误差代理？

### NLA-ARN-E04

比较非对称训练动力学中“最大模特征值”“最大实部特征值”“最大奇异值”回答的问题。为离散迭代和连续流分别选主指标。

### NLA-ARN-E05

一个数据驱动 Koopman 算子产生很多不稳定 Ritz 点。设计排查：数据划分、残差、重启稳定性、bootstrap、Schur 子空间与伪谱各自做什么？

## 分级提示

- `B01`：$q_2=(-1,1,1)^T/\sqrt3$，$q_3=(1,2,-1)^T/\sqrt6$；
- `B03`：先算复数模 $\sqrt{0.15^2+0.20^2}$；
- `C03`：分解尾项消失后 $AQ_j=Q_jH_j$；
- `C05`：$r_0=\beta q_1$；
- `D02`：寻找 $\kappa(V)$ 或左右向量夹角；
- `E04`：离散长期稳定与谱半径相关，瞬时最坏放大与谱范数相关。

## 解答入口

完成独立尝试后再打开：[[解答 - Arnoldi 方法]]。
