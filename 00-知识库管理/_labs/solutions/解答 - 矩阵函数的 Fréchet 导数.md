---
type: solution-set
status: draft
area: [labs, math/matrix-analysis, math/matrix-calculus, ai/automatic-differentiation]
prerequisites: ["[[习题 - 矩阵函数的 Fréchet 导数]]"]
related: ["[[矩阵函数的 Fréchet 导数]]", "[[Kronecker 积、向量化与矩阵方程]]", "[[伴随算子]]", "[[练习与测验 MOC]]"]
sources: ["Higham-2008-Functions-of-Matrices", "Higham-Relton-2014-Higher-Frechet", "AlMohy-Higham-2009-Expm-Frechet"]
created: 2026-08-16
updated: 2026-08-16
---

# 解答 - 矩阵函数的 Fréchet 导数

> [!important] 使用方式
> 先独立写出导数算子的输入输出，再核对公式。若只看最终矩阵而不解释线性算子、余项、伴随和条件，本组题的核心目标尚未完成。

## A 级：识别与复述

### MA-FR-A01：四种“导数对象”

设 $A,E,G\in\mathbb R^{n\times n}$。

1. $L_f(A,E)$ 是一次方向作用。输入方向 $E$ 为 $n\times n$，输出也是 $n\times n$。

2. $L_f(A)$ 是完整线性算子：

   $$
   L_f(A):\mathbb R^{n\times n}\to\mathbb R^{n\times n}.
   $$

   它不是某一个方向的结果，而是保存所有方向响应的规则。

3. 选定列 `vec` 后，矩阵空间与 $\mathbb R^{n^2}$ 同构，所以存在

   $$
   K_f(A)\in\mathbb R^{n^2\times n^2}
   $$

   使

   $$
   \operatorname{vec}(L_f(A,E))
   =K_f(A)\operatorname{vec}(E).
   $$

4. $L_f(A)^*(G)$ 是伴随算子对上游 $G$ 的一次作用，输入、输出均为 $n\times n$，满足

   $$
   \langle G,L_f(A,E)\rangle_F
   =\langle L_f(A)^*(G),E\rangle_F.
   $$

5. “导数是 $n\times n$ 矩阵”把完整 $n^2$ 输入自由度压成了一个方向输出。只有在已给定 $E$ 时，$L_f(A,E)$ 才是 $n\times n$；完整 Jacobian 在坐标下是 $n^2\times n^2$。

### MA-FR-A02：判断八个断言

1. **对。** 令扰动为 $tE$，Fréchet 展开除以 $t$ 后取极限即得方向导数。
2. **错。** 各方向极限可能对方向不线性，或没有统一余项控制。
3. **错。** 正确式是 $AE+EA$；只有 $AE=EA$ 时才是 $2AE$。
4. **对。** $\lambda I$ 与所有方向可交换，或直接用重复谱除差 $f[\lambda,\lambda]=f'(\lambda)$。
5. **错。** 对平滑/解析主矩阵函数，重复点使用连续除差 $f'(\lambda)$。重复 eig 向量基不唯一不等于 $f(A)$ 不可微。
6. **对。** 列 `vec` 是 Frobenius 空间到欧氏空间的等距同构，故诱导算子范数等于 $\|K_f(A)\|_2$。
7. **错。** 后向稳定只说明结果对应邻近输入；若问题条件数大，邻近输入的精确函数值也可能相差很大。
8. **错。** 反向传播需要伴随 $L_f(A)^*$，不需要导数算子可逆。

### MA-FR-A03：除差与重复谱

对 $f(z)=z^2$：

$$
f[\alpha,\beta]
=\frac{\alpha^2-\beta^2}{\alpha-\beta}
=\alpha+\beta
$$

在 $\alpha\ne\beta$ 时成立；当二者相等时 $f'(\alpha)=2\alpha$，仍等于 $\alpha+\alpha$。因此

$$
F=
\begin{bmatrix}
2&2&4\\
2&2&4\\
4&4&6
\end{bmatrix}.
$$

左上 $2\times2$ 块及 $(3,3)$ 条目都对应相同节点，按定义使用 $f'(1)=2$ 或 $f'(3)=6$；数值上整张表统一是 $\lambda_i+\lambda_j$。

若

$$
A=Q\Lambda Q^*,
\qquad
\widehat E=Q^*EQ,
$$

则

$$
L_f(A,E)=Q(F\odot\widehat E)Q^*.
$$

而

$$
(\Lambda\widehat E+\widehat E\Lambda)_{ij}
=(\lambda_i+\lambda_j)\widehat E_{ij}
=F_{ij}\widehat E_{ij}.
$$

所以

$$
Q(F\odot\widehat E)Q^*
=Q(\Lambda\widehat E+\widehat E\Lambda)Q^*
=AE+EA.
$$

## B 级：手算与构造

### MA-FR-B01：平方函数的非交换反例

直接相乘：

$$
AE=
\begin{bmatrix}1&0\\0&0\end{bmatrix},
\qquad
EA=
\begin{bmatrix}0&0\\0&1\end{bmatrix}.
$$

所以

$$
L_f(A,E)=AE+EA=I_2.
$$

标量捷径给出的却是

$$
2AE=
\begin{bmatrix}2&0\\0&0\end{bmatrix}
\ne I_2.
$$

又因为 $A^2=E^2=0$：

$$
\begin{aligned}
(A+hE)^2
&=A^2+h(AE+EA)+h^2E^2\\
&=hI_2.
\end{aligned}
$$

于是

$$
f(A+hE)-f(A)=hL_f(A,E),
$$

本题余项恰好为零。

对一般 $2\times2$ 的 $A$，列 `vec` 下

$$
\boxed{
K_f(A)=I_2\otimes A+A^T\otimes I_2
}.
$$

### MA-FR-B02：对角矩阵指数的除差手算

标量指数的除差是

$$
e^{[\alpha,\beta]}
=
\begin{cases}
\dfrac{e^\alpha-e^\beta}{\alpha-\beta},&\alpha\ne\beta,\\
e^\alpha,&\alpha=\beta.
\end{cases}
$$

对 $0,1$ 得

$$
F=
\begin{bmatrix}
1&e-1\\
e-1&e
\end{bmatrix}.
$$

$A$ 已在特征坐标中，因此

$$
L:=L_{\exp}(A,E)
=F\odot E
=\begin{bmatrix}
1&2(e-1)\\
3(e-1)&4e
\end{bmatrix}.
$$

另一方面

$$
e^A=\operatorname{diag}(1,e),
$$

$$
e^AE=
\begin{bmatrix}
1&2\\3e&4e
\end{bmatrix},
\qquad
Ee^A=
\begin{bmatrix}
1&2e\\3&4e
\end{bmatrix}.
$$

它们都与 $L$ 不同，因为 $A$ 与 $E$ 不交换。

最后

$$
AL-LA
=\begin{bmatrix}
0&-2(e-1)\\
3(e-1)&0
\end{bmatrix},
$$

而

$$
e^AE-Ee^A
=\begin{bmatrix}
0&2-2e\\
3e-3&0
\end{bmatrix}.
$$

两式逐项相同，交换子恒等式成立。

### MA-FR-B03：SPD 平方根的 Sylvester 方程

$$
X=A^{1/2}=\operatorname{diag}(1,2).
$$

若 $X=\operatorname{diag}(x_1,x_2)$，Sylvester 方程逐元素成为

$$
(x_i+x_j)Z_{ij}=E_{ij}.
$$

因此

$$
Z=
\begin{bmatrix}
2/(1+1)&3/(1+2)\\
3/(2+1)&8/(2+2)
\end{bmatrix}
=\begin{bmatrix}1&1\\1&2\end{bmatrix}.
$$

平方根除差为

$$
\sqrt{\cdot}[\lambda_i,\lambda_j]
=\frac1{\sqrt{\lambda_i}+\sqrt{\lambda_j}},
$$

所以 $F\odot E$ 给出同一个 $Z$。因为 $E=E^*$ 且分母关于 $i,j$ 对称，$Z=Z^*$。

若第二个特征值改为 $\varepsilon^2$，则 $x_2=\varepsilon$，

$$
Z_{22}=\frac{E_{22}}{2\varepsilon}
=\frac4\varepsilon.
$$

它最先发散。非对角项分母为 $1+\varepsilon$，仍保持有界。

## C 级：推导与证明

### MA-FR-C01：多项式与块矩阵定理

对 $k=1$，$L_z(A,E)=E$，公式成立。假设

$$
L_{z^k}(A,E)=\sum_{j=0}^{k-1}A^jEA^{k-1-j}.
$$

由 $A^{k+1}=A^kA$ 和乘积规则：

$$
\begin{aligned}
L_{z^{k+1}}(A,E)
&=L_{z^k}(A,E)A+A^kE\\
&=\sum_{j=0}^{k-1}A^jEA^{k-j}+A^kE\\
&=\sum_{j=0}^{k}A^jEA^{k-j}.
\end{aligned}
$$

归纳完成。

记

$$
\mathcal A_E=\begin{bmatrix}A&E\\0&A\end{bmatrix}.
$$

对 $k=1$ 块公式显然。若对 $k$ 成立，则

$$
\begin{aligned}
\mathcal A_E^{k+1}
&=
\begin{bmatrix}
A^k&\sum_{j=0}^{k-1}A^jEA^{k-1-j}\\
0&A^k
\end{bmatrix}
\begin{bmatrix}A&E\\0&A\end{bmatrix}\\
&=
\begin{bmatrix}
A^{k+1}&A^kE+\sum_{j=0}^{k-1}A^jEA^{k-j}\\
0&A^{k+1}
\end{bmatrix}\\
&=
\begin{bmatrix}
A^{k+1}&L_{z^{k+1}}(A,E)\\
0&A^{k+1}
\end{bmatrix}.
\end{aligned}
$$

对

$$
p(z)=\sum_{k=0}^ma_kz^k
$$

逐项线性组合，得到

$$
p(\mathcal A_E)
=\begin{bmatrix}p(A)&L_p(A,E)\\0&p(A)\end{bmatrix}.
$$

推广到一般矩阵函数可使用：

- 在包含相关谱的区域内收敛的幂级数；
- 与 Jordan 导数数据相配的 Hermite 插值多项式；
- Cauchy 积分公式和 resolvent 的块逆。

需要保证 $f$ 在增广矩阵相关谱上有足够光滑性/解析性，并且选择的是一致的主分支。

块公式给出一种通用构造，但 $2n$ 阶稠密函数的成本、存储和误差传播通常显著高于专用导数算法。数学等价不规定生产实现。

### MA-FR-C02：指数积分公式与伴随

展开积分核：

$$
e^{(1-s)A}Ee^{sA}
=\sum_{p,q\ge0}
\frac{(1-s)^ps^q}{p!q!}A^pEA^q.
$$

逐项积分，并使用

$$
\int_0^1(1-s)^ps^q\,ds
=\frac{p!q!}{(p+q+1)!},
$$

得

$$
\int_0^1e^{(1-s)A}Ee^{sA}\,ds
=\sum_{p,q\ge0}
\frac{A^pEA^q}{(p+q+1)!}.
$$

令 $k=p+q+1$，这正是

$$
\sum_{k=1}^{\infty}\frac1{k!}
\sum_{p=0}^{k-1}A^pEA^{k-1-p}
=L_{\exp}(A,E).
$$

若 $AE=EA$，则

$$
e^{(1-s)A}Ee^{sA}=e^AE,
$$

积分区间长度为 $1$，故 $L_{\exp}(A,E)=e^AE$。

对任意 $G,E$，令

$$
P_s=e^{(1-s)A},
\qquad Q_s=e^{sA}.
$$

矩阵乘法算子 $E\mapsto P_sEQ_s$ 的 Frobenius 伴随是

$$
G\mapsto P_s^*GQ_s^*.
$$

所以

$$
\begin{aligned}
\langle G,L_{\exp}(A,E)\rangle_F
&=\int_0^1\langle G,P_sEQ_s\rangle_F\,ds\\
&=\int_0^1\langle P_s^*GQ_s^*,E\rangle_F\,ds\\
&=\langle L_{\exp}(A^*,G),E\rangle_F.
\end{aligned}
$$

故

$$
L_{\exp}(A)^*(G)=L_{\exp}(A^*,G).
$$

实矩阵损失

$$
\ell(A)=\langle G,e^A\rangle_F
$$

满足

$$
\boxed{
\nabla_A\ell=L_{\exp}(A^T,G)
}.
$$

这里要把上游测量拉回输入，因此使用伴随；导数是否可逆与求梯度无关。

### MA-FR-C03：平方导数的 Kronecker 形式与条件数

列 `vec` 下：

$$
\operatorname{vec}(AE)
=(I\otimes A)\operatorname{vec}(E),
$$

$$
\operatorname{vec}(EA)
=(A^T\otimes I)\operatorname{vec}(E).
$$

所以

$$
\operatorname{vec}(AE+EA)
=\left(I\otimes A+A^T\otimes I\right)\operatorname{vec}(E).
$$

即

$$
K_f(A)=I\otimes A+A^T\otimes I.
$$

当 $A=\operatorname{diag}(\alpha,\beta)$，列 `vec` 顺序为

$$
(E_{11},E_{21},E_{12},E_{22}),
$$

故

$$
K_f(A)
=\operatorname{diag}
\left(2\alpha,\alpha+\beta,
\alpha+\beta,2\beta\right).
$$

Frobenius 诱导绝对条件数是这个对角矩阵的谱范数：

$$
\boxed{
\operatorname{cond}_{\mathrm{abs}}(f,A)
=\max\{|2\alpha|,|\alpha+\beta|,|2\beta|\}
}.
$$

若 $\alpha=-\beta$，两个非对角方向的一阶因子 $\alpha+\beta$ 为零。这是因为对相应 $E$ 有 $AE=-EA$，从而 $AE+EA=0$。

但导数算子并不整体为零：只要 $\alpha\ne0$，对角方向仍分别有 $2\alpha$ 和 $-2\alpha$ 的响应。

## D 级：边界、反例与纠错

### MA-FR-D01：方向导数存在但不是 Fréchet 导数

沿方向 $(a,b)$ 取 $(x,y)=t(a,b)$。若 $(a,b)\ne(0,0)$：

$$
\phi(ta,tb)
=\frac{t^3a^3}{t^2(a^2+b^2)}
=t\frac{a^3}{a^2+b^2}.
$$

因此方向导数为

$$
G_\phi(0;(a,b))
=\frac{a^3}{a^2+b^2}.
$$

它对每个方向存在，但

$$
G(1,0)=1,
\qquad
G(0,1)=0,
$$

而

$$
G(1,1)=\frac12
\ne1+0.
$$

方向结果不满足可加性，因此不可能是线性映射。

对矩阵值函数，沿方向 $H$：

$$
G_F(0;H)
=\frac{h_{11}^3}{h_{11}^2+h_{22}^2}I_2
$$

（分母非零时），同样不对 $H$ 线性。所以 $F$ 在零矩阵处不 Fréchet 可微。

它反驳的是：“只要所有方向导数存在，就自动得到一个 Fréchet/Jacobian 线性化”。还需要线性、连续兼容和统一余项。

### MA-FR-D02：重复谱、eig 基与矩阵函数

因为 $A=\lambda I_n$ 与所有 $E$ 可交换：

$$
\boxed{
L_{\exp}(A,E)=e^AE=e^\lambda E
}.
$$

$A$ 的任意正交/酉基都是特征向量基，完全不唯一。若实现输出某一组 eig 向量，输入发生微小扰动时算法可以选择另一组基；在重特征子空间内部没有天然的单向量对应关系，因此 eig 向量导数可能不唯一或依赖规范。

但矩阵函数值

$$
e^A=e^\lambda I
$$

不依赖基选择，其除差在所有位置都是 $e^\lambda$，所以导数明确。

实现纪律是：对矩阵函数使用连续除差

$$
f[\lambda_i,\lambda_j]\to f'(\lambda)
$$

或 Schur/块算法；不要把特征向量导数中出现的裸 $1/(\lambda_i-\lambda_j)$ 直接当成矩阵函数导数。

### MA-FR-D03：验证与物化的双重陷阱

$A$ 有

$$
n^2=3000^2=9\times10^6
$$

个坐标，因此

$$
K_f(A)\in\mathbb R^{9\times10^6\;\times\;9\times10^6}.
$$

元素数为

$$
(9\times10^6)^2=8.1\times10^{13}.
$$

float64 存储量为

$$
8.1\times10^{13}\times8
=6.48\times10^{14}\ \text{bytes}
=0.648\ \text{PB}.
$$

这还没有计算工作区和副本。

在 $h=10^{-16}$ 做一次前向差分时，$f(A+hE)$ 可能在浮点表示中与 $f(A)$ 几乎相同，减法发生严重相消；除以极小 $h$ 又放大求值误差。因此一次结果无论好坏都没有充分诊断力。

更可靠的方案是取例如

$$
h\in\{10^{-1},10^{-2},10^{-3},10^{-4},10^{-5},10^{-6},10^{-7},10^{-8}\},
$$

同时记录：

1. Taylor 余项 $\|f(A+hE)-f(A)-hL(A,E)\|$；
2. 前向/中心差分与 $L(A,E)$ 的误差；
3. 误差曲线的下降斜率和舍入地板；
4. 多个尺度归一化后的方向；
5. 函数计算自身的残差与定义域距离。

不物化路线是：

- JVP：直接实现 `frechet(A, E)`；
- VJP：直接实现 `frechet_adjoint(A, G)`；
- 验证：随机 $E,G$ 检查
  $$
  \langle G,L(A,E)\rangle_F
  \approx\langle L(A)^*(G),E\rangle_F;
  $$
- 大规模输出若只需作用于向量，再实现 $L(A,E)b$ 的 action。

## E 级：AI 迁移

### AI-FR-E01：连续时间 SSM 的可训练离散化

把 $X=\Delta A$ 看作指数的输入。对 $A$ 的方向 $E$，$X$ 的方向是 $\Delta E$，所以

$$
\boxed{
d_AA_d[E]
=L_{\exp}(\Delta A,\Delta E)
}.
$$

对标量 $\Delta$：

$$
\frac{\partial A_d}{\partial\Delta}
=L_{\exp}(\Delta A,A).
$$

$A$ 与 $\Delta A$ 可交换，因此

$$
\boxed{
\frac{\partial A_d}{\partial\Delta}
=Ae^{\Delta A}=e^{\Delta A}A
}.
$$

前者允许任意矩阵方向 $E$，通常不与 $A$ 交换，必须保留 Fréchet 算子；后者只有一个方向 $A$，恰好与基点 $\Delta A$ 交换。

若上游为 $G$，实 Frobenius 内积下

$$
\begin{aligned}
d\ell
&=\langle G,L_{\exp}(\Delta A,\Delta E)\rangle_F\\
&=\left\langle
\Delta L_{\exp}(\Delta A^T,G),E
\right\rangle_F.
\end{aligned}
$$

故

$$
\boxed{
\nabla_A\ell
=\Delta L_{\exp}(\Delta A^T,G)
}.
$$

非正规诊断至少包括：

1. $\|e^{tA}\|$ 的有限时间峰值，而不只看谱横坐标；
2. Fréchet/Taylor 方向放大或条件估计；
3. Schur 非对角耦合、特征向量条件或 resolvent/伪谱代理；
4. VJP 伴随点积测试；
5. dtype、scaling–squaring 阶段和梯度范数；
6. 不同 $\Delta$ 下的稳定性与梯度尺度。

### AI-FR-E02：阻尼白化层的隐式导数

令

$$
X=A^{1/2},
\qquad X^2=A.
$$

对 $A$ 的方向 $E=dC$（若 $\varepsilon$ 固定）求导：

$$
\boxed{XZ+ZX=E},
\qquad Z=dX.
$$

又因 $W=X^{-1}$：

$$
\boxed{
dW=-X^{-1}ZX^{-1}
}.
$$

在特征值 $\lambda$ 的对角方向，标量增益是

$$
\frac{d}{d\lambda}(\lambda+\varepsilon)^{-1/2}
=-\frac1{2(\lambda+\varepsilon)^{3/2}}.
$$

所以当 $\lambda_{\min}(C)\to0$ 时，固定 $\varepsilon>0$ 把最坏对角增益限制在约

$$
\frac1{2\varepsilon^{3/2}}.
$$

$\varepsilon$ 越大越稳定，但白化偏差也越大。

重复特征值处正确除差取导数极限，并不需要裸 eig-gap 分母。若实现先对特征向量求导再人工除 gap，可能制造不存在的奇异性。

两种反向对象必须区分：

- 展开 $k$ 步 Newton–Schulz：求的是有限步算法映射 $W_k(A)$ 的精确程序梯度；
- 隐式 Fréchet：求的是理想主矩阵函数 $A^{-1/2}$ 的导数，前提是函数定义域和 Sylvester 条件满足。

只有当 $W_k$ 与其导数都已充分逼近理想函数时，二者才近似一致；函数值接近不自动保证导数接近。

### AI-FR-E03：矩阵指数层的反向契约与验收

精确 VJP 是

$$
\boxed{
\nabla_A\ell=L_{\exp}(A^T,G)
}
$$

（复数情形使用 $A^*$ 和实 Frobenius 约定）。

实现接口只需接受 `(A, G)` 并返回 `expm_frechet(A.T, G)` 的方向结果；不需要形成 $K_{\exp}(A)$。若同时需要前向值，可选择联合计算 $e^A$ 与方向导数的专用算法。

伴随点积测试：随机取 $E,G$，比较

$$
s_1=\langle G,L_{\exp}(A,E)\rangle_F,
$$

$$
s_2=\langle L_{\exp}(A^T,G),E\rangle_F.
$$

检查相对差

$$
\frac{|s_1-s_2|}{\max(1,|s_1|,|s_2|)}.
$$

中心差分标量测试令

$$
\varphi(A)=\langle G,e^A\rangle_F.
$$

比较

$$
\frac{\varphi(A+hE)-\varphi(A-hE)}{2h}
$$

与

$$
\langle\nabla_A\ell,E\rangle_F.
$$

最小验收报告应包含：

1. **对象**：主 matrix exponential，而非逐元素指数；
2. **定义域/分支**：指数全局定义，若组合 log/sqrt 则另列谱边界；
3. **精度**：输入、内部乘法/求解、输出 dtype；
4. **算法**：scaling–Padé–squaring、Schur 或 block 方法及停止/缩放信息；
5. **映射**：反传的是精确指数的专用 Fréchet，还是某个有限步近似程序；
6. **条件性**：$\|L_{\exp}(A)\|$ 的估计、方向放大或非正规代理；
7. **测试**：多尺度 Taylor/中心差分与伴随点积；
8. **结构**：实/复、batch、共轭、稀疏或参数化切空间；
9. **失败策略**：NaN、溢出、条件估计过大或梯度异常时的降阶、缩放或回退。

## 总结：本组题应形成的能力

完成本组后，应能稳定执行以下闭环：

1. 把导数识别为矩阵空间上的线性算子；
2. 在扰动插入、块矩阵、除差和 Kronecker 表示之间转换；
3. 用 Sylvester 方程处理平方根等隐式矩阵函数；
4. 用伴随而非显式 Jacobian 完成反向传播；
5. 用 Taylor 斜率、中心差分和伴随点积共同验收；
6. 分开报告重复谱、非正规性、结构约束、函数条件性与算法稳定性。

