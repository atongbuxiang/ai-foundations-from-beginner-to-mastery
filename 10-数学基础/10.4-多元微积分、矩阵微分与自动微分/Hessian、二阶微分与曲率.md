---
type: concept
status: draft
area: [math/calculus, math/linear-algebra, math/optimization, ai/automatic-differentiation]
aliases: [Hessian second differential and curvature, Hessian 矩阵, 二阶 Fréchet 导数, Hessian-vector product, HVP, 方向曲率]
prerequisites: ["[[Taylor 展开与余项]]", "[[全微分与 Fréchet 导数]]", "[[梯度、方向导数与最陡方向]]", "[[Jacobian、JVP 与 VJP]]", "[[定理 - 有限维谱定理]]", "[[二次型与正定矩阵]]"]
related: ["[[多元链式法则与计算图]]", "[[矩阵微分、迹技巧与布局约定]]", "[[自动微分：前向、反向与高阶模式]]", "[[凸函数、Jensen 不等式与上图集]]", "[[光滑性、强凸性与条件数]]", "[[Newton 法、Gauss-Newton 与拟 Newton 法]]", "[[条件数]]", "[[多元微积分、矩阵微分与自动微分 MOC]]"]
sources: ["MIT-18.S096-Second-Derivatives", "Boyd-Vandenberghe-Convex-Optimization", "JAX-Autodiff-Cookbook-HVP", "PyTorch-Jacobians-Hessians-HVP", "Pearlmutter-1994-HVP", "Martens-2020-Natural-Gradient-GGN", "Su-10588-Hessian-Approx"]
exercises: ["[[习题 - Hessian、二阶微分与曲率]]"]
solutions: ["[[解答 - Hessian、二阶微分与曲率]]"]
created: 2026-08-17
updated: 2026-08-27
---

# Hessian、二阶微分与曲率

> [!abstract] 本章主问题
> 对标量函数 $f:X\to\mathbb R$，二阶导数的本体是对称连续双线性型 $D^2f(x)[u,v]$；在欧氏坐标中，它由 Hessian 矩阵 $H(x)$ 表示。$v^\top Hv$ 测量沿 $v$ 的二阶方向曲率，$Hv=D(\nabla f)(x)[v]$ 是梯度的 JVP。大模型通常不能形成 $n\times n$ 的完整 Hessian，却可以用 HVP、迭代线性代数和结构化正半定近似提取真正需要的二阶信息。

## 学习目标

完成本章后，应能：

1. 区分 $D^2f(x)$、$H_f(x)$、$D^2f(x)[u,v]$、$v^\top Hv$ 与 $Hv$；
2. 从“对 $Df$ 再求导”得到连续双线性映射，而非直接背诵偏导数组；
3. 解释标量函数 Hessian 与向量函数二阶导数的类型差异；
4. 在标准坐标中推导 $H_{ij}=\partial_i\partial_jf$；
5. 给出 Hessian 对称所需的可微性条件，并说明“偏导写得出来”不自动保证对称；
6. 推导二阶 Taylor 模型及其积分余项和小 $o$ 余项；
7. 证明沿直线限制 $\phi(t)=f(x+tv)$ 满足 $\phi''(0)=v^\top Hv$；
8. 用极化恒等式从方向二次型恢复混合双线性项；
9. 用 Rayleigh 商和谱分解解释最大、最小方向曲率；
10. 正确应用二阶充分条件，并识别半正定情形的“不确定”；
11. 由 Hessian 正半定判定 $C^2$ 函数在凸域上的凸性；
12. 用 $\mu I\preceq H\preceq LI$ 解释强凸性、平滑性和条件数；
13. 推导二次函数、最小二乘、log-sum-exp/交叉熵和矩阵最小二乘的 Hessian；
14. 把 HVP 识别为梯度映射的 JVP：$Hv=D(\nabla f)(x)[v]$；
15. 比较 forward-over-reverse、reverse-over-reverse 与 full Hessian 的接口和成本；
16. 用梯度中心差分、双线性对称性和 Taylor 缩放检验 HVP；
17. 说明 HVP 测试通过为何仍不能证明所有二阶实现完全正确；
18. 用基向量 HVP 重建小型 Hessian，并说明大型模型为何不应这样做；
19. 推导非线性最小二乘 Hessian 的 $J^\top J$ 项与残差二阶项；
20. 推导一般复合损失的精确 Hessian 与 generalized Gauss–Newton 分解；
21. 区分 Hessian、Gauss–Newton、GGN、Fisher 与 empirical Fisher；
22. 说明正半定曲率近似为何更适合构造稳定下降步，但会丢失负曲率；
23. 解释 Newton、阻尼 Newton、Newton–CG 和信赖域为何需要不同的曲率处理；
24. 解释 Hessian 特征值、迹、逆作用在优化、影响函数和 Laplace 近似中的意义；
25. 推导仿射与非线性重参数化下 Hessian 的变换公式；
26. 说明 Hessian 特征值与“sharpness”为何依赖参数化和尺度；
27. 识别 ReLU 折点、混合精度、随机 mini-batch 和状态更新对二阶检查的影响；
28. 审计“Adam 等价于对角 Newton”一类说法中隐藏的统计与对角近似；
29. 为真实 AI 目标设计可复核的曲率报告，而不是只打印一个最大特征值；
30. 明确本章与链式法则、优化理论、概率统计和高阶自动微分章节的边界。

> [!question] 初学者读完必须能回答
> 1. $D^2f(x)$、Hessian 矩阵、$Hv$ 与 $v^\top Hv$ 的类型分别是什么？
> 2. Hessian 对称需要哪些正则性条件？
> 3. 二阶方向曲率为什么由 Rayleigh 商和特征方向控制？
> 4. 半正定 Hessian 为什么对驻点分类仍可能没有结论？
> 5. HVP 怎样在不形成 $n\times n$ 矩阵时计算曲率作用？
> 6. 精确 Hessian、Gauss–Newton、GGN 与 Fisher 各自保留或舍弃什么？
> 7. 参数化改变时，Hessian 特征值与 sharpness 为什么会改变？

先用下图回答一个视觉问题：**二阶导数怎样从双线性型变成方向曲率，又怎样在大模型里通过矩阵自由作用被使用？**

![[00-知识库管理/_assets/figures/hessian-curvature-hvp/fig-hessian-curvature-hvp-v2.svg|880]]

> [!figure] 图 10.4.8｜二阶对象的类型、特征方向曲率与矩阵自由 HVP
> A 区分二阶双线性型、其 Hessian 坐标表示和方向配对；B 用局部二次模型与特征方向解释正、负和近零曲率；C 展示 $v\mapsto Hv$ 的矩阵自由接口，以及精确 Hessian 与 GGN 正半定作用链的结构差别。来源：独立绘制；生成脚本：[[plot_hessian_curvature_hvp.py]]；确定性结构与解析数据，无随机种子。

**怎样读图。** A 先按输入/输出类型区分 $D^2f[u,v]$、$Hv$ 与 $v^\top Hv$；B 再沿特征向量读取曲率符号与强度；C 最后只跟踪“给一个向量、返回曲率作用”的接口，理解大型模型为何通常用 Krylov 方法而不物化完整 Hessian。

**适用边界（图没有证明什么）。** 二维曲面不能代表高维损失景观，有限几个 HVP 也不能恢复全部谱。GGN 正半定只说明其构造形式，不等于精确 Hessian 没有负曲率，更不证明采用某种二阶近似后优化一定收敛或泛化更好。

## 进入正文前：Hessian 是二阶双线性型的坐标表示，不只是“再求一次偏导”

> [!info] 课程位置
> 前三章已经建立 $Df(x)$、梯度表示和一般导数的 JVP/VJP；本章对 $Df$ 再求导，得到接收两个方向的二阶双线性型。欧氏坐标中的 Hessian、方向曲率 $v^THv$ 与 HVP $Hv$ 是这个对象的三种不同接口。下一章会把一阶和二阶导数沿计算图复合。

> [!tip] 建议两遍阅读
> - **第一遍：** 掌握二阶对象类型、Hessian 坐标矩阵、对称条件、二阶 Taylor 模型、方向曲率与 HVP。
> - **第二遍：** 再读谱/凸性/条件数、驻点分类、Newton 稳定化、GGN/Fisher 分工、重参数化和大模型曲率审计。

> [!question] 本章的推导问题链
> 1. $Df(x)$ 的输出本身是线性泛函，对它再求导后为什么需要两个方向参数？
> 2. 选定基以后，双线性型怎样由矩阵 $H$ 表示为 $u^THv$？
> 3. $Hv$、$v^THv$ 与完整 $H$ 分别回答什么问题，形状为何不同？
> 4. 为什么 Hessian 半正定只给局部二阶信息，在退化方向上仍可能无法分类？

### LogSumExp 的曲率只看 logit 差异

对

$$
F(x)=\log(e^{x_1}+e^{x_2}),
$$

有 $\nabla F(x)=p(x)$，因此

$$
H_F(x)
=D p(x)
=\operatorname{diag}(p)-pp^T.
$$

在 $x=0$，

$$
\boxed{
H_F(0)
=\frac14
\begin{bmatrix}
1&-1\\
-1&1
\end{bmatrix}.}
$$

对任意 $u,v\in\mathbb R^2$，

$$
D^2F(0)[u,v]
=u^TH_F(0)v.
$$

两个正交特征方向为

$$
q_+=\frac1{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix},
\qquad
q_-=\frac1{\sqrt2}\begin{bmatrix}1\\-1\end{bmatrix},
$$

对应特征值

$$
\lambda_+=0,
\qquad
\lambda_-=\frac12.
$$

共同平移方向 $q_+$ 没有二阶曲率，因为 $F(x+c\mathbf1)=F(x)+c$；相对差异方向 $q_-$ 才改变 Softmax 分布并产生曲率。二阶 Taylor 模型为

$$
\boxed{
F(h)
=\log2+\frac{h_1+h_2}{2}
+\frac{(h_1-h_2)^2}{8}
+o(\|h\|_2^2).}
$$

取切片 $h=(t,0)$，立刻回到上一波的 Softplus 展开 $\log2+t/2+t^2/8+o(t^2)$。

> [!note] 符号账本
> | 符号 | 类型/形状 | 含义 |
> |---|---:|---|
> | $D^2f(x)$ | $X\times X\to\mathbb R$ | 连续二阶双线性型 |
> | $H_f(x)$ | $n\times n$ | 选定欧氏坐标后的 Hessian 矩阵 |
> | $H v$ | $n$ | 梯度映射沿 $v$ 的 JVP/HVP |
> | $u^THv$ | 标量 | 两方向的混合二阶响应 |
> | $v^THv$ | 标量 | 沿 $v$ 的方向曲率 |
> | $\lambda_{\min},\lambda_{\max}$ | 实标量 | 单位方向曲率的两端 |

## 阅读前检查：先把六个二阶对象放对位置

设 $X$ 为实赋范空间，$f:X\to\mathbb R$，并假设所需导数存在。

| 对象 | 类型 | 输入后得到什么 | 是否依赖坐标/内积 |
|---|---|---|---|
| $Df(x)$ | $X^*$ 中连续线性泛函 | $Df(x)[v]\in\mathbb R$ | 本体不依赖坐标；不需内积 |
| $D^2f(x)$ | 连续双线性型 $X\times X\to\mathbb R$ | $D^2f(x)[u,v]\in\mathbb R$ | 本体不依赖坐标；不需内积 |
| $H_f(x)$ | $n\times n$ 坐标矩阵 | $u^\top Hv\in\mathbb R$ | 依赖坐标；作为梯度 Jacobian 还依赖所用度量 |
| $Hv$ | 向量/协向量表示 | 与参数 $x$ 同形状 | 欧氏表示中是向量；抽象上先看作 $X^*$ |
| $v^\top Hv$ | 标量二次型 | 沿 $v$ 的二阶方向导数 | 坐标表达依赖基，标量本身不依赖 |
| $q_x(h)$ | $\tfrac12D^2f(x)[h,h]$ | 二阶局部增量 | 是二次型，不是线性映射 |

> [!warning] 三个最容易混淆的等式
>
> $$
> D^2f(x)[u,v]=u^\top H_f(x)v,
> $$
>
> $$
> D^2f(x)[v,v]=v^\top H_f(x)v,
> $$
>
> $$
> H_f(x)v=D(\nabla f)(x)[v]
> $$
>
> 分别是“混合双线性配对”“方向曲率标量”和“Hessian 对向量的作用”。它们的类型不同，不能互换。

## 一、从一阶导数再求一次导数

### 1.1 $Df$ 本身也是一个函数

若 $f:X\to\mathbb R$ 在某邻域可微，则

$$
Df:X\to X^*,
\qquad
x\mapsto Df(x)
$$

是一个把点映到连续线性泛函的函数。若这个函数在 $x$ 处再次 Fréchet 可微，则

$$
D(Df)(x):X\to X^*
$$

是线性算子。给它一个方向 $u\in X$，得到一个线性泛函 $D(Df)(x)[u]\in X^*$；这个泛函还能作用在 $v\in X$ 上。

因此定义

$$
D^2f(x)[u,v]
:=
\bigl(D(Df)(x)[u]\bigr)[v].
$$

> [!analysis] 二阶导数对象的公式七问
> | 问题 | 回答 |
> |---|---|
> | 二阶导数的本体是什么？ | $D^2f(x)$ 是接收两个输入方向并输出标量的连续双线性型，不以矩阵为起点。 |
> | 两个方向各做什么？ | 第一个方向描述微分 $Df$ 随基点怎样变化；得到的新线性泛函再作用于第二个方向。 |
> | Hessian 矩阵从哪里来？ | 选定 $\mathbb R^n$ 标准基后令 $H_{ij}=D^2f[e_i,e_j]$，于是 $D^2f[u,v]=u^THv$。 |
> | 对称性需要什么？ | $C^2$ 是常用充分条件；仅知道某点两种混合偏导都存在，不足以无条件交换顺序。 |
> | HVP 与方向曲率有何区别？ | $Hv$ 是向量/协向量表示，可供 Krylov 算法继续使用；$v^THv$ 是一个方向的曲率标量。 |
> | 怎样数值验收？ | 检查 HVP 的线性性、$u^THv=v^THu$、梯度中心差分收敛和二阶 Taylor 余项缩放。 |
> | AI 中怎样调用？ | 大模型优先使用 HVP、Lanczos/CG 与结构化 PSD 近似；单个最大特征值不能代表完整曲率或泛化。 |

它对 $u$ 线性，也对 $v$ 线性，所以是一个双线性映射。

> [!important] 二阶导数为何不是“一张矩阵”起步
> 第一阶导数把一个扰动送到一个标量；第二阶导数要接收两个扰动。矩阵只是有限维坐标中表示双线性型的工具。先记类型
>
> $$
> D^2f(x):X\times X\to\mathbb R,
> $$
>
> 比先记 $n\times n$ 数组更不容易在矩阵变量、函数空间和重参数化中犯错。

### 1.2 连续双线性意味着什么

双线性映射 $B:X\times X\to\mathbb R$ 连续，等价于存在 $C<\infty$ 使

$$
|B[u,v]|\le C\|u\|\|v\|.
$$

在有限维空间里，每个双线性映射自动连续；在无限维空间中不能省略这一条件。

定义双线性算子范数

$$
\|B\|
=
\sup_{\|u\|\le1,\,\|v\|\le1}|B[u,v]|.
$$

它测量二阶响应在单位方向对上的最大幅度。

### 1.3 向量值函数的二阶导数不是普通 Hessian

若 $F:X\to Y$，则

$$
D^2F(x):X\times X\to Y
$$

是 $Y$ 值双线性映射。在坐标中，若 $F:\mathbb R^n\to\mathbb R^m$，它通常需要三阶数组

$$
\frac{\partial^2F_a}{\partial x_i\partial x_j},
\qquad
a=1,\ldots,m.
$$

可以把它理解为每个输出分量 $F_a$ 各有一个 Hessian $H_{F_a}$。除非输出已被标量化，否则说“$F$ 的 Hessian 是 $n\times n$ 矩阵”是不完整的。

## 二、从双线性型到 Hessian 坐标矩阵

### 2.1 选定标准坐标

令 $f:\mathbb R^n\to\mathbb R$。在标准基 $e_1,\ldots,e_n$ 下定义

$$
H_{ij}(x)=D^2f(x)[e_i,e_j].
$$

若分量二阶偏导存在并与二阶 Fréchet 导数一致，则

$$
H_{ij}(x)
=
\frac{\partial}{\partial x_i}
\left(\frac{\partial f}{\partial x_j}\right)(x)
=
\frac{\partial^2f}{\partial x_i\partial x_j}(x).
$$

对

$$
u=\sum_i u_ie_i,
\qquad
v=\sum_jv_je_j,
$$

由双线性性

$$
\begin{aligned}
D^2f(x)[u,v]
&=D^2f(x)\left[\sum_i u_ie_i,\sum_jv_je_j\right]\\
&=\sum_{i,j}u_iv_jD^2f(x)[e_i,e_j]\\
&=u^\top H(x)v.
\end{aligned}
$$

### 2.2 Hessian 是梯度的 Jacobian，但这句话有条件

在固定的标准欧氏内积下，

$$
Df(x)[v]=\nabla f(x)^\top v.
$$

对 $x$ 沿 $u$ 求导：

$$
D^2f(x)[u,v]
=
\bigl(D(\nabla f)(x)[u]\bigr)^\top v.
$$

因此

$$
D(\nabla f)(x)=H(x)
$$

在本库的列向量约定下成立。

但是梯度是用内积把微分 $Df(x)\in X^*$ 表示成向量后的对象。若度量随位置变化，$D(\operatorname{grad}f)$ 会多出度量变化项；在流形上还需要协变导数。本章默认固定欧氏/Frobenius 度量，相关几何推广留给后续课程。

> [!success] 第一遍停靠线
> 若你能从 Softmax Jacobian 得到 LogSumExp Hessian，算出共同平移方向曲率为 $0$、差异方向曲率为 $1/2$，并区分 $H$、$Hv$ 与 $v^THv$ 的形状，就已掌握本章主干。后面的 GGN、Fisher、Newton 和重参数化属于第二遍。

### 2.3 一个完整的二维例子

令

$$
f(x,y)=x^3+xy^2-2x+4y.
$$

一阶导数为

$$
\nabla f(x,y)
=
\begin{bmatrix}
3x^2+y^2-2\\
2xy+4
\end{bmatrix}.
$$

再求一次导数：

$$
H(x,y)
=
\begin{bmatrix}
6x & 2y\\
2y & 2x
\end{bmatrix}.
$$

在 $(1,2)$ 处，

$$
H=
\begin{bmatrix}
6&4\\
4&2
\end{bmatrix}.
$$

给定 $v=(1,-1)^\top$，

$$
Hv=
\begin{bmatrix}2\\2\end{bmatrix},
\qquad
v^\top Hv=0.
$$

注意 $v^\top Hv=0$ 不意味着 $Hv=0$，也不意味着 $H=0$；这里只说明这个特定方向的二次项为零。

## 三、Hessian 为什么对称

### 3.1 坐标版本：混合偏导相等

若 $f$ 在 $x$ 的某邻域属于 $C^2$，则 Schwarz–Clairaut 定理给出

$$
\frac{\partial^2f}{\partial x_i\partial x_j}
=
\frac{\partial^2f}{\partial x_j\partial x_i},
$$

所以

$$
H(x)=H(x)^\top.
$$

$C^2$ 是清楚而常用的充分条件。仅仅知道两种混合偏导在某点分别存在，不能不加检查地断言它们相等。

### 3.2 坐标无关版本：二阶 Fréchet 导数的对称性

在标准的二阶 Fréchet 可微假设下，二阶导数满足

$$
D^2f(x)[u,v]=D^2f(x)[v,u].
$$

直觉来自小平行四边形的函数增量

$$
\Delta_{s,u}\Delta_{t,v}f(x)
=
f(x+su+tv)-f(x+su)-f(x+tv)+f(x).
$$

交换 $(s,u)$ 与 $(t,v)$ 不改变这个标量，而其主导项为

$$
st\,D^2f(x)[u,v].
$$

交换后主导项为 $st\,D^2f(x)[v,u]$，故二者相同。严格证明需要控制高阶余项，不能只把形式偏导符号交换当作证明。

### 3.3 数值 Hessian 为什么仍可能略不对称

即使数学上的 $H$ 对称，程序得到的 $\widehat H$ 仍可能满足

$$
\widehat H\ne\widehat H^\top
$$

，原因包括：

- 浮点舍入和不同运算路径；
- 有限差分步长不合适；
- mini-batch、dropout 或随机数不一致；
- 状态更新使两次函数调用不是同一函数；
- 自定义一阶规则不支持一致的高阶微分；
- 函数在折点处没有经典二阶导数。

诊断时可报告相对对称误差

$$
\frac{\|\widehat H-\widehat H^\top\|_F}
{\max(1,\|\widehat H\|_F)},
$$

但不要在未找到原因前简单用 $(\widehat H+\widehat H^\top)/2$ 掩盖实现错误。

## 四、二阶 Taylor 模型

### 4.1 一维限制把多元问题变成单变量问题

固定 $x,h$，定义

$$
\phi(t)=f(x+th).
$$

则

$$
\phi'(t)=Df(x+th)[h]
$$

以及

$$
\phi''(t)=D^2f(x+th)[h,h].
$$

若 $f\in C^2$ 于连接 $x$ 与 $x+h$ 的线段邻域，则一维 Taylor 积分公式给出

$$
f(x+h)
=
f(x)+Df(x)[h]
+
\int_0^1(1-t)D^2f(x+th)[h,h]\,dt.
$$

### 4.2 在基点冻结曲率

将积分中的二阶导数拆成基点值与变化量：

$$
\begin{aligned}
f(x+h)
&=f(x)+Df(x)[h]
+\frac12D^2f(x)[h,h]+R_2(x,h),\\
R_2(x,h)
&=\int_0^1(1-t)
\bigl(D^2f(x+th)-D^2f(x)\bigr)[h,h]\,dt.
\end{aligned}
$$

若 $D^2f$ 在 $x$ 连续，则

$$
R_2(x,h)=o(\|h\|^2).
$$

在欧氏坐标中得到熟悉的局部二次模型

$$
m_x(h)
=
f(x)+g^\top h+\frac12h^\top Hh,
\qquad
g=\nabla f(x).
$$

> [!warning] 系数 $\tfrac12$ 从哪里来
> 它不是 Hessian 定义的一部分，而来自
>
> $$
> \int_0^1(1-t)\,dt=\frac12.
> $$
>
> 因此 $D^2f[h,h]=h^\top Hh$，Taylor 二次项才是 $\tfrac12h^\top Hh$。

### 4.3 若 Hessian 是 Lipschitz 的

若沿相关邻域有

$$
\|H(y)-H(z)\|_2\le \rho\|y-z\|_2,
$$

则可由积分余项估计

$$
|R_2(x,h)|
\le
\frac{\rho}{6}\|h\|_2^3.
$$

这给二阶模型的可信半径一个定量尺度，也是三次正则化和信赖域分析的起点。

## 五、方向曲率、谱分解与几何

### 5.1 方向二阶导数

对单位方向 $v$，

$$
\left.\frac{d^2}{dt^2}f(x+tv)\right|_{t=0}
=
D^2f(x)[v,v]
=
v^\top H(x)v.
$$

它描述沿直线 $x+tv$ 的斜率如何变化：

- $v^\top Hv>0$：沿该方向局部向上弯；
- $v^\top Hv<0$：沿该方向局部向下弯；
- $v^\top Hv=0$：二次项消失，但三阶或更高阶仍可能决定形状。

### 5.2 二次型与极化恒等式

记

$$
q(v)=D^2f(x)[v,v].
$$

若 $D^2f(x)$ 对称，则混合项可由方向二次型恢复：

$$
D^2f(x)[u,v]
=
\frac14\bigl(q(u+v)-q(u-v)\bigr).
$$

验证：

$$
q(u+v)=q(u)+2D^2f[u,v]+q(v),
$$

$$
q(u-v)=q(u)-2D^2f[u,v]+q(v).
$$

两式相减即可。

### 5.3 特征方向是纯曲率方向

由实对称矩阵谱定理，

$$
H=Q\Lambda Q^\top,
\qquad
Q^\top Q=I,
$$

其中

$$
\Lambda=\operatorname{diag}(\lambda_1,\ldots,\lambda_n).
$$

写 $h=Qz$，则

$$
h^\top Hh
=
z^\top\Lambda z
=
\sum_i\lambda_i z_i^2.
$$

因此特征向量给出没有二次交叉项的局部坐标，特征值给出对应方向的二阶曲率。

Rayleigh 商

$$
R_H(v)=\frac{v^\top Hv}{v^\top v}
$$

满足

$$
\lambda_{\min}(H)
\le R_H(v)\le
\lambda_{\max}(H),
$$

且上下界分别在极端特征向量处达到。

### 5.4 “曲率”在本章中的确切含义

本章的曲率主要指损失沿参数空间直线的二阶变化 $v^\top Hv$。它不是自动等同于：

- 曲面在微分几何中的主曲率；
- 概率模型的 Fisher 信息几何；
- 优化轨迹本身的弯曲程度；
- 任意重参数化下不变的内禀量。

这些概念彼此相关，但度量、连接和参数化不同，不能只因都叫“曲率”就视为同一对象。

## 六、驻点的二阶判别

设 $x_*$ 为驻点：

$$
\nabla f(x_*)=0.
$$

局部模型化为

$$
f(x_*+h)-f(x_*)
=
\frac12h^\top H_*h+o(\|h\|^2).
$$

### 6.1 正定：严格局部极小

若

$$
H_*\succ0,
$$

则存在 $\mu>0$ 使

$$
h^\top H_*h\ge\mu\|h\|^2.
$$

高阶余项比 $\|h\|^2$ 小，因此充分小的非零 $h$ 满足

$$
f(x_*+h)>f(x_*),
$$

故 $x_*$ 是严格局部极小点。

### 6.2 负定：严格局部极大

若 $H_*\prec0$，同理 $x_*$ 是严格局部极大点。

### 6.3 不定：鞍点

若 $H_*$ 同时有正、负特征值，则分别沿对应特征向量存在上升和下降方向，故 $x_*$ 是鞍点。

### 6.4 半正定或半负定：二阶信息不够

若 $H_*\succeq0$ 但不正定，二阶判别不确定。例如在原点：

| 函数 | Hessian | 原点性质 |
|---|---:|---|
| $f(x)=x^4$ | $0$ | 严格局部极小 |
| $f(x)=-x^4$ | $0$ | 严格局部极大 |
| $f(x,y)=x^4-y^4$ | $0$ | 鞍点 |
| $f(x,y)=x^4$ | $0$ | 非孤立局部极小谷底 |

相同的零 Hessian 对应四种不同局部结构，必须查看更高阶项或其他论证。

> [!warning] 正定 Hessian 不是一般局部极小的必要条件
> $x^4$ 在原点严格极小，但二阶导数为零。正定 Hessian 是常用的充分条件；局部极小只推出在适当光滑条件下 Hessian 半正定。

## 七、Hessian、凸性与条件数

### 7.1 凸性二阶判据

设 $\Omega\subset\mathbb R^n$ 是开凸集，$f\in C^2(\Omega)$。则

$$
f\text{ 在 }\Omega\text{ 上凸}
\iff
H_f(x)\succeq0,
\quad\forall x\in\Omega.
$$

证明思路是限制到任意线段：对

$$
\phi(t)=f(x+t(y-x)),
$$

有

$$
\phi''(t)
=(y-x)^\top H_f(x+t(y-x))(y-x)\ge0.
$$

一维函数 $\phi$ 凸，于是 $f$ 在每条线段上凸。

域的凸性不可省略：即使每个连通分支上的 Hessian 都正定，跨越不连通域也不能应用标准凸性定义。

### 7.2 强凸性与光滑性

若对所有 $x\in\Omega$ 有

$$
\mu I\preceq H_f(x)\preceq LI,
\qquad
0<\mu\le L,
$$

则：

- 下界给 $\mu$-强凸性；
- 上界给梯度 $L$-Lipschitz；
- 对任意方向 $v$，

$$
\mu\|v\|^2
\le v^\top H_f(x)v
\le L\|v\|^2.
$$

二阶 Taylor 积分式进一步给

$$
\frac\mu2\|y-x\|^2
\le
f(y)-f(x)-\nabla f(x)^\top(y-x)
\le
\frac L2\|y-x\|^2.
$$

### 7.3 二次问题的条件数

考虑

$$
f(x)=\frac12x^\top Ax-b^\top x,
\qquad
A\succ0.
$$

其 Hessian 恒为 $A$。谱条件数

$$
\kappa_2(A)
=
\frac{\lambda_{\max}(A)}{\lambda_{\min}(A)}
$$

衡量最陡与最平方向的曲率比。

- $\kappa$ 接近 $1$：等高线接近球形；
- $\kappa\gg1$：狭长谷地，单一标量步长难同时适应各方向；
- 预条件的目标是改变坐标，使有效 Hessian 的谱更集中。

但在非凸问题中，$H$ 可能有负或零特征值，此时不能直接把 $\lambda_{\max}/\lambda_{\min}$ 当作正定条件数。

## 八、四类基本 Hessian 模板

### 8.1 二次函数

令

$$
f(x)=\frac12x^\top Ax+b^\top x+c.
$$

由于标量二次型只看 $A$ 的对称部分，

$$
x^\top Ax=x^\top\frac{A+A^\top}{2}x.
$$

所以

$$
\nabla f(x)
=
\frac{A+A^\top}{2}x+b,
$$

$$
H_f(x)=\frac{A+A^\top}{2}.
$$

若一开始假设 $A=A^\top$，才可简写为 $\nabla f=Ax+b$ 和 $H=A$。

### 8.2 线性最小二乘

令

$$
f(x)=\frac12\|Ax-b\|_2^2.
$$

写残差 $r(x)=Ax-b$，则

$$
Df(x)[v]
=
r(x)^\top Av,
$$

所以

$$
\nabla f(x)=A^\top(Ax-b),
$$

$$
H_f(x)=A^\top A\succeq0.
$$

HVP 可按

$$
Hv=A^\top(Av)
$$

计算，无需形成 $A^\top A$。

### 8.3 log-sum-exp 与 softmax 交叉熵

令

$$
\operatorname{LSE}(z)=\log\sum_{i=1}^K e^{z_i},
\qquad
p=\operatorname{softmax}(z).
$$

则

$$
\nabla_z\operatorname{LSE}(z)=p,
$$

$$
H_z
=
\operatorname{Diag}(p)-pp^\top.
$$

对任意 $v$，

$$
v^\top H_zv
=
\sum_i p_iv_i^2-\left(\sum_ip_iv_i\right)^2
=
\operatorname{Var}_{i\sim p}(v_i)
\ge0.
$$

因此 $H_z\succeq0$。同时

$$
H_z\mathbf1=0,
$$

因为给所有 logits 加同一常数不改变 softmax。对 one-hot 标签 $y$，交叉熵

$$
\ell(z,y)=\operatorname{LSE}(z)-y^\top z
$$

具有相同的 logits Hessian，因为线性项 $-y^\top z$ 没有二阶导数。

### 8.4 矩阵变量的最小二乘

令

$$
f(X)=\frac12\|AXB-C\|_F^2.
$$

记 $R=AXB-C$。在 Frobenius 内积下，

$$
Df(X)[\Delta]
=
\langle R,A\Delta B\rangle_F
=
\langle A^\top RB^\top,\Delta\rangle_F,
$$

所以

$$
\nabla_Xf=A^\top(AXB-C)B^\top.
$$

再对梯度沿 $\Delta$ 求导：

$$
\mathcal H_X[\Delta]
=
A^\top A\,\Delta\,BB^\top.
$$

这是 Hessian 算子，不必把它展平成巨大矩阵。若采用列优先 `vec`，则

$$
\operatorname{vec}(\mathcal H_X[\Delta])
=
\bigl(BB^\top\otimes A^\top A\bigr)
\operatorname{vec}(\Delta).
$$

## 九、HVP：大型模型真正可用的二阶接口

### 9.1 HVP 是梯度的 JVP

固定基点 $x$，定义梯度映射

$$
g(x)=\nabla f(x).
$$

则

$$
\operatorname{HVP}_{f,x}(v)
=
Dg(x)[v]
=
H_f(x)v.
$$

也可写成方向导数

$$
Hv
=
\left.\frac{d}{dt}\nabla f(x+tv)\right|_{t=0}.
$$

这说明上一章的 JVP 已经提供了理解 HVP 的全部类型基础：只需把被求导函数换成 $\nabla f$。

### 9.2 为什么不形成完整 Hessian

若参数量为 $n$：

- 完整 Hessian 有 $n^2$ 个元素；
- 仅以 float32 存储就约需 $4n^2$ 字节；
- $n=10^6$ 时需要约 $4\times10^{12}$ 字节，即约 4 TB；
- 但一个 HVP 只返回 $n$ 个数。

因此大型模型的二阶算法通常把 $H$ 当作“给定 $v$ 返回 $Hv$”的线性算子，配合共轭梯度、Lanczos、随机迹估计等矩阵自由方法。

### 9.3 forward-over-reverse

标量损失的梯度通常适合 reverse mode。然后对梯度函数做一次 forward-mode JVP：

```python
def hvp(f, x, v):
    return jvp(grad(f), (x,), (v,))[1]
```

概念顺序为

$$
f
\xrightarrow{\text{reverse}}
\nabla f
\xrightarrow{\text{forward along }v}
Hv.
$$

这种 forward-over-reverse 组合通常是 HVP 的自然实现，并避免形成完整 Hessian。

### 9.4 reverse-over-reverse

利用对称性，还可令

$$
s(x)=\nabla f(x)^\top v,
$$

然后

$$
\nabla s(x)=H(x)^\top v=H(x)v.
$$

对应伪代码：

```python
def hvp_revrev(f, x, v):
    return grad(lambda z: vdot(grad(f)(z), v))(x)
```

这里必须把 $v$ 视为常量。若 $v=v(x)$ 也参与求导，则乘积法则会产生额外项。

reverse-over-reverse 常有较好的算子覆盖，但可能需要构建更大的高阶反向图；forward-over-reverse 通常更节省相关内存。真实选择仍应根据框架算子覆盖和 profiling 决定。

### 9.5 Pearlmutter 的 $R$-operator 视角

定义方向微分算子

$$
\mathcal R_v\{g(x)\}
=
\left.\frac{d}{dt}g(x+tv)\right|_{t=0}.
$$

则

$$
\mathcal R_v\{x\}=v,
\qquad
\mathcal R_v\{\nabla f(x)\}=Hv.
$$

把 $\mathcal R_v$ 按微分规则传播过梯度程序，就能在不形成 $H$ 的情况下得到精确 HVP。这是现代 forward-over-reverse HVP 的经典来源之一。

### 9.6 完整 Hessian 仍何时有用

完整 Hessian 适合：

- 输入维数很小的教学和验证；
- 小型统计模型的不确定性分析；
- 需要全部元素的符号推导；
- 小矩阵上的直接分解与精确谱分析。

可用基向量 $e_j$ 逐列重建：

$$
H=[He_1\;He_2\;\cdots\;He_n].
$$

这需要约 $n$ 次 HVP 和 $O(n^2)$ 存储，不是大模型默认策略。

## 十、HVP 与二阶导数的验证协议

### 10.1 第零层：纯接口检查

在比较数值前先检查：

1. $f$ 是否真正返回标量；
2. $v$ 是否与被求导参数树同结构、同 dtype、同 device；
3. HVP 输出是否与参数同结构；
4. 随机性、dropout、batch normalization 状态是否冻结；
5. 是否对同一 batch、同一 reduction 和同一正则项求导；
6. 参数是否意外 `detach`、原地修改或经过不可微离散操作。

### 10.2 第一层：梯度中心差分

对足够光滑的 $f$，

$$
Hv
\approx
\frac{\nabla f(x+\varepsilon v)-\nabla f(x-\varepsilon v)}{2\varepsilon}.
$$

定义相对误差

$$
E_{\mathrm{fd}}(\varepsilon)
=
\frac{\left\|Hv-
\frac{\nabla f(x+\varepsilon v)-\nabla f(x-\varepsilon v)}{2\varepsilon}
\right\|}
{\max(1,\|Hv\|)}.
$$

扫描多个 $\varepsilon$ 通常比只试一个值可靠：步长太大会有截断误差，太小会被舍入与消减误差主导。

### 10.3 第二层：双线性对称性测试

随机取 $u,v$，检查

$$
u^\top(Hv)
\approx
v^\top(Hu).
$$

相对误差可写成

$$
E_{\mathrm{sym}}
=
\frac{|u^\top Hv-v^\top Hu|}
{\max(1,|u^\top Hv|,|v^\top Hu|)}.
$$

它不需要形成完整 Hessian，特别适合参数树。

### 10.4 第三层：Taylor 缩放测试

固定单位方向 $v$，令

$$
r_1(t)
=
f(x+tv)-f(x)-t\nabla f(x)^\top v,
$$

$$
r_2(t)
=
r_1(t)-\frac12t^2v^\top Hv.
$$

在充分光滑和未进入浮点噪声区间时：

$$
|r_1(t)|=O(t^2),
\qquad
|r_2(t)|=O(t^3).
$$

把 $t$ 减半，理想情况下 $|r_1|$ 约缩小 $4$ 倍，$|r_2|$ 约缩小 $8$ 倍。

### 10.5 测试通过不等于证明完整正确

有限个随机方向只能检查有限维投影；错误可能落在未采样子空间，或两个错误实现彼此一致。因此高可信验证需要组合：

- 小问题 full Hessian 对照；
- 多个随机方向；
- 差分步长扫描；
- 对称性测试；
- 已知解析模板；
- dtype/batch/状态消融。

## 十一、Newton 步、负曲率与稳定化

### 11.1 从局部二次模型求 Newton 步

最小化

$$
m_x(p)=f(x)+g^\top p+\frac12p^\top Hp
$$

的一阶条件为

$$
Hp=-g.
$$

若 $H\succ0$，唯一解

$$
p_N=-H^{-1}g
$$

是该二次模型的全局最小点。

实现时应解线性系统，不显式计算 $H^{-1}$。

### 11.2 Hessian 不定时 Newton 步未必下降

若 $H$ 不定：

- 二次模型可能向某方向无下界；
- $p_N$ 可能不是下降方向；
- 线性方程即使可解，也不代表该步可靠。

因此非凸优化常用：

- 阻尼 $H+\lambda I$；
- 修正 Cholesky 或特征值截断；
- 信赖域 $\|p\|\le\Delta$；
- 能检测负曲率的 truncated CG/Lanczos；
- 正半定的 Gauss–Newton、GGN 或 Fisher 型替代。

### 11.3 Newton–CG 为什么只需要 HVP

共轭梯度求解

$$
(H+\lambda I)p=-g
$$

只需反复调用

$$
v\mapsto Hv+\lambda v.
$$

因此可以在不存储 $H$ 的情况下近似 Newton 步。这种“外层非线性优化 + 内层矩阵自由线性求解”是大规模二阶方法的基本结构。

## 十二、精确 Hessian、Gauss–Newton 与 GGN

### 12.1 非线性最小二乘的精确分解

令

$$
L(\theta)=\frac12\|r(\theta)\|_2^2
=
\frac12\sum_{i=1}^m r_i(\theta)^2,
$$

残差 Jacobian 为 $J_r\in\mathbb R^{m\times n}$。梯度是

$$
\nabla L=J_r^\top r.
$$

再求导得到

$$
H_L
=
J_r^\top J_r
+
\sum_{i=1}^m r_iH_{r_i}.
$$

第一项总是正半定；第二项包含残差函数自身的二阶弯曲，可带来负曲率。

经典 Gauss–Newton 近似丢弃第二项：

$$
G_{\mathrm{GN}}=J_r^\top J_r\succeq0.
$$

当残差较小，或 $r(\theta)$ 对参数近似线性时，这一近似通常更合理；“总是近似良好”并不成立。

### 12.2 一般复合损失的精确二阶链式结构

令

$$
L(\theta)=\ell(z(\theta)),
\qquad
z:\mathbb R^n\to\mathbb R^m,
\quad
\ell:\mathbb R^m\to\mathbb R.
$$

记 $J_z$ 为模型输出对参数的 Jacobian，$g_z=\nabla_z\ell$，$H_\ell=\nabla_z^2\ell$。则

$$
H_L
=
J_z^\top H_\ell J_z
+
\sum_{i=1}^m(g_z)_iH_{z_i}.
$$

第一项来自“损失对输出的曲率经过模型 Jacobian 拉回”；第二项来自“模型输出本身对参数的弯曲”。完整证明属于[[多元链式法则与计算图]]，本章先掌握结构和类型。

### 12.3 generalized Gauss–Newton

定义

$$
G_{\mathrm{GGN}}
=
J_z^\top H_\ell J_z.
$$

若 $\ell$ 对 $z$ 是凸的，即 $H_\ell\succeq0$，则

$$
v^\top G_{\mathrm{GGN}}v
=(J_zv)^\top H_\ell(J_zv)\ge0,
$$

所以 $G_{\mathrm{GGN}}\succeq0$。

它可通过三步矩阵自由作用计算：

1. JVP：$a=J_zv$；
2. 输出空间曲率：$b=H_\ell a$；
3. VJP：$J_z^\top b$。

### 12.4 GGN 丢掉了什么

GGN 丢弃

$$
\sum_i(g_z)_iH_{z_i}.
$$

因此它：

- 通常更稳定，因为在凸输出损失下是 PSD；
- 不包含模型参数化产生的全部二阶项；
- 可能遗漏真实 Hessian 的负曲率；
- 依赖如何划分“模型输出 $z$”与“损失 $\ell$”的边界。

所以 GGN 是有结构的替代曲率，不是“把 Hessian 算得更快但结果完全相同”。

## 十三、Fisher、empirical Fisher 与 Hessian 不应混称

### 13.1 Fisher 信息

对条件概率模型 $p_\theta(y\mid x)$，score 为

$$
s_\theta(x,y)=\nabla_\theta\log p_\theta(y\mid x).
$$

模型 Fisher 通常定义为

$$
F(\theta)
=
\mathbb E_{x}
\mathbb E_{y\sim p_\theta(\cdot\mid x)}
[s_\theta s_\theta^\top].
$$

它天然 PSD。满足正则条件时，也可写成模型分布下负 log-likelihood Hessian 的期望。

### 13.2 empirical Fisher

训练样本上常见的

$$
F_{\mathrm{emp}}
=
\frac1N\sum_{i=1}^N
g_i g_i^\top,
\qquad
g_i=\nabla_\theta\ell_i,
$$

是观测标签对应的逐样本梯度外积。它同样 PSD，但一般不等于：

- 当前 mini-batch 损失的 Hessian；
- 模型 Fisher；
- GGN；
- Hessian 的对角。

在特定指数族输出、损失匹配和期望定义下，Fisher 与 GGN 可重合；这些条件必须写清楚。

### 13.3 一张防混淆表

| 对象 | 典型公式 | 一定 PSD？ | 包含模型二阶项？ |
|---|---|---:|---:|
| 精确 Hessian | $\nabla_\theta^2L$ | 否 | 是 |
| GN | $J_r^\top J_r$ | 是 | 否 |
| GGN | $J_z^\top H_\ell J_z$ | 当 $H_\ell\succeq0$ 时是 | 否 |
| 模型 Fisher | $\mathbb E_{y\sim p_\theta}[ss^\top]$ | 是 | 不是同一分解问题 |
| empirical Fisher | $N^{-1}\sum_i g_ig_i^\top$ | 是 | 否 |

## 十四、重参数化：Hessian 为什么不是普通张量

### 14.1 仿射坐标变换

令

$$
x=Sz+c,
$$

并定义 $\widetilde f(z)=f(Sz+c)$。则

$$
\nabla_z\widetilde f=S^\top\nabla_xf,
$$

$$
H_z=S^\top H_xS.
$$

这是合同变换，不是相似变换。若 $S$ 可逆，Sylvester 惯性定律保证正、负、零特征值的个数不变，但特征值数值通常改变。

### 14.2 非线性重参数化

更一般地，令 $x=\phi(z)$，$J_\phi=D\phi(z)$。则

$$
\nabla_z(f\circ\phi)
=
J_\phi^\top\nabla_xf,
$$

$$
H_z
=
J_\phi^\top H_xJ_\phi
+
\sum_{i=1}^n
\frac{\partial f}{\partial x_i}H_{\phi_i}.
$$

第二项说明普通坐标 Hessian 在非线性重参数化下不会只按双线性型变换。

### 14.3 驻点处的特殊简化

若 $\nabla_xf=0$，则额外项消失：

$$
H_z=J_\phi^\top H_xJ_\phi.
$$

若 $J_\phi$ 可逆，驻点的 Hessian 惯性保持，因此“局部极小/极大/鞍点的非退化类型”在光滑可逆重参数化下不变；但具体特征值和条件数仍会变化。

### 14.4 对 sharpness 叙事的警告

若只用 $\lambda_{\max}(H)$ 定义“尖锐度”，简单缩放参数就可能改变它。因此报告神经网络损失曲率时至少应说明：

- 参数化和归一化方式；
- loss reduction；
- 数据集或 batch；
- 权重衰减是否包含；
- 所用度量；
- 特征值是精确 Hessian 还是某种近似的。

## 十五、AI 中怎样使用二阶信息

### 15.1 曲率感知优化

- Newton/Newton–CG：用 $H^{-1}g$ 或近似线性求解校正尺度；
- Gauss–Newton/GGN：用 PSD 曲率避免真实 Hessian 的不定性；
- natural gradient：以 Fisher 度量参数分布的局部变化；
- K-FAC、Shampoo 等：进一步利用块、Kronecker 或矩阵结构近似曲率；
- 自适应优化器：用梯度二阶矩形成对角尺度，但不能无条件等同于 Hessian 对角。

### 15.2 谱信息而非整张矩阵

有 HVP 后可以用迭代方法估计：

- 最大/最小特征值与负曲率；
- 前若干特征向量；
- 谱密度近似；
- trace；
- 阻尼线性系统的逆作用。

例如 Hutchinson 估计利用满足 $\mathbb E[zz^\top]=I$ 的随机向量：

$$
\operatorname{tr}(H)
=
\mathbb E[z^\top Hz].
$$

有限样本平均是随机估计，不应把单次 probe 当作精确 trace。

### 15.3 influence 与逆 Hessian 作用

许多影响分析需要

$$
H^{-1}v,
$$

而不是 $H^{-1}$ 本身。可通过阻尼系统

$$
(H+\lambda I)s=v
$$

与 HVP 迭代求解。若 Hessian 不定、奇异或训练点并非局部极小，解释会变得敏感，阻尼不能省略说明。

### 15.4 Laplace 近似

在 MAP 点 $\theta_*$ 附近，把负对数后验二阶展开为

$$
-\log p(\theta\mid\mathcal D)
\approx
C+\frac12(\theta-\theta_*)^\top H(\theta-\theta_*).
$$

若 $H\succ0$，得到局部高斯近似

$$
p(\theta\mid\mathcal D)
\approx
\mathcal N(\theta_*,H^{-1}).
$$

大模型中通常需对角、块对角、低秩、Kronecker 或 GGN/Fisher 近似；不同近似对应不同的不确定性结论。

### 15.5 苏剑林文章中的 Hessian 近似视角

科学空间文章从局部关系

$$
g_\theta
\approx
H_{\theta_*}(\theta-\theta_*)
$$

出发，在参数围绕最优点近似各向同性波动、Hessian 近似对角、局部 Hessian 变化不大等假设下，把梯度平方的滑动平均与 Hessian 尺度联系起来。这有助于理解 Adam 类方法的对角预条件直觉。

但严谨结论应写成：

> 在一组统计、局部线性化和对角化假设下，梯度二阶矩可能提供 Hessian 幅度的代理。

不能缩写为“Adam 就是 Newton 法”或“$\sqrt{\mathbb E[g^2]}$ 总等于 Hessian 对角”。真实 Hessian 可有符号、非对角耦合和负曲率，而平方梯度代理非负且丢失这些信息。

## 十六、非光滑、随机性与实现边界

### 16.1 ReLU 折点

ReLU 在 $0$ 处没有经典一阶导数，更没有经典 Hessian。自动微分框架通常按约定选择一个分支导数；继续对该程序求高阶导得到的是“所选程序规则的导数”，不一定等于经典分析意义下存在的二阶导数。

另外，不能简单说“ReLU 网络 Hessian 处处为零”：

- 单个 ReLU 对其标量输入在非折点二阶导为零；
- 多层网络对跨层参数是多线性的，仍可能有混合二阶项；
- 非线性损失会通过 $J^\top H_\ell J$ 产生曲率；
- 折点处经典 Hessian 不存在。

### 16.2 mini-batch Hessian 不是总体 Hessian

若

$$
L(\theta)=\mathbb E_\xi[\ell(\theta;\xi)],
$$

在可交换微分与期望的条件下

$$
H_L(\theta)=\mathbb E_\xi[H_{\ell(\cdot;\xi)}(\theta)].
$$

一个 mini-batch Hessian 是随机估计，其极端特征值、负曲率和 trace 都会随 batch 波动。报告结果时必须记录 batch 采样、大小和随机种子。

### 16.3 loss reduction 改变尺度

若把逐样本损失从 `mean` 改为 `sum`，梯度和 Hessian 都会乘以 batch size。加入权重衰减

$$
\frac\lambda2\|\theta\|^2
$$

则 Hessian 增加 $\lambda I$。不同实现若 reduction 或正则定义不同，特征值不可直接比较。

### 16.4 混合精度与步长

二阶差分比一阶差分更容易受舍入影响。float16/bfloat16 下直接做微小扰动检查常不可靠。建议：

- 验证阶段使用 float64 或至少 float32；
- 扫描对数步长；
- 区分自动微分 HVP 与有限差分参照；
- 同时报告绝对、相对误差；
- 先在小型确定性子问题上验证。

## 十七、框架接口语义

### 17.1 JAX

典型接口关系：

```python
from jax import grad, hessian, jvp

g = grad(f)
value, hv = jvp(g, (x,), (v,))
H = hessian(f)(x)  # 仅在可承受 full Hessian 时
```

`jvp(grad(f), ...)` 返回 forward-over-reverse HVP。参数是 pytree 时，$v$ 必须有相同树结构；full Hessian 则形成相应的树乘树块结构。

### 17.2 PyTorch

`torch.func.hessian` 当前采用 forward-over-reverse 策略；HVP 可组合 `jvp(grad(f))`：

```python
from torch.func import grad, jvp

def hvp(f, primals, tangents):
    return jvp(grad(f), primals, tangents)[1]
```

若 forward AD 对某算子覆盖不足，可使用 reverse-over-reverse 备选。接口可用不意味着内存、编译和算子覆盖适合当前模型，仍需小规模正确性检查与 profiling。

### 17.3 `hvp` 与 `vhp` 名称陷阱

对光滑标量函数，数学上 $H=H^\top$，所以行向量 $v^\top H$ 转置后与 $Hv$ 相同。但框架 API 的输入输出容器、转置约定和高阶模式组合可能不同。不要只看名称，应检查：

- 函数是否标量输出；
- 返回的是 $Hv$ 还是 $v^\top H$ 的容器表示；
- 多输入时块顺序如何组织；
- 是否创建可继续求导的图；
- 是否支持当前算子和 pytree/tuple 结构。

## 十八、常见错误与最小反例

### 错误 1：Hessian 是函数的一阶 Jacobian

修正：标量函数的一阶 Jacobian 是 $1\times n$ 微分坐标；Hessian 是梯度映射的 Jacobian，是二阶对象。

### 错误 2：$v^\top Hv$ 和 $Hv$ 是同一个东西

修正：前者是标量方向曲率，后者是与参数同维的线性作用结果。

### 错误 3：驻点处 $H\succeq0$ 就一定严格极小

反例：$x^4-y^4$ 在原点 Hessian 为零，但原点是鞍点。

### 错误 4：严格凸函数处处 Hessian 正定

反例：$f(x)=x^4$ 严格凸，但 $f''(0)=0$。

### 错误 5：对任意矩阵 $A$，$\nabla(\tfrac12x^\top Ax)=Ax$

修正：应为 $\tfrac12(A+A^\top)x$。

### 错误 6：Gauss–Newton 就是精确 Hessian

修正：非线性最小二乘还含 $\sum_i r_iH_{r_i}$。

### 错误 7：Fisher、GGN 和 empirical Fisher 总相等

修正：只在特定概率模型、损失匹配和期望定义下存在等价关系。

### 错误 8：HVP 必须先形成 $H$

修正：$Hv=D(\nabla f)[v]$ 可直接由高阶 AD 计算。

### 错误 9：Hessian 特征值是重参数化不变量

修正：仿射变换给合同 $S^\top HS$；一般非线性变换还有梯度相关项。

### 错误 10：自动微分能让不存在的经典二阶导数存在

修正：框架只会按程序内定义的局部规则继续微分；折点处需单独解释。

## 十九、面向真实 AI 任务的二阶审计流程

### 第 1 步：定义标量目标

写清数据、batch、reduction、正则项与随机状态：

$$
L(\theta;\mathcal B,\text{state})\in\mathbb R.
$$

### 第 2 步：声明曲率对象

明确使用：

- 精确 Hessian；
- GN/GGN；
- Fisher；
- empirical Fisher；
- 对角、块、Kronecker 或低秩近似。

不要统一简称为“二阶矩阵”。

### 第 3 步：只暴露矩阵自由作用

优先实现

$$
v\mapsto Cv
$$

，其中 $C$ 是选定曲率算子。先通过已知模板和小问题 full matrix 对照。

### 第 4 步：完成三层验证

1. 形状、dtype、状态和 reduction；
2. 梯度差分与对称性；
3. Taylor 缩放或解析模板。

### 第 5 步：再做谱或线性求解

记录：

- 迭代算法；
- 初始随机向量和种子；
- 迭代次数与残差；
- 阻尼；
- batch；
- 收敛判据。

### 第 6 步：解释参数化依赖

报告模型参数化、归一化、尺度与度量。若比较不同模型 sharpness，先确认比较的量在尺度上有意义。

### 第 7 步：给出负结果和边界

若发现负曲率、奇异性、HVP 不稳定或近似与精确 Hessian 偏离，应保留这些信息，而不是只报告支持预期叙事的正特征值。

## 二十、掌握标准

### Level 1：识别

- 能写出 Hessian、HVP 和方向曲率的形状；
- 能区分 $Hv$ 与 $v^\top Hv$；
- 能对二维函数计算 Hessian。

### Level 2：推导

- 能从 $D(Df)$ 推导双线性二阶导数；
- 能证明 Taylor 二次项和方向曲率公式；
- 能推导最小二乘、softmax 和矩阵最小二乘 Hessian。

### Level 3：证明与反例

- 能说明 Hessian 对称的条件；
- 能证明凸性二阶判据和 Rayleigh 界；
- 能用半正定反例解释二阶判别不充分；
- 能推导非线性重参数化额外项。

### Level 4：计算与验证

- 能实现 forward-over-reverse HVP；
- 能用差分、对称性和 Taylor 缩放验证；
- 能以矩阵自由方式运行 CG/Lanczos 或随机 trace probe；
- 能复核小问题的 full Hessian。

### Level 5：AI 迁移

- 能区分精确 Hessian、GGN、Fisher 与 empirical Fisher；
- 能解释自适应梯度平方与 Hessian 近似之间的条件性联系；
- 能设计包含参数化、batch、reduction、阻尼和残差的曲率实验报告。

## 二十一、本章边界与后续路线

本章已经回答：

- 二阶导数为什么是双线性型；
- Hessian 如何编码方向曲率；
- 二次模型如何决定局部最优性与病态性；
- HVP 如何避免形成完整 Hessian；
- AI 中常见曲率近似彼此有何不同。

以下内容留给后续节点：

- 复合函数一阶/二阶链式法则的系统证明：[[多元链式法则与计算图]]；
- 矩阵变量布局、迹技巧和完整块导数：[[矩阵微分、迹技巧与布局约定]]；
- Newton、信赖域和二阶方法收敛：[[Newton 法、Gauss-Newton 与拟 Newton 法]]；
- Fisher 信息的统计推导：概率统计分卷；
- forward/reverse 混合模式、checkpoint 与高阶 AD 实现：[[自动微分：前向、反向与高阶模式]]。

## 二十二、来源与延伸阅读

- MIT 18.S096：二阶导数、双线性映射和 Hessian 的主教材来源；
- Boyd 与 Vandenberghe：凸性二阶判据、正定性与条件数背景；
- Pearlmutter：不形成 Hessian 的精确 HVP 经典算法；
- JAX Autodiff Cookbook：`grad`、JVP 与 HVP 组合及高阶差分检查；
- PyTorch `torch.func` 教程：dense Hessian、forward-over-reverse 和 reverse-over-reverse 接口；
- Martens：Fisher、GGN、empirical Fisher 和二阶优化的严格关系；
- 苏剑林《从 Hessian 近似看自适应学习率优化器》：对角自适应尺度的应用视角与待审计假设。

## 二十三、自测入口

- 分层习题：[[习题 - Hessian、二阶微分与曲率]]；
- 完整解答：[[解答 - Hessian、二阶微分与曲率]]；
- 前置复习：[[Taylor 展开与余项]]、[[Jacobian、JVP 与 VJP]]、[[二次型与正定矩阵]]；
- 下一节点：[[多元链式法则与计算图]]。
