---
type: exercise
status: draft
topic: "[[Online-to-Batch Conversion]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Online-to-Batch Conversion]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - Online-to-Batch Conversion
## A
### LT-OTB-A01
写 iid online-to-batch filtration 与核心条件期望等式。
### LT-OTB-A02
区分 randomized iterate、averaged predictor 与 last iterate。
### LT-OTB-A03
expected regret 转 risk 时，expectation 分别覆盖哪些随机性？
## B
### LT-OTB-B01
$B_T=4\sqrt T$ 时求 excess-risk 项 ≤0.02 所需 $T$。
### LT-OTB-B02
三个 predictors 的 risks 为 $(0.1,0.2,0.6)$，随机 iterate 的 expected risk 是多少？
### LT-OTB-B03
给前 $T-1$ 个 risk 0、最后一个 risk 1，比较 average 与 last risk。
## C
### LT-OTB-C01
完整证明随机 iterate 的 expected excess-risk bound。
### LT-OTB-C02
在 convex prediction/loss 下用 Jensen 证明平均预测器 bound。
### LT-OTB-C03
推导 bounded loss 下 martingale high-probability bridge，并分开 comparator deviation。
## D
### LT-OTB-D01
$h_t$ 在更新后才对同一 $Z_t$ 评分。指出泄漏和条件期望断点。
### LT-OTB-D02
从训练产生的所有 checkpoints 中用同一在线 losses 选最优。为什么 fixed-comparator 浓缩不够？
### LT-OTB-D03
随机无放回 shuffle、时间序列和 concept drift 各需怎样改桥梁？
## E
### LT-OTB-E01
为流式 LLM 微调设计 test-then-train protocol 与 checkpoint output rule。
### LT-OTB-E02
何时 prediction averaging 合法，何时 parameter averaging 需要独立论证？
### LT-OTB-E03
写 online-to-batch claim card：sample law、filtration、regret、output、confidence 与 selection。
