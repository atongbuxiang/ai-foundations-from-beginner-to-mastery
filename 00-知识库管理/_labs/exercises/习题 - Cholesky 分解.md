---
type: exercise
status: draft
area: [labs, math/matrix-analysis, math/numerical-linear-algebra]
topic: "[[Cholesky 分解]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[二次型与正定矩阵]]", "[[QR 分解]]"]
related: ["[[条件数]]", "[[练习与测验 MOC]]"]
solution: "[[解答 - Cholesky 分解]]"
created: 2026-08-15
updated: 2026-08-15
---

# 习题 - Cholesky 分解

> [!abstract] 训练目标
> 学会辨认适用条件、手算分解与三角求解、证明因子的正定含义、识别半正定边界，并把分解用于协方差采样、白化和对数行列式。

## A. 识别与复述

### MA-CHOL-A01

对下列矩阵，判断是否存在“对角严格为正的实下三角”Cholesky 分解 $\boldsymbol A=\boldsymbol L\boldsymbol L^{\top}$，并说明理由：

$$
\boldsymbol A_1=\begin{bmatrix}2&1\\1&2\end{bmatrix},
\quad
\boldsymbol A_2=\begin{bmatrix}1&2\\2&1\end{bmatrix},
\quad
\boldsymbol A_3=\begin{bmatrix}1&1\\1&1\end{bmatrix},
\quad
\boldsymbol A_4=\begin{bmatrix}1&1\\0&1\end{bmatrix}.
$$

区分“不定”“半正定但奇异”和“非对称”三种失败原因。

## B. 手算与构造

### MA-CHOL-B01

对

$$
\boldsymbol A=
\begin{bmatrix}
9&3\\
3&5
\end{bmatrix},
\qquad
\boldsymbol b=
\begin{bmatrix}
15\\13
\end{bmatrix},
$$

1. 手算下三角 Cholesky 因子 $\boldsymbol L$；
2. 先解 $\boldsymbol L\boldsymbol y=\boldsymbol b$；
3. 再解 $\boldsymbol L^{\top}\boldsymbol x=\boldsymbol y$；
4. 用原方程检查答案。

## C. 推导与证明

### MA-CHOL-C01

设 $\boldsymbol L\in\mathbb R^{n\times n}$ 是对角严格为正的下三角矩阵，并令

$$
\boldsymbol A=\boldsymbol L\boldsymbol L^{\top}.
$$

证明：

1. $\boldsymbol A$ 对称正定；
2. $\det(\boldsymbol A)=\prod_{i=1}^n l_{ii}^2$；
3. 
   $$
   \log\det(\boldsymbol A)=2\sum_{i=1}^n\log l_{ii};
   $$
4. 为什么最后这个公式比先计算行列式再取对数更适合数值程序？

## D. 边界与反例

### MA-CHOL-D01

考虑半正定奇异矩阵

$$
\boldsymbol A=
\begin{bmatrix}
1&1\\
1&1
\end{bmatrix}.
$$

1. 按 Cholesky 递推公式计算 $l_{11},l_{21},l_{22}$；
2. 解释为什么第二个主元等于 0；
3. 它能否写成某个 $\boldsymbol B\boldsymbol B^{\top}$？
4. 为什么“存在 Gram 型分解”和“存在正对角、可逆的标准 Cholesky 因子”不是同一句话？
5. 加 $\varepsilon\boldsymbol I$ 后会发生什么？

## E. AI 迁移

### MA-CHOL-E01

一个潜变量模型使用高斯分布

$$
\boldsymbol z\sim\mathcal N(\boldsymbol\mu,\boldsymbol\Sigma),
\qquad
\boldsymbol\Sigma\in\mathbb R^{d\times d}.
$$

假设 $\boldsymbol\Sigma=\boldsymbol L\boldsymbol L^{\top}\succ0$。回答：

1. 如何由 $\boldsymbol\epsilon\sim\mathcal N(\boldsymbol0,\boldsymbol I)$ 构造样本 $\boldsymbol z$？
2. 如何把观测 $\boldsymbol z$ 白化为标准正态坐标？
3. 如何只用 $\boldsymbol L$ 计算高斯负对数似然中的二次项和 $\log\det\boldsymbol\Sigma$？
4. 若训练中 Cholesky 偶发失败，直接加入 jitter 有什么作用？在这样做前还应检查哪些建模或实现问题？
5. 为什么不应显式形成 $\boldsymbol\Sigma^{-1}$？

## 分级提示

### 方向提示

- MA-CHOL-A01：标准 Cholesky 的充要结构是实对称正定。
- MA-CHOL-B01：设 $\boldsymbol L=[l_{11},0;l_{21},l_{22}]$，逐元素比较。
- MA-CHOL-C01：把二次型写成 $\|\boldsymbol L^{\top}\boldsymbol x\|_2^2$。

### 结构提示

- MA-CHOL-D01：零主元对应一个零特征方向，但矩阵仍可写成秩 1 外积。
- MA-CHOL-E01：所有“逆”的动作都可以改成两次三角求解。

### 计算提示

- MA-CHOL-B01：正确因子为
  $$
  \boldsymbol L=\begin{bmatrix}3&0\\1&2\end{bmatrix}.
  $$

## 解答入口

完成独立尝试后再打开：[[解答 - Cholesky 分解]]。

