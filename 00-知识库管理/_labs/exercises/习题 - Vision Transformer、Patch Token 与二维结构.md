---
type: exercise
status: draft
area: [architecture, transformer, vision-transformer, patch-embedding]
topic: "[[Vision Transformer、Patch Token 与二维结构]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Vision Transformer、Patch Token 与二维结构]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - Vision Transformer、Patch Token 与二维结构

## A. 识别与复述

### ARCH-VIT-A01
写出 $H\times W\times C$ 图像经 $P\times P$ 非重叠 patchification 后的 $N$、patch matrix 与 embedding shapes。

### ARCH-VIT-A02
说明 patch linear projection 与 stride-$P$ convolution 的等价范围。

### ARCH-VIT-A03
列出 class token、mean pooling 与 dense grid readout 的差异。

## B. 手算与建模

### ARCH-VIT-B01
对 $224\times224\times3$ 图像、$P=16,d=768$，计算 $N$、含 class token 的 $T$ 与 patch projection 主参数量。

### ARCH-VIT-B02
若 $H,W$ 各翻倍、$P$ 不变，token 数和 attention pair 数各乘多少？

### ARCH-VIT-B03
对 $230\times224$ 图像和 $P=16$，分别说明 crop、pad、resize 三种合同的形状/信息影响。

## C. 推导与证明

### ARCH-VIT-C01
通过权重重排证明 patch projection 可由 kernel/stride 都为 $P$ 的卷积实现。

### ARCH-VIT-C02
推导 $P\to2P$ 时 patch token 数、attention pairs 与 projection 参数的变化。

### ARCH-VIT-C03
证明无 position、无 class-specific asymmetry 的 encoder 对 patch token 置换等变；mean pooling 后为何变为置换不变？

## D. 边界、反例与纠错

### ARCH-VIT-D01
反驳：“Patch embedding 用卷积实现，所以 ViT 与 CNN 具有相同归纳偏置。”

### ARCH-VIT-D02
构造一维 row-major 序号相邻但二维空间不相邻的 patch 对。

### ARCH-VIT-D03
说明为何把 learned absolute positions 直接截断/重复到新分辨率可能错位。

## E. AI 迁移

### ARCH-VIT-E01
为 patchify/unpatchify 写覆盖整除、padding、通道顺序与 batch 的测试。

### ARCH-VIT-E02
设计 patch size 扫描，联合报告细节任务质量、算力、显存与吞吐。

### ARCH-VIT-E03
为 ViT 与 CNN 的公平比较写 evidence card，保留数据规模、增强和预训练条件。

## 解答入口

[[解答 - Vision Transformer、Patch Token 与二维结构]]
