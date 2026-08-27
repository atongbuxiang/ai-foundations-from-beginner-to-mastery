---
type: exercise
status: verified
area: [language-models, inference, serving]
topic: "[[Prefill、Decode、KV Cache 与 Continuous Batching]]"
solution: "[[解答 - Prefill、Decode、KV Cache 与 Continuous Batching]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Prefill、Decode、KV Cache 与 Continuous Batching

## A. 识别与复述

### LM54-A01
区分 prefill 与 decode 的输入形状、并行性和主要延迟指标。

### LM54-A02
说明 KV cache 保存什么、节省什么、付出什么。

### LM54-A03
区分 FlashAttention 的 IO 优化与 PagedAttention 的 KV 管理。

## B. 手算与构造

### LM54-B01
模型有 32 层、8 个 KV heads、head dimension 128，KV 为 fp16。计算每 token KV bytes 与 4096 tokens 的近似容量。

### LM54-B02
Block 大小 16 tokens，请求长度分别为 17、32、47。求各自 block 数、总 block 数和最后块内部空位。

### LM54-B03
某请求 arrival=0 ms、prefill start=40、首 token=140，随后 token timestamps 为 180、235、295，完成 300。计算 TTFT、各 TBT 与 E2E。

## C. 推导与证明

### LM54-C01
从层、K/V、KV heads、head dimension 与 dtype 推导每 token KV 公式。

### LM54-C02
证明固定 block 大小 $P$ 时单请求最后块内部浪费小于 $P$ tokens。

### LM54-C03
解释 continuous batching 为何提高设备利用率，却不能消除单请求 decode 的因果依赖。

## D. 边界、反例与纠错

### LM54-D01
纠正“启用 FlashAttention 后可以不计 KV cache”。

### LM54-D02
反驳“峰值 tokens/s 更高，所以交互服务一定更好”。

### LM54-D03
审计只用 max context length 乘请求数估算 KV 的容量计划。

## E. AI 迁移

### LM54-E01
为在线引擎设计 per-request 与 per-iteration trace。

### LM54-E02
设计分页 KV 与连续数组 allocator 的公平对照。

### LM54-E03
给显存预算写 admission-control 规则。

独立完成后查看[[解答 - Prefill、Decode、KV Cache 与 Continuous Batching]]。
