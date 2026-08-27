---
type: solution
status: draft
area: [labs, math/linear-algebra, math/numerical-linear-algebra]
topic: "[[线性方程组、消元与 LU 分解]]"
exercise: "[[习题 - 线性方程组、消元与 LU 分解]]"
prerequisites: ["[[线性映射]]", "[[四个基本子空间]]"]
related: ["[[Cholesky 分解]]", "[[练习与测验 MOC]]"]
sources: []
created: 2026-08-15
updated: 2026-08-15
---

# 解答 - 线性方程组、消元与 LU 分解

> [!warning] 使用边界
> 先独立作答。手算 LU 的目标不是背矩阵，而是能解释每个 multiplier、换行和三角求解步骤对应什么操作。

## LA-LU-A01

由

$$
\boldsymbol P\boldsymbol A
=
\boldsymbol L\boldsymbol U
$$

和

$$
\boldsymbol A\boldsymbol x=\boldsymbol b
$$

得到

$$
\boldsymbol L\boldsymbol U\boldsymbol x
=
\boldsymbol P\boldsymbol b.
$$

先做前向代入：

$$
\boldsymbol L\boldsymbol y
=
\boldsymbol P\boldsymbol b,
$$

再做后向代入：

$$
\boldsymbol U\boldsymbol x=\boldsymbol y.
$$

下三角系统从第一行向最后一行解；上三角系统从最后一行向第一行解。

$\boldsymbol U$ 是方形上三角矩阵，且题目已经声明它可逆；等价地，它的每个对角元素非零。

若有多个右端，可以复用：

- permutation 信息；
- $\boldsymbol L,\boldsymbol U$ 因子；
- 实现中的数据结构和重排序。

每个新右端只需重新计算 $\boldsymbol P\boldsymbol b$，再做两次三角求解。

$\boldsymbol P$ 左乘 $\boldsymbol A$ 和 $\boldsymbol b$，交换的是方程顺序，不是未知量顺序。若要重排未知量，需要右乘另一个 permutation matrix，并相应解释变量坐标。

## LA-LU-B01

第一列：

$$
\ell_{21}=\frac42=2,
\qquad
\ell_{31}=\frac{-2}{2}=-1.
$$

消去得到

$$
\begin{bmatrix}
2&1&1\\
0&-8&-2\\
0&8&3
\end{bmatrix}.
$$

第二列：

$$
\ell_{32}=\frac8{-8}=-1.
$$

因此

$$
\boldsymbol U=
\begin{bmatrix}
2&1&1\\
0&-8&-2\\
0&0&1
\end{bmatrix},
\qquad
\boldsymbol L=
\begin{bmatrix}
1&0&0\\
2&1&0\\
-1&-1&1
\end{bmatrix}.
$$

乘法检查：

$$
\begin{aligned}
\boldsymbol L\boldsymbol U
&=
\begin{bmatrix}
1&0&0\\
2&1&0\\
-1&-1&1
\end{bmatrix}
\begin{bmatrix}
2&1&1\\
0&-8&-2\\
0&0&1
\end{bmatrix}\\
&=
\begin{bmatrix}
2&1&1\\
4&-6&0\\
-2&7&2
\end{bmatrix}
=\boldsymbol A.
\end{aligned}
$$

前向代入：

$$
\begin{aligned}
y_1&=3,\\
2y_1+y_2&=-8
\quad\Longrightarrow\quad y_2=-14,\\
-y_1-y_2+y_3&=10
\quad\Longrightarrow\quad y_3=-1.
\end{aligned}
$$

回代：

$$
\begin{aligned}
x_3&=-1,\\
-8x_2-2x_3&=-14
\quad\Longrightarrow\quad x_2=2,\\
2x_1+x_2+x_3&=3
\quad\Longrightarrow\quad x_1=1.
\end{aligned}
$$

所以

$$
\boldsymbol x=(1,2,-1)^{\top}.
$$

代回：

$$
\boldsymbol A\boldsymbol x
=
\begin{bmatrix}
2+2-1\\
4-12\\
-2+14-2
\end{bmatrix}
=
\begin{bmatrix}
3\\-8\\10
\end{bmatrix}
=\boldsymbol b.
$$

## LA-LU-C01

从

$$
\boldsymbol L_1\boldsymbol U_1
=
\boldsymbol L_2\boldsymbol U_2
$$

出发，左乘 $\boldsymbol L_2^{-1}$，右乘
$\boldsymbol U_1^{-1}$：

$$
\boldsymbol L_2^{-1}\boldsymbol L_1
=
\boldsymbol U_2\boldsymbol U_1^{-1}.
$$

单位下三角矩阵的逆和乘积仍是单位下三角，所以左边单位下三角。可逆上三角矩阵的逆和乘积仍是上三角，所以右边上三角。

同一个矩阵同时满足这两种结构：

- 上三角要求主对角线下方全为 0；
- 单位下三角要求主对角线上方全为 0，且对角线全为 1。

因此它只能是 $\boldsymbol I$。于是

$$
\boldsymbol L_2^{-1}\boldsymbol L_1=\boldsymbol I
\quad\Longrightarrow\quad
\boldsymbol L_1=\boldsymbol L_2,
$$

且

$$
\boldsymbol U_2\boldsymbol U_1^{-1}=\boldsymbol I
\quad\Longrightarrow\quad
\boldsymbol U_1=\boldsymbol U_2.
$$

若不固定对角线，取任意可逆对角矩阵
$\boldsymbol D$：

$$
\boldsymbol A
=
\boldsymbol L\boldsymbol U
=
(\boldsymbol L\boldsymbol D)
(\boldsymbol D^{-1}\boldsymbol U).
$$

$\boldsymbol L\boldsymbol D$ 仍下三角，
$\boldsymbol D^{-1}\boldsymbol U$ 仍上三角。只要
$\boldsymbol D\ne\boldsymbol I$，就得到不同分解。

## NLA-LU-D01

行列式为

$$
\det(\boldsymbol A)=0\cdot1-1\cdot1=-1\ne0,
$$

所以 $\boldsymbol A$ 可逆。

无换行消元第一步要用 $a_{11}=0$ 作为 pivot，并计算

$$
\ell_{21}=\frac{1}{0},
$$

因此立即失败。

取

$$
\boldsymbol P=
\begin{bmatrix}
0&1\\
1&0
\end{bmatrix},
$$

则

$$
\boldsymbol P\boldsymbol A
=
\begin{bmatrix}
1&1\\
0&1
\end{bmatrix}.
$$

它本身已上三角，所以可以取

$$
\boldsymbol L=\boldsymbol I,
\qquad
\boldsymbol U=
\begin{bmatrix}
1&1\\
0&1
\end{bmatrix}.
$$

该例表明：可逆性保证方程唯一可解，但不保证当前行顺序的第一个候选 pivot 非零。

若改成

$$
\boldsymbol A_{\varepsilon}
=
\begin{bmatrix}
\varepsilon&1\\
1&1
\end{bmatrix},
$$

无换行 multiplier 为

$$
\ell_{21}=\frac1{\varepsilon}.
$$

$\varepsilon$ 很小时 multiplier 巨大，更新第二行会产生巨大中间数以及接近数相减，使舍入误差被放大。部分选主元会选择绝对值为 1 的第二行作为 pivot，避免这个危险。

## AI-LU-E01

对

$$
\boldsymbol A\boldsymbol x=\boldsymbol b
$$

微分，使用乘积法则：

$$
(\mathrm d\boldsymbol A)\boldsymbol x
+\boldsymbol A\,\mathrm d\boldsymbol x
=
\mathrm d\boldsymbol b.
$$

所以

$$
\boldsymbol A\,\mathrm d\boldsymbol x
=
\mathrm d\boldsymbol b
-(\mathrm d\boldsymbol A)\boldsymbol x.
$$

损失微分为

$$
\mathrm d\mathcal L
=
\boldsymbol g^{\top}\mathrm d\boldsymbol x.
$$

伴随方程给出

$$
\boldsymbol g
=
\boldsymbol A^{\top}\boldsymbol\lambda.
$$

代入：

$$
\begin{aligned}
\mathrm d\mathcal L
&=
\boldsymbol\lambda^{\top}
\boldsymbol A\,\mathrm d\boldsymbol x\\
&=
\boldsymbol\lambda^{\top}
\left[
\mathrm d\boldsymbol b
-(\mathrm d\boldsymbol A)\boldsymbol x
\right]\\
&=
\boldsymbol\lambda^{\top}\mathrm d\boldsymbol b
-
\boldsymbol\lambda^{\top}
(\mathrm d\boldsymbol A)\boldsymbol x.
\end{aligned}
$$

前向需要解 $\boldsymbol A\boldsymbol x=\boldsymbol b$，反向需要解
$\boldsymbol A^{\top}\boldsymbol\lambda=\boldsymbol g$。成熟求解器能利用 pivoting、三角结构和批处理；显式逆增加计算与存储，也通常产生更差的数值路线。

若 $\boldsymbol A$ 在多次求解中不变，可复用：

- permutation；
- LU 因子；
- 转置系统所需的三角因子顺序；
- 稀疏符号分解与重排序。

严重病态时，小 residual

$$
\|\boldsymbol b-\boldsymbol A\widehat{\boldsymbol x}\|
$$

只说明 $\widehat{\boldsymbol x}$ 几乎满足方程，不保证它接近真解；伴随解和梯度也可能对微小输入误差高度敏感。还必须结合条件数、缩放、精度和后向误差判断。

## 无提示重做

- [ ] 48 小时后不看正文重做 LA-LU-B01。
- [ ] 把 NLA-LU-D01 改成 $\varepsilon=10^{-8}$，手工估计 multiplier。
- [ ] 用自己的语言解释 AI-LU-E01 中为什么只需一次伴随求解。

