---
type: exercise
status: verified
area: [training, telemetry, diagnostics]
topic: "[[训练 Telemetry、损失梯度更新与激活总账]]"
solution: "[[解答 - 训练 Telemetry、损失梯度更新与激活总账]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - 训练 Telemetry、损失梯度更新与激活总账

> [!abstract] 训练目标
> 能从训练闭环定义多时钟和六本账，设计开销可控的 telemetry，并从指标先后提出而非武断确认根因。

## A. 识别与复述

### TRN65-A01
列出 wall、microstep、optimizer-step、token 与 scheduler 五个时钟，并说明它们何时会分叉。

### TRN65-A02
列出数据、目标、梯度、更新、参数/激活、系统六本账；每本给两个最小字段。

### TRN65-A03
区分 raw gradient、preconditioned direction 与 realized update。为什么只记 gradient norm 不足以诊断 Adam？

## B. 手算与构造

### TRN65-B01
一次 optimizer update 累积 4 个 microbatches，每个有效 token 数为 980、1000、940、1080。计算该 update 的 token 增量；若第 3 个 update 因 overflow 被跳过，microstep、attempt、optimizer-step 与 token clock 各怎样变化？

### TRN65-B02
logging 每 50 optimizer steps 记录一次，EWMA 的 $\beta=0.9$。估算其记忆长度分别为多少次观测和多少 optimizer steps。

### TRN65-B03
某层参数有 10,000 个元素，gradient norm 为 2，update norm 为 0.05，weight norm 为 5。计算 gradient RMS、update RMS 与 layer UWR。

## C. 推导与证明

### TRN65-C01
证明只知道 batch mean loss，无法恢复样本 loss 方差；构造两个 batch 具有相同均值、不同尾部。

### TRN65-C02
把 AdamW 的 realized update 分成 task direction 与 decay 两项，说明记录总 update norm 为什么不能判断哪一项主导。

### TRN65-C03
说明 sampling interval 与 aggregation window 怎样造成 first-change time 的观测偏移；给出一个更早异常被低频日志晚报的例子。

## D. 边界、反例与纠错

### TRN65-D01
反驳：“training loss 平滑下降，所以训练一定健康。”至少给出 activation、selection 与系统三个反例。

### TRN65-D02
反驳：“指标 A 比 loss 早变化，因此 A 是根因。”指出采样率、共同原因与中介三种竞争解释。

### TRN65-D03
反驳：“telemetry 越密越好。”说明同步、hook、I/O 与保存完整 tensor 怎样改变训练。

## E. AI 迁移

### TRN65-E01
为一个 mixed-precision DDP Transformer 设计 L0/L1/L2 三级 telemetry；写明每级频率和触发条件。

### TRN65-E02
设计三个机器可验不变量，分别覆盖 token 计数、skipped update 和 resume 连续性。

### TRN65-E03
面对“validation 停滞但 train loss 下降”，写出最小 dashboard 和三条竞争解释，说明下一步怎样缩小范围。

## 作答与复盘

先独立画训练闭环与五时钟，再查看 [[解答 - 训练 Telemetry、损失梯度更新与激活总账]]。错题需标记为 clock、object、aggregation、invariant 或 causal-boundary 错误。
