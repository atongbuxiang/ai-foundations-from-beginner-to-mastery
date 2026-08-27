---
type: concept
status: draft
area: [math/linear-algebra, math/numerical-linear-algebra]
aliases: [Gaussian 消元, LU 分解, PA=LU, 高斯消元]
prerequisites: ["[[线性映射]]", "[[四个基本子空间]]"]
related: ["[[迹、行列式与体积]]", "[[Cholesky 分解]]", "[[稳定求解线性方程组]]", "[[线性代数 MOC]]"]
sources: ["MIT-18.06-L2-L5", "Strang-ILA-Ch2", "Golub-VanLoan-Ch3", "Glow-2018"]
exercises: ["[[习题 - 线性方程组、消元与 LU 分解]]"]
solutions: ["[[解答 - 线性方程组、消元与 LU 分解]]"]
created: 2026-08-15
updated: 2026-08-27
---

# 线性方程组、消元与 LU 分解

> [!abstract] 本章主问题
> 怎样把求解一个一般线性系统的工作，拆成一次可复用的分解与多次便宜的三角求解？Gaussian 消元用可逆行变换把一般方程化为上三角方程。把消元乘子保存起来，就得到
> $\boldsymbol A=\boldsymbol L\boldsymbol U$；若需要交换行，则得到
> $\boldsymbol P\boldsymbol A=\boldsymbol L\boldsymbol U$。LU 的核心不只是手算，而是让多个右端、行列式、隐式微分与许多数值算法共享同一消元结构。

> [!info] 学习目标
> 学完后应能判断 $A\boldsymbol x=\boldsymbol b$ 的相容性与解的唯一性；用消元矩阵解释行变换；手算小型 LU 并通过前代、回代求解；说明消元乘子为什么进入 $L$；判断何时必须选主元；比较分解成本与多右端复用收益；区分代数可逆性、算法可执行性和浮点稳定性。

> [!question] 初学者读完必须能回答
> 1. 三种初等行变换为什么保持方程组解集，却会改变列空间本身？
> 2. 消元矩阵怎样把主元下方元素变为零？
> 3. 为什么消元乘子以相反方向累积后进入下三角矩阵 $L$？
> 4. $PA=LU$ 后求解为什么分成 $Pb$、$Ly=Pb$、$Ux=y$ 三步？
> 5. 一个矩阵可逆，为什么仍可能不存在不换行的 LU？
> 6. 部分选主元解决什么风险，又不能解决什么病态性？
> 7. 为什么多右端问题中“分解一次、求解多次”比逐次消元更重要？

![[00-知识库管理/_assets/figures/linear-systems/fig-elimination-lu-solve-pipeline-v2.svg|880]]

> [!figure] 图 1　消元乘子、LU 因子与求解流水线
> 上半部分用一个二阶系统展示 $R_2\leftarrow R_2-2R_1$ 怎样产生 $U$，以及乘子 $2$ 怎样存入 $L$；下半部分展示一般 $PA=LU$ 的置换、前向代入和后向代入。**来源：**依据 Gaussian 消元与 LU 分解定义独立绘制。

**怎样读图。** 先在具体矩阵中追踪一个消元乘子：它负责清零主元下方元素，同时成为 $L$ 的下三角条目。再看下方的一般求解路径，$P$ 必须同时作用于右端。最后比较成本：稠密分解约为 $O(n^3)$，固定因子后的每个新右端只需两次 $O(n^2)$ 三角求解。

**适用边界（图没有证明什么）。** 图中的二阶例子无需换行，不能据此把 $A=LU$ 当作无条件公式；一般算法要写 $PA=LU$ 并采用主元策略。图也没有保证病态矩阵会因选主元而变得良态，条件数属于问题本身，后向稳定性属于算法性质。

## 进入正文前：消元把一次结构分析变成可复用求解器

> [!info] 承接—中心—去路
> - **承接：** [[四个基本子空间]]已经把相容性、唯一性与自由变量翻译成列空间和零空间；上一批的 QR 展示了另一类保持几何的分解。
> - **中心：** 本页把可逆行变换组织为 Gaussian elimination，并把消元乘子保存成 $L$、三角结果保存成 $U$；对一般矩阵还要用 $P$ 记录选主元的行交换。
> - **去路：** [[迹、行列式与体积]]会从 $U$ 的 pivots 读取 determinant；隐式微分和二阶优化会复用一次分解解决多个右端；数值计算卷会进一步研究 growth factor 与后向误差。

### 两遍阅读路线

第一次读方程语义、三类行变换、消元矩阵、$A=LU$ 与前代/回代。第二次再读 pivoting、$PA=LU$、唯一性、Schur complement、复杂度和数值稳定性边界。

全章主线是：

$$
Ax=b
\to PA=LU
\to Ly=Pb
\to Ux=y
\to \text{多右端复用}.
$$

### 本章的问题链

1. 行变换为何保持方程解集，却不保持原矩阵的列空间位置？
2. 每次消元为何等价于左乘可逆初等矩阵？
3. 消元乘子为何在取逆后以正号进入下三角 $L$？
4. 三角系统为什么可按依赖顺序前代或回代？
5. 可逆矩阵为什么仍可能需要换行才能继续消元？
6. 部分选主元控制什么算法风险，又为什么不能改善问题本身的条件数？
7. 为什么分解一次、求解多个右端是 LU 的核心工程价值？

### 从上一批的 Gram 矩阵继续

对设计矩阵 $A$，令

$$
G=A^TA=
\begin{bmatrix}2&1\\1&2\end{bmatrix},
\qquad
A^Tb=\begin{bmatrix}0\\1\end{bmatrix}.
$$

一次消元 $R_2\leftarrow R_2-\tfrac12R_1$ 给出

$$
G=LU,
\qquad
L=\begin{bmatrix}1&0\\1/2&1\end{bmatrix},
\qquad
U=\begin{bmatrix}2&1\\0&3/2\end{bmatrix}.
$$

先解

$$
Ly=A^Tb
$$

得到 $y=(0,1)^T$，再解 $U\hat x=y$，得到

$$
\hat x=(-1/3,2/3)^T,
$$

与 QR 最小二乘结果一致。本例用于连接消元与先前结论；数值上不应据此推广“先形成 $A^TA$”，因为它会平方二范数条件数。

### 最小消元账本

| 对象 | 角色 | 必须检查 |
|---|---|---|
| $E_k$ | 一步可逆行变换 | 必须同步作用于右端 |
| $P$ | 行置换矩阵 | $PA=LU$ 时先计算 $Pb$ |
| $L$ | 单位下三角乘子账本 | 前向代入 |
| $U$ | 上三角消元结果 | pivot、秩与后向代入 |
| pivot | 当前消元除数 | 零/过小需要换行或秩判断 |
| residual | $b-A\hat x$ | 小残差不自动代表小前向误差 |

> [!tip] 初学者的停靠点
> 若只会把矩阵“化上三角”，却说不出为什么要同步变换 $b$、乘子为何进入 $L$、新右端如何复用同一分解，请停在消元矩阵与 LU 求解流水线。

## 阅读前检查

本节只要求：

- [[线性映射]]：矩阵乘向量表示线性映射；
- [[四个基本子空间]]：知道 $\boldsymbol A\boldsymbol x=\boldsymbol b$ 的可解性与列空间、零空间有关；
- 会做矩阵乘法，并知道可逆矩阵不会把两个不同向量映成同一个向量。

若对行变换陌生，可以直接从下面的具体方程开始；本节会重新建立所需规则。

## 先看一个具体问题

考虑

$$
\begin{cases}
2x_1+x_2=1,\\
4x_1+3x_2=5.
\end{cases}
$$

矩阵形式为

$$
\boldsymbol A\boldsymbol x=\boldsymbol b,
\qquad
\boldsymbol A=
\begin{bmatrix}
2&1\\
4&3
\end{bmatrix},
\quad
\boldsymbol x=
\begin{bmatrix}x_1\\x_2\end{bmatrix},
\quad
\boldsymbol b=
\begin{bmatrix}1\\5\end{bmatrix}.
$$

第二个方程减去第一个方程的 2 倍：

$$
(4x_1+3x_2)-2(2x_1+x_2)=5-2.
$$

得到

$$
x_2=3.
$$

再代回第一式：

$$
2x_1+3=1
\quad\Longrightarrow\quad
x_1=-1.
$$

关键不是这个答案，而是我们把原系数矩阵变成了上三角矩阵：

$$
\begin{bmatrix}
2&1\\
4&3
\end{bmatrix}
\longrightarrow
\begin{bmatrix}
2&1\\
0&1
\end{bmatrix}.
$$

上三角系统可以从最后一个未知量开始逐层回代。这就是消元的核心。

## 线性方程组在问什么

给定

$$
\boldsymbol A\in\mathbb F^{m\times n},
\qquad
\boldsymbol x\in\mathbb F^n,
\qquad
\boldsymbol b\in\mathbb F^m,
$$

方程

$$
\boldsymbol A\boldsymbol x=\boldsymbol b
$$

是在寻找所有被线性映射 $\boldsymbol A$ 送到 $\boldsymbol b$ 的输入。

从子空间观点：

- 有解当且仅当 $\boldsymbol b\in\mathcal R(\boldsymbol A)$；
- 若有一个解 $\boldsymbol x_p$，全部解为
  $$
  \boldsymbol x=\boldsymbol x_p+\boldsymbol z,
  \qquad
  \boldsymbol z\in\mathcal N(\boldsymbol A);
  $$
- 方阵情形唯一可解，当且仅当
  $\mathcal N(\boldsymbol A)=\{\boldsymbol0\}$，也就是 $\boldsymbol A$ 可逆。

消元把这些抽象判断变成可执行过程：它揭示 pivot、自由变量、秩、矛盾行和三角求解。

## 为什么可以对方程做行变换

合法的初等行变换有三种：

1. 交换两行；
2. 把一行乘非零标量；
3. 把一行的倍数加到另一行。

每一种都对应左乘一个可逆的初等矩阵。对

$$
\boldsymbol A\boldsymbol x=\boldsymbol b
$$

左右同时左乘可逆矩阵 $\boldsymbol E$：

$$
\boldsymbol E\boldsymbol A\boldsymbol x
=
\boldsymbol E\boldsymbol b.
$$

新方程与原方程解集相同：

- 若 $\boldsymbol A\boldsymbol x=\boldsymbol b$，左右同乘 $\boldsymbol E$ 立即得
  $\boldsymbol E\boldsymbol A\boldsymbol x=\boldsymbol E\boldsymbol b$，所以每个原解都是新方程的解；
- 新方程左乘 $\boldsymbol E^{-1}$ 就恢复原方程。

> [!warning] 必须同时变换右端
> 只对 $\boldsymbol A$ 做行变换而不对 $\boldsymbol b$ 做相同操作，会得到另一个方程组。

### 一个消元矩阵

开头使用的操作是

$$
R_2\leftarrow R_2-2R_1.
$$

对应

$$
\boldsymbol E=
\begin{bmatrix}
1&0\\
-2&1
\end{bmatrix}.
$$

于是

$$
\boldsymbol E\boldsymbol A
=
\begin{bmatrix}
1&0\\
-2&1
\end{bmatrix}
\begin{bmatrix}
2&1\\
4&3
\end{bmatrix}
=
\begin{bmatrix}
2&1\\
0&1
\end{bmatrix}
=\boldsymbol U.
$$

$\boldsymbol E$ 把第一行的 2 倍从第二行中消去。

## 从消元到 LU

由

$$
\boldsymbol E\boldsymbol A=\boldsymbol U
$$

可得

$$
\boldsymbol A=\boldsymbol E^{-1}\boldsymbol U.
$$

而

$$
\boldsymbol E^{-1}
=
\begin{bmatrix}
1&0\\
2&1
\end{bmatrix}.
$$

定义

$$
\boldsymbol L=\boldsymbol E^{-1},
$$

就得到

$$
\boldsymbol A=\boldsymbol L\boldsymbol U,
$$

其中

$$
\boldsymbol L=
\begin{bmatrix}
1&0\\
2&1
\end{bmatrix},
\qquad
\boldsymbol U=
\begin{bmatrix}
2&1\\
0&1
\end{bmatrix}.
$$

$\boldsymbol L$ 中的 2 正是消元时使用的 multiplier。

> [!analysis] $A=LU$ 的七问拆解
> | 问题 | 回答 |
> |---|---|
> | 这条公式从哪里来？ | 消元先得到 $EA=U$；把全部消元操作逆转，便有 $A=E^{-1}U$，而这些逆操作按顺序汇总成单位下三角矩阵 $L$。 |
> | $L$ 与 $U$ 分别保存什么？ | $U$ 保存消元后的上三角方程，$L$ 保存各步 multiplier，也就是“怎样由新方程重建原方程”的历史。 |
> | 形状与对角约定是什么？ | 方阵情形 $L,U\in\mathbb F^{n\times n}$；常令 $L$ 的对角为 1，于是尺度自由度归入 $U$。 |
> | 为什么不能永远写 $A=LU$？ | 某一步 pivot 可能为 0 或过小；交换行后正确的一般形式是 $PA=LU$，并且置换必须同样作用在右端 $b$ 上。 |
> | 分解后怎样求解？ | 由 $PAx=LUx=Pb$，先前代解 $Ly=Pb$，再回代解 $Ux=y$；不要显式计算 $L^{-1}$ 或 $U^{-1}$。 |
> | 怎样验收而不靠肉眼？ | 检查 $\|PA-LU\|$、三角结构、$L$ 的单位对角，并把求得的 $x$ 代回原残差 $\|Ax-b\|$。 |
> | AI 与数值计算为何关心？ | 隐式层、二阶优化、Gaussian 模型和多个右端会反复解同一系数矩阵；一次 $O(n^3)$ 分解可复用为每个右端约 $O(n^2)$ 的三角求解。 |

> [!intuition] 两个三角因子的分工
> $\boldsymbol U$ 保存消元后的上三角系统；$\boldsymbol L$ 保存如何由这些新方程重新组合出原方程。消元没有丢失信息，而是把信息拆成“最终三角结构”和“消元历史”。

## 一般消元算法

设

$$
\boldsymbol A=(a_{ij})\in\mathbb F^{n\times n}.
$$

在第 $k$ 步，假设当前 pivot

$$
u_{kk}\ne0.
$$

对每个 $i>k$，定义 multiplier

$$
\ell_{ik}
=
\frac{u_{ik}}{u_{kk}}.
$$

然后执行

$$
R_i\leftarrow R_i-\ell_{ik}R_k.
$$

对尚未处理的元素，这相当于更新

$$
u_{ij}
\leftarrow
u_{ij}-\ell_{ik}u_{kj},
\qquad
i,j>k.
$$

每一步把 pivot 下方元素变为 0。完成后：

- 所有 multiplier 放进单位下三角矩阵 $\boldsymbol L$；
- 消元结果成为上三角矩阵 $\boldsymbol U$；
- 若过程中没有换行，则
  $$
  \boldsymbol A=\boldsymbol L\boldsymbol U.
  $$

~~~mermaid
flowchart LR
    A["A 与 b"] --> E["逐列选择 pivot 并消去下方元素"]
    E --> LU["保存 multiplier 得 L；剩余系数得 U"]
    LU --> F["前代 Ly = b"]
    F --> B["回代 Ux = y"]
    B --> X["得到 Ax = b 的解"]
~~~

## 三角方程为什么容易解

### 下三角前向代入

对

$$
\boldsymbol L\boldsymbol y=\boldsymbol b,
$$

第 $i$ 行为

$$
\sum_{j=1}^{i}\ell_{ij}y_j=b_i.
$$

若 $\ell_{ii}\ne0$，则

$$
y_i
=
\frac{
b_i-\sum_{j=1}^{i-1}\ell_{ij}y_j
}{
\ell_{ii}
}.
$$

右边只使用已经求出的
$y_1,\ldots,y_{i-1}$，所以从上向下计算。

### 上三角后向代入

对

$$
\boldsymbol U\boldsymbol x=\boldsymbol y,
$$

第 $i$ 行给出

$$
x_i
=
\frac{
y_i-\sum_{j=i+1}^{n}u_{ij}x_j
}{
u_{ii}
}.
$$

它只使用后面已经求出的量，所以从 $i=n$ 向 $1$ 计算。

## 完整三阶手算

取

$$
\boldsymbol A=
\begin{bmatrix}
2&1&1\\
4&-6&0\\
-2&7&2
\end{bmatrix}.
$$

### 第一列消元

第一个 pivot 是 2。multipliers 为

$$
\ell_{21}=\frac42=2,
\qquad
\ell_{31}=\frac{-2}{2}=-1.
$$

执行

$$
R_2\leftarrow R_2-2R_1,
\qquad
R_3\leftarrow R_3-(-1)R_1=R_3+R_1.
$$

得到

$$
\begin{bmatrix}
2&1&1\\
0&-8&-2\\
0&8&3
\end{bmatrix}.
$$

### 第二列消元

第二个 pivot 是 $-8$：

$$
\ell_{32}=\frac8{-8}=-1.
$$

执行

$$
R_3\leftarrow R_3-(-1)R_2=R_3+R_2,
$$

得到

$$
\boldsymbol U=
\begin{bmatrix}
2&1&1\\
0&-8&-2\\
0&0&1
\end{bmatrix}.
$$

把 multipliers 放进 $\boldsymbol L$：

$$
\boldsymbol L=
\begin{bmatrix}
1&0&0\\
2&1&0\\
-1&-1&1
\end{bmatrix}.
$$

直接相乘可以检查

$$
\boldsymbol L\boldsymbol U=\boldsymbol A.
$$

### 用同一分解求解

令

$$
\boldsymbol b=
\begin{bmatrix}
3\\-8\\10
\end{bmatrix}.
$$

先解

$$
\boldsymbol L\boldsymbol y=\boldsymbol b.
$$

逐行得到

$$
\begin{aligned}
y_1&=3,\\
2y_1+y_2&=-8
\quad\Longrightarrow\quad y_2=-14,\\
-y_1-y_2+y_3&=10
\quad\Longrightarrow\quad y_3=-1.
\end{aligned}
$$

再解

$$
\boldsymbol U\boldsymbol x=\boldsymbol y.
$$

从最后一行向上：

$$
\begin{aligned}
x_3&=-1,\\
-8x_2-2x_3&=-14
\quad\Longrightarrow\quad x_2=2,\\
2x_1+x_2+x_3&=3
\quad\Longrightarrow\quad x_1=1.
\end{aligned}
$$

因此

$$
\boldsymbol x=
\begin{bmatrix}1\\2\\-1\end{bmatrix}.
$$

代回原方程：

$$
\boldsymbol A\boldsymbol x
=
\begin{bmatrix}3\\-8\\10\end{bmatrix}
=\boldsymbol b.
$$

## 哪些矩阵可以不换行直接做 LU

> [!theorem] 无换行 LU 的存在条件
> 对方阵 $\boldsymbol A\in\mathbb F^{n\times n}$，若每个顺序主子矩阵
> $\boldsymbol A_{1:k,1:k}$ 都可逆，则消元的每个 pivot 都非零，存在
> $$
> \boldsymbol A=\boldsymbol L\boldsymbol U,
> $$
> 其中 $\boldsymbol L$ 是单位下三角，$\boldsymbol U$ 是对角非零的上三角矩阵。

这里的顺序主子矩阵是左上角 $k\times k$ 块。

为什么这些条件与 pivot 有关？用归纳法说明。假设前 $k-1$ 个 pivot
非零，因此此前的消元已经能进行。进入第 $k$ 步、但尚未用
$u_{kk}$ 消去其下方元素时，左上角块已经具有

$$
\boldsymbol A_{1:k,1:k}
=
\boldsymbol L_k\boldsymbol U_k,
$$

这里构造 $u_{kk}$ 本身不需要除以 $u_{kk}$；只有继续消去第 $k$ 列下方元素时才需要。$\boldsymbol L_k$ 是单位下三角，因而必可逆。若
$\boldsymbol A_{1:k,1:k}$ 可逆，则

$$
\boldsymbol U_k
=
\boldsymbol L_k^{-1}\boldsymbol A_{1:k,1:k}
$$

也可逆。上三角矩阵可逆当且仅当每个对角元非零，所以第 $k$ 个
pivot $u_{kk}$ 不会为 0，归纳可以继续。这一论证不需要预先使用行列式。

反过来，若每个 pivot 非零，消元可以继续并生成上述因子。

### 为什么可逆仍然不够

考虑

$$
\boldsymbol A=
\begin{bmatrix}
0&1\\
1&0
\end{bmatrix}.
$$

它可逆，因为它只是交换两个坐标；但第一个 pivot 是 0，无法计算

$$
\ell_{21}=\frac{1}{0}.
$$

问题不是方程没有唯一解，而是当前行顺序不适合直接消元。

## 选主元与 $\boldsymbol P\boldsymbol A=\boldsymbol L\boldsymbol U$

交换两行可以把非零候选移到 pivot 位置。行交换用 permutation matrix
$\boldsymbol P$ 表示。

对上面的例子，取

$$
\boldsymbol P=
\begin{bmatrix}
0&1\\
1&0
\end{bmatrix},
$$

则

$$
\boldsymbol P\boldsymbol A=\boldsymbol I.
$$

一般带行选主元的分解写为

$$
\boldsymbol P\boldsymbol A
=
\boldsymbol L\boldsymbol U.
$$

求解时不能漏掉 $\boldsymbol P$：

$$
\boldsymbol A\boldsymbol x=\boldsymbol b
\quad\Longrightarrow\quad
\boldsymbol L\boldsymbol U\boldsymbol x
=
\boldsymbol P\boldsymbol b.
$$

### 部分选主元

第 $k$ 步在当前列的第 $k$ 行及其下方，选择绝对值最大的候选作为 pivot，再交换到第 $k$ 行。这称为 partial pivoting。

它有两个目的：

1. 避免除以 0；
2. 避免除以很小的数，减轻 multiplier 和舍入误差的放大。

> [!warning] 选主元不是形式细节
> 一个数学上可逆的矩阵仍可能因为极小 pivot 让无主元消元产生巨大中间量。部分选主元在实践中通常可靠，但仍存在最坏情形的元素增长；完整稳定性需要[[浮点数与舍入误差]]和[[前向误差与后向误差]]的语言。

## 唯一性

> [!theorem] 规范化 LU 的唯一性
> 若
> $$
> \boldsymbol A
> =\boldsymbol L_1\boldsymbol U_1
> =\boldsymbol L_2\boldsymbol U_2,
> $$
> 其中 $\boldsymbol L_1,\boldsymbol L_2$ 都是单位下三角，
> $\boldsymbol U_1,\boldsymbol U_2$ 都是可逆上三角，则两个分解相同。

证明：整理得到

$$
\boldsymbol L_2^{-1}\boldsymbol L_1
=
\boldsymbol U_2\boldsymbol U_1^{-1}.
$$

左边是单位下三角，右边是上三角。一个矩阵若同时是单位下三角和上三角，只能是单位阵。因此

$$
\boldsymbol L_2^{-1}\boldsymbol L_1=\boldsymbol I,
\qquad
\boldsymbol U_2\boldsymbol U_1^{-1}=\boldsymbol I,
$$

从而

$$
\boldsymbol L_1=\boldsymbol L_2,
\qquad
\boldsymbol U_1=\boldsymbol U_2.
$$

规定 $\boldsymbol L$ 的对角线为 1 是必要的；否则可在两个因子之间任意移动非零对角缩放。

## 分块消元与 Schur 补

把矩阵分块：

$$
\boldsymbol A=
\begin{bmatrix}
\boldsymbol A_{11}&\boldsymbol A_{12}\\
\boldsymbol A_{21}&\boldsymbol A_{22}
\end{bmatrix},
$$

并假设 $\boldsymbol A_{11}$ 可逆。则

$$
\boldsymbol A
=
\begin{bmatrix}
\boldsymbol I&\boldsymbol0\\
\boldsymbol A_{21}\boldsymbol A_{11}^{-1}&\boldsymbol I
\end{bmatrix}
\begin{bmatrix}
\boldsymbol A_{11}&\boldsymbol A_{12}\\
\boldsymbol0&
\boldsymbol A_{22}
-\boldsymbol A_{21}\boldsymbol A_{11}^{-1}\boldsymbol A_{12}
\end{bmatrix}.
$$

右下角

$$
\boldsymbol S
=
\boldsymbol A_{22}
-\boldsymbol A_{21}\boldsymbol A_{11}^{-1}\boldsymbol A_{12}
$$

称为 Schur complement。它就是“消去第一组变量后剩余系统的有效系数矩阵”。

实际程序不会显式形成
$\boldsymbol A_{11}^{-1}$，而是通过解

$$
\boldsymbol A_{11}\boldsymbol X=\boldsymbol A_{12}
$$

获得同一作用。分块公式中的逆表示数学关系，不等于推荐实现。

## 计算成本与多右端复用

对稠密 $n\times n$ 矩阵：

- LU 分解约需 $\frac23n^3$ 量级浮点运算；
- 一次前代加回代约需 $2n^2$ 量级运算；
- 若同一 $\boldsymbol A$ 对应多个右端
  $\boldsymbol b_1,\ldots,\boldsymbol b_s$，只需分解一次，再重复三角求解。

这正是“先分解、再求解”优于对每个右端重新消元的原因。

稀疏矩阵还要考虑 fill-in：原本为 0 的位置可能在 $\boldsymbol L,\boldsymbol U$ 中变成非零。此时重排序策略既服务于稳定性，也服务于内存与计算量。

## 数学公式与数值算法的边界

| 问题 | 数学层结论 | 数值层还要检查 |
|---|---|---|
| 是否唯一可解 | $\boldsymbol A$ 可逆 | 条件数是否巨大 |
| LU 是否存在 | 合适 pivot 顺序下可分解 | 是否需要选主元、元素增长多大 |
| 残差是否小 | $\|\boldsymbol b-\boldsymbol A\widehat{\boldsymbol x}\|$ | 小残差是否对应小前向误差 |
| 是否求逆 | $\boldsymbol x=\boldsymbol A^{-1}\boldsymbol b$ | 实现应使用 solve，而非显式 inverse |
| 是否利用结构 | 一般 LU 可用 | SPD 用 Cholesky，最小二乘常用 QR/SVD |

算法选择必须利用矩阵结构：

- Hermitian 正定系统优先考虑[[Cholesky 分解]]；
- 一般稠密方阵使用带主元 LU；
- 超定最小二乘优先 QR，严重病态或秩亏时考虑 SVD；
- 大规模稀疏系统常使用迭代法与预条件。

## 在 AI 中的连接

### 隐式层和隐式微分

设某个模型中

$$
\boldsymbol A(\boldsymbol\theta)\boldsymbol x
=
\boldsymbol b(\boldsymbol\theta),
\qquad
\boldsymbol A\in\mathbb R^{n\times n}.
$$

对参数做微分：

$$
(\mathrm d\boldsymbol A)\boldsymbol x
+\boldsymbol A\,\mathrm d\boldsymbol x
=
\mathrm d\boldsymbol b.
$$

整理：

$$
\boldsymbol A\,\mathrm d\boldsymbol x
=
\mathrm d\boldsymbol b
-(\mathrm d\boldsymbol A)\boldsymbol x.
$$

因此求 $\mathrm d\boldsymbol x$ 本质上又是解一个以
$\boldsymbol A$ 为系数的线性系统。反向传播可通过伴随系统复用分解，而不应显式形成
$\boldsymbol A^{-1}$。

### 可逆流与 LU 参数化

若一个可逆线性层

$$
\boldsymbol y=\boldsymbol W\boldsymbol x,
\qquad
\boldsymbol W\in\mathbb R^{d\times d},
$$

使用置换和 LU 参数化，则可逆性主要由 $\boldsymbol U$ 的非零对角控制，log-determinant 可以由三角对角线高效计算。这是 normalizing flow 中把一般可逆变换和可计算 Jacobian determinant 连接起来的一种方式。

### 二阶与预条件系统

Newton、Gauss–Newton、K-FAC 类方法会产生

$$
\boldsymbol H\boldsymbol p=-\boldsymbol g
$$

或分块近似系统。小规模稠密块可以直接分解；大规模情形通常只能做矩阵—向量乘积和迭代求解。LU 提供直接法基线，也帮助理解 Schur 补、块消元与预条件。

## 前沿地位与研究边界

- Gaussian 消元、LU 存在性和三角求解是经典定理；
- 部分选主元是成熟数值方法，但实践可靠不等于不存在最坏增长例子；
- 稀疏重排序、通信规避 LU、低精度分解加 iterative refinement 属于更深入的数值算法；
- 在 AI 中，瓶颈常不是算术次数，而是批处理、GPU 通信、稀疏结构和反向传播内存；
- “模型中出现逆矩阵公式”不意味着实现应显式求逆，这一点在自动微分系统中仍然成立。

## 边界与常见误区

1. 行变换保持方程解集，但通常不保持列空间本身。
2. $\boldsymbol A$ 可逆不保证当前顺序下无主元 LU 能直接进行。
3. 有小 residual 不一定有小 solution error；病态矩阵会放大误差。
4. $\boldsymbol P\boldsymbol A=\boldsymbol L\boldsymbol U$ 中不能在求解时漏乘 $\boldsymbol P\boldsymbol b$。
5. 不要通过显式 $\boldsymbol A^{-1}$ 来实现一次线性求解。
6. 一般 LU 不利用正定结构；能用 Cholesky 时不应无理由退回通用分解。
7. 稀疏矩阵的因子可能产生 fill-in，非零元素数而不只是 $n$ 决定真实成本。

## 本节回顾

- 消元通过可逆行变换把系统化成上三角形式。
- multiplier 收集成单位下三角 $\boldsymbol L$，消元结果形成 $\boldsymbol U$。
- 求解分成前代和回代，不需要显式求逆。
- 零或过小 pivot 需要换行；一般写成
  $\boldsymbol P\boldsymbol A=\boldsymbol L\boldsymbol U$。
- 可逆性、条件数、pivot 选择和算法稳定性是不同层次的问题。
- LU 在隐式微分、可逆流、二阶方法和多右端求解中直接出现。

## 练习

- [[习题 - 线性方程组、消元与 LU 分解]]
- [[解答 - 线性方程组、消元与 LU 分解]]

## 来源

- [MIT 18.06：Elimination、LU/LDU、permutations 与 $PA=LU$ 的课程顺序](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/pages/readings/)。
- [MIT 18.06 Lecture 2：Elimination with matrices](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-2-elimination-with-matrices/)。
- Gilbert Strang, *Introduction to Linear Algebra*, Chapter 2。
- Gene H. Golub & Charles F. Van Loan, *Matrix Computations*, 4th ed., Chapter 3。
- Diederik P. Kingma & Prafulla Dhariwal, [*Glow: Generative Flow with Invertible $1\times1$ Convolutions*](https://arxiv.org/abs/1807.03039), 2018：原文附录给出了可逆卷积权重的 LU 参数化与高效 log-determinant。
