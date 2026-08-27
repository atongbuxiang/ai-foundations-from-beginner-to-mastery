---
type: exercise
status: draft
area: [architecture, attention, multi-head]
topic: "[[Multi-Head Attention、投影子空间与参数量]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Multi-Head Attention、投影子空间与参数量]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - Multi-Head Attention、投影子空间与参数量

## A. 识别与复述

### ARCH-MHA-A01
写出第 r 个 head 与最终 MHA 的公式。

### ARCH-MHA-A02
在标准 $hd_h=d_{model}$ 下说明增加 head 数对每头宽、主投影参数量和 score 元素数的影响。

### ARCH-MHA-A03
解释 packed projection 的 reshape 为何不等于 heads 共享投影。

## B. 手算与建模

### ARCH-MHA-B01
$d_{model}=512,h=8,d_k=d_v=64$，忽略 bias，计算 Q/K/V/O 参数量。

### ARCH-MHA-B02
固定 $d_{model}=768$，比较 12 heads 与 24 heads 的每头宽；若 $B=4,T=1024$，计算两者显式 score 元素数。

### ARCH-MHA-B03
$B=2,h=8,T_q=16,T_k=128,d_k=64,d_v=64$，列出 Q/K/V/S/H/concat/output shapes。

## C. 推导与证明

### ARCH-MHA-C01
推导标准 MHA 忽略 bias 的 $4d^2$ 参数量，并写出不满足等宽约定的一般式。

### ARCH-MHA-C02
在固定 $hd_k=d$ 下推导 score matmul 主阶 work 对 h 消去，而显式 score storage 仍随 h 线性增长。

### ARCH-MHA-C03
证明同步置换 head 顺序并相应置换 $W_O$ 输入块不改变函数。

## D. 边界、反例与纠错

### ARCH-MHA-D01
反驳：“更多 heads 一定严格增加参数量和表达力。”

### ARCH-MHA-D02
构造所有 heads 参数相同的功能冗余情形。

### ARCH-MHA-D03
解释为什么逐个可剪的 heads 不推出它们可同时全部剪掉。

## E. AI 迁移

### ARCH-MHA-E01
设计 head pruning curve 实验，区分 zeroing、结构删除、联合剪枝与微调。

### ARCH-MHA-E02
为 MHA 与 GQA 比较写参数、KV heads、cache、FLOP、quality 与 kernel 账本。

### ARCH-MHA-E03
设计跨 seed 的 head 专门化研究，处理 head permutation 不可辨识性。

## 解答入口

[[解答 - Multi-Head Attention、投影子空间与参数量]]
