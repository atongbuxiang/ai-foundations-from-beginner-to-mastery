---
type: exercise
status: draft
area: [architecture, state-space-models, hippo, s4]
topic: "[[HiPPO、S4 与结构化长记忆]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - HiPPO、S4 与结构化长记忆]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - HiPPO、S4 与结构化长记忆

## A. 识别与复述

### ARCH-HIPPO-A01
用 measure、basis、coefficients 和 projection reconstruction 定义 HiPPO 的记忆目标。

### ARCH-HIPPO-A02
解释“投影最优”相对于哪些对象，并列出两个不能外推的结论。

### ARCH-HIPPO-A03
概述从 HiPPO matrix 到 S4 长卷积核的五步计算链。

## B. 手算与建模

### ARCH-HIPPO-B01
在 $[-1,1]$ 均匀概率测度下取 $g_0=1,g_1=\sqrt3x$。对 $u(x)=2+x$ 计算 $c_0,c_1$ 并重构。

### ARCH-HIPPO-B02
给定离散标量 $\bar A=0.8,\bar B=1,C=2$，求前四个 SSM kernel coefficients 和生成函数。

### ARCH-HIPPO-B03
对 $M=\operatorname{diag}(2,3)$、$u=v=(1,1)^T$，用 Woodbury/Sherman–Morrison 求 $(M+uv^T)^{-1}$。

## C. 推导与证明

### ARCH-HIPPO-C01
证明 orthogonal projection error 与子空间任意扰动正交，并推出最佳近似。

### ARCH-HIPPO-C02
说明对 time-varying coefficient integral 求导为何同时产生边界输入项与 basis/measure 变化项。

### ARCH-HIPPO-C03
从 DPLR $A=\Lambda-PQ^*$ 说明 Woodbury 如何把 resolvent 约化为 diagonal inverse 与低秩系统。

## D. 边界、反例与纠错

### ARCH-HIPPO-D01
构造改变 measure 后同一常数/线性 basis 投影系数发生变化的例子。

### ARCH-HIPPO-D02
反驳：“HiPPO 的 projection optimality 证明 S4 在任意任务上最优。”

### ARCH-HIPPO-D03
解释为什么裸 SSM core 线性不意味着完整 S4 网络线性。

## E. AI 迁移

### ARCH-HIPPO-E01
为 HiPPO/S4 写一份 continuum–discretization–kernel–task 四层误差账。

### ARCH-HIPPO-E02
设计 S4 复现实验，分数学等价、数值精度、硬件速度和任务质量。

### ARCH-HIPPO-E03
把科学空间 SSM 四篇映射到本节的 I/T/E/H/O 证据层，并说明引用边界。

## 解答入口

[[解答 - HiPPO、S4 与结构化长记忆]]

