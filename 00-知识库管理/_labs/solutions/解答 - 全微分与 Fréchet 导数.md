---
type: solution
status: draft
area: [labs, math/calculus, math/functional-analysis, math/matrix-calculus, ai/automatic-differentiation]
prerequisites: ["[[习题 - 全微分与 Fréchet 导数]]"]
related: ["[[全微分与 Fréchet 导数]]", "[[梯度、方向导数与最陡方向]]", "[[Jacobian、JVP 与 VJP]]", "[[矩阵函数的 Fréchet 导数]]", "[[误差传播、条件估计与停止准则]]", "[[练习与测验 MOC]]"]
sources: ["OpenStax-Calculus-Volume-3-4.4", "MIT-18.02-Tangent-Approximation", "MIT-18.S096-Derivatives-Linear-Operators", "MIT-18.S096-General-Vector-Spaces", "TTU-Gateaux-Frechet-2025", "JAX-JVP-Official", "Su-2383-Determinant-Derivative", "Su-10366-Pseudoinverse"]
created: 2026-08-17
updated: 2026-08-17
---

# 解答 - 全微分与 Fréchet 导数

> [!abstract] 使用说明
> 本解答反复使用同一套四步法：先定类型，再作精确增量；抽取对扰动线性的项；最后证明剩余项除以输入扰动范数趋零。请不要只核对最终公式，尤其要检查自己的量词、矩阵形状、范数和程序语义是否完整。

## A 级：对象、量词与概念层级

### CALC-FR-A01：翻译十二个声明

#### 1. 映射

$$
F:X\to Y
$$

表示 $F$ 把输入赋范空间 $X$ 中的点映到输出赋范空间 $Y$。函数对象包括定义域、陪域和映射规则。

#### 2. 导数算子

$$
DF(a)\in\mathcal L(X,Y)
$$

表示 $F$ 在基点 $a$ 的导数是从 $X$ 到 $Y$ 的有界线性算子。它接收输入扰动，不是 $Y$ 中的一个输出值。

#### 3. 精确增量分解

$$
F(a+h)=F(a)+DF(a)[h]+r(h)
$$

表示真实输出由基点值、一阶线性响应和剩余误差组成；三项都属于 $Y$。

#### 4. 小 $o$ 余项

$$
r(h)=o(\|h\|_X)
$$

表示

$$
\lim_{\|h\|_X\to0}
\frac{\|r(h)\|_Y}{\|h\|_X}=0.
$$

完整量词是：任意 $\varepsilon>0$，存在 $\delta>0$，使所有满足 $0<\|h\|<\delta$ 的扰动都有

$$
\|r(h)\|_Y\le\varepsilon\|h\|_X.
$$

#### 5. 微分

$$
dF_a[h]=DF(a)[h]
$$

是导数算子对指定扰动 $h$ 的作用，属于 $Y$。

#### 6. 真实有限增量

$$
\Delta F=F(a+h)-F(a)
$$

一般不是 $h$ 的线性函数，并且

$$
\Delta F=dF_a[h]+r(h).
$$

#### 7. 方向导数

$$
D_vF(a)=DF(a)[v]
$$

需要 $F$ 在 $a$ Fréchet 可微，或至少已有足以保证该公式的统一可微性。仅有偏导或方向导数存在不能预先写右端。

#### 8. 算子范数

$$
\|DF(a)\|_{\mathrm{op}}
=\sup_{\|v\|_X=1}\|DF(a)[v]\|_Y
$$

是所选输入输出范数下，单位输入扰动的一阶最大输出幅度。

#### 9. 标量微分

$$
Df(a)\in X^*
$$

表示 $f:X\to\mathbb R$ 的导数是 $X$ 上的连续线性泛函。

#### 10. 梯度表示

$$
Df(a)[h]=\langle\nabla f(a),h\rangle
$$

需要 $X$ 是带指定内积的 Hilbert 空间，或有限维内积空间。梯度是同一线性泛函在该内积下的 Riesz 表示。

#### 11. Jacobian 表示

$$
DF(a)[h]=J_F(a)h
$$

需要有限维空间和选定的输入输出基。$J_F(a)$ 是导数算子的坐标矩阵，不是额外的导数对象。

#### 12. 矩阵乘法导数

$$
DM(A,B)[E,F]=EB+AF.
$$

若

$$
A,E\in\mathbb R^{m\times n},
\qquad
B,F\in\mathbb R^{n\times p},
$$

则两个一阶项及输出都属于 $\mathbb R^{m\times p}$。导数的输入是扰动对 $(E,F)$。

### CALC-FR-A02：判断十六个断言

1. **错。** $DF(a)$ 是 $X\to Y$ 的有界线性算子；$DF(a)[h]$ 才是 $Y$ 中向量。
2. **错。** $x\mapsto F(a)+DF(a)[x-a]$ 通常是仿射映射；只有常数项恰为零时才线性。
3. **错。** 必须有 $\|r(h)\|/\|h\|\to0$。例如 $r(h)=|h|$ 趋零但不是 $o(|h|)$。
4. **对。** 两候选之差沿 $h=tv$ 的归一化余项趋零，从而在每个 $v$ 上为零。
5. **对。** 有界线性项和小 $o$ 余项都随 $h\to0$ 消失。
6. **错。** $f(x)=|x|$ 在零点连续但不可微。
7. **对。** 把 $h=tv$ 代入统一余项即可。
8. **错。** 本章的 $k(x,y)$ 在原点连续，方向映射恒为零且线性，却不 Fréchet 可微。
9. **对。** Fréchet 的整个小球统一余项推出每条固定直线上的 Gâteaux 极限。
10. **错。** 有限维等价范数不会改变 Fréchet 可微性。
11. **错。** 诱导算子范数依赖输入输出范数；只有有限维拓扑性质保持。
12. **错。** 无限维中存在不连续线性映射，所以要显式要求有界。
13. **错。** 微分属于对偶空间；梯度还依赖内积。
14. **错。** 一阶微分是
    $$
    d(AB)=dA\,B+A\,dB.
    $$
    $dA\,dB$ 属于精确增量的二阶项。
15. **对。** $DF(a)[v]$ 属于输出切向量空间，与 $F(a)$ 的输出结构相容。
16. **错。** 框架可能在不可微点选择约定导数，或使用 stop-gradient、自定义 VJP。

### CALC-FR-A03：为十二个任务选择工具

| 任务 | 工具 | 原因 |
|---|---|---|
| 1 | Fréchet 归一化余项 | 直接对应全方向统一定义 |
| 2 | 固定方向切片 | $D_vF(a)=DF(a)[v]$ |
| 3 | 方向映射线性检查 | 非线性立即否定统一线性导数 |
| 4 | Hadamard 变化方向序列 | 让坏方向随尺度移动并收敛 |
| 5 | 算子范数 | 定义即单位扰动最大一阶响应 |
| 6 | 精确扰动展开 | 按扰动次数抽取一阶项 |
| 7 | 双线性有界性 | 控制 $\|B(h,k)\|\le C\|h\|\|k\|$ |
| 8 | 等价范数 | 有限维范数只改变常数 |
| 9 | 对偶空间 | 标量微分是连续线性泛函 |
| 10 | Jacobian 坐标表示 | 线性算子选基后成为矩阵 |
| 11 | JVP | 直接计算 $DF(a)[v]$ |
| 12 | 伴随点积测试 | 验证 $\langle Av,w\rangle=\langle v,A^*w\rangle$ |

## B 级：定义计算、形状与一阶展开

### CALC-FR-B01：六个基本映射

#### 1. 常值

若 $F(x)=c$，

$$
F(x+h)-F(x)=0.
$$

因此

$$
DF(x)[h]=0,
$$

余项为零。

#### 2. 有界线性映射

若 $F(x)=Lx$，

$$
F(x+h)-F(x)=Lh.
$$

故

$$
DF(x)=L.
$$

有界性保证它确实属于 $\mathcal L(X,Y)$。

#### 3. 仿射映射

若 $F(x)=Lx+b$，

$$
F(x+h)-F(x)
=L(x+h)+b-(Lx+b)
=Lh.
$$

所以 $DF(x)=L$。

#### 4. 平方范数

$$
\|x+h\|_2^2-\|x\|_2^2
=2x^\top h+\|h\|_2^2.
$$

候选导数为

$$
Df(x)[h]=2x^\top h.
$$

余项验证：

$$
\frac{\|h\|_2^2}{\|h\|_2}
=\|h\|_2\to0.
$$

#### 5. 一般二次型

$$
q(x+h)-q(x)
=(x+h)^\top A(x+h)-x^\top Ax
$$

$$
=h^\top Ax+x^\top Ah+h^\top Ah.
$$

前两项是

$$
x^\top(A+A^\top)h.
$$

故

$$
Dq(x)[h]=x^\top(A+A^\top)h.
$$

使用谱范数，

$$
\frac{|h^\top Ah|}{\|h\|_2}
\le
\|A\|_2\|h\|_2\to0.
$$

#### 6. 二维到二维映射

$$
F(x,y)=
\begin{bmatrix}
x^2+xy\\
e^y-x
\end{bmatrix}.
$$

在 $a=(1,0)$，输入扰动写成 $(h,k)$。

第一分量：

$$
(1+h)^2+(1+h)k-1
=2h+k+h^2+hk.
$$

第二分量：

$$
e^k-(1+h)-(1-1)
=k-h+o(\sqrt{h^2+k^2}).
$$

所以

$$
DF(1,0)[h,k]
=
\begin{bmatrix}
2h+k\\
-h+k
\end{bmatrix}.
$$

Jacobian 为

$$
J_F(1,0)
=
\begin{bmatrix}
2&1\\
-1&1
\end{bmatrix}.
$$

又

$$
F(1,0)=
\begin{bmatrix}
1\\0
\end{bmatrix},
$$

故局部仿射近似为

$$
L(x,y)
=
\begin{bmatrix}
1\\0
\end{bmatrix}
+
\begin{bmatrix}
2&1\\
-1&1
\end{bmatrix}
\begin{bmatrix}
x-1\\y
\end{bmatrix}.
$$

### CALC-FR-B02：双线性、内积与矩阵乘法

#### 1. 双线性映射

由双线性，

$$
B(x+h,y+k)
=B(x,y)+B(h,y)+B(x,k)+B(h,k).
$$

因此候选导数

$$
DB(x,y)[h,k]
=B(h,y)+B(x,k)
$$

对 $(h,k)$ 整体线性。

若使用最大乘积范数

$$
\|(h,k)\|_\times=\max\{\|h\|,\|k\|\},
$$

且

$$
\|B(h,k)\|\le C\|h\|\|k\|,
$$

则

$$
\frac{\|B(h,k)\|}{\|(h,k)\|_\times}
\le
C\|(h,k)\|_\times\to0.
$$

故候选确为 Fréchet 导数。

#### 2. 内积

$$
d(x^\top y)[h,k]
=h^\top y+x^\top k.
$$

余项为 $h^\top k$。

#### 3. 矩阵乘法

$$
DM(A,B)[E,F]=EB+AF.
$$

两个偏导槽为

$$
D_AM(A,B)[E]=EB,
$$

$$
D_BM(A,B)[F]=AF.
$$

#### 4. 形状

给定

$$
A,E\in\mathbb R^{3\times4},
\qquad
B,F\in\mathbb R^{4\times2},
$$

有

$$
EB,AF,EF\in\mathbb R^{3\times2}.
$$

#### 5. 为什么 $EF$ 是余项

$EF$ 对扰动对不是线性的。例如同时把 $(E,F)$ 放大 $\alpha$，有

$$
(\alpha E)(\alpha F)=\alpha^2EF,
$$

而线性映射应只放大 $\alpha$。

但严格证明必须保留它，因为

$$
(A+E)(B+F)-AB-(EB+AF)=EF.
$$

只有写出它，才能证明归一化剩余趋零。

### CALC-FR-B03：算子范数与局部条件性

#### 1. 对角线性映射

坐标矩阵为

$$
L=
\begin{bmatrix}
3&0\\0&1
\end{bmatrix}.
$$

欧氏诱导范数等于最大奇异值：

$$
\|L\|_2=3.
$$

$\infty$ 诱导范数等于最大绝对行和：

$$
\|L\|_\infty=3.
$$

本例两者数值相同只是矩阵特殊，不代表一般不依赖范数。

#### 2. 指数与加法映射

$$
F(x_1,x_2)=
\begin{bmatrix}
e^{x_1}\\x_1+x_2
\end{bmatrix}.
$$

在原点，

$$
DF(0,0)[h_1,h_2]
=
\begin{bmatrix}
h_1\\h_1+h_2
\end{bmatrix},
$$

矩阵为

$$
J=
\begin{bmatrix}
1&0\\1&1
\end{bmatrix}.
$$

计算

$$
J^\top J
=
\begin{bmatrix}
2&1\\1&1
\end{bmatrix}.
$$

其最大特征值为

$$
\lambda_{\max}
=\frac{3+\sqrt5}{2}.
$$

所以

$$
\|DF(0,0)\|_2
=
\sqrt{\frac{3+\sqrt5}{2}}
=\frac{1+\sqrt5}{2}.
$$

#### 3. 局部上界

任意 $\varepsilon>0$，当 $h$ 足够小时，

$$
\|F(h)-F(0)\|_2
\le
\left(
\frac{1+\sqrt5}{2}+\varepsilon
\right)\|h\|_2.
$$

#### 4. 相对尺度失败

输出基点

$$
F(0,0)=(1,0)
$$

非零，所以以输出范数作分母没有问题。但输入基点 $a=0$，表达式

$$
\frac{\|h\|}{\|a\|}
$$

无定义，因此标准输入相对扰动模型不适用。

#### 5. 更合适报告

报告绝对条件数

$$
\kappa_{\rm abs}
=\frac{1+\sqrt5}{2},
$$

并给出带实际输入单位的绝对扰动预算。若各分量有自然尺度，可引入参考尺度向量或分量型条件数，而不是除以零。

## C 级：证明、反例与理论重建

### CALC-FR-C01：三条基本定理

#### 1. 唯一性

设 $A,B$ 都是候选 Fréchet 导数。则

$$
F(a+h)-F(a)-A[h]=r_A(h),
$$

$$
F(a+h)-F(a)-B[h]=r_B(h),
$$

且两余项除以 $\|h\|$ 都趋零。

固定 $v\ne0$，取 $h=tv$，相减：

$$
t(A-B)[v]=r_B(tv)-r_A(tv).
$$

所以

$$
\|(A-B)[v]\|
\le
\|v\|
\left(
\frac{\|r_A(tv)\|}{\|tv\|}
+
\frac{\|r_B(tv)\|}{\|tv\|}
\right)\to0.
$$

故 $(A-B)[v]=0$。$v=0$ 时由线性同样成立，于是 $A=B$。

这里用到：

- 线性：$A[tv]=tA[v]$；
- 统一余项：沿任意 $tv$ 都可使用；
- 不需要用到有界性。

#### 2. 可微推出连续

$$
F(a+h)-F(a)=DF(a)[h]+r(h).
$$

有界性给出

$$
\|DF(a)[h]\|
\le
\|DF(a)\|_{\rm op}\|h\|.
$$

因此

$$
\|F(a+h)-F(a)\|
\le
\|DF(a)\|_{\rm op}\|h\|+\|r(h)\|\to0.
$$

这里有界性负责线性项连续，统一小 $o$ 负责余项。

#### 3. 推出方向导数

固定 $v$：

$$
\frac{F(a+tv)-F(a)}t
=DF(a)[v]+\frac{r(tv)}t.
$$

且

$$
\left\|\frac{r(tv)}t\right\|
=
\|v\|
\frac{\|r(tv)\|}{\|tv\|}\to0.
$$

所以

$$
D_vF(a)=DF(a)[v].
$$

这里线性用于提出 $t$，统一余项保证任意固定 $v$ 的路径可用。

#### 4. 假设使用位置

| 结论 | 线性 | 有界 | 统一余项 |
|---|---|---|---|
| 唯一性 | 抽出 $t$ | 非必要 | 必要 |
| 连续性 | 识别一阶项 | 必要，尤其无限维 | 必要 |
| 方向公式 | 抽出 $t$ | 不是该极限的核心 | 必要 |

#### 5. 为什么不能反向

固定直线的极限结构是

$$
\forall v\ \exists\delta_v\ \forall |t|<\delta_v.
$$

Fréchet 结构要求

$$
\exists\delta\ \forall h,\ \|h\|<\delta.
$$

$\delta_v$ 可能随方向恶化，甚至坏方向随尺度移动，所以逐方向结论不能交换量词成为统一结论。

### CALC-FR-C02：四层可微性与连续反例

#### 1. $h$ 连续

$$
|h(x,y)|
=\frac{|x|^3}{x^2+y^2}
\le|x|
\le\sqrt{x^2+y^2}\to0.
$$

沿 $v=(a,b)$，

$$
\frac{h(ta,tb)-h(0,0)}t
=
\frac{a^3}{a^2+b^2}
$$

对 $(a,b)\ne0$。零方向导数自然为零。

#### 2. 方向映射非线性

$$
D_{(1,0)}h=1,\qquad
D_{(0,1)}h=0,
$$

但

$$
D_{(1,1)}h=\frac12.
$$

若线性，应有 $D_{(1,1)}h=1$，矛盾。

#### 3. $k$ 连续

由 $2|x^6y|\le x^{12}+y^2$，

$$
|k(x,y)|
\le\frac12\sqrt{x^2+y^2}\to0.
$$

#### 4. 全部方向导数为零

若 $v=(a,b)$ 且 $b\ne0$，

$$
\frac{k(ta,tb)}t
=
\frac{|t|}{t}\sqrt{a^2+b^2}
\frac{t^7a^6b}{t^{12}a^{12}+t^2b^2}.
$$

约去 $t^2$ 后，后因子数量级为 $t^5$，故趋零。若 $b=0$，分子含 $y=0$，恒为零。

因此方向映射为零算子。

#### 5. Fréchet 失败

若 Fréchet 导数存在，根据方向导数公式只能是 $A=0$。沿 $y=x^6$，

$$
\frac{x^6y}{x^{12}+y^2}
=\frac12.
$$

于是

$$
\frac{|k(x,x^6)|}{\sqrt{x^2+x^{12}}}
=\frac12,
$$

不趋零。

#### 6. Hadamard 失败

取

$$
t_j\downarrow0,
\qquad
v_j=(1,t_j^5)\to(1,0).
$$

则

$$
t_jv_j=(t_j,t_j^6).
$$

所以

$$
\frac{k(t_jv_j)}{t_j}
=\frac12\sqrt{1+t_j^{10}}
\to\frac12.
$$

而零算子作用在 $(1,0)$ 上为零，故 Hadamard 条件失败。

#### 7. 蕴含图

$$
\text{Fréchet}
\Longrightarrow
\text{Hadamard}
\Longrightarrow
\text{Gâteaux}
\Longrightarrow
\text{全部方向导数存在且方向映射线性}
\Longrightarrow
\text{偏导存在}.
$$

$h$ 说明“连续且全部方向导数存在”不推出方向映射线性；$k$ 说明“连续且方向映射线性”仍不推出 Hadamard 或 Fréchet。

### CALC-FR-C03：范数等价与双线性余项定理

#### 1. 可微性不依赖有限维范数

设 $F$ 在输入 $\alpha$ 范数、输出 $\alpha$ 范数下满足

$$
\frac{\|r(h)\|_{\alpha,Y}}{\|h\|_{\alpha,X}}\to0.
$$

由范数等价，存在常数 $C_Y,c_X>0$ 使

$$
\|r(h)\|_{\beta,Y}
\le C_Y\|r(h)\|_{\alpha,Y},
$$

$$
\|h\|_{\beta,X}
\ge c_X\|h\|_{\alpha,X}.
$$

故

$$
\frac{\|r(h)\|_{\beta,Y}}{\|h\|_{\beta,X}}
\le
\frac{C_Y}{c_X}
\frac{\|r(h)\|_{\alpha,Y}}{\|h\|_{\alpha,X}}
\to0.
$$

反向同理。

#### 2. 导数映射不变

候选 $A$ 是同一个代数线性映射。范数只改变连续性常数和极限度量；有限维中所有线性映射在两套范数下都连续。唯一性又保证不会产生另一个导数。

#### 3. 算子范数会变

$$
\|A\|_{\alpha\to\alpha}
=
\sup_{h\ne0}
\frac{\|Ah\|_\alpha}{\|h\|_\alpha}
$$

和

$$
\|A\|_{\beta\to\beta}
$$

优化的是不同单位球，数值与最坏方向可不同。

#### 4. 乘积范数

$$
\max\{\|h\|,\|k\|\}
\le
\|h\|+\|k\|
\le
2\max\{\|h\|,\|k\|\}.
$$

所以最大范数与和范数等价。

#### 5. 双线性余项

使用和范数，

$$
\frac{\|B(h,k)\|}{\|h\|+\|k\|}
\le
C\frac{\|h\|\|k\|}{\|h\|+\|k\|}.
$$

又

$$
\frac{ab}{a+b}\le\min\{a,b\}\le a+b
$$

对 $a,b\ge0$，故比例趋零。使用最大范数的证明已见 B02。

## D 级：失败边界与声明审计

### CALC-FR-D01：审计十二个错误推导

1. **错误：** 偏导只控制坐标轴。**修正：** 若能证明连续偏导充分条件或直接验证统一余项，才可把全微分写成偏导的坐标和。
2. **错误：** 全部固定方向仍缺统一性。**修正：** 检查方向映射线性和归一化余项在方向上的一致收敛。
3. **错误：** 线性只解决一项要求。**修正：** 再证明 $\|r(h)\|/\|h\|\to0$；反例 $k$ 否定原命题。
4. **错误：** 普通趋零弱于小 $o$。**修正：** 必须除以 $\|h\|$ 后仍趋零。
5. **错误：** 切平面方程含基点常数。**修正：** 导数是线性；切平面对应局部仿射模型。
6. **错误：** 梯度需要内积，矩阵需要布局。**修正：** 先写 $Df(a)[h]$，再声明内积和坐标表示。
7. **错误：** 导数的类型是输入扰动空间到输出扰动空间的线性算子。**修正：** 只有梯度在选定内积下常与输入同形。
8. **错误：** 精确等式中不能删项。**修正：** 先保留 $dA\,dB$，再证明它是二阶余项。
9. **错误：** 一次 JVP 只检查一个投影。**修正：** 做线性、伴随、多方向多尺度和坏方向搜索。
10. **错误：** 框架可采用不可微点约定。**修正：** 单独审计经典导数、程序规则和差分证据。
11. **错误：** 条件数是局部一阶量。**修正：** 大扰动要控制邻域导数、余项或全局常数。
12. **错误：** 等价只保证拓扑和阶数。**修正：** 条件数数值取决于范数。

### CALC-FR-D02：微分、梯度、Jacobian 与坐标

#### 1. $(x,y)$ 坐标微分

$$
df
=2x\,dx+8y\,dy.
$$

这是一个线性泛函。

#### 2. $(u,v)$ 坐标

由

$$
x=\frac{u+v}{2},
\qquad
y=\frac{u-v}{2},
$$

得到

$$
f(u,v)
=\frac{(u+v)^2}{4}+(u-v)^2.
$$

所以

$$
\frac{\partial f}{\partial u}
=\frac{u+v}{2}+2(u-v)
=\frac52u-\frac32v,
$$

$$
\frac{\partial f}{\partial v}
=\frac{u+v}{2}-2(u-v)
=-\frac32u+\frac52v.
$$

于是

$$
df
=
\left(\frac52u-\frac32v\right)du
+
\left(-\frac32u+\frac52v\right)dv.
$$

#### 3. 同一实际扰动

坐标扰动满足

$$
du=dx+dy,\qquad dv=dx-dy.
$$

把它们代入 $(u,v)$ 微分并使用 $u=x+y,v=x-y$，化简后正好得到

$$
2x\,dx+8y\,dy.
$$

标量作用值一致。

#### 4. 梯度数组

若各自把坐标空间配上标准欧氏内积，偏导数组分别为

$$
\nabla_{x,y}f=
\begin{bmatrix}
2x\\8y
\end{bmatrix},
$$

$$
\nabla_{u,v}^{\rm coord}f=
\begin{bmatrix}
\frac52u-\frac32v\\
-\frac32u+\frac52v
\end{bmatrix}.
$$

这里有一个重要细节：$(u,v)$ 变换不是保持原标准欧氏度量的正交变换。若坚持表示同一个原物理欧氏内积，则 $(u,v)$ 坐标中的度量矩阵为

$$
G_{uv}
=
\left(\frac{\partial(x,y)}{\partial(u,v)}\right)^\top
\left(\frac{\partial(x,y)}{\partial(u,v)}\right)
=\frac12I,
$$

相应 Riesz 梯度应为偏导数组的两倍。

#### 5. 为什么不矛盾

微分是坐标无关线性泛函；偏导数组是协向量分量；梯度数组还取决于度量。坐标或内积改变时，数组按相应规则改变，但对同一实际扰动的标量作用保持一致。

#### 6. 加权内积下的梯度

设

$$
G=
\begin{bmatrix}
1&0\\0&9
\end{bmatrix}.
$$

要求

$$
df[h]
=
\nabla_G f^\top Gh.
$$

而标准微分分量为 $(2x,8y)^\top$，所以

$$
G\nabla_Gf
=
\begin{bmatrix}
2x\\8y
\end{bmatrix}.
$$

因此

$$
\nabla_Gf
=
\begin{bmatrix}
2x\\8y/9
\end{bmatrix}.
$$

#### 7. 依赖总结

| 对象 | 坐标改变 | 内积改变 |
|---|---|---|
| 抽象微分 $Df$ | 本体不变，分量变换 | 不变 |
| Jacobian/偏导数组 | 改变 | 不直接依赖内积 |
| 梯度向量 | 分量改变 | 向量本身也改变 |

### CALC-FR-D03：AI 与程序语义审计

#### 1. ReLU 零点

经典双侧 Fréchet 导数不存在，因为左右斜率不同。框架通常选择 $0$ 或其他约定次梯度。应分别记录“经典不可微”和“框架规则为零”；有限差分可能跨过分支。

#### 2. stop-gradient

前向数学复合若按普通函数理解为 $y=3x^2$，经典导数是 $6x$。程序 stop-gradient 明确把 $dz/dx$ 设为零，所以反向给零。验证应针对程序定义的自定义导数契约，不得声称它等于原前向数学函数的经典导数。

#### 3. 标量广播

映射

$$
s\mapsto s\mathbf1_B
$$

是线性的，JVP 为 $ds\,\mathbf1_B$；伴随 VJP 把长度 $B$ 的余切量求和回标量。需要测试复制与归约轴。

#### 4. Top-k 索引改变

排序间隔非零且索引不变的局部区域内，可把选择当固定线性投影；在并列或交换边界处通常不连续或不可微。框架多冻结索引路径。应测试 ties 和近 ties，不能由一个稳定样本推出全局可微。

#### 5. matmul 漏槽

总导数应为

$$
dA\,B+A\,dB.
$$

漏掉后项会使仅扰动 $B$ 的 JVP 为零，立即用槽位测试可发现。

#### 6. 单方向有限差分

只能支持该方向投影。应扩展多方向、多尺度、线性性、伴随和最坏方向搜索；不能证明完整 Jacobian。

#### 7. $\theta=e^\phi$

两个坐标中的微分由链式法则连接：

$$
\frac{dL}{d\phi}
=
\frac{dL}{d\theta}e^\phi.
$$

梯度大小变化包含坐标尺度，不可直接解释为“参数更重要”。

#### 8. 单纯形边界

任意欧氏双侧扰动可能离开定义域。应只测试可行锥、内部重参数化或单纯形切空间方向。环境空间 Fréchet 导数与约束导数不是同一声明。

## E 级：AI 迁移、综合推导与验证设计

### CALC-FR-E01：线性层的多参数导数

#### 1. 精确展开

记

$$
\Phi(W,x,b)=Wx+b.
$$

则

$$
\Phi(W+E,x+h,b+c)-\Phi(W,x,b)
$$

$$
=(W+E)(x+h)+b+c-(Wx+b)
$$

$$
=Ex+Wh+c+Eh.
$$

#### 2. 总导数

$$
D\Phi(W,x,b)[E,h,c]
=Ex+Wh+c.
$$

它对扰动三元组整体线性，输出在 $\mathbb R^m$。

#### 3. 小 $o$ 余项

余项为 $Eh$。采用

$$
\|(E,h,c)\|_\times
=\max\{\|E\|_2,\|h\|_2,\|c\|_2\},
$$

有

$$
\frac{\|Eh\|_2}{\|(E,h,c)\|_\times}
\le
\frac{\|E\|_2\|h\|_2}{\|(E,h,c)\|_\times}
\le
\|(E,h,c)\|_\times\to0.
$$

#### 4. 三个偏导算子

$$
D_W\Phi[E]=Ex,
$$

$$
D_x\Phi[h]=Wh,
$$

$$
D_b\Phi[c]=c.
$$

#### 5. 标量损失的微分

令

$$
r=Wx+b-y.
$$

损失

$$
\ell=\frac12r^\top r.
$$

平方范数微分先给出

$$
D\ell[E,h,c]
=r^\top D\Phi[E,h,c]
$$

$$
=r^\top(Ex+Wh+c).
$$

这一步已经给出完整导数线性泛函。

#### 6. 读出梯度

用 Frobenius 内积

$$
\langle U,V\rangle_F=\operatorname{tr}(U^\top V),
$$

有

$$
r^\top Ex
=\operatorname{tr}(x r^\top E)
=\langle rx^\top,E\rangle_F.
$$

另外

$$
r^\top Wh
=(W^\top r)^\top h,
$$

$$
r^\top c=r^\top c.
$$

故

$$
\nabla_W\ell=rx^\top,
$$

$$
\nabla_x\ell=W^\top r,
$$

$$
\nabla_b\ell=r.
$$

#### 7. 两类测试

JVP 测试：随机生成 $(E,h,c)$，比较

$$
\frac{\|\Phi(W+tE,x+th,b+tc)-\Phi(W,x,b)-tD\Phi[E,h,c]\|}
{|t|}
$$

随 $t$ 缩小的行为。本例余项是 $t^2Eh$，归一化后应为 $O(t)$。

伴随点积测试：对随机输出余切量 $u$，

$$
u^\top(Ex+Wh+c)
$$

应等于

$$
\langle ux^\top,E\rangle_F
+
(W^\top u)^\top h
+
u^\top c.
$$

#### 8. 批处理与广播

若

$$
\Phi(W,X,b)=WX+b\mathbf1^\top,
$$

则

$$
d\Phi=dW\,X+W\,dX+db\,\mathbf1^\top.
$$

前向 JVP 中 $db$ 被复制到每个样本；反向 VJP 中偏置余切量沿批次列求和。权重梯度累积为输出余切矩阵乘 $X^\top$。

### CALC-FR-E02：矩阵乘法、注意力与误差预算

#### 1. 总导数

$$
S(Q,K)=\frac{QK^\top}{\sqrt d}.
$$

所以

$$
DS(Q,K)[E,F]
=
\frac{EK^\top+QF^\top}{\sqrt d}.
$$

输出、JVP 与分数矩阵都在 $\mathbb R^{T\times T}$。

#### 2. 二阶余项

精确展开给出

$$
S(Q+E,K+F)-S(Q,K)
$$

$$
=
\frac{EK^\top+QF^\top+EF^\top}{\sqrt d}.
$$

余项为

$$
\frac{EF^\top}{\sqrt d}.
$$

#### 3. 谱范数上界

$$
\|DS[E,F]\|_2
\le
\frac{
\|E\|_2\|K\|_2
+
\|Q\|_2\|F\|_2
}{\sqrt d}.
$$

#### 4. Frobenius 上界

使用

$$
\|AB\|_F\le\|A\|_F\|B\|_2,
$$

得到

$$
\|DS[E,F]\|_F
\le
\frac{
\|E\|_F\|K\|_2
+
\|Q\|_2\|F\|_F
}{\sqrt d}.
$$

更松但只用 Frobenius 范数的界为

$$
\|DS[E,F]\|_F
\le
\frac{
\|E\|_F\|K\|_F
+
\|Q\|_F\|F\|_F
}{\sqrt d}.
$$

#### 5. 两个偏导槽

$$
D_QS[E]=\frac{EK^\top}{\sqrt d},
$$

$$
D_KS[F]=\frac{QF^\top}{\sqrt d}.
$$

前者受 $K$ 尺度控制，后者受 $Q$ 尺度控制；二者定义域虽然同形，但算子不同。

#### 6. JVP

程序只需计算两次矩阵乘法并相加：

$$
(E,K)\mapsto EK^\top,
\qquad
(Q,F)\mapsto QF^\top.
$$

无需构造把两个 $T\times d$ 输入向量化后映到 $T^2$ 输出的巨大 Jacobian。

#### 7. 伴随作用

给 $G\in\mathbb R^{T\times T}$，有

$$
\langle G,EK^\top\rangle_F
=\langle GK,E\rangle_F,
$$

$$
\langle G,QF^\top\rangle_F
=\langle G^\top Q,F\rangle_F.
$$

因此

$$
DS(Q,K)^*[G]
=
\left(
\frac{GK}{\sqrt d},
\frac{G^\top Q}{\sqrt d}
\right).
$$

#### 8. 结论边界

- $1/\sqrt d$ 控制理想实数模型的一阶尺度，不自动控制浮点点积误差；
- $T$ 增大改变矩阵范数、归约长度和 softmax 分布；
- softmax 的导数与饱和性属于后续复合层；
- 低精度误差含舍入、累积和执行顺序；
- 大扰动需保留 $EF^\top$ 及后续非线性余项；
- 因此不能从当前节点的局部导数直接推出完整注意力模块全局稳定。

### CALC-FR-E03：统一导数验证协议

#### 阶段 0：固定实验契约

记录：

- 输入输出 pytree/数组形状；
- dtype 与内部累积精度；
- CPU/GPU 与确定性设置；
- batch 维和广播轴；
- 随机种子、dropout、BatchNorm 状态；
- 约束集合与允许方向；
- 是否存在 stop-gradient 或自定义导数。

没有这些信息，不同运行可能不是同一个数学程序。

#### 阶段 1：线性性

随机取 $u,v$ 和标量 $\alpha,\beta$，检查

$$
A[\alpha u+\beta v]
\approx
\alpha A[u]+\beta A[v].
$$

应按 dtype 设计绝对加相对容差，并测试极端尺度。失败说明候选甚至不是线性算子。

#### 阶段 2：伴随一致性

随机取输入切向量 $v$ 和输出余切量 $w$，计算

$$
\eta
=
\frac{
|\langle A[v],w\rangle-\langle v,A^*[w]\rangle|
}{
1+|\langle A[v],w\rangle|+|\langle v,A^*[w]\rangle|
}.
$$

跨多个随机样本、dtype 和 batch 形状测试。这证明前后向实现彼此一致，不证明它们等于真实导数。

#### 阶段 3：Taylor 余项

对单位方向 $v_i$ 和尺度

$$
t\in\{10^{-1},10^{-2},\dots\},
$$

计算

$$
R_1(t,v_i)
=
\frac{
\|F(x+tv_i)-F(x)-tA[v_i]\|
}{|t|}.
$$

若二阶光滑，截断主导区应近似按 $O(t)$ 下降。

#### 阶段 4：中心方向差分

另算

$$
C(t,v)
=
\left\|
\frac{F(x+tv)-F(x-tv)}{2t}
-A[v]
\right\|.
$$

在三阶光滑时，中心差分截断误差通常为 $O(t^2)$；它适合验证方向作用。Taylor 余项则更直接对应 Fréchet 定义。两者用途不同。

#### 阶段 5：每尺度搜索坏方向

固定方向可能漏掉移动峰值。对每个 $t$：

1. 随机采样大量单位向量；
2. 选择 $R_1(t,v)$ 最大者；
3. 在单位球面上做局部上升或 power-like 搜索；
4. 保存最坏方向 $v_t$；
5. 检查 $v_t$ 是否随 $t$ 集中到分支、稀疏或约束边界。

这比复用同一批方向更接近统一余项审计。

#### 阶段 6：专项测试

- 分支边界：构造靠近 ReLU/Top-k/tie 的输入；
- 约束：只用切空间或可行锥方向；
- 稀疏：测试零元素激活与索引改变；
- 低精度：比较 float64 参考和目标精度；
- batch/broadcast：改变批大小并检查归约；
- 随机程序：固定随机流或使用可重参数化噪声。

#### 阶段 7：识别尺度区间

典型曲线分为：

1. $t$ 太大：高阶项主导，未进入局部区；
2. 中间区：出现预期 $O(t)$ 或 $O(t^2)$ 斜率；
3. $t$ 太小：消去和舍入使误差停止下降或反升。

若没有中间幂律区，可能原因包括导数实现错误、不可微、尺度病态、随机状态变化或精度不足。

#### 阶段 8：证据边界

即使全部测试通过，也只是有限样本、有限精度证据。它不能替代：

$$
\forall\varepsilon>0\ \exists\delta>0\ \forall h
$$

的数学证明，尤其不能排除未采样的尺度依赖坏方向。

#### 阶段 9：四栏审计表

| 声明 | 已证 | 已测 | 未证/限制 | 框架约定 |
|---|---|---|---|---|
| $A$ 线性 | 若由代码原语组合可形式证明则记录 | 随机叠加测试 | 全 dtype/控制流 | pytree 加法语义 |
| $A=DF(x)$ | 解析推导与余项证明 | 多尺度 Taylor | 未覆盖全部方向/边界 | 自定义 JVP |
| $A^*$ 正确 | 伴随公式推导 | 点积测试 | 数值容差 | 自定义 VJP |
| 经典可微 | 定理假设核验 | 只能提供证据 | 分支/约束/随机性 | 不可微点选择 |

这种写法能防止把“测试通过”升级为“定理已证”，也能防止把“框架有返回值”写成“经典导数存在”。

## 总结：一套可迁移的解题模板

面对新的向量、矩阵或函数空间映射：

1. 写出 $F:X\to Y$ 与基点；
2. 选择并声明输入输出范数；
3. 写一般扰动 $h$；
4. 作精确增量 $F(a+h)-F(a)$；
5. 收集对 $h$ 线性的项，得到候选 $A[h]$；
6. 检查 $A$ 的线性与有界性；
7. 把其余项写成 $r(h)$；
8. 证明 $\|r(h)\|/\|h\|\to0$；
9. 再选择梯度、Jacobian、JVP 或 VJP 表示；
10. 最后讨论数值验证、程序规则与 AI 应用边界。

只要这十步没有跳过，绝大多数多元与矩阵求导错误都会在进入复杂链式法则之前暴露。
