---
type: concept
status: draft
area: [math/calculus, math/matrix-calculus, math/matrix-analysis, ai/differentiable-programming]
aliases: [Differentiating Eigendecomposition and SVD, 谱分解求导, 可微 SVD, 特征分解的导数]
prerequisites: ["[[矩阵微分、迹技巧与布局约定]]", "[[逆矩阵、线性求解与隐式微分]]", "[[定理 - 有限维谱定理]]", "[[奇异值分解]]", "[[矩阵扰动]]", "[[特征向量与子空间扰动定理]]"]
related: ["[[矩阵函数的 Fréchet 导数]]", "[[非正规矩阵、预解式与伪谱]]", "[[极分解]]", "[[矩阵符号函数]]", "[[自动微分：前向、反向与高阶模式]]", "[[多元微积分、矩阵微分与自动微分 MOC]]"]
sources: ["[[S-2025-Su-10878-SVD的导数]]", "Davis-Kahan-1970", "Wedin-1972", "Townsend-2016-SVD-Derivative", "Ionescu-2015-Matrix-Backpropagation", "Higham-Functions-of-Matrices"]
exercises: ["[[习题 - 特征值、特征向量与 SVD 的导数]]"]
solutions: ["[[解答 - 特征值、特征向量与 SVD 的导数]]"]
created: 2026-08-18
updated: 2026-08-27
---

# 特征值、特征向量与 SVD 的导数

> [!abstract] 本章主问题
> 简单谱值通常可微：对称矩阵的简单特征值满足 $D\lambda_i(A)[E]=u_i^\top Eu_i$，简单正奇异值满足 $D\sigma_i(A)[E]=u_i^\top Ev_i$。方向变量的导数却含“扰动 ÷ 谱间隙”；当谱值碰撞时，单个向量失去唯一意义，应改为谱簇、投影、子空间或次梯度。非正规矩阵还要用左右特征向量，灵敏度不只由谱间隙决定。

## 学习目标

完成本章后，你应能：

1. 区分谱值、单个方向与不变子空间三种求导对象；
2. 从 $Au_i=\lambda_i u_i$ 与 $u_i^\top u_i=1$ 推导对称简单特征值导数；
3. 在规范 $u_i^\top du_i=0$ 下推导特征向量导数；
4. 解释 $(\lambda_i-\lambda_j)^{-1}$ 与有限扰动的 Davis–Kahan 界为何同源；
5. 推导一般非对称矩阵简单特征值的左右向量公式；
6. 用 $\|w_i\|\|v_i\|/|w_i^*v_i|$ 解释非正规谱敏感性；
7. 说明重复特征值处单个特征向量为何不是函数；
8. 陈述重复对称特征值的一阶分裂由压缩扰动 $U^\top EU$ 决定；
9. 用谱投影/子空间替代不具有基不变意义的逐列梯度；
10. 从 $A=U\Sigma V^\top$ 推导简单奇异值导数；
11. 解释奇异向量导数中的 $\sigma_i^2-\sigma_j^2$ 与 $1/\sigma_i$ 分母；
12. 正确处理符号、相位、排列与子空间内部旋转自由度；
13. 推导只依赖奇异值的谱函数梯度；
14. 区分谱范数/核范数的普通梯度与次梯度；
15. 审计 PCA、白化、谱归一化、低秩层和矩阵优化器的可微边界；
16. 使用残差、投影距离、方向差分和伴随测试验证实现。

> [!question] 初学者读完必须能回答
> 1. 简单特征值与特征向量的导数为何具有不同稳定性？
> 2. 特征向量导数中的谱间隙分母从哪里来？
> 3. 重复谱处为什么单个基向量不再是良好求导对象？
> 4. 谱投影和主角怎样提供基不变的子空间比较？
> 5. SVD 方向导数中的碰撞分母与零奇异值分母分别表示什么？
> 6. 非正规矩阵为什么还要检查左右特征向量条件性？

先用下图回答一个视觉问题：**为什么谱值可以平稳变化，而方向会因 gap 消失、重谱或秩变化而失去唯一导数？**

![[00-知识库管理/_assets/figures/spectral-derivatives/fig-eigen-svd-derivatives-v2.svg|880]]

> [!figure] 图 10.4.13｜简单谱、重谱子空间与 SVD 退化分母
> A 对照简单特征值公式与方向的 gap 分母；B 展示重复谱内部基可旋转而投影 $UU^\top$ 保持不变；C 区分奇异值导数与奇异向量的碰撞、零值和秩变化边界。来源：独立绘制；生成脚本：[[plot_calculus_operator_figures_v2.py]]；确定性结构示意，无随机种子。

**怎样读图。** A 先把标量谱值响应与方向响应分开；B 不再追踪圆内某一组基，而追踪整个子空间的投影；C 再定位两个不同分母：谱碰撞控制子空间内旋转，零奇异值控制与补空间的耦合。

**适用边界（图没有证明什么）。** 图以实对称矩阵和标准 SVD 为主，不代表一般非正规谱问题只由 gap 控制。它没有给出完整反向公式，也不能证明软件在排序、符号、相位和重复谱处选择的基连续。

## 进入正文前：谱值、方向与底层映射不是同一个对象

> [!info] 课程位置
> [[行列式、log-det 与迹的导数]]处理不依赖特征向量选择的体积量；本章进一步研究谱分解本身怎样变化。核心困难不在多求几次偏导，而在输出对象可能有符号、排列和子空间内部旋转自由度。下一章[[逆函数定理与隐函数定理]]会说明：谱坐标失效并不自动意味着底层映射不可逆。

> [!tip] 建议两遍阅读
> - **第一遍：** 只掌握对称简单特征值与特征向量导数、谱间隙分母，以及下面例子中“谱碰撞但线性映射仍可逆”的分层结论。
> - **第二遍：** 再读谱投影、重复谱分裂、非正规左右特征向量、SVD 补空间项、谱函数与次梯度边界。

> [!question] 本章的推导问题链
> 1. 为什么简单特征值的导数没有 gap 分母，而特征向量导数必然出现 gap？
> 2. 单个特征向量的符号和重谱内部旋转为什么会破坏普通坐标导数？
> 3. 哪些任务真正依赖逐列基，哪些只依赖投影或整个子空间？
> 4. 谱分解的坐标失效时，底层矩阵映射、逆映射和概率密度是否仍可能光滑？

### 贯穿第四波的旋转—伸缩族

定义

$$
R_\tau=
\begin{bmatrix}
\cos\tau&-\sin\tau\\
\sin\tau&\cos\tau
\end{bmatrix},
\qquad
D_\tau=
\begin{bmatrix}
2e^\tau&0\\
0&1
\end{bmatrix},
\qquad
T_\tau=R_\tau D_\tau.
$$

令

$$
A_\tau=T_\tau T_\tau^\top
=R_\tau
\begin{bmatrix}
4e^{2\tau}&0\\
0&1
\end{bmatrix}
R_\tau^\top.
$$

因此只要

$$
4e^{2\tau}\ne1,
$$

一组连续选取的特征对就是

$$
\lambda_1(\tau)=4e^{2\tau},
\quad
u_1(\tau)=R_\tau e_1,
\qquad
\lambda_2(\tau)=1,
\quad
u_2(\tau)=R_\tau e_2.
$$

在 $\tau=0$，

$$
A_0=
\begin{bmatrix}4&0\\0&1\end{bmatrix},
\qquad
\dot A_0=
\begin{bmatrix}
8&3\\
3&0
\end{bmatrix}.
$$

简单特征值公式立即给出

$$
\dot\lambda_1
=e_1^\top\dot A_0e_1=8,
\qquad
\dot\lambda_2
=e_2^\top\dot A_0e_2=0.
$$

对第一特征向量，

$$
\dot u_1
=\frac{u_2^\top\dot A_0u_1}{\lambda_1-\lambda_2}u_2
=\frac3{4-1}e_2
=e_2.
$$

这恰好等于

$$
\frac{d}{d\tau}(R_\tau e_1)\bigg|_{\tau=0}=e_2.
$$

第二方向同理满足 $\dot u_2=-e_1$。注意标量谱值只读取 $\dot A_0$ 的对角投影，而方向变化由非对角耦合除以 gap 决定。

真正重要的边界发生在

$$
\tau_*=-\log2.
$$

此时

$$
4e^{2\tau_*}=1,
\qquad
A_{\tau_*}=I.
$$

任何正交基都是 $A_{\tau_*}$ 的特征基，所以逐列 $u_i(A)$ 不再是单值对象。但

$$
T_{\tau_*}=R_{\tau_*}
$$

仍是条件数为 $1$ 的正交矩阵；失效的是谱基坐标，不是底层线性映射。

> [!note] 符号账本
> | 符号 | 类型 | 含义 |
> |---|---:|---|
> | $R_\tau$ | $2\times2$ 正交矩阵 | 随参数旋转的方向基 |
> | $D_\tau$ | $2\times2$ 正对角矩阵 | 两个主轴的伸缩 |
> | $T_\tau$ | 可逆矩阵 | 后三章使用的坐标变换 |
> | $A_\tau=T_\tau T_\tau^\top$ | SPD 矩阵 | 用于观察特征值和特征向量 |
> | $\lambda_i,u_i$ | 标量、单位向量 | 简单谱区域中的特征对 |
> | $\lambda_1-\lambda_2$ | 标量 | 控制方向可辨识性的谱间隙 |
> | $P=UU^\top$ | 投影矩阵 | 重谱时比逐列基更稳定的对象 |

> [!analysis] 对称简单特征对导数的公式七问
> | 问题 | 回答 |
> |---|---|
> | 谱值公式是什么？ | $D\lambda_i(A)[E]=u_i^\top Eu_i$；它读取扰动在当前特征方向上的 Rayleigh 分量。 |
> | 向量公式是什么？ | 在 $u_i^\top du_i=0$ 规范下，$du_i=\sum_{j\ne i}u_j\frac{u_j^\top Eu_i}{\lambda_i-\lambda_j}$。 |
> | gap 从哪里来？ | 把微分特征方程投影到其他特征方向后，要解 $(\lambda_i-\lambda_j)u_j^\top du_i=u_j^\top Eu_i$。 |
> | 为什么必须选规范？ | 单位特征向量至少有符号自由度；复数情形还有相位，自由度不固定就无法唯一谈逐列导数。 |
> | 重谱处怎么办？ | 不应继续除以零；改研究压缩扰动、谱投影、分离谱簇或具有基不变性的最终损失。 |
> | 怎样验收？ | 先查分解残差，再比较谱值方向差分；向量需先做符号/相位对齐，并随 gap 扫描误差。 |
> | AI 中怎样调用？ | PCA、白化、谱归一化、低秩层与矩阵优化器必须先声明依赖谱值、单个方向还是整个子空间。 |

> [!success] 第一遍停靠线
> 若你能从 $\dot A_0=\begin{bmatrix}8&3\\3&0\end{bmatrix}$ 算出 $\dot\lambda_1=8$ 与 $\dot u_1=e_2$，并解释为何 $\tau=-\log2$ 时特征基不可微而 $T_\tau$ 仍完全可逆，就已掌握本章主干。第一遍可暂时跳过非正规谱与完整 SVD 反向公式。

## 零、先问：你到底要对什么求导

设矩阵 $A$ 发生扰动 $A+tE$。谱分解会产生多类输出：

| 输出对象 | 是否天然唯一 | 正确比较方式 |
|---|---|---|
| 单个简单特征值/奇异值 | 排序固定且无碰撞时局部唯一 | 标量差 |
| 单个特征向量/奇异向量 | 有符号/相位自由度 | 先选连续规范，或比较一维投影 |
| 重复谱内部的一组基 | 不唯一，可任意正交旋转 | 不逐列比较 |
| 分离谱簇对应的子空间 | 基不唯一，但子空间可唯一 | 主角、投影矩阵 |
| 截断秩-$r$ 重构 | 边界有 gap 时通常稳定 | 重构/投影，而非基列 |

“`eigh` 返回了一个矩阵 $U$”不意味着 $U(A)$ 在所有点都是单值光滑函数。软件必须选择排序、符号和退化空间中的某组基，这些选择可能随微小扰动突然变化。

## 一、实对称矩阵的简单特征值

设

$$
A=A^\top=U\Lambda U^\top,
$$

并取标准化特征对

$$
Au_i=\lambda_i u_i,
\qquad
u_i^\top u_i=1.
$$

假设 $\lambda_i$ 是简单特征值，即 $\lambda_i\ne\lambda_j$ 对所有 $j\ne i$。

### 1.1 微分特征方程

对 $Au_i=\lambda_i u_i$ 微分：

$$
E u_i+A\,du_i
=d\lambda_i\,u_i+\lambda_i\,du_i.
$$

左乘 $u_i^\top$，利用 $u_i^\top A=\lambda_i u_i^\top$：

$$
u_i^\top Eu_i+\lambda_i u_i^\top du_i
=d\lambda_i+\lambda_i u_i^\top du_i.
$$

两项抵消，得到

$$
\boxed{
D\lambda_i(A)[E]=u_i^\top Eu_i.
}
$$

在对称矩阵空间的 Frobenius 内积下，

$$
u_i^\top Eu_i=\operatorname{tr}(u_iu_i^\top E),
$$

故

$$
\boxed{\nabla_A\lambda_i=u_i u_i^\top.}
$$

这是一维谱投影，而不是“特征值放在对角线相应位置”的坐标偏导。

### 1.2 规范条件来自单位长度

对 $u_i^\top u_i=1$ 微分：

$$
2u_i^\top du_i=0,
$$

所以

$$
\boxed{u_i^\top du_i=0.}
$$

即一阶变化位于 $u_i$ 的正交补中。它也固定了局部符号规范：选择与原向量内积为正的连续分支，使导数没有沿自身方向的任意分量。

### 1.3 特征向量导数

将微分方程左乘另一个特征向量 $u_j^\top$（$j\ne i$）：

$$
u_j^\top Eu_i+\lambda_j u_j^\top du_i
=\lambda_i u_j^\top du_i.
$$

所以

$$
u_j^\top du_i
=\frac{u_j^\top Eu_i}{\lambda_i-\lambda_j}.
$$

再用 $du_i$ 在标准正交基中的展开和 $u_i^\top du_i=0$：

$$
\boxed{
Du_i(A)[E]
=\sum_{j\ne i}
u_j\frac{u_j^\top Eu_i}{\lambda_i-\lambda_j}.
}
$$

方向变化由两个因素共同决定：扰动在 $u_j\leftrightarrow u_i$ 间的耦合 $u_j^\top Eu_i$，以及谱间隙 $|\lambda_i-\lambda_j|$。

### 1.4 二维例子

$$
A=\begin{bmatrix}\lambda_1&0\\0&\lambda_2\end{bmatrix},
\qquad
E=\begin{bmatrix}0&\varepsilon\\\varepsilon&0\end{bmatrix}.
$$

对 $u_1=e_1$：

$$
d\lambda_1=e_1^\top Ee_1=0,
$$

$$
du_1=e_2\frac{\varepsilon}{\lambda_1-\lambda_2}.
$$

谱值一阶不动，方向却可明显旋转；当 gap 变小，方向导数放大。这与[[矩阵扰动]]中的有限旋转角 $\theta\approx\varepsilon/\mathrm{gap}$ 完全一致。

## 二、从单个向量升级到谱投影

### 2.1 一维投影去掉符号自由度

令

$$
P_i=u_i u_i^\top.
$$

$u_i$ 换成 $-u_i$ 时 $P_i$ 不变。微分为

$$
dP_i=du_i\,u_i^\top+u_i\,du_i^\top.
$$

代入上式：

$$
\boxed{
dP_i
=\sum_{j\ne i}
\frac{u_j u_j^\top E u_i u_i^\top
+u_i u_i^\top E u_j u_j^\top}
{\lambda_i-\lambda_j}.
}
$$

该对象不受符号跳变影响，但仍需要目标特征值与其余谱分离。

### 2.2 谱簇投影

设索引集合 $I$ 对应一簇特征值，并与补集保持 gap。定义

$$
P_I=U_IU_I^\top.
$$

即使簇内部含重复值，$U_I$ 可右乘任意正交矩阵而 $P_I$ 不变。$P_I$ 的一阶变化只涉及“簇内—簇外”耦合，可写成 Sylvester 方程或 resolvent 围道积分；分母由簇间 gap 控制，不需要簇内部有间隙。

> [!important] 正确的稳定单位
> 当科学问题只关心 PCA 子空间、低秩张成空间或谱簇时，应对 $P_I$ 或子空间损失求导，不应给簇内部任意基附加逐列监督。

## 三、重复特征值：标量分支也会失去普通可微性

设对称 $A$ 有重数 $k$ 的特征值 $\lambda$，对应标准正交基 $U_0\in\mathbb R^{n\times k}$。在扰动 $A+tE$ 下，该簇的一阶分裂由小矩阵

$$
B=U_0^\top E U_0
$$

的特征值决定：

$$
\lambda_j(A+tE)=\lambda+t\,\mu_j(B)+o(t),
$$

其中 $\mu_j(B)$ 是 $B$ 的特征值（按相应顺序匹配）。

方向 $E$ 改变时，$B$ 的排序特征值不是 $E$ 的单一线性泛函。因此“第 $i$ 个排序特征值”在碰撞点通常只有方向导数，不是 Fréchet 可微。

例：$A=0_{2\times2}$，最大特征值函数满足

$$
D\lambda_{\max}(0)[E]=\lambda_{\max}(E),
$$

右侧对 $E$ 不是线性的，所以不存在普通梯度。其凸次微分为

$$
\partial\lambda_{\max}(A)
=\{U_0HU_0^\top:H\succeq0,\ \operatorname{tr}H=1\},
$$

其中 $U_0$ 张成最大特征值子空间。

## 四、一般非对称矩阵：左右特征向量

对一般实/复方阵，右、左特征向量满足

$$
Av_i=\lambda_i v_i,
\qquad
w_i^*A=\lambda_i w_i^*.
$$

假设 $\lambda_i$ 是简单特征值，且归一化为

$$
w_i^*v_i=1.
$$

微分 $Av_i=\lambda_i v_i$ 并左乘 $w_i^*$：

$$
w_i^*Ev_i+w_i^*A,dv_i
=d\lambda_i+w_i^*\lambda_i,dv_i.
$$

后两项抵消：

$$
\boxed{D\lambda_i(A)[E]=w_i^*Ev_i.}
$$

若未令 $w_i^*v_i=1$，则

$$
D\lambda_i(A)[E]
=\frac{w_i^*Ev_i}{w_i^*v_i}.
$$

### 4.1 非正规条件数

在 $\|v_i\|_2=\|w_i\|_2=1$ 的尺度下，

$$
\kappa(\lambda_i)=\frac1{|w_i^*v_i|}.
$$

若左右特征向量几乎正交，极小矩阵扰动也能显著移动特征值。正规矩阵可选 $w_i=v_i$，条件数为 $1$；非正规矩阵则可能远大于 $1$。

### 4.2 缺陷点与 exceptional point

当矩阵不可对角化、特征值发生 Jordan 合并时，特征值随扰动可能按 $t^{1/k}$ 而非 $t$ 变化。例如

$$
A(t)=\begin{bmatrix}0&1\\t&0\end{bmatrix}
$$

的特征值是 $\pm\sqrt t$。在 $t=0$ 不存在有限普通导数。此时不能用简单谱公式加一个小 $\varepsilon$ 冒充精确微分；应转向伪谱、谱投影或广义特征结构。

## 五、只依赖谱值的对称谱函数

设 $A=U\Lambda U^\top$ 对称，且

$$
F(A)=\sum_i\phi(\lambda_i)=\operatorname{tr}\phi(A).
$$

即使逐个特征向量的导数复杂，标量微分为

$$
\begin{aligned}
dF
&=\sum_i\phi'(\lambda_i)u_i^\top dA\,u_i\\
&=\operatorname{tr}\left(U\phi'(\Lambda)U^\top dA\right).
\end{aligned}
$$

所以

$$
\boxed{
\nabla_A F=U\phi'(\Lambda)U^\top=\phi'(A).
}
$$

若 $\phi$ 光滑，这个组合在重复特征值处往往仍光滑，因为相同特征值上的 $\phi'(\lambda)$ 相同，内部基旋转会抵消。例：

$$
\nabla_A\operatorname{tr}(A^2)=2A,
\qquad
\nabla_A\log\det A=A^{-1}\quad(A\succ0).
$$

这说明“分解因子不唯一”不必然导致所有下游标量都不可微；关键是下游函数是否对规范变换不变。

## 六、SVD 的简单奇异值导数

设实矩阵

$$
A=U\Sigma V^\top,
$$

并取奇异三元组

$$
Av_i=\sigma_i u_i,
\qquad
A^\top u_i=\sigma_i v_i,
\qquad
\|u_i\|=\|v_i\|=1.
$$

假设 $\sigma_i>0$ 且简单。

### 6.1 推导 $d\sigma_i$

对 $Av_i=\sigma_i u_i$ 微分：

$$
Ev_i+A\,dv_i=d\sigma_i\,u_i+\sigma_i\,du_i.
$$

左乘 $u_i^\top$：

$$
u_i^\top Ev_i+u_i^\top A\,dv_i
=d\sigma_i+\sigma_i u_i^\top du_i.
$$

由 $u_i^\top A=\sigma_i v_i^\top$，且单位约束给 $v_i^\top dv_i=u_i^\top du_i=0$，故

$$
\boxed{D\sigma_i(A)[E]=u_i^\top Ev_i.}
$$

因此

$$
\boxed{\nabla_A\sigma_i=u_iv_i^\top.}
$$

这与科学空间《SVD的导数》的主线一致；课程额外保留简单、正奇异值与规范选择条件。

### 6.2 通过对称增广矩阵理解

定义

$$
\mathcal A=
\begin{bmatrix}0&A\\A^\top&0\end{bmatrix}.
$$

若 $(u_i,v_i,\sigma_i)$ 是奇异三元组，则

$$
\mathcal A\frac1{\sqrt2}\begin{bmatrix}u_i\\v_i\end{bmatrix}
=\sigma_i\frac1{\sqrt2}\begin{bmatrix}u_i\\v_i\end{bmatrix}.
$$

$-\sigma_i$ 也对应 $[u_i;-v_i]/\sqrt2$。因此 SVD 导数可视为对称特征分解导数的一种结构化特例；奇异值碰撞和零值问题对应增广矩阵的谱碰撞。

## 七、奇异向量导数：分母从哪里来

先考虑实方阵、满秩、正奇异值两两不同。微分

$$
A=U\Sigma V^\top
$$

并左乘 $U^\top$、右乘 $V$。记

$$
P=U^\top E V,
\qquad
\Omega_U=U^\top dU,
\qquad
\Omega_V=V^\top dV.
$$

由正交约束，$\Omega_U,\Omega_V$ 都是反对称矩阵。得到

$$
P=\Omega_U\Sigma+d\Sigma-\Sigma\Omega_V.
$$

对角项立刻给

$$
d\sigma_i=P_{ii}=u_i^\top Ev_i.
$$

对 $i\ne j$，令 $\alpha=(\Omega_U)_{ij}$、$\beta=(\Omega_V)_{ij}$：

$$
\begin{bmatrix}
\sigma_j&-\sigma_i\\
-\sigma_i&\sigma_j
\end{bmatrix}
\begin{bmatrix}\alpha\\\beta\end{bmatrix}
=
\begin{bmatrix}P_{ij}\\P_{ji}\end{bmatrix}.
$$

当 $\sigma_i\ne\sigma_j$ 时，

$$
\boxed{
(\Omega_U)_{ij}
=\frac{\sigma_jP_{ij}+\sigma_iP_{ji}}
{\sigma_j^2-\sigma_i^2},
}
$$

$$
\boxed{
(\Omega_V)_{ij}
=\frac{\sigma_iP_{ij}+\sigma_jP_{ji}}
{\sigma_j^2-\sigma_i^2}.
}
$$

分母 $\sigma_j^2-\sigma_i^2$ 来自必须同时满足左右奇异方程与两个正交约束。接近碰撞时，奇异向量导数变大。

### 7.1 矩形矩阵的补空间项

紧致 SVD 只给出列空间中的旋转。若 $A\in\mathbb R^{m\times n}$ 为秩 $r$，$u_i$ 在 $\operatorname{span}(U_r)^\perp$ 的变化还含

$$
(I-U_rU_r^\top)du_i
=\frac{(I-U_rU_r^\top)Ev_i}{\sigma_i},
$$

右侧类似：

$$
(I-V_rV_r^\top)dv_i
=\frac{(I-V_rV_r^\top)E^\top u_i}{\sigma_i}.
$$

因此接近零奇异值时，即使正奇异值之间有间隙，方向导数也可能因 $1/\sigma_i$ 放大。秩变化处紧致 SVD 的输出维数本身改变，普通固定形状导数模型失效。

## 八、符号、相位、排列与规范不变性

### 8.1 符号与相位

实 SVD 中

$$
(u_i,v_i)\mapsto(-u_i,-v_i)
$$

不改变 $\sigma_i u_iv_i^\top$。复数中可同时乘相反相位。若损失直接惩罚 $u_i$ 与某固定向量的欧氏差，符号翻转会制造假不连续；应改为投影损失或先对齐规范。

### 8.2 排列

软件通常按 $\sigma_1\ge\cdots$ 排序。碰撞时排序分支交换，所以逐索引输出可能不光滑。若只需要一簇低秩空间，应使用簇投影；若需要谱值的对称函数，应直接构造排列不变目标。

### 8.3 重复奇异值

若一簇奇异值相同，$U_I,V_I$ 可同时右乘同一个正交矩阵 $R$：

$$
U_I\Sigma_I V_I^\top
=(U_IR)\Sigma_I(V_IR)^\top.
$$

逐列奇异向量不是唯一函数；而左右子空间投影 $U_IU_I^\top$、$V_IV_I^\top$ 仍可在簇与外部谱分离时平滑变化。

## 九、只依赖奇异值的函数

设

$$
F(A)=\sum_i\phi(\sigma_i(A)),
$$

且所在点满足使组合可微的条件。则

$$
dF=\sum_i\phi'(\sigma_i)u_i^\top dA\,v_i,
$$

所以

$$
\boxed{
\nabla_AF=U\operatorname{Diag}(\phi'(\sigma_i))V^\top.
}
$$

例：

- $F(A)=\frac12\|A\|_F^2=\frac12\sum_i\sigma_i^2$，梯度为 $A$；
- Schatten-$p$ 的 $p$ 次幂 $\frac1p\sum_i\sigma_i^p$（$p>1$）梯度为 $U\operatorname{Diag}(\sigma_i^{p-1})V^\top$；
- 满秩方阵的 $\log|\det A|=\sum_i\log\sigma_i$，极分解意义下梯度等价于 $A^{-\top}$。

组合对符号、相位和同值子空间旋转不变，往往比直接依赖 $U,V$ 更平滑。

## 十、谱范数与核范数：何时只有次梯度

### 10.1 谱范数

$$
\|A\|_2=\sigma_1(A).
$$

若 $\sigma_1>\sigma_2$，

$$
\boxed{\nabla_A\|A\|_2=u_1v_1^\top.}
$$

若最大奇异值重数为 $k$，普通梯度一般不存在；次微分为

$$
\partial\|A\|_2
=\{U_1HV_1^\top:H\succeq0,\operatorname{tr}H=1\}.
$$

### 10.2 核范数

若紧致 SVD 为 $A=U_r\Sigma_rV_r^\top$，则

$$
\partial\|A\|_*
=\{U_rV_r^\top+W:
U_r^\top W=0,\ WV_r=0,\ \|W\|_2\le1\}.
$$

满秩且相关维数消除零奇异子空间时，次梯度可能唯一；秩亏点通常不光滑。自动微分框架返回的某个值只是约定选择，不能升级成处处 Fréchet 可微。

## 十一、AI 应用与失败边界

### 11.1 PCA 与表示子空间

协方差 $C=X^\top X/B$ 的前 $r$ 个特征向量定义 PCA 子空间。若 $\lambda_r>\lambda_{r+1}$，前 $r$ 维投影对扰动稳定；内部特征值重复不影响整体子空间。损失应作用于 $P=U_rU_r^\top$ 或重构 $XP$，而非逐列基。

### 11.2 白化与逆平方根

$$
C^{-1/2}=U\Lambda^{-1/2}U^\top.
$$

小特征值通过 $\lambda^{-1/2}$ 和其导数 $-\frac12\lambda^{-3/2}$ 放大噪声。jitter $C+\varepsilon I$ 改变模型并设置最小尺度；必须报告 $\varepsilon$ 与敏感性。

### 11.3 谱归一化

$$
\widehat W=\frac{W}{\sigma_1(W)}.
$$

若 $\sigma_1$ 简单，可用 $u_1v_1^\top$；实践常用有限次幂迭代，所以训练程序实际求导对象还包含近似方向、状态更新与 stop-gradient 选择。最大奇异值碰撞时普通梯度不唯一。

### 11.4 低秩截断

最佳秩-$r$ 近似

$$
A_r=U_r\Sigma_rV_r^\top
$$

在边界 $\sigma_r=\sigma_{r+1}$ 处不唯一。若 gap 明确，截断映射局部平滑；gap 消失时选择哪个 $r$ 维方向会跳变。

### 11.5 Muon、极分解与正交化

极因子 $UV^\top$ 对奇异向量的联合符号/旋转不变，并可通过极分解的 Sylvester 方程求导；它可能比单独 $U,V$ 更稳定。但秩亏、接近零奇异值仍是边界，见[[极分解]]和[[矩阵函数的 Fréchet 导数]]。

## 十二、验证协议

### 12.1 分解残差先于梯度

检查

$$
\|Av_i-\lambda_iv_i\|,
\qquad
\|Av_i-\sigma_i u_i\|,
\qquad
\|A^\top u_i-\sigma_i v_i\|,
$$

以及正交性和重构误差。前向分解不准确时，梯度公式没有可靠基点。

### 12.2 标量谱值方向差分

对简单谱值比较

$$
\frac{\lambda_i(A+hE)-\lambda_i(A-hE)}{2h}
$$

与 $u_i^\top Eu_i$；SVD 类似。必须跟踪同一分支，不能只按索引盲目匹配接近碰撞的输出。

### 12.3 向量应先对齐

简单实向量可把新向量符号调整为与基准内积为正；复数需对齐相位。重谱时使用投影差

$$
\|\widehat U\widehat U^\top-UU^\top\|
$$

或主角，不能逐列差。

### 12.4 扫描谱间隙

固定扰动大小，系统扫描 gap，记录方向导数范数、投影变化、有限差分误差和框架 backward 的 NaN/警告。只在 gap 很大的随机矩阵上测试，会错过核心失败边界。

### 12.5 规范不变性测试

对重复子空间内随机旋转 $R$，检查下游损失是否满足

$$
L(U_I,V_I)=L(U_IR,V_IR).
$$

若不满足，模型正在学习一个数值算法任意选择的基，而非矩阵本身的可识别属性。

## 十三、贯通例题：可微 PCA 重构损失

设对称协方差 $C(\theta)$ 的前 $r$ 个特征值与其余谱分离，$U_r$ 是任一正交基，投影

$$
P=U_rU_r^\top.
$$

定义

$$
L=\frac12\|X-XP\|_F^2.
$$

虽然 $U_r$ 在内部重根时可旋转，$P$ 与 $L$ 不变。对 $P$ 的环境梯度可由矩阵微分得到；对 $C$ 的梯度则通过谱投影导数的伴随求得，其条件性由簇间

$$
\delta=\lambda_r-\lambda_{r+1}>0
$$

控制，而不要求 $\lambda_1,\ldots,\lambda_r$ 彼此不同。若改成逐列监督

$$
\sum_{i=1}^r\|u_i-q_i\|^2,
$$

内部重根时目标依赖任意基选择，数学上不可识别，训练中也会出现跳变。

## 十四、常见误区速查

| 误区 | 修正 |
|---|---|
| 对称矩阵所有特征向量都可微 | 需要简单谱或改为分离谱簇的投影 |
| 特征向量符号跳变说明子空间跳变 | 一维投影可能完全不变 |
| 重复谱只需在分母加 $\varepsilon$ | 这改变导数且未解决对象不唯一 |
| 一般矩阵也用 $u^\top Eu$ | 非正规问题需左右特征向量 $w^*Ev$ |
| 特征值间隔大就保证一般矩阵稳定 | 非正规性/左右向量夹角也关键 |
| SVD 只有 $\sigma_i^2-\sigma_j^2$ 边界 | 矩形/秩亏还出现 $1/\sigma_i$ 与维数变化 |
| 框架返回 backward 就等于处处可微 | 退化点可能是约定值、NaN 或近似 |
| PCA 应逐列对齐特征向量 | 应比较子空间投影或主角 |

## 十五、掌握检查清单

- [ ] 我能推导对称简单特征值与特征向量的一阶公式。
- [ ] 我能解释规范条件 $u_i^\top du_i=0$。
- [ ] 我能把 gap 分母与 Davis–Kahan/Wedin 联系起来。
- [ ] 我知道重复谱的一阶分裂由压缩扰动决定。
- [ ] 我能为非正规矩阵使用左右特征向量。
- [ ] 我能推导简单奇异值导数。
- [ ] 我理解 SVD 内部旋转、符号和排列自由度。
- [ ] 我会用投影/子空间替代退化点逐列梯度。
- [ ] 我能判断谱范数与核范数何时只有次梯度。
- [ ] 我会扫描 gap、对齐规范并验证前向残差。
- [ ] 我能审计 PCA、白化、谱归一化和低秩截断的边界。

## 十六、训练入口

- 分层习题：[[习题 - 特征值、特征向量与 SVD 的导数]]；
- 独立解答：[[解答 - 特征值、特征向量与 SVD 的导数]]。

## 来源与延伸

1. 苏剑林，[SVD的导数](https://www.spaces.ac.cn/archives/10878)：SVD 恒等式微分、奇异方向和反向梯度的问题入口；见本地来源卡[[S-2025-Su-10878-SVD的导数]]。
2. Davis & Kahan；Wedin：Hermitian 与奇异子空间扰动、gap 边界的经典来源。
3. Townsend, *Differentiating the Singular Value Decomposition*：SVD 微分的紧凑推导。
4. Ionescu et al., “Matrix Backpropagation for Deep Networks with Structured Layers”：特征/SVD 等结构层反向传播。
5. Higham, *Functions of Matrices*：谱函数、Fréchet 导数与退化结构。

> [!success] 本章出口
> 应形成条件反射：先问输出是否对符号、相位、排列和子空间换基不变，再决定能否谈普通导数；简单谱用标量/向量公式，重复谱用压缩扰动、谱投影或次梯度，非正规谱还要审计左右向量条件数。下一章用逆函数与隐函数定理说明这些“局部可微分支”究竟在什么条件下存在。
