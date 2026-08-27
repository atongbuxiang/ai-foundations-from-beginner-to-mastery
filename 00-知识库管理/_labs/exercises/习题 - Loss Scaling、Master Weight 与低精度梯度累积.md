---
type: exercise
status: verified
area: [training, numerical-computing, mixed-precision]
topic: "[[Loss Scaling、Master Weight 与低精度梯度累积]]"
solution: "[[解答 - Loss Scaling、Master Weight 与低精度梯度累积]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Loss Scaling、Master Weight 与低精度梯度累积

> [!abstract] 训练目标
> 能推导 loss scaling 的链式法则，计算安全 scale 区间，区分 attempt/backward/update 时钟，并实现样本加权 accumulation 与全局 overflow consensus。

## A. 识别与复述

### TRN58-A01
loss scaling、FP32 master weight 与 gradient accumulation 分别解决什么问题？为什么三者不能互相替代？

### TRN58-A02
区分 attempt clock、backward clock 与 successful-update clock。scheduler、EMA 和 optimizer moments 应绑定哪一个时钟，为什么必须声明？

### TRN58-A03
写出 dynamic GradScaler 的最小状态：当前 scale、增长/回退因子、增长间隔和连续成功计数；描述 finite 与 overflow 两条转移。

## B. 手算与构造

### TRN58-B01
未缩放 gradient 的非零绝对值范围为 $[2^{-30},2^8]$，FP16 最小保留阈值按 $2^{-24}$、最大有限值按 $2^{15}$ 粗算。求同时避免下溢与溢出的 $S$ 区间。

### TRN58-B02
两个 micro-batch 有效样本数分别为 3、1，对应 gradient sum 为 $s_1=(3,6)$、$s_2=(5,1)$。求全局 sample-mean gradient；若直接平均两个 local mean，得到什么？

### TRN58-B03
初始 scale 1024，backoff $=1/2$，growth $=2$，每连续 2 次成功增长。给定结果序列 success, success, overflow, success, success，列出每次检查后的 scale 与 successful-update count。

## C. 推导与证明

### TRN58-C01
对 $\widetilde L=S L$ 用链式法则证明 $\nabla_\theta\widetilde L=S\nabla_\theta L$；说明为什么 unscale 后的精确梯度方向不变，以及有限精度下仍可能不同的边界。

### TRN58-C02
证明若先对 scaled gradient 以固定阈值 $\tau$ clip、再除以 $S$，等价于对原 gradient 使用阈值 $\tau/S$，因此算法随 scale 漂移。

### TRN58-C03
推导用 FP16 参数副本直接更新时的 half-ulp 停滞条件，并说明 FP32 master weight 如何把多次小更新累积到可见变化。

## D. 边界、反例与纠错

### TRN58-D01
反驳：“gradient accumulation 只要除以 micro-step 数就等价于大 batch。”给出 unequal micro-batch 或 token mask 反例。

### TRN58-D02
反驳：“每个 rank 独立判断 overflow 就可以；有问题的 rank 自己 skip。”说明参数与 optimizer state 如何分叉。

### TRN58-D03
反驳：“skipped step 没更新参数，所以 scheduler/EMA 是否前进无所谓。”给出第四次首次成功更新已不同的最小例子。

## E. AI 迁移

### TRN58-E01
为 AMP + DDP + accumulation 写一个按顺序的 step 状态机，明确 `no_sync`、unscale、finite consensus、clip、step、scheduler 与 zero-grad 的位置。

### TRN58-E02
设计 telemetry 表来诊断 intermittent overflow：至少包含 scale、amax、nonfinite、skip、梯度范数、三个时钟与 rank consensus。

### TRN58-E03
设计 FP32 reference、目标 mixed-precision policy 和三个单因素变体的比较，说明如何用 time-to-quality 而非单 step 吞吐验收。

## 作答与复盘

先把状态机画出来，再查看 [[解答 - Loss Scaling、Master Weight 与低精度梯度累积]]。复盘时强制回答：哪个对象被 scale、哪个时钟前进、哪个 divisor 最后只执行一次。
