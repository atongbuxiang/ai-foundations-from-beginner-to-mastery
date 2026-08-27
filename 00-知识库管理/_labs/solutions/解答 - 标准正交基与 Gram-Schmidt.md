---
type: solution
status: draft
area: [labs, math/linear-algebra]
topic: "[[标准正交基与 Gram-Schmidt]]"
exercise: "[[习题 - 标准正交基与 Gram-Schmidt]]"
prerequisites: ["[[内积空间]]", "[[正交投影]]"]
related: ["[[QR 分解]]", "[[练习与测验 MOC]]"]
sources: []
created: 2026-08-14
updated: 2026-08-14
---

# 解答 - 标准正交基与 Gram-Schmidt

> [!warning] 使用边界
> 先完成独立尝试并记录卡点。能顺着读懂解答不等于能独立重建；使用提示或解答后，请在 48 小时后无提示重做。

## LA-GS-A01

两列分别为

$$
\boldsymbol q_1=\frac1{\sqrt2}(1,1,0)^{\top},
\qquad
\boldsymbol q_2=\frac1{\sqrt2}(1,-1,0)^{\top}.
$$

长度和内积：

$$
\|\boldsymbol q_1\|_2^2
=\|\boldsymbol q_2\|_2^2=1,
\qquad
\boldsymbol q_1^{\top}\boldsymbol q_2
=\frac{1-1}{2}=0.
$$

因此

$$
\boldsymbol Q^{\top}\boldsymbol Q
=
\begin{bmatrix}
\boldsymbol q_1^{\top}\boldsymbol q_1&
\boldsymbol q_1^{\top}\boldsymbol q_2\\
\boldsymbol q_2^{\top}\boldsymbol q_1&
\boldsymbol q_2^{\top}\boldsymbol q_2
\end{bmatrix}
=\boldsymbol I_2.
$$

另一方面，

$$
\boldsymbol Q\boldsymbol Q^{\top}
=\boldsymbol q_1\boldsymbol q_1^{\top}
+\boldsymbol q_2\boldsymbol q_2^{\top}
=
\begin{bmatrix}
1&0&0\\
0&1&0\\
0&0&0
\end{bmatrix}
\ne\boldsymbol I_3.
$$

$\boldsymbol Q^{\top}\boldsymbol Q$ 表示先把标准正交坐标合成为向量，再读回坐标，所以在 $\mathbb R^2$ 坐标空间中是恒等映射。

$\boldsymbol Q\boldsymbol Q^{\top}$ 表示把 $\mathbb R^3$ 向量投影到
$\operatorname{span}(\boldsymbol e_1,\boldsymbol e_2)$，因此会消去第三个坐标。

## LA-GS-B01

第一步：

$$
r_{11}=\|\boldsymbol a_1\|_2=\sqrt2,
\qquad
\boldsymbol q_1
=\frac1{\sqrt2}
\begin{bmatrix}1\\1\\0\end{bmatrix}.
$$

第二列沿第一方向的坐标：

$$
r_{12}
=\boldsymbol q_1^{\top}\boldsymbol a_2
=\frac{1+1+0}{\sqrt2}
=\sqrt2.
$$

投影：

$$
r_{12}\boldsymbol q_1
=
\begin{bmatrix}1\\1\\0\end{bmatrix}.
$$

残差：

$$
\boldsymbol v_2
=\boldsymbol a_2-r_{12}\boldsymbol q_1
=
\begin{bmatrix}0\\0\\1\end{bmatrix}.
$$

因此

$$
r_{22}=\|\boldsymbol v_2\|_2=1,
\qquad
\boldsymbol q_2
=
\begin{bmatrix}0\\0\\1\end{bmatrix}.
$$

检查：

$$
\boldsymbol q_1^{\top}\boldsymbol q_2=0,
\qquad
\|\boldsymbol q_1\|_2=\|\boldsymbol q_2\|_2=1.
$$

## LA-GS-C01

假设

$$
\sum_{i=1}^{k}c_i\boldsymbol q_i=\boldsymbol0.
$$

固定任意 $j\in\{1,\ldots,k\}$，两边与
$\boldsymbol q_j$ 做内积：

$$
\left\langle
\sum_{i=1}^{k}c_i\boldsymbol q_i,
\boldsymbol q_j
\right\rangle
=
\langle\boldsymbol0,\boldsymbol q_j\rangle=0.
$$

利用内积线性：

$$
\sum_{i=1}^{k}
c_i\langle\boldsymbol q_i,\boldsymbol q_j\rangle=0.
$$

标准正交性给出

$$
\langle\boldsymbol q_i,\boldsymbol q_j\rangle
=
\begin{cases}
1,&i=j,\\
0,&i\ne j.
\end{cases}
$$

所以和只剩 $c_j=0$。由于 $j$ 任意，所有系数都为零，向量组线性无关。

## LA-GS-D01

第一步：

$$
\boldsymbol q_1=
\begin{bmatrix}1\\0\end{bmatrix}.
$$

第二个投影系数为 $r_{12}=2$，因此

$$
\boldsymbol v_2
=
\begin{bmatrix}2\\0\end{bmatrix}
-2\begin{bmatrix}1\\0\end{bmatrix}
=\boldsymbol0.
$$

于是 $r_{22}=0$，无法计算

$$
\boldsymbol q_2=\frac{\boldsymbol v_2}{r_{22}}.
$$

失败原因是
$\boldsymbol a_2=2\boldsymbol a_1$，没有第二个新方向。但它们张成的一维空间仍有标准正交基

$$
\left\{
\begin{bmatrix}1\\0\end{bmatrix}
\right\}.
$$

## LA-GS-E01

由 $\boldsymbol L=\boldsymbol Q\boldsymbol T$，

$$
\Delta\boldsymbol W
=\boldsymbol Q(\boldsymbol T\boldsymbol R).
$$

令
$\widetilde{\boldsymbol R}=\boldsymbol T\boldsymbol R$，
得到

$$
\Delta\boldsymbol W
=\boldsymbol Q\widetilde{\boldsymbol R}.
$$

矩阵乘积没有改变，只是重新选择了中间 $r$ 维空间的坐标。因此更新矩阵和左侧列空间都不变。

$\boldsymbol Q$ 的列在欧氏内积下正交；统计独立却是随机变量联合分布的性质。零相关或正交一般不推出独立，除非再加入联合高斯等条件。

## 无提示重做

- [ ] 48 小时后重做所有使用提示或解答的题。
- [ ] 把 LA-GS-B01 的输入顺序交换，观察输出基是否改变。

