---
type: exercise-set
status: draft
area: [labs, math/matrix-analysis]
prerequisites: ["[[Rayleigh 商与极值表征]]"]
related: ["[[二次型与正定矩阵]]", "[[幂法、反幂法与 Rayleigh 商迭代]]", "[[特征向量与子空间扰动定理]]", "[[练习与测验 MOC]]"]
sources: ["Axler-LADR4e-7B-7C", "MIT-18.409-Courant-Fischer"]
solutions: ["[[解答 - Rayleigh 商与极值表征]]"]
created: 2026-08-16
updated: 2026-08-16
---

# 习题 - Rayleigh 商与极值表征

> [!abstract] 训练目标
> 把“特征值是缩放率”升级为“特征值是方向和子空间优化值”：既能手算 Rayleigh 商，也能重建 Courant–Fischer 与 Ky Fan 证明，并能判断 PCA、Hessian、广义特征问题和非 Hermitian 反例中的适用边界。

## 作答规则

1. A–E 每级三题，共 15 题；
2. 每次写 Rayleigh 商都要说明矩阵、向量、标量域和分母正性；
3. 使用极值定理时必须声明 Hermitian/实对称假设与特征值排序；
4. 子空间题要区分目标值、最优子空间和子空间基；
5. AI 题必须写清张量形状、矩阵对象与经验估计误差。

## A 级：识别与复述

### MA-RQ-A01：对象、实值与尺度

设 $A\in\mathbb C^{n\times n}$，$x\in\mathbb C^n\setminus\{0\}$。

1. 写出 $\rho_A(x)$；
2. 证明 $\rho_A(cx)=\rho_A(x)$，其中 $c\ne0$；
3. $A$ 满足什么条件时，可以保证 $\rho_A(x)$ 对所有 $x$ 都为实数？
4. 为什么不能只用 $x^*Ax$ 比较不同方向？

### MA-RQ-A02：判断五个断言

判断并说明理由：

1. 对任意方阵，最大 Rayleigh 商等于最大模特征值；
2. Hermitian 矩阵的 Rayleigh 商总位于最小与最大特征值之间；
3. 单位球面上 Rayleigh 商的全部驻点都是局部最大值；
4. $Q^*Q=I_k$ 时，$\operatorname{tr}(Q^*AQ)$ 只依赖 $\operatorname{col}(Q)$；
5. 小 Rayleigh 残差一定保证向量接近某个预先指定的特征向量。

### MA-RQ-A03：形状与广义问题

给定

$$
A,B\in\mathbb R^{d\times d},
\qquad
Q\in\mathbb R^{d\times k},
\qquad
x\in\mathbb R^d.
$$

1. 写出 $Q^TAQ$、$Q^TBQ$ 和 $\operatorname{tr}(Q^TAQ)$ 的形状；
2. 广义 Rayleigh 商 $x^TAx/(x^TBx)$ 的标准变分理论为何要求 $B\succ0$？
3. $Q^TQ=I_k$ 与 $Q^TBQ=I_k$ 分别表示哪种几何中的标准正交？

## B 级：手算与构造

### MA-RQ-B01：二维角度参数化

设

$$
A=\begin{bmatrix}2&1\\1&2\end{bmatrix},
\qquad
x(\theta)=\begin{bmatrix}\cos\theta\\\sin\theta\end{bmatrix}.
$$

1. 求 $\rho_A(x(\theta))$；
2. 求全部驻点角度；
3. 分类最大值、最小值并写出对应特征向量；
4. 计算 $\|A\|_2$，说明它是否等于最大 Rayleigh 商。

### MA-RQ-B02：试探子空间与 Ritz 值

设

$$
A=\operatorname{diag}(7,4,1),
$$

以及

$$
q_1=\frac1{\sqrt2}(e_1+e_3),
\qquad
q_2=e_2,
\qquad
Q=[q_1,q_2].
$$

1. 验证 $Q^TQ=I_2$；
2. 计算压缩矩阵 $H=Q^TAQ$ 与 Ritz 值；
3. 求 $\min_{0\ne x\in\operatorname{col}(Q)}\rho_A(x)$；
4. 这个子空间是否达到 Courant–Fischer 对 $\lambda_2$ 的最大值？它是否等于 $\operatorname{span}\{e_1,e_2\}$？解释这两件事为什么不矛盾。

### MA-RQ-B03：广义 Rayleigh 商手算

设

$$
A=\begin{bmatrix}5&0\\0&2\end{bmatrix},
\qquad
B=\begin{bmatrix}1&0\\0&4\end{bmatrix}.
$$

1. 求 $B^{-1/2}AB^{-1/2}$；
2. 求广义 Rayleigh 商的最大值和最小值；
3. 解 $Ax=\lambda Bx$；
4. 验证两个方向在 $B$ 内积下可以归一化为 $B$-标准正交基。

## C 级：推导与证明

### MA-RQ-C01：加权平均与等号条件

设 $A=A^*$，特征值按 $\lambda_1\ge\cdots\ge\lambda_n$ 排列。

1. 从谱分解证明 $\rho_A(x)$ 是特征值的凸组合；
2. 证明 $\lambda_n\le\rho_A(x)\le\lambda_1$；
3. 若 $\lambda_1=\cdots=\lambda_r>\lambda_{r+1}$，完整刻画 $\rho_A(x)=\lambda_1$ 的全部非零向量。

### MA-RQ-C02：重建 Courant–Fischer

不引用现成结论，证明

$$
\lambda_k
=\max_{\dim S=k}\min_{0\ne x\in S}\rho_A(x).
$$

证明必须明确写出：

1. 达到下界的候选子空间；
2. 任意 $k$ 维子空间与哪个 $(n-k+1)$ 维子空间必有非零交；
3. 为什么交中的向量给出上界。

### MA-RQ-C03：Ky Fan 与 PCA

设 $A=A^*$ 且 $Q^*Q=I_k$。

1. 证明
   $$
   \operatorname{tr}(Q^*AQ)
   =\sum_{i=1}^n\lambda_i\|Q^*u_i\|_2^2;
   $$
2. 证明 $0\le p_i=\|Q^*u_i\|_2^2\le1$ 且 $\sum_ip_i=k$；
3. 推出
   $$
   \max_{Q^*Q=I_k}\operatorname{tr}(Q^*AQ)
   =\sum_{i=1}^k\lambda_i;
   $$
4. 说明边界重谱时最优基为什么不唯一。

## D 级：边界、反例与纠错

### MA-RQ-D01：非对称矩阵的失败

取

$$
A=\begin{bmatrix}0&-1\\1&0\end{bmatrix}.
$$

1. 求 $A$ 的复特征值；
2. 对任意实非零 $x$ 计算 $x^TAx/(x^Tx)$；
3. 解释为何该 Rayleigh 商不能刻画一般矩阵的特征值；
4. 若要研究 $A$ 对向量长度的最大放大率，应改研究什么对象？

### MA-RQ-D02：目标唯一但基不唯一

取

$$
A=\operatorname{diag}(5,5,2).
$$

1. 求最大 Rayleigh 商及所有最大化方向；
2. 对 $k=2$ 求 Ky Fan 最大值；
3. 构造两组不同的最优 $Q$；
4. 说明为何给两个顶端特征向量固定命名可能制造虚假差异。

### MA-RQ-D03：不定分母

取

$$
A=I_2,
\qquad
B=\operatorname{diag}(1,-1).
$$

1. 写出 $\rho_{A,B}(x)$；
2. 构造一列非零向量使分母趋于 $0$；
3. 判断该商是否存在有限最大值与最小值；
4. 指出标准广义 Rayleigh 极值证明在哪一步失效。

## E 级：AI 迁移

### AI-RQ-E01：PCA 与解释方差

中心化表示矩阵 $H\in\mathbb R^{m\times d}$，定义

$$
C=\frac1mH^TH.
$$

1. 证明单位方向 $q$ 上的平均平方激活等于 $q^TCq$；
2. 写出前 $k$ 维表示子空间的 Ky Fan 优化；
3. 最优值如何解释为累计方差？
4. 若 $\lambda_k=\lambda_{k+1}$，为什么“前 $k$ 子空间”本身可能也不唯一？

### AI-RQ-E02：Hessian 曲率预算

某损失在参数点附近的 Hessian 为 Hermitian 矩阵 $H$，其极端特征值为

$$
\lambda_1=12,
\qquad
\lambda_n=-0.8.
$$

1. 单位更新方向的二阶项范围是什么？
2. 这能否说明该点局部凸？
3. 若只允许更新位于试探子空间 $\operatorname{col}(Q)$，应分析哪个小矩阵？
4. 给出一项不能只凭这两个特征值判断的训练结论。

### AI-RQ-E03：广义谱目标的选择

有三个候选任务：

1. LDA：最大化类间散度与类内散度之比；
2. 图谱聚类：在正交于常数向量的空间中最小化 Laplacian 商；
3. 表示压缩：最大化投影后的总协方差能量。

分别写出合适的 Rayleigh/Ky Fan 型目标、关键约束和必须检查的退化条件。

## 分级提示

### 方向提示

- B01：先用 $2\sin\theta\cos\theta=\sin2\theta$；
- B02：先算 $Aq_1$，不要默认 $q_1$ 是特征向量；
- C02：使用 $\dim(S\cap L)\ge\dim S+\dim L-n$；
- C03：$QQ^*$ 是秩 $k$ 的正交投影；
- D03：取靠近直线 $x_1=x_2$ 的向量；
- E03：明确普通正交、加权正交和排除零空间三种约束。

### 结构提示

- Courant–Fischer 证明分“构造一个达到值的空间”和“任意空间不可能更好”两半；
- Ky Fan 证明把矩阵优化变成权重 $p_i$ 的线性优化；
- AI 题先写对象和形状，再写目标，不要只报算法名称。

### 计算提示

- B02 中 $q_1^TAq_1=4$，但还需自行计算非对角项；
- B03 中 $B^{-1/2}=\operatorname{diag}(1,1/2)$；
- D03 可令 $x(t)=(1,t)^T$ 并令 $t\to1$。

## 作答记录

| 题号 | 首次状态 | 错误类型 | 回链节点 | 间隔重做 |
|---|---|---|---|---|
| MA-RQ-A01—A03 |  |  | [[Rayleigh 商与极值表征]] |  |
| MA-RQ-B01—B03 |  |  | [[Rayleigh 商与极值表征]] |  |
| MA-RQ-C01—C03 |  |  | [[Rayleigh 商与极值表征]] |  |
| MA-RQ-D01—D03 |  |  | [[Rayleigh 商与极值表征]] |  |
| AI-RQ-E01—E03 |  |  | [[Rayleigh 商与极值表征]] |  |

完整解答见[[解答 - Rayleigh 商与极值表征]]。

