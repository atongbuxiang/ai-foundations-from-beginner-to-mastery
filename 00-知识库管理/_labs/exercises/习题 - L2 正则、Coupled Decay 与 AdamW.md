---
type: exercise
status: verified
area: [training, optimization, regularization]
topic: "[[L2 正则、Coupled Decay 与 AdamW]]"
solution: "[[解答 - L2 正则、Coupled Decay 与 AdamW]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - L2 正则、Coupled Decay 与 AdamW

> [!abstract] 训练目标
> 从更新合同而非参数名区分 L2、coupled decay 与 decoupled decay；能推导累计收缩、各向异性和 Weight RMS 缩放律的适用边界。

## A. 识别与复述

### TRN15-A01
写出目标中加入 $\lambda\|\theta\|^2/2$ 后的梯度；说明在普通 SGD 中它何时等价于乘法 weight decay。

### TRN15-A02
写出预条件优化器中的 coupled L2 与 AdamW 式 decoupled decay 一步更新，标出正则项是否进入 $m,v$。

### TRN15-A03
为什么仅看到配置项 `weight_decay=0.01` 不能判断实际数学合同？

## B. 手算与构造

### TRN15-B01
令任务梯度为零，$P=\operatorname{diag}(1,0.1)$，$\theta=(1,1)$，$\eta=0.1,\lambda=0.2$。分别计算 coupled preconditioned shrink 与 AdamW shrink。

### TRN15-B02
固定 $\eta\lambda=0.01$，连续 100 步纯 AdamW decay 后权重倍率是多少？与 $e^{-1}$ 比较。

### TRN15-B03
学习率依次为 $0.1,0.05,0.01$，$\lambda=0.2$。求三步精确累计 decay multiplier，并给一阶指数近似。

## C. 推导与证明

### TRN15-C01
证明普通 SGD 对 $L(\theta)+\lambda\|\theta\|^2/2$ 的一步更新等于先做 task gradient 再乘加 $-\eta\lambda\theta$；说明有 momentum 时为何“进入动量”仍会破坏简单等价。

### TRN15-C02
证明变学习率 AdamW 的纯 decay 轨迹为 $\theta_T=\theta_0\prod_{t=1}^T(1-\eta_t\lambda_t)$；推导小步长的指数近似及误差阶。

### TRN15-C03
在线性随机递推 $\theta_{t+1}=(1-\eta\lambda)\theta_t-\eta u_t$ 中，设 $u_t$ 零均值、独立、方差 1。推导稳态方差并得到小 $\eta\lambda$ 下的 Weight RMS 近似。

## D. 边界、反例与纠错

### TRN15-D01
构造二维对角预条件器例子，反驳“L2 正则与 weight decay 对所有优化器都等价”。

### TRN15-D02
反驳：“decoupled 表示 decay 与学习率无关。”

### TRN15-D03
Weight RMS 公式 $\sqrt{\eta/(2\lambda)}$ 为什么不是所有网络层的精确预测？至少列五项假设或断点。

## E. AI 迁移

### TRN15-E01
为 transformer 参数分组制定 decay 审计表：哪些参数通常需要单独决定，为什么不能靠名称猜？

### TRN15-E02
设计一次检验 Weight RMS 缩放律的实验，要求区分稳态、有限时间和初始化效应。

### TRN15-E03
比较两个训练 recipe 的 weight decay 时，怎样把 LR schedule 与累计 shrink 对齐，而不是只比较 $\lambda$？

## 作答与复盘

必须写清 `task gradient / preconditioner / decay / state` 的顺序。独立完成后打开 [[解答 - L2 正则、Coupled Decay 与 AdamW]]。
