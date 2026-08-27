---
type: solution
status: draft
area: [architecture, efficient-attention, complexity, systems]
topic: "[[Attention 的二次复杂度、内存与 IO 瓶颈]]"
exercise: "[[习题 - Attention 的二次复杂度、内存与 IO 瓶颈]]"
sources: ["[[S-2022-Dao-FlashAttention]]", "[[S-2021-Su-8610-线性Transformer反例]]", "[[S-2020-Su-7546-线性Attention]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - Attention 的二次复杂度、内存与 IO 瓶颈

## A. 识别与复述

### ARCH-COST-A01
训练和 prefill 同时处理 $n$ 个 queries，dense pairwise 部分约为 $2Bn^2d$ MAC；训练还要为反向保存或重算状态。Decode 第 $t$ 步只有一个新 query，单步 attention 算术约随 $t$ 线性增长，却反复读取历史 KV。因而需要分别报告训练、prefill、单步 decode 和累计生成；一个 $O(n^2)$ 标签既不说明常数，也不说明内存与 IO。

### ARCH-COST-A02
FLOPs/MACs 数算术工作；峰值显存数某一时刻驻留的参数、状态、activation/cache 与临时 buffer；HBM 流量数跨慢速显存边界搬运的 bytes；KV payload 只数每层已缓存 K/V 标量；wall-clock 是具体硬件、kernel、并发和同步共同产生的时间。它们相关但不是可互换的指标。

### ARCH-COST-A03
忽略 bias 与常数实现差异：Q/K/V/O 投影为 $4Bnd^2$；score 与 value aggregation 为 $2Bn^2d$；两矩阵 FFN 为 $2Bndd_{ff}$。总主项为 $4Bnd^2+2Bn^2d+2Bndd_{ff}$。

## B. 手算与建模

### ARCH-COST-B01
$4Bnd^2=4\cdot2\cdot2048\cdot1024^2=17{,}179{,}869{,}184$ MAC；$2Bn^2d=2\cdot2\cdot2048^2\cdot1024=17{,}179{,}869{,}184$ MAC；$2Bndd_{ff}=2\cdot2\cdot2048\cdot1024\cdot4096=34{,}359{,}738{,}368$ MAC。此配置中 FFN 主项最大，是另外两项各两倍；不能仅凭 $n^2$ 就断言 attention 已支配全层。

### ARCH-COST-B02
payload 为 $2LBTh_{kv}d_hs$ bytes：
$$2\cdot32\cdot1\cdot8192\cdot8\cdot128\cdot2=1{,}073{,}741{,}824\ \text{bytes}=1\ \text{GiB}.$$
这不含 allocator/page、padding、量化 scale、metadata 或并行副本。

### ARCH-COST-B03
令 $an^2=bn$，非零交点为 $n_*=b/a$。若 linear 方法固定成本为 $c$，则应解 $an^2=bn+c$。$a,b,c$ 依 kernel、dtype、并行度和硬件；渐近记号丢弃这些量，所以不能给出实际 crossover。

## C. 推导与证明

### ARCH-COST-C01
第 $t$ 个生成步读取约 $2h_{kv}d_h(T_0+t-1)$ 个 K/V 标量。跨 $N$ 步求和为
$$2h_{kv}d_h\sum_{t=1}^{N}(T_0+t-1)=2h_{kv}d_h\left(NT_0+\frac{N(N-1)}2\right).$$
当 $T_0$ 固定、$N\to\infty$ 时为 $\Theta(N^2h_{kv}d_h)$；KV cache 避免重算投影，却没有消除读历史的累计二次项。

### ARCH-COST-C02
每头每个 query-key 对一个 score，shape 为 $B\times h_q\times n\times n$，故 $Bh_qn^2$ 个标量。FlashAttention 分块重算/归约 score，不把完整矩阵写入 HBM，所以峰值中间存储可近线性；但每个 query 仍与每个 key 做点积，pairwise MAC 仍是 $\Theta(Bn^2d)$。

### ARCH-COST-C03
若总算术量为 $F$、慢存储流量为 $Q$ bytes，算术强度 $I=F/Q$。运行性能上界为
$$\min(P,WI),$$
时间下界为 $\max(F/P,Q/W)$。当 $I>P/W$ 时算力上界更紧，近似 compute-bound；当 $I<P/W$ 时带宽上界更紧，近似 bandwidth-bound。

## D. 边界、反例与纠错

### ARCH-COST-D01
少 FLOPs 可能伴随更多不规则 gather、kernel launches、同步、低 occupancy 或更大重算；训练还受 backward/optimizer 影响，decode 常受 cache bandwidth 影响。因此同一 FLOP 下降可能在训练、prefill、decode 得到完全不同的时间变化，必须实测各阶段。

### ARCH-COST-D02
取 dense 时间 $t_d(n)=n^2$，linear 时间 $t_l(n)=1000+10n$。在 $n=16$ 时 $t_d=256<t_l=1160$；直到解 $n^2>1000+10n$ 后 linear 才可能胜出。这就是有限规模常数压倒渐近阶的最小反例。

### ARCH-COST-D03
“显存”可包含参数、梯度、optimizer state、activation、临时 workspace、KV cache 与 allocator 碎片。50% 下降若没有分项和峰值时间线，就无法知道是训练 activation checkpointing、权重量化、cache head sharing，还是仅测试 batch/length 改变造成。

## E. AI 迁移

### ARCH-COST-E01
固定模型/checkpoint 与 tokenizer，取 batch/concurrency、prompt length、generated length 的二维或三维网格；逐项记录硬件型号、软件版本、dtype/quantization、cache layout、sampling 参数和 warmup。输出 prefill tok/s、time-to-first-token、inter-token latency 分布、end-to-end tok/s、峰值显存、能耗/功率及失败/OOM 边界。

### ARCH-COST-E02
Prefill 扫 prompt length，记录 achieved FLOPs、SM utilization、HBM bandwidth、kernel breakdown、TTFT 与峰值 workspace；decode 固定 prompt、扫 batch/并发与生成长度，记录每 token bytes、带宽占用、ITL p50/p95、cache hit/layout 和 arithmetic intensity。用 profiler 验证瓶颈，不用吞吐单值反推机制。

### ARCH-COST-E03
模板至少含：模型函数是否改变（pattern/kernel/normalization/cache 参数化）；理论 shape 与复杂度；中间量/bytes/通信；近似误差或 exact 合同；训练与评估任务、长度、seed；质量与稳定性；硬件/kernel/version；训练、prefill、decode 分阶段 wall-clock；crossover 和失败区间。最后把代数、理论、实验、解释与开放问题分级。
