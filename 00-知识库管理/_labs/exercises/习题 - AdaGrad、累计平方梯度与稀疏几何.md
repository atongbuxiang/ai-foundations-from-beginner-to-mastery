---
type: exercise
status: verified
area: [training, optimization, adaptive-optimization]
topic: "[[AdaGrad、累计平方梯度与稀疏几何]]"
solution: "[[解答 - AdaGrad、累计平方梯度与稀疏几何]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - AdaGrad、累计平方梯度与稀疏几何

> [!abstract] 训练目标
> 从累计平方梯度推出逐坐标度量，能手算轨迹、证明尺度性质，并判断稀疏梯度场景中“自适应”究竟意味着什么。

## A. 识别与复述

### TRN09-A01
写出 diagonal AdaGrad 的状态、方向和参数更新，并逐项说明 $G_{t,i}$、$\epsilon$ 与 $\eta$ 的角色和单位。

### TRN09-A02
为什么 AdaGrad 常被称为“数据依赖的几何”？这里的“几何”具体由哪个正定矩阵定义？

### TRN09-A03
区分“稀疏坐标获得较大有效学习率”与“稀疏模型一定训练得更好”两句话的逻辑强度。

## B. 手算与构造

### TRN09-B01
一维情形取 $\theta_0=2,\eta=1,\epsilon=0$，梯度依次为 $g_1=3,g_2=4$。计算 $G_1,G_2$、两步有效学习率与 $\theta_1,\theta_2$。

### TRN09-B02
二维梯度依次为 $(3,0),(0,4),(3,0)$，取 $\eta=1,\epsilon=0$。计算第三步更新前的累计器和第三步位移；解释两个坐标的历史如何分离。

### TRN09-B03
某 embedding 的两个坐标累计平方梯度为 $G=(100,1)$，当前梯度为 $(2,2)$，$\eta=0.1,\epsilon=0$。求更新并比较与 SGD 的方向。

## C. 推导与证明

### TRN09-C01
证明对 $H_t=\operatorname{diag}(\sqrt{G_t}+\epsilon)$，AdaGrad 更新是
$$\arg\min_\Delta\{g_t^\top\Delta+\tfrac1{2\eta}\Delta^\top H_t\Delta\}.$$

### TRN09-C02
设一维所有历史梯度同时乘正数 $c$ 且 $\epsilon=0$。证明 AdaGrad 的每一步方向不变；再说明只在时刻 $k$ 之后放大梯度为什么没有这个结论。

### TRN09-C03
证明若 $|g_t|=a>0$ 恒定，则第 $t$ 步位移绝对值为 $\eta/\sqrt t$，并判断总路程 $\sum_{t=1}^T\eta/\sqrt t$ 是否有界。

## D. 边界、反例与纠错

### TRN09-D01
反驳：“AdaGrad 的学习率会衰减到零，所以参数总会收敛。”给出只凭步长衰减不能推出参数收敛的理由或反例。

### TRN09-D02
构造一个梯度尺度在训练中途突然改变的例子，说明历史累计器可能让新阶段更新过小。

### TRN09-D03
为什么把 $G_t$ 重置为零不只是“改了超参数”，而是改变了优化器状态和后续轨迹？

## E. AI 迁移

### TRN09-E01
在词频长尾的 embedding 表中，怎样记录统计量才能检验“稀有 token 从 AdaGrad 获益”而不只看总体 loss？

### TRN09-E02
设计一次 AdaGrad 与 SGD 的公平比较，至少控制初始权重、batch 顺序、调参预算、停止规则与稀疏/稠密参数组。

### TRN09-E03
大模型训练中若 optimizer state 必须分片，估算 diagonal AdaGrad 对 $P$ 个参数的持久状态开销，并指出这个估算没有包括什么。

## 作答与复盘

每题记录 `independent / hinted / copied / blocked / careless`、用时与错误类型。完成独立尝试后打开 [[解答 - AdaGrad、累计平方梯度与稀疏几何]]。
