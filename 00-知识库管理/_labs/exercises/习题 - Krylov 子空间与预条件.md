---
type: exercise
status: draft
area: [math/numerical-linear-algebra, math/krylov-methods]
topic: "[[Krylov 子空间与预条件]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[定常迭代法与谱半径]]", "[[Arnoldi 方法]]", "[[二次型与正定矩阵]]"]
related: ["[[解答 - Krylov 子空间与预条件]]", "[[实验 - 预条件的谱重塑、PCG 收敛与成本权衡]]"]
solution: "[[解答 - Krylov 子空间与预条件]]"
created: 2026-08-15
updated: 2026-08-15
---

# 习题 - Krylov 子空间与预条件

> [!abstract] 训练目标
> 掌握残差多项式、投影、左右/对称预条件和成本模型，并能判断 AI 线性算子的结构是否授权特定方法。

## A. 识别与复述

### NLA-KRY-A01

定义 $\mathcal K_k(A,r_0)$。为什么实际实现不直接使用 $[r_0,Ar_0,\ldots]$ 作为数值基？

### NLA-KRY-A02

比较 FOM、GMRES 与 CG 的搜索空间、测试条件和目标范数。

### NLA-KRY-A03

解释“预条件器是算子接口而不是逆矩阵”。列出一个好预条件器的五个评价维度。

## B. 手算与构造

### NLA-KRY-B01

取

$$
A=\begin{bmatrix}2&1\\0&3\end{bmatrix},\quad r_0=(1,1)^T.
$$

求 $\mathcal K_1,\mathcal K_2,\mathcal K_3$ 的维数，并解释何时空间停止增长。

### NLA-KRY-B02

若 $x_2=x_0+(\alpha I+\beta A)r_0$，写出残差多项式 $p_2(t)$ 并验证 $p_2(0)=1$。

### NLA-KRY-B03

对

$$
A=\begin{bmatrix}4&1\\1&3\end{bmatrix},\quad M=\operatorname{diag}(4,3),
$$

求 $M^{-1}A$ 与 $M^{-1/2}AM^{-1/2}$，比较它们的对称性和特征值。

### NLA-KRY-B04

对 $A=\operatorname{diag}(1,1000)$，比较 $M=I$、$M=\operatorname{diag}(1,100)$ 与 $M=A$ 的广义条件数。若一次应用成本分别为 $1,2,100$，为什么不能只按迭代数选择？

### NLA-KRY-B05

左预条件中某轮 $r=(10^{-3},1)^T$，$M=\operatorname{diag}(10^{-6},1)$。计算 $\|r\|_2$ 与 $\|M^{-1}r\|_2$，说明范数含义。

### NLA-KRY-B06

设计一个 $4\times4$ 两块 Jacobi 预条件器：给出块分区、`apply(r)` 伪代码和设置/每次应用成本的阶数量级。

## C. 推导与证明

### NLA-KRY-C01

证明任意 $x_k\in x_0+\mathcal K_k(A,r_0)$ 的残差都可写成 $r_k=p_k(A)r_0$，其中 $\deg p_k\le k$ 且 $p_k(0)=1$。

### NLA-KRY-C02

由 Arnoldi 分解推导 GMRES 小最小二乘

$$
\min_y\|\beta e_1-\bar H_ky\|_2.
$$

### NLA-KRY-C03

若 $A$ 与 $M$ 都 SPD，证明 $M^{-1}A$ 与 $M^{-1/2}AM^{-1/2}$ 相似，并说明其特征值为正实数。

### NLA-KRY-C04

证明谱等价

$$
c_1v^TMv\le v^TAv\le c_2v^TMv
$$

推出 $\sigma(M^{-1}A)\subset[c_1,c_2]$。

### NLA-KRY-C05

对可对角化 $A=V\Lambda V^{-1}$ 推导

$$
\|p(A)\|_2\le\kappa_2(V)\max_i|p(\lambda_i)|.
$$

为什么它提示非正规问题不能只画特征值？

### NLA-KRY-C06

若 $A$ 的最小多项式相对于 $r_0$ 的次数为 $m$，证明存在 $x_m\in x_0+\mathcal K_m$ 使残差为零。

## D. 边界、反例与纠错

### NLA-KRY-D01

纠正“$A,M$ 都 SPD，所以 $M^{-1}A$ 是对称矩阵”。指出正确结构。

### NLA-KRY-D02

给出一个预条件残差很小但真残差不小的例子。最终停止应如何验收？

### NLA-KRY-D03

为什么让内层预条件求解每次使用不同容差，可能破坏普通 CG 或右预条件 GMRES？应换什么框架？

### NLA-KRY-D04

反驳“块越大，预条件一定越好”。同时考虑谱、设置、应用、并行和复用。

### NLA-KRY-D05

某学习型预条件器在平均测试集上把迭代数减半。设计一份不足以被平均数掩盖的验收清单。

## E. AI 迁移

### NLA-KRY-E01

为 Hessian-free 阻尼牛顿步设计 matrix-free 求解：HVP、预条件、方法选择、停止和负曲率检测分别如何处理？

### NLA-KRY-E02

隐式微分要求解 $(I-J_f^T)v=g$。为什么不能默认 PCG？给出结构检查与备选方法。

### NLA-KRY-E03

为 Transformer 中一个具有层/头块结构的线性系统设计块预条件实验；如何避免只报告训练分布上的迭代数？

### NLA-KRY-E04

多个相邻优化步的线性系统共享难解方向。设计 Krylov 子空间回收/低秩校正，并说明何时应丢弃旧子空间。

### NLA-KRY-E05

一个神经预条件器是含 ReLU 的非线性映射。说明它与标准 PCG 假设的冲突，并给出安全外层方案与验收量。

## 分级提示

- `B01`：检查 $r_0$ 与 $Ar_0$ 是否线性相关；
- `B03`：相似矩阵特征值相同，但元素对称性不同；
- `C04`：使用广义 Rayleigh 商；
- `C06`：相对最小多项式 $m(A)r_0=0$，且若 $A$ 非奇异则 $m(0)\ne0$；
- `D02`：选择尺度悬殊的 $M$；
- `E02`：先检查对称性与正定性，再谈算法。

## 解答入口

完成独立尝试后再打开：[[解答 - Krylov 子空间与预条件]]。
