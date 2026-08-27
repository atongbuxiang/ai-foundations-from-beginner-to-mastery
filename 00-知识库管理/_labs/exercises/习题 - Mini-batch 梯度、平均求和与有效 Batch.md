---
type: exercise
status: verified
area: [training, optimization, statistics]
topic: "[[Mini-batch 梯度、平均求和与有效 Batch]]"
solution: "[[解答 - Mini-batch 梯度、平均求和与有效 Batch]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Mini-batch 梯度、平均求和与有效 Batch

## A. 识别与复述

### TRN02-A01
写出 empirical full gradient、batch mean gradient 和 batch sum gradient，并比较三者期望。

### TRN02-A02
variance 按 $1/B$ 与 standard deviation 按 $1/\sqrt B$ 有何区别？

### TRN02-A03
区分 nominal batch、effective batch 与 critical batch。

## B. 手算与构造

### TRN02-B01
一维 gradients 为 $\{-1,1,3,5\}$。求总体均值、分母为 $N$ 的 variance，以及 with-replacement $B=2$ 的 batch-mean variance。

### TRN02-B02
用同一总体计算 without-replacement $B=2$ 的 covariance，并检查 $B=N$ 端点。

### TRN02-B03
权重 $a=(0.8,0.1,0.1)$，求 $B_{eff}=1/\sum a_i^2$；解释为何不等于 3。

## C. 推导与证明

### TRN02-C01
从独立 centered gradients 出发推导 $\operatorname{Cov}(\widehat G_B)=C/B$，明确 cross terms 为什么为零。

### TRN02-C02
证明 mean-SGD 与 sum-SGD 的单步等价要求 $\eta_{sum}=\eta_{mean}/B$。

### TRN02-C03
推导归一化加权平均的 covariance $C\sum_i a_i^2$，说明用了哪些同分布/独立条件。

## D. 边界、反例与纠错

### TRN02-D01
给出两个完全相关样本使 variance 不按 $1/B$ 降低的反例。

### TRN02-D02
构造 sequence-mean 与 token-mean 给不同 gradient 的最小变长序列例子。

### TRN02-D03
反驳：“world size 翻倍，所以有效 batch 必然翻倍。”列出 reduction、重复样本和相关性反例。

## E. AI 迁移

### TRN02-E01
local batch 4、world size 8、accumulation 16，每 sequence 1024 tokens 且无 mask，求 global sequences/tokens per optimizer step。

### TRN02-E02
设计 Monte Carlo 验证 $1/B$ covariance 与 finite-population correction，说明 seeds、重复次数和误差指标。

### TRN02-E03
审计论文中“batch=4096”：提出至少八个澄清问题，使该数字可与另一训练对比。

## 作答与复盘

逐题记录作答状态；完成独立尝试后打开 [[解答 - Mini-batch 梯度、平均求和与有效 Batch]]。
