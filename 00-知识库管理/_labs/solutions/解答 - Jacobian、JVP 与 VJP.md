---
type: solution
status: draft
area: [labs, math/calculus, math/linear-algebra, math/matrix-calculus, ai/automatic-differentiation]
prerequisites: ["[[习题 - Jacobian、JVP 与 VJP]]"]
related: ["[[Jacobian、JVP 与 VJP]]", "[[Hessian、二阶微分与曲率]]", "[[多元链式法则与计算图]]", "[[矩阵微分、迹技巧与布局约定]]", "[[自动微分：前向、反向与高阶模式]]", "[[练习与测验 MOC]]"]
sources: ["MIT-18.S096-Derivatives-Linear-Operators", "MIT-18.S096-Jacobians-Matrix-Functions", "JAX-JVP-VJP-Official", "JAX-JVP-API", "JAX-VJP-API", "PyTorch-Func-Transforms", "Baydin-2018-AD-Survey", "Su-10958-JVP"]
created: 2026-08-17
updated: 2026-08-17
---

# 解答 - Jacobian、JVP 与 VJP

> [!abstract] 使用说明
> 本解答采用“算子—坐标—作用—验证”顺序：先写 $DF(x)$ 的方向和空间，再决定是否使用 Jacobian；JVP 沿输入切向量向前，VJP 把输出协向量向后回拉；最后用有限差分和伴随点积从不同侧面验证。请勿只核对矩阵乘法结果。

## A 级：对象、类型与接口语言

### CALC-JV-A01：翻译十四个声明

#### 1. 导数算子

$$
DF(x)\in\mathcal L(X,Y)
$$

表示 $F:X\to Y$ 在 $x$ 的 Fréchet 导数是从输入扰动空间 $X$ 到输出扰动空间 $Y$ 的连续线性算子。

#### 2. Jacobian 坐标矩阵

$$
J_F(x)\in\mathbb R^{m\times n}
$$

表示 $F:\mathbb R^n\to\mathbb R^m$ 的导数在所选输入、输出基下由 $m$ 行、$n$ 列矩阵表示。本库用输出坐标为行、输入坐标为列。

#### 3. 分量偏导

$$
(J_F)_{ij}=\frac{\partial F_i}{\partial x_j}
$$

表示第 $j$ 个输入坐标对第 $i$ 个输出坐标的一阶影响。需要 $F$ 已可微或满足足够条件使偏导表确实表示统一导数。

#### 4. 列解释

$$
J_{:j}=DF(x)[e_j]
$$

在标准坐标中表示 Jacobian 第 $j$ 列是沿第 $j$ 个输入基向量的输出一阶响应。

#### 5. JVP

$$
\operatorname{JVP}_{F,x}(v)=DF(x)[v]
$$

输入 $v\in X$，输出属于 $Y$。在坐标中为 $Jv$，它是 tangent pushforward。

#### 6. 对偶映射

$$
A':Y^*\to X^*
$$

表示线性映射 $A:X\to Y$ 把输出协向量回拉为输入协向量。定义只需线性结构，不需内积。

#### 7. 对偶配对恒等式

$$
(A'u^*)[v]=u^*[Av]
$$

左边先回拉输出协向量再测量输入向量；右边先向前作用再由输出协向量测量。两者是同一个标量。

#### 8. VJP

$$
\operatorname{VJP}_{F,x}(u^*)=DF(x)'[u^*]
$$

输入属于 $Y^*$，输出属于 $X^*$。它是 cotangent pullback。

#### 9. 欧氏伴随恒等式

$$
u^\top(Jv)=(J^\top u)^\top v
$$

表示标准欧氏配对下 JVP 与 VJP 互为伴随；常用于点积测试。

#### 10. 加权伴随

$$
J^\dagger=M_X^{-1}J^\top M_Y
$$

是在输入内积 $v^\top M_Xw$、输出内积 $y^\top M_Yu$ 下表示伴随的矩阵。普通转置只是 $M_X=M_Y=I$ 的特例。

#### 11. 标量输出梯度

$$
\nabla f=J_f^\top1
$$

标量函数的 Jacobian 是一行；输出协向量空间一维，以 $1$ 为 VJP seed 后，在欧氏内积下得到梯度列。

#### 12. Jacobian 坐标变换

若 $x=Sz,y=Tu$，新坐标函数为 $\widetilde F(z)=T^{-1}F(Sz)$，则

$$
J_{\widetilde F}=T^{-1}J_FS.
$$

矩阵变化是同一抽象算子的坐标变化。

#### 13. 正规算子作用

$$
J^\top Jv
$$

先用 JVP 得到 $Jv$，再把该输出向量作为欧氏 cotangent seed 做 VJP。结果属于输入空间坐标，不必形成 $J$。

#### 14. 全一输出种子

$$
J^\top\mathbf1
=\nabla\left(\sum_iF_i\right)
$$

表示输出各分量之和的欧氏梯度，不是完整 Jacobian。

### CALC-JV-A02：判断十八个断言

1. **错。** 坐标无关对象是 $DF(x)$；Jacobian 是基下表示。
2. **对。** 本库采用输出行、输入列，因此形状 $m\times n$。
3. **错。** 偏导存在不推出 Fréchet 可微；需要统一余项或连续偏导等充分条件。
4. **对。** tangent 对应被扰动 primal 的结构和形状。
5. **错。** JVP 输出与函数输出同结构；当 $m\ne n$ 时通常不与输入 tangent 同形。
6. **对。** 它测量输出一阶扰动。
7. **错。** $A'u^*=u^*\circ A$ 不需要内积。
8. **对。** 标准欧氏基/配对下回拉数组是 $J^\top u$。
9. **错。** 加权伴随为 $M_X^{-1}J^\top M_Y$。
10. **错。** 转置回拉协向量；逆映射输出向量，类型与存在条件不同。矩形 $J$ 甚至没有两侧逆。
11. **对。** $Je_j$ 是第 $j$ 列。
12. **对。** $(J^\top e_i)^\top$ 是第 $i$ 行。
13. **对。** 标量输出唯一对偶基种子是 $1$。
14. **错。** 得到 $J^\top\mathbf1$，即行和/输出和的梯度。
15. **对，作为基本经验。** full $J$ 需要 $n$ 列探针，少于 $m$ 个行探针；仍需 profiling。
16. **错。** 反向内存受计算图深度、保存中间量、batch 和实现策略影响。
17. **错。** 它只说明被测两个黑箱作用互为伴随；可能共同实现框架在不可微点的约定。
18. **错。** 返回数组通常表示欧氏/Frobenius 配对下的微分坐标；其他度量梯度还需 Riesz 逆映射。

### CALC-JV-A03：为十二个任务选择最直接工具

| 任务 | 工具 | 关键说明 |
|---|---|---|
| 1 | Fréchet 余项 | 检查统一 $o(\|h\|)$ |
| 2 | Jacobian 坐标矩阵 | 小型全敏感度表 |
| 3 | JVP | 已知输入 tangent，输出 $Jv$ |
| 4 | VJP | 输出 scalarization/cotangent 回拉 |
| 5 | 输入基探针 | $Je_j$ 逐列恢复 |
| 6 | 输出对偶基探针 | $J^\top e_i$ 转置后逐行恢复 |
| 7 | 加权伴随 | $M_X^{-1}J^\top M_Y$ |
| 8 | `vec`/Kronecker | $B^\top\otimes A$，需声明展平顺序 |
| 9 | 方向中心差分 | 扫描步长，比较 $Jv$ |
| 10 | 伴随点积测试 | 比较 $\langle u,Jv\rangle$ 与 $\langle J^\top u,v\rangle$ |
| 11 | `vmap`/批量探针 | 向量化输出基或样本级变换 |
| 12 | profiling | 维数规则只给起点，实际硬件计时决定 |

## B 级：手算、形状与种子

### CALC-JV-B01：一个 $\mathbb R^2\to\mathbb R^3$ 映射

#### 1. Jacobian

$$
J_F(x,y)=
\begin{bmatrix}
y&x\\
e^x&1\\
2x&-2y
\end{bmatrix}.
$$

在 $a=(0,1)$，

$$
\boxed{
J=\begin{bmatrix}
1&0\\
1&1\\
0&-2
\end{bmatrix}.}
$$

#### 2. 两列

$$
Je_1=(1,1,0)^\top,
\qquad
Je_2=(0,1,-2)^\top.
$$

第一列是只扰动 $x$ 的输出响应；第二列是只扰动 $y$ 的响应。

#### 3. JVP

对 $v=(2,-1)^\top$，

$$
Jv=
\begin{bmatrix}
2\\1\\2
\end{bmatrix}.
$$

#### 4. VJP

对 $u=(1,3,-2)^\top$，

$$
J^\top u
=\begin{bmatrix}
1&1&0\\
0&1&-2
\end{bmatrix}
\begin{bmatrix}1\\3\\-2\end{bmatrix}
=\boxed{(4,7)^\top}.
$$

#### 5. 点积测试

$$
u^\top(Jv)=1\cdot2+3\cdot1-2\cdot2=1,
$$

而

$$
(J^\top u)^\top v=4\cdot2+7\cdot(-1)=1.
$$

#### 6. 三个输出种子

$$
J^\top e_1=(1,0)^\top,
\quad
J^\top e_2=(1,1)^\top,
\quad
J^\top e_3=(0,-2)^\top.
$$

把它们转置并按行排列，恢复 $J$。

#### 7. 标量化函数

$$
\phi(x,y)=xy+3(e^x+y)-2(x^2-y^2).
$$

所以

$$
\nabla\phi(x,y)
=\begin{bmatrix}
y+3e^x-4x\\
x+3+4y
\end{bmatrix}.
$$

在 $(0,1)$ 得

$$
\nabla\phi(a)=(4,7)^\top=J^\top u.
$$

### CALC-JV-B02：由黑箱作用恢复矩阵

#### 1. 恢复矩阵

三次基 JVP 直接给列：

$$
\boxed{
J=\begin{bmatrix}
1&-1&3\\
2&0&4
\end{bmatrix}.}
$$

#### 2. 一般 JVP

$$
J\begin{bmatrix}2\\-1\\1\end{bmatrix}
=\begin{bmatrix}2+1+3\\4+0+4\end{bmatrix}
=\boxed{(6,8)^\top}.
$$

#### 3. VJP

$$
J^\top\begin{bmatrix}2\\-3\end{bmatrix}
=\begin{bmatrix}
1&2\\-1&0\\3&4
\end{bmatrix}
\begin{bmatrix}2\\-3\end{bmatrix}
=\boxed{(-4,-2,-6)^\top}.
$$

#### 4. 输出基种子

$$
J^\top e_1=(1,-1,3)^\top,
\qquad
J^\top e_2=(2,0,4)^\top.
$$

它们转置后是 $J$ 的两行。

#### 5. 只用 VJP 恢复

依次调用输出对偶基 $e_1,e_2$，得到 $J^\top e_i$；转置每个结果并按 $i$ 堆叠即可。

#### 6. 相对伴随残差

对随机 $v,u$，定义

$$
s_f=u^\top\widehat{\operatorname{JVP}}(v),
\qquad
s_r=\widehat{\operatorname{VJP}}(u)^\top v,
$$

并报告

$$
\eta_{\rm adj}
=\frac{|s_f-s_r|}{\max(1,|s_f|,|s_r|)}.
$$

#### 7. 证据边界

三次列探针只确定某个点上黑箱线性作用的坐标。一个非线性程序可能只在这些方向返回设定值，却没有统一余项；也可能基点附近不连续。Fréchet 可微还需检查所有小扰动的统一一阶模型。

### CALC-JV-B03：批量线性层与广播

#### 1. 总 JVP

$$
\boxed{
\dot Y=\dot W X+W\dot X+\dot b\mathbf1_B^\top.}
$$

三项形状均为 $p\times B$。

#### 2. 总 VJP

在 Frobenius 配对下：

$$
\boxed{
\bar W=UX^\top,
\qquad
\bar X=W^\top U,
\qquad
\bar b=U\mathbf1_B.}
$$

形状分别为 $p\times q,q\times B,p$。

#### 3. 伴随恒等式

$$
\boxed{
\langle U,\dot Y\rangle_F
=\langle\bar W,\dot W\rangle_F
+\langle\bar X,\dot X\rangle_F
+\bar b^\top\dot b.}
$$

#### 4. 广播反向求和

$\dot b$ 在前向被复制到 $B$ 列。输出每列对同一个 $b$ 的协向量贡献必须相加，故

$$
\bar b=\sum_{j=1}^B U_{:j}=U\mathbf1_B.
$$

#### 5. mean 与 sum

若总损失由 batch sum 改成 batch mean，输出 seed 和所有输入 cotangent 均多一个 $1/B$ 因子。

#### 6. 只对 $W$ 求导

定义单输入函数

$$
G(W)=WX+b\mathbf1_B^\top,
$$

把 $X,b$ 闭包为固定量。此时 tangent 只有 $\dot W$，JVP 为 $\dot W X$，VJP 返回 $UX^\top$。

#### 7. per-example 与聚合

聚合权重梯度形状是 $p\times q$：

$$
\bar W=\sum_{j=1}^B U_{:j}X_{:j}^\top.
$$

per-example 权重梯度保留 batch 轴，形状为 $B\times p\times q$，第 $j$ 个块为

$$
U_{:j}X_{:j}^\top.
$$

## C 级：证明与理论重建

### CALC-JV-C01：Jacobian 的表示定理与坐标变换

#### 1. 线性算子的矩阵表示

设

$$
h=\sum_{j=1}^nh_je_j,
\qquad
A[e_j]=\sum_{i=1}^mJ_{ij}f_i.
$$

由 $A$ 线性，

$$
\begin{aligned}
A[h]
&=\sum_jh_jA[e_j]\\
&=\sum_jh_j\sum_iJ_{ij}f_i\\
&=\sum_i\left(\sum_jJ_{ij}h_j\right)f_i.
\end{aligned}
$$

输出第 $i$ 个坐标为 $\sum_jJ_{ij}h_j$，所以

$$
[A h]_{\mathcal B_Y}=J[h]_{\mathcal B_X}.
$$

#### 2. 分量偏导公式

若 $F$ 在 $x$ 可微，则

$$
DF(x)[e_j]
=\lim_{t\to0}\frac{F(x+te_j)-F(x)}t.
$$

取第 $i$ 个输出坐标，得到

$$
[DF(x)[e_j]]_i
=\lim_{t\to0}\frac{F_i(x+te_j)-F_i(x)}t
=\partial_jF_i(x).
$$

而左边正是 $J_{ij}$，故

$$
J_{ij}=\partial_jF_i.
$$

#### 3. 列解释

把 $h=e_j$ 代入 $[DF(x)[h]]=J[h]$：

$$
[DF(x)[e_j]]=Je_j=J_{:j}.
$$

#### 4. 输入/输出换坐标

若

$$
x=Sz,
\qquad
y=Tu,
\qquad
\widetilde F(z)=T^{-1}F(Sz),
$$

则小扰动按

$$
h_x=Sh_z
$$

变换。输出一阶扰动在新坐标中为

$$
h_u=T^{-1}J_Fh_x
=T^{-1}J_FSh_z.
$$

所以

$$
\boxed{J_{\widetilde F}=T^{-1}J_FS.}
$$

#### 5. tangent 变换

输入 tangent：

$$
v_x=Sv_z.
$$

输出 tangent：

$$
w_y=Tw_u,
\qquad
w_u=T^{-1}w_y.
$$

于是

$$
J_{\widetilde F}v_z=T^{-1}J_Fv_x.
$$

#### 6. cotangent 变换

保持标量配对。输出侧：

$$
u_y^\top\delta y
=u_u^\top\delta u,
\qquad
\delta y=T\delta u.
$$

故

$$
u_u=T^\top u_y.
$$

输入侧同理：

$$
\bar x^\top\delta x
=\bar z^\top\delta z,
\qquad
\delta x=S\delta z,
$$

故

$$
\bar z=S^\top\bar x.
$$

并且

$$
J_{\widetilde F}^\top u_u
=S^\top J_F^\top T^{-\top}u_u
=S^\top J_F^\top u_y,
$$

与输入协向量变换一致。

#### 7. 抽象算子没有改变

$S,T$ 只改变输入、输出向量的坐标编码；$J$ 的元素因此按 $T^{-1}JS$ 变化。几何中的实际扰动 $h$ 与一阶输出 $A[h]$ 没变，改变的是它们的数字列表和矩阵表示。

### CALC-JV-C02：对偶回拉、伴随与加权度量

#### 1. 定义与线性

对 $u^*\in Y^*$，定义

$$
A'u^*=u^*\circ A.
$$

对标量 $\alpha,\beta$ 和 $u^*,w^*$：

$$
\begin{aligned}
A'(\alpha u^*+\beta w^*)
&=(\alpha u^*+\beta w^*)\circ A\\
&=\alpha(u^*\circ A)+\beta(w^*\circ A)\\
&=\alpha A'u^*+\beta A'w^*.
\end{aligned}
$$

所以 $A'$ 线性。

#### 2. 配对恒等式

由函数复合定义，对每个 $v\in X$，

$$
(A'u^*)[v]
=(u^*\circ A)[v]
=u^*[Av].
$$

#### 3. 欧氏坐标

若 $u^*$ 用行 $u^\top$ 表示，$A$ 用 $J$ 表示，则

$$
(A'u^*)[v]
=u^\top Jv
=(J^\top u)^\top v.
$$

所以回拉协向量的列数组为 $J^\top u$。

#### 4. 加权伴随

要求

$$
\langle Jv,u\rangle_Y
=\langle v,J^\dagger u\rangle_X.
$$

代入内积：

$$
v^\top J^\top M_Yu
=v^\top M_XJ^\dagger u.
$$

对所有 $v,u$ 成立，故

$$
J^\top M_Y=M_XJ^\dagger.
$$

由于 $M_X$ 可逆，

$$
\boxed{J^\dagger=M_X^{-1}J^\top M_Y.}
$$

#### 5. 恒等式核验

直接代回：

$$
\begin{aligned}
\langle v,J^\dagger u\rangle_X
&=v^\top M_XM_X^{-1}J^\top M_Yu\\
&=v^\top J^\top M_Yu\\
&=(Jv)^\top M_Yu\\
&=\langle Jv,u\rangle_Y.
\end{aligned}
$$

#### 6. 四个对象

| 对象 | 需要内积 | 方向 | 主要作用 |
|---|---:|---|---|
| 对偶映射 $A'$ | 否 | $Y^*\to X^*$ | 协向量回拉 |
| 伴随 $A^*$ | 是 | $Y\to X$ | 用向量表示对偶回拉 |
| 转置 $J^\top$ | 坐标对象 | $\mathbb R^m\to\mathbb R^n$ | 标准欧氏基中表示伴随 |
| 逆 $A^{-1}$ | 不需内积，但需双射 | $Y\to X$ | 把输出向量解回输入向量 |

#### 7. 矩形反例

取

$$
J=\begin{bmatrix}1&2&3\\0&1&0\end{bmatrix}
\in\mathbb R^{2\times3}.
$$

$J^\top$ 存在且为 $3\times2$，但 $J$ 不是方阵，不存在普通两侧逆。因此 $J^\top$ 显然不等于 $J^{-1}$。

### CALC-JV-C03：按列/行构造、成本与矩阵自由作用

#### 1. $n$ 个 JVP

标准输入基满足

$$
J=\begin{bmatrix}Je_1&\cdots&Je_n\end{bmatrix}.
$$

每次 JVP 输出一列 $m$ 维向量，全部 $n$ 列唯一确定 $J$。

#### 2. $m$ 个 VJP

标准输出基满足

$$
J_{i:}=(J^\top e_i)^\top.
$$

每次 VJP 输出一行的转置，全部 $m$ 行唯一确定 $J$。

#### 3. 基本选择

- $m\gg n$：列数较少，forward/JVP 通常合理；
- $n\gg m$：行数较少，reverse/VJP 通常合理；
- $m=1$：一次 VJP；
- $n=1$：一次 JVP。

#### 4. 系统因素

至少包括：primitive 规则效率、编译融合、向量化、稀疏/卷积结构、保存中间量、checkpoint、GPU 利用率、内存带宽、通信、dtype、批大小和编译开销。

#### 5. 黑箱算法

对输入 $v$：

```text
w = jvp(F, x, v)        # w = Jv
z = vjp(F, x, w)        # z = Jᵀw = JᵀJv
```

对输出 $u$：

```text
v = vjp(F, x, u)        # v = Jᵀu
w = jvp(F, x, v)        # w = Jv = JJᵀu
```

这里第二步都使用同一固定基点处的线性作用。

#### 6. 自伴随与半正定

$$
(J^\top J)^\top=J^\top J,
\qquad
v^\top J^\top Jv=\|Jv\|_2^2\ge0.
$$

同理

$$
(JJ^\top)^\top=JJ^\top,
\qquad
u^\top JJ^\top u=\|J^\top u\|_2^2\ge0.
$$

#### 7. 成本边界

代数只说明需要哪些线性作用，不能规定每个 primitive 的实现成本、缓存策略、编译融合或硬件吞吐。因此不能从“两次黑箱调用”推出固定的两倍前向运行时间。

## D 级：错误审计与软件语义

### CALC-JV-D01：审计十五条声明

1. **错误。** 偏导表是候选坐标表示；先用 Fréchet 余项或充分条件证明可微。
2. **错误。** $Jv\in\mathbb R^m$，$v\in\mathbb R^n$；仅 $m=n$ 时数值形状可能相同。
3. **错误。** VJP 回拉协向量，不反解输出向量。验证类型 $Y^*\to X^*$。
4. **错误。** 反向传播应用局部对偶映射/伴随；从不要求每层 Jacobian 可逆。
5. **错误。** 普通转置只对应标准欧氏内积；加权情形用 $M_X^{-1}J^\top M_Y$。
6. **错误。** 向量输出必须先给 cotangent seed，即选择标量测量；不存在唯一“向量函数梯度”。
7. **错误。** 全一 seed 给 $J^\top\mathbf1$。用输出基种子才能逐行形成 full $J$。
8. **错误。** 批梯度通常是样本梯度的和或均值；per-example gradient 还保留 batch 轴。
9. **错误。** 前向复制对应反向沿复制轴求和。用线性层伴随测试验证。
10. **错误。** 选择取决于输入/输出维数、程序和硬件；两者应 profiling。
11. **错误。** Krylov/幂迭代可使用 $Jv,J^\top u$ 估计谱或作用，无需物化 $J$。
12. **错误。** 两个错误规则可能互为伴随；还需解析/有限差分验证真实 JVP。
13. **错误。** 中心差分直接检查 JVP；VJP 还需伴随测试或标量化差分。
14. **错误。** forward-mode 或高阶组合可能需要独立 JVP 规则；正确一次 backward 不保证可组合性。
15. **错误。** 默认数组通常是欧氏/Frobenius 微分坐标；自然梯度还需 Fisher 度量逆作用。

### CALC-JV-D02：batch、mask、归约与 per-example 语义

#### 1. Jacobian 形状与结构

把 $X$ 展平为 $Bd$ 维，

$$
J_\ell\in\mathbb R^{B\times Bd}.
$$

若样本完全独立，第 $b$ 行只依赖第 $b$ 个 $d$ 维输入块，因此是行块对角/局部支撑结构。张量形式可看成 $B\times B\times d$，非对角样本块为零。

#### 2. mean seed

$$
L=\frac1B\mathbf1^\top\ell,
$$

所以

$$
\nabla_XL
=J_\ell^\top\frac{\mathbf1}{B}.
$$

VJP seed 是 $\mathbf1/B$。

#### 3. sum 与 mean

seed $\mathbf1$ 对应样本和，$\mathbf1/B$ 对应样本均值；全部 input cotangent 相差因子 $B$。

#### 4. BatchNorm 耦合

训练态 batch normalization 的每个样本输出依赖整个 batch 的均值/方差。因此 $\partial\ell_b/\partial X_c$ 对 $b\ne c$ 也可能非零，Jacobian 不再按样本块对角。

#### 5. mask 风险

布尔索引可能改变动态输出长度，导致 seed 结构随数据变化；mask 选择本身通常是离散、不可微的。应固定被微分的连续值路径，并记录被选索引是否 stop-gradient。

#### 6. 三类测试

- 样本独立：只扰动样本 $c$，检查其他逐样本损失 JVP 是否为零；
- 归约因子：比较 sum 与 mean VJP 是否精确相差 $B$；
- 广播/批求和：逐样本 seed 做 VJP，再求和，与全一 seed 的单次 VJP 比较。

#### 7. 每样本参数梯度

把单样本损失写成参数显式输入函数 $\ell(\theta;x_b)$，对 $\theta$ 做 `grad/vjp`，再用 `vmap` 沿样本轴批量化。输出树每个参数叶子前增加 batch 轴；这与对 $X$ 求梯度是不同输入槽。

### CALC-JV-D03：API 与测试协议审计

#### 1. 对象形状

若 $f:\mathbb R^n\to\mathbb R^m$：

$$
x,v\in\mathbb R^n,
\quad
y,y2,jv,u\in\mathbb R^m,
\quad
J^\top u\in\mathbb R^n.
$$

`jt_u` 在单输入 API 中常仍包装为一元 tuple，实际数组是 `jt_u[0]`。

#### 2. 稳定残差

严格 `==` 会因浮点舍入失败。使用

$$
\eta_{\rm adj}
=\frac{|u^\top jv-(jt\_u)^\top v|}
{\max(1,|u^\top jv|,|(jt\_u)^\top v|)}
$$

并按 dtype、问题尺度设置容差。

#### 3. tuple 解包

若只有输入 $x$：

```text
(jt_u_x,) = pullback(u)
```

多输入时返回与 primals 对应的 tuple/tree，不能把容器整体传给普通点积。

#### 4. 中心差分

对一列对数步长 $\varepsilon_k$，计算

$$
q_k=\frac{f(x+\varepsilon_kv)-f(x-\varepsilon_kv)}{2\varepsilon_k},
$$

并报告 $\|q_k-jv\|/\max(1,\|jv\|)$，寻找先按 $O(\varepsilon^2)$ 下降、后被舍入抬升的区间。

#### 5. 线性测试

随机 $v_1,v_2,u_1,u_2,\alpha,\beta$，分别检查

$$
J(\alpha v_1+\beta v_2)
\approx\alpha Jv_1+\beta Jv_2
$$

和

$$
J^\top(\alpha u_1+\beta u_2)
\approx\alpha J^\top u_1+\beta J^\top u_2.
$$

#### 6. 控制项

固定随机种子；明确 train/eval；关闭或控制 dropout；检查 detach/stop-gradient；避开或单独测试不可微点；记录 dtype；检查 in-place/state mutation；确保相同基点与参数版本。

#### 7. 为什么两类测试都要

有限差分把 JVP 与原函数真实局部变化联系起来，但不直接检查 VJP；伴随测试把 VJP 与 JVP 联系起来，但两者可能共同错误。二者结合形成“原函数—JVP—VJP”三角闭环。

## E 级：综合推导与 AI 迁移

### CALC-JV-E01：结构化矩阵映射

#### 1. 一组形状契约

可以取

$$
A,C\in\mathbb R^{r\times m},
\qquad
X,H\in\mathbb R^{m\times n},
\qquad
B,D\in\mathbb R^{n\times s}.
$$

于是

$$
AXB,CXD\in\mathbb R^{r\times s},
$$

所以

$$
F:\mathbb R^{m\times n}\to\mathbb R^{r\times s}.
$$

这不是唯一可能的形状选择，但必须保证两项同属输出空间。

#### 2. JVP

$F$ 对 $X$ 线性，因此

$$
F(X+H)-F(X)=AHB+CHD.
$$

所以

$$
\boxed{DF(X)[H]=AHB+CHD.}
$$

#### 3. Frobenius VJP

给 $U\in\mathbb R^{r\times s}$：

$$
\begin{aligned}
\langle U,AHB\rangle_F
&=\langle A^\top UB^\top,H\rangle_F,\\
\langle U,CHD\rangle_F
&=\langle C^\top UD^\top,H\rangle_F.
\end{aligned}
$$

故

$$
\boxed{
DF(X)^*[U]
=A^\top UB^\top+C^\top UD^\top
\in\mathbb R^{m\times n}.}
$$

#### 4. Kronecker Jacobian

按列向量化：

$$
\begin{aligned}
\operatorname{vec}(AHB)
&=(B^\top\otimes A)\operatorname{vec}(H),\\
\operatorname{vec}(CHD)
&=(D^\top\otimes C)\operatorname{vec}(H).
\end{aligned}
$$

所以

$$
\boxed{
J_F=B^\top\otimes A+D^\top\otimes C
\in\mathbb R^{rs\times mn}.}
$$

#### 5. 与转置作用一致

$$
J_F^\top
=B\otimes A^\top+D\otimes C^\top.
$$

利用 `vec` 恒等式，

$$
(B\otimes A^\top)\operatorname{vec}(U)
=\operatorname{vec}(A^\top UB^\top),
$$

以及

$$
(D\otimes C^\top)\operatorname{vec}(U)
=\operatorname{vec}(C^\top UD^\top).
$$

相加正好得到结构化 VJP 的 `vec`。

#### 6. 伴随点积测试

随机取 $H,U$，检查

$$
\boxed{
\langle U,AHB+CHD\rangle_F
=\left\langle
A^\top UB^\top+C^\top UD^\top,H
\right\rangle_F.}
$$

#### 7. 显式与结构化比较

显式 $J$ 需要存储 $rsmn$ 个标量，Kronecker 和还可能变得稠密；结构化作用只保存 $A,B,C,D$ 并执行矩阵乘法。显式矩阵适合小尺寸布局核对、秩/谱理论；大规模训练应优先 JVP/VJP。还需考虑乘法顺序、中间矩阵大小和稀疏结构，不能仅比较元素总数。

### CALC-JV-E02：矩阵自由 Gauss–Newton/NTK 接口

#### 1. 参数空间算子

给 $v\in\mathbb R^n$：

1. 调用 JVP 得 $w=Jv\in\mathbb R^m$；
2. 以 $w$ 为输出 cotangent 调用 VJP，得
   $$
   z=J^\top w=J^\top Jv.
   $$

#### 2. 输出空间算子

给 $u\in\mathbb R^m$：

1. 调用 VJP 得 $v=J^\top u\in\mathbb R^n$；
2. 对该 $v$ 调用 JVP，得
   $$
   w=Jv=JJ^\top u.
   $$

#### 3. 对称半正定

$$
(J^\top J)^\top=J^\top J,
\qquad
v^\top J^\top Jv=\|Jv\|_2^2\ge0.
$$

$$
(JJ^\top)^\top=JJ^\top,
\qquad
u^\top JJ^\top u=\|J^\top u\|_2^2\ge0.
$$

#### 4. 非零特征值

取 SVD

$$
J=U\Sigma V^\top.
$$

则

$$
J^\top J=V\Sigma^\top\Sigma V^\top,
$$

而

$$
JJ^\top=U\Sigma\Sigma^\top U^\top.
$$

二者非零特征值都是 $J$ 非零奇异值的平方，含相同重数；零特征值数可因 $m,n$ 不同而不同。

#### 5. 空间选择

若参数维数 $n$ 极大而输出/样本维数 $m$ 较小，$JJ^\top$ 作用在较小的输出空间，可让 Krylov 向量、线性系统和显式小矩阵更便宜。反之，若 $n\ll m$，参数空间算子可能更合适。JVP/VJP 单次成本和数据结构仍需实测。

#### 6. 测试

**伴随测试**：先验证底层 $Jv,J^\top u$ 满足配对恒等式。

**自伴随测试**：随机 $a,b$，检查

$$
a^\top(J^\top Jb)
\approx
(J^\top Ja)^\top b.
$$

**Rayleigh 测试**：随机 $v,u$，检查

$$
v^\top J^\top Jv\ge-\tau,
\qquad
u^\top JJ^\top u\ge-\tau,
$$

其中 $\tau$ 是浮点容差，并与 $\|Jv\|^2,\|J^\top u\|^2$ 对照。

#### 7. 理论边界

$J^\top J$ 是固定点处输出最小二乘几何产生的 Gauss–Newton 型核心，不等于一般损失的完整 Hessian；$JJ^\top$ 是经验 NTK 型 Gram 算子，但训练中 $J$ 会随参数变化。半正定性不提供非线性训练的全局收敛、步长或泛化保证。

### CALC-JV-E03：设计一份可复核的 AD 接口报告

选择多头注意力之前的共享线性投影：

$$
Q_{btd}=\sum_{k=1}^{d_{\rm in}}X_{btk}W_{kd},
$$

即

$$
Q=XW.
$$

这里

$$
X\in\mathbb R^{B\times T\times d_{\rm in}},
\qquad
W\in\mathbb R^{d_{\rm in}\times d_{\rm out}},
\qquad
Q\in\mathbb R^{B\times T\times d_{\rm out}}.
$$

#### 1. 树结构

primal tree 为 `(X, W)`；tangent tree 为 `(dX, dW)`，叶子形状分别与 primal 相同。输出 cotangent 是

$$
U\in\mathbb R^{B\times T\times d_{\rm out}},
$$

输入 cotangent tree 为 `(barX, barW)`。

#### 2. JVP

把前两个轴合并为 $N=BT$ 只是记号便利。精确增量给

$$
\boxed{\dot Q=\dot XW+X\dot W.}
$$

逐索引为

$$
\dot Q_{btd}
=\sum_k\dot X_{btk}W_{kd}
+\sum_kX_{btk}\dot W_{kd}.
$$

#### 3. VJP 与参数共享

在所有 $b,t,d$ 上使用 Frobenius 配对：

$$
\boxed{
\bar X_{bt:}=U_{bt:}W^\top,}
$$

以及

$$
\boxed{
\bar W=\sum_{b=1}^B\sum_{t=1}^T
X_{bt:}^\top U_{bt:}.}
$$

$W$ 被所有 batch/token 位置共享，所以它的 VJP 必须累加全部位置贡献。

#### 4. 需要哪种接口

- 给定输入/参数扰动传播到全部 query：JVP；
- 标量训练损失回到 $X,W$：VJP；
- 检查小型投影所有坐标敏感度：full Jacobian；
- 估计 $J^\top J$ 作用：JVP 后接 VJP。

通常不应为真实 $B,T,d$ 形成 full Jacobian。

#### 5. 维数与 profiling

若只对 $W$ 求 full Jacobian，输入坐标数为 $d_{\rm in}d_{\rm out}$，输出坐标数为 $BTd_{\rm out}$；仅看维数可能偏向某一模式，但矩阵乘法 primitive、批量化、编译和显存决定真实速度。应分别 benchmark `jvp/vjp/jacfwd/jacrev` 的目标尺寸，并排除首次编译时间或单独报告。

#### 6. batch、mask 与归约

投影自身逐位置独立，但同一 $W$ 造成参数 VJP 跨位置求和。padding mask 若只在后续 attention 使用，不影响投影导数；若投影前乘 mask，JVP/VJP 中需带相同 mask。损失 sum/mean 决定 seed 缩放。

#### 7. 四类测试

1. **解析小例**：取 $B=T=1$，与普通矩阵乘法公式对照；
2. **中心差分**：比较 $\dot Q$ 与
   $$
   \frac{(X+\varepsilon\dot X)(W+\varepsilon\dot W)
   -(X-\varepsilon\dot X)(W-\varepsilon\dot W)}{2\varepsilon};
   $$
3. **线性性**：分别在 $(\dot X,\dot W)$ 和 $U$ 上测试；
4. **伴随点积**：检查
   $$
   \langle U,\dot Q\rangle_F
   =\langle\bar X,\dot X\rangle_F
   +\langle\bar W,\dot W\rangle_F.
   $$

#### 8. 实验契约

记录框架与版本、设备、dtype、随机种子、容差、张量布局、是否 contiguous、编译模式、train/eval、损失归约和 mask。float32 的差分最优步长通常远大于 float64，不能复用同一绝对容差。

#### 9. 不可微与高阶边界

纯投影是光滑双线性映射；若扩展到 attention，还会遇到 mask 的离散选择、softmax 数值稳定、dropout 随机性和 fused kernel 自定义反向。一次 VJP 正确不保证 custom JVP 或高阶变换正确。

#### 10. 结论分层

- **数学证明**：给出双线性增量和伴随公式；
- **实现证据**：四类测试在记录的配置下通过；
- **性能证据**：目标设备上的同步 benchmark；
- **AI 效果猜想**：某种 Jacobian 正则或矩阵自由算法是否改善训练，需独立实验，不能由接口正确性推出。

#### 11. 最短排查顺序

1. 核对 $B,T,d_{\rm in},d_{\rm out}$ 与 matmul 轴；
2. 核对函数签名中被求导输入槽；
3. 检查 loss sum/mean 与 seed；
4. 检查 $\bar W$ 是否沿 $B,T$ 累加；
5. 做解析小例；
6. 做伴随点积；
7. 扫描差分步长；
8. 固定随机性与模式；
9. 检查自定义/fused primitive；
10. 若数学正确但性能差，再 profiler 定位编译、内存或 kernel 问题。

## 总结性核对

完成本组后，应能闭卷重建：

$$
\boxed{
DF(x):X\to Y
\quad\Longleftrightarrow\quad
\begin{cases}
J &: \text{选基后的完整坐标表},\\
v\mapsto Jv &: \text{切向量前推/JVP},\\
u^*\mapsto u^*\circ DF(x) &: \text{协向量回拉/VJP}.
\end{cases}}
$$

标准欧氏坐标把最后一行显示成 $u\mapsto J^\top u$；这个显示不应掩盖 VJP 的对偶类型，也不应被误读为逆映射。
