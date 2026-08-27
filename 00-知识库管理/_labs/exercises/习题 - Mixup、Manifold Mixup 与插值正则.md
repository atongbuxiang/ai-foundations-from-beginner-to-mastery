---
type: exercise
status: draft
area: [neural-networks/regularization, mixup, manifold-mixup, vicinal-risk]
topic: "[[Mixup、Manifold Mixup 与插值正则]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Mixup、Manifold Mixup 与插值正则]]"
created: 2026-08-24
updated: 2026-08-24
---
# 习题 - Mixup、Manifold Mixup 与插值正则

## A

### NN-MIX-A01
写出标准 Mixup 的 pairing、$\lambda$、input 与 target 合同，并说明哪些随机轴必须记录。

### NN-MIX-A02
解释 empirical risk 与 vicinal risk 的差别。为什么 Mixup loss 不是原 ERM risk 的无偏估计？

### NN-MIX-A03
区分 input chord、hidden chord、data manifold 与 geodesic；为什么 “Manifold Mixup” 的名称不是几何证明？

## B

### NN-MIX-B01
对 $\lambda\sim\operatorname{Beta}(\alpha,\alpha)$，分别在 $\alpha=0.2,1,10$ 时计算 $\mathbb E\lambda$、$\operatorname{Var}(\lambda)$ 与 $\mathbb E[\lambda(1-\lambda)]$。

### NN-MIX-B02
取 $x_1=(2,0),x_2=(0,4),y_1=e_1,y_2=e_3,\lambda=0.25$。计算 mixed input/target；若 $p=(0.2,0.1,0.7)$，计算 CE。

### NN-MIX-B03
Manifold Mixup 在 hidden layer 得到 $h_i,h_j$，suffix cotangent 为 $g=(2,-1)$、$\lambda=0.3$。求回到两路 hidden states 的 cotangents，并写出共享 prefix parameter gradient。

## C

### NN-MIX-C01
推导 symmetric Beta 的 variance、二阶矩和 $\mathbb E[\lambda(1-\lambda)]$；解释为何 mean 不能衡量 mixing strength。

### NN-MIX-C02
证明 soft-target CE 的 label-linearity，并说明为什么该式不推出 logits 或 representations 沿 chord 线性。

### NN-MIX-C03
证明 fixed-prior Label Smoothing 与 target Mixup 可交换；列出完整训练 pipeline 不交换的至少三个原因。

## D

### NN-MIX-D01
构造一个三分类 manifold-intrusion 反例：两类 endpoints 的 chord 穿过第三类 support。说明 target 冲突与可观测诊断。

### NN-MIX-D02
审计 `lambda=max(lambda,1-lambda)`、self-pair、local-rank permutation 与 global pairing 对 vicinal distribution 的影响。

### NN-MIX-D03
分析 augmentation order、BatchNorm/LayerNorm、padding/attention mask 与 hidden-layer placement 的非交换性。

## E

### NN-MIX-E01
设计 natural、matched-strength 与 semantic-validity 三轨 Mixup 实验，规定 distance、entropy、compute 与 held-out 指标。

### NN-MIX-E02
为图像、回归、multi-label、segmentation 与 token sequence 各写一份最小 label/input geometry 合同。

### NN-MIX-E03
设计 Input Mixup 与 Manifold Mixup 的公平比较，要求控制 layer sampling、memory、normalization state、pairing 和 tuning budget。

## 解答入口

[[解答 - Mixup、Manifold Mixup 与插值正则]]
