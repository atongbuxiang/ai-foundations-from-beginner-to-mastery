---
type: exercise
status: draft
area: [architecture, transformer, shapes, parameters, compute]
topic: "[[Transformer 形状、参数量与 FLOPs 总账]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Transformer 形状、参数量与 FLOPs 总账]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - Transformer 形状、参数量与 FLOPs 总账

## A. 识别与复述

### ARCH-COST-A01
定义 $B,T,d,h,d_h,d_{ff},L,V$，并写出标准假设 $hd_h=d$。

### ARCH-COST-A02
区分参数量、MAC/FLOP、activation memory、KV cache 与 wall-clock。

### ARCH-COST-A03
说明训练、prefill 与 decode 为什么必须分账。

## B. 手算与建模

### ARCH-COST-B01
对 $d=768,d_{ff}=3072$，计算标准 MHA、普通 FFN 与标准 block 的主参数量。

### ARCH-COST-B02
对 $B=2,T=512,d=768,d_{ff}=3072$，分别写出投影、pairwise attention 与 FFN 的 forward MAC 数。

### ARCH-COST-B03
对 $V=50000,d=1024,L=24$ decoder-only，估算 tied 与 untied embedding/head 对总参数的差额。

## C. 推导与证明

### ARCH-COST-C01
从 Q/K/V/O shapes 推导标准 MHA 参数 $4d^2$，说明固定 $d$ 时为何不再乘 $h$。

### ARCH-COST-C02
推导 attention pair 项相对 projection 和 FFN 项的两个交叉长度。

### ARCH-COST-C03
推导 cross-attention 的 Q、K/V、O 与 pairwise MAC 账，并指出生成时可复用的项。

## D. 边界、反例与纠错

### ARCH-COST-D01
反驳：“Transformer 每层成本就是 $O(T^2d)$。”

### ARCH-COST-D02
解释 Flash-style attention 为什么可降低 materialized activation memory，却不改变 dense relation 的 all-pairs 数学定义。

### ARCH-COST-D03
构造少 FLOPs 但实际延迟更高的合理场景。

## E. AI 迁移

### ARCH-COST-E01
为一个真实模型建立参数—训练—prefill—decode—memory 五联成本卡。

### ARCH-COST-E02
设计 FLOP 公式与实测 profiler 的对账实验，处理 MAC 口径、padding 与 fused kernels。

### ARCH-COST-E03
比较 MHA、GQA 与 MQA 时，写出 K/V 参数与 cache 变化以及必须保持的质量/延迟控制。

## 解答入口

[[解答 - Transformer 形状、参数量与 FLOPs 总账]]
