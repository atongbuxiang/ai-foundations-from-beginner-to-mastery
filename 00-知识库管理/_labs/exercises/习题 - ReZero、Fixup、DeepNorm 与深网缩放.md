---
type: exercise
status: draft
area: [neural-networks/residual-stability, initialization, residual-scaling]
topic: "[[ReZero、Fixup、DeepNorm 与深网缩放]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - ReZero、Fixup、DeepNorm 与深网缩放]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - ReZero、Fixup、DeepNorm 与深网缩放

## A

### NN-RFD-A01
分别说明 forward state、state Jacobian、parameter gradient 与 parameter update 四本账。为什么不能用其中一个代表全部？

### NN-RFD-A02
写出 ReZero、Fixup 与 DeepNorm 的核心方法合同，并指出每个 scale 是运行时变量、可学习参数还是初始化操作。

### NN-RFD-A03
DeepNorm 中哪些权重按 $\beta$ 缩放？为什么“所有 attention 矩阵都乘 $\beta$”不是严格复现？

## B

### NN-RFD-B01
ReZero 中 $F(x)=3,g^+=2,\alpha=0$，用学习率 $0.01$ 的 SGD 算 gate 与 branch 参数第一步梯度及新 $\alpha$。

### NN-RFD-B02
计算 Fixup 在 $(m,L)=(2,100),(3,256),(4,729)$ 时的非末层缩放。

### NN-RFD-B03
计算 encoder-only DeepNorm 在 $N=100$ 时的 $\alpha,\beta$；验证 $\alpha\beta=4^{-1/4}$ 与 $N$ 无关。

## C

### NN-RFD-C01
对 ReZero 推导 $\partial\mathcal L/\partial\alpha$、$\nabla_\theta\mathcal L$ 与 $\nabla_x\mathcal L$。给出 gate/branch 同时零梯度的充分例子。

### NN-RFD-C02
对 $F(x)=W_2\phi(W_1x)$ 且 $W_2=0$，推导 $\nabla_{W_2}\mathcal L$ 与 $\nabla_{W_1}\mathcal L$，说明 zero-last 的学习启动顺序。

### NN-RFD-C03
写出 DeepNorm 单子层的 state Jacobian。它为什么一般既不是 $I+J_G$，也不是初始恒等映射？

## D

### NN-RFD-D01
团队同时使用 ReZero $\alpha=0$ 与 Fixup zero-last。分析首步是否可能死锁，并给出两种保留近恒等但能启动学习的修改。

### NN-RFD-D02
某实现把 DeepNorm 的 $\beta$ 当作每次前向都乘在 branch 输出上的常数。指出它与论文合同的差异，以及对梯度、weight decay 和推理函数的影响。

### NN-RFD-D03
设计极深模型的逐层监控面板，至少覆盖 activation、branch ratio、gate、gradient、update、Jacobian、dtype/ulp 与系统性能。

## E

### NN-RFD-E01
反驳：“ReZero 初始化 dynamical isometry，所以训练全程 condition number 为 1，所有 branch 参数第一步都有健康梯度。”

### NN-RFD-E02
设计 ReZero/Fixup/DeepNorm 的 natural protocol 与 matched-update protocol。哪些架构差异使三者无法做到完全 apples-to-apples？

### NN-RFD-E03
把 encoder–decoder 的 DeepNorm 四个系数写出，并为 $N=12,M=6$ 计算近似数值；说明为什么两侧不能共用 encoder-only 系数。

