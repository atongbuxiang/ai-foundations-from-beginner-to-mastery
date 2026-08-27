---
type: exercise
status: verified
area: [training, optimization, curvature]
topic: "[[Newton、Damping、Trust Region 与 Levenberg–Marquardt]]"
solution: "[[解答 - Newton、Damping、Trust Region 与 Levenberg–Marquardt]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Newton、Damping、Trust Region 与 Levenberg–Marquardt

> [!abstract] 训练目标
> 从局部二次模型推导 Newton、damped step 与 trust-region KKT 条件；能用 predicted/actual reduction 决定接受、拒绝和半径更新，而不是迷信“二阶”标签。

## A. 识别与复述

### TRN18-A01
写出二次模型 $m(p)=g^\top p+\tfrac12p^\top Bp$。Newton step、Tikhonov-damped step 与 trust-region step 分别解决什么问题？

### TRN18-A02
区分 curvature damping、目标函数中的 $L_2$ penalty 与 AdamW parameter decay；为什么相似的 $+\lambda$ 符号不能证明状态转移相同？

### TRN18-A03
定义 actual reduction、predicted reduction 与比值 $\rho$。解释为什么分母必须为正且足够大，才能把 $\rho$ 当作模型质量信号。

## B. 手算与构造

### TRN18-B01
取 $B=\operatorname{diag}(1,9)$、$g=(2,-3)^\top$。计算 Newton step；再取 $\lambda=3$ 计算 damped step，并说明两个 eigenmode 的收缩程度。

### TRN18-B02
一维 $m(p)=-2p-\tfrac12p^2$，约束 $|p|\le1$。求 trust-region 全局最优解、predicted reduction，并说明无约束驻点为何不是极小点。

### TRN18-B03
某步的旧 loss 为 10，新 loss 为 9.4，局部模型预测下降 0.5。求 $\rho$。若另一候选新 loss 为 10.1，预测仍下降 0.5，又得何值？给出常见接受/拒绝解释。

## C. 推导与证明

### TRN18-C01
在 $B\succ0$ 时，完成平方证明 $p_N=-B^{-1}g$ 是二次模型唯一极小点；说明 $B$ 仅可逆但不正定时证明在哪一步失效。

### TRN18-C02
在 $B=Q\operatorname{diag}(\mu_i)Q^\top$ 下推出 damped step 的 eigenmode 形式 $\tilde p_i=-\tilde g_i/(\mu_i+\lambda)$，并给出 $B+\lambda I\succ0$ 的条件。

### TRN18-C03
写出 Euclidean trust-region 子问题的 KKT 条件，解释 $\lambda(\|p\|-\Delta)=0$ 如何把 Newton 与边界解统一起来。

## D. 边界、反例与纠错

### TRN18-D01
给出一个不定 $B$ 的二维例子，使 Newton 方程有唯一解但该点是 saddle 或 maximizer；说明“线性方程解出”不是下降证书。

### TRN18-D02
反驳：“只要把 damping 调得足够大，训练一定更快。”从模型偏差、步长、数值稳定与 wall-clock 四方面回答。

### TRN18-D03
构造 predicted reduction 极小或为非正的场景，说明直接计算 $\rho=\text{ared}/\text{pred}$ 会如何失真，并提出防护规则。

## E. AI 迁移

### TRN18-E01
为大模型二阶/近二阶更新设计 trust-region 日志字段，至少覆盖 model decrease、真实 loss、半径/阻尼、步范数、退出原因与重试。

### TRN18-E02
如何在含 dropout 与随机数据增强的训练中测量 actual reduction，避免把随机 realization 的变化误当成局部模型误差？

### TRN18-E03
设计 LM/Gauss–Newton 与 AdamW 的公平实验：列出预算、调参、停止、失败计数和资源指标；说明为何只按 iteration 对齐不公平。

## 作答与复盘

每题记录 `independent / hinted / copied / blocked / careless`。完成后用一张表同时写出“方程、约束、globalization signal、失败出口”，再打开 [[解答 - Newton、Damping、Trust Region 与 Levenberg–Marquardt]]。
