---
type: exercise
status: verified
area: [language-models, evaluation, sampling]
topic: "[[Pass-at-k、Best-of-N、采样估计与选择偏差]]"
solution: "[[解答 - Pass-at-k、Best-of-N、采样估计与选择偏差]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Pass-at-k、Best-of-N、采样估计与选择偏差

## A. 识别与复述

### LM59-A01
区分单样本成功率、oracle pass@$k$、selector success 与端到端用户效用。

### LM59-A02
解释 HumanEval 组合估计量中的 $n,c,k$ 各表示什么。

### LM59-A03
说明 Best-of-$N$ 为什么同时改变覆盖率、选择误差与计算预算。

## B. 手算与构造

### LM59-B01
若 iid 单样本成功率 $p=0.2$，计算 $k=1,3,5$ 时至少一次成功的概率。

### LM59-B02
从 $n=10$ 个样本中观察到 $c=3$ 个通过，计算不放回抽 $k=2$ 个至少一个通过的组合估计。

### LM59-B03
有 4 个候选，真实效用 $(0,1,0,1)$，selector 分数 $(.9,.7,.6,.5)$。计算 oracle coverage 与 top-1 selected success。

## C. 推导与证明

### LM59-C01
由补事件推导 iid 情形的 $1-(1-p)^k$。

### LM59-C02
推导 $\widehat{\mathrm{pass@}k}=1-\binom{n-c}{k}/\binom nk$，并说明 $n-c<k$ 时的结果。

### LM59-C03
用最大值的噪声选择解释 winner's curse：为何被选候选的估计分数平均偏高。

## D. 边界、反例与纠错

### LM59-D01
构造 pass@10 很高但部署只返回一个错误答案的系统。

### LM59-D02
反驳“把 $N$ 增大到足够大就能免费提高质量”。

### LM59-D03
说明同一 prompt 的多样本相关时，iid 公式为什么可能低估或高估覆盖误差。

## E. AI 迁移

### LM59-E01
为代码生成比较设计 token/latency 等预算匹配协议。

### LM59-E02
设计 verifier 的独立 validation/test 审计，避免用隐藏测试选择答案。

### LM59-E03
为 self-consistency 实验定义 estimand、采样单位、聚合器与区间。

独立完成后查看[[解答 - Pass-at-k、Best-of-N、采样估计与选择偏差]]。
