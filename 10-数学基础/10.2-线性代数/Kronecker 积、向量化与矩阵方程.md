---
type: concept
status: draft
area: [math/linear-algebra, math/matrix-analysis, math/matrix-calculus, ai/optimization]
aliases: [Kronecker Product, vec 算子, Sylvester 方程, Lyapunov 方程, 矩阵方程]
prerequisites: ["[[线性映射]]", "[[基与坐标]]", "[[线性方程组、消元与 LU 分解]]"]
related: ["[[Schur 分解]]", "[[多线性映射、张量与缩并]]", "[[全微分与 Fréchet 导数]]", "[[Jacobian、JVP 与 VJP]]", "[[矩阵函数的 Fréchet 导数]]", "[[结构化矩阵与结构化扰动]]", "[[伴随算子]]", "[[矩阵分析 MOC]]", "[[线性代数 MOC]]"]
sources: ["Petersen-Pedersen-Matrix-Cookbook", "Kolda-Bader-2009", "SciPy-solve-sylvester", "PyTorch-kron"]
exercises: ["[[习题 - Kronecker 积、向量化与矩阵方程]]"]
solutions: ["[[解答 - Kronecker 积、向量化与矩阵方程]]"]
created: 2026-08-16
updated: 2026-08-27
---

# Kronecker 积、向量化与矩阵方程

> [!abstract] 本章主问题
> 怎样把作用在矩阵未知量两侧的线性映射，编码为普通向量空间中的一个线性系统，同时保留原有块结构？Kronecker 积把两个映射组合到张量积空间，`vec` 按固定列顺序重排矩阵坐标，并给出 $\operatorname{vec}(AXB)=(B^T\otimes A)\operatorname{vec}(X)$。这套语言统一矩阵方程、Jacobian、可分离协方差与 K-FAC，但推导中的巨型 Kronecker 矩阵通常不应在程序中显式形成。

> [!question] 初学者读完必须能回答
> 1. $A\otimes B$ 的块定义、指标定义和输出形状怎样相互对应？
> 2. Kronecker、外积、Hadamard 与普通矩阵乘法的指标规则有何不同？
> 3. `vec` 按列堆叠时，一个 $2\times2$ 矩阵的元素顺序是什么？
> 4. $\operatorname{vec}(AXB)$ 恒等式为何出现 $B^T\otimes A$，左右顺序怎样检查？
> 5. Sylvester/Lyapunov 方程怎样形式化为线性系统，唯一可解条件是什么？
> 6. 为什么理论上出现 $n^2\times n^2$ 系数矩阵，实际算法却应利用 Schur/三角结构？
> 7. 可分离协方差、K-FAC 与矩阵 Jacobian 怎样复用这套索引语言？

![[00-知识库管理/_assets/figures/kron-vec/fig-kron-vec-sylvester-structure-v2.svg|880]]

> [!figure] 图 1　块积、列向量化与结构化矩阵方程
> 左栏按块展示 $A\otimes B$，中栏固定 `vec` 的列堆叠顺序并写出双边乘法恒等式，右栏把 Sylvester 方程形式化为大线性系统，同时强调实际 Schur 求解不物化巨型系数矩阵。**来源：**依据 Matrix Cookbook、Kolda–Bader 与 SciPy Sylvester 接口独立绘制。

**怎样读图。** 先从左栏做形状乘法：$m\times n$ 与 $p\times q$ 产生 $mp\times nq$。再逐元素检查中栏 `vec` 顺序，只有约定固定后转置位置才有意义。最后看右栏，展开公式用于证明唯一性和导数结构；实际计算保留矩阵形状，先做 Schur/三角化再解 Sylvester 子问题。

**适用边界（图没有证明什么）。** 图使用按列堆叠约定；行优先展平会改变排列矩阵和恒等式外观。Kronecker 表示能够把矩阵方程化为普通线性系统，却不意味着显式构造该系统在内存、复杂度或条件性上合理。

## 进入正文前：矩阵未知量也是一个向量空间中的未知量

> [!info] 承接—中心—去路
> - **承接：** [[伴随算子]]得到矩阵参数梯度 $G_A=g_yx^T$，但它仍以二维数组出现；[[线性方程组、消元与 LU 分解]]只直接处理向量未知量的线性系统。
> - **中心：** `vec` 为矩阵空间选择一套坐标顺序，Kronecker 积表示“同时作用于行轴与列轴”的组合映射，于是矩阵方程可以暂时翻译成普通线性系统。
> - **去路：** [[多线性映射、张量与缩并]]会去掉对二维矩阵的限制，用自由指标和求和指标直接描述高阶数组；数值算法则尽量保留原矩阵结构，而不是物化巨大 Kronecker 矩阵。

### 两遍阅读路线

第一遍固定 column-major `vec`，掌握 Kronecker 形状、四种乘积的区别和 $\operatorname{vec}(AXB)$ 恒等式。第二遍再读交换矩阵、Sylvester/Lyapunov 方程、谱唯一性、K-FAC、条件性与不物化原则。

全章主线是：

$$
X\in\mathbb F^{p\times q}
\xrightarrow{\operatorname{vec}}
\operatorname{vec}(X)\in\mathbb F^{pq},
\qquad
X\mapsto AXB
\longleftrightarrow
\operatorname{vec}(X)\mapsto(B^T\otimes A)\operatorname{vec}(X).
$$

### 本章的问题链

1. 矩阵空间怎样在固定基与元素顺序后变成普通坐标空间？
2. Kronecker、外积、Hadamard 和矩阵乘法各自保留或缩并哪些指标？
3. 为什么 column-major `vec` 使右乘 $B$ 对应第一个因子 $B^T$？
4. 怎样用 shape 与指标两种检查独立验证 vec 恒等式？
5. 矩阵方程何时唯一可解，为什么理论表示和实际算法不同？
6. K-FAC 和矩阵 Jacobian 为什么能利用 Kronecker 结构而不形成稠密大矩阵？

### 贯穿例：把上一页的参数梯度展开成一个向量

上一页得到

$$
w=e_3,
\qquad
\hat x=(-1/3,2/3)^T,
\qquad
G_A=w\hat x^T
=
\begin{bmatrix}
0&0\\
0&0\\
-1/3&2/3
\end{bmatrix}.
$$

按列堆叠，

$$
\operatorname{vec}(G_A)
=
\begin{bmatrix}
0\\0\\-1/3\\0\\0\\2/3
\end{bmatrix}
=\hat x\otimes w.
$$

最后一个等号是 rank-one 外积与 Kronecker 向量之间的坐标桥：先列出 $\hat x_1w$，再列出 $\hat x_2w$。如果改用 row-major flatten，数字顺序会改变，公式也必须随之改变。

再把参数矩阵换成一般未知量 $X$。若线性算子为

$$
\mathcal L(X)=AXB,
$$

那么固定 `vec` 后，$\mathcal L$ 的表示矩阵就是 $B^T\otimes A$。这里的价值是揭示结构、唯一性与导数；若 $X$ 很大，实际求解仍应调用矩阵方程算法。

### 最小索引账本

| 对象 | 形状 | 坐标长度/结果 |
|---|---:|---:|
| $X$ | $p\times q$ | $pq$ 个自由坐标 |
| $\operatorname{vec}(X)$ | $pq\times1$ | 按列堆叠 |
| $A$ | $m\times p$ | 作用于行轴 |
| $B$ | $q\times n$ | 作用于列轴 |
| $B^T\otimes A$ | $mn\times pq$ | $X\mapsto AXB$ 的坐标矩阵 |
| $AXB$ | $m\times n$ | `vec` 后长度 $mn$ |

> [!tip] 初学者的停靠点
> 若公式中的 $B^T\otimes A$ 只能靠背诵，先停下来手写一个 $2\times2$ 的 $X$，按列标出四个位置，再检查左乘混合行、右乘混合列。顺序约定没有固定之前，不进入 Sylvester 方程。

## 学习目标

完成本章后，应能：

1. 从块矩阵和指标两种角度定义 $A\otimes B$ 并计算形状；
2. 区分 Kronecker 积、外积、Hadamard 积与普通矩阵乘法；
3. 证明混合乘积、转置、逆、秩、谱和范数性质；
4. 按列堆叠定义 $\operatorname{vec}$ 并手算矩阵向量化；
5. 完整证明
   $$
   \operatorname{vec}(AXB)=(B^T\otimes A)\operatorname{vec}(X);
   $$
6. 用交换矩阵处理转置和不同排列；
7. 把 Sylvester、Lyapunov 和双边矩阵方程改写为线性系统；
8. 判断矩阵方程唯一可解的谱条件；
9. 把 `vec` 恒等式迁移到 Jacobian、VJP/JVP、可分离协方差与 K-FAC；
10. 解释为什么理论上的 Kronecker 系数矩阵通常不应在代码中显式形成。

## 阅读前检查与约定

需要熟悉：

- [[线性映射]]与矩阵表示；
- [[基与坐标]]与坐标顺序；
- [[线性方程组、消元与 LU 分解]]；
- [[Schur 分解]]只在后半部分的结构化 Sylvester 数值算法中使用；若尚未学习，可先完成 Kronecker、`vec` 与恒等式主线；
- 矩阵形状、转置和迹。

本章最重要的约定是：

> [!important] `vec` 一律按列堆叠
> 对 $X=[x_1,\ldots,x_n]\in\mathbb F^{m\times n}$，
> $$
> \operatorname{vec}(X)
> =\begin{bmatrix}x_1\\x_2\\\vdots\\x_n\end{bmatrix}
> \in\mathbb F^{mn}.
> $$

所有公式都依赖这个顺序。若软件默认按行展平，必须转换顺序或重新推导公式。

## 一、Kronecker 积的块定义

设

$$
A=[a_{ij}]\in\mathbb F^{m\times n},
\qquad
B\in\mathbb F^{p\times q}.
$$

> [!definition] Kronecker 积
> $$
> A\otimes B
> =
> \begin{bmatrix}
> a_{11}B&\cdots&a_{1n}B\\
> \vdots&\ddots&\vdots\\
> a_{m1}B&\cdots&a_{mn}B
> \end{bmatrix}
> \in\mathbb F^{mp\times nq}.
> $$

每个标量 $a_{ij}$ 被替换成一个 $p\times q$ 块 $a_{ij}B$。所以形状规则是

$$
(m\times n)\otimes(p\times q)
\longrightarrow(mp)\times(nq).
$$

### 1.1 完整手算

取

$$
A=\begin{bmatrix}1&2\\3&4\end{bmatrix},
\qquad
B=\begin{bmatrix}1&0\\0&-1\end{bmatrix}.
$$

则

$$
A\otimes B
=\begin{bmatrix}
B&2B\\
3B&4B
\end{bmatrix}
=\begin{bmatrix}
1&0&2&0\\
0&-1&0&-2\\
3&0&4&0\\
0&-3&0&-4
\end{bmatrix}.
$$

### 1.2 指标定义

若使用零起始索引，则

$$
(A\otimes B)_{ip+r,\,jq+s}
=a_{ij}b_{rs},
$$

其中

$$
0\le i<m,
\quad
0\le j<n,
\quad
0\le r<p,
\quad
0\le s<q.
$$

这说明行索引实际上是二元索引 $(i,r)$ 的编码，列索引是 $(j,s)$ 的编码。

## 二、四种“乘积”必须区分

| 运算 | 典型输入 | 输出形状 | 核心含义 |
|---|---|---|---|
| 矩阵乘法 $AB$ | $m\times n$ 与 $n\times q$ | $m\times q$ | 对共享指标求和 |
| Hadamard 积 $A\odot B$ | 相同形状 | 相同形状 | 对应元素相乘，不求和 |
| 外积 $uv^T$ | $u\in\mathbb F^m,v\in\mathbb F^n$ | $m\times n$ | 构造 rank-$1$ 矩阵 |
| Kronecker 积 $A\otimes B$ | 任意矩阵 | $(mp)\times(nq)$ | 块替换/张量积映射 |

它们偶尔产生相同数字，但对象和索引规则不同。

例如 $u\otimes v$ 对两个向量通常被实现为长度 $mn$ 的 Kronecker 向量；$uv^T$ 是 $m\times n$ 矩阵。二者在选定 `vec` 顺序后可以互相重排，但不应因此把概念混为一谈。

## 三、Kronecker 积为什么表示组合映射

设

$$
A:V\to V',
\qquad
B:W\to W'.
$$

在张量积空间上定义

$$
(A\otimes B)(v\otimes w)
=(Av)\otimes(Bw),
$$

再线性延拓到 $V\otimes W$。选定积基后，这个映射的矩阵正是块形式 $A\otimes B$。

因此 Kronecker 积不是为了制造大矩阵而发明的记号；它是“两个映射分别作用在两个因子空间上”的坐标表示。

## 四、核心代数性质

设所有乘法形状兼容。

### 4.1 双线性与结合性

$$
(A+C)\otimes B=A\otimes B+C\otimes B,
$$

$$
A\otimes(B+D)=A\otimes B+A\otimes D,
$$

$$
(\alpha A)\otimes B
=A\otimes(\alpha B)
=\alpha(A\otimes B),
$$

$$
(A\otimes B)\otimes C
=A\otimes(B\otimes C).
$$

最后一式在自然索引识别下成立；具体数组轴顺序仍需写清。

### 4.2 混合乘积性质

若 $AC$ 与 $BD$ 可乘，则

$$
\boxed{
(A\otimes B)(C\otimes D)
=(AC)\otimes(BD).
}
$$

对简单张量 $x\otimes y$，

$$
\begin{aligned}
(A\otimes B)(C\otimes D)(x\otimes y)
&=(A\otimes B)(Cx\otimes Dy)\\
&=ACx\otimes BDy\\
&=((AC)\otimes(BD))(x\otimes y).
\end{aligned}
$$

简单张量张成整个张量积空间，所以两个线性映射相同。

### 4.3 转置、伴随与逆

$$
(A\otimes B)^T=A^T\otimes B^T,
$$

$$
(A\otimes B)^*=A^*\otimes B^*.
$$

若 $A,B$ 可逆，则

$$
(A\otimes B)^{-1}=A^{-1}\otimes B^{-1},
$$

因为混合乘积给出

$$
(A\otimes B)(A^{-1}\otimes B^{-1})=I\otimes I=I.
$$

### 4.4 秩、范数与条件数

$$
\operatorname{rank}(A\otimes B)
=\operatorname{rank}(A)\operatorname{rank}(B).
$$

奇异值是两两乘积

$$
\{\sigma_i(A)\sigma_j(B)\}_{i,j},
$$

所以

$$
\|A\otimes B\|_2
=\|A\|_2\|B\|_2,
$$

$$
\|A\otimes B\|_F
=\|A\|_F\|B\|_F.
$$

若 $A,B$ 都可逆，

$$
\kappa_2(A\otimes B)
=\kappa_2(A)\kappa_2(B).
$$

因此两个中等病态因子组合后可能非常病态。

### 4.5 特征值与行列式

若 $A\in\mathbb C^{n\times n}$、$B\in\mathbb C^{m\times m}$，且

$$
Au_i=\lambda_i u_i,
\qquad
Bv_j=\mu_jv_j,
$$

则

$$
(A\otimes B)(u_i\otimes v_j)
=\lambda_i\mu_j(u_i\otimes v_j).
$$

所以谱由两两乘积构成。行列式为

$$
\det(A\otimes B)
=\det(A)^m\det(B)^n.
$$

> [!warning] 一般不交换
> 通常 $A\otimes B\ne B\otimes A$。二者可以通过置换矩阵相似/等价地重新排列，但不能直接删去顺序。

## 五、`vec` 算子与列优先顺序

设

$$
X=
\begin{bmatrix}
1&2&3\\
4&5&6
\end{bmatrix}.
$$

按列堆叠：

$$
\operatorname{vec}(X)
=\begin{bmatrix}
1\\4\\2\\5\\3\\6
\end{bmatrix}.
$$

这与许多 C/Python 数组的默认 row-major flatten

$$
[1,2,3,4,5,6]^T
$$

不同。

### 5.1 `vec` 是线性同构

$$
\operatorname{vec}(\alpha X+\beta Y)
=\alpha\operatorname{vec}(X)+\beta\operatorname{vec}(Y).
$$

它把 $\mathbb F^{m\times n}$ 与 $\mathbb F^{mn}$ 线性同构，只改变坐标组织，不丢失信息。

### 5.2 Frobenius 内积变成普通内积

$$
\langle X,Y\rangle_F
=\operatorname{tr}(X^*Y)
=\operatorname{vec}(X)^*\operatorname{vec}(Y).
$$

因此

$$
\|X\|_F=\|\operatorname{vec}(X)\|_2.
$$

## 六、全章关键恒等式

设

$$
A\in\mathbb F^{m\times p},
\quad
X\in\mathbb F^{p\times q},
\quad
B\in\mathbb F^{q\times n}.
$$

那么 $AXB\in\mathbb F^{m\times n}$，并且

> [!theorem] vec–Kronecker 恒等式
> $$
> \boxed{
> \operatorname{vec}(AXB)
> =(B^T\otimes A)\operatorname{vec}(X).
> }
> $$

> [!analysis] vec–Kronecker 恒等式的七问拆解
> | 问题 | 回答 |
> |---|---|
> | 它把什么问题线性化？ | 把矩阵未知量上的双边线性作用 $X\mapsto AXB$ 写成普通坐标向量上的矩阵乘法。 |
> | 每个对象的形状是什么？ | $A:m\times p$、$X:p\times q$、$B:q\times n$；因此 $B^T\otimes A$ 为 $mn\times pq$，输入/输出 vec 长度为 $pq/mn$。 |
> | 为什么采用 $B^T\otimes A$ 的顺序？ | column-major `vec` 先完整堆叠每一列；左乘 $A$ 在每个列块内部作用，右乘 $B$ 在列块之间混合，故分别落在第二/第一 Kronecker 因子。 |
> | 转置从哪里来？ | 输出第 $j$ 列使用系数 $b_{sj}$ 混合输入第 $s$ 列，而 $B^T$ 的 $(j,s)$ 元正是 $b_{sj}$。 |
> | 怎样做最小验算？ | 取 $A=I$ 或 $B=I$ 得到两个特例，再用 $2\times2$ 矩阵逐列展开；只做 shape 检查不能排除顺序错误。 |
> | 约定改变会怎样？ | row-major flatten 会通过交换/排列矩阵改变公式外观；不能把不同库的 `reshape` 默认值静默混用。 |
> | 为什么理论上写出、工程上却常不构造？ | $n\times n$ 矩阵未知量会产生 $n^2\times n^2$ 系数矩阵；实际 Sylvester/Lyapunov 和 K-FAC 算法应利用分解、矩阵乘与结构化求解。 |

形状检查：

$$
B^T\otimes A
\in\mathbb F^{nm\times qp},
$$

$$
\operatorname{vec}(X)\in\mathbb F^{pq},
$$

输出长度 $mn$，与 $\operatorname{vec}(AXB)$ 一致。

> [!warning] 为什么是 $B^T$ 而不是 $B$
> 右乘 $B$ 组合的是 $X$ 的列；按列向量化后，列混合系数出现在 Kronecker 的第一个因子，并发生转置。只凭记忆很容易写错，必须做形状或指标检查。

## 七、vec 恒等式的指标证明

记

$$
Y=AXB.
$$

其元素为

$$
y_{ij}
=\sum_{r=1}^{p}\sum_{s=1}^{q}
a_{ir}x_{rs}b_{sj}.
$$

列向量化中，$y_{ij}$ 位于索引 $(j-1)m+i$；$x_{rs}$ 位于 $(s-1)p+r$。

而

$$
(B^T\otimes A)_{(j-1)m+i,\,(s-1)p+r}
=(B^T)_{js}A_{ir}
=b_{sj}a_{ir}.
$$

所以矩阵—向量乘的该分量为

$$
\sum_{s=1}^q\sum_{r=1}^p
b_{sj}a_{ir}x_{rs}
=y_{ij}.
$$

每个分量都相等，恒等式得证。

### 7.1 两个常用特例

左乘：

$$
\operatorname{vec}(AX)
=(I_q\otimes A)\operatorname{vec}(X).
$$

右乘：

$$
\operatorname{vec}(XB)
=(B^T\otimes I_p)\operatorname{vec}(X).
$$

若写成 $AXB^T$，则

$$
\operatorname{vec}(AXB^T)
=(B\otimes A)\operatorname{vec}(X).
$$

复数情形注意：公式本身使用普通转置。若原式是 $AXB^*$，则

$$
\operatorname{vec}(AXB^*)
=(\overline B\otimes A)\operatorname{vec}(X).
$$

## 八、交换矩阵与转置

对 $X\in\mathbb F^{m\times n}$，存在一个只含 $0,1$ 的置换矩阵

$$
K_{m,n}\in\mathbb R^{mn\times mn}
$$

使

$$
\boxed{
K_{m,n}\operatorname{vec}(X)
=\operatorname{vec}(X^T).
}
$$

$K_{m,n}$ 称为交换矩阵或 commutation matrix。它满足

$$
K_{m,n}^{-1}=K_{m,n}^T=K_{n,m}.
$$

并能表达 Kronecker 因子换序：

$$
K_{m,p}(A\otimes B)K_{q,n}
=B\otimes A,
$$

其中形状按 $A\in\mathbb F^{m\times n}$、$B\in\mathbb F^{p\times q}$ 匹配。

这说明 $A\otimes B$ 与 $B\otimes A$ 的差异可以是坐标排列，但排列矩阵不能凭空省略。

## 九、矩阵方程如何变成线性系统

### 9.1 双边方程 $AXB=C$

若未知量是 $X\in\mathbb F^{p\times q}$，则

$$
AXB=C
$$

等价于

$$
(B^T\otimes A)\operatorname{vec}(X)
=\operatorname{vec}(C).
$$

这把“矩阵未知量”转成普通向量未知量。

### 9.2 Sylvester 方程

标准 Sylvester 方程为

$$
AX+XB=C,
$$

其中

$$
A\in\mathbb F^{m\times m},
\quad
X,C\in\mathbb F^{m\times n},
\quad
B\in\mathbb F^{n\times n}.
$$

向量化得到

$$
\boxed{
\left(I_n\otimes A+B^T\otimes I_m\right)
\operatorname{vec}(X)
=\operatorname{vec}(C).
}
$$

系数矩阵大小为 $mn\times mn$。

> [!definition] Kronecker 和
> 常把
> $$
> A\oplus B^T
> =I_n\otimes A+B^T\otimes I_m
> $$
> 称为适配本方程约定的 Kronecker sum。

### 9.3 唯一可解条件

$I_n\otimes A$ 的特征值为 $\lambda_i(A)$，$B^T\otimes I_m$ 的特征值为 $\lambda_j(B)$。两项可交换，所以 Kronecker 和的特征值为

$$
\lambda_i(A)+\lambda_j(B).
$$

因此 Sylvester 方程对每个 $C$ 唯一可解，当且仅当

$$
\boxed{
\lambda_i(A)+\lambda_j(B)\ne0
\quad\text{对所有 }i,j.
}
$$

等价地，

$$
\operatorname{spec}(A)
\cap
\operatorname{spec}(-B)
=\varnothing.
$$

### 9.4 对角例子的完整求解

取

$$
A=\operatorname{diag}(1,2),
\qquad
B=\operatorname{diag}(3,4),
$$

$$
C=\begin{bmatrix}4&5\\6&7\end{bmatrix}.
$$

由于

$$
(AX+XB)_{ij}=(a_i+b_j)x_{ij},
$$

逐元素得到

$$
X=
\begin{bmatrix}
4/(1+3)&5/(1+4)\\
6/(2+3)&7/(2+4)
\end{bmatrix}
=\begin{bmatrix}
1&1\\
6/5&7/6
\end{bmatrix}.
$$

这个例子也直观显示唯一性分母 $a_i+b_j$。

## 十、Lyapunov 方程与稳定系统

连续 Lyapunov 方程常写成

$$
AX+XA^*=-Q.
$$

向量化后：

$$
\left(I\otimes A+\overline A\otimes I\right)
\operatorname{vec}(X)
=-\operatorname{vec}(Q).
$$

如果 $A$ 的全部特征值实部为负，则

$$
\lambda_i(A)+\overline{\lambda_j(A)}
$$

实部也为负，不会为零，因而解唯一。若 $Q\succ0$，在标准条件下解还具有正定性，并可表示为

$$
X=\int_0^\infty e^{tA}Qe^{tA^*}\,dt.
$$

验证：对积分内被积函数求导，

$$
\frac{d}{dt}
\left(e^{tA}Qe^{tA^*}\right)
=Ae^{tA}Qe^{tA^*}+e^{tA}Qe^{tA^*}A^*.
$$

从 $0$ 积到 $\infty$，稳定性使无穷端为零，得到 $AX+XA^*=-Q$。

## 十一、为什么实际算法不显式构造 Kronecker 系数

若 $X\in\mathbb R^{m\times n}$，Sylvester 的向量化系数是 $mn\times mn$，存储量为

$$
O(m^2n^2).
$$

当 $m=n=1000$ 时，未知量长度是一百万，而显式系数矩阵有 $10^{12}$ 个元素，完全不可行。

生产算法通常：

1. 对 $A,B$ 做 Schur 分解；
2. 把方程变换到三角/准三角坐标；
3. 通过块回代求解；
4. 再变换回原坐标。

这就是 Bartels–Stewart 类路线。`vec` 形式主要用于：

- 证明唯一性与条件性；
- 推导 Jacobian；
- 识别 Kronecker 结构；
- 设计矩阵自由的 matvec 或预条件器。

> [!warning] 表达式等价不等于算法等价
> 把矩阵方程写成普通线性系统是理论桥梁，不是建议调用通用稠密求解器处理巨型 Kronecker 矩阵。

## 十二、矩阵映射的 Jacobian

考虑线性矩阵映射

$$
F(X)=AXB.
$$

微扰 $H$ 满足

$$
F(X+H)-F(X)=AHB.
$$

向量化：

$$
\operatorname{vec}(AHB)
=(B^T\otimes A)\operatorname{vec}(H).
$$

所以在列 `vec` 坐标中，Jacobian 是

$$
\boxed{
J_F=B^T\otimes A.
}
$$

这不是额外定理，而是同一个线性映射的两种坐标表示。

### 12.1 双线性映射的微分

若

$$
F(A,X,B)=AXB,
$$

则一阶微分为

$$
dF=(dA)XB+A(dX)B+AX(dB).
$$

每一项再用 `vec` 恒等式，可得到对不同参数块的 Jacobian。矩阵微分中大量 Kronecker 公式都来自这一模式。

### 12.2 VJP 不需要显式 Jacobian

若上游 cotangent 为 $G$，Frobenius 内积给出

$$
\langle G,AHB\rangle_F
=\langle A^*GB^*,H\rangle_F.
$$

所以反向传播为

$$
\bar X=A^*GB^*.
$$

这等价于乘 $J_F^*$，但完全不需要构造 $B^T\otimes A$。自动微分系统通常利用这样的结构化 VJP/JVP。

## 十三、AI 中的直接接口

### 13.1 K-FAC 的形状来源

线性层

$$
y=Wx,
\qquad
W\in\mathbb R^{d_{out}\times d_{in}},
$$

设输出反向信号为 $\delta\in\mathbb R^{d_{out}}$。单样本权重梯度是

$$
G=\delta x^T.
$$

按列向量化：

$$
\operatorname{vec}(G)
=x\otimes\delta.
$$

其外积为

$$
\operatorname{vec}(G)\operatorname{vec}(G)^T
=(xx^T)\otimes(\delta\delta^T).
$$

Fisher/Gauss–Newton 块需要对样本取期望。K-FAC 的核心近似之一是把联合期望近似分解：

$$
\mathbb E[(xx^T)\otimes(\delta\delta^T)]
\approx
\mathbb E[xx^T]\otimes\mathbb E[\delta\delta^T].
$$

> [!warning] 这是近似，不是恒等式
> `vec` 与 Kronecker 关系是精确代数；把期望拆成两个因子的 Kronecker 积需要统计独立性或近似假设。

### 13.2 可分离协方差

若二维网格/矩阵变量的协方差近似为

$$
\Sigma\approx\Sigma_c\otimes\Sigma_r,
$$

则

$$
\log\det(\Sigma_c\otimes\Sigma_r)
=m\log\det\Sigma_c+n\log\det\Sigma_r
$$

（维数按因子调整），逆也可分解为因子逆的 Kronecker 积。这能大幅降低高斯模型和预条件器的存储与计算，但可分离性必须由数据验证。

### 13.3 可分离卷积与二维算子

二维离散算子常形如

$$
L=I\otimes L_x+L_y\otimes I,
$$

即 Kronecker 和。它对应分别沿两个轴作用，再把结果相加。可分离滤波也可通过先沿行、再沿列的两个小算子实现，而不形成整体大矩阵。

### 13.4 隐式层与矩阵方程

深度平衡模型、状态空间层和二阶优化中，反向传播可能需要求解 Sylvester/Lyapunov 型线性化方程。`vec` 形式解释 Jacobian 的谱与唯一性；实现应调用结构化求解器或矩阵自由迭代。

### 13.5 参数共享与 Kronecker 结构

当同一线性变换沿 token、空间位置或多轴重复作用时，整体算子常可写成 $I\otimes W$ 或若干 Kronecker 项之和。这是共享参数在大向量坐标中的精确表示。

## 十四、软件与存储顺序纪律

### 14.1 NumPy

NumPy 默认 `reshape(-1)`/`ravel()` 通常按 C-order（行优先）。本章列 `vec` 对应

```python
v = X.reshape(-1, order="F")
```

恢复矩阵也必须使用同一顺序。

### 14.2 PyTorch

PyTorch 的常规 contiguous 张量按 row-major 逻辑展平。要模拟本章二维列 `vec`，可显式转置后再连续化：

```python
v = X.transpose(0, 1).contiguous().reshape(-1)
```

批量/高阶张量还要先定义轴顺序，不能照抄二维技巧。

### 14.3 `torch.kron` 的高阶推广

当前 PyTorch `torch.kron` 会把两个输入补到相同阶数，并把对应轴长度相乘。这是矩阵 Kronecker 积的数组推广；它不等同于 `einsum` 的任意缩并，也不自动选择节省内存的实现。

### 14.4 不物化原则

若目标只是计算

$$
y=(B^T\otimes A)\operatorname{vec}(X),
$$

应改算

$$
Y=AXB
$$

再向量化。前者存储 $O(mnpq)$ 级系数，后者保留两个小矩阵乘法。

## 十五、条件性与误差边界

Sylvester 方程的唯一性只问

$$
\lambda_i(A)+\lambda_j(B)\ne0.
$$

但数值稳定性还问这些和离零有多远。定义 separation

$$
\operatorname{sep}(A,-B)
=\min_{X\ne0}
\frac{\|AX+XB\|_F}{\|X\|_F}.
$$

这正是向量化算子

$$
I\otimes A+B^T\otimes I
$$

的最小奇异值。于是

$$
\|X\|_F
\le
\frac{\|C\|_F}{\operatorname{sep}(A,-B)}.
$$

> [!important] 一般矩阵不能只看特征值距离
> 若 $A,B$ 非正规，$\min_{i,j}|\lambda_i(A)+\lambda_j(B)|$ 可能高估真实 separation。可靠条件性应使用算子最小奇异值或 Schur-based 估计。

## 十六、常见误区

> [!warning] 误区 1：`vec` 就是软件默认 flatten
> 数学公式使用哪种堆叠必须先声明。列优先公式配 row-major flatten 会产生隐蔽的置换错误。

> [!warning] 误区 2：$\operatorname{vec}(AXB)=(A\otimes B)\operatorname{vec}(X)$
> 一般错误。列 `vec` 下是 $(B^T\otimes A)\operatorname{vec}(X)$。

> [!warning] 误区 3：复数情形把所有转置都换成伴随
> `vec(AXB)` 的坐标重排产生普通转置 $B^T$；只有原式含 $B^*$ 时才出现 $\overline B$。

> [!warning] 误区 4：证明写成巨型线性系统，就应显式求解它
> 理论表示与生产算法不同。Sylvester/Lyapunov 应利用 Schur、稀疏或低秩结构。

> [!warning] 误区 5：Kronecker 因子可随意换序
> 换序通常需要 commutation/permutation matrix。

> [!warning] 误区 6：K-FAC 分解是精确恒等式
> 单样本梯度外积的 Kronecker 结构精确；期望因子化一般是近似。

> [!warning] 误区 7：唯一可解等于良态
> 谱不相交只保证非奇异；接近相交或非正规性仍可使 separation 很小。

## 十七、掌握检查

1. $(m\times n)\otimes(p\times q)$ 的形状是什么？
2. 为什么混合乘积性质需要两个普通矩阵乘法都形状兼容？
3. 对 $2\times3$ 矩阵，列 `vec` 的元素顺序是什么？
4. 能否从指标完整推出 vec–Kronecker 恒等式？
5. Sylvester 系数为什么是 $I\otimes A+B^T\otimes I$？
6. 唯一性条件和 conditioning 分别由什么控制？
7. 为什么 VJP 不需要显式构造 Kronecker Jacobian？
8. K-FAC 中哪一步精确，哪一步是近似？
9. NumPy/PyTorch 默认 flatten 与本章约定有什么差别？

## 十八、练习与后继

- 分层练习：[[习题 - Kronecker 积、向量化与矩阵方程]]；
- 独立详解：[[解答 - Kronecker 积、向量化与矩阵方程]]；
- 抽象来源与高阶推广：[[多线性映射、张量与缩并]]；
- 微分接口：[[全微分与 Fréchet 导数]]、[[矩阵函数的 Fréchet 导数]]；
- 数值结构：[[Schur 分解]]、[[稳定求解线性方程组]]。

## 来源与证据边界

- Kaare Brandt Petersen & Michael Syskind Pedersen, [*The Matrix Cookbook*](https://www.math.uwaterloo.ca/~hwolkowi/matrixcookbook.pdf)：Kronecker/vec 恒等式与矩阵微分公式索引；
- Tamara G. Kolda & Brett W. Bader, [*Tensor Decompositions and Applications*](https://doi.org/10.1137/07070111X), 2009：张量积、Kronecker、向量化、展开与多线性记号的统一参照；
- SciPy, [solve_sylvester](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.solve_sylvester.html)：Schur-based Bartels–Stewart 软件接口与方程约定；
- PyTorch, [torch.kron](https://docs.pytorch.org/docs/stable/generated/torch.kron.html)：当前数组 Kronecker API 的形状契约；
- Cookbook 用于公式导航，不单独承担数值稳定性结论；Sylvester 的生产算法和 separation 边界需回到矩阵计算教材与官方数值库文档。
