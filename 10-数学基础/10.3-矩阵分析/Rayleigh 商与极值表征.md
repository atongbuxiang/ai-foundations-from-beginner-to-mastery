---
type: concept
status: draft
area: [math/matrix-analysis, math/optimization, ai/representation]
aliases: [Rayleigh Quotient, Courant-Fischer 定理, 极小极大原理, Ky Fan 最大原理]
prerequisites: ["[[定理 - 有限维谱定理]]", "[[二次型与正定矩阵]]", "[[内积空间]]", "[[子空间、张成与线性无关]]"]
related: ["[[特征向量与子空间扰动定理]]", "[[幂法、反幂法与 Rayleigh 商迭代]]", "[[共轭梯度法]]", "[[矩阵扰动]]", "[[有效秩]]", "[[矩阵分析 MOC]]"]
sources: ["Axler-LADR4e-7B-7C", "MIT-18.409-Courant-Fischer", "Ky-Fan-Maximum-Principle"]
exercises: ["[[习题 - Rayleigh 商与极值表征]]"]
solutions: ["[[解答 - Rayleigh 商与极值表征]]"]
created: 2026-08-15
updated: 2026-08-27
---

# Rayleigh 商与极值表征

> [!abstract] 本章主问题
> 怎样把“矩阵沿某个方向的能量”变成与向量长度无关的量，并从单个方向推广到最优子空间？对 Hermitian 矩阵，Rayleigh 商是特征值的加权平均；其极值给出两端特征值，Courant–Fischer 原理刻画第 $k$ 个特征值，Ky Fan 原理则刻画前 $k$ 个特征值之和。

## 学习目标

完成本章后，应能独立完成以下任务：

1. 定义 Rayleigh 商并说明为什么分母不能省略；
2. 从谱分解推出 Rayleigh 商是特征值的加权平均；
3. 证明最大、最小 Rayleigh 商等于最大、最小特征值，并刻画等号条件；
4. 用约束优化的一阶条件解释“驻点就是特征向量”；
5. 完整陈述并证明 Courant–Fischer 极小极大原理；
6. 用 Ky Fan 最大原理解释 PCA 为什么选择前 $k$ 个特征方向；
7. 把广义 Rayleigh 商化为标准 Hermitian 特征值问题；
8. 用 Ritz 值和残差判断一个候选方向的谱意义；
9. 区分 Hermitian 变分定理、一般矩阵特征值与奇异值问题；
10. 把这些结论迁移到 PCA、Hessian、LDA、图 Laplacian 和大模型表示分析。

> [!question] 初学者读完必须能回答
> 1. 为什么 Rayleigh 商必须除以 $x^*x$，它因此获得了什么不变性？
> 2. 在特征向量坐标中，Rayleigh 商为什么是特征值的凸组合？
> 3. 最大值和最小值为何恰是极端特征值，等号何时成立？
> 4. 球面约束优化的一阶条件为什么给出特征方程 $Ax=\lambda x$？
> 5. Courant–Fischer 如何从“选一个方向”升级为“选一个 $k$ 维子空间”？
> 6. Ky Fan 原理为何直接解释 PCA 的前 $k$ 维最优子空间？
> 7. 广义 Rayleigh 商、Ritz 值和非 Hermitian 情形各需增加什么条件？

下图回答：去除向量尺度后，怎样从单方向的 Rayleigh 商逐步提升到第 $k$ 个特征值与最优 $k$ 维子空间？

![[00-知识库管理/_assets/figures/rayleigh/fig-rayleigh-sphere-minmax-subspace-v2.svg|880]]

> [!figure] 图 1：从尺度无关方向量到极小极大子空间
> **图源与改绘：** 本库原创教学图；内容参照 Axler、MIT 18.409 的 Courant–Fischer 讲义与 Ky Fan 最大原理。
>
> **怎样读图。** 左栏先把非零向量压到单位球面，因此只剩方向；中栏在特征基中把 $\rho_A(x)$ 写成以 $|c_i|^2/\|x\|^2$ 为权重的特征值平均，所以它必在 $\lambda_{\min}$ 与 $\lambda_{\max}$ 之间；右栏把单方向极值推广到 $k$ 维子空间，连接第 $k$ 个特征值与前 $k$ 个特征值之和。
>
> **适用边界（图没有证明什么）。** 这些实数序关系依赖 $A=A^*$。广义商 $x^*Ax/x^*Bx$ 需要 $B\succ0$，可经 $B^{1/2}$ 白化；非 Hermitian 矩阵一般没有同样的 Rayleigh 极值表征。Ritz 值接近特征值还不足以保证单个向量稳定，需同时检查残差与谱间隙。

## 进入正文前：把绝对能量除以长度，才能比较方向

> [!info] 课程位置
> [[二次型与正定矩阵]]研究 $x^*Ax$，但它会随 $x$ 的长度平方缩放。本章用分母 $x^*x$ 消去这个无关变化，先从“某个方向有多大曲率”得到两端特征值，再把一个方向推广到最优子空间。下一章将问：这些最优方向在数据或矩阵被扰动后还稳定吗？

> [!tip] 建议两遍阅读
> - **第一遍：** 只掌握尺度不变性、特征值凸组合、Rayleigh–Ritz 两端极值。
> - **第二遍：** 再读 Courant–Fischer、Ky Fan、广义 Rayleigh 商、Ritz 残差与 PCA/Hessian/图 Laplacian 映射。

> [!question] 本章的推导问题链
> 1. 为什么 $q_A(cx)=|c|^2q_A(x)$ 使不同长度的向量无法直接比较？
> 2. 除以 $x^*x$ 后，为什么只剩下“方向”？
> 3. 换到特征向量坐标后，分子与分母如何共同产生凸组合权重？
> 4. 为什么凸组合不可能越过最大和最小特征值，何时能达到边界？

### 继续跟踪 $H_\tau$

仍记

$$
q_+=\frac1{\sqrt2}(1,1)^T,\qquad
q_-=\frac1{\sqrt2}(1,-1)^T,
$$

其对应特征值分别为 $2-\tau$ 与 $\tau$。取单位向量

$$
x=c_+q_++c_-q_-,
\qquad |c_+|^2+|c_-|^2=1.
$$

因为 $q_+,q_-$ 是 $H_\tau$ 的正交特征向量，

$$
\boxed{
\rho_{H_\tau}(x)
=(2-\tau)|c_+|^2+\tau|c_-|^2.}
$$

这是两个特征值的加权平均，所以

$$
\tau\le \rho_{H_\tau}(x)\le2-\tau.
$$

左端仅在 $x$ 属于 $q_-$ 特征空间时达到，右端仅在 $x$ 属于 $q_+$ 特征空间时达到。注意：$\tau\downarrow0$ 描述正定裕量消失；$\tau\uparrow1$ 则使两个特征值相遇，这是下一章“方向不再唯一”的边界。

> [!note] 符号账本
> | 符号 | 形状/约束 | 作用 |
> |---|---:|---|
> | $A$ | $n\times n$, $A=A^*$ | 具有实特征值和正交特征基的矩阵 |
> | $x$ | $n$ 维非零向量 | 待测试的方向；商对其缩放不变 |
> | $c_i=u_i^*x$ | 标量 | $x$ 在第 $i$ 个特征方向的坐标 |
> | $w_i$ | $[0,1]$，$\sum_iw_i=1$ | 方向能量占比，即凸组合权重 |
> | $\rho_A(x)$ | 实标量 | 单位长度意义下的方向能量/曲率 |

## 阅读前检查

本章会直接使用四件事：

- [[定理 - 有限维谱定理]]：Hermitian 矩阵存在标准正交特征基；
- [[二次型与正定矩阵]]：$x^*Ax$ 表示沿 $x$ 的能量或曲率；
- [[内积空间]]：单位球面、正交补和标准正交列；
- [[子空间、张成与线性无关]]：维数、交空间和基的语言。

若还不熟悉特征值排序，本章固定采用

$$
\lambda_1\ge \lambda_2\ge\cdots\ge\lambda_n,
$$

并假设 $A=A^*\in\mathbb F^{n\times n}$，其中 $\mathbb F=\mathbb R$ 或 $\mathbb C$。改变排序约定会交换公式中的 `max` 与 `min`，但不会改变定理本质。

## 一、从“方向曲率”提出问题

给定 Hermitian 矩阵 $A$，二次型

$$
q_A(x)=x^*Ax
$$

会随 $x$ 的长度按平方缩放：

$$
q_A(cx)=|c|^2q_A(x).
$$

因此直接比较 $q_A(x)$ 没有意义。只要把 $x$ 放大，数值就会随之放大。我们真正想问的是：

> 单位长度的输入沿方向 $x$ 会获得多少平均能量或曲率？

这要求除去向量长度的影响。

> [!definition] Rayleigh 商
> 对非零向量 $x\in\mathbb F^n$，定义
> $$
> \rho_A(x)=\frac{x^*Ax}{x^*x}.
> $$

因为 $A$ Hermitian，$x^*Ax$ 为实数，所以 $\rho_A(x)\in\mathbb R$。它还满足尺度不变性：

$$
\rho_A(cx)=\rho_A(x),\qquad c\ne0.
$$

因此 Rayleigh 商研究的是**方向**，不是某个特定长度的坐标向量。等价地，我们可以只在单位球面 $\|x\|_2=1$ 上研究

$$
\rho_A(x)=x^*Ax.
$$

## 二、谱坐标中的核心公式

由谱定理，存在酉矩阵

$$
U=[u_1,\ldots,u_n]
$$

使得

$$
A=U\Lambda U^*,
\qquad
\Lambda=\operatorname{diag}(\lambda_1,\ldots,\lambda_n).
$$

把任意非零向量写成特征基展开

$$
x=\sum_{i=1}^n c_i u_i.
$$

因为特征向量标准正交，

$$
x^*x=\sum_{i=1}^n|c_i|^2,
$$

并且

$$
x^*Ax
=\sum_{i=1}^n\lambda_i|c_i|^2.
$$

所以

$$
\boxed{
\rho_A(x)
=\frac{\sum_{i=1}^n\lambda_i|c_i|^2}
{\sum_{i=1}^n|c_i|^2}
=\sum_{i=1}^n w_i\lambda_i
}
$$

其中

$$
w_i=\frac{|c_i|^2}{\sum_j|c_j|^2},
\qquad
w_i\ge0,
\qquad
\sum_iw_i=1.
$$

> [!important] 全章的发动机
> Rayleigh 商是全部特征值的凸组合。方向 $x$ 在特征方向 $u_i$ 上的能量占比 $w_i$，就是特征值 $\lambda_i$ 的权重。

> [!analysis] 谱坐标核心式的公式七问
> | 问题 | 回答 |
> |---|---|
> | 分母解决了什么？ | $x^*x=\|x\|_2^2$ 消去长度平方缩放，使 $\rho_A(cx)=\rho_A(x)$。 |
> | 为什么权重是 $|c_i|^2$？ | 正交特征基消去交叉项，分子为 $\sum_i\lambda_i|c_i|^2$，分母为 $\sum_i|c_i|^2$。 |
> | 为什么是凸组合？ | $w_i=|c_i|^2/\sum_j|c_j|^2\ge0$ 且 $\sum_iw_i=1$，因而商是特征值的加权平均。 |
> | Hermitian 条件用在哪里？ | 它保证实特征值、正交特征基和实 Rayleigh 商；一般矩阵不能沿用同一序关系。 |
> | 等号何时成立？ | 最大值要求 $x$ 全部落在最大特征值子空间；若是重特征值，等号方向不唯一。 |
> | 怎样验收候选特征对？ | 除了商 $\rho_A(x)$，还应检查残差 $\|Ax-\rho_A(x)x\|$ 和与其他谱的 gap。 |
> | AI 中怎样调用？ | PCA 最大化方差，Hessian 商测曲率，谱聚类最小化 Laplacian 能量；多维版转向 Courant–Fischer/Ky Fan。 |

由凸组合立刻得到

$$
\lambda_n\le \rho_A(x)\le\lambda_1.
$$

这个简单式子同时解释了极值、正定性、近似特征向量和迭代算法。

> [!success] 第一遍停靠线
> 现在应能不看笔记写出 $x=\sum_i c_i u_i$，再推出 $\rho_A(x)=\sum_iw_i\lambda_i$。若你还能说出为何极值在极端特征子空间达到，本章主干已成立；后文是从一维到 $k$ 维的加深。

## 三、极端特征值的变分表征

> [!theorem] Rayleigh–Ritz 极值定理
> 对 Hermitian 矩阵 $A$，
> $$
> \lambda_1
> =\max_{x\ne0}\rho_A(x)
> =\max_{\|x\|_2=1}x^*Ax,
> $$
> $$
> \lambda_n
> =\min_{x\ne0}\rho_A(x)
> =\min_{\|x\|_2=1}x^*Ax.
> $$

### 3.1 证明

上一节已经证明对所有非零 $x$，

$$
\lambda_n\le\rho_A(x)\le\lambda_1.
$$

取 $x=u_1$，得到

$$
\rho_A(u_1)=\lambda_1;
$$

取 $x=u_n$，得到

$$
\rho_A(u_n)=\lambda_n.
$$

因此两个界都能达到，结论成立。

### 3.2 等号条件

若最大特征值是单重的，即 $\lambda_1>\lambda_2$，那么

$$
\rho_A(x)=\lambda_1
$$

当且仅当 $x\in\operatorname{span}\{u_1\}$。

若最大特征值重数为 $r$，即

$$
\lambda_1=\cdots=\lambda_r>\lambda_{r+1},
$$

那么所有最大化方向构成整个顶端特征子空间

$$
\operatorname{span}\{u_1,\ldots,u_r\}.
$$

所以“最大化方向”不一定唯一。唯一的是谱子空间，而不是其中某一组基向量。

## 四、驻点为什么就是特征向量

尺度不变使我们可以研究约束问题

$$
\max_{x^*x=1}x^*Ax.
$$

在实数情形构造 Lagrangian

$$
\mathcal L(x,\mu)=x^TAx-\mu(x^Tx-1).
$$

因为 $A=A^T$，

$$
\nabla_x\mathcal L=2Ax-2\mu x.
$$

一阶必要条件为

$$
Ax=\mu x.
$$

左乘 $x^T$ 并使用 $x^Tx=1$，得到

$$
\mu=x^TAx=\rho_A(x).
$$

因此单位球面上 Rayleigh 商的每个驻点都是特征向量，驻点值就是对应特征值。

> [!warning] 驻点不都等于最大值
> $u_1$ 给出最大值，$u_n$ 给出最小值；中间特征向量通常是球面约束下的鞍点。只写出 $Ax=\mu x$ 还没有完成极值分类。

在复数情形可以使用实微分、Wirtinger 语言，或直接在单位球面的切空间中计算方向导数；结论不变。

## 五、完整二维手算

考虑

$$
A=
\begin{bmatrix}
3&1\\
1&3
\end{bmatrix}.
$$

单位圆上的向量写成

$$
x(\theta)=
\begin{bmatrix}
\cos\theta\\
\sin\theta
\end{bmatrix}.
$$

因为 $\|x(\theta)\|_2=1$，

$$
\rho_A(x(\theta))
=x(\theta)^TAx(\theta).
$$

展开：

$$
\begin{aligned}
\rho_A(x(\theta))
&=3\cos^2\theta+2\sin\theta\cos\theta+3\sin^2\theta\\
&=3+\sin2\theta.
\end{aligned}
$$

所以

$$
\max_\theta\rho_A=4,
\qquad
\min_\theta\rho_A=2.
$$

最大值在 $\theta=\pi/4$ 达到，对应方向

$$
u_1=\frac1{\sqrt2}(1,1)^T;
$$

最小值在 $\theta=-\pi/4$ 达到，对应方向

$$
u_2=\frac1{\sqrt2}(1,-1)^T.
$$

直接计算也有

$$
Au_1=4u_1,
\qquad
Au_2=2u_2.
$$

几何上，Rayleigh 商沿单位圆变化；极值方向正是二次型椭圆的主轴方向。

## 六、为什么第 $k$ 个特征值需要子空间

只做一次最大化得到 $\lambda_1$。为了得到 $\lambda_2$，一种办法是限制

$$
x\perp u_1.
$$

此时

$$
\lambda_2
=\max_{\substack{x\ne0\\x\perp u_1}}\rho_A(x).
$$

继续施加正交约束，得到

$$
\lambda_k
=\max_{\substack{x\ne0\\x\perp u_1,\ldots,u_{k-1}}}\rho_A(x).
$$

但这个写法已经预先知道前 $k-1$ 个特征向量。Courant–Fischer 原理把它改写为不依赖某组已知特征基的子空间优化。

## 七、Courant–Fischer 极小极大原理

> [!theorem] Courant–Fischer
> 设 $A=A^*$ 且 $\lambda_1\ge\cdots\ge\lambda_n$。则对 $1\le k\le n$，
> $$
> \boxed{
> \lambda_k
> =\max_{\dim S=k}\;
> \min_{\substack{x\in S\\x\ne0}}\rho_A(x)
> }
> $$
> 以及
> $$
> \boxed{
> \lambda_k
> =\min_{\dim T=n-k+1}\;
> \max_{\substack{x\in T\\x\ne0}}\rho_A(x).
> }
> $$

第一式读作：

> 在所有 $k$ 维子空间中，寻找一个“最弱方向仍尽可能强”的子空间。

第二式读作：

> 在所有 $n-k+1$ 维子空间中，寻找一个“最强方向已尽可能弱”的子空间。

### 7.1 第一种形式的证明

先取

$$
S_\star=\operatorname{span}\{u_1,\ldots,u_k\}.
$$

对任意 $0\ne x\in S_\star$，谱展开只含 $\lambda_1,\ldots,\lambda_k$，所以

$$
\rho_A(x)\ge\lambda_k.
$$

取 $x=u_k$ 达到等号，于是

$$
\min_{0\ne x\in S_\star}\rho_A(x)=\lambda_k.
$$

这说明右侧至少为 $\lambda_k$。

反过来，任取 $k$ 维子空间 $S$。令

$$
L=\operatorname{span}\{u_k,u_{k+1},\ldots,u_n\},
$$

则

$$
\dim S+\dim L=k+(n-k+1)=n+1>n.
$$

由维数公式，$S\cap L$ 至少含一个非零向量 $y$。因为 $y$ 只含 $u_k,\ldots,u_n$ 分量，

$$
\rho_A(y)\le\lambda_k.
$$

因此

$$
\min_{0\ne x\in S}\rho_A(x)
\le\rho_A(y)
\le\lambda_k.
$$

这对每个 $S$ 都成立，所以最大值不超过 $\lambda_k$。上下界合并即得结论。

### 7.2 第二种形式的证明骨架

取

$$
T_\star=\operatorname{span}\{u_k,u_{k+1},\ldots,u_n\}.
$$

则其中所有方向的 Rayleigh 商都不超过 $\lambda_k$，并由 $u_k$ 达到等号。

另一方面，任意 $n-k+1$ 维子空间 $T$ 必与

$$
\operatorname{span}\{u_1,\ldots,u_k\}
$$

有非零交。交中的非零向量 Rayleigh 商至少为 $\lambda_k$，所以 $T$ 内最大值不可能低于 $\lambda_k$。

## 八、从定理读出三个重要推论

### 8.1 正定性是全方向下界

因为

$$
\lambda_n=\min_{x\ne0}\rho_A(x),
$$

所以

$$
A\succ0
\iff
\lambda_n>0
\iff
x^*Ax\ge \lambda_n\|x\|_2^2
\quad\text{对所有 }x.
$$

在优化中，若 $A=\nabla^2f$，这就是局部强凸曲率下界。

### 8.2 算子范数的 Hermitian 特例

Hermitian 矩阵满足

$$
\|A\|_2=\max_i|\lambda_i|.
$$

注意

$$
\max_x\rho_A(x)=\lambda_1
$$

不一定等于 $\|A\|_2$；当 $|\lambda_n|>\lambda_1$ 时，谱范数由最负特征值的绝对值决定。

### 8.3 单调性

若 $A\preceq B$，那么对所有 $x\ne0$，

$$
\rho_A(x)\le\rho_B(x).
$$

代入 Courant–Fischer 即得

$$
\lambda_k(A)\le\lambda_k(B),
\qquad k=1,\ldots,n.
$$

这是从 Loewner 序到逐项特征值序的桥梁。

## 九、Ritz 值：只在试探子空间里优化

大矩阵问题通常不会直接在整个 $\mathbb F^n$ 上优化。取一个 $m$ 维试探子空间

$$
\mathcal K=\operatorname{col}(Q),
\qquad
Q^*Q=I_m,
$$

并把 $x$ 写成 $x=Qy$。则

$$
\rho_A(Qy)
=\frac{y^*Q^*AQy}{y^*y}.
$$

因此 $A$ 在试探子空间中的极值由压缩矩阵

$$
H=Q^*AQ
$$

的特征值给出。这些特征值称为 Ritz 值，对应向量 $Qy$ 称为 Ritz 向量。

> [!important] 算法接口
> Lanczos、Arnoldi、子空间迭代和 Rayleigh–Ritz 方法的共同结构，是先建立小子空间 $Q$，再求解小矩阵 $Q^*AQ$ 的谱问题。

若 $\theta_1\ge\cdots\ge\theta_m$ 是 Ritz 值，则 Poincaré 分离给出

$$
\lambda_i(A)\ge\theta_i\ge\lambda_{i+n-m}(A),
\qquad i=1,\ldots,m.
$$

它说明压缩后的谱不能任意跑出原谱范围，但“Ritz 值接近”还不自动保证“Ritz 向量接近”；方向稳定仍需要残差和谱间隙，见[[特征向量与子空间扰动定理]]。

## 十、Ky Fan 最大原理：一次选择 $k$ 个方向

PCA 并不是只找一个最大方差方向，而是寻找一个 $k$ 维子空间，使投影后的总方差最大。对应定理是：

> [!theorem] Ky Fan 最大原理
> 若 $A=A^*$ 且 $\lambda_1\ge\cdots\ge\lambda_n$，则
> $$
> \boxed{
> \sum_{i=1}^k\lambda_i
> =\max_{Q^*Q=I_k}\operatorname{tr}(Q^*AQ).
> }
> $$
> 最大值由 $Q=[u_1,\ldots,u_k]$ 达到；若边界处存在重特征值，最优基不唯一。

### 10.1 证明

记 $U=[u_1,\ldots,u_n]$。有

$$
\begin{aligned}
\operatorname{tr}(Q^*AQ)
&=\operatorname{tr}(Q^*U\Lambda U^*Q)\\
&=\sum_{i=1}^n\lambda_i\|Q^*u_i\|_2^2.
\end{aligned}
$$

令

$$
p_i=\|Q^*u_i\|_2^2.
$$

因为 $QQ^*$ 是秩 $k$ 的正交投影，

$$
0\le p_i\le1,
\qquad
\sum_{i=1}^np_i
=\operatorname{tr}(QQ^*)
=k.
$$

要最大化 $\sum_i\lambda_ip_i$，最优做法是把总权重 $k$ 放在最大的 $k$ 个特征值上，即

$$
p_1=\cdots=p_k=1,
\qquad
p_{k+1}=\cdots=p_n=0.
$$

于是最大值为 $\sum_{i=1}^k\lambda_i$。

### 10.2 为什么目标只依赖子空间

若 $R\in\mathbb F^{k\times k}$ 酉，则

$$
(QR)^*(QR)=I_k
$$

且

$$
\operatorname{tr}((QR)^*A(QR))
=\operatorname{tr}(R^*Q^*AQR)
=\operatorname{tr}(Q^*AQ).
$$

所以目标不关心子空间内部选哪组标准正交基。这个“右酉不变性”正是 PCA 方向在重谱下可以旋转的原因。

## 十一、广义 Rayleigh 商

许多问题中的长度不是 $x^*x$，而是由 Hermitian 正定矩阵 $B\succ0$ 定义的

$$
\|x\|_B^2=x^*Bx.
$$

> [!definition] 广义 Rayleigh 商
> $$
> \rho_{A,B}(x)
> =\frac{x^*Ax}{x^*Bx},
> \qquad x\ne0,
> $$
> 其中 $A=A^*$，$B=B^*\succ0$。

约束优化

$$
\max_{x^*Bx=1}x^*Ax
$$

的一阶条件为

$$
Ax=\lambda Bx,
$$

即广义特征值问题。

### 11.1 化为标准问题

因为 $B\succ0$，存在唯一的 $B^{1/2}\succ0$。令

$$
y=B^{1/2}x,
\qquad
x=B^{-1/2}y.
$$

则

$$
x^*Bx=y^*y
$$

且

$$
x^*Ax
=y^*B^{-1/2}AB^{-1/2}y.
$$

因此

$$
\rho_{A,B}(x)
=\rho_{B^{-1/2}AB^{-1/2}}(y).
$$

矩阵 $B^{-1/2}AB^{-1/2}$ 仍是 Hermitian，所以全部标准变分结论都可以迁移过来。

### 11.2 一个手算例子

取

$$
A=\begin{bmatrix}4&0\\0&1\end{bmatrix},
\qquad
B=\begin{bmatrix}1&0\\0&2\end{bmatrix}.
$$

则

$$
\rho_{A,B}(x)
=\frac{4x_1^2+x_2^2}{x_1^2+2x_2^2}.
$$

沿 $e_1$ 的值为 $4$，沿 $e_2$ 的值为 $1/2$；广义特征方程

$$
Ax=\lambda Bx
$$

也给出广义特征值 $4$ 和 $1/2$。

> [!warning] 为什么要求 $B\succ0$
> 若 $B$ 不定或奇异，分母可能为零或改变符号，单位“球面”可能不紧，标准最大最小结论会失败。此时必须进入矩阵铅笔和不定内积理论，不能机械套用本节公式。

## 十二、Rayleigh 商、残差与后验可信度

给定单位向量 $x$，我们想用某个标量 $\mu$ 近似

$$
Ax\approx\mu x.
$$

考虑残差平方

$$
\phi(\mu)=\|Ax-\mu x\|_2^2.
$$

实数 Hermitian 情形下展开并求导：

$$
\phi'(\mu)=-2x^TAx+2\mu.
$$

所以最佳标量是

$$
\mu=\rho_A(x).
$$

定义 Rayleigh 残差

$$
r=Ax-\rho_A(x)x.
$$

它自动满足

$$
x^*r=0.
$$

若把单位向量写成 $x=\sum_ic_iu_i$，则

$$
\|r\|_2^2
=\sum_i|c_i|^2(\lambda_i-\rho_A(x))^2.
$$

因为 $\sum_i|c_i|^2=1$，必有某个特征值满足

$$
\boxed{
\min_i|\lambda_i-\rho_A(x)|\le\|r\|_2.
}
$$

这说明小残差保证 Rayleigh 商靠近**某个**特征值。

> [!warning] 小残差仍不指定方向
> 若多个特征值聚得很近，小残差只能说明 $x$ 接近相应谱簇，不能保证它接近其中某个固定特征向量。要把标量精度升级为方向精度，还需要谱间隙，见[[特征向量与子空间扰动定理]]。

## 十三、与迭代算法的接口

### 13.1 幂法

幂法让主特征方向的系数相对放大；每次归一化后的 Rayleigh 商可作为特征值估计，但真正的停止依据还应包含残差。

### 13.2 Rayleigh 商迭代

Rayleigh 商迭代使用当前

$$
\rho_A(x_k)
$$

作为反幂法移位。对于 Hermitian 矩阵和单特征值，它在局部可达到三次收敛；这属于算法结论，详细条件见[[幂法、反幂法与 Rayleigh 商迭代]]。

### 13.3 Lanczos 与 Ritz 方法

Lanczos 在 Krylov 子空间中构造 $Q$，再求 $Q^*AQ$ 的 Ritz 值。Courant–Fischer 解释为什么扩展试探子空间通常能改进极值近似，而有限精度下的正交性和 ghost Ritz 值需要额外数值分析。

### 13.4 共轭梯度法

对 SPD 矩阵，二次函数

$$
f(x)=\frac12x^TAx-b^Tx
$$

的曲率范围是

$$
\lambda_n\le\rho_A(d)\le\lambda_1.
$$

条件数

$$
\kappa_2(A)=\lambda_1/\lambda_n
$$

因此控制最陡方向与最平方向的曲率比，也进入[[共轭梯度法]]的收敛界。

## 十四、AI 中的直接接口

### 14.1 PCA：最大化投影方差

设中心化样本矩阵 $X\in\mathbb R^{d\times m}$，样本协方差为

$$
C=\frac1mXX^T\succeq0.
$$

单位方向 $q$ 上的投影方差是

$$
\frac1m\|q^TX\|_2^2=q^TCq=\rho_C(q).
$$

所以第一主成分最大化 Rayleigh 商；前 $k$ 个主成分由 Ky Fan 问题

$$
\max_{Q^TQ=I_k}\operatorname{tr}(Q^TCQ)
$$

给出，最优值是前 $k$ 个协方差特征值之和。

### 14.2 表示能量与子空间探针

若隐藏表示 $H\in\mathbb R^{m\times d}$，则

$$
C_H=\frac1mH^TH
$$

的 Rayleigh 商测量特征方向上的平均平方激活。只报告最大特征向量容易受小 gap 影响；报告前 $k$ 子空间、累计解释方差和主角度通常更稳健。

### 14.3 Hessian：方向曲率

在参数点 $\theta$ 附近，

$$
L(\theta+\Delta)
\approx L(\theta)+g^T\Delta+\frac12\Delta^TH\Delta.
$$

单位更新方向 $d$ 的二阶曲率是

$$
d^THd=\rho_H(d).
$$

最大特征值给出最尖锐局部方向，最小特征值为负则表明存在负曲率方向。但深度网络 Hessian 常有重谱、近零谱和随机估计误差，方向解释必须同时报告残差与 gap。

### 14.4 LDA 与度量约束

线性判别分析中的目标常形如

$$
\frac{x^TS_Bx}{x^TS_Wx},
$$

即 $S_W\succ0$ 度量下的广义 Rayleigh 商。若 $S_W$ 奇异，必须正则化、限制到其像空间或使用广义逆；不能假装分母始终正定。

### 14.5 图 Laplacian

对无向图 Laplacian $L\succeq0$，

$$
x^TLx=\frac12\sum_{i,j}w_{ij}(x_i-x_j)^2.
$$

常数向量给出最小特征值 $0$。在正交于常数向量的子空间中最小化 Rayleigh 商，得到第二小特征值和谱聚类的松弛方向。

### 14.6 广义特征问题与白化

广义问题

$$
Ax=\lambda Bx
$$

可以看成先在 $B$ 度量中白化，再对 $B^{-1/2}AB^{-1/2}$ 做普通谱分析。数值实现中通常使用 Cholesky 或结构化广义 eigensolver，不显式形成 $B^{-1/2}$。

## 十五、三个必须区分的层次

| 层次 | 典型问题 | 正确对象 |
|---|---|---|
| 目标值 | 最大能量是多少？ | $\lambda_1$ 或 $\sum_{i=1}^k\lambda_i$ |
| 最优子空间 | 哪个 $k$ 维空间取得最优值？ | 谱投影/列空间 |
| 子空间基 | 用哪 $k$ 个向量表示它？ | 任意相差右酉变换的标准正交基 |

当边界处有重特征值时，目标值可能稳定、最优大子空间可能稳定，但某个单独列向量完全不唯一。这个区分是理解 PCA、谱聚类和表示比较的关键。

## 十六、非 Hermitian 矩阵为何不能直接套用

若 $A\ne A^*$，实数情形的二次型只看到对称部分：

$$
x^TAx=x^T\left(\frac{A+A^T}{2}\right)x.
$$

例如

$$
A=\begin{bmatrix}0&-1\\1&0\end{bmatrix}
$$

的特征值是 $\pm i$，但对所有实 $x$，

$$
x^TAx=0.
$$

所以 Rayleigh 商极值并不刻画一般非对称矩阵的特征值。一般矩阵的放大率应研究

$$
\frac{\|Ax\|_2}{\|x\|_2},
$$

其极值是奇异值；一般特征值则通常通过 Schur 形式、预解式和伪谱分析。

## 十七、数值实现纪律

1. 理论要求 Hermitian 时，先检查 $\|A-A^*\|$，不要默认输入完全对称；
2. 大矩阵只需矩阵—向量乘时，优先使用 Lanczos/LOBPCG 等迭代方法；
3. 广义问题不要显式计算 $B^{-1}$ 或 $B^{-1/2}$，应使用 Cholesky/广义 eigensolver；
4. 报告候选特征对时至少给出归一化残差
   $$
   \frac{\|Ax-\rho_A(x)x\|_2}{(\|A\|_2+|\rho_A(x)|)\|x\|_2};
   $$
5. 报告特征方向时同时给出目标谱与相邻谱的间隙；
6. 比较 $k$ 维表示时优先比较投影矩阵或主角度，而不是逐列余弦。

## 十八、常见误区

> [!warning] 误区 1：最大 Rayleigh 商总等于谱范数
> 只有当 $\lambda_1\ge|\lambda_n|$ 时才成立。一般 Hermitian 矩阵的谱范数是 $\max_i|\lambda_i|$。

> [!warning] 误区 2：驻点只有最大、最小特征向量
> 全部特征向量都是球面上的驻点；中间特征方向通常是鞍点。

> [!warning] 误区 3：前 $k$ 个特征向量逐列唯一
> 符号/相位永远不唯一；重特征值下，子空间内部任意正交/酉旋转都同样正确。

> [!warning] 误区 4：小残差保证接近指定特征向量
> 小残差只保证靠近某个谱值或谱簇。指定方向还需要隔离的谱间隙。

> [!warning] 误区 5：广义 Rayleigh 商只要 $B$ 对称即可
> 标准变分理论要求 $B\succ0$。奇异或不定 $B$ 会改变问题类型。

> [!warning] 误区 6：对任何方阵都能用极值求特征值
> 本章的实值极值结构来自 Hermitian 性；一般矩阵必须换工具。

## 十九、掌握检查

在查看习题解答前，尝试回答：

1. 为什么 $\rho_A(x)$ 是特征值的凸组合？
2. 最大特征值重数大于一时，最大化集合是什么？
3. Courant–Fischer 第一式的证明为什么必然出现维数交公式？
4. Ky Fan 目标为什么只依赖 $\operatorname{col}(Q)$？
5. 怎样把 $Ax=\lambda Bx$ 化为标准 Hermitian 特征值问题？
6. 小残差能保证什么，不能保证什么？
7. PCA、Hessian 和图 Laplacian 分别优化哪个 Rayleigh 型目标？

## 二十、练习与后继

- 分层练习：[[习题 - Rayleigh 商与极值表征]]；
- 独立详解：[[解答 - Rayleigh 商与极值表征]]；
- 方向稳定性：[[特征向量与子空间扰动定理]]；
- 计算算法：[[幂法、反幂法与 Rayleigh 商迭代]]、[[Lanczos 方法]]；
- SPD 优化接口：[[共轭梯度法]]；
- 课程入口：[[矩阵分析 MOC]]。

## 来源与证据边界

- Sheldon Axler, [*Linear Algebra Done Right*, 4th ed.](https://linear.axler.net/LADR4e.pdf)：谱定理、自伴算子与极值结构的教材级依据；
- MIT 18.409, [Lecture 2: Courant–Fischer characterization](https://ocw.mit.edu/courses/18-409-topics-in-theoretical-computer-science-an-algorithmists-toolkit-fall-2009/resources/mit18_409f09_spiel_lec2/)：极值公式、证明与图 Laplacian 接口；
- Ky Fan 最大原理用于多方向 trace 变分；本章给出有限维 Hermitian 情形的自包含证明；
- [[二次型与正定矩阵]]承担能量/曲率前置，[[幂法、反幂法与 Rayleigh 商迭代]]承担算法收敛，[[特征向量与子空间扰动定理]]承担方向误差；本章不把三者混成同一个结论。
