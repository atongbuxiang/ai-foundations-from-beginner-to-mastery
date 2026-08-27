---
type: exercise
status: verified
area: [language-models, decoding]
topic: "[[Logits、Softmax、Temperature 与 Categorical Sampling]]"
solution: "[[解答 - Logits、Softmax、Temperature 与 Categorical Sampling]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Logits、Softmax、Temperature 与 Categorical Sampling

## A. 识别与复述

### LM49-A01
区分 logit、softmax probability 与实际 rollout kernel。

### LM49-A02
说明 temperature 对排名、odds 与 entropy 的影响。

### LM49-A03
解释 categorical inverse-CDF sampling，并说明 token 顺序为何属于实现合同。

## B. 手算与构造

### LM49-B01
对 logits $(2,1,0)$ 计算 $\tau=1$ 的 softmax，保留四位小数。

### LM49-B02
两个 token 的 logit 差为 $1.4$；计算 $\tau=.7$ 与 $\tau=1.4$ 时的 odds ratio。

### LM49-B03
概率按 token-id 顺序为 $(.5,.3,.2)$。对 $U=.49,.50,.81$ 分别做 inverse-CDF 采样，采用区间左闭右开约定。

## C. 推导与证明

### LM49-C01
证明 softmax 对所有 logits 加同一常数不变。

### LM49-C02
令 $\beta=1/\tau$，推导 $dH/d\tau=\operatorname{Var}_\tau(z)/\tau^3$。

### LM49-C03
从条件概率链式法则推导自回归 sampler 的序列概率。

## D. 边界、反例与纠错

### LM49-D01
纠正“把 $\tau=0$ 直接代入 softmax 就得到 greedy”。

### LM49-D02
构造同 seed 但输出不同、且两实现都没有 bug 的服务案例。

### LM49-D03
反驳“temperature 和 top-$p$ 的执行顺序无关”。

## E. AI 迁移

### LM49-E01
为生产 sampling request 写最小分布与随机性日志合同。

### LM49-E02
设计检验某实现是否正确采样给定三分类分布的统计实验。

### LM49-E03
设计 temperature sweep，避免把样本多样性误称为事实质量。

独立完成后查看[[解答 - Logits、Softmax、Temperature 与 Categorical Sampling]]。
