---
type: exercise
status: draft
area: [math/numerical-linear-algebra, math/krylov-methods]
topic: "[[Lanczos 方法]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[幂法、反幂法与 Rayleigh 商迭代]]", "[[标准正交基与 Gram-Schmidt]]", "[[定理 - 有限维谱定理]]"]
related: ["[[解答 - Lanczos 方法]]", "[[实验 - Lanczos Ritz 收敛、残差与正交性]]", "[[Arnoldi 方法]]"]
solution: "[[解答 - Lanczos 方法]]"
created: 2026-08-15
updated: 2026-08-15
---

# 习题 - Lanczos 方法

> [!abstract] 训练目标
> 检查你能否从正交投影推出三项递推，手算小型三对角矩阵，使用 Ritz 残差与谱间隙解释误差，并在有限精度和 AI 隐式算子中设计可信算法。

## A. 识别与复述

### NLA-LAN-A01

定义 Krylov 子空间、Lanczos 基、Ritz 值与 Ritz 向量。说明它们分别属于“搜索空间”“坐标基”“小问题输出”和“原空间近似”中的哪一层。

### NLA-LAN-A02

写出 $k$ 步 Lanczos 分解

$$
AQ_k=Q_kT_k+\beta_kq_{k+1}e_k^T,
$$

标明每个对象的形状，并解释为什么 $T_k$ 是实对称三对角矩阵。

### NLA-LAN-A03

区分 lucky breakdown、数值 breakdown、正交性丢失、ghost Ritz value、锁定与重启。哪些现象表示成功，哪些需要算法处置？

## B. 手算与构造

### NLA-LAN-B01

对

$$
A=\operatorname{diag}(4,2,1),\qquad q_1=(1,1,1)^T/\sqrt3,
$$

手算 $\alpha_1,\beta_1,q_2,\alpha_2,\beta_2,q_3,\alpha_3$，并写出完整 $T_3$。

### NLA-LAN-B02

使用 `B01` 的前两步，求 $T_2$ 的两个特征值并与 $A$ 的谱 $\{4,2,1\}$ 比较。它们是否必须已经位于某个真特征值附近？

### NLA-LAN-B03

已知 $\beta_k=0.04$，归一化 Ritz 向量 $y$ 的最后一个分量为 $e_k^Ty=-0.03$。计算 Ritz 残差范数。若 $\|A\|_2\approx20$、$\varepsilon=10^{-5}$，尺度化停止条件是否满足？

### NLA-LAN-B04

一个对称稀疏矩阵有 $n=10^6$、$\operatorname{nnz}(A)=7\times10^6$，运行 $k=50$ 步。按一次稀疏 matvec 约 $2\operatorname{nnz}(A)$ 浮点运算估算 matvec 总量；再估算保存 $Q_k$ 的双精度内存。说明为何“短递推”与“返回全部 Ritz 向量”有不同存储量。

### NLA-LAN-B05

对特征值 $\{1,2,5\}$ 采用 shift-and-invert，移位 $\sigma=2.1$。写出变换后特征值，指出最大模目标，并计算相对第二大模的幂法收敛因子。

### NLA-LAN-B06

设 $T_2$ 的特征值为 $1.2,3.7$，扩展后的 $T_3$ 特征值为 $0.9,2.1,3.9$。验证交错关系。由此能否断言 $3.9$ 已是 $A$ 的准确最大特征值？

## C. 推导与证明

### NLA-LAN-C01

证明：若 $H_k=Q_k^TAQ_k$ 同时是上 Hessenberg 和对称矩阵，则 $H_k$ 必为三对角矩阵。

### NLA-LAN-C02

从 $q_i^TAq_j=(Aq_i)^Tq_j$ 和已有递推证明：对 $i\le j-2$，$q_i^TAq_j=0$。据此完整推出 Lanczos 三项递推。

### NLA-LAN-C03

若 $T_ky=\theta y$、$\|y\|=1$，由 Lanczos 分解证明

$$
\|A(Q_ky)-\theta Q_ky\|_2=|\beta_ke_k^Ty|.
$$

指出等号使用了哪一个正交性条件。

### NLA-LAN-C04

证明 Ritz 对满足 Galerkin 条件

$$
Q_k^T(AQ_ky-\theta Q_ky)=0.
$$

并用几何语言解释“残差与搜索空间正交”。

### NLA-LAN-C05

假设 $A$ 对称，Ritz 对为 $(\theta,x)$、$\|x\|=1$、残差为 $r$。证明至少存在一个特征值满足

$$
|\lambda_i-\theta|\le\|r\|_2.
$$

再说明为什么要把残差转成单个特征向量误差仍需谱间隙。

### NLA-LAN-C06

证明 $\mathcal K_k(A,q_1)$ 中任一向量可写成 $p_{k-1}(A)q_1$，其中 $\deg p_{k-1}\le k-1$。据此解释 Lanczos 是如何隐式选择谱滤波多项式的。

## D. 边界、反例与纠错

### NLA-LAN-D01

取

$$
A=\begin{bmatrix}0&1\\0&0\end{bmatrix},\qquad q_1=e_2.
$$

说明为什么对它套用“对称 Lanczos 三项递推”会失败，并指出投影矩阵不对称的直接证据。

### NLA-LAN-D02

解释有限精度中已收敛 Ritz 方向为何可能再次渗入后续基向量，并产生重复的 ghost Ritz value。给出至少两种诊断和两种处置。

### NLA-LAN-D03

令 $A=\operatorname{diag}(1,1+\delta)$，$x=(1,1)^T/\sqrt2$，$\theta=x^TAx$。计算残差。说明当 $\delta$ 很小时，为何“小残差”不能证明 $x$ 接近某一个唯一特征向量。

### NLA-LAN-D04

纠正“若 $\beta_k<10^{-12}$ 就一定可以停止”的规则。给出同时考虑算子尺度、目标精度和相对残差的停止量。

### NLA-LAN-D05

纠正“shift-and-invert 应先显式计算 $(A-\sigma I)^{-1}$”的实现建议。分别讨论分解/预条件求解、稀疏填充、内层误差和最终原问题残差。

## E. AI 迁移

### NLA-LAN-E01

你只能调用 Hessian-vector product。设计估计损失 Hessian 最大正曲率与最负曲率的 Lanczos 契约：写出算子、目标、起点、停止、输出和失败诊断。

### NLA-LAN-E02

对中心化数据矩阵 $X\in\mathbb R^{N\times d}$，不显式形成协方差 $C=X^TX/N$。写出 $Cv$ 的实现、Lanczos 所需数据遍历量，并比较与随机 SVD 的适用边界。

### NLA-LAN-E03

用 Lanczos 估计图 Laplacian 的最小非零特征对。解释零特征向量、连通分量、投影约束和 shift-and-invert 各自的作用。

### NLA-LAN-E04

随机 Lanczos 求积（SLQ）估计 $\operatorname{tr}f(A)$。写出单次探针近似

$$
z^Tf(A)z\approx\|z\|^2e_1^Tf(T_k)e_1,
$$

并区分 Krylov 截断误差与随机迹估计误差。

### NLA-LAN-E05

一个模型正则项依赖前几个 Hessian Ritz 值。比较对固定 $k$ 步 Lanczos 计算图求导与对精确简单特征值求导；讨论重根、排序、锁定和内存的影响。

## 分级提示

### 方向提示

- `B01`：本章手算结果从 $\alpha_1=7/3$ 开始；
- `C01`：对称性把 Hessenberg 上方的远带也同时消掉；
- `C03`：代入 $T_ky=\theta y$ 后只剩一个秩一项；
- `D03`：$\theta=1+\delta/2$。

### 结构提示

- `B05`：变换谱为 $1/(\lambda_i-\sigma)$；
- `C06`：Krylov 生成元正是 $I,A,\ldots,A^{k-1}$；
- `E03`：先把常数向量或已知零空间投影掉；
- `E04`：两类误差由 $k$ 与探针数两个独立预算控制。

### 数值提示

- `B03`：绝对残差为 $1.2\times10^{-3}$；
- `B04`：只保存基约需 $400$ MB；
- `B05`：目标为 $\lambda=2$，谱比为 $1/11$。

## 解答入口

完成独立尝试后再打开：[[解答 - Lanczos 方法]]。
