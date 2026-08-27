---
type: exercise-set
status: draft
area: [math/calculus, math/matrix-calculus, math/probability]
aliases: [行列式导数习题, logdet 习题]
prerequisites: ["[[行列式、log-det 与迹的导数]]"]
related: ["[[解答 - 行列式、log-det 与迹的导数]]", "[[练习与测验 MOC]]"]
sources: ["Su-2383-Determinant-Derivative", "Magnus-Neudecker-Matrix-Differential-Calculus", "Higham-Functions-of-Matrices"]
created: 2026-08-18
updated: 2026-08-18
---

# 习题 - 行列式、log-det 与迹的导数

> [!abstract] 训练目标
> 从余子式/Jacobi 公式逐步走到稳定计算、Gaussian、flow 与随机迹估计。每次使用 $A^{-1}$ 前必须先声明可逆性；每次使用 log-det 必须说明定义域与数值实现。

## A. 概念与一阶直觉（3 题）

### A1. 单位阵处的一阶体积

不用 Jacobi 公式，直接从行列式的置换展开证明

$$
\det(I+tB)=1+t\operatorname{tr}(B)+O(t^2).
$$

解释为什么非对角元素不会贡献一阶项。

### A2. adjugate 与梯度

从 $\partial\det A/\partial a_{ij}=C_{ij}$ 出发，证明

$$
D\det(A)[E]=\operatorname{tr}(\operatorname{adj}(A)E)
$$

并写出 Frobenius 梯度。特别说明 adjugate 与余子式矩阵相差哪个转置。

### A3. 三个定义域

比较 $\det A$、$\log|\det A|$、实值 $\log\det A$ 的定义域与奇异边界。分别回答：奇异处是否有导数？负行列式处是否有实值？

## B. 核心推导（3 题）

### B1. 可逆 Jacobi 公式

由

$$
\det(A+tE)=\det(A)\det(I+tA^{-1}E)
$$

推导 $D\det(A)[E]$、$\nabla_A\det A$、$D\log|\det A|[E]$ 与其梯度。

### B2. 奇异矩阵

对以下矩阵计算 $\operatorname{adj}(A)$ 与 $D\det(A)[E]$：

$$
A_1=\begin{bmatrix}1&0\\0&0\end{bmatrix},
\qquad
A_2=\begin{bmatrix}0&0\\0&0\end{bmatrix}.
$$

说明秩 $n-1$ 与秩不超过 $n-2$ 的一阶差异。

### B3. 迹幂函数

不假设 $A$ 与 $dA$ 可交换，推导

$$
d\operatorname{tr}(A^4)=4\operatorname{tr}(A^3dA).
$$

再写出梯度，并解释为什么不能据此声称 $d(A^4)=4A^3dA$。

## C. 统计与结构化模型（3 题）

### C1. Gaussian 协方差

对

$$
\ell(\mu,\Sigma)
=\frac12\log\det\Sigma
+\frac12(x-\mu)^\top\Sigma^{-1}(x-\mu),
\quad\Sigma\succ0,
$$

推导 $\nabla_\mu\ell$ 与 $\nabla_\Sigma\ell$。解释两个协方差项的统计作用。

### C2. Cholesky 参数化

令 $\Sigma=LL^\top$，$L$ 为正对角下三角。

1. 推导 $\log\det\Sigma$；
2. 给出环境空间中的 $\nabla_L$；
3. 若 $L_{ii}=e^{s_i}$，求对 $s_i$ 的导数；
4. 说明严格下三角自由元对纯 log-det 的梯度为何为零。

### C3. 低秩更新

使用矩阵行列式引理把

$$
\log\det(D+UU^\top),
\qquad D=\operatorname{Diag}(e^s)
$$

化为一个 $r\times r$ log-det。写出复杂度主项与正定性理由。

## D. 数值与 AI 实现（3 题）

### D1. 稳定 log-det

分别为 SPD 矩阵与一般实可逆矩阵设计 log-det/logabsdet 计算流程。说明输出哪些量、使用何种分解、怎样处理符号，以及为什么 `log(det(A))` 不合格。

### D2. 三角 flow 层

设可逆变换的 Jacobian 为下三角矩阵 $J(x)$，对角元为 $e^{s_i(x_{<i})}$。求 $\log|\det J(x)|$。若将某个对角参数化改为普通实数 $a_i$，会出现哪些可逆性与导数问题？

### D3. Hutchinson 估计

证明若 $\mathbb E[\xi\xi^\top]=I$，则 $\mathbb E[\xi^\top M\xi]=\operatorname{tr}M$。据此为

$$
\operatorname{tr}(A^{-1}A')
$$

写一个只用 matvec 与线性求解的估计器，并列出至少四项误差/复现实验信息。

## E. 证明与研究边界（3 题）

### E1. 秩与最早非零阶

证明若 $\operatorname{rank}(A)\le n-2$，则 $D\det(A)=0$。进一步讨论：若 $\operatorname{nullity}(A)=k$，沿一般方向扰动时 det 最早可能在哪一阶非零？只需给出基于奇异值/适当基变换的论证框架。

### E2. log-det barrier

对 SPD 变量 $X$ 考虑 $f(X)=-\log\det X$。

1. 推导梯度；
2. 推导 Hessian 作用 $H_X[E]$；
3. 证明二阶方向曲率非负；
4. 解释它为何在正定锥边界形成屏障。

### E3. 公式审计

逐条判断并修正：

1. “$\nabla_A\log\det A=A^{-1}$”；
2. “det 在奇异矩阵处不可微”；
3. “对任意光滑标量函数 $f$ 都有 $d f(A)=f'(A)dA$”；
4. “flow 的 Jacobian 在每点 det 非零就足以保证全局可逆”；
5. “jitter 不改变概率模型，只帮助 Cholesky”。

## 提交规范

答案必须区分：坐标梯度与方向导数、可逆与奇异、数学表达与数值实现、局部可逆与全局双射。D 层需给可复现诊断；E 层需指出失效的准确前提。
