---
type: solution
status: draft
area: [neural-networks/initialization, orthogonal-initialization, dynamical-isometry]
topic: "[[正交初始化与 Dynamical Isometry]]"
exercise: "[[习题 - 正交初始化与 Dynamical Isometry]]"
sources: ["[[S-2014-Saxe-Deep-Linear-Dynamics]]", "[[S-2017-Pennington-Dynamical-Isometry]]", "[[S-2026-PyTorch-NN-Init]]"]
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - 正交初始化与 Dynamical Isometry

## A

### NN-DISO-A01
Square orthogonal：$Q\in\mathbb R^{n\times n}$ 且 $Q^TQ=QQ^T=I$，输入输出全空间双向保长。Column-semi-orthogonal：$W\in\mathbb R^{m\times n},m\ge n,W^TW=I_n$，从整个 $\mathbb R^n$ 等距嵌入。Row-semi-orthogonal：$m\le n,WW^T=I_m$，$W^T$ 对输出空间保长，$W$ 只在 row space 上保长并有 kernel。

### NN-DISO-A02
Mean squared singular value 稳定只要求 $r^{-1}\sum_i s_i^2\approx1$；condition number 可控要求 $s_{\max}/s_{\min}$ 不大；dynamical isometry 要求所有 relevant $s_i$ 都集中在 1 附近。前者允许一个方向接近 0、另一个变大，后两者逐步排除这种不均匀。

### NN-DISO-A03
若 $h^\ell=\phi(W_\ell h^{\ell-1}+b_\ell)$，则
$$J=D_LW_L\cdots D_1W_1,
\qquad D_\ell=\operatorname{diag}(\phi'(z^\ell)).$$
除 $W_\ell$ 外还有 activation derivative matrices；矩形 shape、normalization、residual addition 等结构会进一步改变 factorization。

## B

### NN-DISO-B01
$W^TW=I_3$ 可逆于 input side，所以 $\operatorname{rank}W=3$。$W^TW$ 的 eigenvalues 全为 1，因此三个 singular values 全为 1。任意 $x$ 满足
$$\|Wx\|^2=x^TW^TWx=x^Tx=\|x\|^2.$$
它是从三维空间到五维空间的等距嵌入。

### NN-DISO-B02
$WW^T=I_3$ 给 rank $W=3$。由 rank–nullity，$\dim\ker W=5-3=2$。$W^TW$ 是投影到 row space 的 rank-3 orthogonal projector，eigenvalues 为
$$\{1,1,1,0,0\}.$$
所以它不能对 kernel directions 保长。

### NN-DISO-B03
乘积
$$J=g^LQ_L\cdots Q_1$$
是 scalar $g^L$ 乘 orthogonal matrix，全部 singular values 为 $|g|^L$。$1.01^{100}\approx2.7048$，所以每个方向的 amplitude 已放大约 2.70，平方长度约放大 7.32；单层 1% 偏差会沿 depth 相乘。

## C

### NN-DISO-C01
若 $A^TA=B^TB=I$，则
$$(AB)^T(AB)=B^TA^TAB=B^TB=I.$$
归纳得 $Q_L\cdots Q_1$ 正交。Deep linear network 的 Jacobian 等于这一 product，因此 $J^TJ=I$，所有 singular values 精确为 1，满足 dynamical isometry。

### NN-DISO-C02
取二维 $W_1=W_2=I_2$，选择输入使第一层 ReLU mask
$$D_1=\operatorname{diag}(1,0),\qquad D_2=I_2.$$
则
$$J=D_2W_2D_1W_1=\operatorname{diag}(1,0),$$
rank 为 1。两个 weight matrices 都正交，activation derivative 已删掉一个方向。

### NN-DISO-C03
两个 singular values 是 $\sqrt{2-\varepsilon^2}$ 与 $\varepsilon$，故
$$\frac{s_1^2+s_2^2}{2}=\frac{2-\varepsilon^2+\varepsilon^2}{2}=1.$$
但
$$\kappa(J_\varepsilon)=\frac{\sqrt{2-\varepsilon^2}}{\varepsilon}\to\infty.$$
这给出“平均平方正确、最坏方向任意坏”的精确反例。

## D

### NN-DISO-D01
若 $m<n$，任何 $W:\mathbb R^n\to\mathbb R^m$ 都有至少 $n-m$ 维 kernel，非零 kernel vector 被映到 0，不可能对所有输入保长。若 $m>n$ 且 columns orthonormal 才能对整个输入空间保长；所以必须声明 shape 与哪侧 orthonormal。

### NN-DISO-D02
Reshape 后的 kernel matrix 忽略 spatial overlap、stride、padding、boundary 与 weight sharing。真实 convolution operator 是更大的结构化矩阵，其 singular spectrum 不由 kernel reshape 的 $QQ^T$ 单独决定。反例可取 stride/padding 导致部分输入像素从未被覆盖，即使 reshape matrix rows orthonormal，operator 仍有额外 null directions。

### NN-DISO-D03
普通更新 $W^+=W-\eta G$ 后
$$(W^+)^TW^+=I-\eta(W^TG+G^TW)+\eta^2G^TG,$$
一般不等于 $I$。只有 gradient 位于合适 tangent direction 并配合 manifold-preserving update/retraction 才能保持约束；初始化正交不是训练约束。

## E

### NN-DISO-E01
在小网络对同一 batch 显式形成 $J$，用 SVD 得 ground-truth singular values。再只用自动微分 JVP/VJP 实现 power iteration、Hutchinson trace 与 Lanczos，比较 $s_{\max}$、$\operatorname{tr}(J^TJ)$、谱分位近似误差。确认 operator uses exact train/eval state and dtype。大网络只跑 matrix-free 路线，并用缩小 width/depth 的重叠区验证 estimator bias。

### NN-DISO-E02
先定义 data tangent basis $T\in\mathbb R^{n\times k}$，$T^TT=I$，且 $k\le\min(m,n)$。审计 restricted Jacobian $JT$ 的 singular values，而不是把 bottleneck 必然产生的全空间 zeros 计作算法失败。报告 tangent basis 的来源、估计误差、off-tangent directions 与 decoder composition；结论只能说在该数据子空间/批次附近近等距。

### NN-DISO-E03
固定 architecture、activation、fan convention、global output second moment、data batch、depth/width 与 seed set。四组分别使用 Gaussian、Xavier、Kaiming、orthogonal with matched gain。必须报告 rank、mean $s^2$、median/quantiles、$s_{\max}$、可靠的 $s_{\min}$ 或 lower proxy、condition estimate、random JVP/VJP gain，以及初始 loss/gradient。不能只用训练 speed 反推谱，也不能只用平均 norm 宣称 isometry。
