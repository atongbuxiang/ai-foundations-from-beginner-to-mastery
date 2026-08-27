---
type: exercise
status: draft
area: [neural-networks/activations, relu, nonsmoothness]
topic: "[[ReLU、Leaky ReLU 与次梯度约定]]"
difficulty: [A, B, C, D, E]
related: ["[[解答 - ReLU、Leaky ReLU 与次梯度约定]]", "[[ELU、SELU 与自归一化接口]]"]
solution: "[[解答 - ReLU、Leaky ReLU 与次梯度约定]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - ReLU、Leaky ReLU 与次梯度约定

## A. 识别与复述

### NN-REL-A01
区分 ReLU 在 0 的 classical derivative、convex subdifferential 与 framework backward convention。

### NN-REL-A02
写出 ReLU、leaky ReLU、PReLU 对 input 与 negative-slope parameter 的局部导数。

### NN-REL-A03
解释 activation sparsity、dead unit 与 hardware sparse speedup 为什么是三个不同概念。

## B. 手算与建模

### NN-REL-B01
对 $f(x_1,x_2)=\operatorname{ReLU}(x_1+x_2-1)$ 给出两半空间的公式、gradient 与边界。

### NN-REL-B02
一个 PReLU channel 的输入为 $(-2,-1,0,3)$，upstream 为 $(1,2,4,-1)$，$a=0.1$。按 zero convention 0 计算 $\bar x$ 与 $\bar a$。

### NN-REL-B03
若一条深层路径连续经过 $k$ 个负侧 leaky gate，$a=0.01$，计算 activation-only gain 在 $k=5,10$ 时的量级。

## C. 推导与证明

### NN-REL-C01
证明 ReLU/leaky ReLU 对 $c\ge0$ 正齐次，并推出相邻层的等价重缩放；给出 $c<0$ 失败例子。

### NN-REL-C02
若 $Z$ 关于 0 对称且 $E[Z^2]=q$，证明 ReLU 与 leaky ReLU 的输出二阶矩分别为 $q/2$ 与 $(1+a^2)q/2$。

### NN-REL-C03
证明固定 activation mask 后 ReLU 网络在相应 open region 内为 affine；说明 region 边界上为什么不能直接沿用同一 Jacobian。

## D. 边界、反例与纠错

### NN-REL-D01
反驳：“Leaky ReLU 的导数从不为 0，所以深层梯度有正下界。”

### NN-REL-D02
给出一次 mini-batch inactive 但单元并未 dataset-wide dead 的例子，并提出可靠 dead-rate 定义。

### NN-REL-D03
反驳：“ReLU 网络对输入的 Hessian 几乎处处为 0，所以它等价于线性模型。”

## E. AI 迁移

### NN-REL-E01
为 fused in-place ReLU kernel 设计 forward/backward、alias、kink、低精度与 determinism 验收。

### NN-REL-E02
为 ReLU/leaky/PReLU 比较设计 activation-aware initialization 与 matched-compute protocol。

### NN-REL-E03
一个训练后网络出现 40% zero activations。列出至少六种解释，并设计区分它们的诊断。

## 解答入口

[[解答 - ReLU、Leaky ReLU 与次梯度约定]]
