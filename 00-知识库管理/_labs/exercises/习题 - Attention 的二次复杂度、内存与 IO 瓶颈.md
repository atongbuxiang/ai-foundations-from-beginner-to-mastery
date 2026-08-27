---
type: exercise
status: draft
area: [architecture, efficient-attention, complexity, systems]
topic: "[[Attention 的二次复杂度、内存与 IO 瓶颈]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Attention 的二次复杂度、内存与 IO 瓶颈]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - Attention 的二次复杂度、内存与 IO 瓶颈

## A. 识别与复述

### ARCH-COST-A01
区分训练、prefill 与 autoregressive decode，并说明为什么三者不能共用一句“Attention 是 $O(n^2)$”作为完整成本结论。

### ARCH-COST-A02
分别说明 FLOPs/MACs、峰值显存、HBM 流量、KV-cache payload 与 wall-clock latency 衡量什么。

### ARCH-COST-A03
写出 dense MHA 单层 QKVO、$QK^\top+AV$ 与两层 FFN 的主 MAC 项。

## B. 手算与建模

### ARCH-COST-B01
令 $B=2,n=2048,d=1024,d_{ff}=4096$。按主项计算单层 QKVO、pairwise attention 与 FFN 的 MAC 数，并判断哪个最大。

### ARCH-COST-B02
令 $L=32,B=1,T=8192,h_{kv}=8,d_h=128,s=2$ bytes。只计 K/V payload，计算 KV cache 字节数与 GiB 数。

### ARCH-COST-B03
忽略常数，比较 quadratic 方法 $an^2$ 与 linear 方法 $bn$。推导 crossover 长度，并解释为什么渐近阶本身不能给出实际 crossover。

## C. 推导与证明

### ARCH-COST-C01
证明 full causal decoding 若第 $t$ 步读取全部历史 K/V，则跨 $N$ 个生成步的历史读取标量数仍为 $\Theta(N^2h_{kv}d_h)$。

### ARCH-COST-C02
从矩阵 shape 推导 prefill 中 score tensor 的标量数 $Bh_qn^2$；再解释 FlashAttention 为何能减少其中间存储却不改变 dense pairwise 算术阶。

### ARCH-COST-C03
给出一个简化 roofline 判据：若算术强度 $I=F/Q$，峰值算力为 $P$、内存带宽为 $W$，推导性能上界并给出 compute-bound 与 bandwidth-bound 的分界。

## D. 边界、反例与纠错

### ARCH-COST-D01
反驳：“一个方法 FLOPs 更少，所以训练一定更快、decode 也一定更快。”

### ARCH-COST-D02
构造一个短序列区间，使 $O(n)$ 方法因固定开销大而慢于 $O(n^2)$ 方法。

### ARCH-COST-D03
解释为何只报告“显存下降 50%”不足以判断优化来自 activation、optimizer state、参数、allocator 还是 KV cache。

## E. AI 迁移

### ARCH-COST-E01
为一个 LLM serving benchmark 写出最小实验矩阵，至少覆盖 batch、prompt length、generated length、dtype、并发和硬件。

### ARCH-COST-E02
设计一个实验，分别定位 prefill compute 瓶颈与 decode bandwidth 瓶颈，并列出需要记录的至少六个指标。

### ARCH-COST-E03
给出评审“高效 Attention”论文时的成本总账模板，要求同时记录改变的数学对象、实现对象、误差对象与质量协议。

## 解答入口

[[解答 - Attention 的二次复杂度、内存与 IO 瓶颈]]
