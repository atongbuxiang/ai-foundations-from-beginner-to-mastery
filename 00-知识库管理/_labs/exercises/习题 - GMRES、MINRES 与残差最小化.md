---
type: exercise
status: draft
area: [math/numerical-linear-algebra, math/krylov-methods]
topic: "[[GMRES、MINRES 与残差最小化]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[Arnoldi 方法]]", "[[Lanczos 方法]]", "[[Krylov 子空间与预条件]]"]
related: ["[[解答 - GMRES、MINRES 与残差最小化]]", "[[实验 - GMRES 重启、MINRES 结构与残差最小化]]"]
solution: "[[解答 - GMRES、MINRES 与残差最小化]]"
created: 2026-08-15
updated: 2026-08-15
---

# 习题 - GMRES、MINRES 与残差最小化

> [!abstract] 训练目标
> 从结构选择、Arnoldi/Lanczos 投影和重启成本三个层次掌握最小残差方法，并能迁移到非正规 Jacobian、KKT 与可变预条件。

## A. 识别与复述

### NLA-MR-A01

比较 CG、MINRES、GMRES 的矩阵假设、最优量、递推长度和内存。

### NLA-MR-A02

解释 GMRES 的搜索空间、测试空间和 Petrov–Galerkin 条件。它与 FOM 有何不同？

### NLA-MR-A03

区分 happy breakdown、数值 breakdown、停滞和达到容差四种退出状态。

### NLA-MR-A04

设计 GMRES$(m)$ 日志表，至少包含八列，使不同 $m$ 能按同一精度和资源公平比较。

### NLA-MR-A05

解释右预条件 GMRES 为何直接最小化原方程残差，并写出从预条件变量恢复 $x$ 的公式。

## B. 手算与构造

### NLA-MR-B01

对正文

$$
A=\begin{bmatrix}2&1\\0&1\end{bmatrix},\quad b=(1,1)^T,\quad x_0=0
$$

手算两步 Arnoldi 与 GMRES，给出 $Q_2,H_2,x_1,x_2$ 和真残差。

### NLA-MR-B02

若

$$
\bar H_2=
\begin{bmatrix}
2&1\\1&2\\0&1
\end{bmatrix},
\qquad \beta=1,
$$

写出 GMRES 小最小二乘的正规方程，仅用于手算求 $y$；再说明实现为何不推荐这样做。

### NLA-MR-B03

对 $A=\operatorname{diag}(1,-1)$、$b=(1,1)^T$，计算 CG 首步分母；再在 $\mathcal K_1,\mathcal K_2$ 中计算最小残差。

### NLA-MR-B04

完整 GMRES 运行到 $k=100$，维数 $n=10^7$，每向量 float32。只计 Arnoldi 基，估算内存；估算累计正交内积数。

### NLA-MR-B05

左预条件中 $r=(1,1)^T$、$M=\operatorname{diag}(10^6,10^{-3})$。比较 $\|r\|_2$ 与 $\|M^{-1}r\|_2$，解释停止差异。

## C. 推导与证明

### NLA-MR-C01

由 Arnoldi 分解推导

$$
\min_y\|\beta e_1-\bar H_ky\|_2
$$

并证明 $r_k\perp A\mathcal K_k$。

### NLA-MR-C02

证明完整 GMRES 的精确算术残差二范数单调不增。为什么这不推出严格下降？

### NLA-MR-C03

推导 GMRES 的残差多项式表达，并证明相对最小多项式次数给出有限终止上界。

### NLA-MR-C04

若 $A=V\Lambda V^{-1}$，推导对角化特征值界并指出 $\kappa(V)$ 的意义。

### NLA-MR-C05

说明对称 $A$ 时 Arnoldi Hessenberg 为什么退化为三对角；由此写出 MINRES 小最小二乘。

## D. 边界、反例与纠错

### NLA-MR-D01

纠正“重启 GMRES$(m)$ 等于完整 GMRES 只是不存旧向量”。指出丢失的信息。

### NLA-MR-D02

反驳“同样特征值意味着 GMRES 收敛曲线相同”。给出正规/非正规对照思路。

### NLA-MR-D03

为什么一般 ILU 不能直接作为 MINRES 预条件器？需要什么结构？

### NLA-MR-D04

递推残差已为 $10^{-12}$，真残差仍为 $10^{-6}$。列出至少四个排查步骤。

### NLA-MR-D05

奇异对称系统中，“最小残差解”“最小长度解”“预条件坐标下最小长度解”有何不同？

## E. AI 迁移

### NLA-MR-E01

为 $(I-J_f^T)v=g$ 的隐式反向设计 GMRES/FGMRES 实验，写出算子接口、预条件、重启和停止。

### NLA-MR-E02

一个 KKT 系统对称不定。设计 MINRES 块预条件契约，并说明为何块预条件器仍需 SPD。

### NLA-MR-E03

每次预条件调用都运行不同步数的神经内层求解器。为什么应考虑 FGMRES？需要多存什么？

### NLA-MR-E04

非凸 Hessian 系统用 MINRES 得到很小线性残差。为什么外层优化仍可能失败？补充哪些量？

### NLA-MR-E05

在多 GPU 上比较 GMRES$(20)$、GMRES$(80)$ 与 pipelined/communication-avoiding 变体，设计公平报告。

## 分级提示

- B02：$\bar H_2^T\bar H_2=\begin{bmatrix}5&4\\4&6\end{bmatrix}$；
- B03：$b^TAb=0$；
- C01：最小二乘残差正交于 $\mathcal R(\bar H_k)$；
- C03：使用 $p(0)=1$；
- D02：考虑 Jordan 型上三角耦合；
- E03：保存预条件后的方向 $Z_k$。

## 解答入口

完成独立尝试后再打开：[[解答 - GMRES、MINRES 与残差最小化]]。
