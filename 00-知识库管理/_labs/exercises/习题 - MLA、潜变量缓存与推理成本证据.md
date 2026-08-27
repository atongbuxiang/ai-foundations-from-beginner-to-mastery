---
type: exercise
status: draft
area: [architecture, efficient-attention, mla, latent-cache]
topic: "[[MLA、潜变量缓存与推理成本证据]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - MLA、潜变量缓存与推理成本证据]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - MLA、潜变量缓存与推理成本证据

## A. 识别与复述

### ARCH-MLA-A01
说明 Linformer 型 sequence-axis compression 与 MLA per-token feature-axis latent compression 的根本区别。

### ARCH-MLA-A02
写出 MLA 的联合 KV latent、展开 K/V 与 query projection 的抽象 shape。

### ARCH-MLA-A03
为什么 RoPE 通常需要单独的位置 key/query 支路，不能无条件吸收到 content projection？

## B. 手算与建模

### ARCH-MLA-B01
令 $h_q=128,d_h=128,d_c=512,d_R=64$。比较 MHA 与 MLA 每 token 每层缓存标量数及比例。

### ARCH-MLA-B02
给定 $q=xW_Q,c=yW_D,k=cW_{UK}$，把 $q^\top k$ 重写为只与 latent $c$ 点积的形式，并给出吸收后 query shape。

### ARCH-MLA-B03
若 cache 使用 BF16，而吸收前后矩阵乘法顺序不同，列出至少三种可能产生数值差异的来源。

## C. 推导与证明

### ARCH-MLA-C01
证明线性 content key projection 可吸收到 query：$q^\top(W_{UK}c)=(W_{UK}^\top q)^\top c$；对 value/output 链写出相应结合律重排。

### ARCH-MLA-C02
推导 MLA payload 比例 $(d_c+d_R)/(2h_qd_h)$，并写明它成立所忽略的系统项。

### ARCH-MLA-C03
给出一个带非线性或 position-dependent 变换的反例，使 projection absorption 不再成立。

## D. 边界、反例与纠错

### ARCH-MLA-D01
反驳：“MLA cache 维度更小，所以任何配置和硬件上 decode 都更快。”

### ARCH-MLA-D02
解释为什么有限规模消融只能支持特定模型族内的经验排序，不能证明 MLA 全局最优。

### ARCH-MLA-D03
构造 $d_c+d_R\ge 2h_{kv}d_h$ 的 GQA 配置，说明 MLA 相对 cache 优势不是定义上必然。

## E. AI 迁移

### ARCH-MLA-E01
写一个 expanded-training form 与 absorbed-decode form 的数值等价测试，覆盖 RoPE 支路与低精度容差。

### ARCH-MLA-E02
设计 MLA/GQA 公平比较，明确参数匹配、训练 token、head dimension、cache dtype、kernel maturity 与 serving load。

### ARCH-MLA-E03
建立 MLA 证据表，把代数恒等式、整模型系统报告、消融、理论解释和开放工程权衡分别标为 I/T/E/H/O。

## 解答入口

[[解答 - MLA、潜变量缓存与推理成本证据]]
