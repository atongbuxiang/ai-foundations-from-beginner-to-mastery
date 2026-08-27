---
type: concept
status: draft
area: [math/calculus, math/matrix-calculus, math/probability, ai/generative-models]
aliases: [Jacobi Formula, Log-Determinant Derivative, 行列式导数, logdet 导数, 迹函数导数]
prerequisites: ["[[矩阵微分、迹技巧与布局约定]]", "[[逆矩阵、线性求解与隐式微分]]", "[[迹、行列式与体积]]", "[[Cholesky 分解]]", "[[条件数]]"]
related: ["[[多重积分、换元公式与积分变换]]", "[[特征值、特征向量与 SVD 的导数]]", "[[矩阵函数的 Fréchet 导数]]", "[[多元高斯分布]]", "[[多元微积分、矩阵微分与自动微分 MOC]]"]
sources: ["Su-2383-Determinant-Derivative", "Magnus-Neudecker-Matrix-Differential-Calculus", "Petersen-Pedersen-Matrix-Cookbook", "Higham-Functions-of-Matrices", "Dinh-2017-RealNVP", "Kingma-Dhariwal-2018-Glow"]
exercises: ["[[习题 - 行列式、log-det 与迹的导数]]"]
solutions: ["[[解答 - 行列式、log-det 与迹的导数]]"]
created: 2026-08-18
updated: 2026-08-27
---

# 行列式、log-det 与迹的导数

> [!abstract] 本章主问题
> 行列式的一阶变化由 Jacobi 公式控制：对任意方阵方向 $E$，
> $$
> D\det(A)[E]=\operatorname{tr}(\operatorname{adj}(A)E).
> $$
> 当 $A$ 可逆时，它等于 $\det(A)\operatorname{tr}(A^{-1}E)$；因此 $D\log|\det A|[E]=\operatorname{tr}(A^{-1}E)$。数学上出现 $A^{-1}$，数值上仍应用分解和求解；概率模型中 log-det 衡量体积变化，梯度会在接近奇异时放大。

## 学习目标

完成本章后，你应能：

1. 从行列式对每一行/列的多线性推出代数余子式偏导；
2. 陈述并证明 Jacobi 公式的 adjugate 版本；
3. 在可逆情形推出 $d\det A=\det(A)\operatorname{tr}(A^{-1}dA)$；
4. 解释为什么 adjugate 公式在奇异点仍成立，而逆矩阵公式不成立；
5. 由 $\det(I+tB)$ 推出 $D\det(I)[B]=\operatorname{tr}(B)$；
6. 推导 $\nabla_A\det A=\det(A)A^{-\top}$ 与 $\nabla_A\log|\det A|=A^{-\top}$；
7. 区分 $\log\det A$、$\log|\det A|$ 与 SPD 情形；
8. 用 Cholesky/LU 稳定计算 log-det，并说明不应先形成 det；
9. 推导 $d\operatorname{tr}(A^k)=k\operatorname{tr}(A^{k-1}dA)$；
10. 理解 $d\operatorname{tr}f(A)=\operatorname{tr}(f'(A)dA)$ 的适用范围；
11. 推导 Gaussian 负对数似然对协方差的梯度；
12. 推导 $\Sigma=LL^\top$ 参数化下的 log-det 梯度；
13. 解释正规化流换元公式中的 log-absolute-determinant；
14. 使用矩阵行列式引理处理低秩更新；
15. 理解 Hutchinson 迹估计如何把 trace-inverse 变成随机线性求解；
16. 识别近奇异、符号变化、秩变化和复对数分支处的边界。

> [!question] 初学者读完必须能回答
> 1. Jacobi 公式在奇异与可逆矩阵处分别应写成什么形式？
> 2. 为什么 $d\log|\det A|$ 会化为 trace-inverse 作用？
> 3. $\log\det A$、$\log|\det A|$ 与 SPD 情形有什么区别？
> 4. 为什么稳定实现要用 Cholesky/LU，而不能先算 det 再取 log？
> 5. Gaussian 与 normalizing flow 分别怎样调用 log-det？
> 6. 接近奇异时，数值与梯度会出现什么共同危险？

先用下图回答一个视觉问题：**体积的一阶相对变化怎样变成 trace 公式，并在概率模型中被稳定计算？**

![[00-知识库管理/_assets/figures/logdet/fig-determinant-logdet-trace-derivative-v2.svg|880]]

> [!figure] 图 10.4.12｜体积变化、分解计算与概率模型调用
> A 把 $|\det A|$ 解释为体积缩放，并给出 log-det 的一阶 trace 形式；B 对照 SPD 的 Cholesky 与一般矩阵的带置换 LU；C 连接 Gaussian 与 flow，并标出最小奇异值趋零的边界。来源：独立绘制；生成脚本：[[plot_calculus_operator_figures_v2.py]]；确定性结构示意，无随机种子。

**怎样读图。** A 先区分体积本身与相对体积变化；B 沿分解的对角元素在对数域累计，避免 det 的上溢/下溢；C 再看同一个 log-det 项如何分别承担协方差体积惩罚和变量换元校正，并在奇异边界放大梯度。

**适用边界（图没有证明什么）。** 立方体只提供几何直觉，不能替代 Jacobi 公式证明；分解路线依赖矩阵结构与符号处理。接近奇异的警告不提供统一误差界，复杂域分支、秩变化和随机迹估计还需单独分析。

## 进入正文前：log-det 衡量的是相对体积变化

> [!info] 课程位置
> [[逆矩阵、线性求解与隐式微分]]已经给出 solve 节点的切向和伴随规则；本章处理统一计算图的另一条分支。Jacobi 公式把行列式的多项式导数化为 trace-inverse，而[[多重积分、换元公式与积分变换]]会进一步说明它为何出现在概率密度换元中。

> [!tip] 建议两遍阅读
> - **第一遍：** 掌握 Jacobi 公式的可逆版本、$\nabla_A\log|\det A|=A^{-\top}$、SPD 情形的 Cholesky 计算，以及下面二维例子的 $1/3$ 贡献。
> - **第二遍：** 再读奇异点的 adjugate 版本、$\operatorname{tr}f(A)$、低秩更新、Gaussian/flow 应用与随机 trace-inverse 估计。

> [!question] 本章的推导问题链
> 1. 绝对体积变化为什么含 $\det A$，相对体积变化为什么只剩一个 trace？
> 2. det 在奇异点仍可微，为什么 log-det 却在那里失去定义并产生梯度爆炸？
> 3. 数学公式出现 $A^{-1}$，数值实现为什么仍应使用 Cholesky、LU 或线性求解？
> 4. 同一个 log-det 项怎样分别进入 Gaussian 归一化与 normalizing flow 换元？

### 闭合统一例子的第二条分支

仍取

$$
A(\theta)=
\begin{bmatrix}
2+\theta&1\\
1&2
\end{bmatrix}.
$$

直接计算得到

$$
\det A(\theta)=3+2\theta.
$$

当 $\theta>-3/2$ 时 $A(\theta)$ 为 SPD，因而实数

$$
r(\theta)=\frac12\log\det A(\theta)
$$

有定义。直接求导给出

$$
r'(\theta)=\frac1{3+2\theta},
\qquad
\boxed{r'(0)=\frac13.}
$$

现在用矩阵微分重算同一结果。在 $A_0$ 处，

$$
A_0^{-1}
=\frac13
\begin{bmatrix}
2&-1\\
-1&2
\end{bmatrix},
\qquad
E=\frac{dA}{d\theta}
=\begin{bmatrix}1&0\\0&0\end{bmatrix}.
$$

由

$$
d\log\det A=\operatorname{tr}(A^{-1}dA)
$$

可得

$$
Dr(A_0)[E]
=\frac12\operatorname{tr}(A_0^{-1}E)
=\frac12\cdot\frac23
=\frac13.
$$

因此

$$
\boxed{\nabla_A r(A_0)=\frac12A_0^{-\top}.}
$$

上一章已经算出求解分支

$$
q(\theta)=\frac12\|A(\theta)^{-1}b\|_2^2
$$

在原点的导数是

$$
q'(0)=-\frac{10}{27}.
$$

两条分支在共享的 $A$ 处相加：

$$
\boxed{
L'(0)=q'(0)+r'(0)
=-\frac{10}{27}+\frac{9}{27}
=-\frac1{27}.}
$$

这同时完成三重核对：直接标量求导、前向 JVP 与反向矩阵梯度配对都给出 $-1/27$。

当 $\theta\downarrow-3/2$ 时，

$$
\det A(\theta)\downarrow0,
\qquad
r'(\theta)=\frac1{3+2\theta}\longrightarrow+\infty.
$$

这不是绘图或浮点实现造成的假象，而是 log-det 在奇异边界的真实条件性；与此同时，线性求解分支也会因最小特征值趋零而变得病态。

> [!note] 符号账本
> | 符号 | 类型 | 含义 |
> |---|---:|---|
> | $\det A$ | 标量 | 有向体积缩放 |
> | $\log\det A$ | 标量 | SPD 矩阵的对数体积 |
> | $\log|\det A|$ | 标量 | 一般实可逆矩阵的对数绝对体积 |
> | $\operatorname{adj}(A)$ | 方阵 | 奇异点也有定义的伴随矩阵 |
> | $A^{-\top}$ | 方阵 | Frobenius 几何下 log-det 的梯度 |
> | $E=dA/d\theta$ | 方阵 | 参数方向诱导的矩阵扰动 |
> | $\sigma_{\min}(A)$ | 非负标量 | 距离奇异性与梯度放大的关键尺度 |

> [!analysis] log-det 微分的公式七问
> | 问题 | 回答 |
> |---|---|
> | 核心公式是什么？ | 可逆时 $D\log|\det A|[E]=\operatorname{tr}(A^{-1}E)$；SPD 时可去掉绝对值。 |
> | 它从哪里来？ | Jacobi 公式先给 $D\det(A)[E]=\det(A)\operatorname{tr}(A^{-1}E)$，再除以 $\det A$。 |
> | 梯度为什么是 $A^{-\top}$？ | 因为 $\operatorname{tr}(A^{-1}E)=\operatorname{tr}((A^{-\top})^\top E)=\langle A^{-\top},E\rangle_F$。 |
> | 奇异点怎么办？ | det 的 adjugate 公式仍成立；但 $\log|\det A|$ 无定义，不能把逆矩阵公式延拓过去。 |
> | 怎样稳定计算？ | SPD 用 Cholesky 对角线的对数和，一般可逆矩阵用带主元 LU 的符号与对数绝对值；不要先形成 det。 |
> | 怎样验收？ | 比较方向有限差分与 $\operatorname{tr}(A^{-1}E)$，并监测最小奇异值、分解状态和求解残差。 |
> | AI 中怎样调用？ | Gaussian 协方差、normalizing flow、Laplace 近似、DPP、核方法与二阶模型都会调用 log-det 或 trace-inverse。 |

> [!success] 第一遍停靠线
> 若你能分别用 $\det A(\theta)=3+2\theta$ 和 trace-inverse 公式得到 $r'(0)=1/3$，再与求解分支的 $-10/27$ 相加得到 $L'(0)=-1/27$，就已掌握本章主干。还应能说明为什么 $\theta\downarrow-3/2$ 时 det 的导数仍可谈，而 log-det 与线性求解都会失稳。

## 零、几何入口：行列式为何与 AI 概率密度有关

方阵 $A\in\mathbb R^{n\times n}$ 把单位立方体变成由列向量 $a_1,\ldots,a_n$ 张成的平行多面体：

$$
|\det A|=\text{有向线性变换的体积缩放绝对值}.
$$

符号记录定向是否翻转，绝对值记录体积。当变量变换 $y=f(x)$ 局部由 Jacobian $J_f(x)$ 近似时，密度必须按体积伸缩修正，因此出现 $|\det J_f|$。高维中 det 很容易上溢/下溢，所以概率模型几乎总在对数域使用

$$
\log|\det J_f|.
$$

本章先解决导数；完整的密度换元证明放在[[多重积分、换元公式与积分变换]]。

## 一、从代数余子式到 Jacobi 公式

### 1.1 元素偏导

设 $A=(a_{ij})$，记 $C_{ij}$ 为元素 $a_{ij}$ 的代数余子式。固定除 $a_{ij}$ 外的所有元素。由于行列式对第 $i$ 行线性，$\det A$ 关于 $a_{ij}$ 是一次函数，且

$$
\boxed{
\frac{\partial\det A}{\partial a_{ij}}=C_{ij}.
}
$$

这正是苏剑林《行列式的导数》采用的入口：让各元素随标量 $t$ 变化，再由多元链式法则求和。

### 1.2 adjugate 的索引方向

余子式矩阵为 $C=(C_{ij})$，伴随矩阵（adjugate）定义为

$$
\operatorname{adj}(A)=C^\top.
$$

并满足

$$
A\operatorname{adj}(A)=\operatorname{adj}(A)A=\det(A)I.
$$

对方向 $E=(e_{ij})$，

$$
\begin{aligned}
D\det(A)[E]
&=\sum_{i,j}C_{ij}e_{ij}\\
&=\operatorname{tr}(C^\top E)\\
&=\operatorname{tr}(\operatorname{adj}(A)E).
\end{aligned}
$$

所以对所有方阵，包括奇异矩阵，都有

$$
\boxed{
D\det(A)[E]=\operatorname{tr}(\operatorname{adj}(A)E).
}
$$

与 $D f(A)[E]=\operatorname{tr}((\nabla_Af)^\top E)$ 比较：

$$
\boxed{
\nabla_A\det(A)=\operatorname{adj}(A)^\top=C.
}
$$

### 1.3 可逆情形的 Jacobi 公式

若 $A$ 可逆，

$$
\operatorname{adj}(A)=\det(A)A^{-1}.
$$

因此

$$
\boxed{
D\det(A)[E]
=\det(A)\operatorname{tr}(A^{-1}E).
}
$$

沿可微曲线 $A(t)$：

$$
\boxed{
\frac{d}{dt}\det A(t)
=\det A(t)\operatorname{tr}\left(A(t)^{-1}A'(t)\right).
}
$$

梯度为

$$
\boxed{
\nabla_A\det(A)=\det(A)A^{-\top}.
}
$$

### 1.4 另一证明：分离基点与相对扰动

若 $A$ 可逆，

$$
\det(A+tE)=\det(A)\det(I+tA^{-1}E).
$$

只需证明

$$
\det(I+tB)=1+t\operatorname{tr}(B)+O(t^2).
$$

行列式展开中，一阶项只能从某一个对角位置选 $tB_{ii}$，其余位置选单位阵的 $1$；任何包含两个 $tB$ 的项至少二阶。因此一阶系数是 $\sum_iB_{ii}=\operatorname{tr}B$。于是

$$
\det(A+tE)
=\det A\left[1+t\operatorname{tr}(A^{-1}E)+O(t^2)\right].
$$

这也解释了科学空间文章中的核心近似：

$$
\boxed{
\det(I+tB)=1+t\operatorname{tr}(B)+o(t).
}
$$

## 二、奇异矩阵处究竟发生什么

### 2.1 det 是多项式，所以处处可微

$\det A$ 是 $n^2$ 个元素的多项式，因此在所有矩阵处光滑。奇异只会使“含 $A^{-1}$ 的表达”失效，不会使 det 自身不可微。正确通式仍是

$$
D\det(A)[E]=\operatorname{tr}(\operatorname{adj}(A)E).
$$

### 2.2 秩决定一阶项是否消失

- 若 $\operatorname{rank}(A)=n-1$，$\operatorname{adj}(A)$ 通常非零，某些方向上 det 有非零一阶变化；
- 若 $\operatorname{rank}(A)\le n-2$，所有 $(n-1)\times(n-1)$ 余子式为零，故 $\operatorname{adj}(A)=0$，det 的一阶导数在所有方向都为零；最早的非零变化可能是二阶或更高阶。

例：在 $A=0_{2\times2}$，

$$
\det(tE)=t^2\det E,
$$

所以一阶导数为零，但函数不是局部常数。

### 2.3 log-det 的边界不同

$\log|\det A|$ 只在 $A$ 可逆的各个连通区域上定义；当 $A$ 接近奇异，值趋向 $-\infty$，梯度 $A^{-\top}$ 可能爆炸。det 处处光滑并不意味着 log-det 可跨越奇异集合光滑延拓。

## 三、log-det 与 log-absolute-determinant

### 3.1 一般实可逆矩阵

在 $\det A\ne0$ 的区域，

$$
d\log|\det A|
=\frac{1}{\det A}d\det A
=\operatorname{tr}(A^{-1}dA).
$$

所以

$$
\boxed{
D\log|\det A|[E]=\operatorname{tr}(A^{-1}E),
\qquad
\nabla_A\log|\det A|=A^{-\top}.
}
$$

在不跨越 $\det A=0$ 时，$\det A$ 的符号局部恒定，绝对值不会额外引入一个导数符号。

### 3.2 SPD 矩阵

若 $A\succ0$，则 $\det A>0$，可以直接写

$$
\log\det A.
$$

其梯度是 $A^{-1}$，因为 $A=A^\top$。若把变量限制在对称空间，$A^{-\top}=A^{-1}$ 本来就是对称的，无需额外投影。

### 3.3 一般 $\log\det A$ 的实数边界

若实矩阵 $A$ 有负行列式，实数 $\log\det A$ 未定义，但 $\log|\det A|$ 有定义。复数情形还涉及复对数分支与特征值穿越支割线；不能无条件沿用实公式作全局声明。

## 四、数值计算：永远不要先算 det 再取 log

### 4.1 SPD：Cholesky

若

$$
A=LL^\top,
$$

其中 $L$ 下三角且对角正，则

$$
\det A=(\det L)^2=\left(\prod_iL_{ii}\right)^2,
$$

$$
\boxed{
\log\det A=2\sum_i\log L_{ii}.
}
$$

这样避免巨大/极小乘积，也复用稳定分解。涉及 $A^{-1}v$ 或 trace-inverse 时用 Cholesky 三角求解，不形成 $A^{-1}$。

### 4.2 一般可逆矩阵：带主元 LU

若 $PA=LU$，则

$$
\det A=\det(P)\prod_iU_{ii}.
$$

数值程序通常分别返回 sign 与 logabsdet：

$$
s=\operatorname{sign}(\det A),
\qquad
\ell=\sum_i\log|U_{ii}|,
$$

并用主元置换修正 $s$。概率密度常只用 $\ell$；定向相关问题还需 $s$。

### 4.3 近奇异不是实现小问题

当最小奇异值 $\sigma_{\min}(A)$ 很小，

$$
\|\nabla_A\log|\det A|\|_2
=\|A^{-\top}\|_2
=\frac1{\sigma_{\min}(A)}.
$$

梯度爆炸准确反映体积接近塌缩的高敏感性。加 jitter $A+\varepsilon I$ 会改善条件，但也改变目标；应记录 $\varepsilon$ 并说明这是模型正则化还是纯数值近似。

## 五、迹函数的导数

### 5.1 线性迹

$$
f(A)=\operatorname{tr}(C^\top A)
\quad\Longrightarrow\quad
\boxed{\nabla_Af=C.}
$$

若 $f(A)=\operatorname{tr}(CA)$，则 $\nabla_Af=C^\top$。

### 5.2 矩阵幂的迹

乘积法则给

$$
d(A^k)=\sum_{j=0}^{k-1}A^j(dA)A^{k-1-j}.
$$

矩阵因子不能交换，所以一般不能写 $d(A^k)=kA^{k-1}dA$。但取迹后，每一项可循环成

$$
\operatorname{tr}(A^{k-1}dA).
$$

因此

$$
\boxed{
d\operatorname{tr}(A^k)
=k\operatorname{tr}(A^{k-1}dA),
}
$$

$$
\boxed{
\nabla_A\operatorname{tr}(A^k)
=k(A^{k-1})^\top.
}
$$

迹消除了非交换展开中各插入位置的差异，但矩阵函数本身的导数仍不是普通标量求导。

### 5.3 $\operatorname{tr}f(A)$

对多项式 $f$，由上式线性组合：

$$
d\operatorname{tr}f(A)
=\operatorname{tr}(f'(A)dA).
$$

该结论可在适当谱域与正则性条件下推广到解析矩阵函数。它说的是“矩阵函数取迹后的标量微分”；不能推出

$$
df(A)=f'(A)dA
$$

作为一般矩阵恒等式。完整的非交换 Fréchet 导数见[[矩阵函数的 Fréchet 导数]]。

### 5.4 log-det 与 trace-log

当矩阵对数定义良好（例如 $A\succ0$）时，

$$
\log\det A=\operatorname{tr}(\log A).
$$

谱分解 $A=Q\Lambda Q^\top$ 给

$$
\operatorname{tr}\log A=\sum_i\log\lambda_i
=\log\prod_i\lambda_i.
$$

这提供 log-det、谱和矩阵函数之间的桥梁，但数值上不一定要做特征分解；SPD 情形 Cholesky 通常更直接。

## 六、复合参数与低秩结构

### 6.1 $A=A(\theta)$

链式法则应保留方向作用：

$$
d\log|\det A(\theta)|
=\operatorname{tr}\left(A(\theta)^{-1}D_\theta A[d\theta]\right).
$$

反向观点是先得到对 $A$ 的 seed $A^{-\top}$，再通过构造 $A(\theta)$ 的 VJP 回拉到 $\theta$。

### 6.2 Cholesky/因子参数化 $\Sigma=LL^\top$

若 $L$ 可逆，

$$
\log\det(LL^\top)=2\log|\det L|.
$$

所以环境空间梯度

$$
\boxed{\nabla_L\log\det(LL^\top)=2L^{-\top}.}
$$

若 $L$ 被限制为正对角下三角，允许方向只在下三角；实现中的参数梯度应投影/映射到这些自由元素。若对角用 $L_{ii}=e^{s_i}$ 参数化，则

$$
\log\det\Sigma=2\sum_i s_i,
\qquad
\frac{\partial}{\partial s_i}\log\det\Sigma=2.
$$

### 6.3 矩阵行列式引理

若 $A$ 可逆，$U,V\in\mathbb R^{n\times r}$，则

$$
\boxed{
\det(A+UV^\top)
=\det(A)\det(I_r+V^\top A^{-1}U).
}
$$

从而

$$
\log|\det(A+UV^\top)|
=\log|\det A|
+\log|\det(I_r+V^\top A^{-1}U)|,
$$

前提是相关矩阵可逆且符号/绝对值被正确处理。当 $r\ll n$ 时，更新项只需 $r\times r$ log-det 与对 $A$ 的多右端求解。

## 七、Gaussian 负对数似然

设 $x\in\mathbb R^d$、均值 $\mu$、协方差 $\Sigma\succ0$，记 $r=x-\mu$。忽略常数，单样本负对数似然为

$$
\ell(\mu,\Sigma)
=\frac12\log\det\Sigma
+\frac12r^\top\Sigma^{-1}r.
$$

### 7.1 对均值

$$
\boxed{\nabla_\mu\ell=-\Sigma^{-1}r.}
$$

实现为解 $\Sigma y=r$，再取 $-y$。

### 7.2 对协方差

第一项：

$$
d\left(\frac12\log\det\Sigma\right)
=\frac12\operatorname{tr}(\Sigma^{-1}d\Sigma).
$$

第二项利用 $d\Sigma^{-1}=-\Sigma^{-1}(d\Sigma)\Sigma^{-1}$：

$$
\begin{aligned}
d\left(\frac12r^\top\Sigma^{-1}r\right)
&=-\frac12r^\top\Sigma^{-1}(d\Sigma)\Sigma^{-1}r\\
&=-\frac12\operatorname{tr}(\Sigma^{-1}rr^\top\Sigma^{-1}d\Sigma).
\end{aligned}
$$

因 $\Sigma$ 对称，最终

$$
\boxed{
\nabla_\Sigma\ell
=\frac12\left(
\Sigma^{-1}-\Sigma^{-1}rr^\top\Sigma^{-1}
\right).
}
$$

第一项惩罚总体体积，第二项根据样本方向调整 Mahalanobis 距离。两者缺一不可；只最小化二次项会倾向无限放大协方差。

### 7.3 白化实现

令 $\Sigma=LL^\top$。解 $Ly=r$，则

$$
r^\top\Sigma^{-1}r=\|y\|_2^2,
\qquad
\log\det\Sigma=2\sum_i\log L_{ii}.
$$

无需显式形成 $\Sigma^{-1}$。这同时提高数值稳定性并复用分解。

## 八、正规化流中的 log-absolute-determinant

若可逆映射 $z=f(x)$ 把数据变量变到潜变量，则换元公式给

$$
\log p_X(x)
=\log p_Z(f(x))
+\log|\det J_f(x)|.
$$

训练既要让变换后样本在基分布下概率高，也要校正局部体积压缩/膨胀。直接对稠密 $d\times d$ Jacobian 求行列式通常成本 $O(d^3)$，因此 flow 架构特意设计：

- 三角 Jacobian：log-det 是对角对数之和；
- coupling layer：部分变量保持不变，Jacobian 呈块三角；
- 可逆 $1\times1$ 卷积：对通道矩阵做可复用的 LU 参数化；
- 连续流：把 log-det 演化改写为 Jacobian trace，并可能用随机迹估计。

> [!warning] 双射与奇异边界
> 只有局部 Jacobian 非奇异还不足以自动得到全局一一对应；正规化流需要在目标域上控制可逆性。若 $\det J_f=0$，log-det 发散，普通密度换元公式失效。

## 九、大规模 trace-inverse 与随机估计

某些模型需

$$
\frac{d}{d\theta}\log\det A(\theta)
=\operatorname{tr}\left(A^{-1}\frac{dA}{d\theta}\right).
$$

若无法形成完整 trace，可用 Hutchinson 恒等式：若随机向量 $\xi$ 满足

$$
\mathbb E[\xi]=0,
\qquad
\mathbb E[\xi\xi^\top]=I,
$$

则对任意方阵 $M$，

$$
\boxed{\mathbb E[\xi^\top M\xi]=\operatorname{tr}(M).}
$$

取 $M=A^{-1}A'(\theta)$：

$$
\operatorname{tr}(A^{-1}A')
=\mathbb E[\xi^\top A^{-1}A'\xi].
$$

每个 probe 可先算 $v=A'\xi$，再解 $Au=v$，最后算 $\xi^\top u$；或利用迹循环与具体算子结构选择更便宜次序。

随机估计引入方差，线性求解又引入偏差/误差；报告必须包含 probe 分布、数量、随机种子策略、求解容差和置信度。若 $A$ 非对称，估计仍对 trace 无偏，但数值求解与方差性质需另审计。

## 十、贯通例题：对角加低秩 Gaussian 协方差

令

$$
\Sigma=D+UU^\top,
\qquad
D=\operatorname{Diag}(e^s),
\qquad
U\in\mathbb R^{d\times r},\ r\ll d.
$$

矩阵行列式引理给

$$
\begin{aligned}
\log\det\Sigma
&=\log\det D
+\log\det(I_r+U^\top D^{-1}U)\\
&=\sum_{i=1}^d s_i
+\log\det K,
\end{aligned}
$$

其中

$$
K=I_r+U^\top D^{-1}U\succ0.
$$

计算只需：元素级 $D^{-1}$、形成 $r\times r$ 的 $K$、对 $K$ 做 Cholesky。复杂度从稠密 $O(d^3)$ 降为约 $O(dr^2+r^3)$。

若需要对 $\Sigma$ 的上游梯度 $G=\nabla_\Sigma L$，链式法则给

$$
d\Sigma=\operatorname{Diag}(e^s\odot ds)+dU\,U^\top+U\,dU^\top,
$$

所以

$$
\boxed{
\nabla_sL=e^s\odot\operatorname{diag}(G),
\qquad
\nabla_UL=(G+G^\top)U.
}
$$

若 $L$ 只依赖对称 $\Sigma$，可取 $G=G^\top$，于是 $\nabla_UL=2GU$。

## 十一、常见误区速查

| 误区 | 修正 |
|---|---|
| 奇异矩阵处 det 不可微 | det 是多项式，处处光滑；是逆式和 log-det 失效 |
| $d\det A=\det A\operatorname{tr}(A^{-1}dA)$ 对所有 $A$ 成立 | 只对可逆 $A$；通式用 adjugate |
| $\nabla_A\log|\det A|=A^{-1}$ | 一般为 $A^{-\top}$；对称时才相同 |
| 先算 $\det A$ 再取 log | 用 Cholesky/LU 的对角对数 |
| $d(A^k)=kA^{k-1}dA$ | 一般错误；取迹后循环性才合并各项 |
| $\log\det A$ 对所有实可逆矩阵有实值 | 负 det 时用 $\log|\det A|$ 或处理复分支 |
| jitter 只是数值细节 | 它改变矩阵和目标，应记录并解释 |
| flow 只要局部 det 非零就是全局双射 | 局部可逆不自动保证全局单射/满射 |
| Hutchinson 给精确 trace | 有限 probe 是随机估计，还叠加求解误差 |

## 十二、掌握检查清单

- [ ] 我能从代数余子式推出 adjugate Jacobi 公式。
- [ ] 我能区分奇异点的 det 导数与 log-det 边界。
- [ ] 我能从 $\det(I+tB)$ 解释 trace 为一阶体积变化。
- [ ] 我能正确读出 $A^{-\top}$ 而非 $A^{-1}$。
- [ ] 我知道何时写 logdet、logabsdet 与 sign。
- [ ] 我会用 Cholesky/LU 稳定计算，不先形成 det 或 inverse。
- [ ] 我能推导 $\operatorname{tr}(A^k)$ 的导数并指出非交换边界。
- [ ] 我能推导 Gaussian 协方差梯度。
- [ ] 我能解释 flow 的 log-det 与体积换元关系。
- [ ] 我能使用行列式引理处理低秩更新。
- [ ] 我知道随机 trace 估计还需误差与方差报告。

## 十三、训练入口

- 分层习题：[[习题 - 行列式、log-det 与迹的导数]]；
- 独立解答：[[解答 - 行列式、log-det 与迹的导数]]。

## 来源与延伸

1. 苏剑林，[行列式的导数](https://spaces.ac.cn/archives/2383)：代数余子式、曲线 $A(t)$ 与 $\det(I+tA)$ 一阶展开的问题入口。
2. Magnus & Neudecker, *Matrix Differential Calculus*：矩阵变量的微分与统计应用。
3. Petersen & Pedersen, *The Matrix Cookbook*：det、inverse、trace 常用公式核对手册。
4. Higham, *Functions of Matrices*：矩阵函数、矩阵对数与 Fréchet 导数的严格延伸。
5. Dinh et al., “Density Estimation using Real NVP”；Kingma & Dhariwal, “Glow”：可逆生成模型中结构化 Jacobian 与 log-det。

> [!success] 本章出口
> 你应能从“行列式等于体积”走到“trace 是相对体积的一阶变化”，再走到可计算的 Gaussian 与 flow 目标；同时知道 det 的多项式光滑性、log-det 的奇异屏障和数值分解是三个不同层次。下一步可进入[[特征值、特征向量与 SVD 的导数]]，处理谱重数与子空间的不光滑边界。
