---
type: exercise
status: draft
area: [neural-networks/residual-stability, jacobian, backpropagation]
topic: "[[残差块 Jacobian 与梯度直通]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - 残差块 Jacobian 与梯度直通]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - 残差块 Jacobian 与梯度直通

## A

### NN-RJG-A01
对 $y=x+F(x;\theta)$ 写出 $J_xF,J_\theta F,J_xy$ 的 shape，并写出输入 JVP、输入 VJP 与参数 VJP。

### NN-RJG-A02
判断并解释：“identity rail 存在”“总 Jacobian 等于 identity”“梯度 norm 保持”“block 可逆”四个命题之间的逻辑关系。

### NN-RJG-A03
对 $y=P(x)+\alpha F(N(x))$ 写出精确 Jacobian，并指出什么条件下直达项才是 $I$。

## B

### NN-RJG-B01
对
$$
J_F=\begin{bmatrix}-1/2&1\\0&-1/2\end{bmatrix},
\qquad g_y=(1,-1)^\mathsf T,
$$
分别计算 identity VJP、branch VJP 与总 $g_x$。

### NN-RJG-B02
标量 block 为 $y=x+cx$。分别对 $c=0,-1,-2,1/2$ 求 forward gain 与 backward gain，判断消失、变号和放大。

### NN-RJG-B03
已知 $\|J_F\|_2=0.2$。给出 $I+J_F$ 的 $\sigma_{\min},\sigma_{\max}$ 保证和条件数上界。它们是等号还是保守界？

## C

### NN-RJG-C01
从 differential 推导 $g_x=g_y+J_F^\mathsf Tg_y$ 与 $g_\theta=J_\theta F^\mathsf Tg_y$，不得直接引用计算图结论。

### NN-RJG-C02
完整展开三层线性 residual Jacobian $(I+A_2)(I+A_1)(I+A_0)$ 的 8 项，保持矩阵顺序，并按 path length 分组。

### NN-RJG-C03
对
$$
M=\begin{bmatrix}0.1&3\\0&0.1\end{bmatrix}
$$
求 eigenvalues、$M^\mathsf TM$、singular values 的近似，并解释为什么 eigenvalue 不能诊断单步最坏梯度增益。

## D

### NN-RJG-D01
构造一个 $P\ne I$ 的 projection residual block，给出 $J_P+\alpha J_FJ_N$ 的 shape 账本。若 $P$ 降维，为什么不能有正的全空间 $\sigma_{\min}$？

### NN-RJG-D02
写出无需显式构造 Jacobian 的 JVP/VJP 对偶测试。列出 stochastic mask、BatchNorm state、in-place、detach 与 broadcast reduction 五类失败原因。

### NN-RJG-D03
ReLU branch 的输入恰有一个 preactivation 为 0。为什么中心差分可能与框架 VJP 不一致？给出可靠 gradient-check 协议。

## E

### NN-RJG-E01
构造两个具有相同 $\|J_F\|_2$ 的标量/二维 branch，使一个 residual block 放大而另一个衰减或抵消。说明 norm-only 诊断丢失了什么。

### NN-RJG-E02
若 $\|A_\ell\|_2\le c/N<1$，证明 $\|J_{0\to N}\|_2\le e^c$，并给出 $\sigma_{\min}$ 的 product lower bound。该下界随 $N\to\infty$ 趋向什么？

### NN-RJG-E03
设计一个 100 层 residual net 的 Jacobian 诊断仪表盘：至少包括 per-block rail/branch 夹角、随机 JVP/VJP、极端 singular value 估计、log-depth gain 和 finite-difference audit。

