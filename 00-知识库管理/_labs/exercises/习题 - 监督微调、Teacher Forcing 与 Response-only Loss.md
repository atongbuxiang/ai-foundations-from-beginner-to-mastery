---
type: exercise
status: verified
area: [language-models, supervised-finetuning, teacher-forcing]
topic: "[[监督微调、Teacher Forcing 与 Response-only Loss]]"
solution: "[[解答 - 监督微调、Teacher Forcing 与 Response-only Loss]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - 监督微调、Teacher Forcing 与 Response-only Loss

## A. 识别与复述

### LM26-A01
定义 teacher forcing，并写它与自由生成的条件历史差别。

### LM26-A02
区分 input、shifted label、attention relation 与 loss mask。

### LM26-A03
Full-sequence 与 response-only loss 的 estimand 各是什么？

## B. 手算与构造

### LM26-B01
对 [U,q,A,a,b,EOS] 写 inputs、labels 与只监督 a,b,EOS 的 mask。

### LM26-B02
两设备 $(N,D)=(12,6),(9,3)$，算 global target mean 与等设备 mean。

### LM26-B03
两 turns 的 $(N,D)=(4,4),(6,2)$，算 per-token 与 per-turn mean。

## C. 推导与证明

### LM26-C01
由 $p(y\mid x)$ 的链式法则推导 response-only token NLL。

### LM26-C02
证明 global $N/D$ 使每个有效 target 等权。

### LM26-C03
说明 response-only mask 不等于阻止 assistant 读取 prompt。

## D. 边界、反例与纠错

### LM26-D01
反驳“response-only 总比 full-sequence 更正确”。

### LM26-D02
构造截断后 $D=0$ 的样本并给处理方案。

### LM26-D03
反驳“Teacher forcing 的分布差证明所有生成错误都来自 exposure bias”。

## E. AI 迁移

### LM26-E01
设计 shift/mask/global-reduction 的最小 oracle。

### LM26-E02
审计只报告 SFT epochs、未报告 effective targets 的训练。

### LM26-E03
预注册 full vs response-only 的预算匹配实验。

独立完成后查看[[解答 - 监督微调、Teacher Forcing 与 Response-only Loss]]。

