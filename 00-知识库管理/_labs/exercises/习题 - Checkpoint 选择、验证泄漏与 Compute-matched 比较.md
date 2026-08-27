---
type: exercise
status: verified
area: [training, model-selection, benchmarking]
topic: "[[Checkpoint 选择、验证泄漏与 Compute-matched 比较]]"
solution: "[[解答 - Checkpoint 选择、验证泄漏与 Compute-matched 比较]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Checkpoint 选择、验证泄漏与 Compute-matched 比较

## A. 识别与复述

### TRN71-A01
为什么 evaluation cadence、patience、smoothing 和 tie-break 都属于 checkpoint selection procedure？

### TRN71-A02
区分 best validation、test at selected checkpoint 与 oracle best test。

### TRN71-A03
列出数据/更新、算术/系统、调参/开发、推理/部署四本预算。

## B. 手算与构造

### TRN71-B01
若 10 个独立 checkpoint 的 validation noise 都是均值 0、SD 0.1 的正态，解释选择最小值为何乐观；用 $E[\min Z_i]\approx-1.54$ 粗估偏差。

### TRN71-B02
方法 A 120k tok/s、30B tokens 达标，B 100k tok/s、20B 达标。计算 time-to-quality 与相对差异。

### TRN71-B03
A 启动 12 runs、4 失败，成功 time 为 8 个小时；B 启动 12 runs、1 失败，成功 time 为 10 个小时。说明为何成功均值不足，并给一个固定 12 小时预算的比较方案。

## C. 推导与证明

### TRN71-C01
在 $\widehat R_k=R+\varepsilon_k$ 且噪声非退化对称时，说明 $E[\min_k\widehat R_k]<R$。

### TRN71-C02
说明 nested CV 中 outer 与 inner folds 分别估计什么；为何不能把 inner best score 当最终性能。

### TRN71-C03
推导吞吐与收敛 token 共同决定 $T_{q^*}=N_{q^*}/r$，构造吞吐排序与 time-to-quality 排序相反的条件。

## D. 边界、反例与纠错

### TRN71-D01
反驳：“两方法都训练 100k steps，所以 compute matched。”

### TRN71-D02
反驳：“test 不参与梯度，所以可以反复用来挑配置。”

### TRN71-D03
反驳：“只要 throughput 提高，端到端训练一定更快。”

## E. AI 迁移

### TRN71-E01
为两个 LLM recipe 写冻结的 checkpoint/early-stop/test 协议。

### TRN71-E02
设计 token-matched、hardware-time-matched 与 total-R&D-matched 三个并列结果表。

### TRN71-E03
某方法在更密 evaluation 下取得更好 best validation。设计公平重评方案。
