---
type: solution
status: draft
area: [labs, math/linear-algebra, math/numerical-linear-algebra]
topic: "[[QR 分解]]"
exercise: "[[习题 - QR 分解]]"
prerequisites: ["[[标准正交基与 Gram-Schmidt]]", "[[最小二乘]]"]
related: ["[[Cholesky 分解]]", "[[练习与测验 MOC]]"]
sources: []
created: 2026-08-15
updated: 2026-08-15
---

# 解答 - QR 分解

> [!warning] 使用边界
> 先独立作答。数值算法题不存在只凭方法名称就完整的答案，必须说明问题结构、条件性和需要的输出。

## LA-QR-A01

薄 QR 的形状为

$$
\boldsymbol Q\in\mathbb R^{8\times3},
\qquad
\boldsymbol R\in\mathbb R^{3\times3}.
$$

标准正交列给出

$$
\boldsymbol Q^{\top}\boldsymbol Q
=\boldsymbol I_3.
$$

而

$$
\boldsymbol Q\boldsymbol Q^{\top}
\in\mathbb R^{8\times8}
$$

是到
$\mathcal R(\boldsymbol Q)=\mathcal R(\boldsymbol A)$
的正交投影，不是 $\boldsymbol I_8$。

满列秩意味着 Gram–Schmidt 每一步残差非零，所以
$r_{jj}>0$。上三角矩阵对角全非零当且仅当可逆，因此
$\boldsymbol R$ 可逆。

## LA-QR-B01

两列

$$
\boldsymbol a_1=(1,1)^{\top},
\qquad
\boldsymbol a_2=(1,-1)^{\top}
$$

正交，且长度都是 $\sqrt2$。所以

$$
\boldsymbol Q
=\frac1{\sqrt2}
\begin{bmatrix}
1&1\\
1&-1
\end{bmatrix},
\qquad
\boldsymbol R
=
\begin{bmatrix}
\sqrt2&0\\
0&\sqrt2
\end{bmatrix}.
$$

直接相乘：

$$
\boldsymbol Q^{\top}\boldsymbol Q=\boldsymbol I_2,
\qquad
\boldsymbol Q\boldsymbol R
=
\begin{bmatrix}1&1\\1&-1\end{bmatrix}
=\boldsymbol A.
$$

对角线为正，满足唯一性约定。

## LA-QR-C01

代入 QR：

$$
\begin{aligned}
\boldsymbol A^{*}\boldsymbol A
&=
(\boldsymbol Q\boldsymbol R)^{*}
(\boldsymbol Q\boldsymbol R)\\
&=
\boldsymbol R^{*}\boldsymbol Q^{*}
\boldsymbol Q\boldsymbol R\\
&=
\boldsymbol R^{*}\boldsymbol I\boldsymbol R\\
&=
\boldsymbol R^{*}\boldsymbol R.
\end{aligned}
$$

第二行使用乘积共轭转置会反转顺序；第三行使用标准正交列。

满列秩时 $\boldsymbol A^{*}\boldsymbol A\succ0$，而
$\boldsymbol R$ 是正对角上三角，因此它正是上三角 Cholesky 因子。

$\boldsymbol A^{*}\boldsymbol A$ 的特征值为
$\sigma_i(\boldsymbol A)^2$，所以

$$
\begin{aligned}
\kappa_2(\boldsymbol A^{*}\boldsymbol A)
&=
\frac{\lambda_{\max}(\boldsymbol A^{*}\boldsymbol A)}
{\lambda_{\min}(\boldsymbol A^{*}\boldsymbol A)}\\
&=
\frac{\sigma_1(\boldsymbol A)^2}
{\sigma_n(\boldsymbol A)^2}\\
&=
\kappa_2(\boldsymbol A)^2.
\end{aligned}
$$

## LA-QR-D01

第二列满足

$$
\boldsymbol a_2=2\boldsymbol a_1,
$$

所以列线性相关，秩为 1。

第一步得到

$$
\boldsymbol q_1
=\frac1{\sqrt{14}}(1,2,3)^{\top}.
$$

第二列的投影就是自身，残差为零，因此
$r_{22}=0$，不能归一化出第二个方向。

说“QR 分解不存在”不准确：

- 可以得到含零对角的上三角/上梯形因子；
- 可以只保留秩 1 的列空间基；
- 可以使用带列主元 QR 揭示秩。

失效的是“满列秩薄 QR 中 $\boldsymbol R$ 可逆”的结论。
由于 $\mathcal N(\boldsymbol A)\ne\{\boldsymbol0\}$，产生同一预测的参数不唯一。

## NLA-QR-E01

显式正规方程逆不应作为默认实现：

1. 形成 $\boldsymbol X^{\top}\boldsymbol X$ 会平方二范数条件数；
2. 显式求逆比解线性方程更昂贵且通常更不稳定；
3. 近秩亏时可能丢失可辨识方向的有效数字。

Householder QR：

- 适合满列秩或数值上良态/中度病态的高瘦稠密问题；
- 通常比 SVD 便宜；
- 通过三角求解得到最小二乘解；
- 需要秩诊断时可使用带列主元 QR。

SVD：

- 成本更高；
- 直接显示奇异值、数值秩和近零方向；
- 适合严重病态、最小范数解、正则化或谱解释。

至少报告残差、相对残差、条件数估计或奇异值范围、数值秩阈值、特征缩放、计算精度、算法和正则化。验证集误差还需单独报告，不能把数值残差等同于泛化能力。

## 无提示重做

- [ ] 48 小时后重做 LA-QR-C01。
- [ ] 为 NLA-QR-E01 增加“矩阵稀疏且只能做矩阵—向量乘积”的变式。

