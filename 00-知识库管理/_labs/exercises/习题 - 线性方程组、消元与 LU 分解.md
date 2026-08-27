---
type: exercise
status: draft
area: [labs, math/linear-algebra, math/numerical-linear-algebra]
topic: "[[线性方程组、消元与 LU 分解]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[线性映射]]", "[[四个基本子空间]]"]
related: ["[[Cholesky 分解]]", "[[练习与测验 MOC]]"]
solution: "[[解答 - 线性方程组、消元与 LU 分解]]"
created: 2026-08-15
updated: 2026-08-15
---

# 习题 - 线性方程组、消元与 LU 分解

> [!abstract] 训练目标
> 从解集与形状识别开始，完整执行一次 LU 与三角求解，证明分解唯一性，辨认无主元消元的失败，并把 solve 思维迁移到隐式 AI 模块。

## A. 识别与复述

### LA-LU-A01

设

$$
\boldsymbol A\in\mathbb R^{n\times n},
\qquad
\boldsymbol P\boldsymbol A
=\boldsymbol L\boldsymbol U,
$$

其中 $\boldsymbol P$ 是 permutation matrix，
$\boldsymbol L$ 是单位下三角，
$\boldsymbol U$ 是可逆上三角。

回答：

1. 求解 $\boldsymbol A\boldsymbol x=\boldsymbol b$ 时，两个三角方程分别是什么？
2. 前向代入和后向代入各自按什么顺序进行？
3. 为什么 $\boldsymbol U$ 可逆？
4. 若有 $s$ 个不同右端，哪些工作可以复用？
5. $\boldsymbol P$ 作用于未知量还是方程？

## B. 手算与构造

### LA-LU-B01

对

$$
\boldsymbol A=
\begin{bmatrix}
2&1&1\\
4&-6&0\\
-2&7&2
\end{bmatrix},
\qquad
\boldsymbol b=
\begin{bmatrix}
3\\-8\\10
\end{bmatrix},
$$

不换行完成：

1. 写出每一步 multiplier；
2. 求 $\boldsymbol A=\boldsymbol L\boldsymbol U$；
3. 解 $\boldsymbol L\boldsymbol y=\boldsymbol b$；
4. 解 $\boldsymbol U\boldsymbol x=\boldsymbol y$；
5. 检查 $\boldsymbol L\boldsymbol U=\boldsymbol A$ 和
   $\boldsymbol A\boldsymbol x=\boldsymbol b$。

## C. 推导与证明

### LA-LU-C01

设

$$
\boldsymbol A
=\boldsymbol L_1\boldsymbol U_1
=\boldsymbol L_2\boldsymbol U_2,
$$

其中两个 $\boldsymbol L_i$ 都是单位下三角，两个
$\boldsymbol U_i$ 都是可逆上三角。

1. 证明
   $$
   \boldsymbol L_2^{-1}\boldsymbol L_1
   =
   \boldsymbol U_2\boldsymbol U_1^{-1};
   $$
2. 证明一个同时是单位下三角和上三角的矩阵只能是单位阵；
3. 推出规范化 LU 唯一；
4. 构造一个例子说明：若不固定 $\boldsymbol L$ 的对角线为 1，分解一般不唯一。

## D. 边界与反例

### NLA-LU-D01

考虑

$$
\boldsymbol A=
\begin{bmatrix}
0&1\\
1&1
\end{bmatrix}.
$$

1. 证明 $\boldsymbol A$ 可逆；
2. 说明无换行消元在哪一步失败；
3. 给出一个 permutation matrix
   $\boldsymbol P$，并求
   $\boldsymbol P\boldsymbol A=\boldsymbol L\boldsymbol U$；
4. 解释这个例子为什么反驳“矩阵可逆就不需要选主元”；
5. 再把左上角的 0 改成很小的 $\varepsilon>0$，说明即使能除，为什么仍可能数值危险。

## E. AI 迁移

### AI-LU-E01

模型中的隐式变量满足

$$
\boldsymbol A(\boldsymbol\theta)\boldsymbol x
=
\boldsymbol b(\boldsymbol\theta),
\qquad
\boldsymbol A\in\mathbb R^{n\times n}.
$$

某个标量损失 $\mathcal L$ 对 $\boldsymbol x$ 的梯度为

$$
\boldsymbol g=\nabla_{\boldsymbol x}\mathcal L.
$$

1. 对方程微分，推导 $\mathrm d\boldsymbol x$ 满足的线性系统；
2. 令伴随变量满足
   $$
   \boldsymbol A^{\top}\boldsymbol\lambda=\boldsymbol g,
   $$
   推导
   $$
   \mathrm d\mathcal L
   =
   \boldsymbol\lambda^{\top}\mathrm d\boldsymbol b
   -
   \boldsymbol\lambda^{\top}
   (\mathrm d\boldsymbol A)\boldsymbol x;
   $$
3. 说明为什么前向和反向都应该调用线性求解器，而不是显式形成逆矩阵；
4. 若 $\boldsymbol A$ 在多次反向中不变，哪些分解可以复用？
5. 若 $\boldsymbol A$ 严重病态，小残差是否足以说明梯度准确？

## 分级提示

### 方向提示

- LA-LU-B01：第一列 multipliers 是 $2,-1$，第二列 multiplier 是 $-1$。
- LA-LU-C01：下三角矩阵的逆仍为下三角，上三角同理。
- NLA-LU-D01：交换两行后矩阵已经是上三角。

### 结构提示

- AI-LU-E01：先写
  $$
  (\mathrm d\boldsymbol A)\boldsymbol x
  +\boldsymbol A\,\mathrm d\boldsymbol x
  =\mathrm d\boldsymbol b,
  $$
  再用 $\boldsymbol g=\boldsymbol A^{\top}\boldsymbol\lambda$。

### 计算提示

- LA-LU-B01 的正确上三角因子最后一行是
  $[0,0,1]$。

## 解答入口

完成独立尝试后再打开：[[解答 - 线性方程组、消元与 LU 分解]]。

