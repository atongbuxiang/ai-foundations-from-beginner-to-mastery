---
type: concept
status: draft
area: [math/convex-analysis, math/nonsmooth-optimization, ai/regularization]
aliases: [次梯度, 次微分, 凸共轭, Fenchel 共轭, Fenchel–Young 不等式]
prerequisites: ["[[凸函数、Jensen 不等式与上图集]]", "[[凸集、凸组合与分离超平面]]", "[[线性泛函与对偶空间]]"]
related: ["[[优化与凸分析 MOC]]", "[[f-散度、Bregman 散度与概率度量]]", "[[近端算子、复合优化与稀疏正则]]", "[[弱对偶、强对偶与 Slater 条件]]"]
sources: ["MIT-6.253-Lectures-7-12", "Stanford-EE364B-Subgradients", "Boyd-Vandenberghe-2004-Ch3-Ch5", "Rockafellar-1970-Convex-Analysis", "Bubeck-2015-Convex-Optimization"]
created: 2026-08-19
updated: 2026-08-27
---

# 次梯度、共轭函数与 Fenchel 对偶

> [!abstract] 本章主问题
> 可微凸函数用唯一切平面给全局下界；不可微凸函数改用一族支撑平面，其斜率集合就是次微分。Fenchel 共轭把“一个斜率能截出多高的仿射下界”编码成新函数，Fenchel–Young 等号又把斜率、原变量和最优性连成同一张证书。它是 $ell_1$、hinge、max、entropy、dual norm、proximal method 与对偶推导的共同语言。

## 学习目标

完成本章后，你应当能够：

1. 从全局仿射下界定义 convex subgradient 与 subdifferential；
2. 区分 classical derivative、directional derivative、subgradient 与 autodiff convention；
3. 手算 $|x|$、ReLU、hinge、$ell_1$ norm、maximum 和 indicator 的次微分；
4. 解释 $partial f(x)$ 为什么 closed convex，以及它何时可能为空；
5. 使用 sum、affine precomposition 与 pointwise maximum 的次微分规则，并写出资格条件；
6. 证明 convex Fermat rule：$0\in\partial f(x^*)$ 当且仅当 $x^*$ global optimal；
7. 解释为什么任取 $g\in\partial f(x)$ 后，$-g$ 未必是函数值下降方向；
8. 定义 Fenchel conjugate，并证明其总是 convex、lower semicontinuous；
9. 手算 affine、quadratic、norm、indicator 与 negative entropy 的共轭；
10. 推导 Fenchel–Young inequality 及 equality–subgradient equivalence；
11. 解释 biconjugate $f^{**}$ 与 closed convex envelope 的关系；
12. 从 variable splitting 推导基本 Fenchel dual；
13. 区分 weak duality、zero gap、dual attainment 与 primal attainment；
14. 把 dual norm、entropy/logsumexp、sparse penalty 与 robust support function 接到 AI；
15. 审计“框架返回了一个梯度，所以函数可微”“写出 dual 就有强对偶”等错误。

> [!question] 初学者读完必须能回答
> 1. convex subgradient 为什么是对所有 $y$ 成立的全局 affine lower bound？
> 2. derivative、directional derivative、subgradient 与 autodiff 在 kink 处的 convention 有何不同？
> 3. $|x|$、ReLU、hinge、$\ell_1$ norm、maximum 与 indicator 的次微分怎样计算？
> 4. convex Fermat rule $0\in\partial f(x^*)$ 为什么等价于 global optimality？
> 5. Fenchel conjugate $f^*(y)=\sup_x\{\langle y,x\rangle-f(x)\}$ 的 slope/intercept 几何是什么？
> 6. Fenchel–Young inequality 的等号怎样等价于双向 subgradient relation？
> 7. biconjugate、closed convex envelope、weak duality、zero gap 与 attainment 为什么必须区分？

## 阅读前检查

- [[凸函数、Jensen 不等式与上图集]]：convex function 的一阶 supporting inequality；
- [[凸集、凸组合与分离超平面]]：supporting hyperplane、relative interior；
- [[线性泛函与对偶空间]]：$y^Tx$ 是 primal–dual pairing，不应默认为“两个同型向量”；
- [[f-散度、Bregman 散度与概率度量]]：已经见过一次 Fenchel variational representation，本章补齐通用机制。

> [!note] 课程位置
> OPT-03 用唯一梯度支撑可微凸函数，但真实 AI 目标常含 $\ell_1$、hinge、max、indicator 与 norm，这些函数在关键点恰好不可微。本章把“唯一切线”推广成“全部合法支撑斜率”，再把斜率搬到 dual space：subgradient 负责局部接触，conjugate 记录最佳仿射下界，Fenchel–Young equality 把 primal point 与 dual certificate 闭合。OPT-13 会在此基础上加入一般约束与强对偶条件。

> [!tip] 建议两遍阅读
> **第一遍**沿贯穿投影问题掌握 $\partial\delta_C=N_C$、Fermat rule、support function 与 Fenchel–Young equality。**第二遍**再系统计算 $|x|$、norm、entropy、biconjugate 与一般 Fenchel dual。第一次阅读只要能分清 primal variable $x$、dual slope $y$、supremum 中被消去的变量，就不要被符号淹没。

## 本章的推导问题链

1. 函数在 kink 处没有唯一 derivative 时，怎样用所有全局 affine lower bounds 保存一阶信息？
2. 为什么 constraint indicator 的次微分恰好是 feasible set 的 normal cone？
3. $0\in\partial F(x^*)$ 为什么是 convex minimization 的充要条件？
4. 固定 slope $y$ 后，最高能把仿射下界推到哪里；为什么答案由 conjugate 编码？
5. Fenchel–Young gap 为什么永远非负，等号怎样等价于双向 subgradient relation？
6. 把两个 Fenchel–Young inequalities 相加，怎样得到 primal upper value、dual lower value与零 gap 证书？

## 贯穿算例收束：normal cone 就是缺失的梯度

沿用

$$
q(x)=\frac12\|x-a\|_2^2,
\qquad
C=\operatorname{conv}\{0,e_1,e_2\},
\qquad
F(x)=q(x)+\delta_C(x),
$$

其中

$$
a=\begin{pmatrix}1\\1\end{pmatrix},
\qquad
x^*=\begin{pmatrix}1/2\\1/2\end{pmatrix},
\qquad
r=a-x^*=\begin{pmatrix}1/2\\1/2\end{pmatrix}.
$$

OPT-02 已证明 $r^T(z-x^*)\le0$ 对所有 $z\in C$ 成立。这句话现在可以压缩成

$$
r\in N_C(x^*)=\partial\delta_C(x^*).
$$

### 符号与对象账本

| 符号 | primal/dual 层 | 本例含义 | 类型检查 |
|---|---|---|---|
| $x$ | primal | 被选择的可行权重 | $\mathbb R^2$ 中的点 |
| $y$ | dual | affine lower bound 的 slope/证书 | dual pairing 中的线性泛函坐标 |
| $\partial F(x)$ | primal 点上的斜率集合 | 全部 convex subgradients | 集合，不是某个框架返回的单向量 |
| $N_C(x)$ | 几何证书 | constraint indicator 的次微分 | boundary 上可能是一条锥 |
| $q^*(y)$ | conjugate | 消去 primal $x$ 后的 slope cost | 关于 $y$ 的函数 |
| $\delta_C^*(y)=\sigma_C(y)$ | support function | $y$ 方向上 $C$ 的最大 pairing | 不是 probability support |
| $d(y)$ | dual objective | 对 primal optimum 的下界 | 与 primal objective 符号约定绑定 |

### 第一步：用 convex Fermat rule 重证最优性

在 $x^*$，

$$
\nabla q(x^*)=x^*-a=-r.
$$

又因为 $x^*$ 位于 active face $x_1+x_2=1$ 的相对内部，

$$
N_C(x^*)=\{\tau(1,1)^T:\tau\ge0\}.
$$

于是 $r\in N_C(x^*)$，从而

$$
\boxed{
0\in\nabla q(x^*)+N_C(x^*)
=\partial\bigl(q+\delta_C\bigr)(x^*)
=\partial F(x^*).
}
$$

对 proper convex $F$，这不是仅有必要性，而是 global optimality 的充要条件。这里的“0”是零向量；“$\in$”提醒我们右侧可能是一个集合。

### 第二步：手算两个 conjugates

对 indicator，

$$
\delta_C^*(y)
=\sup_{x\in C}y^Tx
=\sigma_C(y).
$$

因为 $C=\operatorname{conv}\{0,e_1,e_2\}$，线性函数最大值在顶点取得，所以

$$
\boxed{
\sigma_C(y)=\max\{0,y_1,y_2\}.
}
$$

对平方距离，令 supremum 中的一阶条件 $y-(x-a)=0$，得到 $x=a+y$，故

$$
\boxed{
q^*(y)=a^Ty+\frac12\|y\|_2^2.
}
$$

两式的输入都是 dual slope $y$，但一个编码 feasible geometry，另一个编码 quadratic curvature。

### 第三步：从 Fenchel–Young 推出 dual lower bound

Fenchel–Young 分别给

$$
q(x)+q^*(-y)\ge\langle -y,x\rangle,
$$

$$
\delta_C(x)+\delta_C^*(y)\ge\langle y,x\rangle.
$$

相加后 pairing 抵消：

$$
F(x)
\ge-q^*(-y)-\delta_C^*(y).
$$

因此一个合法 Fenchel dual 是

$$
\boxed{
\max_y d(y),
\qquad
d(y)=a^Ty-\frac12\|y\|_2^2-\max\{0,y_1,y_2\}.
}
$$

任意 $y$ 都给 $d(y)\le p^*$；这叫 weak duality，不需要先知道最优 $y$。

### 第四步：同一残差闭合零 gap

取 $y^*=r=(1/2,1/2)^T$。先算 support：

$$
\sigma_C(y^*)=\max\{0,1/2,1/2\}=\frac12
=\langle y^*,x^*\rangle.
$$

这正是 $y^*\in\partial\delta_C(x^*)$ 的 Fenchel–Young 等号。再算 dual value：

$$
\begin{aligned}
d(y^*)
&=\langle a,y^*\rangle
-\frac12\|y^*\|_2^2
-\sigma_C(y^*)\\
&=1-\frac14-\frac12\\
&=\frac14
=q(x^*)=p^*.
\end{aligned}
$$

于是 $x^*$ 给 primal value $1/4$，$y^*$ 给与它相等的 dual lower bound；两边夹住同一个数，构成可检查的最优性证书，而不只是“算法看起来收敛”。

### 核心公式七问：Fenchel–Young equality

对

$$
f(x)+f^*(y)\ge\langle y,x\rangle,
$$

逐项回答：

1. **目的：**把任意 primal point 与 dual slope 的差写成非负 certificate；
2. **对象：**$f$ 是 proper convex function，$x$ 是 primal input，$y$ 是 dual slope；
3. **来路：**由 $f^*(y)=\sup_z\{\langle y,z\rangle-f(z)\}$，把 $z=x$ 代入 supremum；
4. **步骤：**先得 $f^*(y)\ge\langle y,x\rangle-f(x)$，再移项；
5. **读法：**conjugate 至少要支付用 slope $y$ 在 $x$ 处接触 $f$ 所需的截距；
6. **检查：**等号当且仅当 $y\in\partial f(x)$，等价于 $x\in\partial f^*(y)$（在相应 closed-convex 条件下）；
7. **去路：**OPT-13 用它系统构造 Lagrange/Fenchel dual，OPT-14 用它解释 prox 与 resolvent，信息论中的 variational divergence 也依赖同一 supremum 结构。

> [!warning] 两个不能越过的边界
> 第一，autodiff 在 kink 处返回一个数，只是实现选择了某个 branch/subgradient convention，不等于函数经典可微。第二，写出一个 dual 只自动得到 weak duality；zero gap 和 primal/dual attainment 还需要 qualification。本例中 $q$ 连续且 full-domain、$\delta_C$ proper closed convex，条件足够好，所以 $y^*=r$ 能闭合 gap；不能把这个结论无条件复制到所有问题。

> [!success] 第一遍停靠线
> 不看正文，能写出 $N_C(x^*)$、验证 $0\in\nabla q(x^*)+N_C(x^*)$；能从顶点求出 $\sigma_C(y)=\max(0,y_1,y_2)$，从 completing the square 求出 $q^*(y)$，并用 $y^*=(1/2,1/2)^T$ 算出 primal value = dual value = $1/4$。若只会背 conjugate 表而说不清 supremum 中谁被优化，先回到对象账本。

## 零、从唯一切线到一束支撑线

$f(x)=|x|$ 在 $x=0$ 不可微，但所有斜率 $g\in[-1,1]$ 都满足

$$
|y|\ge |0|+g(y-0),\qquad \forall y\in\mathbb R.
$$

这些直线都从下方支撑图像。不可微不是“没有一阶信息”，而是“一阶支撑信息不唯一”。

先用下图回答一个视觉问题：**kink 处的一束支撑斜率，怎样经凸共轭变成 dual variable，并由 Fenchel–Young 等号闭合成证书？**

![[00-知识库管理/_assets/figures/optimization/fig-subgradient-conjugate-fenchel-v2.svg|880]]

> [!figure] 图 10.7.4｜次梯度束、凸共轭与 Fenchel–Young gap
> A 在 $f(x)=|x|$ 的 kink 处画出 $[-1,1]$ 内多条合法 supporting lines；B 固定 dual slope 并向上移动仿射函数，接触时的最佳截距定义 $f^*$；C 将 $f(x)+f^*(y)-\langle x,y\rangle$ 作为非负 primal-dual gap，并列出等号的次梯度条件。来源：独立绘制；生成脚本：[[plot_convex_foundations_v2.py]]；确定性结构示意，无随机种子。

**怎样读图。** A 区分“某个框架选择的 kink 梯度”与完整次微分集合；B 把 $x$ 视为 supremum 中被优化的 primal variable、$y$ 视为固定 slope；C 先检查 gap 非负，再用 $y\in\partial f(x)\Leftrightarrow x\in\partial f^*(y)$ 判定何时闭合。

**适用边界（图没有证明什么）。** 图主要展示 proper closed convex 一维直觉；边界点的次微分会包含 domain normal，非凸 generalized gradient 是另一理论；任取 $g\in\partial f(x)$ 后 $-g$ 未必保证有限步下降；写出 conjugate/dual 不自动保证强对偶、primal/dual attainment 或数值稳定。

## 一、定义：全局仿射下界

设 $f:\mathbb R^n\to\mathbb R\cup\{+\infty\}$ proper convex。向量 $g\in\mathbb R^n$ 称为 $f$ 在 $x\in\operatorname{dom}f$ 的 subgradient，若

$$
f(y)\ge f(x)+g^T(y-x),
\qquad \forall y\in\mathbb R^n.
$$

全部次梯度构成 subdifferential：

$$
\partial f(x)
=\{g:f(y)\ge f(x)+g^T(y-x),\ \forall y\}.
$$

若 $x\notin\operatorname{dom}f$，约定 $\partial f(x)=\varnothing$。

> [!important] 这是全局定义
> 普通导数描述局部线性近似；convex subgradient 的不等式对所有 $y$ 成立。正是 convexity 把局部斜率升级为 global lower certificate。

### 1.1 可微情形只是特例

若 $f$ convex 且在 $x$ differentiable，则

$$
\partial f(x)=\{\nabla f(x)\}.
$$

反过来，在 $x\in\operatorname{int}(\operatorname{dom}f)$ 等标准条件下，若 $\partial f(x)$ 是 singleton，则 $f$ 在 $x$ differentiable。边界点必须谨慎，因为 domain 的法锥会进入次微分。

### 1.2 几何解释

重写为

$$
f(y)\ge g^Ty+\bigl(f(x)-g^Tx\bigr).
$$

右侧是以 $g$ 为 slope、在 $x$ 接触 $f$ 的 affine minorant。于是 $\partial f(x)$ 是 epigraph 在 $(x,f(x))$ 处所有 nonvertical supporting hyperplanes 的 slope 集合。

## 二、为什么次微分是 closed convex set

固定 $x$，每个 $y$ 给出对 $g$ 的 closed halfspace：

$$
g^T(y-x)\le f(y)-f(x).
$$

因此

$$
\partial f(x)
=\bigcap_y
\{g:g^T(y-x)\le f(y)-f(x)\}
$$

是 closed convex set；它可以是 singleton、line segment、polytope、unbounded set 或 empty。

### 2.1 非空性不是无条件的

proper convex $f$ 在

$$
x\in\operatorname{ri}(\operatorname{dom}f)
$$

时有 $\partial f(x)\ne\varnothing$。在 domain boundary 可能为空。例如在 $[0,\infty)$ 上定义

$$
f(x)=-\sqrt{x},
$$

并在负半轴取 $+\infty$。它 convex，但在 $0$ 没有 finite slope 能全局支撑。

这解释了为什么 subdifferential calculus 常写 relative-interior qualification，而不是只写“函数凸”。

## 三、必须会手算的例子

### 3.1 绝对值

$$
\partial |x|=
\begin{cases}
\{1\},&x>0,\\
[-1,1],&x=0,\\
\{-1\},&x<0.
\end{cases}
$$

在 $0$，令 $y>0$ 得 $g\le1$；令 $y<0$ 得 $g\ge-1$。

### 3.2 ReLU 与 hinge

对 $r(x)=\max\{0,x\}$：

$$
\partial r(0)=[0,1].
$$

对 binary hinge $h(z)=\max\{0,1-z\}$：

$$
\partial h(z)=
\begin{cases}
\{-1\},&z<1,\\
[-1,0],&z=1,\\
\{0\},&z>1.
\end{cases}
$$

框架在 kink 处返回 $0$、$1/2$ 或某条 branch derivative，只是从集合中选定一个实现 convention，不证明经典可微。

### 3.3 $\ell_1$ norm

$$
\partial\|x\|_1
=\{g:g_i=\operatorname{sign}(x_i)\text{ if }x_i\ne0,
\ g_i\in[-1,1]\text{ if }x_i=0\}.
$$

零坐标保留一个区间，正是 sparsity optimality certificate 的来源。

### 3.4 Euclidean norm

$$
\partial\|x\|_2=
\begin{cases}
\left\{x/\|x\|_2\right\},&x\ne0,\\
\{g:\|g\|_2\le1\},&x=0.
\end{cases}
$$

更一般地，任意 norm 在 $x=0$ 的次微分是 dual unit ball。

### 3.5 indicator 与 normal cone

对 closed convex set $C$，定义

$$
\delta_C(x)=
\begin{cases}
0,&x\in C,\\
+\infty,&x\notin C.
\end{cases}
$$

若 $x\in C$，则

$$
\partial\delta_C(x)
=N_C(x)
=\{g:g^T(y-x)\le0,\ \forall y\in C\},
$$

即 convex normal cone。于是 constraint geometry 已被 extended-value objective 吸收。

## 四、pointwise maximum：active pieces 的凸包

令

$$
f(x)=\max_{1\le i\le m} f_i(x),
$$

各 $f_i$ convex，active set 为

$$
I(x)=\{i:f_i(x)=f(x)\}.
$$

在标准正则条件下：

$$
\partial f(x)
=\operatorname{conv}
\left(\bigcup_{i\in I(x)}\partial f_i(x)\right).
$$

若 $f_i$ differentiable：

$$
\partial f(x)=
\operatorname{conv}\{\nabla f_i(x):i\in I(x)\}.
$$

这统一了 $|x|=\max\{x,-x\}$、hinge、max-margin、worst-group risk 与 maximum eigenvalue。

## 五、次微分演算及资格条件

### 5.1 正缩放与和

对 $a>0$：

$$
\partial(af)(x)=a\partial f(x).
$$

总有弱方向

$$
\partial f(x)+\partial g(x)
\subseteq\partial(f+g)(x).
$$

要取得 equality，常用条件之一是

$$
\operatorname{ri}(\operatorname{dom}f)
\cap
\operatorname{ri}(\operatorname{dom}g)
\ne\varnothing.
$$

省略 qualification 会在边界与 extended-value functions 上制造错误。

### 5.2 affine precomposition

若 $h(x)=f(Ax+b)$，则

$$
A^T\partial f(Ax+b)
\subseteq\partial h(x).
$$

在 $A$ 与 domain 满足相应 relative-interior qualification 时取 equality。维度必须核对：$\partial f$ 在输出 dual space，$A^T$ 把 covector pull back 到输入空间。

### 5.3 directional derivative

convex directional derivative

$$
f'(x;d)
=\lim_{t\downarrow0}
\frac{f(x+td)-f(x)}t
$$

在适当有限性条件下满足

$$
f'(x;d)=
\sup_{g\in\partial f(x)}g^Td.
$$

即 directional derivative 是 subdifferential 的 support function。可微时集合退化为 singleton，恢复 $\nabla f(x)^Td$。

## 六、Fermat rule：零次梯度就是全局证书

对 proper convex $f$：

$$
x^*\in\arg\min_x f(x)
\Longleftrightarrow
0\in\partial f(x^*).
$$

证明只需代入定义：

$$
0\in\partial f(x^*)
\Longleftrightarrow
f(y)\ge f(x^*),\quad\forall y.
$$

对 composite problem

$$
\min_x\;\ell(x)+\lambda\|x\|_1,
$$

若 $\ell$ differentiable convex，则最优性为

$$
0\in\nabla\ell(x^*)+\lambda\partial\|x^*\|_1.
$$

逐坐标：

$$
x_i^*\ne0
\Rightarrow
\nabla_i\ell(x^*)=-\lambda\operatorname{sign}(x_i^*),
$$

$$
x_i^*=0
\Rightarrow
|\nabla_i\ell(x^*)|\le\lambda.
$$

零坐标不是“梯度必为零”，而是 smooth gradient 被 regularizer 的区间抵消。

## 七、警告：负次梯度未必让函数值立即下降

对 differentiable $f$，$d=-\nabla f(x)$ 给

$$
f'(x;d)=-\|\nabla f(x)\|^2<0.
$$

对 nondifferentiable convex $f$，取任意 $g\in\partial f(x)$ 后，通常不能推出

$$
f'(x;-g)<0,
$$

因为

$$
f'(x;-g)
=\sup_{h\in\partial f(x)}(-h^Tg)
$$

可能为正。例：

$$
f(x_1,x_2)=|x_1|+2|x_2|,
$$

在 kink 附近选择不合适的 subgradient，有限步可能越过折点并使目标上升。subgradient method 的证明通常控制到最优点的 distance 或 best/average objective，不要求每一步 monotone。

## 八、Fenchel 共轭：给每个斜率找最佳截距

对任意 extended-real function $f$，定义

$$
f^*(y)
=\sup_x\{y^Tx-f(x)\}.
$$

固定 $y$，若 affine function

$$
x\mapsto y^Tx-\beta
$$

要处处不高于 $f$，必须

$$
\beta\ge\sup_x(y^Tx-f(x))=f^*(y).
$$

因此 $f^*(y)$ 是 slope $y$ 对应的最小 intercept penalty，$y^Tx-f^*(y)$ 是该斜率能给出的最高 global affine lower bound。

### 8.1 共轭为什么总 convex

对每个固定 $x$，

$$
y\mapsto y^Tx-f(x)
$$

是 affine。pointwise supremum of affine functions 是 convex 且 lower semicontinuous，所以即便原 $f$ 非凸，$f^*$ 仍 closed convex。

## 九、必须会算的共轭表

### 9.1 正定二次函数

若

$$
f(x)=\frac12x^TQx,\qquad Q\succ0,
$$

最大化 $y^Tx-\frac12x^TQx$ 的 stationarity 给 $x=Q^{-1}y$，故

$$
f^*(y)=\frac12y^TQ^{-1}y.
$$

曲率在共轭中取逆：原函数陡的方向，共轭较平。

### 9.2 affine function

若 $f(x)=a^Tx+b$，则

$$
f^*(y)=
\begin{cases}
-b,&y=a,\\
+\infty,&y\ne a.
\end{cases}
$$

因为 $y-a\ne0$ 时可沿该方向把线性项送到 $+\infty$。

### 9.3 norm 与 dual ball

令 $f(x)=\|x\|$，dual norm 为 $\|y\|_*$. Hölder 给

$$
y^Tx-\|x\|
\le(\|y\|_*-1)\|x\|.
$$

因此

$$
f^*(y)=\delta_{\{\|y\|_*\le1\}}(y).
$$

反过来，dual unit ball 的 indicator 共轭为 primal norm。

### 9.4 indicator 与 support function

$$
(\delta_C)^*(y)
=\sup_{x\in C}y^Tx
=\sigma_C(y).
$$

hard constraint 在共轭侧变成 support function；集合几何与 penalty 是同一变换的两面。

### 9.5 negative entropy 与 logsumexp

在 probability simplex $\Delta_n$ 上定义

$$
f(p)=\sum_{i=1}^np_i\log p_i,
$$

在 simplex 外取 $+\infty$。对

$$
f^*(z)=\sup_{p\in\Delta_n}
\left\{z^Tp-\sum_i p_i\log p_i\right\},
$$

Lagrange stationarity 给 $p_i\propto e^{z_i}$，代回：

$$
f^*(z)=\log\sum_i e^{z_i}.
$$

于是 softmax 不是凭空出现：它是 entropy-conjugate maximizer，也是 $\nabla\operatorname{LSE}(z)$。

## 十、Fenchel–Young inequality 与等号

由 supremum 定义，对任意 $x,y$：

$$
f^*(y)\ge y^Tx-f(x),
$$

即

$$
f(x)+f^*(y)\ge y^Tx.
$$

定义 Fenchel–Young gap：

$$
\mathcal G_f(x,y)
=f(x)+f^*(y)-y^Tx
\ge0.
$$

等号等价于

$$
y^Tx-f(x)=\sup_z(y^Tz-f(z)),
$$

也就是 $x$ 达到共轭中的 supremum。整理定义得到

$$
\mathcal G_f(x,y)=0
\Longleftrightarrow
y\in\partial f(x).
$$

若 $f$ proper closed convex，还等价于

$$
x\in\partial f^*(y).
$$

所以 subgradient graph 在共轭下反转：

$$
(\partial f)^{-1}=\partial f^*.
$$

## 十一、biconjugate：从所有仿射下界重建函数

再取一次共轭：

$$
f^{**}(x)=\sup_y\{y^Tx-f^*(y)\}.
$$

每一项 $y^Tx-f^*(y)$ 都是 $f$ 的 affine lower bound，所以

$$
f^{**}\le f.
$$

Fenchel–Moreau theorem 表明：若 $f$ proper、convex、lower semicontinuous，则

$$
f^{**}=f.
$$

一般情况下，$f^{**}$ 是 $f$ 的 lower-semicontinuous convex envelope。几何上，epigraph 被闭凸包化；建模上，这可能是 relaxation，不应把 relaxed optimum 自动当成原非凸问题的精确解。

## 十二、基本 Fenchel dual 的逐行推导

考虑

$$
\min_x\; g(x)+f(Ax).
$$

引入 $z=Ax$：

$$
\min_{x,z}\;g(x)+f(z)
\quad\text{s.t.}\quad Ax-z=0.
$$

用 dual variable $y$ 构造

$$
L(x,z,y)=g(x)+f(z)+y^T(Ax-z).
$$

分别对 $x,z$ 取 infimum：

$$
\inf_x\{g(x)+(A^Ty)^Tx\}
=-g^*(-A^Ty),
$$

$$
\inf_z\{f(z)-y^Tz\}
=-f^*(y).
$$

得到 Fenchel dual：

$$
\max_y\;-g^*(-A^Ty)-f^*(y).
$$

### 12.1 weak duality 不需要强条件

任意 primal $x$ 与 dual $y$，两次 Fenchel–Young 给

$$
g(x)+g^*(-A^Ty)\ge-x^TA^Ty,
$$

$$
f(Ax)+f^*(y)\ge y^TAx.
$$

相加：

$$
g(x)+f(Ax)
\ge -g^*(-A^Ty)-f^*(y).
$$

因此每个 dual feasible value 都是 primal lower bound。

### 12.2 strong duality 需要 qualification

典型充分条件是 $f,g$ proper closed convex，并满足类似

$$
\operatorname{ri}(A\operatorname{dom}g)
\cap
\operatorname{ri}(\operatorname{dom}f)
\ne\varnothing.
$$

不同版本条件略有差异。没有 qualification，可能 positive duality gap，也可能 dual supremum 不 attained。Lagrange dual、Slater 与完整强对偶证明留给[[弱对偶、强对偶与 Slater 条件]]。

## 十三、AI 中的五个高频接口

### 13.1 sparse learning

$\ell_1$ 次微分给稀疏坐标证书；但直接 subgradient update 不等于 soft-thresholding。后者来自 proximal operator，见[[近端算子、复合优化与稀疏正则]]。

### 13.2 max-margin 与 structured prediction

hinge、maximum over labels 和 worst-case loss 的次微分来自 active configurations 的 convex hull。tie 时只反传一个 argmax 是合法 selection，但可能引入实现相关轨迹。

### 13.3 entropy、softmax 与 Fenchel–Young losses

negative entropy 与 logsumexp conjugate；softmax 是共轭最大化器。把 simplex、temperature 和 additive-shift null direction写清，才能正确解释 cross-entropy。

### 13.4 adversarial norm geometry

$$
\sup_{\|\delta\|\le\varepsilon}g^T\delta
=\varepsilon\|g\|_*.
$$

这是 indicator–support conjugacy，而不是某种只属于神经网络的技巧。FGSM 的 first-order inner problem 依赖 local linearization，非线性有限扰动仍需单独验证。

### 13.5 variational critics

$f$-divergence 的 variational lower bound来自 conjugate representation。critic class 受限、optimization 未完成和 finite samples 会使等号失效；一个较高的 lower bound 不自动等于真实 divergence。

## 十四、autodiff、finite difference 与次梯度

| 对象 | 回答的问题 | kink 处的状态 |
|---|---|---|
| classical gradient | 是否有唯一线性一阶近似？ | 通常不存在 |
| convex subdifferential | 哪些 slope 给 global affine lower bound？ | 可能是一整个集合 |
| directional derivative | 沿指定单侧方向的斜率？ | 通常存在但不对方向线性 |
| autodiff gradient | 当前程序分支规定返回什么？ | 一个 implementation selection |
| central difference | 跨越两侧后的对称差商？ | 可能给集合内部值，也可能误导 |

测试协议应同时记录数学函数、程序表达式、kink tolerance、左右方向、框架版本与所选 convention。

## 十五、常见错误与纠正

| 错误 | 为什么错 | 纠正 |
|---|---|---|
| 不可微就没有一阶信息 | convex kink 有支撑 slope 集合 | 使用 $\partial f(x)$ |
| 任意局部斜率都叫 subgradient | 定义要求全局下界 | 对所有 $y$ 验证 inequality |
| convex function 每点都有 subgradient | domain boundary 可为空 | 检查 $\operatorname{ri}(\operatorname{dom}f)$ |
| $-g$ 必使 $f$ 下降 | 非光滑 directional derivative取整个集合的 support | 次梯度法分析 distance/best iterate |
| sum rule 永远取等号 | extended domains 需要 qualification | 写 relative-interior condition |
| autodiff 返回一个值说明可微 | 程序选择不等于数学唯一性 | 分开 classical 与 implementation |
| $f^*$ 只在 $f$ convex 时定义 | 任意 extended function 都可取共轭 | 但 $f^*$ 总是 closed convex |
| $f^{**}=f$ 无条件成立 | 需 proper closed convex | 一般只得到 closed convex envelope |
| 写出 dual 就有 zero gap | 只自动得到 weak duality | 检查 qualification/attainment |
| dual variable 与 primal variable同型 | pairing 依赖空间与单位 | 明确 dual space、norm 和 $A^T$ |

## 十六、你应能独立重建的主链

$$
g\in\partial f(x)
\Longleftrightarrow
f(y)\ge f(x)+g^T(y-x),\ \forall y,
$$

$$
0\in\partial f(x^*)
\Longleftrightarrow
x^*\in\arg\min f,
$$

$$
f^*(y)=\sup_x(y^Tx-f(x)),
$$

$$
f(x)+f^*(y)-y^Tx\ge0,
$$

$$
f(x)+f^*(y)=y^Tx
\Longleftrightarrow
y\in\partial f(x)
\Longleftrightarrow
x\in\partial f^*(y),
$$

$$
f=f^{**}
\quad\text{for proper closed convex }f.
$$

## 十七、来源与证据分工

1. MIT 6.253，[Lecture Notes 7、11、12](https://ocw.mit.edu/courses/6-253-convex-analysis-and-optimization-spring-2012/pages/lecture-notes/)：conjugacy、Fenchel duality、subgradient calculus 与 qualification 的严格主线；
2. Stanford EE364B，[Subgradients](https://web.stanford.edu/class/ee364b/lectures/subgradients_slides.pdf)：次微分几何、active maximum、directional derivative 与 optimality；
3. Boyd & Vandenberghe，[Convex Optimization](https://stanford.edu/~boyd/cvxbook/)：工程建模、conjugate examples 与 duality；
4. Rockafellar，*Convex Analysis*：closed convex functions、biconjugacy 与 relative-interior 理论复核；
5. Bubeck，[Convex Optimization: Algorithms and Complexity](https://arxiv.org/abs/1405.4980)：非光滑 oracle 与后续算法复杂度接口。

> [!info] 证据纪律
> 本章给出 Fenchel dual template，但不把“formal dual 已写出”当作 zero gap 或 attainment。完整 Lagrange/Slater 证据在 OPT-13；算法性的 subgradient convergence、proximal 与 mirror updates 分别放到后续节点。

## 十八、下一步

先进入[[光滑性、强凸性与条件数]]，理解为什么有限步一阶算法需要梯度变化上界、为什么统一曲率下界能把 stationarity 变成距离与函数值证书；随后在[[一阶最优性条件与梯度下降]]中逐行推出收敛率。
