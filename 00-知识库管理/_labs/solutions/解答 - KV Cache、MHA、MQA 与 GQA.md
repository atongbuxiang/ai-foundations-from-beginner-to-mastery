---
type: solution
status: draft
area: [architecture, efficient-attention, kv-cache, gqa, mqa]
topic: "[[KV Cache、MHA、MQA 与 GQA]]"
exercise: "[[习题 - KV Cache、MHA、MQA 与 GQA]]"
sources: ["[[S-2019-Shazeer-MQA]]", "[[S-2023-Ainslie-GQA]]", "[[S-2024-Su-10091-MHA-MQA-GQA-MLA]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - KV Cache、MHA、MQA 与 GQA

## A. 识别与复述

### ARCH-CACHE-A01
未来每个新 query 都要与历史 K/V 计算 score 和加权和，所以历史 K/V 可跨步复用；历史 Q 只在其自己的输出时使用，通常不会被未来 query 读取。缓存 K/V 避免每步对整个前缀重算 K/V projections。

### ARCH-CACHE-A02
所有方案有 $h_q$ 个 query heads、每头 $d_h$。MHA：$h_{kv}=h_q$；MQA：$h_{kv}=1$；GQA：$1<h_{kv}<h_q$ 且若干 query heads 共享一个 KV head。Residual width 与 Q head count 不必因 KV sharing 改变。

### ARCH-CACHE-A03
若连续分组且 $h_q$ 被 $h_{kv}$ 整除，group size $g=h_q/h_{kv}$，mapping 可写 $g(a)=\lfloor a h_{kv}/h_q\rfloor=\lfloor a/g\rfloor$。实现必须固定 head 排列与整除/映射规则。

## B. 手算与建模

### ARCH-CACHE-B01
group size 为 4。query 0–3 映到 KV0，4–7 到 KV1，8–11 到 KV2；所以 0–11 的映射为 $(0,0,0,0,1,1,1,1,2,2,2,2)$。

### ARCH-CACHE-B02
公式 $2LBTh_{kv}d_hs$。公共因子除 $h_{kv}$ 外为 $2\cdot40\cdot8\cdot4096\cdot128\cdot2=671{,}088{,}640$ bytes。MHA 乘 32 得 20 GiB；GQA 乘 8 得 5 GiB；MQA 乘 1 得 0.625 GiB。

### ARCH-CACHE-B03
MHA 的 $W_K,W_V$ 合计约 $2d(h_qd_h)$ 参数；GQA 为 $2d(h_{kv}d_h)$，比例 $h_{kv}/h_q$。$W_Q$ 和 $W_O$ 仍可保持 $d\times h_qd_h$ 与 $h_qd_h\times d$，不因定义强制改变。

## C. 推导与证明

### ARCH-CACHE-C01
归纳。Prefill 后 cache 与 full forward 的历史 K/V 相同。假设到 $t-1$ 相同，第 $t$ 步以同一参数、position ID 得同一新 K/V，append 后 cache 正是 full causal row 可见的 $K_{\le t},V_{\le t}$；同一 mask、head mapping 和 softmax 给相同输出。浮点归约次序可能只给容差等价。

### ARCH-CACHE-C02
每 token、每层有 K 和 V 两份，每份 $B h_{kv}d_h$ 标量，$T$ tokens 即 $2BTh_{kv}d_h$。相对 MHA payload 比例是 $h_{kv}/h_q$，但 latency 还含 Q/O/FFN 算术、launch、allocator、通信、batching 与 kernel efficiency，不能同比例缩放。

### ARCH-CACHE-C03
若不缓存，第 $t$ 步需为约 $T_0+t$ 个 tokens 重算 K/V projections，跨 $N$ 步为 $\Theta((NT_0+N^2)d h_{kv}d_h)$；缓存后只为每个新 token 算一次，为 $\Theta(Nd h_{kv}d_h)$，另加一次 prompt prefill。缓存消除 projection 重算，不消除 attention 读历史。

## D. 边界、反例与纠错

### ARCH-CACHE-D01
已有 positions 0–4，new token 在 full forward 应为 5；若 cached decode 把它标 0，RoPE key/query 与旧 cache 的相对位移全部错 5。K/V shape、head count 和 mask shape 都合法，但 logits 改变；用 full-vs-cache reference 才能捕获。

### ARCH-CACHE-D02
即使 payload 减 $h_q$ 倍，端到端仍有非 KV 工作；小 batch 可能 launch-bound，大 batch/模型可能受 FFN、Q/O 或通信限制，MQA kernel layout 也可能利用率不同。质量变化还可能要求更大模型。只能说理论 cache bytes/读流量的该分项缩小。

### ARCH-CACHE-D03
Paged cache 按页分配会有尾页浪费；batch padding/最大长度预留增大容量；量化需额外 scale/zero-point；tensor parallel 可能复制或重分片 KV；另有 metadata/alignment/fragmentation。因此 payload 是必要基线，不是 allocator 峰值。

## E. AI 迁移

### ARCH-CACHE-E01
小张量高精度 reference 显式 expand KV heads，比较 MHA/GQA/MQA full causal forward；再测一次 prefill+逐 token、不同 chunk prefill，batch 内不同 cache lengths/left padding。覆盖 RoPE offset、mask、dtype、serialization；比较 hidden/logits 并让错误 mapping/offset 负对照失败。

### ARCH-CACHE-E02
固定总参数/训练 token/数据和尽量一致的 Q/O/FFN，扫 $h_{kv}$；若参数差异不可避免则同时报告。多 seed 测 perplexity、长短任务；同硬件/kernel 测 payload/allocated bytes、HBM throughput、TTFT/ITL/throughput 与通信，给 quality–memory–latency Pareto。

### ARCH-CACHE-E03
合同写明层/head/order、[B,T,H,D] 等 layout、dtype/quant scale、global position/rope offset、padding/sequence lengths、append/chunk 语义、page/eviction 生命周期、beam/reorder、跨设备 ownership、序列化 schema/checkpoint version，以及 full/cache/round-trip 回归测试。
