---
type: exercise
status: verified
area: [language-models, safety, abstention, refusal]
topic: "[[Abstention、Refusal、Over-refusal 与风险覆盖]]"
solution: "[[解答 - Abstention、Refusal、Over-refusal 与风险覆盖]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Abstention、Refusal、Over-refusal 与风险覆盖

## A. 识别与复述

### LM69-A01
区分 abstain、refuse、safe-complete 与 escalate。

### LM69-A02
定义 selective coverage 与 selective risk。

### LM69-A03
解释 correctness confidence 与 safety risk 为什么应分开。

## B. 手算与构造

### LM69-B01
八个样本按 correctness score 从高到低的错误指示为 $(0,1,0,0,1,0,1,1)$。计算 coverage $.25,.5,1$ 时的 risk。

### LM69-B02
Harmful/benign 请求各 100 个。系统在 harmful 上回答 12 个，在 benign 上拒答 18 个。计算 unsafe answer rate、harmful recall、over-refusal 与 benign utility。

### LM69-B03
组 A/B 的已回答错误数/已回答数/总数分别为 $4/80/100$ 与 $2/20/100$。计算各组 coverage 与 selective risk，并解释总体可能掩盖什么。

## C. 推导与证明

### LM69-C01
说明单调变换 confidence 可保持 risk–coverage 排序而改变数值校准。

### LM69-C02
写出代价敏感多动作 Bayes 决策，并解释为什么没有通用最佳拒答阈值。

### LM69-C03
解释在 validation 扫阈值后直接报告同一集最低 risk 为什么乐观。

## D. 边界、反例与纠错

### LM69-D01
反驳“回答样本 accuracy 99%，所以系统可靠”。

### LM69-D02
构造事实置信很高但仍应拒答，以及事实置信很低但不应以安全理由拒答的例子。

### LM69-D03
某组 risk 更低但 coverage 只有 5%。解释为什么不能直接称其更公平。

## E. AI 迁移

### LM69-E01
为高风险问答设计 answer/abstain/refuse/safe-complete/escalate 代价表。

### LM69-E02
写阈值选择、冻结、测试与线上失效协议。

### LM69-E03
设计 over-refusal 的 benign paired set 与群体报告。

独立完成后查看[[解答 - Abstention、Refusal、Over-refusal 与风险覆盖]]。
