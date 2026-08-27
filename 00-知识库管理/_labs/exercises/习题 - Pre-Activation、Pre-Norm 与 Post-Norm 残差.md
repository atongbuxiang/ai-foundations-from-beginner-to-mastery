---
type: exercise
status: draft
area: [neural-networks/residual-stability, normalization-placement]
topic: "[[Pre-Activation、Pre-Norm 与 Post-Norm 残差]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Pre-Activation、Pre-Norm 与 Post-Norm 残差]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - Pre-Activation、Pre-Norm 与 Post-Norm 残差

## A

### NN-PAP-A01
从统一块 $x^+=Q(S(x)+F(P(x)))$ 说明 $P,Q,S$ 分别承担什么角色，并写出一般 Jacobian。

### NN-PAP-A02
分别写出 original post-activation、full pre-activation、Transformer Pre-Norm 和 Post-Norm 的前向式。哪两个形式显式含未经后置算子过滤的 $I$？

### NN-PAP-A03
列出 CNN full pre-activation 与 Transformer Pre-Norm 至少四项不能混同的内部合同。

## B

### NN-PAP-B01
令 $F(x)=Ax$、$P(x)=Bx$、$Q(x)=Cx$、$S(x)=Dx$。写出总映射与 Jacobian，并核对乘法顺序。

### NN-PAP-B02
复算正文二维例子：$A=\begin{bmatrix}0&-2\\0.2&0\end{bmatrix}$、$x=(1,-1)^\mathsf T$。求 pre-activation 与 post-activation 的局部 Jacobian、秩和行列式。

### NN-PAP-B03
设局部 $J_N=\operatorname{diag}(0,2)$、$J_F=0.5I$。分别求 Pre-Norm 与 Post-Norm Jacobian 的特征值，并解释零方向。

## C

### NN-PAP-C01
用微分逐步推导 $J_{\mathrm{PreNorm}}=I+J_F(N(x))J_N(x)$ 与 $J_{\mathrm{PostNorm}}=J_N(x+F(x))(I+J_F(x))$，不得省略求值点。

### NN-PAP-C02
证明 constant branch $F(x)=c$ 时，Pre-Norm 的 Jacobian 是 $I$，Post-Norm 的 Jacobian 是 $J_N(x+c)$。这能否证明所有 Post-Norm 深网梯度消失？

### NN-PAP-C03
两个连续 Pre-Norm 子层为 $u=x+F_1(N_1(x))$、$y=u+F_2(N_2(u))$。写出 $J_{y\leftarrow x}$，并说明为什么不能把两个 branch Jacobian 简单相加。

## D

### NN-PAP-D01
对 $x^+=Px+F(N(x))$，讨论 $P$ 为 identity、orthogonal projection 与降维矩阵时“identity rail”的准确说法。

### NN-PAP-D02
某报告只在 eval mode 对单样本测了 CNN pre-activation Jacobian，却声称 train mode 同样稳定。指出至少四个遗漏，并给出修正实验。

### NN-PAP-D03
分析 dropout 放在 branch 内、addition 后和 shortcut 上的差异。固定 mask Jacobian、期望 Jacobian与 evaluation map 是否相同？

## E

### NN-PAP-E01
构造一个 $2\times2$ 的 $J_F$，使 Pre-Norm 形式 $I+J_FJ_N$ 在 $J_N=I$ 时奇异。它反驳了哪个常见命题？

### NN-PAP-E02
设计 pre-activation/Post-activation 或 Pre-Norm/Post-Norm 的公平消融：列出必须匹配或分别调优的变量、Jacobian/优化/性能指标与结论边界。

### NN-PAP-E03
审计下述论证：“Pre-Norm 有显式 $I$，所以不需要 final norm、warm-up、residual scaling，也必然比 Post-Norm 泛化好。”逐项指出证据缺口。

