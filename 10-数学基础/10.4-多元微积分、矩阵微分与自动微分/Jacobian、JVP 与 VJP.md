---
type: concept
status: draft
area: [math/calculus, math/linear-algebra, math/matrix-calculus, ai/automatic-differentiation]
aliases: [Jacobian JVP and VJP, Jacobian 矩阵, Jacobian-vector product, vector-Jacobian product, pushforward and pullback]
prerequisites: ["[[全微分与 Fréchet 导数]]", "[[梯度、方向导数与最陡方向]]", "[[线性泛函与对偶空间]]", "[[伴随算子]]", "[[基与坐标]]"]
related: ["[[Hessian、二阶微分与曲率]]", "[[多元链式法则与计算图]]", "[[矩阵微分、迹技巧与布局约定]]", "[[自动微分：前向、反向与高阶模式]]", "[[Kronecker 积、向量化与矩阵方程]]", "[[矩阵函数的 Fréchet 导数]]", "[[多元微积分、矩阵微分与自动微分 MOC]]"]
sources: ["MIT-18.S096-Derivatives-Linear-Operators", "MIT-18.S096-Jacobians-Matrix-Functions", "JAX-JVP-VJP-Official", "JAX-JVP-API", "JAX-VJP-API", "PyTorch-Func-Transforms", "Baydin-2018-AD-Survey", "Su-10958-JVP"]
exercises: ["[[习题 - Jacobian、JVP 与 VJP]]"]
solutions: ["[[解答 - Jacobian、JVP 与 VJP]]"]
created: 2026-08-17
updated: 2026-08-27
---

# Jacobian、JVP 与 VJP

> [!abstract] 本章主问题
> 若 $F:X\to Y$ 在 $x$ 处可微，唯一的一阶对象是线性算子 $DF(x):X\to Y$。选定输入/输出坐标后，它由 Jacobian 矩阵 $J_F(x)$ 表示；给定输入切向量 $v$，JVP 计算 $DF(x)[v]=Jv$；给定输出协向量 $u^*$，VJP 计算对偶回拉 $DF(x)'[u^*]=u^*\circ DF(x)$，在标准欧氏坐标中通常返回 $J^\top u$。完整 Jacobian 是一张坐标表，JVP/VJP 才是大规模可微程序真正需要的矩阵自由作用。

## 学习目标

完成本章后，应能：

1. 把 $DF(x)$、$J_F(x)$、$Jv$ 和 $J^\top u$ 放入正确空间；
2. 解释 Jacobian 是导数线性算子在输入/输出基下的矩阵表示；
3. 从基向量作用证明 Jacobian 第 $j$ 列等于 $DF(x)[e_j]$；
4. 从坐标函数证明 $(J_F)_{ij}=\partial F_i/\partial x_j$；
5. 区分 Jacobian 的数学布局和软件张量布局；
6. 把 JVP 解释为输入切向量的 pushforward；
7. 把 VJP 解释为输出协向量经对偶映射的 pullback；
8. 说明对偶回拉不需要内积，而伴随向量表示需要内积；
9. 在标准欧氏坐标中推导 VJP 返回 $J^\top u$；
10. 在加权内积下推导伴随矩阵 $M_X^{-1}J^\top M_Y$；
11. 使用伴随点积恒等式验证 JVP/VJP 实现；
12. 用 JVP 逐列、用 VJP 逐行重建小型 Jacobian；
13. 根据输入维数 $n$ 和输出维数 $m$ 选择 `jacfwd` 或 `jacrev` 的基本方向；
14. 解释为何标量损失对海量参数通常适合一次反向 VJP；
15. 说明成本规则只是量级指南，不替代实际 profiling；
16. 正确处理多输入、多输出、批维和树状参数结构；
17. 推导批量线性层对输入、权重和偏置的 JVP/VJP；
18. 解释广播为何在 VJP 中变成沿广播轴求和；
19. 对矩阵映射写算子形式、`vec` Jacobian 和结构化 VJP；
20. 用坐标变换公式审计 Jacobian 与 VJP 的变换规律；
21. 区分 full Jacobian、block Jacobian、per-example Jacobian 与 batch-summed gradient；
22. 使用有限差分、线性性和伴随点积三类测试定位导数实现错误；
23. 解释随机方向测试为什么不能证明整个 Jacobian 完全正确；
24. 将 JVP/VJP 迁移到反向传播、Jacobian 正则、NTK/Gauss–Newton 乘法与扩散速度场；
25. 明确本章与链式法则、Hessian、矩阵微分和自动微分系统章节的边界。

> [!question] 初学者读完必须能回答
> 1. $DF(x)$ 与 $J_F(x)$ 为什么不是完全同一个层次的对象？
> 2. 若 $F:\mathbb R^n\to\mathbb R^m$，$J$、$Jv$ 与 $J^\top u$ 的形状分别是什么？
> 3. JVP 为什么叫切向量的前推，VJP 为什么叫协向量的回拉？
> 4. 对偶回拉为什么不需要内积，而写成 $J^\top u$ 时为什么隐含坐标配对？
> 5. 伴随点积恒等式如何同时检查 JVP 与 VJP 实现？
> 6. 完整 Jacobian 为什么可按列用 JVP、按行用 VJP 构造？
> 7. 标量损失对海量参数为何通常适合反向模式？

先用下图回答一个视觉问题：**同一个导数算子，为什么既可以写成整张 Jacobian，也可以只通过 JVP 或 VJP 被使用？**

![[00-知识库管理/_assets/figures/jacobian-jvp-vjp/fig-jacobian-jvp-vjp-v2.svg|880]]

> [!figure] 图 10.4.6｜导数算子、前推/回拉接口与完整 Jacobian 的构造成本
> A 区分无坐标的导数算子、其方向作用和选基后的矩阵表；B 对照 JVP 的切向量前推与 VJP 的协向量回拉，并给出配对恒等式；C 用 $F:\mathbb R^8\to\mathbb R^3$ 示意按 8 个输入方向取列与按 3 个输出种子取行。来源：独立绘制；生成脚本：[[plot_jacobian_jvp_vjp.py]]；确定性结构示意，无随机种子。

**怎样读图。** A 先把 $DF(x)$ 看作一个“吃输入扰动、吐输出扰动”的线性规则，矩阵 $J$ 只是选基后的坐标表；B 沿上路读 $v\mapsto Jv$，沿下路反向读 $u^*\mapsto J^\top u$，两路由 $u^*(Jv)=(J^\top u)^*v$ 锁定；C 再比较完整物化 Jacobian 所需的基方向数。

**适用边界（图没有证明什么）。** 图中的“forward 约按 $n$ 次、reverse 约按 $m$ 次”是形成完整 Jacobian 的结构性计数，不是任意程序的精确运行时间。实际成本受计算图、稀疏性、批处理、编译融合和内存影响；一次随机点积测试也不能证明整套导数实现完全正确。

## 进入正文前：Jacobian 是坐标表，JVP 与 VJP 是真正使用它的两条通道

> [!info] 课程位置
> [[全微分与 Fréchet 导数]]给出无坐标的导数算子，[[梯度、方向导数与最陡方向]]处理标量输出的协向量表示。本章面对一般向量输出：选基后可把导数写成 Jacobian，但大型系统通常只计算 $Jv$ 或把输出协向量回拉为 $J^Tu$。下一章会把同一思想用于梯度映射，得到 HVP。

> [!tip] 建议两遍阅读
> - **第一遍：** 掌握 $DF$、$J$、JVP、VJP 的类型与形状，能手算一次前推、回拉和伴随点积测试。
> - **第二遍：** 再读完整 Jacobian 成本、多输入输出、batch/广播、矩阵变量、坐标变化、框架 API 与三层验证协议。

> [!question] 本章的推导问题链
> 1. 同一个线性算子选定输入/输出基后，为什么 Jacobian 的列是输入基方向的响应？
> 2. 为什么 JVP 与函数输出同形，而 VJP 与被求导输入同形？
> 3. 输出协向量为什么沿复合映射反向回拉，而不是像切向量一样向前推？
> 4. 在不形成完整 Jacobian 时，怎样用配对恒等式同时验收 JVP 与 VJP？

### Softmax 把一阶与二阶接口连起来

令

$$
p(x)=\nabla F(x)
=
\begin{bmatrix}
\dfrac{e^{x_1}}{e^{x_1}+e^{x_2}}\\[6pt]
\dfrac{e^{x_2}}{e^{x_1}+e^{x_2}}
\end{bmatrix}.
$$

在 $x=0$，

$$
p(0)=\begin{bmatrix}1/2\\1/2\end{bmatrix},
\qquad
\boxed{
J_p(0)
=\frac14
\begin{bmatrix}
1&-1\\
-1&1
\end{bmatrix}.}
$$

因此输入切向量 $v=(v_1,v_2)^T$ 的 JVP 是

$$
\boxed{
J_p(0)v
=\frac{v_1-v_2}{4}
\begin{bmatrix}1\\-1\end{bmatrix}.}
$$

输出种子 $u=(u_1,u_2)^T$ 的欧氏 VJP 是

$$
\boxed{
J_p(0)^Tu
=\frac{u_1-u_2}{4}
\begin{bmatrix}1\\-1\end{bmatrix}.}
$$

本例 Jacobian 恰好对称，所以两条公式外形相似；一般矩形 Jacobian 绝不能据此省略转置。还可直接读出

$$
J_p(0)\begin{bmatrix}1\\1\end{bmatrix}=0,
$$

因为同时平移两个 logits 不改变 Softmax 概率。

> [!note] 符号账本
> | 符号 | 形状 | 含义 |
> |---|---:|---|
> | $DF(x)$ | $X\to Y$ | 无坐标导数算子 |
> | $J_F(x)$ | $m\times n$ | 选定基后的导数矩阵，输出为行、输入为列 |
> | $v$ | $n$ | 输入切向量 |
> | $Jv$ | $m$ | JVP，输入扰动的前推 |
> | $u^*$ | $Y^*$ | 输出端线性测量/cotangent |
> | $J^Tu$ | $n$ | 标准欧氏坐标中的 VJP 数组表示 |
> | $p(x)$ | $2$ | 二分类 Softmax 向量函数 |

## 阅读前检查：先把六个对象放对位置

设

$$
F:X\to Y,
\qquad
x\in X,
$$

并假设 $F$ 在 $x$ 处 Fréchet 可微。

| 对象 | 类型 | 是否依赖坐标/内积 | 作用方向 |
|---|---|---|---|
| $DF(x)$ | $\mathcal L(X,Y)$ 中线性算子 | 不依赖坐标；可微性依赖范数拓扑 | $X\to Y$ |
| $J_F(x)$ | $m\times n$ 坐标矩阵 | 依赖输入/输出基和布局 | 坐标 $\mathbb R^n\to\mathbb R^m$ |
| $v$ | 输入切向量 | 向量坐标依赖基 | 位于 $X$ |
| $DF(x)[v]=Jv$ | 输出切向量/JVP | 坐标式依赖基 | 位于 $Y$ |
| $u^*$ | 输出协向量 | 协向量坐标依赖对偶基 | 位于 $Y^*$ |
| $DF(x)'[u^*]$ | 输入协向量/VJP | 对偶映射本身不需内积 | 位于 $X^*$ |

> [!warning] 最常见的形状错误
> 若 $F:\mathbb R^n\to\mathbb R^m$，则 $J\in\mathbb R^{m\times n}$，$Jv\in\mathbb R^m$，$J^\top u\in\mathbb R^n$。JVP 与函数输出同形状；VJP 与被求导输入同形状。二者通常都不与对方同形。

## 一、导数算子是本体，Jacobian 是坐标表示

### 1.1 从统一一阶模型开始

Fréchet 可微意味着存在唯一线性算子 $A=DF(x)$，使

$$
F(x+h)=F(x)+A[h]+r(h),
\qquad
\frac{\|r(h)\|_Y}{\|h\|_X}\to0.
$$

$A$ 能直接通过“输入一个扰动，输出一个一阶响应”描述，不需要先写成矩阵。

### 1.2 选择输入和输出基

现在令 $X,Y$ 分别为 $n,m$ 维实向量空间，选基

$$
\mathcal B_X=(e_1,\ldots,e_n),
\qquad
\mathcal B_Y=(f_1,\ldots,f_m).
$$

对每个输入基向量 $e_j$，$A[e_j]\in Y$ 可展开为

$$
A[e_j]=\sum_{i=1}^m J_{ij}f_i.
$$

把这些坐标列并排，得到

$$
J=[J_{ij}]\in\mathbb R^{m\times n}.
$$

任意 $h=\sum_jh_je_j$，由线性性

$$
\begin{aligned}
A[h]
&=\sum_jh_jA[e_j]\\
&=\sum_i\left(\sum_jJ_{ij}h_j\right)f_i.
\end{aligned}
$$

所以输出坐标满足

$$
[A[h]]_{\mathcal B_Y}
=J[h]_{\mathcal B_X}.
$$

> [!important] 列解释
> Jacobian 的第 $j$ 列是导数对第 $j$ 个输入基方向的响应坐标：
> $$
> J_{:j}=[DF(x)[e_j]]_{\mathcal B_Y}.
> $$

### 1.3 标准坐标中的偏导公式

若

$$
F=(F_1,\ldots,F_m):\mathbb R^n\to\mathbb R^m,
$$

并使用标准基，则

$$
DF(x)[e_j]
=\begin{bmatrix}
D_{e_j}F_1(x)\\
\vdots\\
D_{e_j}F_m(x)
\end{bmatrix}
=\begin{bmatrix}
\partial_jF_1(x)\\
\vdots\\
\partial_jF_m(x)
\end{bmatrix}.
$$

因此采用“输出坐标为行、输入坐标为列”的本库约定：

$$
\boxed{
J_F(x)=
\begin{bmatrix}
\dfrac{\partial F_1}{\partial x_1}&\cdots&\dfrac{\partial F_1}{\partial x_n}\\
\vdots&\ddots&\vdots\\
\dfrac{\partial F_m}{\partial x_1}&\cdots&\dfrac{\partial F_m}{\partial x_n}
\end{bmatrix}
\in\mathbb R^{m\times n}.}
$$

### 1.4 Jacobian 存在不是“偏导表存在”的同义词

若只知道所有偏导存在，可以把它们排成一个候选数组，但这不自动证明存在统一线性近似。只有在 $F$ 已 Fréchet 可微，或满足连续偏导等充分条件时，这张表才确实表示 $DF(x)$。

### 1.5 Jacobian 不是新的导数概念

同一个 $DF(x)$ 可以有多种表示：

- 直接给出算子规则 $h\mapsto A[h]$；
- 选基后给出矩阵 $J$；
- 只提供接口 $v\mapsto Jv$；
- 只提供对偶接口 $u\mapsto J^\top u$；
- 对矩阵变量给出结构化公式，不展平。

矩阵是表达方式，不是本体。

## 二、JVP：把输入切向量向前推

### 2.1 定义

> [!definition] Jacobian–vector product
> 给定 $v\in X$，JVP 是
> $$
> \operatorname{JVP}_{F,x}(v):=DF(x)[v]\in Y.
> $$
> 在标准坐标中为
> $$
> \boxed{\operatorname{JVP}_{F,x}(v)=J_F(x)v.}
> $$

它也叫 tangent pushforward：把输入空间的切向量推到输出空间。

### 2.2 JVP 就是可微函数的向量方向导数

由 Fréchet 可微，

$$
\begin{aligned}
DF(x)[v]
&=\lim_{t\to0}\frac{F(x+tv)-F(x)}t.
\end{aligned}
$$

JVP 不只给一个标量斜率，而给出输出空间中的完整一阶变化向量。

### 2.3 JVP 是关于切向量的线性映射

固定基点 $x$ 后，

$$
\operatorname{JVP}(\alpha v+\beta w)
=\alpha\operatorname{JVP}(v)+\beta\operatorname{JVP}(w).
$$

若实现不满足这一性质，常见原因包括：把有限差分误当精确 JVP、基点被意外改变、控制流选择依赖切向量、或自定义规则错误。

### 2.4 JVP 读取 Jacobian 的列组合

写

$$
v=\sum_{j=1}^nv_je_j.
$$

则

$$
Jv=\sum_{j=1}^nv_jJe_j.
$$

因此 JVP 是 Jacobian 各列按 $v_j$ 的线性组合。特别地，

$$
Je_j=J_{:j}.
$$

用全部输入基向量做 JVP，可以逐列重建完整 Jacobian。

### 2.5 不要混淆基点和方向

JVP 依赖两类输入：

$$
(x,v)\longmapsto(F(x),DF(x)[v]).
$$

- $x$ 是 primal/base point，决定在哪线性化；
- $v$ 是 tangent，决定沿哪个一阶方向作用；
- JVP 对 $v$ 线性，但一般不对 $x$ 线性。

## 三、VJP 的原始形式：对偶映射与协向量回拉

### 3.1 为什么反向对象必须是协向量

设

$$
A=DF(x):X\to Y.
$$

输出协向量 $u^*\in Y^*$ 是一个线性测量 $u^*:Y\to\mathbb R$。把它与 $A$ 复合，得到

$$
u^*\circ A:X\to\mathbb R,
$$

它正是输入空间上的协向量。

### 3.2 对偶映射

定义

$$
A':Y^*\to X^*,
\qquad
A'[u^*]=u^*\circ A.
$$

于是对任意 $v\in X$，

$$
\boxed{
(A'[u^*])[v]=u^*[A[v]].}
$$

> [!definition] Vector–Jacobian product
> VJP 是输出协向量沿导数算子的对偶回拉：
> $$
> \operatorname{VJP}_{F,x}(u^*)=DF(x)'[u^*]\in X^*.
> $$

> [!analysis] JVP 与 VJP 配对的公式七问
> | 问题 | 回答 |
> |---|---|
> | 导数本体是什么？ | $DF(x):X\to Y$；Jacobian 只是选基后的坐标矩阵，JVP/VJP 是对它的前向和对偶接口。 |
> | JVP 的输入输出是什么？ | 输入 $v\in X$，输出 $DF(x)[v]\in Y$；标准坐标中是 $Jv$。 |
> | VJP 的输入输出是什么？ | 输入输出协向量 $u^*\in Y^*$，返回 $DF(x)'[u^*]\in X^*$；不选择内积也能定义。 |
> | 为什么软件常写 $J^Tu$？ | 标准欧氏内积用 Riesz 表示协向量，回拉后的行坐标 $u^TJ$ 以列数组返回就是 $J^Tu$。 |
> | 怎样检查形状？ | 若 $J\in\mathbb R^{m\times n}$，则 $Jv\in\mathbb R^m$，$J^Tu\in\mathbb R^n$；前者同输出形，后者同输入形。 |
> | 怎样联合验收？ | 随机或基方向上检查 $u^T(Jv)=(J^Tu)^Tv$，再分别做有限差分与线性性测试。 |
> | AI 中怎样选择？ | 少输入方向/多输出适合 JVP；标量损失/海量参数通常用一次反向 VJP；形成完整 Jacobian 前先比较 $n,m$ 与稀疏结构。 |

它也叫 cotangent pullback。方向从输出对偶空间返回输入对偶空间。

### 3.3 对偶回拉不需要内积

$A'[u^*]=u^*\circ A$ 只用函数复合和线性结构，不需要长度、角度、正交或 Riesz 表示。因此，VJP 的最原始对象是协向量到协向量的映射。

这与上一章“梯度需要内积”完全一致：

- 微分/协向量的回拉是天然的；
- 把回拉后的协向量显示成输入空间中的梯度向量，需要选内积。

### 3.4 标准坐标中的行向量形式

令输出协向量的坐标行为 $u^\top$。则

$$
u^*[A[v]]
=u^\top Jv
=(u^\top J)v.
$$

因此 VJP 的协向量坐标行为

$$
\boxed{u^\top J.}
$$

软件通常用列数组保存结果，于是返回它的转置表示：

$$
\boxed{J^\top u.}
$$

“vector–Jacobian product”这个名字强调 $u^\top J$；API 返回数组常写成 $J^\top u$。二者表达同一回拉协向量。

> [!success] 第一遍停靠线
> 若你能写出 Softmax 在原点的 $2\times2$ Jacobian，对任意 $v,u$ 分别算出 JVP 与 VJP，并用配对恒等式核验二者，就已掌握本章主干。请同时说明本例因对称而外形相似，一般 Jacobian 并不对称甚至不方。

### 3.5 VJP 读取 Jacobian 的行组合

若 $u=e_i$，则

$$
e_i^\top J=J_{i:},
$$

即第 $i$ 个输出坐标对应的 Jacobian 行。用全部输出对偶基做 VJP，可以逐行重建完整 Jacobian。

## 四、伴随表示：何时 VJP 变成 $J^\top u$

### 4.1 选定内积后的伴随

若 $X,Y$ 是内积空间，$A:X\to Y$ 的伴随 $A^*:Y\to X$ 满足

$$
\langle A v,u\rangle_Y
=\langle v,A^*u\rangle_X.
$$

Riesz 表示把输出协向量 $u^*$ 表示成输出向量 $u$，再把回拉协向量 $A'[u^*]$ 表示成输入向量 $A^*u$。

因此：

- 对偶映射 $A'$ 是不依赖内积的 pullback；
- 伴随 $A^*$ 是选定两个内积后的向量表示；
- 标准欧氏坐标中，$A^*$ 的矩阵是 $J^\top$。

### 4.2 伴随点积恒等式

在实欧氏坐标中，

$$
\boxed{
u^\top(Jv)=(J^\top u)^\top v.}
$$

左边先做 JVP 再与输出种子配对；右边先做 VJP 再与输入方向配对。二者必须完全相等（浮点实现中近似相等）。

这条恒等式是验证一对黑箱 JVP/VJP 是否互为伴随的核心测试。

### 4.3 加权内积下不是普通转置

设输入、输出内积分别为

$$
\langle v,w\rangle_X=v^\top M_Xw,
\qquad
\langle y,u\rangle_Y=y^\top M_Yu,
$$

其中 $M_X,M_Y\succ0$。若伴随坐标矩阵为 $J^\dagger$，则要求

$$
(Jv)^\top M_Yu
=v^\top M_X(J^\dagger u)
$$

对所有 $v,u$ 成立。因此

$$
J^\top M_Y=M_XJ^\dagger,
$$

从而

$$
\boxed{J^\dagger=M_X^{-1}J^\top M_Y.}
$$

普通 $J^\top$ 只是在 $M_X=M_Y=I$ 时表示伴随。

### 4.4 软件“梯度数组”隐藏了什么

多数张量框架返回一个与输入数组同形的 VJP 数组，并默认使用元素级欧氏/Frobenius 配对解释它。若参数实际采用别的度量，则该数组首先是微分的坐标表示；要得到度量梯度，还需应用相应 Riesz 逆映射，例如 $M_X^{-1}$。

## 五、一个从头算到底的例子

令

$$
F(x,y)=
\begin{bmatrix}
xy\\
\sin x\\
x+y^2
\end{bmatrix}
:\mathbb R^2\to\mathbb R^3.
$$

### 5.1 Jacobian

$$
J_F(x,y)=
\begin{bmatrix}
y&x\\
\cos x&0\\
1&2y
\end{bmatrix}.
$$

在 $a=(0,1)$，

$$
J:=J_F(a)=
\begin{bmatrix}
1&0\\
1&0\\
1&2
\end{bmatrix}.
$$

### 5.2 JVP

取输入切向量

$$
v=\begin{bmatrix}2\\-1\end{bmatrix}.
$$

则

$$
Jv=
\begin{bmatrix}
2\\2\\0
\end{bmatrix}.
$$

这表示沿输入方向 $(2,-1)$，三个输出坐标的一阶变化分别为 $(2,2,0)$。

### 5.3 VJP

取输出种子

$$
u=\begin{bmatrix}1\\-2\\3\end{bmatrix}.
$$

标准欧氏 VJP 为

$$
J^\top u
=\begin{bmatrix}
1&1&1\\
0&0&2
\end{bmatrix}
\begin{bmatrix}1\\-2\\3\end{bmatrix}
=\begin{bmatrix}2\\6\end{bmatrix}.
$$

### 5.4 点积测试

左边：

$$
u^\top(Jv)
=(1,-2,3)
\begin{bmatrix}2\\2\\0\end{bmatrix}
=-2.
$$

右边：

$$
(J^\top u)^\top v
=(2,6)
\begin{bmatrix}2\\-1\end{bmatrix}
=-2.
$$

两边一致。

### 5.5 用基探针恢复 Jacobian

输入基 JVP：

$$
Je_1=(1,1,1)^\top,
\qquad
Je_2=(0,0,2)^\top,
$$

给出两列。输出基 VJP：

$$
J^\top e_1=(1,0)^\top,
\quad
J^\top e_2=(1,0)^\top,
\quad
J^\top e_3=(1,2)^\top,
$$

转置后给出三行。

## 六、标量输出：为什么一次 VJP 得到梯度

### 6.1 标量函数的 Jacobian

若

$$
f:\mathbb R^n\to\mathbb R,
$$

按输出行、输入列约定，Jacobian 是 $1\times n$ 行：

$$
J_f(x)=
\begin{bmatrix}
\partial_1f&\cdots&\partial_nf
\end{bmatrix}.
$$

微分为

$$
Df(x)[v]=J_f(x)v.
$$

### 6.2 输出种子 $1$

输出空间是 $\mathbb R$，其对偶空间也是一维。取协向量种子 $1$，VJP 返回

$$
J_f(x)^\top\cdot1
=\begin{bmatrix}
\partial_1f\\
\vdots\\
\partial_nf
\end{bmatrix}.
$$

在标准欧氏内积下，这正是梯度列向量：

$$
\boxed{\nabla f(x)=\operatorname{VJP}_{f,x}(1).}
$$

### 6.3 为什么神经网络反向传播适合 reverse mode

训练损失常是

$$
L:\mathbb R^n\to\mathbb R,
$$

其中 $n$ 可以是数百万或数十亿参数。形成完整 Jacobian 其实只需形成它唯一的一行；一次输出种子为 $1$ 的 VJP 就能回拉到全部输入参数坐标。

这说明 reverse mode 的优势来自 **输出维数小**，不是来自“梯度天然向后流”这样的比喻。

### 6.4 向量输出不能默认全设为一

若 $F:\mathbb R^n\to\mathbb R^m$ 且 $m>1$，用 $u=\mathbf1$ 做 VJP 得到

$$
J_F(x)^\top\mathbf1
=\nabla\left(\sum_{i=1}^mF_i(x)\right)
$$

（标准欧氏解释）。它只是输出分量求和的梯度，不是“向量函数的梯度”或完整 Jacobian。必须先说明要测量哪一个标量组合。

## 七、完整 Jacobian 的构造成本

### 7.1 按列构造：输入基 JVP

对 $F:\mathbb R^n\to\mathbb R^m$，

$$
J=
\begin{bmatrix}
Je_1&\cdots&Je_n
\end{bmatrix}.
$$

因此形成完整 Jacobian 需要 $n$ 个输入基方向的 JVP，或把这些方向批量化。

### 7.2 按行构造：输出基 VJP

同理，

$$
J=
\begin{bmatrix}
(J^\top e_1)^\top\\
\vdots\\
(J^\top e_m)^\top
\end{bmatrix}.
$$

因此可用 $m$ 个输出基种子的 VJP 逐行构造，或把这些种子批量化。

### 7.3 基本选择规则

| 形状 | 构造完整 $J$ 的基本倾向 | 原因 |
|---|---|---|
| $m\gg n$，高瘦 Jacobian | forward/JVP | 输入基方向更少，共 $n$ 列 |
| $n\gg m$，矮宽 Jacobian | reverse/VJP | 输出种子更少，共 $m$ 行 |
| $m=1$ | reverse/VJP | 一个种子得到整行/梯度 |
| $n=1$ | forward/JVP | 一个输入方向得到整列 |

PyTorch 将这一点概括为 `jacfwd` 与 `jacrev` 的经验选择；JAX 同样说明 JVP 可按列、VJP 可按行构造 Jacobian。

### 7.4 这不是精确运行时间定理

“按 $n$ 或 $m$ 计”只是方向数量层面的模型。真实成本还受以下因素影响：

- 原函数中每个算子的 JVP/VJP 实现；
- 编译器融合、向量化和设备利用率；
- 稀疏、卷积、共享参数等结构；
- 多个方向是循环还是批量执行；
- 反向时保存或重算中间量的策略；
- dtype、通信、内存带宽与编译开销。

因此应把维数规则当作算法选择起点，再用目标硬件上的 profiling 验证。

### 7.5 reverse mode 的内存代价

一次 VJP 的算术成本常与少量前向求值同量级，但反向传播通常需要保存或重建前向中间量。深计算图会产生显著激活内存；checkpoint/rematerialization 用额外重算换内存。完整系统机制留给[[自动微分：前向、反向与高阶模式]]。

### 7.6 为什么大规模问题通常不物化 $J$

完整 Jacobian 有 $mn$ 个坐标。若 $n,m$ 都大，存储本身就不可接受；而许多算法只需要：

$$
Jv,
\qquad
J^\top u,
\qquad
J^\top Jv,
\qquad
JJ^\top u.
$$

这些都可以把 JVP 与 VJP 组合为矩阵自由算子：

$$
J^\top Jv
=\operatorname{VJP}(\operatorname{JVP}(v)),
$$

这里的记号表示在同一固定 Jacobian 上先乘 $J$ 再乘 $J^\top$，并非对 JVP 结果再次对基点求导。

## 八、多个输入、多个输出与树状结构

### 8.1 直积空间观点

若

$$
F:X_1\times\cdots\times X_p
\to
Y_1\times\cdots\times Y_q,
$$

则输入扰动是元组

$$
v=(v_1,\ldots,v_p),
$$

JVP 输出与 $F$ 的可微输出部分同结构：

$$
DF(x)[v]
=(w_1,\ldots,w_q).
$$

VJP 接收输出协向量元组

$$
u^*=(u_1^*,\ldots,u_q^*)
$$

并返回输入协向量元组。

### 8.2 “同结构”不等于“同一数值形状”

JAX 的 `jvp` 要求 tangents 与 primals 具有相同树结构和数组形状；返回的 tangent outputs 与函数输出结构对应。PyTorch `torch.func.jvp` 也要求每个 primal 有同尺寸 tangent。VJP 则让输出 cotangent 与相应输出结构/形状匹配，并返回与被求导输入对应的结构。

树结构可以包含：

- 参数字典；
- 多层 tuple/list；
- 不同形状的权重、偏置与状态；
- 一个或多个张量输出。

不能把整个参数树未经约定地当成单一扁平向量。

### 8.3 静态参数与零切向量

若函数有多个参数，但只希望对其中一部分求 JVP，可以：

- 把其他参数闭包捕获为固定量；
- 或为其提供零切向量；
- 或用 API 的参数选择机制。

“未提供切向量”“提供数值零切向量”“声明不可微静态参数”在框架中可能有不同编译和类型语义，不能一概视为同一个操作。

### 8.4 辅助输出

训练函数常同时返回损失和日志/状态。`has_aux` 一类接口把辅助对象排除在被微分输出之外。若误把统计量、索引或缓存加入可微输出，VJP 的种子结构和内存都会改变。

## 九、批量线性层：一次推导看清全部形状

设

$$
W\in\mathbb R^{p\times q},
\quad
X\in\mathbb R^{q\times B},
\quad
b\in\mathbb R^p,
$$

批量线性层为

$$
Y=WX+b\mathbf1_B^\top
\in\mathbb R^{p\times B}.
$$

### 9.1 总 JVP

给定切向量

$$
(\dot W,\dot X,\dot b),
$$

精确一阶项为

$$
\boxed{
\dot Y
=\dot W X+W\dot X+\dot b\mathbf1_B^\top.}
$$

形状逐项为

$$
(p\times q)(q\times B),
\quad
(p\times q)(q\times B),
\quad
(p\times1)(1\times B).
$$

每项都属于 $\mathbb R^{p\times B}$。

### 9.2 给输出协向量种子

令

$$
U\in\mathbb R^{p\times B}
$$

表示输出 cotangent，使用 Frobenius 配对。需要把

$$
\langle U,\dot Y\rangle_F
$$

改写成分别关于 $\dot W,\dot X,\dot b$ 的配对。

### 9.3 权重 VJP

$$
\begin{aligned}
\langle U,\dot W X\rangle_F
&=\operatorname{tr}(U^\top\dot W X)\\
&=\operatorname{tr}(XU^\top\dot W)\\
&=\langle UX^\top,\dot W\rangle_F.
\end{aligned}
$$

所以

$$
\boxed{\bar W=UX^\top\in\mathbb R^{p\times q}.}
$$

### 9.4 输入 VJP

$$
\begin{aligned}
\langle U,W\dot X\rangle_F
&=\operatorname{tr}(U^\top W\dot X)\\
&=\langle W^\top U,\dot X\rangle_F.
\end{aligned}
$$

所以

$$
\boxed{\bar X=W^\top U\in\mathbb R^{q\times B}.}
$$

### 9.5 偏置 VJP 与广播求和

$$
\begin{aligned}
\langle U,\dot b\mathbf1_B^\top\rangle_F
&=\operatorname{tr}(U^\top\dot b\mathbf1_B^\top)\\
&=\mathbf1_B^\top U^\top\dot b\\
&=(U\mathbf1_B)^\top\dot b.
\end{aligned}
$$

所以

$$
\boxed{\bar b=U\mathbf1_B\in\mathbb R^p.}
$$

这就是广播操作在反向中沿广播轴求和的来源。

### 9.6 总伴随测试

正确实现必须满足

$$
\boxed{
\langle U,\dot Y\rangle_F
=\langle\bar W,\dot W\rangle_F
+\langle\bar X,\dot X\rangle_F
+\bar b^\top\dot b.}
$$

它同时检验权重转置、批维求和和各输入块的形状。

## 十、矩阵变量：算子公式通常优于巨型 Jacobian

### 10.1 双边线性映射

设固定

$$
A\in\mathbb R^{r\times m},
\qquad
B\in\mathbb R^{n\times s},
$$

定义

$$
F(X)=AXB,
\qquad
X\in\mathbb R^{m\times n}.
$$

因为 $F$ 本身线性，

$$
\boxed{DF(X)[H]=AHB.}
$$

这就是结构化 JVP，输出形状为 $r\times s$。

### 10.2 `vec` Jacobian

采用按列 `vec`，

$$
\operatorname{vec}(AHB)
=(B^\top\otimes A)\operatorname{vec}(H).
$$

所以显式 Jacobian 为

$$
J=B^\top\otimes A
\in\mathbb R^{rs\times mn}.
$$

这个矩阵适合理论分析，但实际计算通常没有必要形成。

### 10.3 结构化 VJP

给输出种子 $U\in\mathbb R^{r\times s}$，

$$
\begin{aligned}
\langle U,AHB\rangle_F
&=\operatorname{tr}(U^\top AHB)\\
&=\operatorname{tr}(BU^\top AH)\\
&=\langle A^\top UB^\top,H\rangle_F.
\end{aligned}
$$

因此

$$
\boxed{\operatorname{VJP}(U)=A^\top UB^\top.}
$$

它与乘 $(B^\top\otimes A)^\top=B\otimes A^\top$ 等价，但保留矩阵结构、更省存储，也更容易核对形状。

### 10.4 展平顺序必须成为契约

若改用按行展平，Kronecker Jacobian 的排列会改变。软件张量的 Jacobian 常把

$$
\text{output shape}+\text{input shape}
$$

拼接成高阶数组，而不是立即压成二维矩阵。任何 reshape、transpose、batch 维解释都必须记录，否则“数值元素都对”仍可能作用在错误坐标顺序上。

## 十一、坐标变换下的 Jacobian 与 VJP

### 11.1 输入和输出同时换坐标

设原坐标满足

$$
x=Sz,
\qquad
y=Tu,
$$

其中 $S,T$ 可逆。新坐标表示为

$$
\widetilde F(z)=T^{-1}F(Sz).
$$

输入切向量先由 $S$ 送到原坐标，导数作用后再由 $T^{-1}$ 转回输出新坐标，因此

$$
\boxed{J_{\widetilde F}=T^{-1}J_FS.}
$$

### 11.2 JVP 的坐标一致性

若 $v_x=Sv_z$，则

$$
J_{\widetilde F}v_z
=T^{-1}J_FSv_z
=T^{-1}J_Fv_x.
$$

它正是同一输出切向量在新坐标中的表示。

### 11.3 VJP 的协向量变换

输出协向量的行/列写法很容易混乱，更安全的做法是直接保持标量配对：

$$
u_y^\top\delta y
=u_u^\top\delta u,
\qquad
\delta y=T\delta u.
$$

于是列坐标满足

$$
u_u=T^\top u_y.
$$

回拉后也应满足

$$
\bar z=S^\top\bar x.
$$

直接检查：

$$
J_{\widetilde F}^\top u_u
=S^\top J_F^\top T^{-\top}u_u
=S^\top J_F^\top u_y.
$$

这正是输入协向量的坐标拉回规律。

> [!warning] 转置不是逆
> $J^\top$ 的作用是按欧氏配对把输出协向量回拉；它一般不把输出扰动“解回输入”。只有在额外可逆、方阵等条件下才可能讨论 $J^{-1}$，而 $J^\top\ne J^{-1}$ 通常成立。

## 十二、复合映射的前向与反向顺序预览

### 12.1 两层复合

设

$$
x\xmapsto{F}y\xmapsto{G}z.
$$

后续[[多元链式法则与计算图]]将严格证明

$$
D(G\circ F)(x)=DG(F(x))\circ DF(x).
$$

本章只读取它对 JVP/VJP 的接口后果。

### 12.2 JVP 按前向顺序推送

输入切向量 $v_x$ 先经过

$$
v_y=DF(x)[v_x],
$$

再经过

$$
v_z=DG(y)[v_y].
$$

在坐标中，

$$
v_z=J_GJ_Fv_x.
$$

### 12.3 VJP 按反向顺序回拉

输出协向量 $u_z^*$ 先由 $DG(y)'$ 回拉到 $Y^*$：

$$
u_y^*=DG(y)'[u_z^*],
$$

再由 $DF(x)'$ 回拉到 $X^*$：

$$
u_x^*=DF(x)'[u_y^*].
$$

欧氏坐标中，

$$
u_x=J_F^\top J_G^\top u_z
=(J_GJ_F)^\top u_z.
$$

这就是反向传播“反向”的代数原因：对偶映射把复合顺序反转。完整计算图、局部规则和分支汇合留到 CALC-09。

## 十三、JAX 与 PyTorch 接口语义

### 13.1 JAX `jvp`

官方接口可抽象为

```text
jax.jvp(fun, primals, tangents)
    -> (primals_out, tangents_out)
```

其中：

- `primals` 决定基点；
- `tangents` 与 `primals` 具有同样的树结构和数组形状；
- `tangents_out` 与可微函数输出结构对应；
- 返回的是函数值和 JVP，不是完整 Jacobian。

### 13.2 JAX `vjp`

可抽象为

```text
y, pullback = jax.vjp(fun, *primals)
input_cotangents = pullback(output_cotangent)
```

`pullback` 接收与输出结构匹配的 cotangent，返回与被求导输入结构匹配的 cotangent。JAX 官方明确把 `grad` 说明为 `vjp` 的标量输出特例。

### 13.3 PyTorch `torch.func`

当前 `torch.func` 提供：

- `jvp`：forward-mode Jacobian–vector product；
- `vjp`：reverse-mode vector–Jacobian product；
- `jacfwd`：以 forward mode 构造 Jacobian；
- `jacrev`：以 reverse mode 构造 Jacobian；
- `vmap`：把多个探针/样本方向向量化。

多输入时 primals 与 tangents 都是 tuple；对模块参数求 Jacobian 时，通常要把模块改写为参数显式输入的函数，或使用 `functional_call`。

### 13.4 API 名字不能替代类型检查

调用前仍应写清：

$$
F:\text{input tree}\to\text{output tree},
$$

并逐叶核对 tangent/cotangent 的形状、dtype 与可微语义。若只看到一个叫 `grad` 或 `backward` 的方法名，不能由名称推断它返回的是 full Jacobian、样本和、样本均值还是某个输出种子的 VJP。

### 13.5 自定义规则与不可微程序

框架可以为 primitive 或自定义函数注册 JVP/VJP 规则。规则存在表示框架会返回某个导数语义，不自动证明原始数学函数在该点经典可微。需要特别审计：

- ReLU、max、排序、索引等不可微/离散点；
- `stop_gradient`、detach 与原地修改；
- 数据依赖控制流；
- 随机数、状态和副作用；
- 自定义 backward 与 forward 公式是否互为伴随；
- 高阶变换是否还能穿过自定义规则。

## 十四、三层验证协议

### 14.1 第一层：类型、形状与线性

先检查：

1. JVP 输入 tangent 与被扰动输入同结构；
2. JVP 输出与函数输出同结构；
3. VJP seed 与函数输出同结构；
4. VJP 返回值与被求导输入同结构；
5. 固定基点后，JVP 对 tangent 近似满足线性；
6. 固定基点后，VJP 对 cotangent 近似满足线性。

浮点线性测试例如

$$
\operatorname{JVP}(\alpha v+\beta w)
\approx
\alpha\operatorname{JVP}(v)
+\beta\operatorname{JVP}(w).
$$

### 14.2 第二层：方向有限差分

对 JVP 候选 $q$，检查

$$
q\approx
\frac{F(x+\varepsilon v)-F(x-\varepsilon v)}{2\varepsilon}.
$$

应扫描多个 $\varepsilon$：过大时截断误差主导，过小时舍入消去主导。一次步长吻合不是充分证据。

### 14.3 第三层：伴随点积测试

随机取输入 tangent $v$ 和输出 cotangent $u$，计算

$$
s_{\rm fwd}=\langle u,\operatorname{JVP}(v)\rangle_Y,
$$

以及

$$
s_{\rm rev}=\langle\operatorname{VJP}(u),v\rangle_X.
$$

正确的互伴随实现应满足

$$
s_{\rm fwd}\approx s_{\rm rev}.
$$

它能高效发现转置、广播求和、复共轭、布局和参数遗漏错误。

### 14.4 小问题上的 full Jacobian 对照

当 $m,n$ 足够小：

1. 用解析公式或 `jacfwd/jacrev` 得到 $J$；
2. 检查黑箱 JVP 与 $Jv$；
3. 检查黑箱 VJP 与 $J^\top u$；
4. 用输入基/输出基重建列与行；
5. 比较不同构造的布局顺序。

### 14.5 随机测试的证据边界

有限个随机探针通过不能证明所有方向都正确。错误可能位于：

- 随机分布几乎不触及的稀疏坐标；
- 特定 batch、mask 或分支；
- 极端尺度和 dtype；
- 对称性导致的抵消子空间；
- 训练/推理模式差异。

随机测试是故障检测工具，不是一般可微性或全空间等式证明。

### 14.6 推荐误差指标

伴随测试可报告

$$
\eta_{\rm adj}
=\frac{|s_{\rm fwd}-s_{\rm rev}|}
{\max(1,|s_{\rm fwd}|,|s_{\rm rev}|)}.
$$

方向差分可报告

$$
\eta_{\rm fd}(\varepsilon)
=\frac{\left\|
\dfrac{F(x+\varepsilon v)-F(x-\varepsilon v)}{2\varepsilon}
-\operatorname{JVP}(v)
\right\|}
{\max(1,\|\operatorname{JVP}(v)\|)}.
$$

必须同时记录 $\varepsilon$、dtype、范数、随机种子和运行模式。

## 十五、AI 中真正调用 JVP/VJP 的场景

### 15.1 标量损失反向传播

神经网络训练最常见的是

$$
\theta\mapsto L(\theta)\in\mathbb R.
$$

一次以 $1$ 为输出种子的 VJP 回拉到所有参数块，得到欧氏/Frobenius 配对下的梯度数组。这是 reverse mode 在机器学习中占主导的核心形状原因。

### 15.2 多任务与向量损失

若输出是

$$
L(\theta)=(L_1,\ldots,L_m),
$$

种子 $u$ 得到

$$
J_L(\theta)^\top u
=\nabla_\theta\left(\sum_i u_iL_i\right).
$$

改变 $u$ 就改变标量化权重。若需要每个任务的独立梯度，应使用输出基种子逐行/批量构造，而不是默认全一向量。

### 15.3 per-example gradient

若批损失向量为

$$
\ell(\theta)=(\ell_1(\theta),\ldots,\ell_B(\theta)),
$$

普通总损失反向只返回

$$
J_\ell(\theta)^\top\mathbf1
=\sum_{b=1}^B\nabla\ell_b.
$$

每样本梯度需要 Jacobian 的各行，通常通过 `vmap` 与 `grad/vjp` 组合获得。样本和、样本均值与 per-example 数组必须明确区分。

### 15.4 Jacobian 范数正则与随机探针

若要惩罚

$$
\|J\|_F^2=\operatorname{tr}(J^\top J),
$$

可用随机向量 $z$ 满足 $\mathbb E[zz^\top]=I$，则

$$
\mathbb E\|Jz\|_2^2
=\operatorname{tr}(J^\top J)
=\|J\|_F^2.
$$

这允许用 JVP 估计 Jacobian Frobenius 范数，而不物化 $J$。但有限探针带随机方差，并且正则项的反向还涉及更高阶导数。

### 15.5 Gauss–Newton 与 NTK 型乘法

若模型输出对参数 Jacobian 为 $J_\theta$，很多大规模算法只需要

$$
J_\theta^\top J_\theta v
$$

或

$$
J_\theta J_\theta^\top u.
$$

前者可用 JVP 后接 VJP，后者可用 VJP 后接 JVP（都在固定线性化点解释）。它们分别作用于参数空间和输出/样本空间，是 Gauss–Newton、经验 NTK 与线性化模型计算的重要接口。

### 15.6 对抗输入与敏感方向

输入 JVP $J_xv$ 回答“给定扰动方向怎样改变全部输出”；输出 logit/loss 的 VJP 则回答“指定输出测量回拉到哪些输入坐标”。两者解决不同问题：前者推已知方向，后者由输出目标生成输入协向量。

### 15.7 扩散模型速度场

对联合输入速度场

$$
v_\theta(x_t,t),
$$

沿 $(\dot x_t,\dot t)$ 的变化是联合 JVP：

$$
Dv_\theta(x_t,t)[\dot x_t,\dot t].
$$

科学空间相关推导展示了 JVP 在扩散速度场中的实际入口。数学上仍应先写清被线性化的联合输入、切向量结构和输出形状。

### 15.8 隐式层与可微求解器预览

隐式层反向常需要求解包含 $J^\top$ 的线性系统，而不是显式构造 Jacobian。JVP/VJP 提供矩阵自由 matvec；方程从何而来、何时可逆以及求解误差怎样进入梯度，留给[[逆矩阵、线性求解与隐式微分]]。

## 十六、常见误区与逐条纠正

### 误区 1：“Jacobian 就是导数本身”

纠正：Jacobian 是选定输入/输出坐标后的矩阵表示；$DF(x)$ 是坐标无关的线性算子。

### 误区 2：“有偏导表就一定有 Jacobian”

纠正：可排出候选数组不等于已证明统一 Fréchet 微分。必须先满足可微条件。

### 误区 3：“JVP 的 vector 是输出向量”

纠正：JVP 的 tangent 属于输入空间，结果属于输出空间。

### 误区 4：“VJP 的种子属于输入空间”

纠正：VJP seed 是输出协向量，回拉结果才属于输入对偶空间。

### 误区 5：“VJP 总是普通转置乘向量”

纠正：对偶回拉天然存在；用向量表示时依赖内积。非欧氏伴随为 $M_X^{-1}J^\top M_Y$。

### 误区 6：“转置能把输出变化反解成输入变化”

纠正：$J^\top$ 是协向量回拉，不是 $J^{-1}$，也不是最小二乘伪逆。

### 误区 7：“向量输出 `.backward()` 默认得到完整 Jacobian”

纠正：必须提供输出 cotangent seed；返回的是该 seed 对应的行组合，而非完整 Jacobian。

### 误区 8：“全一 seed 给向量函数梯度”

纠正：它给输出分量和的梯度，即 $J^\top\mathbf1$。

### 误区 9：“forward mode 总比 reverse mode 快”

纠正：形成完整 Jacobian 时主要比较输入与输出方向数；单次作用、程序结构、批量化、设备和内存会改变实际结果。

### 误区 10：“JVP/VJP 不形成 Jacobian，所以没有 Jacobian 数学对象”

纠正：它们正是同一线性算子的正向/对偶作用；不物化矩阵不等于不存在导数。

### 误区 11：“广播的反向仍是广播”

纠正：广播的 JVP 会广播切向量，VJP 必须沿被复制轴求和，回到原输入形状。

### 误区 12：“batch 维就是函数输出维”

纠正：batch 可以是独立样本轴、被归约轴或模型真正输出轴。不同语义决定 Jacobian 是块对角、求和还是耦合结构。

### 误区 13：“伴随点积测试通过就证明经典导数存在”

纠正：它只验证两个实现的线性作用互相一致；两者可能共同实现了某个框架约定，而原函数在该点不可微。

### 误区 14：“随机方向测试通过等于整张 Jacobian 正确”

纠正：有限探针可能漏掉特定子空间、分支、mask 和极端尺度。

### 误区 15：“自定义 backward 对一次训练有效，就能任意高阶组合”

纠正：高阶变换还要求自定义规则本身可微、与 JVP/VJP 约定兼容并正确处理保存值与副作用。

## 十七、解题与实现工作流

### 步骤 1：写清函数签名

$$
F:X\to Y,
$$

列出每个输入/输出叶子的形状、dtype、批维和可微性。

### 步骤 2：先写导数算子作用

从精确增量或已知规则写

$$
DF(x)[h].
$$

优先保持矩阵/张量结构，不急于 `vec`。

### 步骤 3：按任务选择表示

- 需要小型完整表：构造 Jacobian；
- 已知输入方向：JVP；
- 已知输出测量/损失：VJP；
- 需要 $J^\top J$ 或 $JJ^\top$ 作用：组合黑箱 JVP/VJP；
- 需要谱、秩或逐元素审计：可能必须物化小型 Jacobian。

### 步骤 4：核对方向与配对

画出

$$
X\xrightarrow{DF}Y,
\qquad
Y^*\xrightarrow{DF'}X^*.
$$

不要只凭 API 名称猜形状。

### 步骤 5：核对布局和广播

记录输出轴、输入轴、batch 轴、展平顺序、参数组和广播归约轴。

### 步骤 6：执行三层验证

先形状/线性，再有限差分 JVP，最后伴随点积；小问题上与显式 $J$ 对照。

### 步骤 7：报告证据边界

区分：

- 数学推导；
- 框架当前 API 语义；
- 浮点测试证据；
- 性能 profiling；
- 对训练收敛或泛化的进一步猜想。

## 十八、知识结构表

| 层次 | 核心对象 | 公式 | 常见错误 |
|---|---|---|---|
| 一阶本体 | $DF(x):X\to Y$ | $F(x+h)=F(x)+DF(x)[h]+o(\|h\|)$ | 把偏导表当可微性证明 |
| 坐标表示 | $J\in\mathbb R^{m\times n}$ | $[DF(x)[h]]=J[h]$ | 行列约定颠倒 |
| 前向作用 | JVP | $v\mapsto Jv$ | tangent 形状错误 |
| 对偶回拉 | VJP | $u^*\mapsto u^*\circ DF$ | 把 cotangent 当普通输出扰动 |
| 欧氏伴随 | $J^\top u$ | $u^\top Jv=(J^\top u)^\top v$ | 把转置当逆 |
| 完整 Jacobian | 列/行探针 | $n$ 个 JVP 或 $m$ 个 VJP | 忽略批量化与真实成本 |
| 多输入 | block derivative | $DF[h_1,\ldots,h_p]$ | 漏参数块或广播和 |
| 矩阵变量 | 结构化算子 | $H\mapsto AHB$ | 无必要地形成 Kronecker 巨矩阵 |
| AI 反向 | 标量 seed $1$ | $\nabla L=J_L^\top1$ | 误称 full Jacobian |
| 验证 | 差分 + adjoint test | $\langle u,Jv\rangle=\langle J^\top u,v\rangle$ | 用有限探针冒充证明 |

## 十九、最低掌握标准

### Level 1：会读形状

- 能为 $F:\mathbb R^n\to\mathbb R^m$ 写出 $J,Jv,J^\top u$ 的形状；
- 能从偏导表构造小型 Jacobian；
- 能用基探针逐列/逐行恢复矩阵。

### Level 2：会推导

- 能从 Fréchet 导数证明 Jacobian 的列解释；
- 能从对偶映射定义推导 VJP；
- 能推导加权伴随；
- 能推导线性层和 $AXB$ 的 JVP/VJP。

### Level 3：会选择与验证

- 能依据 $m,n$ 和实际任务选择 full J/JVP/VJP；
- 能解释 reverse mode 的内存代价；
- 能完成方向差分、线性性和伴随点积测试；
- 能识别 batch、广播、布局和 seed 错误。

### Level 4：会迁移

- 能设计 per-example gradient 与多任务 seed；
- 能构造 $J^\top Jv$、$JJ^\top u$ 等矩阵自由算子；
- 能审计扩散 JVP、Jacobian 正则、NTK/Gauss–Newton 接口；
- 能区分局部导数接口、自动微分实现和训练层面结论。

## 二十、本章边界与后续接口

本章建立一阶导数的三种表示/作用接口，但不完整展开以下主题：

- 二阶导数、HVP 与曲率：[[Hessian、二阶微分与曲率]]；
- 链式法则证明、计算图分支与反向累积：[[多元链式法则与计算图]]；
- 矩阵微分布局、迹技巧和复杂矩阵表达式：[[矩阵微分、迹技巧与布局约定]]；
- 前向/反向 AD 的程序变换、tape、checkpoint 与高阶组合：[[自动微分：前向、反向与高阶模式]]；
- 隐式层中的线性系统与伴随求解：[[逆矩阵、线性求解与隐式微分]]；
- 谱分解和矩阵函数自定义 VJP：[[矩阵函数的 Fréchet 导数]]及后续谱导数节点；
- 复数非全纯函数的 Wirtinger/实 Jacobian 语义：复分析与自动微分扩展专题。

> [!summary] 本章压缩
> 1. $DF(x)$ 是导数本体，$J$ 是选基后的矩阵表示。
> 2. JVP 计算 $DF(x)[v]=Jv$，把输入切向量推到输出。
> 3. VJP 计算 $DF(x)'[u^*]$，把输出协向量回拉到输入。
> 4. 标准欧氏坐标用 $J^\top u$ 表示 VJP；一般度量的伴随不是普通转置。
> 5. full Jacobian 可由 $n$ 个列 JVP 或 $m$ 个行 VJP 构造。
> 6. 标量输出只需一个 VJP seed $1$，这解释了反向传播对海量参数的适用性。
> 7. 矩阵、批量和树状参数应保持结构，通常不应物化巨型 Jacobian。
> 8. 方向差分与伴随点积测试互补，但有限测试不是一般证明。

## 二十一、练习、复现与自检

- 分层习题：[[习题 - Jacobian、JVP 与 VJP]]；
- 完整解答：[[解答 - Jacobian、JVP 与 VJP]]；
- 配图脚本：[[plot_jacobian_jvp_vjp.py]]；
- 建议先闭卷完成 A/B 层的形状与手算，再在 C 层重建对偶/伴随与成本理论，最后用 D/E 层审计真实可微程序。

## 来源说明

- MIT 18.S096 *Matrix Calculus for Machine Learning and Beyond*：导数线性算子、Jacobian、矩阵函数 Jacobian、adjoint differentiation 与 forward/reverse AD 的课程主线；
- JAX 官方 *Forward- and reverse-mode autodiff*、`jax.jvp` 与 `jax.vjp`：tangent/cotangent、pushforward/pullback、逐列/逐行构造及当前 API 语义；
- PyTorch `torch.func` 官方文档与 Jacobian/Hessian 教程：`jvp/vjp/jacfwd/jacrev/vmap` 的当前接口、结构和经验选择；
- Baydin、Pearlmutter、Radul、Siskind（JMLR 2018）：自动微分与机器学习、forward/reverse accumulation 的系统综述；
- 科学空间扩散速度场文章：联合输入方向 JVP 的 AI 问题入口，不替代一般可微性、链式法则或 AD 实现理论。

> [!warning] 状态说明
> 本节点已经建立正文、图、训练题和解答，但在完成真实作答、代码复现、错题回炉与间隔复查前保持 `draft`。
