---
type: exercise
status: draft
area: [learning-theory/scale-sensitive-dimension, regression/generalization]
topic: "[[Fat-Shattering、回归与 Lipschitz 风险]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[实值函数类、伪维与阈值化]]", "[[覆盖数、Metric Entropy 与 Chaining 入口]]"]
related: ["[[解答 - Fat-Shattering、回归与 Lipschitz 风险]]", "[[分类间隔、Margin Bound 与 SVM 接口]]"]
solution: "[[解答 - Fat-Shattering、回归与 Lipschitz 风险]]"
created: 2026-08-23
updated: 2026-08-23
---

# 习题 - Fat-Shattering、回归与 Lipschitz 风险

> [!abstract] 训练目标
> 能写出 fat-shattering 的完整量词，计算简单类的 scale profile，推导线性球 dimension bound，并把尺度容量通过 entropy、Rademacher 与 loss contract 连接到回归风险。

## A. 识别与复述

### LT-FAT-A01

按正文 convention 写出 $d$ 点被 $\gamma$-fat-shattered 的完整量词与不等式。

### LT-FAT-A02

区分 VC dimension、pseudo-dimension 与 fat-shattering profile。

### LT-FAT-A03

陈述 fat dimension 的尺度单调性、class 单调性、amplitude scaling 与 translation invariance。

## B. 手算与数值判断

### LT-FAT-B01

对常数类 $\{f_c\equiv c:c\in[-2,2]\}$，计算 $\gamma=1$ 与 $\gamma=3$ 时的 fat dimension。

### LT-FAT-B02

线性 $\ell_2$ 球有 $B=3$、输入 radius $R=2$、$\gamma=0.5$、ambient dimension $p=100$。计算正文 upper bound。

### LT-FAT-B03

若 $\operatorname{fat}_{0.5}(\mathcal F)=25$，输出整体乘 $a=4$。写出新类在尺度 $\gamma=2$ 的 fat dimension。

## C. 推导与证明

### LT-FAT-C01

证明尺度单调性、amplitude scaling 与固定函数 translation invariance。

### LT-FAT-C02

从 fat witnesses 推导该样本上的 empirical Rademacher complexity 至少为 $\gamma$。

### LT-FAT-C03

将 C02 与线性球 $BR/\sqrt d$ upper bound 合成，推导 $\operatorname{fat}_\gamma\le(BR/\gamma)^2$。

## D. 边界、反例与纠错

### LT-FAT-D01

解释为何 thresholds 若允许随 sign pattern 改变，definition 会退化；用单函数类说明问题。

### LT-FAT-D02

反驳“连续参数类必有无限 fat dimension”，使用常数函数区间和 resolution 说明。

### LT-FAT-D03

说明为什么 squared loss 不能从 fat dimension 直接接一个全局 $L=1$ contraction；给出 bounded-range 修正。

## E. AI 迁移

### LT-FAT-E01

对 frozen embedding 上的 linear regression head，写出从 $B,R,\gamma$ 到 fat/cover/risk 的完整证书链与缺失常数。

### LT-FAT-E02

reward model 只通过 pairwise preferences 训练。说明应研究 difference class，而非绝对 score class，并写出对应函数。

### LT-FAT-E03

分析 diffusion score regression 为什么需要 vector-valued capacity；至少列出 output norm、time/noise sampling、target tail 与 squared-loss range 四项。
