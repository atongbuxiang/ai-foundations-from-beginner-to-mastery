---
type: exercise-set
status: draft
area: [math/calculus, math/matrix-calculus, math/matrix-analysis]
aliases: [谱分解导数习题, 可微 SVD 习题]
prerequisites: ["[[特征值、特征向量与 SVD 的导数]]"]
related: ["[[解答 - 特征值、特征向量与 SVD 的导数]]", "[[练习与测验 MOC]]"]
sources: ["[[S-2025-Su-10878-SVD的导数]]", "Davis-Kahan-1970", "Wedin-1972", "Townsend-2016-SVD-Derivative"]
created: 2026-08-18
updated: 2026-08-18
---

# 习题 - 特征值、特征向量与 SVD 的导数

> [!abstract] 训练目标
> 15 题按“简单谱—方向—重谱—非正规—SVD—AI 审计”递进。每次写导数前必须声明谱间隙、规范与真正不变的输出对象。

## A. 基本概念（3 题）

### A1. 三层对象

说明简单特征值、单个特征向量、重复谱簇的投影三者在唯一性与可微条件上的区别。为什么 $u$ 与 $-u$ 的欧氏距离不适合衡量一维特征子空间？

### A2. 规范条件

由 $u(t)^\top u(t)=1$ 推出 $u^\top u'=0$。若不固定符号/相位规范，$u'$ 为什么不再是良定义对象？给出一个数值对齐规则。

### A3. gap 的作用

对

$$
A=\begin{bmatrix}2&0\\0&2-\delta\end{bmatrix},
\quad
E=\begin{bmatrix}0&1\\1&0\end{bmatrix},
$$

计算主特征值和主特征向量沿 $E$ 的方向导数，并比较 $\delta=1,10^{-2},10^{-6}$。

## B. 对称与一般特征问题（3 题）

### B1. 简单对称特征对

从 $Au_i=\lambda_i u_i$ 完整推导

$$
D\lambda_i[E]=u_i^\top Eu_i,
\qquad
Du_i[E]=\sum_{j\ne i}u_j\frac{u_j^\top Eu_i}{\lambda_i-\lambda_j}.
$$

明确指出每一步使用的对称性、简单性和规范条件。

### B2. 谱投影导数

令 $P_i=u_iu_i^\top$。推导 $DP_i[E]$，证明它对 $u_i\mapsto-u_i$ 不变，并给出 $\|DP_i[E]\|$ 关于 gap 的粗略上界。

### B3. 非正规简单特征值

设 $Av=\lambda v$、$w^*A=\lambda w^*$。推导

$$
D\lambda[E]=\frac{w^*Ev}{w^*v}.
$$

对

$$
A_\varepsilon=\begin{bmatrix}1&1/\varepsilon\\0&2\end{bmatrix}
$$

讨论当 $\varepsilon\to0$ 时特征值为何可高度敏感，尽管特征值间隔恒为 $1$。

## C. 重谱与 SVD（3 题）

### C1. 重复最大特征值

在 $A=0_{2\times2}$ 处证明

$$
D\lambda_{\max}(0)[E]=\lambda_{\max}(E)
$$

只是方向导数而非 Fréchet 导数。给出两个方向说明该映射不满足可加性。

### C2. 简单奇异值

从 $Av_i=\sigma_i u_i$、$A^\top u_i=\sigma_i v_i$ 和单位约束推导

$$
D\sigma_i[E]=u_i^\top Ev_i.
$$

再推导只依赖奇异值的函数 $F(A)=\sum_i\phi(\sigma_i)$ 的梯度。

### C3. SVD 旋转方程

在实方阵、满秩、奇异值互异条件下，令 $P=U^\top EV$、$\Omega_U=U^\top dU$、$\Omega_V=V^\top dV$。从

$$
P=\Omega_U\Sigma+d\Sigma-\Sigma\Omega_V
$$

推导 $i\ne j$ 的 $2\times2$ 线性系统和解，并解释 $\sigma_i=\sigma_j$ 时不是简单的“除零计算错误”。

## D. 实现与 AI 审计（3 题）

### D1. 可微 PCA

设计一个验证 PCA 前 $r$ 维子空间导数的实验。要求包含：协方差构造、gap 扫描、投影距离、有限差分、内部基随机旋转不变性，以及至少三个诊断量。

### D2. 谱归一化

对 $\widehat W=W/\sigma_1(W)$，在 $\sigma_1>\sigma_2$ 时推导 $D\widehat W[E]$。说明有限次幂迭代、stop-gradient 和最大奇异值碰撞分别改变了什么。

### D3. 白化

设 $C=U\Lambda U^\top\succ0$，$Y=XC^{-1/2}$。分析最小特征值趋于零时前向值和反向导数的尺度；比较 hard clipping、$C+\varepsilon I$ 和截断子空间三种处理的数学含义。

## E. 证明与边界（3 题）

### E1. 重谱的一阶分裂

设 $A$ 在子空间 $\mathcal U$ 上为 $\lambda I$，$U_0$ 是其正交基。给出论证：$A+tE$ 在该簇中的一阶修正由 $U_0^\top EU_0$ 的特征值决定。解释为何结果与 $U_0$ 的换基无关。

### E2. 次梯度

分别写出并解释：

1. 最大特征值在重根处的次微分；
2. 谱范数在最大奇异值重数 $k$ 时的次微分；
3. 核范数在秩亏矩阵处的次微分。

说明自动微分返回其中一个矩阵为什么不等于函数普通可微。

### E3. 规范不变性审计

某模型把 SVD 的前 $r$ 列 $U_r$ 送入普通 MLP。证明/反驳：“只要训练数据没有完全重复奇异值，该模型就是矩阵 $A$ 的稳定函数。”要求讨论符号、接近碰撞、排列、有限精度与分布外样本，并提出一个基不变替代设计。

## 提交规范

每题至少包含：谱假设、输出对象、规范、方向导数或梯度类型、退化边界。D/E 层必须区分数学映射、数值分解算法和框架 backward 约定。
