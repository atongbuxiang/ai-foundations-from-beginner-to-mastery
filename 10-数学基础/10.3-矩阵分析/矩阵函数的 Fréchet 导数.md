---
type: concept
status: draft
area: [math/matrix-analysis, math/matrix-calculus, numerical-linear-algebra, ai/automatic-differentiation]
aliases: [矩阵函数的 Frechet 导数, Matrix Function Fréchet Derivative, Matrix Function Differential, Loewner Matrix]
prerequisites: ["[[全微分与 Fréchet 导数]]", "[[矩阵函数与矩阵指数]]", "[[Kronecker 积、向量化与矩阵方程]]", "[[多线性映射、张量与缩并]]", "[[伴随算子]]", "[[矩阵范数]]"]
related: ["[[全微分与 Fréchet 导数]]", "[[Jacobian、JVP 与 VJP]]", "[[函数极限、连续性与收敛模式]]", "[[矩阵扰动]]", "[[Schur 分解]]", "[[极分解]]", "[[矩阵符号函数]]", "[[非正规矩阵、预解式与伪谱]]", "[[结构化矩阵与结构化扰动]]", "[[矩阵分析 MOC]]"]
sources: ["Higham-2008-Functions-of-Matrices", "Higham-Relton-2014-Higher-Frechet", "AlMohy-Higham-2009-Expm-Frechet", "Kandolf-Relton-2017-Block-Krylov-Frechet", "SciPy-expm-frechet"]
exercises: ["[[习题 - 矩阵函数的 Fréchet 导数]]"]
solutions: ["[[解答 - 矩阵函数的 Fréchet 导数]]"]
created: 2026-08-16
updated: 2026-08-27
---

# 矩阵函数的 Fréchet 导数

> [!abstract] 本章主问题
> 对矩阵函数 $F(A)=f(A)$，怎样定义一个同时适用于非交换乘法、条件数分析和反向传播的导数？答案不是另一个可以随意左右相乘的矩阵，而是矩阵空间上的线性算子
> $$
> E\longmapsto L_f(A,E).
> $$
> 它给出输入扰动 $E$ 的一阶输出响应，决定函数的局部条件数；反向传播使用的则是这个线性算子的伴随 $L_f(A)^*$。块矩阵、除差矩阵、Kronecker 表示和 Sylvester 方程是同一个导数的不同坐标或计算接口。

## 学习目标

完成本章后，应能：

1. 解释为什么矩阵函数的导数是线性算子而不是普通 $n\times n$ 矩阵；
2. 区分方向导数、Gâteaux 导数和 Fréchet 导数；
3. 用统一余项定义证明 Fréchet 导数的唯一性；
4. 从乘积展开推导多项式矩阵函数的导数；
5. 证明并使用增广块矩阵公式；
6. 对可对角化矩阵推导 Daleckii–Krein 除差公式；
7. 正确处理重复特征值，不把除差误写成除以零；
8. 推导逆、指数、对数和平方根的导数；
9. 把导数写成 Kronecker Jacobian，并解释为什么通常不应显式物化；
10. 从 Fréchet 导数范数定义绝对与相对条件数；
11. 区分无结构条件数与对称、SPD、稀疏等结构化条件数；
12. 用伴随恒等式推导矩阵函数层的 VJP；
13. 为矩阵指数、平方根和谱函数写出可执行反向传播方程；
14. 使用 Taylor 余项、中心差分和伴随点积测试验证实现；
15. 解释重复谱为何不必使 $f(A)$ 的导数奇异，而非正规性仍可使其高度敏感；
16. 把理论迁移到 SSM、白化、矩阵优化器、Lie 参数化和可微谱层。

> [!question] 初学者读完必须能回答
> 1. 为什么 $L_f(A,\cdot)$ 是从矩阵空间到矩阵空间的线性算子，而不是普通 $n\times n$ 矩阵？
> 2. $f(A+hE)=f(A)+hL_f(A,E)+o(h)$ 中的统一余项比逐方向极限强在哪里？
> 3. 对 $f(A)=A^2$，为什么导数是 $AE+EA$ 而通常不是 $2AE$？
> 4. 增广块矩阵怎样在右上块中编码同一个 Fréchet 导数？
> 5. Daleckii–Krein 除差公式怎样处理重复特征值而不“除以零”？
> 6. JVP 与 VJP 为什么分别使用 $L_f(A)$ 和它的伴随 $L_f(A)^*$？
> 7. 完整 Kronecker Jacobian 何时有理论价值，为什么生产计算通常不应显式物化？
> 8. 非正规性、分支边界与结构化扰动分别怎样影响条件性？

下图把“抽象线性算子—块矩阵计算接口—自动微分接口”放在同一条链上，避免把它们误当成三个不同的导数。

![[00-知识库管理/_assets/figures/frechet-derivative/fig-matrix-function-frechet-operator-interfaces-v2.svg|880]]

> [!figure] 图 1：矩阵函数 Fréchet 导数的三个互补接口
> **图源与改绘：** 本库独立绘制；内容参照 Higham 的矩阵函数理论、Al-Mohy–Higham 的指数 Fréchet 算法与标准自动微分伴随关系。
>
> **怎样读图。** A 先固定导数的对象类型：$E\mapsto L_f(A,E)$；B 用增广块矩阵把这一算子作用读成矩阵函数的右上块；C 分别给出前向 JVP、反向 VJP 和 Hermitian 谱坐标中的除差表达。三个 panel 描述的是同一个算子在不同任务下的接口。
>
> **适用边界（图没有证明什么）。** 块公式需要 $f$ 在相关谱区域中有定义，谱公式的简洁形式依赖 Hermitian 或良态可对角化结构。重复谱本身不自动导致爆炸，但非正规特征基、函数分支边界和接近奇异的 Sylvester 算子都可能放大导数。

## 进入正文前：矩阵函数的导数是一台“输入方向到输出方向”的机器

> [!info] 课程位置
> 前面的 [[矩阵函数与矩阵指数]]回答怎样定义和计算 $f(A)$；本章回答当 $A$ 发生小变化时，$f(A)$ 的一阶变化是什么。中心对象不是某个 $n\times n$ “导数矩阵”，而是线性算子 $E\mapsto L_f(A,E)$。下一章会说明：当 $A$ 非正规时，这台线性机器为什么可能被预解式显著放大。

> [!tip] 建议两遍阅读
> - **第一遍：** 先掌握对象形状、平方函数反例、Fréchet 定义和增广块公式；暂不物化 Kronecker Jacobian。
> - **第二遍：** 再读除差公式、常用函数导数、条件数、伴随 VJP、数值算法与非正规边界。

> [!question] 本章的推导问题链
> 1. 输入矩阵有 $n^2$ 个自由度时，为什么导数不可能天然只是 $n\times n$ 矩阵？
> 2. 展开 $(A+E)^2$ 时，非交换性怎样迫使一阶项成为 $AE+EA$？
> 3. 怎样用一个关于所有小方向都统一成立的余项定义“最佳线性近似”？
> 4. 为什么把 $A,E$ 放入上三角增广块后，$L_f(A,E)$ 会出现在 $f(\mathcal A_E)$ 的右上块？

### 贯穿 MA-13—16 的非正规三角矩阵

固定

$$
T_K=
\begin{bmatrix}
-1&K\\
0&-2
\end{bmatrix},
\qquad K\ge0,
\qquad
E_{12}=
\begin{bmatrix}0&1\\0&0\end{bmatrix}.
$$

因为 $T_K+hE_{12}=T_{K+h}$，对矩阵指数有闭式

$$
e^{T_K}
=
\begin{bmatrix}
e^{-1}&K(e^{-1}-e^{-2})\\
0&e^{-2}
\end{bmatrix},
$$

于是可以直接从参数差商读出

$$
\boxed{
L_{\exp}(T_K,E_{12})
=
\begin{bmatrix}
0&e^{-1}-e^{-2}\\
0&0
\end{bmatrix}.}
$$

这个最小例同时说明三点：$L_{\exp}(T_K,E_{12})$ 与 $e^{T_K}$ 形状相同；它是**指定方向** $E_{12}$ 的输出，而不是完整 Jacobian；沿上三角耦合方向的导数温和，不代表所有方向的最坏条件数都温和。后两章会比较允许与不允许的方向。

> [!note] 符号账本
> | 符号 | 形状/条件 | 含义 |
> |---|---:|---|
> | $A$ | $n\times n$ | 线性化基点 |
> | $E$ | $n\times n$ | 输入扰动方向 |
> | $L_f(A,E)$ | $n\times n$ | 沿 $E$ 的一阶输出响应 |
> | $L_f(A)$ | 矩阵空间到矩阵空间 | 完整 Fréchet 导数算子 |
> | $R_A(E)$ | $n\times n$ | 去掉一阶项后的余项 |
> | $G$ | $n\times n$ | 标量损失从输出端传回的 cotangent；VJP 使用 $L_f(A)^*(G)$ |
> | $T_K$ | $2\times2$ 上三角 | 固定点谱、可调非正规耦合的贯穿例 |

## 阅读前检查：本章会补齐哪些缺口

### 检查 1：矩阵函数不是逐元素函数

本章讨论的是主矩阵函数 $f(A)$，不是把 $f$ 分别作用到 $a_{ij}$。其定义、分支和数值路线见[[矩阵函数与矩阵指数]]。

### 检查 2：`vec` 约定

本库使用列堆叠：

$$
\operatorname{vec}(X)
=\begin{bmatrix}
x_{:1}\\x_{:2}\\\vdots\\x_{:n}
\end{bmatrix}.
$$

因此

$$
\operatorname{vec}(AXB)
=(B^T\otimes A)\operatorname{vec}(X).
$$

详见[[Kronecker 积、向量化与矩阵方程]]。

### 检查 3：伴随不是逆

对矩阵空间使用 Frobenius 实内积

$$
\langle X,Y\rangle_F
=\operatorname{Re}\operatorname{tr}(X^*Y).
$$

线性算子 $\mathcal L$ 的伴随 $\mathcal L^*$ 由

$$
\langle G,\mathcal L(E)\rangle_F
=\langle \mathcal L^*(G),E\rangle_F
$$

定义。反向传播需要伴随，不要求 $\mathcal L$ 可逆。

### 检查 4：先把一般导数算子迁移到矩阵空间

[[全微分与 Fréchet 导数]]已经建立有界线性算子、统一小 $o$ 余项、Gâteaux/Hadamard/Fréchet 层级和双线性微分。本章把同一定义专门应用于有限维矩阵空间，并进一步处理矩阵函数的非交换结构、谱公式、条件数与伴随 VJP。

## 一、为什么标量公式会失败

### 1.1 最小反例：平方函数

对标量 $x$，

$$
(x+\varepsilon e)^2
=x^2+2\varepsilon xe+O(\varepsilon^2).
$$

若机械类比，可能猜测矩阵平方的导数是 $2AE$。但

$$
(A+\varepsilon E)^2
=A^2+\varepsilon(AE+EA)+\varepsilon^2E^2.
$$

所以正确的一阶项是

$$
\boxed{L_{z^2}(A,E)=AE+EA}.
$$

取

$$
A=\begin{bmatrix}0&1\\0&0\end{bmatrix},
\qquad
E=\begin{bmatrix}0&0\\1&0\end{bmatrix}.
$$

则

$$
AE=\begin{bmatrix}1&0\\0&0\end{bmatrix},
\qquad
EA=\begin{bmatrix}0&0\\0&1\end{bmatrix},
$$

因此

$$
L_{z^2}(A,E)=I,
\qquad
2AE=\begin{bmatrix}2&0\\0&0\end{bmatrix}.
$$

错误来自矩阵乘法不交换。只有 $AE=EA$ 时，$AE+EA=2AE$。

### 1.2 导数的输入输出形状

函数

$$
F:\mathbb C^{n\times n}\to\mathbb C^{n\times n}
$$

的输入有 $n^2$ 个坐标，输出也有 $n^2$ 个坐标。若硬写普通 Jacobian，它应是

$$
n^2\times n^2,
$$

而不是 $n\times n$。

更自然的做法是不急着选坐标，把导数保留为线性算子：

$$
L_f(A):\mathbb C^{n\times n}\to\mathbb C^{n\times n},
\qquad
E\mapsto L_f(A,E).
$$

这里：

- $A$ 是线性化基点；
- $E$ 是输入方向；
- $L_f(A,E)$ 是该方向的一阶输出；
- $L_f(A)$ 是完整导数算子。

### 1.3 第一个核心纪律

> [!important] 不要问“导数矩阵是多少”而不说明对象
> 至少要区分：
> 1. 方向作用 $L_f(A,E)$；
> 2. 整个线性算子 $L_f(A)$；
> 3. 选定 `vec` 后的 $n^2\times n^2$ Kronecker 矩阵；
> 4. 标量损失反向传播所需的伴随作用 $L_f(A)^*(G)$。

## 二、Fréchet 导数的定义

### 2.1 定义

> [!definition] Fréchet 导数
> 若存在关于 $E$ 的线性映射 $L_f(A,\cdot)$，使
> $$
> f(A+E)
> =f(A)+L_f(A,E)+R_A(E),
> $$
> 且
> $$
> \lim_{\|E\|\to0}
> \frac{\|R_A(E)\|}{\|E\|}=0,
> $$
> 则称 $f$ 在 $A$ 处 Fréchet 可微，$L_f(A,E)$ 是沿 $E$ 的 Fréchet 导数。

> [!analysis] Fréchet 导数定义的公式七问
> | 问题 | 回答 |
> |---|---|
> | 哪个变量在变化？ | 基点 $A$ 固定，方向矩阵 $E\to0$；$f$ 是矩阵函数而不是逐元素函数。 |
> | 导数的对象类型是什么？ | $L_f(A)$ 是矩阵空间上的线性算子，$L_f(A,E)$ 才是它作用于一个方向后的矩阵。 |
> | 为什么必须要求关于 $E$ 线性？ | “一阶近似”应能叠加方向与尺度；若方向结果不线性，就不能成为局部统一线性模型。 |
> | 小 $o$ 余项强在哪里？ | $\|R_A(E)\|/\|E\|\to0$ 对所有趋零方向统一成立，而不只是每条固定射线各自有极限。 |
> | 与普通 Jacobian 怎样对应？ | 选定列堆叠坐标后，$L_f(A)$ 可表示为 $n^2\times n^2$ 矩阵；这只是坐标表示，不是新的导数。 |
> | 怎样做数值验收？ | 检查 $\|f(A+hE)-f(A)-hL_f(A,E)\|=O(h^2)$，再用伴随点积测试验收 VJP。 |
> | AI 中怎样调用？ | 矩阵指数 SSM、白化/平方根层和谱参数化的 JVP 用 $L_f(A,E)$，反向传播用伴随作用而非显式完整 Jacobian。 |

也常写成

$$
f(A+E)-f(A)-L_f(A,E)=o(\|E\|).
$$

### 2.2 定义中的三层要求

1. **方向完整**：同一个 $L_f(A)$ 必须处理所有足够小的 $E$；
2. **一阶线性**：
   $$
   L_f(A,\alpha E_1+\beta E_2)
   =\alpha L_f(A,E_1)+\beta L_f(A,E_2);
   $$
3. **统一余项**：误差相对 $\|E\|$ 趋于零，不能为每条方向各选一套互不兼容的近似。

### 2.3 为什么导数唯一

假设 $L_1,L_2$ 都满足定义。对固定方向 $E$ 和标量 $t\to0$：

$$
f(A+tE)-f(A)=tL_1(E)+o(|t|),
$$

$$
f(A+tE)-f(A)=tL_2(E)+o(|t|).
$$

相减并除以 $t$：

$$
(L_1-L_2)(E)=o(1).
$$

令 $t\to0$ 得 $(L_1-L_2)(E)=0$。由于 $E$ 任意，$L_1=L_2$。

> [!success] 第一遍停靠线
> 若你已能解释 $L_f(A)$ 与 $L_f(A,E)$ 的类型差别，从展开式推出 $L_{z^2}(A,E)=AE+EA$，并说清统一小 $o$ 余项为何比逐方向极限更强，就已掌握定义主干。接着读完增广块矩阵定理即可进入 [[非正规矩阵、预解式与伪谱]]；除差、VJP 与算法实现可在第二遍补齐。

### 2.4 Gâteaux/方向导数为何更弱

沿固定方向的方向导数是

$$
G_f(A,E)
=\lim_{t\to0}
\frac{f(A+tE)-f(A)}{t}.
$$

Fréchet 可微必然推出这个极限存在且

$$
G_f(A,E)=L_f(A,E).
$$

反过来不自动成立。仅仅“每条直线上都有导数”不能保证：

- 方向结果对 $E$ 线性；
- 不同方向之间连续兼容；
- 存在统一的一阶余项控制。

在有限维矩阵问题中，解析主矩阵函数通常有良好的 Fréchet 理论；但在分支边界、秩变化和非光滑谱变换处仍必须单独检查。

## 三、基本运算规则

设相关导数存在。

### 3.1 线性组合

$$
L_{\alpha f+\beta g}(A,E)
=\alpha L_f(A,E)+\beta L_g(A,E).
$$

### 3.2 乘积规则

对矩阵函数乘积 $h(A)=f(A)g(A)$：

$$
\boxed{
L_h(A,E)
=L_f(A,E)g(A)+f(A)L_g(A,E)
}.
$$

顺序不可交换。

### 3.3 复合规则

若 $h=g\circ f$，则

$$
\boxed{
L_h(A,E)
=L_g\bigl(f(A),L_f(A,E)\bigr)
}.
$$

这就是矩阵空间版本的 JVP 链式法则。

### 3.4 逆映射规则

若 $X(A)$ 可逆，微分恒等式

$$
X(A)X(A)^{-1}=I
$$

得到

$$
L_X(A,E)X^{-1}+X L_{X^{-1}}(A,E)=0.
$$

所以

$$
\boxed{
L_{X^{-1}}(A,E)
=-X^{-1}L_X(A,E)X^{-1}
}.
$$

特别地，$f(A)=A^{-1}$ 时

$$
\boxed{L_{\mathrm{inv}}(A,E)=-A^{-1}EA^{-1}}.
$$

## 四、多项式导数：全部理论的最小模型

### 4.1 矩阵幂

对 $k\ge1$，

$$
\boxed{
L_{z^k}(A,E)
=\sum_{j=0}^{k-1}A^jEA^{k-1-j}
}.
$$

证明可用乘积规则归纳。若对 $k$ 成立，则

$$
A^{k+1}=A^kA,
$$

从而

$$
\begin{aligned}
L_{z^{k+1}}(A,E)
&=L_{z^k}(A,E)A+A^kE\\
&=\sum_{j=0}^{k-1}A^jEA^{k-j}+A^kE\\
&=\sum_{j=0}^{k}A^jEA^{k-j}.
\end{aligned}
$$

### 4.2 多项式

若

$$
p(z)=\sum_{k=0}^{m}a_kz^k,
$$

则

$$
\boxed{
L_p(A,E)
=\sum_{k=1}^{m}a_k
\sum_{j=0}^{k-1}A^jEA^{k-1-j}
}.
$$

### 4.3 什么时候退化为标量公式

若 $AE=EA$，每一项都相同：

$$
A^jEA^{k-1-j}=A^{k-1}E.
$$

于是

$$
L_p(A,E)=p'(A)E=Ep'(A).
$$

所以“$df=f'(A)dA$”不是完全错误，而是一个需要 $A$ 与方向 $E$ 可交换的特殊情形。

### 4.4 二阶余项从哪里来

在 $(A+E)^k$ 的完全展开中：

- 不含 $E$ 的项给 $A^k$；
- 恰含一个 $E$ 的项给 $L_{z^k}(A,E)$；
- 至少含两个 $E$ 的项构成 $O(\|E\|^2)$。

这既证明导数公式，也解释“一阶线性化”为什么只保留一个扰动插入位置。

## 五、增广块矩阵定理

### 5.1 核心公式

构造

$$
\mathcal A_E=
\begin{bmatrix}
A&E\\
0&A
\end{bmatrix}.
$$

在 $f$ 的光滑/定义域条件满足时，

$$
\boxed{
f(\mathcal A_E)
=
\begin{bmatrix}
f(A)&L_f(A,E)\\
0&f(A)
\end{bmatrix}
}.
$$

### 5.2 先对幂证明

直接归纳可得

$$
\mathcal A_E^k
=
\begin{bmatrix}
A^k&\displaystyle\sum_{j=0}^{k-1}A^jEA^{k-1-j}\\
0&A^k
\end{bmatrix}.
$$

因此对多项式 $p$：

$$
p(\mathcal A_E)
=
\begin{bmatrix}
p(A)&L_p(A,E)\\
0&p(A)
\end{bmatrix}.
$$

再通过 Hermite 插值、Cauchy 积分或适当逼近推广到一般主矩阵函数。

### 5.3 这条公式告诉我们什么

1. $f(A)$ 与 $L_f(A,E)$ 是同一个增广函数值的不同块；
2. 导数保留了矩阵函数演算的相似协变结构；
3. 任意可用的 $f$ 算法原则上都能通过 $2n\times2n$ 块矩阵产生导数；
4. 这只是通用构造，不代表它总是最高效或最稳定的生产算法。

### 5.4 相似协变

令 $A=SBS^{-1}$、$E=SHS^{-1}$。对增广块矩阵做相似变换可得

$$
\boxed{
L_f(SBS^{-1},SHS^{-1})
=S L_f(B,H)S^{-1}
}.
$$

这将一般可对角化问题化到特征坐标，但非酉 $S$ 会同时引入条件数放大。

## 六、Daleckii–Krein 除差公式

### 6.1 可对角化情形

设

$$
A=Z\Lambda Z^{-1},
\qquad
\Lambda=\operatorname{diag}(\lambda_1,\ldots,\lambda_n),
$$

并令特征坐标中的扰动为

$$
\widehat E=Z^{-1}EZ.
$$

定义一阶除差

$$
f[\alpha,\beta]
=
\begin{cases}
\dfrac{f(\alpha)-f(\beta)}{\alpha-\beta},
&\alpha\ne\beta,\\[1.1em]
f'(\alpha),&\alpha=\beta.
\end{cases}
$$

构造除差矩阵

$$
F_{ij}=f[\lambda_i,\lambda_j].
$$

则

$$
\boxed{
L_f(A,E)
=Z\bigl(F\odot\widehat E\bigr)Z^{-1}
}.
$$

这里 $\odot$ 是 Hadamard 积。

### 6.2 为什么是除差

先考虑 $A=\Lambda$。块矩阵定理与上三角矩阵函数公式说明，方向 $E_{ij}$ 从第 $j$ 个特征方向耦合到第 $i$ 个特征方向时，其一阶增益为

$$
f[\lambda_i,\lambda_j].
$$

于是每个特征坐标分量独立缩放：

$$
(L_f(\Lambda,E))_{ij}
=f[\lambda_i,\lambda_j]E_{ij}.
$$

最后用相似协变搬回原坐标。

### 6.3 重复特征值不是除以零

当 $\lambda_i\to\lambda_j=\lambda$：

$$
\lim_{\lambda_i\to\lambda}
\frac{f(\lambda_i)-f(\lambda)}{\lambda_i-\lambda}
=f'(\lambda).
$$

因此正确连续延拓是 $f'(\lambda)$。对解析 $f$，重复谱本身不会让 $L_f$ 自动发散。

最鲜明的例子是

$$
A=\lambda I.
$$

此时所有条目都使用 $f'(\lambda)$：

$$
\boxed{L_f(\lambda I,E)=f'(\lambda)E}.
$$

虽然 $A$ 的特征向量完全不唯一，矩阵函数的导数却可以非常良态。

### 6.4 Hermitian 情形最清楚

若

$$
A=Q\Lambda Q^*,
\qquad Q^*Q=I,
$$

则

$$
L_f(A,E)
=Q\left(F\odot(Q^*EQ)\right)Q^*.
$$

酉变换不放大 Frobenius 范数，因此

$$
\|L_f(A)\|_{F\to F}
=\max_{i,j}|f[\lambda_i,\lambda_j]|.
$$

这给出谱函数敏感性的精确坐标解释：

- 对角扰动由 $f'(\lambda_i)$ 控制；
- 特征方向间耦合由除差 $f[\lambda_i,\lambda_j]$ 控制；
- 不需要单独求导特征向量。

### 6.5 非正规矩阵为什么更难

若 $A=Z\Lambda Z^{-1}$ 但 $Z$ 很病态，则粗略地

$$
\|L_f(A,E)\|_F
\lesssim
\kappa_2(Z)^2
\max_{i,j}|f[\lambda_i,\lambda_j]|
\|E\|_F.
$$

点谱与除差只描述特征坐标内的增益，进出斜特征基还可能各放大一次。下一节点[[非正规矩阵、预解式与伪谱]]会把这种现象推广到 resolvent 与伪谱语言。

## 七、四类常用矩阵函数的导数

### 7.1 逆

已由逆规则得到

$$
\boxed{L_{z^{-1}}(A,E)=-A^{-1}EA^{-1}}.
$$

当 $A$ 接近奇异时，两个逆因子会放大扰动，提示条件数大约含 $\|A^{-1}\|^2$。

### 7.2 矩阵指数

由幂级数逐项求导：

$$
L_{\exp}(A,E)
=\sum_{k=1}^{\infty}\frac1{k!}
\sum_{j=0}^{k-1}A^jEA^{k-1-j}.
$$

等价积分式为

$$
\boxed{
L_{\exp}(A,E)
=\int_0^1e^{(1-s)A}Ee^{sA}\,ds
}.
$$

若 $AE=EA$，才简化为

$$
L_{\exp}(A,E)=e^AE.
$$

一般还满足交换子恒等式

$$
\boxed{
A L_{\exp}(A,E)-L_{\exp}(A,E)A
=e^AE-Ee^A
}.
$$

证明方法是对积分核关于 $s$ 求导并使用微积分基本定理。

### 7.3 SPD 矩阵对数

对 $A\succ0$，主对数导数可写成

$$
\boxed{
L_{\log}(A,E)
=\int_0^{\infty}
(A+tI)^{-1}E(A+tI)^{-1}\,dt
}.
$$

若 $AE=EA$，积分退化为

$$
L_{\log}(A,E)=A^{-1}E.
$$

一般不能这样简化。

特别注意：

$$
d\,\operatorname{tr}(\log A)
=\operatorname{tr}(A^{-1}dA)
$$

成立，是因为 trace 消除了非交换排列；它不表示

$$
d(\log A)=A^{-1}dA
$$

对任意方向成立。

### 7.4 SPD 平方根

令

$$
X=A^{1/2},
\qquad X^2=A.
$$

沿 $E$ 求导，记 $Z=L_{\sqrt{\cdot}}(A,E)$：

$$
XZ+ZX=E.
$$

所以

$$
\boxed{
L_{\sqrt{\cdot}}(A,E)
=Z,
\quad
XZ+ZX=E
}.
$$

这是 Sylvester 方程。因 $X\succ0$，$\lambda_i(X)+\lambda_j(X)>0$，解唯一。

若 $A=Q\operatorname{diag}(\lambda_i)Q^*$，则在特征坐标中

$$
\widehat Z_{ij}
=\frac{\widehat E_{ij}}
{\sqrt{\lambda_i}+\sqrt{\lambda_j}},
$$

与除差恒等式

$$
\frac{\sqrt{\lambda_i}-\sqrt{\lambda_j}}
{\lambda_i-\lambda_j}
=\frac1{\sqrt{\lambda_i}+\sqrt{\lambda_j}}
$$

完全一致。

### 7.5 逆平方根

令 $X=A^{1/2}$、$W=A^{-1/2}=X^{-1}$。先求

$$
XZ+ZX=E,
$$

再由逆规则得到

$$
\boxed{
L_{z^{-1/2}}(A,E)
=-X^{-1}ZX^{-1}
}.
$$

当 $\lambda_{\min}(A)$ 很小时，平方根 Sylvester 与两侧逆都会放大误差。这正是白化和矩阵预条件器需要 damping 的理论原因之一。

### 7.6 matrix sign 与 polar 的位置

[[矩阵符号函数]]的导数由对合与交换结构导出 Sylvester 方程；[[极分解]]的导数也通过正定因子上的 Sylvester 方程组织。本章的贡献是说明它们不是孤立技巧，而是 Fréchet 线性化的一般实例。

## 八、Kronecker 形式：完整 Jacobian 的坐标表示

### 8.1 定义

因为 $E\mapsto L_f(A,E)$ 是线性映射，所以存在唯一矩阵

$$
K_f(A)\in\mathbb C^{n^2\times n^2}
$$

满足

$$
\boxed{
\operatorname{vec}(L_f(A,E))
=K_f(A)\operatorname{vec}(E)
}.
$$

$K_f(A)$ 就是选定列 `vec` 坐标后的完整 Jacobian。

### 8.2 平方函数的 Kronecker 形式

由

$$
L_{z^2}(A,E)=AE+EA
$$

和 vec 恒等式：

$$
\operatorname{vec}(AE)
=(I\otimes A)\operatorname{vec}(E),
$$

$$
\operatorname{vec}(EA)
=(A^T\otimes I)\operatorname{vec}(E),
$$

所以

$$
\boxed{
K_{z^2}(A)=I\otimes A+A^T\otimes I
}.
$$

### 8.3 为什么通常不物化

若 $A$ 是 $5000\times5000$，则 $K_f(A)$ 是

$$
25{,}000{,}000\times25{,}000{,}000.
$$

它有 $6.25\times10^{14}$ 个元素。float64 仅存储就约需 $5$ PB。

因此：

- 理论上用 $K_f(A)$ 描述 Jacobian、条件数和谱；
- 计算上用 $E\mapsto L_f(A,E)$ 与 $G\mapsto L_f(A)^*(G)$；
- 大规模问题进一步只算 $L_f(A,E)b$ 或少量方向。

## 九、条件数：函数本身是否敏感

### 9.1 绝对条件数

对选定矩阵范数，

$$
\boxed{
\operatorname{cond}_{\mathrm{abs}}(f,A)
=\|L_f(A)\|
=\max_{E\ne0}
\frac{\|L_f(A,E)\|}{\|E\|}
}.
$$

它给出单位绝对输入扰动的一阶最坏输出放大。

在 Frobenius 范数和列 `vec` 下：

$$
\operatorname{cond}_{\mathrm{abs}}(f,A)
=\|K_f(A)\|_2.
$$

### 9.2 相对条件数

当 $A\ne0$ 且 $f(A)\ne0$：

$$
\boxed{
\operatorname{cond}_{\mathrm{rel}}(f,A)
=\frac{\|L_f(A)\|\,\|A\|}{\|f(A)\|}
}.
$$

它是局部、最坏方向、范数型的一阶量。必须同时写明：

- 使用什么输入/输出范数；
- 允许哪些扰动方向；
- 相对缩放如何定义；
- $f(A)$ 接近零时是否改用绝对量。

### 9.3 条件性与算法稳定性

> [!important] 两个问题必须分开
> - 条件数：精确函数 $f$ 对输入扰动是否敏感；
> - 稳定性：算法是否等价于在邻近输入上精确计算 $f$。
>
> 即使算法后向稳定，若 $\|L_f(A)\|$ 很大，前向误差仍可能很大。

### 9.4 结构化条件数

若输入理论上必须属于某个结构集合，例如 Hermitian、SPD、Toeplitz、稀疏模式或 Hamiltonian，则合法扰动 $E$ 只属于相应切空间 $\mathcal S$。结构化绝对条件数应写成

$$
\operatorname{cond}_{\mathcal S}(f,A)
=\max_{0\ne E\in\mathcal S}
\frac{\|L_f(A,E)\|}{\|E\|}.
$$

它不大于无结构条件数，但更贴近真实数据生成和算法误差。后续[[结构化矩阵与结构化扰动]]会系统展开。

## 十、伴随 Fréchet 导数与反向传播

### 10.1 从 JVP 到 VJP

前向线性化是

$$
dY=L_f(A,dA).
$$

设标量损失 $\ell$ 对输出 $Y=f(A)$ 的上游矩阵为 $G$，即

$$
d\ell=\langle G,dY\rangle_F.
$$

代入：

$$
d\ell
=\langle G,L_f(A,dA)\rangle_F.
$$

由伴随定义：

$$
d\ell
=\langle L_f(A)^*(G),dA\rangle_F.
$$

因此

$$
\boxed{
\nabla_A\ell=L_f(A)^*(G)
}.
$$

### 10.2 解析函数的伴随恒等式

定义共轭反射标量函数

$$
f^{\#}(z)=\overline{f(\overline z)}.
$$

对解析主矩阵函数，在标准 Frobenius 内积下：

$$
\boxed{
L_f(A)^*(G)=L_{f^{\#}}(A^*,G)
}.
$$

若 $f$ 的幂级数系数为实数，如 $\exp$，则 $f^{\#}=f$：

$$
L_f(A)^*(G)=L_f(A^*,G).
$$

### 10.3 矩阵指数的 VJP

前向：

$$
L_{\exp}(A,E)
=\int_0^1e^{(1-s)A}Ee^{sA}\,ds.
$$

反向：

$$
\boxed{
L_{\exp}(A)^*(G)
=L_{\exp}(A^*,G)
=\int_0^1e^{(1-s)A^*}Ge^{sA^*}\,ds
}.
$$

实矩阵时把 $A^*$ 换成 $A^T$。

### 10.4 SPD 平方根的 VJP

前向导数是 Sylvester 算子的逆：

$$
\mathcal S_X(Z)=XZ+ZX=E,
\qquad X=A^{1/2}.
$$

其伴随算子为

$$
\mathcal S_X^*(Y)=X^*Y+YX^*.
$$

因此给定上游 $G$，反向梯度 $Y=L_{\sqrt{\cdot}}(A)^*(G)$ 由

$$
\boxed{
X^*Y+YX^*=G
}.
$$

若 $A\succ0$ 且 $X=X^*$，前向和反向使用同一个自伴 Sylvester 算子。

### 10.5 参数化矩阵的链式法则

若 $A=A(\theta)$，则

$$
\frac{\partial\ell}{\partial\theta_k}
=\left\langle
L_f(A)^*(G),
\frac{\partial A}{\partial\theta_k}
\right\rangle_F.
$$

这把“矩阵函数反向”与“参数化反向”分开：

1. 先把上游 $G$ 通过 $L_f(A)^*$ 拉回到矩阵 $A$；
2. 再通过 $A(\theta)$ 的 Jacobian 拉回到参数 $\theta$。

## 十一、数值计算路线

### 11.1 通用 block enlargement

计算

$$
f\left(
\begin{bmatrix}A&E\\0&A\end{bmatrix}
\right)
$$

并取右上块。优点是统一、易验证；缺点是维数翻倍，通用算法可能不充分利用重复对角块和方向结构。

### 11.2 专用矩阵指数算法

矩阵指数可用 scaling–Padé–squaring 的导数版本，同时计算

$$
e^A,
\qquad
L_{\exp}(A,E).
$$

其思想是对缩放、Padé 有理式和 squaring 递推逐层求导，而不是把整个问题当作黑盒 $2n$ 阶指数。SciPy 的 `expm_frechet` 提供专用 `SPS` 路线和用于对照的 `blockEnlarge` 路线。

### 11.3 Schur 与 Parlett 路线

对一般稠密矩阵：

1. 先做 $A=QTQ^*$；
2. 在上三角/准上三角 $T$ 上计算函数与导数；
3. 使用块 Parlett 递推或 Sylvester 方程处理非对角块；
4. 用酉变换搬回。

它比显式 Jordan 分解可靠，因为 Schur 向量是酉的，且避免构造对扰动不连续的 Jordan 链。

### 11.4 Hermitian 谱路线

若 $A$ Hermitian，酉特征分解和除差公式非常直接：

$$
L_f(A,E)
=Q\left(F\odot(Q^*EQ)\right)Q^*.
$$

但实现仍需处理：

- 近重复特征值时稳定计算除差；
- 保留 Hermitian 结构；
- 函数分支和谱定义域；
- 不为求导特征向量而显式除以不必要的 gap。

### 11.5 大规模 action

若只需要

$$
L_f(A,E)b,
$$

完整形成 $L_f(A,E)$ 仍可能太贵。可使用 block Krylov 或 action 方法，只调用 $A$、$A^*$、$E$ 与向量/窄块的乘法。低秩 $E=UV^*$ 时尤其适合保留低秩结构。

### 11.6 路线选择表

| 任务 | 推荐表示 | 主要风险 |
|---|---|---|
| 小规模教学/验证 | $2n$ 块矩阵 | 成本约随维数翻倍显著上升 |
| 稠密 $e^A$ 与一个方向 | 专用 `expm_frechet` | 尺度、非正规性、条件数 |
| 一般稠密 $f(A)$ | Schur–Parlett/专用函数算法 | 谱簇与 Sylvester separation |
| Hermitian/SPD 谱函数 | 除差或 Sylvester | 小特征值、分支、近重复除差 |
| 大稀疏，仅需 action | block Krylov/action | 停止准则、非正规收敛、低秩假设 |
| 条件数估计 | 反复应用 $L_f$ 与 $L_f^*$ | 不应显式构造 $K_f(A)$ |

## 十二、实现验收：不能只看“自动求导没报错”

### 12.1 线性测试

检查

$$
L_f(A,\alpha E_1+\beta E_2)
\approx
\alpha L_f(A,E_1)+\beta L_f(A,E_2).
$$

这能发现把方向错误广播、转置或共轭的实现问题。

### 12.2 一阶 Taylor 余项

定义

$$
r(h)=
\|f(A+hE)-f(A)-hL_f(A,E)\|.
$$

在进入舍入误差地板前，应观察到

$$
r(h)=O(h^2).
$$

若画 $\log r$ 对 $\log h$，局部斜率应接近 $2$。

### 12.3 差分导数

前向差分

$$
D_h^{\mathrm{fwd}}
=\frac{f(A+hE)-f(A)}{h}
$$

截断误差 $O(h)$；中心差分

$$
D_h^{\mathrm{ctr}}
=\frac{f(A+hE)-f(A-hE)}{2h}
$$

截断误差通常 $O(h^2)$。但 $h$ 太小时二者都会受相消和函数计算误差限制。

对满足条件的实矩阵解析函数，complex-step 可作为补充验证工具，但如果底层算法本身使用复算术并破坏所需结构，也不能无条件相信。

### 12.4 伴随点积测试

随机取 $E,G$，验证

$$
\boxed{
\langle G,L_f(A,E)\rangle_F
\approx
\langle L_f(A)^*(G),E\rangle_F
}.
$$

这是 VJP 实现最有价值的局部测试之一，因为它不需要显式 Jacobian。

### 12.5 结构与定义域测试

还应检查：

- Hermitian $A,E$ 是否产生理论上 Hermitian 的方向输出；
- SPD 的最小特征值是否远离分支/奇异边界；
- 实输入是否因主分支而合法地产生复输出；
- 计算的是主矩阵函数还是 SVD 广义矩阵函数；
- batch、dtype、共轭和 `vec` 顺序是否一致。

## 十三、四个完整手算例子

### 13.1 平方函数：非交换的一阶项

沿用第一节的

$$
A=\begin{bmatrix}0&1\\0&0\end{bmatrix},
\quad
E=\begin{bmatrix}0&0\\1&0\end{bmatrix}.
$$

因为 $A^2=0$，

$$
(A+hE)^2
=h(AE+EA)+h^2E^2
=hI,
$$

这里 $E^2=0$。所以该方向上甚至得到精确关系

$$
f(A+hE)-f(A)=hL_f(A,E).
$$

### 13.2 对角矩阵的指数

令

$$
A=\operatorname{diag}(0,1),
\qquad
E=\begin{bmatrix}1&2\\3&4\end{bmatrix}.
$$

指数除差矩阵为

$$
F=
\begin{bmatrix}
1&e-1\\
e-1&e
\end{bmatrix}.
$$

故

$$
\boxed{
L_{\exp}(A,E)
=\begin{bmatrix}
1&2(e-1)\\
3(e-1)&4e
\end{bmatrix}
}.
$$

而

$$
e^AE
=\begin{bmatrix}1&2\\3e&4e\end{bmatrix},
$$

二者一般不同。

### 13.3 SPD 平方根

令

$$
A=\operatorname{diag}(1,4),
\quad
X=A^{1/2}=\operatorname{diag}(1,2),
$$

$$
E=\begin{bmatrix}2&3\\3&8\end{bmatrix}.
$$

由

$$
Z_{ij}=\frac{E_{ij}}{x_i+x_j},
$$

得到

$$
Z=\begin{bmatrix}1&1\\1&2\end{bmatrix}.
$$

核对：

$$
XZ+ZX
=\begin{bmatrix}2&3\\3&8\end{bmatrix}=E.
$$

### 13.4 重复谱与稳定函数值

令 $A=2I$。对指数：

$$
L_{\exp}(2I,E)=e^2E.
$$

这里任意正交基都是特征基，因此“特征向量的导数”没有唯一意义；但 $e^A=e^2I$ 的 Fréchet 导数完全明确。由此应记住：

> [!important] 可微矩阵函数不等于可微特征向量参数化
> 对重复谱，直接对 eig 输出求导可能遇到基选择奇异性；对 $f(A)$ 使用除差、块公式或 Schur 算法，往往仍有良好的一阶对象。

## 十四、AI 中的直接接口

### 14.1 连续时间 SSM 的离散化

状态传播矩阵

$$
A_d=e^{\Delta A}
$$

对 $A$ 的方向 $E$ 满足

$$
dA_d=L_{\exp}(\Delta A,\Delta E).
$$

若步长 $\Delta$ 也可训练，则还要加入

$$
\frac{\partial}{\partial\Delta}e^{\Delta A}
=Ae^{\Delta A},
$$

因为 $A$ 与 $\Delta A$ 可交换。不能把对矩阵 $A$ 的方向导数和对标量 $\Delta$ 的导数混为一式。

### 14.2 白化与协方差层

白化常含

$$
W=(C+\varepsilon I)^{-1/2}.
$$

其反向敏感性同时受：

- 最小特征值；
- damping $\varepsilon$；
- batch 协方差估计噪声；
- 特征值簇；
- 使用精确谱分解、Newton–Schulz 还是隐式 Sylvester

影响。重复特征值不应通过裸 $1/(\lambda_i-\lambda_j)$ 处理；正确除差在极限处连续。

### 14.3 矩阵优化器与预条件

Shampoo 类预条件、逆平方根和 polar/msign 更新都调用矩阵函数。前向近似误差与反向 Fréchet 条件数是两件事：有限步迭代可能给出足够好的更新方向，却不一定给出精确矩阵函数的梯度。

### 14.4 Lie 群与结构参数化

正交/酉参数化常写成

$$
Q=e^S,
\qquad S^*=-S.
$$

方向 $H^*=-H$ 下

$$
dQ=L_{\exp}(S,H).
$$

由于方向被限制在斜 Hermitian 切空间，评估条件性时应使用结构化方向，而不是所有无结构矩阵。

### 14.5 可微谱滤波

图神经网络、核方法和协方差几何中可能使用 $f(A)$ 作为谱滤波器。Daleckii–Krein 公式说明：

- $f'(\lambda_i)$ 控制特征值本身的变化；
- $f[\lambda_i,\lambda_j]$ 控制不同谱方向的耦合；
- 仅检查标量 $f'$ 不能完整描述矩阵输入的敏感性。

### 14.6 反向传播的生产契约

一个可微矩阵函数层至少应记录：

1. 函数分支与输入谱定义域；
2. 前向算法、dtype 和停止准则；
3. JVP/VJP 是专用算法、隐式方程还是迭代展开；
4. 是否保留 Hermitian/SPD/稀疏结构；
5. 小特征值、非正规性和 separation 诊断；
6. Taylor 与伴随点积测试结果；
7. 是否对迭代近似本身求导，还是使用精确函数的隐式导数。

## 十五、边界与常见误区

### 15.1 把矩阵函数导数当成逐元素导数

逐元素函数的 Jacobian 通常是逐元素乘法；主矩阵函数的导数包含不同矩阵位置之间的耦合。两者形状相同但对象不同。

### 15.2 把 $L_f(A,E)$ 写成 $f'(A)E$

仅在 $A$ 与 $E$ 可交换等特殊情形成立。一般应使用扰动插入和除差。

### 15.3 认为每条方向有极限就够了

还需检查方向结果线性以及余项的统一性。Gâteaux 可微弱于 Fréchet 可微。

### 15.4 认为重复特征值必然导致梯度爆炸

裸特征向量参数化可能奇异，但平滑主矩阵函数的除差在重复点取 $f'(\lambda)$。真正的危险还包括函数分支、小特征值、缺陷性和非正规基。

### 15.5 只看特征值判断条件性

非正规矩阵可在固定点谱下因特征基病态、resolvent 放大或 Sylvester separation 很小而产生巨大 Fréchet 导数。

### 15.6 显式构造完整 Jacobian

$K_f(A)$ 用于理论与小规模验证。生产反向应优先实现 $L_f$、$L_f^*$ 或 action。

### 15.7 用一个极小 $h$ 做差分检查

$h$ 太大时截断误差明显，太小时相消和舍入占主导。应扫一段对数步长并观察误差斜率与地板。

### 15.8 认为自动微分通过就代表数学正确

框架可能对特定算法路径求导，而不是对理想矩阵函数求导；迭代截断、分支、特征向量规范和 dtype 都会改变实际 VJP。

### 15.9 忽略复数微分约定

对复矩阵和实值损失，应使用实 Frobenius 内积、共轭转置和明确的 Wirtinger/实线性约定。不能把 $T$ 与 $*$ 随意互换。

### 15.10 把无结构最坏方向当成真实数据误差

若输入始终 Hermitian/SPD，反 Hermitian 方向不是合法扰动。结构化条件数可能显著不同，必须与应用的数据约束一致。

## 十六、前沿地位与研究边界

| 内容 | 知识地位 | 本章处理方式 |
|---|---|---|
| Fréchet 定义、运算规则、块公式 | 经典成熟理论 | 完整推导与手算 |
| Daleckii–Krein 除差公式 | 经典成熟理论 | 可对角化/Hermitian 情形完整展开 |
| exp/log/sqrt 导数 | 经典成熟理论 | 给出积分或 Sylvester 公式 |
| Kronecker 形式与条件数 | 经典敏感性理论 | 连接 D3 的 vec 语言 |
| 伴随 Fréchet 与 VJP | 成熟自动微分接口 | 从 Frobenius 伴随推导 |
| scaling–Padé–squaring 导数 | 成熟数值算法 | 讲设计与软件契约，不复刻生产源码 |
| block Krylov derivative action | 成熟大规模路线 | 给出适用边界和低秩方向接口 |
| 高阶 Fréchet 导数 | 成熟但更进阶 | 说明为多线性映射，留作后续扩展 |
| 非正规 Fréchet 条件性 | 成熟理论与活跃算法交界 | 下一节点用伪谱系统化 |
| 近似迭代的梯度等同精确函数梯度 | 一般不成立 | 强制区分算法映射与理想函数 |

## 十七、掌握检查

1. 为什么 $L_f(A)$ 是 $n^2$ 维空间上的线性算子？
2. Fréchet 定义中的“统一余项”比方向导数多保证了什么？
3. 怎样从 $(A+E)^k$ 的扰动插入推导矩阵幂导数？
4. 块矩阵右上角为什么恰是 $L_f(A,E)$？
5. 除差在重复特征值处应取什么值？
6. 为什么 $A=\lambda I$ 时 eig 向量不唯一但 $L_f$ 可以良态？
7. $L_{\exp}(A,E)$ 何时等于 $e^AE$？
8. SPD 平方根导数为什么是 Sylvester 方程？
9. $d\,\operatorname{tr}(\log A)$ 与 $d(\log A)$ 有何区别？
10. $K_f(A)$ 的形状是什么，为什么不应在大规模问题中物化？
11. 条件数大和算法不稳定分别是什么意思？
12. 怎样从 $L_f(A)$ 得到反向传播的 $L_f(A)^*$？
13. Taylor 余项和伴随点积测试分别检查什么？
14. 非正规性为何能在点谱不变时放大导数？
15. 对迭代近似求导和使用精确函数隐式导数有什么区别？

## 十八、练习与后继

- 分层练习：[[习题 - 矩阵函数的 Fréchet 导数]]；
- 独立详解：[[解答 - 矩阵函数的 Fréchet 导数]]；
- 定义与函数演算前置：[[矩阵函数与矩阵指数]]；
- vec/Jacobian 前置：[[Kronecker 积、向量化与矩阵方程]]；
- 伴随/VJP 前置：[[伴随算子]]、[[多线性映射、张量与缩并]]；
- 专门实例：[[极分解]]、[[矩阵符号函数]]；
- 下一理论节点：[[非正规矩阵、预解式与伪谱]]；
- 结构化方向：[[结构化矩阵与结构化扰动]]。

## 来源与证据边界

- Nicholas J. Higham, [*Functions of Matrices: Theory and Computation*](https://epubs.siam.org/doi/10.1137/1.9780898717778)：Fréchet 导数、条件数、块矩阵、Schur–Parlett 与主要矩阵函数算法的规范来源；
- Nicholas J. Higham & Samuel D. Relton, [*Higher Order Fréchet Derivatives of Matrix Functions and the Level-2 Condition Number*](https://doi.org/10.1137/130945259), 2014：一阶定义、Kronecker 形式、高阶导数与条件数层级；
- Awad H. Al-Mohy & Nicholas J. Higham, [*Computing the Fréchet Derivative of the Matrix Exponential, with an Application to Condition Number Estimation*](https://eprints.maths.manchester.ac.uk/1218/), 2009：矩阵指数 scaling–squaring 导数算法与条件估计；
- Peter Kandolf & Samuel D. Relton, [*A Block Krylov Method to Compute the Action of the Fréchet Derivative of a Matrix Function on a Vector*](https://eprints.maths.manchester.ac.uk/2566/), 2017：大规模 action 与低秩方向；
- Vanni Noferini, [*A Daleckii–Krein Formula for the Fréchet Derivative of a Generalized Matrix Function*](https://eprints.maths.manchester.ac.uk/2462/), 2016：经典可对角化除差公式的明确陈述及广义矩阵函数推广；
- SciPy, [scipy.linalg.expm_frechet](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.expm_frechet.html)：当前 `SPS`、`blockEnlarge`、batch core shape 与返回契约；
- 本章关于解析函数的结论不自动扩展到逐奇异值广义矩阵函数、非主分支或非光滑谱截断；软件能返回结果也不证明输入远离分支边界或问题良态。
