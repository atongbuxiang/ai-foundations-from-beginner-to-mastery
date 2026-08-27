---
type: solution
status: draft
area: [math/linear-algebra, math/matrix-analysis, numerical-linear-algebra]
topic: Schur 分解
exercise: "[[习题 - Schur 分解]]"
prerequisites: ["[[Schur 分解]]", "[[QR 分解]]", "[[广义特征向量与 Jordan 结构]]"]
related: ["[[特征分解]]", "[[定理 - 有限维谱定理]]", "[[矩阵函数与矩阵指数]]", "[[矩阵扰动]]"]
sources: ["Axler-LADR4e-5C-6B-7B", "LAPACK-Schur", "SciPy-linalg-schur", "MIT-18.335-Week6"]
created: 2026-08-15
updated: 2026-08-15
---

# 解答 - Schur 分解

> [!warning] 使用边界
> 请先独立完成[[习题 - Schur 分解]]并记录卡点。能跟随下文计算，不等于能独立恢复复 Schur 归纳证明、识别实 $2\times2$ 块、构造最小反例，或在数值实验中区分后向残差与谱前向误差。

## A. 识别与复述

## LA-SCHUR-A01

### 1. 每个复方阵是否都有复 Schur 分解

**正确。**

任意 $A\in\mathbb C^{n\times n}$ 都存在酉矩阵 $Q$ 与上三角矩阵 $T$，使

$$
A=QTQ^*.
$$

存在性的关键是：复特征多项式必有根，因此总能先找到一个单位特征向量，再对低一维压缩块归纳。

### 2. 每个实方阵是否都能实上三角化

**错误。**

实旋转矩阵

$$
R=\begin{bmatrix}0&-1\\1&0\end{bmatrix}
$$

没有实特征值。若它能实相似为上三角矩阵，上三角对角线上必须出现实特征值，矛盾。

最小修正是：每个实方阵都能被实正交相似为**准上三角矩阵**，其对角线上允许编码共轭复特征值对的 $2\times2$ 实块。

### 3. 复 Schur 对角线是否给出全部特征值

**正确。**

酉相似保持特征多项式，而上三角矩阵满足

$$
\det(tI-T)=\prod_{j=1}^n(t-t_{jj}).
$$

所以对角元按代数重数给出全部特征值。

### 4. Schur 向量是否全是特征向量

**错误。**

由 $AQ=QT$ 的第 $j$ 列，

$$
Aq_j=\sum_{i=1}^j t_{ij}q_i.
$$

$q_1$ 必为特征向量；当 $j>1$ 时，右侧通常含先前的 $q_i$，故 $q_j$ 通常不是特征向量。最小修正是：前 $k$ 个 Schur 向量作为整体张成 $A$-不变子空间。

### 5. 前缀 Schur 子空间是否不变

**正确。**

上式表明每个 $Aq_j$ 都位于 $\operatorname{span}(q_1,\ldots,q_j)$。于是

$$
A\operatorname{span}(q_1,\ldots,q_k)
\subseteq
\operatorname{span}(q_1,\ldots,q_k).
$$

### 6. 正规矩阵的三角 Schur 形式

**正确。**

正规性在酉相似下保持，而正规上三角矩阵必为对角矩阵。因此严格上三角部分全为零。

### 7. 对角 Schur 形式能否推出正规

**正确。**

若 $A=QDQ^*$ 且 $D$ 对角，则

$$
AA^*=QDD^*Q^*=QD^*DQ^*=A^*A.
$$

所以 $A$ 正规。

### 8. Schur 分解是否唯一

**错误。**

可以重排特征值；每个 Schur 向量还可乘单位模相位；重复特征值的子空间内部有更多酉自由度。即便对角元素互异，也不能要求 $Q,T$ 逐元素唯一。

### 9. 实 $2\times2$ 对角块的含义

**正确，按标准实 Schur 形式理解。**

标准算法把实特征值放进 $1\times1$ 块，把非实共轭对放进 $2\times2$ 实块。不能只读这个块的两个对角元，而应对整个块求特征值。

### 10. QR 与 Schur 是否只是不同写法

**错误。**

$$
A=QR
$$

是乘积分解，常用于最小二乘；

$$
A=QTQ^*
$$

是酉相似分解，服务于谱与不变子空间。两处字母 $Q$ 的角色也不必相同。

### 11. 一步 QR 迭代是否为酉相似

**正确。**

因为 $A_k=Q_kR_k$，所以 $R_k=Q_k^*A_k$，从而

$$
A_{k+1}=R_kQ_k=Q_k^*A_kQ_k.
$$

### 12. 小重构残差能否保证小谱前向误差

**错误。**

小残差说明计算结果是邻近矩阵的精确分解，即后向误差小；若原矩阵高度非正规或接近缺陷，邻近矩阵的特征值仍可能相差很大。还必须讨论特征值或谱簇本身的条件性。

### 13. 复 Schur 三角泄漏

**正确。**

复 Schur 形式应为上三角，因此

$$
\|\operatorname{tril}(T,-1)\|
$$

直接测量所有严格下三角元素的大小。通常还应除以 $\|T\|$ 得到相对量。

### 14. 实 Schur 的第一条次对角线是否全是误差

**错误。**

合法 $2\times2$ 实块需要第一条次对角线元素。实 Schur 的泄漏检查只能处罚合法块结构以下的元素，不能把块内部元素误删。

### A 题结构总表

| 问题 | 正确对象 |
|---|---|
| 一般复方阵 | 复上三角 Schur 形式 |
| 一般实方阵 | 实准上三角 Schur 形式 |
| 单个 Schur 列 | 通常不是特征向量 |
| 前缀 Schur 列空间 | 不变子空间 |
| 正规矩阵 | Schur 形式可对角 |
| 小残差 | 后向准确，不自动等于前向准确 |

## B. 手算、构造与验收

## LA-SCHUR-B01

### 1. 谱、重数与可对角化性

$$
\begin{aligned}
p_A(t)
&=\det(tI-A)\\
&=\det\begin{bmatrix}t-1&1\\-1&t-3\end{bmatrix}\\
&=(t-1)(t-3)+1\\
&=(t-2)^2.
\end{aligned}
$$

唯一特征值为 $\lambda=2$，代数重数 $a_2=2$。又

$$
A-2I
=
\begin{bmatrix}-1&-1\\1&1\end{bmatrix},
$$

故

$$
\ker(A-2I)
=\operatorname{span}\left\{\begin{bmatrix}1\\-1\end{bmatrix}\right\},
\qquad
g_2=1.
$$

因为 $g_2<a_2$，$A$ 不可对角化。

### 2. 标准正交性

直接计算

$$
q_1^{\mathsf T}q_1=q_2^{\mathsf T}q_2=1,
\qquad
q_1^{\mathsf T}q_2=0.
$$

因此

$$
Q
=\frac1{\sqrt2}
\begin{bmatrix}
1&1\\
-1&1
\end{bmatrix},
\qquad
Q^{\mathsf T}Q=I.
$$

### 3. 用列坐标得到 $T$

第一列：

$$
Aq_1
=\frac1{\sqrt2}
\begin{bmatrix}2\\-2\end{bmatrix}
=2q_1.
$$

第二列：

$$
Aq_2
=\frac1{\sqrt2}
\begin{bmatrix}0\\4\end{bmatrix}
=-2q_1+2q_2.
$$

因此 $AQ=QT$ 中两列的坐标依次是 $[2,0]^{\mathsf T}$ 与 $[-2,2]^{\mathsf T}$：

$$
\boxed{
T=Q^{\mathsf T}AQ
=
\begin{bmatrix}
2&-2\\
0&2
\end{bmatrix}
}.
$$

### 4. 重构与 Schur 向量语义

由 $T=Q^{\mathsf T}AQ$ 及 $QQ^{\mathsf T}=I$，

$$
QTQ^{\mathsf T}
=QQ^{\mathsf T}AQQ^{\mathsf T}
=A.
$$

$q_1$ 是特征向量，因为 $Aq_1=2q_1$。但

$$
Aq_2=-2q_1+2q_2\ne2q_2,
$$

所以 $q_2$ 不是特征向量。

### 5. 矩阵幂

写成

$$
T=2I+N,
\qquad
N=\begin{bmatrix}0&-2\\0&0\end{bmatrix},
\qquad
N^2=0.
$$

故对 $k\ge0$，

$$
T^k
=2^kI+k2^{k-1}N
=2^k
\begin{bmatrix}
1&-k\\0&1
\end{bmatrix}.
$$

乘回原坐标：

$$
\boxed{
A^k
=QT^kQ^{\mathsf T}
=2^{k-1}
\begin{bmatrix}
2-k&-k\\
k&2+k
\end{bmatrix}
}.
$$

当 $k=0$ 时右侧为 $I$，所以公式包含初值。

### 6. 矩阵指数

由于 $2I$ 与 $N$ 可交换且 $N^2=0$，

$$
e^{tT}
=e^{2t}e^{tN}
=e^{2t}(I+tN)
=e^{2t}
\begin{bmatrix}
1&-2t\\0&1
\end{bmatrix}.
$$

因此

$$
\boxed{
e^{tA}
=Qe^{tT}Q^{\mathsf T}
=e^{2t}
\begin{bmatrix}
1-t&-t\\
t&1+t
\end{bmatrix}
}.
$$

### 7. 四个精确验收量

所有等式在精确算术中成立，所以

$$
\boxed{
\|A-QTQ^{\mathsf T}\|_F
=\|Q^{\mathsf T}Q-I\|_F
=\|\operatorname{tril}(T,-1)\|_F
=\|Aq_1-2q_1\|_2
=0
}.
$$

浮点实验中不会恰好为零，应把前三者相对化并与机器精度、维数及问题尺度比较。

### 8. 严格上三角耦合量

$$
\|T\|_F^2
=|2|^2+|-2|^2+|2|^2
=12,
$$

而

$$
\sum_i|\lambda_i|^2=4+4=8.
$$

所以

$$
\boxed{
\|T\|_F^2-\sum_i|\lambda_i|^2=4=|-2|^2
}.
$$

在复 Schur 形式中，这一差值正是全部严格上三角元素模平方之和。本例只有一个耦合 $t_{12}=-2$。

### 9. 旋转矩阵的实与复 Schur 形式

特征多项式为

$$
p_R(t)=t^2+1,
$$

在 $\mathbb R$ 上没有根。若存在实上三角相似形式，其实对角元必须是实特征值，矛盾。

但实 Schur 允许 $2\times2$ 对角块。取

$$
Q=I_2,
\qquad
T=R,
$$

则 $R=QTQ^{\mathsf T}$，且整个 $T$ 就是一个合法实块。

在 $\mathbb C$ 上可取

$$
q_1=\frac1{\sqrt2}\begin{bmatrix}1\\-i\end{bmatrix},
\qquad
q_2=\frac1{\sqrt2}\begin{bmatrix}1\\i\end{bmatrix},
\qquad
Q=[q_1\ q_2].
$$

因为

$$
Rq_1=iq_1,
\qquad
Rq_2=-iq_2,
$$

所以

$$
Q^*RQ
=\begin{bmatrix}i&0\\0&-i\end{bmatrix}.
$$

这是同时也是特征分解的复 Schur 分解；原因是 $R$ 正规。

## C. 推导与证明

## LA-SCHUR-C01

### 1. 上三角与不变旗标等价

设 $[A]_{\mathcal Q}=(a_{ij})$，其中 $\mathcal Q=(q_1,\ldots,q_n)$。

若矩阵上三角，则第 $j$ 列在第 $j$ 行以下为零，因此

$$
Aq_j=\sum_{i=1}^{j}a_{ij}q_i.
$$

对任意 $k$，当 $j\le k$ 时 $Aq_j\in V_k$，故 $AV_k\subseteq V_k$。

反过来，若每个 $V_k$ 都不变，则

$$
Aq_j\in AV_j\subseteq V_j
=\operatorname{span}(q_1,\ldots,q_j).
$$

所以 $Aq_j$ 在 $q_{j+1},\ldots,q_n$ 方向上的坐标全为零，即第 $j$ 列对角线以下全为零。故矩阵上三角。

### 2. 复 Schur 定理的维数归纳证明

**归纳命题。** 每个 $n$ 维复内积空间上的线性算子都能在某组标准正交基下表示为上三角矩阵。

**基例。** $n=1$ 时显然成立。

**归纳步骤。** 假设命题对 $n-1$ 维成立。因为 $A$ 的特征多项式是次数 $n$ 的复多项式，代数学基本定理保证存在特征值 $\lambda$ 与非零特征向量 $v$。归一化得到

$$
q_1=\frac{v}{\|v\|},
\qquad
Aq_1=\lambda q_1.
$$

把 $q_1$ 扩充为标准正交基 $(q_1,w_2,\ldots,w_n)$。令

$$
W=\operatorname{span}(w_2,\ldots,w_n)=q_1^\perp.
$$

在这组基下，第一列是 $[\lambda,0,\ldots,0]^{\mathsf T}$，因此矩阵具有块形

$$
[A]
=
\begin{bmatrix}
\lambda&r^*\\
0&B
\end{bmatrix}.
$$

注意：这只用到 $\operatorname{span}(q_1)$ 不变；$W$ 本身未必对 $A$ 不变。这里的 $B$ 表示把 $Aw$ 正交投影回 $W$ 后得到的压缩算子

$$
B=P_WA|_W:W\to W.
$$

$W$ 是 $n-1$ 维复内积空间。由归纳假设，存在 $W$ 上的标准正交基 $(u_2,\ldots,u_n)$，使 $B$ 在该基下上三角。由于每个 $u_j\in W=q_1^\perp$，

$$
(q_1,u_2,\ldots,u_n)
$$

是整个 $V$ 的标准正交基。在这组基中左下块仍为零，右下块变成上三角，所以整个矩阵上三角。归纳完成。

若把这组基向量作为 $Q$ 的列，则

$$
Q^*AQ=T,
\qquad
A=QTQ^*.
$$

### 3. 谱、迹与行列式

酉相似不改变特征多项式：

$$
\begin{aligned}
\det(tI-A)
&=\det\bigl(tI-QTQ^*\bigr)\\
&=\det\bigl(Q(tI-T)Q^*\bigr)\\
&=\det(Q)\det(tI-T)\det(Q^*)\\
&=\det(tI-T).
\end{aligned}
$$

其中 $\det(Q)\det(Q^*)=|\det Q|^2=1$。又因 $T$ 上三角，

$$
\det(tI-T)=\prod_{i=1}^n(t-t_{ii}).
$$

故谱按代数重数就是 $t_{11},\ldots,t_{nn}$。

迹在相似变换下不变，且三角矩阵的迹是对角和：

$$
\operatorname{tr}(A)
=\operatorname{tr}(T)
=\sum_i t_{ii}.
$$

行列式同理：

$$
\det(A)
=\det(T)
=\prod_i t_{ii}.
$$

### 4. 正规上三角矩阵必对角

设 $T=(t_{ij})$ 上三角且正规，即 $T^*T=TT^*$。比较两边的 $(1,1)$ 元素：

$$
(T^*T)_{11}=\sum_{k=1}^n|t_{k1}|^2=|t_{11}|^2,
$$

因为第一列对角线以下全为零；而

$$
(TT^*)_{11}=\sum_{k=1}^n|t_{1k}|^2
=|t_{11}|^2+\sum_{k=2}^n|t_{1k}|^2.
$$

二者相等迫使 $t_{1k}=0$ 对所有 $k>1$。于是

$$
T=t_{11}\oplus T_2.
$$

把正规等式限制到右下块可知 $T_2$ 仍正规且上三角。对维数归纳，$T_2$ 对角，因此 $T$ 对角。

现在若 $A$ 正规，取 Schur 分解 $A=QTQ^*$。正规性在酉相似下保持：

$$
T^*T=Q^*A^*AQ=Q^*AA^*Q=TT^*.
$$

故 $T$ 对角，$A$ 酉可对角化。

反过来，若 $A=QDQ^*$ 且 $D$ 对角，则 $DD^*=D^*D$，乘回 $Q,Q^*$ 得 $AA^*=A^*A$。因此

$$
\boxed{A\text{ 酉可对角化}\Longleftrightarrow A\text{ 正规}}.
$$

### 5. Schur 前缀子空间与投影

由

$$
AQ=QT
$$

及分块形式，

$$
A[Q_1\ Q_2]
=
[Q_1\ Q_2]
\begin{bmatrix}T_{11}&T_{12}\\0&T_{22}\end{bmatrix}.
$$

比较第一块列得到

$$
\boxed{AQ_1=Q_1T_{11}}.
$$

故 $\operatorname{range}(Q_1)$ 对 $A$ 不变。

在 Schur 坐标中，$P=Q_1Q_1^*$ 变成

$$
Q^*PQ
=D
=\begin{bmatrix}I&0\\0&0\end{bmatrix}.
$$

分别计算

$$
TD
=\begin{bmatrix}T_{11}&0\\0&0\end{bmatrix},
\qquad
DT
=\begin{bmatrix}T_{11}&T_{12}\\0&0\end{bmatrix}.
$$

因此 $TD=DT$ 当且仅当 $T_{12}=0$。酉相似保持乘积关系，所以

$$
\boxed{AP=PA\Longleftrightarrow T_{12}=0}.
$$

这说明“不变”只保证左下块为零；投影可交换还要求右上块也为零，即子空间及其正交补都不变。

### 6. QR 迭代是一串酉相似

由 $A_k=Q_kR_k$ 且 $Q_k^*Q_k=I$，

$$
R_k=Q_k^*A_k.
$$

所以

$$
\boxed{A_{k+1}=R_kQ_k=Q_k^*A_kQ_k}.
$$

定义

$$
Z_m=Q_0Q_1\cdots Q_{m-1}.
$$

对 $m=1$，有 $A_1=Z_1^*A_0Z_1$。若

$$
A_m=Z_m^*A_0Z_m,
$$

则

$$
\begin{aligned}
A_{m+1}
&=Q_m^*A_mQ_m\\
&=Q_m^*Z_m^*A_0Z_mQ_m\\
&=(Z_mQ_m)^*A_0(Z_mQ_m)\\
&=Z_{m+1}^*A_0Z_{m+1}.
\end{aligned}
$$

归纳即得结论。由于酉矩阵乘积仍酉，每一步都保持特征值与二范数条件良好的坐标变换。

### 7. 二阶三角块的幂与函数

设

$$
T^k=\begin{bmatrix}\lambda^k&s_k\\0&\mu^k\end{bmatrix}.
$$

初值 $s_0=0$。右乘 $T$ 得

$$
T^{k+1}
=
\begin{bmatrix}
\lambda^{k+1}&\lambda^k\eta+s_k\mu\\
0&\mu^{k+1}
\end{bmatrix},
$$

所以

$$
s_{k+1}=\eta\lambda^k+\mu s_k.
$$

展开递推：

$$
s_k
=\eta\sum_{j=0}^{k-1}\lambda^{k-1-j}\mu^j.
$$

因此

$$
T^k=
\begin{bmatrix}
\lambda^k&\eta\sum_{j=0}^{k-1}\lambda^{k-1-j}\mu^j\\
0&\mu^k
\end{bmatrix}.
$$

若 $\lambda\ne\mu$，有限几何和给出

$$
\sum_{j=0}^{k-1}\lambda^{k-1-j}\mu^j
=\frac{\lambda^k-\mu^k}{\lambda-\mu}.
$$

若 $\lambda=\mu$，共有 $k$ 项，故该和为 $k\lambda^{k-1}$。

对多项式 $f(z)=\sum_{k=0}^m c_kz^k$，线性相加得到

$$
f(T)_{12}
=\eta\sum_{k=0}^m c_k
\sum_{j=0}^{k-1}\lambda^{k-1-j}\mu^j.
$$

当 $\lambda\ne\mu$ 时，

$$
f(T)_{12}
=\eta\sum_kc_k\frac{\lambda^k-\mu^k}{\lambda-\mu}
=\eta\frac{f(\lambda)-f(\mu)}{\lambda-\mu}.
$$

当 $\lambda=\mu$ 时，

$$
f(T)_{12}
=\eta\sum_kc_kk\lambda^{k-1}
=\eta f'(\lambda).
$$

这正是“互异谱点用一阶差商、重合谱点用导数”的统一规律。

## D. 边界、反例与纠错

## LA-SCHUR-D01

### 1. Schur 向量是否逐列为特征向量

**错误。** 取已经上三角的

$$
A=\begin{bmatrix}1&1\\0&2\end{bmatrix},
\qquad
Q=I,
\qquad
T=A.
$$

这是合法 Schur 分解，但

$$
Ae_2=\begin{bmatrix}1\\2\end{bmatrix}\ne2e_2.
$$

断裂点在于 $AQ=QT$ 的第 $j$ 列允许含 $q_1,\ldots,q_{j-1}$。最小修正：$q_1$ 必为特征向量；前 $k$ 列作为整体张成不变子空间。

### 2. Schur 分解是否唯一

**错误。** 取

$$
A=\operatorname{diag}(1,2).
$$

既可取 $Q=I,T=\operatorname{diag}(1,2)$，也可取交换矩阵

$$
Q=\begin{bmatrix}0&1\\1&0\end{bmatrix},
\qquad
T=\operatorname{diag}(2,1).
$$

此外还能给 Schur 向量乘单位模相位。最小修正：Schur 形式在给定排序、相位约定且无重复谱时仍只有受限意义的唯一性；通常只比较谱、子空间与残差。

### 3. 实方阵是否总能实上三角化

**错误。** 取

$$
R=\begin{bmatrix}0&-1\\1&0\end{bmatrix}.
$$

它没有实特征值，但任何实上三角矩阵的对角元都是实特征值。最小修正：允许实准上三角形式中的 $2\times2$ 块，或转到 $\mathbb C$ 使用复 Schur 形式。

### 4. 不变子空间的正交投影是否一定可交换

**错误。** 仍取

$$
A=\begin{bmatrix}1&1\\0&2\end{bmatrix},
\qquad
\mathcal S=\operatorname{span}(e_1),
\qquad
P=\begin{bmatrix}1&0\\0&0\end{bmatrix}.
$$

因为 $Ae_1=e_1$，$\mathcal S$ 不变。但

$$
AP=\begin{bmatrix}1&0\\0&0\end{bmatrix},
\qquad
PA=\begin{bmatrix}1&1\\0&0\end{bmatrix},
$$

所以 $AP\ne PA$。断裂点在于 $\mathcal S^\perp=\operatorname{span}(e_2)$ 不变性失败。最小修正：若 $\mathcal S$ 与 $\mathcal S^\perp$ 都不变，即 $\mathcal S$ 是约化子空间，则其正交投影与 $A$ 可交换。

### 5. 酉坐标是否能治愈谱条件性

**错误。** 比较

$$
A_0=\begin{bmatrix}0&1\\0&0\end{bmatrix},
\qquad
A_\varepsilon=\begin{bmatrix}0&1\\\varepsilon&0\end{bmatrix}.
$$

输入扰动满足

$$
\|A_\varepsilon-A_0\|_2=\varepsilon,
$$

但 $A_0$ 的双重特征值 $0$ 在 $A_\varepsilon$ 中裂成

$$
\lambda_\pm=\pm\sqrt\varepsilon.
$$

谱移动是 $O(\sqrt\varepsilon)$，大于输入扰动的 $O(\varepsilon)$。Schur 坐标的换入换出不放大二范数，但原问题“特征值作为矩阵的函数”仍可能病态。

### 6. QR 分解是否自动给出 Schur 分解

**错误。** 对旋转矩阵 $R$，一种 QR 分解是

$$
R=QI,
\qquad
Q=R.
$$

若把 QR 的 $I$ 误当 Schur 的 $T$，其特征值是 $(1,1)$，与 $R$ 的 $(i,-i)$ 完全不同。根本原因是 QR 关系 $A=QR$ 不是相似关系；Schur 要求 $T=Q^*AQ$。

### 7. 上三角正规矩阵能否有严格上三角元素

**错误。** 比较正规等式的 $(1,1)$ 元素，第一行范数必须等于第一列范数。上三角性使第一列只剩 $t_{11}$，于是第一行其余元素必须全为零；对右下块归纳，所有严格上三角元素都为零。

最小修正：一般上三角矩阵可以有严格上三角元素；加上正规性后必为对角矩阵。

### 8. 相同 Schur 对角线能否推出相似

**错误。** 取

$$
A=I_2,
\qquad
B=J_2(1)=\begin{bmatrix}1&1\\0&1\end{bmatrix}.
$$

两者的 Schur 对角线都是 $(1,1)$，但 $A$ 的最小多项式是 $t-1$，$B$ 的最小多项式是 $(t-1)^2$，故不相似。Schur 对角线只保存特征值多重集合，不能恢复 Jordan 链或全部相似结构。

### 9. 机器精度级残差能否推出机器精度级特征值误差

**错误。** 第 5 问的近缺陷例子已经说明：一个 $O(\varepsilon)$ 的后向扰动可能引起 $O(\sqrt\varepsilon)$ 的特征值变化。若重特征值来自更大 Jordan 块，敏感性还可能呈 $\varepsilon^{1/m}$ 阶。

最小修正：小重构残差说明计算 Schur 对是后向准确的；只有在目标特征值或谱簇条件良好时，才能进一步推出相应前向误差小。

### D 题诊断表

| 错误直觉 | 缺少的条件或对象 |
|---|---|
| Schur 列都是 eigenvectors | 应改看前缀不变子空间 |
| 实上三角总存在 | 应允许 $2\times2$ 实块 |
| 不变投影必可交换 | 还需正交补也不变 |
| 酉基保证谱稳定 | 还需特征值/谱簇条件良好 |
| 同谱即相似 | 还需广义特征结构 |
| 小残差即小前向误差 | 还需条件数或谱分离控制 |

## E. AI 迁移：稳定 Schur 子空间、瞬态与反向传播

## AI-SCHUR-E01

记左上稳定块为

$$
M=\begin{bmatrix}r&\gamma\\0&r\end{bmatrix}.
$$

### 1. 稳定不变子空间

在 Schur 坐标中，前两个坐标组成

$$
\mathcal E=\operatorname{span}(e_1,e_2).
$$

若 $y=[z^{\mathsf T},0]^{\mathsf T}$，则

$$
Ty
=
\begin{bmatrix}Mz\\0\end{bmatrix}
\in\mathcal E.
$$

所以 $\mathcal E$ 对 $T$ 不变。乘回 $Q$，

$$
\mathcal S=Q\mathcal E=\operatorname{range}(Q_1)
$$

对 $A$ 不变。

又

$$
M^k
=
\begin{bmatrix}
r^k&\gamma kr^{k-1}\\
0&r^k
\end{bmatrix}.
$$

由于 $0<r<1$，既有 $r^k\to0$，也有 $kr^{k-1}\to0$。因此对每个 $h_0\in\mathcal S$，

$$
A^kh_0\to0.
$$

这里“稳定”指该不变子空间上的离散时间渐近衰减；它不意味着每个有限时刻都单调收缩，也不意味着整个三维系统稳定，因为 $u>1$。

### 2. 不变不等于正交投影可交换

在 Schur 坐标中，

$$
D=Q^{\mathsf T}PQ
=\begin{bmatrix}I_2&0\\0&0\end{bmatrix}.
$$

直接相乘：

$$
TD
=
\begin{bmatrix}
r&\gamma&0\\
0&r&0\\
0&0&0
\end{bmatrix},
$$

而

$$
DT
=
\begin{bmatrix}
r&\gamma&\beta\\
0&r&0\\
0&0&0
\end{bmatrix}.
$$

因为 $\beta\ne0$，$TD\ne DT$，从而

$$
\boxed{AP\ne PA}.
$$

这并不否定 $\mathcal S$ 不变：左下块为零已经保证稳定子空间内的向量不会产生第三坐标；右上角 $\beta$ 表示第三个坐标可以驱动第一个坐标，所以正交补并不不变。

### 3. 前向状态与有限时间瞬态

由二阶重复对角三角块公式，

$$
M^k
=
\begin{bmatrix}
r^k&\gamma kr^{k-1}\\0&r^k
\end{bmatrix}.
$$

因为 $y_0=Q^{\mathsf T}h_0=e_2$ 且第三坐标为零，

$$
\boxed{
y_k=T^ke_2
=
\begin{bmatrix}
\gamma kr^{k-1}\\
r^k\\
0
\end{bmatrix}
}.
$$

$Q$ 正交，所以

$$
\boxed{
\|h_k\|_2
=\|y_k\|_2
=\sqrt{|\gamma|^2k^2r^{2k-2}+r^{2k}}
}.
$$

尽管 $r^k$ 最终衰减，耦合产生的

$$
kr^{k-1}
$$

可以先增大再减小。它是重复 Schur 对角值与严格上三角耦合共同产生的有限时间多项式瞬态。

### 4. 终端损失的反向传播

前向映射为

$$
y_K=T^Ky_0.
$$

对

$$
L=\frac12\|y_K\|_2^2
$$

使用转置链式法则，

$$
\boxed{
\nabla_{y_0}L=(T^K)^{\mathsf T}y_K
}.
$$

先求完整矩阵幂。第三坐标到第一坐标的累积耦合是

$$
\begin{aligned}
c
&=\beta\sum_{j=0}^{K-1}r^{K-1-j}u^j\\
&=\beta\frac{u^K-r^K}{u-r}.
\end{aligned}
$$

因此用题中记号，

$$
T^K
=
\begin{bmatrix}
a&b&c\\
0&a&0\\
0&0&u^K
\end{bmatrix},
\qquad
y_K=\begin{bmatrix}b\\a\\0\end{bmatrix}.
$$

于是

$$
\boxed{
\nabla_{y_0}L
=
\begin{bmatrix}
ab\\
b^2+a^2\\
cb
\end{bmatrix}
}.
$$

本题刻意采用实正交 Schur 坐标，因此普通转置就是反向线性映射。若扩展到复状态，必须先声明实值损失下采用的复微分/Wirtinger 约定，再把相应伴随写成共轭转置，不能直接机械替换符号。

第三分量可能非零，是因为梯度问的是：“若初始第三坐标发生无穷小变化，损失如何变化？”虽然当前轨迹的 $y_{0,3}=0$，一个假想的第三坐标扰动仍会经 $u$ 放大，再通过 $\beta$ 驱动第一坐标，最终影响损失。**实际激活为零不等于对应灵敏度为零。**

### 5. 正交坐标中的范数保持

因为 $h_k=Qy_k$ 且 $Q^{\mathsf T}Q=I$，

$$
\|h_k\|_2^2
=y_k^{\mathsf T}Q^{\mathsf T}Qy_k
=\|y_k\|_2^2.
$$

又由 $y_0=Q^{\mathsf T}h_0$，转置链式法则给出

$$
\nabla_{h_0}L=Q\nabla_{y_0}L,
$$

所以

$$
\|\nabla_{h_0}L\|_2
=\|\nabla_{y_0}L\|_2.
$$

这排除了“仅因换基矩阵病态，坐标范数被额外放大”的假象；它不能排除 $T^k$ 中 $kr^{k-1}$、$u^k$ 或跨块耦合本身造成的真实动力学与梯度增长。

### 6. 重排稳定谱簇

三个特征值按代数重数是

$$
r, r, u.
$$

其中前两个满足 $|r|<1$，第三个满足 $|u|>1$。SciPy 复 Schur 接口可用

```python
T, Q, sdim = scipy.linalg.schur(A, output="complex", sort="iuc")
```

其中 `iuc` 表示 inside unit circle。也可传入返回 `abs(z) < 1` 的自定义谓词。正确排序后应有

$$
\boxed{\texttt{sdim}=2}.
$$

数值上若特征值非常靠近单位圆，必须声明分类容差；不能把浮点等于 $1$ 当作可靠边界。

### 7. 数值验收设计

若按上一问请求复 Schur 输出，计算返回的 $Q,T$ 可能为复数，因此以下统一用共轭转置 $Q^*$；若保持实 Schur 输出，$Q^*$ 就退化为 $Q^{\mathsf T}$。可报告下列相对量：

1. **分解重构**
   $$
   r_{\mathrm{rec}}
   =\frac{\|A-QTQ^*\|_F}{\max(\|A\|_F,\epsilon)};
   $$
2. **酉性**
   $$
   r_{\mathrm{orth}}=\|Q^*Q-I\|_F;
   $$
3. **稳定子空间不变性**
   $$
   r_{\mathrm{inv}}
   =\frac{\|AQ_1-Q_1T_{11}\|_F}{\max(\|A\|_F,\epsilon)};
   $$
4. **复三角泄漏**
   $$
   r_{\mathrm{tri}}
   =\frac{\|\operatorname{tril}(T,-1)\|_F}{\max(\|T\|_F,\epsilon)};
   $$
5. **排序验收**：检查 $T_{11}$ 的两个对角元满足 $|t_{ii}|<1$，其余对角元满足 $|t_{jj}|>1$，并验证 `sdim == 2`。

这些残差判断“计算出来的对象是否自洽”；若还要判断稳定子空间是否对输入扰动敏感，应另报告稳定/不稳定谱簇的分离或相关条件估计。

### 8. 对角状态矩阵删去了什么

若直接把状态矩阵参数化为对角矩阵，则各坐标独立传播：

$$
y_{k+1,i}=\lambda_i y_{k,i}.
$$

它删去了 Schur 形式中的严格上三角耦合，因此也删去了：

- $kr^{k-1}$ 一类重复谱点的多项式瞬态；
- 不同谱方向之间的 divided-difference 响应；
- 一个坐标驱动另一个坐标的非正规有限时间放大；
- 本题中不稳定坐标经 $\beta$ 影响稳定坐标的跨块通道。

这可能是有益的归纳偏置：传播可并行、长序列卷积更容易计算、稳定性约束更直接。但它比“一般矩阵在酉坐标下的表达”更强，会排除真实系统或学习系统中的方向耦合。因此模型设计结论应写成：

> 对角参数化用表达能力交换了计算结构与可控性；若任务依赖有限时间非正规瞬态，一般三角、低秩修正或其他结构化状态矩阵可能更合适。

## 最终自检

完成本套题后，应能在不翻正文的情况下说明：

1. 为什么复数域上的特征值存在足以启动 Schur 归纳，但不能直接推出正交补不变；
2. 为什么实 Schur 需要 $2\times2$ 块；
3. 为什么 $q_j$ 通常不是特征向量，而 $\operatorname{span}(q_1,\ldots,q_j)$ 却不变；
4. 为什么正规性会把三角 Schur 形式压成对角形式；
5. 为什么 QR 分解不是 Schur 分解，而 QR 迭代却能逼近 Schur 形式；
6. 为什么小重构残差只首先支持后向准确性；
7. 为什么稳定特征值仍可能伴随有限时间瞬态；
8. 为什么正交 Schur 投影不一定是与 $A$ 可交换的谱投影。

若第 1、4、5、6 或 8 项不能独立推导，建议回到[[Schur 分解]]相应证明，再隔日重做 C2、C4、C5、C6 与 D4、D9。
