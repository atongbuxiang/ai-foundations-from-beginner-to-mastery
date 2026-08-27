---
type: concept
status: draft
area: [math/numerical-linear-algebra, math/krylov-methods]
aliases: [GMRES, MINRES, 残差最小化方法]
prerequisites: ["[[Krylov 子空间与预条件]]", "[[Arnoldi 方法]]", "[[Lanczos 方法]]", "[[共轭梯度法]]"]
related: ["[[稀疏矩阵计算与存储复杂度]]", "[[稳定最小二乘与正规方程的风险]]", "[[数值稳定性]]", "[[非正规矩阵、预解式与伪谱]]", "[[实验 - GMRES 重启、MINRES 结构与残差最小化]]"]
sources: ["[[S-1986-Saad-Schultz-GMRES]]", "[[S-2011-Choi-Paige-Saunders-MINRESQLP]]", "[[S-1994-Barrett-线性系统迭代模板]]", "[[S-2026-PETSc-KSP与PCG契约]]"]
exercises: ["[[习题 - GMRES、MINRES 与残差最小化]]"]
solutions: ["[[解答 - GMRES、MINRES 与残差最小化]]"]
created: 2026-08-15
updated: 2026-08-27
---

# GMRES、MINRES 与残差最小化

> [!abstract] 本章主问题
> GMRES 用 Arnoldi 基在一般方阵的 Krylov 仿射空间中逐阶最小化真残差二范数；MINRES 利用对称性把同一目标压缩为 Lanczos 短递推，并允许矩阵不定。两者的“最小残差”都只在当前搜索空间内成立，重启、非正规性、预条件坐标和有限精度决定生产环境中是否真的可靠。

先用下图回答一个视觉问题：**怎样按矩阵结构选择 CG/MINRES/GMRES，残差最小化怎样被压缩到小问题，重启又改变了什么？**

![[00-知识库管理/_assets/figures/numerical-analysis/fig-gmres-minres-restart-v2.svg|880]]

> [!figure] 图 10.8.18｜结构化方法选择、GMRES 小最小二乘与重启语义
> A 按 SPD、对称不定、一般方阵和矩形最小二乘分流到 CG/PCG、MINRES、GMRES/FGMRES 与 LSQR/LSMR；B 从 Arnoldi 关系把 GMRES 的原空间 residual 最小化压缩为 $\min_y\|\beta e_1-\bar H_ky\|_2$，再构造 $x_k=x_0+V_ky_k$；C 说明 MINRES 在对称不定结构下使用 Lanczos 三对角最小二乘，并把重启表示为“扩展—保留信息—重新开始”的信息压缩。来源：独立绘制；理论接口参考 Saad–Schultz、Choi–Paige–Saunders、Barrett et al. 与 PETSc；生成脚本：[[plot_numerical_large_scale_v2.py]]；确定性结构示意，无随机种子。

**怎样读图。** A 先验证线性、对称性与正定性，而不是从“Hessian”等应用名字猜方法；B 再沿 Arnoldi—小最小二乘—回代读 GMRES，并把 Givens 更新看成基于同一小问题的在线 residual norm 维护；C 最后区分 MINRES 的合法短递推和 GMRES$(m)$ 的重启：后者节省基存储与正交化，却会丢弃部分残差多项式/谱信息。任何预条件坐标中的内部 residual 最终都要与原问题 $b-Ax$ 对照。

**适用边界（图没有证明什么）。** 完整 GMRES 的 residual 单调性是精确算术、嵌套搜索空间下的结论，不推出解误差单调，也不延续到任意重启周期。MINRES 需要 Hermitian/实对称结构，奇异兼容系统或最小长度解还需 MINRES-QLP 等语义。可变/非线性预条件通常要求 flexible 变体；非正规矩阵的收敛不能只由特征值散点预测。

## 一、学习目标

完成本章后，你应能：

1. 从最小残差问题推导 GMRES 的 Arnoldi 小最小二乘；
2. 手算一个两步 GMRES，并验证残差正交于 $A\mathcal K_k$；
3. 用 Givens 旋转解释在线残差估计和更新；
4. 证明完整 GMRES 的真残差在精确算术中单调不增；
5. 用残差多项式解释谱、非正规性和有限终止；
6. 解释 GMRES$(m)$ 为什么省资源却可能停滞；
7. 区分左、右和 flexible 预条件的残差含义；
8. 从 Lanczos 推导 MINRES 的小型三对角最小二乘；
9. 根据 SPD、对称不定、奇异和一般非对称结构选择 CG、MINRES、GMRES 或其变体；
10. 用真残差、正交缺陷、重启状态和成本写出可验收报告。

> [!question] 初学者读完必须能回答
> 1. SPD、对称不定与一般方阵分别为什么对应 CG、MINRES 与 GMRES？
> 2. Arnoldi 关系怎样把 GMRES 压缩成小型最小二乘？
> 3. Givens 旋转如何在线更新 residual norm 而不每步重解全部问题？
> 4. 完整 GMRES 的 residual 为什么单调不增，解误差为何未必？
> 5. GMRES$(m)$ 重启节省哪些资源，又可能丢失哪些信息？
> 6. MINRES 为什么可以处理对称不定系统，而 CG 可能曲率 breakdown？
> 7. Left/right/flexible 预条件后，为什么仍必须重算原问题 true residual？

> [!note] 课程位置
> NUM-17 的 CG 依赖 SPD 能量几何；本章把方法选择拆成两条：一般非对称系统用 Arnoldi–GMRES 最小化二范数 residual，对称但不定系统用 Lanczos–MINRES 保留短递推。下一章会解释这些方法为何只有在稀疏 matvec、正交化、通信与存储都可承受时才真正“大规模”。

> [!tip] 建议两遍阅读
> 第一遍只在统一非正规 $A$ 上手算两步 GMRES，并用对称增广矩阵说明 MINRES 的合法位置；第二遍再进入 Givens 在线更新、GMRES$(m)$、left/right/flexible 预条件、奇异系统与 residual gap。第一遍始终问“当前最小化的是哪个方程、哪个范数下的 residual”。

## 本章的推导问题链

1. 为什么删除对称正定性后，CG 的能量最优与三项递推不再合法？
2. Arnoldi 怎样把 $x_0+\mathcal K_k$ 中的高维 residual 压缩成小型最小二乘？
3. 第一步 GMRES 的最优系数怎样由一维投影得到？
4. 为什么第二步出现 happy breakdown，并与 Jordan block 的二次最小多项式一致？
5. 完整 GMRES residual 单调不增，为何解误差仍未必单调？
6. 如何从同一个 $A$ 构造对称不定增广系统，使 MINRES 合法而 CG 非法？
7. Restart 与预条件为何会改变搜索信息或 residual 语义，却不能改变最终 true residual 合同？

## 贯穿算例：同一个非正规 block 上的两步 GMRES

取

$$
A=
\begin{bmatrix}
1&2&0\\
0&1&0\\
0&0&3
\end{bmatrix},
\qquad
x_\dagger=(1,-1,0)^T,
\qquad
b=Ax_\dagger=(-1,-1,0)^T,
\qquad
x_0=0.
$$

$A$ 非对称，且被右端激活的左上 block 是特征值为 $1$ 的二阶 Jordan block。CG 没有合法的 SPD 能量解释；GMRES 则只要求一般方阵和可计算 matvec。

### 符号与对象账本

| 对象 | 定义 | 本例中的值/作用 |
|---|---|---|
| $r_0$ | $b-Ax_0$ | $(-1,-1,0)^T$，范数 $\beta=\sqrt2$ |
| $Q_k$ | Arnoldi 标准正交基 | 张成 $\mathcal K_k(A,r_0)$ |
| $\bar H_k$ | $AQ_k=Q_{k+1}\bar H_k$ | 小型上 Hessenberg |
| $y_k$ | 小最小二乘变量 | 决定 $x_k=x_0+Q_ky_k$ |
| $r_k$ | $b-Ax_k$ | GMRES 直接最小化其二范数 |
| $p_k$ | residual polynomial | $r_k=p_k(A)r_0$，$p_k(0)=1$ |
| $\mathcal J$ | $\left[\begin{smallmatrix}0&A\\A^T&0\end{smallmatrix}\right]$ | MINRES 的对称不定伴随例 |
| GMRES$(m)$ | 每 $m$ 步重启 | 限制存储但丢弃部分多项式历史 |

### 第一步：Arnoldi 给出一个一维最小二乘

归一化初始 residual：

$$
q_1=\frac1{\sqrt2}(-1,-1,0)^T.
$$

计算

$$
Aq_1=\frac1{\sqrt2}(-3,-1,0)^T,
\qquad
h_{11}=q_1^TAq_1=2.
$$

正交余量为

$$
w=Aq_1-2q_1
=\frac1{\sqrt2}(-1,1,0)^T,
$$

所以

$$
h_{21}=1,
\qquad
q_2=\frac1{\sqrt2}(-1,1,0)^T,
\qquad
\bar H_1=\begin{bmatrix}2\\1\end{bmatrix}.
$$

GMRES 的高维问题变成

$$
\min_y
\left\|
\begin{bmatrix}\sqrt2\\0\end{bmatrix}
-
\begin{bmatrix}2\\1\end{bmatrix}y
\right\|_2.
$$

一维投影给出

$$
y_1=\frac{2\sqrt2}{5},
\qquad
x_1=q_1y_1=\left(-\frac25,-\frac25,0\right)^T.
$$

回到原方程重算：

$$
r_1=b-Ax_1=\left(\frac15,-\frac35,0\right)^T,
\qquad
\|r_1\|_2=\sqrt{\frac25}.
$$

它确实满足 $r_1\perp A\mathcal K_1$，但不要求 $r_1\perp\mathcal K_1$；后者是 FOM/CG 风格的另一种投影条件。

### 第二步：happy breakdown 与二次最小多项式

继续作用

$$
Aq_2=\frac1{\sqrt2}(1,1,0)^T.
$$

投影系数为

$$
h_{12}=q_1^TAq_2=-1,
\qquad
h_{22}=q_2^TAq_2=0,
$$

且余量为零，所以

$$
h_{32}=0,
\qquad
H_2=
\begin{bmatrix}
2&-1\\
1&0
\end{bmatrix}.
$$

解

$$
H_2y=\sqrt2e_1
$$

得到 $y=(0,-\sqrt2)^T$，从而

$$
x_2=Q_2y=(1,-1,0)^T=x_\dagger,
\qquad
r_2=0.
$$

在被激活的 Jordan block 上，最小多项式为 $(t-1)^2$，故合法 residual polynomial

$$
p_2(t)=(1-t)^2,
\qquad
p_2(0)=1
$$

满足 $p_2(A)r_0=0$。重复根很重要：只在 eigenvalue $1$ 放一个根不能消掉 Jordan 导数项。

### 第三步：MINRES 不是“更省内存的 GMRES”

由同一个 $A$ 构造对称增广矩阵

$$
\mathcal J=
\begin{bmatrix}
0&A\\
A^T&0
\end{bmatrix}.
$$

$\mathcal J=\mathcal J^T$，其 eigenvalues 是

$$
\pm3,
\qquad
\pm(1+\sqrt2),
\qquad
\pm(\sqrt2-1).
$$

因此它对称但不定：CG 的正曲率分母没有保证，MINRES 却可用 Lanczos 三对角关系最小化二范数 residual。MINRES 的短递推来自**对称性**，不是来自随意截断 Arnoldi 历史。

### 第四步：单调 residual、重启与真误差必须分开

本例完整 GMRES 有

$$
\|r_0\|_2=\sqrt2,
\qquad
\|r_1\|_2=\sqrt{2/5},
\qquad
\|r_2\|_2=0.
$$

完整 GMRES 的搜索空间逐步嵌套，所以 residual norm 单调不增；GMRES$(m)$ 重启后不再保留整条嵌套历史，可能停滞。即使 residual 单调，非正规 $A$ 上的解误差仍受 $A^{-1}$ 与方向影响，不能由同一曲线替代。

### 核心公式七问：$\min_y\|\beta e_1-\bar H_ky\|_2$

1. **从哪来？** 写 $x=x_0+Q_ky$，再用 Arnoldi 关系和 $r_0=\beta q_1$ 把高维 residual 提到 $Q_{k+1}$ 坐标。
2. **为什么范数相等？** $Q_{k+1}$ 列正交，左乘它不改变小坐标向量的二范数。
3. **为何不用小正规方程？** $\bar H_k^T\bar H_k$ 会平方小问题条件数；Givens/QR 可在线稳定维护最小二乘。
4. **GMRES 最小化什么？** 只在当前 $x_0+\mathcal K_k$ 中最小化当前坐标定义的 residual，不声称全空间解误差最小。
5. **MINRES 为什么更短？** 对称性使 Arnoldi 退化为 Lanczos 三对角；不定性不妨碍 residual 最小化，却会破坏 CG 能量几何。
6. **Restart 丢什么？** 丢掉长 Krylov 基与已经形成的高次 residual polynomial 信息；省内存和正交化的代价可能是停滞。
7. **AI 中如何验收？** 隐式层、KKT 与非对称 Jacobian 求解要报告 true residual、重启周期、预条件方向、matvec/归约和下游梯度误差。

> [!warning] 教学模型边界
> 右端特意只激活二阶 Jordan block，因此完整 GMRES 两步精确终止；一般右端还会激活第三个 eigenvalue，需要第三步。六维增广矩阵只用于说明 MINRES 的结构边界，不表示所有奇异值问题都应改写成增广系统求解。

> [!success] 第一遍停靠线
> 应能算出 $\bar H_1=(2,1)^T$、$y_1=2\sqrt2/5$、$r_1=(1,-3,0)^T/5$ 与 $H_2=\left[\begin{smallmatrix}2&-1\\1&0\end{smallmatrix}\right]$，解释 $p_2(t)=(1-t)^2$ 为何消掉 Jordan block，并说清 $\mathcal J$ 对称不定时 MINRES 合法而 CG 不合法。

## 二、先按矩阵结构选方法

求解

$$
Ax=b,\qquad A\in\mathbb C^{n\times n}.
$$

最先问的不是“哪个名字最快”，而是 $A$ 有什么可信结构：

| 结构 | 首选主线 | 最小化/投影量 |
|---|---|---|
| Hermitian/SPD | CG/PCG | $A$-能量误差最小 |
| Hermitian/对称，可不定 | MINRES | 二范数残差最小 |
| 一般方阵 | GMRES/FGMRES | 二范数残差最小 |
| 矩形最小二乘 | LSQR/LSMR | Golub–Kahan 双对角化下的残差 |
| 一般方阵、内存极紧 | BiCGStab 等 | 短递推，但通常失去逐阶最小性 |

> [!warning] “Hessian”不自动等于 SPD
> 非凸优化 Hessian 可不定；近似 Jacobian 通常非对称；自动微分实现还可能因随机 batch、状态或不一致的 JVP/VJP 破坏线性和对称性。

## 三、从搜索空间到最小残差

令

$$
r_0=b-Ax_0,
\qquad
\mathcal K_k=\operatorname{span}\{r_0,Ar_0,\ldots,A^{k-1}r_0\}.
$$

GMRES 定义为

$$
\boxed{
x_k=\arg\min_{x\in x_0+\mathcal K_k}\|b-Ax\|_2.}
$$

若写 $x=x_0+s$，$s\in\mathcal K_k$，这就是一个受限最小二乘问题：

$$
\min_{s\in\mathcal K_k}\|r_0-As\|_2.
$$

一阶最优条件为

$$
\boxed{r_k\perp A\mathcal K_k.}
$$

这与 FOM/CG 的 $r_k\perp\mathcal K_k$ 不同。GMRES 的测试空间是 $A\mathcal K_k$。

## 四、Arnoldi 把大问题压缩成小问题

从

$$
q_1=\frac{r_0}{\beta},\qquad \beta=\|r_0\|_2
$$

开始做 $k$ 步 Arnoldi：

$$
AQ_k=Q_{k+1}\bar H_k,
$$

其中 $Q_{k+1}$ 列标准正交，$\bar H_k\in\mathbb C^{(k+1)\times k}$ 为上 Hessenberg。

任意候选写成

$$
x=x_0+Q_ky.
$$

则

$$
\begin{aligned}
r(y)
&=r_0-AQ_ky\\
&=Q_{k+1}\bigl(\beta e_1-\bar H_ky\bigr).
\end{aligned}
$$

正交矩阵保持二范数，因此

$$
\boxed{
y_k=\arg\min_y\|\beta e_1-\bar H_ky\|_2,
\qquad x_k=x_0+Q_ky_k.}
$$

大规模 $n$ 维最小残差问题被压缩成 $(k+1)\times k$ 小最小二乘；大算子只通过 matvec 出现。

### 4.1 为什么不形成正规方程

不能把小问题草率写成

$$
\bar H_k^*\bar H_ky=\bar H_k^*\beta e_1
$$

再认为万事大吉。正规方程平方条件数；生产实现通常用逐列 Givens 旋转维护 $\bar H_k$ 的 QR。

## 五、Givens 旋转与在线残差

第 $j$ 个 Arnoldi 列产生一个新的次对角元 $h_{j+1,j}$。先应用旧 Givens 消去此前结构，再构造

$$
G_j=
\begin{bmatrix}
c_j&s_j\\
-\overline{s_j}&c_j
\end{bmatrix}
$$

把

$$
\begin{bmatrix}h_{jj}\\h_{j+1,j}\end{bmatrix}
\mapsto
\begin{bmatrix}\rho_j\\0\end{bmatrix}.
$$

同样旋转右端 $\beta e_1$。若旋转后右端记为 $g$，则第 $j$ 步最小残差范数可由末分量得到：

$$
\|r_j\|_2=|g_{j+1}|.
$$

它无需每轮额外 matvec。最终或周期性仍应重算

$$
r_j^{true}=b-Ax_j,
$$

因为有限精度下 Arnoldi 正交性、Givens 更新和递推残差都会漂移。

## 六、完整手算：两步 GMRES

取

$$
A=\begin{bmatrix}2&1\\0&1\end{bmatrix},
\qquad
b=\begin{bmatrix}1\\1\end{bmatrix},
\qquad x_0=0.
$$

真解是 $x_*=(0,1)^T$。

### 6.1 第一步 Arnoldi

$$
\beta=\sqrt2,\qquad q_1=\frac1{\sqrt2}(1,1)^T.
$$

$$
Aq_1=\frac1{\sqrt2}(3,1)^T.
$$

$$
h_{11}=q_1^TAq_1=2.
$$

去掉 $2q_1$：

$$
w=\frac1{\sqrt2}(1,-1)^T,
\qquad h_{21}=1,
\qquad q_2=\frac1{\sqrt2}(1,-1)^T.
$$

所以

$$
\bar H_1=\begin{bmatrix}2\\1\end{bmatrix}.
$$

小问题为

$$
\min_y\left\|
\begin{bmatrix}\sqrt2\\0\end{bmatrix}
-
\begin{bmatrix}2\\1\end{bmatrix}y
\right\|_2.
$$

投影系数

$$
y_1=\frac{2\sqrt2}{5}.
$$

故

$$
x_1=Q_1y_1=(2/5,2/5)^T.
$$

真残差

$$
r_1=b-Ax_1=(-1/5,3/5)^T,
$$

$$
\|r_1\|_2=\sqrt{2/5}.
$$

并且

$$
r_1^TAq_1=0,
$$

验证了 $r_1\perp A\mathcal K_1$。

### 6.2 第二步

$$
Aq_2=q_2.
$$

所以

$$
h_{12}=0,\qquad h_{22}=1,\qquad h_{32}=0.
$$

投影矩阵为

$$
H_2=
\begin{bmatrix}
2&0\\
1&1
\end{bmatrix}.
$$

解

$$
H_2y=\sqrt2e_1
$$

得

$$
y=(\sqrt2/2,-\sqrt2/2)^T.
$$

于是

$$
x_2=Q_2y=(0,1)^T=x_*.
$$

$h_{32}=0$ 表示 Krylov 空间已不变，称为 happy breakdown：它不是失败，而是精确收敛。

## 七、单调性、有限终止与残差多项式

### 7.1 完整 GMRES 单调不增

因为

$$
\mathcal K_k\subseteq\mathcal K_{k+1},
$$

上一轮候选仍属于下一轮候选集，所以

$$
\boxed{\|r_{k+1}\|_2\le\|r_k\|_2.}
$$

这不保证每轮严格下降；曲线可以长时间平台。

### 7.2 多项式形式

任意 Krylov 候选对应

$$
r_k=p_k(A)r_0,\qquad p_k(0)=1,\quad \deg p_k\le k.
$$

GMRES 选择使二范数最小的多项式：

$$
\|r_k\|_2
=
\min_{\substack{p(0)=1\\\deg p\le k}}
\|p(A)r_0\|_2.
$$

若 $A$ 非奇异，且相对于 $r_0$ 的最小多项式次数为 $m$，可把该多项式归一化为 $p(0)=1$；精确算术中完整 GMRES 至多 $m$ 步得到零残差，故至多 $n$ 步。奇异或不相容系统必须另行检查是否存在满足 $p(0)=1$ 且 $p(A)r_0=0$ 的残差多项式，不能直接套用“至多 $n$ 步精确解”。

### 7.3 为什么只看特征值不够

若 $A=V\Lambda V^{-1}$，有粗界

$$
\|p(A)\|_2
\le\kappa_2(V)\max_i|p(\lambda_i)|.
$$

非正规时 $\kappa(V)$ 可巨大；缺陷矩阵还带来 Jordan 导数项。两个特征值完全相同的矩阵可以有完全不同的 GMRES 暂态和停滞。应结合：

- 特征向量条件性；
- 数值域与到原点的距离；
- 伪谱/resolvent；
- 右端在困难方向上的权重；
- 直接观测的真残差。

## 八、重启 GMRES$(m)$

完整 GMRES 第 $k$ 步需保存约 $k+1$ 个基向量，累计正交内积约

$$
1+2+\cdots+k=\frac{k(k+1)}2.
$$

为控制资源，GMRES$(m)$ 每构造 $m$ 个方向后：

1. 计算当前 $x$；
2. 重算/继承新残差；
3. 丢弃旧 Arnoldi 基；
4. 从新残差开始下一周期。

每周期仍在该周期的 Krylov 空间中最小化残差，因此精确算术真残差不增；但它不再等价于一个不断扩大的全局 $\mathcal K_k(A,r_0)$，旧多项式信息被压缩成单个当前残差。

后果：

- 可能停滞或出现周期性；
- 增大 $m$ 通常提供更丰富空间，但每轮正交更贵；
- 固定 matvec 预算下，最佳 $m$ 不一定单调；
- deflated/thick/recycled restart 可保留近似不变子空间；
- 多右端或缓慢变化系统可用 GCRO-DR/LGMRES 等回收信息。

> [!tip] 重启参数是资源—收敛超参数
> 必须在同一真残差、同一 matvec/时间预算下比较，并记录峰值基内存和全局归约。

## 九、预条件 GMRES 与真实验收量

### 9.1 左预条件

$$
M^{-1}Ax=M^{-1}b.
$$

GMRES 最小化的是

$$
\|M^{-1}(b-Ax)\|_2,
$$

不一定是原方程真残差。最终必须重算 $b-Ax$。

### 9.2 右预条件

令 $x=x_0+M^{-1}z$：

$$
AM^{-1}z=r_0.
$$

右预条件 GMRES 可直接最小化原残差二范数；但需保存/应用预条件后的基方向。

### 9.3 Flexible GMRES

若第 $j$ 步使用 $z_j=M_j^{-1}v_j$，实际预条件器随步数改变，普通右预条件 GMRES 的 $M^{-1}V_k$ 关系失效。FGMRES 显式保存

$$
Z_k=[z_1,\ldots,z_k]
$$

并令

$$
x_k=x_0+Z_ky.
$$

适用于变容差内层求解、非线性多重网格或学习型预条件器，代价是额外存储。

## 十、MINRES：利用对称性保留最小残差

若

$$
A=A^*,
$$

但不要求正定，Arnoldi 退化为 Lanczos：

$$
AQ_k=Q_{k+1}\bar T_k,
$$

$\bar T_k$ 为扩展对称三对角矩阵。MINRES 解

$$
\boxed{
\min_y\|\beta e_1-\bar T_ky\|_2.}
$$

与 GMRES 一样最小化二范数残差，却可借三对角结构使用短递推，存储和每轮工作不随 $k$ 线性增长。

### 10.1 为什么 MINRES 能处理不定矩阵

它不把 $p^TAp>0$ 当作步长分母的基础，而是对 Lanczos 小最小二乘做稳定正交变换。对

$$
A=\operatorname{diag}(1,-1),\qquad b=(1,1)^T,
$$

CG 首步有

$$
b^TAb=0,
$$

无法定义步长；MINRES 第 1 步残差无法下降，但第 2 步可精确求解。

### 10.2 预条件契约

MINRES 的算子必须保持 Hermitian/对称；预条件器必须 SPD，并以保持自伴结构的方式应用。任意 ILU 或非对称神经映射不能直接塞入 MINRES。

## 十一、奇异与不相容系统

若对称 $A$ 奇异，需要区分：

1. **相容**：$b\in\mathcal R(A)$，存在精确解；
2. **不相容**：只能最小化 $\|Ax-b\|$；
3. **最小长度**：在所有最小残差解中再选 $\|x\|$ 最小者。

MINRES-QLP 在 Lanczos 小问题上使用 QLP 分解，面向病态、奇异或不相容系统，并改善最小长度解的计算。

预条件后所谓“最小长度”可能对应预条件坐标下的加权范数，而不是原欧氏范数。报告必须写清目标。

## 十二、CG、MINRES 与 GMRES 的精确边界

| 条件 | CG | MINRES | GMRES |
|---|---:|---:|---:|
| SPD | 合法，能量最优 | 合法，残差最优 | 合法但通常资源更高 |
| 对称不定 | 不合法 | 合法 | 合法但浪费对称结构 |
| 一般非对称 | 不合法 | 不合法 | 合法 |
| 短递推 | 是 | 是 | 否（完整形式） |
| 每步二范数残差最小 | 否 | 是 | 是 |
| 可变预条件 | 普通 PCG 不可 | 普通 MINRES 不可 | 用 FGMRES |

对于一般非对称问题，BiCG、QMR、BiCGStab 等用伴随或双递推换固定存储，但不再具有完整 GMRES 的逐阶残差最优性，曲线可能剧烈波动甚至 breakdown。

## 十三、有限精度与生产级停止

### 13.1 正交性丢失

一次 MGS、CGS、重正交策略会改变：

$$
\|Q_k^*Q_k-I\|.
$$

正交性劣化会污染 Hessenberg 关系、残差估计和新信息量。生产实现应记录正交化类型与必要时的 refinement。

### 13.2 递推残差间隙

内部估计 $|g_{k+1}|$ 与

$$
\|b-A\widehat x_k\|
$$

在舍入下可能分离。可靠流程：

1. 内部估计用于廉价筛选；
2. 周期/周期末显式重算真残差；
3. 最终报告尺度化后向误差；
4. 若差距过大，进行 residual replacement、重启或提高精度；
5. 记录 breakdown、happy breakdown、停滞和最大迭代退出原因。

### 13.3 非正规问题的前向解释

即便真残差很小，

$$
\frac{\|x-\widehat x\|}{\|x\|}
\lesssim
\kappa(A)\times\text{相对后向误差}
$$

仍可能很大。最小残差只解决算法残差目标，不消除问题本身的病态性。

## 十四、成本与通信

完整 GMRES 第 $k$ 步：

- 1 次 matvec；
- 约 $k$ 次内积与 axpy 正交；
- 保存 $k+1$ 个长度 $n$ 的基向量；
- 小 Hessenberg/Givens 更新；
- 分布式环境中多次全局归约。

累计正交成本约 $O(nk^2)$，基内存 $O(nk)$。重启限制为 $m$ 后，每周期约 $O(nm^2)$、内存 $O(nm)$，但周期数可能上升。

MINRES 借 Lanczos 短递推，每轮常数向量存储；这正是结构信息带来的算法红利。

## 十五、与 AI 的连接

### 15.1 隐式微分与深度平衡模型

反向常求

$$
(I-J_f^T)v=g.
$$

一般 $J_f$ 非对称且非正规，GMRES/FGMRES 比 CG 更符合结构。应监控 VJP 真残差、重启停滞和非正规暂态。

### 15.2 KKT 与鞍点系统

约束优化、PDE 反演和某些二阶训练产生

$$
\begin{bmatrix}
H&B^T\\
B&0
\end{bmatrix}
\begin{bmatrix}d\\\lambda\end{bmatrix}
=
\begin{bmatrix}g\\c\end{bmatrix}.
$$

它对称却通常不定：CG 不合法；若预条件保持对称且 SPD，可用 MINRES。块预条件和 Schur 补结构比“加一点对角”更重要。

### 15.3 非凸 Newton–MR

对称 Hessian 不定时，MINRES 可继续最小化线性残差；但优化目标还需要负曲率、信赖域和模型下降判断。线性求解成功不自动等于外层优化步安全。

### 15.4 随机算子

若每轮 JVP/HVP 使用不同 batch，算法看到的是变化算子，固定 Krylov 多项式理论不再原样成立。可固定内层 batch、降低内层精度目标，或使用容许变化的外层方法，并对固定参考算子重算残差。

## 十六、实验

[[实验 - GMRES 重启、MINRES 结构与残差最小化]]验证：

1. 非正规 Grcar 系统上完整 GMRES 与 GMRES$(8/16)$ 的差异；
2. 对称不定二维系统中 CG 首步 breakdown，而 MINRES 两步解出；
3. 固定 120 次 matvec 时，重启维数与最终残差、基内存、累计正交工作的非单调权衡。

## 十七、常见误区

> [!danger] 误区 1：GMRES 每步都降低解误差
> 它保证当前空间内二范数残差最小，不保证任意前向误差范数单调。

> [!danger] 误区 2：重启只省内存，不改变数学算法
> 重启丢弃旧 Krylov 基，可能停滞。

> [!danger] 误区 3：MINRES 就是给 CG 加一个绝对值
> 它基于 Lanczos 小最小二乘，结构和证明不同。

> [!danger] 误区 4：左预条件 GMRES 的内部残差就是原残差
> 它通常最小化 $\|M^{-1}r\|$。

> [!danger] 误区 5：库返回 converged 就无需复核
> 必须记录 norm type、preconditioning side、原因码和真残差。

## 十八、掌握标准

- **L1**：能按 SPD、对称不定、一般非对称选择方法；
- **L2**：能推导 Arnoldi/Lanczos 小最小二乘；
- **L3**：能手算 GMRES、解释 Givens 与残差多项式；
- **L4**：能诊断重启停滞、非正规性、正交丢失和残差间隙；
- **L5**：能为 KKT、隐式微分和随机 JVP 系统写结构与验收契约。

## 十九、继续学习

- 习题：[[习题 - GMRES、MINRES 与残差最小化]]；
- 解答：[[解答 - GMRES、MINRES 与残差最小化]]；
- 实验：[[实验 - GMRES 重启、MINRES 结构与残差最小化]]；
- 下一章：[[稀疏矩阵计算与存储复杂度]]；
- 来源：[[S-1986-Saad-Schultz-GMRES]]、[[S-2011-Choi-Paige-Saunders-MINRESQLP]]、[[S-1994-Barrett-线性系统迭代模板]]、[[S-2026-PETSc-KSP与PCG契约]]。
