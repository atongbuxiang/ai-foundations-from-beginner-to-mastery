---
type: exercise
status: draft
area: [labs, math/linear-algebra, math/numerical-linear-algebra]
topic: "[[QR 分解]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[标准正交基与 Gram-Schmidt]]", "[[最小二乘]]"]
related: ["[[Cholesky 分解]]", "[[练习与测验 MOC]]"]
solution: "[[解答 - QR 分解]]"
created: 2026-08-15
updated: 2026-08-15
---

# 习题 - QR 分解

> [!abstract] 训练目标
> 检查薄 QR 的形状和投影含义、独立完成小矩阵分解、推导 Gram 矩阵关系、识别秩亏边界，并为病态最小二乘选择合适算法。

## A. 识别与复述

### LA-QR-A01

设

$$
\boldsymbol A\in\mathbb R^{8\times3}
$$

满列秩，并有薄 QR

$$
\boldsymbol A=\boldsymbol Q\boldsymbol R.
$$

回答：

1. $\boldsymbol Q,\boldsymbol R$ 的形状；
2. $\boldsymbol Q^{\top}\boldsymbol Q$ 的形状和值；
3. $\boldsymbol Q\boldsymbol Q^{\top}$ 的形状和几何意义；
4. $\boldsymbol R$ 为什么可逆。

## B. 手算与构造

### LA-QR-B01

求

$$
\boldsymbol A=
\begin{bmatrix}
1&1\\
1&-1
\end{bmatrix}
$$

的正对角 QR 分解。完整检查
$\boldsymbol Q^{\top}\boldsymbol Q=\boldsymbol I$ 和
$\boldsymbol Q\boldsymbol R=\boldsymbol A$。

## C. 推导与证明

### LA-QR-C01

设 $\boldsymbol A=\boldsymbol Q\boldsymbol R$ 是满列秩薄 QR。

1. 推导
   $$
   \boldsymbol A^{*}\boldsymbol A
   =\boldsymbol R^{*}\boldsymbol R;
   $$
2. 说明为什么这使 $\boldsymbol R$ 成为
   $\boldsymbol A^{*}\boldsymbol A$ 的上三角 Cholesky 因子；
3. 利用奇异值说明
   $$
   \kappa_2(\boldsymbol A^{*}\boldsymbol A)
   =\kappa_2(\boldsymbol A)^2.
   $$

## D. 边界与反例

### LA-QR-D01

考虑

$$
\boldsymbol A=
\begin{bmatrix}
1&2\\
2&4\\
3&6
\end{bmatrix}.
$$

1. 说明它为什么不满列秩；
2. 对列做 Gram–Schmidt，指出在哪一步出现什么；
3. 说明“QR 分解不存在”是否准确；
4. 为什么不能再通过可逆 $\boldsymbol R$ 得到唯一最小二乘解？

## E. AI 迁移

### NLA-QR-E01

你要拟合线性 probe：

$$
\min_{\boldsymbol w}
\|\boldsymbol X\boldsymbol w-\boldsymbol y\|_2,
\qquad
\boldsymbol X\in\mathbb R^{100000\times512}.
$$

特征列尺度差异很大，而且可能近线性相关。比较：

1. 显式计算
   $(\boldsymbol X^{\top}\boldsymbol X)^{-1}
   \boldsymbol X^{\top}\boldsymbol y$；
2. Householder QR；
3. SVD。

说明哪种不应作为默认实现，QR 和 SVD 各自适合什么需求，并指出还需要报告哪些数值诊断。

## 分级提示

### 方向提示

- LA-QR-B01：两列已经正交，只需分别归一化。
- LA-QR-C01：代入 $\boldsymbol A=\boldsymbol Q\boldsymbol R$ 并使用
  $\boldsymbol Q^{*}\boldsymbol Q=\boldsymbol I$。
- LA-QR-D01：第二列是第一列的两倍。

### 结构提示

- NLA-QR-E01：比较条件数、是否能处理数值秩、计算代价和诊断信息。

### 计算提示

- LA-QR-B01：
  $$
  \boldsymbol Q
  =\frac1{\sqrt2}
  \begin{bmatrix}1&1\\1&-1\end{bmatrix}.
  $$

## 解答入口

完成独立尝试后再打开：[[解答 - QR 分解]]。

