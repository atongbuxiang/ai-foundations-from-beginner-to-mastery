---
type: solution-set
status: draft
area: [labs, math/linear-algebra, math/matrix-calculus]
prerequisites: ["[[习题 - Kronecker 积、向量化与矩阵方程]]"]
related: ["[[Kronecker 积、向量化与矩阵方程]]", "[[多线性映射、张量与缩并]]", "[[练习与测验 MOC]]"]
sources: ["Petersen-Pedersen-Matrix-Cookbook", "SciPy-solve-sylvester"]
created: 2026-08-16
updated: 2026-08-16
---

# 解答 - Kronecker 积、向量化与矩阵方程

> [!important] 使用方式
> 先独立写出 shape 和指标，再核对本解答。这里不仅给结果，还保留“为何成立、何处容易错、怎样迁移到 AI”的推理链。除非特别说明，`vec` 都按列堆叠。

## A 级：识别与复述

### LA-KV-A01：四种乘积与形状

1. 因为 $A$ 是 $2\times3$、$B$ 是 $4\times5$，所以

   $$
   A\otimes B\in\mathbb R^{(2\cdot4)\times(3\cdot5)}
   =\mathbb R^{8\times15}.
   $$

2. $AB$ 没有定义，因为 $A$ 的列数 $3$ 不等于 $B$ 的行数 $4$。

3. $A\odot B$ 没有定义，因为 Hadamard 积要求两个数组同形，而 $2\times3\ne4\times5$。

4. $uv^T\in\mathbb R^{2\times4}$，它是二阶外积矩阵。若把向量 Kronecker 积写成列向量，则 $u\otimes v\in\mathbb R^8$。两者含有相同的两两乘积，但排列和对象形状不同。

5. 运算的指标结构如下：

   - 矩阵乘法对共享指标求和；
   - Hadamard 积逐元素相乘，不求和；
   - 外积保留两个输入指标，不求和；
   - Kronecker 积保留成对的行、列指标，再把复合指标编码为大矩阵的行、列，不求和。

> [!warning] 常见误区
> “出现乘号”不等于“发生求和”。是否求和必须由指标是否重复并被消去来判断。

### LA-KV-A02：列 `vec` 与软件顺序

列堆叠依次取第 1、2、3 列，因此

$$
\operatorname{vec}(X)
=\begin{bmatrix}1&4&2&5&3&6\end{bmatrix}^T.
$$

row-major flatten 依次读取第 1、2 行：

$$
\operatorname{rvec}(X)
=\begin{bmatrix}1&2&3&4&5&6\end{bmatrix}^T.
$$

二者包含相同元素，只是排列不同。存在一个置换矩阵 $P$ 使

$$
\operatorname{rvec}(X)=P\operatorname{vec}(X).
$$

它也可用交换矩阵表达为

$$
\operatorname{rvec}(X)=\operatorname{vec}(X^T)
=K_{2,3}\operatorname{vec}(X).
$$

显式代码约定是：

```python
# NumPy：Fortran/column-major 顺序
x_col = X.reshape(-1, order="F")

# PyTorch：先转置，再把转置结果变为连续存储并拉平
x_col = X.T.contiguous().reshape(-1)
```

`reshape(-1)` 在常见 NumPy/PyTorch 默认设置下都是 row-major 语义，不能无说明地代入列 `vec` 公式。

### LA-KV-A03：判断六个断言

1. **错。** 一般 $A\otimes B\ne B\otimes A$；二者在相容维数下至多通过行列置换联系。
2. **对。** 逐块取共轭转置，得到 $(A\otimes B)^*=A^*\otimes B^*$。
3. **错。** 正确公式是
   $$
   \operatorname{rank}(A\otimes B)
   =\operatorname{rank}(A)\operatorname{rank}(B).
   $$
4. **对。** 可逆时，Kronecker 积的最大、最小奇异值分别相乘，所以
   $$
   \kappa_2(A\otimes B)=\kappa_2(A)\kappa_2(B).
   $$
5. **错。** 列 `vec` 的正确公式为
   $$
   \operatorname{vec}(AXB)=(B^T\otimes A)\operatorname{vec}(X).
   $$
6. **错。** 唯一性只说明线性算子可逆。最小奇异值或 separation 可以非常小，此时逆算子范数很大，问题仍可能严重病态。

## B 级：手算与构造

### LA-KV-B01：Kronecker 块手算

把 $A$ 的每个标量替换为该标量乘 $B$：

$$
A\otimes B
=\begin{bmatrix}B&-B\\2B&0B\end{bmatrix}
=\begin{bmatrix}
1&2&-1&-2\\
0&3&0&-3\\
2&4&0&0\\
0&6&0&0
\end{bmatrix}.
$$

交换次序则得到

$$
B\otimes A
=\begin{bmatrix}A&2A\\0A&3A\end{bmatrix}
=\begin{bmatrix}
1&-1&2&-2\\
2&0&4&0\\
0&0&3&-3\\
0&0&6&0
\end{bmatrix}.
$$

两个矩阵的 $(1,2)$ 元素分别是 $2$ 与 $-1$，故一般不相等。

又有

$$
\det A=2,
\qquad
\det B=3.
$$

对两个 $2\times2$ 矩阵，行列式公式给出

$$
\det(A\otimes B)
=(\det A)^2(\det B)^2
=2^2\cdot3^2=36.
$$

从块结构也可核对：$A$ 可逆，使用块初等变换或 Kronecker 特征值乘积，结果同样是 $36$。

### LA-KV-B02：数值核对 vec 恒等式

先直接相乘：

$$
AX=
\begin{bmatrix}7&10\\3&4\end{bmatrix},
\qquad
Y=AXB=
\begin{bmatrix}17&10\\7&4\end{bmatrix}.
$$

所以

$$
\operatorname{vec}(Y)
=\begin{bmatrix}17&7&10&4\end{bmatrix}^T.
$$

由于

$$
B^T=\begin{bmatrix}1&1\\0&1\end{bmatrix},
$$

故

$$
B^T\otimes A
=\begin{bmatrix}A&A\\0&A\end{bmatrix}
=\begin{bmatrix}
1&2&1&2\\
0&1&0&1\\
0&0&1&2\\
0&0&0&1
\end{bmatrix}.
$$

而

$$
\operatorname{vec}(X)=\begin{bmatrix}1&3&2&4\end{bmatrix}^T,
$$

于是

$$
(B^T\otimes A)\operatorname{vec}(X)
=\begin{bmatrix}17&7&10&4\end{bmatrix}^T
=\operatorname{vec}(Y).
$$

形状也相容：$4\times4$ 的算子作用于长度 $4$ 的向量，输出正好是 $2\times2$ 矩阵的列 `vec`。

### LA-KV-B03：对角 Sylvester 方程

由于 $A,B$ 均为对角矩阵，逐元素有

$$
(a_i+b_j)x_{ij}=c_{ij}.
$$

因此

$$
x_{11}=\frac3{1+2}=1,
\quad
x_{12}=\frac5{1+4}=1,
\quad
x_{21}=\frac{10}{3+2}=2,
\quad
x_{22}=\frac{14}{3+4}=2,
$$

即

$$
X=\begin{bmatrix}1&1\\2&2\end{bmatrix}.
$$

列 `vec` 下，

$$
(I_2\otimes A+B^T\otimes I_2)\operatorname{vec}(X)
=\operatorname{vec}(C),
$$

其中系数矩阵是

$$
I_2\otimes A+B^T\otimes I_2
=\operatorname{diag}(3,5,5,7).
$$

四个特征值是 $3,5,5,7$，均非零，因此解唯一。直接计算

$$
AX+XB
=\begin{bmatrix}3&5\\10&14\end{bmatrix}=C
$$

完成验证。

## C 级：推导与证明

### LA-KV-C01：混合乘积与谱

对任意简单张量 $x\otimes y$，先后作用两个算子：

$$
\begin{aligned}
(A\otimes B)(C\otimes D)(x\otimes y)
&=(A\otimes B)(Cx\otimes Dy)\\
&=ACx\otimes BDy\\
&=(AC\otimes BD)(x\otimes y).
\end{aligned}
$$

简单张量张成整个张量积空间，因此两个线性算子在一组生成元上相同，便有

$$
(A\otimes B)(C\otimes D)=AC\otimes BD.
$$

若 $Au_i=\lambda_i u_i$、$Bv_j=\mu_jv_j$，则

$$
\begin{aligned}
(A\otimes B)(u_i\otimes v_j)
&=Au_i\otimes Bv_j\\
&=(\lambda_i u_i)\otimes(\mu_jv_j)\\
&=\lambda_i\mu_j(u_i\otimes v_j).
\end{aligned}
$$

所以 $u_i\otimes v_j$ 是特征值 $\lambda_i\mu_j$ 的特征向量。若 $A$ 有 $n$ 个线性无关特征向量、$B$ 有 $m$ 个，则所有 $u_i\otimes v_j$ 形成张量积空间的一组基，共 $nm$ 个方向，因而覆盖全部特征空间维数。

### LA-KV-C02：从指标重建 vec 恒等式

采用从 $0$ 开始的索引以清楚表示线性位置。列 `vec` 中，矩阵 $Z\in\mathbb F^{m\times n}$ 的元素 $z_{ij}$ 位于位置

$$
\alpha=i+mj.
$$

同理，$x_{rs}$ 在 $\operatorname{vec}(X)$ 中的位置是

$$
\beta=r+ps.
$$

Kronecker 积 $B^T\otimes A$ 的相应元素为

$$
(B^T\otimes A)_{i+mj,\,r+ps}
=(B^T)_{js}A_{ir}
=b_{sj}a_{ir}.
$$

因此其第 $i+mj$ 个输出分量是

$$
\begin{aligned}
\big[(B^T\otimes A)\operatorname{vec}(X)\big]_{i+mj}
&=\sum_{r=0}^{p-1}\sum_{s=0}^{q-1}
 b_{sj}a_{ir}x_{rs}\\
&=(AXB)_{ij}\\
&=\big[\operatorname{vec}(AXB)\big]_{i+mj}.
\end{aligned}
$$

每个分量都相等，故

$$
\operatorname{vec}(AXB)=(B^T\otimes A)\operatorname{vec}(X).
$$

这里 $B$ 必须转置，根本原因是：$B$ 的列指标 $j$ 成为输出的慢指标，而被求和的 $s$ 必须与 $X$ 的列块位置对齐。

### LA-KV-C03：Sylvester 唯一性与后验界

分别向量化两项：

$$
\operatorname{vec}(AX)=(I\otimes A)\operatorname{vec}(X),
$$

$$
\operatorname{vec}(XB)=(B^T\otimes I)\operatorname{vec}(X).
$$

故系统为

$$
\left(I\otimes A+B^T\otimes I\right)\operatorname{vec}(X)
=\operatorname{vec}(C).
$$

若 $A=Q_AT_AQ_A^{-1}$、$B^T=Q_BT_BQ_B^{-1}$，其中 $T_A,T_B$ 上三角，则利用混合乘积律，系数矩阵相似于

$$
I\otimes T_A+T_B\otimes I.
$$

该矩阵仍为上三角，其对角元恰为所有

$$
\lambda_i(A)+\lambda_j(B).
$$

因此 Sylvester 算子可逆当且仅当

$$
\lambda_i(A)+\lambda_j(B)\ne0
\quad\text{对所有 }i,j,
$$

等价地，

$$
\operatorname{spec}(A)\cap\operatorname{spec}(-B)=\varnothing.
$$

最后由 separation 定义，对解 $X$ 有

$$
\|C\|_F=\|AX+XB\|_F
\ge \operatorname{sep}(A,-B)\|X\|_F.
$$

当 separation 为正时移项即得

$$
\|X\|_F\le
\frac{\|C\|_F}{\operatorname{sep}(A,-B)}.
$$

这比只看是否唯一更强：它定量描述了逆算子的放大能力。

## D 级：边界、反例与纠错

### LA-KV-D01：row-major 公式错位

本题中

$$
\operatorname{rvec}(X)=\begin{bmatrix}1&2&3&4\end{bmatrix}^T.
$$

沿用 B02 的列 `vec` 系数矩阵会得到

$$
(B^T\otimes A)\operatorname{rvec}(X)
=\begin{bmatrix}16&6&11&4\end{bmatrix}^T.
$$

但

$$
AXB=\begin{bmatrix}17&10\\7&4\end{bmatrix},
$$

所以

$$
\operatorname{rvec}(AXB)
=\begin{bmatrix}17&10&7&4\end{bmatrix}^T.
$$

二者不等。失败并非 vec 恒等式错误，而是公式和存储约定不匹配。row-major 其实等于对转置做 column-major：

$$
\operatorname{rvec}(X)=\operatorname{vec}(X^T).
$$

重新推导可得

$$
\operatorname{rvec}(AXB)
=(A\otimes B^T)\operatorname{rvec}(X).
$$

也可引入交换矩阵 $K$，在列公式两侧做相应置换。原则是：置换必须同时作用于输入、输出和算子，不能只替换向量的读取顺序。

### LA-KV-D02：显式物化的内存灾难

$X$ 有

$$
2000\times2000=4\times10^6
$$

个未知量。因此向量化系数矩阵的形状是

$$
(4\times10^6)\times(4\times10^6),
$$

元素数为

$$
16\times10^{12}.
$$

float64 每个元素 $8$ bytes，所以仅矩阵存储量为

$$
16\times10^{12}\times8
=128\times10^{12}\ \text{bytes}
=128\ \text{TB}.
$$

这还没有计算因子分解、工作区和中间副本。可行路线包括：

1. 先做 Schur 分解，再用 Bartels–Stewart 型三角回代；
2. 只实现算子 $X\mapsto AX+XB$ 和它的伴随，用 Krylov 迭代法；
3. 对低秩右端使用低秩 ADI、rational Krylov 等低秩方法；
4. 在稀疏情形中保留 $A,B$ 的稀疏结构，绝不形成 Kronecker 和。

`vec` 形式仍然有理论价值：它揭示可逆条件、谱、Jacobian、伴随和条件数，也提供迭代法所需的算子解释；“不物化”不等于“不使用该数学表示”。

### LA-KV-D03：特征值离零但 separation 很小

$B=[0]$，而 $A_K$ 的特征值恒为 $1,2$，所以任何有限 $K$ 下 $A_K$ 都可逆，唯一性不变。

对

$$
x=\begin{bmatrix}-K\\1\end{bmatrix},
$$

有

$$
A_Kx
=\begin{bmatrix}1&K\\0&2\end{bmatrix}
\begin{bmatrix}-K\\1\end{bmatrix}
=\begin{bmatrix}0\\2\end{bmatrix}.
$$

因此由 separation 的最小化定义，代入这个非零试探向量：

$$
\operatorname{sep}(A_K,0)
\le\frac{\|A_Kx\|_2}{\|x\|_2}
=\frac2{\sqrt{K^2+1}}.
$$

该上界随 $|K|$ 增大趋于 $0$。这里特征值始终远离 $0$，但矩阵越来越非正规，特征向量基越来越病态，最小奇异值却可变得很小。因此非正规问题的条件性必须看奇异值、separation 或伪谱，不能只看特征值距离。

## E 级：AI 迁移

### AI-KV-E01：K-FAC 的精确式与近似式

对线性层 $y=Wx$，链式法则给出

$$
G=\nabla_W\ell=\delta x^T,
$$

其 shape 是 $d_{out}\times d_{in}$。利用列 `vec` 公式

$$
\operatorname{vec}(ab^T)=b\otimes a,
$$

得到

$$
g:=\operatorname{vec}(G)=x\otimes\delta.
$$

单样本梯度外积是精确恒等式：

$$
\begin{aligned}
gg^T
&=(x\otimes\delta)(x\otimes\delta)^T\\
&=(xx^T)\otimes(\delta\delta^T).
\end{aligned}
$$

对数据分布取期望仍然精确：

$$
F=\mathbb E\left[(xx^T)\otimes(\delta\delta^T)\right].
$$

K-FAC 再作因子化近似：

$$
\boxed{
\mathbb E\left[(xx^T)\otimes(\delta\delta^T)\right]
\approx
\mathbb E[xx^T]\otimes\mathbb E[\delta\delta^T]
}
$$

框中的期望拆分不是代数恒等式；它相当于忽略激活二阶统计与反向信号二阶统计之间的某些依赖。报告实验时必须把“梯度外积的精确 Kronecker 结构”与“期望的统计近似”分开。

### AI-KV-E02：可分离协方差

由 Kronecker 逆公式，

$$
\Sigma^{-1}=\Sigma_c^{-1}\otimes\Sigma_r^{-1}.
$$

由于 $\Sigma_c$ 是 $n\times n$、$\Sigma_r$ 是 $m\times m$，

$$
\det(\Sigma_c\otimes\Sigma_r)
=(\det\Sigma_c)^m(\det\Sigma_r)^n,
$$

所以

$$
\log\det\Sigma
=m\log\det\Sigma_c+n\log\det\Sigma_r.
$$

SPD 矩阵的二范数条件数满足

$$
\kappa_2(\Sigma)
=\kappa_2(\Sigma_c)\kappa_2(\Sigma_r).
$$

若真实协方差只是近似可分离，应至少分别报告：

1. **模型误差**：例如 $\|\widehat\Sigma-\Sigma_c\otimes\Sigma_r\|/\|\widehat\Sigma\|$，描述结构假设偏差；
2. **数值误差**：线性求解残差、舍入误差和因子条件数，描述在既定近似模型上的计算可靠性。

两者不能合并为一个“误差”，因为改善求解精度无法消除错误的可分离假设。

### AI-KV-E03：隐式层中的矩阵线性化

列 `vec` 下的理论 Jacobian/线性系统为

$$
\underbrace{(I_n\otimes A+B^T\otimes I_m)}_{J}
\operatorname{vec}(X)=\operatorname{vec}(C).
$$

唯一性条件是

$$
\lambda_i(A)+\lambda_j(B)\ne0
\quad\text{对所有 }i,j,
$$

也就是

$$
\operatorname{spec}(A)\cap\operatorname{spec}(-B)=\varnothing.
$$

但实现中 $J$ 有 $(mn)^2$ 个元素，显式构造会破坏原问题的矩阵结构、增加存储与计算量，并妨碍使用 Schur、Krylov、低秩或稀疏算法。更合适的实现契约是提供

$$
X\longmapsto AX+XB
$$

以及反向所需的伴随算子

$$
Y\longmapsto A^*Y+YB^*,
$$

然后用结构化直接法或 matrix-free 迭代法求解。还应同时检查残差与 separation/条件估计：有唯一解不保证反向传播稳定。

## 总结：本组题应形成的能力

完成本组后，应能稳定完成以下闭环：

1. 先确定 vec 顺序与复合指标；
2. 从指标推导 Kronecker 算子，而不是背转置位置；
3. 区分可逆性、条件性和求解算法；
4. 用结构化算子解释 Jacobian，但不盲目物化；
5. 在 K-FAC 等应用中明确标出精确等式与统计近似的分界。

