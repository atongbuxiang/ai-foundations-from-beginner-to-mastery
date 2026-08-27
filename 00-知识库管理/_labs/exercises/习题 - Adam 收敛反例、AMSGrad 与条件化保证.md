---
type: exercise
status: verified
area: [training, optimization, online-learning]
topic: "[[Adam 收敛反例、AMSGrad 与条件化保证]]"
solution: "[[解答 - Adam 收敛反例、AMSGrad 与条件化保证]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Adam 收敛反例、AMSGrad 与条件化保证

> [!abstract] 训练目标
> 能复原经典反例的目标与最优点，解释 Adam 的遗忘为何破坏证明，并准确陈述 AMSGrad 修补了什么、没有保证什么。

## A. 识别与复述

### TRN13-A01
写出三周期线性损失 $f_t$：第一步斜率 $C$、其余两步斜率 $-1$，定义域 $[-1,1]$。当 $C>2$ 时最佳固定 comparator 是谁？

### TRN13-A02
Adam 反例针对的是哪种理论声明？它是否等价于“Adam 在所有深度学习任务都失败”？

### TRN13-A03
写出 AMSGrad 的 $\tilde v_t$ 与 $\hat v_t^{\max}$ 更新，指出其关键单调性。

## B. 手算与构造

### TRN13-B01
取 $C=4$。计算一个三步周期在固定 $x$ 上的累计损失，并找出 $[-1,1]$ 上的最优 $x$。

### TRN13-B02
设 $\beta_1=0,\beta_2=0.2,v_0=0$，梯度为 $4,-1,-1$。计算 Adam 的 $v_1,v_2,v_3$ 与无 epsilon 的归一化梯度大小。

### TRN13-B03
对同一序列计算 AMSGrad 的 running maximum denominator；比较第 2、3 步对负梯度的缩放。

## C. 推导与证明

### TRN13-C01
证明每周期总斜率 $C-2>0$ 时，任意整周期数的累计线性目标在 $x=-1$ 最小。

### TRN13-C02
解释为何证明中常需要控制“有效学习率”的跨时刻变化；写出一个代表性单调条件。

### TRN13-C03
证明 AMSGrad 的 $\hat v_t^{\max}=\max(\hat v_{t-1}^{\max},\tilde v_t)$ 逐坐标非减；它为何阻止大历史二阶矩被完全遗忘？

## D. 边界、反例与纠错

### TRN13-D01
反驳：“AMSGrad 分母单调，所以参数一定收敛到全局最优。”

### TRN13-D02
经典反例使用投影、线性凸损失和特定超参数。为什么删除这些条件后不能仍声称复现了同一定理反例？

### TRN13-D03
给出“经验上 Adam 表现好”与“在线 convex regret guarantee”可同时成立/失败而不矛盾的解释。

## E. AI 迁移

### TRN13-E01
把经典三周期反例做成最小可执行审计，应记录哪些轨迹和断言？

### TRN13-E02
在真实模型比较 Adam 与 AMSGrad，如何防止把额外状态/不同 kernel 的系统代价遗漏？

### TRN13-E03
阅读一个新优化器的“convergence theorem”时，给出假设—结论—外推三栏审计模板。

## 作答与复盘

先写 protocol、comparator 与 quantifier，再看结论。独立完成后打开 [[解答 - Adam 收敛反例、AMSGrad 与条件化保证]]。
