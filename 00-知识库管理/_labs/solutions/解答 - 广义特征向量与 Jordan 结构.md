---
type: solution
status: draft
area: [math/linear-algebra, math/matrix-analysis]
topic: 广义特征向量与 Jordan 结构
exercise: "[[习题 - 广义特征向量与 Jordan 结构]]"
prerequisites: ["[[广义特征向量与 Jordan 结构]]", "[[特征多项式与重数]]"]
related: ["[[特征分解]]", "[[Schur 分解]]", "[[矩阵函数与矩阵指数]]", "[[矩阵扰动]]"]
sources: ["Axler-LADR4e-8A-8C", "LAPACK-DHSEQR", "PyTorch-linalg-eig"]
created: 2026-08-15
updated: 2026-08-15
---

# 解答 - 广义特征向量与 Jordan 结构

> [!warning] 使用边界
> 请先独立完成[[习题 - 广义特征向量与 Jordan 结构]]并记录卡点。能沿着下文复述，不等于已经能独立恢复 Jordan 块、重建核空间证明，或在浮点问题中主动拒绝不可靠的 Jordan 诊断。

## A. 识别与复述

## LA-JORD-A01

### 1. 普通特征向量是否属于广义特征向量

**正确。**

普通特征向量满足

$$
(\boldsymbol A-\lambda I)\boldsymbol v=0,
\qquad
\boldsymbol v\ne0.
$$

这就是定义中取 $k=1$ 的情形，所以它是一阶广义特征向量。

### 2. 广义特征向量是否一定不是普通特征向量

**错误。**

广义特征向量包含普通特征向量。最小修正是：

> 阶大于 $1$ 的广义特征向量不是普通特征向量。

### 3. 零向量的身份

**正确。**

广义特征空间是子空间，必须包含零向量；但“广义特征向量”的定义要求非零。否则零向量会同时对应所有 $\lambda$，失去区分作用。

### 4. 某个五次幂为零能否确定阶

**错误。**

阶是满足

$$
(\boldsymbol A-\lambda I)^k\boldsymbol v=0
$$

的**最小**正整数。已知五次幂为零，只能推出阶不超过 $5$。例如普通特征向量的一次幂已经为零，五次幂当然也为零。

### 5. 有限维中的统一表达

**正确。**

核空间链在最多 $n$ 次严格增长后必须稳定，因此所有会在有限步被消去的向量都已经位于

$$
\ker(\boldsymbol A-\lambda I)^n.
$$

### 6. 核空间一旦停止是否永久停止

**正确。**

若 $K_k=K_{k+1}$，任取 $\boldsymbol v\in K_{k+2}$ 并令

$$
\boldsymbol w=(\boldsymbol A-\lambda I)\boldsymbol v.
$$

则 $\boldsymbol w\in K_{k+1}=K_k$，所以 $\boldsymbol v\in K_{k+1}$。故 $K_{k+2}=K_{k+1}$；归纳即可。

### 7. 块数量与代数重数

**错误。**

块数量等于几何重数 $g_\lambda$；代数重数等于所有对应块大小之和。

例如 $J_3(2)$ 只有一个块，但 $a_2=3$、$g_2=1$。

### 8. 最大块与最小多项式

**正确。**

若最大块大小为 $s_\lambda$，则恰好需要

$$
(\boldsymbol A-\lambda I)^{s_\lambda}
$$

才能消去该特征值对应的所有链；更低次数无法消去最长链。因此最小多项式中 $(t-\lambda)$ 的指数就是 $s_\lambda$。

### 9. $a_\lambda=g_\lambda$ 的结构含义

**正确。**

若块大小为 $r_1,\ldots,r_b$，则

$$
a_\lambda=\sum_i r_i,
\qquad
g_\lambda=b.
$$

每个 $r_i\ge1$。只有所有 $r_i=1$ 时，和才等于项数。

### 10. 任意实方阵是否有实 Jordan 形式

**错误。**

还需要特征多项式在 $\mathbb R$ 上分裂。例如

$$
\begin{bmatrix}0&-1\\1&0\end{bmatrix}
$$

的特征多项式是 $t^2+1$，没有实根，因此不存在只由实特征值 Jordan 块组成的实 Jordan 形式。转到 $\mathbb C$ 后可以对角化。

### 11. Jordan 基是否总能正交

**错误。**

非平凡 Jordan 链满足

$$
(\boldsymbol A-\lambda I)\boldsymbol v_2=\boldsymbol v_1,
$$

它不是由互相独立的特征方向组成。一般 Jordan 换基矩阵只要求可逆，不要求正交/酉。若一个复矩阵能被酉对角化，它必须正规；非平凡 Jordan 块不是正规矩阵。

### 12. 核空间增长能否唯一恢复块

**正确。**

若

$$
d_k=\dim\ker(\boldsymbol A-\lambda I)^k,
$$

则

$$
d_k-d_{k-1}
=
\#\{\text{块大小}\ge k\}.
$$

进一步相减即可得到大小恰好为 $k$ 的块数。

### 13. 谱半径为一是否保证矩阵幂有界

**错误。**

取

$$
\boldsymbol A=J_2(1)
=
\begin{bmatrix}1&1\\0&1\end{bmatrix}.
$$

虽然 $\rho(\boldsymbol A)=1$，但

$$
\boldsymbol A^k
=
\begin{bmatrix}1&k\\0&1\end{bmatrix},
$$

范数随 $k$ 增长。最小修正：谱半径不超过 $1$，并且单位圆上的特征值只有大小为 $1$ 的 Jordan 块，才保证固定有限维矩阵的幂有界。

### 14. 一般浮点矩阵的数值选择

**正确。**

Jordan 块对扰动不连续，显式恢复又依赖多次近秩判定。Schur 分解使用正交/酉换基，是一般稠密特征问题的标准数值接口。

### A 题结构总表

| 对象 | Jordan 语言 |
|---|---|
| $a_\lambda$ | 对应块大小之和 |
| $g_\lambda$ | 对应块数量 |
| 最小多项式指数 | 最大块大小 |
| $d_k-d_{k-1}$ | 大小至少为 $k$ 的块数量 |
| 可对角化 | 所有块都是 $1\times1$，且特征多项式分裂 |

## B. 手算与构造

## LA-JORD-B01

矩阵已经是两个块的直和：

$$
\boldsymbol A
=
J_3(2)\oplus J_2(-1).
$$

记

$$
N_3
=
\begin{bmatrix}
0&1&0\\
0&0&1\\
0&0&0
\end{bmatrix},
\qquad
N_2
=
\begin{bmatrix}
0&1\\
0&0
\end{bmatrix}.
$$

则

$$
J_3(2)=2I_3+N_3,
\qquad
J_2(-1)=-I_2+N_2.
$$

### 1. 特征多项式与代数重数

上三角矩阵的特征多项式由对角线读取：

$$
\begin{aligned}
p_{\boldsymbol A}(t)
&=(t-2)^3(t+1)^2.
\end{aligned}
$$

因此

$$
a_2=3,
\qquad
a_{-1}=2.
$$

检查总次数：$3+2=5$，等于矩阵维数。

### 2. 核空间维数

对 $\lambda=2$，第二个块满足

$$
J_2(-1)-2I_2=-3I_2+N_2,
$$

其对角元都是 $-3$，所以可逆，不贡献核。只需看 $N_3$：

$$
\begin{aligned}
d_1(2)&=\dim\ker N_3=1,\\
d_2(2)&=\dim\ker N_3^2=2,\\
d_3(2)&=\dim\ker N_3^3=3.
\end{aligned}
$$

对 $\lambda=-1$，第一个块满足

$$
J_3(2)+I_3=3I_3+N_3,
$$

可逆，所以只看 $N_2$：

$$
d_1(-1)=1,
\qquad
d_2(-1)=2.
$$

### 3. 从增长量恢复块

约定 $d_0=0$。对 $\lambda=2$：

$$
\Delta_1=1,
\qquad
\Delta_2=1,
\qquad
\Delta_3=1,
\qquad
\Delta_4=0.
$$

所以大小至少为 $1,2,3$ 的块都各有一个，大小至少为 $4$ 的块没有。唯一块大小是 $3$。

对 $\lambda=-1$：

$$
\Delta_1=1,
\qquad
\Delta_2=1,
\qquad
\Delta_3=0.
$$

所以唯一块大小是 $2$。

### 4. 两种重数、缺陷与可对角化

每个特征值都只有一个块，因此

$$
g_2=1,
\qquad
g_{-1}=1.
$$

缺陷为

$$
a_2-g_2=3-1=2,
\qquad
a_{-1}-g_{-1}=2-1=1.
$$

由于存在大小大于 $1$ 的块，$\boldsymbol A$ 不可对角化。

### 5. 最小多项式

最大 $2$-块大小为 $3$，最大 $(-1)$-块大小为 $2$，故

$$
\boxed{
m_{\boldsymbol A}(t)
=(t-2)^3(t+1)^2
}.
$$

本例每个特征值都只有一个块，所以恰有

$$
m_{\boldsymbol A}=p_{\boldsymbol A}.
$$

当然满足 $m_{\boldsymbol A}\mid p_{\boldsymbol A}$。

### 6. Jordan 链与向量阶

对 $\lambda=2$：

$$
(\boldsymbol e_1,\boldsymbol e_2,\boldsymbol e_3)
$$

是一条长度为 $3$ 的链，因为

$$
(\boldsymbol A-2I)\boldsymbol e_1=0,
\quad
(\boldsymbol A-2I)\boldsymbol e_2=\boldsymbol e_1,
\quad
(\boldsymbol A-2I)\boldsymbol e_3=\boldsymbol e_2.
$$

所以 $\boldsymbol e_1,\boldsymbol e_2,\boldsymbol e_3$ 的阶分别为 $1,2,3$。

对 $\lambda=-1$：

$$
(\boldsymbol e_4,\boldsymbol e_5)
$$

是一条长度为 $2$ 的链，因为

$$
(\boldsymbol A+I)\boldsymbol e_4=0,
\qquad
(\boldsymbol A+I)\boldsymbol e_5=\boldsymbol e_4.
$$

所以阶分别为 $1,2$。

### 7. $\boldsymbol A^k$ 的闭式

因为 $N_3^3=0$，

$$
J_3(2)^k
=
2^kI_3
+k2^{k-1}N_3
+\binom{k}{2}2^{k-2}N_3^2.
$$

展开为

$$
J_3(2)^k
=
\begin{bmatrix}
2^k&k2^{k-1}&\binom{k}{2}2^{k-2}\\
0&2^k&k2^{k-1}\\
0&0&2^k
\end{bmatrix}.
$$

若 $k<2$，含 $\binom{k}{2}$ 的项按零处理。

因为 $N_2^2=0$，

$$
\begin{aligned}
J_2(-1)^k
&=(-I_2+N_2)^k\\
&=(-1)^kI_2+k(-1)^{k-1}N_2\\
&=
\begin{bmatrix}
(-1)^k&k(-1)^{k-1}\\
0&(-1)^k
\end{bmatrix}.
\end{aligned}
$$

因此

$$
\boxed{
\boldsymbol A^k
=
\begin{bmatrix}
2^k&k2^{k-1}&\binom{k}{2}2^{k-2}&0&0\\
0&2^k&k2^{k-1}&0&0\\
0&0&2^k&0&0\\
0&0&0&(-1)^k&k(-1)^{k-1}\\
0&0&0&0&(-1)^k
\end{bmatrix}
}.
$$

当 $k=0$ 时，整体应读作 $I_5$；带 $k$ 或 $\binom{k}{2}$ 的项为零。

### 8. 矩阵指数

对三阶块：

$$
e^{tJ_3(2)}
=
e^{2t}
\left(
I_3+tN_3+\frac{t^2}{2}N_3^2
\right)
=
e^{2t}
\begin{bmatrix}
1&t&t^2/2\\
0&1&t\\
0&0&1
\end{bmatrix}.
$$

对二阶块：

$$
e^{tJ_2(-1)}
=
e^{-t}(I_2+tN_2)
=
e^{-t}
\begin{bmatrix}
1&t\\
0&1
\end{bmatrix}.
$$

合并得到

$$
\boxed{
e^{t\boldsymbol A}
=
\begin{bmatrix}
e^{2t}&te^{2t}&\tfrac{t^2}{2}e^{2t}&0&0\\
0&e^{2t}&te^{2t}&0&0\\
0&0&e^{2t}&0&0\\
0&0&0&e^{-t}&te^{-t}\\
0&0&0&0&e^{-t}
\end{bmatrix}
}.
$$

### 9. 状态传播

初始向量是

$$
\boldsymbol h_0=\boldsymbol e_3+\boldsymbol e_5.
$$

由 $\boldsymbol A^k$ 的第 3 列与第 5 列相加：

$$
\boxed{
\boldsymbol h_k
=
\begin{bmatrix}
\binom{k}{2}2^{k-2}\\
k2^{k-1}\\
2^k\\
k(-1)^{k-1}\\
(-1)^k
\end{bmatrix}
}.
$$

来源对应如下：

- $\binom{k}{2}2^{k-2}$ 与 $k2^{k-1}$ 来自长度 $3$ 的 $\lambda=2$ 链；
- $k(-1)^{k-1}$ 来自长度 $2$ 的 $\lambda=-1$ 链；
- 纯指数项分别来自每条链的最后坐标。

检查 $k=0$：按组合数约定得到

$$
\boldsymbol h_0=[0,0,1,0,1]^{\mathsf T}.
$$

检查 $k=1$：

$$
\boldsymbol h_1=[0,1,2,1,-1]^{\mathsf T},
$$

与直接计算 $\boldsymbol A\boldsymbol h_0$ 一致。

## C. 推导与证明

## LA-JORD-C01

记 $N=T-\lambda I$、$K_k=\ker N^k$。

### 1. 核空间链单调增长

任取 $\boldsymbol v\in K_k$，则

$$
N^k\boldsymbol v=0.
$$

再作用一次 $N$：

$$
N^{k+1}\boldsymbol v
=N(N^k\boldsymbol v)
=N0
=0.
$$

所以 $\boldsymbol v\in K_{k+1}$。因此

$$
K_k\subseteq K_{k+1}
$$

对每个 $k$ 成立。

### 2. 一次相等导致永久稳定

假设 $K_k=K_{k+1}$。先证明 $K_{k+2}=K_{k+1}$。

本来已有 $K_{k+1}\subseteq K_{k+2}$。反向包含方面，任取 $\boldsymbol v\in K_{k+2}$，令

$$
\boldsymbol w=N\boldsymbol v.
$$

因为

$$
N^{k+1}\boldsymbol w
=N^{k+2}\boldsymbol v
=0,
$$

有 $\boldsymbol w\in K_{k+1}=K_k$。因此

$$
N^k\boldsymbol w=0.
$$

代入 $\boldsymbol w=N\boldsymbol v$：

$$
N^{k+1}\boldsymbol v=0,
$$

即 $\boldsymbol v\in K_{k+1}$。故二者相等。对后续层级重复这一论证，得到

$$
K_{k+j}=K_k
$$

对所有 $j\ge0$ 成立。

### 3. 为什么到 $n$ 必稳定

若 $K_k\subsetneq K_{k+1}$ 严格包含，则

$$
\dim K_{k+1}\ge\dim K_k+1.
$$

从 $\dim K_0=0$ 开始，若直到 $K_n$ 每一步都严格增长，则 $\dim K_n\ge n$，只能是 $K_n=V$；下一步无法再增长。若更早出现相等，则第 2 问说明之后永久稳定。

所以无论哪种情况，

$$
K_n=K_{n+1}=\cdots.
$$

若 $\boldsymbol v$ 是对应于 $\lambda$ 的广义特征向量，则存在某个 $m$ 使 $N^m\boldsymbol v=0$，即 $\boldsymbol v\in K_m$。稳定性给出 $\boldsymbol v\in K_n$。反过来，$K_n$ 中非零向量按定义都是广义特征向量。因此加上零向量后

$$
G_\lambda(T)=K_n=\ker(T-\lambda I)^n.
$$

### 4. 广义特征空间的不变性

任取 $\boldsymbol v\in G_\lambda(T)$。由第 3 问，

$$
(T-\lambda I)^n\boldsymbol v=0.
$$

因为 $T$ 与 $T-\lambda I$ 可交换，

$$
\begin{aligned}
(T-\lambda I)^n(T\boldsymbol v)
&=T(T-\lambda I)^n\boldsymbol v\\
&=T0\\
&=0.
\end{aligned}
$$

所以 $T\boldsymbol v\in G_\lambda(T)$。

### 5. Jordan 链的线性无关与矩阵

假设

$$
c_1\boldsymbol v_1+\cdots+c_r\boldsymbol v_r=0.
$$

若有非零系数，令 $j$ 是最大非零下标。作用 $N^{j-1}$：

$$
c_jN^{j-1}\boldsymbol v_j=0,
$$

因为所有 $i<j$ 的项已被消去，而

$$
N^{j-1}\boldsymbol v_j=\boldsymbol v_1.
$$

于是

$$
c_j\boldsymbol v_1=0.
$$

因 $\boldsymbol v_1\ne0$，得到 $c_j=0$，矛盾。故链向量线性无关。

又因为 $T=\lambda I+N$，

$$
\begin{aligned}
T\boldsymbol v_1&=\lambda\boldsymbol v_1,\\
T\boldsymbol v_2&=\boldsymbol v_1+\lambda\boldsymbol v_2,\\
T\boldsymbol v_3&=\boldsymbol v_2+\lambda\boldsymbol v_3,\\
&\ \vdots\\
T\boldsymbol v_r&=\boldsymbol v_{r-1}+\lambda\boldsymbol v_r.
\end{aligned}
$$

矩阵第 $j$ 列记录 $T\boldsymbol v_j$ 的坐标，因此在有序基 $(\boldsymbol v_1,\ldots,\boldsymbol v_r)$ 下为

$$
J_r(\lambda)
=
\begin{bmatrix}
\lambda&1&0&\cdots&0\\
0&\lambda&1&\ddots&\vdots\\
\vdots&\ddots&\ddots&\ddots&0\\
0&\cdots&0&\lambda&1\\
0&\cdots&\cdots&0&\lambda
\end{bmatrix}.
$$

### 6. 从主分解到 Jordan 形式

假设特征多项式在 $\mathbb F$ 上分裂，特征值为 $\lambda_1,\ldots,\lambda_q$。

**第一步：广义特征空间直和分解。**

主分解定理给出

$$
V
=
G_{\lambda_1}(T)
\oplus\cdots\oplus
G_{\lambda_q}(T).
$$

每个分量都对 $T$ 不变。

**第二步：去掉标量部分。**

在 $G_{\lambda_j}(T)$ 上定义

$$
N_j=(T-\lambda_jI)|_{G_{\lambda_j}(T)}.
$$

由广义特征空间定义，某个幂 $N_j^{s_j}=0$，所以 $N_j$ 幂零，并且

$$
T|_{G_{\lambda_j}}
=
\lambda_jI+N_j.
$$

**第三步：对每个幂零部分构造链基。**

幂零算子的 Jordan 基定理说明：每个 $G_{\lambda_j}$ 都有一组由 $N_j$-链组成的基。

**第四步：把幂零链转换为 $T$ 的 Jordan 块。**

若

$$
N_j\boldsymbol v_1=0,
\qquad
N_j\boldsymbol v_{\ell+1}=\boldsymbol v_\ell,
$$

则

$$
T\boldsymbol v_1=\lambda_j\boldsymbol v_1,
\qquad
T\boldsymbol v_{\ell+1}=\boldsymbol v_\ell+\lambda_j\boldsymbol v_{\ell+1}.
$$

所以这条链对应 $J_r(\lambda_j)$。

**第五步：合并所有基。**

由于广义特征空间之和是直和，各空间的基合并后成为 $V$ 的基；在该基下，不同空间不互相耦合，所以矩阵是所有 Jordan 块的块对角矩阵。

分裂条件用在第一步：若特征多项式不在当前域上分裂，就不能按所有一次因子 $t-\lambda_j$ 完成这种分解。

### 7. 核空间维数公式

先看一个大小为 $r_i$ 的块。其幂零部分 $N_i$ 满足

$$
N_i\boldsymbol e_j
=
\begin{cases}
0,&j=1,\\
\boldsymbol e_{j-1},&j\ge2.
\end{cases}
$$

作用 $k$ 次后，前 $k$ 个基向量被消去；若 $k\ge r_i$，全部被消去。因此

$$
\dim\ker N_i^k=\min(k,r_i).
$$

块对角矩阵的零空间是各块零空间的直和，所以

$$
\boxed{
d_k
=
\sum_{i=1}^{b}\min(k,r_i)
}.
$$

求一阶差分：

$$
\begin{aligned}
d_k-d_{k-1}
&=
\sum_{i=1}^{b}
\bigl[\min(k,r_i)-\min(k-1,r_i)\bigr].
\end{aligned}
$$

括号内的量等于

$$
\begin{cases}
1,&r_i\ge k,\\
0,&r_i<k.
\end{cases}
$$

所以

$$
\boxed{
d_k-d_{k-1}
=
\#\{i:r_i\ge k\}
}.
$$

### 8. 唯一性与三个不变量

定义

$$
\Delta_k=d_k-d_{k-1}.
$$

大小恰好为 $k$ 的块数是

$$
\Delta_k-\Delta_{k+1},
$$

因为 $\Delta_k$ 统计大小至少为 $k$ 的块，而 $\Delta_{k+1}$ 统计仍能达到下一层的块。故 $d_k$ 序列唯一决定每一种块大小的数量，Jordan 块除排列外唯一。

代数重数方面，所有对应块对特征多项式贡献

$$
(t-\lambda)^{r_1}\cdots(t-\lambda)^{r_b}
=(t-\lambda)^{\sum_i r_i},
$$

所以

$$
a_\lambda=\sum_i r_i.
$$

几何重数方面，每个块的幂零部分只有一个核方向，所以

$$
g_\lambda=b.
$$

最小多项式必须消去所有块。大小为 $r_i$ 的块需要因子 $(t-\lambda)^{r_i}$；同时消去所有块只需要最大指数，因此

$$
s_\lambda=\max_i r_i.
$$

## D. 边界、反例与纠错

## LA-JORD-D01

### 1. 重复特征值是否必有非平凡块

**错误。**

反例：

$$
\boldsymbol A=2I_2.
$$

其特征多项式是 $(t-2)^2$，但特征空间是整个 $\mathbb R^2$，Jordan 形式为

$$
J_1(2)\oplus J_1(2).
$$

断裂点：重复根只确定代数重数，不决定几何重数。最小修正：当 $g_\lambda<a_\lambda$ 时，至少存在一个非平凡 Jordan 块。

### 2. $a_\lambda,g_\lambda$ 是否决定全部块

**错误。**

比较

$$
J_3(0)\oplus J_1(0)
$$

与

$$
J_2(0)\oplus J_2(0).
$$

二者都有

$$
a_0=4,
\qquad
g_0=2,
$$

但块划分分别为 $3+1$ 与 $2+2$。前者最小多项式为 $t^3$，后者为 $t^2$。

断裂点：总大小与块数量不能唯一确定整数分拆。最小修正：加入所有核空间维数 $d_k$ 后可以唯一恢复。

### 3. 唯一实特征值为零是否推出幂零

**错误。**

取

$$
\boldsymbol A
=
\begin{bmatrix}
0&0&0\\
0&0&-1\\
0&1&0
\end{bmatrix}
=
[0]\oplus
\begin{bmatrix}0&-1\\1&0\end{bmatrix}.
$$

它唯一的实特征值是 $0$，但另外两个复特征值是 $\pm i$，因此不幂零；事实上旋转块的平方是 $-I_2$。

断裂点：“只看实特征值”遗漏了特征多项式不在 $\mathbb R$ 上分裂。最小修正：若特征多项式在当前域上分裂，且所有特征值都是零，则由 Cayley–Hamilton 得到幂零。

### 4. 谱位于闭单位圆是否保证幂有界

**错误。**

反例：

$$
J_2(1)^k
=
\begin{bmatrix}1&k\\0&1\end{bmatrix}.
$$

所有特征值都等于 $1$，但矩阵幂线性增长。

断裂点：谱位置只给出指数因子，没有记录 Jordan 多项式因子。最小修正：再要求单位圆上的所有 Jordan 块均为 $1\times1$。

### 5. Jordan 与 Schur 的数值稳定性

**错误。**

Jordan 分解写成

$$
\boldsymbol A
=
\boldsymbol P\boldsymbol J\boldsymbol P^{-1},
$$

其中 $\boldsymbol P$ 可能病态，且块大小会在任意小扰动下跳变。Schur 分解写成

$$
\boldsymbol A
=
\boldsymbol Q\boldsymbol T\boldsymbol Q^*,
$$

其中 $\boldsymbol Q$ 酉/正交，条件数为 $1$。LAPACK 的一般特征值流程计算 Schur 形式，而不是 Jordan 形式。

断裂点：代数分类的“规范”不等于数值映射的“连续稳定”。

### 6. 三阶广义特征向量的二次作用

**错误。**

“三阶”表示最小消去指数是 $3$，所以必须满足

$$
(\boldsymbol A-\lambda I)^3\boldsymbol v=0,
$$

但

$$
(\boldsymbol A-\lambda I)^2\boldsymbol v\ne0.
$$

题中结论若成立，阶至多为 $2$。

### 7. 相同特征多项式和最小多项式是否保证相似

**错误。**

比较两个六阶幂零矩阵：

$$
\boldsymbol A
=J_3(0)\oplus J_3(0),
$$

$$
\boldsymbol B
=J_3(0)\oplus J_2(0)\oplus J_1(0).
$$

二者的特征多项式都是

$$
t^6,
$$

最大块大小都是 $3$，所以最小多项式都是

$$
t^3.
$$

但

$$
\dim\ker\boldsymbol A=2,
\qquad
\dim\ker\boldsymbol B=3,
$$

即几何重数不同，故不相似。

断裂点：特征多项式只看总大小，最小多项式只看最大大小；二者都不记录中间块的数量与分布。

### 8. 实对称矩阵能否形成非平凡块

**错误。**

实对称矩阵由谱定理正交对角化，所以所有 Jordan 块都是 $1\times1$。重复特征值只扩大特征空间，不产生链式缺陷。

断裂点：忽略了对称/正规结构提供的正交特征基。

### 9. `eig` 的特征向量梯度是否总有限唯一

**错误。**

重复特征值对应的特征向量基不唯一；接近重复时，特征向量对扰动高度敏感。PyTorch 官方文档明确警告：依赖特征向量的梯度只在特征值互异时保证有限，间距接近零时会数值不稳定。

最小修正：若目标依赖单个一般矩阵特征向量，需要互异谱、足够间隔及规范化/相位不变目标；若只依赖对称矩阵或子空间，应使用相应结构化接口和子空间级目标。

### D 题反例索引

| 被否定的缺条件结论 | 最小对象 | 缺失条件/信息 |
|---|---|---|
| 重根必缺陷 | $2I_2$ | 几何重数 |
| $a,g$ 决定块 | $3+1$ 对 $2+2$ | 核增长/最大块 |
| 只有实零特征值就幂零 | $0\oplus R_{90^\circ}$ | 特征多项式分裂 |
| 闭单位圆保证幂有界 | $J_2(1)$ | 单位圆块必须平凡 |
| $p,m$ 决定相似类 | $3+3$ 对 $3+2+1$ | 全部块分布 |

## E. AI 迁移

## AI-JORD-E01

### 1. 相同谱，不同结构

两个矩阵的特征多项式都是

$$
p(t)=(t-1)^2,
$$

所以唯一特征值都是 $1$，代数重数都是 $2$，谱半径都是

$$
\rho=1.
$$

但

$$
\boldsymbol A_1-I=0,
$$

故

$$
g_1(\boldsymbol A_1)=2
$$

且 Jordan 块是 $J_1(1)\oplus J_1(1)$。

另一方面，

$$
\boldsymbol A_2-I
=
\begin{bmatrix}0&1\\0&0\end{bmatrix},
$$

其核为 $\operatorname{span}\{\boldsymbol e_1\}$，所以

$$
g_1(\boldsymbol A_2)=1
$$

且整体是一个 $J_2(1)$。

### 2. 前向状态

对 $\boldsymbol A_1$：

$$
\boldsymbol A_1^k=I,
$$

所以

$$
\boxed{
\boldsymbol h_k^{(1)}
=
\begin{bmatrix}0\\1\end{bmatrix}
}.
$$

对 $\boldsymbol A_2=I+N$，$N^2=0$，所以

$$
\boldsymbol A_2^k=I+kN
=
\begin{bmatrix}1&k\\0&1\end{bmatrix}.
$$

因此

$$
\boxed{
\boldsymbol h_k^{(2)}
=
\begin{bmatrix}k\\1\end{bmatrix}
}.
$$

二者谱半径相同，但一个状态恒定，另一个线性增长。谱半径只记录指数尺度 $|\lambda|^k$；非平凡 Jordan 块还产生组合数/多项式因子。

### 3. 对初始状态的梯度

因为

$$
\boldsymbol h_K=\boldsymbol A^K\boldsymbol h_0,
$$

且

$$
L=\frac12\boldsymbol h_K^{\mathsf T}\boldsymbol h_K,
$$

链式法则给出

$$
\nabla_{\boldsymbol h_K}L=\boldsymbol h_K,
$$

$$
\boxed{
\nabla_{\boldsymbol h_0}L
=(\boldsymbol A^K)^{\mathsf T}\boldsymbol h_K
}.
$$

对 $\boldsymbol A_1$：

$$
\boldsymbol A_1^K=I,
\qquad
\boldsymbol h_K^{(1)}=\begin{bmatrix}0\\1\end{bmatrix},
$$

所以

$$
\boxed{
\nabla_{\boldsymbol h_0}L
=
\begin{bmatrix}0\\1\end{bmatrix}
}.
$$

对 $\boldsymbol A_2$：

$$
\boldsymbol A_2^K
=
\begin{bmatrix}1&K\\0&1\end{bmatrix},
\qquad
\boldsymbol h_K^{(2)}
=
\begin{bmatrix}K\\1\end{bmatrix}.
$$

因此

$$
\begin{aligned}
\nabla_{\boldsymbol h_0}L
&=
\begin{bmatrix}1&0\\K&1\end{bmatrix}
\begin{bmatrix}K\\1\end{bmatrix}\\
&=
\boxed{
\begin{bmatrix}K\\K^2+1\end{bmatrix}
}.
\end{aligned}
$$

前向状态范数是 $O(K)$，而该损失对初始状态的梯度范数是 $O(K^2)$。额外一次 $\boldsymbol A^{K\mathsf T}$ 传播又引入一个线性因子。

> [!important] 不能过度外推
> 这是共享、线性、常系数状态转移的精确结论。一般神经网络的 Jacobian 随层和数据变化，梯度行为不能仅由单个 Jordan 块决定；这个例子用于隔离一种机制。

### 4. 小扰动与平方根谱分裂

把 $\boldsymbol A_\varepsilon$ 看成 $\boldsymbol A_2$ 的扰动：

$$
\boldsymbol A_\varepsilon
=
\boldsymbol A_2
+
\begin{bmatrix}0&0\\\varepsilon&0\end{bmatrix}.
$$

在二范数下，扰动大小是 $\varepsilon$。特征多项式为

$$
\begin{aligned}
p_\varepsilon(t)
&=
\det
\begin{bmatrix}
t-1&-1\\
-\varepsilon&t-1
\end{bmatrix}\\
&=(t-1)^2-\varepsilon.
\end{aligned}
$$

根是

$$
\boxed{
\lambda_\pm=1\pm\sqrt\varepsilon
}.
$$

两根间距为

$$
|\lambda_+-\lambda_-|
=2\sqrt\varepsilon.
$$

所以输入扰动是 $O(\varepsilon)$，谱分裂却是 $O(\sqrt\varepsilon)$。当 $\varepsilon\to0$ 时，分裂对扰动不呈线性 Lipschitz 响应，这是缺陷点病态性的明确信号。

### 5. 特征向量基趋于病态

令

$$
s=\sqrt\varepsilon.
$$

对 $\lambda_+=1+s$，可取

$$
\boldsymbol v_+
=
\begin{bmatrix}1\\s\end{bmatrix};
$$

对 $\lambda_-=1-s$，可取

$$
\boldsymbol v_-
=
\begin{bmatrix}1\\-s\end{bmatrix}.
$$

验证第一条：

$$
\boldsymbol A_\varepsilon
\begin{bmatrix}1\\s\end{bmatrix}
=
\begin{bmatrix}1+s\\\varepsilon+s\end{bmatrix}
=
\begin{bmatrix}1+s\\s^2+s\end{bmatrix}
=(1+s)
\begin{bmatrix}1\\s\end{bmatrix}.
$$

另一条同理。

特征向量矩阵为

$$
\boldsymbol P_\varepsilon
=
\begin{bmatrix}
1&1\\
s&-s
\end{bmatrix}.
$$

其行列式

$$
\det\boldsymbol P_\varepsilon=-2s=-2\sqrt\varepsilon
$$

趋于零。更精确地，

$$
\boldsymbol P_\varepsilon
\boldsymbol P_\varepsilon^{\mathsf T}
=
\begin{bmatrix}2&0\\0&2s^2\end{bmatrix},
$$

所以奇异值为 $\sqrt2$ 与 $\sqrt2s$，当 $0<s\le1$ 时

$$
\boxed{
\kappa_2(\boldsymbol P_\varepsilon)
=\frac1s
=\frac1{\sqrt\varepsilon}
}.
$$

两个特征向量都趋向 $[1,0]^{\mathsf T}$，特征基趋于共线。虽然每个 $\varepsilon>0$ 时矩阵都可对角化，但对角化越来越病态。

### 6. 能否从接近的数值特征值断言精确 Jordan 块

**不能。** 接近的数值特征值至少可能来自：

- 精确重根且可对角化；
- 精确缺陷 Jordan 块；
- 两个真正不同但很接近的特征值；
- 数据噪声、舍入误差或迭代算法误差；
- 一个高度非正规的近缺陷矩阵。

可执行诊断清单：

1. **报告残差**：检查
   $$
   \|\boldsymbol A\boldsymbol v_i-\widehat\lambda_i\boldsymbol v_i\|
   $$
   而不只报告特征值。
2. **检查精度与尺度**：记录 dtype、矩阵范数、平衡处理及算法容差。
3. **查看 Schur 形式/不变子空间**：对聚簇谱报告相应 Schur 子空间，而不是强行解释单个向量。
4. **检查特征向量条件性**：查看特征向量矩阵的条件数、左右特征向量夹角或软件提供的 condition estimate。
5. **做扰动试验**：在与数据误差相称的尺度加入多次小扰动，观察谱簇和子空间是否稳定。
6. **多阈值检查 rank**：若输入是精确/高精度问题，可比较
   $$
   \sigma_i(\boldsymbol A-\lambda I),
   \quad
   \sigma_i((\boldsymbol A-\lambda I)^2)
   $$
   在多个阈值下的判定；不能隐藏容差。
7. **利用已知结构**：若矩阵理论上对称/Hermitian，应先检查并投影到该结构，再用 `eigh`；对称矩阵不会有非平凡 Jordan 块。
8. **区分符号输入与测量输入**：整数/有理符号矩阵可以精确讨论 Jordan 块；带噪浮点权重通常只能讨论“接近缺陷”和相应条件性。

### 7. 应报告什么对象

若任务是在更大系统中稳定跟踪一个二维近重复谱簇，应优先报告**Schur 不变子空间**及其残差、谱区间和间隔，而不是：

- 宣称一个不稳定的精确 Jordan 块；
- 或把任意选择的单个特征向量当成稳定语义方向。

理由：

1. Schur 向量来自正交/酉变换，换基不放大范数；
2. 谱簇内部的基可能旋转，但整个不变子空间可以比单个向量稳定；
3. 可把相邻特征值排序到同一 Schur 块，保留上三角耦合信息；
4. 它与 LAPACK 等标准数值流程一致。

仍需说明的局限：

- 若该谱簇与其余谱没有间隔，连整个子空间也可能不稳定；
- 有限样本权重和训练噪声会使“精确不变”只近似成立；
- 二维示例中整个空间本身当然是不变的，实际价值出现在更大矩阵中选取一个谱簇对应的子空间；
- Schur 形式不会自动给出唯一可解释方向，仍需结合任务定义。

### E 题结论表

| 观察 | 精确数学机制 | 工程含义 |
|---|---|---|
| 相同谱半径却不同前向增长 | $J_2(1)^k=I+kN$ | 不能只监控谱半径 |
| 梯度达到 $O(K^2)$ | 前向与伴随传播各含链因子 | 长时共享状态转移需检查非正规瞬态 |
| $O(\varepsilon)$ 扰动产生 $O(\sqrt\varepsilon)$ 分裂 | 缺陷重根的平方根响应 | 接近 Jordan 点时 eig 病态 |
| 特征向量基条件数 $1/\sqrt\varepsilon$ | 两列趋于共线 | 不要给单个向量过度语义解释 |
| Schur 子空间优先 | 酉/正交换基 | 聚簇谱的更稳健报告单位 |

## 最终复盘

若本组题仍有错误，按结构回链：

| 错误类型 | 回看位置 |
|---|---|
| 混淆广义向量的阶 | [[广义特征向量与 Jordan 结构#一、广义特征向量]] |
| 不会证明核空间稳定 | [[广义特征向量与 Jordan 结构#二、核空间增长链]] |
| 不会从 $d_k$ 恢复块 | [[广义特征向量与 Jordan 结构#九、怎样从核空间增长恢复 Jordan 块]] |
| 混淆 $a,g,m_A$ | [[广义特征向量与 Jordan 结构#9.4 三个最重要的读块规则]] |
| 不会求矩阵幂/指数 | [[广义特征向量与 Jordan 结构#十二、Jordan 块的矩阵幂]]、[[广义特征向量与 Jordan 结构#十三、矩阵指数与一般矩阵函数]] |
| 把理论 Jordan 当数值算法 | [[广义特征向量与 Jordan 结构#十五、为什么 Jordan 形式数值不稳定]] |
| 只看谱半径解释状态/梯度 | [[广义特征向量与 Jordan 结构#十七、AI 中的直接连接]] |

建议在 24 小时后不看答案重做 B7–B9、C5–C8 与 E2–E7；能独立写出公式、条件和工程边界，才算形成了可迁移掌握。
