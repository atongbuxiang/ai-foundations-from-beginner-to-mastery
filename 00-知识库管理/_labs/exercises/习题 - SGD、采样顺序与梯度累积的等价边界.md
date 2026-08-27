---
type: exercise
status: verified
area: [training, optimization, gradient-accumulation]
topic: "[[SGD、采样顺序与梯度累积的等价边界]]"
solution: "[[解答 - SGD、采样顺序与梯度累积的等价边界]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - SGD、采样顺序与梯度累积的等价边界

## A. 识别与复述

### TRN03-A01
列出 gradient accumulation 与一次大 batch 精确等价的六项条件。

### TRN03-A02
区分“累积 gradient 后一步”和“每个 micro-batch 做一步”。

### TRN03-A03
为什么同一 epoch 使用同一 multiset 的样本仍不保证相同轨迹？

## B. 手算与构造

### TRN03-B01
$\ell_i(\theta)=\tfrac12(\theta-y_i)^2$，$\theta_0=0$，$y=(1,3)$，$\eta=0.1$。计算一次大 batch 与依次两步的结果。

### TRN03-B02
两个 micro-batch 有效 token 数为 3 和 7，各自 mean gradients 为 2 和 5。求正确 global token-mean gradient；比较错误地各除 $K=2$。

### TRN03-B03
clip threshold 1，$g_1=2,g_2=-1$。计算 per-micro clip 后相加与先相加后 clip。

## C. 推导与证明

### TRN03-C01
用有限和结合律证明按 $b_k/B$ 加权 micro means 等于 global mean。

### TRN03-C02
证明若每个 micro loss 都加入未缩放的 $\lambda R(\theta)$，累积后 regularizer gradient 被放大 $K$ 倍。

### TRN03-C03
证明对非线性 loss，顺序 SGD 的第二个 gradient 在更新参数处计算，因此一般不等于冻结参数的 batch gradient。

## D. 边界、反例与纠错

### TRN03-D01
用两个不同 micro-batch 均值说明 BatchNorm forward 破坏 per-example 可加性。

### TRN03-D02
构造“数学上等价但浮点不 bitwise 相同”的三个数加法例子。

### TRN03-D03
最后 accumulation window 只有 $K'<K$ 个 micro-batches，代码仍把每个 loss 除 $K$。说明 bias 并给修正。

## E. AI 迁移

### TRN03-E01
为 mixed-precision DDP accumulation 写操作顺序：scale/backward、no-sync、all-reduce、unscale、clip、step、update scaler。

### TRN03-E02
设计一个 accumulation equivalence unit test，分别覆盖 MLP、BatchNorm 网络和 gradient clipping。

### TRN03-E03
审计“accumulation=8 等价于 8 倍 data parallel”在数值、吞吐、通信、BN 和 schedule 上的边界。

## 作答与复盘

完成独立尝试后打开 [[解答 - SGD、采样顺序与梯度累积的等价边界]]。
