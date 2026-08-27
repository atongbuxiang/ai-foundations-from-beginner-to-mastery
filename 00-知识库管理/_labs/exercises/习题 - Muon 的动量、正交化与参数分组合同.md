---
type: exercise
status: verified
area: [training, optimization, muon, implementation-contract]
topic: "[[Muon 的动量、正交化与参数分组合同]]"
solution: "[[解答 - Muon 的动量、正交化与参数分组合同]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Muon 的动量、正交化与参数分组合同

> [!abstract] 训练目标
> 能把当前 Muon 实现写成逐步状态机，识别 EMA/sum momentum、Nesterov、decay order、parameter grouping 与 distributed order 的非等价性，并建立可迁移 checkpoint 合同。

## A. 识别与复述

### TRN27-A01
按当前 PyTorch 语义，依次写出 parameter filter、EMA buffer、Nesterov matrix、finite-step NS、shape adjustment、decoupled decay 与 parameter update。

### TRN27-A02
为什么 parameter grouping 是算法定义的一部分？分别讨论 fused QKV、embedding、output head、bias/norm 与 convolution reshape。

### TRN27-A03
解释 grad is None 与显式零梯度为何不同；在 momentum、decay 和 conditional computation 下各会产生什么状态差异？

## B. 手算与构造

### TRN27-B01
取 $B_0=0,\mu=0.9,G_1=2,G_2=-1$。分别计算 EMA-style 与 sum-style buffer 的两步轨迹；再计算开启 Nesterov 时当前 PyTorch 风格的 $M_1,M_2$。

### TRN27-B02
令 $\eta=10^{-3},\lambda=0.1,s(A,B)=2$，标量化取 $W_t=3,\widehat Q_t=0.5$。按“base-LR decay 后 adjusted-LR update”计算 $W_{t+1}$；再算错误地让 decay 也用 adjusted LR 的结果。

### TRN27-B03
构造两个标量 worker gradient $G_1=2,G_2=-1$，用 sign 作为一维 msign。比较 sign$(G_1+G_2)$ 与 sign$(G_1)+$sign$(G_2)$，并解释它如何推广为“all-reduce 前后做 polar 不等价”的最小反例。

## C. 推导与证明

### TRN27-C01
在固定 $\mu$、零初始化且无其他非线性时，证明 EMA buffer 与 sum buffer 之间的比例关系；随后解释 normalization、epsilon、clipping、checkpoint 或 time-varying $\mu$ 为何会破坏简单迁移。

### TRN27-C02
证明一般有
$$
\operatorname{polar}\!\begin{pmatrix}G_Q\\G_K\\G_V\end{pmatrix}
\ne
\begin{pmatrix}\operatorname{polar}(G_Q)\\\operatorname{polar}(G_K)\\\operatorname{polar}(G_V)\end{pmatrix},
$$
并说明右侧甚至可能不满足与左侧相同的 spectral budget。

### TRN27-C03
为一个 Muon checkpoint 定义状态不变量：给出至少八个 restore-time assertions，覆盖 tensor identity、shape、group、buffer semantics、dtype、NS、scaling 与 distributed layout。

## D. 边界、反例与纠错

### TRN27-D01
反驳“两个实现都写 momentum=0.95，所以 checkpoint 可互换”。给出至少三种 transition-level 差异。

### TRN27-D02
反驳“局部 shard 上做 Muon 只是 global Muon 的并行实现”。从 nonlinearity、global shape scaling 与跨 shard singular vectors 三方面说明。

### TRN27-D03
找出以下实验描述缺失的最小信息：“我们对所有 weight 使用 Muon，lr=0.001，获得更快收敛。”要求把缺失字段分为算法、参数组、数值和系统四类。

## E. AI 迁移

### TRN27-E01
写一份最小 Muon run manifest，足以让另一团队重建单步状态转移和 parameter ownership。

### TRN27-E02
设计单元测试，逐项检测 decay 是否使用 base LR、None gradient 是否跳过状态、Nesterov 是否在正确 buffer 上组合，以及 save/load 后下一步是否 bitwise/容差一致。

### TRN27-E03
为 fused-QKV Transformer 制定 grouping ablation：比较 joint、按 Q/K/V 分块和按 attention head 分块，列出保持不变的预算与需要报告的 residual/quality/system 指标。

## 作答与复盘

每题记录 independent / hinted / copied / blocked / careless。任何答案若没有具体 transition equation 与字段名，均视为未完成；完成后再打开 [[解答 - Muon 的动量、正交化与参数分组合同]]。
