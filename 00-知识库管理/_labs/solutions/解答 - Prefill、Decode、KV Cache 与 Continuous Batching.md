---
type: solution
status: verified
area: [language-models, inference, serving]
topic: "[[Prefill、Decode、KV Cache 与 Continuous Batching]]"
exercise: "[[习题 - Prefill、Decode、KV Cache 与 Continuous Batching]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Prefill、Decode、KV Cache 与 Continuous Batching

## A. 识别与复述

### LM54-A01
Prefill 处理整段已有 prompt，可在 token 维并行并建立 KV，TTFT 对它敏感；decode 每请求每轮只推进一个 token，必须等待上一 token，TBT/TPOT 对它敏感。Batch 可把多个请求的 decode 拼起来提高利用率，但单请求的时间依赖仍串行。

### LM54-A02
每层缓存历史 token 的 K 与 V，使新 query 无需重算旧 token 的 K/V 和前缀前向；代价是显存随 live tokens 线性增长，另有读带宽、allocator、分页表、共享/回滚和生命周期管理。

### LM54-A03
FlashAttention 分块 exact attention，减少中间 attention 矩阵的 HBM IO/存储；PagedAttention 把跨步持久 KV 映射到非连续固定 blocks，减少预留与碎片并支持共享。一个是算子 IO 路径，一个是服务 KV allocator/寻址。

## B. 手算与构造

### LM54-B01
每 token 为 $32\times2\times8\times128\times2=131072$ bytes，即 128 KiB。4096 tokens 为 536,870,912 bytes，即 512 MiB。未计 metadata、对齐、workspace 与权重。

### LM54-B02
Block 数为 $\lceil n/16\rceil$：2、2、3，总 7。最后块空位分别 15、0、1，总内部空位 16 tokens。长度 32 恰好填满最后块。

### LM54-B03
TTFT=$140-0=140$ ms。若首 token timestamp 为 140，后续 TBT 为 40、55、60 ms；E2E=$300-0=300$ ms。Prefill queue wait 为 40 ms，但 TTFT 还含 prefill/调度/首 token 返回。

## C. 推导与证明

### LM54-C01
每层每个 token 有 $n_{kv}d_h$ 个 K 元素和同数 V 元素，共因子 2；每元素 $b$ bytes，跨 $L$ 层相加，所以 $b_{\rm token}=L\cdot2\cdot n_{kv}\cdot d_h\cdot b$。总 KV 再乘 live cached tokens；GQA/MQA 必须用 KV head 数。

### LM54-C02
写 $n=qP+r$，$0\le r<P$。若 $r=0$ 无浪费；若 $r>0$，最后块空位 $P-r$，满足 $0<P-r<P$。因此单请求末块内部浪费严格少于一个 block；不含 metadata 与其他碎片。

### LM54-C03
调度器在 iteration 边界移出完成请求、加入新请求，减少固定 batch 的空槽并形成更大有效矩阵。但请求的 $y_{t+1}$ 分布以已采出的 $y_t$ 为条件，计算图上仍有先后；跨请求并行不能让同一请求未知的未来 token 提前确定。

## D. 边界、反例与纠错

### LM54-D01
FlashAttention 可减少 attention 中间张量 IO，但 decode 下一步仍需历史 K/V；若不存就要重算前缀。容量表仍要包含 persistent KV，除非另用压缩、滑窗、重计算等明确策略。

### LM54-D02
峰值吞吐点可能处于高并发饱和区，queue 与 p99 TTFT/TBT 已不可接受。交互服务应比较同一 arrival/长度分布下满足 SLO 的 goodput、尾延迟和错误率；总 tokens/s 只是一个坐标。

### LM54-D03
该估算把所有请求都视为始终占满窗口，可能极度保守；也可能漏掉 beam、共享/复制、临时 speculative KV、碎片和抢占。应基于 prompt/output 长度与并发的 live-token 分布，乘结构公式，再加 allocator/workspace/权重安全余量并压测尾部。

## E. AI 迁移

### LM54-E01
请求 trace：arrival、queue、prefill start/end、逐 token timestamp、finish、prompt/output lengths、finish reason。Iteration trace：active IDs、prefill/decode token 数、batch shape、KV blocks 分配/释放/共享/抢占、kernel time、显存、scheduler decision。绑定 model/engine/hardware 版本。

### LM54-E02
固定模型、dtype、kernel、scheduler policy、prompt/output/arrival trace 与显存上限，只改 allocator；扫并发与长度离散度。报告可接纳请求、内部/外部碎片、KV 利用率、TTFT/TBT p50/p99、throughput/goodput、metadata/寻址开销和 OOM。

### LM54-E03
按当前 live KV、待入请求 prompt 与保守输出 reservation 估计增量 blocks；预留权重/workspace/碎片 safety margin。若加入后超过预算，则排队、降并发或显式拒绝；不要静默超售。用实际增长逐步修正 reservation，并对 beam/speculation 单独乘扩展因子。
