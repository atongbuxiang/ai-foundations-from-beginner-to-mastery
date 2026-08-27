---
type: exercise
status: verified
area: [language-models, evaluation, robustness]
topic: "[[Contamination、Prompt Sensitivity、Robustness 与不确定性]]"
solution: "[[解答 - Contamination、Prompt Sensitivity、Robustness 与不确定性]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Contamination、Prompt Sensitivity、Robustness 与不确定性

## A. 识别与复述

### LM63-A01
区分 exposure、memorization 与 exploitation。

### LM63-A02
列出 exact、near-duplicate、semantic、label/answer 与 benchmark-format contamination。

### LM63-A03
区分 prompt 平均表现、worst-case、方差与 best-prompt 分数。

## B. 手算与构造

### LM63-B01
三个 prompt 的 accuracy 为 $(.8,.6,.4)$。计算均值、population standard deviation、range 与 worst-case。

### LM63-B02
模型在 canonical order 上正确 80/100，在每题随机置换后的 5 次重复共正确 310/500。计算两种 accuracy 与差值。

### LM63-B03
item 1 有五个 prompt 得分 $(1,1,1,1,0)$，item 2 只有一个 prompt 得分 $(0)$。计算把 6 格当独立 observation 的均值，以及先按 item 平均再等权的均值。

## C. 推导与证明

### LM63-C01
写出 item×prompt×seed 的分层随机效应分解，并解释每个方差分量。

### LM63-C02
说明 canonical-order performance drop 为何不是训练污染的充分条件。

### LM63-C03
推导 paired permutation test 的交换原理，并说明配对单位应是什么。

## D. 边界、反例与纠错

### LM63-D01
构造完全没有训练污染但 canonical-order probe 仍显著的模型。

### LM63-D02
反驳“exact string overlap 为零就证明 benchmark 干净”。

### LM63-D03
说明在 100 个 prompt 中挑最佳一个后不校正地报告结果会造成什么偏差。

## E. AI 迁移

### LM63-E01
为闭源 API 设计不需要训练语料访问的污染证据组合。

### LM63-E02
设计 prompt family 的预注册与 hierarchical bootstrap。

### LM63-E03
设计版本回归矩阵，区分 model、template、decoder 与 judge 改动。

独立完成后查看[[解答 - Contamination、Prompt Sensitivity、Robustness 与不确定性]]。
