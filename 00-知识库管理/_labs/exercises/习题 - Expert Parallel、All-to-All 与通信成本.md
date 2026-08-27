---
type: exercise
status: draft
area: [architecture, moe, distributed-systems]
topic: "[[Expert Parallel、All-to-All 与通信成本]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Expert Parallel、All-to-All 与通信成本]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - Expert Parallel、All-to-All 与通信成本

## A. 识别与复述

### ARCH-EP-A01
按顺序列出一次 Expert Parallel 前向的六个阶段。

### ARCH-EP-A02
区分 logical payload、physical link traffic 与 wall-clock latency。

### ARCH-EP-A03
说明 DP、TP、PP、EP、SP 分别切什么。

## B. 手算与建模

### ARCH-EP-B01
$T=8192,k=2,d=4096,s=2,r=.75$，计算前向 dispatch+combine 过网逻辑 payload。

### ARCH-EP-B02
$E=64,D=8$，专家均匀放置时求 experts/device；若每专家 1.5B 参数，算每设备专家参数量。

### ARCH-EP-B03
两次实现均发送 200 MiB：A 为 8 个大消息，B 为 1024 个小消息。用 $t\approx Q/B+N\ell$ 解释谁可能更慢。

## C. 推导与证明

### ARCH-EP-C01
从 assignment 数推导 $Q_{fwd}\approx2rTkds$。

### ARCH-EP-C02
证明同步 step time 受最忙 rank 下界控制，而非只受平均 load 控制。

### ARCH-EP-C03
给出计算—通信完全串行与理想完全重叠的时间上下界。

## D. 边界、反例与纠错

### ARCH-EP-D01
反驳：“All-to-All bytes 下降 20%，端到端延迟就下降 20%。”

### ARCH-EP-D02
说明 dropless local kernel 为什么不消除网络通信或负载偏斜。

### ARCH-EP-D03
构造平均负载相同、最大负载不同的两个分配，解释尾延迟差异。

## E. AI 迁移

### ARCH-EP-E01
设计 EP benchmark 的最小 sweep 与指标。

### ARCH-EP-E02
设计验证 expert placement 对跨节点流量影响的实验。

### ARCH-EP-E03
为 profiler trace 写一个通信瓶颈诊断决策树。

## 解答入口

[[解答 - Expert Parallel、All-to-All 与通信成本]]

