---
type: exercise
status: draft
area: [learning-theory/margin, classification/svm]
topic: "[[分类间隔、Margin Bound 与 SVM 接口]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[收缩引理与 Lipschitz 损失复合]]", "[[范数约束线性类的复杂度]]"]
related: ["[[解答 - 分类间隔、Margin Bound 与 SVM 接口]]", "[[支持向量机、最大间隔与核方法]]"]
solution: "[[解答 - 分类间隔、Margin Bound 与 SVM 接口]]"
created: 2026-08-23
updated: 2026-08-23
---

# 习题 - 分类间隔、Margin Bound 与 SVM 接口

> [!abstract] 训练目标
> 能从 signed margin、ramp sandwich 与 contraction 推出风险界，计算 linear/SVM 的 functional/geometric margin，并审计 scale、阈值选择、多分类与 robust margin 的边界。

## A. 识别与复述

### LT-MAR-A01

定义 binary functional margin 与 affine-linear geometric margin；说明二者在 $(w,b)\mapsto(cw,cb)$ 下怎样变化。

### LT-MAR-A02

写出 $\phi_\gamma$ ramp loss 的分段定义，并陈述它与 $\mathbf1\{u\le0\}$、$\mathbf1\{u\le\gamma\}$ 的 sandwich。

### LT-MAR-A03

区分 margin generalization、SVM optimization 与 surrogate calibration 各自控制什么。

## B. 手算与数值判断

### LT-MAR-B01

给定 margins $(-0.4,0.1,0.3,0.8,1.2)$，分别计算 training error、$\gamma=0.5$ 的低 margin 比例和平均 ramp loss。

### LT-MAR-B02

取 $w=(3,4)$、$b=-1$、$x=(2,1)$、$y=+1$。计算 functional 与 geometric margin；再把 $(w,b)$ 乘以 10，重复计算。

### LT-MAR-B03

取 $m=1000$、$\widehat{\mathfrak R}=0.02$、$\gamma=0.5$、经验低 margin 比例 $0.08$、$\delta=0.05$。按正文安全 bound 计算分类风险上界。

## C. 推导与证明

### LT-MAR-C01

逐段证明 ramp sandwich 与 $1/\gamma$-Lipschitz 性。

### LT-MAR-C02

从 Rademacher risk theorem、margin-class sign invariance 与 factor-$2$ contraction 完整推出正文 margin bound。

### LT-MAR-C03

从“最大化最小 geometric margin”推导 hard-margin SVM primal；再消去 slack，得到 soft-margin hinge objective。

## D. 边界、反例与纠错

### LT-MAR-D01

构造两个 training error 都为 0、minimum margin相同，但 empirical margin distribution明显不同的分类器。

### LT-MAR-D02

说明为什么观察同一数据后从连续 $\gamma$ 中挑最小 bound 不能直接引用 fixed-$\gamma$ theorem；给出有限网格修正。

### LT-MAR-D03

反驳“把 logits 全部乘 100 会无条件改善 margin generalization certificate”，指出必须同步变化的 complexity/radius。

## E. AI 迁移

### LT-MAR-E01

为 frozen encoder + linear probe 设计一张 margin certificate 记录表，至少列出七项必须报告的量。

### LT-MAR-E02

写出 multiclass logit margin，并解释 scalar binary contraction 为什么不足；列出需要替换的三个对象。

### LT-MAR-E03

若 score 对输入是 $L_x$-Lipschitz，证明 $Yf(x)>L_x\varepsilon$ 是半径 $\varepsilon$ 内不翻转的充分条件；说明它还不是 robust population bound。
