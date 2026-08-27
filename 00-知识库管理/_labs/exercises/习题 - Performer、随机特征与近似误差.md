---
type: exercise
status: draft
area: [architecture, efficient-attention, performer, random-features]
topic: "[[Performer、随机特征与近似误差]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Performer、随机特征与近似误差]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - Performer、随机特征与近似误差

## A. 识别与复述

### ARCH-PERF-A01
把 softmax 的未归一化指数点积写成 kernel，并说明 attention 中还缺哪一步归一化。

### ARCH-PERF-A02
写出正高斯随机特征的单样本形式与 $m$ 个 feature 的 Monte Carlo 估计器。

### ARCH-PERF-A03
为什么“kernel estimator 无偏”不推出“normalized attention output 无偏”？

## B. 手算与建模

### ARCH-PERF-B01
在一维中令 $q=1,k=2,\omega=0$，计算单个正随机 feature 对 $e^{qk}$ 的估计值，并说明单样本不必接近期望。

### ARCH-PERF-B02
给定真实 $(N,D)=(6,3)$ 与扰动 $(\delta N,\delta D)=(0.3,-0.1)$，比较精确 ratio 变化和一阶近似。

### ARCH-PERF-B03
若 $m$ 从 64 增到 256，独立 Monte Carlo 标准误差在理想有限方差条件下约缩小多少？state/MAC 又约变化多少？

## C. 推导与证明

### ARCH-PERF-C01
用高斯矩母函数证明 $\mathbb E[e^{\omega^\top(q+k)-(\|q\|^2+\|k\|^2)/2}]=e^{q^\top k}$。

### ARCH-PERF-C02
对 $(N+\delta N)/(D+\delta D)$ 做一阶展开，推导 denominator 小时的误差放大项。

### ARCH-PERF-C03
证明共享同一组随机 features 能使全序列得到一个一致 kernel realization；说明每个 token 重新采样为何会改变模型与缓存语义。

## D. 边界、反例与纠错

### ARCH-PERF-D01
给出一个无偏 numerator/denominator estimator 的 ratio 有偏例子。

### ARCH-PERF-D02
解释为什么随机特征方差可能随 $\|q+k\|$ 快速增大；缩放与归一化如何影响问题？

### ARCH-PERF-D03
反驳：“增加随机 feature 数会单调提升训练后模型的任务性能。”

## E. AI 迁移

### ARCH-PERF-E01
设计 Performer 近似审计，报告 kernel、row normalization、attention output 与最终 logits 四层误差。

### ARCH-PERF-E02
写一个随机性可复现合同：训练、评估、checkpoint、distributed replicas 和 KV/state cache 各应怎样处理随机矩阵？

### ARCH-PERF-E03
设计 $m$ 的预算曲线，联合报告误差分位数、内存、吞吐与长序列任务质量。

## 解答入口

[[解答 - Performer、随机特征与近似误差]]
