---
type: solution
status: draft
area: [labs, math/calculus, math/linear-algebra, math/optimization, ai/automatic-differentiation]
prerequisites: ["[[习题 - Hessian、二阶微分与曲率]]"]
related: ["[[Hessian、二阶微分与曲率]]", "[[多元链式法则与计算图]]", "[[矩阵微分、迹技巧与布局约定]]", "[[自动微分：前向、反向与高阶模式]]", "[[Newton 法、Gauss-Newton 与拟 Newton 法]]", "[[练习与测验 MOC]]"]
sources: ["MIT-18.S096-Second-Derivatives", "Boyd-Vandenberghe-Convex-Optimization", "JAX-Autodiff-Cookbook-HVP", "PyTorch-Jacobians-Hessians-HVP", "Pearlmutter-1994-HVP", "Martens-2020-Natural-Gradient-GGN", "Su-10588-Hessian-Approx"]
created: 2026-08-17
updated: 2026-08-17
---

# 解答 - Hessian、二阶微分与曲率

> [!abstract] 使用说明
> 本解答按“类型 → 坐标 → 作用 → 几何 → 验证 → AI 解释”展开。核对时不要只看矩阵结果：必须确认标量函数、方向、参数树、内积、光滑性、batch 与曲率对象都与题目一致。

## A 级：对象、类型与逻辑边界

### CALC-HC-A01：翻译十六个二阶声明

#### 1. 二阶导数属于连续双线性映射空间

$$
D^2f(x)\in\mathcal B_2(X\times X;\mathbb R)
$$

表示二阶 Fréchet 导数接收两个输入方向 $u,v\in X$，返回实数，并分别对两个方向线性且连续。这里没有选基，也不需要内积。

#### 2. 对微分映射再求导

$$
D^2f(x)[u,v]
=
\bigl(D(Df)(x)[u]\bigr)[v].
$$

$Df:X\to X^*$；先沿 $u$ 对这个泛函值函数求导，得到 $X^*$ 中元素，再让它作用在 $v$ 上。这个公式解释了双线性类型的来源。

#### 3. Hessian 的坐标元素

$$
H_{ij}=D^2f(x)[e_i,e_j].
$$

选定标准基后，用二阶双线性型测量一对基向量，所得标量放入第 $(i,j)$ 个坐标。矩阵依赖所选基。

#### 4. 双线性型的矩阵表示

$$
D^2f(x)[u,v]=u^\top Hv.
$$

这是有限维实坐标表达；$u,v\in\mathbb R^n$，$H\in\mathbb R^{n\times n}$。抽象双线性型不依赖欧氏内积，但把它写成矩阵乘法需要坐标。

#### 5. Hessian 是梯度的 Jacobian

$$
H=D(\nabla f)(x).
$$

这要求使用固定欧氏内积，把 $Df$ 通过 Riesz 表示成列梯度 $\nabla f$。若度量随点变化，则普通梯度导数还会包含度量变化，不应原样套用。

#### 6. 二阶对称性

$$
D^2f(x)[u,v]=D^2f(x)[v,u].
$$

标准二阶 Fréchet 可微条件下二阶导数对称；坐标教材通常用 $f\in C^2$ 作为清楚的充分条件。只知道某点混合偏导分别存在不够。

#### 7. 二阶 Taylor–Peano 模型

$$
f(x+h)=f(x)+g^\top h+\frac12h^\top Hh+o(\|h\|^2).
$$

它说扣除常数、一阶和二阶局部项后，余项相对 $\|h\|^2$ 消失。一个安全的充分条件是 $D^2f$ 在 $x$ 邻域存在且在 $x$ 连续。

#### 8. 方向曲率

$$
\left.\frac{d^2}{dt^2}f(x+tv)\right|_{t=0}=v^\top Hv.
$$

沿直线把多元函数限制成一元函数；右端是标量，不是 HVP 向量。

#### 9. 极化恒等式

若

$$
q(w)=D^2f(x)[w,w],
$$

且二阶双线性型对称，则

$$
D^2f[u,v]
=
\frac14(q(u+v)-q(u-v)).
$$

它说明所有方向二次型包含全部混合双线性信息。

#### 10. Rayleigh 商界

对实对称 Hessian 和非零 $v$，

$$
\lambda_{\min}(H)
\le
\frac{v^\top Hv}{\|v\|^2}
\le
\lambda_{\max}(H).
$$

若 $v$ 归一化，Rayleigh 商就是单位方向曲率。

#### 11. HVP

$$
Hv=D(\nabla f)(x)[v].
$$

HVP 是梯度映射沿输入 tangent $v$ 的 JVP。输出与 $x$、$v$ 同形状，不需要形成完整 $H$。

#### 12. 用 HVP 恢复 Hessian

$$
H=[He_1\;\cdots\;He_n].
$$

矩阵第 $j$ 列是对第 $j$ 个标准基方向的 HVP。此法适合小型验证，需要 $n$ 次作用和 $O(n^2)$ 存储。

#### 13. 非线性重参数化公式

$$
H_{f\circ\phi}
=
J_\phi^\top H_fJ_\phi
+
\sum_i(\partial_if)H_{\phi_i}.
$$

第一项是双线性曲率拉回，第二项来自坐标映射本身的弯曲。所有量在对应点 $x=\phi(z)$ 取值。仿射变换或 $f$ 的驻点处，第二项消失。

#### 14. 非线性最小二乘 Hessian

$$
H_L=J_r^\top J_r+\sum_ir_iH_{r_i}.
$$

要求 $L=\tfrac12\sum_ir_i^2$ 且各残差二阶可微。第一项 PSD；第二项可不定。GN 只保留第一项。

#### 15. generalized Gauss–Newton

$$
G_{\mathrm{GGN}}=J_z^\top H_\ell J_z.
$$

对 $L(\theta)=\ell(z(\theta))$，它保留输出损失曲率经模型 Jacobian 的拉回。若 $H_\ell\succeq0$，则 GGN PSD；它不含模型输出的二阶项。

#### 16. Hutchinson 恒等式

若随机向量满足

$$
\mathbb E[zz^\top]=I,
$$

则

$$
\mathbb E[z^\top Hz]
=
\mathbb E[\operatorname{tr}(Hzz^\top)]
=
\operatorname{tr}(H).
$$

有限 probe 平均只是无偏随机估计；必须报告分布、样本数与方差/置信区间。

### CALC-HC-A02：判断二十个断言

1. **错。** 二阶本体是双线性映射；$n\times n$ 只适用于标量函数的有限维坐标表示。
2. **对。** 这是标量函数二阶导数的类型。
3. **对。** $D^2F(x):\mathbb R^n\times\mathbb R^n\to\mathbb R^m$，坐标中可看作每个输出一个 Hessian。
4. **错。** 仅在一点存在的混合偏导未必相等；$C^2$ 是常用充分条件。
5. **对。** 连续二阶偏导保证混合偏导相等。
6. **错。** $Hv\in\mathbb R^n$，$v^\top Hv\in\mathbb R$。
7. **错。** 取

$$
H=\begin{bmatrix}1&1\\1&1\end{bmatrix},
\qquad
v=\begin{bmatrix}1\\-1\end{bmatrix}
$$

时二者都为零；为了得到“曲率零但 HVP 非零”，可取

$$
H=\begin{bmatrix}0&1\\1&0\end{bmatrix},
\qquad
v=e_1,
$$

则 $v^\top Hv=0$ 而 $Hv=e_2\ne0$。
8. **对。** 在二阶 Taylor 余项条件下，这是严格局部极小的充分条件。
9. **错。** $x^4-y^4$ 在原点 Hessian 为零却是鞍点。
10. **错。** $x^4$ 严格凸，但 $f''(0)=0$。
11. **对。** 需要域开且凸、函数 $C^2$。
12. **错。** 一般应为

$$
\nabla\left(\frac12x^\top Ax\right)
=
\frac{A+A^\top}{2}x.
$$

13. **对。** $Hv=D(\nabla f)[v]$ 可用混合 AD 计算。
14. **对。** 每次得到一列；大型模型通常不可行。
15. **对。** 由 Hessian 对称性。
16. **错。** 精确 Hessian 还含 $\sum_ir_iH_{r_i}$。
17. **对。** 因为

$$
v^\top Gv=(Jv)^\top H_\ell(Jv)\ge0.
$$

18. **错。** empirical Fisher 是观测逐样本梯度外积平均，一般不等于损失 Hessian。
19. **错。** 仿射重参数化就给 $S^\top HS$，特征值通常改变；非线性时还有梯度相关项。
20. **错。** 折点处框架可能按预定分支继续求导，返回程序约定值，不证明经典二阶可微。

### CALC-HC-A03：为十五个任务选择最直接工具

| 任务 | 最直接工具 | 理由与边界 |
|---|---|---|
| 1 | 二阶 Fréchet 定义 | $D(Df)$ 的类型直接产生两个方向 |
| 2 | 二阶 Taylor 积分余项 | 可用 Hessian 连续性或 Lipschitz 常数定量控制 |
| 3 | 方向限制 | 对 $t\mapsto f(x+tv)$ 求二阶导得到 $v^\top Hv$ |
| 4 | 极化恒等式 | 从 $q(u\pm v)$ 恢复混合项 |
| 5 | 谱分解/Rayleigh 商 | 最大 Rayleigh 商在最大特征向量达到 |
| 6 | Rayleigh 商或最小特征值 | 负 Rayleigh 商给下降二次方向；还需驻点才能直接分类 |
| 7 | full Hessian | 维数小且确实需要全部坐标 |
| 8 | HVP | 输出 $O(n)$，不存 $O(n^2)$ 数组 |
| 9 | 梯度中心差分 | 与高阶 AD 路径相对独立；需步长扫描 |
| 10 | 双线性对称测试 | 比较 $u^\top Cv$ 与 $v^\top Cu$ |
| 11 | Lanczos | 只需反复矩阵向量作用；结果依赖迭代收敛 |
| 12 | Hutchinson | $z^\top Hz$ 的均值估计 trace；需不确定性 |
| 13 | GN/GGN 分解 | 丢弃残差/模型二阶项得到 PSD 结构 |
| 14 | Sylvester 惯性定律 | 可逆合同保持正负零惯性，不保持特征值数值 |
| 15 | 阻尼线性求解 | CG/MINRES 等只需 $v\mapsto Hv+\lambda v$；算法依赖定性 |

## B 级：手算、形状与谱

### CALC-HC-B01：一个二维非凸函数的完整二阶审计

#### 1. 梯度与 Hessian

$$
f(x,y)=x^3+xy^2-2x+4y.
$$

所以

$$
\nabla f(x,y)
=
\begin{bmatrix}
3x^2+y^2-2\\
2xy+4
\end{bmatrix},
$$

$$
H_f(x,y)
=
\begin{bmatrix}
6x&2y\\
2y&2x
\end{bmatrix}.
$$

#### 2. 对称性条件

$f$ 是多项式，属于 $C^\infty$，所以混合偏导相等，Hessian 对称。

#### 3. 在 $a=(1,2)$ 处

$$
H(a)=
\begin{bmatrix}
6&4\\
4&2
\end{bmatrix}.
$$

同时

$$
\nabla f(a)=
\begin{bmatrix}5\\8\end{bmatrix},
\qquad
f(a)=11.
$$

#### 4. HVP 与方向曲率

对

$$
v=\begin{bmatrix}1\\-1\end{bmatrix},
$$

有

$$
Hv=
\begin{bmatrix}2\\2\end{bmatrix},
$$

但

$$
v^\top Hv=(1,-1)\begin{bmatrix}2\\2\end{bmatrix}=0.
$$

$Hv\ne0$ 说明梯度沿 $v$ 的变化不为零；方向曲率为零说明这次梯度变化与 $v$ 正交，因此沿同一方向做配对时二次项消失。

#### 5. 特征值

特征多项式为

$$
\lambda^2-8\lambda-4=0,
$$

故

$$
\lambda_{1,2}=4\pm2\sqrt5.
$$

一个为正，一个为负，所以 Hessian 不定；相对切平面存在正、负方向二次弯曲。

#### 6. 为什么不能称 $a$ 为驻点鞍点

因为

$$
\nabla f(a)=(5,8)^\top\ne0.
$$

足够小位移中一阶项通常主导。Hessian 不定只说明二阶部分有两种符号，不等于该点满足鞍点的驻点条件。

#### 7. 二阶 Taylor 模型

令 $h=(h_1,h_2)^\top$，则

$$
\begin{aligned}
f(a+h)
&=11+5h_1+8h_2\\
&\quad+\frac12
\left(6h_1^2+8h_1h_2+2h_2^2\right)
+o(\|h\|^2).
\end{aligned}
$$

### CALC-HC-B02：非对称系数矩阵与二次优化

#### 1. 对称部分

$$
S=\frac{A+A^\top}{2}
=
\begin{bmatrix}
2&1\\
1&6
\end{bmatrix}.
$$

#### 2. 二次型只看对称部分

写

$$
A=S+K,
\qquad
K=\frac{A-A^\top}{2},
\qquad
K^\top=-K.
$$

标量 $x^\top Kx$ 的转置为

$$
(x^\top Kx)^\top=x^\top K^\top x=-x^\top Kx,
$$

故它只能为零，所以 $x^\top Ax=x^\top Sx$。

#### 3. 梯度与 Hessian

$$
\nabla f(x)=Sx+b,
\qquad
H_f=S.
$$

#### 4. 强凸与平滑常数

$S$ 的特征多项式

$$
\lambda^2-8\lambda+11=0
$$

给出

$$
\lambda_\pm=4\pm\sqrt5.
$$

二者均正，所以 $f$ 强凸。可取

$$
\mu=4-\sqrt5,
\qquad
L=4+\sqrt5.
$$

#### 5. 唯一驻点

解

$$
Sx_*=-b=
\begin{bmatrix}2\\8\end{bmatrix}
$$

得

$$
x_*
=
\begin{bmatrix}
4/11\\14/11
\end{bmatrix}.
$$

由于 $S\succ0$，它是唯一全局极小点。

#### 6. 谱条件数

$$
\kappa_2(S)
=
\frac{4+\sqrt5}{4-\sqrt5}
=
\frac{21+8\sqrt5}{11}.
$$

#### 7. HVP 与方向曲率

$$
v=\begin{bmatrix}2\\-1\end{bmatrix},
\qquad
Hv=
\begin{bmatrix}3\\-4\end{bmatrix},
$$

$$
v^\top Hv=2\cdot3+(-1)(-4)=10.
$$

#### 8. 直接写 $H=A$ 的错误

$A$ 非对称，而光滑标量函数 Hessian 必须对称。反对称部分根本不影响 $x^\top Ax$，所以真正 Hessian 是 $S$。

### CALC-HC-B03：softmax 交叉熵的输出空间曲率

#### 1. 梯度

记

$$
Z=\sum_je^{z_j},
\qquad
p_i=\frac{e^{z_i}}Z.
$$

则

$$
\frac{\partial}{\partial z_i}\log Z=p_i,
$$

所以

$$
\nabla_z\ell=p-y.
$$

#### 2. Hessian

softmax Jacobian 满足

$$
\frac{\partial p_i}{\partial z_j}
=p_i(\delta_{ij}-p_j),
$$

于是

$$
H_z=\operatorname{Diag}(p)-pp^\top.
$$

#### 3. 数值矩阵

代入 $p=(1/2,1/3,1/6)^\top$：

$$
H_z
=
\frac1{36}
\begin{bmatrix}
9&-6&-3\\
-6&8&-2\\
-3&-2&5
\end{bmatrix}.
$$

#### 4. 零方向

$$
H_z\mathbf1
=
p-p(p^\top\mathbf1)
=p-p=0.
$$

这是因为

$$
\operatorname{softmax}(z+c\mathbf1)=\operatorname{softmax}(z),
$$

共同平移 logits 不改变概率。

#### 5. PSD 证明

$$
\begin{aligned}
v^\top H_zv
&=\sum_ip_iv_i^2-\left(\sum_ip_iv_i\right)^2\\
&=\mathbb E_p[v_i^2]-\mathbb E_p[v_i]^2\\
&=\operatorname{Var}_p(v_i)\ge0.
\end{aligned}
$$

#### 6. 指定方向

对 $v=(1,-1,0)^\top$：

$$
Hv
=
\begin{bmatrix}
5/12\\
-7/18\\
-1/36
\end{bmatrix},
$$

$$
v^\top Hv
=
\frac5{12}+\frac7{18}
=
\frac{29}{36}.
$$

#### 7. 标签为什么消失

$-y^\top z$ 对 $z$ 是线性函数，其 Hessian 为零。因此标签影响梯度 $p-y$，不影响 logits Hessian。

#### 8. GGN–vector product

若 $z=z(\theta)$：

1. $a=J_zv$：参数方向的 logits JVP；
2. $b=(\operatorname{Diag}(p)-pp^\top)a$：输出损失 HVP；
3. $J_z^\top b$：VJP 拉回参数空间。

最终得到

$$
G_{\mathrm{GGN}}v
=
J_z^\top H_zJ_zv.
$$

## C 级：证明、反例与坐标

### CALC-HC-C01：Taylor、方向曲率与极化

#### 1. 直线限制的导数

令

$$
\phi(t)=f(x+th).
$$

链式法则给

$$
\phi'(t)=Df(x+th)[h],
$$

$$
\phi''(t)=D^2f(x+th)[h,h].
$$

#### 2. 积分余项

由微积分基本定理

$$
\phi(1)=\phi(0)+\int_0^1\phi'(s)\,ds.
$$

又有

$$
\phi'(s)=\phi'(0)+\int_0^s\phi''(t)\,dt.
$$

代回并交换积分次序：

$$
\begin{aligned}
\phi(1)
&=\phi(0)+\phi'(0)
+\int_0^1\int_0^s\phi''(t)\,dt\,ds\\
&=\phi(0)+\phi'(0)
+\int_0^1(1-t)\phi''(t)\,dt.
\end{aligned}
$$

替换回 $f$ 即得题设公式。

#### 3. 小 $o$ 余项

减去冻结在 $x$ 的二阶项：

$$
R_2
=
\int_0^1(1-t)
\bigl(D^2f(x+th)-D^2f(x)\bigr)[h,h]\,dt.
$$

于是

$$
|R_2|
\le
\frac12
\sup_{t\in[0,1]}
\|D^2f(x+th)-D^2f(x)\|\,\|h\|^2.
$$

由连续性，上确界因子随 $h\to0$ 趋于零，故 $R_2=o(\|h\|^2)$。

#### 4. Lipschitz Hessian 的三次界

若

$$
\|D^2f(x+th)-D^2f(x)\|
\le\rho t\|h\|,
$$

则

$$
\begin{aligned}
|R_2|
&\le
\int_0^1(1-t)\rho t\|h\|^3\,dt\\
&=\rho\|h\|^3
\left(\frac12-\frac13\right)\\
&=\frac\rho6\|h\|^3.
\end{aligned}
$$

#### 5. 极化

设 $B=D^2f(x)$ 对称。则

$$
q(u+v)=B[u,u]+2B[u,v]+B[v,v],
$$

$$
q(u-v)=B[u,u]-2B[u,v]+B[v,v].
$$

相减后除以 $4$：

$$
B[u,v]=\frac14(q(u+v)-q(u-v)).
$$

#### 6. 为什么坐标轴曲率不够

$q(e_i)=H_{ii}$ 只能恢复对角元素。混合项 $H_{ij}$ 要用 $q(e_i+e_j)$ 或其他组合方向才能恢复。例如

$$
\begin{bmatrix}1&0\\0&1\end{bmatrix}
\quad\text{和}\quad
\begin{bmatrix}1&1/2\\1/2&1\end{bmatrix}
$$

在两个坐标轴上的二次型都为 $1$，但混合曲率不同。

### CALC-HC-C02：二阶最优性与凸性边界

#### 1. 正定充分条件

若 $\nabla f(x_*)=0$ 且 $H_*\succ0$，存在 $\mu>0$ 使

$$
h^\top H_*h\ge\mu\|h\|^2.
$$

Taylor 公式给

$$
f(x_*+h)-f(x_*)
=
\frac12h^\top H_*h+o(\|h\|^2).
$$

取邻域使余项绝对值不超过 $\mu\|h\|^2/4$，则非零小 $h$ 满足

$$
f(x_*+h)-f(x_*)
\ge
\frac\mu4\|h\|^2>0.
$$

故为严格局部极小。

#### 2. 不定推出鞍点

不定意味着存在单位向量 $u,v$ 使

$$
u^\top H_*u>0,
\qquad
v^\top H_*v<0.
$$

沿 $tu$ 和 $tv$ 的 Taylor 二次主项分别为正、负；充分小的 $t\ne0$ 下，函数在 $x_*$ 任意邻域既取更大值又取更小值，所以是鞍点。

#### 3. 零 Hessian 三类反例

在原点：

- $x^4\ge0$，严格局部极小；
- $-x^4\le0$，严格局部极大；
- $x^4-y^4$ 沿 $y=0$ 为正，沿 $x=0$ 为负，是鞍点。

三者梯度和 Hessian 都为零，差异来自四阶项。

#### 4. 凸性二阶判据

若 $f$ 凸且二阶可微，限制到任意直线

$$
\phi(t)=f(x+tv)
$$

仍凸，所以

$$
\phi''(0)=v^\top H_f(x)v\ge0.
$$

因此 $H_f(x)\succeq0$。

反之若 Hessian 处处 PSD，对任意 $x,y$ 令

$$
\phi(t)=f(x+t(y-x)),\quad t\in[0,1].
$$

则

$$
\phi''(t)
=(y-x)^\top H_f(x+t(y-x))(y-x)\ge0.
$$

$\phi$ 为一维凸函数，于是

$$
f((1-t)x+ty)
\le
(1-t)f(x)+tf(y).
$$

#### 5. 严格凸但 Hessian 不处处正定

$f(x)=x^4$ 在 $\mathbb R$ 上严格凸，但

$$
f''(0)=0.
$$

#### 6. 域凸性不可删

凸性定义要求任意两点之间的线段留在定义域。例

$$
f(x)=\frac1{x^2},
\qquad
\operatorname{dom}f=\mathbb R\setminus\{0\}
$$

在每个点有 $f''(x)=6/x^4>0$，但整个定义域不是凸集，不能称其在该非凸域上满足标准全局凸性线段不等式。

#### 7. 二侧二次界

令 $h=y-x$。积分 Taylor 公式给

$$
f(y)-f(x)-\nabla f(x)^\top h
=
\int_0^1(1-t)h^\top H_f(x+th)h\,dt.
$$

用谱界夹住被积函数：

$$
\mu\|h\|^2
\le h^\top H_f(x+th)h
\le L\|h\|^2.
$$

积分 $\int_0^1(1-t)dt=1/2$，得到

$$
\frac\mu2\|h\|^2
\le
f(y)-f(x)-\nabla f(x)^\top h
\le
\frac L2\|h\|^2.
$$

### CALC-HC-C03：非线性重参数化的额外项

#### 1. 分量推导

先有

$$
\frac{\partial\widetilde f}{\partial z_a}
=
\sum_i
\frac{\partial f}{\partial x_i}
\frac{\partial\phi_i}{\partial z_a}.
$$

再对 $z_b$ 求导：

$$
\begin{aligned}
\frac{\partial^2\widetilde f}{\partial z_b\partial z_a}
&=
\sum_{i,j}
\frac{\partial^2f}{\partial x_j\partial x_i}
\frac{\partial\phi_j}{\partial z_b}
\frac{\partial\phi_i}{\partial z_a}\\
&\quad+
\sum_i
\frac{\partial f}{\partial x_i}
\frac{\partial^2\phi_i}{\partial z_b\partial z_a}.
\end{aligned}
$$

矩阵形式就是

$$
H_{\widetilde f}
=J_\phi^\top H_fJ_\phi
+\sum_i(\partial_if)H_{\phi_i}.
$$

#### 2. 仿射情形

若 $\phi(z)=Sz+c$，所有分量 $\phi_i$ 的 Hessian 为零，所以只剩

$$
H_{\widetilde f}=S^\top H_fS.
$$

#### 3. 驻点情形

若 $\nabla_xf=0$，则所有系数 $\partial_if$ 为零，额外项消失。

#### 4. 具体计算

复合函数为

$$
\widetilde f(z)
=
\frac12z_1^2+\frac12e^{2z_2}.
$$

直接求导：

$$
\nabla_z\widetilde f
=
\begin{bmatrix}
z_1\\e^{2z_2}
\end{bmatrix},
$$

$$
H_{\widetilde f}
=
\begin{bmatrix}
1&0\\0&2e^{2z_2}
\end{bmatrix}.
$$

在 $z=(0,0)$ 为

$$
H_{\widetilde f}(0,0)
=
\begin{bmatrix}1&0\\0&2\end{bmatrix}.
$$

再用公式核对。此时 $x=(0,1)$，

$$
H_f=I,
\qquad
J_\phi=I,
\qquad
\nabla_xf=(0,1)^\top.
$$

$\phi_1=z_1$ 的 Hessian 为零，$\phi_2=e^{z_2}$ 的 Hessian 在原点为

$$
H_{\phi_2}
=
\begin{bmatrix}0&0\\0&1\end{bmatrix}.
$$

因此

$$
J_\phi^\top H_fJ_\phi
+(\partial_2f)H_{\phi_2}
=I+
\begin{bmatrix}0&0\\0&1\end{bmatrix}
=
\begin{bmatrix}1&0\\0&2\end{bmatrix}.
$$

#### 5. 漏掉的项

只保留合同项会错误得到 $I$，漏掉 $(2,2)$ 坐标上的额外 $1$。它来自坐标曲线 $e^{z_2}$ 自身的加速度与非零梯度配对。

#### 6. 非不变性

一般变换既包含合同，又包含梯度相关项；即使在驻点只有合同，合同也不保持特征值数值，只在可逆时保持惯性。因此普通 Hessian 谱不是一般参数化不变量。

## D 级：自动微分、验证与数值实验

### CALC-HC-D01：设计一套 HVP 三层验证实验

令 $A$ 的第 $i$ 行为 $a_i^\top$，定义

$$
t=Ax,
\qquad
s=\sigma(t),
\qquad
w=s\odot(1-s).
$$

#### 1. 解析导数

因为 softplus 的导数是 sigmoid，

$$
\nabla f(x)=A^\top s+\lambda x.
$$

所以

$$
H_f(x)=A^\top\operatorname{Diag}(w)A+\lambda I.
$$

#### 2. 解析 HVP

按结合顺序计算：

$$
Hv
=
A^\top\bigl(w\odot(Av)\bigr)+\lambda v.
$$

只需要两次矩阵向量乘和逐元素乘法。

#### 3. forward-over-reverse

```python
def loss(x):
    return softplus(A @ x).sum() + 0.5 * lam * vdot(x, x)

def hvp_ad(x, v):
    return jvp(grad(loss), (x,), (v,))[1]
```

将结果与解析 `A.T @ (w * (A @ v)) + lam * v` 比较。

#### 4. 中心差分扫描

对

$$
\varepsilon\in
\{10^{-1},10^{-2},\ldots,10^{-7}\}
$$

计算

$$
h_{\mathrm{fd}}(\varepsilon)
=
\frac{\nabla f(x+\varepsilon v)-\nabla f(x-\varepsilon v)}{2\varepsilon}
$$

与 AD HVP 的相对误差。float32 可根据尺度调整区间；高可信验证宜再用 float64。

#### 5. 对称性检查

随机生成 $u,v$ 并归一化，计算

$$
E_{\mathrm{sym}}
=
\frac{|u^\top Hv-v^\top Hu|}
{\max(1,|u^\top Hv|,|v^\top Hu|)}.
$$

重复多个 seed。

#### 6. Taylor 缩放

定义

$$
r_1(t)=f(x+tv)-f(x)-t\nabla f(x)^\top v,
$$

$$
r_2(t)=r_1(t)-\frac12t^2v^\top Hv.
$$

对 $t, t/2,t/4,\ldots$ 记录残差比。理想中间区间内

$$
\frac{|r_1(t)|}{|r_1(t/2)|}\approx4,
\qquad
\frac{|r_2(t)|}{|r_2(t/2)|}\approx8.
$$

#### 7. U 形误差曲线

中心差分截断误差随 $\varepsilon$ 变小而下降；但两个相近梯度相减会产生消减误差，除以更小 $\varepsilon$ 又放大舍入误差，所以误差常先降后升。

#### 8. 记录清单

- $A,x,u,v$ 的生成种子和范数；
- dtype/device；
- softplus 的稳定实现；
- 样本求和或平均；
- $\lambda$ 是否同时进入解析与 AD 目标；
- 参数树 flatten/unflatten 顺序；
- 差分步长；
- 绝对和相对误差；
- 编译 warm-up 与 profiling 是否分开。

### CALC-HC-D02：高阶 AD 接口与模式审计

#### 方法对照

| 方法 | 结果 | 存储/成本倾向 | 适用场景 |
|---|---|---|---|
| `hessian(L)(theta)` | 完整块 Hessian | 至少 $O(n^2)$ 输出存储 | 小模型、验证、确需所有坐标 |
| `jvp(grad(L), ..., v)` | $Hv$ | 输出 $O(n)$；forward-over-reverse | 大模型矩阵自由二阶作用 |
| `grad(vdot(grad(L), v))` | $H^\top v=Hv$ | reverse-over-reverse；高阶图可能更大 | forward AD 覆盖不足时备选 |
| 基向量重复 HVP | 完整 Hessian 各列 | $n$ 次作用和 $O(n^2)$ 存储 | 小型一致性测试 |
| pytree/tuple 块 | 各参数组二阶块 | 结构随 API 布局 | 模块化审计、块近似 |

#### forward-over-reverse

先用 reverse mode 得到标量损失对海量参数的梯度，再对梯度程序沿一个方向做 forward JVP。这正计算

$$
D(\nabla L)(\theta)[v]=Hv.
$$

#### reverse-over-reverse

先构造标量

$$
s(\theta)=\nabla L(\theta)^\top v,
$$

再反向求梯度得到 $H^\top v$。光滑标量目标下由对称性等于 $Hv$。

#### 为什么 $v$ 要视为常量

若 $v=v(\theta)$，则

$$
\nabla_\theta(\nabla L^\top v)
=
Hv+(Dv)^\top\nabla L.
$$

第二项使结果不再是纯 HVP。因此要传入独立 tangent，或在必要时停止对 $v$ 的梯度。

#### 高阶微分故障来源

- 自定义 VJP 可能只定义一阶反传，且反传程序不可再微分；
- 自定义 JVP 若不满足真实导数规律，高阶结果会一致地错误；
- 原地修改和 alias 破坏函数式变换；
- dropout、随机采样和状态更新令两次调用不是同一函数；
- 某些算子没有 forward AD 或二阶导规则；
- `detach`、整数索引和离散控制流截断路径；
- 参数树叶子顺序或空叶处理错误。

#### 小模型测试

取 $n\le20$ 的确定性网络：

1. 以 float64 计算 full Hessian $H$；
2. 检查 $\|H-H^\top\|_F$；
3. 对多个随机 $v$ 比较 `H @ v`、forward-over-reverse 和 reverse-over-reverse；
4. 与梯度中心差分比较；
5. 逐块检查 pytree flatten 后的布局；
6. 再扩大模型做独立性能 profiling。

框架文档只能说明接口语义，不能保证当前模型的算子覆盖、内存和速度最优。

### CALC-HC-D03：矩阵自由谱报告

一份合格设计如下。

#### 1. 先锁定曲率算子

报告开头写明

$$
C=H,
\quad G_{\mathrm{GGN}},
\quad F,
\quad\text{或 }F_{\mathrm{emp}}.
$$

这些对象不可混名。固定数据、模型状态、loss reduction 和正则。

#### 2. 对称性预检

对至少十对随机 $u,v$ 计算

$$
u^\top C(v)-v^\top C(u).
$$

若明显不对称，Lanczos 的对称矩阵假设失效，应先排查实现。

#### 3. 极端特征值

- 最大代数特征值：对 $C$ 运行 Lanczos 或幂迭代；
- 最小代数特征值：对 $-C$ 求最大特征值后取负，或使用能选取最小代数特征值的 Lanczos；
- 报告 Ritz 残差

$$
\|Cq-\widehat\lambda q\|.
$$

只求最大绝对值可能返回巨大负特征值的绝对值，不能代替最大代数特征值。

#### 4. Hutchinson trace

用独立 Rademacher probes $z_k\in\{-1,+1\}^n$：

$$
\widehat\tau
=
\frac1K\sum_{k=1}^Kz_k^\top C z_k.
$$

报告样本标准差、标准误和随 $K$ 的稳定性。复用同一 probes 可降低不同模型比较的随机差异。

#### 5. 阻尼线性系统

用 CG 的前提是 $C+\lambda I$ 对称正定；若精确 Hessian 仍不定，应增大阻尼、使用 MINRES，或采用能处理负曲率的信赖域方法。报告相对残差

$$
\frac{\|(C+\lambda I)s-b\|}{\|b\|}.
$$

#### 6. batch 波动

对多个固定 seed 的 batch 重复上述估计，分别报告 batch 内迭代误差和 batch 间统计波动。不要把二者合并成一个模糊误差条。

#### 7. 为什么“最大特征值大”不够

它没有说明：

- 是否有更大幅度的负曲率；
- 参数缩放是否改变谱；
- loss 是 sum 还是 mean；
- 是否包含权重衰减；
- 是 Hessian 还是 PSD 替代；
- Ritz 对是否收敛；
- batch 波动多大；
- 该特征方向是否与实际优化步相关。

因此不能单凭一个数声称模型“更尖锐”或泛化更差。

## E 级：结构化推导与 AI 迁移

### CALC-HC-E01：Gauss–Newton 何时漏掉关键负曲率

#### 1. 残差导数

$$
r_1=x^2-1,
\qquad
r_2=xy.
$$

所以

$$
J_r
=
\begin{bmatrix}
2x&0\\
y&x
\end{bmatrix},
$$

$$
H_{r_1}
=
\begin{bmatrix}2&0\\0&0\end{bmatrix},
\qquad
H_{r_2}
=
\begin{bmatrix}0&1\\1&0\end{bmatrix}.
$$

#### 2. 精确分解

由

$$
\nabla L=J_r^\top r
$$

再求导：

$$
H_L
=
J_r^\top J_r
+r_1H_{r_1}+r_2H_{r_2}.
$$

具体地，

$$
G=J_r^\top J_r
=
\begin{bmatrix}
4x^2+y^2&xy\\
xy&x^2
\end{bmatrix},
$$

$$
r_1H_{r_1}+r_2H_{r_2}
=
\begin{bmatrix}
2x^2-2&xy\\
xy&0
\end{bmatrix}.
$$

所以

$$
H_L
=
\begin{bmatrix}
6x^2+y^2-2&2xy\\
2xy&x^2
\end{bmatrix}.
$$

#### 3. 在 $(0,0)$

$$
J_r(0,0)=0,
\qquad
G(0,0)=0.
$$

但 $r_1=-1,r_2=0$，故

$$
H_L(0,0)
=
\begin{bmatrix}-2&0\\0&0\end{bmatrix}.
$$

沿 $e_1$ 的真实方向曲率为 $-2$，GN 为 $0$。GN 完全漏掉由非零残差乘残差函数二阶导产生的负曲率。

#### 4. 在根 $(1,0)$

此时 $r=0$，第二项消失：

$$
J_r(1,0)
=
\begin{bmatrix}2&0\\0&1\end{bmatrix},
$$

$$
G(1,0)=H_L(1,0)
=
\begin{bmatrix}4&0\\0&1\end{bmatrix}.
$$

#### 5. 一个非根点

取 $(0,1)$ 与 $v=e_1$。有

$$
G(0,1)
=
\begin{bmatrix}1&0\\0&0\end{bmatrix},
$$

$$
H_L(0,1)
=
\begin{bmatrix}-1&0\\0&0\end{bmatrix}.
$$

因此

$$
v^\top Gv=1,
\qquad
v^\top H_Lv=-1.
$$

两者甚至符号相反。

#### 6. “残差小”不是完整保证

被丢弃项的范数满足粗界

$$
\left\|\sum_ir_iH_{r_i}\right\|
\le
\sum_i|r_i|\,\|H_{r_i}\|.
$$

残差小有帮助，但若 $H_{r_i}$ 很大、$J_r^\top J_r$ 近奇异、所需方向恰在 GN 的小特征子空间，残差项仍可能相对重要。

#### 7. 算法行为

在 $(0,0)$，GN 没有看到 $x$ 方向的负曲率，可能只因阻尼而移动；精确 Newton 模型识别负曲率但二次模型无下界，不能直接无保护求最小。阻尼 GN 提供稳定 PSD 系统，精确 Newton 则需要信赖域、修正 Hessian 或负曲率处理。

### CALC-HC-E02：矩阵变量最小二乘的 Hessian 算子

记

$$
R(X)=AXB-C.
$$

#### 1. 梯度

沿扰动 $\Delta$：

$$
DR(X)[\Delta]=A\Delta B.
$$

所以

$$
\begin{aligned}
Df(X)[\Delta]
&=\langle R,A\Delta B\rangle_F\\
&=\operatorname{tr}(R^\top A\Delta B)\\
&=\operatorname{tr}((A^\top RB^\top)^\top\Delta)\\
&=\langle A^\top RB^\top,\Delta\rangle_F.
\end{aligned}
$$

故

$$
\nabla_Xf=A^\top(AXB-C)B^\top.
$$

#### 2. Hessian 作用

梯度对 $X$ 是仿射的，因此

$$
\mathcal H_X[\Delta]
=
A^\top A\,\Delta\,BB^\top.
$$

#### 3. 自伴随

$$
\begin{aligned}
\langle U,\mathcal H[V]\rangle_F
&=\langle U,A^\top AVBB^\top\rangle_F\\
&=\langle AUB,AVB\rangle_F\\
&=\langle A^\top AUBB^\top,V\rangle_F\\
&=\langle\mathcal H[U],V\rangle_F.
\end{aligned}
$$

#### 4. PSD

$$
\langle\Delta,\mathcal H[\Delta]\rangle_F
=
\|A\Delta B\|_F^2\ge0.
$$

#### 5. Kronecker 表示

利用

$$
\operatorname{vec}(M\Delta N)
=(N^\top\otimes M)\operatorname{vec}(\Delta),
$$

且 $BB^\top$ 对称，得到

$$
\operatorname{vec}(\mathcal H[\Delta])
=
(BB^\top\otimes A^\top A)
\operatorname{vec}(\Delta).
$$

#### 6. 严格正定条件

$\mathcal H$ 严格正定当且仅当

$$
A\Delta B=0\Longrightarrow\Delta=0.
$$

对全部 $m\times n$ 矩阵变量，这等价于：

$$
\operatorname{rank}(A)=m
\quad\text{且}\quad
\operatorname{rank}(B)=n,
$$

即 $A$ 满列秩、$B$ 满行秩。

证明充分性：存在左逆 $A_L$ 和右逆 $B_R$，若 $A\Delta B=0$，则

$$
\Delta=A_L(A\Delta B)B_R=0.
$$

必要性可通过任一非零零空间向量构造秩一 $\Delta$。

#### 7. 矩阵自由接口

```python
def hvp(delta):
    return A.T @ (A @ delta @ B) @ B.T

def damped(delta, lam):
    return hvp(delta) + lam * delta
```

CG 中用 Frobenius 内积

```python
vdot(U, V) = sum(U * V)
```

而不形成 $(mn)\times(mn)$ Kronecker 矩阵。

#### 8. 零曲率方向

所有满足

$$
A\Delta B=0
$$

的 $\Delta$ 都是零曲率方向。若 $z\in\ker A$，可构造列落在 $z$ 方向的 $\Delta$；若 $w^\top B=0$，可构造行落在该左零空间方向的 $\Delta$。秩亏会造成不可辨识参数组合和平坦方向。

### CALC-HC-E03：设计一份神经网络曲率审计报告

下面是一份可执行的报告规范。

#### 1. 固定实验对象

记录：

- 模型结构、参数初始化和 checkpoint 哈希；
- 固定数据索引与预处理；
- `eval`/`train` 模式；
- dropout 随机种子和 batch norm 状态；
- loss 是逐样本 sum、mean 还是其他加权；
- 权重衰减是否进入目标；
- dtype/device 和框架版本。

#### 2. 四个对象的定义

精确 Hessian：

$$
H=\nabla_\theta^2L_{\mathcal B}(\theta).
$$

GGN：若 $L=|\mathcal B|^{-1}\sum_b\ell(z_b(\theta),y_b)$，则

$$
G=\frac1{|\mathcal B|}\sum_b
J_b^\top H_{\ell,b}J_b.
$$

模型 Fisher：

$$
F=\frac1{|\mathcal B|}\sum_b
\mathbb E_{\widetilde y\sim p_\theta(\cdot|x_b)}
[s_bs_b^\top].
$$

empirical Fisher 若被选用，必须另名：

$$
F_{\mathrm{emp}}
=
\frac1{|\mathcal B|}\sum_b
g_bg_b^\top
$$

，其中 $g_b$ 使用观测标签。

梯度平方对角代理例如

$$
d_t=\beta d_{t-1}+(1-\beta)g_t\odot g_t.
$$

它不是完整矩阵。

#### 3. 定性保证

| 对象 | PSD 保证 | 负曲率 |
|---|---:|---:|
| 精确 Hessian | 无 | 保留 |
| GGN | 输出损失凸时有 | 丢弃模型二阶负曲率 |
| Fisher | 有 | 无 |
| empirical Fisher | 有 | 无 |
| 梯度平方对角 | 非负对角 | 无，且无非对角耦合 |

#### 4. 同向量比较

固定同一组单位 Rademacher/Gaussian probes $v_k$，比较：

$$
Hv_k,
\quad
Gv_k,
\quad
Fv_k,
\quad
d\odot v_k.
$$

报告相对差异、余弦相似度和二次型

$$
v_k^\top Cv_k.
$$

同一 probes 能减少比较噪声。

#### 5. 验证

- 精确 HVP：解析小模型、梯度中心差分、双线性对称、Taylor 缩放；
- GGN：小模型显式 $J^\top H_\ell J$ 对照，以及 JVP → 输出 HVP → VJP 三段点积检查；
- Fisher：检查 score、标签采样分布和 Monte Carlo 收敛；
- empirical Fisher：逐样本梯度与 batch-summed gradient 严格区分。

#### 6. 谱、trace 与逆作用

- 用 Lanczos 估计精确 Hessian 的最大和最小代数特征值；
- 对 PSD 对象检查最小 Ritz 值是否仅为数值小负数；
- 用共享 Hutchinson probes 比较 trace；
- 用 CG/MINRES 求 $(C+\lambda I)^{-1}b$，报告残差和迭代数；
- 对多个 $\lambda$ 做敏感性分析。

#### 7. 参数化控制

至少做一次功能等价的参数缩放或归一化对照。若函数近似不变而 Hessian 谱明显变化，应明确结论是“坐标 sharpness”，不是参数化不变的内禀属性。

#### 8. 审计“Adam 近似 Hessian”

逐项检查：

1. 是否接近某个驻点；
2. 梯度局部线性化是否成立；
3. 参数波动是否近似零均值且各向同性；
4. Hessian 是否近似对角；
5. Hessian 在平均窗口内是否近似不变；
6. 平方梯度得到的是 $H^2$ 尺度还是 $H$；
7. 负特征值和非对角耦合如何被丢失；
8. $\beta_2$、偏置修正、$\epsilon$ 和学习率如何改变解释。

最终结论只能是条件性代理关系，不能宣称一般等价。

#### 9. 解析保证与经验观察分栏

解析保证示例：

- 光滑标量目标的 Hessian 对称；
- 凸输出损失下 GGN PSD；
- Fisher 和外积矩阵 PSD；
- Hutchinson 在指定 probe 条件下无偏。

经验观察示例：

- 当前 checkpoint 上 $Gv$ 与 $Hv$ 接近；
- 某 batch 下最大特征值变化；
- 梯度平方对角与 Hessian 对角相关；
- 某个阻尼值改善了内层收敛。

#### 10. 可复现与可证伪

- 保存配置、seed、数据索引和代码版本；
- 预先定义指标与停止条件；
- 报告失败 probe、负曲率和不收敛案例；
- 给出原始数值表而非只给平滑曲线；
- 对关键结论提供至少一个反事实对照；
- 明确哪些结论仅适用于该模型、batch 和参数化。

这样的报告才能把“二阶分析”从漂亮图形升级为可复核的科学论证。
