---
type: exercise
status: draft
area: [math/numerical-linear-algebra, math/randomized-linear-algebra]
topic: "[[随机化低秩近似与随机 SVD]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[奇异值分解]]", "[[定理 - Eckart–Young–Mirsky]]", "[[SVD 算法与谱范数估计]]"]
related: ["[[解答 - 随机化低秩近似与随机 SVD]]", "[[实验 - 随机 SVD 的过采样、幂步与概率证书]]"]
solution: "[[解答 - 随机化低秩近似与随机 SVD]]"
created: 2026-08-15
updated: 2026-08-15
---

# 习题 - 随机化低秩近似与随机 SVD

> [!abstract] 训练目标
> 从 range finder 的手算进入确定性误差骨架、概率证书、pass 复杂度和 AI 部署，建立“随机采样—稳定正交—小问题—独立验收”的完整链。

## A. 识别与复述

### NLA-RLA-A01

解释 randomized SVD 的 Stage A 与 Stage B。随机性主要出现在哪里？

### NLA-RLA-A02

区分目标秩 \(k\)、过采样 \(p\)、sketch 维数 \(\ell\) 和幂参数 \(q\)。

### NLA-RLA-A03

比较谱范数误差、Frobenius 范数误差、子空间角和下游任务误差。

### NLA-RLA-A04

比较 Gaussian、Rademacher、SRHT 和 CountSketch 的主要优点与限制。

### NLA-RLA-A05

比较 truncated SVD、Nyström、CUR 与 ID 的因子结构和适用对象。

## B. 手算与构造

### NLA-RLA-B01

令

$$
A=\operatorname{diag}(5,2,1),\quad
\Omega=(1,1,0)^T.
$$

取 \(\ell=1\)，求 \(Y=A\Omega\)、单位基 \(Q\) 与投影误差 \(\|(I-QQ^T)A\|_2\)。

### NLA-RLA-B02

仍取 B01 的 \(A\)，改用

$$
\Omega=
\begin{bmatrix}
1&0\\
1&1\\
0&1
\end{bmatrix}.
$$

说明 \(Y=A\Omega\) 的列空间维数，并构造一个与其正交的单位向量；用它表达投影残差的谱范数。

### NLA-RLA-B03

对奇异值

$$
[10,5,2,1,0.5],
$$

目标秩 \(k=2\)。计算最佳 rank-2 的谱误差和 Frobenius 误差；再计算 \(q=1\) 幂变换后的奇异值。

### NLA-RLA-B04

后验测试取 \(\alpha=10,r=6\)，观测

$$
\max_i\|R\omega_i\|_2=0.012.
$$

计算谱范数证书上界与名义失败概率。

### NLA-RLA-B05

一个稠密 \(m=10^6,n=10^4\) 矩阵，取 \(k=40,p=10\)。只按数量级估算 \(A\Omega\)、正交化与完整 SVD 的主工作量，说明随机路线的优势条件。

## C. 推导与证明

### NLA-RLA-C01

由 \(Y=A\Omega\)、\(Y=QR\) 和 \(B=Q^TA\) 推导 \(QB=QQ^TA\)，并证明 \(QQ^T\) 是正交投影。

### NLA-RLA-C02

用 SVD 分块和

$$
\Omega_1=V_1^T\Omega,\quad \Omega_2=V_2^T\Omega
$$

解释确定性界中

$$
\Sigma_2\Omega_2\Omega_1^\dagger
$$

的三个因素分别代表什么。

### NLA-RLA-C03

证明

$$
(AA^T)^qA=U\Sigma^{2q+1}V^T
$$

并说明为什么幂方案必须间歇重正交。

### NLA-RLA-C04

若值域近似 \(Q\) 已固定，证明在 \(\mathcal R(Q)\) 中最佳 Frobenius 范数 rank-\(k\) 近似可由 \(B=Q^TA\) 的截断 SVD 得到。

### NLA-RLA-C05

从失败界 \(\alpha^{-r}\) 推导：若希望名义失败概率不超过 \(10^{-9}\)，取 \(\alpha=10\) 时至少需要多少个独立探针？为什么它仍不是确定性证书？

## D. 边界、反例与纠错

### NLA-RLA-D01

反驳“Gaussian \(\Omega\) 以概率 \(1\) 捕获 rank-\(k\) 子空间，所以 \(p=0\) 与 \(p=10\) 没区别”。

### NLA-RLA-D02

构造一个没有低秩结构的矩阵，说明 randomized SVD 误差大不等于算法失效。

### NLA-RLA-D03

为什么把 \(Y=(AA^T)^qA\Omega\) 按公式直接形成 \(AA^T\) 和矩阵幂通常是数值与计算上的坏实现？

### NLA-RLA-D04

用构造 \(Q\) 的同一批随机向量计算后验误差。指出偏差来源，并给出修正实验。

### NLA-RLA-D05

一个实现只报告单 seed 的 Frobenius 相对误差。列出至少七项缺失的可靠性信息。

## E. AI 迁移

### NLA-RLA-E01

设计大规模 PCA 的 randomized SVD 实验，覆盖中心化、explained variance、子空间稳定、多 seed 和流式 pass。

### NLA-RLA-E02

计划用随机 SVD 初始化 LoRA。说明该初始化能证明什么、不能证明什么，并设计与随机初始化的公平对照。

### NLA-RLA-E03

对 Transformer 激活做在线低秩压缩。写出误差—延迟—内存合同，并说明固定矩阵离线最优为何不够。

### NLA-RLA-E04

用 Nyström 近似 PSD 核矩阵。写出构造、PSD 保持条件，以及采样偏置和 \(W^\dagger\) 病态性的检查。

### NLA-RLA-E05

矩阵分布在 64 个 worker 上，只允许两次全数据 pass。设计一个可合并 sketch、正交化、独立验证和通信报告方案。

## 分级提示

- B01：\(Q=(5,2,0)^T/\sqrt{29}\)，残差可从二维块的最大特征值求；
- B02：找同时正交于 \((5,2,0)^T\) 与 \((0,2,1)^T\) 的向量；
- B04：使用 \(\alpha\sqrt{2/\pi}\)；
- C04：把候选写成 \(QX\)，利用 \(Q\) 的等距性；
- C05：解 \(10^{-r}\le10^{-9}\)。

## 解答入口

完成独立尝试后再打开：[[解答 - 随机化低秩近似与随机 SVD]]。
