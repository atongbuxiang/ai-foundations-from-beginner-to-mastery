---
type: exercise
status: verified
area: [language-models, evaluation, calibration]
topic: "[[Proper Scoring、Calibration、ECE 与 Selective Generation]]"
solution: "[[解答 - Proper Scoring、Calibration、ECE 与 Selective Generation]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Proper Scoring、Calibration、ECE 与 Selective Generation

## A. 识别与复述

### LM60-A01
定义 binary calibration，并说明概率必须绑定到明确事件与总体。

### LM60-A02
区分 Brier score、log loss、ECE 与 accuracy。

### LM60-A03
定义 coverage、selective risk 与 risk–coverage curve。

## B. 手算与构造

### LM60-B01
对预测 $(p,y)=(.8,1),(.7,0),(.2,0)$ 计算平均 binary Brier score。

### LM60-B02
两个等频 bin 的 $(\mathrm{conf},\mathrm{acc},n)$ 分别为 $(.25,.20,40)$ 与 $(.80,.65,60)$，计算 ECE。

### LM60-B03
五个样本按置信度从高到低的错误指示为 $(0,0,1,0,1)$。计算 coverage 为 $.4,.6,1$ 时的 selective risk。

## C. 推导与证明

### LM60-C01
证明在 $Y\sim\mathrm{Bernoulli}(q)$ 下，期望 Brier loss 由 $p=q$ 唯一最小化。

### LM60-C02
证明温度缩放保持 logits 的类别 argmax，但一般改变 NLL 与 calibration。

### LM60-C03
说明有限分箱 ECE 为何可能被两个不同可靠性函数共享，并据此解释其非唯一性。

## D. 边界、反例与纠错

### LM60-D01
构造 accuracy 相同但 Brier/log loss 显著不同的两个预测器。

### LM60-D02
反驳“ECE 很小，所以模型适合自动做高风险决策”。

### LM60-D03
解释用 token 平均概率直接当“整段答案事实正确概率”的问题。

## E. AI 迁移

### LM60-E01
为问答系统定义 answer-level correct event 与 claim-level supported event 的两套校准表。

### LM60-E02
设计 validation temperature scaling，列出不可泄漏给校准器的信息。

### LM60-E03
为 selective generation 选择阈值，使 risk 不超过预注册上限并报告不确定性。

独立完成后查看[[解答 - Proper Scoring、Calibration、ECE 与 Selective Generation]]。
