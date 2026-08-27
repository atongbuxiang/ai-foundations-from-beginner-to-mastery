---
type: solution
status: draft
area: [neural-networks/residual-stability, normalization-placement]
topic: "[[Pre-Activation、Pre-Norm 与 Post-Norm 残差]]"
exercise: "[[习题 - Pre-Activation、Pre-Norm 与 Post-Norm 残差]]"
sources: ["[[S-2016-He-Identity-Mappings]]", "[[S-2020-Xiong-Transformer-LayerNorm]]", "[[S-2022-Su-9009-PreNorm-PostNorm]]"]
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - Pre-Activation、Pre-Norm 与 Post-Norm 残差

## A

### NN-PAP-A01

$P$ 预处理 branch 输入，$S$ 是 shortcut，$Q$ 处理 addition 后的总状态。令 $z=S(x)+F(P(x))$，则

$$
J_{x^+}=J_Q(z)[J_S(x)+J_F(P(x))J_P(x)].
$$

乘法顺序来自输入扰动先过 $P$、再过 $F$，shortcut 与 branch 相加后再整体过 $Q$。

### NN-PAP-A02

$$
\begin{aligned}
\text{post-activation: }&x^+=\phi(x+F(x)),\\
\text{full pre-activation: }&x^+=x+F(P(x)),\\
\text{Pre-Norm: }&x^+=x+F(N(x)),\\
\text{Post-Norm: }&x^+=N(x+F(x)).
\end{aligned}
$$

full pre-activation 与 Pre-Norm 的 Jacobian 分别为 $I+J_FJ_P$ 与 $I+J_FJ_N$，显式含未被后置算子左乘的 $I$。其余两者分别被 $J_\phi$、$J_N$ 左乘。

### NN-PAP-A03

至少包括：预处理算子（BN/ReLU 对 LN/RMSNorm）、归约轴、状态形状（feature map 对 token residual stream）、branch（convolution 对 attention/FFN）、BN train/eval 统计语义、ReLU 非光滑 mask 与 Transformer 的 masking/双子层结构。它们只能共享抽象 Jacobian 外壳。

## B

### NN-PAP-B01

$$
x^+=C(Dx+ABx)=(CD+CAB)x.
$$

所以

$$
J=C(D+AB).
$$

$AB$ 不能写成 $BA$：扰动先经 $B$，再经 $A$。$C$ 位于最外层，因此左乘整个和。

### NN-PAP-B02

$x=(1,-1)^\mathsf T$ 给出 $D_x=\operatorname{diag}(1,0)$：

$$
J_{\mathrm{pre}}=I+AD_x
=\begin{bmatrix}1&0\\0.2&1\end{bmatrix}.
$$

其秩为 2，行列式为 1。另一方面

$$
x+Ax=(3,-0.8)^\mathsf T,
$$

故 $D_y=\operatorname{diag}(1,0)$，

$$
J_{\mathrm{post}}=D_y(I+A)
=\begin{bmatrix}1&-2\\0&0\end{bmatrix}.
$$

其秩为 1，行列式为 0。

### NN-PAP-B03

Pre-Norm：

$$
J_{\mathrm{pre}}=I+0.5J_N=\operatorname{diag}(1,2),
$$

特征值为 $1,2$。Post-Norm：

$$
J_{\mathrm{post}}=J_N(1.5I)=\operatorname{diag}(0,3),
$$

特征值为 $0,3$。$J_N$ 的零方向在 Pre-Norm 中仍由 $I$ 传递，在 Post-Norm 中被最外层 norm 删除。

## C

### NN-PAP-C01

Pre-Norm 令 $z=N(x)$、$y=x+F(z)$：

$$
dz=J_N(x)dx,
$$

$$
dy=dx+J_F(N(x))dz,
$$

故

$$
J_{\mathrm{pre}}=I+J_F(N(x))J_N(x).
$$

Post-Norm 令 $z=x+F(x)$、$y=N(z)$：

$$
dz=[I+J_F(x)]dx,
$$

$$
dy=J_N(x+F(x))dz,
$$

故

$$
J_{\mathrm{post}}=J_N(x+F(x))[I+J_F(x)].
$$

### NN-PAP-C02

$F(x)=c$ 时 $J_F=0$。Pre-Norm 的输出是 $x+c$，所以 Jacobian 为 $I$；Post-Norm 输出是 $N(x+c)$，所以 Jacobian 为 $J_N(x+c)$。这只证明后置 norm 在 constant-branch 反例中仍过滤方向，不能推出任意参数、任意层数的梯度乘积必消失。

### NN-PAP-C03

定义

$$
A_1=J_{F_1}(N_1(x))J_{N_1}(x),
$$

$$
A_2=J_{F_2}(N_2(u))J_{N_2}(u).
$$

则

$$
J_{y\leftarrow x}=(I+A_2)(I+A_1).
$$

展开为 $I+A_1+A_2+A_2A_1$。最后的复合项以及 $A_2$ 在中间状态 $u$ 的求值点都不能由 $A_1+A_2$ 表示。

## D

### NN-PAP-D01

- $P=I$：存在真正的全维 identity differential；
- $P$ 为同维正交矩阵：存在 norm-preserving shortcut，但不是坐标恒等；
- $P$ 为正交 projection 或降维矩阵：nullspace 方向不由 shortcut 传递，只能说存在 projection rail，不能说全空间 identity rail。

完整 Jacobian 是 $P+J_FJ_N$；branch 可能补偿丢失方向，但需另证。

### NN-PAP-D02

遗漏包括：train-mode BN 使用 batch statistics、样本间 Jacobian 耦合、running-state 更新、dropout/数据增强状态、microbatch/SyncBN、混合精度与数据分布。修正实验应在 train/eval 两种 mode、多个 batch size/同步组、固定和随机 batch composition 下测 block/global JVP/VJP，并记录统计量、activation mask、dtype 与训练结果。

### NN-PAP-D03

branch 内 dropout 只随机化 branch 项；addition 后 dropout 会同时随机过滤 shortcut 与 branch sum；shortcut dropout 直接破坏恒等 rail。固定 mask 时可写条件 Jacobian，但

$$
\mathbb E[J_M],
\quad
J_{\mathbb E[f_M]},
\quad
J_{f_{\mathrm{eval}}}
$$

只有在额外线性/缩放条件下才可能相同；Jacobian norm 的期望更不能与期望 Jacobian 的 norm 互换。

## E

### NN-PAP-E01

取

$$
J_F=-I,
\qquad
J_N=I.
$$

则

$$
I+J_FJ_N=0,
$$

完全奇异。它反驳“只要 Pre-Norm/full pre-activation 显式含 $I$，梯度就一定不会消失”的命题。

### NN-PAP-E02

匹配数据、token/图像预处理、参数/FLOPs、训练步数、硬件、precision 与调参预算；对每种 placement 分别调学习率、warm-up、初始化和 residual scale，并同时给出固定超参协议。记录 activation/branch RMS、JVP/VJP、gradient/update、loss spike、time-to-loss、最终验证性能、多 seed CI 与 wall time。结论必须绑定模型、深度、任务和协议，不能写成放置方式的普遍排序。

### NN-PAP-E03

显式 $I$ 只说明单子层 Jacobian 的加法结构：

- final norm 服务最终输出尺度/参数化，是否需要不能由中间 $I$ 决定；
- warm-up 取决于初始梯度、optimizer 与学习率；
- residual scaling 控制跨层 branch 累积；
- 泛化需要数据、容量、学习算法与评估协议。

四个结论都超出了结构恒等式的证据层。
