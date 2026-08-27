---
type: exercise
status: verified
area: [training, distributed-systems, memory]
topic: "[[ZeRO、FSDP、激活重计算与 Offload]]"
solution: "[[解答 - ZeRO、FSDP、激活重计算与 Offload]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - ZeRO、FSDP、激活重计算与 Offload

> [!abstract] 训练目标
> 能从对象生命周期计算 steady 与 peak memory，推导 ZeRO/FSDP 分片账、checkpointing 重计算边界和 offload 链路下界，并写出可恢复 checkpoint 合同。

## A. 识别与复述

### TRN63-A01
区分 parameter、gradient、optimizer state、master weight、activation、temporary buffer 与 allocator reserved memory；哪些通常随 batch/sequence 变化？

### TRN63-A02
说明 ZeRO-1、2、3 分别分片哪些 model states。FSDP full-shard 的执行语义为何不能只描述成“每卡存 $1/P$ 参数”？

### TRN63-A03
activation checkpointing 与 CPU/NVMe offload 各用什么资源换显存？列出其新关键路径风险。

## B. 手算与构造

### TRN63-B01
理想 mixed-precision Adam 为 16 B/parameter。对 $N=1$B、$P=8$，计算 DDP、ZeRO-1、ZeRO-2、ZeRO-3 的稳态 model-state bytes，采用参数2 B、梯度2 B、master4 B、moments8 B。

### TRN63-B02
某 rank 的持久 shard 2 GB、一次 full-layer gather 3 GB、当时 live activation 8 GB、workspace 1.5 GB、其他 buffer 0.9 GB。求该时刻 live peak；为什么不能报 2 GB？

### TRN63-B03
每 step 需从 CPU 搬入并写回共 24 GB optimizer state，单向可持续带宽 48 GB/s，假设不能重叠。求仅传输的时间下界；若 step compute 为 0.35 s，判断瓶颈。

## C. 推导与证明

### TRN63-C01
用上述 16 B 账推导各 ZeRO stage 的 per-rank 稳态式，并指出 padding、metadata、bucket 与临时 full params 为什么使实测更大。

### TRN63-C02
把 peak memory 写成 $\max_t\sum_j M_j(t)$。构造两个对象单独峰值都不大、但生命周期重叠导致 OOM 的时间线。

### TRN63-C03
对 $L$ 层等成本网络，说明每隔约 $\sqrt L$ 层保存 checkpoint 可将保存 activation 数量降到 $O(\sqrt L)$，同时引入重计算。

## D. 边界、反例与纠错

### TRN63-D01
反驳：“ZeRO-3 把 16N 除以 $P$，所以显存峰值就是 $16N/P$。”至少列出四个瞬态或非 model-state 项。

### TRN63-D02
反驳：“activation checkpointing 只省显存，不改变数值结果。”讨论 dropout/RNG、stateful op、autocast 与非确定 kernel。

### TRN63-D03
反驳：“offload 到 CPU 后 GPU 显存越低，训练一定越快。”给出 PCIe/NVLink、pinned memory、prefetch 与 contention 反例。

## E. AI 迁移

### TRN63-E01
为一次 OOM 写 memory-trace 采集表，至少包含对象、dtype、shape、生命周期、allocated/reserved、collective/recompute 与时间戳。

### TRN63-E02
设计 ZeRO-3、checkpointing 与 offload 的逐步消融，规定 capacity、tokens/s、time-to-quality、failure/restart 与工程复杂度验收。

### TRN63-E03
写一个 world-size-independent checkpoint 合同：列出 model/optimizer shards、param ordering、RNG、sampler、scaler、scheduler 与 topology metadata 的恢复政策。

## 作答与复盘

先画 $M(t)$，再查看 [[解答 - ZeRO、FSDP、激活重计算与 Offload]]。若只给稳态除法、不列瞬态和 activation，memory 题视为未完成。
