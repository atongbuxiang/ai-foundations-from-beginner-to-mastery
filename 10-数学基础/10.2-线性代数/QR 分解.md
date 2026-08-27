---
type: concept
status: draft
area: [math/linear-algebra, math/numerical-linear-algebra]
aliases: [QR Factorization, QR Decomposition]
prerequisites: ["[[标准正交基与 Gram-Schmidt]]", "[[线性映射]]"]
related: ["[[最小二乘]]", "[[Cholesky 分解]]", "[[极分解]]", "[[Householder 与 Givens 变换]]", "[[实验 - Gram-Schmidt 与 QR 的正交性误差]]", "[[线性代数 MOC]]"]
sources: ["Axler-LADR4e-7D", "MIT-18.06-L17", "MIT-18.335-L9-L10"]
exercises: ["[[习题 - QR 分解]]"]
solutions: ["[[解答 - QR 分解]]"]
created: 2026-08-14
updated: 2026-08-27
---

# QR 分解

> [!abstract] 本章主问题
> 怎样在保持矩阵列空间不变的同时，把倾斜列改写成标准正交方向，并把剩余计算压缩为上三角系统？QR 分解写成 $A=QR$：$Q$ 提供列空间的标准正交基，$R$ 记录原列在该基中的逐列坐标。它连接 Gram–Schmidt、稳定最小二乘、子空间迭代和 QR 特征值算法，但“存在一种 QR”与“选哪种数值算法”是两层问题。

> [!info] 学习目标
> 学完本章后，应能区分薄 QR、完整 QR 与带列主元 QR；证明满列秩薄 QR 的存在性和适当符号约定下的唯一性；从 Gram–Schmidt 系数读出上三角 $R$；用 $Q^*A=R$ 和 $Q^*Q=I$ 验收分解；通过 $Rx=Q^*b$ 求解满列秩最小二乘；比较 MGS、Householder 与 Givens 的稳定性、成本和存储方式。

> [!question] 初学者读完必须能回答
> 1. 薄 QR 与完整 QR 的 $Q,R$ 形状分别是什么？
> 2. 为什么 $Q$ 与 $A$ 张成相同列空间？
> 3. $R$ 为什么是上三角，而不是一般稠密矩阵？
> 4. 为什么 $Q^*Q=I$ 不意味着薄 $Q$ 还满足 $QQ^*=I_m$？
> 5. QR 怎样把最小二乘化成上三角求解？
> 6. CGS/MGS、Householder 与 Givens 在精确结构相同的同时，为何数值表现不同？
> 7. 秩亏时为什么需要 QRCP、SVD 或显式秩判定？

![[00-知识库管理/_assets/figures/qr-factorization/fig-qr-columns-triangular-algorithms-v2.svg|880]]

> [!figure] 图 1　列空间几何、上三角坐标与算法路线
> 左栏展示 $A$ 的非正交列，中栏用标准正交列 $Q$ 表示同一列空间，右栏用上三角 $R$ 保存逐列坐标；底栏比较 MGS、Householder、Givens 与最小二乘接口。**来源：**依据 Gram–Schmidt 系数结构和薄 QR 定义独立绘制。

**怎样读图。** 先只比较左、中两栏：列向量改变了，但 span 不变；$Q^*Q=I$ 让坐标分析稳定而简单。再看 $R$ 的零下三角，因为第 $j$ 个原列只使用前 $j$ 个已构造方向。最后看底栏，Householder 通常是稠密 QR 主线，Givens 适合局部消元，MGS 适合教学、增量与某些迭代场景。

**适用边界（图没有证明什么）。** 图默认 $m\ge n$ 且满列秩的薄 QR；秩亏、宽矩阵和带主元分解需要额外声明形状与置换。实际实现常只保存 Householder 向量而不显式形成 $Q$，所以公式中的矩阵对象与程序中的存储结构不能直接等同。

## 进入正文前：QR 把“子空间几何”与“坐标求解”分开

> [!info] 承接—中心—去路
> - **承接：** [[标准正交基与 Gram-Schmidt]]已经构造与 $A$ 同列空间的 $Q$；[[正交投影]]说明 $Q^*b$ 是目标在这些方向上的分析坐标。
> - **中心：** 本页把每个原列在逐步正交基下的坐标收集为上三角 $R$，得到 $A=QR$。$Q$ 负责几何，$R$ 负责坐标与可解的三角系统。
> - **去路：** [[最小二乘]]会把 $\min_x\|Ax-b\|$ 化成 $Rx=Q^*b$；Schur 与 QR 算法则会把正交变换继续用于谱计算。

### 两遍阅读路线

第一次读薄 QR 的形状、上三角来源、手算分解和最小二乘接口。第二次再读完整 QR、唯一性、Householder/Givens/MGS 的算法差异、列主元与秩亏边界。

全章主线是：

$$
A\text{ 的倾斜列}
\to Q\text{ 的标准正交列}
\to R=Q^*A
\to A=QR
\to Rx=Q^*b.
$$

### 本章的问题链

1. 薄 QR 与完整 QR 分别保存多少个方向，形状如何核对？
2. 为什么 $Q$ 与 $A$ 的列空间相同？
3. 第 $j$ 个原列只依赖前 $j$ 个 $q_i$，为何使 $R$ 上三角？
4. $Q^*Q=I$ 为什么让 $R=Q^*A$，却不推出 $QQ^*=I$？
5. 正对角线约定怎样消除符号或复相位自由度？
6. QR 如何把大空间中的最近点问题压缩成小型三角求解？
7. 数学上同为 QR 的 MGS、Householder 与 Givens 为什么有不同稳定性和适用场景？

### 贯穿例的完整 QR

前页已经得到

$$
Q=
\begin{bmatrix}
1/\sqrt2&1/\sqrt6\\
1/\sqrt2&-1/\sqrt6\\
0&2/\sqrt6
\end{bmatrix}.
$$

由 $R=Q^TA$，

$$
R=
\begin{bmatrix}
\sqrt2&1/\sqrt2\\
0&\sqrt{3/2}
\end{bmatrix},
\qquad A=QR.
$$

对 $b=e_3$，

$$
Q^Tb=
\begin{bmatrix}
0\\2/\sqrt6
\end{bmatrix}.
$$

因此最小二乘参数只需解上三角系统

$$
Rx=Q^Tb,
$$

而不必形成 $A^TA$。下一页会解得 $\hat x=(-1/3,2/3)^\top$，并检查 $A\hat x=QQ^Tb$。

### 最小分解账本

| 对象 | 形状 | 角色 |
|---|---|---|
| $A$ | $m\times n$ | 原始列与待分析线性映射 |
| $Q$ | $m\times n$（薄） | 列空间的标准正交基，$Q^*Q=I_n$ |
| $R$ | $n\times n$ | 原列在 $Q$ 下的上三角坐标 |
| $Q^*A=R$ | identity | 分析原列坐标 |
| $QR=A$ | reconstruction | 验收不能只看这一条，还要检查正交性 |
| $Q^*b$ | $n$ 维坐标 | 目标在列空间方向上的坐标 |

> [!tip] 初学者的停靠点
> 若只知道调用 `qr(A)`，却不能解释为什么 $R$ 上三角或薄 $Q$ 为什么没有 $QQ^*=I_m$，先停在“薄 QR”与“Gram–Schmidt 为什么产生上三角矩阵”。

## 阅读前检查

- [[标准正交基与 Gram-Schmidt]]：怎样逐列构造标准正交方向；
- [[线性映射]]：矩阵列是标准基向量的像；
- [[最小二乘]]不是本章前置；第一次阅读只需接受后文会用 QR 处理 $\|\boldsymbol A\boldsymbol x-\boldsymbol b\|_2$ 最小化问题，完整几何可在学完本章后再读。

需要的矩阵乘法形状：

$$
\boldsymbol A\in\mathbb F^{m\times n},
\quad
\boldsymbol Q\in\mathbb F^{m\times n},
\quad
\boldsymbol R\in\mathbb F^{n\times n},
$$

所以 $\boldsymbol Q\boldsymbol R$ 是 $m\times n$。

## 先看一个具体问题

设 $\boldsymbol A$ 有两列：

$$
\boldsymbol A=
\begin{bmatrix}
1&1\\
1&0\\
0&1
\end{bmatrix}
=
\begin{bmatrix}
\boldsymbol a_1&\boldsymbol a_2
\end{bmatrix}.
$$

列向量线性无关，但不正交。我们希望：

1. 用标准正交列 $\boldsymbol q_1,\boldsymbol q_2$ 表示同一个列空间；
2. 记录原列在新基下的坐标；
3. 利用正交性简化最小二乘。

这正对应

$$
\boldsymbol A=\boldsymbol Q\boldsymbol R.
$$

## 薄 QR 与完整 QR

> [!definition] 薄 QR
> 设 $m\ge n$，且
> $\boldsymbol A\in\mathbb F^{m\times n}$ 满列秩。薄 QR 分解是
> $$
> \boldsymbol A=\boldsymbol Q\boldsymbol R,
> $$
> 其中
> $$
> \boldsymbol Q\in\mathbb F^{m\times n},
> \qquad
> \boldsymbol Q^{*}\boldsymbol Q=\boldsymbol I_n,
> $$
> 且
> $$
> \boldsymbol R\in\mathbb F^{n\times n}
> $$
> 是可逆上三角矩阵。

> [!analysis] 薄 QR 定义的七问拆解
> | 问题 | 回答 |
> |---|---|
> | 为什么要求 $m\ge n$ 且满列秩？ | 才可能在 $\mathbb F^m$ 中容纳 $n$ 个标准正交列，并让方形 $R$ 可逆。 |
> | $Q$ 保留什么？ | 保留 $A$ 的列空间几何，但更换为标准正交基。 |
> | $R$ 保留什么？ | 保留原列相对于 $Q$ 的坐标与尺度，正对角约定还消除符号/相位自由度。 |
> | 为什么 $R$ 上三角？ | 第 $j$ 个原列在逐步构造中只使用 $q_1,\ldots,q_j$。 |
> | 怎样验收？ | 同时检查 $\|A-QR\|$、$\|I-Q^*Q\|$、三角结构与对角尺度。 |
> | 定义没有指定什么？ | 没有指定使用 CGS、MGS、Householder 还是 Givens，也没有指定显式形成 $Q$。 |
> | AI/数值接口是什么？ | 最小二乘、子空间正交化、低秩因子规范化和迭代谱算法。 |

“薄”表示只保留 $\mathcal R(\boldsymbol A)$ 所需的 $n$ 个标准正交方向。

完整 QR 把 $\boldsymbol Q$ 补成
$m\times m$ 酉矩阵：

$$
\boldsymbol A
=
\begin{bmatrix}
\boldsymbol Q_1&\boldsymbol Q_2
\end{bmatrix}
\begin{bmatrix}
\boldsymbol R\\
\boldsymbol0
\end{bmatrix}.
$$

$\boldsymbol Q_1$ 张成列空间，
$\boldsymbol Q_2$ 张成左零空间
$\mathcal N(\boldsymbol A^{*})$。

## Gram–Schmidt 为什么产生上三角矩阵

在第 $j$ 步，

$$
\boldsymbol a_j
=
r_{1j}\boldsymbol q_1+\cdots+
r_{j-1,j}\boldsymbol q_{j-1}
+r_{jj}\boldsymbol q_j.
$$

不会出现 $\boldsymbol q_{j+1},\ldots,\boldsymbol q_n$，
因为它们还没有被构造。把所有列并排：

$$
\begin{bmatrix}
\boldsymbol a_1&\cdots&\boldsymbol a_n
\end{bmatrix}
=
\begin{bmatrix}
\boldsymbol q_1&\cdots&\boldsymbol q_n
\end{bmatrix}
\begin{bmatrix}
r_{11}&r_{12}&\cdots&r_{1n}\\
0&r_{22}&\cdots&r_{2n}\\
\vdots&\ddots&\ddots&\vdots\\
0&\cdots&0&r_{nn}
\end{bmatrix}.
$$

因此 $\boldsymbol R$ 必然上三角，而且

$$
r_{ij}=\boldsymbol q_i^{*}\boldsymbol a_j
\quad(i\le j),
\qquad
r_{jj}>0.
$$

左乘 $\boldsymbol Q^{*}$：

$$
\boldsymbol Q^{*}\boldsymbol A
=\boldsymbol Q^{*}\boldsymbol Q\boldsymbol R
=\boldsymbol R.
$$

所以 $\boldsymbol R$ 就是原矩阵各列在标准正交列基中的坐标。

~~~mermaid
flowchart LR
    A["A：原始列"] --> Q["Q：同一列空间的标准正交基"]
    A --> R["R：原始列在 Q 中的坐标"]
    Q --> QR["A = QR"]
    R --> QR
    QR --> LS["把最小二乘化为三角方程"]
~~~

## 存在性与唯一性

### 存在性

满列秩意味着矩阵列线性无关。对它们执行 Gram–Schmidt：

- 每一步残差非零；
- 归一化后得到标准正交列；
- 系数自然组成上三角 $\boldsymbol R$。

因此薄 QR 存在。

### 为什么需要规定正对角线

若

$$
\boldsymbol A=\boldsymbol Q\boldsymbol R,
$$

则把 $\boldsymbol Q$ 的某一列乘 $-1$，同时把 $\boldsymbol R$ 对应行乘 $-1$，乘积不变。复数中还可乘单位相位。

规定

$$
r_{jj}>0
$$

消除这种自由度。对满列秩实/复矩阵，正对角线的薄 QR 唯一。

## 手算例子

沿用

$$
\boldsymbol A=
\begin{bmatrix}
1&1\\
1&0\\
0&1
\end{bmatrix}.
$$

由[[标准正交基与 Gram-Schmidt]]的手算：

$$
\boldsymbol q_1
=\frac1{\sqrt2}
\begin{bmatrix}1\\1\\0\end{bmatrix},
\qquad
\boldsymbol q_2
=\frac1{\sqrt6}
\begin{bmatrix}1\\-1\\2\end{bmatrix}.
$$

因此

$$
\boldsymbol Q=
\begin{bmatrix}
1/\sqrt2&1/\sqrt6\\
1/\sqrt2&-1/\sqrt6\\
0&2/\sqrt6
\end{bmatrix}.
$$

各坐标为

$$
r_{11}=\sqrt2,
\qquad
r_{12}=\frac1{\sqrt2},
\qquad
r_{22}=\frac{\sqrt6}{2}.
$$

所以

$$
\boldsymbol R=
\begin{bmatrix}
\sqrt2&1/\sqrt2\\
0&\sqrt6/2
\end{bmatrix}.
$$

验证第二列：

$$
\begin{aligned}
r_{12}\boldsymbol q_1+r_{22}\boldsymbol q_2
&=
\frac12
\begin{bmatrix}1\\1\\0\end{bmatrix}
+
\frac12
\begin{bmatrix}1\\-1\\2\end{bmatrix}\\
&=
\begin{bmatrix}1\\0\\1\end{bmatrix}
=\boldsymbol a_2.
\end{aligned}
$$

## 用 QR 解最小二乘

考虑

$$
\min_{\boldsymbol x}
\|\boldsymbol A\boldsymbol x-\boldsymbol b\|_2,
\qquad
\boldsymbol A=\boldsymbol Q\boldsymbol R.
$$

把 $\boldsymbol Q$ 补成完整酉矩阵
$[\boldsymbol Q\ \boldsymbol Q_{\perp}]$。
酉变换保持二范数：

$$
\begin{aligned}
\|\boldsymbol A\boldsymbol x-\boldsymbol b\|_2^2
&=
\left\|
\begin{bmatrix}
\boldsymbol Q^{*}\\
\boldsymbol Q_{\perp}^{*}
\end{bmatrix}
(\boldsymbol Q\boldsymbol R\boldsymbol x-\boldsymbol b)
\right\|_2^2\\
&=
\|\boldsymbol R\boldsymbol x-\boldsymbol Q^{*}\boldsymbol b\|_2^2
+
\|\boldsymbol Q_{\perp}^{*}\boldsymbol b\|_2^2.
\end{aligned}
$$

第二项与 $\boldsymbol x$ 无关，所以最优解满足

$$
\boldsymbol R\widehat{\boldsymbol x}
=\boldsymbol Q^{*}\boldsymbol b.
$$

因为 $\boldsymbol R$ 可逆上三角，只需回代，不需要形成
$\boldsymbol A^{*}\boldsymbol A$，也不需要显式求逆。

### 继续手算

取

$$
\boldsymbol b=(1,2,0)^{\top}.
$$

先算

$$
\boldsymbol Q^{\top}\boldsymbol b
=
\begin{bmatrix}
3/\sqrt2\\
-1/\sqrt6
\end{bmatrix}.
$$

解三角方程：

$$
\frac{\sqrt6}{2}x_2=-\frac1{\sqrt6}
\quad\Longrightarrow\quad
x_2=-\frac13.
$$

第一行：

$$
\sqrt2x_1+\frac1{\sqrt2}\left(-\frac13\right)
=\frac3{\sqrt2}.
$$

两边乘 $\sqrt2$：

$$
2x_1-\frac13=3
\quad\Longrightarrow\quad
x_1=\frac53.
$$

预测与残差：

$$
\boldsymbol A\widehat{\boldsymbol x}
=
\begin{bmatrix}4/3\\5/3\\-1/3\end{bmatrix},
\qquad
\boldsymbol r
=\boldsymbol b-\boldsymbol A\widehat{\boldsymbol x}
=\frac13
\begin{bmatrix}-1\\1\\1\end{bmatrix}.
$$

验证
$\boldsymbol A^{\top}\boldsymbol r=\boldsymbol0$，
说明残差与列空间正交。

## 与 $\boldsymbol A^{*}\boldsymbol A$ 和 Cholesky 的关系

若 $\boldsymbol A=\boldsymbol Q\boldsymbol R$，则

$$
\boldsymbol A^{*}\boldsymbol A
=\boldsymbol R^{*}\boldsymbol Q^{*}\boldsymbol Q\boldsymbol R
=\boldsymbol R^{*}\boldsymbol R.
$$

因为满列秩时 $\boldsymbol A^{*}\boldsymbol A$ 正定，
$\boldsymbol R$ 正是它的上三角 Cholesky 因子。

这个恒等式也说明正规方程为什么会平方条件数：
$\boldsymbol A^{*}\boldsymbol A$ 的奇异/特征值是
$\sigma_i(\boldsymbol A)^2$。

## 算法与数值边界

QR 是数学分解，不等于只有一种计算方法。

| 方法 | 核心动作 | 一般数值表现 |
|---|---|---|
| Classical Gram–Schmidt | 一次减去对已有空间的投影 | 近相关列时可能明显失去正交性 |
| Modified Gram–Schmidt | 逐方向更新当前残差 | 通常比 Classical 稳定 |
| Householder QR | 依次用正交反射消去下三角元素 | 稠密矩阵的稳定默认方法 |
| Givens QR | 每次旋转两个坐标消去一个元素 | 适合稀疏/增量结构 |

对稠密 $m\times n$、$m\ge n$ 矩阵，QR 量级为
$O(mn^2)$；显式形成完整 $m\times m$ 的 $\boldsymbol Q$ 往往没有必要。

配套的[[实验 - Gram-Schmidt 与 QR 的正交性误差]]用同一个满秩病态矩阵族比较 CGS 与 MGS，并分别检查重构残差和正交性缺陷。

## 秩亏情形

若 $\boldsymbol A$ 不满列秩，朴素 Gram–Schmidt 某一步会得到零残差，
$r_{jj}=0$，$\boldsymbol R$ 不可逆。

这时需要区分目标：

- 只求列空间基：跳过相关列或使用带主元 QR；
- 求最小二乘最小范数解：使用秩揭示 QR 或 SVD；
- 判断数值秩：必须给容差和误差模型，不能只比较浮点数是否严格为零。

## 在 AI 中的连接

- **线性 probe/回归**：QR 比显式正规方程更适合作为稳定基线。
- **正交参数化**：QR 可把任意满秩矩阵映射到 Stiefel 流形上的正交列，但符号约定和反向传播需处理。
- **PCA 与子空间跟踪**：QR 用于保持迭代基的正交性。
- **Muon/极分解**：QR 产生某个正交因子，但一般不是最近正交矩阵；后者由极分解给出。
- **低秩因子**：$\boldsymbol L=\boldsymbol Q\boldsymbol R$ 可把子空间与坐标尺度分开，减少解释混淆。

## 边界与常见误区

1. $\boldsymbol Q^{*}\boldsymbol Q=\boldsymbol I$ 不意味着矩形
   $\boldsymbol Q\boldsymbol Q^{*}=\boldsymbol I$；后者是列空间投影。
2. QR 不等于特征分解；上三角 $\boldsymbol R$ 的对角线一般不是
   $\boldsymbol A$ 的特征值。
3. “用 QR 解最小二乘”不是计算
   $(\boldsymbol A^{*}\boldsymbol A)^{-1}$。
4. 数学分解的存在性不能告诉你具体实现是否后向稳定。
5. rank-deficient QR 仍可存在，但上三角因子不可逆，唯一解推导不再成立。

## 本节回顾

- QR 把列空间的几何基 $\boldsymbol Q$ 与坐标 $\boldsymbol R$ 分开。
- Gram–Schmidt 直接给出上三角结构。
- 满列秩、正对角线约定下薄 QR 唯一。
- 最小二乘化为
  $\boldsymbol R\widehat{\boldsymbol x}=\boldsymbol Q^{*}\boldsymbol b$。
- 实际计算通常优先 Householder QR；近秩亏时需带主元 QR 或 SVD。

## 练习

- [[习题 - QR 分解]]
- [[解答 - QR 分解]]

## 来源

- Sheldon Axler, [Linear Algebra Done Right, 4th ed.](https://linear.axler.net/LADR4e.pdf), Section 7D。
- [MIT 18.06：Gram–Schmidt and A = QR](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/pages/readings/)。
- [MIT 18.335：Solving least squares by QR; Modified Gram–Schmidt and Householder QR](https://ocw.mit.edu/courses/18-335j-introduction-to-numerical-methods-spring-2019/pages/week-4/)。
