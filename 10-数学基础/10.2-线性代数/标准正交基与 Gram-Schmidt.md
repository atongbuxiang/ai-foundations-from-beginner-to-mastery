---
type: concept
status: draft
area: [math/linear-algebra]
aliases: [Gram-Schmidt 正交化, 施密特正交化, Orthonormal Basis]
prerequisites: ["[[向量空间]]", "[[子空间、张成与线性无关]]", "[[内积空间]]"]
related: ["[[正交投影]]", "[[QR 分解]]", "[[最小二乘]]", "[[数值稳定性|Gram-Schmidt 的数值稳定性]]", "[[实验 - Gram-Schmidt 与 QR 的正交性误差]]", "[[线性代数 MOC]]"]
sources: ["Axler-LADR4e-6B", "MIT-18.06-L17"]
exercises: ["[[习题 - 标准正交基与 Gram-Schmidt]]"]
solutions: ["[[解答 - 标准正交基与 Gram-Schmidt]]"]
created: 2026-08-14
updated: 2026-08-27
---

# 标准正交基与 Gram-Schmidt

> [!abstract] 本章主问题
> 怎样在不改变张成空间的前提下，把一组倾斜、耦合的基改造成标准正交基？Gram–Schmidt 逐个减去新向量沿旧方向的投影，再把剩余的新方向归一化。结果保留每一步的 span，却让坐标可由内积直接读出，并自然产生 $A=QR$、正交投影和最小二乘算法。

> [!info] 学习目标
> 学完本章后，应能区分正交组、标准正交组与标准正交基；从一维最近点推导投影系数；手算 Gram–Schmidt 并证明逐步保持张成；说明线性无关为何保证残差非零；从正交化读出 QR 分解；比较 CGS、MGS、重正交化与 Householder QR 的数值边界。

> [!question] 初学者读完必须能回答
> 1. 正交、单位长度与“构成整个空间的基”分别增加了什么条件？
> 2. 为什么 $\langle a,q\rangle q$ 是 $a$ 沿单位方向 $q$ 的分量？
> 3. 第 $j$ 步为什么要减去所有已有 $q_i$ 方向，而不只减最近一个？
> 4. 每一步怎样证明新旧向量组张成同一子空间？
> 5. 残差为零与原向量组线性相关为什么等价？
> 6. Gram–Schmidt 中的系数怎样组成上三角矩阵 $R$？
> 7. 精确算术下正确的 CGS 为什么在浮点数中仍可能丢失正交性？

![[00-知识库管理/_assets/figures/orthonormal-bases/fig-gram-schmidt-residual-qr-v2.svg|880]]

> [!figure] 图 1　投影消除、垂直残差与 QR 结构
> 左侧把 $a_2$ 分解成沿 $q_1$ 的投影与垂直残差 $r_2$；右侧依次展示归一化、消除旧分量、再次归一化；底栏连接逐步 span 不变、$Q^*Q=I$ 与 $A=QR$。**来源：**依据 Gram–Schmidt 构造与 QR 关系独立绘制。

**怎样读图。** 先把 $a_1$ 归一化为 $q_1$。再从 $a_2$ 中减去沿 $q_1$ 的投影，得到垂直于 $q_1$ 的残差；这个残差仍携带 $a_2$ 增加的新方向，归一化后成为 $q_2$。一般第 $j$ 步对所有旧 $q_i$ 重复同一消除，由此得到上三角系数结构。

**适用边界（图没有证明什么）。** 图展示精确算术中的几何构造，没有表达舍入误差的累计。CGS、MGS 与 Householder QR 在精确算术中可产生同一类分解，但浮点正交性和实现成本不同；“图上垂直”不能替代 $\|I-Q^*Q\|$ 的数值验收。

## 进入正文前：把倾斜坐标改造成可以直接测量的坐标

> [!info] 承接—中心—去路
> - **承接：** [[内积空间]]已经提供正交、投影系数和勾股定理；[[子空间、张成与线性无关]]说明输入向量组应保留同一个 span 且不能丢失新方向。
> - **中心：** Gram–Schmidt 逐列把“旧方向分量”从新向量中扣除，留下正交残差，再归一化；它同时保持逐步 span 并产生标准正交坐标。
> - **去路：** [[QR 分解]]会把扣除系数收集成上三角 $R$，[[正交投影]]会用 $QQ^*$ 直接计算最近点，[[最小二乘]]会用正交残差判定最优性。

### 两遍阅读路线

第一次手算两列例子，逐步回答“投影减了什么、残差为何正交、span 为何不变、何时会除以零”。第二次再读一般递推、QR 系数结构和 CGS/MGS/Householder 的浮点差异。

全章主线是：

$$
a_j
\to \text{减去旧方向投影}
\to v_j\perp\operatorname{span}(q_1,\ldots,q_{j-1})
\to q_j=\frac{v_j}{\|v_j\|}
\to A=QR.
$$

### 本章的问题链

1. 为什么标准正交组比一般基更容易读取坐标与长度？
2. $\langle a,q\rangle q$ 为什么恰好是沿单位方向 $q$ 的分量？
3. 为什么第 $j$ 步必须减去所有旧方向，而不是只减最后一个？
4. 新残差与旧 $q_i$ 为什么严格正交？
5. $v_j=0$ 为什么恰好暴露 $a_j$ 没有增加新方向？
6. 每一步的新旧向量组为何张成同一前缀子空间？
7. 系数为什么自然排成上三角矩阵，浮点实现又为何可能破坏正交？

### 贯穿例：把 $A$ 的两列正交化

对

$$
a_1=(1,1,0)^\top,
\qquad
a_2=(1,0,1)^\top,
$$

第一步得到

$$
q_1=\frac1{\sqrt2}(1,1,0)^\top.
$$

第二步先减去旧方向：

$$
v_2
=a_2-\langle a_2,q_1\rangle q_1
=\left(\frac12,-\frac12,1\right)^\top,
$$

其范数为 $\|v_2\|=\sqrt{3/2}$，故

$$
q_2=\frac1{\sqrt6}(1,-1,2)^\top.
$$

检查：$q_1^Tq_2=0$、$\|q_1\|=\|q_2\|=1$，并且 $\operatorname{span}(q_1,q_2)=\operatorname{span}(a_1,a_2)$。后续所有投影和最小二乘计算都复用这组 $Q=[q_1\ q_2]$。

### 最小过程账本

| 量 | 作用 | 失败时意味着什么 |
|---|---|---|
| $r_{ij}=\langle a_j,q_i\rangle$ | 第 $j$ 列沿旧方向 $q_i$ 的坐标 | 内积/共轭约定写反会破坏消除 |
| $v_j=a_j-\sum_{i<j}r_{ij}q_i$ | 删除全部旧方向后的新残差 | 浮点消去可能损失有效数字 |
| $r_{jj}=\|v_j\|$ | 新方向的尺度 | 为零表示精确线性相关 |
| $q_j=v_j/r_{jj}$ | 归一化新方向 | 近零会导致数值不稳定 |
| $Q^*Q=I$ | 正交性证书 | 程序中用 $\|I-Q^*Q\|$ 验收 |
| $A=QR$ | 重构证书 | 还需同时检查正交性，残差小不够 |

> [!tip] 初学者的停靠点
> 若能套递推式，却无法解释为什么 $v_j$ 与每个旧 $q_i$ 正交，先完整展开第二步；若不知道 $v_j=0$ 与输入线性相关的等价关系，则先完成“为什么不会除以零”。

## 阅读前检查

开始前只需要知道：

- [[向量空间]]：线性组合、张成、线性无关和基；
- [[内积空间]]：内积、范数与正交；
- 本章会从一维最小距离重新得到：向量在单位方向 $\boldsymbol q$ 上的分量是
  $$
  \operatorname{proj}_{\boldsymbol q}(\boldsymbol a)
  =\langle\boldsymbol a,\boldsymbol q\rangle\boldsymbol q.
  $$

这里约定复内积对第一变量线性，因此坐标写成
$\langle\boldsymbol a,\boldsymbol q\rangle=\boldsymbol q^{*}\boldsymbol a$。

## 先看一个具体问题

在 $\mathbb R^3$ 中给定

$$
\boldsymbol a_1=
\begin{bmatrix}1\\1\\0\end{bmatrix},
\qquad
\boldsymbol a_2=
\begin{bmatrix}1\\0\\1\end{bmatrix}.
$$

它们线性无关，所以张成一个二维平面；但它们既不正交，也不是单位向量：

$$
\boldsymbol a_1^{\top}\boldsymbol a_2=1\ne0,
\qquad
\|\boldsymbol a_1\|_2=\|\boldsymbol a_2\|_2=\sqrt2.
$$

若直接用它们表示向量，坐标不能只靠点积读出。我们希望在不改变所张成平面的前提下，找到单位向量
$\boldsymbol q_1,\boldsymbol q_2$，满足

$$
\boldsymbol q_1^{\top}\boldsymbol q_2=0,
\qquad
\|\boldsymbol q_1\|_2=\|\boldsymbol q_2\|_2=1.
$$

Gram–Schmidt 正是在解决这个问题。

## 正交、标准正交和标准正交基

> [!definition] 三个层次
> 向量组 $(\boldsymbol q_1,\ldots,\boldsymbol q_k)$：
>
> - 若 $i\ne j$ 时 $\langle\boldsymbol q_i,\boldsymbol q_j\rangle=0$，称为正交组；
> - 若进一步每个 $\|\boldsymbol q_i\|=1$，称为标准正交组；
> - 若它还是整个空间或目标子空间的一组基，称为标准正交基。

把这些向量作为列组成

$$
\boldsymbol Q=
\begin{bmatrix}
\boldsymbol q_1&\cdots&\boldsymbol q_k
\end{bmatrix}
\in\mathbb F^{m\times k},
$$

标准正交条件可压缩为

$$
\boldsymbol Q^{*}\boldsymbol Q=\boldsymbol I_k.
$$

左边第 $(i,j)$ 个元素正是
$\boldsymbol q_i^{*}\boldsymbol q_j=\langle\boldsymbol q_j,\boldsymbol q_i\rangle$：
对角线是 1，非对角线是 0。

## 为什么标准正交基特别方便

若 $\boldsymbol q_1,\ldots,\boldsymbol q_k$ 是子空间 $U$ 的标准正交基，任意
$\boldsymbol x\in U$ 都有展开

$$
\boldsymbol x=\sum_{i=1}^{k}c_i\boldsymbol q_i.
$$

两边与 $\boldsymbol q_j$ 做内积：

$$
\begin{aligned}
\langle\boldsymbol x,\boldsymbol q_j\rangle
&=
\left\langle
\sum_{i=1}^{k}c_i\boldsymbol q_i,
\boldsymbol q_j
\right\rangle\\
&=
\sum_{i=1}^{k}c_i
\langle\boldsymbol q_i,\boldsymbol q_j\rangle\\
&=c_j.
\end{aligned}
$$

第二行使用内积的线性；第三行使用标准正交性。因此

$$
c_j=\langle\boldsymbol x,\boldsymbol q_j\rangle.
$$

坐标无需再解方程。长度也满足 Parseval/Pythagoras 形式：

$$
\|\boldsymbol x\|^2
=\sum_{i=1}^{k}|c_i|^2.
$$

## Gram–Schmidt 过程

给定线性无关向量

$$
\boldsymbol a_1,\ldots,\boldsymbol a_n,
$$

希望构造标准正交向量
$\boldsymbol q_1,\ldots,\boldsymbol q_n$。

### 第一步：归一化第一个方向

$$
\boldsymbol v_1=\boldsymbol a_1,
\qquad
r_{11}=\|\boldsymbol v_1\|,
\qquad
\boldsymbol q_1=\frac{\boldsymbol v_1}{r_{11}}.
$$

因为 $\boldsymbol a_1\ne0$，所以 $r_{11}>0$。

### 第二步：从第二个向量减去旧方向

先计算 $\boldsymbol a_2$ 在 $\boldsymbol q_1$ 上的坐标

$$
r_{12}=\langle\boldsymbol a_2,\boldsymbol q_1\rangle.
$$

再减去投影：

$$
\boldsymbol v_2
=\boldsymbol a_2-r_{12}\boldsymbol q_1.
$$

检查它与 $\boldsymbol q_1$ 正交：

$$
\begin{aligned}
\langle\boldsymbol v_2,\boldsymbol q_1\rangle
&=
\langle\boldsymbol a_2,\boldsymbol q_1\rangle
-r_{12}\langle\boldsymbol q_1,\boldsymbol q_1\rangle\\
&=r_{12}-r_{12}=0.
\end{aligned}
$$

最后归一化：

$$
r_{22}=\|\boldsymbol v_2\|,
\qquad
\boldsymbol q_2=\frac{\boldsymbol v_2}{r_{22}}.
$$

### 一般第 $j$ 步

把 $\boldsymbol a_j$ 沿所有已有方向的投影都减掉：

$$
r_{ij}
=\langle\boldsymbol a_j,\boldsymbol q_i\rangle,
\qquad 1\le i<j,
$$

$$
\boldsymbol v_j
=\boldsymbol a_j
-\sum_{i=1}^{j-1}r_{ij}\boldsymbol q_i,
$$

$$
r_{jj}=\|\boldsymbol v_j\|,
\qquad
\boldsymbol q_j=\frac{\boldsymbol v_j}{r_{jj}}.
$$

> [!analysis] 一般第 $j$ 步的七问拆解
> | 问题 | 回答 |
> |---|---|
> | 输入是什么？ | 一个新列 $a_j$ 和已经构造好的标准正交组 $q_1,\ldots,q_{j-1}$。 |
> | $r_{ij}$ 是什么？ | $a_j$ 沿单位方向 $q_i$ 的坐标；复数情形共轭位置由内积约定决定。 |
> | 为什么减去所有投影？ | 要让残差同时正交于整个旧 span，而非只正交于最后一个方向。 |
> | 为什么残差保留新信息？ | $a_j=v_j+\sum_{i<j}r_{ij}q_i$，所以加入 $v_j$ 与加入 $a_j$ 得到同一前缀 span。 |
> | 何时可以归一化？ | 当 $v_j\ne0$；输入组线性无关恰好保证这一点。 |
> | 何时失败？ | 精确 $v_j=0$ 表示依赖；浮点 $\|v_j\|$ 很小表示近相关和潜在正交性丢失。 |
> | 后续怎样使用？ | $q_j$ 进入 $Q$，全部 $r_{ij}$ 进入上三角 $R$，形成 $A=QR$。 |

~~~mermaid
flowchart LR
    A["新向量 aⱼ"] --> P["计算它在 q₁,…,qⱼ₋₁ 上的投影"]
    P --> R["减掉全部旧方向，得到残差 vⱼ"]
    R --> O["vⱼ 与全部旧方向正交"]
    O --> N["除以 ||vⱼ||，得到单位向量 qⱼ"]
~~~

## 为什么它保持张成空间

> [!theorem] 前缀张成空间保持
> 对每个 $j$，
> $$
> \operatorname{span}(\boldsymbol q_1,\ldots,\boldsymbol q_j)
> =
> \operatorname{span}(\boldsymbol a_1,\ldots,\boldsymbol a_j).
> $$

证明使用归纳。

当 $j=1$，$\boldsymbol q_1$ 只是 $\boldsymbol a_1$ 的非零倍数，两者张成同一直线。

假设前 $j-1$ 个方向已经保持张成空间。由构造，

$$
\boldsymbol v_j
=\boldsymbol a_j
-\sum_{i<j}r_{ij}\boldsymbol q_i,
$$

所以 $\boldsymbol v_j$ 属于
$\operatorname{span}(\boldsymbol a_1,\ldots,\boldsymbol a_j)$；
$\boldsymbol q_j$ 是 $\boldsymbol v_j$ 的非零倍数，也属于该空间。

反过来，把等式改写为

$$
\boldsymbol a_j
=\boldsymbol v_j+\sum_{i<j}r_{ij}\boldsymbol q_i
=r_{jj}\boldsymbol q_j+\sum_{i<j}r_{ij}\boldsymbol q_i,
$$

可见 $\boldsymbol a_j$ 属于
$\operatorname{span}(\boldsymbol q_1,\ldots,\boldsymbol q_j)$。
两个方向的包含关系都成立，因此两个张成空间相等。

## 为什么不会除以零

若某一步 $\boldsymbol v_j=\boldsymbol0$，则

$$
\boldsymbol a_j
=\sum_{i<j}r_{ij}\boldsymbol q_i.
$$

前缀张成空间保持告诉我们右边属于
$\operatorname{span}(\boldsymbol a_1,\ldots,\boldsymbol a_{j-1})$，
这意味着 $\boldsymbol a_j$ 可由前面向量线性表示，与原向量组线性无关矛盾。

因此，对线性无关输入，所有 $r_{jj}>0$。

## 手算例子

回到开头的

$$
\boldsymbol a_1=(1,1,0)^{\top},
\qquad
\boldsymbol a_2=(1,0,1)^{\top}.
$$

第一步：

$$
r_{11}=\sqrt2,
\qquad
\boldsymbol q_1=\frac1{\sqrt2}(1,1,0)^{\top}.
$$

第二个向量沿 $\boldsymbol q_1$ 的坐标：

$$
r_{12}
=\boldsymbol q_1^{\top}\boldsymbol a_2
=\frac1{\sqrt2}.
$$

减去投影：

$$
\begin{aligned}
\boldsymbol v_2
&=
\begin{bmatrix}1\\0\\1\end{bmatrix}
-\frac1{\sqrt2}
\frac1{\sqrt2}
\begin{bmatrix}1\\1\\0\end{bmatrix}\\
&=
\begin{bmatrix}1/2\\-1/2\\1\end{bmatrix}.
\end{aligned}
$$

其长度为

$$
r_{22}
=\sqrt{\frac14+\frac14+1}
=\sqrt{\frac32}
=\frac{\sqrt6}{2}.
$$

所以

$$
\boldsymbol q_2
=\frac1{\sqrt6}(1,-1,2)^{\top}.
$$

验证：

$$
\boldsymbol q_1^{\top}\boldsymbol q_2
=\frac{1-1+0}{\sqrt{12}}=0,
\qquad
\|\boldsymbol q_2\|_2^2
=\frac{1+1+4}{6}=1.
$$

## 从 Gram–Schmidt 到 QR

由每一步的改写式，

$$
\boldsymbol a_j
=\sum_{i=1}^{j}r_{ij}\boldsymbol q_i.
$$

系数只在 $i\le j$ 时出现，因此排成矩阵后

$$
\boldsymbol A=\boldsymbol Q\boldsymbol R,
$$

其中 $\boldsymbol R$ 是上三角矩阵。这就是[[QR 分解]]。

## 精确算术与浮点实现

> [!warning] 公式正确不代表最朴素实现总能保持正交
> 在精确算术中，Gram–Schmidt 得到严格标准正交列；浮点数中，接近线性相关的输入会让“两个接近向量相减”，造成有效数字丢失。

- Classical Gram–Schmidt 一次计算并减去全部原始投影，可能明显丢失正交性；
- Modified Gram–Schmidt 逐次更新残差，通常更可靠；
- Householder QR 使用酉/正交反射，通常是稠密矩阵 QR 的稳定默认选择；
- 若输入本身近秩亏，任何算法都必须面对问题条件性，稳定算法不能创造不存在的信息。

完整数值理论见[[数值稳定性|Gram-Schmidt 的数值稳定性总论]]；当前可先运行[[实验 - Gram-Schmidt 与 QR 的正交性误差]]，观察“重构残差很小，但 $\boldsymbol Q$ 已明显不正交”的现象。

## 在 AI 中的连接

- **表示去相关**：正交基把子空间中的坐标解耦，但正交不等于统计独立。
- **PCA/SVD**：奇异向量本身就是标准正交组，坐标能量可直接相加。
- **正交初始化**：希望线性层在若干方向上不过度放大或压缩；矩形正交列与方阵正交需要区分。
- **LoRA/低秩因子**：对因子列空间做 QR 可以分离“子空间选择”和“内部坐标尺度”。
- **Krylov 方法**：Arnoldi/Lanczos 每一步都要把新方向对已有基正交化。

## 边界与常见误区

1. 正交组若含零向量，不能归一化成标准正交组。
2. Gram–Schmidt 要求按顺序处理；改变输入顺序通常改变输出基。
3. 输出基不唯一：每个实单位向量可换符号，复数情形可换单位相位。
4. “列两两正交”不等于矩阵是方阵正交矩阵；矩形 $\boldsymbol Q$ 只有
   $\boldsymbol Q^{*}\boldsymbol Q=\boldsymbol I$。
5. 正交化不会改变张成空间，但会改变坐标和基向量的具体含义。

## 本节回顾

- Gram–Schmidt 解决的是：在不改变张成空间的前提下构造标准正交基。
- 第 $j$ 步先减去已有方向的所有投影，再归一化残差。
- 线性无关保证残差非零，因此不会除以零。
- 标准正交坐标可由内积直接读取，长度等于坐标平方和。
- 浮点实现还需比较 Classical、Modified 和 Householder 方法。

## 练习

- [[习题 - 标准正交基与 Gram-Schmidt]]
- [[解答 - 标准正交基与 Gram-Schmidt]]

## 来源

- Sheldon Axler, [Linear Algebra Done Right, 4th ed.](https://linear.axler.net/LADR4e.pdf), Section 6B。
- [MIT 18.06：Gram–Schmidt and A = QR](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/pages/readings/)。
- [MIT 18.335：Classical、Modified Gram–Schmidt 与 Householder QR](https://ocw.mit.edu/courses/18-335j-introduction-to-numerical-methods-spring-2019/pages/week-4/)。
