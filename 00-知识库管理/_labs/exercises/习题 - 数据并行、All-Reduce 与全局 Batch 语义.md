---
type: exercise
status: verified
area: [training, distributed-systems, data-parallelism]
topic: "[[数据并行、All-Reduce 与全局 Batch 语义]]"
solution: "[[解答 - 数据并行、All-Reduce 与全局 Batch 语义]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - 数据并行、All-Reduce 与全局 Batch 语义

> [!abstract] 训练目标
> 能从全局经验风险推导 DDP reduction，处理 unequal inputs 与二维 accumulation，并把 ring 字节、bucket overlap 和数值等价分层审计。

## A. 识别与复述

### TRN61-A01
数据并行复制什么、切分什么、在哪个对象上同步？“world size”为什么不必等于 data-parallel degree？

### TRN61-A02
区分 local sum、local mean、collective sum 与 collective mean。为什么必须把最后 divisor 与前两层 operator 一起写？

### TRN61-A03
定义 local micro-batch、per-rank accumulated batch、global batch 与 token-weighted batch；哪些量会随 TP/PP 度数增加，哪些不会？

## B. 手算与构造

### TRN61-B01
三个 rank 有效样本数为 $(4,2,3)$，local gradient mean 为 $(1,4,7)$（标量）。求正确 global sample mean 与简单 rank mean，并解释差异。

### TRN61-B02
长度 $M=1$ GiB 的 gradient、$P=8$。按 ring All-Reduce 每 rank 传输量 $2(P-1)M/P$，计算字节量；与 parameter server 每 worker 发送并接收 $M$ 的粗略量比较。

### TRN61-B03
DP degree 16、TP degree 4、PP degree 2，每 rank 每次 forward micro-batch 为 2，accumulation 8 次。若无其他复制轴，求总 GPU 数和 global batch；指出把总 GPU 数乘进 batch 的错误结果。

## C. 推导与证明

### TRN61-C01
从 $L=(1/N)\sum_{r,i}\ell_{ri}$ 推导 $g=(\sum_r s_r)/(\sum_r n_r)$，其中 $s_r=\sum_i\nabla\ell_{ri}$。何时 average of local means 才等价？

### TRN61-C02
推导二维 micro-step × rank 账本：每个 cell 保存 gradient sum 与有效 token/sample count；说明最后一次归一化为何最稳妥。

### TRN61-C03
推导 ring All-Reduce 的 reduce-scatter 与 all-gather 各需 $P-1$ 轮、每轮约传 $M/P$，得到总量 $2(P-1)M/P$。

## D. 边界、反例与纠错

### TRN61-D01
反驳：“64 GPU、每卡 batch 8，所以 global batch 必为 512。”构造其中含 TP=8 的配置。

### TRN61-D02
反驳：“All-Reduce 代数相同，所以多卡与单卡应逐比特相同。”用浮点非结合律与 bucket/order 说明。

### TRN61-D03
反驳：“最后一个 uneven batch 可以照常平均 rank mean，影响可忽略。”给出小 rank 提前结束或 padding mask 的系统偏差。

## E. AI 迁移

### TRN61-E01
为 DDP + variable-length sequence 写最小 reduction manifest，至少包含 sampler、mask/token count、loss reduction、collective dtype/operator 与 divisor。

### TRN61-E02
设计从 1 到 64 个 DP ranks 的 strong-scaling 实验，明确 baseline、fixed global batch、warmup、bucket、质量与失败指标。

### TRN61-E03
构造一个验证框架 DDP reduction 语义的 tiny oracle：明确输入、解析梯度、单卡参照、容差和逐比特边界。

## 作答与复盘

所有 batch 题先画 DP/TP/PP mesh，再查看 [[解答 - 数据并行、All-Reduce 与全局 Batch 语义]]。只写“除以 world size”而不写 local reduction 和有效计数，视为不完整。
