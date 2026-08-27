---
type: exercise
status: verified
area: [training, scaling-laws, systems]
topic: "[[IsoFLOP、训练算力口径与系统校正]]"
solution: "[[解答 - IsoFLOP、训练算力口径与系统校正]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - IsoFLOP、训练算力口径与系统校正

> [!abstract] 训练目标
> 建立从模型 FLOPs 到硬件执行、墙钟时间、能耗与碳排的分层账本，避免把不同成本对象混写成一个“算力”。

## A. 识别与复述

### TRN52-A01
区分 model FLOPs、executed hardware FLOPs、peak hardware FLOPs、wall-clock time、energy 与 carbon。哪些量需要系统遥测而不能只由模型配置推出？

### TRN52-A02
区分 total、non-embedding、active 与 trainable parameter count。对 dense、MoE、冻结微调分别说明哪一项最容易误导。

### TRN52-A03
解释 MFU 与 HFU 的分子、分母和用途。activation checkpointing 为什么常使二者差异扩大？

## B. 手算与构造

### TRN52-B01
用 $C_{model}\approx6ND$ 估算一个 $N=10^9$、$D=3\times10^{11}$ 的 dense decoder 预训练 FLOPs。写成科学计数法。

### TRN52-B02
某集群峰值为 $2\times10^{18}$ FLOP/s，训练的 model FLOPs 为 $1.8\times10^{21}$，MFU 为 45%。估算训练秒数与小时数。

### TRN52-B03
训练平均功率 1.2 MW、持续 100 小时，PUE 为 1.15，电网强度 0.35 kgCO$_2$e/kWh。计算设施总能耗与碳排。

## C. 推导与证明

### TRN52-C01
从一次参数在 forward 中约一次乘加、backward 对 activation 与 weight 各需同阶工作出发，解释 $6ND$ 的来源及其失效项。

### TRN52-C02
推导
$$
t\approx\frac{C_{model}}{P_{peak}\cdot MFU},
$$
并写出由 $t$、平均 IT 功率、PUE 和电网强度得到 energy/carbon 的链条。

### TRN52-C03
设 executed FLOPs $C_{hw}=rC_{model}$。证明若把 HFU 错当 MFU，估计时间会差一个怎样的因子？

## D. 边界、反例与纠错

### TRN52-D01
反驳：“两个训练运行 model FLOPs 相同，所以时间、费用和碳排也相同。”

### TRN52-D02
MoE 模型有 1T total 参数、50B active 参数。为什么把 1T 直接代入 $6ND$ 可能高估主干计算，却仍可能低估通信与路由代价？

### TRN52-D03
为什么较低 FLOPs 不必然意味着较低碳排？给出硬件利用率、电力来源与时段三个反例机制。

## E. AI 迁移

### TRN52-E01
写一个 compute manifest，至少包含参数口径、token 口径、算子边界、精度、重算、稀疏、硬件、利用率和失败运行。

### TRN52-E02
设计一次两种训练系统的公平 time-to-quality 比较：规定质量阈值、预热、编译、超参、失败与不确定性如何处理。

### TRN52-E03
为论文中的“训练成本降低 40%”写审计问题，确保能判断它指 FLOPs、GPU-hours、美元、能耗还是碳排。

## 作答与复盘

每次计算先写明账本层级，再查看 [[解答 - IsoFLOP、训练算力口径与系统校正]]；不允许用“算力”一词掩盖单位。
