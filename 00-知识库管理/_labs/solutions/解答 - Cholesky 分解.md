---
type: solution
status: draft
area: [labs, math/matrix-analysis, math/numerical-linear-algebra]
topic: "[[Cholesky 分解]]"
exercise: "[[习题 - Cholesky 分解]]"
prerequisites: ["[[二次型与正定矩阵]]", "[[QR 分解]]"]
related: ["[[条件数]]", "[[练习与测验 MOC]]"]
sources: []
created: 2026-08-15
updated: 2026-08-15
---

# 解答 - Cholesky 分解

> [!warning] 使用边界
> 先独立作答。Cholesky 失败不只是“程序报错”：它通常是在暴露非对称、不正定、秩亏、舍入误差或建模参数化中的某一种问题。

## MA-CHOL-A01

$\boldsymbol A_1$ 对称，且顺序主子式为

$$
2>0,
\qquad
\det(\boldsymbol A_1)=3>0,
$$

所以它正定，存在唯一正对角 Cholesky 分解。

$\boldsymbol A_2$ 对称，但

$$
\det(\boldsymbol A_2)=-3<0,
$$

故它不定，不存在该分解。

$\boldsymbol A_3$ 对称半正定，但行列式为 0，因而奇异。它没有对角严格为正、可逆的 Cholesky 因子；允许零对角时可以有退化的 Gram 型因子。

$\boldsymbol A_4$ 不是对称矩阵，而任何 $\boldsymbol L\boldsymbol L^{\top}$ 都必定对称，因此不存在这种分解。

## MA-CHOL-B01

设

$$
\boldsymbol L=
\begin{bmatrix}
l_{11}&0\\
l_{21}&l_{22}
\end{bmatrix}.
$$

由 $\boldsymbol L\boldsymbol L^{\top}=\boldsymbol A$，逐项得到

$$
l_{11}^2=9,
\qquad
l_{11}l_{21}=3,
\qquad
l_{21}^2+l_{22}^2=5.
$$

取正对角：

$$
l_{11}=3,
\qquad
l_{21}=1,
\qquad
l_{22}=2.
$$

所以

$$
\boldsymbol L=
\begin{bmatrix}3&0\\1&2\end{bmatrix}.
$$

先做前代：

$$
\begin{bmatrix}3&0\\1&2\end{bmatrix}
\begin{bmatrix}y_1\\y_2\end{bmatrix}
=
\begin{bmatrix}15\\13\end{bmatrix}.
$$

第一行给 $y_1=5$，第二行给

$$
5+2y_2=13
\quad\Longrightarrow\quad
y_2=4.
$$

再做回代：

$$
\begin{bmatrix}3&1\\0&2\end{bmatrix}
\begin{bmatrix}x_1\\x_2\end{bmatrix}
=
\begin{bmatrix}5\\4\end{bmatrix}.
$$

第二行给 $x_2=2$，第一行给

$$
3x_1+2=5
\quad\Longrightarrow\quad
x_1=1.
$$

检查：

$$
\boldsymbol A\boldsymbol x
=\begin{bmatrix}9&3\\3&5\end{bmatrix}
\begin{bmatrix}1\\2\end{bmatrix}
=\begin{bmatrix}15\\13\end{bmatrix}
=\boldsymbol b.
$$

## MA-CHOL-C01

首先

$$
\boldsymbol A^{\top}
=(\boldsymbol L\boldsymbol L^{\top})^{\top}
=\boldsymbol L\boldsymbol L^{\top}
=\boldsymbol A,
$$

所以 $\boldsymbol A$ 对称。

对任意非零 $\boldsymbol x$，

$$
\boldsymbol x^{\top}\boldsymbol A\boldsymbol x
=\boldsymbol x^{\top}\boldsymbol L\boldsymbol L^{\top}\boldsymbol x
=\|\boldsymbol L^{\top}\boldsymbol x\|_2^2.
$$

$\boldsymbol L$ 的对角线全非零，所以它和 $\boldsymbol L^{\top}$ 都可逆。非零 $\boldsymbol x$ 不可能满足 $\boldsymbol L^{\top}\boldsymbol x=\boldsymbol0$，故上式严格大于 0。因此 $\boldsymbol A\succ0$。

利用行列式乘法和三角矩阵行列式：

$$
\det(\boldsymbol A)
=\det(\boldsymbol L)\det(\boldsymbol L^{\top})
=\left(\prod_{i=1}^n l_{ii}\right)^2
=\prod_{i=1}^n l_{ii}^2.
$$

由于每个 $l_{ii}>0$，可以取对数：

$$
\log\det(\boldsymbol A)
=\sum_{i=1}^n\log(l_{ii}^2)
=2\sum_{i=1}^n\log l_{ii}.
$$

高维行列式可能极大而上溢，或极小而下溢；先求乘积还会扩大动态范围。把乘法转成对数求和可以让中间量保持可表示，并复用已经计算的 Cholesky 对角线。不过若矩阵极度病态，因子本身仍可能不准确；对数公式不是条件性问题的万能修复。

## MA-CHOL-D01

递推给出

$$
l_{11}=\sqrt{a_{11}}=1,
\qquad
l_{21}=\frac{a_{21}}{l_{11}}=1,
$$

以及

$$
l_{22}
=\sqrt{a_{22}-l_{21}^2}
=\sqrt{1-1}
=0.
$$

第二个主元为零，是因为第二列与第一列相同，没有新增独立方向；矩阵存在零特征值，秩只有 1。

它仍然可以写成

$$
\boldsymbol A
=\begin{bmatrix}1\\1\end{bmatrix}
\begin{bmatrix}1&1\end{bmatrix}
=\boldsymbol B\boldsymbol B^{\top}.
$$

也可以形式上写成

$$
\boldsymbol A
=\begin{bmatrix}1&0\\1&0\end{bmatrix}
\begin{bmatrix}1&1\\0&0\end{bmatrix},
$$

但这个下三角因子奇异、对角不全正。Gram 型分解只保证半正定；标准 Cholesky 的正对角和可逆性对应严格正定。

加入 $\varepsilon\boldsymbol I$ 后，特征值从 $2,0$ 变成 $2+\varepsilon,\varepsilon$。当 $\varepsilon>0$ 时矩阵严格正定，标准 Cholesky 恢复存在；与此同时我们求解和解释的已经是正则化矩阵，而不是原奇异矩阵。

## MA-CHOL-E01

若 $\boldsymbol\epsilon\sim\mathcal N(\boldsymbol0,\boldsymbol I)$，则

$$
\boldsymbol z=\boldsymbol\mu+\boldsymbol L\boldsymbol\epsilon
$$

的均值为 $\boldsymbol\mu$，协方差为

$$
\operatorname{Cov}(\boldsymbol z)
=\boldsymbol L\boldsymbol I\boldsymbol L^{\top}
=\boldsymbol\Sigma.
$$

白化不需要形成 $\boldsymbol L^{-1}$。令 $\boldsymbol r=\boldsymbol z-\boldsymbol\mu$，通过三角求解

$$
\boldsymbol L\boldsymbol y=\boldsymbol r
$$

得到 $\boldsymbol y$；在模型成立时，$\boldsymbol y\sim\mathcal N(\boldsymbol0,\boldsymbol I)$。

高斯二次项可写成

$$
(\boldsymbol z-\boldsymbol\mu)^{\top}
\boldsymbol\Sigma^{-1}
(\boldsymbol z-\boldsymbol\mu)
=\|\boldsymbol y\|_2^2,
$$

对数行列式是

$$
\log\det\boldsymbol\Sigma
=2\sum_i\log l_{ii}.
$$

这样只需要一次 Cholesky 和三角求解，无需显式求逆。显式逆通常需要更多计算和存储，还会把本可由稳定求解完成的问题变成更敏感的矩阵构造。

jitter 把 $\boldsymbol\Sigma$ 替换为 $\boldsymbol\Sigma+\varepsilon\boldsymbol I$，抬高小特征值并改善条件数。但失败前应先检查：

- 是否因实现错误导致矩阵不对称；
- 协方差参数化是否本应保证半正定；
- 是否有数据秩亏、重复样本或批量太小；
- 是否出现 NaN、Inf、尺度溢出或混合精度误差；
- $\varepsilon$ 相对矩阵尺度是否合理；
- 模型是否真的需要完整严格正定协方差。

jitter 是有含义的正则化，不应成为掩盖上游错误的固定补丁。

## 无提示重做

- [ ] 48 小时后不看提示重做 MA-CHOL-B01 与 MA-CHOL-C01。
- [ ] 把 MA-CHOL-E01 改写成批量协方差的伪代码，并标注每个张量形状。

