---
type: exercise
status: draft
area: [math/numerical-linear-algebra]
topic: "[[幂法、反幂法与 Rayleigh 商迭代]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[特征分解]]", "[[二次型与正定矩阵]]", "[[稳定求解线性方程组]]"]
related: ["[[解答 - 幂法、反幂法与 Rayleigh 商迭代]]", "[[实验 - 谱间隙、移位与 Rayleigh 商迭代收敛]]", "[[Hessenberg 化与 QR 特征值算法]]"]
solution: "[[解答 - 幂法、反幂法与 Rayleigh 商迭代]]"
created: 2026-08-15
updated: 2026-08-15
---

# 习题 - 幂法、反幂法与 Rayleigh 商迭代

> [!abstract] 训练目标
> 检查你能否从谱展开重建收敛率，手算三类迭代，使用残差和谱间隙验收结果，并在非正规、聚簇和 AI 大规模算子中识别理论边界。

## A. 识别与复述

### NLA-EIG-A01

分别说明幂法、固定移位反幂法和 RQI 的目标特征值、每步核心运算、可复用分解和主要收敛条件。

### NLA-EIG-A02

区分“最大模特征值”“最大代数特征值”“离 $\sigma$ 最近的特征值”和“最大奇异值”。为每个对象给出一个适合的迭代入口。

### NLA-EIG-A03

解释 Rayleigh 商变化量、特征残差、方向角和谱间隙分别提供什么信息。哪一个应作为最基本的停止指标？

## B. 手算与构造

### NLA-EIG-B01

对

$$
A=\operatorname{diag}(5,2),
\qquad x_0=(1,1)^T/\sqrt2,
$$

手算 $x_1,x_2$ 和 $\rho_1,\rho_2$，并写出第二分量相对第一分量的变化。

### NLA-EIG-B02

若初始方向误差常数为 $1$，谱比分别为 $0.2,0.8,0.98$，估计把误差降到 $10^{-6}$ 至少需要多少步。使用

$$
k\ge\frac{\log10^{-6}}{\log r}.
$$

### NLA-EIG-B03

对 $A=\operatorname{diag}(-4,1)$、$x_0=(1,1)^T/\sqrt2$ 计算前三个归一化方向的符号模式。给出不受符号翻转影响的误差度量。

### NLA-EIG-B04

对

$$
A=\operatorname{diag}(5,2,1),
\quad \sigma=1.9,
\quad x_0=(1,1,1)^T/\sqrt3,
$$

计算一次反幂步骤的未归一化 $y_1$，并比较三个分量相对目标分量的比例。

### NLA-EIG-B05

取 $A=\operatorname{diag}(1,3)$，单位向量

$$
x=(\sin\theta,\cos\theta)^T
$$

靠近 $e_2$。计算 Rayleigh 商，并证明一次 RQI 后新角度满足

$$
|\tan\theta_+|=|\tan\theta|^3.
$$

### NLA-EIG-B06

对 $A=\operatorname{diag}(1,2,5)$ 和单位向量 $x=(0,\sqrt{0.99},0.1)^T$，计算 $\rho$、残差范数以及到最近特征值的距离，验证

$$
\min_i|\rho-\lambda_i|\le\|r\|.
$$

## C. 推导与证明

### NLA-EIG-C01

设对称矩阵按模满足 $|\lambda_1|>|\lambda_2|\ge\cdots$，且 $x_0=\sum_i\alpha_iq_i$、$\alpha_1\ne0$。完整推导幂法方向误差为

$$
O\left(|\lambda_2/\lambda_1|^k\right).
$$

### NLA-EIG-C02

对称矩阵中，令 $x=\cos\theta\,q_1+\sin\theta\,w$，其中 $w\perp q_1$、$\|w\|=1$。证明

$$
|\rho(x)-\lambda_1|
\le(\lambda_1-\lambda_n)\sin^2\theta.
$$

### NLA-EIG-C03

用特征基展开证明

$$
\min_i|\rho-\lambda_i|\le\|Ax-\rho x\|
$$

对单位向量 $x$ 成立。

### NLA-EIG-C04

推导固定移位反幂法目标 $\lambda_j$ 相对于第二近特征值 $\lambda_\ell$ 的收敛因子

$$
\left|\frac{\lambda_j-\sigma}{\lambda_\ell-\sigma}\right|.
$$

### NLA-EIG-C05

把“Rayleigh 商误差二阶”和“反幂方向更新”组合，给出对称 RQI 局部三次收敛的证明骨架，并逐条列出假设。

### NLA-EIG-C06

正交迭代满足 $Y_{k+1}=AZ_k$、$Y_{k+1}=Z_{k+1}R_{k+1}$。证明若 $\mathcal S_k=\mathcal R(Z_k)$，则

$$
\mathcal S_{k+1}=A\mathcal S_k
$$

在满秩情况下成立，并解释为什么 QR 不改变子空间却防止列塌缩。

## D. 边界、反例与纠错

### NLA-EIG-D01

构造一个 $2\times2$ 对角矩阵，使两个特征值模相同但特征值不同，并说明幂法为何不收敛到唯一方向。

### NLA-EIG-D02

给出 $x_0$ 与主特征向量精确正交的例子，证明幂法以后每一步仍没有主方向分量。

### NLA-EIG-D03

对 Jordan 块

$$
J=\begin{bmatrix}\lambda&1\\0&\lambda\end{bmatrix}
$$

求 $J^k$，说明为什么只看特征值 $\lambda^k$ 会漏掉暂态多项式因子。

### NLA-EIG-D04

纠正“反幂法先计算 `inv(A-σI)`，以后矩阵乘就快了”的建议。比较分解复用、稀疏性、舍入和验收。

### NLA-EIG-D05

构造或解释一个情形，其中 $|\rho_{k+1}-\rho_k|$ 很小，但特征残差仍不够小。说明为何只监控 Rayleigh 商变化可能提前停止。

## E. AI 迁移

### NLA-EIG-E01

谱归一化对 $W\in\mathbb R^{d_{out}\times d_{in}}$ 每次训练只做一步奇异值幂迭代。写出 $u,v$ 更新、形状、所得承诺和在谱隙小或权重快速变化时的失败模式。

### NLA-EIG-E02

你只能调用 Hessian-vector product，想估计损失 Hessian 的最大正特征值与最负特征值。说明为什么单次“最大模幂法”不够，并提出方法组合与验收量。

### NLA-EIG-E03

流式块幂迭代中 $V_t\in\mathbb R^{n\times p}$。解释每步 QR 的作用，比较 Householder QR 与 Cholesky QR，并写出正交性与子空间残差指标。

### NLA-EIG-E04

随机 SVD 对 $A\in\mathbb R^{m\times n}$ 使用 $Y=(AA^T)^qA\Omega$。说明幂参数 $q$ 怎样改变奇异值比例、为什么每轮要正交化，以及过大的 $q$ 有什么有限精度风险。

### NLA-EIG-E05

一个可微层展开 $K$ 步幂法。比较“对有限 $K$ 步算法求导”与“对精确特征向量求导”，说明 gap、初始化和 stop-gradient 怎样改变梯度含义。

## 分级提示

### 方向提示

- `B05`：先写 $\rho=1\sin^2\theta+3\cos^2\theta$；
- `C01`：从 $A^kx_0$ 提取 $\lambda_1^k$；
- `C03`：残差平方是带权距离平方和；
- `D03`：写 $J=\lambda I+N$ 且 $N^2=0$；
- `E04`：奇异值被提升到 $\sigma_i^{2q+1}$。

### 结构提示

- `B06`：三个坐标中只有第二、第三坐标非零；
- `C04`：对 $(A-\sigma I)^{-1}$ 应用幂法谱比；
- `C06`：QR 改变基，不改变列空间；
- `D05`：聚簇特征值可让特征值估计稳定而方向仍慢。

### 计算提示

- `B02`：结果约为 $9,62,684$ 步；
- `B06`：$\rho=2.03$；
- `D01`：可取 $\operatorname{diag}(1,-1)$。

## 解答入口

完成独立尝试后再打开：[[解答 - 幂法、反幂法与 Rayleigh 商迭代]]。

