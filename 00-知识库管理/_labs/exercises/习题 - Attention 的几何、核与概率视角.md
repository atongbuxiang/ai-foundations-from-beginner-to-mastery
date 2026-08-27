---
type: exercise
status: draft
area: [architecture, attention, kernels, probability]
topic: "[[Attention 的几何、核与概率视角]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Attention 的几何、核与概率视角]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - Attention 的几何、核与概率视角

## A. 识别与复述

### ARCH-GKP-A01
写出 dot product 的 norm–angle 分解，并说明 cosine attention 删除哪条通道。

### ARCH-GKP-A02
把一行 normalized attention 写成 categorical distribution 与 value 条件期望。

### ARCH-GKP-A03
区分 PSD kernel feature map 与一般 $\phi(q)^T\varphi(k)$ affinity factorization。

## B. 手算与建模

### ARCH-GKP-B01
对权重 $(1/2,1/4,1/8,1/8)$ 计算 entropy、effective support $e^H$ 与 collision concentration。

### ARCH-GKP-B02
两个 key 与 q 的夹角相同，但 norms 分别为 1 和 3。若 q norm 为 2，比较 dot-product score 与 cosine score。

### ARCH-GKP-B03
给定 $\phi(q)=(1,2)$，$\varphi(k_1)=(2,0)$，$\varphi(k_2)=(1,1)$，values 为 3、7，计算 normalized linear attention 输出。

## C. 推导与证明

### ARCH-GKP-C01
用 tensor powers 证明 $e^{q^Tk}$ 可写为无限维 inner product。

### ARCH-GKP-C02
推导 linear attention 的结合律重排，并给出 $T,r,d_v$ 的主要时间/状态量。

### ARCH-GKP-C03
推导 normalized output 的 numerator/denominator 误差分解，并指出需要的下界条件。

## D. 边界、反例与纠错

### ARCH-GKP-D01
构造 $\phi\ne\varphi$ 导致非对称 affinity，说明它不自动是 PSD Gram kernel。

### ARCH-GKP-D02
构造小 denominator 使很小的 denominator 误差造成较大 normalized output 误差。

### ARCH-GKP-D03
反驳：“attention 越集中，预测一定越准确且解释越忠实。”

## E. AI 迁移

### ARCH-GKP-E01
设计 exact softmax 与 random-feature attention 的 kernel/output/cost 三层实验。

### ARCH-GKP-E02
设计长度可比的 attention concentration 报告，处理可见位置数变化。

### ARCH-GKP-E03
为 causal linear attention 写 prefix state、reset/segment、denominator 与 finite-precision 审计。

## 解答入口

[[解答 - Attention 的几何、核与概率视角]]
