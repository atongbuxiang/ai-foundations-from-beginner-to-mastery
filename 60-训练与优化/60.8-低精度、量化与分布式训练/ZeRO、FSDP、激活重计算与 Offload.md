---
type: concept
status: verified
area: [training, distributed-training, memory-optimization]
course_id: TRN-63
prerequisites: ["[[数据并行、All-Reduce 与全局 Batch 语义]]", "[[Tensor、Pipeline、Sequence 与 Expert Parallel]]"]
related: ["[[训练量化、优化器状态压缩与 QAT]]", "[[通信 Roofline、非确定性与分布式训练证据地图]]"]
sources: ["[[S-2020-Rajbhandari-ZeRO]]", "[[S-2026-PyTorch-FSDP]]", "[[S-2016-Chen-Activation-Checkpointing]]", "[[S-2021-Ren-ZeRO-Offload]]", "[[S-2022-Korthikanti-Sequence-Parallelism]]"]
created: 2026-08-26
updated: 2026-08-26
---

# ZeRO、FSDP、激活重计算与 Offload

> [!abstract] 本节目标
> 能按参数、梯度、optimizer/master、activation、temporary collective、workspace 和 allocator 七类对象计算 steady 与 peak memory；理解 sharding、recomputation 和 offload 分别交换什么资源，不再用“理论除以卡数”估显存。

## 一、显存是时间函数

令 $M_j(t)$ 是对象 $j$ 在 step 时间 $t$ 的驻留 bytes，峰值是

$$
M_{peak}=\max_t\sum_jM_j(t),
\tag{1}
$$

不是各对象各自峰值之和，也不是 steady-state 表格的一行。至少分：

1. model weights/buffers；
2. gradients；
3. optimizer states 与 master weights；
4. saved activations；
5. full-parameter/all-gather/reduce-scatter temporary；
6. kernel workspace、通信 bucket；
7. allocator fragmentation、graph/runtime metadata。

## 二、Baseline mixed-precision Adam 账

对 $N$ 个参数，一个常见但非普适的简化是：BF16/FP16 forward weight 2 bytes、gradient 2、FP32 master 4、Adam $m,v$ 各 4，总计

$$
M_{state}\approx16N\text{ bytes}.
\tag{2}
$$

有的框架参数本身就是 FP32 master 并临时 cast；有的 gradient FP32；8-bit optimizer 或无 master policy 又不同。表格必须来自实际 parameter/state tensors，而非背诵 16。

## 三、ZeRO 三阶段的稳态代数

记每 rank 完整 weights、gradients、optimizer/master bytes 为 $W,G,O$，data-parallel degree 为 $P$。忽略临时 buffer 时：

| 方案 | 每 rank steady model-state memory |
|---|---:|
| DDP | $W+G+O$ |
| ZeRO-1 | $W+G+O/P$ |
| ZeRO-2 | $W+(G+O)/P$ |
| ZeRO-3 | $(W+G+O)/P$ |

[[S-2020-Rajbhandari-ZeRO]] 的核心是依次消除 optimizer、gradient、parameter redundancy。这个表只描述均匀 shard 的稳态理想值；activation、buffer、临时 full parameters、bucket 和不均匀分组不在其中。

## 四、FSDP/ZeRO-3 的执行时间线

以 FULL_SHARD 风格模块为例：

1. 计算外只持有 parameter shard；
2. forward 前 AllGather 形成该模块 full parameters；
3. 执行 forward，按策略 reshard；
4. backward 前再 materialize 所需参数；
5. 计算 local gradients；
6. ReduceScatter 得到 gradient shard；
7. 本地 optimizer 更新 state/parameter shard。

峰值取决于是否 prefetch 下一模块、当前 full module 多大、是否同时存在两个 full buffers。wrap 太粗会大峰值，太细会大量小 collective 与 latency。

[[S-2026-PyTorch-FSDP]] 还允许 param/reduce/buffer dtype 分开；“FSDP mixed precision”不是一个 dtype。

## 五、通信量没有凭空消失

DDP 常对完整 gradient 做 All-Reduce；ZeRO-2/3 可用 ReduceScatter 让每 rank 只保留 shard，ZeRO-3 另需 parameter AllGather。是否更快取决于：

- 总 bytes 与 collective 次数；
- 网络拓扑和 group；
- bucket/wrap 大小；
- 与 forward/backward 的 overlap；
- parameter reuse 和 reshard policy。

“与 DDP 同阶通信”不等于同 latency 或同关键路径。

## 六、Activation memory 与 checkpointing

对 Transformer 的粗量级，saved activation 可随

$$
M_A=O(BSLH)
$$

增长，并包含 QKV、attention probabilities、MLP intermediate 等不同常数。checkpointing 只保存部分边界，backward 时重算内部 forward。

对 $L$ 层均匀链，分成约 $\sqrt L$ 段可获得经典 $O(\sqrt L)$ activation 驻留与额外 forward work 的权衡。[[S-2016-Chen-Activation-Checkpointing]] 提供该主线；现代 selective recomputation 会按 tensor bytes/FLOPs 选择，而非整层一刀切。

重算正确还需恢复 dropout/RNG/autocast 状态；否则 graph 数学上相同，实际随机路径不同。

## 七、Offload 把 capacity 问题变成数据移动问题

若每 step 需在 host/device 间传 $M_{move}$ bytes，有效带宽 $B_{link}$，至少有

$$
T_{move}\ge\frac{M_{move}}{B_{link}}+n_{msg}\alpha.
\tag{3}
$$

若能与 GPU compute 重叠，关键路径增加近似

$$
T_{tail}\approx\max(0,T_{move}-T_{overlap\ window}).
\tag{4}
$$

[[S-2021-Ren-ZeRO-Offload]] 把 optimizer state/compute 放 CPU 以换取 GPU capacity。真实收益依赖 CPU 算力、pinned memory、PCIe/NVLink、NUMA、prefetch 和 page fault。NVMe offload 又有更低带宽/更高 latency。

## 八、Peak-memory 手算例

假设 $N=1$B，$W=2$ GB、$G=2$ GB、FP32 master+$m+v=12$ GB，所以 model states 共 16 GB。$P=8$ 的理想 ZeRO-3 稳态为 2 GB/rank。

但若一个 wrap unit 的 full parameters 为 1.2 GB，双 buffer prefetch 为 2.4 GB，saved activations 8 GB，workspace/buckets 3 GB，allocator reserve 2 GB，则峰值至少近似

$$
2+2.4+8+3+2=17.4\text{ GB},
$$

而不是“16/8=2 GB”。这正是 steady 与 peak 分账的必要性。

## 九、Checkpoint 与故障恢复

分片训练的 checkpoint 还要声明：

- sharded/local/full state dict；
- model、optimizer、scaler、scheduler、RNG、data sampler 的 state；
- 保存时是否 all-gather，峰值内存/网络/存储 bytes；
- world size 改变时怎样 reshard；
- 异步保存是否冻结了一致 logical step；
- 恢复后 skipped update 与 accumulation window 是否重放。

能保存权重不等于能精确继续训练。

## 十、图解：为什么 $16N/P$ 不是峰值答案

带着一个问题读图：**模型状态已完全分片后，为什么 forward/backward 仍可能 OOM？**

![[00-知识库管理/_assets/figures/training-optimization/fig-zero-fsdp-memory-timeline-v1.svg|900]]

> [!figure] 图 TRN-63-01　持久状态账本与 FSDP/ZeRO-3 峰值时间线
> 来源：自绘机制图；分片语义依据 [[S-2020-Rajbhandari-ZeRO]] 与 [[S-2026-PyTorch-FSDP]]，重计算依据 [[S-2016-Chen-Activation-Checkpointing]]，offload 依据 [[S-2021-Ren-ZeRO-Offload]]。

**怎样读图**：左栏只算理想持久 model state；右栏把它当底座，再沿时间叠加 layer all-gather、live activation、gradient、workspace 与 allocator。峰值是整条 $M(t)$ 的最大值，而不是稳态分片公式。

**图没有证明什么**：阶梯高度不是某框架的实测 trace，也没有断言 checkpointing/offload 总能提速；它们用 recompute 或数据移动交换 capacity，是否获益必须看关键路径。

## 十一、决策矩阵

| 瓶颈 | 首选候选 | 付出的资源 |
|---|---|---|
| optimizer/gradient/parameter redundancy | ZeRO/FSDP | collective、临时 full params |
| saved activation | checkpoint/selective recompute/SP | extra FLOPs、RNG 复杂性 |
| device capacity 仍不足 | CPU/NVMe offload | link bytes、CPU/NVMe time |
| 单层本身放不下 | tensor/expert parallel | 层内 collective |
| 深度/总模型放不下 | pipeline parallel | bubble、P2P、schedule state |

最终选择必须用 peak memory、time-to-quality、failure/restart 与工程复杂度共同验收。
