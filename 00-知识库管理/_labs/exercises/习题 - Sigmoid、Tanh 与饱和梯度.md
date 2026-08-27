---
type: exercise
status: draft
area: [neural-networks/activations, sigmoid, tanh]
topic: "[[Sigmoid、Tanh 与饱和梯度]]"
difficulty: [A, B, C, D, E]
related: ["[[解答 - Sigmoid、Tanh 与饱和梯度]]", "[[ReLU、Leaky ReLU 与次梯度约定]]"]
solution: "[[解答 - Sigmoid、Tanh 与饱和梯度]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - Sigmoid、Tanh 与饱和梯度

## A. 识别与复述

### NN-SAT-A01
写出 sigmoid、tanh 的值域、导数、最大斜率、对称性与相互关系。

### NN-SAT-A02
用精确数学语言定义“饱和”，并区分它与 finite-precision 输出恰等于端点。

### NN-SAT-A03
解释 sigmoid 在 ordinary hidden layer 中的均值漂移问题，以及它为何仍适合作 gate/Bernoulli link。

## B. 手算与建模

### NN-SAT-B01
对 target $y=1$ 的 binary logit $z=2$，用分离链式法则和 fused logits loss 两种路线计算 $dL/dz$。

### NN-SAT-B02
计算 $L$ 层标量链 $h_\ell=\sigma(h_{\ell-1})$ 在所有 preactivation 为 0 时的 derivative，并求 $L=10$ 的值。

### NN-SAT-B03
对 $\sigma_\tau(x)=\sigma(x/\tau)$ 推导导数；比较 $\tau=2,1,1/2$ 的中心斜率与过渡宽度。

## C. 推导与证明

### NN-SAT-C01
证明 $\tanh x=2\sigma(2x)-1$，并由此重建 tanh derivative。

### NN-SAT-C02
若 $Z$ 关于 0 对称，证明 $E\sigma(Z)=1/2$ 与 $E\tanh Z=0$；列出所需可积性条件。

### NN-SAT-C03
推导 $\log\sigma(x)=-\operatorname{softplus}(-x)$ 和 $\log(1-\sigma(x))=-\operatorname{softplus}(x)$。

## D. 边界、反例与纠错

### NN-SAT-D01
反驳：“tanh 在 0 的导数为 1，因此 tanh 网络不会梯度消失。”

### NN-SAT-D02
说明为何朴素 sigmoid 在大负输入溢出，并给出分支稳定实现及其等价性证明。

### NN-SAT-D03
构造 input distribution 不对称使 tanh output mean 非零的例子；解释“zero-centered activation”的正确含义。

## E. AI 迁移

### NN-SAT-E01
为 LSTM/GRU 类 sigmoid gate 设计饱和诊断，要求区分有意记忆状态与不可训练饱和。

### NN-SAT-E02
为 BF16 binary classifier 设计 logits-domain 数值验收，覆盖极端 logits、loss、gradient 与 probability 展示。

### NN-SAT-E03
设计 sigmoid/tanh/ReLU 的公平 hidden-layer 消融，并说明为何 gate/output 层不应同时机械替换。

## 解答入口

[[解答 - Sigmoid、Tanh 与饱和梯度]]
