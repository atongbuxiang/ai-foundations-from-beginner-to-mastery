---
type: concept
status: draft
area: [math/functional-analysis, math/pde, math/numerical-analysis, ai/scientific-machine-learning, ai/neural-operators]
aliases: [弱导数与 Sobolev 空间, 变分形式与神经算子, Weak Derivatives and Sobolev Spaces]
prerequisites: ["[[Banach 空间、Hilbert 空间与正交投影]]", "[[有界算子、紧算子与谱理论基础]]", "[[函数极限、连续性与收敛模式]]", "[[连续性方程与守恒律]]"]
related: ["[[几何、泛函分析、核与算子基础 MOC]]", "[[正定核、RKHS 与表示定理]]", "[[习题 - 弱导数、Sobolev 空间与神经算子接口]]", "[[解答 - 弱导数、Sobolev 空间与神经算子接口]]", "[[实验 - 弱导数、变分残差与解算子频谱审计]]", "[[S-2014-Su-3092-格林函数与线性响应]]"]
sources: ["MIT-18.155-Sobolev", "MIT-18.102-Functional-Analysis", "Evans-2010-PDE", "Adams-Fournier-2003-Sobolev", "MIT-FE-Introduction", "Lu-et-al-2021-DeepONet", "Li-et-al-2021-FNO", "Kovachki-et-al-2023-Neural-Operator", "Raissi-et-al-2019-PINN", "E-Yu-2018-Deep-Ritz", "Khodayi-Mehr-Zavlanos-2020-VarNet", "Czarnecki-et-al-2017-Sobolev-Training", "Su-3092-Green-Function"]
created: 2026-08-19
updated: 2026-08-23
---

# 弱导数、Sobolev 空间与神经算子接口

> [!abstract] 本章主问题
> 经典微积分要求函数在每一点都足够光滑，但偏微分方程的真实解、有限元近似和 ReLU 网络经常在某些点不可微。**弱导数**把导数从“逐点极限”改写为“对所有测试函数成立的积分恒等式”；**Sobolev 空间**则用弱导数的可积性衡量函数的整体正则性。这样，Poisson 方程可在 $H_0^1$ 中写成良定的变分问题，Galerkin 方法、Deep Ritz、变分 PINN 与神经算子也能放进同一张对象—拓扑—误差地图。本章不把“残差很小”“训练损失很低”“换网格能运行”误写成“已经逼近真实解算子”。

> [!question] 初学者读完必须能回答
> 1. 为什么把导数移到测试函数上，就能给 $|x|$、阶跃函数或分片线性函数定义分布导数？
> 2. 分布导数与弱导数有什么差别？为什么 $H'=\delta_0$ 意味着 Heaviside 函数不属于 $W^{1,p}$？
> 3. $W^{k,p}$、$H^k$、$H_0^1$、$H^{-1}$ 分别控制什么？边界值为什么需要 trace theorem？
> 4. Poincaré、Sobolev embedding、Rellich compactness 的假设和结论各是什么？哪些边界情况不能偷换？
> 5. $-\Delta u=f$ 怎样从强形式变成弱形式？Lax–Milgram 为什么给出存在唯一性？
> 6. 能量最小化、弱形式与 Galerkin 离散何时等价？Céa 引理把数值误差归结为什么？
> 7. 为什么分片线性有限元的逐单元二阶强残差可能很差，但有限元弱残差恰好为零？
> 8. PINN、Deep Ritz、VPINN/VarNet 各自最小化哪个对象，需要网络有几阶导数？
> 9. 单个 PDE 解 $u_\theta(x)$ 与解算子 $\mathcal G:a\mapsto u$ 有什么根本区别？
> 10. DeepONet/FNO 的通用逼近、参数跨网格共享和实际的分辨率泛化为什么是三件事？

先用下图回答一个视觉问题：**逐点导数失效后怎样保留微分结构，Sobolev 空间如何编码正则与边界，而从一个弱 PDE 到“学到解算子”还隔着哪些验收层？**

![[00-知识库管理/_assets/figures/functional-analysis/fig-weak-sobolev-variational-operator-v2.svg|880]]

> [!figure] 图 10.10.8｜Weak derivative、Sobolev contracts 与 neural operators
> A 以 $u(x)=|x|$ 的 kink 与 $u'=\operatorname{sign}(x)$ a.e. 示意，把 derivative 从 pointwise limit 改写为对所有 test functions 成立的 integration-by-parts identity；B 从 $W^{k,p}$ norm 连接 embedding、trace、Poincaré 与 compactness，并把 dimension、exponents 与 domain regularity 标为不可省条件；C 串联 input coefficient space、weak problem、well-posed solution map $\mathcal G:X\to Y$、discretization/learning 与 norm-based tests。来源：独立绘制；理论接口参考 distributions、Sobolev spaces、variational PDE、Galerkin theory 与 neural operators；生成脚本：[[plot_functional_analysis_v2.py]]；确定性结构示意，无随机种子。

**怎样读图。** A 先将 $D^\alpha$ 从粗糙 $u$ 转移到光滑 compactly supported test function，并用“对所有 tests”确定 weak derivative；B 再明确每个 theorem 的完整合同，尤其是空间维数、指数、domain boundedness/regularity 与 boundary trace；C 最后从单个 solution 升到 solution operator，先证明 input-to-solution map well posed，再分开 data、discretization、model、optimization 与 solver errors，并在目标 function-space norm 中验收。

**适用边界（图没有证明什么）。** 折线只说明 $|x|$ 的弱一阶导数，不覆盖 Heaviside 的 delta distribution 或 higher-order singularities；weak derivative、weak convergence 与 weak PDE formulation 不是同义词。Embedding/trace/Rellich/Poincaré 均有条件与临界例外。低 collocation/variational residual、共享网络参数或在新网格上可运行，都不单独证明 continuum operator approximation、resolution convergence 或 out-of-distribution generalization。

## 0. 对象合同与学习路线

### 0.1 基本约定

- $\Omega\subset\mathbb R^d$ 是开集；涉及 trace、Poincaré 或紧嵌入时会额外要求 $\Omega$ 有界、连通或具有 Lipschitz 边界；
- $L^p(\Omega)$ 的元素是“几乎处处相等”的等价类，不是预先带有每点取值的连续函数；
- 多重指标 $\alpha=(\alpha_1,\ldots,\alpha_d)$，$|\alpha|=\sum_i\alpha_i$，$D^\alpha=\partial_1^{\alpha_1}\cdots\partial_d^{\alpha_d}$；
- $C_c^\infty(\Omega)$ 是支集紧含于 $\Omega$ 的光滑测试函数空间；$\mathcal D'(\Omega)$ 是 distributions；
- $1\le p\le\infty$，$p'$ 表示 Hölder 共轭指数：$1/p+1/p'=1$；
- 内积与弱形式先写实数情形；复数情形需加入共轭；
- “弱”可能指 weak derivative、weak PDE formulation 或 weak convergence，三者相关但不是一个概念。

### 0.2 四层对象不能混写

| 层 | 典型对象 | 比较标准 | 典型问题 |
|---|---|---|---|
| 点态/经典层 | $C^1,C^2$ 函数 | 每一点导数、PDE 残差 | 经典解是否存在？ |
| 分布层 | $\mathcal D'(\Omega)$ | 对所有测试函数的作用 | 跳跃或奇性怎样被微分？ |
| Sobolev/变分层 | $W^{k,p},H_0^1,H^{-1}$ | 范数、弱收敛、双线性型 | 弱解是否存在、唯一、稳定？ |
| 算子学习层 | $\mathcal G:X\to Y$ | 输入/输出函数空间上的误差 | 是否学到一族问题的解映射？ |

本章的主线是

$$
\text{integration by parts}
\Longrightarrow \text{distributional derivative}
\Longrightarrow W^{k,p}
\Longrightarrow \text{weak PDE}
\Longrightarrow \text{Galerkin / neural solver / neural operator}.
$$

## 1. 为什么经典导数不够

### 1.1 三类不可避免的非光滑对象

1. **方程本身产生奇性。** 不连续系数、角点区域、冲击波和点源都可能让经典二阶导数不存在；
2. **数值空间主动使用低正则函数。** 线性有限元只要求跨单元连续，梯度可在单元界面跳跃；
3. **神经网络也可能分片光滑。** ReLU 网络在激活超平面上不可经典微分，二阶分布导数集中在这些界面上。

若理论只允许 $C^2$ 解，就会把大量稳定、可计算而且物理合理的解排除在外。

### 1.2 分部积分揭示真正可保留的结构

若 $u\in C^1(\Omega)$，$\varphi\in C_c^\infty(\Omega)$，则测试函数在边界附近为零，所以

$$
\int_\Omega \partial_i u(x)\varphi(x)\,dx
=-\int_\Omega u(x)\partial_i\varphi(x)\,dx.
$$

右端只要求 $u$ 局部可积；这提示我们把右式当成导数的定义。关键不是“把不可微点忽略掉”，而是用**对所有测试函数成立的恒等式**保存导数的整体作用。

## 2. 测试函数、分布与弱导数

### 2.1 局部可积函数诱导分布

每个 $u\in L^1_{\mathrm{loc}}(\Omega)$ 定义 regular distribution

$$
T_u(\varphi)=\int_\Omega u(x)\varphi(x)\,dx,
\qquad \varphi\in C_c^\infty(\Omega).
$$

一般 distribution 是 $C_c^\infty(\Omega)$ 上满足适当连续性的线性泛函。Dirac delta

$$
\delta_{x_0}(\varphi)=\varphi(x_0)
$$

不是由普通 $L^1_{\rm loc}$ 函数诱导的，却是合法分布。

> [!definition] 分布导数
> 对 $T\in\mathcal D'(\Omega)$，定义
> $$
> \langle D^\alpha T,\varphi\rangle
> =(-1)^{|\alpha|}\langle T,D^\alpha\varphi\rangle.
> $$
> 因为测试函数可以被任意次微分，每个分布都拥有任意阶分布导数。

> [!definition] 弱导数
> 若 $u\in L^1_{\rm loc}(\Omega)$，并存在 $v\in L^1_{\rm loc}(\Omega)$ 使
> $$
> \int_\Omega v\varphi
> =(-1)^{|\alpha|}\int_\Omega uD^\alpha\varphi
> \quad\forall\varphi\in C_c^\infty(\Omega),
> $$
> 则称 $v$ 是 $u$ 的 $\alpha$ 阶弱导数，写作 $D^\alpha u=v$。

区别在于：分布导数总存在，但它未必还能由局部可积函数表示；只有能由函数表示时，才是 Sobolev 意义下的弱导数。

### 2.2 例一：$u(x)=|x|$

在 $(-1,1)$ 上，对任意测试函数 $\varphi$，分段积分得

$$
-\int_{-1}^1|x|\varphi'(x)\,dx
=\int_{-1}^0(-1)\varphi(x)\,dx+\int_0^1(1)\varphi(x)\,dx.
$$

因此

$$
u'(x)=\operatorname{sign}(x)\quad\text{a.e.}
$$

$x=0$ 的取值不影响 $L^p$ 等价类，所以 $|x|\in W^{1,\infty}(-1,1)$。再微分一次却得到

$$
D^2|x|=2\delta_0,
$$

不是普通函数，故 $|x|\notin W^{2,p}(-1,1)$ 对所有 $1\le p\le\infty$。

### 2.3 例二：Heaviside 跳跃与 ReLU

令 $H(x)=\mathbf1_{(0,\infty)}(x)$，则

$$
\langle H',\varphi\rangle
=-\int_0^\infty\varphi'(x)\,dx
=\varphi(0)=\langle\delta_0,\varphi\rangle.
$$

所以 $H'=\delta_0$。在包含 $0$ 的区间上，$H$ 不属于 $W^{1,p}$：它的分布导数不是 $L^p$ 函数。另一方面，$\operatorname{ReLU}(x)=x_+$ 满足

$$
D(x_+)=H\quad\text{a.e.},\qquad D^2(x_+)=\delta_0.
$$

因此 ReLU 属于局部 $W^{1,\infty}$，但不属于局部 $W^{2,p}$。这会直接影响要求二阶强残差的 PDE loss。

### 2.4 唯一性、乘积法则与链式法则

若 $v,w\in L^1_{\rm loc}$ 都代表 $u$ 的同一个弱导数，则

$$
\int(v-w)\varphi=0\quad\forall\varphi\in C_c^\infty
$$

由分布的基本引理知 $v=w$ a.e.，所以弱导数作为等价类唯一。

在条件充分时，经典规则仍成立。例如 $u\in W^{1,p}$、$\eta\in C^1$ 且 $\eta'$ 有界，则

$$
\nabla(\eta\circ u)=\eta'(u)\nabla u\quad\text{a.e.}
$$

若 $u\in W^{1,p}$、$\psi\in C^1$ 且 $\psi,\nabla\psi$ 有界，则

$$
\nabla(\psi u)=\psi\nabla u+u\nabla\psi.
$$

> [!warning] 不要无条件复制经典规则
> 对非 Lipschitz 外函数、低可积性乘积或 distribution 与 distribution 的乘积，表达式可能没有定义。弱导数扩展了微分，却没有自动建立任意非线性运算。

## 3. Sobolev 空间：以可积弱导数度量正则性

### 3.1 整数阶定义

> [!definition] $W^{k,p}(\Omega)$
> $$
> W^{k,p}(\Omega)
> =\{u\in L^p(\Omega):D^\alpha u\in L^p(\Omega),\ |\alpha|\le k\}.
> $$
> 当 $1\le p<\infty$，常用范数
> $$
> \|u\|_{W^{k,p}}
> =\left(\sum_{|\alpha|\le k}\|D^\alpha u\|_{L^p}^p\right)^{1/p};
> $$
> $p=\infty$ 时取最大值。只含 $|\alpha|=k$ 的部分称为 seminorm $|u|_{W^{k,p}}$。

$W^{k,p}$ 是 Banach space；$p=2$ 时写 $H^k=W^{k,2}$，内积

$$
\langle u,v\rangle_{H^k}
=\sum_{|\alpha|\le k}\int_\Omega D^\alpha uD^\alpha v
$$

使其成为 Hilbert space。这里的“正则”是整体积分意义，不保证每一点都有经典导数。

### 3.2 Mollifier：为什么光滑函数仍然是核心工具

取 $\rho\in C_c^\infty(\mathbb R^d)$，$\rho\ge0$，$\int\rho=1$，令

$$
\rho_\varepsilon(x)=\varepsilon^{-d}\rho(x/\varepsilon),
\qquad u_\varepsilon=\rho_\varepsilon*u.
$$

在远离边界的子域上，$u_\varepsilon\in C^\infty$，且

$$
D^\alpha u_\varepsilon=\rho_\varepsilon*D^\alpha u.
$$

因此可用光滑近似证明 Sobolev 定理。对一般开集，$C^\infty(\Omega)\cap W^{k,p}$ 在 $W^{k,p}(\Omega)$ 中通常稠密；但

$$
W_0^{k,p}(\Omega):=\overline{C_c^\infty(\Omega)}^{\,W^{k,p}}
$$

是带零边界条件的子空间，不能把“$C_c^\infty$ 在 $W^{k,p}$ 中总稠密”当成无条件结论。

### 3.3 Fractional 与 negative spaces

在 $\mathbb R^d$ 上可用 Fourier transform 定义

$$
\|u\|_{H^s(\mathbb R^d)}^2
=\int_{\mathbb R^d}(1+|\xi|^2)^s|\widehat u(\xi)|^2\,d\xi,
\qquad s\in\mathbb R.
$$

$s>0$ 惩罚高频；$s<0$ 容许更奇异对象。对 $V=H_0^1(\Omega)$，其 continuous dual 记为

$$
H^{-1}(\Omega)=V^*.
$$

若 $f\in H^{-1}$，$\langle f,v\rangle_{H^{-1},H_0^1}$ 仍有意义，即使 $f$ 不是逐点定义的普通函数。这正是点源、粗糙 forcing 与弱 PDE 的自然语言。

## 4. 边界、Poincaré 与嵌入：每个定理都带条件

### 4.1 Trace：$L^p$ 等价类如何谈边界值

边界 $\partial\Omega$ 在 $d$ 维 Lebesgue measure 下通常为零；任意改变边界上的逐点值不会改变 $L^p$ 元素。因此“令 $u=0$ on $\partial\Omega$”不能仅靠选一个代表元定义。

对 Lipschitz domain，存在连续 trace operator

$$
\operatorname{Tr}:W^{1,p}(\Omega)\to L^p(\partial\Omega)
$$

（更精确的像空间是 fractional boundary space），并与光滑函数的边界限制一致。在常用条件下

$$
W_0^{1,p}(\Omega)=\ker(\operatorname{Tr}).
$$

所以 $H_0^1$ 中的“零边界”是 closure/trace 意义的 essential boundary condition。

### 4.2 Poincaré–Friedrichs inequality

若 $\Omega$ 是适当的有界连通区域，则对 $u\in W_0^{1,p}(\Omega)$，

$$
\|u\|_{L^p}\le C_P\|\nabla u\|_{L^p}.
$$

于是 $\|\nabla u\|_{L^2}$ 在 $H_0^1$ 上是与完整 $H^1$ 范数等价的 norm。若没有零 trace，则常数函数让右端为零；需改为

$$
\|u-u_\Omega\|_{L^p}\le C\|\nabla u\|_{L^p}.
$$

### 4.3 Sobolev embedding 的维数阈值

在有界且足够规则的区域，$W^{1,p}$ 的典型结论为：

| 条件 | 典型连续嵌入 | 不能误读为 |
|---|---|---|
| $1\le p<d$ | $W^{1,p}\hookrightarrow L^{p^*}$，$p^*=dp/(d-p)$ | 自动连续或有界 |
| $p=d$ | 嵌入每个有限 $L^q$（常数依赖 $q$） | 一般嵌入 $L^\infty$ |
| $p>d$ | 嵌入 Hölder $C^{0,\alpha}$，$\alpha=1-d/p$（端点需谨慎表述） | 任意更高 Hölder 正则 |

在 $\mathbb R^d$ 上，Fourier Cauchy–Schwarz 给出重要阈值

$$
H^s(\mathbb R^d)\hookrightarrow C^0_b(\mathbb R^d)
\quad\text{当 }s>d/2.
$$

因此 point evaluation $u\mapsto u(x)$ 此时是连续泛函；低于阈值时，单点监督未必对 $H^s$ 元素天然有意义。这也解释了为什么足够高阶的 Sobolev function space 可以成为 RKHS，而普通 $L^2$ 不是。

### 4.4 Rellich–Kondrachov：有界不等于紧，嵌入可能紧

在有界规则区域，若指数严格低于临界值，Sobolev embedding 常是 compact。例如

$$
H^1(\Omega)\Subset L^2(\Omega)
$$

在有界 Lipschitz domain 上成立：每个 $H^1$ bounded sequence 都有在 $L^2$ 中 strongly convergent 的 subsequence。

紧性不能无条件搬到 $\mathbb R^d$。取固定 bump $\psi$ 并平移 $u_n(x)=\psi(x-ne_1)$，其 $H^1$ norms 不变，却没有 strongly convergent $L^2$ subsequence。这说明 bounded domain/防止质量逃向无穷远是实质条件。

## 5. 弱收敛与直接法

在 Banach space $X$ 中，$u_n\rightharpoonup u$ 表示

$$
\ell(u_n)\to\ell(u)\quad\forall\ell\in X^*.
$$

Strong convergence 推出 weak convergence，反向通常不成立。若 $1<p<\infty$，$W^{1,p}$ 是 reflexive；bounded sequence 可提取 weakly convergent subsequence。若泛函 $J$ 满足：

1. coercive：$\|u\|\to\infty$ 时 $J(u)\to\infty$；
2. sequentially weakly lower semicontinuous；
3. admissible set weakly closed；

则 minimizing sequence 可先由 coercivity 取得 boundedness，再以 weak compactness 抽子列，最后由 weak lower semicontinuity 得到 minimizer。这是变分 PDE 与能量模型存在性证明的标准骨架。

## 6. Poisson 方程：从强形式到弱形式

### 6.1 强形式

考虑

$$
\begin{cases}
-\Delta u=f,&x\in\Omega,\\
u=0,&x\in\partial\Omega.
\end{cases}
$$

若要求逐点成立，通常至少需要 $u\in C^2(\Omega)$。这个要求对粗糙数据和非光滑区域过强。

### 6.2 降一阶：推导弱形式

取 $v\in C_c^\infty(\Omega)$，乘上方程并积分：

$$
\int_\Omega(-\Delta u)v
=\int_\Omega fv.
$$

Green identity 把一阶导数转移到 $v$：

$$
\int_\Omega\nabla u\cdot\nabla v
-\int_{\partial\Omega}\partial_nu\,v
=\int_\Omega fv.
$$

Dirichlet test space $V=H_0^1(\Omega)$ 的 trace 为零，边界项消失。定义

$$
a(u,v)=\int_\Omega\nabla u\cdot\nabla v,
\qquad \ell(v)=\langle f,v\rangle_{H^{-1},H_0^1}.
$$

> [!definition] Poisson 弱解
> 找 $u\in H_0^1(\Omega)$，使
> $$
> a(u,v)=\ell(v)\quad\forall v\in H_0^1(\Omega).
> $$

这里只需一阶弱导数。若 $f\in L^2$，则 $\ell(v)=\int fv$；更一般 $f\in H^{-1}$ 也可以。

### 6.3 Lax–Milgram：存在唯一性合同

设 $V$ 是 Hilbert space，$a:V\times V\to\mathbb R$ 满足

$$
|a(u,v)|\le M\|u\|_V\|v\|_V
$$

以及 coercivity

$$
a(v,v)\ge\alpha\|v\|_V^2,
\qquad\alpha>0.
$$

若 $\ell\in V^*$，则存在唯一 $u\in V$ 使 $a(u,v)=\ell(v)$ 对所有 $v$ 成立，并且

$$
\|u\|_V\le\frac1\alpha\|\ell\|_{V^*}.
$$

对 Poisson，取 $\|v\|_V=\|\nabla v\|_{L^2}$，Poincaré 保证它是 norm；此时 $a(v,v)=\|v\|_V^2$。因此弱解存在、唯一并稳定依赖于 $f$。

> [!warning] 弱解不自动变成经典解
> 从 Lax–Milgram 只得到 $u\in H_0^1$。要推出 $H^2$、$C^1$ 或逐点 PDE，需要额外的 elliptic regularity；它依赖区域边界、系数与数据的光滑性。角点、界面或退化系数都可能破坏提升。

### 6.4 Energy minimization

定义

$$
J(v)=\frac12a(v,v)-\ell(v)
=\frac12\int_\Omega|\nabla v|^2-\langle f,v\rangle.
$$

对任意方向 $w\in V$，

$$
\frac{d}{dt}J(u+tw)\bigg|_{t=0}=a(u,w)-\ell(w).
$$

所以 stationary condition 正是弱形式。对 symmetric coercive $a$，$J$ strictly convex，唯一 stationary point 也是全局 minimizer。Deep Ritz 直接参数化并最小化这个 energy；但 Monte Carlo quadrature 与 nonconvex parameterization 会让“理论唯一 minimizer”不等于“训练一定找到它”。

### 6.5 Dirichlet 与 Neumann 边界的角色

- Dirichlet condition 被编码进 trial/test space，称为 essential boundary condition；
- Neumann flux 来自分部积分的 boundary term，称为 natural boundary condition；
- pure Neumann Poisson 只确定到 additive constant，并需 compatibility condition，例如 $-\Delta u=f$、$\partial_nu=g$ 时
  $$
  \int_\Omega f+\int_{\partial\Omega}g=0
  $$
  （符号随方程约定而定）。

对 $-\nabla\cdot(A(x)\nabla u)=f$，若 $A$ bounded 且 uniformly elliptic，

$$
\xi^\top A(x)\xi\ge\lambda|\xi|^2\quad\text{a.e.},
$$

同一套 Lax–Milgram 结构仍成立。失去 uniform ellipticity 后不能照抄结论。

## 7. Galerkin 与有限元：误差由最佳逼近控制

### 7.1 离散弱问题

取 finite-dimensional conforming subspace $V_h\subset V$，求 $u_h\in V_h$ 使

$$
a(u_h,v_h)=\ell(v_h)\quad\forall v_h\in V_h.
$$

减去连续弱形式得到 Galerkin orthogonality：

$$
a(u-u_h,v_h)=0\quad\forall v_h\in V_h.
$$

### 7.2 Céa 引理

对任意 $w_h\in V_h$，coercivity、orthogonality 与 continuity 给出

$$
\begin{aligned}
\alpha\|u-u_h\|_V^2
&\le a(u-u_h,u-u_h)\\
&=a(u-u_h,u-w_h)\\
&\le M\|u-u_h\|_V\|u-w_h\|_V.
\end{aligned}
$$

约去一项后

$$
\boxed{\|u-u_h\|_V\le\frac{M}{\alpha}\inf_{w_h\in V_h}\|u-w_h\|_V.}
$$

Céa 不直接给 $h$ 的收敛率；还需 interpolation estimate 与解的 regularity。例如一维分片线性有限元，在 $u\in H^2$ 和 quasi-uniform mesh 下通常有 $H^1$ error $O(h)$、$L^2$ error $O(h^2)$。若 $u\notin H^2$，速率会下降。

### 7.3 强残差与弱残差为何可以完全不同

分片线性 $u_h$ 在每个单元内部满足 $u_h''=0$，但其斜率在节点跳跃，分布二阶导数包含 node deltas。若在单元内部 collocation 计算

$$
r_{\rm strong}(x)=-u_h''(x)-f(x)=-f(x),
$$

看起来残差并不变小；与此同时 Galerkin residual

$$
R(v_h)=a(u_h,v_h)-\ell(v_h)=0
\quad\forall v_h\in V_h
$$

精确为零。两者检查的是不同对象：一个要求逐点二阶结构，另一个只要求在测试空间上的积分平衡。

## 8. 三类神经 PDE 方法的对象合同

### 8.1 Strong-form PINN

用网络 $u_\theta(x)$ 表示单个解，最常见 loss 为

$$
\mathcal L_{\rm PINN}
=\frac1{N_r}\sum_i|\mathcal N[u_\theta](x_i)-f(x_i)|^2
+\lambda_b\frac1{N_b}\sum_j|\mathcal B[u_\theta](z_j)-g(z_j)|^2.
$$

优点是形式直接、automatic differentiation 易用；代价是：

- $\mathcal N$ 若含二阶导数，网络和实现必须支持相应导数；
- finite collocation loss 不是连续 $L^2$ residual norm，更不是自动的 solution error bound；
- 稀疏点可能漏掉窄峰、界面和边界层；
- penalty boundary condition 存在权重与可行性误差；hard construction 可精确满足边界，但改变 hypothesis class 与 conditioning。

### 8.2 Deep Ritz

若 PDE 来自 coercive energy，令 $u_\theta\in V$ 并最小化

$$
\widehat J(\theta)
=\frac1N\sum_i\left[\frac12|\nabla u_\theta(x_i)|^2-f(x_i)u_\theta(x_i)\right].
$$

它只需一阶导数，并直接对应 energy norm，但仅适合有合适 variational principle 的问题；非对称、非 coercive 或 saddle-point 系统需要其他结构。

### 8.3 Weak/variational PINN、VPINN 与 VarNet

选 test functions $v_1,\ldots,v_m$，最小化

$$
\mathcal L_{\rm weak}(\theta)
=\sum_{j=1}^m|a(u_\theta,v_j)-\ell(v_j)|^2.
$$

分部积分可降低 $u_\theta$ 所需导数阶数，并在有正 measure 的区域聚合误差。但 finite test family 只检查 residual 在该 test span 上的投影；若 tests 太少、尺度单一或 quadrature 不准，loss 仍可能遗漏误差。

| 方法 | 学习对象 | 需要的导数 | 理论接口 | 主要盲点 |
|---|---|---:|---|---|
| strong PINN | 单个函数 $u$ | 与强算子阶数相同 | classical/strong residual | 点采样、刚性、尖峰 |
| Deep Ritz | 单个 energy minimizer | 常低一阶 | coercive variational problem | 必须有合适能量；非凸训练 |
| VPINN/VarNet | 单个 weak solution | 可经分部积分降阶 | weak residual/test space | tests 与 quadrature 覆盖不足 |

> [!important] AD 只回答“网络表达式的导数是什么”
> Automatic differentiation 不证明真解具有该阶正则性，不证明有限 collocation residual 控制解误差，也不替代 well-posedness。它是求导实现，不是 PDE 定理。

## 9. 从求一个解到学习解算子

### 9.1 解算子是什么

一族 PDE 可写成

$$
\mathcal A(a,u)=0,
\qquad u=\mathcal G(a),
$$

其中输入 $a$ 可是 forcing、系数、初值、边界或几何，输出 $u$ 是整条函数/场。神经算子学习

$$
\mathcal G:X\to Y,
$$

而不是固定 $a$ 下的一个 $u_\theta:\Omega\to\mathbb R$。必须声明输入空间 $X$、输出空间 $Y$、训练分布 $\mu$ 与 error norm；否则“逼近算子”没有可检验含义。

对 Dirichlet Poisson，

$$
\mathcal G=(-\Delta)^{-1}:H^{-1}(\Omega)\to H_0^1(\Omega)
$$

由 Lax–Milgram 连续。更光滑数据和区域可获得更强输出空间。well-posedness 是可学习目标稳定存在的前提之一。

### 9.2 Green function 是线性解算子的坐标表示

在线性问题且 Green kernel 存在时，形式上

$$
u(x)=\int_\Omega G(x,y)f(y)\,dy.
$$

这把“输入函数 $f$ 到输出函数 $u$”显式写成 integral operator，也是理解 neural operator integral layer 的桥梁。[[S-2014-Su-3092-格林函数与线性响应]]提供了这种响应—Green 函数直觉；正式的 Sobolev、边界与良定性结论仍以 PDE/functional-analysis 来源为准。

### 9.3 DeepONet：传感器编码与查询坐标分离

典型 DeepONet 写成

$$
\mathcal G_\theta(a)(y)
=\sum_{k=1}^p b_k(a(x_1),\ldots,a(x_m))t_k(y)+b_0.
$$

Branch net 编码有限 sensor values，trunk net 编码 output location。它能在不同 query points 评估输出，但输入信息已经经过 sensor map

$$
a\mapsto(a(x_1),\ldots,a(x_m)).
$$

若两个输入函数在 sensors 上相同而真实输出不同，任何后续网络都无法区分它们。Universal approximation theorem 不能消除 sensor non-injectivity、有限数据和 OOD 输入问题。

### 9.4 Fourier Neural Operator：频域参数化 integral operator

FNO layer 的简化形式为

$$
v_{\ell+1}(x)
=\sigma\!\left(Wv_\ell(x)+\mathcal F^{-1}\big(R_\ell(k)\,\mathcal Fv_\ell(k)\big)(x)\right),
$$

其中只保留有限 Fourier modes，并在频域学习 multiplier $R_\ell(k)$。这提供 global receptive field 和高效 FFT，但同时带来：

- Fourier truncation 与 unresolved high-frequency error；
- grid sampling、aliasing 与 FFT normalization；
- 非周期边界上的 padding/extension artifact；
- 新分辨率上“能运行”不等于 continuum operator error 已收敛。

### 9.5 三种常被混淆的“无网格/跨网格”陈述

1. **Architecture statement：** 参数可在不同 discretizations 间共享；
2. **Approximation statement：** 在 compact subset of function space 上存在参数逼近某个 continuous operator；
3. **Empirical generalization statement：** 用有限分辨率与有限分布训练后，在新网格、新系数尺度、新几何上仍准确。

第一条不推出第三条；第二条通常是存在性定理，也不提供给定优化器、样本量和宽度的成功保证。分辨率实验必须同时报告 physical grid、modes、anti-aliasing、输入生成过程和 continuum reference。

## 10. Sobolev training：监督导数就是改变拓扑

普通 regression 只匹配函数值：

$$
\mathcal L_0=\sum_i|f_\theta(x_i)-f(x_i)|^2.
$$

Sobolev training 再匹配一阶或高阶导数：

$$
\mathcal L_{\rm Sob}
=\mathcal L_0+\lambda\sum_i\|\nabla f_\theta(x_i)-\nabla f(x_i)\|^2.
$$

这不是“免费增加数据”，而是试图在更强的 Sobolev-type topology 中逼近目标。它可能改善 sample efficiency 与局部几何，却要求 derivative labels 可靠、尺度经归一化、目标确有相应正则性。数值微分会放大噪声；在不可微界面强迫经典 derivative target 甚至会改错问题。

## 11. 误差总账：训练 loss 之外还有六层

设真实 continuum solution operator 为 $\mathcal G$，离散参考为 $\mathcal G_h$，学习模型为 $\mathcal G_{\theta,h}$。一个实用分解是

$$
\|\mathcal G(a)-\mathcal G_{\theta,h}(a)\|_Y
\le
\underbrace{\|\mathcal G(a)-\mathcal G_h(a)\|_Y}_{\text{discretization/reference}}
+\underbrace{\|\mathcal G_h(a)-\mathcal G^*_{\Theta,h}(a)\|_Y}_{\text{representation}}
+\underbrace{\|\mathcal G^*_{\Theta,h}(a)-\mathcal G_{\theta,h}(a)\|_Y}_{\text{optimization/statistics}}.
$$

部署时至少审计：

| 误差层 | 问题 | 最低证据 |
|---|---|---|
| 建模/良定性 | PDE 是否有唯一稳定解？ | coercivity、stability 或适定性说明 |
| 表示 | architecture 能否表达所需尺度/边界？ | capacity 与 approximation audit |
| 离散/reference | 标签解本身多准？ | mesh refinement / solver tolerance |
| sampling/quadrature | loss 是否近似目标积分？ | 重采样、adaptive points、quadrature convergence |
| optimization | 是否只停在坏 local basin？ | 多 seed、loss 与 solution error 同报 |
| distribution/OOD | 输入是否超出训练 support？ | 按频率、系数、几何、分辨率分层测试 |
| arithmetic | FFT、导数与线性解是否受精度影响？ | precision/conditioning audit |

> [!warning] Residual-to-error 需要 stability
> 只有当算子在所选 spaces/norms 下有 stability estimate，例如
> $$
> \|u-\tilde u\|_V\le C\|\mathcal A\tilde u-f\|_{V^*},
> $$
> residual 才能控制 solution error。Finite sampled residual、错误 norm 或不适定问题不能直接套用这个结论。

## 12. 高频误区与反例

1. **“几乎处处可导就一定在 $W^{1,p}$。”** 错；还需导数可积并确实代表分布导数。跳跃函数 a.e. 导数为零，但分布导数含 delta。
2. **“每个 distribution derivative 都是 weak derivative。”** 错；weak derivative 要由 $L^1_{\rm loc}$ 函数表示。
3. **“$H^1$ 函数可逐点取值。”** 维数和 embedding 阈值未满足时错；它首先是 a.e. 等价类。
4. **“$p=d$ 时 $W^{1,p}\hookrightarrow L^\infty$。”** 一般错；临界嵌入需要更精细空间。
5. **“bounded sequence 一定有 strong convergent subsequence。”** 无限维空间中错；需 compact embedding 等额外结构。
6. **“弱解总比经典解不唯一。”** 错；Lax–Milgram 可在弱空间中给出唯一性，经典问题反而可能无解。
7. **“Galerkin residual 为零说明真实误差为零。”** 错；只在 $V_h$ test space 上为零，误差由最佳逼近控制。
8. **“PINN loss 很小就证明 PDE 解准确。”** 错；还缺 quadrature、coverage、stability、boundary 和 optimization 证据。
9. **“FNO 换网格可运行，所以是 discretization invariant。”** 错；需要 resolution convergence against continuum-quality reference。
10. **“Universal approximation 保证训练和 OOD 泛化。”** 错；它通常只是 compact set 上的存在性陈述。

## 13. 从零学习的四层掌握标准

### 第一层：识别

- 能区分 classical、distributional 和 weak derivative；
- 能说出 $W^{1,p}$、$H_0^1$、$H^{-1}$ 的对象；
- 能区分单解网络和 operator learner。

### 第二层：计算

- 能算 $|x|$、Heaviside、ReLU 的分布导数；
- 能把 Poisson 强形式推成弱形式和 energy；
- 能读懂一维分片线性 FEM 的 stiffness system。

### 第三层：证明

- 能证明弱导数 a.e. 唯一；
- 能逐项核验 Poisson 的 Lax–Milgram 假设；
- 能从 Galerkin orthogonality 推导 Céa 引理；
- 能给出 embedding/compactness 删除假设后的反例机制。

### 第四层：研究与应用

- 能为 PINN、Deep Ritz、VPINN 选择匹配的 function/test spaces 与 norms；
- 能设计 DeepONet/FNO 的 sensor、mode、resolution 与 OOD audit；
- 能把 PDE error 拆成建模、离散、表示、采样、优化与泛化误差；
- 能明确哪些结论是 theorem、哪些只是 finite experiment evidence。

## 14. 章末审计清单

- [ ] 每个函数是否先声明所在的 $L^p/W^{k,p}$ space，而不是只写“足够光滑”？
- [ ] distribution derivative 是否真的由函数表示，还是包含 delta/measure？
- [ ] trace、Poincaré、embedding、compactness 是否写了 domain 与指数条件？
- [ ] PDE 的 trial space、test space、bilinear form、load functional 是否完整？
- [ ] existence、uniqueness、stability、regularity 是否分开陈述？
- [ ] energy equivalence 是否依赖 symmetric/coercive structure？
- [ ] Galerkin error 是否同时说明 approximation 与 regularity？
- [ ] neural loss 是 pointwise、energy 还是 weak residual？quadrature 在哪里？
- [ ] 单实例 solver 与 solution operator 是否明确区分？
- [ ] operator experiment 是否覆盖 unseen inputs、unseen resolutions 与 continuum reference？
- [ ] “通用逼近”“参数共享”“经验泛化”是否没有互相替代？

## 15. 本章来源与阅读顺序

1. MIT 18.102/18.155 notes：先读弱导数、Sobolev 与 embedding 的严谨定义；
2. Evans 与 Adams–Fournier：补全 PDE、trace、embedding、compactness 的正式定理与证明；
3. MIT finite-element notes：沿 Poisson 弱形式、Lax–Milgram、Galerkin、Céa 建立数值主线；
4. PINN、Deep Ritz、VarNet/VPINN 原始论文：比较 strong residual、energy 与 weak residual；
5. DeepONet、FNO 与 JMLR neural-operator framework：进入函数到函数的学习；
6. [[S-2014-Su-3092-格林函数与线性响应]]：只作 Green function/response 的中文直觉桥，不承担本章定理证据。

正式入口：

- [MIT 18.155 Differential Analysis: Sobolev spaces](https://ocw.mit.edu/courses/18-155-differential-analysis-fall-2004/resources/section10/)
- [MIT 18.102 Functional Analysis lecture notes](https://ocw.mit.edu/courses/18-102-introduction-to-functional-analysis-spring-2021/3d4cc88026d44a01f936cd6a0aa995cb_MIT18_102s20_lec_FA.pdf)
- [A gentle introduction to the finite element method](https://math.mit.edu/~stoopn/18.086/FEintro.pdf)
- [Physics-informed neural networks](https://www.sciencedirect.com/science/article/pii/S0021999118307125)
- [The Deep Ritz method](https://arxiv.org/abs/1710.00211)
- [DeepONet](https://www.nature.com/articles/s42256-021-00302-5)
- [Fourier Neural Operator](https://openreview.net/pdf?id=c8P9NQVtmnO)
- [Neural Operator: Learning Maps Between Function Spaces](https://www.jmlr.org/papers/v24/21-1524.html)
- [VarNet: Variational Neural Networks for PDEs](https://proceedings.mlr.press/v120/khodayi-mehr20a.html)
- [Sobolev Training for Neural Networks](https://proceedings.neurips.cc/paper_files/paper/2017/hash/758a06618c69880a6cee5314ee42d52f-Abstract.html)

## 16. 继续学习

- 做题：[[习题 - 弱导数、Sobolev 空间与神经算子接口]]
- 核对完整证明：[[解答 - 弱导数、Sobolev 空间与神经算子接口]]
- 运行数值审计：[[实验 - 弱导数、变分残差与解算子频谱审计]]
- 回到算子谱：[[有界算子、紧算子与谱理论基础]]
- 回到核空间与点求值：[[正定核、RKHS 与表示定理]]
- 比较守恒律的分布弱形式：[[连续性方程与守恒律]]
