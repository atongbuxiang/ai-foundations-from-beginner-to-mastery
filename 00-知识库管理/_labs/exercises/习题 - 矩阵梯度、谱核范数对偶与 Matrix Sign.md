---
type: exercise
status: verified
area: [training, optimization, matrix-analysis, muon]
topic: "[[矩阵梯度、谱核范数对偶与 Matrix Sign]]"
solution: "[[解答 - 矩阵梯度、谱核范数对偶与 Matrix Sign]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - 矩阵梯度、谱核范数对偶与 Matrix Sign

> [!abstract] 训练目标
> 从 Frobenius pairing 和 SVD 证明 spectral/nuclear duality；能处理 rank-deficient non-uniqueness，并严格区分 polar/msign、classical matrix sign 与 finite-step polynomial。

## A. 识别与复述

### TRN26-A01
矩阵梯度 $G$ 如何通过 Frobenius pairing 定义？为什么 pairing 使用 Frobenius 内积不表示 step budget 必须使用 Frobenius norm？

### TRN26-A02
给出 spectral norm、nuclear norm 和 Frobenius norm 的奇异值表达，并写出它们之间的基本不等式。

### TRN26-A03
分别定义本卷的 SVD-type msign/polar factor 与 classical square-matrix sign；指出定义域、变换对象和数值计算目标的差异。

## B. 手算与构造

### TRN26-B01
对 $G=\operatorname{diag}(4,1)$，求 spectral-unit 最速方向、最大预测下降、Frobenius-unit 最速方向及两者的预测下降。

### TRN26-B02
令
$$
G=\begin{bmatrix}3&0\\0&0\\0&0\end{bmatrix}\in\mathbb R^{3\times2}.
$$
写出 canonical polar factor，并构造至少两个不同的 spectral-unit maximizer，使其与 $G$ 的 pairing 都等于 $\lVert G\rVert_*$。

### TRN26-B03
对
$$
G=\begin{bmatrix}0&2\\1&0\end{bmatrix},
$$
手算 SVD-type msign。再验证其 spectral norm、Frobenius norm 与 $\langle G,\operatorname{msign}(G)\rangle_F$。

## C. 推导与证明

### TRN26-C01
使用 von Neumann trace inequality 证明
$$
\sup_{\lVert\Delta\rVert_2\le1}\langle G,\Delta\rangle_F=\lVert G\rVert_*,
$$
并说明 $U_rV_r^T$ 如何达到等号。

### TRN26-C02
证明列满秩 $G\in\mathbb R^{m\times n}$（$m\ge n$）的 polar factor满足
$$
Q=G(G^TG)^{-1/2},
$$
且 $Q^TQ=I$。

### TRN26-C03
刻画 rank-deficient 情形的一族最优解
$$
U_rV_r^T+U_0KV_0^T,\qquad \lVert K\rVert_2\le1,
$$
并证明 canonical choice $K=0$ 在该族中具有最小 Frobenius norm。

## D. 边界、反例与纠错

### TRN26-D01
取
$$
A=\begin{bmatrix}1&1\\0&-1\end{bmatrix}.
$$
验证 $A^2=I$，从而 classical sign$(A)=A$；再说明 polar/msign$(A)$ 不可能等于 $A$。这反驳了什么混淆？

### TRN26-D02
反驳“只要输出矩阵 spectral norm 为 1，它就是 $G$ 的最速方向”。构造一个 norm 合格但 pairing 很差甚至方向相反的矩阵。

### TRN26-D03
解释为什么有限步 Newton–Schulz 输出不能在无 residual 证据时标记为 exact polar；至少列出 rank、initial scaling、step count 与 dtype 四个失败轴。

## E. AI 迁移

### TRN26-E01
设计一个 SVD reference test：输入 tall、wide、rank-deficient 和 ill-conditioned 四类矩阵，验证一个 msign 实现的 feasibility、pairing 与 canonical-null-space 行为。

### TRN26-E02
为训练日志设计字段，使读者能区分 exact SVD polar、finite-step NS output 与 classical sign routine，并记录对应残差。

### TRN26-E03
审计一句话：“Muon 把每个矩阵梯度归一化为正交矩阵。”指出对矩形、rank-deficient、finite-step 和 shape-scaled 情形应如何改写才准确。

## 作答与复盘

每题记录 independent / hinted / copied / blocked / careless。先手算 SVD 与 rank support，再打开 [[解答 - 矩阵梯度、谱核范数对偶与 Matrix Sign]]。
