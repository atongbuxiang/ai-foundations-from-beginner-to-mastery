---
type: exercise
status: draft
area: [architecture, efficient-attention, kv-cache, gqa, mqa]
topic: "[[KV Cache、MHA、MQA 与 GQA]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - KV Cache、MHA、MQA 与 GQA]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - KV Cache、MHA、MQA 与 GQA

## A. 识别与复述

### ARCH-CACHE-A01
解释 autoregressive decoding 为什么缓存 K/V 而通常不缓存历史 Q。

### ARCH-CACHE-A02
用 $h_q,h_{kv},d_h$ 统一定义 MHA、GQA 与 MQA。

### ARCH-CACHE-A03
写出 query head 到 KV head 的 group mapping，并说明需要什么整除合同。

## B. 手算与建模

### ARCH-CACHE-B01
令 $h_q=32,h_{kv}=8$。列出 query heads 0–11 对应的 KV head，并给出 group size。

### ARCH-CACHE-B02
令 $L=40,B=8,T=4096,d_h=128,s=2$。分别计算 MHA($h_{kv}=32$)、GQA($8$)、MQA($1$) 的 K/V payload GiB。

### ARCH-CACHE-B03
若 K/V projection 从 MHA 改为 GQA，忽略 bias，推导 W_K/W_V 参数量变化；Q/O 是否必然变化？

## C. 推导与证明

### ARCH-CACHE-C01
证明只要 cached K/V、position IDs、mask 与 head mapping 一致，逐 token cached decode 与 full causal attention 在实数算术中逐步等价。

### ARCH-CACHE-C02
推导每层 KV cache 标量数 $2BTh_{kv}d_h$，并解释为什么节省比例 $h_{kv}/h_q$ 不等于 latency 比例。

### ARCH-CACHE-C03
比较不缓存与缓存时生成 $N$ 个 token 的 K/V projection 重算量；明确 prompt/history 长度如何进入。

## D. 边界、反例与纠错

### ARCH-CACHE-D01
构造 cache offset 从 0 重启导致 RoPE full/cache 不等价、但 tensor shape 全部正确的例子。

### ARCH-CACHE-D02
反驳：“MQA 的 cache 是 MHA 的 $1/h_q$，所以吞吐一定提升 $h_q$ 倍。”

### ARCH-CACHE-D03
解释 allocator page、padding、quantization scale、tensor parallel replication 为何使实际显存不同于 payload 公式。

## E. AI 迁移

### ARCH-CACHE-E01
写一个 MHA/GQA/MQA reference test，覆盖 full forward、prefill+decode、chunked prefill 与不同 batch cache length。

### ARCH-CACHE-E02
设计 GQA group 数的公平消融，联合测质量、cache、bandwidth、latency 与参数量。

### ARCH-CACHE-E03
给出 production KV-cache 接口合同，覆盖 layout、dtype、offset、padding、eviction、serialization 与版本兼容。

## 解答入口

[[解答 - KV Cache、MHA、MQA 与 GQA]]
