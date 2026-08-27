---
type: exercise
status: verified
area: [language-models, evaluation]
topic: "[[语言模型评估对象、任务单位与 Benchmark 合同]]"
solution: "[[解答 - 语言模型评估对象、任务单位与 Benchmark 合同]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - 语言模型评估对象、任务单位与 Benchmark 合同

## A. 识别与复述

### LM57-A01
用总体、配置、生成随机性和效用函数写出一个语言模型评估 estimand，并逐项解释。

### LM57-A02
区分条件模型、解码行为、工具系统和在线产品四个被评对象。

### LM57-A03
解释 sampling unit、observation 与独立 cluster 为什么可能不是同一层。

## B. 手算与构造

### LM57-B01
任务 A 有 $20/25$ 正确，任务 B 有 $3/15$ 正确。分别计算 task-macro 与 example-micro accuracy。

### LM57-B02
用户甲有 4 个请求，得分 $(1,1,1,0)$；用户乙有 1 个请求，得分 $0$。计算 request-average 与 user-average。

### LM57-B03
100 题中 6 次 timeout、4 次 parser failure；其余 90 题中 72 题正确。计算“删除失败后的 accuracy”和“失败记零的端到端 accuracy”。

## C. 推导与证明

### LM57-C01
证明两阶段抽样下，先求每用户均值再平均与直接把所有请求平均一般不相等，并给出相等条件。

### LM57-C02
把有限 benchmark、每题 $R$ 次随机生成的估计量写成双重平均，并指出题目不确定性与生成不确定性的来源。

### LM57-C03
说明为何删除 timeout 后估计的是条件期望，而不是所有请求的总体期望。

## D. 边界、反例与纠错

### LM57-D01
反驳“同一个 checkpoint 的 benchmark 分数是模型固有常数”。

### LM57-D02
构造 micro 上系统 A 优于 B、macro 上 B 优于 A 的例子。

### LM57-D03
解释 validation 上挑过 prompt 后再把同一 split 称为无偏 test 的问题。

## E. AI 迁移

### LM57-E01
为一个 RAG 问答 benchmark 写最小 run manifest。

### LM57-E02
为多轮客服系统设计以 user 为 cluster 的评估抽样与区间协议。

### LM57-E03
把“模型 A 得 82 分，所以更好”改写成可审计的比较主张。

独立完成后查看[[解答 - 语言模型评估对象、任务单位与 Benchmark 合同]]。
