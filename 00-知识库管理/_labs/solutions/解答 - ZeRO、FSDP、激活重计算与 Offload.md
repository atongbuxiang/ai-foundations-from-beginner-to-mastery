---
type: solution
status: verified
area: [training, distributed-systems, memory]
topic: "[[ZeRO、FSDP、激活重计算与 Offload]]"
exercise: "[[习题 - ZeRO、FSDP、激活重计算与 Offload]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - ZeRO、FSDP、激活重计算与 Offload

> [!warning] 使用边界
> 所有 $N/P$ 都是理想稳态账；实际是否 OOM 由时间线上的 activation、gather、workspace、allocator 与并发 buffer 共同决定。

## A. 识别与复述

### TRN63-A01
parameter/gradient/master/moments 是 model/optimizer state；activation 是 forward 为 backward 保存的中间量；temporary buffer 来自 kernel/collective；allocated 是活跃分配，reserved 还含 allocator cache。activation 常随 local batch、sequence、hidden/layers 增长；有些 workspace 与 shape 也变，parameter/state 通常不随 batch 变。

### TRN63-A02
ZeRO-1 分片 optimizer states（在本账含 FP32 master/moments），ZeRO-2 再分 gradient，ZeRO-3 再分 parameter。full-shard 执行时仍需在层前 all-gather 可计算参数、层后 reshard，并在 backward 再 materialize/reduce-scatter；所以稳态 $1/P$ 旁有 transient full-layer bytes 与通信。

### TRN63-A03
checkpointing 用 extra FLOPs/时间和更复杂 RNG 重放换 saved activation；offload 用 CPU/NVMe 容量换 PCIe/NVLink/NVMe 传输、host memory 和 prefetch 调度。新瓶颈分别是 recompute 关键路径与数据移动尾巴。

## B. 手算与构造

### TRN63-B01
按 params 2、grads 2、optimizer/master 12 B：DDP $16N=16$ GB；ZeRO-1 $4N+12N/8=5.5$ GB；ZeRO-2 $2N+(2+12)N/8=3.75$ GB；ZeRO-3 $16N/8=2$ GB。均不含 activation、buffer、metadata 与 allocator。

### TRN63-B02
若这些对象同时 live，峰值为 $2+3+8+1.5+.9=15.4$ GB。2 GB 只是 persistent shard；OOM 发生在生命周期重叠处，因此必须报告 $M(t)$ 而不是一条 steady formula。

### TRN63-B03
顺序传输下界 $24/48=0.5$ s。它大于 compute 0.35 s，且题设不能 overlap，所以至少 0.85 s/step，数据移动是主导项。真实双向同时传输、协议与 contention 会改变数值，需实测。

## C. 推导与证明

### TRN63-C01
DDP 为 $2+2+12=16$ B/N。Stage 1 只除 optimizer：$4+12/P$；Stage 2 再除 grad：$2+14/P$；Stage 3 全分：$16/P$。padding/alignment、flat-param metadata、prefetch bucket、all-gather full layer、reduce buffer 与 delayed free 都会把实测 peak 推高。

### TRN63-C02
正确式是
$$
M_{peak}=\max_t\sum_jM_j(t).
$$
例如 activation A 在 $t=1..5$ 占 8 GB，parameter gather B 在 $t=4..6$ 占 6 GB；各自峰值不超 8 GB，但 $t=4..5$ 合计 14 GB，若容量 12 GB 就 OOM。逐项最大值或稳态平均都看不到重叠。

### TRN63-C03
把 $L$ 层分成约 $\sqrt L$ 段，每段长度约 $\sqrt L$；只保存段边界约 $\sqrt L$ 个 activation。backward 到某段时从边界重算该段，段内临时 activation 也约 $\sqrt L$，总同时保存阶为 $O(\sqrt L)$，代价是额外 forward compute。常数和最优策略依层成本/大小而变。

## D. 边界、反例与纠错

### TRN63-D01
反例项包括：当前 wrapped layer 的 full parameter all-gather；saved/live activation；gradient/reduce-scatter bucket；kernel workspace；prefetch 的下一层参数；allocator fragmentation/reserved；通信临时 buffer。任意重叠都使 peak 大于 $16N/P$。

### TRN63-D02
recompute 若未恢复 dropout RNG，会产生不同 mask；stateful op 可能被执行两次；autocast context 或 kernel choice 不一致会改变数值；并行 non-deterministic op 也可分叉。应保存/恢复 RNG 并用 forward/recompute oracle 检验所需复现层级。

### TRN63-D03
若每 step 从 CPU 拉回大量 state，PCIe 传输可超过 compute；pinned host memory 不足、NUMA 错位、NVMe queue、同时 data-loader 争用、prefetch 太早占 GPU/太晚造成 stall 都可能降速。容量成功与 time-to-quality 成功是两条门。

## E. AI 迁移

### TRN63-E01
每个 event 记录 timestamp、rank、phase/layer、对象名、global/local shape、dtype/bytes、allocated/reserved、create/free、stream、gather/reshard/reduce、checkpoint save/recompute、prefetch/offload、workspace、OOM 前最后成功点。配套周期性 memory snapshot 与 profiler，才能重建 $M(t)$。

### TRN63-E02
从 DDP/FSDP baseline 开始，依次只加 ZeRO-3、再加 checkpointing、再加 offload；每步保持 model/data/update contract。验收 peak allocated/reserved 与最大可训练 shape；tokens/s/step tail；matched learning curve/time-to-quality；OOM/NaN/restart 分母；checkpoint 大小/恢复时间和维护复杂度。只在前一步仍不满足 capacity 时引入下一机制。

### TRN63-E03
保存逻辑参数名/稳定 ID 到 shard 映射、model/master/gradient-policy/optimizer states、param-group 与 ordering、scaler、scheduler/EMA、global update id、RNG streams、sampler/data cursor、dataloader state、parallel mesh/topology metadata与软件版本。恢复时先按逻辑全局对象重分片到新 world size，再验证小步数值/质量；不能依赖旧 rank 编号直接拼文件。

## 无提示重做

- [ ] 48 小时后重算四种稳态账。
- [ ] 一周后从一次 OOM trace 找出生命周期重叠。
