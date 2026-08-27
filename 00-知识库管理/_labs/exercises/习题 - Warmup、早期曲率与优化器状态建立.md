---
type: exercise
status: verified
area: [training, optimization, warmup, stability]
topic: "[[Warmup、早期曲率与优化器状态建立]]"
solution: "[[解答 - Warmup、早期曲率与优化器状态建立]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Warmup、早期曲率与优化器状态建立

> [!abstract] 训练目标
> 把 warmup 写成精确时钟上的控制函数，并能区分早期曲率、optimizer state、相对更新、噪声、数值范围和架构放大六类机制，而不是用一个故事解释所有成功。

## A. 识别与复述

### TRN34-A01
给出 linear warmup 的完整合同：起点、终点、长度、端点约定和时钟。为什么“warmup 2000 steps”仍不充分？

### TRN34-A02
列出 warmup 可能缓解的六类机制，并为每类写一个能把它与其他机制区分开的遥测量。

### TRN34-A03
区分“减少 early LR”“重置/建立 optimizer state”“避免 mixed-precision overflow”。三者分别作用在训练链的哪一段？

## B. 手算与构造

### TRN34-B01
一维二次目标 $L(\theta)=50\theta^2/2$，peak LR 为 $0.05$，前 5 个成功 update 线性从 0 增长。列出每步 LR，并判断无 warmup 与 warmup 各步是否满足 $0<\eta<2/50$。

### TRN34-B02
Adam 取 $\beta_1=0.9,\beta_2=0.99$，梯度恒为 $g=2$。计算前两步未校正与偏差校正后的 $m,v,m/\sqrt v$；说明 warmup 与 bias correction 不能互相替代。

### TRN34-B03
训练每次尝试 step 有 20% 概率 overflow 并跳过 optimizer update。若 scheduler 按尝试 step 走 100 步 warmup，求第 100 次尝试时期望成功 update 数；与 success-step clock 比较。

## C. 推导与证明

### TRN34-C01
对时变二次曲率 $\lambda_t$ 推导 SGD 一步稳定条件。说明 linear warmup 能保证稳定所需的充分条件，以及为何未知 $\lambda_t$ 时它不是证明。

### TRN34-C02
展开 EMA 二阶矩 $v_t=(1-\beta_2)\sum_{k=1}^t\beta_2^{t-k}g_k^2$，推导恒定梯度下偏差修正，并解释早期非平稳梯度为何仍会留下状态滞后。

### TRN34-C03
设参数初始范数很小，方向范数近似常数。推导 linear warmup 下累计相对位移的上界，并说明它与单步稳定条件不是同一概念。

## D. 边界、反例与纠错

### TRN34-D01
构造一个 warmup 无法修复的失败：NaN 在乘 LR 之前产生。写出最短因果链。

### TRN34-D02
反驳“有 warmup 就说明早期 Hessian 更尖”。给出至少两个同样能产生收益的替代机制和相应干预实验。

### TRN34-D03
为什么只比较“有/无 warmup”且同时改变总训练步数、peak LR 或 decay 起点，不能识别 warmup 主效应？

## E. AI 迁移

### TRN34-E01
为大型语言模型设计 warmup 机制矩阵：六个假说各给 mediator、干预、预测结果与反证信号。

### TRN34-E02
设计 success-update、token 和 wall-clock 三种 warmup 时钟的对照实验；明确数据量、compute 与失败 step 如何入账。

### TRN34-E03
写一份训练事故记录：前 200 step loss spike、clip rate 与 overflow 同时上升。给出诊断顺序，不允许直接把根因归为“LR 太大”。

## 作答与复盘

先画出“假说—中介量—干预—反证”四列矩阵，再查看 [[解答 - Warmup、早期曲率与优化器状态建立]]。
