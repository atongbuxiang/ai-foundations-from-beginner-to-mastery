---
type: solution
status: verified
area: [training, optimization, matrix-analysis, muon]
topic: "[[矩阵梯度、谱核范数对偶与 Matrix Sign]]"
exercise: "[[习题 - 矩阵梯度、谱核范数对偶与 Matrix Sign]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - 矩阵梯度、谱核范数对偶与 Matrix Sign

> [!warning] 使用边界
> 本文件把 SVD-type polar/msign、classical matrix sign 与 finite-step polynomial 分开。若算法未做 exact SVD/root，解答中的 exact identities只能作为 reference target。

## A. 识别与复述

### TRN26-A01
$G$ 由
$$
DL(W)[\Delta]=\operatorname{tr}(G^T\Delta)=\langle G,\Delta\rangle_F
$$
定义。pairing 负责表示 differential；step norm 负责定义允许的一步。二者是两个槽位：可用 Frobenius pairing 表示 gradient，同时用 spectral norm、nuclear norm 或加权 norm 限制 $\Delta$。

### TRN26-A02
若奇异值为 $\sigma_i$：
$$
\lVert G\rVert_2=\max_i\sigma_i,\qquad
\lVert G\rVert_F=\sqrt{\sum_i\sigma_i^2},\qquad
\lVert G\rVert_*=\sum_i\sigma_i.
$$
故
$$
\lVert G\rVert_2\le\lVert G\rVert_F\le\lVert G\rVert_*
\le\sqrt r\,\lVert G\rVert_F
\le r\,\lVert G\rVert_2.
$$
更紧的具体界取决于 rank 与 spectrum。

### TRN26-A03
SVD-type msign 对矩形矩阵 $G=U_r\Sigma_rV_r^T$ 定义为 $U_rV_r^T$，把正 singular values 变成 1。Classical sign 对满足谱条件的方阵按 $A(A^2)^{-1/2}$ 或解析矩阵函数定义，变换 eigenvalues。finite-step NS 只是多项式/rational iteration 的某次输出，依赖 scaling、steps 和 arithmetic；三者不能按名称互换。

## B. 手算与构造

### TRN26-B01
$G$ 的 nuclear norm 为 5，polar 为 $I$。spectral-unit 最速下降方向是 $-I$，pairing $-5$。Frobenius-unit 方向是
$$
-\frac{G}{\sqrt{17}},
$$
pairing 为 $-\sqrt{17}\approx-4.123$。后者也满足 spectral norm $\le1$，但未在第二奇异方向上用满预算。

### TRN26-B02
canonical factor 为
$$
Q_c=\begin{bmatrix}1&0\\0&0\\0&0\end{bmatrix}.
$$
另两种 maximizer：
$$
Q_1=\begin{bmatrix}1&0\\0&1\\0&0\end{bmatrix},\qquad
Q_2=\begin{bmatrix}1&0\\0&0\\0&1\end{bmatrix}.
$$
二者列正交，spectral norm 为 1，且 $\langle G,Q_i\rangle_F=3=\lVert G\rVert_* $。差异完全位于 $G$ 看不见的 null-space。

### TRN26-B03
$$
G^TG=\operatorname{diag}(1,4),
\qquad
(G^TG)^{-1/2}=\operatorname{diag}(1,1/2).
$$
所以
$$
Q=G(G^TG)^{-1/2}
=\begin{bmatrix}0&1\\1&0\end{bmatrix}.
$$
$\lVert Q\rVert_2=1$，$\lVert Q\rVert_F=\sqrt2$，并且
$$
\langle G,Q\rangle_F=2+1=3=\lVert G\rVert_*.
$$

## C. 推导与证明

### TRN26-C01
设 $G=U\Sigma V^T$。von Neumann inequality 给
$$
\langle G,\Delta\rangle_F
\le\sum_i\sigma_i(G)\sigma_i(\Delta).
$$
若 $\lVert\Delta\rVert_2\le1$，则每个 $\sigma_i(\Delta)\le1$，故右侧不超过 $\sum_i\sigma_i(G)=\lVert G\rVert_* $。取 $\Delta=U_rV_r^T$ 时 spectral norm 为 1，且 trace pairing 正好为 $\operatorname{tr}\Sigma_r$，所以上界达到。

### TRN26-C02
compact SVD $G=U\Sigma V^T$，列满秩使 $\Sigma$ 可逆。于是
$$
G^TG=V\Sigma^2V^T,\qquad
(G^TG)^{-1/2}=V\Sigma^{-1}V^T.
$$
相乘得
$$
G(G^TG)^{-1/2}=UV^T=Q.
$$
再算 $Q^TQ=VU^TUV^T=I_n$。若不满列秩，普通 inverse 不存在，需 pseudoinverse/support 定义。

### TRN26-C03
在补全基下，$G$ 只占 $U_r,V_r$ block。任意
$$
Q_K=U_rV_r^T+U_0KV_0^T,\quad\lVert K\rVert_2\le1
$$
的两个 block 作用于正交 domain/range，故 $\lVert Q_K\rVert_2=\max(1,\lVert K\rVert_2)=1$，且第二项与 $G$ pairing 为零，所以达到同一极值。Frobenius 正交分解给
$$
\lVert Q_K\rVert_F^2=r+\lVert K\rVert_F^2,
$$
最小值在 $K=0$ 唯一取得。

## D. 边界、反例与纠错

### TRN26-D01
直接相乘得
$$
A^2=\begin{bmatrix}1&0\\0&1\end{bmatrix}.
$$
其 eigenvalues 为 $\pm1$，classical sign 保持它们，故 sign$(A)=A$。但 $A^TA\ne I$，且 $\lVert A\rVert_2>1$；满秩 polar factor 必须正交，所以 polar$(A)\ne A$。该例删除了“eigenvalue sign 等于 singular-value sign”的混淆。

### TRN26-D02
若 exact polar 为 $Q=UV^T$，取 $\Delta=-Q$。它的 spectral norm 仍为 1，但
$$
\langle G,\Delta\rangle_F=-\lVert G\rVert_*,
$$
是最大上升方向的相反号，而不是 maximizer；若优化下降方向，则反过来取 $+Q$ 也会错。norm feasibility 只是一道门，alignment/pairing 才决定线性目标。

### TRN26-D03
有限步输出的 singular values 是多项式迭代值而非精确 1。rank deficiency 使零值永远为零；initial scaling 决定是否进入 attraction interval；step count 决定小 singular value 是否被拉起；dtype/GEMM error 可使 residual 反弹。必须报告 orthogonality、polar alignment、direction/dual gap，而非按函数名授予 exact 标签。

## E. AI 迁移

### TRN26-E01
用 FP64 SVD 构造 $Q_{ref}=U_rV_r^T$。四类输入分别覆盖 tall/wide、已知 rank 缺失、log-spaced condition、clustered singular values。断言：

- 输出 shape 正确且 finite；
- spectral norm 不超预算容差；
- pairing 接近 nuclear norm；
- direction cosine 接近 reference；
- orthogonality target 按 tall/wide/rank support 选择 projector；
- exact canonical routine 在 null-space 不添加额外 Frobenius energy。

### TRN26-E02
字段至少包括 target_type（polar/msign/classical-sign）、solver（SVD/root/NS）、implementation/version、input scaling、rank tolerance、steps、coefficients、input/compute/accumulation dtype、shape/layout、orthogonal residual、polar residual、direction cosine、dual gap 与 reference precision。

### TRN26-E03
准确说法是：Muon 对选定二维 parameter 的 momentum matrix 应用有限步 NS，多数情况下近似其 SVD-type polar direction；full-rank exact target 的非零 singular values 为 1。矩形输出只在较小维一侧正交，rank-deficient target 是 partial isometry，finite-step singular values 未必为 1，随后还会做 shape scaling。因此“归一化为正交矩阵”既遗漏对象，也遗漏近似和尺度。

## 无提示重做

- [ ] 48 小时后从 von Neumann inequality 重证 spectral/nuclear duality。
- [ ] 一周后用一个 rank-1 矩阵和一个非正规 involution 区分 non-uniqueness 与 classical sign。
