---
type: exercise
status: draft
area: [math/numerical-linear-algebra]
topic: "[[Hessenberg 化与 QR 特征值算法]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[Schur 分解]]", "[[Householder 与 Givens 变换]]", "[[幂法、反幂法与 Rayleigh 商迭代]]"]
related: ["[[解答 - Hessenberg 化与 QR 特征值算法]]", "[[实验 - Hessenberg 约化、移位与 QR deflation]]", "[[Lanczos 方法]]", "[[Arnoldi 方法]]"]
solution: "[[解答 - Hessenberg 化与 QR 特征值算法]]"
created: 2026-08-15
updated: 2026-08-15
---

# 习题 - Hessenberg 化与 QR 特征值算法

> [!abstract] 训练目标
> 检查你能否从双侧正交相似推导 Hessenberg 约化，从正交迭代解释 QR 迭代，手算移位与 deflation，并识别生产 eigensolver 的结构、状态和非正规边界。

## A. 识别与复述

### NLA-HQR-A01

分别定义：上 Hessenberg、未约化 Hessenberg、实 Schur 形式、deflation、bulge chasing。指出每个概念在算法链中的位置。

### NLA-HQR-A02

区分以下对象：一次 QR 分解、无移位 QR 迭代、移位 QR 迭代、Householder Hessenberg 约化。写出每个对象的输入输出等式。

### NLA-HQR-A03

说明 `DGEHRD` 与 `DHSEQR` 分别负责什么；解释 `COMPZ='N'/'I'/'V'` 的用户意图，以及 `INFO>0` 为什么必须报告。

## B. 手算与构造

### NLA-HQR-B01

对

$$
A=\begin{bmatrix}1&2&3\\3&4&5\\4&6&7\end{bmatrix},
$$

构造把 $(3,4)^T$ 映到 $(-5,0)^T$ 的二维 Householder $P$，嵌入 $U=1\oplus P$，计算 $H=U^TAU$ 并检查 $h_{31}=0$ 与迹不变。

### NLA-HQR-B02

对

$$
A_0=\begin{bmatrix}2&1\\1&2\end{bmatrix}
$$

做一步无移位 QR 迭代，要求 $R$ 对角为正。计算 $Q,R,A_1=RQ$，并验证 $A_1=Q^TA_0Q$ 和迹、行列式不变。

### NLA-HQR-B03

对尾部对称块

$$
B=\begin{bmatrix}3&0.4\\0.4&1\end{bmatrix}
$$

计算 Wilkinson shift。先求两个精确特征值，再用稳定公式检查选择的是离 $d=1$ 更近者。

### NLA-HQR-B04

给定

$$
H=\begin{bmatrix}
1&2&3\\
10^{-14}&4&5\\
0&0.2&6
\end{bmatrix}
$$

在双精度 $u\approx1.1\times10^{-16}$ 下，用简化判据

$$
|h_{21}|\le100u(|h_{11}|+|h_{22}|)
$$

判断能否 deflate。再将整个矩阵乘 $10^{12}$，说明相对判据的结果是否变化。

### NLA-HQR-B05

对实 $2\times2$ 块

$$
B=\begin{bmatrix}1&-2\\2&1\end{bmatrix}
$$

计算特征值，并说明为什么实 Schur 形式允许保留这个块，而不能要求实对角化。

### NLA-HQR-B06

用工作量代理“稠密显式 QR 步为 $n^3$、Hessenberg 隐式步为 $6n^2$”，计算 $n=64,256,1024$ 时二者的比值，并解释这不是精确 flop 常数。

## C. 推导与证明

### NLA-HQR-C01

证明移位 QR 步

$$
A_k-\mu I=QR,
\qquad
A_{k+1}=RQ+\mu I
$$

满足 $A_{k+1}=Q^TA_kQ$。

### NLA-HQR-C02

说明第 $k$ 个嵌入反射器 $U_k=I_k\oplus P_k$ 为什么不会破坏前 $k-1$ 列已经形成的 Hessenberg 零，并解释左右两侧各自的作用。

### NLA-HQR-C03

证明若 $H$ 上 Hessenberg，且 $H=QR$ 的 QR 由相邻 Givens 消去次对角元构造，则 $RQ$ 仍为上 Hessenberg。可以使用带宽/列空间论证。

### NLA-HQR-C04

从正交迭代

$$
AZ_k=Z_{k+1}R_{k+1},
\qquad Z_0=I
$$

出发，归纳证明 $T_k=Z_k^TAZ_k$ 与无移位 QR 迭代矩阵一致（假设 QR 唯一符号约定）。

### NLA-HQR-C05

若把 $h_{i+1,i}$ 设置为零，写出扰动矩阵 $E$，证明

$$
\|E\|_F=|h_{i+1,i}|.
$$

解释尺度感知 deflation 为什么是一种后向误差判定。

### NLA-HQR-C06

设计算结果满足 $\widehat Q^T\widehat Q\approx I$、$\widehat T$ 准上三角。说明如何由

$$
E=A-\widehat Q\widehat T\widehat Q^T
$$

构造 Schur 后向残差，并指出正交缺陷为什么必须单独报告。

## D. 边界、反例与纠错

### NLA-HQR-D01

给出一个 $2\times2$ 矩阵和一个正交 $U$，验证只左乘 $U^TA$ 会改变迹或特征值，而双侧 $U^TAU$ 保持它们。

### NLA-HQR-D02

说明绝对判据 `abs(h[i+1,i]) < 1e-12` 为什么不具尺度不变性。构造整体放大/缩小后结论翻转的例子，并写出相对判据。

### NLA-HQR-D03

有人要求实矩阵 QR 迭代最终必须得到实上三角矩阵。用平面旋转矩阵给出反例，并说明正确目标。

### NLA-HQR-D04

考虑

$$
A_\varepsilon=\begin{bmatrix}1&1\\0&1+\varepsilon\end{bmatrix}.
$$

说明 $\varepsilon\to0$ 时特征向量怎样变得近乎平行，以及为什么后向稳定算法仍可能给出前向敏感的单特征向量。

### NLA-HQR-D05

某程序调用 `DHSEQR` 得到 `INFO=37`，却直接返回全部 `WR/WI` 并标记成功。指出契约错误，列出应保存和报告的信息。

## E. AI 与科学计算迁移

### NLA-HQR-E01

Arnoldi 给出

$$
AQ_k=Q_{k+1}\bar H_k,
$$

其中 $Q_k\in\mathbb R^{n\times k}$。说明为什么只需对小型 $H_k$ 做 Schur/QR，写出 Ritz 残差的来源和形状。

### NLA-HQR-E02

DMD 从快照 $X,Y\in\mathbb R^{d\times N}$ 拟合低维演化算子。设计“SVD 降维—低维算子—实 Schur—模态/子空间验收”链，并说明非正规性风险。

### NLA-HQR-E03

训练固定点或循环网络的 Jacobian $J\in\mathbb R^{d\times d}$ 被投影到 $k$ 维子空间。解释为什么小型 Schur 比显式特征向量分解更稳健，以及仅用谱半径判断短期稳定的缺口。

### NLA-HQR-E04

要计算小型非正规矩阵的 $\exp(A)$ 并参与反向传播。说明 Schur 路线的前向优势，以及聚簇、重排、$2\times2$ 块和梯度条件性需要怎样报告。

### NLA-HQR-E05

一个工程师准备在 GPU 上手写“每步 dense QR + RQ”替代供应商 eigensolver。给出评审意见：从复杂度、Hessenberg、移位、AED、数值状态和验证六方面说明最小可接受方案。

## 分级提示

### 方向提示

- `B01`：二维反射为 $[[-0.6,-0.8],[-0.8,0.6]]$；
- `B02`：第一列归一化后为 $(2,1)^T/\sqrt5$；
- `C01`：插入 $Q^TQ$；
- `C05`：$E$ 只有一个非零元素；
- `D03`：实旋转的特征值为复共轭对。

### 结构提示

- `B03`：$\delta=(3-1)/2=1$；
- `C03`：相邻 Givens 的乘积不会产生远离第一条次对角线的非零；
- `C04`：用 QR 唯一性识别 $Z_k^TZ_{k+1}$；
- `E01`：Ritz 残差只沿新生成的 $q_{k+1}$ 方向。

### 计算提示

- `B03`：$\mu=1-0.16/(1+\sqrt{1.16})$；
- `B04`：阈值约 $5.5\times10^{-14}$；
- `B06`：比值代理为 $n/6$。

## 解答入口

完成独立尝试后再打开：[[解答 - Hessenberg 化与 QR 特征值算法]]。

