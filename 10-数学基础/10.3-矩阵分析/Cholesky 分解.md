---
type: concept
status: draft
area: [math/linear-algebra, math/matrix-analysis, math/numerical-linear-algebra]
aliases: [Cholesky Factorization, LL* 分解]
prerequisites: ["[[二次型与正定矩阵]]", "[[QR 分解]]"]
related: ["[[最小二乘]]", "[[条件数]]", "[[稳定求解线性方程组]]", "[[实验 - 正定边界、条件数与 Cholesky pivot]]", "[[矩阵分析 MOC]]"]
sources: ["Axler-LADR4e-7D", "MIT-18.335-L14", "Golub-VanLoan-Ch4"]
exercises: ["[[习题 - Cholesky 分解]]"]
solutions: ["[[解答 - Cholesky 分解]]"]
created: 2026-08-14
updated: 2026-08-27
---

# Cholesky 分解

> [!abstract] 本章主问题
> 正定性怎样转化为一个既可证明、又可计算的三角结构？每个 Hermitian 正定矩阵都能唯一写成
> $\boldsymbol A=\boldsymbol L\boldsymbol L^{*}$，其中
> $\boldsymbol L$ 是正对角下三角矩阵。它把二次能量变成平方范数，把线性求解变成两次三角代入，并统一服务于 log-determinant、白化和高斯采样。

> [!info] 学习目标
> 完成本章后，你应能：准确陈述 Cholesky 分解的存在唯一性条件；由 $A=LL^*$ 推出能量恒等式；手算低阶分解并推导逐列递推；用 Schur 补解释每个正主元；通过两次三角代入求解 SPD 系统；计算 log-determinant、白化和高斯采样；区分正定、半正定与对称不定输入所需的不同分解。

> [!question] 初学者读完必须能回答
> 1. 为什么正定性保证递推中的每个平方根都严格为正？
> 2. 把对角元规定为正，为什么能消除分解的符号不唯一性？
> 3. $x^*Ax=\|L^*x\|_2^2$ 怎样连接能量几何与三角分解？
> 4. Cholesky 递推与高斯消元、Schur 补之间是什么关系？
> 5. 为什么解 $Ax=b$ 应做前代和回代，而不应显式形成 $A^{-1}$？
> 6. 怎样从 $L$ 稳定计算 $\log\det A$，以及怎样实现白化和高斯采样？
> 7. 零主元或负主元分别在传达什么结构或数值警告？

下图回答：正定性怎样同时保证能量平方化、消元主元为正，以及一次分解支持多个计算接口？

![[00-知识库管理/_assets/figures/cholesky/fig-cholesky-energy-elimination-solve-v2.svg|880]]

> [!figure] 图 1：Cholesky 的结构、递推与计算接口
> **图源与改绘：** 本库原创教学图；内容参照 Golub–Van Loan、MIT 18.335 与正定矩阵的标准教材论述。
>
> **怎样读图。** 左栏从 $A=LL^*$ 读取能量平方化与 log-determinant；中栏把每一步主元看成剩余 Schur 补的曲率检查，正主元允许递推继续；右栏展示同一因子如何经两次三角代入解方程，并复用于白化和高斯采样。
>
> **适用边界（图没有证明什么）。** 无主元 $LL^*$ Cholesky 的标准保证要求 Hermitian 正定。半正定输入可能需要带主元或秩揭示版本；对称不定矩阵应转向 $LDL^*$ 及对称主元策略。接近零的主元同时可能反映建模退化、病态性或舍入误差，不能仅用“加一个小量”掩盖而不说明。

## 进入正文前：正定裕量会在消元中变成正主元

> [!info] 课程位置
> [[二次型与正定矩阵]]用谱和能量定义 $A\succ0$；本章回答更计算化的问题：正定性为什么能保证消元不遇到非正平方根？一旦得到 $L$，解方程、$\log\det A$、白化和高斯采样都变成三角计算。

> [!tip] 建议两遍阅读
> - **第一遍：** 手算 $2\times2$ 贯穿例，看懂 $A=LL^*$、能量平方化和两次三角代入。
> - **第二遍：** 再读 Schur 补存在性证明、递推实现、稳定性边界及半正定/不定输入的替代方案。

> [!question] 本章的推导问题链
> 1. 一个 $2\times2$ 下三角矩阵与其转置相乘后，各元素如何匹配？
> 2. 第二个对角元的被开方量为什么是 Schur 补？
> 3. 为什么 $A\succ0$ 保证这些 Schur 补一直为正？
> 4. 当最后一个主元趋近零时，分解失效之前已经告诉了我们什么？

### 继续跟踪 $H_\tau$

对上一章的

$$
H_\tau=
\begin{bmatrix}1&1-\tau\\1-\tau&1\end{bmatrix},
\qquad 0<\tau\le1,
$$

直接匹配元素得到

$$
\boxed{
L_\tau=
\begin{bmatrix}
1&0\\
1-\tau&\sqrt{2\tau-\tau^2}
\end{bmatrix}},
\qquad
H_\tau=L_\tau L_\tau^T.
$$

特别看第二个对角元：

$$
\ell_{22}^2
=1-(1-\tau)^2
=2\tau-\tau^2
=\tau(2-\tau)
=\det H_\tau.
$$

当 $\tau\downarrow0$ 时，$H_\tau$ 仍可在数学上保持正定，但第二个 pivot 已趋近零；在极限 $\tau=0$ 处，它只是秩一半正定矩阵。因此主元不只是算法中间量，也是正定边界的诊断信号。

> [!note] 符号账本
> | 符号 | 形状/约束 | 作用 |
> |---|---:|---|
> | $A$ | $n\times n$, $A=A^*\succ0$ | 待分解的 Hermitian 正定矩阵 |
> | $L$ | $n\times n$ 下三角，$\ell_{ii}>0$ | 唯一的 Cholesky 因子 |
> | $L^*$ | $n\times n$ 上三角 | 复数情形为共轭转置，不能随意写成 $L^T$ |
> | $\ell_{jj}^2$ | 正实数 | 第 $j$ 步 Schur 补的 pivot |
> | $b,x$ | $n$ 维向量 | 用 $Ly=b$ 和 $L^*x=y$ 解 $Ax=b$ |

## 阅读前检查

- [[二次型与正定矩阵]]：$\boldsymbol A\succ0$ 的方向能量与谱判据；
- [[QR 分解]]：上/下三角矩阵和标准正交分解；
- 三角方程的基本回代：下三角用前向代入，上三角用后向代入。

## 先看一个具体问题

给定

$$
\boldsymbol A=
\begin{bmatrix}
4&2\\
2&3
\end{bmatrix}.
$$

它正定，因为首个顺序主子式为 $4>0$，行列式为
$12-4=8>0$。

我们尝试寻找下三角矩阵

$$
\boldsymbol L=
\begin{bmatrix}
\ell_{11}&0\\
\ell_{21}&\ell_{22}
\end{bmatrix},
\qquad
\ell_{11},\ell_{22}>0,
$$

使

$$
\boldsymbol A=\boldsymbol L\boldsymbol L^{\top}.
$$

乘开：

$$
\boldsymbol L\boldsymbol L^{\top}
=
\begin{bmatrix}
\ell_{11}^2&\ell_{11}\ell_{21}\\
\ell_{11}\ell_{21}&\ell_{21}^2+\ell_{22}^2
\end{bmatrix}.
$$

逐项匹配：

$$
\ell_{11}=2,
\qquad
\ell_{21}=1,
\qquad
\ell_{22}=\sqrt{3-1}=\sqrt2.
$$

所以

$$
\boldsymbol L=
\begin{bmatrix}
2&0\\
1&\sqrt2
\end{bmatrix}.
$$

## 正式定义与定理

> [!theorem] Cholesky 分解
> 若
> $\boldsymbol A\in\mathbb F^{n\times n}$ Hermitian 正定，则存在唯一的下三角矩阵
> $\boldsymbol L$，其对角元素为正，并满足
> $$
> \boldsymbol A=\boldsymbol L\boldsymbol L^{*}.
> $$

> [!analysis] Cholesky 定理的公式七问
> | 问题 | 回答 |
> |---|---|
> | 输入契约是什么？ | $A$ 必须是方阵、Hermitian 且严格正定；这三个条件都不应省略。 |
> | 输出的形状和约定是什么？ | $L$ 与 $A$ 同阶、下三角且对角元严格为正；上三角约定写作 $A=R^*R$。 |
> | 为什么存在？ | 递归消元后的 Schur 补仍正定，所以每个对角被开方量都严格为正。 |
> | 为什么唯一？ | 正对角约定固定每个平方根的符号；两个候选因子的比值只能是单位下三角酉矩阵，因而是恒等矩阵。 |
> | 它怎样改写能量？ | $x^*Ax=\|L^*x\|_2^2$；正定二次型是经可逆线性变换后的欧氏平方长度。 |
> | 怎样验收数值结果？ | 检查 $\|A-LL^*\|/\|A\|$、对角元符号与最小 pivot；解方程时另查相对残差。 |
> | AI 中怎样调用？ | 用于高斯过程、协方差白化/采样、自然梯度和 $\log\det$；加 jitter 时必须记录尺度及模型含义。 |

也常使用上三角形式

$$
\boldsymbol A=\boldsymbol R^{*}\boldsymbol R,
\qquad
\boldsymbol R=\boldsymbol L^{*}.
$$

必须先声明采用哪一种约定。

## 为什么它表达“平方能量”

若
$\boldsymbol A=\boldsymbol L\boldsymbol L^{*}$，则

$$
\boldsymbol x^{*}\boldsymbol A\boldsymbol x
=
\boldsymbol x^{*}\boldsymbol L\boldsymbol L^{*}\boldsymbol x
=
\|\boldsymbol L^{*}\boldsymbol x\|_2^2.
$$

如果 $\boldsymbol L$ 可逆，$\boldsymbol x\ne0$ 时
$\boldsymbol L^{*}\boldsymbol x\ne0$，所以二次型严格为正。

反过来，Cholesky 定理表明每个正定能量都可以通过一个可逆线性变换化成普通欧氏平方长度。

> [!success] 第一遍停靠线
> 你应能手算 $H_\tau=L_\tau L_\tau^T$，说出第二个 pivot 为何随 $\tau\downarrow0$ 坍缩，并把 $Ax=b$ 拆成 $Ly=b$ 与 $L^*x=y$。做到这三件事后，可先进入 [[Rayleigh 商与极值表征]]，再回头学习递推细节。

## 逐项递推公式

写

$$
\boldsymbol A=\boldsymbol L\boldsymbol L^{*}.
$$

第 $(i,j)$ 个元素满足

$$
a_{ij}
=
\sum_{k=1}^{\min(i,j)}
\ell_{ik}\overline{\ell_{jk}}.
$$

### 对角元素

当 $i=j$：

$$
a_{jj}
=
\sum_{k=1}^{j-1}|\ell_{jk}|^2
+|\ell_{jj}|^2.
$$

规定 $\ell_{jj}>0$，得到

$$
\ell_{jj}
=
\sqrt{
a_{jj}
-\sum_{k=1}^{j-1}|\ell_{jk}|^2
}.
$$

### 对角线下方

当 $i>j$：

$$
a_{ij}
=
\sum_{k=1}^{j-1}
\ell_{ik}\overline{\ell_{jk}}
+
\ell_{ij}\overline{\ell_{jj}}.
$$

因为 $\ell_{jj}$ 取正实数，

$$
\ell_{ij}
=
\frac{
a_{ij}
-\sum_{k=1}^{j-1}
\ell_{ik}\overline{\ell_{jk}}
}
{\ell_{jj}}.
$$

算法按列或按块推进：先算当前对角元，再算它下面的元素。

~~~mermaid
flowchart LR
    A["Hermitian 正定矩阵 A"] --> P["计算当前正 Cholesky pivot"]
    P --> C["计算该列对角线下方元素"]
    C --> S["更新剩余 Schur 补"]
    S --> P
    C --> L["得到 A = LL*"]
~~~

## 为什么根号里的量为正

分块写成

$$
\boldsymbol A=
\begin{bmatrix}
\boldsymbol A_{11}&\boldsymbol a\\
\boldsymbol a^{*}&\alpha
\end{bmatrix},
\qquad
\boldsymbol A_{11}\succ0.
$$

若
$\boldsymbol A_{11}=\boldsymbol L_{11}\boldsymbol L_{11}^{*}$，
令

$$
\boldsymbol \ell
=\boldsymbol L_{11}^{-1}\boldsymbol a.
$$

剩余对角平方是 Schur 补

$$
s
=\alpha-\boldsymbol a^{*}\boldsymbol A_{11}^{-1}\boldsymbol a.
$$

取向量

$$
\boldsymbol z=
\begin{bmatrix}
-\boldsymbol A_{11}^{-1}\boldsymbol a\\
1
\end{bmatrix},
$$

正定性给出

$$
0<
\boldsymbol z^{*}\boldsymbol A\boldsymbol z
=
\alpha-\boldsymbol a^{*}\boldsymbol A_{11}^{-1}\boldsymbol a
=s.
$$

所以每一步剩余 pivot 都严格为正，可以开平方且不会除以零。这也是 Cholesky 失败可作为“矩阵不是数值正定”的诊断信号之一。

## 唯一性为什么成立

假设

$$
\boldsymbol A
=\boldsymbol L_1\boldsymbol L_1^{*}
=\boldsymbol L_2\boldsymbol L_2^{*},
$$

两者都下三角且正对角。令

$$
\boldsymbol U
=\boldsymbol L_2^{-1}\boldsymbol L_1.
$$

在原等式左右分别乘 $\boldsymbol L_2^{-1}$ 和
$\boldsymbol L_2^{-*}$，得到

$$
\boldsymbol U\boldsymbol U^{*}=\boldsymbol I.
$$

$\boldsymbol U$ 是下三角矩阵，又由上式可知它是酉矩阵。酉矩阵的列标准正交：最后一列只有最后一个坐标可能非零，归一化迫使其模长为 1；它与前面各列正交，又迫使最后一行的其余元素为 0。逐阶向左上角重复，得到 $\boldsymbol U$ 必须是对角矩阵。

因为 $\boldsymbol L_1,\boldsymbol L_2$ 的对角元素都为正，$\boldsymbol U$ 的对角元素也为正；酉性再迫使它们全为 1。因此

$$
\boldsymbol U=\boldsymbol I,
\qquad
\boldsymbol L_1=\boldsymbol L_2.
$$

对初学者也可从递推公式直接看：第一列每个元素被唯一确定；减去第一列贡献后，剩余子问题继续唯一。

## 用 Cholesky 解线性方程

要解

$$
\boldsymbol A\boldsymbol x=\boldsymbol b,
\qquad
\boldsymbol A=\boldsymbol L\boldsymbol L^{*},
$$

不计算 $\boldsymbol A^{-1}$。分两步：

1. 前向代入：
   $$
   \boldsymbol L\boldsymbol y=\boldsymbol b;
   $$
2. 后向代入：
   $$
   \boldsymbol L^{*}\boldsymbol x=\boldsymbol y.
   $$

每个三角求解需要 $O(n^2)$；分解约需
$n^3/3$ 量级运算，比一般 LU 利用对称性节省常数和存储。

## 手算求解

使用

$$
\boldsymbol A=
\begin{bmatrix}4&2\\2&3\end{bmatrix},
\quad
\boldsymbol L=
\begin{bmatrix}2&0\\1&\sqrt2\end{bmatrix},
\quad
\boldsymbol b=
\begin{bmatrix}2\\3\end{bmatrix}.
$$

先解

$$
\begin{bmatrix}2&0\\1&\sqrt2\end{bmatrix}
\begin{bmatrix}y_1\\y_2\end{bmatrix}
=
\begin{bmatrix}2\\3\end{bmatrix}.
$$

得到

$$
y_1=1,
\qquad
1+\sqrt2y_2=3
\Longrightarrow
y_2=\sqrt2.
$$

再解

$$
\begin{bmatrix}2&1\\0&\sqrt2\end{bmatrix}
\begin{bmatrix}x_1\\x_2\end{bmatrix}
=
\begin{bmatrix}1\\\sqrt2\end{bmatrix}.
$$

得到

$$
x_2=1,
\qquad
2x_1+1=1
\Longrightarrow
x_1=0.
$$

代回：

$$
\boldsymbol A
\begin{bmatrix}0\\1\end{bmatrix}
=
\begin{bmatrix}2\\3\end{bmatrix}
=\boldsymbol b.
$$

## 与 QR 的关系

若
$\boldsymbol B\in\mathbb F^{m\times n}$ 满列秩且

$$
\boldsymbol B=\boldsymbol Q\boldsymbol R,
$$

则

$$
\boldsymbol B^{*}\boldsymbol B
=
\boldsymbol R^{*}\boldsymbol Q^{*}\boldsymbol Q\boldsymbol R
=
\boldsymbol R^{*}\boldsymbol R.
$$

所以 $\boldsymbol R$ 是
$\boldsymbol B^{*}\boldsymbol B$ 的上三角 Cholesky 因子。

但数值上不应为了求 QR 而先形成
$\boldsymbol B^{*}\boldsymbol B$：这会平方条件数。代数恒等式与稳定计算路线必须区分。

## 行列式与 log-determinant

因为三角矩阵行列式是对角元素乘积，

$$
\det(\boldsymbol A)
=
\det(\boldsymbol L)\det(\boldsymbol L^{*})
=
\prod_{i=1}^{n}\ell_{ii}^2.
$$

因此

$$
\log\det(\boldsymbol A)
=2\sum_{i=1}^{n}\log\ell_{ii}.
$$

实际计算优先求对数和，而不是先乘出可能上溢/下溢的巨大或极小行列式。

## 高斯采样与白化

若
$\boldsymbol z\sim\mathcal N(\boldsymbol0,\boldsymbol I)$，
定义

$$
\boldsymbol x=\boldsymbol\mu+\boldsymbol L\boldsymbol z,
$$

则

$$
\operatorname{Cov}(\boldsymbol x)
=
\boldsymbol L\boldsymbol I\boldsymbol L^{\top}
=\boldsymbol A.
$$

反过来，解

$$
\boldsymbol L\boldsymbol z
=\boldsymbol x-\boldsymbol\mu
$$

可把相关高斯变量转到单位协方差坐标。实现时使用三角求解，不计算
$\boldsymbol L^{-1}$。

## 半正定和近奇异边界

若 $\boldsymbol A\succeq0$ 但不正定，某个 pivot 可能为 0：

$$
\boldsymbol A=
\begin{bmatrix}1&1\\1&1\end{bmatrix}
$$

只有秩 1。第一步给 $\ell_{11}=1,\ell_{21}=1$，第二步

$$
\ell_{22}=\sqrt{1-1}=0.
$$

标准“正对角、可逆”Cholesky 条件失效。可根据任务使用：

- pivoted Cholesky；
- 低秩因子；
- LDL$^{*}$ 分解；
- 加阻尼 $\boldsymbol A+\varepsilon\boldsymbol I$。

但阻尼改变了矩阵的谱和原问题，必须记录 $\varepsilon$。

## 数值边界

- 输入应先按 Hermitian/对称结构处理；舍入导致的微小不对称需判断来源，不能盲目只取一半。
- 非常小的 Cholesky pivot 表示接近奇异边界，后续除法会放大误差。
- 数学上正定的矩阵在低精度下可能因为舍入被判断失败；这需要结合尺度、条件数和后向误差分析。
- 不定矩阵不能使用标准 Cholesky；应考虑带主元 LDL$^{*}$ 等方法。

[[实验 - 正定边界、条件数与 Cholesky pivot]]给出 $2\times2$ 解析例子，展示分解真正失败之前，接近零的 pivot 已怎样连续预警病态性。

## 在 AI 中的连接

- **高斯过程与贝叶斯模型**：协方差求解和 log-determinant 是核心成本。
- **多元高斯与 VAE**：Cholesky 参数化保证协方差正定，并用于重参数化采样。
- **白化与 Normalization**：三角因子提供一种坐标变换；批量估计噪声通常需要阻尼。
- **二阶优化**：正定近似系统可用 Cholesky 求解；大规模时则需迭代法和预条件。
- **Shampoo/矩阵优化器**：二阶矩阵正则化后的逆平方根与正定分解密切相关。
- **最小二乘**：正规矩阵的 Cholesky 求解速度快，但会继承平方条件数问题。

## 边界与常见误区

1. Cholesky 不是对任意方阵都存在；标准版本要求 Hermitian 正定。
2. $LL^{*}$ 中的共轭转置不能在复数情形写成普通转置。
3. 不要显式构造 $L^{-1}$ 或 $A^{-1}$ 来解方程。
4. PSD 与 PD 不同；零 pivot 对应真实或数值秩亏。
5. 加 jitter 能改善计算，但会改变统计模型和优化几何。
6. $A=B^{*}B$ 的代数形式不代表形成 $B^{*}B$ 是稳定算法。

## 本节回顾

- Cholesky 是正定矩阵的唯一正对角三角平方根。
- 递推中的正 pivot 来自正定性和 Schur 补。
- 解 $Ax=b$ 时做两次三角求解，不计算逆矩阵。
- log-det、相关高斯采样和白化可直接读取 Cholesky 因子。
- 近零 pivot 是条件性和数值秩风险，不应被静默忽略。

## 练习

- [[习题 - Cholesky 分解]]
- [[解答 - Cholesky 分解]]

## 来源

- Sheldon Axler, [Linear Algebra Done Right, 4th ed.](https://linear.axler.net/LADR4e.pdf), Section 7D。
- Gene H. Golub & Charles F. Van Loan, *Matrix Computations*, 4th ed., Chapter 4。
- [MIT 18.335：Cholesky Factorization and Specialized Solvers](https://ocw.mit.edu/courses/18-335j-introduction-to-numerical-methods-spring-2019/pages/resource-index/)。
