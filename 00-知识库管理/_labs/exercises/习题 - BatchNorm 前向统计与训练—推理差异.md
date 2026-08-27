---
type: exercise
status: draft
area: [neural-networks/normalization, batch-normalization, inference]
topic: "[[BatchNorm 前向统计与训练—推理差异]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - BatchNorm 前向统计与训练—推理差异]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - BatchNorm 前向统计与训练—推理差异

## A

### NN-BNF-A01
对 $(N,C)$ 与 $(N,C,H,W)$ 输入分别写出每个 channel 的归约集合、nominal group size、affine 参数 shape 与输出 shape。

### NN-BNF-A02
区分 current batch mean/variance、population moments、running buffers。说明训练输出和 running update 各自使用哪一类对象。

### NN-BNF-A03
按 PyTorch 2.13 语义写出 forward variance correction、running variance observation correction、momentum update 与 track-running-stats 为 false 时的 eval 行为。

## B

### NN-BNF-B01
对 batch $x=(1,3)$、$\gamma=2,\beta=-1,\varepsilon=0$ 完整计算训练输出。再把 companion 3 改成 5，计算第一个样本的新输出。

### NN-BNF-B02
running mean 初值 0、running variance 初值 1，新 batch mean 为 4、unbiased variance 为 9，PyTorch-style momentum $a=0.1$。计算更新后的 buffers；再说明若误把 0.1 当“旧值系数”会得到什么。

### NN-BNF-B03
一维 affine 层 $z=3x+2$ 后接 eval BN，$\gamma=4,\beta=-1,\bar\mu=5,\bar q=4,\varepsilon=0$。求折叠后的 weight 与 bias，并用 $x=1$ 验证。

## C

### NN-BNF-C01
证明 Linear/Conv 的共享 bias 在紧接 train-mode BatchNorm centering 时被消去；列出至少两个该证明不适用的计算图。

### NN-BNF-C02
若 $X_1,\ldots,X_m$ IID、variance 为 $\sigma^2$，证明 biased sample variance $q_B$ 满足
$$\mathbb E[q_B]=(m-1)\sigma^2/m.$$

### NN-BNF-C03
从 eval BN 公式推导逐 channel 的 Conv/Linear folding：
$$W'_c=a_cW_c,\qquad b'_c=a_c(b_c-\bar\mu_c)+\beta_c.$$
说明为什么 train-mode 不能进行同样折叠。

## D

### NN-BNF-D01
反驳：“BatchNorm 后每个 channel 都服从标准正态，且彼此独立。”

### NN-BNF-D02
反驳：“optimizer momentum 与 BN momentum 都叫 momentum，因此数值含义相同。”给出两种更新式并解释新旧观测的权重。

### NN-BNF-D03
反驳：“把一个 batch 依次分成四个 microbatches 做 gradient accumulation，与一次用完整 batch 做 BatchNorm 完全等价。”

## E

### NN-BNF-E01
写一份 BatchNorm checkpoint/deployment 审计：覆盖 parameters、buffers、mode、track state、folding、domain shift 与验证数据污染。

### NN-BNF-E02
设计一个 small-batch sensitivity 实验。固定哪些变量？记录 batch statistics、running mismatch、train/eval output gap 和最终 metric 时怎样避免只看单 seed？

### NN-BNF-E03
设计 Conv+BN folding 的数值验收，覆盖无 bias、有 bias、多个 channels、不同 epsilon、fp32/fp16 与反复保存加载；规定误差指标和结论边界。

## 解答入口

[[解答 - BatchNorm 前向统计与训练—推理差异]]

