---
type: exercise
status: draft
area: [learning-theory/empirical-process, learning-theory/loss-composition]
topic: "[[收缩引理与 Lipschitz 损失复合]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[Rademacher 复杂度与经验复杂度]]", "[[光滑性、强凸性与条件数]]"]
related: ["[[解答 - 收缩引理与 Lipschitz 损失复合]]", "[[范数约束线性类的复杂度]]"]
solution: "[[解答 - 收缩引理与 Lipschitz 损失复合]]"
created: 2026-08-23
updated: 2026-08-23
---

# 习题 - 收缩引理与 Lipschitz 损失复合

> [!abstract] 训练目标
> 能对齐 contraction convention，计算常见 loss 的 Lipschitz 常数，把 score complexity传递到 loss risk，并识别平方损失、vector logits、calibration 与 temperature 的边界。

## A. 识别与复述

### LT-CON-A01

陈述正文 factor-2 coordinate contraction lemma，包括 $A,\phi_i,L$ 与零点条件。

### LT-CON-A02

解释为什么把 $\phi_i$ 换成 $\psi_i(t)=\phi_i(t)-\phi_i(0)$ 不改变 signed empirical complexity。

### LT-CON-A03

区分 loss Lipschitz、gradient Lipschitz/smoothness、bounded loss 与 calibrated surrogate。

## B. 手算与数值判断

### LT-CON-B01

计算 absolute、hinge 与 binary logistic margin loss 对 score 的 Lipschitz 常数。

### LT-CON-B02

若 $|t|,|y|\le3$，平方损失对 prediction 的 Lipschitz 常数可取多少？若 $\widehat{\mathfrak R}(\mathcal F)=0.02$，正文 contraction 上界是多少？

### LT-CON-B03

margin ramp 的 $\gamma=0.25$，score complexity 为 0.03。计算 loss complexity 的 factor-2 contraction 上界；讨论 $\gamma$ 减半后的变化。

## C. 推导与证明

### LT-CON-C01

证明 centering identity，并说明固定常数项为何能移出 supremum。

### LT-CON-C02

用一坐标 conditioning/maximizer 比较解释 contraction proof 的 induction step，指出 factor 2 来自哪里。

### LT-CON-C03

从 empirical Rademacher risk theorem 与 factor-2 contraction 推出

$$
P\ell_f\le P_m\ell_f+4L\widehat{\mathfrak R}(\mathcal F)+3\sqrt{\log(2/\delta)/(2m)}.
$$

列出成立所需范围条件。

## D. 边界、反例与纠错

### LT-CON-D01

证明平方损失不是全局 Lipschitz；给定任意 $L$，构造 $u,v,y$ 使差商大于 $L$。

### LT-CON-D02

说明 softmax cross-entropy 为什么不是把 scalar contraction 对 $K$ 个 logits 各用一次即可解决。至少列出 vector geometry、class coupling 与 range 三项。

### LT-CON-D03

构造 surrogate population gap 很小但不能仅凭 contraction 得到 task-risk gap 的逻辑说明；指出缺失的 theorem 类型。

## E. AI 迁移

### LT-CON-E01

分析 temperature-scaled logistic/softmax loss 中 $\tau$ 对 Lipschitz constant 的影响，并说明低温度的复杂度代价。

### LT-CON-E02

区分 optimizer gradient clipping 与 prediction-to-loss Lipschitz。设计一段审计说明何时二者能通过 stability 发生联系。

### LT-CON-E03

InfoNCE 一项依赖 batch scores。写出 vector/batch-level function map，并列出应用 contraction 前需要固定的 norm、temperature 与 batch sampling 对象。
