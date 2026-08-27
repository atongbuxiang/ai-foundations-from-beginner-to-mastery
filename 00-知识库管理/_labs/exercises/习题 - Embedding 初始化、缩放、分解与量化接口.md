---
type: exercise
status: draft
area: [neural-networks/embedding-output, embedding-initialization, factorization, quantization]
topic: "[[Embedding 初始化、缩放、分解与量化接口]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Embedding 初始化、缩放、分解与量化接口]]"
created: 2026-08-24
updated: 2026-08-24
---
# 习题 - Embedding 初始化、缩放、分解与量化接口

## A

### NN-ECQ-A01
若 $E_{ij}$ 独立、零均值、方差 $\sigma_E^2$，推导 $\mathbb E\|e_i\|_2^2$。若希望 row RMS norm 为 $O(1)$，$\sigma_E^2$ 应如何随 $d$ 缩放？

### NN-ECQ-A02
区分参数初始化 scale、forward 时固定乘法 scale 与 LayerNorm/RMSNorm。为什么三者不能仅因都改变数值尺度而互换？

### NN-ECQ-A03
分别说明低秩分解、frequency-adaptive dimension 与量化改变的是 rank/capacity、token-group capacity 还是数值表示误差。

## B

### NN-ECQ-B01
取 $V=50{,}000,d=1024,r=128$。计算 full 与 $E=AB$ 的参数量、FP16 参数本体字节、压缩倍数与每 token 额外 dense MAC。

### NN-ECQ-B02
同一 full table 使用 INT4 raw codes。计算原始 codes 字节及相对 FP16 比例。若每 64 个 weights 额外存一个 FP16 scale，求 metadata 和总字节。

### NN-ECQ-B03
一个无 clipping 的 per-row affine quantizer 取 $d=1024,s=0.02$，且 $\|h\|_2=10$。给出 row $L_2$ error 与 output-logit error 的最坏上界。

## C

### NN-ECQ-C01
对单 token $q_i$，令 $a=A^\mathsf Tq_i$、$e=B^\mathsf Ta$。从微分推导 $\nabla_A L$ 与 $\nabla_B L$，并指出哪一支是 row sparse。

### NN-ECQ-C02
证明 $(AR)(R^{-1}B)=AB$ 的 gauge。说明病态 $R$ 为什么在函数不变时仍改变优化、正则化与有限精度。

### NN-ECQ-C03
从 truncated SVD 构造 balanced factors $A_0,B_0$，写出 reconstruction error。为什么它不保证 task loss 最优？

## D

### NN-ECQ-D01
模型推理权重为 INT4，却仍在训练中 OOM。建立包含 working weights、master weights、gradients、moments、scales 与 activations 的内存账。

### NN-ECQ-D02
direct-tied embedding 同时用于 row gather 与 output GEMM。设计测试检查量化后 Parameter/storage identity、kernel fallback、logit error 与实际内存，避免静默复制 dense output。

### NN-ECQ-D03
frequency-adaptive embedding 按旧语料分桶，部署域的 rare-but-critical tokens 频率上升。设计 drift 监控与重新分桶/升维策略。

## E

### NN-ECQ-E01
设计 full、rank-$r$、adaptive-dimension、INT8、INT4 五方案的 Pareto 实验；至少报告函数类、质量、稀有词、参数/状态、吞吐、延迟、通信与能耗。

### NN-ECQ-E02
反驳：“参数量缩小 8 倍，所以训练内存和推理延迟都会缩小 8 倍。”给出至少六本独立账。

### NN-ECQ-E03
给出 rare/special-token 安全门：在允许发布压缩模型前，如何用 row error、logit margin、分桶 NLL、generation regression 与回滚条件联合验收？
