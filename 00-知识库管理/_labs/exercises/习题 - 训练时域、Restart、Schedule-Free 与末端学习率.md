---
type: exercise
status: verified
area: [training, optimization, horizon, restart, schedule-free]
topic: "[[训练时域、Restart、Schedule-Free 与末端学习率]]"
solution: "[[解答 - 训练时域、Restart、Schedule-Free 与末端学习率]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - 训练时域、Restart、Schedule-Free 与末端学习率

> [!abstract] 训练目标
> 把 horizon、continue、resume、restart、branch 和 fine-tune 分开；能为每次训练转移写出状态 keep/reset/transform 合同，并审计最终输出点。

## A. 识别与复述

### TRN36-A01
区分 continue、resume、restart、branch 与 fine-tune；分别说明参数、optimizer moments、scheduler counter、RNG 和 data cursor 的默认处理。

### TRN36-A02
Schedule-Free 为什么可能不预先使用 horizon，却仍不是 stateless？解释快速点、平均点、求梯度点的不同语义。

### TRN36-A03
区分 last、best-validation、EMA/SWA 与 branch-end checkpoint。为什么末端 LR 与输出选择必须共同报告？

## B. 手算与构造

### TRN36-B01
full-horizon cosine $\eta_t(T)=\tfrac12\eta_{max}[1+\cos(\pi t/T)]$。取 $t=T/2$，比较 horizon 为 $T$ 与 $2T$ 时的 LR。

### TRN36-B02
某 checkpoint 含 $(\theta,m,v,k,r,d)$，分别代表参数、两矩、计数器、RNG、data cursor。为“精确 resume”“只重启 LR”“新数据 fine-tune”各写 keep/reset/transform 表。

### TRN36-B03
在线平均 $x_t=(1-c_t)x_{t-1}+c_tz_t$，$c_t=1/t$，$z_1=2,z_2=4,z_3=10$。算出 $x_1,x_2,x_3$；若 eval 错用 $z_3$，差多少？

## C. 推导与证明

### TRN36-C01
证明对任意 $0<t<T$，把 cosine horizon 从 $T$ 改成 $2T$ 会改变历史 LR；据此说明“从 $T$ checkpoint 继续”不是严格的 $2T$ baseline。

### TRN36-C02
把 restart 写成状态映射 $S^+=R(S^-)$。证明仅说“restart LR”不能唯一确定下一步更新，至少给出两种 moments 处理产生不同结果。

### TRN36-C03
展开一般在线平均 $x_t=(1-c_t)x_{t-1}+c_tz_t$ 的权重，给出权重和为 1 的条件，并解释 evaluation point 是算法的一部分。

## D. 边界、反例与纠错

### TRN36-D01
反驳“schedule-free 就不需要 warmup、LR、状态或 checkpoint 合同”。逐项给出缺失后会发生的歧义。

### TRN36-D02
反驳“只要参数相同，resume 就精确”。构造 moments 或 data cursor 不同导致下一步分叉的例子。

### TRN36-D03
为什么从多个停止时刻中挑验证最好者会增加 selection budget？它如何让“final LR 更好”的结论发生验证泄漏？

## E. AI 迁移

### TRN36-E01
写一份可机读 checkpoint contract，覆盖 version、parameter groups、optimizer state、scheduler phase、averaging state、RNG、data cursor 与 precision scaler。

### TRN36-E02
设计比较 full-horizon cosine、WSD branch 与 Schedule-Free 的实验，要求训练、调参、选择和评估四本预算账都可核对。

### TRN36-E03
为“预训练主干后做三个 cooldown 分支”设计 lineage 图和去重 compute 规则，避免把共享主干重复或漏计。

## 作答与复盘

先画 state transition 表，再查看 [[解答 - 训练时域、Restart、Schedule-Free 与末端学习率]]。
