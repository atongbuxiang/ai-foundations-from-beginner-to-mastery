---
type: exercise
status: verified
area: [language-models, pretraining-data, contamination]
topic: "[[Benchmark 污染、时间截止与成员重叠审计]]"
solution: "[[解答 - Benchmark 污染、时间截止与成员重叠审计]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Benchmark 污染、时间截止与成员重叠审计

## A. 识别与复述

### LM20-A01
区分 exposure、memorization、retrieval 与 exploitation。

### LM20-A02
列出 benchmark input/label/rationale/template 五种成员单位。

### LM20-A03
exact、n-gram、semantic 与 black-box detector 各有什么盲点？

## B. 手算与构造

### LM20-B01
$\pi=2\%,r=90\%,f=1\%$，算 detector 阳性的污染后验。

### LM20-B02
给 draft/release/crawl/cutoff/eval 五个日期，判断直接 exposure 是否时间上可能并列例外。

### LM20-B03
dirty 组 80% 正确、clean 组 60%，构造 item difficulty 混杂使 20 点差非因果。

## C. 推导与证明

### LM20-C01
由 Bayes 推导 $P(C=1\mid+)$。

### LM20-C02
用因果反事实说明 clean/dirty gap 为何不识别污染增益。

### LM20-C03
说明 detector 有 label noise 时 observed overlap rate 对 true rate 的偏差。

## D. 边界、反例与纠错

### LM20-D01
反驳“exact overlap=0 就是无污染”。

### LM20-D02
反驳“检测到 overlap 就证明模型靠记忆答对”。

### LM20-D03
指出用 test set 反复调 decontamination threshold 的 adaptive leakage。

## E. AI 迁移

### LM20-E01
设计含 pretrain/SFT/RAG 的 cutoff 与 exclusion manifest。

### LM20-E02
设计 detector calibration set 与 threshold report。

### LM20-E03
审计模型卡中“训练截止早于 benchmark，所以绝无污染”。

独立完成后查看[[解答 - Benchmark 污染、时间截止与成员重叠审计]]。

