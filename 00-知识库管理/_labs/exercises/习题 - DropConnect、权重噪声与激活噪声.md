---
type: exercise
status: draft
area: [neural-networks/regularization, dropconnect, weight-noise, activation-noise, stochastic-estimators]
topic: "[[DropConnect、权重噪声与激活噪声]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - DropConnect、权重噪声与激活噪声]]"
created: 2026-08-24
updated: 2026-08-24
---
# 习题 - DropConnect、权重噪声与激活噪声

## A

### NN-NOI-A01
以 $z=Wx+b$ 为基准，分别写出 activation Dropout、DropConnect、additive weight noise、additive activation noise 与 multiplicative Gaussian activation noise 的前向式。

### NN-NOI-A02
为每种噪声声明随机对象的 shape 与共享轴。解释 per-example、per-batch 与 across-time shared noise 如何改变跨样本/跨时间 covariance。

### NN-NOI-A03
区分 forward noise、gradient masking 与 optimizer noise；为什么“梯度中出现零”不足以证明实现的是 DropConnect？

## B

### NN-NOI-B01
令 $W=\begin{bmatrix}1&2\\-1&1\end{bmatrix}$、$x=(2,1)^\mathsf T$、$q=0.5$。计算无噪声输出，以及 activation Dropout 和独立 DropConnect 的输出条件均值与 covariance matrices。

### NN-NOI-B02
对 B01 写出 activation Dropout 与 DropConnect 的一次采样梯度：设上游梯度为 $g=(3,-2)^\mathsf T$，activation mask 为 $(1,0)$，connection mask 为全 1；求 $\nabla_xL$ 与 $\nabla_WL$。

### NN-NOI-B03
若 additive weight noise entries 独立、均值 0、方差 $\sigma_W^2$，推导 $z=(W+E)x$ 的每个输出方差。再对 covariance 为 $\Sigma_\varepsilon$ 的 additive activation noise 推导 $\operatorname{Cov}(W(x+\varepsilon))$。

## C

### NN-NOI-C01
推导 independent activation Dropout 的跨输出 covariance，并证明 independent DropConnect 在不同输出 rows 间 covariance 为 0；明确独立性条件。

### NN-NOI-C02
从 $\mathbb E[L(u+\varepsilon)]$ 的二阶 Taylor 展开推导 noise-induced penalty，说明 input、activation、preactivation 与 weight noise 分别作用于哪个 Hessian/Jacobian 对象。

### NN-NOI-C03
解释 local reparameterization 的目标：它在 Gaussian/variational setting 中保持哪些 preactivation marginals，改变哪些跨样本或联合依赖，并如何影响 gradient estimator variance。

## D

### NN-NOI-D01
审计命题：“只要 activation Dropout 与 DropConnect 匹配每个输出方差，它们就是同一个正则器。”用 B01 的 covariance 结果反驳，并列出还会不同的三个维度。

### NN-NOI-D02
解释随机零权重为何不自动带来 sparse-kernel 加速。分别讨论 mask generation、memory traffic、dense compute、conditional execution 与 accelerator utilization。

### NN-NOI-D03
给出一个 forward distribution 大致匹配但 gradient distribution 不匹配的构造，并说明 forward-only unit test 为什么不足。

## E

### NN-NOI-E01
设计 matched-moment 实验，比较 activation Dropout、DropConnect 与 Gaussian noise；规定要匹配的 conditional moments 和必须额外测量的 joint statistics。

### NN-NOI-E02
设计 matched-quality 与 natural-protocol 两条实验轨道，说明二者回答的问题为何不同。

### NN-NOI-E03
评审命题：“输入噪声等价于 Tikhonov 正则，因此所有噪声注入都等价于 weight decay。”将其拆成 exact、approximate 与 false-generalization 三层。

## 解答入口

[[解答 - DropConnect、权重噪声与激活噪声]]
