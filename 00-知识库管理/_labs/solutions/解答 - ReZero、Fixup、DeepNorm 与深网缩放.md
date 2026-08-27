---
type: solution
status: draft
area: [neural-networks/residual-stability, initialization, residual-scaling]
topic: "[[ReZero、Fixup、DeepNorm 与深网缩放]]"
exercise: "[[习题 - ReZero、Fixup、DeepNorm 与深网缩放]]"
sources: ["[[S-2021-Bachlechner-ReZero]]", "[[S-2019-Zhang-Dauphin-Ma-Fixup]]", "[[S-2022-Wang-DeepNet-DeepNorm]]"]
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - ReZero、Fixup、DeepNorm 与深网缩放

## A

### NN-RFD-A01

forward state 看 $x_\ell$ 与 branch 的量级；state Jacobian 看输入扰动的局部线性传播；parameter gradient 看损失对参数的敏感度；parameter update 还包含 learning rate、optimizer preconditioner、weight decay 等。$J_x=I$ 仍可让 $\nabla_\theta=0$；gradient norm 正常仍可因 optimizer 产生过大 update；forward RMS 正常也不能排除方向性 Jacobian 病态。

### NN-RFD-A02

- ReZero：$x^+=x+\alpha_\ell F(x)$，$\alpha_\ell$ 是零初始化、可学习、运行时存在的 gate；
- Fixup：branch 内非末权重初始化乘 $L^{-1/(2m-2)}$，末层置零，并加可学习 bias/multiplier；depth scale 是初始化操作；
- DeepNorm：$x^+=\operatorname{LN}(\alpha x+G(x;\theta))$，$\alpha$ 是固定运行时 shortcut scale，$\beta$ 是指定权重的初始化 scale。

### NN-RFD-A03

$\beta$ 缩放 FFN 权重，以及 attention 的 value 和 output projections；query/key 不按该规则缩放。因此统一缩放所有 attention 矩阵会改变 attention logits、softmax temperature 与梯度，不再是论文方法合同。

## B

### NN-RFD-B01

$$
\frac{\partial\mathcal L}{\partial\alpha}=g^+F(x)=6,
$$

而 $\alpha=0$ 使

$$
\nabla_\theta\mathcal L=0.
$$

SGD 更新

$$
\alpha^+=0-0.01(6)=-0.06.
$$

branch 参数第一步不变；下一步若 $\alpha\ne0$ 才获得常规梯度。

### NN-RFD-B02

$$
s=L^{-1/(2m-2)}.
$$

- $(m,L)=(2,100)$：$s=100^{-1/2}=0.1$；
- $(3,256)$：$s=256^{-1/4}=0.25$；
- $(4,729)$：$s=729^{-1/6}=1/3$，因为 $729=3^6$。

### NN-RFD-B03

$$
\alpha=(200)^{1/4}\approx3.7606,
\qquad
\beta=(800)^{-1/4}\approx0.1880.
$$

乘积为

$$
\alpha\beta
=\left(\frac{2N}{8N}\right)^{1/4}
=4^{-1/4}=\frac1{\sqrt2},
$$

与 $N$ 无关。

## C

### NN-RFD-C01

对 $x^+=x+\alpha F(x;\theta)$：

$$
\frac{\partial\mathcal L}{\partial\alpha}=g^{+\mathsf T}F(x;\theta),
$$

$$
\nabla_\theta\mathcal L
=\alpha J_\theta F(x;\theta)^\mathsf Tg^+,
$$

$$
\nabla_x\mathcal L
=(I+\alpha J_xF)^\mathsf Tg^+.
$$

若 $\alpha=0$ 且 $F(x;\theta)=0$，则 gate 与 branch 参数梯度都为零，而输入梯度仍为 $g^+$。ReZero 与精确 zero-output branch 的无审计叠加就是充分例子。

### NN-RFD-C02

令 $h=\phi(W_1x)$，$F=W_2h$。则

$$
\nabla_{W_2}\mathcal L=g^+h^\mathsf T,
$$

通常非零；

$$
\nabla_{W_1}\mathcal L
=\left[(W_2^\mathsf Tg^+)\odot\phi'(W_1x)\right]x^\mathsf T=0.
$$

末层先离开零点，之后 $W_2^\mathsf Tg^+$ 才为更早层打开梯度。

### NN-RFD-C03

令

$$
z=\alpha x+G(x;\theta).
$$

则

$$
\boxed{
J_{x^+}=J_{\mathrm{LN}}(z)[\alpha I+J_G(x)]
}.
$$

最外层 LayerNorm 左乘整个残差和，shortcut 还是 $\alpha I$ 而非 $I$，所以一般不是 $I+J_G$。即使 branch 很小，$\operatorname{LN}(\alpha x)$ 通常也不是 $x$，故不是精确恒等初始化。

## D

### NN-RFD-D01

ReZero 给 $\alpha=0$，Fixup zero-last 又给 $F(x)=0$。于是

$$
\partial\mathcal L/\partial\alpha=g^TF=0,
\qquad
\nabla_\theta\mathcal L=\alpha J_\theta F^Tg=0,
$$

可能完全死锁。修改一：保留 ReZero 的零 gate，但不要 zero-last，使 $F(x)$ 非零，gate 先学；修改二：保留 Fixup zero-last，去掉 ReZero 或把 gate 初始化为小非零 $\varepsilon$，使末层或 branch 参数能启动。两者都需测初始 Jacobian/update，而不是凭“近恒等”命名。

### NN-RFD-D02

论文的 $\beta$ 改变指定参数的初始值，参数随后自由更新；错误实现相当于训练和推理都使用 $G(x;\beta\theta)$ 或 $\beta G$。它持续缩小 branch forward 和参数梯度，改变 effective learning rate；若 weight decay 作用于未缩放参数，函数空间中的正则强度也变化；推理函数多了固定缩放，无法通过只载入论文权重复现。

### NN-RFD-D03

面板应至少包括：每层 activation RMS/max；branch/state RMS ratio；$\alpha$/gate quantiles 与 saturation；parameter/activation gradient norm、correlation；update-to-weight；JVP/VJP gain 与 singular estimates；compute/add/accumulator dtype、ulp ratio、finite/nonzero/absorption fraction；loss spike；throughput、peak memory、通信量和重计算误差。按 depth、训练 step 与 module type 分层展示。

## E

### NN-RFD-E01

ReZero 只在初始化且 residual stack shortcut 真为 identity 时给 $J_x=I$。训练一开始 $\alpha$ 改变，$I+\alpha J_F$ 可放大、相消或非正规；首尾层也可改变总 condition number。branch 参数梯度恰被 $\alpha=0$ 乘为零，只有 gate 梯度通常非零。因此命题的“训练全程”和“所有参数第一步”两部分都错误。

### NN-RFD-E02

natural protocol 固定 optimizer、schedule、数据、训练步和调参预算；matched-update protocol 通过 parameter groups/学习率匹配初始 $\|\Delta\theta\|/\|\theta\|$ 或 function change。仍无法完全匹配：ReZero 有学习 gate 和首步冻结，Fixup 无 norm且有 scalar bias/multiplier，DeepNorm 是 Post-LN 并有运行时 $\alpha$、选择性 $\beta$；参数化与函数类本身不同。应报告 Pareto 结果与各自最佳协议。

### NN-RFD-E03

encoder–decoder 中：

$$
\alpha_e=0.81(N^4M)^{1/16},
\qquad
\beta_e=0.87(N^4M)^{-1/16},
$$

$$
\alpha_d=(3M)^{1/4},
\qquad
\beta_d=(12M)^{-1/4}.
$$

取 $N=12,M=6$：

$$
\alpha_e\approx1.6862,
\quad
\beta_e\approx0.4179,
\quad
\alpha_d\approx2.0598,
\quad
\beta_d\approx0.3433.
$$

encoder-only 公式则给 $\alpha\approx2.2134,\beta\approx0.3195$，与两侧都不同。decoder 每层子层结构和 encoder–decoder 更新传播不同，论文因此给出分侧系数；共用 encoder-only 值会脱离其更新界合同。
