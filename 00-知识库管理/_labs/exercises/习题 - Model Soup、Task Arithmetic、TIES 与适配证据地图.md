---
type: exercise
status: verified
area: [language-models, model-merging, task-arithmetic, ties]
topic: "[[Model Soup、Task Arithmetic、TIES 与适配证据地图]]"
solution: "[[解答 - Model Soup、Task Arithmetic、TIES 与适配证据地图]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Model Soup、Task Arithmetic、TIES 与适配证据地图

## A. 识别与复述

### LM32-A01
参数合并需要哪些坐标、base、tokenizer 前提？

### LM32-A02
区分 uniform/greedy soup、task arithmetic 与 output ensemble。

### LM32-A03
TIES 的 trim、elect sign、merge 各做什么？

## B. 手算与构造

### LM32-B01
$\theta_0=(1,1),\theta_1=(2,0),\theta_2=(1,3)$，算 uniform soup 与 task-vector sum。

### LM32-B02
TIES 坐标 updates $(.8,.6,-.1)$，trim $|v|<.2$、sum-elect、mean-aligned，算 merged。

### LM32-B03
updates $(-.7,.5,-.6)$ 按同规则算，并与普通均值比较。

## C. 推导与证明

### LM32-C01
用一阶 Taylor 解释 task-vector addition 的局部近似，并写二阶失效项。

### LM32-C02
证明多个 LoRA deltas 的 rank 上界不超过 ranks 之和。

### LM32-C03
定义两 checkpoint 的线性插值 barrier。

## D. 边界、反例与纠错

### LM32-D01
构造两个功能等价但 hidden units 置换后直接平均失败的网络。

### LM32-D02
反驳“sign conflict 消失就没有任务冲突”。

### LM32-D03
指出 greedy soup 在 validation 上的选择偏差。

## E. AI 迁移

### LM32-E01
设计 base/task-vector/merge serialization oracle。

### LM32-E02
写多任务 merge 的逐任务/OOD/安全评估矩阵。

### LM32-E03
审计只报平均分、未报 ingredients/search/coefficients 的合并研究。

独立完成后查看[[解答 - Model Soup、Task Arithmetic、TIES 与适配证据地图]]。

