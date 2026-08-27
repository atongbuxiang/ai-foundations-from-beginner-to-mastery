---
type: exercise
status: draft
area: [architecture, moe, loss-free, assignment]
topic: "[[Loss-Free 路由、偏置更新与分配视角]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Loss-Free 路由、偏置更新与分配视角]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - Loss-Free 路由、偏置更新与分配视角

## A. 识别与复述

### ARCH-LFREE-A01
给出“loss-free”的精确定义，并指出它不排除哪些训练干预。

### ARCH-LFREE-A02
说明为何 selection score 可用 $s_i+b_i$，而 mixing weight 仍只用 $s_i$。

### ARCH-LFREE-A03
写出容量约束 assignment 的目标与行列约束。

## B. 手算与建模

### ARCH-LFREE-B01
目标 $[4,4]$、负载 $[6,2]$、$b=[0,0]$、$\eta=.1$，做一次符号反馈更新。

### ARCH-LFREE-B02
对 $s=[.55,.50]$ 使用上一题 bias，判断 Top-1 专家；计算不加 bias 的结果。

### ARCH-LFREE-B03
给定 score 矩阵 $S=\begin{bmatrix}9&7&2\\8&6&5\\4&9&7\\3&8&9\end{bmatrix}$，三个专家容量均为 2，构造一个可行 Top-1 assignment 并算总 score。

## C. 推导与证明

### ARCH-LFREE-C01
从容量约束 LP 的拉格朗日函数推导专家 dual price 如何进入调整后 score。

### ARCH-LFREE-C02
说明 threshold $A_{ti}=1[s_{ti}>\beta_i]$ 如何让每 token 激活数动态变化。

### ARCH-LFREE-C03
分析比例反馈 $b^{r+1}=b^r-\eta e^r$ 的一步方向，并说明为何仅凭该式不能证明闭环收敛。

## D. 边界、反例与纠错

### ARCH-LFREE-D01
反驳：“bias 不进入 mixing weight，所以不改变模型输出。”

### ARCH-LFREE-D02
构造过大 $\eta$ 导致两个专家负载振荡的例子。

### ARCH-LFREE-D03
解释 stale statistics 与数据漂移如何破坏反馈效果。

## E. AI 迁移

### ARCH-LFREE-E01
设计 aux-loss 与 loss-free 的公平对照。

### ARCH-LFREE-E02
设计一个 quantile approximation 误差测试。

### ARCH-LFREE-E03
为在线路由控制写出稳定性监控与回退机制。

## 解答入口

[[解答 - Loss-Free 路由、偏置更新与分配视角]]
