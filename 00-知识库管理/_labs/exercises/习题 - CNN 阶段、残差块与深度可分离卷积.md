---
type: exercise
status: draft
area: [architecture, cnn]
topic: "[[CNN 阶段、残差块与深度可分离卷积]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - CNN 阶段、残差块与深度可分离卷积]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - CNN 阶段、残差块与深度可分离卷积

## A. 识别与复述
### ARCH-CNN-A01
Stage table 至少应有哪些列？
### ARCH-CNN-A02
何时 residual shortcut 需要 projection？
### ARCH-CNN-A03
区分 classic bottleneck 与 depthwise-separable block。

## B. 手算与建模
### ARCH-CNN-B01
计算 $56^2,64\to64$ 的 3×3 standard conv MACs；空间减半、通道双倍后的 3×3 $128\to128$ 是否相近？
### ARCH-CNN-B02
对 $C=64,K=3$ 计算 standard 与 depthwise+pointwise 参数比。
### ARCH-CNN-B03
设计 $C=64\to256$ 的 bottleneck，取 $C_b=64$，计算三层参数（无 bias）。

## C. 推导与证明
### ARCH-CNN-C01
推导 depthwise+pointwise effective kernel 的 factorization 限制。
### ARCH-CNN-C02
推导 width/resolution multiplier 对 standard conv MACs 的近似缩放。
### ARCH-CNN-C03
证明 residual addition 要求两支张量同 shape；列出可实现的 projection。

## D. 边界、反例与纠错
### ARCH-CNN-D01
构造 standard kernel 不能由单个 depthwise+pointwise layer 表示的 $2\to2$、2-tap 例子。
### ARCH-CNN-D02
反驳：“参数少十倍，模型文件、显存和延迟都少十倍。”
### ARCH-CNN-D03
为什么盲目每次下采样都把通道翻倍不保证最优？

## E. AI 迁移
### ARCH-CNN-E01
为移动端 backbone 写公平 benchmark 协议。
### ARCH-CNN-E02
给定 stage 表，如何定位 activation-memory hotspot？
### ARCH-CNN-E03
比较 CNN stem 与 ViT patch embedding 的局部 bias 和下采样边界。

## 解答入口
[[解答 - CNN 阶段、残差块与深度可分离卷积]]
