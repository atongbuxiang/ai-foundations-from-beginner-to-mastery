---
type: exercise
status: draft
area: [architecture, long-context, position-interpolation, rope-scaling]
topic: "[[长度外推、位置插值与 RoPE 缩放]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - 长度外推、位置插值与 RoPE 缩放]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - 长度外推、位置插值与 RoPE 缩放

## A. 识别与复述

### ARCH-EXT-A01
区分直接外推、位置插值、统一 RoPE 缩放、逐频缩放与截断/重映射。

### ARCH-EXT-A02
解释“NTK-aware”作为历史名称与“得到 NTK 理论保证”之间的差别。

### ARCH-EXT-A03
长度扩展时为什么必须同时登记训练覆盖、位置变换、attention 可见域与微调协议？

## B. 手算与建模

### ARCH-EXT-B01
训练长度 $L_0=2048$，目标长度 $L_1=8192$。位置插值比例是多少？原位置 $m=6000$ 映射到哪里？

### ARCH-EXT-B02
单频相位为 $\phi=\omega m$。比较直接外推、统一缩放 $m/s$ 与截断 $\min(m,w)$ 在 $m>w$ 时的相位。

### ARCH-EXT-B03
对频率 $(1,0.1,0.01)$ 与逐频尺度 $(4,2,1)$，计算位置 $m=8$ 的新相位；指出局部与全局分辨率差异。

## C. 推导与证明

### ARCH-EXT-C01
证明位置插值 $m'=m/s$ 把 $[0,L_1)$ 映射回约 $[0,L_0)$；计算相邻测试 token 在训练坐标中的间距。

### ARCH-EXT-C02
从 RoPE 相对相位 $\omega_i(m-n)$ 推导逐频尺度 $s_i$ 如何改变每一通道的有效波长。

### ARCH-EXT-C03
把 ReRoPE 类局部保真重映射写成分段函数，分析连续性、远程分辨率与额外计算接口。

## D. 边界、反例与纠错

### ARCH-EXT-D01
反驳：“位置插值把所有测试坐标压回训练范围，所以无需长上下文微调或评测。”

### ARCH-EXT-D02
构造只在局部窗口任务上成功、却完全不使用远程信息的模型，说明其不能证明有效长上下文。

### ARCH-EXT-D03
解释改变 RoPE base 可能改善某长度档、同时损伤短程分辨率或其他任务的原因。

## E. AI 迁移

### ARCH-EXT-E01
设计一个至少包含直接外推、PI、统一缩放、逐频缩放和局部窗口基线的公平实验。

### ARCH-EXT-E02
为训练后 context extension 写 serving 迁移清单，覆盖 checkpoint、config、cache 与 batch packing。

### ARCH-EXT-E03
提出一种选择缩放超参数的协议，避免在最终测试集上反复调参造成信息泄露。

## 解答入口

[[解答 - 长度外推、位置插值与 RoPE 缩放]]
