---
type: exercise
status: verified
area: [training, scaling-laws, emergence]
topic: "[[Broken Scaling、涌现表象与优化架构数据分解]]"
solution: "[[解答 - Broken Scaling、涌现表象与优化架构数据分解]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Broken Scaling、涌现表象与优化架构数据分解

> [!abstract] 训练目标
> 识别 kink 与“涌现”的竞争解释，用连续底层能力、指标变换、有限样本和训练缺口构造可检验诊断。

## A. 识别与复述

### TRN55-A01
定义 local scaling exponent。它比一条全局拟合直线多提供什么诊断信息？

### TRN55-A02
列出至少六种表观 broken scaling 的来源，并把它们分成测量、统计、优化、数据、架构与真实函数形状。

### TRN55-A03
区分底层连续能力、离散 benchmark 指标与“机制突然出现”。为什么三者不能由同一张 accuracy 图直接等同？

## B. 手算与构造

### TRN55-B01
若每一步正确概率由 $p=0.70$ 平滑升到 $0.80$，任务要求连续 $m=10$ 步全对，计算 exact-match 概率的变化倍数。

### TRN55-B02
真实成功率 $p=0.01$，评测样本数 $n=100$。计算观察到零次成功的概率。若 $n=1000$，该概率约为多少？

### TRN55-B03
设 $L(x)=x^{-0.3}(1+(x/x_b)^4)^{-0.1}$。求 $x\ll x_b$ 与 $x\gg x_b$ 的渐近幂指数。

## C. 推导与证明

### TRN55-C01
若观测指标 $M(x)=g(p(x))$，推导其 log-slope 与 $g'(p)$、$p'(x)$ 的关系，并说明 threshold/ceiling 如何放大或压平变化。

### TRN55-C02
对 exact match $M=p^m$ 推导相对弹性 $d\log M/d\log p=m$。它如何解释长链任务的陡峭表象？

### TRN55-C03
写出含优化、架构、数据主效应及两两交互的 gap decomposition。说明只做单因素升级为何不能识别交互项。

## D. 边界、反例与纠错

### TRN55-D01
反驳：“所有涌现能力都只是指标幻觉。”什么证据才可能支持真实机制或算法转变？

### TRN55-D02
反驳：“分段幂律拟合优于单幂律，所以 breakpoint 是真实相变。”至少讨论参数数目、选择偏差、held-out 与替代族。

### TRN55-D03
为什么“优化—架构—数据三重奏”是有用的解释坐标，却不是精确可加的普遍定理？

## E. AI 迁移

### TRN55-E01
为一个声称涌现的 benchmark 设计指标审计：至少包括连续 surrogate、样本量、置信区间、阈值和多重比较。

### TRN55-E02
设计 $2\times2\times2$ 的 optimizer–architecture–data 干预矩阵，并说明怎样估计主效应与交互。

### TRN55-E03
把“模型在 10B 参数处突然学会推理”改写成证据边界明确、包含竞争解释的研究结论。

## 作答与复盘

先问“是哪一层突然：潜变量、指标、采样还是机制？”，再查看 [[解答 - Broken Scaling、涌现表象与优化架构数据分解]]。
