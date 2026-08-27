---
type: exercise
status: draft
topic: "[[神经网络容量与 Norm-Based Bound]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - 神经网络容量与 Norm-Based Bound]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - 神经网络容量与 Norm-Based Bound
## A
### LT-NNB-A01
区分 architecture capacity 与 solution-dependent capacity。
### LT-NNB-A02
spectral norm 与 Frobenius norm 在界中分别控制什么？
### LT-NNB-A03
定义 stable rank，并说明其与 rank 的关系。
## B
### LT-NNB-B01
两层网络的谱范数为 $2,3$，输入半径 $B=4$；求 Lipschitz 上界与输出 norm 上界。
### LT-NNB-B02
某层奇异值为 $(4,2,2,0)$，求 stable rank。
### LT-NNB-B03
若 $B=1$、谱范数乘积为 $6$、各层 stable-rank 之和为 $9$，求示意复杂度 $\mathcal C(W)$。
## C
### LT-NNB-C01
证明 $1$-Lipschitz 激活网络的逐层 Lipschitz 乘积界。
### LT-NNB-C02
解释 perturbation telescope 为什么产生相对层扰动之和。
### LT-NNB-C03
证明相邻 ReLU 层做 $c$ 与 $c^{-1}$ 重缩放时，示意 spectral complexity 不变。
## D
### LT-NNB-D01
审计“网络参数越多，泛化一定越差”。
### LT-NNB-D02
审计“训练后 norm-based bound 与 test error 正相关，所以 norm 是泛化的原因”。
### LT-NNB-D03
为什么一个数学正确但数值大于 1 的分类错误率界不能称为定量解释？
## E
### LT-NNB-E01
为一个 ResNet 设计 norm/margin certificate 的最小报告表。
### LT-NNB-E02
设计实验区分 raw sharpness proxy 与重缩放不变复杂度。
### LT-NNB-E03
写 norm-based generalization claim card，包含 theorem、估计误差和 post-selection 修正。

